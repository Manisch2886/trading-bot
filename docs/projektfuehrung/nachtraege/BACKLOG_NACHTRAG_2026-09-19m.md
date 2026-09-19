# Backlog-Nachtrag 19.09.2026 (m) — TB-53b, TB-58, TB-58b und der Nachmittag

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(l) voraus.** Einzufügen als **Block 2s**, nach Block 2r.
⭐ **Dieser Nachtrag nennt keine konkreten Kettennummern** (K2i) — die vergibt
die ausführende Sitzung nach Messung.

---

### 2s — Der Resolver ist fertig, und das Register kennt Codeherkunft und Lock

| # | Punkt |
|---|---|
| **T53.1** | ⭐⭐ **TB-53a, rein lesend und ohne Sitzung gemessen: der Engpass ist EINE Datei, nicht 90 Module.** Von den 90 Selektionsmodulen (`rolle == "Selektion/Backtest"`, TB-46) erreichen **71 direkt** und **19 über `multi_symbol_optimise`** die Funktion `get_strategy_paths()`. ⭐ **Module mit eigenem `data`-Pfad: 0 von 90.** Module über `shared/paths.py`: 0 von 90. ⇒ ⚠️ **Die Backlog-Beschreibung „der grosse Umbau: 90 Selektionsmodule" (Rang 0,85) ist falsch — Berichtigung nötig** |
| **T53.2** | ⭐⭐ **DIE SPERRLISTE MUSSTE NICHT ANGEFASST WERDEN.** Alle neun `multi_symbol_optimise.py` nehmen `_P = get_strategy_paths(__file__)` und `DATA_DIR = _P["DATA_DIR"]` — **sie bauen keinen Pfad, sie bekommen einen.** Suche nach eigenem Pfadbau in `multi_symbol_optimise.py` und `multi_symbol_walk_forward.py`: **nichts** |
| **T53.3** | ⭐ **TB-53b ausgeführt** (`29016cf`): `get_strategy_paths()` bezieht `DATA_DIR` und `CONFIG_DIR` aus `shared/paths.py` statt sie selbst zu bauen — **eine Umsetzung des Resolvers, nicht zwei** (gegen T55.8/T54.3). Gemessen: **63 Pfade ohne Modus zeichengleich** · **9/9 unter Modus in der Snapshot-Wurzel** · falscher Hash wirft (9/9, rc 1) · `LIVE_DATA_DIR` wirft · Sperrklinken 6/29 · Basislauf UNERWARTET 0 · **23 neue Proben, gegen die alte Fassung 14 rot** |
| **T53.4** | ⚠️⚠️ **EINE WÖRTLICHE ZUSICHERUNG HÄTTE EIN LEGITIMES MUSTER VERBOTEN.** Die geforderte Prüfung „Wurzel des Aufrufers == Wurzel des Resolvers" machte **vier grüne Tests rot**: `test_determinismus`, `test_ladeprotokoll` und `test_wellenauswahl` laden **absichtlich** eine Bot-Kopie aus einem Wegwerfbaum mit der **echten `shared/`**. ⭐ **Gewählt (Betreiberentscheidung nach T55b.5): Nachbar-Prüfung per `realpath`** — das antwortende `paths.py` muss physisch neben `strategy_paths.py` liegen; die Wurzelgleichheit der neun Bots misst Probe E1 bei jedem Testlauf. ⚠️ **Mutation ohne die Prüfung liefert STILL einen Pfad aus einem fremden Baum (E5)** |
| **T58.1** | ⭐⭐ **FABLES BEFUND, der TB-58 ausgelöst hat:** *„Der Lese-Audit beweist, welche DATEN gelesen wurden. Er sagt nichts darüber, welcher CODE gelesen hat."* ⚠️ **Ein Lauf mit gespaltenem Baum hätte ein sauberes Lese-Audit und wäre trotzdem nicht reproduzierbar** — kein einzelner Commit beschriebe den gelaufenen Code. ⇒ **Codeherkunft neben Datenherkunft, und der Lock als dritte Achse** |
| **T58.2** | ⭐⭐ **FABLES DREI FÄLLE statt unserer zwei.** Nicht „Quelltext oder Messung", sondern: **Probe im Testlauf** (genügt nicht — ein Selektionslauf ist kein Testlauf) · **Messung im Lauf, berichtet** (genügt allein nicht — belegt den Zustand, verhindert ihn nicht) · ⭐ **Messung im Lauf, BLOCKIEREND, ins Audit geschrieben — das IST die Zusicherung.** *„Der Lauf prüft sich selbst, oder etwas anderes prüft ihn gelegentlich. Für ein Register zählt nur das Erste"* |
| **T58.3** | ⭐ **TB-58 ausgeführt** (`d852bce`, `6518e41`). **`requirements.lock`: SHA-256 `96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`**, **67 Pakete**, `pandas==2.3.3`, `numpy==2.0.2`, `pandas-market-calendars==4.6.1`; Interpreter `3.9.6 (Clang 17.0.0)`, Plattform `macOS-15.7.9-x86_64-i386-64bit`, Maschine `x86_64`. ⭐⭐ **Drei unabhängige Wege — `pip freeze --all`, `dist-info`, `importlib.metadata` — null Unterschiede** |
| **T58.4** | ⭐⭐ **„OHNE MODUS PASSIERT NICHTS" IST DREIFACH BELEGT, nicht behauptet.** **N1:** eine zählende Attrappe ersetzt `subprocess`, `importlib.metadata` und `os.system` **vor** dem Import → **0/0/0**; mit eingebauter Mutation **2/2** — die Probe beisst. **N3:** am Syntaxbaum kein Modulimport von `subprocess`/`importlib`/`platform`/`hashlib` (B5). **N4:** **144 Pfade über neun Bots zeichengleich** gegen den Vorgänger-Commit |
| **T58.5** | ⭐ **Fünf Abbruchproben, jede beisst einzeln, jede geht ohne ihre Prüfung durch:** falscher Commit · fehlende `TB_SELEKTIONSCOMMIT` · **gespaltener Baum** · **schmutziger Arbeitsbaum** · verfälschte Lock-Zeile. **44/44** in `shared/test_startpruefungen.py`, **9/9** gegen den echten Arbeitsbaum. ⭐ **Dritte Umgebungsvariable `TB_SELEKTIONSCOMMIT`** — dieselbe Bauart wie der Snapshot-Hash: der Modus **trägt** den erwarteten Wert |
| **T58.6** | ⚠️ **ABWEICHUNG, gefragt und freigegeben:** Teil B wörtlich machte **18/24** Proben in `test_paths.py` und **18/23** in `test_strategy_paths.py` rot — sie setzen nur zwei Variablen, starten mit `python -c` (**kein `__file__`**) und legen `paths.py` in einen Ordner ohne Git. ⭐ **Freigabe auf die AUFRUFUMGEBUNG beider Dateien erweitert — nicht auf ihre Zusicherungen.** *Geändert wurde, WIE die Tests aufrufen, nicht WAS sie behaupten* |
| **T58b.1** | ⭐⭐ **DAS REGISTER KENNT JETZT CODEHERKUNFT UND LOCK.** **Abschnitt 19** (Registertext 5e, Ergänzung Codeherkunft — **Entscheidung** nach F17) und **Abschnitt 20** (Tatsachennotiz zu 5f — der Lock), Commit **`409d71d`**, **160 Zeilen hinzu / 0 entfernt**. ⭐ **Das Wegwerfbaum-Muster ist im Register als Testtechnik benannt und im Selektionsmodus ausdrücklich unzulässig** |
| **T58b.2** | ⭐⭐ **DIE PROBE, DIE DEN EINTRAG WAHR MACHT:** Nach dem Commit ein Lauf unter dem Modus mit **`pandas==0.0.1`** im Lock, Baum sauber → **rc 2**, Meldung nennt das Paket. *Ein Registertext, den der Code nicht einhält, wäre schlimmer als keiner* |
| **T58b.3** | ⭐ **Belege und Aufträge sind ab jetzt im Repo** (`be6e72c`): `docs/belege/TB-58/` (25 Dateien, 8 byteweise Duplikate weggelassen, mit `HERKUNFT.md`), `docs/belege/TB-58b/`, `docs/auftraege/TB-58.md` und `TB-58b.md`. ⚠️ **Keine ZIP mehr** — Begründung T54.5 |

---

### 2s (Fortsetzung) — was der Nachmittag über unsere Arbeitsweise ergab

| # | Punkt |
|---|---|
| **B1** | ⭐⭐ **F1b/Q2 IST FÜR DIE DATEN BELEGT, NICHT FÜR DEN LAUF — Berichtigung einer eigenen Aussage.** Ein frischer Klon auf einer dritten Umgebung (Linux, Python 3.11.15) rechnete gegen den committeten Snapshot: `UNVERAENDERT`, beide Hashes gleich; Datenstand aus dem geklonten `data/` ebenfalls `d9449faf…`/223. ⚠️ **Das beweist den Snapshot** (SHA-256 über Dateiinhalte ist von pandas unabhängig), ⚠️⚠️ **nicht den Lauf** — den entscheiden pandas und numpy. **Fable: „Für den Lauf ist der Reproduktionstest noch nicht möglich, weil der Lock fehlt, gegen den er zu laufen hätte"** — der Lock existiert seit `d852bce` |
| **B2** | ⚠️⚠️ **DIE CLOUD FÄLLT ALS ZWEITE MASCHINE FÜR DIE LAUFREPRODUKTION AUS.** Gemessen: die Cloud-Umgebung hat Python **3.10, 3.11, 3.12, 3.13**, **kein 3.9**, kein `pyenv`. Der Lock schreibt **3.9.6 mit pandas 2.3.3** fest. ⭐ **Verbleibend: ein frischer Klon auf demselben Mac mit demselben Lock** — das belegt Reproduzierbarkeit aus dem Repo, **nicht Maschinenunabhängigkeit.** ⚠️ **Offene Frage an Fable** |
| **B3** | ⭐ **Die Sperre gegen den zweiten Snapshot greift auch im Wegwerf-Klon** — rc **2**: *„Ein bestehender Snapshot wird NIE überschrieben."* **Der Schutz sitzt im Code, nicht in der Umgebung** |
| **B4** | ⚠️⚠️ **macOS SCHÜTZT `~/Downloads` — Claude-Code-Sitzungen können dort NICHT lesen** (`Operation not permitted`, per Read-Werkzeug **und** per Shell, auch ausserhalb der Sandbox). ⭐ **Das hat drei Sitzungsstarts gekostet, bis eine Sitzung die Ursache benannte.** ⇒ **Aufträge liegen ab sofort in `logs/auftraege/` im Projektordner** — gitignoriert, kein Ordnerschutz, erscheint nicht in `git status` |
| **B5** | ⭐⭐ **DAS PROJEKT IST SEIT HEUTE ORTSUNABHÄNGIG.** Ursache der bisherigen Sperre: Claude Code legt seine Anmeldung im **macOS-Schlüsselbund** ab, der in einer SSH-Sitzung nicht entsperrt ist — die Sitzung fiel auf „API Usage Billing / Not logged in" zurück. ⭐ **`security unlock-keychain` (ohne `-p`, Eingabeaufforderung) behebt es**; danach meldet die Kopfzeile `Claude Max`. ⚠️ **Kein Passwort in einer Datei, einem Skript oder einer Variablen** |
| **B6** | ⚠️ **Zwei Werkzeugfehler des Betreuers, beide folgenreich:** (1) **Ein Überschreiben über die Geräteverbindung meldete Erfolg und änderte nichts** — die Auftragsdatei blieb die alte Fassung. ⇒ ⭐ **Regel: nie überschreiben, immer neuer Dateiname, danach mit `grep` gegenprüfen.** (2) **Ein `git status` über die Verbindung hinterliess eine verwaiste `.git/index.lock`**, weil die Verbindung nicht löschen darf. ⇒ ⭐ **Regel: über die Geräteverbindung kein `git status`, kein `git log` — nur reines Dateilesen** |
| **B7** | ⭐ **Vorprüfung vor die Sitzung, nicht in sie** (K2b, bestätigt): Die dist-info-Ordner unter `trading-env/lib/python3.9/site-packages` sind **ohne jede Ausführung lesbar** — daraus entstand der Lock-Entwurf ausserhalb der Sitzung, und **aus „erzeugen" wurde „gegenprüfen"**. ⭐⭐ *Eine Datei aus einer Quelle ist eine Behauptung; eine, bei der zwei unabhängige Wege dasselbe sagen, ist eine Messung* |

---

## Berichtigung — Rang 0,85

**Zu finden** (Abschnitt 3, Rang **0,85**, „der grosse Umbau: 90 Selektionsmodule").
⚠️ **Ersetzen, alter Wortlaut bleibt darunter als ersetzt gekennzeichnet und
datiert.** Der neue Wortlaut sagt: ⭐ **kein Umbau von 90 Modulen, sondern eine
Datei — gemessen am 19.09.2026 (T53.1), ausgeführt in TB-53b** (`29016cf`).

---

## Neue Kettenzeilen

⭐ **Die nächsten freien Nummern, gemessen** — dieser Nachtrag nennt keine:

```
| ⟨frei⟩ | ⭐ **Das Lese-Audit (Fables Schicht 3)** — was gelesen wurde, je Datei, gegen das Manifest. ⚠️ Die Codeherkunft ist seit TB-58 abgedeckt; hier fehlt noch die Datenseite | offen |
| ⟨frei⟩ | ⭐ **Laufreproduktion gegen den Lock** — frischer Klon, `TB_SELEKTIONSCOMMIT` gesetzt, derselbe Lock. ⚠️ Nicht in der Cloud möglich (B2) | offen |
| ⟨frei⟩ | **TB-56 — die Faltenschranke `ERSTE_MOEGLICHE_FALTE = 2019` messen und entfernen** (F14/F16), Berichtigung 17.3, Drei-Kategorien-Regel zu Registertext 0 | zu formulieren |
```

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2l** | ⚠️⚠️ **Aufträge nie nach `~/Downloads`** — macOS-Ordnerschutz sperrt Claude-Code-Sitzungen aus (B4). **`logs/auftraege/` im Projektordner** |
| **K2m** | ⭐ **Jeder Auftrag trägt `[ortsunabhängig]` oder `[Mac-pflichtig]`** — und **jeder Teil wird einzeln geprüft**, bevor „Mac-pflichtig" geschrieben wird |
| **K2n** | ⭐ **Jede Rückfrage an den Betreiber und seine Antwort kommen wörtlich in den Bericht** — sonst leben sie nur im Sitzungsverlauf, der mit der Sitzung verschwindet |
| **K2o** | ⭐ **Die Sitzung committet ihren eigenen Auftrag mit** (`docs/auftraege/`) und ihre Belege (`docs/belege/TB-xx/`). **Keine ZIP** |
| **K2p** | ⚠️ **Nie am Repo arbeiten, während eine Mac-Sitzung läuft** — die Sitzung prüft `git status` und hielte zu Recht an |
| **K2q** | ⚠️ **Über die Geräteverbindung nie überschreiben und nie `git status`/`git log`** (B6) |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte Zeilen:
   die der ersetzten Kettenzeile 0,85, sonst keine.**
2. ⚠️ **Alter Wortlaut von 0,85 als ersetzt gekennzeichnet darunter.**
3. ⭐ **Welche Kettennummern vergeben wurden, steht im Bericht** — mit der
   Messung, wie sie ermittelt wurden.
