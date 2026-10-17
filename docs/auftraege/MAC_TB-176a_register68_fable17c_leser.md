# TB-176a Register 68 (Fable 17c, R108, neun Marken, S-B1 Nachtrag 10a.5) und Leser auf `alle_trades` (E2) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 20:38** (Helfer BAU176A, per Skript aus Bausteinen, `/tmp/w36/sc/tb176/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis E2 (mit R und K) an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `6da15e0`; Start am HEAD `6da15e07e4940f1ea5bb8bf07301a90f41cd6a94`.**

**Sitzungstitel:** `TB-176a` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `6da15e07e4940f1ea5bb8bf07301a90f41cd6a94` (kommt bis zum Start ein Commit dazu, füllt der steuernde Chat HEAD und Soll neu) · **Start:** über den Sitzungswächter (`starte_TB-176a`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (Python 3.9, numpy 2.0.2, pandas 2.3.3 nach `requirements.lock`); Werkzeug `docs/belege/TB-176a/tb176a_werkzeug.py` (Anhang A), kurz `WZ`. **Belege:** `docs/belege/TB-176a/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-176a_register68_fable17c_leser.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FL ⇒ FM).
**Grundlage Register (zeichengleich, nicht umdeuten):** Fable-Antwort 17.10.c (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md`, md5 `a2b38226f683d8d106a5dec61fa5f325`, 10 079 B; bis Schritt 0 git-ignoriert unter `data_sicherung/steuernder_chat_tmp/f17c/`), Registerblock R108; Anfrage 17.10.c (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md`, md5 `0a559c880aa422ca0d77f03c5aa240bc`, 6 703 B) und Übergabe 17.10.c (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md`, md5 `db41d912f05314a47dcc0e501c3aed5a`, 2 212 B), ebenda; R56 (b) (Anfrage und Antwort mit Commit im Repo, bevor eingetragen wird); Bauart 67 (Register aus Fable mit Marken, TB-175). Quelle des Auftrags: Nachricht des steuernden Chats an den Helfer BAU176A vom 17.10.2026 (Schnitt TB-176a/b; ausserhalb des Repos).
**Schnitt (steuernder Chat, 17.10.2026):** TB-176a = 0, V, R, K, E2, A, F **ohne Handelscode**. **Nicht** in TB-176a: Wert und Ort des Startkapitals nach R108 (d) (TB-176b, Handelscode, nach einer Frage an den Verfahrensprüfer zur Voraussetzung in (d)) und die nachgeholte Prüfung nach R108 (e) (nach Fable). Beides kommt in A auf BACKLOG Rang 1.
**Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 (mit Fable 17.10.c ins Repo) ⇒ V ⇒ R (Register 68, neun Marken, S-B1 10a.5 mit Marke an 10a.2) ⇒ K (Kopien, Index, Dialog-Index) ⇒ E2 (Leser) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F. Registereintrag nur in R.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 35 („Opus Trading Bots-17.10.2026 b“), 17.10.2026, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript, Zeit 2026-10-17T18:40:36.385Z UTC): Your questions have been answered: "Gibst du TB-176a frei? Der Auftrag macht vier Dinge. (1) Er bringt Anfrage, Antwort und Übergabe von Fable 17.10.c unverändert ins Repo, mit md5 vorher und nachher. (2) Er schreibt Register 68 mit R108, zeichengleich aus der Antwort, dazu die neun Marken. In S-B1 steht der Nachtrag 10a.5 im Wortlaut, aber mit dem Vermerk „nicht eingetragen“. R108 (a) verlangt dafür eine äussere Quelle, die noch fehlt; die suche ich danach. Die Messung zum Startkapital steht als Tatsachennotiz in 68.2 (a). (3) Er stellt die zwei Leser auswertung.py und embargo_neun.py auf alle gefundenen Trades um. (4) Er committet die Umzugsdateien. Kein Handelscode, keine Kurse, kein Live, kein Geld. Nicht dabei sind der Ort des Startkapitals (TB-176b) und die Prüfung nach R108 (e); beide warten auf Fable 17.10.d. bau.sh endet mit rc 0, die 20 Simulationen waren gut. Simuliert wurde auf dem Gerät mit Python 3.10, am Mac läuft 3.9. Nach R108 (c) ist D4 bei t3_supertrend auf den alten Listen danach rot; das bleibt bis zur Neuerzeugung so. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Das Register steht dann auf dem Stand von Fable 17.10.c."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. `WZ register` übernimmt die Zeile wörtlich in den Kopfsatz von 68. TB-176a ändert keinen Handelscode und keine Datei der Sperrliste; unter `research/` ändert E2 genau zwei Leser: `research/tb24_haltedauern/auswertung.py` und `research/faltenplan_neun/embargo_neun.py`.

## Was eingetragen wird (Schritt R, K)

- **Abschnitt 68** (`WZ register`): Titel `## 68. Fable 17c — Registerblock R108 (TB-176a)`; Kopfsatz (Bauart 67, Quelle mit md5, Anfrage und Übergabe, Karte wörtlich); **68.1 R108** „> R108 …“ und „> Quelle des Grundes“ **zeichengleich** aus dem Codeblock der Antwort (das Werkzeug liest sie aus der Datei und vergleicht nach dem Schreiben Zeichen für Zeichen), eine „**Kette:**“-Zeile (Marken, ohne Marke, „Zählung: kein Fall; sechzehn“ nach R108 (f)); **68.2 Voraussetzungen und Befunde**: `v_voraussetzung.txt` wörtlich eingerückt und die Tatsachennotizen **(a)** R108 (d), die zwei Voraussetzungen in eckigen Klammern, gemessen durch Lesen (Register am Stand `7fe6342`: Stellen, die einen Wert des Startkapitals nennen; Wert je `equity_simulation.py` mit Zeile) — nur gemessen, Wert und Ort werden **nicht** eingetragen; **(b)** R108 (a): Tatsachennotiz mit äusserer Quelle liegt nicht vor, nicht eingetragen; **(c)** R56 (b).
- **Neun Marken** (R108 (f)); je Zeilenpaar wie 67 (Leerzeile, Marke, „Eintrag und Stand oben bleiben zeichengleich.“); der alte Satz bleibt unberührt; Einfügestelle nach „> Quelle des Grundes“ (62.2, 66.1, 67.1), nach der letzten Zeichengleich-Zeile (16.6; 41.3 C2: nach der Marke aus R86, vor C3) bzw. am Ende des Unterabschnitts (16.4, 16.8, 29.3, 37.5); stehen dort schon Marken, kommt die neue dahinter:
  - an 62.2: `> ⭐ **62.2 R101 ERGÄNZT und BERICHTIGT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (a): ERGÄNZT zu (a) bis (c), BERICHTIGT zu (a) („lies“), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 16.4: `> ⭐ **16.4 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (b), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 16.6: `> ⭐ **16.6 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (c), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 16.8: `> ⭐ **16.8 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (b), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 29.3: `> ⭐ **29.3 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (d), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 37.5: `> ⭐ **37.5 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (d), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 41.3 C2: `> ⭐ **41.3 C2 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (c), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 66.1: `> ⭐ **66.1 R106 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (e), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 67.1: `> ⭐ **67.1 R107 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkte (b) bis (e), TB-176a, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
- **S-B1-Vorregistrierung** (`docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md`, R108 (a)): Marke an 10a.2 (Ende des Unterabschnitts) `> ⭐ **S-B1 10a.2 ERGÄNZT durch 10a.5** (Fable 17c R108 (68.1), Unterpunkt (a), TB-176a, ⟨DATUM⟩).` + Zeichengleich-Zeile; **datierter Nachtrag 10a.5** nach 10a.4 (vor `---` und `## 11.`): Kopf `### 10a.5 Nachtrag vom ⟨DATUM⟩ — Ergänzung zu Registertext 3 (10a.2) (R108 (a), TB-176a)`, der Wortlaut aus R108 (a) zeichengleich als `> …` (Text zwischen „Wortlaut: „“ und „“ Der Grund trägt“), eine Quellenzeile. 10a.2 und alles Übrige bleiben zeichengleich (`WZ register` prüft es).
- **Ohne Marke** (R108 (f)): 15.4, 17.1, 24.3, 37.3, 38.5, 40.7, 41.1, 41.2, 58.4, 58.5, 62.5, 66.2, Abschnitt 10, S-B1 2, 3.2, 9, 10a.4.
- **Index** (K, `WZ index`): Kopf 0–68, Zeile `| 68 aus 17c |`, neuer Abschnitt 19 (Tabelle der neun Marken aus `r_daten.json`, Satz zur S-B1-Marke und zu 10a.5). **Dialog-Index** 17c über Handfelder.
- Append-only bis auf die neun Marken (`WZ register` prüft es nach dem Schreiben). Register am Bau-HEAD 12688 Zeilen, 67 letzter Abschnitt, kein „R108“.

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen; aus `data_sicherung/` nur die drei Fable-Dateien in Schritt 0 kopieren. Keine Neuerzeugung der neun Listen; `positionen_holen.py`, `alle_bots.py`, `auswertung.py`, `embargo_neun.py` werden nicht gestartet (nur in der Probe an einer Kopie im Temp-Ordner); `test_faltenplan_neun.py` läuft nicht (liest Kursdateien). Nichts unter `strategies/`, `shared/`, `data/`, `config/` ändern; unter `research/` nur die zwei Leser in E2. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`, kein `git stash`, kein `rm`, kein `mv`. **Schreiben darf die Sitzung nur:** die drei Fable-Dateien (Schritt 0, `cp`), `docs/VORREGISTRIERUNG_neuselektion.md` und `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` (nur `WZ register`), `REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Werkzeugen), die zwei Leser (E2, `cp` aus dem Temp-Ordner), BACKLOG und Journal (A, nur `WZ`), das Ergebnis, `docs/auftraege/AKTUELLER_AUFTRAG.md` wie im 0a-Soll, und unter `BEL`.

## Lage nach dem Auslegen

Soll in 0a vom steuernden Chat gefüllt (`[' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md']`); am Bau-HEAD wären es 4 Einträge gewesen: ` M docs/auftraege/AKTUELLER_AUFTRAG.md`, ` M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, ` M docs/projektfuehrung/UEBERGABE.md`, `?? docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md`.

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `6da15e07e4940f1ea5bb8bf07301a90f41cd6a94`, genau die Einträge `[' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md']`, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb176a_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "6da15e07e4940f1ea5bb8bf07301a90f41cd6a94": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "6da15e07e4940f1ea5bb8bf07301a90f41cd6a94": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (N Eintraege)` mit N = Zahl der Einträge im Soll. Anhänge holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb176a_werkzeug.py 169283defde94e2def8edc3b8b6b0ff4def6df9323717b644f452b932c5185ab`; `auswertung.py 9de89e6d302454686f490e151237313011993150f2a120acc0bf879e5331d14b`; `embargo_neun.py f35119ba4b89494d211023c598835640d179f5586c566bc732e5a77c49cc6348`; `tb176a_probe_leser.py e99c4664e79ac36a756ab3bce04e0a9c0290a265e8b7249553518555323b8cf0`; `Dateien 4`; sonst **ABBRUCH**.

**Fable 17.10.c ins Repo** (git-ignoriert ⇒ nicht im 0a-Soll; genau diese Zeilen):

```
cp data_sicherung/steuernder_chat_tmp/f17c/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md
cp data_sicherung/steuernder_chat_tmp/f17c/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md
cp data_sicherung/steuernder_chat_tmp/f17c/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md
```

**md5 vorher (Quelle) = nachher (Repo)** (genau dieser Befehl). Soll: `Pruefungen: 3, NEIN: 0`, letzte Zeile `rc 0`; sonst **ABBRUCH** (die drei Kopien bleiben unverfolgt liegen; melden):

```bash
trading-env/bin/python3 -B "$TMPDIR/tb176a_werkzeug.py" md5 > "$TMPDIR/tb176a_md5.txt" 2>&1; echo "rc $?" >> "$TMPDIR/tb176a_md5.txt"; tail -2 "$TMPDIR/tb176a_md5.txt"
```

Dann genau diese Zeilen (die erste fügt die in 0a geprüften Pfade mit Namen hinzu, dazu die drei Fable-Dateien), Commit `TB-176a Schritt 0: Fable 17.10.c (Anfrage, Antwort, Uebergabe) und Stand des steuernden Chats vor TB-176a (Auftrag)`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
trading-env/bin/python3 -B -c "import subprocess, sys; z = [l[3:] for l in open(sys.argv[1], encoding='utf-8').read().split(chr(10)) if l]; print('git add', len(z)); raise SystemExit(subprocess.run(['git', 'add', '--'] + z).returncode)" "$TMPDIR/tb176a_0a.txt"
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-176a
cp "$TMPDIR/tb176a_0a.txt" docs/belege/TB-176a/0a_status.txt
cp "$TMPDIR/tb176a_md5.txt" docs/belege/TB-176a/0a_md5.txt
cp "$TMPDIR/tb176a_werkzeug.py" docs/belege/TB-176a/tb176a_werkzeug.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py voraussetzung > docs/belege/TB-176a/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (35 Prüfungen: die Gruppe der Leser und der Messung je md5 = Bau; BACKLOG Rang 1, Journal FL oder FM; Anfrage, Antwort und Übergabe 17.10.c verfolgt, gleich HEAD, md5 wie Soll; Registerblock R108 mit dem Wortlaut aus (a); 67 da, 68 nicht; neun Marken-Orte eindeutig; S-B1 10a.2/10a.4 da, 10a.5 nicht; Index-Kopf 0–67, Zeile 67, Pflegezeile TB-175, kein Abschnitt 19; Dialog-Index ohne 17c; Register am Stand `7fe6342` lesbar). Die `info`-Zeilen zu R108 (d) sind Messung, kein Urteil, und gehen wörtlich in 68.2. **Abbruch in V:** im Arbeitsbaum liegt nur der unverfolgte Ordner `BEL`. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-176a/abbruch.txt`, dann `git add` mit Namen für `docs/belege/TB-176a/0a_status.txt`, `docs/belege/TB-176a/0a_md5.txt`, `docs/belege/TB-176a/tb176a_werkzeug.py`, `docs/belege/TB-176a/v_voraussetzung.txt`, `docs/belege/TB-176a/abbruch.txt`, Commit `TB-176a Abbruch: V`, pushen, melden.

## Schritt R — Register 68, neun Marken, S-B1 10a.5

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-176a/v_voraussetzung.txt --probe > docs/belege/TB-176a/r_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/r_probe.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-176a/v_voraussetzung.txt > docs/belege/TB-176a/r_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/r_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach genau diese `git add`, Commit `TB-176a R: Register 68 (Fable 17c, R108), neun Marken, S-B1 Nachtrag 10a.5`, pushen ⇒ **⟨R⟩**:

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md
git add docs/belege/TB-176a/0a_status.txt
git add docs/belege/TB-176a/0a_md5.txt
git add docs/belege/TB-176a/tb176a_werkzeug.py
git add docs/belege/TB-176a/v_voraussetzung.txt
git add docs/belege/TB-176a/r_probe.txt
git add docs/belege/TB-176a/r_eintrag.txt
git add docs/belege/TB-176a/r_daten.json
```

## Schritt K — Kopien, Index, Dialog-Index (wie TB-175 Schritt K)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-176a/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-176a/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-176a/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨R⟩ > docs/belege/TB-176a/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-176a/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_index.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py handfelder docs/belege/TB-176a/k_handfelder.json > docs/belege/TB-176a/k_handfelder.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_handfelder.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-176a/k_handfelder.json > docs/belege/TB-176a/k_dialog_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_dialog_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-176a/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`. **Kein Abbruch** bei rc ≠ 0 in K: festhalten, die Dateien dieses Schritts nicht committen, nicht zurücksetzen, melden, weiter mit E2. Entsteht eine weitere Teildatei: mit Namen anfügen, melden. Dann genau diese `git add`, Commit `TB-176a K: Registerkopie, Index, Dialog-Index`, pushen ⇒ **⟨K⟩**; danach `git status --porcelain` — Soll: keine Ausgabe:

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
git add docs/belege/TB-176a/k_registerkopie.txt
git add docs/belege/TB-176a/k_abschnitte.txt
git add docs/belege/TB-176a/k_pruefen.txt
git add docs/belege/TB-176a/k_index_zeilen.txt
git add docs/belege/TB-176a/k_index.txt
git add docs/belege/TB-176a/k_handfelder.txt
git add docs/belege/TB-176a/k_dialog_index.txt
git add docs/belege/TB-176a/k_dialog_pruefen.txt
git add docs/belege/TB-176a/k_handfelder.json
```

## Schritt E2 — Leser auf `<bot>_alle_trades.csv` (R107 (e))

**Was sich ändert (Anhänge B und C, vollständig):** `research/tb24_haltedauern/auswertung.py` (sha256 `9de89e6d302454686f490e151237313011993150f2a120acc0bf879e5331d14b`) liest nur noch `<bot>_alle_trades.csv` und rechnet auf allen gefundenen Trades: `lade()` ohne `nur_ausgefuehrt`, die Gegenprobe zum Positionslimit (`tabelle_limit_vergleich`, `gegenprobe_positionslimit.csv`; braucht ausgeführt/alle und `trades_uebersprungen`) entfällt, `datenbasis` ohne `trades_ausgefuehrt`, `symbole_ausgefuehrt` und `abgleich_exposure_messung` (fehlen in der neuen Meta), dafür `symbole_gefunden`; Docstring und Ausgabezeile mitgezogen. `research/faltenplan_neun/embargo_neun.py` (sha256 `f35119ba4b89494d211023c598835640d179f5586c566bc732e5a77c49cc6348`): `haltedauern_tage()` liest `<bot>_alle_trades.csv`, Schlüssel `n_positionen` → `n_trades_gefunden`, Herkunft und Ausgabe mitgezogen, Docstring. **Nicht geändert** (Messung nach R94 (b); Startkapital nach R108 (d) erst mit TB-176b, braucht ausgeführte Positionen nach R97 (b) bzw. R45/R84 (e)): `research/mtm_drawdown/grundlage.py`, `messung.py`, `test_mtm_kern.py` (BACKLOG). Die Gegenprobe zu `auswertung.py` im Test (`research/tb24_haltedauern/test_haltedauer_kern.py`, seit TB-175) trifft am neuen `auswertung.py` genau einmal (am Bau gemessen; E2 lässt den Test laufen).

**Probe (Anhang D, `docs/belege/TB-176a/tb176a_probe_leser.py`, sha256 `e99c4664e79ac36a756ab3bce04e0a9c0290a265e8b7249553518555323b8cf0`):** an einer Kopie im Temp-Ordner mit kleinen Listen (6 Trades je Bot, 2 davon `ausgefuehrt=False`, bei der Hälfte der Bots ohne diese Spalte; Meta im Format von `positionen_holen.py`): `auswertung.py` rc 0, n = 6 je Bot, Median 3,5 Tage (von Hand), `datenbasis` ohne ausgeführt-Felder, keine Limit-Datei; `embargo_neun` liest alle 6, P95 und Embargo von Hand; Gegenprobe: die Fassung am HEAD (`git show HEAD:…`) scheitert an derselben Kopie an `<bot>_positionen.csv` — 9 Prüfungen. Kein Lauf auf den echten Listen, keine Kurse.

**D4 nach R108 (c) (Befund der alten Listen, kein Fehler; am Bau gerechnet, nicht gelaufen):** `research/faltenplan_neun/test_faltenplan_neun.py` D4 vergleicht `embargo_neun` mit dem in TB-24 veröffentlichten P90 (ausgeführte Positionen). Auf den abgelegten Listen: P90 alle gefundenen = ausgeführte bei acht Bots, **bei t3_supertrend 8,6833 gegen 9,5000**; P95 t3 → Embargo 12 statt 13, sobald gerechnet. Nach R108 (c) bleibt D4 bis zur Neuerzeugung unverändert und 16.6 bei 13; mit der Neuerzeugung liest die Herleitung die neuen Listen (oder `embargo_neun.py` wird historischer Stand); geprüft wird die Herleitung dann mit erzeugten Beispieldaten. Der Test liest Kursdateien und läuft hier nicht (Verboten). Die zwei Leser lesen kein Startkapital (R108 (d) (2); `WZ nachher2` prüft es).

```
cp "$TMPDIR/auswertung.py" research/tb24_haltedauern/auswertung.py
cp "$TMPDIR/embargo_neun.py" research/faltenplan_neun/embargo_neun.py
cp "$TMPDIR/tb176a_probe_leser.py" docs/belege/TB-176a/tb176a_probe_leser.py
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_probe_leser.py > docs/belege/TB-176a/e2_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/e2_probe.txt
trading-env/bin/python3 -B research/tb24_haltedauern/test_haltedauer_kern.py > docs/belege/TB-176a/e2_test.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/e2_test.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py nachher2 > docs/belege/TB-176a/e2_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/e2_nachher.txt
```

Soll: `e2_probe.txt` endet mit `Ergebnis: 9 von 9 bestanden` und `rc 0`; `e2_test.txt` mit `Alle Pruefungen bestanden.` und `rc 0`; `e2_nachher.txt` mit `rc 0` (übrige Gruppe und Messung unverändert, zwei Leser = Anhang, Probe = Anhang). **Abbruchweg E2** (eine nicht wie Soll; kein E2-Commit; E bleibt):

```
trading-env/bin/python3 -B -c "import os, shutil, subprocess; b = 'docs/belege/TB-176a/'; ts = ['research/tb24_haltedauern/auswertung.py', 'research/faltenplan_neun/embargo_neun.py']; [shutil.copy(t, b + 'abbruch_' + os.path.basename(t)) for t in ts]; [open(t, 'wb').write(subprocess.run(['git', 'show', 'HEAD:' + t], capture_output=True, check=True).stdout) for t in ts]; open(b + 'abbruch.txt', 'w').write('E2: nicht wie Soll, siehe Belege\nneue Leser nach BEL kopiert, Stand aus HEAD wiederhergestellt\n')"
trading-env/bin/python3 -B -c "import os, subprocess; f = ['docs/belege/TB-176a/' + x for x in ('abbruch.txt', 'abbruch_auswertung.py', 'abbruch_embargo_neun.py', 'tb176a_probe_leser.py', 'e2_probe.txt', 'e2_test.txt', 'e2_nachher.txt')]; d = [x for x in f if os.path.exists(x)]; print('git add', len(d), 'von', len(f)); raise SystemExit(subprocess.run(['git', 'add'] + d).returncode)"
git commit -q -m "TB-176a Abbruch: E2"
git push -q origin main
git status --porcelain
```

Soll danach `git status --porcelain` ohne Ausgabe. Sonst genau diese `git add`, Commit `TB-176a E2: Leser auf alle_trades.csv (auswertung.py, embargo_neun.py; R107 (e), R108 (c))`, pushen:

```
git add research/tb24_haltedauern/auswertung.py
git add research/faltenplan_neun/embargo_neun.py
git add docs/belege/TB-176a/tb176a_probe_leser.py
git add docs/belege/TB-176a/e2_probe.txt
git add docs/belege/TB-176a/e2_test.txt
git add docs/belege/TB-176a/e2_nachher.txt
```


## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ backlog` hängt an Rang 1: Register 68 mit R108 (a) S-B1 10a.5 (äussere Quelle offen), (b) Sammler und Leseregel, (c) 16.6 bleibt 13, D4 unverändert bis zur Neuerzeugung; **offen** (d) Wert und Ort des Startkapitals (TB-176b, Handelscode) und (e) die nachgeholte Prüfung; dazu E2. `WZ kennung`. Block nach `docs/belege/TB-176a/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-176a: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-176a_register68_fable17c_leser.md` mit: Kopf mit Commits; Kurz; Schritt 0 (`0a_md5.txt` wörtlich); V wörtlich (mit den `info`-Zeilen zu R108 (d)); R (`r_eintrag.txt` letzte Zeilen, Marken-Zeilen aus `r_daten.json`); K (rc je Beleg); E2 (letzte Zeilen der drei Belege); offen: R108 (d) und (e), äussere Quelle zu 10a.5; In einfacher Sprache.

```
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py kennung > docs/belege/TB-176a/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-176a/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-176a/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py journal docs/belege/TB-176a/a_block.md --probe > docs/belege/TB-176a/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-176a/tb176a_werkzeug.py journal docs/belege/TB-176a/a_block.md > docs/belege/TB-176a/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-176a/a_journal.txt
```

Soll je `rc 0`. Genau diese `git add`, Commit `TB-176a Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-176a_register68_fable17c_leser.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-176a/a_kennung.txt
git add docs/belege/TB-176a/a_backlog_probe.txt
git add docs/belege/TB-176a/a_backlog.txt
git add docs/belege/TB-176a/a_block.md
git add docs/belege/TB-176a/a_journal_probe.txt
git add docs/belege/TB-176a/a_journal.txt
```

**F.**

```
git status --porcelain > "$TMPDIR/tb176a_f.txt"
cp "$TMPDIR/tb176a_f.txt" docs/belege/TB-176a/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-176a/f_numstat.txt
git add docs/belege/TB-176a/f_porcelain.txt
git add docs/belege/TB-176a/f_numstat.txt
git commit -q -m "TB-176a F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; `f_numstat.txt`: Register und `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` je Spalte 2 = `0`; unter `research/` genau `research/tb24_haltedauern/auswertung.py` und `research/faltenplan_neun/embargo_neun.py`; kein Pfad unter `strategies/`, `shared/`, `data/`, `config/`.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; `WZ md5` nicht `rc 0`; V nicht `rc 0`; `WZ register --probe`/`register` nicht `rc 0` (Abbruch nach `register` vor ⟨R⟩: Register und S-B1 bleiben geändert, nicht zurücksetzen, melden; Abbruch-Commit mit den vorhandenen Belegen wie in TB-173); **kein Abbruch** in K; E2 nicht wie Soll (dann Abbruchweg E2, **kein E2-Commit**); A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Zuerst legt die Sitzung die neue Antwort des Verfahrensprüfers mit Anfrage und Übergabe ins Repo und trägt ihren Regeltext R108 wortgleich ins Register ein, nur angehängt, mit neun Hinweisen an alten Stellen. In die Vorregistrierung des ETF-Vorhabens S-B1 kommt ein datierter Nachtrag: Gold und Silber werden über börsengehandelte Rohstoff-Papiere (ETC) gehandelt, weil es dafür keinen UCITS-Fonds gibt; die äussere Quelle für diesen Grund fehlt noch und ist als offen vermerkt. Gemessen, aber nicht entschieden wird, wo das Startkapital heute steht. Danach rechnen zwei Auswertungen der Haltedauern auf allen gefundenen Trades statt nur auf den ausgeführten. Den Ort des Startkapitals im Code und die nachgeholte Prüfung der Schranke macht ein späterer Auftrag.

## Anhänge


### Anhang A — Werkzeug

<!-- DATEI tb176a_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-176a Werkzeug (Anhang A): Fable 17c ins Register (Abschnitt 68, R108 zeichengleich, neun Marken, 68.2) und in die S-B1-Vorregistrierung (Nachtrag 10a.5, Marke an 10a.2);
Index, Handfelder; Voraussetzungen, Nachher-Pruefung E2, Kennung, BACKLOG, Journal. Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | nachher2 | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, json, os, re, subprocess, sys
P = "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-176a/"
REG, IDX, DI, SB1 = "docs/VORREGISTRIERUNG_neuselektion.md", P + "REGISTER_INDEX.md", P + "FABLE_DIALOG_INDEX.md", "docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md"
AUF, QU = "docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md", "data_sicherung/steuernder_chat_tmp/f17c/"
FA = P + "FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md"
FQ = P + "FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md"
FU = P + "FABLE_UEBERGABE_2026-10-17c_eroeffnung.md"
MD5F = {"docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md": "a2b38226f683d8d106a5dec61fa5f325", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md": "0a559c880aa422ca0d77f03c5aa240bc", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md": "db41d912f05314a47dcc0e501c3aed5a"}
CODE = {"research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/tb24_haltedauern/auswertung.py": "c15e6375520e1aeccc41ce152ca3b870", "research/tb24_haltedauern/haltedauer_kern.py": "60942de99b323fa472ae25478a5a6836", "research/tb24_haltedauern/live_haltedauern.py": "7d21a66cd3173a99adff2c9c1346c815", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/test_haltedauer_kern.py": "a482804dde0c24499cef3d972995bb2a", "research/faltenplan_neun/embargo_neun.py": "b93af14604112c427ab1a3f1606fccc6", "research/faltenplan_neun/test_faltenplan_neun.py": "ae43038a02e7b4ad603c116f1683ffe0", "research/mtm_drawdown/grundlage.py": "81cf1c93243a8248b96cf072e07fc289", "research/mtm_drawdown/messung.py": "00eb23079f1b92532f48f099f74dbe2f", "research/mtm_drawdown/test_mtm_kern.py": "80f1511a18d26a61537748c2739d0d79", "research/wf_kapital_dd/messung.py": "94c091f4c4e13ff4aa2e867dd4fd4fa5"}
NEU_E2 = {"research/tb24_haltedauern/auswertung.py": "9de89e6d302454686f490e151237313011993150f2a120acc0bf879e5331d14b", "research/faltenplan_neun/embargo_neun.py": "f35119ba4b89494d211023c598835640d179f5586c566bc732e5a77c49cc6348"}
PROBE_E2, PSHA = BEL + "tb176a_probe_leser.py", "e99c4664e79ac36a756ab3bce04e0a9c0290a265e8b7249553518555323b8cf0"
STAND_D = "7fe6342"
BOTS = ["elliott_wave", "elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion", "t3_supertrend", "turtle_soup_crypto", "turtle_soup_stocks", "volatility_breakout", "volatility_breakout_crypto"]
RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R108)"
TITEL = "## 68. Fable 17c — Registerblock R108 (TB-176a)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | zg | ende, Kopf der Marke, Zusatz) - R108 (f); folgende Marken-Tripel am Ort werden uebersprungen
MARKEN = [("62.2", "### 62.2 ", "quelle", "62.2 R101 ERGÄNZT und BERICHTIGT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (a): ERGÄNZT zu (a) bis (c), BERICHTIGT zu (a) („lies“)"),
          ("16.4", "### 16.4 ", "ende", "16.4 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (b)"),
          ("16.6", "### 16.6 ", "zg", "16.6 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (c)"),
          ("16.8", "### 16.8 ", "ende", "16.8 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (b)"),
          ("29.3", "### 29.3 ", "ende", "29.3 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (d)"),
          ("37.5", "### 37.5 ", "ende", "37.5 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (d)"),
          ("41.3 C2", "### 41.3 ", "zg", "41.3 C2 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (c)"),
          ("66.1", "### 66.1 ", "quelle", "66.1 R106 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (e)"),
          ("67.1", "### 67.1 ", "quelle", "67.1 R107 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkte (b) bis (e)")]
MARKE_SB1 = "S-B1 10a.2 ERGÄNZT durch 10a.5"
OHNE = "15.4, 17.1, 24.3, 37.3, 38.5, 40.7, 41.1, 41.2, 58.4, 58.5, 62.5, 66.2, Abschnitt 10, S-B1 2, 3.2, 9, 10a.4"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def info(t): OUT.append("info  " + t)
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (sum(not l.startswith("info") for l in OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def beleg(n): return lies(BEL + n).rstrip("\n").split("\n") if os.path.exists(BEL + n) else [""]
def block():
    """((R-Zeile, Quellenzeile), Z. Zaun auf, Z. Zaun zu) oder None."""
    z = lies(FA if os.path.exists(FA) else QU + os.path.basename(FA)).split("\n")
    if z.count(KOPF_A) != 1: return None
    a = z.index(KOPF_A) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [z[i] for i in range(a + 1, e) if z[i]]; soll = ["R108 — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for l, s in zip(b, soll)] != soll: return None
    return (b[0], b[1]), a + 1, e + 1
def wortlaut(r):
    m = re.findall(r"Wortlaut: „(.*?)“ Der Grund trägt", r); return m[0] if len(m) == 1 else None
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m, frei="R108"):
    """Index der Einfuegestelle (vor dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any(frei in z[i] for i in range(a, e)): return None
    if m[2] == "zg": k = [i for i in range(a, e) if z[i] == ZG][-1:]
    elif m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    else:
        j = e - 1
        while j > a and z[j] in ("", "---"): j -= 1
        k = [j] if j > a else []
    if len(k) != 1: return None
    k = k[0]
    while k + 3 < e and z[k + 1] == "" and z[k + 2].startswith("> ⭐ ") and z[k + 3] == ZG: k += 3
    return k + 1
def c2_ok(z, i):
    c2 = [n for n, l in enumerate(z) if l.startswith("**C2 (b) — Deckel")]; c3 = [n for n, l in enumerate(z) if l.startswith("**C3 (c) — ")]
    return len(c2) == 1 and len(c3) == 1 and c2[0] < i < c3[0]
def markenzeilen(kopf, zusatz, datum): return ["", "> ⭐ **%s** (%s, TB-176a, %s)." % (kopf, zusatz, datum), ZG]
def sb1_stellen(s):
    """(Einfuegestelle Marke 10a.2, Einfuegestelle 10a.5) oder (None, None)."""
    if any(l.startswith("### 10a.5") for l in s) or any("R108" in l for l in s) or sum(l.startswith("## 11. ") for l in s) != 1: return None, None
    a, e = unterabschnitt(s, "### 10a.2 "); b, f = unterabschnitt(s, "### 10a.4 ")
    if a is None or b is None or not s[f].startswith("## 11. "): return None, None
    return einfuege(s, (None, "### 10a.2 ", "ende")), einfuege(s, (None, "### 10a.4 ", "ende"))
def mess_d():
    """R108 (d): Werte des Startkapitals im Register am Stand 7fe6342 und in den neun equity_simulation.py (nur Messung)."""
    r = git("show", STAND_D + ":" + REG); z = r.stdout.decode("utf-8").split("\n") if r.returncode == 0 else []
    kopf, reg = "?", []
    for i, l in enumerate(z):
        if l.startswith("## ") or l.startswith("### "): kopf = l.split(" ")[1]
        for m in re.finditer(r"(Startkapital|STARTING_CAPITAL)[`\s  =:]*\d[\d\s  .,_]*", l): reg.append((i + 1, kopf, l[max(0, m.start() - 40):m.end() + 30].strip()))
    sim = []
    for b in BOTS:
        f = "strategies/%s/equity_simulation.py" % b; t = lies(f).split("\n") if os.path.exists(f) else []
        w = [(i + 1, re.match(r"STARTING_CAPITAL\s*=\s*([^#]+)", l).group(1).strip()) for i, l in enumerate(t) if re.match(r"STARTING_CAPITAL\s*=", l)]
        sim.append((f, w))
    return r.returncode == 0, reg, sim
def code_gleich(ausser=()):
    for f, m in sorted(CODE.items()):
        if f not in ausser: p(md5f(f) == m, "unveraendert: %s md5 %s" % (f, m[:12]))
def voraussetzung():
    code_gleich()
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-176a" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-176a")
    k = kennungen(); p(max(k) in ("FL", "FM"), "Journal: hoechste %s (FL am Bau-HEAD)" % max(k))
    for f in (FA, FQ, FU): p(verfolgt_gleich(f) and md5f(f) == MD5F[f], "R56 (b)/S0-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5F[f]))
    b = block(); p(b is not None, "Registerblock 17c: genau R108 und Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[1], b[2]) if b else "?"))
    p(b is not None and wortlaut(b[0][0]) is not None, "R108 (a): Wortlaut 10a.5 genau einmal zwischen „Wortlaut: „“ und „“ Der Grund trägt“")
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 67. ") for l in z) == 1 and not any(l.startswith("## 68. ") for l in z) and not re.search(r"\bR108\b", reg), "Register: 67 da, 68 nicht; R108 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for m in MARKEN:
        i = einfuege(z, m); p(i is not None and (m[0] != "41.3 C2" or c2_ok(z, i)), "Ort %s: Einfuegestelle vor Z. %s eindeutig, R108 dort noch nicht genannt" % (m[0], i + 1 if i else "?"))
    s = lies(SB1).split("\n"); i1, i2 = sb1_stellen(s)
    p(i1 is not None and i2 is not None and i1 < i2, "S-B1: 10a.2 und 10a.4 je einmal, 10a.5 nicht, R108 nicht; Marke vor Z. %s, 10a.5 vor Z. %s" % (i1 and i1 + 1, i2 and i2 + 1))
    zi = lies(IDX).split("\n"); k = [i for i, l in enumerate(zi) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    p(len(k) == 1 and "Abschnitte 0–67" in zi[k[0]], "Index-Kopf Z. %s nennt 0–67" % (k[0] + 1 if k else "?"))
    p(sum(l.startswith("| 67 aus 17b |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-175 (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and not any(l.startswith("## 19. ") for l in zi), "Index: Zeile 67, Pflegezeile TB-175, Pflege-Anker je genau einmal; kein Abschnitt 19")
    p(not any(l.startswith("| 17c |") for l in lies(DI).split("\n")), "Dialog-Index: 17c noch nicht")
    ok, reg_d, sim = mess_d(); p(ok, "R108 (d): Register am Stand %s lesbar (git show)" % STAND_D)
    info("R108 (d) Voraussetzung (Messung, kein Urteil): Register am Stand %s nennt einen Wert des Startkapitals an %d Stelle(n)%s" % (STAND_D, len(reg_d), ":" if reg_d else ""))
    for n, kp, t in reg_d: info("  Z. %d (%s): %s" % (n, kp, t))
    for f, w in sim: info("R108 (d) Wert: %s %s" % (f, "; ".join("Z. %d STARTING_CAPITAL = %s" % x for x in w) or "kein STARTING_CAPITAL"))
    werte = set(v for _f, w in sim for _n, v in w); info("R108 (d): neun Dateien, %s" % ("alle denselben Wert %s" % werte.pop() if len(werte) == 1 and all(len(w) == 1 for _f, w in sim) else "NICHT derselbe Wert (Befund an 29.3): %s" % sorted(werte)))
    ende()
def md5cmd():
    for f in (FA, FQ, FU): p(md5f(QU + os.path.basename(f)) == MD5F[f] and md5f(f) == MD5F[f], "md5 vorher %s = nachher %s = %s" % (QU + os.path.basename(f), f, MD5F[f]))
    ende()
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg_v, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); salt = lies(SB1); s = salt.split("\n"); va = lies(beleg_v).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg_v)
    b = block(); p(b is not None and md5f(FA) == MD5F[FA], "Quelle md5 %s, Registerblock R108" % MD5F[FA])
    w = wortlaut(b[0][0]) if b else None; p(w is not None, "Wortlaut 10a.5 aus R108 (a) gelesen")
    p(not any(l.startswith("## 68. ") for l in z) and z[-1] == "" and z[-2] != "", "68 noch nicht im Register; endet mit einer Leerzeile")
    einf = [(einfuege(z, m), m) for m in MARKEN]; p(all(i is not None for i, _ in einf) and len(set(i for i, _ in einf)) == len(MARKEN) and c2_ok(z, [i for i, m in einf if m[0] == "41.3 C2"][0] or 0), "%d Einfuegestellen eindeutig (41.3 zwischen C2 und C3)" % len(MARKEN))
    i1, i2 = sb1_stellen(s); p(i1 is not None and i2 is not None and i1 < i2, "S-B1: Einfuegestellen Marke 10a.2 und 10a.5 eindeutig")
    k = karte(); p(k is not None, "Karte TB-176a gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    (r, q), za, ze = b
    ok, reg_d, sim = mess_d(); werte = sorted(set(v for _f, ww in sim for _n, v in ww))
    kopf = ("Reines Eintragen von Registertext, Bauart wie 67. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R108)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.c (`%s`) und die Übergabe 17.10.c (`%s`), beide seit `%s`. Marken nach R108 (f); "
            "der datierte Nachtrag 10a.5 nach R108 (a) steht in `%s`. Karte des Betreibers (Auftrag TB-176a, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-176a.") % (
            FA, MD5F[FA], format(os.path.getsize(FA), ",").replace(",", " "), za, ze, s0, FQ, FU, s0, SB1, k, datum)
    kette = ("**Kette:** Marken nach R108 (f): 62.2 (R101), Unterpunkt (a), ergänzt und berichtigt; 16.4 und 16.8, Unterpunkt (b); 16.6 und 41.3 C2, Unterpunkt (c); 29.3 und 37.5, Unterpunkt (d); 66.1 (R106), Unterpunkt (e); "
             "67.1 (R107), Unterpunkte (b) bis (e); S-B1-Vorregistrierung 10a.2, ergänzt durch den Nachtrag 10a.5 (Unterpunkt (a)). Ohne Marke: " + OHNE + ". Zählung: kein Fall; sechzehn (R108 (f)). "
             "Nicht mit TB-176a: Wert und Ort des Startkapitals (R108 (d) (1) bis (3)) und die nachgeholte Prüfung nach R108 (e) (BACKLOG Rang 1).")
    neu = ["", TITEL, "", kopf, "", "### 68.1 " + titel(r), "", "> " + r, "> " + q, "", kette, ""]
    neu += ["### 68.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-176a), Zeilen wörtlich:" % beleg_v, ""] + ["    " + l for l in vb] + ["",
        ("(a) R108 (d), die zwei Voraussetzungen (nur das Ob), gemessen durch Lesen: Das Register am Stand `%s` nennt einen Wert des Startkapitals an %d Stelle(n)%s. Die neun `strategies/<bot>/equity_simulation.py` tragen %s (Fundstellen je Datei oben). "
         "Ob eine genannte Stelle der Ort im Sinn von R108 (d) und 37.5 ist, ist hier nicht entschieden; Wert und Ort werden mit TB-176a nicht eingetragen.") % (
         STAND_D, len(reg_d), (": " + "; ".join("Z. %d (%s)" % (n, kp) for n, kp, _t in reg_d)) if reg_d else "", ("denselben Wert `%s`" % werte[0]) if len(werte) == 1 else ("verschiedene Werte %s" % werte)), "",
        "(b) R108 (a): Der Nachtrag 10a.5 steht im Wortlaut aus R108 (a) in `%s`; die Tatsachennotiz mit äusserer Quelle und Datum (kein UCITS-Fonds auf ein einzelnes Edelmetall) liegt im Repo nicht vor und ist nicht eingetragen." % SB1, "",
        "(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.c liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `%s0a_md5.txt`)." % (s0, QU, BEL), ""]
    s10a5 = ["", "### 10a.5 Nachtrag vom %s — Ergänzung zu Registertext 3 (10a.2) (R108 (a), TB-176a)" % datum, "", "> " + w, "",
             "*Quelle: R108 (a) (Register `%s`, Abschnitt 68.1), Fable-Antwort 17.10.c (`%s`, md5 `%s`). 10a.2 bleibt zeichengleich (Marke dort). Die Tatsachennotiz mit äusserer Quelle und Datum ist nicht eingetragen (68.2 (b)).*" % (REG, FA, MD5F[FA])]
    if probe: print("\n".join(neu + ["", "--- S-B1 ---"] + markenzeilen(MARKE_SB1, "Fable 17c R108 (68.1), Unterpunkt (a)", datum) + s10a5)); ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m[3], m[4], datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    s[i2:i2] = s10a5; s[i1:i1] = markenzeilen(MARKE_SB1, "Fable 17c R108 (68.1), Unterpunkt (a)", datum); schreibe(SB1, "\n".join(s))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s**" % m[3])] for m in MARKEN}
    s2 = lies(SB1).split("\n"); ms = [i + 1 for i, l in enumerate(s2) if l.startswith("> ⭐ **%s**" % MARKE_SB1)]; n5 = [i + 1 for i, l in enumerate(s2) if l.startswith("### 10a.5 ")]
    json.dump({"marken": [[m[0], m[3], (mz[m[0]] or [0])[0]] for m in MARKEN], "abschnitt_68": r2.index(TITEL) + 1, "sb1_marke": (ms or [0])[0], "sb1_10a5": (n5 or [0])[0]}, open(os.path.dirname(beleg_v) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: %d Marken Z. %s; Abschnitt 68 Z. %d" % (len(MARKEN), sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "R108 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al):] == neu, "Register append-only bis auf die %d Marken (je Leerzeile, Marke, Zeichengleich-Zeile)" % len(MARKEN))
    weg = set(x for n in ms for x in (n - 1, n, n + 1)) | set(range(n5[0] - 1, n5[0] - 1 + len(s10a5))) if len(ms) == 1 and len(n5) == 1 else set()
    p(len(ms) == 1 and len(n5) == 1 and [l for i, l in enumerate(s2) if i + 1 not in weg] == salt.split("\n") and s2.count("> " + w) == 1 and w in r,
      "S-B1: Marke Z. %s, 10a.5 Z. %s; sonst zeichengleich; Wortlaut = R108 (a)" % (ms, n5))
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 68. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) == len(MARKEN) and all(m[2] for m in mk) and d["sb1_marke"] and d["sb1_10a5"], "Abschnitt 68 in genau einer Teildatei: T%s; %d Marken mit Zeile; S-B1 Marke und 10a.5" % (teil, len(mk))); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]; rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–67" in z[k[0]], "Kopf genau einmal, nennt 0–67"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–67", "Abschnitte 0–68")
    i = [j for j, l in enumerate(z) if l.startswith("| 67 aus 17b |")]
    if p(len(i) == 1, "Zeile 67 genau einmal"): z.insert(i[0] + 1, "| 68 aus 17c | %s | R108 (68.1); 68.2 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 19. Die Marken aus Fable 17c (TB-176a)", "", "Alle %d Marken, die TB-176a nach R108 (f) im Register gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-176a/r_daten.json`." % len(mk), "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, T) for o, kp, n in sorted(mk, key=lambda m: m[2])] + ["",
           "Dazu in `%s`: Marke an 10a.2 (Z. %d, „%s“) und der datierte Nachtrag 10a.5 (Z. %d), R108 (a). Der Index ist kein Registertext." % (SB1, d["sb1_marke"], MARKE_SB1, d["sb1_10a5"]), ""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 19. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 19"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-175 (")]
    if p(len(j) == 1, "Pflegezeile TB-175 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-175 (", "In TB-175 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-176a (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-176a (`index`); 68 (R108) kommt zu T%s; neuer Abschnitt 19 (%d Marken, S-B1 10a.2/10a.5)." % (datum, s0, rcm, T, len(mk)))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"17c": {"frage": lies(FQ).split("\n")[0].split(" — ", 1)[-1].strip(),
                       "entscheidung": "(a) einverstanden: S-B1 10a.5 (Gold/Silber als ETC, äussere Quelle nötig), USD/EZB-Referenzkurs, Wochenrenditen; (b) einverstanden: Sammler mit vier Ergänzungen, Leseregel nach 24.3; (c) 16.6 bleibt 13 bis zur Herleitung mit R44, D4 Mechanikprobe; (d) anders: erst Wert und Ort des Startkapitals (37.5), dann die Leser; (e) anders: Prüfung mit gegen ohne Schranke nachholen (R108)",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17c geschrieben: %s" % ziel)
def nachher2():
    code_gleich(ausser=tuple(NEU_E2))
    for f, s in sorted(NEU_E2.items()):
        p(sha(f) == s, "E2 umgestellt: %s = Anhang (sha256 %s)" % (f, s[:12]))
        p(not re.search(r"STARTING_CAPITAL|startkapital", lies(f), re.I), "R108 (d) (2): %s liest kein Startkapital" % f)
    p(sha(PROBE_E2) == PSHA, "Probe E2 = Anhang E")
    pr, te = beleg("e2_probe.txt"), beleg("e2_test.txt")
    p(pr[-2:] == ["Ergebnis: 9 von 9 bestanden", "rc 0"], "e2_probe.txt: 9 von 9, rc 0")
    p(te[-2:] == ["Alle Pruefungen bestanden.", "rc 0"] and any("Gegenprobe 13: auswertung.py schreibt neben ERGEBNIS_DIR -> auswertung.py faellt auf" in l for l in te), "e2_test.txt: Test am neuen auswertung.py gruen, Gegenprobe trifft")
    ende()
BL_TEXT = (" · **Register 68 (Fable 17c, R108) mit TB-176a (%s, Journal %s)**: R108 (a) S-B1 Nachtrag 10a.5 im Wortlaut (Gold/Silber als ETC), Marke an 10a.2, **Tatsachennotiz mit äusserer Quelle und Datum offen**; "
    "Währung USD mit EZB-Referenzkurs, Wochenrenditen; (b) Sammler mit vier Ergänzungen, Leseregel nach 24.3, Auswerteplan vor der ersten Auswertung an den Verfahrensprüfer; (c) 16.6 bleibt 13 bis zur Herleitung aus den neuen Listen (R44), "
    "D4 unverändert bis zur Neuerzeugung, Mechanikprobe auf Beispieldaten; **offen: (d) Startkapital Wert und Ort (TB-176b, Handelscode, nach der Frage zur Voraussetzung, 68.2 (a))** und **(e) nachgeholte Prüfung mit gegen ohne Schranke "
    "(t3_supertrend, zwei Elliott-Bots)**; E2 mit TB-176a: `auswertung.py` und `embargo_neun.py` lesen `<bot>_alle_trades.csv` (R107 (e)) |")
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-176a" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-176a"):
        z[a[0]] = z[a[0]][:-2] + BL_TEXT % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-176a: " % neu), "Kopfzeile ## %s — TB-176a: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["md5"]: md5cmd()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["nachher2"]: nachher2()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

### Anhang B — `research/tb24_haltedauern/auswertung.py` (vollständig, ersetzt die Datei)

<!-- DATEI auswertung.py -->
````python
"""
Auswertung: Haltedauern, Ueberlappungsmatrix, Einordnung (TB-24)
==============================================================================
Liest je Bot `daten/<bot>_alle_trades.csv` und `daten/<bot>_meta.json`
(erzeugt von `positionen_holen.py`) und rechnet auf ALLEN gefundenen Trades
(R107 (e), TB-176a): kein Filter auf ausgefuehrte Positionen, keine Eingabe
aus trades_ausgefuehrt, allocation oder capital_after. Die Gegenprobe zum
Positionslimit (ausgefuehrt gegen alle) ist damit entfallen. Schreibt alle
Tabellen des Berichts nach `ergebnisse/`. Rechnet ausschliesslich mit den
Funktionen aus `haltedauer_kern.py`.

**Liest nur.** Es wird keine Bot-Datei und nichts unter `results/` angefasst.

Nutzung:
    python3 auswertung.py
"""

import itertools
import json
import os

import pandas as pd

import haltedauer_kern as k

_DIR = os.path.dirname(os.path.abspath(__file__))
DATEN_DIR = os.path.join(_DIR, "daten")
ERGEBNIS_DIR = os.path.join(_DIR, "ergebnisse")
os.makedirs(ERGEBNIS_DIR, exist_ok=True)

BOTS = [
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
]

# Zuordnung Bot -> Ertragsquelle. Das ist eine LESART, keine Messung, und
# deshalb hier offen hingeschrieben statt im Text versteckt. Grundlage sind
# die Einstiegsregeln aus Uebergabeprotokoll Abschnitt 3:
#   trend      - handelt die Fortsetzung einer Bewegung (T3-Crossover,
#                Bollinger-Ausbruch)
#   umkehr     - handelt die Rueckkehr zu einem Mittelwert bzw. das
#                Scheitern eines Ausbruchs (RSI-2 unter Schwelle,
#                False-Breakout an Donchian-Extremen)
#   muster     - handelt ein abgeschlossenes Wellenmuster und erwartet die
#                Gegenbewegung. Das ist der Sache nach gegen den vorherigen
#                Trend gerichtet, aber weder ein Mittelwert-Ruecklauf noch
#                eine Ausbruchsfortsetzung; die externe Analyse mit ihrer
#                Zaehlung "vier Trendfolge, vier Mean-Reversion" muss einen
#                der beiden Elliott-Bots anders eingeordnet haben als hier.
#                Die Abweichung ist benannt, nicht aufgeloest.
ERTRAGSQUELLE = {
    "elliott_wave": "muster",
    "t3_supertrend": "trend",
    "rsi2_crypto": "umkehr",
    "turtle_soup_crypto": "umkehr",
    "volatility_breakout_crypto": "trend",
    "elliott_wave_stocks": "muster",
    "rsi2_mean_reversion": "umkehr",
    "turtle_soup_stocks": "umkehr",
    "volatility_breakout": "trend",
}

HIST_KANTEN = [0, 1, 2, 3, 5, 8, 11, 16, 21, 31, 61, 91]


def lade(bot: str) -> pd.DataFrame:
    """Alle gefundenen Trades des Bots (R107 (e)); eine Spalte `ausgefuehrt`
    aus aelteren Listen wird nicht ausgewertet."""
    pfad = os.path.join(DATEN_DIR, f"{bot}_alle_trades.csv")
    return pd.read_csv(pfad, parse_dates=["entry_time", "exit_time"])


def lade_meta(bot: str) -> dict:
    with open(os.path.join(DATEN_DIR, f"{bot}_meta.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 1. Haltedauern je Bot
# ---------------------------------------------------------------------------

def tabelle_haltedauern(positionen: dict, meta: dict) -> pd.DataFrame:
    zeilen = []
    for bot in BOTS:
        p = positionen[bot]
        kz = k.kennzahlen(k.haltedauer_tage(p))
        ker = k.kennzahlen(p["kerzen"])
        zeilen.append({
            "bot": bot,
            "anlageklasse": meta[bot]["anlageklasse"],
            "zeitrahmen": meta[bot]["zeitrahmen"],
            "ertragsquelle": ERTRAGSQUELLE[bot],
            "n": kz["n"],
            "tage_min": round(kz["min"], 2),
            "tage_p10": round(kz["p10"], 2),
            "tage_q1": round(kz["q1"], 2),
            "tage_median": round(kz["median"], 2),
            "tage_q3": round(kz["q3"], 2),
            "tage_p90": round(kz["p90"], 2),
            "tage_max": round(kz["max"], 2),
            "tage_mittel": round(kz["mittel"], 2),
            "kerzen_median": round(ker["median"], 1),
            "kerzen_q1": round(ker["q1"], 1),
            "kerzen_q3": round(ker["q3"], 1),
            "horizont_klasse": k.horizont_klasse(kz["median"]),
        })
    return pd.DataFrame(zeilen)


def tabelle_ausstiegsarten(positionen: dict) -> pd.DataFrame:
    zeilen = []
    for bot in BOTS:
        p = positionen[bot]
        gesamt = len(p)
        for art, kz in sorted(k.kennzahlen_je_ausstiegsart(p).items(),
                               key=lambda kv: -kv[1]["n"]):
            zeilen.append({
                "bot": bot, "ausstiegsart": art, "n": kz["n"],
                "anteil_pct": round(100 * kz["n"] / gesamt, 1),
                "tage_p10": round(kz["p10"], 2), "tage_q1": round(kz["q1"], 2),
                "tage_median": round(kz["median"], 2), "tage_q3": round(kz["q3"], 2),
                "tage_p90": round(kz["p90"], 2), "tage_max": round(kz["max"], 2),
            })
    return pd.DataFrame(zeilen)


def tabelle_histogramm(positionen: dict) -> pd.DataFrame:
    spalten = {}
    for bot in BOTS:
        spalten[bot] = k.histogramm(k.haltedauer_tage(positionen[bot]), HIST_KANTEN)
    return pd.DataFrame(spalten)


def tabelle_zweigipfligkeit(positionen: dict) -> pd.DataFrame:
    zeilen = []
    for bot in BOTS:
        z = k.zweigipfligkeit(positionen[bot])
        zeilen.append({
            "bot": bot,
            "ausstiegsarten": len(z["arten"]),
            "zwei_gruppen": z["zwei_gruppen"],
            "verglichen": " / ".join(z.get("vergleich", [])),
            "begruendung": z["begruendung"],
        })
    return pd.DataFrame(zeilen)


# ---------------------------------------------------------------------------
# 2. Ueberlappung
# ---------------------------------------------------------------------------

def tabelle_ueberlappung(positionen: dict, meta: dict) -> pd.DataFrame:
    zeilen = []
    for a, b in itertools.permutations(BOTS, 2):
        u = k.ueberlappung(positionen[a], positionen[b])
        zeilen.append({
            "bot_a": a, "bot_b": b,
            "gleiche_anlageklasse": meta[a]["anlageklasse"] == meta[b]["anlageklasse"],
            "fenster_von": u["gemeinsames_fenster"][0] if u["gemeinsames_fenster"] else None,
            "fenster_bis": u["gemeinsames_fenster"][1] if u["gemeinsames_fenster"] else None,
            "positionstage_a": u["tage_a"], "positionstage_b": u.get("tage_b"),
            "titeltage_a": u["titeltage_a"],
            "anteil_tage_pct": None if u["anteil_tage"] is None else round(100 * u["anteil_tage"], 1),
            "anteil_titel_pct": None if u["anteil_titel"] is None else round(100 * u["anteil_titel"], 2),
        })
    return pd.DataFrame(zeilen)


def tabelle_naehe(positionen: dict, meta: dict, zufallslaeufe: int = 200) -> pd.DataFrame:
    """Nur Paare derselben Anlageklasse: ueber Anlageklassen hinweg gibt es
    kein gemeinsames Symbol, die Zahl waere per Konstruktion 0."""
    zeilen = []
    for a, b in itertools.permutations(BOTS, 2):
        if meta[a]["anlageklasse"] != meta[b]["anlageklasse"]:
            continue
        n = k.naehe(positionen[a], positionen[b], zufallslaeufe=zufallslaeufe)
        analytisch = k.naehe_erwartet_analytisch(positionen[a], positionen[b])
        zeilen.append({
            "bot_a": a, "bot_b": b,
            "einstiege_a": n["einstiege_a"], "einstiege_b": n["einstiege_b"],
            "gemeinsame_symbole": n["gemeinsame_symbole"],
            "treffer": n["treffer"],
            "anteil_pct": None if n["anteil"] is None else round(100 * n["anteil"], 1),
            "zufall_pct": None if n["anteil_zufall"] is None else round(100 * n["anteil_zufall"], 1),
            "zufall_analytisch_pct": round(100 * analytisch, 1) if analytisch == analytisch else None,
            "ueberschuss": None if n["ueberschuss"] is None else round(n["ueberschuss"], 2),
        })
    return pd.DataFrame(zeilen)


def tabelle_versatz(positionen: dict, meta: dict) -> pd.DataFrame:
    """Verteilung des Versatzes zwischen den Einstiegen zweier Bots im selben
    Titel. Nur Paare derselben Anlageklasse (sonst kein gemeinsames Symbol)."""
    zeilen = []
    for a, b in itertools.permutations(BOTS, 2):
        if meta[a]["anlageklasse"] != meta[b]["anlageklasse"]:
            continue
        v = k.versatz_verteilung(positionen[a], positionen[b])
        if v["n"] == 0:
            continue
        zeile = {
            "bot_a": a, "bot_b": b,
            "einstiege_a": v["einstiege_a"], "mit_b_im_titel": v["n"],
            "median_versatz_tage": round(v["median_versatz"], 1),
            "median_versatz_bis_30_tage": round(v["median_versatz_bis_30_tage"], 1),
            "anteil_bis_3_tage_pct": round(100 * v["anteil_bis_3_tage"], 1),
        }
        zeile.update({f"n[{name}]": anzahl for name, anzahl in v["histogramm"].items()})
        zeile["n[< -30]"] = v["unter_minus_30"]
        zeile["n[>= 30]"] = v["ueber_plus_30"]
        zeilen.append(zeile)
    return pd.DataFrame(zeilen)


# ---------------------------------------------------------------------------
# 3. Einordnung
# ---------------------------------------------------------------------------

def einordnung(haltedauern: pd.DataFrame, ueber: pd.DataFrame, naehe_df: pd.DataFrame,
                versatz: pd.DataFrame) -> dict:
    klassen = {}
    for name, _von, _bis in k.HORIZONT_KLASSEN:
        teil = haltedauern[haltedauern["horizont_klasse"] == name]
        klassen[name] = {
            "bots": list(teil["bot"]),
            "anzahl": int(len(teil)),
            "ertragsquellen": sorted(set(teil["ertragsquelle"])),
        }

    fenster_3_10 = klassen["3 bis 10 Tage"]
    gleiche_klasse = ueber.merge(
        haltedauern[["bot", "horizont_klasse"]].rename(
            columns={"bot": "bot_a", "horizont_klasse": "klasse_a"}), on="bot_a")
    gleiche_klasse = gleiche_klasse.merge(
        haltedauern[["bot", "horizont_klasse"]].rename(
            columns={"bot": "bot_b", "horizont_klasse": "klasse_b"}), on="bot_b")

    return {
        "vermutung": {
            "wortlaut": ("Sechs der neun haben Median-Haltedauern zwischen drei und "
                          "zehn Tagen und bespielen ein Fenster."),
            "bots_im_fenster_3_bis_10": fenster_3_10["bots"],
            "anzahl": fenster_3_10["anzahl"],
            "trifft_zu": fenster_3_10["anzahl"] == 6,
        },
        "horizont_klassen": klassen,
        "median_spanne_tage": [float(haltedauern["tage_median"].min()),
                                float(haltedauern["tage_median"].max())],
        "staerkstes_paar_titeltage": ueber.sort_values("anteil_titel_pct", ascending=False)
            .head(1).to_dict("records"),
        "staerkstes_paar_naehe": naehe_df.sort_values("ueberschuss", ascending=False)
            .head(1).to_dict("records"),
        "schwaechstes_paar_naehe": naehe_df[naehe_df["ueberschuss"].notna()]
            .sort_values("ueberschuss").head(1).to_dict("records"),
        "paare_gleiche_klasse_und_quelle": int(len(gleiche_klasse[
            (gleiche_klasse["klasse_a"] == gleiche_klasse["klasse_b"])
            & (gleiche_klasse["bot_a"].map(ERTRAGSQUELLE)
               == gleiche_klasse["bot_b"].map(ERTRAGSQUELLE))])),
        "groesster_versatz": versatz.reindex(
            versatz["median_versatz_bis_30_tage"].abs().sort_values(ascending=False).index
        ).head(3).to_dict("records"),
    }


def main():
    positionen = {bot: lade(bot) for bot in BOTS}
    meta = {bot: lade_meta(bot) for bot in BOTS}

    haltedauern = tabelle_haltedauern(positionen, meta)
    ausstiegsarten = tabelle_ausstiegsarten(positionen)
    hist = tabelle_histogramm(positionen)
    zwei = tabelle_zweigipfligkeit(positionen)
    print("Ueberlappungsmatrix (72 geordnete Paare) - das dauert etwa eine Minute ...",
          flush=True)
    ueber = tabelle_ueberlappung(positionen, meta)
    naehe_df = tabelle_naehe(positionen, meta)
    versatz = tabelle_versatz(positionen, meta)

    haltedauern.to_csv(os.path.join(ERGEBNIS_DIR, "haltedauern_je_bot.csv"), index=False)
    ausstiegsarten.to_csv(os.path.join(ERGEBNIS_DIR, "haltedauern_je_ausstiegsart.csv"), index=False)
    hist.to_csv(os.path.join(ERGEBNIS_DIR, "haltedauern_histogramm.csv"))
    zwei.to_csv(os.path.join(ERGEBNIS_DIR, "verteilungsform.csv"), index=False)
    ueber.to_csv(os.path.join(ERGEBNIS_DIR, "ueberlappungsmatrix.csv"), index=False)
    naehe_df.to_csv(os.path.join(ERGEBNIS_DIR, "naehe_der_einstiege.csv"), index=False)
    versatz.to_csv(os.path.join(ERGEBNIS_DIR, "versatz_der_einstiege.csv"), index=False)

    zusammenfassung = einordnung(haltedauern, ueber, naehe_df, versatz)
    zusammenfassung["datenbasis"] = {
        bot: {
            "zeitrahmen": meta[bot]["zeitrahmen"],
            "anlageklasse": meta[bot]["anlageklasse"],
            "trades_gefunden": meta[bot]["trades_gefunden"],
            "symbole_gefunden": meta[bot]["symbole_gefunden"],
            "erster_einstieg": meta[bot]["erster_einstieg"][:10],
            "letzter_ausstieg": meta[bot]["letzter_ausstieg"][:10],
        } for bot in BOTS
    }
    with open(os.path.join(ERGEBNIS_DIR, "zusammenfassung.json"), "w") as f:
        json.dump(zusammenfassung, f, indent=2, ensure_ascii=False)

    print("\n--- Haltedauern (Kalendertage, alle gefundenen Trades) ---")
    print(haltedauern[["bot", "zeitrahmen", "n", "tage_p10", "tage_q1", "tage_median",
                        "tage_q3", "tage_p90", "kerzen_median",
                        "horizont_klasse"]].to_string(index=False))
    v = zusammenfassung["vermutung"]
    print(f"\nVermutung '{v['wortlaut']}'")
    print(f"  -> {v['anzahl']} Bots im Fenster 3 bis 10 Tage: {', '.join(v['bots_im_fenster_3_bis_10'])}")
    print(f"  -> trifft_zu = {v['trifft_zu']}")
    print(f"\nMedian-Spanne aller neun Bots: "
          f"{zusammenfassung['median_spanne_tage'][0]:.2f} bis "
          f"{zusammenfassung['median_spanne_tage'][1]:.2f} Kalendertage")
    print(f"\n{len(os.listdir(ERGEBNIS_DIR))} Dateien in ergebnisse/ geschrieben.")


if __name__ == "__main__":
    main()
````

### Anhang C — `research/faltenplan_neun/embargo_neun.py` (vollständig, ersetzt die Datei)

<!-- DATEI embargo_neun.py -->
````python
#!/usr/bin/env python3
"""
Das Embargo je Bot - Registertext 2d (TB-36)
==============================================================================
Rein lesend, reine Standardbibliothek. `live_params.py`, `forward_test.py` und
die Backtest-Dateien werden als **Text gelesen**, nie importiert - neun
gleichnamige Module kollidieren in `sys.modules`, und ein Import fuehrte
ausserdem Bot-Code aus, wo nur eine Zahl gebraucht wird.

DIE REGEL (Registertext 2d)
------------------------------------------------------------------------------
    Embargo = laengste Zeitbremse des Bots in Handelstagen + 1
    Bots ohne Zeitbremse: 95. Perzentil der Haltedauer + 1

"Handelstage" heisst bei Krypto Kalendertage - der Markt laeuft durch. Bei
Aktien ist ein Handelstag ein Boersentag; wo eine Zeitbremse in KALENDERtagen
notiert ist, wird die Umrechnung **an der Kursreihe gemessen**, nicht mit
5/7 geschaetzt (Feiertage).

WAS EINE ZEITBREMSE IST - UND WELCHER BOT KEINE HAT
------------------------------------------------------------------------------
Eine Zeitbremse ist der Notausstieg nach fester Zeit: `MAX_HOLD_DAYS` bzw.
`MAX_HOLD_HOURS`. **Acht der neun Bots haben eine**, und das ist nicht
geraten: TB-24 hat es gemessen (`research/tb24_haltedauern/BERICHT.md`,
Abschnitt 1) - "bei jedem der acht Bots mit Zeitausstieg liegt der Median der
Zeitausstiege exakt auf `MAX_HOLD_DAYS` bzw. `MAX_HOLD_HOURS`".

**Ohne Zeitbremse ist genau `t3_supertrend`.** Seine drei Ausstiegsarten sind
`stop_loss`, `trend_flip` und `t3_crossunder` (TB-24,
`daten/t3_supertrend_meta.json`) - keine davon ist eine Uhr. Fuer ihn gilt der
zweite Halbsatz der Regel.

DAS 95. PERZENTIL
------------------------------------------------------------------------------
Gerechnet auf allen gefundenen Trades der TB-24-Liste
(`daten/<bot>_alle_trades.csv`; R107 (e), TB-176a - kein Filter auf
ausgefuehrte Positionen), Haltedauer als exakte Differenz
`exit_time - entry_time` in Tagen. Die Perzentilrechnung ist die lineare
Interpolation, die auch `pandas.Series.quantile` verwendet; dass sie
zeichengleich rechnet, prueft `test_faltenplan_neun.py` an den in TB-24
veroeffentlichten P90-Werten aller neun Bots nach.

Ein Embargo ist eine Zahl von Tagen. Ein gebrochenes Perzentil wird deshalb
**aufgerundet** - abrunden hiesse, den Rand kuerzer zu machen, als die
Messung ihn ausweist.

    python3 research/faltenplan_neun/embargo_neun.py
    python3 research/faltenplan_neun/embargo_neun.py --json bericht.json
"""

import argparse
import csv
import datetime as dt
import json
import math
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB36_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

sys.path.insert(0, _HIER)

from faltenplan_neun import (BOTS, fensteranker, kursdatei,  # noqa: E402
                             symbole)

TB24_DATEN = os.path.join("research", "tb24_haltedauern", "daten")

# Wo die Zeitbremse jedes Bots steht. Ein Bot kann mehrere haben (Backtest und
# Live-Lauf getrennt notiert); die Regel verlangt die LAENGSTE, also werden
# alle gelesen und verglichen.
#
#   einheit "balken"       -> Balken des Bot-Zeitrahmens
#   einheit "kalendertage" -> echte Kalendertage (nur elliott_wave_stocks)
ZEITBREMSEN = {
    "elliott_wave": [
        ("strategies/elliott_wave/backtest_elliott.py", "MAX_HOLD_HOURS",
         "balken"),
        ("strategies/elliott_wave/forward_test.py", "MAX_HOLD_HOURS",
         "balken"),
    ],
    "t3_supertrend": [],
    "rsi2_crypto": [
        ("strategies/rsi2_crypto/live_params.py", "MAX_HOLD_DAYS", "balken"),
    ],
    "turtle_soup_crypto": [
        ("strategies/turtle_soup_crypto/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
    "volatility_breakout_crypto": [
        ("strategies/volatility_breakout_crypto/live_params.py",
         "MAX_HOLD_DAYS", "balken"),
    ],
    "elliott_wave_stocks": [
        ("strategies/elliott_wave_stocks/backtest_elliott.py",
         "MAX_HOLD_HOURS", "balken"),
        ("strategies/elliott_wave_stocks/forward_test.py", "MAX_HOLD_DAYS",
         "kalendertage"),
    ],
    "rsi2_mean_reversion": [
        ("strategies/rsi2_mean_reversion/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
    "turtle_soup_stocks": [
        ("strategies/turtle_soup_stocks/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
    "volatility_breakout": [
        ("strategies/volatility_breakout/live_params.py", "MAX_HOLD_DAYS",
         "balken"),
    ],
}

# Stunden je Balken - nur zur Umrechnung von Balken in Tage bei Krypto.
BALKENSTUNDEN = {"1h": 1, "4h": 4, "1d": 24}


# ==============================================================================
# 1. Zahlen aus Bot-Dateien lesen (nie importieren)
# ==============================================================================
def lies_konstante(relpfad: str, name: str, basis: str = None):
    """Den Wert einer Modulkonstanten aus dem QUELLTEXT lesen.

    Gesucht wird eine Zuweisung auf oberster Ebene - `NAME = 123`. Zeilen mit
    Einrueckung zaehlen nicht (das waere eine lokale Variable), Kommentare
    hinter dem Wert werden abgeschnitten. Gibt None, wenn es die Zuweisung
    nicht gibt.
    """
    pfad = os.path.join(basis or BASE_DIR, relpfad)
    muster = re.compile(r"^" + re.escape(name) + r"\s*=\s*([0-9]+(?:\.[0-9]+)?)")
    with open(pfad, "r", encoding="utf-8") as datei:
        for nummer, zeile in enumerate(datei, start=1):
            treffer = muster.match(zeile)
            if treffer:
                roh = treffer.group(1)
                wert = float(roh) if "." in roh else int(roh)
                return wert, f"{relpfad}:{nummer}"
    return None, None


# ==============================================================================
# 2. Handelstage - gemessen, nicht geschaetzt
# ==============================================================================
def handelstage(markt: str, basis: str = None) -> list:
    """Die Boersentage des Marktes, aus den Kursdateien gesammelt.

    Krypto laeuft durch; dort ist jeder Kalendertag ein Handelstag. Bei Aktien
    ist es der Kalender, den die Kursdateien tatsaechlich zeigen - mit
    Feiertagen, ohne Annahme.
    """
    tage = set()
    for symbol in symbole(markt, basis):
        pfad = kursdatei(symbol, "1d", basis)
        if not os.path.exists(pfad):
            continue
        with open(pfad, "r", encoding="utf-8") as datei:
            datei.readline()
            for zeile in datei:
                zeile = zeile.strip()
                if zeile:
                    tage.add(zeile.split(",")[0][:10])
    return sorted(dt.date.fromisoformat(t) for t in tage)


def kalendertage_in_handelstagen(kalendertage: int, markt: str,
                                 basis: str = None) -> float:
    """Wie viele Handelstage in `kalendertage` Kalendertagen liegen (Median).

    Gemessen ueber alle Startpunkte im Auswertungsfenster: fuer jeden
    Handelstag d die Zahl der Handelstage in (d, d + n Kalendertage].
    """
    if markt == "krypto":
        return float(kalendertage)
    tage = handelstage(markt, basis)
    anker = fensteranker(markt, basis)
    if anker is not None:
        tage = [t for t in tage if t >= anker]
    if not tage:
        return float(kalendertage)
    zahlen = []
    j = 0
    for i, start in enumerate(tage):
        grenze = start + dt.timedelta(days=kalendertage)
        j = max(j, i + 1)
        while j < len(tage) and tage[j] <= grenze:
            j += 1
        if tage[-1] >= grenze:                 # nur vollstaendige Fenster
            zahlen.append(j - i - 1)
    if not zahlen:
        return float(kalendertage)
    zahlen.sort()
    mitte = len(zahlen) // 2
    return (float(zahlen[mitte]) if len(zahlen) % 2
            else (zahlen[mitte - 1] + zahlen[mitte]) / 2.0)


def balken_in_handelstagen(balken: int, bot: str, basis: str = None) -> float:
    """Balken des Bot-Zeitrahmens in Handelstagen.

    Tagesbalken sind Handelstage - eins zu eins, in beiden Maerkten. Stunden-
    und Vier-Stunden-Balken gibt es nur bei Krypto, dort ist ein Kalendertag
    ein Handelstag.
    """
    zeitrahmen = BOTS[bot]["zeitrahmen"]
    if zeitrahmen == "1d":
        return float(balken)
    return balken * BALKENSTUNDEN[zeitrahmen] / 24.0


# ==============================================================================
# 3. Das 95. Perzentil der Haltedauer
# ==============================================================================
def perzentil(werte, q: float):
    """Lineare Interpolation - zeichengleich zu `pandas.Series.quantile`."""
    s = sorted(werte)
    n = len(s)
    if n == 0:
        return None
    if n == 1:
        return float(s[0])
    pos = q * (n - 1)
    unten = math.floor(pos)
    oben = math.ceil(pos)
    if unten == oben:
        return float(s[unten])
    return float(s[unten] + (pos - unten) * (s[oben] - s[unten]))


def haltedauern_tage(bot: str, basis: str = None) -> list:
    """Haltedauer je gefundenem Trade in Tagen, aus der TB-24-Liste (R107 (e))."""
    pfad = os.path.join(basis or BASE_DIR, TB24_DATEN, f"{bot}_alle_trades.csv")
    werte = []
    with open(pfad, "r", encoding="utf-8") as datei:
        for zeile in csv.DictReader(datei):
            ein = dt.datetime.fromisoformat(zeile["entry_time"])
            aus = dt.datetime.fromisoformat(zeile["exit_time"])
            werte.append((aus - ein).total_seconds() / 86400.0)
    return werte


# ==============================================================================
# 4. Das Embargo
# ==============================================================================
def embargo_fuer_bot(bot: str, basis: str = None) -> dict:
    markt = BOTS[bot]["markt"]
    bremsen = []
    for relpfad, name, einheit in ZEITBREMSEN[bot]:
        wert, herkunft = lies_konstante(relpfad, name, basis)
        if wert is None:
            continue
        if einheit == "balken":
            in_handelstagen = balken_in_handelstagen(wert, bot, basis)
        else:
            in_handelstagen = kalendertage_in_handelstagen(int(wert), markt,
                                                           basis)
        bremsen.append({
            "konstante": name, "wert": wert, "einheit": einheit,
            "herkunft": herkunft,
            "handelstage": round(in_handelstagen, 4),
        })

    if bremsen:
        laengste = max(bremsen, key=lambda b: b["handelstage"])
        grundlage = laengste["handelstage"]
        embargo = int(math.ceil(grundlage)) + 1
        art = "zeitbremse"
        p95 = None
    else:
        werte = haltedauern_tage(bot, basis)
        p95_roh = perzentil(werte, 0.95)
        # Bei Krypto ist ein Kalendertag ein Handelstag; t3_supertrend - der
        # einzige Bot ohne Zeitbremse - ist ein Krypto-Bot.
        grundlage = (p95_roh if markt == "krypto"
                     else kalendertage_in_handelstagen(int(math.ceil(p95_roh)),
                                                       markt, basis))
        embargo = int(math.ceil(grundlage)) + 1
        art = "perzentil"
        laengste = None
        p95 = {"p95_tage": round(p95_roh, 4), "n_trades_gefunden": len(werte),
               "herkunft": f"{TB24_DATEN}/{bot}_alle_trades.csv"}

    return {
        "bot": bot, "markt": markt, "zeitrahmen": BOTS[bot]["zeitrahmen"],
        "art": art,
        "zeitbremsen": bremsen,
        "laengste_zeitbremse": laengste,
        "perzentil95": p95,
        "grundlage_handelstage": round(grundlage, 4),
        "embargo_handelstage": embargo,
    }


def embargos(basis: str = None) -> dict:
    return {bot: embargo_fuer_bot(bot, basis) for bot in BOTS}


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Das Embargo je Bot nach Registertext 2d.")
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    print("=" * 78)
    print("Embargo je Bot - Registertext 2d (TB-36)")
    print("Zeitbremse in Handelstagen + 1; ohne Zeitbremse: P95 + 1")
    print("=" * 78)
    ergebnis = embargos()

    print(f"\n{'Bot':<28}{'Art':<11}{'Grundlage':<30}{'Handelstage':>12}"
          f"{'Embargo':>9}")
    print("-" * 92)
    for bot, e in ergebnis.items():
        if e["art"] == "zeitbremse":
            b = e["laengste_zeitbremse"]
            grundlage = f"{b['konstante']} = {b['wert']:g} ({b['einheit']})"
        else:
            grundlage = f"P95 = {e['perzentil95']['p95_tage']:.2f} Tage"
        print(f"{bot:<28}{e['art']:<11}{grundlage:<30}"
              f"{e['grundlage_handelstage']:>12.2f}{e['embargo_handelstage']:>9}")

    print("\nHerkunft je Zahl")
    print("-" * 92)
    for bot, e in ergebnis.items():
        if e["art"] == "zeitbremse":
            for b in e["zeitbremsen"]:
                markierung = ("  <- laengste"
                              if b is e["laengste_zeitbremse"] else "")
                print(f"  {bot:<28}{b['konstante']} = {b['wert']:g} "
                      f"({b['einheit']}, {b['handelstage']:g} Handelstage)"
                      f"  aus {b['herkunft']}{markierung}")
        else:
            p = e["perzentil95"]
            print(f"  {bot:<28}keine Zeitbremse - P95 = {p['p95_tage']:.4f} "
                  f"Tage aus {p['n_trades_gefunden']} gefundenen Trades, {p['herkunft']}")

    if argumente.json:
        with open(argumente.json, "w", encoding="utf-8") as datei:
            json.dump(ergebnis, datei, indent=2, ensure_ascii=False,
                      sort_keys=True)
        print(f"\nBericht: {argumente.json}")

    print("\nRein lesend - es wurde nichts geaendert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
````

### Anhang D — Probe E2

<!-- DATEI tb176a_probe_leser.py -->
````python
#!/usr/bin/env python3
"""TB-176a E2 Probe (Anhang E): die zwei umgestellten Leser an einer Kopie mit kleinen <bot>_alle_trades.csv (R107 (e)).
Aufruf aus der Repo-Wurzel; schreibt nur in einen Temp-Ordner; liest keine Kurse. Gegenprobe: die Fassung am HEAD (git show) liest
<bot>_positionen.csv und scheitert an derselben Kopie. Rueckgabe 0 = alle ja."""
import csv, datetime as dt, json, os, shutil, subprocess, sys, tempfile, types
sys.dont_write_bytecode = True
TB, FN = "research/tb24_haltedauern/", "research/faltenplan_neun/"
BOTS = [("elliott_wave", "krypto", "4h"), ("t3_supertrend", "krypto", "4h"), ("rsi2_crypto", "krypto", "1d"), ("turtle_soup_crypto", "krypto", "1d"), ("volatility_breakout_crypto", "krypto", "1d"),
        ("elliott_wave_stocks", "aktien", "1d"), ("rsi2_mean_reversion", "aktien", "1d"), ("turtle_soup_stocks", "aktien", "1d"), ("volatility_breakout", "aktien", "1d")]
TAGE = [1, 2, 3, 4, 10, 6]                       # Haltedauern in Tagen; Zeile 3 und 4 "nicht ausgefuehrt"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def liste(pfad, mit_spalte):
    k = ["trade_zeile", "symbol", "entry_time", "exit_time", "result", "pnl_pct", "entry_price", "exit_price", "kerzen"] + (["ausgefuehrt"] if mit_spalte else [])
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(k)
        for i, d in enumerate(TAGE):
            ein = dt.datetime(2022, 1, 3) + dt.timedelta(days=11 * i)
            w.writerow([i, "AAA" if i % 2 else "BBB", ein, ein + dt.timedelta(days=d), "time_exit", 1.0, 10.0, 10.1, d] + ([str(i not in (2, 3))] if mit_spalte else []))
def meta(pfad, bot, kl, tf):
    json.dump({"bot": bot, "zeitrahmen": tf, "anlageklasse": kl, "trades_gefunden": len(TAGE), "symbole_gefunden": 2, "symbole_geladen": 2,
               "erster_einstieg": "2022-01-03 00:00:00", "letzter_ausstieg": "2022-03-05 00:00:00", "ausstiegsarten": {"time_exit": len(TAGE)},
               "spalte_result_vorhanden": True, "kerzen_ohne_wert": 0}, open(pfad, "w"), indent=2)
def head(pfad): return subprocess.run(["git", "--no-optional-locks", "show", "HEAD:" + pfad], capture_output=True, check=True).stdout.decode("utf-8")
basis = tempfile.mkdtemp(prefix="tb176a_probe_", dir=os.environ.get("TMPDIR") or None)
# --- Leser 1: tb24_haltedauern/auswertung.py ---------------------------------
for fall in ("neu", "alt"):
    d = os.path.join(basis, "a_" + fall); os.makedirs(d + "/daten")
    shutil.copy(TB + "haltedauer_kern.py", d)
    if fall == "neu": shutil.copy(TB + "auswertung.py", d)
    else: open(d + "/auswertung.py", "w", encoding="utf-8").write(head(TB + "auswertung.py"))
    for n, (bot, kl, tf) in enumerate(BOTS):
        liste(d + "/daten/%s_alle_trades.csv" % bot, n % 2 == 0); meta(d + "/daten/%s_meta.json" % bot, bot, kl, tf)
    r = subprocess.run([sys.executable, "-B", "auswertung.py"], cwd=d, capture_output=True, text=True)
    if fall == "neu":
        p(r.returncode == 0, "auswertung.py (neu) an der Kopie: rc %d %s" % (r.returncode, (r.stderr.strip().split("\n") or [""])[-1][:120]))
        hz = list(csv.DictReader(open(d + "/ergebnisse/haltedauern_je_bot.csv", encoding="utf-8"))) if r.returncode == 0 else []
        p(len(hz) == 9 and all(int(z["n"]) == len(TAGE) for z in hz), "haltedauern_je_bot.csv: je Bot n = %d (alle gefundenen Trades, auch die %d mit ausgefuehrt=False): %s" % (len(TAGE), 2, sorted(set(z["n"] for z in hz))))
        med = sorted(TAGE)[len(TAGE) // 2 - 1:len(TAGE) // 2 + 1]; m = sum(med) / 2.0
        p(all(abs(float(z["tage_median"]) - m) < 1e-9 for z in hz) and hz, "Median je Bot = %.1f Tage (von Hand: Median von %s)" % (m, TAGE))
        zf = json.load(open(d + "/ergebnisse/zusammenfassung.json", encoding="utf-8")) if r.returncode == 0 else {"datenbasis": {}}
        db = zf["datenbasis"]
        p(len(db) == 9 and all("trades_ausgefuehrt" not in v and "symbole_ausgefuehrt" not in v and v.get("symbole_gefunden") == 2 and v.get("trades_gefunden") == len(TAGE) for v in db.values()),
          "zusammenfassung.json: datenbasis ohne trades_/symbole_ausgefuehrt, mit trades_gefunden %d und symbole_gefunden 2" % len(TAGE))
        p(r.returncode == 0 and not os.path.exists(d + "/ergebnisse/gegenprobe_positionslimit.csv"), "gegenprobe_positionslimit.csv entfallen (haengt an ausgefuehrt)")
    else:
        p(r.returncode != 0 and "_positionen.csv" in r.stderr, "Gegenprobe: auswertung.py am HEAD scheitert an derselben Kopie (liest <bot>_positionen.csv): rc %d" % r.returncode)
# --- Leser 2: faltenplan_neun/embargo_neun.py --------------------------------
sys.path.insert(0, os.path.abspath(FN))
for fall in ("neu", "alt"):
    b = os.path.join(basis, "e_" + fall); os.makedirs(b + "/" + TB + "daten"); liste(b + "/" + TB + "daten/t3_supertrend_alle_trades.csv", True)
    mod = types.ModuleType("embargo_" + fall); mod.__file__ = os.path.abspath(FN + "embargo_neun.py")
    quelle = open(FN + "embargo_neun.py", encoding="utf-8").read() if fall == "neu" else head(FN + "embargo_neun.py")
    exec(compile(quelle, mod.__file__, "exec"), mod.__dict__)
    try:
        w = sorted(mod.haltedauern_tage("t3_supertrend", b)); e = mod.embargo_fuer_bot("t3_supertrend", b); fehler = None
    except Exception as x:
        w, e, fehler = None, None, x
    if fall == "neu":
        p(w == sorted(float(x) for x in TAGE), "embargo_neun.haltedauern_tage (neu): alle %d gefundenen Trades %s" % (len(TAGE), w))
        q = (len(TAGE) - 1) * 0.95; s = sorted(TAGE); p95 = s[int(q)] + (q - int(q)) * (s[int(q) + 1] - s[int(q)])
        p(e is not None and e["art"] == "perzentil" and e["perzentil95"]["n_trades_gefunden"] == len(TAGE) and e["perzentil95"]["herkunft"].endswith("t3_supertrend_alle_trades.csv")
          and abs(e["perzentil95"]["p95_tage"] - p95) < 1e-9 and e["embargo_handelstage"] == int(-(-p95 // 1)) + 1,
          "embargo_fuer_bot(t3_supertrend): P95 %.4f (von Hand), Embargo %s = aufgerundet + 1, n_trades_gefunden %s, herkunft alle_trades" % (p95, e and e["embargo_handelstage"], e and e["perzentil95"]["n_trades_gefunden"]))
    else:
        p(isinstance(fehler, FileNotFoundError) and "_positionen.csv" in str(fehler), "Gegenprobe: embargo_neun.py am HEAD scheitert an derselben Kopie (liest <bot>_positionen.csv): %s" % type(fehler).__name__)
print("Kopie: %s" % basis); print("\n".join(OUT)); n = sum(l.startswith("ja") for l in OUT)
print("Ergebnis: %d von %d bestanden" % (n, len(OUT))); sys.exit(0 if n == len(OUT) else 1)
````

