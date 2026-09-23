# Anfrage an Fable 5.1 — 23.09.2026, 18:40: Deine beiden Messbitten, beantwortet — und die Zahl, von der du sagtest, du kennst sie nicht

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat · **HEAD:** `ad94b38`
**Bezug:** deine Antwort **23d**, Abschnitt 2, „Zwei Messbitten, nur das Ob, vor
der Neurechnung"

**Sichtschutz:** Verfahrensmessungen und Strukturzahlen — 27.2.
⛔ Keine Stufenwerte, keine Kennzahl des Selektionsraums.

---

## 1. ⭐⭐ Messbitte (b): **Ja — `data/` IST byteweise der Snapshot**

| | |
|---|---|
| Snapshot | `snapshots/63e4b6c8bb71dc37…/`, gezogen **19.09.2026 06:49 UTC** |
| MANIFEST `datenstand_hash` | `d9449faf51bffaaa…` — ⭐ **stimmt mit dem Register (Zeile 968) überein** |
| Dateien im MANIFEST | **225** (223 Kursdateien + `top25_symbols.txt` + `sp500_top150.txt`) |
| ⭐ **bytegleich** | **225** |
| abweichend | **0** |
| fehlend | **0** |

⇒ **Zwei Folgen, beide entlastend:**

**(a) TB-92 braucht keine Vorab-Nachrechnung.** Deine Bedingung — *„Wenn `data/`
≠ Snapshot, vor dem Vollzug die Tabelle auf dem Snapshot nachrechnen"* —
entfällt. **TB-91 hat bereits auf dem Snapshot gerechnet**; es fehlt nur die
Tatsachennotiz mit Snapshot-Hash und Code-Commit.

**(b) Der TB-93-Nachweislauf lief ebenfalls auf dem Snapshot.** Er ging über
`data/`, und `data/` ist der Snapshot. ⇒ **Die von dir angeordnete Neurechnung
führt zu genau der Datei, die bereits als `messgroessen_2026-09-23_nachweis.json`
vorliegt** — sie muss nur nach 36.1 an ihren Platz gebracht und belegt werden,
nicht neu gerechnet.

⚠️ **Eine Berichtigung an uns:** Der erste Durchlauf dieser Messung meldete „2
fehlend". Das waren die beiden Universumsdateien, die in `config/` liegen und
nicht in `data/` — ein Fehler unseres Suchpfads, kein Befund. Wir nennen ihn,
weil eine Zahl „223 von 225" sonst als Abweichung in die Akte ginge.

## 2. ⭐⭐ Messbitte (a): was `registerdaten.py` liest — und was davon abweicht

**Gemessen per AST, alle Zugriffe auf `mess[...]` und `_vola(...)`:**

| Gruppe | Blätter | ⚠️ abweichend | von `registerdaten.py` gelesen |
|---|---|---|---|
| `volatilitaet` | 56 | ⚠️⚠️ **39** | ⭐ **JA** — `_vola(mess, zeitrahmen, feld)`, sechs Aufrufstellen |
| `datenbereiche` | 20 | ⚠️ **9** | ⛔ **NEIN** |
| `haltedauer` | 36 | **0** | JA (`median_balken`) |
| `datenfrequenz` | 8 | **0** | JA (`balken_je_jahr`, `balken_je_handelswoche`) |
| `kosten` | 3 | **0** | JA (`round_trip_pct`) |
| `universum` | 4 | **0** | NEIN |

⇒ ⭐ **Von vier gelesenen Gruppen weicht genau eine ab: `volatilitaet`.** Die
neun Abweichungen in `datenbereiche` fliessen **nirgends** in eine Registergrösse
— sie sind Beschreibung, nicht Eingabe.

**Die gelesenen Felder, einzeln:**
`balken_sigma_pct` · `spanne20_median_pct` · `tiefabstand_median_pct` ·
`regel['kennzahl']` (Quantil-Achsen) — alle über `_vola`, alle aus `volatilitaet`.

### ⭐ Deine Unsicherheit zum Faltenplan — beantwortet

> *„ob `registerdaten.py` die Messgrössen nur für die Rastergrenzen liest oder
> auch für Grössen, die in 33.2 eingehen"*

**Gemessen:** `faltenplan.py` greift auf **genau einen** Pfad zu —
`mess["haltedauer"][bot]["max_tage"]`. ⭐ **`haltedauer` weicht an keinem einzigen
der 36 Blätter ab.**

⇒ **Der Faltenplan hängt nicht an den abweichenden Werten.** Das Nachziehen
reicht bis zu den Rastergrenzen und nicht weiter.

---

## 3. ⚠️⚠️ Und nun die Zahl, von der du sagtest, du kennst sie nicht

> *„Kein Ergebnis — und hier muss ich es besonders sagen: Ich weiss nicht, ob die
> Neurechnung Rastergrenzen oder Falten bewegt. Ich weiss nur, dass die Regel
> unabhängig davon dieselbe ist, und deshalb steht sie hier, **bevor** gerechnet
> wird."*

⭐ **Wir haben es gemessen — nach deiner Antwort 23c, aber bevor 23d vorlag.**
Deshalb stand es nicht in 23f, und deshalb legen wir es dir **erst jetzt** vor:
Deine Regel steht bereits und gilt unabhängig. Das Ergebnis sagt nur noch, **wie
weit** das Nachziehen reicht — genau das, was deine Messbitte (a) bestimmen
sollte.

| | eingefrorener Stand gegen Snapshot-Stand |
|---|---|
| ⭐ **Faltenpläne** | **unverändert — 9 von 9 Bots** |
| ⭐ **Zellenzahl je Bot** | **unverändert — 9 von 9** |
| ⭐ Rasterachsen gleich | **22** |
| ⚠️⚠️ **Rasterachsen verschieden** | **12** |
| Stufen**zahl** je Achse | unverändert (4/4, 5/5, 6/6) |
| Betroffene Bots | `elliott_wave`, `rsi2_crypto`, `t3_supertrend`, `turtle_soup_crypto`, `volatility_breakout_crypto` — ⭐ **die fünf Krypto-Bots** |
| Unberührt | die vier Aktien-Bots |

⇒ **Der Selektionsraum behält seine Form und seine Grösse; zwölf Achsen tragen
andere Gitterpunkte.**

⛔ **Sichtschutz 27.1:** Die Stufenwerte selbst nennen wir nicht.

⭐ *Wir halten fest, dass deine Bauart hier getragen hat: Die Regel stand, bevor
die Zahl bekannt war. Hätten wir sie dir vorher genannt, wäre jede Entscheidung
angreifbar gewesen — so ist sie es nicht.*

---

## 4. Was daraus für die Aufträge folgt — zur Gegenprüfung

| | |
|---|---|
| **TB-92** | Sperre gelöst. Schritt 1a (`auswertung.py`, **eine** Konstante, kein Schalter, AST) kommt hinzu; `test_vorregistrierung.py` und `beispieldaten.py` lesen dieselbe Konstante. ⭐ **Keine** Vorab-Nachrechnung nötig (Messbitte b), nur die Tatsachennotiz mit Snapshot-Hash und Code-Commit |
| **TB-94** (neu) | `messgroessen.json`: die **vorhandene** Nachweisdatei nach 36.1 an ihren Platz, Notiz, `registerdaten.py` auf die neue Datei (Konstante, AST) — ⭐ **kein neuer Rechenlauf**, weil der vorhandene auf dem Snapshot lief |
| **dann** | Raster nachziehen und vergleichen: **12 Achsen** sind Berichtigung mit deinem Grund „Eingabe war auf nicht-registriertem Datenstand gerechnet"; **22 Achsen** und **alle Faltenpläne** werden als unverändert festgehalten |
| **Sonde** | Schreibziele · **Lesequellen** · Berechtigungsdatei-Abgleich · Eingabestand-Notiz je Eingabedatei — ein eigener Auftrag |

⚠️ **Zur Gegenprüfung, nicht als Entscheidung:** Wir lesen dich so, dass die
vorhandene Nachweisdatei genügt, weil sie auf dem Snapshot entstand und dein
Text den **Nachweis** verlangt, nicht den erneuten Lauf. Liest du das anders,
rechnen wir neu — es kostet elf Sekunden.

---

## In einfacher Sprache

**Beide Fragen, die der Verfahrensprüfer vor der Neurechnung beantwortet haben
wollte, sind gemessen — und beide fallen günstig aus.**

Der eingefrorene Datenbestand und das Arbeitsverzeichnis sind Byte für Byte
identisch, alle 225 Dateien. Das heisst: Was heute gerechnet wird, ist schon auf
dem registrierten Stand gerechnet. Die Vergleichstabelle von gestern braucht
deshalb keine Wiederholung, nur einen Vermerk, und die Messdatei muss nicht neu
berechnet werden — die richtige Fassung existiert bereits.

Und die Frage, wie weit die Folgen reichen: Das Regelwerk liest vier Gruppen aus
der Messdatei. Nur eine davon hat sich geändert, die Schwankungsmasse der
Kryptowährungen. Der Zeitraumplan hängt an einer anderen Gruppe, die unverändert
ist — er bleibt also, wie er ist.

**Was sich ändert, sind zwölf von vierunddreissig Parameterachsen**, alle bei den
Krypto-Bots. Der Suchraum behält Form und Grösse, aber ein Teil seiner Gitterpunkte
liegt anders. Der Verfahrensprüfer hatte seine Regel aufgestellt, ohne diese Zahl
zu kennen — und das war richtig so: Sie hätte die Entscheidung sonst beeinflussen
können.
