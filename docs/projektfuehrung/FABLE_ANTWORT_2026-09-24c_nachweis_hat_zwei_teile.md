# FABLE_ANTWORT 2026-09-24c — Ein Nachweis hat zwei Teile, und „bytegleich" ist nur einer; ein Weg statt dreier Anordnungen; die Haltedauern kommen aus denselben gefundenen Trades wie die Faltenlänge — und die Mischung war nicht beabsichtigt

*Bezug: `FABLE_ANFRAGE_2026-09-24e_richtiges_ergebnis_falscher_ort.md` (24.09., 22:00). Der Anhang zu dieser Nachricht war noch einmal 24c — die ist in 24b Teil B beantwortet; ich nehme an, gemeint war 24e, und die liegt in der Ablage. Kenntnisnahme zu 0; drei Entscheidungen; eine Präzisierung meines Nachweisbegriffs aus 23e.*

---

## 0. Kenntnisnahme

**5.4 sagt „gefundene" im Wortlaut, mit Begründung** — meine Unsicherheit aus 24b ist ausgeräumt, und A3 (Signalpfad) steht auf Registertext. Der Begründungssatz in 5.4 („eine Faltenlänge, die vom Positionslimit abhinge, wäre keine Festlegung vor dem Lauf") ist zugleich der Massstab für Frage 3 — ihr habt ihn richtig dorthin gelegt.

**Zu Befund 1:** Das ist der wichtigste Einzelbefund über meine eigene Regel: 23e verlangte „im Selektionsmodus, bytegleich" und hätte mit `diff` allein einen **erfüllten** Nachweis erzeugt, der null Dateien aus dem Snapshot liest. Dass TB-102 den Lesehaken mitlaufen liess, obwohl 23e ihn nicht verlangt hat, ist der Grund, warum wir es wissen. Ich habe „im Modus" gesagt und gemeint „aus dem Snapshot" — und nicht bedacht, dass ein Programm den Modus schlicht nicht kennen kann.

## 1. Präzisierung zu 23e — der Nachweis hat zwei Teile

> **Registertext, Ersatz für den Nachweisbegriff aus 23e (Eingabestand):** Ein Reproduzierbarkeitsnachweis besteht aus **zwei** Teilen, und beide sind Pflicht: **(a)** dem Ergebnisvergleich — die erzeugte Datei ist bytegleich zur eingefrorenen; **(b)** dem **Leseprotokoll** — alle Lesezugriffe des Laufs auf Kurs-, Universums- und Ergebnisdateien liegen innerhalb `snapshots/<hash>/` oder auf registrierten Eingabedateien, **null** im Repo-Arbeitsstand (`data/`, `config/`, `ergebnisse/` ausserhalb der registrierten Pfade). Fehlt (b) oder zeigt es einen Zugriff ausserhalb, ist der Nachweis **2**, gleich was (a) sagt. „Bytegleich" ohne Leseprotokoll ist kein Nachweis, sondern ein Zufall, der heute stimmt.

*Quelle des Grundes:* 5e (der Lauf belegt, woraus er nachweislich gelesen hat) und TB-98 Befund 1 / TB-102 Lesart 2: richtiges Ergebnis, falscher Ort, keine Warnzeile. Kein Ergebnis.

*Für alle bisherigen Nachweise heisst das:* TB-91 A1b (`benchmark.py` im Modus, zweimal bytegleich) — hatte es ein Leseprotokoll? TB-95 hat später mit Lesehaken gemessen, dass `benchmark.py` 222 + 2 Dateien aus dem Snapshot liest; wenn diese Messung derselbe Lauf-Typ war, gilt A1b als vollständig; wenn nicht, ist das Leseprotokoll für die Benchmark-Tabelle einmal nachzuholen. **Nur das Ob.** Der TB-93/TB-102-Nachweis für `messgroessen.json` ist nach dieser Regel **2** — nicht geführt.

## 2. Frage (1) — welcher Modus: einer, der Resolver

**Entscheidung:** `messgroessen.py` wird auf `shared/paths.py` umgestellt — Kursdaten über `DATA_DIR`, Universumsdateien über `CONFIG_DIR`, beides unter dem Modus aus dem Snapshot (mit dem Resolver-Beschluss aus 24b A2). `TB30A_BASE_DIR` bleibt, was es ist — Ersatz der Repo-Wurzel für Mutationsproben —, aber es ist **kein** Weg zum Snapshot und wird als solcher nicht mehr genannt.

> **Registertext, Ergänzung zu 5a/5e:** Jedes Modul des Laufbereichs, das Kursdaten oder Universumsdateien liest, bezieht seine Pfade über den Resolver (`shared/paths.py`, `get_strategy_paths()`). Eine eigene Pfadlogik für diese Dateien ist ein Befund der Lesequellen-Sonde (1). Es gibt **eine** Anordnung, die der Snapshot vorgibt (Kurse flach, Universum unter `config/`), und der Resolver ist der einzige Ort, der sie kennt.

*Quelle des Grundes:* `strategy_paths.py` selbst („Hier steht KEIN zweiter Resolver") und 24b A2. Drei Anordnungen sind zwei zu viel; und ein Programm, das den Modus nicht kennt, kann ihn nicht einhalten. Kein Ergebnis.

*Folge:* Der Nachweis für `messgroessen.json` wird **nach** der Umstellung geführt — beide Teile. Vorher beweist nichts etwas, ihr sagt es richtig.

## 3. Frage (2) — `haltedauern_je_bot.csv`: Eingabedatei, ja; aber sie wird nicht mehr aus ausgeführten Trades gebaut

Sie ist Eingabe einer Herleitung von Registertext (über `messgroessen.json` → `purge_tage` → Purge/Embargo/Trainingsende; → Donchian-Untergrenze zweier Bots, eine Rasterachse). Also Eingabedatei nach 23d: Eingabestand registriert, reproduzierbar aus Snapshot und Code, Erzeuger unter 36.1 — und ihr heutiger Erzeuger (`tb24_haltedauern/auswertung.py`) schreibt fest ohne Sperre, ihre Quelle sind **ausgeführte** Trades, die seit TB-26 nicht mehr reproduzierbar erzeugt werden können (TB-98 Befund 2).

**Aber die Antwort auf Frage 2 hängt an Frage 3**, und dort entscheidet sich, dass diese Datei in ihrer heutigen Form gar nicht mehr gebraucht wird.

## 4. Frage (3) — die Mischung: nicht beabsichtigt, und sie wird aufgelöst

**Der Grundsatz aus 5.4** lautet: Eine Festlegung vor dem Lauf darf nicht von einem Wert abhängen, der im Lauf ein Rasterparameter ist — sonst hinge sie am Ausgang. 5.4 wendet ihn auf die Faltenlänge an und schliesst deshalb das Positionslimit aus (gefundene statt ausgeführte Trades). **Purge, Embargo, Trainingsende und die Donchian-Untergrenze ruhen auf ausgeführten Trades — also auf demselben Positionslimit.** Das ist derselbe Grundsatz, an drei Stellen nicht angewandt. Ich sehe keinen Grund, der die drei Stellen ausnimmt, und das Register nennt keinen; also gilt er.

**Zwei Dinge sind zu trennen, und ich trenne sie ausdrücklich:**

**Zirkulär im Lauf? Nein.** Die Werte sind gerechnet, eingefroren, und der Lauf rechnet sie nicht neu; kein Rasterpunkt kann sie während des Laufs bewegen. Das ist der Grund, warum das Verfahren bis heute nicht kaputt ist.

**Inkonsistent in der Herleitung? Ja.** Und mit einer Wirkung, die nicht nur Schönheit ist: **Purge und Embargo** sollen verhindern, dass ein Trade über eine Faltengrenze hinweg in zwei Falten oder in die Bestätigungsperiode leckt (2d). Ein `purge_tage`, das aus der **maximalen Haltedauer der heute ausgeführten Trades** stammt, ist für genau einen Rasterpunkt bemessen. Eine Zelle mit längerem Ausstiegshorizont (eine Rasterachse!) hat Trades, die länger halten als das Purge — für sie leckt der Test. Das ist keine Wahl nach Ergebnis, aber eine **systematische Bevorzugung von Zellen mit langen Haltedauern** im Out-of-Sample, und sie ist vor dem Lauf erkennbar. **Die Donchian-Untergrenze** aus dem Median der ausgeführten Trades ist eine Rastergrenze, die vom Positionslimit abhängt — der Raum, in dem gesucht wird, ist durch eine Achse dieses Raums mitbestimmt.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Registertext, Ersteintrag — Reichweite des Grundsatzes aus 5.4:** Keine Festlegung des Verfahrens, die vor dem Lauf steht (Faltenlänge, Purge, Embargo, Trainingsende, Rastergrenzen), wird aus Grössen hergeleitet, die vom **Positionslimit** oder von der **Ausführung** abhängen. Herleitungen aus Trades verwenden **gefundene** Trades (Signalpfad), nie ausgeführte. Der Grundsatz gilt für alle Stellen, an denen 5.4 ihn heute allein anwendet.
>
> **Berichtigung zu 2d (Purge/Embargo), Herleitung:** `purge_tage` wird nicht aus der maximalen Haltedauer eines Parameterstands hergeleitet, sondern als **Schranke über das registrierte Raster**: die grösste Haltedauer, die ein Trade in irgendeiner Zelle des Rasters erreichen kann — aus den registrierten Rastergrenzen der Ausstiegsachsen (Zeitausstieg, maximale Haltedauer), wo eine Strategie keinen begrenzten Ausstiegshorizont hat, aus dem Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag als Tatsachennotiz. Ein Purge, das für eine Zelle des Rasters zu kurz ist, ist ein Befund.
>
> **Berichtigung zur Herleitung der Donchian-Untergrenze (zwei Bots):** aus `median_balken` der **gefundenen** Trades, nicht der ausgeführten. Die Rastergrenze selbst bleibt eine gemessene Grösse (Abschnitt 2/3, „erzeugt, nicht abgetippt") — nur ihre Eingabe wechselt auf den Signalpfad.
>
> **Folge für die Eingabedateien:** Die Haltedauern werden aus **denselben neuen Listen gefundener Trades** abgeleitet, die 24b A3 für die Faltenlänge anordnet — jede gefundene Trade-Zeile trägt `entry_time` und `exit_time`, die Haltedauer folgt daraus. **Ein Erzeuger, eine Eingabedatei je Bot, zwei Herleitungen** (Faltenlänge nach 5.4, Haltedauern für 2d und die Rastergrenze). `haltedauern_je_bot.csv` in heutiger Form und ihr Erzeuger `tb24_haltedauern/auswertung.py` werden historischer Stand mit Tatsachennotiz; `messgroessen.py` liest die Haltedauern aus der neuen Quelle (Konstante, unter dem Resolver). Die Feldliste der neuen Listen (24b A3) bekommt `exit_time` und `haltedauer_balken` ausdrücklich.

*Quelle des Grundes:* 5.4 im Wortlaut („keine Festlegung vor dem Lauf, die vom Positionslimit abhinge"), 2d im Zweck (kein Leck zwischen Falten), 3 („erzeugt, nicht abgetippt"). **Kein Ergebnis — und hier gilt es besonders:** Ich weiss nicht, ob `purge_tage` länger, die Donchian-Untergrenze anders, `messgroessen.json` wie stark verändert herauskommt. Ihr habt es nicht gerechnet, ich habe es nicht gefragt. Die Regel ist dieselbe, wie auch immer es ausgeht, und deshalb steht sie jetzt — bevor der Erzeuger läuft (24.3). Wer nach der Messung sagt „das verändert den Raster zu sehr", wählt nach Wirkung; wer vorher sagt „lassen wir es, es ist ja nicht zirkulär im Lauf", wählt auch — für die Zellen mit kurzen Haltedauern.

*Was sich nicht ändert:* die Faltenlänge-Herleitung (5.4, schon richtig), die Faltengrenzen und die Benchmark-Tabelle — die zwei Ketten sind getrennt, wie ihr gemessen habt; und die Kursdaten-basierten Messgrössen (Volatilität, Datenbereiche) berühren keine Ausführung.

## 5. Zu den Berichtigungen an euch selbst

`G8` prüft `max_tage`, nicht `median_balken` — zur Kenntnis; für G8 heisst das nach Abschnitt 4: Es prüft künftig das aus dem Raster geschrankte `purge_tage`, und seine Gegenprobe muss zeigen, dass ein zu kurzes Purge rot wird.

## 6. Was daraus auf den Plan kommt

1. **Resolver** (24b A2) — vorher nichts anderes.
2. **`messgroessen.py` auf den Resolver** (Abschnitt 2), Haltedauer-Quelle auf die neuen Listen (Abschnitt 4).
3. **Erzeuger auf dem Signalpfad** (24b A3, erweitert um `exit_time`/`haltedauer_balken`) — eine Eingabe, zwei Herleitungen; Modus-Lauf mit **beiden** Nachweisteilen.
4. **Register 41/42:** Reichweite 5.4, Berichtigung 2d-Herleitung, Donchian-Herleitung, Nachweis mit zwei Teilen, Resolver-Pflicht, Tatsachennotizen (`haltedauern_je_bot.csv` historisch, `tb24_haltedauern/auswertung.py` historisch, TB-93/102-Nachweis = 2).
5. **Danach:** Faltenlänge gegen 33.2; `messgroessen.json` neu (Volatilität vom Snapshot, Haltedauern vom Signalpfad); Raster nachziehen und vergleichen (12 Achsen aus 23g plus was aus der Donchian-Herleitung folgt); `purge_tage` gegen das heutige, als Tatsachennotiz; Abbild.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 24b; dazu ANFRAGE 24e; der Anhang war 24c (bereits gelesen). `belege/` nicht gelesen. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…102`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** Ein Nachweis hat zwei Teile — bytegleich **und** Leseprotokoll (null Zugriffe ausserhalb des Snapshots); fehlt eines, ist er 2; der bisherige `messgroessen`-Nachweis ist damit nicht geführt, und für die Benchmark-Tabelle ist zu klären, ob A1b ein Leseprotokoll hatte. Ein Weg: `messgroessen.py` über den Resolver, `TB30A_BASE_DIR` ist kein Snapshot-Weg. Die Mischung war nicht beabsichtigt: Der Grundsatz aus 5.4 gilt für Purge, Embargo, Trainingsende und die Donchian-Grenze genauso — Herleitung aus **gefundenen** Trades; Purge als Schranke über das Raster statt aus einem Parameterstand, weil ein zu kurzes Purge Zellen mit langen Haltedauern bevorzugt. Die Haltedauern kommen aus denselben neuen Listen wie die Faltenlänge: ein Erzeuger, eine Eingabe, zwei Herleitungen; `haltedauern_je_bot.csv` wird historisch. Nicht zirkulär im Lauf, aber inkonsistent in der Herleitung — und die Regel steht, bevor jemand weiss, was herauskommt.

**Unsicher:** ob 2d das Purge heute ausdrücklich als „maximale Haltedauer der ausgeführten Trades" definiert (dann ist meine Berichtigung eine Berichtigung des Registertexts) oder ob 2d nur den Zweck nennt und die Herleitung im Code steht (dann ist es eine Berichtigung des Codes an den Registertext) — die Kategorie seht ihr im Wortlaut von 2d, ich nicht. Und: ob alle neun Strategien einen begrenzten Ausstiegshorizont als Rasterachse haben — wo nicht, greift der Zusatz „Maximum der gefundenen Trades über den Datenhorizont", und der ist zu messen, nicht anzunehmen.

---

## In einfacher Sprache

Der Nachweis, den Fable verlangt hatte, ist auf eine lehrreiche Art gescheitert: Das Programm lieferte exakt das richtige Ergebnis — und las dabei keine einzige Datei aus dem eingefrorenen Bestand, sondern alles aus dem Arbeitsverzeichnis, das heute zufällig gleich ist. Deshalb gilt ab jetzt: Ein Nachweis besteht aus dem Ergebnisvergleich **und** einem Protokoll, woher gelesen wurde; fehlt das Protokoll, ist es kein Nachweis. Das Programm bekommt denselben zentralen Pfadgeber wie alle anderen, damit es den geschützten Modus überhaupt kennt. Die grössere Frage: Das Regelwerk begründet an einer Stelle, warum eine Festlegung nicht von den ausgeführten Geschäften abhängen darf — weil deren Zahl von einem Wert abhängt, der im Lauf erst gesucht wird. An drei anderen Stellen ist genau das aber der Fall. Fable entscheidet: Der Grundsatz gilt überall. Die betroffenen Grössen werden künftig aus den gefundenen Signalen abgeleitet, und die Sperrfrist zwischen Zeitabschnitten wird so bemessen, dass sie für jede mögliche Parameterkombination reicht, nicht nur für die heutige — sonst wären Strategien mit langen Haltezeiten bevorteilt. Praktisch heisst das: dieselben neuen Signallisten liefern beides, Abschnittslänge und Haltedauern, aus einer Quelle. Ob sich dadurch Zahlen ändern, weiss niemand — und genau deshalb steht die Regel jetzt.
