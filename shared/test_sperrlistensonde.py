#!/usr/bin/env python3
"""
Selbstpruefung der Sperrlisten-Sonde (TB-85, Auftrag B5)
==============================================================================
Jede Pruefung ist eine **Mutationsprobe**: der Sonde wird absichtlich ein
Fehler untergeschoben, und geprueft wird, dass sie ihn mit dem richtigen
Ausgang (36.5) UND mit Nennung des Punktes meldet. Eine Sonde, die alles
gruen meldet, waere hier rot.

⚠️⚠️ Alles laeuft auf KOPIEN in einem Wegwerf-Ordner - nie gegen die echten
gesperrten Dateien. Das Register und die zehn im Abschnitt 10 genannten
Dateien werden dorthin kopiert; das Abbild wird dort erzeugt; mutiert wird
nur dort. Der Ordner wird am Ende entfernt.

Die sieben Faelle des Auftrags (B5)                              erwartet
------------------------------------------------------------------------------
  1  Abbild stimmt mit Repo und Registertext                       2 (nicht-
     (kein Punkt mit 1; Punkte 2 und 5 sind 0)                       pruefbare
                                                                     Punkte)
  2  Eine Datei im Repo veraendert (Kopie, ein Byte anders)        1, Punkt
                                                                     genannt
  3  Ein Punkt fehlt im Abbild                                     1
  4  Ein Punkt zu viel im Abbild                                   1
  5  Abbilddatei fehlt                                             2
  6  Registerdatei nicht lesbar                                    2
  7  Ein Punkt ohne Pfade (13)                                     2, genannt

Dazu (Teil H): 1 schlaegt 2; Titel im Abbild veraendert; Registertext mit
einem 15. Punkt; eine im Abbild genannte Datei fehlt (2, nicht 0); der
Erzeuger schreibt nur einmal (1, Hash genannt); die Befehlszeile liefert
denselben Wert wie die Funktion; die Sonde schreibt nichts.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_HIER)
sys.path.insert(0, _HIER)
sys.path.insert(0, os.path.join(BASE_DIR, "research", "vorregistrierung"))

import sperrlistensonde as sonde     # noqa: E402
import sperrliste_abbild as erzeuger  # noqa: E402

bestanden = 0
gescheitert = []


def pruefe(name, bedingung, zusatz=""):
    """Eine Mutationsprobe. Jede Probe druckt ihr Ergebnis sofort - der Beleg
    soll jede einzelne Probe zeigen, nicht nur die gescheiterten."""
    global bestanden
    if bedingung:
        bestanden += 1
        print("  [ OK ] %s" % name)
    else:
        gescheitert.append("%s%s" % (name, (" - " + str(zusatz)[:200]) if zusatz else ""))
        print("  [FEHL] %s%s" % (name, (" - " + str(zusatz)[:200]) if zusatz else ""))


# ---------------------------------------------------------------------------
# Die Kopie
# ---------------------------------------------------------------------------

def _kopiere(rel, wurzel):
    quelle = os.path.join(BASE_DIR, rel)
    ziel = os.path.join(wurzel, rel)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    shutil.copy2(quelle, ziel)


def baue_kopie():
    """Register + alle in Abschnitt 10 genannten Dateien in einen Wegwerf-Ordner."""
    wurzel = tempfile.mkdtemp(prefix="tb85_sonde_")
    assert os.path.realpath(wurzel) != os.path.realpath(BASE_DIR)
    _kopiere(sonde.REGISTER, wurzel)
    punkte, _, _ = sonde.lies_abschnitt_10(os.path.join(BASE_DIR, sonde.REGISTER))
    for p in punkte:
        for rel in p["pfade"]:
            _kopiere(rel, wurzel)
    for rel, _ in sonde.BESTIMMT_NICHT_EINGETRAGEN:
        if os.path.isfile(os.path.join(BASE_DIR, rel)):
            _kopiere(rel, wurzel)
    return wurzel


def _register(wurzel):
    return os.path.join(wurzel, sonde.REGISTER)


def _lade(pfad):
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def _schreibe(pfad, inhalt):
    with open(pfad, "w", encoding="utf-8") as f:
        json.dump(inhalt, f, indent=2, ensure_ascii=False, sort_keys=True)


def _punkt(bericht, nummer):
    return next(p for p in bericht["punkte"] if p["punkt"] == nummer)


# ---------------------------------------------------------------------------
# Die Faelle
# ---------------------------------------------------------------------------

def fall_1(wurzel, abbild):
    """Abbild stimmt mit Repo und Registertext -> 2 (nicht-pruefbare Punkte dabei)."""
    b = sonde.pruefen(abbild, _register(wurzel), wurzel)
    pruefe("1a: unveraendert -> Gesamtwert 2 (nicht-pruefbare Punkte dabei)",
           b["ausgang"] == 2, b["grund"])
    pruefe("1b: kein Punkt mit 1",
           all(p["ausgang"] != 1 for p in b["punkte"]))
    pruefe("1c: Punkte 2 und 5 (nur Dateien) sind 0",
           _punkt(b, 2)["ausgang"] == 0 and _punkt(b, 5)["ausgang"] == 0)
    pruefe("1d: (ii) Abbild = Registertext",
           b["ii"]["ausgang"] == 0 and b["ii"]["befunde"] == [])
    pruefe("1e: 14 Punkte im Bericht", len(b["punkte"]) == 14)
    pruefe("1f: jeder 2er-Punkt nennt seinen Grund",
           all(p["gruende"] for p in b["punkte"] if p["ausgang"] == 2))
    pruefe("1g: jede gemessene Datei steht mit Hash und 'gleich' im Bericht",
           all(d["stand"] == "gleich" and d["sha256"]
               for p in b["punkte"] for d in p["dateien"]))


def fall_2(wurzel, abbild):
    """Eine Datei der Kopie um ein Byte veraendert -> 1, Punkt genannt."""
    rel = _punkt(_lade_abbild_punkte(abbild), 1)["pfade"][0]
    voll = os.path.join(wurzel, rel)
    with open(voll, "rb") as f:
        original = f.read()
    try:
        with open(voll, "ab") as f:
            f.write(b"\n")
        b = sonde.pruefen(abbild, _register(wurzel), wurzel)
        pruefe("2a: ein Byte anders -> Gesamtwert 1", b["ausgang"] == 1, b["grund"])
        pruefe("2b: Punkt 1 traegt den Befund", _punkt(b, 1)["ausgang"] == 1)
        pruefe("2c: der Grund nennt die Datei",
               any(rel in g for g in _punkt(b, 1)["gruende"]), _punkt(b, 1)["gruende"])
        pruefe("2d: der Gesamtgrund nennt den Punkt", "[1]" in b["grund"], b["grund"])
        pruefe("2e: die uebrigen Punkte sind unveraendert (kein zweiter 1er)",
               sum(1 for p in b["punkte"] if p["ausgang"] == 1) == 1)
    finally:
        with open(voll, "wb") as f:
            f.write(original)
    b = sonde.pruefen(abbild, _register(wurzel), wurzel)
    pruefe("2f: zurueckgesetzt -> wieder 2, kein 1er",
           b["ausgang"] == 2 and all(p["ausgang"] != 1 for p in b["punkte"]))


def _lade_abbild_punkte(abbild):
    return {"punkte": _lade(abbild)["punkte"]}


def fall_3(wurzel, abbild):
    """Ein Punkt fehlt im Abbild -> 1 (ii)."""
    mut = os.path.join(wurzel, "abbild_ohne_punkt7.json")
    a = _lade(abbild)
    a["punkte"] = [p for p in a["punkte"] if p["punkt"] != 7]
    _schreibe(mut, a)
    b = sonde.pruefen(mut, _register(wurzel), wurzel)
    pruefe("3a: Punkt fehlt -> 1", b["ausgang"] == 1, b["grund"])
    pruefe("3b: (ii) nennt die Punktzahl 13 gegen 14",
           any("Punktzahl" in f and "13" in f and "14" in f for f in b["ii"]["befunde"]),
           b["ii"]["befunde"])


def fall_4(wurzel, abbild):
    """Ein Punkt zu viel im Abbild -> 1 (ii)."""
    mut = os.path.join(wurzel, "abbild_punkt15.json")
    a = _lade(abbild)
    a["punkte"].append({"punkt": 15, "titel": "Erfunden", "pfade": [], "hashes": {},
                        "nicht_dateibezogen": "nichts", "quelle": "Registerabschnitt 10, Punkt 15"})
    _schreibe(mut, a)
    b = sonde.pruefen(mut, _register(wurzel), wurzel)
    pruefe("4a: Punkt zu viel -> 1", b["ausgang"] == 1, b["grund"])
    pruefe("4b: (ii) nennt die Punktzahl 15 gegen 14",
           any("Punktzahl" in f and "15" in f for f in b["ii"]["befunde"]), b["ii"]["befunde"])
    pruefe("4c: ein 1 aus (ii) schlaegt die 2 des erfundenen Punktes",
           _punkt(b, 15)["ausgang"] == 2 and b["ausgang"] == 1)


def fall_5(wurzel, abbild):
    """Abbilddatei fehlt -> 2."""
    b = sonde.pruefen(os.path.join(wurzel, "gibt_es_nicht.json"), _register(wurzel), wurzel)
    pruefe("5a: Abbild fehlt -> 2", b["ausgang"] == 2, b["grund"])
    pruefe("5b: der Grund sagt es", "nicht lesbar" in (b["grund"] or ""), b["grund"])
    pruefe("5c: kein Punkt wurde als geprueft gefuehrt", b["punkte"] == [])
    kaputt = os.path.join(wurzel, "kaputt.json")
    with open(kaputt, "w") as f:
        f.write("{ kein json")
    b = sonde.pruefen(kaputt, _register(wurzel), wurzel)
    pruefe("5d: Abbild kein JSON -> 2", b["ausgang"] == 2, b["grund"])


def fall_6(wurzel, abbild):
    """Registerdatei nicht lesbar -> 2 - und ein Befund in (i) schlaegt das trotzdem."""
    b = sonde.pruefen(abbild, os.path.join(wurzel, "kein_register.md"), wurzel)
    pruefe("6a: Register fehlt -> 2", b["ausgang"] == 2, b["grund"])
    pruefe("6b: (ii) ist 2 und nennt das Register",
           b["ii"]["ausgang"] == 2 and any("nicht lesbar" in f for f in b["ii"]["befunde"]),
           b["ii"]["befunde"])
    pruefe("6c: (i) wurde trotzdem gemessen (14 Punkte im Bericht)", len(b["punkte"]) == 14)

    if os.geteuid() != 0:
        reg = _register(wurzel)
        alt = stat.S_IMODE(os.stat(reg).st_mode)
        try:
            os.chmod(reg, 0)
            b = sonde.pruefen(abbild, reg, wurzel)
            pruefe("6d: Register ohne Leserecht -> 2", b["ausgang"] == 2, b["grund"])
        finally:
            os.chmod(reg, alt)

    # Register mit einem 15. Punkt: Registertext weicht vom Abbild ab -> 1
    reg15 = os.path.join(wurzel, "register_15.md")
    with open(_register(wurzel), encoding="utf-8") as f:
        text = f.read()
    anker = "14. **Die Reihenfolge Selektion"
    pos = text.index(anker)
    ende = text.index("\n\n", pos)
    text = text[:ende] + "\n15. **Ein fuenfzehnter Punkt** — `registerdaten.py`" + text[ende:]
    with open(reg15, "w", encoding="utf-8") as f:
        f.write(text)
    b = sonde.pruefen(abbild, reg15, wurzel)
    pruefe("6e: Registertext mit 15. Punkt -> 1", b["ausgang"] == 1, b["grund"])
    pruefe("6f: (ii) nennt 14 gegen 15",
           any("Punktzahl" in f and "15" in f for f in b["ii"]["befunde"]), b["ii"]["befunde"])


def fall_7(wurzel, abbild):
    """Ein Punkt ohne Pfade (13) -> 2, mit Nennung."""
    b = sonde.pruefen(abbild, _register(wurzel), wurzel)
    p13 = _punkt(b, 13)
    pruefe("7a: Punkt 13 hat im Abbild keine Pfade",
           _punkt(_lade_abbild_punkte(abbild), 13)["pfade"] == [])
    pruefe("7b: Punkt 13 -> 2", p13["ausgang"] == 2)
    pruefe("7c: der Grund nennt 'kein Dateipfad' und den Wortlaut 'Abschnitt 8'",
           any("kein Dateipfad" in g and "Abschnitt 8" in g for g in p13["gruende"]), p13["gruende"])
    pruefe("7d: der Gesamtgrund nennt Punkt 13", "13" in b["grund"], b["grund"])
    pruefe("7e: Punkte 7 und 9 (nur Konstanten) ebenso 2",
           _punkt(b, 7)["ausgang"] == 2 and _punkt(b, 9)["ausgang"] == 2)


def teil_h(wurzel, abbild):
    """Weitere Mutationsproben ueber die sieben Faelle hinaus."""
    # H1: 1 schlaegt 2 - Datei veraendert UND nicht-pruefbare Punkte
    rel = "config/top25_symbols.txt"
    voll = os.path.join(wurzel, rel)
    with open(voll, "rb") as f:
        original = f.read()
    try:
        with open(voll, "wb") as f:
            f.write(original[:-1] if original else b"x")
        b = sonde.pruefen(abbild, _register(wurzel), wurzel)
        pruefe("H1: 1 schlaegt 2 - Gesamt 1 bei 12 nicht-pruefbaren Punkten",
               b["ausgang"] == 1 and _punkt(b, 8)["ausgang"] == 1, b["grund"])
    finally:
        with open(voll, "wb") as f:
            f.write(original)

    # H2: Titel im Abbild veraendert -> 1, Feld genannt
    mut = os.path.join(wurzel, "abbild_titel.json")
    a = _lade(abbild)
    a["punkte"][4]["titel"] = "Abbruchkriterien und Kapitalregel (geaendert)"
    _schreibe(mut, a)
    b = sonde.pruefen(mut, _register(wurzel), wurzel)
    pruefe("H2: Titel veraendert -> 1 mit 'Feld titel'",
           b["ausgang"] == 1 and any("Punkt 5, Feld titel" in f for f in b["ii"]["befunde"]),
           b["ii"]["befunde"])

    # H3: Pfad im Abbild veraendert (Datei existiert, Hash im Abbild stimmt) -> 1 aus (ii)
    mut = os.path.join(wurzel, "abbild_pfad.json")
    a = _lade(abbild)
    p2 = a["punkte"][1]
    alt = p2["pfade"][0]
    p2["pfade"] = [alt, "config/sp500_top150.txt"]
    p2["hashes"]["config/sp500_top150.txt"] = sonde.sha256_datei(
        os.path.join(wurzel, "config/sp500_top150.txt"))
    _schreibe(mut, a)
    b = sonde.pruefen(mut, _register(wurzel), wurzel)
    pruefe("H3: zusaetzlicher Pfad im Abbild -> 1 aus (ii), obwohl (i) gleich",
           b["ausgang"] == 1 and _punkt(b, 2)["ausgang"] == 0
           and any("Feld pfade" in f for f in b["ii"]["befunde"]), b["ii"]["befunde"])

    # H4: eine im Abbild genannte Datei fehlt -> 2 (Datei fehlt), nie 0
    fehl = os.path.join(wurzel, "shared", "zuteilung.py")
    os.rename(fehl, fehl + ".weg")
    try:
        b = sonde.pruefen(abbild, _register(wurzel), wurzel)
        p10 = _punkt(b, 10)
        pruefe("H4: genannte Datei fehlt -> Punkt 2 mit 'Datei fehlt'",
               p10["ausgang"] == 2 and any("Datei fehlt" in g for g in p10["gruende"]),
               p10["gruende"])
    finally:
        os.rename(fehl + ".weg", fehl)

    # H5: Hash im Abbild verfaelscht -> 1 (die Datei ist unveraendert, das Abbild luegt)
    mut = os.path.join(wurzel, "abbild_hash.json")
    a = _lade(abbild)
    p5 = a["punkte"][4]
    p5["hashes"][p5["pfade"][0]] = "0" * 64
    _schreibe(mut, a)
    b = sonde.pruefen(mut, _register(wurzel), wurzel)
    pruefe("H5: falscher Hash im Abbild -> 1, Punkt 5",
           b["ausgang"] == 1 and _punkt(b, 5)["ausgang"] == 1, b["grund"])

    # H6: der Erzeuger schreibt nur einmal - zweiter Aufruf 1 mit Hash
    h_vorher = sonde.sha256_datei(abbild)
    rc, text = erzeuger.erzeugen(abbild, _register(wurzel), wurzel)
    pruefe("H6a: zweiter Aufruf des Erzeugers -> 1", rc == 1, text)
    pruefe("H6b: er nennt Pfad und Hash der vorhandenen Datei",
           abbild in text and h_vorher in text, text)
    pruefe("H6c: die Datei ist unveraendert", sonde.sha256_datei(abbild) == h_vorher)
    rc, text = erzeuger.erzeugen(os.path.join(wurzel, "neu.json"),
                                 os.path.join(wurzel, "kein_register.md"), wurzel)
    pruefe("H6d: Erzeuger ohne lesbares Register -> 2, nichts geschrieben",
           rc == 2 and not os.path.exists(os.path.join(wurzel, "neu.json")), text)

    # H7: Befehlszeile = Funktion, --json ist lesbar
    cmd = [sys.executable, os.path.join(_HIER, "sperrlistensonde.py"),
           "--abbild", abbild, "--register", _register(wurzel), "--wurzel", wurzel]
    r = subprocess.run(cmd, capture_output=True, text=True)
    pruefe("H7a: Befehlszeile liefert 2 wie die Funktion", r.returncode == 2, r.stderr[:200])
    pruefe("H7b: die Textausgabe endet mit dem Rueckgabewert",
           "RUECKGABEWERT 2 NICHT PRUEFBAR" in r.stdout, r.stdout[-200:])
    pruefe("H7c: die Textausgabe nennt benchmark_drawdowns_vt.json als 'bestimmt, nicht eingetragen'",
           "Bestimmt, nicht eingetragen" in r.stdout and "benchmark_drawdowns_vt.json" in r.stdout)
    r = subprocess.run(cmd + ["--json"], capture_output=True, text=True)
    try:
        j = json.loads(r.stdout)
        ok = j["ausgang"] == 2 and len(j["punkte"]) == 14
    except ValueError:
        ok = False
    pruefe("H7d: --json ist gueltiges JSON mit ausgang 2", ok, r.stdout[:200])
    r = subprocess.run(cmd[:2] + ["--abbild", os.path.join(wurzel, "fehlt.json")],
                       capture_output=True, text=True)
    pruefe("H7e: fehlendes Abbild ueber die Befehlszeile -> 2", r.returncode == 2)

    # H8: die Sonde schreibt nichts
    def _stand():
        return sorted((os.path.relpath(os.path.join(d, f), wurzel), os.path.getsize(os.path.join(d, f)))
                      for d, _, fs in os.walk(wurzel) for f in fs)
    vorher = _stand()
    sonde.pruefen(abbild, _register(wurzel), wurzel)
    pruefe("H8: die Sonde schreibt nichts (Dateiliste und Groessen gleich)", _stand() == vorher)


# ---------------------------------------------------------------------------

def main():
    print(__doc__.strip().split("\n")[0])
    wurzel = baue_kopie()
    print("Kopie unter %s" % wurzel)
    try:
        print("\nfall_0  Der Erzeuger legt das Abbild in der Kopie an.")
        abbild = os.path.join(wurzel, "sperrliste_abbild_probe.json")
        rc, text = erzeuger.erzeugen(abbild, _register(wurzel), wurzel)
        pruefe("0: der Erzeuger schreibt das Abbild in die Kopie (rc 0)", rc == 0, text)
        if rc != 0:
            raise SystemExit(text)
        for fall in (fall_1, fall_2, fall_3, fall_4, fall_5, fall_6, fall_7, teil_h):
            print("\n%s  %s" % (fall.__name__, (fall.__doc__ or "").strip().split("\n")[0]))
            fall(wurzel, abbild)
    finally:
        shutil.rmtree(wurzel, ignore_errors=True)
    print("\n" + "=" * 78)
    if gescheitert:
        print("%d bestanden, %d GESCHEITERT:" % (bestanden, len(gescheitert)))
        for g in gescheitert:
            print("  - %s" % g)
        return 1
    print("%d/%d Pruefungen bestanden." % (bestanden, bestanden))
    return 0


if __name__ == "__main__":
    sys.exit(main())
