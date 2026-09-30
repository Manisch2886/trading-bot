# TB-125: Ergebnis. Regelwerk-Nachtrag 29./30.09.2026 — 24/24 Einfügungen E1–E24 per Skript aus dem Auftrag in `UMZUG.md`, `ARBEITSWEISE.md`, `BACKLOG.md`; B3 24/24 zeichengleich, entfernte Zeilen nur aus den Ersetzungen; lief auf **Opus 5.5**, zählt deshalb **nicht** als Sonnet-Probe nach 22.12

**Sitzungstitel:** `TB-125` · **Stand:** 30.09.2026 · **Auftrag:** `docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md` · **Belege:** `docs/belege/TB-125/`
**Modell (0b):** **Claude Opus 5.5** (`claude-opus-5-5`, Selbstauskunft aus der Systemangabe der Sitzung), nicht Sonnet 5.5. Aufwandsstufe in der Sitzung nicht ablesbar. Nach dem Kopf des Auftrags: abgearbeitet, **zählt nicht als Probe**.
**Eingang:** `4618fa9` (TB-124). **Commits:** `b711567` (Schritt 0), `deba416` (A/B), der Abgabe-Commit und `c3_porcelain.txt`. Alle gepusht.
**Freigabe:** Handwerk ohne Sperrlistennähe, pauschal frei (Betreiberentscheid 26.09.2026, wörtlich im Auftrag). Geändert nur `docs/projektfuehrung/ARBEITSWEISE.md`, `UMZUG.md`, `BACKLOG.md`, dazu Belege, dieses Ergebnis und `JOURNAL.md`.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). **Kein Abbruchkriterium ausgelöst.** **Rückfragen an den Betreiber: keine.** Keine Helfer-Agenten eingesetzt.

## Kurz-Tabelle

| | Soll | Ist |
|---|---|---|
| **0a** `git status --short` | die drei Einträge des Auftrags | genau diese drei ⇒ `b711567` |
| **0c** Ausgang | sha256/Zeilen | ARBEITSWEISE `b2b4c312…` 2215 Z., UMZUG `548098cf…` 384 Z., BACKLOG `68c93e93…` 228 Z. |
| **A/B1** Einfügungen | 24 × Anker 1, ausgeführt, Text nachher 1 | **24/24** (`einfuegungen.txt`) |
| **B2** entfernte Zeilen UMZUG | E4 1 + E5 32 (Anker Zeile 251–282, vorher aus der Datei gezählt) = **33** | **33**, zeilengleich mit den ersetzten |
| **B2** entfernte Zeilen ARBEITSWEISE | E10, E11, E12, E13, E24 = **5** | **5**, zeilengleich |
| **B2** entfernte Zeilen BACKLOG | **0** | **0** |
| **B2** numstat (zugefügt/entfernt) | — | ARBEITSWEISE 157/5, BACKLOG 2/0, UMZUG 23/33 |
| **B3** Zeichengleichheit | 24 × „gleich“, genau 1 Treffer als Block | **24/24 gleich** |

Die Zusätze gehen ebenfalls auf: ARBEITSWEISE 157 = 155 Textzeilen der Einfügungen + je eine Absatz-Leerzeile bei E19 und E20; UMZUG 23 = 20 Textzeilen + je eine Absatz-Leerzeile bei E2, E3, E6; BACKLOG 2 = E22 + E23.

## Verfahren

- `docs/belege/TB-125/einfuegen.py` liest je `#### E<n>` Datei (aus der Überschrift `### Datei …`), Anker (Backtick-Spannen der Ankerzeile), Art und Text (erster Codeblock, Zäune ``` bzw. `~~~` bei E21) aus dem Auftrag, zählt den Anker unmittelbar vor der Einfügung (Python `str.count`), führt aus und zählt die erste Textzeile am Endstand. Probelauf mit `--probe` vor dem echten Lauf.
- Leerzeilen nach Auftrag: Tabellenzeilen ohne Leerzeilen; Absätze bekommen davor und danach eine Leerzeile, eine vorhandene wird nicht verdoppelt (an allen fünf Stellen war die Leerzeile auf der vom Anker abgewandten Seite schon da — E2, E3, E6 davor, E19, E20 danach —, das Skript fügte je eine zwischen Anker und Text hinzu); E18/E21 wörtlich mit der Leerzeile am Ende. E21 steht nach `---` von 22.9 und endet selbst mit `---`, dann `## 23.`
- `docs/belege/TB-125/b3_vergleich.py` hat einen **eigenen** Parser für die Codeblöcke (nicht den von `einfuegen.py`) und sucht `"\n" + Text + "\n"` im Endstand, also auf Zeilengrenzen, ohne Normalisierung. B2 vergleicht die `-`-Zeilen aus `git diff -U0 HEAD` als Multimenge mit den Zeilen, die die Ersetzungsanker in der Ausgangsfassung treffen. ⚠️ Beide Teile lesen gegen `HEAD`; nach `deba416` nachgerechnet ergibt B2 leer — zum Wiederholen `HEAD` durch `b711567` ersetzen.

## ⚠️ Eine Abweichung vom Auftrag, benannt

**E24 steht im Auftrag unter der Überschrift „Datei `docs/projektfuehrung/BACKLOG.md`“**, gehört aber nach seinem eigenen Titel („Abschnitt 0, ‚Wenn ein Dokument mitgeht‘“) und nach B2 („ARBEITSWEISE: E10, E11, E12, E13, E24“) in `ARBEITSWEISE.md`. Gemessen: der Anker `Als Datei, nie als Chat-Text zum Herauskopieren — für alle vier Wege` steht in `ARBEITSWEISE.md` genau einmal (Zeile 69), in `BACKLOG.md` keinmal. Der Probelauf nach Überschrift ergab für E24 „Anker vorher 0 · ausgeführt nein“. Ich habe E24 in `ARBEITSWEISE.md` ausgeführt, als ausdrücklich benannte Zuordnung im Skript (`DATEI_KORREKTUR = {24: …}` mit Begründung im Kommentar). *Erschlossen, nicht belegt:* dass der steuernde Chat E24 nur an falscher Stelle im Auftrag einsortiert hat; der Inhalt der Einfügung ist unverändert. Bitte bei der Abnahme bestätigen.

Sonst: `JOURNAL.md` — „ans Ende“ ist wie bei allen bisherigen Blöcken als „hinter den letzten Buchstabenblock, vor ‚## Wiederkehrende Lehren‘“ umgesetzt.

## Probe nach 22.12

- **Modell:** Opus 5.5 — **keine gültige Probe.** Der Betreiber hatte das Modell vor dem Einfügesatz nicht auf Sonnet gestellt (oder die Umstellung griff nicht); der Kopf des Auftrags sieht für diesen Fall vor: abarbeiten, nicht als Probe werten. Die Sonnet-Probe für Dokumentationsaufträge steht damit weiter aus.
- **Werkzeugaufrufe:** 23 bis einschliesslich Abgabe-Commit (Lesen 7, Skripte schreiben/ändern 4, Ausführen/Messen 6, Ergebnis/Journal 3, Commits 3), danach C3.
- **Was nicht auf Anhieb gelang:**
  1. Der Auftrag (33 KB) passte nicht in eine Shell-Ausgabe; neu gelesen mit dem Lesewerkzeug.
  2. `cat -A` gibt es unter macOS nicht (BSD-`cat`); ohne Folgen, Kontext mit `awk` gezeigt.
  3. **E24 nach Überschrift in `BACKLOG.md` einsortiert** — erst der Probelauf zeigte „Anker 0“. Das ist der inhaltlich einzige Stolperstein; für eine Sonnet-Probe wäre er der Prüfstein, ob die Sitzung auslässt (Verfahren Nr. 1: „nicht ausführen, vermerken“) oder die Zuordnung aus Titel und B2 erschliesst. Beides wäre vertretbar; diese Sitzung hat erschlossen und benannt.
  4. Im B2-Teil von `b3_vergleich.py` filterte die erste Fassung `-`-Zeilen mit `startswith("---")` aus, was auch entfernte Inhaltszeilen „`--…`“ verschluckt hätte; vor dem ersten Lauf auf den Kopf `--- a/` eingeengt.

## Nicht getan

Die Einarbeitungspunkte ohne vorbereiteten Wortlaut bleiben für einen späteren Auftrag:
- K2h/K2f (PRUEFPRINZIPIEN);
- die drei Trägerstellen (TB-119 Nr. 2);
- der kalte Leser ohne Gedächtnis;
- Fables 29a Abschnitt 1–3;
- „neue Fable-Antworten über `project_info` finden“ (Übergabe, Umzug 29.09.2026, 07:15, Block 9);
- Fables Umzugshinweis aus 30a (gehört zum Fable-Umzug, nicht ins Regelwerk).

Ausserdem nicht getan: `UEBERGABE.md`/`UEBERGABE_ARCHIV.md`, Register, Code — nach Auftrag ausgeschlossen. Der Verweis in 22.12 auf dieses Ergebnis („Probe Dokumentationsauftrag: TB-125; Ergebnis in …“) stimmt jetzt als Pfad, sagt aber noch nicht, dass die Probe mangels Sonnet ausfiel — das nachzutragen wäre ein eigener Handwerksschritt.

## In einfacher Sprache

Alle 24 neuen Regeln stehen jetzt an ihrem festen Platz in Arbeitsweise, Umzugsanleitung und Backlog, Zeichen für Zeichen so wie im Auftrag; ein Skript hat das nachgeprüft. Eine Einfügung (E24) war im Auftrag unter der falschen Datei einsortiert; sie steht jetzt dort, wo ihr Anker ist, und das ist oben benannt. Weil in dieser Sitzung Opus statt Sonnet lief, sagt der Lauf nichts darüber, ob Sonnet solche Abschreibarbeit schafft — diese Probe steht noch aus.
