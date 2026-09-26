# TB-117: Ergebnis. Bündel „Wachen vor dem Tag“ (Fable 27a) — Register 45.11 und 46 (R9–R17 zeichengleich, 10 Marken, numstat 232/0); Sonde zweiseitig; `herkunft.py` vierte Öffnung (`fehlend` im Modus 2, MANIFEST und Snapshot-`config/` in `EINGEFROREN`); `auswertung.py` prüft `herkunft.json` (R14, Lesart 46.9); neues Abbild `46f0ad5d…`; 46.11 Vollzug

**Sitzungstitel:** `TB-117` · **Stand:** 27.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md` · **Belege:** `docs/belege/TB-117/`
**Eingang:** `8b342ab` (Abgabe TB-116). Commits: `753ec11` (Schritt 0), `4c5615d` (Block A), `42ef509` (Block B),
`ff2f254` (Block C), `852f253` (Block D), `54ce889` (Block E), `33f30e2` (Block E, Nachtrag: Testrunde am sauberen Stand),
der Abgabe-Commit (Block F: 46.11, Journal DP, dieses Dokument). Nach jedem Commit gepusht.
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md`
(md5 `d4367c65a9dcad4b28cceb6f50706d59`, 30 836 Bytes, geprüft). Freigabe des Betreibers 26.09.2026, ca. 22:20
(Auswahlkarte, wörtlich im Auftrag): „Alle vier freigeben (Empfohlen)“.
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6). Kein Abbruchkriterium ausgelöst.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Auftrag, Zeiger, Fable-Antwort committet (`753ec11`), keine weiteren Dateien im Baum. 0b: `register()` `5acb4c19…` (`fehlend` leer, 20 Teile), `herkunft.py` `ed521ac1…`, Sonde `f88e54ee…`, `auswertung.py` `a864b216…` (in TB-116 0b nicht gemessen; gleich dem Eintrag im Abbild `5e5ad109…`), Sonde gegen `5e5ad109…` 34/0/0, Benchmark im Modus `64fb2912…` |
| ⭐⭐ **A** | **45.11** (R11) am Ende von 45 und Abschnitt **46** (46.0–46.10), **10 Marken**. numstat **232/0**, R9–R17 je `diff` **rc 0** (9/9; Mutationsprobe R13 rc 1), **35 Zitate** `diff` rc 0, Sonde gegen `5e5ad109…` vorher = nachher (JSON-Hash `6840f57f…` gleich), `register()` `5acb4c19…` ⇒ **`6bcb4f58…`**, `test_vorregistrierung` **196/196** |
| ⭐⭐ **B** | Sonde vergleicht **zusätzlich** Liste heute (`lies_eingefroren`) ↔ Gruppe `eingefroren` des Abbilds; Befund ⇒ 1 mit Eintrag und Seite. Gegen `5e5ad109…` kein Mengenbefund (19/19); gegen `e655c1c8…` **genau die neun TB-24-Listen „Liste → Abbild fehlt“** (wie R9 erwarten lässt). `sperrlistensonde.py` `f88e54ee…` ⇒ **`98c02e0e…`**, `test_sperrlistensonde` **65/65** (+6: `fall_9`, Mutation „Vergleich aus“ mit Gegenprobe) |
| ⭐⭐ **C** | R10: `register()` und `block()` enden unter dem Modus mit **2**, wenn `fehlend` nicht leer ist (je eigene Fundstelle). R15 (a): `MANIFEST.json` und die beiden Snapshot-`config/`-Kopien in `EINGEFROREN` — **keine dritte Pfadauflösung nötig**. R17 (a): Modulkopf. `herkunft.py` `ed521ac1…` ⇒ **`c6c13388…`**, `register()` ⇒ **`b8f2cc33…`** (23 Teile, `fehlend` leer). `test_ersatzwerte` **77/77** (+7, Teil I), sechs Testannahmen nachgezogen, die alten Fassungen brechen genau dort |
| ⭐⭐ **D** | `auswertung.py` liest `herkunft.json`: unter dem Modus **2** bei jeder der fünf Bedingungen (Meldung: Bot, Feld, erwartet, gefunden); ohne Modus nur Anzeige (Lesart 46.9); Herkunft im **Kopf** des Berichts (Text und `--json`); Docstring `_abbruch_2` berichtigt (R8 (a)). `auswertung.py` `a864b216…` ⇒ **`8ec45123…`**, `register()` ⇒ **`e87a4d8e…`**. `test_ersatzwerte` **99/99** (+22, Teil J), `test_vorregistrierung` **196/196** unverändert |
| ⭐⭐ **E** | Abbild **`sperrliste_abbild_2026-09-26_tb117.json`**, sha256 **`46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f`** (11 432 B, 14 Punkte, `eingefroren` **22** = `EINGEFROREN` 22, HEAD `852f253`; vorher `test -f` rc 1, nichts überschrieben). Sonde dagegen **37/0/0, (ii) 0, kein Mengenbefund**. Gegen `5e5ad109…`: sieben Einträge, **jeder einer Änderung dieses Auftrags zugeordnet**. Unverändert: Benchmark im Modus Repo **und** Klon **`64fb2912…`**, ohne Modus **8/8 bytegleich** (= TB-114 C), Trockenlauf **9 × rc 0**, `faltenplan.json` `0e54ac5c…`, Laufbereich **81** (= TB-114). Probe R13 (a) `shared/test_ausschlussmengen.py` **9/9**. `auswertung.py` im **echten** Modus auf Beispieldaten: gut rc 0 mit Herkunft im Kopf, falscher Datenstand rc 2. Tests am Stand `54ce889`: **44 Dateien, 41 rc 0** (`test_vorregistrierung` 196/196 ohne Zeitgrenze nachgelaufen, `test_ersatzwerte` 99/99, `test_sperrlistensonde` 65/65, `test_ausschlussmengen` 9/9, `test_startpruefungen` 44/44, `test_arbeitsbaum_laufbereich` 26/26, `test_rueckfaelle_modus` 48/48, `test_snapshot` 164/164); ohne rc 0 nur die drei bekannten **ohne Bezug** (`test_drawdown_beide_masse` terminiert nicht, `test_stabile_sortierung` 43/3, `test_wellenauswahl` 322/1 — dieselben Stellen wie TB-114 C) |
| **F** | **46.11** (Vollzug, Tatsachennotiz), numstat **81/0**, Sonde gegen `46f0ad5d…` vorher = nachher, `register()` `e87a4d8e…` ⇒ **`01f5997a9a13b4b30162e2a04965670a9ffa8d725a93d579e530dc0708ec2a70`** (Selbstbezug: dieser Wert steht nur hier, nicht im Register), `test_vorregistrierung` **196/196**. Journal **DP** |

---

## 1. Block A — 45.11 und Abschnitt 46

Bauart TB-114: Vorlage `abschnitt46_vorlage.md` mit Platzhaltern, Einsetzskript `eintrag_register_46.py`
(Quellen `git:753ec11:…` — Fable-Antwort und Auftrag am Stand Schritt 0), Probelauf gegen eine Kopie
(`probelauf.sh`), dann einmal echt. Wachen im Skript: Eingangszeilen 10034, keine Marke in 9 oder 10, Abschnitt 10
unverändert an derselben Stelle, jede alte Zeile in derselben Reihenfolge im neuen Text (additiv).

- **45.11** am Ende von 45 (R11 zeichengleich, samt „Quelle des Grundes“; Kette mit dem Eingangswert des Abbilds).
- **46.0–46.10**: 46.1 R9, 46.2 R10, 46.3 R12, 46.4 R13, 46.5 R14, 46.6 R15, 46.7 R16, 46.8 R17 zeichengleich;
  46.9 Lesart des steuernden Chats (Zitat aus dem Auftrag, zeichengleich eingesetzt); 46.10 das Offene.
- Die **Tatsachennotiz „an Punkt 8“** aus R15 (a) steht in **46.6**, mit Verweis auf Punkt 8, nicht in Abschnitt 10.
- **Fables erstes „Unsicher“** (Sonde auf der Sperrliste oder im Abbild?) ist in 46.1 gemessen: Listentext von
  Abschnitt 10 nennt `sperrlistensonde` 0-mal; das Abbild `5e5ad109…` nennt sie einmal, nur als
  `"parser"` im Feld `erzeugt` — in keinem Punkt, in keiner Gruppe.

**Die zehn Marken** (je neue Zeilen direkt unter dem Anker, der alte Satz zeichengleich):

| Ort | Anker (Anfang der Zeile, innerhalb des Abschnitts genau einmal) |
|---|---|
| 12 | letzte Zeile der TB-108-Marke „(41.1, A7). Die Sätze oben bleiben zeichengleich.“ |
| 16.4 | unter „#### Prüfung vor dem Tag“, hinter „⚠️ **Das Leiter-Skript existiert noch nicht.** Siehe 16.11, Zeile 3.“ — ⚠️ der Anker musste über die Kopfzeile „#### Prüfung vor dem Tag“ gesucht werden, weil das Skript jede `#`-Zeile als Abschnittsgrenze nimmt (erster Probelauf: Abbruch ohne Schreiben) |
| 36.5 | letzte Zeile der TB-113-Marke |
| 40.6 | letzte Zeile der TB-108-Berichtigung „Zitate und Text oben bleiben zeichengleich.“ |
| **40.8 (e)** | ⚠️ **nicht eindeutig im Sinn des Auftrags:** (e) ist eine Tabellenzeile. Die Marke steht als **eigene Tabellenzeile `↳ (e)` direkt unter der Zeile (e)** (Bauart TB-114 an 42.6 (5)) — nicht unter dem Zitat „Zu (d) und (e)“, weil die Zeile (e) der Ort ist, der sagt, dass die Sonde die Gruppen aus dem Abbild liest |
| 41.1 A10 | letzte Zeile des „Stand, gemessen“ von A10 |
| 41.1 A12 | unter der TB-114-Marke von A12 |
| 45.3 | letzte Zeile der Kette von 45.3 |
| 45.7 | letzte Zeile der Kette von 45.7 |
| 45.10 | letzte Zeile von 45.10 (vor 45.11) |

## 2. Block B — die Sonde zweiseitig (R9)

**Gelesen am Stand `8b342ab`/`4c5615d`:** `lies_eingefroren` (Z. 258 ff.) liest `EINGEFROREN` mit `ast` und löst
nach R5 auf; `_pruefe_gruppe` (Z. 418 ff.) prüft die Einträge **aus dem Abbild** gegen die Dateien. Die zweite
Seite fehlte vollständig — der Befund aus TB-114.

**Einbau:** neue Funktion `_vergleiche_eingefroren(abbild, wurzel)` direkt vor `_vergleiche_mit_register`; gerufen
in `pruefen()` **nach** der Schleife über die Gruppen. Ihr Ergebnis wird der Gruppe `eingefroren` als Feld `mengen`
angehängt, ihre Gründe den Gründen der Gruppe; der Ausgang der Gruppe wird mit „1 schlägt 2“ (36.5) verrechnet.
`_pruefe_gruppe` bleibt unverändert (die Prüfung Abbild → Dateien ist dieselbe). Neue Schlusszeile
„Mengenvergleich eingefroren (46.1): Liste heute n / Abbild m, nur in der Liste k, nur im Abbild j [Ausgang]“.
Fehlt die Gruppe im Abbild (vor TB-97), läuft kein Mengenvergleich (die Gruppe ist schon 2); ist die Liste
heute nicht lesbar, ist der Vergleich 2, nie 0.

**Proben** (`test_sperrlistensonde.py`, `fall_9`): 9a frisches Abbild ohne Mengenbefund; 9b ein Eintrag mehr in
`EINGEFROREN` (Kopie) ⇒ 1, „Liste → Abbild fehlt“ mit Eintrag; 9c ein Eintrag weniger ⇒ 1, „Abbild → Liste
fehlt“; 9d Kopie danach wie vorher; 9M Mutation „Vergleich aus“ ⇒ 9b rot, 9M-G Gegenprobe.

**Messung gegen das alte Abbild `e655c1c8…`** (`b_sonde.txt`): Befund in Punkten 11/12 (`herkunft.py`) **und** —
neu — in der Gruppe `eingefroren`: die **neun TB-24-Listen** als „Liste → Abbild fehlt“, „nur im Abbild“ 0.
Das ist genau, was R9 erwarten lässt; kein Befund über die Sonde.

## 3. Block C — `herkunft.py`, vierte Öffnung (R10, R15 (a), R17 (a))

**R10.** Die Messung ist in `_register_messen()` ausgelagert (unverändert); `register()` ruft sie und prüft mit
Fundstelle `register`, `block()` ruft sie und prüft mit Fundstelle `block` — so nennt jede Meldung ihre eigene
Stelle (die Bauart, mit der TB-114 `datenstand` von `block` trennt). Abbruchform: das bestehende
`_abbruch_2(stelle, text)` dieser Datei (`ABBRUCH (herkunft.py::<stelle>): …`, `SystemExit(2)`); die Meldung
nennt die fehlenden Einträge. `paths` wird nur geladen, wenn etwas fehlt — ohne Fehlendes ist der Weg wie vorher.
Ohne Modus: unverändert, `fehlend` ist ein Feld.

**R15 (a), C2 — vorher gemessen** (`c2_pfade.txt`):

| Frage | gemessen |
|---|---|
| Registrierter Snapshot | Register **18**, Z. 2847: `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` |
| Liegen die drei Dateien im Snapshot-Ordner, versioniert? | **ja**, alle drei in `git ls-files` (seit `1075dec`) |
| Pfade genau | `snapshots/63e4b6c8…/MANIFEST.json` (`5cf1103e…`), `snapshots/63e4b6c8…/config/top25_symbols.txt` (`3afc95a4…`), `snapshots/63e4b6c8…/config/sp500_top150.txt` (`6acba892…`); die beiden `config/` bytegleich mit dem Repo |
| Pfadregel TB-114 B1 in `herkunft.py` **und** Sonde | enthält `/`, beginnt nicht mit `ergebnisse/` ⇒ **repo-relativ in beiden**; je Eintrag derselbe absolute Pfad, 22/22 gleich. **Keine dritte Auflösung nötig** — Fables zweites „Unsicher“ ist damit beantwortet |
| Fables drittes „Unsicher“ | Die `config/`-Kopien stecken **nur im Snapshot-Hash** (MANIFEST `dateien_gesamt` 225), **nicht im Datenstand** (`kursdateien` 223, `d9449faf…`) |

**R17 (a).** Der Modulkopf nennt jetzt, was `register()` hasht: die Registerdatei und genau `EINGEFROREN`,
darunter die neun TB-24-Listen (seit TB-114) und MANIFEST samt Snapshot-`config/` (seit TB-117), und dass
`register()`/`block()` unter dem Modus bei Fehlendem mit 2 enden.

**Nachgezogene Testannahmen (Grundsatz 40)** — die alten Fassungen (Stand `42ef509`) gegen die neue
`herkunft.py` brechen genau an diesen Stellen und sonst nirgends (`c_testannahmen_alt.txt`: 62/70 und 63/65):

| Test | alt | neu | warum |
|---|---|---|---|
| `test_ersatzwerte` E-a, F-a, F-a2, F-a3 | Wegwerfbaum trägt nur `herkunft.py` | Wegwerfbaum trägt Registerdatei und alle Einträge von `EINGEFROREN` (`_eingefroren_kopieren`; ohne `ergebnisse/`, wenn E-c den Ordner fehlen lassen muss) | Jeder Modus-Lauf von `block()` im alten Baum endet nach R10 mit 2 — das neue Verhalten, nicht der Gegenstand dieser vier Proben |
| `test_ersatzwerte` H-a, H-a2 | 19 Einträge | 22 | R15 (a) |
| `test_ersatzwerte` H-aM | abweichend = neun TB-24-Listen | + die drei Snapshot-Einträge | unter der alten Regel (`_HIER`) lägen auch sie woanders |
| `test_ersatzwerte` H-b | 20 Teile, Listen am Ende | 23 Teile, Listen an −12…−3, Snapshot-Einträge am Ende | R15 (a) |
| `test_sperrlistensonde` 8a | 19 | 22 | R15 (a) |
| `test_sperrlistensonde` H7f | 34 Pfad-Bestandteile | 37 | R15 (a) |

⚠️ **Reibung mit der Freigabe:** `shared/test_sperrlistensonde.py` ist „nur Block B“ freigegeben; 8a und H7f
brechen aber durch Block C. Nachgezogen im Commit von Block C nach dem Satz des Auftrags „Testannahmen, die
Anzahlen fest kodieren, werden nach Grundsatz 40 nachgezogen“ und nach dem Vorbild TB-114 (dieselben zwei
Zeilen, damals im `herkunft.py`-Block). Zwei Literale, kein Prüfverhalten geändert.

**Neue Proben (Teil I):** I-a Modus + fehlende Datei ⇒ 2 an `register`, Meldung nennt den Eintrag; I-b dasselbe an
`block`; I-Mr/I-Mb Mutation „Wache aus“ ⇒ rc 0 mit `fehlend` gefüllt, je mit Gegenprobe; I-c ohne Modus rc 0 mit
`fehlend` = genau der Eintrag. `register()` im Repo: `fehlend` leer, 23 Teile (H-b).

## 4. Block D — `auswertung.py`, Öffnung (R14, R8 (a), Lesart 46.9)

**Gelesen:** Docstring Z. 51–52 (`herkunft.json` im Vertrag, nirgends gelesen), `main()` (Z. 637 ff.),
`_abbruch_2` (Z. 131 ff.), Register 12 und 36.5.

**Gebaut:**
- `lies_herkunft(wurzel, bots)` und `herkunft_pruefen(wurzel, bots)` (neuer Teil „0. Herkunft“ vor „1. Einlesen“),
  gerufen in `main()` **vor** `ein_bot` — unter dem Modus wird nichts ausgewertet, dessen Herkunft nicht passt.
- Unter dem Modus ⇒ 2 (`_abbruch_2("herkunft_pruefen", …)`), Meldung „<bot>: Feld <f> - erwartet …, gefunden …“:
  Datei fehlt; `TB_SELEKTIONSCOMMIT` kein 7–40-Hex-Bezeichner; Commit nicht mit dem Tag-Commit beginnend (Präfix);
  Datenstand ≠ `REGISTRIERTER_DATENSTAND`; Register-Hash ≠ `herkunft.register()["register"]` zur Laufzeit; ein Feld
  eines Bots ≠ dem des ersten Bots.
- **Registrierter Datenstand:** Konstante `REGISTRIERTER_DATENSTAND = "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84"`,
  Fundstelle **Register 18**, Tabelle „Der gezogene Snapshot“, Zeile „Datenstand (`datenstand_hash`)“ (Z. 2852 am
  Stand von Block A). Die Probe J-r liest den Wert aus dem Registertext und vergleicht.
- Ohne Modus (Lesart 46.9): gelesen, wenn vorhanden, für die ausgewerteten Bots; kein Abbruch; fehlende Dateien
  werden im Kopf genannt.
- **Kopf des Berichts:** Block „HERKUNFT (herkunft.json je Bot; Register 46.5, Lesart 46.9)“ direkt unter der
  Überschrift mit Commit, Datenstand, Register (einheitlich oder je Bot) und dem Hinweis geprüft/angezeigt;
  `--json` trägt das Feld `herkunft`.
- **R8 (a):** der Satz „(`Abbruch` oben endet mit 1 und bleibt, wie er ist.)“ ist **berichtigt** (nicht nur
  gestrichen): „endet seit TB-111 ebenfalls mit 2, Register 44.1 …“.
- `beispieldaten.py` **nicht** geändert: der gute Fall unter dem Modus erzeugt seine `herkunft.json` im
  Wegwerfbaum (Teil J) bzw. im Scratchpad (E).

**Proben (Teil J, 22):** J-1…J-4 je ein Fall ⇒ 2 mit Bot und Feld, je Mutation mit Gegenprobe; J-5 Abweichung
untereinander ⇒ 2 mit Mutation „Vergleich aus“; J-6 ungültiger `TB_SELEKTIONSCOMMIT` ⇒ 2; J-7 auch mit `--bot`
werden alle neun gelesen; J-g guter Fall, Kopf trägt die Herkunft; J-o1 ohne Modus Nullwerte und fehlende Datei
kein Abbruch; J-o2 `auswertung.py` ohne Modus auf Beispieldaten rc 0, Kopf zeigt die Nullwerte; J-o3 ohne
`herkunft.json` rc 0, „fehlt“ im Kopf; J-r Konstante = Register 18. Der Modus ist in Teil J **im Prozess
nachgestellt** (`paths._MODUS`, `TB_SELEKTIONSCOMMIT`), `herkunft.register()` läuft echt; der **echte** Modus-Lauf
steht in E (`e_auswertung_modus.txt`). ⚠️ J-2 bis J-4 setzen den falschen Wert bei **allen neun** Bots — mit nur
einem abweichenden Bot fing der Vergleich untereinander die Mutation auf (erster Lauf: J-2M rot, gemessen), die
Probe hätte nicht allein gebissen.

## 5. Block E — Abbild und Nachmessung

| | gemessen | Beleg |
|---|---|---|
| Abbild | `sperrliste_abbild_2026-09-26_tb117.json`, `46f0ad5d…`, 11 432 B, 14 Punkte, bestimmt 0, eingefroren 22 = `lies_eingefroren` (Reihenfolge und Menge) | `e1_abbild.txt` |
| Sonde gegen das neue Abbild | 37/0/0, (ii) 0, Mengenvergleich 22/22 ohne Befund, rc 2 (nur Regel-Bestandteile) | `e2_sonde.txt` |
| Sonde gegen `5e5ad109…` | rc 1, sieben Einträge — siehe unten | `e2_sonde.txt` |
| Benchmark im Modus | Repo und frischer Klon `64fb2912…` | `e_laeufe.txt` |
| Trockenlauf | 9 × rc 0; `import auswertung` im Modus rc 0 | `e_laeufe.txt` |
| ohne Modus | 8/8 sha256 gleich TB-114 C | `e_g2_ausgaben.txt` |
| `faltenplan.json` | `0e54ac5c…` (= Abbild) | `e1_abbild.txt`, `e2_sonde.txt` |
| Laufbereich | 81 Module, gemeinsam mit TB-112/TB-114 81, neu 0, weg 0; `herkunft.py` nicht darin | `e_laufbereich.txt` |
| `auswertung.py` im echten Modus | Beispieldaten `turtle_soup_stocks`, `herkunft.json` für alle neun: rc 0, Kopf „geprüft“ mit Commit `852f253…`, `d9449faf…`, `e87a4d8e…`; ein Datenstand auf Null ⇒ rc 2 | `e_auswertung_modus.txt` |
| Probe R13 (a) | `shared/test_ausschlussmengen.py` 9/9: vier Mengen je genau einmal (`ast`, nicht importiert), gleich `{PAXGUSDT, XAUTUSDT}`; drei Mutationen je mit Gegenprobe | `e3_ausschlussmengen.txt` |
| Tests | Tests am Stand `54ce889`: **44 Dateien, 41 rc 0** (`test_vorregistrierung` 196/196 ohne Zeitgrenze nachgelaufen, `test_ersatzwerte` 99/99, `test_sperrlistensonde` 65/65, `test_ausschlussmengen` 9/9, `test_startpruefungen` 44/44, `test_arbeitsbaum_laufbereich` 26/26, `test_rueckfaelle_modus` 48/48, `test_snapshot` 164/164); ohne rc 0 nur die drei bekannten **ohne Bezug** (`test_drawdown_beide_masse` terminiert nicht, `test_stabile_sortierung` 43/3, `test_wellenauswahl` 322/1 — dieselben Stellen wie TB-114 C); ⚠️ die Zeitgrenze von 900 s je Datei in `e_tests.sh` war für `test_vorregistrierung` zu knapp (Abbruch in Teil I, kein Befund; ohne Grenze 196/196 in 899 s, `e_test_vorregistrierung.txt`). Ein erster Anlauf lief mit zwei unversionierten Dateien im Baum und wurde nach der ersten Datei abgebrochen; gemessen ist der zweite am sauberen Stand | `e_tests.txt` |

**Sonde gegen `5e5ad109…` — jeder Eintrag zugeordnet:**

| Eintrag | Ursache |
|---|---|
| Punkt 3, 5, 14: `auswertung.py` ABWEICHUNG `8ec45123…` | Block D |
| Punkt 11, 12: `herkunft.py` ABWEICHUNG `c6c13388…` | Block C |
| Gruppe `eingefroren`: `auswertung.py` ABWEICHUNG | Block D |
| Gruppe `eingefroren`: drei × „Liste → Abbild fehlt“ (MANIFEST, zwei `config/`) | Block C (R15 (a)) |

Kein Eintrag ohne Zuordnung. Die Sonde selbst (Block B) steht in keinem Abbild und erscheint deshalb nicht.

## 5a. Block F — 46.11 (Vollzug)

Vorlage `f_46_11_vorlage.md`, Einsetzskript `f_eintrag_46_11.py` (nur Anhängen; Wachen: Eingangszeilen 10266,
46.11 fehlt, 46 ist der letzte Abschnitt, Leser-Wachen wie in A, additiv), Probelauf gegen eine Kopie, dann echt.
numstat **81/0**; Sonde gegen `46f0ad5d…` vorher = nachher (JSON-Hash `9f7364ef…` gleich, 37/0/0);
`register()` `e87a4d8e…` ⇒ `01f5997a…` (steht nach der Selbstbezugsregel nur hier, nicht in 46.11);
`test_vorregistrierung` **196/196**. 46.11 enthält kein Zitat (nur Tatsachen dieser Sitzung), deshalb kein Zitat-`diff`.
Belege: `f_messung_vorher.txt`, `f_eintrag.txt`, `f_numstat.txt`, `f_messung_nachher.txt`,
`f_test_vorregistrierung.txt`.

## 6. Für Fable

**Reibungen zwischen R14 und dem Code (und wie sie im Rahmen der Freigabe gelöst sind):**

1. **R14 schweigt über „ohne Modus“.** Umgesetzt ist die Lesart des steuernden Chats (46.9): Anzeige ohne Abbruch.
   ⚠️ Damit reibt sich **Register 12** („bricht bei jeder Verletzung des Datenvertrags ab“) mit dem Docstring, der
   `herkunft.json` zum Vertrag zählt: ohne Modus ist eine fehlende `herkunft.json` eine Vertragsverletzung ohne
   Abbruch. Bitte 46.9 bestätigen oder anders entscheiden (dann eine weitere Öffnung).
2. **„für jeden Bot“ / „die neun“ bei `--bot`.** Unter dem Modus liest die Prüfung immer alle neun (`rd.BOTS`),
   auch wenn nur ein Bot ausgewertet wird (J-7); ohne Modus nur die ausgewerteten. Bitte bestätigen.
3. **Bedingung 5 (untereinander) ist neben 2–4 fast redundant:** Da 2–4 jede Datei gegen einen festen Sollwert
   prüfen, sind neun Dateien, die 2–4 bestehen, schon gleich — ausser beim **Commit**, der als Präfix verglichen wird
   (kurzer `TB_SELEKTIONSCOMMIT`, zwei verschiedene volle Commits mit gleichem Anfang; J-5). Gebaut wie registriert.
4. **Der registrierte Datenstand hat jetzt drei Orte:** Register 18, `shared/snapshot.py::VERANKERTER_DATENSTAND`,
   `auswertung.py::REGISTRIERTER_DATENSTAND`. Ein Import aus `snapshot.py` hätte `snapshot.py` in den Laufbereich
   von `auswertung.py` gezogen; die Probe J-r bindet die neue Kopie an den Registertext. Plan-Punkt 6 („ein Wert, ein
   Ort“) — Zusammenlegung mit einer späteren Öffnung?
5. **`herkunft` wird in `auswertung.py` erst in `herkunft_pruefen` und nur unter dem Modus importiert.** Deshalb ist
   der gemessene Laufbereich (Lauf-Typ „auswertung“ = nur `import auswertung`) unverändert 81. **Der echte
   Modus-Lauf von `auswertung.py` lädt aber `herkunft.py`** — das betrifft R5 (a)/R4: `herkunft.py` gehört damit
   schon **vor** dem Zellen-Erzeuger zum Laufbereich des Tages, und `ARBEITSBAUM_PFADE` (in `paths.py`, nicht
   freigegeben) führt es nicht. Vorschlag: am Tag-Commit den Lauf-Typ „auswertung“ als echten Lauf messen, nicht
   als Import; die Liste nach R4 vor dem Tag nachziehen.
6. **Register-Hash zur Laufzeit** (Fables fünftes „Unsicher“): gemessen im echten Modus-Lauf — die Prüfung besteht nur,
   wenn zwischen Schreiben der `herkunft.json` und Auswertung weder Register noch eine Datei aus `EINGEFROREN`
   geändert wurde; sonst 2. Dazu kommt: der Commit in `herkunft.json` muss mit `TB_SELEKTIONSCOMMIT` beginnen, und
   die Startprüfung verlangt `TB_SELEKTIONSCOMMIT` = HEAD — **Zellen-Erzeuger und Auswertung müssen am selben
   Commit laufen.** Die Reihenfolge am Tag muss beides wissen.
7. **R8 (a) berichtigt, nicht gestrichen** — der neue Satz nennt den richtigen Ausgang und die Quelle.

**Die Pfade aus C2:** `snapshots/63e4b6c8…/MANIFEST.json`, `…/config/top25_symbols.txt`,
`…/config/sp500_top150.txt` — repo-relativ, in `herkunft.py` und Sonde gleich aufgelöst, keine dritte Auflösung.

**Nachgezogene Testannahmen:** siehe Abschnitt 3 (sechs Stellen, zwei Dateien); in Block D keine.

**Weitere Beobachtungen:**
- `test_sperrlistensonde.py` wurde in Block C angefasst, obwohl „nur Block B“ freigegeben (Abschnitt 3).
- Der Auftrag nannte als 0b-Wert für `auswertung.py` „die Werte aus TB-116 0b“; TB-116 0b hat `auswertung.py` nicht
  gemessen. Der Wert `a864b216…` ist deshalb gegen den Eintrag im Abbild `5e5ad109…` gemessen.
- Die Marke an **40.8 (e)** steht als Tabellenzeile (Abschnitt 1).

**Offen (46.10):** Leiter-Lesarten (TB-116) bei Fable; Listen-Erzeuger (40.6); Zellen-Erzeuger (Stufe V, mit R16
(b)); Stufe IV; Bestätigung 46.9; R15 (b) am Tag-Commit.

## 7. In einfacher Sprache

Fable hatte die Lücken aus den letzten Prüfungen beantwortet; diese Sitzung hat sie geschlossen, ohne an einer
Schwelle oder einem Ergebnis etwas zu ändern.

- **Regelwerk:** Fables neue Textbausteine stehen wörtlich im Register (Abschnitt 45.11 und 46), zehn Hinweise an
  den alten Stellen zeigen dorthin.
- **Prüfwerkzeug:** Es vergleicht jetzt in beide Richtungen — nicht nur „stimmen die Dateien im Abbild noch?“,
  sondern auch „steht im Abbild genau das, was heute festgehalten werden soll?“. Gegen das alte Abbild meldet es
  jetzt genau die neun Handelslisten, die damals gefehlt hätten.
- **`herkunft.py`:** Im Selektionsmodus hält es an, wenn eine festgehaltene Datei fehlt, und es hält jetzt auch die
  Beschreibungsdatei des Datenstands und die beiden Symbollisten des Snapshots fest.
- **`auswertung.py`:** Es prüft endlich, woher die Zahlen kommen — im Selektionsmodus hält es an, wenn Commit,
  Datenstand oder Regelwerk nicht passen, und es schreibt die Herkunft oben in jeden Bericht.
- **Nachgemessen:** Alles, was vorher herauskam, kommt unverändert heraus. Ein neues Abbild ist geschrieben, und die
  Prüfung dagegen ist sauber.
