# TB-175 Register 67 (Fable 17b, R107, neun Marken), Prüfung 13 in `test_haltedauer_kern.py` erneuern (Teil 1) (ohne E2) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 19:10** (Helfer BAU175, per Skript aus Bausteinen, `/tmp/w/sc/tb175/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis E (mit R und K) an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `5031cd0`; Start am HEAD `5031cd0207234379d4a427de6734d42f6f814a0e`.**

**Sitzungstitel:** `TB-175` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `5031cd0207234379d4a427de6734d42f6f814a0e` (kommt bis zum Start ein Commit dazu, füllt der steuernde Chat HEAD und Soll neu) · **Start:** über den Sitzungswächter (`starte_TB-175`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (Python 3.9, numpy 2.0.2, pandas 2.3.3 nach `requirements.lock`); Werkzeug `docs/belege/TB-175/tb175_werkzeug.py` (Anhang A), kurz `WZ`. **Belege:** `docs/belege/TB-175/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-175_pruefung13_leser_alle_trades.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FK ⇒ FL).
**Grundlage Register (zeichengleich, nicht umdeuten):** Fable-Antwort 17.10.b (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md`, md5 `d13e691973d3b98528b72c67ac000eb9`, 10 051 B; bis Schritt 0 git-ignoriert unter `data_sicherung/steuernder_chat_tmp/f17b/`), Registerblock R107; Anfrage 17.10.b (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md`, md5 `af2c861a88a083dd7652dcbc07650d8f`, 5 797 B, ebenda); R56 (b) (Anfrage und Antwort mit Commit im Repo, bevor eingetragen wird); Bauart 66 (Register aus Fable mit Marken, TB-173). Quelle des Auftrags: Nachricht des steuernden Chats an den Helfer BAU175 vom 17.10.2026 (ausserhalb des Repos).
**Ohne E2:** die Umstellung der Leser (R107 (e)) ist gebaut, geht aber erst nach einer Frage an den Verfahrensprüfer (D4: Embargo t3_supertrend 13 → 12 ändert eine registrierte Herleitung); hier nicht enthalten.
**Grundlage Teil 1:** Bestand BESTAND_RANG1B Abschnitt 2 (steuernder Chat, 17.10.2026); Beleg `docs/belege/TB-169/e_alt_vorher.txt` Z. 61 (Prüfung 13 rot, einziges FEHLT, rc 1); `research/tb24_haltedauern/positionen_holen.py` Z. 116 (`--ziel`, `required=True`), Z. 124 (`ZIEL_DIR`), Z. 190–204 (`_schreibe_einmal`, `O_CREAT|O_EXCL`) am Bau-HEAD.
**Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 (mit Fable 17.10.b ins Repo) ⇒ V ⇒ R (Register 67 und neun Marken) ⇒ K (Kopien, Index, Dialog-Index) ⇒ E (Teil 1: Prüfung 13) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F. Registereintrag nur in R.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 34 („Opus Trading Bots-17.10.2026 a“), 17.10.2026, 19:14, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-175 frei? Der Auftrag macht drei Dinge. (1) Er bringt Anfrage und Antwort von Fable 17.10.b unverändert ins Repo, mit md5 vorher und nachher. (2) Er schreibt Register 67 mit R107, zeichengleich aus der Antwort, dazu die neun Marken nach R107 (f) und Tatsachennotizen. Die Notizen halten fest: Die t3-Voraussetzung deckt TB-169 3b ab, aber nur als Teilmessung. Die Leser lasen bisher ausgeführte Positionen. Über alle gefundenen Trades fiele das Embargo von t3 von 13 auf 12, das geht als Frage an Fable. (3) Er erneuert Prüfung 13 im Alt-Test der Haltedauern, die seit TB-98 rot ist. Die Prüfung kontrolliert jetzt: Ziel nur aus --ziel, Schreiben nur einmalig. Zusätzlich bekommen die drei git-Aufrufe im Test --no-optional-locks. Kein Handelscode, keine Kurse, kein Live, kein Geld. Die Leser-Umstellung ist nicht dabei, sie wird TB-176 nach Fable. bau.sh endet mit rc 0, die drei Simulationen waren gut. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Das Register steht dann auf dem Stand der Fable-Antwort, und der Alt-Test ist wieder grün."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. `WZ register` übernimmt die Zeile wörtlich in den Kopfsatz von 67. TB-175 ändert keinen Handelscode und keine Datei der Sperrliste; Teil 1 ändert genau eine Testdatei: `research/tb24_haltedauern/test_haltedauer_kern.py`.

## Was eingetragen wird (Schritt R, K)

- **Abschnitt 67** (`WZ register`): Titel `## 67. Fable 17b — Registerblock R107 (TB-175)`; Kopfsatz (Bauart 66, Quelle mit md5, Karte wörtlich); **67.1 R107** „> R107 …“ und „> Quelle des Grundes“ **zeichengleich** aus dem Codeblock der Antwort (das Werkzeug liest sie aus der Datei und vergleicht nach dem Schreiben Zeichen für Zeichen), eine „**Kette:**“-Zeile; **67.2 Voraussetzungen und Befunde**: `v_voraussetzung.txt` wörtlich eingerückt und die Tatsachennotizen **(a)** Voraussetzung R107 (b) gemessen durch Lesen: TB-169 3b führt t3_supertrend (`docs/belege/TB-169/e_abnahme.txt`, `test_listen_erzeuger.py`), Wachen eingeschaltet; Einschränkung: Vergleich mit Lauf B (Schranke am natürlichen Tag), nicht mit ausgeschalteter Schranke, und Prüfung 8 prüft den 3b-Lauf nicht — Teilmessung, zur Kenntnis an den Verfahrensprüfer; **(b)** Voraussetzung R107 (e) gemessen durch Lesen: die drei Leser aus R107 (e) (`auswertung.py`, `embargo_neun.py`, `grundlage.py` mit `messung.py`) und dazu `wf_kapital_dd/messung.py` lasen ausgeführte Positionen; B3, B6/B7, C2 rechneten nicht aus gefundenen Trades; noch nicht umgestellt; Befund vor der Umstellung (D4 in `test_faltenplan_neun.py`, t3_supertrend P90 und Embargo, Zahlen per Skript aus dem Bau-Beleg); Frage an den Verfahrensprüfer. Die Umstellung (E2) folgt als eigener Bauauftrag nach der Fable-Antwort. Alle Fundstellen (Datei, Zeile) stehen im Werkzeug (`FUND`, am Bau per Skript aus dem Bestand des steuernden Chats gezogen und am Repo geprüft); V prüft jede Zeile, die Notiz zitiert e_abnahme.txt per Skript; **(c)** Zählung: R107 (a) nennt den sechzehnten Fall, Indexzeilen an 48.20 und 54.3 nur wie R107 (f) sagt; **(d)** R56 (b): Anfrage und Antwort 17.10.b seit ⟨S0⟩ im Repo, md5 vorher = nachher.
- **Neun Marken** (R107 (f)); je Zeilenpaar wie 66 (Leerzeile, Marke, „Eintrag und Stand oben bleiben zeichengleich.“); der alte Satz bleibt unberührt; steht am Ort schon eine Marke, kommt die neue dahinter (an 64.1 nach dem Absatz „Abnahme nach R98 (d)“ und seinen Marken aus R105, R106; an 16.4 und 16.8 am Ende des Unterabschnitts vor `---`; sonst nach der letzten Zeichengleich-Zeile bzw. nach „> Quelle des Grundes“):
  - an 62.3: `> ⭐ **62.3 R102 ERGÄNZT und BERICHTIGT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (a): ERGÄNZT zu (d), BERICHTIGT zu (c) („lies“), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 55.4: `> ⭐ **55.4 R81 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (a), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 66.1: `> ⭐ **66.1 R106 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (b), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 64.1: `> ⭐ **64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (b), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 56.3: `> ⭐ **56.3 R86 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkte (c) und (e), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 57.3: `> ⭐ **57.3 R92 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (c): die Voraussetzung in (c) ist gemessen erfüllt, TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 16.4: `> ⭐ **16.4 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (d), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 16.8: `> ⭐ **16.8 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (d), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 58.4: `> ⭐ **58.4 R97 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (e), TB-175, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
- **Ohne Marke** (R107 (f)): 28.6, 51.2 (R57), 26.2, 16.9, 62.2 (R101), 55.1 (R78), 56.1 (R84), 48.13 (R45), 57.1 (R90), 61.1 (R98), 58.1 (R94), 58.2 (R95), 60.1, 63.1, 24.3, 17.1, 17.2, 29.3, 37.3, 37.5, 40.6, 62.5, 66.2, Abschnitte 9, 10, 41, 42.
- **Index** (K, `WZ index`): Kopf 0–67, Zeile `| 67 aus 17b |`, neuer Abschnitt 18 (Tabelle der neun Marken aus `r_daten.json`) mit „Indexzeilen aus Fable 17b“: 48.20 (R52) und 54.3 (R76) → R107 (a), sechzehnter Fall, sechzehn Fälle (R107 (f)), ohne Marke. **Dialog-Index** 17b über Handfelder.
- Append-only bis auf die neun Marken (`WZ register` prüft es nach dem Schreiben). Register am Bau-HEAD 12595 Zeilen, 66 letzter Abschnitt, kein „R107“.

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen; aus `data_sicherung/` nur die zwei Fable-Dateien in Schritt 0 kopieren. Keine Neuerzeugung der neun Listen; `positionen_holen.py`, `alle_bots.py`, `auswertung.py` werden nicht gestartet. Nichts unter `strategies/`, `shared/`, `data/`, `config/` ändern; unter `research/` in Teil 1 nur `research/tb24_haltedauern/test_haltedauer_kern.py`. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`, kein `git stash`, kein `rm`, kein `mv`. **Schreiben darf die Sitzung nur:** die zwei Fable-Dateien (Schritt 0, `cp`), `docs/VORREGISTRIERUNG_neuselektion.md` (nur `WZ register`), `REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Befehlen), `research/tb24_haltedauern/test_haltedauer_kern.py` (E), `BACKLOG.md` (`WZ backlog`), `JOURNAL.md` (`WZ journal`), `BEL`, das Ergebnis.

## Teil 1 — die neue Prüfung 13 (Anhang B: `research/tb24_haltedauern/test_haltedauer_kern.py` vollständig, sha256 `b73adc87d57c764eb71ee00f725019dcedb70164599a20c7e9c77e6d065f8cba`; Bau-Stand md5 `807d278e60a953cac40a836d28d13c96`)

**Am Bau-HEAD gemessen:** Prüfung 13 (`wache_repo_unveraendert`, Z. 330–402) prüft (a) Arbeitsbaum vor = nach über `git status --porcelain` und `git diff -- <8 Produktivordner>`, (b) per Syntaxbaum: ein schreibendes Programm muss *irgendwo* `ERGEBNIS_DIR`, `DATEN_DIR` oder `TemporaryDirectory` nennen, und *jedes* `to_csv` zählt als Schreiben. Seit 46e3ed0 (TB-98) schreibt `positionen_holen.py` in den Ordner aus `--ziel` über `_schreibe_einmal`; sein einziges `to_csv` (`alle.to_csv(index=False)`) liefert nur Text ⇒ (b) rot.

**Neu in (b):** je Schreibaufruf (open/`os.open`/`os.fdopen` mit Schreibmodus bzw. -flags, `to_csv`/`to_json`/… nur mit Ziel, `os.makedirs`/`replace`/…, `shutil.*`, `np.save*`, `write_text`) ein erlaubter Ort — allgemein: der Aufruf bildet sein Ziel aus `ERGEBNIS_DIR`/`DATEN_DIR` (je genau einmal auf Modulebene aus `_DIR`) oder liegt in einem `with …TemporaryDirectory()`; **`positionen_holen.py`:** `--ziel` genau einmal, `required=True`, kein `default`, kein `set_defaults`; `ZIEL_DIR` genau einmal, nur `os.path.abspath(<parse_args>.ziel)`; jeder Schreibaufruf liegt in `_schreibe_einmal`, dort `os.open` mit `O_CREAT|O_EXCL` ohne `O_TRUNC` auf einen Pfad aus `ZIEL_DIR`, sonst nur `os.fdopen`. Dazu sechs Gegenproben im Speicher (`GEGENPROBEN_13`: Voreinstellung, nicht Pflicht, `ZIEL_DIR` nicht aus `--ziel`, `O_TRUNC` statt `O_EXCL`, `open(…, "w")` statt `_schreibe_einmal`, `auswertung.py` schreibt neben `ERGEBNIS_DIR`); jede muss genau einmal treffen und rot machen. `wache_repo_unveraendert(ordner=None)` nimmt für die Gegenprobe an Kopien einen Ordner; Aufruf im Test unverändert. **(a):** nur `--no-optional-locks` an den drei git-Aufrufen (Z. 317, 319, 364), sonst unverändert. Übrige Abschnitte des Tests unverändert (Unterschied nur in Z. 317–402).

**Am Bau gemessen (Gerät, Python 3.10.12, an der Kopie):** alt rc 1 mit genau dem einen FEHLT; neu rc 0, 50 ok-Zeilen vor 13 gleich, Prüfung 13 mit 8 ok; Gegenprobe an Kopien: Voreinstellung und `open(…, "w")` rot.

**Teil (a) — entschieden (steuernder Chat, 17.10.2026: Vorschlag B):** Der Test rief `git status --porcelain` (Z. 317, 364) und `git diff` (Z. 319) ohne `--no-optional-locks`; git durfte dabei `.git/index` auffrischen und kurz `.git/index.lock` anlegen (nicht im porcelain sichtbar). Hier läuft der Test nach ⟨S0⟩, wie in TB-169. Schwäche: eine Inhaltsänderung an einer schon geänderten Datei ausserhalb der acht Produktivordner sieht (a) nicht. Gebaut ist nur `git --no-optional-locks` an diesen drei Aufrufen; die Schwäche bleibt (Vorschlag A, Vergleich ohne git, nicht gebaut).

## Lage nach dem Auslegen

Soll in 0a vom steuernden Chat gefüllt (`[' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md']`); am Bau-HEAD wären es 4 Einträge gewesen: ` M docs/auftraege/AKTUELLER_AUFTRAG.md`, ` M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, ` M docs/projektfuehrung/UEBERGABE.md`, `?? docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md`.

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `5031cd0207234379d4a427de6734d42f6f814a0e`, genau die Einträge `[' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md']`, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb175_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "5031cd0207234379d4a427de6734d42f6f814a0e": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "5031cd0207234379d4a427de6734d42f6f814a0e": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (N Eintraege)` mit N = Zahl der Einträge im Soll. Anhänge holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb175_werkzeug.py 30b0d207aa24e4fafac1873253756fecd9f3031989f2cd81d0cecc04fbce49e2`; `test_haltedauer_kern.py b73adc87d57c764eb71ee00f725019dcedb70164599a20c7e9c77e6d065f8cba`; `Dateien 2`; sonst **ABBRUCH**.

**Fable 17.10.b ins Repo** (git-ignoriert ⇒ nicht im 0a-Soll; genau diese Zeilen):

```
cp data_sicherung/steuernder_chat_tmp/f17b/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md
cp data_sicherung/steuernder_chat_tmp/f17b/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md
```

**md5 vorher (Quelle) = nachher (Repo)** (genau dieser Befehl). Soll: `Pruefungen: 2, NEIN: 0`, letzte Zeile `rc 0`; sonst **ABBRUCH** (die zwei Kopien bleiben unverfolgt liegen; melden):

```bash
trading-env/bin/python3 -B "$TMPDIR/tb175_werkzeug.py" md5 > "$TMPDIR/tb175_md5.txt" 2>&1; echo "rc $?" >> "$TMPDIR/tb175_md5.txt"; tail -2 "$TMPDIR/tb175_md5.txt"
```

Dann genau diese Zeilen (die erste fügt die in 0a geprüften Pfade mit Namen hinzu, dazu die zwei Fable-Dateien), Commit `TB-175 Schritt 0: Fable 17.10.b (Anfrage, Antwort) und Stand des steuernden Chats vor TB-175 (Auftrag)`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
trading-env/bin/python3 -B -c "import subprocess, sys; z = [l[3:] for l in open(sys.argv[1], encoding='utf-8').read().split(chr(10)) if l]; print('git add', len(z)); raise SystemExit(subprocess.run(['git', 'add', '--'] + z).returncode)" "$TMPDIR/tb175_0a.txt"
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-175
cp "$TMPDIR/tb175_0a.txt" docs/belege/TB-175/0a_status.txt
cp "$TMPDIR/tb175_md5.txt" docs/belege/TB-175/0a_md5.txt
cp "$TMPDIR/tb175_werkzeug.py" docs/belege/TB-175/tb175_werkzeug.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py voraussetzung > docs/belege/TB-175/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (41 Prüfungen: fünf Programme der Gruppe je md5 = Bau, Test = Bau-Stand, BACKLOG Rang 1, Journal FK oder FL; Anfrage und Antwort 17.10.b verfolgt, gleich HEAD, md5 wie Soll; Registerblock R107; 66 da, 67 nicht; neun Marken-Orte eindeutig; Index-Kopf 0–66, Zeile 66, Pflegezeile TB-173, kein Abschnitt 18; Dialog-Index ohne 17b). **Abbruch in V:** im Arbeitsbaum liegt nur der unverfolgte Ordner `BEL`. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-175/abbruch.txt`, dann `git add` mit Namen für `docs/belege/TB-175/0a_status.txt`, `docs/belege/TB-175/tb175_werkzeug.py`, `docs/belege/TB-175/v_voraussetzung.txt`, `docs/belege/TB-175/abbruch.txt`, Commit `TB-175 Abbruch: V`, pushen, melden.

## Schritt R — Register 67 und neun Marken

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-175/v_voraussetzung.txt --probe > docs/belege/TB-175/r_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/r_probe.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-175/v_voraussetzung.txt > docs/belege/TB-175/r_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/r_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach genau diese `git add`, Commit `TB-175 R: Register 67 (Fable 17b, R107), neun Marken`, pushen ⇒ **⟨R⟩**:

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-175/0a_status.txt
git add docs/belege/TB-175/0a_md5.txt
git add docs/belege/TB-175/tb175_werkzeug.py
git add docs/belege/TB-175/v_voraussetzung.txt
git add docs/belege/TB-175/r_probe.txt
git add docs/belege/TB-175/r_eintrag.txt
git add docs/belege/TB-175/r_daten.json
```

## Schritt K — Kopien, Index, Dialog-Index (wie TB-173 Schritt K)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-175/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-175/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-175/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨R⟩ > docs/belege/TB-175/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-175/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_index.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py handfelder docs/belege/TB-175/k_handfelder.json > docs/belege/TB-175/k_handfelder.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_handfelder.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-175/k_handfelder.json > docs/belege/TB-175/k_dialog_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_dialog_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-175/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`. **Kein Abbruch** bei rc ≠ 0 in K: festhalten, die Dateien dieses Schritts nicht committen, nicht zurücksetzen, melden, weiter mit E. Entsteht eine weitere Teildatei: mit Namen anfügen, melden. Dann genau diese `git add`, Commit `TB-175 K: Registerkopie, Index, Dialog-Index`, pushen ⇒ **⟨K⟩**; danach `git status --porcelain` — Soll: keine Ausgabe:

```
git add docs/projektfuehrung/REGISTER_INDEX.md
git add docs/projektfuehrung/FABLE_DIALOG_INDEX.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil1.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil2.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil3.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil4.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil5.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil6.md
git add docs/projektfuehrung/register_kopie
git add docs/belege/TB-175/k_registerkopie.txt
git add docs/belege/TB-175/k_abschnitte.txt
git add docs/belege/TB-175/k_pruefen.txt
git add docs/belege/TB-175/k_index_zeilen.txt
git add docs/belege/TB-175/k_index.txt
git add docs/belege/TB-175/k_handfelder.txt
git add docs/belege/TB-175/k_dialog_index.txt
git add docs/belege/TB-175/k_dialog_pruefen.txt
git add docs/belege/TB-175/k_handfelder.json
```

## Schritt E — Teil 1: Prüfung 13 erneuern

```
trading-env/bin/python3 -B research/tb24_haltedauern/test_haltedauer_kern.py > docs/belege/TB-175/e_alt.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/e_alt.txt
cp "$TMPDIR/test_haltedauer_kern.py" research/tb24_haltedauern/test_haltedauer_kern.py
trading-env/bin/python3 -B research/tb24_haltedauern/test_haltedauer_kern.py > docs/belege/TB-175/e_neu.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/e_neu.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py gegenprobe > docs/belege/TB-175/e_gegenprobe.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/e_gegenprobe.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py nachher > docs/belege/TB-175/e_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/e_nachher.txt
```

Soll: `e_alt.txt` endet mit `rc 1` (alter Test, erwartet rot: genau das eine FEHLT der alten Prüfung 13); `e_neu.txt` endet mit `Alle Pruefungen bestanden.` und `rc 0`; `e_gegenprobe.txt` und `e_nachher.txt` enden mit `rc 0` (Gruppe unverändert, Test = Anhang, alt/neu vor 13 gleich, 13 mit 8 ok, drei Kopien wie Soll). **Abbruchweg E** (eine dieser Bedingungen nicht erfüllt; kein E-Commit):

```
trading-env/bin/python3 -B -c "import os, shutil, subprocess; t = 'research/tb24_haltedauern/test_haltedauer_kern.py'; b = 'docs/belege/TB-175/'; da = os.path.exists(t); shutil.copy(t, b + 'abbruch_test_haltedauer_kern.py') if da else None; open(t, 'wb').write(subprocess.run(['git', 'show', 'HEAD:' + t], capture_output=True, check=True).stdout); open(b + 'abbruch.txt', 'w').write('E: nicht wie Soll, siehe Belege\nneuer Test nach BEL kopiert, Test aus HEAD wiederhergestellt\n')"
trading-env/bin/python3 -B -c "import os, subprocess; f = ['docs/belege/TB-175/' + x for x in ('abbruch.txt', 'abbruch_test_haltedauer_kern.py', '0a_status.txt', '0a_md5.txt', 'tb175_werkzeug.py', 'v_voraussetzung.txt', 'r_probe.txt', 'r_eintrag.txt', 'r_daten.json', 'e_alt.txt', 'e_neu.txt', 'e_gegenprobe.txt', 'e_nachher.txt')]; d = [x for x in f if os.path.exists(x)]; print('git add', len(d), 'von', len(f)); raise SystemExit(subprocess.run(['git', 'add'] + d).returncode)"
git commit -q -m "TB-175 Abbruch: E"
git push -q origin main
git status --porcelain
```

Der Abbruchweg kopiert den neuen Test nach `BEL`, stellt den Test aus `HEAD` wieder her und fügt nur vorhandene Belege hinzu (schon committete bleiben unverändert). Soll danach: `git status --porcelain` ohne Ausgabe; scheitert der Push: melden, nicht wiederholen. Sonst (alle wie Soll) genau diese `git add`, Commit `TB-175 E: Pruefung 13 erneuert (Schreibziele je Aufruf; positionen_holen nur ueber --ziel und O_EXCL)`, pushen:

```
git add research/tb24_haltedauern/test_haltedauer_kern.py
git add docs/belege/TB-175/e_alt.txt
git add docs/belege/TB-175/e_neu.txt
git add docs/belege/TB-175/e_gegenprobe.txt
git add docs/belege/TB-175/e_nachher.txt
```


## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ backlog` hängt an Rang 1: Register 67 mit R107 (a) Zeilenschnitt der drei Aktien-Bots vor R44 als eigene Bauaufträge (Handelscode, 37.3), (c) Modus-Wache im Listen-Erzeuger vor R44, (d) Sammler zulässig, Kandidaten nicht vor der Zulassung; Voraussetzungen (b), (e) offen; D4-Befund und E2 als nächster Bauauftrag nach der Fable-Antwort; `grundlage.py` und `wf_kapital_dd/messung.py` Z. 120; dazu Teil 1. `WZ kennung`. Block nach `docs/belege/TB-175/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-175: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-175_pruefung13_leser_alle_trades.md` mit: Kopf mit Commits; Kurz; Schritt 0 (`0a_md5.txt` wörtlich); V wörtlich (letzte Zeilen); Register 67 (Zeile und neun Marken aus `r_daten.json`); K (je rc); E (die Zeilen der Prüfung 13 aus `e_alt.txt` und `e_neu.txt` wörtlich, Zahl der ok-Zeilen vor 13, `e_gegenprobe.txt` ja-Zeilen); Teil (a) (der Absatz oben, Entscheid B); Offen (Schwäche von (a); D4-Frage an den Verfahrensprüfer, danach E2; `grundlage.py`, `wf_kapital_dd`). Dann:

```
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py kennung > docs/belege/TB-175/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-175/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-175/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py journal docs/belege/TB-175/a_block.md --probe > docs/belege/TB-175/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-175/tb175_werkzeug.py journal docs/belege/TB-175/a_block.md > docs/belege/TB-175/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-175/a_journal.txt
```

Soll je `rc 0`. Genau diese `git add`, Commit `TB-175 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-175_pruefung13_leser_alle_trades.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-175/a_kennung.txt
git add docs/belege/TB-175/a_backlog_probe.txt
git add docs/belege/TB-175/a_backlog.txt
git add docs/belege/TB-175/a_block.md
git add docs/belege/TB-175/a_journal_probe.txt
git add docs/belege/TB-175/a_journal.txt
```

**F.**

```
git status --porcelain > "$TMPDIR/tb175_f.txt"
cp "$TMPDIR/tb175_f.txt" docs/belege/TB-175/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-175/f_numstat.txt
git add docs/belege/TB-175/f_porcelain.txt
git add docs/belege/TB-175/f_numstat.txt
git commit -q -m "TB-175 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; `f_numstat.txt`: Register Spalte 2 = `0`; unter `research/` genau `research/tb24_haltedauern/test_haltedauer_kern.py`; kein Pfad unter `strategies/`, `shared/`, `data/`, `config/`.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; `WZ md5` nicht `rc 0`; V nicht `rc 0`; `WZ register --probe`/`register` nicht `rc 0` (Abbruch nach `register` vor ⟨R⟩: Register bleibt geändert, nicht zurücksetzen, melden; Abbruch-Commit mit den vorhandenen Belegen wie in TB-173); **kein Abbruch** in K; E nicht wie Soll (dann Abbruchweg E, **kein E-Commit**); A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Zuerst legt die Sitzung die neue Antwort des Verfahrensprüfers mit ihrer Anfrage ins Repo und trägt ihren Regeltext R107 wortgleich ins Register ein, nur angehängt, mit neun Hinweisen an alten Stellen. In die Aufgabenliste kommen: die drei Aktien-Bots bekommen vor der Neuerzeugung einen Zeilenschnitt (eigene Code-Aufträge), der Listen-Erzeuger eine Wache für den Datenmodus, und ein reiner Sammler darf laufen, ein Kandidat mit Orders nicht vor seiner Zulassung. Danach:

Ein Selbsttest der Haltedauer-Untersuchung prüft, dass deren Programme nur in erlaubte Ordner schreiben. Seit das Holprogramm in einen beim Aufruf genannten Ordner schreibt (und nie überschreibt), meldete der Test einen Fehler, den es nicht gibt. Die neue Prüfung schaut jeden einzelnen Schreibbefehl an: allgemein muss er in den eigenen Ergebnis- oder Datenordner gehen, beim Holprogramm nur in den Pflicht-Zielordner und nur über die eine Schreibstelle, die nie überschreibt. Damit die Prüfung nicht bloss grün aussieht, wird sie an verfälschten Kopien rot.

## Anhänge

### Anhang A — Werkzeug

<!-- DATEI tb175_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-175 Werkzeug (Anhang A): Pruefung 13 in test_haltedauer_kern.py erneuern - Fable 17b ins Register (Abschnitt 67, R107 zeichengleich, neun Marken, 67.2), Index, Handfelder; Voraussetzungen, Gegenprobe an Kopien, Nachher-Pruefung, Kennung, BACKLOG, Journal.
Python 3.9, Aufruf aus der Repo-Wurzel. Nur gegenprobe importiert den Test (numpy/pandas). --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | nachher2 | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | gegenprobe | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, sys
P = "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-175/"
GR = "research/tb24_haltedauern/"
TEST, TSHA, BASIS = GR + "test_haltedauer_kern.py", "b73adc87d57c764eb71ee00f725019dcedb70164599a20c7e9c77e6d065f8cba", "807d278e60a953cac40a836d28d13c96"
CODE = { "research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/tb24_haltedauern/auswertung.py": "c15e6375520e1aeccc41ce152ca3b870", "research/tb24_haltedauern/haltedauer_kern.py": "60942de99b323fa472ae25478a5a6836", "research/tb24_haltedauern/live_haltedauern.py": "7d21a66cd3173a99adff2c9c1346c815", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd" }
ALT13 = "  FEHLT wer schreibt, schreibt in den eigenen Ordner (aussen vor: ['positionen_holen.py'])"
KOPF13, N13 = "13. Wache: die Untersuchung fasst nichts ausserhalb ihres Ordners an", 8
RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "Gruppe unveraendert: %s md5 %s" % (f, m[:12]))
def beleg(n): return lies(BEL + n).rstrip("\n").split("\n") if os.path.exists(BEL + n) else [""]
def voraussetzung():
    code_gleich(); p(md5f(TEST) == BASIS, "Test vor E = Bau-Stand (md5 %s, Pruefung 13 alt)" % BASIS[:12])
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-175" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-175")
    k = kennungen(); p(max(k) in ("FK", "FL"), "Journal: hoechste %s (FK am Bau-HEAD)" % max(k))
    voraussetzung_reg(); ende()
def gegenprobe():
    """An Kopien der Gruppe im Temp-Ordner: unveraendert gruen; mit Voreinstellung fuer --ziel bzw. open(..., "w") statt _schreibe_einmal rot."""
    import importlib.util, shutil, tempfile
    sys.dont_write_bytecode = True; sys.path.insert(0, os.path.abspath(GR)); basis = os.environ.get("TMPDIR") or tempfile.gettempdir()
    spec = importlib.util.spec_from_file_location("tb175_test13", os.path.abspath(TEST)); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
    t._ARBEITSBAUM_ZU_BEGINN = t._arbeitsbaum(); t.LEISE = True
    for fall, alt, neu in (("kontrolle", None, None), ("voreinstellung", '_aufruf.add_argument("--ziel", required=True,', '_aufruf.add_argument("--ziel", required=True, default=".",'),
                           ("open_w", 'hashes[f"{BOT}_alle_trades.csv"] = _schreibe_einmal(\n        f"{BOT}_alle_trades.csv", alle.to_csv(index=False))',
                            'open(os.path.join(ZIEL_DIR, f"{BOT}_alle_trades.csv"), "w").write(\n        alle.to_csv(index=False))')):
        o = tempfile.mkdtemp(prefix="tb175_%s_" % fall, dir=basis); n = 1
        for name in sorted(os.listdir(GR)):
            if name.endswith(".py") and not name.startswith("test_"): shutil.copy(GR + name, o)
        if alt:
            q = lies(o + "/positionen_holen.py"); n = q.count(alt); schreibe(o + "/positionen_holen.py", q.replace(alt, neu))
        del t.FEHLER[:]; t.wache_repo_unveraendert(o); fe = list(t.FEHLER)
        if alt is None: p(fe == [], "Kopie %s (%s): Pruefung 13 gruen, FEHLT %d" % (fall, o, len(fe)))
        else: p(n == 1 and any(f.startswith("wer schreibt") and "positionen_holen.py" in f for f in fe), "Kopie %s: Ersetzung %d-mal, Pruefung 13 rot: %s" % (fall, n, [f[:160] for f in fe][:3]))
    ende()
def nachher():
    code_gleich(); p(sha(TEST) == TSHA, "Test im Repo = Anhang (sha256 %s)" % TSHA[:12])
    a, e, g = beleg("e_alt.txt"), beleg("e_neu.txt"), beleg("e_gegenprobe.txt")
    p(a[-1] == "rc 1" and [l for l in a if l.startswith("  FEHLT")] == [ALT13], "e_alt.txt: rc 1, einziges FEHLT = alte Pruefung 13 an positionen_holen.py")
    p(e[-1] == "rc 0" and len(e) > 1 and e[-2] == "Alle Pruefungen bestanden." and not [l for l in e if "FEHLT" in l], "e_neu.txt: 'Alle Pruefungen bestanden.', rc 0, kein FEHLT")
    vor = lambda z: [l for l in z[:z.index(KOPF13)] if l.startswith("  ok")] if KOPF13 in z else None
    va, ve = vor(a), vor(e)
    p(va is not None and va == ve and len(va) > 0, "uebrige Pruefungen (vor 13) unveraendert gruen: alt %s, neu %s ok-Zeilen, gleich" % (len(va or []), len(ve or [])))
    s13 = [l for l in e[e.index(KOPF13) + 1:] if l.startswith("  ok")] if KOPF13 in e else []
    p(len(s13) == N13 and sum("Gegenprobe 13:" in l for l in s13) == N13 - 2 and any("(aussen vor: keine)" in l for l in s13), "e_neu.txt Pruefung 13: %d ok (Arbeitsbaum, Schreibziele, %d Gegenproben)" % (len(s13), N13 - 2))
    p(g[-1] == "rc 0" and sum(l.startswith("ja    Kopie") for l in g) == 3, "e_gegenprobe.txt: 3 Kopien wie Soll, rc 0")
    ende()
BL_TEXT = (" · **Register 67 (Fable 17b, R107) mit TB-175 (%s, Journal %s)**: R107 (a) **Zeilenschnitt** am Horizontbeginn vor der Indikatorbildung bei `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` **vor R44**, je Bot ein eigener Bauauftrag (Handelscode, Bauart E-6, 37.3 mit Hashes je Datei, eine Freigabe je Auftrag, Abnahme mit Gegenprobe 40.7 auf dem Test-Snapshot); R107 (c) **Modus-Wache im Listen-Erzeuger vor R44** (vor dem ersten Lesen Selektionsmodus gesetzt und DATA_DIR = Snapshot-Wurzel, sonst 2; Probe nach R86 (d) mit Gegenprobe); R107 (d) **Sammler zulässig** unter den Bedingungen aus R107 (d), **Kandidaten mit Orders (S-B1, KI-Bot) laufen nicht vor ihrer Zulassung**, auch nicht als Papierpfad; Voraussetzungen R107 (b) (Teilmessung, zur Kenntnis an den Verfahrensprüfer) und (e) gemessen (67.2 (a), (b)); **`research/mtm_drawdown/grundlage.py`** liest die TB-24-Liste und das Startkapital aus der Meta (Z. 189–198) gegen R107 (e) und 37.5 (2): umstellen auf Rekonstruktion nach R97 (b) (Vorbild `research/wf_kapital_dd/messung.py`) mit Startkapital aus Register 29.3 (`messung.py`, `test_mtm_kern.py` mit); Befund `research/wf_kapital_dd/messung.py` Z. 120: Startkapital aus `es.STARTING_CAPITAL` statt aus Register 29.3 → zur nächsten Fable-Anfrage; **nächster Bauauftrag nach der Fable-Antwort zu D4: E2** — `research/tb24_haltedauern/auswertung.py` und `research/faltenplan_neun/embargo_neun.py` auf alle gefundenen Trades (R107 (e); gebaut und an einer Kopie geprobt, nicht im Repo); über alle gefundenen Trades ergäbe D4 (`test_faltenplan_neun.py`) für t3_supertrend P90 8,6833 statt 9,5000, Embargo 12 statt 13 (registrierte Herleitung ändert sich), die übrigen acht Bots gleich; Frage an den Verfahrensprüfer · **TB-175 Teil 1: Prüfung 13 in `" + TEST + "` erneuert** (seit 46e3ed0/TB-98 rot, jetzt grün: je Schreibaufruf ein erlaubter Ort, "
    "ERGEBNIS_DIR/DATEN_DIR aus `_DIR`; `positionen_holen.py`: ZIEL_DIR nur aus Pflicht-`--ziel` ohne Voreinstellung, Schreiben nur über `_schreibe_einmal` mit O_EXCL; "
    "sechs Gegenproben im Test, an Kopien Voreinstellung und `open(..., \"w\")` rot; übrige Prüfungen unverändert grün); Teil (a): git-Aufrufe im Test mit `--no-optional-locks` |")
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-175" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-175"):
        z[a[0]] = z[a[0]][:-2] + BL_TEXT % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-175: " % neu), "Kopfzeile ## %s — TB-175: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
# --- Registerauftrag Fable 17b (R107, Abschnitt 67, neun Marken) - Bauart TB-173 ---
import json, subprocess
REG, IDX, DI = "docs/VORREGISTRIERUNG_neuselektion.md", P + "REGISTER_INDEX.md", P + "FABLE_DIALOG_INDEX.md"
AUF, QU = "docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md", "data_sicherung/steuernder_chat_tmp/f17b/"
FA = P + "FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md"; FQ = P + "FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md"
MD5F = {"docs/projektfuehrung/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md": "d13e691973d3b98528b72c67ac000eb9", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md": "af2c861a88a083dd7652dcbc07650d8f"}
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R107)"
TITEL = "## 67. Fable 17b — Registerblock R107 (TB-175)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | zg | ende | Absatzanfang, Kopf der Marke, Zusatz) - R107 (f)
MARKEN = [("62.3", "### 62.3 ", "quelle", "62.3 R102 ERGÄNZT und BERICHTIGT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (a): ERGÄNZT zu (d), BERICHTIGT zu (c) („lies“)"),
          ("55.4", "### 55.4 ", "zg", "55.4 R81 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (a)"),
          ("66.1", "### 66.1 ", "quelle", "66.1 R106 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (b)"),
          ("64.1", "### 64.1 ", "**Abnahme nach R98 (d)**", "64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (b)"),
          ("56.3", "### 56.3 ", "zg", "56.3 R86 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkte (c) und (e)"),
          ("57.3", "### 57.3 ", "quelle", "57.3 R92 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (c): die Voraussetzung in (c) ist gemessen erfüllt"),
          ("16.4", "### 16.4 ", "ende", "16.4 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (d)"),
          ("16.8", "### 16.8 ", "ende", "16.8 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (d)"),
          ("58.4", "### 58.4 ", "quelle", "58.4 R97 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (e)")]
CODE_E2 = {"research/faltenplan_neun/embargo_neun.py": "b93af14604112c427ab1a3f1606fccc6", "research/mtm_drawdown/grundlage.py": "81cf1c93243a8248b96cf072e07fc289", "research/mtm_drawdown/messung.py": "00eb23079f1b92532f48f099f74dbe2f", "research/mtm_drawdown/test_mtm_kern.py": "80f1511a18d26a61537748c2739d0d79", "research/wf_kapital_dd/messung.py": "94c091f4c4e13ff4aa2e867dd4fd4fa5"}
NEU_E2 = {"research/tb24_haltedauern/auswertung.py": "fbafe5291c305bb64fa27a216100c006bd6c1c912dc981c69583cfcd70c2eb8d", "research/faltenplan_neun/embargo_neun.py": "ad11bd0ca33d28ca179101cd94f262ca42ba46e9507010578279577b1f4fa58f"}
PROBE_E2, PSHA = BEL + "tb175_probe_leser.py", "adbdd1451eb4270d1e74b4ce30d2914e5511faec3bcfbbbe9463c30159099297"
FUND = {"abn": ["docs/belege/TB-169/e_abnahme.txt", 85, 85, ["ja    t3_supertrend: 3b spaetes Symbol CCC gleich mit/ohne Schranke · 16/16"]], "tle_tag": ["research/tb24_haltedauern/test_listen_erzeuger.py", 159, 163, ["    c0 = b[b[\"symbol\"] == \"CCC\"]", "    if len(c0):", "        r = lauf(bot, seed, False, \"\", json.dumps({\"CCC\": str(c0[\"entry_time\"].min().date())})); x = tab(r[\"liste\"])", "        y = x[x[\"symbol\"] == \"CCC\"].reset_index(drop=True)[[\"entry_time\", \"exit_time\"]] if x is not None else None", "        pruefe(bot + \": 3b spaetes Symbol CCC gleich mit/ohne Schranke\", y is not None and y.equals(c0.reset_index(drop=True)[[\"entry_time\", \"exit_time\"]]), \"%s/%d\" % (None if y is None else len(y), len(c0)))"]], "tle_modus": ["research/tb24_haltedauern/test_listen_erzeuger.py", 161, 161, ["        r = lauf(bot, seed, False, \"\", json.dumps({\"CCC\": str(c0[\"entry_time\"].min().date())})); x = tab(r[\"liste\"])"]], "tle_wachen": ["research/tb24_haltedauern/test_listen_erzeuger.py", 85, 86, ["    if \"wache1_aus\" in modus: ph.wache_zeilen = lambda a: None", "    if \"wachen_aus\" in modus: ph.wache_zeilen = lambda a: None; ph.wache_trades = lambda tr, h: None"]], "tle_aus": ["research/tb24_haltedauern/test_listen_erzeuger.py", 87, 88, ["    if \"schranke_aus\" in modus:", "        alt = ph.basis.hole_trades; ph.basis.hole_trades = lambda es, a, h=None: alt(es, a)"]], "tle_p8": ["research/tb24_haltedauern/test_listen_erzeuger.py", 177, 177, ["    pruefe(bot + \": 8 nur Dateien des Test-Snapshots gelesen (%d read_csv)\" % (A[\"gelesen\"] + B[\"gelesen\"]), not A[\"fremd\"] and not B[\"fremd\"] and A[\"gelesen\"] > 0, (A[\"fremd\"] + B[\"fremd\"])[:2])"]], "aus_lade": ["research/tb24_haltedauern/auswertung.py", 69, 71, ["def lade(bot: str, nur_ausgefuehrt: bool = True) -> pd.DataFrame:", "    if nur_ausgefuehrt:", "        pfad = os.path.join(DATEN_DIR, f\"{bot}_positionen.csv\")"]], "emb": ["research/faltenplan_neun/embargo_neun.py", 232, 232, ["    pfad = os.path.join(basis or BASE_DIR, TB24_DATEN, f\"{bot}_positionen.csv\")"]], "gl_meta": ["research/mtm_drawdown/grundlage.py", 189, 198, ["        \"startkapital_meta\": meta.get(\"startkapital\"),", "        \"allocation_pct_meta\": meta.get(\"allocation_pct\"),", "        \"positionslimit_meta\": meta.get(\"max_concurrent_positions\"),", "        \"abgleich_exposure_messung_identisch\": (meta.get(\"abgleich_exposure_messung\") or {}).get(\"identisch\"),", "    }", "", "    # Kette der Kapitalstaende - schliesst sie, ist die Liste die einer", "    # Kapitalsimulation und die Kurvenreihenfolge rekonstruierbar.", "    try:", "        ereignisse = mtm_kern.ereignisreihenfolge(pos, float(meta[\"startkapital\"]))"]], "wf": ["research/wf_kapital_dd/messung.py", 120, 120, ["    startkapital = float(es.STARTING_CAPITAL)"]], "mg": ["research/vorregistrierung/messgroessen.py", 230, 231, ["    pfad = os.path.join(BASE_DIR, \"research\", \"tb24_haltedauern\",", "                        \"ergebnisse\", \"haltedauern_je_bot.csv\")"]]}
D4 = {"p90a": "8,6833", "p90p": "9,5000", "emba": 12, "embp": 13}
def fz(k): f, a, e, _t = FUND[k]; return "Z. %d" % a if a == e else "Z. %d–%d" % (a, e)
def fund_ok():
    for k, (f, a, e, t) in sorted(FUND.items()):
        z = lies(f).split("\n") if os.path.exists(f) else []; p(z[a - 1:e] == t, "Fundstelle %s: %s %s unveraendert (Bau-Stand)" % (k, f, fz(k)))
def nachher2():
    for f, m in sorted(CODE.items()):
        if not f.endswith("auswertung.py"): p(md5f(f) == m, "E2 unveraendert: %s md5 %s" % (f, m[:12]))
    for f, m in sorted(CODE_E2.items()):
        if not f.endswith("embargo_neun.py"): p(md5f(f) == m, "E2 unveraendert (Messung nach R94 (b), nicht Teil von E2): %s md5 %s" % (f, m[:12]))
    for f, s in sorted(NEU_E2.items()): p(sha(f) == s, "E2 umgestellt: %s = Anhang (sha256 %s)" % (f, s[:12]))
    p(sha(PROBE_E2) == PSHA and sha(TEST) == TSHA, "Probe E2 = Anhang E, Test = Anhang B")
    pr, te = beleg("e2_probe.txt"), beleg("e2_test.txt")
    p(pr[-2:] == ["Ergebnis: 9 von 9 bestanden", "rc 0"], "e2_probe.txt: 9 von 9, rc 0")
    p(te[-2:] == ["Alle Pruefungen bestanden.", "rc 0"] and any("Gegenprobe 13: auswertung.py schreibt neben ERGEBNIS_DIR -> auswertung.py faellt auf" in l for l in te), "e2_test.txt: Test am neuen auswertung.py gruen, Gegenprobe 6 trifft")
    ende()
OHNE = "28.6, 51.2 (R57), 26.2, 16.9, 62.2 (R101), 55.1 (R78), 56.1 (R84), 48.13 (R45), 57.1 (R90), 61.1 (R98), 58.1 (R94), 58.2 (R95), 60.1, 63.1, 24.3, 17.1, 17.2, 29.3, 37.3, 37.5, 40.6, 62.5, 66.2, Abschnitt 9, 10, 41, 42"
def info(t): OUT.append("info  " + t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def block():
    """((R-Zeile, Quellenzeile), Z. Zaun auf, Z. Zaun zu) oder None."""
    z = lies(FA if os.path.exists(FA) else QU + os.path.basename(FA)).split("\n")   # vor Schritt 0 (nur am Bau): die Quelle
    if z.count(KOPF_A) != 1: return None
    a = z.index(KOPF_A) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [z[i] for i in range(a + 1, e) if z[i]]; soll = ["R107 — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for l, s in zip(b, soll)] != soll: return None
    return (b[0], b[1]), a + 1, e + 1
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m):
    """Index der Einfuegestelle (nach dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any("R107" in z[i] for i in range(a, e)): return None
    if m[2] == "zg": k = [i for i in range(a, e) if z[i] == ZG][-1:]
    elif m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    elif m[2] == "ende":
        j = e - 1
        while j > a and z[j] in ("", "---"): j -= 1
        k = [j] if j > a else []
    else:
        k = [i for i in range(a, e) if z[i].startswith(m[2])]
        if len(k) == 1:
            while k[0] + 3 < e and z[k[0] + 1] == "" and z[k[0] + 2].startswith("> ⭐ ") and z[k[0] + 3] == ZG: k[0] += 3
    return k[0] + 1 if len(k) == 1 else None
def markenzeilen(m, datum): return ["", "> ⭐ **%s** (%s, TB-175, %s)." % (m[3], m[4], datum), ZG]
def stand_kopf():
    z = lies(IDX).split("\n"); return z, [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def md5cmd():
    for f in (FA, FQ): p(md5f(QU + os.path.basename(f)) == MD5F[f] and md5f(f) == MD5F[f], "md5 vorher %s = nachher %s = %s" % (QU + os.path.basename(f), f, MD5F[f]))
    ende()
def voraussetzung_reg():
    for f in (FA, FQ): p(verfolgt_gleich(f) and md5f(f) == MD5F[f], "R56 (b)/S0-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5F[f]))
    b = block(); p(b is not None, "Registerblock 17b: genau R107 und Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[1], b[2]) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 66. ") for l in z) == 1 and not any(l.startswith("## 67. ") for l in z) and not re.search(r"\bR107\b", reg), "Register: 66 da, 67 nicht; R107 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for m in MARKEN: i = einfuege(z, m); p(i is not None, "Ort %s: Einfuegestelle nach Z. %s eindeutig, R107 dort noch nicht genannt" % (m[0], i if i else "?"))
    zi, k = stand_kopf(); p(len(k) == 1 and "Abschnitte 0–66" in zi[k[0]], "Index-Kopf Z. %s nennt 0–66" % (k[0] + 1 if k else "?"))
    p(sum(l.startswith("| 66 aus 17a |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-173 (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and not any(l.startswith("## 18. ") for l in zi), "Index: Zeile 66, Pflegezeile TB-173, Pflege-Anker je genau einmal; kein Abschnitt 18")
    p(not any(l.startswith("| 17b |") for l in lies(DI).split("\n")), "Dialog-Index: 17b noch nicht")
    for f, m in sorted(CODE_E2.items()): p(md5f(f) == m, "E2-Ausgang: %s md5 %s" % (f, m[:12]))
    fund_ok()
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    b = block(); p(b is not None and md5f(FA) == MD5F[FA], "Quelle md5 %s, Registerblock R107" % MD5F[FA])
    p(not any(l.startswith("## 67. ") for l in z) and z[-1] == "" and z[-2] != "", "67 noch nicht im Register; endet mit einer Leerzeile")
    einf = [(einfuege(z, m), m) for m in MARKEN]; p(all(i is not None for i, _ in einf) and len(set(i for i, _ in einf)) == len(MARKEN), "9 Einfuegestellen eindeutig")
    k = karte(); p(k is not None, "Karte TB-175 gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    (r, q), za, ze = b
    kopf = ("Reines Eintragen von Registertext, Bauart wie 66. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R107)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.b (`%s`, seit `%s`) und die Übergabe 17.10.a (zweite Anfrage im selben Chat). Marken nach R107 (f). "
            "Karte des Betreibers (Auftrag TB-175, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-175.") % (FA, MD5F[FA], format(os.path.getsize(FA), ",").replace(",", " "), za, ze, s0, FQ, s0, k, datum)
    kette = ("**Kette:** Marken nach R107 (f): 62.3 (R102), Unterpunkt (a), ergänzt und berichtigt; 55.4 (R81), Unterpunkt (a); 66.1 (R106) und 64.1, Absatz „Abnahme nach R98 (d)“, Unterpunkt (b); "
             "56.3 (R86), Unterpunkte (c) und (e); 57.3 (R92), Unterpunkt (c); 16.4 und 16.8, Unterpunkt (d); 58.4 (R97), Unterpunkt (e). Ohne Marke: " + OHNE + ". "
             "Indexzeilen 48.20 (R52) und 54.3 (R76): sechzehn Fälle (R107 (f)). Voraussetzungen in (b) und (e) gemessen: 67.2 (a) (Teilmessung) und (b); Umstellung der Leser: nach der Frage zu D4 (BACKLOG Rang 1).")
    neu = ["", TITEL, "", kopf, "", "### 67.1 " + titel(r), "", "> " + r, "> " + q, "", kette, ""]
    neu += ["### 67.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-175), Zeilen wörtlich:" % beleg, ""] + ["    " + l for l in vb] + ["",
        ("(a) R107 (b), Voraussetzung (nur das Ob), gemessen durch Lesen am Stand `%s`: TB-169 3b führt t3_supertrend — `%s` %s: „%s“; `%s` %s (Tag des späten Symbols = frühester Einstieg, alle alten Einstiege am Tag oder später). "
         "Wachen eingeschaltet: Modus leer (%s), Ersetzung der Wachen nur in „wache1_aus“/„wachen_aus“ (%s). **Einschränkung:** verglichen wird mit Lauf B (Schranke am natürlichen Tag), nicht mit ausgeschalteter Schranke (%s), "
         "und Prüfung 8 (fremde Lesepfade, %s) prüft den 3b-Lauf nicht. **Teilmessung**, zur Kenntnis an den Verfahrensprüfer.") % (s0, FUND["abn"][0], fz("abn"), FUND["abn"][3][0].strip(), FUND["tle_tag"][0], fz("tle_tag"), fz("tle_modus"), fz("tle_wachen"), fz("tle_aus"), fz("tle_p8")), "",
        ("(b) R107 (e), Voraussetzung (nur das Wie), gemessen durch Lesen am Stand `%s`: die drei Leser aus R107 (e) — `%s` %s (`<bot>_positionen.csv`; 41.2 B6/B7, Quelle von B3), `%s` %s (41.3 C2, P95 t3_supertrend) und `%s` mit `research/mtm_drawdown/messung.py` (TB-24-Liste, Startkapital aus der Meta, %s) — "
         "und dazu `%s` (Rekonstruktion; Startkapital %s aus `es.STARTING_CAPITAL`) lasen ausgeführte Positionen; 41.2 B3, B6/B7 und 41.3 C2 rechneten nicht aus gefundenen Trades (B3 über `%s` %s aus `haltedauern_je_bot.csv`). Noch nicht umgestellt. "
         "Befund vor der Umstellung: über alle gefundenen Trades ergäbe D4 (`research/faltenplan_neun/test_faltenplan_neun.py`) für t3_supertrend P90 %s statt %s, Embargo %d statt %d; die übrigen acht Bots gleich (am Bau auf den abgelegten Listen gerechnet, der Test lief nicht). Frage an den Verfahrensprüfer.")
         % (s0, FUND["aus_lade"][0], fz("aus_lade"), FUND["emb"][0], fz("emb"), FUND["gl_meta"][0], fz("gl_meta"), FUND["wf"][0], fz("wf"), FUND["mg"][0], fz("mg"), D4["p90a"], D4["p90p"], D4["emba"], D4["embp"]), "",
        "(c) Zählung: R107 (a) nennt den sechzehnten Fall; die Indexzeilen an 48.20 (R52) und 54.3 (R76) stehen nur, wie R107 (f) sagt (Index, ohne Marke).", "",
        "(d) R56 (b): Anfrage und Antwort 17.10.b liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `docs/belege/TB-175/0a_md5.txt`)." % (s0, QU), ""]
    if probe: print("\n".join(neu)); ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m, datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s**" % m[3])] for m in MARKEN}
    json.dump({"marken": [[m[0], m[3], (mz[m[0]] or [0])[0]] for m in MARKEN], "abschnitt_67": r2.index(TITEL) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: 9 Marken Z. %s; Abschnitt 67 Z. %d" % (sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "R107 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al):] == neu, "append-only bis auf die neun Marken (je Leerzeile, Marke, Zeichengleich-Zeile)")
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 67. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) == 9 and all(m[2] for m in mk), "Abschnitt 67 in genau einer Teildatei: T%s; 9 Marken mit Zeile" % teil); T = str(teil[0]) if teil else "?"
    z, k = stand_kopf(); rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–66" in z[k[0]], "Kopf genau einmal, nennt 0–66"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–66", "Abschnitte 0–67")
    i = [j for j, l in enumerate(z) if l.startswith("| 66 aus 17a |")]
    if p(len(i) == 1, "Zeile 66 genau einmal"): z.insert(i[0] + 1, "| 67 aus 17b | %s | R107 (67.1); 67.2 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 18. Die Marken aus Fable 17b (TB-175)", "", "Alle 9 Marken, die TB-175 nach R107 (f) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-175/r_daten.json`.", "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, T) for o, kp, n in sorted(mk, key=lambda m: m[2])] + ["",
           "### Indexzeilen aus Fable 17b", "",
           "- **48.20 (R52):** Zählung → R107 (a) (67.1): sechzehnter Fall („Aussage über das Repo ohne Kennzeichnung, die nicht trifft (R76 (e))“); sechzehn Fälle (R107 (f)). Ohne Marke (R107 (f)). Der Index ist kein Registertext.",
           "- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R107 (a) (67.1): sechzehnter Fall. Ohne Marke (R107 (f)). Der Index ist kein Registertext.", ""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 18. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 18"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-173 (")]
    if p(len(j) == 1, "Pflegezeile TB-173 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-173 (", "In TB-173 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-175 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-175 (`index`); 67 (R107) kommt zu T%s; neuer Abschnitt 18 (9 Marken, Indexzeilen 48.20 und 54.3)." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"17b": {"frage": lies(FQ).split("\n")[0].split(" — ", 1)[-1].strip(),
                       "entscheidung": "(a) einverstanden: Zeilenschnitt je Bot vor R44, „lies“ zu R102 (c); (b) einverstanden mit Voraussetzung (t3 geschlossen); (c) Modus-Wache im Erzeuger Pflicht; (d) Sammler ja, Kandidat mit Orders vor der Zulassung nein; (e) Leser auf gefundenen Trades, ausgeführte Positionen nur nach R45/R84 (e) oder R97 (b) (R107)",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17b geschrieben: %s" % ziel)

if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["md5"]: md5cmd()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["gegenprobe"]: gegenprobe()
    elif a == ["nachher"]: nachher()
    elif a == ["nachher2"]: nachher2()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

### Anhang B — Test (vollständig, ersetzt `research/tb24_haltedauern/test_haltedauer_kern.py`)

<!-- DATEI test_haltedauer_kern.py -->
````python
"""
Selbsttests des Rechenkerns - mit Gegenproben UND Mutationsproben
==============================================================================
Nach Prinzip 12 des Uebergabeprotokolls ("eine gruene Pruefung ist erst dann
etwas wert, wenn belegt ist, dass sie auch rot werden kann") steht hier
zweierlei:

* **Gegenproben** - zu jeder Behauptung ein zweiter Fall, in dem dieselbe
  Pruefung anschlagen MUSS: zur getrennten Verteilung die ueberlappende, zum
  Treffer am Fensterrand der Nicht-Treffer einen Tag daneben, zur Ueberlappung
  im selben Titel die Ueberlappung ohne gemeinsamen Titel.
* **Mutationsproben** - der Quelltext des Rechenkerns wird gezielt an EINER
  Stelle verfaelscht, das veraenderte Modul frisch geladen und dieselbe
  Pruefungsreihe darauf laufen gelassen. Sie MUSS dann fehlschlagen. Damit ist
  belegt, dass die Pruefungen die jeweilige Rechenregel wirklich festhalten
  und nicht bloss daneben herlaufen. Jede Textersetzung wird vorher darauf
  geprueft, dass sie genau einmal zutrifft - eine Mutation, die nichts
  veraendert, wuerde sonst als bestandene Probe durchgehen.

Alle Erwartungswerte sind von Hand nachrechenbar konstruiert; keiner ist aus
einem Lauf des Kerns uebernommen und wiedererkannt.

    python3 test_haltedauer_kern.py
"""

import os
import subprocess
import sys
import types

import numpy as np
import pandas as pd

import haltedauer_kern

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
KERN_PFAD = os.path.join(_DIR, "haltedauer_kern.py")

FEHLER = []
LEISE = False
GEZAEHLT = [0]


def pruefe(bedingung, text):
    GEZAEHLT[0] += 1
    if bedingung:
        if not LEISE:
            print(f"  ok    {text}")
    else:
        if not LEISE:
            print(f"  FEHLT {text}")
        FEHLER.append(text)


def pos(zeilen):
    """zeilen: (symbol, entry, exit, result). pnl_pct/kerzen werden nicht
    gebraucht und deshalb nicht erfunden."""
    df = pd.DataFrame(zeilen, columns=["symbol", "entry_time", "exit_time", "result"])
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])
    return df


def tag(n, basis="2020-01-01"):
    return str((pd.Timestamp(basis) + pd.Timedelta(days=n)).date())


# ===========================================================================
# Die Pruefungsreihe. Sie bekommt das zu pruefende Modul uebergeben, damit
# dieselbe Reihe auch auf ein mutiertes Modul angewandt werden kann.
# ===========================================================================

def pruefungsreihe(k):

    # -- 1. Haltedauer in Kalendertagen -----------------------------------
    p = pos([("A", "2020-01-01", "2020-01-04", "time_exit")])
    pruefe(float(k.haltedauer_tage(p).iloc[0]) == 3.0,
           "1.1 Einstieg 01., Ausstieg 04. -> 3 Kalendertage")

    p_stunden = pos([("A", "2020-01-01 07:00", "2020-01-03 11:00", "time_exit")])
    pruefe(abs(float(k.haltedauer_tage(p_stunden).iloc[0]) - (2 + 4 / 24)) < 1e-9,
           "1.2 Stundenkerzen: 2 Tage 4 Stunden -> 2,1667 Tage (nicht 2, nicht 3)")

    p_null = pos([("A", "2020-01-01", "2020-01-01", "stop_loss")])
    pruefe(float(k.haltedauer_tage(p_null).iloc[0]) == 0.0,
           "1.3 Gegenprobe: Ein- und Ausstieg am selben Tag -> 0 Tage")

    # -- 2. Verteilungs-Kennzahlen ---------------------------------------
    kz = k.kennzahlen(list(range(1, 11)))
    pruefe(kz["n"] == 10 and kz["median"] == 5.5 and kz["mittel"] == 5.5,
           "2.1 n=10, Median 5,5, Mittel 5,5 bei 1..10")
    pruefe(kz["q1"] == 3.25 and kz["q3"] == 7.75,
           "2.2 Quartile 3,25 / 7,75 (lineare Interpolation)")
    pruefe(abs(kz["p10"] - 1.9) < 1e-9 and abs(kz["p90"] - 9.1) < 1e-9,
           "2.3 10./90. Perzentil 1,9 / 9,1")

    schief = k.kennzahlen([1, 1, 1, 1, 1, 1, 1, 1, 1, 100])
    pruefe(schief["median"] == 1.0 and schief["mittel"] == 10.9,
           "2.4 Gegenprobe: ein Ausreisser zieht den Mittelwert (10,9), nicht den Median (1,0)")
    pruefe(k.kennzahlen([])["n"] == 0, "2.5 leere Reihe -> n = 0, kein Absturz")

    # -- 3. Histogramm: links geschlossen, rechts offen -------------------
    h = k.histogramm([0.0, 2.9, 3.0, 9.99, 10.0, 100.0], [0, 3, 10])
    pruefe(list(h) == [2, 2, 2],
           "3.1 Klassen [0,3) [3,10) [10,inf) zaehlen 2 / 2 / 2")
    h_rand = k.histogramm([3.0], [0, 3, 10])
    pruefe(list(h_rand) == [0, 1, 0],
           "3.2 Gegenprobe Klassengrenze: 3,0 gehoert in [3,10), nicht in [0,3)")

    # -- 4. Zweigipfligkeit ueber die Ausstiegsart ------------------------
    getrennt = pos([("A", tag(i), tag(i + 1), "stop_loss") for i in range(10)]
                    + [("A", tag(i), tag(i + 10), "time_exit") for i in range(10)])
    z = k.zweigipfligkeit(getrennt)
    pruefe(z["zwei_gruppen"] is True,
           "4.1 Stop nach 1 Tag gegen Zeitausstieg nach 10 Tagen -> zwei Gruppen")

    vermischt = pos([("A", tag(i), tag(i + 1 + (i % 9)), "stop_loss") for i in range(10)]
                     + [("A", tag(i), tag(i + 1 + (i % 9)), "time_exit") for i in range(10)])
    z2 = k.zweigipfligkeit(vermischt)
    pruefe(z2["zwei_gruppen"] is False,
           "4.2 Gegenprobe: gleiche Streuung in beiden Arten -> KEINE zwei Gruppen")

    eine_art = pos([("A", tag(i), tag(i + 3), "time_exit") for i in range(10)])
    pruefe(k.zweigipfligkeit(eine_art)["zwei_gruppen"] is False,
           "4.3 nur eine Ausstiegsart -> keine zwei Gruppen (und kein Absturz)")

    # -- 5. Positionstage: Ein- und Ausstiegstag eingeschlossen -----------
    drei = pos([("X", "2020-01-01", "2020-01-03", "time_exit")])
    pruefe(len(k.positionstage(drei)) == 3,
           "5.1 Position vom 01. bis 03. belegt drei Kalendertage")
    pruefe(len(k.positionstage(p_null)) == 1,
           "5.2 Gegenprobe: Ein-Tages-Position belegt genau einen Tag")

    wochenende = pos([("X", "2020-01-03", "2020-01-06", "time_exit")])   # Fr bis Mo
    pruefe(len(k.positionstage(wochenende)) == 4,
           "5.3 Freitag bis Montag sind vier Kalendertage - das Wochenende zaehlt mit")

    zwei_titel = pos([("X", "2020-01-01", "2020-01-03", "time_exit"),
                       ("Y", "2020-01-01", "2020-01-03", "time_exit")])
    pruefe(len(k.positionstage(zwei_titel)) == 3
           and len(k.positionstage_je_titel(zwei_titel)) == 6,
           "5.4 zwei Titel an denselben drei Tagen: 3 Positionstage, 6 Titeltage")

    # -- 6. Gemeinsames Fenster ------------------------------------------
    frueh = pos([("X", "2020-01-01", "2020-01-05", "time_exit")])
    spaet = pos([("X", "2020-02-01", "2020-02-05", "time_exit")])
    pruefe(k.gemeinsames_fenster(frueh, spaet) == (None, None),
           "6.1 Gegenprobe: Zeitraeume ohne Ueberschneidung -> kein gemeinsames Fenster")
    von, bis = k.gemeinsames_fenster(frueh, pos([("X", "2020-01-03", "2020-01-09", "x")]))
    pruefe(str(von.date()) == "2020-01-03" and str(bis.date()) == "2020-01-05",
           "6.2 Fenster ist die Schnittmenge (03. bis 05.)")

    # -- 7. Ueberlappung: nicht symmetrisch, Titel getrennt von Tagen -----
    a = pos([("X", "2020-01-01", "2020-01-10", "time_exit")])
    b = pos([("X", "2020-01-01", "2020-01-02", "time_exit"),
              ("X", "2020-01-09", "2020-01-10", "time_exit")])
    u_ab = k.ueberlappung(a, b)
    u_ba = k.ueberlappung(b, a)
    pruefe(u_ab["tage_a"] == 10 and u_ab["anteil_tage"] == 0.4,
           "7.1 A haelt 10 Tage, an 4 davon haelt auch B -> 40 %")
    pruefe(u_ba["anteil_tage"] == 1.0,
           "7.2 Gegenprobe zur Richtung: umgekehrt sind es 100 % - die Zahl ist nicht symmetrisch")

    fremder_titel = pos([("Y", "2020-01-01", "2020-01-10", "time_exit")])
    u_fremd = k.ueberlappung(a, fremder_titel)
    pruefe(u_fremd["anteil_tage"] == 1.0 and u_fremd["anteil_titel"] == 0.0,
           "7.3 Gegenprobe Titel gegen Tage: dieselben Tage, anderer Titel -> 100 % / 0 %")

    # -- 8. Naehe der Einstiege ------------------------------------------
    # Eine lange Fuellposition je Bot haelt das gemeinsame Fenster offen,
    # damit die zu pruefenden Einstiege hineinfallen.
    a_naehe = pos([("X", tag(0), tag(31), "time_exit"),
                    ("X", tag(10), tag(11), "stop_loss")])
    b_treffer = pos([("X", tag(0), tag(31), "time_exit"),
                      ("X", tag(13), tag(14), "stop_loss")])
    b_daneben = pos([("X", tag(0), tag(31), "time_exit"),
                      ("X", tag(14), tag(15), "stop_loss")])

    n_treffer = k.naehe(a_naehe, b_treffer, zufallslaeufe=0)
    pruefe(n_treffer["einstiege_a"] == 2 and n_treffer["treffer"] == 2,
           "8.1 Abstand genau 3 Tage liegt NOCH im Fenster -> 2 von 2 Einstiegen")
    n_daneben = k.naehe(a_naehe, b_daneben, zufallslaeufe=0)
    pruefe(n_daneben["treffer"] == 1,
           "8.2 Gegenprobe Fensterrand: Abstand 4 Tage liegt NICHT mehr drin -> 1 von 2")

    kein_titel = pos([("Z", tag(0), tag(31), "time_exit"),
                       ("Z", tag(10), tag(11), "stop_loss")])
    pruefe(k.naehe(a_naehe, kein_titel, zufallslaeufe=0)["treffer"] == 0,
           "8.3 Gegenprobe: gleiche Tage, aber kein gemeinsamer Titel -> 0 Treffer")

    # -- 9. Versatz: Vorzeichen und Deckung mit der Naehe-Zahl ------------
    v = k.versatz_verteilung(a_naehe, b_treffer)
    pruefe(v["n"] == 2 and v["median_versatz"] == 1.5,
           "9.1 Versatz 0 und +3 Tage -> Median 1,5")
    pruefe(v["histogramm"]["0 bis < 3"] == 1 and v["histogramm"]["3 bis < 10"] == 1,
           "9.2 Vorzeichen: B steigt SPAETER ein -> positiver Versatz")
    pruefe(abs(v["anteil_bis_3_tage"] - n_treffer["anteil"]) < 1e-12,
           "9.3 Deckung: 'Anteil bis 3 Tage' aus der Versatzrechnung gleicht dem "
           "Anteil aus der Fenstersuche")

    v_um = k.versatz_verteilung(b_treffer, a_naehe)
    pruefe(v_um["median_versatz"] == -1.5,
           "9.4 Gegenprobe Vorzeichen: umgekehrte Richtung -> Median -1,5")

    # -- 10. Zufallsvergleich: Ziehung gegen geschlossene Form ------------
    # 50 A-Einstiege und 20 B-Einstiege auf 1000 Tagen. Der erwartete Anteil
    # haengt nur von den ANZAHLEN ab: 1 - (1 - 7/1000)**20 = 0,1314.
    lang_a = pos([("X", tag(0), tag(999), "time_exit")]
                  + [("X", tag(i), tag(i + 1), "stop_loss") for i in range(0, 1000, 20)])
    lang_b = pos([("X", tag(0), tag(999), "time_exit")]
                  + [("X", tag(i + 7), tag(i + 8), "stop_loss") for i in range(0, 1000, 50)])
    erwartet = k.naehe_erwartet_analytisch(lang_a, lang_b)
    gezogen = k.naehe(lang_a, lang_b, zufallslaeufe=200)["anteil_zufall"]
    pruefe(abs(gezogen - erwartet) < 0.03,
           f"10.1 Ziehung ({gezogen:.3f}) und geschlossene Form ({erwartet:.3f}) "
           "liegen weniger als 3 Prozentpunkte auseinander")
    pruefe(gezogen <= erwartet + 1e-9,
           "10.2 die Ziehung liegt nicht ueber der geschlossenen Form - diese "
           "vernachlaessigt die Randeffekte und ist deshalb die obere Schranke")

    # -- 11. Horizont-Klassen --------------------------------------------
    pruefe(k.horizont_klasse(2.99) == "bis 2 Tage",
           "11.1 Median 2,99 Tage -> 'bis 2 Tage'")
    pruefe(k.horizont_klasse(3.0) == "3 bis 10 Tage" and k.horizont_klasse(10.0) == "3 bis 10 Tage",
           "11.2 Gegenprobe Klassengrenze: 3,0 und 10,0 liegen im Fenster der Vermutung")
    pruefe(k.horizont_klasse(10.5) == "11 bis 30 Tage" and k.horizont_klasse(21.0) == "11 bis 30 Tage",
           "11.3 10,5 und 21,0 liegen darueber")
    pruefe(k.horizont_klasse(200.0) == "ueber 90 Tage", "11.4 200 Tage -> 'ueber 90 Tage'")


# ===========================================================================
# Mutationsproben
# ===========================================================================

MUTATIONEN = [
    ("Haltedauer in Stunden statt Tagen",
     "return (aus - ein) / pd.Timedelta(days=1)",
     "return (aus - ein) / pd.Timedelta(hours=1)"),
    ("Ausstiegstag nicht mehr als Positionstag gezaehlt",
     'for tag in pd.date_range(a, b, freq="D"):',
     'for tag in pd.date_range(a, b, freq="D")[:-1]:'),
    ("Naehe-Fenster um einen Tag zu eng",
     'spanne = np.timedelta64(fenster_tage, "D")',
     'spanne = np.timedelta64(fenster_tage - 1, "D")'),
    ("Vorzeichen des Versatzes gedreht",
     "versatz.append(float(abstand[np.argmin(np.abs(abstand))]))",
     "versatz.append(float(-abstand[np.argmin(np.abs(abstand))]))"),
    ("Histogramm-Klassen rechts geschlossen statt links",
     "zaehler = [int(((s >= grenzen[i]) & (s < grenzen[i + 1])).sum())",
     "zaehler = [int(((s > grenzen[i]) & (s <= grenzen[i + 1])).sum())"),
    ("Zweigipfligkeit immer bejaht",
     'getrennt = bool(a["q3"] < b["q1"] or b["q3"] < a["q1"])',
     "getrennt = True"),
    ("Grenze der Horizont-Klasse verschoben",
     '("bis 2 Tage", 0.0, 3.0),',
     '("bis 2 Tage", 0.0, 4.0),'),
    ("Ueberlappung auf B statt auf A bezogen",
     '"anteil_tage": (len(tage_a & tage_b) / len(tage_a)) if tage_a else None,',
     '"anteil_tage": (len(tage_a & tage_b) / len(tage_b)) if tage_b else None,'),
    ("Titel-Ueberlappung rechnet mit Tagen statt mit Titeln",
     '"anteil_titel": (len(titel_a & titel_b) / len(titel_a)) if titel_a else None,',
     '"anteil_titel": (len(tage_a & tage_b) / len(tage_a)) if tage_a else None,'),
    ("getrennte Zeitraeume gelten als ueberlappend",
     "if von > bis:\n        return None, None",
     "if False:\n        return None, None"),
]


def mutiertes_modul(alt: str, neu: str):
    with open(KERN_PFAD) as f:
        quelle = f.read()
    treffer = quelle.count(alt)
    if treffer != 1:
        raise AssertionError(
            f"Mutation trifft {treffer}-mal statt genau einmal: {alt!r}")
    modul = types.ModuleType("haltedauer_kern_mutiert")
    modul.__file__ = KERN_PFAD
    exec(compile(quelle.replace(alt, neu), "<mutiert>", "exec"), modul.__dict__)
    return modul


def mutationsproben():
    global FEHLER, LEISE
    print("\n12. Mutationsproben - jede Verfaelschung des Kerns muss auffallen")
    bestanden = 0
    for name, alt, neu in MUTATIONEN:
        modul = mutiertes_modul(alt, neu)
        gemerkt, FEHLER, LEISE = FEHLER, [], True
        try:
            try:
                pruefungsreihe(modul)
            except Exception as fehler:               # Absturz zaehlt als erkannt
                FEHLER.append(f"Absturz: {type(fehler).__name__}")
            erkannt, anzahl = bool(FEHLER), len(FEHLER)
        finally:
            FEHLER, LEISE = gemerkt, False
        if erkannt:
            print(f"  ok    {name} -> {anzahl} Pruefung(en) schlagen an")
            bestanden += 1
        else:
            print(f"  FEHLT {name} -> KEINE Pruefung schlaegt an")
            FEHLER.append(f"Mutation unerkannt: {name}")
    print(f"  {bestanden} von {len(MUTATIONEN)} Mutationen erkannt")


# ===========================================================================
# Wache: die Untersuchung fasst nichts aussehalb ihres Ordners an
# ===========================================================================

_PRODUKTIVORDNER = ("strategies", "shared", "results", "broker", "config",
                    "dashboard", "notifications", "system")


def _arbeitsbaum():
    """Zustand des Arbeitsbaums - Namen UND Inhalt der Aenderungen."""
    status = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain"], cwd=_REPO_ROOT,
                            capture_output=True, text=True)
    diff = subprocess.run(["git", "--no-optional-locks", "diff", "--", *_PRODUKTIVORDNER],
                          cwd=_REPO_ROOT, capture_output=True, text=True)
    return status.stdout + "\n---\n" + diff.stdout


# Beim Laden dieses Tests aufgenommen, damit die Wache am Ende auch das
# sieht, was der TEST selbst angerichtet haben koennte - etwa eine
# Mutationsprobe, die versehentlich neben das Wegwerf-Verzeichnis schreibt.
_ARBEITSBAUM_ZU_BEGINN = None


# ---------------------------------------------------------------------------
# 13 (b) Schreibziele - je Schreibaufruf, ueber den Syntaxbaum (TB-175)
# ---------------------------------------------------------------------------
# Bis TB-175 galt: wer schreibt (open mit w/a/x oder JEDER to_csv/to_json-
# Aufruf), muss irgendwo im Quelltext ERGEBNIS_DIR, DATEN_DIR oder
# TemporaryDirectory nennen. Seit TB-98 (46e3ed0) schreibt
# positionen_holen.py in den Ordner aus dem Pflichtargument --ziel, ueber
# _schreibe_einmal (O_EXCL); die alte Fassung war damit rot, ohne dass falsch
# geschrieben wurde (`alle.to_csv(index=False)` liefert nur Text). Jetzt gilt
# je Schreibaufruf:
#   * allgemein: der Aufruf bildet sein Ziel aus ERGEBNIS_DIR oder DATEN_DIR
#     (beide genau einmal auf Modulebene aus `_DIR`), oder er liegt in einem
#     `with ...TemporaryDirectory()`-Block;
#   * positionen_holen.py (Register 36.1): ZIEL_DIR genau einmal, nur aus
#     `--ziel` (required=True, keine Voreinstellung, kein set_defaults), und
#     geschrieben wird nur in `_schreibe_einmal`, das mit O_CREAT|O_EXCL
#     (ohne O_TRUNC) in ZIEL_DIR oeffnet.

import ast as _ast

_ERLAUBTE_ORTE = ("ERGEBNIS_DIR", "DATEN_DIR")
_SCHREIBMODUS = ("w", "a", "x", "+")
_METHODE_ZIEL = {"to_csv": "path_or_buf", "to_json": "path_or_buf",
                 "to_excel": "excel_writer", "to_parquet": "path",
                 "to_pickle": "path", "to_feather": "path", "to_html": "buf",
                 "to_string": "buf", "to_markdown": "buf", "savefig": "fname"}
_OS_SCHREIBT = ("makedirs", "mkdir", "replace", "rename", "remove", "unlink",
                "rmdir", "symlink", "link", "truncate")
_SHUTIL_SCHREIBT = ("copy", "copy2", "copyfile", "copytree", "move", "rmtree")
_NP_SCHREIBT = ("save", "savetxt", "savez", "savez_compressed")
_OS_SCHREIBFLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_APPEND", "O_TRUNC")


def _namen(knoten):
    return {k.id for k in _ast.walk(knoten) if isinstance(k, _ast.Name)}


def _attrs(knoten):
    return {k.attr for k in _ast.walk(knoten) if isinstance(k, _ast.Attribute)}


def _modus(knoten, stelle):
    werte = list(knoten.args[stelle:stelle + 1]) + [
        k.value for k in knoten.keywords if k.arg == "mode"]
    if not werte:
        return False
    w = werte[0]
    if not (isinstance(w, _ast.Constant) and isinstance(w.value, str)):
        return True                     # Modus nicht ablesbar: gilt als schreibend
    return any(z in w.value for z in _SCHREIBMODUS)


def _schreibart(knoten):
    """Name der Schreibart, wenn der Aufruf schreibt, sonst None."""
    f = knoten.func
    basis = f.value.id if (isinstance(f, _ast.Attribute)
                           and isinstance(f.value, _ast.Name)) else None
    name = f.id if isinstance(f, _ast.Name) else getattr(f, "attr", None)
    if name == "open" and basis in (None, "io", "codecs", "builtins"):
        return "open" if _modus(knoten, 1) else None
    if name == "open" and basis == "os":
        return "os.open" if _attrs(knoten) & set(_OS_SCHREIBFLAGS) else None
    if name == "fdopen":
        return "os.fdopen" if _modus(knoten, 1) else None
    if basis == "os" and name in _OS_SCHREIBT:
        return "os." + name
    if basis == "shutil" and name in _SHUTIL_SCHREIBT:
        return "shutil." + name
    if basis in ("np", "numpy") and name in _NP_SCHREIBT:
        return "np." + name
    if name in ("write_text", "write_bytes"):
        return name
    if name in _METHODE_ZIEL and isinstance(f, _ast.Attribute):
        if knoten.args or any(k.arg == _METHODE_ZIEL[name] for k in knoten.keywords):
            return name                 # mit Ziel; ohne Ziel liefert es nur Text
    return None


def _schreibaufrufe(baum):
    """(Aufruf, Schreibart, umgebende Funktion, in TemporaryDirectory-Block)."""
    gefunden = []

    def gehe(knoten, funktion, temp):
        if isinstance(knoten, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            funktion = knoten.name
        if isinstance(knoten, (_ast.With, _ast.AsyncWith)) and any(
                isinstance(p.context_expr, _ast.Call) and "TemporaryDirectory" in (
                    {getattr(p.context_expr.func, "id", None),
                     getattr(p.context_expr.func, "attr", None)})
                for p in knoten.items):
            temp = True
        if isinstance(knoten, _ast.Call):
            art = _schreibart(knoten)
            if art:
                gefunden.append((knoten, art, funktion, temp))
        for kind in _ast.iter_child_nodes(knoten):
            gehe(kind, funktion, temp)

    gehe(baum, None, False)
    return gefunden


def _zuweisungen(baum, name):
    """Alle Zuweisungen an `name` (auch in Funktionen), als (Knoten, Wert, Modulebene)."""
    oben = set(id(k) for k in baum.body)
    gef = []
    for k in _ast.walk(baum):
        ziele = (k.targets if isinstance(k, _ast.Assign) else
                 [k.target] if isinstance(k, (_ast.AnnAssign, _ast.AugAssign)) else [])
        for z in ziele:
            if name in {t.id for t in _ast.walk(z) if isinstance(t, _ast.Name)}:
                gef.append((k, getattr(k, "value", None), id(k) in oben))
        if isinstance(k, _ast.Global) and name in k.names:
            gef.append((k, None, False))
    return gef


def _regel_allgemein(baum, aufrufe):
    grund = []
    for ort in _ERLAUBTE_ORTE:
        z = _zuweisungen(baum, ort)
        if z and not (len(z) == 1 and z[0][2] and "_DIR" in _namen(z[0][1])):
            grund.append(f"{ort} nicht genau einmal auf Modulebene aus _DIR")
    for knoten, art, _funktion, temp in aufrufe:
        if temp:
            continue
        if not (_namen(knoten) & set(_ERLAUBTE_ORTE)) or not any(
                _zuweisungen(baum, o) for o in _namen(knoten) & set(_ERLAUBTE_ORTE)):
            grund.append(f"Z. {knoten.lineno} {art} ohne ERGEBNIS_DIR/DATEN_DIR")
    return grund


def _regel_positionen_holen(baum, aufrufe):
    """Register 36.1: Ziel nur aus --ziel, Schreiben nur ueber _schreibe_einmal."""
    grund = []
    ziel_arg = [k for k in _ast.walk(baum) if isinstance(k, _ast.Call)
                and getattr(k.func, "attr", None) == "add_argument"
                and any(isinstance(a, _ast.Constant) and a.value == "--ziel"
                        for a in k.args)]
    if len(ziel_arg) != 1:
        grund.append(f"--ziel {len(ziel_arg)}-mal statt genau einmal")
    else:
        kw = {k.arg: k.value for k in ziel_arg[0].keywords}
        if not (isinstance(kw.get("required"), _ast.Constant)
                and kw["required"].value is True):
            grund.append("--ziel nicht required=True")
        if "default" in kw:
            grund.append("--ziel mit Voreinstellung (default)")
    if any(isinstance(k, _ast.Call) and getattr(k.func, "attr", None) == "set_defaults"
           for k in _ast.walk(baum)):
        grund.append("set_defaults vorhanden")
    leser = {z.id for k in _ast.walk(baum) if isinstance(k, _ast.Assign)
             and isinstance(k.value, _ast.Call)
             and getattr(k.value.func, "attr", None) == "parse_args"
             for z in k.targets if isinstance(z, _ast.Name)}
    erlaubt = {_ast.dump(_ast.parse(f"os.path.abspath({n}.ziel)", mode="eval").body)
               for n in leser} | {_ast.dump(_ast.parse(f"{n}.ziel", mode="eval").body)
                                  for n in leser}
    z = _zuweisungen(baum, "ZIEL_DIR")
    if not (len(z) == 1 and z[0][2] and z[0][1] is not None
            and _ast.dump(z[0][1]) in erlaubt):
        grund.append("ZIEL_DIR nicht genau einmal, nur aus --ziel")
    defs = [k for k in baum.body if isinstance(k, _ast.FunctionDef)
            and k.name == "_schreibe_einmal"]
    if len(defs) != 1:
        grund.append("_schreibe_einmal nicht genau einmal auf Modulebene")
    for knoten, art, funktion, _temp in aufrufe:
        if funktion != "_schreibe_einmal":
            grund.append(f"Z. {knoten.lineno} {art} ausserhalb von _schreibe_einmal")
        elif art == "os.open":
            fl = set().union(*(_attrs(a) for a in knoten.args[1:2]))
            pfad = knoten.args[0] if knoten.args else None
            aus_ziel = pfad is not None and ("ZIEL_DIR" in _namen(pfad) or any(
                "ZIEL_DIR" in _namen(w) for _k, w, _o in (
                    _zuweisungen(defs[0], pfad.id) if defs and isinstance(pfad, _ast.Name)
                    else []) if w is not None))
            if not ({"O_CREAT", "O_EXCL"} <= fl) or "O_TRUNC" in fl:
                grund.append(f"Z. {knoten.lineno} os.open ohne O_CREAT|O_EXCL")
            if not aus_ziel:
                grund.append(f"Z. {knoten.lineno} os.open nicht in ZIEL_DIR")
        elif art != "os.fdopen":
            grund.append(f"Z. {knoten.lineno} {art} in _schreibe_einmal")
    if defs and not any(art == "os.open" and f == "_schreibe_einmal"
                        for _k, art, f, _t in aufrufe):
        grund.append("_schreibe_einmal ohne os.open")
    return grund


_SONDERREGELN = {"positionen_holen.py": _regel_positionen_holen}


def schreibziele_aus_quellen(quellen):
    """quellen: {Dateiname: Quelltext}. Liefert [(Datei, Grund)] - leer = gut."""
    befund = []
    for name in sorted(quellen):
        baum = _ast.parse(quellen[name])
        aufrufe = _schreibaufrufe(baum)
        regel = _SONDERREGELN.get(name)
        if regel is None and not aufrufe:
            continue
        for g in (regel or _regel_allgemein)(baum, aufrufe):
            befund.append((name, g))
    return befund


def _gruppe(ordner):
    return {n: open(os.path.join(ordner, n), encoding="utf-8").read()
            for n in sorted(os.listdir(ordner))
            if n.endswith(".py") and not n.startswith("test_")}


# Gegenproben zu 13 (b) (Prinzip 12): je EINE Stelle im Quelltext verfaelscht,
# nur im Speicher; jede muss genau einmal treffen und die Datei rot machen.
GEGENPROBEN_13 = [
    ("--ziel mit Voreinstellung", "positionen_holen.py",
     '_aufruf.add_argument("--ziel", required=True,',
     '_aufruf.add_argument("--ziel", required=True, default=".",'),
    ("--ziel nicht Pflicht", "positionen_holen.py",
     '_aufruf.add_argument("--ziel", required=True,',
     '_aufruf.add_argument("--ziel", required=False,'),
    ("ZIEL_DIR nicht aus --ziel", "positionen_holen.py",
     "ZIEL_DIR = os.path.abspath(_args.ziel)",
     'ZIEL_DIR = os.path.join(_DIR, "daten")'),
    ("O_EXCL durch O_TRUNC ersetzt", "positionen_holen.py",
     "os.O_WRONLY | os.O_CREAT | os.O_EXCL",
     "os.O_WRONLY | os.O_CREAT | os.O_TRUNC"),
    ('open(..., "w") statt _schreibe_einmal', "positionen_holen.py",
     'hashes[f"{BOT}_alle_trades.csv"] = _schreibe_einmal(\n'
     '        f"{BOT}_alle_trades.csv", alle.to_csv(index=False))',
     'open(os.path.join(ZIEL_DIR, f"{BOT}_alle_trades.csv"), "w").write(\n'
     '        alle.to_csv(index=False))'),
    ("auswertung.py schreibt neben ERGEBNIS_DIR", "auswertung.py",
     'open(os.path.join(ERGEBNIS_DIR, "zusammenfassung.json"), "w")',
     'open(os.path.join(_DIR, "..", "zusammenfassung.json"), "w")'),
]


def wache_repo_unveraendert(ordner=None):
    """Die Untersuchung fasst nichts ausserhalb ihres Ordners an.

    Bis TB-30a stand hier eine andere Pruefung: `git status` durfte nichts
    ausserhalb von `research/tb24_haltedauern/` und `docs/` melden. Die war
    falsch gebaut, und zwar so, dass es erst auffiel, als sie zum ersten Mal
    anschlug.

    Sie prueft naemlich nicht diese Untersuchung, sondern den ARBEITSBAUM -
    und der enthaelt alles, woran gerade sonst noch gearbeitet wird. TB-30a
    aendert `shared/` und legt `research/vorregistrierung/` an, beides
    ausdruecklich beauftragt und mit TB-24 nicht verwandt. Die alte Fassung
    meldete das als Verstoss von TB-24. Ein Waechter, der bei fremder Arbeit
    rot wird, wird abgeschaltet - und dann faengt er auch den Fall nicht
    mehr, fuer den er da ist. (Dieselbe Falle steckte in
    `research/versuchsregister/test_versuchsregister.py`; sie ist dort in
    derselben Aenderung behoben.)

    An ihre Stelle treten zwei Zusicherungen, die beide diese Untersuchung
    betreffen und beide rot werden koennen:

      1. **Dieser Testlauf veraendert nichts.** Aufgenommen beim Laden,
         verglichen am Ende - inklusive der zehn Mutationsproben, die
         dazwischen laufen.
      2. **Wer schreibt, schreibt in den eigenen Ordner.** Ueber den
         Syntaxbaum geprueft, nicht ueber eine Textsuche: ein Kommentar mit
         `open(..., "w")` soll nicht anschlagen. Seit TB-175 je
         Schreibaufruf: Ziel aus ERGEBNIS_DIR/DATEN_DIR, bei
         `positionen_holen.py` nur aus `--ziel` ueber `_schreibe_einmal`
         (O_EXCL); dazu sechs Gegenproben im Speicher (GEGENPROBEN_13).

    Was hier bewusst NICHT geschieht: `auswertung.py` starten. Es wuerde die
    abgelegten Ergebnisdateien neu schreiben - eine Wache, die den Zustand
    veraendert, den sie prueft, ist keine.
    """
    print("\n13. Wache: die Untersuchung fasst nichts ausserhalb ihres "
          "Ordners an")
    ausgabe = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain"], cwd=_REPO_ROOT,
                              capture_output=True, text=True)
    if ausgabe.returncode != 0:
        pruefe(False, "git status nicht ausfuehrbar")
        return

    pruefe(_ARBEITSBAUM_ZU_BEGINN == _arbeitsbaum(),
           "dieser Testlauf hat den Arbeitsbaum nicht veraendert")

    # (b) TB-175: jeder Schreibaufruf an einen erlaubten Ort (Regeln oben).
    quellen = _gruppe(ordner or _DIR)
    befund = schreibziele_aus_quellen(quellen)
    pruefe(not befund,
           f"wer schreibt, schreibt nur an einen erlaubten Ort "
           f"(aussen vor: {befund or 'keine'})")
    for titel, datei, alt, neu in GEGENPROBEN_13:
        treffer = quellen.get(datei, "").count(alt)
        rot = treffer == 1 and any(
            d == datei for d, _g in schreibziele_aus_quellen(
                dict(quellen, **{datei: quellen[datei].replace(alt, neu)})))
        pruefe(rot, f"Gegenprobe 13: {titel} -> {datei} faellt auf"
                    + ("" if treffer == 1 else f" (trifft {treffer}-mal)"))


# ===========================================================================
# Der Live-Weg: dass er "keine Datenbank gefunden" meldet, beweist nichts
# ===========================================================================

def pruefe_live_weg():
    """`live_haltedauern.py` findet in dieser Umgebung keine Datenbank. Eine
    Meldung "nichts gefunden" ist aber kein Beleg dafuer, dass der Weg
    funktionieren WUERDE - genau die Falle aus Prinzip 12. Hier wird deshalb
    eine Datenbank mit dem echten Schema aufgebaut, mit von Hand
    nachrechenbaren Trades gefuellt und ausgelesen.
    """
    import shutil
    import sqlite3
    import tempfile

    print("\n14. Live-Weg gegen eine gebaute Datenbank (Gegenprobe zu 'nichts gefunden')")
    import live_haltedauern as lh

    ordner = tempfile.mkdtemp(prefix="tb24_live_")
    try:
        pfad = os.path.join(ordner, "paper_trading_elliott_wave.db")
        conn = sqlite3.connect(pfad)
        conn.execute("CREATE TABLE trades (symbol TEXT, entry_time TEXT, "
                      "exit_time TEXT, result TEXT, pnl_pct REAL, status TEXT)")
        conn.executemany("INSERT INTO trades VALUES (?,?,?,?,?,?)", [
            # 3 Tage, Strategie-Ausstieg
            ("BTCUSDT", "2026-09-01 07:00:00", "2026-09-04 07:00:00", "stop_loss", -6.0, "closed"),
            # 10 Tage, Strategie-Ausstieg
            ("ETHUSDT", "2026-09-02 07:00:00", "2026-09-12 07:00:00", "time_exit", 2.0, "closed"),
            # 2 Tage, aber vom Nutzer geschlossen - darf NICHT in den Median
            ("XRPUSDT", "2026-09-03 07:00:00", "2026-09-05 07:00:00", "manual_close", 1.0, "closed"),
            # offen - darf gar nicht gelesen werden
            ("ADAUSDT", "2026-09-10 07:00:00", None, None, None, "open"),
        ])
        conn.commit()
        conn.close()

        gemerkt = lh._REPO_ROOT
        lh._REPO_ROOT = ordner
        try:
            df = lh.lese_trades("elliott_wave")
            fehlt = lh.lese_trades("t3_supertrend")
        finally:
            lh._REPO_ROOT = gemerkt

        pruefe(df is not None and len(df) == 3,
               "14.1 drei geschlossene Trades gelesen, der offene nicht")
        pruefe(fehlt is None,
               "14.2 Gegenprobe: fehlende Datenbank gibt None, nicht einen leeren Satz - "
               "'nicht nachgesehen' und 'nichts da' bleiben unterscheidbar")

        strategie = df[df["result"] != lh.MANUELL]
        tage = sorted(haltedauer_kern.haltedauer_tage(strategie))
        pruefe(tage == [3.0, 10.0],
               "14.3 Haltedauern 3 und 10 Tage - der manuelle Ausstieg (2 Tage) "
               "bleibt aussen vor")
        pruefe(haltedauer_kern.kennzahlen(tage)["median"] == 6.5,
               "14.4 Median daraus 6,5 Tage")

        # Gegenprobe zum Schreibschutz: mode=ro muss einen Schreibversuch
        # abweisen. Sonst waere "liest nur" eine Behauptung, keine Eigenschaft.
        verweigert = False
        try:
            with sqlite3.connect(f"file:{pfad}?mode=ro", uri=True) as c:
                c.execute("DELETE FROM trades")
        except sqlite3.OperationalError:
            verweigert = True
        pruefe(verweigert,
               "14.5 mode=ro verweigert einen Schreibversuch auf dieselbe Datei")
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


if __name__ == "__main__":
    # Vor allem anderen: der Ausgangszustand des Arbeitsbaums. Die Wache in
    # Abschnitt 13 vergleicht ihn am Ende mit dem dann erreichten - so sieht
    # sie auch, was dieser Test selbst angerichtet haette.
    _ARBEITSBAUM_ZU_BEGINN = _arbeitsbaum()

    print("1.-11. Gegenproben auf dem echten Rechenkern")
    pruefungsreihe(haltedauer_kern)
    print(f"  {GEZAEHLT[0] - len(FEHLER)} von {GEZAEHLT[0]} Gegenproben bestanden")

    pruefe_live_weg()
    mutationsproben()
    wache_repo_unveraendert()

    print()
    if FEHLER:
        print(f"{len(FEHLER)} Pruefung(en) fehlgeschlagen:")
        for f in FEHLER:
            print(f"  - {f}")
        sys.exit(1)
    print("Alle Pruefungen bestanden.")
````

