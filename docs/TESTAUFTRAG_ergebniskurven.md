# Testauftrag: Ergebniskurven erneuert und gegen Veralterung gesichert

**Für eine lokale Claude-Code-Sitzung auf dem Mac.**

Geprüfter Stand: Branch `claude/new-session-bb4yi0`, Basis `origin/main`
(`317e6b9`, nach Merge von PR #84).

> ## Was diese Sitzung darf
>
> **Alle Schritte laufen ohne Rückfragen durch.** Diese Änderung fasst keine
> Bot-Datenbank an, löst keinen Trade aus, sendet keine Order und verändert
> keine Kursdatei unter `data/`.
>
> **Nicht anfassen:** `live_params.py`, `forward_test.py`,
> `equity_simulation.py`, `shared/portfolio_overview.py`,
> `dashboard/portfolio_sicht.py`, alles unter `broker/`, Crontab,
> launchd-Vorlagen. Kein `--echt` irgendwo.
>
> **Zwei Schritte schreiben absichtlich** in den Arbeitsbaum: Schritt 6
> (`--erzeugen`) und Schritt 9 (Montags-Mail). Beide Male steht dabei, was
> danach in `git status` stehen darf. Jede andere Änderung ist ein Befund.
>
> **Nicht starten:** `research/hrp_portfolio/nachtrag_sync_korrektur*.py` und
> `research/trend_overlay/nachtrag_sync_korrektur*.py`. Diese Module sind
> **nicht rein lesend** — sie überschreiben ihre eigenen
> `corrected_curves*/`-Schnappschüsse. Schritt 11 benutzt stattdessen ein
> Modul, das das nicht tut.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short              # muss LEER sein
git rev-parse --abbrev-ref HEAD
git log --oneline -3
python3 -c "import pandas; print('pandas', pandas.__version__)"
```

Erwartet: Branch `claude/new-session-bb4yi0`, die beiden obersten Commits sind
„Ergebniskurven aller neun Bots neu erzeugt" und „Wiederholungssperre: …".

---

## Schritt 1 — Die Prüfung ist grün

```bash
python3 shared/ergebniskurven.py
echo "Rueckgabewert: $?"
```

Erwartet:

* `Zusammenfassung: 9x AKTUELL`
* `Alle geprueften Kurven passen zur heutigen Konfiguration.`
* **Rückgabewert 0**

Der Lauf dauert rund **50 Sekunden** (ein Python-Prozess je Bot).

```bash
git status --short              # nach dem Lauf wieder LEER
```

**Ist die Arbeitskopie nicht leer, ist das ein Befund.** Die Prüfung darf
keine Datei anfassen — das ist eine der Kernzusicherungen.

---

## Schritt 2 — Die Selbsttests

```bash
python3 shared/test_ergebniskurven.py
echo "Rueckgabewert: $?"
```

Erwartet: **44 von 44 Prüfungen bestanden**, Rückgabewert 0. Dauer rund eine
Minute.

Besonders zu lesen sind zwei Zeilen in Abschnitt 3:

```
  [OK ] die Zeilenzahl ist unveraendert geblieben   207 vorher, 207 nachher
  [OK ] eine reine Zeilenzahl-Wache waere hier blind geblieben
```

Das ist die eigentliche Zusicherung: Die Prüfung schlägt an, **obwohl** die
Zeilenzahl gleich bleibt.

```bash
git status --short              # wieder LEER
```

---

## Schritt 3 — Die Leerprobe (die Prüfung muss rot werden können)

Ohne diesen Schritt ist Schritt 2 nichts wert. Der Inhaltsvergleich wird
gezielt entfernt; Abschnitt 3 muss dann **fehlschlagen**.

```bash
cp shared/ergebniskurven.py /tmp/ek.bak
python3 - <<'EOF'
p = "shared/ergebniskurven.py"
s = open(p).read()
alt = '        ungleich = (a.iloc[:gemeinsam] != b.iloc[:gemeinsam]).any(axis=1)'
neu = '        ungleich = (a.iloc[:gemeinsam].head(0) != b.iloc[:gemeinsam].head(0)).any(axis=1)'
assert s.count(alt) == 1, "Zeile nicht gefunden - Leerprobe waere wirkungslos"
open(p, "w").write(s.replace(alt, neu))
print("Inhaltsvergleich entfernt")
EOF

python3 shared/test_ergebniskurven.py | sed -n '/3) KERN/,/^4)/p'
```

Erwartet in Abschnitt 3:

```
  [FEHLER] nach der Aenderung Rueckgabewert 1
  [FEHLER] meldet ABWEICHEND
  [FEHLER] der Inhaltsvergleich sieht den Unterschied
```

Und weiterhin **grün**:

```
  [OK ] die Zeilenzahl ist unveraendert geblieben   207 vorher, 207 nachher
  [OK ] eine reine Zeilenzahl-Wache waere hier blind geblieben
```

Genau das ist der Nachweis: Der Prüffall ist so gewählt, dass **nur** der
Inhaltsvergleich ihn fangen kann. (Abschnitt 4 — der HRP-Fall — bleibt bei
dieser Leerprobe grün, weil sich dort die Zeilenzahl mitändert und die
Zeilenzahl-Wache ihn ebenfalls fängt. Auch das ist erwartet.)

**Zurücksetzen, unbedingt:**

```bash
cp /tmp/ek.bak shared/ergebniskurven.py
git status --short               # muss wieder LEER sein
```

---

## Schritt 4 — Die Erzeugung ist wiederholbar

```bash
md5 results/equity_curve.csv results/*/equity_curve.csv > /tmp/md5_a.txt
python3 shared/ergebniskurven.py --erzeugen > /dev/null
rmdir results/elliott_wave 2>/dev/null    # leerer Ordner, falls angelegt
md5 results/equity_curve.csv results/*/equity_curve.csv > /tmp/md5_b.txt
diff /tmp/md5_a.txt /tmp/md5_b.txt && echo "BYTEWEISE GLEICH"
git status --short
```

Erwartet: `BYTEWEISE GLEICH`, und `git status --short` zeigt **höchstens**
`results/portfolio_overview/portfolio_overview_curve_live.csv` — sonst nichts.
(Unter Linux statt `md5` bitte `md5sum`.)

---

## Schritt 5 — Die vier unveränderten Bots (Gegenprobe der Erzeugung)

```bash
python3 shared/ergebniskurven.py --erzeugen | grep -E "unveraendert|geschrieben"
```

Erwartet — genau diese vier als `unveraendert`:

```
  rsi2_crypto: unveraendert
  t3_supertrend: unveraendert
  turtle_soup_crypto: unveraendert
  volatility_breakout_crypto: unveraendert
```

und die übrigen fünf ebenfalls als `unveraendert` (sie wurden im Commit ja
bereits erneuert).

**Warum das der wichtigste Einzelschritt ist:** Ein Verfahren, das *alle* neun
Kurven verändert, hat nichts bewiesen. Dass vier Bots byteweise identisch
herauskommen, belegt, dass die Erzeugung den Bot trifft und nicht etwas
anderes.

---

## Schritt 6 — Der Befund lässt sich künstlich herbeiführen

Eine Kurve wird gezielt verfälscht; die Prüfung muss sie finden **und den
Grund benennen**.

```bash
cp results/rsi2_crypto/equity_curve.csv /tmp/rsi2_crypto_echt.csv

# Genau EINE Zahl in der Mitte verändern - Zeilenzahl bleibt gleich.
python3 - <<'EOF'
import pandas as pd
p = "results/rsi2_crypto/equity_curve.csv"
df = pd.read_csv(p)
df.loc[100, "capital_after"] = round(df.loc[100, "capital_after"] + 1.0, 2)
df.to_csv(p, index=False)
print("eine Zelle geaendert, Zeilen:", len(df))
EOF

python3 shared/ergebniskurven.py --bot rsi2_crypto
echo "Rueckgabewert: $?"
```

Erwartet: `[!!] ABWEICHEND`, Rückgabewert **1**, und eine Zeile

```
  Erste abweichende Zeile (100), Spalten capital_after:
```

**Zurücksetzen:**

```bash
cp /tmp/rsi2_crypto_echt.csv results/rsi2_crypto/equity_curve.csv
git status --short               # LEER (bzw. nur die portfolio_overview-Datei)
python3 shared/ergebniskurven.py --bot rsi2_crypto | tail -2
```

Erwartet danach wieder `AKTUELL`.

---

## Schritt 7 — `VERALTET` und `--nur-abweichung`

```bash
cp results/t3_supertrend/equity_curve.csv /tmp/t3_echt.csv
python3 - <<'EOF'
import pandas as pd
p = "results/t3_supertrend/equity_curve.csv"
df = pd.read_csv(p)
df.head(len(df) - 30).to_csv(p, index=False)     # 30 Zeilen abschneiden
EOF

python3 shared/ergebniskurven.py --bot t3_supertrend | grep -E "VERALTET|ABWEICHEND|Grund"
python3 shared/ergebniskurven.py --bot t3_supertrend > /dev/null; echo "voreingestellt: $?"
python3 shared/ergebniskurven.py --bot t3_supertrend --nur-abweichung > /dev/null; echo "nur-abweichung: $?"

cp /tmp/t3_echt.csv results/t3_supertrend/equity_curve.csv
```

Erwartet: Marke `[!] VERALTET` (nicht ABWEICHEND), Grund „der gemeinsame Teil
stimmt, es fehlen 30 spätere Zeilen (neue Kursdaten)", voreingestellt
Rückgabewert **1**, mit `--nur-abweichung` Rückgabewert **0**.

Das ist die Trennung, ohne die ein Cronjob jeden Tag melden würde.

---

## Schritt 8 — Der Live-Betrieb ist nicht betroffen

```bash
git diff --stat 317e6b9..HEAD -- strategies/ broker/
```

Erwartet: **leer**. Kein Bot-Code, keine `live_params.py`, nichts unter
`broker/`.

```bash
ls broker/STOP broker/STOP_IBKR 2>/dev/null   # falls vorhanden, unveraendert
python3 shared/status_overview.py 2>/dev/null | head -20
```

Die Bots müssen unverändert laufen; das Werkzeug wird von keinem Bot
aufgerufen.

---

## Schritt 9 — Die verschobenen Zahlen nachvollziehen

```bash
python3 shared/portfolio_overview.py | grep -E "Vergleichsfenster|Rendite im Fenster|Max Drawdown kombiniert"
```

Erwartet:

```
Gemeinsames Vergleichsfenster: 2022-03-18 bis 2026-08-20
  Rendite im Fenster:        69.68%
  Max Drawdown kombiniert:   -11.29%
```

Zum Vergleich die alten Zahlen (Fenster bis **2026-06-27**, Rendite
**+80,52 %**, Drawdown **−6,24 %**). Wer sie selbst sehen will:

```bash
git stash list                                  # sollte leer sein
git checkout 317e6b9 -- results/
python3 shared/portfolio_overview.py | grep -E "Vergleichsfenster|Rendite im Fenster|Max Drawdown kombiniert"
git checkout HEAD -- results/                   # UNBEDINGT zurueck
git status --short
```

Dann das Dashboard:

```bash
python3 dashboard/portfolio_sicht.py --berechnen | tail -6
```

Erwartet: Gruppe `alle`: 9 Bots, 2022-03-18 bis 2026-08-20, Rendite
**+69.68 %**, max. Drawdown **−11.29 %**. Gruppe `nur_echte_trades`: „keine
Zahl" (kein Bot erreicht die Schwelle von 10 Live-Trades).

Und der kombinierte Vierer-Drawdown:

```bash
cd strategies/rsi2_mean_reversion
python3 portfolio_correlation_analysis.py | sed -n '/MAX DRAWDOWN JE BOT/,$p'
cd ~/trading-bot
```

Erwartet: kombiniert **−9,34 %** (vorher −1,43 %), Rendite im Fenster
**+74,69 %** (vorher +140,92 %).

```bash
git status --short
```

Erwartet: nur `results/portfolio_overview/portfolio_overview_curve_live.csv`
(von `portfolio_overview.py` selbst geschrieben) und gegebenenfalls der
gitignorierte `dashboard_snapshot.json`. Danach:

```bash
git checkout -- results/portfolio_overview/
```

---

## Schritt 10 — Alle bestehenden Tests

```bash
for t in broker/test_broker.py broker/test_ibkr.py \
         dashboard/test_dashboard.py dashboard/test_portfolio_sicht.py \
         notifications/test_manual_close.py notifications/test_schliess_benachrichtigung.py \
         shared/test_empfehlung_format.py shared/test_kursdaten.py \
         shared/test_ergebniskurven.py \
         system/test_caffeinate_plist.py system/test_log_rotation.py; do
  printf "%-52s " "$t"; python3 "$t" > /tmp/t.log 2>&1; echo "exit=$?  $(grep -i bestanden /tmp/t.log | tail -1)"
done
```

Erwartet: überall `exit=0`.

> **Achtung `dashboard/test_dashboard.py`:** Ohne `node` überspringt es vier
> Prüfungen und meldet **780/780 statt 784** — das sieht grün aus, ist aber
> unvollständig. Auf dem Mac des Nutzers ist `node` derzeit nicht installiert.
> Steht dort 780, ist das kein Fehler dieser Änderung; in der Cloud-Sitzung
> (mit `node`) waren es 784/784.

Die Untersuchungen:

```bash
for t in research/*/test_*.py; do
  printf "%-58s " "$t"; timeout 1200 python3 "$t" > /tmp/t.log 2>&1; echo "exit=$?"
done
git status --short                # muss LEER sein
```

Erwartet: `exit=0` überall — mit **zwei bekannten Ausnahmen**:

* `research/elliott_wave_params/test_params.py` braucht ein Argument
  (`elliott_wave` oder `elliott_wave_stocks`) und gibt sonst nur seine
  Benutzungszeile aus. **Kein Fehler.**
* `research/exposure_messung/test_exposure_kern.py` meldet **1** von
  23 Prüfungen als fehlgeschlagen („am Tag mit nur einem gültigen Kurs zählt
  dieser allein"). **Vorbestehend**, Ursache ist eine
  pandas-Verhaltensänderung bei `pct_change`, nicht eine Kurve — die Ausgabe
  ist vor und nach der Kurvenerneuerung Zeile für Zeile identisch.

---

## Schritt 11 — Der eine Folgebefund (HRP)

```bash
python3 research/hrp_portfolio/nachtrag_vbc_regimefilter.py | tail -12
echo "Rueckgabewert: $?"
```

Erwartet: Rückgabewert **1**, neun `FEHLGESCHLAGEN`-Zeilen, alle beginnend mit
`korrigiert_v1 /`, und der Abbruch „9 Abweichungen — der Vergleich wäre nicht
belastbar."

**Das ist bekannt und im Übergabedokument Abschnitt 5 erklärt:** Der Anker
`korrigiert_v1` liest vier Kurven (darunter `elliott_wave`) **live** aus
`results/`, statt sie wie die übrigen Anker eingefroren zu halten. Die
**Kernaussage** des HRP-Berichts ist davon nicht betroffen — sie hängt an
`korrigiert_v2` gegen `v2_mit_regimefilter`, und `korrigiert_v2` bestätigt im
selben Lauf weiterhin alle neun Werte (die `OK`-Zeilen darüber).

Die entscheidende Frage des Auftrags lautete anders und ist beantwortet:

```bash
git diff 317e6b9..HEAD --stat -- results/volatility_breakout_crypto/
```

Erwartet: **leer**. Die eine Kurve, an der dort das Vorzeichen hängt, ist
unverändert.

```bash
git status --short                # muss LEER sein - dieses Modul schreibt nicht
```

---

## Schritt 12 — Abschluss

```bash
git status --short                # LEER
python3 shared/ergebniskurven.py | tail -2
echo "Rueckgabewert: $?"
```

Erwartet: `Alle geprueften Kurven passen zur heutigen Konfiguration.`,
Rückgabewert 0.

---

## Was ein Befund wäre

| Beobachtung | Bedeutung |
|---|---|
| Schritt 1 meldet nicht `9x AKTUELL` | Die Kurven passen auf dem Mac nicht zu dem, was hier gerechnet wurde — dann die Kursdaten unter `data/` vergleichen (dort kommen täglich neue Kerzen dazu; `VERALTET` ist dann erwartbar, `ABWEICHEND` nicht). |
| `git status` nach Schritt 1, 2 oder 11 nicht leer | Eine Zusicherung ist gebrochen. |
| Schritt 3 bleibt in Abschnitt 3 grün | Der Test prüft nicht, was er zu prüfen behauptet. |
| Schritt 5 meldet weniger als vier `unveraendert` | Die Erzeugung trifft den Bot nicht. |
| Schritt 8 zeigt ein Diff in `strategies/` oder `broker/` | Bot-Code wurde angefasst — das war ausgeschlossen. |
| Schritt 11 meldet Fehler **ausserhalb** von `korrigiert_v1` | Eine weitere Grundlage hat sich verschoben als angenommen. |
