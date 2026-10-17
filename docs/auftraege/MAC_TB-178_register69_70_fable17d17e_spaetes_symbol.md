# TB-178 Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110) mit Marken; Abnahme des späten Symbolfalls am Erzeuger (R110 (a)) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 22:00** (Helfer BAU178B, per Skript aus Bausteinen, `/tmp/w36/sc/tb178/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis P (mit R und K) an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `e79ca2c`; Start am HEAD `e79ca2ce3f50c8828bd52f712fbb4a8e1bada4e3`.**

**Sitzungstitel:** `TB-178` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `e79ca2ce3f50c8828bd52f712fbb4a8e1bada4e3` (kommt bis zum Start ein Commit dazu, füllt der steuernde Chat HEAD und Soll neu) · **Start:** über den Sitzungswächter (`starte_TB-178`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (Python 3.9, numpy 2.0.2, pandas 2.3.3 nach `requirements.lock`); Werkzeug `docs/belege/TB-178/tb178_werkzeug.py` (Anhang A), kurz `WZ`; Probe `docs/belege/TB-178/tb178_probe_spaetes_symbol.py` (Anhang B). **Belege:** `docs/belege/TB-178/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-178_register69_70_spaetes_symbol.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FN ⇒ FO).
**Grundlage Register (zeichengleich, nicht umdeuten):** Fable-Antwort 17.10.d (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md`, md5 `3b886ee769174d7c474679dd4452c9eb`, 6 141 B), Registerblock R109; Fable-Antwort 17.10.e (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md`, md5 `1d964b3107485a44ba29467ebc56c34a`, 5 115 B), Registerblock R110; je Anfrage und Übergabe (Anhang „Quellen“ unten); bis Schritt 0 git-ignoriert unter `data_sicherung/steuernder_chat_tmp/f17d/` und `data_sicherung/steuernder_chat_tmp/f17e/`. R56 (b) (Anfrage und Antwort mit Commit im Repo, bevor eingetragen wird); Bauart 67/68 (Register aus Fable mit Marken, TB-175, TB-176a). Quelle des Auftrags: Nachricht des steuernden Chats an den Helfer BAU178B vom 17.10.2026 (ausserhalb des Repos).
**Schnitt (Vorschlag des Helfers BAU178B, Entscheid beim steuernden Chat):** TB-178 = Fable-Dateien, Register 69/70 mit Marken, Index und Kopien, Abnahme des späten Symbolfalls (R110 (a)) — **ohne Handelscode**. **Nicht** in TB-178: der Bauauftrag nach 37.3 aus R110 (b) (Nachtrag zu Punkt 9, `STARTING_CAPITAL` in `shared/handelskosten.py`, neun Importe, neues Abbild, Ergänzung zu 29.3) und die Probe nach R110 (c) in `shared/test_ergebniskurven.py` (Vorschlag TB-180, Handelscode, frischer Gegenleser Pflicht). Beides kommt in A auf BACKLOG Rang 1.
**Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 (mit Fable 17.10.d und 17.10.e ins Repo) ⇒ V ⇒ R (Register 69 und 70, zehn Marken) ⇒ K (Kopien, Index, Dialog-Index) ⇒ P (Probe am Erzeuger) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F. Registereintrag nur in R.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 35 („Opus Trading Bots-17.10.2026 b“), 17.10.2026, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript, Zeit 2026-10-17T20:15:56.508Z UTC): Your questions have been answered: "Gibst du TB-178 frei? Der Auftrag macht drei Dinge. (1) Er bringt Anfrage, Übergabe und Antwort von Fable 17.10.d und 17.10.e unverändert ins Repo, mit md5 vorher und nachher. (2) Er schreibt Register 69 (R109) und 70 (R110) zeichengleich aus den Antworten, dazu zehn Marken, Index und Kopien. (3) Er prüft am Mac den späten Symbolfall für t3_supertrend, elliott_wave und elliott_wave_stocks: mit und ohne Schranke bytegleich, dazu die Gegenprobe in beide Richtungen. Die Probe liegt mit Prüfzahl im Repo. In der Simulation lief t3 58/58 und elliott_wave 11/11 bytegleich, und die Gegenproben schlugen an. Ist die Prüfung grün, ist die Bedingung des Tags aus R105 (c) für alle drei Bots erfüllt. Kein Handelscode, keine Kursdaten aus data/, kein Geld. Das Startkapital (Sperrliste, Konstante, Test-Anpassung) ist Handelscode und kommt als eigener Auftrag TB-180 mit frischem Gegenleser. bau.sh endet mit rc 0, simuliert auf dem Gerät mit Python 3.10, am Mac läuft 3.9. Gesendet wird erst nach einer eigenen Karte „Senden?“. TB-179 (Regeln der KI-Forschung) folgt danach; ich passe ihn an den neuen Stand an. Empfehlung: freigeben."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. `WZ register` übernimmt die Zeile wörtlich in die Kopfsätze von 69 und 70. TB-178 ändert keinen Handelscode, keine Datei der Sperrliste und nichts unter `research/`, `strategies/`, `shared/`, `data/`, `config/`.

## Was eingetragen wird (Schritt R, K)

- **Abschnitt 69** (`WZ register`): Titel `## 69. Fable 17d — Registerblock R109 (TB-178)`; Kopfsatz (Bauart 67/68, Quelle mit md5, Anfrage und Übergabe, Karte wörtlich); **69.1 R109** „> R109 …“ und „> Quelle des Grundes“ **zeichengleich** aus dem Codeblock der Antwort 17.10.d (das Werkzeug liest sie aus der Datei und vergleicht nach dem Schreiben Zeichen für Zeichen), eine „**Kette:**“-Zeile; **69.2 Voraussetzungen und Befunde**: `v_voraussetzung.txt` wörtlich eingerückt; **(a)** R109 (b), Voraussetzung (nur das Wie), gemessen durch Lesen: TB-169 3b setzt den Tag selbst (`research/tb24_haltedauern/test_listen_erzeuger.py`, `hb()`, Zeilen mit Commit) — gesetzt, wie R110 (a) es einträgt; **(b)** der Registertext zu 29.3 aus R109 (a) wird **nicht** eingetragen (er folgt dem Bauauftrag nach R110 (b)); **(c)** R56 (b).
- **Abschnitt 70** (`WZ register`, im selben Aufruf nach 69): Titel `## 70. Fable 17e — Registerblock R110 (TB-178)`; Kopfsatz wie 69; **70.1 R110** zeichengleich aus der Antwort 17.10.e; Kette; **70.2**: (a) Abnahme nach R110 (a) folgt in Schritt P, Ergebnis im Ergebnis TB-178, bis dahin offen; (b) R110 (b), (c) nicht Teil von TB-178; (c) R56 (b).
- **Zehn Marken** (R109 (c): vier; R110 (d): sechs); je Zeilenpaar wie 67/68 (Leerzeile, Marke, „Eintrag und Stand oben bleiben zeichengleich.“); der alte Satz bleibt unberührt; Einfügestelle nach „> Quelle des Grundes“ (68.1, 66.1, 67.1, 69.1) bzw. am Ende des Unterabschnitts (29.3, 37.2, 37.5, 38.5); stehen dort schon Marken, kommt die neue dahinter (an 29.3 und 66.1 erst R109, dann R110):
  - an 68.1 (R109): `> ⭐ **68.1 R108 BERICHTIGT und ERGÄNZT durch R109 (69.1)** (Fable 17d R109, Unterpunkt (a): BERICHTIGT („lies“); Unterpunkte (a) und (b): ERGÄNZT, TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 29.3 (R109): `> ⭐ **29.3 ERGÄNZT durch R109 (69.1)** (Fable 17d R109, Unterpunkt (a), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 66.1 (R109): `> ⭐ **66.1 R106 BERICHTIGT durch R109 (69.1)** (Fable 17d R109, Unterpunkt (b) („lies“), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 67.1 (R109): `> ⭐ **67.1 R107 ERGÄNZT durch R109 (69.1)** (Fable 17d R109, Unterpunkt (b), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 69.1 (R110): `> ⭐ **69.1 R109 BERICHTIGT und ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkte (a) und (b): BERICHTIGT („lies“); Unterpunkte (a) bis (c): ERGÄNZT, TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 66.1 (R110): `> ⭐ **66.1 R106 ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkt (a), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 37.2 (R110): `> ⭐ **37.2 ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkt (b), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 37.5 (R110): `> ⭐ **37.5 ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkt (b), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 29.3 (R110): `> ⭐ **29.3 ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkt (b), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - an 38.5 (R110): `> ⭐ **38.5 ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkt (b), TB-178, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
- **Ohne Marke** (R109 (c)): 59.1, 29.2, 24.6, 37.3, 37.5, 38.5, 23.5, 56.3 (R86), 56.4 (R87), 57.1 (R90), 65.2 (R105), 66.2, 67.2, Abschnitt 10. (R110 (d)): 36.1, 37.1, 37.3, 37.6, 38.4, 56.4, 64.1, 67.1, 68.2, Abschnitt 10 (Indexzeile Punkt 9).
- **Index** (K, `WZ index`): Kopf 0–70, Zeilen `| 69 aus 17d |` und `| 70 aus 17e |`, neuer Abschnitt 20 (Tabelle der zehn Marken aus `r_daten.json`). **Dialog-Index** 17d und 17e über Handfelder.
- Append-only bis auf die zehn Marken (`WZ register` prüft es nach dem Schreiben). Register am Bau-HEAD 12785 Zeilen, 68 letzter Abschnitt, kein „R109“, kein „R110“.

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen; aus `data_sicherung/` nur die sechs Fable-Dateien in Schritt 0 kopieren. Keine Neuerzeugung der neun Listen; `positionen_holen.py` läuft nur in der Probe (Schritt P) an einem synthetischen Snapshot im Temp-Ordner (Lesehaken prüft es). Nichts unter `research/`, `strategies/`, `shared/`, `data/`, `config/` ändern. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`, kein `git stash`, kein `rm`, kein `mv`. **Schreiben darf die Sitzung nur:** die sechs Fable-Dateien (Schritt 0, `cp`), `docs/VORREGISTRIERUNG_neuselektion.md` (nur `WZ register`), `REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Werkzeugen), BACKLOG und Journal (A, nur `WZ`), das Ergebnis, `docs/auftraege/AKTUELLER_AUFTRAG.md` wie im 0a-Soll, und unter `BEL`.

## Lage nach dem Auslegen

Soll in 0a vom steuernden Chat gefüllt (`[' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md']`); am Bau-HEAD wären es 2 Einträge gewesen: ` M docs/auftraege/AKTUELLER_AUFTRAG.md`, `?? docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md`.

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `e79ca2ce3f50c8828bd52f712fbb4a8e1bada4e3`, genau die Einträge `[' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md']`, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb178_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "e79ca2ce3f50c8828bd52f712fbb4a8e1bada4e3": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "e79ca2ce3f50c8828bd52f712fbb4a8e1bada4e3": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (N Eintraege)` mit N = Zahl der Einträge im Soll. Anhänge holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb178_werkzeug.py 552f5c4d709586c3bf15bd32f5028fefb93a6e507d0893cd8c34166df693a1af`; `tb178_probe_spaetes_symbol.py 1fe6f12ef5f47603743524f5567cbf84f8edae81c459349d6284a1eeafe0fa88`; `Dateien 2`; sonst **ABBRUCH**.

**Fable 17.10.d und 17.10.e ins Repo** (git-ignoriert ⇒ nicht im 0a-Soll; genau diese Zeilen):

```
cp data_sicherung/steuernder_chat_tmp/f17d/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md
cp data_sicherung/steuernder_chat_tmp/f17d/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md
cp data_sicherung/steuernder_chat_tmp/f17d/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md
cp data_sicherung/steuernder_chat_tmp/f17e/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md
cp data_sicherung/steuernder_chat_tmp/f17e/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md
cp data_sicherung/steuernder_chat_tmp/f17e/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md
```

**md5 vorher (Quelle) = nachher (Repo)** (genau dieser Befehl). Soll: `Pruefungen: 6, NEIN: 0`, letzte Zeile `rc 0`; sonst **ABBRUCH** (die sechs Kopien bleiben unverfolgt liegen; melden):

```bash
trading-env/bin/python3 -B "$TMPDIR/tb178_werkzeug.py" md5 > "$TMPDIR/tb178_md5.txt" 2>&1; echo "rc $?" >> "$TMPDIR/tb178_md5.txt"; tail -2 "$TMPDIR/tb178_md5.txt"
```

Dann genau diese Zeilen (die erste fügt die in 0a geprüften Pfade mit Namen hinzu, dazu die sechs Fable-Dateien), Commit `TB-178 Schritt 0: Fable 17.10.d und 17.10.e (je Anfrage, Antwort, Uebergabe) und Stand des steuernden Chats vor TB-178 (Auftrag)`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
trading-env/bin/python3 -B -c "import subprocess, sys; z = [l[3:] for l in open(sys.argv[1], encoding='utf-8').read().split(chr(10)) if l]; print('git add', len(z)); raise SystemExit(subprocess.run(['git', 'add', '--'] + z).returncode)" "$TMPDIR/tb178_0a.txt"
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-178
cp "$TMPDIR/tb178_0a.txt" docs/belege/TB-178/0a_status.txt
cp "$TMPDIR/tb178_md5.txt" docs/belege/TB-178/0a_md5.txt
cp "$TMPDIR/tb178_werkzeug.py" docs/belege/TB-178/tb178_werkzeug.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py voraussetzung > docs/belege/TB-178/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (34 Prüfungen: die Gruppe der Erzeuger-Dateien je md5 = Bau; BACKLOG Rang 1, Journal FN oder FO; Anfrage, Antwort und Übergabe 17.10.d und 17.10.e verfolgt, gleich HEAD, md5 wie Soll; Registerblöcke R109 und R110; 68 da, 69/70 nicht; neun Marken-Orte eindeutig (69.1 entsteht erst in R); Index-Kopf 0–68, Zeile 68, Pflegezeile TB-176a, Abschnitt 19, kein Abschnitt 20; Dialog-Index ohne 17d/17e; Voraussetzung R109 (b) lesbar; Probe noch nicht im Repo). Die `info`-Zeile zu R109 (b) ist Messung, kein Urteil, und geht wörtlich in 69.2. **Abbruch in V:** im Arbeitsbaum liegt nur der unverfolgte Ordner `BEL`. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-178/abbruch.txt`, dann `git add` mit Namen für `docs/belege/TB-178/0a_status.txt`, `docs/belege/TB-178/0a_md5.txt`, `docs/belege/TB-178/tb178_werkzeug.py`, `docs/belege/TB-178/v_voraussetzung.txt`, `docs/belege/TB-178/abbruch.txt`, Commit `TB-178 Abbruch: V`, pushen, melden.

## Schritt R — Register 69 und 70, zehn Marken

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-178/v_voraussetzung.txt --probe > docs/belege/TB-178/r_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/r_probe.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-178/v_voraussetzung.txt > docs/belege/TB-178/r_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/r_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach genau diese `git add`, Commit `TB-178 R: Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110), zehn Marken`, pushen ⇒ **⟨R⟩**:

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-178/0a_status.txt
git add docs/belege/TB-178/0a_md5.txt
git add docs/belege/TB-178/tb178_werkzeug.py
git add docs/belege/TB-178/v_voraussetzung.txt
git add docs/belege/TB-178/r_probe.txt
git add docs/belege/TB-178/r_eintrag.txt
git add docs/belege/TB-178/r_daten.json
```

## Schritt K — Kopien, Index, Dialog-Index (wie TB-176a Schritt K)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-178/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-178/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-178/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨R⟩ > docs/belege/TB-178/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-178/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_index.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py handfelder docs/belege/TB-178/k_handfelder.json > docs/belege/TB-178/k_handfelder.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_handfelder.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-178/k_handfelder.json > docs/belege/TB-178/k_dialog_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_dialog_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-178/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`. **Kein Abbruch** bei rc ≠ 0 in K: festhalten, die Dateien dieses Schritts nicht committen, nicht zurücksetzen, melden, weiter mit P. Entsteht eine weitere Teildatei: mit Namen anfügen, melden. Dann genau diese `git add`, Commit `TB-178 K: Registerkopie, Index, Dialog-Index`, pushen ⇒ **⟨K⟩**; danach `git status --porcelain` — Soll: keine Ausgabe:

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
git add docs/belege/TB-178/k_registerkopie.txt
git add docs/belege/TB-178/k_abschnitte.txt
git add docs/belege/TB-178/k_pruefen.txt
git add docs/belege/TB-178/k_index_zeilen.txt
git add docs/belege/TB-178/k_index.txt
git add docs/belege/TB-178/k_handfelder.txt
git add docs/belege/TB-178/k_dialog_index.txt
git add docs/belege/TB-178/k_dialog_pruefen.txt
git add docs/belege/TB-178/k_handfelder.json
```

## Schritt P — Abnahme des späten Symbolfalls am Erzeuger (R110 (a))

Die Probe (Anhang B, sha256 `1fe6f12ef5f47603743524f5567cbf84f8edae81c459349d6284a1eeafe0fa88`) startet `research/tb24_haltedauern/positionen_holen.py` über `test_listen_erzeuger.lauf` je Bot (t3_supertrend, elliott_wave, elliott_wave_stocks) an einem synthetischen Snapshot im Temp-Ordner: AAA, BBB, CCC (+ BTCUSDT bei Krypto) und SPAET mit spätem Datenbeginn; der Handelbar-Tag jedes Symbols kommt aus der Rechnung nach 23.5 (`faltenschranke_messung.handelbar_ab`), **kein Tag gesetzt**; kein Symbol trägt vor seinem Tag ein Signal (Bedingung des Falls, R110 (a)). Je Bot sechs Prüfungen: 1 Tage gerechnet, 2 rc mit/ohne Schranke 0, 3 Ausgaben bytegleich, 4 Zählzeile 0 und SPAET-Trades erst ab dem Tag, 5 Lesehaken (nur Snapshot-Dateien, kein `data/`), 6 Gegenprobe beide Seiten (SPAET mit Signal vor dem Tag: ohne Schranke rc 2 nach R87 (c); mit Schranke rc 0, Zählzeile über 0). Genau diese Befehle:

```
cp "$TMPDIR/tb178_probe_spaetes_symbol.py" docs/belege/TB-178/tb178_probe_spaetes_symbol.py
trading-env/bin/python3 -B docs/belege/TB-178/tb178_probe_spaetes_symbol.py > docs/belege/TB-178/p_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/p_probe.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py nachher > docs/belege/TB-178/p_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/p_nachher.txt
```

Soll: `p_probe.txt` endet mit `Ergebnis: 18 von 18 bestanden` und `rc 0`; `p_nachher.txt` mit `rc 0` (Erzeuger-Dateien unverändert, Probe = Anhang B, 6 von 6 je Bot). **Kein Abbruch** in P: weicht ein Beleg ab, trotzdem genau diese `git add` und Commit `TB-178 P: Abnahme spaeter Symbolfall am Erzeuger (R110 (a))`, pushen, in A als offen eintragen, melden (P ändert nichts ausser `BEL`). Dann ⇒ **⟨P⟩**:

```
git add docs/belege/TB-178/tb178_probe_spaetes_symbol.py
git add docs/belege/TB-178/p_probe.txt
git add docs/belege/TB-178/p_nachher.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ backlog` hängt an Rang 1: Register 69/70 mit R109/R110; offen der Bauauftrag nach 37.3 aus R110 (b) und die Probe nach R110 (c) (Vorschlag TB-180, Handelscode); R110 (a) Abnahme mit TB-178 (Ergebnis aus `p_probe.txt`). `WZ kennung`. Block nach `docs/belege/TB-178/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-178: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-178_register69_70_spaetes_symbol.md` mit: Kopf mit Commits; Kurz; Schritt 0 (`0a_md5.txt` wörtlich); V wörtlich (mit der `info`-Zeile zu R109 (b)); R (`r_eintrag.txt` letzte Zeilen, Marken-Zeilen aus `r_daten.json`); K (rc je Beleg); P (`p_probe.txt` die 18 Prüfzeilen und die Zählzeilen, `p_nachher.txt`); ob nach R110 (a) damit die Bedingung des Tags aus R105 (c) für alle drei Bots erfüllt und R107 (b) erledigt ist (nur wenn P 18 von 18); offen: R110 (b), (c); das Ob aus R110 (a) („ob eine andere Abnahme in 64.1 allein auf 3b steht“) — nicht gemessen; In einfacher Sprache.

```
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py kennung > docs/belege/TB-178/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-178/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-178/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py journal docs/belege/TB-178/a_block.md --probe > docs/belege/TB-178/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-178/tb178_werkzeug.py journal docs/belege/TB-178/a_block.md > docs/belege/TB-178/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-178/a_journal.txt
```

Soll je `rc 0`. Genau diese `git add`, Commit `TB-178 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-178_register69_70_spaetes_symbol.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-178/a_kennung.txt
git add docs/belege/TB-178/a_backlog_probe.txt
git add docs/belege/TB-178/a_backlog.txt
git add docs/belege/TB-178/a_block.md
git add docs/belege/TB-178/a_journal_probe.txt
git add docs/belege/TB-178/a_journal.txt
```

**F.**

```
git status --porcelain > "$TMPDIR/tb178_f.txt"
cp "$TMPDIR/tb178_f.txt" docs/belege/TB-178/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-178/f_numstat.txt
git add docs/belege/TB-178/f_porcelain.txt
git add docs/belege/TB-178/f_numstat.txt
git commit -q -m "TB-178 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; `f_numstat.txt`: Register Spalte 2 = `0`; kein Pfad unter `research/`, `strategies/`, `shared/`, `data/`, `config/`.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; `WZ md5` nicht `rc 0`; V nicht `rc 0`; `WZ register --probe`/`register` nicht `rc 0` (Abbruch nach `register` vor ⟨R⟩: Register bleibt geändert, nicht zurücksetzen, melden; Abbruch-Commit mit den vorhandenen Belegen wie in TB-173); **kein Abbruch** in K und P; A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Die Sitzung legt zwei neue Antworten des Verfahrensprüfers mit Anfrage und Übergabe ins Repo und trägt ihre Regeltexte R109 und R110 wortgleich ins Register ein, nur angehängt, mit zehn Hinweisen an alten Stellen. Danach prüft sie an erfundenen Kursdaten mit einem spät beginnenden Symbol, dass die Schranke am Handelbar-Tag bei allen drei betroffenen Bots nichts ändert, wenn vor dem Tag kein Signal liegt, und dass sie greift, wenn eines vorliegt. Wo das Startkapital im Code seinen festen Ort bekommt (ein Eingriff in Handelscode und Sperrliste), macht ein eigener Auftrag.

## Anhänge


### Quellen (Schritt 0)

| Datei im Repo | aus | Bytes | md5 |
|---|---|---|---|
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md` | `data_sicherung/steuernder_chat_tmp/f17d/` | 3 594 | `007196934a22163335439c2888886047` |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md` | `data_sicherung/steuernder_chat_tmp/f17d/` | 6 141 | `3b886ee769174d7c474679dd4452c9eb` |
| `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md` | `data_sicherung/steuernder_chat_tmp/f17d/` | 1 548 | `b968fc124c5361f03e0f1118fdec1994` |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md` | `data_sicherung/steuernder_chat_tmp/f17e/` | 3 653 | `36389b7829a6e77c3ebe327fc58b7d25` |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md` | `data_sicherung/steuernder_chat_tmp/f17e/` | 5 115 | `1d964b3107485a44ba29467ebc56c34a` |
| `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md` | `data_sicherung/steuernder_chat_tmp/f17e/` | 1 540 | `a204bed16a9f30adda7c2b34489856ba` |

### Anhang A — Werkzeug

<!-- DATEI tb178_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-178 Werkzeug (Anhang A): Fable 17d und 17e ins Register (Abschnitt 69 = R109, Abschnitt 70 = R110, je zeichengleich, Marken nach R109 (c)
und R110 (d), 69.2 und 70.2); Index, Handfelder; Voraussetzungen, Nachher-Pruefung der Probe (P), Kennung, BACKLOG, Journal.
Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, json, os, re, subprocess, sys
P = "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-178/"
REG, IDX, DI = "docs/VORREGISTRIERUNG_neuselektion.md", P + "REGISTER_INDEX.md", P + "FABLE_DIALOG_INDEX.md"
AUF = "docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md"
QU = {"17d": "data_sicherung/steuernder_chat_tmp/f17d/", "17e": "data_sicherung/steuernder_chat_tmp/f17e/"}
FA = {"17d": P + "FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md", "17e": P + "FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md"}
FQ = {"17d": P + "FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md", "17e": P + "FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md"}
FU = {"17d": P + "FABLE_UEBERGABE_2026-10-17d_eroeffnung.md", "17e": P + "FABLE_UEBERGABE_2026-10-17e_eroeffnung.md"}
DATEIEN = [(d, f) for d in ("17d", "17e") for f in (FQ[d], FA[d], FU[d])]
MD5F = {"docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md": "007196934a22163335439c2888886047", "docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md": "3b886ee769174d7c474679dd4452c9eb", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md": "b968fc124c5361f03e0f1118fdec1994", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md": "36389b7829a6e77c3ebe327fc58b7d25", "docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md": "1d964b3107485a44ba29467ebc56c34a", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md": "a204bed16a9f30adda7c2b34489856ba"}
CODE = {"research/tb24_haltedauern/test_listen_erzeuger.py": "d77e73ed5ff7a737a22e53879ff72575", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/haltedauer_kern.py": "60942de99b323fa472ae25478a5a6836", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "research/faltenplan_neun/faltenschranke_messung.py": "584d9ff959dab7428a97a945b091e118", "strategies/t3_supertrend/multi_symbol_optimise.py": "dc85993e8d42647dea2eb2593335aab8", "strategies/elliott_wave/multi_symbol_optimise.py": "bf11370b140d3e61488ad81599b45b37", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "571076168d56f9e809ef0595f53d6e7d"}
PROBE, PSHA = BEL + "tb178_probe_spaetes_symbol.py", "1fe6f12ef5f47603743524f5567cbf84f8edae81c459349d6284a1eeafe0fa88"
KOPF_A = {"17d": "## Registerblock — zeichengleich kopierbar, nummeriert (ab R109)", "17e": "## Registerblock — zeichengleich kopierbar (ab R110)"}
RN = {"17d": "R109", "17e": "R110"}; NR = {"17d": "69", "17e": "70"}
TITEL = {"17d": "## 69. Fable 17d — Registerblock R109 (TB-178)", "17e": "## 70. Fable 17e — Registerblock R110 (TB-178)"}
RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
TLE = "research/tb24_haltedauern/test_listen_erzeuger.py"
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | ende, Kopf der Marke, Zusatz); vorhandene Marken-Tripel am Ort werden uebersprungen
MARKEN = {"17d": [("68.1", "### 68.1 ", "quelle", "68.1 R108 BERICHTIGT und ERGÄNZT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (a): BERICHTIGT („lies“); Unterpunkte (a) und (b): ERGÄNZT"),
                  ("29.3", "### 29.3 ", "ende", "29.3 ERGÄNZT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (a)"),
                  ("66.1", "### 66.1 ", "quelle", "66.1 R106 BERICHTIGT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (b) („lies“)"),
                  ("67.1", "### 67.1 ", "quelle", "67.1 R107 ERGÄNZT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (b)")],
          "17e": [("69.1", "### 69.1 ", "quelle", "69.1 R109 BERICHTIGT und ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkte (a) und (b): BERICHTIGT („lies“); Unterpunkte (a) bis (c): ERGÄNZT"),
                  ("66.1", "### 66.1 ", "quelle", "66.1 R106 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (a)"),
                  ("37.2", "### 37.2 ", "ende", "37.2 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)"),
                  ("37.5", "### 37.5 ", "ende", "37.5 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)"),
                  ("29.3", "### 29.3 ", "ende", "29.3 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)"),
                  ("38.5", "### 38.5 ", "ende", "38.5 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)")]}
OHNE = {"17d": "59.1, 29.2, 24.6, 37.3, 37.5, 38.5, 23.5, 56.3 (R86), 56.4 (R87), 57.1 (R90), 65.2 (R105), 66.2, 67.2, Abschnitt 10",
        "17e": "36.1, 37.1, 37.3, 37.6, 38.4, 56.4, 64.1, 67.1, 68.2, Abschnitt 10 (Indexzeile Punkt 9)"}
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
def block(d):
    """((R-Zeile, Quellenzeile), Z. Zaun auf, Z. Zaun zu) oder None."""
    f = FA[d]; z = lies(f if os.path.exists(f) else QU[d] + os.path.basename(f)).split("\n")
    if z.count(KOPF_A[d]) != 1: return None
    a = z.index(KOPF_A[d]) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [z[i] for i in range(a + 1, e) if z[i]]; soll = [RN[d] + " — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for l, s in zip(b, soll)] != soll: return None
    return (b[0], b[1]), a + 1, e + 1
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m, frei):
    """Index der Einfuegestelle (vor dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any(re.search(r"\b%s\b" % frei, z[i]) for i in range(a, e)): return None
    if m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    else:
        j = e - 1
        while j > a and z[j] in ("", "---"): j -= 1
        k = [j] if j > a else []
    if len(k) != 1: return None
    k = k[0]
    while k + 3 < e and z[k + 1] == "" and z[k + 2].startswith("> ⭐ ") and z[k + 3] == ZG: k += 3
    return k + 1
def markenzeilen(kopf, zusatz, datum): return ["", "> ⭐ **%s** (%s, TB-178, %s)." % (kopf, zusatz, datum), ZG]
def mess_b():
    """R109 (b), Voraussetzung (nur das Wie): woher TB-169 3b den Tag des spaeten Symbols nimmt - Zeilen in test_listen_erzeuger.py."""
    t = lies(TLE).split("\n") if os.path.exists(TLE) else []
    u = [i + 1 for i, l in enumerate(t) if "x.update(t)" in l and "def hb" in t[i - 1]]
    c = [i + 1 for i, l in enumerate(t) if 'json.dumps({"CCC": str(c0["entry_time"].min().date())})' in l]
    return u, c
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "unveraendert: %s md5 %s" % (f, m[:12]))
def voraussetzung():
    code_gleich()
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-178" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-178")
    k = kennungen(); p(max(k) in ("FN", "FO"), "Journal: hoechste %s (FN am Bau-HEAD)" % max(k))
    for d, f in DATEIEN: p(verfolgt_gleich(f) and md5f(f) == MD5F[f], "R56 (b)/S0-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5F[f]))
    for d in ("17d", "17e"):
        b = block(d); p(b is not None, "Registerblock %s: genau %s und Quelle im Codeblock (Z. %s)" % (d, RN[d], "%d–%d" % (b[1], b[2]) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 68. ") for l in z) == 1 and not any(l.startswith("## 69. ") or l.startswith("## 70. ") for l in z) and not re.search(r"\bR109\b|\bR110\b", reg), "Register: 68 da, 69 und 70 nicht; R109/R110 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for d in ("17d", "17e"):
        for m in MARKEN[d]:
            if m[0] == "69.1": continue
            i = einfuege(z, m, RN[d]); p(i is not None, "Ort %s (%s): Einfuegestelle vor Z. %s eindeutig, %s dort noch nicht genannt" % (m[0], RN[d], i + 1 if i else "?", RN[d]))
    zi = lies(IDX).split("\n"); k = [i for i, l in enumerate(zi) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    p(len(k) == 1 and "Abschnitte 0–68" in zi[k[0]], "Index-Kopf Z. %s nennt 0–68" % (k[0] + 1 if k else "?"))
    p(sum(l.startswith("| 68 aus 17c |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-176a (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and sum(l.startswith("## 19. ") for l in zi) == 1 and not any(l.startswith("## 20. ") for l in zi), "Index: Zeile 68, Pflegezeile TB-176a, Pflege-Anker, Abschnitt 19 je genau einmal; kein Abschnitt 20")
    dl = lies(DI).split("\n"); p(not any(l.startswith("| 17d |") or l.startswith("| 17e |") for l in dl), "Dialog-Index: 17d und 17e noch nicht")
    u, c = mess_b(); p(len(u) == 1 and len(c) == 1, "R109 (b) Voraussetzung lesbar: %s hb() und Pruefung 3b je genau eine Zeile" % TLE)
    info("R109 (b) Voraussetzung (Messung, kein Urteil; R110 (a): gesetzt): %s Z. %s `x.update(t)` in hb() - die vom Test uebergebenen Tage ueberschreiben die Rechnung; Z. %s Pruefung 3b setzt den Tag von CCC (`json.dumps({\"CCC\": ...})`)" % (TLE, u, c))
    p(not os.path.exists(PROBE), "Probe noch nicht im Repo (%s)" % PROBE)
    ende()
def md5cmd():
    for d, f in DATEIEN: p(md5f(QU[d] + os.path.basename(f)) == MD5F[f] and md5f(f) == MD5F[f], "md5 vorher %s = nachher %s = %s" % (QU[d] + os.path.basename(f), f, MD5F[f]))
    ende()
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def abschnitt(d, s0, k, datum, b, beleg_v, vb):
    (r, q), za, ze = b; n = NR[d]
    kopf = ("Reines Eintragen von Registertext, Bauart wie 67 und 68. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „%s“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.%s (`%s`) und die Übergabe 17.10.%s (`%s`), beide seit `%s`. "
            "Marken nach %s. Karte des Betreibers (Auftrag TB-178, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-178.") % (
            FA[d], MD5F[FA[d]], format(os.path.getsize(FA[d]), ",").replace(",", " "), KOPF_A[d][3:], za, ze, s0, d[-1], FQ[d], d[-1], FU[d], s0, "R109 (c)" if d == "17d" else "R110 (d)", k, datum)
    if d == "17d":
        u, c = mess_b()
        kette = ("**Kette:** Marken nach R109 (c): 68.1 (R108), Unterpunkt (a) berichtigt, Unterpunkte (a) und (b) ergänzt; 29.3, Unterpunkt (a); 66.1 (R106), Unterpunkt (b), berichtigt; 67.1 (R107), Unterpunkt (b). "
                 "Ohne Marke: " + OHNE[d] + ". Zählung: kein Fall; sechzehn (R109 (b)).")
        mitte = ["### 69.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-178), Zeilen wörtlich:" % beleg_v, ""] + ["    " + l for l in vb] + ["",
            ("(a) R109 (b), Voraussetzung (nur das Wie), gemessen durch Lesen am Commit `%s`: `%s` setzt den Tag selbst — `hb()` überschreibt die Rechnung mit den vom Test übergebenen Tagen (`x.update(t)`, Z. %s), "
             "Prüfung 3b übergibt den Tag von CCC (Z. %s). Ergebnis: gesetzt; so eingetragen in R110 (a) (70.1).") % (s0, TLE, ", ".join(map(str, u)), ", ".join(map(str, c))), "",
            "(b) R109 (a): Der Registertext zu 29.3 wird mit TB-178 nicht eingetragen; er folgt dem Bauauftrag nach 37.3 aus R110 (b) (70.1) in der dort berichtigten Fassung.", "",
            "(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.d liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `%s0a_md5.txt`)." % (s0, QU[d], BEL), ""]
    else:
        kette = ("**Kette:** Marken nach R110 (d): 69.1 (R109), Unterpunkte (a) und (b) berichtigt, (a) bis (c) ergänzt; 66.1 (R106), Unterpunkt (a); 37.2, 37.5, 29.3 und 38.5, Unterpunkt (b). "
                 "Ohne Marke: " + OHNE[d] + ". Zählung: kein Fall; sechzehn (R110).")
        mitte = ["### 70.2 Voraussetzungen und Befunde", "", "Voraussetzungen: dieselbe Messung wie 69.2 (`%s`)." % beleg_v, "",
            "(a) R110 (a): Die Abnahme am Erzeuger (Probe mit sha256 im Repo, 6 von 6 je Bot, Gegenprobe beide Seiten) folgt in TB-178 nach diesem Eintrag (Schritt P); ihr Ergebnis steht im Ergebnis TB-178, nicht hier. Bis dahin offen.", "",
            "(b) R110 (b) und (c): Der Bauauftrag nach 37.3 (Nachtrag zu Punkt 9, Konstante, neues Abbild, Ergänzung zu 29.3) und die Probe in `shared/test_ergebniskurven.py` sind Handelscode und nicht Teil von TB-178.", "",
            "(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.e liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `%s0a_md5.txt`)." % (s0, QU[d], BEL), ""]
    return ["", TITEL[d], "", kopf, "", "### %s.1 " % n + titel(r), "", "> " + r, "> " + q, "", kette, ""] + mitte
def register(datum, s0, beleg_v, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg_v).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg_v)
    bb = {d: block(d) for d in ("17d", "17e")}
    for d in bb: p(bb[d] is not None and md5f(FA[d]) == MD5F[FA[d]], "Quelle %s md5 %s, Registerblock %s" % (d, MD5F[FA[d]], RN[d]))
    p(not any(l.startswith("## 69. ") or l.startswith("## 70. ") for l in z) and z[-1] == "" and z[-2] != "", "69 und 70 noch nicht im Register; endet mit einer Leerzeile")
    k = karte(); p(k is not None, "Karte TB-178 gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    neu = {}; ganz = z
    for d in ("17d", "17e"):
        einf = [(einfuege(ganz, m, RN[d]), m) for m in MARKEN[d]]
        if not p(all(i is not None for i, _ in einf) and len(set(i for i, _ in einf)) == len(einf), "%s: %d Einfuegestellen eindeutig (%s)" % (RN[d], len(einf), ", ".join("%s vor Z. %s" % (m[0], i and i + 1) for i, m in einf))): ende()
        for i, m in sorted(einf, key=lambda x: -x[0]): ganz[i:i] = markenzeilen(m[3], m[4], datum)
        neu[d] = abschnitt(d, s0, k, datum, bb[d], beleg_v, vb); ganz = ganz[:-1] + neu[d]
    if probe: print("\n".join(neu["17d"] + neu["17e"])); ende()
    schreibe(REG, "\n".join(ganz))
    r2 = lies(REG).split("\n"); alle = MARKEN["17d"] + MARKEN["17e"]
    mz = [(m, [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s** (" % m[3])]) for m in alle]
    json.dump({"marken": [[m[0], m[3], (n or [0])[0]] for m, n in mz], "abschnitt_69": r2.index(TITEL["17d"]) + 1, "abschnitt_70": r2.index(TITEL["17e"]) + 1},
              open(os.path.dirname(beleg_v) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(n) == 1 for _m, n in mz), "nachher: %d Marken Z. %s; Abschnitt 69 Z. %d, 70 Z. %d" % (len(alle), sorted(x for _m, n in mz for x in n), r2.index(TITEL["17d"]) + 1, r2.index(TITEL["17e"]) + 1))
    for d in ("17d", "17e"):
        (r, q), _a, _e = bb[d]; p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "%s mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)" % RN[d])
    weg = set(x for _m, v in mz for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; soll = al + neu["17d"][:-1] + neu["17e"]
    p(r3 == soll, "Register append-only bis auf die %d Marken (je Leerzeile, Marke, Zeichengleich-Zeile)" % len(alle))
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]; alle = MARKEN["17d"] + MARKEN["17e"]
    tl = {}
    for n in ("69", "70"):
        tl[n] = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and ("\n## %s. " % n) in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(all(len(v) == 1 for v in tl.values()) and len(mk) == len(alle) and all(m[2] for m in mk), "Abschnitte 69 und 70 in je genau einer Teildatei: %s; %d Marken mit Zeile" % (tl, len(mk)))
    T = {n: (str(v[0]) if len(v) == 1 else "?") for n, v in tl.items()}
    z = lies(IDX).split("\n"); k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]; rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–68" in z[k[0]], "Kopf genau einmal, nennt 0–68"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–68", "Abschnitte 0–70")
    i = [j for j, l in enumerate(z) if l.startswith("| 68 aus 17c |")]
    if p(len(i) == 1, "Zeile 68 genau einmal"):
        z[i[0] + 1:i[0] + 1] = ["| 69 aus 17d | %s | R109 (69.1); 69.2 Voraussetzungen und Befunde | – |" % T["69"], "| 70 aus 17e | %s | R110 (70.1); 70.2 Voraussetzungen und Befunde | – |" % T["70"]]
    tab = ["---", "", "## 20. Die Marken aus Fable 17d und 17e (TB-178)", "", "Alle %d Marken, die TB-178 nach R109 (c) und R110 (d) im Register gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-178/r_daten.json`." % len(mk), "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, "?") for o, kp, n in sorted(mk, key=lambda m: m[2])] + ["", "Der Index ist kein Registertext.", ""]
    tt = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t)]
    for j, row in enumerate(tab):
        m = re.match(r"\| (\S+) \| Z\. (\d+) \| (.*) \| \? \|$", row)
        if m:
            hit = [t for t in tt if ("> ⭐ **%s** (" % m.group(3)) in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]; tab[j] = row[:-3] + ("%s |" % hit[0] if len(hit) == 1 else "? |")
    p(not any(r.endswith("| ? |") for r in tab), "jede Marke in genau einer Teildatei")
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 20. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 20"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-176a (")]
    if p(len(j) == 1, "Pflegezeile TB-176a genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-176a (", "In TB-176a (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-178 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-178 (`index`); 69 (R109) kommt zu T%s, 70 (R110) zu T%s; neuer Abschnitt 20 (%d Marken)." % (datum, s0, rcm, T["69"], T["70"], len(mk)))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    f = lambda d: lies(FQ[d]).split("\n")[0].split(" — ", 1)[-1].strip()
    json.dump({"17d": {"frage": f("17d"), "entscheidung": "(a) anders: 59.1 ist Beleg, kein Ort; Registertext zu 29.3 nach der Tatsachennotiz mit neun Fundstellen; Ort im Modul aus 38.5 (R109 (a)); (b) anders bei der Fallwahl: später Symbolfall wird gebaut, Tag aus der Rechnung nach 23.5; Voraussetzung zu 3b zu messen (R109 (b))", "offen": "ja"},
               "17e": {"frage": f("17e"), "entscheidung": "(a) einverstanden: 3b setzt den Tag, alle drei Bots am gebauten Fall, Abnahme am Erzeuger; (b) anders: Pfad zuerst ins Register (Nachtrag zu Punkt 9 nach 38.5), Bauauftrag nach 37.3 in vier Schritten, Sonde bis zum Tag 2 mit Tatsachennotiz; (c) einverstanden: test_ergebniskurven.py Handwerk in der Freigabe (R110)", "offen": "ja"}},
              open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17d, 17e geschrieben: %s" % ziel)
def nachher():
    code_gleich()
    p(sha(PROBE) == PSHA, "Probe im Repo = Anhang B (sha256 %s)" % PSHA[:16])
    pr = beleg("p_probe.txt"); n = [l for l in pr if l.startswith("ja    ") or l.startswith("NEIN  ")]
    for b in ("t3_supertrend", "elliott_wave", "elliott_wave_stocks"):
        nb = [l for l in n if l[6:].startswith(b + ": ")]; p(len(nb) == 6 and all(l.startswith("ja") for l in nb), "R110 (a) %s: %d von 6 (Abnahme am Erzeuger)" % (b, sum(l.startswith("ja") for l in nb)))
    p(any(l.startswith("Zaehlzeile Gegenprobe") for l in pr) and pr[-2:] == ["Ergebnis: 18 von 18 bestanden", "rc 0"], "p_probe.txt: 18 von 18, rc 0; Gegenprobe beide Seiten mit Zaehlzeile")
    ende()
BL_TEXT = (" · **Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110) mit TB-178 (%s, Journal %s)**: R109 (a) 59.1 ist Beleg, kein Ort; R110 (b) Ort ist `STARTING_CAPITAL` in `shared/handelskosten.py`, sobald das Modul "
    "als Nachtrag zu Punkt 9 mit Pfad und Hash auf der Sperrliste steht; **offen: Bauauftrag nach 37.3 in vier Schritten und die Probe in `shared/test_ergebniskurven.py` (R110 (b), (c); Handelscode, Vorschlag TB-180)**; "
    "R110 (a) später Symbolfall: Abnahme am Erzeuger mit TB-178 (Probe `docs/belege/TB-178/tb178_probe_spaetes_symbol.py`, Ergebnis siehe `p_probe.txt`) |")
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-178" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-178"):
        z[a[0]] = z[a[0]][:-2] + BL_TEXT % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-178: " % neu), "Kopfzeile ## %s — TB-178: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
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
    elif a == ["nachher"]: nachher()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

### Anhang B — Probe (Schritt P, nach `docs/belege/TB-178/tb178_probe_spaetes_symbol.py`)

<!-- DATEI tb178_probe_spaetes_symbol.py -->
````python
#!/usr/bin/env python3
"""TB-178 Probe nach R110 (a) (R109 (b), R108 (e), R107 (b), R106 (b)): der herbeigefuehrte spaete Symbolfall, Abnahme am Erzeuger
(research/tb24_haltedauern/positionen_holen.py, gestartet ueber test_listen_erzeuger.lauf in einem Temp-Ordner).
Snapshot (synthetisch, kein data/ des Repos): AAA, BBB, CCC (+ BTCUSDT bei Krypto) ab Achsenbeginn, SPAET mit spaetem Datenbeginn
(vor dem Schnitt). Der Handelbar-Tag jedes Symbols kommt aus der Rechnung nach 23.5 (faltenschranke_messung.handelbar_ab, R87 (a)) -
die Probe setzt KEINEN Tag (tags "{}"). Bedingung des Falls (R110 (a)): kein Symbol traegt vor seinem Tag ein Signal - bis zum
gerechneten Tag ein ruhiger, gleichmaessig fallender Vorlauf, ab dem Tag Zufallsweg (Seed). Je Bot, Wachen nach R86 (d) und R87 (c) an:
  S = Schranke am Tag (Modus "")   O = ohne Schranke (Modus "schranke_aus": hole_trades ohne handelbar)
Je Bot 6 Pruefungen: 1 Tage gerechnet, SPAET-Tag vor dem Schnitt und nach den Tagen der uebrigen; der Lauf nutzte die Rechnung
2 rc S = rc O = 0   3 Ausgaben bytegleich   4 Zaehlzeile entfernt 0 / nur in S 0; SPAET hat Trades, keiner vor seinem Tag
5 Lesehaken (nur Snapshot-Dateien)   6 Gegenprobe beide Seiten (40.7, 41.1 A5, R110 (a)): SPAET ohne ruhigen Vorlauf (Signal vor dem Tag) ->
  ohne Schranke rc 2 (R87 (c)); mit Schranke rc 0 und Zaehlzeile ueber 0 (Zeilen, die die Schranke gegenueber einem Lauf ohne Schranke
  und ohne Wachen entfernt).
Aufruf aus der Repo-Wurzel: <python> -B <diese Datei> [bot ...]  (rc 0 = alle bestanden; Soll 18 von 18)"""
import json, os, subprocess, sys
WURZEL = os.getcwd(); sys.path.insert(0, os.path.join(WURZEL, "research", "tb24_haltedauern"))
import numpy as np, pandas as pd
import test_listen_erzeuger as tle
SEED = int(os.environ.get("R109B_SEED", "178"))
START = {"1d": "2023-01-02", "4h": "2023-06-01", "1h": "2024-06-01", "aktien": "2019-01-02"}
MODUS = {"vorlauf": True}
def tage(bot, d):
    c = ("import sys, json; sys.path.insert(0, 'research/faltenplan_neun'); import faltenschranke_messung as f; "
         "print(json.dumps(f.handelbar_ab(%r)))" % bot)
    r = subprocess.run([sys.executable, "-B", "-c", c], cwd=WURZEL, capture_output=True, text=True, env=dict(os.environ, TB36_BASE_DIR=d))
    if r.returncode: raise SystemExit("Rechnung 23.5: rc %s %s" % (r.returncode, r.stderr[-300:]))
    return json.loads(r.stdout.strip().split("\n")[-1])
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    tf = tle.TF.get(bot, "1d"); t = tle.achse(bot, versatz); ak = bot in tle.AKTIEN
    syms = ["AAA", "BBB", "CCC"] + ([] if ak else ["BTCUSDT"]) + ["SPAET"]
    for u in ("data", "config", "strategies/" + bot, "research"): os.makedirs(os.path.join(d, u), exist_ok=True)
    import shutil; shutil.copy(os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"), os.path.join(d, "strategies", bot))
    os.symlink(os.path.join(WURZEL, "research", "universum_trockenlauf"), os.path.join(d, "research", "universum_trockenlauf"))
    open(os.path.join(d, "config", "top25_symbols.txt"), "w").write("" if ak else "\n".join(syms) + "\n")
    open(os.path.join(d, "config", "sp500_top150.txt"), "w").write("\n".join(syms) + "\n" if ak else "")
    st = pd.Timestamp(START["aktien" if ak else tf]); fmt = "%Y-%m-%d" if tf == "1d" else "%Y-%m-%d %H:%M:%S"
    tt = {s: t[(t < pd.Timestamp(tle.SCHNITT)) | bool(ab_schnitt)] for s in syms}; tt["SPAET"] = tt["SPAET"][tt["SPAET"] >= st]
    def schreibe(s, c, o, h, lo, vol):
        pd.DataFrame({"open_time": tt[s].strftime(fmt), "open": o, "high": h, "low": lo, "close": c, "volume": vol}).to_csv(
            os.path.join(d, "data", "%s_%s.csv" % (s, tf)), index=False)
    for s in syms: n = len(tt[s]); schreibe(s, *([np.ones(n)] * 4), np.full(n, 10**5))   # nur Zeitachse: die Rechnung liest Zeitstempel
    tg = tage(bot, d); json.dump(tg, open(os.path.join(d, "tage_rechnung.json"), "w"))
    for k, s in enumerate(syms):
        r = np.random.default_rng(seed + k); v = 0.012 if tf != "1d" else 0.025; n = len(tt[s])
        ruhig = (tt[s].normalize() < pd.Timestamp(tg[s])) if (tg.get(s) and (MODUS["vorlauf"] or s != "SPAET")) else np.zeros(n, bool)
        sch = r.normal(0.0001, v, n); sch[ruhig] = -0.0005
        c = 50 * np.exp(np.cumsum(sch)); o = c * (1 + np.where(ruhig, 0.0005, r.normal(0, v / 5, n)))
        h = np.maximum(o, c) * (1 + np.where(ruhig, 0.0002, np.abs(r.normal(0, v / 3, n))))
        lo = np.minimum(o, c) * (1 - np.where(ruhig, 0.0002, np.abs(r.normal(0, v / 3, n))))
        schreibe(s, c, o, h, lo, r.integers(10**5, 10**6, n))
tle.snapshot = snapshot
n = [0, 0]
def pruefe(t, ok, info=""):
    n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + t + (" · " + str(info) if info else ""), flush=True); return ok
def zeilen(liste): return set(liste.split("\n")[1:]) - {""} if liste else set()
for bot in (sys.argv[1:] or ["t3_supertrend", "elliott_wave", "elliott_wave_stocks"]):
    sd = (SEED, 0); MODUS["vorlauf"] = True
    S, O = tle.lauf(bot, sd, False, "", "{}"), tle.lauf(bot, sd, False, "schranke_aus", "{}")
    import tempfile
    with tempfile.TemporaryDirectory() as d: snapshot(bot, d, False, SEED); tg = json.load(open(os.path.join(d, "tage_rechnung.json")))
    sp = tg.get("SPAET"); andere = [v for k, v in tg.items() if k != "SPAET"]
    pruefe(bot + ": 1 Tage aus der Rechnung nach 23.5, kein Tag gesetzt; SPAET %s vor dem Schnitt und nach den uebrigen (%s); Lauf nutzte die Rechnung (spur %s)" % (sp, max(andere) if andere and None not in andere else andere, S["spaet"]),
           sp is not None and sp < tle.SCHNITT and None not in andere and sp > max(andere) and S["spaet"] == sp == O["spaet"])
    pruefe(bot + ": 2 rc S %s, rc O %s (Wachen R86 (d), R87 (c) an)" % (S["rc"], O["rc"]), S["rc"] == 0 and O["rc"] == 0, (S["fehler"] if S["rc"] else "") + (O["fehler"] if O["rc"] else ""))
    pruefe(bot + ": 3 Ausgaben S und O bytegleich (%s Zeichen)" % len(S["liste"] or ""), S["liste"] is not None and S["liste"] == O["liste"])
    zs, zo = zeilen(S["liste"]), zeilen(O["liste"]); x = tle.tab(S["liste"])
    xs = x[x["symbol"] == "SPAET"] if x is not None else None
    vor = None if xs is None or sp is None else int((xs["entry_time"].dt.normalize() < pd.Timestamp(sp)).sum())
    print("Zaehlzeile %s: Zeilen S %d, O %d; von der Schranke entfernt %d; nur in S %d; SPAET-Trades %s, davon vor dem Tag %s, erster Einstieg %s"
          % (bot, len(zs), len(zo), len(zo - zs), len(zs - zo), None if xs is None else len(xs), vor, None if xs is None or xs.empty else xs["entry_time"].min()), flush=True)
    pruefe(bot + ": 4 Zaehlzeile entfernt 0, nur in S 0; SPAET traegt Trades ab dem Tag, keinen davor", len(zs) > 0 and not (zo - zs) and not (zs - zo) and xs is not None and len(xs) > 0 and vor == 0)
    pruefe(bot + ": 5 Lesehaken: nur Snapshot-Dateien gelesen (S %d, O %d)" % (S["gelesen"], O["gelesen"]), not S["fremd"] and not O["fremd"] and S["gelesen"] > 0 and O["gelesen"] > 0, (S["fremd"] + O["fremd"])[:2])
    MODUS["vorlauf"] = False
    S2, O2, O3 = tle.lauf(bot, sd, False, "", "{}"), tle.lauf(bot, sd, False, "schranke_aus", "{}"), tle.lauf(bot, sd, False, "schranke_aus+wachen_aus", "{}")
    MODUS["vorlauf"] = True
    weg = len(zeilen(O3["liste"]) - zeilen(S2["liste"])) if O3["liste"] and S2["liste"] else None
    print("Zaehlzeile Gegenprobe %s: mit Schranke rc %s, Zeilen %d; ohne Schranke und Wachen Zeilen %d; Zeilen nur ohne Schranke und Wachen %s"
          % (bot, S2["rc"], len(zeilen(S2["liste"])), len(zeilen(O3["liste"])), weg), flush=True)
    pruefe(bot + ": 6 Gegenprobe beide Seiten (40.7, R110 (a)): SPAET mit Signal vor dem Tag -> ohne Schranke rc %s (%s); mit Schranke rc %s, Zaehlzeile (Zeilen nur ohne Schranke) %s"
           % (O2["rc"], O2["fehler"][:90] if O2["rc"] else "kein Abbruch", S2["rc"], weg), O2["rc"] == 2 and "R87 (c)" in O2["fehler"] and S2["rc"] == 0 and bool(weg))
print("Ergebnis: %d von %d bestanden" % (n[1], n[0])); sys.exit(0 if n[0] and n[0] == n[1] else 1)
````

