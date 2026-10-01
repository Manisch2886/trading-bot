# Bauplan Registerauftrag — stehende Bauart, angewandt in TB-114 und TB-117, für TB-126 (E-2: R18–R55)

Stand der Quellen: Upload `/mnt/user-data/uploads/trading-bot/` (HEAD `41864d4`). Pfade unten relativ zur Repo-Wurzel.
Kürzel: **AU114** = `docs/auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md`, **AU117** = `docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`,
**ER114** = `docs/ERGEBNIS_TB-114_register_45_herkunft_pfadregel.md`, **ER117** = `docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md`,
**AU124/ER124** = TB-124 (jüngste Auftragsform, kein Registerauftrag), **REG** = `docs/VORREGISTRIERUNG_neuselektion.md`, **ÜB** = `docs/projektfuehrung/UEBERGABE.md`.
„belegt“ = mit Fundstelle gelesen; **erschlossen** = abgeleitet, nicht gemessen.

**Grenzen des Uploads (wichtig für alle Befehle):** `docs/belege/TB-114/` und `docs/belege/TB-117/` fehlen (nur `TB-124/` liegt bei),
ebenso `research/vorregistrierung/` und `shared/sperrlistensonde.py`. Die Einsetz- und Prüfskripte (`eintrag_register_45.py`,
`eintrag_register_46.py`, `a2_r_diff.py`, `probelauf.sh`, `f_eintrag_46_11.py`, `0b_ausgang.sh`) sind deshalb **nur dem Namen nach**
belegt; ihr Inhalt und die genauen Aufrufe für `register()` und Sonde sind hier **nicht nachlesbar**.

---

## Ausgangswerte heute (gemessen am Upload bzw. aus dem jüngsten Beleg)

| Grösse | Wert | Fundstelle |
|---|---|---|
| REG Zeilen | 10 347 | `wc -l` am Upload; = `docs/projektfuehrung/REGISTER_INDEX.md:3` |
| REG sha256 | `18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c` | `sha256sum` am Upload; = REGISTER_INDEX:4; = `docs/belege/TB-124/0d_ausgang.txt` |
| REG md5 | `c8a32c0f0037c6c65bd08aae6be5a7c1` | `md5sum` am Upload (in keinem Dokument genannt) |
| letzter Registercommit | `1e11457` (27.09.2026, TB-118) | REGISTER_INDEX:3 (vom Upload aus nicht per git prüfbar) |
| Abschnitte | 0–46, letzter Unterabschnitt 46.11 (REG:10268–10347) | REG |
| `herkunft.register()` | `01f5997a9a13b4b30162e2a04965670a9ffa8d725a93d579e530dc0708ec2a70`, `fehlend []`, 23 Teile | ER117:23, :190; `docs/belege/TB-124/0d_ausgang.txt` und `c5_nachher.txt` |
| gültiges Abbild | `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d1d83…f281f` | REG:10315–10320 (46.11) |
| Sonde gegen dieses Abbild | **rc 2** (Normalfall), Pfad-Bestandteile 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“, Abschnitt-10-Text Z. 905–1018, eingefroren 22, Ausgabe-sha256 `dd4b4b95…`, 84 Zeilen | `docs/belege/TB-124/0d_ausgang.txt` |
| `test_vorregistrierung` | 196/196, Laufzeit ca. 895–899 s | ER114:51; ER117:172 |
| Nummern frei | TB ab 126 · Journal ab **DX** · R-Blöcke ab R56 | ÜB:389 |

---

## 1. Kopf und Schritt 0

### 1.1 Kopf (belegt, AU114:1–24, AU117:1–29, jüngere Form AU124:1–41)
- Titelzeile mit Inhalt; `**Sitzungstitel:**`, `**Angelegt:**` (Datum, Uhrzeit, „vom steuernden Chat“), `**Vorgänger:**` (TB-Nr. + Commit), `**Aufwand:** hoch (ARBEITSWEISE 22.1)` (AU114:3–4).
- `**Grundlage:**` je Fable-Antwort mit Dateiname, **md5 voll**, Bytes, „wird in Schritt 0 committet“, und wo der Registerblock steht (AU117:5).
- Jüngere Pflichtzeilen (AU124:3–5): Repo/Base, **Interpreter immer `trading-env/bin/python3`**, Rückfragen wörtlich ins Ergebnis, „Abbruchkriterium führt zu Abbruch, nicht zu Rückfrage“, **„Jedes Prüfskript liegt unter `docs/belege/TB-nnn/` und wird mitcommittet“**.
- Abschnitt **„Belegt · erschlossen · offen“** mit Messzeitpunkt und Weg der Messung (AU124:43–73).

### 1.2 Freigabezeile (belegt)
- `## ⭐⭐ Freigabe des Betreibers, wörtlich` mit Datum, Uhrzeit, Kanal („Auswahlkarte im steuernden Chat“), Kartentext kursiv und gewählte Option fett (AU114:7–9; AU117:7–13).
- Tabelle `| freigegeben | Pfad / Handlung |`, je Datei eine Zeile; für das Register: „**anhängen**, Marken additiv“ (AU114:11–17; AU117:15–22).
- `⛔ Nicht freigegeben:` mit Grund; in Registeraufträgen stehend: **jede Marke im Listentext von Abschnitt 10**, **Eintrag in Register 9**, Überschreiben eines Abbilds, Code ausserhalb, `crontab`, Datenbanken (AU114:19–24; AU117:24–29). AU124:31–37 gibt je Punkt einen *Grund*.
- Stand heute: E-2/TB-126 ist **nicht freigegeben**, Einzelfreigabe per Karte (M3) (ÜB:213, :276, :302).

### 1.3 Sichtschutz (belegt)
- In TB-114/117 kein eigener Absatz, aber angewandt: Zeilenzahlen der Handelslisten „stehen nur im Beleg — Trade-Zahlen nach 27.1, gehen nicht an Fable“ (ER114:31). Registerabschnitte tragen „⭐ Sichtschutz 27.1: keine Ergebnisgrösse des Selektionsraums; Feldnamen ohne Werte“ (REG:9243 ff., 42.7).
- Jüngere Form: eigener Absatz „**Sichtschutz 27.1:** … liest keine Kennzahl, keine Trade- und keine Zeilenzahl …; aus Testausgaben nur rc, Dauer, Schlusszeile“ (AU124:39). **Für TB-126 übernehmen** (erschlossen: reiner Textauftrag, also kurz: kein Lauf, keine Ausgabe, aus Tests nur rc/Dauer/Schlusszeile).

### 1.4 Schritt 0 (belegt)
- **0a — committen:** Tabelle der erwartet uncommitteten Dateien (Auftrag, `AKTUELLER_AUFTRAG.md`, Fable-Antwort mit md5); „Weitere Dateien: melden, nicht mitcommitten“; Commit-Text vorgegeben; Push (AU114:30–38; AU117:35–43). Jüngere Form: exakte `git status --short`-Liste, „gemessen vom steuernden Chat … mit `git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`“, „Weicht etwas ab ⇒ Abbruch“ (AU124:77–88).
- **0b — Ausgangswerte** in `docs/belege/TB-nnn/0b_ausgang.txt`: `register()` (Soll mit Präfix), Hashes der berührten Sperrlistendateien, Sonde gegen das gültige Abbild (Soll x/0/0, (ii) 0), Benchmark (AU114:40–46; AU117:45–49). Jüngere Form: „**messen, nicht annehmen**“, `git status --porcelain` vor und nach der Sonde zählen (AU124:101–106).
- **Wie gemessen:** Skript `0b_ausgang.sh` im Belegordner (ER122:50; AU124:101 „Bauart wie `docs/belege/TB-122/0b_ausgang.sh`“). Ausgabeform belegt in `docs/belege/TB-124/0d_ausgang.txt`: Kopfzeile HEAD + Zeit; `sha256` je Datei; Block `## herkunft.register()` mit `register <64 hex>`, `fehlend []`, `teile 23`; Block Sonde mit porcelain-Zählung vorher/nachher, `rc`, Ausgabe-sha256 + Zeilenzahl, Zeile (ii), `Pfad-Bestandteile …`, `RUECKGABEWERT 2 NICHT PRUEFBAR …`.
  - **erschlossen, nicht nachlesbar:** Aufruf `trading-env/bin/python3` mit `import herkunft; herkunft.register()` aus `research/vorregistrierung/` bzw. `python3 shared/sperrlistensonde.py <abbild>` (Option `--json` existiert, ER114:47 „JSON-Bericht ohne das Feld `zeilen`“). → Im Auftrag **nicht neu erfinden**, sondern „wie `docs/belege/TB-124/` 0d / `docs/belege/TB-122/0b_ausgang.sh`“ vorgeben.
- **md5 des Registers** stand in TB-114/117 **nicht** in 0b (dort `register()` und Code-Hashes); TB-124 0d misst sha256 des Registers. Für TB-126 erschlossen sinnvoll: sha256 **und** md5 von REG (Soll oben), Zeilenzahl 10 347.
- `test_vorregistrierung` 196/196 war in TB-114/117 **kein** 0b-Wert, sondern Nachweis nach dem Eintrag (AU114:79; AU117:80). Für TB-126 erschlossen: als Basis in 0 mitlaufen lassen (Laufzeit ~15 min, **ohne Zeitgrenze**, s. 9).
- Für TB-126 zusätzlich in Schritt 0 (belegt, Betreiber/ÜB): `git worktree remove` für `tb123_vorher*`, danach nachmessen (ÜB:379); zwischengelagerter BACKLOG-/Journal-Wortlaut aus dem Nachtrag 22:40 als eigene Einfügung (ÜB:390, Wortlaut ÜB:370–373).

---

## 2. Fable-Einträge zeichengleich einsetzen

### 2.1 Bauart (belegt)
- „Zitate werden **eingesetzt, nicht abgetippt**; vorher Probelauf gegen eine Kopie“ (AU117:53; REG:9905–9910, 45.0; REG:10109–10114, 46.0).
- TB-114: Einsetzskript `eintrag_register_45.py` („Kopie der TB-113-Bauart“), **Quellen gelesen aus dem Schritt-0-Commit** (`git:79c2dfa:…`), Probelauf `probelauf.sh` gegen eine Kopie, danach Register `cmp`-gleich mit der Kopie (ER114:35–36).
- TB-117: **Vorlage `abschnitt46_vorlage.md` mit Platzhaltern** + Einsetzskript `eintrag_register_46.py`, Quellen `git:753ec11:…` (Fable-Antwort **und Auftrag** am Stand Schritt 0), Probelauf gegen Kopie, dann einmal echt (ER117:29–31).
- **Wachen im Einsetzskript** (ER117:31–32): Eingangszeilenzahl (dort 10034), keine Marke in 9 oder 10, Abschnitt 10 unverändert, jede alte Zeile in derselben Reihenfolge im neuen Text (= additiv). Für 46.11 eigenes Skript `f_eintrag_46_11.py` „nur Anhängen“, Wachen: Eingangszeilen, Nummer fehlt noch, 46 ist letzter Abschnitt (ER117:187–188).
- Form im Register: je Baustein ein Unterabschnitt `### 46.n Rnn — <Titel>`, der Baustein als **Blockzitat** (`> ` je Zeile), samt „Quelle des Grundes“, darunter `**Kette:**` (was er ergänzt/beantwortet, wo die Marke steht) (REG:10126–10143; Kopfregel REG:10109–10114).
- Kopf `x.0` (belegt, REG:9878–9921, 10084–10124): „Reines Eintragen von Registertext und Tatsachen, Bauart wie …“; Anlass; **Quelle mit Dateiname, md5, Bytes, Commit von Schritt 0** und Abschnitt „Registerblock …“; **Tatsachennotiz zur Herkunft** („Die Datei hat der steuernde Chat übertragen; … ob diese zeichengleich mit Fables Ablage ist, ist nicht gemessen“); Kette zum Vorabschnitt; „Die Nummer hat der steuernde Chat vergeben (Auftrag, Freigabe …), nicht Fable“; Bauart je Eintrag; Regel aus 34; ⛔ keine Marke in 10 (und 9).
- Ausnahme Reihenfolge: ein Baustein, dessen Nummer vorher angekündigt war, steht am angekündigten Ort (R11 als 45.11 am Ende von 45, nicht in 46; REG:10102–10104).

### 2.2 Anker und Grenzen der Quellen für TB-126 (gemessen am Upload)
| Quelle | Registerblock | Form | R |
|---|---|---|---|
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md` (211 Z.) | Überschrift Z. 158 `## Registerblock — zeichengleich kopierbar, nummeriert`, Fence Z. 160 ` ```markdown ` bis Z. 210 ` ``` ` | Markdown: `**R18 — …**`, `*Quelle des Grundes:*` | R18–R32 (15), 2 oder 7 Zeilen je Baustein, R31 mit (a)–(e) |
| `…_2026-09-29b_sammlung_erzeuger_kalter_leser.md` (269 Z.) | Z. 187 `## Registerblock … (ab R33)`, Fence Z. 189 ` ``` ` bis Z. 268 | **Klartext** ohne Fettung: `R33 — …`, `Quelle des Grundes:` | R33–R52 (20), 2/10/13 Zeilen, R48/R49 mit (a)–(h) |
| `…_2026-09-30a_vorgepruefte_fragen_e2.md` (12 925 B, md5 `f9cdbbef…`) | Z. 24 `Registerblock — … (ab R53)` **ohne `##` und ohne Fence**, Bausteine Z. 25–32 bis Dateiende | Klartext | R53–R55 (3), je 2 Zeilen |

- Inventar 38 Blöcke ohne Lücke/Dopplung (27c 15, 29b 20, 30a 3) — belegt ÜB:216.
- **30a ist eine Abschrift ohne Markdown**; die Ablage-Fassung heisst `…_30a_vorlauf_aggregation_leere_menge.md` (md5 `5e5401bc…`, 13 165 B). R53–R55 bytegleich geprüft ⇒ „TB-126 darf R53–R55 aus der Repo-Datei nehmen“ (ÜB:193, :391). Die md5 der Repo-Datei gehört in den Kopf und in 0b.
- ⚠️ Im Text von 29b stehen R-Nummern auch ausserhalb des Blocks (z. B. Z. 130, 142 „→ **R48 (d)**“); Anker darum **nur** zwischen den Fence-Zeilen bzw. ab Z. 24 (30a). Erschlossen: Baustein = von `^(\*\*)?R<n> —` bis vor die nächste solche Zeile, Leerzeilen nicht mitgezählt.
- Erschlossen: Die md5 von 27c und 29b sind am Upload `ff96392e…` und `898d5bd5…` (nur 8 Stellen gemessen) — voll im Auftrag nennen, von der Sitzung in 0a prüfen lassen.

### 2.3 Nachweis (belegt)
- **R-Diff je Baustein, rc 0:** „`a2_r_diff.py` liest Fable-Datei und Register **unabhängig vom Einsetzskript**: 8/8 diff rc 0“ (ER114:41); TB-117 9/9 (ER117:18). Beleg `docs/belege/TB-nnn/a2_r_diff.txt` (REG:9909, 10113).
- **Mutationsprobe:** ein Wort in einem Baustein geändert ⇒ rc 1 (`a2_r_diff_mutation.txt`, ER114:41; „Mutationsprobe R13 rc 1“, ER117:18).
- **Zitate-diff:** alle übrigen eingesetzten Zitate (Teilzitate im Kopf, „Unsicher“-Sätze, Lesart aus dem Auftrag) einzeln `diff` rc 0: 38 Zitate (31 Zeilen, 7 Teile) in TB-114 (`a3_zitate.txt`, ER114:46), 35 in TB-117 (ER117:18). Kein Zitat-diff für einen Abschnitt ohne Zitat (46.11; ER117:191).
- Für TB-126 erschlossen: 38 R-Diffs; wegen dreier Quellformate (Fence markdown / Fence plain / ohne Fence) das Prüfskript mit **drei expliziten Grenzpaaren** (Datei, Startzeile, Endzeile) statt Mustersuche; Prüfskript liegt im Belegordner.

---

## 3. Marken am alten Ort

- **Was:** Jeder Eintrag, der einen alten Satz berichtigt, präzisiert oder ergänzt, steht zusätzlich als **Marke direkt unter dem alten Satz**; „der alte Satz bleibt zeichengleich; die Marke fügt nur hinzu“. Eingeführt in 34 (REG:5899–5908), Grund (Fable 21m, wörtlich REG:5904–5906): „Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme.“ Fortgeschrieben „Die Regel aus 34 gilt weiter“ (REG:8319, 9919, 10120).
- **Wortlaut** (belegt, REG:2975–2977, 8448–8449, 9518–9519): Blockzitat, neue Leerzeile davor:
  `> ⭐ **<Sache>: siehe 46.2** (Fable 27a R10, TB-117, 26.09.2026).`
  `> Eintrag und Stand oben bleiben zeichengleich.`
  Varianten: „Von Fable bestätigt (26a 3 (1)), siehe 45.1“, „beantwortet und fortgeschrieben in 45.11 und 46“. Der Kerntext steht im Auftrag (Tabelle `| Wo | Marke |`, AU114:62–72; AU117:61–73).
- **Wo:** direkt unter dem Anker, **nie in ein Zitat hinein**, sondern darunter; bei mehreren Marken unter die letzte vorhandene (ER117:41–55, Ankertabelle). In **Tabellen** als eigene Zeile `| ↳ (e) | ⭐ **Zweite Seite: siehe 46.1** (…); die Zeile oben bleibt zeichengleich | 46.1 |` direkt unter der Zeile (REG:8202; REG:9221; ER114:44; ER117:50). Wo ein Anker nicht eindeutig ist: im Ergebnis nennen, wo und warum (AU117:73).
- **Warum nie in 10:** Die Sperrlisten-Sonde vergleicht den Listentext von Abschnitt 10 mit dem Abbild (36.6, Prüfung (ii)); eine Zeile dort ändert den Listentext (REG:8323–8325; REG:9242; REG:9921). Was dorthin gehörte, steht im neuen Abschnitt mit Verweis auf den Punkt (z. B. Tatsachennotiz „an Punkt 8“ in 46.6, AU117:26; REG:10122–10124). Historisch: TB-87 setzte noch eingerückte `>`-Zeilen ohne Leerzeile in 10 (REG:6654–6658) — seit TB-108 verboten.
- **Warum nicht in 9 (bisher):** Auftragsregel, nicht Sondenregel: „ein Eintrag in Register 9 (der Verweis aus R8 (d) kommt **nach** dem Tag)“ (AU114:23); in 46.0 als „⛔ In Abschnitt 9 steht keine Marke“ (REG:10124).
- **append-only trotz Marken mitten im Text:** Marken sind **nur neue Zeilen**, nichts wird entfernt ⇒ `git diff --numstat` auf REG zeigt in der **zweiten Spalte 0** (TB-114 218/0, ER114:46; TB-117 232/0, ER117:18; 46.11 81/0, ER117:189). Zusätzlich im Einsetzskript: jede alte Zeile in derselben Reihenfolge im neuen Text (ER117:31–32). Abbruch bei zweiter Spalte ≠ 0 (AU114:156; AU117:193).
- **Nebenwirkung:** Eine Marke **vor** Abschnitt 10 verschiebt dessen Zeilen (TB-114: 901–1014 ⇒ 905–1018); die Sonde bleibt inhaltlich gleich („Listentext wie bei Erzeugung: ja“), aber nur der JSON-Bericht **ohne Feld `zeilen`** ist vorher = nachher (ER114:46–50).
- Marken-Liste steht am Ende im x.10 „Was offen bleibt“ (REG:10262–10264) bzw. in der „Nicht getan“-Tabelle (REG:9247–9252).

---

## 4. Tatsachennotiz und Hash-Übergang nach 37.3

- **Regel 37.3** (Fable 22g, zeichengleich REG:6739): Ein Befund 1 der Sonde **vor dem Tag** ist zulässig, wenn die Änderung beauftragt war — **Pflichtteile: Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz**; geschlossen durch ein **neues Abbild unter neuem Namen**, nie durch Anpassung. Handwerk: Abbilder **nach Bündeln**, nicht nach jeder Änderung; „dass das letzte zum Tag-Commit passt, ist alles“ (REG:6755).
- **Form (belegt, 46.11, REG:10268–10347):**
  1. Kopfsatz „**Gemessen in TB-nnn, Datum** (Belege …, Ergebnis …). Eingang `<commit>`, Schritt 0 `<commit>`, Block A `<commit>`. Freigabe des Betreibers <Datum, Uhrzeit> (Auswahlkarte, wörtlich im Auftrag). Kein Abbruchkriterium ausgelöst.“ (REG:10270–10274)
  2. „**Hash-Übergänge nach 37.3:**“ Tabelle `| Block | Datei | vorher | nachher | Commit | vollzieht |` (REG:10276–10282).
  3. `herkunft.register()`-Kette mit Präfixen je Block (REG:10284–10288) und der **Selbstbezugssatz**: „Der Wert nach diesem Eintrag kann hier nicht stehen (er hasht diesen Text); er steht im Ergebnis.“ (REG:10287–10288; Regel aus 42.5, REG:9690–9691).
  4. je Block ein Absatz „was vollzogen“; gültiges Abbild (Name, sha256, Grösse, Punkte, HEAD); Sonde gegen das alte Abbild mit Zuordnung; „Unverändert gemessen“; „**Nicht vollzogen in TB-nnn:**“ (REG:10290–10347).
- Kurzform für Code ausserhalb des Abbilds (TB-122/TB-124-Entwürfe, ER122:230–276, ER124:284–323): Titel „**Vollzug … in TB-nnn (Tatsachennotiz nach 37.3)**“, Gemessen-Satz, **Grund**, Tabelle `| Datei | vorher | nachher | Commit | vollzieht |`, „`herkunft.register()`: `01f5997a…` alt = neu … der Übergang steht deshalb nur hier und im Commit“, **Nachweis**, **Stand 11.3**. Beide sind als „⚠️ ENTWURF — nicht im Register“ markiert (ER122:232–233; ER124:286–287).
- **Kurzes Beispiel** (REG:10276–10282, gekürzt):
  `| C | research/vorregistrierung/herkunft.py | ed521ac1… | c6c13388… | ff2f254 | R10 (46.2), R15 (a) (46.6), R17 (a) (46.8) |`
- Für TB-126 (erschlossen): **keine** Code-Datei bewegt sich ⇒ kein Hash-Übergang einer Sperrlistendatei, **kein neues Abbild** (vgl. 42.7, REG:9241: „Kein neues Abbild — keine Sperrlistendatei hat sich bewegt“). Die Tatsachennotizen TB-122/TB-124 werden aus den Entwürfen übernommen; die Vollzugsnotiz von TB-126 selbst nennt nur `register()` alt (Selbstbezug: neu nur im Ergebnis).

---

## 5. Was sich durch den Eintrag ändert und wie es gemessen wird

- **`register()` ändert sich bei jedem Registercommit**, weil es die Registerdatei mithasht (REG:9690 „`register()` hasht dieses Register mit (42.5)“). Gemessen und belegt: TB-114 A `a0e477fd…` ⇒ `03178075…` (ER114:50); TB-117 A `5acb4c19…` ⇒ `6bcb4f58…`, F `e87a4d8e…` ⇒ `01f5997a…` (ER117:18, :23). Im Auftrag als „`register()` alt/neu“ gefordert (AU114:78; AU117:79). Der neue Wert gehört **nur ins Ergebnis** (Selbstbezug). Erschlossen für TB-126: Soll „neu ≠ alt, `fehlend []`, Teile 23 unverändert“.
- **Sonde gegen das gültige Abbild vorher = nachher** (AU114:77; AU117:78). Gemessen: TB-114 „der JSON-Bericht ohne das Feld `zeilen` hat vorher und nachher denselben Hash `d612402a…`“ (ER114:47); TB-117 „JSON-Hash `6840f57f…` gleich“ (ER117:18), F „`9f7364ef…` gleich, 37/0/0“ (ER117:189). **Grund, warum die Sonde gleich bleibt** (erschlossen aus TB-124 0d): Das Register steht nicht als Pfad im Abbild; die Sonde liest aus ihm nur den Listentext von Abschnitt 10 (Prüfung (ii)).
- Rückgabewert der Sonde ist **2** im Normalfall („NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]“, `0d_ausgang.txt`; ER114:31 „rc 2 nur für die Regel-Bestandteile, wie immer“). Soll also nicht „rc 0“.
- `test_vorregistrierung` 196/196 nach dem Eintrag (AU114:79; AU117:80).
- Erschlossen für TB-126 zusätzlich: `registerbericht.py --pruefen` rc 0 (der ERZEUGT-Block in 3 darf sich nicht ändern, REG:224–230, 430).

---

## 6. Registerkopie Teil 1–4 und Ablage-Abgleich

- **Wer:** „Registerkopie | nach jedem Registerauftrag erneuert … Die **Mac-Sitzung** erzeugt sie im Registerauftrag mit `docs/werkzeuge/registerkopie.py`, Teile committen; `--marken` für `REGISTER_INDEX.md` | Mac-Sitzung erzeugt, **steuernder Chat legt ab**“ (ARBEITSWEISE 23.4, Projektablage; ebenso `docs/werkzeuge/registerkopie.py:33–34`).
- **Aufruf** (aus der Repo-Wurzel, `registerkopie.py:22–31`):
  - `trading-env/bin/python3 docs/werkzeuge/registerkopie.py` — schreibt `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` und prüft selbst; rc 0/1/2/3 (`:36–38`).
  - `--pruefen` (Bodies bytegleich zum Original am Kopf-Commit, jeder Teil ≤ 240 000 B), `--marken` (MARKE/MARKE+/UEBERSCHRIFT mit Zeile, Abschnitt, Teil), `--ziel <ordner>` für eine Probe.
  - **Nur nach dem Registercommit:** liest `git show HEAD:<REG>`, Abbruch 2, wenn der Arbeitsbaum abweicht (`:66–81`). Kopf-Commit = letzter Registercommit (`git log -1 -- <REG>`) ⇒ **nach dem letzten Commit, der REG ändert**, laufen lassen.
  - Löscht nichts; Teile mit höherer Nummer als `m` werden als VERALTET gemeldet (`:39–40`, `:169–172`).
- **REGISTER_INDEX.md** mit erneuern: „Die Marken misst das Skript neu, die Ketten liest die Sitzung aus seiner Ausgabe. Die Teil-Nummern in der Spalte T … ändern sich mit“ (REGISTER_INDEX:133–135). Fable verlangt für 10 und 17.3/17.9/18 **Indexzeilen** statt Marken (29b R51, Z. 263).
- ⚠️ **Zuschnitt wird sich verschieben (erschlossen, am Upload gerechnet):** Teil 1 (Abschnitte 0–23) hat Body 239 294 B + Kopf 240 B ⇒ **466 B Luft**. Jede Marke in 0–23 (R51 verlangt mehrere in 0–12) schiebt Abschnitt 23 (28 981 B) nach Teil 2 (Luft 19 091 B) ⇒ 37 (29 887 B) nach Teil 3 (Luft 12 889 B) ⇒ 43 nach Teil 4. Alle vier Teile bekommen neue Abschnittsgrenzen; die T-Spalte im Index ändert sich überall. Ein Teil 5 ist nach dieser Rechnung nicht zu erwarten (Teil 4 wächst um 43 + den neuen Abschnitt), sicher ist das erst nach dem Lauf.
- **Ablage-Abgleich** (UMZUG.md Abschnitt 4, Schritt 4, Z. 189–208; ARBEITSWEISE 23.3): (1) Ist-Liste der Ablage aus der Projektschnittstelle holen — **nur der steuernde Chat** hat sie (ER118 E: „die echte hat nur der steuernde Chat“); (2) `python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner> [--heute JJJJ-MM-TT]` ⇒ `soll.txt`, `entfernen.txt`, `ablegen.txt`, `ohne_regel.txt` (`ablage_soll.py:14–18`, `:280–283`); (3) **erst ablegen, dann entfernen**, `ohne_regel.txt` ansehen, nicht löschen; (4) `knowledge_size` vorher/nachher, eine Zeile in `UEBERGABE.md`. Das Skript „löscht und legt nichts ab — das tut der steuernde Chat“ (`:38`).
- **Aufteilung (belegt + erschlossen):** Mac-Sitzung: `registerkopie.py`, `--pruefen`, `--marken`, REGISTER_INDEX nachziehen, committen, pushen. Steuernder Chat nach Abnahme: Ist-Liste, `ablage_soll.py` (über die Geräteanbindung), `project_write` der vier Teile und des Index, md5 **maschinell** vergleichen (nicht Inhalt in den Chat holen, ÜB:382 Fehler Nr. 7; T7 ÜB:310), entfernen, `knowledge_size`, Zeile in ÜB.
- ⚠️ Erschlossen: `ablage_soll.py` vergleicht über den **Dateinamen** (`:16–18`). Die 30a-Antwort heisst in der Ablage anders als im Repo (ÜB:356) ⇒ die Ablage-Fassung wird voraussichtlich unter `entfernen`/„Dialogpaar“ und die Repo-Fassung unter `ablegen` erscheinen. Vorher entscheiden, welche Fassung in der Ablage bleiben soll. Zudem: Wird 27c/29b/30a im Dialog-Index nach TB-126 „registriert“, verlassen nach B5 zitierte ERGEBNIS-Dateien die Ablage (`ablage_soll.py:174–190`).

---

## 7. Abgabe

- **Ergebnisdokument** `docs/ERGEBNIS_TB-nnn_<stichwort>.md` (AU114:136; AU117:177):
  - Kopfzeile mit Inhalt in einem Satz (inkl. numstat, Anzahl Marken, Abbild); Sitzungstitel, Stand, Auftrag, Belege; **Eingang und alle Commits**; Grundlage mit md5/Bytes „geprüft“; Freigabe; Umgebung `trading-env/bin/python3 (3.9.6)`; „Kein Abbruchkriterium ausgelöst“ (ER117:1–11).
  - „⭐ **Kurz:**“-Tabelle je Schritt/Block (ER114:13–22; ER117:13–23).
  - je Block ein Abschnitt mit Nachweisen und Belegdateinamen; Ankertabelle der Marken (ER117:41–55).
  - **„Für Fable“**: Fragen, Reibungen, nachgezogene Testannahmen, Lesarten zur Bestätigung (AU114:136–139; AU117:177). Jüngere Form: „nur falls eine Verfahrensfrage entsteht; der steuernde Chat prüft sie nach dem Fable-Filter vor“ (AU124:202).
  - **„Nicht getan“** (AU124:203) und **„In einfacher Sprache“** (ER114:177 ff.; ER117:239 ff.).
- **Journal:** Block `## <Kürzel> — TB-nnn: …` in `docs/projektfuehrung/JOURNAL.md` (AU114:135 DM; AU117:176 DP); jüngere Form: „ans Ende … mit der Quellenzeile auf das Ergebnis“, Kürzel vor dem Schreiben nachmessen (ARBEITSWEISE 14) (AU124:62, :206). Für TB-126: **DX** (ÜB:389).
- **Commits:** je Block ein Commit, „Nach jedem Commit Push“ (AU114:142–151; AU117:179–189).
- **porcelain** (jüngere Form, AU124:206): nach dem Abgabe-Commit `git status --porcelain` ⇒ `docs/belege/TB-nnn/e_porcelain.txt` als letzter kleiner Commit; belegtes Bild: genau 1 Zeile, die Datei selbst, plus `origin/main = <commit>` (`docs/belege/TB-124/e_porcelain.txt`).

---

## 8. Abbruchkriterien in Registeraufträgen (belegt)

- Ein Ausgangswert in 0b weicht ab (AU114:46, :155); 0a weicht ab (AU124:212).
- **`diff` eines R-Bausteins rc ≠ 0; numstat des Registers mit zweiter Spalte ≠ 0** (AU114:156; AU117:193).
- Sonde meldet gegen das gültige Abbild einen Befund (bzw. „anderes als erwartet“) (AU114:159); Abbild würde überschrieben (AU114:161; AU117:195).
- Änderung ausserhalb der freigegebenen Dateien nötig (AU117:196); `register()` ändert sich, wo es gleich bleiben muss (AU124:215 — gilt in TB-126 **nicht**, dort ändert es sich planmässig).
- Benchmark/Ausgaben/Trockenlauf/Test rot mit Bezug (AU114:160; AU117:194) — für einen reinen Registerauftrag nur `test_vorregistrierung` relevant (erschlossen).
- `git push` scheitert zweimal (AU124:216).
- **„Kein Abbruch sind“** ausdrücklich: Sondenmeldung gegen ein *altes* Abbild (beschreiben), Reibung Fable-Text ↔ Code (melden), abweichende Anzahlen (beschreiben) (AU117:198–201).
- **Bei Abbruch:** committen, was an Belegen da ist, **nie `JOURNAL.md` mit Platzhalter**, Grund in `abbruch.txt`, pushen, melden (AU124:218). Und: kein Registertext mit einem Befund, den der Auftrag nicht vorgesehen hat (ER114:21).

---

## 9. Was in TB-114/TB-117 nicht auf Anhieb ging — und was TB-126 deshalb ausdrücklich sagen sollte

| # | Was geschah | Fundstelle | Satz für TB-126 |
|---|---|---|---|
| 1 | Zwei unversionierte Dateien lagen im Baum (gemeldet, nicht committet) | ER114:17 | 0a als exakte Liste, gemessen mit `--no-optional-locks`; „weitere Dateien: melden, nicht mitcommitten“ |
| 2 | **Ungemessene Erwartung an ein Werkzeug** ⇒ Abbruch in Block C, 45.11 entfiel | ER114:101–110; REG:10069 (R11) | Jede Soll-Angabe mit Fundstelle (Beleg + Zeile), sonst „messen und beschreiben“, keine Erwartung |
| 3 | 0b-Soll „die Werte aus TB-116 0b“ existierte nicht | ER117:232 | Jeden 0b-Sollwert mit Präfix **und** Belegdatei angeben (heute: `docs/belege/TB-124/c5_nachher.txt`) |
| 4 | Marke unter 7.1 verschob Abschnitt 10 um 4 Zeilen | ER114:47–50 | „Sonde vorher = nachher“ heisst: JSON-Bericht **ohne Feld `zeilen`** gleich, (ii) 0, „Listentext wie bei Erzeugung: ja“. Textausgabe ist *nicht* bytegleich, sobald eine Marke vor Z. 905 steht. Die TB-117-Wache „Abschnitt 10 an derselben Stelle“ auf „Abschnitt 10 inhaltlich bytegleich“ umstellen |
| 5 | Anker 16.4: das Skript nahm jede `#`-Zeile als Abschnittsgrenze; erster Probelauf Abbruch ohne Schreiben | ER117:47 | Anker je Marke im Auftrag als eindeutige Zeichenkette mit Zählung „genau 1“ am Arbeitsbaum (Bauart TB-125, ÜB:222) |
| 6 | Anker 40.8 (e) war eine Tabellenzeile | ER117:50 | Tabellenanker ausdrücklich als `| ↳ (x) |`-Zeile vorgeben |
| 7 | Datei angefasst, die nur für einen anderen Block freigegeben war | ER117:114, :231 | Freigabetabelle nennt **jede** Datei: REG, `REGISTER_KOPIE_teil1–4.md`, `REGISTER_INDEX.md`, `JOURNAL.md`, `BACKLOG.md` (zwischengelagerter Wortlaut), Belegordner |
| 8 | Zeitgrenze 900 s zu knapp für `test_vorregistrierung` (899 s) | ER117:172 | `test_vorregistrierung` **ohne Zeitgrenze** |
| 9 | Erster Testlauf mit zwei unversionierten Dateien im Baum, abgebrochen | ER117:172 | Tests erst am sauberen Stand (porcelain vorher = 0 ausserhalb Beleg) |
| 10 | (aus ÜB) Vergleichsskripte lagen nicht im Belegordner; Einfügung unter falscher Dateiüberschrift | ÜB:366, :372–373, :386 | „Jedes Prüf- und Vergleichsskript liegt unter `docs/belege/TB-126/`“; Zieldatei je Einfügung in eigener Zeile |

**Neu für TB-126 (erschlossen aus REG und den Quellen):**
- **Zahlenteil 3:** R51 verlangt eine Marke „3, Zahlenteil“. Zwischen `<!-- ERZEUGT: registerbericht.py -->` (REG:230) und `<!-- ENDE ERZEUGT -->` (REG:430) darf nichts eingefügt werden, sonst `registerbericht.py --pruefen` rc 1 (REG:224–227). Marke **nach Z. 430**.
- **Abschnitt 9:** R51 verlangt „9 → R48 (b)“; 46.0 sagt „In Abschnitt 9 steht keine Marke“ (REG:10124), Grund war nur der Verweis aus R8 (d) nach dem Tag (AU114:23). Der Auftrag muss das ausdrücklich entscheiden.
- **Abschnitt 10:** R45 („Registertext zu Sperrlistenpunkt 10“) und R49 (g) zielen auf 10 ⇒ keine Marke dort, Verweis im neuen Abschnitt + Indexzeile (so verlangt es R51 selbst, 29b Z. 263).
- **Drei Quellformate** (2.2) ⇒ Grenzen explizit, und die Form im Register (Blockzitat) für Klartext-Bausteine festlegen.
- **TB-122/TB-124-Entwürfe:** Die Markierung „⚠️ ENTWURF — nicht im Register“ gehört nicht ins Register; „Stand 11.3“ aus TB-122 ist durch TB-124 überholt (ER122:274–276 gegen ER124:318–321). Im Auftrag sagen, ob zeichengleich mit Zitat-diff übernommen und wie die Überholung gekennzeichnet wird.
- **Zeilenangaben** in den Entwürfen (z. B. „Register Z. 265 und Z. 280“, AU124:51) wandern nach dem Eintrag; nach 38.2 tragen Zeilennummern ihren Commit (REG:16–22).

---

## 10. Offen — vom steuernden Chat im Auftrag zu entscheiden

1. **Gliederung:** ein Abschnitt 47 für alle 38 Bausteine oder 47/48/49 je Fable-Antwort (27c, 29b, 30a)? Gibt es angekündigte Nummern wie 45.11? (in den Quellen nichts gefunden; nur Bezug auf 46.11/45.11 im Text von 27c Z. 18–37).
2. **Marken-Tabelle** für 38 Bausteine (Titel „… zu X“ liefern die Orte; R48–R51 allein betreffen viele Stellen in 0–12). Jede Zeile mit Anker, Zählung „genau 1“.
3. **Abschnitt 9** (R51 vs. 46.0) — siehe 9.
4. **R53-Zählweise** L + 19 gegen wörtlich L + 20 (ER124:325–333; ÜB:198, :279) — Tatsachennotiz neben R53 oder Frage an Fable.
5. Offene Voraussetzungen nach `VORMESSUNG_E-2_2026-09-29.md` samt Nachträgen (ÜB:280).
6. Ob ein **Vollzugsabschnitt** (Bauart 46.11) in einem eigenen letzten Commit folgt — dann `registerkopie.py` erst danach (Kopf-Commit).
7. Ablage: welche 30a-Fassung bleibt; wann der Dialog-Index 27c/29b/30a auf „registriert“ setzt (Folge für B5).
8. Nicht nachlesbar im Upload und deshalb nur als „wie Beleg X“ vorzugeben: genaue Aufrufe von `register()` und Sonde (`docs/belege/TB-122/0b_ausgang.sh`), Einsetz- und Diff-Skripte von TB-114/117 (`docs/belege/TB-114/`, `docs/belege/TB-117/`).
