"""
Selbsttests: Determinismus-Pruefung (TB-23)
==============================================================================
Geprueft wird das VERHALTEN von

    shared/determinismus.py        -> Urteil je Bot, Rueckgabewert, Bericht
    shared/determinismus_lauf.py   -> Permutation, Vergleich, Zwischenspeicher

    python3 shared/test_determinismus.py
    python3 shared/test_determinismus.py --schnell   # ohne die teuren Abschnitte


WARUM DIESER TEST NICHT DEN QUELLTEXT DURCHSUCHT
------------------------------------------------------------------------------
Eine Textsuche nach `kind="stable"` oder nach dem Wort "Permutation" wuerde
genau das pruefen, was der Diff ohnehin zeigt, und nichts darueber sagen, ob
die Zusicherung traegt. Dieselbe Begruendung steht in
`shared/test_stabile_sortierung.py`.

Stattdessen wird das Werkzeug an **echtem Bot-Code** ausgefuehrt - an einer
wegwerfbaren Kopie in einem temporaeren Ordner, die dreimal in
unterschiedlichem Zustand aufgesetzt wird.


DIE EIGENTLICHE ZUSICHERUNG
------------------------------------------------------------------------------
    Liefern zwei Permutationen derselben Symbolliste unterschiedliche
    Backtest-Ergebnisse, meldet das Werkzeug das - und liefern sie dieselben,
    meldet es das ebenfalls.

Der zweite Halbsatz ist der Kern. Ein Test, der immer rot ist, wird
abgeschaltet; ein Werkzeug, das jeden Bot als "nicht deterministisch" meldet,
ist keine Messung, sondern eine Konstante. Deshalb gibt es zu jedem roten Fall
einen gruenen mit **derselben** Kopie.


DIE DREI ZUSTAENDE DER KOPIE (Abschnitt 3 bis 5)
------------------------------------------------------------------------------
Ausgangspunkt ist jedes Mal `strategies/turtle_soup_crypto/` - der guenstigste
echte Bot (24 Symbole, Tageskerzen). Kopiert wird in einen temporaeren
Projektbaum; `data/`, `config/` und `shared/` sind Verweise auf das Original,
also **nur gelesen**. Am Repo selbst aendert sich nichts (Abschnitt 8).

* **UNVERAENDERT** - der Bot, wie er im Repo steht. Erwartung: **kein Befund**.
* **GEHAERTET** - eine Fassung, deren Ergebnis von der Symbolreihenfolge gar
  nicht mehr abhaengen KANN: totale Sortierung mit Zweitschluessel, kein
  Positionslimit, eine Allokation, die das Kapital nie binden kann. Erwartung:
  ebenfalls kein Befund - aber aus einem ganz anderen Grund.
* **ZUTEILUNG ZURUECKGEDREHT** - der unveraenderte Bot, in dem genau eine
  Sache auf den Stand vor TB-26 zurueckgesetzt ist: den knappen Platz bekommt
  wieder der erste Kandidat in der Zeilenreihenfolge des Trade-DataFrames.
  Erwartung: Befund.

**Die erste Erwartung hat sich mit TB-26 umgedreht**, und das ist keine
Abschwaechung des Tests, sondern sein Gegenstand. Bis TB-23 war der
unveraenderte Bot der rote Fall: wurde ein Platz knapp, entschied die
Zeilenreihenfolge. Seit TB-26 entscheidet die Zuteilungskaskade
(`shared/zuteilung.py`), und der unveraenderte Bot ist gruen. Der rote Fall
ist deshalb an den dritten Zustand gewandert - der geht vom **nachweislich
gruenen** Fall aus und aendert genau eine Sache. Waere der rote Fall weiterhin
"irgendein Bot mit mehreren gleichzeitigen Ursachen", koennte eine zweite
Wache das Fehlen der ersten verdecken: der Test wuerde rot, ohne dass klar
waere, welche Zusicherung ihn rot gemacht hat.


DIE ZWEITE FALLE: EINE PROBE, DIE SICH SELBST BESTAETIGT
------------------------------------------------------------------------------
Ein Test, der den Unterschied selbst herstellt und dann findet, hat nichts
gezeigt. Deshalb beobachtet Abschnitt 2 den **Ablauf**: die Kopie schreibt bei
jedem Ladevorgang die Symbolreihenfolge mit, die sie tatsaechlich gesehen hat.
Geprueft wird daran, dass das Werkzeug den Bot wirklich N-mal mit N
verschiedenen Reihenfolgen derselben Symbolmenge aufgerufen hat - und dass der
erste Lauf die unveraenderte Originalreihenfolge war.


DER GEFAEHRLICHSTE FEHLER DES WERKZEUGS (Abschnitt 6)
------------------------------------------------------------------------------
Nicht ein falscher Alarm, sondern eine falsche Entwarnung: kommt die
Permutation gar nicht im Bot an, rechnet das Werkzeug N-mal dasselbe und
meldet neun deterministische Bots. Abschnitt 6 setzt genau diesen Zustand her -
eine Kopie, deren `load_all_symbol_data()` die Reihenfolge ignoriert - und
verlangt, dass das Werkzeug UNKLAR meldet statt DETERMINISTISCH.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

_SHARED_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED_DIR)
sys.path.insert(0, _SHARED_DIR)

import determinismus as d                                      # noqa: E402
import determinismus_lauf as dl                                # noqa: E402

# Der guenstigste echte Bot: 24 Krypto-Symbole auf Tageskerzen, ein Lauf in
# unter zwei Sekunden. Die Aussage dieses Tests haengt nicht an der Strategie,
# nur daran, dass es ECHTER Bot-Code ist.
VORLAGE = "turtle_soup_crypto"

# Datei, in die die Kopie ihre tatsaechlich gesehene Symbolreihenfolge
# schreibt - die Grundlage von Abschnitt 2.
MITSCHRIFT = "ladeordnung.log"


class Protokoll:
    """Sammelt Pruefungen, statt beim ersten Fehler abzubrechen - ein
    einzelner Fehlschlag soll nicht verbergen, was die uebrigen Abschnitte
    gesagt haetten."""

    def __init__(self):
        self.ok = 0
        self.fehler = []

    def pruefe(self, abschnitt: str, text: str, bedingung: bool, zusatz: str = ""):
        if bedingung:
            self.ok += 1
            print(f"  OK    {text}")
        else:
            self.fehler.append(f"{abschnitt}: {text}{(' - ' + zusatz) if zusatz else ''}")
            print(f"  FEHLT {text}" + (f"  [{zusatz}]" if zusatz else ""))


# ===========================================================================
# Der temporaere Projektbaum
# ===========================================================================
def baue_kopie(ordner: str, bot: str = VORLAGE) -> str:
    """Legt <ordner>/strategies/<bot> als echte Kopie an und verweist fuer
    data/, config/ und shared/ auf das Original. Nur der Strategie-Ordner ist
    beschreibbar; alles andere wird gelesen."""
    os.makedirs(os.path.join(ordner, "strategies"), exist_ok=True)
    ziel = os.path.join(ordner, "strategies", bot)
    shutil.copytree(os.path.join(BASE_DIR, "strategies", bot), ziel,
                    dirs_exist_ok=True)
    for name in ("data", "config", "shared"):
        verweis = os.path.join(ordner, name)
        if not os.path.exists(verweis):
            os.symlink(os.path.join(BASE_DIR, name), verweis)
    return ziel


def _ersetze(pfad: str, alt: str, neu: str) -> bool:
    """Eine Textersetzung, die fehlschlaegt statt still nichts zu tun. Eine
    Mutation, die gar nicht eingebaut wurde, wuerde sonst als 'Test bestanden'
    durchgehen - der Fehler, vor dem Prinzip 7.12 warnt."""
    with open(pfad) as f:
        inhalt = f.read()
    if alt not in inhalt:
        return False
    with open(pfad, "w") as f:
        f.write(inhalt.replace(alt, neu, 1))
    return True


def mitschrift_einbauen(strategie_dir: str, ordner: str) -> bool:
    """Die Kopie protokolliert bei jedem Ladevorgang, welche Symbolreihenfolge
    sie GESEHEN hat. Das ist die Beobachtung des Ablaufs - nicht des
    Ergebnisses."""
    pfad = os.path.join(strategie_dir, "multi_symbol_optimise.py")
    log = os.path.join(ordner, MITSCHRIFT).replace("\\", "/")
    return _ersetze(
        pfad,
        "def load_all_symbol_data() -> dict:\n",
        "def load_all_symbol_data() -> dict:\n"
        f"    with open({log!r}, 'a') as _mit:\n"
        "        _mit.write(','.join(SYMBOLS) + '\\n')\n")


def haerten(strategie_dir: str) -> list:
    """Macht die Kopie unabhaengig von der Symbolreihenfolge - und zwar so,
    dass kein Zweifel bleibt, WARUM:

    1. Totale Sortierung: `entry_time, symbol, exit_time` mit stabilem
       Verfahren. Danach gibt es keinen Gleichstand mehr, den die
       Eingabereihenfolge entscheiden koennte.
    2. Kein Positionslimit - die haeufigste Ursache faellt weg.
    3. Eine Allokation von 0,01 %: bei hoechstens ein paar hundert
       gleichzeitig offenen Positionen kann das freie Kapital nie knapp
       werden, also kann auch die Kapitalschranke nie zuteilen.

    Gibt die Liste der Aenderungen zurueck, die NICHT eingebaut werden
    konnten - leer heisst: alle drei sitzen."""
    pfad = os.path.join(strategie_dir, "equity_simulation.py")
    lp = os.path.join(strategie_dir, "live_params.py")
    misslungen = []
    if not _ersetze(pfad, 'combined.sort_values("entry_time")',
                    'combined.sort_values(["entry_time", "symbol", "exit_time"], '
                    'kind="stable")'):
        misslungen.append("totale Sortierung")
    if not _ersetze(pfad, "ALLOCATION_PCT = _ALLOCATION_PCT_PROZENT / 100",
                    "ALLOCATION_PCT = 0.0001"):
        misslungen.append("winzige Allokation")
    if not _ersetze(lp, "MAX_CONCURRENT_POSITIONS = 8",
                    "MAX_CONCURRENT_POSITIONS = None"):
        misslungen.append("kein Positionslimit")
    return misslungen


def zuteilung_zurueckdrehen(strategie_dir: str) -> bool:
    """Setzt in der KOPIE genau eine Sache auf den Stand vor TB-26 zurueck:
    die Zuteilung.

    Vorher entschied bei knappem Platz die Zeilenreihenfolge des
    Trade-DataFrames - Pythons stabile Sortierung liess die Einfuegereihenfolge
    stehen, und die ist die Symbolreihenfolge der Konfigurationsdatei. Genau
    das wird hier wiederhergestellt, indem die beiden Entscheidungen der
    Kaskade auf "der erste der Liste" zurueckgestellt werden. Die Strategie,
    die Parameter und die erzeugten Signale bleiben unberuehrt - deshalb ist
    die Signalmenge auch in diesem Zustand identisch, und nur die AUSWAHL
    schwankt. Abschnitt 5 prueft genau das.

    Der Eingriff sitzt in der Kopie, nicht im Modul: `shared/` ist im
    temporaeren Baum ein Verweis auf das Original und wird nur gelesen.
    """
    pfad = os.path.join(strategie_dir, "equity_simulation.py")
    return _ersetze(
        pfad,
        "from zuteilung import simuliere_portfolio, protokollzeilen",
        "from zuteilung import simuliere_portfolio, protokollzeilen\n"
        "import zuteilung as _vor_tb26\n"
        "_vor_tb26.Zuteiler.waehle = (\n"
        "    lambda self, kandidaten, buch, zeit: list(kandidaten)[0])\n"
        "_vor_tb26.Zuteiler.ausstiegsreihenfolge = (\n"
        "    lambda self, positionen: list(positionen))")


def fehler_einbauen(strategie_dir: str) -> bool:
    """Genau EIN kuenstlicher versteckter Zustand, eingebaut in die GEHAERTETE
    Fassung: eine Zuteilung nach Dateireihenfolge bei bindendem Limit.

    Beides zusammen ist noetig, und das ist der Punkt:

    * Das Limit allein genuegt nicht - in der gehaerteten Fassung ist die
      Trade-Reihenfolge total geordnet (entry_time, symbol, exit_time), also
      steht auch bei bindendem Limit von vornherein fest, wer den Platz
      bekommt. Genau das macht die Gegenprobe in Abschnitt 4 belastbar.
    * Die Sortierung nach Dateireihenfolge allein genuegt ebenfalls nicht -
      ohne knappe Plaetze kommt ohnehin jeder Trade zum Zug.

    Erst die Kombination erzeugt versteckten Zustand: bei drei Plaetzen fuer
    24 Symbole entscheidet die Position in der Symboldatei, wer handelt.
    """
    pfad = os.path.join(strategie_dir, "equity_simulation.py")
    sortierung = _ersetze(
        pfad,
        '    return combined.sort_values(["entry_time", "symbol", "exit_time"], '
        'kind="stable").reset_index(drop=True)',
        "    import multi_symbol_optimise as _mso\n"
        "    _rang = {s: i for i, s in enumerate(_mso.SYMBOLS)}\n"
        '    combined = combined.assign(_datei_rang=combined["symbol"].map(_rang))\n'
        '    return combined.sort_values(["entry_time", "_datei_rang"], '
        'kind="stable").reset_index(drop=True)')
    limit = _ersetze(
        pfad,
        "    result = simulate_portfolio(trades, STARTING_CAPITAL, "
        "ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)",
        "    MAX_CONCURRENT_POSITIONS = 3\n"
        "    result = simulate_portfolio(trades, STARTING_CAPITAL, "
        "ALLOCATION_PCT, MAX_CONCURRENT_POSITIONS)")
    return sortierung and limit


def reihenfolge_verschlucken(strategie_dir: str) -> bool:
    """Eine Kopie, die die Permutation ignoriert: sie laeuft ihre Symbole
    immer alphabetisch durch. Damit rechnet das Werkzeug N-mal dasselbe."""
    pfad = os.path.join(strategie_dir, "multi_symbol_optimise.py")
    return _ersetze(pfad, "    for symbol in SYMBOLS:\n",
                    "    for symbol in sorted(SYMBOLS):\n")


def messe(ordner: str, perms: int = 4, bot: str = VORLAGE, seed: int = 4711,
          voll: bool = True) -> dict:
    """Ruft das Werkzeug so auf, wie ein Mensch es aufrufen wuerde - als
    eigenen Prozess ueber die Kommandozeile, gegen den temporaeren Baum."""
    befehl = [sys.executable, os.path.join(_SHARED_DIR, "determinismus_lauf.py"),
              bot, "--perms", str(perms), "--seed", str(seed), "--basis", ordner]
    if voll:
        befehl.append("--voll")
    kind = subprocess.run(befehl, capture_output=True, text=True, cwd=BASE_DIR)
    for zeile in reversed(kind.stdout.splitlines()):
        if zeile.startswith(dl.META_PREFIX):
            return json.loads(zeile[len(dl.META_PREFIX):])
    return {"urteil": d.UNKLAR,
            "fehler": [f"kein Bericht (rc={kind.returncode})",
                       (kind.stderr or kind.stdout)[-800:]]}


# ===========================================================================
# Abschnitt 1 - der Vergleichskern, ohne Bot
# ===========================================================================
def abschnitt1(p: Protokoll):
    import pandas as pd

    # Permutationen: Lauf 0 ist die Originalreihenfolge, gleicher Startwert
    # liefert dieselbe Folge, anderer eine andere.
    basis = [f"S{i:02d}" for i in range(12)]
    a = dl.permutationen(basis, 6, seed=1)
    b = dl.permutationen(basis, 6, seed=1)
    c = dl.permutationen(basis, 6, seed=2)
    p.pruefe("Abschnitt 1", "Lauf 0 ist die unveraenderte Originalreihenfolge",
             a[0] == basis, f"{a[0][:4]}")
    p.pruefe("Abschnitt 1", "gleicher Startwert -> dieselbe Permutationsfolge",
             a == b)
    p.pruefe("Abschnitt 1", "anderer Startwert -> andere Permutationsfolge",
             a[1:] != c[1:])
    p.pruefe("Abschnitt 1", "jede Permutation enthaelt dieselben Symbole",
             all(sorted(x) == sorted(basis) for x in a))
    p.pruefe("Abschnitt 1", "die Permutationen sind nicht alle gleich",
             len({tuple(x) for x in a}) > 1)

    # Fingerabdruck: reagiert er auf einen einzigen geaenderten Wert?
    trades = pd.DataFrame({
        "symbol": ["AAA", "BBB"],
        "entry_time": pd.to_datetime(["2020-01-01", "2020-01-01"]),
        "exit_time": pd.to_datetime(["2020-01-05", "2020-01-06"]),
        "pnl_pct": [1.0, 2.0],
    })
    gedreht = trades.iloc[::-1].reset_index(drop=True)
    geaendert = trades.copy()
    geaendert.loc[1, "pnl_pct"] = 2.000001

    fp = lambda df: dl._fingerabdruck(sorted(dl.signalzeilen(df)))
    p.pruefe("Abschnitt 1", "Fingerabdruck ignoriert die blosse Zeilenreihenfolge",
             fp(trades) == fp(gedreht))
    p.pruefe("Abschnitt 1", "Fingerabdruck schlaegt bei EINEM geaenderten Wert an",
             fp(trades) != fp(geaendert))

    # Und die Gegenprobe zur Gegenprobe: ein Fingerabdruck, der immer gleich
    # waere, bestuende die vorige Pruefung nicht. Hier wird gezeigt, dass er
    # auch auf ein fehlendes UND auf ein zusaetzliches Symbol reagiert.
    p.pruefe("Abschnitt 1", "Fingerabdruck schlaegt bei einem fehlenden Trade an",
             fp(trades) != fp(trades.iloc[:1]))

    # Zaehlwerk und Kapitalpfad
    kurve = pd.DataFrame({
        "time": pd.to_datetime(["2020-01-05", "2020-01-06"]),
        "symbol": ["AAA", "BBB"], "pnl_pct": [1.0, 2.0],
        "allocation": [100.0, 100.0], "capital_after": [10100.0, 10300.0]})
    p.pruefe("Abschnitt 1", "Kapitalpfad achtet AUF die Reihenfolge",
             dl._fingerabdruck(dl.kapitalpfadzeilen(kurve))
             != dl._fingerabdruck(dl.kapitalpfadzeilen(kurve.iloc[::-1])))
    p.pruefe("Abschnitt 1", "ausgefuehrte Trades ignorieren die Reihenfolge",
             dl._fingerabdruck(sorted(dl.kurvenschluessel(kurve)))
             == dl._fingerabdruck(sorted(dl.kurvenschluessel(kurve.iloc[::-1]))))
    p.pruefe("Abschnitt 1", "Multimenge: zwei gleiche Trades zaehlen doppelt",
             dl.zaehlwerk([("A", "t", 1.0), ("A", "t", 1.0)]) == {("A", "t", 1.0): 2})

    # Der Tupel-Vergleich des Zwischenspeichers - drei der neun Bots legen
    # (DataFrame, Stichtag) ab statt eines DataFrames.
    stichtag = pd.Timestamp("2020-01-01")
    p.pruefe("Abschnitt 1", "Speichervergleich kommt mit (DataFrame, Stichtag) zurecht",
             dl.Symbolspeicher._gleich((trades, stichtag), (trades.copy(), stichtag)))
    p.pruefe("Abschnitt 1", "Speichervergleich sieht einen geaenderten Stichtag",
             not dl.Symbolspeicher._gleich((trades, stichtag),
                                            (trades, pd.Timestamp("2021-01-01"))))
    p.pruefe("Abschnitt 1", "Speichervergleich sieht einen geaenderten Kurs",
             not dl.Symbolspeicher._gleich(trades, geaendert))
    p.pruefe("Abschnitt 1", "Speichervergleich: zwei fehlende Stichtage sind gleich",
             dl.Symbolspeicher._gleich((trades, pd.NaT), (trades, pd.NaT)))

    # Die Ladeordnungs-Wache
    p.pruefe("Abschnitt 1", "Wache schweigt, wenn die Reihenfolge ankommt",
             dl._ladeordnung_pruefen(["A", "B", "C"], ["A", "B", "C"]) == "")
    p.pruefe("Abschnitt 1", "Wache schweigt, wenn ein Symbol keine Daten hat",
             dl._ladeordnung_pruefen(["A", "B", "C"], ["A", "C"]) == "")
    p.pruefe("Abschnitt 1", "Wache schlaegt an, wenn die Reihenfolge NICHT ankommt",
             dl._ladeordnung_pruefen(["C", "B", "A"], ["A", "B", "C"]) != "")


# ===========================================================================
# Abschnitt 2 bis 5 - das Werkzeug an echtem Bot-Code
# ===========================================================================
def abschnitt2_5(p: Protokoll, perms: int):
    # --- 2 + 3: die unveraenderte Kopie -----------------------------------
    with tempfile.TemporaryDirectory(prefix="determinismus_kopie_") as ordner:
        strategie = baue_kopie(ordner)
        p.pruefe("Abschnitt 2", "Mitschrift in die Kopie eingebaut",
                 mitschrift_einbauen(strategie, ordner))
        befund = messe(ordner, perms=perms)

        # --- der Ablauf, nicht das Ergebnis
        pfad = os.path.join(ordner, MITSCHRIFT)
        gesehen = []
        if os.path.exists(pfad):
            with open(pfad) as f:
                gesehen = [z.strip().split(",") for z in f if z.strip()]

        p.pruefe("Abschnitt 2", f"der Bot wurde {perms}-mal aufgerufen",
                 len(gesehen) == perms, f"{len(gesehen)}")
        p.pruefe("Abschnitt 2", "jeder Aufruf sah dieselbe Symbolmenge",
                 bool(gesehen) and all(sorted(g) == sorted(gesehen[0]) for g in gesehen))
        p.pruefe("Abschnitt 2", "die Reihenfolgen waren verschieden",
                 len({tuple(g) for g in gesehen}) == perms,
                 f"{len({tuple(g) for g in gesehen})} verschiedene")
        p.pruefe("Abschnitt 2", "der erste Aufruf sah die Originalreihenfolge",
                 bool(gesehen) and gesehen[0] == list(_originalliste()),
                 f"{gesehen[0][:3] if gesehen else '-'}")

        # Haengen die Permutationen ueberhaupt am Startwert? Seit TB-26 laesst
        # sich das NICHT mehr am Ergebnis ablesen - der Bot liefert unter
        # jeder Reihenfolge dasselbe. Also wird es dort geprueft, wo es
        # sichtbar ist: an den tatsaechlich gesehenen Reihenfolgen.
        messe(ordner, perms=perms, seed=4712)
        with open(pfad) as f:
            alle = [z.strip().split(",") for z in f if z.strip()]
        zweiter_block = alle[perms:]
        p.pruefe("Abschnitt 2", "ein anderer Startwert liefert andere Permutationen",
                 len(zweiter_block) == perms
                 and [tuple(g) for g in zweiter_block] != [tuple(g) for g in gesehen],
                 f"{len(zweiter_block)} Aufrufe im zweiten Block")
        p.pruefe("Abschnitt 2",
                 "auch beim anderen Startwert ist Lauf 0 die Originalreihenfolge",
                 bool(zweiter_block) and zweiter_block[0] == list(_originalliste()))

        # --- Abschnitt 3: die Zusicherung von TB-26, an echtem Bot-Code
        p.pruefe("Abschnitt 3", f"{VORLAGE} unveraendert: KEIN Befund",
                 befund.get("urteil") == d.DETERMINISTISCH,
                 f"{befund.get('urteil')} / {befund.get('ursache')} / "
                 f"{befund.get('fehler')}")
        p.pruefe("Abschnitt 3", "die Signalmenge selbst ist identisch",
                 (befund.get("vergleich") or {}).get("signalmenge_identisch") is True)
        p.pruefe("Abschnitt 3", "auch der Kapitalpfad ist Zeile fuer Zeile gleich",
                 (befund.get("vergleich") or {}).get("kapitalpfad_identisch") is True)
        p.pruefe("Abschnitt 3", "kein Trade ist umstritten",
                 (befund.get("umstrittene_trades") or {}).get("umstritten") == 0,
                 str((befund.get("umstrittene_trades") or {}).get("anteil_pct")))
        # Ohne das waere der gruene Befund wertlos: ein Bot, bei dem nie ein
        # Platz knapp wird, ist trivialerweise reihenfolgeunabhaengig. Erst
        # wenn das Limit wirklich bindet, sagt "kein Befund" etwas ueber die
        # Zuteilung aus.
        p.pruefe("Abschnitt 3", "und das Positionslimit hat trotzdem gebunden",
                 ((befund.get("positionslimit") or {}).get("limit_erreicht_in_laeufen")
                  or 0) > 0,
                 str(befund.get("positionslimit")))

    # --- 4: dieselbe Kopie, gehaertet -> die Gegenprobe --------------------
    with tempfile.TemporaryDirectory(prefix="determinismus_gruen_") as ordner:
        strategie = baue_kopie(ordner)
        misslungen = haerten(strategie)
        p.pruefe("Abschnitt 4", "alle drei Haertungen sitzen im Code",
                 not misslungen, ", ".join(misslungen))
        befund = messe(ordner, perms=perms)
        p.pruefe("Abschnitt 4",
                 "gehaerteter Bot: KEIN Befund (der Test kann auch gruen)",
                 befund.get("urteil") == d.DETERMINISTISCH,
                 f"{befund.get('urteil')} / {befund.get('ursache')} / "
                 f"{befund.get('fehler')}")
        p.pruefe("Abschnitt 4", "auch der Kapitalpfad ist Zeile fuer Zeile gleich",
                 (befund.get("vergleich") or {}).get("kapitalpfad_identisch") is True)
        p.pruefe("Abschnitt 4", "kein Trade ist umstritten",
                 (befund.get("umstrittene_trades") or {}).get("umstritten") == 0)
        p.pruefe("Abschnitt 4", "die Rendite ist ueber alle Permutationen dieselbe",
                 ((befund.get("streuung") or {}).get("rendite_pct") or {})
                 .get("verschiedene_werte") == 1)

    # --- 5: derselbe Bot, nur die Zuteilung zurueckgedreht -----------------
    with tempfile.TemporaryDirectory(prefix="determinismus_mutante_") as ordner:
        strategie = baue_kopie(ordner)
        eingebaut = zuteilung_zurueckdrehen(strategie)
        p.pruefe("Abschnitt 5", "der kuenstliche Fehler sitzt im Code",
                 eingebaut, f"eingebaut={eingebaut}")
        befund = messe(ordner, perms=perms)
        p.pruefe("Abschnitt 5",
                 "Zuteilung nach Dateireihenfolge: Befund gemeldet",
                 befund.get("urteil") == d.NICHT,
                 f"{befund.get('urteil')} / {befund.get('fehler')}")
        p.pruefe("Abschnitt 5", "als Ursache die Zuteilung benannt",
                 "Zuteilung" in (befund.get("ursache") or ""),
                 str(befund.get("ursache")))
        p.pruefe("Abschnitt 5",
                 "die Signalmenge ist weiterhin identisch - NUR die Auswahl schwankt",
                 (befund.get("vergleich") or {}).get("signalmenge_identisch") is True
                 and (befund.get("vergleich") or {}).get("ausgefuehrte_trades_identisch")
                 is False)


def _originalliste() -> list:
    """Die Symbolliste, wie der Vorlagen-Bot sie ohne Zutun sieht."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_symbols_config_lesen", os.path.join(_SHARED_DIR, "symbols_config.py"))
    modul = importlib.util.module_from_spec(spec)
    sys.path.insert(0, _SHARED_DIR)
    spec.loader.exec_module(modul)
    return list(modul.SYMBOLS)


# ===========================================================================
# Abschnitt 6 - die falsche Entwarnung
# ===========================================================================
def abschnitt6(p: Protokoll, perms: int):
    with tempfile.TemporaryDirectory(prefix="determinismus_taub_") as ordner:
        strategie = baue_kopie(ordner)
        haerten(strategie)          # sonst wuerde schon die Zuteilung anschlagen
        p.pruefe("Abschnitt 6", "die Kopie ignoriert die Reihenfolge (eingebaut)",
                 reihenfolge_verschlucken(strategie))
        befund = messe(ordner, perms=perms)
        p.pruefe("Abschnitt 6",
                 "Permutation kommt nicht an -> UNKLAR, nicht DETERMINISTISCH",
                 befund.get("urteil") == d.UNKLAR, str(befund.get("urteil")))
        p.pruefe("Abschnitt 6", "und die Begruendung benennt die Reihenfolge",
                 any("Reihenfolge" in f for f in (befund.get("fehler") or [])),
                 str(befund.get("fehler"))[:200])


# ===========================================================================
# Abschnitt 7 - Reproduzierbarkeit und Rueckgabewert am echten Bot
# ===========================================================================
def abschnitt7(p: Protokoll):
    # Der guenstigste echte Bot, zweimal mit demselben Startwert.
    erst = messe(BASE_DIR, perms=3, bot="rsi2_crypto", seed=99, voll=True)
    zweit = messe(BASE_DIR, perms=3, bot="rsi2_crypto", seed=99, voll=True)
    fp = lambda b: [(l["signal_fp"], l["ausgefuehrt_fp"], l["kapitalpfad_fp"])
                    for l in b.get("laeufe", [])]
    p.pruefe("Abschnitt 7", "zwei Laeufe mit gleichem Startwert sind identisch",
             bool(fp(erst)) and fp(erst) == fp(zweit))
    p.pruefe("Abschnitt 7", "der Zwischenspeicher aendert das Ergebnis nicht",
             fp(erst) == fp(messe(BASE_DIR, perms=3, bot="rsi2_crypto",
                                   seed=99, voll=False)))

    # Seit TB-26 muss ein anderer Startwert am ERGEBNIS nichts mehr aendern -
    # die Permutationen sind andere, der Bot rechnet aber unter jeder
    # Reihenfolge dasselbe. Dass die Permutationen selbst wirklich andere
    # sind, prueft Abschnitt 2 am Ablauf; hier waere es nicht sichtbar.
    anders = messe(BASE_DIR, perms=3, bot="rsi2_crypto", seed=100, voll=True)
    p.pruefe("Abschnitt 7",
             "ein anderer Startwert aendert das Ergebnis nicht mehr (TB-26)",
             bool(fp(erst)) and fp(erst) == fp(anders))

    # Pflicht-Gegencheck: rechnet dieses Werkzeug dasselbe wie der Bot?
    # Lauf 0 laeuft in der unveraenderten Originalreihenfolge - er MUSS
    # deshalb die Kurve treffen, die der Bot selbst erzeugt. Trifft er sie
    # nicht, misst das Werkzeug etwas anderes als den Backtest des Bots, und
    # jede Streuungszahl daraus waere wertlos.
    #
    # Verglichen wird gegen einen FRISCHEN Lauf des Bots (ueber
    # `shared/kurven_lauf.py`, denselben Weg, den `shared/ergebniskurven.py`
    # geht) und nicht mehr gegen `results/rsi2_crypto/equity_curve.csv`. Die
    # abgelegten Kurven stammen von VOR TB-26 und beschreiben die alte
    # Zuteilung; `shared/ergebniskurven.py` meldet sie bis zu ihrer
    # Neuerzeugung zu Recht als ABWEICHEND. Ein Test, der eine bewusst
    # veraltete Datei als Wahrheit nimmt, misst das Alter der Datei und nicht
    # das Werkzeug.
    import pandas as pd
    lauf0 = erst.get("laeufe", [{}])[0]
    with tempfile.TemporaryDirectory(prefix="determinismus_botkurve_") as ziel:
        lauf = subprocess.run(
            [sys.executable, os.path.join(_SHARED_DIR, "kurven_lauf.py"),
             "rsi2_crypto", ziel], capture_output=True, text=True, cwd=BASE_DIR)
        kurvenpfad = os.path.join(ziel, "equity_curve.csv")
        if not os.path.exists(kurvenpfad):
            p.pruefe("Abschnitt 7", "der Bot liess sich zum Vergleich laufen",
                     False, (lauf.stderr or lauf.stdout)[-300:])
        else:
            kurve = pd.read_csv(kurvenpfad)
            p.pruefe("Abschnitt 7",
                     "Lauf 0 trifft die Kurve, die der Bot selbst erzeugt",
                     len(kurve) == lauf0.get("trades_ausgefuehrt")
                     and abs(float(kurve["capital_after"].iloc[-1])
                             - float(lauf0.get("endkapital", 0))) < 0.005,
                     f"{len(kurve)} Zeilen / {kurve['capital_after'].iloc[-1]} gegen "
                     f"{lauf0.get('trades_ausgefuehrt')} / {lauf0.get('endkapital')}")

    # Rueckgabewert des Gesamtprogramms: 0, wenn nichts zu melden ist - das
    # ist seit TB-26 der Normalfall und zugleich die Zusicherung dieser
    # Aufgabe, hier am Gesamtprogramm statt am Hilfsprogramm gemessen.
    lauf = subprocess.run(
        [sys.executable, os.path.join(_SHARED_DIR, "determinismus.py"),
         "--bot", "rsi2_crypto", "--perms", "3"],
        capture_output=True, text=True, cwd=BASE_DIR)
    p.pruefe("Abschnitt 7", "Rueckgabewert 0, wenn kein Befund vorliegt",
             lauf.returncode == 0, f"rc={lauf.returncode}")
    p.pruefe("Abschnitt 7", "der Bericht nennt Bot und Urteil",
             "rsi2_crypto" in lauf.stdout and d.DETERMINISTISCH in lauf.stdout)

    # ... und 1, wenn einer vorliegt. Ein Programm, das nur noch gruen kann,
    # waere keine Messung mehr. Geprueft an der Kopie mit zurueckgedrehter
    # Zuteilung - am echten Bot gibt es diesen Fall nicht mehr.
    with tempfile.TemporaryDirectory(prefix="determinismus_rc1_") as ordner:
        strategie = baue_kopie(ordner)
        p.pruefe("Abschnitt 7", "Zuteilung in der Kopie zurueckgedreht",
                 zuteilung_zurueckdrehen(strategie))
        lauf = subprocess.run(
            [sys.executable, os.path.join(_SHARED_DIR, "determinismus.py"),
             "--bot", VORLAGE, "--perms", "3", "--voll", "--basis", ordner],
            capture_output=True, text=True, cwd=BASE_DIR)
        p.pruefe("Abschnitt 7", "Rueckgabewert 1 bei Befund (fuer den Cronjob)",
                 lauf.returncode == 1, f"rc={lauf.returncode}")
        p.pruefe("Abschnitt 7", "der Bericht nennt den Befund",
                 VORLAGE in lauf.stdout and d.NICHT in lauf.stdout)

    # Ein unbekannter Bot ist ein Aufruffehler (2), kein stilles Gruen.
    lauf = subprocess.run(
        [sys.executable, os.path.join(_SHARED_DIR, "determinismus.py"),
         "--bot", "gibt_es_nicht"], capture_output=True, text=True, cwd=BASE_DIR)
    p.pruefe("Abschnitt 7", "unbekannter Bot -> Rueckgabewert 2",
             lauf.returncode == 2, f"rc={lauf.returncode}")


# ===========================================================================
# Abschnitt 8 - der Test und das Werkzeug veraendern nichts
# ===========================================================================
BEOBACHTET = ("strategies/", "results/", "data/", "shared/", "config/",
              "logs/", "paper_trading_")


def git_zustand() -> str:
    lauf = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                          capture_output=True, text=True)
    return "\n".join(sorted(z for z in lauf.stdout.splitlines()
                            if z[3:].strip('"').startswith(BEOBACHTET)))


def _dateizustand(pfade: list) -> dict:
    stand = {}
    for pfad in pfade:
        if os.path.exists(pfad):
            s = os.stat(pfad)
            stand[pfad] = (s.st_size, s.st_mtime_ns)
    return stand


def abschnitt8(p: Protokoll, vorher_git: str, vorher_dateien: dict):
    p.pruefe("Abschnitt 8", "git status unveraendert (nichts ins Repo geschrieben)",
             vorher_git == git_zustand(),
             f"vorher:\n{vorher_git}\nnachher:\n{git_zustand()}")
    nachher = _dateizustand(list(vorher_dateien))
    abweichend = [k for k in vorher_dateien if nachher.get(k) != vorher_dateien[k]]
    p.pruefe("Abschnitt 8",
             "Symbollisten und abgelegte Ergebniskurven unberuehrt (Groesse und Zeitstempel)",
             not abweichend, ", ".join(abweichend))


def _ueberwachte_dateien() -> list:
    pfade = [os.path.join(BASE_DIR, "config", n) for n in
             ("sp500_top150.txt", "sp500_top50.txt", "sp500_top25.txt",
              "top25_symbols.txt")]
    pfade.append(os.path.join(BASE_DIR, "results", "equity_curve.csv"))
    for bot in d.finde_bots():
        pfade.append(os.path.join(BASE_DIR, "results", bot, "equity_curve.csv"))
        pfade.append(os.path.join(BASE_DIR, "results", bot,
                                  "multi_symbol_optimisation_results.csv"))
    return pfade


# ===========================================================================
def main() -> int:
    schnell = "--schnell" in sys.argv
    perms = 3 if schnell else 4
    vorher_git = git_zustand()
    vorher_dateien = _dateizustand(_ueberwachte_dateien())
    p = Protokoll()

    print("=" * 78)
    print("SELBSTTESTS: Determinismus-Pruefung (TB-23)")
    print("=" * 78)

    print("\n--- Abschnitt 1: Vergleichskern (Permutation, Fingerabdruck, Wache) ---")
    abschnitt1(p)

    if schnell:
        print("\n  (Abschnitt 2-7 uebersprungen: --schnell)")
    else:
        print(f"\n--- Abschnitt 2-5: echtes Bot-Bild ({VORLAGE}-Kopie, {perms} "
              f"Permutationen) ---")
        abschnitt2_5(p, perms)

        print("\n--- Abschnitt 6: die falsche Entwarnung ---")
        abschnitt6(p, perms)

        print("\n--- Abschnitt 7: Reproduzierbarkeit und Rueckgabewerte ---")
        abschnitt7(p)

    print("\n--- Abschnitt 8: der Test selbst veraendert nichts ---")
    abschnitt8(p, vorher_git, vorher_dateien)

    print("\n" + "=" * 78)
    print(f"Ergebnis: {p.ok} bestanden, {len(p.fehler)} fehlgeschlagen")
    for f in p.fehler:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if p.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
