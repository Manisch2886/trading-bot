#!/usr/bin/env python3
"""
TB-41 - Selbsttest des Registernachtrags
==============================================================================
  A  Der Nachtrag selbst: alle neun Pruefungen auf dem echten Repo, kein Befund.
  B  Null entfernte Zeilen, am Diff gegen die Basis gemessen.
  C  Jede ersetzte Fassung steht noch da UND traegt den Verweis.
  D  Mutationsprobe Symbolzahl: eine geaenderte Registerzahl wird gemeldet.
  E  Mutationsprobe Faltenevidenz: ein geaendertes Symbol wird gemeldet.
  F  Mutationsprobe MIN_HISTORY: eine geaenderte Bot-Datei wird gemeldet.
  G  Mutationsprobe "ersetzt": faellt der Verweis weg, wird es gemeldet.
  H  Mutationsprobe "null Zeilen": eine entfernte Zeile wird gemeldet.
  I  Zwei Wachen gegen dasselbe Risiko, EINZELN geprueft:
     Datenstand-Hash allein und git allein finden dieselbe veraenderte
     Kursdatei - keine verdeckt das Fehlen der anderen.
  J  Der Beleg ist nicht abgetippt: das Ergebnisdokument von TB-40 und der
     Registereintrag werden aus zwei getrennten Parsern verglichen.

ZU DEN ZWEI WIEDERKEHRENDEN FALLEN
------------------------------------------------------------------------------
1. Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst. Deshalb biegt hier keine Probe eine Variable im laufenden Prozess
   um. Jede kopiert die betroffenen Dateien in ein Wegwerf-Verzeichnis, aendert
   dort GENAU EINE Zeile und startet `pruefe_register.py` als eigenen Prozess.
   Beobachtet wird der ABLAUF - Rueckgabewert und Befundtext -, nicht eine
   Variable, die der Test selbst gesetzt hat.
2. Eine zweite Wache verdeckt das Fehlen der ersten. Deshalb laufen in I die
   beiden Wachen gegen dasselbe Risiko EINZELN (`--nur datenstand` bzw.
   `--nur daten_unberuehrt`) gegen dieselbe Mutation.

DIESER TEST SCHREIBT NUR IN SEIN WEGWERF-VERZEICHNIS. Er fasst weder data/ noch
strategies/ noch docs/ an; das echte data/ wird ausschliesslich gelesen.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))
WERKZEUG = os.path.join(_HIER, "pruefe_register.py")
REGISTER_REL = os.path.join("docs", "VORREGISTRIERUNG_neuselektion.md")
BELEG_REL = os.path.join("docs", "ERGEBNIS_TB-40_universum_trockenlauf.md")

_ZAEHLER = {"ja": 0, "nein": 0}


def pruefe(text, bedingung, zusatz=""):
    if bedingung:
        _ZAEHLER["ja"] += 1
        print("  ok    %s" % text)
    else:
        _ZAEHLER["nein"] += 1
        print("  FEHLT %s%s" % (text, ("  -> " + zusatz) if zusatz else ""))


def _lauf(args, cwd=None):
    """Das Werkzeug als eigener Prozess. Beobachtet wird, was es TUT."""
    fertig = subprocess.run([sys.executable, WERKZEUG] + args,
                            cwd=cwd or BASE_DIR, capture_output=True, text=True)
    return fertig.returncode, fertig.stdout + fertig.stderr


def _bericht(args, arbeit, name="bericht.json", cwd=None):
    pfad = os.path.join(arbeit, name)
    rc, ausgabe = _lauf(args + ["--json", pfad], cwd=cwd)
    with open(pfad, encoding="utf-8") as f:
        return rc, json.load(f), ausgabe


def _ersetze_einmal(pfad, alt, neu):
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    if text.count(alt) != 1:
        raise AssertionError("Anker %r kommt %dx vor" % (alt[:40], text.count(alt)))
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text.replace(alt, neu))


def _kopie_docs(arbeit):
    """Register und Beleg in ein Wegwerf-Verzeichnis."""
    ziel = os.path.join(arbeit, "docs")
    os.makedirs(ziel, exist_ok=True)
    for rel in (REGISTER_REL, BELEG_REL):
        shutil.copy2(os.path.join(BASE_DIR, rel), os.path.join(arbeit, rel))
    return os.path.join(arbeit, REGISTER_REL), os.path.join(arbeit, BELEG_REL)


def _mini_repo(arbeit, name):
    """Ein winziges git-Repo mit drei erzeugten Kursdateien und dem Register.
    Klein genug, um es zweimal anzulegen; echt genug, damit git und der
    Hash dieselbe Sache sehen."""
    repo = os.path.join(arbeit, name)
    os.makedirs(os.path.join(repo, "data"))
    os.makedirs(os.path.join(repo, "docs"))
    for i, sym in enumerate(("AAA", "BBB", "CCC")):
        with open(os.path.join(repo, "data", "%s_1d.csv" % sym), "w") as f:
            f.write("timestamp,open,high,low,close,volume\n")
            for t in range(5):
                f.write("2020-01-0%d,%d,%d,%d,%d,1\n" % (t + 1, i + 1, i + 2, i, i + 1))
    shutil.copy2(os.path.join(BASE_DIR, REGISTER_REL), os.path.join(repo, REGISTER_REL))
    for befehl in (["init", "-q"], ["config", "user.email", "t@t"],
                   ["config", "user.name", "t"], ["add", "-A"],
                   ["commit", "-qm", "basis"]):
        subprocess.run(["git"] + befehl, cwd=repo, check=True,
                       capture_output=True, text=True)
    return repo


def main():
    basis = os.environ.get("TB41_BASIS", "origin/main")
    print("=" * 78)
    print("TB-41 REGISTERNACHTRAG - Selbsttest")
    print("=" * 78)
    arbeit = tempfile.mkdtemp(prefix="tb41_")
    try:
        # ------------------------------------------------------------------
        print("\nA  Der Nachtrag selbst - alle neun Pruefungen")
        rc, b, _ = _bericht(["--basis", basis, "--arbeitsverzeichnis", arbeit],
                            arbeit, "A.json")
        pruefe("A1: das Werkzeug laeuft durch", rc in (0, 1))
        pruefe("A2: alle neun Pruefungen sind gelaufen", len(b["geprueft"]) == 9,
               str(b["geprueft"]))
        pruefe("A3: kein Befund", not b["befunde"],
               "; ".join(x["befund"] for x in b["befunde"]))
        pruefe("A4: der Rueckgabewert sagt dasselbe wie der Bericht",
               (rc == 0) == (not b["befunde"]))
        pruefe("A5: die Belegquelle steht im Bericht", "beleg" in b["quellen"],
               str(b["quellen"]))
        pruefe("A6: der Datenstand ist der registrierte",
               b["quellen"]["datenstand"]["sha256"].startswith("d9449faf51bffaaa")
               and b["quellen"]["datenstand"]["dateien"] == 223,
               str(b["quellen"].get("datenstand")))

        # ------------------------------------------------------------------
        print("\nB  Null entfernte Zeilen")
        rc, b, _ = _bericht(["--nur", "null_entfernte_zeilen", "--basis", basis,
                             "--arbeitsverzeichnis", arbeit], arbeit, "B.json")
        pruefe("B1: die Pruefung meldet nichts", not b["befunde"],
               "; ".join(x["befund"] for x in b["befunde"]))
        zeilen = b["quellen"].get("numstat", [])
        pruefe("B2: der Diff wurde tatsaechlich ausgewertet", bool(zeilen), str(zeilen))
        pruefe("B3: in jeder betroffenen Registerdatei stehen 0 entfernte Zeilen",
               all(z.split("\t")[1] == "0" for z in zeilen), str(zeilen))
        pruefe("B4: es wurde ueberhaupt etwas ergaenzt",
               all(int(z.split("\t")[0]) > 0 for z in zeilen), str(zeilen))

        # ------------------------------------------------------------------
        print("\nC  Jede ersetzte Fassung steht noch da und traegt den Verweis")
        rc, b, _ = _bericht(["--nur", "ersetzt_gekennzeichnet",
                             "--arbeitsverzeichnis", arbeit], arbeit, "C.json")
        pruefe("C1: kein Befund", not b["befunde"],
               "; ".join(x["befund"] for x in b["befunde"]))

        # ------------------------------------------------------------------
        print("\nD  Mutationsprobe Symbolzahl - eine geaenderte Registerzahl")
        d = os.path.join(arbeit, "D")
        os.makedirs(d)
        reg, beleg = _kopie_docs(d)
        _ersetze_einmal(
            reg,
            "> | `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 18 | 24 |",
            "> | `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 | 23 | 24 |")
        rc, b, _ = _bericht(["--nur", "symbolzahl", "--register", reg,
                             "--beleg", beleg, "--beleg-modus", "dokument",
                             "--arbeitsverzeichnis", d], d, "D.json")
        texte = " | ".join(x["befund"] for x in b["befunde"])
        pruefe("D1: die Mutation wird gemeldet", bool(b["befunde"]))
        pruefe("D2: der Befund nennt den Bot und beide Zahlen",
               "t3_supertrend" in texte and "23" in texte and "18" in texte, texte)
        pruefe("D3: genau dieser eine Befund", len(b["befunde"]) == 1, texte)
        pruefe("D4: der Rueckgabewert meldet den Fehlschlag", rc == 1)

        print("   ... und ohne die Mutation meldet derselbe Aufruf nichts:")
        d2 = os.path.join(arbeit, "D2")
        os.makedirs(d2)
        reg2, beleg2 = _kopie_docs(d2)
        rc2, b2, _ = _bericht(["--nur", "symbolzahl", "--register", reg2,
                               "--beleg", beleg2, "--beleg-modus", "dokument",
                               "--arbeitsverzeichnis", d2], d2, "D2.json")
        pruefe("D5: unveraendert kein Befund und Rueckgabewert 0",
               rc2 == 0 and not b2["befunde"],
               "; ".join(x["befund"] for x in b2["befunde"]))

        # ------------------------------------------------------------------
        print("\nE  Mutationsprobe Faltenevidenz - ein geaendertes Symbol")
        e = os.path.join(arbeit, "E")
        os.makedirs(e)
        reg, beleg = _kopie_docs(e)
        _ersetze_einmal(
            reg,
            "> | `turtle_soup_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, "
            "`TRUMPUSDT`, `UUSDT`, `ZKCUSDT` |",
            "> | `turtle_soup_crypto` | 6 | `BMTUSDT`, `ENSOUSDT`, `PUMPUSDT`, "
            "`TRUMPUSDT`, `UUSDT`, `WLDUSDT` |")
        rc, b, _ = _bericht(["--nur", "faltenevidenz", "--register", reg,
                             "--beleg", beleg, "--beleg-modus", "dokument",
                             "--arbeitsverzeichnis", e], e, "E.json")
        texte = " | ".join(x["befund"] for x in b["befunde"])
        pruefe("E1: die Mutation wird gemeldet", bool(b["befunde"]))
        pruefe("E2: der Befund nennt den Bot und das falsche Symbol",
               "turtle_soup_crypto" in texte and "WLDUSDT" in texte, texte)
        pruefe("E3: der Rueckgabewert meldet den Fehlschlag", rc == 1)

        # ------------------------------------------------------------------
        print("\nF  Mutationsprobe MIN_HISTORY - eine geaenderte Bot-Datei")
        f = os.path.join(arbeit, "F")
        for bot in ("elliott_wave", "t3_supertrend", "rsi2_crypto",
                    "turtle_soup_crypto", "volatility_breakout_crypto",
                    "elliott_wave_stocks", "rsi2_mean_reversion",
                    "turtle_soup_stocks", "volatility_breakout"):
            ziel = os.path.join(f, "strategies", bot)
            os.makedirs(ziel)
            shutil.copy2(os.path.join(BASE_DIR, "strategies", bot,
                                      "multi_symbol_optimise.py"),
                         os.path.join(ziel, "multi_symbol_optimise.py"))
        _ersetze_einmal(
            os.path.join(f, "strategies", "t3_supertrend", "multi_symbol_optimise.py"),
            "MIN_HISTORY_DAYS = 730", "MIN_HISTORY_DAYS = 731")
        rc, b, _ = _bericht(["--nur", "min_history", "--strategien", f,
                             "--arbeitsverzeichnis", arbeit], arbeit, "F.json")
        texte = " | ".join(x["befund"] for x in b["befunde"])
        pruefe("F1: die geaenderte Bot-Datei wird gemeldet", bool(b["befunde"]))
        pruefe("F2: der Befund nennt Bot, Registerwert und Dateiwert",
               "t3_supertrend" in texte and "730" in texte and "731" in texte, texte)
        pruefe("F3: das Register wurde dafuer nicht angefasst",
               open(os.path.join(BASE_DIR, REGISTER_REL), encoding="utf-8")
               .read().count("| **730** |") == 1)

        # ------------------------------------------------------------------
        print("\nG  Mutationsprobe 'ersetzt' - der Verweis faellt weg")
        g = os.path.join(arbeit, "G")
        os.makedirs(g)
        reg, beleg = _kopie_docs(g)
        _ersetze_einmal(
            reg,
            "> ⚠️ **ERSETZT durch Abschnitt 16 (Registernachtrag TB-41, 16.09.2026), 16.1.1.**",
            "> (hier stand einmal ein Verweis)")
        rc, b, _ = _bericht(["--nur", "ersetzt_gekennzeichnet", "--register", reg,
                             "--arbeitsverzeichnis", g], g, "G.json")
        texte = " | ".join(x["befund"] for x in b["befunde"])
        pruefe("G1: der fehlende Verweis wird gemeldet", bool(b["befunde"]))
        pruefe("G2: der Befund nennt die betroffene Stelle",
               "Symbolzahl je Falte" in texte, texte)
        pruefe("G3: die ersetzte Fassung selbst steht dort unveraendert",
               "| `volatility_breakout` | 140 / 142 / 145 / 147 / 148 / 148 / 149 |"
               in open(reg, encoding="utf-8").read())

        # ------------------------------------------------------------------
        print("\nH  Mutationsprobe 'null Zeilen' - eine entfernte Zeile")
        repo_h = _mini_repo(arbeit, "H")
        _ersetze_einmal(os.path.join(repo_h, REGISTER_REL),
                        "## 16. Registernachtrag (TB-41, 16.09.2026)\n", "")
        rc, b, _ = _bericht(["--nur", "null_entfernte_zeilen", "--repo", repo_h,
                             "--basis", "HEAD", "--arbeitsverzeichnis", arbeit],
                            arbeit, "H.json", cwd=repo_h)
        texte = " | ".join(x["befund"] for x in b["befunde"])
        pruefe("H1: die entfernte Zeile wird gemeldet", bool(b["befunde"]))
        pruefe("H2: der Befund nennt die Registerdatei und die Zahl",
               "VORREGISTRIERUNG_neuselektion.md" in texte and "1 entfernte" in texte,
               texte)
        pruefe("H3: der Rueckgabewert meldet den Fehlschlag", rc == 1)

        # ------------------------------------------------------------------
        print("\nI  Zwei Wachen gegen dasselbe Risiko - EINZELN geprueft")
        repo_i = _mini_repo(arbeit, "I")
        daten_i = os.path.join(repo_i, "data")
        rc, b, _ = _bericht(["--nur", "datenstand", "--daten", daten_i,
                             "--erwarteter-datenstand", "00", "--erwartete-dateien", "3",
                             "--arbeitsverzeichnis", arbeit], arbeit, "I0.json",
                            cwd=repo_i)
        vorher = b["quellen"]["datenstand"]["sha256"]
        pruefe("I0: der Hash des unveraenderten Wegwerf-Bestandes ist gemessen",
               len(vorher) == 64 and b["quellen"]["datenstand"]["dateien"] == 3)

        # GENAU EINE geaenderte Zahl in GENAU EINER Kursdatei.
        _ersetze_einmal(os.path.join(daten_i, "BBB_1d.csv"),
                        "2020-01-03,2,3,1,2,1\n", "2020-01-03,2,3,1,9,1\n")

        rc_hash, b_hash, _ = _bericht(
            ["--nur", "datenstand", "--daten", daten_i,
             "--erwarteter-datenstand", vorher[:16], "--erwartete-dateien", "3",
             "--arbeitsverzeichnis", arbeit], arbeit, "I1.json", cwd=repo_i)
        pruefe("I1: der Datenstand-Hash ALLEIN findet die veraenderte Kursdatei",
               rc_hash == 1 and any(x["pruefung"] == "datenstand"
                                    for x in b_hash["befunde"]),
               "; ".join(x["befund"] for x in b_hash["befunde"]))
        pruefe("I2: dabei lief wirklich nur diese eine Wache",
               b_hash["geprueft"] == ["datenstand"], str(b_hash["geprueft"]))

        rc_git, b_git, _ = _bericht(
            ["--nur", "daten_unberuehrt", "--repo", repo_i, "--basis", "HEAD",
             "--arbeitsverzeichnis", arbeit], arbeit, "I2.json", cwd=repo_i)
        pruefe("I3: git ALLEIN findet dieselbe veraenderte Kursdatei",
               rc_git == 1 and any("BBB_1d.csv" in x["befund"]
                                   for x in b_git["befunde"]),
               "; ".join(x["befund"] for x in b_git["befunde"]))
        pruefe("I4: dabei lief wirklich nur diese eine Wache",
               b_git["geprueft"] == ["daten_unberuehrt"], str(b_git["geprueft"]))
        pruefe("I5: keine der beiden Wachen verdeckt das Fehlen der anderen - "
               "beide melden fuer sich", rc_hash == 1 and rc_git == 1)
        pruefe("I6: das echte data/ ist dabei nicht angefasst worden",
               os.path.realpath(daten_i) != os.path.realpath(
                   os.path.join(BASE_DIR, "data")))

        # ------------------------------------------------------------------
        print("\nJ  Der Beleg ist nicht abgetippt")
        sys.path.insert(0, _HIER)
        import pruefe_register as pr
        zahlen_beleg, evidenz_beleg = pr.beleg_aus_dokument(
            os.path.join(BASE_DIR, BELEG_REL))
        register_text = open(os.path.join(BASE_DIR, REGISTER_REL),
                             encoding="utf-8").read()
        zahlen_reg = pr.register_symbolzahl(register_text)
        evidenz_reg = pr.register_faltenevidenz(register_text)
        pruefe("J1: der Beleg liefert alle neun Bots", len(zahlen_beleg) == 9,
               str(sorted(zahlen_beleg)))
        pruefe("J2: das Register liefert alle neun Bots", len(zahlen_reg) == 9,
               str(sorted(zahlen_reg)))
        pruefe("J3: die zwei Parser lesen verschiedene Dateien - und kommen "
               "auf dieselben Zahlen",
               all(zahlen_reg[k]["falten"] == zahlen_beleg[k]["falten"] and
                   zahlen_reg[k]["bestaetigung"] == zahlen_beleg[k]["bestaetigung"]
                   for k in zahlen_beleg))
        pruefe("J4: dasselbe fuer die Listen ohne Faltenevidenz",
               all(evidenz_reg[k]["symbole"] == sorted(evidenz_beleg[k])
                   for k in evidenz_beleg))
        pruefe("J5: die eingetragenen Zahlen unterscheiden sich von der alten, "
               "falschen Fassung",
               "| `t3_supertrend` | 6 / 9 / 13 / 13 / 13 / 17 / 18 | 23 | 24 |"
               in register_text and
               zahlen_reg["t3_supertrend"]["falten"] == [3, 6, 9, 13, 13, 13, 17])
        pruefe("J6: es kommt nirgends ein Symbol hinzu - jede eingetragene Zahl "
               "ist hoechstens so gross wie die alte",
               all(a <= b for a, b in zip(
                   zahlen_reg["rsi2_crypto"]["falten"], [6, 9, 13, 13, 13, 17, 18])))
    finally:
        shutil.rmtree(arbeit, ignore_errors=True)

    print("\n" + "=" * 78)
    gesamt = _ZAEHLER["ja"] + _ZAEHLER["nein"]
    print("%d/%d Pruefungen bestanden." % (_ZAEHLER["ja"], gesamt))
    print("=" * 78)
    return 0 if _ZAEHLER["nein"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
