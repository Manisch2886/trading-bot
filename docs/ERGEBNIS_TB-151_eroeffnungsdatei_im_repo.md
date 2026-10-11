# TB-151: Ergebnis. Eröffnungsdatei des steuernden Chats verfolgt unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, `docs/werkzeuge/ablage_soll.py` führt sie als B2 Stand (ein Name in `STAND`), sechs Läufe mit 0 Fehlern, BACKLOG- und Journalblock (EP)

**Sitzungstitel:** `TB-151 Eröffnungsdatei im Repo` · **Stand:** 11.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-151_eroeffnungsdatei_im_repo.md` ·
**Belege:** `docs/belege/TB-151/` · **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9.6)
**Sichtschutz 27.1:** Keine Ergebnisgrössen des Selektionsraums. Die Sitzung hat keine Kennzahl, keine Trade-Liste und keine
Datei unter `research/` gelesen oder erzeugt; die Läufe arbeiten nur auf Dateinamen unter `docs/` und einer künstlichen Ist-Liste.
**Eingang:** `fa40ccb` (= `origin/main`), Arbeitsbaum wie 0a (sieben Einträge). Commits: `82120cf` (Schritt 0, ⟨S0⟩),
`c462c08` (A: Skripte, Läufe mit der Vorfassung), `f204955` (B: Werkzeug allein, ⟨B⟩), `45d07ec` (B: Belege),
`011efc7` (C: Datei allein, ⟨C⟩), `64fed51` (C: Belege), der Abgabe-Commit (BACKLOG, Journal, dieses Dokument) und ein
kleiner Commit mit `d4_numstat.txt` und `d4_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**⟨KENNUNG⟩** `EP` · **⟨FOLGEKENNUNG⟩** `EQ` · **⟨DATUM⟩** `11.10.2026` (zur Laufzeit gemessen mit `date +%d.%m.%Y`).
**Rückfragen an den Betreiber:** keine. **Abbruchkriterium:** keines ausgelöst.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `fa40ccb9c12d3fa554676c76aa5327c12b9e68a1`, sieben Einträge wie im Auftrag | gleich (`0a_head.txt`, `0a_status.txt`); beide `cmp` gleich; ⟨S0⟩ = `82120cf` |
| 0b | md5 `379f2472…` · `004bf1d2…` · `46c6a180…` · `769588e7…` | alle vier gleich, im ersten Versuch (`0b_md5.txt`); laeufe.py 6 481 B, aendere.py 1 709 B; danach neu nur `docs/belege/TB-151/` |
| A | rc 0, 3 × `ok`, 0 × `FEHL`, `ERGEBNIS alt: 0 Fehler \| Python 3.9.<x>` | rc 0, 3 × `ok`, 0 × `FEHL`, `ERGEBNIS alt: 0 Fehler \| Python 3.9.6` |
| B (aendere.py) | die zwei Soll-Zeilen wörtlich | wörtlich gleich (`b_aendere.txt`); md5 nachher `2d050828f6cf80b2f95196955828e8c7`, 14 652 B; keine `ablage_soll.py.tb151.neu` liegen geblieben |
| B (Lauf) | rc 0, 7 × `ok`, 0 × `FEHL`, `ERGEBNIS fehlt: 0 Fehler \| Python 3.9.<x>` | rc 0, 7 × `ok`, 0 × `FEHL`, Python 3.9.6 |
| B (numstat) | eine Zeile `3 1 docs/werkzeuge/ablage_soll.py` | gleich (`b_numstat.txt`); ⟨B⟩ = `f204955` |
| C (Kopie) | zwei Zeilen, beide `769588e7c4234ccfe694106a40c761e5` | gleich (`c_kopie.txt`) |
| C (Lauf) | rc 0, 9 × `ok`, 0 × `FEHL`, `ERGEBNIS neu: 0 Fehler \| Python 3.9.<x>` | rc 0, 9 × `ok`, 0 × `FEHL`, Python 3.9.6 |
| C (git) | `git add` ohne Meldung „ignoriert“, `c_verfolgt.txt` eine Zeile | `git add` ohne Meldung; `c_verfolgt.txt` = `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`; ⟨C⟩ = `011efc7` |
| D1 | Anker `## 6 — Geparkt, null Arbeit` genau einmal; numstat `7 0` | Anker einmal (Z. 404 von 415); numstat `7 0` |
| D2 | Anker `## Wiederkehrende Lehren` genau einmal; Kennung EP; numstat `24 0` | Anker einmal (Z. 10455); letzter Block EO, gesetzt EP; numstat `24 0` |

## Die Läufe, wörtlich

`a_laeufe_alt.txt`:

```text
ok   Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/
0 | rc 0 | Ist 0 | Soll 52 | entfernen 0 | bleibt 0 | ablegen 52 | ohne Regel 0
ok   Basis: Pfade aus dem Soll der Vorfassung, die Datei ist nicht darunter
alt_mit | rc 0 | Ist 56 | Soll 52 | entfernen 2 | bleibt 52 | ablegen 0 | ohne Regel 2
ok   alt_mit: die Datei steht nur in ohne_regel.txt, Grund 'keine Regel'
ERGEBNIS alt: 0 Fehler | Python 3.9.6
```

`b_laeufe_fehlt.txt`:

```text
ok   Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/
neu_fehlt | rc 0 | Ist 55 | Soll 53 | entfernen 2 | bleibt 52 | ablegen 1 | ohne Regel 1
ok   neu_fehlt: die Datei steht in soll.txt und ablegen.txt, blanker Name, Grund 'B2 Stand - FEHLT IM REPO'
ok   neu_fehlt: Soll +1, ablegen +1, Ist -1, ohne Regel -1, bleibt und entfernen wie alt_mit
ok   Gegenprobe soll.txt: die uebrigen 52 Zeilen sind gleich in alt_mit, neu_fehlt
ok   Gegenprobe entfernen.txt: die uebrigen 2 Zeilen sind gleich in alt_mit, neu_fehlt
ok   Gegenprobe ablegen.txt: die uebrigen 0 Zeilen sind gleich in alt_mit, neu_fehlt
ok   Gegenprobe ohne_regel.txt: die uebrigen 1 Zeilen sind gleich in alt_mit, neu_fehlt
ERGEBNIS fehlt: 0 Fehler | Python 3.9.6
```

`c_laeufe_neu.txt`:

```text
ok   Voraussetzung: die Datei liegt unter docs/projektfuehrung/
neu_mit | rc 0 | Ist 56 | Soll 53 | entfernen 2 | bleibt 53 | ablegen 0 | ohne Regel 1
neu_ohne | rc 0 | Ist 55 | Soll 53 | entfernen 2 | bleibt 52 | ablegen 1 | ohne Regel 1
ok   neu_mit: die Datei steht nur in soll.txt, mit Ablagepfad, Grund 'B2 Stand'
ok   neu_mit: bleibt +1, Soll +1, ohne Regel -1, sonst wie alt_mit
ok   neu_ohne: die Datei steht in soll.txt und ablegen.txt, mit Ablagepfad, ohne 'FEHLT IM REPO'
ok   neu_ohne: ablegen +1, Ist -1, ohne Regel -1, Soll wie neu_mit, bleibt und entfernen wie alt_mit
ok   Gegenprobe soll.txt: die uebrigen 52 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ok   Gegenprobe entfernen.txt: die uebrigen 2 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ok   Gegenprobe ablegen.txt: die uebrigen 0 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ok   Gegenprobe ohne_regel.txt: die uebrigen 1 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ERGEBNIS neu: 0 Fehler | Python 3.9.6
```

`c_laeufe_datiert.txt` (Tatsachennotiz, kein Soll):

```text
Notiz Voraussetzung: Datei unter docs/projektfuehrung/ ja
neu_datiert | rc 0 | Ist 57 | Soll 53 | entfernen 3 | bleibt 53 | ablegen 0 | ohne Regel 1
Notiz entfernen.txt: projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT_2026-10-10.md	B2 datierte Fassung - EROEFFNUNG_STEUERNDER_CHAT.md liegt im Repo
Notiz Zahlen gegen neu_mit: Ist +1, Soll +0, entfernen +1, bleibt +0, ablegen +0, ohne Regel +0
ERGEBNIS datiert: 0 Fehler | Python 3.9.6
```

Die Phase `datiert` stimmt mit der Messung am Gerät überein: gleiche Notizzeilen, gleiche Unterschiede gegen `neu_mit`.

## Abweichungen vom Auftrag

- **Zahlen der Läufe:** Ist, Soll und bleibt liegen am Mac durchweg um 1 höher als am Gerät (Vorlauf `0`: Soll 52 statt 51).
  Der Auftrag hat das erwartet („mindestens um diesen Auftrag, der dann unter `docs/auftraege/` liegt“) und nennt es
  ausdrücklich kein Abbruchkriterium. Alle Unterschiede zwischen den Läufen sind gleich wie am Gerät.
- **Arbeitsweise, keine Abweichung im Ergebnis:** Die zwei Python-Blöcke (0b) und die zwei Anhang-Blöcke (D1, D2) hat die
  Sitzung nicht abgetippt, sondern mit einem kurzen Python-Aufruf aus dem Auftragsdokument geschnitten und geschrieben; in
  den Anhang-Blöcken hat sie nur ⟨KENNUNG⟩, ⟨FOLGEKENNUNG⟩ und ⟨DATUM⟩ ersetzt und die Blöcke vor den Anker gesetzt, mit einer
  Leerzeile danach. Nachweis der Zeichengleichheit: md5 in `0b_md5.txt` und die numstat-Zahlen aus D1/D2.
- Sonst keine.

## Nicht getan

- `UMZUG.md`, `ARBEITSWEISE.md` (TB-152), `ablage_ereignisse.json`, `.gitignore`, alles unter `logs/` (nur gelesen).
- Die Kopie unter `logs/steuernder_chat/` bleibt liegen.
- Kein Abgleich mit der echten Ablage, nichts abgelegt (steuernder Chat).
- Die festen Monatsangaben `2026-09-` in `ablage_soll.py` (Nebenbefund, eigener Auftrag).
- Kein Lauf gegen Daten oder eine db (ARBEITSWEISE 7c nicht einschlägig).

## In einfacher Sprache

Der Eröffnungstext, den jeder neue steuernde Chat zuerst liest, liegt jetzt gesichert im Repo unter
`docs/projektfuehrung/`, als genaue Kopie (gleiche Prüfsumme) der bisherigen Datei. Das kleine Werkzeug, das die Soll-Liste
für die Projektablage erstellt, kennt jetzt den Namen dieser Datei: Liegt sie im Repo, gehört sie in die Ablage; fehlt sie
dort, sagt das Werkzeug das; vorher hiess es nur „passt zu keiner Regel“. Sechs Probeläufe mit einer künstlichen Liste
haben das gezeigt, und für alle anderen Dateien dieser Liste hat sich nichts verändert. An den Handelsprogrammen und an
den Daten hat sich nichts geändert.
