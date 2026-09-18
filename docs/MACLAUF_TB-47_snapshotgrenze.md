# Mac-Lauf TB-47 — Die Snapshot-Grenze

**Ausgeführt am 18.09.2026, 07:47–08:32 UTC (09:47–10:32 CEST), auf dem
Betriebsrechner, als autonome Claude-Code-Sitzung nach
[`docs/TESTAUFTRAG_TB-47_snapshotgrenze.md`](TESTAUFTRAG_TB-47_snapshotgrenze.md).**
Zweig `claude/new-session-ebo6mm`, Stand `ee34f1a`.

Rohausgaben: `~/Downloads/TB-47_ergebnisse/` (als ZIP
`~/Downloads/TB-47_macergebnisse_<Zeit>.zip`), Sicherung der neun Datenbanken
unter `~/Downloads/TB-47_db_sicherung_20260918T074742Z/`. Der Basislauf liegt
zusätzlich im Repo als
`research/datenordner_schnitt/ergebnisse/basislauf_tb47_mac.json`.

---

## Das Wichtigste zuerst

**Alles, was der Auftrag erwartet hat, ist eingetreten — auf Python 3.9.6,
mit `pandas` 2.3.3, am echten Bestand.** Kein Abbruchgrund, kein Befund gegen
den Zweig. Die einzige Abweichung vom Auftrag liegt in der Zählweise eines
`grep` in Schritt 5b (die Zählung traf die eigene Shell); die Nachprüfung aus
einer Datei heraus ergibt **0 Überlebende**. Einzelheiten in Frage 6 und 9.

| Frage des Auftrags | Antwort |
|---|---|
| 1. Fassungen | Python **3.9.6** (beide Interpreter), `pandas` **2.3.3**, `numpy` 2.0.2, `dateparser` 1.2.2, `pandas_market_calendars` 4.6.1, `scipy` **fehlt**, `node` v24.21.0, GNU `timeout` **fehlt**, `gh` fehlt |
| 2. Datenstand vorher / nachher | beide `d9449faf…` / 223 — **unverändert** |
| 3. ⭐ `datenstand_hash` = `d9449faf…`? | **Ja, gezeigt:** `beide gleich: True`, `trifft den Anker: True`, zweiter Hash verschieden |
| 4. ⭐ Teilkerzen | **36 von 223**, alle `rand_erste`, **keine LETZTE Kerze** — exakt der Cloud-Wert |
| 5. ⭐ `test_snapshot.py` | **110 von 110**, Rückgabewert 0, kein `(Anker)`-Fehler |
| 6. ⭐ Prozessgruppe | 5a **11/11** (1.5 und 2.3 grün); 5b `Art: zeitgrenze`, **0 Überlebende** (nach Selbsttreffer-Bereinigung); Schritt 8: Zeile „Überlebende Prozesse" **leer** |
| 7. Datenbanken | `OK: alle neun Datenbanken byteweise identisch` — 7b nicht nötig |
| 8. Basislauf | **55 grün · 5 bekannt rot · 3 ungeprüft · 1 Zeitgrenze · 0 UNERWARTET** |
| 9. Abweichungen | eine, in der Messung, nicht im Werkzeug — siehe unten |

---

## 1. Python- und Paketfassungen (`00_umgebung.txt`)

```
macOS 15.7.9 (24G830), Darwin 24.6.0, x86_64
/usr/bin/python3           Python 3.9.6
trading-env/bin/python3    Python 3.9.6
pandas 2.3.3  numpy 2.0.2
dateparser 1.2.2
pandas_market_calendars 4.6.1
scipy: ModuleNotFoundError
node v24.21.0 (/usr/local/bin/node)
gh, timeout: nicht vorhanden
```

Abweichungen von der Tabelle des Auftrags: **keine.** Die Tabelle nennt
3.9.6 und `pandas` 2.3.3 — genau das wurde vorgefunden. Damit ist der in der
Cloud nicht prüfbare Punkt („`signal`, `os.killpg`, `start_new_session` auf
3.9 nur syntaktisch geprüft") jetzt **im Lauf** geprüft: alle vier
TB-47-Werkzeuge (`snapshot.py`, `zeitabdeckung.py`, `basislauf.py`,
`test_prozessgruppe.py`) starten und laufen auf 3.9.6 durch.

## 2. Datenstand vorher und nachher

```
01_datenstand_vorher.txt:
d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Kursdateien)  data

08_datenstand_nachher.txt:
d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84  (223 Kursdateien)  data
```

Der Datencron hat seit dem 15.09. **nichts** fortgeschrieben; der Anker gilt
weiterhin. `git status --porcelain` nach Schritt 8: **leer**.

## 3. ⭐ Ergibt `datenstand_hash` weiterhin `d9449faf…`? (`03_zwei_hashes.txt`)

```
herkunft.datenstand   : d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223
snapshot.gesamthash   : d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223
beide gleich          : True
verankerter Wert      : d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223
trifft den Anker      : True
snapshot_hash (223)   : 4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608
die beiden Hashes sind verschieden: True
```

`snapshot.py` rechnet dasselbe wie das registrierte Verfahren
(`research/vorregistrierung/herkunft.py`), und der zweite Hash über dieselben
223 Dateien ist ein anderer Wert — wie vorgesehen.

## 4. ⭐ Teilkerzen am echten Bestand (`04_teilkerzen.txt`, `04_teilkerzen.json`)

```
Geprueft: 223 Kursdatei(en), 0 uebersprungen.
36 Datei(en) mit Befund
Zusammenfassung: 36x rand_erste
Rueckgabewert: 1

Dateien mit Befund : 36 von 223
Arten              : {'rand_erste': 36}
LETZTE Kerze betroffen: False
```

**Exakt der Cloud-Wert vom 18.09.:** 36 von 223, nur `rand_erste`, keine
letzte Kerze. Der gefährliche Fall (ein Abruf mitten in eine Kerze) liegt
**nicht** vor. Alle 36 Befunde sind Krypto-Dateien, deren erste Tages- oder
4h-Kerze aus einer unvollständigen 1h-Teilmenge abgeleitet ist (z. B.
`AAVEUSDT_1d.csv`: erste Kerze 2020-10-15 aus 21 von 24 Stunden).

## 5. ⭐ `test_snapshot.py` auf 3.9.6 (`02_test_snapshot.txt`)

```
110 von 110 Pruefungen bestanden, 0 fehlgeschlagen.
Rueckgabewert: 0
```

Kein `(Anker)`-Fehler. Probe 3t: `der Rueckgabewert ist NICHT_PRUEFBAR (2),
nie 0 — rc=2` grün. Probe 3u: grün (der Anker wurde in Schritt 1 getroffen).
Randbedingung 5 des Tests: Datenstand vor und nach dem Test identisch, git
sieht unter `data/` nichts.

## 6. ⭐ Beendet der Runner die ganze Prozessgruppe?

**5a (`05a_prozessgruppe.txt`):** `11 von 11 Pruefungen bestanden`,
Rückgabewert 0.

```
1.5 ⭐ DER ENKELPROZESS LEBT EBENFALLS NICHT MEHR   PID 16310
2.3 ⭐ der Enkelprozess ueberlebt das alte Verfahren - genau das war der Befund   PID 16315
```

Die Gegenprobe 2.3 ist grün — der Test misst also die Reparatur, nicht einen
Zufall. Abbruch an der Zeitgrenze in 5,0 s (Probe 1.3).

**5b (`05b_zeitgrenze.txt`), der echte Fall:**

```
Art      : zeitgrenze
Dauer    : 45.0 s
```

⚠️ Die wörtliche Zeile des Auftrags ergab `Gefundene Ueberlebende: 4`. **Alle
vier Treffer waren die eigene Shell:** Claude Code führt jeden Befehl über
einen `/bin/bash -c '…'`-Umschlag aus, dessen Befehlszeile den gesamten
Heredoc-Text — und damit das Wort `drawdown` — enthält; `grep "[d]rawdown"`
schützt nur gegen den `grep`-Prozess selbst, nicht gegen diesen Umschlag
(dasselbe Artefakt kannte schon der TB-46b-Lauf: „`pkill -f` trifft eigene
Shell"). Die Prozessliste in `05b_zeitgrenze.txt` zeigt **nur**
`/bin/bash -c …`-Zeilen, keinen einzigen Python-Prozess. Schon die
Vorher-Zählung (`05b_prozesse_vorher.txt` = `2`) war dieses Artefakt.

Nachgeprüft mit einer Zählung, die das Muster **nur in einer Datei** trägt
(`05b_ueberlebende.py`, eigene PID ausgeschlossen, aufgerufen ohne Heredoc):

```
--- Nachpruefung 3: Aufruf der Datei ohne Heredoc (Befehlszeile enthaelt kein Muster) ---
Gefundene Ueberlebende (ohne Selbsttreffer): 0
```

**0 Überlebende.** Kein `kill -9` war nötig.

**Schritt 8, nach dem vollen Basislauf** (in dem
`shared/test_drawdown_beide_masse.py` 900 s lief und dabei — per `ps`
beobachtet — einen Enkel mit 98,7 % CPU startete):

```
--- Ueberlebende Prozesse (erwartet: KEINE) ---
(leer)
```

Beobachtet während des Laufs: um 08:21 UTC standen Kind (PID 18647) und Enkel
(PID 18649, 98,7 % CPU, 14:45 min) in der Prozessliste; um 08:25 UTC waren
beide verschwunden und der Basislauf beim nächsten Test. Genau das ist der
Unterschied zu den beiden früheren Mac-Läufen, in denen der Enkel 22 Minuten
weiterrechnete. **Teil 4 ist auf dem Rechner des Befunds wirksam.**

## 7. Die neun Datenbanken (`07_ergebnis.txt`, `07_diff.txt`)

```
OK: alle neun Datenbanken byteweise identisch
```

`07_diff.txt` ist leer; 7b entfiel. Zwischen Sicherung (07:47:42 UTC) und
Vergleich (07:54:22 UTC) lag kein Cron-Termin. *Zusätzlich, nicht vom Auftrag
verlangt (`09_info_db_nach_basislauf.txt`):* auch **nach** dem Basislauf
(08:32 UTC), also über die Cron-Termine 08:00 UTC (stündlich, 4-stündlich)
hinweg, sind alle neun Hashes noch identisch mit `vorher.sha256` — die Bots
hatten in dieser Stunde nichts zu schreiben. Die Sicherung wurde **nicht**
zurückgespielt.

## 8. Basislauf (`08_basislauf.txt`, `08_basislauf.json`)

64 Testdateien, Zeitgrenze 900 s je Datei, Dauer 07:54:37–08:31:43 UTC
(37 min), Rückgabewert 0.

| | Anzahl | Dateien |
|---|---|---|
| **grün** | **55** | darunter `shared/test_snapshot.py` (5,6 s), `shared/test_zeitabdeckung.py`, `shared/test_zuteilung.py` (in der Cloud Netzsperre, hier grün) |
| **rot, alle bekannt** | **5** | `shared/test_stabile_sortierung.py` (3) · `shared/test_wellenauswahl.py` (1) · `dashboard/test_portfolio_sicht.py` (1) · `research/exposure_messung/test_exposure_kern.py` (1) · `research/hrp_portfolio/test_hrp_core.py` (`scipy` fehlt) |
| **ungeprüft, nicht rot** | **3** | `research/drawdown_reihenfolge/test_drawdown.py` · `research/fib_score_stufen/test_stufen.py` · `research/elliott_wave_params/test_params.py` (Bot-Argument) |
| **Zeitgrenze** | **1** | `shared/test_drawdown_beide_masse.py` (900,0 s, erwartet) |
| **UNERWARTET** | **0** | |

Das ist wörtlich die Liste „bekannt rot auf dem Mac" des Auftrags — nicht
mehr, nicht weniger. Der TB-46b-Maclauf hatte 54/5/3/1; das eine Grün mehr
ist `shared/test_snapshot.py` bzw. die neuen Dateien dieses Zweiges
(`test_zeitabdeckung.py`, `test_prozessgruppe.py`, das in Schritt 5a gesondert
lief).

## 9. Abweichungen von diesem Auftrag

1. **Schritt 5b, Zählung der Überlebenden** — s. Frage 6. Der wörtliche
   Befehl zählte 4, alles Selbsttreffer des Bash-Umschlags von Claude Code.
   Ergänzt wurden drei Nachprüfungen (im selben `05b_zeitgrenze.txt`), die
   letzte davon sauber: **0**. Das Werkzeug ist nicht betroffen; nur die
   Messvorschrift des Auftrags ist in einer Claude-Code-Sitzung anfällig für
   diesen Fehlschluss. Vorschlag für künftige Aufträge: Muster in eine Datei
   legen oder `ps … | grep -v '/bin/bash'` mit einem Python-Zähler.
2. **Schritt 8 wurde im Hintergrund gestartet** (Ausgabe erst am Ende in
   `08_basislauf.txt` sichtbar, weil gepuffert); Start- und Endzeit stehen
   in `08_startzeit.txt`. Die `sleep 15`-Nachprüfung, der Datenstand nachher
   und `git status` liefen danach wie beschrieben.
3. **Zusatzbeobachtung** `09_info_db_nach_basislauf.txt` (Datenbanken auch
   nach dem Basislauf identisch) — vom Auftrag nicht verlangt, nur Information.
4. Die Testausgaben von Schritt 2, 4, 5a, 6 und 8 wurden per Umleitung in die
   Datei geschrieben und der Rückgabewert danach angehängt (statt `tee` in
   der Pipe), damit `$?` den des Werkzeugs und nicht den von `tee` meldet.
   Inhaltlich derselbe Befehl.

Nichts davon berührt `data/`, `live_params.py`, eine Crontab, einen
Registertext oder einen Broker-Endpunkt. **Es wurde kein Snapshot gezogen**
(`~/Downloads/TB-47_niemals` existiert nicht, Schritt 6 brach mit
Rückgabewert 2 an den 36 Teilkerzen ab — wie von Registertext 5a verlangt).

## Was geändert wurde

| Datei | |
|---|---|
| `docs/MACLAUF_TB-47_snapshotgrenze.md` | dieses Dokument |
| `research/datenordner_schnitt/ergebnisse/basislauf_tb47_mac.json` | **neu** — der Basislauf dieses Laufs |

`git status --porcelain` nach dem Commit: siehe `08_git_status_nach_commit.txt`
im Ergebnisordner.
