### 45.11 R11 — Abbild gültig; Tatsachennotiz zum Abbruch TB-114 (Fable 27a, TB-117, 26.09.2026)

> ⟦Z:fab:104⟧
> ⟦Z:fab:105⟧

**Kette:** Vollzug der in **45.0** angekündigten Nummer 45.11 — nicht durch
TB-114 (Abbruch in Block C, `e07fefd`/`90307cb`), sondern mit Fables Antwort
27a (T114-2) in TB-117. Das Abbild ist seit TB-114 unverändert; gemessen am
Eingang von TB-117 (`753ec11`, `docs/belege/TB-117/0b_ausgang.txt`): sha256
`5e5ad1097909b3531e19b238153cabc46e7b551bb25e369ddc6735836e71cd06`, Sonde
dagegen 34/0/0. Der Satz in R11 „Nach dem Bündel (R9, R10, R14, R15) folgt
ein neues Abbild nach 37.3" wird in TB-117 Block E vollzogen; das Ergebnis
steht in **46.11**. Bis dahin gilt `5e5ad109…`. Die Marke unter 45.10 zeigt
hierher und auf 46.

## 46. Sonde zweiseitig, `fehlend` im Modus, zwei Erzeuger, Snapshot-Bindung, Herkunftsprüfung in `auswertung.py` — die Einträge aus Fable 27a (TB-117, 26.09.2026)

### 46.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **45**
(TB-114). Anlass ist die Tagesanfrage 27a an den Verfahrensprüfer
(`FABLE_ANFRAGE_2026-09-27a_tagesanfrage_tb114_tb115.md`) zu den Ergebnissen **TB-114** (Register 45,
dritte Öffnung von `herkunft.py`, Abbruch in Block C) und **TB-115** (drei
Verfahrensmessungen, nur lesend). Fables Einordnung, zeichengleich:
„⟦T:fab:72|**Ein Bündel, eine Freigabekarte je Sperrlistendatei** (`herkunft.py`, `auswertung.py`, Sonde), dann ein Abbild.⟧"

**Quelle:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md`
(md5 `d4367c65a9dcad4b28cceb6f50706d59`, 30 836 Bytes, committet in TB-117
Schritt 0, `753ec11`), Abschnitt „Registerblock — zeichengleich kopierbar,
nummeriert", R9–R17. ⚠️ **Tatsachennotiz zur Herkunft (wie 41.0, 43.0,
45.0):** Die Datei hat der steuernde Chat übertragen; die Zitate hier sind
zeichengleich mit der Datei im Repo, ob diese zeichengleich mit Fables Ablage
ist, ist nicht gemessen.

**Die Kette zu 45:** R11 ist die in 45.0 angekündigte Nummer **45.11** und
steht deshalb am Ende von 45, nicht hier. R9, R10, R12 bis R17 stehen als
**46.1 bis 46.8** in der Reihenfolge des Codeblocks. 45.7 (R7) bekommt mit
R16 (a) eine Nummer 7 der Liste; 45.5 (R5) mit R16 (b) einen Punkt (d); 45.8
(R8 (a)) wird mit der Öffnung von `auswertung.py` in TB-117 vollzogen (46.11).
Die Nummer 46 hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20), nicht Fable.

**Bauart je Eintrag:** 45.11 und 46.1 bis 46.8 tragen je einen Baustein
**zeichengleich** aus dem Codeblock am Ende der Fable-Antwort, samt seiner
„Quelle des Grundes", als Blockzitat, **eingesetzt, nicht abgetippt**; je
Baustein ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-117/a2_r_diff.txt`). Nichts ist umformuliert. Darunter steht
je Eintrag die Kette (wohin die Marke am alten Ort zeigt). 46.9 ist eine
Lesart des steuernden Chats, 46.10 die Liste des Offenen; der Vollzug in
TB-117 folgt als 46.11.

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)); die
Tatsachennotiz „an Punkt 8" aus R15 (a) steht deshalb in **46.6**, mit
Verweis auf Punkt 8. ⛔ **In Abschnitt 9 steht keine Marke.**

### 46.1 R9 — Ergänzung zu 40.8 (e) (Sonde, zweite Seite)

> ⟦Z:fab:98⟧
> ⟦Z:fab:99⟧

**Kette:** ergänzt **40.8 (e)** (die Sonde liest die Gruppen aus dem Abbild);
beantwortet T114-2 (Fable 27a Abschnitt 2). Marke in 40.8 als eigene
Tabellenzeile direkt unter der Zeile (e). **Fables erstes „Unsicher",
zeichengleich:**
„⟦T:fab:79|Ob `sperrlistensonde.py` selbst im Abbild oder auf der Sperrliste steht — wenn ja, folgt der Sonden-Öffnung ein Abbild nach 37.3; wenn nein, nicht. Nicht gemessen.⟧"
**Gemessen (TB-117, am Stand `753ec11`, nur lesend):** Der Listentext von
Abschnitt 10 nennt `sperrlistensonde` 0-mal; das Abbild `5e5ad109…` nennt die
Sonde einmal, und zwar nur als Parser im Feld `erzeugt`
(`"parser": "shared/sperrlistensonde.py::lies_abschnitt_10"`), in keinem
Punkt und in keiner Gruppe. Das neue Abbild nach dem Bündel folgt trotzdem, weil
`herkunft.py` und `auswertung.py` geöffnet werden (R11). Vollzug in TB-117
Block B (46.11).

### 46.2 R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`)

> ⟦Z:fab:101⟧
> ⟦Z:fab:102⟧

**Kette:** ergänzt **41.1 A10** (kein Fallback unter dem Modus); beantwortet
T114-1. Marke unter dem „Stand, gemessen" von A10. Der Nachtrag im Modulkopf
(R17 (a), 46.8) gehört zu derselben Öffnung. Vollzug in TB-117 Block C
(46.11).

### 46.3 R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen)

> ⟦Z:fab:107⟧
> ⟦Z:fab:108⟧

**Kette:** Tatsachennotiz zu **40.6**, **41.1 A12** und **45.3**; beantwortet
T114-3 und berichtigt die Lesart der Anfrage („folgt dann dem Pfad des
Erzeugers (R5)" — gemeint ist 40.6). Marken am Ende von 40.6, unter der
TB-114-Marke von 41.1 A12 und am Ende von 45.3. ⛔ **Nicht vollzogen und nicht
Teil von TB-117:** Die Listen werden nicht neu erzeugt, `EINGEFROREN` behält
die neun heutigen Listen.

### 46.4 R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4)

> ⟦Z:fab:110⟧
> ⟦Z:fab:111⟧
> ⟦Z:fab:112⟧
> ⟦Z:fab:113⟧
> ⟦Z:fab:114⟧
> ⟦Z:fab:115⟧
> ⟦Z:fab:116⟧
> ⟦Z:fab:117⟧

**Kette:** beantwortet F1-1 bis F2-3 (Fable 27a Abschnitt 3, M1 und M2).
Marke unter **16.4** („Prüfung vor dem Tag") für (f). Die Notizen (a) bis (e)
stehen hier und nicht an 5e, 28, 31 und Punkt 10, weil diese Stellen
Registertext bzw. Sperrlistentext sind (Punkt 10 liegt in Abschnitt 10, dort
steht keine Marke). ⭐ **(a) Die Probe** (vier Ausschlussmengen gleich) wird
in TB-117 Block E gebaut, ausserhalb der Sperrlistendateien; die Mengen
werden nur gelesen (46.11). ⛔ **(d) ändert vor dem Tag nichts** an
`shared/zuteilung.py`; die Messbitte steht als R7 Nr. 7 in 46.7 (a).

### 46.5 R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`)

> ⟦Z:fab:119⟧
> ⟦Z:fab:120⟧

**Kette:** ergänzt **12** (Vollständigkeitstest; `auswertung.py` bricht bei
jeder Verletzung des Datenvertrags ab) und **36.5** (Ausgänge); beantwortet
F3-3. Marken am Ende von 12 und am Ende von 36.5. Was R14 ohne Modus
bedeutet, sagt R14 nicht; die Lesart des steuernden Chats steht in **46.9**.
Vollzug in TB-117 Block D (46.11), zusammen mit R8 (a) (45.8).

### 46.6 R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8

> ⟦Z:fab:122⟧
> ⟦Z:fab:123⟧
> ⟦Z:fab:124⟧
> ⟦Z:fab:125⟧

**Kette:** beantwortet F3-1 und F3-2. ⭐ **Tatsachennotiz an Punkt 8 der
Sperrliste (Abschnitt 10), hier statt dort, weil in 10 keine Marke steht:**
Punkt 8 bleibt im Wortlaut und bindet die Repo-Dateien
`config/top25_symbols.txt` und `config/sp500_top150.txt`; unter dem Modus
liest der Lauf die Snapshot-Kopien, gebunden über das Abbild (Gruppe
`eingefroren`, R15 (a)). (a) wird in TB-117 Block C vollzogen
(`herkunft.py::EINGEFROREN`) und im neuen Abbild (Block E) gebunden
(46.11). (b) ist Tag-Vorbedingung und wird am Tag-Commit gemessen, nicht in
TB-117.

### 46.7 R16 — Ergänzungen zu R5 und R7

> ⟦Z:fab:127⟧
> ⟦Z:fab:128⟧
> ⟦Z:fab:129⟧
> ⟦Z:fab:130⟧

**Kette:** (a) ist **Nr. 7** der Liste in **45.7** (R7), vor dem Tag
ergänzt und damit nach 45.7 zulässig, datiert 26.09.2026 (Fable 27a);
Marke unter 45.7. (b) ist Punkt **(d)** zu **45.5** (R5); gilt für den
Zellen-Erzeuger, der noch nicht gebaut ist.

### 46.8 R17 — Tatsachennotizen 27a

> ⟦Z:fab:132⟧
> ⟦Z:fab:133⟧
> ⟦Z:fab:134⟧
> ⟦Z:fab:135⟧
> ⟦Z:fab:136⟧
> ⟦Z:fab:137⟧

**Kette:** (a) wird mit der Öffnung von `herkunft.py` in TB-117 Block C
vollzogen (46.11). (b) bis (d) sind Tatsachen; (c) und (d) schliessen die
Verfahrensmessungen aus 45.7 (R7) und damit Zeile (1) von 45.10.

### 46.9 Lesart des steuernden Chats zu R14 ohne Modus — von Fable zu bestätigen (Tatsachennotiz)

R14 nennt die fünf Abbruchbedingungen, sagt aber nicht, ob sie auch ohne
Selektionsmodus gelten. Der steuernde Chat hat im Auftrag eine Lesart
festgelegt und für Fable benannt, zeichengleich
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20):

„⟦T:auf:59|R14 unter dem Modus vollständig: Jede der fünf Bedingungen endet mit 2. Ohne Modus liest `auswertung.py` `herkunft.json`, wenn vorhanden, und zeigt Commit, Datenstand und Register-Hash im Kopf des Berichts, bricht aber nicht ab. Grund: Ohne Modus laufen Beispieldaten und Tests, und `beispieldaten.py` schreibt Nullwerte (Z. 210 ff.). Dieselbe Bauart wie R10 (`fehlend` ⇒ 2 nur unter dem Modus).⟧"

⚠️ **Vorläufig, bis Fable bestätigt.** TB-117 setzt diese Lesart in Block D
um; weicht Fables Antwort ab, ist das eine weitere Öffnung von
`auswertung.py`.

### 46.10 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | **Leiter-Lesarten** zu 16.4 (TB-116, fünf Stellen L1–L5) | Fable |
| (2) | **Der Listen-Erzeuger** nach 40.6 (41.1 A12, 45.5, 46.3) | Plan-Punkte 3 und 5 |
| (3) | **Der Zellen-Erzeuger** (Stufe V; 45.5, 46.7 (b)) | Stufe V |
| (4) | **Stufe IV** (Leiter-Skript, 16.11 Zeile 3) | Stufe IV |
| (5) | Bestätigung der Lesart **46.9** | Fable |
| (6) | R15 (b) `snapshot.py --pruefen` als Tag-Vorbedingung | am Tag-Commit |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich):
12 · 16.4 · 36.5 · 40.6 · 40.8 (e) · 41.1 A10 · 41.1 A12 · 45.3 · 45.7 ·
45.10. ⛔ Keine in Abschnitt 10, keine in 9.
