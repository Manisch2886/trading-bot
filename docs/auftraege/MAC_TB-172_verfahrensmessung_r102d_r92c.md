# TB-172 Verfahrensmessung R102 (d) und R92 (c) (R86 (e) für die Aktien-Bots): Indikatorwerte vor dem Horizontbeginn, Form von open_time am Snapshot — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 10:34** (Helfer BAU172, per Skript aus Bausteinen, `$HOME/sc/tb172/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis A an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `12a47f8`.**

**Sitzungstitel:** `TB-172` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `12a47f89bb458aacf690a2ae0d6a708bbea1935f` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-172`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (Python 3.9; das Werkzeug braucht nur die Standardbibliothek); Werkzeug `docs/belege/TB-172/tb172_werkzeug.py` (Anhang A, sha256 `5f712255e6027c14b05a01bf807e29f4c22a4744ef81a59d6368c50067c2dd29`), kurz `WZ`. **Belege:** `docs/belege/TB-172/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FH ⇒ FI).
**Grundlage:** R102 (d) (Register Z. 12320), R92 (c) (Z. 12020), R86 (e) (Z. 11896), 27.2; Vorbild Verfahrensmessung TB-148 (`docs/auftraege/MAC_TB-148_verfahrensmessung_schluessel_zeitzone_handelbar.md`), Form von Schritt 0 und Abbruchwegen wie TB-171. **Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ M (M1 R102 (d), M2 R92 (c), Nachher) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F. **Kein Registereintrag.** Befunde gehen als Frage an den Verfahrensprüfer; diese Sitzung entscheidet nichts.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 33 („Opus Trading Bots-16.10.2026 c“), 17.10.2026, 15:21, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-172 frei? Das ist eine reine Messung durch Lesen, mit Belegen, Ergebnis, BACKLOG-Satz und Journal. Es gibt keinen Registereintrag, keinen Handelscode, keine Kurse, kein Live und kein Geld. (1) R102 (d): Bilden rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout ihre Indikatoren aus Kursen vor dem Horizontbeginn? An der Kopie hiess das bei allen drei „ja“. Bei rsi2 habe ich es selbst nachgesehen: Die Indikatoren laufen über die ganze Reihe, entry_cutoff setzt nur den Startbalken. Laut Kommentar ist das der gewollte SMA(200)-Vorlauf. Das wird ein Befund für Fable zu 28.6/R57. (2) R92 (c): Im Snapshot tragen 150 von 150 Aktien-Dateien reine Kalenderdaten (1 417 557 Zeilen, keine Zone, keine verschiebende Uhrzeit). Damit ist R92 (c) erfüllt. Gelesen wird dort nur die Datumsspalte, kein Kurs. bau.sh endet mit rc 0, alle drei Simulationen waren gut. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Damit stehen die Befunde im Repo, und der R102-(d)-Befund kann mit der Antwort auf 17.10.a an Fable gehen."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. TB-172 ändert keinen Handelscode, keine Datei der Sperrliste, nichts unter `strategies/`, `shared/`, `research/`, `data/`, `snapshots/`, `config/`.

R102 (d) (Register Z. 12320), wörtlich: „(d) [Voraussetzung, vor der Neuerzeugung der Listen (R44) zu messen, nur das Ob (27.2): ob rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout Indikatorwerte aus Zeilen vor dem Horizontbeginn bilden.“

R92 (c) (Register Z. 12020), Ausschnitt wörtlich: „als Verfahrensmessung am Datenbestand des Snapshots (27.2), nur die Form: ob open_time in jeder Aktien-Tagesreihe als Kalenderdatum steht, ohne Zonenangabe und ohne Uhrzeit, die den Tag verschiebt; gezählt je Datei, kein Kurs wird gelesen oder genannt.“

## Verboten

Kein Programm des Repos ausführen oder importieren (das Werkzeug liest Quelltext per `ast` und Text, startet nichts). Kein Lauf auf Kursdaten; M2 liest im Snapshot je Zeile nur das Feld `open_time`, kein Kurs wird gelesen, ausgegeben oder genannt; `data/` wird weder gelesen noch geschrieben. Keine Neuerzeugung der Listen. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`, kein `rm`, kein `mv`. Keine Unter-Agenten.

## Die Messung (Anhang A, `WZ r102d`, `WZ r92c`)

**M1 — R102 (d), nur das Ob, durch Lesen des Codes.** Je Bot `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`: `strategies/<bot>/multi_symbol_optimise.py` (`load_all_symbol_data`, `get_trades_for_symbol`) und das Backtest-Modul (`run_backtest`); dazu der Weg des Listen-Erzeugers (`research/tb24_haltedauern/positionen_holen.py::lesesicht_an`, `research/exposure_messung/bot_lauf.py::_schranke_je_symbol`). **Regel, vor der Messung geschrieben:** „ja“, wenn weder beim Laden noch in `run_backtest` ein Zeilenschnitt an `open_time >=` steht und `entry_cutoff` nur den Startindex `start_i` setzt (dann geht die Reihe mit den Zeilen vor dem Horizontbeginn in `compute_indicators`); „nein“, wenn ein Zeilenschnitt vor der Übergabe `data[symbol] =` steht. **Kontrolle:** `elliott_wave_stocks` (Zeilenschnitt E-6/TB-163) muss als „nein“ erkannt werden, sonst `NEIN`. Beleg `BEL` `m1_r102d.md`: Tabelle Bot, Datei, Zeile, Rolle, Wortlaut (höchstens 200 Zeichen), drei Zeilen `- URTEIL R102 (d) <bot>: ja|nein`. Am Bau (Kopie, HEAD `12a47f8`): `URTEIL R102 (d) rsi2_mean_reversion: ja` · `URTEIL R102 (d) turtle_soup_stocks: ja` · `URTEIL R102 (d) volatility_breakout: ja` · `KONTROLLE elliott_wave_stocks: nein (Zeilenschnitt Z. 119)`.

**M2 — R92 (c), nur die Form, am Datenbestand des Snapshots** `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`: Aktien-Tagesreihen = Einträge des `MANIFEST.json` mit Namen `*_1d.csv` ohne `USDT`; je Datei sha256 gegen das MANIFEST und je Zeile nur `open_time` in Klassen gezählt: D nur Kalenderdatum `JJJJ-MM-TT` · M Datum mit `00:00[:00]` ohne Zone · Z mit Zonenangabe · U andere Uhrzeit ohne Zone · X sonst. **Regel:** Form erfüllt je Datei, wenn Spalte `open_time` da, Zeilen > 0 und Z + U + X = 0; R92 (c) erfüllt, wenn jede Datei so steht. Beleg `m2_r92c.md`: Zählung je Datei und Summe, eine Zeile `- URTEIL R92 (c): …`. Am Bau (Kopie): `Summe: Dateien 150, Zeilen 1417557, D 1417557, M 0, Z 0, U 0, X 0, doppelte Tage 0` · `URTEIL R92 (c): erfüllt (150 von 150 Dateien: open_time Kalenderdatum, ohne Zone, ohne verschiebende Uhrzeit; D 1417557, M 0)`.

**Zur Kenntnis (gemeldet, nicht entschieden):** (1) R102 (c) (Z. 12320) nennt als Bauart „rsi2_mean_reversion, Z. 106 vor Z. 112“ und „der Zeilenschnitt am Horizontbeginn bleibt“; am Code ist bei `rsi2_mean_reversion` Z. 112 kein Zeilenschnitt, sondern nur `entry_cutoff = horizontbeginn_ts(...)` (Docstring Z. 75–79: „KEINE Kappung … vor der Indikator-Berechnung“). (2) TB-148 hielt `snapshots/` aus dem Lesen heraus (Sichtschutz 27.1); R92 (c) verlangt die Messung am Datenbestand des Snapshots, nur die Form: das Werkzeug liest nur `open_time` und nennt keine Kurse.

## Lage nach dem Auslegen

Beim Start genau 2 Einträge (Soll in 0a).

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `12a47f89bb458aacf690a2ae0d6a708bbea1935f`, genau diese 2 Einträge, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md
```

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb172_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "12a47f89bb458aacf690a2ae0d6a708bbea1935f": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "12a47f89bb458aacf690a2ae0d6a708bbea1935f": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (2 Eintraege)`. Anhang holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb172_werkzeug.py 5f712255e6027c14b05a01bf807e29f4c22a4744ef81a59d6368c50067c2dd29`; `Dateien 1`; sonst **ABBRUCH**. Dann genau diese `git add`, Commit `TB-172 Schritt 0: Stand des steuernden Chats vor TB-172 (Auftrag)`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/auftraege/MAC_TB-172_verfahrensmessung_r102d_r92c.md
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-172
cp "$TMPDIR/tb172_0a.txt" docs/belege/TB-172/0a_status.txt
cp "$TMPDIR/tb172_werkzeug.py" docs/belege/TB-172/tb172_werkzeug.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py voraussetzung > docs/belege/TB-172/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (20 Prüfungen am Bau: 14 gelesene Dateien je md5 = Bau, Messbelege noch nicht da, R102 (d) und R92 (c) im Wortlaut, BACKLOG Rang 1 Stand TB-171, Journal FH, Snapshot da). **Abbruch in V:** im Arbeitsbaum liegt nur der unverfolgte Ordner `BEL`. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-172/abbruch.txt`, dann `git add` mit Namen für `abbruch.txt`, `0a_status.txt`, `tb172_werkzeug.py` und `v_voraussetzung.txt`, Commit `TB-172 Abbruch: V`, pushen, `git status --porcelain` leer; melden.

## Schritt M — messen

```
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py r102d docs/belege/TB-172/m1_r102d.md > docs/belege/TB-172/m1_r102d.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/m1_r102d.txt
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py r92c docs/belege/TB-172/m2_r92c.md > docs/belege/TB-172/m2_r92c.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/m2_r92c.txt
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py nachher > docs/belege/TB-172/m_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/m_nachher.txt
```

Soll: `m1_r102d.txt`, `m2_r92c.txt`, `m_nachher.txt` enden je mit `rc 0` (rc 0 heisst: Messung vollständig, Kontrolle erkannt, sha256 = MANIFEST; „ja“ bei R102 (d) oder „nicht erfüllt“ bei R92 (c) ist ein Befund, kein Abbruch). **Abbruchweg M** (ein Beleg nicht `rc 0`; kein M-Commit):

```
trading-env/bin/python3 -B -c "open('docs/belege/TB-172/abbruch.txt', 'w').write('M: erster Beleg ohne rc 0, siehe Belege\n')"
trading-env/bin/python3 -B -c "import os, subprocess; f = ['docs/belege/TB-172/' + x for x in ('abbruch.txt', '0a_status.txt', 'tb172_werkzeug.py', 'v_voraussetzung.txt', 'm1_r102d.md', 'm1_r102d.txt', 'm2_r92c.md', 'm2_r92c.txt', 'm_nachher.txt')]; d = [x for x in f if os.path.exists(x)]; print('git add', len(d), 'von', len(f)); raise SystemExit(subprocess.run(['git', 'add'] + d).returncode)"
git commit -q -m "TB-172 Abbruch: M"
git push -q origin main
git status --porcelain
```

Der Abbruchweg fügt nur vorhandene Belege hinzu (eine Python-Zeile prüft jeden Pfad vor `git add`). Soll danach: `git status --porcelain` ohne Ausgabe; scheitert der Push: melden, nicht wiederholen. Sonst (alle `rc 0`) genau diese `git add`, Commit `TB-172 M: Verfahrensmessung R102 (d) und R92 (c)`, pushen ⇒ **⟨M⟩**:

```
git add docs/belege/TB-172/0a_status.txt
git add docs/belege/TB-172/tb172_werkzeug.py
git add docs/belege/TB-172/v_voraussetzung.txt
git add docs/belege/TB-172/m1_r102d.md
git add docs/belege/TB-172/m1_r102d.txt
git add docs/belege/TB-172/m2_r92c.md
git add docs/belege/TB-172/m2_r92c.txt
git add docs/belege/TB-172/m_nachher.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ kennung` (Soll „Kennung FI …“). Block nach `docs/belege/TB-172/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-172: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md` mit: Kurz; V wörtlich (letzte Zeilen); M1 (die drei Urteilszeilen und die Kontrollzeile wörtlich, Verweis auf die Tabelle in `m1_r102d.md`) — belegt: Fundstellen, erschlossen: das Ob am Code, offen: Wirkung auf 28.6/R57; M2 (Summenzeile und Urteilszeile wörtlich; Abweichungen je Datei, falls da) — belegt: Zählung; R86 (e) für die vier Aktien-Bots: Stand nach M2; Befunde für den Verfahrensprüfer (nur melden: R102 (d) „ja“ je Bot; R92 (c) falls nicht erfüllt; die zwei Punkte „Zur Kenntnis“); Abweichungen; In einfacher Sprache. Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Dann:

```
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py kennung > docs/belege/TB-172/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-172/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-172/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py journal docs/belege/TB-172/a_block.md --probe > docs/belege/TB-172/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-172/tb172_werkzeug.py journal docs/belege/TB-172/a_block.md > docs/belege/TB-172/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-172/a_journal.txt
```

Soll je `rc 0`. Genau diese `git add`, Commit `TB-172 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-172/a_kennung.txt
git add docs/belege/TB-172/a_backlog_probe.txt
git add docs/belege/TB-172/a_backlog.txt
git add docs/belege/TB-172/a_block.md
git add docs/belege/TB-172/a_journal_probe.txt
git add docs/belege/TB-172/a_journal.txt
```

**F.**

```
git status --porcelain > "$TMPDIR/tb172_f.txt"
cp "$TMPDIR/tb172_f.txt" docs/belege/TB-172/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-172/f_numstat.txt
git add docs/belege/TB-172/f_porcelain.txt
git add docs/belege/TB-172/f_numstat.txt
git commit -q -m "TB-172 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; im numstat nur `docs/` (kein Pfad unter `strategies/`, `shared/`, `research/`, `data/`, `snapshots/`).

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V nicht `rc 0`; ein Beleg aus M nicht `rc 0` (dann Abbruchweg M, **kein M-Commit**); A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Bevor die neun Trade-Listen neu erzeugt werden, sind zwei Dinge nachzumessen, ohne etwas zu rechnen. Erstens: Lesen drei Aktien-Bots für ihre Kennzahlen (RSI, Donchian, Bollinger) auch Kurstage vor dem Beginn ihres Zeitraums? Das wird am Programmtext abgelesen. Zweitens: Steht in jeder Aktien-Kursdatei des eingefrorenen Datenstands das Datum als reiner Kalendertag, ohne Uhrzeit oder Zeitzone, die den Tag verschieben könnte? Das wird je Datei gezählt, ohne einen Kurs anzusehen. Was dabei auffällt, geht als Frage an den Prüfer; hier wird nichts geändert.

## Anhänge

### Anhang A — Werkzeug

<!-- DATEI tb172_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-172 Werkzeug (Anhang A): Verfahrensmessung R102 (d) (Lesen des Codes, nur das Ob) und R92 (c) (Form von open_time am Snapshot, je Datei gezaehlt, kein Kurs).
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel; importiert und startet kein Programm des Repos. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | r102d <BELEG> | r92c <BELEG> | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import ast, csv, datetime, hashlib, json, os, re, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-172/"
SNAP = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
CODE = { "strategies/rsi2_mean_reversion/multi_symbol_optimise.py": "b325d38f55279e6b80839b6e12857849", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "58589cfbdc50a5e0c602014f88fe73ae", "strategies/rsi2_mean_reversion/equity_simulation.py": "774e7fecad93bdad38bcba5e568b7243", "strategies/turtle_soup_stocks/multi_symbol_optimise.py": "0d7398e704778a0cfb84424ff4d76486", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "d8f24c681d39e300a8bfd28580b446d6", "strategies/turtle_soup_stocks/equity_simulation.py": "f45e55aadcb9d03b4342ec32e8644914", "strategies/volatility_breakout/multi_symbol_optimise.py": "3ec15ddc4140e51e452ec0cddd43f18f", "strategies/volatility_breakout/backtest_breakout.py": "ea48150ccab663f981bd4fa3f772a06a", "strategies/volatility_breakout/equity_simulation.py": "dd5fa96bb927aecb26051fbaefb4a0cd", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "571076168d56f9e809ef0595f53d6e7d", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json": "e0f647ce41f55a918547bb505eb5ecbf", "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/config/sp500_top150.txt": "bf54515b89f6e6e9e458ff6e6c8dcae9" }
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; R105 (d) t3_supertrend unberührt |"
BOTS = (("rsi2_mean_reversion", "backtest_rsi2.py"), ("turtle_soup_stocks", "backtest_turtle_soup.py"), ("volatility_breakout", "backtest_breakout.py"), ("elliott_wave_stocks", None))
W102 = "(d) [Voraussetzung, vor der Neuerzeugung der Listen (R44) zu messen, nur das Ob (27.2): ob rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout Indikatorwerte aus Zeilen vor dem Horizontbeginn bilden."
W92 = "als Verfahrensmessung am Datenbestand des Snapshots (27.2), nur die Form: ob open_time in jeder Aktien-Tagesreihe als Kalenderdatum steht, ohne Zonenangabe und ohne Uhrzeit, die den Tag verschiebt; gezählt je Datei, kein Kurs wird gelesen oder genannt."
RC, HZ, CI, AB, RB = r"pd\.read_csv\(", r"horizontbeginn_ts\(", r"compute_indicators\(", r"data\[symbol\]\s*=", r"run_backtest\("
CUT, ST = r"\[\s*\w+\[\s*[\"']open_time[\"']\s*\]\s*>=", r"start_i\s*=\s*max\(\s*start_i\s*,.*entry_cutoff"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def kurz(s): s = s.strip(); return s if len(s) <= 200 else s[:199] + "…"
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "unveraendert seit dem Bau: %s md5 %s" % (f, m[:12]))
def funktion(datei, name):
    q = lies(datei); z = q.split("\n")
    for k in ast.walk(ast.parse(q)):
        if isinstance(k, ast.FunctionDef) and k.name == name:
            a = k.lineno
            if k.body and isinstance(k.body[0], ast.Expr) and isinstance(getattr(k.body[0], "value", None), ast.Constant) and isinstance(k.body[0].value.value, str): a = k.body[0].end_lineno + 1
            return [(n, z[n - 1]) for n in range(a, k.end_lineno + 1)]
    return []
def treffer(zeilen, muster): return [(n, l) for n, l in zeilen if re.search(muster, l) and not l.strip().startswith("#")]
def voraussetzung():
    code_gleich(); p(not os.path.exists(BEL + "m1_r102d.md") and not os.path.exists(BEL + "m2_r92c.md"), "Messbelege m1/m2 noch nicht da")
    reg = lies(REG).split("\n"); r102 = [l for l in reg if l.startswith("> R102 — ")]; r92 = [l for l in reg if l.startswith("> R92 — ")]
    p(len(r102) == 1 and W102 in r102[0], "Register: R102 genau einmal, (d) im Wortlaut"); p(len(r92) == 1 and W92 in r92[0], "Register: R92 genau einmal, (c) im Wortlaut")
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]; p(len(z) == 1 and z[0].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-171")
    p(max(kennungen()) == "FH", "Journal: hoechste FH (naechste FI)"); p(os.path.exists(SNAP + "/MANIFEST.json"), "Snapshot mit MANIFEST.json: " + SNAP[:22] + "…")
    ende()
def r102d(beleg):
    L = ["# TB-172 M1 — R102 (d), nur das Ob: bilden rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout Indikatorwerte aus Zeilen vor dem Horizontbeginn?", "",
         "Gelesen per `ast` und Zeilensuche (Werkzeug `r102d`); nichts ausgeführt, nichts importiert, kein Kurs. Wortlaut je Zeile höchstens 200 Zeichen; Kommentar- und Docstring-Zeilen zählen nicht als Code.", "",
         "Regel (vor der Messung im Auftrag geschrieben): **ja**, wenn weder in `load_all_symbol_data` (Optimierer) noch in `run_backtest` (Backtest-Modul) ein Zeilenschnitt an `open_time >=` steht und `entry_cutoff` im Backtest nur den Startindex `start_i` setzt; dann geht die eingelesene Reihe mit den Zeilen vor dem Horizontbeginn in `compute_indicators`. **nein**, wenn ein Zeilenschnitt vor der Übergabe `data[symbol] =` steht (Kontrolle: `elliott_wave_stocks`, E-6/TB-163).", "",
         "| Bot | Datei | Z. | Rolle | Wortlaut |", "|---|---|---|---|---|"]
    U = []
    def zeile(bot, datei, tr, rolle):
        for n, l in tr: L.append("| %s | `%s` | %d | %s | `%s` |" % (bot, datei, n, rolle, kurz(l).replace("|", "\\|").replace("`", "'")))
    for bot, bm in BOTS:
        mso = "strategies/%s/multi_symbol_optimise.py" % bot; f = funktion(mso, "load_all_symbol_data"); rc_, hz, cut, ci, ab = [treffer(f, m) for m in (RC, HZ, CUT, CI, AB)]
        for t, r in ((rc_, "Einlesen"), (hz, "Horizontbeginn"), (cut, "Zeilenschnitt"), (ci, "Indikatoren beim Laden"), (ab, "Übergabe")): zeile(bot, mso, t, r)
        da = p(bool(f and rc_ and hz and ab), "%s: load_all_symbol_data mit Einlesen, Horizontbeginn, Übergabe gefunden" % bot)
        schnitt = bool(cut and ab) and cut[0][0] < ab[0][0]
        if bm is None:
            p(schnitt, "Kontrolle %s: Zeilenschnitt vor der Übergabe erkannt" % bot); U.append("KONTROLLE %s: %s" % (bot, ("nein (Zeilenschnitt Z. %d)" % cut[0][0]) if schnitt else "kein Schnitt erkannt")); continue
        g = funktion(mso, "get_trades_for_symbol"); ci2, rb = treffer(g, CI), treffer(g, RB); zeile(bot, mso, ci2, "Indikatoren je Lauf"); zeile(bot, mso, rb, "Backtest")
        bd = "strategies/%s/%s" % (bot, bm); r = funktion(bd, "run_backtest"); st, cut2 = treffer(r, ST), treffer(r, CUT); zeile(bot, bd, st, "entry_cutoff setzt Startindex"); zeile(bot, bd, cut2, "Zeilenschnitt")
        p(bool((ci or ci2) and rb and st), "%s: compute_indicators, run_backtest, start_i aus entry_cutoff gefunden" % bot)
        U.append("URTEIL R102 (d) %s: %s" % (bot, "ja" if da and not cut and not cut2 else "nein"))
    for datei, fn, m, rolle in (("research/tb24_haltedauern/positionen_holen.py", "lesesicht_an", r"_vor_schnitt\(", "Erzeuger: Sicht nur am Schnitt"), ("research/exposure_messung/bot_lauf.py", "_schranke_je_symbol", r"neu\[symbol\]\s*=\s*\(df,", "Erzeuger: df unverändert")):
        f = funktion(datei, fn); t, c = treffer(f, m), treffer(f, CUT); zeile("Erzeuger", datei, t + c, rolle); p(bool(t) and not c, "%s %s: gefunden, kein Zeilenschnitt an open_time >=" % (datei, fn))
    L += ["", "## Urteil (erschlossen am Code, nicht durch Lauf)", ""] + ["- " + u for u in U] + ["", "Bei **ja**: Befund zu 28.6 und R57, kommt als Frage an den Verfahrensprüfer (R102 (d)); hier ist nichts entschieden."]
    schreibe(beleg, "\n".join(L) + "\n"); print("\n".join(U)); ende()
KL = (("D", re.compile(r"^\d{4}-\d{2}-\d{2}$")), ("M", re.compile(r"^\d{4}-\d{2}-\d{2}[ T]00:00(:00(\.0+)?)?$")),
      ("Z", re.compile(r"^\d{4}-\d{2}-\d{2}([ T][0-9:.]+)?\s*(Z|UTC|[+-]\d{2}:?\d{2})$")), ("U", re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?$")))
def klasse(v):
    for k, r in KL:
        if r.match(v):
            try: datetime.date(int(v[:4]), int(v[5:7]), int(v[8:10]))
            except ValueError: return "X"
            return k
    return "X"
def r92c(beleg):
    m = json.loads(lies(SNAP + "/MANIFEST.json")); dat = m.get("dateien", {}); a = sorted(k for k in dat if k.endswith("_1d.csv") and "USDT" not in k and "/" not in k)
    sp = set(s.strip() + "_1d.csv" for s in lies(SNAP + "/config/sp500_top150.txt").split("\n") if s.strip() and not s.strip().startswith("#"))
    p(len(a) > 0, "MANIFEST: %d Aktien-Tagesreihen (Name *_1d.csv ohne USDT; Art %s)" % (len(a), sorted(set(dat[k].get("art", "?") for k in a))))
    L = ["# TB-172 M2 — R92 (c), nur die Form von open_time je Aktien-Tagesreihe des Snapshots", "", "Snapshot `%s`. Gelesen je Zeile nur das Feld `open_time` (csv, Standardbibliothek); kein Kurs gelesen oder genannt. Klassen: D nur Kalenderdatum `JJJJ-MM-TT` · M Datum mit `00:00[:00]` ohne Zone · Z mit Zonenangabe · U andere Uhrzeit ohne Zone · X sonst (leer, ungültig). Form erfüllt, wenn Spalte da, Zeilen > 0 und Z + U + X = 0." % SNAP, "",
         "Abgleich mit `config/sp500_top150.txt`: nur im MANIFEST %s · nur in der Liste %s" % (sorted(set(a) - sp)[:10], sorted(sp - set(a))[:10]), "",
         "| Datei | Zeilen | D | M | Z | U | X | doppelte Tage | sha256 = MANIFEST | Form |", "|---|---|---|---|---|---|---|---|---|---|"]
    S = dict.fromkeys("NDMZUX", 0); abw, sha_ok, dup_s = [], 0, 0
    for n in a:
        f = SNAP + "/" + n; z = dict.fromkeys("NDMZUX", 0); tage, dup, spalte = set(), 0, False; h = hashlib.sha256()
        with open(f, "rb") as fb:
            for blk in iter(lambda: fb.read(1 << 20), b""): h.update(blk)
        ok_sha = h.hexdigest() == dat[n].get("sha256"); sha_ok += ok_sha
        with open(f, encoding="utf-8", newline="") as fh:
            r = csv.reader(fh); kopf = next(r, [])
            if "open_time" in kopf:
                spalte, i = True, kopf.index("open_time")
                for row in r:
                    v = row[i].strip() if len(row) > i else ""; k = klasse(v); z["N"] += 1; z[k] += 1
                    if k in "DM": dup += v[:10] in tage; tage.add(v[:10])
        form = spalte and z["N"] > 0 and z["Z"] + z["U"] + z["X"] == 0
        if not form: abw.append(n)
        for k in S: S[k] += z[k]
        dup_s += dup
        L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %s | %s |" % (n, z["N"], z["D"], z["M"], z["Z"], z["U"], z["X"], dup, "ja" if ok_sha else "NEIN", "ja" if form else ("NEIN (keine Spalte open_time)" if not spalte else "NEIN")))
    L.append("| **Summe %d Dateien** | %d | %d | %d | %d | %d | %d | %d | %d ja | %d ja |" % (len(a), S["N"], S["D"], S["M"], S["Z"], S["U"], S["X"], dup_s, sha_ok, len(a) - len(abw)))
    p(sha_ok == len(a), "sha256 je Aktien-Datei = MANIFEST (%d von %d)" % (sha_ok, len(a)))
    u = ("URTEIL R92 (c): erfüllt (%d von %d Dateien: open_time Kalenderdatum, ohne Zone, ohne verschiebende Uhrzeit; D %d, M %d)" % (len(a), len(a), S["D"], S["M"])) if not abw else ("URTEIL R92 (c): nicht erfüllt (%d von %d Dateien weichen ab: %s)" % (len(abw), len(a), ", ".join(abw[:10])))
    L += ["", "## Urteil (gezählt)", "", "- " + u, "", "Nicht erfüllt: kommt mit der Fundstelle als Frage an den Verfahrensprüfer (R92 (c)); hier ist nichts entschieden."]
    schreibe(beleg, "\n".join(L) + "\n"); print("Summe: Dateien %d, Zeilen %d, D %d, M %d, Z %d, U %d, X %d, doppelte Tage %d" % (len(a), S["N"], S["D"], S["M"], S["Z"], S["U"], S["X"], dup_s)); print(u); ende()
def nachher():
    code_gleich()
    for b, n in (("m1_r102d", 3), ("m2_r92c", 1)):
        t = lies(BEL + b + ".txt").rstrip("\n").split("\n") if os.path.exists(BEL + b + ".txt") else [""]; md = lies(BEL + b + ".md") if os.path.exists(BEL + b + ".md") else ""
        p(t[-1] == "rc 0", "%s.txt endet mit rc 0" % b); p(len(re.findall(r"^- URTEIL R", md, re.M)) == n, "%s.md: %d Urteilszeile(n)" % (b, n))
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    m1 = lies(BEL + "m1_r102d.md") if os.path.exists(BEL + "m1_r102d.md") else ""; m2 = lies(BEL + "m2_r92c.md") if os.path.exists(BEL + "m2_r92c.md") else ""
    u1 = re.findall(r"^- URTEIL R102 \(d\) (\w+): (\w+)$", m1, re.M); u2 = re.findall(r"^- URTEIL R92 \(c\): (.*)$", m2, re.M)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    p(len(u1) == 3 and len(u2) == 1, "Urteile aus m1 (3) und m2 (1) gelesen")
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-171") and not nein():
        z[a[0]] = z[a[0]][:-2] + (" · **TB-172 (%s, Journal %s): Verfahrensmessung R102 (d) und R92 (c) (R86 (e) für die Aktien-Bots)** (R102 (d) durch Lesen des Codes, nur das Ob, ob Indikatorwerte aus Zeilen vor dem Horizontbeginn gebildet werden: %s; "
            "R92 (c) am Snapshot 63e4b6c8…, nur die Form von open_time je Aktien-Datei, kein Kurs: %s); Befunde gehen als Frage an den Verfahrensprüfer, hier nichts entschieden |") % (datum, kenn, ", ".join("%s %s" % x for x in u1), u2[0][:300])
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen())); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-172: " % neu), "Kopfzeile ## %s — TB-172: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 2 and a[0] == "r102d": r102d(a[1])
    elif len(a) == 2 and a[0] == "r92c": r92c(a[1])
    elif a == ["nachher"]: nachher()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

