# Journal-Nachtrag 19.09.2026 (c) — TB-55

**Anzufügen am Ende von `docs/projektfuehrung/JOURNAL.md`.** Nichts wird
umgeschrieben.

> ⚠️ **Zum Blockbuchstaben:** Der letzte eingearbeitete Block stammt aus
> Nachtrag (b) — nach der damaligen Messung **BF**. ⚠️ **Vor dem Einfügen
> messen, welcher Buchstabe wirklich der letzte ist** — genau hier hat der
> Betreuer am 18.09. falsch geraten (AX statt AZ), und TB-50 musste fünf Blöcke
> verschieben.

---

## Block ⟨nächster⟩ — TB-55: die Sitzung, deren Ergebnis ein Nichthandeln ist

**19.09.2026. Cloud-Sitzung, Basis `main` = `origin/main` = `7e48e1f`.
Nichts committet ausser dem Ergebnisdokument.**

⭐ **Dies ist die erste Sitzung dieses Projekts, deren Ergebnis darin besteht,
dass sie die beauftragte Handlung nicht ausgeführt hat.**

---

### Was gemessen wurde, und es war alles in Ordnung

| | |
|---|---|
| `datenstand_hash` | `d9449faf…a995f84` · **223** Kursdateien — ⭐ **dreimal gemessen, dreimal identisch** |
| Dateien gesamt | **225** — genau `config/sp500_top150.txt` und `config/top25_symbols.txt`, ⚠️ **keine dritte** |
| Teilkerzen | **36** Befunde von **223** geprüften Dateien |
| davon zugelassen | ⭐ **36**, Herkunft *Abschnitt 17.3* · Arten `{'rand_erste': 36}` · Urteile `{'abgeleitete_teilkerze': 36}` |
| `nicht_zugelassen` | ⭐ **`[]` — leer** |
| Rückgabewert / stderr | **0** / **0 Byte** |

⭐ **Damit ist die Ausnahme aus 17.3 vollständig gedeckt:** kein Befund wäre
ohne sie durchgerutscht, und keiner ist von ihr nicht gedeckt.

⭐ **Und Messung 2 rechnet an der Quelle:** `herkunft.py::datenstand('data')`
importiert und direkt aufgerufen — nicht dreimal dasselbe Werkzeug.

---

### Warum trotzdem nicht gezogen wurde

**Nicht eine der Abweichungen betrifft eine Zahl. Alle betreffen die
Umgebung.**

| | Soll (Auftrag) | Tatsächlich |
|---|---|---|
| Interpreter | `trading-env/bin/python3` (**3.9.6** auf dem Mac) | `/usr/local/bin/python3`, **3.11.15** — `trading-env/` existiert hier nicht |
| Schritt 0 | neun `*.db` quersummen **und kopieren** | ⚠️ **keine einzige vorhanden** (gitignoriert, nur auf dem Mac) — die Sicherung ist **strukturell nicht herstellbar** |
| Zweig | `main`, kein eigener Zweig | Sitzungsmandat: eigener Zweig, Push auf `main` untersagt |
| Ort | *„diese Aufgabe **ist** der Mac-Lauf"* | **kein Mac-Lauf** |

> ⭐ **Der Satz, auf den es ankam, und er stammt aus dem Bericht:** *„Daraus
> folgt: ein Zug auf dem Mac wird sehr wahrscheinlich denselben `snapshot_hash`
> ergeben. Es folgt aber **nicht**, dass dieser Lauf ihn ziehen durfte."*

⭐ **Die Sitzung hat die Gegenargumente selbst aufgeschrieben**, statt sie zu
verschweigen — Arbeitsbaum sauber, alle 225 Dateien versioniert,
`.gitattributes` nicht vorhanden, Rechnung nur mit Standardbibliothek. **Und
hat trotzdem nicht gezogen.**

**Der Betreiber hat auf Rückfrage bestätigt:** *„Nicht ziehen, nur
berichten."*

---

### ⭐⭐ Der Gewinn, der nicht bestellt war

```
63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
```

**Dieselbe Zahl, dreimal gerechnet, auf zwei Maschinen:**

| Lauf | Maschine | Interpreter | Art |
|---|---|---|---|
| **TB-49**, 18.09. | Cloud | 3.11.x | ⭐ **echter Zug**: `GEZOGEN - 225 Datei(en), 211.0 MB, jede byteweise gegen die Quelle geprueft`, Nachprüfung `UNVERAENDERT` |
| **TB-49**, 18.09. | MacBook | **3.9.6** | Trockenlauf, rc 0 |
| **TB-55**, 19.09. | Cloud | 3.11.15 | Trockenlauf, rc 0 |

⚠️ **Was das nicht ist:** nicht F1b/Q2 — die fragt nach der Reproduktion des
**gezogenen** Snapshots aus dem Repo, und es gibt bis heute **einen** echten
Zug, in ein Wegwerf-Verzeichnis. ⚠️ **Und nichts über den Bestand:** alle drei
lasen denselben. *Gleiche Eingabe → gleiche Ausgabe ist das Mindeste einer
Hash-Funktion.*

⭐ **Was es ist:** Der Name ist **unabhängig von Maschine und
Python-Nebenversion** — und er steht **vor** dem Zug fest. ⚠️ **Meldet der Mac
etwas anderes, wird nicht gezogen, sondern geklärt.**

---

### ⚠️⚠️ Der Befund über die Projektführung

**Der Auftrag nennt den Mac an drei Stellen — und macht den Ort an keiner zum
Abbruchkriterium.** Die Abbruchkriterien nannten ausschliesslich Zahlen.

⭐ **Die Sitzung hat den Abbruch selbst abgeleitet und zusätzlich gefragt.**
⚠️ **Bei der einen unwiederholbaren Handlung dieses Projekts darf die
Absicherung nicht am Urteil der Sitzung und an der Anwesenheit des Betreibers
hängen.**

⇒ ⭐ **Schritt −1 Ortsprüfung**, ab sofort in jedem `MAC_`-Auftrag:
`uname -s` = `Darwin` · `test -x trading-env/bin/python3` · Version 3.9.x ·
neun `*.db` auffindbar · `~/trading-bot` auf `main`. ⚠️ **Weicht eine ab:
Auftrag beendet** — nicht ziehen, nicht ersatzweise trocken laufen, nicht den
Interpreter austauschen.

> ⭐ **Der Satz, der die Regel trägt:** *Der Zug ist nicht wiederholbar; der
> Abbruch ist es.*

**`MAC_TB-55_snapshot_ziehen_v2.md`:** **+31 Zeilen, 0 entfernt, 2
Einfügestellen** — mit `diff` gemessen, nicht geschätzt.

---

### ⚠️ Zwei Berichtigungen an eigenen Aussagen

| | |
|---|---|
| **1** | Ich hatte behauptet, `63e4b6c8…` sei **auch in den TB-52-Berichten** aufgetaucht. **Gegengezählt: 0 Treffer in beiden TB-52-Archiven.** Er kommt aus TB-49 (Cloud **und** Mac) und TB-55. *Der Beleg wird dadurch nicht schwächer, aber die Aussage war falsch* |
| **2** | ⚠️ **Nummernkollision im Backlog:** Nachtrag (g) hat Rang **0,86** für „TB-55 = Faltenschranke + Berichtigung 17.3" vergeben; **formuliert und ausgeführt wurde unter TB-55 der Snapshot.** Aufgelöst in Nachtrag (h): **0,86 = Snapshot**, **0,87 = TB-56 Faltenschranke**. Nach F17 eine **Berichtigung** — sie löst einen Widerspruch innerhalb des Backlogs auf |

---

### ⚠️ Was der Registerprüfer nicht gesagt hat

Er meldet **`KEIN BEFUND`** — und im Nebensatz:
`Quelle beleg: dokument (Trockenlauf nicht lauffaehig: No module named
'pandas')`.

⚠️⚠️ **Fall von A1: ein fehlgeschlagener Aufruf und ein leeres Ergebnis sehen
gleich aus.** Das Urteil ist nicht falsch — auf dem Mac rechnet er wirklich —,
**aber ein Glied der Kette ist Papier statt Messung, und das steht nicht im
Urteil, sondern daneben.** ⇒ **T55.7.**

---

### Der Stand nach dieser Sitzung

| | |
|---|---|
| `data/` | ⭐ **unberührt** — `git status --porcelain -- data` leer, dreimal derselbe Hash |
| `snapshots/` | **existiert nicht** — weder dort noch unter `data/snapshots/` |
| `.gitignore` | **nicht geändert** — `git check-ignore` Rückgabewert **1**, von keinem Muster erfasst |
| Sperrliste, `shared/snapshot.py`, `shared/paths.py` | **unberührt** |
| Register | **kein Text geändert** |
| `size-pack` | **114.77 MiB** · `in-pack` **2496** — ⭐ Ausgangswert für die Zuwachsmessung auf dem Mac |
| Auftrag | ⭐ **unverbraucht**, jetzt als v2 mit Ortsprüfung |

---

### In einfacher Sprache

**Die eingefrorene Kopie der Kursdaten wurde nicht angelegt — und das war
richtig.** Alle inhaltlichen Prüfungen waren in Ordnung, jede einzelne. Aber
der Lauf fand auf dem falschen Rechner statt: In der Cloud fehlen das
vorgeschriebene Python und die neun Datenbanken, die vorher gesichert werden
sollen.

**Der Fehler lag in der Aufgabenstellung.** Sie sagte dreimal, dass sie für den
Mac ist, aber nie: *prüfe das zuerst und höre sonst auf.* Ab jetzt steht das als
erster Schritt in jedem Mac-Auftrag.

**Und es kam etwas heraus, das nicht bestellt war:** Der Name, den die Kopie
tragen wird, ist inzwischen auf zwei verschiedenen Rechnern mit zwei
verschiedenen Python-Versionen gerechnet worden und dreimal gleich
herausgekommen. ⚠️ **Nennt der Mac sie anders, wird nicht gezogen, sondern
nachgeforscht.**
