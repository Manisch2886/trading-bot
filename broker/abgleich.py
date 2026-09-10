"""
Abgleich: was die Simulation annimmt gegen das, was die Boerse tatsaechlich tat
==============================================================================
Der eigentliche Erkenntnisgewinn dieser Anbindung. Die Paper-Trading-Simulation
rechnet mit

  * dem SCHLUSSKURS der Signalkerze als Einstieg bzw. Ausstieg (oder dem
    Stop-Preis, wenn der Stop getroffen wurde) - also mit einem Kurs, zu dem
    niemand gehandelt hat,
  * pauschal 2 * (TRADING_FEE_PCT + SLIPPAGE_PCT) = 0,30 Prozentpunkten
    Kosten fuer Gebuehren und Slippage zusammen.

Tatsaechlich ausgefuehrt wird zu einem mengengewichteten Mischkurs aus einer
oder mehreren Teilausfuehrungen, und die Gebuehr steht danach in der Antwort
der Boerse. Dieser Bericht stellt beides nebeneinander:

    Abweichung je Seite   (Ausfuehrungspreis gegen Simulationspreis, in %)
    PnL der Simulation    (pnl_pct aus der Bot-Datenbank)
    PnL der Ausfuehrung   (aus den echten Quote-Betraegen und Gebuehren)
    Unterschied           (in Prozentpunkten)

WAS DER BERICHT NICHT KANN, und das gehoert dazugesagt: das SPOT-Testnet hat
ein eigenes, kuenstliches Orderbuch. Eine dort gemessene Slippage sagt etwas
ueber die API und die eigene Rechnung - nicht darueber, wie viel Slippage an
der echten Boerse entsteht. Wer das wissen will, braucht realistische
Orderbuecher (siehe broker/README.md, Abschnitt zum Demo Mode).

Aufruf:
    python3 broker/abgleich.py
    python3 broker/abgleich.py --json
"""

import argparse
import json
import os
import sqlite3
import sys

_BROKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _BROKER_DIR not in sys.path:
    sys.path.insert(0, _BROKER_DIR)

import spiegel            # noqa: E402

# Die Kostenannahme des Bots. NICHT hier hartkodiert, sondern aus dessen
# forward_test.py gelesen - dieselbe Begruendung wie bei
# notifications/manual_close.py::kostensatz(): eine zweite Kopie der Zahl
# laeuft irgendwann auseinander, und dann vergleicht dieser Bericht gegen etwas,
# womit der Bot nie gerechnet hat.
def kostenannahme_pct(bot: str) -> float:
    import ast
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


def _gebuehr_in(gebuehren: dict, waehrung: str) -> float:
    return float((gebuehren or {}).get(waehrung) or 0.0)


def _quote_waehrung(symbol: str) -> str:
    """Die Bots handeln ausschliesslich ...USDT-Paare (symbols_config.py)."""
    return "USDT" if symbol.endswith("USDT") else symbol[-4:]


def zeile_auswerten(trade: dict, kauf: dict, verkauf: dict,
                     kostenannahme: float) -> dict:
    """Eine Zeile des Berichts. `verkauf` darf None sein - dann laeuft die
    Spiegelung noch."""
    quote = _quote_waehrung(trade["symbol"])
    einstieg_abw = None
    if kauf and kauf.get("ausfuehrungspreis") and kauf.get("simulationspreis"):
        einstieg_abw = ((kauf["ausfuehrungspreis"] - kauf["simulationspreis"])
                        / kauf["simulationspreis"] * 100)
    ausstieg_abw = None
    if verkauf and verkauf.get("ausfuehrungspreis") and verkauf.get("simulationspreis"):
        ausstieg_abw = ((verkauf["ausfuehrungspreis"] - verkauf["simulationspreis"])
                        / verkauf["simulationspreis"] * 100)

    # ZWEI Renditen, und der Unterschied zwischen ihnen ist kein Detail.
    #
    # Die Simulation rechnet JE EINHEIT: (Ausstieg - Einstieg) / Einstieg, minus
    # der pauschalen Kostenannahme. Vergleichbar ist damit nur eine Rendite, die
    # ebenfalls je Einheit rechnet - also mit den EFFEKTIVEN Preisen:
    #
    #   Einstieg effektiv = bezahlter Betrag / tatsaechlich erhaltene Menge
    #   Ausstieg effektiv = erhaltener Betrag / tatsaechlich verkaufte Menge
    #
    # Beides enthaelt damit die echten Gebuehren, egal in welcher Waehrung sie
    # abgerechnet wurden - einmal im Zaehler, einmal im Nenner, nie doppelt.
    #
    # Die zweite Zahl (`pnl_kapital_pct`) rechnet auf das EINGESETZTE KAPITAL:
    # Erloes gegen Kosten. Sie fuehrt einen Effekt mit, den die erste bewusst
    # heraushaelt - die RESTMENGE. Verkauft werden darf nur ein ganzes Vielfaches
    # der Schrittweite, und nach Abzug der Gebuehr in der Basiswaehrung bleibt
    # praktisch immer ein Rest liegen. Bei kleinen Positionen ist dieser Rest
    # groesser als die gesamte Slippage: aus 0,002 BTC werden nach 0,1 % Gebuehr
    # 0,001998, und verkaufbar sind davon nur 0,00199 - 0,4 % der Position
    # bleiben liegen. Wer beide Zahlen nicht trennt, haelt diesen Rundungsrest
    # fuer Slippage. (Genau das ist beim Bauen dieses Berichts zuerst passiert
    # und erst im Test aufgefallen.)
    pnl_echt = pnl_kapital = restmenge = None
    einstieg_effektiv = ausstieg_effektiv = None
    if kauf and kauf.get("quote_menge") and kauf.get("menge_netto"):
        kauf_gebuehren = json.loads(kauf.get("gebuehren") or "{}")
        kosten = float(kauf["quote_menge"]) + _gebuehr_in(kauf_gebuehren, quote)
        einstieg_effektiv = kosten / float(kauf["menge_netto"])
    if verkauf and verkauf.get("quote_menge") and verkauf.get("menge_brutto"):
        verkauf_gebuehren = json.loads(verkauf.get("gebuehren") or "{}")
        erloes = (float(verkauf["quote_menge"])
                  - _gebuehr_in(verkauf_gebuehren, quote))
        ausstieg_effektiv = erloes / float(verkauf["menge_brutto"])
    if einstieg_effektiv and ausstieg_effektiv:
        pnl_echt = (ausstieg_effektiv - einstieg_effektiv) / einstieg_effektiv * 100
        kosten = float(kauf["quote_menge"]) + _gebuehr_in(
            json.loads(kauf.get("gebuehren") or "{}"), quote)
        erloes = (float(verkauf["quote_menge"]) - _gebuehr_in(
            json.loads(verkauf.get("gebuehren") or "{}"), quote))
        pnl_kapital = (erloes - kosten) / kosten * 100
        restmenge = max(0.0, float(kauf["menge_netto"])
                        - float(verkauf["menge_brutto"]))

    pnl_sim = trade.get("pnl_pct")
    unterschied = (pnl_echt - pnl_sim) if (pnl_echt is not None
                                           and pnl_sim is not None) else None
    return {
        "trade_id": trade["id"], "symbol": trade["symbol"],
        "status": trade["status"], "grund": trade.get("result"),
        "einstieg_sim": kauf.get("simulationspreis") if kauf else trade.get("entry_price"),
        "einstieg_echt": kauf.get("ausfuehrungspreis") if kauf else None,
        "einstieg_abweichung_pct": einstieg_abw,
        "ausstieg_sim": (verkauf.get("simulationspreis") if verkauf
                          else trade.get("exit_price")),
        "ausstieg_echt": verkauf.get("ausfuehrungspreis") if verkauf else None,
        "ausstieg_abweichung_pct": ausstieg_abw,
        "einstieg_effektiv": einstieg_effektiv,
        "ausstieg_effektiv": ausstieg_effektiv,
        "pnl_simulation_pct": pnl_sim,
        "pnl_ausfuehrung_pct": pnl_echt,
        "pnl_kapital_pct": pnl_kapital,
        "restmenge": restmenge,
        "unterschied_pp": unterschied,
        "kostenannahme_pp": kostenannahme,
        "order_kauf": kauf.get("order_id") if kauf else None,
        "order_verkauf": verkauf.get("order_id") if verkauf else None,
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
        "mittlerer_kapitalunterschied_pp": (
            round(sum(z["pnl_kapital_pct"] - z["pnl_simulation_pct"]
                      for z in vollstaendig
                      if z["pnl_kapital_pct"] is not None
                      and z["pnl_simulation_pct"] is not None)
                  / len([z for z in vollstaendig
                         if z["pnl_kapital_pct"] is not None
                         and z["pnl_simulation_pct"] is not None]), 4)
            if [z for z in vollstaendig if z["pnl_kapital_pct"] is not None
                and z["pnl_simulation_pct"] is not None] else None),
        "nicht_gespiegelt": nicht_gespiegelt,
        "fehlversuche": fehlversuche,
    }


def _z(wert, stellen=2, breite=10):
    return ("-" if wert is None else f"{wert:.{stellen}f}").rjust(breite)


def als_text(d: dict) -> str:
    linien = []
    linien.append("=" * 100)
    linien.append(f"ABGLEICH Simulation <-> Binance SPOT-TESTNET - Bot {d['bot']}")
    linien.append("=" * 100)
    linien.append(f"Gespiegelte Trades: {d['anzahl_gespiegelt']} "
                  f"(vollstaendig, also Kauf UND Verkauf: {d['anzahl_vollstaendig']})")
    linien.append(f"Kostenannahme der Simulation: {d['kostenannahme_pp']:.2f} "
                  f"Prozentpunkte je Trade (Gebuehr + Slippage, pauschal)")
    linien.append("")
    linien.append("Trade Symbol      Einstieg sim /  echt   Abw %   "
                  "Ausstieg sim /  echt   Abw %    PnL sim  PnL echt   Diff pp "
                  "  PnL Kap.   Restmenge")
    linien.append("-" * 122)
    for z in d["zeilen"]:
        linien.append(
            f"{z['trade_id']:>5} {z['symbol']:<10} "
            f"{_z(z['einstieg_sim'], 4, 12)} {_z(z['einstieg_echt'], 4, 12)} "
            f"{_z(z['einstieg_abweichung_pct'], 3, 7)} "
            f"{_z(z['ausstieg_sim'], 4, 12)} {_z(z['ausstieg_echt'], 4, 12)} "
            f"{_z(z['ausstieg_abweichung_pct'], 3, 7)} "
            f"{_z(z['pnl_simulation_pct'], 2, 9)} {_z(z['pnl_ausfuehrung_pct'], 2, 9)} "
            f"{_z(z['unterschied_pp'], 2, 9)} {_z(z['pnl_kapital_pct'], 2, 9)} "
            f"{_z(z['restmenge'], 8, 11)}")
    linien.append("-" * 122)
    linien.append(
        f"Mittlere Abweichung: Einstieg "
        f"{_z(d['mittlere_einstiegsabweichung_pct'], 3, 7)} %, Ausstieg "
        f"{_z(d['mittlere_ausstiegsabweichung_pct'], 3, 7)} %; mittlerer "
        f"PnL-Unterschied {_z(d['mittlerer_unterschied_pp'], 3, 7)} Prozentpunkte "
        f"(je Einheit), {_z(d['mittlerer_kapitalunterschied_pp'], 3, 7)} "
        f"Prozentpunkte auf das eingesetzte Kapital")
    linien.append("")
    linien.append("PnL echt rechnet JE EINHEIT mit den effektiven Preisen "
                  "(bezahlter Betrag durch")
    linien.append("erhaltene Menge) - nur das ist mit der Simulation "
                  "vergleichbar. PnL Kap. rechnet auf")
    linien.append("das eingesetzte Kapital und enthaelt deshalb auch die "
                  "Restmenge, die nach Gebuehr und")
    linien.append("Schrittweite nicht verkaufbar war. Bei kleinen Positionen ist "
                  "dieser Rest groesser als")
    linien.append("die gesamte Slippage - beide Zahlen nicht zu trennen hiesse, "
                  "Rundung fuer Slippage zu")
    linien.append("halten.")
    linien.append("")
    linien.append("KEIN Durchschnitt ueber die PnL-Spalten als 'Rendite' lesen: das "
                  "waere wieder eine")
    linien.append("Summierung von Trade-Prozenten (Methodik-Grundsatz 2). Die Spalte "
                  "Diff pp ist der")
    linien.append("Punkt dieses Berichts - sie zeigt je Trade, wie weit die "
                  "Kostenannahme von der")
    linien.append("Wirklichkeit abweicht.")
    if d["nicht_gespiegelt"]:
        linien.append("")
        linien.append(f"NICHT gespiegelt ({len(d['nicht_gespiegelt'])}):")
        for n in d["nicht_gespiegelt"]:
            linien.append(f"  Trade {n['trade_id']:>5} {n['seite']:<12} "
                          f"{n['symbol']:<10} {n['grund']}")
    if d["fehlversuche"]:
        linien.append("")
        linien.append(f"Fehlversuche (neueste zuerst, hoechstens 20):")
        for f in d["fehlversuche"]:
            linien.append(f"  {f['zeitpunkt']} Trade {f['trade_id']} "
                          f"{f['seite']} ({f['modus']}): {f['grund']}")
    linien.append("")
    linien.append("Das Testnet hat ein eigenes, kuenstliches Orderbuch. Die hier "
                  "gemessene Slippage")
    linien.append("prueft die Anbindung und die eigene Rechnung - sie ist KEINE "
                  "Aussage ueber die")
    linien.append("Slippage an der echten Boerse.")
    linien.append("")
    linien.append("Und die Abweichungsspalten enthalten ZWEI Dinge: die "
                  "Ausfuehrungsabweichung und den")
    linien.append("ZEITVERSATZ zwischen Bot-Lauf und Bruecken-Lauf. Die Bruecke "
                  "kauft zum JETZIGEN Kurs,")
    linien.append("die Simulation rechnet mit dem Schlusskurs der Signalkerze. "
                  "Laeuft die Bruecke direkt")
    linien.append("nach dem Bot, ist der Versatz klein; laeuft sie Stunden "
                  "spaeter, misst die Spalte")
    linien.append("vor allem Marktbewegung. Eine grosse Einstiegsabweichung bei "
                  "nur einem Trade ist")
    linien.append("deshalb meist ein Hinweis auf den Zeitpunkt des Laufs, nicht "
                  "auf die Boerse.")
    return "\n".join(linien)


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(description=__doc__.splitlines()[1])
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
