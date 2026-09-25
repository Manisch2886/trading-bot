"""TB-106 E5 - herkunft.py nach Block E, Beleg mit dem ECHTEN Snapshot. Aufruf aus der Repo-Wurzel:
    trading-env/bin/python3 -W ignore docs/belege/TB-106/e5_herkunft.py <herkunft.py am Stand 327bc79>
(1) Modus (TB_SELEKTIONSWURZEL = echter Snapshot 63e4b6c8) in einem Wegwerfbaum (test_ersatzwerte._e_baum):
    herkunft.py --anhaengen -> datenstand der Zeile; Vergleich mit herkunft.datenstand(<Snapshot>) und mit dem
    registrierten Datenstand d9449faf. Das echte ergebnisse/herkunft_protokoll.jsonl wird nicht beschrieben.
(2) Modus, block() ohne daten_dir -> rc.
(3) Ohne Modus: block() der neuen Fassung gegen block() der Fassung 327bc79, beide mit _HIER = dem echten
    Ordner (die alte Quelle wird mit __file__ = research/vorregistrierung/herkunft.py ausgefuehrt), ohne zeitpunkt_utc.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

V = os.path.abspath("research/vorregistrierung")
sys.path.insert(0, V)
import herkunft  # noqa: E402
import test_ersatzwerte as te  # noqa: E402

SNAP_HASH = "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
SNAP = os.path.abspath(os.path.join("snapshots", SNAP_HASH))
REGISTRIERT = "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84"
ECHT = os.path.join(V, "ergebnisse", "herkunft_protokoll.jsonl")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else "(fehlt)"


print("# TB-106 E5, HEAD %s, %s" % (os.popen("git rev-parse --short HEAD").read().strip(),
                                    datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")))
echt_vorher = sha(ECHT)
print("echtes herkunft_protokoll.jsonl vorher:", echt_vorher)

with tempfile.TemporaryDirectory() as t:
    baum, _, v, head = te._e_baum(t)
    u = {k: x for k, x in os.environ.items()
         if k not in ("TB30A_BASE_DIR", "PYTHONPATH") and not k.startswith("TB_SELEKTIONS")}
    u.update({"TB_SELEKTIONSWURZEL": SNAP, "TB_SELEKTIONSHASH": SNAP_HASH, "TB_SELEKTIONSCOMMIT": head})
    r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(v, "herkunft.py"), "--anhaengen", "tb106-e5"],
                       capture_output=True, text=True, env=u)
    prot = os.path.join(v, "ergebnisse", "herkunft_protokoll.jsonl")
    zeile = json.loads(open(prot).read().splitlines()[-1]) if os.path.exists(prot) else {}
    snap = herkunft.datenstand(SNAP)
    print("\n(1) Modus, echter Snapshot, --anhaengen im Wegwerfbaum: rc %d" % r.returncode)
    print("    Zeile: datenstand %s, datendateien %s" % (zeile.get("datenstand"), zeile.get("datendateien")))
    print("    herkunft.datenstand(<Snapshot>): %s, %d Dateien" % (snap["datenstand"], snap["dateien"]))
    print("    Zeile == Snapshot: %s;  == registrierter Datenstand d9449faf: %s" % (
        zeile.get("datenstand") == snap["datenstand"], zeile.get("datenstand") == REGISTRIERT))
    print("    data/ des Wegwerfbaums (eine erfundene Datei): %s - nicht gehasht: %s" % (
        herkunft.datenstand(os.path.join(baum, "data"))["datenstand"][:16],
        zeile.get("datenstand") != herkunft.datenstand(os.path.join(baum, "data"))["datenstand"]))
    if r.returncode:
        print("    stderr:", r.stderr[-400:])
    r2 = subprocess.run([sys.executable, "-W", "ignore", os.path.join(v, "probe_block.py")],
                        capture_output=True, text=True, env=u)
    print("\n(2) Modus, block() ohne daten_dir: rc %d; stderr: %s" % (r2.returncode, r2.stderr.strip()[-200:]))

alt_quelle = open(sys.argv[1], encoding="utf-8").read()
ns = {"__file__": os.path.join(V, "herkunft.py"), "__name__": "herkunft_alt"}
exec(compile(alt_quelle, sys.argv[1], "exec"), ns)
alt = ns["block"]("tb106-e5")
neu = herkunft.block("tb106-e5")
alt.pop("zeitpunkt_utc")
neu.pop("zeitpunkt_utc")
print("\n(3) ohne Modus: block() alt (327bc79) == neu, ohne zeitpunkt_utc: %s" % (alt == neu))
print("    Felder: %s" % sorted(neu))
print("    datenstand %s, datendateien %s, register %s" % (neu["datenstand"], neu["datendateien"], neu["register"]))
print("    (commit/arbeitsbaum_sauber/geaenderte_dateien stammen aus dem Arbeitsbaum zum Messzeitpunkt)")
print("\nechtes herkunft_protokoll.jsonl nachher:", sha(ECHT), "- unveraendert:", sha(ECHT) == echt_vorher)
