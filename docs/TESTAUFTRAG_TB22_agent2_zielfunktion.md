# Testauftrag: die Zielfunktion von Agent 2 (TB-22)

**Stand: 2026-09-13** · Gegenstand: die Änderung aus TB-22 an
`shared/param_search_agent.py`. Dieses Dokument ist **eigenständig ausführbar**:
es setzt nichts voraus ausser dem Repo, Python 3 und `pandas`.

---

## 0. Worum es geht (in drei Sätzen)

Agent 2 (`shared/param_search_agent.py`) schlägt Parameter vor. Er wählt seit
TB-22 nach `robustness_score_chronologisch` — dem `robustness_score`, gerechnet
auf `max_drawdown_chronologisch_pct` statt auf dem Drawdown der
aneinandergehängten Symbol-Blöcke.

**Das ist die Zusicherung, die zu prüfen ist:** Führen die beiden Maße zu
verschiedenen Rangfolgen, gewinnt die chronologische. Alles andere in diesem
Dokument dient ihr.

---

## 1. Voraussetzungen

| | |
|---|---|
| Python | 3.9+ (getestet mit 3.11) |
| Pflicht | `pandas` |
| Nicht nötig | `anthropic`, `binance`, `scipy`, `yfinance`, `node`, Netzzugang, API-Schlüssel, `config/email_config.py` |

Der Test legt für alles Fehlende Attrappen an (`anthropic`, `binance`,
`email_config`, `telegram_config`, die Kursdaten-Abrufmodule). Jede davon wirft
beim Aufruf `AssertionError` — er kann also gar nicht unbemerkt ins Netz gehen
oder etwas verschicken.

**Er ruft keine Kursdaten ab, verschickt nichts, schreibt keine Datei und fasst
keine Datenbank an.** Abschnitt 6 des Tests weist das per `git status` nach.

---

## 2. Der eine Befehl

```bash
cd <repo>
python3 shared/test_agent2_zielfunktion.py
```

**Erwartet:** `41 von 41 Pruefungen bestanden, 0 fehlgeschlagen.` und
Rückgabewert `0` (Stand 2026-09-13; die Zahl wächst, wenn Prüfungen dazukommen —
entscheidend ist die `0` hinter „fehlgeschlagen").

Laufzeit: **etwa 4 Sekunden.**

Einzelne Teile (nützlich beim Nachstellen eines Fehlschlags):

```bash
python3 shared/test_agent2_zielfunktion.py --bot t3_supertrend
python3 shared/test_agent2_zielfunktion.py --mutation auswahl_auf_blockmass
```

Der `--mutation`-Aufruf ist eine **Innenansicht**: er lässt die Prüfung auf
einer absichtlich kaputten Kopie laufen und gibt `1` zurück, wenn sie — wie
gewollt — durchfällt.

---

## 3. Was der Test prüft, und wie

### Abschnitt 1 — die Zusicherung (4 Prüfungen)

**1a, über 40 erzeugte Datensätze.** Ein Zufallsgenerator mit festem Startwert
erzeugt Ergebnistabellen, wie `evaluate_combination_multi` sie liefert (beide
Drawdown-Maße, der `robustness_score` auf dem Blockmaß). Eine im Test **getrennt
geschriebene** Rangfolge rechnet für jeden Datensatz aus, wer auf welchem Maß
gewinnen müsste. Nur die Datensätze, in denen die beiden Sieger **verschieden**
sind, sind der Prüffall — dass es solche überhaupt gibt, wird eigens geprüft
(Stand 2026-09-13: 31 von 40). In **jedem** davon muss der Agent den
chronologischen Sieger wählen.

**1b, ohne jede Formel.** Zwei Zeilen mit gleicher Rendite und gleicher
Trade-Zahl, deren Drawdowns über Kreuz stehen (−10 / −200 gegen −200 / −10).
Welche gewinnen muss, ergibt sich aus „kleinerer Rückgang ist besser" — ohne
dass man etwas ausrechnen müsste. Diese Prüfung hängt an keiner Formel, an
keiner Rundung und an keiner Tabelle.

### Abschnitt 2 — Gegenprobe (7 Prüfungen)

Sind beide Drawdowns **gleich**, muss der Agent denselben Gewinner wählen wie
auf dem alten Maß, und der neue Score muss Zeile für Zeile dem alten gleichen.
Die Umstellung erfindet keine neue Zahl, sie nimmt einen anderen Nenner.

**2c prüft den Ersatzweg**, der greift, wenn `run_agent_search` ausserhalb der
neun Bots mit einer `evaluate_fn` ohne chronologischen Drawdown aufgerufen wird:
er muss **benannt** werden (im Ergebnis und im Prompt), er muss dann nach dem
alten Maß wählen — und er darf **nicht** greifen, sobald der Wert vorliegt. Das
ist die Wache, die andernfalls das Fehlen der ersten verdecken könnte.

### Abschnitt 3 — der Prompt sagt es (7 Prüfungen)

Geprüft wird der Prompt, der **tatsächlich abgeschickt wird** — die Attrappe
schreibt jeden mit. Er muss

* genau das Feld nennen, nach dem die Auswahl **tatsächlich** lief (aus dem
  Ergebnis gelesen, nicht hingeschrieben — so können Prompt und Auswahl nicht
  auseinanderlaufen),
* einen ausgewiesenen Abschnitt „ZIELGROESSE DER AUSWAHL" haben,
* sagen, dass das Blockmaß **nicht** das Auswahlkriterium ist,
* **beide** Maße in der Tabelle führen (ausweisen, nicht verschweigen).

Zusätzlich muss die **Ausgabe** die Zielgröße benennen, nicht nur der Prompt.

### Abschnitt 4 — die Unvalidiert-Kennzeichnung bleibt (3 × 6 Prüfungen)

End-to-End über den **echten** `quarterly_review.build_report()` jedes der drei
Bots, die Agent 2 überhaupt aufrufen — **ein Prozess je Bot**, sonst lädt
`sys.modules` still den falschen. Geprüft wird, dass Überschrift, Pflichthinweis
und Schlusshinweis unverändert im Bericht stehen, dass die Zielgrößen-Angabe
dazugekommen ist — und, als Gegenprobe, dass ein Bericht **ohne** die Angabe sie
auch wirklich nicht enthält (sonst prüfte die Zeile darüber nichts) und der
Pflichthinweis **nicht** an ihr hängt.

### Abschnitt 5 — Mutationsproben (5 Prüfungen)

Jede Wache wird einzeln aus einer **Kopie** der Datei entfernt, die Kopie unter
dem kanonischen Modulnamen geladen und die zugehörige Prüfung darauf laufen
gelassen. Sie **muss** dann anschlagen:

| Mutation | trifft |
|---|---|
| `auswahl_auf_blockmass` — `max(...)` wieder auf `robustness_score` | Abschnitt 1 |
| `score_auf_blockdrawdown` — der neue Score rechnet auf dem Blockmaß | Abschnitt 1 |
| `zielgroesse_nicht_im_prompt` — der Abschnitt fällt aus der Nachricht | Abschnitt 3 |
| `prompt_nennt_falsches_mass` — der Prompt nennt das Blockmaß als maßgeblich | Abschnitt 3 |
| `ausgabe_ohne_zielgroesse` — `zielmass_zeile()` gibt Leerstring zurück | Abschnitt 4 |

Die Kopien entstehen ausschliesslich unterhalb des Temporärverzeichnisses.

### Abschnitt 6 — Folgenlosigkeit (1 Prüfung)

`git status --porcelain` vor und nach dem Lauf muss identisch sein.

---

## 4. Die zwei Fallen, die bewusst umgangen sind

Sie sind aus #73, #77, #78, #79, #81, #86, TB-15 und TB-20 bekannt.

**Falle 1 — die selbstbestätigende Probe.** Nirgends steht ein Gewinner von Hand
hingeschrieben und wird anschliessend wiedererkannt. Die Datensätze entstehen
aus einem Zufallsgenerator; welche Zeile gewinnen muss, rechnet eine getrennt
geschriebene Rangfolge aus; dass der Prüffall überhaupt eintritt (beide Maße
gehen auseinander), wird vorab nachgewiesen statt vorausgesetzt. Abschnitt 1b
kommt ganz ohne Formel aus, Abschnitt 5 beobachtet den **Ablauf** an mutierten
Kopien.

**Falle 2 — die zweite Wache verdeckt das Fehlen der ersten.** Die Prüffälle
sind so gewählt, dass je nur eine Zusicherung greifen kann:

* **Abschnitt 1** hängt ausschliesslich an der Auswahl. Die Attrappe schlägt
  ohnehin **jede** Kombination des Datensatzes der Reihe nach vor — das Modell
  entscheidet nichts, und was im Prompt steht, ist für diesen Abschnitt
  gleichgültig.
* **Abschnitt 3** hängt ausschliesslich am abgeschickten Prompt und sagt nichts
  darüber, wer gewinnt.
* **Abschnitt 2** kann nur über Gleichheit beider Maße bestehen.
* **Abschnitt 4** hängt an einer Konstanten aus `shared/empfehlung_format.py`,
  die mit der Zielgröße nichts zu tun hat — und prüft beide Richtungen getrennt.

---

## 5. Kein einziger echter API-Aufruf

Zwei unabhängige Vorkehrungen:

1. Der **Sendeweg ist ein Parameter**: `run_agent_search(…, call_fn=)`. Der Test
   reicht eine Attrappe herein, die jeden Prompt mitschreibt und JSON
   zurückgibt.
2. Zusätzlich wird `param_search_agent.call_claude` für die Dauer jedes Laufs
   durch eine Funktion ersetzt, die beim Aufruf sofort eine Ausnahme wirft.
   Käme irgendein Pfad doch am Parameter vorbei, fällt der Test **hart** durch,
   statt still ins Netz zu gehen.

Dazu die `anthropic`-Attrappe aus Abschnitt 1 dieses Dokuments, die schon beim
Anlegen eines Clients abbricht.

---

## 6. Gegenprobe: alle bestehenden Tests

```bash
python3 shared/test_drawdown_beide_masse.py --ohne-kursdaten   # 181/181
python3 shared/test_empfehlung_format.py                        #  70/70
python3 shared/test_live_params_werte.py                        #  69/69
python3 shared/test_ergebniskurven.py                           #  44/44
python3 shared/test_stabile_sortierung.py                       #  46/46
python3 shared/test_wellenauswahl.py                            # 323/323
python3 notifications/test_schliess_benachrichtigung.py         #  99/99
python3 broker/test_broker.py                                   # 163/163
python3 system/test_log_rotation.py                             # 117/117
python3 system/test_caffeinate_plist.py                         #  53/53
```

**Umgebungsbedingte Fehlschläge**, die auf unverändertem `main` genauso
auftreten (mit einem Basislauf belegt — Tabelle im Ergebnisdokument):

| Test | Grund |
|---|---|
| `shared/test_kursdaten.py` | 62/66 — `yfinance` fehlt |
| `dashboard/test_dashboard.py` | Abbruch — `fastapi` fehlt |
| `dashboard/test_portfolio_sicht.py` | 66/68 — `fastapi` fehlt |
| `broker/test_ibkr.py` | Abbruch — Zeitzonendaten `US/Eastern` fehlen |
| `system/test_dienst_plists.py` | 140/144, 4 offene Platzhalter (kein Fehlschlag) |

Ohne `node` überspringt `dashboard/test_dashboard.py` zusätzlich vier Prüfungen
und meldet 780/780 statt 784.

---

## 7. Was ein Fehlschlag bedeutet

| Abschnitt | Fällt durch, wenn … |
|---|---|
| 1a / 1b | die Auswahl wieder am Blockmaß hängt — **der Befund, um den es in TB-22 geht** |
| 2 | die Umstellung mehr ändert als beabsichtigt |
| 2c | der Ersatzweg still greift oder nicht benannt wird |
| 3 | der Prompt nicht (mehr) sagt, worauf ausgewählt wird — ein Vorschlag ohne nachvollziehbare Grundlage |
| 4 | die Unvalidiert-Kennzeichnung fehlt oder die Zielgrößen-Angabe nicht im Bericht ankommt |
| 5 | eine Prüfung besteht **trotz** entfernter Wache — dann prüft sie nichts |
| 6 | der Testlauf hat etwas im Repo verändert |
