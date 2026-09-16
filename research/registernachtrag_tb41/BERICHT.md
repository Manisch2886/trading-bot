# Registernachtrag TB-41 — Prüfwerkzeug

**Abgeschlossene Arbeit.** Dieser Ordner enthält **kein** Untersuchungsergebnis,
sondern das Werkzeug, mit dem der Registernachtrag TB-41 geprüft wird. Er fasst
**keinen** Bot-Code an, ändert keine Kursdatei, keinen Parameter und keine
Datei unter `research/faltenplan_neun/`, `research/universum_trockenlauf/` oder
`research/etf_trendfolge/`.

Registereintrag: `docs/VORREGISTRIERUNG_neuselektion.md`, **Abschnitt 16**
Ergebnis zum Kopieren: `docs/ERGEBNIS_TB-41_registernachtrag.md`
Testauftrag für den Mac: `docs/TESTAUFTRAG_TB-41_registernachtrag.md`

---

## 1. Warum es das gibt

Ein Registernachtrag trägt Zahlen ein, die **woanders** gemessen wurden. Genau
da geht so etwas kaputt: jemand tippt 137 als 173, und niemand merkt es, weil
die Quelle in einem anderen Dokument steht. Die Aufgabenstellung verlangt
deshalb ausdrücklich: *maschinell verglichen, nicht abgetippt.*

Dieses Werkzeug tippt nichts ab. Es liest jede eingetragene Zahl aus dem
Register, liest sie ein zweites Mal aus ihrer Quelle und vergleicht.

## 2. Die neun Prüfungen

```bash
python3 research/registernachtrag_tb41/pruefe_register.py
python3 research/registernachtrag_tb41/test_registernachtrag_tb41.py
```

| Prüfung | Register | Quelle |
|---|---|---|
| `symbolzahl` | 16.1.1 | TB-40-Trockenlauf bzw. dessen Ergebnisdokument |
| `faltenevidenz` | 16.1.2 | dieselbe |
| `min_history` | 16.7 (b) | die neun `strategies/<bot>/multi_symbol_optimise.py`, **gelesen** |
| `umstellungstag` | 16.5 | `docs/umstellungstag_entscheidungskerze.json` |
| `universumsdatei` | 16.1.3 | `config/top25_symbols.txt`, `shared/symbols_config.py` |
| `datenstand` | 16.0 | SHA-256 über `data/` |
| `daten_unberuehrt` | Randbedingung | `git diff` / `git status` über `data/` |
| `null_entfernte_zeilen` | Randbedingung | `git diff --numstat` über die zwei Registerdateien |
| `ersetzt_gekennzeichnet` | 15.4 / 15.5 / 15.7 | das Register selbst |

Einzeln aufrufbar mit `--nur <name>` — das ist kein Komfort, sondern
Voraussetzung für Prüfteil I (unten).

## 3. Zwei Belegquellen für dieselbe Zahl

Die Messung selbst ist **TB-40**, nicht diese Arbeit. Wo dessen Werkzeug laufen
kann (Bot-Abhängigkeiten vorhanden, also auf dem MacBook), wird es aufgerufen
und sein JSON gelesen — das ist die harte Form. Wo es das nicht kann (Cloud:
kein `pandas`, Binance mit 403 gesperrt), wird das **committete
Ergebnisdokument** von TB-40 geparst.

**Welche Quelle benutzt wurde, steht im Bericht.** Geraten wird nichts, und
stillschweigend ausgelassen wird auch nichts: fällt der Trockenlauf aus, nennt
die Zeile `Quelle beleg:` den Grund.

## 4. Der Selbsttest: 41 Prüfungen

| Teil | Was er zeigt |
|---|---|
| A | alle neun Prüfungen auf dem echten Repo, kein Befund |
| B | null entfernte Zeilen — am Diff gemessen, und es wurde wirklich etwas ergänzt |
| C | jede ersetzte Fassung steht noch da **und** trägt den Verweis |
| D | Mutationsprobe: eine geänderte Registerzahl wird gemeldet — und ohne die Mutation meldet derselbe Aufruf nichts |
| E | Mutationsprobe: ein geändertes Symbol in der Evidenzliste wird gemeldet |
| F | Mutationsprobe: eine geänderte Bot-Datei wird gemeldet |
| G | Mutationsprobe: fällt der „ERSETZT"-Verweis weg, wird es gemeldet |
| H | Mutationsprobe: eine entfernte Registerzeile wird gemeldet |
| I | **zwei Wachen gegen dasselbe Risiko, einzeln geprüft** |
| J | der Beleg ist nicht abgetippt: zwei getrennte Parser, zwei Dateien, dieselben Zahlen |

### Zu den beiden wiederkehrenden Fallen

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich
   selbst.** Deshalb biegt hier keine Probe eine Variable im laufenden Prozess
   um. Jede kopiert die betroffenen Dateien in ein Wegwerf-Verzeichnis, ändert
   dort **genau eine** Zeile und startet `pruefe_register.py` als **eigenen
   Prozess**. Beobachtet wird der **Ablauf** — Rückgabewert und Befundtext —,
   nicht eine Variable, die der Test selbst gesetzt hat.
2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Gegen das Risiko „eine
   Kursdatei hat sich verändert" stehen hier zwei: der Datenstand-Hash und
   `git`. In Teil I laufen sie **einzeln** (`--nur datenstand` bzw.
   `--nur daten_unberuehrt`) gegen **dieselbe** Mutation — eine geänderte Zahl
   in einer erzeugten Kursdatei eines Wegwerf-Repos. Beide greifen für sich.
   Das echte `data/` wird dabei nur gelesen; der Test prüft auch das.

## 5. Was dabei aufgefallen ist

**Eine vierte falsche Zahl**, die in der Aufgabenstellung nicht steht: der
Wortlaut von Registertext 3b (b) spricht von **„den fünf Werten"** von
`MIN_HISTORY_*`. Gezählt sind es **vier** (17 520 · 730 · 500 · 1 825) in zwei
Einheiten. Die Zahl stammt aus TB-40 und ist dort schon falsch. **Der Wortlaut
bleibt stehen** — er ist der registrierte —, die Tatsachennotiz daneben sagt,
was gezählt wurde. Siehe Register 16.1.4 und 16.7.

## 6. Was dieser Ordner nicht tut

* **Kein Selektionslauf, kein Raster, keine Parameterübernahme.**
* **Keine Messung.** Die Symbolzahlen stammen aus TB-40; hier wird verglichen.
* **Keine Kursdatei angefasst** — als Test nachgewiesen.
* **`research/universum_trockenlauf/` unberührt** — es ist die Belegquelle und
  wird nur aufgerufen.

---

## In einfacher Sprache

**Was wir wissen wollten.** Ob die Zahlen, die wir ins Vorab-Dokument
(„Register") eingetragen haben, wirklich dieselben sind wie die, die vorher
gemessen wurden — und nicht beim Übertragen verrutscht sind.

**Was herauskam.** Alle stimmen. Neun Prüfungen, kein Befund. Dabei ist
zusätzlich aufgefallen, dass ein Wort im Register („fünf Werte") nicht zur
Tabelle darunter passt; richtig sind vier. Das steht jetzt daneben.

**Warum das so ist.** Ein Programm liest die Zahl aus dem Register, ein zweites
liest dieselbe Zahl aus der Quelle, und dann werden sie verglichen. Abgetippt
wird nichts — ein Tippfehler fällt sofort auf. Wir haben das Programm
absichtlich in Kopien kaputt gemacht (eine Zahl verändert, eine Zeile gelöscht,
einen Hinweis entfernt), und jedes Mal hat es Alarm geschlagen.

**Was das für dich heisst.** Du musst die Zahlen nicht nachzählen. Ein Befehl
genügt, und er sagt entweder „kein Befund" oder nennt genau die Stelle, die
nicht stimmt. Am MacBook prüft er zusätzlich gegen eine frische Messung statt
gegen das aufgeschriebene Ergebnis.

---

*TB-41, 16.09.2026. Kein Selektionslauf, kein signierter Tag, keine
Parameterübernahme.*
