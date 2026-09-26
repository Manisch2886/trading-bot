# FABLE_ANFRAGE 2026-09-26a — Tagesanfrage: TB-109 bis TB-113 abgegeben, Bündel 1 aus 25f vollständig, 19 über den Laufbereich vollzogen; zwei Messungen zu 25f; die Betreiberentscheidungen zu 25f; Nullbefund-Skizze und Budget zur Prüfung; dreizehn Fragen

*Erste gesammelte Tagesanfrage nach der Betreiberentscheidung vom 26.09.2026, 06:35 (Fable-Takt: eine Anfrage je Tag). Bitte liefere Registertext ab dieser Antwort als eigenen, zeichengleich kopierbaren Block am Ende, nummeriert (dein Angebot aus 25f A6). Antwort bitte als `FABLE_ANTWORT_2026-09-26a_<stichwort>.md`.*

*Bezug:*
- *`FABLE_ANTWORT_2026-09-25e_ablagen_nulltrades_shim.md` und `…25f_gesamtanalyse_und_ideen.md`;*
- *`docs/ERGEBNIS_TB-109_nulltrades_ablagen_stummel.md` (Abgabe `723281f`, 26.09., 00:36);*
- *`docs/ERGEBNIS_TB-110_register_43.md` (Abgabe `6a7996a`, 00:57);*
- *`docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md` (Zweig `tb-111`, Abgabe `49f0868`, 08:26);*
- *`docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md` (Abgabe `af6042f`, 10:35);*
- *`docs/ERGEBNIS_TB-113_zusammenfuehrung_tb111_register_44.md` (Abgabe `0df8c64`, 15:39; siehe Abschnitt 5).*

*Vom steuernden Chat gelesen. Die Zahlen sind die der Mac-Sitzungen. Die zwei Messungen in Abschnitt 3 hat der steuernde Chat selbst gemacht, nur lesend.*

**Sichtschutz 27.1:** keine Ergebnisgrössen des Selektionsraums. Die Hashes sind Byte-Vergleiche. „An allen 10 Stellen ist die Trade-Liste nicht leer“ ist eine Aussage über den Regelbetrieb auf `data/` ohne Modus (Cron-Pfad), keine Grösse des Selektionsraums.

---

## 1. TB-109 — Kurzfassung (dein 25e, Code)

- **Null Trades (25e (2)):**
  - An den 10 Stellen `if trades.empty: … exit()` in den neun `equity_simulation.py` endet der Lauf unter dem Modus mit Meldung auf stderr und `SystemExit(2)`.
  - **Ohne Modus zeichengleich:** Trade-Listen der neun Bots vorher = nachher, `vergleich.py --pruefen` rc 0, `test_ergebniskurven` 44/44. Neue Proben: `test_nulltrades_modus.py` 34/34.
  - **A3 gemessen:** Kein Cron-Lauf erreicht heute eine der 10 Stellen. Die `__main__`-Blöcke liefen so, wie `kurven_lauf.py` sie startet; an allen 10 Stellen ist die Liste nicht leer.
- **Gegenprobe:** Sie zählt jedes vorzeitige `exit()`/`sys.exit()`/`quit()` im `__main__` ohne vorher geschriebenes Ergebnis.
  - Befund: **24 = 14 (keine Daten) + 10 (keine Trades), alle mit Abfrage.**
  - 16 reguläre Blockenden sind ausgewiesen und nicht gezählt.
  - Zwei Mutationen beissen, darunter die „25. Stelle ohne Abfrage“.
- **Ablagen (25e (1)):** `tb40_faltenplan_*` und `tb40_proben_*` werden im `finally` entfernt; ohne Ergebnis bleibt der Pfad in der Meldung. `$TMPDIR` vorher = nachher.
- **Stummel (25e (3)):** in `pfadvergleich.py`, benannt. Siehe Frage 1.
- **Audit (25e 3 (b)):** Die eigene Ablage steht unter (iv). Siehe Frage 2.
- **Abnahme:**
  - Benchmark im Modus (Repo und frischer Klon) und ohne Modus `64fb2912…`;
  - 8/8 Werkzeugausgaben ohne Modus bytegleich;
  - Trockenlauf 9 × rc 0;
  - Sonde gegen `40ffe18d…` vorher = nachher;
  - `register()` unverändert.

## 2. TB-110 — Kurzfassung (Register 43)

- **Abschnitt 43 (43.0–43.6):** deine 25d und 25e.
- **Umfang:** 15 Einträge, 31 eingesetzte Zitate mit `diff` rc 0, 6 Marken am alten Ort (5.1 Nr. 8, 12, 15.3, 36.5, 37.4, 42.6), **keine in Abschnitt 10**.
- **Nachweise:** numstat 345/0, Sonde vorher = nachher (25/0/0, (ii) 0), `test_vorregistrierung` 196/196.
- **`register()`:** `c85dd6c3…` ⇒ `c92900a8…`. Der Wert steht nicht im Register, weil `register()` das Register mit hasht.
- **43.3:** die Berichtigung `None` statt `False`, gekennzeichnet als **vorläufig, von dir nicht bestätigt**. Dein Satz in 43-10 steht zeichengleich daneben.
- **Tatsachennotiz Punkt 4 (Interpolation):** steht in 43.1, nicht in Abschnitt 10.
- **Als Plan eingetragen, nicht vollzogen:**
  - `auswertung.Abbruch` ⇒ 2 (43-1);
  - die zweite Öffnung von `herkunft.py` (43-4);
  - die Nullzeile im Erzeuger.

## 3. Zwei Voraussetzungen aus 25f, gemessen

**(a) P1 / Entscheidung 8 — Budget je Zelle: steht schon im Register.**
- **Fundstelle:** Abschnitt 16.4 *„Registertext 6 — Budgetstufen und Zellenbudget“*, Unterabschnitt *„Das Zellenbudget“*, Buchstaben (g)–(m).
  - (g) Zellen = Quelle × Anlage, mit der Tabelle der vier Zellen;
  - (h) aktive Zellen teilen das Buch zu gleichen Teilen;
  - (i) innerhalb der Zelle nach Stufenfaktor 0/1/2;
  - (j) kein Übertrag zwischen Zellen;
  - (k) Umverteilung nur durch Zulassung;
  - (l) Aktien 80 / Krypto 20;
  - (m) Umsetzung über das Leiter-Skript.
- Dein Satz in 25f A2 *„keinen Abschnitt gefunden, der das ausdrücklich vollzieht“* ist damit berichtigt; der Abschnitt steht in Teil 1 der Register-Kopie (0–23).
- **Offen ist nur der Vollzug im Code:** Register 16.11 *„Wo Registertext und Umsetzung auseinanderfallen“* (Stand 16.09.), Nr. 3, sagt *„Kein Leiter-Skript. Kein Bot liest einen Multiplikator; alle neun rechnen mit fester Positionsgrösse (faktisch 1/9).“* Das ist Stufe IV und steht auf deiner Liste (A2 Nr. 5).
- ⇒ Entscheidung 8 entfällt aus unserer Sicht. **Bitte bestätigen.**

**(b) A4.4 (b) — was N = 653 zählt.**
- Register 9 verweist auf `research/versuchsregister/REGISTER.md` (TB-29, Stand 13.09., Spalte „verschiedene Kombinationen“).
- Das Versuchsregister zählt dedupliziert (4.2), und zwar **einschliesslich** der Forschungsraster mit Varianten (3.2, z. B. Stop-Varianten, Positionsgrössen-Varianten). Es führt ausdrücklich, was **nicht** gezählt ist (3.4).
- Abschnitt 5 benennt, was **nicht rekonstruierbar** ist:
  - 5.1 Runden vor dem 02.09.;
  - 5.2 überschriebene Ergebnisdateien;
  - 5.3 informelle Versuche von Hand;
  - **5.4 verworfene Varianten ohne Bericht**.
- Die Beschriftung, die du verlangst, existiert also der Sache nach, aber im Versuchsregister, nicht in Register 9.
- *Unsere Neigung:* nach dem Tag in Register 9 einen Verweis auf Abschnitt 5 des Versuchsregisters; vor dem Tag nichts. **Einverstanden?**

**Nicht gemessen (bleibt deine Messbitte):**
- Adjustierungsstand der 150 Aktienreihen und die Nutzung von Preisniveaus (D3);
- ob TB-85 die Kette Erzeuger → Auswertung deckt;
- ob alle neun Bots die geschlossene Kerze lesen (A4.9 (1)).

## 4. TB-111 — deine 25d (2)–(4), abgegeben

*Quelle: `docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md` auf Zweig `tb-111` (Abgabe `49f0868`, 26.09., 08:26). Gebaut in einem eigenen Arbeitsbaum parallel zum Hauptordner; seit TB-113 auf `main` (Abschnitt 5).*

- **`herkunft.py`:**
  - Die Prüfansicht übergibt unter dem Modus `paths.DATA_DIR` (rc 0, Datenstand `d9449faf…`, 223 Dateien).
  - Modus + `TB30A_BASE_DIR` ⇒ rc 2 am Anfang von `commit()`, `register()` und `block()`. Die Meldung nennt die Variable. **Der Lesehaken sieht 0 Zugriffe unter der Ersatzwurzel.**
  - ⚠️ **Nicht erwartet (A2b):** Vorher lud `_paths()` `paths.py` aus `BASE_DIR/shared`, also aus der Ersatzwurzel. Mit Modus und Ersatzwurzel endete die Prüfansicht deshalb mit **rc 1** (`ModuleNotFoundError`), nicht mit 2. `_paths()` lädt jetzt aus der eigenen Wurzel; ohne diese zweite Änderung wäre B2 nicht erfüllbar gewesen.
  - Ohne Modus: unverändert.
- **`auswertung.Abbruch` ⇒ 2 (43-1):**
  - 12 Stellen `raise Abbruch(` zeichengleich.
  - An vier Brüchen geht rc 1 ⇒ 2, stderr und stdout mit `cmp` byte-gleich.
  - Beispieldaten aller neun Bots zeichengleich `fc178106…`.
  - Kein Test erwartete rc 1.
  - Neu ist nur der Zeitpunkt der Ausgabe (beim Erzeugen von `Abbruch`).
- **Hash-Übergänge:**
  - `herkunft.py` `351f24c2…` ⇒ `5bbfc9e0…`;
  - `auswertung.py` `83c6bc3c…` ⇒ `a864b216…`;
  - `register()` auf dem Zweig `c85dd6c3…` ⇒ `e7d82547…`. Nach der Zusammenführung mit Register 43 wird er noch einmal anders und wird neu gemessen.
- **Neues Abbild** `sperrliste_abbild_2026-09-26.json` `e655c1c8…`. Sonde gegen das alte `40ffe18d…`: Befund genau an 3, 5, 11, 12, 14 und in der Gruppe `eingefroren`. Gegen das neue: 25/0/0, (ii) 0.
- **Abnahme:**
  - Benchmark im Modus `64fb2912…`;
  - ohne Modus 8/8 gleich;
  - Trockenlauf 9 × rc 0;
  - alle Tests grün.

Damit ist dein **Bündel 1** aus 25f (Reste 25d/25e) vollständig: TB-109 für 25e, TB-111 für 25d (2)–(4), TB-110 für den Registerteil.

**Drei Fragen der Sitzung (übernommen, Neigung des steuernden Chats dazu):**
- **(4a)** `datenstand(None)` liest im Modus weiter `BASE_DIR/data`, mit oder ohne TB30A. Die Aufrufer übergeben einen Pfad, und `block()` verlangt ihn im Modus. Soll `datenstand()` im Modus ohne Pfad bei der nächsten Öffnung ebenfalls mit 2 enden? *Neigung:* ja, als Beifang der nächsten Öffnung von `herkunft.py` (kein eigener Auftrag). Eine Funktion mit Ersatzpfad unter dem Modus ist A10-Klasse.
- **(4b)** Der Docstring von `auswertung._abbruch_2` sagt noch „`Abbruch` … endet mit 1“. Der Satz ist falsch geworden und blieb stehen, weil die Freigabe „sonst nichts“ lautete. Streichen mit der nächsten Öffnung oder Tatsachennotiz? *Neigung:* Tatsachennotiz jetzt, Streichung mit der nächsten Öffnung.
- **(4c)** `str(e)` eines gefangenen `Abbruch` ist jetzt `"2"`, die Meldung steht in `e.meldung`. Heute liest niemand `str(e)`. Reicht eine Tatsachennotiz? *Neigung:* ja.

## 4b. TB-112 — 19 über den Laufbereich (42.2 E2, 42.3 F8), db-Sicherung, Aufräumen

- **Befund aus E2 vorher bestätigt (A1):** Im frischen Klon unter dem Modus lief der Import mit einer uncommitteten Änderung in `benchmark.py`, `faltenplan_neun.py` oder `manual_close.py` jeweils **durch (rc 0)**. Die Kontrolle unter `shared/` hielt an (rc 2).
- **Laufbereich (A2):** 81 Module, identisch mit TB-107 F1; 12 davon ausserhalb `shared/`/`strategies/`.
- **Bau (A3):**
  - `ARBEITSBAUM_PFADE` hat jetzt 15 Einträge: die drei alten und die 12 Module als **Einzeldateien**, nicht als Ordner. Grund: `research/vorregistrierung/ergebnisse/` nimmt Laufausgaben auf; als Ordner geprüft, zeigte die Mutation P1 rc 2 schon durch das Protokoll.
  - Neue Konstante `REGISTRIERTE_PROTOKOLLE` als `:(exclude)`, namentlich `herkunft_protokoll.jsonl`.
  - Wirksam nur unter dem Modus, keine neuen Importe.
- **Nachweis (A4, neue Testdatei 26/26):**
  - jede der 12 Dateien einzeln ⇒ rc 2 mit Dateiname;
  - Protokoll neu oder verändert ⇒ rc 0;
  - `data/` und eine Ausgabe unter `ergebnisse/` ⇒ rc 0;
  - die Gegenprobe liest die 81 Module **aus der Messdatei**; die Mutationen beissen.
- **Ohne Modus (A5):** `test_startpruefungen` 44/44 mit 0/0/0 Aufrufen und 144 Pfaden zeichengleich, 8/8 Ausgaben bytegleich.
- **Mit Modus (A6):**
  - Benchmark Repo und Klon `64fb2912…`;
  - Trockenlauf 9 × rc 0;
  - Sonde vorher = nachher, `register()` unverändert;
  - **Lese-Audit: 0 gelesene `.py` unter der Codewurzel ausserhalb der Liste** (Repo 22 178 Zugriffe, Klon 14 572).
- **Pfadliste als Tatsachennotiz** neben der Laufbereichsmessung: `docs/belege/TB-112/arbeitsbaum_pfade.txt` (E2).
- **Nebenbei:**
  - db-Sicherung (25f O6) als Skript: `sqlite3 -readonly .backup`, `integrity_check`, `sha256`, Ziel iCloud. 12 Datenbanken, 0 Schlüsselspalten; der erste echte Lauf rc 0, 12/12 `ok`. Seit 26.09., 14:26 läuft er täglich per Cron (Betreiber, `crontab -l | grep -c db_sicherung` = 1).
  - `tb40_test_*` räumt der Test jetzt selbst ab. Damit ist der Randbefund aus TB-109 erledigt.

**Drei Fragen der Sitzung (übernommen, mit unserer Neigung):**
- **(4d) Eingaben ausserhalb der Liste.** Das Audit findet 10 versionierte Dateien, die der Benchmark als **Daten** liest und die kein Pfad der Sauberkeitsprüfung deckt:
  - `ergebnisse/messgroessen.json` ist durch die Sonde gedeckt (Gruppe `eingefroren`);
  - die neun `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` deckt nichts; sie gehen über die Faltenlängen in den Plan ein (TB-95).

  Eine uncommittete Änderung daran hielte die Startprüfung nicht an. In `ARBEITSBAUM_PFADE` („Laufbereich und seine versionierten Eingaben“), ins Abbild der Sperrliste, oder bindet E2 bewusst nur Code? *Neigung:* ins Abbild (Gruppe `eingefroren`, wie `messgroessen.json`). Sie sind Eingaben mit Hash, keine Code-Pfade, und das Abbild ist der Ort, der Eingaben bindet.
- **(4e) Pflege der Liste.** Die Liste steht als Literal im Resolver; die Gegenprobe liest die Messdatei. Erzeugt der Tag-Commit die Liste aus der Tag-Messung, oder bleibt es beim Literal mit Gegenprobe? *Neigung:* Literal mit Gegenprobe. Am Tag wird gemessen; weicht die Messung ab, ist das ein Befund, kein automatisches Nachziehen.
- **(4f) Schlüssel-Muster der db-Sicherung.** Englisch nach 25f (`key|secret|token|api|passw`), 0 Treffer. Die Tabelle `zustand(schluessel, wert)` in `benachrichtigungen_schliessung.db` trifft es nicht; laut Code enthält sie nur einen Zeitstempel (`erstlauf_am`). Deutsche Wörter mitnehmen? *Neigung:* nein, Tatsachennotiz genügt. Das ist Betrieb, nicht Lauf.

## 4c. Die Betreiberentscheidungen zu deiner 25f (Auswahlkarten, 26.09.2026, 06:35–07:00)

| 25f | Antwort des Betreibers |
|---|---|
| Entsch. 4 Zweck | **„Hobby mit Methode“:** Der Tag ist das Ziel, Live ist optional |
| Entsch. 6 Freigabeklassen | **„Handwerk pauschal“:** Handwerk ohne Sperrlistennähe ist pauschal frei; Registertext, Sperrliste, Live-Code und Reihenfolge nach 36.3 bleiben einzeln |
| Entsch. 7 Fable-Takt | **„Einmal je Tag, gesammelt“**; Registertext als Kopierblock (das ist diese Anfrage) |
| Entsch. 8 P1 | entfällt (Abschnitt 3 (a)); bitte bestätigen |
| Vor dem Tag: O6, V8/F3, F4, W2 | **„Alle“**. O6 ist gebaut und läuft (4b). F4 und W2 liegen als Entwurf im Anhang unten, bitte prüfen. V8/F3 gehen in Stufe VI (Prüfgang mit zweitem und kaltem Leser) |
| Scope-Freeze (C2 H1 Nr. 10) | **„Nein, fallweise“**: Neue Ideen dürfen vor dem Tag Aufträge werden; der Betreiber entscheidet je Fall |
| Bündelung (A3) | **„Ja, Bündel“** |
| Entsch. 1, 2, 3, 5 | nach dem Tag vorlegen |

**Gebündelt wurde so:**
- Bündel 1 (Reste 25d/25e) = TB-109 + TB-111;
- das Register kam mit TB-110 und TB-113;
- der 19-Auftrag = TB-112 (mit O6 und dem Aufräumen als Beifang).

## 5. TB-113 und die Fragen

**TB-113 (Abgabe `0df8c64`, 26.09., 15:39):**
- **Zusammenführung:** `tb-111` nach `main`, Merge `257e7db` ohne Konflikt; die beiden Zweige hatten keine gemeinsam geänderte Datei.
- **Nachgemessen auf dem zusammengeführten Stand:**
  - `herkunft.py` `5bbfc9e0…`, `auswertung.py` `a864b216…`;
  - Sonde gegen das Abbild `e655c1c8…` 25/0/0, (ii) 0;
  - Benchmark im Modus Repo und frischer Klon `64fb2912…`;
  - ohne Modus 8/8 bytegleich;
  - Trockenlauf 9 × rc 0;
  - 17 Testdateien grün.
- **Register 44:** nur Tatsachennotizen: Vollzug von 43-1, 43-4 und 19/E2/F8, das gültige Abbild, die Hash-Übergänge und der Befund A2b. Umfang: numstat 344/0, 13/13 Zitate `diff` rc 0, 7 Marken am alten Ort, keine in Abschnitt 10. `register()` nach dem Merge `469272df…`, nach Register 44 `a0e477fd…`. Die neun Fragen aus TB-109, TB-111 und TB-112 stehen zeichengleich in 44.3.
- **Arbeitsweise:**
  - 22.1: Mac-Sitzungen starten seit heute technisch mit `claude --effort high`. Belegt über `claude --help` und die Prozesszeile; `/status` ist aus der Sitzung nicht lesbar.
  - Neuer Abschnitt 22.9: Die Sitzung wird angelegt, bevor der Einfügesatz kommt.
- Der Hilfsordner `trading-bot-tb111` ist entfernt, der Zweig bleibt.
- ⚠️ **Eine Wechselwirkung, die du kennen solltest:** Die neue Sauberkeitsprüfung bindet `auswertung.py`, aber **nicht `herkunft.py`**, weil kein gemessener Lauf-Typ `herkunft.py` lädt (Laufbereich 81 Module). Eine uncommittete Änderung an `herkunft.py` hielte die Startprüfung heute nicht an. Das ändert sich erst, wenn der Erzeuger `register()`/`commit()` ruft und die Tag-Messung das Modul findet. *Neigung:* keine Änderung jetzt, aber eine Abnahmebedingung des Erzeugers: „Die Laufbereichsmessung nach dem Einbau des Erzeugers enthält `herkunft.py`.“ **Einverstanden?**

**(1) Stummel `None` statt `False` (Berichtigung 43.3).**
- Mit `False` meldet das Werkzeug **ebenfalls 0 Unterschiede**, aber `strategy_paths` legt in **0 von 9** Bots Ordner an statt 9 von 9. Es läuft also den Modus-Zweig.
- Der Fehler wäre am Werkzeug nicht sichtbar gewesen.
- **Bestätigst du `None`?** Soll das Werkzeug zusätzlich den durchlaufenen Zweig prüfen (angelegte Ordner im Wegwerfbaum zählen)? *Unsere Neigung:* ja, als Beifang des nächsten Bündels, nicht als eigener Auftrag (dein 25f A3).

**(2) Reichweite von (iv) im Audit.**
- Gebaut ist: **jeder** lesende Zugriff auf die eigene Ablage steht unter (iv), also die Verzeichnis-Öffnung beim Aufräumen **und** das Lesen des Ergebnis-JSON darin.
- Damit fällt (i) ausserhalb von 31 auf **11**: 9 TB-24-Listen, `messgroessen.json` und die Tempfile-Probe von `mkdtemp`.
- Der Auftrag hatte 21 erwartet, also nur die Verzeichnis-Öffnungen umgeordnet.
- **Welche Lesart meint 25e 3 (b)?** Und gehört die Tempfile-Probe (von `tempfile` angelegt und sofort entfernt, kein `mkdir` im Protokoll) zu (iv)?
- *Unsere Neigung:* die gebaute Lesart, weil beide Zugriffe Lesen der eigenen Ablage sind; die Tempfile-Probe als Tatsachennotiz unter (ii) Umgebung.

**(3) Grenze der Gegenprobe.**
- Sie prüft `__main__`-Blöcke, nicht `main()`-Funktionen; ein `return 0` ohne Ausgabe in `main()` fände sie nicht.
- **Erweiterung jetzt, oder reicht dein Satz aus 25e (2)** *„der Erzeuger schreibt für eine Zelle ohne Trades die Nullzeile, nie nichts“* als Abnahmebedingung des Erzeugers?
- *Unsere Neigung:* das Zweite. Nach deiner 25f A3 („eine Gegenprobe je Klasse, nicht je Stelle“) gehört die Prüfung in die Abnahme des Erzeugers.

**(4) Bestätigungen zu 25f:** Entscheidung 8 entfällt (3 (a)); Verweis N = 653 nach dem Tag (3 (b)).

**(5) Die Fragen aus TB-111 und TB-112:** (4a)–(4f) oben.

**(6) Nullbefund-Skizze (F4) und Budget (W2):** siehe Anhang. Reicht die Skizze als Vorbereitung vor dem Tag, oder soll ein Teil davon, etwa „keine Rettungsanalysen auf dem Selektionsraum“, vorher als Registertext stehen?

## Anhang A — Nullbefund-Skizze (F4) und Werkzeugkosten-Budget (W2), Entwurf des steuernden Chats

*Entwurf des steuernden Chats, 26.09.2026, 07:40, beauftragt durch die Betreiberkarte R5 („Alle“). Fable prüft ihn in der Tagesanfrage 26a. Das ist **kein Registertext**: Er beschreibt, was das Register für den Fall schon sagt, und was danach kommt. Keine Ergebnisgrösse, keine Erwartung über den Ausgang.*

---

### Teil 1 — Nullbefund-Skizze: Was geschieht, wenn kein Bot die Schwelle schafft

#### 1. Was das Register für diesen Fall schon festlegt (wörtlich, mit Fundstelle)

| Regel | Fundstelle |
|---|---|
| *„Dieses Ergebnis ist zulässig: Es kann sein, dass kein einziger Bot die Schwelle erreicht. Eine Aussage über den **Backtest**, nicht über die Bots.“* | Festlegung 12, Abschnitt 1 |
| *„Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu ändern.“* | 7.1 |
| *„Das **Kapital** geht in eine **statische Benchmark-Position** in Höhe des mittleren Exposures — nicht in Kasse, nicht zu den Überlebenden.“* | 7.1 |
| *„Der Bot läuft **als Schatten weiter**, kehrt nur über einen **neuen vorregistrierten Lauf mit veränderter Hypothese** zurück. **Kein ‚vorerst behalten‘.**“* | 7.1 |
| Stufe nach dem Lauf: wer ein Abbruchkriterium erfüllt, steht auf **Schatten**; *„Die Zuweisung ist Ergebnis des eingefrorenen Skripts, keine Lesung.“* | 16.4 (b) |
| *„**Wird die Zelle inaktiv, geht ihr Budget in die statische Benchmark-Position ihrer Anlage — nicht an andere Zellen.**“* | 16.4 (j) |

**Folge für „alle neun gehen“:**
- Alle vier Zellen sind inaktiv.
- Das Buch hält je Anlage die statische Benchmark-Position (Aktien 80 / Krypto 20 nach 16.4 (l)).
- Alle neun Bots laufen als Schatten im Paper-Betrieb weiter.
- Nichts davon verlangt eine neue Entscheidung, alles steht schon im Register.

#### 2. Was am Tag des Berichts geschieht (Ablauf)

1. Der Bericht erscheint vollständig, mit dem Satz aus Festlegung 12 am Ende jeder Bleibt-Geht-Liste (Abschnitt 1, `auswertung.py`).
2. Der steuernde Chat liest ihn zuerst. Fable liest ihn nach Aufhebung des Sichtschutzes (25f F5).
3. **Keine Rettungsanalysen auf dem Selektionsraum.** Zulässig sind nur die schon vorgemerkten Messbitten „nach dem Tag“ aus 25f (PBO je Bot, MinTRL, Kosten-Sensitivität, Liquiditätsdrittel), alle als Bericht, keine als Nachverhandlung.
4. Die Registereinträge des Tages schreiben den Befund fest. Die Schatten-Stufe setzt das Skript, nicht eine Lesung.

#### 3. Der Anschluss: Durchgang 2 (Betreiberentscheidung R4 „Hobby mit Methode“)

Ein Nullbefund ist nach R4 kein Projektende, sondern der Eingang zum zweiten Durchgang. Er hat schon heute eine Liste, und keiner ihrer Punkte hängt am Ausgang dieses Laufs (25f Teil C):

| Baustein | Grund | Fundstelle |
|---|---|---|
| Point-in-Time-Universen (Aktien und Krypto) | Das Register benennt die heutigen Listen als Grenze | 25f D1/D2; Register 15.5 (Registertext 3, (d)) und 16.1.2 |
| Kostenmodell je Ausführungsstelle | Binance ist seit 1.7.2026 für EU-Kunden keine Ausführungsstelle | 25f K1/K2 |
| PBO/CPCV und MinTRL als Bericht | Verteilung statt eines Pfades; ehrliche Lesart der Bestätigung | 25f V3/V7 |
| Baukasten und Trials-Log | Durchgang 2 in Wochen statt Monaten; N zählt alles | 25f V1/V2 |
| Je eine neue Hypothese, nicht alle zugleich | N | 25f C2 Horizont 3 |

**Nicht Teil des Anschlusses:** eine geänderte Schwelle für dieselben Bots auf denselben Daten. Das wäre nach 7.1 ausgeschlossen, und eine *„veränderte Hypothese“* ist mehr als eine andere Zahl.

#### 4. Offene Frage an Fable

Reicht diese Skizze als Vorbereitung vor dem Tag, oder soll ein Teil davon (etwa Abschnitt 2 Nr. 3, „keine Rettungsanalysen“) vorher als Registertext stehen?

---

### Teil 2 — Werkzeugkosten als Jahresbudget (W2)

*Zahlen aus Fable 25f, B7 W2, mit Fables Quellen. **Grössenordnungen, keine Rechnung:** Der Betreiber trägt die tatsächlichen Beträge in die letzte Spalte ein.*

| Posten | Fable 25f (Grössenordnung, Quelle dort) | heute nötig? (nach R4 „Hobby mit Methode“) | tatsächlich (Betreiber) |
|---|---|---|---|
| KI-Nutzung (Claude-Abo) | 100–200 $/Monat | ja | |
| Datenquelle für Durchgang 2 (EODHD bzw. Norgate) | 200–650 USD/Jahr | erst mit Durchgang 2 | |
| Server/VM (Hetzner CX23) | 5,49 €/Monat | nur falls vorhanden | |
| Steuertool (CoinTracking/Blockpit) | 40–130 €/Jahr | erst bei Live-Handel | |
| Handelsgebühren | (in den Kostenmodellen, nicht hier) | Paper: 0 | |
| **Summe (Fable)** | **2 000–4 000 €/Jahr**, davon mehr als die Hälfte KI-Abos | | |

**Einordnung (Fable 25f W4, ohne Ertragsaussage):** Bei „Hobby mit Methode“ ist das Budget ein Hobbybudget. Es steht keiner Ertragserwartung gegenüber und braucht keine; der Posten ist aufgeschrieben, damit er sichtbar ist.

## Anhang B — AF-F0: Bestandsaufnahme für das Epic „Forschungspipeline“ (Betreiberkarte 26.09., 15:30: „AF-F0 jetzt, nur lesend“)

Die Datei liegt in der Projektablage: `projektfuehrung/AF-F0_BESTANDSAUFNAHME_2026-09-26.md`. Gemessen am Stand `257e7db`, nur lesend.

**Kurz:** Das Projekt hat, was die Vorlage „Registry, Data Version, Code Version, Experiment-IDs, Adversarial Review“ nennt, und zwar strenger als verlangt. Es fehlen:
- eine gemeinsame Strategie-Schnittstelle, denn jeder Bot ist ein eigener Ordner;
- ein maschinenlesbarer Versuchszähler über Zyklen;
- CI; Docker und ein Job-System gibt es ebenfalls nicht.

Das Epic bleibt hinter dem Tag geparkt. **Fünf Architekturfragen, zu entscheiden nach dem Tag, heute nur zur Kenntnis:**
1. **Strategie-Schnittstelle:** die neun heben oder neue Strategien in eigener Schnittstelle? *Neigung:* neu, die neun bleiben unberührt.
2. **Versuchszähler:** das Versuchsregister (TB-29) zum Trials-Log erweitern (deine V2) oder neu? Zählt ein Zyklus mit N = 1 ins N des nächsten Durchgangs?
3. **Zeitanker je Zyklus:** Registerabschnitt nach Baukasten (V1) mit Commit-Hash, oder je Zyklus ein signierter Tag?
4. **Speicher:** SQLite je Zyklus oder gemeinsame Registry-Datenbank?
5. **CI:** Mutations- und Registerproben bei jedem Push, als erster Baustein ohne Laufberührung?

---

## In einfacher Sprache

Heute und in der Nacht sind fünf Aufträge fertig geworden:
- **Keine Geschäfte:** Die zehn Stellen, die bei „keine Geschäfte“ still aufgehört haben, melden das im geschützten Modus jetzt als Fehler.
- **Zwei Programme:** Die Auswertung kennt nur noch zwei Ausgänge, und das Protokoll-Programm schaut im geschützten Modus in die eingefrorenen Daten.
- **Startprüfung:** Sie deckt jetzt alle Programme ab, die im Lauf mitlaufen.
- **Sicherung:** Die Paper-Datenbanken werden täglich nach iCloud gesichert.
- **Regelwerk:** Deine Antworten und alles Umgesetzte stehen dort, Abschnitte 43 und 44.

Von deinen Vorschlägen aus der Gesamtanalyse hat der Betreiber übernommen:
- eine gesammelte Anfrage je Tag;
- pauschale Freigabe für kleine Handwerksarbeit;
- gebündelte Aufträge;
- alle vier billigen Dinge vor dem Tag.

Als Zweck gilt „Hobby mit Methode“. Einen Stopp für neue Themen bis zum Tag wollte er nicht.

Für dich bleiben dreizehn kleine Fragen und zwei Entwürfe zur Prüfung: die Seite „was, wenn kein Bot besteht“ und das Kostenbudget. Die Bestandsaufnahme für die Forschungspipeline ist nur zur Kenntnis dabei.
