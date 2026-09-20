# Anfrage an Fable 5.1, bestehender Chat — 20.09.2026, fünfte

**Die Messung, die seinen Vorschlag umsetzen sollte, widerlegt seine Prämisse.
Das Auseinanderlaufen von 4a und 3b (a) ist nicht einseitig — und 21.3 (b)
wörtlich gelesen gäbe vier Aktien-Bots Selektionsfalten ab 1967.**

**Herkunft:** TB-72 sollte `faltenplan.py` die erste Falte aus dem Trockenlauf
ableiten lassen (Fables Antwort vom 20.09., Abschnitt 2 Punkt 2). **Schritt 1
war die Messung, die der Auftrag ausdrücklich in beide Richtungen verlangt
hat** — und sie hat den Auftrag angehalten, bevor eine Zeile Code geändert
wurde. *Die Sitzung ist danach durch einen Verbindungsabbruch beendet worden;
die Messung liegt vor, geändert wurde nichts.*

**Die Antwort gehört in den Chat, der TB-61 bis TB-72 bearbeitet.**

---

## Warum die Frage nicht selbst entschieden wird

| | |
|---|---|
| ⚠️⚠️ | **Der Registertext und seine eigene Begründung sagen Verschiedenes.** 21.3 (b) sagt *„bindet 3b (a)"* ohne Richtung; die Begründung im selben Satz nennt nur den einen Fall — *„eine Falte, in der der Loader kein Symbol handelbar macht, erzeugt keinen Trade"* |
| ⚠️ | **Die Wirkung ist gemessen und gross.** Vier Aktien-Bots bekämen 50 zusätzliche Selektionsfalten, `rsi2_crypto` eine. Eine Auslegung nach dieser Zahl wäre die nachträgliche Wahl, gegen die F17 steht |
| ⭐ | **Es ist sein Vorschlag**, und seine Begründung dafür nennt den Mechanismus ausdrücklich einseitig: *„`MIN_HISTORY_*` macht Symbole **später** handelbar, als 4a aus der Datenlage rechnet"* |

---

## Der gesendete Text, wörtlich

```
Die Messung zu deinem Vorschlag ist da, und sie widerlegt seine Prämisse. Wir
haben nichts geaendert - der Auftrag verlangte die Messung in BEIDE Richtungen,
bevor eine Zeile Code faellt.


WAS DU ANGENOMMEN HAST. "Das Auseinanderlaufen von 4a und 3b (a) hat einen
Mechanismus - MIN_HISTORY_* macht Symbole SPAETER handelbar, als 4a aus der
Datenlage rechnet."

WAS GEMESSEN IST. Das Auseinanderlaufen geht in beide Richtungen, und die
haeufigere ist die andere.

  Gemessen mit research/universum_trockenlauf/universum_trockenlauf.py::messe_bot
  am letzten Zeitpunkt jeder Falte (Lesart H), Gegenprobe gegen
  trockenlauf_ohne_schranke aus TB-56: neun von neun gleich.

  Bot                          Plan (4a)   Trockenlauf   Kandidatenfalten vor 4a
                                                          (davon mit H >= 1)
  ---------------------------------------------------------------------------
  t3_supertrend                     2018          2019         1  (0)   SPAETER
  elliott_wave                 2018-2019     2018-2019         1  (0)   gleich
  turtle_soup_crypto                2018          2018         1  (0)   gleich
  volatility_breakout_crypto        2018          2018         1  (0)   gleich
  rsi2_crypto                       2019          2018         2  (1)   FRUEHER
  elliott_wave_stocks               2017          1967        55 (50)   FRUEHER
  turtle_soup_stocks                2017          1967        55 (50)   FRUEHER
  rsi2_mean_reversion               2018          1967        56 (51)   FRUEHER
  volatility_breakout               2018          1967        56 (51)   FRUEHER

  Bei den vier Aktien-Bots reichen die Kursdateien bis 1962 zurueck; ab 1967
  macht der Loader durchgehend 16 und mehr Symbole handelbar.

WAS DARAUS FOLGT. 21.3 (b) lautet: "Ergeben 4a und 3b (a) fuer einen Bot
verschiedene erste Falten, bindet 3b (a)." Woertlich gelesen und mit dieser
Messung bekaemen vier Aktien-Bots Selektionsfalten ab 1967 - fuenfzig Jahre
Historie, in der es weder das registrierte Universum noch die Bots gab.

Die Begruendung im selben Registersatz sagt das Gegenteil: "Eine Falte, in der
der Loader kein Symbol handelbar macht, erzeugt keinen Trade und damit keinen
Falten-Sharpe." Das rechtfertigt, den Beginn nach HINTEN zu schieben. Es sagt
nichts darueber, ihn nach vorn zu ziehen.

Und 4a traegt eine Bedingung, die der Trockenlauf gar nicht prueft: "vom ersten
Jahr, in dem am 1. Januar Daten fuer UNIVERSUM und Indikator-Vorlauf
vorliegen". Der Trockenlauf misst den Loader gegen den vorhandenen
Kursbestand, nicht gegen die Frage, ob das registrierte Universum in jenem Jahr
existierte.

UNSERE LESART, die wir dir vorlegen statt sie zu vollziehen:

  21.3 (b) bindet nur dort, wo 3b (a) SPAETER liegt als 4a. Formal:
  erste Falte = max(4a, 3b (a)). 4a setzt den frueheste moeglichen Beginn
  (Universum und Vorlauf), 3b (a) kann ihn verschieben, nie vorziehen.

  Unter dieser Lesart aendert sich genau ein Bot: t3_supertrend, 2018 -> 2019,
  wie du es entschieden hast. Alle anderen acht bleiben, wo sie sind.

UND DAMIT AUCH DEIN VORSCHLAG (2) IN ANDERER FORM. "faltenplan.py leitet die
erste Falte aus dem Trockenlauf ab statt 4a nachzurechnen" kann so nicht
stehen: der Trockenlauf allein gibt 1967. Was bleibt, ist die Klasse zu
schliessen, nur anders herum - der Plan rechnet 4a wie bisher UND wendet den
Trockenlauf als Verschiebung nach hinten an, in einer Funktion, die beides
zusammenfuehrt. Dann kann er die Regel weiterhin nicht verfehlen, und er kann
auch nicht in die andere Richtung verfehlen.

DREI FRAGEN:

  (1) Trifft unsere Lesart max(4a, 3b (a))? Wenn ja: ist das eine Berichtigung
      von 21.3 (b) - der Satz bekommt die Richtung, die seine Begruendung
      ohnehin meint - oder eine Praezisierung ohne Ersatztext?

  (2) Falls nein und 3b (a) bindet in beide Richtungen: rsi2_crypto begaenne
      2018 statt 2019 (2 handelbare Symbole, H = 2), und die vier Aktien-Bots
      1967. Wir halten das nicht fuer gemeint, aber wir raten nicht.

  (3) Gehoert in 4a ein Satz, der sagt, woran "Universum liegt vor" gemessen
      wird? Heute steht die Bedingung im Registertext, und kein Code prueft
      sie - sie lebt darin, dass faltenplan.py die Datenlage nach 4a
      nachrechnet. Genau die Parallelrechnung wolltest du abschaffen.
```

---

## In einfacher Sprache

**Was passiert ist:** Der Auftrag sollte einen zweiten Rechenweg abschaffen und
den Plan direkt ablesen lassen, was die Bots wirklich handeln können. Die erste
Messung war eine Kontrolle in beide Richtungen — und sie hat ergeben, dass vier
Bots dann 1967 anfangen würden. Ihre Kursdateien reichen so weit zurück; das
Regelwerk meint aber etwas anderes.

**Warum nicht einfach das Offensichtliche tun:** Weil im Regelwerk ein Satz
steht, der wörtlich genommen 1967 sagt, und eine Begründung daneben, die das
Gegenteil meint. Welcher gilt, ist eine Auslegung — und die Wirkung kennen wir
schon. Genau dann darf man nicht selbst entscheiden.

**Was nicht passiert ist:** Es wurde keine Zeile geändert. Die Messung lag vor,
bevor irgendetwas angefasst wurde. Genau dafür stand sie an erster Stelle.
