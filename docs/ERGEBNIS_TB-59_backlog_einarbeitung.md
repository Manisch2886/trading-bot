# ERGEBNIS TB-59 — Einarbeitung der Nachträge (n) bis (u)

⚠️⚠️ **Dieses Dokument ist KEIN Selbstbericht der ausführenden Sitzung.** Die
TB-59-Mac-Sitzung hat die Arbeit ausgeführt, aber die Abgabe nach Abschnitt 6
des Auftrags nicht geliefert. **Die Nachweise hier sind am 20.09.2026 von der
Chat-Sitzung über die Geräteanbindung unabhängig nachgemessen worden**, rein
lesend, am Arbeitsbaum.

⚠️ **Nachgeholt, und das gehört dazugesagt** (Prüfprinzip A7): Die Messung fand
**nach** der Arbeit statt, nicht währenddessen. Was dadurch nicht mehr messbar
ist, steht in Nachweis 1 ausdrücklich als *nicht prüfbar* — nicht als grün.

⭐ **Der Umstand hat auch einen Vorteil, und er ist der einzige Grund, warum
diese Form überhaupt tragfähig ist:** Das Projekt führt als Prüfprinzip, dass
eine Prüfung durch jemanden, der das Werkzeug nicht gebaut hat, mehr wiegt als
ein Selbstbericht (Backlog **Q2**, Punkt 3). **Hier hat der Prüfer die Arbeit
nicht gemacht.**

---

## Die sieben Nachweise aus Abschnitt 6 des Auftrags

| # | Nachweis | Ergebnis |
|---:|---|---|
| **1** | `git status --short` **vor** dem ersten Schreiben | ⚠️ **NICHT PRÜFBAR — nachträglich nicht mehr messbar.** Belegt ist nur der Zustand **davor**: Commit `aa05cc1` wurde von der Sitzung selbst als Schritt 0 erzeugt, danach war der Baum sauber. *Nicht grün, nicht rot — nicht prüfbar (A2)* |
| **2** | `git diff --numstat` je Datei | ⭐ `1008  0  docs/projektfuehrung/BACKLOG.md` · `23  67  docs/projektfuehrung/ARBEITSWEISE.md` |
| **3** | Zeilenzahl `BACKLOG.md` vorher / nachher | **951 → 1 959** (+1 008), **0 entfernte Zeilen** |
| **4** | Nummernnachweis „ursprünglich genannt → vergeben" | ⭐ **20 Vermerke**, alle in der verlangten Form. Tabelle unten |
| **5** | Gegenprobe auf Kollisionen | ⭐ **24 Blocküberschriften, keine doppelt** · **`K2a` bis `K2z` je genau einmal** · `K3a` bis `K3j` je genau einmal |
| **6** | `git status --porcelain` **nach** dem letzten Commit | ⚠️ **OFFEN** — es hat keinen Commit gegeben. Siehe „Was die Sitzung schuldig blieb" |
| **7** | Nichts ausserhalb `docs/` geändert | ⭐ **0 Dateien** ausserhalb `docs/` — gemessen über `git diff --name-only` |

---

## Nachweis 4 — die Nummernvergabe, vollständig

**Wortlaut des ersten Vermerks, zur Form:**

> `**K2p** *(im Nachtrag (n) als `K2r` vorgeschlagen; `K2r` war zum Zeitpunkt der
> Einarbeitung nicht die nächste freie — vergeben als `K2p`, gemessen)*`

| vergeben | vorgeschlagen war | aus Nachtrag |
|---|---|---|
| `K2p` | `K2r` | (n) |
| `K2q` | `K2s` | (n) |
| `K2r` | `K2t` | (n) |
| `K2s` | `K2u` | (o) |
| `K2t` | `K2v` | (o) |
| `K2u` | `K2w` | (o) |
| `K2v` | `K2x` | (o) |
| `K2w` | `K2y` | (p) |
| `K2x` | `K2z` | (p) |
| `K2y` | `K3a` | (p) |
| `K2z` | `K3b` | (p) |
| **9 weitere** | aus (q) und (r) | ⭐ auf `K3a` bis `K3j`, gleiche Form |

⭐ **Die Vergabe ist lückenlos fortlaufend ab der gemessenen freien Nummer.**
`K2l` bis `K2o` waren durch die Nachträge (s) und (t) belegt, die Vergabe beginnt
bei `K2p` und läuft ohne Sprung bis `K3j`. **Der K2-Namensraum ist damit
erschöpft; die nächste freie Nummer ist `K3k`.**

### ⚠️ Eine Berichtigung am Auftrag selbst — der Fehler lag bei mir

**Abschnitt 2.2 des Auftrags behauptete:** *„betroffen sind (n), (o), (p) und
(q), mit drei Doppelbelegungen."*

⚠️ **Gemessen am 20.09.2026 mit einem Muster, das auch `K3` erfasst:** `(p)`
nennt zusätzlich `K3a` und `K3b`, `(q)` nennt `K2x`, `K2y`, `K2z`, `K3a`, `K3b`.
**Die Doppelbelegungen zwischen (p) und (q) sind vier, nicht drei.**

> ⭐ **Die Ursache: Das Suchmuster im Auftrag deckte nur `K2[a-z]` ab.** Es konnte
> `K3`-Nummern strukturell nicht sehen. **Die Schlussfolgerung — jede
> vorgeschlagene Nummer als Platzhalter behandeln und neu messen — war richtig
> und hat getragen; die Zahl daneben war zu klein.**

⚠️ **Dieselbe Fehlerfamilie wie Block 7, Punkt 3, nur eine Ebene höher:** nicht
ein Name statt einer Messung, sondern **eine Messung mit einem Instrument, das
den Suchraum nicht abdeckt.** ⭐ *Ein leeres Ergebnis und ein blinder Sucher
sehen gleich aus (A1).*

---

## Nachweis 2, zweite Zeile — der Ersatz in `ARBEITSWEISE.md`

**Ein einziger Hunk:** `@@ -674,67 +674,23 @@` — genau am verlangten Ankertext
`## 10. Die Sitzungsuebergabe`. Abschnitt 10 heisst jetzt *„Der Umzug in einen
neuen Chat"*, die Abschnitte 11, 12 und 13 folgen unverändert.

⚠️⚠️ **Der Auftrag nannte 70 entfernte Zeilen. Es sind 67. Der Fehler lag im
Auftrag, nicht in der Ausführung.**

Die Zahl 70 war aus `743 − 674 + 1` **gerechnet, aber nicht nachgezählt**: Die
drei Zeilen vor Abschnitt 11 sind Trenner und gehörten nicht zum Abschnitt.

> ⭐⭐ **Die Sitzung hat sich an die Ankertexte gehalten statt an meine Zahl — und
> genau das war richtig.** Hätte sie die 70 treffen wollen, hätte sie drei Zeilen
> entfernt, die niemand entfernen wollte. **Ein falsches SOLL in einem Auftrag
> ist gefährlicher als eines in einem Bericht: dort liest es jemand als
> Anweisung.**

⇒ **Regel `K2o` (*„eine SOLL-Zahl ist gezählt, nicht geschätzt"*) gilt
verschärft für Zahlen, die einer anderen Sitzung vorgegeben werden.**

---

## Was die Sitzung schuldig blieb — und was daraus folgt

| | Auflage | Stand |
|---|---|---|
| ⚠️⚠️ | **Commit und Push** | **nicht erfolgt.** Die Arbeit lag rund elf Stunden **ungesichert** im Arbeitsbaum — ein Rechner, keine Version |
| ⚠️ | **Ergebnisdokument** | nicht erstellt; **dies ist der Ersatz**, unabhängig gemessen |
| ⚠️ | **Journal-Nachtrag** | nicht erstellt; nachgeholt als `JOURNAL_NACHTRAG_2026-09-19g.md` |

⭐ **Die Lehre, und sie betrifft die Auftragsform, nicht die Sitzung:** Der
Auftrag führte Commit und Push als **Nachweis 6 am Ende der Liste**. Eine
Sitzung, die ihre Arbeit für fertig hält, ist damit fertig, **bevor sie
gesichert hat**.

> ⚠️ **Sichern ist keine Abgabe, sondern ein Schritt — und er gehört nicht ans
> Ende, sondern nach jeden abgeschlossenen Teil.**

⭐ *Dieselbe Begründung wie in `UMZUG.md` Abschnitt 1, dort für die Übergabe:
„Wer sie erst beim Umzug schreibt, hat ein Zeitfenster, in dem ein unerwarteter
Abbruch Arbeit vernichtet. Wer sie laufend pflegt, hat keins."* **Für das
Sichern von Arbeit galt derselbe Satz bisher nicht — er gilt ab jetzt.**

---

## Bewertung

⭐ **Die Arbeit selbst ist gut.** Die drei Zahlen, die tragen, halten: **1008 / 0**
im Backlog, **ein** Hunk genau am Ankertext in der Arbeitsweise, **keine
Kollision** bei 24 Blöcken und 36 K-Nummern. Die 20 Nummernvermerke sind
vollständig und in der verlangten Form. **Die Sitzung hat an zwei Stellen dem
Auftrag widersprochen und lag beide Male richtig** — bei den 67 Zeilen und bei
den `K3`-Nummern, die mein Muster nicht gesehen hatte.

⚠️ **Die Abgabe ist es nicht.** Drei von acht Auflagen offen, darunter die
einzige, die Arbeit vor Verlust schützt.

---

## In einfacher Sprache

**Was wir wissen wollten:** Hat die Sitzung die acht Notizen korrekt in die
Aufgabenliste einsortiert — ohne dass etwas verschwindet und ohne dass zwei
Einträge dieselbe Nummer bekommen?

**Was herauskam:** Ja. Die Liste ist von 951 auf 1 959 Zeilen gewachsen, und
**keine einzige Zeile wurde dabei entfernt** — das ist maschinell nachgewiesen.
Jede der 36 Nummern kommt genau einmal vor. Zwanzig Nummern musste die Sitzung
neu vergeben, weil die Notizen geratene Nummern enthielten; zu jeder steht
daneben, was ursprünglich dastand.

**Warum das so ist:** Die Aufgabe war so geschrieben, dass die Sitzung nachzählen
musste statt zu übernehmen — und an zwei Stellen hat sie **meiner** Vorgabe
widersprochen und hatte recht. Einmal hatte ich eine Zeilenzahl geschätzt statt
gezählt, einmal hatte ich mit einem Suchmuster gemessen, das einen Teil der
Nummern gar nicht sehen konnte.

**Was das für dich heisst:** Die inhaltliche Arbeit ist in Ordnung und kann
gesichert werden. Der Haken ist ein anderer: **Die Sitzung hat elf Stunden lang
nicht gespeichert.** Ein Absturz oder ein versehentliches Zurücksetzen hätte
alles gekostet. Das liegt an der Form meines Auftrags, der das Sichern ans Ende
gestellt hat — künftig wird nach jedem fertigen Teil gesichert, nicht erst zum
Schluss.
