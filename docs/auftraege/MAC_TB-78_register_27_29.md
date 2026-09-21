# TB-78 Register 27–29, Prüfprinzip A8, Arbeitsweise-Regeln — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-78 Register 27-29`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, Base `main`. Direkt auf `main`, kein Zweig, kein PR
(Dokumentationsaufgabe, `ARBEITSWEISE.md` Abschnitt 5b).

⛔ **Diese Aufgabe rechnet nicht.** Sie ändert **keinen** Code, **keine**
Sperrlisten-Datei, **keine** Datei unter `research/`, `strategies/`, `shared/`,
`snapshots/`. Sie schreibt ausschliesslich nach `docs/`.

⭐ **Verwiesen, nicht abgeschrieben:** `docs/PRUEFPRINZIPIEN.md` und
`docs/projektfuehrung/ARBEITSWEISE.md` gelten unverändert und sind lesbar.

---

## Schritt 0 — Sichern, was schon dasteht

⚠️ **Im Arbeitsbaum liegen bereits elf Änderungen unter
`docs/projektfuehrung/`**, die der steuernde Chat über die Geräteanbindung
abgelegt hat, bevor diese Sitzung startete. Sie sind **nicht** von dir und
**nicht** Gegenstand deiner inhaltlichen Arbeit — aber sie gehören gesichert,
bevor du anfängst.

Es sind zehn neue Dateien und eine geänderte:

```
docs/projektfuehrung/FABLE_ANTWORT_2026-09-20a_grenzfall.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21d_sichtschutz.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21e_fassung_gemessen.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21f_fassungsvergleich.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21h_festlegung_11.md
docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21b_messmeldung_vorlauf_und_kapitalpfad.md
docs/projektfuehrung/UEBERGABE_2026-09-19.md          (geändert: 442 → 984 Zeilen)
```

Dazu diese Auftragsdatei selbst unter `docs/auftraege/` und der Zeiger
`docs/auftraege/AKTUELLER_AUFTRAG.md`.

**Was du tust:**

1. `git status --short` — erwartet sind genau diese Dateien plus
   `.claude/settings.local.json` (unversioniert, bleibt liegen) plus die zwei
   Auftragsdateien.
2. ⚠️ **Prüfe die Ersetzung an `UEBERGABE_2026-09-19.md`, bevor du sie
   committest:** `git diff --numstat -- docs/projektfuehrung/UEBERGABE_2026-09-19.md`
   muss **`542  0`** zeigen — 542 Zeilen hinzu, **null entfernt**. Zeigt es eine
   andere Zahl in der zweiten Spalte als `0`, **brich ab und melde es**: dann ist
   die alte Fassung kein Präfix der neuen, und es ist etwas verlorengegangen.
3. Committe und pushe alles ausser `.claude/settings.local.json`, mit der
   Nachricht `TB-78 Schritt 0: Fable-Dokumente und Uebergabe-Nachtrag 4 ins Repo`.
4. `git status --short` erneut — erwartet: nur noch `.claude/settings.local.json`.

---

## Was diese Aufgabe einträgt — die Übersicht

| Schritt | Datei | Art |
|---|---|---|
| 1 | Register, neuer **Abschnitt 27** — Sichtschutz | zeichengleich aus Fable 21g |
| 2 | Register, neuer **Abschnitt 28** — `asof`, Horizontbeginn, Vorlauf | Berichtigungen |
| 3 | Register, neuer **Abschnitt 29** — Beginn des Kapitalpfads | **neuer** Registertext |
| 4 | `docs/PRUEFPRINZIPIEN.md` — neues Prinzip **`A8`** | Ergänzung |
| 5 | `docs/projektfuehrung/ARBEITSWEISE.md` — drei Regeln | Ergänzung |
| 6 | `docs/ERGEBNIS_TB-77_horizont_je_bot.md` — Berichtigungsblock | Anfügen |
| 7 | Abschlussprüfung, Journalblock, Abgabe | — |

⚠️ **Nacheinander, jeder Schritt mit eigenem Commit und Push.** Nicht sammeln.
*Grund, gemessen: In TB-59 stand das Sichern als letzter Nachweis; die Arbeit lag
elf Stunden ungesichert im Arbeitsbaum, auf einem Rechner und in keiner Version.*

⚠️ **Das Register ist append-only.** Jeder der drei Abschnitte wird **ans Ende
der Datei angehängt**. Nichts weiter oben wird geändert, umformuliert oder
entfernt — auch nicht, wenn es überholt ist. Was überholt ist, bekommt seine
ERSETZT-Marke **im neuen Abschnitt**, nicht an der alten Stelle.

⚠️ **Nachweis je Registerschritt:** `git diff --numstat -- docs/VORREGISTRIERUNG_neuselektion.md`
muss in der **zweiten Spalte `0`** zeigen. Zeigt sie etwas anderes, hast du
gelöscht — zurücknehmen und melden.

---

## Schritt 1 — Registerabschnitt 27: Sichtschutz des Verfahrensprüfers

**Quelle:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md`,
Abschnitt 3. ⭐ **Zeichengleich eintragen, nicht nachformulieren.** Der Text ist
Fables Entscheidung; jede Umformulierung wäre eine zweite Fassung.

Hänge ans Ende von `docs/VORREGISTRIERUNG_neuselektion.md` an:

```markdown

---

## 27. Sichtschutz des Verfahrensprüfers (Fable 21g, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung.** Er regelt, was der
Verfahrensprüfer vor dem signierten Tag wissen darf — und damit, ob seine
Registerentscheidungen nachträgliche Wahlen sein können. Quelle des Grundes
nach F17; die Regel nennt kein Ergebnis.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md`,
Abschnitt 3, zeichengleich übernommen. Vorgeschichte: 21d (Fables Vorschlag),
dazu zwei Messungen des steuernden Chats vom 21.09. — das Register ist rein
(24 Sharpe-Erwähnungen, alle Regeltext, keine gemessene Kennzahl je
Parametersatz), `BACKLOG.md` ist es nicht (Z. 190 `W14`, Z. 170 `T39.2`).

### 27.1 bis 27.5 — der Registertext, zeichengleich

> **27. Sichtschutz des Verfahrensprüfers**
>
> **27.1** Der Verfahrensprüfer erhält vor dem signierten Tag keine Ergebnisgrössen des Selektionsraums: keine Kennzahl eines Parametersatzes (Sharpe, Rendite, Drawdown, Trefferquote, Anzahl Trades), keine Aussage, welche oder wie viele Sätze eine Bedingung erfüllen, keine Rangfolge, keine Plateau-Lage — **und keine Erwartung, Schätzung oder Prognose über den Ausgang des Laufs**, gleich ob als Zahl oder als Satz.
>
> **27.2** Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl, Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die registrierten heutigen Parameter, wenn die Regel vor der Messung geschrieben stand (Bauart 24.3).
>
> **27.3** Das Register darf der Verfahrensprüfer vollständig lesen; was darin steht, hat dieses Tor bereits passiert (gemessen 21.09.: keine Kennzahl je Parametersatz im Registertext). Eine Ablage-Kopie trägt Commit-Hash, Datum und die Kennzeichnung KOPIE.
>
> **27.4** Der Verfahrensprüfer führt in jeder Antwort ein Leseprotokoll (welche Dateien er in diesem Chat gelesen hat). Das Protokoll ist Selbstauskunft. Die Prüfung, ob seine Begründungen Grössen nach 27.1 enthalten, ist Pflicht des steuernden Chats (Prüfprinzipien).
>
> **27.5** Wer dem Verfahrensprüfer einen Treffer nach 27.1 in einer Datei meldet, nennt Datei und Fundstelle, nicht den Inhalt.
>
> **Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim Inkrafttreten (21.09.2026):**
> Der Chat des Verfahrensprüfers wurde am 21.09. neu begonnen; er kennt aus dem Vorgängerchat nichts. Sein Wissensstand beim Inkrafttreten ist vollständig: der Wortlaut von `FABLE_UEBERGABE_2026-09-21_neuer_chat.md` (Fassung 2) und die Dateien `FABLE_ANTWORT_2026-09-20e_konjunktion.md`, `FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`, `FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`, alle in der Projektablage. Darin enthaltene Grössen, die an 27.1 grenzen: die Wirkung von Abschnitt 23 auf die DD-Toleranz der fünf Krypto-Bots (2,4- bis 5,0-fach); die Zahlen aus 24.6 (59 von 64 Falten tiefer, Mediane je Bot −1,39 bis −3,09 Prozentpunkte, fünf Falten flacher; Krypto 2018–2020 nicht enthalten). Beides sind Wirkungen auf die heutigen Parameter, gemessen nach der jeweils vorher geschriebenen Regel (27.2). Dazu, am 21.09. durch eine Treffermeldung mitgeteilt: der Wortlaut der Erwartung in `BACKLOG.md` Zeile 190 (W14) über die Zahl der Bots auf Schatten — eine Erwartung nach 27.1, keine Messung; sie lag nach Festlegung 12 als Möglichkeit bereits vor. Weitere Grössen nach 27.1 kennt der Verfahrensprüfer nicht.

### 27.6 Wo der Nullpunkt liegt

⭐ **Die Protokollkette beginnt nicht mit 21d, sondern mit der Tatsachennotiz
oben.** Fable, 21g Abschnitt 4: *„Der Sichtschutz regelt den Grund, nicht den
Zugriff — und ein Grund lässt sich nicht rückwirkend entkennen."* Die
Rückwirkung ist deshalb **Bestandsaufnahme, kein Pflichtenrückbau**: *„Was ich
beim Inkrafttreten wusste, wird festgehalten, nicht bewertet."*

**Für den Vorgängerchat des Verfahrensprüfers** gilt: seine Entscheidungen
(Abschnitte 23–26) sind registriert, und die Reihenfolge Regel → Messung ist im
Register selbst dokumentiert (24.3 vor 24.6). Was er sonst wusste, ist nicht
mehr feststellbar und muss es nicht sein — die Prüfung nach 27.4 ist auf seine
Begründungen genauso anwendbar, und sie liegen vollständig vor.

### 27.7 Ein Verstoss beim Melden des Verstosses — festgehalten, nicht geglättet

⚠️ Der steuernde Chat hat Fable am 21.09. den **Inhalt** des Sichtschutz-Treffers
zitiert (`BACKLOG.md` Z. 190 wörtlich) statt seiner Fundstelle. Fable hat es
selbst gemeldet und in die Tatsachennotiz eingetragen: *„Durch das Zitat kenne
ich die Zeile jetzt."*

⭐ **Daraus ist 27.5 entstanden.** Der Fehler steht hier, weil er die Regel
erzeugt hat und weil die Fehlerklasse benannt gehört: **wer prüft, fasst an** —
dieselbe Klasse, gegen die `A1` und `B1` gebaut sind.

### 27.8 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Register-KOPIE in die Projektablage legen** (mit Commit-Hash, Datum, Kennzeichnung KOPIE nach 27.3). Sie wird erst gezogen, **nachdem** alle Abschnitte dieser Aufgabe stehen — eine Kopie des Zwischenstands liefe sofort auseinander | steuernder Chat, nach TB-78 |
| ⛔ | **`BACKLOG.md` bereinigen oder verschieben.** 27.1 verlangt es nicht; die Regel liegt beim Leser, nicht bei der Datei | — |
| ⚠️ | **Die Prüfung nach 27.4** (Fables Begründungen gegen verbotene Grössen lesen) ist eine stehende Pflicht des steuernden Chats, kein Schritt dieser Aufgabe. Sie steht ab jetzt als Prüfprinzip `A8` (Schritt 4) | laufend |
```

**Nachweis 1:** `git diff --numstat -- docs/VORREGISTRIERUNG_neuselektion.md`
→ zweite Spalte **`0`**. Dazu: `grep -c "27.5" docs/VORREGISTRIERUNG_neuselektion.md`
und der Wortlaut von 27.1 per `grep -n "keine Erwartung, Schätzung oder Prognose"`.

**Commit:** `TB-78 Schritt 1: Registerabschnitt 27, Sichtschutz des Verfahrenspruefers`. **Pushen.**

---

## Schritt 2 — Registerabschnitt 28: `asof`, Horizontbeginn, Vorlauf

**Drei Berichtigungen in einem Abschnitt**, alle derselben Sache: dem Datum, ab
dem ein Bot rechnen darf.

⚠️ **Rechne den Horizontbeginn selbst nach, bevor du ihn einträgst.**
`2026-09-19` minus `RECENT_YEARS_ONLY = 10 Jahre` = `2016-09-19`. Die Konstante
liest du aus dem Code (Fundstellen stehen in Register 26.1) — **nicht aus diesem
Auftrag übernehmen**, sondern gegenmessen und beides im Bericht nennen. Weicht
der gelesene Wert von 10 ab, **brich ab und melde es**.

Hänge ans Ende der Registerdatei an:

```markdown

---

## 28. `asof` ist gesetzt — Berichtigung zu 26.3 und 26.6, und der Vorlauf-Satz gilt fort (TB-78, 21.09.2026)

⭐ **Drei Berichtigungen, Kategorie „Berichtigung" nach F17** (Registertext an
Registertext; die Quelle des Grundes ist eine Entscheidung des
Verfahrensprüfers, kein Ergebnis).

⚠️ **Abschnitt 26 bleibt zeichengleich stehen.** Was dort überholt ist, wird
hier benannt und trägt seine ERSETZT-Marke an dieser Stelle.

### 28.1 Warum es eine Berichtigung braucht — der Auftrag lief mit überholter Prämisse

**Gemessen 21.09.2026:** TB-77 hat durchgehend gegen die ursprüngliche
Auftragsfassung gearbeitet; der Nachtrag, der zwei Blocker aufhob, ist nie
angekommen (`grep` über Ergebnisdokument und `docs/belege/TB-77/` nach
*„Nachtrag zu TB-77"* und `FABLE_ANTWORT_2026-09-21b`: **0 Treffer**).

⭐ **Regel daraus, festgehalten, weil sie teuer war:** *Nach jeder Antwort des
Verfahrensprüfers werden die **laufenden** Aufträge gegen sie geprüft, nicht nur
die kommenden. Ein Nachtrag in eine laufende Sitzung ist billiger als eine
Berichtigung im Register.*

### 28.2 Registertext 5a, Ergänzung — woher `asof` kommt

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md`,
Abschnitt (2), zeichengleich.

> **Registertext 5a, Ergänzung:** asof ist das UTC-Datum des Erstellungszeitpunkts des registrierten Snapshots. Es wird im `MANIFEST.json` als Feld `asof` geführt und im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof.

**Fables Begründung, warum das Erstellungsdatum und nicht das Datenende** — im
Wortlaut, weil sie den Unterschied trägt:

> *„Das Datenende (grösstes `open_time` über alle Kursdateien) wäre eine zweite aus dem Inhalt abgeleitete Grösse — genau die Bauart, die ich bei `fensteranker` abgelehnt habe, weil sie mit den Daten wandert. […] Dieser Abstand ist eine Frische-Tatsache und gehört als eigenes Manifest-Feld (`datenende`) dorthin, nicht in asof. Das Erstellungsdatum ist bereits registriert, von niemandem anders berechenbar und unabhängig davon, welches Symbol zuletzt eine Kerze hatte."*

**Bekannte Wirkung auf die Zulässigkeit, aus derselben Quelle:** Der
Horizontbeginn verschiebt sich gegenüber dem Datenende um vier Tage (19.09.
statt 15.09.). Die erste Falte nach 4a beginnt am 1. Januar eines Jahres; eine
Verschiebung im September ändert das Jahr nicht. ⭐ *Das ist eine
Kalenderaussage, keine Ergebnisaussage.*

### 28.3 Tatsachennotiz — der Wert von `asof`

| | Wert | Fundstelle |
|---|---|---|
| **`asof`** | **`2026-09-19`** | Abschnitt 18, `zeitpunkt_utc` = `2026-09-19T06:49:32+00:00`, gelesen aus `snapshots/63e4b6c8…/MANIFEST.json` |
| Snapshot | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | Abschnitt 18, Commit `1075dec` |

⭐ **Der Wert ist keine neue Messung.** Er stand seit dem 19.09. als Tatsache im
Register; was fehlte, war die Zeile, die ihn `asof` nennt.

### 28.4 ⚠️ ERSETZT: die Platzhalter-Tabelle in 26.3

**Die vier Platzhalter-Zeilen in 26.3** — *„[PLATZHALTER — `asof` ist nicht
gesetzt; Datum folgt, sobald 5a einen Wert hat]"* — **gelten als ERSETZT.** Sie
bleiben dort zeichengleich stehen (append-only). Die gültige Fassung:

| Bot | Markt | `RECENT_YEARS_ONLY` | Horizontbeginn = `asof` − Konstante |
|---|---|---:|---|
| `elliott_wave` | krypto | keine | **kein Horizont** (26.2) |
| `t3_supertrend` | krypto | keine | **kein Horizont** |
| `rsi2_crypto` | krypto | keine | **kein Horizont** |
| `turtle_soup_crypto` | krypto | keine | **kein Horizont** |
| `volatility_breakout_crypto` | krypto | keine | **kein Horizont** |
| `elliott_wave_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `rsi2_mean_reversion` | aktien | 10 Jahre | **2016-09-19** |
| `turtle_soup_stocks` | aktien | 10 Jahre | **2016-09-19** |
| `volatility_breakout` | aktien | 10 Jahre | **2016-09-19** |

⚠️ **Die Konstante ist aus dem Code gelesen** (Fundstellen 26.1), nicht
registriert. Ob sie als registrierte Grösse nach `registerdaten.py` gehört,
bleibt offen — siehe 28.7.

⚠️ **Abgegrenzt, damit es niemand verwechselt:** 15.6 Punkt 3 nennt
*„gemessen vom letzten Kurstag (2026-09-01) zurück auf 2016-09-01"*. Das ist die
**Datenuhr**, genau der Bezug, den 26.2 ablöst — **kein `asof`**. Die
Ähnlichkeit der beiden Daten (2016-09-01 gegen 2016-09-19) ist Zufall des
Kalenders und kein Hinweis darauf, dass es dasselbe wäre.

### 28.5 ⚠️ ERSETZT: die zwei Zeilen in 26.6, die `asof` als offen führen

**Zeile 1 von 26.6** — *„`asof` setzen. Wann und wodurch, ist Fables Frage (1)
im neuen Chat; die Lesart ‚mit Snapshot und Tag zugleich' ist nicht entschieden.
Bis dahin bleibt 26.3 ein Platzhalter"* — **ist ERSETZT.** Entschieden seit
21b: **durch den Snapshot, nicht durch den Tag.** Fable, wörtlich: *„Nicht mit
dem signierten Tag — der Tag friert ein, was das Register sagt; er erzeugt keine
Zahl."*

**Zeile 2 von 26.6** — *„Tatsachennotiz 4d füllen: vier Daten in 26.3"* — **ist
mit 28.4 erledigt.**

**Zeile 4 von 26.6** (die Wache in `auswertung.py`) — **ist ERSETZT.** Fable hat
seinen eigenen Vorschlag am 21.09. zurückgezogen: *„Mein Vorschlag ‚in den
Auswerter' war falsch adressiert."* Die Wache geht in die vier
`multi_symbol_optimise.py` (TB-30b). ⚠️ **Und sie prüft nicht gegen den
Horizontbeginn, sondern gegen den Beginn der ersten Selektionsfalte** —
siehe Abschnitt 29.

**Zeile 5 von 26.6** (`FABLE_ANTWORT_2026-09-21a` liegt in keinem Träger) — **ist
mit Schritt 0 dieser Aufgabe erledigt**; die Datei liegt unter
`docs/projektfuehrung/`.

⭐ **Unverändert offen bleiben:** Zeile 3 (die vier Optimierer, TB-30b), Zeile 6
(`RECENT_YEARS_ONLY` als registrierte Grösse, Entscheidungsvorlage) und Zeile 7
(nicht gemessen, wie viele Einstiege vor einem Horizontbeginn liegen).

### 28.6 Registertext 4a, Präzisierung, Ergänzung — der Vorlauf-Satz gilt fort

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.1, zeichengleich.

> **4a, Präzisierung, Ergänzung:** Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand. Der Satz aus der Fassung vom 20.09. gilt fort; die Fassung vom 21.09. hat ihn nicht ersetzt, sondern ausgelassen.

**Quelle des Grundes,** Fable wörtlich: *„Ein Vorlauf, der auf Kursen vor dem
Horizontbeginn rechnet, ist derselbe Zugriff"*, den Abschnitt 26 verbietet.
Kategorie: **Berichtigung** (Registertext an Registertext). Kein Ergebnis.

**Die Messung dazu, 21.09.2026, 17:48 durch den steuernden Chat:** Der Satz
*„Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den ersten Kurs im
Bestand"* steht im Register **genau einmal**, in **Z. 4307** — und zwar
**innerhalb des Zitats der als ersetzt markierten Fassung** in 26.2. Er steht
also im Register ausschliesslich als Teil dessen, was ausser Kraft ist.

⭐ **Und die Tatsache, die Fables Unsicherheit auflöst** (*„ob ich den Satz
absichtlich gestrichen habe"*): Die Fassung vom 20.09. ist **nie** in einen
Registertext übernommen worden — gemessen, `grep` im Register: *„Horizontbeginn"*
**0 Treffer**, *„4a, Präzisierung"* **0 Treffer**. Es gab nichts zu streichen;
der Satz ist zwischen zwei Antworten verlorengegangen, nicht im Register.

### 28.7 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Das Feld `asof` ins `MANIFEST.json` schreiben.** 28.2 verlangt es, aber der Snapshot ist nach 17.1 *„nach seiner Erzeugung nicht mehr geschrieben"*. Ob das Manifest Teil dieses Schreibverbots ist, sagt kein Registertext. ⭐ *Fable hält in 21b fest, dass der Snapshot-Hash über den Dateien liegt und nicht über dem Manifest — eine Ergänzung änderte den Hash also nicht.* **Das ist eine Verfahrensfrage vor dem Tag und wird nicht nebenbei entschieden** | Verfahrensprüfer / Betreiber |
| ⛔ | **Das Feld `datenende` ins `MANIFEST.json`** — derselbe Grund | dito |
| ⛔ | **`registerdaten.py` anfassen** | — |
| ⛔ | **Den Faltenplan nach 4a ableiten.** Er hängt an einer offenen Frage an den Verfahrensprüfer (Status des gesperrten `faltenplan.json`, `FABLE_ANFRAGE_2026-09-21b`, Abschnitt C) | eigene Aufgabe, nach seiner Antwort |
```

**Nachweis 2:** `numstat` zweite Spalte `0` · der gelesene Wert von
`RECENT_YEARS_ONLY` mit Fundstelle · `grep -c "2016-09-19"` im Register.

**Commit:** `TB-78 Schritt 2: Registerabschnitt 28, asof gesetzt und Vorlauf-Satz berichtigt`. **Pushen.**

---

## Schritt 3 — Registerabschnitt 29: Beginn des Kapitalpfads

⭐ **Das ist NEUER Registertext, keine Berichtigung** — und das ist gemessen,
nicht angenommen.

**Die Messung, 21.09.2026 durch den steuernden Chat:** Gesucht nach
*„Kapitalpfad"* in Verbindung mit Beginn/Start/1. Januar/erste Falte: **ein
Treffer**, Z. 4296, und der beschreibt den **Schaden**, nicht die Regel:
*„der Kapitalpfad (Registertext 1a) beginnt die erste Falte mit einem
Kapitalstand, der aus nicht registrierten Jahren stammt."* **`Startkapital`
kommt im Register überhaupt nicht vor (0 Treffer).**

⚠️ **Wiederhole diese zwei Messungen selbst**, bevor du den Abschnitt schreibst,
und nenne deine Zahlen im Bericht. *Grund: `C1` — eine Zahl aus einem fremden
Bericht wird an ihrer Quelle nachgerechnet. Findest du mehr Treffer, ist der
Text eine Berichtigung und keine Neuaufnahme; dann brich ab und melde es.*

Hänge ans Ende der Registerdatei an:

```markdown

---

## 29. Der Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte (TB-78, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung** — gemessen: das Register regelt
den Beginn des Kapitalpfads bisher nicht (siehe 29.2).
⭐ **Bauart 24.3: die Regel steht vor der Messung.**

### 29.1 Der Befund — eine Lücke zwischen Horizontbeginn und erster Falte

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.2.

Abschnitt 26 verbietet Einstiege **vor dem Horizontbeginn** (28.4: `2016-09-19`
für die vier Aktien-Bots). Die erste Selektionsfalte beginnt nach 4a am
**1. Januar**. Dazwischen liegen dreieinhalb bis fünfzehn Monate, in denen ein
Einstieg nach 26 **zulässig** ist, in **keiner Falte** auftaucht — und durch den
Kapitalpfad läuft.

⭐ **Fable, wörtlich:** *„Das ist genau der Schaden, mit dem (d) begründet wurde
(‚verändern das Kapital, mit dem die erste Falte beginnt'), nur kürzer."*

⚠️ **Dasselbe kann bei Krypto auftreten**, wo Bedingung (i) wegen des Vorlaufs
später liegt als der erste handelbare Tag — `rsi2_crypto`: 2018 handelbar, erste
Falte 2019.

⚠️⚠️ **Und die Wache aus 21b sieht es nicht**, weil sie gegen den Horizontbeginn
prüft. Deshalb ändert sich mit diesem Abschnitt auch die Wache (29.4).

### 29.2 Die Messung — das Register regelt es nicht

| gesucht | Treffer | was der Treffer sagt |
|---|---:|---|
| `Kapitalpfad` + Beginn/Start/1. Januar/erste Falte | **1** (Z. 4296) | beschreibt den **Schaden**: *„der Kapitalpfad (Registertext 1a) beginnt die erste Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt"* |
| `Startkapital` | **0** | — |

⇒ **Der Text unten ist eine Neuaufnahme.** *Fable hatte das in 21c ausdrücklich
offengelassen: „Steht im Register bereits ein Satz, der den Beginn des
Kapitalpfads festlegt, legt ihn mir im Wortlaut vor — dann ist mein Vorschlag
gegenstandslos oder eine Berichtigung dazu, und das kann ich von hier nicht
sehen."*

### 29.3 Der Registertext, zeichengleich

> **Zu 4a / 26:** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese Regel ohne Belang.

**Quelle des Grundes:** 4a (Falten sind ganze Kalenderjahre) und der Grund von
26 (kein Trade ausserhalb aller Falten im Kapitalpfad). Kein Ergebnis.

⭐ **Der letzte Satz ist Absicht.** Er schliesst aus, dass die Regel später mit
dem Hinweis *„die Wirkung ist ja klein"* aufgeweicht wird — dieselbe Bauart wie
24.3.

### 29.4 Die Wache in TB-30b — geändert gegenüber 21b

⚠️ **Die Fassung aus 21b (Prüfung gegen den Horizontbeginn) ist ERSETZT.** Es
gilt:

> **Wache (TB-30b), angepasst:** frühester Einstieg ≥ **Beginn der ersten Selektionsfalte** (nicht nur ≥ Horizontbeginn). Der Bericht führt je Bot drei Daten nebeneinander: Horizontbeginn, Beginn der ersten Falte, frühester Einstieg.

⚠️ **Ort der Wache unverändert:** in den vier `multi_symbol_optimise.py`, **nicht**
in `auswertung.py` (eingefroren, Abschnitt 0 Z. 31; Fables Rücknahme in 21b).

### 29.5 Was noch zu messen ist — nur das Ob, nicht die Wirkung

| | zu messen | ⚠️ |
|---|---|---|
| 1 | Wo der Kapitalpfad der neun Optimierer **heute** beginnt | — |
| 2 | Ob es in den vorhandenen Trade-Listen Einstiege zwischen Horizontbeginn (bzw. erstem handelbarem Tag) und dem 1. Januar der ersten Falte **gibt** | ⛔ **Nur das Ob, nicht die Wirkung auf Kennzahlen** — eine Zahl über Kennzahlen fiele unter 27.1 |
| | | ⚠️ **Und jede Messung an den neun `paper_trading_*.db` läuft auf einer KOPIE** |

⛔ **Nicht Gegenstand dieser Aufgabe.** Eigene Aufgabe, nach TB-78.
```

**Nachweis 3:** `numstat` zweite Spalte `0` · deine beiden eigenen
`grep`-Zählungen mit ihren Mustern im Bericht.

**Commit:** `TB-78 Schritt 3: Registerabschnitt 29, Beginn des Kapitalpfads`. **Pushen.**

---

## Schritt 4 — Prüfprinzip `A8`

⚠️⚠️ **Die Nummer ist gemessen und lautet `A8`, nicht `A5`.** In
`docs/PRUEFPRINZIPIEN.md` ist `A5` seit dem 18.09. vergeben (*„Ein Werkzeug, das
nicht mehr misst, sagt es"*, Z. 65); höchstes Prinzip der Gruppe A ist `A7`.
Der Vorschlag `A5` stammt aus einem Nachtrag des steuernden Chats, der die
Nummer nicht gemessen hatte — `K2i`.

⚠️ **Miss es selbst nach**, bevor du schreibst: `grep -nE "^### A[0-9]" docs/PRUEFPRINZIPIEN.md`.
Ist `A8` belegt, nimm die nächste freie und **melde die Abweichung**.

⛔ **Nichts umnummerieren.** Der Kopf der Datei sagt es ausdrücklich: *„Nichts
wird umnummeriert — ein Verweis aus einem alten Journalblock muss weiter
treffen."*

Füge **hinter `A7`** und **vor der Überschrift `## B — Wie eine Probe sich
selbst täuscht`** ein:

```markdown

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
```

**Nachweis 4:** `git diff --numstat -- docs/PRUEFPRINZIPIEN.md` → zweite Spalte
**`0`** · `grep -nE "^### A[0-9]" docs/PRUEFPRINZIPIEN.md` → `A1`…`A8`,
**keine Nummer doppelt**.

**Commit:** `TB-78 Schritt 4: Pruefprinzip A8, Selbstauskunft ist keine Wache`. **Pushen.**

---

## Schritt 5 — Drei Regeln in `ARBEITSWEISE.md`

⚠️ **Nichts umformulieren, nichts ersetzen — nur anfügen.** Alle drei sind neu.

**Ankertext (Regel 1 und 2):** Hänge in **Abschnitt 15**
(*„Was mit „zukünftig" gesagt wird…"*), **hinter** dem bestehenden
Unterabschnitt *„### Und jede Rückfrage an den Betreiber steht samt Antwort
wörtlich im Bericht"*, diesen neuen Unterabschnitt an:

```markdown

### ⭐⭐ Und dasselbe gilt für den Verfahrensprüfer — in beide Richtungen

⚠️⚠️ **Gemessen am 21.09.2026 an der Projektablage: der Austausch war halb
abgelegt.** Fable hatte neun Antworten dort liegen; von uns lag **eine einzige**
Anfrage. Die Rückmeldung von 16:24, die Sichtschutz-Antwort und die
Festlegungs-11-Berichtigung von 17:36 existierten nur im Chatverlauf — und der
ist nach `UMZUG.md` Abschnitt 2 **kein Träger**.

> ⭐ **Jede Anfrage und jede Rückmeldung an den Verfahrensprüfer wird abgelegt
> wie seine Antwort** — `projektfuehrung/FABLE_ANFRAGE_<datum><buchstabe>_<stichwort>.md`,
> im Wortlaut des gesendeten Textes, nicht als Zusammenfassung.

⚠️ **Warum das schlimmer ist als gar keine Ablage:** *Ein halb abgelegter
Austausch sieht im Streitfall vollständig aus.* Wer nur Fables Seite liest,
sieht neun Entscheidungen ohne die Fragen, die sie ausgelöst haben — und kann
nicht prüfen, ob die Frage die Antwort schon enthielt.

### ⭐ Bei jeder Übergabe wird ungefragt gesagt, was mitgeht und was nicht

**Anweisung des Betreibers, 21.09.2026.** Der Regelfall ist: **nichts
mitschicken** — der Übergabetext ist selbsttragend, und zwei Quellen für
denselben Sachverhalt lassen bei jeder Abweichung offen, welche gilt.
**Ausnahme:** der Beleg auf Widerspruch. Die Entscheidung wird **genannt**, nicht
stillschweigend getroffen.
```

**Ankertext (Regel 3):** Hänge in **Abschnitt 6d**
(*„Jede Entscheidung wird als anklickbare Frage gestellt — mit Empfehlung"*),
**am Ende des Abschnitts**, vor der Überschrift von Abschnitt 7, an:

```markdown

### ⭐ Auch Fables Fragen an den Betreiber werden ungefragt mit einer Empfehlung beantwortet

⚠️ **Anweisung des Betreibers, 21.09.2026, nach zwei Nachfragen an einem
Nachmittag.** Stellt der Verfahrensprüfer dem Betreiber eine Entscheidungsfrage,
**beantwortet der steuernde Chat sie mit einer Empfehlung, bevor der Betreiber
klickt** — gemessen statt geraten, und mit ausdrücklicher Nennung der Stelle, an
der Fable falsch oder unbelegt liegt.

⭐ **Der Betreiber soll nicht erst „Deine Empfehlung?" fragen müssen.** Dieselbe
Begründung wie 6d selbst: *eine benannte Empfehlung ist widersprechbar; eine
ausgelassene ist nur Arbeit.*
```

**Nachweis 5:** `git diff --numstat -- docs/projektfuehrung/ARBEITSWEISE.md` →
zweite Spalte **`0`** · die drei neuen Überschriften per `grep -n`.

**Commit:** `TB-78 Schritt 5: ARBEITSWEISE, drei Regeln zum Verfahrenspruefer`. **Pushen.**

---

## Schritt 6 — Die „Offen"-Liste aus TB-77 berichtigen

`docs/ERGEBNIS_TB-77_horizont_je_bot.md` führt unter „Offen" die Wache *„samt
Mutationsprobe in `auswertung.py`"*. ⚠️ **Das ist überholt** — Fable hat es in
21b zurückgezogen.

⛔ **Nicht überschreiben.** Ein Ergebnisdokument beschreibt, was eine Sitzung
getan und gewusst hat; es wird nicht rückdatiert. Hänge stattdessen **ans Ende
der Datei** an:

```markdown

---

## ⚠️ Berichtigung, nachgetragen am 21.09.2026 (TB-78)

**Diese Sitzung hat gegen die ursprüngliche Auftragsfassung gearbeitet.** Ein
Nachtrag, der zwei Blocker aufhob, ist nie angekommen — gemessen, `grep` über
dieses Dokument und `docs/belege/TB-77/`: **0 Treffer** für *„Nachtrag zu TB-77"*
und `FABLE_ANTWORT_2026-09-21b`. **Das Dokument bleibt unverändert stehen; was
überholt ist, steht hier.**

| | steht oben | richtig ist, seit |
|---|---|---|
| **1** | Der Platzhalter für `asof` in Registerabschnitt 26.3 | `asof` = **2026-09-19** (Fable 21b; Register **28.2/28.3**, Fundstelle Abschnitt 18) |
| **2** | 26.6: *„`asof` setzen. Wann und wodurch, ist Fables Frage (1)"* | entschieden: **durch den Snapshot, nicht durch den Tag** (Register **28.5**) |
| **3** | „Offen": *„Wache samt Mutationsprobe in `auswertung.py`"* | Fable hat das **zurückgezogen** (*„Mein Vorschlag ‚in den Auswerter' war falsch adressiert"*): die Wache geht in die vier `multi_symbol_optimise.py`, **und sie prüft gegen den Beginn der ersten Selektionsfalte**, nicht gegen den Horizontbeginn (Register **29.4**) |

⭐⭐ **Und ein Befund, der der Sitzung zugutekommt:** Sie hat
`registerdaten.FESTLEGUNGEN` selbst gelesen und die Kette in 26.7 an der Quelle
belegt. Fables Berichtigung (*„keine Festlegung trägt diesen Satz"*) war
**falsch**; er hat sie in 21h vollständig zurückgenommen. ⚠️ **Hätte der
Nachtrag diese Sitzung erreicht, hätte sie Festlegung 11 aus der Kette entfernt
— auf fremde Autorität, gegen die Quelle.** *Das Nichtankommen hat einen
Registerfehler verhindert.*

⭐ **Regel daraus:** *Eine Berichtigung des Verfahrensprüfers wird gemessen wie
jede andere Behauptung — gerade dann, wenn sie uns berichtigt. Wer sagt „ich
kann die Quelle nicht lesen", liefert damit den Grund, seine Quellenangabe zu
prüfen, nicht sie zu übernehmen.*

**Zwei Befunde dieser Sitzung, die übernommen sind:** Der Auftrag nannte **16.3**
als Fundstelle für *„asof kommt aus dem Register, nie aus der Uhr"* — der Satz
steht in **17.1**. Und `FABLE_ANTWORT_2026-09-21a` lag in keinem Träger ausser
der Projektablage; sie liegt seit TB-78 Schritt 0 im Repo.
```

**Nachweis 6:** `numstat` zweite Spalte `0`.

**Commit:** `TB-78 Schritt 6: Berichtigung zur TB-77-Offen-Liste`. **Pushen.**

---

## Schritt 7 — Abschlussprüfung, Journalblock, Abgabe

### 7.1 Die Abschlussprüfung

| | zu prüfen | Soll |
|---|---|---|
| 1 | `git diff --numstat` je geänderter Datei über alle Commits dieser Aufgabe | zweite Spalte überall **`0`** |
| 2 | Registerabschnitte | `grep -nE "^#+ *2[6-9]\."` zeigt **26, 27, 28, 29**, jeden **genau einmal** als `##`-Überschrift |
| 3 | ⭐ **Sperrlisten-Hashes unverändert** | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` (`research/vorregistrierung/ergebnisse/benchmark_drawdowns.json`) · `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` (`…/faltenplan.json`) · `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` (`…/benchmark_drawdowns_vt.json`) — **voller Pfad, nie der blosse Name** |
| 4 | Nichts ausserhalb `docs/` geändert | `git diff --stat <Commit vor Schritt 0>..HEAD -- . ":(exclude)docs"` → **leer** |
| 5 | Prüfprinzip-Nummern | `A1`…`A8`, keine doppelt |
| 6 | `git status --porcelain` **nach dem letzten Commit** | nur `.claude/settings.local.json` |
| 7 | ⚠️ **Zweite, unabhängig geschriebene Zählung** für Prüfung 2 und 5 | *Ein Messergebnis wird gegen eine zweite Zählung gehalten, bevor es als Nachweis gilt* |

⛔ **Kein Basislauf, keine Datenstand-Messung, keine Datenbank-Quersummen.**
Diese Aufgabe berührt nichts davon; ein Basislauf hier wäre Zeit ohne Aussage.

### 7.2 Das Ergebnisdokument

`docs/ERGEBNIS_TB-78_register_27_29.md`. Darin je Schritt: was eingetragen
wurde, `numstat`, die Nachweise, und **jede Abweichung von diesem Auftrag mit
Begründung**. Am Ende **„In einfacher Sprache"** (`ARBEITSWEISE.md` Abschnitt 4).

⚠️ **Jede Rückfrage an den Betreiber und seine Antwort kommen wörtlich hinein**,
nicht als Zusammenfassung.

### 7.3 Der Journalblock

⭐ **Direkt anfügen, nicht als Nachtragsdatei** (`ARBEITSWEISE.md` Abschnitt 14,
Regel 3, Betreiberentscheidung 21.09.2026 aus TB-75):

- ans Ende von `docs/projektfuehrung/JOURNAL.md`, **vor** `## Wiederkehrende Lehren`
- **Blockbuchstabe gemessen**, nicht geraten: letzter Block plus eins
- Quellenzeile: `*Quelle: `docs/ERGEBNIS_TB-78_register_27_29.md`*`
- ⛔ nichts im Journal umschreiben, nur anfügen

### 7.4 Diese Auftragsdatei

Sie liegt bereits unter `docs/auftraege/` und ist mit Schritt 0 committet.

**Letzter Commit:** `TB-78: Ergebnisdokument und Journalblock`. **Pushen.**

---

## Abbruchkriterien

⛔ **Brich ab und melde, wenn:**

1. `numstat` bei einer Datei in der zweiten Spalte **nicht `0`** zeigt.
2. Der aus dem Code gelesene Wert von `RECENT_YEARS_ONLY` **nicht 10** ist.
3. Deine eigene Messung zu 29.2 **mehr als einen** `Kapitalpfad`-Treffer oder
   **mehr als null** `Startkapital`-Treffer findet.
4. `A8` in `docs/PRUEFPRINZIPIEN.md` bereits belegt ist.
5. Ein Sperrlisten-Hash sich geändert hat.
6. Die `numstat`-Prüfung an `UEBERGABE_2026-09-19.md` in Schritt 0 nicht
   `542  0` zeigt.

⭐ **Das Abbruchkriterium gilt für Fehlschläge, die den Gegenstand der Aufgabe
betreffen** (`T44.11`). Ein roter Test, der mit diesen Änderungen nichts zu tun
hat, ist kein Abbruchgrund — **er wird gemeldet**.

---

## In einfacher Sprache

**Was diese Aufgabe macht:** Sie schreibt vier Entscheidungen ins Regelwerk, die
seit heute Nachmittag feststehen, aber noch nirgends im Repo stehen.

**Erstens:** Der Prüfer, der die Regeln festlegt, darf vor dem grossen Lauf nicht
wissen, wie er ausgeht — keine Ergebniszahlen und auch keine Vermutungen. Das
wird Abschnitt 27.

**Zweitens:** Das Stichtagsdatum, ab dem gerechnet werden darf, ist jetzt gesetzt
— es kommt vom Tag, an dem der Datenbestand eingefroren wurde (19.09.2026), und
nicht vom Versiegeln. Damit lassen sich die vier Startdaten eintragen, die bisher
als Platzhalter dastanden.

**Drittens:** Ein Satz über die Anlaufzeit der Indikatoren war zwischen zwei
Antworten verlorengegangen. Er gilt weiter.

**Viertens:** Zwischen dem Stichtag und dem 1. Januar des ersten Auswertungsjahres
könnten Käufe liegen, die in keinem Auswertungsjahr zählen, aber das Startkapital
verändern. Die Regel dagegen wird festgeschrieben, **bevor** nachgemessen wird, ob
es solche Käufe gibt — sonst würde die Regel danach gewählt.

**Was sie ausdrücklich nicht macht:** Sie ändert keine Zeile Programmcode, sie
rührt keine gesperrte Datei an, und sie leitet den Faltenplan nicht ab — dafür
fehlt noch eine Antwort des Prüfers.
