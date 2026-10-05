# REGISTER-KOPIE Abschnitt 45 (von 0–54) — Register-Z. 10162–10385 — Commit 9b7b06065ebdae3f36f3102306c76bb844300e90 — 2026-10-05 — Original sha256 8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc — KOPIE, nicht das Register

## 45. Messbitten nach dem Tag, Reichweite (iv), Eingaben im Abbild, Pflege der Pfadliste, Abnahmebedingungen des Erzeugers — die Einträge aus Fable 26a (TB-114, 26.09.2026)

### 45.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, Bauart wie **43**
(TB-110). Anlass ist die **erste gesammelte Tagesanfrage** an den
Verfahrensprüfer — Fable, zeichengleich: „Erste gesammelte Tagesanfrage."
— mit dem neuen Fable-Takt, einmal je Tag: „diese Antwort ist die erste im neuen Takt."
Sie beantwortet die Ergebnisse TB-109 bis TB-113 und die Fragen, die
**44.3** (44-12) zeichengleich sammelt.

**Quelle:**
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md`
(md5 `e2a492165d44f6ee3d02eba99d2acf2c`, 22 331 Bytes, committet in TB-114
Schritt 0, `79c2dfa`), Abschnitt „Registerblock — zeichengleich kopierbar,
nummeriert", R1–R8. ⚠️ **Tatsachennotiz zur Herkunft (wie 41.0, 43.0):** Die
Datei hat der steuernde Chat übertragen; die Zitate hier sind zeichengleich
mit der Datei im Repo, ob diese zeichengleich mit Fables Ablage ist, ist nicht
gemessen.

**Die Kette zu 43 und 44:** 43.3 führt die Berichtigung „`None` statt
`False`" als **vorläufig**; 44.3 (1) führt die Fragen aus TB-109, TB-111 und
TB-112 als offen bei Fable. **Beide sind hier beantwortet** (45.1 bis 45.8).
Die Zeilen in 43 und 44 bleiben zeichengleich; Marken darunter verweisen
hierher. Die Nummer hat der steuernde Chat vergeben
(`docs/auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md`,
Freigabe des Betreibers 26.09.2026, ca. 16:30), nicht Fable.

**Bauart je Eintrag:** 45.1 bis 45.8 tragen je einen Baustein R1 bis R8
**zeichengleich** aus dem Codeblock am Ende der Fable-Antwort, samt seiner
„Quelle des Grundes", als Blockzitat, **eingesetzt, nicht abgetippt**; je
Baustein ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-114/a2_r_diff.txt`). Nichts ist umformuliert. Darunter steht
je Eintrag die Kette (wohin die Marke am alten Ort zeigt). 45.9 ist eine
Tatsachennotiz des steuernden Chats, 45.10 die Liste des Offenen; der Vollzug
in TB-114 folgt als 45.11.

**Einordnung von R6 — Fables drittes „Unsicher", zeichengleich:**
„Ob R6 eine Ergänzung zu 27 oder zu 7.1 ist — ich schlage 27 vor (es geht um Lesen nach dem Tag); Handwerk der Einordnung."
Eingeordnet ist R6 als Ergänzung zu **27**, wie sein Titel sagt; die Marke
steht **an beiden Orten** (am Ende von 27 und unter 7.1), weil 7.1 die Regel
ist, auf die R6 sich für „Bleibt oder Geht" beruft.

⭐ **Die Regel aus 34 gilt weiter:** Marken am alten Ort, der alte Satz
zeichengleich, `git diff --numstat` auf dieses Register mit `0` in der zweiten
Spalte. ⛔ **In Abschnitt 10 steht keine Marke** (Sonde, Prüfung (ii)).

### 45.1 R1 — Marke an 43.3 (Bestätigung)

> **R1 — Marke an 43.3 (Bestätigung).** Die Berichtigung „`selektionsmodus = lambda: None` statt `lambda: False`" ist von Fable bestätigt (26a 3 (1)). Grund: Der Stummel soll das Werkzeug so laufen lassen wie am Stand TB-52; gemessen tut das nur `None` (`strategy_paths` legt 9 von 9 Ordner an), `False` nimmt den Modus-Zweig und meldet trotzdem 0 Unterschiede. Fables Beispiel `lambda: False` in 25e 3 war ungemessen — neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt". Handwerk als Beifang: Das Werkzeug zählt künftig die angelegten Ordner im Wegwerfbaum und meldet den durchlaufenen Zweig.
> *Quelle des Grundes:* Messung TB-109/TB-113, Prüfprinzip A5. Kein Ergebnis.

**Kette:** bestätigt **43-11** (43.3, „vorläufig, von Fable nicht
bestätigt"); die Überschrift und der Text von 43.3 bleiben zeichengleich, die
Marke steht darunter. Die Zweigprüfung im Werkzeug ist Beifang, kein Auftrag.

### 45.2 R2 — Ergänzung zu 42 (Klasse (iv), Reichweite)

> **R2 — Ergänzung zu 42 (Klasse (iv), Reichweite).** Klasse (iv) umfasst jeden lesenden Zugriff eines Laufs auf seine eigene Zwischenablage: die Verzeichnis-Öffnung beim Aufräumen und das Lesen des darin abgelegten Ergebnisses. Die Probe, die `tempfile` beim Anlegen einer Ablage selbst macht (kein `mkdir` im Protokoll, sofort entfernt), ist Umgebung — Klasse (ii) — und wird als Tatsachennotiz geführt.
> *Quelle des Grundes:* 25b (Definition von (iv): angelegt mit `mkdtemp`, vom Lauf selbst gelesen, entfernt oder im Beleg), 25e 3 (b). Kein Ergebnis.

**Kette:** ergänzt **42.2 E1** (Klasse (iv)); beantwortet TB-109 Frage 2
(44.3). Marke unter 42.2 E1.

### 45.3 R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`)

> **R3 — Ergänzung zu 30.2 (3) / 33.3 (Abbild der Sperrliste, Gruppe `eingefroren`).** Versionierte Dateien, die ein Lauf des Laufbereichs als Daten liest und die kein Code sind, gehören mit ihrem Hash in die Gruppe `eingefroren` des Abbilds — namentlich die neun Listen `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`, aus denen der Faltenplan seine Faltenlängen herleitet (TB-95). Die Startprüfung nach 19/E2 bindet Code; das Abbild bindet Eingaben. Dass eine Änderung der Listen den Plan und damit dessen Abbild änderte, ersetzt die Bindung der Eingabe nicht: Der Nachweis verlangt die Eingabe bytegleich und gelesen (24c).
> *Quelle des Grundes:* 25b (Klasse „Code" gegen Eingaben), 24c (zwei Teile des Nachweises), 24c B1. Kein Ergebnis.

**Kette:** ergänzt **30.2 (3)** und **33.3**; beantwortet TB-112 Frage 1
(44.3). Marken unter 30.2 und 33.3. Die Voraussetzung dafür, dass die Gruppe
`eingefroren` diese Pfade aufnehmen kann, ist in **45.9** gemessen; der
Vollzug steht in **45.11**.

> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Zitat und Kette oben bleiben zeichengleich.

> ⭐ **45.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 45.4 R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`)

> **R4 — Ergänzung zu 19 / 42.2 E2 (Pflege von `ARBEITSBAUM_PFADE`).** Die Liste der Pfade der Sauberkeitsprüfung steht als Literal im Resolver; eine Gegenprobe liest die Laufbereichsmessung aus der Messdatei und vergleicht. Am Tag-Commit wird der Laufbereich neu gemessen; weicht die Messung von der Liste ab, ist das ein Befund: Die Liste wird vor dem Tag nachgezogen, nie durch ihn. Die Liste wird nicht aus der Messung erzeugt.
> *Quelle des Grundes:* Prüfprinzip B3 (ein Gegenbeweis gegen eine bewegliche Referenz prüft nichts), 25b E5 (Messung am Tag-Commit). Kein Ergebnis.

> ⭐ **45.4 (R4) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** ergänzt **19** und **42.2 E2**; beantwortet TB-112 Frage 2 (44.3).
Heute gebaut ist genau diese Form (Literal in `shared/paths.py`, Gegenprobe
in `shared/test_arbeitsbaum_laufbereich.py` gegen
`docs/belege/TB-112/a2_laufbereich.txt`, 44-8). Marken unter 19 (unter der
TB-113-Marke) und unter 42.2 E2.

### 45.5 R5 — Abnahmebedingungen des Erzeugers

> **R5 — Abnahmebedingungen des Erzeugers (Ergänzung zu 24b A12 / Plan-Punkt 10).**
> (a) Die Laufbereichsmessung nach dem Einbau des Erzeugers enthält `research/vorregistrierung/herkunft.py`; `ARBEITSBAUM_PFADE` ist danach nachgezogen (R4). Bis dahin ist `herkunft.py` am committeten Stand über die Sperrliste (Punkte 11/12) und das Abbild gebunden; die Lücke im Arbeitsbaum ist als Tatsachennotiz in 44 benannt.
> (b) `zellen.csv` enthält für jede Zelle des Rasters genau eine Zeile; die Zeilenzahl ist gleich der Zahl der Zellen; eine Zelle ohne Trades trägt die Nullzeile (Sharpe 0 nach Registertext 1c, leere Trade-Liste), nie nichts. Eine fehlende Zeile ist ein Befund über den Erzeuger, kein Ausgang.
> (c) `herkunft.datenstand()` endet unter dem Modus ohne übergebenen Pfad mit 2; Beifang der nächsten Öffnung von `herkunft.py`, kein eigener Auftrag.
> *Quelle des Grundes:* 24b A10 (kein Fallback unter dem Modus), 25e (2) (null Trades ist ein Wert), 36.5, 26a 5. Kein Ergebnis.

> ⭐ **45.5 (R5) (a) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **45.5 (b) BERICHTIGT durch R33 (48.1)** (Fable 29b R33, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** ergänzt **41.1 A12** und die Zeile **(5)** in **42.6** (der
Erzeuger auf dem Signalpfad); beantwortet TB-109 Frage 3 (b) und TB-111
Frage 1 (c) (44.3) und Fables Punkt (5) zur Wechselwirkung (a). **(c) ist in
TB-114 vollzogen** (Block B, 45.11). Marken unter 41.1 A12 und in 42.6
Zeile (5).

> ⭐ **45.5 ERGÄNZT durch R34 (48.2)** (Fable 29b R34, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **45.5 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 45.6 R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag)

> **R6 — Ergänzung zu 27 (Messungen auf dem Selektionsraum nach dem Tag).** Nach dem signierten Tag werden auf dem Selektionsraum dieses Durchgangs nur die Messungen gerechnet, die vor dem Tag als Messbitte registriert sind (R7). Jede weitere Messung auf denselben Zellen ist ein Versuch: Sie wird im Versuchsregister geführt und zählt in N des nächsten Durchgangs. Keine Messung nach dem Tag — registriert oder nicht — ändert Bleibt oder Geht; das sagt 7.1. Registrierte Messbitten sind Bericht, nicht Tor.
> *Quelle des Grundes:* 7.1, Festlegung 11, Literatur (Story-telling und Data Snooping nach dem Ergebnis, López de Prado; „every backtest must be reported with all trials"). Kein Ergebnis.

**Kette:** ergänzt **27**; beruft sich auf **7.1**. Registertext **vor** dem
Tag, weil er am Tag danach schon gelten muss (Fable 26a 3 (6)). Marken am
Ende von 27 und unter 7.1.

### 45.7 R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a

> **R7 — Liste der registrierten Messbitten für nach dem Tag (Anhang zu R6), Stand 26a.**
> 1. PBO je Bot über alle Zellen (CSCV, S = 16) — 25f V3.
> 2. MinTRL und Lo-Standardfehler je Gewinnerzelle — 25f V7.
> 3. Netto-Sharpe der Gewinnerzellen unter 0,5 %, 1,0 % und 1,6 % Roundtrip — 25f K2.
> 4. Implizite Kelly-Fraktion je Bot gegen die feste Positionsgrösse — 25f P5.
> 5. Krypto-Umkehr-Bots nach Liquiditätsdrittel des Universums — 25f S8.
> 6. Block-Bootstrap-Band je Gewinnerzelle für den Vergleich mit der Bestätigungsperiode — 25f O2.
> Verfahrensmessungen nach 27.2 (vor dem Tag zulässig, nicht Teil dieser Liste): Adjustierungsstand und Herkunft der 150 Aktienreihen im Snapshot; Nutzung von Preisniveaus je Bot; ob alle neun Bots die geschlossene Kerze lesen; ob TB-85 die Kette Erzeuger → Auswertung deckt. Ergänzungen dieser Liste vor dem Tag sind zulässig und werden datiert; nach dem Tag ist die Liste geschlossen.
> *Quelle des Grundes:* R6. Kein Ergebnis.

**Kette:** Anhang zu **45.6**. Die vier Verfahrensmessungen nach 27.2 sind
nicht Teil der Liste; drei davon sind in 45.10 als offen geführt. Ergänzungen
vor dem Tag werden datiert angehängt, hier oder in einem späteren Abschnitt
mit Marke hier.

> ⭐ **Nr. 7: siehe 46.7 (a)** (Fable 27a R16 (a), TB-117, 26.09.2026). Zitat
> und Kette oben bleiben zeichengleich.

### 45.8 R8 — Tatsachennotizen 26a

> **R8 — Tatsachennotizen 26a.**
> (a) `auswertung._abbruch_2`: Der Docstring sagt „`Abbruch` … endet mit 1"; falsch seit TB-111, stehen geblieben wegen der Freigabe „sonst nichts"; Streichung mit der nächsten planmässigen Öffnung.
> (b) `str(e)` eines gefangenen `Abbruch` ist `"2"`, die Meldung steht in `e.meldung`; im Laufbereich (81 Module, Stand TB-113) liest kein Aufrufer `str(e)` — Suchmuster in der Notiz nennen, Messung am Tag-Commit wiederholen.
> (c) db-Sicherung (25f O6): Schlüssel-Muster `key|secret|token|api|passw`, 0 Treffer über 12 Datenbanken; die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` enthält laut Code nur `erstlauf_am`; deutsche Wörter nicht aufgenommen — Betrieb, nicht Lauf.
> (d) N = 653 (Register 9): Was das Versuchsregister nicht zählt und nicht rekonstruieren kann, steht dort in 3.4 und 5.1–5.4; ein Verweis aus Register 9 auf Abschnitt 5 des Versuchsregisters wird nach dem Tag eingetragen. Folge für die Lesart: N_nominal ist eine Untergrenze.
> (e) Berichtigung zu 25f A2 und C3 Entscheidung 8: Das Zellenbudget steht in 16.4 (g)–(m); offen ist nur der Vollzug im Code (16.11, Zeile 3; Stufe IV). Fables Satz „keinen Abschnitt gefunden" war aus dem Gedächtnis; Fables Regel: Vor „steht nicht im Register" wird im Text gesucht, nicht erinnert, und das Suchwort genannt.
> *Quelle des Grundes:* Messungen TB-111, TB-112, TB-113, 26a 3 (a)/(b). Kein Ergebnis.

**Kette:** (a) und (b) beantworten TB-111 Fragen 2 und 3, (c) TB-112 Frage 3
(44.3). ⛔ **(a) ist nicht vollzogen:** Der Docstring von
`auswertung._abbruch_2` bleibt bis zur nächsten planmässigen Öffnung von
`auswertung.py` stehen. ⛔ **(d) ist nicht vollzogen:** Der Verweis aus
Register 9 kommt **nach** dem Tag; in 9 steht deshalb heute keine Marke.

### 45.9 Tatsachennotiz des steuernden Chats zu R3 — zwei Pfadregeln

Fables erstes „Unsicher", zeichengleich:
„Ob die Gruppe `eingefroren` des Abbilds heute Dateien ausserhalb `research/vorregistrierung/` aufnehmen kann"

**Gemessen am 26.09.2026 über die Brücke am Stand `0df8c64`, nur lesend** (vom
steuernden Chat; in TB-114 am Stand `79c2dfa` wiederholt, beide Dateien
unverändert):

- `herkunft.register()` löst jeden Eintrag von `EINGEFROREN` mit
  `os.path.join(_HIER, rel)` auf, also immer relativ zu
  `research/vorregistrierung/` — die Zeile, zeichengleich:
  `pfad = os.path.normpath(os.path.join(_HIER, rel))`
- `shared/sperrlistensonde.py::_aufloesen` löst einen Eintrag nur dann
  relativ zu `research/vorregistrierung/` auf, wenn er kein `/` enthält oder
  mit `ergebnisse/` beginnt; sonst repo-relativ (Feld `pfadregel` im Abbild) —
  die Zeile, zeichengleich:
  `if "/" not in pfad or pfad.startswith("ergebnisse/"):`
- **Folge:** Ein Eintrag für `research/tb24_haltedauern/daten/…` wäre in einem
  der beiden Programme nicht auffindbar. `register()` führt eine nicht
  gefundene Datei in `fehlend` und rechnet ohne sie weiter:
  `fehlend.append(rel)`
- Die zehn heutigen Einträge sind von der Abweichung nicht betroffen: jeder
  hat entweder kein `/` oder das Präfix `ergebnisse/`, beide Regeln liefern
  denselben Ort.
- **Vollzug:** Block B von TB-114 (45.11).

### 45.10 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | Die drei Verfahrensmessungen nach 27.2: ob alle neun Bots die **geschlossene Kerze** lesen; **Adjustierungsstand und Herkunft der 150 Aktienreihen** im Snapshot; ob **TB-85** die Kette Erzeuger → Auswertung deckt | TB-115 |
| (2) | **Der Erzeuger** auf dem Signalpfad, mit den Abnahmebedingungen aus 45.5 (a) und (b) | Plan-Punkte 3 und 5 |
| (3) | **Das Faltenplan-Abbild** und die Faltenplan-Sonde | Plan-Punkt 7, TB-101 |
| (4) | **Stufe IV** (Leiter-Skript, 16.11 Zeile 3; Fable 26a 2 (a), R8 (e)) | Stufe IV |
| (5) | R8 (a) Docstring `auswertung._abbruch_2`; R8 (d) Verweis in Register 9 | nächste Öffnung von `auswertung.py`; nach dem Tag |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich):
7.1 · 19 · 27 · 30.2 · 33.3 · 41.1 A12 · 42.2 E1 · 42.2 E2 · 42.6 Zeile (5)
· 43.3 · 44.3. ⛔ Keine in Abschnitt 10, keine in 9.

> ⭐ **Beantwortet und fortgeschrieben in 45.11 und 46** (Fable 27a, TB-117,
> 26.09.2026). Tabelle und Text oben bleiben zeichengleich.

### 45.11 R11 — Abbild gültig; Tatsachennotiz zum Abbruch TB-114 (Fable 27a, TB-117, 26.09.2026)

> **R11 — 45.11 (Abbild gültig; Tatsachennotiz zum Abbruch TB-114).** Gültiges Abbild ist `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json`, `5e5ad109…` (10 805 B, 14 Punkte, `eingefroren` 19, HEAD `0b7ab4b`); Sonde dagegen 34/0/0, (ii) 0, gemessen TB-114 C und TB-115 0b (vorher = nachher). Tatsachennotiz: TB-114 endete in Block C mit Abbruchkriterium, weil der Auftrag gegen das alte Abbild `e655c1c8…` „die neun neuen Einträge in `eingefroren`" als Befund erwartete; die Sonde meldet Zuwachs in `EINGEFROREN` gegen ein altes Abbild nur mittelbar über den Hash von `herkunft.py` (Punkte 11/12). Zwei Ursachen: eine ungemessene Erwartung im Auftrag (Regel des steuernden Chats: Erwartungen an ein Werkzeug nur mit Fundstelle) und eine einseitige Sonde (R9). Der Abbruch war regelgerecht; nichts wurde repariert. Nach dem Bündel (R9, R10, R14, R15) folgt ein neues Abbild nach 37.3.
> *Quelle des Grundes:* Messungen TB-114/TB-115, Nachtrag 6d (Abbruchkriterium führt zu Abbruch, nie zu Rückfrage). Kein Ergebnis.

**Kette:** Vollzug der in **45.0** angekündigten Nummer 45.11 — nicht durch
TB-114 (Abbruch in Block C, `e07fefd`/`90307cb`), sondern mit Fables Antwort
27a (T114-2) in TB-117. Das Abbild ist seit TB-114 unverändert; gemessen am
Eingang von TB-117 (`753ec11`, `docs/belege/TB-117/0b_ausgang.txt`): sha256
`5e5ad1097909b3531e19b238153cabc46e7b551bb25e369ddc6735836e71cd06`, Sonde
dagegen 34/0/0. Der Satz in R11 „Nach dem Bündel (R9, R10, R14, R15) folgt
ein neues Abbild nach 37.3" wird in TB-117 Block E vollzogen; das Ergebnis
steht in **46.11**. Bis dahin gilt `5e5ad109…`. Die Marke unter 45.10 zeigt
hierher und auf 46.

