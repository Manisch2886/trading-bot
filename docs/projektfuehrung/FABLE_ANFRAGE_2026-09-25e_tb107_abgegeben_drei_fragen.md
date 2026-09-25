# FABLE_ANFRAGE 2026-09-25e — TB-107 abgegeben: die vier Rückfälle ausserhalb der Sperrliste geschlossen, Laufbereich 81 Module, Gegenprobe ohne Fund; drei Fragen

*Bezug: `FABLE_ANFRAGE_2026-09-25d_tb106_abgegeben_vier_fragen.md` (deine Antwort steht noch aus). Dazu `docs/ERGEBNIS_TB-107_nicht_gesperrte_rueckfaelle.md` (Abgabe `f61bd97`, 25.09.2026, 22:14). Vom steuernden Chat gelesen, nicht nachgemessen; die Zahlen sind die der Mac-Sitzung.*

**Sichtschutz 27.1:** keine Ergebnisgrössen des Selektionsraums. Die Hashes sind Byte-Vergleiche; `MIN_HISTORY_HOURS = 17520` ist ein registrierter Codewert (16.7 (b)), kein Ergebnis.

**Reihenfolge:** 25d und 25e sind unabhängig voneinander beantwortbar. Nur eine Stelle hängt an 25d Frage (1): Block C unten ist **vor** deiner Antwort gebaut, nach einer Betreiberentscheidung vom 25.09., 20:27, als eigener Commit `f5fdb53`. Sagst du dort „nur Tatsachennotiz“, nimmt `git revert f5fdb53` Code und Probendatei gemeinsam zurück.

---

## 1. TB-107 — Kurzfassung

- **`_min_history` (25c 4 (2)):** `re.findall`, genau ein Treffer, sonst rc 2, unabhängig vom Modus. Die Meldung nennt Datei und Trefferzahl. `kerzen_elliott_wave()` endet ohne `MIN_HISTORY_HOURS` mit rc 2 statt dem stillen Hinweis. **Gemessen:** `elliott_wave` trägt `MIN_HISTORY_HOURS` genau einmal, die acht anderen je genau einmal `MIN_HISTORY_DAYS`. Der Hinweis-Zweig war also nie der echte Pfad. Der `TypeError` in `loader_lesart()` ist damit unerreichbar (Probe `B-A3`; die Mutation „`re.search` zurück“ führt wieder in ihn). `fsm.json`/`lesart.json` bytegleich.
- **Die zweite Kopie in `faltenplan_neun.py` (25d Befund 1):** `volle_jahre()` ohne inneres Jahr und `faltenlaenge()` bei leerer Zählung ⇒ rc 2. **Mit der echten Eingabe nicht erreicht**, auch nicht über ihr `basis`-Argument; das übergeben im Repo nur Tests, über eine Ersatzwurzel, die unter dem Modus seit TB-104 mit 2 endet. `fn.json`/`eft.json` bytegleich. Eigener Commit, siehe oben.
- **`getattr` in `strategy_paths.py` (25c 4 (3)(b)):** entfernt. `_im_selektionsmodus()` ruft `paths.selektionsmodus()` direkt; fehlt die Funktion, bricht es mit `AttributeError` ab, **vor** der Ordneranlage. Die zwei Proben bekommen ein `paths` mit der Funktion. **Live-Abnahme ohne Modus:** 101 Aufrufer in allen neun Bots, je ein eigener Prozess, alle Pfade und alle danach vorhandenen Ordner vorher = nachher. Die Cron-Wächter mit Ersatzmodul bleiben grün (`test_ergebniskurven` 44/44).
- **Zwischenablage `tb40_lauf_*` (25b 3 (1)):** `messe_bot()` entfernt den Ordner im `finally`, nachdem das Ergebnis gelesen ist. Ohne Ergebnis bleibt er, und sein Pfad steht in der Meldung. Die drei Bedingungen der Klasse (iv) sind damit erfüllt:
  - (1) `mkdtemp`;
  - (2) nur der Kindprozess schreibt, nur `messe_bot()` liest;
  - (3) entfernt.

  Gemessen: `$TMPDIR` vor und nach jedem Lauf gleich. Vorher hinterliess ein einziger Lauf der alten Fassung 74 Ordner. Das Aufräumen selbst erscheint im Lese-Audit als 10 Verzeichnis-Öffnungen in Klasse (i) ausserhalb (Aufrufstapel `universum_trockenlauf.py:334`); das sind Zugriffe auf die eigene Zwischenablage.
- **Laufbereich neu gemessen (25b (5)):** am Code-Endstand mit dem Werkzeug aus TB-104 D1, dieselben drei Lauf-Typen im Modus (Trockenlauf aller neun, Benchmark, `auswertung.py`-Import): **81 Module**. Gegenüber den 80 von TB-104 ist **nur `shared/regimewache.py`** neu (mit TB-105 eingebaut); keines ist weggefallen.
- **Gegenprobe über alle `__main__`-Stellen (25c 4 (3)(a)):** `shared/test_main_gegenprobe.py` liest die Liste aus der Messdatei, nicht aus einem Literal. Sie sucht per AST je `__main__`-Block jede Stelle „fehlende Daten ⇒ `exit()`“ und verlangt davor `paths.selektionsmodus()`. **Am echten Stand: 14 Stellen, alle mit Abfrage**, genau die aus TB-105. Zwei Mutationen beissen je allein: eine Kopie ohne Abfrage und eine erfundene fünfzehnte Datei. Ein Tatsachenkommentar im Test sagt: Am Tag-Commit ersetzt die Tag-Messung die Liste.
- **Abnahme:**
  - Benchmark im Modus im Repo **und im frischen Klon** bytegleich `64fb2912…`, ohne Modus ebenso;
  - ohne Modus 8/8 Werkzeugausgaben bytegleich gegen `f22f91e`;
  - Trockenlauf 9 × rc 0, Klasse (iii) 0;
  - Sonde gegen `40ffe18d…` vorher = nachher (keine Sperrlistendatei berührt), `register()` unverändert `0ece95e2…`;
  - alle Tests grün, darunter `test_vorregistrierung` 196/196; dazu vier neue Testdateien.

## 2. Drei Fragen aus dem Ergebnis

**(1) Zwei weitere Ablagen in `universum_trockenlauf.py`.**
- `tb40_faltenplan_*` entsteht in `hole_faltenplan()`, nur ohne `--faltenplan-json`; im Benchmark wird diese Funktion nicht gerufen.
- `tb40_proben_*` entsteht in den Probeläufen `--stille-filter`.

Beide bleiben weiter liegen; sie waren nicht freigegeben. Sind sie ausserhalb der gemessenen Modus-Läufe eine Tatsachennotiz, oder behandeln wir sie wie `tb40_lauf_*`? *Unsere Neigung:* wie `tb40_lauf_*`, in einem der nächsten kleinen Aufträge. Grund: Der Laufbereich wird am Tag über **alle** registrierten Lauf-Typen gemessen (25b (5)). Ob einer davon `hole_faltenplan()` ohne JSON ruft, ist heute offen. Die Regel „nie entfernt ist Befund 1“ hängt nicht davon ab, welcher Lauf es ist.

**(2) Zehn Stellen `if trades.empty: print(…); exit()` in den `equity_simulation.py`.** Sie liegen im `__main__` der Laufbereichsdateien und enden auch unter dem Modus mit 0. Die Gegenprobe zählt sie nicht: Sie greifen bei **fehlenden Trades nach einer Rechnung**, nicht bei fehlender Eingabe, und ihnen geht kein Ladeaufruf voraus. Ist diese Abgrenzung richtig? Oder ist „0 Trades ⇒ 0“ im Modus ebenfalls ein Aufruf, der „nicht gemessen hat“ (deine Lesart von 36.5 in 25a Abschnitt 4: „Kein Aufruf endet mit 0, ohne dass gemessen wurde“)? *Wir haben keine feste Neigung.* Einerseits ist „keine Trades“ ein gemessenes Ergebnis. Andererseits endet das Skript danach ohne Ausgabe und mit 0, und ein Aufrufer kann das nicht von „gerechnet, Ausgabe geschrieben“ unterscheiden. Die Stellen sind heute von keinem Modus-Lauf erreicht (die Läufe importieren die Module, `__main__` läuft nicht).

**(3) `research/resolver_selektion/pfadvergleich.py` endet eigenständig jetzt mit rc 1.** Das Werkzeug aus TB-52 legt die `paths.py` der Fassung TB-52 **ohne** `selektionsmodus` neben die echte `strategy_paths.py`. Seit das `getattr` weg ist, bricht das mit `AttributeError` ab. Das ist genau die Folge, die du in 25c 4 (3)(b) beschrieben hast: „Ein Nachbar ohne die Funktion ist kein Nachbar.“ Die zwei Tests, die das Werkzeug importieren (`test_paths` Probe A, `test_startpruefungen` N4), sind grün: A hängt die Funktion an, N4 nutzt einen Stand, der sie schon führt.
- Soll das Werkzeug die Funktion ebenso anhängen (eine Zeile; die Datei war nicht freigegeben)?
- Oder bleibt es ein historisches Werkzeug mit Tatsachennotiz „rc 1 seit TB-107, Grund …“?

*Unsere Neigung:* die eine Zeile, weil ein Werkzeug, das dauerhaft 1 meldet, die Bedeutung von 1 verwässert (36.5).

---

**Was als Nächstes geplant ist:**
- deine Antworten auf 25d und 25e;
- danach Register 41/42 mit deinen Einträgen aus 24c, 24d, 25a, 25b (a–h), 25c (a–h) und den Antworten auf 25d/25e;
- danach der Auftrag zu 19 (Sauberkeit über den Laufbereich), mit der Ausnahme für registrierte Protokolle, die nach 25c vorher im Register stehen muss.

## In einfacher Sprache

Der letzte Aufräum-Auftrag ist sauber durch. Die vier Notlösungen in den nicht gesperrten Hilfsprogrammen sind geschlossen:
- Die Mindestdauer muss genau einmal im Programmtext stehen.
- Die zweite Kopie der Notlösung bricht ab.
- Das Pfadprogramm nimmt nicht mehr still „Regelbetrieb“ an.
- Zwischenordner werden aufgeräumt.

Im normalen Betrieb hat sich an keiner Zahl und keinem Pfad etwas geändert. Das ist an allen 101 Stellen geprüft, an denen die Bots das Pfadprogramm benutzen.

Eine neue Dauerprüfung meldet künftig jedes Skript im geschützten Bereich, das die Modus-Abfrage vergisst; heute findet sie keines. Offen sind drei kleine Fragen:
- zwei weitere Zwischenordner, die noch liegen bleiben;
- zehn Stellen, die bei null Trades still mit „fertig“ enden;
- ein altes Prüfwerkzeug, das jetzt folgerichtig einen Fehler meldet.
