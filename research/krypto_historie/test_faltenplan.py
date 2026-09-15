#!/usr/bin/env python3
"""
Selbsttest des Faltenplan-Werkzeugs (TB-31)
==============================================================================
`research/krypto_historie/faltenplan.py` rechnet die Regel aus Abschnitt 5.3
der Vorregistrierung nach. Aus seiner Zahl folgt, ob die Krypto-Haelfte der
Neuselektion ueberhaupt stattfinden kann - eine falsche Zahl waere hier
teurer als ein Absturz, weil sie plausibel aussieht.

Die tragende Zusicherung ist Teil A: **dasselbe Werkzeug reproduziert den
von Hand geschriebenen Aktien-Faltenplan aus dem Register.** Der steht dort
seit TB-30a fest (2019 bis 2025 Selektion, 2026 Bestaetigung) und ist nicht
aus diesem Code entstanden. Trifft die Rechnung ihn, rechnet sie die Regel
nach; trifft sie ihn nicht, ist die Krypto-Zahl daneben, egal wie plausibel
sie wirkt. Der Plan wird dabei **aus der Registerdatei gelesen**, nicht hier
abgeschrieben - aendert der Betreiber ihn, wird dieser Test rot.

Dazu die Raender, an denen so eine Regel erfahrungsgemaess kippt: der
Stichtag auf den Tag genau, der 29. Februar, der Go-Live-Schnitt und die
Frage, ob die letzte Falte wirklich nie selektiert wird.

ZU DEN MUTATIONSPROBEN
------------------------------------------------------------------------------
Zweistufig, wie in diesem Projekt ueblich: jede Probe belegt erst, dass sie
**ohne** Mutation das Richtige sieht, dann, dass sie **mit** Mutation das
Verfaelschte sieht. Und jede greift **eine** Wache an, damit keine zweite
das Fehlen der ersten verdeckt:

* Teil F verfaelscht die Vorlaufzeit (`minus_jahre`). Faellt sie aus, beginnt
  der Faltenplan zu frueh - und niemand sonst merkt es, denn die Zahl der
  Falten sieht dann sogar **besser** aus.
* Teil G verfaelscht den point-in-time-Filter (`symbole_in_falte`). Faellt
  er aus, sind ploetzlich alle 24 Symbole in jeder Falte - genau die
  Gluettung, die der Auftrag ausdruecklich verbietet. Die Zahl der Falten
  bleibt dabei unveraendert richtig; ohne eine eigene Probe fiele es nicht
  auf.

    python3 research/krypto_historie/test_faltenplan.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import datetime as dt
import json
import os
import re
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import faltenplan as fp                                    # noqa: E402

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")

bestanden = 0
gescheitert = []


def pruefe(was, bedingung, hinweis=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"  OK    {was}")
    else:
        gescheitert.append(was)
        print(f"  FEHLT {was}" + (f"   [{hinweis}]" if hinweis else ""))


def aktienplan_aus_register():
    """Liest die Aktien-Zeilen der Faltenplan-Tabelle aus dem Register.

    Absichtlich aus der Datei und nicht hier abgeschrieben: eine hier
    eingetippte Kopie bliebe gruen, auch wenn der Betreiber den Plan
    aenderte - und dann rechnete dieses Werkzeug still gegen ein Register,
    das es nicht mehr gibt.
    """
    plaene = {}
    with open(REGISTER, "r", encoding="utf-8") as datei:
        for zeile in datei:
            if "| aktien |" not in zeile:
                continue
            spalten = [s.strip() for s in zeile.strip().strip("|").split("|")]
            if len(spalten) < 7:
                continue
            bot = spalten[0].strip("`")
            jahre = re.findall(r"\b(20\d\d)\b", spalten[5])
            bestaetigung = re.findall(r"\b(20\d\d)\b", spalten[6])
            if jahre and bestaetigung:
                plaene[bot] = ([int(j) for j in jahre], int(bestaetigung[0]))
    return plaene


def schreibe_daten(ordner, beginn_je_symbol, zeitrahmen="1d"):
    """Kursdateien mit genau einer Datenzeile - mehr braucht die Regel nicht,
    sie liest nur den ersten Zeitstempel."""
    for symbol, tag in beginn_je_symbol.items():
        with open(os.path.join(ordner, f"{symbol}_{zeitrahmen}.csv"), "w",
                  encoding="utf-8") as datei:
            datei.write("open_time,open,high,low,close,volume\n")
            datei.write(f"{tag},1.0,1.0,1.0,1.0,1.0\n")


# ---------------------------------------------------------------------------
def teil_a():
    print("\nA. Die Regel reproduziert den Aktien-Faltenplan des Registers")

    aus_register = aktienplan_aus_register()
    pruefe("die Faltenplan-Tabelle des Registers ist lesbar",
           len(aus_register) == 4, f"{sorted(aus_register)}")
    if not aus_register:
        return

    erwartete_jahre, erwartete_bestaetigung = list(aus_register.values())[0]
    pruefe("alle vier Aktien-Bots haben denselben Plan",
           all(v == (erwartete_jahre, erwartete_bestaetigung)
               for v in aus_register.values()))

    # Aktien-Kursdaten reichen bis 1962 zurueck - hier genuegt ein Symbol,
    # das frueh genug beginnt, damit die Untergrenze 2019 bindet.
    beginn = {"AAA": dt.date(1962, 1, 2)}
    erstes = fp.erste_faltenjahr(beginn)
    pruefe(f"erste Falte ist {erwartete_jahre[0]}, nicht frueher",
           erstes == erwartete_jahre[0], f"{erstes}")
    pruefe("die Untergrenze 2019 bindet hier, nicht die Vorlaufzeit",
           erstes == fp.FRUEHESTE_FALTE)

    bloecke = fp.falten(erstes, 1)
    gerechnete_jahre = [b["jahre"][0] for b in bloecke[:-1]]
    pruefe("die Selektionsfalten stimmen mit dem Register ueberein",
           gerechnete_jahre == erwartete_jahre,
           f"{gerechnete_jahre} statt {erwartete_jahre}")
    pruefe("die Bestaetigungsperiode stimmt mit dem Register ueberein",
           bloecke[-1]["jahre"] == [erwartete_bestaetigung],
           f"{bloecke[-1]['jahre']}")
    pruefe("sie endet am Go-Live-Schnitt, nicht am Jahresende",
           bloecke[-1]["bis_ausschliesslich"] == fp.GO_LIVE)


def teil_b():
    print("\nB. Der Stichtag der Vorlaufzeit - auf den Tag genau")

    pruefe("genau vier Jahre vor Faltenbeginn reichen",
           fp.erste_faltenjahr({"A": dt.date(2018, 1, 1)}) == 2022)
    pruefe("einen Tag spaeter reicht es nicht mehr",
           fp.erste_faltenjahr({"A": dt.date(2018, 1, 2)}) == 2023)
    pruefe("ein Tag frueher aendert nichts",
           fp.erste_faltenjahr({"A": dt.date(2017, 12, 31)}) == 2022)
    pruefe("BTC-Listing irgendwann im zweiten Halbjahr 2017 ergibt IMMER 2022",
           {fp.erste_faltenjahr({"A": dt.date(2017, m, 17)}) for m in range(7, 13)} == {2022},
           "die Aussage haengt doch am genauen Tag")
    pruefe("der 29.02. faellt nicht auf die Nase",
           fp.minus_jahre(dt.date(2024, 2, 29), 1) == dt.date(2023, 2, 28))
    pruefe("das Mindesttraining ist einstellbar und wirkt",
           fp.erste_faltenjahr({"A": dt.date(2021, 9, 1)}, mindesttraining=2) == 2024
           and fp.erste_faltenjahr({"A": dt.date(2021, 9, 1)}, mindesttraining=4) == 2026)


def teil_c():
    print("\nC. Faltenlaenge, Go-Live-Schnitt und die letzte Falte")

    einjahr = fp.falten(2022, 1)
    pruefe("Einjahres-Falten ab 2022 ergeben fuenf Bloecke bis zum Schnitt",
           [b["jahre"] for b in einjahr]
           == [[2022], [2023], [2024], [2025], [2026]], f"{[b['jahre'] for b in einjahr]}")
    pruefe("kein Block beginnt nach dem Go-Live-Schnitt",
           all(b["von"] < fp.GO_LIVE for b in einjahr))
    pruefe("kein Block reicht ueber den Go-Live-Schnitt hinaus",
           all(b["bis_ausschliesslich"] <= fp.GO_LIVE for b in einjahr))

    zweijahr = fp.falten(2022, 2)
    pruefe("Zweijahres-Falten ab 2022 ergeben drei Bloecke",
           [b["jahre"] for b in zweijahr] == [[2022, 2023], [2024, 2025], [2026]],
           f"{[b['jahre'] for b in zweijahr]}")
    pruefe("dieselbe Historie ergibt bei zwei Jahren Faltenlaenge halb so "
           "viele Selektionsfalten",
           len(einjahr) - 1 == 4 and len(zweijahr) - 1 == 2)

    pruefe("ohne erstes Faltenjahr gibt es keinen Plan statt eines leeren",
           fp.falten(None, 1) == [])


def teil_d():
    print("\nD. Point-in-time: wer kommt in welcher Falte vor?")

    beginn = {
        "FRUEH":  dt.date(2017, 8, 17),
        "MITTE":  dt.date(2018, 6, 11),
        "SPAET":  dt.date(2023, 5, 3),
    }
    pruefe("2022 ist nur das frueh gelistete Paar dabei",
           fp.symbole_in_falte(beginn, dt.date(2022, 1, 1)) == ["FRUEH"])
    pruefe("2023 kommt das 2018 gelistete dazu",
           fp.symbole_in_falte(beginn, dt.date(2023, 1, 1)) == ["FRUEH", "MITTE"])
    pruefe("das 2023 gelistete ist bis zum Go-Live-Schnitt in KEINER Falte",
           all("SPAET" not in fp.symbole_in_falte(beginn, dt.date(j, 1, 1))
               for j in range(2019, 2027)),
           "ein spaet gelistetes Paar rutscht in eine Selektionsfalte")


def teil_e():
    print("\nE. Der ganze Plan, aus echten Dateien gelesen")

    with tempfile.TemporaryDirectory() as ordner:
        schreibe_daten(ordner, {"AUSDT": "2017-08-17", "BUSDT": "2018-06-11",
                                "CUSDT": "2025-01-19"})
        plan = fp.plan_fuer_bot("rsi2_crypto", ordner,
                                ["AUSDT", "BUSDT", "CUSDT", "FEHLTUSDT"])
        pruefe("vier Selektionsfalten", plan["anzahl_selektionsfalten"] == 4,
               f"{plan['anzahl_selektionsfalten']}")
        pruefe("die Bestaetigungsperiode ist 2026",
               plan["bestaetigungsperiode"]["jahre"] == [2026])
        pruefe("ein Symbol ohne Datei wird gemeldet statt still weggelassen",
               plan["ohne_datei"] == ["FEHLTUSDT"])
        pruefe("die erste Selektionsfalte hat genau ein Symbol",
               plan["selektionsfalten"][0]["symbole"] == ["AUSDT"])
        pruefe("die letzte Selektionsfalte hat zwei",
               plan["selektionsfalten"][-1]["symbole"] == ["AUSDT", "BUSDT"])
        pruefe("das 2025 gelistete Paar taucht nirgends auf",
               all("CUSDT" not in b["symbole"] for b in plan["selektionsfalten"]))

    with tempfile.TemporaryDirectory() as ordner:
        schreibe_daten(ordner, {"AUSDT": "2021-09-01"})
        plan = fp.plan_fuer_bot("rsi2_crypto", ordner, ["AUSDT"])
        pruefe("der heutige Datenbeginn ergibt NULL Selektionsfalten",
               plan["anzahl_selektionsfalten"] == 0,
               f"{plan['anzahl_selektionsfalten']}")
        pruefe("und trotzdem eine Bestaetigungsperiode - sie ist die letzte Falte",
               plan["bestaetigungsperiode"] is not None)

    # Die Messung aus binance_historie.py --messen ist derselbe Weg
    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, "messung.json")
        with open(pfad, "w", encoding="utf-8") as datei:
            json.dump({"messung": {"AUSDT": {"1d": {"beginn_tag": "2017-08-17"}}}}, datei)
        plan = fp.plan_fuer_bot("rsi2_crypto", ordner, ["AUSDT"], messung=pfad)
        pruefe("ein Messbericht ergibt denselben Plan wie eine Kursdatei",
               plan["anzahl_selektionsfalten"] == 4 and plan["erstes_faltenjahr"] == 2022)


def teil_f():
    print("\nF. Mutationsprobe: die Vorlaufzeit")

    with tempfile.TemporaryDirectory() as ordner:
        schreibe_daten(ordner, {"AUSDT": "2021-09-01"})
        ohne = fp.plan_fuer_bot("rsi2_crypto", ordner, ["AUSDT"])
        pruefe("ohne Mutation: der heutige Datenbeginn ergibt null Falten",
               ohne["anzahl_selektionsfalten"] == 0)

        echt = fp.minus_jahre
        fp.minus_jahre = lambda datum, jahre: datum          # Vorlaufzeit faellt aus
        try:
            mit = fp.plan_fuer_bot("rsi2_crypto", ordner, ["AUSDT"])
        finally:
            fp.minus_jahre = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               mit["erstes_faltenjahr"] != ohne["erstes_faltenjahr"],
               f"{mit['erstes_faltenjahr']} vs {ohne['erstes_faltenjahr']}")
        pruefe("mit Mutation: es entstehen Falten, die es nicht geben darf",
               mit["anzahl_selektionsfalten"] > 0,
               "die Vorlaufzeit ist also nicht das, was die Falten begrenzt")
        pruefe("und sie saehe dabei BESSER aus als die richtige Zahl",
               mit["anzahl_selektionsfalten"] > ohne["anzahl_selektionsfalten"])


def teil_g():
    print("\nG. Mutationsprobe: der point-in-time-Filter")

    with tempfile.TemporaryDirectory() as ordner:
        schreibe_daten(ordner, {"AUSDT": "2017-08-17", "SPAETUSDT": "2025-01-19"})
        ohne = fp.plan_fuer_bot("rsi2_crypto", ordner, ["AUSDT", "SPAETUSDT"])
        pruefe("ohne Mutation: das spaete Paar ist in keiner Falte",
               all("SPAETUSDT" not in b["symbole"] for b in ohne["selektionsfalten"]))

        echt = fp.symbole_in_falte
        fp.symbole_in_falte = lambda beginn, faltenbeginn, mindesttraining=None: sorted(beginn)
        try:
            mit = fp.plan_fuer_bot("rsi2_crypto", ordner, ["AUSDT", "SPAETUSDT"])
        finally:
            fp.symbole_in_falte = echt
        pruefe("mit Mutation: die Verfaelschung greift ueberhaupt",
               any("SPAETUSDT" in b["symbole"] for b in mit["selektionsfalten"]))
        pruefe("mit Mutation: die ZAHL der Falten bleibt dabei unveraendert richtig",
               mit["anzahl_selektionsfalten"] == ohne["anzahl_selektionsfalten"],
               "die Falten-Zahl wuerde den Ausfall also gar nicht anzeigen")


def main() -> int:
    print("=" * 78)
    print("Selbsttest des Faltenplan-Werkzeugs (TB-31)")
    print("=" * 78)
    teil_a()
    teil_b()
    teil_c()
    teil_d()
    teil_e()
    teil_f()
    teil_g()
    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden} bestanden, {len(gescheitert)} GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
        return 1
    print(f"{bestanden}/{bestanden} Pruefungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
