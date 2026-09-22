# TB-88 — Nachmessung vor Punkt 3 und Punkt 8: ist der Bezeichner ein Schlüssel, und was genau ist rot?

**Sitzungstitel:** `TB-88`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD beim Schreiben:** `afe6192`
**Vorgänger:** TB-87 (`afe6192`), TB-86 (`ee4e65c`), TB-85 (`755b3c4`)

⛔⛔ **DIESER AUFTRAG ÄNDERT KEINE EINZIGE PROGRAMMDATEI.** Kein `.py` wird
geschrieben, kein Abbild erzeugt, keine Registerzeile eingetragen, kein Hash
bewegt. **Er misst.** Wer an einer Stelle das Gefühl hat, „das könnte man gleich
mitmachen": nicht mitmachen, sondern ins Ergebnisdokument schreiben.

---

## 0. Der Anlass, in einem Satz

Der Betreiber hat Plan-Punkt 3 (Bezeichner der Bestätigungsperiode) und Punkt 8
(Vollzug `benchmark_drawdowns_vt.json`) **freigegeben** — und die Vormessung des
steuernden Chats hat ergeben, dass beide in ihrer heutigen Formulierung **nicht
ausführbar** sind. ⭐ **Dieser Auftrag prüft die Vormessung nach**, damit Fables
Entscheidung auf gemessenen und nicht auf übernommenen Zahlen steht.

⚠️ **Du übernimmst die Zahlen unten nicht — du misst sie nach.** Weicht etwas
ab, gilt deine Messung, und die Abweichung kommt ausdrücklich ins
Ergebnisdokument. *Die Vormessung ist eine Behauptung, bis sie jemand
gegengeprüft hat (`A8`).*

---

## 1. Schritt 0 — der Arbeitsbaum

⚠️ **Im Arbeitsbaum liegen drei Dateien, die nicht von dir stammen. Sie sind zu
committen, nicht zu entfernen:**

| Datei | was sie ist |
|---|---|
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22f_kosten_gemessen.md` | Anfrage an Fable, abgelegt 22.09. 20:10 |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22h_bezeichner_ist_schluessel.md` | Anfrage an Fable, die diesen Auftrag begründet |
| `docs/auftraege/MAC_TB-88_messung_punkt3_punkt8.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` (geändert, nicht neu) | die Tabelle wurde von TB-87 auf TB-88 umgestellt |

```
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22f_kosten_gemessen.md \
        docs/projektfuehrung/FABLE_ANFRAGE_2026-09-22h_bezeichner_ist_schluessel.md \
        docs/auftraege/MAC_TB-88_messung_punkt3_punkt8.md \
        docs/auftraege/AKTUELLER_AUFTRAG.md
git commit -m "Doku: Anfragen 22f und 22h an Fable, Auftrag TB-88, Zeiger umgestellt"
```

⭐ Liegt eine davon schon im `HEAD`, ist das in Ordnung — dann committe nur, was
übrig ist. **Danach `git status --porcelain` leer.**

---

## 2. M1 ⭐⭐ — Ist der Bezeichner ein Schlüssel?

**Die Behauptung der Vormessung:** `faltenplan.py:338` liefert den Bezeichner
der Bestätigungsperiode; `auswertung.py` vergleicht ihn gegen die Spalte `falte`
der `zellen.csv`; `beispieldaten.py` schreibt in diese Spalte den **Faltennamen**.
Heute halten beide Seiten nur, weil es **derselbe String** ist.

**Zu messen, jede Stelle mit Zeilennummer und Zitat:**

| | Datei | was zu belegen ist |
|---|---|---|
| **(a)** | `research/vorregistrierung/faltenplan.py` | die Zeile, die `"bestaetigungsperiode"` setzt — **Zeilennummer** und Ausdruck |
| **(b)** | `research/vorregistrierung/faltenplan.py` | die Zeile, die `rolle = "bestaetigung"` vergibt — ist die Bestätigungsfalte **die letzte** der Liste `falten`? |
| **(c)** | `research/vorregistrierung/auswertung.py` | die Funktion `bestaetigungsperiode`: **wird der Name verglichen oder nur berichtet?** Beide Zeilen zitieren (Zuweisung und Filter) samt der `Abbruch`-Zeile |
| **(d)** | `research/vorregistrierung/beispieldaten.py` | womit die Spalte `falte` befüllt wird — Faltenname oder Bezeichner? |
| **(e)** | das ganze Repo ohne `trading-env/` | **jede** Fundstelle von `bestaetigungsperiode` in `.py`, mit Datei und Zeile. Gibt es eine weitere Stelle, die den Wert vergleicht statt ihn nur auszugeben? |

---

## 3. M2 ⭐⭐ — Die Probe, ohne eine Datei anzufassen

⛔ **`faltenplan.py` wird NICHT geändert** — sie ist Sperrlistenpunkt 2.

⭐ **Stattdessen: der Plan wird im Speicher verändert.** Ein kleines Skript unter
`docs/belege/TB-88/` (dort darf geschrieben werden):

```python
# m2_bezeichner_probe.py  - Schema, an die Modulnamen anpassen
plan = fp.faltenplan(mess)
plan[BOT]["bestaetigungsperiode"] = "2026-01-01/2026-09-01"   # nur im Speicher
# ... Beispieldaten mit dem UNVERAENDERTEN Plan erzeugen (Spalte `falte`
#     traegt weiter den Faltennamen) und aw.ein_bot mit dem GEAENDERTEN Plan
#     aufrufen - genau die Lage nach einer Aenderung von Z. 338 allein.
```

**Zu belegen:** Kommt `Abbruch` — mit welchem Wortlaut? Oder läuft es durch?

⭐ *Das ist die Mutationsprobe in ihrer billigsten Form: Sie zeigt die Wirkung
der Änderung, ohne die Änderung zu machen.* ⚠️ **Läuft es durch, ist die
Vormessung falsch** — dann bitte ausdrücklich so ins Ergebnisdokument, mit dem
Grund.

---

## 4. M3 — Die Zeilennummern gegen den Registertext

Registertext 35.1 und die Marke darunter nennen `faltenplan.py:336`
(Erzeugung) und `:368` (Konsolenausgabe in `main()`).

**Zu messen:** Auf welchen Zeilen stehen die beiden Stellen **heute**? Seit
welchem Commit weichen sie ab — `git log -L` oder `git blame` auf die Zeile.
⭐ *Vermutung der Vormessung: TB-86 (`ee4e65c`) hat oberhalb eingefügt. Vermutung,
nicht Messung.*

---

## 5. M4 ⭐⭐ — Was genau ist rot?

⚠️ **`test_vorregistrierung.py` wird seit 21.9 als „rot — offen durch eigene
Änderung, blockierend für den Tag" geführt. Nirgends steht, WELCHE Prüfungen.**

```
cd research/vorregistrierung && python3 test_vorregistrierung.py
```

**Zu belegen:**

| | |
|---|---|
| **(a)** | die **vollständige** Liste der gescheiterten Prüfungen, mit ihren Kennungen (`A1`, `B3`, …) und der Meldung |
| **(b)** | die Zahl bestanden / gescheitert und der Rückgabewert |
| **(c)** | ⭐ **je gescheiterter Prüfung ein Satz: hängt sie am Vollzug von Punkt 8 — oder an etwas anderem?** *Das ist die eigentliche Frage: „rot" ist keine Diagnose* |
| **(d)** | läuft der Test **gar nicht** (Importfehler, fehlendes Modul), dann ist das das Ergebnis — mit der Meldung, nicht mit einer Vermutung (`A2`) |

⚠️ **Hinweis:** Über die Geräteanbindung ist der Test **nicht** lauffähig
(eigene Linux-Umgebung, `ModuleNotFoundError: binance`, gemessen 22.09.). Auf dem
Mac mit `trading-env` sollte er laufen. **Braucht er das venv, aktiviere es und
schreib in den Beleg, dass du es getan hast.**

---

## 6. M5 — Was der Vollzug von Punkt 8 berührt

| | zu messen |
|---|---|
| **(a)** | `registerbericht.py`: die Zeile, die `symbole_point_in_time` liest — **Zeilennummer** (23.5 nennt 178) und die Datei, aus der sie liest |
| **(b)** | Trägt `ergebnisse/benchmark_drawdowns_vt.json` den Schlüssel `symbole_handelbar_in_falte` — und trägt sie ihn **statt** oder **neben** dem alten? Je Bot, je Falte stichprobenweise |
| **(c)** | `status` je Bot in `_vt.json`: neunmal `endgueltig`? (23.5 behauptet es) |
| **(d)** | **Wer sonst noch** `benchmark_drawdowns.json` liest — alle `.py` ohne `trading-env/`, mit Zeile |
| **(e)** | Existiert `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`? Und `herkunft.json`? **`test -f`, nicht öffnen.** Wo ist der Pfad definiert? |

---

## 7. M6 — Die drei Hashes, vorher und nachher

**Vor dem ersten und nach dem letzten Schritt** je `sha256` von:

```
research/vorregistrierung/ergebnisse/benchmark_drawdowns.json
research/vorregistrierung/ergebnisse/faltenplan.json
research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json
```

⭐ **Erwartung: alle drei beide Male gleich.** Dieser Auftrag bewegt nichts.
⛔ **Weicht einer ab: ABBRUCH und Meldung, keine Rückfrage.**

---

## 8. ⛔ Abbruchkriterien

| | |
|---|---|
| ⛔ | Eine der drei Hashes ändert sich |
| ⛔ | Eine Programmdatei ausserhalb von `docs/belege/TB-88/` ist am Ende geändert |
| ⛔ | `python3 faltenplan.py` wird aufgerufen (auch nicht mit `--ziel`) |
| ⛔ | Eine Datei in `ergebnisse/` entsteht oder ändert sich |

⭐ **Abbruchkriterium heisst ABBRUCH und Meldung — nie Rückfrage.**

---

## 9. Ins Ergebnisdokument

`docs/belege/TB-88/ERGEBNIS_TB-88.md`, dazu die Messdateien `m1_…`–`m6_…`.

**Es muss beantworten:**

1. ⭐⭐ **Ist der Bezeichner ein Schlüssel — ja oder nein?** Mit dem Zitat der
   Vergleichszeile und dem Ergebnis der Probe aus M2
2. ⭐ **Welche Prüfungen sind rot, und woran hängt jede?**
3. ⭐ Welche Zeilennummern gelten heute, und seit wann weichen sie ab
4. ⭐ Was der Vollzug von Punkt 8 berührt — und ob der Protokollort existiert
5. ⚠️ **Jede Abweichung von der Vormessung ausdrücklich**, mit „Vormessung sagt
   X, gemessen ist Y"

**Danach Commit und Push.** Ein Journalblock nach der üblichen Form.

---

## In einfacher Sprache

Der Betreiber hat zwei Arbeiten freigegeben — aber beim Vorbereiten kam heraus,
dass beide so nicht gehen. **Dieser Auftrag ändert deshalb nichts, er misst
nach.**

Die wichtigste Messung: Der Name des Bestätigungszeitraums soll sich ändern. Wir
vermuten, dass dieser Name kein Etikett ist, sondern ein **Suchschlüssel** — und
dass eine Änderung an einer Stelle das Programm abstürzen lässt. **Statt es
auszuprobieren und die geschützte Datei anzufassen**, wird der Plan nur im
Arbeitsspeicher verändert. Das zeigt dieselbe Wirkung und lässt die Datei in
Ruhe.

Die zweite Messung: Ein Testprogramm gilt seit Tagen als „rot", aber nirgends
steht, **welche** Prüfungen scheitern. Ohne diese Liste weiss niemand, ob die
freigegebene Arbeit den Test wirklich grün macht.

⭐ **Und wenn die Vormessung falsch war, ist das ein gutes Ergebnis** — es steht
dann ausdrücklich so im Bericht.
