# TB-114: Ergebnis. Register 45 (Fable 26a, R1–R8 zeichengleich, 11 Marken, numstat 218/0); `herkunft.py` dritte Öffnung (B1 eine Pfadregel mit der Sonde, `register()` vorher = nachher; B3 neun TB-24-Listen in `EINGEFROREN`, `fehlend` leer; B4 `datenstand(None)` im Modus 2); neues Abbild `5e5ad109…` (Sonde 34/0/0); ⚠️ **Abbruchkriterium in Block C: Die Sonde meldet gegen das alte Abbild nur den Hash von `herkunft.py`, die neun neuen Einträge nicht — Block D (45.11) entfällt**

**Sitzungstitel:** `TB-114` · **Stand:** 26.09.2026, ca. 18:15 · **Auftrag:**
`docs/auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md` · **Belege:** `docs/belege/TB-114/`
**Eingang:** `0df8c64` (Abgabe TB-113). Commits: `79c2dfa` (Schritt 0), `77147f7` (Block A, Register 45), `0b7ab4b`
(Block B, `herkunft.py` und Tests), `e07fefd` (Block C, Abbild und Nachmessung), der Abgabe-Commit (Journal DM, dieses
Dokument). **Block D entfällt** (Abbruch). Nach jedem Commit gepusht.
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md`
(md5 `e2a492165d44f6ee3d02eba99d2acf2c`, 22 331 Bytes, geprüft). Freigabe des Betreibers 26.09.2026, ca. 16:30
(Auswahlkarte, wörtlich im Auftrag).
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Auftrag, Zeiger, Fable-Antwort committet (`79c2dfa`). ⚠️ Zwei weitere unversionierte Dateien lagen im Baum und sind **nicht** mitcommittet (Auftrag: „melden, nicht mitcommitten"): `docs/projektfuehrung/AF-F0_BESTANDSAUFNAHME_2026-09-26.md`, `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-26a_tagesanfrage_tb109_bis_113.md`. 0b: alle Ausgangswerte wie erwartet |
| ⭐⭐ **A** | Register **45** (45.0–45.10) und **11 Marken**. numstat **218/0**, R1–R8 je `diff` **rc 0** (8/8; Mutationsprobe rc 1), **38 Zitate** `diff` rc 0, Sonde gegen `e655c1c8…` vorher = nachher, `register()` `a0e477fd…` ⇒ **`03178075…`**, `test_vorregistrierung` **196/196** |
| ⭐⭐ **B** | B1: `register()` vor = nach B1 **bytegleich** (`03178075…`). B2 gemessen (Frage an Fable). B3: neun Listen, `register()` ⇒ **`5acb4c19…`**, 20 Teile, **`fehlend` leer**. B4: `datenstand()` ohne Pfad im Modus ⇒ **2**. `herkunft.py` `5bbfc9e0…` ⇒ **`ed521ac1…`**. `test_ersatzwerte` **70/70** (+9 Proben), `test_sperrlistensonde` **59/59**; **drei Testannahmen nachgezogen** |
| **C** | Abbild `sperrliste_abbild_2026-09-26_tb114.json` **`5e5ad109…`** (10 805 B, neu, nichts überschrieben). Sonde dagegen **34/0/0, (ii) 0**, eingefroren 19. ⚠️ Sonde gegen `e655c1c8…`: **Befund nur Punkte 11/12 (`herkunft.py`)**, Gruppe `eingefroren` 0 — **die neun neuen Einträge meldet sie nicht** ⇒ Abbruchkriterium. Nachmessung (nur lesend) trotzdem vollständig: Benchmark im Modus Repo **und** Klon **`64fb2912…`**, Trockenlauf **9 × rc 0**, ohne Modus **8/8 bytegleich** (= TB-113 A5), `faltenplan.json` `0e54ac5c…` unverändert, Laufbereich **81** (gleich TB-112, ohne `herkunft.py`), Tests 43 Dateien, **40 rc 0** (`test_vorregistrierung` 196/196, `test_ersatzwerte` 70/70, `test_sperrlistensonde` 59/59, `test_startpruefungen` 44/44, `test_arbeitsbaum_laufbereich` 26/26, `test_stille_ausfaelle` 27/27, `test_universum_trockenlauf` 163/163); nicht rc 0 und ohne Bezug zu dieser Sitzung: `test_drawdown_beide_masse` (terminiert bekanntlich nicht, nach 880 s beendet), `test_stabile_sortierung` 43/3 und `test_wellenauswahl` 322/1 (abgelegte Ergebniskurven, siehe `c_tests_anmerkung.txt`) |
| ⛔ **D** | **Entfällt.** 45.11 schreibt „Sonde gegen das alte Abbild mit genau dem erwarteten Befund" — das ist nicht eingetreten. Kein Registertext mit einem Befund, den der Auftrag nicht vorgesehen hat |
| **E** | Journal **DM**, dieses Dokument |

---

## 0. Schritt 0

| | |
|---|---|
| 0a | `git status`: die drei erwarteten Dateien, md5 der Fable-Antwort `e2a492165d44f6ee3d02eba99d2acf2c` ✔. Dazu **zwei weitere** unversionierte Dateien (oben) — gemeldet, liegen weiter unversioniert. Commit `79c2dfa`, gepusht |
| 0b | `0b_ausgang.txt`: `register()` **`a0e477fd…`** ✔; `herkunft.py` **`5bbfc9e0…`** ✔; Sonde gegen `e655c1c8…` **25/0/0, (ii) 0** ✔ (rc 2 nur für die Regel-Bestandteile, wie immer); die neun `research/tb24_haltedauern/daten/<bot>_alle_trades.csv` **alle versioniert**, unverändert, je sha256 im Beleg (die Zeilenzahlen stehen **nur** im Beleg — sie sind Trade-Zahlen nach 27.1 und gehen nicht an Fable) |

## 1. Block A — Register 45

Eingesetzt mit `eintrag_register_45.py` (Kopie der TB-113-Bauart: Zitate **eingesetzt**, nicht abgetippt; Quellen
`git:79c2dfa:…`), vorher Probelauf gegen eine Kopie (`probelauf.sh`), das Register danach `cmp`-gleich mit der Kopie.

| | |
|---|---|
| 45.0 | Anlass (erste gesammelte Tagesanfrage, neuer Fable-Takt — beides zeichengleich als Teilzitat), Quelle mit md5, Kette zu 43/44, Einordnung von R6 (Fables drittes „Unsicher", zeichengleich) |
| 45.1–45.8 | R1–R8 **zeichengleich** als Blockzitat, je mit „Quelle des Grundes" und einer Kettenzeile. `a2_r_diff.py` liest Fable-Datei und Register **unabhängig vom Einsetzskript**: **8/8 diff rc 0**; Mutationsprobe (ein Wort in R7 geändert) ⇒ rc 1 (`a2_r_diff_mutation.txt`) |
| 45.9 | Tatsachennotiz Pfadregel (Fables erstes „Unsicher" zeichengleich; die zwei Codezeilen als Teilzitate aus `herkunft.py` Z. 121/123 und `sperrlistensonde.py` Z. 160 am Stand `79c2dfa`) |
| 45.10 | Offen: TB-115 (drei Verfahrensmessungen), Erzeuger, Faltenplan-Abbild, Stufe IV, R8 (a)/(d); Liste der Marken |
| Marken | **7.1 · 19 · 27 · 30.2 · 33.3 · 41.1 A12 · 42.2 E1 · 42.2 E2 · 42.6 Zeile (5) · 43.3 · 44.3** — elf, wie der Auftrag sie aufzählt (7 Zeilen, 11 Orte). In 42.6 als Tabellenzeile `↳ (5)` direkt unter (5), sonst als Blockzitat unter dem Anker. **Keine in 10, keine in 9** |

**Nachweise:** numstat **218/0** (`a1_numstat.txt`); **38 Zitate** (31 Zeilen, 7 Teile) `diff` rc 0 (`a3_zitate.txt`);
Sonde gegen `e655c1c8…` vorher = nachher — der JSON-Bericht ohne das Feld `zeilen` hat vorher und nachher denselben
Hash `d612402a…`; ⚠️ **einzige Änderung: der Listentext von Abschnitt 10 steht jetzt in Z. 905–1018 statt 901–1014**,
weil die Marke unter 7.1 vor Abschnitt 10 liegt (4 Zeilen). Inhalt und Listentext-Hash unverändert
(„wie bei Erzeugung: ja"). `register()` `a0e477fd…` ⇒ **`03178075d24f1f41137c9f8f45604556e04cd513e12757b899eb47a0a5c1e91a`**.
`test_vorregistrierung` **196/196 rc 0** (895 s).

## 2. Block B — `herkunft.py`, dritte Öffnung

`git diff --stat 77147f7 0b7ab4b -- research shared`: `herkunft.py` +38/−4, `test_ersatzwerte.py` +137/−3,
`test_sperrlistensonde.py` (8a und H7f).

| | Änderung | Nachweis |
|---|---|---|
| **B1** | Neue Funktion `_eingefroren_pfad(rel)`: kein `/` oder Präfix `ergebnisse/` ⇒ relativ zu `_HIER`, sonst relativ zu `_WURZEL` (der Wurzel, in der das Modul liegt — wie `_HIER` unabhängig von `TB30A_BASE_DIR`). `register()` löst die Registerdatei wie bisher auf und jeden Eintrag von `EINGEFROREN` über `_eingefroren_pfad`; `rel` geht unverändert in den Hash. Die Sonde wird **nicht** importiert | `register()` als JSON (Hash, 11 Teile, `fehlend`) vor und nach B1 **`cmp` rc 0** — `03178075…` (`b1_nachweis.txt`). `herkunft.py` nach B1 allein `3c3fe17e…` (nicht einzeln committet) |
| **B2** | nur gemessen | Abschnitt 5 unten, `b2_fehlend.txt` |
| **B3** | Die neun Listen, repo-relativ, in der Reihenfolge von `ls strategies/` (elliott_wave, elliott_wave_stocks, rsi2_crypto, rsi2_mean_reversion, t3_supertrend, turtle_soup_crypto, turtle_soup_stocks, volatility_breakout, volatility_breakout_crypto) | `register()` **`5acb4c1924a4a009f82e5b4ffe353d70ba0a2452949be166afaa1af8e9fee6af`**, **20 Teile, `fehlend` []**, die neun sha256 gleich 0b (`b3_register.txt`) |
| **B4** | `datenstand()`: `if not daten_dir and _paths().selektionsmodus() is not None:` ⇒ `_abbruch_2("datenstand", …)`, **vor** `os.listdir`. Die Bedingung ist absichtlich nicht wortgleich mit der in `block()` (E1-Mutation verlangt genau eine Fundstelle). Ohne Modus: Rückgabe wie vorher (neu ist nur, dass `paths` dabei geladen wird — wie schon in `block()`) | H-c/H-cM/H-d unten |

**Neue Proben** (`test_ersatzwerte.py` Teil H, 61 ⇒ **70/70**, 74 s):

| Probe | prüft |
|---|---|
| H-a | im laufenden Prozess: je Eintrag von `EINGEFROREN` `herkunft._eingefroren_pfad(rel)` == `normpath(join(_WURZEL, sonde._aufloesen(rel)))`, 19 Einträge, 0 abweichend |
| H-a2 | dieselbe Gegenprobe in einem Wegwerfbaum `<t>/research/vorregistrierung/` (eigener Prozess) |
| H-aM / H-aM-G | Mutation „alte Regel: `_HIER`" ⇒ genau die neun TB-24-Einträge abweichend (Gegenprobe rot); ohne Mutation nicht |
| H-b | `register()` im Repo: `fehlend` leer, 20 Teile, die neun Listen am Ende in der Reihenfolge von `strategies/` |
| H-c | Modus, Wegwerfbaum aus Teil E: `datenstand()` ohne Pfad ⇒ rc 2, Meldung nennt `datenstand`, keine Ausgabe |
| H-cM / H-cM-G | Mutation „Wache ⇒ `if False:`" ⇒ rc 0 und hasht `BASE_DIR/data`; ohne Mutation nicht |
| H-d | ohne Modus: `datenstand()` ohne Pfad rc 0, Hash = `BASE_DIR/data` wie vorher |

**Nachgezogene Testannahmen (Grundsatz 40)** — die Fassungen am Stand `77147f7` gegen das neue `herkunft.py`
brechen **genau** an diesen drei Stellen und nirgends sonst (`b_testannahmen_alt.txt`: 60/61 bzw. 57/59):

| Datei, Probe | vorher | nachher | Grund |
|---|---|---|---|
| `test_ersatzwerte.py` **E-bM** | Mutation „Voreinstellung in `block()` zurück" ⇒ erwartet **rc 0** | erwartet: **nicht** rc 2 an `block`, **aber** rc 2 an `datenstand` | Seit B4 hält die zweite Wache den mutierten Lauf auf. Die Mutation beisst weiter, weil E-b rc 2 **an der Stelle `block`** verlangt |
| `test_sperrlistensonde.py` **8a** | Gruppe `eingefroren` hat **10** Einträge | **19** | R3/45.3 |
| `test_sperrlistensonde.py` **H7f** | „Pfad-Bestandteile: **25** geprueft" | **34** (15 + 19) | R3/45.3 |

## 3. Block C — Abbild und Nachmessung

| Messung | Soll | gemessen | Beleg |
|---|---|---|---|
| Abbild | neuer Name, nichts überschrieben | `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb114.json`, `test -f` vorher: fehlt; **`5e5ad1097909b3531e19b238153cabc46e7b551bb25e369ddc6735836e71cd06`**, 10 805 B, 14 Punkte (Z. 905–1018), bestimmt 0, **eingefroren 19**, HEAD `0b7ab4b` | `c1_abbild.txt` |
| Sonde gegen das neue Abbild | 0 Befunde, (ii) 0, eingefroren 19 | **34/0/0, (ii) 0**, beide Gruppen 0, rc 2 nur Regel-Bestandteile | `c2_sonde_neu.txt` |
| ⚠️ Sonde gegen `e655c1c8…` | **genau** Hash `herkunft.py` **und** die neun neuen Einträge | rc 1: Punkte **11 und 12** je `herkunft.py` ABWEICHUNG `ed521ac1…` (eine Datei, zwei Punkte ⇒ 23/2/0). Gruppe `eingefroren`: **0, 10 Dateien gleich** — **die neun neuen Einträge erscheinen nirgends im Bericht** (auch nicht im JSON: 0 Treffer `tb24`) | `c2_sonde_alt.txt` |
| Benchmark im Modus, Repo | `64fb2912…` | **`64fb2912…`**, rc 0, 59 s, Sauberkeit über alle 15 Pfade leer | `c_laeufe.txt` |
| Benchmark im Modus, frischer Klon | `64fb2912…` | **`64fb2912…`**, rc 0, 57 s, `status --ignored` vorher/nachher leer | `c_laeufe.txt` |
| Trockenlauf im Modus | 9 × rc 0 | **9 × rc 0**, `auswertung`-Import rc 0 | `c_laeufe.txt` |
| ohne Modus, 8 Ausgaben | bytegleich | **8/8 bytegleich** (= TB-113 A5) | `c_g2_ausgaben.txt` |
| `ergebnisse/faltenplan.json` | unverändert | `0e54ac5c…`, letzter Commit `a2fcf01` | — |
| Laufbereich | 81, ohne `herkunft.py` | **81, gemeinsam 81** mit TB-112, `herkunft.py` nicht darin | `c_laufbereich.txt` |
| Tests | rc 0 | 43 Dateien, **40 rc 0** (`test_vorregistrierung` 196/196, `test_ersatzwerte` 70/70, `test_sperrlistensonde` 59/59, `test_startpruefungen` 44/44, `test_arbeitsbaum_laufbereich` 26/26, `test_stille_ausfaelle` 27/27, `test_universum_trockenlauf` 163/163); nicht rc 0 und ohne Bezug zu dieser Sitzung: `test_drawdown_beide_masse` (terminiert bekanntlich nicht, nach 880 s beendet), `test_stabile_sortierung` 43/3 und `test_wellenauswahl` 322/1 (abgelegte Ergebniskurven, siehe `c_tests_anmerkung.txt`) | `c_tests.txt` |

### ⚠️ Der Abbruch — was die Sonde sieht und was nicht

Die Sonde prüft die Gruppe `eingefroren` **aus dem Abbild heraus** (`_pruefe_gruppe`, Register 40.8 (e): „die
Gruppen kommen aus dem Abbild"): je Eintrag **des Abbilds** den Hash der Datei. Ob `herkunft.py::EINGEFROREN`
heute **mehr** Einträge hat als das Abbild, vergleicht sie nicht — `lies_eingefroren` wird nur beim **Bilden** eines
Abbilds gerufen. Gegen das alte Abbild zeigt sich die Erweiterung deshalb **nur mittelbar**, über den Hash von
`herkunft.py` in den Punkten 11/12 (dort steht die Liste). Der Auftrag erwartete die neun Einträge als eigenen
Befund; das Abbruchkriterium „gegen das alte … anderes als erwartet" greift. **Nichts wurde repariert** (die Sonde
ist nicht freigegeben). Folge: **Block D (45.11) ist nicht geschrieben**; das neue Abbild ist erzeugt und
committet, aber **nicht als gültig registriert** — das wäre 45.11.

Nicht betroffen sind die übrigen Abbruchkriterien: kein unerwarteter Befund, kein anderer Hash, Benchmark, Ausgaben,
Trockenlauf und Tests wie oben.

## 4. B3 — der Pfad des künftigen Erzeugers (Tatsachennotiz)

Gelesen: Register **40.6** (Fable 24a) und **41.1 A12** (Fable 24b), dazu der heutige Erzeuger.

- **40.6:** Die Listen werden „vor dem Tag einmal auf dem registrierten Snapshot mit dem registrierten Code neu
  erzeugt … durch einen Erzeuger unter 36.1 (`--ziel`, Einmal-Schreibsperre)"; „`faltenplan.py` liest sie über einen
  registrierten Pfad (Konstante, kein Schalter). **Die alten Listen (`78e2bc6`) bleiben liegen als historischer
  Stand**".
- **41.1 A12:** Der registrierte Code ist der **Signalpfad**; die neuen Listen haben ein anderes Format (ohne
  `ausgefuehrt`, ohne Kennzeichnung im Symbolfeld, mit `exit_time`/`haltedauer_balken`). Stand: Erzeuger nicht gebaut.
- **Heute:** `research/tb24_haltedauern/positionen_holen.py` (TB-98) schreibt nur nach `--ziel` (Pflicht, keine
  Voreinstellung), mit `O_CREAT|O_EXCL`, und endet mit 1, wenn eine Zieldatei existiert — in den heutigen Ordner
  könnte es gar nicht schreiben. `faltenplan.py` Z. 144 liest `TB24_DATEN = BASE_DIR/research/tb24_haltedauern/daten`,
  also **genau die neun Dateien**, die jetzt in `EINGEFROREN` stehen.
- **Ergebnis:** Die neuen Listen kommen **nicht** an denselben Pfad; ihr Pfad ist noch **nicht registriert** (die
  Pfadkonstante in `faltenplan.py` ist TB-100-Rest). Nach R5 folgt `EINGEFROREN` dem Pfad des Erzeugers **bei dessen
  Einbau**; bis dahin bindet es die Dateien, die der Lauf heute liest. Der Kommentar in `EINGEFROREN` sagt das.

## 5. B2 — wer liest `register()["fehlend"]`?

`b2_fehlend.sh` / `.txt`:

- **Suchmuster** `\[.fehlend.\]|register_fehlend|\.get\(.fehlend` über alle versionierten `.py`: Leser sind nur
  `herkunft.block()` (kopiert es als `register_fehlend` in den Herkunftsblock) und die Prüfansicht `herkunft.main()`
  (druckt `! fehlend …`); dazu die Zwillingsdatei `research/turn_of_month/herkunft.py` und die Tests. Aufrufer von
  `register()/block()/anhaengen()` ausserhalb `docs/`: nur `test_ersatzwerte.py`. Laufbereich: `herkunft.py` 0 Zeilen.
- **Probe** in einem frischen Klon mit dem neuen `herkunft.py` (lokal committet), `rsi2_crypto_alle_trades.csv`
  weggelegt:

| | rc | sichtbar |
|---|---|---|
| ohne Modus, `register()` | 0 | `fehlend` [die Liste], 19 Teile, anderer Hash `ccacf260…` |
| ohne Modus, Prüfansicht | **0** | Zeile `! fehlend …` |
| **Modus**, Prüfansicht | **0** | dieselbe Zeile; die Startprüfung lässt die gelöschte Liste durch (nicht in `ARBEITSBAUM_PFADE`) |
| Modus, `--json` | 0 | `register_fehlend` im Block |
| Gegenprobe, Liste zurück | 0 | Hash wieder `5acb4c19…` |

⇒ **Eine fehlende eingefrorene Datei führt nirgends zu rc ≠ 0**, weder ohne noch im Modus. Sie ändert den
Register-Hash still und steht nur als Feld bzw. Druckzeile da. Keine Änderung (Frage unten).

## 6. Für Fable

1. **B2 — ein Hash, der eine fehlende Datei still auslässt (A5-Klasse?).** `register()` führt eine fehlende Datei
   von `EINGEFROREN` in `fehlend` und rechnet ohne sie; kein Aufrufer macht daraus einen Rückgabewert ≠ 0, auch
   nicht unter dem Modus (gemessen: gelöschte TB-24-Liste ⇒ Prüfansicht rc 0, Startprüfung rc 0, weil die Listen
   nicht in `ARBEITSBAUM_PFADE` stehen). Soll `register()` bzw. `block()` unter dem Modus bei nicht leerem `fehlend`
   mit 2 enden? Und gehören die neun Listen zusätzlich in die Sauberkeitsprüfung, oder genügt, dass der
   Faltenplan-Leser (`faltenplan.py`) an einer fehlenden Liste ohnehin abbricht?
2. **Die Sonde sieht Zuwachs in `EINGEFROREN` nicht (Abbruch dieser Sitzung).** Sie prüft `eingefroren` aus dem
   Abbild heraus (40.8 (e)); neue Einträge in `herkunft.py` erscheinen gegen ein altes Abbild nur als Hash-Abweichung
   von `herkunft.py` (Punkte 11/12). Genügt diese mittelbare Anzeige — `herkunft.py` steht auf der Sperrliste —,
   oder soll die Sonde `lies_eingefroren(wurzel)` mit der Gruppe des Abbilds vergleichen (fehlender/zusätzlicher
   Eintrag ⇒ 1)? Und darf das neue Abbild `5e5ad109…` danach in 45.11 als gültig eingetragen werden?
3. **Pfad des Erzeugers (B3, Abschnitt 4):** Die neuen Listen kommen nicht an denselben Pfad, und ihr Pfad ist nicht
   registriert. Bestätigst du: `EINGEFROREN` bindet bis zum Einbau des Erzeugers die neun heutigen Dateien und folgt
   dann dem Pfad des Erzeugers (R5)?
4. **Nachgezogene Testannahmen** (Abschnitt 2): E-bM (seit B4 zwei Wachen hintereinander — die Mutation der ersten
   endet jetzt an der zweiten mit 2 statt mit 0), 8a (10 ⇒ 19), H7f (25 ⇒ 34). Einwände?
5. **Randbefund:** Der Modulkopf von `herkunft.py` beschreibt `register` als Hash über „die Registerdatei, die Module
   dieses Ordners und die vorab berechneten Tabellen" — seit B3 gehören die neun Listen dazu. Nicht geändert (nur
   B1/B3/B4 freigegeben); Nachtrag mit der nächsten Öffnung?

## 7. In einfacher Sprache

Fables acht Textbausteine stehen jetzt wörtlich im Regelwerk, als Abschnitt 45, und an elf älteren Stellen steht
ein Hinweis darauf. Das Programm, das die „eingefrorenen" Dateien mit Prüfsumme festhält, sucht Pfade jetzt nach
derselben Regel wie das Prüfwerkzeug; damit konnten die neun Handelslisten aufgenommen werden, aus denen der
Faltenplan seine Längen ableitet. Ausserdem bricht es im Selektionsmodus ab, wenn ihm kein Datenordner genannt
wird. Am Ergebnis des Laufs hat sich nichts geändert: Benchmark, Ausgaben und Tests sind gleich geblieben.
Beim Nachmessen zeigte sich aber eine Lücke im Prüfwerkzeug: Gegen das alte Abbild meldet es nur, dass sich das
Programm geändert hat, nicht, dass neun Dateien dazugekommen sind. Das war eine Abbruchbedingung. Deshalb ist der
letzte Registereintrag (45.11) nicht geschrieben; Fable und der Betreiber entscheiden, wie es weitergeht.
