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

---------------------------------------------------------------------------
DATA_DIR und CONFIG_DIR kommen aus dem Resolver (TB-53b)
---------------------------------------------------------------------------
Bis TB-53b hat diese Datei den Kursdatenpfad **selbst** gebaut
(`os.path.join(base_dir, "data")`) und `shared/paths.py` nie beruehrt.
Damit ging der Selektionsmodus aus TB-52 an **allen 90 Selektionsmodulen**
vorbei: 71 davon fragen `get_strategy_paths()` direkt, 19 ueber
`multi_symbol_optimise` - und kein einziges `shared/paths.py`
(gemessen 19.09.2026, TB-53a).

Seit TB-53b werden `DATA_DIR` und `CONFIG_DIR` **nicht mehr hier gebaut,
sondern aus `shared/paths.py` bezogen.** Damit gilt hier, was dort gemessen
ist:

    ohne Modus   DATA_DIR ist zeichengleich mit vorher - der Cron-Fall und
                 der Regelfall (gemessen: 9 von 9 Bots, `shared/test_strategy_paths.py`)
    mit Modus    DATA_DIR zeigt in die Snapshot-Wurzel; der Hash wird von
                 `paths.py` geprueft, nicht hier

⚠️ **Hier steht KEIN zweiter Resolver.** Die Umgebungsvariablen werden hier
nicht gelesen, der Hash nicht geprueft, `Selektionsfehler` nicht noch einmal
definiert. Zwei Quellen fuer eine Aussage laufen irgendwann auseinander, und
niemand merkt es (Backlog T55.8, T54.3).

`RESULTS_DIR`, `LOGS_DIR` und `DB_FILE` bleiben, wie sie sind: sie zeigen auf
den **Betrieb**, nicht auf die Kursdaten, und duerfen nie in den Snapshot
zeigen.

⚠️ **Der eine Fallstrick, und wie er zugesichert ist.** `shared/paths.py`
bestimmt seine Wurzel aus der **eigenen** Lage; diese Funktion bestimmt
`base_dir` aus der Lage des **Aufrufers**. Dass beides fuer die neun Bots
dieselbe Wurzel ist, war bis TB-53b eine Annahme. Sie ist am 19.09.2026
gemessen (9 von 9 zeichengleich) und wird seitdem bei jedem Lauf von
`shared/test_strategy_paths.py` (Probe E) nachgemessen.

⚠️ **Im Quelltext zugesichert ist etwas anderes, und zwar absichtlich:** dass
das `paths`, das hier antwortet, **das neben dieser Datei** ist - dieselbe
`shared/`. Ein fremdes `paths` (anderer Baum, anderes Paket gleichen Namens)
wirft einen `Resolverfehler`, statt still einen Pfad aus einem anderen Baum
zu liefern. ⭐ **Die Wurzel des Aufrufers wird hier NICHT gegen die Wurzel
des Resolvers geprueft.** Beim Bau von TB-53b hat genau diese Pruefung drei
Tests rot gemacht (`test_determinismus` ueber das Werkzeug
`determinismus_lauf.py --basis`, `test_ladeprotokoll`, `test_wellenauswahl`):
sie laden **absichtlich** eine Bot-Kopie aus einem Wegwerfbaum mit der
echten `shared/` - Ergebnisse und Datenbank im Wegwerfbaum, Kursdaten aus
dem Resolver. Das ist ein Muster dieses Projekts, kein Fehler; der Betreiber
hat am 19.09.2026 entschieden, es zu erhalten.
"""

import os

# ⚠️ `paths` wird ueber den Modulnamen importiert, nicht ueber seinen
# Dateipfad: nur so ist es DASSELBE Modulobjekt wie bei jedem anderen
# Importeur im Prozess (`symbols_config`, die Abrufskripte) - ein zweites
# Modulobjekt haette einen eigenen `Selektionsfehler`-Typ, den ein
# `except paths.Selektionsfehler` nicht faengt, und schriebe die
# Modus-Zeile ein zweites Mal auf stderr. Wer `strategy_paths` importieren
# kann, hat `shared/` auf `sys.path` - `paths` liegt daneben.
import paths


class Resolverfehler(RuntimeError):
    """Das `paths`, das geantwortet hat, ist nicht das neben dieser Datei.

    ⚠️ Eigener Typ, damit ein Aufrufer ihn von einem `OSError` und vom
    `Selektionsfehler` aus `paths.py` unterscheiden kann. Er wird **nicht**
    abgefangen und in einen Rueckfallwert verwandelt - ein Kursdatenpfad aus
    einem fremden Resolver waere der stille falsche Pfad, den diese
    Zusicherung verhindern soll (Prueffrage D1).
    """


_HIER = os.path.dirname(os.path.realpath(__file__))


def _resolver_ist_nachbar():
    """Liegt `paths.py` physisch neben dieser Datei? (Symlinks aufgeloest -
    ein Wegwerfbaum, der `shared/` per Symlink einbindet, ist dieselbe
    `shared/`.)"""
    return os.path.dirname(os.path.realpath(paths.__file__)) == _HIER


def _im_selektionsmodus():
    """Ist der Selektionsmodus aktiv? Gefragt wird `paths.selektionsmodus()`.

    ⚠️ Zwei Proben setzen absichtlich ein `paths` OHNE diese Funktion ein:
    `shared/test_paths.py` Probe A (die Fassung aus TB-52) und
    `shared/test_strategy_paths.py` C4 (ein nachgebauter Resolver). Fuer sie
    bleibt es beim Verhalten vor TB-105 (Ordner werden angelegt). Das echte
    `paths.py` fuehrt die Funktion; dass es das echte ist, sichert
    `_resolver_ist_nachbar()` zu.
    """
    frage = getattr(paths, "selektionsmodus", None)
    return frage is not None and frage() is not None


def get_strategy_paths(caller_file: str) -> dict:
    strategy_dir = os.path.dirname(os.path.abspath(caller_file))
    base_dir = os.path.dirname(os.path.dirname(strategy_dir))  # .../strategies/<name> -> .../strategies -> BASE
    strategy_name = os.path.basename(strategy_dir)

    # ⭐ Die Zusicherung aus TB-53b: der Resolver, der gleich antwortet, ist
    # der aus dieser `shared/`. Sonst wird nicht weitergerechnet.
    if not _resolver_ist_nachbar():
        raise Resolverfehler(
            "%s hat `paths` aus %s bekommen, erwartet wird das paths.py neben "
            "%s. DATA_DIR kaeme dann aus einem fremden Resolver - hier wird "
            "nicht weitergerechnet."
            % (os.path.abspath(caller_file), paths.__file__, __file__))

    results_dir = os.path.join(base_dir, "results", strategy_name)
    logs_dir = os.path.join(base_dir, "logs", strategy_name)
    db_file = os.path.join(base_dir, f"paper_trading_{strategy_name}.db")

    # TB-105 (Fable 25a (A) (iii)): unter dem Selektionsmodus werden die
    # Betriebsordner NICHT angelegt - ein geschuetzter Lauf schreibt nicht
    # ins Repo. Die Pfade kommen trotzdem zurueck; wer unter dem Modus doch
    # hineinschreibt, bricht mit FileNotFoundError ab, statt still Spuren
    # im Betrieb zu hinterlassen. Ohne Modus unveraendert.
    if not _im_selektionsmodus():
        os.makedirs(results_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)

    return {
        "BASE_DIR": base_dir,
        "STRATEGY_NAME": strategy_name,
        "DATA_DIR": paths.DATA_DIR,
        "CONFIG_DIR": paths.CONFIG_DIR,
        "RESULTS_DIR": results_dir,
        "LOGS_DIR": logs_dir,
        "DB_FILE": db_file,
    }
