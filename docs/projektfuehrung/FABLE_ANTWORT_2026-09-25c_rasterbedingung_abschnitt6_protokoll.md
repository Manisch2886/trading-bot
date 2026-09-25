# FABLE_ANTWORT 2026-09-25c — Die Berichtigung ist angenommen, mit einer Fundstelle: der Zustand steht in Abschnitt 6, nicht 4; `herkunft.py` wird für eine Zeile geöffnet und bleibt sonst zu; das Herkunftsprotokoll bekommt eine eigene Zeile und eine Ausnahme von 19; vier Fragen beantwortet

*Bezug: `FABLE_ANFRAGE_2026-09-25c_rasterbedingung_und_tb105.md`. Einspruch aufgelöst, drei Messungen, TB-105, vier Fragen. Reihenfolge wie die Anfrage.*

**Leseprotokoll dieses Chats, Stand jetzt:** wie 25b; dazu ANFRAGE 25c (Anhang). Nichts weiter gelesen. Ergebnisgrössen nach 27.1: keine.

---

## 1. `_bedingung` — Berichtigung angenommen; der Zustand ist registriert, aber in Abschnitt 6

**Angenommen.** Der Wert steuert, welche Zellen **existieren**, nicht, ob eine Zelle die Drawdown-Bedingung besteht; `zulaessigkeit()` nimmt ihn nicht entgegen. Weder (α) noch (β) — mein Einspruch hat eine unklare Benennung getroffen, nicht die Stelle, die ich befürchtet hatte. Das ist der richtige Ausgang eines Einspruchs: gemessen, nicht beschwichtigt.

**Eine Fundstelle berichtige ich an eurer Berichtigung:** Der Satz *„Zellen, in denen die Strategie nicht definiert ist, existieren nicht … von 1.024 auf 384"* steht in **Abschnitt 6 (Die Plateau-Regel)**, im Absatz nach der Spitzenformel — nicht in Abschnitt 4. Abschnitt 4 ist die Drawdown-Bedingung, also genau das, wovon ihr den Zustand abgrenzen wollt; „keine Rasterbedingung (Abschnitt 4)" würde beim nächsten Leser dieselbe Verwechslung erzeugen, die ihr gerade auflöst. Richtig: **„keine Rasterbedingung (Abschnitt 6)"**. *[Gelesen im Register, Teil 1; nicht im Repo gemessen — die Nummer ist im Kopf der Kopie nachzusehen, sie lässt sich nicht verwechseln.]*

**Der Rest — richtig eingeordnet, und ich schärfe ihn um einen Punkt:**

> **Registertext, Ergänzung zu 6 und 24b A2 — unbekannter Bedingungstext:** Ein nicht leerer `_bedingung`-Text, den der Code nicht als Rasterbedingung erkennt, ist ein Widerspruch zwischen Register und Code und endet mit 2 — unabhängig vom Modus. Die Deutung des Textes geschieht an **einer** Stelle; jeder Leser (Zellenzahl, Zellmenge, Nachbarschaft) ruft sie. Ein zweiter Textvergleich desselben Strings ist ein zweiter Parser (24b B4).

*Quelle des Grundes:* 6 (die Rasterbedingung ist Registertext; ein Code, der sie still übergeht, rechnet ein anderes Raster mit N = 1.024 statt 384 und macht Abschnitt 3 und Festlegung 10 unbemerkt falsch), 24b A2, 24b B4. Kein Ergebnis. **Für TB-106:** rc 2 in `auswertung.py` jetzt; die zweite Stelle (`registerdaten.py:605`, Punkt 1) bekommt die Tatsachennotiz bis 40.8 (h), und **dort** wird die Deutung auf eine Funktion zusammengezogen, die beide rufen — nicht früher, weil Punkt 1 nicht für diesen Satz allein geöffnet wird. Eure Neigung „unabhängig vom Modus" ist richtig, aus eurem Grund.

---

## 2. Die drei Messungen

**(a) `anhaengen()` geht über `block()`, `block()` ruft `datenstand()` ohne Argument** — damit gilt der erste Fall aus 25a: `herkunft.py` wird **planmässig für diese Stelle geöffnet** (Punkte 11/12, 37.3: Auftrag, Freigabe, alter und neuer Hash, neues Abbild). Das ist eine **Berichtigung meiner Entscheidung in 37.4** („nicht öffnen"), und ich adressiere sie als solche:

> **Berichtigung zu 37.4 (Entscheidung „Nicht öffnen"):** `herkunft.py` wird einmal geöffnet, um `datenstand()` den Datenpfad durch `block()` und `anhaengen()` durchzureichen (Argument, keine Voreinstellung unter dem Modus). Sonst ändert sich nichts: `EINGEFROREN` bleibt, wie 39.7 es entschieden hat; `register()` bezeugt weiter die Abschnitt-0-Menge; die Sonde bezeugt Abschnitt 10. **Planmässig geöffnet heisst nicht offen** — eine Öffnung nach 37.3 trägt genau die Änderung, für die sie beauftragt ist.

*Quelle des Grundes:* 37.4 nannte als Grund für „nicht öffnen" den Ort, nicht den Wortlaut, und die Sonde als Ersatz; für den Datenpfad der Protokollkette gibt es keinen Ersatz ausser einem zweiten Ort (25a). Der Satz „heute gleich, aber keine Eigenschaft des Codes" ist TB-102 in Kleinformat und steht als Tatsachennotiz daneben. Kein Ergebnis.

**(b) `_min_history` bricht nicht mit 2 ab** — Frage (2) unten.

**(c) `MINDESTTRAINING_JAHRE` rechnet nirgends** — zwei tote Felder, eine tote Zeile: dieselbe Berichtigung wie die drei Felder, wie in 25b (4) gesagt; Konstante bis 40.8 (h). `research/krypto_historie/faltenplan.py` mit eigener Konstante: ausserhalb des Laufbereichs, Tatsachennotiz (`K4f`, `T56b.6`), sonst nichts.

**(d) 19 beschreibt den Stand** — der Befund steht. Dass ihr die Erweiterung als eigenen Auftrag nach TB-106 führt, weil sie die Startprüfung jedes Laufs ändert, ist richtig — mit zwei Sätzen von mir: Sie ist **Tag-Vorbedingung**, nicht Wunsch; und sie hängt an Frage (4)(b), weil das Herkunftsprotokoll unter `research/` liegt und die Sauberkeitsprüfung sonst am ersten Lauf scheitert (Abschnitt 4 unten).

---

## 3. TB-105 — Kenntnisnahme, und was 11 jetzt heisst

11.1 erfüllt, 3 von 3, `RegimefilterFehlt`, Hashes mit BTCUSDT gleich, vier Proben beissen allein — und die Messung, dass `t3_supertrend` **vorher** ohne BTCUSDT still weiterrechnete, mit anderem Hash: Das ist der Determinismus-Befund, mit dem 11.1 am 14.09. begründet wurde, jetzt gemessen statt behauptet. (c) und (a) mit rc 2 unter dem Modus, Schreibziele beim Import weg, F1 im frischen Klon mit leerem `git status --porcelain --ignored`, F2 bytegleich, F3 8/8, 196/196. **Angenommen.**

⚠️ **Damit niemand „Abschnitt 11 erfüllt" liest:** Der Schlusssatz von Abschnitt 10 nennt **beide** Bug-Fixes aus 11. Erfüllt ist **11.1**. 11.2 (Agent 2 auf dem führenden Mass; `evaluate_combination_multi` liefert den Kapital-Drawdown noch nicht) und 11.3 (Durchreichung `sma_trend_filter`, `bb_*`) sind **TB-30b** und offen — sie gehören zum Laufcode, den es nach 24.5 noch nicht gibt. Tatsachennotiz zu 11: 11.1 geschlossen (TB-105), 11.2/11.3 offen.

**Zur Zwischenablage:** (1) und (2) erfüllt, (3) nicht — Befund 1, Handwerk. Eine Ergänzung zur Datei: `universum_trockenlauf.py` steht nicht im Abbild, und das ist heute richtig; **mit dem Faltenplan-Abbild (TB-100) wird die Erzeugerkette des Trockenlaufs registriert** — 33.3 sagt es schon: *„der erzeugende Code wird mit der Datei registriert (5e)"*. Bedingung (ii) der ersten Falte kommt aus dieser Kette (25.3); ein Abbild, dessen Erzeuger ungebunden ist, bezeugt weniger, als es sagt.

**Zum Befund der Ersatzmodule** — Frage (3).

---

## 4. Die vier Fragen

### (1) `_bedingung` — ja, mit Abschnitt 6 (oben)

### (2) `_min_history` — ja, in TB-106, und die Regel gilt so, wie ihr sie zitiert

`re.findall`, genau ein Treffer, sonst `SystemExit(2)`, unabhängig vom Modus; Mutationsproben „zwei Treffer" und „kein Treffer". Der Grund für „unabhängig vom Modus" ist derselbe wie bei (1): Ein Muster, das in einer Bot-Datei nicht genau einmal trifft, ist ein Widerspruch zwischen der registrierten Tabelle in 16.7 (b) und dem Code — kein Laufzustand. Und der stille Hinweis in `kerzen_elliott_wave()` ist die TB-45-Klasse (weiter ohne Wert); der `TypeError` in `loader_lesart()` ist laut, aber 1 statt 2 — nach 36.5 ein Aufruf, der nicht messen konnte und es nicht mit dem eigenen Wert sagt. Beides geht mit.

### (3) Die Bauart von TB-105

**(a) Die Modus-Abfrage an den 14 Stellen selbst — in Ordnung, mit einer Tatsachennotiz und einer Gegenprobe.** Das Verfahren zählt keine Zeilen; es verlangt, dass es einen Resolver gibt und keinen Fallback. Vierzehn Aufrufe derselben Funktion (`paths.selektionsmodus()`) sind kein zweiter Ort für einen Wert — der Wert lebt in `paths.py`. **Der eigentliche Befund ist der, den ihr gefunden habt:** Drei Regelbetrieb-Werkzeuge (`kurven_lauf.py`, `determinismus_lauf.py`, `messung_primaerschluessel.py`) ersetzen `strategy_paths` in `sys.modules` durch ein Teilmodul. Das ist im Regelbetrieb Handwerk mit Live-Freigabe; **im Laufbereich wäre es ein zweiter Resolver.** Regel daraus, klein: Ein Werkzeug, das den Resolver-Nachbarn austauscht, endet unter dem Modus mit 2, bevor es das tut — dann kann es nie in den Laufbereich geraten. Tatsachennotiz zu den drei Dateien; ob ihr sie ändert, ist Live-Freigabe. **Gegenprobe zu den 14 Stellen:** eine Prüfung, dass jede `__main__`-Stelle im Laufbereich die Abfrage trägt — sonst fehlt sie beim fünfzehnten Skript still (dieselbe Kopplung wie `G6`). Handwerk.

**(b) `getattr(paths, "selektionsmodus", None)` — ja, ein Rückfall der Form nach; entfernen.** Eure Neigung ist richtig, und der Grund ist stärker, als ihr ihn nennt: Fehlt dem Nachbarn die Funktion, kann `strategy_paths.py` **nicht wissen**, ob der Modus an ist — und „dann Regelbetrieb" ist eine Annahme über genau die Frage, die der Modus beantwortet. Ein Nachbar ohne die Funktion ist kein Nachbar; das ist 19 (gespaltener Baum) in kleiner Form. Also: direkter Aufruf, ohne Modus wie mit Modus, und die zwei Proben bekommen ein `paths`, das die Funktion trägt. Dass `_resolver_ist_nachbar()` das echte `paths.py` zusichert, macht den Zweig unerreichbar, nicht zulässig — euer Zitat aus 25b trifft.

### (4) Zwei Schreibziel-Fragen

**(a) Bytecode-Caches — Klasse (ii), Umgebung.** Der Interpreter schreibt sie, nicht der Lauf; ihr Inhalt ist aus dem registrierten Code abgeleitet und keine Eingabe; sie liegen ausserhalb Repo und Snapshot. In der Umgebungsliste stehen sie als **Muster** (`~/Library/Caches/com.apple.python/<wurzel>/…`), nicht als Pfade — der Klonpfad wechselt. Zwei Bedingungen, damit (ii) nicht zur Hintertür wird: Ein `__pycache__` **im Repo** ist nur zulässig, wenn es git-ignoriert ist und nicht unter `snapshots/` liegt (im Klon war `--ignored` leer — gemessen, gut); und ein Cache ist nie Eingabe im Sinn von 5e — der Lese-Audit führt `.pyc`-Zugriffe unter (ii), nicht unter (i).

**(b) `herkunft_protokoll.jsonl` — eigene Zeile, und eine Ausnahme von 19, die vor dem 19-Auftrag entschieden sein muss.**

> **Ergänzung zu 25a (A) (iii) — registrierte Protokolle:** Zulässige Schreibziele eines Modus-Laufs sind `--ziel`, Belegpfade, Zwischenablagen nach (iv) und **registrierte Protokolle** — heute genau eines: `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl` (10.1). Ein registriertes Protokoll ist append-only: Die Schreibregel 36.1 gilt in Anhängeform — nie kürzen, nie umschreiben, nie neu anlegen, wenn es existiert; seine Unversehrtheit prüft der Kettenhash (10.1), und `--pruefen` liest es als registrierte Eingabe (i). **Sein Ordner wird nicht angelegt:** Fehlt der registrierte Ort, endet `anhaengen()` mit 2 — ein fehlender Ort ist ein Baum, der nicht der registrierte ist, und ein `makedirs` wäre ein Fallback für genau diese Feststellung. **Ausnahme von 19:** Registrierte Protokolle sind von der Sauberkeitsprüfung des Arbeitsbaums ausgenommen wie `data/` (19), weil sie planmässig während des Laufs wachsen; die Ausnahme ist auf die namentlich registrierten Pfade beschränkt, und der Kettenhash ersetzt dort die Sauberkeit.

*Quelle des Grundes:* 10.1 (das Protokoll ist der Ort der Läufe, append-only, Kettenhash), 38.3 (es entsteht mit dem Erzeuger), 19 (die `data/`-Ausnahme mit ihrem Grund: eine Datei, die planmässig zwischen Läufen wechselt, darf die Startprüfung nicht auslösen). Kein Ergebnis. *Warum die Ausnahme jetzt und nicht später:* Sobald 19 auf den Laufbereich erweitert ist, liegt das Protokoll unter einem geprüften Pfad — der zweite Lauf würde an der Spur des ersten scheitern. Der 19-Auftrag braucht diese Zeile, bevor er beginnt.

**Zu `makedirs` in `anhaengen()`:** Der Ordner `ergebnisse/` trägt versionierte Dateien und existiert in jedem Klon; das `makedirs` ist tot — und geht mit derselben Öffnung (2 (a)) heraus, weil eine tote Zeile mit Fallback-Form dieselbe Klasse ist wie `getattr` in (3)(b).

---

## 5. Auf Register 41/42, zusätzlich

| | Eintrag |
|---|---|
| a | Berichtigung an der Benennung: „keine Rasterbedingung (Abschnitt 6)"; Registertext „unbekannter Bedingungstext ⇒ 2, eine Deutung" (1) |
| b | Berichtigung zu 37.4: `herkunft.py` einmal geöffnet für den Datenpfad der Kette; sonst zu; „planmässig geöffnet ist nicht offen" (2 (a)) |
| c | Tatsachennotiz zu 11: 11.1 geschlossen (TB-105, 3/3, vorher stiller Weiterlauf gemessen); 11.2/11.3 offen, TB-30b (3) |
| d | `_min_history`: genau ein Treffer oder 2, unabhängig vom Modus; die Erzeugerkette des Trockenlaufs wird mit dem Faltenplan-Abbild registriert (33.3) (4 (2), 3) |
| e | Ersatzmodule der Regelbetrieb-Wächter: Tatsachennotiz; unter dem Modus 2; Gegenprobe über alle `__main__`-Stellen des Laufbereichs (4 (3)(a)) |
| f | `getattr`-Ersatz in `strategy_paths.py`: Rückfall, entfernt (4 (3)(b)) |
| g | Klasse (ii) umfasst Interpreter-Caches als Muster; `__pycache__` im Repo nur git-ignoriert und ausserhalb `snapshots/` (4 (4)(a)) |
| h | Registrierte Protokolle als eigene Zeile in (iii); append-only; Ordner nicht anlegen; Ausnahme von 19 — **vor dem 19-Auftrag** (4 (4)(b)) |

---

**Kurz:** Einspruch aufgelöst — der Wert regelt, welche Zellen existieren (Rasterbedingung), nicht die Drawdown-Bedingung; angenommen, aber die Fundstelle ist Abschnitt 6, nicht 4, und Abschnitt 4 ist genau die Verwechslung. Ein unbekannter Bedingungstext endet mit 2, modusunabhängig, und wird an einer Stelle gedeutet. `anhaengen()` geht über `block()` ohne Pfad: `herkunft.py` wird für diese eine Zeile planmässig geöffnet — Berichtigung zu 37.4 — und bleibt sonst zu. `_min_history`: genau ein Treffer oder 2, mit TB-106. 11.1 ist geschlossen und gemessen; 11.2/11.3 bleiben offen. Vierzehn Inline-Abfragen sind in Ordnung, die Ersatzmodule der Wächter sind der Befund; das `getattr` kommt weg. Bytecode-Caches sind Umgebung nach Muster. Das Herkunftsprotokoll bekommt eine eigene Zeile: append-only, kein Ordner anlegen, ausgenommen von 19 wie `data/` — und diese Ausnahme muss vor dem 19-Auftrag im Register stehen.

**Unsicher:** nichts, was eine Entscheidung dieser Antwort trägt. Voraussetzung, zu messen: dass `ergebnisse/` in jedem Klon existiert, weil versionierte Dateien darin liegen (wenn nicht, gilt trotzdem: fehlt der Ort, 2).

---

## In einfacher Sprache

Mein Einspruch von gestern ist geklärt: Die fragliche Stelle entscheidet nur, welche Parameterkombinationen es überhaupt gibt, nicht, ob eine die Verlustgrenze einhält. Das steht so im Regelwerk — aber im Abschnitt über die Plateau-Regel, nicht dort, wo ihr es zitiert; die Nummer ist zu berichtigen, weil die falsche Nummer genau die Verwechslung wieder einführen würde. Ein kleiner Rest wird zum Abbruch gemacht: Ein Bedingungstext, den der Code nicht kennt, darf nicht still übergangen werden.

Das Herkunftsprogramm muss doch einmal geöffnet werden, für genau eine Zeile: Es hasht sonst den falschen Datenordner, wenn es das Protokoll fortschreibt. Geöffnet für eine Zeile heisst nicht geöffnet für alles.

Der letzte Auftrag ist sauber; die Marktfilter-Wache sitzt, und die Messung zeigt, dass der Bot vorher tatsächlich still mit anderem Ergebnis weiterrechnete. Zu den Bauart-Fragen: Die vierzehn Einzelabfragen sind in Ordnung; der Ersatz, der greift, wenn eine Funktion fehlt, kommt weg. Zwischenspeicher des Interpreters gelten als Umgebung. Und das fortlaufende Herkunftsprotokoll bekommt eigene Regeln — nur anhängen, nie umschreiben, keinen Ordner anlegen, und es ist von der Prüfung „Arbeitsbaum sauber" ausgenommen, sonst würde der zweite Lauf an der Spur des ersten scheitern.
