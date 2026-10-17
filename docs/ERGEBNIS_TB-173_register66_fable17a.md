# ERGEBNIS TB-173 — Register 66: Fable 17a, Registerblock R106 mit vier Marken, 66.2 Voraussetzung R106 (c) und Tatsachennotiz TB-172; BACKLOG

**Sitzung:** TB-173, Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-173_register66_fable17a.md` · **Zweig:** `main`
**Commits:** `f79f239` (S0, Fable 17.10.a und Auftrag) · `7fe6342` (R, Register 66 und vier Marken) · `ae5c151` (K, Registerkopie, Index, Dialog-Index) · der Abgabe-Commit „TB-173 Abgabe: Ergebnis, BACKLOG, Journal FJ“, der dieses Ergebnis enthält · danach „TB-173 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-173/` · **Journal:** FJ · **Kein Abbruch.**

## Kurz

Die drei Fable-Dateien vom 17.10.a (Übergabe, Anfrage, Antwort) liegen unverändert seit `f79f239` im Repo (R56 (b)). Register 66 trägt R106 mit Quellenzeile zeichengleich aus dem Registerblock der Antwort (Z. 28–31), dazu eine Kettenzeile und 66.2 mit dem Voraussetzungsbeleg und drei Tatsachennotizen. **(a)** Die Voraussetzung aus R106 (c) ist gemessen, nur das Ob und nur am Code: In der Prüfung mit Schranke waren die Wachen nach R86 (d) und R87 (c) eingeschaltet. Die Probe bildet ihren Kursabschnitt selbst und liest keine Datei ausserhalb des Repos. Das ist eine Teilmessung. **(b)** TB-172: R102 (d) „ja“ bei drei Aktien-Bots, R92 (c) erfüllt. **(c)** R56 (b). Vier Marken nach R106 (e) stehen an 57.1, 61.1, 64.1 und 65.2; sonst ist das Register nur angehängt (numstat 78/0). Kein Handelscode, kein Lauf auf Kursen, kein Test, keine Probe, kein Live, kein Broker.

## Schritt 0

0a: Zweig `main`, HEAD = origin/main = `d81ef20e2707350ec77418dda0ae03a2fff1ccdf`, genau die fünf Soll-Einträge (`0a_status.txt`), Karte gefüllt; letzte Zeile `0a gut (5 Eintraege)`. Holbefehl: `tb173_werkzeug.py 2a0fc39171cacda95d6ec1e93fcebf47944fb23776b0e5cf7f49f5fbb82c6cc9`, `Dateien 1`. S0 = `f79f239`, gepusht, porcelain danach leer.

`0a_md5.txt`, wörtlich:

```
ja    md5 docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md = e222920fc17f72fb7f516d41a6203457
ja    md5 docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17a_r105c_weg1_elliott_t3.md = fae73317801514cd86be1f9101a1c401
ja    md5 docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17a_eroeffnung.md = 2d1b9293fc22e8c79a0111655302ad5c
Pruefungen: 3, NEIN: 0
rc 0
```

## Schritt V — Voraussetzungen

`v_voraussetzung.txt`, wörtlich:

```
ja    R56 (b)/0a-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md verfolgt, gleich HEAD, md5 e222920fc17f72fb7f516d41a6203457
ja    R56 (b)/0a-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17a_r105c_weg1_elliott_t3.md verfolgt, gleich HEAD, md5 fae73317801514cd86be1f9101a1c401
ja    R56 (b)/0a-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17a_eroeffnung.md verfolgt, gleich HEAD, md5 2d1b9293fc22e8c79a0111655302ad5c
ja    Registerblock 17a: genau R106 und Quelle im Codeblock (Z. 28–31)
ja    Register: 65 da, 66 nicht; R106 0 Treffer
ja    Register endet mit genau einer Leerzeile
ja    Ort 65.2: Einfuegestelle nach Z. 12465 eindeutig, R106 dort noch nicht genannt
ja    Ort 57.1: Einfuegestelle nach Z. 12004 eindeutig, R106 dort noch nicht genannt
ja    Ort 61.1: Einfuegestelle nach Z. 12235 eindeutig, R106 dort noch nicht genannt
ja    Ort 64.1: Einfuegestelle nach Z. 12447 eindeutig, R106 dort noch nicht genannt
ja    R106 (c) Stand: research/tb24_haltedauern/test_elliott_verdraengung.py sha256 59f6c90b… (Stand der Probe TB-171)
ja    R106 (c) Stand: research/tb24_haltedauern/test_listen_erzeuger.py sha256 e196884a… (Stand der Probe TB-171)
ja    R106 (c) Stand: research/tb24_haltedauern/positionen_holen.py sha256 b6d1e2d6… (Stand der Probe TB-171)
ja    R106 (c) Voraussetzung, Wachen: Pruefung 1 (mit Schranke) ruft den Erzeuger mit leerem Modus (research/tb24_haltedauern/test_elliott_verdraengung.py Z. [102])
ja    R106 (c) Voraussetzung, Wachen: research/tb24_haltedauern/test_listen_erzeuger.py ersetzt die Wachen nur in den Modi wache1_aus/wachen_aus (Z. [85, 86])
ja    R106 (c) Voraussetzung, Wachen: research/tb24_haltedauern/positionen_holen.py main ruft wache_zeilen Z. [327] und wache_trades Z. [337] ohne Bedingung (Einrueckung 4)
ja    R106 (c) Voraussetzung, Wachen: wache_zeilen (Z. [295]) nach R86 (d), wache_trades (Z. [303]) nach R86 (d) und R87 (c)
ja    R106 (c) Voraussetzung, Beleg docs/belege/TB-171/e_probe.txt, elliott_wave: Pruefung 1 ja (rc 0); Pruefung 2 ja, Wache R87 (c) beisst ohne Schranke
ja    R106 (c) Voraussetzung, Beleg docs/belege/TB-171/e_probe.txt, elliott_wave_stocks: Pruefung 1 ja (rc 0); Pruefung 2 ja, Wache R87 (c) beisst ohne Schranke
ja    R106 (c) Beleg docs/belege/TB-171/e_probe.txt: 16 von 16, rc 0
ja    R106 (c) Voraussetzung, Kursabschnitt: die Probe bildet ihn selbst (bauplan, einsetzen) in der Kopie des Test-Snapshots; der Snapshot entsteht aus default_rng(seed + k) im Temp-Ordner
info  Lesestelle Probe Z. 50: pd.read_csv(…) Wurzel d
info  Lesestelle Probe Z. 76: open(…) Wurzel tempfile.mkdtemp()
info  Lesestelle Probe Z. 79: pd.read_csv(…) Wurzel tempfile.mkdtemp()
info  Lesestelle Probe Z. 136: open(…) Wurzel tle.WURZEL
info  Lesestelle tle Z. 53: shutil.copy(…) Wurzel WURZEL
info  Lesestelle tle Z. 54: os.symlink(…) Wurzel WURZEL
info  Lesestelle tle Z. 96: open(…) Wurzel d
info  Lesestelle tle Z. 98: open(…) Wurzel d
info  Lesestelle tle Z. 106: pd.read_csv(…) Wurzel Speicher
ja    R106 (c) Voraussetzung, Lesen: 9 Lesestellen in Probe und tle, Wurzel nur Temp-Ordner der Probe (d, z, t, tempfile.mkdtemp()), Repo (WURZEL) oder Speicher
ja    R106 (c) Voraussetzung, Lesen: kein absoluter Pfad, kein expanduser/HOME, kein data/ des Repos; Kindprozess mit TB36_BASE_DIR und DATA_DIR im Temp-Ordner (Teilmessung am Code; e_probe.txt fuehrt keine Lesespur)
ja    TB-172: docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md und docs/belege/TB-172/m1_r102d.txt: R102 (d) ja bei rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout; rc 0
ja    TB-172: docs/belege/TB-172/m2_r92c.txt: R92 (c) erfüllt (150 von 150), rc 0
ja    BACKLOG-Leser: research/exposure_messung/auswertung.py Z. 73 liest <bot>_positionen.csv
ja    BACKLOG-Leser: research/faltenplan_neun/embargo_neun.py Z. 232 liest <bot>_positionen.csv
ja    BACKLOG-Leser: research/mtm_drawdown/grundlage.py Z. 65 liest <bot>_positionen.csv
ja    BACKLOG-Leser: research/tb24_haltedauern/auswertung.py Z. 71 liest <bot>_positionen.csv
ja    Index-Kopf Z. 3 nennt 0–65
ja    BACKLOG: Rang 1 (Stand TB-172) genau einmal
ja    Index: Zeile 65, Pflegezeile TB-170, Pflege-Anker je genau einmal; kein Abschnitt 17
ja    Dialog-Index: 17a noch nicht
ja    Journal: hoechste FI, naechste FJ frei
Pruefungen: 34, NEIN: 0
rc 0
```

## Register 66

`WZ register 17.10.2026 f79f239 … --probe` 5/0, rc 0 (`r_probe.txt`); `WZ register` 8/0, rc 0 (`r_eintrag.txt`). Aus `r_daten.json`:

- **Abschnitt 66** ab Z. 12531 (`## 66. Fable 17a — Registerblock R106 (TB-173)`); 66.1 Z. 12535, 66.2 Z. 12542. R106 und „Quelle des Grundes“ je genau einmal zeichengleich mit dem Codeblock.
- **Vier Marken** (Reihenfolge des Registers):

| Ort | Zeile | Kopf |
|---|---|---|
| 57.1 | Z. 12006 | 57.1 R90 ERGÄNZT durch R106 (66.1) |
| 61.1 | Z. 12240 | 61.1 R98 ERGÄNZT durch R106 (66.1) |
| 64.1 | Z. 12455 | 64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R106 (66.1) |
| 65.2 | Z. 12476 | 65.2 R105 PRÄZISIERT und ERGÄNZT durch R106 (66.1) |

Append-only bis auf die vier Markenpaare (je Leerzeile, Marke, „Eintrag und Stand oben bleiben zeichengleich.“). numstat Register `f79f239..7fe6342`: 78/0. Ohne Marke nach R106 (e): 56.4, 55.4, 54.2, 48.14, 65.3, Abschnitt 10. R = `7fe6342`, gepusht.

## Schritt K

| Beleg | rc | Inhalt |
|---|---|---|
| `k_registerkopie.txt` | 0 | Teil 6: Abschnitte 58–66, Body 106 592 B ≤ 240 000; BYTEGLEICH (1 217 316 B, sha256 `945ba13f…`) |
| `k_abschnitte.txt` | 0 | Abschnitte 0–66: 67 Dateien, BYTEGLEICH; neu `REGISTER_KOPIE_ABSCHNITT_66.md` |
| `k_pruefen.txt` | 0 | BYTEGLEICH |
| `k_index_zeilen.txt` | 0 | 471 Zahlen, davon 11 geändert (die Marken verschieben Zeilen) |
| `k_index.txt` | 0 | 5/0: 66 in T6, Kopf 0–66, Zeile „66 aus 17a“, Abschnitt 17 (4 Marken), Pflegezeile TB-173 |
| `k_handfelder.txt` | 0 | Handfelder 17a |
| `k_dialog_index.txt` | 0 | 67 Zeilen, 67 Antworten, gleich; 67 von 67 mit allen sechs Feldern |
| `k_dialog_pruefen.txt` | 0 | 67 von 67; offen 14, ohne Registertext 13, registriert 40 |

Keine weitere Teildatei. K = `ae5c151`, gepusht.

## BACKLOG und Journal

`WZ kennung`: „Kennung FJ (hoechste FI)“. `WZ backlog 17.10.2026 FJ` hängt an Rang 1 an: Register 66 mit TB-173; **R105 (c) Weg 1 bei `elliott_wave` und `elliott_wave_stocks` geschlossen** (R106 (c), Voraussetzung gemessen, 66.2 (a)); **`t3_supertrend` nach R106 (d)** Weg 1 oder Tatsachennotiz als eigener Handelscode-Punkt vor dem Tag; R102 (d)-Befund an den Verfahrensprüfer; vier Leser auf `<bot>_alle_trades.csv` umstellen. Journal-Block `docs/belege/TB-173/a_block.md` vor `## Wiederkehrende Lehren`. Belege: `a_*.txt`.

## Offen

- **`t3_supertrend` nach R106 (d):** Weg 1 (Fall auf dem Test-Snapshot herbeiführen: Einstieg vor dem Tag, Position über den Tag offen, danach ein zweites Kreuzen nach oben, z. B. über den Gleichstand mit konstanten Kursen) oder eine Tatsachennotiz mit Fundstelle, dass `use_t3_exit` nie False ist und der Gleichstand keinen Einstieg ohne Ausstieg bildet. Handelscode, eigener Auftrag mit Bau-Helfer und frischem Gegenleser — oder Tatsachennotiz.
- **R102 (d)-Befund** aus TB-172 an den Verfahrensprüfer mit der nächsten Anfrage.
- **Vier Leser vor der Neuerzeugung** auf `<bot>_alle_trades.csv` umstellen: `research/exposure_messung/auswertung.py` Z. 73, `research/faltenplan_neun/embargo_neun.py` Z. 232, `research/mtm_drawdown/grundlage.py` Z. 65, `research/tb24_haltedauern/auswertung.py` Z. 71. Ob `research/exposure_messung/auswertung.py` (eigene Liste aus `research/exposure_messung/daten/`) zur Neuerzeugung gehört, ist offen.
- **Index-Kopf:** mischt weiter Stände (BACKLOG seit TB-170).

## Abweichungen

Keine vom Auftrag. Beobachtungen:

- Unter der vorgegebenen ersten Zeile tragen die Commit-Nachrichten die Zuschreibungszeilen (Co-Authored-By, Claude-Session), wie in den bisherigen TB-Commits.
- Mehrere `git add` eines Schritts liefen in einem Bash-Aufruf mit `&&` verkettet statt je einem eigenen Aufruf; Pfade und Reihenfolge wie im Auftrag. Vor den Commits R und K habe ich `git status --porcelain` zusätzlich angesehen.
- Neben dem Werkzeug habe ich zum Schreiben dieses Ergebnisses die Fable-Antwort 17.10.a, das Ergebnis TB-172 und den Journalblock FI gelesen; ausgeführt wurde dabei nichts.

## In einfacher Sprache

Die neue Antwort des Verfahrensprüfers liegt jetzt zusammen mit Anfrage und Übergabe im Repo, und ihr Regeltext steht wortgleich als neuer Abschnitt im Register. An vier älteren Stellen weist ein kurzer Vermerk auf ihn hin; sonst wurde nur angehängt. Der Text hält fest, dass bei den zwei Elliott-Bots ein zu früher Kauf keinen späteren mehr verdrängt. Vorher wurde am Programmtext geprüft, dass die Wächter bei dieser Probe eingeschaltet waren und die Probe ihre Testkurse selbst baut. Offen bleiben ein eigener Code-Auftrag für den T3-Bot, eine Frage an den Prüfer und vier Leseprogramme, die vor dem Neuerzeugen der Listen umzustellen sind.
