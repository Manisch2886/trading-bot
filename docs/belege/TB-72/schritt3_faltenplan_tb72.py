"""TB-72 Schritt 3: den neuen Faltenplan DANEBEN schreiben und gegenueberstellen.

Schreibt `research/vorregistrierung/ergebnisse/faltenplan_tb72.json` mit
denselben json.dump-Einstellungen wie `faltenplan.py::main` (das selbst
IMMER nach faltenplan.json schreibt und deshalb hier nicht aufgerufen wird;
Sperrliste Punkt 2: nie ueberschreiben, immer neuer Dateiname, gegenpruefen).

Gegenuebergestellt wird zweimal:
  (a) gegen den SPEICHERSTAND vor TB-72 (docs/belege/TB-72/
      faltenplan_4a_stand_vor_tb72.json, Schritt 0) - das ist der Plan, den
      benchmark_drawdowns_vt.json und die Register-Abschnitte 21-24 tragen;
  (b) gegen ergebnisse/faltenplan.json auf der Platte - der ist TB-30a-Stand
      (a2fcf01: Krypto-Platzhalter, Aktien ab 2019) und seit TB-56/TB-61
      nicht neu geschrieben worden (Befund K4k aus Schritt 1).

    trading-env/bin/python3 docs/belege/TB-72/schritt3_faltenplan_tb72.py
"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))  # docs/belege/TB-72 -> Repo-Wurzel
VR = os.path.join(BASE, "research", "vorregistrierung")
sys.path.insert(0, VR)
import faltenplan as vfp
import registerdaten as rd

ZIEL = os.path.join(VR, "ergebnisse", "faltenplan_tb72.json")
VORHER = os.path.join(BASE, "docs", "belege", "TB-72", "faltenplan_4a_stand_vor_tb72.json")
PLATTE = os.path.join(VR, "ergebnisse", "faltenplan.json")
assert os.path.basename(ZIEL) != "faltenplan.json"

plan = vfp.faltenplan(rd._mess())
with open(ZIEL, "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
    f.write("\n")
print(f"Geschrieben: {os.path.relpath(ZIEL, BASE)}\n")

FELDER = ("erste_falte", "selektionsfalten", "bestaetigungsperiode",
          "faltenlaenge_jahre", "purge_tage", "embargo_tage", "go_live_schnitt",
          "status", "trades_je_jahr")


def gegenueber(titel, alt_pfad):
    with open(alt_pfad, encoding="utf-8") as f:
        alt = json.load(f)
    print("=" * 100)
    print(f"{titel}\n  alt: {os.path.relpath(alt_pfad, BASE)}")
    print("=" * 100)
    print(f"{'Bot':<28}{'Feld':<22}{'alt':<40}neu")
    print("-" * 100)
    bots_geaendert, falten_geaendert, nur_embargo = set(), [], []
    for bot in plan:
        for feld in FELDER:
            a, n = alt[bot].get(feld), plan[bot].get(feld)
            if a != n:
                bots_geaendert.add(bot)
                print(f"{bot:<28}{feld:<22}{str(a):<40}{n}")
        # Falten einzeln: Name, Rolle, Grenzen, Training, Embargo
        af = {f["name"]: f for f in alt[bot].get("falten", [])}
        nf = {f["name"]: f for f in plan[bot]["falten"]}
        for name in sorted(set(af) | set(nf)):
            if af.get(name) != nf.get(name):
                falten_geaendert.append((bot, name))
                bots_geaendert.add(bot)
                if name not in af:
                    print(f"{bot:<28}{'Falte ' + name:<22}{'-':<40}neu: {nf[name]['rolle']}")
                elif name not in nf:
                    print(f"{bot:<28}{'Falte ' + name:<22}{af[name]['rolle']:<40}entfaellt")
                else:
                    diff = {k: (af[name].get(k), nf[name].get(k))
                            for k in set(af[name]) | set(nf[name])
                            if af[name].get(k) != nf[name].get(k)}
                    print(f"{bot:<28}{'Falte ' + name:<22}{str(diff)}")
                    # Nur die Embargo-Liste anders (eine entfallene Falte kann
                    # nicht mehr embargiert werden): Folge, keine eigene Aenderung.
                    if set(diff) == {"embargo_nach_falten"}:
                        nur_embargo.append((bot, name))
                        falten_geaendert.pop()
        neue_felder = sorted(set(plan[bot]) - set(alt[bot]))
        if neue_felder:
            print(f"{bot:<28}{'neue Felder':<22}{'-':<40}{neue_felder}")
    print("-" * 100)
    print(f"Bots mit Aenderung an den Feldern {FELDER} oder an einer Falte: "
          f"{len(bots_geaendert)} {sorted(bots_geaendert)}")
    print(f"Geaenderte, neue oder entfallene Falten (Grenzen, Rolle, Training): "
          f"{len(falten_geaendert)} {falten_geaendert}")
    print(f"Folgeaenderung nur an embargo_nach_falten: {len(nur_embargo)} {nur_embargo}\n")
    return sorted(bots_geaendert), falten_geaendert


b_a, f_a = gegenueber("(a) Speicherstand vor TB-72 (4a allein) gegen neuen Plan", VORHER)
b_b, f_b = gegenueber("(b) faltenplan.json auf der Platte (TB-30a-Stand) gegen neuen Plan", PLATTE)
print("Erwartung aus dem Auftrag: genau ein Bot, genau eine Falte - gilt fuer (a):",
      "JA" if b_a == ["t3_supertrend"] and len(f_a) == 1 else "NEIN (Befund)")
print("Neue Felder je Bot (Herkunft der Ableitung):",
      sorted(set(plan["t3_supertrend"]) - {"markt", "status", "faltenlaenge_jahre",
       "trades_je_jahr", "faltenlaenge_begruendung", "purge_tage", "embargo_tage",
       "mindesttraining_jahre", "go_live_schnitt", "erste_falte", "erste_falte_quelle",
       "falten", "selektionsfalten", "bestaetigungsperiode"}))
