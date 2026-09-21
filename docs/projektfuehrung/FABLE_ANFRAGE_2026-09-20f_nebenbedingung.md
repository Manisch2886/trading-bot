# Anfrage an Fable 5.1, bestehender Chat — 20.09.2026, sechste

**Registertext 24.2 vertieft die Bot-Seite der Drawdown-Nebenbedingung. Die
Grenze, gegen die geprüft wird, kommt von der Benchmark-Seite und bleibt, wo sie
ist. Die Nebenbedingung bindet dadurch härter — und niemand hat gerechnet, wie
viel härter.**

**Herkunft:** TB-73 hat die Wirkung gemessen (Register 24.6): in 59 von 64
Falten ist der tägliche Drawdown tiefer, Median der Differenzen je Bot −1,39 bis
−3,09 Prozentpunkte. Die Frage entstand beim Lesen des Ergebnisses, nicht beim
Messen.

**Die Antwort gehört in den Chat, der TB-61 bis TB-73 bearbeitet.**

---

## ⚠️ Eine Berichtigung an mir selbst, bevor die Frage steht

**Meine erste Fassung fragte, ob die Benchmark-Seite mitziehen muss. Das ist
falsch herum.** Der Benchmark **war immer schon** tagesbewertet:
`bh_tagesrenditen` ist ein Kursindex, er kennt keine offenen Positionen und
damit keinen Unterschied zwischen realisiert und unrealisiert.

⭐ **Die Asymmetrie bestand also von Anfang an — 24.2 beseitigt sie.** Dass die
Bedingung danach härter bindet, ist nicht die Nebenwirkung einer Änderung,
sondern **das, was sie immer hätte tun sollen.** Genau das steht in seiner
Begründung: *„eine Nebenbedingung, die unrealisierte Verluste nicht sieht, ist
in genau den Falten nachgiebig, in denen sie binden soll."*

⭐ **Und die Kalibrierung ist davon unberührt:** Weder der Faktor 1,25 noch
`DD_Toleranz` wurde je an einer Bot-Zahl geeicht — `DD_Toleranz` ist der Median
der **Benchmark**-Drawdowns (Festlegung 5), 1,25 eine Betreiberfestlegung vom
14.09. **Es gibt keine geerbte Verzerrung.**

⇒ **Was übrig bleibt, ist keine Frage nach der Regel, sondern nach dem, was aus
ihr folgen darf.**

---

## Der gesendete Text, wörtlich

```
Eine Frage, die aus TB-73 folgt und die wir nicht selbst beantworten.


ZUERST EINE BERICHTIGUNG AN UNS SELBST. Wir wollten fragen, ob die
Benchmark-Seite der Nebenbedingung mitziehen muss, wenn 24.2 die Bot-Seite
vertieft. Das ist falsch herum: bh_tagesrenditen ist ein Kursindex, er kennt
keine offenen Positionen und war damit immer schon tagesbewertet. Die
Asymmetrie bestand von Anfang an, und 24.2 beseitigt sie. Auch die Kalibrierung
ist unberuehrt - DD_Toleranz ist der Median der BENCHMARK-Drawdowns
(Festlegung 5), der Faktor 1,25 eine Betreiberfestlegung vom 14.09.; keine der
beiden wurde je an einer Bot-Zahl geeicht.

WAS BLEIBT. Die Nebenbedingung bindet nach 24.2 haerter als bisher, ohne dass
sich eine Grenze bewegt hat:

  erlaubt(f) = min(1,25 x DD_Benchmark(f), DD_Toleranz)
  bestanden  = dd_satz >= erlaubt(f)

dd_satz wird tiefer, erlaubt(f) bleibt. Gemessen (24.6): in 59 von 64 Falten
mit Grundlage ist M tiefer als E, Median der Differenzen je Bot -1,39 bis
-3,09 Prozentpunkte, Faktor-Perzentile 1,04 / 1,30 / 1,88. In den schweren
Falten mehr: turtle_soup_stocks 2020 -29,91 -> -34,45,
volatility_breakout 2020 -9,41 -> -12,60, turtle_soup_crypto 2022
-27,86 -> -30,38.

DIE FRAGE, ZWEITEILIG:

  (1) Der Grenzfall. Es kann sein, dass fuer einen Bot am Ende KEIN
      Parametersatz die Bedingung in allen Selektionsfalten besteht. Der
      Auswerter kennt den Fall - test_vorregistrierung Teil D prueft
      b_kein_satz_besteht_die_drawdown_bedingung - aber das Register sagt
      unseres Wissens nirgends, was dann gilt. Faellt der Bot aus der
      Selektion? Laeuft er mit seinen heutigen Parametern weiter? Wird
      berichtet und nichts getan?

      Das ist keine Zahlenfrage, und sie muss VOR dem Lauf beantwortet sein -
      sonst wird sie beantwortet, waehrend man das Ergebnis schon sieht.

  (2) Duerfen wir vorher messen, wie viele Saetze es kostet? Und hier ist
      unsere Lesart eine andere als bei 24.3, deshalb legen wir sie vor statt
      sie anzuwenden:

      Bei 24.3 war die Zahl folgenlos - der Grund stand in 1a, die Zahl
      konnte nichts entscheiden. HIER waere die Zahl eine Aussage ueber den
      AUSGANG des Laufs: wie viele Parametersaetze zulaessig bleiben, je Bot.
      Das ist naeher an der Selektion als alles, was wir bisher gemessen
      haben. Eine Regel, die man waehlt, nachdem man weiss, wie viele
      Kandidaten sie uebrig laesst, ist die nachtraegliche Wahl in Reinform.

      Unsere Neigung: (1) beantworten, ohne zu messen. Aber wir raten nicht.

  (3) Nachrichtlich, weil es zu (1) gehoert: Fuer die fuenf Krypto-Bots
      konnten die Falten 2018-2020 gar nicht gemessen werden - die
      TB-24-Trade-Listen beginnen erst 09/2021 bis 03/2022, Datenstand vor
      dem TB-34-Neuaufbau. Ausgerechnet Krypto 2020 fehlt, die Falte aus
      deiner eigenen Warnung. Steht in 24.6 als Luecke. Wir fragen nicht
      danach, wir sagen es nur dazu.
```

---

## In einfacher Sprache

**Worum es geht:** Die Verlustgrenze eines Bots wird gegen einen Vergleichswert
gerechnet. Ab jetzt wird der Verlust des Bots strenger gemessen — der
Vergleichswert bleibt gleich. Das ist richtig so; er war nie zu locker, der Bot
war zu nachsichtig gemessen.

**Was das bedeutet:** Es werden weniger Parametersätze zulässig sein als
gedacht. Im äussersten Fall bei einem Bot gar keiner.

**Was wir fragen:** Was gilt dann? Das muss feststehen, **bevor** gerechnet
wird — sonst entscheidet man es, während man das Ergebnis schon vor sich sieht.

**Und was wir bewusst nicht tun:** vorher nachzählen, wie viele Sätze es kostet.
Diese Zahl wäre eine Aussage über den Ausgang, und danach zu entscheiden ist
genau der Fehler, gegen den das ganze Verfahren gebaut ist.
