# Backlog-Nachtrag (v) — der Sitzungsstart (19.09.2026)

⚠️⚠️ **ZWISCHENLAGER, offene Bringschuld** — `logs/auftraege/` ist gitignoriert.
Zu übertragen nach `docs/projektfuehrung/nachtraege/`, sobald TB-59 fertig ist.

⚠️ **Nummern nach K2i.** Gemessener Stand unverändert (`BACKLOG.md`, 951 Zeilen,
`fef279c`): ⚠️ ÜBERHOLT durch TB-59 — der Namensraum K2 ist seither erschöpft. Gemessen am 20.09.2026: `K2a` bis `K2z` sämtlich belegt, `K3a` bis `K3j` neu vergeben, nächste freie ist **`K3k`**. Vorgeschlagen waren `K2l`/`K2m`
in (s), `K2n`/`K2o` in (t). Dieser Nachtrag schlägt **`K3k`** vor. **Die Vergabe
gehört der einarbeitenden Sitzung.**

| # | Punkt |
|---|---|
| **K3k** | ⭐⭐ **WIE EINE MAC-SITZUNG GESTARTET WIRD — vier Regeln, aus einem gemessenen Hänger.** Am 19.09.2026, 23:11, hat `claude --remote-control "<Anweisungstext>"` die Sitzung gestartet und **den Text nicht übergeben**; Eingabezeile leer, `/remote-control` aktiv. ⚠️ **Die Ursache ist NICHT gemessen** (Anführungszeichen zerlegt · Text abgeschnitten · Flag übergibt keinen ersten Zug) und wird nicht behauptet — die Abhilfe braucht sie nicht. **Die vier Regeln:** (1) **Der Anweisungstext reist nie im Startbefehl mit** — nackt starten, Text als eigener Block in die wartende Zeile. (2) **Fester Zeiger `docs/auftraege/AKTUELLER_AUFTRAG.md`**, damit der einzufügende Satz jedes Mal identisch ist, **mit Empfangszeile** am Ende. (3) **Commit und Start nie über zwei Nachrichten trennen** — jeder Auftrag trägt einen Schritt 0, der den Arbeitsbaum committet, und der Nachweis „sauber" wird danach geprüft. (4) ⭐ **Nach jedem Start messen, ob der Text angekommen ist.** Eingetragen in `ARBEITSWEISE.md` **Abschnitt 14 (neu)** mit Berichtigung von Abschnitt 1, und in die Erinnerung |
| **K3l** | ⚠️ **PRÄZISIERUNG ZU K3k (4), am selben Abend nötig geworden — die Messung beweist den EMPFANG, nicht den FORTSCHRITT.** Nach dem Schritt-0-Commit stand `HEAD` dreieinhalb Minuten still, während die Sitzung 1 544 Zeilen Nachträge und ein 951-Zeilen-Backlog las. **Die Unterscheidung:** nichts bewegt sich **und** Schritt 0 hat nicht committet ⇒ Text nicht angekommen; nichts bewegt sich, **aber** Schritt 0 hat committet ⇒ **sie liest, kein Befund**. ⭐ *Wer das nicht trennt, unterbricht eine arbeitende Sitzung — dieselbe Fehlerklasse wie Block 7, Punkt 2, wo aus einem UTC-Zeitstempel geschlossen wurde, eine Sitzung sei tot.* **Für eine lesende Sitzung ist der Fortschritt in Web und App sichtbar, nicht im Repo** |
| **K3m** | ⚠️ **WIDERSPRUCH IN `ARBEITSWEISE.md` AUFGEDECKT, berichtigt:** Abschnitt 1 verlangte *„IMMER als fertiger Einzeiler mit Dateipfad"* und *„ein Befehl, eine Zeile, ein Einfügen"* (ergänzt 15.09.2026) — **genau dieser Einzeiler hat den Hänger erzeugt**. Die Begründung von damals (zwei Schritte heissen zweimal kopieren) stimmt; die Folgerung trägt nicht mehr. ⭐ **Der Grundsatz „Pfad immer mitgeben, nie beschreiben" bleibt** — er gilt jetzt für den Text, nicht für die Befehlszeile |

---

## Nachgetragen 23:22 — zwei Anweisungen des Betreibers

*(nächste freie K-Nummern nach dem oben vorgeschlagenen `K3m`: `K3n`, `K3o`)*

| # | Punkt |
|---|---|
| **K3n** | ⭐ **DIE TB-NUMMER STEHT IM SITZUNGSTITEL.** Anweisung 19.09.2026: *„Zukünftig sollen auch TB-Angaben im Titel der Claude-Sitzung stehen, damit ich diese in der Historie auseinanderhalten kann."* ⚠️⚠️ **Deckt eine Lücke auf, die `ARBEITSWEISE.md` seit dem 15.09. hatte:** Der Sitzungstitel war Pflicht — **aber nur im Kopf des Aufgabendokuments** (Abschnitt 3). Bei einer nackt gestarteten Mac-Sitzung erreicht er die Sitzungsliste nicht, und der am 19.09. eingeführte **immer identische** Einfügesatz (K3k, Regel 2) hätte **jeder Sitzung denselben Eintrag gegeben** — die Lücke wäre grösser geworden statt kleiner. **Behoben:** Die TB-Nummer steht als Präfix am Anfang des Einfügesatzes. ⭐⭐ **Und der angehängte Satz macht aus dem Titel eine Wache** — nennt `AKTUELLER_AUFTRAG.md` eine andere Nummer als die vorangestellte, bricht die Sitzung ab, statt den falschen Auftrag abzuarbeiten. *Der häufigste Fehler bei einem Zeiger ist ein Zeiger, den jemand zu aktualisieren vergisst.* ⚠️ **Nicht gemessen:** ob Claude Code den Historieneintrag wirklich aus der ersten Nachricht bildet — **kostet beim nächsten Start einen Blick** |
| **K3o** | ⭐⭐ **WAS MIT „ZUKÜNFTIG" GESAGT WIRD, WIRD EINGETRAGEN — ohne weitere Aufforderung.** Anweisung 19.09.2026: *„Füge zukünftig auch immer alle Angaben, die ich mit zukünftig erwähne, in die entsprechenden Dokumentationen nach."* ⇒ **Eine mit „zukünftig" eingeleitete Angabe ist eine stehende Anforderung, keine Bemerkung**, und wird **in derselben Antwort** in die zuständigen Träger eingetragen: Erinnerung immer · `ARBEITSWEISE.md`, `DOKUMENTATIONSSTANDARD.md` oder `UMZUG.md` je nach Gegenstand · Backlog-Nachtrag immer, mit gemessener Nummer · Projektablage nachziehen. ⚠️ **Läuft eine Mac-Sitzung, geht der Text ins Zwischenlager `logs/auftraege/` mit Bringschuld im Kopf** — kein Aufschub, sondern der Weg. Eingetragen als `ARBEITSWEISE.md` **Abschnitt 15 (neu)**. ⭐ *Warum nötig: Die Anweisungen dieses Tages sind mehrfach erst auf Nachfrage in die Dokumente gelangt — und der Chatverlauf ist nach `UMZUG.md` Abschnitt 2 ausdrücklich kein Träger* |

---

## Nachgetragen 20.09.2026 — der Lesepfad

*(nächste freie K-Nummer nach dem oben vorgeschlagenen `K3o`: `K3p`. ⚠️ Gemessen
20.09.2026: `K2a` bis `K2z` sind sämtlich belegt, `K3a` bis `K3j` durch TB-59
vergeben — der K2-Namensraum ist erschöpft.)*

| # | Punkt |
|---|---|
| **K3p** | ⭐⭐ **DER LESEPFAD HAT KEINE REGEL, DER AUFBEWAHRUNGSPFAD SCHON — und deshalb erbt er dessen Wachstum.** Gemessen 20.09.2026: Die sechs Dokumente des Eröffnungstextes umfassen **462 594 Bytes**, davon `BACKLOG.md` allein **350 403 Bytes = 75,7 %**. Darin entscheiden **131 240 Bytes = 37,5 %** nichts mehr: Abschnitte `2b`–`2r` (110 052 B, Rückblicke auf TB-34 bis TB-55), neun ERLEDIGT-Zeilen in Abschnitt 2 (14 120 B), Abschnitt 9 (5 946 B, ⚠️ **inhaltlich Doppel zu `ARBEITSWEISE.md` — der gefährlichere Teil, weil zwei Träger auseinanderlaufen**), Abschnitt 6 (1 122 B). ⭐ **Die Regel dagegen steht seit jeher in Zeile 2 der Datei selbst** (*„Nur aktive Punkte. Alles Abgeschlossene steht im JOURNAL.md"*) **und wurde seit Wochen gebrochen.** ⭐⭐ **Betreiberentscheidung 20.09.2026: Archiv anlegen, mit Verschiebenachweis** — `BACKLOG_ARCHIV.md`, und statt „null entfernte Zeilen" gilt für diese eine Operation *„jede entfernte Zeile erscheint zeichengleich im Archiv"*, per `diff` nachgewiesen. **Das ist der strengere Nachweis, weil er beide Seiten prüft statt einer.** Formuliert als `logs/auftraege/MAC_TB-60_backlog_archiv.md`. ⛔ **Abschnitt 8 (Gestrichen) und `PRUEFPRINZIPIEN.md` bleiben** — 1 990 Bytes, die Wochen sparen |
| **K3q** | ⚠️ **OFFEN, und bewusst so:** Die gewählte Variante räumt die heutigen 37,5 % ab, **hält das künftige Wachstum aber nicht auf.** Die Variante mit stehender Regel (*„jeder Nachtrag nennt nicht nur, was er hinzufügt, sondern auch, was er ablöst"*, in `DOKUMENTATIONSSTANDARD.md`) wurde am 20.09.2026 **nicht** gewählt. ⇒ **Das Archiv ist in einigen Wochen erneut fällig.** Hier festgehalten, damit es beim nächsten Mal keine Überraschung ist, sondern ein Termin |
| **K3r** | ⚠️ **EIGENER BEFUND ZUR EIGENEN ARBEIT:** Sämtliche Dokumentationsänderungen dieser Sitzung trugen `numstat X / 0`, und diese Null wurde jedes Mal **als Qualitätsnachweis vorgezeigt**. Sie ist einer — für die Beweiskraft. ⚠️ **Sie ist zugleich die Ursache des Wachstums, und das wurde kein einziges Mal benannt, bis der Betreiber danach fragte.** ⭐ **Die Lehre: Ein Nachweis, der nur eine Richtung prüft, wird zum Anreiz in diese Richtung.** *Dieselbe Familie wie A4 — ein dauerhaft grüner Nachweis, der nichts kosten kann, hört auf, eine Wache zu sein* |

---

## Nachgetragen 20.09.2026 — die Dokumentationsregel

*(nächste freie K-Nummer nach `K3r`: `K3s`, gemessen)*

| # | Punkt |
|---|---|
| **K3s** | ⭐⭐ **DOKUMENTATION WIRD AKTUELL GEHALTEN, NICHT ANGEHÄUFT.** Anweisung des Betreibers 20.09.2026. **Jede Änderung sagt, was sie ablöst; das Abgelöste wird entfernt statt danebengestellt.** ⚠️ **Vier Träger ausgenommen, weil dort die Aufzeichnung das Produkt ist:** Register, `JOURNAL.md`, Backlog-Abschnitt 8, `PRUEFPRINZIPIEN.md` — *ein Register, aus dem etwas entfernt werden kann, beweist nichts mehr.* ⭐ **Faustregel sonst: die Regel behalten, den Fall streichen**, ein Satz Fall innerhalb der Regel genügt. ⚠️ **Gelöscht wird nur mit Nachweis.** Eingetragen als `DOKUMENTATIONSSTANDARD.md` Regel 9 und `ARBEITSWEISE.md` Abschnitt 16. ⭐ **Messbarer Anlass:** Zwischen der Frage des Betreibers um 09:50 und 10:36 ist die Pflichtlektüre um **+7 243 Bytes** gewachsen, während über ihre Verkleinerung geredet wurde |

| **K3t** | ⚠️⚠️ **ANMELDUNG IST REGEL 0 JEDER MAC-SITZUNG.** Gemessen 20.09.2026, 10:44: Der Start meldete *„`/remote-control` requires a claude.ai subscription. Run `/login`"*, Fusszeile **„Not logged in"**, Kopfzeile **„API Usage Billing"** statt „Claude Max" — **BERICHTIGT 20.09.2026: Die Anmeldung war nicht abgelaufen — der macOS-Schlüsselbund war gesperrt** (`security unlock-keychain`), vom Betreiber bestätigt. *Die zuvor hier stehende Ursachenvermutung war unbelegt.* ⚠️ **Zwei Folgen:** ohne sie fehlt `/remote-control` (Sitzung in App und Web unsichtbar), **und der Lauf wird direkt abgerechnet statt über das Abo**. ⭐ **Erster Befehl ist `/login`, nicht der Auftrag**; Kontrolle an der Kopfzeile „Claude Max". Eingetragen als `ARBEITSWEISE.md` Abschnitt 14 **Regel 0** und im Zeiger `AKTUELLER_AUFTRAG.md` |

---

## Nachgetragen 20.09.2026, Mittag

*(nächste freie K-Nummern nach `K3t`: `K3u`, `K3v`, `K3w` — gemessen: höchste im
Backlog ist `K3j`, `K3k`–`K3t` belegt dieser Nachtrag)*

| # | Punkt |
|---|---|
| **K3u** | ⭐ **JEDE AUFGABE BEGINNT MIT EINEM SATZ IN EINFACHER SPRACHE.** Anweisung 20.09.2026: ein bis zwei Sätze, was jetzt gemacht wird, ohne auszuholen. ⚠️ **Nicht zu verwechseln mit Abschnitt 4** — das ist der Abschluss und gilt nur bei fremden Rückmeldungen; dies ist der Einstieg und gilt immer. Eingetragen als `ARBEITSWEISE.md` **Abschnitt 17** |
| **K3v** | ⛔ **`screen`/`tmux` und Mosh gegen Verbindungsabbrüche: VERWORFEN 20.09.2026, Betreiberentscheidung** — zu komplex bzw. zwei Installationen auf dem Betriebsrechner (Homebrew fehlt, `ARBEITSWEISE.md` 7b). **Nicht erneut vorschlagen.** ⚠️ **Eine Einstellung, die Abbrüche verhindert, gibt es nicht:** Keepalive wirkt nur gegen Leerlauf; beim Wechsel WLAN → Mobilfunk bekommt das Telefon eine neue IP und die TCP-Verbindung endet. ⭐ **Abhilfe vollständig auf der Auftragsseite: nach jedem fertigen Teil sofort committen und pushen** — kostet den Betreiber nichts. *Gemessen: TB-59 verlor so elf Stunden, TB-60 vierzig Minuten Arbeit* |
| **K3w** | ⭐⭐ **EINE NEUE REGEL GILT AUCH FÜR SCHON GESCHRIEBENE, NOCH NICHT GESTARTETE AUFTRÄGE.** `ARBEITSWEISE.md` Abschnitt 14, Regel 3 („sichern nach jedem fertigen Teil") entstand am 20.09. um 10:50; der TB-60-Auftrag war da fertig und wurde **nicht nachgezogen** — derselbe Verlust trat zum zweiten Mal ein. **Beim Formulieren einer Regel wird geprüft, welche offenen Aufträge sie betrifft** |
| **K3x** | ⭐ **Ein langer `&&`-Block verschluckt seine eigenen Prüfungen.** **Gemessen am 20.09.2026: verkettet zweimal nicht durchgelaufen, allein eingefügt zweimal sofort erfolgreich.** ⚠️ **Die Ursache ist NICHT gemessen** — eine Passphrase-Abfrage war es nicht, es erschien keine. ⇒ **Der Push kommt nie in einen `&&`-Block, sondern immer in eine eigene Zeile.** ⭐ **Und die Lehre darüber hinaus: Wenn die Abhilfe ohne Ursache auskommt, gehört keine Ursache in den Text.** *Am 20.09. wurde zweimal geschrieben, die Abhilfe brauche die Diagnose nicht — und beide Male trotzdem eine Diagnose geliefert, die sich als falsch erwies* |
