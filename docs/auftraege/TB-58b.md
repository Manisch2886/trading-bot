# TB-58b Die Registereinträge zu Codeherkunft und Lock

⚠️ **[Mac-pflichtig]** — Push auf `main`.
*(Gemessen: der Registerprüfer braucht `trading-env`; das Schreiben allein ginge
ortsunabhängig, das Prüfen nicht.)*

**Sitzungstitel: `TB-58b Registereinträge Codeherkunft und Lock`**
**Modell: Opus 5, Aufwand hoch.**

Repo `Manisch2886/trading-bot`, Arbeitsordner `~/trading-bot`, Zweig **`main`**.
⚠️ **Kein eigener Zweig, kein Pull Request.**

**Formuliert 19.09.2026, nach Fables Antwort zu Schicht 3.**

---

## ⚠️⚠️ Schritt −1 — Ortsprüfung und Vorbedingung

| Prüfung | Soll |
|---|---|
| `uname -s` | **`Darwin`** |
| `test -x trading-env/bin/python3` | vorhanden, **3.9.x** |
| Arbeitsordner, Zweig | `~/trading-bot`, **`main`**, aktuell mit `origin` |
| `git status --short` | **0 Zeilen** |
| ⚠️⚠️ **TB-58 ist durch** | **`requirements.lock` liegt versioniert im Projektwurzelverzeichnis** und `shared/paths.py` trägt die Startprüfungen |

⚠️⚠️ **Fehlt `requirements.lock` oder die Startprüfungen: ABBRUCH.**
*Ein Registereintrag über etwas, das es nicht gibt, ist schlimmer als kein
Eintrag.*

---

## Worum es geht

**TB-58 hat zwei Lücken geschlossen, die Fable am 19.09. benannt hat** — die
**Codeherkunft** neben der Datenherkunft, und den **Lock** als dritte Achse der
Laufidentität. ⚠️ **TB-58 hat ausdrücklich keinen Registertext angefasst. Dies
ist der Nachtrag.**

⭐ **Art der Änderung, eingeordnet nach F17:** Der Lock-Eintrag ist eine
**Tatsachennotiz** (eine Messung wird festgehalten, wie Abschnitt 18). Die
Ergänzung zur Codeherkunft ist eine **Entscheidung** — sie trifft etwas, das
im Register offen war. ⚠️ **Ihre Begründung nennt kein Ergebnis**, und sie ist
vor dem Tag zulässig.

---

## Die harten Regeln

1. ⚠️⚠️ **Es wird NUR HINZUGEFÜGT.** Kein bestehender Registertext wird
   umgeschrieben.
2. ⚠️ **`data/`, `snapshots/`, jede `*.db`, die Sperrliste, `shared/*`:
   unberührt.** Diese Aufgabe fasst **eine** Datei an:
   `docs/VORREGISTRIERUNG_neuselektion.md`.
3. ⚠️ **Keine Zahl abschreiben** — der Lock-Hash wird **aus der Datei
   gerechnet**, nicht aus einem Bericht übernommen.
4. ⚠️⚠️ **Keine Abschnittsnummer raten** (K2i) — die höchste vergebene wird
   gemessen, und im Bericht steht, welche es wurde und warum.
5. **Kein Netzabruf ausser `fetch`/`push`, keine Order, kein Bot-Lauf.**
6. **Secrets:** nie `cat` auf Konfigurationsdateien.
7. ⭐ **Fallen Wortlaut und Zweck auseinander und der Betreiber ist erreichbar:
   fragen, nicht entscheiden.**

**Interpreter:** `trading-env/bin/python3`. **Prüfprinzipien:** **A1**, **A2**,
**A7**, **D5**, **D6**.

---

## Schritt 0 — Sichern und messen

| | |
|---|---|
| ⭐ **Jede `*.db` ausserhalb `trading-env/`** | Quersummen + Kopie, gezählt |
| **Datenstand vorher** | `d9449faf…`, **223** |
| ⭐ **Snapshot `--pruefen`** | `UNVERAENDERT`. ⚠️ Sonst ABBRUCH |
| ⭐ **Registerprüfer VORHER** | KEIN BEFUND, **vor** jeder Änderung (A7) |
| ⭐ **`requirements.lock`** | **SHA-256 selbst rechnen**, Paketzahl zählen, `pandas`-Fassung lesen |

---

## Schritt 1 — Wohin, gemessen

1. **Höchste vergebene Abschnittsnummer** in
   `docs/VORREGISTRIERUNG_neuselektion.md` — Muster auf die
   Überschriftenzeilen. *(Nach TB-55b war es 18; **das ist zur Gegenprüfung
   genannt, nicht zum Abschreiben.**)*
2. ⚠️ **Prüfen, ob es bereits einen Abschnitt zu Codeherkunft oder Lock gibt**
   — mehrere kennzeichnende Zeichenfolgen. ⭐ **Findet sich einer, der
   dasselbe festhält: melden, nicht verdoppeln.**
3. ⭐ **Die Form von Abschnitt 18 übernehmen** — er ist die jüngste
   Tatsachennotiz und die beste Vorlage.

---

## Schritt 2 — Die beiden Einträge

⭐ **Inhaltlich das Folgende; die Form richtet sich nach Abschnitt 18.**

### (A) Ergänzung zur Codeherkunft — Fables Wortlaut, geprüft

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

### (B) Tatsachennotiz zum Lock

> **Tatsachennotiz zu Registertext 5f — der Lock. Datum: 19.09.2026.**
>
> Die Umgebung, in der der Selektionslauf rechnet, ist in
> **`requirements.lock`** im Projektwurzelverzeichnis festgehalten, versioniert
> unter Commit ⟨gemessen⟩.
>
> | | |
> |---|---|
> | SHA-256 der Datei | ⟨**selbst gerechnet**⟩ |
> | Pakete | ⟨gezählt⟩, sämtlich mit `==` |
> | Interpreter | ⟨aus dem Kopf der Datei⟩ |
> | Plattform | ⟨aus dem Kopf der Datei⟩ |
>
> Der Lauf prüft bei Start Interpreter, Paketfassungen und Plattform gegen
> diese Datei und bricht bei Abweichung ab (**Rückgabewert 2**).
>
> ⚠️ **`requirements.txt` ist kein Lock** — es nennt, was installierbar ist;
> `requirements.lock` nennt, was gelaufen ist.

⚠️ **Die Werte in ⟨⟩ misst die Sitzung selbst.** Dieses Dokument nennt sie
nicht.

---

## Schritt 3 — Einchecken

1. `git status --short` — **nur** `docs/VORREGISTRIERUNG_neuselektion.md`.
2. ⚠️ **`git diff --numstat` — entfernte Zeilen: 0.** **Weicht es ab: ABBRUCH,
   nicht committen, melden.**
3. `add` + `commit` + `push` in einem Zug, `git status` **danach**.

---

## Zum Schluss

1. **Datenstand am Ende** — `d9449faf…`/223.
2. **Jede gesicherte `*.db` byteweise identisch**, mit Zahl.
3. **Snapshot `--pruefen`** — `UNVERAENDERT`.
4. ⭐ **Registerprüfer nachher** — KEIN BEFUND.
5. ⭐⭐ **Die Probe, die diesen Eintrag erst wahr macht:** Nach dem Commit einen
   Lauf unter dem Selektionsmodus mit **absichtlich abweichendem Lock** starten
   — ⚠️ **er muss mit rc 2 abbrechen.** *Ein Registertext, der etwas behauptet,
   was der Code nicht tut, ist schlimmer als keiner.*
6. `docs/ERGEBNIS_TB-58b_registereintraege.md`, endet mit **„In einfacher
   Sprache"**.
7. ⭐ **KEINE ZIP.** Stattdessen **mitcommitten**: die Belege nach
   `docs/belege/TB-58b/` und eine Kopie dieses Auftrags nach
   `docs/auftraege/TB-58b.md`.
8. ⚠️ **Nachzuholen, was TB-58 nicht getan hat:** die Belege jener Sitzung nach
   `docs/belege/TB-58/` und ihr Auftrag nach `docs/auftraege/TB-58.md` —
   ⭐ **der Auftrag liegt unverändert in `logs/auftraege/TB-58.md`.**
   *Begründung: ein Beleg in `~/Downloads` ist kein Beleg; er existiert auf
   einem Rechner und in keiner Version (T54.5).*

**Der Bericht beantwortet ausdrücklich:**

- ⭐ **Welche Abschnittsnummern wurden vergeben, und wie gemessen?**
- ⭐⭐ **Wie lautet der SHA-256 der `requirements.lock`, selbst gerechnet?**
- ⚠️ **Gab es schon einen Abschnitt zu Codeherkunft oder Lock?**
- **`numstat`: entfernte Zeilen wirklich 0?**
- ⭐ **Bricht ein Lauf mit abweichendem Lock wirklich mit rc 2 ab?**
- **Welche Beobachtungen hast du gemacht, die du NICHT ausgeführt hast?**

---

## In einfacher Sprache

**Das Regelwerk erfährt zwei Dinge, die es bisher nicht wusste.**

**Erstens:** Der Auswahllauf muss künftig beweisen, aus welchem Verzeichnis
sein Programmcode stammt — und dass dort nichts Unfertiges herumliegt.
⭐ **Bisher konnte er nur beweisen, welche Daten er gelesen hat, nicht welches
Programm sie gelesen hat.**

**Zweitens:** Es wird festgehalten, welche Programmbibliotheken in welcher
genauen Fassung installiert waren. **Ohne diese Angabe lässt sich ein Lauf
später nicht wiederholen**, selbst wenn Code und Daten stimmen.

⚠️ **Und zum Schluss wird geprüft, dass der Code wirklich tut, was der neue
Text behauptet** — mit einem Lauf, der absichtlich falsch aufgesetzt ist und
abbrechen muss. **Ein Regeltext, den das Programm nicht einhält, wäre
schlimmer als gar keiner.**
