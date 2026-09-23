# Anfrage an Fable 5.1 — 23.09.2026, 19:05: Der Absturz ist weg, der Modus-Nachweis steht — aber zwei Fertigkriterien widersprechen sich, und Punkt 8 ist im Code vollzogen und im Register nicht

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat · **HEAD:** `fcc3265` (TB-92 Abgabe)
**Bezug:** deine Antworten **23d** und **23e**

**Sichtschutz:** Verfahrensmessungen — 27.2. ⛔ Keine Kennzahl des
Selektionsraums; die Meldetexte von `G6`/`H3` geben wir nur dem Sinn nach wieder,
ohne die Zahlen, die sie nennen.

⚠️⚠️ **Der Arbeitsbaum steht in einem Zwischenzustand.** Wir haben nichts
nachgebessert und warten.

---

## 1. ⭐⭐ Was der Vollzug erreicht hat

| | |
|---|---|
| ⭐⭐ **Der Absturz ist weg** | `test_vorregistrierung.py` läuft **erstmals bis zur Schlusszeile** — Teil A bis H, 501 s, keine Ausnahme. Mit der alten Tabelle brach er in **Teil A** ab |
| ⭐ **Form (ii) gewahrt** | `benchmark_drawdowns.json` steht **unverändert** bei `a163c498…`. Nicht ersetzt, nicht überschrieben. Geändert wurden die **Leser** |
| ⭐ **Alle drei Leser, ein Commit** | `auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py` über **eine** Konstante — ⛔ kein Schalter (12). AST aller Funktionskörper unverändert |
| ⭐⭐ **Modus-Nachweis A1b (23e)** | `benchmark.py` im Selektionsmodus über `snapshots/<hash>/`: **zweimal** gelaufen, je 51 s, **beide bytegleich** mit der Neurechnung (`64fb2912…`) |

⭐ **Und ein Fund, den die Sitzung von sich aus gemacht hat:** Sie hat einen
**Lesehaken** gebaut und protokolliert, was der Lauf im Modus tatsächlich öffnet.
Ergebnis: 222 Dateien aus `snapshot/csv`, 2 aus `snapshot/config` — ⚠️ **aber
auch `ergebnisse/messgroessen.json` und neun Trade-Listen aus dem Repo.** Das ist
deine Sonde „Lesequellen" im Kleinen, und sie findet genau die Datei, deren
Eingabestand du in 23d beanstandet hast.

## 2. ⛔ Was nicht erreicht ist

**`test_vorregistrierung.py`: 163 bestanden, 2 gescheitert — `G6` und `H3`.**

⭐ **Dieselben zwei Namen und dieselbe Zahl wie in TB-88 und TB-90** — aber
**zum ersten Mal am echten Stand gemessen**, nicht in der Simulation.

| | dem Sinn nach, ohne Zahlen |
|---|---|
| `G6` | bei `elliott_wave`: zwei Falten werden als Testfalten geführt, nicht als Trainingsjahre |
| `H3` | ohne eine gesetzte Null ändert sich die Statistik |

⇒ ⭐ **Der Vollzug hat sie nicht berührt** — so wie du es in 23a vorhergesagt
hast: *„G6 und H3 berühren keine Tabelle, sondern den Faltenplan."* Jetzt ist es
gemessen statt erwartet.

**Nach dem Auftrag (B3) sind Block C und D damit entfallen.** Die Sitzung hat
**nicht nachgebessert**.

---

## 3. ⚠️⚠️ Der Widerspruch — gefunden von der Mac-Sitzung, nicht von uns

**Zwei Fertigkriterien für denselben Punkt, und sie sagen Verschiedenes:**

| Quelle | Wortlaut | erfüllt? |
|---|---|---|
| ⭐ **Deine Antwort 23d** | *„`test_vorregistrierung.py` läuft **durch bis zur Schlusszeile** (Absturz weg); `G6`/`H3` bleiben der eigene Punkt aus 23a"* | ✔ **JA** |
| ⛔ **Registertext 38.4** (Z. 6775) | *„Vollzug fertig, wenn … `test_vorregistrierung.py` **grün** — die roten Prüfungen misst TB-88 —, neues Abbild, Sonde gegen das Abbild 0 für die Pfade"* | ⛔ **NEIN** |

⚠️ **Der Registertext trägt die Zweideutigkeit in sich:** Der Einschub *„die
roten Prüfungen misst TB-88"* deutet darauf, dass `G6`/`H3` **nicht** als Blocker
gemeint waren — das Wort davor verlangt aber „grün".

⭐ **Die Sitzung hat dem Auftrag gehorcht und abgebrochen**, mit dem Satz:
*„Welches Kriterium gilt, entscheidet nicht diese Sitzung."* Wir halten das für
richtig.

### ⚠️⚠️ Und die Folge, die uns am meisten beschäftigt

> **„Der Vollzug ist im Code erfolgt, im Register nicht."**

Es fehlen: Registertext (Schritt 1), Tatsachennotizen zu `_vt`/`_tb72` (2),
**neues Abbild** (4), Determinismus-Notiz (5) — deine eigenen fünf Schritte.

⇒ **Repo und Register stehen auseinander.** Das duldet das Verfahren sonst
nicht, und es ist der einzige Grund, warum wir dich heute noch fragen statt
morgen.

---

## Die Frage

| | |
|---|---|
| **(1)** | Welches Kriterium gilt — dein Satz aus 23d („durch bis zur Schlusszeile") oder der Registertext 38.4 („grün")? ⭐ Wir lesen den Einschub *„die roten Prüfungen misst TB-88"* als Hinweis, dass `G6`/`H3` nie Blocker sein sollten — aber das ist Auslegung, und sie steht dir zu |
| **(2)** | Falls **23d** gilt: Wird Punkt 8 **jetzt** zu Ende geführt (Registertext, Notizen, neues Abbild), mit `G6`/`H3` als eigenem, offenem Punkt? Dann braucht es einen Folgeauftrag, und 38.4 bekommt eine Berichtigung |
| **(3)** | Falls **38.4** gilt: Punkt 8 bleibt offen, bis `G6`/`H3` grün sind. ⚠️ **Dann steht der Code-Vollzug ohne Registerdeckung** — bleibt er stehen, wird er zurückgenommen, oder bekommt er eine Tatsachennotiz „vollzogen, Registereintrag folgt"? |
| **(4)** | ⚠️ Unabhängig davon: `G6` und `H3` sind jetzt **am echten Stand** gemessen. Sollen wir ihre Ursache ausmessen (eigener Auftrag), oder bleibt das nach 23a hinter dem Vollzug? |

⭐ *Wir neigen zu (1) „23d gilt" mit (2): Dein Satz ist jünger als der
Registertext, er ist in Kenntnis von `G6`/`H3` geschrieben, und der Einschub im
Registertext zeigt in dieselbe Richtung. Aber ein Fertigkriterium auszulegen, das
im Register steht, ist nichts, was wir uns nehmen.*

---

## In einfacher Sprache

**Der Stichtags-Blocker ist zur Hälfte gefallen.** Das Prüfprogramm stürzte seit
Tagen ab, weil die Vergleichstabelle bei fünf von neun Bots keine Zeitabschnitte
enthielt. Nach dem Austausch läuft es zum ersten Mal komplett durch — alle acht
Teile, gut acht Minuten.

**Aber es ist nicht fehlerfrei.** Zwei von hundertfünfundsechzig Prüfungen
scheitern weiterhin — dieselben zwei wie seit Tagen, und sie haben mit der
Tabelle nichts zu tun. Das hatte der Verfahrensprüfer so vorhergesagt.

**Und jetzt kommt das Problem:** Er selbst hat an einer Stelle geschrieben, es
genüge, dass das Programm „durchläuft" — im Register steht dagegen „fehlerfrei".
Beides ist von ihm, beides betrifft denselben Punkt, und beides sagt etwas
anderes. Die Mac-Sitzung hat das bemerkt, nicht nachgebessert und die Frage
weitergegeben. Das war richtig.

**Deshalb fragen wir heute noch:** Der Austausch ist im Programmcode schon
geschehen, im Register aber nicht eingetragen — und dieser Zwischenzustand soll
nicht über Nacht stehen bleiben, ohne dass der Verfahrensprüfer davon weiß.
