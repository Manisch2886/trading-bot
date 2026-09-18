# Backlog-Nachtrag 18.09.2026 (b) — TB-49

> ⚠️ EINGEARBEITET am 18.09.2026 in `docs/projektfuehrung/BACKLOG.md`, Commit 02de1f7.
> Dieses Dokument bleibt als Beleg des Nachtrags stehen und wird nicht
> mehr fortgeschrieben.

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **NACH dem Nachtrag (a) einzuarbeiten** — er setzt Block **2g** und die
dortige Kettentabelle voraus.

> ⚠️ **Nichts wird entfernt.** Ein neuer Block, zwei benannte Ersetzungen,
> Ergänzungen an einer Tabelle. Prüfung: `git diff --numstat` — entfernte Zeilen
> nur so viele, wie die Ersetzungen umfassen.

---

## Ersetzung 1 — die Kopfzeile

`**Stand: 18.09.2026.**` bleibt, **keine Änderung nötig**, wenn Nachtrag (a)
schon eingearbeitet ist.

---

## Ersetzung 2 — zwei Zeilen der Kette (Abschnitt 3)

**Zu finden** (die zwei Zeilen aus Nachtrag (a)):

```
| **0,82** | ⭐ **TB-49 — die Ausnahme ins Werkzeug, der Prüfer ins Repo** | **formuliert 18.09.**, `CLOUD_TB-49_ausnahme_ins_werkzeug.md`. **Der letzte Schritt vor dem Snapshot** |
| **0,84** | **Snapshot ziehen** | ⚠️ **erst nach TB-49** — das Werkzeug verweigert heute bei allen 36 Befunden |
```

**Zu ersetzen durch:**

```
| ~~0,82~~ | ~~TB-49 — die Ausnahme ins Werkzeug~~ | ⭐ **CLOUD FERTIG 18.09.**, Zweig `claude/new-session-kfbw56`. ⚠️ **Mac-Lauf und Merge offen** — der Mac-Lauf trägt hier wirklich etwas. Siehe Block **2h** |
| **0,84** | **Snapshot ziehen** | ⭐ **nach dem Merge nicht mehr blockiert.** ⚠️ **Eigene Entscheidung mit eigener Freigabe** — TB-49 hat ihn ausdrücklich nicht gezogen |
```

---

## Neuer Block 2h — aus TB-49

**Einzufügen NACH Block „2g — Aus TB-48, Registernachtrag".**

---

### 2h — Aus TB-49, die Ausnahme ins Werkzeug (Stand 18.09.2026)

**TB-49 ist in der Cloud fertig, Zweig `claude/new-session-kfbw56`.**
⚠️ **Mac-Lauf vor dem Merge, nicht danach.** Datenstand `d9449faf…`/223 vorher =
nachher, **kein Snapshot gezogen**, Sperrliste maschinell geprüft unberührt.

| # | Punkt |
|---|---|
| **T49.1** | ⭐⭐ **DER NACHWEIS IN ZWEI ZAHLEN: 2 → 0, bei unverändert 36 Befunden.** Am Stand von TB-48 gegen dasselbe `data/`: `RC_ALT=2`. Mit dem Zweig: `RC_TROCKENLAUF=0`, und `teilkerzen()["befunde"]` führt weiter **alle 36**. *Die Prüfung ist nicht weicher geworden, nur klüger.* Am Wegwerf-Bestand wirklich gezogen: **225 Dateien, 211,0 MB, jede byteweise gegen die Quelle geprüft**, `UNVERAENDERT` beim Nachprüfen |
| **T49.2** | ⭐⭐ **ENTSCHIEDEN JE BEFUND, NICHT JE DATEI — und das stand nicht im Auftrag.** Im `rand_letzte`-Versuch trägt `BTCUSDT_1d.csv` **beides**: einen zugelassenen `rand_erste` an ihrer ersten Kerze und den gestellten `rand_letzte`. Der zugelassene bleibt in der Zählung, **die Datei bricht trotzdem ab.** ⚠️ *Eine Zulassung je Datei hätte den gefährlichen Rand durchgelassen, sobald derselbe Name auch einen erlaubten Befund trägt.* Probe `3x` misst es |
| **T49.3** | ⭐ **Die Ausnahme ist als REGEL umgesetzt, drei Bedingungen** (`shared/snapshot.py::_zulassung`): Art `rand_erste` · **erste** Kerze der Datei · Urteil `ABGELEITETE_TEILKERZE` **und** `aggregat_passt is True`. **Keine Liste der 36 Dateien** — ein neu gelistetes Symbol ist damit automatisch gedeckt, ein `rand_letzte` nie |
| **T49.4** | ⭐ **Zwei Entwurfsentscheidungen, die niemand verlangt hatte.** **(1)** Bedingung **(b)** wird eigens nachgestellt, obwohl `rand_erste` heute nur an der ersten Kerze entsteht: *„Die Bedingung des Registers lautet ‚die erste Kerze der Datei', nicht ‚ein Befund, der sich so nennt'. Wer die Herkunft des Namens für den Nachweis nimmt, prüft nichts."* **(2)** Bedingung **(c)** holt das Urteil **aus dem geladenen Modul**, statt es abzuschreiben — kennt `zeitabdeckung.py` den Namen künftig nicht mehr, ist die Bedingung **nicht prüfbar** ⇒ **2**. *Eine Abschrift liefe gegen ein Urteil, das die Prüfung gar nicht mehr vergibt: die Ausnahme griffe dann entweder nie oder immer* |
| **T49.5** | ⭐ **`kein_zeuge` ist beantwortet: nicht belegbar ist nicht zugelassen — und es ist folgenlos.** Die **175** Dateien mit `kein_zeuge` tragen **null** Befunde. Grund im Aufbau: fehlt der feinere Zeuge, kehrt `pruefe_datei` **vor** der Deckungsprüfung um und hinterlässt einen **Hinweis**, keinen Befund; `rand_erste` entsteht ausschliesslich aus der Deckungsprüfung. **Wo `kein_zeuge` steht, kann es keinen `rand_erste` geben.** ⚠️ **Streng wird die Regel erst, wenn eine Eingabe von aussen einen Befund ohne Deckung behauptet oder einer Datei der Zeuge abhandenkommt** — Probe `3aa` |
| **T49.6** | **Keine Übergehen-Flagge** — drei erfundene Flaggen ergeben **2**, und der Quelltext kennt keine (Probe `3ad`, zusätzlich von Hand nachgesehen). `shared/test_snapshot.py`: **110 → 164**, acht neue Proben, **sechs mit beissender Mutation**; die beiden übrigen können es nicht sein und sollen es nicht (Negativprobe · Messung einer **Abwesenheit**) |
| **T49.7** | ⚠️⚠️ **MEINE VERMUTUNG WAR FALSCH — und der Befund ist grösser als die Zahl.** Ich hatte vermutet, 2022 sei die früheste **Krypto**-Falte und 2019 die über alle neun. **Gemessen je Bot: alle neun beginnen 2019, Krypto eingeschlossen.** ⭐ **Woher die 2022 kommt:** `research/krypto_historie/daten/faltenplan_nach_tb34.json` — **`mindesttraining: 4`, nur Krypto**, `erstes_faltenjahr: 2022`, Symbolreihe `[3, 6, 9, 13]` — **zeichengleich die Reihe aus T34.9.** ⭐ **Der schlagende Beleg steht im Register selbst:** Abschnitt **15.6** nennt für die Krypto-Bots **ebenfalls 2019**. *Die 2022 in 17.3 widerspricht nicht einer `research/`-Datei, sondern dem eigenen Registertext.* ⚠️ **Der eigentliche Gehalt: zwei Faltenpläne mit verschiedenen ersten Falten liegen im Repo, und nur einer steht im Register — das ist T34.10.** ⭐ **Die Schlussfolgerung trägt trotzdem:** Prüfung 16 rechnet nach — **null** der 36 kurzen ersten Kerzen fällt in ein Faltenfenster, in dem ihr Symbol geladen ist |
| **T49.8** | ⚠️ **NEBENBEOBACHTUNG, NICHT AUFGELÖST: die 2019 kommt aus einer Schranke, nicht aus den Daten.** `erstes_faltenjahr_ohne_schranke` steht bei **acht von neun** Bots auf **2017 oder 2018**; die 2019 entsteht durch `ERSTE_MOEGLICHE_FALTE = 2019`. ⚠️ **Steht diese Schranke im Register?** Wenn nicht, führt das Register eine Zahl aus dem Code als Tatsache. **Nicht nachgesehen — gehört in den Mac-Lauf oder die nächste Registerrunde** |
| **T49.9** | ⚠️⚠️ **DER PREIS VON T48.3 IST BEZIFFERBAR: `pruefe_abschnitt17.py` lag den Unterlagen der TB-49-Sitzung NICHT bei** — das Archiv enthielt allein den Auftragstext, und im Repo war die Datei nirgends, **weil meine TB-48-Auflage sie draussen gehalten hat.** Sie wurde aus der Belegtabelle des TB-48-Ergebnisses **neu geschrieben**, und das steht ausdrücklich in der Datei: ⭐ *„Ein neu geschriebenes Werkzeug ist kein wiederhergestelltes."* **Auflage am Ergebnis geprüft: 19 Zahlen, genau eine Abweichung, Rückgabewert 1 — wie in TB-48.** Selbsttest `test_abschnitt17.py` **24/24**. ⭐ **Damit hat `ARBEITSWEISE.md` §11 eine Rechnung, nicht nur eine Regel** |
| **T49.10** | **Zwei Zahlen aus Abschnitt 17 fasst der Prüfer bewusst nicht an:** `pandas_market_calendars` (17.5 sagt *„auf dem Betriebsrechner"*) und die Drift-Messung aus 17.8 (braucht einen echten yfinance-Abruf, nach T35.4 bis TB-30b untersagt). ⭐ *„Das ist der Inhalt des Befunds, nicht seine Umgehung."* Erstere steht im Mac-Testauftrag |
| **T49.11** | ⭐ **`git status --porcelain` wurde ZWEIMAL genommen — vor und nach dem letzten Commit, beide im Beleg, die zweite leer.** Dritter Versuch nach TB-46 und TB-48, erstes Mal richtig. Basislauf **58 grün / 3 rot / 3 ungeprüft / 1 Zeitgrenze = 65**, ⭐ **einer mehr grün als in TB-48, und es ist genau der neue Test.** Die vier „UNERWARTET" sind dieselben vier Rechnerunterschiede wie in TB-48 |
| **T49.12** | ⚠️ **Die Buchstaben (a)(b)(c) bedeuten im Register etwas anderes als im Code.** Register: (a) erste Kerze / nicht `rand_letzte`, (b) Aggregat, (c) im Manifest aufgeführt. Code: (a) Art, (b) erste Kerze, (c) Aggregat. **Beide Nummerierungen stehen im Manifest nebeneinander**, und die Abbruchmeldung nennt „(b)/(c)". Sachlich stimmt alles — *aber „Bedingung (b)" heisst an zwei Stellen Verschiedenes.* **Dieselbe Familie wie `_ist_geraet` (T44.10).** Klein |
| **T49.13** | ⚠️ **Die Fehlermeldung zweier bekannt roter Tests sagt das Gegenteil von dem, was sie meint:** *„Abschnitt 6: `shared/ergebniskurven.py` meldet ‚9x AKTUELL' — Neu erzeugen mit: …"* — **wer das liest, schliesst „alles aktuell", und der Test ist trotzdem rot.** Gemeint ist offenbar die Erwartung, nicht der Fund. Betrifft `shared/test_stabile_sortierung.py` und `shared/test_wellenauswahl.py`. **Gehört zu T45.6** |
| **T49.14** | **`shared/test_umstellungstag.py` druckt für `volatility_breakout_crypto` `2026-09-18T12:43:54Z`** — einen Zeitpunkt **aus der Sitzung**, während der Umstellungstag `2026-09-16T04:42:24Z` ist. ⭐ **Im Repo ist nichts passiert:** `docs/umstellungstag_entscheidungskerze.json` steht **nicht** im Diff. **Aber eine Ausgabe, die ein heutiges Datum neben den festgehaltenen Umstellungstag stellt, ist verwechselbar.** Beim Mac-Lauf ein Blick wert, dort liegt die echte Datei |
| **T49.15** | **Offen, Betreiber: wird der TB-41-Prüfer um Abschnitt 17 erweitert, oder bleiben die beiden Werkzeuge nebeneinander?** TB-49 hat den TB-41-Prüfer **nicht** angefasst — *„diese Arbeit legt ein zweites Werkzeug daneben, sie baut das erste nicht um."* Er kennt Abschnitt 17 weiterhin nicht, und das sagt er selbst |
| **T49.16** | ⭐ **MAC-LAUF 18.09., 15:05–15:57, Python 3.9.6: ALLES BESTÄTIGT.** Trockenlauf **rc 0** mit 36 zugelassenen Befunden und Registerverweis · `rand_letzte` und nicht-abgeleiteter `rand_erste` je **rc 2**, kein Snapshot · `shared/test_snapshot.py` **164/164**, kein einziges `[FEHL` · **die neunzehn Zahlen zum ersten Mal auf dem Betriebsrechner: 19 von 19 geprüft, genau eine Abweichung (Nr. 15), rc 1 — zeichengleich zur Cloud**, keine Prüfung `nicht pruefbar` · Selbsttest **24/24** · früheste Falte **alle neun 2019** · **neun Datenbanken byteweise identisch** (`diff` leer, 9 Zeilen) · Datenstand `d9449faf…`/223 vorher = nachher · `git status` leer · **kein Snapshot-Ordner** |
| **T49.17** | ⚠️⚠️⚠️ **MEINE TB-47-KORREKTUR WAR FALSCH — und T38.10 hatte recht.** Ich hatte `system/test_log_rotation.py` aus `BEKANNT_ROT` gestrichen: *„auf BEIDEN Rechnern grün, 117/117."* **Zehn Einzelläufe auf dem Mac: 3 von 10 rot**, immer `116 von 117`, immer eine **zeitabhängige** Probe zum Restfenster, ein bis zwei fehlende Zeilen von 238–512, **und die gefallene Probe wechselt.** Rate **~30 %**. ⭐ **Der Satz der Sitzung, der es erklärt:** *„Die Streichung stützt sich auf je EINE Messung pro Rechner; bei ~30 % Flackerrate trifft eine Einzelmessung mit 70 % Wahrscheinlichkeit grün."* ⚠️ **Und es stand längst im Backlog: T38.10, seit dem 15.09. — ich habe einen dokumentierten Befund mit einer Einzelmessung überstimmt, ohne nachzusehen.** ⇒ **Beide Listen sind falsch, in entgegengesetzte Richtungen:** `UMGEBUNGEN.md` („bekannt rot") und `basislauf.py` Zeile 54–57 („auf beiden Rechnern gruen", **meine Streichung, seit TB-47 in `main`**). ⭐ **Richtig: grün im Regelfall, zeitabhängig flackernd.** ⚠️ **TB-50 Teil 5 muss korrigiert werden, BEVOR die Aufgabe läuft** — er verlangt dort das Streichen genau des richtigen Vermerks |
| **T49.18** | ⭐ **NEUES PRÜFPRINZIP, aus T49.17: eine Einzelmessung kann die ABWESENHEIT eines flackernden Fehlers nicht belegen.** Sie belegt nur, dass er in diesem Lauf nicht auftrat. **Gehört nach `docs/PRUEFPRINZIPIEN.md` als A6** — Text liegt als eigener Nachtrag bei |
| **T49.19** | ⚠️ **Mein Testauftrag prüfte nur `/tmp` auf Wegwerf-Reste.** Die Sitzung hat zusätzlich **`$TMPDIR`** gemessen (`/var/folders/b_/…/T/`) — *„wo `mkdtemp` auf dem Mac wirklich liegt"*. **Beide null.** ⚠️ *Ohne die Ergänzung hätte die Prüfung an der falschen Stelle gesucht und „sauber" gemeldet* — Prüfprinzip **A1**. **Gehört in die Testauftrags-Liste (`ARBEITSWEISE.md` §7c)** |
| **T49.20** | **Zwei weitere Alterungen in `docs/UMGEBUNGEN.md`, vom Mac gemessen:** *„sonst 1 312 statt **62** Testdateien"* — der Basislauf zählt jetzt **65** (die 62 ist von TB-45) · **`pandas_market_calendars` steht gar nicht in der Paketzeile**, obwohl Registertext 5f darauf verweist: **Mac 4.6.1, Cloud 5.4.0** · macOS-Fassung **15.7.9 (24G830), x86_64** fehlt ebenfalls. **Bestätigt** wurden: `node` v24.21.0 vorhanden, `scipy` fehlt, `pandas`/`numpy`/`dateparser` 2.3.3 / 2.0.2 / 1.2.2, und **`test_drawdown_beide_masse.py` hinterlässt seit TB-47 keinen Prozess mehr** |

---

## ⚠️ Berichtigung zu T47.9 aus dem Nachtrag (a)

**Der Nachtrag (a) trägt in Block 2f den Punkt T47.9:**

> *„`BEKANNT_ROT` enthielt einen falschen Eintrag: `system/test_log_rotation.py`
> ist 117/117 GRÜN auf beiden Rechnern. … Gestrichen, mit Kommentar: ‚Ein
> falscher Eintrag in dieser Liste ist teurer als gar keiner.'"*

⚠️ **Diese Aussage ist durch den TB-49-Mac-Lauf widerlegt (T49.17).**

**Anzufügen an T47.9, als eigener Satz — der alte Text bleibt stehen:**

> ⚠️⚠️ **BERICHTIGT 18.09.2026 durch den TB-49-Mac-Lauf (T49.17): Die Datei ist
> NICHT durchgehend grün. Zehn Einzelläufe auf dem Mac ergaben 3 von 10 rot,
> immer an einer zeitabhängigen Probe. Die Streichung beruhte auf je EINER
> Messung pro Rechner und war damit nicht belegt.** ⭐ **Richtig ist: grün im
> Regelfall, zeitabhängig flackernd — siehe T38.10, das den Befund seit dem
> 15.09. führte.**

⭐ **Nichts wird entfernt** — der Fehler bleibt mit seiner Berichtigung stehen,
damit ihn niemand wiederholt (`ARBEITSWEISE.md` §9).

---

## Ergänzung zu T34.10 (Abschnitt 2b)

**Anzufügen an den vorhandenen Punkt T34.10:**

> ⚠️⚠️ **HOCHGESTUFT 18.09.2026 durch TB-49, Teil 4.** Die Frage ist nicht mehr
> nur „wie viele Falten bekommt der Lauf", sondern: **welcher der beiden
> Faltenpläne im Repo gilt.** `research/faltenplan_neun/daten/faltenplan.json`
> (alle neun, erste Falte **2019**) gegen
> `research/krypto_historie/daten/faltenplan_nach_tb34.json`
> (`mindesttraining: 4`, nur Krypto, erste Falte **2022**). ⚠️ **Die 2022 im
> Registertext 17.3 stammt aus dem zweiten — und widerspricht damit Abschnitt
> 15.6 des Registers selbst.** ⭐ **Solange T34.10 offen ist, trägt das Register
> eine Zahl aus einem Plan, der nicht der registrierte ist.** **Vor dem
> signierten Tag.**

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K1j** | ⚠️ **Buchstaben (a)(b)(c) doppelt belegt** — Register gegen Code, siehe **T49.12** |
| **K1k** | ⚠️ **Irreführende Fehlermeldung** in `test_stabile_sortierung.py` und `test_wellenauswahl.py`, siehe **T49.13** — gehört zu T45.6 |
| **K1l** | **Verwechselbare Ausgabe** in `shared/test_umstellungstag.py`, siehe **T49.14** |
| **K1m** | ⚠️ **`ERSTE_MOEGLICHE_FALTE = 2019` — steht diese Schranke im Register?** Siehe **T49.8**. *Nicht nachgesehen* |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — entfernte Zeilen **nur**
   aus der einen Ersetzung (zwei Kettenzeilen), jede zugeordnet.
2. `git branch --show-current && git status --short` **vor** dem Commit.
3. `git add` + `commit` + `push` **in einem Zug**.
