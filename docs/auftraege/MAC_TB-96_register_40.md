# TB-96 — Registerabschnitt 40: Testannahmen, und die Entscheidung über die neun Handelslisten

**Sitzungstitel:** `TB-96` · **Angelegt:** 24.09.2026 vom steuernden Chat
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`
**Vorgänger:** TB-95 (`2938145`). **Aufwand:** hoch.
⛔ **Reine Registerarbeit: keine `.py` wird geändert, nichts wird gerechnet.**

---

## ⭐⭐ Worum es geht

TB-95 hat den Test grün gemacht und Fables Messbitte beantwortet. Fable hat in
**24a** geantwortet: Abschnitt 40 eintragen — und dazu **drei neue
Registertexte**, von denen einer die Arbeit der nächsten Woche bestimmt.

⭐ **Die Entscheidung, um die es geht:** Die neun Handelslisten gehen über eine
**Schwellenentscheidung** in den Faltenplan ein. Auf die Frage, ob dafür ein
Hash-Eintrag genügt, sagt Fable **nein** — mit einem Grund, der ins Register
gehört:

> Eine Schwellenentscheidung ist nicht „kleiner" als ein stetiger Einfluss, sie ist **unsichtbarer**.

⚠️ **Drei Berichtigungen an Fable hat er angenommen** (`benchmark.py` an zwei
statt drei Punkten · `beispieldaten.py` liest keine Tabelle · TB-94 → TB-96).
Er zählt sie ausdrücklich mit: *„dieselbe Klasse wie die sechs Rücknahmen der
ersten Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung
genannt."* Das gehört in den Registertext.

---

## ⛔ Was NICHT geschieht

| | |
|---|---|
| ⛔ | **Keine `.py`.** Nicht `test_vorregistrierung.py` (F4, die vier Literale ⇒ TB-97), nicht `sperrlistensonde.py` (⇒ TB-97), nicht `faltenplan.py`, nicht die Erzeuger |
| ⛔ | **Nichts gerechnet.** Keine Trade-Liste neu erzeugt, keine Faltenlänge abgeleitet (⇒ TB-98). Keine Datei in `ergebnisse/` geschrieben |
| ⛔ | **Kein neues Abbild.** Es hat sich keine Sperrlistendatei bewegt; das Abbild vom 23.09. (`2f23f76c…`) bleibt das gültige |
| ⛔ | **Kein alter Registersatz umgeschrieben.** Append-only, `numstat` zweite Spalte `0` |

---

## 0. Schritt 0

Arbeitsbaum committen. Er trägt vom steuernden Chat:

| | |
|---|---|
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-24a_…md` | neu |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_…md` | neu |
| `docs/projektfuehrung/ARBEITSWEISE.md` | geändert (22.5, 22.6, 22.7) |
| `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` | geändert (Schliess-Auslöser) |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | geändert |
| dieser Auftrag | neu |

`find .git -name '*.lock'` → keine. Danach Arbeitsbaum leer.

⚠️ **Freigabe prüfen:** `FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`
muss im Repo liegen. **Fehlt sie, brich ab.**

---

## Block A — Messen vor dem Schreiben

⚠️ Die Zahlen unten sind **Vormessung** des steuernden Chats. Nach `A8` misst du
jede nach; weicht eine ab, **gilt deine Messung**, und die Abweichung kommt ins
Ergebnisdokument.

| | zu prüfen | Vormessung |
|---|---|---|
| **A1** | Register endet bei Abschnitt **39.10**; nächster freier Abschnitt ist **40** | ja |
| **A2** | `test_vorregistrierung.py` | `73c9b837…`, Commit `9e2a071` |
| **A3** | Sperrlistendateien und beide Abbilder unverändert seit `2938145`; Sonde gegen `sperrliste_abbild_2026-09-23.json` | 0 Befunde, 15/15 gleich, (ii) `0`, Gesamtausgang `2` |
| **A4** | ⭐ **Fables Unsicherheit zu 5.4** — nennt 5.4 die Schwelle als Parameter? | ⭐ **Die Schwelle ist registriert:** „30 Trades je Jahr" steht als **Festlegung 7** in der Tabelle (Z. 62) und in **5.1 Nr. 6** (Z. 574). `faltenplan.py::faltenlaenge_jahre` liest sie als `rd.ZWEIJAHRES_SCHWELLE_TRADES`, **nicht** als Literal |
| **A5** | ⚠️ Was 5.4 **nicht** nennt: den **Parameterstand**, mit dem die Listen erzeugt wurden | 5.4 sagt nur, die Trades seien **„gefunden, nicht ausgeführt"**, weil das Positionslimit ein Rasterparameter ist. Welche übrigen Parameter am 13.09. galten, steht nirgends |
| **A6** | ⭐⭐ **Die neue Kopplung:** `G6` liest seit TB-95 den Registertext **5.1 Nr. 4** maschinell | Prüfe Muster und Fundstelle. ⚠️ **Wird der Wortlaut dieser Zeile je umformuliert, wird `G6` rot** — das ist eine Kopplung, die heute niemand sieht |

Beleg: `a_messungen.txt`.

⇒ **A4/A5 beantworten Fables Unsicherheit teilweise:** Die Schwelle ist
registriert, der Parameterstand der Erzeugung nicht. Genau das braucht die
Tatsachennotiz, die er verlangt.

---

## Block B — Der Nachtrag zu 39.8

⭐ Fable: *„40.5 als Nachtrag zu 39.8 — es setzt dessen Tatsache fort, und wer
39.8 liest, soll dort fündig werden."*

**Trage am Ende von 39.8 additiv ein** (⛔ nichts in 39.8 umschreiben):

- Die Antwort auf die Messbitte: `benchmark.py` → `fp.faltenplan` →
  `faltenlaenge_jahre` → `read_csv`; jede Liste genau einmal, nur im
  Hauptprozess; Inhalte gehen **über die Faltenlänge** ein.
- Die Störprobe in beide Richtungen: eine Zeile weg ⇒ bytegleich; zwei von drei
  weg ⇒ ein Bot kippt auf Zweijahresfalten, die anderen acht bleiben gleich.
- ⚠️ **Der methodische Satz, der über den Fall hinausgeht:** Die Störprobe, wie
  der Auftrag TB-95 sie vorschlug („eine Zeile entfernen genügt"), hätte **allein
  das falsche ‚nein'** ergeben.
- Herkunft: `78e2bc6`, 13.09.2026, TB-24; nicht im Snapshot, nicht auf der
  Sperrliste; im Register als Quelle genannt (5.4), ohne Hash.
- ⇒ **Verweis auf 40.6**, wo die Einordnung steht. ⛔ Nicht mit „Einordnung steht
  aus" enden.

---

## Block C — Abschnitt 40

Bauart wie 38/39: Fables Texte als **eingesetzte Blockzitate** (`diff` gegen die
Quelldatei mit `rc 0` als Beleg), darunter Grund und Tatsachennotizen, am Ende
die Marken.

### 40.1 Tatsachennotiz — der Test ist grün

`test_vorregistrierung.py` (`73c9b837…`, `9e2a071`) läuft am 23.09.2026
**165/165, rc 0**, 534 s. ⇒ **Tag-Vorbedingung „null rote Prüfungen, null
‚bekannt rot'" (21.9, A4) ist für diesen Test erfüllt.** Geändert nur diese eine
Datei; keine Prüfung entfallen, keine Ausnahme, keine Toleranz; kein
Sperrlistenhash bewegt; Sonde 0 Befunde.

### 40.2 `G6` — Jahre aus dem Register, Abdeckung gerechnet

Wie gebaut; und **gemessen vor der Änderung:** Die Sache hinter 5.1 Nr. 4 war
bei allen neun Bots erfüllt — rot war **nur die Formulierung**.

⚠️⚠️ **Die Kopplung ausdrücklich festhalten (A6):** `G6` liest den Wortlaut von
5.1 Nr. 4 maschinell. Findet es dort nicht genau einen Treffer, ist das Ergebnis
`None` und die Prüfung **rot**. ⇒ Wer diese Registerzeile umformuliert, bricht
den Test. **Marke bei 5.1 Nr. 4** (siehe unten) — sie ist der eigentliche Schutz.

### 40.3 `H3` — strikte Mehrheit statt fester Zahl

Gemessen vor der Änderung: Die vier alten Namen **trafen alle**; vier Nullen
verschieben den Median über neun Falten nicht. Kleinstes wirksames k = ⌈n/2⌉.
Die Probe beisst wieder; die Gegenprobe mit leerer Menge scheitert.

⭐ **Fables Einordnung, zeichengleich zitieren:** *„H3 griff nicht ins Leere,
sondern die **Zahl** war gealtert … dieselbe Klasse wie der Name, nur
unsichtbarer."*

### 40.4 Die weiteren Literale und `F4`

Liste wie im Ergebnisdokument TB-95 (Teil D, Teil F, `beispieldaten.py`
Z. 69/77), dazu **F4**: prüft mit `<=`, wo der Text „unter" sagt, und **hat nie
gebissen**. ⇒ Beides ist **beschlossen** (40.7/40.8), nicht erledigt.

### 40.5 ⛔ entfällt als eigener Unterabschnitt

Der Inhalt steht als Nachtrag in **39.8** (Block B). ⭐ **Diesen Satz
trotzdem als 40.5 schreiben**, mit Verweis — sonst sucht später jemand eine
Nummer, die es nicht gibt, und hält das Register für lückenhaft.

### 40.6 ⭐⭐ Die neun Handelslisten — Eingabedateien nach 23d

**Fables Registertext aus 24a Abschnitt 3 zeichengleich** einsetzen (beginnend
„Registertext, Ergänzung zu 23d („Eingabestand") und zu 5.4: Die neun
Trade-Listen …"), dazu:

- **sein Grund**, zeichengleich: die Schwellenentscheidung ist unsichtbarer,
  nicht kleiner; ein Hash-Eintrag hielte fest, **dass** die Listen so sind, nicht
  **ob** sie den Datenstand beschreiben, mit dem der Lauf rechnet;
- seine Antwort auf unseren Einwand: 23d verlangt **nicht**, dass eine Eingabe
  **im** Snapshot liegt, sondern dass sie **aus** Snapshot und registriertem Code
  **reproduzierbar** ist — die Listen sind Ergebnisdateien der neun Backtests,
  und TB-90 hat gezeigt, dass die byte-identisch reproduzieren;
- seine Einordnung unseres zweiten Umstands: *„Aus der Git-Historie
  reproduzierbar heisst, aus einem Datenstand, den der Lauf nicht verwendet"* —
  historischer Stand, kein Eingabestand;
- ⚠️ **kein Ergebnis:** Er verlangt die Ableitung, **ohne zu wissen**, ob sie
  33.2 bestätigt; und er braucht danach nur das Ob je Bot (1 oder 2), keine
  Trade-Zahlen (27.1).

**Tatsachennotiz zu 5.4 (aus A4/A5):** Die Schwelle „30 gefundene Trades je
vollem Kalenderjahr" ist **Festlegung 7** und steht in 5.1 Nr. 6; `faltenplan.py`
liest sie aus `registerdaten`, nicht als Literal. ⚠️ **Nicht registriert ist der
Parameterstand, mit dem die Listen am 13.09.2026 erzeugt wurden.** 5.4 sagt nur,
die Trades seien „gefunden, nicht ausgeführt", weil das Positionslimit ein
Rasterparameter ist. ⇒ Der Parameterstand der **Neu**-Erzeugung gehört nach
Fables Unsicherheit als Tatsachennotiz zu 5.4, sonst ist die Ableitung nicht
reproduzierbar. ⛔ Der **Regeltext** von 5.4 bleibt unverändert.

**Folge für den Plan:** ⭐ **Plan-Punkt 7 (Abbild des Faltenplans, 33.3, und die
Faltenplan-Sonde) rückt vor** — es ist die Wache, die diese Klasse fängt, und sie
fehlt (33.5). ⚠️ **Das Abbild wird NACH der Ableitung erzeugt, nicht vorher** —
sonst bildet es einen Stand ab, der gerade geprüft wird.

### 40.7 ⭐ Ergänzung zu 12 — jede Mutationsprobe hat eine Gegenprobe

**Fables Registertext aus 24a Abschnitt 5 zeichengleich** einsetzen, dazu sein
Grund (`A8`: eine Wache ist, was ein anderer gegenprüfen kann) und die Tatsache,
die ihn ausgelöst hat: **F4 hat drei Wochen „bestanden", ohne je gemessen zu
haben.** ⇒ Vor dem Tag wird die Gegenprobe für **alle acht** Mutationsproben
einmal geführt und als Tatsachennotiz festgehalten.

### 40.8 Beschlossen, nicht ausgeführt — was TB-97 und TB-98 tun

Tabelle, damit das Register sagt, was offen ist und warum:

| | Sache | Auftrag |
|---|---|---|
| (a) | `F4`: `<=` → `<`, Probe mit Mehrheit wie `H3`, Gegenprobe | TB-97 |
| (b) | Die vier Literale bauartgleich umstellen. ⭐ Fables Regel: Wo eine Prüfung eine konkrete Registeraussage prüft, liest sie die Jahre **maschinell aus dieser Stelle**; wo sie nur „irgendeine Selektionsfalte" braucht, nimmt sie sie **aus dem Plan**, ohne Literal. Für 4.4: Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan. ⚠️ *„Eine Prüfung, die an einem Beispieljahr hängt, prüft das Beispiel"* | TB-97 |
| (c) | Gegenproben für alle acht Mutationsproben, mit Notiz | TB-97 |
| (d) | Sonde: **getrennte Schlusszeilen** — „Pfad-Bestandteile: n geprüft, davon 0/1/2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". ⭐ Der Gesamtwert bleibt, wie 36.5 ihn definiert | TB-97 |
| (e) | ⚠️ **Befund:** Die Gruppe „bestimmt" steht **fest verdrahtet** in `sperrlistensonde.py`. Fable: *„Ein Literal in einer Wache — dieselbe Klasse wie G6, nur an der Sonde selbst."* Sie liest künftig **alle drei Gruppen aus dem Abbild**; Gegenprobe: Abbild mit erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn | TB-97 |
| (f) | Neun Listen auf dem Snapshot neu erzeugen, Sperrlistenpunkt, Faltenlänge nach 5.4 ableiten, gegen 33.2 vergleichen | TB-98 |
| (g) | Abbild des Faltenplans (33.3) und Faltenplan-Sonde — **nach** (f) | TB-100 |
| (h) | `messgroessen.json` auf dem Snapshot (23d/23e) | TB-101 |

⚠️ **(b) vor (f):** Teil D bricht mit `KeyError`, sobald der Bot Zweijahresfalten
bekommt — und **ob er das bekommt, weiss vor der Ableitung niemand.**

### 40.9 ⚠️ Drei Berichtigungen an Fable — angenommen

Alle drei zeichengleich mit seiner Annahme:

| | gemessen | Fables Annahme |
|---|---|---|
| (a) | `benchmark.py` an **zwei** Punkten (4 und 6) | „drei" — *„nicht gemessen"* |
| (b) | `beispieldaten.py` liest **keine** Benchmark-Tabelle | als Leserin **angenommen**, *„weil es die Testdaten erzeugt — nicht gemessen"* |
| (c) | TB-94 → **TB-96** für `messgroessen.json` | Plan vom Vormittag |

⭐ **Sein Satz dazu, zeichengleich:** *„Alle drei sind dieselbe Klasse wie die
sechs Rücknahmen der ersten Woche: eine Tatsache über den Bestand behauptet
statt als Voraussetzung genannt. Ich zähle sie mit."*

### 40.10 Was hier ausdrücklich NICHT getan wird

Tabelle wie 38.8/39.10.

### ⭐ Marken am alten Ort

| Marke | wohin |
|---|---|
| ⭐⭐ **`G6` liest diese Zeile maschinell — Wortlaut nicht ändern** | **5.1 Nr. 4** |
| Tag-Vorbedingung erfüllt (Test grün) | **21.9**, unter der Tabelle der Folgen |
| Listen sind Eingabedateien, werden neu erzeugt; Parameterstand fehlt | **5.4** |
| Faltenlänge wird neu abgeleitet und gegen diesen Text verglichen | **33.2** |
| Abbild rückt vor, wird nach der Ableitung erzeugt | **33.5** |
| Jede Mutationsprobe hat eine Gegenprobe | **12** |
| Gruppen kommen aus dem Abbild | **37.2** und **36.6** |
| Eingabestand: zweiter Anwendungsfall | **23d**-Abschnitt im Register (39.6, wo die Notiz „nicht eingetragen" steht) |
| Nachtrag | **39.8** (Block B) |

⚠️ **Setze keine Marke, deren Zielabschnitt du nicht gelesen hast.** Passt eine
nicht, lass sie weg und **melde, welche und warum**.

---

## Block D — Nachweise und Abgabe

| | |
|---|---|
| **D1** | ⭐⭐ `git --no-optional-locks log -1 --numstat -- docs/VORREGISTRIERUNG_neuselektion.md` → **zweite Spalte `0`**, `-`-Zeilen im Gesamtdiff **0**. Zeichengleich ins Ergebnisdokument |
| **D2** | Jedes Blockzitat mit `diff` gegen die Quelle, `rc 0`. Zahl der Zitate und Zahl der `rc 0` nennen |
| **D3** | Hashes vorher/nachher: ⛔ **keine Datei ausserhalb von `docs/` darf sich geändert haben.** Sonde gegen `sperrliste_abbild_2026-09-23.json` vorher und nachher: unverändert |
| **D4** | Belege nach `docs/belege/TB-96/`: `a_messungen.txt`, `d1_numstat.txt`, `d2_zitate.txt`, `d3_hashes.txt`, `d3_sonde.txt` |
| **D5** | Ergebnisdokument `docs/ERGEBNIS_TB-96_register_40.md`, Bauart wie TB-94, mit „In einfacher Sprache" und „Für die Folgesitzung vorbereitet" |
| **D6** | Journalblock |

**Commits:** (1) Schritt 0 · (2) ⭐ **Block B und C in EINEM Commit** · (3) Abgabe.

---

## ⚠️ Abbruchkriterien

1. Fables Antwort 24a liegt nicht im Repo.
2. Register endet nicht bei 39.10 — dann hat jemand dazwischen geschrieben.
3. Ein gemessener Hash weicht von der Vormessung ab → **deine Messung gilt**,
   eintragen und aufschreiben, nicht fragen.
4. `numstat` zweite Spalte ≠ 0 nach einem Versuch, es zu richten.
5. Eine Datei ausserhalb von `docs/` hat sich geändert.
6. ⚠️ **A6 misslingt** — `G6` liest 5.1 Nr. 4 nicht so, wie der Auftrag es
   annimmt. Dann stimmt 40.2 nicht: melden, 40.2 auf das Gemessene stellen.

---

## In einfacher Sprache

Der Verfahrensprüfer hat geantwortet, und seine Antwort bringt drei neue Regeln
ins Regelwerk — dieser Auftrag trägt sie ein und schreibt sonst nichts um.

**Die wichtigste Entscheidung:** Neun alte Handelslisten bestimmen, ob ein Bot
ein- oder zweijährige Zeitabschnitte bekommt. Wir hatten gefragt, ob es reicht,
ihre Prüfsumme festzuhalten. Die Antwort ist nein, und der Grund ist gut: Eine
Ja-Nein-Schwelle ist nicht harmloser als ein stetiger Einfluss, sondern nur
schwerer zu sehen. Eine Prüfsumme würde bezeugen, **dass** die Listen so sind —
nicht, **ob** sie zum eingefrorenen Datenbestand passen. Sie werden deshalb aus
diesem Bestand neu erzeugt, geschützt, und die Zeitabschnittslänge wird danach
neu abgeleitet und mit dem Regelwerk verglichen. Ob sich dabei etwas ändert,
weiss niemand — und genau deshalb steht die Regel fest, **bevor** gerechnet wird.

**Die zweite Regel:** Jede Gegenprobe im Prüfprogramm braucht selbst eine
Gegenprobe. Anlass ist eine Prüfung, die drei Wochen lang „bestanden" hat,
ohne je etwas gemessen zu haben — ein falsches Vergleichszeichen.

**Und ein Fund, den dieser Auftrag festhält, weil ihn sonst niemand sieht:** Das
Prüfprogramm liest seit gestern eine Zeile des Regelwerks wörtlich. Wer diese
Zeile umformuliert — auch gut gemeint —, macht das Prüfprogramm rot. Der Auftrag
setzt deshalb einen Vermerk direkt an diese Zeile.
