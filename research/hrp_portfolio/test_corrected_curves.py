"""
Sanity-Checks fuer corrected_curves.py (Nachtrag zum Sync-Check)
====================================================================
Bewusst ohne Test-Framework, wie in allen Vorgaenger-Untersuchungen.
Geprueft wird ausschliesslich die LOGIK des Umbiegens - dass die erzeugten
Kurven zahlenmaessig stimmen, prueft `generate()` selbst auf den echten
Daten (byteweiser Vergleich der synchronen Bots, Sync-Check-Kennzahlen der
abweichenden). Diese Tests brauchen deshalb keine Kursdaten und laufen in
Sekunden.

Nutzung:  python3 test_corrected_curves.py
"""

import os
import sys
import types

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

import corrected_curves as cc

PASSED = FAILED = 0


def check(label, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  OK    {label}")
    else:
        FAILED += 1
        print(f"  FEHLER {label}   {detail}")


def fake_po(bot_names, legacy=None):
    """Minimaler Ersatz fuer portfolio_overview: liefert dieselbe
    dict-Struktur wie discover_bots() und reicht sie unveraendert durch."""
    module = types.ModuleType("fake_po")
    module.LEGACY_EQUITY_CSV_PATHS = legacy or {}
    module.discover_bots = lambda: {
        name: {"equity_csv": f"/results/{name}/equity_curve.csv",
               "db_file": None, "is_live": True}
        for name in bot_names}
    module.load_all_curves = lambda bots: {n: dict(v) for n, v in bots.items()}
    return module


print("\n1) Bot-Listen")
check("die fuenf abweichenden und die vier synchronen Bots ueberschneiden sich nicht",
      not (set(cc.DIVERGENT_BOTS) & set(cc.CLEAN_BOTS)),
      str(set(cc.DIVERGENT_BOTS) & set(cc.CLEAN_BOTS)))
check("zusammen ergeben sie genau 9 Bots", len(cc.ALL_BOTS) == 9, str(len(cc.ALL_BOTS)))
strategies = os.path.join(_REPO_ROOT, "strategies")
if os.path.isdir(strategies):
    on_disk = {n for n in os.listdir(strategies)
               if os.path.isdir(os.path.join(strategies, n)) and not n.startswith("__")}
    check("die Liste deckt sich mit den tatsaechlich vorhandenen Bot-Ordnern",
          set(cc.ALL_BOTS) == on_disk, f"nur in Liste: {set(cc.ALL_BOTS) - on_disk}, "
                                        f"nur auf Platte: {on_disk - set(cc.ALL_BOTS)}")
check("jeder abweichende Bot hat einen Sync-Check-Referenzwert",
      set(cc.SYNC_CHECK_REFERENCE) == set(cc.DIVERGENT_BOTS))
check("der als veraltet dokumentierte Bot gilt konfigurationsseitig als synchron",
      set(cc.KNOWN_STALE_BOTS) <= set(cc.CLEAN_BOTS))

print("\n2) Die beiden Tauschmengen")
check("SWAP_PRIMARY sind genau die fuenf abweichenden Bots",
      set(cc.SWAP_PRIMARY) == set(cc.DIVERGENT_BOTS))
check("SWAP_WITH_STALE nimmt genau den veralteten Bot zusaetzlich dazu",
      set(cc.SWAP_WITH_STALE) == set(cc.DIVERGENT_BOTS) | set(cc.KNOWN_STALE_BOTS)
      and len(cc.SWAP_WITH_STALE) == 6)

print("\n3) Umbiegen der Quellpfade")
generated = {b: {"csv": f"/korrigiert/{b}.csv"} for b in cc.ALL_BOTS}
po_stub = fake_po(cc.ALL_BOTS)

_, curves = cc.load_corrected_curves(po_stub, generated)          # Vorgabe = SWAP_PRIMARY
swapped = {b for b, v in curves.items() if v["equity_csv"].startswith("/korrigiert/")}
check("Vorgabe tauscht genau die fuenf abweichenden Bots",
      swapped == set(cc.DIVERGENT_BOTS), str(sorted(swapped)))
check("die synchronen Bots lesen weiterhin die Original-Datei",
      all(curves[b]["equity_csv"] == f"/results/{b}/equity_curve.csv" for b in cc.CLEAN_BOTS))

_, curves_none = cc.load_corrected_curves(po_stub, generated, swap_bots=())
check("eine leere Tauschmenge laesst alle neun Pfade unveraendert (Basis 'original')",
      all(v["equity_csv"] == f"/results/{b}/equity_curve.csv" for b, v in curves_none.items()))

_, curves_all = cc.load_corrected_curves(po_stub, generated, swap_bots=cc.SWAP_WITH_STALE)
swapped_all = {b for b, v in curves_all.items() if v["equity_csv"].startswith("/korrigiert/")}
check("SWAP_WITH_STALE tauscht sechs Bots, die drei uebrigen bleiben unveraendert",
      swapped_all == set(cc.SWAP_WITH_STALE) and len(swapped_all) == 6, str(sorted(swapped_all)))

# Ein Tippfehler in der Tauschliste darf nicht still zu einer ungetauschten
# Kurve fuehren - das waere genau der Fehler, den dieser Nachtrag behebt.
try:
    cc.load_corrected_curves(po_stub, generated, swap_bots=("gibt_es_nicht",))
    check("ein unbekannter Bot in der Tauschliste bricht ab statt still zu ignorieren", False)
except SystemExit:
    check("ein unbekannter Bot in der Tauschliste bricht ab statt still zu ignorieren", True)

print("\n4) Sonderpfad der elliott_wave-Kurve")
legacy_po = fake_po(cc.ALL_BOTS, legacy={"elliott_wave": "/legacy/equity_curve.csv"})
resolved = cc.original_csv_path("/nicht/vorhanden", "elliott_wave", legacy_po)
check("ohne results/elliott_wave/equity_curve.csv greift der Legacy-Pfad aus "
      "portfolio_overview (nicht neu definiert, sondern von dort gelesen)",
      resolved == "/legacy/equity_curve.csv", resolved)
real_root = _REPO_ROOT
real_path = cc.original_csv_path(real_root, "t3_supertrend", legacy_po)
check("fuer die uebrigen Bots bleibt es beim Standardpfad results/<bot>/equity_curve.csv",
      real_path.endswith(os.path.join("results", "t3_supertrend", "equity_curve.csv")), real_path)

print("\n" + "=" * 60)
print(f"{PASSED} Checks bestanden, {FAILED} fehlgeschlagen.")
print("=" * 60)
sys.exit(1 if FAILED else 0)
