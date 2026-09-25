# FABLE_ANTWORT 2026-09-25b — Zwischenablagen sind eine vierte Klasse; Quelltext ist Code, aber nur, wo die Startprüfung ihn bindet; der gerechnete Plan bekommt eine registrierte Abbildung statt zu schrumpfen; `mindesttraining` und `embargo_nach_falten` gehen mit; der Laufbereich ist die Vereinigung aller Lauf-Typen — und ein „keine Nebenbedingung", das ich nicht stehen lasse

*Bezug: `FABLE_ANFRAGE_2026-09-25b_laufbereich_gemessen_fuenf_fragen.md`. Ein Ergebnis, vier Messantworten, fünf Fragen. Reihenfolge wie die Anfrage; dazwischen ein Einspruch zu Messung (4), der vor TB-106 geklärt gehört.*

**Leseprotokoll dieses Chats, Stand jetzt:** wie 25a; dazu ANFRAGE 25b (Anhang). Nichts weiter gelesen. Ergebnisgrössen nach 27.1: keine — `trades_je_jahr` ist mir als Feldname begegnet, ohne Wert.

---

## 1. TB-104 — Kenntnisnahme

Leser auf dem Resolver; Ersatzwurzeln heissen Messwerkzeug und brechen unter dem Modus mit 2 ab, **bevor** gelesen wird — das ist 24d Abschnitt 3 so, wie ich es meinte, und die Reihenfolge (erst 2, dann lesen) ist der Teil, der zählt. Das Universum aus `CONFIG_DIR` plus `registerdaten.UNIVERSUM`, eine Namensliste. Die drei Felder draussen, 9 + 9 + 77 Vorkommen weniger und sonst zeichengleich, Faltengrenzen gleich; `G8` und `G9` angepasst, nicht gelöscht, mit `G8M`. Benchmark-Tabelle im Modus zweimal `64fb2912…` — erwartet, weil die Felder ungelesen waren, und trotzdem die Messung, die den Satz erst wahr macht. Neues Abbild `cb4eb1b4…`, alte Punkte 2/4/6 planmässig. Nachweis bleibt 2 wegen der zwei Eingaben — richtig. Und `regimewache.pruefe_einbau()` **0 von 3**: die offene Voraussetzung aus 11.1, jetzt gemessen statt vermutet; TB-105 (b) schliesst sie.

**Ein Punkt zur Abnahme von TB-105, der Verfahren ist, nicht Handwerk:** Ihr habt das `makedirs` im **frischen Klon** gefunden, weil im Repo alle 18 Ordner existieren und `makedirs` dort nichts tut. Dasselbe gilt für jede Schreibziel-Prüfung: Ein Schreibzugriff, dessen Ziel schon existiert, ist unsichtbar. Die Abnahme „Klasse (iii) leer" wird deshalb **in einer Umgebung gemessen, in der die Ziele fehlen** (frischer Klon oder Wegwerf-Wurzel mit dem Snapshot daneben) — sonst misst sie den Zustand des Repos, nicht das Verhalten des Codes. Das gehört als Satz in die Klasse (iii) (Abschnitt 3 (1) unten).

---

## 2. Die vier Messungen

**(1) `datenstand(daten_dir=None)`** — angenommen; `herkunft.py` bleibt zu, der Erzeuger ruft `datenstand(paths.DATA_DIR)` und `register()` selbst, nicht `block()` — das ist zugleich 37.4 (Feld `teile` über `register()`). *Was ihr mit „heute gleich, keine Eigenschaft des Codes" benennt, ist TB-102 in Kleinformat und gehört als Tatsachennotiz zu 37.4.* **Eine Lücke bleibt, und sie ist zu messen, nicht anzunehmen:** Das append-only-Protokoll (10.1: `herkunft_protokoll.jsonl`, Kettenhash; 38.3: „entsteht mit dem Erzeuger") wird über `anhaengen()` geschrieben. *[Messbitte, nur das Ob: baut `anhaengen()` seinen Eintrag selbst über `block()` — dann ruft es `datenstand()` ohne Argument und ist unter dem Modus unbrauchbar — oder nimmt es einen fertigen Block entgegen?]* Im ersten Fall gilt 25a: `herkunft.py` wird für genau diese Stelle planmässig geöffnet (Punkt 11/12, 37.3), weil die Alternative — die Kette im Erzeuger nachzubauen — ein zweiter Ort für dieselbe Funktion wäre.

**(2) `makedirs` beim Import** — Klasse (iii), beauftragt; und `bot_lauf.py` dazu. Angenommen. Abnahme wie in Abschnitt 1.

**(3) Der Stichtag** — meine Voraussetzung traf wörtlich nicht zu; sie war als solche gekennzeichnet, ihr habt sie gemessen, das Ergebnis ist gleich. So soll der Mechanismus laufen; ich zähle das nicht als Fall. **Euer Vorschlag ist richtig, mit einer Änderung an der Herkunft der Zahl:** Der Stichtag ist kein Literal, sondern **der Go-Live-Schnitt aus 5.2, ausschliesslich** — das ist das Verfahren von TB-40/16.1.1, und es ist registriert.

> **Präzisierung zu 25a (B), Teil (2):** Die geladene Menge je Bot wird **am Stichtag Go-Live-Schnitt (5.2), ausschliesslich** ermittelt — jede Kursreihe auf den Stichtag gekürzt, Loader wie in TB-40 — und gegen die Bestätigungsspalte von 16.1.1 verglichen. Ein Trockenlauf am Datenende bleibt zulässig als Nachweis „kein Fallback"; die Mengenprüfung gegen das Register läuft am Stichtag. Tatsachennotiz: am Stand `63e4b6c8…` ergeben beide Stichtage bei 9/9 Bots dieselbe Menge (TB-104).

*Quelle des Grundes:* 16.1.1 wurde so gemessen; eine Prüfung gegen das Register nimmt das Verfahren des Registers. Kein Ergebnis.

**(4) Ersatzwerte in `auswertung.py` — hier lege ich Einspruch ein, bevor TB-106 läuft.** Ihr schreibt, `_bedingung` liefere `None` mit der *„registrierten Bedeutung ‚keine Nebenbedingung'"*. **Ich finde im Register keinen Zustand „keine Nebenbedingung".** Abschnitt 4 kennt die Bedingung für jeden Bot; 5.3 sagt, `auswertung.py` *weigert sich*, einen Bot mit Platzhalter-Plan auszuwerten — *„es gibt dann keine Zahl, die so tut, als gäbe es eine"*; 7 (b) kennt den Fall „kein Satz besteht", nicht den Fall „es gibt nichts zu bestehen". Ein Pfad, auf dem ein Bot **ohne** Nebenbedingung bewertet wird, ist der VH-Fehler aus 23.2 in seiner reinsten Form: Jeder Satz besteht. Zwei Lesarten, und ihr seht den Code, ich nicht:

| | Lesart | Folge |
|---|---|---|
| (α) | `None` ist der interne Weg, den **Plateau-Gewinner über alle Zellen ohne Zulässigkeitsfilter** zu rechnen — der Berichtsfall aus 7 (b), Markierung „nicht zulässig" | registriert; dann heisst der Zustand im Code „Bericht nach 7 (b)", nicht „keine Nebenbedingung" — Tatsachennotiz, sonst nichts |
| (β) | `None` bewirkt, dass ein Bot **bewertet** wird, als hätte er keine Drawdown-Bedingung | nicht registriert; ein Fallback der schwersten Art (Schwelle weg statt Schwelle ersetzt); unter dem Modus **2**, wie die anderen — und zwar zuerst |

*[Messbitte, nur das Ob: Welche der beiden ist es — geht ein `None` aus `_bedingung` in `zulaessigkeit`/`bestanden` ein, oder nur in den Berichtszweig?]* Bis dahin steht (4) für mich nicht als „kein Ersatzwert", sondern als offen. Dass die Stelle mit registrierten Eingaben unerreichbar ist, ändert nichts — das war bei der Fünferliste auch so, bis jemand den Modus einschaltete.

---

## 3. Die fünf Fragen

### (1) Zwischenablagen — eine vierte Klasse, mit drei Bedingungen; „nie entfernt" ist Befund 1

Eure Neigung trifft, aber sie lässt die Leseseite offen: Der Elternprozess **liest** die Datei, die das Kind geschrieben hat. Im Lese-Audit ist das ein Zugriff ausserhalb des Snapshots — nach (i) ein Befund, obwohl es keiner ist. Deshalb braucht es die Klasse, nicht nur die Erlaubnis.

> **Ergänzung zu 25a (A) — Klasse (iv), Zwischenablage:** Eine Datei, die derselbe Lauf schreibt **und** liest, ist Zwischenablage. Sie ist zulässig, wenn (1) ihr Ordner je Lauf neu und eindeutig angelegt wird (`mkdtemp`) **oder** unter `--ziel` liegt, (2) kein Prozess ausserhalb des Laufs sie liest — im Audit erscheint jeder Lesezugriff auf sie mit dem Schreibzugriff desselben Laufs daneben — und (3) sie am Ende des Laufs entfernt ist **oder** ihr Pfad im Beleg steht. Fehlt eine der drei, ist sie Befund 1 der Schreibziele-Sonde. Klasse (iii) („Schreibziele leer") heisst damit: kein Schreibzugriff ausser `--ziel`, Belegpfaden und Klasse (iv). Gemessen wird (iii) und (iv) in einer Umgebung, in der die Ziele fehlen (Abschnitt 1).

*Quelle des Grundes:* 5e — der Audit soll zeigen, woraus der Lauf gelesen hat; eine Zwischenablage, die er selbst geschrieben hat, ist keine Eingabe, und der Audit muss das **sehen**, nicht wissen. Warum (1): Ein deterministischer Pfad in `$TMPDIR` könnte vom nächsten Lauf gelesen werden — dann wäre eine Zwischenablage eine unregistrierte Eingabe; `mkdtemp` schliesst das aus. Warum (3): Elf Ordner je Lauf, die niemand entfernt, sind kein Verfahrensfehler, aber ein Bestand, den niemand kennt — und „nie entfernt" heisst heute: **Befund 1**, bis das Aufräumen eingebaut ist (Handwerk, klein). Kein Ergebnis.

### (2) Quelltext als Daten — Klasse „Code", aber nur, wo die Startprüfung ihn bindet

Eure Neigung ist richtig, und sie hat eine Bedingung, die ihr mitgenannt habt, ohne sie zu prüfen: *„über den Commit und die Startprüfung (sauberer Arbeitsbaum über `strategies/`) gebunden."* Genau das ist das Kriterium.

> **Ergänzung zu 25a (A) — Klasse „Code":** Ein Lesezugriff auf eine Datei unter der Codewurzel ist Klasse „Code" und zulässig, wenn die Datei in einem Pfad liegt, den die Startprüfung (19) über `HEAD` und sauberen Arbeitsbaum bindet. Eine Datei unter der Codewurzel **ausserhalb** dieser Pfade ist weder Code noch Eingabe — sie ist ungebunden und ein Befund 1. Ein Leser, der Werte per Muster aus Quelltext liest, endet mit 2, wenn das Muster nicht genau einmal trifft; ein Ersatzwert ist ausgeschlossen.

*Quelle des Grundes:* 19 (Codeherkunft: `HEAD`, sauberer Baum — das ist, was „Code" registriert), 16.7 (b) (die `MIN_HISTORY_*`-Werte sind registriert und leben im Bot-Code, `T56b.6`: keine Kopie). Kein Ergebnis.

**Und der Befund, den diese Frage erst sichtbar macht:** 19 nennt als `ARBEITSBAUM_PFADE` **`shared/`, `strategies/` und `requirements.lock`** — nicht `research/`, nicht `notifications/`. Der gemessene Laufbereich hat 11 Module aus `research/` und eines aus `notifications/`. Ein veränderter, uncommitteter `benchmark.py` oder `faltenplan.py` würde die Startprüfung heute **nicht** aufhalten. *[Voraussetzung, zu messen: dass 19 den Stand noch beschreibt — die Tatsachennotiz dort ist vom 19.09.]*

> **Ergänzung zu 19 (Registertext 5e, Codeherkunft):** Die Sauberkeitsprüfung des Arbeitsbaums erstreckt sich auf **jeden Pfad des Laufbereichs** (Abschnitt 5 unten), nicht nur auf `shared/`, `strategies/` und `requirements.lock`; `data/` bleibt ausgenommen (19, aus dem dort genannten Grund). Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert.

*Quelle des Grundes:* 19 selbst — „Liegen Aufrufer und Resolver in verschiedenen Bäumen, beschreibt kein einzelner Commit den gelaufenen Code"; das gilt für jedes Modul, das läuft. Kein Ergebnis. Zu den neun Optimierern selbst: sie liegen unter `strategies/`, sind also heute schon gebunden — eure Lesart „Code" gilt für sie ohne Vorbehalt. *[Messbitte, nur das Ob: endet `_min_history` mit 2, wenn das Muster in einer Datei nicht genau einmal trifft?]*

### (3) Der gerechnete Plan schrumpft nicht — die Sonde vergleicht eine registrierte Abbildung, und die Feldliste des Plans wird selbst Registertext

Ihr habt recht, und meine Präzisierung aus 25a war zu breit. Der Plan trägt seit 25.3 und 32.1 **absichtlich** Herleitungsgrössen — `erste_falte_4a`, `erste_falte_trockenlauf_H`, `horizontbeginn`, `erste_falte_4a_warm_ab` —, *„damit im Plan steht, warum er dort beginnt"*. Die sind keine Verfahren-A-Felder, sondern das Gegenteil: die Spur der registrierten Regel. Ein Plan ohne sie wäre weniger prüfbar, nicht mehr.

> **Berichtigung zu 25a (1), Präzisierung zu 33.3/35.4:** „Der Plan … trägt keine Grösse, die 33.2/33.3 nicht kennt" lies: **„Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die das Verfahren nicht kennt** (Trainingsgrenzen, Embargo, Purge, Mindesttraining). Die Faltenplan-Sonde vergleicht den Plan mit dem Abbild über eine **registrierte Abbildung**: je Feld des Abbilds (33.3) der Planschlüssel, aus dem es gebildet wird. Die **Feldliste des gerechneten Plans** — jeder Schlüssel je Plan und je Falte, mit der Registerstelle, die ihn begründet — ist Registertext; ein Schlüssel im Plan, der dort nicht steht, ist ein Befund der Sonde, ein fehlender ebenso."

*Quelle des Grundes:* 33.3 (ein Abbild trägt genau die Grössen seines Abschnitts — das Abbild, nicht der Plan), 25.3/32.1 (der Plan trägt seine Herleitung), 33.1 (Felder, die ein anderes Verfahren beschreiben, dürfen nicht drin sein). Kein Ergebnis. **Zu `G8` heute:** Die Feldliste „aus dem Code" ist eine Kopie des Codes im Test — als benannter Zwischenstand zulässig, wie ihr es benannt habt; sie wandert mit Register 41/42 in den Registertext. Wie der Test dann an den Registertext gebunden wird (Parser wie `G6`, oder Literal mit Test gegen das Register wie in 32.5 (c)), ist die offene Frage aus 32.5 und Handwerk; ich entscheide sie nicht mit.

### (4) `mindesttraining_jahre`, `embargo_nach_falten`, die Berichtszeile — dieselbe Berichtigung, mit einer Messung davor

Ja, alle drei. 23.5 hat sie schon benannt (*„Beides ist der ersetzte Verfahren-A-Satz (TB-65)"*, `T56b.6`), und 15.1 sagt: **kein Mindesttraining**, 2c: **kein Embargo zwischen Selektionsfalten**. Sie gehören zur Berichtigung Code an 2c/4a wie die drei Felder — und im ERZEUGT-Block von Abschnitt 3 steht die Zeile „Mindesttraining vor der ersten Falte: 4 Jahre" bis heute, was mit dem nächsten Erzeugen des Blocks von selbst verschwindet (39.1: der Block ist noch nicht neu erzeugt).

**Vorher eine Messung, die ihr angeboten habt, und die ich brauche:** *[Voraussetzung, zu messen: geht `MINDESTTRAINING_JAHRE` heute noch in `erste_falte_4a` ein?]* Wenn ja, ist das kein totes Feld, sondern eine Verfahren-A-Regel im Rechenpfad — dann ist die Entfernung eine Berichtigung des Codes an 15.1/25.3 mit gemessener Wirkung auf die erste Falte (Bauart 24.3: die Regel steht, die Wirkung wird berichtet, sie entscheidet nichts). Wenn nein, sind es zwei tote Felder und eine tote Zeile; sie gehen mit derselben Berichtigung.

**Zur Konstante in `registerdaten.py`** (Sperrlistenpunkt 1, Abschnitt-0-eingefroren): Das Feld und die Zeile gehen jetzt; die Konstante selbst bleibt, bis Punkt 1 ohnehin planmässig geöffnet wird (40.8 (h), die zwölf Rasterachsen) — bis dahin Tatsachennotiz „tot, kein Leser". *Ein Wert, der nichts mehr steuert, aber einen Namen trägt, der eine Regel verspricht, ist die K1h-Klasse; sie wird mit dem nächsten geplanten Zugriff auf die Datei bereinigt, nicht mit einem eigenen.*

### (5) `messgroessen.py` gehört dazu — der Laufbereich ist die Vereinigung aller Lauf-Typen, und die Liste der Lauf-Typen ist registriert

Ja. Meine Aufzählung in 25a war beispielhaft und damit unvollständig — die 80 sind die drei gemessenen Lauf-Typen, nicht der Laufbereich.

> **Berichtigung zu 25a Abschnitt 4 (Laufbereich):** Der Laufbereich ist die **Vereinigung** über alle Lauf-Typen des Selektionsmodus. Lauf-Typen sind: der Trockenlauf aller neun Bots; jeder Erzeuger einer registrierten Eingabedatei (`messgroessen.py`, der Listen-Erzeuger auf dem Signalpfad, der Erzeuger der Benchmark-Tabelle mit `faltenplan.py` und seinen Kindprozessen, der Abbild-Erzeuger); `auswertung.py` samt Laufwrapper; die Sonden, soweit sie im Modus laufen. Die Liste der Lauf-Typen ist Registertext und am Tag abschliessend; der Laufbereich wird **am Tag-Commit** über alle Lauf-Typen gemessen (Import-Audit), und das Rückfall-Inventar darüber ist am Tag leer.

*Quelle des Grundes:* 5e und die Messung, dass `messgroessen.py` ein Modus-Lauf ist (TB-103) — was unter dem Modus läuft, ist Laufbereich, gleich ob ich es aufgezählt habe. Kein Ergebnis. **Folge:** `herkunft.py` und `shared/regimewache.py` treten mit dem Erzeuger bzw. mit TB-105 (b) ein; die 80 sind ein Zwischenstand mit Datum. Und (c) — die `exit()`-Stellen in `__main__` — gehört dazu, sobald ein Modus-Lauf ein Bot-Skript direkt startet; ob der Listen-Erzeuger das tut (Import oder Kindprozess), ist Handwerk, aber die Regel gilt so oder so, weil der Laufbereich am Tag gemessen wird, nicht heute.

---

## 4. Was auf Register 41/42 kommt, zusätzlich zu 24c/24d/25a

| | Eintrag |
|---|---|
| a | Klasse (iv) Zwischenablage mit drei Bedingungen; Messumgebung für (iii)/(iv) (3 (1), Abschnitt 1) |
| b | Klasse „Code" mit Bindung an die Startprüfung; Ergänzung zu 19: Sauberkeit über den Laufbereich (3 (2)) |
| c | Berichtigung zu 25a (1): Plan schrumpft nicht; registrierte Abbildung; Feldliste des Plans als Registertext (3 (3)) |
| d | `mindesttraining_jahre`, `embargo_nach_falten`, Berichtszeile: Verfahren-A-Reste, dieselbe Berichtigung; Konstante in `registerdaten.py` tot bis 40.8 (h) (3 (4)) |
| e | Berichtigung zu 25a Abschnitt 4: Laufbereich = Vereinigung; Lauf-Typen registriert; Messung am Tag-Commit (3 (5)) |
| f | Präzisierung zu 25a (B) (2): Stichtag = Go-Live-Schnitt (5.2) (2 (3)) |
| g | Tatsachennotizen: TB-104 (Leser, Felder, Abbild `cb4eb1b4…`, Benchmark im Modus, Umgebungsliste, Schreibziel `manual_close.py`), `datenstand()`-Signatur und `block()` (zu 37.4), `regimewache` 0/3 (zu 11.1), die 80 Module mit Datum |
| h | offen bis zur Messung: `_bedingung` `None` (α oder β) — **vor TB-106**; `anhaengen()`; `_min_history` bei Fehltreffer; `MINDESTTRAINING_JAHRE` in `erste_falte_4a` |

---

**Kurz:** TB-104 angenommen; die Abnahme von Schreibzielen misst dort, wo die Ziele fehlen. Vier Messungen: `herkunft.py` bleibt zu, aber `anhaengen()` ist zu messen; `makedirs` ist (iii); der Stichtag wird der Go-Live-Schnitt aus 5.2, mein Vorschlag war als Voraussetzung gekennzeichnet und ist so behandelt worden; **und „keine Nebenbedingung" lasse ich nicht stehen** — ich finde den Zustand im Register nicht, und wenn `None` einen Bot ohne Drawdown-Bedingung bewertet, ist es der VH-Fehler als Fallback: vor TB-106 klären. Fünf Fragen: Zwischenablagen sind Klasse (iv) mit drei Bedingungen, „nie entfernt" ist Befund 1; Quelltext ist Code, wo die Startprüfung ihn bindet — und die bindet `research/` heute nicht, das ist ein Befund an 19; der Plan schrumpft nicht, die Sonde vergleicht eine registrierte Abbildung, die Feldliste des Plans wird Registertext; `mindesttraining`/`embargo_nach_falten` gehen mit, vorher messen, ob `MINDESTTRAINING_JAHRE` noch rechnet; `messgroessen.py` gehört zum Laufbereich, der die Vereinigung aller registrierten Lauf-Typen ist und am Tag-Commit gemessen wird.

**Unsicher:** (1) ob 19 den heutigen Stand von `ARBEITSBAUM_PFADE` noch beschreibt; (2) ob `anhaengen()` über `block()` geht; (3) welche Lesart bei `_bedingung` gilt; (4) ob `MINDESTTRAINING_JAHRE` in `erste_falte_4a` eingeht.

---

## In einfacher Sprache

Der Umbau der Leseprogramme ist durch, die alten Felder sind raus, die Vergleichstabelle ist Byte für Byte gleich geblieben, ein neues Abbild ist gezogen. Angenommen.

Ein Einspruch: Ihr habt eine Stelle als harmlos eingestuft, an der ein Bot ohne Verlustgrenze bewertet würde, wenn die Grenze fehlt — ihr nennt das „registrierte Bedeutung". Ich finde diese Bedeutung im Regelwerk nicht. Entweder ist es der bekannte Berichtsfall, dann heisst es künftig so; oder es ist die gefährlichste Notlösung im ganzen Code, und sie kommt als Erste weg. Das ist vor dem nächsten Auftrag zu klären.

Zu den fünf Fragen: Zwischendateien sind erlaubt, wenn sie je Lauf neu angelegt, nur vom Lauf selbst gelesen und am Ende entfernt werden — heute bleiben sie liegen, das gilt bis zur Behebung als Befund. Programmtext darf als Programmtext gelesen werden, aber nur dort, wo die Startprüfung ihn bindet — und die bindet einen Teil des Laufbereichs heute nicht, das ist ein neuer Befund. Der Zeitplan behält seine Herleitungsfelder; statt ihn zu beschneiden, wird die Zuordnung zum Abbild ins Regelwerk geschrieben. Zwei weitere Reste des alten Verfahrens gehen denselben Weg wie die drei Felder. Und das Messprogramm gehört zum geschützten Bereich, der am Ende über alle Lauf-Arten gemessen wird, nicht über drei.
