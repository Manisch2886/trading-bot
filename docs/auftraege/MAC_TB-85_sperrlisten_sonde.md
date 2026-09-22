# TB-85 — Schritt 1 von Fables Reihenfolge: das Abbild der Sperrliste und die Sonde, plus der Nullpunkt-Lauf

**Sitzungstitel:** `TB-85 Sperrlisten-Sonde — Abbild, Sonde, Nullpunkt`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**Erstellt:** 22.09.2026, 08:30 Ortszeit · **Vorgänger:** TB-84 (`03e544e`)
**Erwarteter Ausgangsstand:** `HEAD` = `origin/main` = `03e544e` oder jünger

⭐⭐ **BETREIBERFREIGABE LIEGT VOR:** 22.09.2026, 07:50 — für **Schritt 1 und 2**
von Fables Reihenfolge (36.3). ⚠️ **Dieser Auftrag ist Schritt 1 allein.**
Schritt 2 (`faltenplan.py main()` absichern) ist **TB-86** und wird erst
geschrieben, wenn dieser hier durch ist.

---

## 0. ⚠️ Das ist der erste Auftrag seit Tagen, der CODE schreibt

| ⭐ | **Erlaubt — und nur das** |
|---|---|
| ⭐ | **Neu anlegen:** das Abbild der Sperrliste (Datendatei) |
| ⭐ | **Neu anlegen:** die Sperrlisten-Sonde (`.py`, neue Datei) |
| ⭐ | **Neu anlegen:** eine Selbstprüfung der Sonde (`.py`, neue Datei) |

| ⛔ | **Verboten** |
|---|---|
| ⛔ | **Jede vorhandene `.py` ändern** — ⚠️ insbesondere `herkunft.py` (Sperrliste 11/12), `faltenplan.py` (Schritt 2, **nicht** dieser Auftrag), `auswertung.py`, `benchmark.py`, `registerdaten.py` |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — `main()` überschreibt `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) |
| ⛔ | **Eine gesperrte Datei schreiben** — die Schreibregel 36.1 gilt ab sofort auch für dich |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** (Registeränderung) — das Abbild wird **erzeugt und gemessen**, sein Eintrag ins Register ist TB-87 |

---

## 1. Schritt 0

1. **Schlüsselbund entsperren**, Kopfzeile „Claude Max".
2. **Committe, was im Arbeitsbaum liegt.** `git status --short` leer.
3. ⚠️⚠️ **Nullmessung ZUERST:** die drei Sperrlisten-Hashes messen und in
   `docs/belege/TB-85/schritt0_hashes_vorher.txt` schreiben:
   - `research/vorregistrierung/ergebnisse/faltenplan.json` → soll `0e54ac5c…`
   - `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` → soll `a163c498…`
   - `research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json` → soll `4549395f…`
   ⛔ **Weicht einer ab: ABBRUCH, melden, nichts weiter tun.**

---

## 2. Teil A — Das Abbild der Sperrliste

**Registertext:** 36.6 (Fable 22c). Die Datei trägt *„genau die Punkte des
Registerabschnitts 10 mit Pfad und Hash — nicht mehr, nicht weniger"*.

### A1 — Name und Ort

```
research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-22.json
```

⭐ **Das Datum im Namen ist Absicht:** 36.6 verlangt, dass *„jede Fortschreibung
der Sperrliste vor dem Tag ein neues Abbild unter neuem Namen erzeugt, das alte
bleibt"*.

### A2 — Was hineingehört, und wie du es ermittelst

**Je Punkt 1–14 aus Registerabschnitt 10 ein Eintrag mit:**

| Feld | Inhalt |
|---|---|
| `punkt` | die Nummer (1–14) |
| `titel` | die Überschrift des Punktes, zeichengleich aus dem Register |
| `pfade` | **Liste** der im Punkt genannten Dateipfade, repo-relativ — **leer**, wenn der Punkt keine Datei nennt |
| `hashes` | Abbildung `{pfad: sha256}`, **frisch gemessen**; leer, wenn `pfade` leer |
| `nicht_dateibezogen` | ⭐ **Freitext**, wenn der Punkt Grössen nennt, die **keine** Datei sind (Konstanten, Funktionen, Docstrings, Registerverweise) — wörtlich, was er nennt |
| `quelle` | `"Registerabschnitt 10, Punkt <n>"` |

⚠️⚠️ **Die Klassifikation ist gemessen und liegt vor:**
`docs/projektfuehrung/VORARBEIT_sperrlisten_sonde.md`. ⭐ **Du übernimmst sie
nicht — du misst sie nach** und trägst ein, was **du** findest. Weicht deine
Messung ab: eintragen, was du misst, **und melden**.

⚠️ **Zur Erinnerung aus der Vorarbeit** (nachzumessen, nicht zu glauben): Nur
die Punkte **1, 2, 5, 8** sind allein über Datei-Hashes prüfbar; **13** nennt
gar keine Datei; **7** und **9** nennen nur Konstanten; **6, 12, 14** meinen
Funktionen oder einen Docstring; **11** nennt zusätzlich den Repo-Commit.

### A3 — ⚠️ Zwei Dinge, die NICHT ins Abbild gehören

| ⛔ | |
|---|---|
| ⛔ | **`ergebnisse/benchmark_drawdowns_vt.json`** (`4549395f…`) — es ist **kein Punkt** des Abschnitts 10, sondern *„für die Sperrliste bestimmt"* (21.9/23.7, Vollzug steht aus). ⚠️ **Ob die Sonde es prüfen soll, liegt bei Fable** (Anfrage 22c); bis dahin **nicht ins Abbild**, aber in den Bericht der Sonde als eigener Abschnitt „bestimmt, nicht eingetragen" |
| ⛔ | Die Listen `EINGEFROREN` und `SPERRLISTE_DATEIEN` aus `herkunft.py` — 36.6 sagt ausdrücklich, sie werden **nicht** das Abbild |

### A4 — ⚠️ Die Schreibregel gilt für den Erzeuger des Abbilds

**36.1 (2):** Der Erzeuger schreibt **einmalig**. Existiert
`sperrliste_abbild_2026-09-22.json` bereits, **bricht er ab mit Rückgabewert 1**
und nennt Pfad und Hash der vorhandenen Datei — **er überschreibt nie, auch
nicht mit identischem Inhalt.**

⭐ **Der Erzeuger ist ein eigenes kleines Skript**
(`research/vorregistrierung/sperrliste_abbild.py` oder ein Belegskript unter
`docs/belege/TB-85/`) — **Handwerk, du entscheidest**, aber er wird mit
committet, weil 36.6 auf 33.3 verweist und 5e den erzeugenden Code registriert.

---

## 3. Teil B — Die Sonde

### B1 — Name und Ort

```
shared/sperrlistensonde.py
```

⭐ **Begründung, zum Eintragen ins Ergebnisdokument:** `shared/` ist der Ort der
gemeinsamen Werkzeuge (`snapshot.py`, `regimewache.py`). ⛔ **Nicht** in
`herkunft.py` — Fable 22c: *„`herkunft.py` scheidet als Ort aus"*, es steht
selbst auf der Sperrliste.

### B2 — ⭐⭐ Die drei Ausgänge (Registertext 36.5)

| Wert | Bedeutung |
|---:|---|
| **0** | geprüft und in Ordnung |
| **1** | geprüft und **Befund** — Abweichung, mit Nennung des Punktes |
| **2** | ⭐ **nicht prüfbar** — Eingabe fehlt, Quelle nicht lesbar, Aufruf gescheitert |

⚠️⚠️ **Registertext 36.5, wörtlich:** *„Kein Aufruf endet mit 0, ohne dass
gemessen wurde."* ⇒ Ein Punkt, den die Sonde nicht messen kann, wird **nie** als
in Ordnung geführt.

⭐ **Bauart nach `shared/snapshot.py`** — lies dessen Kopf (Z. 214–232), dort
steht die Begründung für den dritten Ausgang (Vorfall TB-45).

### B3 — Was die Sonde prüft (36.6)

| | Prüfung | Ergebnis |
|---|---|---|
| **(i)** | jeden Punkt des **Abbilds** gegen die Datei im Repo (Hash neu messen) | Abweichung → **1** |
| **(ii)** | das **Abbild gegen den Registertext** von Abschnitt 10 — Punktzahl, Titel, Pfade | Abweichung → **1** |

⚠️⚠️ **Und der Fall, der hier der wichtigste ist:**

> ⭐ **Jeder Punkt, für den der Registertext nichts Messbares hergibt** (kein
> Pfad, nur eine Konstante, nur ein Funktionsname, nur ein Registerverweis),
> wird **einzeln mit `2` gemeldet und benannt** — nicht übersprungen, nicht als
> geprüft geführt.
>
> ⚠️ **Der Gesamtrückgabewert:** `1`, wenn irgendein Punkt einen Befund hat;
> sonst `2`, wenn irgendein Punkt nicht prüfbar war; sonst `0`.
> ⛔ **Ein `1` schlägt ein `2`** — ein Befund ist wichtiger als eine Lücke.

⚠️ **Das ist unser Vorschlag an Fable** (Anfrage 22c, Abschnitt 4) und **seine
Antwort steht aus.** ⭐ **Er wird trotzdem so gebaut**, weil er ohne die Antwort
auskommt: Die Sonde sagt beim ersten Lauf selbst, wo der Registertext nichts
Messbares enthält. ⚠️ **Das gehört ausdrücklich ins Ergebnisdokument** — falls
Fable anders entscheidet, ist die Sonde neu und nicht gesperrt, also änderbar.

### B4 — Aufrufform

```
python3 shared/sperrlistensonde.py --abbild <pfad> [--json]
```

⭐ Der Bericht nennt je Punkt: Nummer, Titel, Prüfergebnis (`0`/`1`/`2`) und bei
`1` oder `2` den **Grund**. Dazu der eigene Abschnitt für
`benchmark_drawdowns_vt.json` (A3).

### B5 — Selbstprüfung

`shared/test_sperrlistensonde.py`, nach dem Muster von
`shared/test_regimewache.py`. ⭐ **Mindestens diese Fälle, jeder als
Mutationsprobe:**

| # | Fall | erwartet |
|---:|---|---|
| 1 | Abbild stimmt mit Repo und Registertext | ⭐ **0** oder **2** (wenn nicht-prüfbare Punkte dabei sind — dann **2**) |
| 2 | Eine Datei im Repo verändert (Kopie, ein Byte anders) | **1**, und der Punkt wird genannt |
| 3 | Ein Punkt fehlt im Abbild | **1** |
| 4 | Ein Punkt zu viel im Abbild | **1** |
| 5 | Abbilddatei fehlt | **2** |
| 6 | Registerdatei nicht lesbar | **2** |
| 7 | ⭐ Ein Punkt ohne Pfade | **2**, mit Nennung |

⚠️⚠️ **Alle Prüfungen laufen auf KOPIEN in einem temporären Ordner** — ⛔ **nie
gegen die echten gesperrten Dateien.**

---

## 4. Teil C — Der Nullpunkt-Lauf

**Fables Schritt 1, wörtlich:** *„Sperrlisten-Sonde schreiben und einmal laufen
lassen — Nachweis, dass heute alles stimmt (der Nullpunkt)."*

1. Sonde gegen das erzeugte Abbild laufen lassen
2. **Ausgabe vollständig** nach `docs/belege/TB-85/nullpunkt.txt`, mit
   Rückgabewert in Zeile 1
3. ⭐ **Erwartet: kein Punkt mit `1`.** Punkte mit `2` sind **erwartet und kein
   Fehler** — sie sind der gemessene Befund über den Registertext
4. ⛔ **Tritt irgendwo `1` auf: ABBRUCH und melden.** Nach 36.2 ist ein
   Sperrlistenbruch *„eine Tatsachennotiz — nie eine stille Reparatur"*

---

## 5. ⛔ Abbruchkriterien

| # | Wenn … | dann |
|---:|---|---|
| **1** | ⚠️⚠️ Einer der drei Sperrlisten-Hashes weicht ab (Schritt 0 oder am Ende) | ⛔⛔ **SOFORT ABBRUCH.** Nichts reparieren, nur melden |
| **2** | Die Sonde meldet beim Nullpunkt-Lauf irgendwo **`1`** | ⛔ ABBRUCH, melden |
| **3** | Du müsstest eine vorhandene `.py` ändern | ⛔ ABBRUCH — der Auftrag ist falsch geschnitten |
| **4** | Das Abbild existiert bereits | ⛔ Der Erzeuger bricht ab (36.1 (2)) — **melden, nicht überschreiben** |
| **5** | Eine Selbstprüfung aus B5 schlägt fehl | ⛔ Anhalten, melden; **die Sonde nicht anpassen, bis der Fall verstanden ist** |
| **6** | Register `numstat` zeigt in Spalte 2 etwas anderes als `0` | ⛔ ABBRUCH — dieser Auftrag ändert das Register **gar nicht** |

---

## 6. Schritte

| # | Tun | Nachweis |
|---:|---|---|
| **0** | Schlüsselbund, Arbeitsbaum, **drei Hashes vorher** | `schritt0_hashes_vorher.txt` |
| **1** | **Abschnitt 10 auslesen** und die 14 Punkte klassifizieren (A2) | `schritt1_klassifikation.txt` |
| **2** | **Erzeuger** schreiben (mit Einmal-Schreibsperre nach 36.1 (2)) | Commit |
| **3** | **Abbild erzeugen** und messen (`wc -c`, sha256) | `schritt3_abbild.txt` |
| **4** | **Sonde** schreiben (drei Ausgänge, B3) | Commit |
| **5** | **Selbstprüfung** schreiben und laufen lassen — **alle sieben Fälle** | `schritt5_selbstpruefung.txt` |
| **6** | ⭐ **Nullpunkt-Lauf** (Teil C) | `nullpunkt.txt` |
| **7** | **Mutationsprobe am Erzeuger:** ihn ein zweites Mal aufrufen → muss mit **1** abbrechen und den Hash nennen | `schritt7_mutationsprobe.txt` |
| **8** | **Drei Hashes nachher** | `schritt8_hashes_nachher.txt` |
| **9** | `git diff --numstat` — ⚠️ **das Register darf gar nicht vorkommen** | Abschlussbeleg |
| **10** | **`AKTUELLER_AUFTRAG.md`** — ⭐ **bereits auf TB-85 gesetzt, nur lesen** | `grep -c "TB-85"` ≥ 1 |
| **11** | **Journalblock** und `docs/auftraege/ERGEBNIS_TB-85.md` | Commit |
| **12** | **Abgabe**: Status leer, `numstat` nachgetragen | Abschlussbeleg |

---

## 7. Ins Ergebnisdokument

1. **Die Klassifikation der 14 Punkte, wie DU sie gemessen hast** — mit dem
   Vergleich zur Vorarbeit (Abweichungen ausdrücklich)
2. **Der Nullpunkt-Lauf im Wortlaut**, samt Rückgabewert
3. ⭐ **Welche Punkte `2` liefern und warum** — das ist der eigentliche Befund
   dieses Auftrags
4. **Die sieben Selbstprüfungen** mit Ergebnis
5. **Die Mutationsprobe am Erzeuger** (Schritt 7)
6. **Die drei Hashes vorher und nachher**
7. ⚠️ **Offen und benannt:** Fables Antwort auf Anfrage 22c steht aus — prüft
   die Sonde auch „für die Sperrliste bestimmte" Pfade (`_vt.json`)? Und gilt
   sein `2` auch für nicht-messbare Registerpunkte (unser Vorschlag)?
8. ⭐ **Was NICHT getan wurde:** keine vorhandene `.py` geändert, kein
   `faltenplan.py` aufgerufen, kein Registereintrag, kein Hash auf die Sperrliste

---

## In einfacher Sprache

**Das ist die erste Aufgabe seit Tagen, bei der wieder Programmcode entsteht** —
und sie baut genau das, was die gestern gemeldete Falle künftig verhindert.

Drei Dinge werden neu angelegt: **eine maschinenlesbare Liste** der geschützten
Dateien, gebildet aus dem Regelwerk; **ein Prüfprogramm**, das diese Liste gegen
die echten Dateien und gegen das Regelwerk kontrolliert; und **eine
Selbstprüfung**, die dem Prüfprogramm absichtlich Fehler unterschiebt, damit man
sieht, dass es sie findet.

Dann läuft das Prüfprogramm **ein erstes Mal** — der Nullpunkt: der Nachweis,
dass heute alles stimmt.

⭐ **Das Interessanteste dabei wird sein, wie oft es „nicht prüfbar" sagt.** Wir
haben gemessen, dass das Regelwerk nur bei vier von vierzehn Punkten schlicht
eine Datei nennt; bei den übrigen nennt es Zahlenwerte, einzelne Funktionen oder
verweist auf sich selbst. Das Prüfprogramm soll diese Punkte **beim Namen
nennen**, statt sie stillschweigend zu überspringen oder als geprüft
auszugeben — genau das war der Fehler, der dieses ganze Thema ausgelöst hat.

⚠️ **Nichts Vorhandenes wird angefasst.** Kein bestehendes Programm wird
geändert, das Regelwerk gar nicht. Und die Prüfsummen der drei geschützten
Dateien werden vorher **und** nachher gemessen.
