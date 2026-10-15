# TB-165 Register 61: Fable 15a — Registerblock R98–R99, drei Marken, 61.3 Voraussetzungen und Befunde — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 15.10.2026, 21:24** (Helfer BAU165, per Skript aus Bausteinen, `$HOME/sc/tb165/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an Kopien simuliert. Ohne Gegenleser. **Gebaut am HEAD `a9bf4a7`.**

**Sitzungstitel:** `TB-165` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `a9bf4a7c1865348b2c4f37be2fc67b92251ae920` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-165`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-165_register61_fable15a.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`; Werkzeug `docs/belege/TB-165/tb165_werkzeug.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-165/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-165_register61_fable15a.md`. **Journal:** nächste freie Kennung (am Bau-HEAD höchste FA ⇒ FB).
**Grundlage:** Fable-Antwort 15.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md`, md5 `9bc9e2f1ccf3e14804549b23662a2caf`), Registerblock Z. 46–49; R56 (b) und R99 (g) (die drei Dateien 15.10.a mit Commit im Repo, bevor eingetragen wird). **Zeitgrenze:** jeder Bash-Aufruf mit dem Parameter `timeout` des Bash-Werkzeugs, 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V (Voraussetzungen) ⇒ R (Register 61 und drei Marken) ⇒ K (Kopien, Index, Dialog-Index) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F.

## Was eingetragen wird

- **Abschnitt 61** (`WZ register`): Titel `## 61. Fable 15a — Registerblock R98–R99 (TB-165)`; Kopfabsatz „Reines Eintragen …, Bauart wie 58“ mit md5 der Quelle; **61.1 R98** und **61.2 R99** je „> R…“ und „> Quelle des Grundes“ **zeichengleich** aus dem Codeblock (das Werkzeug liest sie aus der Datei und vergleicht nach dem Schreiben Zeichen für Zeichen), je eine „**Kette:**“-Zeile; **61.3 Voraussetzungen und Befunde** (`v_voraussetzung.txt` wörtlich eingerückt; (a) R99 (g) mit dem Befund zu 56; (b) R99 (b) mit der Tabelle je Stelle von „25c (1)“; (c) R98 (b) offen bis zum Bau E-3; (d) F4 in die nächste Fable-Anfrage).
- **Marken nach R99 (d)**, je Zeilenpaar wie 58 hinter dem letzten Eintrag am alten Ort (hinter der letzten Zeile „Eintrag und Stand oben bleiben zeichengleich.“, sonst hinter der Quellenzeile); der alte Satz bleibt unberührt:
  - `> ⭐ **57.1 R90 ERGÄNZT durch R98 (61.1)** (Fable 15a R98, TB-165, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - `> ⭐ **56.3 R86 ERGÄNZT durch R98 (61.1)** (Fable 15a R98, Unterpunkt (d), TB-165, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
  - `> ⭐ **57.2 R91 PRÄZISIERT durch R99 (61.2)** (Fable 15a R99, Unterpunkt (b), TB-165, ⟨DATUM⟩).` + `> Eintrag und Stand oben bleiben zeichengleich.`
- **Ohne Marke** (R99 (d)): 48.14 (R46), 55.4 (R81), 56.4 (R87), 37.3, 37.5, 41.1, 48.13 (R45), 57.5, 57.6, Abschnitt 10, Abschnitt 9, ERZEUGT-Block von 3; „25c (1)“ an keinem Ort (R99 (b)) — dafür eine Indexzeile.
- Append-only: `git diff --numstat` des Registers zeigt in Spalte 2 eine `0`.

## Am Bau gemessen (Vorschau von 61.3, an einer Kopie)

Voraussetzung an der Kopie: Pruefungen: 20, NEIN: 0, rc 0 (`gen/vorschau_v.txt`). Text, wie ihn `WZ register` für 61.3 setzt (ohne die eingerückten Zeilen; ⟨S0⟩ setzt das Werkzeug):

(a) R99 (g): 37, 55 und 57 am Commit `35dae90` = am Stand `⟨S0⟩` = gelesene Kopie (37 am Kopf `d950e03`, 55 und 57 am Kopf `3f2e97e`; Leerzeilen am Abschnittsende nicht gezählt). **Befund:** 56 am Kopf `3f2e97e`, den der Verfahrensprüfer gelesen hat (Leseprotokoll 15a), ist ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ (drei Zeilen, gesetzt mit TB-162); sonst zeichengleich. R95 selbst hat er in 58 am Commit `35dae90` gelesen. Übergabe, Anfrage und Antwort 15.10.a liegen seit `⟨S0⟩` im Repo (R56 (b)).

(b) R99 (b): „25c (1)“ steht am Stand `⟨S0⟩` in 12 Zeilen ausserhalb 57, darunter R60 (b) (Z. 11352) und R63 (c) (Z. 11434), wie 57.5 („auch im Blocktext“); dazu 3 Zeilen in 57 (Z. 11986, 12025, 12035). Gemessen sind zwölf Zeilen einschliesslich R60 (b) und R63 (c), nicht zwölf und zwei dazu. Die Lesart „25c (1) ist 42.3 F1 (a)“ je Stelle ausserhalb 57 (Ausschnitt höchstens 200 Zeichen; Urteil aus der Liste je Zeile im Werkzeug, gemessen vom steuernden Chat am 15.10.2026; 42.3 F1 (a), Register Z. 9310–9312: „unbekannter Bedingungstext ⇒ 2“):

| Z. | Ort | Zeile | Ausschnitt | Urteil |
|---|---|---|---|---|
| 9632 | 43, 43.1 | Quelle des Grundes | … Eingabe, er rechnet auf ihr — kann er das nicht, hat er nicht gemessen), 12 (kein Auffüllen), 25c (1) (Register-Code-Widerspruch ist 2). Kein Ergebnis. Eure Beobachtung, dass die Meldungen „ni… | trifft |
| 10532 | 46, 46.5 | Quelle des Grundes | …2 (nennt `herkunft.json` als Teil des Vertrags), Abschnitt 12 (Vertragsbruch ⇒ Abbruch), 36.5, 25c (1) (Register-Code-Widerspruch ist 2), Prüfprinzip A8. Kein Ergebnis. | trifft |
| 10760 | 47, 47.8 | Quelle des Grundes | > *Quelle des Grundes:* 12, 5e/19, 42.2 E5, R10 (dieselbe Bauart), 25c (1). Kein Ergebnis. | trifft (42.3 F1 (a): unbekannter Bedingungstext ⇒ 2; R25: endet mit 2) |
| 11031 | 48, 48.16 | andere Zeile | …wertung.py in diesem Fall ausgegebene Zelle; Abweichung ist ein Register-Code-Widerspruch nach 25c (1).] M48. | trifft |
| 11073 | 48, 48.18 | R-Zeile | …0“; 4.2; 9), die gemessene Übereinstimmung; eine Abweichung ist ein Register-Code-Widerspruch (25c (1)) und wird gemeldet, nicht eingetragen. Der Registertext legt keine dieser Definitionen neu… | trifft |
| 11074 | 48, 48.18 | Quelle des Grundes | > Quelle des Grundes: 13 („Das Urteil ist Code“), 12, Sperrliste 3/5/7/9, 38.2, 25c (1), 2.1, Messung TB-121. Kein Ergebnis. | trifft |
| 11352 | 51, 51.5 | R-Zeile | …gen die Selektionsfalten des Gewinners; eine Abweichung ist ein Register-Code-Widerspruch nach 25c (1) und wird gemeldet.] (c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mitt… | trifft |
| 11434 | 52, 52.1 | R-Zeile | …d kein Mittel daraus rechnet.] Trifft sie nicht zu, ist das ein Register-Code-Widerspruch nach 25c (1) zur Bewertung in R48 (d) und R60 (b) und wird gemeldet, nicht eingetragen. (d) Der Zellen-… | trifft |
| 11435 | 52, 52.1 | Quelle des Grundes | …ch R49 (e)), R45 (kein zweiter Rechenweg), 24.4 (bewertet zum Marktpreis, nicht zum Einstand), 25c (1). Kein Ergebnis. | trifft |
| 11555 | 53, 53.4 | R-Zeile | …k_tagesreihen/<markt>.csv liest und R39 <bot>.csv verlangt, ist ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50). Er wird zugunsten von R39 aufgelöst; R39 ist damit b… | trifft |
| 11891 | 56, 56.4 | R-Zeile | …achennotiz, und die Wache bleibt. Kann er es bei einem, ist das ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50) und kommt vor dem Bau mit der Fundstelle als Frage an… | trifft |
| 11966 | 56, 56.8 | andere Zeile | \| 14 \| R87 (d) verweist auf „25c (1), nach der Wiedergabe in R48 und R50“; 42.3 („Aus Fable 25c“) führt keinen Eintrag „(1)“, d… | trifft |

Stellen mit „Frage an Fable“: keine.

(c) R98 (b): offen. Ob `entry_cutoff` in den sechs Backtests die drei Bedingungen erfüllt und welche Stelle es bei elliott_wave, elliott_wave_stocks und t3_supertrend ist, misst der Bau E-3 durch Lesen (27.2, nur das Wie); nicht Teil von TB-165.

(d) F4 (Punkte 10 bis 12 der Anfrage 10.10.a): kommt mit Wortlaut in die nächste Fable-Anfrage (R99 (f)); nicht Teil von TB-165.

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen. Kein neues Abbild. Nichts unter `strategies/`, `shared/`, `data/`, `config/`, `research/` ändern oder committen. **Schreiben darf die Sitzung nur:** `docs/VORREGISTRIERUNG_neuselektion.md` (R, nur `WZ register`), `docs/projektfuehrung/REGISTER_INDEX.md`, `REGISTER_KOPIE_teil*.md`, `register_kopie/`, `FABLE_DIALOG_INDEX.md` (K, nur mit den genannten Werkzeugen), `docs/projektfuehrung/BACKLOG.md` (`WZ backlog`), `docs/projektfuehrung/JOURNAL.md` (`WZ journal`), `docs/belege/TB-165/`, das Ergebnis.

## Lage nach dem Auslegen

Am Bau-HEAD `a9bf4a7`: geändert `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, `docs/projektfuehrung/UEBERGABE.md`; unverfolgt `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md`, `docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-15a_eroeffnung.md`. Das Auslegen ändert dazu `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab. **Beim Start genau 7 Einträge** (Soll in 0a). Mitgenommen werden nur diese; die drei Fable-Dateien 15.10.a werden vorher per md5 geprüft (wie `9a1bc7a` in TB-162).

## Schritt 0 — Ausgang

**0a. Zuerst:** `git status --porcelain > "$TMPDIR/tb165_0a.txt"`, `git rev-parse HEAD` und `git rev-parse --abbrev-ref HEAD`. Soll: Zweig `main`, HEAD `a9bf4a7c1865348b2c4f37be2fc67b92251ae920` und genau diese 7 Einträge; sonst **ABBRUCH** (vor ⟨S0⟩ und vor jedem Push). Kein späterer Schritt wechselt den Zweig.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-165_register61_fable15a.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-15a_eroeffnung.md
```

Werkzeug aus Anhang B holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-165_register61_fable15a.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2] + "/tb165_werkzeug.py", "w", encoding="utf-8").write(t)
print("tb165_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll genau: `tb165_werkzeug.py 200abc0c09620658c98061f9b12cc86bc7316fe83d6b8f1035a153279b5c1834`; sonst **ABBRUCH**. Dann die drei Fable-Dateien prüfen (genau dieser Befehl):

```
trading-env/bin/python3 -B "$TMPDIR/tb165_werkzeug.py" md5 > "$TMPDIR/tb165_md5.txt" 2>&1; echo "rc $?" >> "$TMPDIR/tb165_md5.txt"
```

Soll: letzte Zeilen `Pruefungen: 3, NEIN: 0` und `rc 0`; sonst **ABBRUCH**. Commit `TB-165 Schritt 0: Stand des steuernden Chats und Fable 15.10.a` mit genau diesen Pfaden, pushen ⇒ **⟨S0⟩** (7 Zeichen). Erst danach: `mkdir -p docs/belege/TB-165`, `cp "$TMPDIR/tb165_0a.txt" docs/belege/TB-165/0a_status.txt`, `cp "$TMPDIR/tb165_md5.txt" docs/belege/TB-165/0a_md5.txt`, `cp "$TMPDIR/tb165_werkzeug.py" docs/belege/TB-165/tb165_werkzeug.py` (je `diff` ohne Ausgabe).

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-165_register61_fable15a.md
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-15a_eroeffnung.md
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py voraussetzung > docs/belege/TB-165/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0`, davor `Pruefungen: 20, NEIN: 0` (drei Fable-Dateien verfolgt und gleich HEAD; Registerblock; 60 da, 61 nicht; drei Marken-Orte; R99 (g) je Abschnitt mit dem Befund zu 56; R99 (b) zwölf Zeilen mit R60 (b) und R63 (c); 42.3 F1 (a); Anker in Index, Dialog-Index, BACKLOG, Journal). Sonst **ABBRUCH**.

## Schritt R — Register 61 und Marken

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-165/v_voraussetzung.txt --probe > docs/belege/TB-165/r_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/r_probe.txt
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ docs/belege/TB-165/v_voraussetzung.txt > docs/belege/TB-165/r_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/r_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. Danach: drei Marken, Abschnitt 61 am Registerende, R98/R99 zeichengleich, append-only bis auf die drei Marken (`r_eintrag.txt`). Commit `TB-165 R: Register 61 (Fable 15a, R98–R99), drei Marken`, pushen ⇒ **⟨R⟩**.

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-165/0a_status.txt
git add docs/belege/TB-165/0a_md5.txt
git add docs/belege/TB-165/tb165_werkzeug.py
git add docs/belege/TB-165/v_voraussetzung.txt
git add docs/belege/TB-165/r_probe.txt
git add docs/belege/TB-165/r_eintrag.txt
git add docs/belege/TB-165/r_daten.json
```

## Schritt K — Kopien, Index, Dialog-Index (wie TB-162 Schritt K)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-165/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-165/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-165/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨R⟩ > docs/belege/TB-165/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-165/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_index.txt
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py handfelder docs/belege/TB-165/k_handfelder.json > docs/belege/TB-165/k_handfelder.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_handfelder.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-165/k_handfelder.json > docs/belege/TB-165/k_dialog_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_dialog_index.txt
trading-env/bin/python3 -B docs/werkzeuge/dialog_index.py --pruefen > docs/belege/TB-165/k_dialog_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/k_dialog_pruefen.txt
```

Soll: jede Belegdatei endet mit `rc 0`. `registerkopie.py` schreibt Teildateien und Abschnittskopien neu (61 neu, alle Köpfe 0–61); `c2_index_zeilen.py` (aus TB-154, unverändert) schreibt die Zeilenangaben von ⟨S0⟩ auf ⟨R⟩ um; `WZ index` setzt Kopf (0–61), Zeilen 56, 57 und 61, Abschnitt 14 (3 Marken, zwei Indexzeilen) und die Pflegezeile; `dialog_index.py --handfelder` setzt die Zeile 15a. Entsteht eine weitere Teildatei: mit Namen anpassen, melden. rc ≠ 0 eines Schritts: festhalten, die Dateien dieses Schritts nicht committen, melden (kein Abbruch). Commit `TB-165 K: Registerkopie, Index, Dialog-Index`, pushen ⇒ **⟨K⟩**.

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
git add docs/belege/TB-165/k_registerkopie.txt
git add docs/belege/TB-165/k_abschnitte.txt
git add docs/belege/TB-165/k_pruefen.txt
git add docs/belege/TB-165/k_index_zeilen.txt
git add docs/belege/TB-165/k_index.txt
git add docs/belege/TB-165/k_handfelder.txt
git add docs/belege/TB-165/k_dialog_index.txt
git add docs/belege/TB-165/k_dialog_pruefen.txt
git add docs/belege/TB-165/k_handfelder.json
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py kennung > docs/belege/TB-165/a_kennung.txt; echo "rc $?" >> docs/belege/TB-165/a_kennung.txt` (Soll „Kennung FB …“, `rc 0`). Dann:

```
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-165/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-165/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/a_backlog.txt
```

Block nach `BEL/a_block.md` (Schreibwerkzeug; erste Zeile `## <Kennung> — TB-165: …`, Quellenzeile, `**Quelle:**`, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; keine weitere `## `-Zeile, kein `---`), dann:

```
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py journal docs/belege/TB-165/a_block.md --probe > docs/belege/TB-165/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-165/tb165_werkzeug.py journal docs/belege/TB-165/a_block.md > docs/belege/TB-165/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-165/a_journal.txt
```

Soll je `rc 0`; endet eine Probe nicht mit `rc 0`: zweiten nicht ausführen, **ABBRUCH**. **Ergebnis** `docs/ERGEBNIS_TB-165_register61_fable15a.md` (Schreibwerkzeug): Kopf mit Commits · „Kurz“ · Schritt 0 (`0a_md5.txt` wörtlich) · Voraussetzungen (`v_voraussetzung.txt` wörtlich) · Register 61 (Zeile, drei Marken mit Zeile aus `r_daten.json`, numstat) · **61.3 (a) und (b)** aus dem Register übernommen, mit der Liste der Stellen „Frage an Fable“ · K (je rc) · BACKLOG (Rang 1: als Nächstes TB-30b E-3 mit der Messung nach R98 (b)) · **Offen:** R98 (b) mit dem Bau E-3; F4 (Punkte 10–12 der Anfrage 10.10.a) und jede Stelle „Frage an Fable“ aus 61.3 (b) in die nächste Fable-Anfrage; der Befund zu 56 (R99 (g)) zur Kenntnis an den Verfahrensprüfer · Abweichungen · **In einfacher Sprache** (drei bis fünf Sätze, ohne Kürzel). Dann:

```
git add docs/ERGEBNIS_TB-165_register61_fable15a.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-165/a_kennung.txt
git add docs/belege/TB-165/a_backlog_probe.txt
git add docs/belege/TB-165/a_backlog.txt
git add docs/belege/TB-165/a_block.md
git add docs/belege/TB-165/a_journal_probe.txt
git add docs/belege/TB-165/a_journal.txt
```

Commit `TB-165 Abgabe: Ergebnis, BACKLOG, Journal FB`, pushen ⇒ **⟨F⟩**. Zuletzt `git status --porcelain > "$TMPDIR/tb165_f.txt"`, `cp "$TMPDIR/tb165_f.txt" docs/belege/TB-165/f_porcelain.txt`, `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-165/f_numstat.txt` (Soll: Register Spalte 2 = `0`; kein Pfad unter `strategies/`, `shared/`, `data/`, `config/`, `research/`), dann:

```
git add docs/belege/TB-165/f_porcelain.txt
git add docs/belege/TB-165/f_numstat.txt
```

Commit `TB-165 F: porcelain und numstat`, pushen.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab (Zweig, HEAD, Einträge); Holbefehl-Soll weicht ab; md5 einer Fable-Datei 15.10.a weicht ab; V nicht `rc 0`; `WZ register --probe`/`register` nicht `rc 0`; `WZ backlog`/`journal` nicht `rc 0`; `git push` scheitert zweimal (nicht für den Abbruch-Commit); Claude Code verlangt eine Bestätigung (melden, nicht umgehen). **Kein Abbruch:** ein Schritt in K mit rc ≠ 0.
**Abbruchweg:** vor ⟨S0⟩ nichts schreiben, nur melden. Danach genau eine neue Datei `printf '%s\n' "<Schritt>: <Grund>" > docs/belege/TB-165/abbruch.txt`, `git add` dieser Datei und jeder schon entstandenen, nicht committeten Belegdatei unter `docs/belege/TB-165/` mit Namen (nie `git add -A`, nie `-f`; keine Datei ausserhalb `docs/belege/TB-165/`), Commit `TB-165 Abbruch: <Schritt>`, pushen (scheitert der Push: melden, nicht wiederholen), melden. Bei einem Abbruch nach `WZ register` (vor ⟨R⟩) bleibt das Register im Arbeitsbaum geändert — das steht in der Meldung; nicht zurücksetzen.

## In einfacher Sprache

Die Sitzung legt die neue Antwort des Verfahrensprüfers mit Anfrage und Übergabe ins Repo und trägt deren zwei Regeltexte wortgleich ins Register ein, nur angehängt. Die erste Regel sagt, dass die Sperre gegen zu frühe Käufe bei jedem Bot dort sitzt, wo er seine Käufe bildet, dass ein Parameter dafür genügen kann, eine Freigabe je Bauauftrag reicht und die Prüfung am Erzeuger läuft. Die zweite hält Tatsachen fest, zum Beispiel wie ein alter Verweis zu lesen ist. An drei alten Stellen kommt ein Hinweis dazu, dass sie ergänzt sind. Es läuft nichts auf Kursdaten, kein Code wird geändert.

## Anhang — Dateien und ihre Befehle

| Datei | Befehl |
|---|---|
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/UEBERGABE.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/auftraege/MAC_TB-165_register61_fable15a.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-15a_eroeffnung.md` | Auslegen durch den steuernden Chat; Commit ⟨S0⟩ (Schritt 0) |
| `docs/VORREGISTRIERUNG_neuselektion.md` | Schritt R (Commit ⟨R⟩) |
| `docs/belege/TB-165/0a_status.txt` | Schritt 0 (Commit ⟨R⟩) |
| `docs/belege/TB-165/0a_md5.txt` | Schritt 0 (Commit ⟨R⟩) |
| `docs/belege/TB-165/tb165_werkzeug.py` | Schritt 0 (Commit ⟨R⟩) |
| `docs/belege/TB-165/v_voraussetzung.txt` | Schritt V (Commit ⟨R⟩) |
| `docs/belege/TB-165/r_probe.txt` | Schritt R (Commit ⟨R⟩) |
| `docs/belege/TB-165/r_eintrag.txt` | Schritt R (Commit ⟨R⟩) |
| `docs/belege/TB-165/r_daten.json` | Schritt R (Commit ⟨R⟩) |
| `docs/projektfuehrung/REGISTER_INDEX.md` | Schritt K |
| `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil1.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil2.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil3.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil4.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil5.md` | Schritt K |
| `docs/projektfuehrung/REGISTER_KOPIE_teil6.md` | Schritt K |
| `docs/projektfuehrung/register_kopie` | Schritt K |
| `docs/belege/TB-165/k_registerkopie.txt` | Schritt K |
| `docs/belege/TB-165/k_abschnitte.txt` | Schritt K |
| `docs/belege/TB-165/k_pruefen.txt` | Schritt K |
| `docs/belege/TB-165/k_index_zeilen.txt` | Schritt K |
| `docs/belege/TB-165/k_index.txt` | Schritt K |
| `docs/belege/TB-165/k_handfelder.txt` | Schritt K |
| `docs/belege/TB-165/k_dialog_index.txt` | Schritt K |
| `docs/belege/TB-165/k_dialog_pruefen.txt` | Schritt K |
| `docs/belege/TB-165/k_handfelder.json` | Schritt K |
| `docs/ERGEBNIS_TB-165_register61_fable15a.md` | Schritt A |
| `docs/projektfuehrung/BACKLOG.md` | Schritt A |
| `docs/projektfuehrung/JOURNAL.md` | Schritt A |
| `docs/belege/TB-165/a_kennung.txt` | Schritt A |
| `docs/belege/TB-165/a_backlog_probe.txt` | Schritt A |
| `docs/belege/TB-165/a_backlog.txt` | Schritt A |
| `docs/belege/TB-165/a_block.md` | Schritt A |
| `docs/belege/TB-165/a_journal_probe.txt` | Schritt A |
| `docs/belege/TB-165/a_journal.txt` | Schritt A |
| `docs/belege/TB-165/f_porcelain.txt`, `docs/belege/TB-165/f_numstat.txt` | Abgabe |
| `docs/belege/TB-165/abbruch.txt` | nur Abbruchweg |
| `$TMPDIR/tb165_*` | 0a, Holbefehl, md5, Abgabe; bleiben liegen |

## Anhang B — Werkzeug

### Werkzeug

```python
#!/usr/bin/env python3
"""TB-165 Werkzeug (Anhang B): Fable 15a ins Register (Abschnitt 61, R98-R99, drei Marken nach R99 (d), 61.3 Voraussetzungen und Befunde), Index, Handfelder, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  md5                                      0a: md5 der drei Fable-Dateien 15.10.a (rc 0 = alle wie Soll)
  voraussetzung                            Voraussetzungen aus R98/R99 und Anker messen (rc 0 = alle ja)
  register <DATUM> <S0> <BELEG> [--probe]  Abschnitt 61 (R98, R99 zeichengleich), 61.3, drei Marken
  index <S0> <DATUM> [--probe]             REGISTER_INDEX.md: Kopf 0-61, Zeilen 56/57, Zeile 61, Abschnitt 14, Pflege (nach c2_index_zeilen.py)
  handfelder <ZIEL>                        Handfelder 15a fuer dialog_index.py
  backlog <DATUM> <KENNUNG> [--probe]      BACKLOG Rang 1: Stand TB-165
  kennung | journal <BLOCK> [--probe]      naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, os, re, subprocess, sys
REG, IDX, JO, BL, DI = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md", "docs/projektfuehrung/FABLE_DIALOG_INDEX.md"
P = "docs/projektfuehrung/"
FA = P + "FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md"
DREI = {FA: "9bc9e2f1ccf3e14804549b23662a2caf", P + "FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md": "26108d4fe8474e8035d500a78371ed21",
        P + "FABLE_UEBERGABE_2026-10-15a_eroeffnung.md": "4821ff1958955d333585c839b007dbe7"}
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R98)"
TITEL61 = "## 61. Fable 15a — Registerblock R98–R99 (TB-165)"
ZEICHENGLEICH = "> Eintrag und Stand oben bleiben zeichengleich."
# Urteil je Zeile ausserhalb 57 (R99 (b)), gemessen vom steuernden Chat, 15.10.2026: Lesart „25c (1) ist 42.3 F1 (a)“ trifft an allen zwölf Stellen
URTEIL = {n: "trifft" for n in (9632, 10532, 11031, 11073, 11074, 11352, 11434, 11435, 11555, 11891, 11966)}
URTEIL[10760] = "trifft (42.3 F1 (a): unbekannter Bedingungstext ⇒ 2; R25: endet mit 2)"
# (Ort, Anfang des Unterabschnitts, Wort, R, Unterabschnitt neu, Unterpunkt) - R99 (d)
MARKEN = [("57.1 R90", "### 57.1 ", "ERGÄNZT", "R98", "61.1", ""), ("56.3 R86", "### 56.3 ", "ERGÄNZT", "R98", "61.1", "Unterpunkt (d)"),
          ("57.2 R91", "### 57.2 ", "PRÄZISIERT", "R99", "61.2", "Unterpunkt (b)")]
GELESEN = {37: "d950e03", 55: "3f2e97e", 56: "3f2e97e", 57: "3f2e97e"}
M56 = "> ⭐ **56.1 R84 PRÄZISIERT durch R95 (58.2)**"
KETTE = ["**Kette:** Marken nach R99 (d): 57.1 (R90); 56.3 (R86), Unterpunkt (d). Ohne Marke (R99 (d)): 48.14 (R46), 55.4 (R81), 56.4 (R87), 37.3, 37.5, 41.1, 48.13 (R45). Offen: die Voraussetzung in (b), Messung mit dem Bau E-3 (61.3 (c)).",
         "**Kette:** Marke nach R99 (d): 57.2 (R91), Unterpunkt (b). Indexzeile statt Marke (R99 (b)): „25c (1)“ ist 42.3 F1 (a). Nach (f) erledigt: 57.6 Nr. 4 für F1 und F2, Nr. 5, Nr. 6; F4 kommt in die nächste Anfrage (61.3 (d)). Voraussetzungen und Befunde: 61.3."]
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", " · Register 60 (Vollzug TB-163 nach 37.3; Posten 5 nach R43 neu gefasst) mit TB-164 (15.10.2026, Journal FA) |"
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def gitrc(*a): r = subprocess.run(["git"] + list(a), capture_output=True, text=True); return r.returncode, r.stdout
def git(*a): return gitrc(*a)[1]
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def abschnitt(txt, n):
    z = txt.split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## %d. " % n)]
    if len(a) != 1: return None
    e = next((i for i in range(a[0] + 1, len(z)) if re.match(r"## \d+\. ", z[i])), len(z)); b = z[a[0]:e]
    while b and b[-1] == "": b.pop()
    return b
def block():
    """[(Zeile R, Zeile Quelle, Zeilennummer R in der Fable-Datei)] fuer R98 und R99."""
    z = lies(FA).split("\n"); a = z.index(KOPF_A) + 1
    while z[a] == "": a += 1
    if z[a] != "```": return None
    e = z.index("```", a + 1); b = [(i + 1, l) for i, l in enumerate(z[a + 1:e], a + 1) if l]
    if [l[:6] for _, l in b] != ["R98 — ", "Quelle", "R99 — ", "Quelle"]: return None
    return [(b[0][1], b[1][1], b[0][0]), (b[2][1], b[3][1], b[2][0])]
def stellen25c(z):
    """Jede Registerzeile mit „25c (1)“: (Z., Abschnitt, Unterabschnitt, Art, Ausschnitt <= 200 Zeichen, Urteil)."""
    aus, ab, ua = [], None, ""
    for i, l in enumerate(z):
        m = re.match(r"^## (\d+)\. ", l)
        if m: ab, ua = int(m.group(1)), ""
        if l.startswith("### "): ua = l[4:].split(" ")[0]
        if "25c (1)" not in l: continue
        k = l.index("25c (1)"); a, e = max(0, k - 95), min(len(l), k + 98)
        aus_ = ("…" if a else "") + l[a:e] + ("…" if e < len(l) else "")
        art = "R-Zeile" if re.match(r"^> (\*\*)?R\d+ — ", l) else ("Quelle des Grundes" if re.match(r"^> \*?Quelle de", l) else "andere Zeile")
        u = URTEIL.get(i + 1, "Frage an Fable (nicht in der Liste)") if ab != 57 else "–"
        aus.append((i + 1, ab, ua, art, aus_, u))
    return aus
def befund_b(z):
    s = stellen25c(z); auss = [x for x in s if x[1] != 57]; in57 = [x for x in s if x[1] == 57]
    def in_up(nr, von, bis):
        t = [i for i, l in enumerate(z) if l.startswith("> %s — " % nr)]
        if len(t) != 1: return None
        l = z[t[0]]; k = l.find("25c (1)"); u = [(m.start(), m.group(1)) for m in re.finditer(r"[.\]] \(([a-h])\) ", l)]
        vor = [x for x in u if x[0] < k]; nach = [x for x in u if x[0] > k]
        return t[0] + 1 if vor and vor[-1][1] == von[1] and (not nach or nach[0][1] == bis[1]) else None
    return s, auss, in57, in_up("R60", "(b)", "(c)"), in_up("R63", "(c)", "(d)")
def sec56(alt, neu):
    if alt is None or neu is None or len(neu) != len(alt) + 3: return False
    i = next((k for k in range(len(alt)) if alt[k] != neu[k]), len(alt))
    return neu[:i] + neu[i + 3:] == alt and sorted(x[:len(M56)] for x in neu[i:i + 3]) == sorted(["", M56, ZEICHENGLEICH[:len(M56)]])
def r99g():
    """[(Abschnitt, gleich 35dae90/HEAD, gleich gelesene Kopie, Befund-56)]"""
    h, c = lies(REG), git("show", "35dae90:" + REG); aus = []
    for n, g in sorted(GELESEN.items()):
        x, y, w = abschnitt(c, n), abschnitt(h, n), abschnitt(git("show", "%s:%s" % (g, REG)), n)
        aus.append((n, g, x is not None and x == y, x == w, n == 56 and sec56(w, y)))
    return aus
def ort(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None, None
    e = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### "))
    zg = [i for i in range(a[0], e) if z[i] == ZEICHENGLEICH]; q = [i for i in range(a[0], e) if z[i].startswith("> Quelle des Grundes")]
    return a[0], e, (zg[-1] if zg else (q[0] if len(q) == 1 else None))
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def md5cmd():
    for f, m in DREI.items(): p(os.path.exists(f) and md5(lies(f)) == m, "md5 %s = %s" % (f, m))
    ende()
def voraussetzung():
    for f, m in DREI.items():
        p(bool(git("ls-files", "--error-unmatch", f).strip()) and git("diff", "--name-only", "HEAD", "--", f).strip() == "" and md5(lies(f)) == m, "R99 (g)/R56 (b): %s verfolgt, gleich HEAD, md5 %s" % (f, m))
    b = block(); p(b is not None, "Registerblock 15a: genau R98, Quelle, R99, Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[0][2], b[1][2] + 1) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 60. ") for l in z) == 1 and not re.search(r"^## 61\. ", reg, re.M) and not re.search(r"\bR9[89]\b", reg), "Register: 60 da, 61 nicht; R98/R99 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for o, anf, w, rr, ua, up in MARKEN:
        a, e, at = ort(z, anf); p(a is not None and at is not None and not any(rr in z[i] for i in range(a, e)), "Ort %s: genau einmal, Einfuegestelle Z. %s, %s dort noch nicht genannt" % (o, at + 1 if at is not None else "?", rr))
    for n, g, x, y, b56 in r99g():
        if n == 56: p(x and not y and b56, "R99 (g) Befund: 56 am 35dae90 = HEAD; gelesene Kopie (%s) ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ (+3 Zeilen, TB-162), sonst zeichengleich" % g)
        else: p(x and y, "R99 (g): Abschnitt %d am 35dae90 = HEAD = gelesene Kopie (%s), Endleerzeilen nicht gezaehlt" % (n, g))
    s, auss, in57, r60, r63 = befund_b(z)
    p(sorted(x[0] for x in auss) == sorted(URTEIL), "R99 (b): Zeilen mit „25c (1)“ ausserhalb 57 = die %d Zeilen der Urteilsliste" % len(URTEIL))
    p(len(auss) == 12 and r60 in [x[0] for x in auss] and r63 in [x[0] for x in auss], "R99 (b): „25c (1)“ in %d Zeilen ausserhalb 57 (darunter R60 (b) Z. %s, R63 (c) Z. %s), %d in 57" % (len(auss), r60, r63, len(in57)))
    p(any(l.startswith("### 42.3 Aus Fable 25c") for l in z) and any(l.startswith("**F1 (a) — ") for l in z), "42.3 und F1 (a) genau da")
    ix = lies(IDX).split("\n")
    p(sum("Abschnitte 0–60" in l and l.startswith("**Stand:** Register ") for l in ix) == 1 and sum(l.startswith("| 60 Vollzug TB-163 |") for l in ix) == 1 and sum(l.startswith("| 56 aus 09a |") for l in ix) == 1
      and sum(l.startswith("| 57 aus 10a |") and l.endswith("| – |") for l in ix) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-164 (") for l in ix) == 1 and sum(l.startswith("**Pflege:**") for l in ix) == 1
      and not any(l.startswith("## 14. ") for l in ix), "Index: Kopf 0–60, Zeilen 56, 57 (– ), 60, Pflegezeile TB-164, Pflege-Anker je genau einmal; kein Abschnitt 14")
    p(not any(l.startswith("| 15a |") for l in lies(DI).split("\n")), "Dialog-Index: 15a noch nicht")
    bl = lies(BL).split("\n"); p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl) == 1, "BACKLOG: Rang 1 (Stand TB-164) genau einmal")
    k = kennungen(); p(max(k) == "FA" and naechste(max(k)) not in k, "Journal: höchste Kennung %s, nächste %s frei" % (max(k), naechste(max(k))))
    ende()
def text613(z, vb, s0):
    s, auss, in57, r60, r63 = befund_b(z); g = r99g()
    t = ["### 61.3 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `docs/belege/TB-165/v_voraussetzung.txt` (Werkzeug `voraussetzung`, Anhang B des Auftrags TB-165), Zeilen wörtlich:", ""]
    t += ["    " + l for l in vb] + [""]
    ok = [str(n) for n, _, x, y, _ in g if n != 56 and x and y]
    t.append("(a) R99 (g): %s am Commit `35dae90` = am Stand `%s` = gelesene Kopie (37 am Kopf `d950e03`, 55 und 57 am Kopf `3f2e97e`; Leerzeilen am Abschnittsende nicht gezählt). "
             "**Befund:** 56 am Kopf `3f2e97e`, den der Verfahrensprüfer gelesen hat (Leseprotokoll 15a), ist ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ (drei Zeilen, gesetzt mit TB-162); sonst zeichengleich. R95 selbst hat er in 58 am Commit `35dae90` gelesen. "
             "Übergabe, Anfrage und Antwort 15.10.a liegen seit `%s` im Repo (R56 (b))." % (", ".join(ok[:-1]) + " und " + ok[-1], s0, s0))
    t += ["", "(b) R99 (b): „25c (1)“ steht am Stand `%s` in %d Zeilen ausserhalb 57, darunter R60 (b) (Z. %s) und R63 (c) (Z. %s), wie 57.5 („auch im Blocktext“); dazu %d Zeilen in 57 (Z. %s). "
          "Gemessen sind zwölf Zeilen einschliesslich R60 (b) und R63 (c), nicht zwölf und zwei dazu. Die Lesart „25c (1) ist 42.3 F1 (a)“ je Stelle ausserhalb 57 (Ausschnitt höchstens 200 Zeichen; Urteil aus der Liste je Zeile im Werkzeug, gemessen vom steuernden Chat am 15.10.2026; 42.3 F1 (a), Register Z. 9310–9312: „unbekannter Bedingungstext ⇒ 2“):"
          % (s0, len(auss), r60, r63, len(in57), ", ".join(str(x[0]) for x in in57)), "", "| Z. | Ort | Zeile | Ausschnitt | Urteil |", "|---|---|---|---|---|"]
    t += ["| %d | %d, %s | %s | %s | %s |" % (n, a, u, art, x.replace("|", "\\|"), ur) for n, a, u, art, x, ur in auss]
    fr = [str(x[0]) for x in auss if x[5].startswith("Frage an Fable")]
    t += ["", "Stellen mit „Frage an Fable“: %s." % (("Z. " + ", ".join(fr) + "; sie kommen mit Wortlaut als Frage an den Verfahrensprüfer (R99 (b))") if fr else "keine")]
    t += ["", "(c) R98 (b): offen. Ob `entry_cutoff` in den sechs Backtests die drei Bedingungen erfüllt und welche Stelle es bei elliott_wave, elliott_wave_stocks und t3_supertrend ist, misst der Bau E-3 durch Lesen (27.2, nur das Wie); nicht Teil von TB-165.",
          "", "(d) F4 (Punkte 10 bis 12 der Anfrage 10.10.a): kommt mit Wortlaut in die nächste Fable-Anfrage (R99 (f)); nicht Teil von TB-165.", ""]
    return t
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    z = lies(REG).split("\n"); bl = block(); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1] == "Pruefungen: %d, NEIN: 0" % sum(1 for l in vb if l.startswith(("ja ", "NEIN"))), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    p(bl is not None and md5(lies(FA)) == DREI[FA], "Quelle md5 %s, Registerblock R98/R99" % DREI[FA])
    p(not any(l.startswith("## 61. ") for l in z) and z[-1] == "" and z[-2] != "", "61 noch nicht im Register; endet mit einer Leerzeile")
    einf = []
    for o, anf, w, rr, ua, up in MARKEN:
        a, e, at = ort(z, anf)
        if p(a is not None and at is not None and not any(rr in z[i] for i in range(a, e)), "Ort %s: Einfuegestelle Z. %s" % (o, at + 1 if at is not None else "?")):
            einf.append((at + 1, ["", "> ⭐ **%s %s durch %s (%s)** (Fable 15a %s, %sTB-165, %s)." % (o, w, rr, ua, rr, up + ", " if up else "", datum), ZEICHENGLEICH]))
    if nein(): ende()
    titel = []
    for zeile, _, _ in bl:
        t = zeile.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
        if len(t) > 140: t = t[:139].rsplit(" ", 1)[0] + "…"
        titel.append(t)
    kopf = ("Reines Eintragen von Registertext, Bauart wie 58. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R98)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden Leseprotokoll, Teile, „Kurz“ und „Unsicher“ der Antwort. Zum Dialog gehören die Anfrage 15.10.a und die Übergabe 15.10.a (beide seit `%s`). Eingetragen am %s mit TB-165.") % (
            FA, DREI[FA], format(len(lies(FA).encode("utf-8")), ",").replace(",", " "), bl[0][2], bl[1][2] + 1, s0, s0, datum)
    neu = ["", TITEL61, "", kopf, ""]
    for k, ((zeile, quelle, _), t) in enumerate(zip(bl, titel)):
        neu += ["### 61.%d %s" % (k + 1, t), "", "> " + zeile, "> " + quelle, "", KETTE[k], ""]
    neu += text613(z, vb, s0)
    if probe: ende()
    for at in sorted(set(x[0] for x in einf), reverse=True): z[at:at] = [l for a2, zz in einf if a2 == at for l in zz]
    alt = lies(REG); z = z[:-1] + neu; schreibe(REG, "\n".join(z))
    r2 = lies(REG).split("\n"); mz = [(i + 1, l) for i, l in enumerate(r2) if l.startswith("> ⭐ **") and "(Fable 15a R9" in l and "TB-165" in l]
    soll = ["> ⭐ **%s %s durch %s (%s)**" % (m[0], m[2], m[3], m[4]) for m in MARKEN]; zu = {s: [n for n, l in mz if l.startswith(s)] for s in soll}
    json.dump({"marken": [[m[0], m[2], m[3], m[4], (zu[s] or [0])[0]] for m, s in zip(MARKEN, soll)], "abschnitt_61": r2.index(TITEL61) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(len(mz) == 3 and all(len(v) == 1 for v in zu.values()), "nachher: 3 Marken Z. %s; Abschnitt 61 Z. %d" % ([n for n, _ in mz], r2.index(TITEL61) + 1))
    p(all(r2.count("> " + b[0]) == 1 and r2.count("> " + b[1]) == 1 for b in bl), "R98, R99 mit Quellenzeile je genau einmal zeichengleich im Register (Zeichenvergleich mit dem Codeblock)")
    al = alt.split("\n"); r3 = [l for i, l in enumerate(r2) if i + 1 not in [x for n0, _ in mz for x in (n0 - 1, n0, n0 + 1)]]
    p(r3[:len(al) - 1] == al[:-1] and r3[len(al) - 1:] == neu, "ohne die drei Marken (je Leerzeile, Marke, Zeichengleich-Zeile): altes Register vorn unverändert, dahinter genau Abschnitt 61 (append-only)")
    ende()
def index(s0, datum, probe):
    d = json.load(open("docs/belege/TB-165/r_daten.json", encoding="utf-8")); mk = d["marken"]; mz = [m[4] for m in mk]
    p(len(mk) == 3 and all(mz), "r_daten.json: 3 Marken mit Zeile")
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 61. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 61 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–60" in z[k[0]], "Kopf genau einmal, nennt 0–60"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–60", "Abschnitte 0–61")
    i = [j for j, l in enumerate(z) if l.startswith("| 56 aus 09a |")]
    if p(len(i) == 1 and z[i[0]].endswith(" |"), "Zeile 56 genau einmal"): z[i[0]] = z[i[0]][:-2] + "; 56.3 R86 ERGÄNZT durch R98 (61.1) (Z. %d) |" % mz[1]
    i = [j for j, l in enumerate(z) if l.startswith("| 57 aus 10a |")]
    if p(len(i) == 1 and z[i[0]].endswith("| – |"), "Zeile 57 genau einmal, ohne Marke"): z[i[0]] = z[i[0]][:-4] + " 57.1 R90 ERGÄNZT durch R98 (61.1) (Z. %d); 57.2 R91 **PRÄZISIERT durch R99 (61.2)** (Z. %d) |" % (mz[0], mz[2])
    i = [j for j, l in enumerate(z) if l.startswith("| 60 Vollzug TB-163 |")]
    if p(len(i) == 1, "Zeile 60 genau einmal"): z.insert(i[0] + 1, "| 61 aus 15a | %s | R98–R99 (61.1–61.2); 61.3 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 14. Die Marken aus Fable 15a (TB-165)", "", "Alle 3 Marken, die TB-165 nach R99 (d) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-165/r_daten.json`.", "",
           "| Ort | Marke | Wort | durch | T |", "|---|---|---|---|---|"]
    tab += ["| %s | Z. %d | %s | %s (%s) | %s |" % (o, zz, w, rr, ua, T) for o, w, rr, ua, zz in sorted(mk, key=lambda m: m[4])]
    tab += ["", "### Indexzeilen aus Fable 15a", "",
            "- **„25c (1)“, an jeder Stelle des Registers:** „25c (1)“ ist 42.3 F1 (a), nach R91 (f) → R99 (b) (61.2). Ohne Marke (R99 (b), (d)). Messung je Stelle: 61.3 (b). Der Index ist kein Registertext.",
            "- **Abschnitt 10, Sperrlistenpunkte 9 und 11 (R90 (f)); Punkte 6, 10 und 11 (R81 (b)):** bestätigt durch R99 (c) (61.2), unverändert. Der Index ist kein Registertext.", ""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "", "Pflege-Anker genau einmal, davor Leerzeile"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-164 (")]
    if p(len(j) == 1, "Pflegezeile TB-164 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-164 (", "In TB-164 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-165 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-165 (`index`); 61 (R98–R99) kommt zu T%s; neuer Abschnitt 14 (3 Marken)." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"15a": {"frage": "Wo sitzt die Schranke nach R90 (c) bei den neun Bots — reicht ein Parameter wie entry_cutoff, genügt eine Freigabe je Bauauftrag, wo läuft die Prüfung nach R90 (g) — und tragen der Verweis in R90 (c) und die Lesarten aus 57.6 Nr. 4 und 5?",
                       "entscheidung": "Die Schranke sitzt je Bot, wo sein Scan den Einstieg bildet; ein Parameter trägt unter drei Bedingungen, sonst der Scan mit 37.3; eine Freigabe je Bauauftrag; Abnahme am Erzeuger (R98). Der Verweis in R90 (c) trägt; R91 (f) gilt an jeder Stelle, Indexzeile statt Marke; Lesarten zu 15.5 und Abschnitt 10 bestätigt (R99).",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 15a geschrieben: %s" % ziel)
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-164"):
        z[a[0]] = z[a[0]][:-2] + " · Register 61 (Fable 15a: R98 Schranke je Bot, Parameterweg, eine Freigabe je Bauauftrag, Abnahme am Erzeuger; R99) mit TB-165 (%s, Journal %s); als Nächstes TB-30b E-3, mit der Messung nach R98 (b) |" % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def kennung():
    h = max(kennungen()); print("Kennung %s (letzte %s)" % (naechste(h), h))
def journal(blk, probe):
    t = lies(blk); z = lies(JO).split("\n"); k = kennungen(); neu = naechste(max(k))
    b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-165: " % neu), "Kopfzeile ## %s — TB-165: …" % neu); p(len(i) == 1, "Anker genau einmal")
    p(bool(i) and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "davor '---' und Leerzeile"); p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---")
    p("### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Teile 'Was gemessen ist', 'In einfacher Sprache'"); p(neu not in k, "Kennung %s frei" % neu)
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["md5"]: md5cmd()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif a == ["kennung"]: kennung()
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
```
