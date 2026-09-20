# Fables Antwort — erste Falte: 4a, 3b (a) und die Richtung (20.09.2026, fünfte)

**Eingegangen am 20.09.2026, 19:54 Ortszeit.** Antwort auf
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20e_erste_falte.md`.

⭐ **Wörtlich abgelegt, nach der Regel aus Nachtrag (m).**

⚠️⚠️ **Er nimmt seinen eigenen Vorschlag zurück und legt einen dritten Befund
daneben: eine Uhr im Selektionspfad, die der AST-Test nicht gefunden hat.**

---

## Vorab: sein Vorschlag (2) war falsch

> „Der Plan bezieht die erste Falte aus dem Trockenlauf" hätte den Aktien-Bots
> 1967 gegeben. Ich hatte den Mechanismus als einseitig angenommen (der Loader
> verschiebt nach hinten) und nicht bedacht, dass der Trockenlauf gegen den
> *ganzen* Kursbestand misst — und der reicht bei yfinance bis 1962. **Die
> Messung in beide Richtungen war die richtige Reihenfolge; zurückgenommen.**

---

## (1) `max(4a, 3b (a))` trifft — aber als Konjunktion, nicht als Richtungsregel

> `max(4a, 3b (a))` ist das richtige Ergebnis. Der Grund dafür ist einfacher als
> „3b (a) darf nur nach hinten schieben": **Eine Selektionsfalte muss zwei
> Bedingungen erfüllen, und jede ist eine Untergrenze.**
>
> > **Registertext 4a / 21.3 (b), Neufassung als ein Satz.** Ein Kalenderjahr ist
> > Selektionsfalte eines Bots, wenn (i) es im registrierten Datenhorizont des
> > Bots liegt und am 1. Januar der Indikator-Vorlauf erfüllt ist, **und** (ii)
> > der Loader des Bots in ihm an mindestens einem Handelstag mindestens ein
> > Symbol handelbar macht (Trockenlauf, 3b (b)). Die erste Selektionsfalte ist
> > das erste Jahr, das beide Bedingungen erfüllt.
>
> Damit kann (ii) den Beginn nie vorziehen, weil (i) weiter gelten muss — und (i)
> kann ihn nie vorziehen, weil (ii) weiter gelten muss. 21.3 (b) ist der
> Sonderfall, in dem (ii) später liegt; seine Begründung beschreibt genau diesen
> Fall und keinen anderen. **Berichtigung mit Ersatztext**, alter Wortlaut bleibt
> als ersetzt stehen. Wirkung bekannt: ein Bot, `t3_supertrend`, 2018 → 2019.

## (2) Nein — `rsi2_crypto` bleibt 2019

> Unter der Konjunktion bleibt `rsi2_crypto` bei 2019: (ii) ist 2018 erfüllt
> (zwei Symbole irgendwann im Jahr), (i) nicht — 150 Tagesbalken Vorlauf am
> 1. Januar 2018 brauchen Daten ab August 2017, BTC beginnt am 17.08.2017, das
> sind 137. … **Es gibt keine Lesart, in der 3b (a) allein bindet; sie war nie
> gemeint, und sie ist nach der Neufassung auch nicht mehr formulierbar.**

## (3) ⚠️⚠️ „Universum liegt vor" raus — der Datenhorizont rein

> „Daten für **Universum** und Vorlauf liegen vor" ist als Messgrösse unbrauchbar:
> Das registrierte Universum ist eine heutige Liste, und ihre Ticker haben Daten
> ab 1962. … der Survivorship-Vorbehalt (3c) hält genau diesen Umstand fest.
>
> Was der Plan tatsächlich rechnet, wenn er 2017/2018 liefert, ist etwas anderes:
> **der Datenhorizont des Bots.** Der ist eine registrierte Konstante
> (`RECENT_YEARS_ONLY` = 10) — **und er ist relativ zu „heute" definiert. Das ist
> die Wanduhr im Selektionspfad, die der AST-Test nicht gefunden hat, weil sie
> keine `now()`-Zeile ist, sondern eine Zahl, die erst mit dem Laufdatum zu einem
> Datum wird.**
>
> > **4a, Präzisierung.** „Im Datenhorizont" heisst: ab dem Horizontbeginn des
> > Bots, berechnet als registriertes `asof` (5a) minus `RECENT_YEARS_ONLY` des
> > Bots; das Ergebnis steht je Bot als absolutes Datum in der Tatsachennotiz zu
> > 4d. Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den ersten
> > Kurs im Bestand.
>
> Für Krypto ändert das nichts; für Aktien macht es die 2017/2018 zu einer
> abgeleiteten Zahl **und es friert sie ein: Ohne `asof` rutscht die erste Falte
> jedes Jahr um eins, und ein Lauf 2027 auf demselben Snapshot hätte einen
> anderen Faltenplan.**

⭐ **Sein Schluss zum Plan:** *„(i) ist keine Nachrechnung des Loaders, sondern
Arithmetik auf registrierten Konstanten; (ii) kommt aus dem Trockenlauf und wird
nicht nachgerechnet. Der Plan führt beide in einer Funktion zusammen — eure Form
— und kann in keiner Richtung verfehlen, weil er nichts selbst misst."*

---

## Seine offene Unsicherheit — hier beantwortet

> **Unsicher:** ob der Horizont bei allen vier Aktien-Bots dieselbe Konstante ist
> und ob sie in Jahren oder Tagen zählt … und ob `RECENT_YEARS_ONLY` heute im
> Backtest relativ zum Laufdatum oder relativ zum letzten Kurs im Bestand rechnet
> — im zweiten Fall ist die Wanduhr eine **Datenuhr**, mit demselben Effekt.

⭐⭐ **Gemessen am 20.09.2026, 19:58 — beides:**

| | Befund | Fundstelle |
|---|---|---|
| **Konstante** | **Bei allen vier Aktien-Bots `RECENT_YEARS_ONLY = 10`**, in **Jahren** (`pd.DateOffset(years=…)`). Krypto: keine | `strategies/{elliott_wave_stocks,rsi2_mean_reversion,turtle_soup_stocks,volatility_breakout}/multi_symbol_optimise.py`, Z. 54 / 52 / 46 / 49 |
| **Bezug** | ⚠️ **Datenuhr, nicht Wanduhr** — `entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)`. Relativ zum **letzten Kurs im Bestand**, nicht zum Laufdatum. *Sein zweiter Fall, mit demselben Effekt* | ebenda, Z. 93 / 93 / 81 / 88 |
| ⚠️⚠️ **Dritter Befund, den er nicht gefragt hat** | **Die Bots rechnen `entry_cutoff` JE SYMBOL**, innerhalb der Ladeschleife (`data[symbol] = (df_ind, entry_cutoff)`). **`faltenplan_neun.fensteranker` nimmt den SPÄTESTEN letzten Kurstag des Marktes**, *„damit alle Symbole desselben Bots auf demselben Fenster liegen"* (Docstring Z. 271–278). **Das ist nicht dasselbe** — ein Symbol, dessen Datei früher endet, bekommt beim Bot ein früheres Fenster | `multi_symbol_optimise.py` Z. 84–91 gegen `research/faltenplan_neun/faltenplan_neun.py` Z. 270–290 |

---

## Was daraus folgt

| | |
|---|---|
| ⭐ | **Die Neufassung als Konjunktion ist entschieden** und geht als Berichtigung mit Ersatztext ins Register — Teil von TB-72 |
| ⭐ | **`t3_supertrend` 2018 → 2019 bleibt die einzige Wirkung** |
| ⚠️⚠️ | **Die 4a-Präzisierung ist eine eigene, grössere Sache** — sie braucht `asof` aus 5a, ein absolutes Datum je Bot, und sie berührt den dritten Befund |
| ⚠️ | **Der dritte Befund ist noch niemandem vorgelegt worden** — er entscheidet, ob „das Fenster" überhaupt eine Zahl je Bot ist oder eine je Symbol |
