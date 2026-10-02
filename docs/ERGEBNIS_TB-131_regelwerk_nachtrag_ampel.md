# TB-131: Ergebnis. Regelwerk-Nachtrag 02.10.2026 (Auftragstext am Antwortende, Fehler Nr. 17–19, T7, R65 (a)) — E1–E5 zeichengleich; `ampel.py` liest `null` als 0 und zählt leere Schritte nicht

**Sitzungstitel:** `TB-131` · **Stand:** 02.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-131_regelwerk_nachtrag_ampel.md` ·
**Belege:** `docs/belege/TB-131/`
**Eingang:** `e8cfff8` (TB-130 D3). Commits: `5d4f843` (Schritt 0: Stand des steuernden Chats, **⟨S0⟩**), `002aa58`
(A: Regelwerk-Nachtrag, mit den Belegen aus 0a/0b), `278cf0f` (B: `ampel.py`), `a50aeed` (C: Nachweis), der
Abgabe-Commit (D: dieses Dokument, Journal EC) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit
gepusht, jeder Push im ersten Versuch.
**Freigabe:** pauschal für Handwerk ohne Sperrlistennähe (Betreiber 26.09.2026); die Regel in E1 hat der Betreiber am
02.10.2026, 10:45, wörtlich verlangt. **Keine Rückfrage an den Betreiber in dieser Sitzung.**
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau die 3 Einträge des steuernden Chats | **3/3 gleich**, in `$TMPDIR/tb131_0a.txt` **bevor** `docs/belege/TB-131/` entstand, danach nach `0a_status.txt` kopiert ⇒ `5d4f843` |
| 0b | sha256, md5, Zeilen der drei Zieldateien; `ampel.py` md5 `0c42ee78…`, 35 Zeilen | `0b_ausgang.txt`: ARBEITSWEISE **2389** Z., BACKLOG **281** Z. (deckt sich mit der Vorzählung des steuernden Chats); `ampel.py` md5 **`0c42ee78b6fa162e795f0cab026cde9e`, 35 Zeilen** ⇒ Schritt B ausgeführt |
| E1–E5 | Anker vorher 1, ausgeführt, erste Zeile nachher 1 | **5/5**: je Anker 1, ausgeführt ja, Text nachher 1 (`einfuegungen.txt`; Skript `einfuegen.py` liest Zieldatei, Anker, Art und Text aus dem Auftrag; vorher Probelauf `--probe` ohne Schreiben: erste Textzeilen in den Zieldateien je 0) |
| B1 | Inhalt zeichengleich mit dem Codeblock, md5 `997ce08b…`, 40 Zeilen | per Skript aus dem einzigen ```` ```python ````-Block des Auftrags geschrieben (plus Zeilenumbruch am Ende): md5 **`997ce08b0d944bed680285584b9936f8`, 40 Zeilen**, numstat 7/2 |
| B2 alt(P1) | rc 0 | **rc 0** |
| B2 neu(P1) | rc 0, Ausgabe bytegleich alt(P1) | **rc 0, bytegleich** |
| B2 alt(P2) | rc ≠ 0 (Gegenprobe: der Befund) | **rc 1**, letzte stderr-Zeile unter Python 3.9.6: `TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'` |
| B2 neu(P2) | rc 0, Ausgabe bytegleich neu(P1) | **rc 0, bytegleich** |
| C1 | `einfuegungen.txt` E1–E5 je 1/ja/1 | wie E1–E5 oben |
| C2 numstat | ARBEITSWEISE 8/0, BACKLOG 6/0, `ampel.py` 7/2; entfernte Zeilen nur dort | **8/0 · 6/0 · 7/2**; alle übrigen Zeilen in `c2_numstat.txt` sind neue Belegdateien (je `n 0`) |
| C3 | jeder Text genau einmal als Block, Bytevergleich; md5 `ampel.py` gegen B1 | **5/5 GLEICH**, je Vorkommen 1 und an Zeilengrenzen 1; `ampel.py` **GLEICH** (`c3_vergleich.py`, eigener Parser, unabhängig von `einfuegen.py`; das md5-Soll liest das Skript aus dem Auftrag) |

Zur Zusammensetzung der Zahlen: ARBEITSWEISE 8 = E1 1 + E2 2 + E3 2 + E4 3 Tabellenzeilen. BACKLOG 6 = 5 Zeilen
des Blocks E5 + 1 Leerzeile danach; die Leerzeile davor war schon da und wurde nicht verdoppelt.

## Einfügestellen

| | Datei | nach/vor Zeile (vor jeder Einfügung, Probelauf) |
|---|---|---|
| E1 | ARBEITSWEISE | nach 67 („Letzte Zeile: Umzugsampel, gemessen mit …“); die Ampelzeile bleibt in der Tabelle davor, die neue Zeile folgt ihr, wie der Anker verlangt |
| E2 | ARBEITSWEISE | nach 173 („Vor dem Urteil „Widerspruch“ prüfen …“), letzte Zeile der Tabelle |
| E3 | ARBEITSWEISE | nach 164 („Grosse Dokumente nicht im Chat zusammensetzen: …“), letzte Zeile der Tabelle |
| E4 | ARBEITSWEISE | nach 202 („Marken nennen Bezeichner, nicht Zeilen (R49 (e))“), letzte Zeile der Tabelle |
| E5 | BACKLOG | vor 270 (`## 6 — Geparkt, null Arbeit`) |

## Abweichungen und Lesarten

- **E1 und die Ampelzeile:** Der Auftrag setzt E1 *nach* der Zeile „Letzte Zeile: Umzugsampel …“. Wörtlich so
  ausgeführt; die Prüfliste in Abschnitt 0 ist eine Liste von Haken, nicht die Reihenfolge der Antwort, und der
  eingefügte Text sagt selbst, dass die Ampelzeile die letzte bleibt.
- `einfuegen.py` ist per `sed` aus der TB-128-Vorlage abgeleitet. Die Ersetzung der Belegpfade traf auch den
  Vorlagenvermerk im Docstring (er zeigte kurz auf sich selbst); vor dem ersten Lauf auf `TB-128` zurückgesetzt.
  Inhaltlich ohne Wirkung.
- `c3_vergleich.py` ist ebenfalls aus der TB-128-Vorlage abgeleitet (Schnitte nur an `#### E<n>` und `## `, damit
  der `###`-Kopf **im** E5-Codeblock nicht schneidet — die Falle aus TB-127/TB-128 trat diesmal nicht auf) und um
  die md5-Prüfung von `ampel.py` erweitert. Das Soll liest das Skript aus der Zeile `Soll nachher: md5 `…`` des
  Auftrags, nicht aus dem Gedächtnis.
- `b2_probe_ampel.txt` nennt den Pfad der erfundenen Protokolle unter `$TMPDIR` (ein `mkdtemp`-Ordner); die
  Protokolle selbst sind nicht committet, sie entstehen bei jedem Lauf neu aus dem Skript.
- **Journal:** letzter Block vorher **EB** (TB-130) ⇒ neuer Block **EC**, eingefügt nach EB und vor `---` /
  `## Wiederkehrende Lehren`. Nächste Kennung: **ED**. Der erste Einfügeversuch brach an seiner eigenen Wache ab
  (Assertion, ohne zu schreiben): „Wiederkehrende Lehren“ kommt im Journal dreimal vor (Z. 7192, 7537 im Fliesstext,
  9908 als Kopf). Verankert an `\n---\n\n## Wiederkehrende Lehren\n`, gezählt 1, dann eingefügt; numstat 35/0.

## Nicht getan

Einem späteren Auftrag bzw. dem steuernden Chat vorbehalten:

- `ARBEITSWEISE.md` und `BACKLOG.md` in der Ablage erneuern — macht der steuernde Chat, `BACKLOG.md` erst nach der
  27.4-Prüfung;
- unverändert offen aus ERGEBNIS_TB-128: K2h/K2f; die drei Trägerstellen; Fables 29a Abschnitt 1; die Sonnet-Probe;
  `docs/werkzeuge/registerkopie_abschnitte.py` entfernen (Betreiberentscheid fehlt; die Datei ist unverändert).

Ausserdem nicht angefasst: Register, `docs/VORREGISTRIERUNG_*`, `research/`, `shared/`, `strategies/`, `UMZUG.md`,
jedes andere Werkzeug unter `docs/werkzeuge/`, `UEBERGABE*.md` und die `FABLE_*`-Dateien (`UEBERGABE.md` und
`AKTUELLER_AUFTRAG.md` nur in Schritt 0 so committet, wie sie im Arbeitsbaum lagen).

## In einfacher Sprache

Die Regeln vom 02.10. stehen jetzt wörtlich im Regelwerk: Der Starttext für die nächste Programmiersitzung steht am
Ende jeder Antwort des steuernden Chats, direkt vor der Ampelzeile. Aus den Fehlern Nr. 17, 18 und 19 sind
Prüfhaken geworden, dazu die Regel zu frischen Ablagepfaden (T7), die Regel aus R65 (a) für Registeraufträge und
zwei Regeln, wie der steuernde Chat mit dem Arbeitsbaum und mit Folgeaufträgen umgeht. In `BACKLOG.md` steht, was aus
der Abnahme von TB-130 offen ist. Ein Skript hat jeden Text aus dem Auftrag eingesetzt, ein zweites, unabhängiges
hat nachgeprüft, dass jeder Text genau einmal und Zeichen für Zeichen gleich dasteht.

Das kleine Messprogramm für die Umzugsampel brach ab, wenn im Protokoll leere Einträge standen. Die neue Fassung
behandelt leere Felder als null und überspringt Schritte ohne Inhalt. Geprüft an zwei erfundenen Beispielen: Bei
einem normalen Protokoll rechnen alte und neue Fassung genau gleich; bei einem Protokoll mit leeren Einträgen bricht
die alte ab, und die neue rechnet dasselbe wie beim normalen.
