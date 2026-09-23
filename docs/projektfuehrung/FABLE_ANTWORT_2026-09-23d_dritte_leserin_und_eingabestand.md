# FABLE_ANTWORT 2026-09-23d — Der Lauf liest die neue Tabelle, also wird `auswertung.py` geöffnet — minimal, ohne Schalter; und eine Eingabe des Laufs muss aus dem registrierten Snapshot reproduzierbar sein, nicht aus der Git-Historie

*Bezug: `FABLE_ANFRAGE_2026-09-23e_dritte_leserin_eingefroren.md` (16:15) und `FABLE_ANFRAGE_2026-09-23f_eingefroren_ohne_eingaben.md` (18:00). Beide zusammen, weil sie dieselbe Frage von zwei Seiten stellen: Was bezeugt eine eingefrorene Datei am Tag — und was muss dafür gelten? Vier Entscheidungen, zwei Regeln, eine Erweiterung der Sonde.*

---

## 0. Mein Fehler zuerst

Die Tatsachennotiz aus TB-88 (M5) nennt drei Leser der alten Tabelle, darunter `auswertung.py::main`. Meine fünf Vollzugsschritte in 23c nennen zwei. Ich habe die Notiz gelesen und den dritten beim Schreiben verloren — dieselbe Klasse wie der Vorlauf-Satz am 21.09. Gut, dass TB-92 mit Sperre am Anfang geschrieben wurde; das ist die Regel „nicht übernehmen, nachmessen" in Anwendung auf mich.

## 1. 23e — die dritte Leserin

**(1) Ja.** „Die Tabelle, die der Lauf liest" heisst `auswertung.py::main`; alles andere wäre ein Test, der neben dem Bewachten steht (12), und ein Bericht, der etwas anderes zeigt als der Lauf rechnet. Der Vollzug von Punkt 8 umfasst `auswertung.py`.

**Warum das Öffnen hier zulässig ist, obwohl ich es in 21b (3) für die Wache abgelehnt habe:** Das Einfrieren von `auswertung.py` schützt das **Urteil** — Selektionsstatistik, Plateau-Regel, Abbruchkriterien, Kapitalregel (Punkte 3 und 5) — davor, nach Kenntnis von Ergebnissen geändert zu werden. Eine Wache hätte dem Urteil eine Zeile Logik hinzugefügt; das war abzulehnen, weil es einen zweiten Ort für eine Regel geschaffen hätte. Ein **Lesepfad** ist kein Urteil. Und die Änderung ist erzwungen, nicht gewählt: Mit der alten Tabelle kann der Lauf am Tag nicht einmal starten (fünf Bots ohne Falte) — der Grund kommt aus dem Register (23, 25, Punkt 4 nach Vollzug), nicht aus einer Wirkung. F17 ist erfüllt; 37.3 gibt den Zeitpunkt (vor dem Tag, planmässig, Freigabe, Notiz).

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Zu Sperrlistenpunkt 4, Vollzug, Schritt 1a:** `auswertung.py` liest die vollzogene Tabelle über **eine** Konstante am Modulanfang, deren Wert der registrierte Pfad der neuen Tabelle ist. **Kein Kommandozeilenschalter** — Abschnitt 12 sagt „`auswertung.py` hat keinen Schalter", und eine Option, die bestimmt, welche Tabelle gilt, wäre einer. Bedingungen: AST-Vergleich aller Funktionskörper unverändert; genau eine Zuweisung verändert (die Pfadkonstante); `test_vorregistrierung.py` und `beispieldaten.py` lesen dieselbe Konstante, damit Test und Lauf nicht auseinanderfallen können; Tatsachennotiz mit altem und neuem Hash von `auswertung.py`. Die Änderung geschieht in demselben Auftrag wie der Vollzug (TB-92), nicht danach.

**(2) `EINGEFROREN` bleibt, wie es ist — es trägt weiter den alten Pfad, nicht beide.** Der Grund ist nicht der Wortlaut, sondern der Ort: `EINGEFROREN` steht in `herkunft.py` (Punkte 11/12), und in 22d habe ich entschieden, `herkunft.py` nicht zu öffnen, weil die Sperrlisten-Sonde die Lücke schliesst. Das gilt hier genauso: Die **neue** Tabelle ist durch Punkt 4 und das Abbild geschützt (Sonde); die **alte** bleibt in `EINGEFROREN` als das, was sie ist — der registrierte historische Stand, dessen Hash `register()` bezeugt. Die Tatsachennotiz zu 37.4 wird um den Satz ergänzt: „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde." Zwei Nachweise, zwei Gegenstände, kein Widerspruch (22d).

*Kein Ergebnis:* Welche Tabelle der Lauf liest, ist entschieden, bevor irgendwer eine Zahl aus einem Lauf gesehen hat; die Tabelle selbst ist nach 23b bytegleich zur TB-72-Tabelle bis auf einen Namen.

**(3)** entfällt.

**(4) Ja — die Sonde führt auch Lesequellen.** Ihr habt recht: Die Sonde „Schreibziele" aus 23c hätte diesen Fall nicht gefunden. Erweiterung:

> **Sonde „Lesequellen" (statisch, Ergänzung zu „Schreibziele"):** Für jedes Modul des Laufbereichs (`research/vorregistrierung/`, `shared/`, die neun `strategies/*/` im Selektionspfad) werden die im Quelltext genannten Lesepfade unter `ergebnisse/`, `config/` und `data/` erhoben (AST: Literale und Voreinstellungen von Argumenten). Jeder Lesepfad muss ein registrierter Pfad sein — Punkt der Sperrliste, Gruppe „bestimmt" oder `EINGEFROREN` — **und** der Pfad, den das Register für diesen Zweck als gültig nennt (heute: die vollzogene Tabelle, nicht die historische). Ein Lesepfad auf einen historischen Stand ist 1. Die Sonde ist die statische Seite von 5e (Lese-Audit): 5e sagt nach dem Lauf, woraus gelesen wurde; die Sonde sagt vor dem Lauf, woraus gelesen werden **kann**.

*Quelle des Grundes:* 5e und 12; kein Ergebnis.

## 2. 23f — eine bezeugte Datei ohne Eingaben

Zuerst das, was die Messung geleistet hat: Meine Bedingung („bytegleich, sonst Befund und Stopp") hat einen Befund erzeugt, und die Sitzung hat ihn **ausgemessen statt gedeutet** — mit der Gegenprobe gegen `a2fcf01`, die nicht im Auftrag stand. Code deterministisch, Eingaben verändert, Ursache ein einzelner Commit (`90e3cbd`, TB-34), Muster der Abweichungen deckungsgleich mit den berührten Dateien. Das ist die Form, in der ein Befund vorgelegt werden soll.

**(1) Nein.** Eine Datei, die **Eingabe des Laufs** ist (`registerdaten.py` liest sie; Raster 3 ist „erzeugt, nicht abgetippt"; der Faltenplan hängt daran), darf am Tag keinen anderen Datenstand beschreiben als den, mit dem der Lauf rechnet. Der Lauf rechnet auf dem registrierten Snapshot (5a, 17.1, 18; Selektionsmodus, gemessen 22.09.). Der Snapshot enthält die Krypto-Historie ab 2017 (TB-34, 10: „vollzogen vor jedem Lauf"). `messgroessen.json` beschreibt den Stand davor. Am Tag würde das Register also einen Hash bezeugen, der sagt „die Messgrössen des Verfahrens sind diese", während der Lauf über Daten geht, für die sie nicht gelten. Das ist kein Bezeugungsproblem, das eine Notiz löst — es ist ein **Widerspruch zwischen zwei registrierten Dingen** (Snapshot und Messgrössen), und Widersprüche im Register werden vor dem Tag geschlossen, nicht beschrieben.

**(2) Neu rechnen — auf dem registrierten Snapshot, nicht auf `data/`.** Nicht den Datenstand zurückführen: Der Snapshot ist registriert (18, asof 28, datenende 31.5), TB-34 ist als Tatsache mit Grund im Register (10: kein Amendment, weil kein Lauf), und zwei Wochen Krypto-Historie zu verwerfen, um eine Messdatei zu retten, kehrt die Rangfolge um — die Daten sind registriert, die Messdatei ist aus ihnen abgeleitet.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Registertext, Ersteintrag — Eingabestand eingefrorener Ergebnisdateien:** Jede eingefrorene Datei, die der Lauf oder die Herleitung eines Registertexts liest (Eingabe des Verfahrens), ist aus dem **registrierten Snapshot** (5a) und dem **registrierten Code** reproduzierbar; Snapshot-Hash und Code-Commit ihrer Erzeugung stehen als Tatsachennotiz neben ihrem Hash. Eine Eingabe, die nur aus der Git-Historie reproduzierbar ist, ist keine Eingabe des Laufs, sondern ein historischer Stand: Sie bleibt liegen, bezeugt und benannt, und wird **vor dem Tag einmal auf dem Snapshot neu gerechnet** — mit dem abgesicherten Erzeuger, `--ziel` neu, Schreibregel 36.1, Beleg. Die Reproduzierbarkeit wird vor dem Tag einmal nachgewiesen (Bauart 23b: Lauf auf dem Snapshot → bytegleich mit der eingefrorenen Datei; sonst Befund). Dateien, die weder der Lauf noch eine Herleitung liest (historische Stände nach Form (ii)), brauchen den Nachweis nicht — sie bezeugen, was war.
>
> **Für `ergebnisse/messgroessen.json`:** Neurechnung mit dem nach 36.1 abgesicherten `messgroessen.py` auf dem Snapshot `snapshots/<hash>/` im Selektionsmodus, neuer Pfad, Hash; die alte Datei bleibt in `EINGEFROREN` als historischer Stand (Eingabestand `a2fcf01`, Tatsachennotiz); `registerdaten.py` liest die neue über eine Konstante (Punkt 1: vor dem Tag, 37.3, AST-Nachweis). **Dann werden alle Herleitungen, die daran hängen, nach den registrierten Regeln nachgezogen und verglichen** — Raster 3 („erzeugt, nicht abgetippt"), Faltenplan 33.2, und was sonst `registerdaten.py` daraus bildet. Jede Abweichung ist Tatsachennotiz und, wo sie Registertext berührt, Berichtigung mit dem Grund „Eingabe war auf nicht-registriertem Datenstand gerechnet" — **nicht** eine Wahl. Was sich nicht ändert, wird ebenfalls festgehalten.

*Quelle des Grundes:* 5a/5e (der Lauf liest den Snapshot und nichts anderes), 3 („erzeugt, nicht abgetippt" — eine erzeugte Zahl gilt nur mit ihren Eingaben), 12 (kein Schalter, keine Lesart, die vom Stand abhängt). **Kein Ergebnis — und hier muss ich es besonders sagen:** Ich weiss nicht, ob die Neurechnung Rastergrenzen oder Falten bewegt. Ich weiss nur, dass die Regel unabhängig davon dieselbe ist, und deshalb steht sie hier, **bevor** gerechnet wird (Bauart 24.3). Wer nach der Neurechnung sagt „das bewegt zu viel, lassen wir es", wählt nach Wirkung — und wer vorher sagt „das bewegt wahrscheinlich nichts, also Notiz", wählt auch.

**(3)** entfällt für Eingaben; gilt für historische Stände (Notiz genügt, Nachweis entfällt).

**(4) Ja, als Regel — mit der Unterscheidung oben.** `ergebnisse/faltenplan.json` ist nach 30 historischer Stand, wird nicht gelesen: Notiz genügt. `ergebnisse/benchmark_drawdowns.json` wird nach dem Vollzug nicht mehr gelesen: Notiz genügt. Die **vollzogene** Benchmark-Tabelle ist Eingabe des Laufs: Ihr Eingabestand (TB-91 rechnete auf `data/` — ist `data/` byteweise der Snapshot? Nach 10 unverändert seit 15.09., der Snapshot vom 19.09.; das ist zu messen, nicht anzunehmen) und der Reproduzierbarkeitsnachweis auf dem Snapshot gehören vor den Tag. Und `ergebnisse/messgroessen.json` ist der Fall, der die Regel ausgelöst hat.

**Zwei Messbitten, nur das Ob, vor der Neurechnung:** (a) Welche Schlüssel von `messgroessen.json` liest `registerdaten.py`, und in welche Registergrössen fliessen sie (Rastergrenzen? `MIN_HISTORY`? Faltenplan-Eingaben)? Das bestimmt, was nachgezogen werden muss — nicht, ob. (b) Ist `data/` heute byteweise der Kursdatenteil des Snapshots (`d9449faf…`)? Wenn ja, ist die TB-91-Tabelle bereits auf dem Snapshot gerechnet und braucht nur die Notiz; wenn nein, gilt für sie dasselbe wie für `messgroessen.json`.

## 3. Zu 23f Abschnitt 4 — die Berechtigungsdatei

Kenntnisnahme, und der Vorschlag ist richtig: Die Sonde prüft, ob jeder Pfad der drei Gruppen in der Berechtigungsdatei steht. Eine Liste, die einer anderen hinterherläuft, wenn niemand abgleicht, ist die Fehlerklasse aus 22c (`EINGEFROREN` gegen Abschnitt 10) — der Abgleich gehört in die Sonde, nicht in ein Gedächtnis.

## 4. Was das für den Plan heisst

- **TB-92 (Vollzug 8):** Sperre lösen; Schritt 1a (`auswertung.py`, Konstante, AST) hinzu; `EINGEFROREN` unverändert. Voraussetzung Messbitte (b): Wenn `data/` ≠ Snapshot, vor dem Vollzug die Tabelle auf dem Snapshot nachrechnen (bytegleich erwartet — sonst Befund).
- **Neu, vor dem Tag, Stufe III:** `messgroessen.json` auf dem Snapshot neu rechnen; Herleitungen nachziehen und vergleichen; Registertext „Eingabestand" eintragen; `registerdaten.py` auf die neue Datei.
- **Sonde:** drei Gruppen (10, „bestimmt", `EINGEFROREN`), Schreibziele, **Lesequellen**, Berechtigungsdatei-Abgleich, Eingabestand-Notiz je Eingabedatei.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 23c; dazu ANFRAGE 23e, ANFRAGE 23f (als Anhang). Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…93`, `belege/TB-91…`, `belege/TB-93…`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** 23e: Ja, `auswertung.py` gehört in den Vollzug — der Lauf ist `main`. Öffnen ist zulässig, weil ein Lesepfad kein Urteil ist und die Änderung vom Register erzwungen wird, nicht von einer Wirkung; minimal, eine Konstante, **kein Schalter** (12), AST-Nachweis, Test und Lauf lesen dieselbe Konstante. `EINGEFROREN` bleibt unverändert (herkunft.py nicht öffnen, 22d); die neue Tabelle schützt Punkt 4 über die Sonde. Sonde führt auch **Lesequellen**. 23f: Nein — eine Eingabe des Laufs darf keinen anderen Datenstand beschreiben als den Snapshot. `messgroessen.json` wird auf dem Snapshot neu gerechnet, die alte bleibt historisch; alle Herleitungen (Raster 3, Faltenplan) werden nach den registrierten Regeln nachgezogen; jede Abweichung ist Berichtigung, keine Wahl — und die Regel steht, bevor gerechnet wird. Allgemeine Regel: Eingaben des Laufs tragen Snapshot-Hash und Code-Commit und sind daraus reproduzierbar; historische Stände brauchen nur die Notiz. Zwei Messbitten: Was liest `registerdaten.py` aus der Datei, und ist `data/` heute byteweise der Snapshot?

**Unsicher:** ob `registerdaten.py` die Messgrössen nur für die Rastergrenzen liest oder auch für Grössen, die in 33.2 eingehen — davon hängt ab, wie weit das Nachziehen reicht, nicht ob.

---

## In einfacher Sprache

Zwei Funde, eine Wurzel. Erstens: Das Auswertungsprogramm — also das, was am Stichtag wirklich rechnet — liest die alte Vergleichstabelle fest verdrahtet, und Fable hatte es in seiner Vollzugsliste vergessen. Es wird deshalb minimal geändert: eine einzige Pfadangabe, kein Wahlschalter, mit Nachweis, dass sonst nichts angefasst wurde. Test und Lauf müssen dieselbe Tabelle lesen, sonst prüft der Test etwas anderes als das, was läuft. Zweitens: Eine eingefrorene Messdatei, aus der Regelwerksgrössen abgeleitet sind, beschreibt einen Datenstand, den es nur noch in der Versionshistorie gibt — die Krypto-Daten wurden danach um vier Jahre erweitert. Fable entscheidet: Eine Eingabe des Laufs muss aus dem eingefrorenen Datenbestand reproduzierbar sein, nicht aus der Historie. Die Datei wird auf dem Datenbestand neu gerechnet, alles, was davon abhängt, wird nachgezogen und verglichen, und jede Änderung wird als Berichtigung eingetragen — ob viel oder wenig, spielt für die Regel keine Rolle, und deshalb steht sie fest, bevor gerechnet wird. Das Prüfprogramm soll künftig auch erfassen, welche Dateien die Laufprogramme lesen, nicht nur, welche sie schreiben.
