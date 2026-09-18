# Der Resolver-Modus und sein Nachweis — TB-52, Teil 1

**Gemessen 18.09.2026.** Die Werkzeuge, mit denen die TB-52-Freigabe für
`shared/paths.py` belegt wird.

| Datei | |
|---|---|
| `pfadvergleich.py` | alte gegen neue Fassung, alle neun Bots, **ohne** gesetzten Modus |
| `kindprozess.py` | was im Kindprozess passiert — sieben Messungen |
| `ergebnisse/pfadvergleich.json` · `ergebnisse/kindprozess.json` | die Messwerte |

> ⚠️ **Beide Werkzeuge ändern nichts** und rühren `data/` nicht an. Wo ein
> Snapshot gebraucht würde, steht eine **Attrappe** im Wegwerfordner — nach
> Registertext 5 / **F1a** wird der Snapshot erst am Tag des signierten Tags
> gezogen.

---

## Der Pfadvergleich — die Bedingung, an der die Freigabe hängt

> ⭐ **Ohne gesetzten Modus liefert `paths.py` dieselben Zeichenketten wie
> vorher.**

| | |
|---|---|
| **Bezugscommit** | `062bacf62638f41df55d3f861feb4f6281fdef18`, festgenagelt (**B3**) |
| **Verglichene Pfade** | ⭐ **99** — 9 Bots × 11 Pfadarten |
| **Unterschiede** | ⭐ **0** |
| **Nur in der neuen Fassung** | 5 Zugänge: `LIVE_DATA_DIR`, `LIVE_CONFIG_DIR`, `MANIFEST`, `UMGEBUNG_HASH`, `UMGEBUNG_WURZEL` |

**Die 11 Pfadarten je Bot:** aus `paths` die vier `SHARED_DIR`, `BASE_DIR`,
`DATA_DIR`, `CONFIG_DIR`; aus `strategy_paths` die sieben `BASE_DIR`,
`STRATEGY_NAME`, `DATA_DIR`, `CONFIG_DIR`, `RESULTS_DIR`, `LOGS_DIR`, `DB_FILE`.
`strategy_paths.py` ist **nicht** geändert worden und steht als Kontrolle dabei.

**Wie gemessen wird — und warum so:**

- Die alte Fassung kommt aus `git show <BEZUGSCOMMIT>:shared/paths.py`, nicht
  aus dem Gedächtnis und nicht aus einer Kopie im Arbeitsbaum.
- Beide Fassungen laufen in **je einem eigenen Prozess** (**B6**, TB-40) und in
  **je einem eigenen Wegwerfbaum** gleicher Form, damit beide dieselbe
  `BASE_DIR` haben und die Zeichenketten direkt vergleichbar sind.
- Je Bot wird **aus der Sicht dieses Bots** gemessen: der Probeprozess baut
  `sys.path` genau so auf wie die Bot-Dateien.
- ⚠️ **Nicht** „sieht gleich aus", nicht am Quelltext, nicht stichprobenartig.

⚠️ **`data/` und `config/` werden in beiden Wegwerfbäumen angelegt**, damit der
Vergleich nicht versehentlich den T46.8-Unterschied mitmisst statt der
Zeichenketten. T46.8 hat seine eigene Probe in `shared/test_paths.py`, Probe F.

### ⭐ Die Selbstprobe: sieht der Vergleich überhaupt etwas?

**Prüfprinzip A5** — *ein Werkzeug, das nicht mehr misst, sagt es.* Der
Vergleich läuft ein zweites Mal gegen eine **absichtlich verstellte** alte
Fassung (`"data"` → `"daten_verstellt"`).

| | |
|---|---|
| gegen die echte alte Fassung | **0** Unterschiede |
| gegen die verstellte | ⭐ **9** Unterschiede |

**Findet er dort keinen Unterschied, ist der Ausgang NICHT PRÜFBAR**, nicht grün.
Ebenso, wenn der festgenagelte Commit fehlt (**B3**/**A2**).

---

## Der Kindprozess — sieben Messungen

Der Selektionslauf startet **Prozesse** (TB-40). Gemessen an **echten**
Unterprozessen, die einen Pfad auflösen — nicht an einer Behauptung über
`os.environ`.

| # | Frage | Gemessen | |
|---|---|---|---|
| 1 | Kind **ohne** Modus | Live-Bestand | Regelfall und Cron-Fall |
| 2 | Kind **mit** Modus | Snapshot | ⭐ die Umgebungsvariable wird vererbt |
| 3 | **Enkel** mit Modus | Snapshot | auch zwei Ebenen tief |
| 4 | **prozesslokaler** Modus im Eltern | ⚠️ Kind liest **still** den Live-Bestand | ⭐ **das Loch des prozesslokalen Wegs, gemessen** |
| 5 | Kind erbt **anderen** Hash | `rc=1`, `Selektionsfehler` | ⭐ der Hash im Modus macht daraus einen Abbruch |
| 6 | **übriggebliebener** Modus | eine Zeile auf `stderr` | ⭐ **D1** — der Lauf sagt es |
| 7 | **Cron-Nachbildung** (magere Umgebung) | Live-Bestand | Cron erbt die interaktive Shell nicht |

### ⚠️ Was beim Bauen schiefging — benannt statt still berichtigt

**Messung 5 stand zuerst auf „trifft nicht zu", obwohl der Resolver richtig
warf.** Der Probeprozess fing die Ausnahme selbst ab, um sie melden zu können —
und lieferte damit **immer** `rc=0`. Die Bedingung prüfte aber den
Rückgabewert.

> ⭐ **Prüfprinzip A1 im Kleinen:** ein gescheiterter Aufruf und ein leeres
> Ergebnis sehen gleich aus. Behoben mit einem zweiten Probeprozess **ohne**
> `try`, an dem „wirft" am Rückgabewert sichtbar ist.

**Dieselbe Falle ein zweites Mal, in `shared/test_paths.py`, Probe E1:** eine
Vorlage formatierte Kind- und Enkelquelltext in einem Durchgang und ersetzte
zweimal; der Enkel brach mit `TypeError` ab, lieferte **leere** Ausgabe, und die
Probe las das als *„erbt den Modus nicht"*.

> ⚠️ **Gefunden nur, weil `kindprozess.py` dasselbe kurz vorher gegenteilig
> gemessen hatte** (**C2** — zwei Messungen auf dieselbe Frage). Probe E1 sagt
> jetzt **NICHT PRÜFBAR**, wenn der Enkel nichts liefert.
