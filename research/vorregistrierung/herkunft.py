#!/usr/bin/env python3
"""
TB-30a - Herkunft: was in jeder Ergebnisdatei stehen muss
==============================================================================
Ein Ergebnis ohne Herkunft ist eine Zahl ohne Lauf. Dieses Modul erzeugt den
Herkunftsblock, der in JEDE Ergebnisdatei des Selektionslaufs gehoert, und
fuehrt das **append-only**-Protokoll, in dem jeder Lauf eine Zeile bekommt.

DREI HASHES
------------------------------------------------------------------------------
  commit      Der Git-Commit, auf dem gerechnet wurde - samt der Angabe, ob
              der Arbeitsbaum dabei sauber war. Ein Lauf auf einem
              schmutzigen Baum ist nicht reproduzierbar, und das steht dann
              auch so da.
  datenstand  SHA-256 ueber die Kursdateien, die in den Lauf eingehen -
              Dateiname, Groesse, Inhalt. TB-31 aendert `data/`; ohne diesen
              Hash liesse sich hinterher nicht sagen, auf welchem Datenstand
              ein Ergebnis entstand.
  register    SHA-256 ueber die eingefrorenen Festlegungen: die Registerdatei,
              die Module dieses Ordners und die vorab berechneten Tabellen.
              Aendert sich eine Festlegung, aendert sich dieser Hash - und
              das Protokoll zeigt, dass zwei Laeufe NICHT unter derselben
              Vorregistrierung liefen.

WARUM APPEND-ONLY
------------------------------------------------------------------------------
Ein ueberschreibbares Protokoll beantwortet die einzige Frage nicht, fuer die
es da ist: *wurde zwischendurch noch einmal gerechnet?* Die Datei wird
deshalb nur ergaenzt; das Programm weigert sich, eine bestehende Zeile zu
aendern oder zu entfernen, und prueft beim Anhaengen die Kette der
Vorgaengerzeilen (jede Zeile traegt den Hash der vorigen).

WAS OHNE BETREIBER GEHT - UND WAS NICHT
------------------------------------------------------------------------------
Commit-, Datenstand- und Register-Hash erzeugt dieses Modul selbst. Der
**signierte Tag** (GPG) und der **externe Zeitanker** (OpenTimestamps)
brauchen den Schluessel bzw. das Netz des Betreibers; die kopierbare
Anleitung dafuer steht im Testauftrag. `--pruefen` meldet, welche der vier
Verankerungen vorliegen und welche fehlen.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))
# TB-111 (Fable 25d (3)): die Wurzel, in der dieses Modul liegt - ohne
# TB30A_BASE_DIR. Aus ihr kommt paths.py, damit schon die Frage "Modus?"
# nichts unter einer Ersatzwurzel liest.
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

PROTOKOLL = os.path.join(_HIER, "ergebnisse", "herkunft_protokoll.jsonl")

REGISTERDATEI = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")
EINGEFROREN = [
    "registerdaten.py", "faltenplan.py", "benchmark.py", "kennzahlen.py",
    "auswertung.py", "messgroessen.py", "pruefe_grenzsaetze.py",
    "ergebnisse/messgroessen.json", "ergebnisse/faltenplan.json",
    "ergebnisse/benchmark_drawdowns.json",
]
# Die Commit-Hashes, die zusaetzlich auf die Sperrliste gehoeren: Simulation,
# Erkennung und Optimierer je Bot. Sie liegen ausserhalb dieses Ordners und
# werden ueber den Git-Commit des Repos mit erfasst.
SPERRLISTE_DATEIEN = [
    "shared/messkette.py", "shared/zuteilung.py",
    "strategies/*/equity_simulation.py", "strategies/*/multi_symbol_optimise.py",
    "strategies/*/multi_symbol_walk_forward.py",
]


def _sha256_datei(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def commit() -> dict:
    _ersatzwurzel_pruefen("commit")
    def git(*args):
        try:
            return subprocess.run(["git", "-C", BASE_DIR, *args],
                                  capture_output=True, text=True,
                                  check=True).stdout.strip()
        except Exception:
            return ""
    hash_ = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    return {"commit": hash_ or "unbekannt",
            "arbeitsbaum_sauber": status == "" and bool(hash_),
            "geaenderte_dateien": len([z for z in status.splitlines() if z])}


def datenstand(daten_dir=None) -> dict:
    """SHA-256 ueber alle Kursdateien, in stabiler Reihenfolge."""
    daten_dir = daten_dir or os.path.join(BASE_DIR, "data")
    h = hashlib.sha256()
    dateien = sorted(f for f in os.listdir(daten_dir) if f.endswith(".csv"))
    for name in dateien:
        pfad = os.path.join(daten_dir, name)
        h.update(name.encode("utf-8"))
        h.update(str(os.path.getsize(pfad)).encode("utf-8"))
        h.update(_sha256_datei(pfad).encode("utf-8"))
    return {"datenstand": h.hexdigest(), "dateien": len(dateien)}


def register() -> dict:
    """SHA-256 ueber die eingefrorenen Festlegungen."""
    _ersatzwurzel_pruefen("register")
    h = hashlib.sha256()
    fehlend = []
    teile = []
    for rel in ([os.path.relpath(REGISTERDATEI, _HIER)] + EINGEFROREN):
        pfad = os.path.normpath(os.path.join(_HIER, rel))
        if not os.path.exists(pfad):
            fehlend.append(rel)
            continue
        d = _sha256_datei(pfad)
        teile.append({"datei": rel, "sha256": d})
        h.update(rel.encode("utf-8"))
        h.update(d.encode("utf-8"))
    return {"register": h.hexdigest(), "teile": teile, "fehlend": fehlend}


def _paths():
    """shared/paths.py - erst bei Bedarf geladen (TB-106), damit der Import
    dieses Moduls unveraendert bleibt; nicht ueber strategy_paths.
    TB-111: aus `_WURZEL`, nicht aus `BASE_DIR` - sonst laese die Frage nach
    dem Modus unter `TB30A_BASE_DIR` (gemessen: dort rc 1, `paths` fehlt)."""
    ordner = os.path.join(_WURZEL, "shared")
    if ordner not in sys.path:
        sys.path.insert(0, ordner)
    import paths
    return paths


def _abbruch_2(stelle: str, text: str):
    """Meldung auf stderr, dann `SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)`."""
    print(f"ABBRUCH (herkunft.py::{stelle}): {text}", file=sys.stderr)
    raise SystemExit(_paths().RUECKGABEWERT_STARTPRUEFUNG)


def _ersatzwurzel_pruefen(stelle: str):
    """TB-111 (Fable 25d (3), 24d Abschnitt 3: erst 2, dann lesen): unter dem
    Selektionsmodus ist `TB30A_BASE_DIR` kein Weg - Abbruch mit 2, bevor
    `BASE_DIR`, `REGISTERDATEI` oder `commit()` die Variable benutzen.
    Gerufen von `commit()`, `register()` und `block()`. Ohne die Variable wird
    `paths` hier nicht geladen; ohne Modus bleibt alles, wie es war."""
    if not (os.environ.get("TB30A_BASE_DIR") or BASE_DIR != _WURZEL):
        return
    if _paths().selektionsmodus() is not None:
        _abbruch_2(stelle,
                   f"TB30A_BASE_DIR ist unter dem Selektionsmodus gesetzt "
                   f"({BASE_DIR}) - die Variable ersetzt die Repo-Wurzel fuer "
                   f"Mutationsproben und ist unter dem Modus kein Weg "
                   f"(Fable 25d (3)); gelesen wird nichts")


def block(anlass: str = "lauf", daten_dir=None) -> dict:
    """Der Herkunftsblock, der in jede Ergebnisdatei gehoert.

    TB-106 (Fable 25c 2 (a), Berichtigung zu 37.4): `daten_dir` geht an
    `datenstand()`. Unter dem Selektionsmodus ist er Pflicht - keine
    Voreinstellung, sonst hashte die Kette `BASE_DIR/data` statt des
    Snapshots. Ohne Modus bleibt die Voreinstellung `BASE_DIR/data`.
    """
    _ersatzwurzel_pruefen("block")
    if daten_dir is None and _paths().selektionsmodus() is not None:
        _abbruch_2("block",
                   "unter dem Selektionsmodus ohne daten_dir aufgerufen - keine "
                   "Voreinstellung unter dem Modus (Fable 25c 2 (a))")
    c, d, r = commit(), datenstand(daten_dir), register()
    return {
        "zeitpunkt_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "anlass": anlass,
        "commit": c["commit"],
        "arbeitsbaum_sauber": c["arbeitsbaum_sauber"],
        "geaenderte_dateien": c["geaenderte_dateien"],
        "datenstand": d["datenstand"],
        "datendateien": d["dateien"],
        "register": r["register"],
        "register_fehlend": r["fehlend"],
    }


def _letzte_zeile() -> dict:
    if not os.path.exists(PROTOKOLL):
        return None
    with open(PROTOKOLL, encoding="utf-8") as f:
        zeilen = [z for z in f.read().splitlines() if z.strip()]
    return json.loads(zeilen[-1]) if zeilen else None


def _kettenhash(eintrag: dict) -> str:
    return hashlib.sha256(json.dumps(eintrag, sort_keys=True,
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def anhaengen(anlass: str = "lauf", daten_dir=None) -> dict:
    """Eine Zeile ans append-only-Protokoll. Nichts wird ueberschrieben.

    `daten_dir` wie bei `block()`. Der Ordner des Protokolls wird nicht
    angelegt (TB-106, Fable 25c 4 (4)(b)): fehlt der registrierte Ort, ist das
    ein Baum, der nicht der registrierte ist - Abbruch mit 2, unabhaengig vom
    Modus.
    """
    vorher = _letzte_zeile()
    eintrag = block(anlass, daten_dir)
    eintrag["vorgaenger"] = (_kettenhash({k: v for k, v in vorher.items()
                                          if k != "kette"})
                             if vorher else None)
    eintrag["kette"] = _kettenhash({k: v for k, v in eintrag.items()
                                    if k != "kette"})
    if not os.path.isdir(os.path.dirname(PROTOKOLL)):
        _abbruch_2("anhaengen",
                   f"der Ordner des registrierten Protokolls fehlt: "
                   f"{os.path.dirname(PROTOKOLL)} - er wird nicht angelegt")
    with open(PROTOKOLL, "a", encoding="utf-8") as f:
        f.write(json.dumps(eintrag, ensure_ascii=False, sort_keys=True) + "\n")
    return eintrag


def kette_pruefen() -> list:
    """Meldet jede Zeile, deren Vorgaengerhash nicht passt."""
    if not os.path.exists(PROTOKOLL):
        return []
    with open(PROTOKOLL, encoding="utf-8") as f:
        zeilen = [json.loads(z) for z in f.read().splitlines() if z.strip()]
    fehler = []
    vorher = None
    for i, e in enumerate(zeilen):
        erwartet = (_kettenhash({k: v for k, v in vorher.items() if k != "kette"})
                    if vorher else None)
        if e.get("vorgaenger") != erwartet:
            fehler.append(f"Zeile {i + 1}: Vorgaengerhash passt nicht")
        if e.get("kette") != _kettenhash({k: v for k, v in e.items()
                                          if k != "kette"}):
            fehler.append(f"Zeile {i + 1}: eigener Hash passt nicht")
        vorher = e
    return fehler


def verankerung() -> dict:
    """Welche der vier Verankerungen liegen vor?"""
    def git(*args):
        try:
            return subprocess.run(["git", "-C", BASE_DIR, *args],
                                  capture_output=True, text=True,
                                  check=True).stdout.strip()
        except Exception:
            return ""
    tags = [t for t in git("tag", "--list", "TB-30a*").splitlines() if t]
    signiert = []
    for t in tags:
        art = git("cat-file", "-t", t)
        if art == "tag" and "BEGIN PGP SIGNATURE" in git("cat-file", "-p", t):
            signiert.append(t)
    ots = [f for f in os.listdir(os.path.join(_HIER, "ergebnisse"))
           if f.endswith(".ots")] if os.path.isdir(
               os.path.join(_HIER, "ergebnisse")) else []
    return {
        "signierter_tag": {"vorhanden": bool(signiert), "tags": signiert,
                           "wer": "Betreiber (GPG-Schluessel)"},
        "zeitanker_opentimestamps": {"vorhanden": bool(ots), "dateien": ots,
                                     "wer": "Betreiber (Netzzugang)"},
        "herkunft_in_ergebnisdateien": {"vorhanden": True,
                                        "wer": "dieses Modul"},
        "urteil_ist_code": {"vorhanden": os.path.exists(
            os.path.join(_HIER, "auswertung.py")), "wer": "dieses Repo"},
    }


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--anhaengen", metavar="ANLASS",
                   help="eine Zeile ans append-only-Protokoll haengen")
    p.add_argument("--pruefen", action="store_true",
                   help="Kette und Verankerung pruefen")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.anhaengen:
        # Unter dem Modus der Datenordner des Snapshots aus dem Resolver
        # (TB-106); ohne Modus die Voreinstellung.
        resolver = _paths()
        e = anhaengen(args.anhaengen, resolver.DATA_DIR
                      if resolver.selektionsmodus() is not None else None)
        print(json.dumps(e, indent=2, ensure_ascii=False, sort_keys=True))
        return 0

    # Die Pruefansicht wie --anhaengen: unter dem Modus der Datenordner des
    # Snapshots (TB-111, Fable 25d (2)); ohne Modus die Voreinstellung.
    resolver = _paths()
    b = block("pruefung", resolver.DATA_DIR
              if resolver.selektionsmodus() is not None else None)
    if args.json:
        print(json.dumps({"herkunft": b, "verankerung": verankerung(),
                          "kettenfehler": kette_pruefen()},
                         indent=2, ensure_ascii=False, sort_keys=True))
        return 1 if kette_pruefen() else 0

    print(__doc__.strip().split("\n")[0])
    print(f"\n  Commit        {b['commit'][:12]}  "
          f"Arbeitsbaum {'sauber' if b['arbeitsbaum_sauber'] else 'GEAENDERT'} "
          f"({b['geaenderte_dateien']} Datei(en))")
    print(f"  Datenstand    {b['datenstand'][:16]}...  "
          f"({b['datendateien']} Kursdateien)")
    print(f"  Register      {b['register'][:16]}...")
    if b["register_fehlend"]:
        print(f"  ! fehlend     {b['register_fehlend']}")
    print("\n  Verankerung:")
    for name, v in verankerung().items():
        print(f"    {'JA ' if v['vorhanden'] else 'OFFEN'}  {name:32s} "
              f"({v['wer']})")
    fehler = kette_pruefen()
    print(f"\n  Protokoll     {'keine Kettenfehler' if not fehler else fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
