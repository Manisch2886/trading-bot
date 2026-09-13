"""
Auswertung der Stufen - traegt der Score etwas?
====================================================================
Liest `results/<bot>_muster.csv` (aus lauf.py) und beantwortet die vier
Fragen des Auftrags. Rechnet nur noch auf den bereits erzeugten
Trade-Zeilen; kein Bot-Code wird hier mehr aufgerufen.

Aufbau der Ergebnisdatei `results/<bot>_auswertung.json`:

  stufen          je Stufe 0-3: Gruppengroesse, Nettorendite, Bootstrap-
                  Intervall (ueber Trades UND ueber Symbole), Trefferquote,
                  Ausstiegsarten
  monotonie       Rangkorrelation Stufe<->Rendite, Vergleiche zwischen
                  benachbarten Stufen, Schwellenfrage (0 gegen >=1)
  bedingungen     Wirkung JEDER der drei Bedingungen einzeln - die
                  Zerlegung, die die Stufe verdeckt
  rundungsartefakt  0,33 gegen 0,34 innerhalb Stufe 1 (und 0,66/0,67
                  innerhalb Stufe 2), samt der Angabe, WELCHE Bedingung
                  die 0,34 traegt
  stetig          die Nebenfrage: gibt es unter dem Score eine stetige
                  Groesse, und traegt sie mehr als die Stufe?
  macht           wie gross muesste die Stichprobe sein, um einen
                  Unterschied dieser Groessenordnung zu finden

ZU DEN P-WERTEN: es werden viele Vergleiche gerechnet. Ein einzelner
p-Wert unter 0,05 unter zwei Dutzend Tests ist kein Befund - die
Auswertung weist deshalb die ZAHL der Vergleiche mit aus und der
Bericht redet nicht von "signifikant", wo nur ein Einzelvergleich
knapp durchkommt.

Aufruf:  python3 auswertung.py <elliott_wave|elliott_wave_stocks>
"""

import json
import os
import sys

import botenv                                                     # noqa: E402

BOT = botenv.bot_from_argv() if __name__ == "__main__" else None

import numpy as np                                                # noqa: E402
import pandas as pd                                               # noqa: E402

import bedingungen as bd                                          # noqa: E402
import statistik as st                                            # noqa: E402

STUFEN = (0, 1, 2, 3)
# Ab wie vielen Trades eine Gruppe ueberhaupt kommentiert wird. Der
# Auftrag sagt es selbst: "Eine Stufe mit zwoelf Mustern traegt keine
# Aussage." 30 ist die Zahl, die das Projekt an anderer Stelle schon
# als Mindestgroesse fuer eine Trade-Stichprobe benutzt
# (multi_symbol_optimise.MIN_TRADES beim Krypto-Bot).
MIN_AUSSAGEKRAEFTIG = 30


def _z(x):
    """JSON kennt kein numpy."""
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return None if np.isnan(x) else round(float(x), 6)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, dict):
        return {str(k): _z(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_z(v) for v in x]
    if isinstance(x, float):
        return None if np.isnan(x) else round(x, 6)
    return x


def gruppe(df: pd.DataFrame, name: str) -> dict:
    """Beschreibung einer Trade-Gruppe - immer MIT Gruppengroesse."""
    if df.empty:
        return {"name": name, "n": 0, "aussagekraeftig": False}
    pnl = df["pnl_pct"].astype(float).to_numpy()
    boot = st.bootstrap_mittelwert(pnl)
    boot_c = st.bootstrap_mittelwert(pnl, cluster=df["symbol"].to_numpy())
    arten = df["result"].value_counts()
    return {
        "name": name,
        "n": int(len(df)),
        "symbole": int(df["symbol"].nunique()),
        "mittel_pnl_pct": round(float(pnl.mean()), 2),
        "median_pnl_pct": round(float(np.median(pnl)), 2),
        "streuung_pnl_pct": round(float(pnl.std(ddof=1)), 2) if len(pnl) > 1 else None,
        "summe_pnl_pct": round(float(pnl.sum()), 2),
        "trefferquote_pct": round(float((pnl > 0).mean() * 100), 1),
        "ci95_trades": [round(boot["ci_low"], 2), round(boot["ci_high"], 2)]
                       if boot and boot["ci_low"] is not None else None,
        "ci95_cluster_symbole": [round(boot_c["ci_low"], 2), round(boot_c["ci_high"], 2)]
                                if boot_c and boot_c["ci_low"] is not None else None,
        "ausstieg": {str(k): int(v) for k, v in arten.items()},
        "haltedauer_median": round(float(df["haltedauer_balken"].median()), 1)
                             if "haltedauer_balken" in df else None,
        "aussagekraeftig": bool(len(df) >= MIN_AUSSAGEKRAEFTIG),
    }


def vergleich(a: pd.DataFrame, b: pd.DataFrame, name: str) -> dict:
    """Zwei Gruppen gegeneinander.

    EIN Test (der Permutationstest auf den Mittelwertunterschied), dazu
    drei Angaben, die denselben Unterschied nur von verschiedenen Seiten
    beleuchten und keine zusaetzlichen p-Werte erzeugen:

      * Bootstrap-Intervall ueber TRADES   - die uebliche Unsicherheit
      * Bootstrap-Intervall ueber SYMBOLE  - Trades desselben Symbols sind
        nicht unabhaengig; dieses Intervall ist das ehrlichere
      * Weglassprobe                       - jedes Symbol einmal raus:
        haengt der Unterschied an einem einzigen Wert?

    Die Trefferquote steht rein beschreibend daneben (ohne p-Wert). Sie
    ist bei diesen Bots aufschlussreich, weil der Median in fast jeder
    Gruppe auf dem Stop liegt: ein Unterschied im Mittelwert kann
    entweder aus mehr Gewinnern oder aus groesseren Gewinnern kommen."""
    pa = a["pnl_pct"].astype(float).to_numpy()
    pb = b["pnl_pct"].astype(float).to_numpy()
    if len(pa) == 0 or len(pb) == 0:
        return {"name": name, "n_a": int(len(pa)), "n_b": int(len(pb)),
                "auswertbar": False}
    diff = st.bootstrap_differenz(pa, pb)
    diff_c = st.bootstrap_differenz_cluster(pa, a["symbol"].to_numpy(),
                                            pb, b["symbol"].to_numpy())
    perm = st.permutation_differenz(pa, pb)
    weglass = st.weglassprobe(pa, a["symbol"].to_numpy(), pb, b["symbol"].to_numpy())
    return {
        "name": name,
        "auswertbar": True,
        "n_a": int(len(pa)), "n_b": int(len(pb)),
        "mittel_a": round(float(pa.mean()), 2),
        "mittel_b": round(float(pb.mean()), 2),
        "differenz_pp": round(float(pa.mean() - pb.mean()), 2),
        "ci95_differenz": [round(diff["ci_low"], 2), round(diff["ci_high"], 2)] if diff else None,
        "ci_schliesst_null_ein": diff["schliesst_null_ein"] if diff else None,
        "ci95_differenz_cluster_symbole": [round(diff_c["ci_low"], 2),
                                           round(diff_c["ci_high"], 2)] if diff_c else None,
        "ci_cluster_schliesst_null_ein": diff_c["schliesst_null_ein"] if diff_c else None,
        "p_permutation": round(perm["p_wert"], 4) if perm else None,
        "weglassprobe_symbole": _z(weglass),
        "trefferquote_a_pct": round(float((pa > 0).mean() * 100), 1),
        "trefferquote_b_pct": round(float((pb > 0).mean() * 100), 1),
        "differenz_trefferquote_pp": round(float(((pa > 0).mean() - (pb > 0).mean()) * 100), 1),
    }


def eindeutigkeit(df: pd.DataFrame) -> dict:
    """Taugt die stetige Groesse als PRIMAERSCHLUESSEL fuer eine kuenftige
    Zuteilungsregel - also: erzeugt sie noch Gleichstaende?

    TB-20 hat dieselbe Frage fuer den `fib_score` beantwortet (87 % bzw.
    99 % der Muster in einer Gleichstandsgruppe). Hier steht die
    Gegenzahl fuer `naehe`, gemessen auf denselben Mustern - je Symbol,
    weil die Auswahl innerhalb eines Symbols stattfindet."""
    def anteil_in_gruppe(spalte):  # noqa: D401
        geteilt = 0
        for _symbol, teil in df.groupby("symbol"):
            zaehl = teil[spalte].round(10).value_counts()
            geteilt += int(zaehl[zaehl > 1].sum())
        return round(geteilt / len(df) * 100, 1) if len(df) else None

    return {
        "anteil_gleichstand_fib_score_pct": anteil_in_gruppe("fib_score"),
        "anteil_gleichstand_naehe_pct": anteil_in_gruppe("naehe"),
        "anteil_gleichstand_naehe_weich_pct": anteil_in_gruppe("naehe_weich"),
        "verschiedene_fib_score_werte": int(df["fib_score"].nunique()),
        "verschiedene_naehe_werte": int(df["naehe"].round(10).nunique()),
        "verschiedene_naehe_weich_werte": int(df["naehe_weich"].round(10).nunique()),
        "muster_gesamt": int(len(df)),
        "bemerkung": ("Gemessen auf den Mustern DIESER Untersuchung (Stufen 0-3, "
                      "nur bearish, nur frisch) und je Symbol. Die 87 % / 99 % aus "
                      "TB-20 beziehen sich auf eine weitere Menge (alle Richtungen, "
                      "ohne Frischefilter) und sind deshalb nicht Ziffer fuer Ziffer "
                      "dieselbe Zahl - die Aussage ist dieselbe."),
    }


def auswerten(df: pd.DataFrame) -> dict:
    erg = {}
    anzahl_tests = 0

    # ---------------- 1. Die Stufen ----------------------------------
    erg["stufen"] = [gruppe(df[df["stufe"] == s], f"Stufe {s}") for s in STUFEN]

    # ---------------- 1b. Liegen die Stufen in denselben Zeiten? -----
    # Ein Unterschied zwischen den Stufen waere wertlos, wenn die hoeheren
    # Stufen einfach in besseren Marktphasen haeufiger auftraeten. Deshalb
    # steht hier die Jahresverteilung je Stufe daneben - beschreibend, ohne
    # Test.
    jahre = pd.to_datetime(df["entry_time"]).dt.year
    erg["zeitliche_verteilung"] = {
        "je_stufe": {
            str(s_): {
                "median_einstieg": str(pd.to_datetime(df.loc[df["stufe"] == s_,
                                                             "entry_time"]).median().date()),
                "je_jahr": {str(j): int(n) for j, n in
                            sorted(jahre[df["stufe"] == s_].value_counts().items())},
            }
            for s_ in STUFEN if (df["stufe"] == s_).any()},
        "bemerkung": ("Beschreibend, kein Test. Verteilen sich die Stufen aehnlich "
                      "ueber die Jahre, kann ein Stufenunterschied nicht allein "
                      "daran liegen, dass eine Stufe in einer besseren Marktphase "
                      "haeufiger vorkommt."),
    }

    # ---------------- 2. Monotonie und Schwelle ----------------------
    sp = st.spearman_permutation(df["stufe"].to_numpy(), df["pnl_pct"].astype(float).to_numpy())
    anzahl_tests += 1
    paare = []
    for s in (1, 2, 3):
        a, b = df[df["stufe"] == s], df[df["stufe"] == s - 1]
        if len(a) and len(b):
            paare.append(vergleich(a, b, f"Stufe {s} gegen Stufe {s - 1}"))
            anzahl_tests += 1

    schwelle = vergleich(df[df["stufe"] >= 1], df[df["stufe"] == 0],
                         "oberhalb der Schwelle (Stufe >=1) gegen Stufe 0")
    ab_zwei = vergleich(df[df["stufe"] >= 2], df[df["stufe"] <= 1],
                        "Stufe >=2 gegen Stufe <=1")
    nur_drei = vergleich(df[df["stufe"] == 3], df[df["stufe"] < 3],
                         "Stufe 3 gegen alles darunter")
    anzahl_tests += 3

    erg["monotonie"] = {
        "spearman_stufe_gegen_pnl": _z(sp),
        "benachbarte_stufen": paare,
        "schwellenfrage": schwelle,
        "stufe_ab_2": ab_zwei,
        "nur_stufe_3": nur_drei,
        "mittelwerte_je_stufe": {str(s): round(float(df[df["stufe"] == s]["pnl_pct"].mean()), 2)
                                 for s in STUFEN if (df["stufe"] == s).any()},
        "monoton_steigend_im_punktwert": bool(
            all(df[df["stufe"] == s]["pnl_pct"].mean() <= df[df["stufe"] == s + 1]["pnl_pct"].mean()
                for s in (0, 1, 2)
                if (df["stufe"] == s).any() and (df["stufe"] == s + 1).any())),
    }

    # ---------------- 3. Die drei Bedingungen einzeln ----------------
    # Die Stufe zaehlt nur, WIE VIELE Bedingungen gelten. Ob sie
    # gleichwertig sind, steht damit nicht fest - genau das wird hier
    # getrennt gemessen.
    einzeln = []
    for name, punkte, lo, hi, fib, titel in bd.BEDINGUNGEN:
        spalte = f"erf_{name}"
        v = vergleich(df[df[spalte]], df[~df[spalte]], f"{titel} erfuellt gegen nicht erfuellt")
        v.update({"bedingung": name, "titel": titel, "teilpunkte_im_bot": punkte,
                  "intervall": [lo, hi], "kanonischer_fib_wert": fib})
        einzeln.append(v)
        anzahl_tests += 1
    erg["bedingungen"] = einzeln

    # Jede Kombination einzeln - damit sichtbar bleibt, dass eine Stufe
    # verschiedene Muster zusammenwirft.
    erg["kombinationen"] = [
        gruppe(df[df["muster_bedingungen"] == k], k)
        for k in sorted(df["muster_bedingungen"].unique())
    ]

    # ---------------- 4. Das Rundungsartefakt ------------------------
    stufe1 = df[df["stufe"] == 1]
    stufe2 = df[df["stufe"] == 2]
    artefakt = {
        "welche_bedingung_traegt_0_34": bd.BEDINGUNGEN[0][5],
        "erklaerung": ("0,34 kann nur von der ERSTEN Bedingung kommen. Innerhalb "
                       "Stufe 1 heisst 0,34 also 'nur Welle 2 passt' und 0,33 'nur "
                       "Welle 3' oder 'nur Welle 4'. Der Rangfolge-Vorzug der 0,34 "
                       "ist damit kein Zufall, sondern ein fest eingebauter Vorzug "
                       "der Welle-2-Bedingung - gewaehlt hat ihn niemand."),
        "stufe1_0_34_gegen_0_33": vergleich(
            stufe1[stufe1["fib_score"] == 0.34], stufe1[stufe1["fib_score"] == 0.33],
            "Stufe 1: 0,34 gegen 0,33"),
        "stufe1_je_bedingung": [gruppe(stufe1[stufe1["muster_bedingungen"] == k], k)
                                for k in sorted(stufe1["muster_bedingungen"].unique())],
        "stufe2_0_67_gegen_0_66": vergleich(
            stufe2[stufe2["fib_score"] == 0.67], stufe2[stufe2["fib_score"] == 0.66],
            "Stufe 2: 0,67 gegen 0,66"),
        "stufe2_je_bedingung": [gruppe(stufe2[stufe2["muster_bedingungen"] == k], k)
                                for k in sorted(stufe2["muster_bedingungen"].unique())],
    }
    anzahl_tests += 2
    erg["rundungsartefakt"] = artefakt

    # ---------------- 5. Die stetige Groesse darunter ----------------
    stetig = {
        "existiert": True,
        "begruendung": ("Alle drei Bedingungen sind Intervallpruefungen auf einem "
                        "Wellenlaengen-VERHAELTNIS - einer stetigen Groesse. Der "
                        "Score schneidet sie auf 0/1."),
        "bemerkung_intervall": ("Es sind Intervalle, keine '±x % um ein Ziel'. Die "
                                "kanonischen Fibonacci-Werte liegen bei Welle 2 und "
                                "Welle 4 auf dem RAND des Intervalls, bei Welle 3 "
                                "unsymmetrisch im Inneren."),
        "spearman_naehe_gegen_pnl": _z(st.spearman_permutation(
            df["naehe"].to_numpy(), df["pnl_pct"].astype(float).to_numpy())),
        "spearman_naehe_fib_gegen_pnl": _z(st.spearman_permutation(
            df["naehe_fib"].to_numpy(), df["pnl_pct"].astype(float).to_numpy())),
        "spearman_naehe_weich_gegen_pnl": _z(st.spearman_permutation(
            df["naehe_weich"].to_numpy(), df["pnl_pct"].astype(float).to_numpy())),
        "spearman_gesamtabstand_gegen_pnl": _z(st.spearman_permutation(
            df["gesamtabstand"].to_numpy(), df["pnl_pct"].astype(float).to_numpy())),
        "saettigung_naehe": {
            "anteil_naehe_null_pct": round(float((df["naehe"] <= 0).mean() * 100), 1),
            "bemerkung": ("`naehe` ist fuer jedes Muster ausserhalb aller drei "
                          "Intervalle exakt 0 und unterscheidet dort nichts mehr. "
                          "`naehe_weich` und `gesamtabstand` haben diese Stelle "
                          "nicht - siehe bedingungen.py."),
        },
        "je_bedingung": {},
        "naehe_quartile": [],
        "entartete_muster": int(df["entartet"].sum()),
        "eindeutigkeit": eindeutigkeit(df),
    }
    anzahl_tests += 4
    for name, _p, _lo, _hi, _f, titel in bd.BEDINGUNGEN:
        teil = df[np.isfinite(df[f"d_{name}"])]
        stetig["je_bedingung"][name] = {
            "titel": titel,
            "n_definiert": int(len(teil)),
            "spearman_abstand_gegen_pnl": _z(st.spearman_permutation(
                teil[f"d_{name}"].to_numpy(), teil["pnl_pct"].astype(float).to_numpy())),
            "spearman_verhaeltnis_gegen_pnl": _z(st.spearman_permutation(
                teil[f"r_{name}"].to_numpy(), teil["pnl_pct"].astype(float).to_numpy())),
        }
        anzahl_tests += 2

    # Quartile der stetigen Naehe - die feinere Fassung der Stufen.
    # `duplicates="drop"` faengt den Fall ab, dass ein Quartilsrand auf
    # den Haeufungspunkt naehe = 0 faellt (alle Stufe-0-Muster).
    try:
        koerbe = pd.qcut(df["naehe"], 4, duplicates="drop")
        for korb, teil in df.groupby(koerbe, observed=True):
            stetig["naehe_quartile"].append(gruppe(teil, f"naehe in {korb}"))
    except ValueError:
        stetig["naehe_quartile"] = None

    erg["stetig"] = stetig

    # ---------------- 6. Wie gross muesste die Stichprobe sein? ------
    streuung = float(df["pnl_pct"].std(ddof=1))
    erg["macht"] = {
        "streuung_pnl_pct": round(streuung, 2),
        "hinweis": ("Normalapproximation, Groessenordnung - keine Planungszahl. "
                    "Sie beantwortet die Frage, die bei einem Nicht-Ergebnis "
                    "sofort kommt: war die Messung ueberhaupt in der Lage, "
                    "etwas zu finden?"),
        "trades_je_gruppe_fuer": {
            f"{d:g}pp": st.benoetigte_stichprobe(d, streuung) for d in (1.0, 2.0, 5.0)},
    }

    erg["anzahl_vergleiche"] = anzahl_tests
    erg["hinweis_mehrfachvergleiche"] = (
        f"{anzahl_tests} Vergleiche. Bei 5 % Irrtumswahrscheinlichkeit sind rein "
        f"zufaellig rund {anzahl_tests * 0.05:.1f} davon 'auffaellig'. Ein einzelner "
        "p-Wert knapp unter 0,05 ist hier kein Befund.")
    return erg


def main():
    botenv.print_hinweis()
    csv_pfad = os.path.join(botenv.RESULTS_DIR, f"{BOT}_muster.csv")
    if not os.path.exists(csv_pfad):
        raise SystemExit(f"{csv_pfad} fehlt - erst 'python3 lauf.py {BOT}' ausfuehren.")
    df = pd.read_csv(csv_pfad)
    print(f"[{BOT}] {len(df)} Trades, Stufen: "
          f"{dict(sorted(df['stufe'].value_counts().items()))}")

    erg = auswerten(df)
    erg = {"hinweis": botenv.UNTERSUCHUNG_HINWEIS, "bot": BOT,
           "quelle": os.path.basename(csv_pfad), **_z(erg)}

    pfad = os.path.join(botenv.RESULTS_DIR, f"{BOT}_auswertung.json")
    with open(pfad, "w") as fh:
        json.dump(erg, fh, indent=2, ensure_ascii=False)
    print(f"[{BOT}] geschrieben: {pfad}")

    # Kurzfassung auf der Konsole
    print(f"\n[{BOT}] Nettorendite je Stufe (Bootstrap-95 %-Intervall ueber Trades):")
    for s in erg["stufen"]:
        if s["n"] == 0:
            continue
        ci = s["ci95_trades"]
        print(f"  {s['name']}: n={s['n']:>4}  Mittel {s['mittel_pnl_pct']:>6.2f} %  "
              f"CI [{ci[0]:>6.2f}, {ci[1]:>6.2f}]  Treffer {s['trefferquote_pct']:>4.1f} %"
              f"{'' if s['aussagekraeftig'] else '   (zu klein)'}")
    m = erg["monotonie"]
    print(f"  Spearman(Stufe, PnL) = {m['spearman_stufe_gegen_pnl']['rho']:.3f}  "
          f"p = {m['spearman_stufe_gegen_pnl']['p_wert']:.4f}")
    sw = m["schwellenfrage"]
    print(f"  Schwelle: Stufe>=1 minus Stufe 0 = {sw['differenz_pp']:+.2f} pp  "
          f"CI {sw['ci95_differenz']}  p = {sw['p_permutation']:.4f}")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
