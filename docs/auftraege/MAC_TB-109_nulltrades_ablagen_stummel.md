# TB-109 — „null Trades ist ein Wert“ an zehn Stellen, zwei weitere Zwischenablagen, der benannte Stummel in `pfadvergleich.py`, Klasse (iv) im Audit

**Sitzungstitel:** `TB-109` · **Angelegt:** 25.09.2026, 23:20, vom steuernden Chat
**Vorgänger:** TB-108 (Register 41/42) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Anschluss in derselben Sitzung:** TB-110 (Register 43), siehe Block H am Ende.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**25.09.2026, 23:04, zwei Auswahlkarten im steuernden Chat:**

| Frage | Antwort |
|---|---|
| *„Darf ich TB-109 so bauen, wie im Entwurf beschrieben? Der Entwurf setzt Fable 25e um; die 10 Stellen liegen im Live-Code der Bots.“* | **„Alles freigeben (Empfohlen)“**: die 10 Stellen `trades.empty` in 9 `equity_simulation.py` (nur unter dem Modus rc 2, ohne Modus bytegleich), die zwei Zwischenordner in `universum_trockenlauf.py`, der Stummel in `pfadvergleich.py` (mit `None` statt Fables `False`), die erweiterte Gegenprobe, die Audit-Auswertung, dazu die Tests |
| *„Soll nach TB-108 auch Register 43 (Fable 25d und 25e, gut zehn Einträge) als eigener Auftrag vorbereitet werden?“* | **„Ja, als TB-110 (Empfohlen)“**: reine Registerarbeit wie TB-108, kein Code, läuft nach TB-109 |

**Grundlage:**
- Fable 25e: (1) zwei weitere Ablagen wie `tb40_lauf_*`; (2) „null Trades ist ein Wert“, die zehn Stellen wie die vierzehn, die Gegenprobe zählt jedes `exit()` ohne Ausgabe; (3) der benannte Stummel in `pfadvergleich.py`; 3 (b) Klasse (iv) im Audit;
- Fable 25d (1): `f5fdb53` steht, kein Revert.

**Nicht in diesem Auftrag** (gesperrt oder an einen anderen Anlass gebunden):
- 25d (4): `auswertung.Abbruch` ⇒ 2. Das kommt mit der nächsten planmässigen Öffnung von `auswertung.py` (Punkte 3/5/14, neues Abbild).
- 25d (2)/(3): `herkunft.py` mit Prüfansicht und `TB30A_BASE_DIR`. Eine Öffnung, mit dem Erzeuger oder vor ihm.

---

## ⚠️ Ein Widerspruch in Fable 25e (3) — so wird gebaut

Fable schlägt für den Stummel `selektionsmodus = lambda: False` vor. `shared/strategy_paths.py` fragt seit TB-107 aber `paths.selektionsmodus() is not None` (Ergebnis TB-107, D1). **`False is not None` ist wahr:** Mit Fables Stummel hielte `strategy_paths` den Modus für **aktiv**, würde keine Ordner anlegen, und das Werkzeug würde etwas anderes vergleichen als gemeint.

`test_paths` Probe A benutzt darum `def selektionsmodus(): return None`. **Der Stummel in `pfadvergleich.py` bekommt `return None`, wie Probe A**, benannt als „Fassung TB-52 plus `selektionsmodus()` → `None`, weil der heutige Nachbar die Funktion verlangt“.

Den Widerspruch in der nächsten Anfrage an Fable als Berichtigung melden (Bauart 25a „achter Fall“). Das ist kein Grund zu warten: Fables Absicht, „vergleicht weiter die Pfadauflösung“, ist nur mit `None` erfüllt.

---

## Freigegebene Dateien (Karte 23:04)

| Pfad | was | Art |
|---|---|---|
| die 9 `strategies/*/equity_simulation.py` mit den **10** Stellen `if trades.empty: … exit()` (Liste: `docs/belege/TB-107/f_gegenprobe.txt` Z. 21–31) | unter dem Modus: Meldung auf stderr, `SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)`, Bauart wie die 14 Stellen aus TB-105 C (Abfrage an der Stelle, kein Name aus `strategy_paths`); **ohne Modus unverändert** | ⚠️ **Live-Code** (Cron-Wächter 3:50/4:10, `runpy` im `__main__`) |
| `research/universum_trockenlauf/universum_trockenlauf.py` | `hole_faltenplan()` (Z. 259, `tb40_faltenplan_`) und die Probeläufe (Z. 681, `tb40_proben_`): Ordner im `finally` entfernen; ohne Ergebnis Pfad in der Meldung (Bauart TB-107 E) | Laufbereich, nicht gesperrt |
| `research/resolver_selektion/pfadvergleich.py` | benannter Stummel `selektionsmodus()` → `None` (siehe oben) | ausserhalb des Laufbereichs |
| `shared/test_main_gegenprobe.py` | zählt jedes `exit()`/`sys.exit()`/`quit()` im `__main__` ohne vorher geschriebenes Ergebnis, nicht nur nach fehlender Eingabe (25e (2)); erwartet danach 24 Stellen mit Abfrage | Test |
| das Audit-Auswertungswerkzeug (`docs/belege/TB-104/d_auswerten.py` bzw. seine Kopie) | Lesezugriffe eines Laufs auf seine eigene Klasse-(iv)-Ablage als (iv) führen, nicht als (i) ausserhalb (25e 3 (b)) | Messwerkzeug |
| die Tests dieser Module | — | — |

⛔ Nicht freigegeben: alles unter `research/vorregistrierung/`, `shared/paths.py`, `shared/strategy_paths.py`, `regimewache.py`, die Cron-Wächter selbst, `forward_test.py`, `live_params.py`, Register, `crontab`.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet (alle unter `docs/`):

| Datei | Stand |
|---|---|
| `auftraege/MAC_TB-109_nulltrades_ablagen_stummel.md` | dieser Auftrag |
| `auftraege/MAC_TB-110_register_43.md` | der Anschlussauftrag |
| `auftraege/MAC_TB-111_herkunft_auswertung_oeffnung.md` | der **parallele** Auftrag für Sitzung B im Worktree |
| `auftraege/AKTUELLER_AUFTRAG.md` | Zeiger auf TB-109 (mit TB-110 als Anschluss) und TB-111 (Worktree) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25d_kopie_pruefansicht_abbruch_zwei.md` | neu, aus der Projektablage abgeschrieben |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25e_ablagen_nulltrades_shim.md` | neu, aus der Projektablage abgeschrieben |
| `projektfuehrung/UEBERGABE_2026-09-25.md`, `projektfuehrung/AUFGABEN_BETREIBER_2026-09-26.md` | Nachträge |

Weicht der Arbeitsbaum davon ab: melden, nichts Fremdes mitcommitten.

**0c — ⭐ Worktree für die parallele Sitzung B anlegen**, direkt nach dem Schritt-0-Commit und **vor** Block A:

```
git worktree add ../trading-bot-tb111 -b tb-111 HEAD
```

- Prüfen: `git --no-optional-locks worktree list` zeigt `../trading-bot-tb111 [tb-111]`, und `docs/auftraege/MAC_TB-111_…` liegt dort.
- Danach arbeitest du **nur im Hauptordner**. Den Worktree nicht betreten und nichts darin ändern. Der Zweig `tb-111` gehört Sitzung B.
- Scheitert der Befehl: melden, TB-109 trotzdem abarbeiten (TB-111 fällt dann aus).

**0b — nach 7c:**
- keine `.git/*.lock`;
- HEAD am Eingang = Abgabe-Commit von TB-108 (im Ergebnis nennen);
- Datenstand `d9449faf…`, `*.db` vorher;
- Hashes aller freigegebenen und gesperrten Dateien vorher (`docs/belege/TB-107/hashes.sh`);
- Sonde gegen `40ffe18d…` vorher;
- Zahl der `tb40_*`-Ordner in `$TMPDIR` vorher, je Präfix (nur zählen).

## Block A — Vormessung nachmessen

| | Stelle | Vormessung |
|---|---|---|
| A1 | die 10 Stellen `if trades.empty: … exit()` | Liste `docs/belege/TB-107/f_gegenprobe.txt` Z. 21–31: `elliott_wave:155`, `elliott_wave_stocks:178`, `rsi2_crypto:142`, `rsi2_mean_reversion:173`, `t3_supertrend:149`, `turtle_soup_crypto:125`, `turtle_soup_stocks:164`, `volatility_breakout:158`, `volatility_breakout_crypto:173` und `:179` (je `equity_simulation.py`, im `__main__`) |
| A2 | Wer startet diese `__main__`-Blöcke im Betrieb? | TB-105 A3: die Cron-Wächter `ergebniskurven` (3:50) und `determinismus` (4:10) per `runpy`; `crontab -l` gesperrt ⇒ statisch |
| A3 | Erreicht einer der Cron-Läufe heute eine der 10 Stellen (Bot ohne Trades)? | nicht gemessen. **Messen**: vorher je Bot die Trade-Liste im Speicher (Bauart `b3_trades.py`), leer ja/nein |
| A4 | `universum_trockenlauf.py:259` (`tb40_faltenplan_`) und `:681` (`tb40_proben_`) | beide ohne Aufräumen |
| A5 | `pfadvergleich.py` eigenständig | rc 1 (`AttributeError`, TB-107 D) |
| A6 | Gegenprobe heute | 14 Stellen gezählt, 10 ausgewiesen |

## Block B — die 10 Stellen (Live-Code)

- **B1:** An jeder Stelle, vor dem bestehenden `print`/`exit()`: unter dem Modus Meldung auf stderr und `SystemExit(paths.RUECKGABEWERT_STARTPRUEFUNG)`. Die Abfrage steht an der Stelle selbst (`import paths`, `paths.selektionsmodus()`), wie die 14 aus TB-105 C. **Kein** neuer Name aus `strategy_paths` (Ersatzmodule der Cron-Wächter). **Ohne Modus zeichengleich wie vorher.**
- **B2:** Proben im Wegwerfbaum (Bauart `shared/test_rueckfaelle_modus.py` Teil C):
  - je Datei „leere Trade-Liste, Modus ⇒ rc 2“ und „ohne Modus ⇒ rc 0 wie vorher“;
  - eine Mutation für die Bauart mit Gegenprobe.
- **B3 — Abnahme Live-Code ohne Modus:**
  - die Trade-Listen-Hashes der neun Bots vorher = nachher (`b3_trades.py`);
  - `research/tb27_kapitalsimulation/vergleich.py --pruefen` rc 0;
  - `test_ergebniskurven` grün;
  - `test_rueckfaelle_modus` grün.

## Block C — `universum_trockenlauf.py`

- Beide Ablagen wie `tb40_lauf_*` (TB-107 E): im `finally` entfernen; ohne Ergebnis bleibt der Ordner, und sein Pfad steht in der Meldung. Nur die zwei Funktionen ändern, `import shutil` lokal wie in TB-107.
- Proben mit eigenem `TMPDIR` und Mutation „Aufräumen weg“ je Ablage.
- **Abnahme:** `ut.json`, `sf.json` bytegleich. `$TMPDIR` vor und nach einem Lauf `hole_faltenplan()` **ohne** `--faltenplan-json` und nach `--stille-filter` gleich.

## Block D — `pfadvergleich.py`

Der benannte Stummel `selektionsmodus()` → **`None`** (siehe den Widerspruch oben), mit Kommentar „Fassung TB-52 plus `selektionsmodus()` → None, weil der heutige Nachbar die Funktion verlangt (Fable 25e (3); `None` statt `False`, weil `strategy_paths` `is not None` fragt)“.

**Abnahme:** eigenständig rc 0 („GRUEN“); `test_paths` A und `test_startpruefungen` N4 grün. Probe: der Stummel mit `False` ⇒ das Werkzeug meldet Unterschiede. Das belegt den Widerspruch am Verhalten.

## Block E — Gegenprobe und Audit

- **E1:** `shared/test_main_gegenprobe.py` zählt jedes `exit()`/`sys.exit()`/`quit()` im `__main__` einer Laufbereichsdatei, dem kein geschriebenes Ergebnis vorausgeht (25e (2)). Die Liste weiter aus `docs/belege/TB-107/f1_laufbereich_vereinigung.txt`. Erwartet am echten Stand: **24** Stellen, alle mit Abfrage.
  - Mutation: eine 25. Stelle ohne Abfrage ⇒ rot, mit Gegenprobe.
  - Findet die erweiterte Probe weitere Stellen ohne Abfrage: **nicht** selbst ändern (die Dateien sind nicht freigegeben), melden.
- **E2:** Das Audit-Auswertungswerkzeug ordnet Zugriffe eines Laufs auf seine **eigene** Klasse-(iv)-Ablage (von ihm angelegt und entfernt) der Klasse (iv) zu, nicht (i) ausserhalb (25e 3 (b)). Neue Fassung unter `docs/belege/TB-109/`, die alte bleibt.
  - Abnahme: der Benchmark-Lauf aus G1 mit dem neuen Werkzeug; Klasse (i) ausserhalb wieder 21 (wie TB-106); die 10 Öffnungen unter (iv).

## Block F — Abnahme gesamt

- **Benchmark im Modus**, Repo **und** frischer Klon: `64fb2912…`.
- **Ohne Modus:** 8/8 Ausgaben bytegleich; Benchmark `64fb2912…`.
- Trockenlauf 9 × rc 0.
- Sonde gegen `40ffe18d…` vorher = nachher (kein Sperrlistenpfad berührt); `register()` wie am Eingang (nach TB-108 neu, den Wert aus dem TB-108-Ergebnis nehmen).
- **Tests mit Namen:** `test_rueckfaelle_modus`, `test_ergebniskurven`, `test_paths`, `test_strategy_paths`, `test_startpruefungen`, `test_universum_trockenlauf`, `test_zwischenablage`, `test_main_gegenprobe`, `test_vorregistrierung` 196/196, alle neuen.

⛔ Sichtschutz 27.1: keine Kennzahl, keine Trade-Zahl; „Trade-Liste leer ja/nein“ je Bot (A3) ist zulässig.

## Block G — Abgabe

- Ergebnis `docs/ERGEBNIS_TB-109_nulltrades_ablagen_stummel.md` mit einem Abschnitt „Für Fable“. Darin: A3 gemessen; die 24 Stellen; der Widerspruch `False`/`None` mit dem Verhaltensbeleg aus D; Klasse (iv) im Audit.
- Journalblock; `git --no-optional-locks status --porcelain` leer.
- **Commits:** (1) Schritt 0 · (2) Block B · (3) Block C · (4) Block D · (5) Block E · (6) Belege und Ergebnis.

## ⚠️ Abbruchkriterien

1. Ohne Modus ändert sich ein Trade-Hash, eine der 8 Ausgaben oder `vergleich.py --pruefen` ⇒ die Änderung zurücknehmen, melden.
2. Die Benchmark-Tabelle ist nicht bytegleich ⇒ nicht weiterbauen.
3. A3 zeigt, dass ein Cron-Lauf heute eine der 10 Stellen erreicht ⇒ B trotzdem bauen (ohne Modus bleibt alles gleich), aber im Ergebnis ausdrücklich melden.
4. Eine Änderung bräuchte eine nicht freigegebene Datei ⇒ melden, nicht bauen.

---

## Block H — Anschluss: TB-110 in derselben Sitzung

⭐ Der Betreiber ist über Nacht nicht erreichbar. Damit die Nacht genutzt wird, arbeitet diese Sitzung **nach der Abgabe von TB-109** den Auftrag **`docs/auftraege/MAC_TB-110_register_43.md`** ab. Er ist freigegeben (Karte 23:04) und steht im Zeiger als Anschluss.

- Beginne TB-110 erst, wenn der Abgabe-Commit von TB-109 liegt und `git status` leer ist.
- TB-110 hat eigene Belege (`docs/belege/TB-110/`), eigenes Ergebnis und eigene Commits.
- Stösst TB-109 auf ein Abbruchkriterium, beginne TB-110 **nicht**. Melde beides.

---

## In einfacher Sprache

Der Prüfer hat entschieden: Wenn ein Bot keine Geschäfte findet, ist das ein Ergebnis (Wert 0) und kein Grund, still aufzuhören. Zehn Stellen in den Simulationsprogrammen hören heute still auf; im geschützten Modus melden sie das künftig als Fehler. Zwei weitere Zwischenordner werden aufgeräumt. Ein altes Prüfwerkzeug bekommt einen kleinen, ausdrücklich benannten Aufsatz. Beim Vorschlag des Prüfers für diesen Aufsatz steckt ein kleiner Denkfehler; er wird im Auftrag richtiggestellt und ihm gemeldet.
