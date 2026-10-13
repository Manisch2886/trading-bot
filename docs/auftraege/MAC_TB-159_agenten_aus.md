# TB-159 Agenten-Schalter: Agent 1, 3 und 4 abschalten über `config/agenten_aus.txt` — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 13.10.2026, 22:45** (Helfer BAU159, per Skript aus Bausteinen, `$HOME/sc/tb159/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an einer Kopie simuliert. Urteil und Freigabe liegen beim steuernden Chat; zwei frische Gegenleser sind Pflicht. **Gebaut am HEAD `300ba31`.**

**Sitzungstitel:** `TB-159` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `300ba31997802dbc4293397c338117d6f9e06d5b` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-159`), nicht von Hand.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-159_agenten_aus.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), kurz `PY`; das Werkzeug `docs/belege/TB-159/tb159_werkzeug.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-159/`. **Ergebnis:** `docs/ERGEBNIS_TB-159_agenten_aus.md`. **Journal:** die nächste freie Kennung zur Laufzeit (`PY WZ kennung`, Schritt C), unten `<Kennung>`; am Bau-HEAD höchste ET ⇒ EU.
**Ziel:** Der Betreiber (13.10.2026, 21:00): „schalte die bewertenden agents ab … wir können sie später bei bedarf wieder aktivieren“. Agent 1 (`shared/daily_interpreter.py`), Agent 3 (`shared/market_context_agent.py`) und Agent 4 (`shared/portfolio_interpreter_agent.py`) fragen am Anfang `agent_abgeschaltet(name)` in `shared/claude_client.py`; steht ihr Name in der verfolgten Datei `config/agenten_aus.txt`, rufen sie die API nicht auf und geben `""` zurück — wie heute bei einem fehlgeschlagenen Aufruf. Dazu neue Tests, eine Zeile im Backlog, Ergebnis und Journal.
**Bauart:** Code-Änderung mit Tests, Mac-Testauftrag nach ARBEITSWEISE 7c; Vorbild `docs/auftraege/MAC_TB-143_waechter_modus_schalter.md` (Einbau per Skript mit `assert` auf den Anker), Schritt 0, Abbruchweg und Anhang „Dateien und ihre Befehle“ wie `MAC_TB-157_regelwerk_nachtrag_1013.md`; bei Widerspruch gilt dieser Auftrag, und es gelten nur die Schritte, die hier stehen.
**ARBEITSWEISE 7c — die acht Punkte und wo sie hier stehen:**

| Punkt aus 7c | hier |
|---|---|
| Schritt 0: Sicherung der neun `*.db` mit Quersummen | Schritt 0c (`$TMPDIR/tb159_db/`, `0c_db_sicherung.txt`); nach dem letzten Test 8a (`b_db_nachher.txt`) |
| Datenstand vorher und nachher | 0d (`0d_datenstand_vorher.txt`) und 8a (`b_datenstand_nachher.txt`): md5-Liste über `data/*`; mit dem 7c-Sollwert `d9449faf…` (anderes Verfahren) nicht vergleichbar |
| Basislauf mit Zeitgrenze je Datei | Schritt A: je Datei ein Aufruf, 540 s im Werkzeug |
| Interpreter `trading-env/bin/python3` | Kopf (`PY`), jeder Befehl |
| Abbruchkriterium nur für den Gegenstand | Abbruchkriterien |
| `git status --porcelain` nach dem letzten Commit | Schritt C, Abgabe |
| Commit und Push nach jedem fertigen Teil; Belege unter `docs/belege/TB-159/` | ⟨S0⟩, ⟨A⟩, ⟨F⟩ und der letzte Commit in Schritt C |
| „In einfacher Sprache“ | Ergebnis (Schritt C) und Abschnitt unten |

**Zeitgrenze:** jeder Bash-Aufruf der Sitzung mit dem Parameter `timeout` des Bash-Werkzeugs (höchstens 600000 ms; nicht der Shell-Befehl `timeout`, den macOS ohne coreutils nicht hat); die Tests je Datei in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 → A (Basislauf) → B (Einbau erst in einer Kopie, dort Tests, dann ins Repo, Nachlauf, Commit) → C (Backlog, Journal, Ergebnis, Abgabe). **Jede Datei, die die Sitzung schreibt, entsteht mit dem Befehl aus dem Anhang „Dateien und ihre Befehle“** — kein anderer Weg.

## Lage nach dem Auslegen

Am Bau-HEAD `300ba31` gemessen (`git ls-files -m` und `-o --exclude-standard`): geändert `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, `docs/projektfuehrung/UEBERGABE.md`; unverfolgt: nichts. Das Auslegen durch den steuernden Chat ändert dazu den Zeiger in `docs/auftraege/AKTUELLER_AUFTRAG.md` und legt diesen Auftrag ab (unverfolgt). **Beim Start liegen daher genau vier Einträge vor: drei geänderte Dateien und dieser Auftrag** (Soll in 0a).

## ⭐ Freigabe

**Betreiber 13.10.2026, Karte nach 21:00:** „Agent 1, 3 und 4 (Recommended)“ · „Schalterdatei (Recommended)“. Kein Handel, keine Parameter, kein Cron, keine `.env`, keine Schlüssel. Kein Programm ausserhalb des Repos (kein `osascript`, `launchctl`, `kill`, `crontab`).

**Die Sitzung darf ändern, und nichts sonst:**

| Zieldatei | Stücke | numstat-Soll ⟨S0⟩..⟨A⟩ (+ / −) |
|---|---|---|
| `config/agenten_aus.txt` | A1 | **13 / 0** |
| `shared/test_agenten_aus.py` | A2 | **163 / 0** |
| `shared/claude_client.py` | A3 | **32 / 0** |
| `shared/daily_interpreter.py` | A4a, A4b | **4 / 1** |
| `shared/market_context_agent.py` | A5a, A5b | **4 / 1** |
| `shared/portfolio_interpreter_agent.py` | A6a, A6b | **4 / 1** |
| `docs/projektfuehrung/BACKLOG.md` | A7 (eine Zeile vor Z. 197 „## 5 — Nach TB-30b“, Ende Abschnitt 4) | 1 / 0 (in ⟨F⟩) |
| `docs/projektfuehrung/JOURNAL.md` | Block der Sitzung (Schritt C) | Zeilen des Blocks + 3 / 0 (in ⟨F⟩) |
| neu: `docs/belege/TB-159/…`, `docs/ERGEBNIS_TB-159_agenten_aus.md` | Belege, Werkzeug, Ergebnis | — |

**Nicht erlaubt:** jede andere Datei unter `shared/`, `strategies/`, `config/`; Agent 2 (`param_search_agent.py`, `agent_optimise.py`), `quarterly_interpreter.py`, `quarterly_review.py`; `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` nach Schritt 0.

## Belegt · erschlossen · offen

**Belegt (am Bau-HEAD):** Agent 1 `shared/daily_interpreter.py` Z. 43, bei Fehlschlag `""`; Agent 3 `shared/market_context_agent.py` Z. 42, `""`; Agent 4 `shared/portfolio_interpreter_agent.py` Z. 129, `""`. Aufrufer von Agent 1 und 3: nur die neun `strategies/*/daily_summary_email.py` (z. B. `rsi2_crypto` Z. 179/180 und 193/194; die übrigen acht gleich gebaut, `grep -rn` ohne `trading-env/`); Aufrufer von Agent 4: `shared/weekly_portfolio_email.py` Z. 173, `if interpretation:` Z. 174. Jeder Aufrufer prüft `if <ergebnis>:`, ein `""` lässt nur den KI-Teil weg. Die Cron-Zeilen der neun Tagesberichte sind seit 08.09.2026 auskommentiert (Docstring dort).
**Erschlossen:** Die Aufrufer brauchen keine Änderung (F3): bei `""` druckt jeder Tagesbericht „(Keine Einordnung erhalten …)“ bzw. „(Kein Marktkontext erhalten …)“ und verschickt den Bericht ohne KI-Teil; die Wochen-Mail lässt die KI-Einordnung weg und behält die Rohdaten. Die Druckzeile „API-Key gesetzt?“ ist dann irreführend; davor steht die Logzeile „Agent <n> abgeschaltet (config/agenten_aus.txt)“.
**Hinweis:** `test_agent2_zielfunktion.py` ruft `git status --porcelain` im Repo-Ordner; in der Kopie (ohne `.git`) ist dieser Teil leer-grün — massgeblich ist der Lauf im Repo (B8).
**Offen (nur am Mac messbar):** ob die Kopie aus verfolgten Dateien für die Tests reicht (Simulation: ja); Basislauf und Nachlauf mit `trading-env/bin/python3` (3.9); ob Cron die Wochen-Mail nach ⟨A⟩ ohne KI-Teil verschickt (erst beim nächsten Wochenlauf).

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-159/` entsteht:** `git status --porcelain > "$TMPDIR/tb159_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `300ba31997802dbc4293397c338117d6f9e06d5b` und genau diese 4 Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-159_agenten_aus.md
```

Dann das Werkzeug aus Anhang B holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-159_agenten_aus.md "$TMPDIR/tb159_werkzeug.py" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2], "w", encoding="utf-8").write(t)
print("tb159_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb159_werkzeug.py d5a403dd0ffd3ab46d243f9b71c569306dddbcd3a5caaf1bbecadcc4e576c16d`; sonst **ABBRUCH** (vor ⟨S0⟩: nur melden, siehe Abbruchweg). Commit `TB-159 Schritt 0: Stand des steuernden Chats vor TB-159` mit genau den vier Pfaden aus 0a (Block unten), pushen ⇒ **⟨S0⟩**. **Unmittelbar nach dem gepushten ⟨S0⟩:** `mkdir -p docs/belege/TB-159`; erst ab hier gibt es `abbruch.txt` (Abbruchweg). Dann `cp "$TMPDIR/tb159_0a.txt" docs/belege/TB-159/0a_status.txt` und `cp "$TMPDIR/tb159_werkzeug.py" docs/belege/TB-159/tb159_werkzeug.py` (je `cmp` gleich).

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-159_agenten_aus.md
```

**0b. Ausgang** ⇒ `0b_ausgang.txt`, Befehl:

```
{ wc -l shared/claude_client.py shared/daily_interpreter.py shared/market_context_agent.py shared/portfolio_interpreter_agent.py docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md; md5 shared/claude_client.py shared/daily_interpreter.py shared/market_context_agent.py shared/portfolio_interpreter_agent.py docs/projektfuehrung/BACKLOG.md docs/projektfuehrung/JOURNAL.md; } > docs/belege/TB-159/0b_ausgang.txt
```

Soll (am Bau-HEAD `300ba31`): `claude_client.py` 134 Z., `fd034c968454682e81366182ceb9c4f5` · `daily_interpreter.py` 60 Z., `f17b0f1375090ba91ac3fbab3f871d70` · `market_context_agent.py` 84 Z., `c581ad8324e241cbc04fcdbffdcd6f95` · `portfolio_interpreter_agent.py` 174 Z., `7d899df8670e80d9d2242b8f48bbf45b` · `BACKLOG.md` 496 Z., `fd096b8e4cb97315f1b9ffd2bbc3041c` · `JOURNAL.md` 10953 Z., `84b2246ef95ad1616b1ded56287b3ae9`. Weicht eine ab: vermerken; die Anker entscheiden (Schritt B).

**0c. Sicherung der neun `*.db`** (7c; nur lesen — die Sitzung schreibt nie in eine `*.db`), genau diese drei Befehle: `mkdir -p "$TMPDIR/tb159_db"`, `cp -p paper_trading_*.db "$TMPDIR/tb159_db/"`, `md5 paper_trading_*.db "$TMPDIR"/tb159_db/paper_trading_*.db > docs/belege/TB-159/0c_db_sicherung.txt`. Soll: 18 Zeilen, je Datenbank zwei gleiche md5 (Original und Sicherung; am Bau-HEAD 9 Dateien `paper_trading_*.db`). Ungleich, weil ein Cronjob gerade schrieb: Befund unter „Abweichungen“, kein Abbruch.

**0d. Datenstand vorher:** `md5 data/* > docs/belege/TB-159/0d_datenstand_vorher.txt`. Soll: 223 Zeilen (verfolgte Dateien in `data/` am Bau-HEAD).

## Schritt A — Basislauf vor der Änderung

Je Testdatei ein eigener Aufruf (Bash-Zeitgrenze 600000 ms; `WZ basis` bricht eine Datei nach 540 s ab und meldet „Zeitgrenze“), genau dieser Block:

```
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis vorher docs/belege/TB-159/a_basis_vorher.txt shared/test_empfehlung_format.py; echo "rc $?" >> docs/belege/TB-159/a_basis_vorher.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis vorher docs/belege/TB-159/a_basis_vorher.txt shared/test_agent2_kapitalmass.py; echo "rc $?" >> docs/belege/TB-159/a_basis_vorher.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis vorher docs/belege/TB-159/a_basis_vorher.txt shared/test_agent2_zielfunktion.py; echo "rc $?" >> docs/belege/TB-159/a_basis_vorher.txt
```

`WZ basis` hängt je Aufruf eine Zeile „Lauf vorher · … · rc · Dauer · `[OK ]`/`[FEHLER]`-Zeilen · letzte Zeile“ an, dahinter steht `rc <n>`. Soll: drei Zeilen (die Tests der berührten Module), jede gefolgt von `rc 0`. Ist eine rot, **ABBRUCH** (sie betrifft den Gegenstand); ein bekannt roter Test ist hier keiner. **Zählweise:** `test_empfehlung_format`, `test_agent2_zielfunktion` und `test_agenten_aus` zählen mit `[OK ]` (am Bau 70, 41 und 30, Python 3.10); `test_agent2_kapitalmass` hat ein eigenes Format (am Bau „34/34“, `[OK ]` 0). Massgeblich sind rc und letzte Zeile. **Kein API-Aufruf:** Schutz sind die `anthropic`-Platzhalter, die jede der vier Testdateien vorn in `sys.path` legt. Dass `WZ basis` `ANTHROPIC_API_KEY` aus der Umgebung der Läufe nimmt, schützt allein nicht: `get_client()` liest auch `config/email_config.py`.

## Schritt B — Einbau erst in der Kopie, dann ins Repo, Commit ⟨A⟩

Cron führt den Code im Arbeitsbaum aus (F9). Deshalb entsteht die Änderung zuerst in einer Kopie unter `$TMPDIR`; erst wenn dort alle Tests grün sind, kommen die sechs Dateien ins Repo.

1. `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py probe > docs/belege/TB-159/b_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/b_probe.txt` — am Repo, schreibt nichts. Soll: jedes Stück mit „Anker Vorkommen 1“ oder „neu“, die numstat-Sollzeilen wie in der Tabelle oben, „probe: alles gleich, nichts geschrieben“, `rc 0`. Sonst **ABBRUCH** (keinen Anker anpassen, nichts von Hand einfügen).
2. `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py kopie "$TMPDIR/tb159_kopie" > docs/belege/TB-159/b_kopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/b_kopie.txt` — Soll: „kopie: <n> verfolgte Dateien ohne docs/, data/, snapshots/ …“, `rc 0`. Nur verfolgte Dateien: kein `email_config.py`, keine `.env`, keine `*.db`; ohne die Datenordner (die Tests brauchen sie nicht, Simulation).
3. `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py einbau --in "$TMPDIR/tb159_kopie" > docs/belege/TB-159/b_einbau_kopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/b_einbau_kopie.txt` — Soll: „einbau: 6 Dateien geschrieben“, `rc 0`.
4. `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py vergleich --in "$TMPDIR/tb159_kopie" > docs/belege/TB-159/b_vergleich_kopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/b_vergleich_kopie.txt` — Soll: 9 × „GLEICH“, `rc 0`.
5. Die vier Testdateien (die drei aus A und `shared/test_agenten_aus.py`) in der Kopie, je ein Aufruf:

```
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis kopie docs/belege/TB-159/b_basis_kopie.txt shared/test_empfehlung_format.py --in "$TMPDIR/tb159_kopie"; echo "rc $?" >> docs/belege/TB-159/b_basis_kopie.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis kopie docs/belege/TB-159/b_basis_kopie.txt shared/test_agent2_kapitalmass.py --in "$TMPDIR/tb159_kopie"; echo "rc $?" >> docs/belege/TB-159/b_basis_kopie.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis kopie docs/belege/TB-159/b_basis_kopie.txt shared/test_agent2_zielfunktion.py --in "$TMPDIR/tb159_kopie"; echo "rc $?" >> docs/belege/TB-159/b_basis_kopie.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis kopie docs/belege/TB-159/b_basis_kopie.txt shared/test_agenten_aus.py --in "$TMPDIR/tb159_kopie"; echo "rc $?" >> docs/belege/TB-159/b_basis_kopie.txt
```

   Soll: vier Zeilen, jede gefolgt von `rc 0`; die neue Datei endet mit „Alle <n> Pruefungen bestanden.“ Ist eine rot: **ABBRUCH** — im Repo ist dann kein Code geändert, der Abbruch-Commit enthält keine Code-Datei.
6. Erst jetzt ins Repo, genau dieser Block (jedes `cmp` ohne Ausgabe):

```
cp "$TMPDIR/tb159_kopie/config/agenten_aus.txt" config/agenten_aus.txt
cp "$TMPDIR/tb159_kopie/shared/test_agenten_aus.py" shared/test_agenten_aus.py
cp "$TMPDIR/tb159_kopie/shared/claude_client.py" shared/claude_client.py
cp "$TMPDIR/tb159_kopie/shared/daily_interpreter.py" shared/daily_interpreter.py
cp "$TMPDIR/tb159_kopie/shared/market_context_agent.py" shared/market_context_agent.py
cp "$TMPDIR/tb159_kopie/shared/portfolio_interpreter_agent.py" shared/portfolio_interpreter_agent.py
cmp "$TMPDIR/tb159_kopie/config/agenten_aus.txt" config/agenten_aus.txt
cmp "$TMPDIR/tb159_kopie/shared/test_agenten_aus.py" shared/test_agenten_aus.py
cmp "$TMPDIR/tb159_kopie/shared/claude_client.py" shared/claude_client.py
cmp "$TMPDIR/tb159_kopie/shared/daily_interpreter.py" shared/daily_interpreter.py
cmp "$TMPDIR/tb159_kopie/shared/market_context_agent.py" shared/market_context_agent.py
cmp "$TMPDIR/tb159_kopie/shared/portfolio_interpreter_agent.py" shared/portfolio_interpreter_agent.py
```

7. `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py vergleich > docs/belege/TB-159/b_vergleich.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/b_vergleich.txt` — am Repo. Soll wie 4.
8. Dieselben vier Testdateien im Repo, je ein Aufruf:

```
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis nachher docs/belege/TB-159/b_basis_nachher.txt shared/test_empfehlung_format.py; echo "rc $?" >> docs/belege/TB-159/b_basis_nachher.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis nachher docs/belege/TB-159/b_basis_nachher.txt shared/test_agent2_kapitalmass.py; echo "rc $?" >> docs/belege/TB-159/b_basis_nachher.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis nachher docs/belege/TB-159/b_basis_nachher.txt shared/test_agent2_zielfunktion.py; echo "rc $?" >> docs/belege/TB-159/b_basis_nachher.txt
trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py basis nachher docs/belege/TB-159/b_basis_nachher.txt shared/test_agenten_aus.py; echo "rc $?" >> docs/belege/TB-159/b_basis_nachher.txt
```

   Soll wie 5; die neue Datei nennt „Stand der Datei: aus = agent1, agent3, agent4“. Ist eine rot: **ABBRUCH**; `abbruch.txt` und die Meldung beginnen mit „Code im Arbeitsbaum geändert, Cron führt ihn aus — Betreiber entscheidet“.

   8a. Nach dem letzten Test: `md5 paper_trading_*.db > docs/belege/TB-159/b_db_nachher.txt` und `md5 data/* > docs/belege/TB-159/b_datenstand_nachher.txt`, dann `cmp docs/belege/TB-159/0d_datenstand_vorher.txt docs/belege/TB-159/b_datenstand_nachher.txt` (Soll: keine Ausgabe) und die md5 aus `b_db_nachher.txt` gegen 0c. Unterschiede durch laufende Cronjobs sind erwartet: Befund unter „Abweichungen“, kein Abbruch.
9. Commit `TB-159 A: Agent 1, 3 und 4 abschaltbar über config/agenten_aus.txt` (Block unten), pushen ⇒ **⟨A⟩**. Dann `git diff --numstat ⟨S0⟩ ⟨A⟩ > docs/belege/TB-159/b_numstat.txt`; Soll: 21 Zeilen — die sechs der Tabelle oben und 15 Belege aus diesem Block (Zahl aus dem Bauskript).

```
git add config/agenten_aus.txt
git add shared/test_agenten_aus.py
git add shared/claude_client.py
git add shared/daily_interpreter.py
git add shared/market_context_agent.py
git add shared/portfolio_interpreter_agent.py
git add docs/belege/TB-159/0a_status.txt
git add docs/belege/TB-159/tb159_werkzeug.py
git add docs/belege/TB-159/0b_ausgang.txt
git add docs/belege/TB-159/0c_db_sicherung.txt
git add docs/belege/TB-159/0d_datenstand_vorher.txt
git add docs/belege/TB-159/a_basis_vorher.txt
git add docs/belege/TB-159/b_probe.txt
git add docs/belege/TB-159/b_kopie.txt
git add docs/belege/TB-159/b_einbau_kopie.txt
git add docs/belege/TB-159/b_vergleich_kopie.txt
git add docs/belege/TB-159/b_basis_kopie.txt
git add docs/belege/TB-159/b_vergleich.txt
git add docs/belege/TB-159/b_basis_nachher.txt
git add docs/belege/TB-159/b_db_nachher.txt
git add docs/belege/TB-159/b_datenstand_nachher.txt
```

## Schritt C — Backlog, Journal, Ergebnis, Abgabe

**Backlog.** `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py backlog --probe > docs/belege/TB-159/c_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/c_backlog_probe.txt`, dann ohne `--probe`: `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py backlog > docs/belege/TB-159/c_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/c_backlog.txt`. Soll je: vier `ja`, „Zeile als Z. 196“ (so zählt das Werkzeug; die neue Zeile steht danach auf Z. 196, der Anker auf Z. 197+1), `rc 0`. Endet `backlog --probe` nicht mit `rc 0` (auch rc 3): kein Lauf ohne `--probe`, **ABBRUCH**. Stück A7 (Anhang A). Der Punkt „cronjobs für alle 9 daily_summary_email.py deaktivieren“ steht am Bau-HEAD nicht in `BACKLOG*.md` (gesucht); die Zeile kommt deshalb ans Ende von Abschnitt 4.

**Journal.** Zuerst `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py kennung docs/belege/TB-159/c_kennung.txt; echo "rc $?" >> docs/belege/TB-159/c_kennung.txt` (Soll: „Kennung EU …“, dahinter `rc 0`): die nächste freie Kennung zur Laufzeit (am Bau-HEAD höchste ET ⇒ EU; weicht HEAD ab, etwa weil TB-158 vorher lief, bricht 0a vor ⟨S0⟩ ab und der Auftrag wird neu gebaut); sie gilt für Block und Commit, unten `<Kennung>`. Dann schreibt die Sitzung ihren Block nach `docs/belege/TB-159/c_block.md` (Schreibwerkzeug von Claude Code, Gliederung Anhang C). Dann `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py journal docs/belege/TB-159/c_block.md --probe > docs/belege/TB-159/c_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/c_journal_probe.txt` und ohne `--probe`: `trading-env/bin/python3 -B docs/belege/TB-159/tb159_werkzeug.py journal docs/belege/TB-159/c_block.md > docs/belege/TB-159/c_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-159/c_journal.txt`. Soll: sechs Bedingungen `ja`, `rc 0`.

**Ergebnis** `docs/ERGEBNIS_TB-159_agenten_aus.md` (Schreibwerkzeug): Kopf (Stand, Commits ⟨S0⟩, ⟨A⟩) · „Kurz“ (Schritt · Soll · Ist) · „Basislauf und Nachlauf“ (je Datei rc, `[OK ]`-Zahl, Dauer — vorher und nachher) · „Belege“ (Datei · was · Befehl · Bytes · Zeilen · md5; `f_porcelain.txt` und `f_numstat.txt` entstehen erst nach ⟨F⟩) · „Abweichungen“ · „Festlegung F10“ (Schalterdatei vorhanden, aber nicht lesbar ⇒ Agent aus, Warnzeile im Log) · **„So schaltest du einen Agent wieder ein“** (die Zeile in `config/agenten_aus.txt` löschen oder ein `#` davorsetzen, speichern, committen; Datei ganz weg = alle drei an) · **„In einfacher Sprache“**.

**Abgabe.** Commit `TB-159 Abgabe: Ergebnis, Journal <Kennung>` (erster Block unten), pushen ⇒ **⟨F⟩**. Dann `git status --porcelain > "$TMPDIR/tb159_f.txt"`, `cp "$TMPDIR/tb159_f.txt" docs/belege/TB-159/f_porcelain.txt` (`cmp` gleich; Soll 0 B), erst danach `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-159/f_numstat.txt`. Commit `TB-159 F: porcelain und numstat nach der Abgabe` (zweiter Block), pushen. Zuletzt `git status --porcelain` im Chat melden (Soll leer).

```
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-159_agenten_aus.md
git add docs/belege/TB-159/b_numstat.txt
git add docs/belege/TB-159/c_backlog_probe.txt
git add docs/belege/TB-159/c_backlog.txt
git add docs/belege/TB-159/c_kennung.txt
git add docs/belege/TB-159/c_block.md
git add docs/belege/TB-159/c_journal_probe.txt
git add docs/belege/TB-159/c_journal.txt
```

```
git add docs/belege/TB-159/f_porcelain.txt
git add docs/belege/TB-159/f_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab.
- Schritt A: eine Testdatei rc ≠ 0 oder Zeitgrenze.
- Schritt B: `probe`, `kopie`, `einbau` oder `vergleich` endet nicht mit rc 0; in der Kopie (B5) oder im Repo (B8) ist eine Testdatei rot; ein `cp` oder `cmp` in B6 scheitert. Kein Stück von Hand einfügen, keinen Anker anpassen, keinen Test ändern.
- Schritt C: `kennung`, `backlog --probe`, `backlog`, `journal … --probe` oder `journal` endet nicht mit `rc 0` (auch rc 3, rc 64 oder eine Python-Ausnahme, rc 1). Der Code ist dann schon im Repo ⇒ Pflichtsatz zuerst (Abbruchweg).
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung:** melden, nicht umgehen; verlangt schon Schritt 0 oder der Abbruchweg eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage im Chat melden.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal (gilt **nicht** für den Push des Abbruch-Commits, siehe Abbruchweg).

**Kein Abbruch:** 0b weicht ab; md5 der `*.db` (0c, 8a) oder der Datenstand (8a) weichen ab — laufende Cronjobs; `b_numstat.txt`, `f_numstat.txt` oder `f_porcelain.txt` weichen ab — je weiter, unter „Abweichungen“ nennen. **Scheitert dagegen ein Befehl selbst** (rc ≠ 0, Glob ohne Treffer, fehlende Datei): in 0c oder 0d **ABBRUCH** (noch kein Code geändert); in 8a weiter, unter „Abweichungen“ nennen.

**Abbruchweg — so wenig schreiben wie möglich.** **Solange ⟨S0⟩ nicht gepusht ist** (0a weicht ab, der sha256 des Werkzeugs weicht ab, Commit oder Push von ⟨S0⟩ scheitert): nichts schreiben, nichts committen, nur im Chat melden (die Abweichung wörtlich). **Ab dem gepushten ⟨S0⟩** (der Ordner `docs/belege/TB-159/` steht dann): genau eine neue Datei, `printf '%s\n' "<Schritt>: <Grund, ein Satz>" > docs/belege/TB-159/abbruch.txt` (sie beschreibt sich selbst, keine Kopfdatei); dann `git add docs/belege/TB-159/abbruch.txt` und je eine Zeile `git add <Pfad>` **mit dem Namen** jeder Datei aus dem Anhang „Dateien und ihre Befehle“, die im Repo schon entstanden oder geändert und noch nicht committet ist — geschriebene Zieldateien eingeschlossen; die Meldung nennt diese Zieldateien als Erstes. **Abbruch in B1–B5:** keine Code-Datei im Repo ist geändert, der Abbruch-Commit enthält nur Belege. **Abbruch ab B6 (auch in Schritt C):** `abbruch.txt` und die Meldung beginnen mit „Code im Arbeitsbaum geändert, Cron führt ihn aus — Betreiber entscheidet“; die Code-Dateien kommen mit in den Abbruch-Commit. Commit `TB-159 Abbruch: <Schritt>`, pushen, melden. **Scheitert Commit oder Push des Abbruch-Commits: nicht wiederholen, kein Ersatzbefehl, anhalten, nur melden** — kein zweiter Abbruchweg, kein neuer Commit; die Regel „`git push` scheitert zweimal“ gilt nicht für den Abbruch-Commit. Nichts zurückdrehen (kein `git reset`, `revert`, `restore`, `checkout`); die Dateien unter `$TMPDIR` bleiben liegen.

## Nicht in TB-159

- Agent 2 (`param_search_agent.py`, `agent_optimise.py`), `quarterly_interpreter.py`, `quarterly_review.py`, `call_claude` im Übrigen — unberührt (F1).
- Die Druckzeilen „API-Key gesetzt?“ in den Aufrufern — bleiben; sie verhindern nichts (F3: keine Änderung nötig).
- Crontab, `.env`, Schlüssel, Handel, Parameter.

## In einfacher Sprache

Drei KI-Helfer schreiben bisher Einordnungen in die Berichte: zu den neun Tagesberichten, zu den Nachrichten über offene Positionen und zur Wochen-Mail. Jede Anfrage kostet Geld. Nach diesem Auftrag fragt jeder dieser Helfer zuerst eine kleine Liste ab, `config/agenten_aus.txt`. Steht er darin, fragt er die KI nicht und der Bericht geht ohne KI-Teil raus — die Zahlen bleiben. Wieder einschalten: die Zeile mit seinem Namen aus der Liste löschen und committen.

## Anhang — Dateien und ihre Befehle

Jede Datei, die die Sitzung schreibt, mit dem einzigen erlaubten Befehl (Einzelheiten im Schritt).

| Datei | Befehl |
|---|---|
| `docs/belege/TB-159/0a_status.txt` | `git status --porcelain > "$TMPDIR/tb159_0a.txt"`, nach ⟨S0⟩ `cp` (Schritt 0a) |
| `docs/belege/TB-159/tb159_werkzeug.py` | Holbefehl aus Schritt 0a nach `$TMPDIR`, nach ⟨S0⟩ `cp` |
| `docs/belege/TB-159/0b_ausgang.txt` | Block in Schritt 0b |
| `docs/belege/TB-159/0c_db_sicherung.txt` | `md5 paper_trading_*.db "$TMPDIR"/tb159_db/paper_trading_*.db > docs/belege/TB-159/0c_db_sicherung.txt` (Schritt 0c, nach `cp -p` der `*.db`) |
| `docs/belege/TB-159/0d_datenstand_vorher.txt` | `md5 data/* > docs/belege/TB-159/0d_datenstand_vorher.txt` (Schritt 0d) |
| `docs/belege/TB-159/a_basis_vorher.txt` | `PY WZ basis vorher …` (Schritt A) |
| `docs/belege/TB-159/b_probe.txt` | `PY WZ probe > …` (Schritt B1) |
| `docs/belege/TB-159/b_kopie.txt` | `PY WZ kopie … > …` (Schritt B2) |
| `docs/belege/TB-159/b_einbau_kopie.txt` | `PY WZ einbau --in … > …` (Schritt B3) |
| `docs/belege/TB-159/b_vergleich_kopie.txt` | `PY WZ vergleich --in … > …` (Schritt B4) |
| `docs/belege/TB-159/b_basis_kopie.txt` | `PY WZ basis kopie … --in …` (Schritt B5) |
| `docs/belege/TB-159/b_vergleich.txt` | `PY WZ vergleich > …` (Schritt B7) |
| `docs/belege/TB-159/b_basis_nachher.txt` | `PY WZ basis nachher …`, je Datei (Schritt B8) |
| `docs/belege/TB-159/b_db_nachher.txt` | `md5 paper_trading_*.db > docs/belege/TB-159/b_db_nachher.txt` (Schritt 8a) |
| `docs/belege/TB-159/b_datenstand_nachher.txt` | `md5 data/* > docs/belege/TB-159/b_datenstand_nachher.txt` (Schritt 8a) |
| `docs/belege/TB-159/b_numstat.txt` | `git diff --numstat ⟨S0⟩ ⟨A⟩ > …` (Schritt B) |
| `docs/belege/TB-159/c_backlog_probe.txt` | `PY WZ backlog --probe > …` (Schritt C) |
| `docs/belege/TB-159/c_backlog.txt` | `PY WZ backlog > …` (Schritt C) |
| `docs/belege/TB-159/c_kennung.txt` | `PY WZ kennung …` (Schritt C) |
| `docs/belege/TB-159/c_block.md` | Schreibwerkzeug von Claude Code, Gliederung Anhang C |
| `docs/belege/TB-159/c_journal_probe.txt` | `PY WZ journal … --probe > …` (Schritt C) |
| `docs/belege/TB-159/c_journal.txt` | `PY WZ journal … > …` (Schritt C) |
| `docs/ERGEBNIS_TB-159_agenten_aus.md` | Schreibwerkzeug von Claude Code, Gliederung Schritt C |
| `docs/belege/TB-159/f_porcelain.txt` | `git status --porcelain > "$TMPDIR/tb159_f.txt"`, dann `cp` (Schritt C) |
| `docs/belege/TB-159/f_numstat.txt` | `git diff --numstat ⟨S0⟩ ⟨F⟩ > …` (Schritt C) |
| `docs/belege/TB-159/abbruch.txt` | nur bei Abbruch: `printf '%s\n' "…" > …` (Abbruchweg) |
| `config/agenten_aus.txt` | `cp` aus `$TMPDIR/tb159_kopie/` (Schritt B6), Stück A1 |
| `shared/test_agenten_aus.py` | `cp` aus `$TMPDIR/tb159_kopie/` (Schritt B6), Stück A2 |
| `shared/claude_client.py` | `cp` aus `$TMPDIR/tb159_kopie/` (Schritt B6), eingebaut dort mit `PY WZ einbau --in …` |
| `shared/daily_interpreter.py` | `cp` aus `$TMPDIR/tb159_kopie/` (Schritt B6), eingebaut dort mit `PY WZ einbau --in …` |
| `shared/market_context_agent.py` | `cp` aus `$TMPDIR/tb159_kopie/` (Schritt B6), eingebaut dort mit `PY WZ einbau --in …` |
| `shared/portfolio_interpreter_agent.py` | `cp` aus `$TMPDIR/tb159_kopie/` (Schritt B6), eingebaut dort mit `PY WZ einbau --in …` |
| `docs/projektfuehrung/BACKLOG.md` | `PY WZ backlog` (Schritt C) |
| `docs/projektfuehrung/JOURNAL.md` | `PY WZ journal …` (Schritt C) |
| $TMPDIR/tb159_0a.txt, $TMPDIR/tb159_werkzeug.py, $TMPDIR/tb159_kopie/ (Kopie, Schritt B2–B5), $TMPDIR/tb159_db/ (Sicherung der `*.db`, 0c), $TMPDIR/tb159_f.txt | Befehle in Schritt 0a, B und C; bleiben liegen — nicht löschen (`deny`: `Bash(rm:*)`), nicht committen |

## Anhang A — Stücke (wörtlich)

Jedes Stück setzt `WZ einbau` (A1–A6b) bzw. `WZ backlog` (A7) ein; der Anker ist eine ganze Zeile und muss genau einmal vorkommen. „danach“/„davor“: die Zeilen des Blocks kommen hinter/vor die Ankerzeile; „ersetzen“: die Ankerzeile wird durch die eine Zeile des Blocks ersetzt; „neu“: ganze Datei.

#### A1 — `config/agenten_aus.txt`, neu · 13 Zeilen

```text
# Abgeschaltete Agenten (TB-159, 13.10.2026)
#
# Je Zeile ein Name: agent1 (Einordnung der neun Tagesberichte),
# agent3 (Marktkontext per Web-Suche), agent4 (Einordnung der Wochen-Mail).
# Ein Agent, der hier steht, ruft die Claude-API nicht auf; sein Bericht
# geht ohne KI-Teil raus. Alles hinter # ist Kommentar.
#
# So schaltest du einen Agent wieder ein: die Zeile mit seinem Namen löschen
# (oder ein # davorsetzen), speichern, committen. Fehlt diese Datei ganz,
# laufen alle drei Agenten wie vor TB-159.
agent1
agent3
agent4
```

#### A2 — `shared/test_agenten_aus.py`, neu · 163 Zeilen

```python
"""
Selbsttests: der Agenten-Schalter config/agenten_aus.txt (TB-159)
====================================================================
Prueft claude_client.agent_abgeschaltet() (an, aus, Datei fehlt,
Kommentar, unbekannter Name, nicht lesbar) und dass die Agenten 1, 3 und 4
bei "aus" die API NICHT aufrufen und dasselbe zurueckgeben wie bei einem
fehlgeschlagenen Aufruf (leerer Text).

Kein Test ruft die API auf: anthropic wird als Platzhalter-Modul in einem
temporaeren Verzeichnis angelegt (wirft beim Erzeugen eines Clients), und
call_claude wird in jedem Agent-Modul durch eine Zaehlfunktion ersetzt.
Die Schalterdateien der Faelle liegen im temporaeren Verzeichnis; die
verfolgte config/agenten_aus.txt wird nur gelesen.

Nutzung:  python3 shared/test_agenten_aus.py
"""

import contextlib
import inspect
import io
import os
import sys
import tempfile

DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(DIR)

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append(bool(ok))
    print(f"  [{'OK ' if ok else 'FEHLER'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        raise SystemExit(f"\nFEHLGESCHLAGEN: {name}\n{detail}")


STUB_DIR = tempfile.mkdtemp(prefix="tb159_stubs_")
with open(os.path.join(STUB_DIR, "anthropic.py"), "w") as f:
    f.write("class Anthropic:\n"
            "    def __init__(self, *a, **k):\n"
            "        raise RuntimeError('Test darf die API nicht aufrufen')\n")
sys.path.insert(0, STUB_DIR)
sys.path.insert(0, DIR)

import claude_client                      # noqa: E402
import daily_interpreter                  # noqa: E402
import market_context_agent               # noqa: E402
import portfolio_interpreter_agent        # noqa: E402

ARBEIT = tempfile.mkdtemp(prefix="tb159_schalter_")
FEHLT = os.path.join(ARBEIT, "gibt_es_nicht.txt")


def schalterdatei(inhalt):
    pfad = os.path.join(ARBEIT, "agenten_aus.txt")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(inhalt)
    return pfad


def abfrage(name, pfad):
    puffer = io.StringIO()
    with contextlib.redirect_stdout(puffer):
        ergebnis = claude_client.agent_abgeschaltet(name, pfad)
    return ergebnis, puffer.getvalue()


def teste_funktion():
    print("\n1) agent_abgeschaltet()")
    p = schalterdatei("# Kopf\nagent1\nagent3\nagent4\n")
    for name, n in (("agent1", "1"), ("agent3", "3"), ("agent4", "4")):
        aus, log = abfrage(name, p)
        check(f"aus: {name} steht in der Datei", aus is True)
        check(f"aus: {name} schreibt die Logzeile",
              log.strip() == f"Agent {n} abgeschaltet (config/agenten_aus.txt)", repr(log))
    aus, log = abfrage("agent1", schalterdatei("agent3\n"))
    check("an: agent1 fehlt in der Datei, keine Logzeile", aus is False and log == "", repr(log))
    check("Datei fehlt: alle drei an, keine Logzeile",
          all(abfrage(a, FEHLT) == (False, "") for a in ("agent1", "agent3", "agent4")))
    p = schalterdatei("# agent1\n  # agent3 ist aus\nagent4   # Wochen-Mail\n\n")
    check("Kommentar: auskommentierte Zeilen schalten nicht ab",
          abfrage("agent1", p)[0] is False and abfrage("agent3", p)[0] is False)
    check("Kommentar hinter dem Namen wird abgeschnitten", abfrage("agent4", p)[0] is True)
    p = schalterdatei("agent9\nagent 1\nAgent1\nagent13\n")
    check("unbekannte Namen schalten keinen der drei ab",
          all(abfrage(a, p)[0] is False for a in ("agent1", "agent3", "agent4")))
    aus, log = abfrage("agent1", ARBEIT)   # ein Verzeichnis statt einer Datei: nicht lesbar
    check("nicht lesbare Schalterdatei: Agent bleibt aus, mit Warnung",
          aus is True and "nicht lesbar" in log, repr(log))


def teste_agenten():
    print("\n2) Die drei Agenten: aus = kein API-Aufruf, an = genau ein Aufruf")
    aufrufe = []

    def zaehler(*a, **k):
        aufrufe.append(a)
        return {"success": True, "text": "TESTTEXT", "stop_reason": "end_turn", "raw": None}

    faelle = (("agent1", daily_interpreter,
               lambda: daily_interpreter.generate_interpretation("bot", "Zusammenfassung")),
              ("agent3", market_context_agent,
               lambda: market_context_agent.get_market_context(["BTCUSDT"], "bot")),
              ("agent4", portfolio_interpreter_agent,
               lambda: portfolio_interpreter_agent.generate_portfolio_interpretation("Uebersicht")))
    alt = claude_client.AGENTEN_AUS_DATEI
    try:
        for name, modul, aufruf in faelle:
            original = modul.call_claude
            modul.call_claude = zaehler
            try:
                claude_client.AGENTEN_AUS_DATEI = schalterdatei(name + "\n")
                del aufrufe[:]
                puffer = io.StringIO()
                with contextlib.redirect_stdout(puffer):
                    ergebnis = aufruf()
                check(f"{name} aus: leerer Text, kein Aufruf von call_claude",
                      ergebnis == "" and aufrufe == [], f"{ergebnis!r}, {len(aufrufe)} Aufrufe")
                check(f"{name} aus: Logzeile", "abgeschaltet (config/agenten_aus.txt)" in puffer.getvalue())
                claude_client.AGENTEN_AUS_DATEI = FEHLT
                ergebnis = aufruf()
                check(f"{name} an (Datei fehlt): genau ein Aufruf, Text kommt durch",
                      ergebnis == "TESTTEXT" and len(aufrufe) == 1, f"{ergebnis!r}, {len(aufrufe)} Aufrufe")
            finally:
                modul.call_claude = original
    finally:
        claude_client.AGENTEN_AUS_DATEI = alt


def teste_quelle():
    print("\n3) Die Pruefung liest nur die Schalterdatei")
    quelle = inspect.getsource(claude_client.agent_abgeschaltet)
    for wort in ("environ", "getenv", "email_config", "API_KEY", "get_client", "call_claude"):
        check(f"agent_abgeschaltet() enthaelt kein '{wort}'", wort not in quelle)
    check("Pfad ist config/agenten_aus.txt im Repo",
          claude_client.AGENTEN_AUS_DATEI == os.path.join(REPO_ROOT, "config", "agenten_aus.txt"))


def teste_verfolgte_datei():
    print("\n4) Die verfolgte Schalterdatei (Inhalt darf sich aendern)")
    pfad = claude_client.AGENTEN_AUS_DATEI
    if not os.path.isfile(pfad):
        check("Datei fehlt - zulaessig, alle drei Agenten laufen", True)
        return
    with open(pfad, encoding="utf-8") as f:
        inhalt = f.read()
    namen = [z.split("#", 1)[0].strip() for z in inhalt.splitlines()]
    namen = [n for n in namen if n]
    check("jeder Name ist agent1, agent3 oder agent4",
          all(n in ("agent1", "agent3", "agent4") for n in namen), repr(namen))
    check("Kopfkommentar sagt, wie man wieder einschaltet",
          "wieder ein" in inhalt and "löschen" in inhalt)
    print(f"  Stand der Datei: aus = {', '.join(namen) or 'keiner'}")


if __name__ == "__main__":
    print("Selbsttests Agenten-Schalter (TB-159)")
    teste_funktion()
    teste_agenten()
    teste_quelle()
    teste_verfolgte_datei()
    print(f"\nAlle {len(CHECKS)} Pruefungen bestanden.")
```

#### A3 — `shared/claude_client.py`, danach

Anker: ⟦MODEL_HAIKU = "claude-haiku-4-5-20251001"⟧ (am Bau-HEAD Z. 31) · 32 Zeilen

```python

# TB-159: Schalterdatei fuer die bewertenden Agenten 1, 3 und 4. Je Zeile ein
# Name (agent1, agent3, agent4), '#' leitet einen Kommentar ein. Steht ein
# Agent darin, ruft er die API nicht auf und gibt zurueck, was er auch bei
# einem fehlgeschlagenen Aufruf zurueckgibt (leerer Text) - der Bericht geht
# dann ohne KI-Teil raus. Wieder einschalten: die Zeile in der Datei loeschen.
AGENTEN_AUS_DATEI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 "config", "agenten_aus.txt")


def agent_abgeschaltet(name: str, pfad: str = None) -> bool:
    """
    True, wenn `name` in der Schalterdatei steht - dann KEIN API-Aufruf.
    Fehlt die Datei oder steht der Name nicht darin: False, der Agent
    laeuft wie bisher. Liest ausschliesslich die Schalterdatei.
    Ist die Datei vorhanden, aber nicht lesbar: True (lieber kein Aufruf
    als ein ungewollter), mit einer Warnung im Log.
    """
    datei = AGENTEN_AUS_DATEI if pfad is None else pfad
    nummer = name[len("agent"):] if name.startswith("agent") else name
    try:
        with open(datei, encoding="utf-8") as f:
            zeilen = f.read().splitlines()
    except FileNotFoundError:
        return False
    except (OSError, UnicodeDecodeError) as e:
        print(f"Warnung: config/agenten_aus.txt nicht lesbar ({e}) - Agent {nummer} bleibt aus")
        return True
    if name not in {z.split("#", 1)[0].strip() for z in zeilen}:
        return False
    print(f"Agent {nummer} abgeschaltet (config/agenten_aus.txt)")
    return True
```

#### A4a — `shared/daily_interpreter.py`, ersetzen

Anker: ⟦from claude_client import call_claude, MODEL_HAIKU⟧ (am Bau-HEAD Z. 15) · 1 Zeilen

```python
from claude_client import call_claude, MODEL_HAIKU, agent_abgeschaltet
```

#### A4b — `shared/daily_interpreter.py`, davor

Anker: ⟦    user_message = f"Strategie: {strategy_name}\n\nTages-Zusammenfassung:\n{summary_text}"⟧ (am Bau-HEAD Z. 48) · 3 Zeilen

```python
    if agent_abgeschaltet("agent1"):
        return ""

```

#### A5a — `shared/market_context_agent.py`, ersetzen

Anker: ⟦from claude_client import call_claude⟧ (am Bau-HEAD Z. 21) · 1 Zeilen

```python
from claude_client import call_claude, agent_abgeschaltet
```

#### A5b — `shared/market_context_agent.py`, davor

Anker: ⟦    if not symbols:⟧ (am Bau-HEAD Z. 51) · 3 Zeilen

```python
    if agent_abgeschaltet("agent3"):
        return ""

```

#### A6a — `shared/portfolio_interpreter_agent.py`, ersetzen

Anker: ⟦from claude_client import call_claude, MODEL_SONNET⟧ (am Bau-HEAD Z. 38) · 1 Zeilen

```python
from claude_client import call_claude, MODEL_SONNET, agent_abgeschaltet
```

#### A6b — `shared/portfolio_interpreter_agent.py`, davor

Anker: ⟦    if not overview_text or not overview_text.strip():⟧ (am Bau-HEAD Z. 136) · 3 Zeilen

```python
    if agent_abgeschaltet("agent4"):
        return ""

```

#### A7 — `docs/projektfuehrung/BACKLOG.md`, davor (Leerzeile vor dem Anker)

Anker: ⟦## 5 — Nach TB-30b⟧ (am Bau-HEAD Z. 197) · 1 Zeilen

```text
| **K4v** | **TB-159 (13.10.2026): Agent 1, 3 und 4 abgeschaltet über die verfolgte Schalterdatei `config/agenten_aus.txt`** (Betreiber 13.10.2026, 21:00: „schalte die bewertenden agents ab … wir können sie später bei bedarf wieder aktivieren“). Ein abgeschalteter Agent ruft die API nicht auf, schreibt „Agent <n> abgeschaltet (config/agenten_aus.txt)“ ins Log, der Bericht geht ohne KI-Teil raus. Die Cron-Zeilen der neun `daily_summary_email.py` sind seit 08.09.2026 auskommentiert (Docstring dort); der Schalter wirkt zusätzlich bei manuellem Aufruf und auf die Wochen-Mail (Agent 4). **Wieder einschalten:** die Zeile in `config/agenten_aus.txt` löschen, committen. Nicht berührt: Agent 2, `quarterly_interpreter.py`. Ergebnis `docs/ERGEBNIS_TB-159_agenten_aus.md`. |
```

## Anhang B — Werkzeug

### Werkzeug

```python
# TB-159 Werkzeug (Anhang B des Auftrags): probe, kopie, einbau, vergleich, basis, backlog, kennung, journal. Nur Standardbibliothek, Python 3.9.
# Liest die Stuecke wortlich aus dem Auftrag (Anhang A); jeder Anker muss genau einmal als ganze Zeile vorkommen, sonst wird nichts geschrieben.
import os, re, shutil, subprocess, sys, time
AUFTRAG = "docs/auftraege/MAC_TB-159_agenten_aus.md"
PLAN = [['A1', 'config/agenten_aus.txt', 'neu', None], ['A2', 'shared/test_agenten_aus.py', 'neu', None], ['A3', 'shared/claude_client.py', 'danach', 'MODEL_HAIKU = "claude-haiku-4-5-20251001"'], ['A4a', 'shared/daily_interpreter.py', 'ersetzen', 'from claude_client import call_claude, MODEL_HAIKU'], ['A4b', 'shared/daily_interpreter.py', 'davor', '    user_message = f"Strategie: {strategy_name}\\n\\nTages-Zusammenfassung:\\n{summary_text}"'], ['A5a', 'shared/market_context_agent.py', 'ersetzen', 'from claude_client import call_claude'], ['A5b', 'shared/market_context_agent.py', 'davor', '    if not symbols:'], ['A6a', 'shared/portfolio_interpreter_agent.py', 'ersetzen', 'from claude_client import call_claude, MODEL_SONNET'], ['A6b', 'shared/portfolio_interpreter_agent.py', 'davor', '    if not overview_text or not overview_text.strip():']]
TESTS = ["shared/test_empfehlung_format.py", "shared/test_agent2_kapitalmass.py", "shared/test_agent2_zielfunktion.py"]
NEU_TEST = "shared/test_agenten_aus.py"
OHNE = ("docs/", "data/", "snapshots/")  # Kopie ohne Doku und ohne die beiden grossen Datenordner (zusammen rund 420 MB)
BL, BL_ANKER, BL_ZEILE = "docs/projektfuehrung/BACKLOG.md", "## 5 — Nach TB-30b", "A7"
JO, JO_ANKER = "docs/projektfuehrung/JOURNAL.md", "## Wiederkehrende Lehren"
_ST = {}


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def schreib(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def stuecke():
    if _ST:
        return _ST
    z, s = lies(AUFTRAG).split("\n"), _ST
    for i, l in enumerate(z):
        m = re.match(r"^#### (A\d+[a-z]?) — ", l)
        if m:
            a = next(j for j in range(i + 1, len(z)) if z[j].startswith("```") and len(z[j]) > 3)
            assert m.group(1) not in s, "Stueck doppelt: " + m.group(1)
            s[m.group(1)] = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
    return s


def zeilen(t):
    return t[:-1].split("\n")


def entwurf():
    st, fehler, neu, soll = stuecke(), [], {}, {}
    for sid, pfad, art, anker in PLAN:
        if sid not in st:
            fehler.append("%s fehlt im Auftrag" % sid)
            continue
        tz = zeilen(st[sid])
        if art == "neu":
            if os.path.exists(pfad):
                fehler.append("%s gibt es schon" % pfad)
            neu[pfad] = st[sid]
            soll[pfad] = [len(tz), 0]
            print("%s %s neu · %d Zeilen" % (sid, pfad, len(tz)))
            continue
        z = (neu[pfad] if pfad in neu else lies(pfad)).split("\n")
        n = z.count(anker)
        print("%s %s %s · Anker Vorkommen %d%s" % (sid, pfad, art, n, " · Z. %d" % (z.index(anker) + 1) if n == 1 else ""))
        if n != 1:
            fehler.append("%s Anker %d-mal" % (sid, n))
            continue
        i = z.index(anker)
        if art == "ersetzen":
            z[i:i + 1] = tz
        elif art == "davor":
            z[i:i] = tz
        else:
            z[i + 1:i + 1] = tz
        neu[pfad] = "\n".join(z)
        s = soll.setdefault(pfad, [0, 0])
        s[0] += len(tz)
        s[1] += 1 if art == "ersetzen" else 0
    for p, t in neu.items():
        if p.endswith(".py"):
            try:
                compile(t, p, "exec")
            except SyntaxError as e:
                fehler.append("%s nicht uebersetzbar: %s" % (p, e))
    return neu, soll, fehler


def kopie(ziel):
    if os.path.exists(ziel):
        print("NEIN: %s gibt es schon - nichts kopiert" % ziel)
        return 3
    ls = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"], capture_output=True, check=True).stdout.decode("utf-8")
    n = b = 0
    for p in ls.split("\0"):
        if not p or p.startswith(OHNE) or not os.path.isfile(p):
            continue
        os.makedirs(os.path.join(ziel, os.path.dirname(p)), exist_ok=True)
        shutil.copy2(p, os.path.join(ziel, p))
        n, b = n + 1, b + os.path.getsize(p)
    print("kopie: %d verfolgte Dateien ohne docs/, data/, snapshots/, %d B, nach %s" % (n, b, ziel))
    return 0


def einbau(probe):
    neu, soll, fehler = entwurf()
    for p in sorted(soll):
        print("Soll numstat %s %d / %d" % (p, soll[p][0], soll[p][1]))
    if fehler:
        print("NEIN: " + "; ".join(fehler) + " - nichts geschrieben")
        return 3
    if not probe:
        for p, t in neu.items():
            schreib(p, t)
    print("probe: alles gleich, nichts geschrieben" if probe else "einbau: %d Dateien geschrieben" % len(neu))
    return 0


def vergleich():
    st, ok = stuecke(), True
    for sid, pfad, art, anker in PLAN:
        t, z = lies(pfad), lies(pfad).split("\n")
        if art == "neu":
            g = t == st[sid]
        elif art == "ersetzen":
            g = z.count(anker) == 0 and z.count(zeilen(st[sid])[0]) == 1
        else:
            block = zeilen(st[sid])
            i = z.index(anker) if z.count(anker) == 1 else -1
            k = i - len(block) if art == "davor" else i + 1
            g = i >= 0 and z[k:k + len(block)] == block and t.count("\n".join(block)) == 1
        ok = ok and g
        print("%s %s · %s" % (sid, pfad, "GLEICH" if g else "NEIN"))
    return 0 if ok else 3


def basis(name, aus, datei):
    liste = TESTS + ([NEU_TEST] if name in ("nachher", "kopie") else [])
    if datei not in liste:
        print("NEIN: %s gehoert nicht zum Lauf %s (%s)" % (datei, name, ", ".join(liste)))
        return 2
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("ANTHROPIC_API_KEY", None)
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "-B", datei], capture_output=True, text=True, timeout=540, env=env)
        rc, ausgabe = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        rc, ausgabe = "Zeitgrenze 540 s", ""
    z = ausgabe.rstrip("\n").split("\n")
    zeile = "Lauf %s · %s · %s · %s · rc %s · %.1f s · [OK ] %d · [FEHLER] %d · letzte Zeile: %s" % (
        name, sys.executable, time.strftime("%d.%m.%Y %H:%M:%S"), datei, rc, time.time() - t0,
        sum("[OK ]" in l for l in z), sum("[FEHLER]" in l for l in z), z[-1][:200])
    with open(aus, "a", encoding="utf-8") as f:
        f.write(zeile + "\n")
    print(zeile)
    return 0 if rc == 0 else 1


def backlog(probe):
    z, zeile = lies(BL).split("\n"), zeilen(stuecke()[BL_ZEILE])[0]
    b = [z.count(BL_ANKER) == 1, z.count(zeile) == 0, "| **K4v** |" not in "\n".join(z)]
    if b[0]:
        i = z.index(BL_ANKER)
        b.append(z[i - 1] == "" and z[i - 2].startswith("| "))
    print("Anker einmal: %s · Zeile neu: %s · K4v frei: %s · Tabellenende davor: %s" % tuple(["ja" if x else "nein" for x in b] + ["?"] * (4 - len(b))))
    if not all(b) or len(b) < 4:
        print("NEIN - nichts geschrieben")
        return 3
    if not probe:
        z.insert(i - 1, zeile)
        schreib(BL, "\n".join(z))
    print("%s: Zeile als Z. %d" % ("probe" if probe else "eingefuegt", i))
    return 0


def naechste():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
    m = max(k)
    return m, (m[0] + chr(ord(m[1]) + 1)) if m[1] != "Z" else chr(ord(m[0]) + 1) + "A"


def kennung(aus):
    letzte, nx = naechste()
    t = "Kennung %s (naechste freie; hoechste vorhandene %s)" % (nx, letzte)
    schreib(aus, t + "\n")
    print(t)
    return 0


def journal(block, probe):
    b, t = lies(block).rstrip("\n").split("\n"), lies(JO)
    z, k = t.split("\n"), re.findall(r"^## ([A-Z]{2}) — TB-", t, re.M)
    letzte, KENNUNG = naechste()
    i = z.index(JO_ANKER) if z.count(JO_ANKER) == 1 else -1
    c = [("Block beginnt mit '## %s — TB-159: ' (naechste freie nach %s)" % (KENNUNG, letzte), b[0].startswith("## %s — TB-159: " % KENNUNG)),
         ("keine weitere '## '-Zeile im Block", sum(l.startswith("## ") for l in b) == 1),
         ("kein '---' im Block", "---" not in b),
         ("Kennung %s noch frei" % KENNUNG, KENNUNG not in k),
         ("Anker einmal", i >= 0),
         ("vor dem Anker '---' und Leerzeile", i >= 2 and z[i - 1] == "" and z[i - 2] == "---")]
    for n, g in c:
        print("%s: %s" % (n, "ja" if g else "nein"))
    if not all(g for _, g in c):
        print("NEIN - nichts geschrieben")
        return 64
    if not probe:
        z[i - 1:i - 1] = [""] + b + ["", "---"]
        schreib(JO, "\n".join(z))
    print("%s: Kennung %s, %d Zeilen Block" % ("probe" if probe else "eingefuegt", KENNUNG, len(b)))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 3 and a[-2] == "--in":
        stuecke()
        a, wurzel = a[:-2], a[-1]
        if a[0] == "basis" and len(a) == 4:
            a[2] = os.path.abspath(a[2])
        os.chdir(wurzel)
    if len(a) == 2 and a[0] == "kopie":
        sys.exit(kopie(a[1]))
    if len(a) == 2 and a[0] == "kennung":
        sys.exit(kennung(a[1]))
    if a == ["probe"]:
        sys.exit(einbau(True))
    if a == ["einbau"]:
        sys.exit(einbau(False))
    if a == ["vergleich"]:
        sys.exit(vergleich())
    if len(a) == 4 and a[0] == "basis" and a[1] in ("vorher", "nachher", "kopie"):
        sys.exit(basis(a[1], a[2], a[3]))
    if a in (["backlog"], ["backlog", "--probe"]):
        sys.exit(backlog(len(a) == 2))
    if len(a) in (2, 3) and a[0] == "journal" and a[2:] in ([], ["--probe"]):
        sys.exit(journal(a[1], len(a) == 3))
    print("Aufruf: probe | einbau | vergleich | basis vorher|nachher|kopie <beleg> <testdatei> [--in <wurzel>] | kopie <ziel> | backlog [--probe] | kennung <datei> | journal <block> [--probe]")
    sys.exit(2)
```

## Anhang C — Gliederung des Journalblocks

Erste Zeile `## <Kennung> — TB-159: Agent 1, 3 und 4 abgeschaltet über config/agenten_aus.txt`; dann eine Zeile *Quelle: `docs/ERGEBNIS_TB-159_agenten_aus.md`, Commits ⟨S0⟩, ⟨A⟩, ⟨F⟩ = der Commit „TB-159 Abgabe: Ergebnis, Journal <Kennung>“*; `**Quelle:**` (was die Sitzung tat, eigene Worte); `### Was gemessen ist` (0a, 0b, Basislauf, Einbau, Nachlauf mit Zahlen, numstat ⟨S0⟩..⟨A⟩); `### Was offen bleibt` (mindestens: ob die nächste Wochen-Mail ohne KI-Teil kommt); Schlusszeile *Geschrieben <Datum, Uhrzeit> von der Mac-Sitzung TB-159.* Keine Zeile `---`, keine weitere Überschrift `## `.
