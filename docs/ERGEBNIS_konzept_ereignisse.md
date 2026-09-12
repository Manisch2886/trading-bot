# Ergebnis — Konzeptpapier Ereignis-DB und Anbieter-Schnittstelle

**PR #82** · Branch `claude/new-session-uqjk8h`, Basis `origin/main` (`e93ae56`).

**Kein Produktivcode.** Drei neue Dateien unter `docs/`, sonst nichts.

---

## Was zu entscheiden ist

Zwölf Fragen, jede mit Empfehlung, Alternative und Begründung im Konzept.
**Keine ist getroffen.**

| # | Frage | Empfehlung |
|---|---|---|
| E1 | Eine Ereignis-Tabelle oder mehrere? | eine, mit `art`-Spalte |
| E2 | Feste Spalten oder JSON? | **beides**, mit klarer Grenze |
| E3 | Läufe als Ereignisse? | ja — sonst bleibt Punkt 12 ungelöst |
| E4 | Wer schreibt? | eine gemeinsame Funktion in `shared/` |
| E5 | Die drei vorhandenen DBs migrieren? | **nein**, Stichtag |
| E6 | Aufbewahrung? | 400 Tage roh, dann Tagesverdichtung |
| A1 | Registrierung statt Konfiguration? | ja, mit benannter Bruchlinie |
| A2 | „Liest" gegen „handelt"? | zwei Basisklassen, kein Flag |
| A3 | Echtgeld gegen Paper? | **zwei Datenbankdateien** |
| A4 | Crash-Knopf erweitern? | **nein** |
| A5 | Welcher Anbieter zuerst? | **keiner** |
| R1 | Mac zum Server? | **nicht entscheidbar** — hängt am Nutzer |

---

## Die drei Empfehlungen, die am ehesten überraschen

**Die drei vorhandenen Datenbanken werden nicht übernommen.** Sie sind keine
Ereignis-Historien, sondern Arbeitsvermerke: `spiegelungen` beantwortet „ist
diese Order schon draussen?". Überführt man sie, hängt die
Doppelsende-Sicherung einer produktiv laufenden Brücke an einer Tabelle, die
auch das Dashboard beschreibt. Nachimportieren geht jederzeit — die Schlüssel
sind kompatibel.

**Der Crash-Knopf wird nicht erweitert.** Für Trade Republic könnte er
technisch nichts tun, und ein Knopf, der Schliessen suggeriert und es nicht
kann, ist im Notfall schlimmer als keiner. Für Binance ginge es — `api.binance.com`
steht aber namentlich auf der Verbotsliste, zusammen mit neun weiteren Hosts.

**Echtgeld und Paper werden durch zwei Datenbankdateien getrennt, nicht durch
eine Spalte.** Eine Spalte schützt nur, solange jede Abfrage sie im `WHERE`
hat; eine vergessene Bedingung sähe plausibel aus — genau das Fehlerbild aus
PR #81.

---

## Was die Bestandsaufnahme ergab

**Drei Muster tragen das Schema:** ein fachlicher Schlüssel mit `UNIQUE` statt
einer `if`-Abfrage · Erfolg und Versuch in **getrennten** Tabellen (damit ein
Fehlschlag den `UNIQUE`-Platz nicht blockiert) · Zeitstempel als UTC-Text.

**Siebzehn Ereignisarten, verteilt auf sieben Ablageorte** — Telegram, zwei
DBs, eine JSON-Datei, zwei Logdateien, E-Mail und ein Markdown-Dokument, das
von Hand gepflegt wird. Drei Arten landen heute **nirgends abfragbar**, und es
sind die, die am meisten fehlen: Läufe, Agenten-Hinweise, Brücken-Abweichungen.

**`monitor.py`/`state.json` lehrt drei Dinge**, alle im Entwurf bindend: je
Vorgang eine Zeile (kein Mengenvergleich) · erst bestätigen, wenn die Wirkung
eingetreten ist · ein verlorener Zustand muss auffallen statt still neu
anzufangen.

---

## Die Randbedingung, die alles formt

**Die Bots dürfen nicht angefasst werden — also können sie nichts melden.**
Selbstmelder rufen die Schreibfunktion direkt, die Bots werden von einem
Sammler fremdbeobachtet. Für **Trades** geht das sauber. Für **Läufe** nicht:
alle drei möglichen Ersatzquellen (Log-Änderungszeit, neue Log-Zeilen,
Cron-Mail) haben Mängel.

Deshalb ist E3 eine Entscheidung mit Preis. Kurzfristig: Heuristik bauen und
als `quelle='heuristik'` kennzeichnen. Mittelfristig ist es Ihre Entscheidung,
ob zwei Zeilen in `forward_test.py` die Ausnahme wert sind.

---

## Zahlen

* **730 Prozessstarts am Tag** könnten schreiben; die Datenbank wäre dabei rund
  **10 Sekunden von 86.400** beschäftigt. Kollisionen sind selten, aber
  gebündelt — Cronjobs starten auf der Minute.
* **Nebenbefund:** nur `manual_close.py` setzt im ganzen Repo ausdrücklich
  `busy_timeout`; **WAL benutzt niemand.** Für die Ereignis-DB ist WAL fast
  wichtiger als der Timeout, weil das Dashboard bei jedem Seitenaufruf liest.
* **90 Ereignisse am Tag, 33.000 im Jahr, ~10 MB.** Über **80 % davon wären
  Lauf-Ereignisse** — daher die Verdichtungsregel.

---

## Umsetzung

Zehn Schritte, jeder ein eigener PR, mit Abhängigkeiten und Aufwand im Konzept.
Zwei Punkte:

* **Nach Schritt 5 kann man aufhören.** Der Zeitstrahl ist da und nützlich,
  ohne dass ein bestehender Meldeweg verändert wurde.
* **Schritt 6 ist der eigentliche Gewinn** (`monitor.py` liest aus der
  Ereignis-DB, `state.json` entfällt) — und der Schritt mit der höchsten
  Unsicherheit.

Schritt 9 (Anbieter-Schnittstelle) steht hinten: er fasst als einziger
produktiven Brücken-Code an und lohnt erst mit einem dritten Anbieter.

---

## Was du noch tun musst

**Lesen und entscheiden.** Es läuft nichts, es ändert sich nichts, es gibt
nichts zu testen.

Die fünf Fragen, die ohne dich nicht beantwortbar sind:

1. **R1** — Umzug auf einen dauerhaft laufenden Rechner? Daran hängt, ob SQLite
   mit WAL die richtige Grundlage bleibt.
2. **E3** — zwei Zeilen in `forward_test.py` wert? Das ist der Unterschied
   zwischen „vermutlich gelaufen" und „gelaufen".
3. **A4** — bleibt der Crash-Knopf bei der Paper-Welt?
4. **E6** — 400 Tage Rohdaten, oder alles behalten?
5. **Schritt 6** — `monitor.py` umhängen, oder alten Weg parallel lassen?
   Parallel ist sicherer, bedeutet aber wieder zwei Wahrheiten.

## Geänderte Dateien

```
docs/KONZEPT_ereignisse_und_anbieter.md   (neu, das Konzept)
docs/UEBERGABE_konzept_ereignisse.md      (neu)
docs/ERGEBNIS_konzept_ereignisse.md       (neu, dieses Dokument)
```

Nichts sonst. Kein Produktivcode, keine Tests, keine Datenbank, kein
bestehender Code — der Diff enthält ausschliesslich neue Dateien unter `docs/`.
