# Testauftrag TB-19 — Stabile Sortierung

**Autonom ausführbar.** Alles unten läuft ohne Rückfrage, ohne Netz und ohne
Zugangsdaten. Kein Schritt sendet eine Order, keiner ändert einen Parameter.
`broker/` wird nicht berührt, `--echt` kommt nirgends vor.

**Voraussetzungen:** Python 3.9+ mit `pandas`. Für Schritt 5 zusätzlich das
vollständige `trading-env` des Projekts.

Zweig: `claude/new-session-oxhn5e`, Basis `main`.

---

## Was geprüft werden soll

Zwei Auswertungen bauen aus `results/<bot>/equity_curve.csv` eine tägliche
Kapitalkurve:

* `shared/portfolio_overview.py` → `_daily_capital_curve_from_equity_df()`
  — speist die **Montags-Mail** und die **Dashboard-Portfolio-Sicht**
* `strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py`
  → `build_daily_capital_curve()`

Beide sortieren nach `time` und nehmen dann `groupby("date").last()`. Ohne
`kind="stable"` vertauscht Quicksort Zeilen mit **gleichem Zeitstempel** —
und `.last()` greift dann einen Zwischenstand mitten im Tag ab statt des
Tagesschlusses.

**Die Zusicherung, um die es geht:**

> Der Tageswert ist der `capital_after` der in der **Eingabereihenfolge**
> letzten Zeile dieses Tages — unabhängig davon, wie viele Zeilen anderer
> Tage daneben stehen.

Der Zusatz nach dem Gedankenstrich ist der Kern: Fremdzeilen anderer Tage
können den Wert eines Tages inhaltlich nicht berühren. Unter einer
instabilen Sortierung tun sie es trotzdem, weil Quicksorts Vertauschung an
Länge und Lage des ganzen Feldes hängt.

---

## Schritt 1 — Der Selbsttest

```bash
cd ~/trading-bot
python3 shared/test_stabile_sortierung.py
```

**Erwartet:** `Ergebnis: 46 bestanden, 0 fehlgeschlagen`

Zwischendrin stehen bewusst `FEHLT`-Zeilen mit dem Vorspann
`(Mutante '…' - die folgenden FEHLT-Zeilen sind das Ziel)`. Das sind die
Mutationsproben: dort **muss** etwas fehlschlagen. Die Zeile darunter
(`OK Mutante '…': genau [...] schlägt an`) ist das eigentliche Ergebnis.

Schneller Durchlauf ohne die beiden langen Abschnitte:

```bash
python3 shared/test_stabile_sortierung.py --schnell   # erwartet: 41 von 41
```

### Was der Test tut — und was er bewusst nicht tut

Er prüft **Verhalten**, nicht Quelltext. Eine Textsuche nach `kind="stable"`
wäre hier besonders wertlos: sie prüft genau das, was der Diff ohnehin
zeigt.

| Abschnitt | Prüft | Hängt ab an |
|---|---|---|
| 1 | **Kernfall.** Alle Zeilen eines Tages auf demselben Zeitstempel, daneben 0–12 Zeilen anderer Tage. Der Tageswert muss bei **jeder** dieser Längen derselbe sein. | nur der **Stabilität** |
| 2 | Ein Tag mit drei **verschiedenen** Uhrzeiten, absteigend abgelegt. Der Tageswert muss der späteste sein. | nur **dass** sortiert wird |
| 3 | Gegenprobe: ohne doppelte Zeitstempel liefern stabile und instabile Fassung **dieselbe** Kurve. | — |
| 4 | Wiederholbarkeit: beide Skripte zweimal, byteweise dieselbe Ausgabe. Dazu: jede der neun abgelegten Kurven enthält tatsächlich doppelte Zeitstempel. | — |
| 5 | **Mutationsproben** (siehe unten) | — |
| 6 | `shared/ergebniskurven.py` meldet `9x AKTUELL` | — |
| 7 | `git status` unverändert — der Test schreibt nicht ins Repo | — |

### Die beiden Fallen, die umgangen sind

**Falle 1 — die selbstbestätigende Probe.** Der Erwartungswert wird nirgends
aus einem Lauf der geprüften Funktion gewonnen, sondern aus der
**Konstruktion der Eingabe** hergeleitet (die zuletzt eingefügte Zeile des
Tages). Und dass die Probe überhaupt unterscheidet, wird nicht
vorausgesetzt, sondern am **Ablauf** nachgewiesen: derselbe Fall läuft
zusätzlich gegen eine **mutierte Kopie** der echten Datei.

**Falle 2 — die zweite Wache verdeckt das Fehlen der ersten.** In der einen
geänderten Zeile stecken zwei Wachen: *dass* sortiert wird und dass
**stabil** sortiert wird. Abschnitt 1 (nur Gleichstände) kann ausschließlich
an der Stabilität scheitern — fiele die Sortierung ersatzlos weg, bestünde
er weiterhin. Abschnitt 2 (keine Gleichstände) kann ausschließlich daran
scheitern, dass gar nicht sortiert wird. Abschnitt 5 behauptet diese
Trennung nicht, sondern **misst** sie: je Mutante wird festgehalten, welche
Abschnitte anschlagen, und es müssen **genau** die erwarteten sein — nicht
mehr und nicht weniger.

| Mutante | muss anschlagen | darf nicht anschlagen |
|---|---|---|
| `kind="stable"` entfernt | Abschnitt 1 | Abschnitt 2 |
| Sortierung ersatzlos entfernt | Abschnitt 2 | Abschnitt 1 |

Mutiert wird die **echte Datei**, in einer Kopie unter `/tmp`. Das Repo
bleibt unberührt — Abschnitt 7 weist das per `git status` nach.

---

## Schritt 2 — Die verschobenen Zahlen von Hand nachsehen

```bash
cd ~/trading-bot
python3 strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py | tail -6
```

**Erwartet:** `Max Drawdown kombiniert:  -9.41%` (vorher −9,34 %)

```bash
python3 shared/portfolio_overview.py | grep "Max Drawdown kombiniert"
```

**Erwartet:** `-11.41%` (vorher −11,29 %)

Beide Werte sind die, die `research/exposure_messung/` auf demselben
Datenstand ausgewiesen hat.

> **Hinweis:** `shared/portfolio_overview.py` schreibt dabei
> `results/portfolio_overview/*.csv` neu — das ist seine Aufgabe. Nach dem
> Schritt zeigt `git status` diese Datei als geändert. Mit
> `git checkout results/portfolio_overview/` zurücksetzen, falls
> unerwünscht.

---

## Schritt 3 — Gegenprobe auf den echten Daten

Zeigt, dass der Fall kein Laborfall ist: wie viele Tage je Bot einen anderen
Kapitalstand bekommen.

```bash
cd ~/trading-bot && python3 - <<'EOF'
import pandas as pd, glob
def tageswerte(df, kind):
    d = df.sort_values("time", **({} if kind is None else {"kind": kind})).copy()
    d["date"] = d["time"].dt.normalize()
    return d.groupby("date")["capital_after"].last()
for p in sorted(set(glob.glob("results/**/equity_curve.csv", recursive=True))):
    df = pd.read_csv(p, parse_dates=["time"])
    a, b = tageswerte(df, None), tageswerte(df, "stable")
    print(f"{p:52s} Tage={len(a):5d}  abweichend={int((a != b).sum()):5d}  "
          f"Datei chronologisch={df['time'].is_monotonic_increasing}")
EOF
```

**Erwartet:** neun Zeilen, jede mit `Datei chronologisch=True` und einer
Abweichungszahl zwischen 1 (`elliott_wave`) und 698 (`turtle_soup_stocks`).

Das `chronologisch=True` ist der Beleg dafür, dass die **stabile** Variante
die richtige ist: die Datei steht bereits in Ereignisreihenfolge, und eine
stabile Sortierung lässt sie unverändert.

---

## Schritt 4 — Die abgelegten Kurven sind unberührt

```bash
cd ~/trading-bot && python3 shared/ergebniskurven.py | tail -3
```

**Erwartet:** `Zusammenfassung: 9x AKTUELL`, Rückgabewert 0.

Diese Aufgabe ändert keine Kurve, nur die Auswertung darüber.

---

## Schritt 5 — Die bestehenden Selbsttests

```bash
cd ~/trading-bot
for t in $(find . -name "test_*.py" -not -path "./.git/*" | sort); do
  echo "### $t"; python3 "$t" >/tmp/t.out 2>&1; echo "  RC=$?"; tail -2 /tmp/t.out
done
```

**Erwartet:** dasselbe Bild wie auf unverändertem `main`. Falls etwas
fehlschlägt, zum Vergleich den Basislauf machen:

```bash
git stash && for t in ...   # gleiche Schleife
git stash pop
```

Zwei bekannte Umgebungseffekte:

* **Ohne `node`** überspringt `dashboard/test_dashboard.py` vier Prüfungen
  und meldet **780/780 statt 784** — das sieht grün aus, ist aber weniger
  geprüft. Mit `node` im Pfad müssen es 784 sein.
* In einer Umgebung **ohne die Bot-Abhängigkeiten** (`binance`, `scipy`,
  `fastapi`) schlagen einzelne Tests fehl. Das ist **vorbestehend** und mit
  dem Basislauf auf unverändertem `main` nachzuweisen — nicht eine Folge
  dieser Änderung.

---

## Schritt 6 — Der Diff selbst

```bash
cd ~/trading-bot && git diff main -- shared/portfolio_overview.py \
    strategies/rsi2_mean_reversion/portfolio_correlation_analysis.py
```

**Erwartet:** genau zwei geänderte Sortierzeilen plus ein erklärender
Kommentarblock in `portfolio_correlation_analysis.py`. In
`portfolio_overview.py` steht **nur** die Sortierzeile — die Datei wurde in
früheren Aufgaben ausdrücklich nur aufgerufen, nicht geändert.

Keine `live_params.py`, keine `forward_test.py`, keine
`equity_simulation.py`, keine `results/*/equity_curve.csv`, nichts unter
`broker/`.

---

## Abbruchkriterien

Der Test gilt als **nicht bestanden**, wenn eines davon eintritt:

1. Schritt 1 meldet auch nur eine fehlgeschlagene Prüfung.
2. Eine Mutante schlägt **nicht** an (dann prüft der Test nichts) oder
   schlägt in **mehr** Abschnitten an als erwartet (dann greift eine Wache
   zu weit).
3. Schritt 2 liefert andere Zahlen als −9,41 % bzw. −11,41 %.
4. Schritt 4 meldet nicht `9x AKTUELL`.
5. Ein bestehender Selbsttest schlägt fehl, der auf unverändertem `main`
   besteht.
