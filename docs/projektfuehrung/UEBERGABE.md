# UEBERGABE — Stand des steuernden Chats (ab 30.09.2026, 19:13)

> ⚠️ **Ältere Blöcke (25.09. bis 30.09.2026 vor 19:13) stehen in `UEBERGABE_ARCHIV.md`** (nur Repo; abgetrennt am 30.09.2026, T5). Fundstellen „UEBERGABE.md, Nachtrag …“ mit älterem Datum sind dort zu lesen. In der Fable-Ablage liegt nur diese Datei.

---

## Nachtrag 30.09.2026, 19:13 — Betreiberentscheide zu Karten und Tokensparen (Wortlaut für ARBEITSWEISE 0/6d/22.10 und UMZUG, bei E-2 einzuarbeiten)

*Anlass: Der Betreiber hat gefragt: „prüfe vor dem Umzug … ob wir irgendwas noch optimieren können um token zu sparen ohne dem Projekt zu schaden … du hängst dich immer am multiple Choice auf“. Der steuernde Chat hat Vorschläge gemacht, der Betreiber hat geantwortet: „Wir setzten es wie von dir Vorgeschlagen um“ (19:13). Damit gilt 1a · 2a · 3a · 4a. Ausnahmsweise kam die Abfrage als nummerierte Liste im Text, weil es um die Kartenregel selbst ging.*

**Karten (schränkt die Kartenregel vom 19./20./23.09. ein):**
- **M1:** Die Karte ist immer der letzte Schritt einer Antwort. Ergebnis, Dateien, Kopierblöcke, „Deine Aufgaben“ und Ampel sind vorher zugestellt (`SendUserMessage`). Hängt die Karte, fehlt nur die Karte.
- **M2:** Höchstens eine Karte je Antwort, bis zu vier Fragen gebündelt.
- **M3:** Karten nur für echte Betreiberentscheide:
  - Freigaben für Register, Sperrliste, Signalpfad und Parameterdateien;
  - Löschen und Ablage entfernen, Umzug, Geld, Unumkehrbares.
  - Bei Handwerk entscheidet der steuernde Chat selbst und schreibt: „Vorgabe: X — gilt, wenn du nicht widersprichst“.

**Tokens:**
- **T1:** Helfer schreiben ihren Volltext in eine Datei (Scratchpad oder Ausgabeordner). Dem Chat geben sie nur rund 20 Zeilen zurück: Urteile, Abweichungen, Offenes.
- **T2:** Gegenlesen gestuft:
  - Zwei unabhängige Parallelläufe nur für Zahlen und Zitate, die ins Register oder an Fable gehen.
  - Sonst ein Gegenleser auf das fertige Ergebnis.
  - Gemessen 29./30.09.: fünf Helferläufe ≈ 1,03 Mio. Tokens. Der einzelne Ergebnis-Gegenleser (168 000) fand 3 MUSS-Befunde.
- **T3:** Helfer bekommen Zeilenbereiche aus `REGISTER_INDEX.md` und die bekannten Fundstellen mit. Das Register hat 10 347 Zeilen; Helfer brauchten 38–77 Aufrufe.
- **T4:** Sonnet-Probe beim nächsten Fundstellen-Check: Sonnet und Opus parallel, dann Vergleich.
- **T5:** Fable-Ablage entschlacken. Liste siehe Umzugsblock, Block 4 Nr. 3; die Entscheidung per Karte. UEBERGABE.md bekommt eine Archivdatei, in der Ablage bleibt nur der letzte Block.
- **T6:** Kürzere Antworten. „In einfacher Sprache“ ausführlich nur in Dokumenten, im Chat ein bis zwei Zeilen.
- **T7:** Jede neue Fassung wird unter einem neuen Stage-Pfad abgelegt (das ist Block 7 Nr. 2 vom 29.09.; am 30.09. erneut gebraucht).

**Sachentscheide:**
- TB-122 **F1** (Scanbeginn der Breakout-Bots an `WARMUP_PERIOD`) geht in **TB-124**: Nachweis wie in TB-122, Hash-Übergang als Tatsachennotiz.
- **F3** (`SMA_TREND_PERIOD` nach `live_params.py`) bleibt so; Fables R47 regelt es in E-2.

## Umzug 30.09.2026 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

*Geschrieben vom steuernden Chat (29.09., ca. 20:55, bis 30.09.). Anlass: Der Betreiber fragt „vor dem Umzug“, die Ampel steht bei geschätzt rund 150 000. „Gemessen“ heisst: über die Geräteanbindung heute gemessen.*

⚠️ **Ausnahme von UMZUG 3, wie am 29.09.:** Vier Dateien sind uncommittet (Block 2). Sie liegen auf dem Mac-Datenträger; Schritt 0 von TB-124 nimmt sie mit.

### Block 1 — Stand in drei Zeilen

- **Fertig:**
  - Vormessungen zu 27c/29b: `VORMESSUNG_E-2_2026-09-29.md` samt Nachtrag vom 30.09.
  - Vorprüfung nach dem Fable-Filter: acht Punkte, zwei Helfer unabhängig.
  - `FABLE_ANFRAGE_2026-09-30a_vorgepruefte_fragen_e2.md`, drei Fragen, vom Gegenleser geprüft (16 Befunde eingearbeitet).
  - Die Betreiberentscheide vom 30.09. (Nachtrag oben).
- **Läuft:** nichts. Keine Mac-Sitzung. 30a liegt beim Betreiber zum Weitergeben an Fable (bestehender Chat).
- **Als Nächstes:** Auftrag TB-124 schreiben (Block 4 Nr. 1). Dann E-2 vorbereiten, soweit es nicht an 30a hängt.

### Block 2 — HEAD und Commits

- **HEAD `0034960` = Stand 29.09.**, gemessen 30.09. Keine Commits seit dem Umzug vom 29.09.
- **Uncommittet, gemessen:**
  - `docs/projektfuehrung/UEBERGABE.md`: nur angehängt (29.09. und dieser Block).
  - `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` (6/1 aus dem 29.09.).
  - `docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md`: md5 `2df16c49…`, 8 602 B.
  - `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-30a_vorgepruefte_fragen_e2.md`: md5 `6ec10ae9…`, 9 734 B.
- ⚠️ Auf dem Mac liegen weiterhin zwei Worktrees von TB-123 (`$TMPDIR/tb123_vorher`, `$TMPDIR/tb123_vorher2`); siehe Block 4 Nr. 1.
- `FABLE_DIALOG_INDEX.md` kennt 30a noch nicht. Das geht in Schritt 0 von TB-124, mit `dialog_index.py --handfelder`, danach `--pruefen`.

### Block 3 — Tragende Zahlen

- Unverändert gegenüber Block 3 vom 29.09.: Register `18e39ee2…`, Abbild `46f0ad5d…`, `herkunft.register()` `01f5997a…`, Snapshot und Datenstand wie dort.
- `BACKLOG.md`: 220 Zeilen, md5 `2a6e5dd2…`.
- **Ablage:** 50 Dateien, `knowledge_size` 792 990 von 2 000 000 (30.09.).
- **Nummern:** TB frei ab **124** · Journal frei ab **DV** · R-Blöcke frei ab **R53** · Fable-Anfrage **30a vergeben**, frei ab 30b bzw. am nächsten Tag **a**.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-124 (Mac, Handwerk; F1 per Betreiberentscheid 30.09. freigegeben).**
   - Schritt 0: die vier uncommitteten Dateien committen, `FABLE_DIALOG_INDEX.md` um 30a nachziehen.
   - `research/sync_check/sync_table.py` nachziehen, bis `test_sync_check` 33/0 zeigt (Test nicht schwächen; Beleg `docs/belege/TB-123/a3_sync_probe.txt`).
   - Die zwei Worktrees entfernen.
   - Datenstand messen.
   - **F1:**
     - Scanbeginn in beiden `backtest_breakout.py` (`strategies/volatility_breakout/backtest_breakout.py:114, :155`; `strategies/volatility_breakout_crypto/backtest_breakout.py:81, :114`) an die Achse `bb_lookback` binden.
     - Nachweis wie TB-122: mit Voreinstellungen bytegleich, dazu eine Wertprobe mit den kleinen Stufen (Krypto 20 nach REG:255; Aktien 97 nach REG:280).
     - Hash-Übergang als Tatsachennotiz nach 37.3.
   - **R28-Handwerk:** Probe `shared/snapshot.py::VERANKERTER_DATENSTAND` gegen Register 18, wie J-r für `auswertung.py`.
   - Vorher Gegenleser (T2: einer, auf den fertigen Auftrag).
2. **Fable 30a.** Die Antwort wird hier gelesen und bewertet (ARBEITSWEISE 5b).
   - Frage 1: Vorlauf 4a (i) → Faltenplan.
   - Frage 2: Summe oder Verkettung → 2a / R48 (g).
   - Frage 3: 7 (d) bei leerer Menge.
   - Erst danach gehen R48 (c)(g) und der Faltenplan-Vorlauf in E-2.
3. **T5, Ablage entschlacken — Karte an den Betreiber (M3).**
   - **Kandidaten „nur Repo“**, abgeschlossen oder überholt, zusammen 364 040 B (Bytes im Repo gemessen; die Ablage zählt anders, deshalb keine Umrechnung in Tokens):
     - 25f Antwort (112 639) und Anfrage (8 577);
     - 27a Antwort (30 836) und Anfrage (9 484);
     - 27b Antwort (36 823) und Anfrage (10 632);
     - `FABLE_UEBERGABE_2026-09-24` (19 507);
     - `LOESCHLISTE_TB-118` (27 592);
     - `MAC_TB-117`, `-118`, `-121`, `-122` (45 390);
     - `AUFGABEN_BETREIBER_2026-09-26`, `PROJEKTSTAND_2026-09-26`, `PRUEFUNG_2026-09-25` (19 049);
     - `FABLE_WOCHENRUECKMELDUNG_2026-09-22` (10 943);
     - `BACKLOG_NACHTRAG_2026-09-18` (17 679);
     - `RECHERCHE_vintage_datenlage` (14 889).
   - **Dazu:** UEBERGABE in der Ablage nur mit dem letzten Block (heute 92 564 B für 27 Blöcke), der Rest in `UEBERGABE_ARCHIV.md` nur im Repo.
   - **Bleibt:**
     - Registerkopie Teil 1–4 (747 539 B; die braucht Fable);
     - ARBEITSWEISE, UMZUG, PRUEFPRINZIPIEN, DOKUMENTATIONSSTANDARD, REGISTER_INDEX, FABLE_DIALOG_INDEX;
     - 27c und 29b (bis E-2);
     - TB-30b-Bestandsaufnahme und Nachträge (Posten 4/5 offen).
   - **Zu prüfen, nicht entschieden:** Warum `BACKLOG.md` (53 236 B) in der Ablage liegt, obwohl Fable sie vor dem Tag nicht liest (Sichtschutz 27). Die Fundstelle wäre das Konzept 27b / TB-118.
   - **Preis:** Fable findet Altes nicht mehr selbst, sondern nur über Fundstellen.
4. **E-2 vorbereiten.** Inhalt siehe Block 4 Nr. 1 vom 29.09. Neu:
   - Vormessungen erledigt;
   - Tatsachennotizen zu R25 (Z. 53–62), R26 (TB-117 E), R41 (Zeitstempeldifferenz; Neurechnung nach 41.3 C2 als Mac-Messung), R48 (f), R49 (b), R50 (Orte);
   - Regelwerksnachträge zusätzlich M1–M3 und T1–T7 (Nachtrag oben).
5. **Fable-Umzug** nach E-2 (Ampel bei Fable 🟡, ~380 000, Stand 29.09.).
6. Später: E-6 (Posten 4), E-3/E-4 (R44), Posten 5 neu fassen (R43), Leiter-Skript Stufe IV, Öffnung `paths.py` (T117-5, E-9). Nebenbefund DSR-Einheiten (`kennzahlen.py:222–224`) vor R50 prüfen.

### Block 5 — Wartezustände

| wartet | auf |
|---|---|
| Fable 30a | Betreiber gibt die Anfrage weiter (Kopierblock kam am 30.09. im alten Chat); dann Fables Antwort |
| TB-124 | Auftrag durch den steuernden Chat, dann `starte_TB-124` |
| T5 | Karte an den Betreiber |
| Betreiber | Speicher-Export: Frist 29.09. abgelaufen; `docs/archiv/` gibt es nicht (gemessen 30.09., 16:23); ob er gemacht wurde, ist nicht bekannt |

### Block 6 — Freigaben und Entscheide

- **Neu frei (30.09.):** F1 in TB-124 (zwei Signalpfad-Dateien `backtest_breakout.py`).
- **Pauschal frei:** Handwerk ohne Sperrlistennähe (26.09.).
- **Nicht freigegeben:** E-2 (Register), E-3 … E-9, jede Öffnung von `herkunft.py`, `paths.py`, `zuteilung.py`, `auswertung.py`, `kennzahlen.py` (`EINGEFROREN`), F3.
- **Entscheide 30.09.:** M1–M3, T1–T7, F1 → TB-124, F3 so lassen (Nachtrag oben).

### Block 7 — Fehler dieses Chats und die Regeln daraus

| # | Fehler | ⇒ Regel |
|---|---|---|
| 1 | `git status --short` über die Brücke (29.09., erster Beleg) | Bleibt verboten (ARBEITSWEISE 14, Regel 4); nur `rev-parse`, `log`, `show`, md5 |
| 2 | `device_commit_files` meldete „written“, auf dem Gerät lag die alte Fassung (Vormessung, 7 310 statt 8 602 B) | T7; die md5-Probe hat es gefangen |
| 3 | Antwort brach nach dem Dateiversand ab: keine Karte, keine Aufgaben, keine Ampel | M1 |
| 4 | Fable-Anfrage 30a nur als Datei gegeben, nicht als Kopierblock (Regel 19.09., Rüge 24.09.) | Vor dem Absenden prüfen: Steht der volle Text als Kopierblock in DIESER Antwort? Im alten Chat am 30.09. nachgeholt |
| 5 | Vormessung meldete R48 (g) als direkten Widerspruch zwischen Register und Code; das war zu stark | Vor dem Urteil „Widerspruch“ prüfen, ob die Registerstelle den gerechneten Fall wörtlich trifft (Nachtrag Vormessung, Abschnitt 4) |

Weiter gültig: Block 7 vom 29.09. (20:48) samt Kurzfassung.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die vier uncommitteten Dateien aus Block 2 (Schritt 0 von TB-124).
- Die Regeltexte vom 29.09. und 30.09. stehen nur in UEBERGABE und in der Erinnerung, nicht in ARBEITSWEISE/UMZUG (E-2).
- Helferberichte vom 29./30.09.: Die Volltexte liegen nur im alten Chat; ihre Ergebnisse stehen in der Vormessung und in 30a.

### Block 9 — Eröffnungstext

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt.

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Wenn das nicht geht, sag es ausdrücklich, denn dann müssen wir Messungen wieder über mich laufen lassen.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter (project_read liefert immer die ganze Datei):
1. docs/projektfuehrung/UEBERGABE.md — ab der Überschrift „## Nachtrag 30.09.2026, 19:13“ bis Dateiende (Nachtrag und Umzugsblock 30.09.). Ältere Blöcke nur bei Bedarf.
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
Nur wenn die Geräteanbindung fehlt: dieselben Stellen über den Projects-Zugriff (projektfuehrung/…).

Die Regeln vom 29. und 30.09. (u. a. Umzugsampel, Fable-Filter, Karten nach M1–M3, Tokensparen T1–T7, md5 nach jedem Ablegen) stehen in der Erinnerung und in UEBERGABE; in ARBEITSWEISE und UMZUG sind sie noch nicht eingearbeitet — das ist Teil von E-2. PRUEFPRINZIPIEN.md (docs/PRUEFPRINZIPIEN.md) und BACKLOG.md gezielt nachlesen, wenn der Anlass kommt. Grosse Dateien über einen Helfer lesen, der nur eine Kurzfassung zurückgibt.

Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt, und was gerade auf wen wartet. Fang danach in derselben Antwort mit dem ersten Handwerksschritt an.
```

**Stehende Pflichten (Kurzfassung):**
- Umzugsampel als letzte Zeile.
- Helfer nach T1–T3, Gegenleser nach T2.
- An Fable nur vorgeprüfte Verfahrensfragen, als Kopierblock.
- Karten nach M1–M3.
- Aufträge per `starte_TB-<n>`, Wächter-Log prüfen, Nachschau per `send_later`.
- Befehle für den Betreiber je eine Zeile; der Einfügesatz steht am Schluss im Kopierfeld.
- Mac-Sitzungen mit Aufwand hoch.

## Nachtrag 30.09.2026, ca. 19:50 — neuer steuernder Chat: Übernahme, Kartenentscheide, TB-124 gestartet

*Geschrieben vom neuen steuernden Chat (Übernahme 19:24). „Gemessen“ heisst: über die Geräteanbindung.*

- **Brücke geht.** HEAD `0034960`, `BACKLOG.md` 220 Zeilen, md5 `2a6e5dd2…` = Block 3. md5 der Vormessung (`2df16c49…`, 8 602 B) und von 30a (`6ec10ae9…`, 9 734 B) = Block 2.
- ⚠️ **Fehler Nr. 6 (Fortsetzung von Block 7):** Die erste Messung lief als `git status --short` über die Brücke, vor dem Lesen der Kernlektüre. Die Brücke darf nicht löschen, deshalb blieb eine leere `.git/index.lock` liegen, die jeden git-Befehl blockiert hätte. Sie wurde umbenannt in `.git/index.lock.verwaist_claude_2026-09-30`, nicht gelöscht; TB-124 0b räumt sie weg. ⇒ **Regel:** Schon die allererste Brückenmessung verwendet nur `git --no-optional-locks …` (`rev-parse`, `log`, `ls-files`, `diff --name-only`, `worktree list`). Der Eröffnungstext beim nächsten Umzug nennt das im ersten Absatz.
- **Berichtigung Block 4 Nr. 1:** Die Krypto-Stufe 20 steht in Register **Z. 265**, nicht Z. 255 (Z. 255 ist `t3_supertrend`). Die Aktien-Stufen 20 und 97 stehen in Z. 280.
- **Worktrees:** `tb123_vorher` und `tb123_vorher2` sind laut `git worktree list` schon `prunable` (Ordner weg). TB-124 0b macht `git worktree prune`.
- **Betreiberentscheide 30.09.2026, ca. 19:44, per Auswahlkarte:**
  - **F1-Tests:** „Ja, zwei Testdateien (Empfohlen)“. Die zwei `test_posten3_durchreichung.py` der Breakout-Bots werden erweitert. Wortlaut im Auftrag TB-124.
  - **T5:** „Wie vorgeschlagen (Empfohlen)“. ⚠️ Auf der Karte stand „21 Dateien“; richtig sind **18 Dateien**, 364 040 B (Liste Block 4 Nr. 3, nachgezählt).
- **T5 im Repo vollzogen:** `UEBERGABE.md` geteilt. Z. 1–1026 der alten Datei (md5 `a0227fd6…`, 105 480 B) stehen byte-gleich in `UEBERGABE_ARCHIV.md` (nur Repo). Diese Datei beginnt mit dem Nachtrag 30.09., 19:13. Die Probe „Archivteil + Rest = alte Datei“ ist bestanden. Das Entfernen der 18 Dateien aus der Ablage und das Ersetzen von UEBERGABE dort macht der Betreiber von Hand; dieser Chat hat keinen Ablage-Zugriff (kein `project_info`/`project_read`).
- **Fable 30a:** Der Betreiber meldete um 19:28 „fable fertig“. Die Antwort liegt in der Ablage und ist hier nicht lesbar; der Anhang ist angefordert. ⚠️ Sie kommt erst **nach dem Schritt-0-Commit von TB-124** ins Repo, sonst weicht TB-124 0a ab.
- **TB-124:** Auftrag `docs/auftraege/MAC_TB-124_scanbeginn_sync_r28.md`, vom Gegenleser geprüft (7 MUSS eingearbeitet, tragende Stellen selbst nachgelesen). Befund daraus: Bei der Voreinstellung 126 war der Scanbeginn 127 nie bindend (frühester Einstieg Balken 145); F1 wirkt nur bei den Stufen 20 (Balken 39–126) und 97 (116–126).
- ⚠️ **Fehler Nr. 2 erneut (30.09., ca. 19:57):** `device_commit_files` meldete „written“, auf dem Gerät lagen aber 24 859 B statt 25 660 B (ein Zwischenstand von Stage-Pfad `tb124_v3`). Die md5-Probe hat es gefangen. Neu abgelegt über `tb124_v4`, md5 `0740787c…` auf beiden Seiten. ⇒ T7 gilt auch, wenn eine Datei unter einem **schon benutzten** Stage-Pfad nach dem ersten Ablegen noch bearbeitet wurde: für jede Ablage ein frischer Pfad.

## Nachtrag 30.09.2026, ca. 20:20 — Fable 30a eingegangen und bewertet (ARBEITSWEISE 5b); Nachtrag 1 zu TB-124

- **Eingang:** Der Betreiber hängte die Antwort um 19:54 als Chat-Anhang an. Sie liegt byte-gleich als `FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md` im Repo (12 925 B, md5 `f9cdbbef…`). ⚠️ Das ist eine Abschrift aus einem `.txt`-Anhang: Die Markdown-Auszeichnung (Überschriften, Fettungen) fehlt. Der Dateiname ist vom steuernden Chat gesetzt, der Name in der Ablage ist unbekannt. **Vor E-2 werden R53–R55 zeichengleich gegen die Datei in der Ablage geprüft** (Regel 4 vom 29.09.: Abschriften zweifach, `cmp`).
- **Bewertung:**
  - Frage 1 (R53): einverstanden, übernehmen. Folge für TB-124: Der Scanbeginn der Zelle liegt nie vor ihrem Vorlauf.
    - B1 des Auftrags (L + 1) hätte das verletzt. Berichtigt mit `NACHTRAG_1_MAC_TB-124_scanbeginn_vorlauf.md` auf `BB_PERIOD + L − 1`; Code gemessen: `rolling` ohne `min_periods`.
    - Mit der Voreinstellung wird der Scanbeginn 145 statt 127; bytegleich erwartet, weil vorher kein Einstieg möglich ist.
    - Offen für E-2: Wörtlich addiert gibt R53 L + 20 Balken, hergeleitet sind es L + 19 (zwei Fenster teilen einen Balken). Das ist eine Frage der Zählweise, keine Fable-Frage, solange die Herleitung aus dem Code trägt.
  - Frage 2 (R54): einverstanden, übernehmen. Das deckt sich mit dem Nachtrag der Vormessung (kein direkter Widerspruch; aufgelöst auf der Registerseite). Messbitte `netto_rendite_pct` (Leser?) vor E-2.
  - Frage 3 (R55): einverstanden, übernehmen. Probe „leere Menge“ als Handwerk (BACKLOG).
  - Sichtschutz: Die Faltenjahre in Frage 1 sind Verfahrensmessung nach 27.2. Keine Ergebnisgrösse gelesen.
- ⚠️ **Fables Ampel:** Fable meldet „🟡 · ca. 450 000“. Nach den Schwellen vom 29.09. (🔴 über 300 000) ist das **🔴**. Fables Plan „Umzug beim nächsten Registerauftrag (E-2)“ passt trotzdem: Vor E-2 ist keine Fable-Anfrage geplant. Regel: **Vor der nächsten Anfrage an Fable wird Fable umgezogen.** Fables Umzugshinweis zu Abschnitt 6/7 der Vorlage übernehmen.
- **Nummern:** R-Blöcke frei ab **R56** · Fable-Anfrage frei ab 30b bzw. am nächsten Tag a.
- **An die laufende Sitzung TB-124:** Die Sitzung liest den Nachtrag 1 nur auf Hinweis. Der Betreiber schickt ihr dafür einen Satz in die Gerätesitzung (Kopierblock im Chat). Den Nachtrag 1, die Antwort 30a, `docs/belege/TB-124/0c_handfelder.json` und diesen Nachtrag committet sie mit ihrem nächsten Commit. BACKLOG-Block „Aus Fable 30a“ und der Satz im Journal DV stehen im Nachtrag 1.

## Nachtrag 30.09.2026, ca. 22:05 — E-2-Vorbereitung: Schnitt, Inventar (T4-Probe), Auftrag TB-125 entworfen

- **Messbitten aus 30a erledigt** (Nachtrag in `VORMESSUNG_E-2_2026-09-29.md`, ca. 20:15):
  - R54: `netto_rendite_pct` ist eine Berichtsgrösse ohne Leser im Urteil.
  - R53: Stufen und Bollinger-Fenster sind aus `registerdaten.py` lesbar, weitere feste Fenster nicht.
- **Schnitt E-2 (Handwerk, Vorgabe des steuernden Chats, dem Betreiber genannt):**
  - **TB-125:** Regelwerk-Nachtrag (ARBEITSWEISE, UMZUG, BACKLOG K4s/K4t), pauschal frei, als Sonnet-Probe nach dem Entscheid 29.09., 14:05.
  - **TB-126:** Register (R18–R55, Tatsachennotizen TB-122/TB-124), Einzelfreigabe per Karte.
  - Grund: verschiedene Freigabeklassen, keine Abhängigkeit; das Regelwerk liest jeder neue Chat zuerst.
- **T4-Probe (Fundstellen-Check), E-2-Inventar, Sonnet und Opus parallel mit demselben Helferauftrag, ca. 21:45:**
  - Beide fanden 38 R-Blöcke R18–R55 ohne Lücke und ohne Dopplung (27c: 15, 29b: 20, 30a: 3). Die Voraussetzungen im Block benannten beide gleich.
  - Regeln für ARBEITSWEISE/UMZUG: Sonnet zählte 45 gültige, Opus 54. Das ist verschiedene Körnung; Opus fand vier weitere in Nachträgen ausserhalb der Quellenliste. Befund gleich: praktisch nichts eingearbeitet, beide Dateien zuletzt am 27.09. geändert (`aab641e`).
  - Aufwand laut Werkzeugrückmeldung: Sonnet ~253 000 Tokens, 39 Aufrufe, ~9 min; Opus ~196 000 Tokens, 25 Aufrufe, ~5 min.
  - ⇒ Sonnet war hier nicht billiger. Eine Probe, keine Regel.
  - Volltexte nur im Arbeitsordner des Chats, nicht im Repo.
- **TB-125 entworfen:**
  - 24 Einfügungen mit Anker, jeder Anker am Arbeitsbaum vorgezählt (genau 1).
  - Der Gegenleser fand 8 MUSS-Befunde, alle eingearbeitet, u. a.:
    - falsche Zuordnungen und Zeitangaben;
    - „zweimal“ statt dreimal;
    - der Zeiger der Kopierblock-Regel (ARBEITSWEISE 15, Austausch Nr. 5). Die Zeile „als Datei, nie als Chat-Text“ in Abschnitt 0 bekommt deshalb eine Ausnahme (E24).
  - ⚠️ Der Wächter startet ohne Modellwahl. **Vorgabe:** Der Betreiber setzt `/model sonnet` in der Sitzung, Schritt 0 hält das Modell fest; läuft Opus, zählt es nicht als Probe.
  - Abgelegt wird TB-125 erst, wenn TB-124 geschlossen ist.
- **Nicht in TB-125, weil ohne vorbereiteten Wortlaut:** K2h/K2f (PRUEFPRINZIPIEN), die drei Trägerstellen (TB-119 Nr. 2), der kalte Leser ohne Gedächtnis, Fable 29a Abschnitt 1–3, die Regel „`project_info`“ (Block 9 vom 29.09., 07:15).

## Umzug 30.09.2026, ca. 22:15 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

*Geschrieben vom steuernden Chat (Übernahme 30.09., 19:24). Anlass: Betreiber 22:08, wörtlich: „Ich möchte jetzt einen neuen chat eröffnen und umziehen“. Die Karte von ca. 22:07 hatte „Nach Abnahme TB-124 (Empfohlen)“ gewählt. TB-124 ist abgegeben, aber noch nicht bewertet; Bewertung und Schliessen übernimmt der neue Chat. „Gemessen“ heisst: über die Geräteanbindung, 30.09., ca. 22:15. Die Regelwortlaute vom 29./30.09. stehen in dieser Datei ab dem Nachtrag 19:13 und in `UEBERGABE_ARCHIV.md`; ins Regelwerk kommen sie mit TB-125.*

### Block 1 — Stand in drei Zeilen

- **Fertig:**
  - TB-124 abgegeben (Abgabe `407ec5d`, 22:13): F1 nach Nachtrag 1 (Scanbeginn `BB_PERIOD + L − 1`), `test_sync_check` 33/0, R28-Probe; C1 13/13 bytegleich, kein Abbruchkriterium laut Ergebnis.
  - Fable 30a eingegangen, bewertet und im Repo (R53–R55).
  - T5 im Repo vollzogen (`UEBERGABE_ARCHIV.md`).
  - Messbitten R53/R54 erledigt.
  - Auftrag TB-125 (Regelwerk-Nachtrag) geschrieben, gegengelesen, im Repo.
- **Läuft:** Die Sitzung TB-124 ist vermutlich noch offen (nicht geschlossen).
- **Als Nächstes:**
  1. TB-124 bewerten (4/5b, jede Zahl an der Rohausgabe) und schliessen.
  2. TB-125 starten.
  3. TB-126 (Register E-2) schreiben.

### Block 2 — HEAD und Commits

- **HEAD `4618fa9`** (`4618fa98bcec004136dab3e49d9d49af68d3410b`), „TB-124 E3: porcelain nach dem Abgabe-Commit“, 30.09. 22:13. Arbeitsbaum gemessen leer (`diff --name-only HEAD` und `ls-files --others` je 0 Zeilen), bis auf diesen Nachtrag.
- Commits von TB-124: `baf18a2` Schritt 0 · `808aa47` Nachtrag 1 · `f6aaf33` 0 · `105419e` A · `f90135e` B · `499d68b` C · `7453469` D · `65fcaf0` D (C3) · `407ec5d` Abgabe (Journal **DV**) · `4618fa9` E3.
- `MAC_TB-125_regelwerk_nachtrag_29_30_09.md` (33 673 B, md5 `49f039e7…`) wurde von TB-124 mitcommittet (`407ec5d`), ebenso die Nachträge 20:20 und 22:05 dieser Datei und der Nachtrag in `VORMESSUNG_E-2`.
- ⚠️ **Dieser Umzugsblock ist uncommittet.** Schritt 0 von TB-125 nimmt ihn mit (die 0a-Liste von TB-125 ist noch Platzhalter).

### Block 3 — Tragende Zahlen

- Register `18e39ee2…`, Abbild `46f0ad5d…`, `herkunft.register()` `01f5997a…`, Datenstand `d9449faf…` (223 Dateien): unverändert laut Umzugsblock 29.09. (Archiv).
  - TB-124 hat `register()` vorher und nachher gemessen: `docs/belege/TB-124/0d_ausgang.txt`, `c5_nachher.txt`.
  - Datenstand vorher/nachher: `0f_datenstand.txt`, `e_datenstand_nachher.txt`.
  - Diese Zahlen sind hier nicht nachgelesen.
- `BACKLOG.md`: **228 Zeilen**, md5 `29b32189…` (mit dem Block „Aus Fable 30a“ aus TB-124).
- **Nummern:** TB frei ab **126** (TB-125 vergeben, nicht gestartet) · Journal frei ab **DW** · R-Blöcke frei ab **R56** · Fable-Anfrage frei ab 30b, am nächsten Tag ab **a**.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-124 bewerten und schliessen.**
   - Ergebnis `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md`, Belege `docs/belege/TB-124/`.
   - Bewertung nach 4/5b, jede Zahl an der Rohausgabe (`c1_vergleich`, `c2_wertprobe`, `c3_vergleich`, `c5_nachher`, `d_probe`, `a_sync_probe`, `e_datenstand_nachher`, `e_db_identitaet`).
   - Dann `schliesse_4618fa98bcec004136dab3e49d9d49af68d3410b`, erst ab 600 s nach dem letzten Commit (Commit 22:13:36, also frühestens 22:24).
   - ⚠️ **Befund aus TB-124 0b:** Die zwei Worktrees `$TMPDIR/tb123_vorher` und `…_vorher2` **existieren auf dem Mac** (je 458 MB). `git worktree prune` entfernt nichts. Entfernen heisst löschen ⇒ Karte (M3).
2. **TB-125 starten.**
   - 0a-Liste messen und eintragen (`PLATZHALTER_0A`), neue Fassung unter neuem Stage-Pfad ablegen, md5 auf beiden Seiten.
   - Auslöser `starte_TB-125`, Wächter-Log prüfen. Dem Betreiber vor dem Einfügesatz `/model sonnet` als eigenen Schritt geben (Vorgabe, 22.12-Lücke).
   - Nachschau per `send_later`, Abnahme mit `einfuegungen.txt`, `b2_numstat.txt`, `b3_vergleich.txt`.
3. **TB-126 (Register E-2) schreiben.** Freigabekarte vorher (M3). Inhalt:
   - R18–R55 zeichengleich. R53–R55 vorher **gegen die Ablage-Datei prüfen**: Die Repo-Fassung von 30a ist eine Abschrift ohne Markdown.
   - Tatsachennotizen TB-122 (Entwurf `ERGEBNIS_TB-122` Abschnitt 6) und TB-124 (Entwurf im Ergebnis TB-124).
   - R53-Zählweise L + 19 gegen wörtlich L + 20.
   - Offene Voraussetzungen nach VORMESSUNG und ihren Nachträgen.
   - Registerkopie Teil 1–4 neu, Ablage-Abgleich.
   - Inventar-Grundlage: 38 R-Blöcke (27c: 15, 29b: 20, 30a: 3).
4. **Fable-Umzug** vor der nächsten Fable-Anfrage. Fable meldete in 30a 🟡 bei ~450 000, nach UMZUG 3 ist das 🔴. Fables Umzugshinweis: Die Übergabe braucht nur Abschnitt 6 und 7 neu.
5. **T5 beim Betreiber:** 18 Dateien aus der Ablage entfernen (Liste: Umzugsblock 30.09. im Archiv, Block 4 Nr. 3) und `UEBERGABE.md` dort durch die aktuelle ersetzen. Das bestätigt der Betreiber.
6. Später: R53 (a) `faltenplan_neun.py` aus `registerdaten.py` · R55-Probe (leere Menge) · E-6, E-3/E-4, Posten 5, Leiter-Skript Stufe IV, `paths.py` (E-9) · DSR-Nebenbefund `kennzahlen.py:222–224` vor R50 · die TB-125-„Nicht getan“-Punkte (K2h/K2f, Trägerstellen, kalter Leser, 29a 1–3, `project_info`-Regel).

### Block 5 — Wartezustände

| wartet | auf |
|---|---|
| TB-124 | Bewertung und Schliessen durch den neuen steuernden Chat |
| TB-125 | 0a-Liste, Auslöser, dann Betreiber: `/model sonnet` und Einfügesatz |
| TB-126 | Auftrag durch den steuernden Chat, dann Freigabekarte |
| Worktrees | Karte „löschen?“ an den Betreiber |
| Betreiber | T5 in der Ablage · Speicher-Export (Frist 29.09., Stand unbekannt) |
| Fable | nichts offen; vor der nächsten Anfrage erst der Fable-Umzug |

### Block 6 — Freigaben und Entscheide

- **Verbraucht:** F1 in TB-124 (30.09., 19:13) samt Nachtrag „Ja, zwei Testdateien (Empfohlen)“ (19:44).
- **Pauschal frei:** Handwerk ohne Sperrlistennähe (26.09.) — darunter TB-125.
- **Nicht freigegeben:** E-2/TB-126 (Register), E-3 … E-9, jede Öffnung von `herkunft.py`, `paths.py`, `zuteilung.py`, `auswertung.py`, `kennzahlen.py`, F3; ein Umbau des Wächters (Modellschalter).
- **Entscheide 30.09. per Karte:** T5 „Wie vorgeschlagen“ (19:44) · F1-Tests (19:44) · Umzug „Nach Abnahme TB-124“ (ca. 22:07), dann Betreiber 22:08 „jetzt“.

### Block 7 — Fehler dieses Chats und die Regeln daraus

| # | Fehler | ⇒ Regel |
|---|---|---|
| 1 | `git status --short` über die Brücke als allererste Messung ⇒ verwaiste `index.lock` | Schon die erste Messung nur mit `--no-optional-locks` (in TB-125 E5/E13) |
| 2 | `device_commit_files` „written“, aber alte Fassung angekommen (TB-124 v3) | T7 für jede Ablage, auch nach späterer Bearbeitung (TB-125 E18) |
| 3 | B1 im Auftrag TB-124 setzte den Scanbeginn auf L + 1, also vor den Vorlauf. Fable 30a deckte es auf; mit Nachtrag 1 rechtzeitig berichtigt | Ein Auftrag, der ein Signal-/Indikatorfenster verschiebt, leitet den Wert aus den Indikatordefinitionen her, nicht aus einer Konstanten |
| 4 | Worktrees als „`prunable`, Ordner weg“ gemeldet; gemessen hatte ich nur über die Brücke, die `$TMPDIR` des Macs nicht sieht | Pfade ausserhalb des Repos (`$TMPDIR`, Home) sind über die Brücke nicht messbar. `git worktree list` zeigt dort „prunable“ auch für bestehende Ordner ⇒ solche Aussagen als „nicht messbar“ kennzeichnen und die Mac-Sitzung messen lassen |
| 5 | Karte mit „21 Dateien“ statt 18 | Zahlen auf einer Karte vorher nachzählen, wie jede andere Zahl |
| 6 | Kein Ablage-Zugriff in dieser Sitzungsart; Fable 30a kam als Text-Anhang (ohne Markdown) | Ablage-Zugriff als Erstes prüfen (TB-125 E5); Registertext aus einem Anhang vor dem Register gegen die Ablage prüfen |

Weiter gültig: Block 7 vom 29.09. (Archiv) und vom 30.09. vormittags (Archiv), samt Kurzfassung.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die Regeln vom 29./30.09. ⇒ TB-125 (Auftrag liegt, committet).
- Die T4-Inventare (Sonnet/Opus) und der Gegenleser-Volltext zu TB-125 lagen nur im Arbeitsordner dieses Chats. Ihre Ergebnisse stehen im Nachtrag 22:05, die Volltexte gehen verloren; das ist Absicht (T1).
- Dieser Umzugsblock (uncommittet, siehe Block 2).

### Block 9 — Eröffnungstext

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt.

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Wenn das nicht geht, sag es ausdrücklich, denn dann müssen wir Messungen wieder über mich laufen lassen. Schon für diese erste Messung gilt: git über die Brücke nur mit --no-optional-locks (rev-parse, log, show, ls-files, diff --name-only), nie git status. Prüfe ausserdem, ob du die Projektablage lesen kannst (project_info); wenn nicht, sag es — dann kommen Fable-Antworten als Anhang.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter (project_read liefert immer die ganze Datei):
1. docs/projektfuehrung/UEBERGABE.md — ganz (seit der Teilung am 30.09. beginnt sie mit dem Nachtrag 30.09.2026, 19:13; der Umzugsblock steht am Ende). Ältere Blöcke nur bei Bedarf in UEBERGABE_ARCHIV.md.
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
Nur wenn die Geräteanbindung fehlt: dieselben Stellen über den Projects-Zugriff (projektfuehrung/…).

Die Regeln vom 29. und 30.09. (u. a. Umzugsampel, Fable-Filter, Karten nach M1–M3, Tokensparen T1–T7, md5 nach jedem Ablegen) stehen in der Erinnerung und in UEBERGABE; ins Regelwerk kommen sie mit TB-125. PRUEFPRINZIPIEN.md (docs/PRUEFPRINZIPIEN.md) und BACKLOG.md gezielt nachlesen, wenn der Anlass kommt. Grosse Dateien über einen Helfer lesen, der nur eine Kurzfassung zurückgibt.

Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt, und was gerade auf wen wartet. Fang danach in derselben Antwort mit dem ersten Handwerksschritt an.
```

**Stehende Pflichten (Kurzfassung):**
- Umzugsampel als letzte Zeile.
- Karte nach M1–M3.
- Helfer nach T1–T3, Gegenleser nach T2.
- An Fable nur vorgeprüfte Verfahrensfragen, als Kopierblock.
- Aufträge per `starte_TB-<n>`, Wächter-Log prüfen, Nachschau per `send_later`.
- md5 nach jedem Ablegen.
- Befehle für den Betreiber je eine Zeile; der Einfügesatz steht am Schluss im Kopierfeld.

## Nachtrag 30.09.2026, ca. 22:40 — neuer steuernder Chat: Übernahme, TB-124 abgenommen und geschlossen

*Geschrieben vom steuernden Chat (Übernahme 22:16). „Gemessen“ heisst: über die Geräteanbindung.*

- **Brücke geht.** Erste Messung nur mit `--no-optional-locks`. HEAD `4618fa9`, `BACKLOG.md` 228 Zeilen, md5 `29b32189…` = Umzugsblock 2/3. Keine `index.lock`.
- **Ablage lesbar** (`project_info`: 51 Dateien, `knowledge_size` 803 641). Fable 30a liegt dort als `FABLE_ANTWORT_2026-09-30a_vorlauf_aggregation_leere_menge.md` (im Repo: `…_vorgepruefte_fragen_e2.md`). Die Prüfung R53–R55 gegen die Ablage (Umzugsblock Block 4 Nr. 3) macht dieser Chat selbst. T5 ist in der Ablage noch nicht vollzogen (die 18 Dateien und die alte UEBERGABE von 17:18 liegen noch dort).
- **TB-124 bewertet (4/5b):** Ein Gegenleser (T2) auf das fertige Ergebnis, rund 95 Angaben an den Rohausgaben geprüft. Die tragenden Zahlen stimmen:
  - C1 13/13 identisch (Präfixe in `c1_vergleich.txt` = `c1_vorher_hashes.txt`, selbst nachgesehen);
  - `test_sync_check` 33/0, 51 Tests gleich, neue Probe 3/3;
  - Scanbeginn-Tabelle (145 / 39 / 116), Register Z. 265 und Z. 280;
  - Datenstand `d9449faf…`/223 vorher = nachher; 11/12 DBs identisch, die zwölfte (`broker_testnet_t3_supertrend.db`) durch den Cron-Lauf 20:05.
  - Code B: in beiden `backtest_breakout.py` `BB_PERIOD + L − 1`, L aus `df.attrs`, passt zu `rolling` ohne `min_periods`. Kein Test geschwächt (`test_sync_check.py` seit TB-119 unverändert, `sync_table.py` nur +47/0).
  - ⇒ **Abgenommen.** Nichts muss wiederholt werden.
- **Befunde (keine tragende Zahl betroffen):**
  1. Zählfehler „elf Paper-Trading-DBs“ (Ergebnis Z. 237, `e_db_identitaet.txt` Z. 11, JOURNAL DV). Gemessen: **zehn** `paper_trading_*.db` (neun im Wurzelordner, eine unter `strategies/volatility_breakout/`), dazu `benachrichtigungen_schliessung.db` und `broker_testnet_t3_supertrend.db` = 12. „11/12 gleich“ stimmt.
  2. C1: Das `cmp`-Skript liegt nicht unter `docs/belege/TB-124/` (Auftrag, Kopfzeile „Prüfwerkzeuge“); das Laufwerkzeug ist `docs/belege/TB-122/a_lauf.py`. „vorher zweimal hashgleich“ (Ergebnis Z. 166) ist nur für einen Lauf belegt.
  3. Der Kandidat nach dem alten B1 (13/13, Ergebnis Z. 103–105) ist nur im Scratchpad geprüft, ohne Beleg. Nicht tragend, er kam nicht ins Repo.
  4. Der Basislauf 0g (19:53–20:58) überspannt Commit `808aa47` (20:08, nur `docs/`); `0g_basis.txt` nennt nur `baf18a2`. Ergebnis 82/82 unauffällig.
  5. Unter „Nicht getan“ fehlen zwei weitere Scan-Schleifen ab `WARMUP_PERIOD + 1`: `research/trailing_stops/run_one_bot.py:379` und `research/vbc_deepdive/run_deepdive.py:145` (Fundstellen vom Gegenleser, hier nicht nachgelesen).
- **Geschlossen:** `schliesse_4618fa98bcec004136dab3e49d9d49af68d3410b`, Wächter 20:32:46Z: HEAD gleich, Alter 1150 s, PID 69826 mit `TERM` beendet, 0 übrig.
- **Zwischengelagert (5b), für den nächsten Dokumentationsauftrag nach TB-125** (TB-125 bleibt unverändert, weil seine Probe den Umfang E1–E24 misst):
  - BACKLOG, neuer Block vor `## 6 — Geparkt`: `### Aus der Abnahme TB-124 (30.09.2026)` mit (a) die zwei `research/`-Scan-Schleifen aus Befund 5 binden oder begründet lassen, vor E-6/Posten 5; (b) Vergleichsskripte (`cmp`) gehören mit in den Belegordner, in künftigen Aufträgen ausdrücklich nennen.
  - JOURNAL: Tatsachennotiz zu DV: „zehn Paper-Trading-DBs, nicht elf; 11/12 unverändert bleibt richtig“.
- **Nächstes:** TB-125 starten (0a eingetragen, Auslöser, `/model sonnet`).

## Nachtrag 30.09.2026, ca. 23:20 — Kartenentscheide 22:40, T5 in der Ablage vollzogen, TB-125 abgenommen und geschlossen

- **Betreiberentscheide 30.09.2026, ca. 22:40, per Karte:**
  - **Worktrees** `tb123_vorher*`: „TB-126 löscht sie (Empfohlen)“ ⇒ Schritt 0 von TB-126: `git worktree remove` für beide, danach nachmessen.
  - **T5:** „Du machst es (Empfohlen)“.
- **T5 vollzogen (22:41):** Die 18 Dateien der Liste vorher im Repo nachgezählt (18 Dateien, 364 040 B, alle vorhanden), dann per `project_delete` aus der Ablage entfernt. Ablage jetzt 33 Dateien, `knowledge_size` 659 299 (vorher 51 / 803 641). `UEBERGABE.md` in der Ablage ersetzt durch die Fassung aus `b711567` (md5 `0ff4bca9…`, 35 875 B).
  - ⚠️ **Fehler Nr. 7:** Die Ablage-Fassung habe ich mit `project_read` ganz in den Chat geholt, statt nur die md5 zu vergleichen (gegen T1), und die md5 danach nicht maschinell verglichen, nur durchgesehen. ⇒ Nach `project_write` die md5 über eine Datei vergleichen, nie den Inhalt in den Chat holen.
- **TB-125 bewertet (4/5b):** Commits `b711567` 0 · `deba416` A/B · `add243a` Abgabe (Journal **DW**) · `e6456cd`/`41864d4` C3.
  - **Modell: Opus 5.5, nicht Sonnet** (`0b_modell.txt`) ⇒ **keine gültige Probe nach 22.12**; die Sonnet-Probe steht weiter aus.
  - Selbst nachgemessen, mit eigenem Parser: alle 24 Texte E1–E24 kommen am Stand `41864d4` genau einmal in ihrer Zieldatei vor und am Stand `b711567` nirgends. numstat `b711567..deba416`: ARBEITSWEISE 157/5, BACKLOG 2/0, UMZUG 23/33 = `b2_numstat.txt`. Geändert nur die drei Dateien, `JOURNAL.md` (+35/0), Ergebnis und Belege.
  - Die Sitzung fand einen Fehler im Auftrag: **E24 stand unter der Überschrift „Datei BACKLOG.md“**, gehört nach ARBEITSWEISE. Sie hat es nach Titel und B2 richtig zugeordnet und benannt. ⇒ Fehler dieses Chats (Auftrag vom vorigen Chat, gegengelesen): Einfügungen immer mit Zieldatei in der eigenen Zeile.
  - ⇒ **Abgenommen.** `BACKLOG.md` jetzt 230 Zeilen, md5 `75f4577f…`.
- **Geschlossen:** `schliesse_41864d416ff9f552c6cba41010ca1bfc7bfa0c9a`, Wächter 21:15:27Z, PID 85913 mit `TERM` beendet, 0 übrig.
- **Nummern:** TB frei ab **126** · Journal frei ab **DX** · R-Blöcke frei ab **R56**.
- **Nächstes:** Auftrag TB-126 (Register E-2) schreiben, Freigabekarte (M3). Dazu gehören in Schritt 0: die Worktrees, dieser Nachtrag und der zwischengelagerte BACKLOG-/Journal-Wortlaut aus dem Nachtrag 22:40 — Letzteres als eigene Einfügung, weil TB-126 sonst nur das Register ändert.
- **R53–R55 gegen die Ablage geprüft (ca. 23:25, ein Helfer, T2):** Ablage-Fassung `FABLE_ANTWORT_2026-09-30a_vorlauf_aggregation_leere_menge.md` (md5 `5e5401bc…`, 13 165 B) gegen die Repo-Abschrift (`f9cdbbef…`, 12 925 B). Die drei Blöcke sind **bytegleich** (R53 1 047 B `cbaeea5b…`, R54 1 241 B `914ddd1d…`, R55 1 016 B `1f3e534b…`; je zwei Zeilen „Rnn —“ bis „Quelle des Grundes …“). Die 240 B Unterschied der ganzen Dateien sind nur Markdown und Leerzeilen. ⇒ TB-126 darf R53–R55 aus der Repo-Datei nehmen; der Vorbehalt aus dem Nachtrag 20:20 ist erledigt.

## Umzug 01.10.2026, ca. 08:20 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

*Geschrieben vom steuernden Chat (Übernahme 30.09., 22:16). Anlass: Auslöser 6, der Verlauf liegt geschätzt bei rund 230 000 Tokens. Sauberer Stand: keine Mac-Sitzung läuft. „Gemessen“ heisst: über die Geräteanbindung, 01.10.2026.*

⚠️ **Ausnahme von UMZUG 3:** Vier Dateien sind uncommittet (Block 2). Schritt 0 von TB-126 nimmt sie mit.

### Block 1 — Stand in drei Zeilen

- **Fertig:**
  - TB-124 und TB-125 abgenommen und geschlossen (Nachträge 22:40 und 23:20). TB-125 lief auf Opus, die Sonnet-Probe steht aus.
  - T5 in der Ablage vollzogen (33 Dateien).
  - R53–R55 bytegleich mit der Ablage.
  - **Auftrag TB-126 (Register E-2) geschrieben:** `docs/auftraege/MAC_TB-126_register_e2.md`, 131 582 B, md5 `3ec1bcc18f5199dbcd0aca37fddd202a`. Zwei Gegenlese-Durchgänge (12 + 2 MUSS, alle eingearbeitet). Anhang A (38 Überschriften, 88 Marken, sechs Indexzeilen, Prüfskript, JSON) hat ein Helfer am Register `41864d4` gebaut; jeder Anker kommt genau einmal vor, vom Gegenleser nachgeprüft.
- **Läuft:** nichts.
- **Als Nächstes:** Freigabe TB-126 (Karte, die Antwort steht unter diesem Block oder fehlt noch), dann TB-126 starten (Block 4 Nr. 1).

### Block 2 — HEAD und Commits

- **HEAD `41864d4`** (`41864d416ff9f552c6cba41010ca1bfc7bfa0c9a`), TB-125 C3.
- **Uncommittet, gemessen:**
  - ` M docs/projektfuehrung/UEBERGABE.md` (Nachträge 22:40, 23:20 und dieser Block);
  - `?? docs/auftraege/MAC_TB-126_register_e2.md`;
  - `?? docs/projektfuehrung/VORARBEIT_TB-126_bauplan_registerauftrag.md` (md5 `92993b43…`, 30 844 B);
  - `?? docs/projektfuehrung/VORARBEIT_TB-126_inventar_r18_r55.md` (md5 `0701725d…`, 26 534 B).

### Block 3 — Tragende Zahlen

- Register: 10 347 Zeilen, sha256 `18e39ee2…`, md5 `c8a32c0f…`, letzter Abschnitt 46 · `herkunft.register()` `01f5997a…` · Abbild `46f0ad5d…` · Datenstand `d9449faf…`/223 (TB-124 E).
- `BACKLOG.md` 230 Zeilen, md5 `75f4577f…` · Ablage 33 Dateien, `knowledge_size` 659 299.
- **Nummern:** TB frei ab **127** (126 vergeben) · Journal frei ab **DX** · R-Blöcke frei ab **R56** · Fable-Anfrage: am 01.10. frei ab **a**.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-126 starten**, sobald die Freigabe vorliegt (Karte M3; Einzelfreigabe Register):
   - Im Auftrag `PLATZHALTER_FREIGABE` durch den Wortlaut ersetzen (Datum, Uhrzeit, Kanal „Auswahlkarte im steuernden Chat“, Kartentext kursiv, gewählte Option fett, Bauart TB-117). Bei „ohne Marke in 9“ zusätzlich A2/48.0/Freigabetabelle anpassen und die Marke Nr. für Abschnitt 9 in Anhang A streichen.
   - Zeiger `docs/auftraege/AKTUELLER_AUFTRAG.md`: Zeile `| **TB-125** |` durch TB-126 ersetzen, „Gesetzt“-Zeile vorn um „zuvor TB-125, erledigt mit `41864d4`, 30.09.2026;“ ergänzen.
   - `PLATZHALTER_0A` messen (`--no-optional-locks diff --name-only HEAD`, `ls-files --others --exclude-standard`) und eintragen. Erwartet fünf Einträge: die vier aus Block 2 und ` M docs/auftraege/AKTUELLER_AUFTRAG.md`.
   - Danach md5 des Auftrags auf dem Gerät festhalten (in Python am Ort editieren, nicht über `device_commit_files`, oder T7).
   - Auslöser `starte_TB-126`, Wächter-Log „Satz ins Fenster gelegt“. Modell: Opus (Standard), kein `/model`.
   - Nachschau per `send_later` nach etwa 2,5 h (zwei Läufe `test_vorregistrierung` à rund 15 min, dazu Einsetzen und Registerkopie).
2. **Abnahme TB-126** (4/5b, Gegenleser T2, jede Zahl an der Rohausgabe), dann `schliesse_<HEAD>` ab 600 s. Danach Ablage-Abgleich nach UMZUG 4: neue `REGISTER_KOPIE_teil*.md` und `REGISTER_INDEX.md` per `project_write` ablegen, md5 maschinell vergleichen (nie den Inhalt in den Chat holen, Fehler Nr. 7), veraltete Teile entfernen. 30a: In der Ablage bleibt Fables Original (`…_vorlauf_aggregation_leere_menge.md`). Dialog-Index: 27c, 29b und 30a nach TB-126 als registriert führen.
3. **Fable-Umzug** (Fable 🔴, ~450 000) vor der nächsten Anfrage. Danach eine vorgeprüfte Anfrage mit „Für Fable“ aus TB-126: Lesarten 50.5 (Zählweise L + 19) und R48 (d), Reibung R53 („Literal mit Test“), Nebenbefund R28 (`pruefe_abschnitt17.py:97`), Vereinigung der Markenorte R48–R50, Orte ohne Marke (Anhang A, Listen B und C, u. a. R21 „Prüfung vor dem Tag“).
4. **Dokumentationsauftrag** (pauschal frei): 5b-Block in `BACKLOG.md` zur Bewertung von 27c, 29a und 29b (fehlt; Fundstelle der Bewertung in UEBERGABE_ARCHIV suchen) · K2h/K2f, Trägerstellen, kalter Leser, 29a 1–3, `project_info`-Regel (TB-125 „Nicht getan“) · R31 (b), R49 (e) ins Regelwerk · neue Fehlerregeln aus Block 7 unten · Sonnet-Probe mit wirksam gesetztem Modell.
5. Später: R53 (a), R55-Probe, `research/`-Scan-Schleifen (BACKLOG „Aus der Abnahme TB-124“, kommt mit TB-126 0c), R41-Neurechnung, R26-Lauf, E-6, E-3/E-4, Posten 5, Leiter-Skript Stufe IV, `paths.py` (E-9), DSR-Einheiten.

### Block 5 — Wartezustände

| wartet | auf |
|---|---|
| TB-126 | Freigabe des Betreibers (Karte), dann Platzhalter, Zeiger, Auslöser, Einfügesatz |
| Fable | nichts offen; vor der nächsten Anfrage erst der Fable-Umzug |
| Betreiber | Karte TB-126 · Speicher-Export (Frist 29.09., Stand unbekannt) |

### Block 6 — Freigaben und Entscheide

- **Entschieden 30.09., ca. 22:40, per Karte:** Worktrees „TB-126 löscht sie“ (steht im Auftrag) · T5 „Du machst es“ (vollzogen).
- **Pauschal frei:** Handwerk ohne Sperrlistennähe (26.09.).
- **Nicht freigegeben:** TB-126 (Karte gestellt), E-3 … E-9, jede Öffnung von `herkunft.py`, `paths.py`, `zuteilung.py`, `auswertung.py`, `kennzahlen.py`, F3; der Umbau des Wächters (Modellschalter).

### Block 7 — Fehler dieses Chats und die Regeln daraus

| # | Fehler | ⇒ Regel |
|---|---|---|
| 7 | UEBERGABE nach `project_write` ganz per `project_read` in den Chat geholt (T1), md5 nicht maschinell verglichen | Nach `project_write` die md5 über eine Datei vergleichen, nie den Inhalt in den Chat holen |
| 8 | Auftrag TB-125: E24 unter der falschen Dateiüberschrift (Auftrag des vorigen Chats, gegengelesen, nicht gefunden) | Zieldatei je Einfügung in eigener Zeile |
| 9 | Entwurf TB-126 v1: Lesarten als Tatsache formuliert (R48 (d), 50.5), Markentabelle der Sitzung überlassen, Nachweise „an der Kopie“, die am festen Pfad lesen | Lesarten des steuernden Chats im Registertext als „Lesart, vorläufig“ kennzeichnen; Markentabellen gibt der steuernde Chat fertig vor (Helfer, Anker vorgezählt); bei Prüfwerkzeugen messen, welchen Pfad sie lesen |
| 10 | TB-125: Sonnet nicht wirksam (Satz lag vor `/model sonnet` schon im Fenster; ungeklärt, ob umgestellt wurde) | Probe erst mit Modellschalter im Wächter oder mit Bestätigung des Modells vor dem Einfügesatz |

Weiter gültig: die Blöcke 7 vom 29.09. und 30.09. (Archiv und oben) samt Kurzfassung.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die vier uncommitteten Dateien (Block 2) ⇒ TB-126 Schritt 0.
- Die Volltexte der Gegenleser zu TB-124 und TB-126 lagen nur im Arbeitsordner dieses Chats und gehen verloren (T1); ihre Ergebnisse stehen in den Nachträgen 22:40 und hier. Die Markentabelle steht als Anhang A im Auftrag, Bauplan und Inventar als `VORARBEIT_TB-126_*`.

### Block 9 — Eröffnungstext

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt.

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Wenn das nicht geht, sag es ausdrücklich, denn dann müssen wir Messungen wieder über mich laufen lassen. Schon für diese erste Messung gilt: git über die Brücke nur mit --no-optional-locks (rev-parse, log, show, ls-files, diff --name-only), nie git status. Prüfe ausserdem, ob du die Projektablage lesen kannst (project_info); wenn nicht, sag es — dann kommen Fable-Antworten als Anhang.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter (project_read liefert immer die ganze Datei):
1. docs/projektfuehrung/UEBERGABE.md — ab der Überschrift „## Umzug 01.10.2026, ca. 08:20“ bis Dateiende. Ältere Blöcke nur bei Bedarf (in derselben Datei weiter oben, noch ältere in UEBERGABE_ARCHIV.md).
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
Nur wenn die Geräteanbindung fehlt: dieselben Stellen über den Projects-Zugriff (projektfuehrung/…).

Die Regeln vom 29. und 30.09. stehen seit TB-125 in ARBEITSWEISE und UMZUG. PRUEFPRINZIPIEN.md (docs/PRUEFPRINZIPIEN.md), BACKLOG.md und den Auftrag MAC_TB-126 gezielt nachlesen, wenn der Anlass kommt. Grosse Dateien über einen Helfer lesen, der nur eine Kurzfassung zurückgibt.

Sag mir in wenigen Sätzen, was du verstanden hast — Stand, nächster Schritt, und was gerade auf wen wartet. Fang danach in derselben Antwort mit dem ersten Handwerksschritt an.
```

**Stehende Pflichten (Kurzfassung):** Umzugsampel als letzte Zeile · Karte nach M1–M3 · Helfer nach T1–T3, Gegenleser nach T2 · an Fable nur vorgeprüfte Verfahrensfragen, als Kopierblock · Aufträge per `starte_TB-<n>`, Wächter-Log prüfen, Nachschau per `send_later` · md5 nach jedem Ablegen · Befehle für den Betreiber je eine Zeile, der Einfügesatz am Schluss im Kopierfeld.

**Nachtrag zum Umzugsblock, 01.10.2026, ca. 08:22:** Betreiberentscheide per Karte: TB-126 **„Freigeben wie beschrieben (Empfohlen)“** (Wortlaut steht im Auftrag, `PLATZHALTER_FREIGABE` ist ersetzt; der Auftrag hat damit md5 `e16f50b4d2f818db1ea0e5efb748efbc` statt `3ec1bcc1…` aus Block 1) · Umzug **„Jetzt, neuer Chat startet TB-126 (Empfohlen)“**. Offen für den neuen Chat aus Block 4 Nr. 1 damit nur noch: Zeiger, `PLATZHALTER_0A`, md5, Auslöser, Einfügesatz, Nachschau.

**Nachtrag 01.10.2026, ca. 18:50:** Der Betreiber schrieb 18:46 wörtlich: „wie geht es weiter? Umzug später“. Damit gilt der Kartenentscheid von 08:22 zum Umzug nicht mehr: Dieser Chat startet TB-126 selbst. Umgezogen wird frühestens nach der Abnahme von TB-126 (UMZUG 3: nicht, solange eine Mac-Sitzung läuft). Der Umzugsblock 08:20 bleibt als Stand gültig; für den neuen Chat gelten zusätzlich die Nachträge darunter.

## Nachtrag 01.10.2026, ca. 20:15 — Tokenmessung, Sparregeln S1–S7, Umzug jetzt (Ausnahme von UMZUG 3)

- **Gemessen** (Protokoll dieser Sitzung, 30.09. 22:16 bis 01.10. 20:05; effektiv = Eingabe + 0,1 × Cache-Lesen + 2 × Cache-Schreiben + 5 × Ausgabe): rund 16 Mio. effektive Tokens. Davon entfielen 9,2 Mio. auf sechs Helfer (Gegenleser TB-126 2,7 · Markentabelle 1,7 · Bauplan 1,6 · Inventar 1,5 · Gegenleser TB-124 1,4 · Abgleich R53–R55 0,3) und 6,9 Mio. auf den Chat selbst (davon Neueinlesen nach drei Pausen über eine Stunde 2,0 · Verlauf lesen 2,0 · feste Anweisungen 1,3).
  - Grösse des Chats zuletzt **504 000**; die festen Anweisungen allein 121 000. Die Ampel dieses Chats hatte „ca. 240 000“ geschätzt — ⚠️ **Fehler Nr. 11**: geschätzt statt gemessen, ohne die festen Anweisungen.
  - Kosten je Schritt: unter 200 000 rund 32 000 · 200–300 000 rund 45 000 · 300–400 000 rund 54 000 · über 400 000 rund 110 000 (mit Pausen).
  - Helfer: Start je rund 83 000, Ende 270 000–440 000, 37–52 Schritte je Helfer, alle Opus.
- **Betreiberentscheid 01.10.2026, ca. 20:10, per Karte:** „1–4, 6, 7 jetzt, 5 als Probe (Empfohlen)“. Wortlaut für das Regelwerk (nächster Dokumentationsauftrag):
  - **S1:** Ein Chat je Auftragsrunde: Auftrag schreiben, gegenlesen, freigeben, starten, dann umziehen; die Abnahme macht der nächste Chat. Umzug nach gemessener Ampel ab rund 250 000 und immer vor einer Pause von mehr als einer Stunde.
  - **S2:** Die Ampel wird aus dem Protokoll gemessen, nicht geschätzt: im Arbeitsordner des Chats `$CLAUDE_CONFIG_DIR/projects/*/<sitzung>.jsonl` (bzw. `~/.claude/projects/…`), letzter Assistenteneintrag, Grösse = `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`. Schwellen: 🟢 unter 200 000, 🟡 200 000–300 000, 🔴 darüber.
  - **S3:** Mechanik als Skript, nicht als Helfer (Anker zählen, md5, Zeilenbereiche schneiden, Diffs). Der Helfer entscheidet nur, was Urteil braucht.
  - **S4:** Eine zweite Gegenleserunde macht ein frischer Helfer mit Befundliste und geänderten Stellen, nicht der alte fortgesetzt.
  - **S5 (Probe):** Helfer eng zuschneiden: genaue Dateien und Zeilenbereiche, Obergrenze rund 25 Schritte, danach Zwischenbericht statt Abbruch.
  - **S6:** Grosse Dokumente nicht im Chat zusammensetzen: Aufträge abschnittsweise in Dateien schreiben und nicht mehrfach umbauen, keine ganzen Dateien in den Chat holen.
  - **S7:** Eine Nachschau liegt unter einer Stunde, oder vorher wird umgezogen.
  - Nicht beschlossen, ausdrücklich: Gegenlesen streichen, pauschal Sonnet, Fable seltener fragen.
- **Betreiberentscheid 01.10.2026, ca. 20:10, per Karte:** „Jetzt umziehen, Abnahme im neuen Chat (Empfohlen)“ — **Ausnahme von UMZUG 3**: Der Grund der Regel (Zwischenstände nur im Kopf des alten Chats) trifft nicht zu; Auftrag, Freigabe und Stand stehen vollständig im Repo.
- **Stand TB-126 beim Umzug (gemessen):** HEAD `69b9ced`, 6 Commit(s) seit `41864d4`. Bei 0 hat die Sitzung Schritt 0 noch nicht committet; ob der Satz abgeschickt wurde, ist dann nicht bekannt (Betreiber fragen, einmal erinnern).
- **Die Nachschau „Nachschau TB-126“ (20:30) ist gelöscht**, damit der alte Chat nicht parallel weiterarbeitet. Der neue Chat plant seine eigene (S7: unter einer Stunde).
- ⚠️ Dieser Nachtrag ist uncommittet. Hat TB-126 Schritt 0 schon committet, erscheint `UEBERGABE.md` in seinem porcelain als geändert; das ist dieser Nachtrag, kein Fehler der Sitzung. Er geht mit dem nächsten Commit des steuernden Chats bzw. des nächsten Auftrags ins Repo.
- **Für den neuen Chat, Reihenfolge:** (1) Ampel nach S2 messen; (2) TB-126 messen: läuft, abgegeben oder nicht gestartet; (3) Nachschau unter einer Stunde planen; (4) Abnahme nach Block 4 Nr. 2 des Umzugsblocks 08:20, der Gegenleser nach S4/S5.
- **TB-126 ist abgegeben** (gemessen 20:15): `1e13135` 0 · `db108a6` A (Register 47–50) · `8687eef` C (Registerkopie, Index) · `69aab70` Abgabe (Journal DX) · `69b9ced` D3, letzter Commit 2026-10-01 19:30:54 +0200. Die Gerätesitzung ist vermutlich noch offen. **Nächster Schritt im neuen Chat:** Abnahme nach Block 4 Nr. 2, dann `schliesse_69b9ced685ed8945fa0d1bbccc9afc176c724e8b`. Die Ausnahme von UMZUG 3 war damit nicht mehr nötig: Beim Umzug lief keine Arbeit mehr.


## Nachtrag 01.10.2026, ca. 20:45 — neuer steuernder Chat: TB-126 abgenommen und geschlossen, Ablage, Fehler Nr. 12, Umzug

- **Übernahme 20:19.** Geräteanbindung und `project_info` gehen. HEAD `69b9ced`, `BACKLOG.md` 235 Zeilen (md5 `49a4e7b7…`). Ampel nach S2 beim Start 122 866.
- **Abnahme TB-126: abgenommen.** Die Mechanik ist mit eigenen Skripten geprüft, unabhängig von denen der Sitzung (S3; sie lesen per `git show`). Ergebnisse:
  - Register `69b9ced`: 11 094 Zeilen, sha256 `b5804659…`, md5 `9a5a403f…`. Einziger Registercommit ist `db108a6`, numstat 747/0. difflib zeigt nur Einfügungen.
  - 87/87 Marken stehen an Anker und Einfügestelle nach Anhang A, dazu R54 unter 48.16; 88 Markenköpfe.
  - 38/38 R-Blöcke zeilengleich mit den Quellen. 38/38 Überschriften.
  - Köpfe 47–49 und Abschnitt 50 zeilengleich: 179 Zeilen, mit Docstring Z. 36–67 und den Entwürfen TB-122/TB-124 eingesetzt.
  - Abschnitt 10 und ERZEUGT unverändert. `registerkopie.py --pruefen` BYTEGLEICH. Index: 173 Z.-Angaben (eigene Zählung), alle auf Marken-/Überschriftszeilen.
  - `herkunft.register()` am HEAD `525c9c42…`, 23 Teile, `fehlend []` (System-Python im Gerät). Journal DX mit Pflichtsatz.
  - Gegenleser (T2, ein Helfer, 9 Schritte, 141 000): 103 von 115 Werten belegt.
- **Befunde der Abnahme** (keiner trifft ein Abbruchkriterium):
  - B1: `0a_status.txt` hat 6 statt 5 Zeilen. Die sechste ist `?? docs/belege/TB-126/`, der eigene Belegordner der Sitzung (Selbstbezug); das Ergebnis nennt sie nicht. ⇒ Regel für Aufträge: 0a in den Scratch messen wie D3 oder den eigenen Belegordner ausdrücklich ausnehmen.
  - B2: `register()` „nachher (`db108a6`)“ und der zweite Testlauf sind an `1e13135` mit uncommittetem Register gemessen (gleicher Inhalt, sha256 `b5804659…`). Vom steuernden Chat am HEAD bestätigt.
  - B3: C2-Kleinigkeiten. Spalte T: 3 Stellen im Ergebnis, 4 im Beleg. „32 Zeilenangaben“ enthält 2 Dubletten. „184/184 auf Markenzeilen“ heisst im Beleg „mit Markenwort“.
  - B4: „Für Fable“ Nr. 6 nennt Liste B (R27, R28, R30, R48 (d)/(e)) nicht ausdrücklich. Die Fable-Anfrage nimmt sie aus Anhang A, Liste B.
  - B5: Zwei angesagte Abweichungen sind angenommen: „; “ statt Komma in der Kette, weil die Orte selbst Kommas tragen, und eine Leerzeile nach Marke 13. ⇒ Fehler im Auftrag (Vorgängerchat): „kommagetrennt“ bei Orten mit Komma. Regel: Trennzeichen nach den Daten wählen.
  - B6: Worktree `$TMPDIR/tb123_vorher` liegt noch (4 Symlinks, `prunable`). Löschen ist ein Betreiberentscheid (Karte).
  - Bekannt, nicht neu: `registerbericht.py --pruefen` rc 1 (39.1, 42.4 G7, 43-6).
- **`schliesse_69b9ced685ed8945fa0d1bbccc9afc176c724e8b`** gelegt 18:29:24Z (Alter 3510 s). Wächter: PID 20133 mit TERM beendet, 0 übrig.
- **Ablage:** `REGISTER_KOPIE_teil1–4.md` und `REGISTER_INDEX.md` sind per `project_write` (`local_path`) ersetzt, mit festen Namen. Die md5 war vor dem Hochladen gleich zum Gerät: teil1 `35af7cb7…`, teil2 `334df4fb…`, teil3 `716b8443…`, teil4 `9338d605…`, Index `57824f7b…`. ⚠️ **Nach dem Hochladen nicht maschinell verglichen.**
- ⚠️ **Fehler Nr. 12:** Zur md5-Prüfung habe ich `project_read` auf `REGISTER_KOPIE_teil4.md` (158 KB) aufgerufen. Die Datei kam ganz inline in den Chat statt als lokale Datei. Ampel 123 000 ⇒ 320 390. ⇒ **Regel:** `project_read` nie zur Prüfung grosser Ablagedateien. Es liefert auch 158 KB inline. Bis ein Weg gemessen ist, gilt: hochladen per `local_path` aus einer md5-geprüften Datei, kein Rücklesen.
- **Nicht getan:** Dialog-Index (27c, 29b, 30a als registriert, Repo und Ablage); BACKLOG-/Journal-Nachtrag zur Abnahme (B1–B6, Fehler 12) ⇒ nächster Dokumentationsauftrag, zusammen mit S1–S7 und Block 4 Nr. 4 des Umzugsblocks 08:20.
- **Stand:** HEAD `69b9ced`, uncommittet nur `UEBERGABE.md` (Nachträge 20:15 und dieser). Keine Gerätesitzung läuft. Nummern: TB frei ab 127, Journal frei ab DY, R frei ab R56, Fable am 01.10. frei ab a.
- **Für den nächsten Chat, Reihenfolge:**
  - (1) Ampel nach S2.
  - (2) Antwort auf die Karte 20:45 (Worktree, Umzug) aus dem Chatverlauf übernehmen; fehlt sie, einmal erinnern.
  - (3) Fable-Umzug (Block 4 Nr. 3), dann die vorgeprüfte Anfrage aus „Für Fable“ TB-126 samt Liste B (B4).
  - (4) Dokumentationsauftrag TB-127: Dialog-Index, Abnahme-Nachtrag, S1–S7, Fehler 11/12, B1/B5-Regeln, Block 4 Nr. 4. Schritt 0 committet die zwei UEBERGABE-Nachträge.
- **Betreiberentscheid 01.10.2026, ca. 20:50, per Karte:** Worktree `tb123_vorher`: **„TB-127 entfernt mit --force (Empfohlen)“**. Schritt 0 von TB-127 misst zuerst, dass im Worktree nur die 4 Symlinks liegen; danach `git worktree remove --force`. Zur Umzugsfrage hat der Betreiber zurückgefragt: „Wie kann es sein dass wir nach dem einlesen wieder direkt umziehen sollen?“ Die Antwort steht im Chat; die Aufschlüsselung ist aus dem Protokoll gemessen: Start 122 866 (davon feste Anweisungen ~121 000), Kernlektüre +17 300, Abnahme rund +93 000, Fehler Nr. 12 +87 700.
- **Dialog-Index nachgezogen (ca. 21:00, Handwerk, Block 4 Nr. 2):** `docs/werkzeuge/dialog_index.py --handfelder` mit `offen` = nein für 27c, 29b und 30a. Die drei Zeilen stehen jetzt auf registriert, Fundstelle 47/48/49. numstat 3/3, keine andere Zeile geändert, `--pruefen` rc 0 (50/50; Status offen 3, ohne Registertext 12, registriert 35). md5 `56714c98…`, in der Ablage ersetzt. Uncommittet; TB-127 Schritt 0 nimmt ihn mit.

## Nachtrag 01.10.2026, ca. 21:20 — neuer steuernder Chat (Übernahme 20:48): Fable-Umzug vorbereitet, Ablage nachgezogen

- **Übernahme 20:48.** Geräteanbindung und `project_info` gehen. HEAD `69b9ced`, `BACKLOG.md` 235 Zeilen (md5 `49a4e7b7…`). Ampel nach S2 beim Start 143 859.
- **Berichtigung der Uhrzeiten im Nachtrag 20:45:** Die Einträge „ca. 20:50“ (Worktree-Entscheid) und „ca. 21:00“ (Dialog-Index) wurden vor 20:45 geschrieben. mtime `UEBERGABE.md` 20:45:08, `FABLE_DIALOG_INDEX.md` 20:44:24. Die Inhalte stimmen; die Zeiten waren geschätzt.
- **Fable-Umzug:**
  - Vorgabe (kein Widerspruch): Der alte Fable-Chat schreibt die Übergabe selbst, wie am 29.09. Die Bitte steht in `FABLE_ANFRAGE_2026-10-01_umzug_uebergabe.md` (ohne Buchstaben; 01.10. bleibt frei ab a).
  - Fable hat `FABLE_UEBERGABE_2026-10-01_neuer_chat.md` in die Ablage gelegt (im Repo fehlt sie noch; der Betreiber legt sie ab). Fables Ampel: 🔴 · gemessen 203 823 nach zwei Verdichtungen.
  - Gemessen: `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md` (Befundliste 1–8 und Eröffnungstext für den neuen Fable-Chat). Kern: Die vier Suchtreffer tragen. Abweichungen von 22.11: Takt nach Bedarf statt täglich; „In einfacher Sprache“ schreibt der steuernde Chat; Kenntnis höchstens als eine Zeile. Sie sind im Eröffnungstext berichtigt, Fables Text bleibt unverändert. „eingefroren 22“ ist ohne Fundstelle ⇒ Voraussetzung.
- **Ablage nachgezogen:** `ARBEITSWEISE.md` und `UMZUG.md` lagen in der Fassung vom 27.09. (ohne 22.11 und ohne Ampel). Beide sind per `local_path` ersetzt; md5 vor dem Hochladen gleich HEAD: ARBEITSWEISE `7d473a4a…`, UMZUG `3292ff38…`. Kein Rücklesen (Fehler Nr. 12). ⚠️ `BACKLOG.md` in der Ablage ist ebenfalls veraltet (Stand 27.09., Repo 01.10.). Bleibt bis zur Prüfung nach 27.4 so; für Fable ist sie gesperrt.
- **Fable-Übergabe vom 29.09. liegt noch in der Ablage** (23.2: nur die jüngste bleibt) ⇒ Karte.
- **Uncommittet:** `UEBERGABE.md`, `FABLE_DIALOG_INDEX.md`, `FABLE_ANFRAGE_2026-10-01_umzug_uebergabe.md`, `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md`; dazu bald `FABLE_UEBERGABE_2026-10-01_neuer_chat.md`. TB-127 Schritt 0 nimmt alle mit.
- **Stand:** Es läuft keine Gerätesitzung. Nummern: TB frei ab 127, Journal frei ab DY, R frei ab R56, Fable am 01.10. frei ab a.
- **Für den nächsten Chat, Reihenfolge:**
  - (1) Ampel nach S2.
  - (2) Hat der neue Fable-Chat bestätigt (Abschnitt 8 seiner Übergabe)? Seine Suchtreffer gegen die Kopie-Zeilen in der Befundliste prüfen.
  - (3) TB-127 schreiben (Dokumentationsauftrag, Inhalt wie im Nachtrag 20:45 Nr. 4, dazu: Uhrzeiten-Berichtigung oben, Fable-Übergabe ins Repo, BACKLOG-Ablage).
  - (4) Die erste Fable-Anfrage vorprüfen lassen („Für Fable“ TB-126, Liste B; Form nach 22.11).

## Nachtrag 01.10.2026, ca. 21:35 — Ampelregel neu (Betreiberentscheid), Fehler Nr. 13

- **Anlass:** Rückfrage des Betreibers, warum fast nach jeder Eingabe ein Umzug empfohlen wird. Messung: `MESSUNG_2026-10-01_ampel_grundlast.md`, Werkzeug `docs/werkzeuge/ampel.py` (md5 `0c42ee78…`, uncommittet).
- ⚠️ **Fehler Nr. 13:** S2 misst die Gesamtgrösse samt Grundlast (~120 000). Die Schwellen vom 29.09. gelten aber für den Verlauf ohne Grundlast. Geschrieben hat das der Vorgängerchat; dieser Chat hat es ungeprüft angewandt (Ampeln 20:48–21:20). ⇒ **Regel:** Bei jeder Änderung einer Messgrösse die Schwellen mit umrechnen.
- **Betreiberentscheid 01.10.2026, ca. 21:35, per Karte:** „Verlauf, 200k/300k (Empfohlen)“. Wortlaut für das Regelwerk (TB-127: UMZUG 3, ARBEITSWEISE 0, S2 ersetzen):
  - Die Umzugsampel misst den **Verlauf = Grösse − Grundlast**, mit `docs/werkzeuge/ampel.py` aus dem Sitzungsprotokoll. Grösse = `input_tokens + cache_read_input_tokens + cache_creation_input_tokens` des letzten Assistenteneintrags; Grundlast = Grösse des ersten Eintrags des Chats.
  - Schwellen: 🟢 Verlauf unter 200 000 · 🟡 200 000–300 000 · 🔴 darüber.
  - Form der Ampel: `Umzugsampel: <Farbe> · Verlauf <n> (Grundlast <g>) · <Empfehlung>`.
  - Umzug vor einer Pause über einer Stunde nur ab 🟡.
- **Folge für diesen Chat:** Verlauf 128 148 (Grösse 248 600, Grundlast 120 452) ⇒ 🟢. TB-127 wird hier geschrieben.
- **Karte 21:20, Ablage:** „Nach Bestätigung entfernen (Empfohlen)“. `FABLE_UEBERGABE_2026-09-29_neuer_chat.md` verlässt die Ablage, sobald der neue Fable-Chat Abschnitt 8 bestätigt hat. Die Umzugsfrage der Karte hat der Betreiber durch die Rückfrage ersetzt; sie ist mit dem Entscheid oben erledigt.
- **Uncommittet zusätzlich:** `MESSUNG_2026-10-01_ampel_grundlast.md`, `docs/werkzeuge/ampel.py`.

## Nachtrag 01.10.2026, ca. 21:50 — Betreiberentscheid F1–F6 (Tokensparen, aus dem Fable-Chat), F1 vollzogen

- **Betreiberentscheid 01.10.2026, ca. 21:25, per Auswahlkarte im Fable-Chat:** „Alle Massnahmen, die du empfiehlst“, Tokensparen ohne Qualitätsverlust.
  - Anlass: Zweiter Fable-Umzugsversuch, 🔴 bei gemessen 651 713 nach dem Einlesen aller vier Registerteile per `project_read`.
  - Gemessen dort: rund 1 MB Text = 637 677 Tokens, also etwa 1,6 Bytes je Token.
- **Wortlaut der Massnahmen** (für TB-127 ins Regelwerk):
  - **F1 (sofort):** Registerkopie je Abschnitt. 51 Dateien mit gleichem Kopf (Commit, Datum, sha256, KOPIE); `REGISTER_INDEX.md` nennt je Abschnitt die Datei. Die vier Teile verlassen die Ablage, sobald die 51 liegen und md5 geprüft sind. Wortlaut unverändert.
  - **F2 (sofort):** Schätzformel Bytes ÷ 1,6 für alles über `project_read`. Die Ampel bleibt gemessen.
  - **F3 (sofort):** Projekt-Erinnerung verdichten. Überholte Vorgeschichte fällt (Termius, screen, Schlüsselbund, mehrfach erzählte Rügen), jede geltende Regel steht einmal. Vor dem Schreiben bekommt der Betreiber die Streichliste.
  - **F4 (Probe über zwei Anfragen):** Ein Fable-Chat je Anfrage. Vorher geht als Verfahrensfrage an Fable: Darf der Anfangsbestand nach 27 durch das Leseprotokoll festgehalten werden statt durch einen R-Block je Chat? Begonnen wird erst nach der Antwort.
  - **F5 (ab der nächsten Anfrage):** Jede Anfrage nennt die Abschnittsnummern aller berührten Registerstellen. Fable öffnet diese, was der Index als „gilt“ und „dazu“ nennt, und weitere nach eigenem Urteil.
  - **F6 (ab dem nächsten Umzug):** Übergabetexte kürzen. Keine Fehlerliste und keine Landkarte, die schon in R52, 50.1 oder im Index steht; Verweis statt Wiederholung.
  - Ausdrücklich nicht: eine Kurzfassung des Registers als zweite Quelle, zusammenfassende Helfer, das Lesen im Wortlaut zu streichen.
- **Vom Betreiber/Fable schon gemessen, nicht wiederholen:** md5 der fünf Registerdateien in der Ablage gleich den Werten (Fehler-12-Lücke geschlossen). Stichproben in der Kopie: teil1 Z. 2137, teil2 Z. 1308, teil3 Z. 1537, teil4 Z. 1372. 22.11 steht in ARBEITSWEISE der Ablage.
- **F1 vollzogen (Handwerk, steuernder Chat):**
  - Werkzeug `docs/werkzeuge/registerkopie_abschnitte.py` (neu, uncommittet; TB-127 nimmt es in `registerkopie.py` auf, samt `--pruefen`). 51 Dateien `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_00–50.md`. Bodies aneinandergehängt sind BYTEGLEICH mit dem Register am HEAD (sha256 `b5804659…`). Grenzen gleich der alten Vierteilung (3818/6839/9480).
  - `REGISTER_INDEX.md`: Die Tabelle „Teile der Kopie“ ist durch „Kopie je Abschnitt“ ersetzt (51 Zeilen: Abschnitt, Datei, Register-Z.). Die alte Vierteilung steht als Fussnote, weil die Tabellen „T1–T4“ weiterführen. numstat 55/6, md5 `b9e5eaff…`.
  - Ablage: 51 Dateien und der Index per `local_path`, md5 vor dem Hochladen gleich Gerät (Liste der 51 md5 als Ganzes verglichen). `REGISTER_KOPIE_teil1–4.md` per `project_delete` aus der Ablage entfernt; im Repo bleiben sie.
- **Fable-Eröffnung:** Fassung 2 steht in `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md`. Abschnitt 3 ist nach dem Entscheid ersetzt (Index ganz, 45–50 ganz, weitere bei Bedarf), 22.11 angeglichen, F4-Frage angekündigt, keine Stichproben-Wiederholung. Fables Übergabetext selbst bleibt unverändert; die Eröffnung geht vor.
- **Offen aus F:** F3 (Streichliste an den Betreiber; die Projekt-Erinnerung umfasst 7 Dateien, rund 68 KB, davon `preferences.md` 34 KB). F2, F4, F5, F6 ⇒ TB-127 ins Regelwerk; F4-Frage und F5-Form in die erste Fable-Anfrage.
- **Uncommittet zusätzlich:** `docs/werkzeuge/registerkopie_abschnitte.py`, `docs/projektfuehrung/register_kopie/` (51 Dateien), `REGISTER_INDEX.md`.

## Nachtrag 01.10.2026, ca. 22:25 — F3 vollzogen, TB-127 geschrieben, gegengelesen und gestartet

- **Betreiberentscheide 01.10.2026, ca. 22:00, per Karte:** F3 „Wie vorgeschlagen (Empfohlen)“ · Umzug: „Hier TB-127 schreiben“ (gegen die Empfehlung, Ampel stand 🟡, Verlauf 210 020).
- **F3 vollzogen:** Projekt-Erinnerung nach `STREICHLISTE_F3_projekt_erinnerung_2026-10-01.md`. `preferences.md` 34 218 ⇒ 8 648 B, `ways-of-working.md` 10 547 ⇒ 2 232 B. Geltende Regeln sind zusammengelegt, nicht umformuliert; die Ampelzeile nennt die Regel von 21:35.
- **Hinweis:** Die Betreibernachricht 21:23 (F1–F6) kam in diesem Chat zweimal an. Sie ist einmal umgesetzt.
- **TB-127:** `docs/auftraege/MAC_TB-127_regelwerk_tokensparen_registerkopie.md` (md5 `7d55e72f…`, 17 942 B).
  - Inhalt: E1–E9 (UMZUG 3, ARBEITSWEISE 0, BACKLOG K4u und „Aus der Abnahme TB-126“), `registerkopie.py --abschnitte` mit md5-Gleichheit gegen die 51 Referenzdateien, Worktree `tb123_vorher` (Karte 20:45), Journal DY. Ausführungsreihenfolge 0, A, C, B, D.
  - Bewusst nicht drin: Block 4 Nr. 4 des Umzugsblocks 08:20 (5b zu 27c/29a/29b, K2h/K2f, Trägerstellen, kalter Leser, 29a 1–3, `project_info`-Regel, R31 (b), R49 (e), Sonnet-Probe). Die Wortlaute sind nicht vorbereitet ⇒ Auftrag TB-128.
  - Gegenleser: ein Helfer nach S5, 16 Aufrufe, 58 Behauptungen. 3 MUSS, alle eingearbeitet: E9 B6-Satz unabhängig vom Ausgang; E1 ohne unbelegten Fable-Schätzsatz; E2 S1 wörtlich („die Abnahme macht“). Von 9 KANN sind 8 eingearbeitet (`--ziel`-Standard, `--marken`-Konflikt, Reihenfolge, Quellenangaben, Wortlaut „das Lesen im Wortlaut streichen“, B4, Fable-Übergabe unter „Nicht getan“). Keine zweite Runde: Die Änderungen sind per Skript mit Trefferzahl 1 je Ersetzung eingesetzt.
  - Zeiger `AKTUELLER_AUFTRAG.md` steht auf TB-127. 0a ist eingetragen (12 Einträge; `FABLE_UEBERGABE_2026-10-01_neuer_chat.md` optional).
- **Freigabe:** Handwerk ohne Sperrlistennähe, pauschal frei. Der Code liegt in `docs/werkzeuge/` und ist nicht auf der Sperrliste.
- **Für den nächsten Chat:** TB-127 nachschauen bzw. abnehmen (B2 md5-Gleichheit, C3 Zeichengleichheit, 0b Worktree). Dann TB-128 schreiben (Block 4 Nr. 4) und die erste Fable-Anfrage vorprüfen (F4-Frage zu 27, „Für Fable“ TB-126 samt Liste B, Abschnittsnummern nach F5).
- **Betreiberentscheid 01.10.2026, ca. 22:05, per Karte:** „Jetzt umziehen (Empfohlen)“. Der Eröffnungstext steht im Chat: Kernlektüre ab „## Nachtrag 01.10.2026, ca. 20:15“, Ampel mit `ampel.py`. Die Nachschau „Nachschau TB-127“ (22:16) ist gelöscht, damit der alte Chat nicht parallel weiterarbeitet; der neue Chat plant seine eigene (S7). ⚠️ Diese Zeile ist nach dem Anlegen von TB-127 angehängt. Hat Schritt 0 schon committet, erscheint `UEBERGABE.md` im porcelain von TB-127 als geändert; das ist diese Zeile, kein Fehler der Sitzung.

## Nachtrag 01.10.2026, ca. 22:35 — neuer steuernder Chat (Übernahme 22:16): TB-127 abgenommen und geschlossen, Fehler Nr. 14

- **Übernahme 22:16.** Geräteanbindung und `project_info` gehen. HEAD `eaea530`, `BACKLOG.md` 235 Zeilen. Kernlektüre aus dem Repo mit Abschnittsfilter, kein `project_read`. Ampel (`ampel.py`, md5 `0c42ee78…`) beim Start: Verlauf 29 121, Grundlast 123 951.
- **TB-127 abgegeben:** `eaea530` 0 · `0e8b361` A/C · `02806ea` B · `792757e` Abgabe (Ergebnis, Journal DY) · `eeee21d` D3 (porcelain 0 Zeilen), 22:19:26. `origin/main` = HEAD.
- **Abnahme TB-127: abgenommen.** Mit eigenen Skripten geprüft (S3), unabhängig von denen der Sitzung:
  - numstat je Commit: nur die erlaubten Dateien (ARBEITSWEISE 10/2, UMZUG 4/0, BACKLOG 7/0, `registerkopie.py` 126/6, dazu Belege, Ergebnis, Journal 37/0).
  - C3: E1–E9 aus dem Auftrag auf die Dateien am `eaea530` angewandt und mit HEAD verglichen. ARBEITSWEISE ganz zeichengleich. UMZUG und BACKLOG weichen nur um je eine Leerzeile nach E1, E2 und E9 ab, wie der Auftrag (Verfahren Nr. 2: Absätze mit genau einer Leerzeile davor und danach) es verlangt. Jeder Anker 1 Treffer.
  - B2: `registerkopie.py --abschnitte --ziel <scratch>` rc 0, 51 Dateien, die md5-Liste ist gleich der Liste von `register_kopie/`. `--abschnitte --pruefen` rc 0 BYTEGLEICH (829 231 B, sha256 `b5804659…`), auch gegen den Scratch. Ein verfälschtes Byte ⇒ rc 1. `--abschnitte --marken` ⇒ rc 2. Teile-Modus `--pruefen` rc 0. Arbeitsbaum danach unverändert.
- ⚠️ **Fehler Nr. 14 (Auftrag TB-127, Vorgängerchat; der Gegenleser hat ihn nicht gefunden):** 0b verlangte „ausser `.git` genau 4 Einträge, alle Symlinks“. Im Ordner liegt aber der volle Checkout `c064405`: 35 Einträge, 17 Symlinks. Die „4 Symlinks“ aus B6 waren die 4 unversionierten Einträge laut porcelain. Die Sitzung hat sich an den Wortlaut gehalten und den Worktree **nicht** entfernt; das ist richtig so. Gemessen: porcelain 4 Zeilen, alle Symlinks auf den Hauptordner, `c064405` ist Vorfahr von `main` ⇒ beim Entfernen geht nichts verloren. ⇒ **Regel:** Die Vorbedingung vor dem Entfernen eines Worktrees ist „porcelain zeigt nur das Erwartete, keine `M`-Zeile, der Commit ist Vorfahr von main“, nicht die Zahl der Einträge im Ordner.
- **Betreiberentscheid 01.10.2026, ca. 22:20, per Karte:** Worktree `tb123_vorher`: **„TB-128 entfernt (Empfohlen)“**, mit der Vorbedingung oben, dann `git worktree remove --force` und `prune`.
- **`schliesse_eeee21deffaf67bb80ac1834a53c35145a892100`** gelegt 20:29:39Z (Alter 614 s). Wächter: PID 27670 mit TERM beendet, 0 übrig. Die Nachschau „Nachschau TB-127“ ist gelöscht (nicht mehr nötig).
- **Offen aus TB-127 („Nicht getan“):** `FABLE_UEBERGABE_2026-10-01_neuer_chat.md` fehlt im Repo, der Betreiber legt sie ab. `registerkopie_abschnitte.py` (Vorlage) ist überholt ⇒ in TB-128 entfernen (Löschen nach M3: Karte oder ausdrücklich im Auftrag).
- **Stand:** HEAD `eeee21d`, uncommittet nur dieser Nachtrag. Es läuft keine Gerätesitzung. Nummern: TB frei ab 128, Journal frei ab DZ, R frei ab R56, Fable am 01.10. frei ab a, Fehler frei ab 15.
- **Für den nächsten Schritt:** TB-128 schreiben: Block 4 Nr. 4 des Umzugsblocks 08:20 (Z. 435), dazu der Worktree nach dem Entscheid oben, Fehler Nr. 14 als Regel in ARBEITSWEISE 0 und die Vorlage entfernen. Danach die erste Fable-Anfrage vorprüfen (F4-Frage zu 27, „Für Fable“ TB-126 samt Liste B, Abschnittsnummern nach F5).

## Nachtrag 01.10.2026, ca. 22:50 — Betreiberanweisung „zukünftig“: Fable-Dokumente legt der steuernde Chat ab; vollzogen

- **Betreiberanweisung 01.10.2026, 22:34, wörtlich:** „ich möchte das du die Dokumente für fable ablegst und mir einen Übergabetext schreibst. Merke dir das für die Zukunft.“ ⇒ **Regel (zukünftig):** Dokumente für Fable legt der steuernde Chat selbst ab, in der Projektablage und im Repo; der Betreiber bekommt dafür keine Aufgabe. Dazu schreibt der steuernde Chat den Übergabetext als Kopierblock in die Antwort; dem Betreiber bleibt das Einfügen im Fable-Chat. Träger: Projekt-Erinnerung (`preferences.md`, eingetragen), dieser Nachtrag, ARBEITSWEISE 0 und 22.11 ⇒ TB-128.
- **Vollzogen:**
  - `FABLE_UEBERGABE_2026-10-01_neuer_chat.md` liegt jetzt im Repo (uncommittet; TB-128 Schritt 0 nimmt sie mit). Weg: `project_read` kam inline (Fall B), deshalb zwei unabhängige Abschriften durch zwei frische Helfer, `cmp` gleich, md5 `ce4b36d7…`, 38 109 B, 520 Zeilen; nach dem Ablegen md5 auf dem Gerät gleich. ⚠️ Ein md5-Vergleich gegen das Original in der Ablage ist nicht möglich; belegt ist die Gleichheit zweier unabhängiger Abschriften.
  - Ablage: `ARBEITSWEISE.md` (md5 `9ab7ff6b…`, 145 799 B) und `UMZUG.md` (md5 `edfe2a34…`, 25 918 B) auf den Stand nach TB-127 (`eeee21d`) ersetzt, per `local_path`, md5 vorher gleich Gerät, kein Rücklesen. `UEBERGABE.md` ebenfalls ersetzt (Stand mit diesem Nachtrag). Unverändert und weiter gültig: `REGISTER_INDEX.md` (md5 `b9e5eaff…`) und die 51 Abschnittsdateien.
  - Eröffnungstext **Fassung 3** in `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md` (zwei Punkte gegenüber Fassung 2 berichtigt) und als Kopierblock im Chat ausgegeben. Ob Fassung 2 schon gesendet war, ist nicht bekannt.
- **Uncommittet:** `UEBERGABE.md`, `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md`, `FABLE_UEBERGABE_2026-10-01_neuer_chat.md`.
- **Wartet:** Bestätigung des neuen Fable-Chats (Punkt 3 der Eröffnung). Danach verlässt `FABLE_UEBERGABE_2026-09-29_neuer_chat.md` die Ablage (Karte 21:20).

## Nachtrag 01.10.2026, ca. 23:30 — Fable hat bestätigt (Meldung des Betreibers), erste Anfrage 01.10.a geschrieben und abgelegt

- **Betreiber 22:53: „fable fertig“.** In Ablage und Repo lag keine neue Fable-Datei; die Meldung ist als Fables Bestätigung im Chat genommen. ⚠️ Wortlaut, Leseprotokoll und Ampel des neuen Fable-Chats hat der steuernde Chat nicht gesehen. Schätzung nach F2: Index und Abschnitte 45–50 zusammen 141 819 B, dazu die Übergabe 38 109 B ⇒ rund 112 000 Tokens Verlauf, unter 300 000 (22.11, Ergänzung 30.09.).
- **Ablage:** `FABLE_UEBERGABE_2026-09-29_neuer_chat.md` per `project_delete` entfernt (Karte 21:20); im Repo bleibt sie.
- **`FABLE_ANFRAGE_2026-10-01a_anfangsbestand_lesarten_marken.md`** (md5 `2203c5f6…`, 10 786 B), im Repo (uncommittet) und in der Ablage, als Kopierblock im Chat ausgegeben. Ob gesendet, zeigt erst Fables Antwort.
  - Inhalt: Teil 0 zwei Kenntniszeilen (R28-Nebenbefund, ERZEUGT-Block). Sieben Fragen: (1) Anfangsbestand 27 durch Eröffnungstext und Leseprotokoll statt R-Block je Chat (F4); (2) 50.5 L + 19 oder L + 20; (3) R48 (d) Lesart, dazu neu gemessen AW:523–537 (`beta_bereinigung` bildet `mittlere_exposure`, 50.1 nennt die Stelle nicht); (4) R53 ohne Rückfall auf Literal; (5) 25.3 (i) zwei Marken; (6) eine Marke je Ort; (7) Listen B und C, Neigung zu einer Marke bei R21 (REG Z. 2200).
  - Vorprüfung: ein Helfer, 26 Aufrufe, Fundstellen in `vorpruefung.md` (nur im Container). Gegenleser: ein frischer Helfer, 10 Aufrufe, 77 Behauptungen, 67 belegt, 0 MUSS, 8 KANN, 2 nicht prüfbar (HEAD, Chat-Angaben). Alle 8 KANN per Skript eingearbeitet, je Ersetzung Trefferzahl 1; keine zweite Runde.
  - Aus „Für Fable“ TB-126: Nr. 1–3 und 5–7 sind Fragen, Nr. 4 und 8 Kenntnis. Liste B ist ausdrücklich genannt (B4 der Abnahme TB-126).
- **Nicht getan:** Dialog-Index um 01.10.a ergänzen (`dialog_index.py`); TB-128 schreiben.
- **Uncommittet:** `UEBERGABE.md`, `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md`, `FABLE_UEBERGABE_2026-10-01_neuer_chat.md`, `FABLE_ANFRAGE_2026-10-01a_anfangsbestand_lesarten_marken.md`.
- **Wartet:** Fables Antwort `FABLE_ANTWORT_2026-10-01a_<stichwort>.md` in der Ablage. Danach: Antwort gegen das Repo messen, Registerauftrag (Einzelfreigabe) für R56 ff.
- **Nummern:** TB frei ab 128, Journal ab DZ, R ab R56, Fable am 01.10. frei ab b, Fehler ab 15.

## Nachtrag 01.10.2026, ca. 23:35 — Fable 01.10.a beantwortet und im Repo; TB-128 geschrieben, gegengelesen, gestartet; Umzug

- **Betreiberentscheid 01.10.2026, ca. 23:12, per Karte:** Umzug: „Hier TB-128 schreiben“ (gegen die Empfehlung, Ampel 🟡, Verlauf 200 872).
- **Betreiber 23:28: „Fable fertig“.** `FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md` liegt in der Ablage und jetzt im Repo (uncommittet, TB-128 Schritt 0): zwei unabhängige Abschriften, `cmp` gleich, md5 `4995260b…`, 22 084 B, 133 Zeilen; md5 auf dem Gerät gleich.
  - **„Kurz“ der Antwort:** 1 ja mit Bindung (R56) · 2 hergeleiteter Index, Zählweise festgeschrieben (R57) · 3 (a) ja, (b) ja, zwei Träger aus einer Rechnung (R60) · 4 ohne Rückfall, Einträge brauchen Freigabe und Probe (R59) · 5 nebeneinander (R58) · 6 ja · 7 sieben Marken nachtragen (R61). Registerblock R56–R61 ab Z. 110 der Antwort.
  - **Fables Ampel:** 🟡, geschätzt ca. 265 000 Verlauf, Grösse gemessen 383 441; „die nächste Anfrage geht an einen neuen Chat“.
  - **Noch nicht getan:** Antwort bewerten und gegen das Repo messen (jede Zahl, „Unsicher“ 1–6; Nr. 3: Die Eröffnung Fassung 3 steht in `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md` und kommt mit TB-128 Schritt 0 ins Repo). Backlog- und Journal-Nachtrag (5b). Dialog-Index: `dialog_index.py` laufen lassen, Handfelder für 01a. Registerauftrag R56–R61 (Einzelfreigabe des Betreibers, Karte).
- ⚠️ **Fehler Nr. 15:** Die neue Fable-Antwort mit `project_search` gesucht statt mit `project_info` (Liste). Die Suche lieferte drei grosse Ausschnitte in den Chat. Die Regel steht in `UEBERGABE_ARCHIV.md` (25.09.) und kommt mit TB-128 E3 in ARBEITSWEISE 0.
- **Berichtigung zum Nachtrag 23:30:** Der Dialog-Index führt Antworten, nicht Anfragen; für die Anfrage 01.10.a war dort nichts nachzutragen.
- **TB-128:** `docs/auftraege/MAC_TB-128_regelwerk_nachtrag_worktree.md`. Inhalt: E1–E7 (ARBEITSWEISE 0: Fable-Ablage, R31 (b), `project_info`, Fehler Nr. 14/8/9/10, kalter Leser, R49 (e); 22.11: F4–F6 und Fable-Ablage; 22.12: Probe TB-125 ungültig; BACKLOG: Bewertung 27c/29a/29b und „Aus der Abnahme TB-127“), Worktree `tb123_vorher` mit der Vorbedingung nach Fehler Nr. 14, Journal DZ.
  - Bewusst nicht drin (⇒ späterer Auftrag): K2h/K2f (Wortlaut „Stellvertreter“ gegen „Merkmal“ offen), die drei Trägerstellen (kein Ersatzwortlaut), Fables 29a Abschnitt 1, Sonnet-Probe, `registerkopie_abschnitte.py` entfernen (kein Betreiberentscheid).
  - Vorarbeit: ein Helfer (24 Aufrufe), Fundstellen V1–V8. Gegenleser: ein frischer Helfer (13 Aufrufe), 74 Behauptungen, 1 MUSS, 12 KANN; alle eingearbeitet per Skript, 17 Ersetzungen mit je Trefferzahl 1. Keine zweite Runde.
  - Zeiger `AKTUELLER_AUFTRAG.md` steht auf TB-128. 0a ist eingetragen (7 Einträge).
- **Für den nächsten Chat:** (1) Ampel; (2) TB-128 nachschauen bzw. abnehmen (0b Worktree, C3 Zeichengleichheit mit eigenem Skript, numstat ohne entfernte Zeilen), dann `schliesse_<HEAD>` ab 600 s; (3) Fable 01.10.a bewerten, 5b-Nachtrag, Dialog-Index; (4) Registerauftrag R56–R61 schreiben, Karte zur Einzelfreigabe; (5) die nächste Fable-Anfrage geht an einen neuen Fable-Chat (Probe F4, wenn R56 eingetragen ist).
- ⚠️ **Fehler Nr. 16:** Uhrzeiten in diesem Chat geschätzt statt gemessen, rund 20 Minuten zu spät (derselbe Fehler wie im Nachtrag 21:20 berichtigt). Gemessen nach mtime: Die Anfrage 01.10.a trägt „ca. 23:20“ und ist 23:09 abgelegt; der Nachtrag „ca. 23:30“ ist von 23:09; der Auftrag TB-128 ist von 23:23 (im Auftrag berichtigt); dieser Nachtrag ist von 23:33; Auslöser `starte_TB-128` 23:32, Wächter-Log 23:33 „Satz ins Fenster gelegt“, nicht abgeschickt. ⇒ **Regel:** Uhrzeiten mit `date` messen, bevor sie in ein Dokument gehen.
- **Nummern:** TB frei ab 129, Journal nach DZ (Kennung messen), R ab R62, Fable am 01.10. frei ab b, Fehler ab 17.
- **Betreiberentscheid 01.10.2026, 23:36 (gemessen), per Karte:** „Jetzt umziehen (Empfohlen)“. Der Eröffnungstext steht im Chat: Kernlektüre ab „## Nachtrag 01.10.2026, ca. 22:35“, Ampel mit `ampel.py` (zuletzt Verlauf 291 834). Eine Nachschau ist nicht geplant; der neue Chat plant seine eigene (S7). ⚠️ Diese Zeile ist nach dem Anlegen von TB-128 angehängt und steht nicht in der Ablage-Fassung. Hat Schritt 0 schon committet, erscheint `UEBERGABE.md` im porcelain von TB-128 als geändert; das ist diese Zeile, kein Fehler der Sitzung.

## Nachtrag 02.10.2026, 07:38 — neuer steuernder Chat (Übernahme 07:33): altes TB-128-Fenster geschlossen, TB-128 neu angelegt

- **Übernahme 07:33 (gemessen).** Geräteanbindung geht (der Ordner `~/trading-bot` wurde in dieser Sitzung neu freigegeben), `project_info` geht (82 Dokumente, 728 680 von 2 000 000). HEAD `eeee21d` = `origin/main`, `BACKLOG.md` 242 Zeilen. Kernlektüre aus dem Repo mit Abschnittsfilter (UEBERGABE ab Nachtrag 22:35, ARBEITSWEISE 0, UMZUG 3), kein `project_read`. Ampel (`ampel.py`, md5 `0c42ee78…`) um 07:36: Verlauf 31 441, Grundlast 130 851.
- **Ablage:** Seit dem 01.10., 23:27 (Fable-Antwort 01.10.a, 21:27:14Z) liegt keine neue Fable-Datei dort; der jüngste Eintrag ist `UEBERGABE.md` von 23:34.
- **Arbeitsbaum** (`diff --name-only HEAD`, `ls-files -o --exclude-standard`): genau die 7 Einträge aus TB-128 0a.
- **TB-128 war nicht gestartet:** kein Schritt-0-Commit. Das Fenster von 23:33 (PID 31654) stand 8 h 04 min mit dem Satz in der Eingabezeile. Nach 22.9 Nr. 3 geschlossen: `schliesse_eeee21d…` gelegt 05:37:16Z (Alter 33 471 s), 1 Sitzung mit TERM beendet, 0 übrig.
- **`starte_TB-128` wird direkt nach diesem Nachtrag neu gelegt;** das Ergebnis steht im Wächter-Log. Dieser Nachtrag ändert 0a nicht: `UEBERGABE.md` steht dort schon als ` M`. Schritt 0 nimmt ihn mit; die Commit-Meldung nennt den 01.10., Abend, der Stand ist vom 02.10., 07:38.
- **Bis Schritt 0 committet ist, legt der steuernde Chat keine neue Datei in den Arbeitsbaum** (0a verlangt genau 7 Einträge, sonst Abbruch). Die Bewertung von Fable 01.10.a entsteht bis dahin im Container.
- **Wartet:** Der Betreiber schickt den Satz ab (ein Klick, 22.3). Die Nachschau plant der steuernde Chat selbst.
- **Nummern:** unverändert — TB frei ab 129, Journal nach DZ (Kennung messen), R ab R62, Fehler ab 17; Fable am 02.10. frei ab a.

## Nachtrag 02.10.2026, 07:46 — Fable 01.10.a gegen das Repo gemessen und bewertet; Fehler Nr. 17

- **Gelesen im Wortlaut aus dem Repo:** `FABLE_ANTWORT_2026-10-01a_anfangsbestand_vorlauf_exposure_marken.md`, md5 `4995260b…`, 22 084 B, 133 Zeilen. Mechanik als Skript (Zitatsuche im Register `docs/VORREGISTRIERUNG_neuselektion.md`, 11 094 Zeilen, sha256 `b5804659…`, Commit `db108a6`), kein Helfer. Alle Messungen aus der Brücken-VM: Vormessung, kein Nachweis.
- ⚠️ **Fehler Nr. 17 (Vorgängerchat, Nachtrag 23:35):** Der Registerblock der Antwort reicht bis **R62** (Z. 131, „Tatsachennotizen 01a“), nicht bis R61; gezählt wurde nach „Kurz“, das R62 nicht nennt. ⇒ Einzutragen sind **R56–R62**, R ist danach frei ab **R63**. **Regel:** Nummern am Block zählen, nicht an der Kurzfassung.
- **Urteil: Die Antwort trägt.** Keine Zahl und kein Zitat ist falsch. Eine Voraussetzung trifft nicht so, wie sie formuliert ist (R60 (a)), eine Stelle ist unscharf (R60 (c)); beides geht an Fable (02.10.a, neuer Fable-Chat). In Frage 4 widerspricht Fable der Neigung des steuernden Chats (Einträge in `registerdaten.py` sind nicht Handwerk); 32.5 (a) trägt das wörtlich ⇒ angenommen.
- **Bestätigt, je mit Fundstelle im Register (REG):**
  - Zitate: 27.6 (Z. 5133) · R53 „Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf“, „zuzüglich der festen Fenster“, „nicht als Literal gesetzt“ (Z. 10897) · 25.3 (i) beide Teile, Marke 26.2 (Z. 4643–4649) · 28.6 „gegen den Horizontbeginn“ · R48 (d) samt Voraussetzung (Z. 10840 f.) · R50 „Sperrliste 3, 5, 7, 9; Abschnitt-0-Menge“ · 32.5 (a) „Eine Registeränderung — `registerdaten.py` ist Träger der Festlegungen, die Änderung braucht den Betreiber (26.6)“ · 26.6 „… entscheidet der Betreiber“ · Kopf 48 „Vereinigung“ · R51 „9 → R48 (b)“, „12 → R50“ (Z. 10879) · 34 „Marke am alten Ort“.
  - Frage 7, die sieben Marken fehlen wirklich: R21 (47.4) nennt „Die Prüfung vor dem Tag in 16.4 … 4⁹ = 262 144“, Marken stehen nur an 16.4 (b), (i), (j) (Z. 2076, 2159, 2162), nicht unter „Prüfung vor dem Tag“ (Z. 2202, „3⁹ = 19 683“). R36 (48.4) nennt „Festlegung 3 und Abschnitt 8 („drei tiefste Falten-Drawdowns“, „Kapital-Drawdown je Falte“)“, Marken nur an 24.2 und 45.5. R37 (48.5) deutet „Alle Falten“ in Abbruchkriterium (b), Marken an Z. 634, 2085, 2088, 2317, 6386, keine in Abschnitt 7. R55 (49.3) fügt die Berichtszeile „Spitze ohne zulässigen Nicht-Spitzen-Punkt“ hinzu, Marke nur an 7 (d) (Z. 804). R33 (48.1) deutet „leere Trade-Liste“ in 45.5 (b) und 43-7, Marke nur an 45.5 (b). 4.2 (Z. 481–518) trägt nur „ERGÄNZT (Verweis) durch R51“.
  - R61 (c): R26 schreibt „(12: keine Option, die einen Bot ausnimmt; 14: Selektion → Bestätigungsperiode → Bericht für alle neun)“. „12“ ist Abschnitt 12 (dort der Satz), „14“ ist Sperrlistenpunkt 14 („Die Reihenfolge Selektion → Bestätigungsperiode → Bericht“, Abschnitt 10); Abschnitt 14 ist „Der Nulltest S-E1“ (Z. 1327). R30 heisst „Ergänzung zu 14“ (47.13).
  - R62 (a): 25.2 (Z. 4628) „… 137 Balken; der 150. Balken liegt am 2018-01-14“. `data/BTCUSDT_1d.csv`: erster Balken 2017-08-17, 137 Balken bis 31.12.2017, Index 149 = 2018-01-13, Index 150 = 2018-01-14, bis 31.01.2018 keine Lücke. ETH nicht gemessen.
  - Leseprotokoll: 24 gelesene und 27 nicht gelesene Abschnitte, zusammen 51.
- **„Unsicher“ 1 (Indexbasis) — beide Teile treffen.** `strategies/volatility_breakout_crypto/backtest_breakout.py:119–122, 129` und `strategies/volatility_breakout/backtest_breakout.py:160–163, 170`: „0-basiert, rolling ohne min_periods … der Einstieg bei i braucht is_squeeze[i - 1]; also i >= BB_PERIOD + L - 1“, `start_i = BB_PERIOD + squeeze_lookback_days - 1`. Der Index ist nullbasiert, und die Bedingung liest die Vorkerze. `research/vorregistrierung/faltenplan.py:242` rechnet „warm ab“ über `faltenplan_neun.symbolbeginn` → `warm_ab` → `balken_datum(pfad, vorlauf_balken, anker)` (`research/faltenplan_neun/faltenplan_neun.py:301–317`, „`nummer`-ter Balken (0-basiert) ab `anker`“) ⇒ v Balken liegen davor. Beide Voraussetzungen von R57 treffen.
- **„Unsicher“ 2 (Tage in AW:528) — kein Widerspruch.** `research/vorregistrierung/auswertung.py:502–517`: Fenster sind die Falten des Plans, deren Name in `selektionsfalten` steht (halboffen); die Reihe ist die der Gewinnerzelle (Aufruf Z. 665); gemittelt wird über die gemeinsamen Tage mit dem Benchmark (`gemeinsam`, Z. 517), Z. 528 `np.mean` der Spalte `exposure`, zurück als `mittlere_exposure` (Z. 537). Das passt zu R48 (d) („über seine Selektionsfalten (7 (c): ‚über dieselben Tage‘)“). Z. 405 liest die Spalte nur in den Selektionsfalten.
- **„Unsicher“ 3 (Eröffnungstext im Repo):** `FABLE_UEBERGABE_2026-10-01_messung_steuernder_chat.md` trägt Fassung 2 und Fassung 3, beide mit sechs Änderungen; sie unterscheiden sich in Nr. 1 und Nr. 4. Fassung 3 ist uncommittet und kommt mit TB-128 Schritt 0. Welche Fassung im Fable-Chat ankam, weiss nur der Betreiber ⇒ gefragt (Karte 02.10.). R56 (b) ist mit Schritt 0 für beide erfüllt.
- **„Unsicher“ 4:** Die Markenregel (34) und der Wortlaut von Sperrlistenpunkt 14 sind oben gemessen. **5:** Kenntnis. **6:** entscheidet der steuernde Chat beim Schreiben des Registerauftrags.
- ⚠️ **R60 (a), Voraussetzung „`research/exposure_messung/` gehört nicht zum Laufbereich“ trifft nicht für den Ordner:** `shared/paths.py:242` (`ARBEITSBAUM_PFADE`, die Laufbereichsmessung vom 26.09.2026) und `docs/belege/TB-112/a2_laufbereich.txt:8` führen `research/exposure_messung/bot_lauf.py` (Lauf-Typ `trockenlauf`). Es ist die einzige Datei des Ordners in der Liste. Die zwei Stellen, die die Grösse zum Einstand bilden (`exposure_kern.py`, `research/exposure_messung/auswertung.py:234`, nach 50.1), stehen nicht darin; `bot_lauf.py` importiert `exposure_kern` nicht. **Lesart des steuernden Chats, vorläufig bis Fable bestätigt (Bauart 46.9):** R60 (a) gilt für die Stellen, die die Grösse bilden, nicht für den Ordner.
- **R60 (c) unscharf:** „über die Tage der Falte“ sagt nicht, ob die Tage der Tagesreihe oder die gemeinsamen Tage mit dem Benchmark gemeint sind (AW:517 schneidet). ⇒ an Fable.
- **R59 (b), Bestand:** `research/vorregistrierung/registerdaten.py:213–216` führt das Bollinger-Fenster schon als Regel `bollinger_fenster` (20.0). Ob das der „Eintrag“ nach R59 (b) ist und ob er eine Probe gegen `BB_PERIOD` trägt, ist nicht gemessen ⇒ Umsetzungsauftrag mit Einzelfreigabe.
- **R56 (d), neue Pflicht:** Vor der nächsten Fable-Eröffnung misst der steuernde Chat die Dateien der Projekt-Erinnerung, die die Plattform dem Fable-Chat lädt (01a nennt `preferences.md` und `ways-of-working.md`), gegen 27.1 und nennt sie im Eröffnungstext. **R56 (e):** eine Tatsachennotiz vor dem Tag über alle Fable-Chats seit R32 ⇒ BACKLOG.
- **Folgt, nach der Abnahme von TB-128:** TB-129 Registerauftrag (neuer Abschnitt 51: R56–R62 zeichengleich, die Marken nach R61 (b) und aus dieser Antwort, Befundtabelle mit den Messungen oben, 5b-Nachtrag BACKLOG und JOURNAL, Dialog-Index 01a), Gegenleser, Karte zur Einzelfreigabe. Danach Fable 02.10.a an einen neuen Fable-Chat: R60 (a), R60 (c).
- **Nummern:** TB frei ab 129, Journal nach DZ (Kennung messen), R frei ab R63 (nach dem Eintrag von R56–R62), Fehler ab 18, Fable am 02.10. frei ab a.

## Nachtrag 02.10.2026, 08:20 — TB-128 abgenommen und geschlossen; Stand für den Umzug

- **TB-128 abgegeben:** `7238842` 0 (07:51:51) · `472a788` A/C · `c0de90f` Abgabe (Ergebnis, Journal DZ) · `560ca75` D3 (porcelain 0 Zeilen), 07:54:59. `origin/main` = HEAD. Um 07:50:57 war HEAD noch `eeee21d`; der Betreiber hat den Satz danach abgeschickt.
- **Abnahme: abgenommen.** Mit eigenem Skript, unabhängig von dem der Sitzung (Nachschau 08:17):
  - numstat je Commit: nur die erlaubten Dateien. Entfernte Zeilen gibt es nur in `AKTUELLER_AUFTRAG.md` (2/2 in Schritt 0, der Zeigerwechsel des steuernden Chats). ARBEITSWEISE 14/0, BACKLOG 12/0, JOURNAL 33/0, Ergebnis 82/0.
  - C3: E1–E7 aus dem Auftrag (md5 `fa973aeb…`) auf die Dateien am `7238842` angewandt und mit HEAD verglichen. ARBEITSWEISE (2375 → 2389 Zeilen, sha256 `1c4176dc…`) und BACKLOG (242 → 254 Zeilen, sha256 `3c3b254b…`) sind zeichengleich; jeder Anker 1 Treffer, jede erste Textzeile in HEAD 1 Treffer.
  - 0b: alle drei Messungen erfüllt (porcelain 4 Zeilen `??`, keine `M`-Zeile; vier Symlinks; `c064405` ist Vorfahr von main). Der Worktree `tb123_vorher` ist entfernt; `git worktree list` zeigt nur den Hauptordner, auch über die Brücke gemessen.
- **Geschlossen:** `schliesse_560ca75…` gelegt 06:19:15Z (Alter 1456 s), PID 45526 mit TERM beendet, 0 übrig. Die Nachschau ist erledigt, eine weitere ist nicht geplant.
- **Aus dem Ergebnis TB-128:** Die nächste Journal-Kennung ist **EA**. Nicht getan und einem späteren Auftrag vorbehalten: K2h/K2f, die drei Trägerstellen, Fables 29a Abschnitt 1, die Sonnet-Probe, `BACKLOG.md` in der Ablage erneuern (vorher 27.4-Prüfung), `registerkopie_abschnitte.py` entfernen (Betreiberentscheid fehlt).
- **Offen beim Betreiber:** welche Fassung (2 oder 3) des Eröffnungstextes im Fable-Chat ankam. Seine Kartenantwort von 07:50 war der Textanfang, und der ist in beiden Fassungen gleich. Erbeten ist der Satz aus Punkt 1 („Die Dateien REGISTER_KOPIE_teil1–4.md …“): endet er mit „sie verlassen die Ablage“, ist es Fassung 2; mit „nimm die Abschnittsdatei“, Fassung 3.
- **Ablage:** `UEBERGABE.md` und `ARBEITSWEISE.md` werden direkt nach diesem Nachtrag auf diesen Stand ersetzt (per `local_path`, md5 vorher gleich Gerät).
- **Stand:** HEAD `560ca75`, uncommittet nur `UEBERGABE.md` (dieser Nachtrag). Es läuft keine Gerätesitzung. **Nummern:** TB frei ab 129, Journal ab EA, R frei ab R56 (R56–R62 sind von Fable 01a belegt und noch nicht eingetragen; danach ab R63), Fehler ab 18, Fable am 02.10. frei ab a.
- **Für den nächsten Schritt:** TB-129 Registerauftrag (Inhalt im Nachtrag 07:46, Punkt „Folgt“), mit Gegenleser und Karte zur Einzelfreigabe. Vorher 27.1 im Wortlaut lesen (für R56 (d)). Danach Fable 02.10.a an einen neuen Fable-Chat.
- **Betreiberentscheid 02.10.2026, per Karte (gestellt 08:20, eingetragen 08:28):** Umzug: „Jetzt umziehen (Empfohlen)“. Der Eröffnungstext steht im Chat: Kernlektüre ab „## Nachtrag 02.10.2026, 07:38“, Ampel mit `ampel.py` (zuletzt Verlauf 187 886, Grundlast 130 851). Eine Nachschau ist nicht geplant. ⚠️ Diese Zeile ist nach dem Ablegen angehängt und steht nicht in der Ablage-Fassung (md5 `8663f387…`).

## Nachtrag 02.10.2026, 10:04 — neuer steuernder Chat (Übernahme 08:39): TB-129 geschrieben, gegengelesen, freigegeben, Auslöser gelegt

- **Übernahme 08:39 (gemessen).** Es war kein Ordner verbunden; `~/trading-bot` über die Ordnerfreigabe angefordert und erhalten. `project_info` geht (82 Dokumente, 735 544 von 2 000 000). HEAD `560ca75` = `origin/main`, `BACKLOG.md` 254 Zeilen. Kernlektüre aus dem Repo mit Abschnittsfilter, kein `project_read`. Seit dem 01.10., 23:27, keine neue Fable-Datei in der Ablage.
- **TB-129** `docs/auftraege/MAC_TB-129_register_fable_01a.md` (md5 `d0c4111e…`, 70 553 B): Abschnitt 51 (R56–R62 zeichengleich; 51.8 Befundtabelle; 51.9 Lesart zu R60 (a), vorläufig; 51.10 Offenes), 14 Marken an 11 Stellen (die zwölf Zeilen aus R61 (b); 4.2 und 49.1 nennen je zwei Blöcke), BACKLOG-Block, Registerkopie, Index, Dialog-Index, Journal EA. Anhang A mit Daten-Block (43 Fundstellen) und Prüfskript; es lief gegen das Register `db108a6` mit rc 0.
- **Gegenleser:** zwei Runden, je ein frischer Helfer. Runde 1: kein Fehler, fünf Unschärfen, fünf Hinweise. Runde 2: neun Einarbeitungen bestätigt, fünf Folgewidersprüche. Alles eingearbeitet. Die Commit-Angaben konnten die Helfer nicht prüfen (Kopie ohne `.git`); der steuernde Chat hat sie über die Brücke gemessen, die Sitzung misst sie in 0d nach.
- ⚠️ **Berichtigung zum Nachtrag 07:46, „Unsicher“ 2:** „kein Widerspruch“ war zu stark. Gemessen ist: `beta_bereinigung` mittelt über die Selektionsfalten der Gewinnerzelle, und zwar über die gemeinsamen Tage mit dem Benchmark (`auswertung.py:517`). Ob das alle „Handelstage des Zeitraums“ nach R48 (d) sind, ist nicht gemessen ⇒ an Fable mit R60 (c), Messung vor dem Tag (51.8, 51.10 Nr. 6). Gefunden vom Gegenleser.
- **Ohne Marke** (R61 (b) zählt sie nicht auf): 47.9 und 47.13 (R61 (c)), 25.2 (R62 (a)), 50.1 (R60 (d)), 50.4 (R57). Indexzeilen in TB-129 C3; Frage an Fable. Vorgabe des steuernden Chats, dem Betreiber genannt, kein Widerspruch.
- **Neu gemessen:** `data/ETHUSDT_1d.csv` wie BTC (137 Balken bis 31.12.2017, Index 150 = 2018-01-14, Januar 2018 lückenlos). `research/exposure_messung/bot_lauf.py` nennt im Docstring Z. 21–22 „Positionen samt gebundenem Kapital“ ⇒ geht mit R60 (a) an Fable. Seit `1e13135` ist unter `research/`, `shared/`, `strategies/`, `config/`, `data/` nichts geändert.
- **Betreiberentscheid 02.10.2026, per Karte (gestellt 09:13, eingetragen 10:02):** TB-129 „Freigeben wie beschrieben (Empfohlen)“; Eröffnungstext vom 01.10.: **„Fassung 2“**. Daraufhin zwei Sätze im Auftrag angepasst (51.8, Zeile R56; BACKLOG-Punkt R56 (e)). Nach dieser Änderung kein Gegenleser mehr; das Prüfskript lief erneut mit rc 0.
- **`ampel.py`** bricht am Protokoll der Cloud-Sitzung ab (`TypeError`: `null`-Felder, drei Schritte eines anderen Modells mit Nutzung 0 vor dem ersten eigenen). Gemessen mit einer Kopie, die `null` als 0 liest und Schritte mit Grösse 0 auslässt; Grundlast 124 273. Steht als Handwerk im BACKLOG-Block von TB-129.
- ⚠️ **Fehler Nr. 18 (dieser Chat):** Der Verlauf stand um 08:46 bei 173 970 und um 09:12 bei 272 304. Die Antwort 01a und Teile der Vorlage TB-126 wurden ganz in den Chat gelesen. **Regel:** vor dem Lesen die Bytes messen und mit ÷ 1,6 gegen die Ampel rechnen; von Vorlagen nur die Gliederung und die eine gebrauchte Stelle; Wortlaute, die ein Skript einsetzt, liest das Skript.
- **Stand:** HEAD `560ca75`. Arbeitsbaum wie TB-129 0a: ` M docs/auftraege/AKTUELLER_AUFTRAG.md` (Zeiger auf TB-129), ` M docs/projektfuehrung/UEBERGABE.md`, `?? docs/auftraege/MAC_TB-129_register_fable_01a.md`. `starte_TB-129` wird direkt nach diesem Nachtrag gelegt; das Ergebnis steht im Wächter-Log.
- **Wartet:** Der Betreiber schickt den Satz ab (ein Klick, 22.3). Ist Schritt 0 nicht committet, ist der Satz nicht angekommen: einmal Hinweis, dann warten (22.5).
- **Abnahme (nächster Chat):** numstat je Commit; R-Diff 7/7; Marken 14/14 an den Stellen aus Anhang A; Abschnitt 10 und ERZEUGT-Block bytegleich; numstat des Registers zweite Spalte 0; mit eigenem Skript. Dann `schliesse_<HEAD>` ab 600 s.
- **Danach:** Ablage erneuern (52 Abschnittsdateien, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`; vorher 27.4-Prüfung); R56 (d): `preferences.md` und `ways-of-working.md` der Projekt-Erinnerung gegen 27.1 messen und im Eröffnungstext nennen; Fable 02.10.a an einen neuen Fable-Chat (R60 (a), (b), (c); die fünf Orte ohne Marke; `bot_lauf.py`).
- **Nummern:** TB frei ab 130, Journal ab EA (vergibt TB-129), R frei ab R63 (nach TB-129), Fehler ab 19, Fable am 02.10. frei ab a.

## Nachtrag 02.10.2026, 10:19 — Betreiber: „weiter hier im chat“; TB-129 noch nicht gestartet; R56 (d) gemessen

- **Betreiberentscheid 10:16:** kein Umzug, der steuernde Chat arbeitet hier weiter, trotz 🔴 (Verlauf 315 552 um 10:16, Grundlast 124 273). Das Risiko (Verdichtung, Verlust von Gelesenem) ist dem Betreiber genannt. Der Chat liest nichts Grosses mehr selbst; Messungen machen Helfer und Skripte.
- **10:16 gemessen:** HEAD `560ca75`, kein Schritt-0-Commit, kein Ordner `docs/belege/TB-129/` ⇒ der Satz ist nicht abgeschickt. Der Wächter war um 10:04:40 fertig; der Satz steht in der Eingabezeile und in `logs/sitzungswaechter/letzter_satz.txt`. Ein Hinweis an den Betreiber (22.5), dann warten.
- **R56 (d) gemessen (Helfer, nur lesend):** `preferences.md` der Projekt-Erinnerung (8 855 B, 50 Zeilen, Version `b83f65ed2913`, Stand 01.10.2026, 22:41) und `ways-of-working.md` (2 232 B, 26 Zeilen, Version `9c5d1f763573`, Stand 01.10.2026, 21:51): je **0 Treffer** nach 27.1. Kein „%“, keine Kennzahl mit Wert, keine Rangfolge, keine Erwartung über den Lauf. Sechs Zeilen tragen Reizwörter ohne Wert (`preferences.md` Z. 20, 22, 38, 40, 47; `ways-of-working.md` Z. 18) und sind keine Treffer. ⚠️ Die Erinnerung wird nach jedem Chat fortgeschrieben: vor der Eröffnung des Fable-Chats die Versionen vergleichen, bei Abweichung neu messen.
- **Sperre für den steuernden Chat:** Bis Schritt 0 committet ist, kommt keine neue Datei in den Arbeitsbaum (0a verlangt genau drei Einträge). Nach Schritt 0 fasst er `UEBERGABE.md` nicht an, bis die Sitzung abgegeben hat. Der Entwurf von Fable 02.10.a entsteht bis dahin im Container.

## Nachtrag 02.10.2026, 10:46 — Betreiber, „für die Zukunft“: der Auftragstext steht am Ende jeder Antwort

- **Betreiber 10:45, wörtlich:** „du sollst mir immer den text für die aufgabe der claude code tasks zum ende ausgeben damit ich diesen final starten kann. merke dir das endlich für die Zukunft.“
- ⚠️ **Fehler Nr. 19 (dieser Chat, 10:04 und 10:19):** Zweimal stand in „Deine Aufgaben“ nur der Verweis auf das Terminal-Fenster des Wächters, nicht der Einfügesatz als Kopierblock. Die Regel gab es schon (ARBEITSWEISE 0, „Wenn eine Mac-Sitzung startet …“: getrennte Kopierblöcke, „nie weggelassen, weil es letztes Mal schon dastand“; 6b, Start).
- **Regel, verschärft:** Jede Antwort, die einen Claude-Code-Auftrag startklar macht oder auf seinen Start wartet, endet mit dem Text für die Aufgabe als Kopierblock, mit Empfänger darüber — auch wenn der Wächter den Satz schon eingesetzt hat. Der Wortlaut kommt aus `logs/sitzungswaechter/letzter_satz.txt` bzw. aus `AKTUELLER_AUFTRAG.md`, nicht aus dem Gedächtnis.
- **Träger:** Projekt-Erinnerung `preferences.md` (eingetragen 10:46); diese Übergabe; ARBEITSWEISE 0 mit dem nächsten Dokumentationsauftrag (bis TB-129 Schritt 0 committet ist, darf keine weitere Datei im Arbeitsbaum geändert sein). ⚠️ `preferences.md` hat damit eine neue Version: vor der Fable-Eröffnung nach R56 (d) neu messen.
- **Stand 10:46:** HEAD `560ca75`, TB-129 nicht gestartet. Fehler ab 20.

## Nachtrag 02.10.2026, 11:56 — TB-129 abgenommen und geschlossen

- **TB-129 abgegeben** (Betreiber 11:53: „129 fertig“): `477cef2` Schritt 0 (10:47:24) · `b443bcb` 0 · `f63ad4c` A, der einzige Registercommit (11:07:23) · `33b0999` B/C · `72f5b21` Abgabe (Ergebnis, Journal **EA**) · `1833839` D3, 11:12:09. `origin/main` = HEAD, Arbeitsbaum leer.
- **Abnahme: abgenommen.** Mit eigenem Skript, unabhängig von dem der Sitzung (11:54):
  - Register: Der steuernde Chat hat das Soll selbst gebaut (Register am `560ca75`, die 14 Marken aus Anhang A von unten nach oben eingesetzt, Abschnitt 51 aus Kopf, den sieben Blöcken der Quelle, den Ketten und dem Schluss des Auftrags). **Soll und Register am HEAD sind zeichengleich.** ⟨S0⟩ steht als `` `477cef2` ``, ⟨DATUM⟩ als 02.10.2026. numstat 131/0, 11 094 → 11 225 Zeilen, jede alte Zeile in derselben Reihenfolge. Abschnitt 10 und ERZEUGT-Block bytegleich. Marken 14/14 je genau einmal, R-Blöcke 7/7, kein Platzhalter im Register.
  - Je Commit nur erlaubte Dateien. BACKLOG 17/0 (254 → 271 Zeilen), der Block zeichengleich genau einmal. JOURNAL 38/0. Dialog-Index: Zeile `01a`, Status „offen“, Fundstelle 51, 51 Antworten (2/1). `REGISTER_INDEX.md` 244/204 (Zeilenangaben umgeschrieben), Kopf nennt `f63ad4c`, Abschnitte 0–51, 11 225 Zeilen; `## 6.` einmal, die sechs Indexzeilen aus C3 je einmal.
  - `registerkopie.py --pruefen` und `--abschnitte --pruefen`: je rc 0, bytegleich, 52 Abschnittsdateien. `test_vorregistrierung` 196/196, rc 0, 865 s (Rohbeleg `a5_test_vorregistrierung.txt`).
- **Aus dem Ergebnis:** Register nachher sha256 `7f74b0e5a746cbc720b7b7c20af83acddd32d6652c3b57099f18769d3d4b16c4`, md5 `b4764e4e…`. `herkunft.register()` vorher `525c9c42…`, nachher `a1e1366a…`, `fehlend []`, 23 Teile. Für Fable nennt die Sitzung zusätzlich: `registerkopie.py --marken` zählt die erste Zitatzeile von R61 (51.6) als `MARKE` (64 statt 63); und ob es ein eigenes Markenwort für Bestätigungen geben soll. Drei Abweichungen von den Vorlagen beim Index (jede Zahl eines Bereichs umgeschrieben; Index Z. 16 nennt jetzt beide Werkzeuge; Pflegezeile), alle begründet, keine vom Auftrag.
- **Geschlossen:** `schliesse_1833839…` gelegt 11:55:56 (Alter 2 629 s), PID 49921 mit TERM beendet, 0 übrig. Es läuft keine Gerätesitzung.
- **Stand:** HEAD `1833839`, uncommittet nur `UEBERGABE.md` (dieser Nachtrag). **Nummern:** TB frei ab 130, Journal ab EB, R frei ab R63, Fehler ab 20, Fable am 02.10. frei ab a.
- **Als Nächstes:** Ablage erneuern (52 Abschnittsdateien, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`, diese Übergabe; vorher 27.4-Prüfung der zwei Indexdateien), R56 (d) neu messen (`preferences.md` hat seit 10:46 eine neue Version), dann Fable 02.10.a an einen neuen Fable-Chat.

## Nachtrag 02.10.2026, 12:11 — Ablage erneuert; R56 (d) neu gemessen; Fable 02.10.a geschrieben, gegengelesen, abgelegt

- **Ablage (Helfer, 11:57–12:01):** 55/55 Dateien md5-gleich mit dem Gerät und geschrieben: die 52 Abschnittsdateien (`_51` neu), `REGISTER_INDEX.md` (md5 `f81541c6…`, 32 727 B), `FABLE_DIALOG_INDEX.md` (`2757cb91…`, 21 198 B), `UEBERGABE.md`. Vorprüfung der zwei Indexdateien gegen 27.1 an den hinzugefügten Zeilen: ein Kandidat (Index Z. 144, „ohne Marke in 15.6“ neben einem Kennzahl-Namen), kein Wert-Treffer. Ablage danach: 83 Dokumente, 753 049 von 2 000 000.
- **R56 (d), zweite Messung (Helfer, 11:58):** `preferences.md` Version `ae05427ad3eb` (9 241 B, 51 Zeilen; neu nur Z. 51, die Regel zum Auftragstext), `ways-of-working.md` unverändert `9c5d1f763573`: je 0 Treffer nach 27.1. Kontoweit `profile.md` und `preferences.md` im Wortlaut vor dem steuernden Chat: 0 Treffer.
- **Fable 02.10.a:** `FABLE_ANFRAGE_2026-10-02a_exposure_tage_laufbereich_marken.md` (md5 `aef98c69…`, 8 384 B), im Repo (uncommittet) und in der Ablage. Vier Fragen: (1) R60 (a), Lesart 51.9; (2) R60 (b), gemeinsame Tage gegen „Handelstage des Zeitraums“; (3) R60 (c), „Tage der Falte“; (4) fünf Orte ohne Marke. Neu gemessen dazu: In `bot_lauf.py` kommen `gebunden`, `kapital_start`, `mittlere` nur im Docstring vor (Wortsuche); es schreibt `<BOT>_positionen.csv` (Z. 242); im Listentext von Abschnitt 10 kommt `exposure_messung` nicht vor.
- **Eröffnungstext:** `FABLE_UEBERGABE_2026-10-02_eroeffnung.md` (md5 `5e2dbd6d…`, 4 903 B), im Repo (uncommittet). Bauart wie Fassung 3, angepasst: Register `f63ad4c`, Abschnitt 51; keine eigene Bestätigungsrunde, die erste Antwort ist die Antwortdatei mit Leseprotokoll nach R56 (b); R56 (d) mit den vier gemessenen Erinnerungsdateien. Eröffnung und Anfrage gehen in **einer** Nachricht an einen neuen Fable-Chat.
- **Gegenleser** (frischer Helfer): kein Fehler, neun Unschärfen, drei Hinweise; eingearbeitet (u. a. Grenze von R46: Abnahme am Test-Snapshot; der verneinende Teil von R61 (b); Abschnitte 48.14, 34, 10 genannt; Uhrzeiten mit Zone). Nach dem Einarbeiten keine zweite Runde.
- **Als Kopierblock im Chat ausgegeben** (ob gesendet, zeigt erst Fables Antwort). **Wartet:** Betreiber fügt den Block in einen neuen Fable-Chat ein; Fable legt `FABLE_ANTWORT_2026-10-02a_<stichwort>.md` ab; der Betreiber meldet „Fable ist fertig“. Danach: Antwort über `project_info` finden, ins Repo übertragen, md5, gegen Register und Code messen, bewerten (5b), Registerauftrag TB-130 mit Einzelfreigabe.
- **Stand:** HEAD `1833839`. Uncommittet: `UEBERGABE.md`, neu die zwei Dateien oben. Es läuft keine Gerätesitzung; kein Auftrag ist startklar. **Nummern:** TB frei ab 130, Journal ab EB, R frei ab R63, Fehler ab 20, Fable am 02.10. frei ab b.
- **Offen für den nächsten Dokumentationsauftrag (ARBEITSWEISE 0):** Regel aus Fehler Nr. 17 (Nummern am Block zählen), aus Nr. 18 (Bytes vor dem Lesen messen), aus Nr. 19 (Auftragstext am Ende jeder Antwort, Betreiber 10:45); `ampel.py` (`null`-Felder, Schritte mit Grösse 0).

## Nachtrag 02.10.2026, 15:11 — Fable 02.10.a bewertet; TB-130 geschrieben, gegengelesen, freigegeben, Auslöser gelegt

- **Betreiber 14:20: „fable fertig“.** `FABLE_ANTWORT_2026-10-02a_exposure_tage_laufbereich_marken.md` über `project_info` gefunden (abgelegt 13:48:58), zwei unabhängige Abschriften durch Helfer, `cmp` gleich, md5 `a7821eeb…`, 21 709 B, 120 Zeilen; im Repo, md5 auf dem Gerät gleich. `project_read` lieferte Text, keine Datei: Die Bytegleichheit mit der Ablage ist nicht gemessen.
- **Urteil: Die Antwort trägt.** Frage 1 einverstanden (R63: die Lesart 51.9 gilt je Stelle, nicht je Ordner). Frage 2 und 3 anders als die Neigung (R64: gemittelt wird über die Benchmark-Tage; der Schnitt auf die gemeinsamen Tage ist Registertext nach 7, 24.2, 23.3; statt Gleichheit der Tagesmengen eine Wache im Lauf, Ausgang 2). Frage 4 einverstanden (R65: alle fünf Orte tragen Marken, 25.2 als BERICHTIGT; die Aufzählungen schliessen die Regel aus 34 nicht ab). ⇒ angenommen.
- **Gemessen (Helfer, Skript und Lesen, nur lesend):** 34 von 37 Registerzitaten wörtlich gefunden; drei sind Umschreibungen (zweimal der Schluss von R61 (b), einmal „2 = nicht gerechnet“ zu 43.1). `bot_lauf.py` ganz gelesen: kein Anteil je Tag, kein Mittel ⇒ die Voraussetzung von R63 (c) trifft. `beta_bereinigung` lässt ausser Fenstermaske und Schnitt keinen Tag weg; fehlende Werte und doppelte Daten werden dort weder behandelt noch geprüft. **Nicht entscheidbar:** die zweite Voraussetzung von R64 (keine offene Position an einem Tag ohne Benchmark-Tag); den Kalender der Tagesreihe legt noch kein Code fest. Leseprotokoll vollständig nach R56 (b); kein Treffer nach 27.1. Fables Ampel: 🔴, gemessen 332 931 nach einer Anfrage.
- **Vom Helfer gemeldet, nicht nachgelesen:** Tatsachennotiz zu 23.3 („lässt den ersten Kurstag je Falte aus“) gegen `research/vorregistrierung/benchmark.py` (die Reihe entsteht einmal über alle Falten). Steht im BACKLOG-Block von TB-130 als Vorprüfung.
- **TB-130** `docs/auftraege/MAC_TB-130_register_fable_02a.md` (md5 `16933dcf…`, 55 675 B): Abschnitt 52 (R63–R65 zeichengleich; 52.4 Befunde; 52.5 Offenes), **zwölf Marken** an elf Stellen: fünf nach R65 (b), sieben vom steuernden Chat nach R65 (a) bestimmt (4.2, 48.16, 48.19, 51.5 zweimal, 51.6, 51.9); keine an 7 (c) (Frage an Fable, 52.5 Nr. 9). Bauart TB-129 mit Verweis, nicht Abschrift. Das Prüfskript lief am echten Repo mit rc 0 (33 Fundstellen, 7 Zählungen, 9 Dateien im Dateimuster).
- **Gegenleser:** zwei Runden, je ein frischer Helfer. Runde 1: drei Fehler (Marke an 4.2 fehlte; „Umstellung kommt mit dem Zellen-Erzeuger“ war nicht belegt; Platzhalter), sechs Unschärfen, drei Hinweise. Runde 2: elf Einarbeitungen bestätigt, sieben Folgewidersprüche. Alles eingearbeitet; über die letzte Einarbeitung ging keine dritte Runde.
- **Betreiberentscheid 02.10.2026, per Karte (gestellt 14:52, eingetragen 15:09):** TB-130 „Freigeben wie beschrieben (Empfohlen)“.
- ⚠️ **T7 erneut eingetreten:** Der `device_commit_files` der freigegebenen Fassung aus einem schon benutzten Stage-Pfad meldete „written“, auf dem Gerät lag weiter die Fassung davor (md5 `4a45c521…`, mit Platzhalter). Die md5-Wache hat es vor Zeiger, Nachtrag und Auslöser gefangen; zweiter Versuch aus einem frischen Pfad, md5 gleich.
- **Stand:** HEAD `1833839`. Arbeitsbaum wie TB-130 0a: ` M AKTUELLER_AUFTRAG.md` (Zeiger auf TB-130), ` M UEBERGABE.md`, neu der Auftrag und die drei Fable-Dateien vom 02.10. (Anfrage, Antwort, Eröffnung). `starte_TB-130` wird direkt nach diesem Nachtrag gelegt. Bis zur Abgabe fasst der steuernde Chat keine Datei im Arbeitsbaum an.
- **Wartet:** Der Betreiber startet die Aufgabe (der Text steht am Ende der Chat-Antwort und in `logs/sitzungswaechter/letzter_satz.txt`). Danach Abnahme mit eigenem Skript (Bauart der Abnahme TB-129: Soll-Register selbst bauen und zeichengleich vergleichen; ⟨S0⟩ steht in Backticks), `schliesse_<HEAD>` ab 600 s, Ablage (53 Abschnittsdateien, beide Indexdateien, diese Übergabe; vorher Prüfung der Indexdateien gegen 27.1).
- **Danach:** Vorprüfung zu 02a „Unsicher“ 1 (Zeitachse des Falten-Sharpe; 16, 21, 29, 33), dann die nächste Fable-Anfrage an einen neuen Fable-Chat (dazu 52.5 Nr. 5, 6, 7, 9); Dokumentationsauftrag für ARBEITSWEISE 0 (Fehler Nr. 17, 18, 19; R65 (a) als Regel für Registeraufträge; `ampel.py`).
- **Ampel dieses Chats:** 🔴, Verlauf 529 890 um 14:51. Der Betreiber hat um 10:16 entschieden, hier weiterzuarbeiten; die Empfehlung zum Umzug steht in jeder Antwort.
- **Nummern:** TB frei ab 131, Journal ab EB (vergibt TB-130), R frei ab R66 (nach TB-130), Fehler ab 20, Fable am 02.10. frei ab b.

## Nachtrag 02.10.2026, 17:03 — TB-130 abgenommen und geschlossen

- **TB-130 abgegeben** (Betreiber 17:00: „tb130 fertig“): `b0c7a35` Schritt 0 (15:13:49) · `cd1bf02` 0 · `ad351d5` A, der einzige Registercommit (15:32:17) · `2f6967c` B/C · `6690eeb` Abgabe (Ergebnis, Journal **EB**) · `e8cfff8` D3, 15:35:12. `origin/main` = HEAD, Arbeitsbaum leer.
- **Abnahme: abgenommen.** Mit eigenem Skript (17:01), Bauart wie bei TB-129: Soll-Register selbst gebaut (Register am `1833839`, die zwölf Marken aus Anhang A, Abschnitt 52 aus Kopf, den drei Blöcken der Quelle, Ketten und Schluss). **Soll und Register am HEAD sind zeichengleich.** numstat 88/0, 11 225 → 11 313 Zeilen, jede alte Zeile in derselben Reihenfolge; Abschnitt 10 und ERZEUGT-Block bytegleich; Marken 12/12, R-Blöcke 3/3, kein Platzhalter. Je Commit nur erlaubte Dateien. BACKLOG 10/0 (271 → 281 Zeilen), Block zeichengleich. JOURNAL 38/0. Dialog-Index 3/2: `01a` jetzt „registriert“ (offen nein), `02a` „offen“, Fundstelle 52, 52 Antworten. `REGISTER_INDEX.md` 236/207: Kopf nennt `ad351d5`, Abschnitte 0–52; `## 7.` einmal; die fünf Indexzeilen tragen „Marke gesetzt in TB-130“. Beide Prüfläufe der Registerkopie rc 0, 53 Abschnittsdateien. `test_vorregistrierung` 196/196, rc 0, 894 s (Rohbeleg).
- **Aus dem Ergebnis:** Register nachher sha256 `a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece`, md5 `80af174f…`. `herkunft.register()` vorher `a1e1366a…`, nachher `4caf0179…`, `fehlend []`, 23 Teile. Für Fable nennt die Sitzung zusätzlich drei Reibungen: `--marken` zählt die erste Zitatzeile von R65 als `MARKE+` (111 statt 110); an 25.2 steht die neue Marke vor der älteren aus R53, die Reihenfolge am Ort ist nicht mehr die zeitliche; kein eigenes Markenwort für Bestätigungen.
- **Geschlossen:** `schliesse_e8cfff8…` gelegt 17:02:30 (Alter 5 238 s), PID 59669 mit TERM beendet, 0 übrig.
- **Stand:** HEAD `e8cfff8`, uncommittet nur `UEBERGABE.md`. **Nummern:** TB frei ab 131, Journal ab EC, R frei ab R66, Fehler ab 20, Fable am 02.10. frei ab b.
- **Als Nächstes:** Ablage (53 Abschnittsdateien, beide Indexdateien; Helfer, mit Prüfung der Indexdateien gegen 27.1); TB-131 Dokumentationsauftrag (ARBEITSWEISE 0: Regeln aus Fehler Nr. 17, 18, 19, T7, R65 (a); `ampel.py`), Handwerk, pauschal frei; danach Vorprüfung zu 02a „Unsicher“ 1 und die nächste Fable-Anfrage.

## Nachtrag 02.10.2026, 17:15 — Ablage nach TB-130 erneuert; TB-131 geschrieben, gegengelesen, Auslöser gelegt

- **Ablage (Helfer, 17:03–17:08):** 55/55 Dateien md5-gleich mit dem Gerät und geschrieben: 53 Abschnittsdateien (`_52` neu), `REGISTER_INDEX.md` (md5 `cdeda21b…`, 35 714 B), `FABLE_DIALOG_INDEX.md` (`a42842d7…`, 21 783 B). Vorprüfung der Indexdateien gegen 27.1 an den hinzugefügten Zeilen: ein Kandidat (Index Z. 145, „ohne Marke in 15.6“), kein Wert-Treffer. Ablage danach: 86 Dokumente, 776 631 von 2 000 000. `ARBEITSWEISE.md` und `BACKLOG.md` in der Ablage sind noch nicht erneuert (nach TB-131; `BACKLOG.md` erst nach 27.4-Prüfung).
- **TB-131** `docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md` (md5 `ef6791a5…`, 14 798 B), Handwerk, pauschal frei (Betreiberentscheid 26.09.2026): E1–E4 in ARBEITSWEISE 0 (Auftragstext am Antwortende, vor der Umzugsampel; Fehler Nr. 17 und Teilmessung; Fehler Nr. 18 und T7; R65 (a), Sperre des Arbeitsbaums, Folgeauftrag), E5 in BACKLOG, dazu `docs/werkzeuge/ampel.py` (liest `null` als 0, zählt Schritte mit Grösse 0 nicht; neue Fassung md5 `997ce08b…`, 40 Zeilen). Die Probe aus B2 hat der steuernde Chat im Container vorab laufen lassen: alt(P1) = neu(P1), alt(P2) rc 1, neu(P2) = neu(P1).
- **Gegenleser** (eine Runde, frischer Helfer): zwei Fehler (Zahlen zu Fehler Nr. 18 standen nicht in der Übergabe; E1 widersprach „Letzte Zeile: Umzugsampel“), sechs Unschärfen, zwei Hinweise; eingearbeitet. Keine zweite Runde (kleiner Dokumentationsauftrag, T2).
- **Regel aus E1, gilt ab sofort:** Der Auftragstext steht am Ende der Antwort **vor** der Umzugsampel; die Ampelzeile bleibt die letzte.
- **Stand:** HEAD `e8cfff8`. Arbeitsbaum wie TB-131 0a: ` M AKTUELLER_AUFTRAG.md` (Zeiger auf TB-131), ` M UEBERGABE.md`, `?? MAC_TB-131_regelwerk_nachtrag_ampel.md`. `starte_TB-131` wird direkt nach diesem Nachtrag gelegt. Bis zur Abgabe fasst der steuernde Chat keine Datei im Arbeitsbaum an.
- **Wartet:** Der Betreiber startet die Aufgabe. Danach Abnahme (numstat je Commit: ARBEITSWEISE 8/0, BACKLOG 6/0, `ampel.py` 7/2; C3 mit eigenem Skript; md5 von `ampel.py`), `schliesse_<HEAD>` ab 600 s, `ARBEITSWEISE.md` in die Ablage.
- **Danach:** Vorprüfung zu 02a „Unsicher“ 1 (16, 21, 29, 33; als Helferauftrag), dann die nächste Fable-Anfrage an einen neuen Fable-Chat (52.5 Nr. 2, 5, 6, 7, 9; drei Reibungen aus den Ergebnissen TB-129/TB-130).
- **Nummern:** TB frei ab 132, Journal ab EC (vergibt TB-131), R frei ab R66, Fehler ab 20, Fable am 02.10. frei ab b.
