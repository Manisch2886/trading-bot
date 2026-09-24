# TB-102 — Läuft `messgroessen.py` im Selektionsmodus überhaupt? Und die Kette, die niemand benannt hat

**Sitzungstitel:** `TB-102` · **Angelegt:** 24.09.2026 vom steuernden Chat
**Grundlage:** Fable 23d/23e (Eingabestand, Nachweis im Modus) · **Vorgänger:** TB-98 (`bba6f25`)
**Aufwand:** hoch · ⛔ **Reines Messen. Nichts wird platziert, nichts eingetragen, nichts verdrahtet.**

---

## ⭐⭐ Warum dieser Auftrag anders aussieht als geplant

Der Plan sagte: Nachweisdatei nach 36.1 an ihren Platz, Modus-Lauf, `diff`
bytegleich, `registerdaten.py` auf die neue Datei, zwölf Rasterachsen nachziehen.

⚠️⚠️ **Eine Vormessung des steuernden Chats hat das gekippt.**
`messgroessen.py::haltedauern()` (Z. 200–218) liest

```
BASE_DIR/research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv
```

Diese Datei stammt aus **`auswertung.py` derselben TB-24-Messung**, also aus
**denselben neun Handelslisten**, die Register 40.6 neu erzeugen lässt. Commit
`78e2bc6`, 13.09.2026. ⛔ **Sie liegt nicht im Snapshot** (gemessen: 0 Treffer).

⭐ **Die Kette, die daraus folgt — sie steht nirgends im Register:**

```
neun Handelslisten (78e2bc6)
   └─> haltedauern_je_bot.csv (78e2bc6, nicht im Snapshot)
        └─> messgroessen.json, Gruppe `haltedauer`
             └─> faltenplan.py::purge_tage  (Z. 272: mess["haltedauer"][bot]["max_tage"])
                  └─> Purge und Embargo je Falte
                       └─> der Faltenplan, und damit die Benchmark-Tabelle
```

⇒ **`messgroessen.json` jetzt als Eingabe festzuschreiben, hiesse einen Wert
einfrieren, der sich mit 40.6 ändern muss.** Deshalb platziert dieser Auftrag
nichts.

⭐ **Was stattdessen dringlicher ist:** Fable verlangt in 23e den
Reproduzierbarkeitsnachweis **im Selektionsmodus** und veranschlagt „elf
Sekunden". ⚠️ Unter `TB30A_BASE_DIR=<snapshot>` sucht `haltedauern()` die Datei
im Snapshot — **wo sie nicht liegt**. Ob der Lauf dort überhaupt zustande kommt,
ist **nicht gemessen**. Genau das misst dieser Auftrag.

---

## ⛔ Was NICHT geschieht

| | |
|---|---|
| ⛔ | **Nichts wird nach `ergebnisse/` geschrieben.** Die Nachweisdatei bleibt, wo sie ist; `messgroessen.json` wird nicht angefasst |
| ⛔ | **`registerdaten.py` wird nicht geändert** — Sperrlistenpunkt 1 |
| ⛔ | **`messgroessen.py` wird nicht geändert.** Es ist seit TB-93 nach 36.1 abgesichert |
| ⛔ | **Keine Rasterachse nachgezogen, kein Registertext** |
| ⛔ | ⚠️ **`python3 faltenplan.py` nie direkt** — `main()` überschriebe den gesperrten `faltenplan.json` (TB-83). Nur `import` und Aufrufe im Speicher |

---

## 0. Schritt 0

Arbeitsbaum committen (dieser Auftrag, Anfrage 24d, Zeiger). `find .git -name
'*.lock'` → keine. HEAD am Eingang: **`bba6f25`**.

---

## Block A — Die Vormessung nachprüfen

⚠️ Alles unten ist **Vormessung** des steuernden Chats. Nach `A8` misst du nach;
weicht etwas ab, **gilt deine Messung**.

| | zu prüfen | Vormessung |
|---|---|---|
| **A1** | `messgroessen.py` Z. 207–209 liest `haltedauern_je_bot.csv` aus `BASE_DIR/research/tb24_haltedauern/ergebnisse/` | ja |
| **A2** | Die Datei stammt aus `auswertung.py` Z. 310 derselben TB-24-Messung, einziger Commit **`78e2bc6`** | ja |
| **A3** | Sie liegt **nicht** im Snapshot `63e4b6c8…` | 0 Treffer |
| **A4** | `faltenplan.py` Z. 272 liest `mess["haltedauer"][bot]["max_tage"]` für `purge_tage` | ja |
| **A5** | Hashes: `messgroessen.json` `2a9b9166…`, `messgroessen_2026-09-23_nachweis.json` `7f46d5f5…` | ja |
| **A6** | ⭐ **Welche Gruppen von `messgroessen.json` liest `registerdaten.py`, und wohin fliessen sie?** TB-93/TB-95 sagten: vier Gruppen gelesen, nur `volatilitaet` weicht ab, `datenbereiche` fliesst nirgends hin, der Faltenplan hängt an `haltedauer` | nachmessen, **und ergänzen**: fliesst `haltedauer` ausser über `purge_tage` noch irgendwohin? |

⭐ **A7 — die Kette vollständig ausmessen.** Über Z. 207 hinaus: Liest
`messgroessen.py` **noch weitere** Dateien, die nicht im Snapshot liegen? Nimm
den Lesehaken aus TB-92/TB-95/TB-98 (`sys.addaudithook`, Aufrufstapel) und lass
**einen** Lauf ohne Modus in den Scratchpad laufen. **Liste jede geöffnete Datei
mit ihrer Herkunft** (Snapshot / Repo / anderswo).

⚠️ *Das ist die eigentliche Frage dieses Auftrags: Wie viele nicht registrierte
Eingaben hat diese Datei wirklich? Zwei sind bekannt — die Kursdaten (23d) und
jetzt `haltedauern_je_bot.csv`. Ob es dabei bleibt, weiss niemand.*

Belege: `a_vormessung.txt`, `a7_lesequellen.txt`.

---

## Block B — ⭐⭐ Läuft es im Modus?

**B1 — Der Lauf, den 23e verlangt.** `messgroessen.py` im Selektionsmodus gegen
den Snapshot, `--ziel` in den **Scratchpad** (⛔ nicht nach `ergebnisse/`).

| Ausgang | was er bedeutet |
|---|---|
| ⭐ **rc 0 und bytegleich** zu `messgroessen_2026-09-23_nachweis.json` (`7f46d5f5…`) | Der Nachweis aus 23e ist geführt. ⚠️ Dann miss **nach**, woher `haltedauern_je_bot.csv` kam — aus dem Snapshot kann sie nicht gekommen sein |
| ⚠️ **Abbruch, Datei nicht gefunden** | Erwartet nach A3. **Das ist ein Ergebnis, kein Fehler.** Melden, mit der genauen Meldung und der Stelle |
| ⚠️⚠️ **rc 0, aber NICHT bytegleich** | Der schlimmere Fall: Der Lauf hat irgendwo etwas anderes gelesen. **Ursache ausmessen, nicht wegrechnen** |
| ⚠️⚠️⚠️ **rc 0, bytegleich, aber die Datei kam aus dem Repo** | ⭐ Der Modus hat nicht gegriffen — dieselbe Klasse wie Befund 1 aus TB-98. **Das ist der Fund, auf den es ankommt** |

⚠️ **Miss mit dem Lesehaken mit.** Ohne ihn ist „bytegleich" keine Aussage
darüber, *woher* gelesen wurde — und genau daran ist TB-98 hängengeblieben.

**B2 — Gegenprobe ohne Modus**, ebenfalls in den Scratchpad, mit Lesehaken.
`diff` gegen B1 und gegen die Nachweisdatei.

**B3 — Zweimal im selben Modus** (23e: „zweimal, bytegleich"), sofern B1 läuft.

⛔ **Nach jedem Lauf:** Hash von `messgroessen.json` und der Nachweisdatei — beide
unverändert. In `ergebnisse/` ist **nichts** neu.

Belege: `b1_modus.txt`, `b2_ohne_modus.txt`, `b3_zweimal.txt`, `b_hashes.txt`.

---

## Block C — Was die Kette bewegt, ohne etwas zu bewegen

⚠️ **Nur rechnen, nichts schreiben.** Die Frage: Wenn die neun Listen nach 40.6
neu erzeugt werden — **wie weit trägt das?**

| | |
|---|---|
| **C1** | Welche Felder von `haltedauern_je_bot.csv` gehen in `messgroessen.json` ein? (Z. 212–217: vier je Bot.) Welche davon liest irgendjemand? |
| **C2** | ⭐ `max_tage` → `purge_tage`. Und `purge_tage` → was? Miss, wo es im Faltenplan wirkt und ob es die **Faltengrenzen** verschiebt oder nur den Rand |
| **C3** | `median_balken` — TB-95 hat gemessen, dass `test_vorregistrierung.py` G8 es prüft. Wer sonst? |
| **C4** | ⭐⭐ **Die Umkehrfrage:** Gibt es einen Weg, auf dem die neun Listen den Faltenplan beeinflussen, **ausser** über die Faltenlänge (5.4) und über `purge_tage`? Such ihn, statt ihn auszuschliessen |

⛔ **Keine Zahl der Selektionsseite melden** (27.1). Gemeldet wird, **welche
Grösse wohin fliesst**, nicht ihr Wert. ⭐ Ausnahme: `purge_tage` und Faltenzahlen
sind Verfahrensseite (27.2), wie in TB-95.

Beleg: `c_kette.txt`.

---

## Block D — Abgabe

| | |
|---|---|
| **D1** | Hashes vorher/nachher. ⛔ **Keine einzige Datei ausserhalb von `docs/` darf sich geändert haben.** Sonde gegen `sperrliste_abbild_2026-09-23.json`: unverändert |
| **D2** | Ergebnisdokument `docs/ERGEBNIS_TB-102_messgroessen_im_modus.md` |
| **D3** | ⭐⭐ **Ein Abschnitt „Für Fable"**, ohne Kontext lesbar: Läuft der Nachweis aus 23e im Modus — ja, nein, oder ja-aber-aus-dem-Repo? Und: **die Kette aus Block C als Bild**, mit der Frage, ob `haltedauern_je_bot.csv` nach 23d ebenfalls eine Eingabedatei ist, die neu erzeugt werden muss. ⚠️ Sichtschutz 27.1 |
| **D4** | „In einfacher Sprache" · „Für die Folgesitzung vorbereitet" · Journalblock |

**Commits:** (1) Schritt 0 · (2) Belege und Ergebnis.

---

## ⚠️ Abbruchkriterien

1. Eine Datei ausserhalb von `docs/` ändert ihren Hash.
2. In `ergebnisse/` entsteht etwas Neues.
3. `messgroessen.json` oder die Nachweisdatei ändern sich.
4. ⭐ **B1 bricht ab** — das ist ein **Ergebnis**: Block B zu Ende melden, Block C
   trotzdem ausführen (er braucht keinen Lauf), dann abgeben.

⭐ *Dieser Auftrag kann nicht „scheitern". Er kann nur etwas finden oder nichts
finden — und beides wird aufgeschrieben.*

---

## In einfacher Sprache

Eine eingefrorene Messdatei liefert Kennzahlen, aus denen das Regelwerk Grössen
ableitet. Der Verfahrensprüfer verlangt den Nachweis, dass sie sich aus dem
eingefrorenen Datenbestand wiederherstellen lässt — auf demselben Weg, den der
Lauf am Stichtag nimmt.

Beim Vorbereiten ist aufgefallen, dass diese Datei **nicht nur Kursdaten** liest.
Ein Teil ihrer Zahlen — die Haltedauern der Bots — kommt aus einer
Auswertungsdatei, die ihrerseits aus denselben neun Handelslisten stammt, die
gerade neu erzeugt werden sollen. Und diese Auswertungsdatei liegt nicht im
eingefrorenen Bestand.

Daraus ergibt sich eine Kette über fünf Stufen, die bis in den Zeitabschnittsplan
und damit in die Vergleichstabelle reicht. Sie steht nirgends im Regelwerk.

Dieser Auftrag schreibt deshalb **nichts** fest. Er misst zwei Dinge: Ob der
verlangte Nachweislauf im geschützten Modus überhaupt zustande kommt — die
fehlende Datei spricht dagegen —, und wie weit die Kette trägt. Besonders
achtet er darauf, **woher** gelesen wird, nicht nur, ob das Ergebnis stimmt. Bei
einem anderen Programm hat sich diese Woche gezeigt, dass ein Lauf das richtige
Ergebnis liefern und trotzdem am falschen Ort gelesen haben kann.
