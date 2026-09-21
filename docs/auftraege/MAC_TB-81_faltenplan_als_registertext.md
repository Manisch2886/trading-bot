# TB-81 Der Faltenplan als Registertext — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel fuer Claude Code: `TB-81 Faltenplan als Registertext`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, Base `main`. Direkt auf `main`, kein Zweig,
kein PR.

⭐ **Was diese Aufgabe tut:** Sie trägt den **Faltenplan als Registertext** ein
(Fables 30.2 (2)) und berichtigt sein Kriterium für die Abbild-Datei
(30.2 (3)), das er selbst zurückgenommen hat.

⛔ **Diese Aufgabe ändert KEINEN Code.** Kein `faltenplan.py`, keine
Sperrlisten-Datei, nichts unter `research/`, `strategies/`, `shared/`,
`snapshots/`. **Nur `docs/`.**

⛔ **Sie erzeugt NICHT die Abbild-Datei.** Die folgt in einer eigenen Aufgabe,
nachdem der Verfahrensprüfer den Registertext geprüft hat und eine Freigabe
vorliegt.

---

## Was gilt — die Quelle

**`docs/projektfuehrung/FABLE_ANTWORT_2026-09-21k_abbild_schema.md`** ⚠️ liegt
noch **nicht** im Repo; der steuernde Chat legt sie vor dem Start ab. **Findest
du sie unversioniert im Arbeitsbaum, committe sie in Schritt 0 mit.** Fehlt sie
ganz: **abbrechen und melden** — der Wortlaut unten wäre dann ohne Träger.

⭐ **Fables Rücknahme im Wortlaut, weil sie den Grund trägt:**

> *„Mein Satz in 30.2 (3) hat die **Herkunft** einer Datei an einem **Symptom**
> festgemacht (Felder aus dem Trainingsfenster). Als Beleg für ‚anderer
> Verfahrensstand' war das richtig; als Kriterium für ‚ist Abbild' ist es zu
> schwach *und* zu stark zugleich — zu stark, weil es eine Datei mit inhaltlich
> richtigem Plan wegen toter Felder verwirft; zu schwach, weil eine Datei ohne
> diese Felder immer noch etwas anderes tragen kann, das 4a nicht kennt."*

---

## Schritt 0 — Sichern und den Ausgangsstand prüfen

1. `git status --short`, committe, was im Arbeitsbaum liegt (siehe oben).
2. **Prüfe, bevor du schreibst:** `grep -cE "^## 33\." docs/VORREGISTRIERUNG_neuselektion.md`
   muss **0** sein. Ist es 1, **abbrechen und melden**.
3. `shasum -a 256` der drei Sperrlisten-Dateien als Ausgangsstand, **voller
   Pfad** — ⚠️ es gibt sechs Dateien `faltenplan*.json` im Repo.

**Commit:** `TB-81 Schritt 0`. **Pushen.**

---

## Schritt 1 — Die Zahlen selbst messen

⚠️⚠️ **Dieser Auftrag nennt unten Faltenlisten. Übernimm sie NICHT.** Miss sie
selbst aus `research/vorregistrierung/ergebnisse/faltenplan_tb80.json` und
vergleiche. *`C1`: jede Zahl wird an ihrer Quelle nachgerechnet, nicht aus
einem Bericht übernommen — auch nicht aus diesem.*

**Zu messen je Bot:** `horizontbeginn` · `faltenlaenge_jahre` ·
`erste_falte` · die Liste der Selektionsfalten · deren Anzahl.

⭐ **Zweite, unabhängig geschriebene Zählung:** Leite die Faltenliste
zusätzlich aus `falten` ab (Einträge mit `rolle == "selektion"`) und halte sie
gegen `selektionsfalten`. **Weichen sie ab, brich ab und melde es.**

⚠️ **Und gegen Register 21.4 halten** — die dortige Tabelle nennt erste Falte
und Faltenzahl je Bot. Weicht etwas ab, **melden, nicht angleichen**; 21.4 ist
älter als TB-72/TB-80, und welche Fassung gilt, ist keine Handwerksfrage.

Beleg nach `docs/belege/TB-81/schritt1_faltenlisten.txt`, **mit der Umgebung,
in der du gemessen hast**.

**Commit:** `TB-81 Schritt 1: Faltenlisten gemessen`. **Pushen.**

---

## Schritt 2 — Registerabschnitt 33

⚠️ **Append-only.** Ans Ende von `docs/VORREGISTRIERUNG_neuselektion.md`,
nichts weiter oben ändern.

⚠️⚠️ **Die Tabelle in 33.2 füllst du mit DEINEN gemessenen Werten aus Schritt 1**,
nicht mit denen aus diesem Auftrag. Stimmen sie überein, ist das ein Nachweis;
stimmen sie nicht überein, ist es ein Abbruchgrund.

```markdown

---

## 33. Der Faltenplan als Registertext, und was die Abbild-Datei tragen muss (Fable 21k, 21.09.2026)

⭐ **Zwei Dinge in einem Abschnitt:** der Faltenplan nach 4a als Registertext
(Fables 30.2 (2)) und die **Berichtigung** seines Kriteriums aus 30.2 (3), das
er selbst zurückgenommen hat.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21k_abbild_schema.md`,
zeichengleich. Anlass: `FABLE_ANFRAGE_2026-09-21e_abbilddatei_felder.md`.

### 33.1 Berichtigung zu 30.2 (3) — ein Symptom war zum Kriterium geworden

⚠️ **Der Satz in 30.2 (3)** — *„Trägt eine Datei Felder, die 4a nicht kennt
(Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild"* — **ist ERSETZT.**
Er bleibt dort zeichengleich stehen.

**Der Anlass, gemessen 21.09.2026:** Alle drei vorhandenen Pläne tragen
`training_bis_ausschliesslich` (60 verschiedene Werte) und `embargo_nach_falten`
(29 verschiedene) — der gesperrte `faltenplan.json`, `faltenplan_tb72.json`
**und** der am selben Abend erzeugte `faltenplan_tb80.json`. ⭐ **Und: kein
Laufcode liest sie** — `training_bis_ausschliesslich` hat genau einen Treffer im
Repo, `faltenplan.py:306`, und das ist die Stelle, die es **schreibt**.

⭐⭐ **Fables Grund, warum „die Felder wirken ja nicht" trotzdem kein Kriterium
ist — wörtlich:**

> *„Das ist eine Aussage über Code, der **noch nicht eingefroren ist** (TB-30b
> steht aus). Ein Registertext, der davon abhängt, was der Code heute nicht
> liest, wandert mit dem Code — dieselbe Klasse wie die Datenuhr. Und: Ein
> Abbild ist nicht nur für den Lauf da, sondern für jeden, der später nachliest,
> was der Plan war. Sechzig verschiedene Trainingsgrenzen in einer Datei
> beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht
> man der Datei nicht an."*

### 33.2 Der Registertext — der Faltenplan nach 4a

> **Registertext (30.2 (2)), Faltenplan.** Der Faltenplan ist Registertext. Je
> Bot gelten: der Horizontbeginn (absolutes Datum oder ausdrücklich „kein
> Horizont"), die Faltenlänge in Jahren, die erste Selektionsfalte und die
> vollständige Liste der Selektionsfalten. Die Falten sind zusammenhängende
> Kalenderjahre in Schritten der Faltenlänge, aufsteigend und lückenlos vom
> Beginn der ersten Falte bis zum Go-Live-Schnitt. Eine Datei, die diesen Text
> maschinenlesbar wiedergibt, ist sein **Abbild** (33.3); der Registertext ist
> die Quelle.

**Tatsachennotiz — der Plan, gemessen am `<Stand/Commit>` aus
`faltenplan_tb80.json` (SHA-256 `<deiner>`):**

| Bot | Markt | Horizontbeginn | Faltenlänge | erste Falte | Selektionsfalten | # |
|---|---|---|---:|---:|---|---:|
| *(mit deinen gemessenen Werten füllen — neun Zeilen)* | | | | | | |

⚠️ **Zur Herkunft:** Die Werte ruhen auf `asof` = 2026-09-19 (28.3), dem
Horizontbeginn je Bot (28.4), dem Vorlauf gegen den Horizontbeginn (28.6), der
Konjunktion aus 25.3 und dem Trockenlauf nach 3b (b). ⭐ **Abschnitt 32 hat
gemessen, dass die Umstellung von der Datenuhr auf `asof` keine einzige Falte
bewegt** — die Liste ist also dieselbe wie vor der Umstellung, und das ist
belegt, nicht angenommen.

### 33.3 Die Feldliste des Abbilds — abschliessend

**Fables Ersatztext für 30.2 (3), zeichengleich:**

> Das Abbild trägt **genau** die Grössen, die der Registertext des Faltenplans nach 30.2 (2) nennt — nicht mehr, nicht weniger. Der Registertext 30.2 (2) zählt diese Grössen **abschliessend** auf (die Feldliste). Eine Datei ist das Abbild, wenn (i) ihre Feldmenge gleich der Feldliste ist und (ii) ihre Werte je Bot und je Jahr dem Registertext entsprechen. Beides prüft die Sonde nach 30.2 (3); ein zusätzliches Feld ist ein Fehlschlag wie ein fehlendes. Wie die Datei erzeugt wird, ist Handwerk; der erzeugende Code wird mit der Datei registriert (5e).

**Die Feldliste:**

| | Feld | Inhalt |
|---|---|---|
| | `asof` | das Datum aus 28.2/28.3 |
| je Bot | `bot` | der Name |
| je Bot | `horizontbeginn` | Datum **oder** ausdrücklich „kein Horizont" — ⭐ **gesetzt, nicht weggelassen** |
| je Bot | ⭐ **`faltenlaenge_jahre`** | ⚠️ **Ergänzung gegenüber Fables Vorschlag — Begründung in 33.4** |
| je Bot | `erste_selektionsfalte` | die erste Falte |
| je Bot | `selektionsfalten` | die Liste, aufsteigend und lückenlos |
| | `quelle` | der Registerabschnitt, dessen Wortlaut die Datei abbildet |

⛔ **Nicht in der Liste und damit nicht in der Datei:** Trainingsgrenzen,
Embargo, Purge. ⭐ *Fable: „Verfahren B hat kein Trainingsfenster; eine Grösse,
die das Verfahren nicht kennt, kann nicht im Registertext stehen und darf
deshalb nicht in der Datei stehen. Das ist die Folge der Regel, nicht die
Regel."*

⇒ ⚠️ **Keine der drei vorhandenen Dateien ist danach das Abbild** — auch
`faltenplan_tb80.json` nicht, und zwar **nicht wegen ihrer Herkunft**, sondern
weil ihre Feldmenge nicht die Feldliste ist.

### 33.4 ⚠️ Zwei Anpassungen an Fables Feldliste, und warum

**Er hat sie ausdrücklich zur Prüfung gestellt** (*„ich prüfe dann Text und
Feldliste zusammen"*) und eine Unsicherheit benannt.

| | Befund | Folge |
|---|---|---|
| **1** | ⚠️⚠️ **`selektionsfalten` als „Liste von Kalenderjahren" deckt `elliott_wave` nicht ab.** Gemessen: Seine vier Falten sind **Doppeljahre** (`2018-2019`, `2020-2021`, `2022-2023`, `2024-2025`), die der acht übrigen Bots Einzeljahre | Der Registertext in 33.2 sagt **„zusammenhängende Kalenderjahre in Schritten der Faltenlänge"** statt „Kalenderjahre" |
| **2** | ⭐ **Ohne `faltenlaenge_jahre` ist die Liste nicht prüfbar.** Aus `['2018-2019', …]` allein folgt nicht, ob die Faltenlänge 2 ist oder ob zwei Einzeljahre zusammengeschrieben wurden | Das Feld kommt in die Liste |
| **3** | **Seine Unsicherheit — die Bestätigungsperiode je Bot:** Sie steht **bereits** in Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave` `2026-2027`, die acht übrigen `2026`) | ⭐ **Nicht in die Feldliste.** *Ein Abbild bildet ab, was sein Abschnitt sagt; eine Grösse, die anderswo registriert ist, wäre ein zweiter Ort für denselben Wert* — die Bauart, die er in 21j selbst abgelehnt hat |

⚠️ **Alle drei sind dem Verfahrensprüfer vorzulegen.** Punkt 1 und 2 ändern
seinen Wortlaut; Punkt 3 beantwortet seine Unsicherheit. ⛔ **Der Abschnitt gilt
bis dahin mit diesem Vermerk** — er ist nicht vorläufig, aber die Prüfung steht
aus.

### 33.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** | eigene Aufgabe, nach Fables Prüfung von 33.2/33.3 und mit Betreiberfreigabe |
| ⛔ | **Die Sonde schreiben** (Feldmenge und Werte gegen den Registertext) | dieselbe Aufgabe |
| ⛔ | **Eine Datei mit Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **`faltenplan.py` ändern** — die Freigabe vom 21.09. galt für Bedingung (i) und ist verbraucht | — |
| ⚠️ | **Entscheidungsvorlage, nicht vollzogen:** ob die Abbild-Datei aus einem geänderten `faltenplan.py` entsteht oder aus einem **neuen, kleinen Schreiber**, der genau die Feldliste ausgibt. ⭐ *Fable: „gleichwertig, solange der Code registriert ist."* Beides berührt Sperrlisten-nahen Code und braucht eine eigene Freigabe | Betreiber |
```

**Nachweise 2:**

1. `git diff --numstat -- docs/VORREGISTRIERUNG_neuselektion.md` → zweite Spalte
   **`0`**.
2. `grep -nE "^## 33\."` → genau einmal als `##`-Überschrift; zweite,
   unabhängige Zählung dazu.
3. Die neun Zeilen der Tabelle gegen deine Messung aus Schritt 1 — **identisch**.

**Commit:** `TB-81 Schritt 2: Registerabschnitt 33, Faltenplan als Registertext und die Feldliste`. **Pushen.**

---

## Schritt 3 — Abschlussprüfung und Abgabe

| | zu prüfen | Soll |
|---|---|---|
| 1 | `numstat` je Datei über alle Commits | zweite Spalte **`0`** überall |
| 2 | Nichts ausserhalb `docs/` | leer |
| 3 | Drei Sperrlisten-Hashes gegen Schritt 0 | unverändert |
| 4 | `faltenplan_tb80.json` und `faltenplan_tb72.json` | unverändert |
| 5 | Registerabschnitte | `26`…`33`, jeder genau einmal |
| 6 | `git status --porcelain` **nach dem letzten Commit** | nur `.claude/settings.local.json` |

**Ergebnisdokument** `docs/ERGEBNIS_TB-81_faltenplan_registertext.md` mit allen
Nachweisen, **jeder Abweichung mit Begründung** und **„In einfacher Sprache"**.

**Journalblock** direkt ans Ende von `JOURNAL.md`, vor
`## Wiederkehrende Lehren`; **Buchstabe gemessen** (letzter ist `CH`),
Quellenzeile auf das Ergebnisdokument.

---

## Abbruchkriterien

⛔ **Brich ab und melde, wenn:**

1. `grep -cE "^## 33\."` vor deinem Eintrag nicht `0` ist.
2. Deine gemessenen Faltenlisten von denen in diesem Auftrag abweichen.
3. Die zweite Zählung (aus `falten`, `rolle == "selektion"`) von
   `selektionsfalten` abweicht.
4. Die Werte gegen **Register 21.4** abweichen — ⚠️ **melden, nicht angleichen.**
5. Ein Sperrlisten-Hash sich ändert.
6. `FABLE_ANTWORT_2026-09-21k_abbild_schema.md` weder im Repo noch im
   Arbeitsbaum liegt.

---

## In einfacher Sprache

**Was hier gemacht wird:** Der Auswertungsplan — welche Jahre bei welchem Bot
geprüft werden — kommt als Text ins Regelwerk. Bisher stand er nur in einer
Datei; jetzt ist der Text die Quelle und die Datei nur noch sein Abbild.

**Warum das der entscheidende Schritt ist:** Eine Datei kann jemand neu
erzeugen, und dann steht etwas anderes drin. Ein Registertext kann das nicht —
er ist unveränderlich, sobald er steht. Ab jetzt muss sich die Datei nach dem
Text richten, nicht umgekehrt.

**Was dazu neu entschieden wurde:** Der Prüfer hatte festgelegt, welche Felder
die Datei **nicht** enthalten darf. Das hat er zurückgenommen — stattdessen
steht jetzt abschliessend fest, was sie enthalten **muss**, und genau das. Ein
Feld zu viel ist derselbe Fehler wie eines zu wenig, und prüfen kann das ein
kleines Programm statt eines Urteils.

**Was ausdrücklich noch nicht gemacht wird:** Die Datei selbst. Die kommt erst,
wenn der Prüfer den Text gesehen hat — und dafür braucht es eine eigene
Freigabe.
