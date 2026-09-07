"""
Die Tabelle: 2025er-P&L aller neun Bots bei fixer 1000-USD-Position
====================================================================
Liest die Einzelergebnisse von extract.py und stellt sie zusammen.
Reine Informationsauswertung - kein Vergleich, keine Bewertung, keine
Empfehlung. Die Reihenfolge der Zeilen ist in konfiguration.py
festgelegt und folgt nicht dem Ergebnis.

Nutzung:  python3 summary.py
"""

import json
import os

import konfiguration as cfg

DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(DIR, "results")


def laden(schluessel):
    pfad = os.path.join(RESULTS_DIR, f"{schluessel}_pnl.json")
    if not os.path.exists(pfad):
        raise SystemExit(f"{pfad} fehlt - erst extract.py {schluessel} laufen lassen.")
    with open(pfad) as fh:
        return json.load(fh)


def usd(wert):
    return "-" if wert is None else f"{wert:+,.2f}".replace(",", " ")


def main():
    zeilen = [laden(k) for k in cfg.REIHENFOLGE]

    print("=" * 108)
    print(f"P&L 01.01.{cfg.JAHR} - 31.12.{cfg.JAHR} bei fixer Positionsgroesse von "
          f"{cfg.POSITIONSGROESSE_USD:,.0f} USD je Trade".replace(",", " "))
    print("=" * 108)
    kopf = (f"{'Bot / Stand':<30}{'Trades':>8}{'Symb':>6}{'Gewinnrate':>12}"
            f"{'P&L brutto USD':>17}{'P&L netto USD':>16}{'Reihenfolge':>14}")
    print(kopf)
    print("-" * 108)
    for z in zeilen:
        g = z.get("gleichzeitigkeit") or {}
        reihenfolge = "-"
        if g.get("limit") is None:
            reihenfolge = "kein Limit"
        elif g.get("relevant_2025"):
            reihenfolge = f"ja ({g['geblockte_trades_2025']})"
        else:
            reihenfolge = "nein"
        quote = "-" if z["gewinnrate_pct"] is None else f"{z['gewinnrate_pct']} %"
        print(f"{z['schluessel']:<30}{z['trades_2025']:>8}{z.get('symbole_2025', 0):>6}"
              f"{quote:>12}{usd(z['pnl_usd']):>17}"
              f"{usd(z.get('pnl_usd_netto_laut_bot')):>16}{reihenfolge:>14}")

    alt = next(z for z in zeilen if z["schluessel"] == "elliott_wave_alt")
    neu = next(z for z in zeilen if z["schluessel"] == "elliott_wave_neu")
    print("-" * 108)
    print(f"{'elliott_wave: neu minus alt':<30}"
          f"{neu['trades_2025'] - alt['trades_2025']:>8}{'':>6}{'':>12}"
          f"{usd(neu['pnl_usd'] - alt['pnl_usd']):>17}"
          f"{usd((neu.get('pnl_usd_netto_laut_bot') or 0) - (alt.get('pnl_usd_netto_laut_bot') or 0)):>16}")
    print("=" * 108)

    print("\nVerwendete Konfiguration je Zeile:")
    for z in zeilen:
        print(f"\n  {z['schluessel']}  ({z['bot']})")
        print(f"    {z['beschreibung']}")
        print(f"    Parameterquelle : {z['parameterquelle']}"
              + (f", live_params zuletzt geaendert {z['live_params_stand']}"
                 if z.get("live_params_stand") else ""))
        print(f"    Parameter       : {z['verwendete_parameter']}")
        print(f"    Positionslimit  : {z['positionslimit_live']}")
        abw = [k for k in z["konstanten_angeglichen"] if k["abweichung"]]
        if z["konstanten_angeglichen"]:
            print(f"    Sync-Abgleich   : {len(z['konstanten_angeglichen'])} Konstante(n) geprueft, "
                  f"{len(abw)} abweichend"
                  + ("" if not abw else ": " + ", ".join(
                      f"{k['modul']}.{k['konstante']} {k['wert_im_modul']}->{k['wert_live']}" for k in abw)))
        if z.get("regimefilter"):
            r = z["regimefilter"]
            print(f"    BTC-Regimefilter: live {'aktiv' if r['live_aktiv'] else 'inaktiv'}, "
                  f"nachgezogen - {r['geblockt']} von {r['trades_vorher']} Trades geblockt")
        if z.get("gestrichen_wegen_kursluecke"):
            print(f"    Kursluecken     : {z['gestrichen_wegen_kursluecke']} Trade(s) gestrichen "
                  f"({', '.join(z.get('kursluecke_symbole', []))})")

    print("\nReihenfolge-Empfindlichkeit 2025 (PR #23):")
    for z in zeilen:
        g = z.get("gleichzeitigkeit") or {}
        if g.get("limit") is None:
            print(f"  {z['schluessel']:<30} kein Positionslimit - Reihenfolge ohne Einfluss")
        elif g.get("relevant_2025"):
            print(f"  {z['schluessel']:<30} Limit {g['limit']} war bindend: "
                  f"{g['geblockte_trades_2025']} Trades ohne Platz an "
                  f"{g['zeitpunkte_am_limit_2025']} Zeitpunkten, davon "
                  f"{g['davon_mit_mehreren_signalen_gleichzeitig']} mit mehreren Signalen "
                  f"zur selben Zeit")
        else:
            print(f"  {z['schluessel']:<30} Limit {g.get('limit')} war 2025 nie ausgeschoepft")

    zusammenfassung = {"jahr": cfg.JAHR, "positionsgroesse_usd": cfg.POSITIONSGROESSE_USD,
                        "zeilen": zeilen,
                        "elliott_wave_differenz_usd": round(neu["pnl_usd"] - alt["pnl_usd"], 2)}
    pfad = os.path.join(RESULTS_DIR, "zusammenfassung.json")
    with open(pfad, "w") as fh:
        json.dump(zusammenfassung, fh, indent=2, default=str, ensure_ascii=False)
    print(f"\nGespeichert: {pfad}")


if __name__ == "__main__":
    main()
