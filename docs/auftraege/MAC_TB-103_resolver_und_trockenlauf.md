# TB-103 — Resolver-Fix, `messgroessen.py` auf den Resolver, Trockenlauf aller neun Bots im Modus

**Sitzungstitel:** `TB-103` · **Angelegt:** 24.09.2026, 23:00, vom steuernden Chat (neuer Chat nach dem Umzug)
**Grundlage:** Fable 24b A2 (Resolver, kein Fallback, Tag-Vorbedingung Trockenlauf) · Fable 24c Abschnitte 1, 2, 6 (Nachweis mit zwei Teilen, Resolver-Pflicht, Reihenfolge)
**Vorgänger:** TB-102 (`d05e3ff`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)

> **In einfacher Sprache, vorweg:** Im geschützten Modus finden die Bots ihre Symbolliste nicht und nehmen still eine Notliste mit fünf Werten. Diese Sitzung repariert die zentrale Pfadstelle, stellt ein Messprogramm auf dieselbe Stelle um und lässt danach alle neun Bots einmal probeweise im geschützten Modus laufen. Dabei wird protokolliert, woher sie lesen.

---

## ⭐⭐ Freigabe des Betreibers, wörtlich

**24.09.2026, 22:52, Auswahlkarte im steuernden Chat.** Gefragt war: *„Freigabe für den Resolver-Fix (TB-103): Dürfen shared/paths.py und messgroessen.py geändert werden? Beide stehen auf keinem Sperrlistenpunkt (gemessen, TB-98)."* Die Antwort: **„Beide freigeben (Empfohlen)"**.

| freigegeben | Umfang |
|---|---|
| `shared/paths.py` | unter dem Modus `CONFIG_DIR = <snapshot>/config`, kein Fallback, Rückgabe 2, Abbruch statt Warnung |
| `research/vorregistrierung/messgroessen.py` | Umstellung auf den Resolver |
| ⭐ dazu gehörend | die Tests **dieser beiden Module** (`shared/test_paths.py`, `shared/test_startpruefungen.py`, soweit ihre Attrappen den Snapshot nachbauen; die Prüfungen in `research/vorregistrierung/test_vorregistrierung.py`, die `messgroessen.py` betreffen) |

⛔ **Nicht freigegeben, und deshalb nicht angefasst:** `shared/symbols_config.py`, die vier `strategies/*/stocks_symbols_config.py`, `shared/ladeprotokoll.py`, `shared/strategy_paths.py`, `registerdaten.py`, `faltenplan.py`, die Zuteilung, das Register. Wenn der Fix eine dieser Dateien braucht: **nicht ändern, melden** (Abschnitt „Abbruchkriterien").

⚠️ **Die Freigabe vom 24.09., 11:25** (`faltenplan.py` und ein neues Sperrlisten-Abbild) ist **nicht** Teil dieses Auftrags. Sie bleibt unverbraucht.

---

## 0. Schritt 0

**0a — Den Arbeitsbaum des steuernden Chats committen.** Vormessung 24.09., 22:46 und 23:00:

| Datei | Stand |
|---|---|
| `docs/projektfuehrung/UMZUG.md` | geändert, 2 Zeilen (Zeiger im Eröffnungstext auf `UEBERGABE_2026-09-24.md`) |
| `docs/projektfuehrung/UEBERGABE_2026-09-24.md` | neu |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-24e_richtiges_ergebnis_falscher_ort.md` | neu |
| `docs/projektfuehrung/REGISTER_KOPIE_2026-09-24.md` | neu (552 130 Bytes) |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md` | neu, vom steuernden Chat aus der Projektablage abgelegt |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md` | ebenso |
| `docs/auftraege/MAC_TB-103_resolver_und_trockenlauf.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-103 |

⚠️ **`docs/projektfuehrung/_kopf_register_kopie_24.md` NICHT committen.** Es ist eine Hilfsdatei des steuernden Chats (Übergabe Block 8, Fehler 6). Prüfe zuerst, ob ihr Inhalt zeichengleich der Kopf von `REGISTER_KOPIE_2026-09-24.md` ist. **Wenn ja:** löschen. **Wenn nein:** liegen lassen und melden.

**0b — Registerkopie prüfen, bevor sie committet wird.** Der Text für Fables neuen Chat sagt: Die Kopie ist das Register zu Commit `d0dc890`, 7993 Zeilen, Abschnitte 0–40. Miss nach, ob der Teil **unter** dem Kopf zeichengleich zu `git show d0dc890:docs/VORREGISTRIERUNG_neuselektion.md` ist. Bei Abweichung: trotzdem committen, aber im Ergebnisdokument an erster Stelle melden, denn Fable liest diese Datei.

**0c — Nach 7c:** `find .git -name '*.lock'` → keine. HEAD am Eingang: **`d05e3ff`**. Datenstand vorher messen (Soll `d9449faf51bffaaa`). Quersummen der neun `*.db` vorher. Hashes aller Dateien, die dieser Auftrag ändern darf, **und** der gesperrten Dateien vorher (`hashes.sh` aus TB-102 als Vorlage). Sonde gegen `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json` vorher.

Belege: `docs/belege/TB-103/0_schritt0.txt`, `0b_registerkopie.txt`, `0c_hashes_vorher.txt`, `0c_sonde_vorher.txt`.

---

## Block A — Die Vormessung nachprüfen

⚠️ Alles unten ist **Vormessung** des steuernden Chats, 24.09., 22:45–23:00, `HEAD d05e3ff`. Nach `A8` misst du nach. **Wenn etwas abweicht, gilt deine Messung.**

| | zu prüfen | Vormessung |
|---|---|---|
| **A1** | `shared/paths.py`, `else`-Zweig des Moduls: unter dem Modus `DATA_DIR = _MODUS[0]` **und** `CONFIG_DIR = _MODUS[0]`, beide auf die flache Snapshot-Wurzel. Der Kopftext begründet das mit *„Die Snapshot-Wurzel ist flach: die Symbollisten … liegen dort neben den Kursdateien"* | ja. ⚠️ **Der Kopftext ist falsch** (siehe A2) und wird mit dem Fix berichtigt |
| **A2** | Im Snapshot `snapshots/63e4b6c8…/` liegen die Universumsdateien unter `config/`: `top25_symbols.txt`, `sp500_top150.txt`. Die Kursdateien liegen flach in der Wurzel | ja |
| **A3** | ⭐ **Wo der Rückfall eingebaut ist.** `shared/symbols_config.py` (`DEFAULT_SYMBOLS`, 5 Symbole, Zeile „Warnung: … Nutze Standardliste (5 Symbole)") und vier `strategies/*/stocks_symbols_config.py` (3 verschiedene Fassungen nach md5; `volatility_breakout` holt `CONFIG_DIR` über `strategy_paths.get_strategy_paths()`) | 5 Dateien |
| **A4** | ⭐⭐ **Inventar aller Rückfälle, die unter dem Modus greifen könnten.** Nicht nur Symbollisten: Fable 24b A2 sagt *„gleich welcher Art (Symbollisten, Parameter, Pfade, Schwellen)"*. Such im Laufbereich (`shared/`, `strategies/`, `research/vorregistrierung/`) nach Mustern wie `DEFAULT_`, `Standardliste`, `nicht gefunden`, `except … : return <Voreinstellung>`, `os.path.exists(…) … else`. **Nur auflisten, nichts ändern.** Je Fundstelle: Datei:Zeile, was zurückfällt, ob der Modus sie erreicht | nicht gemessen |
| **A5** | `shared/test_paths.py` Z. 256–257, Probe **B2**: `CONFIG_DIR == attrappe`, prüft also die flache Wurzel. Sie wird mit dem Fix **absichtlich rot** und wird umgeschrieben, nicht gelöscht. Dazu: Mutationsproben, die Codezeilen von `paths.py` wörtlich zitieren (Vormessung: um Z. 308, 368, 504). Welche davon trifft der Fix? | ja / zu messen |
| **A6** | `messgroessen.py` importiert **weder** `shared/paths.py` **noch** `strategy_paths.py`. Es baut Kursdaten- und Universumspfade aus `BASE_DIR` (`TB30A_BASE_DIR` oder Repo-Wurzel) + `data/` bzw. `config/`. `haltedauern()` Z. 200–218 liest `research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv` | TB-102 |
| **A7** | ⚠️ `messgroessen.py:59` `SLIPPAGE_PCT` und `GEBUEHR_PCT` sind laut Register (Sperrlistenpunkt zum Kostenmodul, 38.5/38.7) **überwachte Kopien**. Der Umbau berührt diese Zeilen **nicht** | zu messen |
| **A8** | ⭐ **Sperrlistenprüfung:** Stehen `shared/paths.py`, `shared/test_paths.py`, `shared/test_startpruefungen.py`, `research/vorregistrierung/messgroessen.py` oder `test_vorregistrierung.py` auf einem der 14 Punkte (Register Abschnitt 10, Z. 843–1050), in `herkunft.py::SPERRLISTE_DATEIEN` oder im Abbild? | TB-98: `paths.py` auf keinem Punkt. Die anderen **nicht gemessen** |

⛔ **Steht eine Datei aus A8 auf einem Sperrlistenpunkt: diese Datei nicht ändern.** Den Rest des Auftrags so weit wie möglich ausführen und melden.

Belege: `a_vormessung.txt`, `a4_rueckfaelle.txt`, `a8_sperrliste.txt`.

---

## Block B — Der Resolver-Fix in `shared/paths.py`

**B1 — `CONFIG_DIR` unter dem Modus.** `CONFIG_DIR = os.path.join(<snapshot_wurzel>, "config")`. `DATA_DIR` bleibt die flache Wurzel. Der Unterverzeichnisname steht **genau einmal** im Modul, wie `MANIFEST` und `LOCK`. Den falschen Satz im Kopftext (A1) berichtigen: **mit Datum und Verweis auf TB-98 Befund 1 und Fable 24b A2**, nicht still überschreiben.

**B2 — Kein Rückfall unter dem Modus: Abbruch mit 2.** Fable 24b A2, Registertext-Entwurf:

> *„Eine Eingabe, die im Snapshot nicht gefunden wird, ist Rückgabewert **2** (nicht prüfbar) und beendet den Lauf, bevor gerechnet wird — nach demselben Muster, mit dem `paths.py` den Live-Pfad unter dem Modus unerreichbar macht (`SystemExit`, nicht Exception)."*

⇒ Unter dem Modus prüft `paths.py` **beim Import**, dass `<snapshot>/config/` existiert und die Universumsdateien darin liegen und nicht leer sind. Fehlt eine, steht die Meldung auf `stderr` und es folgt `SystemExit(RUECKGABEWERT_STARTPRUEFUNG)`, bevor ein Aufrufer `CONFIG_DIR` benutzen kann. **Damit ist der Rückfall in den fünf Symboldateien unter dem Modus unerreichbar, ohne dass diese Dateien geändert werden** (sie sind nicht freigegeben).

⚠️ **Welche Universumsdateien geprüft werden**, entscheidest du am Befund. Entweder die beiden aus A2, als Namen genau einmal im Modul. Oder, wenn das Manifest die Dateien unter `config/` aufzählt: alle, die es dort nennt. **Begründe die Wahl im Ergebnisdokument.** Kriterium: Es gibt **einen** Ort, der die Anordnung kennt (Fable 24c Abschnitt 2), keine zweite Liste, die getrennt altert.

⛔ **Ohne Modus ändert sich nichts.** Probe A (99 Pfade über neun Bots, 0 Unterschiede) muss unverändert **0** zeigen. Kein zusätzlicher Dateizugriff ohne Modus; die Probe N1 aus `test_startpruefungen.py` (zählende Attrappe, 0/0) bleibt grün.

**B3 — Tests.**

| | Probe | Soll |
|---|---|---|
| **B2 alt** | umschreiben: `CONFIG_DIR == <attrappe>/config` | grün |
| **neu** | Modus, `config/` fehlt in der Attrappe | rc **2**, keine Zeile „Standardliste" |
| **neu** | Modus, `config/` da, eine Universumsdatei fehlt | rc **2** |
| **neu** | Modus, eine Universumsdatei leer | rc **2** |
| **neu** | Modus, alles da | rc 0, `CONFIG_DIR` endet auf `/config` |
| **Mutation** | Fix zurückgenommen (`CONFIG_DIR = _MODUS[0]`) | mindestens eine der neuen Proben **rot** |
| **Mutation** | Existenzprüfung entfernt | die Proben „fehlt" **rot** |

⭐ **Jede Mutationsprobe muss allein beissen** (Fable 24b B3): Die Gegenprobe lässt nur ihre eigene Mutation weg und ändert sonst nichts. ⭐ **Störproben in beide Richtungen** (24b C2): Eine Attrappe, bei der nichts passieren darf, und eine, bei der etwas passieren muss.

**B4 — Die ganze Testlandschaft danach:** `shared/test_paths.py`, `shared/test_startpruefungen.py`, `shared/test_strategy_paths.py`, `shared/test_stille_ausfaelle.py` und der Test, der seit TB-92/TB-94 **188/188** zeigt. Alles grün bis auf Proben, die du in B3 absichtlich umgeschrieben hast. **Jede Zahl mit Namen**: welche Proben neu sind, welche umgeschrieben (Fable 24b B2: *„Namen ins Register, nicht die Zahl"*).

**Commit (2):** Fix und Tests, `paths.py`. Erst **danach** laufen C3 und D, denn `TB_SELEKTIONSCOMMIT` verlangt einen sauberen Arbeitsbaum über `shared/`, `strategies/` und den Lock, und HEAD muss der Fix-Commit sein.

Belege: `b_proben.txt`, `b_mutationen.txt`, `b4_tests.txt`, `b_probe_a.txt`.

---

## Block C — `messgroessen.py` auf den Resolver (Fable 24c Abschnitt 2)

**C1 — Umbau.** Kursdaten über `DATA_DIR`, Universumsdateien über `CONFIG_DIR`, beide aus dem Resolver. Fable nennt `shared/paths.py::get_strategy_paths()`; gemessen liegt `get_strategy_paths` in `shared/strategy_paths.py` und reicht `paths.DATA_DIR`/`paths.CONFIG_DIR` durch. **Nimm den Weg, den die Bots nehmen**, und benenne im Ergebnisdokument die Abweichung in Fables Funktionsangabe.

| | |
|---|---|
| `TB30A_BASE_DIR` | bleibt als Ersatz der **Repo-Wurzel für Mutationsproben**. ⛔ **Kein Weg zum Snapshot** mehr; Kommentar und Hilfetext sagen das |
| `haltedauern_je_bot.csv` | ⚠️ **Quelle bleibt in diesem Auftrag unverändert.** Die neuen Listen aus dem Signalpfad (24b A3, 24c Abschnitt 4) gibt es noch nicht, das ist Plan-Punkt 3. ⇒ Unter dem Modus ist das **der eine erwartete Zugriff ausserhalb** des Snapshots |
| `SLIPPAGE_PCT`, `GEBUEHR_PCT` | ⛔ unberührt (A7) |
| Schreibsperre nach 36.1 (TB-93) | ⛔ unberührt; `--ziel` weiterhin Pflicht, nichts nach `ergebnisse/` |

**C2 — Ohne Modus, bytegleich.** Lauf in den **Scratchpad**. `diff` gegen `messgroessen_2026-09-23_nachweis.json` (`7f46d5f5…`) **und** gegen den Lauf mit dem Code vor C1. Soll: bytegleich. ⚠️ Weicht es ab: **Ursache ausmessen, nicht wegrechnen.** Die Datei erst einfrieren, wenn die Ursache bekannt ist.

**C3 — Im Modus, mit Lesehaken** (`TB_SELEKTIONSWURZEL`, `…HASH`, `…COMMIT`, Haken aus `docs/belege/TB-95/haken/sitecustomize.py` bzw. `TB-102/lesequellen.py`). Lauf in den Scratchpad. Gemeldet werden **beide Teile nach Fable 24c Abschnitt 1**:

| Teil | Soll |
|---|---|
| **(b) Leseprotokoll** | Kursdateien und Universumsdateien **alle** aus `snapshots/63e4b6c8…/`, **0** aus `data/` und `config/`. Genau **ein** Zugriff ausserhalb: `haltedauern_je_bot.csv`. Jede weitere Datei ausserhalb ist ein **Befund** |
| **(a) Ergebnisvergleich** | `diff` gegen die Nachweisdatei, zweimal (23e) |

⛔ **Der Nachweis für `messgroessen.json` gilt danach NICHT als geführt**, gleich was (a) zeigt. Teil (b) enthält einen Zugriff ausserhalb, also ist er nach 24c **2**. So wird es im Ergebnisdokument genannt. Geführt werden kann er erst nach Plan-Punkt 3.

**C4 — Tests.** Die Prüfungen in `test_vorregistrierung.py`, die `messgroessen.py` betreffen (u. a. `G8`, prüft `max_tage`), grün. ⭐ Zusätzlich eine Probe: **Im Modus liest `messgroessen.py` keine einzige Kursdatei aus `data/`.** Dazu die Mutationsprobe „Resolver-Import entfernt" → rot.

**Commit (3):** `messgroessen.py` und Tests.

Belege: `c1_umbau.txt`, `c2_ohne_modus.txt`, `c3_modus_lesequellen.txt`, `c3_zweimal.txt`, `c4_tests.txt`.

---

## Block D — ⭐⭐ Trockenlauf aller neun Bots im Modus (Tag-Vorbedingung, Fable 24b A2)

> *„Vor dem Tag läuft für **alle neun Bots** ein Trockenlauf im Selektionsmodus gegen den echten Snapshot, mit Lesehaken und Aufrufstapel: 0 Zugriffe ausserhalb `snapshots/<hash>/`; geladene Symbolmenge gleich Universumsdatei; kein Fallback; Rückgabe 0. Das Protokoll ist Tatsachennotiz."*

**Wie:** derselbe Lauf-Typ wie TB-98 `a1_neun.sh` (`TB_SELEKTIONSWURZEL`, **kein** Hilfsordner). Mit Lesehaken und Aufrufstapel. ⛔ Nichts nach `ergebnisse/`, `data/`, `config/`; Ausgaben nur in den Scratchpad.

**Je Bot eine Zeile:**

| Spalte | |
|---|---|
| rc | Soll 0 |
| Universumsdatei | Name, Anzahl Zeilen im Snapshot |
| Symbolmenge nach dem Laden | Anzahl; bei Krypto nach `EXCLUDE_SYMBOLS` |
| gleich Universumsdatei? | ja/nein. **Nein** heisst: Differenz mit Grund aus dem Ladeprotokoll (z. B. fehlende Kursdatei), nicht wegerklären |
| Zeile „Standardliste" | Soll **0** |
| Summenzeile des Ladeprotokolls | wörtlich |
| Lesezugriffe ausserhalb `snapshots/63e4b6c8…/` | Soll **0**; jeder Treffer mit Datei und Aufrufstapel. ⚠️ Code-Importe aus dem Repo (`.py`, `.pyc`) sind **Code**, nicht Daten; getrennt zählen, nicht mischen |

⭐ **Gegenprobe ohne Modus**, dieselbe Tabelle. TB-98 hat ohne Modus Krypto 18/24 bzw. 20/24 und Aktien 147/150 gemessen. **Vergleiche die geladene Menge mit und ohne Modus. Gleich heisst: der Tagblocker ist weg.**

⚠️ **Das Ladeprotokoll:** Fable 24b A2 verlangt, dass es *„beide Zahlen und die Quelle der Liste"* nennt. `shared/ladeprotokoll.py` ist **nicht freigegeben**. ⇒ **Nur messen:** Nennt die Summenzeile unter dem Modus beide Zahlen? Nennt sie die Quelle? Ergebnis in „Für die Folgesitzung".

⛔ **Sichtschutz 27.1:** Kein Bot-Ergebnis melden, keine Kennzahl, keine Trade-Zahl. Gemeldet werden rc, Mengen, Quellen und Zugriffe, nicht was gerechnet wurde. Schreibt ein Bot Kennzahlen auf `stdout`, **ins Beleg-Rohprotokoll damit, nicht ins Ergebnisdokument** (`belege/` ist für Fable gesperrt).

Belege: `d_neun_modus.txt`, `d_neun_ohne_modus.txt`, `d_lesequellen/`, `d_lauf.sh`.

---

## Block E — Abgabe

| | |
|---|---|
| **E1** | Hashes nachher. Geändert haben dürfen sich **nur** `shared/paths.py`, die Tests aus der Freigabe-Tabelle, `research/vorregistrierung/messgroessen.py` und `docs/`. ⛔ Alles andere gleich. `messgroessen.json` und die Nachweisdatei unverändert. In `ergebnisse/` nichts Neues. Datenstand nachher = vorher. Quersummen der `*.db` nachher = vorher |
| **E2** | Sonde gegen das Abbild nachher. ⚠️ Der Befund ist **gleich wie vorher**; eine neue Meldung wegen einer der freigegebenen Dateien ist zu erklären, nicht zu unterdrücken |
| **E3** | Ergebnisdokument `docs/ERGEBNIS_TB-103_resolver_und_trockenlauf.md` |
| **E4** | ⭐⭐ **Abschnitt „Für Fable"**, ohne Kontext lesbar, Sichtschutz 27.1: (1) Resolver-Fix, Probenamen, Mutationen. (2) Die Tabelle aus Block D ohne Ergebnisgrössen, und ob die Tag-Vorbedingung aus 24b A2 **erfüllt** ist. (3) `messgroessen.py` im Modus: Teil (b) mit genau dem einen Zugriff ausserhalb, Status **2** nach 24c. (4) Das Rückfall-Inventar aus A4, und welche Rückfälle der Modus jetzt noch erreicht. (5) Die Abweichung „`get_strategy_paths()` liegt in `strategy_paths.py`, nicht in `paths.py`" als Messung zu seiner Resolver-Pflicht |
| **E5** | „Für die Folgesitzung vorbereitet": Ladeprotokoll (D), Rückfälle mit eigener Freigabe (A4), Register 41/42-Stoff |
| **E6** | „In einfacher Sprache" · Journalblock · `git --no-optional-locks status --porcelain` **nach** dem letzten Commit, leer |

**Commits:** (1) Schritt 0 · (2) `paths.py` + Tests · (3) `messgroessen.py` + Tests · (4) Belege und Ergebnis. Nach jedem fertigen Teil pushen (7c).

---

## ⚠️ Abbruchkriterien

1. Eine Datei aus A8 steht auf einem Sperrlistenpunkt → diese Datei nicht ändern, Rest ausführen, melden.
2. Ohne Modus ändert sich ein Pfad (Probe A ≠ 0) → Fix zurücknehmen, melden. **Der Cron importiert `paths.py`.**
3. Eine Datei ausserhalb der Freigabe ändert ihren Hash, oder in `ergebnisse/` entsteht etwas.
4. Der Fix bräuchte eine Änderung an einer nicht freigegebenen Datei (Symboldateien, `ladeprotokoll.py`, `strategy_paths.py`) → nicht ändern, genau benennen, was und warum.
5. ⭐ **Block D zeigt rc ≠ 0 oder einen Zugriff ausserhalb:** Das ist ein **Ergebnis**, kein Abbruch. Block D zu Ende führen, alles melden, abgeben.

---

## ⛔ Was NICHT geschieht

| | |
|---|---|
| ⛔ | Kein Registertext. Register 41/42 ist ein eigener Auftrag |
| ⛔ | Keine neuen Handelslisten, kein Erzeuger auf dem Signalpfad (Plan-Punkt 3) |
| ⛔ | Kein Sperrlisten-Abbild, keine Änderung an `faltenplan.py`. Die Freigabe von 11:25 bleibt unverbraucht |
| ⛔ | `python3 faltenplan.py` nie direkt (TB-83) |
| ⛔ | Keine Änderung am Cron, an `data/`, an `config/` |
| ⛔ | Kein Snapshot neu, kein Hash neu. Der Fehler liegt im Weg zum Snapshot, nicht im Snapshot (Fable 24b A2) |

---

## In einfacher Sprache

Die Bots haben einen geschützten Modus, in dem sie nur aus einem eingefrorenen Datenbestand lesen sollen. In diesem Modus findet aber keiner der neun Bots seine Liste der zu handelnden Werte: Die zentrale Pfadstelle schaut im falschen Ordner nach. Die Bots greifen dann still auf eine eingebaute Notliste mit fünf Werten zurück und melden trotzdem „nichts ausgelassen".

Diese Sitzung repariert die Pfadstelle. Fehlt künftig im geschützten Modus eine Liste, bricht der Lauf ab, statt eine Notliste zu nehmen. Ein Messprogramm, das bisher seine eigenen Pfade gebaut hat, holt sie sich danach von derselben Stelle wie die Bots.

Zum Schluss läuft jeder der neun Bots einmal probeweise im geschützten Modus. Protokolliert wird, woher er liest und wie viele Werte er geladen hat. Das ist die Probe, die vor dem Stichtag laut Verfahrensprüfer stattfinden muss und bisher nie stattgefunden hat.
