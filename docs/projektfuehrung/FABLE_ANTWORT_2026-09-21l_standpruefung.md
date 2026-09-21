# FABLE_ANTWORT 2026-09-21l — Standprüfung nach dem Doppelchat: nichts verschossen, drei Beobachtungen, eine Entscheidung zur Wache

*Bezug: Meldung des Betreibers (21.09., 23:39), versehentlich im alten steuernden Chat weitergearbeitet. Geprüft: alle seit 21k neu abgelegten Dokumente gegen den Registerstand, den sie voraussetzen, und gegen meine eigenen Entscheidungen.*

---

## 1. Was seit 21k in der Ablage neu ist (fünf Dateien, alle gelesen)

| Datei | Zeit (Ablage, Ortszeit) | Von | Art | Änderung am Repo? |
|---|---|---|---|---|
| `RECHERCHE_vintage_datenlage.md` | 23:24 | „Rechercheeinheit des steuernden Chats" | Recherche zum Epic MI (hinter dem Tag geparkt) | nein |
| `FABLE_ANFRAGE_2026-09-21f_registertext_und_feldliste.md` | 23:26 | steuernder Chat, HEAD `a0c6eb0` | die angekündigte Vorlage; vier Fragen an mich | Register 33 eingetragen (TB-81) |
| `BESTANDSAUFNAHME_TB-30b.md` | 23:31 | **keine Herkunftszeile**, HEAD `6071f32` | lesende Vorarbeit | „kein Byte geändert" |
| `NACHTRAG_1_BESTANDSAUFNAHME_TB-30b.md` | 23:33 | dito | lesende Messung | nein |
| `NACHTRAG_2_BESTANDSAUFNAHME_TB-30b.md` | 23:36 | dito | lesende Messung | nein |

**Kein Dokument eines zweiten Fable-Chats** liegt in der Ablage; die Antwortkette a–k ist lückenlos meine. Falls im alten Fable-Chat etwas entstanden ist, ist es nicht abgelegt — und soll es auch nicht werden: Die Kette läuft hier.

## 2. Ergebnis: nichts ist verschossen

- **Kein Code, keine Freigabe verbraucht.** Alle drei Bestandsaufnahme-Dokumente sagen es ausdrücklich, und die Anfrage 21f setzt für alles Weitere eigene Freigaben voraus.
- **Kein Widerspruch zum Register 27–33.** Alle fünf Dokumente kennen 28.4, 29.4, 32 und 33.2 und zitieren sie richtig. Wer immer sie geschrieben hat, hat den aktuellen Stand gelesen.
- **Kein Widerspruch zu meinen Entscheidungen.** Nachtrag 1 (auswertung.py folgt Verfahren B, muss nicht geöffnet werden) ist genau die Lage, die 21b (3) geschützt hat. Nachtrag 2 (der Erzeuger der `zellen.csv` fehlt) widerspricht nichts, es ergänzt die Frist — siehe 4.
- **Sichtschutz:** Alle fünf halten 27.1 ein; die Recherche berührt den Selektionsraum nicht. Kein Befund, aus meiner Sicht — die Prüfung nach 27.4 in der Gegenrichtung bleibt eure.

## 3. Drei Beobachtungen, Handwerk

1. **Die Bestandsaufnahme-Dokumente tragen keine „Von:"-Zeile** und keinen Chat-Bezug — bei zwei parallel schreibenden steuernden Chats ist das genau die Lücke, durch die eine Ablage zwei Fassungen desselben Standes bekommt. Nachtragen, und den alten Chat schliessen oder als „nur lesend" kennzeichnen.
2. **Zwei HEADs:** Anfrage 21f misst an `a0c6eb0`, die Bestandsaufnahme an `6071f32` (= `origin/main`). Welcher jünger ist, steht nirgends. Eine Zeile „Vorgänger/Nachfolger" genügt.
3. **Zeitstempel:** Die Bestandsaufnahme nennt „Stand 23:55", wurde aber um 23:31 abgelegt und ihr Nachtrag 1 nennt 23:32. Tippfehler oder falsche Uhr; für ein Dokument, das Reihenfolge belegen soll (Frage vor Messung), zählt das.

## 4. Was daraus vor den Tag fällt

**(a) Aus Nachtrag 2, keine neue Regel, nur die Folge:** Der signierte Tag setzt voraus, dass der Lauf starten kann (Übergabe Abschnitt 1: HEAD = registrierter Commit, 5e). Ein Erzeuger, der nach dem Tag geschrieben wird, wäre nicht registriert. **Also: Erzeuger vor dem Tag, registriert wie jede andere Laufdatei.** Das verlängert die Strecke bis zum Tag; es ändert kein Wort im Register. Die Bestätigungsperiode-Grenze (2d) und 3b (a)–(e) werden in diesem Erzeuger wirksam — sein Code ist damit die Stelle, an der der Abgleich Registertext↔Verhalten am Ende zu prüfen ist.

**(b) Aus der Bestandsaufnahme Abschnitt 3 — eine Verfahrensfrage, die dort als Betreiberfrage geführt ist und meine ist. Entscheidung (Begründung nennt kein Ergebnis):**

> **Berichtigung zu 29.4:** Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun** `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern. Der Bericht führt je Bot Horizontbeginn (oder „kein Horizont"), Beginn der ersten Selektionsfalte und frühesten Einstieg nebeneinander auf.

*Quelle des Grundes:* Die Regel 29 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte) gilt je Bot für alle neun; 21c 3.2 hat den Fall für Krypto ausdrücklich benannt („rsi2_crypto: 2018 handelbar, erste Falte 2019"). „Die vier" stammt aus 21b, als die Wache noch gegen den Horizontbeginn prüfte, den nur Aktien-Bots haben. Mit dem Wechsel des Prüfdatums in 21c/29.4 hätte die Zahl mitwandern müssen; sie ist es nicht — mein Versehen, dieselbe Art wie der verlorene Vorlauf-Satz. Kein Ergebnis: Ob die Wache bei einem Krypto-Bot je anschlägt, ist für die Regel gleichgültig.

Kategorie: Berichtigung mit Ersatzwort, „vier" → „neun"; 29.4 bleibt stehen, Marke wie üblich.

## 5. Was jetzt bei mir liegt

Die Anfrage 21f mit ihren vier Fragen — sie ist die angekündigte Vorlage und wird in **21m** beantwortet, gleich anschliessend.

**Leseprotokoll dieses Chats, Stand jetzt:** Übergabe (beide Anhänge), 20e, 21a, 21b, ANFRAGE 21b, 21c, 21e, 21f, `BESTANDSAUFNAHME_TB-30b.md`, `NACHTRAG_1_…`, `NACHTRAG_2_…`, `RECHERCHE_vintage_datenlage.md`; Wortlaut Festlegungen 10–12 (vorgelegt); Registerauszüge im Zitat. Nicht gelesen: `REGISTER_KOPIE_2026-09-21.md`, ANFRAGE 21d, `BACKLOG.md`.

---

**Kurz:** Nichts verschossen — kein Code, keine Freigabe, kein Widerspruch zum Register oder zu meinen Entscheidungen, kein Sichtschutz-Befund. Drei Handwerkslücken: fehlende Herkunftszeile, zwei ungeordnete HEADs, ein Zeitstempel. Zwei Folgen vor dem Tag: der Erzeuger der `zellen.csv` muss vor dem Tag stehen und registriert sein; die Wache aus 29.4 gilt für alle neun Optimierer (Berichtigung „vier" → „neun", mein Versehen).

---

## In einfacher Sprache

Der Betreiber hat versehentlich in einem alten Steuer-Chat weitergearbeitet und wollte wissen, ob dabei etwas kaputtgegangen ist. Geprüft: Alle fünf neuen Dokumente haben nur gelesen und gemessen, nichts verändert, und sie kennen den aktuellen Regelstand. Es fehlt ihnen nur eine Absenderzeile — bei zwei parallel schreibenden Chats sollte die immer dastehen. Zwei Dinge folgen daraus: Das Programm, das den grossen Lauf zusammenbaut, gibt es noch nicht und muss vor dem Stichtag fertig und eingefroren sein. Und Fables Kontrollzeile in den Optimierern gehört in alle neun, nicht nur in die vier Aktien-Bots — ein Zahlwort, das beim Umschreiben nicht mitgewandert war.
