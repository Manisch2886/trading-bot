# Backlog-Nachtrag 19.09.2026 (h) — TB-55, der nicht gezogene Snapshot

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(g) voraus** — die Buchstabenreihe läuft weiter, das Datum ist
neu: **(a)–(g) vom 18.09., (h) vom 19.09.**

---

## Neuer Block 2n — aus TB-55 (19.09.2026)

**Einzufügen NACH Block 2m** *(aus Nachtrag (g))*.

---

### 2n — TB-55: der Snapshot, der nicht gezogen wurde

| # | Punkt |
|---|---|
| **T55.1** | ⭐⭐ **DER SNAPSHOT IST NICHT GEZOGEN — und der Grund war nicht eine Zahl, sondern der Rechner.** Der Trockenlauf hat **jeden einzelnen Sollwert getroffen**: `datenstand_hash` `d9449faf…a995f84` · 223 Kursdateien / 225 gesamt · genau `config/sp500_top150.txt` und `config/top25_symbols.txt`, **keine dritte** · 36 Befunde von 223 geprüften, **alle 36 zugelassen**, `nicht_zugelassen == []` · Rückgabewert **0** · stderr **0 Byte**. ⚠️ **Abgebrochen wurde, weil die Sitzung in der Cloud lief und der Auftrag an den Mac gerichtet ist** — dort fehlen `trading-env/` (3.9.6 statt 3.11.15) und die neun `*.db`, also ist **Schritt 0 strukturell nicht herstellbar**. ⭐ **Betreiber am 19.09. bestätigt: „Nicht ziehen, nur berichten"** |
| **T55.2** | ⭐⭐ **`63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` IST DREIMAL GERECHNET WORDEN, AUF ZWEI MASCHINEN.** **TB-49 Cloud** (Python 3.11.x): ⭐ **echter Zug** in ein Wegwerf-Verzeichnis, `GEZOGEN - 225 Datei(en), 211.0 MB, jede byteweise gegen die Quelle geprueft`, Nachprüfung `UNVERAENDERT` · **TB-49 Mac** (`trading-env/bin/python3` = **3.9.6**): Trockenlauf, rc 0 · **TB-55 Cloud** (3.11.15): Trockenlauf, rc 0. ⚠️ **Nicht** in den TB-52-Berichten — eine Behauptung im Gespräch, gegengezählt und **widerlegt** (`grep`: 4 / 2 / 3 Dateien in TB-49/TB-49mac/TB-55, **0** in beiden TB-52-Archiven) |
| **T55.3** | ⚠️ **WAS T55.2 NICHT BELEGT, ausdrücklich festgehalten.** **Nicht F1b/Q2:** die fragt nach der Reproduktion des **gezogenen** Snapshots aus dem Repo; es gibt bis heute **einen** echten Zug, und der ging in ein Wegwerf-Verzeichnis. **Nichts über den Bestand:** alle drei Läufe lasen denselben Datenstand — ⭐ *gleiche Eingabe → gleiche Ausgabe ist das Mindeste einer Hash-Funktion; ein Abweichen wäre ein Befund, ein Treffen ist keine Bestätigung.* **Belegt ist:** Unabhängigkeit von Maschine und Python-Nebenversion, und dass die Rechnung nur die Standardbibliothek braucht |
| **T55.4** | ⭐ **DER NAME STEHT VOR DEM ZUG FEST — und wird zum Abbruchkriterium.** ⚠️ **Meldet der Mac-Lauf beim Ziehen einen anderen `snapshot_hash` als `63e4b6c8…3cb2ceb2`, wird NICHT gezogen, sondern geklärt.** *Dann hat einer der beiden Rechner einen anderen Bestand — die Frage, die hinterher niemand mehr stellen kann* |
| **T55.5** | ⚠️⚠️ **DER AUFTRAG HATTE EINE LÜCKE, UND SIE IST MEINE.** `MAC_TB-55_snapshot_ziehen.md` nennt den Mac an **drei** Stellen (Kopfzeile · Interpreter · *„diese Aufgabe **ist** der Mac-Lauf"*), aber **an keiner steht: prüfe zuerst, wo du bist, und brich sonst ab.** Die Abbruchkriterien nannten ausschliesslich Zahlen. ⭐ **Die Sitzung musste den Abbruch selbst aus der allgemeinen Regel ableiten und hat zusätzlich den Betreiber gefragt** — glücklicher Ausgang, **kein belastbares Verfahren** für die eine unwiederholbare Handlung des Projekts |
| **T55.6** | ⭐⭐ **NEUE REGEL: JEDER `MAC_`-AUFTRAG BEGINNT MIT SCHRITT −1 ORTSPRÜFUNG.** Gemessen wird: `uname -s` = **`Darwin`** · ⭐ `test -x trading-env/bin/python3` *(der eigentliche Nachweis)* · `--version` = **3.9.x** · die neun `*.db` auffindbar · Arbeitsordner `~/trading-bot`, Zweig `main`. ⚠️ **Weicht eine ab: Auftrag beendet** — nicht ziehen, nicht ersatzweise trocken laufen, **nicht den Interpreter austauschen**, nicht nachfragen, ob es trotzdem ginge. ⭐ **Begründung in einem Satz:** *Der Zug ist nicht wiederholbar; der Abbruch ist es.* **Nachzutragen in ARBEITSWEISE §7c**; umgesetzt in `MAC_TB-55_snapshot_ziehen_v2.md` (**+31 Zeilen, 0 entfernt, 2 Einfügestellen**, mit `diff` gemessen) |
| **T55.7** | ⚠️⚠️ **DER REGISTERPRÜFER FÄLLT STILL AUF PAPIER ZURÜCK — Fall von A1.** Er meldet **`KEIN BEFUND`** und im Nebensatz `Quelle beleg: dokument (Trockenlauf nicht lauffaehig: ModuleNotFoundError: No module named 'pandas')`. ⭐ **Das Urteil ist nicht falsch** — auf dem Mac mit `trading-env` rechnet er wirklich —, ⚠️ **aber ein Glied der Kette ist Papier statt Messung, und das steht nicht im Urteil, sondern daneben.** **Zu tun:** entweder ein eigener Zustand nach **A2** (grün = gemessen, ein dritter Rückgabewert = *Kette unvollständig*) **oder** eine Zeile im Urteil selbst: `KEIN BEFUND (n von m Belegen aus Dokument statt Messung)`. ⚠️ **Bis dahin gilt: ein grüner Registerprüfer aus der Cloud sagt weniger als ein grüner vom Mac** |
| **T55.8** | ⚠️ **DIE HASH-RECHNUNG STEHT ZEICHENGLEICH ZWEIMAL IM REPO** — `shared/…::herkunft.py::datenstand` und `research/registernachtrag_tb41/pruefe_register.py:319`. *„Heute liefern beide dasselbe — wer eines ändert, merkt den Unterschied nicht."* ⭐ **Die Doppelung ist gewollt** (der Prüfer soll unabhängig vom geprüften Code sein), ⚠️ **aber „unabhängig" darf nicht „unbemerkt auseinanderlaufend" heissen.** **Vorschlag, billig und ausreichend:** ein Mass, das **beide Rechnungen gegen denselben Bestand** rechnet und auf Gleichheit prüft — **keine** Zusammenlegung der Funktionen |
| **T55.9** | **Die `data/snapshots`-Falle ist bewacht, nicht offen.** Bei `--ziel data/snapshots` bricht das Werkzeug ab (*„Ziel liegt innerhalb der Quelle"*); `data/` enthält heute keine Unterordner (`find` = `git ls-files` = **223**). ⭐ **Aufnehmen, nicht handeln** — der Standardwert von `--ziel` wird nicht angetastet |
| **T55.10** | ⭐ **BEANTWORTET, KEIN OFFENER PUNKT: `EINGABEN` darf eine Liste bleiben.** Der Bericht merkt an, die zwei Konfigurationsdateien stünden *„als Liste, nicht als Regel"*. ⚠️ **D5 verlangt Regeln statt Listen für AUSNAHMEN** — `EINGABEN` ist aber die **Eingabemenge**, und das Register nennt genau diese zwei Dateien. **Eine Regel („alle `.txt` unter `config/`") wäre hier das Risiko:** sie zöge mit, was künftig dort landet, und der Snapshot-Inhalt wäre nicht mehr registriert. ⭐ **Die Liste ist die stärkere Wahl** |
| **T55.11** | **Für den Mac-Lauf festgehalten:** `size-pack` **114.77 MiB**, `in-pack` **2496 Objekte** (Ausgangswert, in der Cloud-Sitzung unverändert). ⚠️ **Ohne diese Zahl wäre die TB-46-Erwartung von +0,001 % auf dem Mac nicht prüfbar.** `.gitignore` braucht **keine** Änderung: `git check-ignore -v snapshots/` und dasselbe auf eine Datei im Snapshot — **beide Rückgabewert 1**, von keinem Muster erfasst |
| **T55.12** | ⭐ **Wie der Datenstand gemessen wurde, und warum das besser ist als verlangt.** Der Auftrag verlangte „dreimal messen"; die Sitzung hat **nicht dreimal dasselbe Werkzeug** benutzt: Messung 2 **importiert `herkunft.py::datenstand` und ruft sie direkt auf** — die registrierte Funktion selbst, nicht das Werkzeug, das sie benutzt. **Dreimal `d9449faf…a995f84` bei 223.** ⚠️ **In ARBEITSWEISE §7c aufzunehmen: „dreimal messen" heisst nicht „dreimal derselbe Aufruf"** |

---

## Berichtigung — Kettenzeile 0,86

**Zu finden** (Abschnitt 3, Rang **0,86**, aus Nachtrag (g): *„TB-55 — die
Faltenschranke messen und entfernen"*).

⚠️ **Hier liegt eine Nummernkollision:** Nachtrag (g) hat **0,86** für „TB-55 =
Faltenschranke + Berichtigung 17.3" vergeben; **formuliert und ausgeführt wurde
unter TB-55 aber der Snapshot.** ⭐ **Auflösung, damit die Nummern eindeutig
bleiben:**

```
| **0,86** | ⭐⭐ **TB-55 — den Snapshot ziehen** · Cloud-Lauf 19.09.: ⚠️ **NICHT gezogen** (falscher Rechner), jeder inhaltliche Sollwert getroffen, Name `63e4b6c8…` vorhergesagt · ⭐ **Auftrag v2 mit Schritt −1 Ortsprüfung liegt bereit, unverbraucht** | ⚠️ **auf dem Mac auszuführen** |
| **0,87** | ⭐ **TB-56 — die Faltenschranke messen und entfernen** (F14/F16) · **Berichtigung von 17.3 im Register** (F17, Kategorie Berichtigung) · **die Drei-Kategorien-Regel zu Registertext 0** | zu formulieren |
```

⚠️ **Der alte Wortlaut von 0,86 bleibt darunter stehen, als ersetzt
gekennzeichnet und datiert** — nach der Drei-Kategorien-Regel (F17) ist das eine
**Berichtigung**: sie löst einen Widerspruch **innerhalb** des Backlogs auf und
trifft keine offene Entscheidung.

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K1x** | ⚠️⚠️ **Jeder `MAC_`-Auftrag beginnt mit Schritt −1 Ortsprüfung** (T55.6). ⭐ **Gegenstück für Cloud-Aufträge mitdenken**, wo der Ort bindet — dort ist die Prüfung „`trading-env/` existiert **nicht**" |
| **K1y** | **„Dreimal messen" heisst nicht „dreimal derselbe Aufruf."** Mindestens eine der Messungen rechnet **an der Quelle** — die registrierte Funktion direkt, nicht über das Werkzeug (T55.12) |
| **K1z** | ⚠️ **`docs/UMGEBUNGEN.md` ist wieder veraltet** — der Eintrag zur Zahl der Testdateien stammt aus TB-50 (**65**); TB-52 hat auf dem Mac **69** gemessen. *Die Datei veraltet schneller, als sie gepflegt wird — beim nächsten Mal mit Messdatum statt mit Zahl allein* |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte Zeilen:
   die der ersetzten Kettenzeile 0,86, sonst keine.** *Dieser Nachtrag ersetzt
   genau eine Zeile und fügt sonst nur ein.* **Weicht es ab, ist das ein
   Befund.**
2. ⚠️ **Prüfen, dass der alte Wortlaut von 0,86 als ersetzt gekennzeichnet
   darunter steht** — nicht gelöscht.
3. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.
