# Anfrage an Fable 5.1 — 23.09.2026, 16:15: Punkt 8 hat eine **dritte** Leserin, und sie ist eingefroren

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `02f2574`
**Bezug:** deine Antwort 23c, Abschnitt 4 („Vollzug von Punkt 8 — frei")

**Sichtschutz:** Codefundstellen und Zählungen — 27.2. ⛔ Keine Tabellenwerte.

⚠️⚠️ **Wir halten TB-92 an, bis du das entschieden hast.** Der Auftrag ist
geschrieben, aber mit einer Sperre am Anfang.

---

## 1. ⭐ Deine Handwerksfrage aus 23c, zuerst — die Antwort ist: **nein**

> *„Die umbenannte und neu geschriebene Kopie der alten Tabelle aus dem
> Bytevergleich — liegt sie noch irgendwo unter `ergebnisse/`?"*

**Gemessen:** `ergebnisse/` enthält **13** Dateien (vorher 12). Die einzige neue
ist `benchmark_drawdowns_2026-09-23_nach_wegA.json`. Kein weiteres JSON im ganzen
Repo wurde nach 12:00 geschrieben. ⇒ **Die Vergleichskopie liegt nirgends.** Die
Mac-Sitzung hat sie flüchtig gehalten.

## 2. ⚠️⚠️ Der Befund: eine dritte Leserin, die du nie genannt hast

**Gemessen, wer `ergebnisse/benchmark_drawdowns.json` im Laufbereich liest:**

| Leser | in 22h / 23a / 23c genannt? | Sperrliste | Schalter |
|---|---|---|---|
| `test_vorregistrierung.py::_tabellen` (Z. 82) | ✔ ja | frei | — |
| `registerbericht.py` (Z. 64) | ✔ ja | frei | — |
| ⛔⛔ **`auswertung.py::main` (Z. 590)** | ⛔ **in keiner der drei** | ⛔ **Punkte 3 und 5** | ⛔ **keiner, fest verdrahtet** |

⚠️ **Das Register weiss es.** Deine eigene Tatsachennotiz aus TB-88 (M5,
Messstand `8851f67`) nennt alle drei wörtlich:

> *„`test_vorregistrierung.py` (Funktion `_tabellen`), `auswertung.py` (`main`)
> und `registerbericht.py` lesen heute `ergebnisse/benchmark_drawdowns.json`"*

⭐ **Wir vermuten kein Versehen in der Sache, sondern eine Lücke in der
Vollzugsliste** — deine fünf Schritte in 23c nennen `registerbericht.py`, aber
`auswertung.py` kommt nicht vor.

### Warum das mehr ist als eine fehlende Zeile

Dein Schritt 1 sagt: *„`benchmark_drawdowns.json` bleibt gesperrt und
unverändert … die neu gerechnete Tabelle ist die, **die der Lauf liest**."*

⚠️⚠️ **`auswertung.py::main` IST der Lauf.** Stellen wir nur deine zwei
genannten Leser um, dann gilt:

| | liest nach dem Vollzug |
|---|---|
| Der **Test**, der grün werden soll | die **neue** Tabelle |
| Der **Bericht** | die **neue** Tabelle |
| ⛔ **Der Selektionslauf am Tag** | die **alte** — bei fünf Bots **ohne eine einzige Falte** |

⇒ ⚠️⚠️ **Der Test würde etwas anderes prüfen als das, was am Tag läuft.** Das
ist die Fehlerklasse, die 12 gerade ausschliessen soll (*„der Test ist der
Vollständigkeitsnachweis des Auswerters"*) — eine Wache, die neben dem Bewachten
steht.

## 3. Was dem entgegensteht

| | |
|---|---|
| ⛔ | `auswertung.py` ist **eingefroren** (15.8 Nr. 3), Registerzeile 40 und 1550 |
| ⛔ | Es steht auf der Sperrliste, **Punkte 3 und 5** |
| ⛔ | Es steht in `herkunft.py::EINGEFROREN` — sein Hash wird am Tag bezeugt |
| ⛔ | Es hat **keinen** `--tabellen`-Schalter; der Pfad steht fest im Quelltext |
| ⚠️ | ⭐ **Und `ergebnisse/benchmark_drawdowns.json` steht selbst in `EINGEFROREN`** (Z. 61) — der **Pfad** ist eingefroren, nicht nur die Datei |

⭐ *Der letzte Punkt ist der unangenehme: Selbst wenn `auswertung.py` einen
Schalter bekäme, wandert mit dem gelesenen Pfad ein Eintrag in `EINGEFROREN` —
und nach deiner eigenen Präzisierung aus 23c ist alles darin gesperrt.*

---

## Die Frage

| | |
|---|---|
| **(1)** | Gehört `auswertung.py` in den Vollzug von Punkt 8 — also: liest der **Lauf** nach dem Vollzug die neue Tabelle? ⭐ Wir lesen deinen Satz „die der Lauf liest" so, aber du hast die Datei nie benannt, und sie ist eingefroren |
| **(2)** | Falls ja: nach **37.3** wie `faltenplan.py`, `benchmark.py` und (neu) `messgroessen.py` — mit Freigabe, Tatsachennotiz, altem und neuem Hash? Und wandert `EINGEFROREN` von `ergebnisse/benchmark_drawdowns.json` auf den neuen Pfad, oder trägt es **beide**? |
| **(3)** | Falls nein: Wie verträgt sich ein grüner Test, der die neue Tabelle liest, mit einem Lauf, der die alte liest — angesichts von 12? ⭐ Dann wäre der Test kein Vollständigkeitsnachweis des Auswerters mehr, sondern einer eines anderen Standes |
| **(4)** | ⚠️ Und unabhängig davon: Deine **statische Sonde „Schreibziele"** aus 23c würde diese Klasse nicht finden — `auswertung.py` **schreibt** die Datei nicht, es **liest** sie. Soll die Sonde auch **Lesequellen** der drei Gruppen führen? |

⭐ *Wir neigen zu (1) mit (2) „beide in `EINGEFROREN`, bis der Tag den alten Pfad
schliesst": Der historische Stand bleibt bezeugt, der neue kommt dazu. Aber das
ist deine Entscheidung, nicht unsere — und (4) ist der eigentliche Fund: Die
Sonde, die du gerade angeordnet hast, hätte diesen Fall nicht gefunden.*

---

## 4. Was sonst aus 23c bereits umgesetzt oder beauftragt ist

| | |
|---|---|
| ⭐ | **Vollzug Punkt 8:** Auftrag TB-92 geschrieben, mit deinen fünf Schritten — ⛔ **angehalten bis zu dieser Antwort** |
| ⭐ | **`messgroessen.py`:** wird als eigener Auftrag formuliert, mit deinen Bedingungen (AST unverändert, Determinismusnachweis bytegleich, Mutationsprobe, Tatsachennotiz) |
| ⭐ | **Hochstufung 2 → 1:** als Auslegung verstanden, nicht als Fund. Deine Tatsachennotiz zu 36.5/37 kommt in den Registerauftrag |
| ⚠️ | **Sonde „Schreibziele":** vorgemerkt — ⭐ siehe Frage (4), sie sollte gleich mit der richtigen Reichweite gebaut werden |

---

## In einfacher Sprache

**Zuerst die gute Nachricht:** Die Kopie, nach der du gefragt hast, liegt
nirgends herum — es gibt genau eine neue Datei, und das ist die neu gerechnete
Tabelle.

**Der Befund ist ein anderer.** Drei Programme lesen die alte Vergleichstabelle.
Du hast in deinen Vollzugsschritten zwei davon genannt. Das dritte ist
ausgerechnet das Auswertungsprogramm — also **das Programm, das am Stichtag die
eigentliche Arbeit macht**. Es ist eingefroren und liest die Datei fest
verdrahtet, ohne die Möglichkeit, woanders hinzuschauen.

**Würde man nur die zwei genannten umstellen**, dann läse das Prüfprogramm die
neue Tabelle und das Auswertungsprogramm die alte — bei fünf von neun Bots eine
Tabelle ohne einen einzigen Zeitabschnitt. Die Prüfung würde grün, obwohl sie
etwas anderes prüft als das, was tatsächlich läuft. Genau das soll nach den
Regeln nicht passieren.

**Deshalb halten wir den Vollzug an**, obwohl er freigegeben ist. Der Auftrag
liegt fertig da und wartet auf einen Satz von dir.
