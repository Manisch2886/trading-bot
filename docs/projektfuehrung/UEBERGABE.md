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
