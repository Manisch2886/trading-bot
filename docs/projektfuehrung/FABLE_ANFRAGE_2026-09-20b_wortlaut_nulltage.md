# Anfrage an Fable 5.1, bestehender Chat — 20.09.2026, zweite

**Zwei Teile. Der erste ist eine Berichtigung einer Angabe, die ich ihm am
selben Tag geliefert habe und auf der sein Schlusssatz beruht. Der zweite ist
die Frage, die er selbst offen gelassen hat.**

**Herkunft:** TB-66 hat Fables Festlegung **VT** umgesetzt (Register Abschnitt
23, `benchmark.py` tagesgenau, Lauf daneben als `benchmark_drawdowns_vt.json`).
Dabei ist der Platzhalter in 23.3 entstanden — und der Widerspruch zur
Aktien-Gegenprobe, der die Berichtigung auslöst.

**Die Antwort gehört in den Chat, der TB-61/TB-65/TB-66 bearbeitet.**

---

## Warum Teil 1 ungefragt kommt

| | |
|---|---|
| ⚠️⚠️ | **Der falsche Satz stammt aus meiner Anfrage, nicht aus seiner Antwort.** Ich habe eine Zeichengleichheit gemeldet, die für **VH** galt, und sie in einer Frage über **VT** verwendet. Die richtige Zahl stand in derselben Messung eine Spalte weiter (`docs/belege/TB-65/frage_c_tabellen.md:11` und `:13`) |
| ⚠️ | **Er hat darauf gebaut.** Sein Schlusssatz *„Für die vier Aktien-Bots ändert sich nichts — die Sperrlisten-Änderung kann dort sofort vollzogen werden"* ist die unmittelbare Folge der falschen Angabe |
| ⭐ | **Es ist noch nichts vollzogen.** `benchmark_drawdowns.json` ist byteweise unberührt (`a163c498…36d1ee`, vor und nach TB-66 gleich). Die Berichtigung kostet nichts ausser dieser Nachricht |

## Warum Teil 2 ihm vorgelegt und nicht entschieden wird

| | |
|---|---|
| ⭐ | **Es ist sein Wortlaut.** Fassung W ändert einen Satz, den er geschrieben hat |
| ⭐ | **Die Wirkung kann die Wahl hier nicht steuern** — sie ist auf jeder registrierten Zahl null. *Das ist der seltene Fall, in dem F17 nicht bindet, weil es keinen Ausgang gibt, nach dem man wählen könnte.* **Die Zuständigkeit bleibt trotzdem seine** |
| ⚠️ | **Sein Satz hat zwei Umsetzungen**, und eine davon lässt eine leere Falte voll aussehen. Das gehört vor die Entscheidung, nicht dahinter |

---

## Der gesendete Text, wörtlich

```
Berichtigung und eine Frage. Beides braucht keine Datei - es ist hier
vollstaendig.


TEIL 1: EINE BERICHTIGUNG ZU MEINER ANFRAGE VOM 20.09., AUS DER DEINE
FESTLEGUNG VT HERVORGING.

In dieser Anfrage stand: "Fuer die vier Aktien-Bots ist der Unterschied null -
beide Mengen sind auf allen 100 Exposure-Stufen und in allen 40 Falten
zeichengleich."

Der Satz war falsch, und zwar an genau der Stelle, an der er fuer dich zaehlte.
Zeichengleich war der Vergleich des alten Vierjahresfilters mit VH (Symbol geht
fuer die ganze Falte ein). Fuer VT - die Lesart, die du festgelegt hast - lag
die Zahl in derselben Messung bereits daneben, in einer Nachbarspalte, die ich
nicht gelesen habe.

GEMESSEN nach dem VT-Lauf (alle neun Bots, 20.09.2026):

  Bei allen vier Aktien-Bots aendern sich die Falten 2019, 2025 und 2026 - in
  92, 99 und 97 der je 100 Exposure-Stufen. Grund: ANET wird am 05.06.2019
  handelbar, PLTR am 29.09.2025, DASH am 08.12.2025, ABNB am 09.12.2025, APP
  am 14.04.2026 und HOOD am 28.07.2026. Der bisherige Lauf zaehlte sie fuer
  das ganze Jahr. Der
  Drawdown aendert sich genau dort, wo die Peak-Trough-Episode VOR dem Eintritt
  liegt; liegt sie danach, sind beide Pfade identisch.

  DD_Toleranz bei 25 / 50 / 100 Prozent Exposure:

    rsi2_mean_reversion   -3,35 / -6,61 / -12,89  ->  -3,32 / -6,55 / -12,77
    volatility_breakout   -3,35 / -6,61 / -12,89  ->  -3,32 / -6,55 / -12,77
    elliott_wave_stocks   unveraendert  -2,18 / -4,33 / -8,55
    turtle_soup_stocks    unveraendert  -2,18 / -4,33 / -8,55

  Also strenger als der bisherige Lauf und weiterhin nachgiebiger als die
  gesperrte Tabelle.

WAS DARAUS FOLGT. Dein Schlusssatz "Fuer die vier Aktien-Bots aendert sich
nichts - die Sperrlisten-Aenderung kann dort sofort vollzogen werden" beruhte
auf meiner falschen Angabe. Wir vollziehen deshalb nicht in zwei Schritten,
sondern einmal fuer alle neun Bots. Vollzogen ist nichts; die gesperrte Tabelle
ist byteweise unberuehrt. Falls die Berichtigung an deiner Festlegung etwas
aendert, sag es.


TEIL 2: DIE FRAGE, DIE DU SELBST OFFEN GELASSEN HAST.

Du hast geschrieben: "nur eines darf im Register stehen, und es muss das sein,
was der Code tut. Vor dem Eintrag nachsehen."

Nachgesehen. Dein Satz "Tage, an denen kein Symbol handelbar ist, tragen
Rendite 0" trifft den Code nicht: bh_tagesrenditen schliesst solche Tage mit
.dropna() aus, statt sie mit 0 zu fuehren. Im Registertext steht an dieser
Stelle derzeit ein sichtbarer Platzhalter, keine der beiden Fassungen.

  W - Wortlaut an den Code: "Tage, an denen kein Symbol handelbar ist, gehen
      nicht in den Benchmark ein." Keine Codeaenderung, kein neuer Lauf.

  C - Code an den Wortlaut: .dropna() durch .fillna(0). Aendert
      bh_tagesrenditen - das ist Sperrliste Punkt 6 - und der Lauf waere zu
      wiederholen.

GEMESSEN, ueber alle neun Bots und 78 Falten:

  Drawdown, 78 x 100 Stufen:    0 abweichende Stufen
  DD_Toleranz, 9 x 100 Stufen:  0
  handelstage:                  4 Falten (C woertlich) bzw. 5 Falten (C voll)

Die Null ist kein Zufall: ein Tag mit Rendite 0 laesst 1 + e*r bei 1, der
Kapitalpfad bewegt sich nicht, Peak und Trough bleiben, wo sie sind.

EIN BEFUND ZU C, DER DIE FRAGE AUFTEILT. Dein Satz hat zwei Umsetzungen, und
sie sind nicht dasselbe:

  C_lit  - .fillna(0) auf dem vorhandenen Rahmen. Der Rahmen kennt nur Tage,
           an denen mindestens ein Symbol einen Kurs hat. Wirkung: +1
           Handelstag in vier Falten - der erste Kurstag, der noch keine
           Rendite hat.

  C_voll - dein Wortlaut vollstaendig: Kalender der Falte, fehlende Tage 0.
           Wirkung: t3_supertrend 2018 haette 365 Handelstage statt 0, obwohl
           der Loader dort kein einziges Symbol laedt. Eine leere Falte saehe
           im Registerbericht voll aus - und "leer" ist das Merkmal, an dem
           3b (a) haengt.

Die fuenf Falten mit abweichender Handelstagszahl, einzeln:

  elliott_wave                 2018-2019   W 133   C_lit 134   C_voll 730
  t3_supertrend                2018        W   0   C_lit   0   C_voll 365
  t3_supertrend                2019        W 136   C_lit 137   C_voll 365
  turtle_soup_crypto           2018        W   1   C_lit   2   C_voll 365
  volatility_breakout_crypto   2018        W   1   C_lit   2   C_voll 365

  Der Drawdown bei 100 Prozent ist in allen drei Fassungen derselbe:
  -42,14 / 0,00 / -42,21 / -3,60 / -3,60.

ZUM STELLENWERT VON handelstage: heute eine reine Berichtszahl -
registerbericht.py druckt sie, kein Code liest sie als Kriterium. Die
Falten-Zaehlung nach 3b (a) laeuft ueber die Symbolmenge, nicht ueber diese
Zahl.

WARUM WIR ES DIR VORLEGEN, obwohl der Zahlenunterschied null ist: Es ist dein
Wortlaut, und W aendert ihn. Die Wirkung kann die Wahl hier nicht steuern - sie
ist auf jeder registrierten Zahl null -, aber die Zustaendigkeit fuer den Satz
liegt bei dir.
```

---

## In einfacher Sprache

**Teil 1:** Ich habe ihm gestern eine Zahl geliefert, die aus der falschen
Spalte einer Tabelle stammte. Auf dieser Zahl beruht sein Satz, für die vier
Aktien-Bots ändere sich nichts. Das stimmt nicht — bei zweien wird die Grenze
ein Zehntelprozent strenger. **Das sage ich ihm, bevor er es selbst merkt oder
gar nicht merkt.**

**Teil 2:** In seinem neuen Regelsatz steht ein Halbsatz, den das Programm
anders rechnet, als er ihn geschrieben hat. Es geht um Tage, an denen der Bot
gar nichts handeln kann. Für jede Verlustzahl macht der Unterschied **exakt
null** — gemessen über 7 800 Kombinationen. Nur eine gedruckte Tagesanzahl
ändert sich. Er soll sagen, ob der Text dem Programm folgt oder umgekehrt.
