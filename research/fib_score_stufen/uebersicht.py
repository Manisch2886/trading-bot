"""
Zusammenfassung beider Bots - die Antwort in einer Tabelle
====================================================================
Liest die beiden `results/<bot>_auswertung.json` und stellt sie
nebeneinander. Erzeugt `results/uebersicht.json` und gibt dieselbe
Uebersicht auf der Konsole aus.

Dieses Skript importiert KEINEN Bot-Code und darf deshalb als
einziges beide Bots im selben Prozess anfassen.

Aufruf:  python3 uebersicht.py
"""

import json
import os

import botenv

# Der Ausgang wird nicht "gefuehlt", sondern an drei vorab benannten
# Bedingungen festgemacht - so wie der Auftrag sie formuliert.
AUSGAENGE = {
    "monoton": "Rendite steigt monoton mit der Stufe - der Score ist eine echte Ordinalskala",
    "kein_unterschied": "Kein Unterschied zwischen den Stufen - der Score traegt nichts",
    "nur_drei": "Nur die 3-von-3-Gruppe unterscheidet sich - Ja/Nein-Filter mit falscher Schwelle",
}


def ausgang(e: dict) -> dict:
    """Welcher der drei im Auftrag genannten Ausgaenge ist eingetreten?

    Entscheidungsregel, vorab festgelegt:
      * 'monoton' verlangt, dass JEDER Schritt von Stufe s zu s+1 einen
        Unterschied zeigt, dessen Bootstrap-Intervall die Null NICHT
        einschliesst. Ein blosses Ansteigen der Punktwerte reicht nicht -
        bei vier Gruppen steigt eine zufaellige Folge in einem von
        24 Faellen von selbst monoton.
      * 'nur_drei' verlangt, dass Stufe 3 sich von allem darunter
        abhebt (Intervall ohne Null) UND die Stufen 0-2 untereinander
        nicht.
      * sonst: 'kein_unterschied'.
    """
    m = e["monotonie"]
    schritte = m["benachbarte_stufen"]
    jeder_schritt = all(s.get("ci_schliesst_null_ein") is False for s in schritte) and schritte
    unten_flach = all(s.get("ci_schliesst_null_ein") is not False
                      for s in schritte if not s["name"].startswith("Stufe 3"))
    drei_hebt_ab = m["nur_stufe_3"].get("ci_schliesst_null_ein") is False

    if jeder_schritt:
        schluessel = "monoton"
    elif drei_hebt_ab and unten_flach:
        schluessel = "nur_drei"
    else:
        schluessel = "kein_unterschied"
    return {
        "schluessel": schluessel,
        "text": AUSGAENGE[schluessel],
        "jeder_schritt_unterscheidbar": bool(jeder_schritt),
        "stufe_3_hebt_sich_ab": bool(drei_hebt_ab),
        "punktwerte_steigen_monoton": bool(m["monoton_steigend_im_punktwert"]),
        "schwelle_wirkt": e["monotonie"]["schwellenfrage"].get("ci_schliesst_null_ein") is False,
    }


def main():
    botenv.print_hinweis()
    zusammen = {"hinweis": botenv.UNTERSUCHUNG_HINWEIS, "bots": {}}

    for bot in botenv.BOTS:
        pfad = os.path.join(botenv.RESULTS_DIR, f"{bot}_auswertung.json")
        if not os.path.exists(pfad):
            raise SystemExit(f"{pfad} fehlt - erst 'python3 run_all.py' ausfuehren.")
        e = json.load(open(pfad))
        lauf = json.load(open(os.path.join(botenv.RESULTS_DIR, f"{bot}_lauf.json")))
        zusammen["bots"][bot] = {
            "ausgang": ausgang(e),
            "datenbasis": lauf["datenbasis"],
            "parameter": lauf["parameter"],
            "stufen": [{k: g[k] for k in ("name", "n", "mittel_pnl_pct", "ci95_trades",
                                          "ci95_cluster_symbole", "trefferquote_pct",
                                          "aussagekraeftig")}
                       for g in e["stufen"] if g["n"] > 0],
            "schwellenfrage": e["monotonie"]["schwellenfrage"],
            "spearman_stufe": e["monotonie"]["spearman_stufe_gegen_pnl"],
            "bedingungen": [{k: b[k] for k in ("bedingung", "titel", "n_a", "mittel_a",
                                               "n_b", "mittel_b", "differenz_pp",
                                               "ci95_differenz", "p_permutation")}
                            for b in e["bedingungen"]],
            "rundungsartefakt": e["rundungsartefakt"]["stufe1_0_34_gegen_0_33"],
            "stetig": {
                "naehe": e["stetig"]["spearman_naehe_gegen_pnl"],
                "naehe_weich": e["stetig"]["spearman_naehe_weich_gegen_pnl"],
                "eindeutigkeit": e["stetig"]["eindeutigkeit"],
            },
            "anzahl_vergleiche": e["anzahl_vergleiche"],
        }

    pfad = os.path.join(botenv.RESULTS_DIR, "uebersicht.json")
    with open(pfad, "w") as fh:
        json.dump(zusammen, fh, indent=2, ensure_ascii=False)

    for bot, d in zusammen["bots"].items():
        print(f"\n{'=' * 70}\n{bot}  -  {d['ausgang']['text']}\n{'=' * 70}")
        print(f"{'Stufe':<10}{'n':>6}{'Mittel':>10}{'CI (Trades)':>20}"
              f"{'CI (Symbole)':>20}{'Treffer':>10}")
        for g in d["stufen"]:
            ci, cc = g["ci95_trades"], g["ci95_cluster_symbole"]
            print(f"{g['name']:<10}{g['n']:>6}{g['mittel_pnl_pct']:>9.2f}%"
                  f"{f'[{ci[0]:.2f}, {ci[1]:.2f}]':>20}"
                  f"{f'[{cc[0]:.2f}, {cc[1]:.2f}]':>20}"
                  f"{g['trefferquote_pct']:>9.1f}%"
                  f"{'' if g['aussagekraeftig'] else '   (zu klein)'}")
        sw = d["schwellenfrage"]
        print(f"\nSchwelle (Stufe>=1 gegen Stufe 0): {sw['differenz_pp']:+.2f} pp, "
              f"CI {sw['ci95_differenz']}, p = {sw['p_permutation']:.4f}")
        print(f"Spearman(Stufe, PnL) = {d['spearman_stufe']['rho']:+.3f}, "
              f"p = {d['spearman_stufe']['p_wert']:.4f}   "
              f"({d['anzahl_vergleiche']} Vergleiche insgesamt)")
        print("\nDie drei Bedingungen einzeln:")
        for b in d["bedingungen"]:
            print(f"  {b['titel']:<20} erfuellt n={b['n_a']:>4} {b['mittel_a']:>6.2f}%  "
                  f"nicht n={b['n_b']:>4} {b['mittel_b']:>6.2f}%  "
                  f"Differenz {b['differenz_pp']:+6.2f} pp  CI {str(b['ci95_differenz']):>18}  "
                  f"p = {b['p_permutation']:.4f}")
        r = d["rundungsartefakt"]
        print(f"\n0,34 gegen 0,33 (Stufe 1): {r['differenz_pp']:+.2f} pp, "
              f"CI {r['ci95_differenz']}, p = {r['p_permutation']:.4f}")
        s = d["stetig"]
        print(f"Stetige Naehe gegen PnL: rho = {s['naehe']['rho']:+.3f} "
              f"(p = {s['naehe']['p_wert']:.4f}), weiche Fassung rho = "
              f"{s['naehe_weich']['rho']:+.3f} (p = {s['naehe_weich']['p_wert']:.4f})")
        ein = s["eindeutigkeit"]
        print(f"Gleichstaende je Symbol: fib_score {ein['anteil_gleichstand_fib_score_pct']} %, "
              f"naehe_weich {ein['anteil_gleichstand_naehe_weich_pct']} %")

    print(f"\ngeschrieben: {pfad}")
    botenv.print_hinweis()


if __name__ == "__main__":
    main()
