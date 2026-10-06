# TB-133: Ergebnis. Regelwerk-Nachtrag 04.–06.10.2026 (Umzug nur auf Ansage, Sitzung über den Wächter, git über die Brücke, Ablage durch Helfer, Regeln aus vier Umzügen) — E1–E9 zeichengleich

**Sitzungstitel:** `TB-133` · **Stand:** 06.10.2026, 07:46 (gemessen mit `date`) · **Auftrag:** `docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md` ·
**Belege:** `docs/belege/TB-133/`
**Eingang:** `67a2202` (TB-136 D3). Commits: `1ea5213` (Schritt 0: Stand des steuernden Chats, **⟨S0⟩**), `5216e1d`
(A: Einfügungen E1–E9, mit den Belegen aus 0a/0b, den zwei Skripten und `einfuegungen.txt`), `f5c69b4` (C: Nachweis),
der Abgabe-Commit (D: dieses Dokument, Journal EF) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit
gepusht, jeder Push im ersten Versuch.
**Freigabe:** pauschal für Handwerk ohne Sperrlistennähe (Betreiber 26.09.2026); die Regeln in E4 und E2/E8 hat der
Betreiber am 05.10.2026, 21:25 und 23:58, wörtlich verlangt. **Keine Rückfrage an den Betreiber in dieser Sitzung.**
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | genau die 3 Einträge des steuernden Chats | **3/3 gleich**, in `$TMPDIR/tb133_0a.txt` **bevor** `docs/belege/TB-133/` verändert wurde, danach nach `0a_status.txt` kopiert ⇒ `1ea5213`; `vormessung/v1_vormessung_04a.md` unberührt |
| 0b | md5 und Zeilen wie die Vorzählung; sha256 nur messen | `0b_ausgang.txt`: ARBEITSWEISE **2397** Z. `42e20803…`, UMZUG **378** Z. `edfe2a34…`, BACKLOG **307** Z. `c005a57d…` — alle drei **GLEICH** der Vorzählung |
| E1–E9 | Anker vorher 1, ausgeführt, erste Zeile nachher 1 | **9/9**: je Anker 1, ausgeführt ja, Text nachher 1 (`einfuegungen.txt`; vorher Probelauf `--probe` ohne Schreiben: erste Textzeilen in den Zieldateien je 0) |
| C1 | `einfuegungen.txt` E1–E9 je 1/ja/1 | wie E1–E9 oben |
| C2 numstat | ARBEITSWEISE 16/0, UMZUG 2/0, BACKLOG 10/0 | **16/0 · 2/0 · 10/0** (`c2_numstat.txt`, `git diff --numstat 1ea5213 5216e1d` über `docs/projektfuehrung/`) |
| C3 | jeder Text genau einmal als Block, Bytevergleich | **9/9 GLEICH**, je Vorkommen 1 und an Zeilengrenzen 1 (`c3_vergleich.py`, eigener Parser, unabhängig von `einfuegen.py`) |

Zur Zusammensetzung der Zahlen: ARBEITSWEISE 16 = E1 1 + E2 1 + E3 1 + E4 3 + E5 3 + E6 1 + E7 6 Tabellenzeilen.
UMZUG 2 = Absatz E8 + 1 Leerzeile danach; BACKLOG 10 = 9 Zeilen des Blocks E9 + 1 Leerzeile danach. Die Leerzeile
davor war in beiden Dateien schon da (UMZUG Z. 107, BACKLOG Z. 295) und wurde nicht verdoppelt.

## Einfügestellen

| | Datei | nach/vor Zeile (vor jeder Einfügung, Probelauf) |
|---|---|---|
| E1 | ARBEITSWEISE | nach 42 („Fundstellen nur, wenn sie vor mir liegen; …“) |
| E2 | ARBEITSWEISE | nach 95 („Ein nötiger Umzug wird frühzeitig angekündigt — …“) |
| E3 | ARBEITSWEISE | nach 132 („Kein `git status` über die Geräteanbindung — auch nicht bei der allerersten Messung …“) |
| E4 | ARBEITSWEISE | nach 149 („Vor dem Schliess-Auslöser das Alter des letzten Commits messen …“) |
| E5 | ARBEITSWEISE | nach 167 („„Frischer Stage-Pfad“ heisst ein neuer Pfadname …“) |
| E6 | ARBEITSWEISE | nach 178 („Ein „kein Widerspruch“ nennt, was gemessen ist und was nicht …“) |
| E7 | ARBEITSWEISE | nach 210 („Folgeauftrag gleicher Bauart: auf den Vorgänger verweisen …“) |
| E8 | UMZUG | vor 108 (`### ⚠️ Wann NICHT umgezogen wird`) |
| E9 | BACKLOG | vor 296 (`## 6 — Geparkt, null Arbeit …`) |

Alle sieben Anker in ARBEITSWEISE sind Tabellenzeilen (`| ☐ | …`); die neuen Zeilen stehen nach dem Lauf jeweils
unmittelbar dahinter in derselben Tabelle (nachgemessen mit `grep -n`).

## Abweichungen und Lesarten

- **`c3_vergleich.py`, Ableitung:** Ich habe die Vorlage per Python-Ersetzung (mit `assert count == 1` je Ersatz)
  umgestellt, nicht per `sed`. Der erste Versuch brach an der eigenen Wache ab, ohne zu schreiben: Der neue
  Vorlagenvermerk („Vorlage: docs/belege/TB-131/c3_vergleich.py …“) enthielt genau den Pfad, den ein späterer
  Ersatz für die Aufrufzeile suchte — dieselbe Falle wie in TB-131, nur von der anderen Seite. Im zweiten Versuch
  war der Ersatz auf die ganze Aufrufzeile beschränkt. Vorlagenvermerke danach in beiden Skripten geprüft: beide
  zeigen auf `docs/belege/TB-131/…`.
- **`einfuegen.py`** ist per `sed` aus der TB-131-Vorlage abgeleitet; jede Ersetzung ist mit umgebendem Text eng gefasst, der
  Vorlagenvermerk wurde dabei auf TB-131 gesetzt (vorher TB-128) und nicht getroffen. `diff` gegen die Vorlage:
  nur die im Auftrag genannten Stellen (Kopf, Vorlagenvermerk, Aufrufzeilen, Pfade, `BLOECKE = {"E8", "E9"}`,
  `range(1, 10)`, Kopfzeile der Ausgabe).
- **`c3_vergleich.py`** schneidet wie in TB-131 nur an `#### E<n>` und `## `; der `### `-Kopf **im** E9-Codeblock
  schnitt nicht. Der Teil zu `ampel.py` (und damit `import hashlib`) entfällt; Soll-Anzahl 9.
- **C2** misst `git diff --numstat ⟨S0⟩ HEAD` mit HEAD = `5216e1d` (Commit A), eingeschränkt auf
  `docs/projektfuehrung/`; die Belegdateien desselben Commits stehen damit nicht in der Liste.
- **Journal:** letzter Block vorher **EE** (TB-136) ⇒ neuer Block **EF**, eingefügt nach EE und vor `---` /
  `## Wiederkehrende Lehren`, verankert an `\n---\n\n## Wiederkehrende Lehren\n` (gezählt 1). Das Einsetzen vor
  diesem Anker liess zunächst den Trennstrich `---` zwischen EE und EF weg (der Anker trägt den Strich des
  *vorigen* Blocks); in einem zweiten Schritt mit Wache (`count == 1`) nachgezogen. numstat JOURNAL danach 34/0.
  Nächste Kennung: **EG**.

## Nicht getan

Einem späteren Auftrag bzw. dem steuernden Chat vorbehalten:

- `ARBEITSWEISE.md`, `UMZUG.md` und `BACKLOG.md` in der Ablage erneuern — macht der steuernde Chat, `BACKLOG.md`
  erst nach der 27.4-Prüfung;
- der Fliesstext in `ARBEITSWEISE.md` 6b (Start) und 10 und die git-Liste im Eröffnungstext (`UMZUG.md` Abschnitt 6
  nennt noch `diff --name-only`) — zusammen mit dem Entwurf aus TB-137, Paket 15 (letzte Zeile von E9);
- unverändert offen aus ERGEBNIS_TB-131 (dort aus ERGEBNIS_TB-128 übernommen): K2h/K2f; die drei Trägerstellen;
  Fables 29a Abschnitt 1; die Sonnet-Probe; `docs/werkzeuge/registerkopie_abschnitte.py` entfernen
  (Betreiberentscheid fehlt; die Datei liegt noch, gemessen mit `ls`).

Ausserdem nicht angefasst: Register, `docs/VORREGISTRIERUNG_*`, `research/`, `shared/`, `strategies/`, jedes
Werkzeug unter `docs/werkzeuge/`, `REGISTER_INDEX.md`, die Registerkopie, `UEBERGABE*.md` und die `FABLE_*`-Dateien
(`UEBERGABE.md` und `AKTUELLER_AUFTRAG.md` nur in Schritt 0 so committet, wie sie im Arbeitsbaum lagen). Bestehende
Zeilen in den drei Zieldateien: keine geändert oder entfernt (numstat je `n 0`).

## In einfacher Sprache

Die Regeln, die seit dem 4. Oktober nur in der Übergabe standen, stehen jetzt wörtlich im Regelwerk. Die zwei, die
der Betreiber selbst verlangt hat, sind dabei: Der steuernde Chat zieht nur um, wenn der Betreiber es sagt oder
genehmigt — er darf es vorschlagen, aber nicht von sich aus tun —, und er legt die Programmiersitzung auf dem Mac
selbst über den Sitzungswächter an. Dazu kamen vierzehn weitere Prüfhaken, etwa: Uhrzeiten immer messen statt
schätzen, über die Geräteanbindung kein `git diff`, die Ablage erneuert ein Helfer. In der Umzugsanleitung steht ein
neuer Absatz zur Umzugsregel, in der Aufgabenliste ein Block mit dem, was aus den letzten Tagen offen ist. Ein Skript
hat jeden Text aus dem Auftrag eingesetzt, ein zweites, unabhängiges hat nachgeprüft, dass jeder Text genau einmal
und Zeichen für Zeichen gleich dasteht. Am Code, am Register und an den Werkzeugen hat sich nichts geändert.
