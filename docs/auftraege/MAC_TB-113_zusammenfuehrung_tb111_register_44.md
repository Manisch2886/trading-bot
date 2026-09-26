# TB-113 — `tb-111` nach `main` zusammenführen, Register 44 (TB-111 und TB-112), Wächter auf Aufwand „hoch“, Worktree entfernen

**Sitzungstitel:** `TB-113` · **Angelegt:** 26.09.2026, 10:50 (freigegeben 14:28), vom steuernden Chat
**Vorgänger:** TB-112 (`af6042f`) und TB-111 (Zweig `tb-111`, Abgabe `49f0868`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)

## ⭐⭐ Freigabe des Betreibers, wörtlich

**26.09.2026, ca. 14:28, Auswahlkarte im steuernden Chat:** *„Darf ich TB-113 starten? TB-111 wird in den Hauptordner zusammengeführt und alles neu geprüft. Das Regelwerk bekommt Abschnitt 44 mit dem, was TB-111 und TB-112 umgesetzt haben. Der Wächter-Start mit Aufwand „hoch“ und die Regel „erst Sitzung anlegen“ kommen in die Arbeitsweise. Danach wird der Hilfsordner trading-bot-tb111 entfernt; der Zweig bleibt.“* ⇒ **„Alles freigeben (Empfohlen)“**

| freigegeben | Pfad / Handlung |
|---|---|
| ✔ | `git merge --no-ff tb-111` auf `main`, Push `main` |
| ✔ | `docs/VORREGISTRIERUNG_neuselektion.md`: Abschnitt 44 **anhängen**, Marken additiv |
| ✔ | `docs/projektfuehrung/JOURNAL.md`: Journalblock aus `ERGEBNIS_TB-111` übertragen (Kennung **DK**) und eigener Block |
| ✔ | `docs/projektfuehrung/ARBEITSWEISE.md`: Nachtrag zu 22.1 und neuer Abschnitt 22.9 |
| ✔ | `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`: die vom steuernden Chat geänderte Startzeile committen (siehe 0a) |
| ✔ | `git worktree remove ../trading-bot-tb111` (der Zweig `tb-111` bleibt lokal und auf `origin`) |
| ✔ | `docs/belege/TB-113/`, `docs/ERGEBNIS_TB-113_…md` |

⛔ **Nicht freigegeben:**
- Code-Änderungen jeder Art ausser dem Merge;
- ein neues Abbild. Gültig ist `sperrliste_abbild_2026-09-26.json` `e655c1c8…` aus TB-111;
- jede Marke im Listentext von Abschnitt 10;
- `crontab`.

---

## 0. Schritt 0

**0a — Arbeitsbaum des steuernden Chats committen.** Erwartet:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-113_zusammenfuehrung_tb111_register_44.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger TB-113 |
| `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` | **eine** Zeile geändert: `exec claude --remote-control` ⇒ `exec claude --effort high --remote-control` (Betreiber 26.09.2026, 09:36: *„Starte die Sessions zukünftig immer mit aufwand hoch“*). Prüfen mit `git diff --stat`: 1 Datei, 1 Zeile |

Commit-Text „TB-113 Schritt 0: Arbeitsbaum des steuernden Chats (Auftrag TB-113, Zeiger, Wächter --effort high)“, dann Push.

**0b — Beleg, dass der Schalter greift:**
- `claude --help | grep -c -- '--effort'` (erwartet ≥ 1);
- die eigene Kopfzeile bzw. `/status` nennt den Aufwand. Beides in `0b_effort.txt`.

Greift der Schalter nicht: **melden, weiterarbeiten** (die Zeile bleibt, der steuernde Chat entscheidet).

**0c — Vorbedingungen:**
- `git --no-optional-locks worktree list`;
- `.git/worktrees/trading-bot-tb111/index` seit `49f0868` unverändert, also Sitzung B geschlossen;
- `git merge-tree --write-tree main tb-111` endet mit rc 0. Die Schnittmenge der geänderten Dateien `f4d6d6d..main` gegen `f4d6d6d..tb-111` ist leer, und es gibt kein zweites `sperrliste_abbild_2026-09-26.json` auf `main`.

Weicht etwas ab: **Abbruch, melden.**

## Block A — Zusammenführen

- `git merge --no-ff tb-111 -m "TB-113: tb-111 (TB-111, Fable 25d: herkunft.py im Modus, auswertung.Abbruch 2) nach main"`, dann Push.
- **Danach messen** (TB-111 Abschnitt 7):
  - `register()` neu; erwartet ist weder `e7d82547…` noch `c92900a8…`;
  - Sonde gegen `e655c1c8…`: 25/0/0, (ii) 0;
  - Hashes `herkunft.py` `5bbfc9e0…` und `auswertung.py` `a864b216…`;
  - Benchmark im Modus, Repo **und** frischer Klon: `64fb2912…`;
  - ohne Modus: 8/8 Ausgaben bytegleich (`docs/belege/TB-109/g2_ausgaben.sh`);
  - Trockenlauf: 9 × rc 0;
  - Tests grün: `test_vorregistrierung` 196/196, `test_ersatzwerte`, `test_startpruefungen` 44/44, `test_arbeitsbaum_laufbereich` 26/26.
- **Wechselwirkung TB-111 × TB-112:** Die erweiterte Startprüfung bindet `research/vorregistrierung/auswertung.py` (Laufbereich), `herkunft.py` bindet sie nicht (nicht im Laufbereich, TB-107/TB-112 A2). So festhalten.

## Block B — Journal

- Den Block „Journalblock zum Übertragen“ aus `ERGEBNIS_TB-111` (auf `main` nach dem Merge) **wörtlich** als `## DK — TB-111: …` nach `JOURNAL.md`.
- Danach der eigene Block `## DL — TB-113: …`.

## Block C — Register 44 (Tatsachennotizen, Bauart TB-110)

`## 44. …` sinngemäss: „Vollzug: `herkunft.py` im Modus, `auswertung.py` endet mit 2, 19 über den Laufbereich — Tatsachennotizen TB-111 und TB-112 (TB-113, 26.09.2026)“.

- **44.0 Kopf:** Anlass; TB-111 lief auf einem eigenen Zweig und ist mit diesem Auftrag zusammengeführt; Verweis auf 43.
- **44.1 TB-111:**
  - 43-1 vollzogen: `Abbruch` rc 2, 12 Stellen, Meldung byte-gleich;
  - 43-4 vollzogen: Prüfansicht `paths.DATA_DIR`, TB30A unter dem Modus rc 2 vor dem Lesen, `_paths()` aus der eigenen Wurzel;
  - Befund A2b (vorher rc 1 statt 2);
  - Hash-Übergänge;
  - **gültiges Abbild `e655c1c8…`**; Sonde gegen das alte: Befund genau 3/5/11/12/14 + `eingefroren`;
  - `register()` nach dem Merge.
- **44.2 TB-112:**
  - E2 und F8 vollzogen: `ARBEITSBAUM_PFADE` (15 Einträge), `REGISTRIERTE_PROTOKOLLE` als `:(exclude)`;
  - die Pfadliste `docs/belege/TB-112/arbeitsbaum_pfade.txt` ist die „Tatsachennotiz neben der Laufbereichsmessung“ aus E2;
  - Laufbereich 81 = TB-107;
  - Audit: 0 Code-Zugriffe ausserhalb;
  - Randbefund: 10 versionierte Eingaben ausserhalb der Liste (offen bei Fable);
  - db-Sicherung und `tb40_test_*` nur als Nebennotiz.
- **44.3 Offen:**
  - Fragen an Fable aus TB-109 (`None`, Reichweite (iv), Gegenprobe `main()`), TB-111 (`datenstand(None)`, Docstring, `str(e)`) und TB-112 (Eingaben ausserhalb der Liste, Pflege der Liste, deutsches Schlüssel-Muster);
  - Erzeuger;
  - Faltenplan-Abbild.

**Marken am alten Ort (additiv, Zielabschnitt vorher lesen):**

| Wo | Marke |
|---|---|
| **19**, unter dem Kasten „Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen“ | „vollzogen in TB-112, siehe 44.2“ |
| **36.5**, unter der TB-110-Marke | „`Abbruch` endet mit 2 seit TB-111, siehe 44.1“ |
| **37.4** | „zweite Öffnung `herkunft.py` vollzogen, TB-111, siehe 44.1“ |
| **43**, unter 43-1 und unter 43-4 | je „vollzogen, siehe 44.1“ |
| **42.2 E2** und **42.3 F8**, unter „Stand, gemessen“ | „vollzogen, siehe 44.2“ |

**Nachweise** wie TB-110: numstat zweite Spalte 0 für das Register; `diff` rc 0 je Zitat; Sonde vorher = nachher gegen `e655c1c8…`; `register()` alt/neu; `test_vorregistrierung` 196/196.

## Block D — Arbeitsweise

- **Nachtrag unter 22.1:** „Seit 26.09.2026 technisch hinterlegt: Der Wächter startet `claude --effort high --remote-control` (Betreiber 26.09.2026, 09:36). Beleg: `docs/belege/TB-113/0b_effort.txt`.“
- **Neuer Abschnitt 22.9 „Die Sitzung wird angelegt, bevor der Satz kommt“** mit dem Wortlaut des Betreibers vom 26.09.2026, 09:31: *„Du sollst immer eine Session anlegen, bevor du mir einen Text mit einem Auftrag gibst.“* Dazu die Regel: Der steuernde Chat legt `starte_TB-<Nr>` an und prüft im Wächter-Log „Satz ins Fenster gelegt“. Hängt noch ein nie abgeschicktes Fenster im Repo, schliesst er es vorher mit `schliesse_<HEAD>`. Erst dann gibt er den Einfügesatz aus. Anlass: TB-112 wartete am 26.09. zweieinhalb Stunden in einem Fenster, das niemand fand.

## Block E — Worktree entfernen

Nach dem Push von `main`: `git worktree remove ../trading-bot-tb111`, danach `git worktree list` (nur noch der Hauptordner). Der Zweig `tb-111` bleibt.

## Commits

1. Schritt 0;
2. der Merge-Commit;
3. Register 44 samt Marken;
4. Arbeitsweise;
5. Journal, Belege, `docs/ERGEBNIS_TB-113_zusammenfuehrung_tb111_register_44.md` (mit „Für Fable“ und „In einfacher Sprache“).

Nach jedem Commit Push.

## ⚠️ Abbruchkriterien — melden, nicht reparieren

- `merge-tree` meldet einen Konflikt, oder die Schnittmenge ist nicht leer.
- Nach dem Merge: Sonde (ii) ≠ 0, Benchmark ≠ `64fb2912…`, ein Test rot, oder ohne Modus eine Ausgabe verändert.
- `numstat` des Registers mit zweiter Spalte ≠ 0.

## In einfacher Sprache

Die Nebenarbeit von gestern Nacht (TB-111) wird mit dem Hauptstand zusammengeführt und danach neu geprüft. Das Regelwerk bekommt Abschnitt 44: Dort steht, was TB-111 und TB-112 tatsächlich umgesetzt haben, und an den alten Stellen stehen Verweise darauf. Der Wächter startet Sitzungen künftig mit hohem Aufwand, und die neue Regel „erst Sitzung anlegen, dann Auftragstext“ kommt in die Arbeitsweise. Zum Schluss wird der Hilfsordner der Nebenarbeit entfernt.
