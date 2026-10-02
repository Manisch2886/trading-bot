# TB-129 Register — Fable 01a (R56–R62) als Abschnitt 51, 14 Marken am alten Ort; Registerkopie, Index und Dialog-Index nachziehen

**Sitzungstitel:** `TB-129` · **Modell:** Opus 5.5, Aufwand hoch (Registerauftrag, wie TB-126) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 02.10.2026 vom steuernden Chat
**Vorgänger:** TB-128 (`560ca75`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-129_register_fable_01a.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** immer `trading-env/bin/python3` (7c). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15). Ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Prüfwerkzeuge:** Jedes Skript, das diese Sitzung schreibt (Einsetzen, Prüfen, Vergleichen, Messen), liegt unter `docs/belege/TB-129/` und wird mitcommittet, auch Vergleichsskripte (`cmp`, `diff`).
**Bauart, keine Quelle:** TB-126 (`docs/auftraege/MAC_TB-126_register_e2.md`, Belege `docs/belege/TB-126/`). Wo dieser Auftrag „Bauart TB-126“ sagt, werden die dortigen Skripte als Vorlage übernommen, nicht neu erfunden. Wo sie und dieser Auftrag sich widersprechen, gilt dieser Auftrag. **Massgeblich für Überschriften, Ketten, Marken und Fundstellen ist Anhang A** (Daten-Block), gebaut und geprüft vom steuernden Chat am 02.10.2026 am Register `db108a6`.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**02.10.2026, Auswahlkarte im steuernden Chat (gestellt 09:13, Antwort eingetragen 10:02).** Kartentext: *„Gibst du TB-129 frei? Das umfasst: Register Abschnitt 51 anhängen (R56–R62 zeichengleich, dazu 51.8–51.10 mit den Messungen und einer vorläufigen Lesart des steuernden Chats), 14 Marken am alten Ort (keine in Abschnitt 9, 10 und im ERZEUGT-Block), Registerkopie, Index und Dialog-Index neu, BACKLOG-Block, Journal EA. Kein Code, kein neues Abbild, keine Einträge in registerdaten.py.“* Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**. Zweite Frage derselben Karte, zur Fassung des Eröffnungstextes vom 01.10.2026: gewählt **„Fassung 2“**; daraufhin hat der steuernde Chat nach der Freigabe zwei Sätze angepasst (51.8, Zeile R56; BACKLOG-Block, Punkt R56 (e)), sonst nichts.

| freigegeben | Pfad / Handlung |
|---|---|
| Register **anhängen** (Abschnitt 51: 51.0 Kopf, 51.1–51.7 = R56–R62 zeichengleich, 51.8–51.10 Text des steuernden Chats) und **14 Marken additiv** am alten Ort (Anhang A) | `docs/VORREGISTRIERUNG_neuselektion.md` |
| neu erzeugen, nachziehen | `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_<nn>.md`, `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` (beide über `docs/werkzeuge/registerkopie.py`), `docs/projektfuehrung/REGISTER_INDEX.md` |
| die Zeile für 01a und die Schlusszeile mit der Zahl der Antworten (das Werkzeug `docs/werkzeuge/dialog_index.py` schreibt die Datei neu; was es dabei sonst ändert, steht im Ergebnis) | `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` |
| ein Block (Schritt B) | `docs/projektfuehrung/BACKLOG.md` |
| Journalblock (Kennung messen, erwartet **EA**) | `docs/projektfuehrung/JOURNAL.md` |
| committen in Schritt 0 | dieser Auftrag, `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/projektfuehrung/UEBERGABE.md` |
| Belege, Ergebnis | `docs/belege/TB-129/`, `docs/ERGEBNIS_TB-129_register_fable_01a.md` |
| verwerfen, nur nach rotem Nachweis in A5 und nachdem der Diff als `abbruch_register.diff` gesichert ist | die eigene, uncommittete Änderung am Register (`git checkout -- docs/VORREGISTRIERUNG_neuselektion.md`) |

⛔ **Nicht freigegeben, mit Grund:**
- **Jede Zeile im Listentext von Abschnitt 10.** *Grund:* Die Sperrlisten-Sonde vergleicht ihn mit dem Abbild (36.6, Prüfung (ii)).
- **Jede Zeile im ERZEUGT-Block von Abschnitt 3** (zwischen `<!-- ERZEUGT: registerbericht.py -->` und `<!-- ENDE ERZEUGT -->`). *Grund:* `registerbericht.py --pruefen` vergleicht ihn mit dem Erzeuger.
- **Jede Änderung oder Löschung einer bestehenden Registerzeile.** *Grund:* Das Register ist append-only; Marken sind neue Zeilen (34). Nachweis: numstat zweite Spalte 0. Das gilt auch für die bestehenden `**Kette:**`-Zeilen in 47–49: Sie bleiben, wie sie sind.
- **Eine Marke, die nicht in Anhang A steht.** *Grund:* Die Sitzung baut die Markentabelle nicht selbst (ARBEITSWEISE 0, Fehler Nr. 9). Insbesondere **keine** Marke an 47.9, 47.13, 25.2, 50.1 und 50.4: R61 (b) zählt sie nicht auf; sie gehen als Frage an Fable (51.10).
- **Code jeder Art**, insbesondere `research/`, `shared/`, `strategies/`, `docs/werkzeuge/`. *Grund:* Textauftrag; eingefrorener Code bleibt zu. R59 (b) (Einträge in `registerdaten.py`) ist **nicht** Gegenstand; dafür braucht es eine eigene Freigabe.
- **Ein neues Abbild der Sperrliste.** *Grund:* Keine Sperrlistendatei bewegt sich.
- **Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests.** *Grund:* Sichtschutz; keine Voraussetzung dieses Auftrags braucht einen Lauf. `registerbericht.py --pruefen` ist kein solcher Lauf und in 0b und A5 verlangt.
- Löschen oder Verwerfen ausser dem einen Fall in der Tabelle; `crontab`, Datenbanken; `UEBERGABE.md`, `UEBERGABE_ARCHIV.md` und die Dateien `FABLE_ANTWORT_*`, `FABLE_ANFRAGE_*`, `FABLE_UEBERGABE_*` ändern (ausser dem Commit in Schritt 0). *Grund:* Das sind die Quellen.

**Sichtschutz 27.1:** Diese Sitzung liest keine Kennzahl, keine Trade- und keine Zeilenzahl aus Ergebnisdateien. Aus Testausgaben nur rc, Dauer und Schlusszeile. Code wird nur gelesen, wo Anhang A eine Fundstelle nennt. Die Kalenderzählung in `data/BTCUSDT_1d.csv` und `data/ETHUSDT_1d.csv` (Datum je Zeile, keine Kurse) ist eine Verfahrensmessung nach 27.2.

## Belegt · erschlossen · offen

*Gemessen vom steuernden Chat am 02.10.2026, 08:39–09:00, über die Geräteanbindung, nur lesend, an HEAD `560ca75` (= `origin/main`).*

**Belegt:**
- Register: 11 094 Zeilen, sha256 `b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1`, md5 `9a5a403f1488e00cb61cab7a4de25953` (= `docs/belege/TB-126/a6_messung_nachher.txt`). Letzter Commit, der es änderte: `db108a6`. Letzter Abschnitt: 50 (letzter Unterabschnitt 50.7). Die Datei endet mit einem Zeilenumbruch.
- Quelle der R-Blöcke: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md`, md5 `4995260b7af91d2f4c058b1e2c49e788`, 22 084 B, 133 Zeilen, im Repo seit `7238842`. Codezaun ```` ``` ```` Z. 112 bis Z. 133; Blöcke R56–R62 in Z. 113–132. Zwei unabhängige Abschriften aus der Ablage, `cmp` gleich (`UEBERGABE.md`, Nachtrag 01.10.2026, ca. 23:35).
- **Schnittregel (maschinell geprüft, 7/7):** Ein Block beginnt mit der Zeile, die mit `R<n> — ` beginnt, und endet einschliesslich der ersten folgenden Zeile, die mit `Quelle des Grundes:` beginnt. Jeder der sieben Blöcke hat genau zwei Zeilen; die Leerzeilen dazwischen gehören zu keinem Block. ⚠️ R-Nummern stehen auch ausserhalb des Zauns; geschnitten wird **nur** in Z. 113–132.
- Ausgangswerte mit Fundstelle `docs/belege/TB-126/a6_messung_nachher.txt`: `herkunft.register()` `525c9c42af5022ad659388631c7959a0752a7cbaec05c3b319c280651caf1bfc`, `fehlend []`, 23 Teile · gültiges Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f` · Sonde dagegen: rc 2 (Normalfall), Pfad-Bestandteile 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“, sha256 des JSON-Berichts ohne das Feld `zeilen` `9f7364ef32fd80ffba6931c776f3bdf43dc257a1f6aeac304cf818c89023f35e` · `registerbericht.py --pruefen`: rc 1 (bekannter Befund, ERGEBNIS_TB-126 Nr. 8; verglichen wird nachher gegen vorher) · `test_vorregistrierung` 196/196, rc 0, 910 s, am Arbeitsbaum von `1e13135` mit diesem Register (`docs/belege/TB-126/a6_test_vorregistrierung.txt`).
- Seit `69b9ced` (Abgabe TB-126) ist unter `research/`, `shared/`, `strategies/` nichts geändert (`git diff --name-only 69b9ced HEAD --` leer). Auch seit `1e13135` (Stand des Testlaufs) ist unter `research/`, `shared/`, `strategies/`, `config/`, `data/` nichts geändert (gemessen 02.10.2026, 08:56; die Sitzung misst es in 0c selbst).
- `registerkopie.py --pruefen` (Teile) am `560ca75`: rc 0, bytegleich.
- `FABLE_DIALOG_INDEX.md`: 50 Antworten, keine Zeile `01a`. `BACKLOG.md`: 254 Zeilen, der Anker `## 6 — Geparkt, null Arbeit` zählt 1, `Aus Fable 01a` und `Aus der Übernahme 02.10.2026` je 0.
- Nummern: TB frei ab 130 · Journal **EA** (aus ERGEBNIS_TB-128; die Sitzung misst) · R-Blöcke nach diesem Auftrag frei ab R63.

**Erschlossen:** Sechs der 14 Marken stehen vor Abschnitt 10 (Z. 944); der Abschnitt wandert um 18 Zeilen. Der Text der Sonde ist dann nicht mehr bytegleich, der JSON-Bericht **ohne das Feld `zeilen`** schon (Bauart TB-126, A6).

**Offen (die Sitzung misst, nimmt nichts an):** die Journal-Kennung; die neuen Zeilenbereiche und Teilgrenzen der Registerkopie; welche weiteren Zeilen `dialog_index.py` beim Neuschreiben ändert.

## Schritt 0 — Sicherung, Ausgang, Vorprüfung

**0a. Zuerst, bevor `docs/belege/TB-129/` entsteht:** `git status --porcelain > "$TMPDIR/tb129_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch. Danach die Datei nach `docs/belege/TB-129/0a_status.txt` kopieren.

*Eingetragen vom steuernden Chat am 02.10.2026 beim Ablegen (gemessen mit `git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`):*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-129_register_fable_01a.md
```

Commit `TB-129 Schritt 0: Stand des steuernden Chats 02.10.2026`, pushen. Danach steht für alle Quellenangaben der Commit von Schritt 0, im Folgenden **⟨S0⟩** (kurz, 7 Zeichen).

**0b. Ausgangswerte** ⇒ `docs/belege/TB-129/0b_ausgang.txt`, mit einem Skript `0b_ausgang.sh` in der Bauart von `docs/belege/TB-126/0d_ausgang.sh` (dort die Aufrufe von `herkunft.register()`, Sonde und `registerbericht.py --pruefen` übernehmen). **Messen, nicht annehmen.** Soll: die Werte unter „Belegt“ (Register: Zeilen, sha256, md5 · `herkunft.register()`, `fehlend`, Teile · Abbild-sha256 · Sonde: rc, 37/0/0, (ii), Listentext, sha256 des JSON ohne `zeilen`, dazu `git status --porcelain` gezählt vor und nach der Sonde · `registerbericht.py --pruefen`: rc und Ausgabe als Vergleichswert · md5 und Bytes der Quelle 01a). Dazu den Listentext von Abschnitt 10 (von der Zeile `## 10.` bis vor `## 11.`) und den ERZEUGT-Block von Abschnitt 3 (einschliesslich der beiden Kommentarzeilen) als `0b_abschnitt10_vorher.txt` und `0b_erzeugt_vorher.txt`. Weicht ein Wert mit Soll ab ⇒ Abbruch.

**0c. Basis `test_vorregistrierung`:** `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` ⇒ `0c_basis.txt`. Ist die Ausgabe leer, ist die Basis der Beleg `docs/belege/TB-126/a6_test_vorregistrierung.txt` (196/196); ein eigener Basislauf entfällt. Ist sie nicht leer: Basislauf am Stand ⟨S0⟩ **ohne Zeitgrenze** (Laufzeit rund 900 s), Soll 196/196, sonst Abbruch.

**0d. Vorprüfung vor jedem Registereintrag** ⇒ `docs/belege/TB-129/0d_vorpruefung.txt`, Skript `0d_vorpruefung.py`; das Prüfskript aus Anhang A darf übernommen werden. Alles am Commit ⟨S0⟩.
1. **Marken:** Jeder Anker aus dem Daten-Block kommt im Register genau 1-mal vor, steht am Anfang der genannten Ankerzeile, und jede Einfügestelle „nach Zeile N“ beginnt mit dem angegebenen Anfang. Weicht eine Marke ab ⇒ **Abbruch vor Schritt A**: Kopf und Ketten nennen die 14 Marken und müssen zeichengleich ins Register; bei gleichem sha256 (0b) kann ohnehin kein Anker abweichen.
2. **Quelle:** md5 der Antwortdatei; die Schnittregel ergibt genau R56–R62, je zwei Zeilen, in Z. 113–132.
3. **Noch nicht vergeben:** Im Register zählt `## 51.` 0, und keine Zeile beginnt mit `> R56 — `.
4. **Fundstellen für 51.8:** jede Zeile der Liste `fundstellen` im Daten-Block (Datei, Zeile, Teilzeichenkette: die Zeile enthält sie) und jede Zählung aus `zaehlungen` (Datei, Muster, Soll). Dazu die Kalenderzählung aus `kalender` für beide Kursdateien (erster Balken; Balken bis 2017-12-31; Datum an Index 149 und 150, nullbasiert; 31 Tage im Januar 2018; keine Lücke und kein doppeltes Datum bis 2018-01-31) und die Git-Tatsachen aus `git_tatsachen` (je Datei die Commits aus `git log --format=%h -- <datei>`; die Überschrift „Fassung 2“ steht in der Datei am `eaea530`, „Fassung 3“ erst am `7238842`; Commit-Datum `git log -1 --format=%cs` je Commit wie in `commit_datum`). **Weicht hier etwas ab ⇒ Abbruch vor Schritt A**, denn der Text von 51.8 stimmte dann nicht.

Commit `TB-129 0: Ausgang, Vorprüfung`, pushen.

## Schritt A — Abschnitt 51 und die Marken, in einem Lauf

**A1. Gliederung (vom steuernden Chat vergeben):** 51.0 Kopf · 51.1–51.7 = R56–R62 in der Reihenfolge des Codezauns (51.n = R(55 + n)) · 51.8–51.10 Text des steuernden Chats (A3). Überschriften und Ketten stehen exakt im Daten-Block von Anhang A (`ueberschriften`, je mit `kette`).

**Form je R-Block** (Bauart 47–49):

```
### <51.n> R<nn> — <Bezug, exakt aus Anhang A>

> <Zeile 1 des Blocks, zeichengleich>
> <Zeile 2 des Blocks, zeichengleich>

**Kette:** <exakt aus Anhang A>
```

Jede Zeile des Blocks wird zu `> ` plus der Zeile, unverändert. Leerzeile vor und nach jedem Unterabschnitt. Abschnitt 51 wird ans Dateiende angehängt, mit einer Leerzeile nach der letzten bestehenden Zeile.

**A2. Marken am alten Ort.** Die 14 Marken stehen fertig in Anhang A; massgeblich ist der Daten-Block. Die Sitzung baut die Tabelle **nicht** selbst. Sie setzt jede Marke an ihrer Einfügestelle ein, nachdem 0d Anker und Einfügestelle bestätigt hat: je Marke eine Leerzeile, Markenzeile 1, Markenzeile 2. ⟨DATUM⟩ ist der Tag des Eintrags (TT.MM.JJJJ). Eingesetzt wird von unten nach oben, weil die Zeilennummern am Original gelten; an derselben Einfügestelle steht die Marke mit der kleineren R-Nummer zuerst.

Regeln, nach denen Anhang A gebaut ist (zur Prüfung, nicht zum Neubauen): Gesetzt sind genau die Marken, die R61 (b) aufzählt. Nennt Fable an einem Ort zwei Blöcke (4.2: R48 und R60; 49.1: R57 und R59), sind es zwei Marken, je Block eine (Bauart TB-126). „50.5 — bestätigt durch R57“ steht mit dem Markenwort ERGÄNZT und dem Zusatz „die Lesart ist bestätigt“, weil `registerkopie.py --marken` nur ERSETZT, PRÄZISIERT, BERICHTIGT, ERGÄNZT und KORRIGIERT erkennt (`docs/werkzeuge/registerkopie.py`, `MARKE_WEITER`) und TB-126 Bestätigungen unter ERGÄNZT führt (Anhang A dort, Regel 7). Tabellenzeile: nach der Tabelle und den dort stehenden Marken. Eintrag (43-7): am Ende des Eintrags. Block in 47–50: nach dem Blockzitat und den dort stehenden Marken, vor der Zeile `**Kette:**` (wie die R54-Marke unter 48.16). Nie in ein Zitat oder einen Codeblock hinein; keine in Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block.

**A3. Text des steuernden Chats** — zeichengleich, mit ⟨S0⟩ und ⟨DATUM⟩ ersetzt (dieselbe Ersetzung macht das Prüfskript in A5). Der Kopf steht vor 51.1, der Schluss nach 51.7.

Kopf:

````
## 51. Fable 01a — Registerblock R56–R62 (TB-129)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md`, md5 `4995260b7af91d2f4c058b1e2c49e788`, 22 084 B, im Repo seit Commit `7238842`, unverändert am Commit ⟨S0⟩, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R56)“, Z. 113–132. Die Datei hat der steuernde Chat am 01.10.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` gleich (`docs/projektfuehrung/UEBERGABE.md` am Commit ⟨S0⟩, Nachtrag 01.10.2026, ca. 23:35). Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern 51.1–51.7 hat der steuernde Chat vergeben (Auftrag TB-129, Einzelfreigabe des Betreibers), nicht Fable. Dieser Kopf nennt Datei, md5 und Commit; das ist für die Antwort 01a die Bindung nach R56 (b). Gesetzt sind die Marken, die R61 (b) aufzählt: sieben Zeilen als Nachtrag zu E-2 und fünf aus dieser Antwort, zusammen 14 Marken, weil 4.2 und 49.1 je zwei Blöcke nennen. ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke. Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 51.8; eine Lesart des steuernden Chats steht in 51.9 und ist vorläufig; was offen bleibt, steht in 51.10. 51.8 bis 51.10 sind Text des steuernden Chats, nicht Fables.
````

Schluss:

````
### 51.8 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 01a „zu messen“ nennt. Gemessen über die Geräteanbindung, nur lesend, am 02.10.2026 am Stand `560ca75`; die Sitzung TB-129 hat in Schritt 0 jede Fundstelle am Commit ⟨S0⟩ nachgemessen (`docs/belege/TB-129/0d_vorpruefung.txt`). Zeilenangaben gelten am Commit ⟨S0⟩. Kein Ergebnis gelesen (27.1); die Kalenderzählung in den Kursdateien ist eine Verfahrensmessung nach 27.2.

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R56 (51.1) (b), (e) | der Eröffnungstext des Chats vom 01.10.2026 liegt mit Commit im Repo | `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md` trägt den Eröffnungstext in zwei Fassungen: Fassung 2 seit `eaea530` (01.10.2026), Fassung 3 seit `7238842` (02.10.2026). `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_neuer_chat.md` und die Antwort 01a liegen seit `7238842` im Repo | erfüllt für beide Fassungen, vor diesem Eintrag. Im Chat kam nach Angabe des Betreibers Fassung 2 an (Auswahlkarte, 02.10.2026); das gehört in die Tatsachennotiz nach R56 (e) (51.10) |
| R57 (51.2) | `BB_PERIOD + L − 1` in `backtest_breakout.py` ist ein nullbasierter Index | `strategies/volatility_breakout_crypto/backtest_breakout.py:119–122, 129` und `strategies/volatility_breakout/backtest_breakout.py:160–163, 170`: „0-basiert, rolling ohne min_periods“, „der Einstieg bei i braucht is_squeeze[i - 1]; also i >= BB_PERIOD + L - 1“, `start_i = BB_PERIOD + squeeze_lookback_days - 1` | trifft. Der Index ist nullbasiert, und die Bedingung liest die Vorkerze; beides zusammen ergibt L + 19 (01a, „Unsicher“ 1) |
| R57 (51.2) | `faltenplan.py` wendet einen Vorlauf v als „v Balken liegen davor“ an | `research/vorregistrierung/faltenplan.py:242` ruft `symbolbeginn`; `research/faltenplan_neun/faltenplan_neun.py:415–428` (`symbolbeginn`) ruft `warm_ab` (Z. 402–412), das `balken_datum(pfad, eig["vorlauf_balken"], anker)` zurückgibt; `balken_datum` (Z. 301–318): „Das Datum des `nummer`-ten Balkens (0-basiert) ab `anker`“ | trifft: „warm ab“ ist der Balken mit Index v, v Balken liegen davor |
| R60 (51.5) (a) | `research/exposure_messung/` gehört nicht zum Laufbereich | `shared/paths.py:242` (`ARBEITSBAUM_PFADE`) und `docs/belege/TB-112/a2_laufbereich.txt:8` führen `research/exposure_messung/bot_lauf.py` (Lauf-Typ `trockenlauf`); es ist in beiden die einzige Datei des Ordners. `exposure_kern.py` und `research/exposure_messung/auswertung.py` (Z. 234, 50.1) stehen nicht darin; `bot_lauf.py` importiert `exposure_kern` nicht | trifft für den Ordner **nicht**; trifft für die zwei Stellen, die die Grösse bilden ⇒ Lesart 51.9, an Fable |
| R60 (51.5) (b) | über welche Tage `beta_bereinigung` mittelt | `research/vorregistrierung/auswertung.py:502–503`: Fenster sind die Falten des Plans, deren Name in `selektionsfalten` steht, halboffen (Z. 510–511); die Reihe ist die der Gewinnerzelle (Aufruf Z. 665); gemittelt wird über die gemeinsamen Tage von Tagesreihe und Benchmark (`gemeinsam`, Z. 517; Spalte `exposure`, Z. 523; `np.mean`, Z. 528), zurück unter `mittlere_exposure` (Z. 537) | Falten und Zelle: trifft (R48 (d): „die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“)“). Tage: gemittelt wird über die gemeinsamen Tage mit dem Benchmark; ob das alle „Handelstage des Zeitraums“ nach R48 (d) sind, ist **nicht gemessen** ⇒ offen, an Fable mit R60 (c) (51.9, 51.10 Nr. 6) |
| R60 (51.5) (d) | die Zeile zu R48 (d) in 50.1 wird um die Fundstelle in `beta_bereinigung` ergänzt | Tatsachennotiz zu 50.1: Die Zeile nennt für `auswertung.py` nur Z. 405 (Eingabe aus `zellen.csv`). Dazu kommt: `auswertung.py::beta_bereinigung` bildet eine mittlere Exposure als arithmetisches Mittel der Spalte `exposure` der Tagesreihe (Z. 523, 528) und gibt sie als `mittlere_exposure` zurück (Z. 537) | ergänzt; die Zeile in 50.1 bleibt zeichengleich |
| R61 (51.6) (c) | der Wortlaut von Sperrlistenpunkt 14 | Abschnitt 10, Punkt 14: „Die Reihenfolge Selektion → Bestätigungsperiode → Bericht — im Kopftext von `auswertung.py` als Ablauf festgeschrieben“. Abschnitt 14 heisst „Der Nulltest S-E1“. R26 (47.9) schreibt „(12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun)“; R30 (47.13) heisst „Ergänzung zu 14 und zu den Tag-Vorbedingungen“ | trifft: gemeint ist Sperrlistenpunkt 14 |
| R62 (51.7) (a) | die Tagesdatei ist im Januar 2018 lückenlos | `data/BTCUSDT_1d.csv` und `data/ETHUSDT_1d.csv`, je: erster Balken 2017-08-17, 137 Balken bis 2017-12-31, Index 149 (nullbasiert) = 2018-01-13, Index 150 = 2018-01-14, 31 Tage im Januar 2018, keine Lücke und kein doppeltes Datum bis 2018-01-31 | trifft für beide Dateien: Der 150. Balken ist der 2018-01-13, der 2018-01-14 hat 150 Balken vor sich |
| R62 (51.7) (c) | 24 von 51 Abschnitten gelesen | Das Leseprotokoll von 01a nennt 24 Abschnittsdateien als vollständig gelesen und 27 Abschnitte als nicht gelesen; zusammen 51 (Abschnitte 0–50). Register am `db108a6`, sha256 `b5804659…` | passt |
| R59 (51.4) (b) | Bestand, keine Voraussetzung Fables | `research/vorregistrierung/registerdaten.py:213–216` führt das Bollinger-Fenster als Regel `bollinger_fenster` (20.0); `BB_PERIOD = 20` steht in `strategies/volatility_breakout_crypto/backtest_breakout.py:69` und `strategies/volatility_breakout/backtest_breakout.py:101`. Ob diese Regel der Eintrag nach R59 (b) ist und ob eine Probe gegen `BB_PERIOD` besteht, ist nicht gemessen | offen (51.10) |

### 51.9 Lesart des steuernden Chats zu R60 (a) (51.5) — Reichweite der Voraussetzung

⚠️ **Vorläufig, bis Fable bestätigt** (Bauart 46.9).

R60 (a) setzt voraus, dass `research/exposure_messung/` nicht zum Laufbereich gehört. Für den Ordner trifft das nicht zu: `bot_lauf.py` steht in der Pfadliste (51.8). Die zwei Stellen, die die Grösse zum Einstand bilden (`exposure_kern.py` und `research/exposure_messung/auswertung.py`, 50.1), stehen nicht darin. `bot_lauf.py` selbst nennt in seinem Docstring (Z. 21–22) als Bedarf einer Exposure-Messung je Zeitpunkt die offenen „Positionen samt gebundenem Kapital“; ob es damit die Grösse im Sinn von R60 (a) bildet, ist nicht gemessen und geht mit an Fable. Dieser Eintrag liest R60 (a) für die Stellen, die die Grösse bilden, nicht für den Ordner: Die Bewertung zum Einstand in diesen zwei Dateien legt keine Definition fest; es gilt R48 (d). Das ist eine Lesart des steuernden Chats; sie geht mit der nächsten Anfrage an Fable. Mit ihr geht die Frage zu R60 (b) und (c): „über die Tage der Falte“ sagt nicht, ob die Tage der Tagesreihe oder die gemeinsamen Tage mit dem Benchmark gemeint sind; `beta_bereinigung` schneidet auf die gemeinsamen Tage, und ob das alle Handelstage des Zeitraums nach R48 (d) sind, ist nicht gemessen (51.8).

### 51.10 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R56 (d): die Dateien der Projekt-Erinnerung, die die Plattform einem Chat des Verfahrensprüfers lädt (01a nennt `preferences.md` und `ways-of-working.md`), auf Grössen nach 27.1 messen und im Eröffnungstext nennen | steuernder Chat, vor der nächsten Eröffnung eines Fable-Chats |
| 2 | R56 (e): Tatsachennotiz, die die Protokollkette schliesst (je Chat seit R32 Eröffnungstext und Antwortdateien mit md5 und Commit); darin die Fassung des Eröffnungstextes vom 01.10.2026 | vor dem signierten Tag |
| 3 | R59 (b): Einträge für feste Fenster in `registerdaten.py`, je mit Probe gegen die Konstante und Gegenprobe | Umsetzungsauftrag mit Einzelfreigabe des Betreibers (26.6, 32.5 (a)) |
| 4 | R59 (c), (d) und R57: Probe der Formel je Bot gegen den Signalpfad; Feld im Faltenplan; Herleitung des Vorlaufs für die übrigen sieben Bots | mit R53 (a) (50.7 Nr. 4) |
| 5 | R60 (c): beide Träger aus einer Rechnung, Probe in der Abnahme nach R46 | mit dem Zellen-Erzeuger |
| 6 | R60 (a), (b) und (c): die Lesart 51.9; die Tage in (b) (gemeinsame Tage mit dem Benchmark gegen „Handelstage des Zeitraums“, nicht gemessen) und in (c) | nächste Anfrage an Fable; die Messung zu (b) vor dem Tag |
| 7 | Orte, die R61 (b) nicht aufzählt und die deshalb keine Marke tragen: 47.9 und 47.13 (R61 (c): „14“ lies „Sperrlistenpunkt 14“), 25.2 (R62 (a)), 50.1 (R60 (d)), 50.4 (R57: Schlusssatz bestätigt). Sie stehen als Indexzeilen in `REGISTER_INDEX.md` | nächste Anfrage an Fable |
| 8 | R62 (b): das Literal `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py`, Probe oder Auflösung | Handwerk (50.7 Nr. 6) |
````

**A4. Einsetzen.** Eine Vorlage (`a4_vorlage_51.md`) und ein Einsetzskript (`a4_eintrag.py`) in der Bauart von `docs/belege/TB-126/a5_vorlage_47_50.md` und `a5_eintrag.py`. Quelle, Kopf, Schluss und den Daten-Block aus Anhang A liest das Skript aus dem Commit ⟨S0⟩ (`git show ⟨S0⟩:<pfad>`), nicht aus dem Gedächtnis. **Zuerst ein Probelauf gegen eine Kopie; an der Kopie laufen die Textprüfungen aus A5.** Erst wenn sie grün sind, einmal echt; danach muss das Register `cmp`-gleich mit der Kopie sein. Sonde, `registerbericht.py --pruefen`, `herkunft.register()` und `test_vorregistrierung` lesen das Register am festen Pfad und laufen deshalb am echten Arbeitsbaum, **vor** dem Commit. **Wachen im Skript:** Eingangszeilenzahl 11 094 · jede alte Zeile steht in derselben Reihenfolge im neuen Text · keine neue Zeile zwischen `## 9.` und `## 11.` · keine neue Zeile im ERZEUGT-Block · `## 51.` ist noch nicht vergeben.

**A5. Nachweis** (je ein Skript unter `docs/belege/TB-129/`, unabhängig vom Einsetzskript; Bauart `docs/belege/TB-126/a6_*`):
- R-Diff: liest Quelle und Register getrennt und vergleicht jeden der sieben Blöcke mit `diff` ⇒ **7/7 rc 0**. Mutationsprobe an einer **Kopie** des Registers (ein Wort in einem Block geändert) ⇒ rc 1.
- Zitate: Kopf und Schluss aus **diesem Auftrag** (am Commit ⟨S0⟩; ⟨S0⟩ und ⟨DATUM⟩ ersetzt) gegen das Register ⇒ 2/2 rc 0.
- Überschriften und Ketten gegen Anhang A ⇒ 7/7 gleich. Marken: 14/14 gesetzt gegen Anhang A, je Marke die Zeile nachher.
- `git diff --numstat` des Registers ⇒ zweite Spalte **0**.
- Abschnitt 10 und ERZEUGT-Block nachher gegen `0b_*_vorher.txt` ⇒ **bytegleich** (die Zeilennummern dürfen wandern).
- `registerbericht.py --pruefen` nachher = vorher (rc und Ausgabe).
- Sonde: sha256 des JSON-Berichts ohne `zeilen` nachher = vorher; (ii) 0; „Listentext wie bei Erzeugung: ja“.
- `herkunft.register()` nachher: ≠ vorher, `fehlend []`, 23 Teile. Der neue Wert steht **nur im Ergebnis**, nie im Register (Selbstbezug, 42.5).
- **`test_vorregistrierung`** am echten Register, ohne Zeitgrenze ⇒ 196/196.

Ist ein Nachweis am echten Register rot: den Diff als `docs/belege/TB-129/abbruch_register.diff` sichern, das Register mit `git checkout -- docs/VORREGISTRIERUNG_neuselektion.md` auf ⟨S0⟩ zurücksetzen, Abbruch. **Das Register wird nur committet, wenn alle Nachweise grün sind.**

Commit `TB-129 A: Register 51 (R56–R62 zeichengleich, Tatsachennotizen 01a), Marken`, pushen. **Das ist der einzige Commit, der das Register ändert.**

## Schritt B — BACKLOG (5b)

Verfahren wie TB-128 (Vorlage `docs/belege/TB-128/einfuegen.py`): Anker vorher zählen (Python `str.count`, Soll genau 1; sonst nicht ausführen, vermerken, weitermachen), Text aus **diesem Auftrag** lesen, einfügen, erste Textzeile nachher zählen (Soll 1) ⇒ `b_einfuegung.txt`; `git diff --numstat` der Datei ⇒ zweite Spalte 0; Zeichengleichheit als Bytevergleich des Blocks (Vorlage `docs/belege/TB-128/c3_vergleich.py`).

#### E1 — Abschnitt 5: Bewertung von Fable 01a (5b) und ein Befund aus der Übernahme

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile** (genau eine Leerzeile davor und danach; eine vorhandene wird nicht verdoppelt)

```
### Aus Fable 01a (01.10.2026) — Bewertung nach 5b, eingetragen mit TB-129

- **Bewertung:** Die Antwort trägt; keine Zahl und kein Zitat ist falsch (gemessen am 02.10.2026, `UEBERGABE.md`, Nachtrag 02.10.2026, 07:46). R56–R62 stehen seit TB-129 im Register, Abschnitt 51; die Voraussetzungen mit Befund in 51.8, was offen bleibt in 51.10.
- **An Fable (02.10.a, neuer Fable-Chat):** R60 (a) — die Voraussetzung trifft für den Ordner `research/exposure_messung/` nicht (`bot_lauf.py` steht im Laufbereich), Lesart 51.9; R60 (b) und (c) — über welche Tage gemittelt wird (`beta_bereinigung` nimmt die gemeinsamen Tage mit dem Benchmark; gegen „Handelstage des Zeitraums“ in R48 (d) nicht gemessen); Marken an 47.9, 47.13, 25.2, 50.1 und 50.4, die R61 (b) nicht aufzählt.
- **R56 (d), Pflicht des steuernden Chats:** vor jeder Eröffnung eines Fable-Chats die Dateien der Projekt-Erinnerung, die die Plattform lädt (01a nennt `preferences.md` und `ways-of-working.md`), gegen 27.1 messen und im Eröffnungstext nennen.
- **R56 (e):** vor dem Tag eine Tatsachennotiz über alle Fable-Chats seit R32 (Eröffnungstext, Antwortdateien, md5, Commit); darin die Fassung des Eröffnungstextes vom 01.10.2026: Fassung 2 (Angabe des Betreibers per Karte, 02.10.2026).
- **R59 (b):** Einträge für feste Fenster in `registerdaten.py`, je mit Probe gegen die Konstante des Bot-Codes und Gegenprobe. Umsetzungsauftrag mit Einzelfreigabe (Registeränderung nach 26.6, 32.5 (a)). Bestand: `bollinger_fenster` (20.0) steht dort schon; ob mit Probe, ist nicht gemessen.
- **R59 (c), (d), R57:** Probe der Vorlauf-Formel je Bot gegen den Signalpfad; Feld im Faltenplan; Herleitung für die übrigen sieben Bots. Mit R53 (a).
- **R60 (c):** Der Zellen-Erzeuger schreibt `mittlere_exposure` in `zellen.csv` und die Spalte `exposure` der Tagesreihe aus einer Rechnung; die Abnahme nach R46 prüft die Gleichheit mit Gegenprobe.
- **R62 (b):** `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py` ist ein vierter Ort des Datenstands; Probe oder Auflösung. Handwerk.
- **Fehler Nr. 17 (steuernder Chat, 01.10.2026):** Der Registerblock von 01a reicht bis R62; gezählt wurde nach „Kurz“, das R62 nicht nennt. Regel für ARBEITSWEISE 0 (nächster Dokumentationsauftrag): Nummern am Block zählen, nicht an der Kurzfassung.
- **01a, „Unsicher“ 6 (Zählung):** Der Satz in 25.2 und die „14“ in R26/R30 sind Ungenauigkeiten aus Fable-Texten, berichtigt durch R62 (a) und R61 (c). Sie zählen nicht in die Fehlerliste des steuernden Chats (Vorgabe des steuernden Chats, 02.10.2026).

### Aus der Übernahme 02.10.2026

- **`docs/werkzeuge/ampel.py`:** bricht mit `TypeError` ab, wenn ein Protokollschritt `null` in `cache_read_input_tokens` oder `cache_creation_input_tokens` trägt, und nähme sonst einen Schritt mit Grösse 0 als Grundlast (gemessen am 02.10.2026, 08:40, im Protokoll des steuernden Chats: drei Schritte eines anderen Modells mit Nutzung 0 vor dem ersten eigenen Schritt). Nachziehen: `null` als 0 lesen, Schritte mit Grösse 0 nicht zählen. Handwerk.
```

Soll numstat: `17	0` (16 Zeilen des Blocks und eine Leerzeile danach).

## Schritt C — Registerkopie, Index, Dialog-Index

**C1. Registerkopie.** Nach dem Commit aus A, am sauberen Stand (das Skript bricht mit 2 ab, wenn das Register im Arbeitsbaum vom HEAD abweicht; `docs/werkzeuge/registerkopie.py`, Docstring Z. 18–19). Fünf Aufrufe, Ausgabe und rc je in eine Datei `c1_*.txt`: `registerkopie.py` · `registerkopie.py --pruefen` · `registerkopie.py --marken` · `registerkopie.py --abschnitte` · `registerkopie.py --abschnitte --pruefen`. Soll nach dem Docstring (Z. 23–37, 54–59): rc 0 je Aufruf; 52 Abschnittsdateien `REGISTER_KOPIE_ABSCHNITT_00.md` bis `_51.md` unter `docs/projektfuehrung/register_kopie/`. Meldet das Skript eine Datei als VERALTET: nicht löschen, im Ergebnis nennen. Ein Schreiblauf mit rc 2 oder 3 oder `--pruefen` mit rc ≠ 0 ⇒ Ausgabe festhalten, die Kopien nicht committen, melden (kein Abbruch). Wie die Ausgaben genau aussehen, ist vom Werkzeug abhängig; im Ergebnis beschreiben.

**C2. `docs/projektfuehrung/REGISTER_INDEX.md` nachziehen**, nach der Bauart der vorhandenen Zeilen und mit den Skripten aus `docs/belege/TB-126/` als Vorlage (`c2_index_zeilen.py`, `c2_index_eintraege.py`, `c2_index_pruefen.py`):
- Kopf (Z. 3–5): Commit des Registers, „Abschnitte 0–51“, Zeilenzahl, sha256; „nachgezogen in TB-129“; der Verweis auf die Kopie nennt die Abschnittsdateien.
- „Wie gemessen“ (Z. 7–14): die Zahlen je Art (MARKE, MARKE+, UEBERSCHRIFT) und der Belegpfad neu aus `docs/belege/TB-129/c1_*.txt`.
- Abschnittstabelle: die Zeilenbereiche aller Abschnitte aus den Köpfen der neuen Abschnittsdateien; neue Zeile für 51; die Zuordnung der Abschnitte zu den Teilen (T, Index Z. 72) neu aus `c1`.
- Alle Zeilenangaben „Z. n“ vom Stand `db108a6` auf den neuen Stand umschreiben (Abbildung über die unveränderten alten Zeilen, wie TB-126 C2); Spalte T neu aus `c1`.
- Tabelle 4 („Registertexte ab Abschnitt 18“): eine Zeile „51 aus 01a“ (R56–R62 = 51.1–51.7; 51.8 Voraussetzungen; 51.9 Lesart, vorläufig; 51.10 Offenes). In den Zeilen und Ketten der Orte, die jetzt eine Marke tragen, den Verweis ergänzen: in den Index-Tabellen 1–3 für die Marken in den Registerabschnitten 1, 4, 7, 8 und 16, in Tabelle 4 für 25, 27, 43, 48, 49 und 50.
- Neuer Abschnitt `## 6. Die Marken aus Fable 01a (TB-129)` in der Form des Abschnitts 5 des Index, mit den 14 Marken und ihren Zeilen nachher; er steht nach der Tabelle von Abschnitt 5, vor der Trennlinie `---` und dem Pflegeblock.
- Pflegezeile am Ende ergänzen.

**C3. Indexzeilen statt Marken** — ein eigener Block `### Indexzeilen aus Fable 01a` im neuen Abschnitt 6, mit genau diesen sechs Zeilen (zeichengleich):

```
- **Tag-Vorbedingungen** (Fable 01a, Frage 7, empfohlen): R15 (b) (46.6) · R27 (47.10) · R29 (47.12) · R30 (47.13).
- **47.9 (R26):** „14“ lies „Sperrlistenpunkt 14 (Abschnitt 10)“ → R61 (c) (51.6). Ohne Marke; an Fable (51.10 Nr. 7).
- **47.13 (R30):** „Ergänzung zu 14“ lies „Ergänzung zu Sperrlistenpunkt 14 (Abschnitt 10)“ → R61 (c) (51.6). Ohne Marke; an Fable (51.10 Nr. 7).
- **25.2:** „der 150. Balken liegt am 2018-01-14“ → Tatsachennotiz R62 (a) (51.7). Ohne Marke; an Fable (51.10 Nr. 7).
- **50.1, Zeile R48 (d):** ergänzt durch R60 (d) (51.5) und 51.8. Ohne Marke; an Fable (51.10 Nr. 7).
- **50.4, Schlusssatz:** bestätigt durch R57 (51.2). Ohne Marke; an Fable (51.10 Nr. 7).
```

**C4. Dialog-Index.** Die Datei `docs/belege/TB-129/c4_handfelder.json` mit genau diesem Inhalt anlegen:

```
{"01a": {"frage": "Darf der Anfangsbestand eines neu begonnenen Fable-Chats über Eröffnungstext und Leseprotokoll festgehalten werden, und wie sind Vorlauf, mittlere Exposure, R53 ohne Rückfall und die Marken nach E-2 zu lesen?", "entscheidung": "Ja, mit Bindung (R56); der Vorlauf ist der hergeleitete Index, nicht die Summe (R57); 26.2 und R53 stehen nebeneinander (R58); kein Rückfall auf ein Literal, Einträge brauchen Freigabe und Probe (R59); mittlere Exposure mit zwei Trägern aus einer Rechnung (R60); sieben Marken nachtragen (R61); Tatsachennotizen (R62).", "offen": "ja"}}
```

Dann `trading-env/bin/python3 docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-129/c4_handfelder.json`, danach `--pruefen` ⇒ `c4_dialog_index.txt` (rc je Aufruf). Soll nach dem Docstring (`docs/werkzeuge/dialog_index.py`, Z. 6–30): `--pruefen` rc 0; eine Zeile `01a` mit Fundstelle 51 und Status „offen“ (offen = ja nach dem Kriterium des Docstrings Z. 14–15: die Messbitte zu R60 (a) ist mit Abweichung beantwortet, die zu R60 (b) nicht vollständig gemessen, und keine spätere Anfrage führt sie als beantwortet); 51 Antworten. `git diff --numstat` der Datei festhalten; ändern sich weitere Zeilen, im Ergebnis nennen (kein Abbruch).

Commit `TB-129 B/C: BACKLOG, Registerkopie, Index, Dialog-Index`, pushen.

## Schritt D — Abgabe

**D1.** `docs/ERGEBNIS_TB-129_register_fable_01a.md`: Kopfzeile mit dem Inhalt in einem Satz (numstat, Zahl der Marken, Zahl der Abschnittsdateien); Sitzungstitel, Stand, Auftrag, Belege; Eingang und alle Commits; Quelle mit md5 „geprüft“; Freigabe; „Kein Abbruchkriterium ausgelöst“ oder der Grund · Kurz-Tabelle je Schritt (Soll | Ist) · Markentabelle: die 14 Marken mit ihrer Zeile nachher · `herkunft.register()` vorher und nachher · **Für Fable** (nur Verfahrensfragen): 51.9 und 51.10 Nr. 6 und 7, dazu jede Reibung zwischen Fable-Text und Register, die beim Setzen auffiel · **Nicht getan:** 51.10; die Ablage (macht der steuernde Chat, nach der 27.4-Prüfung) · **In einfacher Sprache.**

**D2. Journal:** Block ans Ende der Buchstabenblöcke von `docs/projektfuehrung/JOURNAL.md` (nach dem letzten Buchstabenblock, vor `## Wiederkehrende Lehren`). Die Kennung vorher messen (erwartet **EA**), mit Quellenzeile auf das Ergebnis.

**D3.** Abgabe-Commit `TB-129 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-129/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab; ein Ausgangswert aus 0b mit Soll weicht ab; der Basislauf in 0c (falls nötig) ist nicht 196/196.
- 0d: Nr. 1, 2, 3 oder 4 weicht ab (auch eine einzelne Marke).
- Ein Nachweis aus A5 ist rot — jeder der dort genannten, auch Überschriften und Ketten, `fehlend []`, 23 Teile und der `cmp` mit der Kopie aus A4. Im Einzelnen:
- Ein R-Block-diff rc ≠ 0; ein Zitat-diff rc ≠ 0; die Mutationsprobe gibt nicht rc 1.
- numstat des Registers mit zweiter Spalte ≠ 0; eine alte Zeile fehlt oder steht in anderer Reihenfolge.
- Abschnitt 10 oder ERZEUGT-Block nicht bytegleich; `registerbericht.py --pruefen` nachher ≠ vorher; Sonde: JSON ohne `zeilen` ≠ vorher oder (ii) ≠ 0.
- `test_vorregistrierung` nach dem Einsetzen nicht 196/196.
- Eine Datei ausserhalb der Freigabetabelle müsste geändert werden.
- `git push` scheitert zweimal.

**Kein Abbruch:** der BACKLOG-Anker ≠ 1 (nicht einfügen, nennen) · ein Schreiblauf von `registerkopie.py` mit rc 2 oder 3 oder `--pruefen` mit rc ≠ 0 (Kopien nicht committen, nennen; C2 und C3 entfallen dann und werden genannt, C4 nicht) · weitere geänderte Zeilen im Dialog-Index (nennen) · eine Reibung zwischen Fable-Text und Code oder Register (unter „Für Fable“ nennen).

**Bei Abbruch:** committen, was an Belegen da ist, **nie** `JOURNAL.md` mit Platzhalter, Grund in `docs/belege/TB-129/abbruch.txt`, pushen, melden. Kein Registertext mit einem Befund, den dieser Auftrag nicht vorsieht.

## In einfacher Sprache

Fable hat am 01.10. sieben Regeltexte geschrieben (R56–R62). Diese Sitzung kopiert sie per Skript ins Register, Zeichen für Zeichen, als neuen Abschnitt 51, und setzt an 14 alten Stellen kleine Hinweise auf die neuen Texte. Dazu kommt eine Tabelle mit dem, was der steuernde Chat im Code und in den Daten nachgemessen hat. Eine Stelle passt nicht ganz zu Fables Annahme, eine zweite ist noch nicht fertig gemessen; beide stehen offen da und gehen als Frage zurück an Fable. Danach wird die Kopie des Registers für Fable neu erzeugt. Am Code ändert sich nichts. Maschinell geprüft wird, dass jeder Text genau so angekommen ist und kein alter Satz verändert wurde.

---

## Anhang A — TB-129: Überschriften, Ketten, Marken und Fundstellen (Vorlage für die Mac-Sitzung)

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `db108a6` (11 094 Zeilen, sha256 `b5804659…`), HEAD `560ca75`. Gebaut vom steuernden Chat am 02.10.2026 mit einem Skript, das Ankerzeilen und Zeilenanfänge am Register misst. **Alle Zeilennummern gelten am Original, vor jeder Einfügung.** Einsetzen deshalb von unten nach oben. **Massgeblich für Skripte ist der JSON-Block am Ende.**

### Tabelle 1 — Überschriften und Ketten (7)

| x.n | Überschriftzeile (exakt) | Kette (exakt) |
|---|---|---|
| 51.1 | `### 51.1 R56 — Ergänzung zu 27.4 und 27.6 (Anfangsbestand eines neu begonnenen Chats des Verfahrensprüfers)` | `**Kette:** Marken: Abschnitt 27. Voraussetzung gemessen: 51.8.` |
| 51.2 | `### 51.2 R57 — Präzisierung zu R53 (49.1) und Bestätigung von 50.5 (Zählweise des Vorlaufs)` | `**Kette:** Marken: 49.1 (R53); 50.5. Voraussetzung gemessen: 51.8.` |
| 51.3 | `### 51.3 R58 — Tatsachennotiz zu 25.3 (i) (Verhältnis der Marken 26.2 und R53)` | `**Kette:** Marken: 25.3, Ersatztext.` |
| 51.4 | `### 51.4 R59 — Ergänzung zu R53 (49.1) (kein Rückfall auf ein Literal; Eingaben der Rechnung)` | `**Kette:** Marken: 49.1 (R53). Bestand gemessen: 51.8.` |
| 51.5 | `### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) (mittlere Exposure: Registertext und Code; zwei Träger)` | `**Kette:** Marken: 4.2; 48.16 (R48). Voraussetzung gemessen: 51.8. Lesart, vorläufig: 51.9. Offen: 51.10 Nr. 6.` |
| 51.6 | `### 51.6 R61 — Marken nach E-2 (Regel, Nachtrag, eine Berichtigung)` | `**Kette:** Marken, nachgetragen nach (b): 1, Tabelle, Zeile 3; 4.2; 7, Tabelle, Zeile (b); 8, Tabelle (R36 und R55); 16.4, „Prüfung vor dem Tag“; 43.2, Eintrag 43-7. Voraussetzung gemessen: 51.8. Orte ohne Marke: 51.10 Nr. 7.` |
| 51.7 | `### 51.7 R62 — Tatsachennotizen 01a` | `**Kette:** Marken: keine. Voraussetzung gemessen: 51.8.` |

### Tabelle 2 — Marken (14)

Sortiert nach Einfügestelle, an derselben Stelle nach R aufsteigend. Jede Marke: Leerzeile, Markenzeile 1, Markenzeile 2 `> Eintrag und Stand oben bleiben zeichengleich.` „Zahl“ = `str.count` des Ankers über den ganzen Registertext. In Ankern steht `\|` für `|` (Tabellensyntax); Anker mit Backtick stehen in doppelten Backticks mit je einem Leerzeichen innen.

| Nr | Ziel laut Fable (R61 (b), wörtlich) | Registerstelle | Anker (Ankerzeile) | Zahl | Einfügestelle | Markenzeile 1 (exakt) |
|---|---|---|---|---|---|---|
| 1 | Abschnitt 1, Tabelle, Zeile 3 — PRÄZISIERT durch R36 (48.4) | 1, Tabelle, Zeile 3 | `\| 3 \| Beurteilung \| Netto-Calmar,` (Z. 61) | 1 | nach Zeile 81: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **Festlegung 3 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 2 | 4.2 — PRÄZISIERT durch R48 (48.16), Unterpunkte (d) und (e), und durch R60 | 4.2 | `` ### 4.2 Warum `DD_Benchmark` und `DD_Toleranz` `` (Z. 481) | 1 | nach Zeile 517: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **4.2 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkte (d) und (e), nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 3 | 4.2 — … und durch R60 | 4.2 | `` ### 4.2 Warum `DD_Benchmark` und `DD_Toleranz` `` (Z. 481) | 1 | nach Zeile 517: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **4.2 PRÄZISIERT durch R60 (51.5)** (Fable 01a R60, TB-129, ⟨DATUM⟩).` |
| 4 | Abschnitt 7, Tabelle, Zeile (b) — PRÄZISIERT durch R37 (48.5) | 7, Tabelle, Zeile (b) | `\| **(b)** \| **Kein** Parametersatz` (Z. 794) | 1 | nach Zeile 805: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **7 (b) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 5 | Abschnitt 8, Tabelle — PRÄZISIERT durch R36 (48.4) | 8, Tabelle | `\| Mittelwert der **drei tiefsten** Falten-Drawdowns \|` (Z. 864) | 1 | nach Zeile 873: `\| Bestätigungsperiode: Sharpe, Rendite, ` | `> ⭐ **8, Tabelle PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 6 | Abschnitt 8, Tabelle — ERGÄNZT durch R55 (49.3) | 8, Tabelle | `\| Mittelwert der **drei tiefsten** Falten-Drawdowns \|` (Z. 864) | 1 | nach Zeile 873: `\| Bestätigungsperiode: Sharpe, Rendite, ` | `> ⭐ **8, Tabelle ERGÄNZT durch R55 (49.3)** (Fable 30a R55, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 7 | 16.4, „Prüfung vor dem Tag“ — PRÄZISIERT durch R21 (47.4) | 16.4, „Prüfung vor dem Tag“ | `#### Prüfung vor dem Tag` (Z. 2200) | 1 | nach Zeile 2212: `> zeichengleich.` | `> ⭐ **16.4, „Prüfung vor dem Tag“ PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 8 | 25.3 — ERGÄNZT durch R58 | 25.3, Ersatztext | `### 25.3 Der Ersatztext` (Z. 4636) | 1 | nach Zeile 4652: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **25.3 (i) ERGÄNZT durch R58 (51.3)** (Fable 01a R58, TB-129, ⟨DATUM⟩).` |
| 9 | 27 — ERGÄNZT durch R56 | Abschnitt 27 | `## 27. Sichtschutz` (Z. 5094) | 1 | nach Zeile 5164: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **Abschnitt 27 ERGÄNZT durch R56 (51.1)** (Fable 01a R56, zu 27.4 und 27.6, TB-129, ⟨DATUM⟩).` |
| 10 | 43.2, Eintrag 43-7 — PRÄZISIERT durch R33 (48.1) | 43.2, Eintrag 43-7 | `**43-7 — Ergänzung zu 24b A2 / 36.5 — null Trades**` (Z. 9652) | 1 | nach Zeile 9673: `15.3.` | `> ⭐ **43-7 PRÄZISIERT durch R33 (48.1)** (Fable 29b R33, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).` |
| 11 | 48.16 — ERGÄNZT durch R60 | 48.16 (R48) | `### 48.16 R48 — Lesarten zu Register 0–12` (Z. 10834) | 1 | nach Zeile 10851: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **48.16 R48 (d) ERGÄNZT durch R60 (51.5)** (Fable 01a R60, TB-129, ⟨DATUM⟩).` |
| 12 | 49.1 — PRÄZISIERT durch R57 und ERGÄNZT durch R59 | 49.1 (R53) | `### 49.1 R53 — Präzisierung zu 4a (i)` (Z. 10895) | 1 | nach Zeile 10898: `> Quelle des Grundes: 2.7 (ein Raster je` | `> ⭐ **49.1 R53 PRÄZISIERT durch R57 (51.2)** (Fable 01a R57, TB-129, ⟨DATUM⟩).` |
| 13 | 49.1 — … und ERGÄNZT durch R59 | 49.1 (R53) | `### 49.1 R53 — Präzisierung zu 4a (i)` (Z. 10895) | 1 | nach Zeile 10898: `> Quelle des Grundes: 2.7 (ein Raster je` | `> ⭐ **49.1 R53 ERGÄNZT durch R59 (51.4)** (Fable 01a R59, TB-129, ⟨DATUM⟩).` |
| 14 | 50.5 — bestätigt durch R57 | 50.5 | `### 50.5 Lesart des steuernden Chats zu R53 (49.1)` (Z. 11068) | 1 | nach Zeile 11072: `R53 nennt die Regel, nicht die Werte (30` | `> ⭐ **50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt** (Fable 01a R57, TB-129, ⟨DATUM⟩).` |

### Ohne Marke — als Indexzeile (C3) und als Frage an Fable (51.10 Nr. 7)

| Ort | Block | Grund |
|---|---|---|
| 47.9 (R26), 47.13 (R30) | R61 (c) | Berichtigung („lies“); R61 (b) zählt die Orte nicht auf |
| 25.2 | R62 (a) | Tatsachennotiz zu einem Satz in 25.2; nicht aufgezählt |
| 50.1, Zeile R48 (d) | R60 (d) | Ergänzung als Tatsachennotiz (steht in 51.8); nicht aufgezählt |
| 50.4, Schlusssatz | R57 | bestätigt; aufgezählt ist nur 50.5 |

### Prüfsumme

```
Marken: 14 an 11 Einfuegestellen
je Abschnitt: 1: 1, 4: 2, 7: 1, 8: 2, 16: 1, 25: 1, 27: 1, 43: 1, 48: 1, 49: 2, 50: 1
Anker mit Zahl 1 (Original): 14 von 14
Anker mit Zahl 1 (nach Simulation): 14 von 14
Bloecke: 7 | Ueberschriften: 7 max. Laenge 115
Fundstellen: 43 | Zaehlungen: 7 | Kalender: 2 Dateien
Git-Tatsachen: 3 - von der Sitzung mit git zu pruefen
rc 0: alles wie angegeben
```

Prüfskript (liest den JSON-Block unten; Aufruf `python3 pruefe_anhang_tb129.py <dieser Auftrag> <repo-wurzel>`; rc 0 = alles wie angegeben). Die Git-Tatsachen prüft die Sitzung mit `git log` und `git show`.

```python
#!/usr/bin/env python3
"""Prueft Anhang A von TB-129 gegen das Register am Stand db108a6 und die Fundstellen fuer 51.8.

Aufruf:  python3 pruefe_anhang_tb129.py <MAC_TB-129_register_fable_01a.md> <repo-wurzel>
Liest den JSON-Block des Auftrags (zwischen den Zeilen 'DATEN-ANFANG' und 'DATEN-ENDE'), zaehlt jeden
Anker mit str.count ueber den ganzen Registertext, prueft Ankerzeile und Einfuegestelle, schneidet die
Quelle nach der Schnittregel, simuliert das Einsetzen (Marken + angehaengter Abschnitt 51) und zaehlt
erneut; prueft Fundstellen, Zaehlungen und den Kalender. Die Git-Tatsachen prueft die Sitzung mit git.
rc 0 = alles wie angegeben, rc 1 = Abweichung.
"""
import csv, datetime, hashlib, json, re, sys

md, repo = sys.argv[1], sys.argv[2].rstrip("/") + "/"
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
reg = open(repo + daten["register"], encoding="utf-8").read()
L = reg.split("\n")
fehler = []
def f(x): fehler.append(x)

if hashlib.sha256(reg.encode()).hexdigest() != daten["register_sha256"]: f("Register-sha256 weicht ab")
if len(reg.splitlines()) != daten["register_zeilen"]: f("Register-Zeilenzahl weicht ab")
a9 = next(i for i, s in enumerate(L, 1) if s.startswith("## 9."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))
if reg.count("## 51.") != 0: f("## 51. ist schon vergeben")
if any(s.startswith("> R56 — ") for s in L): f("R56 steht schon im Register")

FORM = re.compile(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch .+\*\* \(.+, TB-129, ⟨DATUM⟩\)\.$")
marken = daten["marken"]
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker {m['anker']!r} zaehlt {n}")
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f(f"Nr {m['nr']}: Anker beginnt nicht Zeile {m['ankerzeile']}")
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f(f"Nr {m['nr']}: Zeile {m['nach']} beginnt nicht wie angegeben")
    if a9 <= m["nach"] < a11: f(f"Nr {m['nr']}: Einfuegestelle in Abschnitt 9 oder 10")
    if ea <= m["nach"] < ee: f(f"Nr {m['nr']}: Einfuegestelle im ERZEUGT-Block")
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f(f"Nr {m['nr']}: mitten im Zitat")
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f(f"Nr {m['nr']}: mitten in Tabelle")
    if L[m["nach"]] != "": f(f"Nr {m['nr']}: nach der Einfuegestelle steht keine Leerzeile")
    if not FORM.match(m["m1"]): f(f"Nr {m['nr']}: Markenzeile 1 nicht in der Form")
    if m["m2"] != "> Eintrag und Stand oben bleiben zeichengleich.": f(f"Nr {m['nr']}: Markenzeile 2")
schl = [(m["nach"], m["R"]) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")

# Quelle schneiden
q = daten["quelle"]
qroh = open(repo + q["pfad"], "rb").read()
if hashlib.md5(qroh).hexdigest() != q["md5"]: f("Quelle: md5 weicht ab")
if len(qroh) != q["bytes"]: f("Quelle: Bytes weichen ab")
z = qroh.decode("utf-8").split("\n")
bl, cur = {}, None
for i in range(q["von"], q["bis"] + 1):
    s = z[i - 1]
    mm = re.match(r"^R(\d+) — ", s)
    if mm: cur = int(mm.group(1)); bl[cur] = [s]; continue
    if cur is not None:
        bl[cur].append(s)
        if s.startswith("Quelle des Grundes:"): cur = None
if sorted(bl) != list(range(56, 63)): f("Schnitt ergibt nicht R56-R62")
if any(len(v) != 2 or not v[1].endswith("Kein Ergebnis.") for v in bl.values()): f("ein Block hat nicht zwei Zeilen")

# Ueberschriften: Bezug = Anfang des Blocks bis zum ersten Punkt nach dem Bezug
for u in daten["ueberschriften"]:
    kern = u["zeile"].split(" ", 2)[2]                      # "R56 — ..."
    if not bl[u["R"]][0].startswith(kern + "."): f(f"{u['xn']}: Ueberschrift ist nicht der Blockanfang")
    if not u["kette"].startswith("**Kette:** "): f(f"{u['xn']}: Kette nicht in der Form")

# Simulation: Marken von unten nach oben einsetzen, Abschnitt 51 anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"], m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
anhang = ["## 51. Fable 01a — Registerblock R56–R62 (TB-129)", ""]
for u in daten["ueberschriften"]:
    anhang += [u["zeile"], ""] + ["> " + s for s in bl[u["R"]]] + ["", u["kette"], ""]
sim = "\n".join(neu[:-1] + [""] + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker nach Simulation {n}")
zz = [u["zeile"] for u in daten["ueberschriften"]]
if len(set(zz)) != 7 or any(sim.count(x) != 1 for x in zz): f("Ueberschriften nicht eindeutig")
if any(len(x) > 120 for x in zz): f("Ueberschrift laenger als 120 Zeichen")
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")

# Fundstellen, Zaehlungen, Kalender
for d, znr, teil in daten["fundstellen"]:
    zl = open(repo + d, encoding="utf-8").read().split("\n")
    if znr > len(zl) or teil not in zl[znr - 1]: f(f"Fundstelle {d}:{znr} enthaelt nicht {teil!r}")
for d, muster, soll in daten["zaehlungen"]:
    ist = len(re.findall(muster, open(repo + d, encoding="utf-8").read(), re.M))
    if ist != soll: f(f"Zaehlung {d} /{muster}/: {ist} statt {soll}")
k = daten["kalender"]
for d in k["dateien"]:
    tage = [r[0][:10] for r in csv.reader(open(repo + d, encoding="utf-8"))][1:]
    bis = [t for t in tage if t <= "2018-01-31"]
    tag = datetime.date.fromisoformat
    ist = {"erster": tage[0], "balken_bis_2017-12-31": sum(t <= "2017-12-31" for t in tage),
           "index_149": tage[149], "index_150": tage[150],
           "tage_januar_2018": sum("2018-01-01" <= t <= "2018-01-31" for t in tage),
           "luecken_bis_2018-01-31": sum((tag(b) - tag(a)).days != 1 for a, b in zip(bis, bis[1:])),
           "doppelte_bis_2018-01-31": len(bis) - len(set(bis))}
    if ist != k["soll"]: f(f"Kalender {d}: {ist}")

je = {}
for m in marken:
    kk = next(int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1]))
    je[kk] = je.get(kk, 0) + 1
print("Marken:", len(marken), "an", len({m["nach"] for m in marken}), "Einfuegestellen")
print("je Abschnitt:", ", ".join(f"{a}: {v}" for a, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Bloecke:", len(bl), "| Ueberschriften:", len(zz), "max. Laenge", max(len(x) for x in zz))
print("Fundstellen:", len(daten["fundstellen"]), "| Zaehlungen:", len(daten["zaehlungen"]), "| Kalender:", len(k["dateien"]), "Dateien")
print("Git-Tatsachen:", len(daten["git_tatsachen"]), "- von der Sitzung mit git zu pruefen")
if fehler:
    print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
print("rc 0: alles wie angegeben")
```

### Daten (maschinenlesbar, massgeblich für Skripte)

```
DATEN-ANFANG
{
 "stand": "db108a6 (HEAD 560ca75)",
 "register": "docs/VORREGISTRIERUNG_neuselektion.md",
 "register_sha256": "b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1",
 "register_zeilen": 11094,
 "quelle": {
  "pfad": "docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md",
  "md5": "4995260b7af91d2f4c058b1e2c49e788",
  "bytes": 22084,
  "von": 113,
  "bis": 132
 },
 "commit_datum": {
  "eaea530": "2026-10-01",
  "7238842": "2026-10-02"
 },
 "ueberschriften": [
  {
   "xn": "51.1",
   "R": 56,
   "zeile": "### 51.1 R56 — Ergänzung zu 27.4 und 27.6 (Anfangsbestand eines neu begonnenen Chats des Verfahrensprüfers)",
   "kette": "**Kette:** Marken: Abschnitt 27. Voraussetzung gemessen: 51.8."
  },
  {
   "xn": "51.2",
   "R": 57,
   "zeile": "### 51.2 R57 — Präzisierung zu R53 (49.1) und Bestätigung von 50.5 (Zählweise des Vorlaufs)",
   "kette": "**Kette:** Marken: 49.1 (R53); 50.5. Voraussetzung gemessen: 51.8."
  },
  {
   "xn": "51.3",
   "R": 58,
   "zeile": "### 51.3 R58 — Tatsachennotiz zu 25.3 (i) (Verhältnis der Marken 26.2 und R53)",
   "kette": "**Kette:** Marken: 25.3, Ersatztext."
  },
  {
   "xn": "51.4",
   "R": 59,
   "zeile": "### 51.4 R59 — Ergänzung zu R53 (49.1) (kein Rückfall auf ein Literal; Eingaben der Rechnung)",
   "kette": "**Kette:** Marken: 49.1 (R53). Bestand gemessen: 51.8."
  },
  {
   "xn": "51.5",
   "R": 60,
   "zeile": "### 51.5 R60 — Bestätigung und Ergänzung zu R48 (d) (48.16) (mittlere Exposure: Registertext und Code; zwei Träger)",
   "kette": "**Kette:** Marken: 4.2; 48.16 (R48). Voraussetzung gemessen: 51.8. Lesart, vorläufig: 51.9. Offen: 51.10 Nr. 6."
  },
  {
   "xn": "51.6",
   "R": 61,
   "zeile": "### 51.6 R61 — Marken nach E-2 (Regel, Nachtrag, eine Berichtigung)",
   "kette": "**Kette:** Marken, nachgetragen nach (b): 1, Tabelle, Zeile 3; 4.2; 7, Tabelle, Zeile (b); 8, Tabelle (R36 und R55); 16.4, „Prüfung vor dem Tag“; 43.2, Eintrag 43-7. Voraussetzung gemessen: 51.8. Orte ohne Marke: 51.10 Nr. 7."
  },
  {
   "xn": "51.7",
   "R": 62,
   "zeile": "### 51.7 R62 — Tatsachennotizen 01a",
   "kette": "**Kette:** Marken: keine. Voraussetzung gemessen: 51.8."
  }
 ],
 "marken": [
  {
   "nr": 1,
   "R": 36,
   "ziel": "Abschnitt 1, Tabelle, Zeile 3 — PRÄZISIERT durch R36 (48.4)",
   "stelle": "1, Tabelle, Zeile 3",
   "anker": "| 3 | Beurteilung | Netto-Calmar,",
   "ankerzeile": 61,
   "nach": 81,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **Festlegung 3 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 2,
   "R": 48,
   "ziel": "4.2 — PRÄZISIERT durch R48 (48.16), Unterpunkte (d) und (e), und durch R60",
   "stelle": "4.2",
   "anker": "### 4.2 Warum `DD_Benchmark` und `DD_Toleranz`",
   "ankerzeile": 481,
   "nach": 517,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **4.2 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkte (d) und (e), nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 3,
   "R": 60,
   "ziel": "4.2 — … und durch R60",
   "stelle": "4.2",
   "anker": "### 4.2 Warum `DD_Benchmark` und `DD_Toleranz`",
   "ankerzeile": 481,
   "nach": 517,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **4.2 PRÄZISIERT durch R60 (51.5)** (Fable 01a R60, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 4,
   "R": 37,
   "ziel": "Abschnitt 7, Tabelle, Zeile (b) — PRÄZISIERT durch R37 (48.5)",
   "stelle": "7, Tabelle, Zeile (b)",
   "anker": "| **(b)** | **Kein** Parametersatz",
   "ankerzeile": 794,
   "nach": 805,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **7 (b) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 5,
   "R": 36,
   "ziel": "Abschnitt 8, Tabelle — PRÄZISIERT durch R36 (48.4)",
   "stelle": "8, Tabelle",
   "anker": "| Mittelwert der **drei tiefsten** Falten-Drawdowns |",
   "ankerzeile": 864,
   "nach": 873,
   "anfang40": "| Bestätigungsperiode: Sharpe, Rendite, ",
   "m1": "> ⭐ **8, Tabelle PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 6,
   "R": 55,
   "ziel": "Abschnitt 8, Tabelle — ERGÄNZT durch R55 (49.3)",
   "stelle": "8, Tabelle",
   "anker": "| Mittelwert der **drei tiefsten** Falten-Drawdowns |",
   "ankerzeile": 864,
   "nach": 873,
   "anfang40": "| Bestätigungsperiode: Sharpe, Rendite, ",
   "m1": "> ⭐ **8, Tabelle ERGÄNZT durch R55 (49.3)** (Fable 30a R55, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 7,
   "R": 21,
   "ziel": "16.4, „Prüfung vor dem Tag“ — PRÄZISIERT durch R21 (47.4)",
   "stelle": "16.4, „Prüfung vor dem Tag“",
   "anker": "#### Prüfung vor dem Tag",
   "ankerzeile": 2200,
   "nach": 2212,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **16.4, „Prüfung vor dem Tag“ PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 8,
   "R": 58,
   "ziel": "25.3 — ERGÄNZT durch R58",
   "stelle": "25.3, Ersatztext",
   "anker": "### 25.3 Der Ersatztext",
   "ankerzeile": 4636,
   "nach": 4652,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **25.3 (i) ERGÄNZT durch R58 (51.3)** (Fable 01a R58, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 9,
   "R": 56,
   "ziel": "27 — ERGÄNZT durch R56",
   "stelle": "Abschnitt 27",
   "anker": "## 27. Sichtschutz",
   "ankerzeile": 5094,
   "nach": 5164,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **Abschnitt 27 ERGÄNZT durch R56 (51.1)** (Fable 01a R56, zu 27.4 und 27.6, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 10,
   "R": 33,
   "ziel": "43.2, Eintrag 43-7 — PRÄZISIERT durch R33 (48.1)",
   "stelle": "43.2, Eintrag 43-7",
   "anker": "**43-7 — Ergänzung zu 24b A2 / 36.5 — null Trades**",
   "ankerzeile": 9652,
   "nach": 9673,
   "anfang40": "15.3.",
   "m1": "> ⭐ **43-7 PRÄZISIERT durch R33 (48.1)** (Fable 29b R33, nachgetragen nach Fable 01a R61 (b), TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 11,
   "R": 60,
   "ziel": "48.16 — ERGÄNZT durch R60",
   "stelle": "48.16 (R48)",
   "anker": "### 48.16 R48 — Lesarten zu Register 0–12",
   "ankerzeile": 10834,
   "nach": 10851,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **48.16 R48 (d) ERGÄNZT durch R60 (51.5)** (Fable 01a R60, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 12,
   "R": 57,
   "ziel": "49.1 — PRÄZISIERT durch R57 und ERGÄNZT durch R59",
   "stelle": "49.1 (R53)",
   "anker": "### 49.1 R53 — Präzisierung zu 4a (i)",
   "ankerzeile": 10895,
   "nach": 10898,
   "anfang40": "> Quelle des Grundes: 2.7 (ein Raster je",
   "m1": "> ⭐ **49.1 R53 PRÄZISIERT durch R57 (51.2)** (Fable 01a R57, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 13,
   "R": 59,
   "ziel": "49.1 — … und ERGÄNZT durch R59",
   "stelle": "49.1 (R53)",
   "anker": "### 49.1 R53 — Präzisierung zu 4a (i)",
   "ankerzeile": 10895,
   "nach": 10898,
   "anfang40": "> Quelle des Grundes: 2.7 (ein Raster je",
   "m1": "> ⭐ **49.1 R53 ERGÄNZT durch R59 (51.4)** (Fable 01a R59, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 14,
   "R": 57,
   "ziel": "50.5 — bestätigt durch R57",
   "stelle": "50.5",
   "anker": "### 50.5 Lesart des steuernden Chats zu R53 (49.1)",
   "ankerzeile": 11068,
   "nach": 11072,
   "anfang40": "R53 nennt die Regel, nicht die Werte (30",
   "m1": "> ⭐ **50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt** (Fable 01a R57, TB-129, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  }
 ],
 "fundstellen": [
  [
   "strategies/volatility_breakout_crypto/backtest_breakout.py",
   69,
   "BB_PERIOD = 20"
  ],
  [
   "strategies/volatility_breakout_crypto/backtest_breakout.py",
   119,
   "0-basiert, rolling ohne min_periods"
  ],
  [
   "strategies/volatility_breakout_crypto/backtest_breakout.py",
   121,
   "der Einstieg bei i braucht is_squeeze[i - 1]"
  ],
  [
   "strategies/volatility_breakout_crypto/backtest_breakout.py",
   122,
   "also i >= BB_PERIOD + L - 1"
  ],
  [
   "strategies/volatility_breakout_crypto/backtest_breakout.py",
   129,
   "start_i = BB_PERIOD + squeeze_lookback_days - 1"
  ],
  [
   "strategies/volatility_breakout/backtest_breakout.py",
   101,
   "BB_PERIOD = 20"
  ],
  [
   "strategies/volatility_breakout/backtest_breakout.py",
   160,
   "0-basiert, rolling ohne min_periods"
  ],
  [
   "strategies/volatility_breakout/backtest_breakout.py",
   162,
   "der Einstieg bei i braucht is_squeeze[i - 1]"
  ],
  [
   "strategies/volatility_breakout/backtest_breakout.py",
   163,
   "also i >= BB_PERIOD + L - 1"
  ],
  [
   "strategies/volatility_breakout/backtest_breakout.py",
   170,
   "start_i = BB_PERIOD + squeeze_lookback_days - 1"
  ],
  [
   "research/vorregistrierung/faltenplan.py",
   242,
   "beginn = fn.symbolbeginn(bot, horizont)"
  ],
  [
   "research/faltenplan_neun/faltenplan_neun.py",
   301,
   "def balken_datum(pfad: str, nummer: int, anker=None):"
  ],
  [
   "research/faltenplan_neun/faltenplan_neun.py",
   302,
   "Das Datum des `nummer`-ten Balkens (0-basiert) ab `anker`."
  ],
  [
   "research/faltenplan_neun/faltenplan_neun.py",
   402,
   "def warm_ab("
  ],
  [
   "research/faltenplan_neun/faltenplan_neun.py",
   412,
   "return balken_datum(pfad, eig[\"vorlauf_balken\"], anker)"
  ],
  [
   "research/faltenplan_neun/faltenplan_neun.py",
   415,
   "def symbolbeginn("
  ],
  [
   "research/faltenplan_neun/faltenplan_neun.py",
   426,
   "else warm_ab(bot, symbol, anker, basis))"
  ],
  [
   "shared/paths.py",
   239,
   "ARBEITSBAUM_PFADE = ("
  ],
  [
   "shared/paths.py",
   242,
   "\"research/exposure_messung/bot_lauf.py\","
  ],
  [
   "docs/belege/TB-112/a2_laufbereich.txt",
   8,
   "research/exposure_messung/bot_lauf.py\ttrockenlauf"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   21,
   "braucht man je Zeitpunkt die Menge der OFFENEN"
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   22,
   "Positionen samt gebundenem Kapital."
  ],
  [
   "research/exposure_messung/auswertung.py",
   234,
   "\"mittlere_exposure_pct\": round(float((gebunden / kapital_start).mean()) * 100, 2),"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   405,
   "e = float(z[\"mittlere_exposure\"])"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   502,
   "fenster = [(pd.Timestamp(f[\"von\"]), pd.Timestamp(f[\"bis_ausschliesslich\"]))"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   503,
   "for f in plan[bot][\"falten\"] if f[\"name\"] in selektionsfalten]"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   511,
   "return any((d >= a) & (d < b) for a, b in fenster)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   517,
   "gemeinsam = s.index.intersection(b.index)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   523,
   "se = s.loc[gemeinsam, \"exposure\"].to_numpy(dtype=float)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   528,
   "exposure_mittel = float(np.mean(se))"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   537,
   "\"mittlere_exposure\": exposure_mittel,"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   665,
   "bereinigung = beta_bereinigung(bot, wurzel, gew[\"zelle_id\"], plan, sel)"
  ],
  [
   "research/vorregistrierung/registerdaten.py",
   213,
   "if art == \"bollinger_fenster\":"
  ],
  [
   "research/vorregistrierung/registerdaten.py",
   216,
   "return 20.0"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1081,
   "14. **Die Reihenfolge Selektion → Bestätigungsperiode → Bericht** — im"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1082,
   "Kopftext von `auswertung.py` als Ablauf festgeschrieben"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1327,
   "## 14. Der Nulltest S-E1"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10673,
   "(12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun)"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10701,
   "> **R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10840,
   "ist die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md",
   5,
   "## Leseprotokoll dieses Chats (27.4)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md",
   9,
   "die Abschnittsdateien 1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 16, 25, 26, 27, 28, 32, 43, 45, 46, 47, 48, 49, 50;"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md",
   14,
   "Registerabschnitte 0, 2, 10, 13, 15, 17–24, 29–31, 33–42, 44."
  ]
 ],
 "zaehlungen": [
  [
   "shared/paths.py",
   "exposure_messung",
   1
  ],
  [
   "docs/belege/TB-112/a2_laufbereich.txt",
   "exposure_messung",
   1
  ],
  [
   "research/exposure_messung/bot_lauf.py",
   "^\\s*(import|from)\\s+.*exposure_kern",
   0
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "^## 6 — Geparkt, null Arbeit",
   1
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "Aus Fable 01a",
   0
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "Aus der Übernahme 02.10.2026",
   0
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 01a \\|",
   0
  ]
 ],
 "kalender": {
  "dateien": [
   "data/BTCUSDT_1d.csv",
   "data/ETHUSDT_1d.csv"
  ],
  "soll": {
   "erster": "2017-08-17",
   "balken_bis_2017-12-31": 137,
   "index_149": "2018-01-13",
   "index_150": "2018-01-14",
   "tage_januar_2018": 31,
   "luecken_bis_2018-01-31": 0,
   "doppelte_bis_2018-01-31": 0
  }
 },
 "git_tatsachen": [
  {
   "datei": "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md",
   "commits": [
    "7238842",
    "eaea530"
   ],
   "ueberschrift_am": {
    "eaea530": "— Fassung 2 (",
    "7238842": "— Fassung 3 ("
   }
  },
  {
   "datei": "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-01_neuer_chat.md",
   "commits": [
    "7238842"
   ]
  },
  {
   "datei": "docs/projektfuehrung/FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md",
   "commits": [
    "7238842"
   ]
  }
 ]
}
DATEN-ENDE
```
