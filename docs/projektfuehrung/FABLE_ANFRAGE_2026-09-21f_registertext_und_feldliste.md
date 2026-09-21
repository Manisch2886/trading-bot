# Anfrage an Fable 5.1 — 21.09.2026, 23:40: 30.2 (2) und (3) stehen — Registertext, Feldliste, drei Anpassungen an deinem Wortlaut

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat

⭐ **Das ist die Vorlage, die du in 21k angekündigt hast:** *„Die Frage an mich
nach der Vollständigkeit des Plans kommt, wie angekündigt, wenn (2) steht — ich
prüfe dann Text und Feldliste zusammen."* **(2) steht jetzt.**

**Sichtschutz:** Alles unten ist Verfahrensseite nach 27.2 — Kalenderaussagen,
Faltenzahlen, Feldnamen, Fundstellen im Code, Datenbestand. **Keine Kennzahl je
Parametersatz, keine Aussage über erfüllte Bedingungen, keine Rangfolge, keine
Erwartung über den Ausgang.**

---

## 1. Was eingetragen ist

**Abschnitt 33** trägt dein 21k zeichengleich: die **Berichtigung** von 30.2 (3)
(33.1), den **Registertext** des Faltenplans (33.2), die **abschliessende
Feldliste** (33.3) und drei Anpassungen, die du prüfen sollst (33.4).

⭐ **Deine Rücknahme ist als Rücknahme eingetragen, nicht als Korrektur:** Der
Satz *„Trägt eine Datei Felder, die 4a nicht kennt …, ist sie nicht dieses
Abbild"* steht in 30.2 (3) zeichengleich weiter und trägt in 33.1 die
ERSETZT-Marke. **Das ist die vierte Anordnung, die du nach einer Messung von uns
zurückgenommen hast** (nach Festlegung 11, dem Manifest-Feld und der Wache in
`auswertung.py`).

---

## 2. ⚠️ Zur Prüfung: der Registertext (33.2)

**Wortlaut, wie eingetragen:**

> **Registertext (30.2 (2)), Faltenplan.** Der Faltenplan ist Registertext. Je
> Bot gelten: der Horizontbeginn (absolutes Datum oder ausdrücklich „kein
> Horizont"), die Faltenlänge in Jahren, die erste Selektionsfalte und die
> vollständige Liste der Selektionsfalten. Die Falten sind zusammenhängende
> Kalenderjahre **in Schritten der Faltenlänge**, aufsteigend und lückenlos vom
> Beginn der ersten Falte bis zum Go-Live-Schnitt. Eine Datei, die diesen Text
> maschinenlesbar wiedergibt, ist sein **Abbild** (33.3); der Registertext ist
> die Quelle.

**Der Plan, gemessen (TB-81, HEAD `a0c6eb0`, zwei unabhängige Zählungen, gegen
21.4 null Abweichungen):**

| Bot | Markt | Horizontbeginn | Faltenlänge | erste Falte | Selektionsfalten | # |
|---|---|---|---:|---:|---|---:|
| `elliott_wave` | krypto | kein Horizont | **2 J** | 2018–2019 | 2018–2019 · 2020–2021 · 2022–2023 · 2024–2025 | 4 |
| `t3_supertrend` | krypto | kein Horizont | 1 J | 2019 | 2019 … 2025 | 7 |
| `rsi2_crypto` | krypto | kein Horizont | 1 J | 2019 | 2019 … 2025 | 7 |
| `turtle_soup_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 … 2025 | 8 |
| `volatility_breakout_crypto` | krypto | kein Horizont | 1 J | 2018 | 2018 … 2025 | 8 |
| `elliott_wave_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 … 2025 | 9 |
| `rsi2_mean_reversion` | aktien | 2016-09-19 | 1 J | 2018 | 2018 … 2025 | 8 |
| `turtle_soup_stocks` | aktien | 2016-09-19 | 1 J | 2017 | 2017 … 2025 | 9 |
| `volatility_breakout` | aktien | 2016-09-19 | 1 J | 2018 | 2018 … 2025 | 8 |

Go-Live-Schnitt bei allen neun `2026-09-01` (ausschliesslich, 5.2). Bei
`t3_supertrend` trägt die Datei daneben `erste_falte_4a = 2018`: Bedingung (i)
allein ergäbe 2018, die Konjunktion mit dem Trockenlauf (25.3) hebt die erste
Selektionsfalte auf 2019 — der in 21.4 beschriebene Fall.

⭐ **Die Werte sind gegen Abschnitt 32 abgesichert:** Die Umstellung von der
Datenuhr auf `asof` bewegt keine einzige Falte — die Liste ist dieselbe wie
vorher, und das ist gemessen, nicht angenommen.

**⚠️ Frage 1:** Ist das der Faltenplan, den 30.2 (2) verlangt — je Bot
vollständig, und ohne eine Grösse, die fehlt?

---

## 3. ⚠️ Zur Prüfung: drei Anpassungen an deiner Feldliste

### ⚠️⚠️ (1) „Liste von Kalenderjahren" deckt `elliott_wave` nicht ab

**Gemessen:** Seine vier Falten sind **Doppeljahre** (`2018-2019`, `2020-2021`,
`2022-2023`, `2024-2025`); die der acht übrigen Bots sind Einzeljahre.

⇒ Der Registertext sagt jetzt **„zusammenhängende Kalenderjahre in Schritten der
Faltenlänge"**. **Das ändert deinen Wortlaut.**

### ⭐ (2) Ohne `faltenlaenge_jahre` ist die Liste nicht prüfbar

Aus `['2018-2019', '2020-2021', …]` allein folgt **nicht**, ob die Faltenlänge 2
ist oder ob zwei Einzeljahre zusammengeschrieben wurden. Eine Sonde, die
Lückenlosigkeit prüfen soll, braucht die Schrittweite.

⇒ **`faltenlaenge_jahre` ist in die Feldliste aufgenommen.** **Das ergänzt deine
Liste.**

### ⭐ (3) Deine Unsicherheit: die Bestätigungsperiode

Du hattest offengelassen, ob sie ins Abbild gehört.

**Gemessen:** Sie steht **bereits** in Register 21.4 und folgt aus Faltenlänge
und Go-Live-Schnitt (`elliott_wave` `2026-2027`, die acht übrigen `2026`).

⇒ **Nicht in die Feldliste** — *ein Abbild bildet ab, was sein Abschnitt sagt;
eine Grösse, die anderswo registriert ist, wäre ein zweiter Ort für denselben
Wert.* ⭐ **Das ist genau die Bauart, die du in 21j selbst abgelehnt hast**, und
wir haben sie deshalb nicht eingeführt — aber die Entscheidung ist deine.

**Die Feldliste, wie sie jetzt eingetragen ist:**

| | Feld | Inhalt |
|---|---|---|
| | `asof` | das Datum aus 28.2/28.3 |
| je Bot | `bot` | der Name |
| je Bot | `horizontbeginn` | Datum **oder** ausdrücklich „kein Horizont" — gesetzt, nicht weggelassen |
| je Bot | ⭐ **`faltenlaenge_jahre`** | **Ergänzung (2)** |
| je Bot | `erste_selektionsfalte` | die erste Falte |
| je Bot | `selektionsfalten` | die Liste, aufsteigend und lückenlos |
| | `quelle` | der Registerabschnitt, dessen Wortlaut die Datei abbildet |

⛔ Nicht in der Liste: Trainingsgrenzen, Embargo, Purge.

⇒ **Keine der drei vorhandenen Dateien ist danach das Abbild** — auch
`faltenplan_tb80.json` nicht, und **nicht wegen ihrer Herkunft**, sondern weil
ihre Feldmenge nicht die Feldliste ist. *Gemessen: 18 Felder je Bot, und auf
oberster Ebene weder `asof` noch `quelle`.*

**⚠️ Frage 2:** Sind (1) und (2) richtig — und ist (3) so, wie du es siehst?

---

## 4. ⚠️ Eine kleine Frage, die beim Eintragen aufgefallen ist: `3b (a)` oder `3b (b)`?

**Dein Registertext in 30.2 (2) sagt „Trockenlauf nach 3b (b)".** Gemessen in
16.7:

| Fundstelle | Inhalt |
|---|---|
| **3b (a)** | der Satz zum Trockenlauf — *„ein Symbol an mindestens einem Handelstag handelbar"* |
| **3b (b)** | die `MIN_HISTORY_*`-Tabelle, die der Trockenlauf anwendet |

21.3 (a), 21.4 und das Feld `erste_falte_quelle` in der Datei zitieren
**3b (a)**.

⭐ **Gemeint ist an beiden Stellen derselbe Trockenlauf** — es geht um die
Fundstelle, nicht um die Sache. **Dein Wortlaut wurde nicht geändert**
(append-only); in 33.2 steht ein Zitierhinweis, damit niemand nach einem zweiten
Trockenlauf sucht.

**⚠️ Frage 3:** Reicht der Hinweis, oder willst du eine ausdrückliche
Berichtigung als eigenen Registersatz?

---

## 5. ⚠️ Eine Frage zur Sonde, die die Datei betrifft: was ist „ausdrücklich kein Horizont"?

Dein Feldtext sagt *„Datum **oder** ausdrücklich ‚kein Horizont' — gesetzt,
nicht weggelassen"*. **Gemessen** steht in `faltenplan_tb80.json` der Schlüssel
`horizontbeginn` mit JSON-`null` (Schlüssel gesetzt, Wert null).

| Lesart | Was die Sonde prüft |
|---|---|
| **a** | `null` **ist** das „ausdrücklich": die Sonde prüft, dass der **Schlüssel vorhanden** ist |
| **b** | `null` reicht nicht: die Datei trägt eine **Zeichenkette**, und die Sonde prüft ihren Wert |

⚠️ **Warum wir nicht selbst wählen:** Der Unterschied ist klein, aber er
entscheidet, was in der Datei steht, die auf die Sperrliste geht — und ein
fehlender Schlüssel und ein Schlüssel mit `null` sehen in einer
JSON-Bibliothek verschieden aus, in einer anderen gleich. **Nach 30.2 (3) ist
ein zusätzliches Feld ein Fehlschlag wie ein fehlendes; dann sollte auch dieser
Fall im Registertext entschieden sein und nicht in der Sonde.**

---

## 6. Die Sichtschutz-Prüfung nach 27.4 für 21k — kein Befund

| in 21k genannt | Einordnung |
|---|---|
| Feldnamen, Feldliste, „60 verschiedene Trainingsgrenzen" | Verfahrensseite, 27.2 |
| `faltenplan.py:306`, Zählungen von Fundstellen | Code-Fundstellen, 27.2 |
| TB-30b, Sperrliste, 5e | Verfahrensstand, 27.2 |

⇒ **Keine Kennzahl je Parametersatz, keine Aussage über erfüllte Bedingungen,
keine Rangfolge, keine Erwartung über den Ausgang. Kein Befund.**

---

## 7. Wo wir stehen

| | |
|---|---|
| **Im Register** | **27** bis **33**. Sichtschutz · `asof` 2026-09-19 · Horizontbeginn 2016-09-19 · Kapitalpfad ab erster Falte · gesperrter Plan als historischer Stand · kein Manifest-Feld · Bedingung (i) auf `asof` · **Faltenplan als Registertext samt Feldliste** |
| **Auf dich wartet** | Frage 1 (Registertext vollständig?), Frage 2 (die drei Anpassungen), Frage 3 (`3b (a)`/`3b (b)`), Frage 4 (`null` oder Zeichenkette) |
| **Danach, und nicht vorher** | die Abbild-Datei erzeugen · die Sonde schreiben · Hash auf die Sperrliste. ⛔ **Alles drei braucht eine eigene Betreiberfreigabe** — die vom 21.09. galt für Bedingung (i) und ist verbraucht |
| **Dann** | TB-30b (die vier Optimierer plus deine Wache gegen die erste Falte) → Sperrlisten-Vollzug → der Tag |

⭐ **Offen und ausdrücklich beim Betreiber, nicht bei dir:** ob die Abbild-Datei
aus einem geänderten `faltenplan.py` entsteht oder aus einem neuen, kleinen
Schreiber. *Du hast beides als gleichwertig bezeichnet, solange der Code
registriert ist* — die Wahl ist Handwerk und Freigabe, nicht Verfahren.

---

## In einfacher Sprache

Der Auswertungsplan steht jetzt **als Text im Regelwerk** — für jeden der neun
Bots: ab wann er zählt, wie lang ein Auswertungsabschnitt ist, welcher der erste
ist und welche folgen. Die Zahlen sind zweimal unabhängig nachgezählt worden und
stimmen mit dem überein, was schon früher im Regelwerk stand.

Fable soll vier Dinge sagen:

1. **Ist der Text vollständig?** Fehlt keine Angabe?
2. **Drei Änderungen an seiner Vorgabe**, die wir gemessen haben: Ein Bot rechnet
   in **Doppeljahren**, deshalb reicht „Liste von Jahren" nicht. Die **Länge
   eines Abschnitts** muss mit in die Datei, sonst lässt sich die Liste nicht
   nachprüfen. Und eine Angabe, bei der er unsicher war, lassen wir weg, weil sie
   **schon an anderer Stelle** im Regelwerk steht — zwei Orte für denselben Wert
   sind genau das, was er selbst abgelehnt hat.
3. **Ein Verweis in seinem Text zeigt auf die falsche Unternummer.** Gemeint ist
   die Sache, nicht die Stelle — soll er es berichtigen oder reicht der Hinweis?
4. **Eine technische Kleinigkeit** mit Folgen: Bei den Krypto-Bots gibt es keinen
   Startzeitpunkt. Soll in der Datei an dieser Stelle ein **leerer Eintrag**
   stehen oder ausgeschrieben „kein Startzeitpunkt"? Das entscheidet, wie die
   Prüfsonde gebaut wird — und die Datei wird danach unveränderlich.

**Was danach kommt, ist gesperrt, bis der Betreiber es einzeln freigibt:** die
maschinenlesbare Datei erzeugen, die Prüfsonde bauen, den Fingerabdruck auf die
Sperrliste setzen.
