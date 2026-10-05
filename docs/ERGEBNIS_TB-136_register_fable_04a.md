# TB-136: Ergebnis. Nachmessung der Voraussetzungen am Gerät wie 54.5 (rc 0); Register Abschnitt 54 — Fable 04a (R74–R77) zeichengleich, Tatsachennotizen 54.5–54.6, 15 Marken am alten Ort, numstat 110/0; Registerkopie neu in 55 Abschnittsdateien und 5 Teilen, Index und Dialog-Index nachgezogen

**Sitzungstitel:** `TB-136` · **Stand:** 05.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-136_register_fable_04a.md` ·
**Belege:** `docs/belege/TB-136/`
**Eingang:** `d781f1b` (TB-132, D3; = `origin/main`), Arbeitsbaum wie 0a (elf Einträge). Commits: `753ae38` (Schritt 0,
im Folgenden ⟨S0⟩), `e9bf3c0` (0: Ausgang, Vorprüfung, Nachmessung der Voraussetzungen), `9b7b060` (A: Register,
einziger Registercommit), `d55e7ed` (B/C: BACKLOG, Registerkopie, Index, Dialog-Index), der Abgabe-Commit (D: dieses
Dokument, Journal EE) und ein kleiner Commit mit `d3_porcelain.txt`. Nach jedem Commit gepusht, jeder Push im ersten Versuch.
**⟨S0⟩ im Wortlaut:** `753ae38` · **⟨DATUM⟩ im Wortlaut:** `05.10.2026` (`a4_datum.txt`, gemessen zu Beginn von A4 mit
`TZ=Europe/Berlin date +%d.%m.%Y`; derselbe Tag wie in 0a, kein Tageswechsel während der Sitzung).
**Quelle (md5 am ⟨S0⟩ und im Arbeitsbaum geprüft, `0b_ausgang.txt`):**
`docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md`,
`856b2c158e4bb6870876de129ce71f76`, 29 195 B — gleich dem Soll.
**Freigabe:** Betreiber, 04.10.2026 (Auswahlkarte im steuernden Chat, gestellt gegen 21:00, eingetragen 21:04),
„Freigeben wie beschrieben (Empfohlen)“ (wörtlich im Auftrag). **Keine Rückfrage an den Betreiber.**
**Umgebung:** Mac, Hauptordner `~/trading-bot`, lokal; `trading-env/bin/python3` (3.9.6). Gestartet über den Einfügesatz
`TB-136: …`. Modell laut Selbstauskunft Opus 5.5.
**Kein Abbruchkriterium ausgelöst.**

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a Arbeitsbaum | genau die elf Einträge des Auftrags | genau diese elf (`0a_status.txt`) |
| 0a Skripte | sha256 `2dbc5a55…` (Prüfskript), `99881a1b…` (Einfügeskript) | beide gleich; nach dem Kopieren nach `0d_vorpruefung.py` und `a4_eintrag.py` noch einmal gleich |
| 0a Prüfskript `--arbeitsbaum` | rc 0 | rc 0; `Datum des Eintrags: 05.10.2026 (aus --datum)`, Arbeitsbaum geändert 2 (Soll 2), unverfolgt 12 (Soll 12); die fünf Zeilen `Marken:` … `Bloecke:` und `Dateien:` bis vor `*.py im Baum` wie unter „Prüfsumme“ (`0a_pruefung.txt`; `*.py im Baum: 693`, kein Soll) |
| 0b | 11 471 Z., sha256 `9a2cefb7…`, md5 `1ce393ae…`; `register()` `66480962…`, `fehlend []`, 23 Teile; Abbild `46f0ad5d…`; Sonde rc 2, 37/0/0, (ii) 0, Listentext ja, JSON ohne `zeilen` `9f7364ef…`; Quelle `856b2c15…`/29 195 B; Abschnitt 10 `da8697c0…`, ERZEUGT `fda8ead1…` | alles gleich (`0b_ausgang.txt`); `registerbericht.py --pruefen` rc 1 (bekannt, Vergleichswert); Abschnitt 10 Z. 965–1171, ERZEUGT Z. 260–460 |
| 0c | `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` | leer ⇒ Basis `docs/belege/TB-132/a5_test_vorregistrierung.txt` (196/196), kein eigener Basislauf |
| 0d | rc 0, erste Zeile `Datum des Eintrags: <TT.MM.JJJJ> (aus --datum)`, fünf Zeilen wie „Prüfsumme“, `rc 0: alles wie angegeben` | genau so; `*.py im Baum: 695` (693 + die zwei Skripte der Sitzung) (`0d_vorpruefung.txt`) |
| ⭐⭐ 0e | jede `ok`/`FEHL`-Zeile beginnt mit `ok`; `rc 0: Voraussetzungen wie in 54.5`, `rc 0` | **25 von 25 Zeilen `ok`**, beide Schlusszeilen wie Soll (siehe unten) |
| A4 | `git diff --quiet ⟨S0⟩ -- Auftrag Quelle` rc 0; Probelauf an Kopie grün, dann echt, `cmp` gleich; `15 an 15`, `4 (R74-R77)`, `11471 → 11581, 110` | rc 0; Probelauf und echter Lauf je genau diese Ausgabe, `sha256 nachher:` in beiden `8d505a38…`; `cmp` rc 0; die Wache zu R74 (b) lief in beiden Läufen |
| A5 R-Diff | 4/4 rc 0; Mutation rc 1 | **4/4**; Mutation (R74 unter 54.1, „ die “ → „ der “) rc 1 |
| A5 Zitate | 2/2 | Kopf 54.0 und Schluss 54.5–54.6 **2/2** |
| A5 Überschriften/Ketten, Marken | 4/4, 15/15 | **4/4 und 4/4**, **15/15**, jede Markenzeile einmal; in Abschnitt 9, 10 und ERZEUGT-Block je 0; Zeilen nachher gleich der Tabelle in A5 (15/15) |
| A5 numstat, Zeilen | `110	0`, 11 581 | **110/0**, 11 581 |
| A5 Abschnitt 10, ERZEUGT | bytegleich gegen 0b | beide gleich (Z. 965–1171 und 260–460, unverschoben) |
| A5 `registerbericht --pruefen` | nachher = vorher | rc 1 / rc 1, Ausgabe bytegleich |
| A5 Sonde | JSON ohne `zeilen` gleich, (ii) 0, Listentext ja | `9f7364ef…` gleich, (ii) 0, ja; auch der Text bytegleich |
| A5 `register()` | ≠ vorher, `fehlend []`, 23 Teile | `cfff54ca…`, `[]`, 23 |
| A5 `test_vorregistrierung` | 196/196, am echten Register vor dem Commit, ohne Zeitgrenze | **196/196**, rc 0, 940 s (`a5_test_vorregistrierung.txt`) |
| B | Anker 1, erste Textzeile nachher 1, numstat `10	0`, Block bytegleich | Anker 1 (Z. 286), erste Textzeile vorher 0 / nachher 1, **10/0**, GLEICH (1 332 B, 9 Zeilen, Leerzeile davor/danach, Anker danach) |
| C1 | fünf Aufrufe rc 0; 55 Abschnittsdateien `_00`–`_54`; erwartet ein fünfter Teil | alle fünf rc 0; Teile 0–22 / 23–36 / 37–42 / 43–53 / **54**, bytegleich; **55** Abschnittsdateien, bytegleich (siehe „Registerkopie“) |
| C2 | Index nachgezogen (Liste Nr. 1 bis 9, Abschnitt 9, Pflegezeile) | 278 Zahlen in Zeilenangaben umgeschrieben (150 geändert), 9 Ersetzungen und 4 Tabellenzeilen je Anker 1, neue Zeile 54 in Tabelle 4, Abschnitt 9 mit 15 Marken, Abschnittstabelle 0–54 aus den Köpfen |
| C3 | vorher `Indexzeilen aus Fable 04a` 0; zwei Zeilen zeichengleich | 0 vorher (vor C2 und vor C3 gezählt); Block eingesetzt, 2/2 zeichengleich |
| C2/C3 Gegenprobe | — | 308/308 Zeilenangaben auf Markenzeilen; 14/14 (Abschnitt 6), 12/12 (7), 21/21 (8), 15/15 (9); C3 zeichengleich; Indexzeilen 01a 5; 55/55 Tabellenzeilen; Indexzeilen E-2 6 (`c2_index_pruefen.txt`) |
| C4 | `--pruefen` rc 0; 55 Antworten; 04a Fundstelle 54, offen; 02c Fundstelle 53, registriert, Frage/Entscheidung unverändert | rc 0 / rc 0; genau so; Schlüssel `04a` wie erwartet; „55 Antworten.“; numstat 3/2: Zeile 02c (Status, offen), neue Zeile 04a, Schlusszeile — **keine weitere Zeile geändert** |

## Nachmessung der Voraussetzungen (0e; R74 (b), R75 (a), R75 (g))

Aufruf genau wie im Auftrag, einmal, aus der Repo-Wurzel (`docs/belege/TB-136/0e_voraussetzungen.txt`). Endet mit
`rc 0: Voraussetzungen wie in 54.5` und `rc 0`. Das Feld `kalender` im Wortlaut:

```
{"im_repo": [{"import": "pandas_market_calendars", "modul": "notifications/boersenkalender.py", "zeile": 81}], "in_selektionshuelle": [], "paket_vorhanden": "5.4.0"}
```

Die Zeilen der Ausgabe (gekürzt auf Name und Ist; jede beginnt mit `ok`):

| Gruppe | Messung | Ist |
|---|---|---|
| V1, R74 (b) | `im_repo[0].modul` | `notifications/boersenkalender.py` — **die Voraussetzung trifft zu** |
| | Zahl der Einträge in `im_repo` / `import` / `zeile` | 1 / `pandas_market_calendars` / 81 |
| | `in_selektionshuelle` / `paket_vorhanden` | `[]` / `5.4.0` |
| | Kalendername (NYSE, XNYS) im Feld | `[]` |
| Tatsachen zu R74 (b) | `boersenkalender.py` Z. 70 / 81 / 109 | `KALENDER_NAME = "NYSE"` / `import pandas_market_calendars as mcal` / `_KALENDER = mcal.get_calendar(KALENDER_NAME)` |
| | `git grep -n 'pandas_market_calendars' -- '*.py'` | rc 0, 13 Zeilen; Import-Anweisungen genau `notifications/boersenkalender.py:81`; unter `research/vorregistrierung/` kein Treffer |
| | `requirements.lock` Z. 51 | `pandas-market-calendars==4.6.1` |
| V2, R75 (a) | `research/mtm_drawdown/mtm_kern.py` | 339 Zeilen; Z. 210 `buch = np.where(k > 0, kapital_after[…], …)`; Z. 244, 246, 251 wie Soll |
| V3, R75 (g) | Register Abschnitt 8 (Z. 870–924) | 13 Tabellenzeilen; `zellenbericht` 0 |
| Tatsachen zu R75 (b), (d), (g) | `research/vorregistrierung/auswertung.py` | 860 Zeilen; Z. 46 `datum, netto_rendite, exposure`; `kapital_drawdown_mtm_pct`, `zellenbericht`, `bestaetigung_ab_effektiv` je 0 |

Gelesen wurde nur, was der Aufruf liest (Sichtschutz 27.1: aus `eingaben.json` nur das Feld `kalender`). Damit trägt
54.5 keine Zahl, die am Gerät nicht stimmt. V2 trifft im Wortlaut nicht (so steht es in 54.5); das hält den Eintrag nach
R75 (a) nicht auf. `git status --porcelain` danach: neu nur Dateien unter `docs/belege/TB-136/`.

## `herkunft.register()`

| | Wert |
|---|---|
| vorher (Register `9a2cefb7…`, 11 471 Z.) | `664809629137b537d233e19066ac6ab9d422c64be8841ff37c72862e0eb511b3` |
| nachher (Register `8d505a38…`, 11 581 Z.) | `cfff54ca81d3dbf594a28880b17d4ba8389e0436c2d48cd50248586c1de03a81` |

`fehlend []` und 23 Teile vorher wie nachher. Der neue Wert steht nur hier, nicht im Register (42.5).

## Register nachher

11 581 Zeilen · sha256 `8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc` ·
md5 `757cda8cb86e7c43fa6342ca41e56765` — gerechnet mit ⟨S0⟩ = `753ae38` und ⟨DATUM⟩ = `05.10.2026`; Probelauf an der
Kopie und echter Lauf nennen denselben sha256, `cmp` rc 0. Abschnitt 54 steht in Z. 11518–11581 (54.1 Z. 11522, 54.2
Z. 11529, 54.3 Z. 11536, 54.4 Z. 11543, 54.5 Z. 11550, 54.6 Z. 11566). ⟨S0⟩ ist im Register als `` `753ae38` ``
eingesetzt (zweimal im Kopf), das Datum einmal im Kopf („Eingetragen am 05.10.2026.“) und in jeder der 15 Markenzeilen.

## Wie eingetragen

- Einfügeskript aus Anhang A, unverändert (`a4_eintrag.py`, sha256 `99881a1b…`), Probelauf mit `--s0 753ae38 --datum
  05.10.2026 --register <Kopie im Scratch>` über `a4_probelauf.sh`, danach echt mit `--s0 753ae38 --datum 05.10.2026
  --daten docs/belege/TB-136/a4_eintrag_daten.json`. `--vorschau` nicht benutzt.
- Nachweise nach der Bauart TB-132 (`a5_r_diff.py`, `a5_mutation.py`, `a5_zitate.py`, `a5_marken.py`, `a5_nachweis.sh`),
  umgestellt nach der Tabelle „Übernommene Skripte“ (54, R74–R77, 04a, 15, 4, TB-136); sie lesen Auftrag und Quelle selbst
  per `git show 753ae38:…`.
- Ausgang und Nachher-Messung mit demselben Skript `0b_ausgang.sh` (Vorlage TB-132), `vorher` bzw. `nachher`
  (`a5_messung_nachher.txt`, mit den Vergleichen vorher/nachher am Ende).
- `test_vorregistrierung` lief mit `nohup` im Hintergrund am echten Register vor dem Commit A; währenddessen liefen nur
  lesende Prüfungen und das Vorbereiten der B/C-Skripte, ohne Schreiben in BACKLOG, Index oder Kopie.
- Index: `c2_index_zeilen.py` (Abbildung über die unveränderten alten Zeilen, ⟨S0⟩ → `9b7b060`), `c2_index_04a.py`
  (Tabelle für Abschnitt 9 aus `c1_marken.txt` und Anhang A; Datum als Argument), `c2_index_eintraege.py`, `c3_indexzeilen.py`,
  Gegenprobe `c2_index_pruefen.py` (Aufruf jetzt `<S0> <datum>`). **Anders als die Vorlage** liest `c2_index_eintraege.py`
  die neuen Texte der C2-Liste Nr. 1 bis 7 und den Vorspann von Abschnitt 9 aus dem Auftrag am ⟨S0⟩ (Codespannen der
  Listenpunkte bzw. der Codeblock), statt sie abzutippen; eingesetzt werden nur `{Zn}` und `{T}`. Der Vorspann ist wie in
  Abschnitt 8 umbrochen (Breite 118, an Leerzeichen). Kopf, „Wie gemessen“ und Pflegezeile stehen als Text im Skript.
- Dialog-Index: `c4_handfelder.json` aus dem Codeblock des Auftrags am ⟨S0⟩ geschnitten (`cmp` gegen den Auftrag: ja),
  dann `c4_dialog_index.sh`.

### Was an Index Z. 5 und im Absatz „Frühere Vierteilung“ geschrieben ist

- Index Z. 3–5 (Kopf): „am Commit `9b7b060` (05.10.2026), Abschnitte 0–54, 11 581 Zeilen, sha256 `8d505a38…`. … nachgezogen
  in TB-126 (E-2), TB-129 (Fable 01a), TB-130 (Fable 02a), TB-132 (Fable 02c) und TB-136 (Fable 04a). … `_54.md` (Tabelle
  unten; dazu die Teile `REGISTER_KOPIE_teil1–5.md`).“
- Index Z. 76: Kopf unverändert „*Frühere Vierteilung* (bis 01.10.2026; „T1“ … „T4“ in den Tabellen unten bezeichnen sie,
  massgeblich sind Abschnitt und Z.):“, danach „T1 = 0–22 (Z. 1–3854), T2 = 23–36 (Z. 3855–6896), T3 = 37–42 (Z. 6897–9537),
  T4 = 43–53 (Z. 9538–11517), T5 = 54–54 (Z. 11518–11581).“
- **Für später (TB-133):** Die Bezeichnung „Frühere Vierteilung“ und „T1 … T4“ passen nicht mehr zu fünf Teilen; der Kopf
  bleibt nach dem Auftrag zeichengleich, weil drei übernommene Skripte an diesem Literal hängen.

## Registerkopie

| Teil | Abschnitte | Bytes | vorher (TB-132) |
|---|---|---|---|
| T1 | 0–22 | 220 538 | 220 240 (+298, die Marken in 16.6 und 17.5) |
| T2 | 23–36 | 222 495 | 222 495 |
| T3 | 37–42 | 232 429 | 232 429 |
| T4 | 43–53 | 234 587 | 232 545 |
| **T5** | **54** | **24 706** | neu |

Der Zuschnitt ist der gerechnete aus C1 (T4 „rund 234 587 B“, T5 „rund 24 706 B“ — beide auf das Byte); kein Abschnitt
0–53 wechselt den Teil, die Spalte T im Index bleibt für 0–53 gleich. `REGISTER_KOPIE_teil5.md` ist neu und im Commit B/C.
Bodies aneinander 933 576 B, bytegleich mit dem Register am `9b7b060` (`c1_registerkopie.txt`, `c1_pruefen.txt`,
`c1_abschnitte_pruefen.txt`). Abschnittsdatei `_54.md` 24 726 B.

## Markentabelle (gegen Anhang A)

| Nr | alter Ort (Anhang A) | nach Z. (alt) | Marke Z. (neu) | Wort | durch | Art | T |
|---|---|---|---|---|---|---|---|
| 1 | 16.6 | 2348 | 2350 | PRÄZISIERT | R75 (54.2) | MARKE | 1 |
| 2 | 17.5 | 2840 | 2845 | ERGÄNZT | R74 (54.1) | MARKE+ | 1 |
| 3 | 48.1 (R33) | 10795 | 10803 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 4 | 48.2 (R34) | 10802 | 10813 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 5 | 48.4 (R36) | 10816 | 10830 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 6 | 48.5 (R37) | 10826 | 10843 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 7 | 48.7 (R39) | 10846 | 10866 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 8 | 48.14 (R46) | 10895 | 10918 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 9 | 51.5 (R60) | 11239 | 11265 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 10 | 52.2 (R64) | 11331 | 11360 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 11 | 53.1 (R66) | 11385 | 11417 | PRÄZISIERT | R74 (54.1) | MARKE | 4 |
| 12 | 53.3 (R68) | 11399 | 11434 | PRÄZISIERT | R75 (54.2) | MARKE | 4 |
| 13 | 53.4 (R69) | 11406 | 11444 | ERGÄNZT | R75 (54.2) | MARKE+ | 4 |
| 14 | 53.5 (R70) | 11413 | 11454 | PRÄZISIERT | R77 (54.4) | MARKE | 4 |
| 15 | 53.9, nach der Tabelle | 11454 | 11498 | ERGÄNZT | R74 (54.1) | MARKE+ | 4 |

Quelle: `a4_eintrag_daten.json`, `a5_marken.txt`, `c1_marken.txt`, `c2_index_04a_tabelle.md`. 15 Marken an 15
Einfügestellen; die Zeilen nachher gleichen der Soll-Tabelle in A5 (15/15). Nr. 1, 2, 4–7, 9–15 zählt R77 (a) auf;
Nr. 3 und Nr. 8 hat der steuernde Chat nach R65 (a) bestimmt (Kopf 54.0, 54.6 Nr. 6). **Nicht gesetzt nach Anhang A
(wie vorgesehen):** 48.20 (R52) (Indexzeile, Abschnitt 9 des Index), 53.10, 50.2, 29.3, 41.3, 35.1, 27.2; keine Marke in
Abschnitt 9, 10 und im ERZEUGT-Block.

## Für Fable (nur Verfahrensfragen)

1. **54.6 Nr. 2:** Die Voraussetzung zu R75 (a) trifft im Wortlaut nicht: `mtm_kern.py` bildet Kapitalreihen
   (`mtm = buch + unreal`), keine Tagesrendite; Realisiertes kommt über `kapital_after` und ist dort nicht je Position
   geführt. Frage: wie der Zellen-Erzeuger den Beitrag einer Position bildet — vor dem Bau der Attribution.
2. **54.6 Nr. 6, zur Kenntnis:** die zwei Marken des steuernden Chats an 48.1 (R33, PRÄZISIERT durch R75 (c)) und 48.14
   (R46, ERGÄNZT durch R75 (d) und (f)); R77 (a) nennt sie nicht. Dazu: R60 (c), R64 (c)/(d), R66 (b)/(e) und R67 geben der
   Abnahme nach R46 ebenfalls eine Prüfung, 48.14 trägt dafür keine Marke.
3. **54.6 Nr. 7, zur Kenntnis:** die sechs sinngemässen Verweise aus 54.5 (letzte Zeile).
4. **54.6 Nr. 9, zur Kenntnis:** das Leseprotokoll der Antwort 04.10.a (ein `BACKLOG.md`-Ausschnitt aus der Suche der
   Ablage, gesehen und nach R56 (b) genannt; kein eigener Block nach R56 (c)).
5. **54.6 Nr. 10:** Trade-Zahl und ereignisindizierter Drawdown der Zeile im Deckelfall; welcher Handelstag der Deckeltag
   ist, legt R75 nicht fest.
6. **Reibung beim Setzen, Werkzeug (wie TB-129, TB-130, TB-132):** `registerkopie.py --marken` zählt in Abschnitt 54 drei
   Zeilen als Marken, die keine sind: die Blockzeile von R76 (Z. 11538, `MARKE+`, sie nennt „ERSETZT-Marke“), die
   Blockzeile von R77 (Z. 11545, `MARKE`, „PRÄZISIERT durch“) und 54.6 Nr. 6 (Z. 11575, `MARKE`, „PRÄZISIERT durch R75 (c)“);
   dazu drei Überschriften mit Rückverweis (54.1, 54.2, 54.4). Damit stehen die Arten bei `MARKE` 95 = 84 + 9 + 2,
   `MARKE+` 128 = 121 + 6 + 1, `UEBERSCHRIFT` 91 = 88 + 3 — genau wie im Auftrag erwartet. Im Index ist keine der drei
   Zeilen als Marke geführt.
7. **Keine Reibung zwischen Fable-Text und Code oder Register gefunden**, die über 54.5 hinausgeht: alle 25 Messzeilen
   aus 0e trafen das, was 54.5 nennt.

## Nicht getan

- 54.6 (alle zehn Punkte): Verfahrensmessung in der Lock-Umgebung am Snapshot nach R74 (e) mit R72 (d) (Nr. 1, 8),
  Anfragen an Fable (Nr. 2, 6, 7, 9, 10), Zellen-Erzeuger mit Kalender, zweitem Spaltenpaar, Wache und Zählung (Nr. 3),
  Öffnung von `auswertung.py` nach R69 (b) (Nr. 4), Abnahme nach R46 mit Deckelfall (Nr. 5).
- Die Ablage (55 Abschnittsdateien, fünf Teile, `REGISTER_INDEX.md`, `FABLE_DIALOG_INDEX.md`) — macht der steuernde Chat.
- Kein Code, kein neues Abbild, keine Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests; die Dateien unter
  `vormessung/`, `TB-133/`, `TB-134/`, `TB-135/` und die `FABLE_*`-Quellen nicht geändert (nur in Schritt 0 committet).
- `registerbericht.py --pruefen` rc 1 bleibt (schon vor TB-126; Zahlenteil veraltet).

## Nebenbemerkungen zum Ablauf

- Datum des Eintrags ist der 05.10.2026, nicht der Tag der Freigabe (04.10.2026) — so vom Auftrag vorgesehen.
- `test_vorregistrierung` brauchte 940 s statt 892 s (TB-132), vermutlich weil parallel die lesenden Nachweise liefen.
- Der Index-Diff ist mit 193/155 gross, weil `c2_index_zeilen.py` 150 Zeilenangaben auf den neuen Stand umschreibt
  (Marken in 16.6 und 17.5 verschieben fast alles); inhaltlich neu sind nur die Einträge aus C2/C3.
- T4 steht jetzt bei 234 587 von 240 000 B; der nächste Abschnitt kommt nach dem gierigen Zuschnitt in T5.
- Der Zeilenzähler der Sonde (`git status --porcelain` vorher/nachher) zeigt 6 bzw. 18 Zeilen: die Belege der Sitzung.

## In einfacher Sprache

Die Sitzung hat zuerst die Unterlagen des steuernden Chats ins Repo gesichert. Dann hat sie am Betriebsrechner
nachgemessen, ob die Code- und Registerstellen so aussehen, wie es die Vormessung beschreibt — alle 25 Messpunkte
stimmten. Erst danach hat sie Fables vier neue Regeltexte vom 04.10. Zeichen für Zeichen ins Register kopiert, als
Abschnitt 54, mit der Tabelle der Messungen und der Liste der offenen Punkte. An 15 alten Stellen weist eine kleine Marke
auf die neuen Texte. Kein alter Satz wurde geändert (110 Zeilen dazu, 0 weg). Alle Prüfungen und der grosse
Registertest (196/196) sind grün. Danach sind die Kopie des Registers für die Ablage (jetzt 55 Dateien und fünf Teile),
der Wegweiser und die Liste der Fable-Antworten neu erzeugt. Am Code hat sich nichts geändert.
