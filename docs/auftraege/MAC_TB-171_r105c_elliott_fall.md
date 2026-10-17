# TB-171 R105 (c) Weg 1: Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks am Listen-Erzeuger herbeiführen (Probe mit Gegenprobe nach 40.7) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 08:48** (Helfer BAU171, per Skript aus Bausteinen, `$HOME/sc/tb171/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis E an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `241ca0b`.**

**Sitzungstitel:** `TB-171` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `241ca0b0d22b748dcaf7ca5f9fb07d1a6076e99e` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-171`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-171_r105c_elliott_fall.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (Python 3.9, numpy 2.0.2, pandas 2.3.3 nach `requirements.lock`); Werkzeug `docs/belege/TB-171/tb171_werkzeug.py` (Anhang A), kurz `WZ`. **Belege:** `docs/belege/TB-171/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-171_r105c_elliott_fall.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FG ⇒ FH).
**Grundlage:** R105 (a)–(c) (Register Z. 12464), Register 65 (c) (Z. 12515: Weg 2 trägt nicht, Weg 1 bleibt), R90 (g) (Z. 11997), R98 (d) (Z. 12231), R87 (c), 40.7 (Z. 8461); BACKLOG Rang 1 (Punkt „R105 (c) Weg 1“); Vorbild Ort, Aufbau, Abnahme: `research/tb24_haltedauern/test_listen_erzeuger.py` (TB-169, Abnahme nach R98 (d)). **Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ E (Probe schreiben und laufen lassen) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F. **Kein Registereintrag** (R105 (c): „Welcher Weg, ist Handwerk“; der Stand geht mit der nächsten Anfrage an den Verfahrensprüfer).

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 33 („Opus Trading Bots-16.10.2026 c“), 17.10.2026, 09:12, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-171 frei? TB-171 legt nur einen neuen Test an: research/tb24_haltedauern/test_elliott_verdraengung.py. Der Test führt bei beiden Elliott-Bots an einer Kopie der Testdaten den Fall nach R90 (g) herbei. Gemeint ist eine Welle vor dem Handelbar-Tag, die ohne Schranke den späteren Einstieg verdrängen würde. Mit der Schranke steigt die Welle am Tag oder später ein. Ohne Schranke, und auch wenn die Schranke hinter dem Eintrag in traded sitzt, wird die Probe rot. An der Kopie bestand sie 16 von 16; mit falsch gesetzter Schranke waren es 8 von 16. Der Handelscode bleibt unverändert, das prüft der Auftrag über 15 md5. Es gibt keinen Registereintrag, keinen Lauf auf Live-Daten, kein Live und kein Geld. Der Gegenleser und der enge Gegenleser fanden keinen A- und keinen B-Befund. Offen bleibt für Fable, ob die Probe R105 (c) schliesst: R105 (c) spricht von „einer späteren Welle“, am Code wird aber der spätere Einstieg derselben Welle verdrängt. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Die Probe sichert die Schranke am Handelscode, und die Frage an Fable kann parallel laufen."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. TB-171 ändert keinen Handelscode und keine Datei der Sperrliste; neu ist eine Testdatei unter `research/tb24_haltedauern/`.

R105 (c) (Register Z. 12464), Weg 1 wörtlich: „Der Fall wird auf dem Test-Snapshot herbeigeführt (eine Welle vor dem Handelbar-Tag, deren Eintrag in traded ohne Schranke eine spätere Welle verdrängt; ohne Schranke fehlt der zweite Einstieg oder die Wache nach R87 (c) endet mit 2, mit Schranke erscheint er)“

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen (die Probe rechnet auf dem synthetischen Test-Snapshot von `test_listen_erzeuger.py` im Temp-Ordner). Keine Neuerzeugung der neun Listen. Nichts unter `strategies/`, `shared/`, `data/`, `config/` ändern; unter `research/` nur die neue Datei aus E. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`, kein `rm`, kein `mv`.

## Die Probe (Anhang B, neu: `research/tb24_haltedauern/test_elliott_verdraengung.py`, sha256 `59f6c90bde98a04da20fd52f314399a6e35443cacbfc3e2225d00eab3227d573`)

**Warum ein Eingriff nötig ist (am Bau gemessen, Teilmessung am Signalpfad):** Auf dem Test-Snapshot von TB-169 (Seeds 169–180 bei `elliott_wave_stocks`, 169–190 bei `elliott_wave`, zusammen rund 990 Einstiege) entsteht der Fall nie: bei jeder eingestiegenen Welle ist der nächste Lauf der Wellenauswahl (`find_causal_waves`, Läufe nur an `confirm_idx` von Kandidaten) nicht mehr frisch (`SIGNAL_FRESHNESS_BARS` 5 bzw. 48). Erschlossen aus `is_valid_impulse`: die Welle aus den Pivots P1..P6 nach einer gültigen Welle W (P0..P5) kann nie gültig sein; der nächste Lauf ist frühestens die Bestätigung von P7.

**Herbeiführung (nur an der Kopie im Temp-Ordner):** Die Probe baut den Snapshot B wie `test_listen_erzeuger.py` (Seed 169, Versatz 0, ohne Zeilen ab dem Schnitt) und setzt in die Reihe `AAA` ab `2025-03-03` einen Kursabschnitt ein (danach die alte Reihe, auf den Endkurs skaliert): Welle W bearish mit den Pivots 100, 80, 91, 60, 69, 21 (Fib-Score 1.0), bestätigt am Balken k+1 (Lauf r0); dann P6 = 30 (k+2), P7 = 26 (k+3), bestätigt am Balken k+4: die Welle 91, 60, 69, 21, 30, 26 ist gültig (Score 0.33) und gibt den Lauf r1 = k+4, für W noch frisch (4 Balken nach dem Pivot P5); `remove_overlapping` behält W (1.0 > 0.33). Handelbar-Tag von `AAA` = Tag des Balkens k+2 (bei `elliott_wave` auf 00:00 gelegt). Vor dem Abschnitt ist die Reihe `AAA` flach (kein Pivot, kein Einstieg): vor dem Tag kann nur W einsteigen. Ohne Schranke steigt W bei r0 ein (vor dem Tag), `traded` hält ihr `end_time` (`elliott_wave_counter.py` Z. 352–353, 363), bei r1 ist W verdrängt. Mit Schranke (Z. 361, vor `traded.add`) ist W bei r0 gesperrt und steigt bei r1 ein.

**Prüfungen je Bot (geprüft an den Ausgaben des Erzeugers `positionen_holen.py`, Bauart `test_listen_erzeuger.lauf`):** 0 Signalpfad (Handwerk, R98 (d) letzter Satz): ohne `entry_cutoff` Einstieg bei k+1, mit `entry_cutoff` = Tag bei k+4 · 0b beide Einstiege sind W (signal_time = Pivot P5, fib_score 1.0), und ohne Schranke endet W erst am Tag oder später (Position über den Tag offen, R90 (g)) · 1 Erzeuger mit Schranke: rc 0, kein Einstieg von `AAA` vor dem Tag, W erscheint bei k+4 (entry_price wie am Signalpfad) · 2 **Gegenprobe nach 40.7**: Schranke aus ⇒ Wache R87 (c) beisst an W („Einstieg ⟨k+1⟩ vor dem Handelbar-Tag“) und endet mit 2 · 3 Schranke und Wachen aus ⇒ W bei k+1 vor dem Tag mit Ausstieg am Tag oder später, kein Einstieg bei k+4 (verdrängt) · 4 ohne Eingriff (Snapshot wie TB-169), gleicher Tag: `AAA` hat weder bei k+1 noch bei k+4 einen Einstieg (der Eingriff führt den Fall herbei) · 5 `BBB`/`CCC` mit und ohne Tag für `AAA` gleich (Spalten symbol, entry_time, exit_time, result, pnl_pct) · 6 **Gegenprobe zur Lage der Schranke** (R105 (b), Mutante M1): eine Kopie von `elliott_wave_counter.py` im Temp-Ordner der Probe mit der Schranke hinter `traded.add`, im Kindprozess über `sitecustomize` (PYTHONPATH) statt des Originals geladen (Marke `.benutzt`) ⇒ W fehlt bei k+4. Der Handelscode wird dabei nicht berührt. Am Bau: **16 von 16** (Gerät, Python 3.10.12, pandas 2.3.3, numpy 2.2.6, `binance`/`yfinance` als Attrappen ohne Netz, rund 60 s). Gegenprobe am Bau: M1 in einer Kopie des Repos eingesetzt ⇒ die Probe ist rot (rc 1).

**Zur Kenntnis (nicht entschieden, nicht gebaut):** R105 (c) spricht von einer Welle, „deren Eintrag in traded ohne Schranke eine spätere Welle verdrängt“; am Code verdrängt der Eintrag den späteren Einstieg derselben Welle (Schlüssel `end_time`, Register 65 (c)). Die Probe zeigt diesen Fall. Ob das R105 (c) für beide Bots schliesst, entscheidet der Verfahrensprüfer. R105 (d) (`t3_supertrend`) bleibt unberührt.

## Lage nach dem Auslegen

Beim Start genau 2 Einträge (Soll in 0a).

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `241ca0b0d22b748dcaf7ca5f9fb07d1a6076e99e`, genau diese 2 Einträge, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-171_r105c_elliott_fall.md
```

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb171_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-171_r105c_elliott_fall.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "241ca0b0d22b748dcaf7ca5f9fb07d1a6076e99e": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "241ca0b0d22b748dcaf7ca5f9fb07d1a6076e99e": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-171_r105c_elliott_fall.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (2 Eintraege)`. Anhänge holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-171_r105c_elliott_fall.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb171_werkzeug.py 6f049b915d314d287eb791a71e5c7a72953de67cb3bce6f9fcce2c6f1fac7ad0`; `test_elliott_verdraengung.py 59f6c90bde98a04da20fd52f314399a6e35443cacbfc3e2225d00eab3227d573`; `Dateien 2`; sonst **ABBRUCH**. Dann genau diese `git add`, Commit `TB-171 Schritt 0: Stand des steuernden Chats vor TB-171 (Auftrag)`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/auftraege/MAC_TB-171_r105c_elliott_fall.md
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-171
cp "$TMPDIR/tb171_0a.txt" docs/belege/TB-171/0a_status.txt
cp "$TMPDIR/tb171_werkzeug.py" docs/belege/TB-171/tb171_werkzeug.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py voraussetzung > docs/belege/TB-171/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (20 Prüfungen am Bau: Handelscode und Erzeuger je md5 = Bau, Probe noch nicht im Repo, R105 und 65 (c) im Wortlaut, BACKLOG Rang 1 Stand TB-170, Journal FG). **Abbruch in V:** im Arbeitsbaum liegt nur der unverfolgte Ordner `BEL`. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-171/abbruch.txt`, dann `git add` mit Namen für `abbruch.txt`, `0a_status.txt`, die zwei Anhänge und `v_voraussetzung.txt`, Commit `TB-171 Abbruch: V`, pushen, `git status --porcelain` leer; melden.

## Schritt E — Probe schreiben und laufen lassen

```
cp "$TMPDIR/test_elliott_verdraengung.py" research/tb24_haltedauern/test_elliott_verdraengung.py
trading-env/bin/python3 -B research/tb24_haltedauern/test_elliott_verdraengung.py > docs/belege/TB-171/e_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/e_probe.txt
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py nachher > docs/belege/TB-171/e_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/e_nachher.txt
```

Soll: `e_probe.txt` endet mit `Ergebnis: 16 von 16 bestanden` und `rc 0`; `e_nachher.txt` endet mit `rc 0` (Handelscode unverändert, Probe = Anhang, 16 ja). **Abbruchweg E** (ein Beleg nicht `rc 0`; kein E-Commit):

```
trading-env/bin/python3 -B -c "import os; t = 'research/tb24_haltedauern/test_elliott_verdraengung.py'; d = 'docs/belege/TB-171/abbruch_test_elliott_verdraengung.py'; da = os.path.exists(t); os.replace(t, d) if da else None; open('docs/belege/TB-171/abbruch.txt', 'w').write('E: erster Beleg ohne rc 0, siehe Belege\n' + ('Test nach BEL verschoben' if da else 'Test nicht vorhanden') + '\n')"
trading-env/bin/python3 -B -c "import os, subprocess; f = ['docs/belege/TB-171/' + x for x in ('abbruch.txt', 'abbruch_test_elliott_verdraengung.py', '0a_status.txt', 'tb171_werkzeug.py', 'v_voraussetzung.txt', 'e_probe.txt', 'e_nachher.txt')]; d = [x for x in f if os.path.exists(x)]; print('git add', len(d), 'von', len(f)); raise SystemExit(subprocess.run(['git', 'add'] + d).returncode)"
git commit -q -m "TB-171 Abbruch: E"
git push -q origin main
git status --porcelain
```

Der Abbruchweg fügt nur Belege hinzu, die vorhanden sind (eine Python-Zeile prüft jeden Pfad vor `git add`); fehlt der Test (Abbruch vor dem Kopieren), schreibt er „Test nicht vorhanden“ in `abbruch.txt`. Soll danach: `git status --porcelain` ohne Ausgabe; scheitert der Push: melden, nicht wiederholen. Sonst (alle grün) genau diese `git add`, Commit `TB-171 E: Probe R105 (c) Weg 1 (Elliott, Fall nach R90 (g))`, pushen ⇒ **⟨E⟩**:

```
git add research/tb24_haltedauern/test_elliott_verdraengung.py
git add docs/belege/TB-171/0a_status.txt
git add docs/belege/TB-171/tb171_werkzeug.py
git add docs/belege/TB-171/v_voraussetzung.txt
git add docs/belege/TB-171/e_probe.txt
git add docs/belege/TB-171/e_nachher.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ kennung` (Soll „Kennung FH …“). Block nach `docs/belege/TB-171/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-171: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-171_r105c_elliott_fall.md` mit: Kurz; V wörtlich (letzte Zeilen); E (die 12 Zeilen aus `e_probe.txt` wörtlich, Laufzeit); Zur Kenntnis (der Absatz oben); Offen (R105 (c) geschlossen? Frage an den Verfahrensprüfer; R105 (d) t3_supertrend); Abweichungen; In einfacher Sprache. Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Dann:

```
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py kennung > docs/belege/TB-171/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-171/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-171/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py journal docs/belege/TB-171/a_block.md --probe > docs/belege/TB-171/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-171/tb171_werkzeug.py journal docs/belege/TB-171/a_block.md > docs/belege/TB-171/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-171/a_journal.txt
```

Soll je `rc 0`. Genau diese `git add`, Commit `TB-171 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-171_r105c_elliott_fall.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-171/a_kennung.txt
git add docs/belege/TB-171/a_backlog_probe.txt
git add docs/belege/TB-171/a_backlog.txt
git add docs/belege/TB-171/a_block.md
git add docs/belege/TB-171/a_journal_probe.txt
git add docs/belege/TB-171/a_journal.txt
```

**F.**

```
git status --porcelain > "$TMPDIR/tb171_f.txt"
cp "$TMPDIR/tb171_f.txt" docs/belege/TB-171/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-171/f_numstat.txt
git add docs/belege/TB-171/f_porcelain.txt
git add docs/belege/TB-171/f_numstat.txt
git commit -q -m "TB-171 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; im numstat unter `research/` genau die neue Probe.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V nicht `rc 0`; ein Beleg aus E nicht `rc 0` (dann Abbruchweg E, **kein E-Commit**); A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Die zwei Elliott-Bots dürfen vor dem Tag, ab dem ein Symbol handelbar ist, nicht einsteigen. Eine Welle, die zu früh kommt, wird gesperrt und darf später noch einsteigen. Dieser Fall kam in den erfundenen Testkursen nie von selbst vor. Der neue Test baut ihn gezielt in eine Kopie der Testkurse ein und zeigt: mit der Sperre steigt die Welle später ein, ohne die Sperre steigt sie zu früh ein und der spätere Einstieg fehlt. Am Handelscode ändert sich nichts.

## Anhänge

### Anhang A — Werkzeug

<!-- DATEI tb171_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-171 Werkzeug (Anhang A): R105 (c) Weg 1 - Voraussetzungen, Nachher-Pruefung (Handelscode unveraendert, Probe gruen), Kennung, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-171/"
TEST, TSHA = "research/tb24_haltedauern/test_elliott_verdraengung.py", "59f6c90bde98a04da20fd52f314399a6e35443cacbfc3e2225d00eab3227d573"
CODE = { "strategies/elliott_wave/elliott_wave_counter.py": "75b26dd79237cd61c0cf04b45cf93098", "strategies/elliott_wave/multi_symbol_optimise.py": "bf11370b140d3e61488ad81599b45b37", "strategies/elliott_wave/backtest_elliott.py": "df5c314e9268bf5c51a5210113e27082", "strategies/elliott_wave/zigzag_indicator.py": "6e9a91ccc131937079b602be875fa0dd", "strategies/elliott_wave/equity_simulation.py": "a058c69a7a6c25e7239381bfab96fb05", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "b7fd099124b4801aecd68ba1e0fb1a05", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "571076168d56f9e809ef0595f53d6e7d", "strategies/elliott_wave_stocks/backtest_elliott.py": "f1979557a945822dfbe623e0d80ca531", "strategies/elliott_wave_stocks/zigzag_indicator.py": "407cd69fb5c2181c5316e008ea7b7d81", "strategies/elliott_wave_stocks/equity_simulation.py": "4ff525c50514fc25f43f50437148a7bd", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/test_listen_erzeuger.py": "d77e73ed5ff7a737a22e53879ff72575", "research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "research/faltenplan_neun/faltenschranke_messung.py": "584d9ff959dab7428a97a945b091e118" }
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; ab TB-170 über `$TMPDIR`) |"
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
    reg = lies(REG).split("\n"); r105 = [l for l in reg if l.startswith("> R105 — ")]
    p(len(r105) == 1 and "Der Fall wird auf dem Test-Snapshot herbeigeführt" in r105[0], "Register: R105 genau einmal, (c) Weg 1 im Wortlaut")
    p(sum("Damit bleibt Weg 1" in l for l in reg) == 1, "Register 65 (c): Weg 2 traegt nicht, Weg 1 bleibt (genau einmal)")
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(RANG1E) and "R105 (c) Weg 1" in z[0], "BACKLOG Rang 1 genau einmal, Stand TB-170, nennt R105 (c) Weg 1")
    k = kennungen(); p(max(k) == "FG", "Journal: hoechste FG (naechste FH)")
    ende()
def nachher():
    code_gleich()
    p(os.path.exists(TEST) and hashlib.sha256(open(TEST, "rb").read()).hexdigest() == TSHA, "Probe im Repo = Anhang (sha256 %s)" % TSHA[:12])
    e = lies(BEL + "e_probe.txt").rstrip("\n").split("\n") if os.path.exists(BEL + "e_probe.txt") else [""]
    p(e[-1] == "rc 0" and len(e) > 1 and e[-2] == "Ergebnis: 16 von 16 bestanden", "e_probe.txt endet mit 'Ergebnis: 16 von 16 bestanden' und 'rc 0'")
    p(not any(l.startswith("NEIN") for l in e) and sum(l.startswith("ja    ") for l in e) == 16, "e_probe.txt: 16 ja-Zeilen, keine NEIN-Zeile")
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-170"):
        z[a[0]] = z[a[0]][:-2] + (" · **TB-171 (%s, Journal %s): R105 (c) Weg 1, Probe `%s` am Listen-Erzeuger, `elliott_wave` und `elliott_wave_stocks`, 16 von 16** "
            "(Fall nach R90 (g) auf dem Test-Snapshot herbeigeführt durch einen eingesetzten Kursabschnitt; mit Schranke steigt die Welle am Tag oder später ein; "
            "Gegenprobe 40.7: Schranke aus ⇒ Wache R87 (c) beisst an der Welle und endet mit 2, Schranke und Wachen aus ⇒ der spätere Einstieg fehlt; Mutante mit der Schranke hinter `traded.add` an einer Kopie des Counters ⇒ die Welle fehlt); offen, an den Verfahrensprüfer: ob R105 (c) damit "
            "für beide Bots geschlossen ist und ob „eine spätere Welle“ in R105 (c) den späteren Einstieg derselben Welle trägt (Schlüssel end_time, Register 65 (c)); R105 (d) t3_supertrend unberührt |") % (datum, kenn, TEST)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-171: " % neu), "Kopfzeile ## %s — TB-171: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
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

<!-- DATEI test_elliott_verdraengung.py -->
````python
#!/usr/bin/env python3
"""TB-171 (R105 (c) Weg 1; R90 (g), R98 (d), R87 (c), 40.7): Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks am
Listen-Erzeuger research/tb24_haltedauern/positionen_holen.py, auf dem Test-Snapshot von test_listen_erzeuger.py (TB-169, Seed 169,
Versatz 0, Snapshot B ohne Zeilen ab dem Schnitt), mit einem Eingriff NUR an der Kopie im Temp-Ordner: In die Reihe von AAA wird ein
Kursabschnitt eingesetzt (danach die alte Reihe, auf den Endkurs skaliert), der den Fall herbeifuehrt (R81 (h), R75 (f)):
  Welle W (bearish, Pivots P0..P5 = 100, 80, 91, 60, 69, 21; Fib-Score 1.0) wird am Balken k+1 bestaetigt (Lauf r0 = k+1); die Welle
  C2 (P2..P7 = 91, 60, 69, 21, 30, 26; gueltig, Score 0.33) wird am Balken k+4 bestaetigt (Lauf r1 = k+4, frisch fuer W: r1 - Pivot(P5)
  = 4 <= SIGNAL_FRESHNESS_BARS 5 bzw. 48). remove_overlapping behaelt W (Score 1.0 > 0.33). Handelbar-Tag von AAA = Tag des Balkens k+2.
  Ohne Schranke steigt W bei r0 ein (vor dem Tag), traded haelt ihr end_time, bei r1 wird W verdraengt (elliott_wave_counter.py Z. 352-353,
  363). Mit Schranke (Z. 361, vor traded.add) wird W bei r0 gesperrt und steigt bei r1 ein (am Tag oder spaeter).
Handelscode unveraendert; data/ wird nicht gelesen; geprueft an den AUSGABEN des Erzeugers (<bot>_alle_trades.csv, rc).
   0 Herbeifuehrung am Signalpfad (Handwerk, R98 (d) letzter Satz): ohne entry_cutoff W-Einstieg bei k+1, mit entry_cutoff = Tag bei k+4
   1 Erzeuger mit Schranke (Tag {AAA: Tag}): rc 0, kein Einstieg von AAA vor dem Tag, W erscheint mit Einstieg k+4 (der zweite Einstieg)
   2 Gegenprobe (40.7, R87 (c)): Schranke aus -> Wache R87 (c) beisst an W (Einstieg k+1) und endet mit 2 (die Reihe AAA ist vor dem
     Abschnitt flach: kein anderer Einstieg vor dem Tag)
   3 Gegenprobe ohne Wachen: Schranke und Wachen aus -> rc 0, W mit Einstieg k+1 vor dem Tag und Ausstieg am Tag oder spaeter
     (Position ueber den Tag offen, R90 (g)), kein Einstieg bei k+4 (verdraengt)
   4 Gegenprobe zur Herbeifuehrung: ohne Eingriff (Snapshot wie TB-169) und gleichem Tag hat AAA weder bei k+1 noch bei k+4 einen Einstieg
   5 Probe nach 1 auch fuer BBB/CCC: Ausgaben ohne AAA mit und ohne Tag fuer AAA gleich
   6 Gegenprobe zur Lage der Schranke (R105 (b), Mutante M1): eine KOPIE des Counters im Temp-Ordner mit der Schranke HINTER
     traded.add (per sitecustomize im Kindprozess statt des Originals geladen, Marke .benutzt) -> W fehlt bei k+4, kein Einstieg vor dem Tag
   W wird am Signalpfad ueber signal_time (= Pivot P5) und fib_score 1.0 erkannt, am Erzeuger ueber entry_time und entry_price
Aufruf aus der Repo-Wurzel: python3 -B research/tb24_haltedauern/test_elliott_verdraengung.py [bot ...]  (rc 0 = alle bestanden)"""
import json, os, sys
HIER = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HIER)
import test_listen_erzeuger as tle
BOTS = ["elliott_wave", "elliott_wave_stocks"]
SEED = (169, 0)
ANKER = "2025-03-03"
WEG = [100, 80, 91, 60, 69, 21]              # Pivots P0..P5 der Welle W (relativ, x Skala)
_snapshot_alt = tle.snapshot
EINGRIFF = {"an": True}
def bauplan():
    """Balkenliste (high, low) relativ; Index von k (Pivot P5) in der Liste. Beine monoton, je Bein 4 Balken."""
    b = []
    def bein(a, z, n=4):
        for j in range(1, n + 1):
            x = a + (z - a) * j / n; b.append((x * 1.001, x * 0.999))
    bein(70, 100)                                    # Anstieg auf P0 (aus 70, d. h. +43 %: P0 ist sicher ein Hoch)
    b[-1] = (100.0, 99.5)
    for a, z in zip(WEG[:-1], WEG[1:]):
        bein(a, z)
        b[-1] = (z * 1.001, z) if z < a else (z, z * 0.999)
    k = len(b) - 1                                   # P5 = 21 (Tief)
    b += [(23.5, 23.0), (30.0, 29.5), (27.0, 26.0), (29.0, 28.0)]   # k+1 bestaetigt P5; k+2 P6=30; k+3 bestaetigt P6, P7=26; k+4 bestaetigt P7
    return b, k
def einsetzen(bot, d):
    import pandas as pd
    tf = tle.TF.get(bot, "1d"); f = os.path.join(d, "data", "AAA_%s.csv" % tf)
    df = pd.read_csv(f); t = pd.to_datetime(df["open_time"]); b, k = bauplan()
    j = int((t >= pd.Timestamp(ANKER)).values.argmax())
    if tf != "1d":                                   # Balken k+2 auf 00:00 legen (min_entry_idx = erster Balken des Tags)
        while t.iloc[j + k + 2].hour != 0: j += 1
    s = float(df["close"].iloc[j - 1]) / 70.0
    df.loc[:j - 1, ["open", "high", "low", "close"]] = 70.0 * s       # vor dem Abschnitt flach: kein Pivot, kein Einstieg vor W
    for i, (h, lo) in enumerate(b):
        m = (h + lo) / 2 * s
        df.loc[j + i, ["open", "high", "low", "close"]] = [m, h * s, lo * s, m]
    e = j + len(b); fak = b[-1][1] * s / float(df["open"].iloc[e])
    for c in ("open", "high", "low", "close"):
        df.loc[e:, c] = df.loc[e:, c] * fak
    df.to_csv(f, index=False)
    return {"k1": str(t.iloc[j + k + 1]), "k4": str(t.iloc[j + k + 4]), "tag": str(t.iloc[j + k + 2].date()), "p5": str(t.iloc[j + k])}
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    _snapshot_alt(bot, d, ab_schnitt, seed, spaet, versatz)
    if EINGRIFF["an"]:
        x = einsetzen(bot, d); json.dump(x, open(os.path.join(d, "eingriff.json"), "w"))
tle.snapshot = snapshot
def signalpfad(bot):
    import importlib, tempfile, shutil, pandas as pd
    d = tempfile.mkdtemp(); pfad = os.path.join(tle.WURZEL, "strategies", bot)
    st = os.path.join(tle.WURZEL, "strategies") + os.sep   # je Bot frisch: alle Module aus strategies/ aus dem Speicher (live_params, equity_simulation, ...)
    for m in [m for m, v in list(sys.modules.items()) if os.path.abspath(getattr(v, "__file__", None) or "").startswith(st)]: sys.modules.pop(m, None)
    sys.path[:] = [q for q in sys.path if not q.startswith(os.path.join(tle.WURZEL, "strategies") + os.sep)]
    try:
        snapshot(bot, d, False, SEED[0], False, SEED[1]); x = json.load(open(os.path.join(d, "eingriff.json")))
        sys.path.insert(0, pfad); os.environ["TB36_BASE_DIR"] = d
        es = importlib.import_module("equity_simulation"); mso = importlib.import_module("multi_symbol_optimise")
        p = pd.read_csv(os.path.join(d, "data", "AAA_%s.csv" % tle.TF.get(bot, "1d")), parse_dates=["open_time"])
        t0 = mso.get_trades_for_symbol(p, es.DEVIATION_PCT); t1 = mso.get_trades_for_symbol(p, es.DEVIATION_PCT, entry_cutoff=pd.Timestamp(x["tag"]))
        assert os.path.dirname(os.path.abspath(mso.__file__)) == pfad
        w = lambda q, z: q[pd.to_datetime(q["entry_time"]) == pd.Timestamp(x[z])].to_dict("records") if len(q) else []
        return x, zeiten(t0), zeiten(t1), w(t0, "k1"), w(t1, "k4")
    finally:
        shutil.rmtree(d, ignore_errors=True)
def zeiten(q, sym=None):
    import pandas as pd
    if q is None or not len(q): return set()
    if sym is not None: q = q[q["symbol"] == sym]
    return set(pd.to_datetime(q["entry_time"]))
GLEICH = ["symbol", "entry_time", "exit_time", "result", "pnl_pct"]   # ohne trade_zeile/ausgefuehrt: die Zuteilung haengt am Tag von AAA
def bot_pruefen(bot):
    import pandas as pd
    x, e0, e1, w0, w1 = signalpfad(bot); T = pd.Timestamp(x["tag"]); P5 = pd.Timestamp(x["p5"]); k1, k4, tag = pd.Timestamp(x["k1"]), pd.Timestamp(x["k4"]), x["tag"]
    tle.pruefe(bot + ": 0 Signalpfad: ohne Schranke W bei k+1 (%s), mit Schranke ab Tag %s W bei k+4 (%s)" % (k1, tag, k4),
               k1 in e0 and k4 not in e0 and k4 in e1 and k1 not in e1, (sorted(map(str, e0 & {k1, k4})), sorted(map(str, e1 & {k1, k4}))))
    ist_w = lambda r: len(r) == 1 and pd.Timestamp(r[0]["signal_time"]) == P5 and float(r[0]["fib_score"]) == 1.0
    tle.pruefe(bot + ": 0b W ist dieselbe Welle (signal_time = P5 %s, fib_score 1.0), ohne Schranke Ausstieg am Tag oder spaeter" % P5,
               ist_w(w0) and ist_w(w1) and pd.Timestamp(w0[0]["exit_time"]) >= T, [(str(r["signal_time"]), r["fib_score"], str(r["exit_time"])) for r in w0 + w1])
    pw = round(float(w1[0]["entry_price"]), 6) if w1 else None
    tg = json.dumps({"AAA": tag})
    r = tle.lauf(bot, SEED, False, "", tg); a = tle.tab(r["liste"])
    aa = a[a["symbol"] == "AAA"] if a is not None else None; ein = zeiten(a, "AAA")
    tle.pruefe(bot + ": 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, W erscheint bei k+4",
               r["rc"] == 0 and aa is not None and not (aa["entry_time"] < T).any() and k4 in ein and k1 not in ein
               and pw is not None and (aa[aa["entry_time"] == k4]["entry_price"].round(6) == pw).all(), (r["rc"], r["fehler"] if r["rc"] else sorted(map(str, ein & {k1, k4}))))
    r2 = tle.lauf(bot, SEED, False, "schranke_aus", tg)
    tle.pruefe(bot + ": 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an W (Einstieg k+1 %s) mit 2" % k1, r2["rc"] == 2 and "R87 (c)" in r2["fehler"]
               and ("Einstieg %s vor dem Handelbar-Tag" % k1) in r2["fehler"], (r2["rc"], r2["fehler"]))
    r3 = tle.lauf(bot, SEED, False, "schranke_aus+wachen_aus", tg); c = tle.tab(r3["liste"])
    ec = zeiten(c, "AAA")
    c1 = c[(c["symbol"] == "AAA") & (c["entry_time"] == k1)] if c is not None else None
    tle.pruefe(bot + ": 3 Schranke und Wachen aus: W bei k+1 vor dem Tag, Ausstieg am Tag oder spaeter, Einstieg bei k+4 fehlt (verdraengt)",
               r3["rc"] == 0 and k1 in ec and k4 not in ec and c1 is not None and len(c1) == 1 and c1["exit_time"].iloc[0] >= T,
               (r3["rc"], sorted(map(str, ec & {k1, k4})), None if c1 is None or not len(c1) else str(c1["exit_time"].iloc[0])))
    EINGRIFF["an"] = False
    try: r4 = tle.lauf(bot, SEED, False, "", tg)
    finally: EINGRIFF["an"] = True
    o = tle.tab(r4["liste"]); eo = zeiten(o, "AAA")
    tle.pruefe(bot + ": 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei k+1 und k+4", r4["rc"] == 0 and not (eo & {k1, k4}), (r4["rc"], sorted(map(str, eo & {k1, k4}))))
    r5 = tle.lauf(bot, SEED, False, "", "{}"); g = tle.tab(r5["liste"])
    gl = lambda q: q[q["symbol"] != "AAA"][GLEICH].reset_index(drop=True).to_csv(index=False) if q is not None else None
    tle.pruefe(bot + ": 5 BBB/CCC mit und ohne Tag fuer AAA gleich", r5["rc"] == 0 and a is not None and gl(a) == gl(g), r5["rc"])
    r6, benutzt = m1_lauf(bot, tg); m = tle.tab(r6["liste"]); em = zeiten(m, "AAA")
    tle.pruefe(bot + ": 6 Mutante M1 (Kopie des Counters, Schranke hinter traded.add): W fehlt bei k+4 - die Probe 1 schlaegt an",
               benutzt and r6["rc"] == 0 and m is not None and k4 not in em and not any(q < T for q in em), (benutzt, r6["rc"], r6["fehler"] if r6["rc"] != 0 else sorted(map(str, em & {k1, k4}))))
SITE = """import importlib.util, os, sys
_m = os.environ.get("TB171_M1")
if _m:
    _s = importlib.util.spec_from_file_location("elliott_wave_counter", _m); _x = importlib.util.module_from_spec(_s)
    sys.modules["elliott_wave_counter"] = _x; _s.loader.exec_module(_x); open(_m + ".benutzt", "w").write("ja")
"""
def m1_lauf(bot, tg):
    """M1 nur an einer Kopie im Temp-Ordner: Schranke hinter traded.add; der Kindprozess laedt die Kopie ueber sitecustomize (PYTHONPATH)."""
    import tempfile, shutil
    q = os.path.join(tle.WURZEL, "strategies", bot, "elliott_wave_counter.py"); s = open(q, encoding="utf-8").read()
    alt = "            if min_entry_idx is not None and run_bar < min_entry_idx:\n                continue\n            traded.add(end_time)\n"
    neu = "            traded.add(end_time)\n            if min_entry_idx is not None and run_bar < min_entry_idx:\n                continue\n"
    e1, e2 = "_STRATEGY_DIR = os.path.dirname(os.path.abspath(__file__))", "get_strategy_paths(__file__)"
    if not (s.count(alt) == 1 and s.count(e1) == 1 and s.count(e2) == 1): return {"rc": None, "liste": None, "fehler": "M1: Stelle im Counter nicht genau einmal"}, False
    s = s.replace(alt, neu).replace(e1, "_STRATEGY_DIR = %r" % os.path.dirname(q)).replace(e2, "get_strategy_paths(%r)" % q)
    t = tempfile.mkdtemp(); m = os.path.join(t, "m1_elliott_wave_counter.py"); open(m, "w", encoding="utf-8").write(s)
    open(os.path.join(t, "sitecustomize.py"), "w", encoding="utf-8").write(SITE)
    vorher = {k: os.environ.get(k) for k in ("PYTHONPATH", "TB171_M1")}
    os.environ["PYTHONPATH"] = t + (os.pathsep + vorher["PYTHONPATH"] if vorher["PYTHONPATH"] else ""); os.environ["TB171_M1"] = m
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

