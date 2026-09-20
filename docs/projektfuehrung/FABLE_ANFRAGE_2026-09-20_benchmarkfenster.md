# Anfrage an Fable 5.1, bestehender Chat — 20.09.2026

**Eine Frage. Sie legt Registertext 3b (c) aus, den er selbst geliefert hat, und
sie entscheidet die Drawdown-Bedingung aller fünf Krypto-Bots.**

**Herkunft:** TB-61 hat die Benchmark-Tabelle für alle neun Bots neu gerechnet
(daneben, die gesperrte Datei ist byteweise unverändert). TB-65 hat danach
geprüft, welche Schranke dabei gilt — und dabei eine Zweideutigkeit gefunden,
die das Register nicht auflöst.

**Die Antwort gehört in den Chat, der TB-61/TB-65 bearbeitet.**

---

## Der gesendete Text, wörtlich

```
Frage zum Register. Sie braucht keine Datei - sie ist hier vollstaendig.

VORGESCHICHTE. Registertext 3b (c), deine Fassung vom 16.09.2026:

  "Der Benchmark einer Falte - fuer die Drawdown-Nebenbedingung (Abschnitt 4)
  und fuer Rang 3 - wird auf den in dieser Falte geladenen Symbolen des Bots
  gerechnet, nicht auf dem vollen Universum. Bot und Benchmark leben in
  derselben Menge."

Der Auswerter setzte das bisher nicht um; das Register fuehrt es selbst als
offenen Punkt (16.11, Zeile 7, Schliesser TB-30b). benchmark.py rechnete
stattdessen mit einem point-in-time-Filter von vier Jahren. Gemessen: der
Bezeichner MINDESTTRAINING kommt im Register nullmal vor, und alle acht
Fundstellen fuer "vier Jahre" stehen in Bloecken, die als ERSETZT gekennzeichnet
sind. Fuer die vier Aktien-Bots ist der Unterschied null - beide Mengen sind auf
allen 100 Exposure-Stufen und in allen 40 Falten zeichengleich. Fuer die fuenf
Krypto-Bots ist er gross.

DIE FRAGE. 3b (c) sagt "in dieser Falte geladene Symbole". Das laesst zwei
Lesarten zu, und beide sind mit dem Wortlaut vereinbar:

  VH - Ein Symbol, das der Loader in dieser Falte laedt, geht fuer die GANZE
       Falte in den Benchmark ein.
  VT - Es geht erst AB DEM TAG ein, an dem der Loader es laedt.

GEMESSEN, damit die Groessenordnung sichtbar ist (turtle_soup_crypto, Falte
2018, 100 Prozent Exposure):

  VH: -87,92 Prozent. BTC und ETH durchlaufen den Baerenmarkt 2018 vollstaendig.
  VT:  -3,60 Prozent. Derselbe Bot, dieselbe Falte - aber der Loader laedt die
       beiden Symbole erst am 30.12.2018, es bleibt ein Handelstag.

Ueber alle fuenf Krypto-Bots liegt die DD_Toleranz bei 100 Prozent Exposure je
nach Fassung beim 2,4- bis 5,0-fachen dessen, was der bisherige Lauf ergab.

WAS FUER JEDE SEITE SPRICHT, soweit wir es sehen:

  Fuer VH spricht der Wortlaut. "In dieser Falte geladen" ist eine Eigenschaft
  der Falte, nicht eines Tages. Und Lesart H aus 16.2, die du bestaetigt hast,
  zaehlt eine Falte bereits, wenn ein Symbol "an mindestens einem Handelstag"
  handelbar ist - dort genuegt ein Tag, um die ganze Falte zaehlen zu lassen.

  Fuer VT spricht dein Begruendungssatz. "Bot und Benchmark leben in derselben
  Menge" - der Bot kann ein Symbol nicht handeln, bevor sein Loader es laedt.
  Unter VH enthielte der Benchmark Kursbewegungen, an denen der Bot in dieser
  Falte nicht teilnehmen konnte.

WAS WIR NICHT TUN. Wir legen es nicht selbst fest. Die Wirkung ist bekannt -
VT senkt die Toleranz in den fruehen Krypto-Falten drastisch, VH hebt sie stark
an -, und eine Auslegung nach bekannter Wirkung waere genau die nachtraegliche
Wahl, gegen die F17 steht.

ZWEI NEBENFRAGEN, nur falls sie fuer dich zusammenhaengen:

  (1) Gilt dieselbe Lesart fuer Rang 3 (Beta-Bereinigung), oder ist das eine
      eigene Festlegung? 3b (c) nennt beide in einem Satz.
  (2) Muss die gewaehlte Fassung als eigener Registertext stehen, oder ist sie
      eine Tatsachennotiz zu 3b (c)?

Der Stand: Das Amendment zu Sperrliste Punkt 4 ist beschlossen und wartet auf
diese Antwort. Fuer die vier Aktien-Bots koennte es sofort vollzogen werden -
dort ist der Unterschied null.
```

---

## Warum die Frage an Fable geht und nicht entschieden wird

| | |
|---|---|
| ⭐ | **Es ist sein Text.** 3b (c) samt dem Satz *„Bot und Benchmark leben in derselben Menge"* stammt aus seiner Fassung vom 16.09.2026 |
| ⚠️ | **Die Wirkung ist gemessen und bekannt** — Faktor 24 zwischen den beiden Lesarten in einer einzelnen Falte. **Eine Auslegung nach bekannter Wirkung ist eine nachträgliche Wahl** (F17: die Grenze ist die Quelle des Grundes, nicht die Zeit) |
| ⚠️ | **Die Lesart der Chat-Sitzung musste am selben Tag zweimal korrigiert werden** — TB-65 hat gezeigt, dass Abschnitt 5.3 die Folgerung nicht trägt und dass „Verstoß" nicht das Wort des Registers ist. *Das ist der Grund, warum hier niemand mehr allein auslegt* |

## In einfacher Sprache

**Worum es geht:** Die Tabelle, die festlegt, wie tief ein Bot fallen darf, wird
gegen einen Vergleichswert gerechnet — was hätte ein einfaches Halten derselben
Kurse gebracht. Die Frage ist, ab wann ein Kurs in diesen Vergleich eingeht: ab
Jahresbeginn oder erst ab dem Tag, an dem der Bot ihn überhaupt sehen kann.

**Warum das viel ausmacht:** Bei einem Bot im Jahr 2018 sind das −88 % gegen
−3,6 %. Der Unterschied entscheidet, ob seine Toleranz sehr eng oder sehr weit
ist — und damit, welche Parametersätze später überhaupt zulässig sind.

**Warum wir es nicht selbst festlegen:** Wir kennen die Wirkung bereits. Eine
Regel zu wählen, nachdem man weiß, was sie bewirkt, ist genau der Fehler, gegen
den das ganze Register gebaut ist.
