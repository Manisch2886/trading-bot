
---

## 19. Registertext 5e, Ergänzung — die Codeherkunft (TB-58b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Registertext wird
umgeschrieben — hier wird Registertext 5e (Abschnitt 17.4) ergänzt**, in der
Form von Abschnitt 18. Das ist der Nachtrag, den
`docs/ERGEBNIS_TB-58_startpruefungen.md` angekündigt hat: TB-58 hat die
Prüfungen gebaut und ausdrücklich keinen Registertext angefasst.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Entscheidung.**
Sie trifft etwas, das im Register offen war — 5e sagt, welche **Daten** ein
Lauf gelesen hat; nichts sagte, welcher **Code** sie gelesen hat. Sie ist vor
dem Tag zulässig, ihre Begründung nennt kein Ergebnis, und sie hat keine
bekannte Wirkung auf die Zulassung eines Bots: sie entscheidet, wann ein
**Lauf** ein Lauf dieses Registers ist, nicht, welcher Bot durchkommt.

> **Registertext 5e, Ergänzung Codeherkunft. Datum: 19.09.2026.**
>
> Der Selektionslauf prüft bei Start, dass sein **Einstiegspunkt** und der
> **Resolver** unter derselben Git-Wurzel liegen, dass deren `HEAD` der
> registrierte Commit ist und dass der **Arbeitsbaum sauber** ist; bei
> Verletzung bricht er ab (**Rückgabewert 2**). Wurzel, Commit und Sauberkeit
> werden im Lese-Audit protokolliert. **Ein Lauf ohne diese Angaben oder mit
> abweichender Wurzel ist kein Lauf dieses Registers.**
> ⚠️ **Im Regelbetrieb gilt keine dieser Bedingungen.**
>
> **Begründung:** Liegen Aufrufer und Resolver in verschiedenen Bäumen,
> beschreibt kein einzelner Commit den gelaufenen Code. Das Lese-Audit belegt,
> **welche Daten** gelesen wurden; es sagt nichts darüber, **welcher Code**
> gelesen hat.
>
> ⭐ **Das Wegwerfbaum-Muster** — eine Bot-Kopie in einem temporären Verzeichnis
> mit der echten `shared/` — **ist eine Testtechnik des Regelbetriebs und im
> Selektionsmodus unzulässig.**

**Was der Code am Tag dieses Eintrags tut** (`shared/paths.py`, Commit
`6518e413b17dd4b7f5c624549aa145f94fca3a96` auf `main`; jede Zeile gemessen,
Nachweise in `docs/ERGEBNIS_TB-58_startpruefungen.md` und
`shared/test_startpruefungen.py`, 44 Proben mit Mutationsgegenprobe):

| Satz des Registertexts | Umsetzung | Gemessen |
|---|---|---|
| Einstiegspunkt und Resolver unter derselben Git-Wurzel | `sys.modules["__main__"].__file__` und `shared/paths.py`, beide über `realpath` und `git rev-parse --show-toplevel` | gespaltener Baum aus einem anderen Repo **und** aus einem Ordner ohne Git: rc 2, die Meldung nennt beide Wurzeln; `python -c` (kein Einstiegspunkt): rc 2 |
| `HEAD` ist der registrierte Commit | der Modus **trägt** den erwarteten Commit in der dritten Umgebungsvariablen `TB_SELEKTIONSCOMMIT` (7–40 Hex-Zeichen; Zweignamen wie `main` werden abgewiesen); `git rev-parse HEAD` muss damit beginnen | falscher Commit rc 2; fehlende Variable bei gesetzten anderen beiden rc 2; Variable allein `Selektionsfehler` |
| Arbeitsbaum sauber | `git status --porcelain` über `shared/`, `strategies/` und `requirements.lock` (`ARBEITSBAUM_PFADE`), untracked zählt; ⚠️ **nicht** über `data/` — die ist versioniert und wird vom Abruf-Cron laufend verändert, ein Lauf aus dem Snapshot darf daran nicht scheitern | veränderte Datei unter `shared/`, neue Datei unter `strategies/`, veränderter Lock: je rc 2 mit Nennung; neue Datei unter `data/` stört nicht |
| Rückgabewert 2 | `SystemExit(2)` beim Import, nicht `Exception` — ein `except Exception` im Aufrufer kann den Abbruch nicht in einen stillen Weiterlauf verwandeln; der Wert steht genau einmal | rc 2 in jeder Probe, `stdout` leer |
| Wurzel, Commit, Sauberkeit protokolliert | drei der acht Auditzeilen `[paths] codewurzel / commit / arbeitsbaum` auf `stderr` nach bestandener Prüfung, dieselben Werte über `paths.startpruefung()` und `paths.audit_zeilen()` | `stderr`-Zeilen == `audit_zeilen()`; gegen den echten Arbeitsbaum 9 / 9 Bot-Einstiegspunkte |
| Im Regelbetrieb gilt nichts davon | alles im `else`-Zweig des Modus; `subprocess`, `importlib.metadata`, `platform`, `hashlib` werden erst innerhalb der Prüffunktionen importiert | ohne Modus **0 / 0 / 0** `git`-, Paket- und `os.system`-Aufrufe (zählende Attrappe), 144 Pfade über 9 Bots zeichengleich wie vor TB-58 |

Drei Punkte, die diese Tabelle tragen:

1. **„Der registrierte Commit" ist heute der Wert, den der Modus mitbringt.**
   Der signierte Tag (Abschnitt 13) existiert noch nicht; bis dahin sagt
   `TB_SELEKTIONSCOMMIT`, welcher Commit verlangt ist, und die Prüfung misst,
   ob der Baum ihn hat. Sobald der Tag steht, ist es sein Commit. Die Bauart
   ist dieselbe wie beim Snapshot-Hash: der Modus **trägt** den Sollwert, statt
   ihn irgendwo zu suchen, und ein Kindprozess erbt ihn.
2. ⚠️ **Der Lese-Audit als Ganzes (5e, 17.4) ist weiterhin nicht gebaut** —
   17.10, Zeile 3 gilt fort. Was heute existiert, sind die acht Auditzeilen des
   Starts; der spätere Lese-Audit übernimmt sie über `audit_zeilen()`, ohne
   eine zweite Fassung zu pflegen. Der Registertext beschreibt damit etwas, das
   der Code zum Teil noch nicht kann — benannt, nicht verschwiegen (dieselbe
   Regel wie 16.11 und 17.10).
3. **Das Wegwerfbaum-Muster** wird von Bedingung 1 getroffen: eine Bot-Kopie in
   einem temporären Ordner, die die echte `shared/` importiert, hat einen
   anderen Einstiegspunkt als Resolver-Wurzel — im Selektionsmodus rc 2. Im
   Regelbetrieb bleibt es erlaubt und wird weiter gemessen
   (`shared/test_strategy_paths.py`, Probe E, ohne Modus).

**Was diese Ergänzung nicht tut:** kein Selektionslauf, kein signierter Tag,
kein Amendment; der Wortlaut von 5e in 17.4 bleibt stehen und gilt weiter;
17.10 wird nicht umgeschrieben — seine Zeilen beschreiben den Stand vom
18.09.2026, und ob eine davon inzwischen geschlossen ist, steht hier und in
Abschnitt 20, nicht dort.

*Nachgetragen in TB-58b, 19.09.2026. Entscheidung nach F17: vor dem Tag, ohne
Ergebnis in der Begründung, ohne Wirkung auf die Zulassung eines Bots.*

---

## 20. Tatsachennotiz zu Registertext 5f — der Lock (TB-58b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein Registertext wird geändert — hier
wird eine Messung festgehalten**, in der Form von Abschnitt 18. Registertext 5f
(Abschnitt 17.5) verlangt ein `requirements.lock`, „dessen Hash im Register
steht"; bis zu diesem Eintrag stand er nirgends, und 17.10, Zeile 4 hielt
fest, dass es die Datei nicht gab. Seit TB-58 gibt es sie; hier ist ihr Hash.

> **Tatsachennotiz zu Registertext 5f — der Lock. Datum: 19.09.2026.**
>
> Die Umgebung, in der der Selektionslauf rechnet, ist in
> **`requirements.lock`** im Projektwurzelverzeichnis festgehalten, versioniert
> unter Commit `d852bce637ba82ddb60330a7219c6e36a40539c3`.
>
> | | |
> |---|---|
> | SHA-256 der Datei | **`96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** |
> | Pakete | **67**, sämtlich mit `==` |
> | Interpreter | `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]` |
> | Plattform | `macOS-15.7.9-x86_64-i386-64bit` |
>
> Der Lauf prüft bei Start Interpreter, Paketfassungen und Plattform gegen
> diese Datei und bricht bei Abweichung ab (**Rückgabewert 2**).
>
> ⚠️ **`requirements.txt` ist kein Lock** — es nennt, was installierbar ist;
> `requirements.lock` nennt, was gelaufen ist.

**Jede Zahl der Tabelle wurde in TB-58b selbst gemessen, keine abgeschrieben:**

| | Messung |
|---|---|
| SHA-256 | zweimal unabhängig gerechnet — `shasum -a 256` und `hashlib.sha256` unter `trading-env/bin/python3` — beide `96a5c572…`; derselbe Wert steht in der Auditzeile `lock_sha256` eines bestandenen Starts |
| Versioniert | `git log -- requirements.lock` nennt genau einen Commit, `d852bce`, auf `origin/main`; der Blob im Arbeitsbaum ist byteweise der Blob unter `HEAD` (`git hash-object` = `git rev-parse HEAD:requirements.lock`, `863197fb…`) |
| 67 Pakete, sämtlich `==` | 83 Zeilen, davon 67 Paketzeilen; 0 Paketzeilen ohne `==`; gegen `importlib.metadata` unter `trading-env/bin/python3`: **0 Abweichungen** |
| Interpreter, Plattform | Kopfzeilen `interpreter_voll` und `plattform` der Datei, gleichlautend mit `sys.version` und `platform.platform()` des Betriebsinterpreters; dazu `maschine x86_64` |
| Der Kalender | `pandas-market-calendars==4.6.1` — dieselbe Fassung, die die Tatsachennotiz in 17.5 (gemessen TB-47) nennt; `pandas==2.3.3` |

**Die Probe, die diesen Eintrag erst wahr macht** — in einem Wegwerf-Klon des
Repos (kein Objekt und keine Datei im Arbeitsbaum von `~/trading-bot`
berührt), Interpreter `trading-env/bin/python3`, Snapshot `63e4b6c8…`,
`TB_SELEKTIONSCOMMIT` = `HEAD` des Klons, Einstiegspunkt eine committete
Datei:

| Zustand | Rückgabewert | Meldung |
|---|---|---|
| Lock unverändert (Kontrolle) | **0** | acht Auditzeilen, `lock_sha256 96a5c572…` |
| eine Zeile verfälscht (`pandas==0.0.1`), **committet**, Baum sauber | **2** | „1 Abweichung/en … pandas: Lock 0.0.1, installiert 2.3.3" |
| dieselbe Verfälschung **nicht** committet | **2** | „Arbeitsbaum … nicht sauber (1 Eintrag …  M requirements.lock)" — Abschnitt 19, Bedingung 3, greift **vor** der Lock-Prüfung |
| Lock gelöscht und committet | **2** | „requirements.lock fehlt … `nicht pruefbar` ist nicht gruen" |
| Lock richtig, Interpreter `/usr/bin/python3` (gleicher Build, andere Pakete) | **2** | „24 Abweichung/en", die ersten drei „installiert NICHT" |

Drei Punkte, die diese Tabellen tragen:

1. **Was geprüft wird, ist die Umgebung gegen die Datei — nicht die Datei gegen
   diesen Eintrag.** Der Lauf liest den Lock, der unter dem verlangten Commit
   im Baum liegt, vergleicht Interpreter, Plattform und jede Paketzeile mit
   dem, was `importlib.metadata` tatsächlich findet (kein `pip`, kein
   Kindprozess, keine Netzverbindung), und schreibt den SHA-256 der Datei in
   die Auditzeile `lock_sha256`. Ob diese Zeile `96a5c572…` lautet, ist am
   Audit abzulesen; ein anderer Lock wäre ein anderer Commit und scheiterte
   schon an Abschnitt 19.
2. ⚠️ **Nichts wird installiert, nachgezogen oder repariert.** Der Lauf meldet
   die Zahl der Abweichungen und die ersten drei, dann bricht er ab.
3. **Die Interpreter- und die Plattformzeile allein hätten den fremden
   Interpreter nicht bemerkt** — `/usr/bin/python3` ist derselbe Build wie
   `trading-env/bin/python3`; erst die Paketzeilen unterscheiden die beiden
   (24 Abweichungen). Deshalb sind alle drei Achsen im Lock, nicht nur die
   Fassung.

**Was diese Notiz nicht tut:** kein Selektionslauf, kein signierter Tag, kein
Amendment, kein `pip install`; der Wortlaut von 5f in 17.5 ist nicht
umformuliert. 17.10, Zeile 4 bleibt als Befund vom 18.09.2026 stehen; dass sie
mit `d852bce` und `6518e41` geschlossen ist, steht hier. Die Mindestfassung des
Projekts (`docs/UMGEBUNGEN.md`, in 17.10, Zeile 4 mitgenannt) ist **nicht**
Gegenstand dieser Notiz und bleibt offen.

*Nachgetragen in TB-58b, 19.09.2026. Tatsachennotiz: eine Messung, keine
Festlegung.*
