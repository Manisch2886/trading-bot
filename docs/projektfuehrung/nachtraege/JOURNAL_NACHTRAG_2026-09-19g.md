# Journal-Nachtrag (g) — 19./20.09.2026: TB-59, die Backlog-Einarbeitung

⚠️ **Nachgeholt am 20.09.2026 durch die Chat-Sitzung, nicht durch die
ausführende Mac-Sitzung** (Prüfprinzip A7: eine nachgeholte Messung sagt, dass
sie nachgeholt wurde). Der Zustand war inhaltsadressiert wiederherstellbar — der
Arbeitsbaum lag unverändert vor.

**Beleg:** `docs/ERGEBNIS_TB-59_backlog_einarbeitung.md`.

---

## Der Ergebnisblock

**TB-59 — Einarbeitung der Backlog-Nachträge (n) bis (u).** Mac-Sitzung,
19.09.2026, 23:14 bis 23:28 Ortszeit. Ausgangsstand `aa05cc1`.

| | gemessen |
|---|---|
| `BACKLOG.md` | **951 → 1 959 Zeilen**, `numstat` **1008 / 0** |
| `ARBEITSWEISE.md` | **819 → 775 Zeilen**, `numstat` **23 / 67**, ein einziger Hunk `@@ -674,67 +674,23 @@` am Ankertext |
| Kollisionsprobe | **24 Blockbezeichner**, keiner doppelt · **`K2a`–`K2z` und `K3a`–`K3j`** je genau einmal |
| Nummernvermerke | **20**, alle in der Form *„im Nachtrag (x) als `Y` vorgeschlagen; … vergeben als `Z`, gemessen"* |
| Ausserhalb `docs/` geändert | **0 Dateien** |

**Neue Blöcke:** `2s` (TB-56b und Fables Methodenantwort), `2t` Epic **AF**,
`2u` Epic **MI**, `2v` Epic **QR**, `2w` Epic **KG**, `2x` Epic **RT**,
`2y` Querschnitt über (n)–(r).

**`ARBEITSWEISE.md` Abschnitt 10** ist durch den Verweis auf `UMZUG.md` ersetzt.

---

## ⭐⭐ Zwei Stellen, an denen die Sitzung dem Auftrag widersprach — und beide Male recht hatte

| | Der Auftrag sagte | Gemessen |
|---|---|---|
| **1** | *„erwartet werden **70** entfernte Zeilen"* | **67.** Die 70 war aus `743 − 674 + 1` **gerechnet, nicht nachgezählt**; die drei Zeilen vor Abschnitt 11 sind Trenner. ⭐ **Die Sitzung hielt sich an die Ankertexte statt an die Zahl.** Hätte sie die 70 treffen wollen, hätte sie drei Zeilen entfernt, die niemand entfernen wollte |
| **2** | *„betroffen sind (n), (o), (p) und (q), mit **drei** Doppelbelegungen"* | **Vier.** `(p)` und `(q)` nennen zusätzlich `K3a` und `K3b`. ⚠️ **Das Suchmuster im Auftrag deckte nur `K2[a-z]` ab** und konnte `K3`-Nummern strukturell nicht sehen |

> ⭐⭐ **Die Lehre aus beiden: Ein falsches SOLL in einem *Auftrag* ist
> gefährlicher als eines in einem *Bericht* — dort liest es jemand als
> Anweisung.** Regel `K2o` (*„eine SOLL-Zahl ist gezählt, nicht geschätzt"*) gilt
> verschärft für Zahlen, die einer anderen Sitzung vorgegeben werden.

⚠️ **Und Fall 2 ist eine eigene Fehlerfamilie, eine Ebene über Block 7, Punkt 3:**
nicht *ein Name statt einer Messung*, sondern **eine Messung mit einem
Instrument, das den Suchraum nicht abdeckt.** ⭐ *Ein leeres Ergebnis und ein
blinder Sucher sehen gleich aus* (A1).

---

## ⚠️ Der Befund über die Auftragsform

**Drei von acht Auflagen blieben offen:** Commit und Push, Ergebnisdokument,
Journal-Nachtrag. **Die Arbeit lag rund elf Stunden ungesichert im
Arbeitsbaum** — auf einem Rechner, in keiner Version.

**Die Ursache liegt in der Form, nicht in der Sitzung:** Der Auftrag führte
Commit und Push als **Nachweis 6 am Ende der Liste**. Eine Sitzung, die ihre
inhaltliche Arbeit für fertig hält, ist damit fertig, **bevor sie gesichert
hat**.

> ⭐⭐ **Sichern ist keine Abgabe, sondern ein Schritt — und er gehört nicht ans
> Ende, sondern nach jeden abgeschlossenen Teil.**

⭐ **Dieselbe Begründung, die `UMZUG.md` Abschnitt 1 für die Übergabe führt:**
*„Wer sie erst beim Umzug schreibt, hat ein Zeitfenster, in dem ein unerwarteter
Abbruch Arbeit vernichtet. Wer sie laufend pflegt, hat keins."* **Für das Sichern
von Arbeit galt derselbe Satz bisher nicht.**

---

## In einfacher Sprache

**Was wir wissen wollten:** Sind die acht Notizen korrekt in die Aufgabenliste
eingearbeitet — ohne Verlust, ohne doppelte Nummern?

**Was herauskam:** Ja. Die Liste wuchs um 1 008 Zeilen, **keine einzige wurde
entfernt**, und jede der 36 Nummern kommt genau einmal vor. Zwanzig Nummern
mussten neu vergeben werden, weil die Notizen geratene Nummern enthielten; zu
jeder steht daneben, was ursprünglich dastand.

**Warum das so ist:** Der Auftrag verlangte Nachzählen statt Übernehmen — und an
zwei Stellen hat die Sitzung der Vorgabe widersprochen und hatte recht. Beide
Male stand in meinem Auftrag eine Zahl, die ich nicht nachgezählt hatte.

**Was das bedeutet:** Inhaltlich in Ordnung. Aber die Sitzung hat elf Stunden
nicht gespeichert, weil mein Auftrag das Sichern ans Ende gestellt hat. Künftig
wird nach jedem fertigen Teil gesichert.
