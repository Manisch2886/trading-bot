#!/usr/bin/env python3
"""
TB-51: kennt der Basislauf die Stufe "flackernd" - und beisst der Nachweis?
==============================================================================
`research/datenordner_schnitt/basislauf.py` kannte drei Listen: `BEKANNT_ROT`,
`UNGEPRUEFT`, `LAEUFT_WEITER`. Fuer einen Test, der **gruen im Regelfall und
zeitabhaengig rot** ist (`system/test_log_rotation.py`, Mac: 3 von 10 rot,
TB-49), war damit **jede** Einordnung falsch:

  * **kein Eintrag**         -> ein roter Lauf wird UNERWARTET gemeldet (~30 %)
  * **Eintrag in BEKANNT_ROT** -> jeder gruene Lauf wird UNERWARTET gemeldet (~70 %)

TB-51 legt die vierte Liste `FLACKERND` an: beide Ausgaenge sind erwartet, die
Datei zaehlt **eigens** - nicht unter gruen, nicht unter rot -, und die
Ausgabezeile nennt das Ergebnis dieses Laufs und die hinterlegte Rate.

WIE DIESER TEST MISST
------------------------------------------------------------------------------
⚠️ **Am Verhalten, nicht am Quelltext - und ohne vollen Basislauf.** Der
Basislauf dauert 40 Minuten; hier bekommt `basislauf.main()` **gestellte
Ergebnisse**: `testdateien` und `fuehre_aus` werden im geladenen Modul durch
Stellvertreter ersetzt, die Listen durch eine Probeliste. Dann wird die
Ausgabe gelesen, so wie ein Mensch sie liest: die Zeile je Datei, der
Vermerk `<-- UNERWARTET`, die Zahlen unter dem Strich.

⚠️⚠️ **Prueprinzip B1: eine Wache, die nicht beisst, ist keine.** Jede Probe
laeuft ein zweites Mal gegen eine **Mutante** - dieselbe Datei, im Speicher
um genau eine Stelle veraendert - und muss dort **fehlschlagen**. Findet eine
Probe den Fall auch in der Mutante richtig, prueft sie etwas anderes als
angenommen; das waere ein Befund ueber den Test, nicht ueber das Werkzeug.

Die Mutanten, je Probe eine:

  * **M1 "ohne die Stufe"**  - die neue `elif`-Stufe ist abgeschaltet
                               (`elif False:`). Das ist die Fassung vor TB-51.
                               Proben 1 und 2 muessen darin scheitern.
  * **M2 "Stufe greift zu weit"** - die Stufe faengt JEDEN gruenen oder roten
                               Lauf ab, nicht nur die eingetragenen. Proben 3
                               und 4 (die alten Stufen bleiben, wie sie sind)
                               muessen darin scheitern. ⚠️ In M1 muessen sie
                               dagegen weiter bestehen - genau das ist ihre
                               Aussage.
  * **M3 "Summenzeile ohne flackernd"** - die Zahlen unter dem Strich lassen
                               die neue Stufe aus. Probe 5 muss darin scheitern.

⭐ **Und die Gegenprobe gegen die WIRKLICHE Vorgaengerfassung:** Proben 1 und 2
laufen zusaetzlich gegen `basislauf.py` aus Commit `58c0ab9` (der Stand vor
TB-51, aus `git show`) - dort muessen sie ebenfalls scheitern. Ist git nicht
erreichbar, ist das ein roter Ausgang, kein uebersprungener (A1).

Nutzung:  python3 research/datenordner_schnitt/test_flackerstufe.py
"""

import contextlib
import copy
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import types

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
BASISLAUF_PFAD = os.path.join(_HIER, "basislauf.py")
BASISLAUF_REL = os.path.relpath(BASISLAUF_PFAD, _WURZEL)
VORGAENGER_COMMIT = "58c0ab9"        # der Stand von main vor TB-51

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


# ---------------------------------------------------------------------------
# Das Werkzeug laden - aus der Datei, aus veraendertem Quelltext, aus git
# ---------------------------------------------------------------------------

def lade_basislauf():
    """`basislauf.py` ueber den Dateipfad laden, nicht ueber den Suchpfad
    (TB-40: gleichnamige Module werden hier nie ueber `sys.path` importiert)."""
    spez = importlib.util.spec_from_file_location("tb51_basislauf",
                                                  BASISLAUF_PFAD)
    modul = importlib.util.module_from_spec(spez)
    spez.loader.exec_module(modul)
    return modul


def lade_aus_text(text, name):
    """Denselben Quelltext - veraendert - als frisches Modul ausfuehren."""
    modul = types.ModuleType(name)
    modul.__file__ = BASISLAUF_PFAD
    exec(compile(text, BASISLAUF_PFAD, "exec"), modul.__dict__)
    return modul


def quelltext():
    with open(BASISLAUF_PFAD, "r", encoding="utf-8") as f:
        return f.read()


def mutante(name, ersetzungen):
    """Eine Mutante: jede Ersetzung muss GENAU EINMAL treffen - sonst
    veraendert sie etwas anderes als gedacht, und die Gegenprobe waere
    wertlos."""
    text = quelltext()
    for alt, neu in ersetzungen:
        treffer = text.count(alt)
        if treffer != 1:
            raise RuntimeError("Mutante %s: Ankertext %r trifft %d-mal, "
                               "nicht einmal" % (name, alt, treffer))
        text = text.replace(alt, neu)
    return lade_aus_text(text, "tb51_mutante_" + name)


def vorgaengerfassung():
    """`basislauf.py` aus dem Commit vor TB-51 - die wirkliche Fassung ohne
    die Stufe. Rueckgabe (modul, fehlertext)."""
    try:
        lauf = subprocess.run(
            ["git", "show", "%s:%s" % (VORGAENGER_COMMIT, BASISLAUF_REL)],
            cwd=_WURZEL, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as fehler:
        return None, "git nicht ausfuehrbar: %s" % fehler
    if lauf.returncode != 0 or not lauf.stdout.strip():
        # ⚠️ A1: ein gescheiterter Aufruf ist kein leeres Ergebnis.
        return None, ("git show rc=%d, %s"
                      % (lauf.returncode, (lauf.stderr or "").strip()[:120]))
    if "FLACKERND" in lauf.stdout:
        return None, ("Commit %s kennt FLACKERND schon - das ist nicht die "
                      "Fassung ohne die Stufe" % VORGAENGER_COMMIT)
    return lade_aus_text(lauf.stdout, "tb51_vorgaenger"), ""


# ---------------------------------------------------------------------------
# Die gestellte Lage: sieben Dateien, jede Stufe einmal vertreten
# ---------------------------------------------------------------------------

FLK_GRUEN = "probe/test_wechselhaft_heute_gruen.py"
FLK_ROT = "probe/test_wechselhaft_heute_rot.py"
BR_GRUEN = "probe/test_bekannt_rot_heute_gruen.py"
OHNE_ROT = "probe/test_ohne_liste_rot.py"
OHNE_GRUEN = "probe/test_ohne_liste_gruen.py"
UNGEPR = "probe/test_ungeprueft.py"
ZEIT = "probe/test_laeuft_weiter.py"

DATEIEN = [FLK_GRUEN, FLK_ROT, BR_GRUEN, OHNE_ROT, OHNE_GRUEN, UNGEPR, ZEIT]

LISTEN = {
    "FLACKERND": {FLK_GRUEN: "Probe ~30 %, gestellt",
                  FLK_ROT: "Probe ~30 %, gestellt"},
    "BEKANNT_ROT": {BR_GRUEN: "Probe: bekannt rot, gestellt"},
    "UNGEPRUEFT": {UNGEPR: "verlangt ein Argument (gestellt)"},
    "LAEUFT_WEITER": {ZEIT: "terminiert nicht (gestellt)"},
}


def _ergebnis(rel, art, rueckgabe):
    return {"datei": rel, "rueckgabe": rueckgabe, "art": art, "sekunden": 0.1,
            "abgebrochen": art == "zeitgrenze",
            "letzte_zeilen": ["gestellt: %s" % art]}


GESTELLT = {
    FLK_GRUEN: _ergebnis(FLK_GRUEN, "gruen", 0),
    FLK_ROT: _ergebnis(FLK_ROT, "rot", 1),
    BR_GRUEN: _ergebnis(BR_GRUEN, "gruen", 0),
    OHNE_ROT: _ergebnis(OHNE_ROT, "rot", 1),
    OHNE_GRUEN: _ergebnis(OHNE_GRUEN, "gruen", 0),
    UNGEPR: _ergebnis(UNGEPR, "ungeprueft", 1),
    ZEIT: _ergebnis(ZEIT, "zeitgrenze", None),
}


def lauf(modul):
    """`main()` des geladenen Moduls mit gestellten Ergebnissen ausfuehren.

    Rueckgabe: (rc, zeilen der Ausgabe, je_art aus dem JSON oder None).
    """
    for name, inhalt in LISTEN.items():
        setattr(modul, name, dict(inhalt))
    modul.testdateien = lambda wurzel=None: list(DATEIEN)
    modul.fuehre_aus = lambda rel, wurzel, grenze: copy.deepcopy(GESTELLT[rel])

    ordner = tempfile.mkdtemp(prefix="tb51_flackerstufe_")
    ziel = os.path.join(ordner, "lauf.json")
    puffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(puffer):
            rc = modul.main(["--json", ziel])
        je_art = None
        if os.path.exists(ziel):
            with open(ziel, encoding="utf-8") as f:
                je_art = json.load(f).get("je_art")
    finally:
        import shutil
        shutil.rmtree(ordner, ignore_errors=True)
    return rc, puffer.getvalue().splitlines(), je_art


def zeile_fuer(zeilen, rel):
    """Die Ausgabezeile dieser Datei - genau eine."""
    treffer = [z for z in zeilen if rel in z and z.lstrip().startswith("[")]
    return treffer[0] if len(treffer) == 1 else None


def zahlen_unter_dem_strich(zeilen):
    """Die Stufenzahlen nach dem zweiten Trennstrich, wie sie gedruckt sind,
    und die SUMME-Zeile."""
    striche = [i for i, z in enumerate(zeilen) if z.startswith("=" * 20)]
    if len(striche) < 2:
        return {}, None
    zahlen, summe = {}, None
    for z in zeilen[striche[1] + 1:]:
        m = re.match(r"^  (\S+)\s+(\d+)(.*)$", z)
        if not m:
            continue
        if m.group(1) == "SUMME":
            summe = (int(m.group(2)), m.group(3))
        elif m.group(1) == "UNERWARTET":
            break
        else:
            zahlen[m.group(1)] = int(m.group(2))
    return zahlen, summe


# ---------------------------------------------------------------------------
# Die fuenf Proben - jede gibt (bestanden, detail) zurueck
# ---------------------------------------------------------------------------

def probe_1_flackernd_gruen(rc, zeilen, je_art):
    """Eine Datei in FLACKERND, Lauf gruen: nicht UNERWARTET, eigens
    gezaehlt, und die Zeile sagt es."""
    z = zeile_fuer(zeilen, FLK_GRUEN) or ""
    zahlen, _ = zahlen_unter_dem_strich(zeilen)
    gruen_ohne_flackernd = 2                # OHNE_GRUEN und BR_GRUEN
    bedingungen = [
        ("nicht UNERWARTET", "UNERWARTET" not in z),
        ("Zeile nennt 'flackernd (…)'", "flackernd (" in z),
        ("Zeile nennt 'heute gruen'", "heute gruen" in z),
        ("Zeile nennt die Rate", "~30 %" in z),
        ("nicht unter gruen gezaehlt",
         zahlen.get("gruen") == gruen_ohne_flackernd),
        ("eigene Zahl 'flackernd' vorhanden", "flackernd" in zahlen),
        ("JSON zaehlt sie eigens",
         bool(je_art) and je_art.get("flackernd", 0) >= 1),
    ]
    return _auswerten(bedingungen)


def probe_2_flackernd_rot(rc, zeilen, je_art):
    """Dieselbe Liste, Lauf rot: nicht UNERWARTET, eigens gezaehlt."""
    z = zeile_fuer(zeilen, FLK_ROT) or ""
    zahlen, _ = zahlen_unter_dem_strich(zeilen)
    rot_ohne_flackernd = 1                  # OHNE_ROT
    bedingungen = [
        ("nicht UNERWARTET", "UNERWARTET" not in z),
        ("Zeile nennt 'flackernd (…)'", "flackernd (" in z),
        ("Zeile nennt 'heute rot'", "heute rot" in z),
        ("nicht unter rot gezaehlt", zahlen.get("rot") == rot_ohne_flackernd),
        ("eigene Zahl 'flackernd' == 2", zahlen.get("flackernd") == 2),
        ("nicht unter den UNERWARTET-Zeilen",
         not any(FLK_ROT in u for u in zeilen if u.startswith("    - "))),
    ]
    return _auswerten(bedingungen)


def probe_3_bekannt_rot_gruen(rc, zeilen, je_art):
    """Eine Datei in BEKANNT_ROT, Lauf gruen: WEITERHIN UNERWARTET."""
    z = zeile_fuer(zeilen, BR_GRUEN) or ""
    bedingungen = [
        ("UNERWARTET", "UNERWARTET" in z),
        ("Zeile nennt 'bekannt rot'", "bekannt rot" in z),
        ("Zeile sagt 'hier aber GRUEN'", "hier aber GRUEN" in z),
        ("nicht als flackernd eingeordnet", "flackernd (" not in z),
    ]
    return _auswerten(bedingungen)


def probe_4_ohne_liste_rot(rc, zeilen, je_art):
    """Eine Datei in keiner Liste, Lauf rot: WEITERHIN UNERWARTET, und der
    Rueckgabewert ist 1."""
    z = zeile_fuer(zeilen, OHNE_ROT) or ""
    bedingungen = [
        ("UNERWARTET", "UNERWARTET" in z),
        ("nicht als flackernd eingeordnet", "flackernd (" not in z),
        ("Rueckgabewert 1", rc == 1),
        ("steht unter den UNERWARTET-Zeilen",
         any(OHNE_ROT in u for u in zeilen if u.startswith("    - "))),
    ]
    return _auswerten(bedingungen)


def probe_5_summenzeile(rc, zeilen, je_art):
    """gruen + rot + flackernd + ungeprueft + Zeitgrenze = Zahl der Dateien -
    nachgerechnet aus den GEDRUCKTEN Zahlen, nicht aus der SUMME-Zeile."""
    zahlen, summe = zahlen_unter_dem_strich(zeilen)
    stufen = ("gruen", "rot", "flackernd", "ungeprueft", "zeitgrenze")
    bedingungen = [
        ("alle fuenf Stufen gedruckt", all(s in zahlen for s in stufen)),
        ("keine weitere Stufe gedruckt", set(zahlen) <= set(stufen)),
        ("die fuenf Zahlen ergeben %d" % len(DATEIEN),
         sum(zahlen.get(s, 0) for s in stufen) == len(DATEIEN)),
        ("SUMME-Zeile vorhanden", summe is not None),
        ("SUMME nennt %d" % len(DATEIEN),
         summe is not None and summe[0] == len(DATEIEN)),
        ("SUMME ohne 'GEHT NICHT AUF'",
         summe is not None and "GEHT NICHT AUF" not in summe[1]),
        ("Verteilung 2/1/2/1/1",
         [zahlen.get(s) for s in stufen] == [2, 1, 2, 1, 1]),
    ]
    return _auswerten(bedingungen)


def _auswerten(bedingungen):
    gefallen = [name for name, ok in bedingungen if not ok]
    return (not gefallen), ("alle %d Bedingungen" % len(bedingungen)
                            if not gefallen else
                            "gefallen: " + "; ".join(gefallen))


PROBEN = [
    ("1 FLACKERND, heute gruen", probe_1_flackernd_gruen),
    ("2 FLACKERND, heute rot", probe_2_flackernd_rot),
    ("3 BEKANNT_ROT, heute gruen - weiterhin UNERWARTET", probe_3_bekannt_rot_gruen),
    ("4 keine Liste, rot - weiterhin UNERWARTET", probe_4_ohne_liste_rot),
    ("5 Summenzeile geht auf", probe_5_summenzeile),
]

# Die Mutanten - Ankertexte, die GENAU EINMAL im Quelltext stehen muessen.
M1_OHNE_STUFE = ("M1_ohne_stufe", [
    ('elif rel in FLACKERND and e["art"] in ("gruen", "rot"):',
     'elif False:  # MUTATION M1: die Stufe ist abgeschaltet'),
])
M2_ZU_WEIT = ("M2_zu_weit", [
    ('elif rel in FLACKERND and e["art"] in ("gruen", "rot"):',
     'elif e["art"] in ("gruen", "rot"):  # MUTATION M2: faengt alles ab'),
    ('% (FLACKERND[rel], e["heute"]))',
     '% (FLACKERND.get(rel, "?"), e["heute"]))'),
])
M3_SUMME_OHNE = ("M3_summe_ohne_flackernd", [
    ('for art in ("gruen", "rot", "flackernd", "ungeprueft", "zeitgrenze"):',
     'for art in ("gruen", "rot", "ungeprueft", "zeitgrenze"):  # MUTATION M3'),
])

# Welche Mutante muss welche Probe zu Fall bringen - und welche darf sie
# NICHT beruehren (Kontrolle).
BEISST = {
    "1": M1_OHNE_STUFE, "2": M1_OHNE_STUFE,
    "3": M2_ZU_WEIT, "4": M2_ZU_WEIT,
    "5": M3_SUMME_OHNE,
}
UNBERUEHRT = {"3": M1_OHNE_STUFE, "4": M1_OHNE_STUFE}


# ===========================================================================
# 1 - Das Werkzeug, wie es ist
# ===========================================================================

def teil_1_werkzeug():
    print("\n1. DAS WERKZEUG MIT GESTELLTEN ERGEBNISSEN")
    modul = lade_basislauf()
    rc, zeilen, je_art = lauf(modul)
    for name, probe in PROBEN:
        ok, detail = probe(rc, zeilen, je_art)
        check("1.%s" % name, ok, detail)
    z = zeile_fuer(zeilen, FLK_GRUEN) or "(keine Zeile)"
    print("      Zeile der flackernden Datei: %s" % z.strip())
    # ⚠️ Nicht Teil der Stufe, aber ihr Rand: eine flackernde Datei an der
    # Zeitgrenze ist weiterhin UNERWARTET - die Stufe deckt nur gruen/rot.
    modul2 = lade_basislauf()
    alt = GESTELLT[FLK_GRUEN]
    GESTELLT[FLK_GRUEN] = _ergebnis(FLK_GRUEN, "zeitgrenze", None)
    try:
        _, zeilen2, _ = lauf(modul2)
    finally:
        GESTELLT[FLK_GRUEN] = alt
    z2 = zeile_fuer(zeilen2, FLK_GRUEN) or ""
    check("1.6 Rand: FLACKERND an der Zeitgrenze bleibt UNERWARTET",
          "UNERWARTET" in z2 and "flackernd (" not in z2, z2.strip()[:90])


# ===========================================================================
# 2 - Die Mutationsproben: jede Probe muss in ihrer Mutante scheitern
# ===========================================================================

def teil_2_mutationen():
    print("\n2. MUTATIONSPROBEN - jede Probe muss in ihrer Mutante SCHEITERN")
    laeufe = {}
    for kennung, (name, ersetzungen) in list(BEISST.items()) + list(UNBERUEHRT.items()):
        if name not in laeufe:
            laeufe[name] = lauf(mutante(name, ersetzungen))
    for name, probe in PROBEN:
        kennung = name.split()[0]
        mname = BEISST[kennung][0]
        rc, zeilen, je_art = laeufe[mname]
        ok, detail = probe(rc, zeilen, je_art)
        # ⭐ Der Kern: in der Mutante muss die Probe FALLEN.
        check("2.%s beisst in %s" % (kennung, mname), not ok,
              detail if not ok else "⚠️ Probe besteht auch in der Mutante")
    for kennung, (mname, _) in sorted(UNBERUEHRT.items()):
        name, probe = [p for p in PROBEN if p[0].startswith(kennung + " ")][0]
        rc, zeilen, je_art = laeufe[mname]
        ok, detail = probe(rc, zeilen, je_art)
        # Kontrolle: die alten Stufen sind OHNE die neue genauso richtig -
        # genau das behaupten die Proben 3 und 4.
        check("2.%s Kontrolle: besteht unveraendert in %s" % (kennung, mname),
              ok, detail)


# ===========================================================================
# 3 - Die wirkliche Vorgaengerfassung aus git
# ===========================================================================

def teil_3_vorgaenger():
    print("\n3. GEGENPROBE GEGEN DIE VORGAENGERFASSUNG (git show %s)"
          % VORGAENGER_COMMIT)
    modul, fehler = vorgaengerfassung()
    if modul is None:
        check("3.0 Vorgaengerfassung geladen", False, fehler)
        return
    check("3.0 Vorgaengerfassung geladen, ohne FLACKERND", True)
    rc, zeilen, je_art = lauf(modul)
    for kennung in ("1", "2"):
        name, probe = [p for p in PROBEN if p[0].startswith(kennung + " ")][0]
        ok, detail = probe(rc, zeilen, je_art)
        check("3.%s Probe %s scheitert dort" % (kennung, kennung), not ok,
              detail if not ok else "⚠️ besteht auch in der Vorgaengerfassung")
    z = zeile_fuer(zeilen, FLK_ROT) or ""
    check("3.3 dort ist der rote Lauf UNERWARTET - der alte Befund (T50.4)",
          "UNERWARTET" in z, z.strip()[:90])


# ===========================================================================
# 4 - Der Eintrag selbst
# ===========================================================================

def teil_4_eintrag():
    print("\n4. DER EINTRAG IN DER ECHTEN LISTE")
    modul = lade_basislauf()
    liste = getattr(modul, "FLACKERND", None)
    check("4.1 FLACKERND existiert", isinstance(liste, dict))
    if not isinstance(liste, dict):
        return
    rel = "system/test_log_rotation.py"
    wert = liste.get(rel, "")
    check("4.2 test_log_rotation.py steht darin", rel in liste)
    check("4.3 mit Rate", "%" in wert, wert)
    check("4.4 mit Datum", bool(re.search(r"\d{2}\.\d{2}\.\d{4}", wert)))
    check("4.5 mit Herkunft (TB-49)", "TB-49" in wert)
    check("4.6 und in KEINER anderen Liste",
          rel not in modul.BEKANNT_ROT and rel not in modul.UNGEPRUEFT
          and rel not in modul.LAEUFT_WEITER)
    check("4.7 die Datei gibt es wirklich",
          os.path.exists(os.path.join(_WURZEL, rel)))


def main():
    print("=" * 78)
    print("TB-51: die Stufe 'flackernd' im Basislauf - Nachweis mit Mutation")
    print("=" * 78)
    for teil in (teil_1_werkzeug, teil_2_mutationen, teil_3_vorgaenger,
                 teil_4_eintrag):
        try:
            teil()
        except Exception as fehler:                      # noqa: BLE001
            import traceback
            FEHLER.append("%s (Ausnahme)" % teil.__name__)
            print("  [FEHLER] Ausnahme: %s" % fehler)
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
