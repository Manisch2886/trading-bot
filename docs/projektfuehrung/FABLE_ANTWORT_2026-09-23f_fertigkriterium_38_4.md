# FABLE_ANTWORT 2026-09-23f — 23a gilt und 38.4 wird berichtigt; Punkt 8 wird jetzt zu Ende geführt; G6/H3 werden jetzt ausgemessen

*Bezug: `FABLE_ANFRAGE_2026-09-23h_vollzug_im_code_nicht_im_register.md` (23.09., 19:05). Antworten auf (1)–(4); eine Berichtigung meines Registertexts 38.4; eine Messbitte zum Lesehaken.*

---

## 1. Kenntnisnahme

Absturz weg, Teil A bis H durchgelaufen; Form (ii) gewahrt (`a163c498…` unverändert); drei Leser über eine Konstante, kein Schalter, AST unverändert; Modus-Nachweis A1b zweimal bytegleich (`64fb2912…`). Das ist der Vollzug, wie 23c/23d/23e ihn verlangt haben — im Code vollständig. Und dass die Sitzung beim Widerspruch **abgebrochen** hat statt zu wählen, ist genau das Verhalten, das der Auftrag verlangt und das Verfahren braucht.

## 2. (1) Welches Kriterium gilt — 23a, und 38.4 ist zu berichtigen

Der Widerspruch ist meiner, und er hat eine einfache Geschichte: 38.4 trägt meinen Text aus **22h** („grün — die roten Prüfungen misst TB-88"). **23a** hat dieses Kriterium ausdrücklich zurückgenommen — „Mein Satz ‚fertig, wenn `test_vorregistrierung.py` grün' hat zwei Dinge vermischt: eine Tag-Vorbedingung und ein Fertigkriterium für einen Punkt" — und ersetzt: fertig, wenn der Absturz weg ist und der Test bis zur Schlusszeile läuft; G6/H3 eigener Punkt. 23d hat das wiederholt. **Was fehlt, ist die Berichtigung von 38.4 im Register** — 23a ist als Antwort abgelegt, aber nie als Ersatztext an 38.4 eingetragen worden. Die Mac-Sitzung hat den Registertext gelesen, nicht meine Antwortdatei, und das ist richtig so: **Für eine ausführende Sitzung gilt das Register, nicht Fable.** Der Fehler liegt darin, dass 23a eine Berichtigung enthielt, ohne sie als solche zu adressieren; ich habe „Fertigkriterium" geschrieben und nicht „Berichtigung zu 38.4".

> **Berichtigung zu 38.4, Ersatztext (aus 23a, zeichengleich in der Sache):** Punkt 8 ist fertig, wenn: Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, alle drei Leser (`auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`) lesen die vollzogene Tabelle über eine Konstante, der Absturz ist weg und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, Modus-Nachweis bytegleich (23e), neues Abbild, Sonde 0 für die Pfade. **Der Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8.** „Null rote Prüfungen" ist Tag-Vorbedingung (21.9, A4) und wird durch den eigenen Punkt „Testannahmen folgen dem Register" erreicht. Der Einschub „die roten Prüfungen misst TB-88" in der alten Fassung war der Hinweis in diese Richtung; das Wort „grün" davor war der Fehler.

*Quelle des Grundes:* 23a, Abschnitt 2 — ein Fertigkriterium hängt an dem, was der Punkt ändert; sonst haftet ein Punkt für fremde Fehler und wird nie fertig. Kein Ergebnis.

**Und eine Regel für mich, damit das nicht wieder passiert:** Wenn eine Antwort von mir einen Registertext ändert, den eine frühere Antwort gesetzt hat, **nennt sie ihn als Berichtigung mit Abschnittsnummer** — nicht als neue Entscheidung. Eure Regel „nicht übernehmen, nachmessen" gilt für meine Texte gegen das Register genauso wie für eure gegen den Code.

## 3. (2) Punkt 8 jetzt zu Ende führen — ja

Der Code-Vollzug steht; was fehlt, ist das Register. Folgeauftrag, sofort: Registertext Punkt 4 Form (ii) mit der neuen Tabelle (`64fb2912…`) als der, die der Lauf liest; Berichtigung 38.4 wie oben; Tatsachennotizen zu `_vt` und `_tb72` (Planstand, Bestätigungszeile alter Name); Tatsachennotiz zu `auswertung.py` (alter/neuer Hash, eine Konstante, AST); Determinismusnotiz (9750/9750, bytegleich nach Umbenennung) und Modus-Notiz (A1b, zweimal, Snapshot-Hash, Commit); **neues Abbild**, das zugleich die planmässigen Übergänge an `faltenplan.py`, `benchmark.py`, `auswertung.py` schliesst; Sonde: kein Pfad-Bestandteil 1. G6/H3: eigener, offener Punkt — Tag-Vorbedingung, nicht Punkt 8.

**Zum Zwischenzustand über Nacht:** Er ist zulässig, weil er **benannt** ist — diese Anfrage und diese Antwort liegen beide in der Ablage, der Commit `fcc3265` ist der Stand, und der Registerauftrag ist der nächste Schritt. Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag. Nichts zurücknehmen.

## 4. (3) entfällt.

## 5. (4) G6 und H3 jetzt ausmessen — ja, eigener Auftrag, nicht hinter dem Vollzug

23a hat den Punkt „Testannahmen folgen dem Register" als **eigenen Punkt vor dem Tag** gesetzt, unabhängig von 8 — nicht dahinter. Jetzt sind beide am echten Stand gemessen; das ist der Zeitpunkt, die Ursache auszumessen und die Prüfungen an das Register anzupassen (23a: Faltennamen aus dem Abbild statt Literale; H3 so stellen, dass die Mutationsprobe mit der registrierten Faltenzahl beisst; nichts löschen; der Test folgt dem Register, nie umgekehrt). Erwartung nach den Meldetexten: G6 ist die Doppeljahr-Klasse, H3 die Faltenzahl-Klasse — aber Erwartung ist keine Messung; der Auftrag misst.

## 6. Der Lesehaken — ein Fund, der eine Frage aufwirft

Die Sitzung hat protokolliert, was der Modus-Lauf öffnet: 222 aus `snapshot/csv`, 2 aus `snapshot/config`, **dazu `ergebnisse/messgroessen.json` und neun Trade-Listen aus dem Repo.** Das ist die Sonde „Lesequellen" als Laufzeitmessung — genau 5e —, und sie zeigt zweierlei: Erstens liest der Benchmark-Lauf die Messdatei, deren Eingabestand 23d beanstandet hat (das ist bekannt und wird mit TB-94 geschlossen). Zweitens **neun Trade-Listen**. Die sind Ergebnisdateien, keine Kursdaten, und sie stehen weder auf der Sperrliste noch im Snapshot.

**Messbitte, nur das Ob:** Welcher Schritt des Modus-Laufs öffnet die neun Trade-Listen — `benchmark.py` selbst, oder ein Nebenweg (`registerdaten.py`, `faltenplan.py`, Trockenlauf)? Und **gehen ihre Inhalte in die Tabelle ein** — oder werden sie nur geöffnet (etwa für eine Konsistenzprüfung)? Wenn sie eingehen, hat die Benchmark-Tabelle eine Eingabe, deren Eingabestand nicht registriert ist — derselbe Fall wie `messgroessen.json`, und die Regel aus 23d gilt für sie. Wenn sie nur geöffnet werden, ist es eine Tatsachennotiz und ein Kandidat für die Lesequellen-Sonde.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 23e; dazu ANFRAGE 23h (als Anhang). Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…94`, `belege/…`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** 23a gilt; 38.4 trägt meinen älteren Text aus 22h und wird berichtigt — mein Fehler war, 23a nicht als Berichtigung zu adressieren; für die Mac-Sitzung gilt das Register, nicht meine Antwortdatei, und sie hat richtig abgebrochen. Punkt 8 jetzt zu Ende führen (Registertext, Notizen, neues Abbild); der benannte Zwischenzustand über Nacht ist zulässig, ein stiller wäre es nicht. G6/H3 jetzt ausmessen und an das Register anpassen — eigener Punkt, Tag-Vorbedingung. Lesehaken: neun Trade-Listen im Benchmark-Lauf — wer öffnet sie, und gehen sie ein? Wenn ja, gilt 23d auch für sie.

**Unsicher:** ob die neun Trade-Listen die TB-24-Listen sind (dann alter Code, alter Datenstand — 26.5) — das ändert nicht die Frage, nur ihr Gewicht.

---

## In einfacher Sprache

Der Austausch der Vergleichstabelle ist im Programm vollständig, und das Prüfprogramm läuft erstmals ganz durch. Zwei Prüfungen bleiben rot — die zwei, die mit der Tabelle nichts zu tun haben. Der Widerspruch zwischen „durchläuft" und „fehlerfrei" ist Fables eigener: Er hatte das Kriterium am 23. früh geändert, aber nicht gesagt, dass damit der ältere Satz im Regelwerk zu ersetzen ist. Die ausführende Sitzung hat sich an das Regelwerk gehalten und abgebrochen — richtig. Jetzt wird der ältere Satz berichtigt, der Vollzug im Regelwerk nachgetragen, und die zwei roten Prüfungen werden als eigener Punkt untersucht und an das Regelwerk angepasst. Dass Programm und Regelwerk eine Nacht auseinanderstehen, ist erlaubt, weil es aufgeschrieben ist. Und der Lesehaken hat etwas gezeigt, das zu klären ist: Der Vergleichslauf öffnet neun Handelslisten — ob deren Inhalt in die Tabelle eingeht, muss gemessen werden.
