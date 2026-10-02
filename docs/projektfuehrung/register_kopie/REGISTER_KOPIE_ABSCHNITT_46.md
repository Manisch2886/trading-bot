# REGISTER-KOPIE Abschnitt 46 (von 0–51) — Register-Z. 10356–10640 — Commit f63ad4cbd1230427305a24ac3d7467b83f088fd2 — 2026-10-02 — Original sha256 7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4 — KOPIE, nicht das Register

## 46. Sonde zweiseitig, `fehlend` im Modus, zwei Erzeuger, Snapshot-Bindung, Herkunftsprüfung in `auswertung.py` — die Einträge aus Fable 27a (TB-117, 26.09.2026)

### 46.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **45**
(TB-114). Anlass ist die Tagesanfrage 27a an den Verfahrensprüfer
(`FABLE_ANFRAGE_2026-09-27a_tagesanfrage_tb114_tb115.md`) zu den Ergebnissen **TB-114** (Register 45,
dritte Öffnung von `herkunft.py`, Abbruch in Block C) und **TB-115** (drei
Verfahrensmessungen, nur lesend). Fables Einordnung, zeichengleich:
„**Ein Bündel, eine Freigabekarte je Sperrlistendatei** (`herkunft.py`, `auswertung.py`, Sonde), dann ein Abbild."

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

> **R9 — Ergänzung zu 40.8 (e) (Sonde, zweite Seite).** Die Sonde prüft die Gruppe `eingefroren` aus dem Abbild heraus (Abbild → Dateien) **und** vergleicht die heutige Menge `herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds (Liste → Abbild). Ein Eintrag, der in einer der beiden Mengen fehlt, ist ein Befund ⇒ 1, mit Nennung des Eintrags und der Seite. Die Gruppen kommen weiter aus dem Abbild; neu ist nur der Vergleich der Mengen.
> *Quelle des Grundes:* Prüfprinzip C4 (eine Prüfung, die nicht sagt, gegen was sie prüft; zweiseitiger Nachweis), Messung TB-114 Block C. Kein Ergebnis.

**Kette:** ergänzt **40.8 (e)** (die Sonde liest die Gruppen aus dem Abbild);
beantwortet T114-2 (Fable 27a Abschnitt 2). Marke in 40.8 als eigene
Tabellenzeile direkt unter der Zeile (e). **Fables erstes „Unsicher",
zeichengleich:**
„Ob `sperrlistensonde.py` selbst im Abbild oder auf der Sperrliste steht — wenn ja, folgt der Sonden-Öffnung ein Abbild nach 37.3; wenn nein, nicht. Nicht gemessen."
**Gemessen (TB-117, am Stand `753ec11`, nur lesend):** Der Listentext von
Abschnitt 10 nennt `sperrlistensonde` 0-mal; das Abbild `5e5ad109…` nennt die
Sonde einmal, und zwar nur als Parser im Feld `erzeugt`
(`"parser": "shared/sperrlistensonde.py::lies_abschnitt_10"`), in keinem
Punkt und in keiner Gruppe. Das neue Abbild nach dem Bündel folgt trotzdem, weil
`herkunft.py` und `auswertung.py` geöffnet werden (R11). Vollzug in TB-117
Block B (46.11).

### 46.2 R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`)

> **R10 — Ergänzung zu 41.1 A10 (`herkunft.py`, `fehlend`).** `register()` und `block()` enden unter dem Modus mit 2, wenn `fehlend` nicht leer ist; die Meldung nennt die fehlenden Einträge. Ohne Modus bleibt `fehlend` ein Feld und eine Druckzeile der Prüfansicht. Die neun TB-24-Listen werden nicht in `ARBEITSBAUM_PFADE` aufgenommen (R3: die Sauberkeitsprüfung bindet Code); eine fehlende Liste wird über `register()` ⇒ 2, die Sonde (Gruppe `eingefroren`) und den Abbruch in `faltenplan.py` sichtbar. Umsetzung mit der nächsten Öffnung von `herkunft.py`, zusammen mit dem Nachtrag im Modulkopf (R17 a).
> *Quelle des Grundes:* 24b A2 (ein Wert, der so tut, als wäre er gemessen), 41.1 A10. Kein Ergebnis.

**Kette:** ergänzt **41.1 A10** (kein Fallback unter dem Modus); beantwortet
T114-1. Marke unter dem „Stand, gemessen" von A10. Der Nachtrag im Modulkopf
(R17 (a), 46.8) gehört zu derselben Öffnung. Vollzug in TB-117 Block C
(46.11).

### 46.3 R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen)

> **R12 — Tatsachennotiz zu 40.6 / 41.1 A12 / 45.3 (zwei Erzeuger; Bindung der Listen).** Es gibt zwei Erzeuger: den **Listen-Erzeuger** auf dem Signalpfad (40.6, 41.1 A12; heute `research/tb24_haltedauern/positionen_holen.py`, `--ziel`, Einmal-Schreibsperre), der die Trade-Listen vor dem Tag einmal auf dem Snapshot neu erzeugt, und den **Zellen-Erzeuger** (Plan-Punkt 10, R5), der `zellen.csv`, `tagesreihen/` und `herkunft.json` schreibt. `herkunft.py::EINGEFROREN` bindet die neun heutigen Listen unter `research/tb24_haltedauern/daten/`, bis die Listen nach 40.6 neu erzeugt sind und `faltenplan.py` sie über die registrierte Pfadkonstante liest; dann treten die neuen Listen an ihre Stelle, die alten bleiben als historischer Stand liegen und verlassen `EINGEFROREN` (gebunden wird, was gelesen wird, R3); ihre Hashes stehen in `docs/belege/TB-114/`. Die Öffnung von `herkunft.py` dafür erfolgt mit der Neuerzeugung, nicht davor. Der Pfad der neuen Listen ist bis dahin nicht registriert (TB-114 B3).
> *Quelle des Grundes:* 40.6, 41.1 A12, R3, R5. Kein Ergebnis.

**Kette:** Tatsachennotiz zu **40.6**, **41.1 A12** und **45.3**; beantwortet
T114-3 und berichtigt die Lesart der Anfrage („folgt dann dem Pfad des
Erzeugers (R5)" — gemeint ist 40.6). Marken am Ende von 40.6, unter der
TB-114-Marke von 41.1 A12 und am Ende von 45.3. ⛔ **Nicht vollzogen und nicht
Teil von TB-117:** Die Listen werden nicht neu erzeugt, `EINGEFROREN` behält
die neun heutigen Listen.

> ⭐ **46.3 ERGÄNZT durch R39 (48.7)** (Fable 29b R39, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **46.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 46.4 R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4)

> **R13 — Tatsachennotizen zum Snapshot und zu den Eingaben (neben 5e, 28, 31; Punkt 10; 16.4).**
> (a) `XAUTUSDT_1h.csv` im Datenstand `d9449faf…` endet auf einer Teilkerze (letzte Kerze `2026-08-30 18:00`, geschrieben 18:39:01 UTC, 21 min vor Kerzenschluss). Kein Lauf liest sie, weil vier Ausschlussmengen das Symbol streichen: `shared/symbols_config.py::EXCLUDE_SYMBOLS`, `messgroessen.py::AUSGESCHLOSSEN`, `faltenplan_neun.py::KRYPTO_AUSSCHLUSS`, `benchmark.py:145`. Wache: eine Probe liest die vier Mengen ein und verlangt Gleichheit (Handwerk, keine Sperrlistennähe). Zusammenlegung auf einen Ort mit der jeweils nächsten planmässigen Öffnung, nicht vor dem Tag.
> (b) 175 Dateien des Datenstands (150 Aktien-1d, 25 Krypto-1h) haben keinen feineren Zeugen für `rand_letzte`; ihr Rand ist durch Schreibpfad und Zeitstempel belegt (TB-115 M1: Aktien letzte Kerze `2026-09-01`, geschrieben 02.09. 04:20–04:22 UTC; Krypto gemeinsamer Stand 15.09. 09:00–09:59 UTC). Der Beleg gilt als Tag-Vorbedingung erfüllt; keine laufende Prüfung eingefrorener Daten.
> (c) Adjustierungsstand der 150 Aktienreihen: split- und dividendenbereinigt, rückwärts, Schnitt je Symbol am letzten Ex-Tag vor dem 02.09.2026 (`yf.download(…, auto_adjust=True)`, kein `Adj Close`); Abrufcode nicht versioniert, nächstliegend `0f6491b`; yfinance-Fassung nicht belegbar; keine Regel eines Aktien-Bots nutzt ein absolutes Preisniveau (P1 = 0 Fundstellen, TB-115 M2 (c)). Schliesst die Verfahrensmessung D3 aus R7.
> (d) Stufe 3 der Zuteilungskaskade (`shared/zuteilung.py`, Punkt 10) reiht nach dem Median von `close × volume` über 20 Tage über Symbole hinweg; `volume` ist split-bereinigt, `close` split- und dividendenbereinigt — das Dollar-Volumen eines Dividendenzahlers ist in der Vergangenheit um das Produkt seiner späteren Ausschüttungen zu klein ausgewiesen. Stufe 3 entscheidet bei `volatility_breakout`, `elliott_wave_stocks`, `turtle_soup_stocks` (keine Signalspalte) bei leerem Buch; Krypto nicht betroffen. Eigenschaft der eingefrorenen Eingabe; **keine Änderung vor dem Tag** (die Korrektur bräuchte Daten, die der Snapshot nicht hat; Ersatzgrössen änderten die Bedeutung der Regel). Wie oft Stufe 3 entscheidet, ist Messbitte R7 Nr. 7.
> (e) Papierpfad: Die beiden Elliott-Bots messen die Signalfrische (`SIGNAL_FRESHNESS_HOURS`) an `pd.Timestamp.utcnow()` statt an `entscheidungskerze.laufbeginn()`; keine Kerzenwahl, wirksam nur an der 48-h-Grenze. Betrieb, mit der nächsten Öffnung von `forward_test.py`, nach dem Tag.
> (f) Tatsachennotiz zu 16.4 (Evidenz der Leiter): `forward_test.py` legt `entry_price`/`stop_price` (Elliott auch `target_price`) als absolute Zahlen ab und vergleicht sie in späteren Läufen mit neu bereinigten Reihen; über einen Ex-Tag oder Split hinweg passen Niveau und Reihe nicht mehr zusammen. Betroffen sind die Bots mit Stop (`volatility_breakout`, `elliott_wave_stocks`) und `pnl_pct` aller vier Aktien-Bots. Der Selektionspfad ist frei davon. Behebung im Betrieb nach dem Tag, vor dem ersten Stufenwechsel der Leiter, der sich auf Papier-Evidenz stützt.
> *Quelle des Grundes:* Messungen TB-115 M1/M2, 31.3, 37.3, Plan-Punkt 6, 16.4 (i). Kein Ergebnis.

**Kette:** beantwortet F1-1 bis F2-3 (Fable 27a Abschnitt 3, M1 und M2).
Marke unter **16.4** („Prüfung vor dem Tag") für (f). Die Notizen (a) bis (e)
stehen hier und nicht an 5e, 28, 31 und Punkt 10, weil diese Stellen
Registertext bzw. Sperrlistentext sind (Punkt 10 liegt in Abschnitt 10, dort
steht keine Marke). ⭐ **(a) Die Probe** (vier Ausschlussmengen gleich) wird
in TB-117 Block E gebaut, ausserhalb der Sperrlistendateien; die Mengen
werden nur gelesen (46.11). ⛔ **(d) ändert vor dem Tag nichts** an
`shared/zuteilung.py`; die Messbitte steht als R7 Nr. 7 in 46.7 (a).

### 46.5 R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`)

> **R14 — Ergänzung zu 12 und 36.5 (Herkunftsprüfung in `auswertung.py`).** `auswertung.py` liest `<wurzel>/<bot>/herkunft.json` für jeden Bot und endet mit 2, wenn die Datei fehlt, wenn der Commit-Hash vom Tag-Commit (5e, `TB_SELEKTIONSCOMMIT`) abweicht, wenn der Datenstand-Hash vom registrierten Datenstand `d9449faf…` abweicht, wenn der Register-Hash von `herkunft.register()` zur Laufzeit der Auswertung abweicht, oder wenn die neun `herkunft.json` untereinander abweichen. Der Bericht trägt Commit, Datenstand und Register-Hash in seinem Kopf. Der Schreiber von `herkunft.json` (Zellen-Erzeuger) prüft sich nicht selbst; der Auswerter prüft ihn. Umsetzung: eine Öffnung von `auswertung.py` (Punkte 3/5/14) vor dem Tag, zusammen mit der Streichung aus R8 (a); Hash-Übergang nach 37.3.
> *Quelle des Grundes:* Docstring von `auswertung.py` Z. 51–52 (nennt `herkunft.json` als Teil des Vertrags), Abschnitt 12 (Vertragsbruch ⇒ Abbruch), 36.5, 25c (1) (Register-Code-Widerspruch ist 2), Prüfprinzip A8. Kein Ergebnis.

> ⭐ **46.5 (R14) ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **46.5 (R14) ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **46.5 (R14), Bedingung 5 ERGÄNZT durch R27 (47.10)** (Fable 27c R27, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** ergänzt **12** (Vollständigkeitstest; `auswertung.py` bricht bei
jeder Verletzung des Datenvertrags ab) und **36.5** (Ausgänge); beantwortet
F3-3. Marken am Ende von 12 und am Ende von 36.5. Was R14 ohne Modus
bedeutet, sagt R14 nicht; die Lesart des steuernden Chats steht in **46.9**.
Vollzug in TB-117 Block D (46.11), zusammen mit R8 (a) (45.8).

### 46.6 R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8

> **R15 — Ergänzung zu den Tag-Vorbedingungen (Snapshot-Bindung) und Tatsachennotiz zu Punkt 8.**
> (a) Das Abbild der Sperrliste führt in der Gruppe `eingefroren` zusätzlich `snapshots/<hash>/MANIFEST.json` und die Snapshot-Kopien von `config/top25_symbols.txt` und `config/sp500_top150.txt` (heute bytegleich mit dem Repo, `3afc95a4…`, `6acba892…`). Punkt 8 bleibt im Wortlaut (bindet die Repo-Dateien); Tatsachennotiz an Punkt 8: unter dem Modus liest der Lauf die Snapshot-Kopien, gebunden über das Abbild.
> (b) Tag-Vorbedingung: `snapshot.py --pruefen` endet am Tag-Commit mit UNVERAENDERT (rc 0), Beleg im Tag-Ordner. Die Startprüfung vergleicht `TB_SELEKTIONSHASH` weiter mit dem im MANIFEST notierten Hash; sie rechnet den Snapshot nicht nach — den gerechneten Datenstand trägt die Kette (R5 (d), R14).
> *Quelle des Grundes:* R3 (das Abbild bindet Eingaben), Prüfprinzip A8 (Selbstauskunft ist keine Wache), 25f A3 (keine Wache doppelt). Kein Ergebnis.

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

> **R16 — Ergänzungen zu R5 und R7.**
> (a) R7 Nr. 7: Wie oft entscheidet Stufe 3 der Zuteilungskaskade je Aktien-Bot und Falte, und wie oft wäre die Rangfolge unter Stückzahl × Split-Faktor eine andere? Bericht, kein Tor (R13 d).
> (b) R5 (d): Der Zellen-Erzeuger schreibt in `herkunft.json` den mit `herkunft.datenstand(<Snapshot-Datenordner>)` **gerechneten** Datenstand-Hash, nicht den im MANIFEST notierten, dazu Commit und `herkunft.register()`.
> *Quelle des Grundes:* R6/R7, R14, R15. Kein Ergebnis.

**Kette:** (a) ist **Nr. 7** der Liste in **45.7** (R7), vor dem Tag
ergänzt und damit nach 45.7 zulässig, datiert 26.09.2026 (Fable 27a);
Marke unter 45.7. (b) ist Punkt **(d)** zu **45.5** (R5); gilt für den
Zellen-Erzeuger, der noch nicht gebaut ist.

### 46.8 R17 — Tatsachennotizen 27a

> **R17 — Tatsachennotizen 27a.**
> (a) Modulkopf von `herkunft.py` beschreibt `register` als Hash über „die Registerdatei, die Module dieses Ordners und die vorab berechneten Tabellen"; seit TB-114 B3 gehören die neun TB-24-Listen dazu. Nachtrag mit der nächsten Öffnung (R10).
> (b) Testannahmen TB-114 nach Grundsatz 40: `test_ersatzwerte.py` E-bM (Mutation der ersten Wache endet an der zweiten mit 2 statt 0; Ort `block` weiter verlangt), `test_sperrlistensonde.py` 8a (10 ⇒ 19), H7f (25 ⇒ 34); die Fassungen am Stand `77147f7` brechen genau dort (60/61, 57/59).
> (c) M1 (TB-115): 9/9 Bots entscheiden auf der geschlossenen Kerze — Papierpfad über `entscheidungskerze.lade` (je 1 Aufruf, 0 Abrufe an der Schicht vorbei), Selektionspfad über den Rand des Datenstands. Schliesst die Verfahrensmessung aus R7. Randbefund R2 (Endgültigkeit des yfinance-Schlusskurses um 20:15 UTC) ist Betrieb, nicht gemessen.
> (d) M3 (TB-115): Die Sonde bindet von der Kette Datenstand → Zellen-Erzeuger → `zellen.csv` → `auswertung.py` → Bericht nur Glied 4 samt Importen und Tabellen; Glieder 1, 3 und 5 werden über R14 und R15 gebunden, Glied 2 mit dem Zellen-Erzeuger (R5). Damit ist die vierte Verfahrensmessung aus R7 („deckt TB-85 die Kette") beantwortet: nein.
> *Quelle des Grundes:* Messungen TB-114/TB-115. Kein Ergebnis.

**Kette:** (a) wird mit der Öffnung von `herkunft.py` in TB-117 Block C
vollzogen (46.11). (b) bis (d) sind Tatsachen; (c) und (d) schliessen die
Verfahrensmessungen aus 45.7 (R7) und damit Zeile (1) von 45.10.

### 46.9 Lesart des steuernden Chats zu R14 ohne Modus — von Fable zu bestätigen (Tatsachennotiz)

R14 nennt die fünf Abbruchbedingungen, sagt aber nicht, ob sie auch ohne
Selektionsmodus gelten. Der steuernde Chat hat im Auftrag eine Lesart
festgelegt und für Fable benannt, zeichengleich
(`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md`, Freigabe des Betreibers
26.09.2026, ca. 22:20):

„R14 unter dem Modus vollständig: Jede der fünf Bedingungen endet mit 2. Ohne Modus liest `auswertung.py` `herkunft.json`, wenn vorhanden, und zeigt Commit, Datenstand und Register-Hash im Kopf des Berichts, bricht aber nicht ab. Grund: Ohne Modus laufen Beispieldaten und Tests, und `beispieldaten.py` schreibt Nullwerte (Z. 210 ff.). Dieselbe Bauart wie R10 (`fehlend` ⇒ 2 nur unter dem Modus)."

⚠️ **Vorläufig, bis Fable bestätigt.** TB-117 setzt diese Lesart in Block D
um; weicht Fables Antwort ab, ist das eine weitere Öffnung von
`auswertung.py`.

> ⭐ **46.9 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

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

### 46.11 Vollzug in TB-117 (Tatsachennotiz)

**Gemessen in TB-117, 26./27.09.2026** (Belege `docs/belege/TB-117/`, Ergebnis
`docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md`). Eingang `8b342ab`, Schritt 0
`753ec11`, Block A `4c5615d` (45.11 und 46.0–46.10). Freigabe des Betreibers
26.09.2026, ca. 22:20 (Auswahlkarte, wörtlich im Auftrag). Kein
Abbruchkriterium ausgelöst.

**Hash-Übergänge nach 37.3:**

| Block | Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|---|
| B | `shared/sperrlistensonde.py` | `f88e54ee…` | `98c02e0e…` | `42ef509` | R9 (46.1) |
| C | `research/vorregistrierung/herkunft.py` | `ed521ac1…` | `c6c13388…` | `ff2f254` | R10 (46.2), R15 (a) (46.6), R17 (a) (46.8) |
| D | `research/vorregistrierung/auswertung.py` | `a864b216…` | `8ec45123…` | `852f253` | R14 (46.5), Lesart 46.9, R8 (a) (45.8) |

**`herkunft.register()`:** `5acb4c19…` (Eingang) ⇒ `6bcb4f58…` (nach
Block A) ⇒ `b8f2cc33…` (nach Block C; 23 Teile, `fehlend` leer) ⇒
`e87a4d8e…` (nach Block D, gemessen vor diesem Eintrag). Der Wert nach
diesem Eintrag kann hier nicht stehen (er hasht diesen Text); er steht im
Ergebnis.

**B (R9):** Die Sonde vergleicht zusätzlich die heutige Liste
`herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds; ein
Eintrag nur auf einer Seite ist Befund 1 mit Eintrag und Seite
(„Liste → Abbild fehlt“ bzw. „Abbild → Liste fehlt“). Gegen das alte Abbild
`e655c1c8…` meldet sie die neun TB-24-Listen „nur in der Liste“ — die Zeile,
die R11 als fehlend beschreibt.

**C (R10, R15 (a), R17 (a)):** `register()` und `block()` enden unter dem
Modus mit 2, wenn `fehlend` nicht leer ist (je eigene Fundstelle, Meldung
nennt die Einträge); ohne Modus unverändert. `EINGEFROREN` führt zusätzlich
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json`
und die beiden Kopien `…/config/top25_symbols.txt` und
`…/config/sp500_top150.txt` des Snapshots aus Register 18 — versioniert,
repo-relativ, in `herkunft.py` und Sonde gleich aufgelöst; **keine dritte
Pfadauflösung**. Die `config/`-Kopien stecken im Snapshot-Hash (225 Dateien),
nicht im Datenstand (223). Die Tatsachennotiz an Punkt 8 steht in 46.6.

**D (R14, Lesart 46.9, R8 (a)):** `auswertung.py` liest `herkunft.json`
unter dem Modus für alle neun Bots und endet mit 2 bei jeder der fünf
Bedingungen; der registrierte Datenstand steht als Konstante
`REGISTRIERTER_DATENSTAND` mit Fundstelle Register 18. Ohne Modus: nur
Anzeige. Der Kopf des Berichts trägt Commit, Datenstand und Register-Hash.
Der Satz „`Abbruch` … endet mit 1“ ist berichtigt; damit ist Zeile (5) von
45.10 für R8 (a) erledigt.

**Gültiges Abbild ab jetzt** (nach R11 „nach dem Bündel ein neues Abbild“):
`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`,
sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f`
(11 432 B, 14 Punkte, `eingefroren` 22 = `EINGEFROREN`, HEAD `852f253`).
Sonde dagegen 37/0/0, (ii) 0, Mengenvergleich 22/22 ohne Befund. Es ersetzt
`5e5ad109…` (45.11); nichts ist überschrieben.

**Sonde gegen `5e5ad109…`, jeder Eintrag zugeordnet:** Punkte 3, 5, 14 und
Gruppe `eingefroren`: `auswertung.py` (Block D); Punkte 11, 12:
`herkunft.py` (Block C); Gruppe `eingefroren`, „Liste → Abbild fehlt“:
MANIFEST und die zwei Snapshot-`config/`-Kopien (Block C). Kein Eintrag ohne
Zuordnung.

**Probe R13 (a):** `shared/test_ausschlussmengen.py` liest die vier
Ausschlussmengen mit `ast` (keine importiert, keine geändert) und verlangt
Gleichheit samt `XAUTUSDT` — 9/9, drei Mutationen je mit Gegenprobe. Die
Zusammenlegung bleibt der jeweils nächsten planmässigen Öffnung.

**Unverändert gemessen:** Benchmark im Modus Repo und frischer Klon
`64fb2912…`; acht Ausgaben ohne Modus bytegleich mit TB-114; Trockenlauf
9 × rc 0; `faltenplan.json` `0e54ac5c…`; Laufbereich 81 Module (= TB-114).
Tests am Stand `54ce889`:
44 Dateien, 41 rc 0 (darunter `test_vorregistrierung` 196/196,
`test_ersatzwerte` 99/99, `test_sperrlistensonde` 65/65,
`test_ausschlussmengen` 9/9, `test_startpruefungen` 44/44,
`test_arbeitsbaum_laufbereich` 26/26); ohne rc 0 nur die drei bekannten
ohne Bezug zu diesem Auftrag (`test_drawdown_beide_masse` terminiert nicht,
`test_stabile_sortierung` 43/3, `test_wellenauswahl` 322/1 — dieselben
Stellen wie TB-114).

**Nicht vollzogen in TB-117:** R12 (Neuerzeugung der Listen), R15 (b) (am
Tag-Commit), R16 (a) (nach dem Tag) und (b) (mit dem Zellen-Erzeuger), die
Bestätigung von 46.9 durch Fable.

