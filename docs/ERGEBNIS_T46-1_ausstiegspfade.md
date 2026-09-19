# ERGEBNIS T46.1 — Die Ausstiegspfade der neun Bots (Leseprüfung, 19.09.2026)

**Weg: diese Sitzung, über die Geräteanbindung an das MacBook. Rein lesend —
keine Datei unter `strategies/` angefasst, kein Lauf gestartet.**

⚠️ **Jede Aussage sagt, ob sie gemessen oder erschlossen ist**
(`DOKUMENTATIONSSTANDARD.md`, Regel 1). Ausgangsstand `HEAD` = **`b600a65`**,
Arbeitsbaum sauber ausser dem noch nicht committeten TB-59-Auftrag.

---

## Die Frage

**Fable, 17.09.2026, als Sicherheitspunkt vor allem anderen in die Kette
gesetzt (Backlog Rang 0,6):**

> *„‚Hält null Positionen' — heisst das **keine neuen** Positionen, oder
> **schliesst** der Bot offene, weil er sie ohne Kerze nicht bewerten kann?"*
> ⚠️ *„Im zweiten Fall macht ein Parsing-Fehler einen Trade. Ein Bot, der bei
> fehlender Kerze verkauft, hat kein Holdout-Problem, sondern ein
> Sicherheitsproblem."*

---

## Die Antwort: keine neuen. Gemessen, 9 von 9

**Jeder der neun `forward_test.py` trägt in der Ausstiegsschleife dieselbe
Wache, zeichengleich:**

```python
for _, trade in open_trades.iterrows():
    symbol = trade["symbol"]
    if symbol not in indicator_data:      # elliott_wave*: price_data
        continue
```

| Bot | Zeile | Wache gegen |
|---|---:|---|
| `elliott_wave` | 113 | `price_data` |
| `elliott_wave_stocks` | 114 | `price_data` |
| `rsi2_crypto` | 118 | `indicator_data` |
| `rsi2_mean_reversion` | 119 | `indicator_data` |
| `t3_supertrend` | 97 | `indicator_data` |
| `turtle_soup_crypto` | 117 | `indicator_data` |
| `turtle_soup_stocks` | 109 | `indicator_data` |
| `volatility_breakout` | 110 | `indicator_data` |
| `volatility_breakout_crypto` | 124 | `indicator_data` |

**Zweite, unabhängige Messung:** Über alle neun Dateien **`0` Treffer** für einen
Schliess-Aufruf in einem Zweig, der einen leeren oder fehlenden Kursrahmen
behandelt.

**Und die Ladeseite passt dazu:** Acht der neun fangen den leeren Rahmen beim
Laden ab (`if df.empty: continue`) — das Symbol kommt gar nicht erst in die
Indikatordaten, und die Wache oben greift dann. ⚠️ **`t3_supertrend` hat diesen
Zweig nicht** und überlebt nur, weil der Aufruf im `try` der Ladeschleife steht
(bekannt als T45.3/T45.4, hier erneut bestätigt).

⇒ ⭐⭐ **Der Sicherheitspunkt ist geschlossen: Ein Parsing-Fehler oder eine
fehlende Kursdatei macht bei keinem der neun Bots einen Trade.**

---

## ⚠️⚠️ Der Befund, den niemand gesucht hat — dieselbe Wache, andere Richtung

**Die Wache schützt vor dem Verkaufen. Sie tut aber noch etwas:**

> ⚠️ **Wird der Trade übersprungen, wird an diesem Tag auch sein STOP nicht
> geprüft.** Stop-Loss, Zeitbremse und Ausstiegssignal liegen sämtlich **hinter**
> dem `continue`. Fehlt die Kursdatei eines Symbols, ist die Stop-Prüfung für
> die offene Position dieses Symbols an diesem Tag **ausser Kraft**.

**Und sie ist still.** Gemessen: Die Wache ist in allen neun ein **nacktes
`continue`** — keine Protokollzeile, keine Meldung, kein Zähler. Auf der
**Ladeseite** hat TB-45 genau diese Stille bei zwei Bots behoben
(`shared/ladeprotokoll.py`, `_prot.ohne_kursrahmen`); auf der **Ausstiegsseite**
ist sie bei **allen neun** unverändert vorhanden.

⭐ **Dieselbe Familie wie D1:** *„Ein Lauf, der ein Symbol auslässt, sagt es.
Immer."* — TB-45 hat die Regel auf der Eingangsseite durchgesetzt. **Die
Ausstiegsseite hat sie nie erreicht.**

⚠️ **Warum das schwerer wiegt als der ausgelassene Einstieg:** Ein nicht
eröffneter Trade ist ein entgangenes Geschäft. Ein nicht geprüfter Stop ist eine
**offene Position ohne Absicherung**, und zwar genau an einem Tag, an dem mit den
Daten etwas nicht stimmt. *Erschlossen, nicht gemessen: Datenausfälle und
Marktbewegungen sind nicht unabhängig voneinander.*

⚠️ **Nicht gemessen und ausdrücklich offen:** wie oft das real eingetreten ist.
Das stünde in den Bot-Logs; sie sind nicht Gegenstand dieser Leseprüfung.

---

## Was daraus folgt — Vorschlag, nicht Ausführung

| | |
|---|---|
| ⛔ | **Nicht** den `continue` entfernen. Ohne Kerze kann der Stop nicht bewertet werden; ihn zu erzwingen hiesse, auf einem alten Kurs zu handeln — **genau der Trade, den Fables Frage verhindern will** |
| ⭐ | **Melden, nicht handeln.** Die Wache bekommt dieselbe Behandlung wie die Ladeseite: eine Zeile über `shared/ladeprotokoll.py`, die Symbol, Trade-Kennung und Grund nennt. **Ändert kein Verhalten, nur Sichtbarkeit** — dieselbe Klasse wie TB-42 Teil 1, **kein Amendment** |
| ⚠️ | **Berührt alle neun `forward_test.py`** — Sperrliste, **freigabepflichtig**. Betreiberentscheidung |
| ⚠️ | **Registerseite:** Registertext 7, Ergänzung I kennt den **Kein-Entscheid-Tag**. Ob ein Tag, an dem ein Symbol keine Kerze hatte und sein Stop deshalb ungeprüft blieb, darunter fällt, **steht nirgends**. Gehört geklärt, bevor der Backtester-Vergleich solche Tage zählt |

---

## In einfacher Sprache

**Was wir wissen wollten:** Wenn einem Bot die Kursdaten für ein Symbol fehlen —
verkauft er dann die offene Position, weil er sie nicht mehr bewerten kann?

**Was herauskam:** Nein. Alle neun überspringen die Position und lassen sie
unangetastet. Die Sorge war berechtigt, der Fall liegt aber nicht vor.

**Warum das so ist:** In jedem der neun steht dieselbe Zeile, die einen Trade
überspringt, sobald seine Kursdaten fehlen.

**Was dabei auffiel, obwohl niemand danach gesucht hat:** Dieselbe Zeile
überspringt auch die **Stop-Prüfung**. Fehlt an einem Tag die Kursdatei eines
Symbols, wird die Verlustbegrenzung für die offene Position dieses Symbols an
diesem Tag nicht geprüft — und **nichts sagt etwas darüber**, weder im
Protokoll noch per Telegram.

**Was das für dich heisst:** Der gefährliche Fall ist ausgeschlossen. Der neue
Befund ist kein Notfall, aber er gehört behoben — und zwar **nicht**, indem der
Stop erzwungen wird (dann würde auf einem veralteten Kurs gehandelt), sondern
indem der Bot sagt, dass er ihn nicht prüfen konnte. Das ändert nichts am
Handeln und braucht trotzdem deine Freigabe, weil es die neun Bot-Dateien
berührt.

---

*Gemessen 19.09.2026 über die Geräteanbindung, rein lesend. Die Anbindung liest
das Repo, sie rechnet nicht darin (K2l) — es wurde kein Bot ausgeführt.*
