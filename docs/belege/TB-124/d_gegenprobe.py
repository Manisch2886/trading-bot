#!/usr/bin/env python3
"""TB-124 D3 - Gegenprobe (Register 40.7) zu shared/test_verankerter_datenstand.py.

Aufruf (Repo-Wurzel): trading-env/bin/python3 docs/belege/TB-124/d_gegenprobe.py <scratchordner>
Je Fall ein eigener Prozess; geprueft wird der Rueckgabewert. Registerkopien liegen unter <scratchordner>
(ausserhalb des Repos), das Register selbst wird nur gelesen.
  F0  unveraendert                                   -> rc 0
  F1  Konstante im Speicher auf einen anderen Wert   -> rc 1
  F2  Registerkopie mit zwei Datenstandszeilen       -> rc 1
  F3  Registerkopie mit abweichendem Hexwert         -> rc 1
  F4  Registerkopie ohne Datenstandszeile            -> rc 1
  D2  nach main(): kein geladenes Modul aus research/vorregistrierung/
"""
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TEST = os.path.join(REPO, "shared", "test_verankerter_datenstand.py")
REG = os.path.join(REPO, "docs", "VORREGISTRIERUNG_neuselektion.md")
ANFANG = "| Datenstand (`datenstand_hash`) |"
SOLL = "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84"

KIND = r'''
import importlib.util, sys
spec = importlib.util.spec_from_file_location("probe", %(test)r)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
if %(reg)r: m.REGISTERDATEI = %(reg)r
if %(wert)r: m.snapshot.VERANKERTER_DATENSTAND = %(wert)r
rc = m.main()
fremd = sorted(n for n, x in list(sys.modules.items()) if "research/vorregistrierung" in (getattr(x, "__file__", "") or ""))
print("D2 Module aus research/vorregistrierung:", fremd)
sys.exit(rc)
'''


def fall(name, reg="", wert="", soll_rc=None):
    r = subprocess.run([sys.executable, "-W", "ignore", "-c", KIND % dict(test=TEST, reg=reg, wert=wert)],
                       capture_output=True, text=True)
    print("### %s  -> rc %d (Soll %d) %s" % (name, r.returncode, soll_rc, "OK" if r.returncode == soll_rc else "ABWEICHUNG"))
    print("\n".join("    " + z for z in (r.stdout + r.stderr[-400:]).strip().splitlines()))
    return r.returncode == soll_rc


def kopie(sp, name, ersetze):
    text = open(REG, encoding="utf-8").read()
    zeilen = text.split("\n")
    idx = [i for i, z in enumerate(zeilen) if z.startswith(ANFANG)]
    assert len(idx) == 1, idx
    zeilen = ersetze(zeilen, idx[0])
    p = os.path.join(sp, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen))
    return p


sp = os.path.abspath(sys.argv[1])
os.makedirs(sp, exist_ok=True)
print("# TB-124 D3 Gegenprobe zu shared/test_verankerter_datenstand.py, Registerkopien unter %s" % sp)
ok = [
    fall("F0 unveraendert", soll_rc=0),
    fall("F1 Konstante = anderer Wert", wert="0" * 64, soll_rc=1),
    fall("F2 zwei Datenstandszeilen", soll_rc=1,
         reg=kopie(sp, "reg_zwei_zeilen.md", lambda z, i: z[:i + 1] + [z[i]] + z[i + 1:])),
    fall("F3 abweichender Hexwert", soll_rc=1,
         reg=kopie(sp, "reg_anderer_wert.md", lambda z, i: z[:i] + [z[i].replace(SOLL, "e" + SOLL[1:])] + z[i + 1:])),
    fall("F4 ohne Datenstandszeile", soll_rc=1,
         reg=kopie(sp, "reg_ohne_zeile.md", lambda z, i: z[:i] + z[i + 1:])),
]
print("# Ergebnis: %d/%d Faelle mit dem Soll-Rueckgabewert" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
