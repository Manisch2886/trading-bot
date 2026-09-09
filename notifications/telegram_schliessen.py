"""
Telegram-Ablauf "/schliessen" - manuelles Schliessen mit doppelter Bestaetigung
==============================================================================
Die Telegram-Schicht ueber manual_close.py. Sie entscheidet nichts und
schreibt nichts selbst; sie fuehrt den Nutzer durch drei Schritte und ruft
am Ende genau eine Funktion auf.

    /schliessen [bot]        Liste der offenen Positionen, je eine Schaltflaeche
      -> Antippen             Zusammenfassung + "Ja, schliessen" / "Abbrechen"
      -> "Ja, schliessen"     Aufforderung, BESTAETIGEN einzutippen
      -> "BESTAETIGEN"        erst JETZT wird geschrieben

Die beiden Bestaetigungen sind bewusst von UNTERSCHIEDLICHER ART: ein Tipp
auf eine Schaltflaeche und eine getippte Eingabe. Zweimal dieselbe Geste
waere kaum eine zweite Huerde - wer einmal danebentippt, tippt auch zweimal
daneben. Ein Wort abtippen zu muessen unterbricht das.

Zeitliche Begrenzung: eine angefangene Bestaetigung verfaellt nach
BESTAETIGUNG_GUELTIG_SEKUNDEN. Ohne das koennte ein "Ja" von heute Morgen
am Abend noch eine Position zu einem laengst veralteten Kurs schliessen.

WELCHER KURS GESCHRIEBEN WIRD: der, den der Nutzer in der Zusammenfassung
gesehen und bestaetigt hat - NICHT ein beim Ausfuehren neu geholter. Er
bestaetigt eine konkrete Zahl; still zu einer anderen zu schliessen waere
die groessere Ueberraschung. Deshalb das kurze Zeitfenster.
"""

import asyncio
import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import manual_close
import monitor

logger = logging.getLogger(__name__)

# Wie lange eine angefangene Bestaetigung gilt.
BESTAETIGUNG_GUELTIG_SEKUNDEN = 120

# Schluessel im per-Nutzer-Speicher von python-telegram-bot.
WARTET_AUF_TEXT = "schliessen_wartet_auf_text"

# Praefixe der Schaltflaechen-Daten. Telegram erlaubt 64 Byte je Knopf.
CB_WAEHLEN = "sw"        # Position ausgewaehlt
CB_BESTAETIGEN = "sb"    # erste Bestaetigung
CB_ABBRECHEN = "sx"      # Abbruch


def _kurs(symbol: str, kurse: dict):
    eintrag = (kurse or {}).get(symbol)
    if isinstance(eintrag, dict):
        return eintrag.get("price")
    return eintrag


def formatiere_liste(bot_name: str, positionen: list, kurse: dict) -> str:
    """Die Positionsliste als Nachrichtentext. Ohne offene Position gibt es
    nichts zu schliessen - dann sagt die Nachricht genau das."""
    anzeige = manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"]
    if not positionen:
        return f"*{anzeige}*\n\nKeine offenen Positionen - nichts zu schliessen."

    zeilen = [f"*{anzeige}* - {len(positionen)} offene Position(en)", ""]
    for p in positionen:
        kurs = _kurs(p["symbol"], kurse)
        if kurs and p.get("entry_price"):
            pnl = manual_close.berechne_pnl(bot_name, p["entry_price"], kurs)
            kurs_text = f"{kurs:.4f}".rstrip("0").rstrip(".")
            # _pnl_emoji() liefert das Symbol bereits MIT Leerzeichen.
            bewertung = f"{monitor._pnl_emoji(pnl)}{pnl:+.2f}%"
        else:
            kurs_text, bewertung = "nicht verfuegbar", "PnL unbekannt"
        zeilen.append(
            f"`{p['symbol']}`  Entry {p['entry_price']}  |  aktuell {kurs_text}  "
            f"|  {bewertung}")
    zeilen.append("")
    zeilen.append("Zum Schliessen die Position antippen.")
    return "\n".join(zeilen)


def tastatur_liste(bot_name: str, positionen: list, kurse: dict):
    knoepfe = []
    for p in positionen:
        kurs = _kurs(p["symbol"], kurse)
        # Ohne Kurs KEINE Schaltflaeche: ohne Ausstiegskurs darf ohnehin
        # nicht geschrieben werden, und ein Knopf, der garantiert in einer
        # Fehlermeldung endet, ist schlechter als gar keiner.
        if not kurs:
            continue
        knoepfe.append([InlineKeyboardButton(
            f"{p['symbol']} schliessen",
            callback_data=f"{CB_WAEHLEN}:{bot_name}:{p['id']}")])
    knoepfe.append([InlineKeyboardButton(
        "Abbrechen", callback_data=f"{CB_ABBRECHEN}:-:-")])
    return InlineKeyboardMarkup(knoepfe)


def formatiere_zusammenfassung(bot_name, position, kurs, pnl) -> str:
    anzeige = manual_close.SCHLIESSBARE_BOTS[bot_name]["anzeigename"]
    return (
        f"⚠️ *Position schliessen?*\n\n"
        f"Bot: {anzeige}\n"
        f"Symbol: `{position['symbol']}`\n"
        f"Einstieg: {position['entry_price']}  ({position.get('entry_time')})\n"
        f"Ausstieg zum Kurs: *{kurs}*\n"
        f"Geschaetzter PnL: *{pnl:+.2f}%* (inkl. Gebuehren/Slippage)\n\n"
        f"Das schreibt in die Live-Datenbank des Bots und laesst sich nicht "
        f"rueckgaengig machen.")


def tastatur_bestaetigung(bot_name, trade_id):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("Ja, schliessen",
                              callback_data=f"{CB_BESTAETIGEN}:{bot_name}:{trade_id}"),
        InlineKeyboardButton("Abbrechen",
                              callback_data=f"{CB_ABBRECHEN}:-:-"),
    ]])


def text_aufforderung(position, kurs) -> str:
    return (
        f"Letzter Schritt.\n\n"
        f"Tippe genau `{manual_close.BESTAETIGUNGSTEXT}` (in Grossbuchstaben), "
        f"um `{position['symbol']}` zum Kurs {kurs} zu schliessen.\n\n"
        f"Jede andere Eingabe bricht ab. Gueltig fuer "
        f"{BESTAETIGUNG_GUELTIG_SEKUNDEN} Sekunden.")


def formatiere_erfolg(ergebnis: dict) -> str:
    return (
        f"✅ *Position geschlossen*\n\n"
        f"Symbol: `{ergebnis['symbol']}`\n"
        f"Ausstieg: {ergebnis['exit_price']}  ({ergebnis['exit_time']} UTC)\n"
        f"PnL: *{ergebnis['pnl_pct']:+.2f}%*\n"
        f"Vermerkt als: `{ergebnis['result']}`\n\n"
        f"Der Eingriff steht im Protokoll "
        f"(logs/notifications/manuelle_eingriffe.log).")


def merke_bestaetigung(user_data: dict, bot_name, position, kurs, pnl) -> None:
    user_data[WARTET_AUF_TEXT] = {
        "bot": bot_name,
        "trade_id": position["id"],
        "symbol": position["symbol"],
        "kurs": kurs,
        "pnl": pnl,
        "gueltig_bis": time.time() + BESTAETIGUNG_GUELTIG_SEKUNDEN,
    }


def offene_bestaetigung(user_data: dict):
    """Die wartende Bestaetigung - oder None, wenn keine da oder abgelaufen.
    Abgelaufene werden gleich entfernt, damit ein spaeter eintreffendes
    'BESTAETIGEN' nicht doch noch etwas ausloest."""
    eintrag = (user_data or {}).get(WARTET_AUF_TEXT)
    if not eintrag:
        return None
    if time.time() > eintrag["gueltig_bis"]:
        user_data.pop(WARTET_AUF_TEXT, None)
        return None
    return eintrag


def vergiss_bestaetigung(user_data: dict) -> None:
    (user_data or {}).pop(WARTET_AUF_TEXT, None)


def hole_position(bot_name: str, trade_id: int):
    for p in manual_close.offene_positionen(bot_name):
        if p["id"] == trade_id:
            return p
    return None


def kurse_fuer(bot_name: str, positionen: list) -> dict:
    """Live-Kurse fuer die offenen Symbole - ueber dieselbe Abfrage, die
    /status benutzt. Der Aufrufer muss das in einen Thread auslagern
    (siehe die Warnung in telegram_bot.py::status_command)."""
    symbole = sorted({p["symbol"] for p in positionen})
    if not symbole:
        return {}
    if manual_close.SCHLIESSBARE_BOTS[bot_name]["anlageklasse"] == "krypto":
        return monitor.fetch_binance_prices(symbole)
    return monitor.fetch_stock_prices(symbole)
