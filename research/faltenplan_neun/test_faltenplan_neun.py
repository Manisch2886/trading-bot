#!/usr/bin/env python3
"""
Selbsttest des Faltenplans fuer alle neun Bots (TB-36)
==============================================================================
Geprueft wird, was die Aufgabenstellung ausdruecklich verlangt:

  A  **Die Gegenprobe Krypto.** Das neue Werkzeug liefert fuer die fuenf
     Krypto-Bots dieselben Zahlen wie das vorhandene TB-31-Werkzeug mit
     `--mindesttraining 0` - Falte fuer Falte und Symbol fuer Symbol.
  B  Die im Register eingetragenen Zahlen stimmen mit der Rechnung ueberein.
  C  Ein Symbol ohne Historie in einer Falte wird **nicht ausgeschlossen**.
  D  Die Embargo-Rechnung, an einem Bot MIT Zeitbremse und an einem OHNE;
     das 95. Perzentil an einer Reihe mit bekanntem Ergebnis.
  E  Der Registertext ist vollstaendig - und nichts ist geloescht worden.
  F-I  Mutationsproben.

ZU TEIL A - WARUM DIESE PROBE DIE TRAGENDE IST
------------------------------------------------------------------------------
Dieses Werkzeug ist das dritte im Repo, das Falten rechnet. Der Einwand gegen
ein drittes lautet zu Recht: die Faltenlogik soll genau einmal existieren.
Eingeloest wird das hier nicht durch ein Versprechen, sondern durch diese
Probe. Beide Werkzeuge laufen als **eigener Prozess** auf **denselben**
Kursdateien; verglichen werden Faltengrenzen und die Symbolliste je Falte,
nicht nur deren Anzahl. Laufen sie auseinander, faellt dieser Test - und dann
ist eine der beiden Zahlenreihen falsch, egal wie plausibel sie aussieht.

ZU DEN MUTATIONSPROBEN - DIE ZWEI WIEDERKEHRENDEN FALLEN
------------------------------------------------------------------------------
1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Deshalb wird hier keine Variable im laufenden Prozess umgebogen
   und anschliessend dieselbe Variable abgefragt. Jede Probe kopiert den
   Ordner (bzw. die betroffene Bot-Datei) in ein Wegwerf-Verzeichnis, aendert
   dort EINE Zeile und startet das Werkzeug als **eigenen Prozess** auf
   denselben Daten. Beobachtet wird der **Ablauf**: kommt eine andere Zahl
   heraus? Und jede Probe zeigt zuerst, dass sie ohne Mutation das Richtige
   sieht - sonst belegte ein rotes Ergebnis nichts.
2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Die vier Proben
   greifen deshalb vier verschiedene Wachen an, und jede weist nach, dass
   genau ihre Zahl kippt und die anderen stehen bleiben:

   * **F** verfaelscht die Registerschranke `FRUEHESTE_FALTE`. Faellt sie aus,
     beginnt der Plan zu frueh - und sieht dabei sogar **besser** aus, weil es
     mehr Falten werden. Die Symbolzahlen der uebrigen Falten bleiben
     unveraendert richtig; ohne eigene Probe fiele es nicht auf.
   * **G** verfaelscht die Doppeljahr-Schwelle. Faellt sie aus, bekommt
     `elliott_wave` sieben Einzeljahr-Falten statt drei Doppeljahre - die
     erste Falte und alle Symbolzahlen bleiben dabei richtig.
   * **H** verfaelscht den Indikator-Vorlauf eines Bots. Faellt er aus, wird
     die nachrichtliche Lesart B stillschweigend zur Kopie von Lesart A - die
     eingetragene Zahl aendert sich nicht, die Aussage ueber ihren Preis
     schon.
   * **I** verfaelscht die Zeitbremse in der **Bot-Datei** (nicht im
     Werkzeug). Aendert sich das Embargo nicht, kaeme die Zahl nicht aus dem
     Bot - sondern aus einer Abschrift im Werkzeug.

    python3 research/faltenplan_neun/test_faltenplan_neun.py

Rueckgabewert 0, wenn alle Pruefungen bestehen, sonst 1.
"""

import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
sys.path.insert(0, _HIER)

import embargo_neun as em          # noqa: E402
import faltenplan_neun as fp       # noqa: E402

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")
TB31_WERKZEUG = os.path.join(BASE_DIR, "research", "krypto_historie",
                             "faltenplan.py")
KRYPTO_BOTS = ["elliott_wave", "t3_supertrend", "rsi2_crypto",
               "turtle_soup_crypto", "volatility_breakout_crypto"]

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
        print(f"    ok   {name}")
    else:
        gescheitert.append(f"{name} {zusatz}".strip())
        print(f"    FEHL {name} {zusatz}".rstrip())


def _lauf(argv, umgebung=None):
    return subprocess.run([sys.executable] + argv, capture_output=True,
                          text=True, env=umgebung or os.environ.copy())


def _plan_json(werkzeug, argv, umgebung=None):
    """Werkzeug als eigener Prozess laufen lassen und seinen JSON-Bericht lesen."""
    with tempfile.TemporaryDirectory() as tmp:
        ziel = os.path.join(tmp, "bericht.json")
        r = _lauf([werkzeug] + argv + ["--json", ziel], umgebung)
        if r.returncode != 0 or not os.path.exists(ziel):
            return None, r
        with open(ziel, encoding="utf-8") as datei:
            return json.load(datei), r


# ===========================================================================
# A  Die Gegenprobe Krypto - gegen das TB-31-Werkzeug, im eigenen Prozess
# ===========================================================================
def teil_a():
    neu, r_neu = _plan_json(os.path.join(_HIER, "faltenplan_neun.py"), [])
    alt, r_alt = _plan_json(TB31_WERKZEUG, ["--mindesttraining", "0"])
    pruefe("A0: das neue Werkzeug laeuft durch",
           neu is not None, (r_neu.stderr or "")[-300:])
    pruefe("A1: das TB-31-Werkzeug laeuft durch",
           alt is not None, (r_alt.stderr or "")[-300:])
    if neu is None or alt is None:
        return

    neu = neu["plaene"]
    alt = alt["plaene"]
    for bot in KRYPTO_BOTS:
        n, a = neu[bot], alt[bot]
        pruefe(f"A2 [{bot}]: dieselbe erste Falte",
               n["erstes_faltenjahr"] == a["erstes_faltenjahr"],
               f"{n['erstes_faltenjahr']} gegen {a['erstes_faltenjahr']}")
        pruefe(f"A3 [{bot}]: dieselbe Zahl Selektionsfalten",
               n["anzahl_selektionsfalten"] == a["anzahl_selektionsfalten"],
               f"{n['anzahl_selektionsfalten']} gegen "
               f"{a['anzahl_selektionsfalten']}")

        n_falten = n["selektionsfalten"] + [n["bestaetigungsperiode"]]
        a_falten = a["selektionsfalten"] + [a["bestaetigungsperiode"]]
        pruefe(f"A4 [{bot}]: dieselben Faltengrenzen",
               [(f["von"], f["bis_ausschliesslich"]) for f in n_falten]
               == [(f["von"], f["bis_ausschliesslich"]) for f in a_falten],
               f"{[f['von'] for f in n_falten]} gegen "
               f"{[f['von'] for f in a_falten]}")
        pruefe(f"A5 [{bot}]: dieselben Symbole je Falte, namentlich",
               all(sorted(x["symbole_a"]) == sorted(y["symbole"])
                   for x, y in zip(n_falten, a_falten)),
               f"{[len(f['symbole_a']) for f in n_falten]} gegen "
               f"{[len(f['symbole']) for f in a_falten]}")


# ===========================================================================
# B  Die eingetragenen Zahlen gegen die gerechneten
# ===========================================================================
def _registertabelle(ueberschrift, spalten):
    """Die Zeilen der ersten Markdown-Tabelle nach `ueberschrift`."""
    text = open(REGISTER, encoding="utf-8").read()
    ab = text.index(ueberschrift)
    zeilen = []
    gefunden = False
    for zeile in text[ab:].splitlines():
        if zeile.startswith("|"):
            gefunden = True
            felder = [f.strip() for f in zeile.strip().strip("|").split("|")]
            kopf = not felder[0].startswith("`")
            if len(felder) == spalten and not kopf:
                zeilen.append(felder)
        elif gefunden and zeile.strip() == "":
            break
    return zeilen


def _zahlenreihe(feld):
    return [int(x) for x in re.findall(r"\d+", feld.replace("*", ""))]


def teil_b():
    plan = fp.faltenplan()
    emb = em.embargos()

    zeilen = _registertabelle("**Die Symbolzahl je Falte** "
                              "(Tatsachennotiz zu 3b)", 4)
    pruefe("B0: die Symbolzahl-Tabelle steht im Register und hat neun Zeilen",
           len(zeilen) == 9, f"{len(zeilen)} Zeilen")
    for felder in zeilen:
        bot = felder[0].strip("`")
        if bot not in plan:
            pruefe(f"B1 [{felder[0]}]: Bot bekannt", False)
            continue
        p = plan[bot]
        pruefe(f"B1 [{bot}]: Symbolzahl je Selektionsfalte wie gerechnet",
               _zahlenreihe(felder[1]) == p["symbolzahl_je_selektionsfalte"],
               f"Register {felder[1]!r} gegen "
               f"{p['symbolzahl_je_selektionsfalte']}")
        pruefe(f"B2 [{bot}]: Symbolzahl der Bestaetigung wie gerechnet",
               int(felder[2]) == p["symbolzahl_bestaetigung"],
               f"Register {felder[2]} gegen {p['symbolzahl_bestaetigung']}")
        pruefe(f"B3 [{bot}]: Universumsgroesse wie gerechnet",
               int(felder[3]) == p["symbole_gesamt"])

    zeilen = _registertabelle("**Die Faltenliste je Bot** "
                              "(Tatsachennotiz zu 4d)", 6)
    pruefe("B4: die Faltenliste steht im Register und hat neun Zeilen",
           len(zeilen) == 9, f"{len(zeilen)} Zeilen")
    for felder in zeilen:
        bot = felder[0].strip("`")
        if bot not in plan:
            continue
        p = plan[bot]
        pruefe(f"B5 [{bot}]: Zahl der Selektionsfalten wie gerechnet",
               int(felder[4]) == p["anzahl_selektionsfalten"],
               f"Register {felder[4]} gegen {p['anzahl_selektionsfalten']}")
        jahre = [j for b in p["selektionsfalten"] for j in
                 ([b["jahre"][0]] if len(b["jahre"]) == 1
                  else [b["jahre"][0], b["jahre"][-1]])]
        pruefe(f"B6 [{bot}]: die Faltenjahre wie gerechnet",
               _zahlenreihe(felder[3]) == jahre,
               f"Register {felder[3]!r}")

    zeilen = _registertabelle("**Das Embargo je Bot** (Tatsachennotiz zu 2d",
                              5)
    pruefe("B7: die Embargo-Tabelle steht im Register und hat neun Zeilen",
           len(zeilen) == 9, f"{len(zeilen)} Zeilen")
    for felder in zeilen:
        bot = felder[0].strip("`")
        if bot not in emb:
            continue
        pruefe(f"B8 [{bot}]: Embargo wie gerechnet",
               _zahlenreihe(felder[4])[0] == emb[bot]["embargo_handelstage"],
               f"Register {felder[4]!r} gegen "
               f"{emb[bot]['embargo_handelstage']}")

    pruefe("B9: kein Bot ist unterbestimmt (Registertext 4b: mindestens 3)",
           all(p["anzahl_selektionsfalten"] >= 3 for p in plan.values()),
           str({b: p["anzahl_selektionsfalten"] for b, p in plan.items()
                if p["anzahl_selektionsfalten"] < 3}))


# ===========================================================================
# C  Kein Symbol wird ausgeschlossen - am Ablauf, auf erzeugten Daten
# ===========================================================================
def _mini_universum(ordner):
    """Ein Wegwerf-Repo mit drei Symbolen und bekannter Historie.

    `AAA` ist von Anfang an da, `BBB` beginnt MITTEN in der Falte 2021 (und
    hat am 1. Januar 2021 also keine Historie), `CCC` beginnt erst nach dem
    Go-Live-Schnitt. Keins der drei darf aus dem Universum verschwinden.
    """
    os.makedirs(os.path.join(ordner, "config"))
    os.makedirs(os.path.join(ordner, "data"))
    # Die TB-24-Trades braucht das Werkzeug fuer die Faltenlaenge - sie werden
    # nicht nachgebaut, sondern aus dem Repo mitgelesen.
    os.symlink(os.path.join(BASE_DIR, "research"),
               os.path.join(ordner, "research"))
    for liste in ("top25_symbols.txt", "sp500_top150.txt"):
        with open(os.path.join(ordner, "config", liste), "w",
                  encoding="utf-8") as datei:
            datei.write("AAA\nBBB\nCCC\n")
    beginn = {"AAA": dt.date(2018, 1, 1), "BBB": dt.date(2021, 6, 15),
              "CCC": dt.date(2026, 10, 1)}
    for symbol, start in beginn.items():
        zeilen = ["open_time,open,high,low,close,volume"]
        tag = start
        while tag < dt.date(2026, 12, 31):
            zeilen.append(f"{tag.isoformat()},1,1,1,1,1")
            tag += dt.timedelta(days=1)
        inhalt = "\n".join(zeilen) + "\n"
        # Alle drei Zeitrahmen, damit auch die Stunden- und
        # Vier-Stunden-Bots einen Plan bekommen - gezaehlt werden hier
        # ohnehin nur Balken und Daten.
        for zeitrahmen in ("1d", "4h", "1h"):
            with open(os.path.join(ordner, "data",
                                   f"{symbol}_{zeitrahmen}.csv"), "w",
                      encoding="utf-8") as datei:
                datei.write(inhalt)
    return ordner


def teil_c():
    with tempfile.TemporaryDirectory() as tmp:
        ordner = _mini_universum(os.path.join(tmp, "repo"))
        umgebung = os.environ.copy()
        umgebung["TB36_BASE_DIR"] = ordner
        bericht, r = _plan_json(os.path.join(_HIER, "faltenplan_neun.py"), [],
                                umgebung)
        pruefe("C0: das Werkzeug laeuft auf dem Wegwerf-Universum",
               bericht is not None, (r.stderr or "")[-300:])
        if bericht is None:
            return
        p = bericht["plaene"]["rsi2_crypto"]

        pruefe("C1: das Universum behaelt alle drei Symbole",
               p["symbole_gesamt"] == 3, str(p["symbole_gesamt"]))

        falten = {str(f["jahre"][0]): f for f in p["selektionsfalten"]}
        pruefe("C2: BBB ist am 1.1.2021 ohne Historie und zaehlt dort nicht mit",
               falten["2021"]["symbole_a"] == ["AAA"],
               str(falten["2021"]["symbole_a"]))
        pruefe("C3: BBB steht in derselben Falte als 'ohne Historie' - es ist "
               "nicht verschwunden",
               "BBB" in falten["2021"]["symbole_ohne_historie"],
               str(falten["2021"]["symbole_ohne_historie"]))
        pruefe("C4: in der naechsten Falte ist BBB dabei",
               falten["2022"]["symbole_a"] == ["AAA", "BBB"],
               str(falten["2022"]["symbole_a"]))
        pruefe("C5: in JEDER Falte gilt 'mit Historie + ohne Historie = "
               "Universum'",
               all(len(f["symbole_a"]) + len(f["symbole_ohne_historie"])
                   == p["symbole_gesamt"]
                   for f in p["selektionsfalten"] + [p["bestaetigungsperiode"]]))
        pruefe("C6: CCC hat in keiner Falte Historie und wird trotzdem "
               "namentlich gefuehrt",
               "CCC" in p["nie_in_einer_selektionsfalte"]
               and "CCC" in p["symbolbeginn"],
               str(p["nie_in_einer_selektionsfalte"]))

        # Und dasselbe im echten Universum: die Symbole verschwinden nirgends.
        echt = fp.faltenplan()
        pruefe("C7: auch im echten Universum bleibt in jeder Falte die Summe "
               "vollstaendig",
               all(len(f["symbole_a"]) + len(f["symbole_ohne_historie"])
                   == pl["symbole_gesamt"]
                   for pl in echt.values()
                   for f in pl["selektionsfalten"] + [pl["bestaetigungsperiode"]]))


# ===========================================================================
# D  Das Embargo
# ===========================================================================
def teil_d():
    # --- das Perzentil an einer Reihe mit bekanntem Ergebnis --------------
    # 1..100, lineare Interpolation: 1 + 0,95 * 99 = 95,05.
    pruefe("D0: P95 von 1..100 ist 95,05 (lineare Interpolation)",
           abs(em.perzentil(list(range(1, 101)), 0.95) - 95.05) < 1e-9,
           str(em.perzentil(list(range(1, 101)), 0.95)))
    pruefe("D1: P50 von 1..100 ist 50,5",
           abs(em.perzentil(list(range(1, 101)), 0.50) - 50.5) < 1e-9)
    pruefe("D2: ein einziger Wert ist sein eigenes Perzentil",
           em.perzentil([7.0], 0.95) == 7.0)
    pruefe("D3: eine leere Reihe hat kein Perzentil",
           em.perzentil([], 0.95) is None)

    # --- dieselbe Rechnung wie TB-24: die dort veroeffentlichten P90 ------
    # Gelesen, nicht abgeschrieben: aendert der Betreiber die TB-24-Zahlen,
    # wird dieser Test rot.
    pfad = os.path.join(BASE_DIR, "research", "tb24_haltedauern", "ergebnisse",
                        "haltedauern_je_bot.csv")
    import csv as _csv
    with open(pfad, encoding="utf-8") as datei:
        for zeile in _csv.DictReader(datei):
            bot = zeile["bot"]
            eigen = em.perzentil(em.haltedauern_tage(bot), 0.90)
            pruefe(f"D4 [{bot}]: P90 wie in TB-24 veroeffentlicht",
                   abs(eigen - float(zeile["tage_p90"])) < 5e-3,
                   f"{eigen:.4f} gegen {zeile['tage_p90']}")

    # --- ein Bot MIT Zeitbremse -------------------------------------------
    e = em.embargo_fuer_bot("rsi2_crypto")
    wert, _ = em.lies_konstante("strategies/rsi2_crypto/live_params.py",
                                "MAX_HOLD_DAYS")
    pruefe("D5: rsi2_crypto wird ueber die Zeitbremse gerechnet",
           e["art"] == "zeitbremse", e["art"])
    pruefe("D6: sein Embargo ist die Zeitbremse plus 1",
           e["embargo_handelstage"] == int(wert) + 1,
           f"{e['embargo_handelstage']} gegen {int(wert) + 1}")

    # --- ein Bot OHNE Zeitbremse -------------------------------------------
    e = em.embargo_fuer_bot("t3_supertrend")
    p95 = em.perzentil(em.haltedauern_tage("t3_supertrend"), 0.95)
    pruefe("D7: t3_supertrend hat keine Zeitbremse und wird ueber P95 "
           "gerechnet",
           e["art"] == "perzentil" and em.ZEITBREMSEN["t3_supertrend"] == [],
           e["art"])
    pruefe("D8: sein Embargo ist das aufgerundete P95 plus 1",
           e["embargo_handelstage"] == int(-(-p95 // 1)) + 1,
           f"{e['embargo_handelstage']} gegen P95 {p95:.4f}")
    pruefe("D9: genau ein Bot hat keine Zeitbremse",
           sum(1 for b in fp.BOTS if not em.ZEITBREMSEN[b]) == 1)

    # --- die zwei Zeitbremsen von elliott_wave_stocks ----------------------
    e = em.embargo_fuer_bot("elliott_wave_stocks")
    pruefe("D10: elliott_wave_stocks fuehrt zwei Zeitbremsen",
           len(e["zeitbremsen"]) == 2, str(len(e["zeitbremsen"])))
    pruefe("D11: gewaehlt wird die laengste in Handelstagen",
           e["laengste_zeitbremse"]["handelstage"]
           == max(b["handelstage"] for b in e["zeitbremsen"]))
    pruefe("D12: 130 Kalendertage sind weniger Handelstage als 90 Balken",
           min(b["handelstage"] for b in e["zeitbremsen"]) < 90,
           str([b["handelstage"] for b in e["zeitbremsen"]]))


# ===========================================================================
# E  Der Registertext - vollstaendig, und nichts geloescht
# ===========================================================================
ERSETZT_MARKER = [
    "[ersetzt die frühere Fassung mit Mindestzahl 10 Trades]",
    '[ersetzt „mindestens 4"]',
    '[ersetzt „behält seine heutigen Parameter"]',
    "*(ersetzt die frühere Fassung vollständig)*",
]

BESTAND = [                       # Saetze, die stehen bleiben MUESSEN
    "### 5.1 Die Regeln",
    "### 5.3 Krypto: Platzhalter mit Regel",
    "1. **Verankert, expandierend** (nicht rollierend).",
    "5. **Purge und Embargo** in Höhe der **maximalen gemessenen Haltedauer**",
    "8. **Universumsdateien und point-in-time-Regel**",
    "### Der Faltenplan",
]


def teil_e():
    text = open(REGISTER, encoding="utf-8").read()

    for nummer in range(6):
        pruefe(f"E0: Registertext {nummer} steht im Nachtrag",
               re.search(rf"### 15\.\d+ Registertext {nummer} —", text)
               is not None)

    for marker in ERSETZT_MARKER:
        pruefe(f"E1: als ersetzt gekennzeichnet - {marker[:46]}...",
               marker in text)

    pruefe("E2: die ersetzten Stellen im alten Text verweisen auf den Nachtrag",
           text.count("ERSETZT durch Abschnitt 15") == 3,
           str(text.count("ERSETZT durch Abschnitt 15")))
    pruefe("E3: auch die Sperrliste traegt den Hinweis",
           "ist **ersetzt** (Abschnitt 15,\n   > Registertext 3)" in text)

    for satz in BESTAND:
        pruefe(f"E4: nicht geloescht - {satz[:46]}...", satz in text)

    # --- nichts geloescht, maschinell gegen die letzte Fassung OHNE Nachtrag
    vorher = _fassung_ohne_nachtrag()
    if vorher is None:
        pruefe("E5: eine Vorfassung ohne Nachtrag ist auffindbar", False,
               "git nicht verfuegbar oder keine solche Fassung")
        return
    alt_zeilen = vorher.splitlines()
    neu_zeilen = text.splitlines()
    fehlend = _nicht_enthalten(alt_zeilen, neu_zeilen)
    pruefe("E5: jede Zeile der Vorfassung steht unveraendert und in derselben "
           "Reihenfolge noch im Register",
           not fehlend, f"{len(fehlend)} fehlende Zeile(n), z.B. "
                        f"{fehlend[:2]}")


def _fassung_ohne_nachtrag():
    """Die juengste committete Fassung des Registers OHNE Abschnitt 15."""
    r = subprocess.run(["git", "log", "--format=%H", "--",
                        "docs/VORREGISTRIERUNG_neuselektion.md"],
                       capture_output=True, text=True, cwd=BASE_DIR)
    if r.returncode != 0:
        return None
    for commit in r.stdout.split():
        b = subprocess.run(
            ["git", "show", f"{commit}:docs/VORREGISTRIERUNG_neuselektion.md"],
            capture_output=True, text=True, cwd=BASE_DIR)
        if b.returncode == 0 and "## 15. Registernachtrag" not in b.stdout:
            return b.stdout
    return None


def _nicht_enthalten(alt, neu):
    """Die Zeilen aus `alt`, die in `neu` nicht als Teilfolge vorkommen."""
    fehlend, i = [], 0
    for zeile in alt:
        while i < len(neu) and neu[i] != zeile:
            i += 1
        if i < len(neu):
            i += 1
        else:
            fehlend.append(zeile)
            i = 0
    return fehlend


# ===========================================================================
# F-I  Mutationsproben - am Ablauf, im eigenen Prozess
# ===========================================================================
def _werkzeugkopie(ziel):
    shutil.copytree(_HIER, ziel, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "daten"))
    return ziel


def _ersetze(pfad, alt, neu):
    with open(pfad, encoding="utf-8") as datei:
        s = datei.read()
    if alt not in s:
        raise AssertionError(f"Mutationsstelle nicht gefunden in {pfad}: {alt!r}")
    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write(s.replace(alt, neu, 1))


def _mutiert(datei, alt, neu, werkzeug="faltenplan_neun.py"):
    """Den Ordner kopieren, EINE Zeile aendern, das Werkzeug neu starten."""
    with tempfile.TemporaryDirectory() as m:
        ordner = _werkzeugkopie(os.path.join(m, "werkzeug"))
        _ersetze(os.path.join(ordner, datei), alt, neu)
        # Die Repo-Wurzel wandert mit - sonst suchte die Kopie ihre
        # Kursdateien neben dem Wegwerf-Ordner und die Probe scheiterte
        # am fehlenden Pfad statt an der Mutation. Eine Probe, die aus
        # dem falschen Grund scheitert, belegt nichts.
        umgebung = os.environ.copy()
        umgebung["TB36_BASE_DIR"] = BASE_DIR
        bericht, r = _plan_json(os.path.join(ordner, werkzeug), [],
                                umgebung)
        return bericht, r


def teil_f():
    original = fp.faltenplan()
    pruefe("F0: unmutiert beginnt jeder Plan 2019",
           all(p["erstes_faltenjahr"] == 2019 for p in original.values()),
           str({b: p["erstes_faltenjahr"] for b, p in original.items()}))

    bericht, r = _mutiert("faltenplan_neun.py",
                          "FRUEHESTE_FALTE = 2019", "FRUEHESTE_FALTE = 2015")
    pruefe("F1: das mutierte Werkzeug laeuft (sonst belegte F2 nichts)",
           bericht is not None, (r.stderr or "")[-300:])
    if bericht is None:
        return
    mutiert = bericht["plaene"]
    frueher = [b for b in fp.BOTS
               if mutiert[b]["erstes_faltenjahr"] < 2019]
    pruefe("F2: ohne die Registerschranke beginnen acht der neun Plaene "
           "frueher - die Schranke traegt",
           len(frueher) == 8, f"{len(frueher)} Bots: {sorted(frueher)}")
    pruefe("F3: bei rsi2_crypto bindet die Datenlage, nicht die Schranke",
           mutiert["rsi2_crypto"]["erstes_faltenjahr"] == 2019,
           str(mutiert["rsi2_crypto"]["erstes_faltenjahr"]))


def teil_g():
    original = fp.faltenplan()
    pruefe("G0: unmutiert hat genau ein Bot Doppeljahre",
           sum(1 for p in original.values()
               if p["faltenlaenge_jahre"] == 2) == 1)
    pruefe("G1: und es ist elliott_wave mit drei Falten",
           original["elliott_wave"]["faltenlaenge_jahre"] == 2
           and original["elliott_wave"]["anzahl_selektionsfalten"] == 3)

    bericht, r = _mutiert("faltenplan_neun.py",
                          "ZWEIJAHRES_SCHWELLE_TRADES = 30",
                          "ZWEIJAHRES_SCHWELLE_TRADES = 0")
    pruefe("G2: das mutierte Werkzeug laeuft", bericht is not None,
           (r.stderr or "")[-300:])
    if bericht is None:
        return
    mutiert = bericht["plaene"]
    pruefe("G3: ohne die Schwelle bekommt elliott_wave Einzeljahre - die "
           "Doppeljahr-Regel traegt",
           mutiert["elliott_wave"]["faltenlaenge_jahre"] == 1
           and mutiert["elliott_wave"]["anzahl_selektionsfalten"] == 7,
           str(mutiert["elliott_wave"]["anzahl_selektionsfalten"]))
    pruefe("G4: und KEINE andere Wache faengt das ab - erste Falte und "
           "Symbolzahlen bleiben unveraendert richtig",
           mutiert["elliott_wave"]["erstes_faltenjahr"] == 2019
           and mutiert["rsi2_crypto"]["symbolzahl_je_selektionsfalte"]
           == original["rsi2_crypto"]["symbolzahl_je_selektionsfalte"])


def teil_h():
    original = fp.faltenplan()
    pruefe("H0: unmutiert weicht Lesart B bei rsi2_crypto von Lesart A ab",
           original["rsi2_crypto"]["symbolzahl_je_selektionsfalte"]
           != original["rsi2_crypto"]["symbolzahl_je_selektionsfalte_lesart_b"])

    bericht, r = _mutiert("faltenplan_neun.py",
                          '"markt": "krypto", "zeitrahmen": "1d", '
                          '"vorlauf_balken": 150',
                          '"markt": "krypto", "zeitrahmen": "1d", '
                          '"vorlauf_balken": 0')
    pruefe("H1: das mutierte Werkzeug laeuft", bericht is not None,
           (r.stderr or "")[-300:])
    if bericht is None:
        return
    mutiert = bericht["plaene"]["rsi2_crypto"]
    pruefe("H2: ohne Vorlauf faellt Lesart B mit Lesart A zusammen - der "
           "Vorlauf wird wirklich gelesen",
           mutiert["symbolzahl_je_selektionsfalte_lesart_b"]
           == mutiert["symbolzahl_je_selektionsfalte"],
           str(mutiert["symbolzahl_je_selektionsfalte_lesart_b"]))
    pruefe("H3: die EINGETRAGENE Zahl (Lesart A) bleibt davon unberuehrt - "
           "keine zweite Wache verdeckt das",
           mutiert["symbolzahl_je_selektionsfalte"]
           == original["rsi2_crypto"]["symbolzahl_je_selektionsfalte"])


def _repo_mit_mutierter_botdatei(ordner, relpfad, alt, neu):
    """Wegwerf-Repo: alles verlinkt, nur die eine Bot-Datei kopiert."""
    os.makedirs(ordner)
    for name in ("config", "data", "research"):
        os.symlink(os.path.join(BASE_DIR, name), os.path.join(ordner, name))
    # `strategies` wird bot-weise verlinkt; nur der eine Bot-Ordner ist
    # eine echte Kopie. So sieht das Werkzeug alle neun Bots, aber nur
    # einer ist mutiert.
    mutierter_bot = relpfad.split(os.sep)[1]
    os.makedirs(os.path.join(ordner, "strategies"))
    for name in sorted(os.listdir(os.path.join(BASE_DIR, "strategies"))):
        if name != mutierter_bot:
            os.symlink(os.path.join(BASE_DIR, "strategies", name),
                       os.path.join(ordner, "strategies", name))
    ziel = os.path.join(ordner, relpfad)
    os.makedirs(os.path.dirname(ziel))
    for name in sorted(os.listdir(os.path.join(BASE_DIR, "strategies",
                                               mutierter_bot))):
        quelle = os.path.join(BASE_DIR, "strategies", mutierter_bot, name)
        if os.path.isfile(quelle):
            shutil.copy2(quelle, os.path.dirname(ziel))
    _ersetze(ziel, alt, neu)
    return ordner


def teil_i():
    vorher = em.embargo_fuer_bot("rsi2_crypto")["embargo_handelstage"]
    pruefe("I0: unmutiert ist das Embargo von rsi2_crypto 11",
           vorher == 11, str(vorher))

    relpfad = os.path.join("strategies", "rsi2_crypto", "live_params.py")
    with tempfile.TemporaryDirectory() as tmp:
        ordner = _repo_mit_mutierter_botdatei(
            os.path.join(tmp, "repo"), relpfad,
            "MAX_HOLD_DAYS = 10", "MAX_HOLD_DAYS = 42")
        umgebung = os.environ.copy()
        umgebung["TB36_BASE_DIR"] = ordner
        with tempfile.TemporaryDirectory() as aus:
            ziel = os.path.join(aus, "e.json")
            r = _lauf([os.path.join(_HIER, "embargo_neun.py"), "--json", ziel],
                      umgebung)
            pruefe("I1: das Werkzeug laeuft auf dem mutierten Repo",
                   r.returncode == 0 and os.path.exists(ziel),
                   (r.stderr or "")[-300:])
            if not os.path.exists(ziel):
                return
            with open(ziel, encoding="utf-8") as datei:
                mutiert = json.load(datei)
    pruefe("I2: eine geaenderte Zeitbremse im BOT aendert das Embargo - die "
           "Zahl kommt aus der Bot-Datei, nicht aus einer Abschrift",
           mutiert["rsi2_crypto"]["embargo_handelstage"] == 43,
           str(mutiert["rsi2_crypto"]["embargo_handelstage"]))
    pruefe("I3: und nur bei diesem Bot - die anderen acht bleiben stehen",
           all(mutiert[b]["embargo_handelstage"]
               == em.embargo_fuer_bot(b)["embargo_handelstage"]
               for b in fp.BOTS if b != "rsi2_crypto"))


def main():
    print(__doc__.strip().split("\n")[0])
    print("=" * 78)
    for name, teil in (("A", teil_a), ("B", teil_b), ("C", teil_c),
                       ("D", teil_d), ("E", teil_e), ("F", teil_f),
                       ("G", teil_g), ("H", teil_h), ("I", teil_i)):
        print(f"  Teil {name} ...", flush=True)
        teil()
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
