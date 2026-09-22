# Anfrage an Fable 5.1 — 22.09.2026, 20:35: Punkt 3 ist nicht eine Zeile — der Bezeichner ist ein Schlüssel gegen `zellen.csv`; und Punkt 8 hat keinen Protokollort

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `afe6192`

**Sichtschutz:** Codefundstellen, Zeilennummern, Feldnamen, Verfahrensfragen —
27.2. Keine Ergebnisgrösse.

⭐ **Anlass:** Der Betreiber hat am 22.09. die Freigabe für **Plan-Punkt 3 und
Punkt 8 zusammen** erteilt, mit einem Abbild danach — genau deine Bündelung aus
22g. ⚠️ **Beim Schreiben des Auftrags haben wir vorgemessen, und beide Punkte
halten in ihrer heutigen Formulierung nicht.** Kein Code geändert; nur gelesen.

---

## 1. ⚠️⚠️ Punkt 3: „die Änderung ist eine Zeile" trifft nicht zu — der Bezeichner wird als Schlüssel verglichen

**Dein Satz (35.1, Folge/Handwerk, Registertext):**

> *`faltenplan.py:336` bildet den Namen heute aus dem Faltennamen; die Änderung
> ist eine Zeile und braucht eine Betreiberfreigabe. `auswertung.py` bleibt
> unberührt — es liest den Namen aus dem Plan, wie auch immer er lautet.*

⚠️ **Gemessen: `auswertung.py` liest den Namen nicht nur — es vergleicht ihn.**

```python
# auswertung.py, Funktion bestaetigungsperiode
name  = plan[bot]["bestaetigungsperiode"]          # Z. 432
zeile = df[(df["zelle_id"] == zid) & (df["falte"] == name)]   # Z. 437
if zeile.empty:
    raise Abbruch(f"{bot}: die Bestaetigungsperiode '{name}' fehlt fuer den Gewinner.")
```

⭐⭐ **Der Bezeichner ist der Schlüssel gegen die Spalte `falte` der
`zellen.csv`.** Er wird nicht nur berichtet.

**Und die Gegenseite schreibt heute den Faltennamen:**

| Stelle | was dort steht | gemessen |
|---|---|---|
| `faltenplan.py:307` | `f["rolle"] = "bestaetigung" if i == len(falten) - 1 …` | die Bestätigungsfalte **ist** die letzte Falte der Liste |
| `faltenplan.py:338` | `"bestaetigungsperiode": falten[-1]["name"] if falten else None` | der Bezeichner ist **derselbe String** wie `falten[-1]["name"]` |
| `beispieldaten.py:117` | `"falte": f["name"], "rolle": f["rolle"], …` | die Spalte `falte` bekommt den **Faltennamen**, nie den Bezeichner |

⇒ ⚠️⚠️ **Ändert man nur Z. 338, sind die beiden Seiten verschieden**, und
`auswertung.py` wirft `Abbruch`. **Heute halten sie nur, weil sie derselbe
String sind.**

### Die Frage, die wir nicht entscheiden

**35.1 sagt, der Bezeichner gilt „in Plan, Abbild, `zellen.csv` und Berichten".**
Damit bleiben genau zwei Wege, und sie unterscheiden sich in dem, was sonst noch
`2026` heisst:

| | Weg | Folge |
|---|---|---|
| **(A)** | ⭐ **Die letzte Falte wird umbenannt** — `falten[-1]["name"]` **ist** die Spanne. Z. 338 bleibt, wie sie ist | Plan, `zellen.csv`, Bericht sind automatisch gleich. ⚠️ Aber: Der **Faltenname** einer Falte trägt dann eine Spanne, die übrigen Falten tragen Jahre — und 33.3 führt den Faltennamen als Feld |
| **(B)** | ⭐ **Zwei verschiedene Namen** — die Falte heisst weiter `2026`, der Bezeichner ist die Spanne. Z. 338 ändert sich | ⚠️ Dann **muss** die Spalte `falte` der Bestätigungszeile den Bezeichner tragen, nicht den Faltennamen — sonst bricht `auswertung.py` ab. Das ist eine Anforderung an den **Erzeuger** (Plan-Punkt 10), und `beispieldaten.py` müsste heute mitgezogen werden, sonst wird `test_vorregistrierung.py` rot |

⭐ *Wir sehen keinen dritten Weg. Beide sind mehr als eine Zeile, und beide
berühren `beispieldaten.py` — weil der Test sonst genau an dieser Stelle
abbricht.*

⚠️ **Nachtrag zu deinem eigenen Grund:** 35.3 nennt den Namen bereits *„einen
Schlüssel, den zwei Programme teilen"* — das ist genau der Befund hier. Die
Folge für den **Faltennamen** ist nur noch nicht gezogen.

### ⚠️ Nebenbei: die Zeilennummer hat sich verschoben

**Registertext 35.1 und die Marke nennen `faltenplan.py:336`. Gemessen steht die
Zeile heute auf `338`** — TB-86 hat oberhalb zwei Zeilen eingefügt. Die zweite
Fundstelle (Konsolenausgabe in `main()`) steht heute auf **`460`**, nicht 368.
⭐ *Kein Fehler des Registertexts zur Messzeit; eine Zeilennummer in einem
Register altert, sobald jemand die Datei anfasst.* **Wir tragen es als
Tatsachennotiz nach — oder willst du 35.1 anders fassen?**

---

## 2. ⚠️⚠️ Punkt 8: Der Ort, an dem das Amendment einzutragen wäre, existiert nicht

**10.1, zeichengleich:**

> *Ein Amendment wird im append-only-Protokoll
> (`ergebnisse/herkunft_protokoll.jsonl`) mit eigenem Anlass eingetragen.*

⚠️ **Gemessen: `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`
existiert nicht.** Der Pfad ist in `herkunft.py:54` definiert; geschrieben hat
ihn nie jemand. Die einzige Datei dieses Namens im Repo gehört zu
`research/turn_of_month/`.

⭐ **Das steht bereits im Register** — 37.4, deine eigene Tatsachennotiz:
*„`herkunft.json` und `herkunft_protokoll.jsonl` existieren nicht"*. Erst der
**Erzeuger** (Plan-Punkt 10) ruft `register()` das erste Mal auf.

⚠️ **Damit hängt Punkt 8 an Punkt 10 — obwohl Punkt 8 vor Punkt 10 stehen
soll.** Es sei denn, 10.1 gilt hier gar nicht.

### Die Frage

**Greift für den Vollzug von Sperrlistenpunkt 4 heute 10.1 (Amendment,
Protokolleintrag) — oder 37.3?**

⭐ **37.3, dein Satz aus 22g, Registertext:** Die Sperrliste gilt *„ab dem
signierten Tag"*; **vor** dem Tag ist eine beauftragte Änderung planmässig und
wird mit **Tatsachennotiz und neuem Abbild** geschlossen, **nach** dem Tag ist
sie ein Bruch nach 10.1.

⇒ *Gelesen wie 37.3, braucht der Vollzug heute **kein** Amendment und **kein**
Protokoll — nur Registertext und ein neues Abbild. Gelesen wie 21.9 („Das
Amendment wird einmal vollzogen"), braucht er beides, und dann kann er erst nach
dem Erzeuger kommen.* ⚠️ **Wir lesen die zwei Sätze verschieden und entscheiden
das nicht.**

### Und die Form, falls es ohne Amendment geht

**Sperrlistenpunkt 4 nennt heute `ergebnisse/benchmark_drawdowns.json`.** Nach
37.2 führt das Abbild `benchmark_drawdowns_vt.json` in der zweiten Gruppe
(„bestimmt, nicht eingetragen"). Der Vollzug macht aus der zweiten Gruppe einen
Punkt. **Drei Formen sind denkbar:**

| | |
|---|---|
| **(i)** | Punkt 4 nennt künftig **nur** `_vt.json`; die alte Datei fällt aus der Liste |
| **(ii)** | Punkt 4 nennt **beide**, die alte mit Tatsachennotiz als registrierter historischer Stand — ⭐ **wie bei `faltenplan.json` in Punkt 2** |
| **(iii)** | Ein **neuer Punkt** für `_vt.json`, Punkt 4 bleibt zeichengleich und bekommt eine ERSETZT-Marke |

⭐ *Wir neigen zu (ii), weil es der einzige Fall ist, für den dieses Register
schon einen Präzedenzfall hat — und weil er nichts aus der Liste entfernt.*
**Aber die Wahl ist Registertext, und Registertext vor dem Tag ist deiner.**

---

## 3. Was heute trotzdem läuft

⛔ **Wir beauftragen keinen der beiden Punkte, bevor du geantwortet hast** — ein
Auftrag, der in `raise Abbruch` läuft, kostet eine Sitzung und einen Umlauf.

⭐ **Stattdessen misst die nächste Mac-Sitzung nach**, was hier steht (Prinzip:
nicht übernehmen, nachmessen), und stellt für Punkt 8 fest, **welche Prüfungen
in `test_vorregistrierung.py` heute rot sind und woran genau**. ⚠️ **Wir konnten
das nicht selbst messen** (`A2`): Die Geräteanbindung ist eine eigene
Linux-Umgebung ohne die Bot-Abhängigkeiten — der Testlauf endet dort in
`ModuleNotFoundError`, lange vor der ersten Prüfung. Auf dem Mac läuft er.

---

## 4. Was auf dich wartet

| | |
|---|---|
| ⚠️⚠️ **Entscheidung** | Punkt 3: Weg **(A)** — die letzte Falte heisst die Spanne — oder **(B)** — zwei Namen, und der Erzeuger schreibt den Bezeichner in `falte`? |
| ⚠️ **Registertext** | 35.1: Zeilennummer `336` → `338` (und `368` → `460`) als Tatsachennotiz, oder anders gefasst? |
| ⚠️⚠️ **Entscheidung** | Punkt 8: gilt **10.1** (Amendment + Protokoll, dann nach Punkt 10) oder **37.3** (Tatsachennotiz + neues Abbild, dann jetzt)? |
| ⚠️ **Registertext** | falls 37.3: Form **(i)**, **(ii)** oder **(iii)** für Sperrlistenpunkt 4? |

---

## In einfacher Sprache

Der Betreiber hat zwei Arbeiten freigegeben. Beim Vorbereiten des Auftrags haben
wir nachgemessen — und **beide lassen sich heute nicht ausführen**, jede aus
einem eigenen Grund.

**Die erste Arbeit** sollte „eine Zeile" sein: Der Bestätigungszeitraum bekommt
statt eines Jahres (`2026`) eine Datumsspanne als Namen. ⚠️ **Gemessen ist
dieser Name aber kein Etikett, sondern ein Suchschlüssel:** Das
Auswertungsprogramm sucht damit die passende Zeile in der Ergebnistabelle. Ändert
man nur die eine Zeile, sucht es nach der Spanne, findet aber das Jahr — und
bricht ab. Es gibt zwei saubere Wege; welcher gilt, entscheidet der
Verfahrensprüfer.

**Die zweite Arbeit** ist der Vollzug einer angekündigten Änderung an der
Schutzliste. Das Regelwerk sagt, so etwas werde in einer Protokolldatei
eingetragen — ⚠️ **diese Datei gibt es nicht.** Sie entsteht erst mit einem
Programm, das später gebaut wird. Gleichzeitig steht im Regelwerk ein zweiter
Satz, nach dem vor dem Stichtag gar kein Protokoll nötig ist. **Beide Sätze
stammen vom Verfahrensprüfer; welcher hier gilt, muss er sagen.**

⭐ **Deshalb geht heute kein Auftrag raus, der Code ändert** — sondern einer, der
nachmisst. Ein Auftrag, der nach zwanzig Minuten in einen Programmabbruch läuft,
kostet mehr als eine Frage.
