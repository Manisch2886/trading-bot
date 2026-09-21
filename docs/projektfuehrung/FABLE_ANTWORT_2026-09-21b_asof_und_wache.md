# FABLE_ANTWORT 2026-09-21b — asof, Wache, Aktenzeichen, Nachlieferung

*Bezug: Rückmeldung vom 21.09., 16:24. Vier Punkte. Antwort (2) enthält eine Entscheidung, die vor dem Tag ins Register muss.*

---

## (1) Aktenzeichen — übernommen

Richtig ist: **Festlegung 11** = „DSR ist Bericht, nicht Tor", **Festlegung 12** = „Es kann sein, dass kein einziger Bot die Schwelle erreicht". Festlegung 10 ist die DSR-Basis N = 653. Meine Zitate „Festlegung 10/11" in 20a und 21a sind damit falsch; wo ich „Festlegung 10" für den Satz „Bleibt/Geht läuft über die Abbruchkriterien" angeführt habe, trägt keine Festlegung diesen Satz — er folgt aus Abschnitt 7 und Registertext 6b und braucht kein eigenes Aktenzeichen.

Abbruchkriterium (b) steht wörtlich in Abschnitt 7. Der Vorbehalt „falls es fehlt: Berichtigung" ist gegenstandslos; es bleibt ein **Verweis**. Ich habe es nicht nachgeprüft, weil ich das Register nicht lesen kann — das ist der Grund für den Fehler, nicht eine Entschuldigung dafür. Ich zitiere Aktenzeichen künftig nur, wo ihr sie mir im Wortlaut vorgelegt habt.

## (2) asof — wird durch den Snapshot gesetzt, nicht durch den Tag

Eure Lesart ist zur Hälfte richtig: asof entsteht **mit dem Snapshot**. Nicht mit dem signierten Tag — der Tag friert ein, was das Register sagt; er erzeugt keine Zahl.

**Entscheidung (offener Punkt; Begründung nennt kein Ergebnis):**

> **Registertext 5a, Ergänzung:** asof ist das UTC-Datum des Erstellungszeitpunkts des registrierten Snapshots. Es wird im `MANIFEST.json` als Feld `asof` geführt und im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof.

Für den registrierten Snapshot aus Abschnitt 18 (erstellt 2026-09-19T06:49:32Z) heisst das: **asof = 2026-09-19.** Der Wert existiert bereits als Tatsache; was fehlt, ist nur die Zeile, die ihn asof nennt.

*Warum das Erstellungsdatum und nicht das Datenende:* Das Datenende (grösstes `open_time` über alle Kursdateien) wäre eine zweite aus dem Inhalt abgeleitete Grösse — genau die Bauart, die ich bei `fensteranker` abgelehnt habe, weil sie mit den Daten wandert. Innerhalb eines eingefrorenen Snapshots wandert sie zwar nicht mehr, aber sie fällt mit dem Erstellungsdatum auseinander, sobald der Kursdatenstand älter ist als der Snapshot (hier: Kursdaten bis 15.09., Snapshot vom 19.09.). Dieser Abstand ist eine Frische-Tatsache und gehört als eigenes Manifest-Feld (`datenende`) dorthin, nicht in asof. Das Erstellungsdatum ist bereits registriert, von niemandem anders berechenbar und unabhängig davon, welches Symbol zuletzt eine Kerze hatte.

*Bekannte Wirkung auf die Zulässigkeit:* Der Horizontbeginn je Bot verschiebt sich gegenüber dem Datenende um vier Tage (19.09. statt 15.09.). Die erste Falte nach 4a beginnt am 1. Januar eines Jahres; eine Verschiebung im September ändert das Jahr nicht. Die Zahl der Falten bleibt unter beiden Lesarten gleich — das ist eine Kalenderaussage, keine Ergebnisaussage. Das Manifest ändert sich um ein Feld; der Snapshot-Hash liegt über den Dateien, nicht über dem Manifest (Rückfrage vom 17.09.), und bleibt gleich.

**Reihenfolge, wie ihr sie vorschlagt, mit einer Korrektur:** asof eintragen (Tatsachennotiz, jetzt) → Horizontbeginn je Bot ableiten (asof − RECENT_YEARS_ONLY, vier absolute Daten, Tatsachennotiz) → Falten nach 4a ableiten → Faltenplan als Registertext → Tag. Der Faltenplan ist bis zum zweiten Schritt vorläufig, und der zweite Schritt kann heute passieren. Er wartet nicht auf den Tag; er muss vor ihm fertig sein, weil die Falten Registertext sind.

Dass ihr nicht geraten habt, war richtig: Ein geratenes asof wäre nach dem Tag ein Amendment gewesen.

## (3) Wache — keine Ausnahme vom Einfrieren

Einverstanden, ohne Vorbehalt. Das Einfrieren von `auswertung.py` ist mehr wert als die Wache; eine Ausnahme dafür würde die Regel entwerten, die den Lauf schützt. Mein Vorschlag „in den Auswerter" war falsch adressiert.

Wo sie hingehört: Die Wache prüft, dass keine Trade-Liste einen Einstieg vor dem Horizontbeginn enthält. Nach der Berichtigung der vier `multi_symbol_optimise.py` (Cutoff = asof − RECENT_YEARS_ONLY statt `df["open_time"].max()` je Symbol) kann das nur noch eintreten, wenn eine Fassung ohne die Berichtigung läuft — und das schliesst 5e aus (HEAD = registrierter Commit, sauberer Baum). Die Wache ist damit eine Selbstprüfung des Objekts, das ohnehin geändert wird:

> **In TB-30b, in denselben vier Modulen:** Nach dem Erzeugen der Trade-Liste prüft der Optimierer, dass ihr frühester Einstieg ≥ Horizontbeginn ist; sonst Abbruch mit Rückgabewert 2. Der Bericht führt je Bot den frühesten Einstieg und den Horizontbeginn nebeneinander auf.

Kein neues Modul, keine Änderung an eingefrorenem Code, dieselbe Berichtigung. Wenn ihr die Prüfung lieber ausserhalb der Optimierer haben wollt — als eigenständiges Prüfskript nach dem Muster von `snapshot.py --pruefen`, vom Laufwrapper vor `auswertung.py` aufgerufen — ist das gleichwertig; ich ziehe die Fassung in den Optimierern vor, weil sie keinen zweiten Ort erzeugt, an dem der Horizontbeginn steht.

## (4) Nachlieferung

`FABLE_ANTWORT_2026-09-20a_grenzfall.md` liegt bei. **Sie ist die Quelle**; Teil 2 von 21a ist die Kurzfassung. Die Datei trägt oben einen datierten Nachtrag zu den beiden Aktenzeichen und zum gegenstandslosen Berichtigungs-Vorbehalt; der Text vom 20.09. darunter ist unverändert. 21a gebe ich nicht neu aus — die Korrektur aus (1) gilt für beide Dateien, und ihr habt 21a bereits.

---

**Kurz:** (1) Festlegung 11/12 übernommen; (b) ist Verweis auf Abschnitt 7. (2) asof = UTC-Datum der Snapshot-Erstellung = 2026-09-19; als Ergänzung zu 5a und Tatsachennotiz zu Abschnitt 18 eintragen; Reihenfolge asof → Horizonte → Falten → Tag, alles vor dem Tag. (3) Keine Ausnahme vom Einfrieren; Wache als Selbstprüfung in die vier Optimierer, TB-30b. (4) 20a liegt bei, mit Nachtrag; sie ist die Quelle.
