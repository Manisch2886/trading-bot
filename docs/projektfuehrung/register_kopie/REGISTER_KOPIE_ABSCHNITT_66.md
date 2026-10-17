# REGISTER-KOPIE Abschnitt 66 (von 0–70) — Register-Z. 12591–12668 — Commit 47f184b3bd61a7a475f435acca81ad68c9112e21 — 2026-10-17 — Original sha256 640ee3a0ff7cad55bbfc5e673161c6b709311b99458cfb37edfa0134a216bb66 — KOPIE, nicht das Register

## 66. Fable 17a — Registerblock R106 (TB-173)

Reines Eintragen von Registertext, Bauart wie 65. Quelle ist allein `docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md`, md5 `e222920fc17f72fb7f516d41a6203457`, 9 756 B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R106)“, Z. 28–31, im Repo seit Commit `f79f239`. Nicht eingetragen werden „Kurz“, Fragen, Kenntnisse, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.a und die Übergabe 17.10.a (beide seit `f79f239`). Marken nach R106 (e). Karte des Betreibers (Auftrag TB-173, Abschnitt Freigabe, wörtlich): „Karte des Betreibers im Chat 33 („Opus Trading Bots-16.10.2026 c“), 17.10.2026, 16:27, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-173 frei? Das ist ein reiner Registerauftrag. Er schreibt Register 66 mit R106, zeichengleich aus Fable 17.10.a, mit den Marken an 65.2, 57.1, 61.1 und 64.1. Dazu kommen zwei Tatsachennotizen. (a) Die Voraussetzung aus R106 (c) ist gemessen: Die Wachen waren in der Probe eingeschaltet, und die Probe bildet ihren Kursabschnitt selbst, ohne eine Datei ausserhalb des Repos zu lesen. Das ist eine Teilmessung am Code. (b) Das Ergebnis von TB-172. Der Auftrag committet die drei Fable-Dateien vom 17.10.a unverändert. Im BACKLOG vermerkt er, dass Elliott geschlossen ist, dass t3_supertrend nach Weg 1 offen bleibt, dass R102 (d) an Fable geht und welche Leser auf die neue Positionsliste umzustellen sind. Der Auftrag ändert keinen Handelscode, es gibt keine Kurse, kein Live und kein Geld. bau.sh endet mit rc 0, beide Simulationen waren gut. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben."="Freigeben (Recommended)". You can now continue with these answers in mind.“ Eingetragen am 17.10.2026 mit TB-173.

### 66.1 R106 — Präzisierung und Ergänzung zu R105 (65.2) (Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks herbeigeführt, TB-171; Stand…

> R106 — Präzisierung und Ergänzung zu R105 (65.2) (Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks herbeigeführt, TB-171; Stand für t3_supertrend); Tatsachennotiz zu 64.1, Absatz „Abnahme nach R98 (d)“. (a) Lesart. „Eine spätere Welle“ und „eine andere, spätere Welle“ in R105 (c) heissen ein späteres Einstiegssignal nach R90 (g); bei den Elliott-Bots ist das der Einstieg, den die Wellenauswahl bildet, auch der spätere Einstieg derselben Welle (Schlüssel end_time, 65.3 (c)). Massstab bleibt R105 (b). (b) Test-Snapshot. Der Test-Snapshot in R90 (g) und R98 (d) ist ein gebauter Bestand; die Abnahme führt den Fall herbei. Eine Kopie des Test-Snapshots mit einem eingesetzten Kursabschnitt, die die Probe selbst und wiederholbar bildet, ist der Test-Snapshot dieser Prüfung, wenn der Erzeuger unverändert läuft und an seinen Ausgaben geprüft wird. (c) Stand. Für elliott_wave und elliott_wave_stocks ist der Fall nach R90 (g) am Listen-Erzeuger herbeigeführt und abgenommen (TB-171, research/tb24_haltedauern/test_elliott_verdraengung.py, sha256 59f6c90b…, 16 von 16, rc 0): mit Schranke kein Einstieg vor dem Tag, der zweite Einstieg erscheint; Gegenprobe: ohne Schranke endet die Wache nach R87 (c) mit 2; ohne Schranke und Wachen fehlt der zweite Einstieg. Die Gleichheit der Ausgaben mit und ohne Schranke an einem Symbol ohne Signal vor dem Tag steht mit TB-169 (Prüfung 3b, nach der Wiedergabe in der Anfrage 17.10.a). R105 (c) Weg 1 ist für beide Bots geschlossen; die Abnahme nach R98 (d) in 64.1 ist für die zwei Elliott-Bots vollständig, die Bedingung des Tags aus R105 (c) für sie erfüllt. Die Mutante (Schranke hinter traded.add, zweiter Einstieg fehlt) ist Gegenprobe zur Lage der Schranke, nicht Bedingung. [Voraussetzung, zu messen, nur das Ob: dass in der Prüfung mit Schranke die Wachen nach R86 (d) und R87 (c) eingeschaltet waren; dass die Probe den Kursabschnitt selbst bildet und keine Datei ausserhalb des Repos liest.] (d) t3_supertrend (R105 (d)). Die Fundstellen der Anfrage 17.10.a (backtest_trend.py Z. 70, 111–112, 123–124) nennen den Ort, an dem ein späterer Einstieg verdrängt würde (Einstieg nur bei position is None), und einen Grund für den Regelfall (Kreuzen nach unten schliesst vor dem nächsten Kreuzen nach oben, mit use_t3_exit). Zwei Öffnungen bleiben: use_t3_exit ist ein Parameter (Vorgabe True), und beim Gleichstand (Z. 112 „<=“, Z. 124 „<“) kann ein Kreuzen nach oben ohne vorheriges Kreuzen nach unten entstehen, das eine vor dem Tag geöffnete Position verdrängt. Ein Grenzfall ist ein Ort, an dem verdrängt wird (R105 (b)); durch Lesen ist er nicht auszuschliessen. Vor dem Tag schliesst ihn deshalb Weg 1 (der Fall wird auf dem Test-Snapshot herbeigeführt: Einstieg vor dem Tag, Position über den Tag offen, danach ein zweites Kreuzen nach oben; ohne Schranke fehlt es oder die Wache nach R87 (c) endet mit 2, mit Schranke erscheint es; 40.7), oder eine Tatsachennotiz mit Fundstelle sagt, dass use_t3_exit im Lauf und bei der Neuerzeugung nie False ist und der Gleichstand keinen Einstieg ohne Ausstieg bildet; dann greift die Ausnahme nach R90 (g). Welcher Weg, ist Handwerk. (e) Marken, der alte Satz bleibt zeichengleich: 65.2 (R105) — PRÄZISIERT durch R106, Unterpunkt (a); ERGÄNZT durch R106, Unterpunkte (b) bis (d). 57.1 (R90) — ERGÄNZT durch R106, Unterpunkt (b). 61.1 (R98) — ERGÄNZT durch R106, Unterpunkt (b). 64.1, Absatz „Abnahme nach R98 (d)“ — ERGÄNZT durch R106, Unterpunkt (c); die Marke steht nach dem Absatz. Ohne Marke: 56.4 (R87), 55.4 (R81), 54.2 (R75), 48.14 (R46) (Quelle des Grundes, Bauart); 65.3 (Befunde des steuernden Chats); Abschnitt 10.
> Quelle des Grundes: R105 (a) bis (d), R90 (c) und (g), R98 (d), R87 (c) im Wortlaut, R81 (h) und R75 (f) nach der Wiedergabe in R90, 40.7 nach der Wiedergabe in R105, R61 (b), R65 (a), 65.3 (c), 64.1, das Ergebnis TB-171 (docs/belege/TB-171/e_probe.txt nach seiner Wiedergabe), die Anfrage 17.10.a (docs/belege/TB-169/e_abnahme.txt Prüfungen 3a und 3b und backtest_trend.py nach ihrer Wiedergabe; Helfer BAU171 und Gegenleser GEGEN171B nicht gelesen). docs/belege/ und Code nicht gelesen. Kein Ergebnis.

> ⭐ **66.1 R106 ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (b), TB-175, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **66.1 R106 ERGÄNZT durch R108 (68.1)** (Fable 17c R108, Unterpunkt (e), TB-176a, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **66.1 R106 BERICHTIGT durch R109 (69.1)** (Fable 17d R109, Unterpunkt (b) („lies“), TB-178, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **66.1 R106 ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkt (a), TB-178, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken nach R106 (e): 65.2 (R105), Unterpunkt (a) präzisiert, Unterpunkte (b) bis (d) ergänzt; 57.1 (R90) und 61.1 (R98), Unterpunkt (b); 64.1, Absatz „Abnahme nach R98 (d)“, Unterpunkt (c). Ohne Marke: 56.4 (R87), 55.4 (R81), 54.2 (R75), 48.14 (R46); 65.3; Abschnitt 10. Voraussetzung in (c) gemessen: 66.2 (a). Stand t3_supertrend nach (d): BACKLOG Rang 1.

### 66.2 Voraussetzungen und Befunde

Gemessen vor dem Eintrag mit `docs/belege/TB-173/v_voraussetzung.txt` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-173), Zeilen wörtlich:

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

(a) R106 (c), Voraussetzung (nur das Ob), gemessen oben (Zeilen „R106 (c)“) am Code der Probe `research/tb24_haltedauern/test_elliott_verdraengung.py` (sha256 `59f6c90b…`), an `research/tb24_haltedauern/test_listen_erzeuger.py` und `research/tb24_haltedauern/positionen_holen.py` (Stand der Probe TB-171) und am Beleg `docs/belege/TB-171/e_probe.txt`: In der Prüfung mit Schranke (Prüfung 1) ruft die Probe den Erzeuger mit leerem Modus; die Wachen nach R86 (d) (`wache_zeilen`, `wache_trades`) und R87 (c) (`wache_trades`) ersetzt der Test nur in den Modi „wache1_aus“ und „wachen_aus“, der Erzeuger ruft beide ohne Bedingung — eingeschaltet: ja. Die Probe bildet den Kursabschnitt selbst (`bauplan`, `einsetzen`) in der Kopie des Test-Snapshots, der aus Zufallszahlen mit festem Seed im Temp-Ordner entsteht; gelesen werden nur Dateien dieses Temp-Ordners und des Repos, keine Datei ausserhalb — ja. **Teilmessung:** am Code, nicht an einer Lesespur des Laufs (`e_probe.txt` führt keine); den Code der Bots im Kindprozess verfolgt die Messung nicht (dort nur `TB36_BASE_DIR` und `DATA_DIR` auf den Temp-Ordner gesetzt).

(b) Tatsachennotiz TB-172 (`docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md`; Belege `docs/belege/TB-172/m1_r102d.txt`, `docs/belege/TB-172/m2_r92c.txt`): R102 (d) ja bei rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout (Indikatorwerte aus Zeilen vor dem Horizontbeginn, nur das Ob, durch Lesen des Codes); R92 (c) erfüllt (150 von 150 Aktien-Dateien, nur die Form von open_time). Der Befund zu R102 (d) geht als Frage an den Verfahrensprüfer; hier nichts entschieden.

(c) R56 (b): Übergabe, Anfrage und Antwort 17.10.a liegen seit `f79f239` im Repo.

