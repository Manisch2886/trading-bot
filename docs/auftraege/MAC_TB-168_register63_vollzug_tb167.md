# TB-168 Register 63: Vollzug TB-167 (Hash-Übergang nach 37.3, Abhilfe G6 elliott_wave_stocks) und Berichtigung Dialog-Index 16a — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 16.10.2026, 14:22** (Helfer BAU168, per Skript aus Bausteinen, `$HOME/sc/tb168/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 an Kopien simuliert. **Gebaut am HEAD `2ccec1c`.**

**Sitzungstitel:** `TB-168` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `2ccec1cfdf281da2a0ef1c18abaae0232e02c67d` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-168`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`; Werkzeug `docs/belege/TB-168/tb168_werkzeug.py` (Anhang A) kurz `WZ`. **Belege:** `docs/belege/TB-168/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-168_register63_vollzug_tb167.md`.
**Grundlage:** Vorbild TB-164 (Register 60, Vollzug TB-163: Commits `1d037f9`, `92cb637`, `3dfa3ba`, `67167a4`, `a9bf4a7`); Entwurf `docs/ERGEBNIS_TB-167_g6_ews_schranke_vor_schnitt.md` Z. 45–51; 62.5 (a) (Register Z. 12349); Befund K aus TB-167 (ERGEBNIS_TB-167 Z. 27–28, 43). **Zeitgrenze:** jeder Bash-Aufruf mit dem Parameter `timeout` des Bash-Werkzeugs, 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V (Voraussetzungen) ⇒ S (Sperrlisten-Sonde, lesend) ⇒ N (Register 63) ⇒ K (Kopien, Index, Dialog-Index mit Berichtigung 16a) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe).

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 31 („Opus Trading Bots-16.10.2026 a“), 16.10.2026, 14:10, Frage und Antwort im Wortlaut (aus logs/steuernder_chat/2026-10-16_BETREIBER_chat31_karten.md, per Skript): Your questions have been answered: "Freigabe Vollzug TB-168? TB-167 ist fertig, HEAD 2ccec1c (gepusht). Gemessen in Schritt M: Gegenprobe am alten Code mit genau einem Fehler (G6 ews, Falten 2021–2025); nach der Abhilfe test_vorregistrierung 196/196, G6 grün, test_posten4_horizont 34/34, Selektionsfalten für ews 2017–2025. ews-Optimierer sha256 3b775700… ⇒ 0298263c…; geändert ist nur die Reihenfolge plus eine Kommentarzeile. Der Vollzug nach 37.3 trägt den neuen Hash in die Sperrliste ein, mit Tatsachennotiz und Registerkopie, nach dem Vorbild TB-164. Kein Lauf auf Kursdaten, kein Live, kein Geld. Der Auftrag wird gerade gebaut und gegengelesen; deine Freigabe kommt im Wortlaut hinein, gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben."="Ja, freigeben (Recommended)"

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. `WZ register` übernimmt diese Zeile wörtlich in den Kopfsatz von 63.

## Was eingetragen wird — Wortlaute per Skript

- **37.3** (Register Z. 7025): „Ein Befund 1 der Sperrlisten-Sonde vor dem signierten Tag ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein neues Abbild unter neuem Namen geschlossen, nie durch Anpassung des alten.“
- **62.5 (a)** (Register Z. 12349): „Vollzug und Hash-Übergang nach 37.3 kommen als Tatsachennotiz mit einem Folgeauftrag (Bauart 60). Bis dahin offen.“
- **Entwurf** `docs/ERGEBNIS_TB-167_g6_ews_schranke_vor_schnitt.md` (md5 `2267e7334770a6ef950dcf2f782af75a`, zuletzt geändert in `9449f6f`): Z. 45 ist die Überschrift `## Entwurf der Tatsachennotiz nach 37.3` (wird nicht übernommen), **Z. 47–51** der Entwurf (Tabelle Z. 47–49, Satz Z. 51) = `docs/belege/TB-167/m_uebergang.md`. Zeile: `elliott_wave_stocks/multi_symbol_optimise.py` vorher `3b775700…` ⇒ nachher `0298263c…`, Commit `b6aaa24`, vollzieht „R102 (c) (Posten 4; R44, R81 (d); E-6 berichtigt)“.
- **Freigabe von TB-167** (im Entwurf nur „Karte im Auftrag TB-167“): `docs/auftraege/MAC_TB-167_g6_ews_schranke_vor_schnitt.md` Z. 13 (Karte, wörtlich) und Z. 15 (Bedingung); gemessen erfüllt in TB-167 Schritt M (`docs/belege/TB-167/m1_*` bis `m6_*`, ERGEBNIS_TB-167 Z. 29–37).

**Abschnitt 63** (`WZ register`, append-only): Titel `## 63. Vollzug TB-167 (Tatsachennotiz nach 37.3; Abhilfe G6 elliott_wave_stocks) (TB-168)`, Kopfsatz mit der Karte oben wörtlich und dem Verweis auf 62.5 (a); **63.1** mit Quellkopf (Datei, Z. 47–51, Commit, md5), den 5 Zeilen **zeichengleich**, der Karte von TB-167 (Z. 13 zeichengleich) mit Bedingung (Z. 15) und den neun Belegen aus Schritt M, danach der **Sondensatz** in genau einer von zwei Fassungen, gewählt per Skript aus `BEL/s_sonde.txt` (wie TB-164): Punkt 11 `2` ⇒ „nicht prüfbar“; Punkt 11 `1` und Befund nur an Punkt 11 ⇒ „Befund 1 (beauftragt)“. Jeder andere Beleg ⇒ keine Fassung ⇒ **ABBRUCH**. Keine Marke (wie 60).

**Berichtigung Dialog-Index 16a** (Befund K aus TB-167): `dialog_index.py --pruefen` verlangt `offen` in {ja, nein} (`docs/werkzeuge/dialog_index.py` Z. 14, 156); Zeile 16a trägt „–“. `WZ handfelder` schreibt ein JSON nur für 16a: Frage und Entscheidung wie im Index, `offen` = **`nein`** (Wert des steuernden Chats). Kein Regeltext, kein anderes Handfeld.

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen. **Kein neues Abbild** (`sperrliste_abbild.py` läuft nicht). Nichts unter `strategies/`, `shared/`, `data/`, `config/`, `research/` ändern. Die Sonde läuft genau einmal, lesend (Schritt S). Kein Live, kein Broker, kein Geld; `positionen_holen.py` nie. Kein `git add -A`, kein `-f`, kein `git stash`, kein `rm`. **Schreiben darf die Sitzung nur:** `docs/VORREGISTRIERUNG_neuselektion.md` (N, nur `WZ register`, append-only), `docs/projektfuehrung/REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Werkzeugen), `docs/projektfuehrung/BACKLOG.md` (`WZ backlog`), `docs/projektfuehrung/JOURNAL.md` (`WZ journal`), `BEL`, das Ergebnis. `ERGEBNIS_TB-167` wird **nicht** geändert.

## Lage nach dem Auslegen

Am Bau-HEAD `2ccec1c`: Arbeitsbaum sauber (gemessen vom steuernden Chat, 16.10.2026, 14:04). Das Auslegen ändert dazu `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab. **Beim Start genau 2 Einträge** (Soll in 0a).

## Belegt · erschlossen · offen (am Bau)

**Belegt:** HEAD `2ccec1c`; Register endet mit 62, 63 fehlt; ews hat heute den „nachher“-Hash des Entwurfs; das Abbild `46f0ad5d1d83a253…` enthält keinen Pfad `multi_symbol_optimise`; Dialog-Index Zeile 16a `offen` „–“. **An einer Kopie** liefen Schritt 0 (Fall „normal“ bis Commit S0, Fall „0a weicht ab“ mit ABBRUCH vor S0) sowie `WZ voraussetzung` mit einer Simulationskarte (30 Prüfungen, NEIN 0; ohne gefüllte Karte ebenfalls 30 Prüfungen mit genau einem NEIN, doch dann bricht schon 0a ab), `WZ register --probe` mit dem Sonden-Beleg aus TB-164 und `WZ handfelder`. **Erschlossen:** Die Sonde meldet zu Punkt 11 voraussichtlich `2` „nicht prüfbar“ wie in TB-164 (`docs/belege/TB-164/s_auswahl.txt`); gewählt wird erst aus dem Beleg in S. **Offen:** neues Abbild (37.3; nicht Teil).

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `2ccec1cfdf281da2a0ef1c18abaae0232e02c67d`, genau diese 2 Einträge, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
?? docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md
```

```bash
# S0-1 0a
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb168_0a.txt", "w", encoding="utf-8").write(st)
soll = [" M docs/auftraege/AKTUELLER_AUFTRAG.md", "?? docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md"]
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "2ccec1cfdf281da2a0ef1c18abaae0232e02c67d": f.append("HEAD " + g("rev-parse", "HEAD").strip())
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md", encoding="utf-8").read().split("\n")
a = z.index("## Freigabe — Karte des Betreibers, wörtlich"); b = next(i for i in range(a + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a + 1:b] if l.startswith("> ")]
if len(k) != 1 or ("⟪" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (2 Eintraege)`. Werkzeug aus Anhang A holen (genau dieser Befehl):

```bash
# S0-2 Anhang
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md "$TMPDIR" <<'PYEOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2] + "/tb168_werkzeug.py", "w", encoding="utf-8").write(t)
print("tb168_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
PYEOF
```

Soll genau: `tb168_werkzeug.py b55789f15345b15586f53c26b45cc7abc4435311b099740d76a96d089cb7d64f`; sonst **ABBRUCH**. Dann Commit mit genau diesen Pfaden, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```bash
# S0-3 Commit
git add docs/auftraege/AKTUELLER_AUFTRAG.md && git add docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md && git commit -q -m "TB-168 Schritt 0: Stand des steuernden Chats vor TB-168" && git push -q && git status --porcelain
```

Soll: keine Ausgabe. Erst danach:

```bash
# S0-4 Belege
mkdir -p docs/belege/TB-168 && cp "$TMPDIR/tb168_0a.txt" docs/belege/TB-168/0a_status.txt && cp "$TMPDIR/tb168_werkzeug.py" docs/belege/TB-168/tb168_werkzeug.py && diff "$TMPDIR/tb168_0a.txt" docs/belege/TB-168/0a_status.txt && diff "$TMPDIR/tb168_werkzeug.py" docs/belege/TB-168/tb168_werkzeug.py
```

Soll: keine Ausgabe.

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py voraussetzung > docs/belege/TB-168/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0`, davor `Pruefungen: 30, NEIN: 0` (Register 62 da, 63 nicht; Vorbild 60 Z. 12177 und 60.1 Z. 12181; 37.3; 62.5 (a); ERGEBNIS_TB-167 md5, Commit, Grenzen, Z. 47–51 = `m_uebergang.md`, Zeile des Entwurfs; ews heute = nachher; MAC_TB-167 md5, Z. 11/13/15; neun Belege aus M; Abbild und Sonde; Karte TB-168; Dialog-Index 16a; Wert für 16a; Anker in Index, BACKLOG, Journal). Sonst **ABBRUCH**.

## Schritt S — Sperrlisten-Sonde, lesend (Aufruf wie TB-164 Schritt S)

Genau diese fünf Befehle nacheinander:

```
git status --porcelain > "$TMPDIR/tb168_s_vor.txt"
trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json > "$TMPDIR/tb168_sonde.txt" 2>&1; echo "rc $?" >> "$TMPDIR/tb168_sonde.txt"
git status --porcelain > "$TMPDIR/tb168_s_nach.txt"
cp "$TMPDIR/tb168_sonde.txt" docs/belege/TB-168/s_sonde.txt
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py sonde docs/belege/TB-168/s_sonde.txt "$TMPDIR/tb168_s_vor.txt" "$TMPDIR/tb168_s_nach.txt" > docs/belege/TB-168/s_auswahl.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/s_auswahl.txt
```

Soll: `s_auswahl.txt` endet mit `rc 0` und nennt `Fassung: nicht prüfbar` oder `Fassung: Befund 1 (beauftragt)` und den Satz für 63.1. Sonst (keine Fassung, porcelain vor/nach verschieden, Hash von Abbild oder Sonde anders) **ABBRUCH**. Kein Commit in S; die Belege gehen mit N.

## Schritt N — Register 63

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-168/s_sonde.txt --probe > docs/belege/TB-168/n_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/n_probe.txt
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-168/s_sonde.txt > docs/belege/TB-168/n_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/n_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach steht am Registerende `## 63. Vollzug TB-167 (Tatsachennotiz nach 37.3; Abhilfe G6 elliott_wave_stocks) (TB-168)` mit 63.1. Commit `TB-168 N: Register 63 (Vollzug TB-167)`, pushen ⇒ **⟨N⟩**.

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-168/0a_status.txt
git add docs/belege/TB-168/tb168_werkzeug.py
git add docs/belege/TB-168/v_voraussetzung.txt
git add docs/belege/TB-168/s_sonde.txt
git add docs/belege/TB-168/s_auswahl.txt
git add docs/belege/TB-168/n_probe.txt
git add docs/belege/TB-168/n_eintrag.txt
```

## Schritt K — Kopien, Index, Dialog-Index mit Berichtigung 16a (wie TB-164 Schritt K)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-168/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-168/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-168/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨N⟩ > docs/belege/TB-168/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-168/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_index.txt
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py handfelder docs/belege/TB-168/k_handfelder.json > docs/belege/TB-168/k_handfelder.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_handfelder.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-168/k_handfelder.json > docs/belege/TB-168/k_dialog_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_dialog_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-168/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`; `k_dialog_pruefen.txt` nennt `65 von 65` (vorher 64 von 65, TB-167). `registerkopie.py` schreibt Teildateien und Abschnittskopien neu (63 neu); `c2_index_zeilen.py` (aus TB-154, unverändert) schreibt die Zeilenangaben von ⟨S0⟩ auf ⟨N⟩ um; `WZ index` setzt Kopf (0–63), Zeile 63 und die Pflegezeile; `WZ handfelder` nur 16a. Entsteht eine weitere Teildatei: mit Namen anpassen, melden. rc ≠ 0 eines Schritts: festhalten, die Dateien dieses Schritts nicht committen, melden (kein Abbruch). Von Hand ist danach nichts zu tun: die nicht committeten Dateien bleiben im Arbeitsbaum liegen (nicht zurücksetzen, kein `git restore`), stehen damit in `f_porcelain.txt` und im Ergebnis unter Abweichungen; über den Rest entscheidet der steuernde Chat. Commit `TB-168 K: Registerkopie, Index, Dialog-Index`, pushen ⇒ **⟨K⟩**.

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
git add docs/belege/TB-168/k_registerkopie.txt
git add docs/belege/TB-168/k_abschnitte.txt
git add docs/belege/TB-168/k_pruefen.txt
git add docs/belege/TB-168/k_index_zeilen.txt
git add docs/belege/TB-168/k_index.txt
git add docs/belege/TB-168/k_handfelder.json
git add docs/belege/TB-168/k_handfelder.txt
git add docs/belege/TB-168/k_dialog_index.txt
git add docs/belege/TB-168/k_dialog_pruefen.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py kennung > docs/belege/TB-168/a_kennung.txt; echo "rc $?" >> docs/belege/TB-168/a_kennung.txt` (Soll „Kennung FD …“, `rc 0`). Dann:

```
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-168/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-168/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/a_backlog.txt
```

Block nach `BEL/a_block.md` (Schreibwerkzeug; erste Zeile `## <Kennung> — TB-168: …`, Quellenzeile, `**Quelle:**`, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; keine weitere `## `-Zeile, kein `---`), dann:

```
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py journal docs/belege/TB-168/a_block.md --probe > docs/belege/TB-168/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-168/tb168_werkzeug.py journal docs/belege/TB-168/a_block.md > docs/belege/TB-168/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-168/a_journal.txt
```

Soll je `rc 0`; endet eine Probe nicht mit `rc 0`: zweiten nicht ausführen, **ABBRUCH**. **Ergebnis** `docs/ERGEBNIS_TB-168_register63_vollzug_tb167.md` (Schreibwerkzeug): Kopf mit Commits · „Kurz“ · Voraussetzungen (`v_voraussetzung.txt` wörtlich) · **Sonde** (Aufruf; aus `s_sonde.txt` die Zeilen `Punkt 11`, `RUECKGABEWERT` und `rc` wörtlich; `s_auswahl.txt` wörtlich) · Register 63 (Zeile, numstat) · K (je rc; Dialog-Index vorher 64, nachher 65 von 65; Zeile 16a vorher/nachher) · BACKLOG (Rang 1) · **Offen:** neues Abbild (37.3; nicht Teil), R102 (d) (62.5 (b)), TB-166 E-3a neu auf diesem Stand, Urteil zum Befund R100 (c), Sicherung `$HOME/tb167_sicherung` · Abweichungen · **In einfacher Sprache** (drei bis fünf Sätze, ohne Kürzel). Dann:

```
git add docs/ERGEBNIS_TB-168_register63_vollzug_tb167.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-168/a_kennung.txt
git add docs/belege/TB-168/a_backlog_probe.txt
git add docs/belege/TB-168/a_backlog.txt
git add docs/belege/TB-168/a_block.md
git add docs/belege/TB-168/a_journal_probe.txt
git add docs/belege/TB-168/a_journal.txt
```

Commit `TB-168 Abgabe: Ergebnis, BACKLOG, Journal FD`, pushen ⇒ **⟨F⟩**. Zuletzt `git status --porcelain > "$TMPDIR/tb168_f.txt"`, `cp "$TMPDIR/tb168_f.txt" docs/belege/TB-168/f_porcelain.txt`, `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-168/f_numstat.txt` (Soll: Register Spalte 2 = `0`; kein Pfad unter `strategies/`, `shared/`, `data/`, `config/`, `research/`), dann:

```
git add docs/belege/TB-168/f_porcelain.txt
git add docs/belege/TB-168/f_numstat.txt
```

Commit `TB-168 F: porcelain und numstat`, pushen.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab (Zweig, HEAD, Einträge, Karte leer); Holbefehl-Soll weicht ab; V nicht `rc 0`; S: `s_auswahl.txt` nicht `rc 0` (keine Fassung); `WZ register --probe`/`register` nicht `rc 0`; `WZ backlog`/`journal` nicht `rc 0`; `git push` scheitert zweimal (nicht für den Abbruch-Commit); Claude Code verlangt eine Bestätigung (melden, nicht umgehen). **Kein Abbruch:** ein Schritt in K mit rc ≠ 0.
**Abbruchweg:** vor ⟨S0⟩ nichts schreiben, nur melden. Danach genau eine neue Datei `printf '%s\n' "<Schritt>: <Grund>" > docs/belege/TB-168/abbruch.txt`, `git add` dieser Datei und jeder schon entstandenen, nicht committeten Belegdatei unter `docs/belege/TB-168/` mit Namen (nie `git add -A`, nie `-f`; keine Datei ausserhalb `docs/belege/TB-168/`), Commit `TB-168 Abbruch: <Schritt>`, pushen (scheitert der Push: melden, nicht wiederholen), melden. Bei einem Abbruch nach `WZ register` (vor ⟨N⟩) bleibt das Register im Arbeitsbaum geändert — das steht in der Meldung; nicht zurücksetzen.

## In einfacher Sprache

Die Sitzung trägt eine Tatsache ins Register ein, nur angehängt: die alte und die neue Prüfsumme der Datei des Bots elliott_wave_stocks, die TB-167 mit Freigabe geändert hat — wortgleich aus dem Ergebnis von TB-167, dazu die Freigabe des Betreibers im Wortlaut. Vorher misst sie einmal lesend die Sperrlisten-Sonde; je nach Antwort steht im Register „nicht prüfbar“ oder „Befund 1 (beauftragt)“. Danach berichtigt sie eine Lücke im Verzeichnis der Fable-Antworten: Bei der Antwort vom 16.10. a fehlte die Angabe, ob noch etwas offen ist. Es läuft nichts auf Kursdaten, kein Code wird geändert.

## Anhang A — Werkzeug (sha256 `b55789f15345b15586f53c26b45cc7abc4435311b099740d76a96d089cb7d64f`)

### Werkzeug

```python
#!/usr/bin/env python3
"""TB-168 Werkzeug (Anhang A): Voraussetzungen, Auswahl aus dem Sonden-Beleg, Register 63 (Vollzug TB-167 nach 37.3), Index, Handfelder 16a, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  voraussetzung                           Voraussetzungen messen (rc 0 = alle ja)
  sonde <BELEG> <VOR> <NACH>              Fassung des Sondensatzes aus dem Beleg waehlen
  register <DATUM> <S0> <BELEG> [--probe] Abschnitt 63 am Registerende anhaengen (63.1 zeichengleich aus ERGEBNIS_TB-167 Z. 47-51)
  index <S0> <DATUM> [--probe]            REGISTER_INDEX.md: Kopf 0-63, Zeile 63, Pflegezeile (nach c2_index_zeilen.py)
  handfelder <ZIEL>                       JSON nur fuer 16a: Frage und Entscheidung wie im Index, offen = Wert des steuernden Chats
  backlog <DATUM> <KENNUNG> [--probe]     BACKLOG: Rang 1
  kennung | journal <BLOCK> [--probe]     naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, re, os, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
DIX, DWZ, DWZ_SHA = "docs/projektfuehrung/FABLE_DIALOG_INDEX.md", "docs/werkzeuge/dialog_index.py", "3735aa226af0bcdb2e298d324e54ccf91a9714417d7fe5641ee46c26e000e354"
ERG, ERG_MD5, ERG_COMMIT, UEB = "docs/ERGEBNIS_TB-167_g6_ews_schranke_vor_schnitt.md", "2267e7334770a6ef950dcf2f782af75a", "9449f6f", "docs/belege/TB-167/m_uebergang.md"
M167, M167_MD5, M167_COMMIT = "docs/auftraege/MAC_TB-167_g6_ews_schranke_vor_schnitt.md", "188606f7f8f35bef33a7a34530f84203", "bc5e165"
AUF = "docs/auftraege/MAC_TB-168_register63_vollzug_tb167.md"
AB, AB_SHA, SO, SO_SHA = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json", "46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f", "shared/sperrlistensonde.py", "98c02e0e9b42831d88e0cd9cbdc39d64c458691fdbf1e650aa4e32c933cc0d71"
EWS, EWS_ALT, EWS_NEU, ABH = "strategies/elliott_wave_stocks/multi_symbol_optimise.py", "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232", "0298263c755c5d24ccff09c35aa447efd4fff70f05223942813361955e0362e6", "b6aaa24"
SONDE_BEFEHL = "trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild " + AB
TITEL62 = "## 62. Fable 15b und 16b — Registerblöcke R100–R103 (TB-167)"
TITEL60 = "## 60. Vollzug TB-163 (Tatsachennotiz nach 37.3) und Tatsachennotiz Posten 5 (TB-164)"
TITEL601 = "### 60.1 Vollzug TB-163 (Tatsachennotiz nach 37.3)"
TITEL63 = "## 63. Vollzug TB-167 (Tatsachennotiz nach 37.3; Abhilfe G6 elliott_wave_stocks) (TB-168)"
S373, Z373 = "Ein Befund 1 der Sperrlisten-Sonde", 7025
A625 = "(a) R102 (c): gemessen nach diesem Eintrag in Schritt M von TB-167"
OFFEN16A = "nein"
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; als Nächstes Vollzug nach 37.3 (Bauart 60) und TB-166 E-3a neu auf diesem Stand |"
MBEL = [("m1_test_alt.txt", "rc 1"), ("m1_g6_rot.txt", "rc 0"), ("m2_plan_alt.txt", "rc 0"), ("m3_code_probe.txt", "rc 0"), ("m3_code.txt", "rc 0"),
        ("m4_test_neu.txt", "rc 0"), ("m4_g6_gruen.txt", "rc 0"), ("m5_posten4.txt", "rc 0"), ("m6_plan_neu.txt", "rc 0")]
FASSUNG = {"2": "nicht prüfbar", "1": "Befund 1 (beauftragt)"}
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True, text=True).stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def quelle():
    e = lies(ERG); z = e.split("\n"); return e, z, z[46:51]
def karte168():
    """Die Karte zu TB-168 aus dem Abschnitt Freigabe dieses Auftrags (eine Zeile '> ...'); None, wenn nicht gefuellt."""
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
    k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    if len(k) != 1 or ("⟪" + "FREIGABE") in k[0]: return None
    return k[0][2:].strip()
def karte167():
    t = lies(M167); z = t.split("\n"); return t, z
def zeile16a():
    t = [l for l in lies(DIX).split("\n") if l.startswith("| 16a |")]
    if len(t) != 1: return None
    return [x.strip() for x in t[0].strip().strip("|").split("|")]
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def fassung(beleg):
    """Punkt 11 aus dem Beleg: '2' (nicht pruefbar, Rueckgabe 2 ohne Befund) oder '1' (Befund nur an Punkt 11); sonst None."""
    z = lies(beleg).rstrip("\n").split("\n"); m = [re.match(r"^  Punkt 11  \[(\d) ", l) for l in z]; m = [x.group(1) for x in m if x]
    rw = [l for l in z if l.startswith("RUECKGABEWERT ")]; rc = z[-1] if z else ""
    if len(m) != 1 or len(rw) != 1: return None, m, rw, rc
    if m[0] == "2" and rc == "rc 2" and rw[0].startswith("RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [") and re.search(r"[\[ ]11[,\]]", rw[0]): return "2", m, rw, rc
    if m[0] == "1" and rc == "rc 1" and rw[0] == "RUECKGABEWERT 1 BEFUND - BEFUND in Punkt(en) [11]": return "1", m, rw, rc
    return None, m, rw, rc
def satz(f, s0):
    kopf = "**Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-168 am Stand `%s`; Aufruf wie TB-164 Schritt S: `%s`, Abbild `%s…`; Beleg `docs/belege/TB-168/s_sonde.txt`): " % (s0, SONDE_BEFEHL, AB_SHA[:8])
    if f == "2": return kopf + "Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keinen der Optimierer (kein Pfad `strategies/*/multi_symbol_optimise.py` darin) — wie bei 60.1. Der Übergang steht deshalb nur hier und in den Commits."
    return kopf + "Punkt 11 „Befund 1 (beauftragt)“ (`1`). Vor dem Tag zulässig nach 37.3, weil beauftragt (Freigabe: Karte unten); geschlossen wird er durch ein neues Abbild unter neuem Namen (37.3), das TB-168 nicht zieht."
def voraussetzung():
    reg = lies(REG); z = reg.split("\n")
    p(sum(l == TITEL62 for l in z) == 1 and not re.search(r"^## 63\. ", reg, re.M), "Register: 62 genau einmal, 63 noch nicht")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    t60 = [i + 1 for i, l in enumerate(z) if l == TITEL60]; t601 = [i + 1 for i, l in enumerate(z) if l == TITEL601]
    p(t60 == [12177] and t601 == [12181], "Register: Vorbild 60 genau einmal, Z. %s; 60.1 genau einmal, Z. %s" % (t60, t601))
    t373 = [i + 1 for i, l in enumerate(z) if S373 in l.replace("**", "")]; p(t373[:1] == [Z373], "Register: 37.3 „%s“ zuerst Z. %d (%d Treffer)" % (S373, Z373, len(t373)))
    a = [i + 1 for i, l in enumerate(z) if l.startswith(A625)]; p(len(a) == 1 and "(Bauart 60)" in z[a[0] - 1] and z[a[0] - 1].endswith("Bis dahin offen."), "Register: 62.5 (a) genau einmal, Z. %s, nennt Bauart 60 und „Bis dahin offen.“" % a)
    e, ez, q = quelle()
    p(md5(e) == ERG_MD5, "ERGEBNIS_TB-167 md5 %s" % ERG_MD5)
    p(git("log", "--format=%h", "-1", "--", ERG).strip()[:7] == ERG_COMMIT, "ERGEBNIS_TB-167 zuletzt in Commit %s" % ERG_COMMIT)
    p(ez[44] == "## Entwurf der Tatsachennotiz nach 37.3" and ez[45] == "" and q[0] == "| Datei | vorher | nachher | Commit | vollzieht |" and q[3] == ""
      and q[4].startswith("Entwurf, nicht eingetragen (TB-167, ") and ez[51] == "" and ez[52] == "## Was offen bleibt", "ERGEBNIS_TB-167: Z. 45 Kopf, Z. 47-51 Entwurf, Z. 52 leer, Z. 53 'Was offen bleibt'")
    p("\n".join(q) + "\n" == lies(UEB), "ERGEBNIS_TB-167 Z. 47-51 = %s" % UEB)
    w = q[2].split(" | ")
    p(w[0] == "| `%s`" % EWS and w[1] == "`%s`" % EWS_ALT and w[2] == "`%s`" % EWS_NEU and w[3] == "`%s`" % ABH, "Entwurf: Datei, vorher %s…, nachher %s…, Commit %s" % (EWS_ALT[:16], EWS_NEU[:16], ABH))
    p(sha(EWS) == EWS_NEU and git("log", "--format=%h", "-1", "--", EWS).strip()[:7] == ABH, "sha256 heute = nachher, zuletzt in Commit %s" % ABH)
    t, mz = karte167()
    p(md5(t) == M167_MD5 and git("log", "--format=%h", "-1", "--", M167).strip()[:7] == M167_COMMIT, "MAC_TB-167 md5 %s, Commit %s" % (M167_MD5, M167_COMMIT))
    p(mz[10] == "## Freigabe des Betreibers (R102 (c), 37.3) — Karte, wörtlich" and mz[12].startswith("> Karte des Betreibers im Chat 31") and mz[14].startswith("Die Freigabe gilt nur, wenn"), "MAC_TB-167: Z. 11 Kopf, Z. 13 Karte, Z. 15 Bedingung")
    for f, s in MBEL:
        b = "docs/belege/TB-167/" + f; p(os.path.isfile(b) and lies(b).rstrip("\n").split("\n")[-1] == s, "TB-167 %s endet mit %s" % (f, s))
    p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild %s… und Sonde %s…" % (AB_SHA[:16], SO_SHA[:16]))
    p("multi_symbol_optimise" not in lies(AB), "Abbild führt keinen Optimierer")
    k = karte168(); p(k is not None, "Freigabe-Karte TB-168 gefüllt, eine Zeile: %s" % ((k or "-")[:120]))
    r = zeile16a(); p(r is not None and r[6] == "–" and sha(DWZ) == DWZ_SHA, "Dialog-Index: Zeile 16a genau einmal, offen „–“; dialog_index.py %s…" % DWZ_SHA[:16])
    p(OFFEN16A in ("ja", "nein"), "Wert für 16a offen: %s" % OFFEN16A)
    ix = lies(IDX).split("\n")
    p(sum(l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `") and "Abschnitte 0–62" in l for l in ix) == 1 and sum(l.startswith("| 62 aus 15b und 16b |") for l in ix) == 1
      and sum(l.startswith("Zuletzt nachgezogen in TB-167 (") for l in ix) == 1, "Index: Kopf 0–62, Zeile 62, Pflegezeile TB-167 je genau einmal")
    bl = lies(BL).split("\n"); p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl) == 1, "BACKLOG: Rang 1 (Stand TB-167) genau einmal")
    k = kennungen(); p(max(k) == "FC" and naechste(max(k)) not in k, "Journal: höchste Kennung %s, nächste %s frei" % (max(k), naechste(max(k))))
    ende()
def sonde(beleg, vor, nach):
    p(lies(vor) == lies(nach), "git status --porcelain vor und nach der Sonde gleich (%d Zeilen)" % len([l for l in lies(vor).split("\n") if l]))
    p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild %s… und Sonde %s…" % (AB_SHA[:16], SO_SHA[:16]))
    f, m, rw, rc = fassung(beleg)
    p(f is not None, "Punkt 11 im Beleg: %s · %s · %s" % (m, rw[0][:160] if rw else "kein RUECKGABEWERT", rc))
    if f: print("Fassung: %s" % FASSUNG[f]); print("Satz 63.1 (⟨S0⟩ setzt WZ register): " + satz(f, "⟨S0⟩"))
    ende()
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    f = fassung(beleg)[0]; p(f is not None, "Fassung aus dem Beleg: %s" % FASSUNG.get(f, "keine"))
    e, ez, q = quelle(); p(md5(e) == ERG_MD5 and len(q) == 5, "Quelle ERGEBNIS_TB-167 md5 %s, Z. 47-51 (5 Zeilen)" % ERG_MD5)
    t, mz = karte167(); p(md5(t) == M167_MD5 and mz[12].startswith("> Karte des Betreibers im Chat 31"), "Karte TB-167: MAC_TB-167 md5 %s, Z. 13" % M167_MD5)
    k = karte168(); p(k is not None, "Karte TB-168 gefüllt")
    z = lies(REG).split("\n"); p(not any(l.startswith("## 63. ") for l in z) and z[-1] == "" and z[-2] != "", "63 noch nicht im Register; endet mit einer Leerzeile")
    a = [i + 1 for i, l in enumerate(z) if l.startswith(A625)]; p(len(a) == 1, "62.5 (a) genau einmal, Z. %s" % a)
    t601 = [i + 1 for i, l in enumerate(z) if l == TITEL601]; p(t601 == [12181], "Vorbild 60.1 genau einmal, Z. %s" % t601)
    p("multi_symbol_optimise" not in lies(AB), "Abbild führt keinen Optimierer")
    if nein(): ende()
    kopf = ("Reines Eintragen, Bauart 60.1 (Register Z. %d ff.); Karte des Betreibers (Auftrag TB-168, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-168 (Stand `%s`). "
            "Vollzieht 62.5 (a) (Z. %d); 62.5 (a) bleibt zeichengleich. Nichts entfernt, kein bestehender Satz umgeschrieben; kein neues Abbild; keine Marke.") % (t601[0], k, datum, s0, a[0])
    q1 = ("*Übernommen zeichengleich aus dem Entwurf in `%s` Z. 47–51 (Commit `%s`, md5 `%s`); Z. 45 ist die Überschrift des Entwurfs und gehört nicht dazu; Z. 47–51 sind `%s`. Vollzogen in Commit `%s` (TB-167 M). "
          "„Entwurf, nicht eingetragen“ darin beschreibt den Stand im Ergebnis; eingetragen ist der Übergang mit diesem Abschnitt.*") % (ERG, ERG_COMMIT, ERG_MD5, UEB, ABH)
    fk = ("**Freigabe-Karte, wörtlich** (zu „Freigabe: Karte im Auftrag TB-167“ im Entwurf; aus `%s` Z. 13, Commit `%s`, md5 `%s`):") % (M167, M167_COMMIT, M167_MD5)
    bd = ("Bedingung dazu (ebenda Z. 15): „%s“ Gemessen in TB-167 Schritt M vor dem Commit `%s`: %s.") % (mz[14], ABH, ", ".join("`docs/belege/TB-167/%s` %s" % (f_, s_) for f_, s_ in MBEL))
    neu = ["", TITEL63, "", kopf, "", "### 63.1 Vollzug TB-167 (Tatsachennotiz nach 37.3)", "", q1, ""] + q + ["", fk, "", mz[12], "", bd, "", satz(f, s0), ""]
    if probe: ende()
    alt = lies(REG); schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG); p(r2.startswith(alt[:-1]) and r2.count("\n" + TITEL63 + "\n") == 1, "nachher: altes Register unverändert vorn (append-only), 63 genau einmal, Z. %d" % (r2.split("\n").index(TITEL63) + 1))
    p("\n" + "\n".join(q) + "\n" in r2 and "\n" + mz[12] + "\n" in r2, "Z. 47-51 und Karte TB-167 zeichengleich im Register"); p(r2.endswith("\n") and not r2.endswith("\n\n"), "Register endet mit genau einer Leerzeile")
    ende()
def index(s0, datum, probe):
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 63. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 63 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–62" in z[k[0]], "Kopf genau einmal, nennt 0–62"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–62", "Abschnitte 0–63")
    i = [j for j, l in enumerate(z) if l.startswith("| 62 aus 15b und 16b |")]
    if p(len(i) == 1, "Zeile 62 genau einmal"):
        z.insert(i[0] + 1, "| 63 Vollzug TB-167 | %s | 63.1 Hash-Übergang nach 37.3 (Abhilfe G6 elliott_wave_stocks, Commit `%s`; aus ERGEBNIS_TB-167 Z. 47–51) mit Freigabe-Karte und Sonde zu Punkt 11 | – |" % (T, ABH))
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-167 (")]
    if p(len(j) == 1, "Pflegezeile TB-167 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-167 (", "In TB-167 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-168 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-168 (`index`); 63 (Vollzug TB-167) kommt zu T%s." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    r = zeile16a()
    if not p(r is not None and r[6] == "–" and OFFEN16A in ("ja", "nein"), "Zeile 16a genau einmal, offen „–“; neuer Wert %s" % OFFEN16A): ende()
    json.dump({"16a": {"frage": r[2], "entscheidung": r[3], "offen": OFFEN16A}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    OUT.append("info  Handfelder 16a (Frage, Entscheidung wie im Index; offen %s) geschrieben: %s" % (OFFEN16A, ziel)); ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-167"):
        z[a[0]] = z[a[0]][:-2] + " · Register 63 (Vollzug TB-167 nach 37.3, Abhilfe G6 elliott_wave_stocks) mit TB-168 (%s, Journal %s); als Nächstes TB-166 E-3a neu auf diesem Stand |" % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); k = kennungen(); neu = naechste(max(k))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-168: " % neu), "Kopfzeile ## %s — TB-168: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "sonde": sonde(a[1], a[2], a[3])
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
```
