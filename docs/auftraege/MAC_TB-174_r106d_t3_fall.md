# TB-174 R106 (d) Weg 1: Fall nach R90 (g) bei t3_supertrend am Listen-Erzeuger herbeiführen, über den Gleichstand (Probe mit Gegenprobe nach 40.7) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 16:45** (Helfer BAU174, per Skript aus Bausteinen, `$HOME/sc/tb174/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis E an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `d81ef20` (vor TB-173); Start nach TB-173 am HEAD `5a01d55099aa3a91ff7fa7487e359568d5d3a26e`.**

**Sitzungstitel:** `TB-174` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `5a01d55099aa3a91ff7fa7487e359568d5d3a26e` (kommt bis zum Start ein Commit dazu, füllt der steuernde Chat HEAD und Soll neu) · **Start:** über den Sitzungswächter (`starte_TB-174`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-174_r106d_t3_fall.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (Python 3.9, numpy 2.0.2, pandas 2.3.3 nach `requirements.lock`); Werkzeug `docs/belege/TB-174/tb174_werkzeug.py` (Anhang A), kurz `WZ`. **Belege:** `docs/belege/TB-174/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-174_r106d_t3_fall.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FI ⇒ FJ, nach einer Kennung durch TB-173 FK).
**Grundlage:** R106 (d) (Register 66, mit TB-173 eingetragen; Quelle `docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md`, Registerblock), R105 (Z. 12464), R90 (g) (Z. 11997), R98 (d) (Z. 12231), R87 (c) (Z. 11909), 40.7 (Z. 8461); Zeilen am Bau-HEAD. Vorbild Bauart und Abnahme: `research/tb24_haltedauern/test_elliott_verdraengung.py` (TB-171), `test_listen_erzeuger.py` (TB-169). **Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ E (Probe schreiben und laufen lassen) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F. **Kein Registereintrag** (R106 (d): „Welcher Weg, ist Handwerk“; der Stand geht mit der nächsten Anfrage an den Verfahrensprüfer).

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 33 („Opus Trading Bots-16.10.2026 c“), 17.10.2026, 17:03, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-174 frei? TB-174 legt nur einen neuen Test an: research/tb24_haltedauern/test_t3_verdraengung.py. Der Test führt bei t3_supertrend den Fall nach R106 (d) herbei. Gemeint ist ein Einstieg vor dem Tag, dessen Position über den Tag offen bleibt, danach ein zweites Kreuzen nach oben über einen Gleichstand. Mit der Schranke erscheint der zweite Einstieg. Ohne Schranke oder mit falsch sitzender Schranke wird die Probe rot; an der Kopie waren das 3 bzw. 5 von 8, sonst 8 von 8. Der Handelscode bleibt unverändert, das prüft der Auftrag über md5. Es gibt keinen Registereintrag, kein Live und kein Geld. Der frische Gegenleser fand keinen Befund, der stoppt. Ein Risiko bleibt: Der Gleichstand entsteht durch Rundung. Findet der Mac mit seinen Bibliotheksfassungen keinen, wird die Probe rot und bricht ab. Fälschlich grün kann sie nicht werden; das hat der Gegenleser belegt. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Damit schliesst sich die letzte Abnahme vor dem Tag für t3_supertrend; schlägt die Rundung fehl, kostet das nur einen Abbruch ohne Schäden."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. TB-174 ändert keinen Handelscode und keine Datei der Sperrliste; neu ist eine Testdatei unter `research/tb24_haltedauern/`.

R106 (d) wörtlich (Quelle, Registerblock): „(d) t3_supertrend (R105 (d)). Die Fundstellen der Anfrage 17.10.a (backtest_trend.py Z. 70, 111–112, 123–124) nennen den Ort, an dem ein späterer Einstieg verdrängt würde (Einstieg nur bei position is None), und einen Grund für den Regelfall (Kreuzen nach unten schliesst vor dem nächsten Kreuzen nach oben, mit use_t3_exit). Zwei Öffnungen bleiben: use_t3_exit ist ein Parameter (Vorgabe True), und beim Gleichstand (Z. 112 „<=“, Z. 124 „<“) kann ein Kreuzen nach oben ohne vorheriges Kreuzen nach unten entstehen, das eine vor dem Tag geöffnete Position verdrängt. Ein Grenzfall ist ein Ort, an dem verdrängt wird (R105 (b)); durch Lesen ist er nicht auszuschliessen. Vor dem Tag schliesst ihn deshalb Weg 1 (der Fall wird auf dem Test-Snapshot herbeigeführt: Einstieg vor dem Tag, Position über den Tag offen, danach ein zweites Kreuzen nach oben; ohne Schranke fehlt es oder die Wache nach R87 (c) endet mit 2, mit Schranke erscheint es; 40.7), oder eine Tatsachennotiz mit Fundstelle sagt, dass use_t3_exit im Lauf und bei der Neuerzeugung nie False ist und der Gleichstand keinen Einstieg ohne Ausstieg bildet; dann greift die Ausnahme nach R90 (g). Welcher Weg, ist Handwerk.“

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen (die Probe rechnet auf dem synthetischen Test-Snapshot von `test_listen_erzeuger.py` im Temp-Ordner). Keine Neuerzeugung der neun Listen. Nichts unter `strategies/`, `shared/`, `data/`, `config/` ändern; unter `research/` nur die neue Datei aus E. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`, kein `rm`, kein `mv`.

## Die Probe (Anhang B, neu: `research/tb24_haltedauern/test_t3_verdraengung.py`, sha256 `492421a7fe0c6ffc63b0856d3c0e8ed13af8e1346c95db37e6e5007a6d3ab805`)

**Code (am Bau-HEAD gemessen, `strategies/t3_supertrend/backtest_trend.py`):** Einstieg nur bei `position is None` (Z. 111), Kreuzen nach oben `t3_fast[i - 1] <= t3_slow[i - 1] and t3_fast[i] > t3_slow[i]` (Z. 112), Schranke `i >= erster_einstieg` in der Einstiegsbedingung (Z. 114, `erster_einstieg` Z. 102); Ausstieg beim Kreuzen nach unten nur mit `use_t3_exit` und `t3_fast[i] < t3_slow[i]` (Z. 124, strikt). `use_t3_exit=True` ist die Vorgabe (Z. 70); `multi_symbol_optimise.get_trades_for_symbol` (Z. 90–102) und `equity_simulation.collect_all_trades` (Z. 75–103) übergeben ihn nicht, `bot_lauf.hole_trades` ruft `collect_all_trades` (Z. 149–152): im Lauf und bei der Neuerzeugung gilt True (Probe 0b prüft das). Der BTC-Regimefilter steht in `collect_all_trades` (Z. 98–101).

**Herbeiführung (nur an der Kopie im Temp-Ordner, R106 (b)):** Die Probe baut den Snapshot B wie `test_listen_erzeuger.py` (Seed 169, Versatz 0, ohne Zeilen ab dem Schnitt) und setzt in die 4h-Reihe `AAA` einen Kursabschnitt ein (open = high = low = close; davor flach bei 100, danach die alte Reihe auf den Endkurs skaliert): Abfall in 30 Balken von 100 auf L, 1 200 Balken konstant L, 6 Balken je +0,4 %. T3 fast und T3 slow schwingen nach dem Abfall um L (Kreuzen nach oben, nach unten, nach oben = **E1**, ADX 100); ab E1 bleibt fast ≥ slow, bei konstantem Kurs laufen beide auf denselben Gleitkommawert (**Gleichstand**). Am ersten Balken der Stufe (**s**) entsteht ein Kreuzen nach oben ohne vorheriges Kreuzen nach unten (Z. 112 `<=`; Z. 124 `<` greift am Gleichstand nicht). Ohne Schranke ist E1 (vor dem Tag) offen, das Kreuzen bei s wird verdrängt; mit Schranke (Tag = Datum von E1 + 10 Tage) entsteht vor dem Tag keine Position, **E2** erscheint bei s. Ob die Rundung den Gleichstand trifft, hängt von L ab: die Probe wählt (Anker, L) wiederholbar als ersten Kandidaten einer festen Liste (Anker ab 2024-06-03 wochenweise, L aus 63.0, 63.75, 67.25, …), der am Signalpfad alle Bedingungen erfüllt (auch BTC-Regime bei E1 und s), und gibt die Wahl in 0b aus. Am Bau: Anker 2024-06-10, L 63.0, E1 2024-08-05 08:00, Tag 2024-08-15, s 2025-01-01 00:00, Gleichstand 496 Balken, Ausstieg E1 ohne Schranke 2025-01-02 16:00.

**Prüfungen (geprüft an den Ausgaben des Erzeugers `positionen_holen.py`, Bauart `test_listen_erzeuger.lauf`):** 0 Signalpfad (Handwerk, R98 (d) letzter Satz; `collect_all_trades` mit Regimefilter): ohne Schranke E1 vor dem Tag und kein Einstieg bei s, mit Schranke kein Einstieg vor dem Tag und E2 bei s · 0b Gleichstand: von E1 bis s−1 nie fast < slow, fast == slow auf mindestens 60 Balken bis s−1, fast > slow bei s, ADX bei s über der Schwelle, E1 endet ohne Schranke nach s; `use_t3_exit` True und vom Erzeuger nicht übergeben · 1 Erzeuger mit Schranke: rc 0, kein Einstieg von `AAA` vor dem Tag, E2 bei s (entry_price wie am Signalpfad) · 2 **Gegenprobe nach 40.7**: Schranke aus ⇒ Wache R87 (c) beisst an einem Einstieg des Abschnitts vor dem Tag (am Bau: E1) und endet mit 2 · 3 Schranke und Wachen aus ⇒ E1 vor dem Tag mit Ausstieg nach s (Position über den Tag offen), kein Einstieg bei s (verdrängt) · 4 ohne Eingriff (Snapshot wie TB-169), gleicher Tag: `AAA` ohne Einstieg bei E1 und bei s · 5 `BBB`/`CCC`/`BTCUSDT` mit und ohne Tag für `AAA` gleich · 6 **Gegenprobe zur Lage der Schranke** (R105 (b), Mutante M1): eine Kopie von `backtest_trend.py` im Temp-Ordner der Probe mit der Schranke hinter der Zustandsmaschine (Einstieg ohne `i >= erster_einstieg`, Trades vor dem Tag erst in der Ausgabe gestrichen), im Kindprozess über `sitecustomize` (PYTHONPATH) statt des Originals geladen (Marke `.benutzt`) ⇒ rc 0 und kein Einstieg vor dem Tag, aber E2 fehlt. Am Bau: **8 von 8**, rund 25 s (Gerät, Python 3.10.12, pandas 2.3.3, numpy 2.2.6, `binance`/`yfinance` als Attrappen ohne Netz). Gegenproben am Bau an einer Kopie des Repos: Schranke in `backtest_trend.py` entfernt ⇒ rc 1 (3 von 8); Schranke hinter die Zustandsmaschine gelegt ⇒ rc 1 (4 von 8).

**Zur Kenntnis (nicht entschieden):** Der Gleichstand entsteht nur durch Rundung (Gleitkomma-Fixpunkte der zwölf EMA-Ketten); am Bau trifft er in einer Testreihe bei 8 von 97 L-Werten (60 bis 71,875 in Schritten von 0,125, und 64). Ob er am Mac bei derselben Wahl trifft, ist nicht gemessen; die Probe sucht deshalb selbst, und 0b gibt die Wahl aus. Findet sie keinen Kandidaten, sind alle 8 Prüfungen NEIN (Abbruchweg E).

## Lage nach dem Auslegen

Soll in 0a vom steuernden Chat gefüllt (`[' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-174_r106d_t3_fall.md']`); am Bau-HEAD wären es 5 Einträge gewesen: ` M docs/auftraege/AKTUELLER_AUFTRAG.md`, `?? docs/auftraege/MAC_TB-174_r106d_t3_fall.md`, `?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17a_r105c_weg1_elliott_t3.md`, `?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md`, `?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17a_eroeffnung.md`.

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `5a01d55099aa3a91ff7fa7487e359568d5d3a26e`, genau die Einträge `[' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-174_r106d_t3_fall.md']`, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb174_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-174_r106d_t3_fall.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "5a01d55099aa3a91ff7fa7487e359568d5d3a26e": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "5a01d55099aa3a91ff7fa7487e359568d5d3a26e": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-174_r106d_t3_fall.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (N Eintraege)` mit N = Zahl der Einträge im Soll. Anhänge holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-174_r106d_t3_fall.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb174_werkzeug.py 0e9f70b3c4db245af18867cc1631a4d96d189c126cc924410b52d12c2b17ab41`; `test_t3_verdraengung.py 492421a7fe0c6ffc63b0856d3c0e8ed13af8e1346c95db37e6e5007a6d3ab805`; `Dateien 2`; sonst **ABBRUCH**. Dann genau diese Zeilen (fügt die in 0a geprüften Pfade mit Namen hinzu), Commit `TB-174 Schritt 0: Stand des steuernden Chats vor TB-174 (Auftrag)`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
trading-env/bin/python3 -B -c "import subprocess, sys; z = [l[3:] for l in open(sys.argv[1], encoding='utf-8').read().split(chr(10)) if l]; print('git add', len(z)); raise SystemExit(subprocess.run(['git', 'add', '--'] + z).returncode)" "$TMPDIR/tb174_0a.txt"
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-174
cp "$TMPDIR/tb174_0a.txt" docs/belege/TB-174/0a_status.txt
cp "$TMPDIR/tb174_werkzeug.py" docs/belege/TB-174/tb174_werkzeug.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py voraussetzung > docs/belege/TB-174/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (17 Prüfungen: Handelscode und Erzeuger je md5 = Bau, Probe noch nicht im Repo, R106 mit (d) im Wortlaut — am Bau-HEAD vor TB-173 noch NEIN —, R105 genau einmal, BACKLOG Rang 1, Journal FI oder FJ). **Abbruch in V:** im Arbeitsbaum liegt nur der unverfolgte Ordner `BEL`. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-174/abbruch.txt`, dann `git add` mit Namen für `abbruch.txt`, `0a_status.txt`, die zwei Anhänge und `v_voraussetzung.txt`, Commit `TB-174 Abbruch: V`, pushen, `git status --porcelain` leer; melden.

## Schritt E — Probe schreiben und laufen lassen

```
cp "$TMPDIR/test_t3_verdraengung.py" research/tb24_haltedauern/test_t3_verdraengung.py
trading-env/bin/python3 -B research/tb24_haltedauern/test_t3_verdraengung.py > docs/belege/TB-174/e_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/e_probe.txt
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py nachher > docs/belege/TB-174/e_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/e_nachher.txt
```

Soll: `e_probe.txt` endet mit `Ergebnis: 8 von 8 bestanden` und `rc 0`; `e_nachher.txt` endet mit `rc 0` (Handelscode unverändert, Probe = Anhang, 8 ja). **Abbruchweg E** (ein Beleg nicht `rc 0`; kein E-Commit):

```
trading-env/bin/python3 -B -c "import os; t = 'research/tb24_haltedauern/test_t3_verdraengung.py'; d = 'docs/belege/TB-174/abbruch_test_t3_verdraengung.py'; da = os.path.exists(t); os.replace(t, d) if da else None; open('docs/belege/TB-174/abbruch.txt', 'w').write('E: erster Beleg ohne rc 0, siehe Belege\n' + ('Test nach BEL verschoben' if da else 'Test nicht vorhanden') + '\n')"
trading-env/bin/python3 -B -c "import os, subprocess; f = ['docs/belege/TB-174/' + x for x in ('abbruch.txt', 'abbruch_test_t3_verdraengung.py', '0a_status.txt', 'tb174_werkzeug.py', 'v_voraussetzung.txt', 'e_probe.txt', 'e_nachher.txt')]; d = [x for x in f if os.path.exists(x)]; print('git add', len(d), 'von', len(f)); raise SystemExit(subprocess.run(['git', 'add'] + d).returncode)"
git commit -q -m "TB-174 Abbruch: E"
git push -q origin main
git status --porcelain
```

Der Abbruchweg fügt nur Belege hinzu, die vorhanden sind (eine Python-Zeile prüft jeden Pfad vor `git add`); fehlt der Test, schreibt er „Test nicht vorhanden“ in `abbruch.txt`. Soll danach: `git status --porcelain` ohne Ausgabe; scheitert der Push: melden, nicht wiederholen. Sonst (alle grün) genau diese `git add`, Commit `TB-174 E: Probe R106 (d) Weg 1 (t3_supertrend, Fall nach R90 (g))`, pushen ⇒ **⟨E⟩**:

```
git add research/tb24_haltedauern/test_t3_verdraengung.py
git add docs/belege/TB-174/0a_status.txt
git add docs/belege/TB-174/tb174_werkzeug.py
git add docs/belege/TB-174/v_voraussetzung.txt
git add docs/belege/TB-174/e_probe.txt
git add docs/belege/TB-174/e_nachher.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ kennung`. Block nach `docs/belege/TB-174/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-174: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-174_r106d_t3_fall.md` mit: Kurz; V wörtlich (letzte Zeilen); E (die 8 Zeilen aus `e_probe.txt` wörtlich, mit der Wahl aus 0b, Laufzeit); Zur Kenntnis (der Absatz oben); Offen (R106 (d) geschlossen? Frage an den Verfahrensprüfer); Abweichungen; In einfacher Sprache. Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Dann:

```
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py kennung > docs/belege/TB-174/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-174/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-174/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py journal docs/belege/TB-174/a_block.md --probe > docs/belege/TB-174/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-174/tb174_werkzeug.py journal docs/belege/TB-174/a_block.md > docs/belege/TB-174/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-174/a_journal.txt
```

Soll je `rc 0`. Genau diese `git add`, Commit `TB-174 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-174_r106d_t3_fall.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-174/a_kennung.txt
git add docs/belege/TB-174/a_backlog_probe.txt
git add docs/belege/TB-174/a_backlog.txt
git add docs/belege/TB-174/a_block.md
git add docs/belege/TB-174/a_journal_probe.txt
git add docs/belege/TB-174/a_journal.txt
```

**F.**

```
git status --porcelain > "$TMPDIR/tb174_f.txt"
cp "$TMPDIR/tb174_f.txt" docs/belege/TB-174/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-174/f_numstat.txt
git add docs/belege/TB-174/f_porcelain.txt
git add docs/belege/TB-174/f_numstat.txt
git commit -q -m "TB-174 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; im numstat unter `research/` genau die neue Probe.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V nicht `rc 0`; ein Beleg aus E nicht `rc 0` (dann Abbruchweg E, **kein E-Commit**); A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Der T3-Bot darf vor dem Tag, ab dem ein Symbol handelbar ist, nicht einsteigen. Wäre er zu früh eingestiegen, könnte die offene Position ein späteres Kaufsignal blockieren. Das passiert nur in einem Sonderfall: wenn die zwei T3-Linien genau gleich hoch liegen. Der neue Test baut diesen Fall gezielt in eine Kopie der erfundenen Testkurse ein und zeigt: mit der Sperre kommt das spätere Signal durch, ohne die Sperre fehlt es. Am Handelscode ändert sich nichts.

## Anhänge

### Anhang A — Werkzeug

<!-- DATEI tb174_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-174 Werkzeug (Anhang A): R106 (d) Weg 1 bei t3_supertrend - Voraussetzungen, Nachher-Pruefung (Handelscode unveraendert, Probe gruen), Kennung, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-174/"
TEST, TSHA = "research/tb24_haltedauern/test_t3_verdraengung.py", "492421a7fe0c6ffc63b0856d3c0e8ed13af8e1346c95db37e6e5007a6d3ab805"
CODE = { "strategies/t3_supertrend/backtest_trend.py": "896948ee3eca909cded1e68e1c471310", "strategies/t3_supertrend/indicators.py": "8452ad509b7ae9ad9b4ec656995f975c", "strategies/t3_supertrend/multi_symbol_optimise.py": "dc85993e8d42647dea2eb2593335aab8", "strategies/t3_supertrend/equity_simulation.py": "be665a734328d8a1d8231ff211a55a85", "strategies/t3_supertrend/live_params.py": "f28553e8deba39ea68329af10ecd19d6", "strategies/t3_supertrend/regime_filter.py": "b02087926d7d6b376a47b19115f1ca58", "shared/regimewache.py": "82cd933f9ba9b3a3c26ab23b87c1cb69", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/test_listen_erzeuger.py": "d77e73ed5ff7a737a22e53879ff72575", "research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "research/faltenplan_neun/faltenschranke_messung.py": "584d9ff959dab7428a97a945b091e118" }
R106D = "Vor dem Tag schliesst ihn deshalb Weg 1 (der Fall wird auf dem Test-Snapshot herbeigeführt"
RANG1, N = "| **1** | **TB-30b Mass-Reparatur**", 8
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "Handelscode/Erzeuger unveraendert: %s md5 %s" % (f, m[:12]))
def voraussetzung():
    code_gleich(); p(not os.path.exists(TEST), "Probe noch nicht im Repo: " + TEST)
    reg = lies(REG).split("\n"); r106 = [l for l in reg if l.startswith("> R106 — ")]
    p(len(r106) == 1 and R106D in r106[0] and "use_t3_exit" in r106[0], "Register: R106 genau einmal, (d) Weg 1 bei t3_supertrend im Wortlaut (nach TB-173)")
    p(sum(l.startswith("> R105 — ") for l in reg) == 1, "Register: R105 genau einmal")
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-174" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-174")
    k = kennungen(); p(max(k) in ("FI", "FJ"), "Journal: hoechste %s (FI am Bau-HEAD, FJ falls TB-173 eine Kennung setzt)" % max(k))
    ende()
def nachher():
    code_gleich()
    p(os.path.exists(TEST) and hashlib.sha256(open(TEST, "rb").read()).hexdigest() == TSHA, "Probe im Repo = Anhang (sha256 %s)" % TSHA[:12])
    e = lies(BEL + "e_probe.txt").rstrip("\n").split("\n") if os.path.exists(BEL + "e_probe.txt") else [""]
    p(e[-1] == "rc 0" and len(e) > 1 and e[-2] == "Ergebnis: %d von %d bestanden" % (N, N), "e_probe.txt endet mit 'Ergebnis: %d von %d bestanden' und 'rc 0'" % (N, N))
    p(not any(l.startswith("NEIN") for l in e) and sum(l.startswith("ja    ") for l in e) == N, "e_probe.txt: %d ja-Zeilen, keine NEIN-Zeile" % N)
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-174" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-174"):
        z[a[0]] = z[a[0]][:-2] + (" · **TB-174 (%s, Journal %s): R106 (d) Weg 1 bei `t3_supertrend`, Probe `%s` am Listen-Erzeuger, 8 von 8** "
            "(Fall nach R90 (g) über den Gleichstand auf dem Test-Snapshot herbeigeführt durch einen eingesetzten Kursabschnitt: Einstieg vor dem Tag, Position über den Tag offen, "
            "danach ein Kreuzen nach oben am Gleichstand T3 fast = T3 slow ohne Kreuzen nach unten; mit Schranke erscheint der zweite Einstieg; Gegenprobe 40.7: Schranke aus ⇒ Wache R87 (c) endet mit 2, "
            "Schranke und Wachen aus ⇒ der zweite Einstieg fehlt; Mutante mit der Schranke hinter der Zustandsmaschine an einer Kopie von `backtest_trend.py` ⇒ der zweite Einstieg fehlt; "
            "`use_t3_exit` im Lauf True, vom Erzeuger nicht übergeben); offen, an den Verfahrensprüfer: ob R106 (d) damit geschlossen und die Abnahme nach R98 (d) in 64.1 für t3_supertrend vollständig ist |") % (datum, kenn, TEST)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-174: " % neu), "Kopfzeile ## %s — TB-174: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif a == ["nachher"]: nachher()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

### Anhang B — Probe

<!-- DATEI test_t3_verdraengung.py -->
````python
#!/usr/bin/env python3
"""TB-174 (R106 (d), R105 (d); R90 (g), R98 (d), R87 (c), 40.7): Fall nach R90 (g) bei t3_supertrend am Listen-Erzeuger
research/tb24_haltedauern/positionen_holen.py, ueber den Gleichstand (backtest_trend.py Z. 112 "<=", Z. 124 "<"), auf dem Test-Snapshot von
test_listen_erzeuger.py (TB-169, Seed 169, Versatz 0, Snapshot B ohne Zeilen ab dem Schnitt), mit einem Eingriff NUR an der Kopie im
Temp-Ordner (R106 (b)): In die 4h-Reihe von AAA wird ab ANKER ein Kursabschnitt eingesetzt (Kerzen mit open = high = low = close; davor
die Reihe flach bei 100, danach die alte Reihe, auf den Endkurs skaliert):
  Abfall in ND Balken von 100 auf L, dann M Balken konstant L, dann STUFE Balken je +0.4 %. Nach dem Abfall schwingen T3 fast/slow
  (Faktor 0.7) um L: Kreuzen nach oben (R0), nach unten, nach oben (E1, Einstieg, ADX > Schwelle). Ab E1 bleibt T3 fast >= T3 slow;
  bei konstantem Kurs laufen beide auf denselben Gleitkommawert (Gleichstand, fast == slow). Der erste Balken der Stufe (s) bildet
  ein Kreuzen nach oben OHNE vorheriges Kreuzen nach unten (Z. 112 "<=" am Gleichstand, Z. 124 "<" greift nicht).
  Ohne Schranke ist E1 (vor dem Tag) offen, das Kreuzen bei s wird verdraengt (Einstieg nur bei position is None, Z. 111).
  Mit Schranke (Z. 114, i >= erster_einstieg; Tag zwischen E1 und s) entsteht vor dem Tag keine Position, E2 erscheint bei s.
  Ob die Rundung den Gleichstand trifft, haengt von L ab (Gleitkomma-Fixpunkte der EMA-Ketten): die Probe waehlt (ANKER, L) aus einer
  festen Liste als ersten Kandidaten, der am Signalpfad alle Bedingungen erfuellt (wiederholbar, ausgegeben in Pruefung 0b).
Handelscode unveraendert; data/ wird nicht gelesen; geprueft an den AUSGABEN des Erzeugers (t3_supertrend_alle_trades.csv, rc).
   0 Signalpfad (Handwerk, R98 (d) letzter Satz; collect_all_trades mit BTC-Regimefilter): ohne Schranke E1 vor dem Tag, kein Einstieg bei s;
     mit Schranke (entry_cutoff = Tag) kein Einstieg vor dem Tag, E2 bei s
   0b Gleichstand: von E1 bis s-1 nie T3 fast < T3 slow (kein Kreuzen nach unten), fast == slow auf mindestens 60 Balken bis s-1,
     fast > slow bei s, ADX bei s > Schwelle, E1 endet nach s; use_t3_exit im Lauf True (Vorgabe Z. 70, der Erzeuger uebergibt ihn nicht)
   1 Erzeuger mit Schranke (Tag {AAA: Tag}): rc 0, kein Einstieg von AAA vor dem Tag, E2 bei s (entry_price wie am Signalpfad)
   2 Gegenprobe (40.7, R87 (c)): Schranke aus -> Wache R87 (c) beisst an einem Einstieg des eingesetzten Abschnitts vor dem Tag, endet mit 2
   3 Schranke und Wachen aus -> rc 0, E1 vor dem Tag mit Ausstieg nach s (Position ueber den Tag offen), kein Einstieg bei s (verdraengt)
   4 ohne Eingriff (Snapshot wie TB-169), gleicher Tag: AAA ohne Einstieg bei E1 und bei s
   5 BBB/CCC/BTCUSDT mit und ohne Tag fuer AAA gleich
   6 Gegenprobe zur Lage der Schranke (R105 (b), Mutante M1): eine KOPIE von backtest_trend.py im Temp-Ordner mit der Schranke HINTER
     der Zustandsmaschine (Einstieg ohne i >= erster_einstieg, Trades vor dem Tag erst in der Ausgabe gestrichen), im Kindprozess per
     sitecustomize statt des Originals geladen (Marke .benutzt) -> rc 0 und kein Einstieg vor dem Tag, aber E2 fehlt bei s
Aufruf aus der Repo-Wurzel: python3 -B research/tb24_haltedauern/test_t3_verdraengung.py  (rc 0 = alle bestanden)"""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import test_listen_erzeuger as tle
BOTS = ["t3_supertrend"]
SEED = (169, 0)
ANKER, WOCHEN = "2024-06-03", 20                    # Kandidaten: ANKER + 0..WOCHEN-1 Wochen (BTC-Regime bei E1 und s)
LS = [63.0, 63.75, 67.25, 68.5, 71.0, 71.25, 67.125, 67.875]   # Kandidaten fuer L (Gleichstand nach Rundung, am Bau gemessen)
ND, M, STUFE = 30, 1200, 6
K4 = ["open", "high", "low", "close"]
_snapshot_alt = tle.snapshot
EINGRIFF = {"an": True}
WAHL = {}
def bauplan(L):
    c = [100.0 - (100.0 - L) * j / ND for j in range(1, ND + 1)] + [float(L)] * M
    s = len(c); c += [L * (1 + 0.004 * j) for j in range(1, STUFE + 1)]
    return c, s
def abschnitt(df, anker, L):
    import numpy as np, pandas as pd
    t = pd.to_datetime(df["open_time"]); c, s = bauplan(L); j = int((t >= pd.Timestamp(anker)).values.argmax()); e = j + len(c)
    df = df.copy(); df.loc[:j - 1, K4] = 100.0
    df.loc[j:e - 1, K4] = np.repeat(np.array(c)[:, None], 4, axis=1)
    fak = c[-1] / float(df["open"].iloc[e]); df.loc[e:, K4] = df.loc[e:, K4].values * fak
    return df, j, j + s
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    import pandas as pd
    _snapshot_alt(bot, d, ab_schnitt, seed, spaet, versatz)
    if EINGRIFF["an"]:
        f = os.path.join(d, "data", "AAA_%s.csv" % tle.TF.get(bot, "1d"))
        abschnitt(pd.read_csv(f), WAHL["anker"], WAHL["L"])[0].to_csv(f, index=False)
tle.snapshot = snapshot
def module(bot, d):
    import importlib
    pfad = os.path.join(tle.WURZEL, "strategies", bot); st = os.path.join(tle.WURZEL, "strategies") + os.sep
    for m in [m for m, v in list(sys.modules.items()) if os.path.abspath(getattr(v, "__file__", None) or "").startswith(st)]: sys.modules.pop(m, None)
    sys.path[:] = [q for q in sys.path if not q.startswith(st)]; sys.path.insert(0, pfad); os.environ["TB36_BASE_DIR"] = d
    es, mso, bt = (importlib.import_module(x) for x in ("equity_simulation", "multi_symbol_optimise", "backtest_trend"))
    assert os.path.dirname(os.path.abspath(bt.__file__)) == pfad and os.path.dirname(os.path.abspath(mso.__file__)) == pfad
    return es, mso, bt
def kandidat(es, mso, bt, p, btc, anker, L):
    import numpy as np, pandas as pd
    q, j, s = abschnitt(p, anker, L); t = pd.to_datetime(q["open_time"])
    tr = mso.get_trades_for_symbol(q, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
    if not len(tr): return None
    et = pd.to_datetime(tr["entry_time"]); inn = tr[(et >= t[j]) & (et <= t[s])]
    if not len(inn): return None
    e1 = int(np.where(t.values == np.datetime64(pd.Timestamp(inn["entry_time"].iloc[-1])))[0][0])
    x = bt.compute_indicators(q, es.T3_FAST, es.T3_SLOW, bt.T3_FACTOR, bt.DI_LENGTH, bt.ADX_LENGTH, bt.ATR_LENGTH, bt.ATR_MULT)
    f, g, adx = x["t3_fast"].to_numpy(), x["t3_slow"].to_numpy(), x["adx"].to_numpy()
    seg = f[e1:s] - g[e1:s]; eq = np.where(seg == 0)[0]
    T = (t[e1] + pd.Timedelta(days=10)).normalize()
    reg = es.filter_trades_by_regime(pd.DataFrame({"entry_time": [t[e1], t[s]], "symbol": "AAA"}), es.compute_btc_regime(btc))
    ok = ((seg >= 0).all() and len(eq) >= 60 and eq[0] + len(eq) == len(seg) and f[s] > g[s] and adx[s] > es.ADX_THRESHOLD
          and pd.Timestamp(inn["exit_time"].iloc[-1]) > t[s] and t[e1] < T <= t[s] and len(reg) == 2)
    if not ok: return None
    return {"anker": anker, "L": L, "q": q, "e1": t[e1], "s": t[s], "tag": str(T.date()), "gleich": int(len(eq)), "adx_s": round(float(adx[s]), 1),
            "aus_e1": pd.Timestamp(inn["exit_time"].iloc[-1]), "abschnitt": sorted(pd.to_datetime(inn["entry_time"]))}
def signalpfad(bot):
    import inspect, tempfile, shutil, pandas as pd
    d = tempfile.mkdtemp()
    try:
        EINGRIFF["an"] = False
        try: snapshot(bot, d, False, SEED[0], False, SEED[1])
        finally: EINGRIFF["an"] = True
        es, mso, bt = module(bot, d); tf = tle.TF.get(bot, "1d")
        p = pd.read_csv(os.path.join(d, "data", "AAA_%s.csv" % tf), parse_dates=["open_time"])
        btc = pd.read_csv(os.path.join(d, "data", "BTCUSDT_%s.csv" % tf), parse_dates=["open_time"])
        w = None
        for k in range(WOCHEN):
            for L in LS:
                w = kandidat(es, mso, bt, p, btc, str((pd.Timestamp(ANKER) + pd.Timedelta(weeks=k)).date()), L)
                if w: break
            if w: break
        if not w: return None
        q = w.pop("q"); T = pd.Timestamp(w["tag"]); WAHL.update(w)
        a0 = es.collect_all_trades({"AAA": q, "BTCUSDT": btc}, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT)
        a1 = es.collect_all_trades({"AAA": q, "BTCUSDT": btc}, es.T3_FAST, es.T3_SLOW, es.ADX_THRESHOLD, es.STOP_LOSS_PCT,
                                   entry_cutoffs={"AAA": T, "BTCUSDT": btc["open_time"].min()})
        w["ohne"], w["mit"] = zeiten(a0, "AAA"), zeiten(a1, "AAA")
        m = a1[(a1["symbol"] == "AAA") & (pd.to_datetime(a1["entry_time"]) == w["s"])] if len(a1) else a1
        w["pe2"] = round(float(m["entry_price"].iloc[0]), 6) if len(m) == 1 else None
        w["use_t3_exit"] = inspect.signature(bt.run_backtest).parameters["use_t3_exit"].default
        w["msO_uebergibt"] = "use_t3_exit" in inspect.getsource(mso.get_trades_for_symbol) or "use_t3_exit" in inspect.getsource(es.collect_all_trades)
        return w
    finally:
        shutil.rmtree(d, ignore_errors=True)
def zeiten(q, sym=None):
    import pandas as pd
    if q is None or not len(q): return set()
    if sym is not None: q = q[q["symbol"] == sym]
    return set(pd.to_datetime(q["entry_time"]))
GLEICH = ["symbol", "entry_time", "exit_time", "result", "pnl_pct"]
NAMEN = ["0 Signalpfad", "0b Gleichstand", "1 Erzeuger mit Schranke", "2 Gegenprobe 40.7", "3 Schranke und Wachen aus", "4 ohne Eingriff", "5 BBB/CCC/BTCUSDT gleich", "6 Mutante M1"]
def bot_pruefen(bot):
    import pandas as pd
    w = signalpfad(bot)
    if not w:
        for n in NAMEN: tle.pruefe(bot + ": " + n, False, "kein Kandidat (ANKER, L) erfuellt die Bedingungen am Signalpfad")
        return
    T, e1, s, tag = pd.Timestamp(w["tag"]), w["e1"], w["s"], w["tag"]
    tle.pruefe(bot + ": 0 Signalpfad: ohne Schranke E1 (%s) vor dem Tag %s, kein Einstieg bei s (%s); mit Schranke kein Einstieg vor dem Tag, E2 bei s" % (e1, tag, s),
               e1 in w["ohne"] and s not in w["ohne"] and s in w["mit"] and not any(x < T for x in w["mit"]), (sorted(map(str, w["ohne"] & {e1, s})), sorted(map(str, w["mit"] & {e1, s}))))
    tle.pruefe(bot + ": 0b Gleichstand: E1 bis s-1 fast >= slow, fast == slow auf %d Balken bis s-1, fast > slow bei s, ADX %s; use_t3_exit %s, vom Erzeuger nicht uebergeben" % (w["gleich"], w["adx_s"], w["use_t3_exit"]),
               w["use_t3_exit"] is True and not w["msO_uebergibt"] and w["aus_e1"] > s,
               "ANKER %s, L %s, Abschnitt-Einstiege ohne Schranke %s, Ausstieg E1 %s" % (w["anker"], w["L"], [str(x) for x in w["abschnitt"]], w["aus_e1"]))
    tg = json.dumps({"AAA": tag})
    r = tle.lauf(bot, SEED, False, "", tg); a = tle.tab(r["liste"])
    aa = a[a["symbol"] == "AAA"] if a is not None else None; ein = zeiten(a, "AAA")
    tle.pruefe(bot + ": 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, E2 erscheint bei s",
               r["rc"] == 0 and aa is not None and not (aa["entry_time"] < T).any() and s in ein and e1 not in ein
               and w["pe2"] is not None and (aa[aa["entry_time"] == s]["entry_price"].round(6) == w["pe2"]).all(), (r["rc"], r["fehler"] if r["rc"] else sorted(map(str, ein & {e1, s}))))
    r2 = tle.lauf(bot, SEED, False, "schranke_aus", tg)
    vor = [x for x in w["ohne"] if x < T and x >= w["abschnitt"][0]]
    tle.pruefe(bot + ": 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an einem Einstieg des Abschnitts vor dem Tag (%s) mit 2" % ", ".join(map(str, sorted(vor))),
               r2["rc"] == 2 and "R87 (c)" in r2["fehler"] and any(("Einstieg %s vor dem Handelbar-Tag %s bei AAA" % (x, tag)) in r2["fehler"] for x in vor), (r2["rc"], r2["fehler"]))
    r3 = tle.lauf(bot, SEED, False, "schranke_aus+wachen_aus", tg); c = tle.tab(r3["liste"]); ec = zeiten(c, "AAA")
    c1 = c[(c["symbol"] == "AAA") & (c["entry_time"] == e1)] if c is not None else None
    tle.pruefe(bot + ": 3 Schranke und Wachen aus: E1 vor dem Tag, Ausstieg nach s, Einstieg bei s fehlt (verdraengt)",
               r3["rc"] == 0 and e1 in ec and s not in ec and c1 is not None and len(c1) == 1 and c1["exit_time"].iloc[0] > s,
               (r3["rc"], sorted(map(str, ec & {e1, s})), None if c1 is None or not len(c1) else str(c1["exit_time"].iloc[0])))
    EINGRIFF["an"] = False
    try: r4 = tle.lauf(bot, SEED, False, "", tg)
    finally: EINGRIFF["an"] = True
    eo = zeiten(tle.tab(r4["liste"]), "AAA")
    tle.pruefe(bot + ": 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei E1 und bei s", r4["rc"] == 0 and not (eo & {e1, s}), (r4["rc"], sorted(map(str, eo & {e1, s}))))
    r5 = tle.lauf(bot, SEED, False, "", "{}"); g = tle.tab(r5["liste"])
    gl = lambda q: q[q["symbol"] != "AAA"][GLEICH].reset_index(drop=True).to_csv(index=False) if q is not None else None
    tle.pruefe(bot + ": 5 BBB/CCC/BTCUSDT mit und ohne Tag fuer AAA gleich", r5["rc"] == 0 and a is not None and gl(a) == gl(g), r5["rc"])
    r6, benutzt = m1_lauf(bot, tg); m = tle.tab(r6["liste"]); em = zeiten(m, "AAA")
    tle.pruefe(bot + ": 6 Mutante M1 (Kopie von backtest_trend.py, Schranke hinter der Zustandsmaschine): kein Einstieg vor dem Tag, aber E2 fehlt bei s - die Probe 1 schlaegt an",
               benutzt and r6["rc"] == 0 and m is not None and s not in em and not any(x < T for x in em), (benutzt, r6["rc"], r6["fehler"] if r6["rc"] != 0 else sorted(map(str, em & {e1, s}))))
SITE = """import importlib.abc, importlib.util, os, sys
_m = os.environ.get("TB174_M1")
if _m:
    class _Finder(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path=None, target=None):
            if name != "backtest_trend": return None
            open(_m + ".benutzt", "w").write("ja")
            return importlib.util.spec_from_file_location("backtest_trend", _m)
    sys.meta_path.insert(0, _Finder())
"""
def m1_lauf(bot, tg):
    """M1 nur an einer Kopie im Temp-Ordner: Einstieg ohne Schranke, Trades vor dem Tag erst in der Ausgabe gestrichen."""
    import tempfile, shutil
    qd = os.path.join(tle.WURZEL, "strategies", bot); q = os.path.join(qd, "backtest_trend.py"); s = open(q, encoding="utf-8").read()
    ers = [(" and vwap_ok and i >= erster_einstieg:", " and vwap_ok:"),
           ("    return pd.DataFrame(trades)\n\n\ndef print_summary", "    trades = [x for x in trades if entry_cutoff is None or pd.Timestamp(x[\"entry_time\"]) >= pd.Timestamp(entry_cutoff)]\n"
            "    return pd.DataFrame(trades)\n\n\ndef print_summary"),
           ("_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))", "_STRATEGY_DIR = %r" % qd)]
    if not all(s.count(a) == 1 for a, b in ers): return {"rc": None, "liste": None, "fehler": "M1: Stelle in backtest_trend.py nicht genau einmal"}, False
    for a, b in ers: s = s.replace(a, b)
    t = tempfile.mkdtemp(); m = os.path.join(t, "m1_backtest_trend.py"); open(m, "w", encoding="utf-8").write(s)
    open(os.path.join(t, "sitecustomize.py"), "w", encoding="utf-8").write(SITE)
    vorher = {k: os.environ.get(k) for k in ("PYTHONPATH", "TB174_M1")}
    os.environ["PYTHONPATH"] = t + (os.pathsep + vorher["PYTHONPATH"] if vorher["PYTHONPATH"] else ""); os.environ["TB174_M1"] = m
    try:
        r = tle.lauf(bot, SEED, False, "", tg); return r, os.path.exists(m + ".benutzt")
    finally:
        for k, v in vorher.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v
        shutil.rmtree(t, ignore_errors=True)
if __name__ == "__main__":
    for bot in (sys.argv[1:] or BOTS): bot_pruefen(bot)
    print("Ergebnis: %d von %d bestanden" % (tle.n[1], tle.n[0])); sys.exit(0 if tle.n[0] and tle.n[0] == tle.n[1] else 1)
````

