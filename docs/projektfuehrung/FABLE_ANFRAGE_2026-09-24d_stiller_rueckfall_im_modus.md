# FABLE_ANFRAGE 2026-09-24d — ⚠️⚠️ Unter dem Selektionsmodus fallen alle neun Bots still auf eine Fünf-Symbol-Standardliste zurück, und das Ladeprotokoll meldet „Keines ausgelassen"

*An den Verfahrensprüfer. Bezug: Register 40.6, dein Text aus 24a Abschnitt 3. TB-98 ist abgegeben und hat **Block C und D nicht ausgeführt** — aus zwei Gründen, die mit dem Erzeuger wenig zu tun haben. **Der erste ist ein Tagblocker.** Zwei Entscheidungsfragen.*

⚠️ **Sichtschutz 27.1 gewahrt:** keine Trade-Zahlen, **keine Faltenlänge**. Die Zahlen unten sind Symbolzahlen, Hashes und Rückgabewerte (27.2).

---

## 1. ⚠️⚠️ Befund 1 — der stille Rückfall

**Gemessen, neun Bots, je mit und ohne Modus, mit Lesehaken und Aufrufstapel:**

| | mit Modus | ohne Modus |
|---|---|---|
| Kursdaten | ⭐ **aus dem Snapshot**, 0 Zugriffe auf `data/`, 9/9 | `data/` |
| Symbolliste | ⛔ **9× „nicht gefunden. Nutze Standardliste (5 …)"** | gefunden |
| Ladeprotokoll | ⛔ **9× „Geladen: 5 von 5 Symbolen. Keines ausgelassen."** | Krypto 18/24 bzw. 20/24, Aktien 147/150 |

**Die Ursache liegt zwischen Resolver und Snapshot-Aufbau, nicht im Erzeuger.** Der
Snapshot legt die zwei Universumsdateien unter `config/` ab; `shared/paths.py`
setzt unter dem Modus `CONFIG_DIR` auf die **flache Snapshot-Wurzel** (Kopf: *„Die
Snapshot-Wurzel ist flach"*). `symbols_config.py` und
`stocks_symbols_config.py` suchen dort, finden nichts — und nehmen ihre
eingebaute Standardliste.

⭐ **Gegenprobe:** Mit denselben Listen zusätzlich flach in der Wurzel (Hilfsordner
aus Verknüpfungen auf den echten Snapshot) liest der Erzeuger **ausschliesslich**
aus dem Snapshot, 24 bzw. 150 Symbole, 0 Zugriffe auf `data/` oder `config/` im
Repo. ⇒ **Der Modus trägt. Nur die Listen findet er nicht.**

⚠️⚠️ **Die Reichweite: Das gilt für JEDEN Lauf unter dem Modus**, der die
Symbollisten über diese zwei Module liest — nicht nur für diesen Erzeuger. Nach
bisherigem Stand hat **vor TB-98 kein Bot-Lauf unter dem Modus gegen den echten
Snapshot stattgefunden** (null Treffer für die Warnzeile in allen Belegen). ⇒ **Es
ist niemandem aufgefallen, weil es niemand getan hat.**

⭐⭐ **Warum das schwerer wiegt als eine falsche Zahl:** Der Lauf bricht nicht ab.
Er meldet **„Keines ausgelassen"** — eine Aussage, die gerade dann falsch ist, wenn
sie beruhigt. Das ist derselbe stille Ausfall, gegen den der Modus gebaut ist:
`shared/paths.py` wirft unter dem Modus absichtlich einen Fehler, statt einen
falschen Pfad zu liefern, *„damit kein `except Exception` im Aufrufer den Abbruch
in einen stillen Weiterlauf verwandelt"* (22e). Hier wird er es doch.

⚠️ Deine Regel aus 23d — *„eine Eingabe des Laufs ist aus dem registrierten
Snapshot reproduzierbar"* — wäre erfüllt und das Ergebnis trotzdem falsch. **Der
Datenstand stimmte; die Datenmenge nicht.**

## 2. ⚠️ Befund 2 — der Erzeuger läuft mit dem heutigen Code nicht

9/9 Bots brechen **vor dem Schreiben** ab: *„Kennzeichnung hat die Simulation
verändert."*

`positionen_holen.py` ordnet ausgeführte Trades zu, indem es eine **Zeilenkennung
ins Symbol** schreibt (`AAPL#417`). Seit der Zuteilungskaskade aus **TB-26**
(`shared/zuteilung.py`, **Sperrlistenpunkt 10**) fliesst `symbol` in den
Zufallsschlüssel der letzten Stufe — die Kennung verschiebt damit die Zuteilung.
Die **Selbstprüfung des Erzeugers erkennt das und bricht ab**, statt eine
verfälschte Liste zu schreiben.

| | |
|---|---|
| Gegenprobe: Stufe-4-Schlüssel ohne die Kennung | **0 von 9** Bots weichen ab |
| Die alten Listen (`78e2bc6`, 13.09.) | entstanden **vor** TB-26 (`f6d9a28`) |
| ⭐ Für die Faltenlänge zählt | nur `entry_time` der **gefundenen** Trades — die hängt **nicht** an der Zuteilung |

⚠️ **Eine Tatsachennotiz, die dabei anfällt:** Der Kopf von `bot_lauf.py` sagt,
`symbol` sei *„ausschliesslich Beschriftung"*. **Seit TB-26 gilt das nicht mehr.**

## 3. Was TB-98 deshalb **nicht** getan hat

⛔ **Keine Liste erzeugt. Keine Faltenlänge gerechnet — auch nicht „zur
Orientierung".**

⭐ **Der Grund ist deiner:** Technisch wäre sie zu haben, weil `entry_time` nicht
an der Simulation hängt. Aber **wie die zwei Befunde behoben werden, ist nicht
entschieden** — und ein Ergebnis, das vorher bekannt ist, färbt diese Entscheidung
nach Wirkung. Das ist 24.3 und dein eigener Satz aus 40.6: *die Regel steht, bevor
gerechnet ist.*

**Was fertig ist:** Der Erzeuger steht nach 36.1 — `--ziel` Pflicht ohne
Voreinstellung, geprüft **vor** dem Import; Einmal-Schreibsperre **vor der
Rechnung** (der Lesehaken zählt dabei 0 Kursdateien); `O_CREAT|O_EXCL` beim
Schreiben; AST gegen den Vorstand: vier von fünf Funktionen gleich, in `main` nur
die Schreibaufrufe; Schreibformat alt gegen neu **27/27 bytegleich**.
⭐ **Nachgewiesen auch gegen den historischen Ordner selbst:** Aufruf mit `--ziel`
auf `daten/` ergibt rc 1, **27 Dateien mit gleichem Hash und gleicher mtime**. Die
Überschreibgefahr aus 40.6 ist damit dauerhaft weg.

Von 56 gemessenen Pfaden haben sich **genau zwei** bewegt (die zwei
Erzeuger-Dateien). `snapshot.py --pruefen`: **UNVERÄNDERT**.

## 4. Zwei Entscheidungsfragen

**(1) ⭐⭐ Wo wird der stille Rückfall behoben — und ist er künftig ein Abbruch?**

| Weg | Folge |
|---|---|
| **Der Resolver**: unter dem Modus `CONFIG_DIR` = `<snapshot>/config` | **eine Stelle**; Snapshot und Hash unberührt. `shared/paths.py` steht auf keinem Sperrlistenpunkt |
| Die **fünf Symbol-Module** | fünf Stellen, und ein zweiter Resolver entstünde — `strategy_paths.py` sagt ausdrücklich *„Hier steht KEIN zweiter Resolver"* |
| Der **Snapshot-Aufbau** (Listen flach) | neuer Snapshot, **neuer Hash**, Register 18 betroffen |

⭐ *Wir neigen zum Resolver: eine Stelle, kein zweiter Weg, kein neuer Snapshot.*

⚠️⚠️ **Und die Frage dahinter, die wir für die wichtigere halten:** Muss ein
Rückfall auf die Standardliste **unter dem Modus** ein **Abbruch** sein statt einer
Warnung? Jeder Fallback, der unter dem Modus greift, ist ein Weg an dem vorbei, was
der Modus garantieren soll. ⭐ *Eine Wache, die im Zweifel weiterläuft, ist keine —
und „Keines ausgelassen" ist schlimmer als gar keine Meldung.*

**(2) Wie wird die Neu-Erzeugung möglich, ohne den Rechenweg zu verfälschen?**

Die Zuteilung ist gesperrt (Punkt 10), also muss sich der **Erzeuger** ändern —
und das ist eine Änderung seines Rechenwegs, die TB-98 ausdrücklich verboten hat
(deshalb liegt die Frage hier).

| Möglichkeit | offen |
|---|---|
| Zuordnung über eine Spalte, die der Zufallsschlüssel **nicht** liest | ⚠️ ob `simulate_portfolio` eine solche Spalte durchreicht, ist **nicht gemessen** |
| `_alle_trades.csv` **ohne** die Simulationsspalte `ausgefuehrt` | ergäbe ein **anderes Dateiformat** als die historischen Listen |

⇒ **Welche Form ist „der registrierte Code" im Sinn von 40.6?** ⭐ Für die
Faltenlänge selbst ist die Frage folgenlos — sie liest nur `entry_time`. Für die
**Vergleichbarkeit mit den alten Listen** ist sie es nicht.

## 5. Ein Nebenbefund für den Folgeauftrag

⚠️ Es gibt einen **zweiten Leser mit eigener Pfadangabe**:
`research/faltenplan_neun/faltenplan_neun.py` hat eine eigene Funktion
`gefundene_trades_je_jahr` **und eine eigene Konstante** `TB24_DATEN`. ⇒ Eine
registrierte Pfadkonstante in `faltenplan.py` allein lenkt ihn **nicht** um. Dein
Registertext aus 40.6 verlangt, dass `faltenplan.py` die neuen Listen über einen
registrierten Pfad liest — nach dieser Messung sind es **zwei** Dateien.

## 6. Was mitgeschickt wird

⛔ **Nichts.** Der Text ist selbsttragend. `belege/` bleibt nach 27.1 gesperrt.

---

## In einfacher Sprache

Der Auftrag sollte neun Handelslisten aus dem eingefrorenen Datenbestand neu
erzeugen. Er hat sie **nicht** erzeugt — und das ist die richtige Entscheidung.

Die Messung, die vorher kommen sollte, hat etwas Ernstes gefunden. Wenn ein
Bot-Lauf im geschützten Modus startet, findet er die Liste seiner Handelssymbole
nicht: Sie liegt im eingefrorenen Bestand in einem Unterordner, gesucht wird sie
eine Ebene höher. Der Lauf bricht dann **nicht** ab. Er nimmt eine eingebaute
Notliste von fünf Symbolen statt der 24 beziehungsweise 150 — und schreibt ins
Protokoll: **„Geladen: 5 von 5 Symbolen. Keines ausgelassen."** Ein Satz, der
beruhigt und dabei falsch ist.

Das betrifft nicht nur diesen einen Auftrag, sondern **jeden** Lauf in diesem
Modus. Aufgefallen ist es bisher nicht, weil vor diesem Auftrag noch nie ein
Bot-Lauf so gestartet wurde. Behoben ist es nicht — wo es behoben wird, ist eine
Entscheidung: an einer zentralen Stelle, an fünf einzelnen, oder am Aufbau des
Datenbestands selbst, was einen neuen Bestand mit neuer Prüfsumme bedeutete.

Das zweite Hindernis: Das Erzeugerprogramm läuft mit dem heutigen Code überhaupt
nicht mehr. Es markiert Handelszeilen, indem es ein Kürzel an den Symbolnamen
hängt — und seit einer Änderung von vor elf Tagen fliesst der Symbolname in eine
Zufallsentscheidung ein. Die Markierung verschiebt also genau das, was sie nur
beobachten sollte. Das Programm merkt das selbst und bricht ab, statt eine
verfälschte Liste zu schreiben. Auch gut.

Bewusst **nicht** getan: die Abschnittslänge schon mal „zur Orientierung"
ausrechnen. Sie wäre technisch zu haben. Aber solange offen ist, wie die beiden
Hindernisse behoben werden, würde ein bekanntes Ergebnis diese Entscheidung
färben — und genau das soll die Reihenfolge verhindern.
