"""
Selbsttests der neun live_params.py - Werte und Kommentar-Behauptungen
======================================================================
Ohne Test-Framework, wie in allen Pruefungen dieses Projekts.

Warum diese Datei existiert (Befund TB-17, 2026-09-13): `live_params.py`
ist die einzige Quelle jedes Handelsparameters (CLAUDE.md) und wird
"nie automatisch veraendert". Eine Dokumentations-Korrektur in einer
dieser Dateien ist damit ein Eingriff an der empfindlichsten Stelle des
Projekts - und ein Blick in den Diff ist als Zusicherung zu schwach: er
zeigt, was jemand geaendert hat, nicht, was dabei herausgekommen ist.

Die drei Pruefungen:

  1) WERTETABELLE - alle 61 Konstanten aller NEUN Bots stehen unten als
     erwarteter Sollwert. Das ist die eigentliche Zusicherung: aendert
     eine Kommentar-Korrektur versehentlich eine Zahl, schlaegt das hier
     an, und zwar beim betroffenen Bot NAMENTLICH.
  2) REIN DEKLARATIV - die Dateien duerfen nur Zuweisungen enthalten.
     Kein Import, kein Funktionsaufruf, keine Funktion, keine
     Verzweigung. Damit kann sich in einer "Nur-Kommentar"-Aenderung
     auch keine Logik einschleichen, die die Wertetabelle umgeht.
  3) BUY-AND-HOLD-BEHAUPTUNGEN - eine Aussage ueber Buy-and-Hold mit
     einer Prozentzahl muss im selben Historien-Eintrag entweder eine
     Quelle unter research/ bzw. results/ nennen oder als
     zurueckgezogen gekennzeichnet sein. Genau diese Fehlerklasse hat
     TB-17 ausgeloest. Reichweite und Grenzen: siehe Kommentar bei
     `behauptungen_pruefen`.

Die Sollwerte stammen aus dem Stand von `main` vor der TB-17-Korrektur
(PR #88, Commit 74d4f55) und wurden per AST aus den Dateien gelesen,
nicht abgeschrieben.

Nutzung:  python3 shared/test_live_params_werte.py
"""

import ast
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(DIR)

BOTS = [
    "elliott_wave",
    "elliott_wave_stocks",
    "rsi2_crypto",
    "rsi2_mean_reversion",
    "t3_supertrend",
    "turtle_soup_crypto",
    "turtle_soup_stocks",
    "volatility_breakout",
    "volatility_breakout_crypto",
]

# ---------------------------------------------------------------------------
# Die Sollwerte. Bewusst vollstaendig und wortwoertlich ausgeschrieben statt
# aus einer Referenzdatei gelesen: eine Referenzdatei koennte mitwandern,
# diese Tabelle nicht. Wer hier etwas aendert, aendert einen Handelsparameter
# und muss das begruenden - sie ist die Bremse, nicht die Buchhaltung.
#
# LAST_UPDATED steht bewusst MIT drin: der Wert bezeichnet den Stand der
# Parameter und wird in research/pnl_2025_fixed_size/extract.py ausgewertet.
# Eine reine Dokumentations-Aenderung darf ihn also gerade NICHT anfassen.
# ---------------------------------------------------------------------------
SOLLWERTE = {
    "elliott_wave": {
        "DEVIATION_PCT": 10.0,
        "STOP_LOSS_PCT": 6.0,
        "TAKE_PROFIT_FIB": 0.618,
        "LAST_UPDATED": "2026-09-07",
    },
    "elliott_wave_stocks": {
        "DEVIATION_PCT": 5.0,
        "STOP_LOSS_PCT": 3.0,
        "TAKE_PROFIT_FIB": 0.236,
        "USE_TAKE_PROFIT": False,
        "MAX_CONCURRENT_POSITIONS": 8,
        "LAST_UPDATED": "2026-09-03",
    },
    "rsi2_crypto": {
        "SMA_TREND_FILTER": 150,
        "RSI_THRESHOLD": 10.0,
        "STOP_LOSS_PCT": None,
        "ALLOCATION_PCT": 10,
        "MAX_CONCURRENT_POSITIONS": 8,
        "MAX_HOLD_DAYS": 10,
        "LAST_UPDATED": "2026-09-03",
    },
    "rsi2_mean_reversion": {
        "RSI_THRESHOLD": 5.0,
        "STOP_LOSS_PCT": None,
        "MAX_HOLD_DAYS": 10,
        "ALLOCATION_PCT": 5,
        "MAX_CONCURRENT_POSITIONS": 20,
        "LAST_UPDATED": "2026-09-03",
    },
    "t3_supertrend": {
        "T3_FAST_LENGTH": 16,
        "T3_SLOW_LENGTH": 30,
        "ADX_THRESHOLD": 20.0,
        "STOP_LOSS_PCT": 4.0,
        "MAX_CONCURRENT_POSITIONS": 5,
        "T3_FACTOR": 0.7,
        "DI_LENGTH": 14,
        "ADX_LENGTH": 14,
        "ATR_LENGTH": 22,
        "ATR_MULT": 3.0,
        "LAST_UPDATED": "2026-08-31",
    },
    "turtle_soup_crypto": {
        "DONCHIAN_PERIOD": 10,
        "STOP_MODE": "structural",
        "MAX_HOLD_DAYS": 10,
        "ALLOCATION_PCT": 10,
        "MAX_CONCURRENT_POSITIONS": 8,
        "LAST_UPDATED": "2026-09-04",
    },
    "turtle_soup_stocks": {
        "DONCHIAN_PERIOD": 10,
        "STOP_MODE": None,
        "MAX_HOLD_DAYS": 10,
        "ALLOCATION_PCT": 2,
        "MAX_CONCURRENT_POSITIONS": None,
        "LAST_UPDATED": "2026-09-04",
    },
    "volatility_breakout": {
        "BB_SQUEEZE_PERCENTILE": 25.0,
        "BB_LOOKBACK": 126,
        "STOP_LOSS_PCT": 8.0,
        "MAX_HOLD_DAYS": 15,
        "ALLOCATION_PCT": 10,
        "MAX_CONCURRENT_POSITIONS": 15,
        "LAST_UPDATED": "2026-09-03",
    },
    "volatility_breakout_crypto": {
        "BB_SQUEEZE_PERCENTILE": 25.0,
        "BB_LOOKBACK": 126,
        "STOP_LOSS_PCT": 5.0,
        "MAX_HOLD_DAYS": 15,
        "BTC_REGIME_FILTER_ENABLED": True,
        "ALLOCATION_PCT": 10,
        "MAX_CONCURRENT_POSITIONS": 8,
        "LAST_UPDATED": "2026-09-04",
    },
}

CHECKS = []
FEHLER = []


def check(name, ok, detail=""):
    CHECKS.append(bool(ok))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        FEHLER.append(f"{name}   {detail}")


def pfad_von(bot):
    return os.path.join(REPO_ROOT, "strategies", bot, "live_params.py")


def quelle_von(bot):
    with open(pfad_von(bot), encoding="utf-8") as f:
        return f.read()


def konstanten(quelltext):
    """Liest die Zuweisungen auf Modulebene per AST aus.

    Bewusst AST und nicht `import`: ein Import wuerde den Modulcode
    ausfuehren. Diese Dateien tun nichts, aber eine Pruefung, die das
    voraussetzt, kann es nicht mehr feststellen (Pruefung 2).
    """
    werte = {}
    for knoten in ast.parse(quelltext).body:
        if not isinstance(knoten, ast.Assign):
            continue
        for ziel in knoten.targets:
            if isinstance(ziel, ast.Name):
                werte[ziel.id] = ast.literal_eval(knoten.value)
    return werte


# ---------------------------------------------------------------------------
def teste_wertetabelle():
    print("\n1) Wertetabelle: alle Konstanten aller neun Bots unveraendert")
    gesamt = 0
    for bot in BOTS:
        ist = konstanten(quelle_von(bot))
        soll = SOLLWERTE[bot]
        gesamt += len(soll)

        fehlend = sorted(set(soll) - set(ist))
        check(f"{bot}: keine Konstante verschwunden", not fehlend, f"fehlt: {fehlend}")

        neu = sorted(set(ist) - set(soll))
        check(f"{bot}: keine Konstante hinzugekommen", not neu, f"neu: {neu}")

        abweichend = [
            f"{name}: soll {soll[name]!r}, ist {ist[name]!r}"
            for name in sorted(soll)
            if name in ist and (ist[name] != soll[name] or type(ist[name]) is not type(soll[name]))
        ]
        check(f"{bot}: alle {len(soll)} Werte exakt wie erwartet",
              not abweichend, "; ".join(abweichend))

    check(f"insgesamt {gesamt} Konstanten geprueft", gesamt == 61, f"gezaehlt: {gesamt}")


# ---------------------------------------------------------------------------
def teste_rein_deklarativ():
    print("\n2) Rein deklarativ: keine Logik in einer live_params.py")
    for bot in BOTS:
        quelle = quelle_von(bot)
        baum = ast.parse(quelle)

        erlaubt = []
        for knoten in baum.body:
            if isinstance(knoten, ast.Assign):
                continue
            # Der Modul-Docstring ist ein Expr-Knoten mit Konstante.
            if isinstance(knoten, ast.Expr) and isinstance(knoten.value, ast.Constant):
                continue
            erlaubt.append(type(knoten).__name__)
        check(f"{bot}: nur Zuweisungen und Docstring auf Modulebene",
              not erlaubt, f"gefunden: {erlaubt}")

        # Jeder zugewiesene Wert muss ein reines Literal sein. Damit ist
        # ausgeschlossen, dass ein Parameter kuenftig berechnet wird -
        # genau das wuerde die Wertetabelle oben aushebeln.
        nicht_literal = []
        for knoten in baum.body:
            if not isinstance(knoten, ast.Assign):
                continue
            try:
                ast.literal_eval(knoten.value)
            except (ValueError, SyntaxError, TypeError):
                ziele = [z.id for z in knoten.targets if isinstance(z, ast.Name)]
                nicht_literal.extend(ziele)
        check(f"{bot}: jeder Wert ist ein Literal, nichts wird gerechnet",
              not nicht_literal, f"gefunden: {nicht_literal}")

        check(f"{bot}: uebersetzt fehlerfrei", compile(quelle, pfad_von(bot), "exec") is not None)


# ---------------------------------------------------------------------------
# Pruefung 3 - Reichweite und Grenzen, bewusst eng gewaehlt:
#
# GEPRUEFT wird eine Zeile, die "Buy-and-Hold" UND eine Prozentzahl traegt.
# Sie muss im selben Historien-Eintrag eine Quelle unter research/ oder
# results/ nennen oder als zurueckgezogen markiert sein.
#
# NICHT GEPRUEFT wird eine Behauptung, die sich ueber einen Zeilenumbruch
# zwischen Wort und Zahl verteilt. Das ist eine bewusste Entscheidung, keine
# Nachlaessigkeit: sechs der neun Dateien nennen Buy-and-Hold nur als Glied
# der Validierungskette ("Backtest -> Walk-Forward -> ... -> Buy-and-Hold ->"),
# und in volatility_breakout/live_params.py folgt zwei Zeilen darunter "8%
# Stop-Loss". Ein Fenster von zwei Zeilen wuerde dort also Alarm schlagen, wo
# gar keine Behauptung steht. Ein Pruefer, der bei sechs von neun Dateien
# grundlos anspringt, wird abgeschaltet - und schuetzt danach nichts mehr.
# Die enge Regel kostet Trennschaerfe und behaelt dafuer ihre Glaubwuerdigkeit.
#
# Ebenfalls NICHT geprueft: ob die Zahl inhaltlich stimmt. Das kann kein
# Textpruefer leisten - dafuer gibt es den Bericht, auf den er zu verweisen
# verlangt.
# ---------------------------------------------------------------------------
QUELLEN_MUSTER = re.compile(r"\b(research|results)/[A-Za-z0-9_./]+")
PROZENT_MUSTER = re.compile(r"[-+]?\d+[.,]?\d*\s*%")
RUECKZUG_MUSTER = re.compile(
    r"ZURUECKGEZOGEN|ueberholt|gilt (?:das )?nicht mehr|gelten nicht mehr|"
    r"Hier stand|hier stand|MIT Look-Ahead",
)
EINTRAG_MUSTER = re.compile(r"^- \d{4}-\d{2}-\d{2}:", re.MULTILINE)


def eintraege(docstring):
    """Zerlegt einen Docstring in Kopf plus einen Block je Historien-Eintrag."""
    grenzen = [m.start() for m in EINTRAG_MUSTER.finditer(docstring)]
    schnitte = [0] + grenzen + [len(docstring)]
    return [docstring[schnitte[i]:schnitte[i + 1]] for i in range(len(schnitte) - 1)]


def behauptungen_pruefen(docstring):
    """Gibt die unbelegten Buy-and-Hold-Behauptungen als Liste zurueck."""
    unbelegt = []
    for block in eintraege(docstring):
        hat_quelle = bool(QUELLEN_MUSTER.search(block))
        ist_zurueckgezogen = bool(RUECKZUG_MUSTER.search(block))
        for zeile in block.splitlines():
            if "Buy-and-Hold" not in zeile:
                continue
            if not PROZENT_MUSTER.search(zeile):
                continue
            if hat_quelle or ist_zurueckgezogen:
                continue
            unbelegt.append(zeile.strip())
    return unbelegt


def teste_behauptungen():
    print("\n3) Buy-and-Hold-Behauptungen sind belegt oder zurueckgezogen")

    for bot in BOTS:
        docstring = ast.get_docstring(ast.parse(quelle_von(bot))) or ""
        unbelegt = behauptungen_pruefen(docstring)
        check(f"{bot}: keine unbelegte Buy-and-Hold-Behauptung",
              not unbelegt, " | ".join(unbelegt))

    # Gegenprobe. Ein Pruefer, der nie anspringt, ist kein Pruefer - die
    # folgenden Faelle zeigen, dass er die Fehlerklasse aus TB-17 wirklich
    # faengt und die unschuldigen Formulierungen wirklich durchlaesst.
    print("\n3b) Gegenprobe am Pruefer selbst")

    tb17 = (
        "Historie:\n"
        "- 2026-09-02: Aktualisiert auf Top 150 Aktien mit Stop-Loss 3% -\n"
        "  schlaegt Buy-and-Hold klar (1458% vs. 756% Rendite,\n"
        "  -1.32% vs. -34.83% Max Drawdown).\n"
    )
    check("der Originalbefund TB-17 wuerde erkannt", len(behauptungen_pruefen(tb17)) == 1,
          str(behauptungen_pruefen(tb17)))

    mit_quelle = tb17 + "  Siehe research/elliott_wave_params/BERICHT.md.\n"
    check("dieselbe Zeile mit Quelle im Eintrag wird durchgelassen",
          behauptungen_pruefen(mit_quelle) == [])

    zurueckgezogen = tb17.replace("schlaegt", "ZURUECKGEZOGEN - hier stand: schlaegt")
    check("als zurueckgezogen markiert wird durchgelassen",
          behauptungen_pruefen(zurueckgezogen) == [])

    kette = ("- 2026-09-03: Erste Live-Uebernahme\n"
             "  (Backtest -> Walk-Forward -> Buy-and-Hold ->\n"
             "  False-Breakout-Filter-Test). 8% Stop-Loss als robusteste\n"
             "  Kombination validiert.\n")
    check("Buy-and-Hold als Glied der Validierungskette loest NICHT aus",
          behauptungen_pruefen(kette) == [], str(behauptungen_pruefen(kette)))

    # Eine Quelle in einem ANDEREN Eintrag darf nicht als Beleg durchgehen -
    # sonst belegt ein beliebiger Bericht irgendwo in der Datei alles.
    fremde_quelle = ("- 2026-09-01: Siehe research/irgendwas/BERICHT.md.\n"
                     "- 2026-09-02: schlaegt Buy-and-Hold klar (1458% vs. 756%).\n")
    check("Quelle aus einem fremden Eintrag belegt nichts",
          len(behauptungen_pruefen(fremde_quelle)) == 1,
          str(behauptungen_pruefen(fremde_quelle)))


# ---------------------------------------------------------------------------
def main():
    print("Selbsttests der neun live_params.py (Befund TB-17)")
    fehlend = [bot for bot in BOTS if not os.path.exists(pfad_von(bot))]
    if fehlend:
        raise SystemExit(f"live_params.py fehlt fuer: {fehlend}")
    if sorted(BOTS) != sorted(SOLLWERTE):
        raise SystemExit("BOTS und SOLLWERTE beschreiben nicht dieselben Bots")

    teste_wertetabelle()
    teste_rein_deklarativ()
    teste_behauptungen()

    if FEHLER:
        print(f"\nFEHLGESCHLAGEN: {len(FEHLER)} von {len(CHECKS)} Pruefungen")
        for zeile in FEHLER:
            print(f"  - {zeile}")
        raise SystemExit(1)
    print(f"\n{len(CHECKS)}/{len(CHECKS)} Pruefungen bestanden.")


if __name__ == "__main__":
    main()
