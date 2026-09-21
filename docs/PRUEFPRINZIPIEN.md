# Prüfprinzipien

**Gesammelt 18.09.2026.** Jedes Prinzip hier hat einen **Fall** hinter sich, in
dem eine Prüfung grün war und nichts gemessen hat — oder rot war und nichts
gefunden hatte.

> ⚠️ **Dieses Dokument gehört ins Übergabepaket und wird in Aufgabendokumenten
> VERWIESEN, nicht abgeschrieben.** Cloud-Sitzungen können es lesen.

> **Zu den Kürzeln:** `B4` und `C7` waren im Lauf der Arbeit schon in Gebrauch
> und behalten ihre Bedeutung. Alles andere ist hier zum ersten Mal beziffert.
> ⚠️ **Nichts wird umnummeriert** — ein Verweis aus einem alten Journalblock
> muss weiter treffen.

---

## A — Was eine Messung überhaupt ist

### A1 — Ein gescheiterter Aufruf und ein leeres Ergebnis sehen gleich aus

**Der Fall (TB-45):** `shared/test_kursdaten.py:438` fragte den Rückgabewert von
git nicht ab. Mit kaputter Referenz: **`rc=128`, und trotzdem „bestanden"** — mit
**28 grünen Prüfungen**, ohne dass eine einzige etwas gemessen hatte. Dieselbe
Verwechslung in `dashboard/test_portfolio_sicht.py:217`, dort sogar ausdrücklich
hingeschrieben (`returncode != 0 or not stdout.strip()`).

⚠️ **Die Unterscheidung, die dabei nicht verlorengehen darf:** Bei manchen
Prüfungen **ist** ein leeres Ergebnis der Nachweis. *„Keine Kursdatei verändert"
ist der Sollzustand — dort wäre „leer = Fehler" die falsche Verschärfung.*

⭐ **Die Prüffrage:** Ist ein leeres Ergebnis hier der **Nachweis** oder das
**Fehlen** eines Nachweises?

### A2 — „Konnte nicht messen" ist ein eigenes Ergebnis, nicht grün und nicht rot

**Der Fall (TB-46):** `shared/snapshot.py` hat deshalb **drei** Rückgabewerte:
**0** gezogen · **1** Befund · ⭐ **2 nicht prüfbar**. *Wer „nicht prüfbar" als
grün zählt, hat A1. Wer es als rot zählt, bekommt einen Alarm, an den er sich
gewöhnt (A4).*

### A3 — Ein Test, der ein Argument braucht, ist ungeprüft, nicht grün

**Der Fall (TB-45, Mac):** Drei Testdateien geben ohne Bot-Argument nur ihre
Nutzungszeile aus (`rc=1`) und werden von einem Basislauf **nie erreicht**:
`research/drawdown_reihenfolge/test_drawdown.py` ·
`research/fib_score_stufen/test_stufen.py` ·
`research/elliott_wave_params/test_params.py`.

⚠️ **Wer „alle Tests grün" schreibt, meint sie nicht.** Aus der Cloud war
**einer** sichtbar, der Mac zeigte **drei**. **Ungeprüfte gehören im Basislauf
in eine eigene Spalte.**

### A4 — Ein dauerhaft roter Test ist keine Wache

**Der Fall (T38.9):** `shared/test_kursdaten.py` prüfte eine **Auflage** („keine
`forward_test.py` verändert") statt einer **Eigenschaft**. Er wurde nach jeder
freigegebenen Änderung rot — und damit blind. **Die Lockerung auf
*„kein Handelsparameter verändert"* war richtig** (E4), weil sie den Prüfer
wieder beissen lässt (gegengeprobt: `TRADING_FEE_PCT: 0.1 → 0.2` wird gefunden).

**Dasselbe gilt für Meldungen:** *„223 von 223 Dateien veraltet"* täglich per
Telegram wird binnen einer Woche zur Tapete — **und dann fällt die echte nicht
mehr auf** (T38.12).

### A5 — Ein Werkzeug, das nicht mehr misst, sagt es

**Drei Fälle an einem Tag (T41.10):** `loaderlauf.py` lief auf dem Mac gar nicht ·
`pruefe_register.py` verglich nach dem Merge gegen einen leeren Diff und meldete
Erfolg · die TB-40-Vergleichstabelle zeigte auf einen historischen Stand.

⭐ **Gefunden wurde es nur durch einen Selbsttest, der prüfte, OB geprüft
wurde** — *„der Diff wurde tatsächlich ausgewertet"*.

### A6 — Eine Einzelmessung kann die ABWESENHEIT eines flackernden Fehlers nicht belegen

**Der Fall (TB-49, Mac-Lauf 18.09.2026):** `system/test_log_rotation.py` war in
TB-47 aus `BEKANNT_ROT` gestrichen worden, mit der Begründung *„auf BEIDEN
Rechnern grün, 117/117"* — je **eine** Messung pro Rechner.

**Zehn Einzelläufe auf dem Mac:**

| Lauf | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| | ⚠️ **116** | 117 | ⚠️ **116** | 117 | ⚠️ **116** | 117 | 117 | 117 | 117 | 117 |

**Immer `116 von 117`, immer eine zeitabhängige Probe zum Restfenster beim
Rotieren, ein bis zwei fehlende Zeilen von 238–512 — und die gefallene Probe
wechselt.** Rate **~30 %**.

> ⭐ ***„Die Streichung stützt sich auf je EINE Messung pro Rechner; bei ~30 %
> Flackerrate trifft eine Einzelmessung mit 70 % Wahrscheinlichkeit grün."***

⚠️ **Und der Befund stand längst im Backlog** (T38.10, 15.09.: *„flattert —
Rennbedingung zwischen Sichern und Leeren"*). **Eine dokumentierte Aussage wurde
mit einer Einzelmessung überstimmt, ohne nachzusehen, ob es dazu schon etwas
gibt.**

**Die Regel, zweiteilig:**

| | |
|---|---|
| ⭐ **Grün einmal ist kein Nachweis** | Wer einen Eintrag aus einer Rot-Liste streicht, braucht **mehrere** Läufe — bei einem Verdacht auf Zeitabhängigkeit zehn |
| ⚠️ **Vor dem Streichen im Backlog nachsehen** | *Eine geprüfte Aussage ungeprüft zu verwerfen ist derselbe Fehler wie eine Zahl ungeprüft zu übernehmen (**C1**), nur in die andere Richtung* |

**Und die richtige Formulierung für solche Fälle:** nicht „rot" und nicht „grün",
sondern ⭐ **„grün im Regelfall, zeitabhängig flackernd"** — mit der gemessenen
Rate dabei. *Ein flatternder Test untergräbt sonst die Aussagekraft jedes
Basislaufs, ohne dass jemand weiss, wie oft.*

### A7 — Eine nachgeholte Vorher-Messung

*Eine „Vorher"-Messung, die erst nach der Änderung gemacht wird, ist nur dann
eine Vorher-Messung, wenn der gemessene Zustand **inhaltsadressiert**
wiederherstellbar ist — etwa ein Git-Commit, der genau einen Baum bezeichnet
— und wenn die Rekonstruktion **ausdrücklich als solche benannt** wird.*

**Herkunft:** TB-55 (19.09.2026). Der „vorher"-Lauf des Registerprüfers war
übersprungen worden; die Sitzung hat den Stand `7e48e1f` als Worktree
ausgecheckt, dort gemessen und es offengelegt, statt die Messung als
gleichwertig zu behaupten.

⚠️ **Die Grenze:** Bei einem Zustand, der nicht aus dem Inhalt bestimmt ist —
Uhrzeit, Umgebung, laufende Prozesse, Netzlage — ist dasselbe Vorgehen
**wertlos**. Dann gilt: die Messung fehlt, und das ist zu berichten.

### A8 — Eine Selbstauskunft ist erst dann eine Wache, wenn ein anderer sie gegenprüfen kann

*Wo keine Gegenprüfung möglich ist, wird die Prüfung auf das verlagert, was nach
aussen sichtbar ist.*

**Der Fall (21.09.2026, Registerabschnitt 27):** Der Verfahrensprüfer führt nach
27.4 in jeder Antwort ein Leseprotokoll. ⚠️ **Niemand kann messen, was er
gelesen hat.** Er sagt es selbst, 21d: *„Das Leseprotokoll ist eine
Selbstauskunft. Ihr könnt nicht messen, was ich gelesen habe; ihr könnt nur
messen, ob meine Begründungen Zahlen enthalten, die ich nicht haben dürfte."*

⭐ **Die Verlagerung ist die ganze Regel:** geprüft wird nicht das Protokoll,
sondern die **Begründung** — das einzige Erzeugnis, das nach aussen sichtbar ist
und in dem eine unzulässige Grösse auftauchen müsste, wenn sie gewirkt hätte.

⚠️ **Warum das nicht unter `A4` fällt:** `A4` trifft einen Test, der dauerhaft
dieselbe Farbe zeigt und dadurch blind wird. Hier zeigt der Test **gar keine
Farbe** — es gibt keinen Prüfer, nur eine Aussage. **Eine andere Fehlerklasse,
und unter `A4` bliebe sie unsichtbar.**

⭐ **Die Prüffrage:** Gibt es ausser der Aussage des Geprüften irgendeine Spur,
an der ein Dritter sie widerlegen könnte? Wenn nein, ist es keine Wache — dann
gehört die Prüfung an die Stelle, wo eine Spur entsteht.

---

## B — Wie eine Probe sich selbst täuscht

### B1 — Eine Mutationsprobe muss beissen

**Die Bauform dieses Projekts:** Jede neue Prüfung wird **zusätzlich** in einer
Fassung **ohne** die Wache ausgeführt und muss dort **denselben Fehler
übersehen**. In `shared/test_snapshot.py` sind das dreizehn Proben, jede mit
ihrer Gegenprobe (Wache im Speicher entfernt, Modul neu ausgeführt).

⚠️ **Drei Proben waren im ersten Entwurf falsch gebaut** — 3a fand nur die
Grösse, nicht die Quersumme. **Benannt statt still korrigiert.**

### B2 — Der Test gegen blinde Wachen hat selbst eine blinde Stelle

**Der Fall (T43.8), von der Sitzung selbst gefunden:** *„Teil K besteht trotzdem,
weil dort pathlib schon geladen ist, bevor die Wache angeht. **Teil K sieht
diesen Fall also nicht.**"*

⇒ **Die fehlende Prüfung war wichtiger als der Patch.** Ohne sie fällt derselbe
Fall beim nächsten Umbau wieder durch.

### B3 — Ein Gegenbeweis gegen eine bewegliche Referenz prüft nichts

**Der Fall (T41.9):** `pruefe_register.py` hatte `origin/main` als
**Standardwert**. Ist der Zweig gemergt, ist der Diff leer — **die Wache gegen
gelöschte Registerzeilen war nach jedem Merge trivial grün.**

**Die Abhilfe im Projekt:** Referenz **festnageln**. In
`shared/test_leeres_symbol.py` und `shared/test_stille_ausfaelle.py` steht dafür
`BEZUGSCOMMIT = "97aea8878c9fae5e1f12d30e2ea0318dd20aadc5"` — und ist der Commit
nicht zu finden, **ist der Test rot mit dem Vermerk NICHT PRUEFBAR** (A2), nicht
grün.

### B4 — Eine Probe kann sich selbst blind machen — und sie kann sich selbst sehen

**Die erste Hälfte** war bekannt (B2).

⭐ **Die zweite kam am 18.09. dazu (TB-47, Mac):** Die Zählung überlebender
Enkelprozesse meldete **vier**. Das wäre der Gegenbeweis gewesen. Statt es
hinzunehmen hat die Sitzung nachgesehen — **die Zählung zählte sich selbst**: Das
Suchmuster stand in der eigenen Befehlszeile, also fand `ps` die eigene Shell.

| Gegenprobe | Ergebnis |
|---|---|
| nur Python-Prozesse | 1 |
| Zählung aus einer **Datei** heraus, eigener Prozess ausgeschlossen | 1 |
| ⭐ **Aufruf ohne Heredoc — das Muster steht nicht mehr in der Befehlszeile** | **0** |

> ⚠️ **Eine Probe, die sich selbst sieht, meldet einen Fehler, den es nicht
> gibt.** Genau so gefährlich wie einer, den sie nicht sieht — nur teurer, weil
> jemand ihn sucht.

### B5 — Am Syntaxbaum messen, nicht per Textsuche

**Der Fall (TB-46):** Zwei `forward_test.py` **nennen** `data/` in einer
Protokollzeile. Eine Textsuche hätte gemeldet, der Datenordner-Umbau müsse die
Bot-Dateien anfassen — **genau die Dateien, die er nicht anfassen darf.**

⭐ **Über den Syntaxbaum gemessen: null Bot-Dateien bauen einen Pfad.** Der Umbau
kommt ohne sie aus.

**Dieselbe Technik in TB-37:** Die Signatur
`fetch_historical_data(symbol, interval, lookback)` wurde aus dem Syntaxbaum der
**neun Aufrufer** erschlossen, ohne die Datei zu sehen.

### B6 — Ein Import ist keine Leseoperation

**Der Fall (TB-40):** Neun identisch benannte `equity_simulation.py` kollidieren
in `sys.modules`. Die Auflösung war **nicht** eine Namensregel, sondern
**ein Prozess je Bot** — *nicht weil jemand aufpasst, sondern weil jeder Prozess
seinen eigenen `sys.modules` hat.*

**Und Importe haben Nebenwirkungen:** Der Import von
`strategies/elliott_wave/multi_symbol_optimise.py` **braucht Netz** — er holt
eine Konstante aus einem Modul, das auf Modulebene `Client()` anlegt, und
`python-binance` pingt im Konstruktor (T40.6). `shared/paths.py:18` **legt beim
Import `data/` an** (T46.8).

---

## C — Zahlen und ihre Herkunft

### C1 — Jede Zahl wird an ihrer Quelle nachgerechnet, nicht aus einem Bericht übernommen

**Die Fehlerliste im Journal (Block AX) zählt zwölf Fälle, acht aus dieser
Ursache.** Darunter:

| Behauptung | Wirklichkeit |
|---|---|
| „fünf Werte von `MIN_HISTORY_*`" | **vier** — Gruppen gezählt statt Werte (T41.1) |
| „Teilkerze fünf Minuten alt" | **2–3 Stunden** — falscher Cron-Eintrag gelesen (T38.4) |
| „sechs Schreibweisen scheitern auf 3.9" | der Mac fand **acht von vierzehn** (T45.12) |
| „`shared/test_kursdaten.py` ist bekannt rot" | **grün, 82/82** — Liste unbesehen übernommen (T42.6) |
| „die letzte Kerze ist bei allen 223 Dateien sauber" | **175 tragen `kein_zeuge`** — dort ist nichts belegbar (18.09.) |
| „die erste Selektionsfalte beginnt 2022" | der Faltenplan sagt **2019** (TB-48) |
| „2022 ist die früheste **Krypto**-Falte" | **alle neun Bots beginnen 2019**; die 2022 stammt aus einem überholten Faltenplan (TB-49) |
| „`system/test_log_rotation.py` ist auf beiden Rechnern grün" | ⚠️ **3 von 10 Läufen rot** — eine Einzelmessung je Rechner belegte nichts (TB-49, siehe **A6**) |

⭐ **Die Regel:** Fundstellen nur nennen, wenn sie **vorliegen**. Sonst steht
ausdrücklich *„aus dem Gedächtnis"* dabei.

### C2 — Zwei Parser auf zwei Dateien statt einmal abtippen

**Der Fall (TB-41):** Die Symbolzahlen wurden von **zwei getrennten Parsern**
maschinell verglichen. ⭐ **Genau deshalb ist C1-Fall „fünf statt vier"
aufgefallen.**

### C3 — „Kein Befund" ist nicht „geprüft"

**Der Fall (TB-47):** **175 von 223** Kursdateien tragen `kein_zeuge` — es gibt
keine feinere Datei zum Vergleich, also ist die Abdeckung der Randkerzen
**nicht belegbar**. Die Prüfung schweigt dort; sie bestätigt nichts.

⚠️ **Was dort trägt, ist eine andere Zusicherung** (`shared/abrufschutz.py`,
TB-35) — **eine andere, und sie gehört benannt.**

### C4 — Eine Prüfung, die nicht sagt, gegen WAS sie prüft, ist eine Falle

**Der Fall (T41.2 / T43.3):** Das TB-40-Werkzeug las weiter die **historische**
Tabelle in Registerabschnitt 15.5 und hätte bereits korrigierte Zahlen erneut
„korrigiert". **Behoben, indem das Werkzeug den benannten Abschnitt liest, ihn in
Ausgabe und Bericht nennt und gegen die alte Tabelle warnt.**

⭐ **Der zweiseitige Nachweis, der dazugehört:** gegen 16.1.1 **null**
Abweichungen, gegen 15.5 **acht** — bei zeichengleichen Messwerten. *Damit ist
belegt, dass das Werkzeug die Tabelle wirklich wechselt und nicht bloss
schweigt.*

### C5 — Grün in der Cloud heisst strukturell nicht grün auf dem Mac

**Mac 3.9.6, Cloud 3.11+.** `pathlib` hat sich zwischen beiden an genau der
Stelle geändert, an der der Schreibschutz ansetzt (T43.9). ⚠️ **Und die
Cloud-Umgebung ist nicht eine Umgebung, sondern eine je Sitzung** — Pakete
liessen sich in TB-43 nachinstallieren, in TB-39 nicht (T45.6).

⭐ **Die Regel „erst Mac-Lauf, dann Merge" hat sich am ersten Tag bezahlt
gemacht** (T43.10): Ohne sie läge ein Werkzeug in `main`, das auf dem Mac bei
zwei von neun Bots abbricht — ausgerechnet das Werkzeug, das die Registerzahlen
misst.

### C6 — Eine abgeleitete Zahl auf einer gesetzten ist besser als zwei gesetzte

**Der Fall (E2):** Die Mindestzahl Signale in Registertext 7 ist **nicht**
gewählt, sondern abgeleitet: `n ≥ 1 / (1 − Schwelle)`. Nachgerechnet: **18/19 =
94,7 % reisst die 95 %, 19/20 = 95,0 % nicht.** ⚠️ **Die 95 % selbst bleiben
willkürlich** — die 20 sind nur **ihnen gegenüber** abgeleitet.

**Dieselbe Bauform:** die Rasterobergrenze `floor(1 / ALLOCATION_PCT)` (V4) und
`DD_Toleranz` als Median der Benchmark-Drawdowns je Bot (V1b).

### C7 — Zwei Zahlen, zwei Fragen

**Der Fall (TB-47/TB-48):** `datenstand_hash` und `snapshot_hash` sind
**verschieden und beide richtig** — der eine bezeichnet den Kursdatenteil, der
andere den ganzen Snapshot. Ebenso: **182 Module erreichen `data/`**, **101**
zählen eine engere Frage — **beide Zahlen sind richtig** (TB-46).

⚠️ **Und der offene Fall:** **2019** ist mutmasslich die früheste Falte über
alle neun Bots, **2022** die früheste **Krypto**-Falte. Solange das nicht
gemessen ist, ist eine der beiden Zahlen falsch.

⭐ **Die Prüffrage:** Widersprechen sich zwei Zahlen — oder beantworten sie
verschiedene Fragen? **Und steht dabei, welche?**

---

## D — Ausfallformen

### D1 — Ein stiller Ausfall ist schlimmer als ein Abbruch

**Der Satz, der im Projekt dafür steht (F12):**
⭐ ***„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."***

**Der Fall (T40.5):** Drei Bots sortierten **völlig lautlos** aus — bei zu kurzer
Historie **und** bei fehlender Kursdatei keine einzige Zeile. Der Befund, der
den ganzen Trockenlauf auslöste, war nur sichtbar, weil **einer von neun** Bots
ihn meldet.

⚠️ **Offen (T45.4): sechs der neun überspringen ein leeres Symbol weiterhin
still.**

### D2 — Ein Abbruch fällt auf, ein stilles Schreiben nicht

**Der Fall (T44.2):** `pathlib` **vor** der Wache importiert — auf 3.9 legte
`Path.touch()` die Datei **wirklich** an, auf 3.10 schrieb `Path.write_text()`
**wirklich**. `pathlib` **nach** der Wache: alles bricht ab, auch lesend.

⚠️ **Und die „vor"-Reihenfolge ist genau die, in der der echte Trockenlauf
läuft.** Der Schreibschutz war auf dem Mac nie vollständig — weder vor noch nach
TB-43.

### D3 — Eine Funktion muss heissen, was sie tut

**Der Fall (T44.10):** `_ist_geraet()` liefert `not S_ISREG` — also **True für
jedes existierende Verzeichnis**. Heute kein Loch (gemessen). ⚠️ **Käme eine
Operation dazu, die auf ein Verzeichnis wirken kann** — `chmod`, `utime`, ein
Kopiervorgang hinein — **würde der „Gerät"-Zweig sie durchwinken.**

**Derselbe Verdacht bei einer Konstante:** `reg.KURSDATEN_DIR_VERBOTEN` ist der
**Rückfallwert**, auf den sich jemand stützen könnte (T46.5).

### D4 — Stabil aus Zufall der Umstände ist nicht stabil aus Entwurf

**Der Fall (T45.8):** `os.fstat` ist auf allen fünf geprüften Python-Fassungen
ein `builtin_function_or_method` und steht in keinem Klassenrumpf — **heute
harmlos**. ⚠️ **Genau die Bedingung, an der es hängt, hat sich bei
`pathlib._NormalAccessor` zwischen zwei Fassungen geändert.**

**Und ein Beispiel dafür, dass es gutgeht:** `t3_supertrend` überlebt einen
leeren Kursrahmen **nur, weil der Aufruf zufällig im `try` der Ladeschleife
steht** (T45.3) — und die Meldung nennt dann das Symptom statt der Ursache.

### D5 — Eine Ausnahme wird als REGEL umgesetzt, nicht als Liste

**Der Fall (TB-49):** Die 36 `rand_erste`-Befunde sind registriert zugelassen.
Eine **Liste** dieser 36 Dateien veraltet — **jedes neu gelistete Symbol bringt
denselben Befund mit**, und eine ungepflegte Liste blockiert entweder zu Unrecht
oder lässt zu Unrecht durch.

⭐ **Die Regel prüft drei Bedingungen** (Art · **erste** Kerze · nachweislich
Aggregat der feineren Kerzen) und **deckt damit den künftigen Fall mit ab**.
⚠️ **Und `rand_letzte` fällt nie darunter.**

**Dazu gehört:** ⚠️ **keine Übergehen-Flagge.** Die Prüfung schlägt weiter an;
was erlaubt ist, entscheidet ein **Registereintrag**, den ein Prüfer lesen kann —
und das **Manifest führt auf, was bei der Erzeugung zugelassen wurde.**

### D6 — Nichts wird gelöscht oder überschrieben, ohne zu warnen

**Der Fall (T37.1), nachgemessen statt vermutet:** `git pull` **überschreibt eine
gitignorierte Datei kommentarlos**, wenn ein Commit eine Datei am selben Pfad
hinzufügt. ⇒ **Sicherung VOR jeder git-Operation.**

**Und der Grund, warum das hier mehr wiegt als anderswo:** Die neun `*.db` sind
gitignoriert, existieren **nur auf dem MacBook**, sind seit Verfahren B die
**einzige** OOS-Evidenz des Projekts und **nicht neu berechenbar** (T37.2).
