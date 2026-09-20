# Journal-Nachtrag (b) — 20.09.2026, Mittag: die Beauftragung von TB-61 und TB-62

**Chat-Sitzung, 11:55 bis 12:45 Ortszeit.** Keine Mac-Sitzung, keine Rechnung —
alles rein lesend über die Geräteanbindung gemessen, Stand `79742d1` bis
`104fb1f` (fünf Commits).

---

## Der Befund, der die Kette vor dem Tag verändert

⭐⭐ **`benchmark_drawdowns.json` ist für ALLE NEUN Bots überholt** — und vier
davon behaupten das Gegenteil.

| Bot | `status` in der Datei | `falten` dort | nach Registerabschnitt 21 |
|---|---|---|---|
| fünf Krypto-Bots | `platzhalter` | *leer* | 2018/2019, 4 bis 8 Falten |
| `elliott_wave_stocks`, `turtle_soup_stocks` | ⚠️ **`endgueltig`** | **ab 2019** | **2017**, 9 Falten |
| `rsi2_mean_reversion`, `volatility_breakout` | ⚠️ **`endgueltig`** | **ab 2019** | **2018**, 8 Falten |

⚠️ **Die vier Aktienzeilen tragen noch die Falten der mit TB-56 entfernten
Schranke.** Gesucht wurde die leere `dd_toleranz` der fünf Krypto-Bots; die vier
überholten Aktienzeilen fielen nur auf, **weil die Gegenprobe alle neun ausgab
statt nur der fünf**.

⇒ ⭐⭐ **Die Lehre: Ein Zustand, der sich selbst als fertig bezeichnet, wird
nicht nachgeprüft — ein Platzhalter schon.** *Eine Gegenprobe gibt alle Zeilen
aus, nicht nur die verdächtigen.*

### Die Ursache des Platzhalters besteht seit Tagen nicht mehr

`research/vorregistrierung/faltenplan.py:216`, `plan_krypto()`, Docstring:
*„keine Jahreszahlen bis TB-31 gemeldet hat"* — und `benchmark.py:176`
überspringt den Bot daraufhin mit `continue`.

**Gemessen: TB-31 ist seit PR #105 erledigt, TB-34 hat den Kursbestand neu
aufgebaut (`data/`: 223 Dateien, gezählt), die Krypto-Falten stehen seit TB-56b
in Registerabschnitt 21.** Drei Dokumente schrieben *„das hängt an TB-31"*
voneinander ab.

⇒ ⭐ **Wer einen Platzhalter setzt, nennt die Bedingung UND den Ort, an dem ihr
Eintreten sichtbar wird.** Sonst wartet der Code auf ein Ereignis, das längst
stattgefunden hat, und niemand prüft es nach, weil die Begründung plausibel
klingt.

### Und damit erklärt sich der eine rote Test

`auswertung.py:237` liest `eintrag["falten"][z["falte"]]`, sucht die Falte
`2017` und findet in der Tabelle erst `2019`. **Das ist der `KeyError: '2017'`.**

⚠️ *Nicht gemessen, sondern erschlossen: dass TB-61 ihn grün macht. Das ist zu
prüfen, nicht vorauszusetzen* (Nachweis 7 des Auftrags).

---

## ⚠️⚠️ Die Lehre des Tages, und sie ist unangenehm: fünf Messfehler derselben Familie

**An einem Tag, alle mit demselben Muster: ein Instrument, das seinen eigenen
Suchraum nicht abdeckt.**

| | Muster | Folge |
|---|---|---|
| **1** | `K2[a-z]` | sah `K3`-Nummern strukturell nicht — „drei Doppelbelegungen" statt vier |
| **2** | `743 − 674 + 1` | **gerechnet statt gezählt** — 70 entfernte Zeilen statt 67, und die Zahl stand in einem *Auftrag* |
| **3** | Filter auf `---` | verwechselte Markdown-Trenner mit Diff-Kopfzeilen — 546 statt 561 |
| **4** | `^\| \*\*K..\*\* \|` **mit** schliessendem Balken | übersah jede Zeile mit Vergabevermerk — „43 Zeilen, 41 Nummern" statt **64 und 62** |
| **5** | „Pflichtlektüre, sechs Dokumente" | ⚠️ **falsche Bezugsmenge** — der Lesepfad nennt **vier**. Die Erfolgszahl −111 747 Bytes war sechsmal richtig gerechnet, über die falschen Dateien |

⭐⭐ **Fall 4 ist der lehrreichste: Die Ausnahme, an der das Muster scheiterte,
war ausgerechnet der Vergabevermerk, den TB-59 eingeführt hat, um genau diese
Nummern nachvollziehbar zu machen.** *Die Sorgfaltsmassnahme hat die Kontrolle
blind gemacht.*

⭐ **Fall 5 ist eine eigene Klasse:** nicht ein zu enges Muster, sondern eine
**Bezugsmenge, die nie an der Quelle nachgelesen wurde.**

⇒ **Zwei Regeln:**
1. **Ein Messergebnis wird gegen eine zweite, unabhängig geschriebene Zählung
   gehalten, bevor es als Nachweis gilt.**
2. **Eine Kennzahl nennt die Menge, über die sie läuft — und die Menge wird an
   ihrer Quelle nachgelesen, nicht erinnert.**

### Der richtige Verlauf der Pflichtlektüre, je Commit nachgerechnet

| Commit | Zeit | Bytes |
|---|---|---:|
| `aa05cc1` | 19.09. 23:14 | 348 090 |
| `0bb4c92` | 20.09. 10:43 | **443 587** ← Höchststand |
| `c04b348` | 20.09. 11:37 | **318 005** ← Tiefstand, nach dem Archiv |
| `198fc32` | 20.09. 12:27 | 324 330 |

**Vom Höchststand −119 257 (−26,9 %), vom Sitzungsbeginn nur −23 760 (−6,8 %)** —
weil `ARBEITSWEISE.md` am selben Tag um **+12 571 Bytes** gewachsen ist.

⚠️ **Und seit dem Tiefstand um 11:37 ist die Pflichtlektüre in 50 Minuten wieder
um 6 325 Bytes gewachsen** — genau das, was `K3q` vorhergesagt hat.

---

## Zwei Träger, die auseinandergelaufen sind

### ⚠️⚠️ Nachtrag (m) wurde nie eingearbeitet

Seine sechs Nummern `K2l`–`K2q` sind im Backlog an **andere Inhalte** vergeben.
Vier seiner Regeln stehen inhaltlich anderswo. **Zwei stehen nirgends im Repo**,
mit vier Mustern gesucht:

> **(1)** *„Jede Rückfrage an den Betreiber und seine Antwort kommen wörtlich in
> den Bericht — sonst leben sie nur im Sitzungsverlauf, der mit der Sitzung
> verschwindet."*
>
> **(2)** *„Die Sitzung committet ihren eigenen Auftrag mit und ihre Belege."*

⭐⭐ **Regel (1) ist die Pointe: sie ist genau die Vorschrift, die verhindern
soll, dass Betreiberentscheidungen nur im Chat leben — und sie ist selbst im
Chat geblieben.**

### ⚠️⚠️ Die Projektablage ist ein Träger ohne Nachziehverfahren

**Gemessen 12:34:** Die Ablage trug `BACKLOG.md` im Stand von **09:43 UTC**, also
**vor** den TB-61-Berichtigungen. Eine neue Sitzung hätte nach dem
Eröffnungstext gelesen: *„das hängt an TB-31"* — **genau den Satz, den dieselbe
Stunde als überholt nachgewiesen hat.**

⭐ **Die Ursache ist kein Versäumnis, sondern eine Lücke:** Das Repo wird per
Commit nachgezogen, die Erinnerung beim Schreiben — **für die Ablage gab es
keinen Schritt, der sie auslöst.**

⇒ ⭐⭐ **Regel: Wer ein Führungsdokument committet, lädt es im selben Zug in die
Projektablage.** Nachgezogen: alle sieben Dokumente, per Suche gegengeprüft.

---

## ⭐ Betreiberentscheidung: ZIP wird überall abgeschafft

**Vorgelegt als Widerspruch in EINER Datei:** `ARBEITSWEISE.md` Abschnitt 1
verlangte auf acht Zeilen *„Immer gebündelt als ZIP"*, Abschnitt 10 derselben
Datei nannte ZIP *„überholt"*.

⚠️ **Und die Entscheidung stand bereits seit dem 19.09. in der Übergabe**,
Block 8, Regel 9: *„Keine ZIPs, nichts nach `~/Downloads`"* — **sie war
aufgeschrieben und nie in den zuständigen Träger übernommen.** Derselbe
Mechanismus wie bei Nachtrag (m).

**Entscheidung 20.09.2026: (a) — ZIP überall abgeschafft.** Ergebnisse kommen als
Commit im Repo und als einzelne Dateien im Chat.

⭐ **Der Zweck der alten Regel bleibt und wechselt nur das Mittel:** *ein Beleg
muss die Sitzung überleben.* Dafür sorgte das Archiv, künftig der Commit — **und
er ist der stärkere Träger**, weil ein Archiv in `~/Downloads` in keiner Version
liegt.

⚠️ **Der Umbau (TB-62, Schritt 4) unterscheidet drei Gruppen:** Vorschrift
(umschreiben) · Redewendung (umformulieren) · **historischer Beleg (unverändert
lassen)**. *Eine veränderte Beleg-Stelle wäre der einzige Fehler dieser Aufgabe,
der niemandem auffällt.*

---

## Was beauftragt wurde

| | | Art |
|---|---|---|
| **TB-61** | `docs/auftraege/MAC_TB-61_benchmark_neun.md`, 277 Zeilen | ⚠️ **rechnet**, braucht `trading-env`. Lauf **daneben** nach `benchmark_drawdowns_neu.json`; ⛔ die gesperrte Datei bleibt byteweise unverändert (SHA-256 `a163c498…36d1ee` als Nachweis) |
| **TB-62** | `docs/auftraege/MAC_TB-62_nachtraege_m_v.md`, 325 Zeilen | Dokumentation, rechnet nicht |

⭐ **`AKTUELLER_AUFTRAG.md` führt jetzt beide als Tabelle**, und der Einfügesatz
wählt die Zeile über die vorangestellte TB-Nummer aus — **kommt sie nicht vor,
bricht die Sitzung ab.**

⚠️ **Nie gleichzeitig starten** — beide schreiben nach `docs/`.

---

## ⚠️ Zwei eigene Fehlgriffe, ohne die es unvollständig wäre

| | |
|---|---|
| **1** | **Zweimal `git status --porcelain` über die Geräteanbindung** benutzt, was Block 7 Punkt 8 verbietet. Sofort geprüft: **kein `.git/index.lock` zurückgeblieben.** *Folgenlos aus Glück, nicht aus Wissen* |
| **2** | **Der TB-62-Auftrag trug ein falsches SOLL** — `K4d` als nächste freie Nummer und „19 Nummern". Beides war beim Schreiben richtig und **eine halbe Stunde später falsch**, weil der Nachtrag weiter wuchs. ⭐ **Nicht korrigiert, sondern entfernt:** die Sitzung zählt selbst |
| **3** | **Ein Python-Skript scheiterte am deutschen Schlusszeichen** `"` im Quelltext — dieselbe Falle wie gestern. **Es scheiterte beim Parsen, also wurde keine Datei berührt.** Neu geschrieben mit Hilfsvariablen statt Literalen |

---

## In einfacher Sprache

**Was wir wissen wollten:** Was blockiert eigentlich den signierten Tag?

**Was herauskam:** Eine einzige Datei — die Tabelle, die für jeden Bot festlegt,
wie tief er fallen darf. Sie ist bei fünf Bots leer und bei den anderen vier auf
falschen Jahren. **Und der Grund, warum sie leer ist, besteht seit Tagen nicht
mehr:** Der Code wartet auf eine Aufgabe, die längst erledigt ist, weil niemand
ihm gesagt hat, dass sie fertig ist.

**Was das für dich heisst:** Ein Lauf schliesst drei offene Punkte auf einmal —
die fehlenden Zahlen, die falschen Jahre und den einen roten Test. Der Auftrag
dafür liegt bereit und fasst die gesperrte Datei nicht an.

**Und was mich heute beschäftigt hat:** Fünf meiner Messungen waren falsch, alle
auf dieselbe Weise — ich habe mit einem Werkzeug gesucht, das einen Teil des
Suchraums gar nicht sehen konnte. Darunter die Erfolgszahl, die ich dir heute
Vormittag gemeldet habe. Die Dokumentation ist geschrumpft, aber um 24 000
statt um 112 000 Bytes.
