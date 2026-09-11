"""
Abgleich IBKR-Paper: Simulation gegen tatsaechliche Ausfuehrung
==============================================================================
Gegenstueck zu broker/abgleich.py. Die Simulation des Aktien-Bots rechnet mit

  * dem SCHLUSSKURS der Tageskerze als Einstieg bzw. Ausstieg (beim Stop-Exit
    mit dem Stop-Preis) - also mit einem Kurs, zu dem die Bruecke gar nicht
    handeln kann, weil die Boerse zu diesem Zeitpunkt schliesst,
  * pauschal 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT) = 0,30 Prozentpunkten Kosten.

EINFACHER ALS BEI KRYPTO, an genau einer Stelle: IBKR rechnet die Provision
immer in der Kontowaehrung (USD) ab, nie in der gekauften Aktie. Es bleibt
deshalb keine Restmenge liegen - verkauft wird genau die Stueckzahl, die gekauft
wurde. Die zwei getrennten Renditen der Binance-Bruecke (je Einheit gegen
eingesetztes Kapital) fallen hier zusammen; eine Stolperfalle weniger.

SCHWIERIGER ALS BEI KRYPTO, an einer anderen: die Bruecke kauft in der NAECHSTEN
Sitzung, nicht zum Schlusskurs des Signaltags. Die Abweichungsspalte enthaelt
deshalb zu einem grossen Teil die UEBERNACHT-LUECKE. Die Spalte "Verzug" nennt
die Zahl der Kalendertage zwischen der Entscheidung des Bots und der Ausfuehrung
- ohne sie waere die Abweichung nicht einzuordnen.

Aufruf:
    python3 broker/ibkr_abgleich.py
    python3 broker/ibkr_abgleich.py --json
"""

import argparse
import ast
import json
import os
import sys
from datetime import datetime

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _BROKER_DIR not in sys.path:
    sys.path.insert(0, _BROKER_DIR)

import ibkr_spiegel as spiegel        # noqa: E402


def kostenannahme_pct(bot: str) -> float:
    """Die Kostenannahme des Bots - GELESEN aus dessen forward_test.py, nicht
    hier noch einmal hingeschrieben (Methodik-Grundsatz 11). Dieselbe Technik
    wie in notifications/manual_close.py::kostensatz() und broker/abgleich.py."""
    pfad = os.path.join(spiegel.BASE_DIR, "strategies", bot, "forward_test.py")
    with open(pfad, encoding="utf-8") as datei:
        baum = ast.parse(datei.read(), filename=pfad)
    werte = {}
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if (isinstance(ziel, ast.Name)
                        and ziel.id in ("TRADING_FEE_PCT", "SLIPPAGE_PCT")):
                    try:
                        werte[ziel.id] = float(ast.literal_eval(knoten.value))
                    except (ValueError, TypeError, SyntaxError):
                        pass
    fehlend = {"TRADING_FEE_PCT", "SLIPPAGE_PCT"} - set(werte)
    if fehlend:
        raise spiegel.SpiegelFehler(
            f"In {pfad} fehlen {sorted(fehlend)} - ohne die Kostenannahme des "
            f"Bots ist kein Abgleich moeglich.")
    return 2 * (werte["TRADING_FEE_PCT"] + werte["SLIPPAGE_PCT"])


def _tage(von: str, bis: str):
    """Kalendertage zwischen zwei Zeitangaben - None, wenn eine fehlt oder
    unlesbar ist. Geraten wird nicht."""
    for form in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            a = datetime.strptime((von or "").strip()[:25], form)
            break
        except (ValueError, TypeError):
            a = None
    if a is None:
        return None
    for form in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            b = datetime.strptime((bis or "").strip()[:25], form)
            break
        except (ValueError, TypeError):
            b = None
    if b is None:
        return None
    if (a.tzinfo is None) != (b.tzinfo is None):
        a = a.replace(tzinfo=None)
        b = b.replace(tzinfo=None)
    return (b - a).days


def _effektiv(eintrag: dict, seite: str):
    """Der effektive Preis je Stueck: beim Kauf inklusive Provision, beim
    Verkauf abzueglich Provision. Beides in der Kontowaehrung, beides je Stueck -
    damit direkt mit dem pnl_pct des Bots vergleichbar."""
    if not eintrag:
        return None
    stueck = float(eintrag.get("stueck") or 0)
    gegenwert = float(eintrag.get("gegenwert") or 0)
    gebuehr = float(eintrag.get("gebuehr") or 0)
    if not stueck or not gegenwert:
        return None
    return ((gegenwert + gebuehr) if seite == "kauf"
            else (gegenwert - gebuehr)) / stueck


def zeile_auswerten(trade: dict, kauf: dict, verkauf: dict,
                     kostenannahme: float) -> dict:
    einstieg_abw = None
    if kauf and kauf.get("ausfuehrungspreis") and kauf.get("simulationspreis"):
        einstieg_abw = ((kauf["ausfuehrungspreis"] - kauf["simulationspreis"])
                        / kauf["simulationspreis"] * 100)
    ausstieg_abw = None
    if verkauf and verkauf.get("ausfuehrungspreis") and verkauf.get("simulationspreis"):
        ausstieg_abw = ((verkauf["ausfuehrungspreis"] - verkauf["simulationspreis"])
                        / verkauf["simulationspreis"] * 100)

    einstieg_effektiv = _effektiv(kauf, "kauf")
    ausstieg_effektiv = _effektiv(verkauf, "verkauf")
    pnl_echt = None
    if einstieg_effektiv and ausstieg_effektiv:
        pnl_echt = (ausstieg_effektiv - einstieg_effektiv) / einstieg_effektiv * 100
    pnl_sim = trade.get("pnl_pct")
    unterschied = (pnl_echt - pnl_sim) if (pnl_echt is not None
                                           and pnl_sim is not None) else None
    return {
        "trade_id": trade["id"], "symbol": trade["symbol"],
        "status": trade["status"], "grund": trade.get("result"),
        "einstieg_sim": kauf.get("simulationspreis") if kauf else trade.get("entry_price"),
        "einstieg_echt": kauf.get("ausfuehrungspreis") if kauf else None,
        "einstieg_abweichung_pct": einstieg_abw,
        "einstieg_verzug_tage": _tage(trade.get("entry_time"),
                                       kauf.get("zeitpunkt")) if kauf else None,
        "ausstieg_sim": (verkauf.get("simulationspreis") if verkauf
                          else trade.get("exit_price")),
        "ausstieg_echt": verkauf.get("ausfuehrungspreis") if verkauf else None,
        "ausstieg_abweichung_pct": ausstieg_abw,
        "ausstieg_verzug_tage": _tage(trade.get("exit_time"),
                                       verkauf.get("zeitpunkt")) if verkauf else None,
        "einstieg_effektiv": einstieg_effektiv,
        "ausstieg_effektiv": ausstieg_effektiv,
        "stueck": (kauf or {}).get("stueck"),
        "gebuehr_kauf": (kauf or {}).get("gebuehr"),
        "gebuehr_verkauf": (verkauf or {}).get("gebuehr"),
        "pnl_simulation_pct": pnl_sim,
        "pnl_ausfuehrung_pct": pnl_echt,
        "unterschied_pp": unterschied,
        "kostenannahme_pp": kostenannahme,
        "order_kauf": (kauf or {}).get("order_id"),
        "order_verkauf": (verkauf or {}).get("order_id"),
        "konto": (kauf or {}).get("konto") or (verkauf or {}).get("konto"),
        "vollstaendig": bool(kauf and verkauf),
    }


def bericht_daten(bot: str = None, conn=None) -> dict:
    bot = bot or spiegel.ERLAUBTE_BOTS[0]
    kostenannahme = kostenannahme_pct(bot)
    eigene = conn is None
    conn = conn or spiegel.oeffne_spiegel_db(bot)
    try:
        spiegelungen = {}
        for zeile in conn.execute("SELECT * FROM spiegelungen WHERE bot=?", (bot,)):
            eintrag = dict(zeile)
            spiegelungen.setdefault(eintrag["trade_id"], {})[eintrag["seite"]] = eintrag
        zeilen = []
        for trade in spiegel.lies_trades(bot):
            paar = spiegelungen.get(trade["id"])
            if not paar:
                continue
            zeilen.append(zeile_auswerten(
                trade, paar.get(spiegel.SEITE_EROEFFNUNG),
                paar.get(spiegel.SEITE_SCHLIESSUNG), kostenannahme))
        nicht_gespiegelt = [dict(z) for z in conn.execute(
            "SELECT trade_id, seite, symbol, grund, zeitpunkt FROM versuche "
            "WHERE bot=? AND ergebnis='uebersprungen' GROUP BY trade_id, seite",
            (bot,))]
        fehlversuche = [dict(z) for z in conn.execute(
            "SELECT trade_id, seite, symbol, modus, grund, zeitpunkt FROM versuche "
            "WHERE bot=? AND ergebnis='fehlgeschlagen' ORDER BY id DESC LIMIT 20",
            (bot,))]
    finally:
        if eigene:
            conn.close()

    vollstaendig = [z for z in zeilen if z["vollstaendig"]]

    def mittel(schluessel, menge):
        werte = [z[schluessel] for z in menge if z[schluessel] is not None]
        return round(sum(werte) / len(werte), 4) if werte else None

    return {
        "bot": bot,
        "kostenannahme_pp": kostenannahme,
        "zeilen": zeilen,
        "anzahl_gespiegelt": len(zeilen),
        "anzahl_vollstaendig": len(vollstaendig),
        "mittlere_einstiegsabweichung_pct": mittel("einstieg_abweichung_pct", zeilen),
        "mittlere_ausstiegsabweichung_pct": mittel("ausstieg_abweichung_pct", zeilen),
        "mittlerer_unterschied_pp": mittel("unterschied_pp", vollstaendig),
        "mittlerer_einstiegsverzug_tage": mittel("einstieg_verzug_tage", zeilen),
        "nicht_gespiegelt": nicht_gespiegelt,
        "fehlversuche": fehlversuche,
    }


def _z(wert, stellen=2, breite=10):
    return ("-" if wert is None else f"{wert:.{stellen}f}").rjust(breite)


def als_text(d: dict) -> str:
    linien = []
    linien.append("=" * 118)
    linien.append(f"ABGLEICH Simulation <-> IBKR PAPER - Bot {d['bot']}")
    linien.append("=" * 118)
    konten = {z["konto"] for z in d["zeilen"] if z["konto"]}
    linien.append(f"Konto: {', '.join(sorted(konten)) if konten else '-'}")
    linien.append(f"Gespiegelte Trades: {d['anzahl_gespiegelt']} "
                  f"(vollstaendig, also Kauf UND Verkauf: {d['anzahl_vollstaendig']})")
    linien.append(f"Kostenannahme der Simulation: {d['kostenannahme_pp']:.2f} "
                  f"Prozentpunkte je Trade (Gebuehr + Slippage, pauschal)")
    linien.append("")
    linien.append("Trade Symbol   Einstieg sim /  echt   Abw %  Verzug   "
                  "Ausstieg sim /  echt   Abw %    PnL sim  PnL echt   Diff pp")
    linien.append("-" * 118)
    for z in d["zeilen"]:
        linien.append(
            f"{z['trade_id']:>5} {z['symbol']:<8} "
            f"{_z(z['einstieg_sim'], 2, 11)} {_z(z['einstieg_echt'], 2, 11)} "
            f"{_z(z['einstieg_abweichung_pct'], 2, 7)} "
            f"{_z(z['einstieg_verzug_tage'], 0, 7)} "
            f"{_z(z['ausstieg_sim'], 2, 11)} {_z(z['ausstieg_echt'], 2, 11)} "
            f"{_z(z['ausstieg_abweichung_pct'], 2, 7)} "
            f"{_z(z['pnl_simulation_pct'], 2, 9)} {_z(z['pnl_ausfuehrung_pct'], 2, 9)} "
            f"{_z(z['unterschied_pp'], 2, 9)}")
    linien.append("-" * 118)
    linien.append(
        f"Mittelwerte: Einstiegsabweichung "
        f"{_z(d['mittlere_einstiegsabweichung_pct'], 3, 7)} %, Ausstiegsabweichung "
        f"{_z(d['mittlere_ausstiegsabweichung_pct'], 3, 7)} %, PnL-Unterschied "
        f"{_z(d['mittlerer_unterschied_pp'], 3, 7)} Prozentpunkte, Verzug "
        f"{_z(d['mittlerer_einstiegsverzug_tage'], 1, 5)} Tage")
    linien.append("")
    linien.append("Die Spalte VERZUG ist der Schluessel zur Abweichung: der Bot "
                  "rechnet mit dem")
    linien.append("Schlusskurs seines Signaltags, die Bruecke kauft in der "
                  "naechsten offenen Sitzung.")
    linien.append("Was als Abweichung dasteht, ist deshalb zu einem grossen Teil "
                  "die Uebernacht-Luecke")
    linien.append("und nicht die Ausfuehrungsqualitaet. Bei Verzug 0 Tagen ist sie "
                  "aussagekraeftig, bei")
    linien.append("mehreren Tagen misst sie vor allem Marktbewegung.")
    linien.append("")
    linien.append("PnL echt rechnet je Stueck mit den effektiven Preisen "
                  "(Gegenwert plus/minus Provision")
    linien.append("durch Stueckzahl). Eine zweite Rendite auf das eingesetzte "
                  "Kapital braucht es hier")
    linien.append("nicht: IBKR rechnet die Provision in USD ab, nicht in der "
                  "Aktie - es bleibt keine")
    linien.append("Restmenge liegen wie bei Krypto, gekaufte und verkaufte "
                  "Stueckzahl sind gleich.")
    linien.append("")
    linien.append("KEINEN Durchschnitt der PnL-Spalten als 'Rendite' lesen - das "
                  "waere wieder eine")
    linien.append("Summierung von Trade-Prozenten (Methodik-Grundsatz 2).")
    if d["nicht_gespiegelt"]:
        linien.append("")
        linien.append(f"NICHT gespiegelt ({len(d['nicht_gespiegelt'])}):")
        for n in d["nicht_gespiegelt"]:
            linien.append(f"  Trade {n['trade_id']:>5} {n['seite']:<12} "
                          f"{n['symbol']:<8} {n['grund']}")
    if d["fehlversuche"]:
        linien.append("")
        linien.append("Fehlversuche (neueste zuerst, hoechstens 20):")
        for f in d["fehlversuche"]:
            linien.append(f"  {f['zeitpunkt']} Trade {f['trade_id']} "
                          f"{f['seite']} ({f['modus']}): {f['grund']}")
    linien.append("")
    linien.append("Ein Paper-Konto bei IBKR simuliert die Ausfuehrung gegen die "
                  "ECHTEN Kurse und")
    linien.append("Orderbuecher - anders als das Binance-Testnet mit seinem "
                  "eigenen Orderbuch. Die hier")
    linien.append("gemessene Abweichung ist damit naeher an der Wirklichkeit, "
                  "bleibt aber eine Simulation:")
    linien.append("die eigene Order bewegt den Markt nicht, und genau das tut "
                  "eine echte Order.")
    return "\n".join(linien)


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Abgleich Simulation gegen IBKR-Paper-Ausfuehrung.")
    zerleger.add_argument("--bot", default=spiegel.ERLAUBTE_BOTS[0])
    zerleger.add_argument("--json", action="store_true",
                          help="Rohdaten statt Bericht")
    args = zerleger.parse_args(argv)
    try:
        daten = bericht_daten(args.bot)
    except spiegel.SpiegelFehler as fehler:
        print(f"FEHLER: {fehler}")
        return 1
    print(json.dumps(daten, indent=2, sort_keys=True, default=str)
          if args.json else als_text(daten))
    return 0


if __name__ == "__main__":
    sys.exit(main())
