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

## Nachtrag 02.10.2026, 18:30 — TB-131 abgenommen und geschlossen; Vorprüfung für Fable 02.10.b

- **TB-131 abgegeben** (Betreiber 18:21: „131 fertig“): `5d4f843` Schritt 0 (18:07:53) · `002aa58` A · `278cf0f` B · `a50aeed` C · `c405ac9` Abgabe (Ergebnis, Journal **EC**) · `0779453` D3, 18:11:14. `origin/main` = HEAD, Arbeitsbaum leer.
- **Abnahme: abgenommen** (eigenes Skript, 18:22): numstat ARBEITSWEISE 8/0, BACKLOG 6/0, `ampel.py` 7/2; je Commit nur erlaubte Dateien. E1–E5: Anker 1, Block genau einmal, an der vorgegebenen Stelle. `ampel.py` md5 `997ce08b…`, 40 Zeilen; die Probe selbst nachgestellt: alt(P1) = neu(P1), alt(P2) rc 1, neu(P2) = neu(P1). Lesart der Sitzung zu E1 (die Zeile steht in der Prüfliste nach der Ampelzeile, die Liste ist keine Reihenfolge der Antwort): angenommen.
- **Geschlossen:** `schliesse_0779453…` gelegt, Ergebnis im Wächter-Log.
- **Vorprüfung für Fable 02.10.b (Helfer, nur lesend, mit Fundstellen; im Chat des steuernden Chats, 18:28):** (A) Zeitachse: 1a „Flache Tage stehen mit Rendite 0 in der Reihe“ (Z. 1430–1432), 29.3 „Der Kapitalpfad … beginnt am 1. Januar seiner ersten Selektionsfalte“ (Z. 5384), 2a (Z. 1475) gegen 23.3 „er wird nicht mit Rendite 0 geführt, sondern gar nicht“ (Z. 3933–3939), 24.2 und R36; 24.1 „Der Drawdown gehört aus derselben Tagesreihe wie der Sharpe“ (Z. 4295) verknüpft beide. Ob die Tagesreihe Tage vor dem ersten Handelbar-Tag führt, regelt keine Stelle. (B) Kein Ausschluss von fehlenden Werten oder doppelten Daten gefunden, weder im Register noch in `auswertung.py` (einzige NaN-Prüfung Z. 355 für `netto_sharpe`). (C) Kein Urteil liest die Exposure der Bestätigungsperiode (`bestaetigungsperiode`, Z. 608–629, nur Bericht); `bestaetigung_ab_effektiv` kommt im Code nicht vor. (D) `benchmark_tagesreihen` schreiben im Repo nur `beispieldaten.py` und Tests; wer den Dateinamen umstellt, sagt keine Registerstelle. (E) `research/vorregistrierung/benchmark.py`: Die Reihe entsteht einmal über den ganzen Zeitraum (Z. 264–272), je Falte nur ausgeschnitten (Z. 290); die Rendite fehlt am ersten Punkt je Symbol (Z. 185, 205). „Je Falte“ in der Tatsachennotiz zu 23.3 deckt der Code nicht; „höchstens ein Tag je Falte“ ist vereinbar. Nur gelesen, nichts ausgeführt.
- **Stand:** HEAD `0779453`, uncommittet nur `UEBERGABE.md`. **Nummern:** TB frei ab 132, Journal ab ED, R frei ab R66, Fehler ab 20, Fable am 02.10. frei ab b.
- **Als Nächstes:** `ARBEITSWEISE.md` in die Ablage; Fable 02.10.b schreiben (sechs Fragen: Zeitachse, fehlende Werte und doppelte Daten, Bestätigungsperiode, Benchmark-Datei, Marke an 7 (c), Tatsachennotiz zu 23.3), gegenlesen, ablegen, als Kopierblock ausgeben; vorher R56 (d) neu messen.

## Nachtrag 02.10.2026, 18:50 — Fable 02.10.b geschrieben, zweimal gegengelesen, abgelegt; ARBEITSWEISE in der Ablage

**Fable 02.10.b.** Im Arbeitsbaum, uncommittet: `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md` (14 621 B, md5 `9bf6249a…`) und `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02b_eroeffnung.md` (5 002 B, md5 `a29bcf41…`). Die Anfrage liegt auch in der Ablage. Sechs Fragen: 1 Zeitachse der Tagesreihe und des Falten-Sharpe, 2 fehlende Werte und doppelte Daten, 3 Bestätigungsperiode und `bestaetigung_ab_effektiv`, 4 Benchmark-Datei `<bot>.csv` gegen `<markt>.csv`, 5 Marke an 7 (c), 6 Tatsachennotiz zu 23.3 („je Falte“). R-Blöcke ab R66; Antwortdatei `projektfuehrung/FABLE_ANTWORT_2026-10-02b_<stichwort>.md`.

**Gegenleser.** Runde 1: neun Befunde, darunter ein Fehler (24.1 umgekehrt wiedergegeben: der Drawdown folgt der Tagesreihe des Sharpe, nicht umgekehrt). Runde 2 (frischer Helfer, nur die Änderungen): sechs Befunde, darunter ein Fehler (R61 (b) „zweiter Satz“ falsch bestimmt; richtig: „Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist …“). Alle eingearbeitet. Zitatprobe per Skript gegen das Register am `ad351d5`: 44 von 50 Anführungen stehen wörtlich im Register, die übrigen 6 sind keine Registerzitate (Antwortform, Codekommentar, eigener Vorschlag). Beide Fehler waren meine; sie sind vor der Ausgabe gefunden und berichtigt.

**R56 (d), neu gemessen 18:49:** Projekt-Erinnerung `preferences.md` (9 241 B, Stand 08:46 UTC) und `ways-of-working.md` (2 232 B, Stand 01.10., 19:51 UTC) unverändert.

**Ablage.** `ARBEITSWEISE.md` erneuert (151 512 B, md5 `42e20803…`, Stand nach TB-131). `UEBERGABE.md` folgt mit diesem Nachtrag. `BACKLOG.md` ist in der Ablage nicht erneuert (Prüfung nach 27.4 fehlt).

**Stand.** HEAD `0779453`. Uncommittet: `UEBERGABE.md` und die zwei Dateien zu Fable 02.10.b. Keine Gerätesitzung, kein Auftrag startklar. Nummern: TB frei ab 132, Journal ab ED, R frei ab R66, Fehler ab 20, Fable am 02.10. frei ab c.

**Wartet.** Der Betreiber fügt Eröffnungstext und Anfrage als eine Nachricht in einen neuen Fable-Chat ein und meldet „Fable ist fertig“.

**Als Nächstes, nach der Antwort:** über `project_info` finden, zwei unabhängige Abschriften durch Helfer, `cmp`, ins Repo, gegen Register und Code prüfen, bewerten; dann TB-132 schreiben (Registerauftrag, Abschnitt 53, R66 und folgende, Marken; Bauart TB-130), Gegenleser, Karte zur Einzelfreigabe.

## Nachtrag 02.10.2026, 20:20 — Fable 02.10.b bewertet: nichts eingetragen; Messung vor dem Eintrag; Fable 02.10.c geschrieben und abgelegt

**Antwort 02.10.b.** Über `project_info` gefunden, zwei unabhängige Abschriften sind gleich (23 904 B, md5 `33c4e962…`), im Repo unter `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md` (uncommittet). Inhalt: R66–R71. Frage 1 (b) „anders“ (der Falten-Sharpe läuft über alle Tage der Tagesreihe in der Falte), die übrigen einverstanden, Frage 4 mit anderem Schnitt (eine planmässige Öffnung von `auswertung.py`).

**Bewertung (5b): R66–R71 werden nicht eingetragen, bevor Fable neu geantwortet hat.** Drei Blöcke tragen „wird gemeldet, nicht eingetragen“; die Messung (drei Helfer; Belege unter `docs/belege/TB-132/vormessung/`, sechs Dateien, uncommittet) ergab:

1. **R68, erste Voraussetzung trifft nicht:** 16.6 ersetzt 15.4 (d) vollständig (REG Z. 2294; Marke Z. 1490–1493); R37 (ii) ordnet den Wortlaut beider der Leiter zu. R68 (c) führt R60 (c) an, das von den zwei Trägern der Exposure spricht, nicht von Rendite und Exposure.
2. **R71 trifft nur eingeschränkt:** Die Probe `r71_probe.py` (synthetische Kurse, echte `benchmark.py`) bestätigt unter pandas 2.3.3 den „lies“-Satz. Ein Tag fehlt aber auch, wenn kein handelbares Symbol einen Kurs trägt. `pct_change()` (`benchmark.py:205`) füllt auf: Rendite 0 am Lückentag und nach dem Reihenende eines Symbols (FutureWarning). Unter pandas 3.0.5 fehlen in drei Zusatzfällen weitere Tage; der Lock legt 2.3.3 fest. Die Probe lief nicht in der Lock-Umgebung (Python 3.10.12 statt 3.9.6); vor dem Eintrag auf dem Betriebsrechner wiederholen.
3. **R66 (a):** Am Code trifft die Voraussetzung. Aber 17.5 (REG Z. 2826–2829) führt schon einen Handelskalender (`pandas_market_calendars` 4.6.1), den Fable nicht kannte. Heutiger Bestand: 16 275 Aktien-Kurstage, deckungsgleich mit dem NYSE-Kalender des Pakets.
4. **R66 (e):** Kein Code bildet den Falten-Sharpe aus der Tagesreihe. Aber der DSR des Gewinners rechnet einen Sharpe auf den gemeinsamen Tagen mit dem Benchmark (`auswertung.py:670`, `:517`; `kennzahlen.py:219–246`); R66 (c) nennt ihn nicht.
5. **Daten heute (nicht Snapshot):** Krypto je Bot 24 Symbole ohne Lücke; Aktien 150 Symbole, zwei Symbol-Tage Lücke (1974-06-03 `LMT`, 2026-08-10 `MNST`), keine früher endende Reihe.

Dazu: Die Voraussetzung zu R69 (b) und die zweite zu R68 treffen. Fables „Unsicher“ 2: Den Fall gibt es (vier erste Falten). Von 56 Zitaten und Verweisen in 02b treffen 40 im Wortlaut, 14 sinngemäss, 2 nicht.

**Fable 02.10.c.** Im Arbeitsbaum, uncommittet: `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02c_messung_vor_eintrag_r66_r71.md` (22 485 B, md5 `eb9dfec7…`) und `FABLE_UEBERGABE_2026-10-02c_eroeffnung.md` (5 691 B, md5 `0cac4323…`); die Anfrage auch in der Ablage. Sechs Fragen: 1 Handelskalender (17.5 gegen Kurstage im Snapshot), 2 Tage des Sharpe im DSR, 3 R68 ohne 2d, 4 R71 und das Auffüllen, 5 vier Markenorte (52.4 zweimal, 51.6, 52.3, 52.2 durch R71), 6 Nummern geänderter Blöcke (Neigung: dieselbe Nummer, neue ab R72). Zwei Gegenleser-Runden (14 und 8 Befunde, eingearbeitet). Meine Fehler im Entwurf: die Fundstellenliste zu „Handelstag“ war unvollständig, eine Zeilennummer in `kennzahlen.py` lag um eins daneben, und ein Zitat aus 16.6 enthielt einen P95-Wert (27.1; gestrichen, bevor etwas hinausging).

**R56 (d), neu gemessen 20:01:** Projekt-Erinnerung unverändert (`preferences.md` 9 241 B, `ways-of-working.md` 2 232 B).

**Nebenbeobachtungen, nicht verfolgt:** Die DSR-Einheiten (`sr` je Beobachtung gegen `sr0`) sind schon geführt (Register 50.7 Nr. 3, „vor dem Tag“). `tagesschluss` normalisiert `open_time` nicht und prüft keine doppelten Daten; am heutigen Bestand folgenlos.

**Stand.** HEAD `0779453`. Uncommittet: `UEBERGABE.md`; zu Fable 02.10.b Anfrage, Eröffnung, Antwort; zu Fable 02.10.c Anfrage und Eröffnung; `docs/belege/TB-132/vormessung/`. Keine Gerätesitzung, kein Auftrag startklar. Nummern: TB frei ab 132, Journal ab ED, Fehler ab 20, Fable am 02.10. frei ab d. R66–R71 sind in 02b vergeben und nicht eingetragen; neue Blöcke ab R72.

**Wartet.** Der Betreiber fügt Eröffnungstext und Anfrage 02.10.c als eine Nachricht in einen neuen Fable-Chat ein und meldet „Fable ist fertig“.

**Als Nächstes, nach der Antwort:** über `project_info` finden, zwei Abschriften, `cmp`, ins Repo, gegen Register und Code prüfen, bewerten. Dann TB-132 schreiben: Abschnitt 53 mit R66 und folgenden in der letzten Fassung, den Befunden der Vormessung und den Marken; als Schritt 0 läuft `r71_probe.py` in der Lock-Umgebung, bei Abweichung Abbruch ohne Eintrag. Gegenleser, Karte zur Einzelfreigabe.

## Nachtrag 03.10.2026, 01:15 — Fable 02.10.c bewertet: trägt; TB-132 gebaut und zweimal gegengelesen; wartet auf die Einzelfreigabe

**Antwort 02.10.c.** In der Dokumentliste des Projekts gefunden, zwei unabhängige Abschriften sind gleich (30 216 B, md5 `6aad30ec…`), im Repo unter `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md`. Fable hat alle sechs Blöcke neu ausgegeben (R66–R71 in der Fassung 02c) und R72, R73 dazu. Frage 1 „anders“: Für Aktien gilt der Handelskalender nach 17.5, die Kurstage sind die Probe, eine Abweichung endet den Lauf mit 2. Der Sharpe im DSR bleibt, wie der Code ihn rechnet. R68 steht ohne 2d. Das Auffüllen an Kurslücken ist Tatsachennotiz (R72), das Reihenende wird am Snapshot gemessen. R73 hält fest: Die Antwort kam aus dem Chat von 02b, nicht aus einem neuen (Betreiberentscheid per Karte dort, Chat über der Umzugsschwelle).

**Bewertung (5b): Die Blöcke tragen und werden eingetragen.** Gemessen (Belege unter `docs/belege/TB-132/vormessung/`, jetzt neun Dateien): 98 Zitate und Verweise, keine trifft nicht, zehn sinngemäss (`v4_register_02c.md`). Voraussetzungen (`v5_code_02c.md`): R66 (b) nicht entscheidbar (der Code des Laufs benutzt keinen Kalender; im Repo nur „NYSE“ im Live-Pfad; „XNYS“ hätte einen Handelstag mehr, 2025-01-09); R66 (c) trifft für die Funktion `kennzahlen.sharpe`, einen Aufruf gibt es noch nicht; R72, zweite, trifft für `research/mtm_drawdown/mtm_kern.py`. Die Wiederholung der Probe in der Lock-Umgebung (R71, R72) ist Schritt 0e von TB-132; weicht sie ab, wird nichts eingetragen.

**TB-132 gebaut.** `docs/auftraege/MAC_TB-132_register_fable_02c.md` liegt als **Entwurf mit Platzhalter `⟨⟨FREIGABE⟩⟩`** im Repo (127 043 B, md5 `f72bb281…`); solange der Platzhalter steht, bricht die Vorprüfung ab. Kein Zeiger, kein Auslöser. Inhalt: Abschnitt 53 (53.1–53.8 = R66–R73 zeichengleich aus der Antwort 02c; 53.9 Voraussetzungen und Befunde; 53.10 Was offen bleibt), 21 Marken (20 nach R70 (c), eine an 23.3 Registertext 3b (c) vom steuernden Chat nach R65 (a)), Datum des Eintrags fest 03.10.2026. Neu gegenüber TB-130: Datumsprüfung, Probe `r71_probe.py` mit `trading-env/bin/python3` vor dem Eintrag, beides auch als Wache im Einfügeskript, das fertig im Auftrag steht. Gebaut von einem Helfer nach `tb132_vorgabe.md`, zwei Gegenleser-Runden (ein Fehler, zehn Unschärfen, alle eingearbeitet). Soll: 11 313 → 11 471 Zeilen, numstat 158/0, vom steuernden Chat selbst nachgebaut und bytegleich; sha256 des Solls in der Vorschau `1be85dc2…` (mit ⟨S0⟩ als Platzhalter).

**Nach der Freigabe (Karte):** Platzhalter durch den Freigabetext ersetzen (Form wie TB-130: Datum, Kartentext, gewählte Antwort), Auftrag aus frischem Pfad neu legen, md5 am Gerät prüfen, Zeiger in `AKTUELLER_AUFTRAG.md` setzen, Auslöser `docs/auftraege/_ausloeser/starte_TB-132`, Einfügesatz ausgeben. Läuft die Sitzung nicht am 03.10.2026, bricht sie ab; dann Neubau mit neuem Datum. **Abnahme:** Einfügeskript aus dem Auftrag holen, `--vorschau --s0 <S0> --register <Kopie>` auf das Register am `ad351d5`, zeichengleich mit dem Register nach der Sitzung vergleichen; `docs/belege/TB-132/probe_lock_r71.txt` ansehen.

**Offen für die nächste Anfrage an Fable** (steht auch in 53.10): Kalendername; Deckelfall (R68 (d)); die Marke an 23.3 Registertext zur Kenntnis; die zehn sinngemässen Verweise zur Kenntnis.

**Stand.** HEAD `0779453`. Uncommittet: `UEBERGABE.md`; die sechs Dateien zu Fable 02.10.b und 02.10.c; `docs/belege/TB-132/vormessung/` (neun Dateien); der Auftragsentwurf TB-132. Keine Gerätesitzung. Nummern: TB-132 vergeben, TB frei ab 133; Journal ab ED (TB-132 nimmt ED); R66–R73 vergeben, frei ab R74; Fehler ab 20; Fable am 03.10. frei ab a. Der Container des steuernden Chats wurde um 01:10 neu gestartet; die Baudateien unter `/home/claude/tb132/` haben es überstanden, sind aber nur dort.

## Nachtrag 03.10.2026, 07:29 — TB-132 freigegeben und gestartet

**Freigabe.** Auswahlkarte im steuernden Chat (gestellt gegen 01:16, beantwortet 07:28): „Freigeben wie beschrieben (Empfohlen)“. Der Freigabetext steht im Auftrag an der Stelle des Platzhalters.

**Gelegt.** `docs/auftraege/MAC_TB-132_register_fable_02c.md` (127 733 B, md5 `32e18494…`, am Gerät geprüft). Zeiger in `AKTUELLER_AUFTRAG.md` auf TB-132 gesetzt (07:29). Die Vorprüfung des Auftrags lief am Gerät ohne Trockenlauf-Schalter mit `--arbeitsbaum`: rc 0 (Datum, 2 geänderte und 16 unverfolgte Dateien wie erwartet, 21 Marken an 13 Stellen, 8 Blöcke, 98 Fundstellen, 28 Zählungen). Auslöser `starte_TB-132` gelegt; der Wächter hat ihn angenommen und den Einfügesatz geschrieben (`logs/sitzungswaechter/auftragssatz_TB-132.txt`).

**Wartet.** Der Betreiber drückt im geöffneten Terminal die Eingabetaste und meldet „132 fertig“. Die Sitzung läuft nur am 03.10.2026.

**Abnahme danach.** Einfügeskript aus dem Auftrag holen und mit `--vorschau --s0 <S0> --register <Kopie>` auf das Register am `ad351d5` anwenden (Soll in der Vorschau ohne S0: sha256 `1be85dc2…`, 11 471 Zeilen, numstat 158/0); zeichengleich mit dem Register nach der Sitzung vergleichen. `docs/belege/TB-132/probe_lock_r71.txt` ansehen (Kopfzeile 3 `pandas 2.3.3, numpy 2.0.2, Python 3.9.6`, Rückgabewert 0). Bricht die Sitzung in 0e ab, ist das Register unverändert; dann die Ausgabe der Probe an Fable melden. Danach: schliessen (`schliesse_<Hash>`, frühestens 600 s nach dem letzten Commit), Ablage erneuern (54 Abschnittsdateien, Index, Dialog-Index), nächste Anfrage an Fable mit den Punkten aus 53.10 (Kalendername, Deckelfall, Marke an 23.3, sinngemässe Verweise).

## Nachtrag 04.10.2026, 08:42 — neuer steuernder Chat (Übernahme 07:34): TB-132 lief am 03.10. nicht; Neubau für den 04.10. freigegeben und gelegt; Start von Hand; Fable-Übergabe 04.10.

**Übernahme.** Geräteanbindung nach der Ordnerfreigabe lesbar, Projektablage lesbar. 07:36: HEAD `0779453` = `origin/main`, `BACKLOG.md` 287 Zeilen. TB-132 war nicht gelaufen: kein Commit von Schritt 0, `docs/belege/TB-132/` nur `vormessung/`, kein Journalblock ED. Die Sitzung, die der Wächter am 03.10. um 07:29 angelegt hatte (PID 88558), stand noch im Repo; geschlossen über `schliesse_0779453…` (Wächter-Log 04.10., 05:58:45Z: „1 Sitzung(en) mit TERM beendet, 0 noch da“).

**Neubau TB-132.** Die Fassung vom 03.10. (127 733 B, md5 `32e18494…`) ist im Arbeitsbaum ersetzt durch die Fassung mit dem Datum 04.10.2026: `docs/auftraege/MAC_TB-132_register_fable_02c.md`, 130 861 B, md5 `6aa907f480c7c2df7b700fae1b05aecc`, am Gerät mit `cmp` geprüft. Geändert: das Datum des Eintrags in 52 Zeilen; dazu vier Zusätze (Kopfzeile, Neubau-Absatz mit „Start von Hand“, zweite Freigabe, Hinweis unter „Prüfsumme“). Prüfskript und Einfügeskript sind zeichengleich (sha256 `8ef716ac…`, `c75b6e88…`). Gebaut mit einem Skript (`bau.py`, md5 `52d6c488…`), das nur im Container des steuernden Chats und im Scratch der Brücke liegt; dort liegt auch die alte Fassung. Ein Gegenleser (frischer Helfer, elf Prüfpunkte gegen alte Fassung, Diff, Wächter-Log und Zeiger) hatte keinen Befund; seine Anmerkung zum Zeiger ist nachgezogen. **Freigabe:** Auswahlkarte, gestellt gegen 08:00, gewählt „Freigeben wie beschrieben (Empfohlen)“, eingetragen 08:41; der Wortlaut steht im Auftrag. Vorprüfung am Gerät ohne Trockenlauf-Schalter mit `--arbeitsbaum` (08:41): rc 0 (Datum 04.10.2026, 2 geänderte und 16 unverfolgte Dateien, 21 Marken an 13 Stellen, 8 Blöcke, 98 Fundstellen, 28 Zählungen). Der Zeiger in `AKTUELLER_AUFTRAG.md` nennt in der Zeile TB-132 jetzt den 04.10.2026.

**Start.** Ausnahmsweise von Hand (Betreiber, 07:57: „ausnahmsweise in eine neue manuelle claude code session in der app“): neue Claude-Code-Sitzung in der App, lokal im Hauptordner `~/trading-bot`, Einfügesatz wie `logs/sitzungswaechter/letzter_satz.txt`. Kein Auslöser `starte_TB-132`. Die Sitzung läuft nur am 04.10.2026; an einem anderen Tag ist ein dritter Bau nötig.

**Abnahme danach.** Wie im Nachtrag 03.10.2026, 07:29, mit neuem Soll: Vorschau ohne S0 sha256 `b6bd4247e2cf4ccabef052a9da81e4daa5ae541588d10810fb73a1fdc3a67b84`, 11 471 Zeilen, numstat 158/0. Gegen die Vorschau der Fassung vom 03.10. (`1be85dc2…`, nachgebaut) sind genau die 21 Markenzeilen verschieden, je nur im Datum. Ob `schliesse_<Hash>` eine in der App gestartete Sitzung trifft, ist nicht gemessen; der Wächter schliesst Prozesse namens `claude`, deren Arbeitsverzeichnis das Repo ist.

**Fable.** Der Fable-Chat der Antworten 02b und 02c hat am 04.10. eine Übergabe geschrieben: Ablage `projektfuehrung/FABLE_UEBERGABE_2026-10-04_neuer_chat.md` (8 190 B, md5 `49deb8fc…`, Abschrift geprüft). Daraus der Eröffnungstext: drei Stellen eingesetzt (Erinnerungsdateien nach R56 (d), gemessen 07:46, unverändert; Registerstand; freie Nummern ab R74), ein gekennzeichneter Zusatz (Fehlerklasse: elf Fälle mit Fundstelle, 48.20 R52; die Stellen aus 01a Nr. 6 und 02c Z. 41 sind noch nicht gezählt). Ein Gegenleser fand zwei Stellen in Fables Landkarte, die den Wortlaut von 02c nicht treffen („Ausgang 2“ bei R66 (b); „vor dem Eintrag zu messen“ für R66 (b) und (c)); beide stehen im Text, Fables Wortlaut ist nicht geändert. Ablage: `projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md` (9 541 B, md5 `810ccab6…`); dem Betreiber als Kopierblock ausgegeben, 07:55. Beide Dateien liegen noch nicht im Repo, weil 0a von TB-132 die Einträge zählt; sie kommen nach der Abgabe von TB-132 ins Repo, vor einer Antwort (R56 (b)). Vorgabe: Die Anfrage 04.10.a entsteht nach der Abnahme (Punkte aus 53.10, dazu die Zählung der Fehlerklasse); die Eröffnung wird dann mit neuem Stand in Abschnitt 3 neu ausgegeben.

**Beobachtung zur Brücke.** Um 07:37:54 wurde `.git/index` neu geschrieben, zeitgleich mit dem ersten `git --no-optional-locks diff --name-only` dieses Chats; eine `index.lock` blieb nicht liegen, der Arbeitsbaum ist unverändert. Ursache nicht bewiesen. `git --no-optional-locks ls-files -m` liefert dieselbe Liste und liess den Index unberührt (gemessen); spätere Läufe von `diff --name-only HEAD` im Prüfskript (07:54, 08:41) haben ihn nicht mehr geändert. Vorgabe: über die Brücke `ls-files -m` statt `diff --name-only`.

**Stand.** HEAD `0779453`. Uncommittet: `UEBERGABE.md`, `AKTUELLER_AUFTRAG.md` und 16 unverfolgte Dateien (der Auftrag, sechs Dateien zu Fable 02.10.b und 02.10.c, neun unter `docs/belege/TB-132/vormessung/`). Nummern: TB-132 vergeben, TB frei ab 133; Journal ab ED (TB-132 nimmt ED); R66–R73 vergeben, frei ab R74; Fehler ab 20; Fable am 04.10. frei ab a.

**Wartet.** Der Betreiber legt die Sitzung in der App an und schickt den Einfügesatz ab. Der steuernde Chat schaut nach dem Commit von Schritt 0 und schreibt bis zur Abgabe nichts mehr in den Arbeitsbaum.

## Nachtrag 04.10.2026, 08:47 — Start von Hand lief in der Cloud und hörte ohne Arbeit auf; Auftrag nachgezogen, Start über den Wächter; Fehler Nr. 20

**Was geschah.** Der Betreiber hat um 08:44 die Meldung der von Hand angelegten Sitzung weitergegeben: Sie las `AKTUELLER_AUFTRAG.md` auf `main` am Commit `0779453`, fand TB-132 nicht und hörte ohne Arbeit auf. Gemessen 08:46 am Repo des Betriebsrechners: HEAD und `origin/main` `0779453`, 2 geänderte und 16 unverfolgte Dateien wie zuvor, `docs/belege/TB-132/` nur `vormessung/`, kein neuer Worktree, `.git/FETCH_HEAD` vom 29.09.2026. Erschlossen: Die Sitzung lief in der Cloud auf einem eigenen Klon.

**Fehler Nr. 20 (steuernder Chat).** Ich habe den Start von Hand in der App zugesagt und in den Auftrag geschrieben, ohne zu messen, ob eine dort neu angelegte Sitzung im Hauptordner des Betriebsrechners landet: eine Erwartung an ein Werkzeug ohne Fundstelle (ARBEITSWEISE 0). Die Wache im Einfügesatz hat gehalten („Kommt deine Nummer dort nicht vor, brich ab“). ⇒ Ein Start ausserhalb des Wächters wird erst zugesagt, wenn gemessen ist, wo die Sitzung läuft. Fehler frei ab 21.

**Nachgezogen.** Im Auftrag steht in Zeile 5 statt „Start von Hand“ der Absatz „Start“ (sonst zeichengleich mit der Fassung von 08:41): 131 271 B, md5 `3bbaa5a46ecfb8142eb9c24928c512eb`, mit `cmp` geprüft. Vorprüfung am Gerät ohne Trockenlauf-Schalter mit `--arbeitsbaum`: rc 0, Ausgabe gleich der von 08:41. Das Soll der Abnahme ist unverändert (sha256 `b6bd4247…`). Der Zeiger nennt den Start über den Wächter. Nach diesem Nachtrag legt der steuernde Chat den Auslöser `starte_TB-132`; ob der Wächter ihn angenommen hat, steht in `logs/sitzungswaechter/waechter.log`.

**Wartet.** Der Betreiber schickt den Einfügesatz ab: in der App unter der Gerätesitzung oder im Terminalfenster mit der Eingabetaste. Die Sitzung läuft nur am 04.10.2026.

## Nachtrag 04.10.2026, 09:23 — TB-132 hat abgegeben; Register zeichengleich mit dem Soll; Sitzung geschlossen; Stand für den Umzug

**Lauf.** Der Betreiber hat den Satz in der Sitzung abgeschickt, die der Wächter angelegt hatte. Commits: `57ae0d8` (Schritt 0, 08:51:37; das ist ⟨S0⟩), `f32b5c7` (0: Ausgang, Vorprüfung, Probe in der Lock-Umgebung, 08:53:04), `ee43f5f` (A: Register 53, Marken, 09:09:36), `12010b2` (B/C: BACKLOG, Registerkopie, Index, Dialog-Index, 09:10:36), `f909e71` (Abgabe: Ergebnis, Journal ED, 09:12:38), `d781f1b` (D3: porcelain nach der Abgabe, 09:12:41). HEAD = `origin/main` = `d781f1b`, Arbeitsbaum leer (gemessen 09:22). Betreiber, 09:21: „Tb132 fertig“.

**Abnahme, erster Teil (gemessen 09:23 über die Brücke).** Das Einfügeskript aus dem Auftrag am HEAD (sha256 `c75b6e88…`, gleich `docs/belege/TB-132/a4_eintrag.py`) mit `--vorschau --s0 57ae0d8 --register <Kopie>` auf das Register am `ad351d5` (11 313 Zeilen, sha256 `a7496780…`): Das Soll ist mit dem Register am HEAD und im Arbeitsbaum zeichengleich (`cmp`), sha256 `9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff`, 11 471 Zeilen, 158 dazu, 0 weg. Im Register: eine Zeile `## 53.` (Z. 11378), R66–R73 als Blöcke, 21 Marken mit „TB-132, 04.10.2026“, kein ⟨S0⟩ übrig. Probe: `probe_lock_r71_rc.txt` nennt rc 0, Zeile 3 der Ausgabe ist `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6`, Schlusszeile „Rueckgabewert 0“, stderr 0 B, `0e_pycache.txt` 0 B. Der Auftrag am HEAD ist die gelegte Fassung (md5 `3bbaa5a4…`).

**Noch nicht abgenommen (zweiter Teil, nächster Chat).** `docs/ERGEBNIS_TB-132_register_fable_02c.md` (16 501 B) lesen und jede Zahl an der Rohausgabe nachrechnen; BACKLOG-Block (287 → 297 Zeilen), Journal ED, Registerkopie (54 Abschnittsdateien), `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md` (auch: was `dialog_index.py` sonst geändert hat), die Nachweise `a5_*` und `0c_basis.txt` unter `docs/belege/TB-132/`.

**Geschlossen.** `schliesse_d781f1b…` gelegt; Wächter-Log 2026-10-04T07:23:39Z: „1 Sitzung(en) mit TERM beendet, 0 noch da.“.

**Offen, in dieser Reihenfolge.** (1) Abnahme, zweiter Teil. (2) Ablage erneuern: 54 Abschnittsdateien, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`, `UEBERGABE.md`. (3) Die zwei Fable-Dateien vom 04.10. aus der Ablage ins Repo (`FABLE_UEBERGABE_2026-10-04_neuer_chat.md`, md5 `49deb8fc…`; die Eröffnung in der Fassung, die hinausgeht), vor einer Antwort (R56 (b)). (4) Anfrage 04.10.a: die Punkte aus 53.10 (Kalendername, Deckelfall, Marke an 23.3, sinngemässe Verweise), dazu die Zählung der Fehlerklasse (Stellen aus 01a Nr. 6 und 02c Z. 41); die Eröffnung mit neuem Stand in Abschnitt 3 neu ausgeben (Register am `ee43f5f`, 11 471 Zeilen, Abschnitte 0–53, R66–R73 eingetragen als 53.1–53.8) und in der Ablage ersetzen. (5) Regelwerk nachziehen (ARBEITSWEISE 0) als Auftrag an eine Mac-Sitzung: Fehler Nr. 20 (Start ausserhalb des Wächters erst nach Messung, wo die Sitzung läuft) und `ls-files -m` statt `diff --name-only` über die Brücke.

**Stand.** HEAD `d781f1b`. Uncommittet: nur `UEBERGABE.md` (dieser Nachtrag). Keine Gerätesitzung, kein Auftrag startklar. Nummern: TB frei ab 133; Journal ab EE; R frei ab R74; Fehler ab 21; Fable am 04.10. frei ab a. Die Baudateien des Neubaus (`bau.py`, alte Fassung des Auftrags) liegen nur im Container dieses Chats und im Scratch der Brücke. Ampel gelb; Umzug jetzt, die Abnahme, zweiter Teil, macht der nächste Chat.

## Nachtrag 04.10.2026, 09:50 — TB-132 ganz abgenommen; Ablage erneuert; kein Umzug (Betreiber: „fahre einfach fort wie bisher“), Ampel rot

**Betreiber, 09:33:** „Bewerte den anderen Code Cloud Guthaben und fahre einfach fort wie bisher“. Gelesen als: nicht umziehen, hier weiterarbeiten. Der erste Halbsatz ist nicht sicher verstanden; welches Guthaben belastet wird, sieht der steuernde Chat nicht.

**Abnahme, zweiter Teil (frischer Helfer, nur lesend am Repo; 09:35–09:41).** Rund 160 Angaben des Ergebnisdokuments an Rohausgaben und Commits nachgerechnet: alle treffen; etwa 10 ohne prüfbare Quelle (z. B. „jeder Push im ersten Versuch“, eine Uhrzeit). BACKLOG: numstat 10/0, der Block steht wörtlich im Auftrag (Schritt B, Z. 211–219). Journal ED: numstat 40/0, gleich `d2_journal_block.md`, davor EC. Dialog-Index: numstat 4/2; Zeile 02a Status „offen“ → „registriert“ und offen „ja“ → „nein“, neue Zeilen 02b und 02c, Schlusszeile 52 → 54 Antworten. Register-Index: numstat 218/173, Abschnitt 53 und R66–R73 eingetragen, `c2_index_pruefen.txt` rc 0. Alle 145 berührten Pfade liegen unter `docs/`, nichts gelöscht oder umbenannt. `test_vorregistrierung`: rc 0, 892 s, 196/196. Vom steuernden Chat per Skript gemessen: Alle 54 Abschnittsdateien gleichen ihrem Registerausschnitt, die Bereiche decken Z. 1–11 471 lückenlos. **Unschärfe der Freigabetabelle (steuernder Chat, kein Verstoss der Sitzung):** Sie nannte bei 02a nur „offen → nein“; der Auftrag verlangte in Schritt C auch den Status „registriert“.

**Aus dem Ergebnis für später (noch nicht im BACKLOG):** `registerkopie.py --marken` zählt in Abschnitt 53 drei Zeilen als Marken, die keine sind; Reibung im Index, Tabelle 3, Zeile 3b (c) (Vorschlag für den nächsten Indexlauf); die Bestätigung an 48.7 steht mit dem Markenwort ERGÄNZT; beim nächsten Registerabschnitt dieser Grösse dürfte T4 die Grenze überschreiten; `registerbericht.py --pruefen` rc 1 bleibt (bekannt seit vor TB-126).

**Ablage erneuert (Helfer, 09:36–09:39).** 57 Dateien md5-gleich mit dem Gerät hochgeladen: `REGISTER_KOPIE_ABSCHNITT_00.md` bis `_53.md` (53 ist neu), `REGISTER_INDEX.md` (40 183 B, md5 `bcc69099…`), `FABLE_DIALOG_INDEX.md` (23 548 B, md5 `1b05ff40…`), `UEBERGABE.md` im Stand von 09:23 (145 713 B, md5 `b7ebbbfe…`). Dieser Nachtrag steht noch nicht in der Ablage.

**Ampel.** 09:42: Verlauf 330 374 (rot). Kein Umzug auf Anweisung des Betreibers. Der steuernde Chat liest ab hier Grosses nur über Helfer.

**In Arbeit.** Anfrage 04.10.a an Fable: Kalendername (53.10 Nr. 1), Deckelfall (Nr. 2), zur Kenntnis die Marke an 23.3 (Nr. 8) und die sinngemässen Verweise (Nr. 9), dazu die Zählung der Fehlerklasse. Eine Vormessung durch einen Helfer läuft (Wortlaute und Fundstellen); sie kommt nach `docs/belege/TB-133/vormessung/`. Die Eröffnung wird mit dem Stand nach TB-132 neu gemessen. Offen danach: die zwei Fable-Dateien vom 04.10. ins Repo, Regelwerk-Nachtrag als TB-133.

**Stand.** HEAD `d781f1b`. Uncommittet: `UEBERGABE.md`. Keine Gerätesitzung, kein Auftrag startklar. Nummern unverändert: TB frei ab 133, Journal ab EE, R ab R74, Fehler ab 21, Fable am 04.10. frei ab a.

## Nachtrag 04.10.2026, 10:03 — Anfrage 04.10.a an Fable fertig und abgelegt; Eröffnung neu gemessen; Betreiber will Cloud-Sitzungen für Leseaufgaben nutzen

**Anfrage 04.10.a.** `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md` (9 574 B, md5 `db37f969a557b60a27cbd7ac6b942def`), im Repo (uncommittet) und in der Ablage. Drei Fragen, je mit Fundstelle und Neigung: (1) Kalendername der Aktien-Tagesreihe (Neigung: „NYSE“ des Pakets im Lock, als Präzisierung zu R66 (a)); (2) Deckelfall, Proben nach R60 (c) und R36 (Neigung: Proben bleiben, zweiter attribuierter Träger; Herausrechnen, kein zweiter Lauf; 41.3 C2 ist nur über die Marke an 16.6 gelesen und so gekennzeichnet); (3) Zählung der Fehlerklasse (zwölfter Fall: 02b, R68 (c) zu R60 (c); nicht gezählt: die ersetzte Fassung 2d, weil 02b sie als Voraussetzung genannt hatte, die Kalenderquelle in R66 (a), die zwei Stellen aus 01a Nr. 6). Zur Kenntnis: Marke an 23.3, sinngemässe Verweise, Eintrag durch TB-132. Vormessung durch einen Helfer: `docs/belege/TB-133/vormessung/v1_vormessung_04a.md` (57 081 B, md5 `505ba981…`, uncommittet). Ein Gegenleser prüfte acht Punkte an der Quelle: sieben Befunde, alle eingearbeitet (darunter mein Fehler: die „14“ in R26/R30 steht in R61 (c), nicht in R62; ein Zitat ohne markierte Auslassung; `exchange-calendars` stand unter „53.9“, kommt aber aus `requirements.lock`). Keine zweite Gegenleser-Runde.

**Eröffnung.** `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md` neu, mit dem Stand nach TB-132 (9 259 B, md5 `c96f56c9682d4fb8a37188735edae7ad`), Repo und Ablage; ersetzt die Fassung von 07:54. Dazu im Repo: `FABLE_UEBERGABE_2026-10-04_neuer_chat.md` (8 190 B, md5 `49deb8fc…`). R56 (d) gemessen 09:53: unverändert. Eröffnung und Anfrage gehen als ein Kopierblock an den Betreiber (Sendetext 17 426 B, md5 `4eef7787…`).

**Betreiber, 09:55:** Er will das Guthaben für Cloud-Sitzungen von Claude Code nutzen: eine von Hand angelegte Cloud-Sitzung bekommt eine Aufgabe, antwortet mit einer Textdatei im eigenen Chat, legt nichts ab; er kopiert die Antwort in den steuernden Chat. Dafür vergeben: **TB-134** (Cloud, nur lesen: Liste der Voraussetzungen in R33–R73 mit Stand der Messung; Wortlaut 41.3 C2) und **TB-135** (Cloud, nur lesen: Anforderungen an den Zellen-Erzeuger aus R33–R73). Beide als Kopierblock ausgegeben. Eine Cloud-Sitzung sieht nur den gepushten Stand (heute `d781f1b`), keine uncommitteten Dateien, keine Lock-Umgebung, keine Daten; ihre Antwort ist Fundstellenliste, kein Nachweis, und wird an Stichproben gemessen. TB-133 bleibt der Regelwerk-Nachtrag (Mac).

**Stand.** HEAD `d781f1b`. Uncommittet: `UEBERGABE.md`; unverfolgt: `docs/belege/TB-133/vormessung/v1_vormessung_04a.md` und die drei Fable-Dateien vom 04.10. Keine Gerätesitzung. Nummern: TB frei ab 136; Journal ab EE; R ab R74; Fehler ab 21; Fable 04.10.a ausgegeben, frei ab b. Ampel rot (Verlauf über 330 000), kein Umzug auf Anweisung des Betreibers.

**Wartet.** Der Betreiber fügt den Sendetext in einen leeren Fable-Chat ein und meldet „Fable ist fertig“; die Cloud-Antworten kopiert er hierher.

## Umzug 04.10.2026, 10:56 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 10:54: „Bereite den Umzug vor damit wir im neuen Chat nahtlos weiter machen können.“ Die Nachträge vom 04.10.2026 (08:42, 08:47, 09:23, 09:50, 10:03) tragen die Einzelheiten; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **TB-132 ist gelaufen, ganz abgenommen und geschlossen:** Register Abschnitt 53 (R66–R73 als 53.1–53.8, dazu 53.9 und 53.10) und 21 Marken stehen im Register; HEAD `d781f1b`.
- **Die Anfrage 04.10.a an Fable ist hinausgegangen, und die Antwort liegt in der Ablage** (`projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md`, in der Dokumentliste gesehen um 10:54). Sie ist nicht gelesen, nicht ins Repo übertragen und nicht bewertet.
- **Zwei Leseaufgaben für Cloud-Sitzungen (TB-134, TB-135) sind als Kopierblock ausgegeben;** Antworten sind in diesem Chat nicht eingegangen.

### Block 2 — HEAD und Commits

HEAD = `origin/main` = `d781f1b` (04.10.2026, 09:12). TB-132: `57ae0d8` (Schritt 0), `f32b5c7` (0: Ausgang, Vorprüfung, Probe), `ee43f5f` (A: Register 53, Marken), `12010b2` (B/C), `f909e71` (Abgabe, Journal ED), `d781f1b` (D3). Gemessen 10:55: geändert nur `docs/projektfuehrung/UEBERGABE.md`; unverfolgt vier Dateien: `docs/belege/TB-133/vormessung/v1_vormessung_04a.md`, `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_neuer_chat.md`. Keine `index.lock`. Keine Gerätesitzung (Wächter-Log 07:23:39Z: geschlossen).

### Block 3 — Tragende Zahlen

- **Register:** Commit `ee43f5f`, 11 471 Zeilen, Abschnitte 0–53, sha256 `9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff`. Höchster Block im Register: R73.
- **BACKLOG.md** 297 Zeilen. **Journal** bis ED.
- **Ablage,** erneuert 09:39: 54 Abschnittsdateien, `REGISTER_INDEX.md` (40 183 B, md5 `bcc69099…`), `FABLE_DIALOG_INDEX.md` (23 548 B, md5 `1b05ff40…`). `UEBERGABE.md` wird mit diesem Block neu hochgeladen.
- **Fable 04.10.a:** Anfrage 9 574 B, md5 `db37f969a557b60a27cbd7ac6b942def`; Eröffnung (Datei) 9 259 B, md5 `c96f56c9682d4fb8a37188735edae7ad`; Sendetext 17 426 B, md5 `4eef7787…`; alle drei am Gerät geprüft.
- **Nummern:** TB-133 (Regelwerk-Nachtrag, Mac), TB-134 und TB-135 (Cloud, nur lesen) sind vergeben; TB frei ab 136. Journal ab EE. Fehler ab 21. Fable am 04.10. frei ab b. R im Register frei ab R74; was die Antwort 04.10.a vergibt, wird am Block gezählt.

### Block 4 — Offene Punkte, in Reihenfolge

1. **Fable-Antwort 04.10.a holen und messen:** über `project_info` finden, zwei unabhängige Abschriften, `cmp`, md5 mit Fables Angabe vergleichen, ins Repo unter `docs/projektfuehrung/`. Dann jede Fundstelle gegen Register und Code messen (Helfer mit Brückenzugriff, nur lesend), Nummern am Block zählen, nach 5b bewerten. Im Leseprotokoll nachsehen, was Fable zur Projekt-Erinnerung sagt (Punkt 5).
2. **Registerauftrag für den nächsten Abschnitt (54)** nach Bauart TB-132, Einzelfreigabe per Karte. Lehre aus TB-132: Das feste Datum des Eintrags hat einen Neubau gekostet; entweder am Tag der Freigabe starten oder das Datum zur Laufzeit einsetzen lassen (dann hängt das Soll daran, wie schon an ⟨S0⟩).
3. **Cloud-Antworten TB-134 und TB-135,** sobald der Betreiber sie einfügt: Fundstellenlisten, kein Nachweis; an Stichproben über die Brücke messen. TB-134 liefert den Wortlaut von 41.3 C2, der in Frage 2 der Anfrage als „nicht gemessen“ steht.
4. **TB-133, Regelwerk-Nachtrag** als Auftrag an eine Mac-Sitzung (Start über den Wächter): Fehler Nr. 20; `ls-files -m` statt `diff --name-only` über die Brücke; Cloud-Sitzungen nur für Leseaufgaben mit Textantwort (Betreiber, 09:55); die Punkte „für später“ aus dem Ergebnis TB-132 und die Unschärfe der Freigabetabelle in den BACKLOG (Nachtrag 09:50). Schritt 0 committet `UEBERGABE.md` und die unverfolgten Dateien.
5. **R56 (d):** `ways-of-working.md` der Projekt-Erinnerung trägt seit 04.10.2026, 10:53 MESZ einen neuen Stand (2 503 B statt 2 232 B); nicht gelesen. Vor der nächsten Eröffnung für Fable neu gegen 27.1 messen. Die übrigen drei Dateien sind unverändert (gemessen 10:55).
6. **Ablage** nach dem nächsten Registereintrag erneuern (Abschnittsdateien, Index, Dialog-Index).

### Block 5 — Wartezustände

Keine Sitzung läuft. „Fable ist fertig“ hat der Betreiber nicht gemeldet; die Antwort liegt trotzdem in der Ablage und wird ohne Meldung gelesen. Die Cloud-Antworten kopiert der Betreiber in den Chat; bis dahin wartet Punkt 3.

### Block 6 — Freigaben und Entscheide des Betreibers am 04.10.2026

- 07:57: TB-132 von Hand in einer neuen Claude-Code-Sitzung der App starten. Die Sitzung lief in der Cloud und hörte ohne Arbeit auf; danach Start über den Wächter (Vorgabe, kein Widerspruch).
- 08:41, Karte: Neubau TB-132 für den 04.10.2026, „Freigeben wie beschrieben (Empfohlen)“. Verbraucht.
- 09:33: „fahre einfach fort wie bisher“, kein Umzug trotz Ampel. 10:54: Umzug vorbereiten.
- 09:55: Das Guthaben für Cloud-Sitzungen von Claude Code nutzen: von Hand angelegte Cloud-Sitzung, Aufgabe als Kopierblock, Antwort als Textdatei im dortigen Chat, nichts wird abgelegt; der Betreiber kopiert die Antwort in den steuernden Chat.
- Vorgaben ohne Widerspruch: `ls-files -m` über die Brücke; Anfrage 04.10.a erst nach der Abnahme.
- Keine Karte offen.

### Block 7 — Fehler dieses Chats und die Regeln daraus

1. **Nr. 20:** Start von Hand in der App zugesagt und in den Auftrag geschrieben, ohne zu messen, wo eine dort angelegte Sitzung landet. ⇒ Ein Start ausserhalb des Wächters wird erst zugesagt, wenn gemessen ist, wo die Sitzung läuft.
2. **Ohne Nummer:** Das erste `git --no-optional-locks diff --name-only` über die Brücke hat vermutlich `.git/index` neu geschrieben (07:37:54; nicht bewiesen). ⇒ `ls-files -m`.
3. **Ohne Nummer, im Entwurf der Anfrage 04.10.a vom Gegenleser gefunden:** die „14“ in R26/R30 dem Block R62 zugeschrieben (sie steht in R61 (c)); ein Zitat ohne markierte Auslassung; eine Tatsache unter der Quelle „53.9“, die aus `requirements.lock` stammt. ⇒ Fundstellen nur, wenn sie vor mir liegen; der Gegenleser vor jeder Anfrage bleibt.
4. **Ampel:** Der Chat lief auf Anweisung bis 460 540 weiter (rot ab 300 000); der saubere Stand für den Umzug war 09:23 bei 289 306.
5. **Was getragen hat:** Helfer mit Brückenzugriff und der Regel „nur lesen“ haben den zweiten Teil der Abnahme, die Vormessung und das Gegenlesen erledigt, ohne Schreibzugriff auf das Repo; ein Helfer hat 57 Dateien md5-gleich in die Ablage geladen. Der steuernde Chat las nur Kurzberichte.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Die Punkte „für später“ aus `docs/ERGEBNIS_TB-132_register_fable_02c.md` (Nachtrag 09:50): `registerkopie.py --marken` zählt in Abschnitt 53 drei Zeilen als Marken, die keine sind; Reibung im Index, Tabelle 3, Zeile 3b (c); Markenwort ERGÄNZT an 48.7; T4-Grenze beim nächsten Registerabschnitt dieser Grösse; `registerbericht.py --pruefen` rc 1.
- Die Vormessung zur Anfrage 04.10.a liegt unverfolgt unter `docs/belege/TB-133/vormessung/`.
- Die Baudateien des Neubaus von TB-132 (`bau.py`, die Fassung vom 03.10. mit md5 `32e18494…`) liegen nur im Container dieses Chats und gehen mit ihm verloren. Die alte Fassung ist die neue ohne die vier Zusätze und mit dem Datum 03.10.2026.
- Zwei Stellen in der Landkarte der Fable-Übergabe vom 04.10. treffen den Wortlaut von 02c nicht; sie stehen in der Eröffnung, Abschnitt 3.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, zusammen mit diesem Umzug. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 04.10.2026, 11:24 — neuer steuernder Chat (Übernahme 10:57): Fable 04.10.a geholt, gemessen, bewertet: trägt; TB-136 vergeben

**Übernahme.** Der Ordner `~/trading-bot` war nicht verbunden; Freigabe angefordert und erhalten (10:57). Gemessen ohne `git status`: HEAD = `origin/main` = `d781f1b`, `BACKLOG.md` 297 Zeilen, geändert nur `UEBERGABE.md` (160 068 B, md5 `38963f4b…`), unverfolgt die vier genannten Dateien. Projektablage lesbar (95 Dokumente).

**Antwort 04.10.a.** Über `project_info` gefunden, zwei unabhängige Abschriften sind gleich (29 195 B, 167 Zeilen, md5 `856b2c158e4bb6870876de129ce71f76`), im Repo unter `docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md` (unverfolgt, md5 am Gerät nachgemessen). Fable nennt keine md5 der Datei. Inhalt: R74–R77, alle drei Fragen „einverstanden“; Frage 1 mit anderem Grund (17.5) und anderer Voraussetzung, Frage 2 (a) mit drei Festlegungen.

**Zählung am Block:** vier Blöcke R74–R77 (Unterpunkte a–f, a–h, a–e, a–c), 13 Marken in R77 (a) (8 PRÄZISIERT, 5 ERGÄNZT), drei Voraussetzungen in eckigen Klammern (R74 (b), R75 (a), R75 (g)). R frei ab R78.

**Bewertung (5b): R74–R77 tragen; Eintrag als Abschnitt 54 nach Einzelfreigabe.** Messung durch drei Helfer, nur lesend über die Brücke; Belege unter `docs/belege/TB-136/vormessung/` (vier Dateien, unverfolgt), die Bewertung in `v1_bewertung_fable_04a.md`:

1. **V1 (R74 (b), vor dem Eintrag) trifft:** `research/snapshotgrenze/ergebnisse/eingaben.json:96–106`, Feld `kalender`, führt `notifications/boersenkalender.py`, Zeile 81. Beifang: `paket_vorhanden` 5.4.0, der Lock führt 4.6.1.
2. **V2 (R75 (a)) trifft im Wortlaut nicht:** `mtm_kern.py` bildet keine Tagesrendite und keine Exposure, nur Kapitalreihen (`mtm = buch + unreal`, Z. 251); Unrealisiertes ist je Position summiert (Z. 244), Realisiertes kommt über `kapital_after`. Die Meldung ist fällig, bevor der Zellen-Erzeuger die Attribution baut; den Eintrag hält sie nicht auf.
3. **V3 (R75 (g)) trifft am Bestand:** Abschnitt 8 führt 13 Zeilen, keine zu `zellenbericht.csv`; R34 berichtet schon heute ohne eigene Zeile.
4. **65 Fundstellen:** jedes wörtliche Zitat gefunden, kein Verweis ins Leere. Sieben Stellen treffen sinngemäss, darunter „Die Zuteilung läuft je Zelle einmal (R45)“ (R45 sagt das nicht; es schliesst die Rekonstruktion aus der `equity_curve` aus) und „der Index führt die Zählung“ (`REGISTER_INDEX.md` führt heute keine).
5. **Marken über R77 (a) hinaus (R65 (a)), Lesart, vorläufig:** 48.14 (R46) wegen R75 (d) und (f); 48.7 (R39) auch für Unterpunkt (g). Der Auftrag bestimmt sie.
6. **Leseprotokoll:** Fable hat über `project_search` einen Ausschnitt aus `BACKLOG.md` gesehen und nach R56 (b) genannt; das Suchwort steht in der Datei nicht. Fables Ampel: rot, 468 406 nach einer Anfrage; die nächste Anfrage geht an einen neuen Chat.

**R56 (d):** Fable las `preferences.md` (9 241 B) und `ways-of-working.md` (2 232 B), wie genannt. Der neue Stand von `ways-of-working.md` (08:53 UTC) ist gelesen: Werkzeugkopf 2 482 B (oben stand 2 503 B; ungeklärt), neu eine Zeile zur Cloud-Sitzung, keine Grösse nach 27.1 gesehen. Vor der nächsten Eröffnung neu messen.

**Fehler dieses Chats, ohne Nummer:** Pfad des Index den Helfern aus dem Gedächtnis gegeben (`register_kopie/` statt `docs/projektfuehrung/`); 27.3 im Helferauftrag falsch beschrieben. ⇒ Pfade und Inhaltsangaben in Helferaufträgen nur nach `ls` und Überschrift.

**Stand.** HEAD `d781f1b`. Uncommittet: `UEBERGABE.md`; unverfolgt neun Dateien: die vier vom Umzug, die Antwort 04.10.a und vier unter `docs/belege/TB-136/vormessung/`. Keine Gerätesitzung, kein Auftrag startklar. Nummern: TB-136 (Registerauftrag Abschnitt 54, Mac) vergeben, TB frei ab 137; Journal ab EE; R frei ab R78; Fehler ab 21; Fable am 04.10. frei ab b. Ampel 11:24: grün, Verlauf 164 436 (Grundlast 127 365).

**Wartet.** Die Cloud-Antworten TB-134 und TB-135 fügt der Betreiber ein. Sonst wartet nichts auf ihn.

**Als Nächstes:** TB-136 schreiben nach Bauart TB-132 (Verweis auf den Vorgänger, nur Unterschiede und Sollwerte): Abschnitt 54 mit R74–R77 zeichengleich aus der Antwortdatei, Kopf mit Datei, md5 und Commit (R56 (b)), Befunde der Vormessung, Marken (13 von Fable, dazu die des steuernden Chats), Indexzeilen, Dialog-Index, BACKLOG, Journal EE. Schritt 0 committet den Arbeitsbaum und misst V1 am Gerät nach. Das Datum des Eintrags wird zur Laufzeit eingesetzt. Prüfskript vor der Freigabe am echten Repo, Gegenleser, Karte zur Einzelfreigabe. Danach die Cloud-Antworten messen, dann TB-133.

## Umzug 04.10.2026, 13:17 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, auf die Freigabekarte zu TB-136 (gestellt gegen 13:12): „Wir machen eine Pause“. Das ist keine Freigabe und keine Ablehnung: TB-136 ist nicht freigegeben und nicht gestartet. Die Ampel steht auf rot; deshalb der Umzug vor der Pause. Die Nachträge vom 04.10.2026 (11:24) tragen die Bewertung von Fable 04.10.a; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **Fable 04.10.a ist bewertet: trägt** (R74–R77; Nachtrag 11:24; Bewertung in `docs/belege/TB-136/vormessung/v1_bewertung_fable_04a.md`).
- **TB-136 (Register Abschnitt 54, 15 Marken) ist gebaut und zweimal gegengelesen** und liegt als Entwurf im Repo: `docs/auftraege/MAC_TB-136_register_fable_04a.md` (unverfolgt, 128 746 B, md5 `a42eacf11713b15fc6d57ced2f50daa0`). Der Platzhalter `⟨⟨FREIGABE⟩⟩` steht noch darin (einmal, Z. 12). **Es fehlt die Einzelfreigabe des Betreibers.**
- **Die Cloud-Antworten TB-134 und TB-135 sind eingegangen,** abgelegt unter `docs/belege/TB-134/` und `docs/belege/TB-135/` und gemessen (Block 4 Nr. 3).

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `d781f1b`. Gemessen 13:17 ohne `git status`: geändert nur `docs/projektfuehrung/UEBERGABE.md`; unverfolgt 12 Dateien: `docs/auftraege/MAC_TB-136_register_fable_04a.md`; `docs/belege/TB-133/vormessung/v1_vormessung_04a.md`; `docs/belege/TB-134/CLOUD_TB-134_antwort_offene_voraussetzungen.md`; `docs/belege/TB-135/CLOUD_TB-135_antwort_anforderungen_zellen_erzeuger.md`; vier unter `docs/belege/TB-136/vormessung/`; unter `docs/projektfuehrung/` `FABLE_ANFRAGE_2026-10-04a_…`, `FABLE_ANTWORT_2026-10-04a_…`, `FABLE_UEBERGABE_2026-10-04_eroeffnung.md`, `FABLE_UEBERGABE_2026-10-04_neuer_chat.md`. `docs/auftraege/AKTUELLER_AUFTRAG.md` ist unverändert und zeigt noch auf TB-132. Kein Auslöser gelegt, keine Gerätesitzung, keine `index.lock`.

⚠️ Schritt 0a von TB-136 erwartet genau: geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`, unverfolgt diese 12 Dateien. Jede weitere Datei im Arbeitsbaum bricht 0a ab.

### Block 3 — Tragende Zahlen

- **Register** unverändert: Commit `ee43f5f`, 11 471 Zeilen, sha256 `9a2cefb7…71ff`, md5 `1ce393ae2f07513fa76ccc0b0f927d41`. Höchster eingetragener Block R73.
- **Antwort 04.10.a:** 29 195 B, 167 Zeilen, md5 `856b2c158e4bb6870876de129ce71f76`; Anfrage md5 `db37f969…`, Eröffnung md5 `c96f56c9…`.
- **TB-136, Sollwerte aus der Simulation** (Container, an geprüften Kopien): Register 11 471 → 11 581, eingefügt 110 (15 Marken × 3 + Abschnitt 54 = 65), entfernt 0; 15 Marken an 15 Einfügestellen (13 nach R77 (a), zwei des steuernden Chats an 48.1 R33 und 48.14 R46); Abschnitt 54 = 54.1–54.4 (R74–R77), 54.5 Voraussetzungen und Befunde, 54.6 Was offen bleibt. Prüfskript sha256 `2dbc5a55afaecc99c3df35520454720b71dad5ed4d12213f9e91a48532ab15bb`, Einfügeskript sha256 `99881a1b69b9c72a24948d68b839d1c6664db87005d40c81fc407fd159659ea5`. Datum zur Laufzeit (`⟨DATUM⟩`, Schalter `--datum`). Die Registerkopie bekommt einen fünften Teil (Abschnitt 54 allein, gerechnet rund 24 700 B).
- **Am echten Repo gelaufen, nur lesend, Python 3.10 der Brücke:** Prüfskript rc 1 mit genau einer Abweichung (Freigabe-Platzhalter); 0e rc 0, 25 von 25. Nach den drei letzten Textersetzungen (Auftrag Z. 330 und Z. 415) ist das Prüfskript nicht noch einmal gelaufen; die Skripte selbst sind unverändert.
- **Nummern:** TB-136 vergeben (Registerauftrag Abschnitt 54, Mac), TB-133 (Regelwerk-Nachtrag, Mac), TB-134 und TB-135 (Cloud) vergeben und beantwortet; TB frei ab 137. Journal ab EE. R74–R77 sind in 04a vergeben und nicht eingetragen; neue Blöcke ab R78. Fehler ab 21. Fable am 04.10. frei ab b.
- **Ablage:** `UEBERGABE.md` mit diesem Block neu hochgeladen. Abschnittsdateien, Index und Dialog-Index stehen auf dem Stand von 09:39.

### Block 4 — Offene Punkte, in Reihenfolge

1. **Freigabe TB-136 einholen** (Karte, Einzelfreigabe). Kartentext, damit er zur Freigabetabelle des Auftrags passt: „Gibst du TB-136 frei? Das umfasst: Register Abschnitt 54 anhängen (R74–R77 zeichengleich aus Fables Antwort 04.10.a, dazu 54.5–54.6 mit den Messungen des steuernden Chats), 15 Marken am alten Ort (13 nach R77 (a), zwei an 48.1 und 48.14 vom steuernden Chat nach R65 (a) bestimmt; keine in Abschnitt 9, Abschnitt 10 und im ERZEUGT-Block), vorher die Nachmessung der Voraussetzungen am Gerät (bei Abweichung kein Eintrag), Registerkopie, Index und Dialog-Index neu, BACKLOG-Block, Journal EE. Prüfungen am Register: test_vorregistrierung vor dem Commit, registerbericht.py --pruefen, numstat 110/0. Kein Code, kein neues Abbild. Datum des Eintrags: der Tag, an dem die Sitzung einträgt.“ Nach „Freigeben“:
   a. `⟨⟨FREIGABE⟩⟩` ersetzen in der Form von TB-132 Z. 11: fett Datum und „Auswahlkarte im steuernden Chat (gestellt gegen HH:MM, Antwort eingetragen HH:MM).“, dann `Kartentext: *„…“*` im ganzen Wortlaut, dann `Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**.`
   b. Auftrag neu ablegen (frischer Stage-Pfad), md5 beidseitig; Prüfskript am echten Repo ohne `--arbeitsbaum`, mit `--datum`: erwartet rc 0.
   c. `docs/auftraege/AKTUELLER_AUFTRAG.md`, Zeile 39 und Zeile 52, nach `aktueller_auftrag_aenderung.md` (im Archiv, Block 8) ändern; md5 beidseitig.
   d. Diesen Stand in `UEBERGABE.md` nachtragen, **bevor** der Auslöser liegt; danach im Arbeitsbaum nichts mehr anfassen.
   e. Auslöser `docs/auftraege/_ausloeser/starte_TB-136` (leer); Wächter-Log auf „Satz ins Fenster gelegt“ prüfen; Nachschau auf den Schritt-0-Commit.
2. **Nächste Anfrage an Fable** (04.10.b, neuer Fable-Chat; Fables Chat stand bei 468 406): zur Kenntnis die Meldung zu R75 (a), die zwei Marken des steuernden Chats, die sechs sinngemässen Verweise, der Ausschnitt aus `BACKLOG.md` im Leseprotokoll (alles in 54.5 und 54.6 des Auftrags). Vorher `ways-of-working.md` der Projekt-Erinnerung neu gegen 27.1 messen (Werkzeugkopf 2 482 B; oben stand 2 503 B).
3. **Cloud-Antworten, gemessen an Stichproben und Vollzählungen** (Helfer, Register-Kopie sha256-gleich): **TB-134** nennt 12 Klammern „[Voraussetzung“ in 10 Blöcken; im Register stehen ab 48.1 **17 in 11 Blöcken**, es fehlen die fünf in R48 (48.16, Z. 10911–10917; Tabelle 50.1 führt sie). Die 12 genannten treffen zeichengleich; 41.3 C2 (Z. 8870–8884) zeichengleich; „Attribution je Position“ 7 Vorkommen, wie genannt. **TB-135** trägt: 83 Sätze, alle zeichengleich; Code-Treffer (21 in 7 Dateien, 33 in 6) und 17 Punkte aus TB-120 treffen; fünf Sätze mit „Zellen-Erzeuger“ fehlen in der Fundliste (Überschriften 48.7 und 48.14, Titelsätze R39 und R46, Quelle des Grundes von R68). Für die Anforderungsliste des Zellen-Erzeugers kommen R74 und R75 dazu (54.6 Nr. 3 bis 5 des Auftrags). Der Messbericht liegt im Archiv.
4. **TB-133, Regelwerk-Nachtrag** (Mac, Start über den Wächter), wie im Umzug 10:56, Block 4 Nr. 4. Dazu aus diesem Chat: Die Suche der Ablage liefert Ausschnitte gesperrter Dateien; Fables Ampel nach einer Anfrage (Probe F4); die Bezeichnung „Frühere Vierteilung“ im Index bei fünf Teilen; Pfade und Inhaltsangaben in Helferaufträgen nur nach `ls` und Überschrift; Zeilenangaben, die in Registertext gehen, misst ein zweiter Helfer.
5. **Ablage** nach dem Registereintrag erneuern (Abschnittsdateien 0–54, Index, Dialog-Index).

### Block 5 — Wartezustände

Keine Sitzung läuft, kein Auslöser liegt. Die Freigabekarte zu TB-136 ist offen. Auf den Betreiber wartet nur sie.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- Gegen 11:27, Karte: „TB-136 hier bauen“ (gegen die Empfehlung, vorher umzuziehen).
- 11:53: Cloud-Antworten TB-134 und TB-135 eingefügt.
- Gegen 13:15, Karte zur Freigabe von TB-136: „Wir machen eine Pause“. Keine Freigabe.
- Vorgaben ohne Widerspruch: Nummer TB-136; Datum des Eintrags zur Laufzeit; Cloud-Antworten unter `docs/belege/TB-134/` und `docs/belege/TB-135/`; der Kopf „Frühere Vierteilung“ im Index bleibt zeichengleich.
- Keine Karte ist beantwortet offen ausser der Freigabe.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. Den Helfern den Pfad des Index und den Inhalt von 27.3 aus dem Gedächtnis gegeben. ⇒ Pfade und Inhaltsangaben in Helferaufträgen nur nach `ls` und Überschrift.
2. In 54.5 die Zeile „02b Z. 128“ aus einem Helferbericht übernommen; richtig ist Z. 127. Gefunden vom Gegenleser. ⇒ Zeilenangaben, die in Registertext gehen, misst ein zweiter Helfer an der Quelle.
3. Im Chat eine Marke an 48.7 (R39) angekündigt, bevor die Markentabelle gemessen war; richtig sind 48.1 und 48.14. ⇒ Eigene Marken erst nach der Markentabelle nennen.
4. Ampel: Übernahme und Bewertung der Fable-Antwort kosteten 173 189; der Bau von TB-136 im selben Chat führte auf 358 513 (rot ab 300 000). ⇒ Der Chat, der eine Fable-Antwort bewertet, baut nicht auch den Registerauftrag.
5. Was getragen hat: Der Erbauer arbeitete nur an geprüften Kopien im Container (`device_stage_files`), nicht am Repo; drei Gegenleser, eng zugeschnitten; Prüfskript und 0e liefen nur lesend am echten Repo, mit `python3 -B` und Ausgabe ausserhalb von `mnt/`.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Das Baumaterial von TB-136 liegt als Archiv auf dem Mac unter `logs/steuernder_chat/2026-10-04_tb136_bau.tar.gz` (3 154 513 B, md5 `42488dbb66e990bcc6d35434e7caca33`): Vorgabe des steuernden Chats, Bauplan, Markenkandidaten, Baubericht, die drei Gegenleseberichte, die Bau-Pipeline (Teile, Skripte, Simulationsbericht), `aktueller_auftrag_aenderung.md` und der Messbericht zu den Cloud-Antworten. `logs/` wird von git ignoriert (`.gitignore` Z. 27); das Archiv ist nicht committet und steht nicht im Arbeitsbaum.
- Die Punkte „für später“ aus dem Umzug 10:56, Block 8, gelten unverändert (Marken-Zählung in `registerkopie.py --marken`, Tabelle 3 Zeile 3b (c), Markenwort an 48.7, `registerbericht.py --pruefen` rc 1); die T4-Grenze ist in TB-136 als fünfter Teil geführt.
- Die Vormessung zur Anfrage 04.10.a liegt weiter unverfolgt unter `docs/belege/TB-133/vormessung/`; Schritt 0 von TB-136 committet sie mit.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, zusammen mit diesem Umzug. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 04.10.2026, 18:15 — nach der Pause, im selben Chat: Cloud-Sammelauftrag TB-137 geschrieben und ausgegeben

**Betreiber, 18:10:** „Erstelle mir eine umfangreiche Aufgabenliste, die ich in Claude Code Cloud übergeben kann.“ Dazu: Punkte aus dem Backlog dürfen hinein, es wird nur Claude Code Cloud benutzt (das freie Guthaben), „Diese kann gerne auch bis morgen durchlaufen.“ Am Schluss soll die Cloud-Sitzung ein Gesamtergebnis ausgeben, samt dem, was sie schon geliefert hat.

**TB-137, Sammelauftrag an eine Cloud-Sitzung:** 18 Leseaufgaben und Paket 0 (die schon gelieferten Antworten TB-134 und TB-135). Nur lesen, nichts ausführen, nichts ablegen, Sichtschutz wie bei TB-134/TB-135. Pakete: 1 Berichtigung TB-134 (17 Klammern statt 12) · 2 Ergänzung TB-135 · 3 Abnahmeliste nach R46 · 4 Marken vorwärts · 5 Marken rückwärts (R65 (a)) · 6 Ketten · 7 Verweise und Zitate in R33–R73 · 8 Was vor dem Tag fällig ist, gegen `PLAN_VOR_DEM_TAG.md` · 9 Sperrliste · 10 Zellen-Erzeuger, Bestand am Code · 11 Kern der MtM-Reihe (für die Meldung zu R75 (a)) · 12 Kalender und Paketfassungen · 13 Python 3.9 · 14 Durchsicht des Backlogs · 15 Regelwerk mit Entwurf für TB-133 · 16 Übergabe · 17 Einstiegsdokumente · 18 Index. Als Kopierblock im Chat ausgegeben; Kopie auf dem Mac unter `logs/steuernder_chat/CLOUD_TB-137_sammelauftrag_leseaufgaben.md` (15 954 B, md5 `2d1cc4db26ba9879aad2f6a930e469d9`), von git ignoriert, nicht im Arbeitsbaum.

**Gemessen vor dem Schreiben:** Die im Auftrag genannten Pfade sind am HEAD verfolgt. `registerbericht.py` und `snapshot.py` liegen nicht an den vermuteten Orten und stehen deshalb nicht im Auftrag. Die Cloud-Sitzung sieht nur den gepushten Stand `d781f1b`: kein R74–R77, kein TB-136, keine Belege vom 04.10. Den einen Satz aus R75 (a), den Paket 11 braucht, trägt der Auftrag im Wortlaut.

**Stand unverändert:** HEAD `d781f1b`, geändert nur `UEBERGABE.md`, zwölf unverfolgte Dateien, keine Sitzung, kein Auslöser. TB-136 ist nicht freigegeben; die Freigabekarte ist offen. Nummern: TB-137 vergeben, TB frei ab 138; sonst wie im Umzug 13:17, Block 3.

**Wartet.** Das Gesamtergebnis `GESAMTERGEBNIS_CLOUD_TB-137.md` fügt der Betreiber ein, wenn die Cloud-Sitzung fertig ist — in den neuen steuernden Chat. **Abnahme:** Fundstellenlisten sind kein Nachweis; an Stichproben über die Brücke messen. Paket 1 und 2 gegen den Messbericht im Archiv (`cloud/c1_stichproben_cloud_tb134_tb135.md`); Paket 3 gegen 54.6 Nr. 6 des Auftrags TB-136; Paket 5 liefert Kandidaten für Marken, die Entscheidung bleibt beim steuernden Chat und bei Fable.

**Ampel 18:15:** rot, Verlauf 406 252 (Grundlast 127 365). Dieser Chat arbeitet nach diesem Nachtrag nicht weiter; der Eröffnungstext von 13:17 gilt, mit dem Nachsatz zu diesem Nachtrag.

## Nachtrag 04.10.2026, 21:07 — neuer steuernder Chat (Übernahme 20:57): TB-136 freigegeben, Freigabe eingesetzt, Prüfskript rc 0, Zeiger gesetzt; der Auslöser folgt nach diesem Nachtrag

**Übernahme.** Geräteanbindung nach Freigabe des Ordners `~/trading-bot` (20:57); die Projektablage ist lesbar (`project_info`). Gemessen 20:58 ohne `git status`: HEAD = `origin/main` = `d781f1b`, `BACKLOG.md` 297 Zeilen; geändert nur `UEBERGABE.md` (178 070 B, md5 `d31122adc45c1683f9521812cf0f9416`), 12 unverfolgte Dateien wie im Umzug 13:17, Block 2; Auftragsentwurf 128 746 B, md5 `a42eacf11713b15fc6d57ced2f50daa0`, Platzhalter einmal in Z. 12; keine `index.lock`, kein Auslöser; Archiv md5 `42488dbb…ca33`.

**Freigabe.** Auswahlkarte im steuernden Chat (gestellt gegen 21:00, Antwort eingetragen 21:04), Kartentext im Wortlaut aus dem Umzug 13:17, Block 4 Nr. 1 (vom Skript aus dieser Datei gelesen, 684 Zeichen): „Freigeben wie beschrieben (Empfohlen)“. Der Freigabetext steht im Auftrag an der Stelle des Platzhalters (Z. 12), in der Form von TB-132 Z. 11.

**Gelegt.** `docs/auftraege/MAC_TB-136_register_fable_04a.md`: 129 596 B, md5 `95bffeb29976fc2b08b7160281d6b144`, beidseitig geprüft; gegenüber dem Entwurf ist nur Z. 12 geändert, der Platzhalter kommt 0-mal vor. Prüfskript aus dem Archiv (sha256 `2dbc5a55…15bb`) am echten Repo, ohne `--arbeitsbaum`, mit `--datum 04.10.2026`, `python3 -B` (3.10.12 der Brücke), Ausgabe ausserhalb von `mnt/`: **rc 0** (15 Marken an 15 Einfügestellen; Anker mit Zahl 1: 15 von 15, im Original und nach der Simulation; 4 Blöcke; 3 Dateien, 45 Fundstellen, 13 Zählungen). Zeiger: `docs/auftraege/AKTUELLER_AUFTRAG.md` Z. 39 und Z. 52 nach `aktueller_auftrag_aenderung.md` (Archiv) auf TB-136 gesetzt, „Gesetzt 04.10.2026, 21:04“; 7 538 B, md5 `1717b067759e8a2aab136afc8d09a218`, beidseitig geprüft; geändert genau Z. 39 und Z. 52; gegenüber `AKTUELLER_AUFTRAG_neu.md` aus der Simulation weicht nur die Zeit ab.

**Arbeitsbaum vor dem Auslöser** (gemessen 21:05 mit `ls-files -m` und `ls-files --others --exclude-standard`): geändert `docs/projektfuehrung/UEBERGABE.md` und `docs/auftraege/AKTUELLER_AUFTRAG.md`, unverfolgt die 12 Dateien — der Stand, den Schritt 0a erwartet. Nach diesem Nachtrag fasst der steuernde Chat im Arbeitsbaum nichts mehr an, bis die Sitzung abgegeben hat.

**Auslöser.** `docs/auftraege/_ausloeser/starte_TB-136` (leer) wird unmittelbar nach diesem Nachtrag gelegt. Ob der Wächter ihn angenommen hat, steht nicht hier: Das zeigen `logs/sitzungswaechter/waechter.log` und der Schritt-0-Commit.

**Abnahme danach.** Sollwerte im Umzug 13:17, Block 3: Register 11 471 → 11 581 Zeilen, numstat 110/0, 15 Marken an 15 Einfügestellen, Abschnitt 54 mit 54.1–54.6, Registerkopie mit fünftem Teil. Bricht die Sitzung in der Nachmessung der Voraussetzungen ab, ist das Register unverändert. Danach: schliessen (`schliesse_<Hash>`, frühestens 600 s nach dem letzten Commit), Ablage erneuern (Abschnittsdateien 0–54, Index, Dialog-Index), Anfrage 04.10.b an Fable (neuer Fable-Chat; vorher `ways-of-working.md` gegen 27.1 messen), TB-133. Das Gesamtergebnis zu TB-137 steht noch aus.

**Eigener Fehler (ohne Nummer).** Ein `git --no-optional-locks diff --numstat` auf `AKTUELLER_AUFTRAG.md` über die Brücke (21:05), obwohl die Vorgabe für diesen Chat nur `rev-parse`, `log`, `show`, `ls-files` und `worktree list` nennt. Danach gemessen: keine `index.lock`. ⇒ Zeilenbilanzen über die Brücke mit `diff` zweier Kopien ausserhalb des Repos messen, nicht mit git.

**Nummern** unverändert: TB-137 vergeben, TB frei ab 138; Journal ab EE; R74–R77 vergeben und noch nicht eingetragen, neue Blöcke ab R78; Fehler ab 21; Fable am 04.10. frei ab b.

**Ampel 21:06:** grün, Verlauf 63 592 (Grundlast 127 557).

## Nachtrag 05.10.2026, 21:20 — selber steuernder Chat: TB-136 hat am 04.10. nicht gearbeitet; Stand unverändert, Prüfskript rc 0 mit dem Datum 05.10.2026; der Auslöser wird neu gelegt

**Betreiber, 05.10.2026, 21:17:** „weiter“.

**Gemessen 21:18, ohne `git status`.** HEAD = `origin/main` = `d781f1b`; kein Commit seit dem Auslöser vom 04.10.2026, 21:07. Register unverändert (11 471 Zeilen, md5 `1ce393ae2f07513fa76ccc0b0f927d41`). Unter `docs/belege/TB-136/` liegt nur `vormessung/`. Geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`, unverfolgt die 12 Dateien; keine `index.lock`. Auftrag md5 `95bffeb29976fc2b08b7160281d6b144`, Zeiger md5 `1717b067759e8a2aab136afc8d09a218`, beide wie am 04.10. gelegt. `waechter.log` trägt nach „Satz ins Fenster gelegt. ER IST NICHT ABGESCHICKT.“ (04.10.2026, 21:07:30) keinen weiteren Eintrag. ⇒ Der Satz ist bei keiner arbeitenden Sitzung angekommen. Ob das Fenster vom 04.10. noch offen ist, ist über die Brücke nicht messbar.

**Was weiter gilt.** Die Einzelfreigabe vom 04.10.2026 (Karte; im Auftrag Z. 12). Der Auftrag trägt kein festes Datum: Die Sitzung setzt das Datum des Eintrags zur Laufzeit ein (`AKTUELLER_AUFTRAG.md` Z. 39: „sie läuft an jedem Tag“). Deshalb kein Neubau und keine neue Freigabe. Prüfskript (sha256 `2dbc5a55…15bb`) am echten Repo, ohne `--arbeitsbaum`, mit `--datum 05.10.2026`, `python3 -B`, Ausgabe ausserhalb von `mnt/`: **rc 0**; die Ausgabe gleicht dem Lauf vom 04.10. bis auf die Datumszeile.

**Auslöser.** `docs/auftraege/_ausloeser/starte_TB-136` wird unmittelbar nach diesem Nachtrag neu gelegt. Läuft im Repo noch eine claude-Sitzung (das Fenster vom 04.10.), weist der Wächter den Start ab und nennt PID, Laufzeit und Zustand (`docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` Z. 244); dann genügt Enter im alten Fenster. Sonst öffnet er ein neues Fenster und legt den Satz hinein. Was davon eintrat, steht in `logs/sitzungswaechter/waechter.log`, nicht hier. Nach diesem Nachtrag fasst der steuernde Chat im Arbeitsbaum nichts an, bis die Sitzung abgegeben hat.

**Seit dem Nachtrag 04.10.2026, 21:07, dazugekommen (ausserhalb des Arbeitsbaums).** `logs/steuernder_chat/FABLE_04b_bauplan.md` (4 817 B, md5 `fdcf2ff19f709189c37e54fc25209e04`, von git ignoriert): Bauplan der nächsten Anfrage an Fable — Frage 1 Meldung zu R75 (a), Frage 2 Marken an 48.1 und 48.14, zur Kenntnis die sechs sinngemässen Verweise, der `BACKLOG.md`-Ausschnitt im Leseprotokoll und der Eintrag durch TB-136. `ways-of-working.md` der Projekt-Erinnerung gegen 27.1 gemessen (gelesen 04.10.2026, gegen 21:09): Stand 08:53 UTC, 2 482 B nach dem Werkzeugkopf, 0 Treffer; die 2 503 B aus dem Umzug 10:56 sind nicht nachvollzogen. Unmittelbar vor dem Absenden der Eröffnung alle vier Erinnerungsdateien neu messen. Vorgabe des steuernden Chats (04.10.2026, 21:11; kein Widerspruch im Chat): Die Anfrage wird erst fertig geschrieben, wenn Abschnitt 54 eingetragen ist und TB-137 die Pakete 3, 5 und 11 geliefert hat. Das Gesamtergebnis zu TB-137 ist in diesem Chat nicht eingegangen (Stand 21:18). Am 04.10. ging keine weitere Anfrage an Fable hinaus; die nächste trägt das Datum des Tages, an dem sie hinausgeht.

**Fehler dieses Chats (ohne Nummer), zu dem vom 04.10. dazu.**
1. T7 erneut: den Bauplan nach dem Schreiben im selben Stage-Pfad geändert und abgelegt; am Gerät kam die alte Fassung an (4 733 B statt 4 817 B), „written“ war gemeldet. Die md5-Prüfung hat es gezeigt; aus einem frischen Pfad neu abgelegt.
2. Beim Lesen von 54.5 und 54.6 den Zeilenbereich bis vor die nächste Überschrift gezogen und rund 15 KB statt rund 7 KB in den Chat geholt, obwohl die Bytes vorher gemessen waren. ⇒ Einen Ausschnitt aus einem Codeblock an der schliessenden Zaunzeile schneiden, nicht an der nächsten Überschrift; weicht die gemessene Grösse von der erwarteten ab, zuerst den Bereich prüfen.

**Nummern** unverändert: TB-137 vergeben, TB frei ab 138; Journal ab EE; R74–R77 vergeben und noch nicht eingetragen, neue Blöcke ab R78; Fehler ab 21.

**Ampel 21:18:** grün, Verlauf 136 176 (Grundlast 127 557).

## Nachtrag 05.10.2026, 21:27 — Betreiber: die Claude-Code-Sitzung zukünftig wieder vom steuernden Chat anlegen; die Sitzung vom 04.10. wird geschlossen, TB-136 frisch über den Wächter gestartet

**Betreiber, 05.10.2026, 21:25:** „Legst du mir zukünftig wieder bereits eine claude code Sitzung an“.

**Lesart des steuernden Chats, vorläufig** (stehende Anforderung nach ARBEITSWEISE 15). Ist ein Mac-Auftrag startklar, legt der steuernde Chat die Claude-Code-Sitzung selbst über den Sitzungswächter an, bevor er dem Betreiber „Satz abschicken“ als Aufgabe gibt: Der Betreiber findet eine frische Sitzung mit dem Satz vor. Weist der Wächter den Start ab, weil im Repo eine alte Sitzung schläft, und hat diese nicht gearbeitet, schliesst der steuernde Chat sie über den Schliess-Auslöser und startet neu, ohne Rückfrage. „Nicht gearbeitet“ wird gemessen: kein Commit seit ihrem Start, letzter Commit älter als 600 s, nichts Neues unter dem Belegordner des Auftrags, Rechenzeit zwischen zwei Abweisungen des Wächters praktisch unverändert. Anlass: Am 05.10.2026, 21:20 hat der Wächter den neuen Auslöser abgewiesen (Sitzung vom 04.10., PID 52163), und der steuernde Chat hat dem Betreiber das Fenster vom Vortag überlassen, statt eine frische Sitzung anzulegen.

**Gemessen vor dem Schliessen (21:26).** HEAD `d781f1b8f86ca3b423b4032220ad4b304e4d131b`, Alter des letzten Commits 130 405 s; kein Commit seit dem Auslöser vom 04.10.; unter `docs/belege/TB-136/` nur `vormessung/`; geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`, unverfolgt 12. Rechenzeit der Sitzung PID 52163 nach `waechter.log`: 6:56.60 (21:20:28) und 6:58.19 (21:26:16), Zustand S+. Sie hat nicht gearbeitet.

**Träger nach ARBEITSWEISE 15.** Erinnerung: eingetragen 05.10.2026 in `ways-of-working.md` der Projekt-Erinnerung, Abschnitt Delegation, mit dem Wortlaut des Betreibers; die Datei hat dadurch 2 723 B statt 2 482 B und einen neuen Stand — vor der nächsten Eröffnung für Fable neu gegen 27.1 messen. `ARBEITSWEISE.md` (Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“, und 6b, Start) und der Backlog-Nachtrag: **noch nicht eingetragen.** Der Arbeitsbaum bleibt bis zur Abgabe von TB-136 so, wie Schritt 0a ihn erwartet (genau zwei geänderte Dateien); beide Einträge gehen in TB-133 (Regelwerk-Nachtrag). Projektablage: diese Datei, mit diesem Nachtrag hochgeladen.

**Danach, in dieser Reihenfolge.** Schliess-Auslöser `schliesse_d781f1b8f86ca3b423b4032220ad4b304e4d131b`, dann `starte_TB-136`. Was eintrat, steht in `logs/sitzungswaechter/waechter.log`, nicht hier. Im Arbeitsbaum fasst der steuernde Chat danach nichts an, bis die Sitzung abgegeben hat.

**Ampel 21:27:** grün, Verlauf 171 158 (Grundlast 127 557).

## Umzug 05.10.2026, 22:31 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 05.10.2026, 22:25: „tb136 fertig“. Die Sitzung hat abgegeben, alles ist committet und gepusht, die Sitzung ist geschlossen. Die Ampel steht auf gelb (Verlauf 203 404); das ist der saubere Stand für den Umzug. Die Nachträge vom 04.10.2026 (21:07) und vom 05.10.2026 (21:20, 21:27) tragen die Einzelheiten; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **TB-136 ist gelaufen und im Kern abgenommen:** Register Abschnitt 54 (R74–R77 als 54.1–54.4, dazu 54.5 und 54.6) und 15 Marken sind eingetragen, Datum des Eintrags 05.10.2026. Der Soll-Bau des steuernden Chats ist bytegleich mit dem Register am HEAD.
- **Nicht gemessen sind die Schritte B und C der Sitzung** (BACKLOG-Block, Registerkopie, Index, Dialog-Index); **die Ablage ist noch auf dem Stand vor TB-136** (Abschnittsdateien 0–53).
- **TB-137 (Cloud-Sammelauftrag) ist ausgegeben; das Gesamtergebnis ist nicht eingegangen.** Die nächste Anfrage an Fable ist geplant, nicht geschrieben.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `67a2202` (`67a22025a0c867d03456c7857ea1a4ac124fd5b2`). Gemessen 22:30 ohne `git status`: nichts geändert, nichts unverfolgt, keine `index.lock`, kein Auslöser, keine Sitzung (Schliess-Auslöser 22:26, Wächter: „1 Sitzung(en) mit TERM beendet, 0 noch da“). Mit diesem Block ist `docs/projektfuehrung/UEBERGABE.md` wieder geändert und uncommittet; sonst nichts. Commits von TB-136: `753ae38` (Schritt 0, = ⟨S0⟩), `e9bf3c0` (0), `9b7b060` (A, der einzige, der das Register ändert), `d55e7ed` (B/C), `87461f9` (Abgabe), `67a2202` (D3). `docs/auftraege/AKTUELLER_AUFTRAG.md` zeigt auf TB-136; der Auftrag ist erledigt mit `67a2202`, 05.10.2026.

### Block 3 — Tragende Zahlen

- **Register:** Commit `9b7b060`, 11 581 Zeilen, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc`, md5 `757cda8cb86e7c43fa6342ca41e56765`. Abschnitt 54 in Z. 11518–11581 (54.1 Z. 11522, 54.2 Z. 11529, 54.3 Z. 11536, 54.4 Z. 11543, 54.5 Z. 11550, 54.6 Z. 11566). Höchster eingetragener Block R77.
- **Abnahme, gemessen 22:27–22:30** (Helfer, nur lesend; vom steuernden Chat an der Rohausgabe nachgerechnet): Einfügeskript `docs/belege/TB-136/a4_eintrag.py` sha256 `99881a1b…59ea5`; Soll-Bau `--vorschau --s0 753ae38 --datum 05.10.2026` auf das Register am `d781f1b` (11 471 Zeilen, md5 `1ce393ae…`): `cmp` rc 0 gegen das Register am HEAD; eingefügt 110, entfernt 0; 15 von 15 Marken an den Zeilen der Auftragstabelle. Aus den Belegen der Sitzung: Nachmessung der Voraussetzungen 25 von 25 `ok`, rc 0; `test_vorregistrierung` 196/196; `a5_numstat.txt` `110	0`; `d3_porcelain.txt` leer. Die Sitzung meldet keine Rückfrage und kein Abbruchkriterium.
- **Ergebnis der Sitzung:** `docs/ERGEBNIS_TB-136_register_fable_04a.md` (19 008 B, 215 Zeilen). Gelesen sind Z. 1–75 und Z. 166–215; Z. 76–165 nur nach Stichworten.
- **`BACKLOG.md`** 307 Zeilen (vorher 297). **Journal:** EE ist vergeben (TB-136).
- **Nummern:** TB-137 vergeben, TB frei ab 138. Journal ab EF. R74–R77 eingetragen, neue Blöcke ab R78. Fehler ab 21. Fable: Am 04.10. und 05.10. ging nach 04.10.a nichts hinaus; die nächste Anfrage trägt das Datum des Tages, an dem sie hinausgeht.
- **Ablage:** `UEBERGABE.md` mit diesem Block hochgeladen. Abschnittsdateien, Index und Dialog-Index stehen auf dem Stand vom 04.10.2026, 09:39 (vor TB-136).

### Block 4 — Offene Punkte, in Reihenfolge

1. **Rest der Abnahme von TB-136** (Helfer, eng zugeschnitten): Schritt B (BACKLOG-Block, `docs/belege/TB-136/b_*`), Schritt C (Registerkopie mit jetzt 55 Abschnittsdateien unter `docs/projektfuehrung/register_kopie/`, fünfter Teil; `REGISTER_INDEX.md`, Diff laut Sitzung 193/155; `FABLE_DIALOG_INDEX.md`), dazu Z. 76–165 der Ergebnisdatei. Was die Sitzung selbst nennt und noch zu bewerten ist: `registerkopie.py --marken` zählt in Abschnitt 54 drei Zeilen als Marken, die keine sind (Z. 11538, 11545, 11575; laut Sitzung „genau wie im Auftrag erwartet“); `c2_index_eintraege.py` liest die neuen Texte aus dem Auftrag am ⟨S0⟩, statt sie abzutippen („anders als die Vorlage“); T4 der Registerkopie steht bei 234 587 von 240 000 B; der Commit `9b7b060` enthält schon die Skripte für B, C und D — ob der Auftrag das vorsieht, ist nicht gemessen.
2. **Ablage erneuern:** Abschnittsdateien 0–54, Index, Dialog-Index, aus md5-geprüften Kopien per `local_path`, kein Rücklesen; danach die Liste über `project_info` prüfen. Vorbild: Nachtrag 04.10.2026, 09:50.
3. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt: wie im Nachtrag 04.10.2026, 18:15 (Stichproben über die Brücke; Paket 1 und 2 gegen `cloud/c1_stichproben_cloud_tb134_tb135.md` im Archiv).
4. **Nächste Anfrage an Fable** (neuer Fable-Chat): Bauplan in `logs/steuernder_chat/FABLE_04b_bauplan.md`. Sie wartet auf Nr. 2 und auf die Pakete 3, 5 und 11 von TB-137. Inhalt nach 54.6: Frage 1 Meldung zu R75 (a), Frage 2 Marken an 48.1 und 48.14, zur Kenntnis die sechs sinngemässen Verweise, der `BACKLOG.md`-Ausschnitt im Leseprotokoll, der Eintrag durch TB-136. Der Fable-Chat der Antwort 04.10.a hat keine eigene Übergabe abgelegt; die Eröffnung schreibt der steuernde Chat. Unmittelbar vor dem Absenden die vier Erinnerungsdateien neu gegen 27.1 messen: `ways-of-working.md` hat seit 05.10.2026 2 723 B (Eintrag der stehenden Anforderung, Nachtrag 21:27) und kann sich nach jeder Antwort weiter ändern.
5. **TB-133, Regelwerk-Nachtrag** (Mac; die Sitzung legt der steuernde Chat selbst über den Wächter an): wie im Umzug 04.10.2026, 13:17, Block 4 Nr. 4. Dazu aus diesem Chat: die stehende Anforderung vom 05.10.2026 in `ARBEITSWEISE.md` (Abschnitt 0 und 6b, Start) und als Backlog-Nachtrag; die Regeln aus Block 7; aus dem Ergebnis von TB-136 die Bezeichnung „Frühere Vierteilung“ und „T1 … T4“ bei fünf Teilen.
6. **`AKTUELLER_AUFTRAG.md`** beim nächsten Mac-Auftrag umstellen (zuvor TB-136, erledigt mit `67a2202`, 05.10.2026).

### Block 5 — Wartezustände

Keine Sitzung läuft, kein Auslöser liegt, keine Karte ist offen. Auf den Betreiber wartet: das Gesamtergebnis zu TB-137 einfügen, sobald die Cloud-Sitzung fertig ist. Nr. 1 und Nr. 2 aus Block 4 hängen an niemandem.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- 04.10.2026, Karte (gestellt gegen 21:00, eingetragen 21:04): TB-136 „Freigeben wie beschrieben (Empfohlen)“. Wortlaut im Auftrag Z. 12.
- 05.10.2026, 21:17: „weiter“. 21:25: „Legst du mir zukünftig wieder bereits eine claude code Sitzung an“ (stehende Anforderung; Lesart im Nachtrag 21:27). 22:25: „tb136 fertig“.
- Vorgaben ohne Widerspruch: Die Anfrage an Fable wird erst geschrieben, wenn Abschnitt 54 eingetragen ist und TB-137 die Pakete 3, 5 und 11 geliefert hat. Eine alte Sitzung, die nachweislich nicht gearbeitet hat, schliesst der steuernde Chat und startet neu.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. `git --no-optional-locks diff --numstat` über die Brücke, ausserhalb der Vorgabe. ⇒ Zeilenbilanzen über die Brücke mit `diff` zweier Kopien ausserhalb des Repos.
2. T7 erneut: eine Datei nach dem Schreiben im selben Stage-Pfad geändert und abgelegt; am Gerät kam die alte Fassung an. ⇒ Nach jeder Änderung in einen neuen Pfad kopieren; die md5-Prüfung bleibt vor jedem weiteren Schritt.
3. Beim Lesen von 54.5 und 54.6 rund 15 KB statt rund 7 KB in den Chat geholt. ⇒ Ausschnitte aus Codeblöcken an der Zaunzeile schneiden; weicht die gemessene Grösse von der erwarteten ab, zuerst den Bereich prüfen.
4. Am 05.10., 21:20 dem Betreiber das Fenster vom Vortag überlassen, statt eine frische Sitzung anzulegen. ⇒ Stehende Anforderung vom 05.10.2026.
5. Der Satz lag vom 04.10., 21:07 bis zum 05.10., 21:17 unabgeschickt, ohne dass der steuernde Chat es wusste. Die Regel (ein Hinweis, dann warten) hat gehalten; gemessen wurde es erst beim nächsten „weiter“.
6. Ampel: Übernahme, Freigabe und Start kosteten 122 137; mit dem zweiten Start, dem Schliessen und der Kern-Abnahme steht der Verlauf bei 203 404.
7. Was getragen hat: jede Ablage aus frischem Stage-Pfad mit md5 auf beiden Seiten; ein abgewiesener Start-Auslöser als Sonde (der Wächter nennt PID, Laufzeit und Rechenzeit, zwei Abweisungen im Abstand zeigen, ob eine Sitzung arbeitet); der Soll-Bau durch einen Helfer mit eigenen Regeln (132 288 Tokens bei ihm, wenige Tausend hier), die Kernzahlen danach an seiner Rohausgabe nachgerechnet.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert): `2026-10-04_tb136_bau.tar.gz` (Baumaterial, md5 `42488dbb…ca33`), `CLOUD_TB-137_sammelauftrag_leseaufgaben.md` (15 954 B), `FABLE_04b_bauplan.md` (4 817 B, md5 `fdcf2ff19f709189c37e54fc25209e04`).
- Der Ordner des Helfers mit dem Soll-Bau (`abnahme_tb136/` in der Umgebung der Geräteanbindung) verfällt mit diesem Chat; die Zahlen stehen in Block 3.
- Die Punkte „für später“ aus dem Umzug 04.10.2026, 10:56, Block 8, gelten unverändert.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, zusammen mit diesem Umzug. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 05.10.2026, 22:55 — neuer steuernder Chat (Übernahme 22:37): TB-136 ganz abgenommen (B, C, D, E tragen; sechs Befunde, keiner am Register); Ablage erneuert (57 Dateien)

**Übernahme.** Geräteanbindung: Freigabe für `~/trading-bot` angefordert und erteilt (22:37). Gemessen ohne `git status` und ohne `git diff`: HEAD `67a2202` = `origin/main`, `BACKLOG.md` 307 Zeilen, geändert nur `docs/projektfuehrung/UEBERGABE.md` (198 207 B, md5 `e4f0625bc31c5977a0afa166f6fdbbc1`), nichts unverfolgt. Ablage lesbar (`project_info`, 95 Einträge). Kernlektüre aus dem Repo mit Abschnittsfilter gelesen (Umzug 22:31, ARBEITSWEISE 0, UMZUG 3; zusammen rund 34 600 B).

**Abnahme, Rest von TB-136 (Helfer, nur lesend, eigener Ordner ausserhalb des Repos; 22:40–22:51; 36 Schritte, 210 699 Tokens bei ihm).** Vom steuernden Chat mit eigenen Befehlen nachgerechnet: die drei Zeilenbilanzen, die Gleichheit mit HEAD, Register (Zeilen, Bytes, sha256), Bodies der 55 Abschnittsdateien gegen das Register, Kopf von `_54`, Indexzeile 54, Pflegezeile, Auftrag Z. 342, Ergebnis Z. 202. Alles Übrige ist Messung des Helfers.

- **B — trägt.** `BACKLOG.md` 297 → 307 Zeilen, 10 hinzu / 0 entfernt (diff zweier Kopien, `9b7b060` gegen `d55e7ed`), ein Hunk; HEAD gleich `d55e7ed`. Der Block Z. 286–294 ist zeichengleich mit dem Auftrag am ⟨S0⟩ Z. 313–321; die Stelle gibt der Auftrag in Z. 310 und Z. 324 vor; sonst nichts verändert. Der Auftrag am ⟨S0⟩ ist gleich dem am HEAD.
- **C — trägt mit Befund.** 55 Abschnittsdateien; ihre Bodies (ab Zeile 3) aneinander sind bytegleich mit dem Register am HEAD (933 576 B, 11 581 Zeilen, sha256 `8d505a38…568dc`). Von den Dateien `_00` bis `_53` ändern 48 nur die Kopfzeile; sechs tragen dazu nur Einfügungen (16: +3, 17: +3, 48: +18, 51: +3, 52: +3, 53: +16; zusammen 46 = 110 − 64, die Marken aus Schritt A). Kein alter Wortlaut geändert. Fünf Teile lückenlos und ohne Doppelung: 0–22, 23–36, 37–42, 43–53, 54; Grenze 240 000 aus `registerkopie.py` Z. 71 und Auftrag Z. 328. `REGISTER_INDEX.md` 420 → 458 Zeilen; Abschnittstabelle 55 von 55; die neuen Texte zeichengleich mit dem Auftrag (Z. 334–340, 347, 352–368, 375–376). `FABLE_DIALOG_INDEX.md` 70 → 71 Zeilen, 3 hinzu / 2 entfernt: Zeile 04a neu, Zeile 02c auf „registriert“ und offen „nein“. `registerkopie.py --marken`: 95 / 128 / 91 (vorher 84 / 121 / 88); die drei mitgezählten Zeilen 11538, 11545, 11575 erwartet der Auftrag in Z. 370; sie gehen als Zeilenzahl des Suchmusters in Index Z. 8–9 ein, nicht in die 15 Marken.
- **D — trägt mit Befund.** Das Register ändert nur `9b7b060` (sechs Commits gezählt).
- **E — trägt, eine Teilmessung.** Ergebnisdatei Z. 76–165: jede geprüfte Zahl und Fundstelle stimmt; `herkunft.register()` nur gegen die Rohausgabe der Sitzung, nicht selbst ausgeführt. Mit Z. 1–75 und Z. 166–215 (voriger Chat) ist die Ergebnisdatei ganz gelesen.

**Befunde (keiner berührt Register, BACKLOG-Block oder Abschnittsdateien):**

1. **Index-Bilanz:** Das Ergebnis (Z. 202) nennt 193/155; `diff` zweier Kopien ergibt 192/154 (auch mit `diff -d`), Saldo in beiden Fällen +38. In den Belegen liegt keine Rohausgabe mit 193/155. Ursache nicht gemessen; `git diff` ist über die Brücke gesperrt.
2. **Pflegezeile im Index (Z. 455 f.):** „vom Stand `ee43f5f` auf `9b7b060` umgeschrieben“. Der Auftrag (Z. 342) gibt „auf den Commit von Schritt A“ vor; die Sitzung hat den Commit eingesetzt, wie die Zeile von TB-132 es tut. Im Ergebnis nicht als Abweichung genannt. Bewertung: sinngleich; die Unschärfe liegt im Auftrag (steuernder Chat).
3. **Commit-Zuschnitt:** Die elf Skripte für B, C und D liegen schon im Registercommit `9b7b060`. Der Auftrag regelt das nicht (Z. 399 nennt nur die Übernahme aus `docs/belege/TB-132/`). In TB-132 lagen sie im B/C-Commit und im Abgabe-Commit. ⇒ Der nächste Registerauftrag sagt, was Schritt A committet.
4. **Handfeld `entscheidung` der Zeile 04a:** Der Schlusssatz „Die Voraussetzung zu R75 (a) trifft im Wortlaut nicht (54.5)“ stammt aus dem Auftrag (Z. 382), nicht aus Fables Antwort. `dialog_index.py` Z. 49 nennt als Quelle der Handfelder einen Block „**Kurz:**“; die Antwort hat „## Kurz“.
5. **Zeile 04a nennt die Anfragedatei nicht mit Dateinamen** („04a (gleicher Buchstabe)“); die Datei ist vorhanden (9 574 B).
6. **T4:** 234 587 B, Body 234 351 B, es bleiben 5 409 B bis 240 000. Erschlossen, nicht gemessen: Die Marken dieses Eintrags haben die Abschnitte 48 und 51–53 um 40 Zeilen wachsen lassen; setzt der nächste Eintrag wieder Marken in 43–53, läuft T4 über, und das Werkzeug teilt neu (Z. 133). Dann ändern sich die Teilgrenzen im Indexkopf.

**Für TB-133 und den Backlog-Nachtrag (noch nicht im BACKLOG):** Befunde 2 bis 6; dazu aus dem Umzug 22:31, Block 4 Nr. 5 unverändert.

**Nicht gemessen:** `herkunft.register()` selbst; die Markenzahlen 14 / 12 / 21 (TB-129, TB-130, TB-132) in `c2_index_pruefen.txt`; `c1_marken.txt` und `c2_index_zeilen.txt` zeilenweise (nur Zählungen); die Ursache von Befund 1.

**Ablage erneuert (22:51–22:53).** 57 Dateien per `local_path` aus `/home/claude/ablage_2026-10-05_a/`, kein Rücklesen: `REGISTER_KOPIE_ABSCHNITT_00.md` bis `_54.md` (54 ist neu; zusammen 947 530 B), `REGISTER_INDEX.md` (44 079 B, md5 `c0132cd07942774f0ee50dcdbedb3904`), `FABLE_DIALOG_INDEX.md` (24 595 B, md5 `349c1c45a107e5878fcf44533f84d8c3`). Die md5-Liste der 57 Dateien ist am Gerät und im Arbeitsbereich gleich (md5 der Liste `4b7cc36708d5ca1b5842f4f78ba7d8cb`). `project_info` danach: 96 Einträge, die 57 Dateien mit Zeitstempeln 20:51–20:53 UTC; `knowledge_size` 891 677 → 905 461 (Einheit nicht bekannt). Eine Suche in der Ablage lieferte den Kopf von `_54` („von 0–54“, Commit `9b7b060`) und in `_48` die Marke von TB-136. `UEBERGABE.md` geht mit diesem Nachtrag neu in die Ablage.

**Ampel.** 22:53: Verlauf 95 286 (Grundlast 127 705), grün.

**Stand.** HEAD `67a2202` = `origin/main`. Uncommittet: `UEBERGABE.md`. Keine Gerätesitzung, kein Auslöser, kein Auftrag startklar; `logs/sitzungswaechter/letzter_satz.txt` trägt noch den Satz zu TB-136 (erledigt). Nummern unverändert: TB frei ab 138, Journal ab EF, neue Blöcke ab R78, Fehler ab 21.

**Offen, in Reihenfolge.** Block 4 Nr. 1 und Nr. 2 des Umzugs 22:31 sind erledigt. Es bleiben: Nr. 3 TB-137 abnehmen (wartet auf das Gesamtergebnis vom Betreiber); Nr. 4 Anfrage an Fable (wartet nur noch auf die Pakete 3, 5 und 11 von TB-137); Nr. 5 TB-133; Nr. 6 `AKTUELLER_AUFTRAG.md` umstellen.

## Nachtrag 05.10.2026, 23:44 — selber steuernder Chat: Betreiber „Weiter“ (23:39); TB-137 steht noch aus; feste Teile der nächsten Fable-Anfrage und ihrer Eröffnung als Arbeitsentwurf gebaut

**Betreiber, 23:39:** „Weiter“. Gemessen 23:39: Stand unverändert (HEAD `67a2202` = `origin/main`, geändert nur `UEBERGABE.md`, nichts unverfolgt, keine `index.lock`, keine Sitzung, kein Auslöser). Das Gesamtergebnis zu TB-137 ist nicht eingegangen. Gelesen als: weiterarbeiten an dem, was nicht an TB-137 hängt.

**Gebaut:** `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md` (13 181 B, md5 `67ec330b30445f903a1858428ce450c8`; von git ignoriert). Arbeitsentwurf, kein Dokument für Fable, nicht gegengelesen, 29 Platzhalter. Er ergänzt `FABLE_04b_bauplan.md` und enthält:
- die gemessenen Registerzeilen der berührten Unterabschnitte am Stand `9b7b060` (48.13 = R45 und 53.2 = R67 sind jetzt gemessen, nicht mehr erschlossen);
- die Anfrage als Gerüst: Kopf, Form, Frage 1 (Registertext und „Gemessen“ aus 54.5 Z. 11559; Neigung fehlt bis Paket 11), Frage 2 (Gerüst; Kandidaten fehlen bis Paket 5 und 3), K1 bis K3 ausformuliert;
- die Eröffnung für den neuen Fable-Chat: Abschnitt 1, vier Fehlerpunkte aus Abschnitt 5 und Abschnitt 6 per Skript unverändert aus der Eröffnung vom 04.10.2026 (md5 `c96f56c9…`) übernommen; Kopf, Abschnitte 2, 3 und 4 neu (4 verweist auf 54.6, F6); die Erinnerungsdateien stehen als Platzhalter und werden unmittelbar vor dem Absenden gemessen;
- die Reihenfolge „Vor dem Absenden“ (sieben Schritte).

**Nicht gelesen** sind die Blöcke R74–R77 selbst und die berührten alten Unterabschnitte; die vier Landkartenzeilen in Abschnitt 3 der Eröffnung stammen aus Fables Tabelle „Kurz“ (Antwort 04.10.a, Z. 122–134) und den Registerüberschriften. Der Gegenleser misst sie am Wortlaut.

**Vorbereitet für die Abnahme von TB-137:** Der Messbericht `cloud/c1_stichproben_cloud_tb134_tb135.md` liegt im Archiv `logs/steuernder_chat/2026-10-04_tb136_bau.tar.gz` (22 690 B entpackt, in der Umgebung der Geräteanbindung; verfällt mit diesem Chat). Die Form des Gesamtergebnisses steht im Cloud-Auftrag ab „## Das Gesamtergebnis“.

**Fehler dieses Chats (ohne Nummer):** (1) 22:54 `git check-ignore` über die Brücke, ausserhalb der erlaubten Liste; danach gemessen: keine `index.lock`, Arbeitsbaum unverändert. (2) Im ersten Bau des Entwurfs standen geschätzte Uhrzeiten (23:50 statt gemessen 23:43); vor dem Ablegen berichtigt und aus einem neuen Pfad abgelegt. ⇒ Uhrzeit im selben Schritt mit `date` messen, in dem sie in einen Text geht.

**Ampel.** 23:39: Verlauf 136 134 (Grundlast 127 705), grün.

**Stand und Reihenfolge unverändert:** TB-137 abnehmen (wartet auf den Betreiber), dann die Anfrage an Fable fertigschreiben, dann TB-133, dann `AKTUELLER_AUFTRAG.md`.

## Umzug 05.10.2026, 23:46 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 23:39: „Weiter“. Das Gesamtergebnis zu TB-137 ist nicht eingegangen. Ampel 23:44: Verlauf 184 639 (Grundlast 127 705), grün, 15 361 unter Gelb. Das Gesamtergebnis darf bis rund 120 000 Zeichen haben; hier eingefügt, stünde dieser Chat vor Beginn der Abnahme auf Gelb. Der Stand ist sauber (keine Sitzung, kein Auslöser, alles abgelegt), deshalb der Umzug jetzt, vor dem nächsten grossen Block. Die Nachträge vom 05.10.2026, 22:55 und 23:44, tragen die Einzelheiten; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **TB-136 ist ganz abgenommen:** Kern am 05.10., 22:27–22:30 (voriger Chat), Rest (Schritte B, C, D und Z. 76–165 der Ergebnisdatei) 22:40–22:51. Alles trägt; sechs Befunde, keiner am Register, am BACKLOG-Block oder an den Abschnittsdateien (Nachtrag 22:55).
- **Die Ablage ist erneuert** (22:51–22:53): Abschnittsdateien 00–54, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`; `UEBERGABE.md` mit diesem Block.
- **TB-137 steht aus.** Für die nächste Anfrage an Fable liegen die festen Teile und die Eröffnung als Arbeitsentwurf vor; die zwei Fragen warten auf die Pakete 3, 5 und 11.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `67a2202` (`67a22025a0c867d03456c7857ea1a4ac124fd5b2`). Gemessen 23:44 ohne `git status` und ohne `git diff`: geändert nur `docs/projektfuehrung/UEBERGABE.md`, nichts unverfolgt, keine `index.lock`. Keine Sitzung, kein Auslöser (letzter Eintrag in `logs/sitzungswaechter/waechter.log`: 20:26:30Z, „fertig (schliessen)“). `docs/auftraege/AKTUELLER_AUFTRAG.md` zeigt auf TB-136 (erledigt mit `67a2202`, 05.10.2026); `logs/sitzungswaechter/letzter_satz.txt` trägt den Satz zu TB-136. Kein Auftrag startklar.

### Block 3 — Tragende Zahlen

- **Register:** `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `9b7b060`, 11 581 Zeilen, 933 576 B, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc`. Abschnitt 54 in Z. 11518–11581 (54.1 Z. 11522, 54.2 Z. 11529, 54.3 Z. 11536, 54.4 Z. 11543, 54.5 Z. 11550, 54.6 Z. 11566). Höchster eingetragener Block R77.
- **Abnahme TB-136, Rest:** `BACKLOG.md` 297 → 307 Zeilen (10/0). 55 Abschnittsdateien, Bodies aneinander bytegleich mit dem Register. Teile 0–22, 23–36, 37–42, 43–53, 54; T4 234 587 B, 5 409 B unter der Grenze 240 000. `REGISTER_INDEX.md` 420 → 458 Zeilen (gemessen 192/154; die Sitzung nennt 193/155). `FABLE_DIALOG_INDEX.md` 70 → 71 Zeilen (3/2). `registerkopie.py --marken`: 95 / 128 / 91.
- **Ablage:** 96 Einträge. `REGISTER_INDEX.md` 44 079 B, md5 `c0132cd07942774f0ee50dcdbedb3904`; `FABLE_DIALOG_INDEX.md` 24 595 B, md5 `349c1c45a107e5878fcf44533f84d8c3`; md5 der Liste der 57 Dateien `4b7cc36708d5ca1b5842f4f78ba7d8cb`.
- **Registerzeilen der Unterabschnitte, die die nächste Fable-Anfrage berührt** (Stand `9b7b060`): 29.3 Z. 5406 · 48.1 R33 Z. 10795 · 48.13 R45 Z. 10906 · 48.14 R46 Z. 10913 · 51.1 R56 Z. 11223 · 51.5 R60 Z. 11251 · 52.2 R64 Z. 11340 · 52.3 R65 Z. 11365 · 53.1 R66 Z. 11412 · 53.2 R67 Z. 11422.
- **Nummern:** TB-137 vergeben, TB frei ab 138. Journal ab EF. Neue Blöcke ab R78. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Tages, an dem sie hinausgeht.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt. Fundstellenlisten sind kein Nachweis: Stichproben über die Brücke (Helfer, eng zugeschnitten). Paket 1 und 2 gegen `cloud/c1_stichproben_cloud_tb134_tb135.md` im Archiv `logs/steuernder_chat/2026-10-04_tb136_bau.tar.gz` (nach ausserhalb des Repos entpacken; 22 690 B); Paket 3 gegen 54.6 Nr. 6; Paket 5 liefert Kandidaten für Marken, die Entscheidung bleibt beim steuernden Chat und bei Fable; Paket 11 für Frage 1; Paket 15 bringt einen Entwurf für TB-133. Die Cloud-Sitzung sah nur den Stand `d781f1b` (kein R74–R77). Die Form des Gesamtergebnisses steht in `logs/steuernder_chat/CLOUD_TB-137_sammelauftrag_leseaufgaben.md` ab „## Das Gesamtergebnis“.
2. **Anfrage an Fable fertigschreiben** (neuer Fable-Chat): Arbeitsentwurf `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md`, dort „Vor dem Absenden“ (sieben Schritte). K1 bis K3 sind ausformuliert; Frage 1 und Frage 2 brauchen die Pakete 11, 5 und 3. Die Blöcke R74–R77 und die berührten alten Unterabschnitte sind im Wortlaut noch nicht gelesen. Unmittelbar vor dem Absenden die vier Erinnerungsdateien gegen 27.1 messen.
3. **TB-133, Regelwerk-Nachtrag** (Mac; die Sitzung legt der steuernde Chat selbst über den Wächter an): wie im Umzug 04.10.2026, 13:17, Block 4 Nr. 4, und im Umzug 05.10.2026, 22:31, Block 4 Nr. 5. Dazu: die Befunde 2 bis 6 aus dem Nachtrag 22:55, die Regeln aus Block 7 hier, der Entwurf aus Paket 15.
4. **`AKTUELLER_AUFTRAG.md`** beim nächsten Mac-Auftrag umstellen.

### Block 5 — Wartezustände

Keine Sitzung läuft, kein Auslöser liegt, keine Karte ist offen. Auf den Betreiber wartet: das Gesamtergebnis zu TB-137 in den **neuen** steuernden Chat einfügen. Sonst hängt nichts an ihm.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- 22:37: Eröffnung; die Ordnerfreigabe für `~/trading-bot` über die Geräteanbindung ist erteilt.
- 23:39: „Weiter“.
- Vorgabe ohne Widerspruch (ausgegeben 22:56): Die Befunde aus der Abnahme von TB-136 gehen in TB-133 und in den Backlog-Nachtrag.
- Keine Freigabe für Register, Sperrliste, Signalpfad oder Parameterdateien in diesem Chat.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. `git check-ignore` über die Brücke, ausserhalb der erlaubten Liste (22:54). ⇒ Ob ein Pfad ignoriert ist, zeigt `git --no-optional-locks ls-files -o --exclude-standard` nach dem Ablegen.
2. Geschätzte Uhrzeiten in einem Text (23:50 statt gemessen 23:43); vor dem Ablegen berichtigt. ⇒ Die Uhrzeit im selben Schritt mit `date` messen, in dem sie in einen Text geht.
3. Die Ablage selbst erneuert statt über einen Helfer: 57 Antworten von `project_write`, zwei lange Antworten von `device_stage_files` und eine Suche mit zwei ganzen Treffern (rund 6 KB) standen im Chat. ⇒ Die Erneuerung der Ablage macht ein Helfer (Vorbild 04.10.2026, 09:36); als Kontrolle genügt `project_info`.
4. Ampel: Übernahme, Abnahme-Rest und Ablage kosteten 123 302 (22:56); „Weiter“, Entwurf und zwei Nachträge brachten den Verlauf auf 184 639 (23:44).
5. Was getragen hat: ein enger Helfer mit eigenem Ordner für Rohausgaben, die Kernzahlen danach mit eigenen Befehlen nachgerechnet; ein md5 über die md5-Liste statt 57 Zeilen im Chat; unveränderte Textteile per Skript aus der Quelle übernommen, mit `assert` auf die Ankerzeilen.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert): `FABLE_naechste_anfrage_feste_teile.md` (13 181 B, md5 `67ec330b30445f903a1858428ce450c8`), `FABLE_04b_bauplan.md` (4 817 B), `CLOUD_TB-137_sammelauftrag_leseaufgaben.md` (15 954 B), `2026-10-04_tb136_bau.tar.gz`, dazu die Kopien der Nachträge und dieses Blocks (`NACHTRAG_2026-10-05_2255.md`, `NACHTRAG_2026-10-05_2344.md`, `UMZUG_2026-10-05.md`; überflüssig, sobald die Übergabe committet ist — nicht ohne Frage löschen).
- Die Ordner `abnahme_tb136_rest/` (Rohausgaben des Helfers) und `tb137_abnahme/` in der Umgebung der Geräteanbindung verfallen mit diesem Chat; die Zahlen stehen im Nachtrag 22:55.
- Die Punkte „für später“ aus dem Umzug 04.10.2026, 10:56, Block 8, gelten unverändert.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, zusammen mit diesem Umzug. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 06.10.2026, 00:13 — selber steuernder Chat: Betreiber lehnt den Umzug ab („zukünftig“: Umzug nur auf Ansage oder mit Genehmigung); der Umzug 23:46 ist nicht vollzogen; TB-133 wird gebaut

**Betreiber, 05.10.2026, 23:58:** „Nein du ziehst zukünftig um wenn ich das sage oder genehmige. Mach noch eine weitere Aufgabe fertig“.

**Folge.** Der Umzug von 23:46 ist nicht vollzogen; dieser Chat arbeitet weiter. Der Block „Umzug 05.10.2026, 23:46“ bleibt als Standbeschreibung stehen; sein Eröffnungstext ist nicht abgeschickt und gilt nicht. Der Satz „Zieh bei Gelb am nächsten sauberen Stand um, auch wenn ich ‚mach weiter‘ sage“ aus den Eröffnungstexten der steuernden Chats gilt nicht mehr. In `UMZUG.md`, Abschnitt 6, steht er nicht (Helfer, 06.10.2026: der Codeblock Z. 261–275 trägt keinen Satz dazu, wann der neue Chat umzieht).

**Lesart des steuernden Chats, vorläufig (stehende Anforderung nach ARBEITSWEISE 15).** Umgezogen wird nur, wenn der Betreiber es sagt oder genehmigt, bei jeder Ampelfarbe. Der steuernde Chat kündigt an (Zahl, Uhrzeit), fragt per Karte und arbeitet weiter, bis der Betreiber entscheidet; Umzugsblock und Eröffnungstext schreibt er erst nach dem Ja. Die Ampelzeile bleibt die letzte Zeile jeder Antwort.

**Träger nach ARBEITSWEISE 15.** Erinnerung: eingetragen am 06.10.2026 gegen 00:00 in `preferences.md` der Projekt-Erinnerung, Abschnitt „Umzug, Ampel, Tokensparen“, mit dem Wortlaut des Betreibers; die Datei hat dadurch 9 440 B statt 9 241 B und einen neuen Stand — vor der nächsten Eröffnung für Fable neu gegen 27.1 messen. `ARBEITSWEISE.md` (Abschnitt 0), `UMZUG.md` (Abschnitt 3) und der Backlog-Nachtrag: mit TB-133 (E2, E8, E9). Projektablage: diese Datei.

**„Eine weitere Aufgabe“, gelesen als TB-133 (Vorgabe).** Die Abnahme von TB-137 und die Anfrage an Fable hängen am Gesamtergebnis der Cloud-Sitzung; TB-133 ist der einzige Punkt der Liste, der an niemandem hängt, und er trägt die neue Regel ins Regelwerk. Der Entwurf aus TB-137, Paket 15, kommt in einen späteren Nachtrag.

**Bestandsaufnahme für TB-133 (Helfer, nur lesend, 00:00–00:07; 24 Schritte, 180 477 Tokens bei ihm):** 40 Punkte aus den Umzügen und Nachträgen vom 04.10. bis 05.10.2026 im Wortlaut gesammelt, Zielstellen in `ARBEITSWEISE.md` und `UMZUG.md` gemessen, Bauart von TB-131 gemessen. Die Dateien liegen in der Umgebung der Geräteanbindung (`tb133_bestand/`) und verfallen mit diesem Chat.

**Ampel.** 23:59: Verlauf 211 230 (Grundlast 127 705), gelb. Kein Umzug ohne Ansage.

## Nachtrag 06.10.2026, 00:31 — selber steuernder Chat: TB-133 geschrieben, zweimal gegengelesen und gelegt; Zeiger gesetzt; der Auslöser folgt nach diesem Nachtrag

**Auftrag.** `docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md` (20 294 B, 186 Zeilen, md5 `ca9d5234071bcb70be6847685fdfc9aa`), unverfolgt bis Schritt 0. Bauart wie TB-131, nur Einfügungen: E1 bis E7 sechzehn Tabellenzeilen in `ARBEITSWEISE.md` Abschnitt 0, E8 ein Absatz in `UMZUG.md` Abschnitt 3, E9 ein Block im `BACKLOG.md`. Soll in C2: 16/0, 2/0, 10/0. Freigabe: Handwerk ohne Sperrlistennähe, pauschal frei (Betreiberentscheid 26.09.2026).

**Vorzählung** (Skript `logs/steuernder_chat/vorzaehlung_tb133.py`, nur lesend; 00:13, 00:24 und nach den letzten Berichtigungen 00:30): neun Anker je genau 1, erste Textzeilen je 0, rc 0.

**Gegenleser, zwei Runden (frische Helfer, nur lesend).** Runde 1 (00:13–00:21): 18 Befunde. Die wichtigsten: eine Zahl ohne Quelle in E8; „fünf“ statt vier Umzüge im Titel; eine Regel zu Cloud-Sitzungen, die der Betreiberentscheid vom 04.10.2026, 09:55, im Wortlaut nicht trägt (aus E7 entfernt, als offener Punkt in E9); Spannungen zu bestehenden Zeilen (in E4, E6 und E8 jetzt ausdrücklich genannt); zwei feste Stellen in den Vorlagenskripten (`BLOECKE`, der Teil zu `ampel.py`). Runde 2 (00:25–00:30): ein Befund (E3 datierte `diff --numstat` auf den 05.10.2026; die Quelle nennt den 04.10.2026, Nachtrag 21:07) und zwei Nebenbefunde. Alles ist eingearbeitet. Eine dritte Runde gab es nicht: Die letzten vier Ersetzungen sind die Befunde der Runde 2, per Skript mit `assert` eingesetzt, danach neu vorgezählt.

**Fehler dieses Chats (ohne Nummer).** Beim Einarbeiten der Runde 1 die Zeilen von E7 falsch gezählt (fünf statt sechs; C2 und der Schlussabschnitt standen auf 15 statt 16). Gefunden von der eigenen Vorzählung, vor der zweiten Runde berichtigt. ⇒ Zählungen im Auftrag kommen aus der Zählung des Skripts, nicht aus dem Kopf. Die Ampel stand dabei auf Rot.

**Zeiger.** `docs/auftraege/AKTUELLER_AUFTRAG.md` zeigt auf TB-133 (gesetzt 00:30; Z. 39 und Z. 52, Bilanz 2/2; md5 `d18bbb80813661d507264aab8657b449`). Der Arbeitsbaum steht, wie 0a ihn erwartet: geändert `AKTUELLER_AUFTRAG.md` und `UEBERGABE.md`, unverfolgt der Auftrag.

**Nach diesem Nachtrag:** Auslöser `docs/auftraege/_ausloeser/starte_TB-133`. Danach fasst der steuernde Chat im Arbeitsbaum nichts an, bis die Sitzung abgegeben hat. Was der Wächter meldet, steht in `logs/sitzungswaechter/waechter.log` und in der Antwort im Chat.

**Abnahme von TB-133, nach der Abgabe:** enger Helfer, nur lesend: C2 mit `diff` zweier Kopien (`git show ⟨S0⟩:…` gegen HEAD), C3 am Wortlaut, `d3_porcelain.txt` leer. Danach `ARBEITSWEISE.md` und `UMZUG.md` in der Ablage erneuern (Helfer); `BACKLOG.md` erst nach der 27.4-Prüfung.

**Ampel.** 00:23: Verlauf 307 032 (Grundlast 127 705), rot. Kein Umzug ohne Ansage; der Vorschlag geht als Karte an den Betreiber.

**Nummern.** TB-133 ist vergeben und startklar; TB frei ab 138. Journal: EF erwartet (TB-133). Sonst unverändert.

## Umzug 06.10.2026, 07:08 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 06.10.2026, 07:07: „Jetzt umziehen“. Ampel 07:07: Verlauf 377 230 (Grundlast 127 705), rot. Dieser Block ersetzt den Block „Umzug 05.10.2026, 23:46“, der nicht vollzogen wurde. Die Nachträge vom 05.10.2026 (22:55, 23:44) und vom 06.10.2026 (00:13, 00:31) tragen die Einzelheiten; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **TB-136 ist ganz abgenommen** (05.10.2026); die Ablage ist erneuert (Abschnittsdateien 00–54, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`).
- **TB-133 (Regelwerk-Nachtrag) ist startklar, aber nicht gestartet:** Auftrag geschrieben, zweimal gegengelesen, gelegt; Zeiger gesetzt; Sitzung über den Wächter angelegt (06.10.2026, 00:32). **Der Satz ist nicht abgeschickt** (gemessen 00:43, 01:24 und 07:07: kein Commit seit `67a2202`).
- **TB-137 steht aus.** Für die nächste Anfrage an Fable liegen die festen Teile und die Eröffnung als Arbeitsentwurf vor; die zwei Fragen warten auf die Pakete 3, 5 und 11.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `67a2202` (`67a22025a0c867d03456c7857ea1a4ac124fd5b2`). Gemessen 07:07 ohne `git status` und ohne `git diff`: geändert `docs/auftraege/AKTUELLER_AUFTRAG.md` (md5 `d18bbb80813661d507264aab8657b449`) und `docs/projektfuehrung/UEBERGABE.md`; unverfolgt `docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md` (20 294 B, md5 `ca9d5234071bcb70be6847685fdfc9aa`). Genau diese drei Einträge erwartet Schritt 0a von TB-133. Keine `index.lock`.

⚠️ **Bis die Sitzung Schritt 0 committet hat, kommt keine weitere Datei in den Arbeitsbaum** (unter `logs/` ist erlaubt, der Ordner ist ignoriert). `UEBERGABE.md` darf vor Schritt 0 noch ergänzt werden; nach Schritt 0 wird im Arbeitsbaum nichts angefasst, bis die Sitzung abgegeben hat.

Die Sitzung vom 06.10.2026, 00:32, wartet im Terminal-Fenster (`logs/sitzungswaechter/waechter.log`, 22:32:29Z: „Satz ins Fenster gelegt … NICHT ABGESCHICKT“). `logs/sitzungswaechter/letzter_satz.txt` trägt den Satz zu TB-133.

### Block 3 — Tragende Zahlen

- **Register:** `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `9b7b060`, 11 581 Zeilen, 933 576 B, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc`. Abschnitt 54 in Z. 11518–11581. Höchster eingetragener Block R77.
- **TB-133:** neun Einfügungen, nur Einfügungen, Bauart wie TB-131. E1 bis E7: 16 Tabellenzeilen in `ARBEITSWEISE.md` Abschnitt 0; E8: ein Absatz in `UMZUG.md` Abschnitt 3; E9: ein Block im `BACKLOG.md`. Soll in C2: 16/0, 2/0, 10/0. Ausgang: `ARBEITSWEISE.md` 2 397 Zeilen (md5 `42e208032b02d9ab586fb3c8841e3f75`), `UMZUG.md` 378 (md5 `edfe2a34ffa016eaf3ab8ea5bdfdd5a8`), `BACKLOG.md` 307 (md5 `c005a57d88d84dd6c6bbfa626fbc8a95`). Vorzählung rc 0 (00:30). Journal: EF erwartet.
- **Ablage:** 96 Einträge; `UEBERGABE.md` mit diesem Block hochgeladen.
- **Projekt-Erinnerung:** `preferences.md` hat seit dem 06.10.2026 9 440 B (Umzugsregel), `ways-of-working.md` 2 723 B. Vor der Eröffnung für Fable alle vier Dateien neu gegen 27.1 messen.
- **Registerzeilen für die Fable-Anfrage** stehen im Arbeitsentwurf (Block 8) und im Umzug 05.10.2026, 23:46, Block 3.
- **Nummern:** TB-133 startklar, TB-137 vergeben (Cloud), TB frei ab 138. Journal ab EF (für TB-133 erwartet). Neue Blöcke ab R78. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Tages, an dem sie hinausgeht.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-133:** Der Betreiber schickt den Satz ab. Ohne Commit von Schritt 0 ist der Satz nicht angekommen: ein Hinweis, dann warten. Nach der Abgabe: Abnahme durch einen engen Helfer, nur lesend (C2 mit `diff` zweier Kopien aus `git show ⟨S0⟩:…` gegen HEAD; C3 am Wortlaut; `d3_porcelain.txt` leer; Zeiger). Danach die Sitzung über den Schliess-Auslöser schliessen (ab 600 s nach dem letzten Commit), `ARBEITSWEISE.md` und `UMZUG.md` in der Ablage erneuern (Helfer), `BACKLOG.md` erst nach der 27.4-Prüfung. Will der Betreiber neu starten und der Wächter weist ab, weil die Sitzung von 00:32 schläft: nach dem Nachtrag 05.10.2026, 21:27, messen, schliessen, neu anlegen.
2. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt (bis rund 120 000 Zeichen; danach sofort die Ampel messen). Stichproben über die Brücke durch einen engen Helfer. Paket 1 und 2 gegen `cloud/c1_stichproben_cloud_tb134_tb135.md` im Archiv `logs/steuernder_chat/2026-10-04_tb136_bau.tar.gz` (nach ausserhalb des Repos entpacken); Paket 3 gegen 54.6 Nr. 6; Paket 5 liefert Kandidaten für Marken; Paket 11 für Frage 1; Paket 15 bringt einen Entwurf zum Regelwerk. Die Cloud-Sitzung sah nur den Stand `d781f1b`.
3. **Anfrage an Fable fertigschreiben** (neuer Fable-Chat): `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md`, dort „Vor dem Absenden“ (sieben Schritte); Bauplan daneben.
4. **Nächster Regelwerk-Nachtrag** (neue Nummer ab 138), nach TB-133 und TB-137: der Fliesstext in `ARBEITSWEISE.md` 6b und 10, die git-Liste im Eröffnungstext (`UMZUG.md` Abschnitt 6 nennt noch `diff --name-only`), die Regel zu Cloud-Sitzungen, der Entwurf aus Paket 15, die Regeln aus Block 7 hier.
5. **`AKTUELLER_AUFTRAG.md`** beim nächsten Mac-Auftrag umstellen (jetzt TB-133, gesetzt 06.10.2026, 00:30).

### Block 5 — Wartezustände

Die Sitzung TB-133 wartet auf das Abschicken durch den Betreiber. TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Keine Karte ist offen, keine Nachschau ist geplant.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- 05.10.2026, 22:37: Eröffnung; Ordnerfreigabe für `~/trading-bot` erteilt. 23:39: „Weiter“.
- 05.10.2026, 23:58: „Nein du ziehst zukünftig um wenn ich das sage oder genehmige. Mach noch eine weitere Aufgabe fertig“ (stehende Anforderung; Lesart und Träger im Nachtrag 06.10.2026, 00:13).
- 06.10.2026, ca. 00:40, Karte zum Umzug: „Hier bleiben“. 07:07: „Jetzt umziehen“.
- Vorgaben ohne Widerspruch: Die Befunde aus der Abnahme von TB-136 gehen in TB-133; „eine weitere Aufgabe“ ist als TB-133 gelesen.
- Keine Freigabe für Register, Sperrliste, Signalpfad oder Parameterdateien. TB-133 läuft unter der pauschalen Freigabe für Handwerk ohne Sperrlistennähe (26.09.2026).

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. Am 05.10.2026, 23:46, von sich aus umgezogen (Umzugsblock und Eröffnungstext), ohne Ansage des Betreibers. ⇒ Stehende Anforderung vom 05.10.2026, 23:58.
2. `git check-ignore` über die Brücke; geschätzte Uhrzeiten in einem Text; die Ablage selbst erneuert statt über einen Helfer (Regeln im Umzug 05.10.2026, 23:46, Block 7; mit TB-133 im Regelwerk).
3. Beim Bau von TB-133 bei roter Ampel die Zeilen einer Einfügung falsch gezählt (fünf statt sechs); im Entwurf eine Zahl ohne Quelle und ein falsches Datum. Die eigene Vorzählung und zwei Gegenleser haben es gefunden. ⇒ Zählungen im Auftrag kommen aus dem Skript; zwei Runden Gegenlesen bleiben.
4. Ampel: 123 302 (05.10., 22:56) · 198 389 (23:46) · 307 032 (06.10., 00:23, nach Bestandsaufnahme, Auftragstext und erstem Gegenleser) · 359 147 (00:43) · 377 230 (07:07). Drei Helferberichte von 6 bis 9 KB und der Auftragstext von rund 20 KB standen im Chat. ⇒ Helferberichte auf rund 3 KB begrenzen, das Übrige in Dateien; lange Auftragstexte aus Bausteindateien per Skript bauen.
5. Was getragen hat: Vorzählung als Skript vor und nach jeder Berichtigung; Ersetzungen per Skript mit `assert` auf die Trefferzahl; ein md5 über die md5-Liste; die Uhrzeit im selben Schritt mit `date` eingesetzt.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert): `FABLE_naechste_anfrage_feste_teile.md` (13 181 B, md5 `67ec330b30445f903a1858428ce450c8`), `FABLE_04b_bauplan.md`, `CLOUD_TB-137_sammelauftrag_leseaufgaben.md`, `2026-10-04_tb136_bau.tar.gz`, `vorzaehlung_tb133.py`; dazu Arbeitskopien (`TB-133_entwurf.md`, `TB-133_entwurf_v2.md`, vier `NACHTRAG_…`-Dateien, zwei `UMZUG_…`-Dateien), überflüssig, sobald die Übergabe committet ist — nicht ohne Frage löschen.
- Die Ordner der Helfer in der Umgebung der Geräteanbindung (`abnahme_tb136_rest/`, `tb133_bestand/`, `tb133_gegenleser/`, `tb133_gegenleser2/`, `tb137_abnahme/`) verfallen mit diesem Chat.
- Die Punkte „für später“ aus dem Umzug 04.10.2026, 10:56, Block 8, gelten unverändert.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, zusammen mit diesem Umzug. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 06.10.2026, 10:51 — neuer steuernder Chat (Übernahme 07:40): TB-133 abgenommen, Sitzung geschlossen; Abnahme TB-137 vorbereitet

- **Übernahme 07:40:** Ordnerfreigabe für `~/trading-bot` erteilt (07:42); Ablage lesbar (96 Einträge). Der Stand war wie im Umzug 07:08 gemessen.
- **TB-133:** Der Betreiber hat den Satz abgeschickt. Commits `1ea5213` (Schritt 0), `5216e1d` (A), `f5c69b4` (C), `a84ca0d` (Abgabe), `0c70853` (D3), alle am 06.10.2026 zwischen 07:45:00 und 07:47:38. Meldung des Betreibers 10:42. HEAD = `origin/main` = `0c70853` (`0c708531d4342d4fe5c5dd6a04eaea35dd680fe8`).
- **Abnahme (Helfer, nur lesend, 10:44–10:47; Helferauftrag und Bericht im Arbeitsbereich des Chats, sie verfallen mit ihm):** zehn Prüfungen, keine Abweichung gegen ein Soll. C2 mit `diff` zweier Kopien ⟨S0⟩ gegen HEAD: 16/0 · 2/0 · 10/0. C3 am Wortlaut mit eigenem Skript: neun Texte je genau einmal an HEAD, keinmal an ⟨S0⟩, jeder Anker an ⟨S0⟩ genau einmal. Zwei hinzugefügte Leerzeilen (`UMZUG.md` Z. 109, `BACKLOG.md` Z. 305) folgen aus dem Auftrag Z. 36. Journal 34/0, Block EF einmal, nächste Kennung EG. `d3_porcelain.txt` 0 B; `ls-files -m` und `ls-files -o --exclude-standard` leer. Zeiger und Übergabe tragen an ⟨S0⟩ und HEAD die gelegten md5. Stand nach TB-133: `ARBEITSWEISE.md` 2 413 Zeilen, `UMZUG.md` 380, `BACKLOG.md` 317.
- **Befunde ohne Soll, für den nächsten Regelwerk-Nachtrag:** Das Ergebnis nennt „Stand 07:46“, die Abgabe trägt 07:47:32. Der Auftrag nennt die Zwischenüberschrift zu E6 ohne den Zusatz „(Cloud, Mac, Fable)“. **Nicht gemessen:** die Pushes (kein `fetch`; gemessen ist nur HEAD = `origin/main` lokal), der Hergang der zwei gemeldeten Abweichungen (Ableitung von `c3_vergleich.py`, Trennstrich im Journal), die inhaltliche Richtigkeit der neun Texte.
- **Sitzung geschlossen:** Schliess-Auslöser gelegt 08:49:31Z; `waechter.log` 08:49:38Z: „1 Sitzung(en) mit TERM beendet, 0 noch da“ (Alter des Commits 10 915 s).
- **27.4-Prüfung `BACKLOG.md`:** die zehn neuen Zeilen (Z. 296–305) per Muster und im Wortlaut gelesen: keine Grösse nach 27.1. Teilmessung — nur der neue Block.
- **Ablage:** `ARBEITSWEISE.md`, `UMZUG.md`, `BACKLOG.md` und diese Datei erneuert ein Helfer nach diesem Nachtrag; Kontrolle über `project_info`.
- **TB-137, vorbereitet:** Messbericht c1 ausserhalb des Repos entpackt (22 690 B, md5 `edc4c1eb2a1ba1b2b0389cc0f0727786`); Helferauftrag zugeschnitten (acht Stichproben, nicht gegengelesen). Gemessen: Das Register hat am Stand der Cloud-Sitzung (`d781f1b`) 11 471 Zeilen, an HEAD 11 581. Die Zeilennummern des Gesamtergebnisses gelten am Stand `d781f1b`; der Helfer prüft gegen eine Kopie von dort.
- **Nummern:** TB frei ab 138; Journal ab EG; neue Blöcke ab R78; Fehler ab 21. `AKTUELLER_AUFTRAG.md` zeigt noch auf TB-133 (beim nächsten Mac-Auftrag umstellen); kein Auftrag ist startklar.
- **Wartezustände:** TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Keine Karte ist offen, keine Nachschau ist geplant.
- **Ampel:** 07:43 Verlauf 41 266 (Grundlast 135 477) · 10:51 Verlauf 77 316, grün.

## Nachtrag 06.10.2026, 11:12 — selber steuernder Chat: Betreiber „weiter“ (10:58); feste Teile der Fable-Anfrage gegengelesen (Runde 1); Helferauftrag TB-137 geprüft und gelegt; Stellen für TB-138

- **Ablage (zum Nachtrag 10:51):** Ein Helfer hat `ARBEITSWEISE.md`, `UMZUG.md`, `BACKLOG.md` und `UEBERGABE.md` (Stand 10:51, md5 `63344f8e…`) ersetzt; md5 am Stage-Pfad und im neuen Ordner gleich dem Soll, je `replaced:true`, 96 Einträge. Nicht zurückgelesen. **Dieser Nachtrag liegt noch nicht in der Ablage** — Erneuerung zusammen mit der Abnahme von TB-137 (Helfer).
- **Fable-Anfrage, feste Teile:** `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md` ist gegengelesen (Runde 1, frischer Helfer, zehn Prüfungen): keine Zahl ohne Quelle, kein Treffer nach 27.1; elf Berichtigungen per Skript eingearbeitet, Liste am Dateiende. Neu 15 621 B, md5 `66e1b6626fa1acb10409063fcab199f5` (vorher 13 181 B, `67ec330b…`). Die zwei Fragen und alle Platzhalter (13 in der Anfrage, 15 in der Eröffnung) sind offen; die zweite Runde gehört zu Schritt 6 „Vor dem Absenden“.
- **Helferauftrag TB-137:** gelegt unter `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md` (4 059 B, md5 `2af399ded19a61ee21bbb46de98b7ac3`). Seine Zeilenangaben per Skript an der Kopie vom Stand `d781f1b` geprüft: alle treffen (fünf Klammern in R48, fünf Sätze „Zellen-Erzeuger“, R46/R60/R64/R66/R67/R65, `mtm_kern.py` Z. 210, 244, 246, 251). Gezählt an `d781f1b`: 17 Klammern `[Voraussetzung` ab `### 48.1 ` (Z. 10789), 6 davor. `⟨PFAD_ERGEBNIS⟩` setzt der steuernde Chat beim Start ein. Der Messbericht c1 liegt nur in der Umgebung der Geräteanbindung (verfällt mit dem Chat; Quelle bleibt das Archiv).
- **Stellen für den nächsten Regelwerk-Nachtrag (TB-138), per Skript gesucht:** `diff --name-only` steht noch in `ARBEITSWEISE.md` Z. 134 (Abschnitt 0, alte Zeile; Z. 135 aus TB-133 geht ihr vor) und in `UMZUG.md` Z. 266 (Abschnitt 6, Eröffnungstext). Dazu die zwei Befunde aus der Abnahme TB-133 (Nachtrag 10:51).
- **Wartezustände:** unverändert — TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Kein Auftrag ist startklar, keine Karte offen, keine Nachschau geplant.
- **Ampel:** 10:52 Verlauf 86 633 · 11:11 Verlauf 139 186 (Grundlast 135 477), grün. Mit dem Gesamtergebnis TB-137 (bis rund 120 000 Zeichen, bei 1,6 B je Token rund 75 000) ist Gelb zu erwarten — Schätzung, kein Messwert; dann Ankündigung mit Zahl und Karte.

## Nachtrag 06.10.2026, 13:33 — selber steuernder Chat: Betreiber „Fahre im Backlog fort“ (13:22); Vorgabe TB-138 = Verfahrensmessung am Snapshot (54.6 Nr. 1 und Nr. 8, 53.10 Nr. 3); Bestandsaufnahme fertig, Auftrag noch nicht geschrieben

- **Wahl des nächsten Punkts (Handwerk, Vorgabe des steuernden Chats):** Das Gesamtergebnis TB-137 liegt um 13:22 noch nicht vor. Vom Backlog gelesen: Kopf, Abschnitt 1, Abschnitt 3 (Kette) im Wortlaut; Abschnitte 2, 2s, 2z, 4, 5 (Kopf), 7 als Zeilenanfänge (je 210 Zeichen). Aus dem Register 54.6 ganz. Von den zehn Zeilen in 54.6 hängen Nr. 2, 6, 7, 9 an Fable, Nr. 3 bis 5 und 10 am Zellen-Erzeuger (Nr. 4 braucht eine Freigabe). **Nr. 1 und Nr. 8 und 53.10 Nr. 3 hängen an nichts davon** und sind „vor dem signierten Tag“ fällig: die Verfahrensmessung am Snapshot. Darum TB-138 = diese Messung; der Regelwerk-Nachtrag (bisher als „ab 138“ geführt) bekommt die nächste Nummer.
- **Bestandsaufnahme (Helfer, nur lesend, zwischen den Messungen 13:22 und 13:32; Anfang und Ende nicht einzeln gemessen):** Bericht unter `logs/steuernder_chat/TB-138_bestand_verfahrensmessung_helferbericht.md` (39 094 B, md5 `55504357c98f2258e96bb02cff82eac5`), mit Wortlauten und den Zeichen-Offsets der Unterpunkte. Kern:
  - R74 (e) (Block Z. 11524): „Vor dem signierten Tag wird in der Lock-Umgebung am Snapshot gemessen (Verfahrensmessung nach 27.2, zusammen mit der Messung nach R72 (d)), dass die Bedingung aus R66 (b) für den Kalender nach (a) erfüllt ist, je Aktien-Bot. Ist sie es nicht, wird gemeldet und vor dem Tag entschieden; […]“.
  - R66 (b) (Block Z. 11414): An jedem Handelstag des Zeitraums nach (a) trägt mindestens ein Symbol der Universumsdatei des Bots im Snapshot einen Kurs, und kein Symbol trägt einen Kurs an einem Tag, der kein Handelstag ist (Wortlaut gekürzt im Bericht; vor dem Auftrag ganz schneiden).
  - R72 (d) (53.7, Block Z. 11468): keine Kursreihe eines Symbols der zwei Universumsdateien endet vor dem letzten Kurstag ihres Marktes; Zahl der Symbol-Tage Lücke im Zeitraum nach R66 (a). 53.10 Nr. 3 (Z. 11507); Nr. 10 (Z. 11514) hängt an dieser Messung.
  - 54.5 Z. 11558: Stand zu R74 (e) „offen (54.6 Nr. 1 und Nr. 8)“.
  - Snapshot: `snapshots/63e4b6c8bb71…2ceb2/` liegt versioniert im Repo (226 Dateien, davon 223 CSV, `config/` mit 2 txt); Register Z. 3044/3049 nennt denselben Hash. Ab Z. 11412 nennt das Register für „den Snapshot“ der Messung weder Pfad noch Hash — im Auftrag als Lesart kennzeichnen.
  - Lock-Umgebung: `trading-env/` (`pyvenv.cfg` 3.9.6; dist-info `pandas_market_calendars-4.6.1`, `pandas-2.3.3`, `exchange_calendars-4.5.6`); Register Z. 11491 schreibt „Python der Lock-Umgebung (`trading-env/bin/python3`)“. `requirements.lock` Z. 51 `pandas-market-calendars==4.6.1`.
  - Kalender: `notifications/boersenkalender.py` Z. 70 `KALENDER_NAME = "NYSE"`, Import Z. 81, einziger Aufruf Z. 109/125.
  - 54.6 Nr. 8: `eingaben.json`, Feld `kalender`: `paket_vorhanden` „5.4.0“; es kommt aus `importlib.metadata.version` des startenden Interpreters (`erhebung_eingaben.py` Z. 609, 613–618). Welcher Interpreter das war, ist nicht gemessen.
  - Aktien-Bots (Register Z. 3448, 4868, 5744, 5842): `elliott_wave_stocks`, `turtle_soup_stocks`, `rsi2_mean_reversion`, `volatility_breakout`; alle vier lesen `config/sp500_top150.txt` (Z. 1581, 1588).
  - Vorbild für die Bauart: `docs/auftraege/MAC_TB-115_drei_verfahrensmessungen.md` (8 584 B), `docs/ERGEBNIS_TB-115_drei_verfahrensmessungen.md`.
- **Noch zu tun für TB-138:** Vorbild TB-115 lesen (Gliederung und Ort des Messskripts); R66 (a) und (b), R72 (d), R74 (a) und (e) ganz aus dem Register schneiden (Skript); Auftrag aus Bausteinen bauen (nur lesend am Snapshot, neues Messskript mit Zielpfad im Repo, Ausgabe nur Tage und Zählungen, keine Kurse, keine Kennzahl); zwei Runden Gegenlesen; Zeiger umstellen; Sitzung über den Wächter anlegen. Kein Sperrlistenpfad wird geändert (Annahme, vor dem Schreiben an der Sperrliste messen).
- **Ampel:** 13:32 Verlauf 185 343 (Grundlast 135 477), grün, 14 657 unter Gelb. Der Auftragsbau ist der nächste grosse Block; dazu käme das Gesamtergebnis TB-137 (geschätzt rund 75 000). Umzug per Karte angefragt; bis zur Antwort nichts Neues im Arbeitsbaum ausser dieser Datei.

## Umzug 06.10.2026, 13:43 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 06.10.2026, per Karte (gestellt 13:34, beantwortet vor 13:42): „Jetzt umziehen (Empfohlen)“. Ampel 13:42: Verlauf 210 785 (Grundlast 135 477), gelb. Die drei Nachträge vom 06.10.2026 (10:51, 11:12, 13:33) tragen die Einzelheiten; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **TB-133 ist abgenommen** (06.10.2026, zehn Prüfungen, keine Abweichung gegen ein Soll), die Sitzung ist geschlossen, `ARBEITSWEISE.md`, `UMZUG.md`, `BACKLOG.md` und `UEBERGABE.md` sind in der Ablage erneuert.
- **TB-138 ist gewählt, aber nicht geschrieben:** Verfahrensmessung am Snapshot (Register 54.6 Nr. 1 und Nr. 8, 53.10 Nr. 3). Die Bestandsaufnahme liegt vor; der Auftragsbau ist der erste Schritt des neuen Chats. Betreiber 13:22: „Fahre im Backlog fort“.
- **TB-137 steht weiter aus.** Der Helferauftrag für die Abnahme ist geprüft und gelegt. Die festen Teile der nächsten Fable-Anfrage sind gegengelesen (Runde 1); die zwei Fragen warten auf die Pakete 3, 5 und 11.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `0c70853` (`0c708531d4342d4fe5c5dd6a04eaea35dd680fe8`, TB-133 D3, 06.10.2026, 07:47:38). Gemessen 13:42 ohne `git status` und ohne `git diff`: geändert nur `docs/projektfuehrung/UEBERGABE.md` (diese Datei, drei Nachträge und dieser Block, uncommittet); unverfolgt nichts. Keine `index.lock`. `docs/auftraege/AKTUELLER_AUFTRAG.md` unverändert (md5 `d18bbb80813661d507264aab8657b449`), zeigt noch auf TB-133.

Keine Sitzung läuft und keine wartet: `waechter.log` 08:49:38Z „1 Sitzung(en) mit TERM beendet, 0 noch da“. `logs/sitzungswaechter/letzter_satz.txt` trägt noch den Satz zu TB-133; kein Auftrag ist startklar.

Der nächste Mac-Auftrag nimmt `UEBERGABE.md` in Schritt 0 mit. Bis dahin darf der steuernde Chat den Arbeitsbaum anfassen (Auftrag legen, Zeiger umstellen); ab dem Legen des Auslösers gilt wieder: bis Schritt 0 keine weitere Datei, nach Schritt 0 nichts bis zur Abgabe.

### Block 3 — Tragende Zahlen

- **Register:** `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `9b7b060`, 11 581 Zeilen, 933 576 B, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc`. Höchster Block R77. Am Stand `d781f1b` (den die Cloud-Sitzung TB-137 sah) hat es 11 471 Zeilen: **Zeilennummern aus TB-137 gelten dort, nicht an HEAD.**
- **Regeldateien nach TB-133:** `ARBEITSWEISE.md` 2 413 Zeilen (156 926 B, md5 `e85163e98db7f0b9387f4c990b67f8ca`; Abschnitt 0 jetzt 25 681 B), `UMZUG.md` 380 (26 923 B; Abschnitt 3 jetzt 5 897 B), `BACKLOG.md` 317 (73 033 B). Journal: Block EF steht, nächste Kennung EG.
- **TB-138, Fundstellen der Bestandsaufnahme** (Bericht siehe Block 8): R74 (e) Block Z. 11524 · R66 (a), (b) Block Z. 11414 · R72 (d) Block Z. 11468 (Überschrift 53.7, Z. 11466) · 53.10 Nr. 3 Z. 11507, Nr. 10 Z. 11514 · 54.5 Z. 11558 (Stand „offen“) · 54.6 Nr. 1 Z. 11570, Nr. 8 Z. 11577 · 17.5 Z. 2827 (Paket 4.6.1, Python 3.9.6) · 27.2 Z. 5164. Snapshot `snapshots/63e4b6c8bb71…2ceb2/` (226 Dateien, 223 CSV; Register Z. 3044/3049 nennt den Hash). Lock-Umgebung `trading-env/` (Register Z. 11491: `trading-env/bin/python3`); `requirements.lock` Z. 51. `notifications/boersenkalender.py` Z. 70 `KALENDER_NAME = "NYSE"`. Feld `kalender` in `research/snapshotgrenze/ergebnisse/eingaben.json`: `paket_vorhanden` „5.4.0“ (aus `erhebung_eingaben.py` Z. 609, 613–618). Vier Aktien-Bots, alle mit `config/sp500_top150.txt`. Vorbild: `docs/auftraege/MAC_TB-115_drei_verfahrensmessungen.md` (8 584 B).
- **Ablage:** 96 Einträge; `UEBERGABE.md` mit diesem Block hochgeladen (Helfer; Stand in der Antwort des Chats).
- **Projekt-Erinnerung:** `preferences.md` 9 440 B, `ways-of-working.md` 2 723 B (gelesen 07:40; seither von diesem Chat nicht geändert). Vor der Eröffnung für Fable alle vier Dateien neu gegen 27.1 messen.
- **Nummern:** TB-138 vorgesehen für die Verfahrensmessung (noch kein Auftrag, kein Zeiger); der Regelwerk-Nachtrag bekommt die Nummer danach. Journal ab EG. Neue Blöcke ab R78. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Tages, an dem sie hinausgeht.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-138 bauen** (Mac-Auftrag, Verfahrensmessung am Snapshot, nur lesend, neues Messskript mit Zielpfad im Repo; Ausgabe nur Tage und Zählungen, keine Kurse, keine Kennzahl). Schritte: Vorbild TB-115 (Gliederung, Ort des Messskripts, Belege) über einen Helfer oder gezielt lesen · R66 (a) und (b), R72 (d), R74 (a) und (e), 53.10 Nr. 3, 54.6 Nr. 1 und Nr. 8 per Skript aus dem Register schneiden (Offsets im Bericht) · an der Sperrliste messen, dass kein Sperrlistenpfad geändert wird · Auftrag aus Bausteindateien per Skript bauen · zwei Runden Gegenlesen (frische Helfer) · Zeiger umstellen, Auftrag legen, md5 beidseitig · Sitzung über den Wächter anlegen · Einfügesatz als Kopierblock. Drei Messungen: (M1) Bedingung aus R66 (b) je Aktien-Bot für den Kalender „NYSE“ in der Lock-Umgebung; (M2) R72 (d): Reihenenden und Symbol-Tage Lücke; (M3) 54.6 Nr. 8: Paketfassung in `trading-env` gegen „5.4.0“ im Feld `kalender`. **Lesarten, im Auftrag als „Lesart, vorläufig“ zu kennzeichnen:** dass „der Snapshot“ der Ordner mit dem Hash aus Z. 3044/3049 ist; der Zeitraum nach R66 (a) (Wortlaut vorher ganz lesen); „letzter Kurstag ihres Marktes“. Der Betreiber hat der Wahl nicht widersprochen (Vorgabe im Chat 13:34); der Auftrag läuft unter der pauschalen Freigabe für Handwerk ohne Sperrlistennähe, sofern die Messung an der Sperrliste das bestätigt. Das Ergebnis führt zu einem Registereintrag (54.5, Stand zu R74 (e)) — das ist dann eine Einzelfreigabe.
2. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt (bis rund 120 000 Zeichen; danach sofort die Ampel messen). Helferauftrag: `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; `⟨PFAD_ERGEBNIS⟩` einsetzen; c1 neu aus dem Archiv nach ausserhalb des Repos entpacken (`cloud/c1_stichproben_cloud_tb134_tb135.md`, 22 690 B, md5 `edc4c1eb2a1ba1b2b0389cc0f0727786`); Registerkopie vom Stand `d781f1b` mit `git show` ziehen. Die Pakete 8 und 12 berühren TB-138 (Pflichten vor dem Tag; Kalender und Paketfassungen): kommen sie vor dem Start von TB-138, gegen den Auftrag halten.
3. **Anfrage an Fable fertigschreiben** (neuer Fable-Chat): `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md`, dort „Vor dem Absenden“ (sieben Schritte) und die Liste der Runde 1; Bauplan daneben.
4. **Regelwerk-Nachtrag** (Nummer nach TB-138), nach TB-137: `diff --name-only` in `ARBEITSWEISE.md` Z. 134 und `UMZUG.md` Z. 266; der Fliesstext in `ARBEITSWEISE.md` 6b und 10; die Regel zu Cloud-Sitzungen; der Entwurf aus Paket 15; die zwei Befunde aus der Abnahme TB-133 (Nachtrag 10:51); die Regeln aus Block 7 hier.
5. **Backlog und Journal zur Abnahme TB-133** (ARBEITSWEISE 5b): noch nicht eingetragen. Mit TB-138 mitgeben (Journalblock der Sitzung) oder mit dem Regelwerk-Nachtrag; im Chat um 10:52 als Vorgabe „mit dem nächsten Mac-Auftrag“ genannt.
6. **`AKTUELLER_AUFTRAG.md`** beim Legen von TB-138 umstellen.

### Block 5 — Wartezustände

TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. TB-138 wartet auf den Auftragsbau durch den neuen Chat. Keine Sitzung läuft, keine Karte ist offen, keine Nachschau ist geplant.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- 06.10.2026, 07:42: Ordnerfreigabe für `~/trading-bot`. Zwischen 07:43 und 07:45: Satz zu TB-133 abgeschickt. 10:42: Meldung der Sitzung eingefügt.
- 10:58: „weiter“. 13:22: „Fahre im Backlog fort“.
- Karte zum Umzug (gestellt 13:34): „Jetzt umziehen (Empfohlen)“.
- Vorgaben ohne Widerspruch: Die Abnahme von TB-133 kommt mit dem nächsten Mac-Auftrag in Backlog und Journal (10:52). TB-138 ist die Verfahrensmessung am Snapshot, der Regelwerk-Nachtrag bekommt die nächste Nummer (13:34).
- Keine Freigabe für Register, Sperrliste, Signalpfad oder Parameterdateien.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. Im Nachtrag 13:33 stand für den Helferlauf eine geschätzte Uhrzeit („13:24–13:31“); im nächsten Schritt berichtigt. ⇒ Wie gehabt: Uhrzeiten mit `date`, im selben Schritt; für Helferläufe Anfang und Ende messen oder die Spanne zwischen zwei Messungen nennen.
2. Ampel: 41 266 (07:43) · 86 633 (10:52) · 139 186 (11:11) · 185 343 (13:32) · 197 820 (13:34) · 210 785 (13:42). Rund 46 000 kostete allein die Runde „Fahre im Backlog fort“: 17 KB Zeilenanfänge des Backlogs im Chat, dazu 54.6 und ein Helferbericht. Davor 53 000 für die Runde „weiter“: Fable-Entwurf und Bauplan ganz gelesen (18 KB), 12 KB aus dem Gegenleserbericht, zwei Helferaufträge von 5 bis 7 KB im Chat geschrieben. ⇒ Backlog-Übersichten in eine Datei schreiben und nur die Kandidaten in den Chat holen; Helferaufträge aus Bausteinen per Skript; aus Helferberichten nur die Abweichungen lesen.
3. Die Helferaufträge (Abnahme TB-133, Ablage, Gegenleser, Bestandsaufnahme) liefen ohne eigenen Gegenleser; beim Helferauftrag TB-137 hat ein Skript die Zeilenangaben an der Quelle geprüft. Kein Schaden gemessen.
4. Was getragen hat: enge Helfer mit Berichtsgrenze und Berichtsdatei; Berichtigungen per Skript mit `assert` auf genau einen Treffer; md5 und Bytes auf beiden Seiten nach jedem Ablegen; Arbeitsstände sofort nach `logs/steuernder_chat/`; die Karte zum Umzug vor dem grossen Block statt danach.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert): `TB-138_bestand_verfahrensmessung_helferbericht.md` (39 094 B, md5 `55504357c98f2258e96bb02cff82eac5`) · `HELFER_AUFTRAG_TB-137_abnahme.md` (4 059 B, md5 `2af399ded19a61ee21bbb46de98b7ac3`) · `FABLE_naechste_anfrage_feste_teile.md` (15 621 B, md5 `66e1b6626fa1acb10409063fcab199f5`) · `FABLE_04b_bauplan.md` · `CLOUD_TB-137_sammelauftrag_leseaufgaben.md` · `2026-10-04_tb136_bau.tar.gz` · `vorzaehlung_tb133.py`. Dazu Arbeitskopien, die seit dem Commit `1ea5213` überflüssig sind (`TB-133_entwurf.md`, `TB-133_entwurf_v2.md`, vier `NACHTRAG_…`-Dateien, zwei `UMZUG_…`-Dateien) — nicht ohne Frage löschen.
- Verfällt mit diesem Chat: die Ordner der Helfer in der Umgebung der Geräteanbindung (`tb133_abnahme/`, `tb137_abnahme/` mit c1 und der Registerkopie `d781f1b`, `fable_gegenleser/`, `tb138_bestand/`) und im Arbeitsbereich des Chats die Helferaufträge und die Berichte zur Abnahme TB-133 und zum Gegenlesen (ihr Ertrag steht in den Nachträgen 10:51 und 11:12 und am Ende des Fable-Entwurfs).
- Die Punkte „für später“ aus dem Umzug 04.10.2026, 10:56, Block 8, gelten unverändert.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, als erste Nachricht nach dem Ja des Betreibers. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 06.10.2026, 14:25 — neuer steuernder Chat: TB-138 gebaut, gegengelesen, gelegt

- **Übernahme 13:46:** Ordnerfreigabe für `~/trading-bot` vom Betreiber erteilt (Karte der Geräteanbindung). HEAD `0c70853`, `BACKLOG.md` 317 Zeilen, geändert nur diese Datei, unverfolgt nichts. Ablage lesbar (96 Einträge).
- **TB-138 gebaut:** `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md` (33 392 B, md5 `3fbed4ebcb5d0cf4ddcd4ae10c9cea36`), per Skript aus einer Vorlage; das Skript schneidet die Registerwortlaute und prüft 139 Angaben an der Quelle. Zwei Runden Gegenlesen mit drei frischen Helfern (1a Quellen, 1b Logik, 2 Nachlese): Runde 1 nannte fünf Fehler und 23 Lücken (1b) und acht Stellen (1a), Runde 2 vier Fehler und neun Lücken; eingearbeitet, soweit sie den Auftrag betreffen. Nach Runde 2 hat kein weiterer Leser geprüft; die Berichtigungen der Runde 2 hat nur das Bauskript geprüft. Bauteile und Berichte unter `logs/steuernder_chat/TB-138_*`.
- **Drei Messungen:** M1 Bedingung aus R66 (b) für „NYSE“ je Aktien-Bot in `trading-env`; M2 Reihenenden und Symbol-Tage Lücke, dazu 53.10 Nr. 10; M3 Paketfassung (54.6 Nr. 8). Neun Lesarten (L1–L9), als vorläufig gekennzeichnet; der Beginn je Bot kommt aus Register 33.2 (Z. 5994–6004) unter dem Vorbehalt aus R53 (Z. 11005). 53.10 Nr. 10 hat der steuernde Chat dazugenommen (Register Z. 11514 bindet sie an Nr. 3): Vorgabe, gilt, wenn der Betreiber nicht widerspricht.
- **Befunde nebenbei:** `research/vorregistrierung/ergebnisse/faltenplan.json` (im Abbild eingefroren) führt den Stand TB-30a (erste Falte 2019 bei allen vier Aktien-Bots, Krypto „platzhalter“) und ist nicht die Quelle für den Beginn. `XAUTUSDT` hat im Snapshot nur eine `_1h`-Reihe. Der Commit `fc38d25` (Feld `kalender`, 5.4.0) trägt Autor „Claude“ und die Zeitzone +0000.
- **Zeiger:** `AKTUELLER_AUFTRAG.md` zeigt auf TB-138 (md5 `665f314bd9cfb9c00c72ecb606804807`). Backlog und Journal zur Abnahme TB-133 gehen mit TB-138 mit (Schritt B, D2). Der Auslöser `starte_TB-138` wird nach diesem Nachtrag gelegt; ab dann fasst der steuernde Chat den Arbeitsbaum bis zur Abgabe nicht an.
- **Nummern:** Journal EG erwartet für TB-138; der Regelwerk-Nachtrag bekommt die Nummer nach TB-138.
- **Fehler dieses Chats (ohne Nummer):** zwei Werkzeugausgaben ohne Grenze (Ordnerliste des Wächters, 40 Trefferzeilen aus dem Auftrag TB-136) und eine zu knappe Rechnung für das Einlesen. Ampel: Verlauf 31 644 (13:47) · 120 047 (13:52) · 163 553 (14:10) · 203 332 (14:23, gelb). Im ersten Entwurf stützte sich der Beginn je Bot nur auf 21.5; die Tabelle 33.2 und den Vorbehalt aus R53 fand erst der Gegenleser. ⇒ Vor einer Lesart zum Zeitraum im Index nachsehen, was er zu der Stelle als „gilt“ und „dazu“ führt; jede `ls`- und `grep`-Ausgabe mit `head` begrenzen.
- **Offen wie im Umzugsblock 13:43:** TB-137 (Abnahme, sobald das Ergebnis kommt), die Anfrage an Fable, der Regelwerk-Nachtrag. Die Ablage trägt `UEBERGABE.md` noch im Stand 13:43.

## Umzug 06.10.2026, 16:40 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 06.10.2026, per Karte (gestellt nach der Ampel von 14:26, Antwort eingetragen 15:07): „Nach Abgabe TB-138 (Empfohlen)“. 16:37: „Tb138 fertig“. Ampel 16:40: siehe Antwort des Chats (zuletzt gemessen 15:07: Verlauf 249 089, Grundlast 128 903, gelb). Der Nachtrag vom 06.10.2026, 14:25, trägt die Einzelheiten zum Bau; dieser Block genügt zum Weiterarbeiten.

### Block 1 — Stand in drei Zeilen

- **TB-138 ist abgegeben, aber nicht abgenommen** (sechs Commits `5e7037a` bis `8d172c0`, 15:53 bis 16:05). Aus der Journalüberschrift EG der Sitzung, vom steuernden Chat **nicht nachgerechnet**: Kalender „NYSE“ erfüllt R66 (b) bei allen vier Aktien-Bots (0/0 über 16 275 Tage seit 1962); **R72 (d) ein Befund: `APH` endet mit Kurs am 2026-08-31, der Markt am 2026-09-01**; Lücken Aktien 2, Krypto 0; doppelte Daten und Zeitanteile 0; Paketfassung in `trading-env` 4.6.1 gleich Lock, 5.4.0 aus der Cloud-Sitzung von TB-47; Gegenprobe 12/12. Gemessen vom steuernden Chat: rc `m1` 0, `m2` 1, `m3` 0; kein `abbruch.txt`; `d3_porcelain.txt` 0 B.
- **Die Abnahme von TB-138 ist der erste Schritt des neuen Chats.** Der Helferauftrag liegt bereit (Block 8).
- **TB-137 steht weiter aus.** Fable-Anfrage und Regelwerk-Nachtrag warten wie im Umzugsblock 13:43.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `8d172c0` (TB-138 D3, 06.10.2026, 16:05:05). Kette des Tages nach `0c70853`: `5e7037a` Schritt 0 (15:53:41) · `9833724` A: Messskript, Gegenprobe, M1–M3 · `a5cb034` B: BACKLOG · `b923a05` Abgabe: Ergebnis, Journal EG · `439834c` D3 numstat und porcelain · `8d172c0` D3 porcelain neu gemessen. Gemessen 16:38 ohne `git status` und ohne `git diff`: geändert nichts, unverfolgt nichts, keine `index.lock`. **Seit 16:40 ist `docs/projektfuehrung/UEBERGABE.md` wieder geändert und uncommittet (dieser Block);** der nächste Mac-Auftrag nimmt sie in Schritt 0 mit.

**Die Sitzung TB-138 schläft noch:** Wächter-Sonde `starte_TB-99`, 14:38:21Z: „claude im Repo: PID 21434 (Laufzeit 02:12:49, Rechenzeit 1:48.02, S+)“, Start abgewiesen. Schliessen nach der Abnahme über den Schliess-Auslöser (Name nach dem Muster in `docs/auftraege/_ausloeser/_erledigt/`: `schliesse_<voller HEAD-Hash>`, erschlossen; vorher `LIESMICH.md` des Wächters lesen und das Alter des letzten Commits messen, ab 600 s). `AKTUELLER_AUFTRAG.md` zeigt auf TB-138 (md5 `665f314bd9cfb9c00c72ecb606804807`); `letzter_satz.txt` trägt den Satz zu TB-138; kein Auftrag ist startklar.

### Block 3 — Tragende Zahlen

- **Register:** unverändert, 11 581 Zeilen, sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc` (gemessen 16:38), Stand `9b7b060`. Höchster Block R77.
- **TB-138:** Auftrag `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md` (33 392 B, md5 `3fbed4ebcb5d0cf4ddcd4ae10c9cea36`, committet in `5e7037a`) · Ergebnis `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md` (18 100 B, 181 Zeilen, md5 `ac4d8a31c50a6e90e8b2df0cb3a3bf7d`) · Belege `docs/belege/TB-138/` (19 Einträge; `m1.txt` 6 097 B, `m2.txt` 4 124 B, `m3.txt` 1 233 B, `m3_shell.txt` 1 179 B, `gegenprobe.txt` 21 112 B, `d3_numstat.txt` 20 Zeilen).
- **Regeldateien:** `ARBEITSWEISE.md` 2 413 Zeilen (156 926 B, md5 `e85163e98db7f0b9387f4c990b67f8ca`; Abschnitt 0: 25 681 B) · `UMZUG.md` 380 Zeilen (26 923 B; Abschnitt 3: 5 897 B) · `BACKLOG.md` 323 Zeilen (73 765 B, md5 `5721615ef4d59f600018e08d681fc5c8`; sechs Zeilen mehr als 317, wie im Auftrag vorgesehen). Journal: Block EG steht (Z. 10056), nächste Kennung EH.
- **Für den Zeitraum nach R66 (a), im Auftrag als Lesarten L3 und L4, vorläufig:** Ende 31.08.2026 einschliesslich (Register 35.1, Z. 6375, Z. 6385–6388); Beginn je Bot aus Register 33.2, Tabelle Z. 5994–6004 (Aktien 2017/2018/2017/2018; Krypto 2018–2019, 2019, 2019, 2018, 2018), unter dem Vorbehalt aus R53 (49.1, Z. 11005: „die erste Falte ist nach dieser Präzisierung neu abzuleiten“; der Vorlauf nach R53 (a) offen in Z. 11208 und Z. 11323).
- **Ablage:** 96 Einträge (gemessen 13:46). `UEBERGABE.md` mit diesem Block: Stand in der Antwort des Chats. `BACKLOG.md` in der Ablage trägt noch den Stand vor TB-138.
- **Projekt-Erinnerung:** in diesem Chat nicht gelesen und nicht geändert (Stand wie im Umzugsblock 13:43). Vor der Eröffnung für Fable alle vier Dateien neu gegen 27.1 messen.
- **Nummern:** nächster Auftrag nach TB-138 (vorgesehen: Regelwerk-Nachtrag; die Nummer TB-139 ist erschlossen, im Backlog nicht nachgesehen). Journal ab EH. Neue Blöcke ab R78. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Tages, an dem sie hinausgeht.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-138 abnehmen** (zuerst, weil die Sitzung noch schläft und der Befund zu `APH` eine Entscheidung vor dem Tag verlangt). Enger Helfer, nur lesend: `logs/steuernder_chat/HELFER_AUFTRAG_TB-138_abnahme.md`. Danach rechnet der steuernde Chat die Kernzahlen mit eigenen Befehlen nach (letzter Kurstag `APH` gegen den Markt, nur die Datumsspalte; die Zählungen 0/0 und 16 275; rc der drei Messungen). Dann die Sitzung schliessen (Block 2), Backlog- und Journal-Nachtrag zur Abnahme mit dem nächsten Mac-Auftrag.
2. **Befund `APH` (R72 (d): „Endet eine Reihe früher, wird gemeldet und vor dem Tag entschieden“):** nach der Abnahme dem Betreiber melden; die Entscheidung ist eine Verfahrensfrage (Fable) und kein Handwerk. Das Ende des Zeitraums nach L3 ist der 31.08.2026: ob die Reihe im Zeitraum vollständig ist, steht im Ergebnis und ist bei der Abnahme zu prüfen (nicht gemessen).
3. **Registereintrag nach TB-138** (54.5, Stand zu R74 (e); 53.10 Nr. 3 und Nr. 10; 54.6 Nr. 1 und Nr. 8): **Einzelfreigabe des Betreibers**, eigener Registerauftrag; der Chat, der abnimmt, baut ihn nicht selbst, wenn die Ampel es nicht trägt.
4. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt (bis rund 120 000 Zeichen; danach sofort die Ampel messen). Helferauftrag `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilennummern gelten am Stand `d781f1b`. Die Pakete 8 und 12 gegen Auftrag und Ergebnis TB-138 halten.
5. **Anfrage an Fable fertigschreiben** (neuer Fable-Chat): `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md` („Vor dem Absenden“), Bauplan daneben. Dazu neu, zur Kenntnis oder als Frage: der Befund `APH`; die Lesarten L1–L9 aus TB-138; `faltenplan.json` im Abbild führt den Stand TB-30a; `XAUTUSDT` hat im Snapshot nur eine `_1h`-Reihe.
6. **Regelwerk-Nachtrag** (nach TB-137), wie Umzugsblock 13:43, Block 4 Nr. 4; dazu die Regeln aus Block 7 hier und aus dem Nachtrag 14:25.
7. **Ablage:** `BACKLOG.md` erneuern (erst nach der 27.4-Prüfung), durch einen Helfer.
8. **`AKTUELLER_AUFTRAG.md`** beim Legen des nächsten Auftrags umstellen.

### Block 5 — Wartezustände

TB-138 wartet auf die Abnahme durch den neuen Chat; die Sitzung PID 21434 wartet auf das Schliessen. TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Keine Karte ist offen, keine Nachschau ist geplant, keine Rückfrage an Sitzung oder Fable ist offen.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- 06.10.2026, 13:46: Ordnerfreigabe für `~/trading-bot`. Zwischen 15:07 und 15:53: Satz zu TB-138 abgeschickt (erschlossen aus dem Commit von Schritt 0, 15:53:41). 16:37: „Tb138 fertig“.
- Karte zum Umzug: „Nach Abgabe TB-138 (Empfohlen)“ (eingetragen 15:07).
- Vorgaben ohne Widerspruch (im Chat genannt 14:26): 53.10 Nr. 10 läuft in TB-138 mit; die Lesarten L1–L9 gelten als vorläufig; die Abnahme von TB-133 kommt mit TB-138 in Backlog und Journal; TB-137 wird nicht mehr in den alten Chat eingefügt.
- TB-138 lief unter der pauschalen Freigabe für Handwerk ohne Sperrlistennähe (an der Sperrliste gemessen: kein Pfad des Abbilds unter `docs/`).
- **Keine Freigabe** für Register, Sperrliste, Signalpfad oder Parameterdateien.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. Wie Nachtrag 14:25: zwei Werkzeugausgaben ohne Grenze; Einlesen und Bestand teurer als gerechnet; der Beginn je Bot zuerst nur auf 21.5 gestützt. ⇒ Jede `ls`- und `grep`-Ausgabe mit `head` begrenzen; vor einer Lesart den Index nach „gilt“ und „dazu“ fragen.
2. Das Ablege-Skript scheiterte an einer falschen Zählung im Zeiger (`TB-138` dreimal, nicht zweimal), **nachdem** es den Auftrag schon kopiert hatte; der zweite Lauf brauchte eine Ausnahme. Kein Schaden gemessen (md5 beidseitig gleich). ⇒ Ein Ablege-Skript prüft erst alles und schreibt dann; es ist wiederholbar gebaut.
3. Ampel: 31 644 (13:47) · 120 047 (13:52) · 163 553 (14:10) · 203 332 (14:23) · 235 294 (14:26) · 249 089 (15:07). Die erste Runde kostete rund 88 000 in fünf Minuten: Kernlektüre 43 KB, Bestandsbericht 30 KB, dazu Vorbild und zwei Aufträge. ⇒ Den Bestandsbericht durch einen Helfer auf die Stellen kürzen lassen, die der Bau braucht; der Chat, der einen Auftrag baut, liest die Kernlektüre und sonst nur Ausschnitte.
4. Die Berichtigungen aus Runde 2 des Gegenlesens hat nur das Bauskript geprüft, kein weiterer Leser. Bei der Abnahme darauf achten (Gegenprobe-Tabelle G1–G8, Urteil-Regel in M1 Nr. 4).
5. Was getragen hat: Bauskript mit 139 Prüfungen an der Quelle; zwei gleichzeitige Gegenleser mit getrenntem Zuschnitt (Quellen, Logik) und ein dritter für die Nachlese; die Tabelle je Kalenderjahr als Schutz gegen vorläufige Lesarten; die Karte zum Umzug vor dem Warten statt danach.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert), neu aus diesem Chat: `HELFER_AUFTRAG_TB-138_abnahme.md` (3 377 B, md5 `3dbe153ea2b9f1809904fc90267c6f3b`) · `TB-138_entwurf_v1.md`, `_v2.md`, `_v3.md` (v3 gleich dem gelegten Auftrag) · `TB-138_bau_vorlage.md`, `TB-138_bau_bauen.py`, `TB-138_bau_runde1.py`, `TB-138_bau_runde2.py`, `TB-138_bau_ablegen.py`, `TB-138_nachtrag_vorlage.md` · `TB-138_gegenlesen_1a.md`, `_1b.md`, `_2.md` (1b führt sechs Sprachhinweise und 16 Hinweise, 2 weitere 16, nicht einzeln eingearbeitet) · `TB-138_notiz_entscheide.md`. Nicht ohne Frage löschen.
- Unverändert von früher: die Dateien aus dem Umzugsblock 13:43, Block 8 (Helferauftrag TB-137, feste Teile der Fable-Anfrage, Bauplan, Cloud-Sammelauftrag, Archiv TB-136, die überflüssigen Arbeitskopien).
- Verfällt mit diesem Chat: der Ordner `tb138/` und `kern/` in der Umgebung der Geräteanbindung (alles Tragende ist nach `logs/steuernder_chat/` kopiert).

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, als erste Nachricht der Antwort nach „Tb138 fertig“. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 06.10.2026, 20:18 — TB-138 abgenommen, Sitzung geschlossen

Betreiber, 06.10.2026, 20:10: „weiter im backlog“ (im alten Chat; der Umzug war für die Zeit nach der Abgabe entschieden, ein neuer Chat ist nicht eröffnet). Der alte Chat hat deshalb Block 4 Nr. 1 des Umzugsblocks 16:40 selbst erledigt. **Dieser Nachtrag geht dem Umzugsblock 16:40 in Block 1, Block 2 (Sitzung), Block 4 Nr. 1 und Block 5 vor.**

- **TB-138 ist abgenommen** (06.10.2026). Helfer, nur lesend, zehn Prüfungen: sieben ohne Abweichung, drei mit formaler Abweichung, keine gegen einen Messwert. Kein Kurs, keine Rendite, keine Kennzahl in Belegen, Ergebnis oder Journalblock. Bericht: `logs/steuernder_chat/TB-138_abnahme_helferbericht.md` (11 264 B, md5 `8c8251032bfd56d3cd723d3df6926d58`).
- **Abweichungen:** (1) `0b_nachher.txt` weicht in drei Kopfzeilen von `0b_ausgang.txt` ab (Marke, Zeit, HEAD); alle Messwerte sind gleich. (2) Zwei D3-Commits statt einem: In `439834c` trug `d3_porcelain.txt` eine Zeile (`?? docs/belege/TB-138/d3_numstat.txt`), `8d172c0` mass neu; am HEAD hat die Datei 0 B. (3) Das Ergebnis führt Abweichungen vom Auftrag nicht als solche: Das Skript prüft bei Zeilen nach dem letzten Kurstag auch, welche übrigen Spalten leer sind (ausgegeben werden nur Spaltennamen); H je Bot ist ein Ausschnitt der einmal gerechneten Menge und kein eigener `schedule`-Aufruf (ob beides dasselbe liefert, ist nicht gemessen); „In einfacher Sprache“ trägt eine Vermutung („wohl nicht“, Z. 178). Der Beginn je Bot steht als feste Tabelle im Skript (Z. 46–54), wie L4 es vorgibt.
- **Vom steuernden Chat nachgerechnet** (20:16, eigene Befehle am Snapshot, nur die Datumsspalte und ob `close` fehlt): Aktien 150 Reihen, 16 275 Kurstage von 1962-01-02 bis 2026-09-01 (16 274 bis 31.08.2026); früher endend nur `APH` (2026-08-31); `close` fehlt genau einmal; zwei Lücken (`LMT` 1974-06-03, `MNST` 2026-08-10), gerechnet gegen die Kurstage als Ersatz für den Kalender; kein doppelter Tag. Krypto 24 Reihen, 3 316 Tage von 2017-08-17 bis 2026-09-14, keine früher endende Reihe, keine Lücke, kein doppelter Tag. **Nicht nachgerechnet:** der Vergleich mit dem Kalender „NYSE“ in der Lock-Umgebung (0 Tage nur im Kalender, 0 nur in den Daten); er steht nur in der Ausgabe der Sitzung (`m1.txt`).
- **Befund zu R72 (d), genauer:** `APH` hat am 2026-09-01 eine Zeile mit leerem `open`, `high`, `low` und `close` (`m2.txt` Z. 25–27, `m1.txt` Z. 118–120). Der letzte Kurs liegt am 2026-08-31, dem Ende des Zeitraums nach L3; bis dahin hat `APH` keine Lücke. Der Befund hängt an den Lesarten L5 und L7. R72 (d) verlangt: melden und vor dem Tag entscheiden. Dem Betreiber im Chat gemeldet; die Entscheidung ist eine Verfahrensfrage und geht in die nächste Anfrage an Fable.
- **M3:** Die vier Paketfassungen in `trading-env` sind gleich dem Lock. Zu „5.4.0“: `docs/ERGEBNIS_TB-47_snapshotgrenze.md` Z. 3, Z. 122, Z. 348 und Z. 359 (Cloud-Sitzung vom 18.09.2026, Python 3.11.15, Paket 5.4.0 nachinstalliert). Dass dieser Interpreter das Feld `kalender` schrieb, ist erschlossen.
- **Sitzung TB-138:** Schliess-Auslöser `schliesse_<HEAD>` gelegt um 20:18; `waechter.log`: „1 Sitzung(en) mit TERM beendet, 0 noch da.“.
- **Noch offen aus der Abnahme:** Backlog- und Journal-Nachtrag zur Abnahme TB-138 mit dem nächsten Mac-Auftrag (5b). Der Registereintrag nach TB-138 braucht die Einzelfreigabe des Betreibers.
- **Ampel:** 279 597 (16:41) · 295 029 (19:40); der Stand nach diesem Nachtrag steht in der Antwort des Chats.

## Nachtrag 06.10.2026, 21:00 — Bestandsaufnahme zum Registereintrag nach TB-138: in der Hauptsache kein Vorbild für einen Eintrag ohne Fable

- **Betreiber, Karte nach der Ampel von 20:19 (Verlauf 316 395, rot):** „Hier weiterbauen“ — der Registerauftrag zu TB-138 soll im alten Chat entstehen. Der Eröffnungstext von 16:41 ist überholt und nicht ersetzt.
- **Zwei Helfer, nur lesend:** `logs/steuernder_chat/TB-139_bestand_A1.md` (Bauart TB-136, 42 979 B, md5 `3e1fa205aa165f3bb8683a0a6226bf6f`) und `logs/steuernder_chat/TB-139_bestand_A2.md` (Vorbilder und Markenregeln im Register, 61 516 B, md5 `1fa0890646d6261747f3bd3b871f76f5`).
- **Befunde aus den Helferberichten** (vom steuernden Chat nicht nachgemessen):
  1. Die Ergebnisse der Verfahrensmessungen TB-115 kamen **über Fable** ins Register: Tagesanfrage 27a, Antwort, dann TB-117 mit Fable-Blöcken (R11, R13, R17; Register Z. 10358–10552). Kein eigener Abschnitt, keine Notiz des steuernden Chats.
  2. Abschnitte ohne Fable-Block gibt es: 44 (Z. 9855) und 50 (Z. 11030, TB-126; Einleitung endet „Die Nummer hat der steuernde Chat vergeben, nicht Fable“). Marke ohne Fable: Z. 1250 („11.3 ERGÄNZT durch 50.3 und 50.4 (Tatsachennotiz, …, TB-126, 01.10.2026)“).
  3. Statuslisten wie 53.10 und 54.6 bekommen keine Marke (R61 (b), Z. 11272; R77 (c), Z. 11545). Die Erledigung steht im Schlusssatz des neuen Abschnitts (Vorbild Z. 11581).
  4. Eine Zeilenmarke an einer Befundtabelle (54.5, 53.9) setzt nach R65 (a) (Z. 11367) „einen Block“ voraus. Ein Markenwort für „offen, jetzt gemessen“ gibt es nicht (ERGÄNZT 74, PRÄZISIERT 69, BERICHTIGT 11, je einmal NACHGETRAGEN, VOLLZOGEN, BEANTWORTET).
  5. Das Register sagt nicht, wer das Ergebnis einer Verfahrensmessung einträgt und ob der Verfahrensprüfer es vorher sieht. Für „Bedingung erfüllt“ (R74 (e)) nennt es keinen Folgeschritt; für R72 (d) verlangt es Meldung und Entscheidung vor dem Tag.
  6. Prüf- und Einfügeskript von TB-136 setzen eine Fable-Quelle voraus (Auftrag TB-136, Anhang A, Z. 588, 621–638, 824–848, 872). T4 der Registerkopie hat 5 409 B Luft bis 240 000. Sollwert `herkunft.register()` nach TB-136: `cfff54ca81d3dbf594a28880b17d4ba8389e0436c2d48cd50248586c1de03a81` (ERGEBNIS_TB-136 Z. 81; heute nicht gemessen).
- **Folgerung des steuernden Chats, vorläufig:** Der Weg mit Vorbild ist: Ergebnis TB-138 und Befund `APH` zuerst als Anfrage an Fable, danach **ein** Registerauftrag der Bauart TB-136, der Fables Blöcke und die Tatsachennotizen zusammen einträgt. Ein eigener Abschnitt 55 ohne Fable hätte die Bauart von Abschnitt 50, bliebe ohne Zeilenmarken und zöge nach Fables Antwort einen zweiten Registerauftrag nach sich. Dem Betreiber als Karte vorgelegt; die Antwort steht im nächsten Nachtrag.
- **Fehler dieses Chats (ohne Nummer):** Die Vorgabe von 20:19 („als Nächstes kommt der Registereintrag zu TB-138“) stand, bevor gemessen war, wie das Register Messergebnisse aufnimmt; die Karte „Hier weiterbauen“ fragte deshalb nach dem Ort für einen Bau, dessen Weg nicht feststand. ⇒ Vor einer Vorgabe zur Reihenfolge das Vorbild im Register messen lassen.
- **Nummern:** TB-139 ist nicht vergeben; kein Auftrag ist gelegt, kein Zeiger umgestellt.

## Nachtrag 06.10.2026, 21:30 — Anfrage 06.10.a an Fable gebaut (TB-138: Befund `APH`, Form des Eintrags)

- **Betreiber, Karte nach dem Nachtrag 21:00:** „Erst Fable, dann ein Eintrag (Empfohlen)“. Das Ergebnis TB-138 geht als eigene Anfrage an einen neuen Fable-Chat, ohne auf TB-137 zu warten; danach trägt **ein** Registerauftrag der Bauart TB-136 Fables Blöcke und die Tatsachennotizen ein. Kein Auftrag ist gelegt, TB-139 ist nicht vergeben.
- **Dateien, vom steuernden Chat gelegt, unverfolgt** (der nächste Mac-Auftrag nimmt sie in Schritt 0 mit): `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md` (11 681 B, md5 `06ae4b76831d547cff57b2d2ce425dfb`) und `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-06_eroeffnung.md` (7 295 B, md5 `6e9fa10d1e7ae7c733ad1d889c6e81d4`). Für die Ablage dazu das Ergebnis TB-138 ohne den Abschnitt „In einfacher Sprache“ (Z. 1–172, 17 279 B, md5 `e0813faa8cbaf293fc8848e034edb1aa`; Z. 178 der Datei im Repo trägt eine Stelle nach 27.5). Stand der Ablage: in der Antwort des Chats.
- **Zwei Fragen:** (1) Ist die Zeile ohne Kurs von `APH` am 2026-09-01 ein „Endet eine Reihe früher“ nach R72 (d), und was ist dann vor dem Tag zu entscheiden, von wem? (2) Bestätigt Fable die Lesarten L1–L9, und in welcher Form kommt das Ergebnis ins Register (Blöcke ab R78, Marke an den Zeilen „R74 (54.1) (e)“ in 54.5 und „R72 (53.7) (d)“ in 53.9, Stand von 53.10 Nr. 3 und Nr. 10 und 54.6 Nr. 1 und Nr. 8)? Dazu fünf Punkte zur Kenntnis (K1–K5).
- **Vorprüfung** (Helfer, `logs/steuernder_chat/TB-139_vorpruefung_06a.md`): Weder das Register noch das Manifest kennen den Fall. Das Manifest führt 36 zugelassene Befunde, alle `rand_erste`, keinen an einer Aktien-Datei; R13 (b) (46.4, Z. 10480) führt für die 150 Aktien-Dateien den 2026-09-01 als letzte Kerze und spricht nicht von einer Zeile ohne Kurs; R72 (d) stellt das Reihenende nicht unter den Zeitraum nach R66 (a).
- **Gegenlesen** (frischer Helfer, `logs/steuernder_chat/TB-139_gegenlesen_06a.md`): 81 Stellen an der Quelle, sieben Fehler und acht Lücken, alle berichtigt; kein Verstoss gegen 27.1. Die Berichtigungen hat kein weiterer Leser geprüft. Die zwei Absätze „Neigung“ stammen vom steuernden Chat.
- **Erinnerungsdateien gegen 27.1** (Helfer, 21:18): je 0 Treffer in den vier Dateien; Grössen laut Liste 9 461, 2 765, 385 und 673 B (der Lesekopf nennt für die zwei Projektdateien 9 440 und 2 723 B). In diesem Chat wurde keine Erinnerungsdatei geändert.
- **Eigene Zählung, neu:** In den 24 Krypto-`_1d`-Reihen des Snapshots fehlt `close` in keiner Zeile (20:16).
- **Wartezustand:** Der Betreiber eröffnet einen neuen Fable-Chat und fügt Eröffnung und Anfrage ein. Fables Antwort kommt nach `projektfuehrung/FABLE_ANTWORT_2026-10-06a_<stichwort>.md`. Danach: Antwort bewerten (nicht in dem Chat, der den Registerauftrag baut), Registerauftrag bauen, Einzelfreigabe per Karte. Geht die Anfrage erst an einem späteren Tag hinaus, ändern sich Datum, Titel und Dateiname.
- **Unverändert offen:** TB-137 (Abnahme), die zweite Fable-Anfrage (54.6 Nr. 2, 6, 7, 9), der Regelwerk-Nachtrag, Backlog und Journal zur Abnahme TB-138, `BACKLOG.md` in der Ablage.
- **Ampel:** 316 395 (20:19) · 345 974 (21:01); der Stand danach steht in der Antwort des Chats.

## Umzug 07.10.2026, 06:59 — Stand für den neuen steuernden Chat (selbsttragend, alle neun Blöcke)

Betreiber, 07.10.2026, 06:57: „jetzt Hauptchat auch umziehen. Fable läuft.“ Ampel 06:58: Verlauf 450 461 (Grundlast 128 903), rot. **Dieser Block ersetzt den Umzugsblock vom 06.10.2026, 16:40;** die Nachträge vom 06.10.2026 (20:18, 21:00, 21:30) tragen die Einzelheiten und sind nur bei Bedarf zu lesen.

### Block 1 — Stand in drei Zeilen

- **TB-138 ist abgenommen** (06.10.2026; zehn Prüfungen eines Helfers, drei formale Abweichungen, keine gegen einen Messwert), die Sitzung ist geschlossen. Ins Register ist davon nichts eingetragen.
- **Die Anfrage 06.10.a liegt beim Verfahrensprüfer:** ein neuer Fable-Chat arbeitet daran (Betreiber, 07.10.2026, 06:57: „Fable läuft“; wann sie abgeschickt wurde, ist nicht gemessen). Die Antwort steht aus; im Repo liegt keine `FABLE_ANTWORT_2026-10-06…` oder `…-07…` (gemessen 06:58).
- **Danach kommt ein Registerauftrag** (Bauart TB-136), der Fables Blöcke und die Tatsachennotizen zu TB-138 zusammen einträgt. TB-137 steht weiter aus.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` = `8d172c0` (TB-138 D3, 06.10.2026, 16:05:05). Gemessen 07.10.2026, 06:58, ohne `git status` und ohne `git diff`: geändert nur `docs/projektfuehrung/UEBERGABE.md` (diese Datei); unverfolgt `docs/projektfuehrung/FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md` und `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-06_eroeffnung.md`; keine `index.lock`. Der nächste Mac-Auftrag nimmt alle drei in Schritt 0 mit; sein 0a muss diese drei Einträge und den Auftrag selbst erwarten.

**Keine Sitzung läuft:** Schliess-Auslöser 06.10.2026, 20:17 („1 Sitzung(en) mit TERM beendet, 0 noch da“); Wächter-Sonde `starte_TB-99` am 07.10.2026, 04:58:27Z: kein Abbruch wegen einer laufenden Sitzung, Schlüsselbund entsperrt, Abbruch erst am Zeiger (TB-99 ist kein Auftrag). `AKTUELLER_AUFTRAG.md` zeigt auf TB-138 (md5 `665f314bd9cfb9c00c72ecb606804807`); `letzter_satz.txt` trägt den Satz zu TB-138; kein Auftrag ist startklar.

### Block 3 — Tragende Zahlen

- **Register:** unverändert, 11 581 Zeilen, sha256 beginnt `8d505a38ad3abc93` (gemessen 06:58), Stand `9b7b060`. Höchster Block R77; Fable vergibt ab R78. Sollwert `herkunft.register()` nach TB-136: `cfff54ca81d3dbf594a28880b17d4ba8389e0436c2d48cd50248586c1de03a81` (ERGEBNIS_TB-136 Z. 81; seither nicht gemessen).
- **TB-138:** Auftrag `docs/auftraege/MAC_TB-138_verfahrensmessung_snapshot.md` · Ergebnis `docs/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md` (18 100 B, 181 Zeilen; Z. 178 trägt eine Stelle nach 27.5) · Belege `docs/belege/TB-138/`. Kernzahlen, vom steuernden Chat nachgerechnet (nur Datumsspalte und ob `close` fehlt): Aktien 150 Reihen, 16 275 Kurstage 1962-01-02 bis 2026-09-01; früher endend nur `APH` (letzter Kurs 2026-08-31, am 2026-09-01 eine Zeile ohne Kurs); zwei Lücken (`LMT` 1974-06-03, `MNST` 2026-08-10); Krypto 24 Reihen ohne Befund. Nicht nachgerechnet: der Vergleich mit dem Kalender „NYSE“ in der Lock-Umgebung (0/0, nur Ausgabe der Sitzung).
- **Anfrage 06.10.a:** `FABLE_ANFRAGE_2026-10-06a_verfahrensmessung_snapshot_aph.md` (11 681 B, md5 `06ae4b76831d547cff57b2d2ce425dfb`) und `FABLE_UEBERGABE_2026-10-06_eroeffnung.md` (7 295 B, md5 `6e9fa10d1e7ae7c733ad1d889c6e81d4`), beide im Repo (unverfolgt) und in der Ablage. Zwei Fragen: (1) Ist die Zeile ohne Kurs von `APH` ein „Endet eine Reihe früher“ nach R72 (d), und was ist dann vor dem Tag zu entscheiden, von wem? (2) Gelten die Lesarten L1–L9, und in welcher Form kommt das Ergebnis ins Register (Blöcke ab R78, Marke an den Zeilen „R74 (54.1) (e)“ in 54.5 und „R72 (53.7) (d)“ in 53.9, Stand von 53.10 Nr. 3 und Nr. 10 und 54.6 Nr. 1 und Nr. 8)? Dazu K1–K5 zur Kenntnis. Die Antwort wird als `projektfuehrung/FABLE_ANTWORT_2026-10-06a_<stichwort>.md` erwartet.
- **Regeldateien:** `ARBEITSWEISE.md` 2 413 Zeilen (156 926 B, md5 `e85163e98db7f0b9387f4c990b67f8ca`; Abschnitt 0: 25 681 B) · `UMZUG.md` 380 Zeilen (26 923 B; Abschnitt 3: 5 897 B) · `BACKLOG.md` 323 Zeilen (73 765 B, md5 `5721615ef4d59f600018e08d681fc5c8`). Journal: Block EG steht, nächste Kennung EH.
- **Ablage:** 99 Einträge (06.10.2026, 21:31): neu die zwei Fable-Dateien und `projektfuehrung/ERGEBNIS_TB-138_verfahrensmessung_snapshot.md` (nur Z. 1–172, 17 279 B). `UEBERGABE.md` mit diesem Block: Stand in der Antwort des Chats. `BACKLOG.md` in der Ablage trägt noch den Stand vor TB-138.
- **Projekt-Erinnerung:** vier Dateien am 06.10.2026, 21:18, gegen 27.1 gemessen, je 0 Treffer (Grössen laut Liste 9 461, 2 765, 385, 673 B); in diesem Chat nicht geändert. Vor der nächsten Eröffnung für Fable neu messen.
- **Nummern:** TB-139 ist nicht vergeben und für den Registerauftrag nach Fables Antwort vorgesehen; der Regelwerk-Nachtrag bekommt die Nummer danach (Vorgabe des steuernden Chats). Journal ab EH. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Tages, an dem sie hinausgeht.

### Block 4 — Offene Punkte, in Reihenfolge

1. **Fables Antwort 06.10.a übernehmen und bewerten,** sobald der Betreiber „Fable ist fertig“ meldet: über `project_info` finden, ins Repo übertragen (md5 beidseitig), Blöcke und Nummern am Block zählen, jede Zahl an der Quelle nachrechnen, Backlog- und Journal-Nachtrag vormerken (5b). **Die Entscheidung zu `APH` dem Betreiber vorlegen** (Frage 1 (b): das Register sagt nicht, wer entscheidet).
2. **Registerauftrag (TB-139), Bauart TB-136:** Fables Blöcke ab R78 als Abschnitt 55, dazu „Voraussetzungen und Befunde“ und „Was offen bleibt“ des steuernden Chats, Marken nach Fables Antwort. Bestandsaufnahme liegt vor: `logs/steuernder_chat/TB-139_bestand_A1.md` (Gliederung, Daten-Block, Skripte, Schritt C, Sollwerte von TB-136) und `TB-139_bestand_A2.md` (Vorbilder, Markenregeln). Zu beachten: T4 der Registerkopie hat 5 409 B Luft bis 240 000; Prüf- und Einfügeskript stehen an festen Stellen auf TB-136. **Einzelfreigabe des Betreibers per Karte.** Der Chat, der die Antwort bewertet, baut den Auftrag nicht auch (ARBEITSWEISE 0).
3. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt (bis rund 120 000 Zeichen; danach sofort die Ampel messen). Helferauftrag `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilennummern gelten am Stand `d781f1b`. Die Pakete 8 und 12 gegen Auftrag und Ergebnis TB-138 halten.
4. **Zweite Anfrage an Fable** (54.6 Nr. 2 und Nr. 6 als Fragen, Nr. 7 und Nr. 9 zur Kenntnis): `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md`; wartet auf die Pakete 3, 5 und 11 von TB-137.
5. **Regelwerk-Nachtrag** (nach TB-137): wie Umzugsblock 06.10.2026, 13:43, Block 4 Nr. 4; dazu die Regeln aus Block 7 hier, aus Block 7 des Umzugsblocks 16:40 und aus den Nachträgen 14:25 und 21:00.
6. **Backlog und Journal** zur Abnahme TB-138 und zur Anfrage 06.10.a: mit dem nächsten Mac-Auftrag (5b).
7. **Ablage:** `BACKLOG.md` erneuern (erst nach der 27.4-Prüfung), durch einen Helfer.
8. **`AKTUELLER_AUFTRAG.md`** beim Legen des nächsten Auftrags umstellen.

### Block 5 — Wartezustände

Der Fable-Chat arbeitet an 06.10.a; der Betreiber meldet „Fable ist fertig“. TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Keine Mac-Sitzung läuft, keine Karte ist offen, keine Nachschau ist geplant.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat (seit 16:40)

- 06.10.2026, 19:40: „TB138 fertig“ (zweite Meldung; der Stand war unverändert). 20:10: „weiter im backlog“ — der alte Chat hat daraufhin TB-138 selbst abgenommen.
- Karte nach der Ampel von 20:19 (rot): „Hier weiterbauen“. Karte nach dem Nachtrag 21:00: „Erst Fable, dann ein Eintrag (Empfohlen)“.
- 07.10.2026, 06:57: „jetzt Hauptchat auch umziehen. Fable läuft.“
- Vorgaben ohne Widerspruch: `eingaben.json` bleibt als Beleg von TB-47 (K5 der Anfrage); kein zweiter Snapshot vorgeschlagen (Neigung zu Frage 1); TB-139 für den Registerauftrag.
- **Keine Freigabe** für Register, Sperrliste, Signalpfad oder Parameterdateien. Die Freigabe zum Registerauftrag steht aus.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. Die Vorgabe „als Nächstes der Registereintrag“ (20:19) stand, bevor gemessen war, wie das Register Messergebnisse aufnimmt; die Karte „Hier weiterbauen“ fragte nach dem Ort für einen Bau, dessen Weg nicht feststand. ⇒ Vor einer Vorgabe zur Reihenfolge das Vorbild im Register messen lassen.
2. Der Eröffnungstext von 16:41 lag drei Stunden im Chat und war nach „weiter im backlog“ überholt (Abnahme, Sitzung, Ablage). ⇒ Arbeitet ein Chat nach dem Eröffnungstext weiter, kennzeichnet er den alten Text in derselben Antwort als überholt und gibt beim Umzug einen neuen aus.
3. Das Datum der Anfrage (06.10.a) steht in Titel und Dateiname; wann der Betreiber sie abgeschickt hat, ist nicht gemessen. Geht eine Anfrage erst am Folgetag hinaus, weicht das Datum von der Regel ab. ⇒ Beim Ausgeben einer Anfrage spät am Tag den Betreiber fragen, wann er sendet, oder das Datum offen lassen.
4. Die Eröffnung 06.10. trägt zwei unschöne Zeilenumbrüche (Abschnitt 2 und 3), weil das Skript Zeilen ersetzt hat, ohne neu zu umbrechen; der Inhalt stimmt. ⇒ Nach dem Ersetzen in umbrochenem Text die Zeilenlängen prüfen.
5. Ampel im roten Bereich: 316 395 (06.10., 20:19) · 345 974 (21:01) · 428 399 (21:32) · 450 461 (07.10., 06:58). Rund 82 000 kostete die Fable-Anfrage: der Sendetext (18 KB) wurde einmal gelesen und einmal als Kopierblock ausgegeben, dazu vier Helferberichte. ⇒ Eine Fable-Anfrage baut ein frischer Chat; der Kopierblock kommt aus einer Datei, die ein Skript gebaut hat, und wird nur einmal in den Chat geholt.
6. Was getragen hat: die Bestandsaufnahme vor dem Bau (zwei Helfer, getrennter Zuschnitt); die Vorprüfung durch einen Helfer, der den Entwurf gleich mitbaut; Berichtigungen per Skript mit `assert` auf genau einen Treffer; md5 beidseitig bei jeder Ablage.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert), neu seit 16:40: `TB-138_abnahme_helferbericht.md` · `TB-139_bestand_A1.md`, `TB-139_bestand_A2.md` · `TB-139_vorpruefung_06a.md`, `TB-139_gegenlesen_06a.md` · `ablage_06a/` mit dem gekürzten Ergebnis TB-138 und `FABLE_2026-10-06a_SENDETEXT.txt` (18 399 B, md5 `2a5064e789ccee6779d4b8a3c10b819d`). Dazu die Dateien aus dem Umzugsblock 16:40, Block 8. Nicht ohne Frage löschen.
- `HELFER_AUFTRAG_TB-138_abnahme.md` ist erledigt.
- Verfällt mit diesem Chat: die Ordner `tb138/`, `tb139/`, `tb138_abnahme/` und `kern/` in der Umgebung der Geräteanbindung (das Tragende ist nach `logs/steuernder_chat/` kopiert).

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, als erste Nachricht der Antwort auf „jetzt Hauptchat auch umziehen“. Kernlektüre für den neuen Chat: dieser Block bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

---

## Nachtrag 07.10.2026, 10:32 — Fable 06.10.a übernommen und bewertet; TB-140 (Messung) vor TB-139 (Registereintrag); Arbeitstag ohne Umzug

Betreiber, 07.10.2026, 08:10: „Ich bin heute den ganzen Tag unterwegs und arbeite nicht am Mac. Meine Arbeiten kann ich dennoch über die mobile App und Termius ausführen.“ · „Arbeite heute so viel wie möglich selbstständig ab, damit wir endlich wieder größere Fortschritte machen.“ · „Vermutlich können wir heute über den Tag hinweg dann auch keinen Umzug durchführen.“ · „Fable ist fertig.“

Die Abschnitte 1 bis 5 sind die Bewertung des steuernden Chats vom 07.10.2026 zur Antwort 06.10.a, übernommen per Skript aus `logs/steuernder_chat/BEWERTUNG_FABLE_2026-10-06a.md` (dort Abschnitte 1 bis 5; Abschnitt 7 dort ist hier Abschnitt 6). Die Abnahme machte ein Helfer, nur lesend; die Kernzahl hat der steuernde Chat selbst nachgezählt.

### 1. Übernahme
Ablage → Repo über zwei unabhängige Abschriften (zwei Helfer, `cmp` gleich): `docs/projektfuehrung/FABLE_ANTWORT_2026-10-06a_verfahrensmessung_snapshot_aph.md`, 26 689 B, 159 Zeilen, md5 `2fc513b93ef8b3ecb794a543c9fe5dc3`, beidseitig gemessen 07.10.2026. **Grenze:** Die Leerstelle in Zifferngruppen (Z. 3, 20, 21, 130, 132, 154 — Z. 154 ist der Block R79) ist als U+0020 geschrieben; ob die Ablage dort ein anderes Leerzeichen führt, zeigt `project_read` nicht.

### 2. Was Fable entschieden hat
- **APH (R78 (d)):** Reihenende nach R72 (d), war zu melden; berührt 3b (c) im Lauf nicht, weil der Tag ohne Kurs (2026-09-01) nach dem Ende der Bestätigungsperiode liegt. Snapshot bleibt, `benchmark.py` wird nicht geöffnet, die Zeile wird nicht ergänzt. Für den Betreiber bleibt keine Wahl ausser der Einzelfreigabe des Eintrags.
- **Wer entscheidet (R78 (f)):** der Verfahrensprüfer durch Block vor dem signierten Tag; Änderungen an Snapshot, Lock oder Sperrlisten-Code daneben mit Freigabe des Betreibers.
- **L1–L9 bestätigt**, L2 und L6 mit Voraussetzung. Drei Blöcke R78 (a)–(g), R79 (a)–(g), R80 (a)–(c).
- **Sechs Voraussetzungen:** vor dem Eintrag R79 (a), R79 (b); vor dem signierten Tag R78 (d); ohne Zeitpunkt R78 (a), R78 (e), R79 (g).

### 3. Abnahme
Helfer (nur lesend, 30 Schritte): `logs/steuernder_chat/FABLE_06a_abnahme_helferbericht.md`. Geprüft: 52 Verweise, 26 Zitate, 28 Aussagen über das Register, 34 Zahlen, 16 Markenorte. **Keine Abweichung gegen einen Messwert in einem Block.**
Eigene Nachzählung des steuernden Chats am Snapshot `63e4b6c8…` (awk über 174 `*_1d.csv`, 07.10.2026): `close` fehlt in genau einer Zeile (`APH` 2026-09-01); 150 Dateien enden 2026-09-01, 24 enden 2026-09-14; `XAUTUSDT` nur als `_1h.csv`. Nicht nachgerechnet: Kalendervergleich, doppelte `open_time`, Paketfassungen (Ausgabe der Sitzung TB-138).

### 4. Abweichungen und Befunde (gehen in „Voraussetzungen und Befunde“, TB-139)
1. Der Kopf von R78 nennt R74 (e) nicht; R78 (f) gibt R74 (e) eine Lesart, R80 (a) setzt dafür die Marke an 54.1.
2. R78 „Quelle des Grundes“ zitiert „Nicht gemessen: Zeilen ohne close“; im Register steht `close` in Backticks.
3. R79 (c) „in den 24 Krypto-Tagesreihen in keiner“: im Ergebnis TB-138 „nicht gemessen“; Quelle war die Zählung des steuernden Chats (Anfrage). Bekommt in TB-140 einen Beleg (Zusatz Z1).
4. R79 (f) führt die Herkunft von 5.4.0 als Tatsache; die Anfrage nannte sie „erschlossen“. TB-140 liest die Stelle in `docs/ERGEBNIS_TB-47_snapshotgrenze.md` (Zusatz Z2).
5. R79 (g) „dreizehnter Fall“: rechnerisch richtig (zwölf nach R76 (e)); R76 (e) zählt Aussagen „über Repo oder Register“, R79 (g) spricht vom Bestand. Lesart des steuernden Chats, vorläufig: der Snapshot liegt im Repo, also zählt es; zur Kenntnis an Fable.
6. Nur im Antworttext, nicht im Block: „vierzehn Tage“ bei Krypto ist gerechnet, nicht aus „Für Fable“ Nr. 3; L9 sagt, Stundenreihen enden nicht früher — `XAUTUSDT_1h` endet früher (R79 (c) sagt es richtig); „am Tagesschluss“ steht in R48 (d) bei der Exposure.
7. R56 (b): Eröffnung, Anfrage und Antwort 06.10.a sind am HEAD `8d172c0` nicht in git; Schritt 0 von TB-140 committet sie — vor dem Eintrag.
8. Vorbild 25.2 trägt die Marke unter dem berichtigten Satz, kein Blockzitat (Handwerk für TB-139).

### 5. Orte ohne Marke in R80 (a) — der steuernde Chat bestimmt seine Marken in TB-139 (R65 (a))
53.9-Zeile ohne R78 (g) · 54.5-Zeile ohne R79 (f) · 46.4 für R13 (a) · 48.1, 48.2, 48.7 zu R78 (e) · in R80 (b) nicht genannt: 17.0, R37, R48, R53, R75. Erst nennen, wenn die Markentabelle gemessen ist.


### 6. Nicht gemessen
Fables Selbstauskünfte (Ampel, Leseprotokoll-Zahlen); 37.3, 34, 5.2, 2a, 24b A2; `gegenprobe.txt`, `c3_vergleich.txt` der Belege TB-138.

### 7. Vorgaben des steuernden Chats vom 07.10.2026 (gelten, wenn der Betreiber nicht widerspricht)

- **TB-140 ist die „Verfahrensmessung 2“,** nur lesend, auf dem Mac: Sie misst die sechs Voraussetzungen aus R78 und R79 und zwei Belege zu R79 (c) und R79 (f) (Z1: `close` je Tagesreihe des Snapshots; Z2: Herkunft von „5.4.0“ in `docs/ERGEBNIS_TB-47_snapshotgrenze.md`). **Teil 1 vor Teil 2:** Teil 1 = R79 (a), R79 (b), R79 (g), Z1, Z2 (darauf wartet der Eintrag); Teil 2 = R78 (a), R78 (d), R78 (e) durch Lesen des Codes. Freigabe: Handwerk ohne Sperrlistennähe, pauschal frei (Betreiberentscheid 26.09.2026); der Betreiber startet durch Absenden des Satzes. Auftrag: `docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md`.
- **TB-140 läuft vor TB-139.** Grund: R79 (a) und R79 (b) verlangen ihre Messung „vor dem Eintrag“, und sie laufen nur in `trading-env` auf dem Mac.
- **Nummern (berichtigt den Umzugsblock 06:59, Block 3):** TB-139 bleibt der Registerauftrag und trägt genau die Blöcke R78 bis R80 als Abschnitt 55, dazu „Voraussetzungen und Befunde“ und „Was offen bleibt“ des steuernden Chats. TB-140 ist die Messung. Der Regelwerk-Nachtrag bekommt die Nummer danach.
- **Die Einzelfreigabe des Betreibers für den Registereintrag steht aus** (Karte, mit dem fertigen Auftrag). **TB-137 steht weiter aus.**
- **TB-139 baut heute ein Helfer mit eigenem Kontext, kein neuer Chat.** Das weicht von ARBEITSWEISE 0 ab („Der Chat, der eine Fable-Antwort bewertet, baut nicht auch den Registerauftrag“); Grund: Heute ist kein Umzug möglich (Betreiber 08:10). Der Zweck der Regel bleibt gewahrt, weil der Bau nicht im Verlauf des steuernden Chats liegt.
- **Der Auslöser wird erst gelegt,** wenn der gegengelesene Auftrag, der Zeiger und dieser Nachtrag im Arbeitsbaum liegen. Der Betreiber schickt den Satz von unterwegs ab (Claude-App, Gerätesitzung, oder Termius).
- **Die Antwort 06.10.a liegt seit dem 07.10.2026 im Repo** (unverfolgt, md5 `2fc513b93ef8b3ecb794a543c9fe5dc3`, 26 689 B); Schritt 0 von TB-140 committet sie zusammen mit Anfrage und Eröffnung (R56 (b)).

### 8. Fehler dieses Chats (ohne Nummer) und was getragen hat

1. Die Zwischenmeldung an den Betreiber (08:43) nannte die acht Punkte aus Abschnitt 4 „formale Befunde“. Zwei davon (Nr. 3 und Nr. 4) sind Aussagen in einem Block ohne Beleg; dafür misst TB-140 Z1 und Z2. ⇒ Ein Sammelwort für Befunde erst wählen, wenn jeder Befund einzeln eingeordnet ist.
2. Eine Schnellprüfung „Lock gegen `dist-info`“ mit awk über die Geräteanbindung trug nicht (Lesefehler an mehrzeiligen Metadaten bei fünf Paketen); tragfähig daraus ist nur: 67 Zeilen `name==version` im Lock, 67 `dist-info` in `trading-env`. Die Messung macht TB-140 (R79 (a)).
3. Getragen hat: zwei unabhängige Abschriften mit `cmp` für die Übernahme aus der Ablage; Bestand und Entwurf in einem Helfer, danach zwei frische Gegenleser mit getrenntem Zeilenbereich.

### 9. Setzungen im Auftrag TB-140 (Lesarten des steuernden Chats, vorläufig)

- **N7:** „`benchmark.py` wird nicht geöffnet“ (R72 (d), R78 (d)) heisst im Auftrag: nicht geändert, nicht importiert, nicht ausgeführt. Gelesen wird die Datei, weil die Klammer zu R78 (d) das Lesen des Codes verlangt.
- **Z2** kennt drei Urteile: „belegt (Wortlaut)“, „nur erschliessbar“, „nicht gefunden“; die Abgrenzung steht im Auftrag bei Z2.
- **Ziele der Befunde (Schritt D des Auftrags), wo die Klammer kein Ziel und keinen Zeitpunkt nennt:** V1 (Spalte, Datei und Ordner je Lesestelle) geht unter „Für Fable“ und als Tatsache in „Voraussetzungen und Befunde“ des Registerauftrags. V2 (a) (behält oder verwirft, je Stelle) geht mit V2 (b): bei einem Befund dort an den Verfahrensprüfer, sonst als Tatsachennotiz an den steuernden Chat. V3 (ii) geht als Tatsache an den steuernden Chat (für den Bau des Zellen-Erzeugers) und unter „Für Fable“ zur Kenntnis; ob die Prüfung genügt, entscheidet der Verfahrensprüfer. V3 (i) wird vor dem signierten Tag gemessen.
- **Urteile:** rc 0 = erfüllt, rc 1 = nicht erfüllt, rc 2 = nicht messbar. V1 trägt kein „erfüllt“ für den Kern eines künftigen Zellen-Erzeugers, weil es den Erzeuger als Code nicht gibt (`docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md`); gemessen wird am vorhandenen Kern.
- **Bau:** Entwurf und Bestand ein Helfer, drei Gegenleserunden frischer Helfer (zwei mit getrenntem Zeilenbereich, eine über die Änderungen); die Skizzen liefen in der Linux-Umgebung der Geräteanbindung, nicht in `trading-env` und nicht unter macOS. Unterlagen: `logs/steuernder_chat/TB-140_*`.

---

## Nachtrag 07.10.2026, 11:36 — TB-140 abgenommen; V2 (b): „ein solcher Wert wird gebildet“; TB-139 als Entwurf v1; zwei Fragen beim Betreiber

**TB-140** lief 10:45 bis 11:08 (Betreiber 11:20: „Tb140 fertig“): sieben Commits `8127f7f` (Schritt 0, darin Anfrage, Eröffnung und Antwort 06.10.a — R56 (b) erfüllt) bis `b07ec7d` = `origin/main` (lokaler Zeiger); Arbeitsbaum sauber. Ergebnis `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md` (78 246 B), Belege `docs/belege/TB-140/`.

| | Urteil der Sitzung | Kern |
|---|---|---|
| V4 = R79 (a) | erfüllt | 67 von 67 Paketen des Locks, Interpreter und Plattform gleich |
| V5 = R79 (b) | erfüllt | eigener Aufruf je Aktien-Bot: 2 428 / 2 177 / 2 428 / 2 177 Tage, 0 Abweichungen |
| V6 = R79 (g) | erfüllt | Stand `0779453`: `APH` 2026-09-01 ohne `close`; der dreizehnte Fall zählt |
| Z1 (R79 (c)) | erfüllt | Aktien 150 Reihen, 1 Zeile ohne `close`; Krypto 24 Reihen, 0 |
| Z2 (R79 (f)) | „nur erschliessbar“ | `ERGEBNIS_TB-47` verbindet 5.4.0 nicht mit `eingaben.json`/Feld `kalender` |
| V1 = R78 (a) | wie die Klammer; Kern des Erzeugers nicht messbar | kein Zellen-Erzeuger als Code; `tagesschluss` liest `close` aus `paths.DATA_DIR`, der Kern aus `data/` (O7: Ordner, nicht Snapshot) |
| V2 (a) = R78 (d) | verwirft, alle fünf Stellen | Zeilen ohne `close` werden gestrichen |
| **V2 (b) = R78 (d)** | **„ein solcher Wert wird gebildet“** | Aufnahme eines Symbols aus der ganzen Datei (alle neun Lader); frühester Einstieg der vier Aktien-Lader aus `max(open_time)`; Schlüssel der Stufe 4 der Zuteilung aus Ausstiegswerten; Krypto-Einstiege bis Dateiende 2026-09-14. Jeder Codeschritt gedeckt; dass es in eine Ausgabe nach R39 eingeht, ist erschlossen |
| V3 (i), (ii) = R78 (e) | 14 Zeilen, 7 „sagt nichts“; „trifft teils zu“ | `auswertung.py` endet mit 2 nur bei NaN in `netto_sharpe`; ±inf ungeprüft |

**Abnahme** (Helfer, nur lesend, 33 Schritte; `logs/steuernder_chat/TB-140_abnahme_helferbericht.md`): Commits im erlaubten Bereich, keine Code-, Daten-, Register- oder Parameterdatei berührt; 109 Einzelwerte, 291 Fundstellen, E1 und J1 bytegleich. Abweichungen: „git 2.39.5“ (Ergebnis Z. 90) ohne Beleg; `v4.txt` vergleicht den Lock-Kopf mit der Umgebung, die Plattform gegen das Register nur über den Lock-Hash (Register Z. 3234 gleichlautend, vom Helfer gelesen); vier ungenaue Zeilenzuordnungen (Pfadzeile statt `read_csv`); „In einfacher Sprache“ Z. 446–447 („schneiden nirgends ab“) trägt V2 (b) nicht — `benchmark.py:280/290` und `faltenplan.py:312/326` begrenzen am Schnitt; die Sitzung nennt selbst einen Sichtschutz-Vorfall bei einem ihrer Helfer (Ergebnis Z. 427–431). Vom steuernden Chat selbst gezählt: Z1 (awk, gleich), 67 Lock-Zeilen. Nicht nachgerechnet: V4 und V5 nur an der Rohausgabe (V5 lief im Bau mit den Lock-Fassungen in der Linux-Umgebung: 16 275 / 2 428 / 2 177).

**Folge aus V2 (b):** Nach R78 (d) kommt die Frage vor dem Tag an den Verfahrensprüfer, und (d) wird neu entschieden. Ob davor oder danach eingetragen wird, liegt beim Betreiber (Karte in der Antwort zu „Tb140 fertig“).

**TB-139, Entwurf v1** (Helfer, 119 Schritte): `logs/steuernder_chat/2026-10-07_tb139_bau.tar.gz`, darin `tb139/bau/MAC_TB-139_entwurf_v1.md` (143 554 B, md5 `acba64ce6a9d2a851685168410776723`), `tb140_fuellung.md` (Werte zu den 47 Platzhaltern `<<TB-140: …>>`), `marken_tabelle.md`, `baubericht.md`, `sim/`. Abschnitt 55: 55.1–55.3 = R78–R80, 55.4 Voraussetzungen und Befunde, 55.5 Was offen bleibt. Simulation an Kopie: 11 581 → 11 679 Zeilen, 11 Marken Fables an 8 Orten, Prüfskript rc 0, Gegenprobe beisst. T4 behält 4 135 B Luft. **Offen:** vier `<<ENTSCHEID>>` (Form der Marke an der 53.9-Zeile; welche der sieben Markenkandidaten K1–K7, Vorschlag des Helfers nur K5 = 48.2; Dateien der Vormessung; Dialog-Index), `<<FREIGABE>>`, Skripte für A5, B, C, D nicht gebaut, **nicht gegengelesen**.

**Keine Sitzung läuft** (Schliess-Auslöser 11:36, siehe Wächter-Protokoll). `AKTUELLER_AUFTRAG.md` zeigt auf TB-140. Backlog- und Journal-Nachtrag zur Abnahme TB-140: mit dem nächsten Mac-Auftrag (5b). Nummern: nächster Mac-Auftrag nach TB-139 ist TB-141; Journal ab EI; Fable vergibt ab R81.

---

## Nachtrag 07.10.2026, 15:59 — Betreiberentscheide per Karte; Fable-Anfrage 07.10.a im Bau; Befund an der Projekt-Erinnerung

**Karte, beantwortet 07.10.2026, 14:55** (gestellt 11:37 nach der Zustellung von Ergebnis, Aufgaben und Ampel):
- Reihenfolge des Registereintrags: **„Erst Fable, dann ein Eintrag (Empfohlen)“** — heute geht eine neue Fable-Anfrage zum Befund V2 (b) hinaus; R78 bis R80 und was Fable darauf liefert, kommen zusammen als Abschnitt 55 ins Register. TB-139 bleibt Entwurf v1 und wird nach Fables Antwort nachgezogen.
- Umzug: **„Heute Abend am Mac (Empfohlen)“** — der steuernde Chat arbeitet weiter und schreibt Umzugsblock und Eröffnungstext, sobald der Betreiber meldet, dass er am Mac ist. Ampel bei der Frage: gelb, Verlauf 225 223 (11:36); um 15:58: Verlauf 258 805.

**Fable-Anfrage 07.10.a** (neuer Fable-Chat; der letzte endete rot, 412 650): fünf Fragen — (1) R78 (d) neu nach V2 (b), (2) R78 (e) nach V3, (3) Form des einen Eintrags (Blöcke berichtigt, bevor sie eingetragen sind), (4) R79 (f) nach Z2, (5) R78 (a) und der Ordner (V1, O7) — dazu K1 ff. Vorprüfung und Entwurf ein Helfer (129 Schritte), Gegenlesen ein frischer Helfer (rund 350 Stellen, 8 Fehler, 6 Lücken; Sichtschutz 27.1: kein Treffer mit Wert in Anfrage, Eröffnung, Sendetext und der Ablage-Fassung des Ergebnisses TB-140). Unterlagen nach dem Ablegen unter `logs/steuernder_chat/FABLE_07a_*`. Aus der Vorprüfung: Die Untergrenze aus der letzten Zeile regelt das Register schon (26.2, 28.4; Code-Umstellung nach 28.5/R44 offen, TB-30b Posten 4); zu Zufallsschlüssel und Ausstieg am Ende der Spanne fand die Vorprüfung keinen Registersatz.

**Nachtrag zur Abnahme TB-140:** `docs/ERGEBNIS_TB-140…` Z. 235 trifft nicht — die `_1h`- und `_4h`-Reihen enden am 2026-09-15 (Vorprüfung, an der Zeitspalte gezählt; Register 31.5).

**Befund an der Erinnerung (Messung eines Helfers, 15:5x, nur gelesen, nichts geändert; `logs/steuernder_chat/FABLE_07a_erinnerung_messung.md`):** Die vier Dateien der letzten Messung (Projekt `preferences.md` 9 461 B, Projekt `ways-of-working.md` 2 765 B, `/profile.md` 385 B, `/preferences.md` 673 B) tragen weiter je 0 Treffer mit Wert. **Vier weitere gelistete Dateien tragen Werte oder Ergebnisse** und waren von den bisherigen Messungen nicht erfasst: Projekt `overview.md` (10 852 B), Projekt `methodology-and-learnings.md` (7 158 B), `/areas/trading-agent-projekt.md` (5 975 B), Projekt `dashboard-roadmap.md` (3 338 B, Grenzfall). Ein Chat im Projekt bekommt sie als Liste mit Pfad und Beschreibung gezeigt und kann sie mit dem Erinnerungswerkzeug öffnen; was die Plattform einem Fable-Chat im Wortlaut lädt, ist nicht messbar. ⇒ Die Eröffnung 07.10. nennt diese vier Dateien als nicht zu öffnen. Ob sie bereinigt oder gelöscht werden, entscheidet der Betreiber; der steuernde Chat hat nichts geändert. Zur Kenntnis an Fable.

**Zusatz 16:21 zum Nachtrag 15:59:** Die Anfrage 07.10.a liegt im Repo (unverfolgt): `FABLE_ANFRAGE_2026-10-07a_go_live_schnitt_voraussetzungen.md` (27 939 B, md5 `dfe819837d507aee48051567998d1d63`) und `FABLE_UEBERGABE_2026-10-07_eroeffnung.md` (7 796 B, md5 `df96bf552778f7a62836dd2c8c9209ba`); Sendetext `logs/steuernder_chat/ablage_07a/FABLE_2026-10-07a_SENDETEXT.txt` (34 882 B, md5 `ffb620d0aa654c5cd0ad793d75b26701`). Berichtigung v2 nach dem Gegenlesen (21 von 24 Befunden ganz, 2 teilweise, 1 nicht; die Berichtigungen sind nicht erneut gegengelesen). Erwartet: `projektfuehrung/FABLE_ANTWORT_2026-10-07a_<stichwort>.md`, Blöcke ab R81 oder R78–R80 in letzter Fassung (Frage 3). **Berichtigung zum Nachtrag 15:59:** Die Eröffnung sperrt nach R56 (d) schon alle nicht genannten Erinnerungsdateien; die vier Dateien mit Werten standen also bereits unter der Sperre. Neu ist nur, dass sie jetzt gemessen und in der Eröffnung beim Namen genannt sind. Der nächste Mac-Auftrag erwartet in 0a: geändert `UEBERGABE.md`, unverfolgt diese zwei Fable-Dateien (und die Antwort, sobald sie übertragen ist), dazu Zeiger und Auftrag.

---

## Nachtrag 07.10.2026, 18:11 — Fable 07.10.a übernommen und abgenommen; TB-139 als Entwurf v2 (sechs Blöcke); Stand vor dem Umzug

**Betreiber, 07.10.2026, 17:02:** „Die Fable Verfahrensprüfung ist fertig“. **Übernahme:** `projektfuehrung/FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md` aus der Ablage über zwei unabhängige Abschriften (zwei Helfer, `cmp` gleich) ins Repo, unverfolgt: 57 165 B, 244 Zeilen, md5 `388187e2a69218fbe5077e3f0bc1815f`, beidseitig gemessen 17:08. Grenze wie bei 06.10.a: Leerstellen in Zifferngruppen als U+0020; „−inf“ (Z. 227, 242) als U+2212.

**Was Fable entschieden hat** (Antwort „Kurz“, Z. 188–200; ein Eintrag aus EINER Quelldatei: R78–R80 unter ihrer Nummer in letzter Fassung, sie ersetzen die Fassung 06.10.a vollständig; R81–R83 neu):
- Frage 1: Der Befund aus TB-140 war zu melden. Die Entscheidung zu `APH` bleibt, ohne Bedingung (R78 (c), (d)). Für alle neun Bots geht keine Zeile ab dem Go-Live-Schnitt in einen Wert des Laufs ein (5.2); **geschnitten wird im Zellen-Erzeuger**, nicht im Snapshot und nicht in gesperrtem Code; dazu Wache und Abnahme (R81 (b), (c), (g), (h)). Kein Trade ab dem Schnitt; am Ende der Spanne gilt die Konvention des Codes am Datenende (R81 (e), (f); R83 (c)).
- Frage 2: Die Wache nach R78 (e) gilt, der Erzeuger baut sie. Nullzeile 0; Haltedauer „nicht definiert“; eine leere Tagemenge ist ein Befund und vorher zu messen (R82).
- Frage 3: dieselbe Nummer, letzte Fassung, alle drei neu; R80 bleibt Marken-Block (R80 (d)). Frage 4: R79 (f) neu gefasst, vierzehnter gezählter Fall (R79 (g)). Frage 5: eine Datei gleichen Namens ausserhalb des Snapshots ist eine andere Reihe; Benchmark erfüllt, Kern mit der Abnahme (R78 (a), R83 (e)).
- Fables Ampel: rot, geschätzt rund 540 000; die nächste Anfrage geht an einen neuen Fable-Chat.

**Abnahme** (Helfer, nur lesend, 25 Schritte; `logs/steuernder_chat/FABLE_07a_antwort_abnahme_helferbericht.md`): 128 Verweise, 92 Anführungen, rund 90 Angaben, 25 Markenorte geprüft. **Keine Abweichung gegen einen Messwert.** Kein Block übernimmt die drei Stellen, die die Abnahme TB-140 als abweichend führt. Befunde für „Voraussetzungen und Befunde“ (55.7), noch nicht eingesetzt:
1. Kopf von R83 nennt „Voraussetzungen in R78 (a), (d) und (e)“; in der neuen Fassung trägt nur (a) eine Klammer.
2. R83 (b), (f) und (c) führen drei Aussagen ohne den Stand „erschlossen“, den das Ergebnis TB-140 ihnen gibt (dort Z. 195, 229, 246).
3. R80 (c) „gemessen erfüllt“ für R79 (a): die Plattform ist nur mittelbar über den Lock-Hash verglichen. R80 (c) „Offen“ nennt den Lese-Audit aus R78 (a) nicht.
4. R80 (a) führt weiter „Vorbild 25.2 … Blockzitat“; Register Z. 4676 ist kein Blockzitat.
5. R78 (a) „Lese-Audit (41.2 B4, Teil (b))“ — B4 (b) heisst „Leseprotokoll“. R83 (d) verweist auf R49 (f) nur sinngemäss. R82 „Nullzeile 0 (R33, R36)“: in R36 per Mustersuche nicht gefunden (Teilmessung).
6. R79 (c) ist unverändert; der Beleg für die Krypto-Zeile (TB-140 Z1) steht nur in der Quelle von R83 und in K1.
7. Im Antworttext, nicht im Block: Z. 92 „zwei Test-Snapshots“ (R81 (h): drei), Z. 175 „zwei Voraussetzungen“ (R80 (c): drei), Z. 148 nennt die geänderte „Quelle“ von R79 nicht, Z. 216 Zitat ohne „(5.2)“, Z. 93/97 „Einzelfreigabe“ steht so nicht in 37.3.
8. Orte, die weder R80 (a) noch (b) führt: 48.4 (R36), 48.7 (R39), 48.17 (R49), 49.1 (R53), 17.0, 15.3; dazu 53.9-Zeile für R78 (g), 54.5-Zeile für R79 (f), 46.4 für R78 (b), 48.1/48.2 für R78 (e).
9. R56 (b): Anfrage, Eröffnung und Antwort 07.10.a sind nicht in git; Schritt 0 von TB-139 committet sie vor dem Eintrag.
Lesart des steuernden Chats, vorläufig: Keiner dieser Befunde verlangt eine Rückfrage vor dem Eintrag; sie stehen in 55.7 und gehen mit der nächsten Anfrage zur Kenntnis an Fable. Nicht gemessen: Code und Belege (Zahlen nur gegen die Ergebnisse, den Abnahmebericht und das Register).

**Was die neuen Blöcke verlangen** (P6 der Abnahme; gehört in 55.8 und in den Backlog): vor dem Eintrag R79 (a), (b) — gemessen erfüllt (TB-140 V4, V5); R79 (g) erfüllt (V6). Offen: R78 (a) Lese-Audit (Abnahme nach R46) und `close` ohne `open`/`high`/`low` (vor dem Tag); R81 (c) Menge am Tag-Commit (vor dem Tag); R81 (d) (mit Posten 4); R82 (c) leere Tagemengen (vor dem Tag). Zu bauen mit dem Zellen-Erzeuger: Schnitt R81 (b), Wachen R81 (c), (g), R78 (e), R82 (c), Felder R82 (a), (b); Abnahme R81 (h) mit drei Test-Snapshots. Freigabe des Betreibers nur, falls Snapshot, Lock oder gesperrter Code geändert würden (R78 (f); R81 (b) nur falls gewählt).

**TB-139, Entwurf v2** (Helfer, 146 Schritte, über alle Schritte an Kopien simuliert): `logs/steuernder_chat/2026-10-07_tb139_v2.tar.gz`, darin `v2/MAC_TB-139_entwurf_v2.md` (230 503 B, 2 723 Zeilen, md5 `9e3dca61dcfa20d3d4bb166ac89a15c9`), `baubericht_v2.md`, `marken_tabelle.md`, `aenderungen_v1_v2.md`, `sim/sim_bericht.txt`, `skripte/`, `bau.sh`. Vorgesehener Name im Repo: `docs/auftraege/MAC_TB-139_register_fable_07a.md`. Abschnitt 55: 55.0 Kopf (06.10.a „nie eingetragen“, wie Kopf 53), 55.1–55.6 = R78–R83, 55.7 Voraussetzungen und Befunde (18 Zeilen, TB-140 eingesetzt), 55.8 Was offen bleibt (14 Zeilen). 20 Marken an 14 Einfügestellen, 15 Orte aus R80 (a) (PRÄZISIERT 4, BERICHTIGT 1, ERGÄNZT 15). Simulation: 11 581 → 11 733 Zeilen, Prüfskript rc 0, Blöcke 6/6 zeichengleich, Gegenproben beissen; T4 behält 3 069 B Luft. **Acht Platzhalter:** `<<HEAD: b07ec7d oder später>>`, `<<FREIGABE>>`, `<<BEFUNDE-07a>>` (55.7; die neun Punkte oben), `<<BEFUNDE-07a-KURZ>>` (BACKLOG-Block), vier `<<ENTSCHEID>>`: E1 je Teil eine Marke (20, gebaut) oder je Block (25); E2 Marken des steuernden Chats (Vorschlag des Helfers: keine); E3 keine Vormessungsdatei, der Kopf nennt `UEBERGABE.md` am Commit von Schritt 0; E4 Handfelder des Dialog-Index für 06a und 07a. **Nicht getan:** Gegenlesen (zwei frische Helfer mit getrenntem Zeilenbereich), Trockenlauf des Prüfskripts am echten Repo, kein Programm des Repos gelaufen (0b-Werte aus TB-136), Einzelfreigabe des Betreibers.

**Nächste Schritte, in Reihenfolge (für den Chat nach dem Umzug):** (1) Platzhalter füllen und E1–E4 entscheiden (Handwerk), v3 bauen lassen; (2) gegenlesen lassen, berichtigen; (3) Karte „Einzelfreigabe Registereintrag“ mit dem fertigen Auftrag; (4) Auftrag, Zeiger und Nachtrag in den Arbeitsbaum, Auslöser, Betreiber schickt den Satz; (5) Abnahme, Ablage erneuern (Abschnitt 55, Index, Dialog-Index, `BACKLOG.md`); (6) TB-137 abnehmen, sobald das Gesamtergebnis da ist; (7) zweite Fable-Anfrage (54.6 Nr. 2, 6, 7, 9, 10) und der Regelwerk-Nachtrag (TB-141). Für den Zellen-Erzeuger entsteht aus R81/R82 ein eigener Bauauftrag (Backlog E-7/E-8).

**Stand der Dinge:** HEAD `b07ec7d` = `origin/main` (lokaler Zeiger); geändert nur `UEBERGABE.md`; unverfolgt die drei Fable-Dateien vom 07.10. (Anfrage, Eröffnung, Antwort); keine Sitzung läuft; `AKTUELLER_AUFTRAG.md` zeigt auf TB-140 (erledigt); kein Auftrag startklar. Nummern: TB-139 Registerauftrag, danach TB-141; Journal ab EI; Fable vergibt ab R84; Fehler ab 21. Umzug: per Karte „Heute Abend am Mac“; Umzugsblock und Eröffnungstext schreibt der steuernde Chat, sobald der Betreiber meldet, dass er am Mac ist. Ampel 16:22: rot, Verlauf 314 402.

---

## Umzug 07.10.2026, 19:45 — Stand für den neuen steuernden Chat (alle neun Blöcke; die Einzelheiten zu Fable 07.10.a und zu TB-139 trägt der Nachtrag 18:11 unmittelbar davor)

Betreiber: Karte, beantwortet 14:55: „Heute Abend am Mac (Empfohlen)“; 19:42: „bin am mac“. Ampel 19:43: Verlauf 388 272 (Grundlast 130 004), rot. **Dieser Block ersetzt den Umzugsblock vom 07.10.2026, 06:59.** Kernlektüre für den neuen Chat: ab „## Nachtrag 07.10.2026, 18:11“ bis Dateiende; die Nachträge 10:32, 11:36 und 15:59 nur bei Bedarf.

### Block 1 — Stand in drei Zeilen

- **TB-140 (Verfahrensmessung 2) ist gelaufen und abgenommen** (HEAD `b07ec7d`). Die zwei Messungen „vor dem Eintrag“ (R79 (a), (b)) sind erfüllt; der Befund V2 (b) ging mit der Anfrage 07.10.a an Fable.
- **Fable hat mit 07.10.a geantwortet:** sechs Blöcke aus einer Quelldatei (R78–R80 in letzter Fassung, R81–R83 neu); geschnitten wird im Zellen-Erzeuger. Die Antwort ist übernommen und abgenommen: keine Abweichung gegen einen Messwert, neun Befunde zur Form (Nachtrag 18:11).
- **TB-139 (Registereintrag, Abschnitt 55) liegt als Entwurf v2 vor,** an Kopien simuliert, acht Platzhalter, nicht gegengelesen; die Einzelfreigabe des Betreibers steht aus. Im Register steht weiter nichts aus TB-138, TB-140 und den zwei Antworten.

### Block 2 — HEAD und Arbeitsbaum

HEAD = `origin/main` (lokaler Zeiger) = `b07ec7d` (TB-140 D3, 07.10.2026, 11:08). Gemessen 19:43, ohne `git status` und ohne `git diff`: geändert nur `docs/projektfuehrung/UEBERGABE.md` (diese Datei); unverfolgt unter `docs/projektfuehrung/`: `FABLE_ANFRAGE_2026-10-07a_go_live_schnitt_voraussetzungen.md` (27 939 B, md5 `dfe819837d507aee48051567998d1d63`), `FABLE_UEBERGABE_2026-10-07_eroeffnung.md` (7 796 B, md5 `df96bf552778f7a62836dd2c8c9209ba`), `FABLE_ANTWORT_2026-10-07a_schnitt_im_erzeuger_wache_ein_eintrag.md` (57 165 B, md5 `388187e2a69218fbe5077e3f0bc1815f`); keine `index.lock`. **Keine Sitzung läuft** (Schliess-Auslöser 11:36: „1 Sitzung(en) mit TERM beendet, 0 noch da“; seither kein Eintrag im Wächter-Protokoll). `AKTUELLER_AUFTRAG.md` zeigt auf TB-140 (md5 `43826d550a9cf2e4828c5eaccce830df`), `letzter_satz.txt` trägt den Satz zu TB-140; kein Auftrag ist startklar. Der nächste Mac-Auftrag erwartet in 0a: geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`; unverfolgt die drei Fable-Dateien und sich selbst.

### Block 3 — Tragende Zahlen

- **Register:** unverändert, 11 581 Zeilen, sha256 beginnt `8d505a38ad3abc93` (gemessen 19:43), Stand `9b7b060`. Höchster eingetragener Block R77. Fable hat R78–R83 vergeben (nicht eingetragen); der nächste freie Block ist R84.
- **TB-140:** Auftrag `docs/auftraege/MAC_TB-140_verfahrensmessung_voraussetzungen.md` (159 021 B) · Ergebnis `docs/ERGEBNIS_TB-140_verfahrensmessung_voraussetzungen.md` (78 246 B) · Belege `docs/belege/TB-140/` · Commits `8127f7f` (Schritt 0, darin Anfrage, Eröffnung und Antwort 06.10.a) bis `b07ec7d`. Urteile und Abnahme: Nachtrag 11:36; dazu Nachtrag 15:59 (Ergebnis Z. 235 trifft nicht).
- **Fable 06.10.a:** committet, wird nie eingetragen (R80 (d) der Fassung 07.10.a; Vorbild Kopf von Abschnitt 53).
- **TB-139, Entwurf v2:** `logs/steuernder_chat/2026-10-07_tb139_v2.tar.gz` (19,4 MB), darin `v2/MAC_TB-139_entwurf_v2.md` (230 503 B, md5 `9e3dca61dcfa20d3d4bb166ac89a15c9`). Sollwerte der Simulation: 11 581 → 11 733 Zeilen, 20 Marken an 14 Einfügestellen, T4 behält 3 069 B Luft. Vorgesehener Name: `docs/auftraege/MAC_TB-139_register_fable_07a.md`.
- **Regeldateien:** `ARBEITSWEISE.md` 2 413 Zeilen (156 926 B, md5 `e85163e98db7f0b9387f4c990b67f8ca`; Abschnitt 0: 25 681 B) · `UMZUG.md` 380 Zeilen (26 923 B; Abschnitt 3: 5 897 B) · `BACKLOG.md` 331 Zeilen (76 344 B, md5 `d7dd54bbe63eeb26b9288e620f5554bd`). Journal: Block EH steht (TB-140), nächste Kennung EI.
- **Ablage:** heute neu `FABLE_ANFRAGE_2026-10-07a_…`, `FABLE_UEBERGABE_2026-10-07_eroeffnung.md`, `FABLE_ANTWORT_2026-10-07a_…` (von Fable abgelegt), `ERGEBNIS_TB-140_…` (Ablage-Fassung, Z. 1–435, 76 751 B); `UEBERGABE.md` erneuert, zuletzt mit diesem Block. `BACKLOG.md` in der Ablage trägt den Stand vor TB-138. Zahl der Einträge und Füllstand: Zusatz am Ende dieses Blocks.
- **Projekt-Erinnerung:** Messung 07.10.2026 (Nachtrag 15:59 mit Zusatz 16:21): die vier geladenen Dateien je 0 Treffer mit Wert; vier weitere gelistete Dateien tragen Werte und stehen nach R56 (d) unter der Sperre. Nichts geändert. Vor der nächsten Fable-Eröffnung alle gelisteten Dateien neu messen.
- **Nummern:** TB-139 Registerauftrag; der nächste Mac-Auftrag danach ist TB-141 (Regelwerk-Nachtrag). Journal ab EI. Fable vergibt ab R84. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Sendetags und geht an einen neuen Fable-Chat (der letzte endete rot, geschätzt rund 540 000).

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-139 fertig bauen** (dieser neue Chat hat die Antwort nicht bewertet, er darf bauen): Platzhalter füllen — `<<BEFUNDE-07a>>` und `<<BEFUNDE-07a-KURZ>>` aus den neun Punkten des Nachtrags 18:11, `<<HEAD>>` —, E1 bis E4 entscheiden (Handwerk), v3 von einem Helfer bauen lassen; zwei frische Gegenleser mit getrenntem Zeilenbereich; Trockenlauf des Prüfskripts am echten Repo. **Dann Karte „Einzelfreigabe Registereintrag“ mit dem fertigen Auftrag.** Danach Auftrag, Zeiger und Nachtrag in den Arbeitsbaum, Auslöser (`docs/auftraege/_ausloeser/starte_TB-139`), der Betreiber schickt den Satz; Abnahme durch einen Helfer.
2. **Nach dem Eintrag** erneuert ein Helfer die Ablage: Abschnitt 55, Index, Dialog-Index, `BACKLOG.md`.
3. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt (Helferauftrag `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilennummern am Stand `d781f1b`; danach sofort die Ampel messen).
4. **Zweite Fable-Anfrage** (54.6 Nr. 2, 6, 7, 9, 10; dazu zur Kenntnis die neun Befunde zu 07.10.a): feste Teile `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md`; wartet auf die Pakete 3, 5 und 11 von TB-137.
5. **Regelwerk-Nachtrag (TB-141):** die Regeln aus Block 7 hier und aus den Umzugsblöcken 06.10.2026 (13:43, 16:40) und 07.10.2026 (06:59), je Block 7.
6. **Backlog-Einträge aus Fable 07.10.a:** Bauauftrag Zellen-Erzeuger nach R81 und R82 (Schnitt, Wachen, Felder, Abnahme mit drei Test-Snapshots); Messungen vor dem Tag zu R78 (a), R81 (c), R82 (c); R81 (d) mit Posten 4.
7. **Backlog- und Journal-Nachtrag** zur Abnahme TB-140 und zu Fable 07.10.a: steht in TB-139 v2 (Schritt B und Journal).
8. **Beim Betreiber offen** (noch nicht gefragt): ob die vier Erinnerungsdateien mit Werten bereinigt werden; ob eine Fable-Anfrage ab rund 20 KB als Datei statt als Kopierblock übergeben werden darf (Block 7 Nr. 1).

### Block 5 — Wartezustände

TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Kein Fable-Chat hat eine offene Anfrage. Keine Mac-Sitzung läuft, keine Karte ist offen, keine Nachschau ist geplant.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- 08:10: unterwegs, Arbeit über App und Termius; „Arbeite heute so viel wie möglich selbstständig ab, damit wir endlich wieder größere Fortschritte machen.“; „Fable ist fertig.“ · 11:20: „Tb140 fertig“ · 17:02: „Die Fable Verfahrensprüfung ist fertig“ · 19:42: „bin am mac“.
- Karte 14:55: „Erst Fable, dann ein Eintrag (Empfohlen)“ und „Heute Abend am Mac (Empfohlen)“.
- Vorgaben ohne Widerspruch: TB-140 als Messung vor TB-139; TB-139 bleibt der Registerauftrag, der Regelwerk-Nachtrag wird TB-141; TB-139 baut ein Helfer mit eigenem Kontext; Auslöser erst, wenn Auftrag, Zeiger und Nachtrag im Arbeitsbaum liegen.
- **Keine Freigabe** für Register, Sperrliste, Signalpfad oder Parameterdateien. Die Einzelfreigabe zum Registereintrag steht aus.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. **Ampel:** 28 890 (07:03) → 86 022 (08:42) → 196 173 (10:33) → 258 805 (15:58) → 314 402 (16:22) → 380 093 (18:11) → 388 272 (19:43), trotz Helfern. Teuer waren: die Helferaufträge, die der Chat von Hand schrieb (rund 20 Aufträge zu 3 bis 6 KB) statt per Skript aus Bausteindateien, wie es die Regel verlangt; und der Kopierblock der Fable-Anfrage (34 882 B einmal gelesen und einmal ausgegeben: rund 55 000). ⇒ Helferaufträge aus Bausteindateien bauen; für eine Fable-Anfrage dieser Grösse den Betreiber fragen, ob die Datei im Chat als Übergabe genügt. Der Kopierblock ist vom Chat ausgegeben und nicht gegen die Datei geprüft; massgeblich ist `logs/steuernder_chat/ablage_07a/FABLE_2026-10-07a_SENDETEXT.txt`.
2. **Auftragsgrösse:** TB-140 wuchs über drei Gegenleserunden von 58 709 B auf 159 021 B (Vorbild 33 392 B); er lief in 23 Minuten ohne Abweichung. ⇒ Dem Berichtiger ein Grössenziel geben; Lücken, die keine Messung ändern, als Hinweis lassen.
3. **Wortwahl:** „acht formale Befunde“ (Zwischenmeldung 08:43) für eine Liste, in der zwei Aussagen ohne Beleg standen. ⇒ Sammelwort erst nach der Einordnung jedes Befunds.
4. **Schnellprüfung ohne Wert:** Lock gegen `dist-info` per awk trug nicht (Nachtrag 10:32, Abschnitt 8).
5. **Falsche Folgerung im Nachtrag 15:59** zu den Erinnerungsdateien, berichtigt im Zusatz 16:21. ⇒ Vor einer Folgerung die Stelle lesen, die sie regelt (hier die Eröffnung, R56 (d)).
6. **Karte und Stillstand:** Die Karte stand von 11:37 bis 14:55 offen; solange arbeitet der Chat nicht. ⇒ Ist der Betreiber unterwegs, vor der Karte alles Unabhängige anstossen, auch langlaufende Helfer.
7. **Geräteanbindung:** `date` liefert dort UTC ⇒ `TZ=Europe/Berlin date`. Der erste Aufruf der Ordnerfreigabe lief nicht, der zweite wurde erteilt.
8. **Was getragen hat:** der Start über den Wächter von unterwegs (der Betreiber schickt nur den Satz in der App); die Sonde `starte_TB-99` vor dem Zeigerwechsel; zwei unabhängige Abschriften mit `cmp` für Fable-Antworten; Bestand und Entwurf in einem Helfer, danach Gegenleser mit getrenntem Zeilenbereich; der Vorbau von TB-139 während der Messung; die Simulation an Kopien samt Gegenprobe.

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert), neu am 07.10.2026: `BEWERTUNG_FABLE_2026-10-06a.md` · `FABLE_06a_abnahme_helferbericht.md` · `TB-140_*` (Bestand, Entwürfe, drei Gegenleseberichte, Startbericht, Abnahmebericht) · `FABLE_07a_*` (Vorprüfung, Gegenlesen, Änderungen, Messung der Erinnerung, Abnahme der Antwort) · `ablage_07a/` (Sendetext, Ablage-Fassung des Ergebnisses TB-140) · `NACHTRAG_2026-10-07_*` · drei Archive: `2026-10-07_tb139_bau.tar.gz` (v1, 10,8 MB), `2026-10-07_tb139_v2.tar.gz` (19,4 MB), `2026-10-07_tb140_bau.tar.gz` (53,8 MB; enthält auch die bash-Quellen, die ein Gegenleser für eine Probe geladen hat). Nicht ohne Frage löschen.
- Verfällt mit diesem Chat: die Ordner in der Umgebung der Geräteanbindung (`tb139/`, `tb140/`, `fable07a/`, `abnahme_*`, `nachtrag/`, `ablage_tb140/`); das Tragende liegt in den Archiven.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, als erste Nachricht der Antwort auf „bin am mac“. Der neue Chat wird aus der Claude-Desktop-App auf dem MacBook geöffnet, mit dem Rechner ausgewählt (UMZUG 8). Kernlektüre: ab „## Nachtrag 07.10.2026, 18:11“ bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

### Zusatz 19:46 zum Umzugsblock 19:45

- **Betreiber, 07.10.2026, 19:44 („zukünftig“):** „Ich fand deine selbstständige Arbeitsweise heute super und möchte das du zukünftig immer so arbeitest!“ Lesart des steuernden Chats, vorläufig — „so“ heisst: Grosses bauen und prüfen Helfer mit eigenem Kontext, der steuernde Chat holt nur Kurzberichte; Handwerk entscheidet er als Vorgabe, Karten nur für echte Betreiberentscheide; nach jedem Schritt folgt ohne Startzeichen der nächste, auch über mehrere Aufträge und während eine Mac-Sitzung läuft; Zwischenmeldungen mit Ergebnis statt Rückfragen; Aufgaben an den Betreiber nur, wo seine Hand nötig ist. **Träger:** diese Datei; Projekt-Erinnerung `preferences.md` (eingetragen 19:46, Abschnitt „Antworten und Anleitung“; die Datei hat jetzt 10 002 B laut Lesekopf statt 9 440 B — die nächste Fable-Eröffnung nennt die neue Grösse und misst neu); der Eröffnungstext 19:45; `ARBEITSWEISE.md` mit dem Regelwerk-Nachtrag TB-141 (Block 4 Nr. 5).
- **Ablage, gemessen von einem Helfer (`project_info`, 19:4x):** 104 Einträge, Füllstand 1 064 653 von 2 000 000 B (53,2 %); die sieben geprüften Pfade vorhanden (drei Fable-Dateien 07.10., Ergebnis TB-140, Antwort 06.10.a, `UEBERGABE.md`, `BACKLOG.md`); `REGISTER_KOPIE_ABSCHNITT_00` bis `_54` lückenlos; keine doppelten Pfade. Das Erstelldatum von `UEBERGABE.md` bleibt beim Ersetzen stehen (05.10.2026) und sagt nichts über den Inhalt.
- **In diesem Chat versäumt:** Die Aufgaben an den Betreiber trugen keine Kennzeichnung [ortsunabhängig] / [Mac-pflichtig] (Erinnerung, 19.09.2026), und nach dem Auslöser für TB-140 war keine Nachschau per `send_later` geplant (Erinnerung, 24./29.09.2026); der Betreiber meldete „Tb140 fertig“ selbst. ⇒ Beides gilt weiter.

---

## Nachtrag 07.10.2026, 20:13 — neuer steuernder Chat eröffnet; Zweitmessung der neun Befunde zu Fable 07.10.a; Vorgaben E1 bis E4 für TB-139

**Eröffnung:** Ordnerfreigabe für `~/trading-bot` erteilt (der erste Aufruf lief nicht, der zweite wurde erteilt). Gemessen 19:49, ohne `git status` und ohne `git diff`: HEAD `b07ec7d` = `origin/main` (lokaler Zeiger); `BACKLOG.md` 331 Zeilen; geändert nur diese Datei; unverfolgt die drei Fable-Dateien vom 07.10. Ablage (Helfer, `project_info`): 104 Einträge, 1 070 408 von 2 000 000 (53,5 %); der Zusatz 19:46 nennt 1 064 653 — erschlossen, nicht gemessen: Die Datei wurde danach noch einmal erneuert. Ampel 19:50: Verlauf 47 500 (Grundlast 124 190), grün.

**Drei Helfer, nur lesend** (Berichte unter `logs/steuernder_chat/`: `TB-139_v3_BESTAND.md` 36 177 B, `TB-139_v3_MARKEN.md` 31 885 B, `TB-139_v3_ZEILEN.md` 27 231 B):
- **BESTAND:** Der Entwurf v2 (230 503 B) ist um 100 907 B grösser als TB-136 (129 596 B): Umstellskript +34 053, Daten-Block +18 165, Schritt A +15 369, Schritt B +11 338, Belegt +4 020, Entscheide +3 913, Rest +14 049. `bau.sh` verlangt genau acht Platzhalter und bricht mit gefüllten ab (ein Schritt „Entwurf → Auftrag“ fehlt); `quelle07/UEBERGABE.md` im Archiv ist älter als das Repo. Das Prüfskript schreibt im Trockenlauf nichts (am Quelltext gemessen, nicht ausgeführt).
- **MARKEN:** zwölf Paare aus Ort und Bezug am Wortlaut von R65 (a), R61 (b) und R70 (a): zwingend 0, unsicher 1 (48.7 (R39) zu R81 (a), (b)), nicht zwingend 11. Vorbild zu E1: Die Form „ein Teil, ein Markenwort, zwei Blöcke“ kam viermal vor — zweimal je Block eine Marke (4.2 in TB-129, 52.2 in TB-132), zweimal eine Marke (25.2 und 50.1 in TB-130); 34 und spätere Blöcke legen die Zahl nicht fest. Vorbild zu E2: TB-132 setzte eine, TB-136 zwei Marken des steuernden Chats, je mit Zusatz in Marke und Kette und einem Posten unter „Was offen bleibt“. `c1_marken.txt` ist Teilmessung.
- **ZEILEN** (Zweitmessung der neun Befunde, unabhängig vom Abnahmebericht): 51 Angaben, 45 treffen, 3 treffen nicht, 3 sind nicht messbar.

**Fehler in dieser Datei, Nachtrag 18:11, Absatz „Abnahme“:** Punkt 2 nennt „drei Aussagen“, als wäre die Zahl abschliessend, und lässt weg, dass Z. 246 nur `t3_supertrend` betrifft; Punkt 4 „Register Z. 4676 ist kein Blockzitat“ trifft wörtlich nicht und stellt die Anführung um. Beides ist beim Kürzen entstanden: Der Abnahmebericht nennt „bei t3_supertrend“ und „Marke nach Fliesstext“. Punkt 6 „in K1“ meint K1 der Anfrage; Punkt 9 schreibt R56 (b) auch die Anfrage zu, der Block nennt nur Eröffnungstext und Antwortdatei (Herkunft beider nicht gemessen). „Sie stehen in 55.7“ traf nicht: Dort stand der Platzhalter. Aus dem Abnahmebericht selbst: Die 54.5-Zeile für R79 (f) ist „R74 (54.1) (e)“, nicht (b). Im Kopf des Absatzes steht „25 Schritte“ gegen „rund 28 Werkzeugschritte“ im Bericht; „rund 90 Angaben“ ist dort nicht gefunden.

**Die neun Befunde in berichtigter Fassung** (Wortlaut für 55.7; Registerstellen sind mit Bezeichner genannt, nicht mit Zeile, R49 (e); die Zeilenangaben zu Antwort, Anfrage und Ergebnis TB-140 misst der Gegenleser von TB-139 noch einmal an der Quelle):
1. Der Kopf von R83 nennt „Voraussetzungen in R78 (a), (d) und (e)“; in der Fassung 07.10.a trägt nur R78 (a) eine Klammer mit einer Voraussetzung.
2. R83 (b), (f) und (c) führen Aussagen ohne den Stand „erschlossen“, den das Ergebnis TB-140 ihnen gibt (dort Z. 195, 229 und 246; in Z. 246 gilt „Code erschlossen“ nur für `t3_supertrend`, die sechs anderen Bots tragen „Code belegt“, Z. 250, 254, 258, 266, 270, 274). Dasselbe gilt, Teilmessung, für R83 (e) mit R78 (a) „für alle neun Bots“ (Z. 201–209, 330–332), für R83 (g) mit R78 (e) zu +inf und −inf (Z. 311, 336–337) und für R83 (g) zu den übrigen Zahlenspalten (Z. 312–315).
3. R80 (c) nennt R79 (a) „gemessen erfüllt“; TB-140 hat die Plattform nur mittelbar verglichen, gegen den Kopf des Lock (`docs/belege/TB-140/v4.txt`, Z. 10); Abschnitt 20 nennt denselben Wert zeichengleich. R80 (c) nennt unter „Offen“ den Lese-Audit aus R78 (a) nicht.
4. R80 (a) führt weiter „unter dem Blockzitat von R72 (Vorbild 25.2)“ (Antwort 07.10.a, Z. 233; zeichengleich schon in 06.10.a, Z. 157); die Marke an 25.2 steht selbst in `>`-Schreibweise nach Tabelle und Fliesstext, nicht unter einem Blockzitat.
5. R78 (a) schreibt „Lese-Audit (41.2 B4, Teil (b))“; B4 (b) heisst dort „Leseprotokoll“. R83 (d) verweist auf R49 (f) nur sinngemäss. R82 nennt „Nullzeile 0 (R33, R36)“; R36 (48.4), ganz gelesen, nennt die Nullzeile nicht, den Wert 0 trägt nur R33 (48.1).
6. R79 (c) ist gegenüber der Fassung 06.10.a unverändert; der Beleg für die Krypto-Zeile (TB-140, Z1) steht nur in der Quelle von R83 und in K1 der Anfrage 07.10.a (dort Z. 102), nicht in K1 der Antwort (Z. 175).
7. Im Antworttext, nicht im Block: Z. 92 „zwei Test-Snapshots“ (R81 (h): drei); Z. 175 „zwei Voraussetzungen“ (R80 (c): drei); Z. 148 nennt die geänderte „Quelle“ von R79 nicht; Z. 216 führt ein Zitat ohne „(5.2)“; Z. 93 und 97 schreiben „Einzelfreigabe“, das Wort steht in 37.3 nicht.
8. Orte, die R80 weder unter (a) noch unter (b) führt: im Text eines Blocks als Geltungsbereich oder Beleg genannt 17.0, 48.4 (R36), 48.7 (R39), 48.17 (R49), 49.1 (R53); nur in einer „Quelle des Grundes“, Teilmessung, 15.3, 15.7, 24.3, 31.2, 48.5 (R37), 53.4 (R69). Bezüge, die die Marke aus R80 (a) am selben Ort nicht nennt: 53.9, Zeile „R72 (53.7) (d)“, für R78 (g); 54.5, Zeile „R74 (54.1) (e)“, für R79 (f); 46.4 für R78 (b); 48.1 und 48.2 für R78 (e); 48.14 für R78 (a).
9. R56 (b) verlangt den Commit von Eröffnungstext und Antwortdatei vor dem Eintrag; Anfrage, Eröffnung und Antwort 07.10.a waren vor TB-139 nicht in git (`git ls-files`, je 0 Zeilen, 07.10.2026); Schritt 0 von TB-139 committet alle drei vor dem Eintrag.

Lesart des steuernden Chats, vorläufig: Keiner dieser Befunde verlangt eine Rückfrage vor dem Eintrag; sie gehen mit der nächsten Anfrage zur Kenntnis an Fable. Gemessen von zwei Helfern unabhängig (Abnahme und Zweitmessung, 07.10.2026) gegen die Antwort, das Ergebnis TB-140 und das Register; nicht gemessen: Code; von den Belegen ist nur `docs/belege/TB-140/v4.txt` geöffnet.

**Vorgaben des steuernden Chats für TB-139** (Handwerk; sie gelten, wenn der Betreiber nicht widerspricht):
- **E1:** je Teil aus R80 (a) eine Marke im Wortlaut des Marken-Blocks (20 Marken, so simuliert). Das Vorbild steht zwei zu zwei; die Marke übernimmt Fables Wortlaut unverändert, der steuernde Chat teilt ihn nicht auf. Die Form geht in 55.8 zur Kenntnis an Fable.
- **E2:** keine eigene Marke. Kein Ort ist nach R65 (a) zwingend; 48.7 (R39) ist unsicher (R70 (a), dritter gegen vierten Satz) und hängt an der Lesart aus TB-136 (54.6 Nr. 6), die Fable nicht beantwortet hat. Eine fehlende Marke lässt sich nachtragen, eine gesetzte nicht zurücknehmen. 48.7 steht mit beiden Gründen in 55.8 Nr. 10 und geht in die zweite Fable-Anfrage. TB-139 ist damit der erste Registerauftrag seit R65 ohne eigene Marke.
- **E3:** wie gebaut — keine Vormessungsdatei; der Kopf von 55 nennt diese Datei am Commit von Schritt 0.
- **E4:** wie vorgeschlagen — 06a „nein“, 07a „ja“, 04a unberührt.
- **Grössenziel für v3:** nicht grösser als v2 (230 503 B); Berichtigungen nach dem Gegenlesen netto höchstens +3 KB; Lücken, die keine Messung ändern, bleiben Hinweis im Bericht.

**Nächste Schritte:** v3 von einem Helfer bauen lassen (Platzhalter bis auf `<<FREIGABE>>` gefüllt, `bau.sh` um den Schritt „Entwurf → Auftrag“ ergänzt); zwei frische Gegenleser mit getrenntem Zeilenbereich; Trockenlauf des Prüfskripts am echten Repo; dann die Karte „Einzelfreigabe Registereintrag“.

---

## Nachtrag 07.10.2026, 21:19 — TB-139 v3 gebaut und gegengelesen; ein Befund der Klasse A, Berichtigungen K1 bis K15; Befund 8 berichtigt

**Bau (Helfer BAU; `logs/steuernder_chat/TB-139_v3_BAU.md`):** `MAC_TB-139_entwurf_v3.md` 226 717 B, 1 806 Zeilen, md5 `43fafb066da6556f43fbeffd3c2fb410` (−3 786 B gegen v2; angestrebt waren 215 bis 225 KB, verfehlt um 1 717 B). Ein Platzhalter bleibt: `<<FREIGABE…>>`. Simulation für 07.10. und 08.10.2026: 11 581 → 11 733 Zeilen, 20 Marken an 14 Stellen, Blöcke 6/6, Gegenproben G1 bis G7 schlagen an, T4 behält 3 069 B Luft. Trockenlauf des Prüfskripts am echten Repo, 20:50, ohne `--arbeitsbaum`: rc 0 (Marken 20 an 14, Fundstellen 131, Zählungen 18), `.git/index` vorher gleich nachher. 0b an einer Kopie: bestätigt, soweit messbar; `registerbericht.py --pruefen` und `test_vorregistrierung` nicht gemessen. Der Helfer fand beim Start (20:45) ein `v3/` aus einem ersten Lauf (20:15 bis 20:44) vor — der erste Helferaufruf dieses Chats lief, ohne dass sein Bericht ankam; der zweite hat nachgemessen und zweimal neu gebaut (md5 gleich).

**Gegenlesen, zwei frische Helfer mit getrenntem Bereich** (`TB-139_v3_GEGEN1.md` Z. 1–512, rund 430 Angaben; `TB-139_v3_GEGEN2.md` Z. 513–1806, rund 1 010 Angaben): **ein A-Befund** — Block E2 für `BACKLOG.md` nennt „zwei Test-Snapshots (R81 (h))“, R81 (h) nennt drei. Anhang A: kein A-Befund; Blöcke gehen zeichengleich aus der Antwortdatei ins Register, alle Wachen des Einfügeskripts liegen vor dem Schreiben, ein zweiter Lauf wird abgewiesen. Jede Zeilenangabe der neun Befunde trifft an der Quelle (damit zweimal unabhängig gemessen). 23 Befunde der Klasse B.

**Fehler dieses Chats:** (1) Befund 8 im Nachtrag 20:13 führt 15.3 unter „nur in einer Quelle des Grundes“; R82 (d) nennt im Blocktext „1c“, das ist 15.3 (c). Berichtigte Fassung von Punkt 8:
8. Orte, die R80 weder unter (a) noch unter (b) führt: im Text eines Blocks als Geltungsbereich oder Beleg genannt 15.3 (c) (in R82 (d) als „1c“), 17.0, 48.4 (R36), 48.7 (R39), 48.17 (R49), 49.1 (R53); nur in einer „Quelle des Grundes“, Teilmessung, 15.7, 24.3, 31.2, 48.5 (R37), 53.4 (R69). Bezüge, die die Marke aus R80 (a) am selben Ort nicht nennt: 53.9, Zeile „R72 (53.7) (d)“, für R78 (g); 54.5, Zeile „R74 (54.1) (e)“, für R79 (f); 46.4 für R78 (b); 48.1 und 48.2 für R78 (e); 48.14 für R78 (a); 53.1 für R79 (b).
(2) „Das Vorbild steht zwei zu zwei“ (Vorgabe E1) ist zu glatt, aus dem Helferbericht übernommen: 50.1 trägt eine Marke für einen Block und einen Unterabschnitt, zwei Blöcke in einer Marke trägt nur 25.2. (3) „Kein Ort ist nach R65 (a) zwingend“ (Vorgabe E2): Der Gegenleser hält 53.1 (R66) (b) zu R79 (b) für fraglich (R65 (a), zweiter Satz: Bestätigung); der erste Helfer nannte denselben Ort das schwächste „nicht zwingend“. Die Vorgabe E2 bleibt (keine eigene Marke), unsicher heissen jetzt zwei Orte: 48.7 (R39) und 53.1 (R66) (b).

**Berichtigungen für v4 (Vorgabe; ein frischer Helfer, Grössenziel höchstens v3 + 1,5 KB):** K1 „drei Test-Snapshots“ · K2 Befund 8 wie oben, 55.8 Nr. 10 gleich · K3 55.8 Nr. 10 nennt jeden Ort und Bezug aus Befund 8 · K4 E2 und 55.8 Nr. 10: unsicher sind 48.7 und 53.1 · K5 Vorbild zu E1 ohne „zwei zu zwei“ · K6 „nur das Ob (27.2)“ nur bei R78 (a) und R82 (c), nicht bei R81 (c) · K7 „R82 (a), (b) und (d) regeln sie“ als Lesart gekennzeichnet · K8 „schneiden nirgends am 1. September 2026 ab“ im Wortlaut des Ergebnisses TB-140 (Z. 446–447) · K9 „über 174 Dateien“ an der Quelle messen · K10 Lesart zu Z2 nicht als Anführung des Auftrags TB-140 · K11 „(TB-135)“ belegen oder streichen · K12 Indexzeile 5.2 in der Form der Nachbarzeilen · K13 Ketten „Offen: 55.8 Nr. …“ nach dem Vorbild in Abschnitt 54 · K14 „elf“ und „acht Ersetzungen“ nachzählen · K15 rc 1 nennen. Nicht berichtigt, Hinweise: 0a-Soll entsteht erst beim Ablegen (so gewollt); Teilketten-Anker im Backlog; Einfügeskript schreibt `--daten` nach dem Register; `git()` im Vorschau-Modus ohne `--no-optional-locks`.

**Nächste Schritte:** v4 bauen und simulieren, Trockenlauf am echten Repo, ein frischer Helfer liest nur die geänderten Stellen; dann die Karte „Einzelfreigabe Registereintrag“.

### Zusatz 22:03 zum Nachtrag 21:19 — TB-139 v4 fertig bis auf die Freigabe; Start vorbereitet; Bestand für TB-141

- **TB-139, Entwurf v4:** `logs/steuernder_chat/MAC_TB-139_entwurf_v4.md`, 227 781 B, 1 806 Zeilen, md5 `43afc025590f8d34058c1692125eaf2b` (v2 230 503 B, v3 226 717 B); ein Platzhalter, `<<FREIGABE…>>` in Z. 18. Archiv `logs/steuernder_chat/2026-10-07_tb139_v4.tar.gz` (46 488 505 B, md5 `b07fed8b8bac0e123da9c419fb507e74`; darin `tb139/v4/`, Berichte, Helferaufträge, Eingaben, `tb139/start/`, `tb141/`). Zweimal gebaut (md5 gleich). Simulation für 07.10. und 08.10.2026: 11 581 → 11 733 Zeilen, numstat 152/0, 20 Marken an 14 Stellen, Blöcke 6/6, Gegenproben G1 bis G7 schlagen an, T4 behält 3 069 B Luft, Register nachher 998 257 B, Marken nachher 100/145/96. Trockenlauf des Prüfskripts am echten Repo, ohne `--arbeitsbaum`: Helfer 21:41 rc 0; steuernder Chat 22:02 rc 0 (Anker 20 von 20, Fundstellen 131, Zählungen 18), `.git/index` vorher gleich nachher.
- **Berichtigungen:** K1 bis K8, K10, K12 und K15 getan. K9, K11, K14 nicht nötig: an der Quelle belegt (174 im Ergebnis TB-140 Z. 29, 107, 393; TB-135 in `BACKLOG.md` Z. 289 und `docs/belege/TB-135/`; die Listen haben 11 und 8 Einträge). K13: Die zwei Helfer widersprachen sich zum Vorbild; vom steuernden Chat gemessen: In 53 und 54 nennen die Ketten nicht jeden Posten, der den Block nennt (54.2 ohne Nr. 6, 53.1 ohne Nr. 3, 53.4 ohne Nr. 2, 53.7 ohne Nr. 8) — zugeordnet ist nach der Sache. Geändert nur Kette 55.4 („Nr. 1 bis 6 und 11“). Hinweise, nicht berichtigt: Kette 55.1 ohne Nr. 12, Kette 55.6 ohne Nr. 2; der Abschnitt „Entscheide“ nennt zu 48.7 R81 (a), 55.8 Nr. 10 nennt (a) und (b). Die zweite Leserunde hat der Helfer gemacht, der den Bau wiederholte (er hat die Änderungen nicht geschrieben); 55.8 Nr. 10 und Nr. 12 hat der steuernde Chat im Wortlaut gelesen.
- **Geräteanbindung:** Sie fiel während des Berichtigens weg (ein langer Bau im Hintergrund); ein zweiter Helfer hat den Bau in 27 Einzelschritten wiederholt, kein Aufruf über 40 s. ⇒ Bauläufe über die Brücke in Einzelschritten, nichts im Hintergrund, kein Aufruf über 150 s.
- **Nach der Freigabe:** `v4/skripte/z1_abschluss.py` setzt den Wortlaut der Freigabe ein und prüft, dass kein Platzhalter bleibt (mit Probetext 228 685 B). Start (Helfer START, `logs/steuernder_chat/TB-139_START.md`): Auslöser sind leere Dateien unter `docs/auftraege/_ausloeser/`, einzeln, über 30 s Abstand; Sonde `starte_TB-99`, dann Auftrag, Zeiger (`tb139/start/AKTUELLER_AUFTRAG.md` im Archiv, 7 775 B, Platzhalter `@@GESETZT@@`) und Nachtrag, dann `starte_TB-139`. Der Wächter startet mit `--effort high` und setzt kein Modell: Opus 5.5 hängt an der Voreinstellung am Mac, nur der Betreiber sieht es in der Kopfzeile.
- **TB-141, Bestand** (Helfer REGELN, `logs/steuernder_chat/TB-141_bestand_REGELN.md`, 29 249 B): 38 Regeln — steht schon 4, zu ergänzen 18, neu 16; vom Betreiber wörtlich eine (07.10.2026, 19:44). Acht Widersprüche W1 bis W8 zwischen neuen Regeln und bestehenden Zeilen, darunter: Helfer bauen und schreiben Aufträge (heute geübt) gegen 22.10 („nie für Register, Commits, Aufträge schreiben“); „solange die Karte offen ist, arbeitet der Chat nicht“ gegen 13 und 6d („die Arbeit läuft daneben weiter“). Ein Block mehr als im Umzugsblock 19:45 genannt: Umzug 06.10.2026, 07:08, Block 7 Nr. 3 bis 5. Vorbild: TB-133 (20 294 B). Die Widersprüche brauchen vor dem Bau von TB-141 einen Entscheid.
- **Beim Betreiber:** Karte „Einzelfreigabe Registereintrag“ mit drei weiteren Fragen (Erinnerungsdateien, Fable-Anfrage als Datei, Umzug), gestellt nach diesem Zusatz. Ampel 22:03: Verlauf 202 792 (Grundlast 124 190), gelb.

---

## Nachtrag 07.10.2026, 22:45 — Einzelfreigabe für TB-139 erteilt; Auftrag und Zeiger im Arbeitsbaum; Start über den Sitzungswächter

**Karte, gestellt gegen 22:05, beantwortet 22:44 (vier Fragen):**
- **Freigabe:** Kartentext wie im Auftrag unter „Freigabe des Betreibers, wörtlich“; gewählt: „Ja, freigeben (Empfohlen)“. Damit gelten die Vorgaben E1 bis E4 (keine eigene Marke des steuernden Chats).
- **Erinnerungsdateien:** „Bereinigen, Liste vorab (Empfohlen)“ — ein Helfer misst, der steuernde Chat legt je Datei die Streichliste vor; gestrichen wird erst nach dem Blick des Betreibers.
- **Fable-Anfrage:** „Ja, ab 20 KB als Datei (Empfohlen)“ — ab rund 20 KB geht die Anfrage als Datei in den Chat, der Betreiber lädt sie im Fable-Chat hoch; kürzere bleiben Kopierblock. Das ändert die Zeile „Fable-Anfrage: Steht ihr voller Text als Kopierblock in DIESER Antwort?“ in `ARBEITSWEISE.md`, Abschnitt 0 (geht in TB-141; löst den Widerspruch W3 aus dem Bestand).
- **Umzug:** „Nach der Abgabe von TB-139 (Empfohlen)“ — sobald die Mac-Sitzung abgegeben hat und alles committet ist; die Abnahme macht der neue Chat. Umzugsblock und Eröffnungstext schreibt der steuernde Chat dann.

**Auftrag:** `docs/auftraege/MAC_TB-139_register_fable_07a.md`, 228 647 B, 1 806 Zeilen, md5 `4c03950eb4783091734ec8b46d0682da` (Entwurf v4 mit dem Freigabetext, eingesetzt von `z1_abschluss.py`, rc 0: kein Platzhalter, ausserhalb des Freigabetexts gleich dem Entwurf, Simulation am fertigen Auftrag rc 0, 11 581 → 11 733 Zeilen, 20 Marken an 14 Stellen, Blöcke 6/6, Register nachher 998 257 B). Zeiger `docs/auftraege/AKTUELLER_AUFTRAG.md` auf TB-139 gesetzt (Zeile 39 und Zeile 52). **Erwartung 0a:** geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`; unverfolgt die drei Fable-Dateien vom 07.10. und der Auftrag.

**Start:** Sonde `starte_TB-99` 22:44: „claude-Prozesse: 0 im Repo, 0 ausserhalb“, „Schluesselbund entsperrt“. Danach Auftrag, Zeiger und dieser Nachtrag in den Arbeitsbaum, dann `starte_TB-139`. Ob der Satz im Fenster liegt, steht in `logs/sitzungswaechter/waechter.log` („Satz ins Fenster gelegt“); abgeschickt wird er vom Betreiber. Der Wächter startet mit `--effort high` und setzt kein Modell. Bis zum Commit von Schritt 0 legt der steuernde Chat nichts in den Arbeitsbaum, danach nichts bis zur Abgabe. Eine Nachschau per `send_later` ist geplant (unter einer Stunde); ohne Commit von Schritt 0 ist der Satz nicht angekommen: ein Hinweis an den Betreiber, dann warten. Geschlossen wird mit `schliesse_<voller HEAD>`, erst ab 600 s Alter des letzten Commits.

**Für die Abnahme (nächster Chat):** Sollwerte oben; Abnahme durch einen eng zugeschnittenen Helfer, nur lesend (Muster `logs/steuernder_chat/HELFER_AUFTRAG_TB-138_abnahme.md`); danach erneuert ein Helfer die Ablage (Abschnitt 55, Index, Dialog-Index, `BACKLOG.md`). Bau, Berichte und Helferaufträge liegen im Archiv `logs/steuernder_chat/2026-10-07_tb139_v4.tar.gz`; der fertige Auftrag und der Freigabetext zusätzlich unter `logs/steuernder_chat/` (`MAC_TB-139_register_fable_07a.md`, `TB-139_freigabe_0710.txt`). Offen danach: Streichliste der Erinnerungsdateien; die acht Widersprüche W1 bis W8 vor dem Bau von TB-141; TB-137; die zweite Fable-Anfrage.

---

## Umzug 07.10.2026, 23:39 — Stand für den neuen steuernden Chat (alle neun Blöcke; den Bau von TB-139 tragen die Nachträge 20:13, 21:19 mit Zusatz 22:03 und 22:45 unmittelbar davor)

Betreiber: Karte, beantwortet 22:44: „Nach der Abgabe von TB-139 (Empfohlen)“. Ampel 23:38: Verlauf 279 652 (Grundlast 124 190), gelb. **Dieser Block ersetzt den Umzugsblock vom 07.10.2026, 19:45.** Kernlektüre für den neuen Chat: ab dieser Überschrift bis Dateiende; die Nachträge 20:13 bis 22:45 nur bei Bedarf.

### Block 1 — Stand in drei Zeilen

- **TB-139 (Registereintrag, Abschnitt 55, R78–R83, 20 Marken) ist gelaufen und abgegeben** (HEAD `d4a28e9`), **aber noch nicht abgenommen.** Kernzahlen, vom steuernden Chat 23:37 gemessen, wie simuliert: Register 11 733 Zeilen, 998 257 B; numstat 152/0 im Commit `ad1fc0d`; 20 Marken mit „TB-139“; Überschriften 55.1 bis 55.8; alle 12 nicht leeren Zeilen aus Z. 227–243 der Antwortdatei stehen im Register.
- **Die Ablage ist nicht erneuert:** Abschnitt 55 fehlt dort, die Abschnittskopien mit neuen Marken, die Teile, Index, Dialog-Index und `BACKLOG.md` tragen den alten Stand.
- **Zwei Betreiberentscheide vom 07.10.2026, 22:44, sind noch nicht ausgeführt:** Erinnerungsdateien bereinigen (die Streichliste liegt vor, 25 Stellen brauchen sein Urteil) und „Fable-Anfrage ab rund 20 KB als Datei“ (gehört in TB-141).

### Block 2 — HEAD und Arbeitsbaum

HEAD = `d4a28e91f359cdd7fba4baa62f0ba1f8d430badb` (TB-139 D3, 07.10.2026, 23:23); `origin/main` (lokaler Zeiger) = `d4a28e9`. Gemessen 23:37, ohne `git status` und ohne `git diff`: vor diesem Block nichts geändert, nichts unverfolgt; jetzt geändert nur `docs/projektfuehrung/UEBERGABE.md` (dieser Block); keine `index.lock`. **Keine Sitzung läuft** (Schliess-Auslöser 23:37: „1 Sitzung(en) mit TERM beendet, 0 noch da“). `AKTUELLER_AUFTRAG.md` zeigt auf TB-139 (erledigt; md5 `1dbc864fa7b5353ace3f71f66e70b40c`), `letzter_satz.txt` trägt den Satz zu TB-139; kein Auftrag ist startklar. Der nächste Mac-Auftrag erwartet in 0a: geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`; unverfolgt sich selbst.

### Block 3 — Tragende Zahlen

- **Register:** 11 733 Zeilen, 998 257 B, sha256 beginnt `ab97ae1e31da161b`, Stand `ad1fc0d`, Abschnitte 0 bis 55. Höchster eingetragener Block R83; Fable vergibt ab R84.
- **TB-139:** Auftrag `docs/auftraege/MAC_TB-139_register_fable_07a.md` (228 647 B, md5 `4c03950eb4783091734ec8b46d0682da`) · Ergebnis `docs/ERGEBNIS_TB-139_register_fable_07a.md` (22 625 B, 248 Zeilen) · Belege `docs/belege/TB-139/` (66 Dateien) · Commits `e16872e` (Schritt 0: Stand des steuernden Chats), `35b4743` (0), `ad1fc0d` (A: Register), `be2fa85` (B/C), `11429c1` (Abgabe, Journal EI), `d4a28e9` (D3). **Sollwerte für die Abnahme:** 11 581 → 11 733 Zeilen; numstat 152/0; 20 Marken an 14 Einfügestellen (PRÄZISIERT 4, BERICHTIGT 1, ERGÄNZT 15); Blöcke 6/6 zeichengleich aus der Antwort 07.10.a, Z. 227–243; `registerkopie.py --marken` nachher 100/145/96 (vorher 95/128/91); T4 behält 3 069 B Luft; Dialog-Index 06a „nein“, 07a „ja“. Aus dem Ergebnis, ungeprüft: `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126); `test_vorregistrierung` 919 s; Index-Diff 298/252; Abschnitt „Für Fable (nur Verfahrensfragen)“ Z. 189–212.
- **Regeldateien:** `ARBEITSWEISE.md` unverändert (md5 `e85163e98db7f0b9387f4c990b67f8ca`; Abschnitt 0: 25 681 B) · `UMZUG.md` unverändert (Abschnitt 3: 5 897 B) · `BACKLOG.md` 349 Zeilen (82 007 B, md5 `583b4049aca0bd9e9aa12c97580c21c5`). Journal: Block EI steht, nächste Kennung EJ.
- **Ablage:** `UEBERGABE.md` erneuert mit diesem Block; alles andere Stand vor TB-139, `BACKLOG.md` vor TB-138. 104 Einträge, 53,5 % (19:50).
- **Projekt-Erinnerung:** Streichliste `logs/steuernder_chat/TB-139_ERINNERUNG_streichliste.md` (40 914 B, ohne Werte): 12 Dateien, 72 Fundstellen — 5 Zeilen streichen, 8 Halbsätze, 34 bleiben, 25 Entscheid des Betreibers. Nichts geändert. Die kontoweite Datei `/areas/trading-agent-projekt.md` (7 Fundstellen) ist aus einer Projektsitzung nicht schreibbar. Neun Zeilen mit Live-Parametern: nach dem Wortlaut von 27.1 kein Wert, die Messung vom 07.10. zählte sie als Wert.
- **Nummern:** nächster Mac-Auftrag TB-141 (Regelwerk-Nachtrag). Journal ab EJ. Fable vergibt ab R84. Fehler ab 21. Die nächste Fable-Anfrage trägt das Datum des Sendetags und geht an einen neuen Fable-Chat.

### Block 4 — Offene Punkte, in Reihenfolge

1. **TB-139 abnehmen:** ein eng zugeschnittener Helfer, nur lesend, eigener Ordner ausserhalb des Repos (Muster `logs/steuernder_chat/HELFER_AUFTRAG_TB-138_abnahme.md`); er rechnet jede Zahl an der Rohausgabe nach, die Kernzahlen danach der steuernde Chat. Backlog- und Journal-Nachtrag zur Abnahme in derselben Antwort.
2. **Ablage erneuern** (Helfer): Abschnittskopien (55 neu; 05, 42, 46, 48, 53, 54 mit neuen Marken), Teile, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`, `BACKLOG.md`, Ergebnis TB-139; Kontrolle über `project_info`.
3. **Streichliste der Erinnerung:** dem Betreiber die 25 Entscheide als Karte vorlegen, nach Art gebündelt (Live-Parameter; Zählungen zu Verfahrensbefunden; Ergebnisse verworfener Strategien; Einschätzungen eines früheren Fable-Chats); danach bereinigen. Zwei Inhalte fand der Helfer im Repo nicht (Befunde der Paar-Rotation, Fable-Einschätzung zum Neuaufbau): vor dem Streichen klären, wo sie stehen sollen. Die Liste ist dem Betreiber als Datei gegeben.
4. **TB-141, Regelwerk-Nachtrag:** Bestand `logs/steuernder_chat/TB-141_bestand_REGELN.md` (38 Regeln: 4 stehen schon, 18 zu ergänzen, 16 neu; Vorbild TB-133, 20 294 B). Acht Widersprüche W1 bis W8 brauchen vor dem Bau einen Entscheid (W3 ist mit der Karte 22:44 entschieden: ab rund 20 KB als Datei). Dazu Block 7 hier.
5. **TB-137 abnehmen,** sobald der Betreiber `GESAMTERGEBNIS_CLOUD_TB-137.md` einfügt (Helferauftrag `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilennummern am Stand `d781f1b`; danach sofort die Ampel messen).
6. **Zweite Fable-Anfrage:** 54.6 Nr. 2, 6, 7, 9, 10; aus 55.8 die Posten „nächste Anfrage an Fable“ (Nr. 5, 6, 9, 10, 12, 13), darunter die zwei unsicheren Orte 48.7 (R39) und 53.1 (R66) (b) und die Form der Marken; zur Kenntnis die neun Befunde (55.7). Feste Teile `logs/steuernder_chat/FABLE_naechste_anfrage_feste_teile.md`; wartet auf die Pakete 3, 5 und 11 von TB-137. Ab rund 20 KB als Datei. Vor dem Absenden alle Erinnerungsdateien gegen 27.1 messen.
7. **Bauauftrag Zellen-Erzeuger** nach R81 und R82 (55.8 Nr. 1 bis 4; Backlog E-7/E-8).
8. **Stehen so im Register, als Hinweis bekannt:** Kette 55.1 ohne Nr. 12, Kette 55.6 ohne Nr. 2 (Zuordnung nach der Sache; Nachtrag 21:19, Zusatz 22:03).

### Block 5 — Wartezustände

TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Kein Fable-Chat hat eine offene Anfrage. Keine Mac-Sitzung läuft, keine Karte ist offen, keine Nachschau ist geplant.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat

- Karte, gestellt gegen 22:05, beantwortet 22:44: „Ja, freigeben (Empfohlen)“ (Einzelfreigabe TB-139, mit dem Eintrag verbraucht) · „Bereinigen, Liste vorab (Empfohlen)“ · „Ja, ab 20 KB als Datei (Empfohlen)“ · „Nach der Abgabe von TB-139 (Empfohlen)“.
- Vorgaben ohne Widerspruch: E1 bis E4 und das Grössenziel (Nachtrag 20:13; E2 mit zwei unsicheren Orten, Nachtrag 21:19).
- **Keine Freigabe** für weitere Registereinträge, Sperrliste, Signalpfad oder Parameterdateien. In der Erinnerung wird nichts gestrichen, bevor der Betreiber die Liste gesehen und die 25 Stellen entschieden hat.

### Block 7 — Fehler dieses Chats und die Regeln daraus (alle ohne Nummer)

1. **Ampel:** 47 500 (19:50) → 202 792 (22:03) → 245 814 (22:46) → 256 206 (23:10) → 279 652 (23:38), bei 16 Helfern. Die Helferaufträge kamen aus Bausteindateien auf dem Gerät (Aufruf je rund 600 B, der Helfer liest seinen Auftrag selbst) — das trug. Teuer war die Zahl der eigenen Schritte (69): Jeder liest den ganzen Verlauf. ⇒ Messungen bündeln (ein Aufruf, mehrere Fragen); Helfer parallel starten; nach jedem Helferbericht nur eine Nachmessung.
2. **Aus Helferberichten ungeprüft übernommen:** „zwei zu zwei“ (Vorbild E1) und „keiner zwingend“ (E2); dazu eigener Fehler in Befund 8 (15.3 falsch eingeordnet). Alle drei vom Gegenleser gefunden. ⇒ Was in Registertext oder in eine Vorgabe geht, an der Tabelle des Berichts lesen, nicht an der Kurzantwort; der Gegenleser bekommt genau diese Stellen genannt.
3. **Zwei Helfer widersprachen sich** (K13, Vorbild der Ketten). ⇒ Bei Widerspruch misst der steuernde Chat die eine Tatsache selbst, mit einem Skript.
4. **Geräteanbindung fiel 21:31 weg,** während ein Helfer einen langen Bau im Hintergrund laufen liess. ⇒ Bauläufe über die Brücke in Einzelschritten, nichts im Hintergrund, kein Aufruf über 150 s.
5. **Ein Helferaufruf lief, ohne dass sein Bericht ankam** (BAU, 20:15, der Chat wurde unterbrochen); der zweite fand dessen `v3/` vor und mass nach. ⇒ Vor einem Helferstart prüfen, ob der Zielordner schon existiert.
6. **Was getragen hat:** Helferaufträge als Datei; zwei Gegenleser mit getrenntem Bereich und Einordnung A/B mit kleinster Berichtigung; die Zweitmessung der Zeilenangaben; `z1_abschluss.py` (Freigabe einsetzen, dann Simulation am fertigen Auftrag); die Sonde vor dem Zeigerwechsel; der Start vorbereitet, während gegengelesen wurde; Nachschau per `send_later` (eine, nach dem Blick um 23:08 verschoben auf 23:36).

### Block 8 — Zwischengelagert, noch nicht eingearbeitet

- Unter `logs/steuernder_chat/` (von git ignoriert), neu in diesem Chat: `TB-139_v3_BESTAND.md`, `_MARKEN.md`, `_ZEILEN.md`, `_BAU.md`, `_GEGEN1.md`, `_GEGEN2.md`, `TB-139_v3_befunde_07a.md` · `TB-139_v4_BERICHTIGEN.md` · `TB-139_START.md` · `TB-141_bestand_REGELN.md` · `TB-139_ERINNERUNG_streichliste.md` · `MAC_TB-139_entwurf_v4.md`, `MAC_TB-139_register_fable_07a.md`, `TB-139_freigabe_0710.txt` · zwei Archive: `2026-10-07_tb139_v4.tar.gz` (46,5 MB; Bau v4 mit Simulation) und `2026-10-07_tb139_nach_archiv.tar.gz` (189436 B; alle Helferaufträge und Bausteine unter `tb139/auftraege/`, Berichte, Eingaben, Abschlusslauf). Nicht ohne Frage löschen.
- Verfällt mit diesem Chat: die Ordner `tb139/` und `tb141/` in der Umgebung der Geräteanbindung; das Tragende liegt in den zwei Archiven.

### Block 9 — Eröffnungstext

Als Kopierblock im Chat ausgegeben, als erste Nachricht nach der Abgabe; Kopie unter `logs/steuernder_chat/EROEFFNUNG_2026-10-07_nach_TB-139.txt`. Der neue Chat wird aus der Claude-Desktop-App auf dem MacBook geöffnet, mit dem Rechner ausgewählt (UMZUG 8). Kernlektüre: ab der Überschrift dieses Umzugsblocks bis Dateiende, dazu ARBEITSWEISE Abschnitt 0 und UMZUG Abschnitt 3.

## Nachtrag 08.10.2026, 07:36 — neuer steuernder Chat: Abnahme TB-139, Ablage, Entscheide W1/W2/W7, Start TB-141

- **Übernahme** 07.10.2026, 23:52: HEAD `d4a28e9` = `origin/main`, `BACKLOG.md` 349 Zeilen, geändert nur diese Datei. Kernlektüre über die Geräteanbindung mit Abschnittsfilter.
- **TB-139 abgenommen** (Helfer ABNAHME139; Kernzahlen vom steuernden Chat 00:11 mit eigenem Skript nachgemessen, alle wie Soll). Anmerkungen und **Fehler Nr. 21** (Register Z. 11727: „48.7 (R39) zu R81 (a)“ neben „(a) und (b)“, aus dem Auftrag) und **Nr. 22** („Backlog E-7/E-8“ in Block 4 Nr. 7 des Umzugs 07.10., 23:39; richtig: `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 122/123) stehen im Journalblock EJ, den TB-141 einträgt. Bericht `logs/steuernder_chat/TB-139_ABNAHME_bericht.md`.
- **Ablage erneuert** (Helfer ABLAGE139): 63 Dateien (61 ersetzt, 2 neu), 104 → 106 Einträge, 54,2 % → 56,5 %; md5 über die md5-Liste `acef90519ecef4ed36f112b06ed281b1`.
- **Karte** (gestellt 08.10.2026, 00:34; beantwortet vor 06:55): W1 „Helfer bauen Entwürfe (Empfohlen)“ · W2 „Nur wörtlicher Auszug (Empfohlen)“ · W7 „Wichtiges ja, Form als Hinweis (Empfohlen)“. Vorgaben W4, W5, W6, W8 (Antwort 00:33) ohne Widerspruch. Wortlaute: TB-141.
- **TB-141** `docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md` (76 559 B, md5 `fc488cb6a158bec5ac0d4a4f067c25aa`): gebaut von Helfer BAU141, an Kopien simuliert (Python 3.10 und 3.9.25), gegengelesen von GEGEN141_1 und _2 (8 A-Befunde eingearbeitet), zweite Runde GEGEN141_3 (keine A). Formhinweise nicht eingearbeitet (W7): G1 B2–B7 (darunter: das Prüfskript lief nicht am echten Repo, weil `probe` Belege schreibt), G2 B1, B2, B4, B5, B6, B8, G3 B-a, B-b; W8 lässt ARBEITSWEISE Z. 97 stehen. Berichte `logs/steuernder_chat/TB-141_*_bericht.md`.
- **Start:** Sonde 08.10.2026, 07:18:49 (05:18:49Z): 0 Sitzungen, Schlüsselbund entsperrt. Danach Auftrag, Zeiger und dieser Nachtrag in den Arbeitsbaum, dann `starte_TB-141`.
- **Reihenfolge danach:** TB-141 → Abnahme TB-137 (wartet auf den Betreiber) → zweite Fable-Anfrage → Bauauftrag Zellen-Erzeuger (Bestand `logs/steuernder_chat/ERZEUGER_bestand_R81_R82_bericht.md`; Signalpfad braucht Einzelfreigabe nach 37.3). Streichliste der Erinnerung: Karte an den Betreiber, nichts gestrichen.
- Arbeitsdateien unter `$HOME/sc/` der Geräteanbindung verfallen mit diesem Chat; das Tragende liegt in `logs/steuernder_chat/2026-10-08_sc_tb141.tar.gz`.

## Umzug 08.10.2026, 19:58 — Stand für den neuen steuernden Chat (alle neun Blöcke)

Betreiber: Karte, beantwortet 08.10.2026 vor 19:58: „Jetzt umziehen (Empfohlen)“ (zuvor genehmigt: „Nach Abgabe von TB-141“). Ampel 19:54: Verlauf 302 222 (Grundlast 130 887), rot. **Dieser Block ersetzt den Umzugsblock vom 07.10.2026, 23:39.** Den neuen Chat legt der steuernde Chat selbst an (Betreiber 08.10.2026, 08:36, per Karte präzisiert: der steuernde Chat beim Umzug).

### Block 1 — Stand in drei Zeilen
- **TB-141 (Regelwerk-Nachtrag) ist gebaut, gegengelesen, im Arbeitsbaum und gestartet, aber nicht angekommen:** Die Sitzung (PID 3242, seit 09:24) hängt an der Chrome-Startfrage von Claude Code; der Satz ging ins falsche Fenster (Fehler 23).
- **TB-139 ist abgenommen, die Ablage erneuert, die Projekt-Erinnerung bereinigt** (Nachtrag 07:36; Streichliste 08.10.2026 vollzogen).
- **Offen beim Betreiber:** Enter im Terminal-Fenster „claude --effort high --remote-control“ und Satz TB-141 einfügen; Text für die kontoweite Erinnerung (Antwort 07:47) abschicken; Gesamtergebnis TB-137.

### Block 2 — HEAD und Arbeitsbaum
HEAD = `origin/main` = `d4a28e91f359cdd7fba4baa62f0ba1f8d430badb`. Geändert: `docs/projektfuehrung/UEBERGABE.md` (Nachtrag 07:36 und dieser Block), `docs/auftraege/AKTUELLER_AUFTRAG.md` (Zeiger auf TB-141, 7 822 B, md5 `5684de57530b…`, gesetzt 07:36). Unverfolgt: `docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md` (76 559 B, md5 `fc488cb6a158bec5ac0d4a4f067c25aa`). Gemessen ohne `git status`. Terminal auf dem Mac: Fenster mit Titel „claude --effort high --remote-control“ (window_id 20771) wartet an „Use Chrome browser by default?“ (vorausgewählt „1. No, keep browser tools off“); das Fenster 15501 ist eine bash-Shell, in der die Sätze TB-132 bis TB-141 als Befehle stehen. Sonde 19:11: 1 claude-Prozess im Repo, schlafend. Eine Cloud-Sitzung des Betreibers (19:11, Zweig `claude/tb-141-auftrag-7cu68m`) las `origin/main`, fand TB-141 nicht und brach ohne Änderung ab.

### Block 3 — Tragende Zahlen
- **TB-141 Sollwerte:** ARBEITSWEISE 58/0 (2 413 → 2 471 Zeilen), BACKLOG 13/0 (349 → 362), JOURNAL Block der Sitzung + 3 + 11 + 1 (Simulation 28/0); Anhang-Skript sha256 `1af78b61…5d6c`; 0a erwartet geändert `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`, unverfolgt den Auftrag (prüft kein md5 der Übergabe). Berichte: `logs/steuernder_chat/TB-141_BAU141_bericht.md`, `TB-141_GEGEN141_1/2/3_bericht.md`.
- **Register** unverändert: 11 733 Zeilen, 998 257 B, Stand `ad1fc0d`, Abschnitte 0–55, höchster Block R83.
- **Ablage:** 106 Einträge, 56,5 % (08.10.2026, 00:2x); `UEBERGABE.md` mit diesem Block erneuert.
- **Projekt-Erinnerung:** `overview.md` 9 989 B, `methodology-and-learnings.md` 6 338 B (Streichliste vollzogen); `preferences.md` und `ways-of-working.md` mit den Regeln vom 08.10.2026. Kontoweite Datei: Text an den Betreiber (Antwort 07:47), ob abgeschickt, ist nicht gemessen.
- **Nummern:** nächster Mac-Auftrag TB-142 (Wächter-Reparatur); Journal: EJ trägt TB-141, danach EK; Fable vergibt ab R84; Fehler ab 24; die nächste Fable-Anfrage trägt das Datum des Sendetags und geht an einen neuen Fable-Chat.

### Block 4 — Offene Punkte, in Reihenfolge
1. **TB-141 zum Laufen bringen:** messen, ob Schritt 0 committet ist. Wenn nein: per Computer Use (Terminal, Stufe „click“) nachsehen, ob die Startfrage noch steht; Aufgabe an den Betreiber [Mac-pflichtig]: Enter, dann Satz. Danach Nachschau per `send_later`, Abnahme nach der Abgabe (Helfer nach Muster `HELFER_ABNAHME139` im Archiv; Kernzahlen selbst), Schliessen ab 600 s.
2. **TB-142 Wächter-Reparatur** (Fehler 23): Satz ins neu geöffnete claude-Fenster statt ins vorderste Terminal-Fenster; Chrome-Startfrage beim Start beantworten oder abschalten; Erfolgsmeldung erst nach geprüfter Eingabezeile. Vorher: Ziel `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` gegen die Sperrliste prüfen.
3. **TB-137 abnehmen,** sobald der Betreiber das Gesamtergebnis einfügt (Helferauftrag `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilen am Stand `d781f1b`).
4. **Zweite Fable-Anfrage** wie Umzug 07.10.2026, 23:39, Block 4 Nr. 6; dazu Fehler 21 (Register Z. 11727: „48.7 (R39) zu R81 (a)“ neben „(a) und (b)“) zu 55.8 Nr. 10. Vor dem Absenden alle Erinnerungsdateien gegen 27.1 messen (kontoweite Datei erst nach Bestätigung des Betreibers).
5. **Bauauftrag Zellen-Erzeuger** nach R81/R82 erst nach der Fable-Antwort (Bestand `logs/steuernder_chat/ERZEUGER_bestand_R81_R82_bericht.md`; Signalpfad braucht Einzelfreigabe nach 37.3).
6. **Nächster Regelwerk-Nachtrag** (nach TB-141): Regeln vom 08.10.2026 (neuer steuernder Chat beim Umzug wird vom steuernden Chat angelegt; Sitzung nach dem Start selbst ansehen; Erinnerung schreibt nur der steuernde Chat), die 14 Formhinweise aus TB-141, U25 in `UMZUG.md`, W8 und ARBEITSWEISE Z. 97.

### Block 5 — Wartezustände
TB-141 wartet auf den Betreiber (Enter + Satz). TB-137 wartet auf die Cloud-Sitzung und das Einfügen. Kein Fable-Chat hat eine offene Anfrage. Keine Karte offen. Geplante Nachschauen: keine.

### Block 6 — Freigaben und Entscheide des Betreibers am 08.10.2026
- Karte 00:34: W1 „Helfer bauen Entwürfe“, W2 „Nur wörtlicher Auszug“, W7 „Wichtiges ja, Form als Hinweis“ (alle Empfohlen); Vorgaben W4, W5, W6, W8 ohne Widerspruch.
- Karte 07:39 (Streichliste): Live-Parameter „Wert streichen, Verweis lassen“; Zählungen „Zahl streichen, Aussage lassen“; Verworfene „Werte streichen, verworfen bleibt“; Fable-Einschätzung „Streichen“ (alle Empfohlen) — vollzogen.
- Karten zum Umzug: 07:47 „Nach Abgabe von TB-141“; 19:54 „Jetzt umziehen“.
- 08:36 „Lege mir zukünftig immer einen neuen Chat bereit“ → per Karte: der steuernde Chat beim Umzug. 09:22 und 19:11: die Claude-Code-Sitzung für den Mac-Auftrag muss für ihn bereitliegen („so wie es bisher bereits immer gemacht worden ist“).
- **Keine Freigabe** für Registereinträge, Sperrliste, Signalpfad oder Parameterdateien.

### Block 7 — Fehler dieses Chats und die Regeln daraus
- **Nr. 21, 22:** siehe Nachtrag 07:36.
- **Nr. 23:** Der steuernde Chat gab dreimal „Satz abschicken“ aus, gestützt nur auf die Wächter-Zeile „Satz ins Fenster gelegt“; tatsächlich lag der Satz in einer bash-Shell, und die claude-Sitzung hing an der Chrome-Startfrage. Der Betreiber fand den ganzen Tag keine Sitzung. ⇒ Nach jedem Start das claude-Fenster selbst ansehen (Computer Use, nur lesen/klicken); „Satz abschicken“ erst, wenn die Eingabezeile steht; sonst die genaue Handlung am Mac als Aufgabe.
- **Ampel:** 29 759 (23:53) → 101 308 (00:33) → 180 609 (07:38) → 208 294 (07:47) → 302 222 (19:54), bei 14 Helfern. Teuer waren Nachschauen und Fehlersuche am Ende, nicht die Helfer.
- **Getragen hat:** Bausteindateien für Helfer, zwei getrennte Gegenleser plus zweite Runde (8 A gefunden), Simulation unter Python 3.9, Byte-Abgleich beim Schreiben der Erinnerung.

### Block 8 — Zwischengelagert
Unter `logs/steuernder_chat/` (ignoriert): `TB-139_ABNAHME_bericht.md`, `TB-139_ABLAGE_bericht.md`, `TB-139_ERINNERUNG_karte_bericht.md`, `TB-139_ERINNERUNG_suche_zwei_bericht.md`, `TB-141_KARTE_W_bericht.md`, `TB-141_BAU141_bericht.md`, `TB-141_GEGEN141_1/2/3_bericht.md`, `ERZEUGER_bestand_R81_R82_bericht.md`, Archive `2026-10-08_sc_auftraege_berichte.tar.gz` und `2026-10-08_sc_tb141.tar.gz` (Bausteine, Helferaufträge, Bau TB-141 samt Simulation). `$HOME/sc/` der Geräteanbindung verfällt mit diesem Chat (Streichplan und Soll-Dateien darin sind vollzogen).

### Block 9 — Eröffnungstext
Als Kopierblock im Chat ausgegeben und als neuer Chat angelegt (einmalige geplante Aufgabe mit dem Rechner). Wortlaut:

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt. Diesen Chat hat der vorige steuernde Chat für dich angelegt (Betreiber 08.10.2026: „Lege mir zukünftig immer einen neuen Chat bereit“).

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Ist kein Ordner verbunden, fordere die Freigabe für ~/trading-bot an (device_request_folder_access). Wenn das nicht geht, sag es ausdrücklich. git über die Brücke nur mit --no-optional-locks und nur rev-parse, log, show, ls-files, worktree list — nie git status, kein git diff, kein git check-ignore. Geänderte Dateien misst du mit ls-files -m, Unverfolgtes mit ls-files -o --exclude-standard. Uhrzeiten über die Brücke mit TZ=Europe/Berlin date.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter:
1. docs/projektfuehrung/UEBERGABE.md — ab der Überschrift „## Umzug 08.10.2026, 19:58“ bis Dateiende (alle neun Blöcke). Den Nachtrag 08.10.2026, 07:36 davor und den Umzugsblock 07.10.2026, 23:39 nur bei Bedarf.
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
Nur wenn die Geräteanbindung fehlt: dieselben Stellen über den Projects-Zugriff (projektfuehrung/…).

Grosse Dateien über Helfer; Helferaufträge als Bausteindateien auf dem Gerät (Vorbild: sc/auftraege/ im Archiv logs/steuernder_chat/2026-10-08_sc_tb141.tar.gz), Berichte auf rund 3 KB begrenzt; Helfer bauen Entwürfe ausserhalb des Repos, ein frischer Gegenleser ist Pflicht (W1); Erinnerungsdateien schreibt nur der steuernde Chat selbst (Helfer haben kein memory_str_replace). Die Umzugsampel misst du mit docs/werkzeuge/ampel.py auf deinem eigenen Sitzungsprotokoll (~/.claude/projects/*/<sitzung>.jsonl; ampel.py per device_stage_files holen). Messungen bündeln, Helfer parallel starten.

Umgezogen wird nur, wenn ich es sage oder genehmige. Beim Umzug legst du mir den neuen steuernden Chat selbst an (einmalige geplante Aufgabe mit dem Rechner, Eröffnungstext als erste Nachricht) und gibst den Eröffnungstext zusätzlich als Kopierblock aus.

Arbeite selbstständig (Betreiber 07.10.2026, 19:44). Karten nur für echte Betreiberentscheide, als letzter Schritt; vor einer Karte alles Unabhängige anstossen. Aufgaben an mich nur, wo meine Hand nötig ist, je [ortsunabhängig] oder [Mac-pflichtig].

Achtung, das Wichtigste (Einzelheiten in den neun Blöcken):
1. TB-141 (Regelwerk-Nachtrag) liegt startklar im Arbeitsbaum: Auftrag docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md (unverfolgt), Zeiger und UEBERGABE.md geändert. Die Claude-Code-Sitzung auf dem Mac läuft seit 08.10.2026, 09:24 (PID 3242), hing aber an der Chrome-Startfrage von Claude Code; ich muss dort Enter drücken und den Satz einfügen. Miss zuerst, ob Schritt 0 committet ist; wenn ja: Nachschau per send_later, Abnahme nach der Abgabe (Helfer, Kernzahlen selbst), schliessen ab 600 s.
2. Fehler Nr. 23: Der Sitzungswächter meldet „Satz ins Fenster gelegt“, legt den Satz aber ins falsche Terminal-Fenster (eine bash-Shell; dort steht „-bash: TB-141:: command not found“, ebenso TB-132 bis TB-140). Nach jedem Start siehst du selbst nach (Computer Use, Terminal nur Stufe „click“: app_list_windows, app_screenshot des Fensters mit „claude“ im Titel), ob die Sitzung ohne Startfrage an der Eingabezeile steht, bevor du mir „Satz abschicken“ gibst. Den Wächter repariert ein eigener Mac-Auftrag (TB-142) nach TB-141.
3. Ich habe am 08.10.2026 viermal gerügt, dass keine Claude-Code-Sitzung für mich bereitlag. Die Sitzung muss für mich in der App sichtbar und eingabebereit sein.
4. Danach: TB-137 abnehmen, sobald ich das Gesamtergebnis einfüge; zweite Fable-Anfrage (wartet auf TB-137); Bauauftrag Zellen-Erzeuger erst nach Fable.

Sag mir in wenigen Sätzen, was du verstanden hast, und fang in derselben Antwort mit dem ersten Handwerksschritt an. Am Ende jeder Antwort: Kopierblock für die Claude-Code-Sitzung (Wortlaut aus logs/sitzungswaechter/letzter_satz.txt), dann die Zeile mit der Umzugsampel.
```

## Nachtrag 08.10.2026, 21:47 — neuer steuernder Chat (Übernahme 20:01): TB-141 gelaufen, abgenommen, Sitzung geschlossen; Ursache von Fehler Nr. 23; neue Regel zum Start

- **Übernahme:** Gerätefreigabe `~/trading-bot` 20:02; Kernlektüre gelesen. Fenster 20771 stand um 20:14, 20:53 und 21:20 an der Startfrage „Claude in Chrome extension detected“; ein Linksklick des steuernden Chats blieb ohne Wirkung. Der Betreiber gab den Satz um ca. 20:28 in die bash-Shell und in eine Cloud-Sitzung (beides ohne Wirkung), schloss um ca. 21:23 alle Terminal-Fenster (Sonde 21:23:37: 0 claude-Prozesse), öffnete ein neues und startete die Sitzung von Hand (`cd ~/trading-bot && claude --effort high --remote-control`, dann der Satz).
- **TB-141:** Commits `f7d57d4` (Schritt 0, 21:26:37), `7988ce6` (A), `febde0e` (C), `ab362b0` (Abgabe, Journal EJ), `5ed3827` (D3, 21:28:59); HEAD = `origin/main` = `5ed3827e32dc7592a08cc54283893173b459b45e`; Arbeitsbaum leer. **Abgenommen** (Helfer ABNAHME141, Kernzahlen vom steuernden Chat mit eigenen Befehlen nachgemessen): `ARBEITSWEISE.md` 2 413 → 2 471 (58/0), `BACKLOG.md` 349 → 362 (13/0), `JOURNAL.md` 10 528 → 10 578 (50/0 = 35 + 3 + 11 + 1), `UEBERGABE.md` und `UMZUG.md` unverändert; E1–E26 je genau einmal an HEAD, 0 an ⟨S0⟩; 10/10 Prüfanker; Skript bytegleich zum Anhang A; `d3_porcelain.txt` 0 B; EJ einmal, EK frei.
- **Anmerkungen zur Abnahme:** (1) `rc` steht in keiner Belegdatei, nur im Ergebnis und im Journalblock (Ergebnis nennt es). (2) Ergebnis Z. 5 nennt Abgabe- und D3-Commit ohne Hash; Z. 21 Ist-Spalte D3 nur als Verweis. (3) Vier von zehn Prüfankern sind in den Belegen auf 60 Zeichen gekürzt. (4) `c3_vergleich.txt` nennt die Leerzeilen der Form Block nicht eigens; eigene Messung E21, E24, E25, E26 je 1/1. (5) Auftrag Z. 99: „vier Zeilen“ zu E22, der Block hat fünf (Zählfehler des steuernden Chats im Auftrag; von der Sitzung gemeldet, eingefügt ist der Text unverändert). Nicht gemessen: zweites porcelain nach D3, `cmp` gegen `$TMPDIR`. Bericht: `logs/steuernder_chat/TB-141_ABNAHME_bericht.md` (21 871 B, md5 `6892e4c5cbdd7addbafa87c5e111d3d8`).
- **Sitzung geschlossen** über `schliesse_5ed3827e…` um 21:47:23 (Alter 1 099 s; PID 23068, „1 Sitzung(en) mit TERM beendet, 0 noch da“). Im Fenster stand zuletzt ein Angebot von Claude Code („Teach auto mode about your environment?“), unbeantwortet.
- **Ursache von Fehler Nr. 23** (`docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`, Stand `d4a28e9`): Z. 325–329 `set neu to do script …`, danach `return id of window 1`; `neu` wird nicht verwendet, gemeldet wird das vorderste Fenster. Z. 337–339 feste Wartezeit 20 s, keine Prüfung des Fensterinhalts. Z. 347–357 `do script "$SATZ" in window id $FENSTER`, geprüft wird nur der Rückgabewert. `waechter.log`: 20 Starts in Folge mit Fenster 15501 seit 29.09.2026, 15:39:35Z (TB-123). Bestand für TB-142: `logs/steuernder_chat/TB-142_BESTAND_WAECHTER_bericht.md` (md5 `527286875d4581c47fe647bf188bc70d`). Sperrlistennähe: keine `deny`-/`ask`-Regel trifft den Ordner; Register 36.3/37.3 nennen ihn nicht; Auftrag TB-125 Z. 369–371: „Handwerk mit Freigabe, weil der Wächter geändert wird“. Claude-Code-Doku: Schalter `--no-chrome` ist dokumentiert; ob er die Startfrage unterdrückt, ist nicht dokumentiert.
- **Neue Regel (Betreiber 08.10.2026, 21:26, „zukünftig“, „Merke dir das für die Zukunft“):** „`cd ~/trading-bot && claude --effort high --remote-control` + enter sollst du zukünftig immer ausführen und mir lediglich den Text schicken mit der Anweisung.“ Eingetragen in die Projekt-Erinnerung (`ways-of-working.md`, 21:27); `ARBEITSWEISE.md` trägt sie mit dem nächsten Mac-Auftrag. Weg des steuernden Chats: der Sitzungswächter (Terminal bleibt Stufe „click“); TB-142 muss ihn so richten, dass die Sitzung eingabebereit und für den Betreiber sichtbar dasteht.
- **Nummern:** Journal: nächste Kennung EK; nächster Mac-Auftrag TB-142; Fehler ab 24. **Offen beim Betreiber:** Text für die kontoweite Erinnerung (Antwort 07:47), Gesamtergebnis TB-137. Geplante Nachschauen: keine.

## Umzug 08.10.2026, 22:03 — Stand für den neuen steuernden Chat (alle neun Blöcke; die Abnahme von TB-141 und die Ursache von Fehler Nr. 23 trägt der Nachtrag 21:47 unmittelbar davor)

Betreiber: Karte, beantwortet 08.10.2026 zwischen 21:52 und 22:02: „Jetzt umziehen (Empfohlen)“. Ampel 21:52: Verlauf 214 595 (Grundlast 123 426), gelb. **Dieser Block ersetzt den Umzugsblock vom 08.10.2026, 19:58.** Den neuen Chat legt der steuernde Chat selbst an.

### Block 1 — Stand in drei Zeilen
- **TB-141 ist abgegeben, abgenommen und in der Ablage;** die Sitzung ist geschlossen (21:47:23), es läuft keine Claude-Code-Sitzung.
- **TB-142 (Wächter-Reparatur) ist vorbereitet, nicht gebaut:** Bestand und Vorgaben liegen vor; die Einzelfreigabe des Betreibers steht aus.
- **Offen beim Betreiber:** Text für die kontoweite Erinnerung (Antwort 07:47 des Chats vor dem Umzug 19:58) abschicken; Gesamtergebnis TB-137 einfügen.

### Block 2 — HEAD und Arbeitsbaum
HEAD = `origin/main` = `5ed3827e32dc7592a08cc54283893173b459b45e` (gemessen 22:02). Geändert: nur `docs/projektfuehrung/UEBERGABE.md` (Nachtrag 21:47 und dieser Block). Unverfolgt: nichts. `AKTUELLER_AUFTRAG.md` zeigt noch auf TB-141. Terminal auf dem Mac (22:02): ein Fenster (window_id 21040, Vollbild), darin die beendete Sitzung von TB-141; die Fenster 15501 und 20771 gibt es nicht mehr (Betreiber schloss um ca. 21:23 alle Fenster). Wächter-Log, letzte Zeile: „fertig (schliessen)“ 19:47:23Z.

### Block 3 — Tragende Zahlen
- **Regelwerk nach TB-141:** `ARBEITSWEISE.md` 2 471 Zeilen, 172 847 B (Abschnitt 0: 37 017 B); `BACKLOG.md` 362 Zeilen, 86 284 B; `JOURNAL.md` 10 578 Zeilen, letzter Block EJ.
- **Register** unverändert: 11 733 Zeilen, 998 257 B, Abschnitte 0–55, höchster Block R83.
- **Ablage:** 106 Einträge, 57,3 % (Helfer ABLAGE141, 21:5x: `ARBEITSWEISE.md`, `BACKLOG.md`, `UEBERGABE.md` ersetzt); `UEBERGABE.md` wird mit diesem Block noch einmal erneuert. `JOURNAL.md` liegt nicht in der Ablage.
- **Projekt-Erinnerung:** `ways-of-working.md` trägt die Regel vom 08.10.2026, 21:26 (3 378 B); `preferences.md` trägt seit 20:28 die Zeile „Nach jedem Start sieht der steuernde Chat selbst im Terminal-Fenster … nach“ (10 886 B).
- **Nummern:** nächster Mac-Auftrag TB-142; Journal: nächste Kennung EK; Fable vergibt ab R84; Fehler ab 25; die nächste Fable-Anfrage trägt das Datum des Sendetags und geht an einen neuen Fable-Chat.

### Block 4 — Offene Punkte, in Reihenfolge
1. **TB-142 bauen** nach `logs/steuernder_chat/TB-142_VORGABEN.md` (6 891 B, md5 `022ef7fba702ea528566c06a4c704e58`; V1 Fenster aus dem Tab, V2 `--no-chrome` nach Probe, V3 Prüfung des Fensterinhalts statt Wartezeit, V4 der Wächter legt den Satz nicht mehr ins Fenster, V5 Fenster merken und aufräumen, V6 Probe ohne Auftrag, V7 `LIESMICH.md` und zwei Zeilen in ARBEITSWEISE Abschnitt 0, V8 Backlog und Journal, V9 nicht in TB-142). Bestand: `logs/steuernder_chat/TB-142_BESTAND_WAECHTER_bericht.md`. Bauart: Helfer nach Vorbild `HELFER_BAU141.md` (Archiv `2026-10-08_sc_tb141.tar.gz`), Entwurf ausserhalb des Repos, Simulation des Einfügeskripts, zwei getrennte Gegenleser. Dann **eine Karte: Einzelfreigabe** (Wächter wird geändert, TB-125 Z. 369–371; V4 ausdrücklich). Erst nach dem Ja: Auftrag und Zeiger in den Arbeitsbaum, md5 prüfen.
2. **Start von TB-142:** nicht über `starte_TB-142`, solange der alte Wächter läuft (Block 7, zweiter Punkt). Vorgabe: Der Betreiber startet dieses eine Mal noch von Hand, so wie am 08.10.2026 um 21:26 gelungen — neues Terminal-Fenster, Startzeile `cd ~/trading-bot && claude --effort high --remote-control`, bei einer Frage Enter, dann der Satz. Ihm ausdrücklich sagen, dass das von seiner Regel 21:26 abweicht und warum, in einfacher Sprache, ein Handgriff je Schritt.
3. **Nach der Abgabe von TB-142:** Abnahme (Helfer nach Muster `HELFER_ABNAHME141.md`, Kernzahlen selbst), Schliessen ab 600 s; danach der erste echte Start über den reparierten Wächter als Probe, mit eigenem Blick ins Fenster.
4. **TB-137 abnehmen,** sobald der Betreiber das Gesamtergebnis einfügt (Helferauftrag `logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilen am Stand `d781f1b`).
5. **Zweite Fable-Anfrage** wie Umzug 07.10.2026, 23:39, Block 4 Nr. 6; dazu Fehler 21 zu 55.8 Nr. 10. Vor dem Absenden alle Erinnerungsdateien gegen 27.1 messen.
6. **Bauauftrag Zellen-Erzeuger** nach R81/R82 erst nach der Fable-Antwort (Signalpfad braucht Einzelfreigabe nach 37.3).
7. **Nächster Regelwerk-Nachtrag:** die Posten aus Umzug 08.10.2026, 19:58, Block 4 Nr. 6; dazu Fehler Nr. 24 und die Regeln aus Block 7 dieses Blocks, soweit TB-142 sie nicht trägt.

### Block 5 — Wartezustände
Keine Mac-Sitzung läuft. TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Kein Fable-Chat hat eine offene Anfrage. Keine Karte offen. Geplante Nachschauen: keine.

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat (08.10.2026, 20:01 bis 22:02)
- 21:26, „zukünftig“, „Merke dir das für die Zukunft“: Den Start der Claude-Code-Sitzung (`cd ~/trading-bot && claude --effort high --remote-control` + Enter) führt der steuernde Chat immer selbst aus; der Betreiber bekommt lediglich den Text mit der Anweisung.
- Karte nach 21:52: „Jetzt umziehen (Empfohlen)“.
- Vorgabe V4 (Wächter legt den Satz nicht mehr ins Fenster) ist dem Betreiber um 21:52 als Vorgabe genannt; bis 22:02 kein Widerspruch. **Keine Freigabe** für TB-142, für Registereinträge, Sperrliste, Signalpfad oder Parameterdateien.

### Block 7 — Fehler dieses Chats und die Regeln daraus
- **Nr. 24 (steuernder Chat, 20:25 und 20:54):** Die Aufgabe verlangte vom Betreiber, unter fünf Terminal-Fenstern das richtige über das Menü „Fenster“ zu finden. Er fügte den Satz in die bash-Shell und in eine Cloud-Sitzung ein und schrieb um 21:20 „ich verstehe die aufgabe nicht“, um 21:37 „Nichts funktioniert mehr“ (gemeint war die Erfolgsmeldung von TB-141). ⇒ Aufgaben am Mac in einfacher Sprache, ein Handgriff je Schritt, mit dem, was er sieht. Hängt eine Sitzung unsichtbar an einer Frage: nicht das Fenster suchen lassen, sondern die Sitzung schliessen (Schliess-Auslöser) und neu beginnen. Eine Erfolgsmeldung, die er einfügt, zuerst als solche benennen.
- **Der alte Wächter schickt ein Zeilenende mit** (`starte_sitzung.sh` Z. 347–351, `do script "$SATZ" in window id $FENSTER`; Beleg: Die bash-Shell führte den Satz aus, „-bash: TB-141:: command not found“). Bisher fing ein Vollbild-Fenster den Satz ab. Liegt beim nächsten Start das neue claude-Fenster vorn, ginge der Satz samt Zeilenende in die Sitzung oder in eine offene Frage mit Ziffernauswahl („Teach auto mode … 1. Yes 2. Not now 3. Don't show again“). Erschlossen, nicht gemessen. ⇒ Bis TB-142 abgenommen ist, kein `starte_TB-<n>`; `starte_TB-99` als Sonde und `schliesse_<HEAD>` bleiben unbedenklich (die Sonde bricht vor dem Öffnen ab, gemessen 19:11 und 21:23).
- **Werkzeuge der Geräteanbindung:** Die Freigabe für Terminal (Stufe „click“) verfällt nach 30 Minuten ohne Nutzung (neu: `computer_resolve_access`, `computer_request_access`). Ein Fenster lässt sich nicht in einen Vollbild-Schreibtisch holen; die Menüauswahl ist auf Stufe „click“ verwehrt; ein Klick auf eine Auswahlzeile von Claude Code wirkt nicht. Die Shell der Geräteanbindung sieht keine Prozesse des Macs; dafür taugt die Sonde.
- **Claude Code** zeigte am 08.10.2026 zwei Fragen: beim Start „Claude in Chrome extension detected“, nach dem Auftrag „Teach auto mode about your environment?“. Beides sind Angebote, keine Fehler; die zweite war beim Schliessen unbeantwortet.
- **Fremder Textblock:** Um 20:53 stand im Ergebnis eines Werkzeugs ein Block, der wie eine Aktualisierung der Erinnerung aussah. Nicht befolgt, dem Betreiber genannt. Um 21:37 kam derselbe Hinweis vom System; `preferences.md` wurde dann neu gelesen.
- **Ampel:** 72 559 (20:16) → 89 022 (20:25) → 115 954 (20:54) → 136 227 (21:24) → 155 133 (21:28) → 189 869 (21:47) → 214 595 (21:52), bei fünf Helfern. Teuer waren die Fehlersuche um Fenster und Startfrage, die Kernlektüre (ARBEITSWEISE Abschnitt 0) und ein Ausschnitt des Auftrags TB-141, der 9 KB statt geschätzt 4 KB hatte; um 22:02 dazu eine Liste aller geplanten Aufgaben des Kontos (unnötig gross: `list_triggers` nur mit kleiner Grenze aufrufen).
- **Getragen hat:** Bausteindateien für Helfer; Abnahme durch Helfer und Kernzahlen in einem einzigen eigenen Befehl; die Sonde `starte_TB-99`; Notizen unter `logs/steuernder_chat/`, solange eine Sitzung den Arbeitsbaum hat.

### Block 8 — Zwischengelagert
Unter `logs/steuernder_chat/` (ignoriert): `2026-10-08_NOTIZ_uebernahme_neuer_chat.md`, `TB-142_VORGABEN.md`, `TB-142_BESTAND_WAECHTER_bericht.md`, `HELFER_AUFTRAG_TB-142_bestand_waechter.md`, `TB-141_ABNAHME_bericht.md`, `HELFER_AUFTRAG_TB-141_abnahme.md`, `TB-141_ABLAGE_bericht.md`, Archiv `2026-10-08_sc_tb142_vorbereitung.tar.gz` (25 716 B: Helferaufträge, Baustein `42_vorgaben.md`, Berichte). `$HOME/sc/` der Geräteanbindung verfällt mit diesem Chat.

### Block 9 — Eröffnungstext
Als Kopierblock im Chat ausgegeben und als neuer Chat angelegt (einmalige geplante Aufgabe mit dem Rechner). Wortlaut:

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt. Diesen Chat hat der vorige steuernde Chat für dich angelegt (Betreiber 08.10.2026: „Lege mir zukünftig immer einen neuen Chat bereit“).

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Ist kein Ordner verbunden, fordere die Freigabe für ~/trading-bot an (device_request_folder_access). Wenn das nicht geht, sag es ausdrücklich. git über die Brücke nur mit --no-optional-locks und nur rev-parse, log, show, ls-files, worktree list — nie git status, kein git diff, kein git check-ignore. Geänderte Dateien misst du mit ls-files -m, Unverfolgtes mit ls-files -o --exclude-standard. Uhrzeiten über die Brücke mit TZ=Europe/Berlin date.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter:
1. docs/projektfuehrung/UEBERGABE.md — ab der Überschrift „## Umzug 08.10.2026, 22:03“ bis Dateiende (alle neun Blöcke). Den Nachtrag 08.10.2026, 21:47 unmittelbar davor nur bei Bedarf (Abnahme TB-141, Ursache von Fehler Nr. 23).
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“; seit TB-141 rund 37 KB).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
4. logs/steuernder_chat/TB-142_VORGABEN.md (rund 7 KB) — die Vorgaben für den nächsten Mac-Auftrag.
Nur wenn die Geräteanbindung fehlt: die Stellen 1 bis 3 über den Projects-Zugriff (projektfuehrung/…).

Grosse Dateien über Helfer; Helferaufträge als Bausteindateien auf dem Gerät (Vorbilder: sc/auftraege/ in den Archiven logs/steuernder_chat/2026-10-08_sc_tb141.tar.gz und 2026-10-08_sc_tb142_vorbereitung.tar.gz), Berichte auf rund 3 KB begrenzt; Helfer bauen Entwürfe ausserhalb des Repos, ein frischer Gegenleser ist Pflicht (W1); Erinnerungsdateien schreibt nur der steuernde Chat selbst. Die Umzugsampel misst du mit docs/werkzeuge/ampel.py auf deinem eigenen Sitzungsprotokoll (~/.claude/projects/*/<sitzung>.jsonl; ampel.py per device_stage_files holen). Messungen bündeln, Helfer parallel starten.

Umgezogen wird nur, wenn ich es sage oder genehmige. Beim Umzug legst du mir den neuen steuernden Chat selbst an (einmalige geplante Aufgabe mit dem Rechner, Eröffnungstext als erste Nachricht) und gibst den Eröffnungstext zusätzlich als Kopierblock aus.

Arbeite selbstständig (Betreiber 07.10.2026, 19:44). Karten nur für echte Betreiberentscheide, als letzter Schritt; vor einer Karte alles Unabhängige anstossen. Aufgaben an mich nur, wo meine Hand nötig ist, je [ortsunabhängig] oder [Mac-pflichtig].

Achtung, das Wichtigste (Einzelheiten in den neun Blöcken):
1. TB-141 ist abgegeben, abgenommen und in der Ablage; die Sitzung ist geschlossen, es läuft keine Claude-Code-Sitzung. Als Nächstes baust du TB-142 (Wächter-Reparatur, Fehler Nr. 23) nach den Vorgaben: Ein Helfer baut den Entwurf ausserhalb des Repos, zwei frische Gegenleser, dann eine Karte an mich für die Einzelfreigabe (der Wächter wird geändert; Vorgabe V4 dabei ausdrücklich nennen).
2. Ich habe am 08.10.2026, 21:26, entschieden: Den Start der Claude-Code-Sitzung (cd ~/trading-bot && claude --effort high --remote-control + Enter) führst du zukünftig immer selbst aus, ich bekomme lediglich den Text mit der Anweisung. Dein Weg dafür ist der Sitzungswächter. Er ist bis zur Abnahme von TB-142 defekt: Löse keinen starte_-Auslöser aus, bevor du Block 7 gelesen hast (der Wächter legt den Satz samt Zeilenende ins vorderste Terminal-Fenster). Für den Start von TB-142 selbst gilt Block 4 Nr. 2.
3. Aufgaben am Mac gibst du mir in einfacher Sprache: ein Handgriff je Schritt, mit dem, was ich auf dem Bildschirm sehe. Am 08.10.2026 habe ich eine Aufgabe nicht verstanden und den Satz in falsche Fenster eingefügt (Fehler Nr. 24).
4. Danach: TB-137 abnehmen, sobald ich das Gesamtergebnis einfüge; zweite Fable-Anfrage (wartet auf TB-137); Bauauftrag Zellen-Erzeuger erst nach Fable.

Sag mir in wenigen Sätzen, was du verstanden hast, und fang in derselben Antwort mit dem ersten Handwerksschritt an. Am Ende jeder Antwort: Kopierblock für die Claude-Code-Sitzung (Wortlaut aus logs/sitzungswaechter/letzter_satz.txt; ist kein Auftrag startklar, steht das dort), dann die Zeile mit der Umzugsampel.
```

## Nachtrag 09.10.2026, 01:32 — neuer steuernder Chat (Übernahme 08.10.2026, 23:00): TB-142 gebaut und gegengelesen (Entwurf v5); Einzelfreigabe per Karte gestellt

- **Übernahme:** Geräteanbindung nach Ordnerfreigabe (`device_request_folder_access` für `~/trading-bot`); HEAD `5ed3827e32dc7592a08cc54283893173b459b45e`, `BACKLOG.md` 362 Zeilen (gemessen 08.10.2026, 23:00); Kernlektüre aus dem Repo.
- **Auftrag TB-142, Entwurf v5:** `logs/steuernder_chat/TB-142_entwurf_v5.md`, 75 940 B, 1 070 Z., md5 `f220aed1c76d7b146a25da330af5b09c`; Platzhalter `<<FREIGABE_WORTLAUT>>` einmal (Z. 14); Werkzeug sha256 `e1c4c427911b97a59715fc11b767847f4ffbcbd7803f28e409df3067ff829c70`. Gebaut aus Bausteinen (`bau/bauen.py`), Prüfung `sim/pruef.py`: 156 ok, 0 NEIN. Archiv mit Bausteinen, Helferaufträgen, Berichten und `ablegen_tb142.py`: `logs/steuernder_chat/2026-10-09_sc_tb142_bau.tar.gz`.
- **Lauf:** BAU142 (v1, 69 026 B) → GEGEN142_1 (9 A, 18 B) und GEGEN142_2 (4 A, 19 B) → BERICHT142 (v2: alle 13 A, neun B) → BERICHT142b (v3: fünf Entscheide des steuernden Chats, darunter die Teilabgabe) → GEGEN142_3 (Nachlese: 0 A, „startbar“) → v4 (steuernder Chat: fünf Zeilen nach B2, B3, B5, B9 und der Vorgabe zur Probe) → GEGEN142_4 (0 A, 9 B) → v5 (steuernder Chat: vier Zeilen nach GEGEN142_4; nur mit `pruef.py` und `diff` geprüft, **kein** weiterer Gegenleser). Berichte: `logs/steuernder_chat/TB-142_*_bericht.md`.
- **Sollwerte im Auftrag** (an Kopien mit GNU `diff` gezählt; Teilmessung: Linux, bash 5.1, Python 3.10, nichts vom Mac): `starte_sitzung.sh` nach Schritt A 357 Z. (`9 15`), nach Schritt C 622 Z. (`293 34`) · `LIESMICH.md` `65 0` · `ARBEITSWEISE.md` `6 0`, mit geänderter Startzeile `7 0` · `BACKLOG.md` `11 0` · Journal: Block EK + 6 + 1 + 3.
- **Vorgaben des steuernden Chats in diesem Bau (Handwerk; in der Karte genannt):** Probe über einen eigenen Auslöser `probe_<PID>` (dritter Auslösertyp; läuft nur, wenn im Repo genau die genannte Sitzung arbeitet) statt `WAECHTER_PROBE=1` — die plist reicht keine Variablen durch · V4 als Schritt A mit eigenem Commit · „eingabebereit“ erst nach zwei Lesungen in Folge · `--no-chrome` kommt in die Startzeile, wenn die Messung es trägt (dann weicht die Startzeile vom Betreiberwortlaut 08.10.2026, 21:26 ab) · Teilabgabe als erlaubter Ausgang, wenn kein Merkmal der Eingabezeile messbar ist · je widersprochener Stelle eine Zeile „Gilt seit TB-142“ (ARBEITSWEISE vier, mit geänderter Startzeile fünf; LIESMICH drei).
- **Wichtig bis zur Abgabe von TB-142:** Die Zeilen 2185–2189 dieser Datei (Nachtrag 08.10.2026, 21:47) nicht ändern — das Werkzeug prüft ihre md5, `doku` endet sonst mit rc 3 (md5 über die fünf Zeilen bei diesem Nachtrag: `eb6a8513c664c9d9c319af32520c3e47`). Nachträge nur anhängen.
- **Nach dem Ja:** Freigabewortlaut in eine Datei, dann `python3 -B ablegen_tb142.py <repo> <freigabe.txt> '<TT.MM.JJJJ, HH:MM>'` (prüft erst, schreibt dann; an Kopien geprobt: Zeiger Z. 39 und 52, `letzter_satz.txt` auf TB-142, Auftrag nach `docs/auftraege/MAC_TB-142_waechter_reparatur.md`); md5 nachmessen. Start von Hand nach Umzug 08.10.2026, 22:03, Block 4 Nr. 2; kein `starte_TB-142`.
- **Dem Betreiber vor dem Start sagen:** Die Sitzung öffnet mindestens vier Probesitzungen (zwei Testfenster, zwei Probeläufe), die kurz in der Claude-App erscheinen; bleibt ein Fenster mit einer Rückfrage offen, steht es als Aufgabe im Ergebnis.
- **Formhinweise, die im Auftrag stehen bleiben (W7):** Grössenziel 45 KB verfehlt · der Commit-Betreff von Schritt 0 nennt den 08.10.2026 · Kopf Z. 3 nennt zwei Gegenleser · 12 Log-Zeilen des Skripts stehen nicht in der LIESMICH · Rohlesungen bleiben in `$TMPDIR` · übrige B in den Berichten.
- **Fehler dieses Chats:** keiner mit Nummer. Beobachtung: Einem Helfer fiel die Geräteanbindung nach 13 Aufrufen weg („device not connected“), während ein zweiter weiterlief; sein Auftrag lief als frischer Helfer neu ⇒ Helfer schreiben den Bericht nach jeder Prüfung fort und versuchen dreimal neu (so in den Helferaufträgen ab GEGEN142_2).
- **Ampel (gemessen unmittelbar vor diesem Nachtrag):** Verlauf 189 014 (Grundlast 128 002), grün, knapp unter gelb; die Karte fragt den Umzug nach dem Start von TB-142 mit an.

## Nachtrag 09.10.2026, 06:52 — Einzelfreigabe für TB-142 erteilt; Auftrag und Zeiger im Arbeitsbaum; Start von Hand durch den Betreiber

Karte, gestellt nach 01:32, beantwortet vor 06:50: Einzelfreigabe „Freigeben wie gebaut (Empfohlen)“ (mit V4, dem Auslöser `probe_<PID>` und `--no-chrome`, falls die Messung es trägt); Umzug „Nach dem Start umziehen (Empfohlen)“. Abgelegt mit `ablegen_tb142.py` (gemessen 06:50): `docs/auftraege/MAC_TB-142_waechter_reparatur.md` 76 899 B, 1 070 Z., md5 `c3de8bbe0edaa9cd1e4b0d2f49da6b24` (Entwurf v5 mit dem Freigabewortlaut in Z. 14; Werkzeug sha256 aus dem abgelegten Auftrag `e1c4c427911b97a59715fc11b767847f4ffbcbd7803f28e409df3067ff829c70`, wie Soll) · `docs/auftraege/AKTUELLER_AUFTRAG.md` 8 015 B, md5 `69cb176af32ad68f396511a7fbb1697a` (Z. 39 und 52) · `logs/sitzungswaechter/letzter_satz.txt` auf TB-142. Arbeitsbaum: geändert `UEBERGABE.md`, `AKTUELLER_AUFTRAG.md`; unverfolgt der Auftrag — wie 0a es verlangt. Kein `starte_TB-142`.

## Umzug 09.10.2026, 06:52 — Stand für den neuen steuernden Chat (alle neun Blöcke; den Bau von TB-142 trägt der Nachtrag 09.10.2026, 01:32, die Freigabe der Nachtrag unmittelbar davor)

Betreiber: Karte, beantwortet vor 06:50: „Nach dem Start umziehen (Empfohlen)“. Ampel 06:50: Verlauf 210 548 (Grundlast 128 002), gelb. **Dieser Block ersetzt den Umzugsblock vom 08.10.2026, 22:03.** Er ist vor dem Start geschrieben, weil der steuernde Chat nach Schritt 0 nichts im Arbeitsbaum anfasst; den neuen Chat legt der steuernde Chat an, sobald Schritt 0 von TB-142 committet ist.

### Block 1 — Stand in drei Zeilen
- **TB-142 ist freigegeben und liegt im Arbeitsbaum** (Auftrag, Zeiger). Der Betreiber startet die Sitzung dieses eine Mal von Hand; dass sie arbeitet, zeigt der Commit „TB-142 Schritt 0“.
- **Danach:** Abnahme TB-142, Schliessen ab 600 s, erster echter Start über den reparierten Wächter als Probe.
- **Offen beim Betreiber:** Text für die kontoweite Erinnerung abschicken; Gesamtergebnis TB-137 einfügen.

### Block 2 — HEAD und Arbeitsbaum
Beim Schreiben (06:5x): HEAD = `5ed3827e32dc7592a08cc54283893173b459b45e`; geändert `docs/projektfuehrung/UEBERGABE.md`, `docs/auftraege/AKTUELLER_AUFTRAG.md`; unverfolgt `docs/auftraege/MAC_TB-142_waechter_reparatur.md`. Schritt 0 committet genau diese drei. Danach fasst der steuernde Chat im Arbeitsbaum nichts an, bis die Sitzung abgegeben hat (`logs/steuernder_chat/` ist ignoriert und bleibt benutzbar). Die Terminal-Fenster des Macs hat dieser Chat nicht angesehen (kein Computer Use in diesem Chat). Wächter-Log, letzte Zeile beim Umzug 22:03: „fertig (schliessen)“ 19:47:23Z; seither kein Auslöser von diesem Chat.

### Block 3 — Tragende Zahlen
- **Auftrag TB-142:** Zahlen im Nachtrag unmittelbar davor; Sollwerte der Sitzung im Nachtrag 01:32 (`starte_sitzung.sh` nach Schritt A 357 Z. `9 15`, nach Schritt C 622 Z. `293 34`; `LIESMICH.md` `65 0`; `ARBEITSWEISE.md` `6 0`, mit `--no-chrome` `7 0`; `BACKLOG.md` `11 0`; Journal Block EK + 6 + 1 + 3).
- **Regelwerk vor TB-142:** `ARBEITSWEISE.md` 2 471 Zeilen, `BACKLOG.md` 362, `JOURNAL.md` 10 578 (letzter Block EJ), `starte_sitzung.sh` 363, `LIESMICH.md` 304; Register unverändert (höchster Block R83).
- **Ablage:** 106 Einträge; `UEBERGABE.md` mit diesem Block erneuert. Nach TB-142 sind `ARBEITSWEISE.md`, `BACKLOG.md` und `UEBERGABE.md` zu erneuern (Helfer).
- **Nummern:** nächster Mac-Auftrag TB-143; Journal: TB-142 schreibt EK, danach die nächste Kennung; Fable vergibt ab R84; Fehler ab 25; die nächste Fable-Anfrage trägt das Datum des Sendetags und geht an einen neuen Fable-Chat.

### Block 4 — Offene Punkte, in Reihenfolge
1. **Stand der Sitzung messen:** `git --no-optional-locks log -8 --format='%h %ci %s'`. Arbeitet sie, eine Nachschau per `send_later` (unter einer Stunde). Drei Ausgänge: volle Abgabe (`docs/ERGEBNIS_TB-142_waechter_reparatur.md`), **Teilabgabe** (nur V4, wenn kein Merkmal der Eingabezeile messbar war; dann nennt das Ergebnis als Erstes die Frage, die der Betreiber einmal beantworten muss) oder ABBRUCH (`docs/belege/TB-142/abbruch.txt`).
2. **Abnahme TB-142:** Helfer nach Muster `HELFER_ABNAHME141.md`; Kernzahlen selbst in einem Befehl (numstat gegen die Sollwerte aus Block 3; im Skript genau ein `do script`, 0 × ` in window`, `keystroke`, `System Events`; Probe-Logs `d_probe<i>_log.txt`; `messwerte.txt`; porcelain leer). Geänderte Startzeile (`--no-chrome`) dem Betreiber ausdrücklich nennen. Aufgaben für den Betreiber aus dem Ergebnis in einfacher Sprache weitergeben. Schliessen ab 600 s; das von Hand geöffnete Fenster der Sitzung bleibt danach offen (es ist nicht gemerkt) — dem Betreiber sagen.
3. **Nach der Abnahme:** der erste echte Start über den reparierten Wächter als Probe (W5 und W6 liefen in TB-142 nie), mit eigenem Blick ins Fenster; dann `preferences.md` der Projekt-Erinnerung anpassen (Zeile „Wächter-Log ‚Satz ins Fenster gelegt‘ prüfen“ → die neuen Log-Zeilen). Bei einer Teilabgabe oder einem Abbruch: Folgeauftrag TB-143 aus den Bausteinen im Archiv, nicht neu bauen.
4. **TB-137 abnehmen,** sobald der Betreiber das Gesamtergebnis einfügt (`logs/steuernder_chat/HELFER_AUFTRAG_TB-137_abnahme.md`; Zeilen am Stand `d781f1b`).
5. **Zweite Fable-Anfrage** wie Umzug 07.10.2026, 23:39, Block 4 Nr. 6; dazu Fehler 21 zu 55.8 Nr. 10. Vor dem Absenden alle Erinnerungsdateien gegen 27.1 messen.
6. **Bauauftrag Zellen-Erzeuger** nach R81/R82 erst nach der Fable-Antwort (Signalpfad braucht Einzelfreigabe nach 37.3).
7. **Nächster Regelwerk-Nachtrag:** die Posten aus Umzug 08.10.2026, 19:58, Block 4 Nr. 6; Fehler Nr. 24; die Regeln aus Block 7 des Umzugs 22:03 und aus Block 7 hier, soweit TB-142 sie nicht trägt.

### Block 5 — Wartezustände
Mac-Sitzung TB-142: Start durch den Betreiber (Anleitung in der Antwort dieses Chats von 06:5x). TB-137 wartet auf die Cloud-Sitzung und das Einfügen durch den Betreiber. Kein Fable-Chat hat eine offene Anfrage. Keine Karte offen. Geplante Nachschauen: höchstens eine dieses Chats (prüft Schritt 0 und legt dann den neuen Chat an).

### Block 6 — Freigaben und Entscheide des Betreibers in diesem Chat (08.10.2026, 23:00 bis 09.10.2026, 06:50)
- **Einzelfreigabe TB-142:** „Freigeben wie gebaut (Empfohlen)“ — Wortlaut von Frage, Antwort und Beschreibung steht im Auftrag Z. 14. Sie deckt: V4; den neuen Auslöser `probe_<PID>`; `--no-chrome` in der Startzeile, falls die Messung es trägt; die Einfügungen in `LIESMICH.md`, `ARBEITSWEISE.md`, `BACKLOG.md`, `JOURNAL.md`.
- **Umzug:** „Nach dem Start umziehen (Empfohlen)“.
- **Keine Freigabe** für Registereinträge, Sperrliste, Signalpfad oder Parameterdateien. Kein „zukünftig“ des Betreibers in diesem Chat.

### Block 7 — Fehler dieses Chats und die Regeln daraus
- **Kein Fehler mit Nummer.** Eine Uhrzeit (Ampel im Nachtrag 01:32) war zuerst geschätzt und ist im selben Zug berichtigt; die Regel dazu steht schon in Abschnitt 0.
- **Bis TB-142 abgenommen ist, kein `starte_TB-<n>`** (wie Umzug 22:03, Block 7): Der alte Wächter schickt den Satz samt Zeilenende ins vorderste Fenster. Ab dem Commit „TB-142 A“ legt der Wächter keinen Satz mehr in ein Fenster (launchd ruft die Datei aus dem Arbeitsbaum); geprüft ist er erst nach der Abnahme. `starte_TB-99` und `schliesse_<HEAD>` bleiben unbedenklich; während der Mess- und Probephasen zeigt eine Sonde zwei Sitzungen im Repo.
- **Geräteanbindung:** Im neuen Chat war kein Ordner verbunden; `device_request_folder_access` lief erst im zweiten Anlauf (der erste Aufruf wurde nicht ausgeführt). Einem Helfer fiel die Anbindung nach 13 Aufrufen weg („device not connected“), ein zweiter lief gleichzeitig weiter ⇒ Helfer schreiben den Bericht nach jeder Prüfung fort und versuchen dreimal neu; ein abgebrochener Helferauftrag läuft als frischer Helfer neu (Zielordner vorher ansehen).
- **Grössenziel:** 45 KB für den Bauer war gesetzt, nicht gemessen; v1 hatte 69 KB, v5 75,9 KB ⇒ ein Grössenziel aus dem Vorbild gleicher Bauart ableiten (TB-141: 76,6 KB).
- **Berichtigen:** Der Berichtiger arbeitet in den Bausteinen und übernimmt Sollwerte aus der Simulation (`werte.json`), nie von Hand. Kleine Berichtigungen (einzelne Zeilen, kein Sollwert) macht der steuernde Chat per Skript mit `assert` auf genau einen Treffer und lässt einen engen frischen Gegenleser nur diese Zeilen lesen (rund 12 Schritte). Nach v5 kam kein Gegenleser mehr — dem Betreiber vor der Karte gesagt.
- **Getragen hat:** die Nachlese „als Mac-Sitzung durchgehen“ samt Abgleich mit den `deny`-Regeln; Prüfstände der Gegenleser mit Attrappen für `osascript`; Helferantworten auf 3 000 Zeichen, Entscheide an der Tabelle des Berichts gelesen (W6); eine Zwischenmeldung an den Betreiber je abgeschlossener Stufe.
- **Ampel:** Verlauf 189 014 nach Kernlektüre und acht Helferläufen (01:3x), 210 548 nach Karte und Ablegen (06:50). Teuer: Kernlektüre (ARBEITSWEISE Abschnitt 0 mit 37 KB, Umzugsblock, Bestandsausschnitt), die eigenen Helferaufträge (je 5 bis 9 KB) und die Berichtsausschnitte der Gegenleser.

### Block 8 — Zwischengelagert
Unter `logs/steuernder_chat/` (ignoriert): `TB-142_entwurf_v1.md` bis `TB-142_entwurf_v5.md`; `TB-142_BAU142_bericht.md`, `TB-142_GEGEN142_1_bericht.md` bis `TB-142_GEGEN142_4_bericht.md`, `TB-142_BERICHT142_bericht.md`, `TB-142_BERICHT142b_bericht.md`; Archiv `2026-10-09_sc_tb142_bau.tar.gz` (Helferaufträge, Bausteine `sc/tb142/bau/`, `bauen.py`, `pruef.py`, `ablegen_tb142.py`, Berichte); aus dem vorigen Chat weiter `TB-142_VORGABEN.md`, `TB-142_BESTAND_WAECHTER_bericht.md`, `HELFER_AUFTRAG_TB-137_abnahme.md`, `2026-10-08_sc_tb141.tar.gz`, `2026-10-08_sc_tb142_vorbereitung.tar.gz`. `$HOME/sc/` der Geräteanbindung verfällt mit diesem Chat.

### Block 9 — Eröffnungstext
Als Kopierblock im Chat ausgegeben und als neuer Chat angelegt (einmalige geplante Aufgabe mit dem Rechner), sobald Schritt 0 von TB-142 committet ist. Wortlaut:

```
Neue Sitzung zum Trading-Bot-Projekt (steuernder Chat). Das Projekt "Trading Bots" ist angehängt. Diesen Chat hat der vorige steuernde Chat für dich angelegt (Betreiber 08.10.2026: „Lege mir zukünftig immer einen neuen Chat bereit“).

Prüfe als Erstes, ob du über die Geräteanbindung auf ~/trading-bot lesen kannst — nenne mir HEAD, die letzten drei Commits und die Zeilenzahl von docs/projektfuehrung/BACKLOG.md als Beleg. Ist kein Ordner verbunden, fordere die Freigabe für ~/trading-bot an (device_request_folder_access; läuft der Aufruf nicht, in der nächsten Runde noch einmal). Wenn das nicht geht, sag es ausdrücklich. git über die Brücke nur mit --no-optional-locks und nur rev-parse, log, show, ls-files, worktree list — nie git status, kein git diff, kein git check-ignore. Geänderte Dateien misst du mit ls-files -m, Unverfolgtes mit ls-files -o --exclude-standard. Uhrzeiten über die Brücke mit TZ=Europe/Berlin date.

Lies dann nur die Kernlektüre, aus dem Repo über die Geräteanbindung mit Abschnittsfilter:
1. docs/projektfuehrung/UEBERGABE.md — ab der Überschrift „## Umzug 09.10.2026, 06:52“ bis Dateiende (alle neun Blöcke). Den Nachtrag 09.10.2026, 01:32 unmittelbar davor nur bei Bedarf (Bau von TB-142, Sollwerte, Vorgaben des steuernden Chats).
2. docs/projektfuehrung/ARBEITSWEISE.md — nur Abschnitt 0 (von „## 0.“ bis vor „## 1.“; rund 37 KB, nach TB-142 etwas mehr).
3. docs/projektfuehrung/UMZUG.md — nur Abschnitt 3 (von „## 3.“ bis vor „## 4.“).
4. docs/auftraege/MAC_TB-142_waechter_reparatur.md — nur von „## Schritt F“ bis vor „## Nicht in TB-142“ (Abgabe, Teilabgabe, Abbruchkriterien; erst die Bytes messen).
Nur wenn die Geräteanbindung fehlt: die Stellen 1 bis 3 über den Projects-Zugriff (projektfuehrung/…).

Grosse Dateien über Helfer; Helferaufträge als Bausteindateien auf dem Gerät (Vorbilder: sc/auftraege/ im Archiv logs/steuernder_chat/2026-10-09_sc_tb142_bau.tar.gz, für die Abnahme HELFER_ABNAHME141.md in 2026-10-08_sc_tb142_vorbereitung.tar.gz), Berichte auf rund 3 KB begrenzt; Helfer schreiben ihren Bericht nach jeder Prüfung fort und versuchen bei „device not connected“ dreimal neu; Helfer bauen Entwürfe ausserhalb des Repos, ein frischer Gegenleser ist Pflicht (W1); Erinnerungsdateien schreibt nur der steuernde Chat selbst. Die Umzugsampel misst du mit docs/werkzeuge/ampel.py auf deinem eigenen Sitzungsprotokoll (~/.claude/projects/*/<sitzung>.jsonl; ampel.py per device_stage_files holen). Messungen bündeln, Helfer parallel starten.

Umgezogen wird nur, wenn ich es sage oder genehmige. Beim Umzug legst du mir den neuen steuernden Chat selbst an (einmalige geplante Aufgabe mit dem Rechner, Eröffnungstext als erste Nachricht) und gibst den Eröffnungstext zusätzlich als Kopierblock aus.

Arbeite selbstständig (Betreiber 07.10.2026, 19:44). Karten nur für echte Betreiberentscheide, als letzter Schritt; vor einer Karte alles Unabhängige anstossen. Aufgaben an mich nur, wo meine Hand nötig ist, je [ortsunabhängig] oder [Mac-pflichtig].

Achtung, das Wichtigste (Einzelheiten in den neun Blöcken):
1. TB-142 (Wächter-Reparatur, Fehler Nr. 23) ist von mir freigegeben und liegt im Repo. Die Sitzung starte ich dieses eine Mal von Hand; dieser Chat wird angelegt, sobald ihr Schritt 0 committet ist. Miss zuerst, wie weit sie ist (Commits „TB-142 …“, docs/ERGEBNIS_TB-142_waechter_reparatur.md, docs/belege/TB-142/abbruch.txt). Solange sie arbeitet: nichts im Arbeitsbaum anfassen, eine Nachschau per send_later planen (unter einer Stunde). Drei Ausgänge sind möglich: volle Abgabe, Teilabgabe (nur V4) oder ABBRUCH. Dann nimmst du ab (Helfer, Kernzahlen selbst) und schliesst die Sitzung ab 600 s Alter des letzten Commits.
2. Bis TB-142 abgenommen ist, löst du keinen starte_-Auslöser aus (Block 7). Die Sonde starte_TB-99 und schliesse_<HEAD> bleiben unbedenklich. Nach der Abnahme: der erste echte Start über den reparierten Wächter als Probe, mit deinem eigenen Blick ins Fenster; danach passt du die Projekt-Erinnerung an das neue Verhalten an. Ab dann gilt meine Regel vom 08.10.2026, 21:26: Den Start führst du selbst aus, ich bekomme nur den Text mit der Anweisung.
3. Aufgaben am Mac gibst du mir in einfacher Sprache: ein Handgriff je Schritt, mit dem, was ich auf dem Bildschirm sehe (Fehler Nr. 24). Das Ergebnis von TB-142 kann Aufgaben für mich nennen (ein offenes Fenster mit einer Rückfrage, eine Frage, die ich einmal beantworten muss) — gib sie mir genau so weiter.
4. Danach: TB-137 abnehmen, sobald ich das Gesamtergebnis einfüge; zweite Fable-Anfrage (wartet auf TB-137); Bauauftrag Zellen-Erzeuger erst nach Fable.

Sag mir in wenigen Sätzen, was du verstanden hast, und fang in derselben Antwort mit dem ersten Handwerksschritt an. Am Ende jeder Antwort: Kopierblock für die Claude-Code-Sitzung (Wortlaut aus logs/sitzungswaechter/letzter_satz.txt; ist kein Auftrag startklar, steht das dort), dann die Zeile mit der Umzugsampel.
```

## Nachtrag 09.10.2026, 07:01 — nach dem Umzugsblock: Fehler Nr. 25 (Kopierblock ohne Auftrag wurde abgeschickt); Start von TB-142 steht noch aus

- **Fehler Nr. 25 (steuernder Chat, 09.10.2026, 01:32):** Am Ende der Antwort stand unter „Empfänger: Claude-Code-Sitzung auf dem Mac“ ein Kopierfeld mit dem Text „Kein Auftrag startklar. TB-142 wartet auf die Einzelfreigabe …“. Der Betreiber schickte diesen Text an eine Claude-Code-**Cloud**-Sitzung und fügte um 07:00 deren Antwort ein („Verstanden. Ich schicke nichts ab … Diese Sitzung läuft in einem Cloud-Container“). Folgenlos: Die Cloud-Sitzung hat nach eigener Angabe nichts geändert, committet oder gepusht; gemessen 07:01: HEAD = `origin/main` = `5ed3827`, Arbeitsbaum mit genau den drei Einträgen, md5 von Auftrag und Zeiger unverändert. ⇒ **Vorgabe (gilt, wenn der Betreiber nicht widerspricht):** Ist kein Auftrag startklar, steht das als gewöhnlicher Satz am Schluss der Antwort, **nicht** in einem Kopierfeld und ohne Empfängerzeile — ein Kopierfeld trägt nur Text, der abgeschickt werden soll. Das ändert die Form der Regel vom 02.10.2026, 10:45 für diesen einen Fall und gehört in den nächsten Regelwerk-Nachtrag (Abschnitt 0, Gruppe „Am Ende jeder Antwort“).
- **Für den neuen Chat:** Der Satz für TB-142 gehört in das Terminal-Fenster auf dem Mac, in dem der Betreiber die Sitzung von Hand startet — nicht in eine Cloud-Sitzung. Eine Cloud-Sitzung fände in ihrem Klon (Stand `5ed3827`) die Zeile TB-142 nicht und bräche ab; TB-142 misst Terminal und launchd und kann nur auf dem Mac laufen. Fehler ab Nr. 26.

## Nachtrag 09.10.2026, 07:12 — Sitzung für TB-142 doch über den Wächter angelegt (07:08); Fehler Nr. 26; der Satz ist nicht angekommen

- **Betreiber 07:06:** „Wieso hast du noch keine initiale claude Code Sitzung gestartet? … möchte dass diese wiederhergestellt wird.“ ⇒ **Fehler Nr. 26 (steuernder Chat, 06:53 und 07:01):** Die Vorgabe des vorigen Chats („kein `starte_TB-<n>`, Start einmal von Hand“, Umzug 22:03, Block 4 Nr. 2 und Block 7) stand über der Betreiberregel vom 08.10.2026, 21:26 und vom 05.10./08.10. („Sitzung selbst anlegen“). ⇒ Eine Betreiberregel geht einer Vorgabe des steuernden Chats vor; hält der steuernde Chat den Weg für riskant, nennt er das Risiko und fragt per Karte, statt dem Betreiber die Arbeit zu geben. Damit sind Block 1, Block 5 und Block 7 (zweiter Punkt) des Umzugsblocks 06:52 und Nr. 1 des Eröffnungstexts in diesem Punkt überholt: **Die Sitzung wurde nicht von Hand gestartet.**
- **Gemessen:** Auslöser `starte_TB-142` um 07:08:00; Wächter-Log: alle Wachen bestanden, „Terminal-Fenster 21346 offen“, 07:08:23 „Satz ins Fenster gelegt“ (diesmal eine neue Fensternummer, nicht 21040). Sonden `starte_TB-99` 07:09:34 und 07:11:22: eine Sitzung im Repo, PID 40587, Rechenzeit 3,90 s → 4,66 s in 108 s, Zustand S. Kein Commit nach `5ed3827`, kein `docs/belege/TB-142/`. ⇒ Die Sitzung wartet; der Satz samt Zeilenende hat keinen Auftrag ausgelöst (wohin er ging — in eine Startfrage oder ins Leere —, ist nicht gemessen).
- **Nicht gelungen:** der eigene Blick ins Fenster. Terminal ist freigegeben (Stufe „click“), `computer_app_list_windows` nennt nur ein Fenster (21040, anderer Schreibtisch), `computer_app_screenshot` scheiterte zweimal („ScreenCaptureKit did not call back“). Ob die Sitzung an der Eingabezeile oder an einer Frage steht, ist offen.
- **Dem Betreiber gegeben (07:1x):** den Satz in der Claude-App unter der Gerätesitzung abschicken; erscheint sie dort nicht, hängt sie an einer Startfrage ⇒ am Mac im Terminal-Fenster einmal die Eingabetaste, dann der Satz. Nachschau dieses Chats 07:39 geplant. Fehler ab Nr. 27.
