# Anfrage an Fable 5.1, bestehender Chat — 21.09.2026

**Zwei Fragen in einer Nachricht. Es sind die letzten beiden offenen
Verfahrensfragen vor dem signierten Tag.**

**Herkunft:** Teil 1 folgt aus seiner Antwort vom 20.09. (Konjunktion,
`FABLE_ANTWORT_2026-09-20e_konjunktion.md`), Teil 2 aus TB-73 und
Registerabschnitt 24.6. Beide lagen seit dem 20.09. bereit und gehen jetzt
zusammen, weil sie dieselbe Fläche betreffen: **wie der Lauf aussehen wird.**

---

## Warum zusammen und nicht getrennt

| | |
|---|---|
| ⭐ | **Beide entscheiden, was der Lauf tut**, nicht wie ein Text lautet. Wer eine davon beantwortet, hat die andere schon halb im Blick |
| ⭐ | **Er hat heute mehrfach gezeigt, dass er Mehrfachfragen trägt** — die Antwort vom 20.09. beantwortete drei Fragen plus zwei Nebenfragen, jede einzeln |
| ⚠️ | **Getrennt kostet es eine Runde**, und der Tag hängt an beiden |

---

## Der gesendete Text, wörtlich

```
Zwei Fragen. Es sind die letzten beiden offenen Verfahrensfragen vor dem Tag,
und sie gehen zusammen, weil beide entscheiden, wie der Lauf aussieht - nicht
wie ein Text lautet.


=============================================================================
TEIL 1 - DER DATENHORIZONT: JE BOT ODER JE SYMBOL?
=============================================================================

Deine beiden Unsicherheiten aus der Konjunktions-Antwort sind gemessen, und
dabei ist ein dritter Befund aufgefallen, den du nicht gefragt hast.

(a) DIE KONSTANTE. Bei allen vier Aktien-Bots RECENT_YEARS_ONLY = 10, in
    JAHREN (pd.DateOffset(years=...)). Krypto hat keine.

      strategies/elliott_wave_stocks/multi_symbol_optimise.py:54
      strategies/rsi2_mean_reversion/multi_symbol_optimise.py:52
      strategies/turtle_soup_stocks/multi_symbol_optimise.py:46
      strategies/volatility_breakout/multi_symbol_optimise.py:49

(b) DER BEZUG. Datenuhr, nicht Wanduhr - dein zweiter Fall:

      entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)

    Relativ zum letzten Kurs im Bestand, nicht zum Laufdatum. Der Effekt ist
    derselbe, den du beschreibst: waechst der Kursbestand, rutscht das Fenster.

(c) DER DRITTE BEFUND, ungefragt. Die Bots rechnen entry_cutoff JE SYMBOL,
    innerhalb der Ladeschleife, und legen ihn je Symbol ab:

      for symbol in SYMBOLS:
          ...
          entry_cutoff = df["open_time"].max() - pd.DateOffset(years=10)
          data[symbol] = (df_ind, entry_cutoff)

    research/faltenplan_neun/faltenplan_neun.py::fensteranker nimmt dagegen den
    SPAETESTEN letzten Kurstag des Marktes, ausdruecklich "damit alle Symbole
    desselben Bots auf demselben Fenster liegen" (Docstring Z. 271-278).

    Das ist nicht dasselbe. Ein Symbol, dessen Datei frueher endet - delistet,
    Datenluecke, stehengebliebene Datei -, bekommt beim Bot ein frueheres
    Fenster und liefert Trades aus einem Zeitraum, den der Plan fuer
    ausgeschlossen haelt.

    ZWEI FRAGEN DAZU:

      (1) Ist "der Datenhorizont des Bots" eine Zahl je Bot oder je Symbol?
          Deine Praezisierung nennt ihn je Bot ("das Ergebnis steht je Bot als
          absolutes Datum"). Der Code rechnet ihn je Symbol. Eine der beiden
          Stellen muss nachgeben, und wir raten nicht, welche.

      (2) Gehoert die 4a-Praezisierung mit asof noch in dieselbe Berichtigung
          wie die Konjunktion, oder ist das eine eigene Aufgabe? Wir wuerden
          trennen: die Konjunktion ist erledigt und klein (ein Bot, ein
          Ersatztext, Register 25 steht). Die Horizont-Praezisierung braucht
          asof aus 5a, ein absolutes Datum je Bot ODER je Symbol - offen nach
          (1) - und beruehrt den Survivorship-Vorbehalt 3c. Vor dem Tag halten
          wir sie fuer noetig, aber nicht im selben Zug.


=============================================================================
TEIL 2 - DER GRENZFALL: WAS GILT, WENN KEIN SATZ BESTEHT?
=============================================================================

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

  (3) Der Grenzfall. Es kann sein, dass fuer einen Bot am Ende KEIN
      Parametersatz die Bedingung in allen Selektionsfalten besteht. Der
      Auswerter kennt den Fall - test_vorregistrierung Teil D prueft
      b_kein_satz_besteht_die_drawdown_bedingung - aber das Register sagt
      unseres Wissens nirgends, was dann gilt. Faellt der Bot aus der
      Selektion? Laeuft er mit seinen heutigen Parametern weiter? Wird
      berichtet und nichts getan?

      Das ist keine Zahlenfrage, und sie muss VOR dem Lauf beantwortet sein -
      sonst wird sie beantwortet, waehrend man das Ergebnis schon sieht.

  (4) Duerfen wir vorher messen, wie viele Saetze es kostet? Und hier ist
      unsere Lesart eine andere als bei 24.3, deshalb legen wir sie vor statt
      sie anzuwenden:

      Bei 24.3 war die Zahl folgenlos - der Grund stand in 1a, die Zahl
      konnte nichts entscheiden. HIER waere die Zahl eine Aussage ueber den
      AUSGANG des Laufs: wie viele Parametersaetze zulaessig bleiben, je Bot.
      Das ist naeher an der Selektion als alles, was wir bisher gemessen
      haben. Eine Regel, die man waehlt, nachdem man weiss, wie viele
      Kandidaten sie uebrig laesst, ist die nachtraegliche Wahl in Reinform.

      Unsere Neigung: (3) beantworten, ohne zu messen. Aber wir raten nicht.

  (5) Nachrichtlich, weil es zu (3) gehoert: Fuer die fuenf Krypto-Bots
      konnten die Falten 2018-2020 gar nicht gemessen werden - die
      TB-24-Trade-Listen beginnen erst 09/2021 bis 03/2022, Datenstand vor
      dem TB-34-Neuaufbau. Ausgerechnet Krypto 2020 fehlt, die Falte aus
      deiner eigenen Warnung. Steht in 24.6 als Luecke. Wir fragen nicht
      danach, wir sagen es nur dazu.


=============================================================================
ZUR FORM DEINER ANTWORT
=============================================================================

Ab sofort legst du deine Antworten bitte selbst im Projekt "Trading Bots" ab,
statt sie als Datei zurueckzugeben. Pfad und Namensform:

  projektfuehrung/FABLE_ANTWORT_<JJJJ-MM-TT><buchstabe>_<stichwort>.md

Fuer diese hier also zum Beispiel:
  projektfuehrung/FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md

Der Buchstabe laeuft innerhalb eines Tages durch (a, b, c ...). Der Betreiber
meldet dann nur noch "Fable ist fertig".
```

---

## In einfacher Sprache

**Teil 1:** Im Auswahlpfad steckt eine versteckte Uhr — „die letzten zehn
Jahre". Sie wird erst beim Rechnen zu einem Datum, und die Bots rechnen sie für
jedes Wertpapier einzeln, während der Plan sie für alle gemeinsam annimmt. Eine
der beiden Stellen muss nachgeben.

**Teil 2:** Der Verlust eines Bots wird künftig strenger gemessen, die Grenze
bleibt. Es werden also weniger Einstellungen zulässig sein — vielleicht bei
einem Bot gar keine. Was dann gilt, muss feststehen, **bevor** gerechnet wird.

**Und was wir bewusst nicht vorschlagen:** vorher nachzuzählen, wie viele
Einstellungen es kostet. Diese Zahl verrät den Ausgang.
