# Journal-Nachtrag 19.09.2026 (f) — der Nachmittag: Resolver fertig, Register vollständig

**Anzufügen am Ende von `docs/projektfuehrung/JOURNAL.md`, NACH Block BJ.**
⚠️ **Blockbuchstaben messen, nicht raten** — und ⚠️ **das Muster prüfen, bevor
gesucht wird**: in TB-54b traf `"Block "` nichts, und ein leerer Treffer hätte
den nächsten Buchstaben falsch gemacht.

---

## Block ⟨nächster⟩ — TB-53b: der Resolver erreicht die Selektionsseite

**19.09.2026. `main`, `eaf2572` → `29016cf`, gepusht. Python 3.9.6.**

⭐⭐ **Der Engpass war eine Datei, nicht 90 Module.** Rein lesend gemessen, ohne
Sitzung: von den 90 Selektionsmodulen erreichen **71 direkt** und **19 über
`multi_symbol_optimise`** die Funktion `get_strategy_paths()`. **Module mit
eigenem `data`-Pfad: 0 von 90.**

⭐ **Und die Sperrliste blieb unberührt:** Alle neun `multi_symbol_optimise.py`
nehmen `DATA_DIR = _P["DATA_DIR"]` — **sie bauen keinen Pfad, sie bekommen
einen.**

### ⚠️⚠️ Eine wörtliche Zusicherung hätte ein legitimes Muster verboten

Die geforderte Prüfung „Wurzel des Aufrufers == Wurzel des Resolvers" machte
**vier grüne Tests rot**. Der Grund ist kein Fehler, sondern ein bewusstes
Muster: `test_determinismus`, `test_ladeprotokoll` und `test_wellenauswahl`
laden **absichtlich** eine Bot-Kopie aus einem Wegwerfbaum mit der **echten
`shared/`**.

⭐ **Die Sitzung fuhr den Basislauf, bevor sie committete, setzte den
Arbeitsbaum währenddessen auf `HEAD` zurück, damit der Cron nichts Ungeprüftes
sah — und fragte, statt zu entscheiden.** Gewählt: **Nachbar-Prüfung per
`realpath`**; die Wurzelgleichheit der neun Bots misst Probe E1 bei jedem Lauf.

---

## Block ⟨danach⟩ — TB-58: Codeherkunft und Lock

**19.09.2026. `624853b` → `d852bce` (Lock) → `6518e41` (Startprüfungen).**

> ⭐⭐ **Fables Satz, der die Aufgabe ausgelöst hat:** *„Der Lese-Audit beweist,
> welche **Daten** gelesen wurden. Er sagt nichts darüber, welcher **Code**
> gelesen hat."*

⚠️ **Ein Lauf mit gespaltenem Baum hätte ein sauberes Lese-Audit und wäre
trotzdem nicht reproduzierbar.**

### Der Lock

```
SHA-256      96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5
67 Pakete    pandas==2.3.3 · numpy==2.0.2 · pandas-market-calendars==4.6.1
Interpreter  3.9.6 (Clang 17.0.0)
Plattform    macOS-15.7.9-x86_64-i386-64bit · x86_64
```

⭐⭐ **Drei unabhängige Wege — `pip freeze --all`, `dist-info`,
`importlib.metadata` — null Unterschiede.** *Der Entwurf entstand ausserhalb
der Sitzung aus den dist-info-Ordnern; aus „erzeugen" wurde dadurch
„gegenprüfen".*

### ⭐⭐ „Ohne Modus passiert nichts" — dreifach belegt

| | |
|---|---|
| **N1** | Eine **zählende Attrappe** ersetzt `subprocess`, `importlib.metadata`, `os.system` **vor** dem Import → **0/0/0**; mit Mutation **2/2** — die Probe beisst |
| **N3** | Am Syntaxbaum: kein Modulimport von `subprocess`/`importlib`/`platform`/`hashlib` |
| **N4** | **144 Pfade über neun Bots zeichengleich** gegen den Vorgänger |

**Fünf Abbruchproben, jede beisst einzeln, jede geht ohne ihre Prüfung durch.**
44/44 neue Proben, 9/9 gegen den echten Arbeitsbaum. Sperrklinken 6/29,
Basislauf **UNERWARTET 0**.

⭐ **Dritte Umgebungsvariable `TB_SELEKTIONSCOMMIT`** — dieselbe Bauart wie der
Snapshot-Hash: **der Modus trägt den erwarteten Wert.**

⚠️ **Abweichung, gefragt und freigegeben:** Teil B wörtlich machte 18/24 und
18/23 Proben in den bestehenden Testdateien rot. ⭐ **Die Freigabe wurde auf die
Aufrufumgebung erweitert, nicht auf die Zusicherungen** — *geändert wurde, WIE
die Tests aufrufen, nicht WAS sie behaupten.*

---

## Block ⟨danach⟩ — TB-58b: Abschnitte 19 und 20

**19.09.2026. `6236c95` → `409d71d` → `be6e72c` → `02a58fb`.**

**Abschnitt 19** — Registertext 5e, Ergänzung **Codeherkunft** (Entscheidung
nach F17). **Abschnitt 20** — Tatsachennotiz zu 5f, **der Lock**.
**160 Zeilen hinzu, 0 entfernt.**

⭐ **Das Wegwerfbaum-Muster steht jetzt im Register als Testtechnik benannt und
im Selektionsmodus ausdrücklich unzulässig.** *„Sonst kommt in einem Jahr
jemand auf die Idee, die Selektion zur Isolation in einer Kopie laufen zu
lassen."*

> ⭐⭐ **Und die Probe, die den Eintrag wahr macht:** nach dem Commit ein Lauf
> unter dem Modus mit **`pandas==0.0.1`** im Lock, Arbeitsbaum sauber → **rc 2**,
> die Meldung nennt das Paket. **Ein Registertext, den der Code nicht einhält,
> wäre schlimmer als keiner.**

⭐ **Seit `be6e72c` liegen Belege und Aufträge im Repo** —
`docs/belege/TB-58/` (25 Dateien, 8 byteweise Duplikate weggelassen, mit
`HERKUNFT.md`), `docs/belege/TB-58b/`, `docs/auftraege/`. **Keine ZIP mehr.**

---

## Was der Nachmittag über die Arbeitsweise ergab

| | |
|---|---|
| ⚠️⚠️ **Berichtigung** | **F1b/Q2 ist für die DATEN belegt, nicht für den LAUF.** Ein Klon auf einer dritten Umgebung (3.11.15) bestätigte den Snapshot — ⚠️ **den Lauf entscheiden pandas und numpy**, und dafür fehlte bis heute der Lock |
| ⚠️ **Gemessen** | **Die Cloud hat 3.10–3.13, kein 3.9, kein `pyenv`** ⇒ **sie fällt als zweite Maschine für die Laufreproduktion aus.** Offene Frage an Fable |
| ⭐ | **Die Sperre gegen den zweiten Snapshot greift auch im Wegwerf-Klon** (rc 2) — der Schutz sitzt im Code, nicht in der Umgebung |
| ⚠️⚠️ | **macOS schützt `~/Downloads`: Claude-Code-Sitzungen können dort nicht lesen** — drei Sitzungsstarts gingen daran verloren, bis eine Sitzung die Ursache benannte. ⇒ **Aufträge nach `logs/auftraege/`** |
| ⭐⭐ | **Das Projekt ist seit heute ortsunabhängig.** Ursache der Sperre war der in SSH-Sitzungen verschlossene **Schlüsselbund**; `security unlock-keychain` behebt es, danach meldet die Kopfzeile `Claude Max` |
| ⚠️ | **Zwei Werkzeugfehler des Betreuers:** ein Überschreiben meldete Erfolg und änderte nichts; ein `git status` über die Geräteverbindung hinterliess eine verwaiste `.git/index.lock`. ⇒ **nie überschreiben, immer gegenprüfen; über die Verbindung nur lesen** |

---

### Der Stand am Abend des 19.09.

| | |
|---|---|
| **Snapshot** | ⭐ gezogen, registriert (Abschnitt 18), reproduziert (Daten) |
| **Resolver** | ⭐ **Schicht 1 und 2 im Repo; Startprüfungen aktiv.** ⚠️ Schicht 3, das Lese-Audit: **offen** |
| **Register** | ⭐ **Abschnitte 18, 19, 20** — Snapshot, Codeherkunft, Lock |
| **Datenstand** | `d9449faf…`/223 — an diesem Tag **über zwanzigmal** gemessen, immer gleich |
| **Offen vor dem Tag** | Lese-Audit · Faltenschranke + Berichtigung 17.3 + Drei-Kategorien-Regel · `auswertung.py` auf Verfahren B · Laufreproduktion gegen den Lock · Fables Q1 |

---

### In einfacher Sprache

**Der Auswahllauf kann ab heute beweisen, woher sein Programmcode stammt und
auf welcher Umgebung er rechnet** — nicht mehr nur, welche Daten er gelesen
hat. Stimmt eines davon nicht, hört er auf, statt weiterzurechnen.

⭐ **Das Beste daran ist nicht der neue Text im Regelwerk, sondern die Probe
danach:** Es wurde absichtlich eine falsche Angabe eingetragen, und das
Programm hat aufgehört. **Erst dadurch ist der Regeltext mehr als eine
Behauptung.**

**Und ein praktischer Fortschritt:** Von heute an lässt sich am Projekt von
überall arbeiten — der Grund, warum es bisher nicht ging, war ein verschlossener
Schlüsselbund, nicht die Technik.
