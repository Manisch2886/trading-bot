"""
Selbsttests von TB-25
====================================================================
Prueft die Behauptungen, auf denen diese Untersuchung steht - jede
einzeln, mit Abbruch beim ersten Fehlschlag.

Der wichtigste Punkt ist der erste: `bedingungen.py` bildet die
Zerlegung des `fib_score` nach. Eine Nachbildung, die abweicht,
beantwortet die Frage nicht. Sie wird deshalb gegen die ECHTE
`elliott_wave_counter.fibonacci_score()` gerechnet - auf jedem
gemessenen Muster UND auf Zufallspunkten.

Nutzung:  python3 test_stufen.py <elliott_wave|elliott_wave_stocks>
"""

import json
import os
import subprocess
import sys

import botenv

BOT = botenv.bot_from_argv()

import numpy as np                                                # noqa: E402
import pandas as pd                                               # noqa: E402

import bedingungen as bd                                          # noqa: E402
import statistik as st                                            # noqa: E402
import auswertung as aus                                          # noqa: E402
import backtest_elliott as bt                                     # noqa: E402
import live_params as lp                                          # noqa: E402
import multi_symbol_optimise as mo                                # noqa: E402
from elliott_wave_counter import fibonacci_score, find_causal_waves   # noqa: E402

CHECKS = []

# Dateien, die diese Untersuchung ausdruecklich NICHT anfassen darf
# (Randbedingungen des Auftrags).
TABU = [
    f"strategies/{BOT}/live_params.py",
    f"strategies/{BOT}/forward_test.py",
    f"strategies/{BOT}/equity_simulation.py",
    f"strategies/{BOT}/multi_symbol_optimise.py",
    f"strategies/{BOT}/elliott_wave_counter.py",
    f"strategies/{BOT}/zigzag_indicator.py",
    f"strategies/{BOT}/backtest_elliott.py",
]


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


def main():
    botenv.print_hinweis()
    print(f"\n{BOT}: Selbsttests\n")
    rng = np.random.default_rng(st.SEED)

    # ---- 1: Nachbildung gegen die echte Bot-Funktion ----------------
    csv_pfad = os.path.join(botenv.RESULTS_DIR, f"{BOT}_muster.csv")
    if not os.path.exists(csv_pfad):
        raise SystemExit(f"{csv_pfad} fehlt - erst 'python3 lauf.py {BOT}' ausfuehren.")
    df = pd.read_csv(csv_pfad)
    punkte = df[[f"wave{i}" for i in range(6)]].to_numpy(dtype=float)

    echt = np.array([fibonacci_score(list(p)) for p in punkte])
    nach = np.array([bd.score_nachbildung(list(p)) for p in punkte])
    check("Nachbildung == fibonacci_score() auf jedem gemessenen Muster",
          np.array_equal(echt, nach), f"{len(punkte)} Muster")
    check("fib_score in der CSV == fibonacci_score() des Bots",
          np.array_equal(echt, df["fib_score"].to_numpy(dtype=float)))
    check("Stufe == Zahl der erfuellten Bedingungen",
          bool((df["stufe"] == df[[f"erf_{n}" for n in bd.NAMEN]].sum(axis=1)).all()))
    check("Stufe aus Punkten == Stufe aus dem Score",
          bool((df["stufe"] == df["fib_score"].map(bd.stufe_aus_score)).all()))

    # Zufallspunkte - auch ausserhalb dessen, was der Bot je erzeugt.
    zufalls = rng.uniform(1.0, 100.0, size=(20000, 6))
    # Ein paar entartete Faelle bewusst dazu (wave1 == 0 bzw. wave3 == 0),
    # weil fibonacci_score() dort vorzeitig mit 0.0 aussteigt.
    zufalls[:200, 1] = zufalls[:200, 0]
    zufalls[200:400, 3] = zufalls[200:400, 2]
    abw = [(list(p), fibonacci_score(list(p)), bd.score_nachbildung(list(p)))
           for p in zufalls if fibonacci_score(list(p)) != bd.score_nachbildung(list(p))]
    check("Nachbildung == fibonacci_score() auf 20 000 Zufallspunkten",
          not abw, f"{len(zufalls)} Punkte, {len(abw)} Abweichungen")

    # ---- 2: Der Wertebereich ist abgeschlossen ----------------------
    moegliche = set()
    for maske in range(8):
        s = 0.0
        for i, (_n, punkte_i, *_r) in enumerate(bd.BEDINGUNGEN):
            if maske >> i & 1:
                s += punkte_i
        moegliche.add(round(s, 2))
    check("fibonacci_score kann nur sechs Werte annehmen",
          moegliche == {0.0, 0.33, 0.34, 0.66, 0.67, 1.0}, str(sorted(moegliche)))
    nur_erste = {round(sum(p for i, (_n, p, *_r) in enumerate(bd.BEDINGUNGEN)
                           if maske >> i & 1), 2)
                 for maske in range(8) if maske & 1}
    check("0,34 und 0,67 setzen die Welle-2-Bedingung zwingend voraus",
          {0.34, 0.67}.issubset(nur_erste)
          and not ({0.33, 0.66} & nur_erste),
          "der Tie-Break bevorzugt also systematisch ein bestimmtes Kriterium")

    # ---- 3: d <= 1 ist gleichbedeutend mit 'erfuellt' ---------------
    fehler = 0
    for p in zufalls[400:5400]:
        d = bd.abstaende(list(p))
        e = bd.erfuellte(list(p))
        if d is None:
            continue
        for i, name in enumerate(bd.NAMEN):
            if (d[name] <= 1.0 + 1e-12) != e[i]:
                fehler += 1
    check("normierter Abstand d <= 1 <=> Bedingung erfuellt", fehler == 0,
          f"{fehler} Abweichungen auf 5 000 Zufallspunkten")
    check("naehe saettigt bei Stufe 0, naehe_weich nicht",
          float(df.loc[df["stufe"] == 0, "naehe"].max() if (df["stufe"] == 0).any() else 0) == 0.0
          and int(df.loc[df["stufe"] == 0, "naehe_weich"].round(10).nunique()
                  if (df["stufe"] == 0).any() else 1) > 1,
          "genau der Grund, warum beide Masse ausgewiesen werden")

    # ---- 4: Kausalitaet - der korrigierte Pfad ----------------------
    ohne_entry_idx = pd.DataFrame([{"direction": "bearish", "end_time": pd.Timestamp("2020-01-01"),
                                    "wave0": 1.0, "wave5": 2.0, "fib_score": 1.0}])
    try:
        bt.run_backtest(pd.DataFrame({"open_time": [pd.Timestamp("2020-01-01")],
                                      "close": [1.0], "high": [1.0], "low": [1.0]}),
                        ohne_entry_idx)
        verweigert = False
    except ValueError:
        verweigert = True
    check("run_backtest verweigert Wellen ohne entry_idx (Look-Ahead-Sperre, PR #26)",
          verweigert, "ein Lauf mit Look-Ahead ist auf diesem Pfad nicht moeglich")
    lauf_meta = json.load(open(os.path.join(botenv.RESULTS_DIR, f"{BOT}_lauf.json")))
    check("Wellen kommen aus find_causal_waves",
          lauf_meta["kausalitaet"]["wellen_funktion"].endswith("find_causal_waves"))
    check("Einstieg zum Schlusskurs des Bestaetigungsbalkens",
          "Bestaetigungsbalken" in lauf_meta["kausalitaet"]["einstieg"])

    # ---- 5: Die Schwellensenkung veraendert die Stufen 1-3 nicht ----
    ident = lauf_meta["identitaet_lauf_a_gegen_b"]
    check("Lauf A (min_fib 0.3) == Stufen 1-3 aus Lauf B (min_fib 0.0), Zeile fuer Zeile",
          ident["zeile_fuer_zeile_identisch"],
          f"{ident['trades_lauf_a_min_fib_0_3']} Trades, "
          f"geprueft auf {len(ident.get('geprueefte_spalten', []))} Spalten")

    # ---- 6: Parameter sind die aus live_params.py -------------------
    p = lauf_meta["parameter"]
    check("gemessen wurde mit den Live-Parametern",
          p["deviation_pct"] == float(lp.DEVIATION_PCT)
          and p["stop_loss_pct"] == float(lp.STOP_LOSS_PCT)
          and p["take_profit_fib"] == float(lp.TAKE_PROFIT_FIB)
          and p["use_take_profit"] == bool(getattr(lp, "USE_TAKE_PROFIT", True)),
          f"dev {p['deviation_pct']} / stop {p['stop_loss_pct']} / "
          f"fib {p['take_profit_fib']} / TP {p['use_take_profit']}")

    # ---- 7: Kursdaten ueber shared/kursdaten.py (PR #81) ------------
    quelle = open(os.path.join(botenv.REPO_ROOT, "strategies", BOT,
                               "multi_symbol_optimise.py")).read()
    check("load_all_symbol_data streicht unvollstaendige Kerzen (shared/kursdaten.py)",
          "entferne_unvollstaendige" in quelle and "from kursdaten import" in quelle)

    # ---- 8: Statistik ----------------------------------------------
    check("Spearman erkennt einen perfekten Zusammenhang",
          abs(st.spearman([1, 2, 3, 4, 5], [10, 20, 30, 40, 50]) - 1.0) < 1e-12)
    check("Spearman ist bindungsfest",
          abs(st.spearman([1, 1, 2, 2], [5, 6, 7, 8]) - 0.894427191) < 1e-6,
          "Durchschnittsraenge statt der 6*d^2-Kurzformel")
    gleich = st.permutation_differenz(np.arange(50.0), np.arange(50.0), ziehungen=2000)
    check("Permutationstest findet bei identischen Gruppen nichts",
          gleich["p_wert"] > 0.5, f"p = {gleich['p_wert']:.3f}")
    klar = st.permutation_differenz(np.arange(50.0) + 100, np.arange(50.0), ziehungen=2000)
    check("Permutationstest findet einen klaren Unterschied",
          klar["p_wert"] < 0.01, f"p = {klar['p_wert']:.4f}")
    a = st.bootstrap_mittelwert(np.arange(100.0))
    b = st.bootstrap_mittelwert(np.arange(100.0))
    check("Bootstrap ist reproduzierbar (fester Seed, eigener Generator)",
          a == b, f"CI [{a['ci_low']:.3f}, {a['ci_high']:.3f}]")
    # Der Cluster-Bootstrap muss dort deutlich BREITER werden, wo die
    # Trades eines Symbols vollstaendig gleichlaufen - dann steckt die
    # ganze Information in der Zahl der Symbole, nicht der Trades. Das
    # ist die Eigenschaft, auf die es ankommt.
    #
    # Nicht geprueft wird, dass er auf den ECHTEN Daten breiter ist: das
    # ist kein Gesetz. Liegt die Streuung mehr INNERHALB der Symbole als
    # ZWISCHEN ihnen, faellt er enger aus - genau das ist beim Krypto-Bot
    # der Fall und steht so im Bericht.
    kuenstlich = np.repeat(np.arange(10.0), 20)          # 10 Symbole a 20 gleiche Trades
    sym = np.repeat([f"S{i}" for i in range(10)], 20)
    breit = st.bootstrap_mittelwert(kuenstlich, cluster=sym)
    eng = st.bootstrap_mittelwert(kuenstlich)
    check("Cluster-Bootstrap wird breiter, wenn Trades eines Symbols gleichlaufen",
          (breit["ci_high"] - breit["ci_low"]) > 3 * (eng["ci_high"] - eng["ci_low"]),
          f"Cluster {breit['ci_high'] - breit['ci_low']:.2f}, "
          f"Trades {eng['ci_high'] - eng['ci_low']:.2f}")
    echt_c = st.bootstrap_mittelwert(df["pnl_pct"].to_numpy(dtype=float),
                                     cluster=df["symbol"].to_numpy())
    echt_t = st.bootstrap_mittelwert(df["pnl_pct"].to_numpy(dtype=float))
    check("beide Intervalle werden auf den echten Daten ausgewiesen",
          echt_c is not None and echt_t is not None,
          f"Cluster {echt_c['ci_high'] - echt_c['ci_low']:.2f} pp, "
          f"Trades {echt_t['ci_high'] - echt_t['ci_low']:.2f} pp")

    # ---- 9: Auswertung ist reproduzierbar ---------------------------
    e1 = json.dumps(aus._z(aus.auswerten(df)), sort_keys=True)
    e2 = json.dumps(aus._z(aus.auswerten(df)), sort_keys=True)
    check("zweimal ausgewertet == dasselbe Ergebnis", e1 == e2)
    abgelegt = json.load(open(os.path.join(botenv.RESULTS_DIR, f"{BOT}_auswertung.json")))
    frisch = json.loads(e1)
    check("abgelegte Auswertung stimmt mit einer frischen ueberein",
          all(json.dumps(abgelegt[k], sort_keys=True) == json.dumps(frisch[k], sort_keys=True)
              for k in frisch),
          "sonst ist die Ergebnisdatei aelter als der Code")

    # ---- 10: Gruppengroessen stehen ueberall dabei ------------------
    check("jede ausgewiesene Gruppe traegt ihre Groesse",
          all("n" in g for g in abgelegt["stufen"])
          and all("n_a" in v and "n_b" in v for v in abgelegt["bedingungen"]))
    check("zu kleine Gruppen sind als solche markiert",
          all(g["aussagekraeftig"] == (g["n"] >= aus.MIN_AUSSAGEKRAEFTIG)
              for g in abgelegt["stufen"]),
          f"Schwelle {aus.MIN_AUSSAGEKRAEFTIG} Trades")

    # ---- 11: Kein Bot-Code veraendert -------------------------------
    status = subprocess.run(["git", "-C", botenv.REPO_ROOT, "status", "--porcelain"],
                            capture_output=True, text=True).stdout
    beruehrt = [z[3:] for z in status.splitlines()
                if not z[3:].startswith(("research/", "docs/"))]
    check("Arbeitsbaum: nichts ausserhalb von research/ und docs/ veraendert",
          not beruehrt, str(beruehrt))
    # DREI Punkte, nicht zwei. `git diff origin/main HEAD` vergleicht die beiden
    # Spitzen und listet deshalb auch alles auf, was MAIN seit dem Abzweig
    # dazubekommen hat - gemessen am 13.09.2026 waren das die Ordner von TB-23
    # und TB-24 samt zweier neuer Dateien unter shared/. Diese Untersuchung hat
    # davon nichts angefasst, die Pruefung schlug trotzdem fehl.
    # `origin/main...HEAD` vergleicht gegen die MERGE-BASIS und beantwortet
    # genau die Frage der Randbedingung: was hat DIESER Zweig geaendert?
    dreipunkt = "origin/main...HEAD"
    diff = subprocess.run(["git", "-C", botenv.REPO_ROOT, "diff", dreipunkt,
                           "--name-only"], capture_output=True, text=True).stdout.split()
    fremd = [f for f in diff if not f.startswith(("research/", "docs/"))]
    check(f"git diff {dreipunkt} --name-only: nur research/ und docs/",
          not fremd, f"{len(diff)} Dateien" + (f", fremd: {fremd}" if fremd else ""))
    tabu_diff = subprocess.run(["git", "-C", botenv.REPO_ROOT, "diff", dreipunkt,
                                "--name-only", "--"] + TABU,
                               capture_output=True, text=True).stdout.strip()
    check("die im Auftrag benannten Bot-Dateien sind unveraendert",
          not tabu_diff, f"{len(TABU)} Dateien geprueft")

    print(f"\n{BOT}: {sum(1 for _n, ok, _d in CHECKS if ok)} von {len(CHECKS)} Pruefungen bestanden.")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
