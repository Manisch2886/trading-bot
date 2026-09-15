#!/usr/bin/env python3
"""
TB-33 - Herkunft: was in jeder Ergebnisdatei stehen muss
==============================================================================
Ein Ergebnis ohne Herkunft ist eine Zahl ohne Lauf. Nach dem Muster aus
`research/vorregistrierung/herkunft.py` (TB-30a) - dieselben drei Hashes,
dasselbe append-only-Protokoll, nur auf die Dateien dieses Laufs bezogen.

DREI HASHES
------------------------------------------------------------------------------
  commit      Der Git-Commit, auf dem gerechnet wurde - samt der Angabe, ob
              der Arbeitsbaum dabei sauber war.
  datenstand  SHA-256 ueber die Kursdateien dieses Laufs. Bewusst NUR ueber
              research/turn_of_month/daten/, nicht ueber data/: TB-31 aendert
              data/ parallel, und ein Hash, der sich aus fremdem Grund
              aendert, beantwortet die Frage nicht mehr, fuer die er da ist.
  register    SHA-256 ueber die eingefrorenen Festlegungen: die BEIDEN
              Registerdateien und die Module dieses Ordners. Aendert sich
              eine Festlegung, aendert sich dieser Hash - und das Protokoll
              zeigt, dass zwei Laeufe NICHT unter derselben Vorregistrierung
              liefen.

WARUM APPEND-ONLY
------------------------------------------------------------------------------
Ein ueberschreibbares Protokoll beantwortet die einzige Frage nicht, fuer die
es da ist: *wurde zwischendurch noch einmal gerechnet?* Die Datei wird nur
ergaenzt; jede Zeile traegt den Hash der vorigen.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import register as reg  # noqa: E402

BASE_DIR = reg.BASE_DIR
PROTOKOLL = os.path.join(reg.ERGEBNIS_DIR, "herkunft_protokoll.jsonl")

# BEIDE Registereintraege - der Weg ist genauso vorregistriert wie die
# Strategie, und ein Herkunftshash, der nur die Strategie erfasst, liesse
# genau die Haelfte offen, um die es in TB-33 geht.
REGISTERDATEIEN = [
    os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_S-E1_nulltest.md"),
    os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_S-E1_strategiekriterien.md"),
    os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_S-E1_pfadkriterien.md"),
]
EINGEFROREN = ["register.py", "handelstage.py", "kennzahlen.py",
               "auswertung.py", "staging.py"]


def _sha256_datei(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def commit() -> dict:
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
    """SHA-256 ueber die Kursdateien dieses Laufs, in stabiler Reihenfolge."""
    daten_dir = daten_dir or reg.DATEN_DIR
    h = hashlib.sha256()
    if not os.path.isdir(daten_dir):
        return {"datenstand": h.hexdigest(), "dateien": 0, "ordner": daten_dir}
    dateien = sorted(f for f in os.listdir(daten_dir) if f.endswith(".csv"))
    for name in dateien:
        pfad = os.path.join(daten_dir, name)
        h.update(name.encode("utf-8"))
        h.update(str(os.path.getsize(pfad)).encode("utf-8"))
        h.update(_sha256_datei(pfad).encode("utf-8"))
    return {"datenstand": h.hexdigest(), "dateien": len(dateien),
            "ordner": daten_dir}


def register_hash() -> dict:
    """SHA-256 ueber die eingefrorenen Festlegungen."""
    h = hashlib.sha256()
    fehlend, teile = [], []
    pfade = ([(os.path.basename(p), p) for p in REGISTERDATEIEN]
             + [(n, os.path.join(_HIER, n)) for n in EINGEFROREN])
    for name, pfad in pfade:
        if not os.path.exists(pfad):
            fehlend.append(name)
            continue
        d = _sha256_datei(pfad)
        teile.append({"datei": name, "sha256": d})
        h.update(name.encode("utf-8"))
        h.update(d.encode("utf-8"))
    return {"register": h.hexdigest(), "teile": teile, "fehlend": fehlend}


def block(anlass: str = "lauf", daten_dir=None) -> dict:
    """Der Herkunftsblock, der in JEDE Ergebnisdatei gehoert."""
    c, d, r = commit(), datenstand(daten_dir), register_hash()
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


# Genau die Schluessel, die eine Ergebnisdatei tragen MUSS. Pfadkriterium P3
# prueft gegen diese Liste - nicht gegen "irgendein Block ist da".
PFLICHTSCHLUESSEL = ["zeitpunkt_utc", "commit", "arbeitsbaum_sauber",
                     "datenstand", "register"]


def vollstaendig(herkunft: dict) -> list:
    """Welche Pflichtangaben fehlen? Leere Liste heisst vollstaendig."""
    if not isinstance(herkunft, dict):
        return list(PFLICHTSCHLUESSEL)
    return [s for s in PFLICHTSCHLUESSEL
            if s not in herkunft or herkunft[s] in (None, "", "unbekannt")]


def _letzte_zeile():
    if not os.path.exists(PROTOKOLL):
        return None
    with open(PROTOKOLL, encoding="utf-8") as f:
        zeilen = [z for z in f.read().splitlines() if z.strip()]
    return json.loads(zeilen[-1]) if zeilen else None


def _kettenhash(eintrag: dict) -> str:
    return hashlib.sha256(json.dumps(eintrag, sort_keys=True,
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def anhaengen(anlass: str = "lauf") -> dict:
    """Eine Zeile ans append-only-Protokoll. Nichts wird ueberschrieben."""
    vorher = _letzte_zeile()
    eintrag = block(anlass)
    eintrag["vorgaenger"] = (_kettenhash({k: v for k, v in vorher.items()
                                          if k != "kette"}) if vorher else None)
    eintrag["kette"] = _kettenhash({k: v for k, v in eintrag.items()
                                    if k != "kette"})
    os.makedirs(os.path.dirname(PROTOKOLL), exist_ok=True)
    with open(PROTOKOLL, "a", encoding="utf-8") as f:
        f.write(json.dumps(eintrag, ensure_ascii=False, sort_keys=True) + "\n")
    return eintrag


def kette_pruefen() -> list:
    """Meldet jede Zeile, deren Vorgaengerhash nicht passt."""
    if not os.path.exists(PROTOKOLL):
        return []
    with open(PROTOKOLL, encoding="utf-8") as f:
        zeilen = [json.loads(z) for z in f.read().splitlines() if z.strip()]
    fehler, vorher = [], None
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


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--anhaengen", metavar="ANLASS")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.anhaengen:
        print(json.dumps(anhaengen(args.anhaengen), indent=2,
                         ensure_ascii=False, sort_keys=True))
        return 0

    b = block("pruefung")
    if args.json:
        print(json.dumps({"herkunft": b, "kettenfehler": kette_pruefen()},
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
    fehler = kette_pruefen()
    print(f"  Protokoll     {'keine Kettenfehler' if not fehler else fehler}")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
