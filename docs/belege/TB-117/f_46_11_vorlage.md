### 46.11 Vollzug in TB-117 (Tatsachennotiz)

**Gemessen in TB-117, 26./27.09.2026** (Belege `docs/belege/TB-117/`, Ergebnis
`docs/ERGEBNIS_TB-117_wachen_vor_dem_tag.md`). Eingang `8b342ab`, Schritt 0
`753ec11`, Block A `4c5615d` (45.11 und 46.0–46.10). Freigabe des Betreibers
26.09.2026, ca. 22:20 (Auswahlkarte, wörtlich im Auftrag). Kein
Abbruchkriterium ausgelöst.

**Hash-Übergänge nach 37.3:**

| Block | Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|---|
| B | `shared/sperrlistensonde.py` | `f88e54ee…` | `98c02e0e…` | `42ef509` | R9 (46.1) |
| C | `research/vorregistrierung/herkunft.py` | `ed521ac1…` | `c6c13388…` | `ff2f254` | R10 (46.2), R15 (a) (46.6), R17 (a) (46.8) |
| D | `research/vorregistrierung/auswertung.py` | `a864b216…` | `8ec45123…` | `852f253` | R14 (46.5), Lesart 46.9, R8 (a) (45.8) |

**`herkunft.register()`:** `5acb4c19…` (Eingang) ⇒ `6bcb4f58…` (nach
Block A) ⇒ `b8f2cc33…` (nach Block C; 23 Teile, `fehlend` leer) ⇒
`e87a4d8e…` (nach Block D, gemessen vor diesem Eintrag). Der Wert nach
diesem Eintrag kann hier nicht stehen (er hasht diesen Text); er steht im
Ergebnis.

**B (R9):** Die Sonde vergleicht zusätzlich die heutige Liste
`herkunft.py::EINGEFROREN` mit der Gruppe `eingefroren` des Abbilds; ein
Eintrag nur auf einer Seite ist Befund 1 mit Eintrag und Seite
(„Liste → Abbild fehlt“ bzw. „Abbild → Liste fehlt“). Gegen das alte Abbild
`e655c1c8…` meldet sie die neun TB-24-Listen „nur in der Liste“ — die Zeile,
die R11 als fehlend beschreibt.

**C (R10, R15 (a), R17 (a)):** `register()` und `block()` enden unter dem
Modus mit 2, wenn `fehlend` nicht leer ist (je eigene Fundstelle, Meldung
nennt die Einträge); ohne Modus unverändert. `EINGEFROREN` führt zusätzlich
`snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json`
und die beiden Kopien `…/config/top25_symbols.txt` und
`…/config/sp500_top150.txt` des Snapshots aus Register 18 — versioniert,
repo-relativ, in `herkunft.py` und Sonde gleich aufgelöst; **keine dritte
Pfadauflösung**. Die `config/`-Kopien stecken im Snapshot-Hash (225 Dateien),
nicht im Datenstand (223). Die Tatsachennotiz an Punkt 8 steht in 46.6.

**D (R14, Lesart 46.9, R8 (a)):** `auswertung.py` liest `herkunft.json`
unter dem Modus für alle neun Bots und endet mit 2 bei jeder der fünf
Bedingungen; der registrierte Datenstand steht als Konstante
`REGISTRIERTER_DATENSTAND` mit Fundstelle Register 18. Ohne Modus: nur
Anzeige. Der Kopf des Berichts trägt Commit, Datenstand und Register-Hash.
Der Satz „`Abbruch` … endet mit 1“ ist berichtigt; damit ist Zeile (5) von
45.10 für R8 (a) erledigt.

**Gültiges Abbild ab jetzt** (nach R11 „nach dem Bündel ein neues Abbild“):
`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`,
sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f`
(11 432 B, 14 Punkte, `eingefroren` 22 = `EINGEFROREN`, HEAD `852f253`).
Sonde dagegen 37/0/0, (ii) 0, Mengenvergleich 22/22 ohne Befund. Es ersetzt
`5e5ad109…` (45.11); nichts ist überschrieben.

**Sonde gegen `5e5ad109…`, jeder Eintrag zugeordnet:** Punkte 3, 5, 14 und
Gruppe `eingefroren`: `auswertung.py` (Block D); Punkte 11, 12:
`herkunft.py` (Block C); Gruppe `eingefroren`, „Liste → Abbild fehlt“:
MANIFEST und die zwei Snapshot-`config/`-Kopien (Block C). Kein Eintrag ohne
Zuordnung.

**Probe R13 (a):** `shared/test_ausschlussmengen.py` liest die vier
Ausschlussmengen mit `ast` (keine importiert, keine geändert) und verlangt
Gleichheit samt `XAUTUSDT` — 9/9, drei Mutationen je mit Gegenprobe. Die
Zusammenlegung bleibt der jeweils nächsten planmässigen Öffnung.

**Unverändert gemessen:** Benchmark im Modus Repo und frischer Klon
`64fb2912…`; acht Ausgaben ohne Modus bytegleich mit TB-114; Trockenlauf
9 × rc 0; `faltenplan.json` `0e54ac5c…`; Laufbereich 81 Module (= TB-114).
Tests am Stand `54ce889`:
44 Dateien, 41 rc 0 (darunter `test_vorregistrierung` 196/196,
`test_ersatzwerte` 99/99, `test_sperrlistensonde` 65/65,
`test_ausschlussmengen` 9/9, `test_startpruefungen` 44/44,
`test_arbeitsbaum_laufbereich` 26/26); ohne rc 0 nur die drei bekannten
ohne Bezug zu diesem Auftrag (`test_drawdown_beide_masse` terminiert nicht,
`test_stabile_sortierung` 43/3, `test_wellenauswahl` 322/1 — dieselben
Stellen wie TB-114).

**Nicht vollzogen in TB-117:** R12 (Neuerzeugung der Listen), R15 (b) (am
Tag-Commit), R16 (a) (nach dem Tag) und (b) (mit dem Zellen-Erzeuger), die
Bestätigung von 46.9 durch Fable.
