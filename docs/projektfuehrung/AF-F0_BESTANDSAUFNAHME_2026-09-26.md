# AF-F0 — Bestandsaufnahme der Codebasis für die Forschungspipeline (Epic AF)

*Steuernder Chat, 26.09.2026, 15:40. Betreiber-Karte 15:30: „AF-F0 jetzt, nur lesend“. Gemessen über die Brücke am Stand `257e7db` (Merge von TB-113), **nur lesend**: `ls`, `grep`, `wc`, `git --no-optional-locks`. Keine Datenbank geöffnet, nichts gerechnet, kein Ergebnis gelesen.*
*Grundlage: `docs/projektfuehrung/BACKLOG_EPICS.md` 2t (AF0–AF6, Gliederung AF-F0 mit AF-T0.1 bis T0.3) und `docs/vorlagen/vorlage_forschungspipeline_2026-09-19.md` Abschnitt 13.*

⭐ **Was AF-F0 ist:** Die Bestandsaufnahme **vor** jeder Feature- und Task-Struktur (AF6). Sie baut nichts und entscheidet nichts. Das Epic bleibt hinter dem signierten Tag geparkt (AF0).

---

## AF-T0.1 — Codebasis gegen Abschnitt 13 der Vorlage

| Vorlage §13 | Vorhanden? | Was es heute ist (gemessen) | Wiederverwendbar für AF |
|---|---|---|---|
| **Python-Infrastruktur** | ja | `trading-env` (Python 3.9.6), `requirements.txt` 65 Zeilen, **`requirements.lock`** 83 Zeilen, aus `pip freeze` erzeugt, gegengeprüft; der Selektionslauf rechnet genau damit | ja, der Lock ist das Vorbild für „Code Version“ |
| **Backtesting** | ja, **je Bot eigen** | 9 × `equity_simulation.py`, 9 × `multi_symbol_optimise.py`, dazu `backtest_*.py`/`multi_symbol_walk_forward.py`; Selektion über `research/vorregistrierung/` (`faltenplan.py`, `benchmark.py`, `auswertung.py`, `kennzahlen.py`) | teilweise: die Selektionskette ist allgemein, die Bot-Simulationen nicht |
| **Marktdaten** | ja | `shared/kursdaten.py`, `fetch_binance_data.py`, `fetch_multi_data.py`, `binance_historie.py` (Binance Public Data), yfinance; `data/` mit Abruf-Cron; **Snapshot** `snapshots/63e4b6c8…` (Datenstand `d9449faf…`) | ja, Snapshot = „Data Version“ |
| **Strategie-Schnittstelle** | **nein, keine gemeinsame** | Jeder Bot ist ein Ordner mit demselben Dateisatz (`forward_test.py`, `live_params.py`, `indicators.py`, `equity_simulation.py` …); gemeinsam sind nur Hilfsmodule in `shared/` (Resolver `paths.py`, `strategy_paths.py`, `entscheidungskerze.py`, `zuteilung.py`) | ⚠️ **Die grösste Lücke:** AF-F2 („deterministisch reproduzierbare Spezifikation“) braucht eine Schnittstelle, die es heute nicht gibt |
| **Bot-Laufzeit** | ja | 9 × `forward_test.py` (Paper-Betrieb), per Cron; Regimewache 11.1 an drei Stellen | ja |
| **Datenbank** | ja, **SQLite je Bot** | 9 × `paper_trading_<bot>.db` im Wurzelordner, dazu `broker_testnet_t3_supertrend.db` und `benachrichtigungen_schliessung.db`; 39 Module benutzen `sqlite3`; seit heute täglich gesichert (TB-112) | ja für Paper; für eine Registry mit vielen parallelen Zyklen eher nicht (Schreibsperren) |
| **Docker** | **nein** | keine `Dockerfile`, kein Compose | — |
| **Queue / Job-System** | **nein** | kein Redis, keine Celery. `apscheduler` steht im Lock; genutzt wird es nur in `notifications/telegram_bot.py` | — |
| **Scheduler** | ja | `crontab` (Datenabruf, Wächter 3:50/4:10/4:40, Brücke alle 4 h, db-Sicherung 05:20) und `launchd` (`system/*.plist`: Dashboard, Telegram-Bot, caffeinate; Sitzungswächter) | ja, für wenige Zyklen; für viele parallele Experimente nicht |
| **API-Schicht** | ja, klein | `dashboard/app.py` mit **FastAPI**/uvicorn (über Tailscale) | ja, als Anzeige |
| **Logging** | ja, uneinheitlich | `logs/` (gitignoriert), Log-Rotation (`system/README_LOG_ROTATION.md`); `logging`-Modul nur in 10 Modulen, sonst `print` bzw. eigene Protokolle | teilweise |
| **Monitoring** | ja | `notifications/` (Telegram-Bot, `monitor.py`, `waechter_melden.py`), tägliche und wöchentliche E-Mails, Sitzungswächter | ja |
| **Experiment-Tracking** | ja, **auf Papier** | Versuchsregister (`research/versuchsregister/`, N = 653), Vorregistrierungs-Register (44 Abschnitte), `docs/belege/TB-*`, Ergebnisdokumente, `herkunft.py` mit Kettenhash (Protokoll noch nicht angelegt) | ⭐ ja, dem Verfahren nach das Stärkste im Projekt; maschinenlesbar ist nur das Versuchsregister |
| **Strategie-/Modell-Versionierung** | ja | git (GitHub, `Manisch2886/trading-bot`), Register-Hash `register()`, Sperrlisten-Abbild, Codeherkunft (Register 19, seit TB-112 über den ganzen Laufbereich) | ja, das ist AF4 |
| **Paper Trading** | ja | 9 Bots im Paper-Betrieb; IBKR-Paper (`broker/ibkr_paper.py`, `ibkr_spiegel.py`), Binance-Testnet (`broker/binance_testnet.py`) | ja, das ist AF-F8 |
| **Börsen-Anbindungen** | ja, zum Teil | `python-binance` (⚠️ Binance ist seit 1.7.2026 für EU-Kunden keine Ausführungsstelle, Fable 25f), IBKR über `broker/` | teilweise, Venue-Frage offen (25f K1) |
| **CI/CD** | **nein** | kein `.github/workflows`; Tests laufen in den Mac-Sitzungen von Hand | — |
| **Tests** | ja, viele | **86** Testdateien (`test_*.py`) ausserhalb von `trading-env`, mit Mutationsproben; `test_vorregistrierung` 196 Proben | ja |
| *KI-Agenten (aus §14)* | ja, klein | `anthropic` im Lock; `shared/claude_client.py`, `param_search_agent.py`, `market_context_agent.py`, `portfolio_interpreter_agent.py`, Tages-/Quartals-Interpreter | ja, als Muster für den Research-Agenten (AF-F7) |

**Kurz:** Das Projekt hat bereits, was die Vorlage „Registry, Data Version, Code Version, Experiment-IDs, Adversarial Review“ nennt, und zwar strenger als die Vorlage verlangt. Es fehlen die **Industrialisierung** (Strategie-Schnittstelle, Job-System, CI) und ein **maschinenlesbarer Versuchszähler** über alle Zyklen (AF-F1).

## AF-T0.2 — Überschneidungen mit Register, Snapshot und Lock

| Vorlage fordert | Im Projekt schon da | Lücke |
|---|---|---|
| Strategy Registry (Code, Daten, Parameter) | Register + Snapshot `63e4b6c8…` + Lock + Codeherkunft (19) | eine **Tabelle** je Strategie mit Status; heute steht das verteilt in Register, Backlog und Ergebnissen |
| Reproduzierbare Datenstände | Snapshot mit Manifest, `datenstand_hash` | nur **ein** eingefrorener Stand; ein Zyklus braucht je Zyklus einen |
| Experiment-IDs | TB-Nummern, `docs/belege/TB-*` | TB-Nummern sind Aufträge, nicht Experimente; ein Experiment kann mehrere Aufträge brauchen |
| Adversarial Review | Fable als Verfahrensprüfer (Sichtschutz 27) | Fable prüft Verfahren, nicht Kandidaten; das ist Epic RT |
| Mehrfachtest-Korrektur | DSR mit N-Buchführung (Register 9), N = 653 | Zähler über **Zyklen** hinweg und über verworfene Varianten (AF2; 25f V2 „Trials-Log“) |
| Vorab festgelegte Schwellen | das Register selbst (Festlegungen, Abbruchkriterien) | je Zyklus ein **eigener** Zeitanker (AF3/AF5; 25f V1 „Baukasten“) |
| Kein Kapital ohne Mensch | Stufe „Bestätigt“ + zwei Quartale vor Echtgeld (16.4 (f)) | — |

⭐ **Folgerung:** AF ist kein Neubau, sondern die Verallgemeinerung dessen, was das Register für **einen** Durchgang tut, auf **viele**. Fables 25f-Ideen V1 (Baukasten), V2 (Trials-Log) und V4 (Sonden-Bibliothek) sind genau die ersten drei Bausteine dafür.

## AF-T0.3 — Offene Architekturfragen (für Fable, nach dem Tag zu entscheiden)

1. **Strategie-Schnittstelle (AF-F2):** Soll die Pipeline die neun Bots auf eine gemeinsame Schnittstelle heben, oder erzeugt sie neue Strategien in einer neuen Schnittstelle und lässt die neun, wie sie sind? *Neigung:* neu, damit die neun registrierten Bots unberührt bleiben.
2. **Versuchszähler (AF-F1):** Wird das Versuchsregister (TB-29) zum maschinenlesbaren Trials-Log erweitert (25f V2), oder entsteht ein neuer Zähler? Und zählt ein Zyklus mit N = 1 schon in das N der DSR des nächsten Durchgangs?
3. **Zeitanker je Zyklus (AF3/AF5):** Genügt je Zyklus ein Registerabschnitt nach dem Baukasten (25f V1) mit Commit-Hash, oder braucht jeder Zyklus einen eigenen signierten Tag?
4. **Speicher:** SQLite je Zyklus, oder eine gemeinsame Datenbank für die Registry? Das ist erst bei vielen parallelen Zyklen eine Frage (Vorlage §16).
5. **CI:** Sollen die Mutations- und Registerproben künftig bei jedem Push laufen (GitHub Actions)? Das wäre der erste Baustein, der heute schon ohne Laufberührung ginge.

---

## In einfacher Sprache

Das Epic „Forschungspipeline“ soll später neue Strategien automatisch prüfen. Bevor man dafür etwas baut, wurde nachgesehen, was schon da ist, und zwar mehr, als die Vorlage erwartet: Versionierung, eingefrorene Daten, Tests und ein strenges Regelwerk. Es fehlen vor allem eine gemeinsame Schnittstelle für Strategien, ein automatischer Zähler aller Versuche und eine automatische Testausführung. Fünf Architekturfragen gehen an Fable; entschieden wird erst nach dem Tag.
