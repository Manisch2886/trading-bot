"""
Pfad-Helfer fuer strategie-spezifische Skripte
==================================================
Jede Strategie lebt in einem eigenen Ordner unter strategies/<name>/.
Diese Funktion leitet daraus automatisch ab:
- einen EIGENEN results/-Unterordner pro Strategie
- einen EIGENEN logs/-Unterordner pro Strategie
- eine EIGENE Datenbank-Datei pro Strategie (WICHTIG: sonst wuerden
  sich mehrere Strategien eine gemeinsame Trade-Historie teilen)

Nutzung in einem Strategie-Skript (z.B. strategies/elliott_wave/forward_test.py):

    import os, sys
    _STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))
    _SHARED_DIR = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "shared")
    sys.path.insert(0, _SHARED_DIR)

    from strategy_paths import get_strategy_paths
    P = get_strategy_paths(__file__)
    DATA_DIR = P["DATA_DIR"]
    RESULTS_DIR = P["RESULTS_DIR"]
    DB_FILE = P["DB_FILE"]
    # usw.

Die ersten vier Zeilen sind das einzige "Boilerplate", das jedes
Strategie-Skript braucht - unveraendert kopierbar fuer jede neue
Strategie, da der Strategie-Name automatisch aus dem Ordnernamen
gelesen wird.
"""

import os


def get_strategy_paths(caller_file: str) -> dict:
    strategy_dir = os.path.dirname(os.path.abspath(caller_file))
    base_dir = os.path.dirname(os.path.dirname(strategy_dir))  # .../strategies/<name> -> .../strategies -> BASE
    strategy_name = os.path.basename(strategy_dir)

    results_dir = os.path.join(base_dir, "results", strategy_name)
    logs_dir = os.path.join(base_dir, "logs", strategy_name)
    db_file = os.path.join(base_dir, f"paper_trading_{strategy_name}.db")

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    return {
        "BASE_DIR": base_dir,
        "STRATEGY_NAME": strategy_name,
        "DATA_DIR": os.path.join(base_dir, "data"),
        "CONFIG_DIR": os.path.join(base_dir, "config"),
        "RESULTS_DIR": results_dir,
        "LOGS_DIR": logs_dir,
        "DB_FILE": db_file,
    }
