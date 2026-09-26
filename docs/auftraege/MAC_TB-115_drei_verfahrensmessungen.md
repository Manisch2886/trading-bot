# TB-115 — Drei Verfahrensmessungen vor dem Tag, nur lesend: geschlossene Kerze je Bot, Adjustierung der Aktienreihen und Preisniveaus, Deckung der Kette Erzeuger → Auswertung

**Sitzungstitel:** `TB-115` · **Angelegt:** 26.09.2026, 18:35, vom steuernden Chat
**Vorgänger:** TB-114 (`90307cb`, Abbruch in Block C, gemeldet) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Grundlage:** Register 45.7, die Liste der Verfahrensmessungen nach 27.2, zeichengleich aus R7: *„Adjustierungsstand und Herkunft der 150 Aktienreihen im Snapshot; Nutzung von Preisniveaus je Bot; ob alle neun Bots die geschlossene Kerze lesen; ob TB-85 die Kette Erzeuger → Auswertung deckt.“* Dazu Fable 26a Abschnitt 2 (b): Die Kerze *„sollte“* vor dem Tag gemessen werden, *„weil sie eine Tag-Vorbedingung berührt“*.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**26.09.2026, ca. 16:20, Auswahlkarte im steuernden Chat:** *„Fable sagt, die Prüfung, ob alle neun Bots die geschlossene Kerze lesen, sollte vor dem Tag passieren. Das gilt auch für die Aktien-Adjustierung und die TB-85-Kette. Alle drei sind nur lesende Messungen. Wann?“* ⇒ **„Direkt danach TB-115 (Empfohlen)“**. **Dazu ca. 18:40, Auswahlkarte:** *„Darf ich TB-115 starten? Drei Prüfungen, die nur lesen und nichts ändern: (1) Entscheidet jeder Bot auf einer fertigen Kerze? (2) Sind die Aktienkurse um Splits und Dividenden bereinigt, und nutzt ein Bot feste Preisschwellen? (3) Deckt das Prüfwerkzeug die Kette vom Rechnen bis zur Auswertung? Dazu werden zwei meiner Dateien committet, die noch nicht im Repo stehen (AF-F0, Fable-Anfrage 26a).“* ⇒ **„Ja, starten (Empfohlen)“**

| freigegeben | Pfad / Handlung |
|---|---|
| ✔ | **nur lesen**: Code, Register, Snapshot-Manifest, Snapshot-Kursdateien (Spaltenköpfe und Stichproben, siehe M2) |
| ✔ | Wegwerf-Läufe **nur** in einem Wegwerfbaum oder frischen Klon, nie im Hauptordner |
| ✔ | Schritt 0: zwei vom steuernden Chat abgelegte, bisher unversionierte Dateien mitcommitten (TB-114 hat sie gemeldet) |
| ✔ | `docs/projektfuehrung/JOURNAL.md` (Block **DN**), `docs/belege/TB-115/`, `docs/ERGEBNIS_TB-115_drei_verfahrensmessungen.md` |

⛔ **Nicht freigegeben:**
- jede Änderung an Code, Register, Abbild, Tests;
- ein Lauf, der ein Ergebnis des Selektionsraums rechnet oder liest (Sichtschutz 27.1). Keine Sharpe-Werte, keine Trade-Zahlen, keine Zellenwerte im Ergebnis. Zählungen von **Dateien, Spalten, Codezeilen** sind erlaubt, Zeilenzahlen von Trade-Listen nicht (TB-114 0b hat das richtig gehandhabt);
- Datenbanken, `crontab`.

---

## 0. Schritt 0

**0a — Arbeitsbaum committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-115_drei_verfahrensmessungen.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger TB-115 |
| `docs/projektfuehrung/AF-F0_BESTANDSAUFNAHME_2026-09-26.md` | md5 `8dc52a758a09ad983f30a344c7a81213` |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-26a_tagesanfrage_tb109_bis_113.md` | md5 `06a84efdaf4f76a0fcc1c70aaa7eaab5` |

Weitere uncommittete Dateien: melden, nicht mitcommitten. Commit „TB-115 Schritt 0: Auftrag, Zeiger, AF-F0, Fable-Anfrage 26a“, Push.

**0b — Ausgangswerte** (`0b_ausgang.txt`):
- HEAD `90307cb…`;
- `register()` `5acb4c19…`;
- Sonde gegen `sperrliste_abbild_2026-09-26_tb114.json` `5e5ad109…`: 34/0/0.

Am Ende dieselben Werte noch einmal messen. Sie müssen gleich sein, sonst hat die Sitzung etwas verändert ⇒ melden.

## M1 — Liest jeder der neun Bots die geschlossene Kerze?

Gegenstand ist die Regel von `shared/entscheidungskerze.py` (TB-35 N1, „Entscheidungskerze ist die letzte Kerze, deren `close_time` VOR der Startzeit des Laufs liegt“). Je Bot, **auf beiden Pfaden**:

| Pfad | Frage |
|---|---|
| **Papier** (`forward_test.py`) | Geht die Entscheidung über `entscheidungskerze`? Gibt es daneben einen zweiten Zugriff auf die letzte Zeile, etwa `iloc[-1]`, `tail(1)` oder `df[-1:]`, der in eine Entscheidung eingeht (Signal, Stop, Grösse, Ausstieg)? |
| **Selektion** (`equity_simulation.py`, `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py`, soweit im Laufbereich) | Rechnet der Backtest nur auf abgeschlossenen Kerzen? Konkret: Kann die letzte Kerze des Snapshots eine Teilkerze sein (Grenze des Snapshots gegen `close_time`, TB-47), und wird sie gelesen? |

**Vorgehen:**
- `grep` mit Suchmustern, die im Beleg stehen, dann jede Fundstelle **gelesen** und eingeordnet: Entscheidung, Anzeige oder Protokoll.
- Wo die Zuordnung nicht aus dem Code folgt: ein Wegwerflauf mit einer künstlichen Teilkerze am Ende (Muster: Mutationsprobe aus TB-35, falls vorhanden; sonst eigene, im Beleg beschrieben).

**Ergebnis:** eine Tabelle 9 Bots × 2 Pfade mit ja / nein / nicht eindeutig und der Fundstelle.

## M2 — Adjustierung und Herkunft der Aktienreihen; Preisniveaus je Bot

**(a) Herkunft:** Aus `snapshots/63e4b6c8…/MANIFEST.json` und `config/` feststellen:
- wie viele `_1d.csv`-Reihen Aktien sind (Fable nennt 150; gezählt werden hier **Dateien**, gemessen 174 `_1d.csv` insgesamt, davon ein Teil Krypto);
- aus welcher Quelle sie stammen (yfinance?);
- mit welchem Aufruf und welchen Parametern (`auto_adjust`, `actions`, `back_adjust`) sie abgerufen wurden. Den Abrufcode am Stand des Snapshots lesen, nicht am heutigen.

**(b) Adjustierungsstand:**
- Welche Spalten tragen die Dateien? Gibt es `Adj Close` neben `Close`?
- Stichprobe **ohne Ergebnisbezug**: je 3 Aktien mit bekanntem Split (z. B. AAPL 2020, NVDA 2024, TSLA 2022, sofern im Universum) die Schlusskurse am Tag vor und nach dem Split. Ein Sprung um den Split-Faktor heisst unadjustiert.
- Dividenden-Adjustierung, soweit aus den Spalten erkennbar.

**(c) Preisniveaus je Bot:** Nutzt ein Aktien-Bot (`elliott_wave_stocks`, `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`) absolute Preisniveaus? Gemeint sind feste Schwellen in Währung, Mindestpreise, runde Zahlen, Stopps als absoluter Abstand oder Positionsgrösse aus dem Preis ohne Normierung. Gibt es so etwas, verschiebt eine Rückwärts-Adjustierung die Entscheidung. Je Fundstelle: Datei, Zeile, Art.

**Ergebnis:** ein Satz je Punkt, dazu die Folge, **nur benannt**: Muss der Adjustierungsstand als Tatsachennotiz neben 5e (Snapshot) stehen? Bewertet wird nicht, das ist Fables Sache.

## M3 — Deckt die Sperrlistensonde (TB-85) die Kette Erzeuger → Auswertung?

Fables Frage (25f, R7): *„ob TB-85 die Kette Erzeuger → Auswertung deckt“*. Zu messen:

- **Welche Glieder hat die Kette am Tag?**
  - Snapshot;
  - Erzeuger (noch nicht gebaut, 41.1 A12);
  - `zellen.csv`;
  - `auswertung.py`;
  - Bericht.
  
  Dazu je Glied: welche Datei, und ist sie heute auf der Sperrliste (Abschnitt 10), in `EINGEFROREN`, in `ARBEITSBAUM_PFADE` oder in keinem davon?
- **Was prüft die Sonde tatsächlich?**
  - Gruppen, Punkte, Pfad-Bestandteile, gelesen aus `shared/sperrlistensonde.py` und dem Abbild `5e5ad109…`;
  - der Befund aus TB-114 C gehört dazu: Die Gruppe `eingefroren` wird aus dem Abbild heraus geprüft, Zuwachs sieht die Sonde nicht.
- **Lücken:** je Glied, das nicht gedeckt ist, ein Satz, und ob die Lücke **vor dem Tag** geschlossen werden muss (weil der Tag-Commit sie sonst mit einfriert) oder mit dem Erzeuger (R5).

**Ergebnis:** eine Tabelle Glied × Bindung (Sperrliste / Abbild / Startprüfung / keine).

## Block E — Journal, Ergebnis

- Journalblock `## DN — TB-115: …`.
- `docs/ERGEBNIS_TB-115_drei_verfahrensmessungen.md` mit „Für Fable“ (je Messung die offenen Fragen) und „In einfacher Sprache“.
- 0b am Ende wiederholt, gleich.

## Commits

1. Schritt 0;
2. Belege und Ergebnis, Journal.

Nach jedem Commit Push.

## ⚠️ Abbruchkriterien — melden, nicht reparieren

- Eine Messung verlangte, eine Ergebnisgrösse des Selektionsraums zu lesen oder zu rechnen.
- Ein Wert aus 0b ist am Ende anders.
- Eine Messung ginge nur mit einer Änderung im Hauptordner.

**Befunde sind kein Abbruch.** Ein Bot, der die laufende Kerze liest, oder unadjustierte Reihen: melden und weitermessen.

## In einfacher Sprache

Drei Prüfungen, die nur lesen. Erstens: Entscheidet jeder der neun Bots auf einer fertigen Kerze und nicht auf einer, die noch läuft? Zweitens: Sind die Aktienkurse im eingefrorenen Datenstand um Aktiensplits und Dividenden bereinigt, und nutzt ein Bot feste Preisschwellen, die das stören würde? Drittens: Deckt das Prüfwerkzeug die ganze Kette vom Rechnen bis zur Auswertung, oder gibt es Glieder, die niemand bewacht? Geändert wird nichts; die Befunde gehen an Fable.
