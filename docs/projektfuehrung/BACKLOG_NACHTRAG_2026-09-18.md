# Backlog-Nachtrag 18.09.2026

> ⚠️ EINGEARBEITET am 18.09.2026 in `docs/projektfuehrung/BACKLOG.md`, Commit 02de1f7.
> Dieses Dokument bleibt als Beleg des Nachtrags stehen und wird nicht
> mehr fortgeschrieben.

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
**Umfasst: TB-46 Merge · TB-46b · zwei Fable-Runden · TB-47 · Registereintrag
`rand_erste` · TB-48 · TB-49 (formuliert).**

> ⚠️ **Nichts wird entfernt.** Drei neue Blöcke, zwei benannte Ersetzungen.
> Die Prüfung nach dem Einfügen: `git diff --numstat` muss **0 entfernte
> Zeilen** zeigen — dieselbe Regel wie beim Register.

---

## Ersetzung 1 — die Kopfzeile

**Zu finden (Zeile 3 der Datei):**

```
**Stand: 17.09.2026.** Nur **aktive Punkte**. Alles Abgeschlossene steht im
```

**Zu ersetzen durch:**

```
**Stand: 18.09.2026.** Nur **aktive Punkte**. Alles Abgeschlossene steht im
```

---

## Ersetzung 2 — die Kette in Abschnitt 3

**Die Zeilen der Ränge 0,5 bis 0,95 sind überholt.** Vier davon sind erledigt.
**Zu ersetzen: der Tabellenblock von `| 0,5 |` bis `| 0,95 |` durch:**

| Rang | Schritt | Stand |
|---:|---|---|
| ~~0,5~~ | ~~Krypto-Historie (V2)~~ | **ERLEDIGT** — TB-34 Cloud und Mac-Lauf, Datenstand `d9449faf…`/223 |
| ~~0,6~~ | ~~T46.1 — die Ausstiegspfade prüfen~~ | ⭐ **ERLEDIGT 18.09. durch TB-46b (`c5ad722`). KEIN Bot schliesst eine Position bei fehlenden Kursdaten** — strukturell unmöglich, nicht nur unbeobachtet. Siehe Block **2e** |
| ~~0,7~~ | ~~TB-46 Erhebung + Snapshot-Werkzeug~~ | **ERLEDIGT, gemergt `135c306`** |
| ~~0,8~~ | ~~TB-47 Snapshotgrenze~~ | **TEILWEISE ERLEDIGT, gemergt `a1e7fb4`** — Snapshot-Grenze, zwei Hashes, Teilkerzen-Prüfung, Prozessgruppe. ⚠️ **Der eigentliche Umbau der 90 Module steht noch aus** und ist jetzt Rang **0,85**. Siehe Block **2f** |
| ~~0,9~~ | ~~Registernachtrag~~ | **ERLEDIGT durch TB-48, gemergt `db8913a`** — Abschnitt 17, `506 0`. Siehe Block **2g** |
| **0,82** | ⭐ **TB-49 — die Ausnahme ins Werkzeug, der Prüfer ins Repo** | **formuliert 18.09.**, `CLOUD_TB-49_ausnahme_ins_werkzeug.md`. **Der letzte Schritt vor dem Snapshot** |
| **0,84** | **Snapshot ziehen** | ⚠️ **erst nach TB-49** — das Werkzeug verweigert heute bei allen 36 Befunden |
| **0,85** | ⭐ **Der grosse Umbau:** 90 Module der Selektionsseite auf den Snapshot · **Resolver-Modus in `shared/paths.py` als eigener kleiner Schritt mit Mac-Lauf** · **zwei AST-Tests** (kein eigener Datenpfad · **keine Wanduhr**) · **Lese-Audit** · Cache nach **Snapshot-Hash UND Commit** | zu formulieren nach dem Snapshot |
| **0,87** | ⚠️ **In einem Zug, braucht die Freigabe für `shared/entscheidungskerze.py`:** Gleichheitsprüfung aller Quellen · Datencron mit Prüfung vor den Bot-Läufen (**`TZ=UTC`**) · **Kein-Entscheid-Datensatz** in `melde()` · Datenstand-Hash und Kerzenwerte je Lauf ins Protokoll | Block **2e**, Betreiberfreigabe offen |
| **0,95** | **`auswertung.py` auf Verfahren B** | zu formulieren |

---

## Neuer Block 2e — aus TB-46b und der Fable-Runde zum Datencron

**Einzufügen NACH Block „2d — Aus TB-46 und den beiden Fable-Runden".**

---

### 2e — Aus TB-46b, TB-47 und den Fable-Runden (Stand 18.09.2026)

**TB-46b ist erledigt — Cloud und Mac-Lauf, gemergt `c5ad722`.**
**Der Sicherheitspunkt T46.1 ist beantwortet, und die Antwort ist die
beruhigende.**

#### Die Antwort auf T46.1, in einem Satz

> ⭐⭐⭐ **KEIN Bot schliesst eine Position, weil Kursdaten fehlen. Nicht
> „wurde nicht beobachtet", sondern strukturell unmöglich — an neun von neun
> Bots über fünf Ausstiegspfade gelesen.**

**Die gemeinsame Bauform aller neun:**

```
__main__          für jedes Symbol:  df = entscheidungskerze.lade(...)
                                     → in price_data / indicator_data
                  alles in einem try/except Exception je Symbol

check_open_trades  für jeden offenen Trade:
                     if symbol not in <daten>:  continue     ← die Tür
                     future = df[df["open_time"] > entry_time]
                     nur bei Treffer:  UPDATE ... status='closed'
```

⭐ **Es gibt kein `else`.** Ein Symbol ohne Kursdaten erreicht die UPDATE-Zeile
strukturell nicht. **Fables Befürchtung — *„ein Bot, der bei fehlender Kerze
verkauft, hat kein Holdout-Problem, sondern ein Sicherheitsproblem"* — trifft
hier nicht ein.**

| # | Punkt |
|---|---|
| **T46b.1** | ⚠️⚠️ **DER OFFENE PUNKT, der aus der Prüfung entstand: der Rückfall auf die zweite Quelle wird NICHT auf Frische geprüft.** `shared/entscheidungskerze.py`, `lade()`: `_aus_datei()` fragt `ist_frisch()` (Zeile 690) — **`abruf()` (Zeile 663) fragt niemand.** Fällt ein Bot auf den Live-Abruf zurück und liefert dieser eine veraltete oder unvollständige Kerze, **entscheidet der Bot darauf, ohne dass es auffällt**. ⚠️ **Das ist der einzige Weg, auf dem eine falsche Kerze bis zur Entscheidung kommt** |
| **T46b.2** | ⭐⭐ **FABLES ANTWORT (18.09.): GLEICHHEITSPRÜFUNG statt Frischeprüfung.** Nicht *„ist die Kerze frisch genug"* (das braucht eine willkürliche Toleranz), sondern: **der `close_time` der gelieferten Kerze muss dem erwarteten Wert GLEICHEN — aus jeder Quelle, ohne Ausnahme.** Stimmt er nicht, ist es ein **Kein-Entscheid**, kein Notbehelf. ⭐ *„Die Gleichheit braucht keinen Parameter. Eine Toleranz wäre eine zweite willkürliche Zahl an genau der Stelle, an der das Register keine mehr verträgt."* **Angenommen — mein eigener Vorschlag (Frischeprüfung) ist damit verworfen** |
| **T46b.3** | ⚠️ **Die Bündelung, die daraus folgt — und sie braucht die Betreiberfreigabe für `shared/entscheidungskerze.py`:** **(1)** Gleichheitsprüfung auf **allen** Quellen · **(2)** Datencron mit Prüfung **vor** den Bot-Läufen, **`TZ=UTC`** · **(3)** **Kein-Entscheid-Datensatz** in `melde()` statt Fehlerzeilen je Symbol · **(4)** Datenstand-Hash und Kerzenwerte **je Lauf** ins Protokoll. ⚠️ **In EINEM Zug, weil jede Einzeländerung an dieser Datei das Objekt bewegt, gegen das Registertext 7 den Backtest vergleicht** |
| **T46b.4** | ⚠️ **SNAPSHOT VOR DATENCRON — bestätigt.** Läuft der Cron zuerst, ändert sich `data/` täglich und der Registerprüfer meldet **jeden Tag ABWEICHUNG**; die Alternative („erwartet abweichend" führen) wäre ein Alarm, an den man sich gewöhnt (Prüfprinzip **A4**). **Der Cron hat vor dem Tag keine Eile** |
| **T46b.5** | ⚠️ **`Ladeprotokoll.melde()` wird im Papierpfad NIE aufgerufen.** Der gemeinsame Baustein aus TB-42 existiert, und der Betriebspfad benutzt ihn an dieser Stelle nicht. **Gehört in dieselbe Bündelung wie T46b.3** |
| **T46b.6** | ⭐ **EINE der neun Datenbanken wich im Mac-Lauf ab — und die Erklärung ist belegt, nicht plausibilisiert.** `turtle_soup_crypto` hat einen Cronjob `15 0 * * *`; die Änderungszeit 00:15:24 Ortszeit = **22:15:24 UTC** liegt im Prüffenster, und der sqlite-Inhaltsunterschied deckt sich **Zeile für Zeile** mit der Logzeile desselben Laufs. ⭐ **Daraus die neue Regel in `ARBEITSWEISE.md` §7:** Cron-Abweichungen werden **gegen den Crontab-Eintrag desselben Bots** geprüft, nicht von Hand |
| **T46b.7** | **Nebenbefund, klein und offen:** `target_price` kann in `strategies/elliott_wave/forward_test.py:129` `None` sein — ohne Schutz. ⚠️ Berührt `forward_test.py`, also freigabepflichtig; **berichtet, nicht behoben** |

---

## Neuer Block 2f — aus TB-47

**Einzufügen NACH Block 2e.**

---

### 2f — Aus TB-47, Snapshotgrenze (Stand 18.09.2026)

**TB-47 ist erledigt — Cloud und Mac-Lauf, gemergt `a1e7fb4`.**
⚠️ **Nicht der grosse Umbau** — die Grenze, die zwei Hashes, die
Teilkerzen-Prüfung und die Prozessgruppe. **Der Umbau der 90 Module steht als
Rang 0,85 noch aus.**

| # | Punkt |
|---|---|
| **T47.1** | ⭐⭐ **DIE SNAPSHOT-GRENZE IST GEMESSEN, nicht geschätzt: transitive Hülle über 142 Module, und es sind GENAU ZWEI Nicht-Kursdaten-Eingaben** — `config/top25_symbols.txt` und `config/sp500_top150.txt`. **Kein Handelskalender als Datei** (er kommt aus `pandas_market_calendars`, also aus dem Lock), keine weitere Konfigurationsdatei. *Die Grenze ist damit klein genug, um sie vollständig ins Manifest zu schreiben* |
| **T47.2** | ⭐⭐ **DIE ZWEI HASHES, zum ersten Mal nebeneinander gemessen** — auf dem Mac: `datenstand` = **`d9449faf…`** bei 223 Dateien, *trifft den Anker* **True**; `snapshot_hash` = **`4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608`**, *verschieden* **True**. ⚠️ **Der Snapshot-Hash läuft über die sortierten (Pfad, Inhalts-Hash)-Paare der DATEIEN, nicht über das Manifest** — sonst hinge der Name von der Metadaten-Formatierung ab. **Prüfprinzip C7: zwei Zahlen, zwei Fragen** |
| **T47.3** | ⚠️⚠️ **36 von 223 Kursdateien tragen den Befund `rand_erste`** — die **erste** Kerze deckt ihren Zeitraum nicht voll ab, weil die Historie des Symbols innerhalb der Periode beginnt. ⭐ **Die Prüfung stellt je Datei selbst fest, dass die Kerze auf die letzte Stelle das Aggregat genau der vorhandenen feineren Kerzen ist — also abgeleitet, nicht unvollständig geschrieben.** **Auf beiden Rechnern dieselben 36** (Cloud 3.11.15, Mac 3.9.6) |
| **T47.4** | ⭐ **`LETZTE Kerze betroffen: False` bei allen 223** — der Rand, der für einen Snapshot gefährlich wäre, ist sauber. *Die Kerze, in die ein Abruf mitten hineingeschrieben haben könnte, gibt es hier nicht* |
| **T47.5** | ⚠️⚠️ **UND DIE ANGABE, DIE EINE PRÜFUNG NICHT ABDECKT: 175 von 223 Dateien tragen `kein_zeuge`** — 150 Aktien und 25 Krypto-1h. Es gibt **keine feinere Datei zum Vergleich**, also ist die Abdeckung der Randkerzen dort **nicht belegbar**. ⚠️ **Das ist „kein Befund", nicht „geprüft" (Prüfprinzip C3).** Was dort trägt, ist `shared/abrufschutz.py` aus TB-35 — **eine andere Zusicherung.** ⚠️ **Mein Fehler: ich hatte „alle 223 sauber" weitergegeben; korrigiert an der JSON** |
| **T47.6** | ⭐ **`shared/snapshot.py` erweitert: acht Abbruchgründe, drei Rückgabewerte, Trockenlauf als Voreinstellung, kopiert nur mit `--ziehen`.** `shared/test_snapshot.py` von **69 auf 110 Prüfungen**, dreizehn Mutationsproben — **jede führt zusätzlich vor, dass eine Fassung ohne die Wache denselben Fehler übersieht** |
| **T47.7** | ⭐⭐ **PRÜFPRINZIP B4, neue Variante: eine Probe kann sich selbst SEHEN.** Die Zählung überlebender Enkelprozesse meldete **vier** — das Suchmuster stand in der eigenen Befehlszeile, also fand `ps` die eigene Shell. Nach drei immer strengeren Gegenproben: **0**. ⭐ *Die Sitzung hat nicht weitergemacht, sondern nachgesehen.* **Steht jetzt in `docs/PRUEFPRINZIPIEN.md`** |
| **T47.8** | **Prozessgruppe behoben:** `start_new_session=True` + `os.killpg`, `research/datenordner_schnitt/test_prozessgruppe.py` **11/11 mit Gegenprobe**. *Behebt T45.1 — `test_drawdown_beide_masse.py` hinterliess einen Rechenprozess, der zwanzig Minuten weiterlief, auf dem Rechner, auf dem der Betrieb läuft* |
| **T47.9** | ⚠️ **`BEKANNT_ROT` enthielt einen falschen Eintrag: `system/test_log_rotation.py` ist 117/117 GRÜN auf beiden Rechnern.** Der Eintrag stammte aus einem Lauf auf einem alten Checkout. **Gestrichen, mit Kommentar im Code:** *„Ein falscher Eintrag in dieser Liste ist teurer als gar keiner."* (Prüfprinzip **C1**) |
| **T47.10** | **Nebenwert, der jetzt gebraucht wird:** `pandas_market_calendars` **4.6.1** auf dem Mac — ⭐ **die Fassung, von der der Handelskalender kommt.** Gehört nach Registertext 5f ins `requirements.lock` und in den Registereintrag. *Ohne sie hängt das Ergebnis des Selektionslaufs an einer unbenannten Paketfassung* |
| **T47.11** | **Referenzen festgenagelt:** `shared/test_leeres_symbol.py` (45/45) und `shared/test_stille_ausfaelle.py` (27/27) prüfen jetzt gegen `BEZUGSCOMMIT = "97aea8878c9fae5e1f12d30e2ea0318dd20aadc5"` und sind **rot mit dem Vermerk NICHT PRUEFBAR**, wenn der Commit fehlt — nicht grün (Prüfprinzipien **A2** und **B3**) |

---

## Neuer Block 2g — aus TB-48 und TB-49

**Einzufügen NACH Block 2f.**

---

### 2g — Aus TB-48, Registernachtrag (Stand 18.09.2026)

**TB-48 ist erledigt — gemergt `db8913a`.**
⭐ **`git diff --numstat`: `506 0` — 506 Zeilen hinzugefügt, NULL entfernt, genau
eine Datei berührt.** Der Registerprüfer aus TB-41 läuft über alle neun
Prüfungen einschliesslich `null_entfernte_zeilen`: **kein Befund.**

| # | Punkt |
|---|---|
| **T48.1** | ⭐ **Abschnitt 17 der Vorregistrierung trägt jetzt: Registertext 5a (Snapshot-Struktur, Snapshot-Grenze, zwei Hashes), 5e (Lese-Audit als Gültigkeitsbedingung), 5f (Umgebung als dritte Achse), die zwei Ergänzungen zu Registertext 7 (Kein-Entscheid-Tag, `n ≥ 20`), den datierten Nachtrag zur Tatsachennotiz vom 15.09. und — als **17.3** — die Ausnahme `rand_erste`.** **19 Zahlen wurden an ihrer Quelle nachgerechnet, 18 stimmen** |
| **T48.2** | ⚠️⚠️ **DIE EINE ABWEICHUNG IST MEINE: „die erste Selektionsfalte beginnt 2022" — `research/faltenplan_neun/daten/faltenplan.json` sagt 2019.** ⭐ **Die Sitzung hat nicht still korrigiert, sondern als BEFUND gemeldet — und mein indirektes Argument durch eine direkte Messung ersetzt:** *„kurze erste Kerze in einer GELADENEN Falte: Soll 0, Ist 0"*, über alle neun Bots. ⭐ **Damit hängt die Schlussfolgerung nicht mehr an meiner Jahreszahl.** ⚠️ **Zu prüfen (Prüfprinzip C7): ist 2022 die früheste KRYPTO-Falte (T34.9) und 2019 die früheste über alle neun — oder ist eine der beiden Zahlen falsch? TB-49 Teil 4 misst es** |
| **T48.3** | ⚠️ **MEINE REGEL HAT DAS FALSCHE BEWIRKT.** Ich hatte verboten, unter `research/` etwas zu ändern. Die Sitzung hat sich daran gehalten — und **`pruefe_abschnitt17.py` deshalb NICHT ins Repo gelegt.** Der einzige Prüfer, der die neunzehn Zahlen nachrechnet, **existiert nur in einem ZIP.** ⭐ **Daraus `ARBEITSWEISE.md` §11 (neu): Ein Änderungsverbot nennt, wovor es schützt — und Prüfwerkzeuge, die eine Aufgabe erzeugt, gehören ausdrücklich ins Repo.** **TB-49 Teil 3 holt es nach** |
| **T48.4** | ⭐ **Der Prüfer sagt selbst, was er nicht kann:** *„ACHTUNG: dieser Prüfer kennt Abschnitt 17 NICHT."* — genau die Frage ehrlich beantwortet statt weggelassen (Prüfprinzip **C4**) |
| **T48.5** | ⚠️ **`git status` im Beleg war VOR dem letzten Commit aufgenommen — zweiter Fall nach TB-46.** Beide Male trug der Zweig die aktuellen Fassungen; **beide Male war der Beleg wertlos.** ⭐ **Daraus die Regel in `ARBEITSWEISE.md` §7: Statusausgabe nach dem letzten Commit erneut aufnehmen, und vor dem Merge `git diff --stat origin/<zweig> -- docs/ research/`** |
| **TB-49** | **FORMULIERT 18.09.2026** — `CLOUD_TB-49_ausnahme_ins_werkzeug.md`, Cloud. **Klein, drei Dinge, danach lässt sich der Snapshot ziehen.** **Teil 1:** die Ausnahme `rand_erste` in `shared/snapshot.py` — ⚠️ **als REGEL, nicht als Liste** (drei Bedingungen: Art · **erste** Kerze · nachweislich Aggregat der feineren Kerzen). **Keine Übergehen-Flagge**, die Prüfung schlägt weiter an, `rand_letzte` bricht weiter ab, das **Manifest führt die zugelassenen Befunde samt Verweis auf Registertext 5a/17.3**. **Teil 2:** `shared/test_snapshot.py` erweitern (110 bleiben), jede neue Mutationsprobe muss beissen — ⚠️ **der interessante Fall: wie verhält sich die Regel bei den 175 `kein_zeuge`-Dateien, wo Bedingung (c) nicht belegbar ist?** **Teil 3:** `pruefe_abschnitt17.py` nach `research/registernachtrag_tb48/` (T48.3). **Teil 4:** 2019 gegen 2022 messen, je Bot die früheste Falte ausgeben — **kein Registertext wird geändert**. **Teil 5:** kein Snapshot, `data/` unberührt, Sperrliste unberührt |

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

**Anzufügen an die dortige Tabelle:**

| # | Punkt |
|---|---|
| **K1a** | ⚠️ **Sechs der neun Bots überspringen ein leeres Symbol weiterhin STILL** (T45.4) — widerspricht *„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."* **Freigabepflichtig, eigene Aufgabe** |
| **K1b** | **`t3_supertrend` ist nur durch die Einrückung sicher** — `compute_indicators` bricht auf leerem Rahmen ab und überlebt nur, weil der Aufruf im `try` der Ladeschleife steht (T45.3, **D4**) |
| **K1c** | **`target_price` kann `None` sein**, `strategies/elliott_wave/forward_test.py:129` (T46b.7) |
| **K1d** | **`broker/test_ibkr.py` benutzt `US/Eastern`** — veralteter Zonenname; `America/New_York` ist der aktuelle (T46.14) |
| **K1e** | **`shared/paths.py:18` legt `data/` beim Import an** (T46.8) — harmlos heute, **still im Fehlerfall** |
| **K1f** | **Das Hash-Verfahren steht doppelt im Repo**, zeichengleich in `pruefe_register.py:319` und `herkunft.py:96` (T46.6) |
| **K1g** | **Alter `stash@{0}` auf dem Mac** aus der Frühzeit des Projekts — vor dem Snapshot ansehen und wegräumen (T45.11) |
| **K1h** | ⚠️ **`reg.KURSDATEN_DIR_VERBOTEN`** — ein Rückfallwert mit einem Namen, der etwas anderes verspricht (T46.5, **D3**) |
| **K1i** | **Zweiter Umstellungstag ins Register**, sobald sein Datum existiert: der erste Tag, an dem **alle neun** Bots ohne Rückfall aus `data/` lesen — **aus den Logs zu belegen**, nicht zu setzen |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **die zweite Zahl
   muss 0 sein**, ausser den zwei ausgewiesenen Ersetzungen (Kopfzeile: 1;
   Kettenblock: die Zeilen der Ränge 0,5–0,95).
2. `git branch --show-current && git status --short` **vor** dem Commit.
3. `git add` + `commit` + `push` **in einem Zug** (P.2).
