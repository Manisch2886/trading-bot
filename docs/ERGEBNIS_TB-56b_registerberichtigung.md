# ERGEBNIS TB-56b — Die Registerberichtigung zu Abschnitt 15.6 (19.09.2026)

**Weg: diese Sitzung, über die Geräteanbindung an das MacBook. Rein lesend
gemessen; geschrieben wurde ausschliesslich unter `docs/`.**

⚠️ **Jede Aussage hier sagt, ob sie gemessen oder erschlossen ist**
(`DOKUMENTATIONSSTANDARD.md`, Regel 1).

---

## Was TB-56b getan hat

| | |
|---|---|
| **Angehängt** | `docs/VORREGISTRIERUNG_neuselektion.md`, neuer **Abschnitt 21** — Berichtigung zu Registertext 4 |
| **Entfernte Zeilen** | **0** — nachzuweisen über `git diff --numstat` |
| **Gesperrte Dateien berührt** | **keine** |
| **Code geändert** | **nichts** |

---

## Die Messungen dieser Aufgabe

**Alle über die Geräteanbindung, rein lesend, mit `--no-optional-locks`.**

| # | Messung | Ergebnis |
|---:|---|---|
| 1 | `HEAD` vor der Arbeit | `d46fdde`, dann `9235880` nach dem Commit der beiden Führungsdokumente; beide auf `origin/main` |
| 2 | Unversionierte Dateien repoweit | **2** vor dem Commit (`DOKUMENTATIONSSTANDARD.md`, `FABLE_ANFRAGE_…`), **0** danach |
| 3 | Geänderte Dateien gegenüber `HEAD` | **0** |
| 4 | Der berichtigte Satz | `docs/VORREGISTRIERUNG_neuselektion.md`, Zeilen **1355–1360** |
| 5 | Nennt ein Registertext eine Jahreszahl? | **nein** — 4a (Z. 1303–1306) und 3b (a) (Abschnitt 16.7) nennen keine; gemessen durch Lesen beider Texte |
| 6 | Kopien der Schranke im Quelltext | **zwei verbliebene**: `research/faltenplan_neun/faltenplan_neun.py:120`, `research/krypto_historie/faltenplan.py:64`. `registerdaten.py::ERSTE_MOEGLICHE_FALTE`: **0 Treffer** (entfernt in `7387cc5`) |
| 7 | Kommentar über der verbliebenen Kopie | `faltenplan_neun.py:119` verweist auf `registerdaten.py::ERSTE_MOEGLICHE_FALTE` — **auf eine Konstante, die es nicht mehr gibt** |
| 8 | `benchmark_drawdowns.json` (gesperrt) | SHA-256 `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`, letzte Änderung **14.09.2026**, letzter Commit `a2fcf01` (TB-30a) — **byteweise unverändert** |
| 9 | `DD_Toleranz`, gesperrt gegen neu | ändert sich bei **`rsi2_mean_reversion`** und **`volatility_breakout`**, dort auf **allen 100** Exposure-Stufen; bei `elliott_wave_stocks` und `turtle_soup_stocks` **unverändert**; die fünf Krypto-Bots sind in **beiden** Tabellen `status: platzhalter` mit **leerer** `dd_toleranz` |
| 10 | Richtung und Grösse der Abweichung | **tiefer, also nachgiebiger**: −2,18 → −3,35 (25 %), −4,33 → −6,61 (50 %), −8,55 → **−12,89** (100 %) |
| 11 | Nummernstände (K2i) | höchster Blockbezeichner **`2r`** (Überschrift Z. 634) ⇒ frei **`2s`** · höchste K-Nummer **`K2k`** ⇒ frei **`K2l`** · höchste Kettenzeile **`0,97`** · höchster Nachtragsbuchstabe **`(r)`** ⇒ frei **`(s)`**, Journal **`(f)`** ⇒ frei **`(g)`** |
| 12 | `BACKLOG.md` | **951 Zeilen**, 261 525 Bytes, letzter Commit `fef279c` |

**Werkzeug zu 9 und 10:** ein Vergleichsskript über beide JSON-Dateien,
ausgeführt mit `/usr/bin/python3` (3.10.12) **in der Umgebung der
Geräteanbindung**. ⚠️ **Das ist ausdrücklich nicht die registrierte Umgebung**
(3.9.6, `requirements.lock`, Abschnitt 20). Zulässig ist es, weil nur **zwei
JSON-Dateien gelesen und Zahlen verglichen** wurden — keine Registerrechnung,
kein `pandas`, kein Bot-Loader. **Wäre eine Grösse neu zu berechnen gewesen,
hätte das auf dem Mac laufen müssen.**

---

## ⭐⭐ Der Befund, der die Arbeitsteilung von gestern begrenzt

⚠️⚠️ **Die Geräteanbindung ist kein Terminal auf dem MacBook. Sie ist eine
Linux-Umgebung, in die der Ordner `~/trading-bot` eingehängt ist.** Gemessen:

| | |
|---|---|
| `uname -a` | `Linux … 6.8.0-138-generic … Ubuntu SMP … x86_64` |
| `/etc/os-release` | `Ubuntu 22.04.5 LTS` |
| `python3 -V` in dieser Shell | **3.10.12** |
| `trading-env/bin/python3` | Datei **ist vorhanden**, Aufruf scheitert mit `No such file or directory` — eine macOS-Binärdatei läuft dort nicht |
| Einhängung | FUSE auf `/sessions/…/mnt/trading-bot` |

**Was das für „ich messe selbst" heisst** — die Grenze, ehrlich gezogen:

| ⭐ geht über die Anbindung | ⚠️ geht NICHT |
|---|---|
| Dateien lesen, `grep`, `wc`, `cmp`, `shasum`, Zeilen- und Bytezahlen | Den Betriebsinterpreter `trading-env/bin/python3` ausführen |
| Lesende git-Befehle mit `--no-optional-locks`: `HEAD`, `log`, `numstat`, `ls-files`, `branch -r --contains` | Basislauf, Trockenlauf des Laufcodes, Registerprüfer, `snapshot.py`, alles mit `pandas` |
| Dateien unter `docs/` ablegen, solange keine Mac-Sitzung läuft | Alles, was die registrierte Umgebung (3.9.6, Lock) braucht |
| Zahlen aus abgelegten JSON-Dateien vergleichen | Jede Messung, deren Ergebnis ins Register soll |

⭐ **Die Regel daraus:** *Die Anbindung liest das Repo, sie rechnet nicht darin.*
Eine Messung, die ins Register geht, braucht weiterhin einen **Mac-Lauf** —
`UEBERGABE_2026-09-19.md`, Nachtrag 2 ist an dieser Stelle zu weit gefasst und
gehört berichtigt.

⚠️ **Fast wäre daraus ein Fehler der Klasse aus Block 7, Punkt 3 geworden:** Ich
hätte „gemessen über die Geräteanbindung" schreiben können, ohne zu sagen, **mit
welchem Interpreter** — und `3.9.6` stand als Erwartung im Kopf, weil es im
Register steht. **Ein Name ist kein Messwert; eine Umgebung auch nicht.**

---

## Die Entscheidung, die in dieser Aufgabe getroffen wurde

**Betreiberentscheidung 19.09.2026, auf Vorlage mit drei Möglichkeiten und
benannter Empfehlung:** Wo Registertext 4a und 3b (a) verschiedene erste Falten
ergeben, **bindet 3b (a)**. Betroffen ist genau ein Bot, `t3_supertrend`, dessen
Zeile dadurch unverändert bei 2019 und sieben Falten bleibt.

⚠️ **Die Begründung ist strukturell, nicht ergebnisbezogen:** eine Falte ohne
handelbares Symbol erzeugt keinen Trade und damit keinen Falten-Sharpe. Nach der
Entscheidungsaufteilung vom 19.09.2026 ist das eine Verfahrensfrage vor dem Tag
und gehört dem Betreiber — sie wurde ihm vorgelegt, nicht von der Sitzung
entschieden.

---

## Offen, mit Zuordnung

| | Punkt | wohin |
|---|---|---|
| **1** | ⚠️⚠️ **Amendment zu Sperrliste Punkt 4** — Vorlage in Abschnitt 21.6, drei Wege, Empfehlung A | **Betreiber**, vor dem Tag |
| **2** | **Die zwei verbliebenen Code-Kopien der Schranke** nachziehen, dazu der Kommentar in `faltenplan_neun.py:119`, der auf eine entfernte Konstante zeigt | eigene Aufgabe **mit Mac-Lauf** (Freigabe für `faltenplan_neun.py` und seinen Test liegt seit TB-56 vor, nicht in Anspruch genommen) |
| **3** | ⚠️ **`test_faltenplan_neun.py` Probe F verfälscht `FRUEHESTE_FALTE = 2019`** (Zeile 519) — wird die Konstante entfernt, misst diese Probe nichts mehr | zusammen mit 2; **eine Probe, die nichts mehr misst, sagt es** (Prüfprinzip A5) |
| **4** | **Drei-Kategorien-Regel als Registertext 0** | wartet auf **Fable**, Fragen 1 und 3 |
| **5** | **„Änderung an Registertext 5f"** — gemessen: **keine Spezifikation im Repo**; der offene Teil (Lock-Hash) ist mit Abschnitt 20 geschlossen | **Betreiber**: gab es einen konkreten Änderungswunsch, oder ist der Punkt mit Abschnitt 20 erledigt? |
| **6** | **Krypto-Benchmark** — fünf von neun Bots haben **keine** `DD_Toleranz`, `status: platzhalter`, hängt an TB-31 | vor dem Tag, eigene Aufgabe |
| **7** | ⚠️ **Abschnitt 3 sagt dreimal „teilt Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle"** — nach der Berichtigung trifft das auf zwei der vier nicht mehr zu | zusammen mit dem Amendment (1) |

---

## In einfacher Sprache

**Was wir wissen wollten:** Im Regelwerk stand, die Auswertung beginne 2019, weil
das Regelwerk es so vorschreibe. Stimmt das?

**Was herauskam:** Nein. Kein Regeltext nennt eine Jahreszahl. Die Zahl stand nur
im Programm — und in dem Satz, der behauptete, sie komme aus dem Regelwerk. Das
Programm wurde gestern korrigiert, der Satz bis heute nicht.

**Warum das so ist:** Der Satz wurde geschrieben, als die Zahl im Programm noch
stand, und er hat beschrieben, was er vorfand, statt nachzusehen, woher es kam.
Dieselbe Fehlerart, die gestern viermal aufgetreten ist.

**Was das für dich heisst:** Zwei Dinge. Erstens ist die Berichtigung geschrieben
und kostet dich einen Commit. Zweitens — und das ist der unangenehme Teil —
bekämen zwei Bots durch die Korrektur eine **nachgiebigere** Verlustschranke.
Darüber entscheidest du, nicht ich, und zwar genau deshalb, weil man jetzt weiss,
in welche Richtung es ginge. Die Zahlen liegen dir vor.

**Und ein dritter Punkt, der nichts mit dem Register zu tun hat:** Die
Geräteanbindung, auf die wir gestern die ganze Arbeitsteilung gestützt haben,
**liest** dein Repo, aber sie **rechnet** nicht darin — sie läuft auf einem
anderen Betriebssystem als dein MacBook. Messungen fürs Register brauchen
weiterhin einen Mac-Lauf. Das stand so nicht in der Übergabe und gehört
hineingeschrieben.
