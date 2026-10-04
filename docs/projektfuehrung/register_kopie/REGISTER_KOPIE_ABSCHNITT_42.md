# REGISTER-KOPIE Abschnitt 42 (von 0–53) — Register-Z. 8966–9531 — Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff — KOPIE, nicht das Register

## 42. Zugriffsklassen, Laufbereich, die vier Rückfälle und ihr Schluss — die Einträge aus Fable 25a, 25b, 25c und die Tatsachennotizen TB-103 bis TB-107 (TB-108, 25.09.2026)

Bauart, Herkunft der Quellen und Gliederung wie **41.0**. Hier stehen die
Einträge aus **25a, 25b und 25c** (42.1–42.3), die Tatsachennotizen aus den
Aufträgen TB-103 bis TB-107 (42.4), die Hash-Übergänge seit 39.5 (42.5), was
offen bleibt (42.6) und was hier nicht getan wurde (42.7). ⛔ **Nichts aus 25d,
25e, 25f** — die Antworten stehen aus; sie kommen in Abschnitt 43.

### 42.1 Aus Fable 25a (`FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md`)

Fables Liste für dieses Register, 25a Abschnitt 5, zeichengleich (Nachsatz zur
Tabelle):

> **Für Register 41/42 kommen hinzu** (zu 24c Abschnitt 6 und 24d Abschnitt 4): die drei Klassen (3 (A)), die vier Teile der Symbolbedingung (3 (B)), der Laufbereich (4), die Präzisierung zu 33.3/35.4 (1 (1)), die Tatsachennotiz zu TB-103 (Resolver mit MANIFEST als Ort; Trockenlauf mit Umgebungsliste; Ladeprotokoll-Teil (4) offen), die Tatsachennotiz zum Lesehaken (TB-92, `a1b_lesehaken.py`; eure Berichtigung), die Schreibziel-Notiz zu `manuelle_eingriffe.log`, die Einordnung der vier Rückfälle mit dem Verweis auf 11.1.

**D1 — Berichtigung zu 24c Abschnitt 2: die Fundstelle der Resolver-Pflicht** ·
Art: Berichtigung einer Fundstelle · Quelle: 25a Abschnitt 3 (C) · berichtigt
41.2 (B5)

> Angenommen: *„über den Resolver (`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`)"*. Meine Fundstelle `shared/paths.py::get_strategy_paths()` war falsch — eine Funktion in der falschen Datei genannt, nicht gemessen. **Achter Fall**, dieselbe Klasse. Berichtigung zu 24c Abschnitt 2 mit eurem Wortlaut.

⇒ **Die Resolver-Pflicht (41.2, B5) gilt mit dieser Fundstelle:** „über den
Resolver (`shared/paths.py`, direkt oder über
`strategy_paths.get_strategy_paths()`)".

**D6 — die drei Klassen von Zugriffen** · Art: Registertext (Präzisierung zu
24c (b) und zur Tag-Vorbedingung 24b A2) · Quelle: 25a Abschnitt 3 (A)

> **Präzisierung zu 24c (b) und zur Tag-Vorbedingung 24b A2 — drei Klassen von Zugriffen:** Jeder Datei-Zugriff eines Modus-Laufs fällt in genau eine von drei Klassen. **(i) Eingaben** — Kurs-, Universums-, Ergebnis- und Eingabedateien: zulässig nur innerhalb `snapshots/<hash>/` oder als registrierte Eingabedatei; jeder andere ist Befund 1 des Nachweisteils (b). **(ii) Umgebung** — `requirements.lock`, Interpreter- und Plattformdateien, Zufallsquelle, Zeitzonendaten, vom Import der registrierten Pakete geöffnet: zulässig; die Liste dieser Zugriffe je Lauf-Typ steht **mit Aufrufstapel als Tatsachennotiz**, und ein Umgebungszugriff, der in dieser Liste nicht steht, ist ein Befund 1 — nicht weil er die Rechnung berührt, sondern weil niemand weiss, ob er es tut. **(iii) Schreibzugriffe** — ein Modus-Lauf öffnet zum Schreiben nur sein `--ziel` und Belegpfade; jedes andere Schreibziel ist Befund 1 der Schreibziele-Sonde, auch ohne geschriebene Bytes. „0 Zugriffe ausserhalb `snapshots/<hash>/`" in 24b A2 lies „0 Zugriffe der Klasse (i) ausserhalb; Klasse (ii) nach Liste; Klasse (iii) leer".

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5f — die Umgebung ist registriert (Lock mit Hash, Abschnitt 20), und `requirements.lock` ist die Datei, mit der der Modus die Umgebung **prüft**; ein Nachweis, der die Prüfung als Verstoss zählt, widerspricht sich. Warum die Liste trotzdem geführt wird: `/dev/urandom` beim pandas-Import ist harmlos, solange die Neurechnung bytegleich ist — und genau das ist Nachweisteil (a); ein Lauf, der plötzlich eine sechste Umgebungsdatei öffnet, hat ein Paket oder einen Importpfad gewechselt, und das sieht man sonst nirgends. Kein Ergebnis.

⭐ **ERGÄNZT durch 42.2 (E1: Klasse (iv) Zwischenablage; E2: Klasse „Code") und
42.3 (F7: Interpreter-Caches unter (ii); F8: registrierte Protokolle in (iii)).**

**D2 — „0 Zugriffe ausserhalb" lies nach den drei Klassen** · Art: Präzisierung
des eigenen Wortlauts (an 24b A2, 41.1 A11) · Quelle: der letzte Satz von D6
oben. ⭐ **ERGÄNZT durch 42.2 (E1) und 42.3 (F8)** — Klasse (iii) heisst seitdem
„kein Schreibzugriff ausser `--ziel`, Belegpfaden, Klasse (iv) und registrierten
Protokollen".

**D3/D7 — die Liste ist gleich, die Menge ist registriert: die vier Teile der
Symbolbedingung** · Art: Präzisierung des eigenen Wortlauts (an 24b A2) und
Registertext · Quelle: 25a Abschnitt 3 (B). Die Stoffsammlung führt denselben
Text zweimal (D3 als Präzisierung, D7 als Registertext); er steht hier einmal.

> **Präzisierung zu 24b A2 („geladene Symbolmenge gleich Universumsdatei"):** (1) Die **Liste**, die der Bot erhält, ist gleich der Universumsdatei des Snapshots nach `EXCLUDE_SYMBOLS` (16.1.3: 24 von 25; 150). (2) Die **geladene Menge** ist gleich der in 16.1.1 für die Bestätigungsperiode registrierten Zahl je Bot *[Voraussetzung, zu messen: dass der Trockenlauf den Loader am Datenende aufruft, wie die Bestätigungsspalte von 16.1.1 gemessen wurde]*. (3) Jede Differenz zwischen (1) und (2) steht im Ladeprotokoll je Symbol mit Grund. (4) Das Ladeprotokoll nennt die Länge der Liste, die Zeilenzahl der Universumsdatei und die **Quelle** der Liste (Pfad). Gleichheit mit und ohne Modus ist Tatsachennotiz, keine Bedingung.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 3b (b) — welche Symbole geladen werden, entscheidet die registrierte `MIN_HISTORY_*`-Tabelle, und ihr Ergebnis ist in 16.1.1 gemessen und eingetragen; eine Vorbedingung prüft gegen das Register, nicht gegen einen zweiten Lauf. Kein Ergebnis. **Zu (4):** Das Ladeprotokoll nennt heute weder die Zeilenzahl der Datei noch die Quelle — ihr habt es gemessen. Bis das nachgezogen ist (Handwerk mit Freigabe, `shared/ladeprotokoll.py`), ist die Vorbedingung in Teil (4) **nicht** erfüllt; das steht so in der Tatsachennotiz zu TB-103, nicht als Mangel des Laufs, sondern als das, was noch fehlt.

⭐ **PRÄZISIERT durch 42.2 (E6):** Die geladene Menge wird am Stichtag
Go-Live-Schnitt (5.2), ausschliesslich, ermittelt.

**Stand, gemessen:** Teil (4) ist **weiter nicht erfüllt** —
`shared/ladeprotokoll.py` unverändert seit `55b991d` (TB-45); der Meldetext
„Keines ausgelassen." steht dort unverändert (Z. 161).

**D4 — Wiederholung am Tag-Commit** · Art: Ergänzung zur Tag-Vorbedingung (24b
A2, 41.1 A11) · Quelle: 25a Abschnitt 2

> **Ergänzung zur Tag-Vorbedingung (24b A2):** Der Trockenlauf aller neun Bots im Modus wird **am Tag-Commit** wiederholt — wie das letzte Abbild (37.3) trägt sein Protokoll die Hashes des Standes, den der Tag signiert. Ein Trockenlauf an einem früheren Stand ist eine Tatsachennotiz, keine Tag-Vorbedingung.

*Seine Quelle des Grundes, zeichengleich:* „37.3 (das letzte Abbild passt zum Tag-Commit); zwischen `836865f` und dem Tag ändern sich `paths.py`-nahe Module noch (Plan-Punkt 2, die Rückfälle aus Abschnitt 4). Kein Ergebnis."

**D5 — Präzisierung zu 33.3/35.4 (Plan ohne Verfahren-A-Felder)** · Art:
Präzisierung, Ersteintrag — ⭐⭐ **BERICHTIGT durch 42.2 (E3)**: Der Plan
schrumpft nicht; die Sonde vergleicht über eine registrierte Abbildung · Quelle:
25a Abschnitt 1 (1) · entscheidet 41.3 (C5)

> **Präzisierung zu 33.3/35.4 (Ersteintrag):** Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die 33.2/33.3 nicht kennt. Die Faltenplan-Sonde vergleicht den ganzen gerechneten Plan gegen das Abbild, nicht eine Auswahl seiner Felder. Verfahren-A-Felder (`purge_tage`, `embargo_tage`, `training_bis_ausschliesslich`) werden vor dem Tag aus `faltenplan.py` entfernt — Berichtigung des Codes an 2c/4a, planmässig nach 37.3 (Sperrlistenpunkt 2, Freigabe, alter und neuer Hash, neues Abbild). `G8` wird nicht gelöscht, sondern angepasst (23a): es prüft künftig, dass der gerechnete Plan je Falte keine Felder ausserhalb der Feldliste trägt — dieselbe Stelle, die registrierte Erwartung.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 33.1 (Fables Satz: „Sechzig verschiedene Trainingsgrenzen in einer Datei beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht man der Datei nicht an") — er gilt für den gerechneten Plan wie für die Datei. Kein Ergebnis. Wann das geschieht (mit dem Abbild-Auftrag oder davor), ist Handwerk; **vor** der Sonde muss es sein, sonst ist ihr erster Lauf rot aus einem Grund, der keiner ist.

⚠️ **Welcher Teil weiter gilt:** Die Entfernung der drei Verfahren-A-Felder aus
dem gerechneten Plan und die Anpassung von `G8` sind vollzogen (TB-104,
`f334a7b`; 42.5). Der erste Satz („trägt keine Grösse, die 33.2/33.3 nicht
kennt") ist durch E3 ersetzt — er hätte die Herleitungsfelder mitgetroffen.
Marken bei 33.3 und 35.4.

**D8 — der Laufbereich** · Art: Registertext, Ersteintrag — ⭐⭐ **BERICHTIGT
durch 42.2 (E5)**: Vereinigung aller registrierten Lauf-Typen, gemessen am
Tag-Commit · Quelle: 25a Abschnitt 4

> **Registertext, Ersteintrag — Laufbereich:** Der Laufbereich ist die Menge der Module, die ein Modus-Lauf lädt oder ausführt (Trockenlauf aller neun Bots, Erzeuger, `benchmark.py`, `faltenplan.py`, `auswertung.py` und ihre Kindprozesse), gemessen am Aufrufstapel des Lese-Audits. Die Regeln „kein Fallback unter dem Modus" (24b A2), die Resolver-Pflicht (24c) und die drei Ausgänge (36.5) gelten für genau diese Menge; die Sonde „Lesequellen" führt sie. Ein Rückfall in einem Modul ausserhalb des Laufbereichs ist eine Tatsachennotiz, kein Befund — bis das Modul geladen wird.

*Seine Quelle des Grundes, zeichengleich:* „5e (der Lauf belegt, woraus er gelesen hat — und damit, was er ist) und A8 (eine Regel braucht eine Menge, auf der jemand sie prüfen kann). Kein Ergebnis."

⭐ **Dieser Eintrag bestimmt die Menge, für die die drei Ausgänge aus 36.5
gelten** — Marke bei 36.5.

**D9 — Tatsachennotiz zu TB-103** · Art: Tatsachennotiz (mit Bedingung) ·
Quelle: 25a Abschnitt 2

> **Resolver:** `CONFIG_DIR = <snapshot>/config`, Prüfung beim Import gegen das, was **das MANIFEST** unter `config/` nennt, `SystemExit(2)` bei fehlend/leer/nicht genannt, Dateinamen nicht in `paths.py`, ohne Modus 99 Pfade 0 Unterschiede, vier Mutationsproben, jede beisst allein, 35/35 und 191/191. Das ist die Bauart aus 24b A2, und der Punkt, dass das MANIFEST der eine Ort ist, der die Anordnung kennt, ist besser als das, was ich vorgeschlagen hatte („Kurse flach, Universum unter `config/`" stand bei mir als Beschreibung, nicht als Quelle). Die fünf Symboldateien mit dem eingebauten Rückfall sind unverändert; ihr Rückfall ist unter dem Modus unerreichbar — solange `paths.py` so bleibt. Das ist eine Tatsachennotiz mit Bedingung, und sie gehört so ins Register.

Und zum Ladeprotokoll, 25a Abschnitt 3 (B), zeichengleich: „Bis das nachgezogen ist (Handwerk mit Freigabe, `shared/ladeprotokoll.py`), ist die Vorbedingung in Teil (4) **nicht** erfüllt; das steht so in der Tatsachennotiz zu TB-103, nicht als Mangel des Laufs, sondern als das, was noch fehlt."

**Tatsachennotiz (gemessen, TB-103, `docs/ERGEBNIS_TB-103_resolver_und_trockenlauf.md`):**
Resolver `shared/paths.py` (`d87997e`): unter dem Modus `CONFIG_DIR =
<snapshot>/config` (`CONFIG_UNTERORDNER`, Z. 213), Prüfung beim Import gegen
das MANIFEST, `SystemExit(2)` bei fehlender, leerer oder nicht genannter
Universumsdatei; ohne Modus 99 Pfade, 0 Unterschiede. Trockenlauf aller neun
(`836865f`): 9 × rc 0, Liste = Universumsdatei 9/9, 0 Kurs- oder
Universumszugriffe ausserhalb des Snapshots, 0-mal Standardliste; je Bot fünf
Umgebungszugriffe (`requirements.lock` und vier Systemdateien) — die
Umgebungsliste nach D6 (ii). ⚠️ **Die Bedingung:** Der eingebaute Rückfall der
Symbollisten ist unter dem Modus unerreichbar, **solange `paths.py` so bleibt**;
seit TB-105 (`f65c344`) endet zudem `symbols_config.py` unter dem Modus bei
leerer Liste mit 2 (Rückfall (a), D12). Ladeprotokoll-Teil (4) **offen** (D3/D7).

**D10 — Tatsachennotiz: der Lesehaken ist von TB-92** · Art: Tatsachennotiz
(Berichtigung des steuernden Chats) · Quelle: 25a Abschnitt 1 (3) — Wortlaut und
Messung in **41.3 (C9)**. Werkzeug: `docs/belege/TB-92/a1b_lesehaken.py`.

**D11 — Schreibziel `manuelle_eingriffe.log`** · Art: Tatsachennotiz · Quelle:
25a Abschnitt 1 (3), derselbe Absatz wie D10

„der Modus-Lauf öffnet `logs/notifications/manuelle_eingriffe.log` **im Modus `a`** — zum Anhängen, aus dem Repo, über einen Import aus `notifications/`." — „Ein Import, der beim Laden eine Datei zum Schreiben öffnet, ist eine Nebenwirkung, die im Laufbereich nichts zu suchen hat."

**Stand, gemessen:** **behoben in TB-105** (`d48a195`):
`notifications/manual_close.py` legt Ordner und Protokoll erst bei der ersten
Zeile an; der Weg im Modus war `registerdaten.py:62` → `manual_close.py` (TB-104
C5). Benchmark im Modus seither ohne diesen Zugriff (TB-105 F2). Marke bei 39.8.

**D12 — die vier Rückfälle, mit Verweis auf 11.1** · Art: Registertext
(Einordnung und Rangfolge) · Quelle: 25a Abschnitt 4

> **Die vier weiteren Rückfälle — alle vier vor den Tag, in dieser Rangfolge, jeder mit Gegenprobe (Rückfall erreichbar gemacht ⇒ Rückgabe 2):**
>
> | | Rückfall | Warum vor den Tag |
> |---|---|---|
> | **1** | **(b)** `t3_supertrend`: BTC-Regimefilter fällt still weg, wenn BTCUSDT nicht geladen ist | ⚠️ **Schon registriert als Voraussetzung des Laufs** — 11.1 (`shared/regimewache.py`, `pruefe_einbau()`, „Solange er es nicht ist, darf der Lauf nicht starten") und Schlusssatz von Abschnitt 10. Kein neuer Beschluss nötig; euer Fund ist die Messung, dass 11.1 offen ist. Dass BTCUSDT im Trockenlauf geladen war, ändert nichts: 11.1 begründet den Abbruch mit Determinismus, nicht mit dem heutigen Bestand |
> | **2** | **(c)** Backtest-Skripte enden bei „Keine Daten gefunden" mit `exit()`, rc 0 | Das ist TB-45 in Reinform — 0 ohne Messung —, und 36.5 gilt für jede Wache und jeden Lauf: „Kein Aufruf endet mit 0, ohne dass gemessen wurde." Unter dem Modus: 2 |
> | **3** | **(d)** Stille Ersatzwerte für Schwellen in `faltenplan.py`, `benchmark.py`, `auswertung.py` | Ein Ersatzwert für eine registrierte Schwelle ist ein Fallback für einen Parameter (24b A2 nennt Schwellen ausdrücklich) — und er ist schlimmer als ein Schalter, den 12 für `auswertung.py` ausschliesst: Ein Schalter ist sichtbar, ein `.get(…, default)` nicht. Vorab je Stelle Tatsachennotiz, ob die registrierte Eingabe den Schlüssel je auslässt; unabhängig davon Ersatz durch Abbruch 2. `auswertung.py` ist Sperrlistenpunkt 3/5/14 — planmässig nach 37.3, wie TB-92 |
> | **4** | **(a)** Krypto-Liste nach `EXCLUDE_SYMBOLS` leer ⇒ Standardliste | Auf dem registrierten Snapshot unerreichbar — aber die Regel gilt für den Modus, nicht für diesen Snapshot; ein Rückfall, den erst der nächste Snapshot erreicht, ist genau „gleich welcher Art". Kleinster Aufwand (eine Prüfung „leer ⇒ 2" in `symbols_config.py`, Live-Code, eigene Freigabe); kleinster Rang, aber nicht als Notiz abgetan |

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 24b A2 im Wortlaut, 36.5, 11.1. Kein Ergebnis: Keiner der vier verändert, was der Lauf rechnet, wenn alles da ist; sie verändern, was er tut, wenn etwas fehlt — und das ist das Einzige, was der Modus regelt.

**Stand, gemessen — alle vier geschlossen:** (b) TB-105 (`f524327`,
`regimewache.pruefe_einbau()` heute `vollstaendig: True`, 3 von 3 eingebaut;
G1) · (c) TB-105 (`f65c344`, 14 Stellen, unter dem Modus 2; G2) · (a) TB-105
(`f65c344`, `symbols_config.py`) · (d) in den eingefrorenen Dateien TB-106
(`abeca36`, `a08c13a`, `5cc1de4`), in den nicht gesperrten Hilfsprogrammen
TB-107 (`33d50f2`, `f5fdb53`, `5cfe472`, `a79e715`). ⚠️ `f5fdb53` ist **vor**
Fables Antwort auf 25d gebaut und als eigener Commit revertierbar (42.6).
Marke bei 11.

### 42.2 Aus Fable 25b (`FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md`)

Fables Liste für dieses Register, 25b Abschnitt 4, Kopf, zeichengleich:

> ## 4. Was auf Register 41/42 kommt, zusätzlich zu 24c/24d/25a

**E1 (a) — Klasse (iv), Zwischenablage; die Messumgebung für (iii) und (iv)** ·
Art: Registertext (Ergänzung zu 25a (A)) · Quelle: 25b Abschnitt 3 (1) ·
ergänzt 42.1 (D6)

> **Ergänzung zu 25a (A) — Klasse (iv), Zwischenablage:** Eine Datei, die derselbe Lauf schreibt **und** liest, ist Zwischenablage. Sie ist zulässig, wenn (1) ihr Ordner je Lauf neu und eindeutig angelegt wird (`mkdtemp`) **oder** unter `--ziel` liegt, (2) kein Prozess ausserhalb des Laufs sie liest — im Audit erscheint jeder Lesezugriff auf sie mit dem Schreibzugriff desselben Laufs daneben — und (3) sie am Ende des Laufs entfernt ist **oder** ihr Pfad im Beleg steht. Fehlt eine der drei, ist sie Befund 1 der Schreibziele-Sonde. Klasse (iii) („Schreibziele leer") heisst damit: kein Schreibzugriff ausser `--ziel`, Belegpfaden und Klasse (iv). Gemessen wird (iii) und (iv) in einer Umgebung, in der die Ziele fehlen (Abschnitt 1).

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5e — der Audit soll zeigen, woraus der Lauf gelesen hat; eine Zwischenablage, die er selbst geschrieben hat, ist keine Eingabe, und der Audit muss das **sehen**, nicht wissen. Warum (1): Ein deterministischer Pfad in `$TMPDIR` könnte vom nächsten Lauf gelesen werden — dann wäre eine Zwischenablage eine unregistrierte Eingabe; `mkdtemp` schliesst das aus. Warum (3): Elf Ordner je Lauf, die niemand entfernt, sind kein Verfahrensfehler, aber ein Bestand, den niemand kennt — und „nie entfernt" heisst heute: **Befund 1**, bis das Aufräumen eingebaut ist (Handwerk, klein). Kein Ergebnis.

**Stand, gemessen:** `tb40_lauf_*` erfüllt Bedingung (3) seit TB-107 (`a79e715`:
entfernt nach dem Lesen, ohne Ergebnis bleibt der Ordner und sein Pfad steht in
der Meldung). `tb40_faltenplan_*` und `tb40_proben_*` sind offen — Frage 25e (1),
42.6.

> ⭐ **Reichweite: siehe 45.2** (Fable 26a R2, TB-114, 26.09.2026). Eintrag
> und Stand oben bleiben zeichengleich.

**E2 (b) — Klasse „Code"; Ergänzung zu 19: Sauberkeit über den Laufbereich** ·
Art: Registertext · Quelle: 25b Abschnitt 3 (2) · ergänzt 42.1 (D6)

> **Ergänzung zu 25a (A) — Klasse „Code":** Ein Lesezugriff auf eine Datei unter der Codewurzel ist Klasse „Code" und zulässig, wenn die Datei in einem Pfad liegt, den die Startprüfung (19) über `HEAD` und sauberen Arbeitsbaum bindet. Eine Datei unter der Codewurzel **ausserhalb** dieser Pfade ist weder Code noch Eingabe — sie ist ungebunden und ein Befund 1. Ein Leser, der Werte per Muster aus Quelltext liest, endet mit 2, wenn das Muster nicht genau einmal trifft; ein Ersatzwert ist ausgeschlossen.

> **Und der Befund, den diese Frage erst sichtbar macht:** 19 nennt als `ARBEITSBAUM_PFADE` **`shared/`, `strategies/` und `requirements.lock`** — nicht `research/`, nicht `notifications/`. Der gemessene Laufbereich hat 11 Module aus `research/` und eines aus `notifications/`. Ein veränderter, uncommitteter `benchmark.py` oder `faltenplan.py` würde die Startprüfung heute **nicht** aufhalten. *[Voraussetzung, zu messen: dass 19 den Stand noch beschreibt — die Tatsachennotiz dort ist vom 19.09.]*

> **Ergänzung zu 19 (Registertext 5e, Codeherkunft):** Die Sauberkeitsprüfung des Arbeitsbaums erstreckt sich auf **jeden Pfad des Laufbereichs** (Abschnitt 5 unten), nicht nur auf `shared/`, `strategies/` und `requirements.lock`; `data/` bleibt ausgenommen (19, aus dem dort genannten Grund). Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 19 selbst — „Liegen Aufrufer und Resolver in verschiedenen Bäumen, beschreibt kein einzelner Commit den gelaufenen Code"; das gilt für jedes Modul, das läuft. Kein Ergebnis. Zu den neun Optimierern selbst: sie liegen unter `strategies/`, sind also heute schon gebunden — eure Lesart „Code" gilt für sie ohne Vorbehalt. *[Messbitte, nur das Ob: endet `_min_history` mit 2, wenn das Muster in einer Datei nicht genau einmal trifft?]*

**Stand, gemessen:** `shared/paths.py` Z. 225 `ARBEITSBAUM_PFADE = ("shared",
"strategies", LOCK)` — unverändert; die Tatsachennotiz in 19 beschreibt den Stand
(bestätigt in 25c 2 (d)). ⚠️ **Die Erweiterung ist nicht vollzogen**; sie ist
**Tag-Vorbedingung** (25c 2 (d)) und braucht **vorher** die Ausnahme für
registrierte Protokolle (42.3, F8) — die steht mit diesem Eintrag im Register.
Marke bei 19.

> ⭐ **Vollzogen, siehe 44.2 (44-7; TB-112 `9d711dc`, TB-113, 26.09.2026):**
> `ARBEITSBAUM_PFADE` hat 15 Einträge (die 12 Module des Laufbereichs
> ausserhalb `shared/`/`strategies/` als Einzeldateien); die Liste steht als
> Tatsachennotiz neben der Laufbereichsmessung (44-8). Eintrag und Stand oben
> bleiben zeichengleich.

> ⭐ **Pflege von `ARBEITSBAUM_PFADE`: siehe 45.4** (Fable 26a R4, TB-114,
> 26.09.2026). Eintrag, Stand und die Marke oben bleiben zeichengleich.

**E3 (c) — Berichtigung zu 25a (1): der Plan schrumpft nicht; registrierte
Abbildung; die Feldliste des Plans ist Registertext** · Art: Berichtigung und
Registertext · Quelle: 25b Abschnitt 3 (3) · berichtigt 42.1 (D5)

> **Berichtigung zu 25a (1), Präzisierung zu 33.3/35.4:** „Der Plan … trägt keine Grösse, die 33.2/33.3 nicht kennt" lies: **„Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die das Verfahren nicht kennt** (Trainingsgrenzen, Embargo, Purge, Mindesttraining). Die Faltenplan-Sonde vergleicht den Plan mit dem Abbild über eine **registrierte Abbildung**: je Feld des Abbilds (33.3) der Planschlüssel, aus dem es gebildet wird. Die **Feldliste des gerechneten Plans** — jeder Schlüssel je Plan und je Falte, mit der Registerstelle, die ihn begründet — ist Registertext; ein Schlüssel im Plan, der dort nicht steht, ist ein Befund der Sonde, ein fehlender ebenso."

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 33.3 (ein Abbild trägt genau die Grössen seines Abschnitts — das Abbild, nicht der Plan), 25.3/32.1 (der Plan trägt seine Herleitung), 33.1 (Felder, die ein anderes Verfahren beschreiben, dürfen nicht drin sein). Kein Ergebnis. **Zu `G8` heute:** Die Feldliste „aus dem Code" ist eine Kopie des Codes im Test — als benannter Zwischenstand zulässig, wie ihr es benannt habt; sie wandert mit Register 41/42 in den Registertext. Wie der Test dann an den Registertext gebunden wird (Parser wie `G6`, oder Literal mit Test gegen das Register wie in 32.5 (c)), ist die offene Frage aus 32.5 und Handwerk; ich entscheide sie nicht mit.

**Tatsachennotiz — die Feldliste, wie sie heute im Test steht (gemessen,
`test_vorregistrierung.py` `db50e187…`, Z. 105–113; Schlüsselnamen, keine
Werte):** je Plan `bestaetigungsperiode`, `erste_falte`, `erste_falte_4a`,
`erste_falte_4a_warm_ab`, `erste_falte_quelle`, `erste_falte_trockenlauf_H`,
`falten`, `faltenlaenge_begruendung`, `faltenlaenge_jahre`, `go_live_schnitt`,
`horizontbeginn`, `markt`, `selektionsfalten`, `status`, `trades_je_jahr`; je
Falte `angeschnitten`, `bis_ausschliesslich`, `name`, `rolle`, `von`.
⚠️⚠️ **Das ist noch nicht die Feldliste als Registertext:** 25b verlangt je
Schlüssel **die Registerstelle, die ihn begründet**, und die ist nicht
zugeordnet — das ist keine Abschrift, sondern eine Entscheidung je Schlüssel.
**Offen (42.6)**; bis dahin ist die Liste im Test der benannte Zwischenstand, den
25b zulässt. Ebenso offen: die registrierte Abbildung (je Feld des Abbilds der
Planschlüssel) und wie der Test an den Registertext gebunden wird (32.5, bei
Fable ausdrücklich nicht entschieden). Marken bei 33.3 und 35.4.

**E4 (d) — `mindesttraining_jahre`, `embargo_nach_falten`, die Berichtszeile** ·
Art: Berichtigung (Code an 15.1/2c) · Quelle: 25b Abschnitt 3 (4)

> Ja, alle drei. 23.5 hat sie schon benannt (*„Beides ist der ersetzte Verfahren-A-Satz (TB-65)"*, `T56b.6`), und 15.1 sagt: **kein Mindesttraining**, 2c: **kein Embargo zwischen Selektionsfalten**. Sie gehören zur Berichtigung Code an 2c/4a wie die drei Felder — und im ERZEUGT-Block von Abschnitt 3 steht die Zeile „Mindesttraining vor der ersten Falte: 4 Jahre" bis heute, was mit dem nächsten Erzeugen des Blocks von selbst verschwindet (39.1: der Block ist noch nicht neu erzeugt).

> **Zur Konstante in `registerdaten.py`** (Sperrlistenpunkt 1, Abschnitt-0-eingefroren): Das Feld und die Zeile gehen jetzt; die Konstante selbst bleibt, bis Punkt 1 ohnehin planmässig geöffnet wird (40.8 (h), die zwölf Rasterachsen) — bis dahin Tatsachennotiz „tot, kein Leser". *Ein Wert, der nichts mehr steuert, aber einen Namen trägt, der eine Regel verspricht, ist die K1h-Klasse; sie wird mit dem nächsten geplanten Zugriff auf die Datei bereinigt, nicht mit einem eigenen.*

Fables Messbitte dazu ist beantwortet, 25c Abschnitt 2 (c), zeichengleich:
„**(c) `MINDESTTRAINING_JAHRE` rechnet nirgends** — zwei tote Felder, eine tote Zeile: dieselbe Berichtigung wie die drei Felder, wie in 25b (4) gesagt; Konstante bis 40.8 (h)."

**Stand, gemessen:** beide Felder aus dem Plan und die Berichtszeile aus
`registerbericht.py` entfernt (TB-106, `abeca36`). `registerdaten.py:108`
`MINDESTTRAINING_JAHRE = 4` steht weiter; gelesen wird es von keinem Modul
(nur in Kommentaren von `faltenplan.py` und `benchmark.py` genannt) — tot, kein
Leser, bis Punkt 1 planmässig geöffnet wird (40.8 (h)). Der ERZEUGT-Block in
Abschnitt 3 trägt die Zeile „Mindesttraining" weiter, bis er neu erzeugt wird
(39.1; G7). Marke bei 23.5.

**E5 (e) — Berichtigung zu 25a Abschnitt 4: der Laufbereich ist die
Vereinigung aller Lauf-Typen** · Art: Berichtigung und Registertext · Quelle:
25b Abschnitt 3 (5) · berichtigt 42.1 (D8)

> **Berichtigung zu 25a Abschnitt 4 (Laufbereich):** Der Laufbereich ist die **Vereinigung** über alle Lauf-Typen des Selektionsmodus. Lauf-Typen sind: der Trockenlauf aller neun Bots; jeder Erzeuger einer registrierten Eingabedatei (`messgroessen.py`, der Listen-Erzeuger auf dem Signalpfad, der Erzeuger der Benchmark-Tabelle mit `faltenplan.py` und seinen Kindprozessen, der Abbild-Erzeuger); `auswertung.py` samt Laufwrapper; die Sonden, soweit sie im Modus laufen. Die Liste der Lauf-Typen ist Registertext und am Tag abschliessend; der Laufbereich wird **am Tag-Commit** über alle Lauf-Typen gemessen (Import-Audit), und das Rückfall-Inventar darüber ist am Tag leer.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5e und die Messung, dass `messgroessen.py` ein Modus-Lauf ist (TB-103) — was unter dem Modus läuft, ist Laufbereich, gleich ob ich es aufgezählt habe. Kein Ergebnis. **Folge:** `herkunft.py` und `shared/regimewache.py` treten mit dem Erzeuger bzw. mit TB-105 (b) ein; die 80 sind ein Zwischenstand mit Datum. Und (c) — die `exit()`-Stellen in `__main__` — gehört dazu, sobald ein Modus-Lauf ein Bot-Skript direkt startet; ob der Listen-Erzeuger das tut (Import oder Kindprozess), ist Handwerk, aber die Regel gilt so oder so, weil der Laufbereich am Tag gemessen wird, nicht heute.

**Stand, gemessen — ein Zwischenstand mit Datum, nicht der Laufbereich:** 80
Repo-Module (TB-104, `516badc`), 81 am Stand `a79e715` (TB-107, 25.09.2026; neu
nur `shared/regimewache.py`), Liste
`docs/belege/TB-107/f1_laufbereich_vereinigung.txt` (84 Zeilen, davon 3
Messumschläge unter `docs/`). Gemessen über drei Lauf-Typen (Trockenlauf aller
neun, Benchmark, Import von `auswertung.py`), **nicht** über die registrierte
Liste der Lauf-Typen — die ist am Tag abschliessend. Die Messung am Tag-Commit
steht aus (42.6).

> ⭐ **42.2 E5 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**E6 (f) — Präzisierung zu 25a (B) (2): der Stichtag ist der Go-Live-Schnitt** ·
Art: Präzisierung · Quelle: 25b Abschnitt 2 (3) · präzisiert 42.1 (D3/D7)

> **Präzisierung zu 25a (B), Teil (2):** Die geladene Menge je Bot wird **am Stichtag Go-Live-Schnitt (5.2), ausschliesslich** ermittelt — jede Kursreihe auf den Stichtag gekürzt, Loader wie in TB-40 — und gegen die Bestätigungsspalte von 16.1.1 verglichen. Ein Trockenlauf am Datenende bleibt zulässig als Nachweis „kein Fallback"; die Mengenprüfung gegen das Register läuft am Stichtag. Tatsachennotiz: am Stand `63e4b6c8…` ergeben beide Stichtage bei 9/9 Bots dieselbe Menge (TB-104).

*Seine Quelle des Grundes, zeichengleich:* „16.1.1 wurde so gemessen; eine Prüfung gegen das Register nimmt das Verfahren des Registers. Kein Ergebnis."

**E7 (g) — Tatsachennotizen zu TB-104** · Art: Tatsachennotiz · Quelle: 25b
Abschnitt 4, Zeile g. ⚠️ **Fable nennt hier nur Stichworte; die Notiz ist eine
eigene Fassung der Sitzung, kein Fable-Wortlaut** (gemessen,
`docs/ERGEBNIS_TB-104_leser_auf_resolver_und_altfelder.md`, `516badc`). Sein
einziger ausformulierter Satz dazu, 25b Abschnitt 2 (1), zeichengleich:
„*Was ihr mit „heute gleich, keine Eigenschaft des Codes" benennt, ist TB-102 in Kleinformat und gehört als Tatsachennotiz zu 37.4.*"

| | Tatsache (TB-104) |
|---|---|
| Leser | `benchmark.py`, `faltenplan_neun.py`, `loaderlauf.py`, `universum_trockenlauf.py` auf `shared/paths.py` (`572d725`); Ersatzwurzeln unter dem Modus 2, bevor gelesen wird; ohne Modus 8 Ausgaben bytegleich |
| Felder | `purge_tage`, `embargo_tage`, `training_bis_ausschliesslich` aus dem gerechneten Plan (`f334a7b`); Faltengrenzen gleich; `G8`/`G9` angepasst, `G8M` mit Gegenprobe |
| Abbild | `sperrliste_abbild_2026-09-25.json` `cb4eb1b4cf998efcded95acd4d712bb3a0856722489a80ce10bfce511eeb5f89` (`d96b352`) |
| Benchmark im Modus | zweimal bytegleich `64fb2912…`; Kurse und Universum nur aus dem Snapshot; ausserhalb die neun TB-24-Listen und `messgroessen.json` ⇒ Nachweis 2 |
| Umgebungsliste | dieselben fünf Dateien wie TB-103 |
| Schreibziel | `manuelle_eingriffe.log` im Modus `a` über `registerdaten.py:62` → `notifications/manual_close.py` (behoben TB-105, D11) |
| zu 37.4 | `herkunft.py::datenstand(daten_dir=None)` nimmt das Verzeichnis als Argument; `block()` rief es damals ohne Argument — geöffnet in TB-106 (42.3, F2) |
| zu 11.1 | `regimewache.pruefe_einbau()` **0 von 3** — die offene Voraussetzung, geschlossen in TB-105 (G1) |
| Laufbereich | 80 Module, Stand 25.09.2026, 10:32 (E5) |

**E8 (h) — „offen bis zur Messung"** · Art: offene Punkte — ⭐ **BEANTWORTET
durch 25c** · Quelle: 25b Abschnitt 4, Zeile h: „`_bedingung` `None` (α oder β) — **vor TB-106**; `anhaengen()`; `_min_history` bei Fehltreffer; `MINDESTTRAINING_JAHRE` in `erste_falte_4a`"

Alle vier sind beantwortet und umgesetzt: `_bedingung` 42.3 (F1, TB-106) ·
`anhaengen()` 42.3 (F2, TB-106) · `_min_history` 42.3 (F4, TB-107) ·
`MINDESTTRAINING_JAHRE` E4 oben (25c 2 (c), TB-106).

### 42.3 Aus Fable 25c (`FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md`)

**F1 (a) — „keine Rasterbedingung (Abschnitt 6)"; unbekannter Bedingungstext ⇒
2, eine Deutung** · Art: Berichtigung einer Benennung und Registertext ·
Quelle: 25c Abschnitt 1

> **Eine Fundstelle berichtige ich an eurer Berichtigung:** Der Satz *„Zellen, in denen die Strategie nicht definiert ist, existieren nicht … von 1.024 auf 384"* steht in **Abschnitt 6 (Die Plateau-Regel)**, im Absatz nach der Spitzenformel — nicht in Abschnitt 4. Abschnitt 4 ist die Drawdown-Bedingung, also genau das, wovon ihr den Zustand abgrenzen wollt; „keine Rasterbedingung (Abschnitt 4)" würde beim nächsten Leser dieselbe Verwechslung erzeugen, die ihr gerade auflöst. Richtig: **„keine Rasterbedingung (Abschnitt 6)"**. *[Gelesen im Register, Teil 1; nicht im Repo gemessen — die Nummer ist im Kopf der Kopie nachzusehen, sie lässt sich nicht verwechseln.]*

> **Registertext, Ergänzung zu 6 und 24b A2 — unbekannter Bedingungstext:** Ein nicht leerer `_bedingung`-Text, den der Code nicht als Rasterbedingung erkennt, ist ein Widerspruch zwischen Register und Code und endet mit 2 — unabhängig vom Modus. Die Deutung des Textes geschieht an **einer** Stelle; jeder Leser (Zellenzahl, Zellmenge, Nachbarschaft) ruft sie. Ein zweiter Textvergleich desselben Strings ist ein zweiter Parser (24b B4).

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 6 (die Rasterbedingung ist Registertext; ein Code, der sie still übergeht, rechnet ein anderes Raster mit N = 1.024 statt 384 und macht Abschnitt 3 und Festlegung 10 unbemerkt falsch), 24b A2, 24b B4. Kein Ergebnis. **Für TB-106:** rc 2 in `auswertung.py` jetzt; die zweite Stelle (`registerdaten.py:605`, Punkt 1) bekommt die Tatsachennotiz bis 40.8 (h), und **dort** wird die Deutung auf eine Funktion zusammengezogen, die beide rufen — nicht früher, weil Punkt 1 nicht für diesen Satz allein geöffnet wird. Eure Neigung „unabhängig vom Modus" ist richtig, aus eurem Grund.

**Stand, gemessen:** `auswertung.py` endet bei unbekanntem `_bedingung`-Text mit
2 (TB-106, `5cc1de4`). Die zweite Deutungsstelle steht weiter:
`registerdaten.py:605` vergleicht den String `"t3_fast_length <
t3_slow_length"` selbst (Punkt 1, unverändert seit vor 4faef05) — Tatsachennotiz
bis 40.8 (h), dort auf eine Funktion zusammenzuziehen. Marke bei 6.

**F2 (b) — Berichtigung zu 37.4: `herkunft.py` einmal geöffnet** · Art:
Berichtigung · Quelle: 25c Abschnitt 2 (a) · berichtigt 37.4

> **Berichtigung zu 37.4 (Entscheidung „Nicht öffnen"):** `herkunft.py` wird einmal geöffnet, um `datenstand()` den Datenpfad durch `block()` und `anhaengen()` durchzureichen (Argument, keine Voreinstellung unter dem Modus). Sonst ändert sich nichts: `EINGEFROREN` bleibt, wie 39.7 es entschieden hat; `register()` bezeugt weiter die Abschnitt-0-Menge; die Sonde bezeugt Abschnitt 10. **Planmässig geöffnet heisst nicht offen** — eine Öffnung nach 37.3 trägt genau die Änderung, für die sie beauftragt ist.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 37.4 nannte als Grund für „nicht öffnen" den Ort, nicht den Wortlaut, und die Sonde als Ersatz; für den Datenpfad der Protokollkette gibt es keinen Ersatz ausser einem zweiten Ort (25a). Der Satz „heute gleich, aber keine Eigenschaft des Codes" ist TB-102 in Kleinformat und steht als Tatsachennotiz daneben. Kein Ergebnis.

**Stand, gemessen:** geöffnet in TB-106 (`5791b4c`): `block()` und `anhaengen()`
reichen `daten_dir` an `datenstand()` durch, unter dem Modus Pflicht (sonst 2);
kein `makedirs` mehr; im Modus hasht die Kette den Snapshot (`d9449faf…`).
`EINGEFROREN`, `register()` und `SPERRLISTE_DATEIEN` zeichengleich (TB-106 E4).
Hash `56a1c2e1…` → `351f24c2…`, Punkte 11 und 12 (42.5). ⚠️ **Folgefragen 25d
(2) und (3)** (Prüfansicht unter dem Modus; `TB30A_BASE_DIR` wirkt in
`herkunft.py:51` auch unter dem Modus, G6) — offen, 42.6. Marken bei 37.4 und
39.7.

**F3 (c) — Tatsachennotiz zu 11: 11.1 geschlossen, 11.2/11.3 offen** · Art:
Tatsachennotiz · Quelle: 25c Abschnitt 3

> ⚠️ **Damit niemand „Abschnitt 11 erfüllt" liest:** Der Schlusssatz von Abschnitt 10 nennt **beide** Bug-Fixes aus 11. Erfüllt ist **11.1**. 11.2 (Agent 2 auf dem führenden Mass; `evaluate_combination_multi` liefert den Kapital-Drawdown noch nicht) und 11.3 (Durchreichung `sma_trend_filter`, `bb_*`) sind **TB-30b** und offen — sie gehören zum Laufcode, den es nach 24.5 noch nicht gibt. Tatsachennotiz zu 11: 11.1 geschlossen (TB-105), 11.2/11.3 offen.

⚠️ **Das gehört zu Abschnitt 10** (dessen Schlusssatz beide Bug-Fixes nennt);
nach 41.0 steht dort keine Marke — die Notiz steht hier und bei 11. Messung in
42.4 (G1).

**F4 (d) — `_min_history`: genau ein Treffer oder 2; die Erzeugerkette des
Trockenlaufs** · Art: Registertext · Quelle: 25c Abschnitt 4 (2) und 3

> `re.findall`, genau ein Treffer, sonst `SystemExit(2)`, unabhängig vom Modus; Mutationsproben „zwei Treffer" und „kein Treffer". Der Grund für „unabhängig vom Modus" ist derselbe wie bei (1): Ein Muster, das in einer Bot-Datei nicht genau einmal trifft, ist ein Widerspruch zwischen der registrierten Tabelle in 16.7 (b) und dem Code — kein Laufzustand. Und der stille Hinweis in `kerzen_elliott_wave()` ist die TB-45-Klasse (weiter ohne Wert); der `TypeError` in `loader_lesart()` ist laut, aber 1 statt 2 — nach 36.5 ein Aufruf, der nicht messen konnte und es nicht mit dem eigenen Wert sagt. Beides geht mit.

> **Zur Zwischenablage:** (1) und (2) erfüllt, (3) nicht — Befund 1, Handwerk. Eine Ergänzung zur Datei: `universum_trockenlauf.py` steht nicht im Abbild, und das ist heute richtig; **mit dem Faltenplan-Abbild (TB-100) wird die Erzeugerkette des Trockenlaufs registriert** — 33.3 sagt es schon: *„der erzeugende Code wird mit der Datei registriert (5e)"*. Bedingung (ii) der ersten Falte kommt aus dieser Kette (25.3); ein Abbild, dessen Erzeuger ungebunden ist, bezeugt weniger, als es sagt.

**Stand, gemessen:** `faltenschranke_messung.py::_min_history()` mit
`re.findall`, genau ein Treffer, sonst rc 2; `kerzen_elliott_wave()` ohne Wert
rc 2 (TB-107, `33d50f2`); je Bot-Datei genau ein Treffer (G9). ⚠️ **Die
Erzeugerkette ist nicht registriert** — sie kommt mit dem Faltenplan-Abbild
(Plan-Punkt 7, TB-101; die Nummer TB-100 aus 25c ist nie ausgelöst worden) —
offen, 42.6. Marke bei 33.3.

**F5 (e) — Ersatzmodule der Regelbetrieb-Wächter; Gegenprobe über alle
`__main__`-Stellen** · Art: Tatsachennotiz und Registertext · Quelle: 25c
Abschnitt 4 (3)(a)

> **(a) Die Modus-Abfrage an den 14 Stellen selbst — in Ordnung, mit einer Tatsachennotiz und einer Gegenprobe.** Das Verfahren zählt keine Zeilen; es verlangt, dass es einen Resolver gibt und keinen Fallback. Vierzehn Aufrufe derselben Funktion (`paths.selektionsmodus()`) sind kein zweiter Ort für einen Wert — der Wert lebt in `paths.py`. **Der eigentliche Befund ist der, den ihr gefunden habt:** Drei Regelbetrieb-Werkzeuge (`kurven_lauf.py`, `determinismus_lauf.py`, `messung_primaerschluessel.py`) ersetzen `strategy_paths` in `sys.modules` durch ein Teilmodul. Das ist im Regelbetrieb Handwerk mit Live-Freigabe; **im Laufbereich wäre es ein zweiter Resolver.** Regel daraus, klein: Ein Werkzeug, das den Resolver-Nachbarn austauscht, endet unter dem Modus mit 2, bevor es das tut — dann kann es nie in den Laufbereich geraten. Tatsachennotiz zu den drei Dateien; ob ihr sie ändert, ist Live-Freigabe. **Gegenprobe zu den 14 Stellen:** eine Prüfung, dass jede `__main__`-Stelle im Laufbereich die Abfrage trägt — sonst fehlt sie beim fünfzehnten Skript still (dieselbe Kopplung wie `G6`). Handwerk.

**Stand, gemessen:** Die drei Werkzeuge ersetzen `strategy_paths` weiter in
`sys.modules` (`shared/kurven_lauf.py:129`, `shared/determinismus_lauf.py:162`,
`research/zuteilungskaskade/messung_primaerschluessel.py:119`; G3) —
unverändert, Betreiber 25.09.2026, 18:09: vorerst nur Notiz. ⚠️ **Die Regel
„endet unter dem Modus mit 2, bevor es das tut" ist an ihnen nicht umgesetzt**
(Live-Freigabe). Die Gegenprobe ist gebaut: `shared/test_main_gegenprobe.py`
(TB-107, `9827a3e`), liest die Liste aus
`docs/belege/TB-107/f1_laufbereich_vereinigung.txt`, 14 Datenstellen, alle mit
Abfrage, 7/7.

**F6 (f) — `getattr`-Ersatz in `strategy_paths.py`: ein Rückfall, entfernt** ·
Art: Tatsachennotiz · Quelle: 25c Abschnitt 4 (3)(b)

> **(b) `getattr(paths, "selektionsmodus", None)` — ja, ein Rückfall der Form nach; entfernen.** Eure Neigung ist richtig, und der Grund ist stärker, als ihr ihn nennt: Fehlt dem Nachbarn die Funktion, kann `strategy_paths.py` **nicht wissen**, ob der Modus an ist — und „dann Regelbetrieb" ist eine Annahme über genau die Frage, die der Modus beantwortet. Ein Nachbar ohne die Funktion ist kein Nachbar; das ist 19 (gespaltener Baum) in kleiner Form. Also: direkter Aufruf, ohne Modus wie mit Modus, und die zwei Proben bekommen ein `paths`, das die Funktion trägt. Dass `_resolver_ist_nachbar()` das echte `paths.py` zusichert, macht den Zweig unerreichbar, nicht zulässig — euer Zitat aus 25b trifft.

**Stand, gemessen:** entfernt in TB-107 (`5cfe472`): `_im_selektionsmodus()`
ruft `paths.selektionsmodus()` direkt (`shared/strategy_paths.py` Z. 122); ohne
Modus 101 Aufrufer in 9 Bots, Pfade und Ordner vorher = nachher. ⚠️
**Nebenwirkung:** `research/resolver_selektion/pfadvergleich.py` (nicht
freigegeben, unverändert) endet seitdem mit rc 1 statt 0 — Frage 25e (3), 42.6.

**F7 (g) — Klasse (ii) umfasst Interpreter-Caches als Muster** · Art:
Registertext (Ergänzung zu 25a (A) (ii)) · Quelle: 25c Abschnitt 4 (4)(a) ·
ergänzt 42.1 (D6)

> **(a) Bytecode-Caches — Klasse (ii), Umgebung.** Der Interpreter schreibt sie, nicht der Lauf; ihr Inhalt ist aus dem registrierten Code abgeleitet und keine Eingabe; sie liegen ausserhalb Repo und Snapshot. In der Umgebungsliste stehen sie als **Muster** (`~/Library/Caches/com.apple.python/<wurzel>/…`), nicht als Pfade — der Klonpfad wechselt. Zwei Bedingungen, damit (ii) nicht zur Hintertür wird: Ein `__pycache__` **im Repo** ist nur zulässig, wenn es git-ignoriert ist und nicht unter `snapshots/` liegt (im Klon war `--ignored` leer — gemessen, gut); und ein Cache ist nie Eingabe im Sinn von 5e — der Lese-Audit führt `.pyc`-Zugriffe unter (ii), nicht unter (i).

**F8 (h) — registrierte Protokolle als eigene Zeile in (iii); Ausnahme von 19**
· Art: Registertext (Ergänzung zu 25a (A) (iii)) · Quelle: 25c Abschnitt 4
(4)(b) · ergänzt 42.1 (D6)

> **Ergänzung zu 25a (A) (iii) — registrierte Protokolle:** Zulässige Schreibziele eines Modus-Laufs sind `--ziel`, Belegpfade, Zwischenablagen nach (iv) und **registrierte Protokolle** — heute genau eines: `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl` (10.1). Ein registriertes Protokoll ist append-only: Die Schreibregel 36.1 gilt in Anhängeform — nie kürzen, nie umschreiben, nie neu anlegen, wenn es existiert; seine Unversehrtheit prüft der Kettenhash (10.1), und `--pruefen` liest es als registrierte Eingabe (i). **Sein Ordner wird nicht angelegt:** Fehlt der registrierte Ort, endet `anhaengen()` mit 2 — ein fehlender Ort ist ein Baum, der nicht der registrierte ist, und ein `makedirs` wäre ein Fallback für genau diese Feststellung. **Ausnahme von 19:** Registrierte Protokolle sind von der Sauberkeitsprüfung des Arbeitsbaums ausgenommen wie `data/` (19), weil sie planmässig während des Laufs wachsen; die Ausnahme ist auf die namentlich registrierten Pfade beschränkt, und der Kettenhash ersetzt dort die Sauberkeit.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 10.1 (das Protokoll ist der Ort der Läufe, append-only, Kettenhash), 38.3 (es entsteht mit dem Erzeuger), 19 (die `data/`-Ausnahme mit ihrem Grund: eine Datei, die planmässig zwischen Läufen wechselt, darf die Startprüfung nicht auslösen). Kein Ergebnis. *Warum die Ausnahme jetzt und nicht später:* Sobald 19 auf den Laufbereich erweitert ist, liegt das Protokoll unter einem geprüften Pfad — der zweite Lauf würde an der Spur des ersten scheitern. Der 19-Auftrag braucht diese Zeile, bevor er beginnt.

> **Zu `makedirs` in `anhaengen()`:** Der Ordner `ergebnisse/` trägt versionierte Dateien und existiert in jedem Klon; das `makedirs` ist tot — und geht mit derselben Öffnung (2 (a)) heraus, weil eine tote Zeile mit Fallback-Form dieselbe Klasse ist wie `getattr` in (3)(b).

⭐⭐ **Reihenfolge, wie Fable sie verlangt:** Die Ausnahme von 19 steht **mit
diesem Eintrag im Register, vor dem Auftrag, der 19 auf den Laufbereich
erweitert** (42.2, E2). Der Auftrag zur Erweiterung von 19 kann sich auf F8
stützen.

⚠️ **Das gehört auch zu 10.1** (das Protokoll ist dort registriert); nach 41.0
steht dort keine Marke — die Notiz steht hier und bei 19.

**Stand, gemessen:** Ordner-Regel umgesetzt in TB-106 (`5791b4c`: kein
`makedirs`, fehlender Ordner ⇒ 2). `herkunft_protokoll.jsonl` **existiert
nicht** (TB-108, `a3_stand.txt` (2)) und wurde nicht angelegt.

> ⭐ **Vollzogen, siehe 44.2 (44-7; TB-112 `9d711dc`, TB-113, 26.09.2026):**
> Die Ausnahme von 19 steht als `REGISTRIERTE_PROTOKOLLE` (genau
> `herkunft_protokoll.jsonl`) in `shared/paths.py` und wirkt als
> `:(exclude)` in der Sauberkeitsprüfung. Das Protokoll existiert weiter
> nicht. Eintrag und Stand oben bleiben zeichengleich.

### 42.4 Tatsachennotizen aus TB-103 bis TB-107

*Eigene Fassung der Sitzungen, gemessen; kein Fable-Wortlaut.* Belege je Zeile
im genannten Ergebnisdokument.

| | Tatsache | Ergebnisdokument, Commit |
|---|---|---|
| G1 | **11.1 geschlossen:** `regimewache.pruefe_einbau()` 3 von 3 (heute nachgemessen: `vollstaendig: True`); ohne BTCUSDT bricht jede der drei Stellen mit `RegimefilterFehlt` ab. **Vorher** rechnete `t3_supertrend` ohne BTCUSDT still weiter, mit anderem Trade-Hash — der Determinismus-Befund, mit dem 11.1 begründet ist, gemessen. **11.2 und 11.3 offen** (TB-30b) | `ERGEBNIS_TB-105` A1, B; `f524327` |
| G2 | Rückfall (c): 14 × „Keine Daten gefunden" in `__main__` unter dem Modus rc 2, ohne Modus unverändert; Rückfall (a): `symbols_config.py` unter dem Modus rc 2 bei leerer oder fehlender Liste | `ERGEBNIS_TB-105` C, D; `f65c344` |
| G3 | Ersatzmodule für `strategy_paths` in `shared/kurven_lauf.py`, `shared/determinismus_lauf.py`, `research/zuteilungskaskade/messung_primaerschluessel.py` (F5) | `ERGEBNIS_TB-105` Abschnitt 5, Befund 1 |
| G4 | TB-106: keine der Ersatzwert-Stellen wird von der registrierten Eingabe erreicht (A8-Tabelle je Stelle); `benchmark.py::nachschlagen()` ist eine Rechenregel (Grenzwert 0), kein Ersatzwert, unverändert; `register()` `57ec6573…` ⇒ `0ece95e2…`; Abbild `40ffe18d…`; Datenstand der Kette im Modus `d9449faf…` = registrierter Datenstand | `ERGEBNIS_TB-106` A, E, F; `f22f91e` |
| G5 | `auswertung.Abbruch` ist `SystemExit` ohne eigenen Wert und endet mit **1** (Vertragsbruch der Rohergebnisse) — ob 1 oder 2, ist Frage 25d (4) | `ERGEBNIS_TB-106` A10 |
| G6 | `TB30A_BASE_DIR` wirkt in `herkunft.py:51` auch unter gesetzten Modus-Variablen, auf Commit und Registerdatei — Frage 25d (3) | `ERGEBNIS_TB-106` A11 |
| G7 | `registerbericht.py --pruefen` war schon vor TB-106 rot: der ERZEUGT-Block in Abschnitt 3 ist veraltet (39.1) | `ERGEBNIS_TB-106` Befund 2 |
| G8 | Laufbereich 81 Module am Stand `a79e715`, neu gegenüber TB-104 nur `shared/regimewache.py`; Liste `docs/belege/TB-107/f1_laufbereich_vereinigung.txt` (E5) | `ERGEBNIS_TB-107` F1; `9827a3e` |
| G9 | `elliott_wave` trägt `MIN_HISTORY_HOURS`, die acht übrigen `MIN_HISTORY_DAYS`, je genau einmal in `multi_symbol_optimise.py` (heute nachgemessen) | `ERGEBNIS_TB-107` A2 |
| G10 | Die Benchmark-Tabelle `64fb2912f1a2ffb02a36834857fe9a91529b7517a8a7185f5fd7b11642f873b7` ist durch TB-103 bis TB-107 **unverändert**; im Modus bytegleich reproduziert in TB-104 (zweimal), TB-105, TB-106 und TB-107 (je Repo und frischer Klon), ohne Modus ebenso — als Nachweis nach 41.2 (B4) weiter **2** | `ERGEBNIS_TB-104` C5 bis `ERGEBNIS_TB-107` G |
| — | ⚠️ **`f5fdb53` (TB-107 Block C, `faltenplan_neun.py`) ist vor Fables Antwort auf 25d gebaut** und als eigener Commit revertierbar (`git revert f5fdb53` nimmt Code und Probendatei zurück) | `ERGEBNIS_TB-107` Abschnitt 3 |

### 42.5 ⭐⭐ Tatsachennotizen zu 37.3 — die Hash-Übergänge seit 39.5

37.3 verlangt für jeden planmässigen Befund vor dem Tag: Auftrag, Freigabe,
alter und neuer Hash. Gemessen in TB-108 aus der Historie
(`git show <commit>~1:<pfad>` bzw. `<commit>:<pfad>`) für **jeden Pfad des
Abbilds `40ffe18d…`** (vierzehn Punkte und Gruppe „eingefroren") seit
`4faef05` (Ende TB-94, Stand von 39.5); Beleg
`docs/belege/TB-108/c_hashuebergaenge.txt`. Freigaben aus den
Ergebnisdokumenten nachgelesen.

| Datei | alt → neu | Auftrag / Commit | Freigabe | Punkte |
|---|---|---|---|---|
| `research/vorregistrierung/messgroessen.py` | `623f8d771ffd5ae9dc1b979fbe383c85268371ba4f1dfeff055379662be41f25` → `59b396e76af33dfc5549c7a40032d44963b02d3305bf4bf9e721b06001d0301c` | TB-103, `ae136fd` | Betreiber 24.09.2026, 22:52 | ⚠️ **kein Punkt, aber `EINGEFROREN`** — nach 39.7 (23c) gesperrt |
| `research/vorregistrierung/benchmark.py` | `d6bdd55805344da09b6b43d791267b43c9702687fc1c7cdbad1473079443e061` → `4c923cd907c6aa9b14fd035fd775ced00bfcaff0795288dc4b1ccd48d19fc5b8` | TB-104, `572d725` | Betreiber 25.09.2026, 07:52 | 4 und 6; `EINGEFROREN` |
| `research/vorregistrierung/faltenplan.py` | `7aa0b8ccf5619a21d5f082f68d81cb412f98ae9c9724e799da8b48dce7498cfb` → `d57fe9c977e572e1d344971913e3acbb1cd765d2bf145b52cefab69d75e10f41` | TB-104, `f334a7b` | Betreiber 25.09.2026, 07:52 | 2; `EINGEFROREN` |
| `research/vorregistrierung/faltenplan.py` | `d57fe9c977e572e1d344971913e3acbb1cd765d2bf145b52cefab69d75e10f41` → `63dafeb44e027cb5d93ac19cddfc7d4e98b468cece116512c2b3f1601bd4a4c7` | TB-106, `abeca36` | Betreiber 25.09.2026, 18:09 | 2; `EINGEFROREN` |
| `research/vorregistrierung/benchmark.py` | `4c923cd907c6aa9b14fd035fd775ced00bfcaff0795288dc4b1ccd48d19fc5b8` → `aeeec9b89bdadd1b2dc2be76b722dc90c328c9482014bbbbfcabd78edccae219` | TB-106, `a08c13a` | Betreiber 25.09.2026, 18:09 | 4 und 6; `EINGEFROREN` |
| `research/vorregistrierung/auswertung.py` | `c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062` → `83c6bc3c9b683d0bfd9d8c445492060f93759a551d0dcf329b2bd21b0f1cc5a1` | TB-106, `5cc1de4` | Betreiber 25.09.2026, 18:09 | 3, 5 und 14; `EINGEFROREN` |
| `research/vorregistrierung/herkunft.py` | `56a1c2e1514385acd26c3432bd111f3588846c80d173a4d4a471ecae723fb502` → `351f24c2d6a3a512dc1eb1a80b536b99d47c266db38f7dd93b9d1c0199397eef` | TB-106, `5791b4c` (42.3, F2) | Betreiber 25.09.2026, 18:09 | 11 und 12 |
| `research/vorregistrierung/registerbericht.py` | `dace1b01826fa6a999beb9a15a8eda41a4e0c97dec584e451cfc0d9b26daac01` → `de35a5a09d103def310d473170d6e638cfd1f1a24f46f7b1d1e033a674134db7` | TB-104, `f334a7b` | Betreiber 25.09.2026, 09:10:49 (Zusatzfreigabe) | ⭐ auf keinem Punkt — nur Tatsachennotiz |
| `research/vorregistrierung/registerbericht.py` | `de35a5a09d103def310d473170d6e638cfd1f1a24f46f7b1d1e033a674134db7` → `74a22daec99dd4ba2057206fca22596bdc1d3bd7de5dbf465c14c44bb952eb89` | TB-106, `abeca36` | Betreiber 25.09.2026, 18:09 | ⭐ auf keinem Punkt |

**Unverändert seit `4faef05`:** `registerdaten.py` (Punkt 1), `kennzahlen.py`,
`pruefe_grenzsaetze.py`, `shared/zuteilung.py` (Punkt 10), beide
Universumsdateien (Punkt 8) und alle Ergebnisdateien unter `ergebnisse/`, die
auf der Sperrliste oder in `EINGEFROREN` stehen. `test_vorregistrierung.py`
(auf keinem Punkt) hat sich in TB-95, TB-97, TB-103, TB-104 (zweimal) und
TB-106 bewegt; die Kette steht im Beleg.

**Die Abbilder, die diese Übergänge schliessen** (37.3: neues Abbild unter neuem
Namen, das alte bleibt): `sperrliste_abbild_2026-09-23.json` `2f23f76c…` (39.9)
→ **`sperrliste_abbild_2026-09-25.json`
`cb4eb1b4cf998efcded95acd4d712bb3a0856722489a80ce10bfce511eeb5f89`** (TB-104,
`d96b352`; erzeugt an `f334a7b`, das erste Abbild mit der Gruppe „eingefroren",
das `messgroessen.py` mit dem neuen Hash führt) → **`sperrliste_abbild_2026-09-25b.json`
`40ffe18d6a6345d1ab88aa993535cfb10264d8cf2e02e804406bbe85236642c8`** (TB-106,
`e1e6652`; erzeugt an `5791b4c`). Sonde gegen `40ffe18d…` am Eingang von TB-108:
Pfad-Bestandteile 25/0/0, Prüfung (ii) 0 (`docs/belege/TB-108/0_sonde_vorher.txt`).

⚠️ **Zu `messgroessen.py`:** Der Auftrag TB-108 nannte für diese Notiz TB-104
und TB-106. Gemessen ist ein dritter Übergang an einem gesperrten Pfad, TB-103
(`ae136fd`) — `messgroessen.py` steht auf keinem Punkt des Abschnitts 10, aber
in `herkunft.py::EINGEFROREN`, und nach Fables Präzisierung zu 36.1 (1) (39.7)
ist jeder Pfad gesperrt, dessen Hash am Tag bezeugt wird. Freigegeben war die
Änderung (TB-103, Kopf des Ergebnisses: „`paths.py`, `messgroessen.py` und ihre
Tests"); ihr Ergebnis nennt die Berührung als A8 (a). **Eingetragen ist, was
gemessen ist.**

**`herkunft.register()` über die Abschnitt-0-Menge** (Registerdatei plus
`EINGEFROREN`), nachgebaut je Commit aus der Historie (Probe: am Eingang von
TB-108 gleich dem gemessenen Wert):

| Stand | `register()` |
|---|---|
| `4faef05` (Ende TB-94) | `f63c181bd46e5ae481b34bbdddd9178f42255214f892cc73468948c26f54ebc5` |
| `d0dc890` (TB-96, Register 40) | `89f0ab5f9be1cee9cc8978ac9e6012623a6bc922775c658debf9f84c957c61cc` |
| `ae136fd` (TB-103, `messgroessen.py`) | `becfa3c9430946a1021e7a990e5804290cb8f0520e5355a8f2e077f9a7678476` |
| `572d725` (TB-104, `benchmark.py`) | `cca9bb787629136dc2d742b09be9f1e18e4fa3964324a505be295dac1384f795` |
| `f334a7b` (TB-104, `faltenplan.py`) | `57ec6573eb44f18bccaa461da41ac0b835ba1afa1446ef27b4c3409ead56e46e` |
| `abeca36` (TB-106, `faltenplan.py`) | `f42d6d84515aba19765a2d25cb542afeea8dec81433eb5d79d43f3d6a9df1561` |
| `a08c13a` (TB-106, `benchmark.py`) | `cad1495b4fc42f156a15a92c7cd8be7cfe9a7bae1dc7c443d6303729dc4ce107` |
| `5cc1de4` (TB-106, `auswertung.py`) bis zum Eingang von TB-108 | `0ece95e2fd4f5bd2787ea40f6a12988aadb0a414c5132553522b55000c6052d7` |

⚠️ **Die letzte Zeile, und warum der neue Wert hier nicht stehen kann:** Mit
diesem Eintrag ändert sich `register()` zwangsläufig, weil die Registerdatei
selbst Teil der Menge ist. Vorher: **`0ece95e2fd4f5bd2787ea40f6a12988aadb0a414c5132553522b55000c6052d7`**.
Der Wert **nach** diesem Eintrag hängt vom Text dieses Eintrags ab und kann
deshalb nicht in ihm stehen; er ist nach dem Commit gemessen und steht voll in
`docs/ERGEBNIS_TB-108_register_41_42.md` und
`docs/belege/TB-108/h1_hashes_nachher.txt`.

### 42.6 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | **Fable 25d** (vier Fragen: die Kopie in `faltenplan_neun.py` — `f5fdb53` gebaut, revertierbar; die Prüfansicht von `herkunft.py` unter dem Modus; `TB30A_BASE_DIR` unter dem Modus (G6); `auswertung.Abbruch` 1 oder 2 (G5)) | Abschnitt 43 |
| (2) | **Fable 25e** (drei Fragen: `tb40_faltenplan_*`/`tb40_proben_*` (E1); `trades.empty ⇒ exit()`; `pfadvergleich.py` rc 1 (F6)) | Abschnitt 43 |
| (3) | **Fable 25f** (Gesamtanalyse) | Abschnitt 43 |
| (4) | **Die Erweiterung von 19 auf den Laufbereich** (42.2, E2) — Tag-Vorbedingung (25c 2 (d)). Die Ausnahme für registrierte Protokolle, die Fable **vorher** im Register verlangt (25c (h)), steht jetzt in 42.3 (F8) | eigener Auftrag |
| (5) | **Der Erzeuger auf dem Signalpfad** (41.1 A12, 41.2 B3/B6/B7) — und mit ihm die neun Listen, der Deckel von `t3_supertrend` (41.3 C2), die Donchian-Eingabe, `messgroessen.json` neu und der Benchmark-Nachweis mit beiden Teilen (41.2 B4) | Plan-Punkte 3 und 5 |
| ↳ (5) | ⭐ **Abnahmebedingungen des Erzeugers: siehe 45.5** (Fable 26a R5, TB-114, 26.09.2026); die Zeile oben bleibt zeichengleich | 45.5 |
| (6) | **Das Faltenplan-Abbild samt Erzeugerkette des Trockenlaufs** (33.3; 42.3 F4) | Plan-Punkt 7, TB-101 |
| (7) | **Die Feldliste des gerechneten Plans als Registertext** — je Schlüssel die begründende Registerstelle; die registrierte Abbildung (42.2, E3) | mit (6) |
| (8) | **H6 eigenständig oder als Paar gezählt**; danach ggf. „sieben" berichtigen (41.1, A4) | vor dem Tag |
| (9) | **Ladeprotokoll-Teil (4)** — Zeilenzahl der Universumsdatei und Quelle der Liste (42.1, D3/D7) | Handwerk mit Freigabe |
| (10) | Der Laufbereich und die Liste der Lauf-Typen **am Tag-Commit** (42.2, E5); der Trockenlauf aller neun am Tag-Commit (42.1, D4) | Tag |
| (11) | Die Regel „Resolver-Nachbar austauschen ⇒ unter dem Modus 2" an den drei Werkzeugen (42.3, F5) | Live-Freigabe |
| (12) | Die zweite Deutungsstelle der Rasterbedingung `registerdaten.py:605` (42.3, F1) und die tote Konstante `MINDESTTRAINING_JAHRE` (42.2, E4) | 40.8 (h) |

> ⭐ **Beantwortet (TB-110, 26.09.2026):** (1) Fable 25d in **43.1**, (2) Fable
> 25e in **43.2** — dazu eine vorläufige Berichtigung des steuernden Chats an
> 25e (3) in **43.3**. (3) Fable 25f bleibt offen (43.5 (9)). Die Tabelle oben
> bleibt zeichengleich.

### 42.7 Was hier ausdrücklich NICHT getan wurde

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert, nichts gerechnet** — auch wo ein Eintrag eine Codeänderung nahelegt (H6, Ladeprotokoll, Wächter-Ersatzmodule, `bot_lauf.py`-Kopf) | 42.6 |
| ⛔ | **Kein neues Abbild** — keine Sperrlistendatei hat sich bewegt; das gültige Abbild bleibt `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`), Sonde vorher und nachher gleich (`0_sonde_vorher.txt`, `d3_sonde_nachher.txt`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — Marken sind neue Zeilen, nichts entfernt | — |
| ⛔ | **Keine Marke in Abschnitt 10** (Listentext Z. 868–981, geprüft von der Sonde, Prüfung (ii)); was dorthin gehörte (F3: Schlusssatz zu Abschnitt 11; F8: 10.1), steht hier | — |
| ⛔ | **Nichts aus 25d, 25e, 25f** | Abschnitt 43 |
| ⭐ | **Sichtschutz 27.1:** keine Ergebnisgrösse des Selektionsraums; Feldnamen ohne Werte | — |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich): 5.1
Nr. 4 · 5.4 · 6 · 11 (am Ende, in 11.3) · 12 · 15.4 (2d, Tabelle des Deckels)
· 16.6 · 19 (zweimal: unter dem Registertext 5e und unter der Tabelle der
Startprüfungen) · 23.5 · 33.3 · 35.4 · 36.5 · 37.3 · 37.4 · 39.6 · 39.7 · 39.8
· 40.6 · 40.7.

*Diese zwei Abschnitte sind rein additiv: Sie tragen die entschiedenen Einträge
des Verfahrensprüfers aus sechs Antworten zeichengleich ein, beide Fassungen
jeder Kette mit Verweis, die Tatsachen aus fünf Aufträgen und die
Hash-Übergänge seit 39.5 — und entfernen nichts. Gebaut und gerechnet wird
nichts.*

