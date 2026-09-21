# TB-80 Bedingung (i) auf `asof` — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel fuer Claude Code: `TB-80 Bedingung i auf asof`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, Base `main`. Direkt auf `main`, kein Zweig,
kein PR.

⭐ **Was diese Aufgabe tut, in einem Satz:** Der Faltenplan rechnet Bedingung (i)
heute gegen die **Datenuhr**; Registerabschnitt 26.2 sagt seit gestern Abend,
dass der Horizont ein **absolutes Datum je Bot** ist. Diese Aufgabe stellt den
Code auf das Register um und misst, was sich dadurch ändert.

---

## ⭐⭐ Die Freigabe, und was sie abdeckt

> **Betreiberfreigabe, 21.09.2026, 21:47 Ortszeit:**
> `research/vorregistrierung/faltenplan.py` darf für die Umstellung von
> Bedingung (i) auf `asof` geändert werden.

⚠️ **Die Freigabe sagt, dass geändert werden durfte; sie sagt nicht, was
geändert wurde.** Der Diff dieser Datei wird vor dem Abschluss angesehen.

⛔ **Was sie NICHT abdeckt — keine einzige Zeile:**

| | |
|---|---|
| ⛔ | `research/vorregistrierung/ergebnisse/faltenplan.json` (`0e54ac5c…`) — **Sperrliste Punkt 2**, bleibt byteweise unverändert |
| ⛔ | `ergebnisse/benchmark_drawdowns.json` (`a163c498…`) · `ergebnisse/benchmark_drawdowns_vt.json` (`4549395f…`) |
| ⛔ | `auswertung.py` (eingefroren, Abschnitt 0 Z. 31) — **auch nicht der Docstring** |
| ⛔ | die vier `strategies/*/multi_symbol_optimise.py` — **Sperrliste**, und sie sind **TB-30b** |
| ⛔ | `registerdaten.py` · `shared/` · `strategies/` · `snapshots/` |
| ⛔ | `ergebnisse/faltenplan_tb72.json` — der Plan von TB-72 bleibt, wie er ist |

⭐ **Neue Dateien sind erlaubt und erwünscht** — der neue Plan wird **daneben**
gelegt, nichts wird überschrieben. *Ein Verbot nennt, wovor es schützt: hier
davor, dass eine vorhandene registrierte Messung ihren Wert verliert.*

---

## Was gilt — der Registertext, gegen den du prüfst

**Registerabschnitt 26.2, zeichengleich aus dem Register:**

> ⭐ **(i) „im registrierten Datenhorizont des Bots"** — Der Horizont ist ein
> absolutes Datum je Bot (`asof` minus `RECENT_YEARS_ONLY`), **nicht je
> Symbol**.

**Registerabschnitt 28.4 — die vier Daten, die daraus folgen:**

| Bot | Markt | Horizontbeginn |
|---|---|---|
| `elliott_wave` · `t3_supertrend` · `rsi2_crypto` · `turtle_soup_crypto` · `volatility_breakout_crypto` | krypto | **kein Horizont** (26.2) |
| `elliott_wave_stocks` · `rsi2_mean_reversion` · `turtle_soup_stocks` · `volatility_breakout` | aktien | **2016-09-19** |

⚠️ **Lies beide Stellen selbst im Register nach**, bevor du anfängst, und nenne
deine Fundstellen. *`C1`: jede Zahl wird an ihrer Quelle nachgerechnet, nicht
aus einem Auftrag übernommen — auch nicht aus diesem.*

### ⭐⭐ Woher der Code das Datum nimmt — und woher NICHT

⚠️⚠️ **`RECENT_YEARS_ONLY = 10` steht in den vier `multi_symbol_optimise.py`.
Die stehen auf der Sperrliste, und eine Kopie der Konstante in den Faltenplan
wäre genau der Fehler aus `T56b.6`** (*Konstantenkopien; der Kommentar in
`faltenplan_neun.py:119` verweist auf eine Konstante mit 0 Treffern im
Quelltext*).

⇒ ⭐ **Der Plan nimmt den Horizontbeginn als absolutes Datum**, so wie 28.4 ihn
führt — **nicht** `asof` und `RECENT_YEARS_ONLY` getrennt, **nicht** aus den
Bot-Dateien gelesen, **nicht** gerechnet. *Eine Quelle, keine Kopie.*

⚠️ **Wo das Datum im Code steht, ist offen und Gegenstand deiner
Entscheidungsvorlage (Schritt 5)** — Register 26.6 führt *„`RECENT_YEARS_ONLY`
als registrierte Grösse (`registerdaten.py`) statt als Codekonstante"* als
**Entscheidungsvorlage, nicht vollzogen**, und `registerdaten.py` ist dir
verboten. **Für diesen Lauf genügt ein benanntes Literal im Faltenplan mit der
Registerfundstelle im Kommentar.** Es ist ein Zwischenstand, und er wird als
solcher benannt.

---

## Schritt 0 — Sichern und den Ausgangsstand messen

1. `git status --short`, committe, was im Arbeitsbaum liegt.
2. **Messe und notiere als Ausgangsstand:**
   - `shasum -a 256` der drei Sperrlisten-Dateien (voller Pfad, nie der blosse
     Name — ⚠️ **es gibt sechs Dateien `faltenplan*.json` im Repo**)
   - `erste_falte_4a` und `erste_falte` je Bot **aus dem heutigen Code**,
     gerechnet, nicht aus `faltenplan_tb72.json` gelesen
   - den Wert, den `fn.fensteranker(markt)` je Markt heute liefert
3. Beleg nach `docs/belege/TB-80/schritt0_ausgangsstand.txt`.

**Commit:** `TB-80 Schritt 0: Ausgangsstand gemessen`. **Pushen.**

⚠️ **Das ist eine echte Vorher-Messung, keine nachgeholte** (`A7`) — sie läuft,
bevor eine Zeile geändert wird.

---

## Schritt 1 — Die Umstellung

**Was gelten muss:** `erste_falte_4a(bot)` rechnet Bedingung (i) gegen den
**Horizontbeginn je Bot** aus 28.4, nicht gegen `fn.fensteranker(markt)`.

⛔ **Der Auftrag schreibt dir den Patch NICHT vor.** *Grund, gemessen: In TB-44
hat ein vorgeschriebener Patch auf der Fassung gestimmt, die der Verfasser vor
sich hatte, und auf der nächsten die Signatur gebrochen (`T44.1`).* Du siehst
den Code; ich sehe ihn nur lesend.

**Was der Auftrag vorgibt:**

| | |
|---|---|
| ⭐ | **Die Krypto-Bots haben keinen Horizont** (26.2). Für sie darf sich **nichts** ändern — das ist ein Nachweis, kein Nebenbefund |
| ⭐ | **Ein Literal je Markt mit Registerfundstelle im Kommentar**, kein gerechnetes `asof − Konstante`, keine Kopie aus den Bot-Dateien |
| ⚠️ | **Bedingung (ii) bleibt unberührt** — der Trockenlauf nach 3b (b) über `erste_falte_trockenlauf.erste_falte_nach_3b` rechnet weiter, wie er rechnet |
| ⚠️ | **Die Konjunktion bleibt die Konjunktion** (25.3). Du änderst, woraus (i) seinen Beginn nimmt — **nicht**, wie (i) und (ii) verknüpft sind |
| ⭐ | **`fensteranker` wird nicht entfernt.** Andere Stellen benutzen ihn; miss, welche, und melde sie. *Eine Funktion zu löschen, weil ein Aufrufer sie nicht mehr braucht, ist eine andere Aufgabe* |

**Commit:** `TB-80 Schritt 1: Bedingung (i) rechnet gegen den Horizontbeginn aus Register 28.4`. **Pushen.**

---

## Schritt 2 — Die Wirkung messen, berichten, nicht bewerten

**Rechne den Plan neu und lege ihn DANEBEN:**
`research/vorregistrierung/ergebnisse/faltenplan_tb80.json`.

⛔ **`faltenplan.json` und `faltenplan_tb72.json` bleiben byteweise unverändert.**

**Der Vergleich, je Bot, in einer Tabelle:**

| Bot | `erste_falte_4a` vorher | nachher | `erste_falte` vorher | nachher | Zahl der Selektionsfalten vorher → nachher |
|---|---|---|---|---|---|

⚠️⚠️ **Und der Satz, der über der Tabelle steht, bevor du sie liest:**

> ⭐⭐ **Die Regel stand vor der Messung.** Registerabschnitt 26.2 ist am
> 21.09.2026, 19:19 Ortszeit eingetragen worden; diese Messung läuft danach.
> **Was herauskommt, ist keine Wahl** — Bauart 24.3.

⛔ **Keine Bewertung, keine Empfehlung, keine Abwägung.** Nicht *„günstig"*,
nicht *„kostet eine Falte"* im Sinn von schlecht. **Die Zahl steht da, und sie
steht allein.** *Register 24.3, angewandt auf diesen Fall.*

⛔ **Und ausdrücklich NICHT messen:** wie sich die Änderung auf irgendeine
Kennzahl eines Parametersatzes auswirkt. **Das fiele unter 27.1** und ist vor
dem signierten Tag verboten — auch für uns, nicht nur für den
Verfahrensprüfer.

**Commit:** `TB-80 Schritt 2: neuer Plan daneben, Wirkung gemessen`. **Pushen.**

---

## Schritt 3 — Die Mutationsprobe

⭐ **`B1`: eine Probe, die nichts verwerfen kann, ist keine Probe.**

**Setze die Datenuhr künstlich wieder ein** (in einer Wegwerf-Kopie oder im
Speicher, **nicht committet**) und weise nach, dass der Plan dann **den alten
Stand** liefert — Bot für Bot. Beisst die Probe nicht, ist die Umstellung nicht
belegt, sondern nur behauptet.

⚠️ **Zusätzlich die Gegenrichtung:** Verschiebe den Horizontbeginn testweise um
ein Jahr nach hinten und weise nach, dass sich mindestens eine erste Falte
bewegt. *Eine Probe, die in beide Richtungen stumm bleibt, misst nicht die
Grösse, die sie zu messen glaubt.*

**Commit:** `TB-80 Schritt 3: Mutationsprobe in beide Richtungen`. **Pushen.**

---

## Schritt 4 — Der Test

Erweitere `research/faltenplan_neun/test_erste_falte_trockenlauf.py` oder lege
einen eigenen Test daneben — **deine Wahl, begründet**:

| | zu prüfen |
|---|---|
| 1 | `erste_falte_4a` je Aktien-Bot rechnet gegen **2016-09-19**, nicht gegen die Datenuhr |
| 2 | Die fünf Krypto-Bots sind **unverändert** gegenüber dem Ausgangsstand aus Schritt 0 |
| 3 | Die Konjunktion gilt weiter: `erste_falte ≥ erste_falte_4a` bei allen neun |
| 4 | ⭐ **Das Literal stimmt mit dem Register überein** — der Test liest die Zahl aus dem Registertext (28.4) und vergleicht. *Sonst ist es eine Konstante, die niemand gegenprüft* |

⚠️ **Der Test läuft auf dem Mac, `trading-env/bin/python3`.** Nenne die Umgebung
im Bericht — *eine Messung nennt die Umgebung, in der sie lief, nicht die, in
der sie hätte laufen sollen.*

**Commit:** `TB-80 Schritt 4: Test`. **Pushen.**

---

## Schritt 5 — Registerabschnitt 32 und die Entscheidungsvorlage

⚠️ **Das Register ist append-only.** Neuer Abschnitt **32** ans Ende, nichts
weiter oben ändern. Vorher prüfen: `grep -cE "^## 32\." docs/VORREGISTRIERUNG_neuselektion.md`
muss **0** sein.

**Der Abschnitt trägt:**

| | |
|---|---|
| **32.1** | Der Befund — Bedingung (i) rechnete gegen die Datenuhr, 26.2 verlangt das absolute Datum. Mit den Fundstellen, die **du** gemessen hast |
| **32.2** | Tatsachennotiz: die Wirkung je Bot, als Tabelle. ⛔ **Ohne Bewertung** |
| **32.3** | Tatsachennotiz: der neue Plan `faltenplan_tb80.json` mit SHA-256; `faltenplan.json` und `faltenplan_tb72.json` byteweise unverändert, mit Hashes |
| **32.4** | Die Mutationsprobe und ihr Ergebnis in beide Richtungen |
| **32.5** | ⭐ **Entscheidungsvorlage, nicht vollzogen:** wo der Horizontbeginn dauerhaft leben soll. Heute ein Literal im Faltenplan (Zwischenstand). Möglichkeiten mit ihrem Preis: `registerdaten.py` als registrierte Grösse (Registeränderung, Betreiber) · aus dem Registertext gelesen (ein Parser auf Fliesstext) · Literal mit Test gegen das Register (heutiger Stand). ⛔ **Keine Empfehlung nach Aufwand** |
| **32.6** | Was ausdrücklich nicht getan wurde: kein Bot-Code, keine Sperrlisten-Datei, kein `registerdaten.py`, kein Tag, kein Lauf |

**Commit:** `TB-80 Schritt 5: Registerabschnitt 32`. **Pushen.**

---

## Schritt 6 — Abschlussprüfung und Abgabe

| | zu prüfen | Soll |
|---|---|---|
| 1 | `git diff --numstat` je Datei über alle Commits | zweite Spalte **`0`** überall **ausser** `faltenplan.py` — dort **jede entfernte Zeile einzeln der Änderung zugeordnet**, die sie verursacht hat |
| 2 | ⭐ **Der Diff von `faltenplan.py` vollständig im Ergebnisdokument** | die Freigabe sagt nicht, was geändert wurde |
| 3 | Drei Sperrlisten-Hashes | `a163c498…` · `0e54ac5c…` · `4549395f…` **unverändert**, voller Pfad |
| 4 | `faltenplan_tb72.json` | **unverändert**, SHA-256 gegen Schritt 0 |
| 5 | Nichts ausserhalb `docs/`, `research/vorregistrierung/faltenplan.py`, `research/faltenplan_neun/` (Test) und den neuen Ergebnisdateien | |
| 6 | Registerabschnitte | `26`…`32`, jeder genau einmal als `##`-Überschrift |
| 7 | `git status --porcelain` **nach dem letzten Commit** | nur `.claude/settings.local.json` |
| 8 | ⚠️ **Zweite, unabhängig geschriebene Zählung** für Prüfung 6 | |

**Ergebnisdokument** `docs/ERGEBNIS_TB-80_bedingung_i_auf_asof.md`, mit dem
vollständigen Diff, allen Nachweisen, **jeder Abweichung von diesem Auftrag mit
Begründung** und **„In einfacher Sprache"** am Ende.

⚠️ **Jede Rückfrage an den Betreiber und seine Antwort wörtlich hinein**, nicht
als Zusammenfassung.

**Journalblock** direkt ans Ende von `docs/projektfuehrung/JOURNAL.md`, vor
`## Wiederkehrende Lehren`; **Buchstabe gemessen** (letzter ist `CG`),
Quellenzeile auf das Ergebnisdokument.

---

## Abbruchkriterien

⛔ **Brich ab und melde, wenn:**

1. Ein Sperrlisten-Hash sich ändert.
2. `faltenplan_tb72.json` sich ändert.
3. Die Mutationsprobe in **einer** der beiden Richtungen nicht beisst.
4. Ein Krypto-Bot sich zwischen Schritt 0 und Schritt 2 verändert —
   ⚠️ **sie haben keinen Horizont; ändert sich dort etwas, trifft die Umstellung
   mehr als (i).**
5. Der Horizontbeginn, den du im Register liest, nicht `2016-09-19` lautet.
6. `grep -cE "^## 32\."` vor deinem Eintrag nicht `0` ist.

⭐ **Das Abbruchkriterium gilt für Fehlschläge, die den Gegenstand der Aufgabe
betreffen** (`T44.11`). Ein roter Test, der mit dieser Änderung nichts zu tun
hat, wird **gemeldet**, nicht zum Abbruchgrund.

---

## In einfacher Sprache

**Was hier gemacht wird:** Im Regelwerk steht seit gestern Abend, ab welchem Tag
jeder Bot rechnen darf — für die vier Aktien-Bots ist das der 19. September
2016. Das Programm, das die Auswertungsjahre bestimmt, benutzt dafür aber noch
ein anderes Datum: den letzten Tag, für den Kursdaten vorliegen, zehn Jahre
zurück. Das sind achtzehn Tage Unterschied.

**Warum das etwas ausmachen kann:** Ein Bot darf ein Jahr nur auswerten, wenn
seine Indikatoren am 1. Januar schon genug Vorlauf haben. Achtzehn Tage weniger
Vorlauf können bedeuten, dass ein Bot sein erstes Auswertungsjahr verliert.

**Warum das trotzdem in Ordnung ist:** Die Regel stand im Regelwerk, **bevor**
jemand gemessen hat, was sie kostet. Genau darum geht es bei diesem Projekt —
eine Regel, die vorher feststeht, kann nicht nachträglich so gewählt worden
sein, dass das Ergebnis besser aussieht.

**Was ausdrücklich nicht gemacht wird:** Niemand rechnet aus, wie sich die
Änderung auf die Güte einzelner Einstellungen auswirkt. Das wäre genau die Zahl,
die vor dem Versiegeln niemand kennen darf.
