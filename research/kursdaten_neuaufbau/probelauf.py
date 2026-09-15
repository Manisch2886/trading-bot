#!/usr/bin/env python3
"""
Der Neuaufbau gegen die ECHTEN Kursdateien des Repos (TB-34)
==============================================================================
Der Selbsttest `shared/test_kursdaten_neuaufbau.py` arbeitet mit
gleichmaessigen Kunstreihen: 1500 Kerzen, jeder Preis um eins hoeher als der
vorige. Das ist richtig so - eine vertauschte oder fehlende Zeile faellt
darin sofort auf.

Die echten Dateien sehen anders aus. `PEPEUSDT_1h.csv` fuehrt Kurse als
`1.97e-06` und Volumina als `46108639000543.0`, `BTCUSDT_1h.csv` hat 43.797
Zeilen, `UUSDT_1d.csv` 231. Ob der Lader **diese** Dateien liest, vergleicht
und byte-gleich zurueckschreiben wuerde, sagt der Selbsttest nicht.

Dieser Probelauf sagt es - **ohne Netz und ohne eine Datei im Repo
anzufassen**:

* Die Gegenstelle wird aus der **jeweiligen Datei selbst** gebaut: dieselben
  Kerzen, davor `--vorlauf` zusaetzliche (die Historie, die der Endpunkt
  haette), und an den **Raendern** abweichende Werte - genau die Lage, die
  der echte Lauf vorfinden wird, weil dort die Teilkerzen sitzen.
* Erwartet wird je Datei: **0** Abweichungen im Innern, **1** bzw. **2** an
  den Raendern, `alt + vorlauf` Zeilen, und **nicht geschrieben** (der
  Probelauf laeuft im Trockenlauf gegen das Repo).
* Die Schreibprobe laeuft nur auf einer **Kopie** in einem temporaeren
  Ordner: zweimal schreiben, byte-gleich, sichern, zurueckspielen.

    python3 research/kursdaten_neuaufbau/probelauf.py
    python3 research/kursdaten_neuaufbau/probelauf.py --symbole BTCUSDT,PEPEUSDT
    python3 research/kursdaten_neuaufbau/probelauf.py --json daten/probelauf.json

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1. Braucht `pandas`.
"""

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
_SHARED = os.path.join(_WURZEL, "shared")
for _pfad in (_SHARED, os.path.join(_WURZEL, "config")):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import binance_historie as bh                              # noqa: E402
import kursdaten_neuaufbau as kn                           # noqa: E402

sys.path.insert(0, os.path.join(_HIER))
_TESTHILFEN = os.path.join(_SHARED, "test_kursdaten_neuaufbau.py")

bestanden = 0
gescheitert = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{was}" + (f"   [{hinweis}]" if hinweis else ""))
    return bedingung


# ---------------------------------------------------------------------------
# Die Gegenstelle, aus der echten Datei gebaut
# ---------------------------------------------------------------------------
def _hilfen():
    """Die nachgebildete Gegenstelle aus dem Selbsttest mitbenutzen.

    Sie liegt dort, weil sie dort geprueft wird. Eine zweite Fassung hier
    waere eine zweite Wahrheit ueber die Feldform des Endpunkts.
    """
    import importlib.util                                  # noqa: PLC0415

    spez = importlib.util.spec_from_file_location("_tb34_testhilfen", _TESTHILFEN)
    modul = importlib.util.module_from_spec(spez)
    spez.loader.exec_module(modul)
    return modul


def kerzen_aus_datei(pfad, intervall):
    """Die Datei als Kerzenliste `(open_time_ms, o, h, l, c, v)`."""
    datei = bh.Kursdatei(pfad, intervall)
    kerzen = []
    for wert in datei.werte:
        ms = kn.als_ms(dt.datetime.strptime(wert["zeitpunkt"],
                                            bh.ZEITFORMAT[intervall]))
        kerzen.append((ms, wert["open"], wert["high"], wert["low"],
                       wert["close"], wert["volume"]))
    return datei, kerzen


def baue_gegenstelle_reihe(kerzen, intervall, vorlauf, raender):
    """Was der Endpunkt liefern wuerde: mehr Historie, korrigierte Raender.

    `raender`: welche Kerzen **des Altbestands** sich unterscheiden sollen -
    "erste" und/oder "letzte". Gezaehlt wird also in der Datei, nicht in der
    laengeren Endpunktreihe; sonst laege die Abweichung in der vorangestellten
    Historie, wo es nichts zu vergleichen gibt. Sie wird auf `high` gelegt,
    eine Spalte, die der Vergleich exakt prueft.
    """
    schritt = bh.INTERVALL_MS[intervall]
    beginn = kerzen[0][0]
    davor = []
    for i in range(vorlauf, 0, -1):
        basis = kerzen[0][1]
        davor.append((beginn - i * schritt, basis, basis * 1.01, basis * 0.99,
                      basis, 1.0 + i))
    reihe = davor + list(kerzen)
    stellen = {"erste": vorlauf, "letzte": len(reihe) - 1}
    for rand in raender:
        echt = stellen[rand]
        k = list(reihe[echt])
        k[2] = k[2] * 1.5 + 1.0                            # anderes Hoch
        reihe[echt] = tuple(k)
    return reihe


def probe_datei(hilfen, pfad, symbol, intervall, vorlauf):
    """Eine echte Datei durch den Lader schicken - Trockenlauf."""
    datei, kerzen = kerzen_aus_datei(pfad, intervall)
    # Die 1d-Dateien sind vorn UND hinten angeschnitten, 1h/4h nur hinten.
    raender = ["erste", "letzte"] if intervall == "1d" else ["letzte"]
    reihe = baue_gegenstelle_reihe(kerzen, intervall, vorlauf, raender)
    gegenstelle = hilfen.FalscheBinance({(symbol, intervall): reihe})

    drossel = bh.Drossel(mindestpause=0.0)
    abrufer = bh.Abrufer(drossel=drossel, oeffner=gegenstelle)
    stand_ms = reihe[-1][0] + bh.INTERVALL_MS[intervall]
    stand = dt.datetime(1970, 1, 1) + dt.timedelta(milliseconds=stand_ms)

    ergebnis = kn.baue_datei_neu(abrufer, pfad, symbol, intervall, stand,
                                 schreiben=False)
    return datei, ergebnis, len(raender)


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Faehrt den Neuaufbau gegen die echten Kursdateien des "
                    "Repos - im Trockenlauf, ohne Netz.")
    zerleger.add_argument("--ordner", default=os.path.join(_WURZEL, "data"))
    zerleger.add_argument("--symbole", default=None)
    zerleger.add_argument("--zeitrahmen", default="1h,4h,1d")
    zerleger.add_argument("--vorlauf", type=int, default=500,
                          help="wieviele Kerzen der Endpunkt zusaetzlich kennt")
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    try:
        import pandas                                      # noqa: F401,PLC0415
    except ImportError:
        print("pandas fehlt - dieser Probelauf braucht es (wie der Lader selbst).")
        return 1

    from symbols_config import SYMBOLS                     # noqa: PLC0415

    hilfen = _hilfen()
    symbole = ([s.strip() for s in argumente.symbole.split(",") if s.strip()]
               if argumente.symbole else list(SYMBOLS))
    zeitrahmen = [z.strip() for z in argumente.zeitrahmen.split(",") if z.strip()]

    print("=" * 78)
    print("PROBELAUF - der Neuaufbau gegen die echten Kursdateien")
    print("=" * 78)
    print(f"{len(symbole)} Symbol(e) x {len(zeitrahmen)} Zeitrahmen, "
          f"Vorlauf {argumente.vorlauf} Kerzen, Trockenlauf.\n")
    print(f"  {'Datei':<20} {'Zeilen alt':>10} {'neu':>8} "
          f"{'Rand':>5} {'innen':>6}  Urteil")
    print("  " + "-" * 72)

    zeilen = []
    for symbol in symbole:
        for intervall in zeitrahmen:
            pfad = os.path.join(argumente.ordner, f"{symbol}_{intervall}.csv")
            if not os.path.exists(pfad):
                continue
            datei, ergebnis, erwartete_raender = probe_datei(
                hilfen, pfad, symbol, intervall, argumente.vorlauf)
            name = f"{symbol}_{intervall}.csv"
            rand = len(ergebnis.get("rand_abweichungen", []))
            innen = ergebnis["abweichende_zeilen_innen"]

            gut = True
            gut &= pruefe(f"{name}: keine Abweichung im Innern", innen == 0,
                          f"{innen}")
            gut &= pruefe(f"{name}: genau {erwartete_raender} Randabweichung(en)",
                          rand == erwartete_raender, f"{rand}")
            gut &= pruefe(f"{name}: Zeilenzahl waechst um den Vorlauf",
                          ergebnis["neu_zeilen"]
                          == ergebnis["alt_zeilen"] + argumente.vorlauf,
                          f"{ergebnis['alt_zeilen']} -> {ergebnis['neu_zeilen']}")
            gut &= pruefe(f"{name}: im Trockenlauf wird nichts geschrieben",
                          not ergebnis["geschrieben"])
            print(f"  {name:<20} {ergebnis['alt_zeilen']:>10} "
                  f"{ergebnis['neu_zeilen']:>8} {rand:>5} {innen:>6}  "
                  f"{'OK' if gut else 'FEHLER'}")
            zeilen.append({"datei": name, "alt_zeilen": ergebnis["alt_zeilen"],
                           "neu_zeilen": ergebnis["neu_zeilen"],
                           "alt_von": ergebnis["alt_von"],
                           "alt_bis": ergebnis["alt_bis"],
                           "rand": rand, "innen": innen})

    # --- Gegenprobe: eine Abweichung MITTEN in einer echten Datei ---------
    print("\nGegenprobe - eine Abweichung mitten in einer echten Datei")
    beispiel = next((s for s in symbole
                     if os.path.exists(os.path.join(argumente.ordner,
                                                    f"{s}_1d.csv"))), None)
    if beispiel:
        pfad = os.path.join(argumente.ordner, f"{beispiel}_1d.csv")
        datei, kerzen = kerzen_aus_datei(pfad, "1d")
        reihe = baue_gegenstelle_reihe(kerzen, "1d", argumente.vorlauf,
                                       ["erste", "letzte"])
        mitte = len(reihe) // 2
        k = list(reihe[mitte])
        k[3] = k[3] * 0.5                                   # anderes Tief
        reihe[mitte] = tuple(k)
        gegenstelle = hilfen.FalscheBinance({(beispiel, "1d"): reihe})
        abrufer = bh.Abrufer(drossel=bh.Drossel(mindestpause=0.0),
                             oeffner=gegenstelle)
        stand_ms = reihe[-1][0] + bh.INTERVALL_MS["1d"]
        vorher = open(pfad, encoding="utf-8").read()
        ergebnis = kn.baue_datei_neu(
            abrufer, pfad, beispiel, "1d",
            dt.datetime(1970, 1, 1) + dt.timedelta(milliseconds=stand_ms),
            schreiben=True)
        pruefe("eine Abweichung im Innern verhindert das Schreiben",
               not ergebnis["geschrieben"] and ergebnis["abweichende_zeilen_innen"] >= 1)
        pruefe("die echte Repo-Datei bleibt dabei unveraendert",
               open(pfad, encoding="utf-8").read() == vorher)
        print(f"  {beispiel}_1d.csv: {ergebnis['abweichende_zeilen_innen']} "
              f"Zeile(n) innen, nicht geschrieben, Repo-Datei unveraendert.")

    # --- Schreibprobe auf einer Kopie -------------------------------------
    print("\nSchreibprobe - nur auf einer Kopie, nie im Repo")
    muster = next((s for s in symbole
                   if os.path.exists(os.path.join(argumente.ordner,
                                                  f"{s}_1d.csv"))), None)
    if muster:
        with tempfile.TemporaryDirectory() as arbeit:
            quelle = os.path.join(argumente.ordner, f"{muster}_1d.csv")
            ziel = os.path.join(arbeit, f"{muster}_1d.csv")
            shutil.copy2(quelle, ziel)
            vorher = open(ziel, encoding="utf-8").read()

            datei, kerzen = kerzen_aus_datei(ziel, "1d")
            reihe = baue_gegenstelle_reihe(kerzen, "1d", argumente.vorlauf,
                                           ["erste", "letzte"])
            stand_ms = reihe[-1][0] + bh.INTERVALL_MS["1d"]
            stand = dt.datetime(1970, 1, 1) + dt.timedelta(milliseconds=stand_ms)
            sicherungsordner = os.path.join(arbeit, "sicherung1")

            def einmal(ordner):
                # Je Lauf ein eigener Sicherungsordner - genau wie im
                # Werkzeug selbst, das ihn mit einem Zeitstempel benennt und
                # einen belegten Ordner ablehnt.
                gegenstelle = hilfen.FalscheBinance({(muster, "1d"): reihe})
                abrufer = bh.Abrufer(drossel=bh.Drossel(mindestpause=0.0),
                                     oeffner=gegenstelle)
                sicherung = kn.Sicherung(ordner, stand, arbeit)
                return kn.baue_datei_neu(abrufer, ziel, muster, "1d", stand,
                                         schreiben=True, sicherung=sicherung)

            erst = einmal(sicherungsordner)
            nach_erstem = open(ziel, encoding="utf-8").read()
            pruefe("der erste Lauf schreibt", erst["geschrieben"]
                   and nach_erstem != vorher)
            pruefe("die Sicherung haelt den alten Stand zeichengleich",
                   open(os.path.join(sicherungsordner, f"{muster}_1d.csv"),
                        encoding="utf-8").read() == vorher)

            zweit = einmal(os.path.join(arbeit, "sicherung2"))
            pruefe("der zweite Lauf laesst die Datei byte-identisch",
                   open(ziel, encoding="utf-8").read() == nach_erstem)
            pruefe("und findet dann keine Abweichung mehr",
                   zweit["abweichende_zeilen"] == 0,
                   f"{zweit['abweichende_zeilen']}")

            manifest, rueck = kn.zurueckspielen(sicherungsordner, arbeit)
            pruefe("--zurueckspielen stellt den alten Stand wieder her",
                   all(r["zurueckgespielt"] for r in rueck)
                   and open(ziel, encoding="utf-8").read() == vorher)
            print(f"  {muster}_1d.csv: geschrieben, wiederholt byte-gleich, "
                  f"gesichert und zurueckgespielt.")

    if argumente.json:
        pfad = (argumente.json if os.path.isabs(argumente.json)
                else os.path.join(_HIER, argumente.json))
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
        with open(pfad, "w", encoding="utf-8") as datei:
            json.dump({"vorlauf": argumente.vorlauf, "dateien": zeilen},
                      datei, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"\nJSON: {pfad}")

    print("\n" + "=" * 78)
    gesamt = bestanden + len(gescheitert)
    if gescheitert:
        print(f"{bestanden}/{gesamt} Pruefungen bestanden, "
              f"{len(gescheitert)} fehlgeschlagen:")
        for was in gescheitert[:20]:
            print(f"  - {was}")
        return 1
    print(f"{bestanden}/{gesamt} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
