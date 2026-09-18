#!/usr/bin/env python3
"""
Selbsttest zu `pruefe_abschnitt17.py` (TB-49)
==============================================================================
Ein Pruefwerkzeug, das immer "kein Befund" sagt, ist schlimmer als keines -
das ist die Lehre aus TB-45, und sie gilt fuer diesen Pruefer genauso wie fuer
die Wachen, die er nachrechnet.

Dieser Test zeigt dreierlei:

  1. **Der Pruefer beisst.** Zu jeder Bauform gehoert eine Probe, bei der er
     die Abweichung wirklich findet - an gestellten Quellen, nicht an den
     echten.
  2. **Die drei Rueckgabewerte sind unterscheidbar** (0 / 1 / 2), und
     "nicht pruefbar" ist die **2**, nie die 0.
  3. ⭐ **Am echten Bestand meldet er genau EINE Abweichung** - die frueheste
     Selektionsfalte - und endet mit **1**. Das ist die Erwartung aus TB-48;
     faellt sie anders aus, hat sich eine Quelle geaendert und das gehoert
     gesehen.

⚠️ Punkt 3 laeuft ueber alle 223 Kursdateien und kostet rund eine Minute.
Ohne ihn waere dieser Test die Behauptung statt der Messung.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 research/registernachtrag_tb48/test_abschnitt17.py
          python3 research/registernachtrag_tb48/test_abschnitt17.py --schnell
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)

import pruefe_abschnitt17 as p                                  # noqa: E402

WERKZEUG = os.path.join(_HIER, "pruefe_abschnitt17.py")

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print("  [OK ] %s%s" % (name, "   " + detail if detail else ""))
    else:
        FEHLER.append(name)
        print("  [FEHLER] %s%s" % (name, "   " + detail if detail else ""))


def _lauf(*argumente):
    """Das Werkzeug in einem eigenen Prozess - der Rueckgabewert zaehlt."""
    lauf = subprocess.run([sys.executable, WERKZEUG] + list(argumente),
                          capture_output=True, text=True)
    return lauf.returncode, (lauf.stdout or "") + (lauf.stderr or "")


# ---------------------------------------------------------------------------
def abschnitt_1_rechnung():
    """Die vier Pruefungen, die ohne Kursdaten auskommen."""
    print("\n1. DIE RECHNUNGEN OHNE QUELLE")
    m = p.Messungen()
    for nummer, funktion, name in (
            (17, p.p17_schwelle_18_von_19, "18/19 reisst die Schwelle"),
            (18, p.p18_schwelle_19_von_20, "19/20 reisst sie nicht"),
            (19, p.p19_mindestzahl, "n = 1/(1-0,95) = 20")):
        urteil, soll, ist = funktion(m)
        check("%d %s" % (nummer, name), urteil == p.OK,
              "Soll %s / Ist %s" % (soll, ist))

    check("_zeitpunkt liest beide Schreibweisen",
          p._zeitpunkt("2020-10-15").year == 2020
          and p._zeitpunkt("2020-10-15 00:00:00").hour == 0)
    try:
        p._zeitpunkt("15.10.2020")
        check("_zeitpunkt wirft bei unlesbarem Zeitpunkt", False)
    except ValueError:
        check("_zeitpunkt wirft bei unlesbarem Zeitpunkt", True)


def abschnitt_2_beisst():
    """⚠️ Jede Bauform an einer gestellten Quelle, an der sie beissen muss."""
    print("\n2. DER PRUEFER BEISST - an gestellten Quellen")
    arbeit = tempfile.mkdtemp(prefix="tb49_p17_")
    echt_falten, echt_register = p.FALTENPLAN, p.REGISTER
    try:
        # (a) Ein Faltenplan, der die Jahreszahl des Registers TRIFFT ->
        #     Pruefung 15 muss gruen werden. Faende sie auch dann etwas,
        #     pruefte sie nicht den Faltenplan.
        plan = json.loads(p._lies(echt_falten))
        plan["frueheste_falte"] = 2022
        gestellt = os.path.join(arbeit, "faltenplan_2022.json")
        with open(gestellt, "w", encoding="utf-8") as f:
            json.dump(plan, f)
        p.FALTENPLAN = gestellt
        urteil, _, ist = p.p15_frueheste_selektionsfalte(p.Messungen())
        check("15 findet NICHTS, wenn der Faltenplan 2022 sagt",
              urteil == p.OK, str(ist)[:90])

        # (b) Und etwas, wenn er etwas anderes sagt.
        plan["frueheste_falte"] = 2017
        gestellt2 = os.path.join(arbeit, "faltenplan_2017.json")
        with open(gestellt2, "w", encoding="utf-8") as f:
            json.dump(plan, f)
        p.FALTENPLAN = gestellt2
        urteil2, _, ist2 = p.p15_frueheste_selektionsfalte(p.Messungen())
        check("15 findet die Abweichung, wenn er 2017 sagt",
              urteil2 == p.ABWEICHUNG, str(ist2)[:90])
        p.FALTENPLAN = echt_falten

        # (c) ⚠️ Verschwindet der Satz aus dem Register, ist das NICHT
        #     PRUEFBAR - nicht "in Ordnung".
        ohne = os.path.join(arbeit, "register_ohne_satz.md")
        with open(ohne, "w", encoding="utf-8") as f:
            f.write(p._lies(echt_register)
                    .replace("Die erste Selektionsfalte beginnt", "X"))
        p.REGISTER = ohne
        urteil3, _, ist3 = p.p15_frueheste_selektionsfalte(p.Messungen())
        check("15 meldet NICHT PRUEFBAR, wenn der Satz fehlt",
              urteil3 == p.NICHT_PRUEFBAR, str(ist3)[:90])
        p.REGISTER = echt_register

        # (d) Die Mengengleichheit der elf Symbole an einem gestellten
        #     Backlog - eine blosse Zahlengleichheit genuegt ihr nicht.
        echt_backlog = p.BACKLOG
        vertauscht = os.path.join(arbeit, "backlog_vertauscht.md")
        with open(vertauscht, "w", encoding="utf-8") as f:
            f.write(p._lies(echt_backlog).replace("PEPE, PROM", "PEPE, XXXX"))
        p.BACKLOG = vertauscht
        try:
            m = p.Messungen()
            m._roh = _gestellte_befunde()
            urteil4, _, ist4 = p.p11_elf_symbole(m)
            check("11 findet ein vertauschtes Symbol trotz gleicher Anzahl",
                  urteil4 == p.ABWEICHUNG, str(ist4)[:110])
        finally:
            p.BACKLOG = echt_backlog

        # (e) Die Arten-Pruefung an einem gestellten `rand_letzte`.
        m2 = p.Messungen()
        m2._roh = _gestellte_befunde(mit_rand_letzte=True)
        urteil5, _, ist5 = p.p07_letzte_kerze_frei(m2)
        check("7 findet ein gestelltes `rand_letzte`",
              urteil5 == p.ABWEICHUNG, str(ist5)[:90])

        # (f) Die Kreuzprobe Falten x Befunde: ein Symbol, das in seiner
        #     Falte GELADEN ist, muss als Treffer erscheinen.
        m3 = p.Messungen()
        m3._roh = [{"datei": "BTCUSDT_1d.csv", "symbol": "BTCUSDT",
                    "intervall": "1d", "erste": "2019-06-01",
                    "befunde": [{"art": "rand_erste"}], "hinweise": []}]
        urteil6, _, ist6 = p.p16_kurze_kerze_in_geladener_falte(m3)
        check("16 findet eine kurze Kerze in einer geladenen Falte",
              urteil6 == p.ABWEICHUNG, str(ist6)[:90])
    finally:
        p.FALTENPLAN, p.REGISTER = echt_falten, echt_register
        shutil.rmtree(arbeit, ignore_errors=True)


def _gestellte_befunde(mit_rand_letzte=False):
    """36 Befunde in der Form, die `pruefe_ordner` liefert."""
    ab2023 = ["BMT", "ENA", "ENSO", "PEPE", "PROM", "PUMP", "SUI", "TRUMP",
              "U", "WLD", "ZKC"]
    eintraege = []
    for i, roh in enumerate(ab2023):
        eintraege.append({"datei": "%sUSDT_1d.csv" % roh,
                          "symbol": "%sUSDT" % roh, "intervall": "1d",
                          "erste": "2024-01-0%d" % (i % 9 + 1),
                          "befunde": [{"art": "rand_erste"}], "hinweise": []})
    for i in range(36 - len(ab2023)):
        eintraege.append({"datei": "ALT%02d_1d.csv" % i,
                          "symbol": "ALT%02d" % i, "intervall": "1d",
                          "erste": "2018-01-01",
                          "befunde": [{"art": "rand_erste"}], "hinweise": []})
    if mit_rand_letzte:
        eintraege[0]["befunde"].append({"art": "rand_letzte"})
    return eintraege


def abschnitt_3_rueckgabewerte():
    """Die drei Rueckgabewerte sind unterscheidbar."""
    print("\n3. DIE RUECKGABEWERTE")
    check("die drei Werte sind verschieden",
          len({p.OK_RC, p.BEFUND_RC, p.NICHT_PRUEFBAR_RC}) == 3,
          "%s / %s / %s" % (p.OK_RC, p.BEFUND_RC, p.NICHT_PRUEFBAR_RC))
    rc, ausgabe = _lauf("--nur", "17", "--nur", "18", "--nur", "19")
    check("drei gruene Pruefungen ergeben 0", rc == 0, "rc=%d" % rc)
    check("und die Ausgabe sagt KEIN BEFUND", "KEIN BEFUND" in ausgabe)
    rc2, ausgabe2 = _lauf("--nur", "15")
    check("die erwartete Abweichung allein ergibt 1", rc2 == 1, "rc=%d" % rc2)
    check("und die Ausgabe nennt sie beim Namen",
          "frueheste_selektionsfalte" in ausgabe2)
    rc3, ausgabe3 = _lauf("--falten-je-bot")
    check("--falten-je-bot laeuft durch und ergibt 0", rc3 == 0,
          "rc=%d" % rc3)
    check("und nennt alle neun Bots",
          all(b in ausgabe3 for b in ("elliott_wave", "t3_supertrend",
                                      "rsi2_crypto", "turtle_soup_stocks",
                                      "volatility_breakout_crypto")))


def abschnitt_4_echter_bestand():
    """⭐ Am echten Bestand: genau EINE Abweichung, Rueckgabewert 1."""
    print("\n4. AM ECHTEN BESTAND - 19 Zahlen, eine Abweichung")
    bericht = p.pruefe()
    check("alle 19 Pruefungen sind gelaufen",
          len(bericht["geprueft"]) == 19, "%d" % len(bericht["geprueft"]))
    check("keine war NICHT PRUEFBAR",
          not bericht["nicht_pruefbar"],
          str([z["pruefung"] for z in bericht["nicht_pruefbar"]]))
    check("genau EINE Abweichung", len(bericht["befunde"]) == 1,
          str([z["pruefung"] for z in bericht["befunde"]]))
    check("und es ist die frueheste Selektionsfalte (Nummer 15)",
          [z["nummer"] for z in bericht["befunde"]] == [15],
          str([z["nummer"] for z in bericht["befunde"]]))

    rc, ausgabe = _lauf()
    check("der Rueckgabewert der Befehlszeile ist 1", rc == 1, "rc=%d" % rc)
    check("die Ausgabe weist die eine Abweichung als erwartet aus",
          "erwartete Abweichung" in ausgabe)


def main():
    schnell = "--schnell" in sys.argv
    print("=" * 78)
    print("TB-49: Selbsttest des Pruefers fuer Abschnitt 17")
    print("=" * 78)
    abschnitte = [abschnitt_1_rechnung, abschnitt_2_beisst,
                  abschnitt_3_rueckgabewerte]
    if schnell:
        print("\n⚠️ --schnell: Abschnitt 4 (der echte Bestand) bleibt aus. "
              "Das ist kein vollstaendiger Lauf.")
    else:
        abschnitte.append(abschnitt_4_echter_bestand)
    for abschnitt in abschnitte:
        try:
            abschnitt()
        except Exception as fehler:                           # noqa: BLE001
            import traceback
            FEHLER.append("%s (Ausnahme)" % abschnitt.__name__)
            print("  [FEHLER] %s warf eine Ausnahme: %s"
                  % (abschnitt.__name__, fehler))
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print("%d von %d Pruefungen bestanden, %d fehlgeschlagen."
          % (BESTANDEN, gesamt, len(FEHLER)))
    for name in FEHLER:
        print("  - %s" % name)
    if gesamt == 0:
        print("KEINE EINZIGE PRUEFUNG GELAUFEN - das ist ein Fehler, "
              "kein Bestehen.")
        return 1
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
