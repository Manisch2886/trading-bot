# Ergebnis TB-34 — Kursdaten neu aufbauen

**Kurzfassung zum Kopieren. Stand 2026-09-15.**

---

## Die zwei Zahlen zuerst

**1. Was ist heute falsch — je Datei, gemessen:**

| | Wieviele | Ausmass |
|---|---|---|
| `*_1d.csv`, erste Kerze | **24 von 24** | **6–16 von 24 Stunden**, und nachweislich aus den 1h-Daten **abgeleitet** |
| `*_1d.csv`, letzte Kerze | **24 von 24** | **13 von 24 Stunden**, ebenfalls abgeleitet |
| `*_4h.csv`, letzte Kerze | **24 von 24** | 1h-Datei belegt **1 von 4** Stunden, und die 4h-Kerze passt nicht zu deren Aggregat |
| `*_1h.csv`, letzte Kerze | 24 von 24 | aus den Dateien allein **nicht belegbar** — folgt aus dem 4h-Befund |

**2. Wer rechnet auf dem veralteten Stand:**

> **37 Module lesen `data/` unmittelbar, 64 weitere über
> `load_all_symbol_data()` — zusammen 101.** Keines prüft den Stand.
> **Die neun `forward_test.py` sind nicht dabei: alle neun holen live.**
> Deshalb ist es nie aufgefallen — der Teil, der täglich läuft, fragt `data/`
> nie.

`data/` steht bei **2026-08-31** (Krypto) bzw. **2026-09-01** (Aktien). Heute
ist der 2026-09-15.

---

## Was geliefert ist

| Datei | Was |
|---|---|
| `shared/kursdaten_neuaufbau.py` | der Neuaufbau: messen, laden, sichern, vergleichen, ersetzen, zurückspielen |
| `shared/test_kursdaten_neuaufbau.py` | **67/67**, davon drei zweistufige Mutationsproben |
| `shared/zeitabdeckung.py` | die Teilkerzen-Wache, Rückgabewert 1 bei Befund, nur stdlib |
| `shared/test_zeitabdeckung.py` | **40/40**, davon zwei zweistufige Mutationsproben |
| `shared/README_KURSDATEN.md` | beide Werkzeuge, Sicherungskonzept, **Cron-Zeile als Vorschlag** |
| `research/kursdaten_neuaufbau/probelauf.py` | Neuaufbau gegen die **echten** 72 Dateien, **295/295** |
| `research/kursdaten_neuaufbau/datenwege.py` | wer liest `data/`, wer holt live, wer schreibt |
| `research/kursdaten_neuaufbau/BERICHT.md` | die Untersuchung, Symbol für Symbol |
| `docs/TESTAUFTRAG_TB-34_kursdaten.md` | 18 Schritte, 1–7 überall, 8–18 auf dem Mac |
| `docs/UEBERGABE_TB-34_kursdaten.md` | die Übergabe-Zusammenfassung |

**Es wurde keine Kursdatei verändert.** `git diff origin/main HEAD --name-only`
listet keine Datei unter `data/`.

---

## Die Entwurfsentscheidungen, kurz begründet

**Eigenes Modul statt Erweiterung von `binance_historie.py`.** Das TB-31-Modul
**verlängert** nach vorn und schreibt jede vorhandene Zeile zeichengleich
zurück; sein ganzer Wert liegt darin, nie zu überschreiben. Beides in eine
Datei zu legen hiesse, diese Zusicherung von einem Laufzeitschalter abhängig zu
machen — die Bauform, die das Projekt bei der Binance-Brücke verworfen hat
(`testnet=True` im Aufrufpfad). Geteilt wird trotzdem alles: `Drossel`,
`Abrufer`, `kerzen_laden`, `erste_kerze_ms`, `als_dataframe`,
`zeilen_aus_dataframe`, `schreibe_datei`, `Kursdatei`, die 418-Behandlung.
**Eine Netzstelle, eine Schreibweise.**

**Die Wache steht neben `kursdaten.py`, nicht darin.** Drei Gründe:
`entferne_unvollstaendige()` läuft in allen neun Bots bei jedem Laden und
arbeitet zeilenweise im Speicher — die Deckungsprüfung braucht **andere
Dateien** und einen Stichzeitpunkt; `kursdaten.py` **streicht**, eine Teilkerze
gehört aber gemeldet und nicht stillschweigend entfernt (die letzte Tageskerze
zu streichen verschöbe das Ende jedes Backtests); und der Live-Betrieb darf nie
an einer Datenprüfung hängenbleiben. Muster wie `ergebniskurven.py` und
`determinismus.py`: eigenständig, Rückgabewert 1 bei Befund.

**Die Sicherung wird nicht automatisch gelöscht.** Anders als bei der
Log-Rotation (5 Stände): ein Kursdatenstand ist nicht wiederherstellbar, wenn
der Endpunkt ihn nicht mehr so liefert. Ziel: `data_sicherung/<Zeitstempel>/`
neben `data/`, gitignoriert, rund 184 MB je Lauf, mit SHA-256 je Datei im
`MANIFEST.json`. Ein **belegter** Sicherungsordner wird abgelehnt statt
überschrieben.

**Keine angeschnittene Kerze — strukturell.** Übernommen wird nur, was der
Endpunkt als abgeschlossen meldet (`close_time <= Stand`). Der Fehler, der
diese Aufgabe ausgelöst hat, ist damit nicht vermieden, sondern unmöglich.

**Eine Abweichung ausserhalb der Ränder verhindert das Schreiben — ohne
Schalter.** An den Rändern (erste/letzte Zeile des Altbestands) sitzt die
erwartete Teilkerze. Dazwischen hätte sich Historie geändert; das gehört
angesehen, nicht übernommen.

---

## Drei Nebenbefunde, die im Auftrag nicht standen

1. ⚠️ **`strategies/rsi2_crypto/fetch_1d_data.py` und
   `strategies/volatility_breakout_crypto/fetch_1d_data.py` stehen weiterhin
   auf `LOOKBACK = "3650 day ago UTC"`.** Der Betreiber hat die beiden Skripte
   mit dem Fünf-Jahres-Fenster korrigiert; diese beiden nativen Tagesabrufe
   nicht. Heute schneidet das nichts weg (Binance gibt es erst seit Juli 2017),
   **ab Sommer 2027 schon** — und es ist derselbe Fehlertyp.
2. **Keines der acht Abrufskripte schliesst die laufende Kerze aus**, und alle
   überschreiben ihre Datei vollständig. Nach jedem künftigen Abruf steht die
   Teilkerze wieder da.
3. **Eine echte Datenlücke:** 13 Krypto-1h-Dateien fehlen drei Stunden ab dem
   **2021-09-29 07:00**, `PROMUSDT_1h.csv` eine ab dem 2023-03-24 13:00. Sie
   steht **nicht** in `docs/DATENLUECKEN.md` (das führt nur
   Forward-Test-Ausfälle). Ausserdem liegen **19 verwaiste `*_15m.csv`** in
   `data/` — Reste des verworfenen 15-Minuten-Versuchs, von keinem Programm
   gelesen.

---

## Was nach dem Lauf zu erwarten ist — und benannt gehört

| Was | Erwartung |
|---|---|
| `shared/zeitabdeckung.py --datenbeginn <bericht>` | **kein Befund** für die 72 Krypto-Dateien |
| `shared/ergebniskurven.py` | **5× ABWEICHEND** (Krypto), **4× AKTUELL** (Aktien). Ein ABWEICHEND bei einem Aktien-Bot hiesse, der Lauf hat etwas angefasst, was er nicht durfte |
| `research/krypto_historie/faltenplan.py` | **neu zu rechnen** — die TB-31-Zahlen beruhen auf angenommenen Listing-Daten |
| Datenstand-Hash der Vorregistrierung | **ändert sich** |

> ⚠️ **Der Datenstand-Hash der Vorregistrierung ändert sich — und das ist kein
> Amendment.** Er steht in `docs/VORREGISTRIERUNG_neuselektion.md` auf der
> Sperrliste. Er ändert sich **vor** dem Selektionslauf, und genau das ist der
> Grund, warum TB-34 **vor** TB-30b kommt. Wäre erst selektiert und dann
> geladen worden, hätte die Selektion auf einer Historie stattgefunden, die es
> danach nicht mehr gibt.

**Die Ergebniskurven bitte NICHT vorschnell neu erzeugen.** `ABWEICHEND` ist
nach dem Laden richtig; ob und wann neu gerechnet wird, entscheidet der
Betreiber und gehört in denselben Schritt wie die Neuselektion.

---

## Zur Cron-Frage: berichtet, nicht entschieden

**Eine Cron-Zeile steht als Vorschlag im README — für die Wache, nicht für den
Abruf:**

```cron
0 4 * * * cd ~/trading-bot && /usr/bin/python3 shared/zeitabdeckung.py >> logs/system/zeitabdeckung.log 2>&1
```

**Für einen täglichen Abruf** spricht, dass `data/` zwei Wochen alt ist und 101
Module darauf rechnen, ohne dass irgendetwas den Stand prüft.

**Dagegen spricht die Form, in der er heute stattfände:** es gibt in diesem
Projekt **kein Werkzeug, das anhängt**. `binance_historie.py` verlängert nach
vorn, `kursdaten_neuaufbau.py` baut vollständig neu, und die `fetch_*.py`
überschreiben — samt laufender Kerze. Ein täglicher Cronjob mit den heutigen
Skripten machte den Fehler, den TB-34 gerade behebt, zur täglichen Gewohnheit;
ausserdem wechselte der Datenstand-Hash der Vorregistrierung täglich mit, und
`ergebniskurven.py` meldete täglich VERALTET.

**Deshalb keine Abruf-Cron-Zeile.** Erst der Neuaufbau von Hand, dann die Wache
per Cron, dann — falls gewünscht — ein **anhängendes** Abrufwerkzeug als eigene
Aufgabe.

---

**Es wurde kein Raster gerechnet, kein Parameter übernommen und keine Kursdatei
verändert.**
