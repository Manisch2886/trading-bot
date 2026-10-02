#!/usr/bin/env python3
"""TB-131 B2: Probe mit Gegenprobe für docs/werkzeuge/ampel.py.

Alte Fassung: git show <S0>:docs/werkzeuge/ampel.py nach $TMPDIR.
Zwei erfundene Protokolle in $TMPDIR (keine echten Sitzungsdaten):
  P1 normal: drei assistant-Zeilen mit verschiedenen message.id.
  P2 wie P1, davor zwei assistant-Zeilen mit input 0 und null in den Cache-Feldern.
Soll: alt(P1) rc 0 · neu(P1) rc 0, Ausgabe bytegleich alt(P1) · alt(P2) rc != 0 ·
      neu(P2) rc 0, Ausgabe bytegleich neu(P1). Ausgabe nach b2_probe_ampel.txt.

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 docs/belege/TB-131/b2_probe_ampel.py <S0>
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

S0 = sys.argv[1]
NEU = Path("docs/werkzeuge/ampel.py")
AUSGABE = Path("docs/belege/TB-131/b2_probe_ampel.txt")
tmp = Path(tempfile.mkdtemp(prefix="tb131_b2_", dir=os.environ.get("TMPDIR")))

alt = tmp / "ampel_alt.py"
alt.write_bytes(subprocess.run(["git", "show", f"{S0}:docs/werkzeuge/ampel.py"],
                               check=True, capture_output=True).stdout)


def zeile(mid, ts, inp, cr, cc, out):
    return json.dumps({"type": "assistant", "timestamp": ts,
                       "message": {"id": mid, "usage": {
                           "input_tokens": inp, "cache_read_input_tokens": cr,
                           "cache_creation_input_tokens": cc, "output_tokens": out}}})


normal = [
    zeile("msg_p_1", "2026-10-02T10:00:00Z", 2, 100000, 20000, 100),
    zeile("msg_p_2", "2026-10-02T10:01:00Z", 2, 110000, 1000, 50),
    zeile("msg_p_3", "2026-10-02T10:02:00Z", 2, 120000, 500, 20),
]
leer = [
    zeile("msg_l_1", "2026-10-02T09:59:00Z", 0, None, None, 0),
    zeile("msg_l_2", "2026-10-02T09:59:30Z", 0, None, None, 0),
]
p1, p2 = tmp / "P1.jsonl", tmp / "P2.jsonl"
p1.write_text("\n".join(normal) + "\n", encoding="utf-8")
p2.write_text("\n".join(leer + normal) + "\n", encoding="utf-8")


def lauf(skript, proto):
    r = subprocess.run([sys.executable, str(skript), str(proto)], capture_output=True)
    return r.returncode, r.stdout, r.stderr


ergebnis = {}
for name, skript in (("alt", alt), ("neu", NEU)):
    for pn, proto in (("P1", p1), ("P2", p2)):
        ergebnis[(name, pn)] = lauf(skript, proto)

aus = [f"# TB-131 B2 — Probe ampel.py (b2_probe_ampel.py), alt = {S0}:docs/werkzeuge/ampel.py",
       f"# Interpreter {sys.executable} · Python {sys.version.split()[0]}",
       f"# Protokolle in {tmp} (erfunden)"]
for k, (rc, so, se) in ergebnis.items():
    aus.append(f"{k[0]}({k[1]}) rc {rc}")
    for z in so.decode().splitlines():
        aus.append(f"    stdout: {z}")
    letzte = se.decode().strip().splitlines()[-1:] if se else []
    for z in letzte:
        aus.append(f"    stderr (letzte Zeile): {z}")

soll = [
    ("alt(P1) rc 0", ergebnis[("alt", "P1")][0] == 0),
    ("neu(P1) rc 0", ergebnis[("neu", "P1")][0] == 0),
    ("neu(P1) stdout bytegleich alt(P1)", ergebnis[("neu", "P1")][1] == ergebnis[("alt", "P1")][1]),
    ("alt(P2) rc != 0 (Gegenprobe)", ergebnis[("alt", "P2")][0] != 0),
    ("neu(P2) rc 0", ergebnis[("neu", "P2")][0] == 0),
    ("neu(P2) stdout bytegleich neu(P1)", ergebnis[("neu", "P2")][1] == ergebnis[("neu", "P1")][1]),
]
for text, gut in soll:
    aus.append(f"Soll {text}: {'ja' if gut else 'NEIN'}")
alle = all(g for _, g in soll)
aus.append(f"Gesamt: {'alle Soll erfüllt' if alle else 'ABWEICHUNG'}")
AUSGABE.write_text("\n".join(aus) + "\n", encoding="utf-8")
print("\n".join(aus))
sys.exit(0 if alle else 1)
