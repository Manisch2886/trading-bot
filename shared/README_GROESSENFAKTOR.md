# Der Quartals-Multiplikator auf die Positionsgrösse

**Modul:** `shared/groessenfaktor.py` · **Datei:** `config/groessenfaktor.json`
· **Beispiel:** `config/groessenfaktor.beispiel.json` · **Eingeführt:** TB-42

Dieses Dokument beschreibt **das Format der Multiplikator-Datei** und wo der
Wert wirkt. Die ausführliche Begründung jeder Festlegung steht im Kopf von
`shared/groessenfaktor.py`.

---

## Wozu

Das Leiter-Skript des Zellenbudgets (Registertext 6m, TB-41) rechnet einmal je
Quartal für jeden der neun Bots einen Multiplikator auf dessen heutige,
statische Positionsgrösse:

```
m_b = (Zellenanteil × Klassenschlüssel × Bot-Anteil in der Zelle) / (1/9)
```

`1/9` steht im Nenner, weil neun gleich grosse Bots heute je ein Neuntel
tragen. **`m_b = 1,0` heisst also „wie bisher“.**

> ⚠️ **Die schreibende Seite gibt es noch nicht.** Sie entsteht erst, wenn
> `research/vorregistrierung/auswertung.py` auf Verfahren B umgebaut ist. Bis
> dahin fehlt `config/groessenfaktor.json` schlicht — und genau deshalb ist
> der Rückfall auf 1,0 nicht der Ausnahme-, sondern der Normalfall.

## Das Format

`config/groessenfaktor.json` — versioniert, also im Repo, damit im
Git-Verlauf nachlesbar bleibt, welcher Multiplikator wann galt:

```json
{
  "quartal": "2026Q4",
  "erzeugt_utc": "2026-10-01T06:00:00Z",
  "herkunft": "auswertung.py (Verfahren B) - Zellenbudget, Registertext 6m",
  "bots": {
    "elliott_wave": 1.0,
    "elliott_wave_stocks": 1.0,
    "rsi2_crypto": 1.0,
    "rsi2_mean_reversion": 1.0,
    "t3_supertrend": 1.0,
    "turtle_soup_crypto": 1.0,
    "turtle_soup_stocks": 1.0,
    "volatility_breakout": 1.0,
    "volatility_breakout_crypto": 1.0
  }
}
```

Gelesen wird ausschliesslich `bots.<botname>`; der Botname ist der Ordnername
unter `strategies/`. Alles andere ist Beleg für Menschen und wird nur in die
Protokollzeile übernommen (`quartal`).

## Der zulässige Bereich: 0,25 bis 4,0

Ein Multiplikator von 0 oder 50 ist **ein Fehler, kein Befehl**. Ausserhalb
des Bereichs gilt 1,0, und es gibt eine Meldung.

| | |
|---|---|
| **0,25** unten | Darunter fressen Gebühren und Slippage (0,1 % + 0,05 % je Seite, fest) das Ergebnis auf — der Forward-Test misst dann nicht mehr die Strategie. Und **0 bleibt bewusst draussen**: „dieser Bot handelt nicht mehr“ ist eine Entscheidung des Betreibers, keine Zahl, die eine Quartalsrechnung nebenbei setzt. |
| **4,0** oben | Die Bots stehen bei 2 % bis 10 % je Position und 5 bis 20 gleichzeitigen Positionen; mal vier ist ein Bot voll investiert. Darüber wäre es keine Umverteilung mehr, sondern eine andere Strategie — und die gehört durch Backtest, Walk-Forward und Equity-Simulation (Protokoll Abschnitt 7). |
| **symmetrisch** | 4 = 1/0,25. Die Wache sitzt nach oben so eng wie nach unten. |

Die Grenzen stehen in `shared/groessenfaktor.py`, nicht in `live_params.py`:
sie sind kein Handelsparameter, sondern die Wache um einen.

## Was bei Fehlern geschieht — melden, nicht stoppen

| Lage | Faktor | Meldung |
|---|---|---|
| Datei fehlt | 1,0 | nein (Normalfall) — die Protokollzeile steht trotzdem |
| Datei unlesbar | 1,0 | **ja** |
| Abschnitt `bots` fehlt oder unbrauchbar | 1,0 | **ja** |
| eigener Bot nicht aufgeführt | 1,0 | **ja** |
| Wert ist keine Zahl (auch `true`) | 1,0 | **ja** |
| Wert ausserhalb 0,25 – 4,0, `NaN`, `Infinity` | 1,0 | **ja** |

**Ein Bot bleibt nie stehen, weil eine Quartalsrechnung fehlt oder kaputt
ist.** Und still wird der Rückfall nie: jeder Lauf schreibt genau eine Zeile
mit dem geltenden Faktor und seiner Herkunft — auch im Normalfall.

## Wo der Multiplikator angreift

**Nur an der Positionsgrösse, an genau einer Stelle je Bot: dem `INSERT`, mit
dem eine neue Papier-Position eröffnet wird.** Er landet dort in der Spalte
`groessenfaktor` der Trade-Tabelle.

> **Befund (TB-42):** Die neun `forward_test.py` führten bis dahin **gar keine
> Positionsgrösse**. Ihre Trade-Tabellen halten Zeiten, Kurse, Stop und
> `pnl_pct` — kein Stück, keinen Betrag, keinen Anteil. Die Grösse steht
> ausserhalb: `ALLOCATION_PCT` in `strategies/*/equity_simulation.py` und
> `BINANCE_TESTNET_BETRAG_USDT` in `broker/zugang.py`. Der Multiplikator hatte
> dort also nicht mehr als eine Angriffsstelle — sondern **keine**. Die Spalte
> ist die Antwort darauf: der Lauf schreibt die Grösse hin, mit der er
> eröffnet.

Er berührt **kein Signal, keine Schwelle, keine Positionszahl**. Nachgewiesen
am Ablauf, nicht am Quelltext: derselbe Lauf mit `m_b = 1,0` und `m_b = 0,5`
erzeugt dieselben Ein- und Ausstiegszeitpunkte
(`shared/test_groessenfaktor.py`, Abschnitt 3).

`pnl_pct` bleibt unberührt — ein Prozentsatz ist von der Grösse unabhängig.
Wer die Grösse einrechnen will, multipliziert beides; dafür steht die Spalte
da. Alte Trades behalten `NULL`, weil ihnen nachträglich eine 1,0 zu geben
eine Zahl behaupten hiesse, die damals niemand geführt hat.

Die Seite, die diese Spalte in Stücke oder Beträge übersetzt
(Kapitalsimulation, Broker-Brücke), gibt es noch nicht und gehört nicht zu
TB-42.

---

## In einfacher Sprache

**Was wir wissen wollten.** Ab dem nächsten Quartal soll jeder der neun
Handels-Bots nicht mehr automatisch gleich viel Geld einsetzen. Ein
Rechen-Skript soll vierteljährlich je Bot eine Zahl festlegen — einen
*Multiplikator* — die sagt: „Du handelst ab jetzt in halber Grösse“ oder „in
doppelter“. Die Frage war: Wie kommt diese Zahl bei den Bots an?

**Was herauskam.** Die Bots lesen die Zahl jetzt aus einer kleinen Datei
(`config/groessenfaktor.json`). Die Datei gibt es noch nicht — das Skript, das
sie schreibt, ist noch nicht gebaut. Solange sie fehlt, rechnen alle Bots mit
der Zahl **1,0**, und 1,0 heisst schlicht „so gross wie immer“. Es ändert sich
also heute nichts am Handeln.

**Warum das so ist.** Ein Bot darf nie stehenbleiben, nur weil eine Datei
fehlt oder kaputt ist. Deshalb gilt in jedem Zweifelsfall 1,0 und der Bot
läuft weiter. Damit dieses Ausweichen aber nicht heimlich passiert, schreibt
jeder Lauf eine Zeile hin, welche Zahl gerade gilt und woher sie kommt — auch
dann, wenn alles normal ist. Unsinnige Zahlen (0, 50, „ein Wort statt einer
Zahl“) werden nicht übernommen, sondern als Fehler gemeldet: erlaubt ist nur
ein Viertel bis das Vierfache der bisherigen Grösse.

**Was das für dich heisst.** Im Moment: nichts — die Bots handeln genau wie
gestern. In den Protokollen steht ab jetzt je Lauf eine zusätzliche Zeile, die
mit `Groessenfaktor` beginnt. Steht dort `1,0`, ist alles beim Alten. Steht
dort das Wort `Warnung` davor, stimmt etwas mit der Quartalsdatei nicht —
gehandelt wird dann trotzdem weiter, in normaler Grösse.
