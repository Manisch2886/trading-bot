# TB-98 — Ergebnis: Die neun Handelslisten auf dem Snapshot — der Erzeuger ist nach 36.1 umgebaut, aber die Listen lassen sich heute nicht erzeugen: zwei Befunde vor Block C

**Sitzungstitel:** `TB-98` · **Stand:** 24.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-98_neun_listen_auf_dem_snapshot.md` · **Belege:** `docs/belege/TB-98/`
**Eingang:** `e87b06f` (TB-97-Abgabe) · Commits: `a58ed1d` (Schritt 0), `46e3ed0` (Block B,
Erzeuger), `c25a91f` (Block A, Belege und Befund), Abgabe-Commit (dieses Dokument, Journalblock CZ).
**Grundlage:** Register 40.6 und 40.8 (f), Fable 24a Abschnitt 3.
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:** Block A hat die Frage beantwortet, „an der alles hängt" — und die Antwort ist
**zweimal nein**, aus zwei Gründen, die mit dem Erzeuger selbst wenig zu tun haben:

- ⚠️⚠️ **Befund 1 — Unter dem Selektionsmodus fehlen die Symbollisten.** Die Kursdaten
  kommen richtig aus dem Snapshot (0 Zugriffe auf `data/`, 9/9 Bots). Die zwei
  Universumsdateien liegen im Snapshot aber unter `config/`, und `shared/paths.py` sucht sie
  in der flachen Snapshot-Wurzel. Alle neun Bots fallen **still** auf eine Standardliste von
  **5 Symbolen** zurück, und das Ladeprotokoll meldet „Geladen: 5 von 5 Symbolen. Keines
  ausgelassen." Das betrifft nicht nur diesen Erzeuger, sondern **jeden Lauf unter dem Modus**,
  der die Symbollisten über `symbols_config.py` oder `stocks_symbols_config.py` liest.
- ⚠️⚠️ **Befund 2 — Der Erzeuger läuft mit dem heutigen Code nicht, mit und ohne Modus.**
  9/9 Bots brechen vor dem Schreiben ab: „Kennzeichnung hat die Simulation verändert". Die
  Zuteilungskaskade aus TB-26 (`shared/zuteilung.py`, **Sperrlistenpunkt 10**) nimmt das
  Symbol in ihren Zufallsschlüssel auf. Die Zeilenkennung `AAPL#417`, mit der der Erzeuger
  die ausgeführten Trades zuordnet, verschiebt dadurch die Zuteilung. Die alten Listen
  (`78e2bc6`) sind **vor** TB-26 (`f6d9a28`) entstanden. Gegenprobe: ohne Kennung im
  Schlüssel 9/9 gleich.

⇒ **Block C und D sind nicht ausgeführt.** Keine Liste ist erzeugt, keine Faltenlänge
abgeleitet, kein Vergleich gegen 33.2 gerechnet, auch nicht „zur Orientierung" auf einem
Ersatzweg (Abschnitt 4). **Block B ist fertig**: Der Erzeuger schreibt nur noch in einen
ausdrücklich genannten Ordner und überschreibt nie. Nachgewiesen ist das auch gegen den
historischen Ordner `daten/` selbst: Aufruf dort ergibt rc 1, 27 Dateien mit gleichem Hash
und gleicher mtime.

Nichts Gesperrtes hat sich bewegt: 54 von 56 gemessenen Hashes sind gleich, bewegt haben
sich genau `positionen_holen.py` und `alle_bots.py`. Die Sonde zeigt vorher und nachher
dasselbe (0 Befunde). Der Snapshot ist nach `--pruefen` UNVERÄNDERT, `faltenplan.py`
bleibt `7aa0b8cc…`.

---

## 0. Schritt 0

| | |
|---|---|
| Lock-Dateien | `find .git -name '*.lock'` → keine |
| HEAD am Eingang | `e87b06f` ✔ |
| Register Abschnitt 40 | vorhanden (Z. 7632) ✔ — Abbruchkriterium 1 greift nicht |
| Commit | `a58ed1d`: Zeiger, Auftrag TB-98, Fable-Anfrage 24c |

---

## 1. Block A — Messen, bevor gebaut wird

### A1 — Liest der Erzeuger über den Selektionsmodus? (`a1_lesequellen.txt`)

**Statisch.** Die Kursdaten laufen `positionen_holen.py:73-74` → `bot_lauf.py:59-60` →
`equity_simulation` → `multi_symbol_optimise.load_all_symbol_data()` →
`get_strategy_paths()` (`shared/strategy_paths.py:136`) → `shared/paths.DATA_DIR`. Dieser
Weg führt durch den Resolver, **anders als bei `benchmark.py` und `messgroessen.py`**. Die
Symbolliste läuft `symbols_config.py:16-18` bzw. `stocks_symbols_config.py:19-21` →
`CONFIG_DIR`. Unter dem Modus zeigt `CONFIG_DIR` auf die Snapshot-Wurzel
(`paths.py:570`; Kopf Z. 91-93: „Die Snapshot-Wurzel ist flach").

**Dynamisch.** Der Erzeuger lief **unverändert** über den Umschlag `a1_probe.py`: Er setzt
nur `DATEN_DIR` auf einen leeren Scratchpad-Ordner. Mitgeschrieben hat ein Lesehaken
(`haken/sitecustomize.py`, jede geöffnete Datei mit Aufrufstapel). Gelaufen sind 9 Bots,
je mit und ohne Modus (`a1_neun.sh`). Die Startprüfung war 9/9 bestanden
(Commit `a58ed1d`, Arbeitsbaum sauber, Lock `96a5c572…`).

| | mit Modus | ohne Modus | mit Modus, Listen zusätzlich flach (`a1_flach.sh`) |
|---|---|---|---|
| rc / geschrieben | 9× rc 1 / 0 Dateien | 9× rc 1 / 0 Dateien | 9× rc 1 / 0 Dateien |
| Abbruch | Kennzeichnung | Kennzeichnung | Kennzeichnung |
| Symbolliste | **9× „nicht gefunden. Nutze Standardliste (5 …)"** | gefunden | gefunden (über die Verknüpfung auf `<snapshot>/config/`) |
| „Geladen" | **9× 5 von 5, „Keines ausgelassen"** | Krypto 18/24 bzw. 20/24, Aktien 147/150 | wie ohne Modus |
| Kursdateien aus | Snapshot (je 5) | `data/` | Snapshot (24 bzw. 150) |
| Zugriffe auf `data/` oder `config/` im Repo | **0** | – | **0** |

Die dritte Spalte hat einen Hilfsordner im Scratchpad benutzt, der nur aus Verknüpfungen
auf den echten Snapshot besteht. Dazu kommen die zwei Listen zusätzlich flach in der Wurzel.
Das zeigt: **Wird die Liste gefunden, liest der Erzeuger ausschliesslich aus dem Snapshot.**
Befund 1 liegt im Zusammenspiel von Resolver und Snapshot-Aufbau, nicht im Erzeuger. *(Der
Modus hat den Hilfsordner zugelassen, weil `paths.py` nur das Feld `snapshot_hash` im
Manifest prüft, nicht die Dateien. Das ist so gebaut. Die Inhaltsprüfung macht
`snapshot.py --pruefen`.)*

**Ursache von Befund 2** (`a1_kennzeichnung.py/.txt`, ohne Modus, nur im Speicher): Je Bot
wurde der Lauf ohne Kennung gegen den Lauf mit Kennung verglichen, über die fünf
Teilbedingungen aus `positionen_holen.py` (main, Kennzeichnungsprobe).

| | Erzeuger (heutiger Code) | Gegenprobe: Stufe-4-Schlüssel ohne Kennung |
|---|---|---|
| Bots mit ≥ 1 verschiedener Teilbedingung | **9 von 9** | **0 von 9** |

⇒ Die Kennung wirkt ausschliesslich über `zuteilung.zufallsschluessel` (Z. 492-497:
`symbol` ist eines der Felder). Der Satz in `bot_lauf.py` (Kopf Z. 32-37), `symbol` sei
„ausschliesslich Beschriftung", gilt seit TB-26 nicht mehr.

### A2 — Was genau die Liste trägt (`a2_spalten.txt`)

Die Liste hat 10 Spalten. Der Faltenplan liest davon **nur `entry_time`**
(`faltenplan.py:133-134`). `entry_time` hängt an den **gefundenen** Trades
(`hole_trades` → `collect_all_trades`), nicht an der Simulation. Die Simulation bestimmt nur
die Spalte `ausgefuehrt`. Der Erzeuger schreibt die Liste aber erst **nach** der
Kennzeichnungsprobe.
⚠️ **Nebenbefund:** Es gibt einen **zweiten Leser mit eigener Pfadangabe**,
`research/faltenplan_neun/faltenplan_neun.py:207/302-310`. Er hat eine eigene Funktion
`gefundene_trades_je_jahr` und eine eigene Konstante `TB24_DATEN`. Eine registrierte
Pfadkonstante in `faltenplan.py` allein lenkt ihn nicht um (TB-100).

### A3 — Parameterstand (`a3_parameterstand.py/.txt`)

Aus dem Lesehaken sind je Bot die geladenen Repo-Module ermittelt: 16–21 je Bot, in der
Vereinigung 70 Dateien, alle mit SHA-256. `live_params.py` ist bei jedem Bot dabei. Gegen
HEAD sind sie sauber (einzige Zeile im `git status`: der Umschlag selbst). ⚠️ Das ist der
Stand **dieses Versuchs**. Ein Parameterstand gehört aber zu einer erzeugten Liste, und
erzeugt ist keine (E5).

### A4 — Hashes und Sonde am Eingang

`a4_hashes_vorher.txt` enthält 56 Pfade: die 28 aus TB-96/97, die übrigen 18 Dateien unter
`tb24_haltedauern/daten/`, Erzeuger und `alle_bots.py` sowie alles unter
`vorregistrierung/ergebnisse/` (`pfade.txt`, `hashes.sh`). Die neun Listen sind gleich wie in
TB-97. Die Sonde gegen `sperrliste_abbild_2026-09-23.json` ergibt 15/0/0
Pfad-Bestandteile, 12 Regel-Bestandteile mit 2, rc 2 wie in TB-97 (`a4_sonde_vorher.txt`).

---

## 2. Block B — der Erzeuger nach 36.1 (`46e3ed0`)

| | umgesetzt | Beleg |
|---|---|---|
| **B0** | Nicht auf der Sperrliste, nicht in `EINGEFROREN` (Abschnitt 10, Abbild, `herkunft.py`, Sonde, Abbild-Erzeuger: je 0 Treffer). Abbruchkriterium 3 greift nicht | `b0_sperrlistenpruefung.txt` |
| **B1** | `--ziel ORDNER` ist Pflicht, ohne Voreinstellung. Geprüft wird **vor** dem Import von `bot_lauf.py`. Ohne Ziel: rc 2. Fehlender Ordner: rc 2, er wird **nicht** angelegt. Bot-Name nicht an erster Stelle: rc 2 (`bot_lauf.py` liest `sys.argv[1]`). Ganz ohne Argument: rc 1 (wie vorher) | `b_proben.txt` B1a–d |
| **B2** | Sperre **vor der Rechnung** (`sperre_vor_der_rechnung`, im `__main__`-Block vor `main()`). Existiert eine der vier Zieldateien, gibt es rc 1 mit Pfad und SHA-256. Der Lesehaken zählt dabei **0 Kursdateien, 0× `equity_simulation`**. Beim Schreiben wird `O_CREAT\|O_EXCL` verwendet. Entsteht die Datei während des Laufs, rc 1, der Inhalt bleibt. **`--ziel research/tb24_haltedauern/daten` ergibt rc 1, 27 Dateien mit gleichem Hash und gleicher mtime** | B2a–c |
| **B3** | AST gegen `e87b06f`: 4 von 5 Funktionen sind gleich. In `main` sind **nur** die drei Schreibaufrufe anders, dazu ein Aufruf der Herkunftsnotiz. Auf Modulebene ist nur die Zielbestimmung anders (argparse, `ZIEL_DIR`, `DATEN_DIR`/`makedirs` entfernt). Die Schreibstelle ist **alt gegen neu 27/27 bytegleich** | `b3_ast_vergleich.txt`, `b3_format.txt` |
| **B4** | `alle_bots.py --ziel ORDNER [bot …]` ist Pflicht und reicht den Pfad **absolut** durch (die Kindprozesse laufen mit `cwd=_DIR`). Die Durchreichung ist mit relativem Pfad und vorhandener Zieldatei nachgewiesen (rc 1 im Kind) | B4a–c |
| **B5** | `<bot>_herkunft.json` mit Erzeuger, UTC-Zeit, `code_commit`, `selektionsmodus` (das Audit-Dict aus `paths.startpruefung()`, ohne Modus `null`) und je Datei SHA-256. **Keine Trade-Zahlen.** ⚠️ Nicht end-to-end gezeigt, weil kein Lauf bis zum Schreiben kommt (Befund 2) | — |

⚠️ **Was B nicht zeigen kann:** Einen vollständigen Lauf mit geschriebenen Listen gibt es
nicht. Nachgewiesen sind die Schreibstelle für sich (Format 27/27, `O_EXCL`-Probe) und
alle Abbruchwege.

---

## 3. Block C und D — nicht ausgeführt (`c_d_nicht_ausgefuehrt.txt`)

Beide Befunde reichen **jeder für sich**:

- **Befund 2** lässt sich nur mit einem geänderten Rechenweg beheben. Im Erzeuger verbietet
  das B3. In `shared/zuteilung.py` ist es **Sperrlistenpunkt 10**.
- **Befund 1** lässt sich nur in `shared/paths.py`, in den fünf Symbol-Modulen oder am
  Snapshot-Aufbau beheben. E1 erlaubt Bewegung aber nur an den zwei Erzeuger-Dateien. Den
  Pfad im Erzeuger zu setzen, wäre ein zweiter Resolver (`strategy_paths.py`: „Hier steht
  KEIN zweiter Resolver").
- Ein Lauf trotz Befund 1 läse 5 statt 24 bzw. 150 Symbole, still und mit „Keines
  ausgelassen". **Das ist kein Lauf auf dem registrierten Snapshot.**

---

## 4. Warum die Faltenlänge nicht „zur Orientierung" gerechnet ist

Technisch wäre sie zu haben, weil `entry_time` nicht an der Simulation hängt (A2). Sie wurde
trotzdem **nicht** gerechnet. Wie die zwei Befunde behoben werden, ist nicht entschieden.
Ein Ergebnis, das vorher bekannt ist, färbt diese Entscheidung nach Wirkung. Das ist genau
der Fall, den Fable in 40.6 benennt, und die Bauart 24.3 („die Regel steht, bevor gerechnet
ist").

---

## 5. Abgabe — E1 und E2

| | Ergebnis | Beleg |
|---|---|---|
| **E1** | 56 Pfade: **54 gleich**, bewegt sind nur `positionen_holen.py` (`dfaae546…` → `a9e81f02…`) und `alle_bots.py` (`b7841184…` → `6e9ddce9…`). Gleich geblieben sind alle 27 Dateien unter `tb24_haltedauern/daten/` (die neun alten Listen eingeschlossen), beide Abbilder, `faltenplan.py` (`7aa0b8cc…`), `faltenplan.json` (`0e54ac5c…`), alle Tabellen unter `ergebnisse/`. Abbruchkriterien 2, 6 und 7 sind nicht eingetreten | `e1_hashes_nachher.txt` |
| **E1b** | `snapshot.py --pruefen` ergibt **UNVERÄNDERT**, rc 0. Der `git status` ist ausserhalb `docs/belege/TB-98/` leer | `e1b_snapshot_und_status.txt` |
| **E2** | Die Sonde zeigt vorher = nachher (ohne Kopfzeile, zeichengleich): 15 Pfad-Bestandteile mit 0, 0 mit 1, 0 mit 2, rc 2 aus den Regel-Bestandteilen und den im Abbild fehlenden Gruppen, wie am Eingang | `e2_sonde_nachher.txt` |

---

## 6. Für Fable — ohne Kontext lesbar ⭐⭐

> **Anlass.** Register 40.6 verlangt, die neun TB-24-Handelslisten einmal auf dem
> registrierten Snapshot (`63e4b6c8…`) mit dem registrierten Code neu zu erzeugen, zweimal
> bytegleich, und die Faltenlänge nach 5.4 gegen 33.2 zu vergleichen. TB-98 hat den Erzeuger
> nach 36.1 umgebaut (`--ziel` Pflicht, Einmal-Schreibsperre) und vorher gemessen, ob er
> über den Selektionsmodus liest.
>
> **A1 — liest der Erzeuger über den Modus?** Für die **Kursdaten ja**: 0 Zugriffe auf
> `data/`, 9/9 Bots. Für die **Symbollisten nein**: Der Snapshot legt sie unter `config/`
> ab, der Resolver (`shared/paths.py`) sucht sie unter dem Modus in der Snapshot-Wurzel.
> Alle neun Bots nehmen still eine Standardliste von 5 Symbolen, und das Ladeprotokoll
> meldet „Keines ausgelassen". Das gilt für **jeden** Lauf unter dem Modus, nicht nur für
> diesen Erzeuger. Nach bisherigem Stand hat vor TB-98 kein Bot-Lauf unter dem Modus mit dem
> echten Snapshot stattgefunden (in den Belegen 0 Treffer für die Warnzeile). Mit den Listen
> an der erwarteten Stelle (Messung über Verknüpfungen) liest der Erzeuger ausschliesslich
> aus dem Snapshot.
>
> **Zweiter Befund:** Der Erzeuger läuft mit dem heutigen Code überhaupt nicht, mit und
> ohne Modus, 9/9 Bots. Er ordnet ausgeführte Trades zu, indem er eine Zeilenkennung ins
> Symbol schreibt. Seit der Zuteilungskaskade (TB-26, `shared/zuteilung.py`,
> Sperrlistenpunkt 10) fliesst das Symbol in den Zufallsschlüssel der letzten Stufe, und die
> Kennung verschiebt die Zuteilung. Die Selbstprüfung des Erzeugers erkennt das und bricht
> vor dem Schreiben ab. Gegenprobe (Schlüssel ohne Kennung): 9/9 gleich. Die alten Listen
> sind vor TB-26 entstanden. Für die Faltenlänge zählt nur `entry_time` der **gefundenen**
> Trades, und die hängt nicht an der Zuteilung.
>
> **C2 (zweimal bytegleich):** nicht erreicht. **D2 (9/9 gleich, je Bot 1 oder 2):** nicht
> erreicht. Es wurde keine Faltenlänge gerechnet, auch nicht vorläufig, damit das Ergebnis
> die Entscheidung unten nicht färbt.
>
> **Was zu entscheiden ist, zwei Fragen:**
>
> **(1) Die Symbollisten unter dem Modus.** Wo wird es behoben? Möglich wären der Resolver
> (unter dem Modus `CONFIG_DIR` = `<snapshot>/config`: eine Stelle, Snapshot und Hash bleiben
> unberührt), die fünf Symbol-Module oder der Snapshot-Aufbau (flach). Der Snapshot-Aufbau
> hiesse neuer Snapshot, neuer Hash, und Register 18 wäre betroffen. Offen ist auch, ob ein
> Rückfall auf die Standardliste unter dem Modus nicht ein **Abbruch** sein muss statt
> einer Warnung. Er ist derselbe stille Ausfall, gegen den der Modus gebaut ist (Prüffrage D1).
>
> **(2) Die Neu-Erzeugung ohne bestandene Kennzeichnungsprobe.** Die Zuteilung ist gesperrt.
> Also muss sich der Erzeuger ändern, und das ist eine Änderung seines Rechenwegs. Das
> verbietet der Auftrag TB-98 (B3) ausdrücklich, deshalb liegt die Frage hier. Zum Beispiel:
> die Zuordnung über eine Spalte, die der Zufallsschlüssel nicht liest; *ob
> `simulate_portfolio` eine solche Spalte durchreicht, ist nicht gemessen*. Oder
> `_alle_trades.csv` ohne die Simulationsspalte `ausgefuehrt`, was ein anderes Dateiformat
> als die historischen Listen ergibt. Welche Form ist „der registrierte Code" im Sinn von
> 40.6?
>
> **Sichtschutz 27.1:** Dieser Abschnitt nennt keine Trade-Zahlen und keine Faltenlänge. Die
> Zahlen in den Belegen sind Symbolzahlen („Geladen: x von y"), Hashes und Rückgabewerte.

---

## 7. E5 — Wortlaut für die Tatsachennotiz zu 5.4 (Entwurf, **nicht eintragbar**)

⚠️ Eintragbar wird die Notiz erst, wenn Listen erzeugt sind. Was heute gemessen ist, steht
unten; `⟨…⟩` markiert, was fehlt.

> **Tatsachennotiz zu 5.4 — die neun Listen auf dem registrierten Snapshot (TB-⟨…⟩,
> ⟨Datum⟩).** Erzeugt mit `research/tb24_haltedauern/alle_bots.py --ziel ⟨Ordner⟩`
> (Erzeuger `positionen_holen.py` nach 36.1, SHA-256 ⟨…⟩, Stand `46e3ed0`: `a9e81f02…`) im
> Selektionsmodus gegen `snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`
> (`--pruefen` UNVERÄNDERT), Code-Commit ⟨…⟩, Lock `96a5c572…`, Interpreter 3.9.6. Parameterstand:
> die neun `live_params.py` mit SHA-256 (Stand `a58ed1d`, TB-98 A3)
> `elliott_wave a4afe7c1…`, `t3_supertrend 1425af67…`, `rsi2_crypto 37546218…`,
> `turtle_soup_crypto 28e91572…`, `volatility_breakout_crypto 0cae328c…`,
> `elliott_wave_stocks dd2b6afd…`, `rsi2_mean_reversion 6a23bbf6…`,
> `turtle_soup_stocks a556ffbf…`, `volatility_breakout c1bc00d8…`; die übrigen geladenen
> Module je Bot in ⟨Beleg⟩. Hash je `<bot>_alle_trades.csv`: ⟨neun Hashes, aus
> `<bot>_herkunft.json`⟩. Reproduzierbarkeit (23e): zweiter Lauf ⟨bytegleich ja/nein⟩.
> Die alten Listen (`78e2bc6`) bleiben als historischer Stand liegen. Der Regeltext von 5.4
> bleibt unverändert.

---

## 8. Abweichungen vom Auftrag

| | |
|---|---|
| Block C/D | Nicht ausgeführt, Grund in Abschnitt 3. Statt der sechs Belege `c1`…`d3` gibt es **einen**: `c_d_nicht_ausgefuehrt.txt` |
| Commits | (3) heisst „Block A (Belege) und Befund" statt „Block C+D". Block A ist erst dort committet, weil seine Belege nach Block B vollständig waren. Block B ist separat committet (`46e3ed0`) |
| A1 Probelauf | Der Auftrag verlangte **einen** Probelauf für **einen** Bot. Gelaufen sind 1 + 18 + 9 Probeläufe (Scratchpad, nichts geschrieben), weil der erste Lauf beide Befunde zeigte und ihre Reichweite (9/9, mit/ohne Modus) gemessen werden musste |
| Lesehaken | Die erste Fassung scheiterte bei flachem Aufrufstapel (`ValueError`). Sie ist berichtigt, der Lauf wiederholt, das erste Protokoll verworfen (Scratchpad) |

---

## 9. Was NICHT geschah

- ⛔ `faltenplan.py` nicht geändert und nicht ausgeführt, nur gehasht (`7aa0b8cc…` vorher = nachher).
- ⛔ Kein Sperrlistenpunkt, kein Registerabschnitt, kein Abbild. Die Freigabe vom 24.09. 11:25
  ist **nicht verbraucht**.
- ⛔ `shared/paths.py`, die Symbol-Module und `shared/zuteilung.py` sind nicht angefasst.
- ⛔ Keine Liste erzeugt, keine Faltenlänge gerechnet, keine Trade-Zahl gemeldet.
- Die alten Listen und alle übrigen Dateien unter `daten/` sind unverändert (Hash und mtime).

---

## 10. Für die Folgesitzung vorbereitet

- ⚠️⚠️ **Die Reihenfolge aus dem Zeiger (TB-100 nach TB-98) trägt nicht mehr.** TB-100
  (Registerabschnitt 41, Pfadkonstante, Abbild) setzt erzeugte Listen voraus. Vorher müssen
  die zwei Fragen aus Abschnitt 6 entschieden **und umgesetzt** sein. Danach läuft TB-98
  Block C/D erneut; der Erzeuger aus Block B steht dafür bereit.
- Aufruf, sobald die Befunde behoben sind (Ordner vorher anlegen, er wird nicht angelegt):
  `mkdir research/tb24_haltedauern/daten_2026-09-24_snapshot` und dann
  `TB_SELEKTIONSWURZEL=… TB_SELEKTIONSHASH=… TB_SELEKTIONSCOMMIT=<HEAD> trading-env/bin/python3
  research/tb24_haltedauern/alle_bots.py --ziel research/tb24_haltedauern/daten_2026-09-24_snapshot`.
  Die Startprüfung verlangt einen sauberen Arbeitsbaum über `shared/`, `strategies/` und
  die Lock-Datei, und HEAD muss der genannte Commit sein.
- Für die Pfadkonstante (TB-100): Es gibt **zwei** Leser (`faltenplan.py:121`,
  `faltenplan_neun.py:207`), Abschnitt 1 A2.
- Wiederverwendbar: `haken/sitecustomize.py` (Lesehaken mit Aufrufstapel), `a1_lesequellen.py`,
  `a1_flach.sh` (Hilfsordner aus Verknüpfungen), `hashes.sh`/`pfade.txt` (56 Pfade),
  `b_proben.sh`.
- Nicht gemessen: ob `research/exposure_messung/bot_lauf.py main()` mit derselben
  Kennzeichnungsprobe ebenso scheitert. Der Code ist gleich gebaut, aber nicht aufgerufen.

---

## In einfacher Sprache

Neun Handelslisten entscheiden, ob ein Bot ein- oder zweijährige Zeitabschnitte bekommt.
Sie sollten aus dem eingefrorenen Datenbestand neu erzeugt werden.

**Geschafft** ist der Umbau des Erzeugerprogramms. Es schreibt nur noch in einen Ordner, den
man ausdrücklich nennt, und es überschreibt nie etwas. Richtet man es auf den Ordner mit den
alten Listen, bricht es ab, bevor es irgendetwas rechnet. Das ist geprüft, und die alten
Listen sind unberührt.

**Nicht geschafft** ist die Erzeugung selbst, aus zwei Gründen. **Erstens:** Im
eingefrorenen Bestand liegen die Listen der zu handelnden Werte in einem Unterordner. Der
Programmteil, der den Bestand anschliesst, sucht sie aber eine Ebene höher. Er findet sie
nicht und nimmt ohne Fehlermeldung eine Notliste mit fünf Werten statt 24 bzw. 150. Das
hätte jeden späteren Lauf auf dem eingefrorenen Bestand getroffen, nicht nur diesen.
**Zweitens:** Das Erzeugerprogramm stammt aus der Zeit, bevor die Regel eingeführt wurde, wer
bei knappem Platz zum Zug kommt. Seither funktioniert sein Trick nicht mehr, mit dem es
erkennt, welche Trades ausgeführt wurden. Es merkt das selbst und hört auf, bevor es
schreibt.

Beides lässt sich nur an Stellen beheben, die dieser Auftrag nicht anfassen durfte. Zum Teil
stehen sie auf der Sperrliste. Deshalb wird nichts umgangen oder geschätzt. Die Frage geht an
den Verfahrensprüfer.
