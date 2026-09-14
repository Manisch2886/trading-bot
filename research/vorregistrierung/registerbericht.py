#!/usr/bin/env python3
"""
TB-30a - Der Zahlenteil des Registers, erzeugt statt abgetippt
==============================================================================
`docs/VORREGISTRIERUNG_neuselektion.md` enthaelt Tabellen: die Raster je Bot,
den Faltenplan, die vorab berechneten Benchmark-Drawdowns. Diese Zahlen
stehen im Code (`registerdaten.py`, `faltenplan.py`, `benchmark.py`), und
abgetippt liefen sie frueher oder spaeter auseinander - in diesem Projekt ist
genau das schon mehrfach passiert.

Dieses Programm erzeugt den Block. Zwei Betriebsarten:

  (ohne Schalter)  den Block auf die Standardausgabe schreiben
  --pruefen        nachsehen, ob der Block WOERTLICH im Register steht.
                   Rueckgabewert 1, wenn nicht - dann ist das Register
                   veraltet, und das faellt auf, statt zu wirken.

Der Block ist im Register zwischen zwei Markierungen eingefasst:

    <!-- ERZEUGT: registerbericht.py -- nicht von Hand aendern -->
    ...
    <!-- ENDE ERZEUGT -->
"""

import argparse
import json
import os
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB30A_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

import auswertung as aw  # noqa: E402
import faltenplan as fp  # noqa: E402
import registerdaten as rd  # noqa: E402

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")
ANFANG = "<!-- ERZEUGT: registerbericht.py -- nicht von Hand aendern -->"
ENDE = "<!-- ENDE ERZEUGT -->"

EXPOSURE_SPALTEN = ["0.25", "0.50", "0.75", "1.00"]


def _grenzen(achse: dict):
    """Dieselbe Aufzaehlung wie in pruefe_grenzsaetze.py - eine Grenze, die
    dort geprueft wird, muss hier auch im Register auftauchen."""
    import pruefe_grenzsaetze as pg
    return pg.grenzen(achse)


def _wert(w):
    if w is None:
        return "kein"
    if isinstance(w, float):
        return f"{w:g}".replace(".", ",")
    return str(w)


def block() -> str:
    mess = rd._mess()
    plan = fp.faltenplan(mess)
    raster = rd.raster(mess)
    with open(os.path.join(_HIER, "ergebnisse", "benchmark_drawdowns.json"),
              encoding="utf-8") as f:
        tabellen = json.load(f)

    z = [ANFANG, ""]

    # --- Messgroessen ----------------------------------------------------
    z += ["### Die gemessenen Groessen, auf denen jede Grenze ruht", "",
          "Erzeugt von `research/vorregistrierung/messgroessen.py` aus "
          "`data/` und `config/` — **keine Bot-Ergebnisse.**", "",
          "| Zeitrahmen | Titel | σ je Balken | Median 20-Balken-Spanne | "
          "ATR(14) | Median Schluss→Tief |",
          "|---|---:|---:|---:|---:|---:|"]
    for k, v in sorted(mess["volatilitaet"].items()):
        z.append(f"| `{k}` | {v['symbole_gemessen']} | "
                 f"{_wert(v['balken_sigma_pct'])} % | "
                 f"{_wert(v['spanne20_median_pct'])} % | "
                 f"{_wert(v['atr14_median_pct'])} % | "
                 f"{_wert(v['tiefabstand_median_pct'])} % |")
    z += ["", f"Round-Trip-Kosten: **{_wert(mess['kosten']['round_trip_pct'])} %** "
          f"({_wert(mess['kosten']['gebuehr_pct_je_order'])} % Gebühr + "
          f"{_wert(mess['kosten']['slippage_pct_je_order'])} % Slippage je Order, "
          f"Ein- und Ausstieg).", ""]

    # --- Raster ----------------------------------------------------------
    z += ["### Die neun Raster", "",
          "| Bot | Achse | Stufen | Untergrenze | Obergrenze |",
          "|---|---|---|---|---|"]
    definition = rd.raster_definition()
    gesamt = 0
    for bot in rd.BOTS:
        gesamt += rd.zellen(bot, mess)
        for name, achse in definition[bot].items():
            if name.startswith("_"):
                continue
            werte = ", ".join(_wert(w) for w in raster[bot][name])
            if achse["art"] in ("aufzaehlung", "quantile"):
                unten = oben = "*" + achse["grundlage"] + "*"
            else:
                unten = f"*{achse['unten']['grundlage']}*"
                oben = f"*{achse['oben']['grundlage']}*"
            z.append(f"| `{bot}` | `{name}` | {werte} | {unten} | {oben} |")
    z += ["", "### Die Grenzsätze", "",
          "Ein Satz je Grenze, der **kein Ergebnis nennt** — gestützt nur auf "
          "Handelskosten, Datenfrequenz, Volatilität des Universums oder die "
          "Haltedauer-Hypothese des Bots. Gleiche Achsen tragen in der "
          "Aktien- und der Krypto-Variante **dieselbe Regel**, nicht denselben "
          "Wert; sie stehen deshalb nur einmal.", ""]
    gesehen = set()
    for bot in rd.BOTS:
        for name, achse in definition[bot].items():
            if name.startswith("_"):
                continue
            for rolle, g in _grenzen(achse):
                satz = (g.get("satz") or "").strip()
                if not satz or satz in gesehen:
                    continue
                gesehen.add(satz)
                z += [f"**`{name}` — {rolle}** *(Grundlage: {g['grundlage']})*",
                      "", "> " + satz, ""]

    z += ["",
          "| Bot | Zellen dieses Laufs | N historisch | N nominal |",
          "|---|---:|---:|---:|"]
    for bot in rd.BOTS:
        n = rd.zellen(bot, mess)
        h = rd.N_HISTORISCH_JE_BOT[bot]
        z.append(f"| `{bot}` | {n} | {h} | {n + h} |")
    z.append(f"| **Summe** | **{gesamt}** | **{rd.DSR_BASIS_N}** | "
             f"**{gesamt + rd.DSR_BASIS_N}** |")
    z.append("")

    # --- Faltenplan ------------------------------------------------------
    z += ["### Der Faltenplan", "",
          f"Go-Live-Schnitt: **{rd.GO_LIVE_SCHNITT}** (ausschliesslich). "
          f"Mindesttraining vor der ersten Falte: "
          f"**{rd.MINDESTTRAINING_JAHRE} Jahre**.", "",
          "| Bot | Markt | Faltenlänge | gefundene Trades/Jahr | Purge = Embargo | "
          "Selektionsfalten | Bestätigungsperiode |",
          "|---|---|---:|---:|---:|---|---|"]
    for bot, p in plan.items():
        sel = ", ".join(p["selektionsfalten"]) or "*Platzhalter (TB-31)*"
        best = p["bestaetigungsperiode"] or "*Platzhalter (TB-31)*"
        z.append(f"| `{bot}` | {p['markt']} | {p['faltenlaenge_jahre']} J | "
                 f"{_wert(p['trades_je_jahr'])} | {p['purge_tage']} Tage | "
                 f"{sel} | {best} |")
    z.append("")

    # --- Benchmark-Drawdowns ---------------------------------------------
    z += ["### Die vorab berechneten Benchmark-Drawdowns",
          "",
          "Je Falte, je Exposure-Stufe. Die vollständige Tabelle (1 % bis "
          "100 % in Schritten von 1 %) steht in "
          "`research/vorregistrierung/ergebnisse/benchmark_drawdowns.json`; "
          "hier vier Stützstellen.",
          ""]
    gezeigt = set()
    for bot, e in tabellen.items():
        if e["status"] != "endgueltig":
            continue
        schluessel = (e["markt"], tuple(sorted(e["falten"])))
        if schluessel in gezeigt:
            z.append(f"`{bot}` teilt Universum und Faltenplan mit den übrigen "
                     f"{e['markt']}-Bots — dieselbe Tabelle.")
            z.append("")
            continue
        gezeigt.add(schluessel)
        z += [f"**{e['markt']}** (`{e['universumsdatei']}`) — gilt für alle Bots "
              f"dieses Marktes mit gleichem Faltenplan:", "",
              "| Falte | Rolle | Titel (point-in-time) | Handelstage | "
              + " | ".join(f"DD @ {int(float(s) * 100)} %" for s in EXPOSURE_SPALTEN)
              + " |",
              "|---|---|---:|---:|" + "---:|" * len(EXPOSURE_SPALTEN)]
        for name, f in e["falten"].items():
            z.append(f"| {name} | {f['rolle']} | {f['symbole_point_in_time']} | "
                     f"{f['handelstage']} | "
                     + " | ".join(_wert(f["dd_benchmark"][s]) + " %"
                                  for s in EXPOSURE_SPALTEN) + " |")
        z.append("| **DD_Toleranz** | *Median über die Selektionsfalten* | | | "
                 + " | ".join(_wert(e["dd_toleranz"][s]) + " %"
                              for s in EXPOSURE_SPALTEN) + " |")
        z.append("")

    z += [ENDE]
    return "\n".join(z) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    p.add_argument("--pruefen", action="store_true")
    args = p.parse_args()
    erzeugt = block()
    if not args.pruefen:
        sys.stdout.write(erzeugt)
        return 0

    if not os.path.exists(REGISTER):
        print(f"GESCHEITERT: {REGISTER} fehlt.")
        return 1
    with open(REGISTER, encoding="utf-8") as f:
        text = f.read()
    if ANFANG not in text or ENDE not in text:
        print("GESCHEITERT: die Markierungen fehlen im Register.")
        return 1
    im_register = text[text.index(ANFANG):text.index(ENDE) + len(ENDE)] + "\n"
    if im_register != erzeugt:
        print("GESCHEITERT: der erzeugte Block steht nicht woertlich im "
              "Register - die Zahlen dort sind veraltet.")
        print("  Neu erzeugen mit:")
        print("    python3 research/vorregistrierung/registerbericht.py")
        return 1
    print("Der Zahlenteil des Registers stimmt mit dem Code ueberein.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
