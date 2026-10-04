# TB-132 Register — Fable 02c (R66–R73) als Abschnitt 53, 21 Marken am alten Ort; Probe zu R71 in der Lock-Umgebung; Registerkopie, Index und Dialog-Index nachziehen

**Sitzungstitel:** `TB-132` · **Modell:** Opus 5.5, Aufwand hoch (Registerauftrag, wie TB-130) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 02.10.2026 vom steuernden Chat · **Neubau:** 04.10.2026 (nur das Datum des Eintrags)
**Vorgänger:** TB-131 (`0779453`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-132_register_fable_02c.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** immer `trading-env/bin/python3` (7c); das ist das Python der Lock-Umgebung. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15). Ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Datum des Eintrags: 04.10.2026, fest.** Kopf, Marken und Daten-Block tragen dieses Datum. Läuft die Sitzung an einem anderen Tag, bricht sie in 0a ab, ohne etwas zu schreiben oder zu committen. **Neubau 04.10.2026:** Die Fassung mit dem Datum 03.10.2026 (127 733 B, md5 `32e1849434e33737252db3eae165cc9a`, freigegeben am 03.10.2026) ist nicht gelaufen: Am 04.10.2026 um 07:36 standen HEAD und `origin/main` auf `0779453`, ein Commit von Schritt 0 fehlt, und `docs/belege/TB-132/` enthielt nur `vormessung/`. Der Wächter hat den Einfügesatz am 03.10.2026 um 07:29:38 ins Fenster gelegt (`logs/sitzungswaechter/waechter.log`, Zeile `2026-10-03T05:29:38Z`); ob er abgeschickt wurde, ist nicht gemessen. Gegenüber jener Fassung ist das Datum des Eintrags in 52 Zeilen geändert (Kopf, 0a.1, Commit-Text von Schritt 0, 0d, A4, Abbruchkriterien, „In einfacher Sprache“, die 21 Marken in Tabelle 2, die Zeile unter „Prüfsumme“, die Zeile vor dem Einfügeskript, das Feld `datum` und die 21 Marken im Daten-Block); dazu kommen dieser Absatz, der Zusatz in der Zeile „Sitzungstitel“, die Freigabe des Neubaus und der Hinweis unter „Prüfsumme“. Prüfskript und Einfügeskript sind zeichengleich (sha256 wie in Anhang A). **Start:** Ein erster Start von Hand in einer neuen Claude-Code-Sitzung der Claude-App (Betreiber, 04.10.2026) lief nicht im Hauptordner: Nach ihrer eigenen Meldung (weitergegeben 08:44) las die Sitzung den Zeiger auf `main` am Commit `0779453`, fand TB-132 dort nicht und hörte ohne Arbeit auf. Am Repo des Betriebsrechners hat sie nichts berührt (gemessen 08:46: HEAD, Arbeitsbaum, Worktree-Liste und `.git/FETCH_HEAD` unverändert; erschlossen: Cloud-Sitzung mit eigenem Klon). Gestartet wird deshalb wie üblich über den Sitzungswächter; den Einfügesatz schickt der Betreiber ab. Die Sitzung läuft lokal auf dem Betriebsrechner im Hauptordner `~/trading-bot`, nicht in einem Worktree und nicht in der Cloud; läuft sie woanders, steht TB-132 nicht im Zeiger oder der Arbeitsbaum weicht in 0a.2 ab, und sie hört ohne Commit auf.
**Prüfwerkzeuge:** Jedes Skript dieser Sitzung liegt unter `docs/belege/TB-132/` und wird mitcommittet, auch Vergleichsskripte.
**Bauart: TB-130.** Der Auftrag `docs/auftraege/MAC_TB-130_register_fable_02a.md` und die Skripte unter `docs/belege/TB-130/` sind die Vorlage; sie werden übernommen und angepasst, nicht neu erfunden. Wo dieser Auftrag „wie TB-130“ sagt, gilt der dortige Schritt mit den hier genannten Werten. Wo beide sich widersprechen, gilt dieser Auftrag. Verweist TB-130 an der Stelle weiter auf TB-129, gilt der Schritt aus TB-129 mit den Werten dieses Auftrags; solche Stellen nennen hier beide Aufträge. **Neu gegenüber TB-130:** die Datumsprüfung (0a, dazu als Wache im Einfügeskript), die Probe in der Lock-Umgebung (0e, dazu als Wache im Einfügeskript), der Wächter für die Freigabe (0a, 0d) und das Einfügeskript, das fertig in Anhang A steht (A4). **Massgeblich für Überschriften, Ketten, Marken und Fundstellen ist Anhang A** (Daten-Block), gebaut und geprüft vom steuernden Chat am 02.10.2026 am Register `ad351d5`.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**03.10.2026, Auswahlkarte im steuernden Chat (gestellt gegen 01:16, Antwort eingetragen 07:28).** Kartentext: *„Gibst du TB-132 frei? Das umfasst: Register Abschnitt 53 anhängen (R66–R73 zeichengleich aus Fables Antwort 02.10.c, dazu 53.9–53.10 mit den Messungen des steuernden Chats), 21 Marken am alten Ort (20 nach R70 (c), eine an 23.3 vom steuernden Chat nach R65 (a) bestimmt; keine in Abschnitt 10 und im ERZEUGT-Block), vorher die Probe zu R71 in der Lock-Umgebung (bei Abweichung kein Eintrag), Registerkopie, Index und Dialog-Index neu, BACKLOG-Block, Journal ED. Kein Code, kein neues Abbild. Datum des Eintrags fest 03.10.2026.“* Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**.

**Neubau 04.10.2026.** Die Freigabe oben galt der Fassung mit dem Datum 03.10.2026; sie ist nicht gelaufen. Für die Fassung mit dem Datum 04.10.2026: **04.10.2026, Auswahlkarte im steuernden Chat (gestellt gegen 08:00, Antwort eingetragen 08:41).** Kartentext: *„Gibst du den Neubau von TB-132 für den 04.10.2026 frei? Umfang wie am 03.10.2026 freigegeben: Register Abschnitt 53 anhängen (R66–R73 zeichengleich aus Fables Antwort 02.10.c, dazu 53.9–53.10 mit den Messungen des steuernden Chats), 21 Marken am alten Ort, vorher die Probe zu R71 in der Lock-Umgebung (bei Abweichung kein Eintrag), Registerkopie, Index und Dialog-Index neu, BACKLOG-Block, Journal ED. Kein Code, kein neues Abbild. Geändert ist nur das Datum des Eintrags: 04.10.2026 statt 03.10.2026. Start ausnahmsweise von Hand in einer Claude-Code-Sitzung in der App, lokal im Hauptordner ~/trading-bot.“* Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**.

| freigegeben | Pfad / Handlung |
|---|---|
| Register **anhängen** (Abschnitt 53: 53.0 Kopf, 53.1–53.8 = R66–R73 zeichengleich, 53.9–53.10 Text des steuernden Chats) und **21 Marken additiv** am alten Ort (Anhang A) | `docs/VORREGISTRIERUNG_neuselektion.md` |
| neu erzeugen, nachziehen | `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_<nn>.md`, `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` (beide über `docs/werkzeuge/registerkopie.py`), `docs/projektfuehrung/REGISTER_INDEX.md` |
| die Zeilen für 02b und 02c, die Zeile 02a (offen → nein) und die Schlusszeile (das Werkzeug `docs/werkzeuge/dialog_index.py` schreibt die Datei neu; was es dabei sonst ändert, steht im Ergebnis) | `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` |
| ein Block (Schritt B) | `docs/projektfuehrung/BACKLOG.md` |
| Journalblock (Kennung messen, erwartet **ED**) | `docs/projektfuehrung/JOURNAL.md` |
| committen in Schritt 0 | dieser Auftrag, `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/projektfuehrung/UEBERGABE.md`; unter `docs/projektfuehrung/` die sechs Dateien `FABLE_ANFRAGE_2026-10-02b_…`, `FABLE_UEBERGABE_2026-10-02b_eroeffnung.md`, `FABLE_ANTWORT_2026-10-02b_…`, `FABLE_ANFRAGE_2026-10-02c_…`, `FABLE_UEBERGABE_2026-10-02c_eroeffnung.md`, `FABLE_ANTWORT_2026-10-02c_…`; unter `docs/belege/TB-132/vormessung/` die neun Dateien der Vormessung |
| ausführen in 0e, einmal | `docs/belege/TB-132/vormessung/r71_probe.py` mit `trading-env/bin/python3` (lädt `research/vorregistrierung/benchmark.py` lesend; synthetische Kurse in einem Wegwerfordner unter `$TMPDIR`) |
| Belege, Ergebnis | `docs/belege/TB-132/`, `docs/ERGEBNIS_TB-132_register_fable_02c.md` |
| verwerfen, nur nach rotem Nachweis in A5 und nachdem der Diff als `abbruch_register.diff` gesichert ist | die eigene, uncommittete Änderung am Register (`git checkout -- docs/VORREGISTRIERUNG_neuselektion.md`) |

⛔ **Nicht freigegeben, mit Grund:**
- **Jede Zeile im Listentext von Abschnitt 10** und **im ERZEUGT-Block von Abschnitt 3.** *Grund:* Sonde (36.6, Prüfung (ii)) und `registerbericht.py --pruefen` vergleichen sie; R70 (c) nennt dort keinen Ort.
- **Jede Änderung oder Löschung einer bestehenden Registerzeile.** *Grund:* Das Register ist append-only; Marken sind neue Zeilen (34). Nachweis: numstat zweite Spalte 0. Die bestehenden `**Kette:**`-Zeilen bleiben, wie sie sind.
- **Eine Marke, die nicht in Anhang A steht.** *Grund:* Die Sitzung baut die Markentabelle nicht selbst (ARBEITSWEISE 0, Fehler Nr. 9).
- **Ein Registereintrag nach einer Abweichung in 0e.** *Grund:* R71 im Wortlaut: „weicht sie ab, wird gemeldet, nicht eingetragen“; R72 nennt dieselbe Wiederholung als Voraussetzung, „vor dem Eintrag zu messen“. Das Einfügeskript trägt die Sperre als Wache (A4).
- **Code jeder Art**, insbesondere `research/`, `shared/`, `strategies/`, `notifications/`, `docs/werkzeuge/`. *Grund:* Textauftrag. Die Wachen aus R66 (b), R66 (e) und R67, die Bewertung nach R72 (c) und die Öffnung von `auswertung.py` nach R69 (b) sind **nicht** Gegenstand. Auch die Probeskripte unter `docs/belege/TB-132/vormessung/` werden nicht geändert; findet 0e dort ein Hindernis, wird gemeldet.
- **Ein neues Abbild der Sperrliste.** *Grund:* Keine Sperrlistendatei bewegt sich.
- **Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests.** *Grund:* Sichtschutz. `registerbericht.py --pruefen` ist kein solcher Lauf und in 0b und A5 verlangt. `r71_probe.py` ist kein solcher Lauf: Die Probe liest keine Kurs- und keine Ergebnisdatei. `p3_probe.py` wird nicht ausgeführt.
- Löschen oder Verwerfen ausser dem einen Fall in der Tabelle; `crontab`, Datenbanken; `UEBERGABE.md`, `UEBERGABE_ARCHIV.md`, die Dateien `FABLE_ANTWORT_*`, `FABLE_ANFRAGE_*`, `FABLE_UEBERGABE_*` und die Dateien unter `docs/belege/TB-132/vormessung/` ändern (ausser dem Commit in Schritt 0). *Grund:* Das sind die Quellen.

**Sichtschutz 27.1:** Diese Sitzung liest keine Kennzahl, keine Trade- und keine Zeilenzahl aus Ergebnisdateien. Aus Testausgaben nur rc, Dauer und Schlusszeile. Code wird nur gelesen, wo Anhang A eine Fundstelle nennt. Die Ausgabe der Probe enthält synthetische Werte, keine Ergebnisse.

## Belegt · erschlossen · offen

*Gemessen vom steuernden Chat am 02.10.2026, ab 22:55, über die Geräteanbindung, nur lesend, an HEAD `0779453` (= `origin/main`).*

**Belegt:**
- Register: 11 313 Zeilen, sha256 `a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece`, md5 `80af174f41b41d006bd28dce54730c3f` (`docs/belege/TB-130/a5_messung_nachher.txt`; am Gerät nachgemessen). Letzter Commit, der es änderte: `ad351d5`. Letzter Abschnitt: 52 (letzter Unterabschnitt 52.5). Die Datei endet mit einem Zeilenumbruch.
- Quelle der R-Blöcke: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md`, md5 `6aad30eca53d038b65f24577680f7774`, 30 216 B, 157 Zeilen, uncommittet bis Schritt 0. Codezaun Z. 133 bis Z. 157; Blöcke R66–R73 in Z. 134–156, zwischen zwei Blöcken je eine Leerzeile. Zwei unabhängige Abschriften aus der Ablage, `cmp` gleich; md5 auf dem Gerät gleich.
- **Schnittregel (maschinell geprüft, 8/8):** wie TB-130 und TB-129. Ein Block beginnt mit der Zeile, die mit `R<n> — ` beginnt, und endet einschliesslich der ersten folgenden Zeile, die mit `Quelle des Grundes:` beginnt; je Block genau zwei Zeilen. Geschnitten wird **nur** in Z. 134–156. ⚠️ Die Antwort 02b führt R66–R71 in einer älteren Fassung; sie ist **nicht** Quelle.
- Ausgangswerte (`docs/belege/TB-130/a5_messung_nachher.txt`): `herkunft.register()` `4caf01793c8c4bb979eeea0243cff7a1b13004c28716391f61e8a5978a407b56`, `fehlend []`, 23 Teile · gültiges Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f` · Sonde dagegen: rc 2 (Normalfall), 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“, sha256 des JSON-Berichts ohne das Feld `zeilen` `9f7364ef32fd80ffba6931c776f3bdf43dc257a1f6aeac304cf818c89023f35e` · `registerbericht.py --pruefen`: rc 1 (bekannter Befund; verglichen wird nachher gegen vorher) · Abschnitt 10: Z. 965–1171, sha256 der Datei `0b_abschnitt10_nachher.txt` `da8697c0be1da37f8c6d1eddbf715e8003ba517c119576766f13c0e6a61889bc`; ERZEUGT-Block: Z. 260–460, `fda8ead14e4cd96e91548078f9e9dbae0c3a0c631b2a483f4bee757da31c9207` · `test_vorregistrierung` 196/196, rc 0, 894 s, mit diesem Register (`docs/belege/TB-130/a5_test_vorregistrierung.txt`).
- Seit `1e13135` ist unter `research/`, `shared/`, `strategies/`, `config/`, `data/` nichts geändert (`git diff --name-only 1e13135 HEAD --` leer, gemessen 02.10.2026, 22:57; TB-131 änderte nur `docs/`).
- Registerkopie am `0779453`: 53 Abschnittsdateien, vier Teile (gezählt; `--pruefen` läuft in C1).
- `FABLE_DIALOG_INDEX.md`: 52 Antworten, Zeile `02a` mit offen = ja, keine Zeile `02b` und keine `02c`; im Ordner liegen 54 Dateien `FABLE_ANTWORT_*.md`. `BACKLOG.md`: 287 Zeilen, der Anker `## 6 — Geparkt, null Arbeit` zählt 1, `Aus Fable 02b und 02c` zählt 0 (vom steuernden Chat am Gerät gemessen).
- **Lock-Umgebung:** `trading-env/pyvenv.cfg` nennt `version = 3.9.6`; `trading-env/bin/python3` zeigt auf `/Library/Developer/CommandLineTools/usr/bin/python3`; unter `trading-env/lib/python3.9/site-packages` liegen `pandas-2.3.3`, `numpy-2.0.2`, `pandas_market_calendars-4.6.1`, `exchange_calendars-4.5.6` (dist-info); `requirements.lock:52` `pandas==2.3.3`, `:50` `numpy==2.0.2`. Gestartet hat der steuernde Chat dieses Python nicht (in der Geräte-Shell nicht ausführbar).
- **Probe:** `docs/belege/TB-132/vormessung/r71_probe.py`, md5 `4398f6faafff22b786ff1c92554c9f64`, 435 Zeilen; statisch auf Python 3.9 geprüft (keine `match`-Anweisung, keine `X | Y`-Typangabe, kein `zip(strict=…)`, kein geklammerter Kontextmanager, keine f-Zeichenkette mit wiederholtem Anführungszeichen). Vergleichsdatei `docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt`, md5 `adecffe00ffafd7735fbf644ec3d9734`, 25 Zeilen; die Zeile `A - Faelle, die die Aussage pruefen (bestimmen den Rueckgabewert)` ist Z. 6, die Kopfzeile mit den Fassungen Z. 3. Die Vergleichsdatei stammt aus der Geräte-Shell (pandas 2.3.3, numpy 2.2.6, Python 3.10.12), nicht aus der Lock-Umgebung.
- **Trockenlauf und Nachbau (steuernder Chat, 02.10.2026):** Das Prüfskript aus Anhang A lief am echten Repo über die Geräteanbindung mit rc 0 (Ausgabe unter „Prüfsumme“). Die Probe lief in einem Nachbau der Lock-Fassungen (Python 3.9.6, pandas 2.3.3, numpy 2.0.2, aber Linux, nicht der Betriebsrechner): rc 0, Zeile 3 wie in 0e verlangt, ab `A - Faelle` zeilengleich mit der Vergleichsdatei. Das ersetzt 0e nicht. Im Nachbau bricht die Probe mit `UnicodeEncodeError` ab, wenn die Standardausgabe nicht UTF-8 ist (sie druckt „—“); deshalb steht `PYTHONIOENCODING=utf-8` im Aufruf von 0e. Die Variable ändert die Probe nicht.
- Nummern: TB frei ab 133 · Journal **ED** (die Sitzung misst) · R-Blöcke nach diesem Auftrag frei ab R74.

**Erschlossen:** Keine der 21 Marken steht vor Abschnitt 10 (die erste Einfügestelle ist Z. 1447); Abschnitt 10 und der ERZEUGT-Block wandern nicht. Verglichen wird trotzdem wie in TB-130 und TB-129: der JSON-Bericht der Sonde ohne das Feld `zeilen`. Die Ausgabe der Probe sollte ab der Zeile `A - Faelle` der Vergleichsdatei gleichen, weil sie dort nur Tage, Wahrheitswerte und den Wortlaut einer pandas-Warnung druckt.

**Offen (die Sitzung misst, nimmt nichts an):** der Ausgang der Probe in der Lock-Umgebung; die Journal-Kennung; die neuen Zeilenbereiche und Teilgrenzen der Registerkopie; welche weiteren Zeilen `dialog_index.py` ändert.

## Schritt 0 — Datum, Sicherung, Ausgang, Vorprüfung, Probe

**0a. Zuerst, bevor irgendetwas geschrieben oder committet wird.**

1. **Datum:** `date '+%d.%m.%Y'` ⇒ Soll `04.10.2026`. Jedes andere Datum ⇒ **Abbruch mit Meldung, ohne Commit und ohne Beleg im Repo.** Der steuernde Chat baut den Auftrag dann für den neuen Tag neu.
2. **Arbeitsbaum:** `git status --porcelain > "$TMPDIR/tb132_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch.

*Eingetragen vom steuernden Chat beim Ablegen (der Ordner `docs/belege/TB-132/` enthält nur `vormessung/` mit neun Dateien):*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-132_register_fable_02c.md
?? docs/belege/TB-132/
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02c_messung_vor_eintrag_r66_r71.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02b_eroeffnung.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md
```

3. **Skripte aus Anhang A auslesen und Arbeitsbaum prüfen.** Die zwei Skripte werden mit genau diesem Aufruf aus dem Auftrag gelesen, nicht abgeschrieben:

```
trading-env/bin/python3 - docs/auftraege/MAC_TB-132_register_fable_02c.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
for kopf, name in (("### Prüfskript", "pruefe_anhang_tb132.py"), ("### Einfügeskript", "a4_eintrag.py")):
    i = z.index(kopf)
    a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
    b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
    t = "\n".join(z[a + 1:b]) + "\n"
    open(sys.argv[2] + "/" + name, "w", encoding="utf-8").write(t)
    print(name, hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: die zwei sha256 aus Anhang A. Dann `trading-env/bin/python3 "$TMPDIR/pruefe_anhang_tb132.py" docs/auftraege/MAC_TB-132_register_fable_02c.md . --arbeitsbaum > "$TMPDIR/tb132_0a_pruefung.txt"; echo "rc $?"` ⇒ Soll rc 0 (Datum, Register, Anker, Quelle, md5 der 15 gelegten Dateien, Fundstellen, uncommittete Dateien genau wie im Daten-Block). rc ≠ 0 ⇒ Abbruch. Das Prüfskript gibt auch dann rc 1, wenn im Auftrag unter „Freigabe des Betreibers, wörtlich“ noch der Platzhalter statt der Freigabe steht. Der Schalter `--trockenlauf` wird **nicht** benutzt.

Commit `TB-132 Schritt 0: Stand des steuernden Chats 04.10.2026 (Fable 02b und 02c, Vormessung)`, pushen. Danach steht für alle Quellenangaben der Commit von Schritt 0, im Folgenden **⟨S0⟩** (kurz, 7 Zeichen). Erst jetzt `$TMPDIR/tb132_0a.txt` und `$TMPDIR/tb132_0a_pruefung.txt` nach `docs/belege/TB-132/0a_status.txt` und `0a_pruefung.txt` kopieren, die zwei Skripte nach `docs/belege/TB-132/0d_vorpruefung.py` und `docs/belege/TB-132/a4_eintrag.py` (zeichengleich; sha256 danach noch einmal).

**0b. Ausgangswerte** ⇒ `docs/belege/TB-132/0b_ausgang.txt`, mit `0b_ausgang.sh` nach der Vorlage `docs/belege/TB-130/0b_ausgang.sh`. Soll: die Werte unter „Belegt“; dazu md5 und Bytes der Quelle 02c am Commit ⟨S0⟩ und im Arbeitsbaum, `0b_abschnitt10_vorher.txt` und `0b_erzeugt_vorher.txt` (Soll: die zwei sha256 unter „Belegt“). Weicht ein Wert mit Soll ab ⇒ Abbruch.

**0c. Basis `test_vorregistrierung`:** `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` ⇒ `0c_basis.txt`. Leer ⇒ die Basis ist der Beleg `docs/belege/TB-130/a5_test_vorregistrierung.txt` (196/196). Nicht leer ⇒ Basislauf am Stand ⟨S0⟩ ohne Zeitgrenze, Soll 196/196, sonst Abbruch.

**0d. Vorprüfung vor jedem Registereintrag** ⇒ `docs/belege/TB-132/0d_vorpruefung.txt`: `trading-env/bin/python3 docs/belege/TB-132/0d_vorpruefung.py docs/auftraege/MAC_TB-132_register_fable_02c.md .` (ohne Schalter), am Commit ⟨S0⟩. Soll rc 0, die erste Zeile `Datum: 04.10.2026 wie verlangt`, die fünf Zeilen von `Marken:` bis `Bloecke:` wie unter „Prüfsumme“ in Anhang A und die Schlusszeile `rc 0: alles wie angegeben`. Geprüft ist damit:
1. **Marken:** Jeder Anker aus dem Daten-Block kommt im Register genau 1-mal vor, steht am Anfang der genannten Ankerzeile, und jede Einfügestelle „nach Zeile N“ beginnt mit dem angegebenen Anfang. Weicht eine Marke ab ⇒ **Abbruch vor Schritt A**.
2. **Quelle:** md5 der Antwortdatei; die Schnittregel ergibt genau R66–R73, je zwei Zeilen, in Z. 134–156.
3. **Noch nicht vergeben:** Im Register zählt `## 53.` 0, und keine Zeile beginnt mit `> R66 — `.
4. **Fundstellen für 53.9 und 53.10:** jede Zeile der Liste `fundstellen` (Datei, Zeile, Teilzeichenkette: die Zeile enthält sie), jede Zeilenliste aus `zeilen_mit` (Datei, Teilzeichenkette, genau diese Zeilennummern) und jede Zählung aus `zaehlungen`, `glob_summen` und `baum_summen` (dort: alle `*.py`, die git führt oder die unverfolgt und nicht ignoriert sind, ohne `ergebnisse/` und `trading-env/`). **Weicht hier etwas ab ⇒ Abbruch vor Schritt A.** Dazu gehören die zwei Zählungen in `BACKLOG.md` (der Anker zählt 1, `Aus Fable 02b und 02c` zählt 0). Weichen sie ab, bricht schon 0a ab, bevor etwas committet ist.
5. **Dateien:** md5 und Bytes der 15 Dateien aus Schritt 0 wie im Daten-Block.
6. **Freigabe:** Im Auftrag steht kein Platzhalter für die Freigabe mehr. Sonst ⇒ Abbruch.

Nicht nachgemessen werden in 0d die Zählungen am Datenbestand und die Kalendervergleiche aus der Vormessung (`v3_daten.md`, `v5_code_02c.md`); 53.9 nennt sie als Messung der Helfer.

**0e. Probe in der Lock-Umgebung (R71; R72, erste Voraussetzung), vor jedem Registereintrag.** Aus dem Repo-Wurzelverzeichnis, genau so:

```
touch "$TMPDIR/tb132_0e_marke"
unset TB_SELEKTIONSWURZEL TB_SELEKTIONSHASH TB_SELEKTIONSCOMMIT TB30A_BASE_DIR R71_BENCHMARK
PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 trading-env/bin/python3 docs/belege/TB-132/vormessung/r71_probe.py > docs/belege/TB-132/probe_lock_r71.txt 2> docs/belege/TB-132/probe_lock_r71_stderr.txt; echo "rc $?" > docs/belege/TB-132/probe_lock_r71_rc.txt
trading-env/bin/python3 docs/belege/TB-132/0d_vorpruefung.py docs/auftraege/MAC_TB-132_register_fable_02c.md . --probe docs/belege/TB-132/probe_lock_r71.txt > docs/belege/TB-132/0e_probe_vergleich.txt; echo "rc $?" >> docs/belege/TB-132/0e_probe_vergleich.txt
find . \( -name __pycache__ -o -name '*.pyc' \) -newer "$TMPDIR/tb132_0e_marke" -not -path './trading-env/*' -not -path './.git/*' > docs/belege/TB-132/0e_pycache.txt
```

Soll, alle vier:
1. Rückgabewert der Probe **0** (`probe_lock_r71_rc.txt`).
2. Zeile 3 der Ausgabe lautet genau `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6` (pandas 2.3.3 und die Fassungen des Locks; eine andere numpy- oder Python-Fassung heisst: Das war nicht die Lock-Umgebung).
3. Ab der Zeile, die mit `A - Faelle` beginnt, ist die Ausgabe **zeilengleich** mit `docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt` (20 Zeilen, von Z. 6 bis Z. 25 der Vergleichsdatei, bis zur Zeile `ERGEBNIS: … Rueckgabewert 0`; das Prüfskript meldet `Zeilen ab 'A - Faelle': 20 (Vergleich 20)`). Die Zeilen 1 bis 5 dürfen abweichen (Pfad, Fassungen).
4. Der Vergleich in `0e_probe_vergleich.txt` endet mit `rc 0: alles wie angegeben` und `rc 0`.

`probe_lock_r71_stderr.txt` wird festgehalten und im Ergebnis genannt (leer oder Wortlaut); sie ist kein Abbruchkriterium. `0e_pycache.txt` muss leer sein: Die Probe hat dann weder einen Ordner `__pycache__` noch eine `*.pyc` angelegt oder erneuert. Ist sie nicht leer: die Pfade in der Abgabe melden, **nichts löschen**; kein Abbruch. Danach `git status --porcelain`: Neu sind nur Dateien unter `docs/belege/TB-132/`.

**Weicht einer der vier Punkte ab: nichts am Register ändern.** Ausgabe, rc und Vergleich bleiben als Beleg; Grund nach `docs/belege/TB-132/abbruch.txt`; Commit `TB-132 0: Ausgang, Vorprüfung, Probe weicht ab (kein Registereintrag)`, pushen, melden, Sitzung beenden. Die Probe wird nicht geändert und nicht mit anderen Schaltern wiederholt.

Commit `TB-132 0: Ausgang, Vorprüfung, Probe in der Lock-Umgebung`, pushen.

## Schritt A — Abschnitt 53 und die Marken, in einem Lauf

**A1. Gliederung (vom steuernden Chat vergeben):** 53.0 Kopf · 53.1–53.8 = R66–R73 in der Reihenfolge des Codezauns (53.n = R(65 + n)) · 53.9–53.10 Text des steuernden Chats (A3). Überschriften und Ketten stehen exakt im Daten-Block von Anhang A. Form je R-Block wie in 52 und 51 (TB-130 A1, dort nach TB-129 A1): Überschrift, Leerzeile, die zwei Blockzeilen je mit `> ` davor, Leerzeile, Kette. Drei Überschriften (53.1, 53.4, 53.7) wären länger als 140 Zeichen; sie sind am Ende an einer Wortgrenze mit „…“ gekürzt (Bauart 47.4 und 48.7, TB-126). Der Block darunter steht vollständig. Abschnitt 53 wird ans Dateiende angehängt, mit einer Leerzeile nach der letzten bestehenden Zeile.

**A2. Marken am alten Ort.** Die 21 Marken stehen fertig in Anhang A; massgeblich ist der Daten-Block. Die Sitzung baut die Tabelle **nicht** selbst. Je Marke: eine Leerzeile, Markenzeile 1, Markenzeile 2. Das Datum steht fest in der Markenzeile. Eingesetzt wird nach den Zeilennummern am Original; an derselben Einfügestelle steht die Marke mit der kleineren R-Nummer zuerst.

Regeln, nach denen Anhang A gebaut ist (zur Prüfung, nicht zum Neubauen): 20 Marken zählt R70 (c) auf. Eine weitere (23.3, Registertext 3b (c), PRÄZISIERT durch R72 (b)) hat der steuernde Chat nach R65 (a) bestimmt: R72 (b) fasst den Benchmark-Tag „im Sinn von 23.3“ enger als der Wortlaut des Registertexts, R70 (c) nennt nur die Tatsachennotiz; die Marke trägt den Zusatz „vom steuernden Chat nach R65 (a) bestimmt“ und geht zur Kenntnis an Fable (53.10 Nr. 8). Der Ort heisst in der Marke wie in R70 (c); wo R70 (c) den Ort selbst mit Unterpunkt nennt (15.3 (a), 15.3 (c), R48 (d)), steht er im fetten Teil, sonst nicht. Der Unterpunkt des neuen Blocks steht in der Klammer. Bei 52.2 schreibt R70 (c) „ERGÄNZT durch R66 (zu (e))“: Der Zusatz gehört dort zur Marke, nicht zum Ort; er steht deshalb als „zu (e)“ in der Klammer von Marke 14 (gemeint ist R64 (e); Vorbild „zu 27.4 und 27.6“ in der Marke an Abschnitt 27 aus TB-129). Eine Bestätigung trägt ERGÄNZT mit dem Zusatz, was bestätigt ist (48.7, R69). Bei 52.2 nennen die Marken zu R71 und R72 im fetten Teil, was präzisiert ist (erster Kurstag; Benchmark-Tag), wie R70 (c) es in der Klammer tut. Block in 47–52: nach dem Blockzitat und den dort stehenden Marken, vor der Zeile `**Kette:**`. 15.3: direkt unter dem Blockzitat, nach der dort stehenden Marke aus R41, vor der Formelzeile. 23.3, Registertext: direkt unter dem Blockzitat des Ersatztexts. 23.3, Tatsachennotiz: unter dem Blockzitat der Notiz (R70 (c), Vorbild 25.2). Abschnitt 27: am Ende des Abschnitts nach den dort stehenden Marken. 52.4: nach der Tabelle, vor `### 52.5`. An einem Ort: nach den vorhandenen Marken, dann in der Folge der Blocknummern. Keine Marke tragen 7 (c), 17.5 und 50.7 Nr. 3 (R70 (b), Indexzeilen, C3) sowie 24.2 und 29.3 (R70 (c)).

**A3. Text des steuernden Chats** — zeichengleich, mit ⟨S0⟩ ersetzt; ⟨S0⟩ steht im Register in Backticks, wie in 52 (dieselbe Ersetzung macht das Einfügeskript). Der Kopf steht vor 53.1, der Schluss nach 53.8.

Kopf:

````
## 53. Fable 02c — Registerblock R66–R73 (TB-132)

Reines Eintragen von Registertext, Bauart wie 52. Quelle ist allein `docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md`, md5 `6aad30eca53d038b65f24577680f7774`, 30 216 B, im Repo seit Commit ⟨S0⟩, Abschnitt „Registerblock — zeichengleich kopierbar (R66–R71 in der Fassung 02c, sie ersetzen die Fassung 02b vollständig; R72 und R73 neu)“, Z. 134–156. Sie ersetzt die Fassung der Blöcke R66–R71 aus der Antwort 02.10.b vollständig. Die Antwort 02.10.b (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md`) bleibt im Repo; ihre Blöcke sind nie eingetragen worden. Zum Dialog gehören ausserdem die Anfrage 02.10.b (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md`) und die Anfrage 02.10.c (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02c_messung_vor_eintrag_r66_r71.md`). Die Antwortdatei 02.10.c hat der steuernde Chat am 02.10.2026 aus Fables Ablage übertragen, in zwei unabhängigen Abschriften, `cmp` gleich; die Bytegleichheit mit der Ablage ist nicht gemessen. Die Eröffnungstexte (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02b_eroeffnung.md`, `docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md`), die zwei Anfragen und die Antwort 02.10.b liegen seit ⟨S0⟩ im Repo; dieser Kopf nennt Datei, md5 und Commit, das ist die Bindung nach R56 (b). Den Anfangsbestand des Chats hält R73 (53.8) fest: Die Antwort 02.10.c stammt aus dem Chat der Antwort 02.10.b. Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Überschriften von 53.1, 53.4 und 53.7 sind am Ende gekürzt („…“, wie 47.4 und 48.7); der Block darunter steht vollständig. Die Nummern 53.1–53.8 hat der steuernde Chat vergeben (Auftrag TB-132, Einzelfreigabe des Betreibers), nicht Fable. Gesetzt sind 21 Marken: die 20, die R70 (c) aufzählt, und eine an 23.3, Registertext 3b (c), die der steuernde Chat nach R65 (a) bestimmt hat (53.10 Nr. 8). Die Marken zur Tatsachennotiz in 23.3 stehen unter dem Blockzitat der Notiz (R70 (c), Vorbild 25.2). ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke. Ohne Marke bleiben 7 (c), 17.5 und 50.7 Nr. 3 (R70 (b), Indexzeilen) sowie 24.2 und 29.3 (R70 (c)). Die Wiederholung der Probe in der Lock-Umgebung, die R71 und R72 vor dem Eintrag verlangen, ist in TB-132 vor diesem Eintrag gelaufen (53.9). Die Voraussetzungen und Tatsachen der Blöcke stehen mit Befund in 53.9; was offen bleibt, steht in 53.10. Die Vormessung des steuernden Chats liegt unter `docs/belege/TB-132/vormessung/`. 53.9 und 53.10 sind Text des steuernden Chats, nicht Fables.
````

Schluss:

````
### 53.9 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 02c „zu messen“ nennt, und zu den Tatsachen, die die Blöcke über Code und Daten führen. Gemessen am 02.10.2026 am Stand `0779453`, nur lesend, durch Helfer des steuernden Chats; die Berichte liegen unter `docs/belege/TB-132/vormessung/` (`v1_register.md` bis `v5_code_02c.md`, dazu zwei Proben und die zwei Ausgaben der Probe zu R71). Die Sitzung TB-132 hat in Schritt 0 die genannten Zeilen und Zählungen an Code und Register am Commit ⟨S0⟩ nachgemessen (`docs/belege/TB-132/0d_vorpruefung.txt`) und die Probe zu R71 in der Lock-Umgebung wiederholt. Die Zählungen am Datenbestand und die Kalendervergleiche hat sie nicht wiederholt. Zeilenangaben zum Code gelten am Commit ⟨S0⟩. „REG Z.“ nennt Registerzeilen am Stand `ad351d5`, also vor diesem Eintrag. Aussagen über ein Fehlen (kein Aufrufer, kein Kalender im Lauf, kein Zellen-Erzeuger) sind Lesung der Helfer, soweit keine Zählung genannt ist. Gezählt sind Datumszeilen, Zeilennummern und Fassungen. Kein Ergebnis gelesen (27.1).

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R66 (53.1) (b) | welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld `kalender`) | Das Paket `pandas_market_calendars` importiert im Repo nur `notifications/boersenkalender.py` (Z. 81); dort stehen `KALENDER_NAME = "NYSE"` (Z. 70) und der einzige Aufruf `mcal.get_calendar(KALENDER_NAME)` (Z. 109). Die Datei steht nicht auf der Sperrliste und nicht im Laufbereich, weder in `ARBEITSBAUM_PFADE` (`shared/paths.py:239–253`) noch in der gemessenen Hülle (`docs/belege/TB-112/a2_laufbereich.txt`, 84 Pfadzeilen, davon 3 Messumschläge). `shared/entscheidungskerze.py` erreicht sie in Z. 384 (`import boersenkalender`). Diese Datei zählt über den Ordner `shared` zu `ARBEITSBAUM_PFADE`; zur gemessenen Hülle zählt sie nicht. Importiert wird sie von den neun `strategies/*/forward_test.py`, von Tests und von Forschungsskripten, von keinem Modul der gemessenen Hülle: Der Aufruf kommt aus dem Live-Pfad, nicht aus dem Selektionslauf. In den Pfaden der Hülle und in den neun Dateien der Sperrliste und der Gruppe „eingefroren“ steht kein Import und kein Aufruf des Pakets (vier Treffer der Suche in der Hülle sind Kommentar oder Docstring). Das Feld `kalender` aus TB-47 (`research/snapshotgrenze/erhebung_eingaben.py:606–610`) führt Importstellen und Paketfassung, keinen Kalendernamen; 17.5 nennt keinen. Am Bestand vom 02.10.2026 (nur Datumsspalten, nicht der Snapshot des Laufs): 16 275 Kurstage des Aktienmarktes von 1962-01-02 bis 2026-09-01; gegen den Kalender „NYSE“ des Pakets (4.6.1) 0 Tage nur im Kalender und 0 Tage nur in den Daten. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09). Beide Kalendervergleiche sind Ersatzmessungen ausserhalb der Lock-Umgebung: Python 3.10 und pandas 2.3.3 des Systems, die Kalenderpakete in den Fassungen des Locks aus `trading-env` | nicht entscheidbar: Der Code des Laufs benutzt heute keinen Kalender; welchen Namen der Zellen-Erzeuger nimmt, ist offen (53.10 Nr. 1). Die Wache nach R66 (b) prüft die Wahl im Lauf |
| R66 (53.1) (c) | dass der Aufruf mit 252 Perioden je Jahr, bei Krypto 365, die Formel aus 15.3 trifft | `research/vorregistrierung/kennzahlen.py:95–108` (`sharpe`) rechnet `s = float(np.std(r, ddof=1))` (Z. 105) und gibt `float(np.mean(r)) / s * math.sqrt(perioden_je_jahr)` zurück (Z. 108); Standardabweichung 0 oder weniger als zwei Werte ergeben 0. Formel im Register: REG Z. 1449–1450; 1c: REG Z. 1442–1443. Registrierte Konstante ist `registerdaten.py:109` `HANDELSTAGE_JE_JAHR = 252`; die 365 steht als Literal in `auswertung.py:264–265` | trifft für die Funktion; einen Aufruf gibt es noch nicht (der Zellen-Erzeuger fehlt). Den Nenner der Standardabweichung nennt das Register nicht; der Code legt n − 1 fest (R50). Ein nicht endlicher Wert in der Reihe ergäbe still 0; R67 schliesst ihn aus |
| R66 (53.1) (f) | Tatsachen im Block, keine Voraussetzung | `sharpe` (`kennzahlen.py:95–108`) hat keinen Aufrufer in `research/vorregistrierung`, `shared`, `strategies` und `docs/belege` (Suche nach `kz.sharpe(`, `kennzahlen.sharpe(` und `sharpe(`: nur die Definition); `sharpe_fn=` in `beispieldaten.py` (Z. 144, 180) und in den Tests reicht andere Funktionen weiter (`standard_sharpe`, Lambdas), nicht `kennzahlen.sharpe`; `auswertung.py` liest `netto_sharpe` nur aus `zellen.csv` (Z. 353–354, 395, 577, 622–623, 684); `bootstrap` 0 Treffer in `research/vorregistrierung/*.py`. DSR: `auswertung.py:670` mit den Renditen aus `beta_bereinigung` (Schnitt Z. 517, Fenster Z. 511), `kennzahlen.py:219–246`; die Schwelle des DSR kommt aus der Varianz der Selektionsstatistik über die Zellen (`auswertung.py:587–588`). Vier erste Falten: 33.2 (REG Z. 5972, 5973, 5975 und 5976), 23.4 (REG Z. 4009–4014) | trifft |
| R68 (53.3) (b) | Tatsache im Block („auswertung.py liest sie für kein Urteil“) | `mittlere_exposure` wird in `auswertung.py` an zwei Stellen gelesen: Z. 405 in `zulaessigkeit`, nur über die Selektionsfalten (Z. 403); Z. 626 in `bestaetigungsperiode`, nur für den Bericht (Z. 728) | trifft |
| R69 (53.4) | Tatsache in der Quelle des Grundes (was `auswertung.py` nicht kennt) | `zellenbericht` 0 Treffer in `auswertung.py`; `kapital_drawdown_mtm_pct` und `bestaetigung_ab_effektiv` 0 Treffer in allen `*.py` des Repos (ohne `ergebnisse/` und `trading-env/`); `kapital_drawdown_pct` in `auswertung.py` Z. 40, 134, 413–414, 625, 681–682 und 824; `auswertung.py:379` liest `f"{markt}.csv"` | trifft |
| R71 (53.6) | die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner; weicht sie ab, wird gemeldet, nicht eingetragen | `docs/belege/TB-132/vormessung/r71_probe.py`, in TB-132 vor diesem Eintrag mit dem Python der Lock-Umgebung (`trading-env/bin/python3`) wiederholt; die Ausgabe liegt unter `docs/belege/TB-132/probe_lock_r71.txt` und ist ab der Zeile „A - Faelle …“ zeilengleich mit `docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt` | trifft (Rückgabewert 0; bei Abweichung wäre dieser Abschnitt nicht entstanden) |
| R72 (53.7), erste | die Wiederholung der Probe in der Lock-Umgebung auf dem Betriebsrechner | dieselbe Probe; die Ausgabe zeigt das Fortschreiben an der Lücke und nach dem Reihenende, wie (a) und (d) es beschreiben. Unter pandas 3.0.5 (`docs/belege/TB-132/vormessung/ausgabe_pandas_3.0.5.txt`) füllt `pct_change()` nicht auf | trifft |
| R72 (53.7), zweite | dass kein vorhandener Kern, den der Zellen-Erzeuger für die MtM-Reihe übernimmt, am Lückentag anders bewertet als (c) | Einziger vorhandener Kern für eine tägliche MtM-Reihe ist `research/mtm_drawdown/mtm_kern.py`; Z. 166–168 schreibt den letzten Kurs fort (`eigene.ffill()`), Z. 244–247 lässt die Position in `n_offen` und `gebunden` und zählt den Positionstag in `fortgeschrieben`. Probe auf synthetischen Daten (`docs/belege/TB-132/vormessung/p3_probe.py`, pandas 2.3.3, ausserhalb der Lock-Umgebung): Änderung 0 am Lückentag. `exposure_kern.py`, `bot_lauf.py` und der Zellen-Kern nach R43 bewerten nicht täglich. Daneben steht eine Näherung, `research/exposure_messung/auswertung.py::mtm_reihen` (Z. 305–341): Sie schreibt am Lückentag ebenfalls fort (Z. 323), füllt aber vor dem ersten Kurs rückwärts auf und überspringt ein Symbol ohne Kursreihe (Z. 321–322) | trifft für diesen Kern. Nicht von selbst erfüllt: `tagesraster` (Z. 135–148) lässt einen Tag aus, an dem kein übergebenes Symbol einen Kurs hat (das Raster nach R66 (a) gibt der Erzeuger); `gebunden` steht zum Einstand. Welchen Kern der Zellen-Erzeuger übernimmt, legt kein Registertext fest |
| R72 (53.7) (d) | Tatsache im Block („Am Bestand vom 02.10.2026 endet keine Reihe früher“) | Am Bestand (nur Datumsspalten; Dateien vom 02.09.2026 und 15.09.2026): Krypto, je Bot 24 Symbole, 2017-08-17 bis 2026-09-14: keine Lücke, kein Tag ohne jedes Symbol, keine früher endende Reihe, kein doppeltes Datum. Aktien, 150 Symbole: zwei Symbol-Tage Lücke (1974-06-03 `LMT`, 2026-08-10 `MNST`), keine früher endende Reihe, kein doppeltes Datum. Nicht gemessen: Zeilen ohne `close`, der Handelbar-Schnitt je Bot | trifft |
| R73 (53.8) | keine Voraussetzung | Die Angaben sind die des Verfahrensprüfers; der steuernde Chat kann sie nicht messen. Der Eröffnungstext 02.10.c (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md`) liegt im Repo; er war nicht Anfangsbestand | Tatsachennotiz des Verfahrensprüfers |
| R66–R73, Zitate und Verweise | — | 98 Stellen gegen den Wortlaut gemessen (`docs/belege/TB-132/vormessung/v4_register_02c.md`). Sinngemäss treffen zehn: R72 (b) fasst den Benchmark-Tag enger als der Wortlaut von 23.3 (REG Z. 3933–3936), das ist der Inhalt der Präzisierung; R72 nennt im Kopf den Registertext 3b (c), R70 (c) setzt die Marke nur an die Tatsachennotiz (53.10 Nr. 8); „TB-47, Feld kalender“ steht nur in der Erläuterung unter 17.5 (REG Z. 2847); „Dafür“ steht in R60 (c) klein (REG Z. 11196); „Bauart R55, R64“ in R69 (b) meint Prüfungen mit Gegenprobe, die Bauart der beauftragten Änderung steht in R45 (REG Z. 10857); von einer Öffnung spricht unter R36, R37, R34 und R55 nur R55; „R54 an 7 (c)“ ist in R61 (b) ein Glied der Aufzählung, keine Zeile (REG Z. 11209); 24.6 (REG Z. 4471) berichtet eine Zählung in einer Messung; R56 (c) (REG Z. 11168) nennt drei Fälle, der von R73 ist keiner davon; 23.2, Grund 2 (REG Z. 3908) ist Deutung des Verfahrensprüfers | keine Stelle trifft nicht; die sinngemässen gehen zur Kenntnis an Fable (53.10 Nr. 9) |

### 53.10 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | Kalendername für die Aktien-Tagesreihe (R66 (a), (b)): Der Code des Laufs benutzt keinen; im Repo steht nur „NYSE“ im Live-Pfad (53.9) | nächste Anfrage an Fable |
| 2 | Deckelfall (R68 (d)): Behandlung in den Gleichheitsproben nach R60 (c) und R64 (d) und in der Nachrechnung nach R36 | Frage an Fable vor der Öffnung nach R69 (b) |
| 3 | Verfahrensmessung am Snapshot (R72 (d)): keine Kursreihe endet vor dem letzten Kurstag ihres Marktes; Zahl der Symbol-Tage Lücke im Zeitraum nach R66 (a) | vor dem signierten Tag |
| 4 | Planmässige Öffnung von `auswertung.py` (R69 (b)): Dateiname je Bot, mit R36, R37, R34 und R55; Beispieldaten und Tests folgen | eigener Umsetzungsauftrag mit Freigabe, vor der Abnahme nach R46 |
| 5 | Zellen-Erzeuger: Kalender und Raster nach R66 (a); Wachen nach R66 (b), R66 (e) und R67; Falten-Sharpe über die Sharpe-Funktion aus `kennzahlen.py` (R66 (c)); Bewertung am Lückentag und Zahl der Positionstage je Bot (R72 (c)); Zeile der Bestätigungsperiode nach R68 | mit dem Zellen-Erzeuger, Abnahme nach R46 |
| 6 | Wiederholung der Probe bei einer Änderung der pandas-Fassung im Lock (R72 (e)) | bei Anlass, vor dem Tag |
| 7 | Tagesbasis des DSR (R66 (f)): gehört zum Nebenbefund 50.7 Nr. 3 | vor dem Tag |
| 8 | Marke an 23.3, Registertext 3b (c): PRÄZISIERT durch R72 (b). R70 (c) nennt sie nicht; der steuernde Chat hat sie nach R65 (a) bestimmt | nächste Anfrage an Fable, zur Kenntnis |
| 9 | Die sinngemässen Verweise aus 53.9 (letzte Zeile) | nächste Anfrage an Fable, zur Kenntnis |
| 10 | `tagesschluss` (`benchmark.py:155`, `159–160`) normalisiert `open_time` nicht und prüft keine doppelten Daten; am Bestand vom 02.10.2026 folgenlos | mit der Verfahrensmessung nach Nr. 3 |

Von 52.5 sind damit erledigt: Nr. 2 durch R66 (a) und (c), Nr. 5 durch R67, Nr. 6 durch R68 (a) und (b), Nr. 7 durch R69, Nr. 9 durch R70 (a). Nr. 1 (zweite Voraussetzung zu R64) wird nach R66 (e) im Lauf geprüft. Nr. 3 bleibt; der Deckelfall (R68 (d), hier Nr. 2) berührt die Probe dort. Nr. 4 und 8 bleiben, wie sie dort stehen.
````

**A4. Einsetzen.** Das Einfügeskript steht fertig in Anhang A (`### Einfügeskript`); die Sitzung schreibt es nicht selbst und ändert es nicht. Es liegt seit 0a zeichengleich unter `docs/belege/TB-132/a4_eintrag.py`. Es liest Kopf, Schluss und den Daten-Block aus diesem Auftrag und die Blöcke aus der Antwortdatei, beides als Datei. Deshalb vorher: `git diff --quiet ⟨S0⟩ -- docs/auftraege/MAC_TB-132_register_fable_02c.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md; echo "rc $?"` ⇒ Soll rc 0. **Zuerst ein Probelauf gegen eine Kopie** (`cp` des Registers in den Scratch, dann `trading-env/bin/python3 docs/belege/TB-132/a4_eintrag.py --s0 ⟨S0⟩ --register <kopie>`), Vorlage `docs/belege/TB-130/a4_probelauf.sh`; an der Kopie laufen die Textprüfungen aus A5. Erst wenn sie grün sind, einmal echt (`… --s0 ⟨S0⟩ --daten docs/belege/TB-132/a4_eintrag_daten.json`); danach muss das Register `cmp`-gleich mit der Kopie sein. **Zwei Wachen trägt das Skript selbst**, in jedem Lauf ohne `--vorschau`, also im Probelauf und im echten Lauf: Es schreibt nur, wenn das Datum des Rechners der 04.10.2026 ist, und nur, wenn `docs/belege/TB-132/probe_lock_r71.txt` vorhanden ist, ihre Zeile 3 genau `  pandas 2.3.3, numpy 2.0.2, Python 3.9.6` lautet und sie ab der Zeile `A - Faelle` zeilengleich mit `docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt` ist (0e). Sonst bricht es mit einer Meldung ab, bevor es schreibt; das ist dann ein Abbruch, kein Anlass für einen anderen Aufruf. Der Schalter `--vorschau` hebt beide Wachen auf; er gehört dem Soll-Bau des steuernden Chats und wird von der Sitzung **nicht** benutzt. Das Skript nimmt ihn nur zusammen mit `--register <Pfad einer Kopie>` an und verweigert, wenn dieser Pfad (nach `realpath`) das echte Register `docs/VORREGISTRIERUNG_neuselektion.md` im Repo ist: Im Vorschau-Modus wird das Register des Repos nie geschrieben. Soll der Ausgabe: `Marken gesetzt am alten Ort: 21 an 13 Einfuegestellen` · `R-Bloecke: 8 (R66-R73)` · `Zeilen vorher: 11313  nachher: 11471  eingefuegt: 158`. Die Wachen stehen im Kopf des Skripts; eine verletzte Wache bricht ab, bevor geschrieben wird.

**A5. Nachweis:** wie TB-130 A5, dort nach TB-129 A5 (die Liste der Nachweise steht in TB-129), mit `docs/belege/TB-130/a5_*` als Vorlage, unabhängig vom Einfügeskript, und diesen Werten: R-Diff **8/8** rc 0 (Quelle Z. 134–156 gegen 53.1–53.8), Mutationsprobe an einer Kopie rc 1 · Zitate (Kopf und Schluss aus diesem Auftrag, ⟨S0⟩ ersetzt) 2/2 rc 0 · Überschriften und Ketten 8/8 · Marken 21/21 gegen Anhang A, je mit der Folgezeile und der Zeile nachher; keine Markenzeile doppelt · numstat des Registers **`158	0`** · Zeilenzahl nachher 11471 · Abschnitt 10 und ERZEUGT-Block bytegleich gegen `0b_*_vorher.txt` · `registerbericht.py --pruefen` nachher = vorher · Sonde: JSON ohne `zeilen` nachher = vorher, (ii) 0, „Listentext wie bei Erzeugung: ja“ · `herkunft.register()` nachher ≠ vorher, `fehlend []`, 23 Teile, der neue Wert nur im Ergebnis (42.5) · `test_vorregistrierung` am echten Register vor dem Commit, ohne Zeitgrenze, 196/196 (Vorlage `docs/belege/TB-130/test_vorregistrierung.sh`). Ist ein Nachweis am echten Register rot: Diff als `docs/belege/TB-132/abbruch_register.diff` sichern, Register mit `git checkout -- docs/VORREGISTRIERUNG_neuselektion.md` zurücksetzen, Abbruch. **Das Register wird nur committet, wenn alle Nachweise grün sind.** sha256 und md5 des Registers nachher stehen im Ergebnis; der steuernde Chat baut das Soll mit demselben Einfügeskript nach und vergleicht.

Commit `TB-132 A: Register 53 (R66–R73 zeichengleich, Tatsachennotizen 02c), Marken`, pushen. **Das ist der einzige Commit, der das Register ändert.**

## Schritt B — BACKLOG (5b)

Verfahren wie TB-130 Schritt B, dort nach TB-129 Schritt B (Vorlage `docs/belege/TB-130/b_einfuegen.py` und `b_vergleich.py`; Belege `b_einfuegung.txt`, `b_numstat.txt`, `b_vergleich.txt`): Anker vorher zählen (Soll genau 1, in 0a und 0d schon geprüft; sonst nicht ausführen, vermerken, weitermachen), Text aus **diesem Auftrag** einfügen, erste Textzeile nachher zählen (Soll 1), numstat zweite Spalte 0, Bytevergleich des Blocks.

#### E1 — Abschnitt 5: Bewertung von Fable 02b und 02c (5b)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile** (genau eine Leerzeile davor und danach; eine vorhandene wird nicht verdoppelt)

```
### Aus Fable 02b und 02c (02.10.2026) — Bewertung nach 5b, eingetragen mit TB-132

- **Bewertung 02b:** Nicht eingetragen. Von 56 Zitaten und Verweisen trafen 40 im Wortlaut, 14 sinngemäss, 2 nicht (beide in R68: 2d aus 15.4 ist durch 16.6 ersetzt; „beide Träger“ in R60 (c) meint anderes). Die Messung vor dem Eintrag brachte zwei Tatsachen, die 02b nicht kannte: den Handelskalender nach 17.5 und einen Sharpe im DSR auf den gemeinsamen Tagen. Die Antwort bleibt im Repo; ihre Blöcke R66–R71 sind durch 02c vollständig ersetzt.
- **Bewertung 02c:** Die Antwort trägt. 98 Zitate und Verweise gemessen: keines trifft nicht, zehn treffen sinngemäss (53.9, letzte Zeile). R66–R73 stehen seit TB-132 im Register, Abschnitt 53; Befunde in 53.9, Offenes in 53.10. Frage 1 anders als die Neigung: Für Aktien gilt der Handelskalender nach 17.5, die Kurstage sind die Probe dazu, eine Abweichung endet mit 2. Die Probe zu R71 lief in TB-132 in der Lock-Umgebung, vor dem Eintrag.
- **R73:** Die Eröffnung 02.10.c kam im Chat der Antwort 02b an; der Betreiber wählte per Karte, dass dieser Chat antwortet. Fables Ampel: 🔴. Die nächste Anfrage geht an einen neuen Chat (F4).
- **An Fable, nächste Anfrage:** der Kalendername für die Aktien-Tagesreihe (im Repo steht nur „NYSE“, im Live-Pfad; „XNYS“ führt im gemessenen Fenster einen Handelstag mehr); der Deckelfall nach R68 (d), vor der Öffnung nach R69 (b); zur Kenntnis die Marke an 23.3, Registertext 3b (c), und die sinngemässen Verweise (53.10 Nr. 8 und 9).
- **Vor dem signierten Tag:** Verfahrensmessung am Snapshot nach R72 (d) (Reihenende, Symbol-Tage Lücke; dabei `open_time` und doppelte Daten, 53.10 Nr. 10); Tagesbasis des DSR mit dem Nebenbefund 50.7 Nr. 3; Wiederholung der Probe, falls sich die pandas-Fassung im Lock ändert (R72 (e)).
- **Umsetzungsauftrag mit Freigabe (R69 (b)):** planmässige Öffnung von `auswertung.py`: Benchmark-Datei je Bot, zusammen mit R36, R37, R34 und R55; Beispieldaten und Tests in derselben Änderung; neues Abbild.
- **Anforderungen an den Zellen-Erzeuger aus 02c:** Tagesreihe auf jedem Handelstag ab dem 1. Januar der ersten Selektionsfalte (R66 (a)); Wachen mit Ausgang 2 nach R66 (b), R66 (e) und R67; Falten-Sharpe über die Sharpe-Funktion aus `kennzahlen.py` mit 252, bei Krypto 365 (R66 (c)); Bewertung am Lückentag zum letzten Kurs und Zahl der Positionstage je Bot (R72 (c)); Zeile der Bestätigungsperiode nach R68. `mtm_kern.py` bewertet am Lückentag wie R72 (c); sein Raster und `gebunden` zum Einstand passen nicht von selbst (53.9).
```

Soll numstat: `10	0` (9 Zeilen des Blocks und eine Leerzeile danach).

## Schritt C — Registerkopie, Index, Dialog-Index

**C1. Registerkopie:** wie TB-130 C1, dort nach TB-129 C1 (die fünf Aufrufe stehen in TB-129; hier wie dort je Ausgabe und rc nach `c1_*.txt`). Soll: rc 0 je Aufruf; 54 Abschnittsdateien `_00` bis `_53`. Schreiblauf mit rc 2 oder 3 oder `--pruefen` mit rc ≠ 0 ⇒ festhalten, Kopien nicht committen, melden (kein Abbruch; C2 und C3 entfallen dann).

**C2. `docs/projektfuehrung/REGISTER_INDEX.md` nachziehen**, nach der Bauart von TB-130 C2, dort nach TB-129 C2 (Vorlagen `docs/belege/TB-130/c2_*`, sonst `docs/belege/TB-129/c2_*`): Kopf (Commit, „Abschnitte 0–53“, Zeilenzahl, sha256, „nachgezogen in TB-132“, der Verweis auf die Abschnittsdateien bis `_53.md`) · „Wie gemessen“ (Zahlen je Art und Belegpfad neu aus `c1`) · Abschnittstabelle mit neuer Zeile 53 und der Teil-Zuordnung · alle Zeilenangaben „Z. n“ auf den neuen Stand · in der Tabelle der Registertexte ab Abschnitt 18 eine Zeile „53 aus 02c“ (R66–R73 = 53.1–53.8; 53.9 Voraussetzungen und Befunde; 53.10 Offenes) und die Verweise an den Orten mit neuer Marke (15.3 in der Tabelle der Registertexte 0–7; 23, 27, 48, 51, 52) · neuer Abschnitt `## 8. Die Marken aus Fable 02c (TB-132)` in der Form von Abschnitt 7, mit den 21 Marken und ihren Zeilen nachher, vor der letzten Trennlinie `---` und dem Pflegeblock · Pflegezeile.

**C3. Indexzeilen statt Marken (R70 (b)).** Ein eigener Block `### Indexzeilen aus Fable 02c` im neuen Abschnitt 8 des Index, mit genau diesen drei Zeilen (zeichengleich). Vorher zählen: `Indexzeilen aus Fable 02c` zählt 0.

```
- **7 (c):** mittlere Exposure des Gewinners, Tage nach R64 (a), (b) und (d) (52.2). Ohne Marke (R70 (a) und (b), 53.5).
- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1). Ohne Marke (R70 (b), 53.5).
- **50.7 Nr. 3:** Tagesbasis des DSR → R66 (f) (53.1). Ohne Marke (R70 (b), 53.5).
```

**C4. Dialog-Index.** Die Datei `docs/belege/TB-132/c4_handfelder.json` mit genau diesem Inhalt anlegen:

```
{"02a": {"offen": "nein"}, "02b": {"frage": "Führt die Tagesreihe Tage vor dem ersten Handelbar-Tag und über welche Tage läuft der Falten-Sharpe, wer schliesst fehlende Werte und doppelte Daten aus, ab wann gilt R64 für die Zeile der Bestätigungsperiode, wie heisst die Benchmark-Datei, und trägt 7 (c) eine Marke?", "entscheidung": "Tagesreihe ab dem 1. Januar der ersten Falte, Falten-Sharpe über alle Tage der Tagesreihe (R66–R71 in erster Fassung). Nicht eingetragen: Die Messung vor dem Eintrag brachte zwei Tatsachen, die die Antwort nicht kannte (17.5; Sharpe im DSR), die erste Voraussetzung zu R68 traf nicht, die zu R71 nur eingeschränkt. Ihre Blöcke sind nie eingetragen worden und durch 02c vollständig ersetzt.", "offen": "nein"}, "02c": {"frage": "Welche Quelle gilt für den Handelskalender der Aktien-Tagesreihe, auf welchen Tagen steht der Sharpe im DSR, bleibt R68 ohne 2d, was gilt an Kurslücke und Reihenende im Benchmark, welche Orte tragen Marken, und unter welchen Nummern kommen geänderte Blöcke?", "entscheidung": "Kalender nach 17.5, die Kurstage sind die Probe, eine Abweichung endet mit 2 (R66); der Sharpe im DSR bleibt wie im Code (R66 (d), (f)); Reihen eindeutig, vollständig und endlich (R67); Zeile der Bestätigungsperiode ab bestaetigung_ab_effektiv (R68); R39 bestätigt, planmässige Öffnung von auswertung.py (R69); Marken (R70); erster Kurstag einmal je Bot (R71); Kurslücke als Tatsachennotiz, Reihenende am Snapshot messen (R72); Anfangsbestand des Chats (R73). Dieselben Nummern, letzte Fassung.", "offen": "ja"}}
```

Dann `trading-env/bin/python3 docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-132/c4_handfelder.json`, danach `--pruefen` ⇒ `c4_dialog_index.txt`. Soll (Docstring Z. 6–30): `--pruefen` rc 0; 54 Antworten; Zeile `02c` mit Fundstelle 53 und Status „offen“ (offen = ja: R66 (b) nennt eine Voraussetzung, deren Befund „nicht entscheidbar“ ist, R68 (d) stellt eine Frage zurück, R72 (d) verlangt eine Messung am Snapshot); Zeile `02b` mit Fundstelle 53 und Status „registriert“ — das Werkzeug leitet den Status aus dem Dateinamen im Kopf von 53 ab, eingetragen ist aus 02b nichts, das sagt das Feld Entscheidung; Zeile `02a` mit Status „registriert“ (ihre offenen Punkte sind durch 02b und 02c beantwortet oder laufen in 53.10 weiter), Frage und Entscheidung unverändert. `git diff --numstat` festhalten; weitere geänderte Zeilen im Ergebnis nennen (kein Abbruch).

Commit `TB-132 B/C: BACKLOG, Registerkopie, Index, Dialog-Index`, pushen.

## Schritt D — Abgabe

**D1.** `docs/ERGEBNIS_TB-132_register_fable_02c.md`, Bau wie ERGEBNIS_TB-130, dort wie ERGEBNIS_TB-129: Kopfzeile, Stand und Commits, Kurz-Tabelle je Schritt (Soll | Ist), **Probe in der Lock-Umgebung** (rc, Kopfzeile 3 im Wortlaut, Vergleich, stderr), Markentabelle (21 Marken mit Zeile nachher), Register nachher (Zeilen, sha256, md5), `herkunft.register()` vorher und nachher, **Für Fable** (53.10 Nr. 1, 2, 8 und 9; jede Reibung beim Setzen), **Nicht getan** (53.10; die Ablage macht der steuernde Chat), **In einfacher Sprache**.

**D2. Journal:** Block nach dem letzten Buchstabenblock von `docs/projektfuehrung/JOURNAL.md`, vor `## Wiederkehrende Lehren`. Kennung vorher messen (erwartet **ED**), mit Quellenzeile.

**D3.** Abgabe-Commit `TB-132 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-132/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a: Das Datum ist nicht der 04.10.2026 (Abbruch ohne Commit); der Arbeitsbaum weicht ab; ein sha256 der zwei Skripte weicht ab; das Prüfskript gibt nicht rc 0 (auch: die Freigabe ist nicht eingesetzt).
- Ein Ausgangswert aus 0b mit Soll weicht ab; der Basislauf in 0c (falls nötig) ist nicht 196/196.
- 0d: rc ≠ 0 (Marken, Quelle, „noch nicht vergeben“, Fundstellen, Dateien, Freigabe; auch eine einzelne Marke).
- 0e: einer der vier Punkte weicht ab ⇒ melden, **nicht eintragen**.
- A4: Eine Wache des Einfügeskripts schlägt an (Datum, Probe, sha256, Anker).
- Ein Nachweis aus A5 ist rot, jeder der dort genannten.
- Eine Datei ausserhalb der Freigabetabelle müsste geändert werden.
- `git push` scheitert zweimal.

**Kein Abbruch:** der BACKLOG-Anker ≠ 1 erst in Schritt B, also nach bestandenem 0d (nicht einfügen, nennen) · `Indexzeilen aus Fable 02c` zählt in C3 nicht 0 (nicht einfügen, nennen) · `registerkopie.py` mit rc ≠ 0 (Kopien nicht committen, nennen; C2 und C3 entfallen, C4 nicht) · weitere geänderte Zeilen im Dialog-Index (nennen) · eine nicht leere `probe_lock_r71_stderr.txt` bei erfüllten vier Punkten (nennen) · eine nicht leere `0e_pycache.txt` (nennen, nichts löschen) · eine Reibung zwischen Fable-Text und Code oder Register (unter „Für Fable“ nennen).

**Bei Abbruch nach dem Commit von Schritt 0:** committen, was an Belegen da ist, **nie** `JOURNAL.md` mit Platzhalter, Grund in `docs/belege/TB-132/abbruch.txt`, pushen, melden. Kein Registertext mit einem Befund, den dieser Auftrag nicht vorsieht.

## In einfacher Sprache

Fable hat am 02.10. acht Regeltexte geschrieben (R66–R73). Sie legen fest, an welchen Tagen die tägliche Wertreihe eines Bots geführt wird, wie Lücken in den Kursen behandelt werden und wie eine Datei heissen muss, die das Auswertungsprogramm liest. Die Sitzung läuft nur am 04.10.2026; an jedem anderen Tag hört sie sofort auf, ohne etwas zu verändern. Die Dateien, die der steuernde Chat bereitgelegt hat, sichert sie gleich am Anfang ins Repo (Commit und Push), noch vor dem Test. Bevor sie etwas ins Register einträgt, wiederholt sie einen kleinen Test auf dem Betriebsrechner, in genau der Programmumgebung, in der später gerechnet wird. Nur wenn der Test dasselbe zeigt wie die Vormessung, kopiert sie die Texte per Skript ins Register, Zeichen für Zeichen, als Abschnitt 53, und setzt 21 Hinweise an alten Stellen. Dazu kommt eine Tabelle mit dem, was im Code und in den Daten nachgemessen wurde, und eine Liste dessen, was offen bleibt. Am Code ändert sich nichts.

---

## Anhang A — TB-132: Überschriften, Ketten, Marken, Fundstellen, Prüfskript und Einfügeskript (Vorlage für die Mac-Sitzung)

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `ad351d5` (11 313 Zeilen, sha256 `a7496780…`), HEAD `0779453`. Gebaut vom steuernden Chat am 02.10.2026 mit einem Skript, das Ankerzeilen, Einfügestellen und Zeilenanfänge am Register misst; jeder Anker kommt im Register genau einmal vor. **Alle Zeilennummern gelten am Original, vor jeder Einfügung.** **Massgeblich für Skripte ist der JSON-Block am Ende.**

### Tabelle 1 — Überschriften und Ketten (8)

Die Überschrift ist der Anfang des Blocks bis vor den Satzpunkt. Wo die Zeile länger als 140 Zeichen wäre, ist sie am Ende an einer Wortgrenze mit „…“ gekürzt (53.1, 53.4, 53.7).

| x.n | Überschriftzeile (exakt) | Zeichen | Kette (exakt) |
|---|---|---|---|
| 53.1 | `### 53.1 R66 — Präzisierung zu Registertext 1a und 1c (15.3 (a), (c)) und Ergänzung zu R64 (e) (52.2) (Kalender der Tagesreihe; Tage des…` | 137 | `**Kette:** Marken: 15.3 (a); 15.3 (c); 52.2 (R64); 52.4, Zeile „R64 (52.2), zweite“. Indexzeilen ohne Marke (R70 (b)): 17.5; 50.7 Nr. 3. Voraussetzung gemessen: 53.9. Offen: 53.10 Nr. 1, 5 und 7.` |
| 53.2 | `### 53.2 R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen)` | 112 | `**Kette:** Marken: 48.7 (R39). Offen: 53.10 Nr. 5.` |
| 53.3 | `### 53.3 R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv)` | 120 | `**Kette:** Marken: 48.1 (R33); 48.5 (R37); 52.2 (R64). Tatsache gemessen: 53.9. Offen: 53.10 Nr. 2 und 5.` |
| 53.4 | `### 53.4 R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py (Name der Benchmark-Datei); Präzisierung zu R64 (e) (52.2)…` | 139 | `**Kette:** Marken: 48.7 (R39); 51.5 (R60); 52.2 (R64); 52.4, Zeile „R64 (52.2) (a)“. Tatsache gemessen: 53.9. Offen: 53.10 Nr. 4.` |
| 53.5 | `### 53.5 R70 — Marken zu R64 (7 (c)) und zu R66 bis R73; Präzisierung zu R61 (b) (51.6) und R65 (a) (52.3)` | 106 | `**Kette:** Marken: 51.6 (R61); 52.3 (R65). Nach (c) gesetzt: 20 Marken, je in der Kette des Blocks, der sie auslöst. Indexzeilen ohne Marke nach (b): 7 (c); 17.5; 50.7 Nr. 3. Offen: 53.10 Nr. 8 und 9.` |
| 53.6 | `### 53.6 R71 — Berichtigung der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in 23.3 (welcher Tag ausgelassen wird)` | 116 | `**Kette:** Marken: 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; 52.2 (R64). Voraussetzung gemessen: 53.9.` |
| 53.7 | `### 53.7 R72 — Tatsachennotiz zu Registertext 3b (c) (23.3) (Kurslücke und Reihenende im Benchmark) und Ergänzung zu R48 (d) (48.16)…` | 133 | `**Kette:** Marken: 23.3, Registertext 3b (c) (vom steuernden Chat bestimmt, 53.10 Nr. 8); 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; 48.16 (R48); 52.2 (R64). Voraussetzung gemessen: 53.9. Offen: 53.10 Nr. 3, 5, 6 und 10.` |
| 53.8 | `### 53.8 R73 — Tatsachennotiz zu 27 nach R56 (c) (die Antwort 02c stammt aus dem Chat der Antwort 02b)` | 102 | `**Kette:** Marken: Abschnitt 27. Keine Voraussetzung (53.9).` |

### Tabelle 2 — Marken (21)

Sortiert nach Einfügestelle, an derselben Stelle nach R aufsteigend. Jede Marke: Leerzeile, Markenzeile 1, Markenzeile 2 `> Eintrag und Stand oben bleiben zeichengleich.` „Zahl“ = `str.count` des Ankers über den ganzen Registertext. „Grund“ nennt den Wortlaut aus R70 (c) oder, bei Nr. 3, die Regel R65 (a), die der steuernde Chat angewandt hat.

| Nr | Grund | Registerstelle | Anker (Ankerzeile) | Zahl | Einfügestelle | Markenzeile 1 (exakt) |
|---|---|---|---|---|---|---|
| 1 | R70 (c): 15.3 (a) — PRÄZISIERT durch R66, Unterpunkte (a) und (b) | 15.3 (a) | `### 15.3 Registertext 1` (Z. 1428) | 1 | nach Zeile 1447: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **15.3 (a) PRÄZISIERT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (b), TB-132, 04.10.2026).` |
| 2 | R70 (c): 15.3 (c) — PRÄZISIERT durch R66, Unterpunkt (c) | 15.3 (c) | `### 15.3 Registertext 1` (Z. 1428) | 1 | nach Zeile 1447: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **15.3 (c) PRÄZISIERT durch R66 (53.1)** (Fable 02c R66, Unterpunkt (c), TB-132, 04.10.2026).` |
| 3 | R65 (a), angewandt vom steuernden Chat: R72 (b) „Benchmark-Tag des Bots im Sinn von 23.3“; R70 (c) nennt den Ort nicht | 23.3, Registertext 3b (c) | `> **Registertext 3b (c), Fassung 20.09.2026` (Z. 3928) | 1 | nach Zeile 3939: `> an jedem Tag in derselben Menge.` | `> ⭐ **23.3, Registertext 3b (c) PRÄZISIERT durch R72 (53.7)** (Fable 02c R72, Unterpunkt (b), vom steuernden Chat nach R65 (a) bestimmt, TB-132, 04.10.2026).` |
| 4 | R70 (c): 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — BERICHTIGT durch R71 | 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | `**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**` (Z. 3957) | 1 | nach Zeile 3964: `> Tag eine Berichtigung des Codes an den` | `> ⭐ **23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse BERICHTIGT durch R71 (53.6)** (Fable 02c R71, TB-132, 04.10.2026).` |
| 5 | R70 (c): 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — ERGÄNZT durch R72 | 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse | `**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**` (Z. 3957) | 1 | nach Zeile 3964: `> Tag eine Berichtigung des Codes an den` | `> ⭐ **23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse ERGÄNZT durch R72 (53.7)** (Fable 02c R72, TB-132, 04.10.2026).` |
| 6 | R70 (c): 27 — ERGÄNZT durch R73 | Abschnitt 27 | `## 27. Sichtschutz` (Z. 5124) | 1 | nach Zeile 5197: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **Abschnitt 27 ERGÄNZT durch R73 (53.8)** (Fable 02c R73, TB-132, 04.10.2026).` |
| 7 | R70 (c): 48.1 (R33) — PRÄZISIERT durch R68 | 48.1 (R33) | `### 48.1 R33` (Z. 10771) | 1 | nach Zeile 10774: `> Quelle des Grundes: Datenvertrag von a` | `> ⭐ **48.1 R33 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).` |
| 8 | R70 (c): 48.5 (R37) — PRÄZISIERT durch R68 | 48.5 (R37) | `### 48.5 R37` (Z. 10799) | 1 | nach Zeile 10802: `> Quelle des Grundes: 15.1 (Out-of-Sampl` | `> ⭐ **48.5 R37 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).` |
| 9 | R70 (c): 48.7 (R39) — ERGÄNZT durch R67 | 48.7 (R39) | `### 48.7 R39` (Z. 10813) | 1 | nach Zeile 10816: `> Quelle des Grundes: 23.3, 16.7 (b), 37` | `> ⭐ **48.7 R39 ERGÄNZT durch R67 (53.2)** (Fable 02c R67, TB-132, 04.10.2026).` |
| 10 | R70 (c): 48.7 (R39) — ERGÄNZT durch R69: R39 ist bestätigt | 48.7 (R39) | `### 48.7 R39` (Z. 10813) | 1 | nach Zeile 10816: `> Quelle des Grundes: 23.3, 16.7 (b), 37` | `> ⭐ **48.7 R39 ERGÄNZT durch R69 (53.4): R39 ist bestätigt** (Fable 02c R69, TB-132, 04.10.2026).` |
| 11 | R70 (c): 48.16 (R48 (d)) — ERGÄNZT durch R72, Unterpunkt (c) | 48.16 (R48 (d)) | `### 48.16 R48 — Lesarten` (Z. 10876) | 1 | nach Zeile 10899: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **48.16 R48 (d) ERGÄNZT durch R72 (53.7)** (Fable 02c R72, Unterpunkt (c), TB-132, 04.10.2026).` |
| 12 | R70 (c): 51.5 (R60) — PRÄZISIERT durch R69, Unterpunkt (c) | 51.5 (R60) | `### 51.5 R60` (Z. 11194) | 1 | nach Zeile 11203: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **51.5 R60 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).` |
| 13 | R70 (c): 51.6 (R61) — PRÄZISIERT durch R70, Unterpunkt (a) | 51.6 (R61) | `### 51.6 R61` (Z. 11207) | 1 | nach Zeile 11213: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **51.6 R61 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).` |
| 14 | R70 (c): 52.2 (R64) — ERGÄNZT durch R66 (zu (e)) | 52.2 (R64) | `### 52.2 R64` (Z. 11274) | 1 | nach Zeile 11277: `> Quelle des Grundes: Abschnitt 7, Präzi` | `> ⭐ **52.2 R64 ERGÄNZT durch R66 (53.1)** (Fable 02c R66, zu (e), TB-132, 04.10.2026).` |
| 15 | R70 (c): 52.2 (R64) — PRÄZISIERT durch R68 | 52.2 (R64) | `### 52.2 R64` (Z. 11274) | 1 | nach Zeile 11277: `> Quelle des Grundes: Abschnitt 7, Präzi` | `> ⭐ **52.2 R64 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).` |
| 16 | R70 (c): 52.2 (R64) — PRÄZISIERT durch R69, Unterpunkt (c) | 52.2 (R64) | `### 52.2 R64` (Z. 11274) | 1 | nach Zeile 11277: `> Quelle des Grundes: Abschnitt 7, Präzi` | `> ⭐ **52.2 R64 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).` |
| 17 | R70 (c): 52.2 (R64) — PRÄZISIERT durch R71 (erster Kurstag) | 52.2 (R64) | `### 52.2 R64` (Z. 11274) | 1 | nach Zeile 11277: `> Quelle des Grundes: Abschnitt 7, Präzi` | `> ⭐ **52.2 R64 PRÄZISIERT durch R71 (53.6): erster Kurstag** (Fable 02c R71, TB-132, 04.10.2026).` |
| 18 | R70 (c): 52.2 (R64) — PRÄZISIERT durch R72, Unterpunkt (b) (Benchmark-Tag) | 52.2 (R64) | `### 52.2 R64` (Z. 11274) | 1 | nach Zeile 11277: `> Quelle des Grundes: Abschnitt 7, Präzi` | `> ⭐ **52.2 R64 PRÄZISIERT durch R72 (53.7): Benchmark-Tag** (Fable 02c R72, Unterpunkt (b), TB-132, 04.10.2026).` |
| 19 | R70 (c): 52.3 (R65) — PRÄZISIERT durch R70, Unterpunkt (a) | 52.3 (R65) | `### 52.3 R65` (Z. 11281) | 1 | nach Zeile 11284: `> Quelle des Grundes: 34 (Kopf: die Mark` | `> ⭐ **52.3 R65 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).` |
| 20 | R70 (c): 52.4, Zeile „R64 (52.2), zweite“ — ERGÄNZT durch R66, Unterpunkte (a) und (e) | 52.4, nach der Tabelle | `### 52.4 Voraussetzungen und Befunde` (Z. 11288) | 1 | nach Zeile 11299: `\| R65 (52.3) (c) \| — \| die Messung steht` | `> ⭐ **52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (e), TB-132, 04.10.2026).` |
| 21 | R70 (c): 52.4, Zeile „R64 (52.2) (a)“ — BERICHTIGT durch R69, Unterpunkt (c) | 52.4, nach der Tabelle | `### 52.4 Voraussetzungen und Befunde` (Z. 11288) | 1 | nach Zeile 11299: `\| R65 (52.3) (c) \| — \| die Messung steht` | `> ⭐ **52.4, Zeile „R64 (52.2) (a)“ BERICHTIGT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).` |

### Prüfsumme

*Ausgabe des Trockenlaufs des steuernden Chats am 03.10.2026, 01:13, am echten Repo über die Geräteanbindung (HEAD `0779453`), Aufruf mit `--arbeitsbaum --trockenlauf`. Gelesen wurde ein Auszug dieses Auftrags: der Daten-Block und die Zeile mit dem Platzhalter der Freigabe; mehr liest das Prüfskript vom Auftrag nicht. Die Ausgabe gilt für diese Datei, solange die Freigabe nicht eingesetzt ist. Die Sitzung ruft ohne `--trockenlauf`, und die Freigabe ist dann eingesetzt: Es entfallen die fünf Zeilen „Trockenlauf: …“ (Datum, Freigabe, zweimal „noch nicht gelegt“, Zählungen in `BACKLOG.md`); die erste Zeile lautet `Datum: 04.10.2026 wie verlangt`; in 0a zählt der Arbeitsbaum `2 (Soll 2)` und `16 (Soll 16)`; in 0d fehlen die zwei Arbeitsbaum-Zeilen. Die Zahl `*.py im Baum` ist kein Soll; in 0d zählt sie die zwei Skripte der Sitzung mit. Die zwei Zählungen in `BACKLOG.md` hat der steuernde Chat gesondert am Gerät gemessen (1 und 0). Neubau 04.10.2026: Der Block darunter ist die Ausgabe vom 03.10.2026 für die Fassung mit jenem Datum und bleibt so stehen. Der Trockenlauf der Fassung mit dem Datum 04.10.2026 (steuernder Chat, 04.10.2026, 07:54, am echten Repo über die Geräteanbindung, HEAD `0779453`, Aufruf mit `--arbeitsbaum --trockenlauf`) endete mit rc 0; die fünf Zeilen von `Marken:` bis `Bloecke:` und die Zeile `Dateien:` sind zeichengleich mit dem Block. Anders sind die erste Zeile (`heute 04.10.2026, verlangt 04.10.2026`) und der Arbeitsbaum: Zeiger und Auftrag lagen schon, die zwei Zeilen „noch nicht gelegt“ entfallen, gezählt wurden `2 (Soll 2)` und `16 (Soll 16)`.*

```
Trockenlauf: Datumspruefung uebergangen (heute 03.10.2026, verlangt 03.10.2026)
Trockenlauf: die Freigabe ist noch nicht eingesetzt (Platzhalter steht im Auftrag)
Trockenlauf: noch nicht gelegt (geaendert): docs/auftraege/AKTUELLER_AUFTRAG.md
Arbeitsbaum geaendert: 1 (Soll 2)
Trockenlauf: noch nicht gelegt (unverfolgt): docs/auftraege/MAC_TB-132_register_fable_02c.md
Arbeitsbaum unverfolgt: 15 (Soll 16)
Trockenlauf: Zaehlungen uebergangen: docs/projektfuehrung/BACKLOG.md /^## 6 — Geparkt, null Arbeit/; docs/projektfuehrung/BACKLOG.md /Aus Fable 02b und 02c/
Marken: 21 an 13 Einfuegestellen
je Abschnitt: 15: 2, 23: 3, 27: 1, 48: 5, 51: 2, 52: 8
Anker mit Zahl 1 (Original): 21 von 21
Anker mit Zahl 1 (nach Simulation): 21 von 21
Bloecke: 8 | Ueberschriften: 8 max. Laenge 139 | gekuerzt: 3
Dateien: 15 | Fundstellen: 98 | Zeilenlisten: 3 | Zaehlungen: 28 | *.py im Baum: 679
rc 0: alles wie angegeben
```

### Prüfskript

`pruefe_anhang_tb132.py`, sha256 des Skripttexts mit Zeilenumbruch am Ende: `8ef716acb806896ea5c83ab19d805a567ccca737cd5bdc0ff6e0218149ac911d`. Liest den JSON-Block unten. Aufruf `trading-env/bin/python3 <skript> <dieser Auftrag> <repo-wurzel> [--arbeitsbaum | --probe <ausgabe>]`; rc 0 = alles wie angegeben. Es bricht auch ab, solange der Platzhalter für die Freigabe im Auftrag steht. Der Schalter `--trockenlauf` gehört dem steuernden Chat; die Sitzung benutzt ihn nicht.

```python
#!/usr/bin/env python3
"""Prueft Anhang A von TB-132 gegen das Register am Stand ad351d5, die Quelle 02c und die Fundstellen fuer 53.9
und 53.10; dazu das Datum des Eintrags, auf Wunsch den Arbeitsbaum vor Schritt 0 und die Ausgabe der Probe.

Aufruf (Python 3.9, nur Standardbibliothek; rein lesend):
  python3 pruefe_anhang_tb132.py <MAC_TB-132_register_fable_02c.md> <repo-wurzel> [Schalter]

  ohne Schalter      Datum, Freigabe eingesetzt, Register (sha256, Zeilen), Marken (Anker, Einfuegestellen, Form), Quelle (md5,
                     Schnittregel), Ueberschriften, Simulation des Einsetzens, Dateien (md5), Fundstellen,
                     Zaehlungen. Das ist die Vorpruefung 0d.
  --arbeitsbaum      dazu: uncommittete Dateien genau wie im Daten-Block (0a, VOR dem Commit von Schritt 0).
                     Gemessen mit `git --no-optional-locks diff --name-only HEAD` und
                     `git --no-optional-locks ls-files --others --exclude-standard`.
  --probe <ausgabe>  nur die Ausgabe der Probe r71_probe.py pruefen (0e): Kopfzeile 3 genau wie im Daten-Block
                     (pandas, numpy, Python der Lock-Umgebung), letzte Zeile mit "Rueckgabewert 0", und ab der
                     Zeile, die mit "A - Faelle" beginnt, zeilengleich mit der Vergleichsdatei.
  --trockenlauf      NUR fuer den steuernden Chat vor der Sitzung; der Auftrag benutzt diesen Schalter nicht.
                     Uebergeht (a) die Datumspruefung, (b) Zaehlungen in BACKLOG*.md (Leseregel des Helfers),
                     (c) im Arbeitsbaum die Dateien, die erst mit dem Auftrag gelegt werden (Feld "spaeter"),
                     (d) den Platzhalter fuer die Freigabe, solange sie noch nicht eingesetzt ist.
                     Jede Auslassung wird in der Ausgabe genannt.

rc 0 = alles wie angegeben, rc 1 = Abweichung, rc 2 = Aufruf unbrauchbar.
"""
import datetime
import glob
import hashlib
import json
import re
import subprocess
import sys

argv = sys.argv[1:]
schalter = {"--arbeitsbaum": False, "--trockenlauf": False}
probe = None
rest = []
i = 0
while i < len(argv):
    if argv[i] in schalter:
        schalter[argv[i]] = True
    elif argv[i] == "--probe":
        i += 1
        probe = argv[i] if i < len(argv) else None
        if probe is None:
            print("--probe braucht einen Pfad"); sys.exit(2)
    elif argv[i].startswith("--"):
        print("unbekannter Schalter", argv[i]); sys.exit(2)
    else:
        rest.append(argv[i])
    i += 1
if len(rest) != 2:
    print(__doc__); sys.exit(2)
md, repo = rest[0], rest[1].rstrip("/") + "/"
TROCKEN = schalter["--trockenlauf"]
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
fehler = []
def f(x): fehler.append(x)
def lies(d): return open(repo + d, encoding="utf-8").read()
def ohne_schluss(z): return z[:-1] if z and z[-1] == "" else z      # Zeilen einer Datei, ohne das leere Ende
def ende():
    if fehler:
        print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
    print("rc 0: alles wie angegeben"); sys.exit(0)

# ---------------------------------------------------------------- Probe (0e)
if probe is not None:
    p = daten["probe"]
    ist = ohne_schluss(open(probe, encoding="utf-8").read().split("\n"))
    soll = ohne_schluss(lies(p["vergleich"]).split("\n"))
    def ab(z):
        k = [n for n, s in enumerate(z) if s.startswith(p["ab_zeile"])]
        return z[k[0]:] if len(k) == 1 else None
    if len(ist) < 3 or ist[2] != p["kopfzeile_3"]:
        f("Kopfzeile 3 ist %r, verlangt %r" % (ist[2] if len(ist) > 2 else None, p["kopfzeile_3"]))
    if not (len(ist) > 2 and p["pandas"] in ist[2]): f("pandas-Fassung nicht in der Kopfzeile")
    a_ist, a_soll = ab(ist), ab(soll)
    if a_ist is None or a_soll is None:
        f("die Zeile %r kommt nicht genau einmal vor" % p["ab_zeile"])
    elif a_ist != a_soll:
        ungleich = [n for n, (x, y) in enumerate(zip(a_ist, a_soll)) if x != y]
        f("ab %r nicht zeilengleich: %d gegen %d Zeilen, erste ungleiche Zeile (ab dort gezaehlt) %s"
          % (p["ab_zeile"], len(a_ist), len(a_soll), ungleich[0] + 1 if ungleich else "- (Laenge)"))
    letzte = [s for s in ist if s.strip()][-1] if any(s.strip() for s in ist) else ""
    if not letzte.endswith(p["schluss"]): f("letzte Zeile endet nicht mit %r" % p["schluss"])
    print("Probe:", probe)
    print("Kopfzeile 3:", ist[2] if len(ist) > 2 else None)
    print("Zeilen ab %r: %s (Vergleich %s)" % (p["ab_zeile"], len(a_ist) if a_ist else None, len(a_soll) if a_soll else None))
    print("letzte Zeile:", letzte)
    ende()

# ---------------------------------------------------------------- Datum
heute = datetime.date.today().strftime("%d.%m.%Y")
if TROCKEN:
    print("Trockenlauf: Datumspruefung uebergangen (heute %s, verlangt %s)" % (heute, daten["datum"]))
elif heute != daten["datum"]:
    f("Datum ist %s, der Auftrag gilt nur am %s" % (heute, daten["datum"]))
else:
    print("Datum: %s wie verlangt" % heute)
PLATZHALTER = "⟨⟨" + "FREIGABE" + "⟩⟩"          # zusammengesetzt, damit dieses Skript ihn nicht selbst in den Auftrag traegt
if PLATZHALTER in roh:
    if TROCKEN: print("Trockenlauf: die Freigabe ist noch nicht eingesetzt (Platzhalter steht im Auftrag)")
    else: f("im Auftrag steht noch der Platzhalter fuer die Freigabe des Betreibers")

# ---------------------------------------------------------------- Register, Marken
A = daten["abschnitt"]
reg = lies(daten["register"])
L = reg.split("\n")
if hashlib.sha256(reg.encode()).hexdigest() != daten["register_sha256"]: f("Register-sha256 weicht ab")
if len(reg.splitlines()) != daten["register_zeilen"]: f("Register-Zeilenzahl weicht ab")
a9 = next(i for i, s in enumerate(L, 1) if s.startswith("## 9."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))
ueb = daten["ueberschriften"]
R1, R2 = ueb[0]["R"], ueb[-1]["R"]
if reg.count("## %d." % A) != 0: f("## %d. ist schon vergeben" % A)
if any(s.startswith("> R%d — " % R1) for s in L): f("R%d steht schon im Register" % R1)

FORM = re.compile(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch R(\d+) \(%d\.(\d+)\).*\*\* \(Fable 02c R(\d+)(, .+)?, TB-132, %s\)\.$"
                  % (A, re.escape(daten["datum"])))
M2 = "> Eintrag und Stand oben bleiben zeichengleich."
marken = daten["marken"]
if len(marken) != daten["marken_zahl"]: f("Zahl der Marken ist nicht %d" % daten["marken_zahl"])
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f("Nr %d: Anker %r zaehlt %d" % (m["nr"], m["anker"], n))
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f("Nr %d: Anker beginnt nicht Zeile %d" % (m["nr"], m["ankerzeile"]))
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f("Nr %d: Zeile %d beginnt nicht wie angegeben" % (m["nr"], m["nach"]))
    if not m["nach"] > m["ankerzeile"]: f("Nr %d: Einfuegestelle liegt nicht nach dem Anker" % m["nr"])
    if a9 <= m["nach"] < a11: f("Nr %d: Einfuegestelle in Abschnitt 9 oder 10" % m["nr"])
    if ea <= m["nach"] <= ee: f("Nr %d: Einfuegestelle im ERZEUGT-Block" % m["nr"])
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f("Nr %d: mitten im Zitat" % m["nr"])
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f("Nr %d: mitten in Tabelle" % m["nr"])
    if L[m["nach"]] != "": f("Nr %d: nach der Einfuegestelle steht keine Leerzeile" % m["nr"])
    if any(re.match(r"^#{2,3} ", L[i - 1]) for i in range(m["ankerzeile"] + 1, m["nach"] + 1)) and not m["anker"].startswith("## "):
        f("Nr %d: zwischen Anker und Einfuegestelle steht eine Ueberschrift" % m["nr"])
    mm = FORM.match(m["m1"])
    if not mm: f("Nr %d: Markenzeile 1 nicht in der Form" % m["nr"])
    elif not (int(mm.group(2)) == m["R"] == int(mm.group(4)) and int(mm.group(3)) == m["R"] - R1 + 1):
        f("Nr %d: Blocknummer, Unterabschnitt und Klammer passen nicht zusammen" % m["nr"])
    if m["m2"] != M2: f("Nr %d: Markenzeile 2" % m["nr"])
    if m["m1"] in L: f("Nr %d: die Marke steht schon im Register" % m["nr"])
schl = [(m["nach"], m["R"], m["nr"]) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")
if len(set(m["m1"] for m in marken)) != len(marken): f("eine Markenzeile kommt doppelt vor")

# ---------------------------------------------------------------- Quelle schneiden
q = daten["quelle"]
qroh = open(repo + q["pfad"], "rb").read()
if hashlib.md5(qroh).hexdigest() != q["md5"]: f("Quelle: md5 weicht ab")
if len(qroh) != q["bytes"]: f("Quelle: Bytes weichen ab")
z = qroh.decode("utf-8").split("\n")
bl, cur = {}, None
for i in range(q["von"], q["bis"] + 1):
    s = z[i - 1]
    mm = re.match(r"^R(\d+) — ", s)
    if mm: cur = int(mm.group(1)); bl[cur] = [s]; continue
    if cur is not None:
        bl[cur].append(s)
        if s.startswith("Quelle des Grundes:"): cur = None
    elif s.strip() != "": f("Quelle: Zeile %d steht ausserhalb eines Blocks" % i)
if sorted(bl) != list(range(R1, R2 + 1)): f("Schnitt ergibt nicht R%d-R%d" % (R1, R2))
if any(len(v) != 2 or not v[1].endswith("Kein Ergebnis.") for v in bl.values()): f("ein Block hat nicht zwei Zeilen")
if z[q["von"] - 2] != "```" or z[q["bis"]] != "```": f("Quelle: der Codezaun steht nicht direkt vor und nach den Bloecken")

# Ueberschriften: Bezug = Anfang des Blocks bis zum Satzpunkt nach dem Bezug; am Ende gekuerzt nur mit '…'
for n, u in enumerate(ueb, 1):
    if not u["zeile"].startswith("### %d.%d R%d — " % (A, n, u["R"])): f("%s: Ueberschrift beginnt nicht mit Nummer und Block" % u["xn"])
    kern = u["zeile"].split(" ", 2)[2]                      # "R66 — ..."
    anfang = bl.get(u["R"], [""])[0]
    if kern.endswith("…"):
        if not anfang.startswith(kern[:-1]) or anfang[len(kern) - 1:len(kern)].isalnum() or kern[-2] == " ":
            f("%s: gekuerzte Ueberschrift ist nicht der Blockanfang bis zu einer Wortgrenze" % u["xn"])
    elif not anfang.startswith(kern + "."): f("%s: Ueberschrift ist nicht der Blockanfang" % u["xn"])
    if not u["kette"].startswith("**Kette:** "): f("%s: Kette nicht in der Form" % u["xn"])
    orte = [m["stelle"] for m in marken if m["R"] == u["R"]]
    if u["marken_zahl"] != len(orte): f("%s: Kette nennt %d Marken, Tabelle 2 hat %d" % (u["xn"], u["marken_zahl"], len(orte)))

# ---------------------------------------------------------------- Simulation: Marken einsetzen, Abschnitt anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"], m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
anhang = [daten["kopfzeile"], ""]
for u in ueb:
    anhang += [u["zeile"], ""] + ["> " + s for s in bl.get(u["R"], [])] + ["", u["kette"], ""]
sim = "\n".join(neu[:-1] + [""] + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f("Nr %d: Anker nach Simulation %d" % (m["nr"], n))
zz = [u["zeile"] for u in ueb]
if len(set(zz)) != len(ueb) or any(sim.count(x) != 1 for x in zz): f("Ueberschriften nicht eindeutig")
if any(len(x) > 140 for x in zz): f("Ueberschrift laenger als 140 Zeichen")
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")
if neu.count(M2) != L.count(M2) + len(marken): f("Zahl der Folgezeilen nach Simulation")

# ---------------------------------------------------------------- Dateien, Fundstellen, Zaehlungen
for d, md5, nbytes in daten["dateien"]:
    try:
        b = open(repo + d, "rb").read()
    except OSError:
        f("Datei fehlt: %s" % d); continue
    if hashlib.md5(b).hexdigest() != md5 or len(b) != nbytes: f("Datei %s: md5 oder Bytes weichen ab" % d)
cache = {}
def zeilen(d):
    if d not in cache: cache[d] = lies(d).split("\n")
    return cache[d]
for d, znr, teil in daten["fundstellen"]:
    try:
        zl = zeilen(d)
    except OSError:
        f("Fundstelle %s: Datei fehlt" % d); continue
    if znr > len(zl) or teil not in zl[znr - 1]: f("Fundstelle %s:%d enthaelt nicht %r" % (d, znr, teil))
for d, teil, soll in daten["zeilen_mit"]:
    ist = [n for n, s in enumerate(zeilen(d), 1) if teil in s]
    if ist != soll: f("Zeilen mit %r in %s: %s statt %s" % (teil, d, ist, soll))
uebergangen = []
for d, muster, soll in daten["zaehlungen"]:
    if TROCKEN and "BACKLOG" in d:
        uebergangen.append("%s /%s/" % (d, muster)); continue
    ist = len(re.findall(muster, lies(d), re.M))
    if ist != soll: f("Zaehlung %s /%s/: %d statt %d" % (d, muster, ist, soll))
for gl, muster, summe, dateien in daten["glob_summen"]:
    pf = [p for p in sorted(glob.glob(repo + gl, recursive=True)) if "/ergebnisse/" not in p]
    if len(pf) < dateien: f("Glob %s: %d Dateien, mindestens %d erwartet" % (gl, len(pf), dateien))
    ist = sum(len(re.findall(muster, open(p, encoding="utf-8").read(), re.M)) for p in pf)
    if ist != summe: f("Summe %s /%s/: %d statt %d" % (gl, muster, ist, summe))
for gl, teil, dateien, mit in daten["glob_treffer"]:
    pf = sorted(glob.glob(repo + gl))
    ist = sum(teil in open(p, encoding="utf-8").read() for p in pf)
    if len(pf) != dateien or ist != mit: f("Glob %s: %d Dateien, %d mit %r, statt %d und %d" % (gl, len(pf), ist, teil, dateien, mit))
def git(*a):
    r = subprocess.run(["git", "--no-optional-locks", "-C", repo] + list(a), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0: f("git %s: rc %d" % (" ".join(a), r.returncode))
    return [x for x in r.stdout.split("\n") if x]
py = sorted(set(git("ls-files", "--", "*.py") + git("ls-files", "--others", "--exclude-standard", "--", "*.py")))
py = [p for p in py if "/ergebnisse/" not in "/" + p and not p.startswith("trading-env/")]
for muster, summe, dateien in daten["baum_summen"]:
    treffer = {}
    for p in py:
        try:
            n = len(re.findall(muster, open(repo + p, encoding="utf-8", errors="replace").read(), re.M))
        except OSError:
            continue
        if n: treffer[p] = n
    if sum(treffer.values()) != summe or len(treffer) != dateien:
        f("Baum /%s/: %d Treffer in %d Dateien statt %d in %d: %s" % (muster, sum(treffer.values()), len(treffer), summe, dateien, sorted(treffer)[:5]))

# ---------------------------------------------------------------- Arbeitsbaum (0a)
if schalter["--arbeitsbaum"]:
    ab = daten["arbeitsbaum"]
    kopf = git("rev-parse", "HEAD")
    if not (kopf and kopf[0].startswith(ab["head"])): f("HEAD ist %s, erwartet %s" % (kopf[0][:7] if kopf else None, ab["head"]))
    for name, ist, soll in (("geaendert", git("diff", "--name-only", "HEAD"), ab["geaendert"]),
                            ("unverfolgt", git("ls-files", "--others", "--exclude-standard"), ab["unverfolgt"])):
        fehlt, mehr = sorted(set(soll) - set(ist)), sorted(set(ist) - set(soll))
        if TROCKEN:
            spaeter = [x for x in fehlt if x in ab["spaeter"]]
            fehlt = [x for x in fehlt if x not in ab["spaeter"]]
            if spaeter: print("Trockenlauf: noch nicht gelegt (%s): %s" % (name, ", ".join(spaeter)))
        if fehlt: f("Arbeitsbaum, %s, fehlt: %s" % (name, ", ".join(fehlt)))
        if mehr: f("Arbeitsbaum, %s, nicht erwartet: %s" % (name, ", ".join(mehr)))
        print("Arbeitsbaum %s: %d (Soll %d)" % (name, len(ist), len(soll)))
if uebergangen: print("Trockenlauf: Zaehlungen uebergangen: " + "; ".join(uebergangen))

je = {}
for m in marken:
    kk = next(int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1]))
    je[kk] = je.get(kk, 0) + 1
print("Marken:", len(marken), "an", len({m["nach"] for m in marken}), "Einfuegestellen")
print("je Abschnitt:", ", ".join("%d: %d" % (a, v) for a, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Bloecke:", len(bl), "| Ueberschriften:", len(zz), "max. Laenge", max(len(x) for x in zz), "| gekuerzt:", sum(x.endswith("…") for x in zz))
print("Dateien:", len(daten["dateien"]), "| Fundstellen:", len(daten["fundstellen"]), "| Zeilenlisten:", len(daten["zeilen_mit"]),
      "| Zaehlungen:", len(daten["zaehlungen"]) + len(daten["glob_summen"]) + len(daten["glob_treffer"]) + len(daten["baum_summen"]), "| *.py im Baum:", len(py))
ende()
```

### Einfügeskript

`a4_eintrag.py`, sha256 des Skripttexts mit Zeilenumbruch am Ende: `c75b6e88b9bd5aa9049240737731c3c75774b450398dce2bdb6d7ea026b66216`. Liest Kopf, Schluss und den JSON-Block aus diesem Auftrag und die Blöcke aus der Antwortdatei. Aufruf in A4. Ohne `--vorschau` schreibt es nur am 04.10.2026 und nur, wenn die Ausgabe der Probe aus 0e vorliegt und der Vergleichsdatei gleicht. Der Schalter `--vorschau` gehört dem steuernden Chat (nur mit `--register <Kopie>`); die Sitzung benutzt ihn nicht.

```python
#!/usr/bin/env python3
"""TB-132 A4: Register-Abschnitt 53 anhaengen (R66-R73 zeichengleich, Text des steuernden Chats 53.0, 53.9
und 53.10) und die 21 Marken aus Anhang A am alten Ort setzen. Nur Einfuegungen: keine bestehende Zeile
aendert sich, keine faellt weg.

Bauart docs/belege/TB-130/a4_eintrag.py. Alle Texte werden EINGESETZT, nicht abgetippt:
  - Kopf 53.0 und Schluss 53.9-53.10: die beiden ````-Zaeune im Auftrag nach "Kopf:" bzw. "Schluss:" (A3);
  - Ueberschriften, Ketten, Marken und die Angaben zur Quelle: der Daten-Block (JSON) aus Anhang A;
  - R-Bloecke: die Antwortdatei, Zeilen von..bis, Schnittregel des Auftrags (Beginn 'R<n> — ', Ende
    einschliesslich der ersten Zeile 'Quelle des Grundes:').
Ersetzt wird im Text des steuernden Chats nur ⟨S0⟩ -> `<S0>` (Kurzhash in Backticks). Das Datum des Eintrags
steht fest im Auftrag.

Zwei Wachen vor jedem Lauf ohne --vorschau (echter Lauf und Probelauf an einer Kopie):
  - Datum: Der Rechner zeigt das Datum aus dem Daten-Block (Feld "datum"); an jedem anderen Tag wird nichts
    geschrieben.
  - Probe (Schritt 0e; R71: "weicht sie ab, wird gemeldet, nicht eingetragen"): Die Ausgabe der Probe
    (Daten-Block, probe.ausgabe) ist vorhanden, ihre Zeile 3 lautet genau wie probe.kopfzeile_3, und ab der
    Zeile, die mit "A - Faelle" beginnt, ist sie zeilengleich mit der Vergleichsdatei (probe.vergleich, md5 wie
    im Daten-Block). Sonst wird nichts geschrieben.

Der Auftrag und die Antwortdatei werden als Dateien gelesen. Die Sitzung stellt vorher sicher, dass beide
dem Commit von Schritt 0 gleichen (git diff --quiet <S0> -- <auftrag> <quelle>, rc 0).

Marken: je Marke Leerzeile + zwei Markenzeilen nach der Einfuegestelle (Zeilennummer am Original); mehrere
an derselben Stelle in der Reihenfolge des Daten-Blocks (dort nach R aufsteigend, dann nach Nummer).

Wachen: sha256 und Zeilenzahl des Eingangs; '## 53.' noch nicht vergeben; keine Zeile beginnt mit
'> R66 — '; jeder Anker genau einmal, vorher und nachher; jede alte Zeile in derselben Reihenfolge;
Abschnitt 9 und 10 und der ERZEUGT-Block unveraendert; genau 21 neue Markenzeilen, keine doppelt.

Aufruf aus der Repo-Wurzel (Python 3.9, nur Standardbibliothek):
  Probelauf:  trading-env/bin/python3 docs/belege/TB-132/a4_eintrag.py --s0 <S0> --register <kopie>
  echt:       trading-env/bin/python3 docs/belege/TB-132/a4_eintrag.py --s0 <S0>
  weitere:    --auftrag <pfad>   (Standard docs/auftraege/MAC_TB-132_register_fable_02c.md)
              --wurzel <ordner>  (Standard "."; davor stehen Quelle und, ohne --register, das Register)
              --daten <pfad>     (schreibt die gesetzten Marken mit Zeile nachher als JSON)
              --vorschau         (nur fuer den Soll-Bau des steuernden Chats, der Auftrag benutzt das nicht:
                                  ohne die zwei Wachen Datum und Probe; ohne --s0 bleibt `⟨S0⟩` stehen,
                                  mit --s0 <S0> wird der Kurzhash eingesetzt. Nur zusammen mit
                                  --register <Pfad einer Kopie>: Zeigt der Pfad (nach realpath) auf das
                                  echte Register docs/VORREGISTRIERUNG_neuselektion.md im Repo, wird
                                  verweigert; im Vorschau-Modus wird das Register des Repos nie geschrieben)
Rueckgabewert 0 = geschrieben; jede verletzte Wache bricht mit AssertionError ab, bevor geschrieben wird.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

AUFTRAG = "docs/auftraege/MAC_TB-132_register_fable_02c.md"
M2 = "> Eintrag und Stand oben bleiben zeichengleich."


def zaun(text, ab):
    """Inhalt des ersten ````-Zauns nach der Zeile, die genau `ab` ist."""
    z = text.split("\n")
    assert z.count(ab) == 1, ("Zeile nicht genau einmal", ab, z.count(ab))
    i = z.index(ab)
    a = next(k for k in range(i + 1, len(z)) if z[k] == "````")
    b = next(k for k in range(a + 1, len(z)) if z[k] == "````")
    return "\n".join(z[a + 1:b])


def bloecke(wurzel, q, erster, letzter):
    roh = open(os.path.join(wurzel, q["pfad"]), "rb").read()
    assert hashlib.md5(roh).hexdigest() == q["md5"], "Quelle: md5 weicht ab"
    assert len(roh) == q["bytes"], "Quelle: Bytes weichen ab"
    z = roh.decode("utf-8").split("\n")
    bl, cur = {}, None
    for i in range(q["von"], q["bis"] + 1):
        s = z[i - 1]
        m = re.match(r"^R(\d+) — ", s)
        if m:
            assert cur is None, ("Block ohne Ende", i)
            cur = int(m.group(1))
            assert cur not in bl, ("Dopplung", cur)
            bl[cur] = [s]
            continue
        if cur is not None:
            bl[cur].append(s)
            if s.startswith("Quelle des Grundes:"):
                cur = None
        else:
            assert s.strip() == "", ("Zeile ausserhalb eines Blocks", i, s[:60])
    assert cur is None
    assert sorted(bl) == list(range(erster, letzter + 1)), sorted(bl)
    assert all(len(v) == 2 and v[1].endswith("Kein Ergebnis.") for v in bl.values())
    return bl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auftrag", default=AUFTRAG)
    ap.add_argument("--wurzel", default=".")
    ap.add_argument("--register")
    ap.add_argument("--s0")
    ap.add_argument("--daten")
    ap.add_argument("--vorschau", action="store_true")
    a = ap.parse_args()
    assert a.vorschau or a.s0, "--s0 <7 Hexzeichen> fehlt"
    assert a.s0 is None or re.match(r"^[0-9a-f]{7}$", a.s0), "--s0 <7 Hexzeichen> erwartet"
    s0 = "`%s`" % (a.s0 or "⟨S0⟩")

    auftrag = open(a.auftrag, encoding="utf-8").read()
    daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
    abschnitt = daten["abschnitt"]
    marken = daten["marken"]
    ueber = daten["ueberschriften"]
    erster, letzter = ueber[0]["R"], ueber[-1]["R"]
    assert len(marken) == daten["marken_zahl"] == 21
    assert [m["nr"] for m in marken] == list(range(1, len(marken) + 1))
    assert [u["R"] for u in ueber] == list(range(erster, letzter + 1))
    reg_pfad = a.register or os.path.join(a.wurzel, daten["register"])

    def git(ordner, *arg):
        try:
            r = subprocess.run(["git", "-C", ordner] + list(arg), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        except OSError:
            return 127, ""
        return r.returncode, r.stdout.strip()

    # Vorschau: nur an einer Kopie, nie am Register eines Repos (Pfadvergleich nach realpath)
    if a.vorschau:
        assert a.register, "--vorschau nur zusammen mit --register <Pfad einer Kopie>"
        ziel = os.path.realpath(a.register)
        for echt in (os.path.join(a.wurzel, daten["register"]), daten["register"]):
            assert ziel != os.path.realpath(echt), "--vorschau schreibt nicht in das Register des Repos: " + a.register
        rc, oben = git(os.path.dirname(ziel), "rev-parse", "--show-toplevel")
        if rc == 0 and oben:
            assert os.path.relpath(ziel, os.path.realpath(oben)) != daten["register"], \
                "--vorschau schreibt nicht in das Register eines Repos: " + a.register

    # Wachen Datum und Probe (nicht im Vorschau-Modus)
    if not a.vorschau:
        heute = datetime.date.today().strftime("%d.%m.%Y")
        assert heute == daten["datum"], "Datum ist %s, eingetragen wird nur am %s" % (heute, daten["datum"])
        p = daten["probe"]
        assert os.path.isfile(os.path.join(a.wurzel, p["ausgabe"])), "Probe fehlt (Schritt 0e): " + p["ausgabe"]
        vroh = open(os.path.join(a.wurzel, p["vergleich"]), "rb").read()
        assert [hashlib.md5(vroh).hexdigest()] == [d[1] for d in daten["dateien"] if d[0] == p["vergleich"]], "Vergleichsdatei: md5"

        def ab(pfad):
            z = open(os.path.join(a.wurzel, pfad), encoding="utf-8").read().split("\n")
            k = [n for n, t in enumerate(z) if t.startswith(p["ab_zeile"])]
            assert len(k) == 1, ("Zeile nicht genau einmal", p["ab_zeile"], pfad)
            return z[2] if len(z) > 2 else None, z[k[0]:]
        kopf3, ist = ab(p["ausgabe"])
        assert kopf3 == p["kopfzeile_3"], "Probe: Zeile 3 ist %r, verlangt %r" % (kopf3, p["kopfzeile_3"])
        assert ist == ab(p["vergleich"])[1], "Probe: ab %r nicht zeilengleich mit der Vergleichsdatei" % p["ab_zeile"]

    # Text des steuernden Chats
    kopf = zaun(auftrag, "Kopf:")
    schluss = zaun(auftrag, "Schluss:")
    assert kopf.startswith("## %d. " % abschnitt), kopf[:30]
    assert schluss.startswith("### %d.%d " % (abschnitt, len(ueber) + 1)), schluss[:30]
    assert kopf.count("\n") == 2 and kopf.split("\n")[1] == "", "Kopf: Ueberschrift, Leerzeile, ein Absatz"
    kopf, schluss = kopf.replace("⟨S0⟩", s0), schluss.replace("⟨S0⟩", s0)
    if a.s0:
        for t in (kopf, schluss):
            assert "⟨" not in t and "⟩" not in t, t[t.find("⟨"):][:60]

    # R-Bloecke und Anhang
    bl = bloecke(a.wurzel, daten["quelle"], erster, letzter)
    anhang = [kopf, ""]
    for n, u in enumerate(ueber, 1):
        assert u["zeile"].startswith("### %d.%d R%d — " % (abschnitt, n, u["R"])), u["zeile"][:40]
        kern = u["zeile"].split(" ", 2)[2]
        if kern.endswith("…"):
            assert bl[u["R"]][0].startswith(kern[:-1]), u["R"]
        else:
            assert bl[u["R"]][0].startswith(kern + "."), u["R"]
        assert u["kette"].startswith("**Kette:** ")
        anhang += [u["zeile"], ""] + ["> " + s for s in bl[u["R"]]] + ["", u["kette"], ""]
    anhang = "\n".join(anhang) + "\n" + schluss
    assert "⟦" not in anhang and "⟧" not in anhang

    # Register lesen, Marken einsetzen
    roh = open(reg_pfad, "rb").read()
    assert hashlib.sha256(roh).hexdigest() == daten["register_sha256"], "Register: sha256 weicht ab"
    reg = roh.decode("utf-8")
    assert reg.endswith("\n") and not reg.endswith("\n\n")
    alt = reg[:-1].split("\n")
    assert len(alt) == daten["register_zeilen"], len(alt)
    assert reg.count("## %d." % abschnitt) == 0, "Abschnitt schon vergeben"
    assert not any(s.startswith("> R%d — " % erster) for s in alt), "erster Block schon im Register"
    k9 = next(i for i, s in enumerate(alt) if s.startswith("## 9."))
    k11 = next(i for i, s in enumerate(alt) if s.startswith("## 11."))
    ea = next(i for i, s in enumerate(alt) if s.startswith("<!-- ERZEUGT:"))
    ee = next(i for i, s in enumerate(alt) if s.startswith("<!-- ENDE ERZEUGT -->"))
    je_stelle = {}
    for m in marken:
        assert reg.count(m["anker"]) == 1, ("Anker", m["nr"])
        assert alt[m["ankerzeile"] - 1].startswith(m["anker"]), ("Ankerzeile", m["nr"])
        assert alt[m["nach"] - 1].startswith(m["anfang40"]), ("Einfuegestelle", m["nr"])
        assert m["nach"] > m["ankerzeile"], ("Einfuegestelle vor dem Anker", m["nr"])
        p = m["nach"] - 1                     # 0-basiert: Zeile, NACH der eingefuegt wird
        assert not (k9 <= p < k11), ("Abschnitt 9 oder 10", m["nr"])
        assert not (ea <= p <= ee), ("ERZEUGT-Block", m["nr"])
        assert alt[p + 1] == "", ("keine Leerzeile nach der Einfuegestelle", m["nr"])
        assert m["m2"] == M2 and "⟨" not in m["m1"], ("Markenzeilen", m["nr"])
        je_stelle.setdefault(p, []).append(m)
    for p, v in je_stelle.items():
        assert [(m["R"], m["nr"]) for m in v] == sorted((m["R"], m["nr"]) for m in v), ("Reihenfolge", p + 1)
    assert len(set(m["m1"] for m in marken)) == len(marken), "Markenzeile doppelt"
    for m in marken:
        assert m["m1"] not in alt, ("Marke steht schon im Register", m["nr"])
    neu, gesetzt = [], []
    for i, s in enumerate(alt):
        neu.append(s)
        for m in je_stelle.get(i, []):
            neu.extend(["", m["m1"], m["m2"]])
            gesetzt.append((m, len(neu) - 1))          # 1-basierte Zeile der Markenzeile 1
    text = "\n".join(neu) + "\n\n" + anhang + "\n"

    # Wachen am neuen Text
    nz = text[:-1].split("\n")
    it = iter(nz)
    assert all(any(x == y for y in it) for x in alt), "alte Zeilen nicht in Reihenfolge erhalten"
    n9 = next(i for i, s in enumerate(nz) if s.startswith("## 9."))
    n11 = next(i for i, s in enumerate(nz) if s.startswith("## 11."))
    assert nz[n9:n11] == alt[k9:k11], "Abschnitt 9/10 veraendert"
    nea = next(i for i, s in enumerate(nz) if s.startswith("<!-- ERZEUGT:"))
    nee = next(i for i, s in enumerate(nz) if s.startswith("<!-- ENDE ERZEUGT -->"))
    assert nz[nea:nee + 1] == alt[ea:ee + 1], "ERZEUGT-Block veraendert"
    for m, z in gesetzt:
        assert text.count(m["anker"]) == 1, ("Anker nachher", m["nr"])
        assert nz.count(m["m1"]) == 1 and nz[z - 1] == m["m1"] and nz[z] == M2 and nz[z - 2] == "", m["nr"]
    for u in ueber:
        assert nz.count(u["zeile"]) == 1, u["zeile"]
    assert sum(1 for s in nz if s.startswith("## %d. " % abschnitt)) == 1
    for s in ("## 10. ", "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert text.count(s) == reg.count(s), s
    assert nz.count(M2) == alt.count(M2) + len(marken)
    assert not text.endswith("\n\n")

    open(reg_pfad, "w", encoding="utf-8", newline="\n").write(text)
    if a.daten:
        json.dump({"register": reg_pfad, "S0": s0.strip("`"),
                   "marken": [{"nr": m["nr"], "R": m["R"], "stelle": m["stelle"], "nach_alt": m["nach"],
                               "zeile_neu": z, "m1": m["m1"]} for m, z in gesetzt]},
                  open(a.daten, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Register:", reg_pfad)
    print("Marken gesetzt am alten Ort:", len(gesetzt), "an", len(je_stelle), "Einfuegestellen")
    print("R-Bloecke:", len(bl), "(R%d-R%d)" % (erster, letzter))
    print("Zeilen vorher:", len(alt), " nachher:", len(nz), " eingefuegt:", len(nz) - len(alt))
    print("sha256 nachher:", hashlib.sha256(text.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Daten (maschinenlesbar, massgeblich für Skripte)

```
DATEN-ANFANG
{
 "stand": "ad351d5 (HEAD 0779453)",
 "datum": "04.10.2026",
 "abschnitt": 53,
 "kopfzeile": "## 53. Fable 02c — Registerblock R66–R73 (TB-132)",
 "register": "docs/VORREGISTRIERUNG_neuselektion.md",
 "register_sha256": "a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece",
 "register_zeilen": 11313,
 "quelle": {
  "pfad": "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
  "md5": "6aad30eca53d038b65f24577680f7774",
  "bytes": 30216,
  "von": 134,
  "bis": 156
 },
 "ueberschriften": [
  {
   "xn": "53.1",
   "R": 66,
   "zeile": "### 53.1 R66 — Präzisierung zu Registertext 1a und 1c (15.3 (a), (c)) und Ergänzung zu R64 (e) (52.2) (Kalender der Tagesreihe; Tage des…",
   "kette": "**Kette:** Marken: 15.3 (a); 15.3 (c); 52.2 (R64); 52.4, Zeile „R64 (52.2), zweite“. Indexzeilen ohne Marke (R70 (b)): 17.5; 50.7 Nr. 3. Voraussetzung gemessen: 53.9. Offen: 53.10 Nr. 1, 5 und 7.",
   "marken_zahl": 4
  },
  {
   "xn": "53.2",
   "R": 67,
   "zeile": "### 53.2 R67 — Registertext, Ersteintrag, Ergänzung zu R39 (48.7) (Eindeutigkeit und Vollständigkeit der Reihen)",
   "kette": "**Kette:** Marken: 48.7 (R39). Offen: 53.10 Nr. 5.",
   "marken_zahl": 1
  },
  {
   "xn": "53.3",
   "R": 68,
   "zeile": "### 53.3 R68 — Präzisierung zu R33 (48.1), zu R37 (48.5) und zu R64 (52.2) (Zeile der Bestätigungsperiode in zellen.csv)",
   "kette": "**Kette:** Marken: 48.1 (R33); 48.5 (R37); 52.2 (R64). Tatsache gemessen: 53.9. Offen: 53.10 Nr. 2 und 5.",
   "marken_zahl": 3
  },
  {
   "xn": "53.4",
   "R": 69,
   "zeile": "### 53.4 R69 — Auflösung des Widerspruchs zwischen R39 (48.7) und auswertung.py (Name der Benchmark-Datei); Präzisierung zu R64 (e) (52.2)…",
   "kette": "**Kette:** Marken: 48.7 (R39); 51.5 (R60); 52.2 (R64); 52.4, Zeile „R64 (52.2) (a)“. Tatsache gemessen: 53.9. Offen: 53.10 Nr. 4.",
   "marken_zahl": 4
  },
  {
   "xn": "53.5",
   "R": 70,
   "zeile": "### 53.5 R70 — Marken zu R64 (7 (c)) und zu R66 bis R73; Präzisierung zu R61 (b) (51.6) und R65 (a) (52.3)",
   "kette": "**Kette:** Marken: 51.6 (R61); 52.3 (R65). Nach (c) gesetzt: 20 Marken, je in der Kette des Blocks, der sie auslöst. Indexzeilen ohne Marke nach (b): 7 (c); 17.5; 50.7 Nr. 3. Offen: 53.10 Nr. 8 und 9.",
   "marken_zahl": 2
  },
  {
   "xn": "53.6",
   "R": 71,
   "zeile": "### 53.6 R71 — Berichtigung der Tatsachennotiz zu 3b (c), Satz zur Zeitachse, in 23.3 (welcher Tag ausgelassen wird)",
   "kette": "**Kette:** Marken: 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; 52.2 (R64). Voraussetzung gemessen: 53.9.",
   "marken_zahl": 2
  },
  {
   "xn": "53.7",
   "R": 72,
   "zeile": "### 53.7 R72 — Tatsachennotiz zu Registertext 3b (c) (23.3) (Kurslücke und Reihenende im Benchmark) und Ergänzung zu R48 (d) (48.16)…",
   "kette": "**Kette:** Marken: 23.3, Registertext 3b (c) (vom steuernden Chat bestimmt, 53.10 Nr. 8); 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse; 48.16 (R48); 52.2 (R64). Voraussetzung gemessen: 53.9. Offen: 53.10 Nr. 3, 5, 6 und 10.",
   "marken_zahl": 4
  },
  {
   "xn": "53.8",
   "R": 73,
   "zeile": "### 53.8 R73 — Tatsachennotiz zu 27 nach R56 (c) (die Antwort 02c stammt aus dem Chat der Antwort 02b)",
   "kette": "**Kette:** Marken: Abschnitt 27. Keine Voraussetzung (53.9).",
   "marken_zahl": 1
  }
 ],
 "marken_zahl": 21,
 "marken": [
  {
   "nr": 1,
   "R": 66,
   "ziel": "R70 (c): 15.3 (a) — PRÄZISIERT durch R66, Unterpunkte (a) und (b)",
   "stelle": "15.3 (a)",
   "anker": "### 15.3 Registertext 1",
   "ankerzeile": 1428,
   "nach": 1447,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **15.3 (a) PRÄZISIERT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (b), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 2,
   "R": 66,
   "ziel": "R70 (c): 15.3 (c) — PRÄZISIERT durch R66, Unterpunkt (c)",
   "stelle": "15.3 (c)",
   "anker": "### 15.3 Registertext 1",
   "ankerzeile": 1428,
   "nach": 1447,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **15.3 (c) PRÄZISIERT durch R66 (53.1)** (Fable 02c R66, Unterpunkt (c), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 3,
   "R": 72,
   "ziel": "R65 (a), angewandt vom steuernden Chat: R72 (b) „Benchmark-Tag des Bots im Sinn von 23.3“; R70 (c) nennt den Ort nicht",
   "stelle": "23.3, Registertext 3b (c)",
   "anker": "> **Registertext 3b (c), Fassung 20.09.2026",
   "ankerzeile": 3928,
   "nach": 3939,
   "anfang40": "> an jedem Tag in derselben Menge.",
   "m1": "> ⭐ **23.3, Registertext 3b (c) PRÄZISIERT durch R72 (53.7)** (Fable 02c R72, Unterpunkt (b), vom steuernden Chat nach R65 (a) bestimmt, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 4,
   "R": 71,
   "ziel": "R70 (c): 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — BERICHTIGT durch R71",
   "stelle": "23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse",
   "anker": "**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**",
   "ankerzeile": 3957,
   "nach": 3964,
   "anfang40": "> Tag eine Berichtigung des Codes an den",
   "m1": "> ⭐ **23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse BERICHTIGT durch R71 (53.6)** (Fable 02c R71, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 5,
   "R": 72,
   "ziel": "R70 (c): 23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse — ERGÄNZT durch R72",
   "stelle": "23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse",
   "anker": "**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**",
   "ankerzeile": 3957,
   "nach": 3964,
   "anfang40": "> Tag eine Berichtigung des Codes an den",
   "m1": "> ⭐ **23.3, Tatsachennotiz zu 3b (c), Satz zur Zeitachse ERGÄNZT durch R72 (53.7)** (Fable 02c R72, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 6,
   "R": 73,
   "ziel": "R70 (c): 27 — ERGÄNZT durch R73",
   "stelle": "Abschnitt 27",
   "anker": "## 27. Sichtschutz",
   "ankerzeile": 5124,
   "nach": 5197,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **Abschnitt 27 ERGÄNZT durch R73 (53.8)** (Fable 02c R73, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 7,
   "R": 68,
   "ziel": "R70 (c): 48.1 (R33) — PRÄZISIERT durch R68",
   "stelle": "48.1 (R33)",
   "anker": "### 48.1 R33",
   "ankerzeile": 10771,
   "nach": 10774,
   "anfang40": "> Quelle des Grundes: Datenvertrag von a",
   "m1": "> ⭐ **48.1 R33 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 8,
   "R": 68,
   "ziel": "R70 (c): 48.5 (R37) — PRÄZISIERT durch R68",
   "stelle": "48.5 (R37)",
   "anker": "### 48.5 R37",
   "ankerzeile": 10799,
   "nach": 10802,
   "anfang40": "> Quelle des Grundes: 15.1 (Out-of-Sampl",
   "m1": "> ⭐ **48.5 R37 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 9,
   "R": 67,
   "ziel": "R70 (c): 48.7 (R39) — ERGÄNZT durch R67",
   "stelle": "48.7 (R39)",
   "anker": "### 48.7 R39",
   "ankerzeile": 10813,
   "nach": 10816,
   "anfang40": "> Quelle des Grundes: 23.3, 16.7 (b), 37",
   "m1": "> ⭐ **48.7 R39 ERGÄNZT durch R67 (53.2)** (Fable 02c R67, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 10,
   "R": 69,
   "ziel": "R70 (c): 48.7 (R39) — ERGÄNZT durch R69: R39 ist bestätigt",
   "stelle": "48.7 (R39)",
   "anker": "### 48.7 R39",
   "ankerzeile": 10813,
   "nach": 10816,
   "anfang40": "> Quelle des Grundes: 23.3, 16.7 (b), 37",
   "m1": "> ⭐ **48.7 R39 ERGÄNZT durch R69 (53.4): R39 ist bestätigt** (Fable 02c R69, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 11,
   "R": 72,
   "ziel": "R70 (c): 48.16 (R48 (d)) — ERGÄNZT durch R72, Unterpunkt (c)",
   "stelle": "48.16 (R48 (d))",
   "anker": "### 48.16 R48 — Lesarten",
   "ankerzeile": 10876,
   "nach": 10899,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **48.16 R48 (d) ERGÄNZT durch R72 (53.7)** (Fable 02c R72, Unterpunkt (c), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 12,
   "R": 69,
   "ziel": "R70 (c): 51.5 (R60) — PRÄZISIERT durch R69, Unterpunkt (c)",
   "stelle": "51.5 (R60)",
   "anker": "### 51.5 R60",
   "ankerzeile": 11194,
   "nach": 11203,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **51.5 R60 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 13,
   "R": 70,
   "ziel": "R70 (c): 51.6 (R61) — PRÄZISIERT durch R70, Unterpunkt (a)",
   "stelle": "51.6 (R61)",
   "anker": "### 51.6 R61",
   "ankerzeile": 11207,
   "nach": 11213,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **51.6 R61 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 14,
   "R": 66,
   "ziel": "R70 (c): 52.2 (R64) — ERGÄNZT durch R66 (zu (e))",
   "stelle": "52.2 (R64)",
   "anker": "### 52.2 R64",
   "ankerzeile": 11274,
   "nach": 11277,
   "anfang40": "> Quelle des Grundes: Abschnitt 7, Präzi",
   "m1": "> ⭐ **52.2 R64 ERGÄNZT durch R66 (53.1)** (Fable 02c R66, zu (e), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 15,
   "R": 68,
   "ziel": "R70 (c): 52.2 (R64) — PRÄZISIERT durch R68",
   "stelle": "52.2 (R64)",
   "anker": "### 52.2 R64",
   "ankerzeile": 11274,
   "nach": 11277,
   "anfang40": "> Quelle des Grundes: Abschnitt 7, Präzi",
   "m1": "> ⭐ **52.2 R64 PRÄZISIERT durch R68 (53.3)** (Fable 02c R68, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 16,
   "R": 69,
   "ziel": "R70 (c): 52.2 (R64) — PRÄZISIERT durch R69, Unterpunkt (c)",
   "stelle": "52.2 (R64)",
   "anker": "### 52.2 R64",
   "ankerzeile": 11274,
   "nach": 11277,
   "anfang40": "> Quelle des Grundes: Abschnitt 7, Präzi",
   "m1": "> ⭐ **52.2 R64 PRÄZISIERT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 17,
   "R": 71,
   "ziel": "R70 (c): 52.2 (R64) — PRÄZISIERT durch R71 (erster Kurstag)",
   "stelle": "52.2 (R64)",
   "anker": "### 52.2 R64",
   "ankerzeile": 11274,
   "nach": 11277,
   "anfang40": "> Quelle des Grundes: Abschnitt 7, Präzi",
   "m1": "> ⭐ **52.2 R64 PRÄZISIERT durch R71 (53.6): erster Kurstag** (Fable 02c R71, TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 18,
   "R": 72,
   "ziel": "R70 (c): 52.2 (R64) — PRÄZISIERT durch R72, Unterpunkt (b) (Benchmark-Tag)",
   "stelle": "52.2 (R64)",
   "anker": "### 52.2 R64",
   "ankerzeile": 11274,
   "nach": 11277,
   "anfang40": "> Quelle des Grundes: Abschnitt 7, Präzi",
   "m1": "> ⭐ **52.2 R64 PRÄZISIERT durch R72 (53.7): Benchmark-Tag** (Fable 02c R72, Unterpunkt (b), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 19,
   "R": 70,
   "ziel": "R70 (c): 52.3 (R65) — PRÄZISIERT durch R70, Unterpunkt (a)",
   "stelle": "52.3 (R65)",
   "anker": "### 52.3 R65",
   "ankerzeile": 11281,
   "nach": 11284,
   "anfang40": "> Quelle des Grundes: 34 (Kopf: die Mark",
   "m1": "> ⭐ **52.3 R65 PRÄZISIERT durch R70 (53.5)** (Fable 02c R70, Unterpunkt (a), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 20,
   "R": 66,
   "ziel": "R70 (c): 52.4, Zeile „R64 (52.2), zweite“ — ERGÄNZT durch R66, Unterpunkte (a) und (e)",
   "stelle": "52.4, nach der Tabelle",
   "anker": "### 52.4 Voraussetzungen und Befunde",
   "ankerzeile": 11288,
   "nach": 11299,
   "anfang40": "| R65 (52.3) (c) | — | die Messung steht",
   "m1": "> ⭐ **52.4, Zeile „R64 (52.2), zweite“ ERGÄNZT durch R66 (53.1)** (Fable 02c R66, Unterpunkte (a) und (e), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 21,
   "R": 69,
   "ziel": "R70 (c): 52.4, Zeile „R64 (52.2) (a)“ — BERICHTIGT durch R69, Unterpunkt (c)",
   "stelle": "52.4, nach der Tabelle",
   "anker": "### 52.4 Voraussetzungen und Befunde",
   "ankerzeile": 11288,
   "nach": 11299,
   "anfang40": "| R65 (52.3) (c) | — | die Messung steht",
   "m1": "> ⭐ **52.4, Zeile „R64 (52.2) (a)“ BERICHTIGT durch R69 (53.4)** (Fable 02c R69, Unterpunkt (c), TB-132, 04.10.2026).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  }
 ],
 "dateien": [
  [
   "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md",
   "9bf6249ab23e6cd33ea055ab2bd203ec",
   14621
  ],
  [
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02b_eroeffnung.md",
   "a29bcf4117676c7c1261a50080f570ee",
   5002
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md",
   "33c4e962f2c93b7ef70c2fd13107891b",
   23904
  ],
  [
   "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02c_messung_vor_eintrag_r66_r71.md",
   "eb9dfec77365cc2019b49e39f22ebd9f",
   22485
  ],
  [
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md",
   "0cac4323dfc26ac08181e56cfbb58ad2",
   5691
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
   "6aad30eca53d038b65f24577680f7774",
   30216
  ],
  [
   "docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt",
   "adecffe00ffafd7735fbf644ec3d9734",
   3713
  ],
  [
   "docs/belege/TB-132/vormessung/ausgabe_pandas_3.0.5.txt",
   "f33b9b64b684871ef0d41ae7beb2767e",
   3438
  ],
  [
   "docs/belege/TB-132/vormessung/p3_probe.py",
   "ef7a8623c2a8a465677db3a07f769878",
   6749
  ],
  [
   "docs/belege/TB-132/vormessung/r71_probe.py",
   "4398f6faafff22b786ff1c92554c9f64",
   19626
  ],
  [
   "docs/belege/TB-132/vormessung/v1_register.md",
   "b78d2f4729f86484309a0c07ab9e9234",
   29706
  ],
  [
   "docs/belege/TB-132/vormessung/v2_code.md",
   "c831581cc3b01ca114b8acaf8d387711",
   19549
  ],
  [
   "docs/belege/TB-132/vormessung/v3_daten.md",
   "898fe263ceee1f80ce1e9e2d3c94623a",
   9337
  ],
  [
   "docs/belege/TB-132/vormessung/v4_register_02c.md",
   "b75d78c7224da222e8fd398d65880617",
   31802
  ],
  [
   "docs/belege/TB-132/vormessung/v5_code_02c.md",
   "678a64e6c8d82a391043278c06855264",
   24327
  ]
 ],
 "fundstellen": [
  [
   "notifications/boersenkalender.py",
   70,
   "KALENDER_NAME = \"NYSE\""
  ],
  [
   "notifications/boersenkalender.py",
   81,
   "import pandas_market_calendars as mcal"
  ],
  [
   "notifications/boersenkalender.py",
   109,
   "_KALENDER = mcal.get_calendar(KALENDER_NAME)"
  ],
  [
   "shared/entscheidungskerze.py",
   384,
   "import boersenkalender"
  ],
  [
   "shared/paths.py",
   239,
   "ARBEITSBAUM_PFADE = ("
  ],
  [
   "shared/paths.py",
   240,
   "\"shared\", \"strategies\", LOCK,"
  ],
  [
   "shared/paths.py",
   253,
   ")"
  ],
  [
   "research/snapshotgrenze/erhebung_eingaben.py",
   606,
   "return {"
  ],
  [
   "research/snapshotgrenze/erhebung_eingaben.py",
   609,
   "\"paket_vorhanden\": _paketfassung(\"pandas_market_calendars\"),"
  ],
  [
   "research/snapshotgrenze/erhebung_eingaben.py",
   610,
   "}"
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   95,
   "def sharpe(renditen, perioden_je_jahr: int) -> float:"
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   103,
   "if r.size < 2:"
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   105,
   "s = float(np.std(r, ddof=1))"
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   106,
   "if s == 0.0 or not np.isfinite(s):"
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   108,
   "return float(np.mean(r)) / s * math.sqrt(perioden_je_jahr)"
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   219,
   "def deflated_sharpe("
  ],
  [
   "research/vorregistrierung/kennzahlen.py",
   246,
   "\"bestimmt\": True}"
  ],
  [
   "research/vorregistrierung/registerdaten.py",
   109,
   "HANDELSTAGE_JE_JAHR = 252"
  ],
  [
   "research/vorregistrierung/beispieldaten.py",
   144,
   "sharpe_fn=standard_sharpe"
  ],
  [
   "research/vorregistrierung/beispieldaten.py",
   180,
   "sharpe_fn(werte, idx"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   264,
   "def perioden_je_jahr(bot: str) -> int:"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   265,
   "else 365)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   353,
   "df[\"netto_sharpe\"] = np.where("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   354,
   "df[\"netto_sharpe\"].to_numpy(dtype=float))"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   395,
   "[\"netto_sharpe\"].median()"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   577,
   "values=\"netto_sharpe\""
  ],
  [
   "research/vorregistrierung/auswertung.py",
   622,
   "\"netto_sharpe\": (0.0 if int(z[\"n_trades\"]) == 0"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   623,
   "else float(z[\"netto_sharpe\"])),"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   684,
   "\"falten_sharpe\": {r[\"falte\"]: float(r[\"netto_sharpe\"])"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   587,
   "\"sharpe_varianz_ueber_die_zellen\": float(np.var("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   588,
   "statistik.to_numpy(dtype=float), ddof=1))"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   670,
   "dsr = dsr_drei_werte(bereinigung[\"renditen\"], buch)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   490,
   "def beta_bereinigung("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   511,
   "return any((d >= a) & (d < b) for a, b in fenster)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   517,
   "gemeinsam = s.index.intersection(b.index)"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   398,
   "def zulaessigkeit("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   403,
   "df[df[\"falte\"].isin(selektionsfalten)]"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   405,
   "e = float(z[\"mittlere_exposure\"])"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   608,
   "def bestaetigungsperiode("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   626,
   "\"mittlere_exposure\": float(z[\"mittlere_exposure\"]),"
  ],
  [
   "research/vorregistrierung/auswertung.py",
   728,
   "\"bestaetigungsperiode\": bestaetigungsperiode("
  ],
  [
   "research/vorregistrierung/auswertung.py",
   379,
   "f\"{markt}.csv\")"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   135,
   "def tagesraster("
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   148,
   "return tage"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   166,
   "eigene = r.reindex(tage)"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   167,
   "spalten[symbol] = eigene.ffill()"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   168,
   "fort[symbol] = eigene.isna() & spalten[symbol].notna()"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   244,
   "unreal[a:b + 1] +="
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   245,
   "n_offen[a:b + 1] += 1"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   246,
   "gebunden[a:b + 1] += allokation[i]"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   247,
   "fort_zaehler[a:b + 1] += fort_np[s][a:b + 1].astype(int)"
  ],
  [
   "research/mtm_drawdown/mtm_kern.py",
   255,
   "\"fortgeschrieben\": fort_zaehler,"
  ],
  [
   "research/exposure_messung/auswertung.py",
   305,
   "def mtm_reihen("
  ],
  [
   "research/exposure_messung/auswertung.py",
   321,
   "if reihe is None:"
  ],
  [
   "research/exposure_messung/auswertung.py",
   322,
   "continue"
  ],
  [
   "research/exposure_messung/auswertung.py",
   323,
   ".ffill().reindex(tage).ffill().bfill()"
  ],
  [
   "research/exposure_messung/auswertung.py",
   341,
   "return pd.Series(frei + wert, index=tage), naht"
  ],
  [
   "research/vorregistrierung/benchmark.py",
   155,
   "df = pd.read_csv(pfad, parse_dates=[\"open_time\"])"
  ],
  [
   "research/vorregistrierung/benchmark.py",
   159,
   "reihen[s] = pd.Series(df[\"close\"].to_numpy(dtype=float),"
  ],
  [
   "research/vorregistrierung/benchmark.py",
   160,
   "index=pd.DatetimeIndex(df[\"open_time\"]))"
  ],
  [
   "research/vorregistrierung/benchmark.py",
   205,
   "return rahmen.pct_change().mean(axis=1, skipna=True).dropna()"
  ],
  [
   "requirements.lock",
   50,
   "numpy==2.0.2"
  ],
  [
   "requirements.lock",
   51,
   "pandas-market-calendars==4.6.1"
  ],
  [
   "requirements.lock",
   52,
   "pandas==2.3.3"
  ],
  [
   "trading-env/pyvenv.cfg",
   3,
   "version = 3.9.6"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1442,
   "Ist die Standardabweichung 0 (kein Trade in der Falte), ist der"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1443,
   "Falten-Sharpe 0."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1449,
   "*Formel für den Falten-Sharpe: Mittel / Standardabweichung der täglichen"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   1450,
   "Netto-Renditen der Falte × √252 (Krypto: √365 auf Kalendertagen).*"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   2847,
   "gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   3908,
   "Unter VH erzeugt Rang 3 Alpha aus Nichtteilnahme."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   3933,
   "Der Benchmark einer Falte ist an genau"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   3936,
   "er wird nicht mit Rendite 0 geführt, sondern gar nicht."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   3957,
   "**Tatsachennotiz zu 3b (c), Satz zur Zeitachse (TB-71, 20.09.2026):**"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   3959,
   "> Die Umsetzung lässt den ersten Kurstag je Falte aus, weil `pct_change` dort"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   4009,
   "**Wirkung 1 — die Falte, um die es ging**"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   4014,
   "(kein Symbol erreicht 730 Tage vor 2019-08-17; Register 21.3 (b), 21.4)."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   4471,
   "fortgeschriebene Kurstage"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   5972,
   "| `elliott_wave` | krypto |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   5973,
   "| `t3_supertrend` | krypto |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   5975,
   "| `turtle_soup_crypto` | krypto |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   5976,
   "| `volatility_breakout_crypto` | krypto |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10857,
   "Beauftragte Änderung nach 37.3 mit Nachweis in der Bauart von 10.1"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11150,
   "Nebenbefund DSR-Einheiten"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11168,
   "(c) Ein eigener Block nach der Bauart von R32 bleibt nötig"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11196,
   "auswertung.py wird dafür nicht geöffnet."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11209,
   "R54 an 7 (c)"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11297,
   "| R64 (52.2), zweite |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11298,
   "| R64 (52.2) (a) |"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
   133,
   "```"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
   134,
   "R66 — Präzisierung zu Registertext 1a und 1c (15.3 (a), (c))"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
   156,
   "Quelle des Grundes: R56 (a) bis (c), 27.4, Leseprotokolle 02b und 02c. Kein Ergebnis."
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
   157,
   "```"
  ],
  [
   "docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt",
   3,
   "  pandas 2.3.3, "
  ],
  [
   "docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt",
   6,
   "A - Faelle, die die Aussage pruefen (bestimmen den Rueckgabewert)"
  ],
  [
   "docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt",
   25,
   "ERGEBNIS: Aussage bestaetigt unter pandas 2.3.3 -> Rueckgabewert 0"
  ],
  [
   "docs/belege/TB-132/vormessung/ausgabe_pandas_3.0.5.txt",
   3,
   "  pandas 3.0.5, "
  ],
  [
   "docs/belege/TB-132/vormessung/v4_register_02c.md",
   151,
   "**Nicht glatt (S):** Nr. 9, 32, 56, 57, 59, 67, 79, 89, 92, 96. **N:** keine."
  ]
 ],
 "zeilen_mit": [
  [
   "research/vorregistrierung/auswertung.py",
   "kapital_drawdown_pct",
   [
    40,
    134,
    413,
    414,
    625,
    681,
    682,
    824
   ]
  ],
  [
   "research/vorregistrierung/auswertung.py",
   "mittlere_exposure",
   [
    41,
    134,
    405,
    537,
    626
   ]
  ],
  [
   "research/vorregistrierung/auswertung.py",
   "netto_sharpe",
   [
    40,
    133,
    353,
    354,
    355,
    356,
    395,
    577,
    622,
    623,
    674,
    684,
    801,
    822
   ]
  ]
 ],
 "zaehlungen": [
  [
   "research/vorregistrierung/auswertung.py",
   "(?i)zellenbericht",
   0
  ],
  [
   "research/vorregistrierung/auswertung.py",
   "kapital_drawdown_mtm_pct",
   0
  ],
  [
   "research/vorregistrierung/auswertung.py",
   "bestaetigung_ab_effektiv",
   0
  ],
  [
   "docs/belege/TB-112/a2_laufbereich.txt",
   "^(?!#).+$",
   84
  ],
  [
   "docs/belege/TB-112/a2_laufbereich.txt",
   "^docs/belege/",
   3
  ],
  [
   "docs/belege/TB-112/a2_laufbereich.txt",
   "entscheidungskerze",
   0
  ],
  [
   "docs/belege/TB-112/a2_laufbereich.txt",
   "boersenkalender",
   0
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "^## 6 — Geparkt, null Arbeit",
   1
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "Aus Fable 02b und 02c",
   0
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 02a \\|",
   1
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 02b \\|",
   0
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 02c \\|",
   0
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "^## 7\\. Die Marken aus Fable 02a \\(TB-130\\)",
   1
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "^## 8\\. ",
   0
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "Indexzeilen aus Fable 02c",
   0
  ],
  [
   "docs/projektfuehrung/JOURNAL.md",
   "^## EC — TB-131",
   1
  ],
  [
   "docs/projektfuehrung/JOURNAL.md",
   "^## ED ",
   0
  ],
  [
   "docs/projektfuehrung/JOURNAL.md",
   "^## Wiederkehrende Lehren",
   1
  ]
 ],
 "glob_summen": [
  [
   "research/vorregistrierung/**/*.py",
   "kz\\.sharpe\\(|kennzahlen\\.sharpe\\(|[^_a-zA-Z.]sharpe\\(",
   1,
   5
  ],
  [
   "shared/**/*.py",
   "kz\\.sharpe\\(|kennzahlen\\.sharpe\\(|[^_a-zA-Z.]sharpe\\(",
   0,
   1
  ],
  [
   "strategies/**/*.py",
   "kz\\.sharpe\\(|kennzahlen\\.sharpe\\(|[^_a-zA-Z.]sharpe\\(",
   0,
   2
  ],
  [
   "docs/belege/**/*.py",
   "kz\\.sharpe\\(|kennzahlen\\.sharpe\\(|[^_a-zA-Z.]sharpe\\(",
   0,
   1
  ],
  [
   "research/vorregistrierung/*.py",
   "(?i)bootstrap",
   0,
   5
  ],
  [
   "research/vorregistrierung/*.py",
   "sharpe_fn=(kz\\.|kennzahlen\\.)?sharpe\\b",
   0,
   5
  ]
 ],
 "glob_treffer": [
  [
   "strategies/*/forward_test.py",
   "entscheidungskerze",
   9,
   9
  ]
 ],
 "baum_summen": [
  [
   "import pandas_market_calendars|import exchange_calendars|get_calendar\\(",
   2,
   1
  ],
  [
   "kapital_drawdown_mtm_pct",
   0,
   0
  ],
  [
   "bestaetigung_ab_effektiv",
   0,
   0
  ]
 ],
 "arbeitsbaum": {
  "head": "0779453",
  "geaendert": [
   "docs/auftraege/AKTUELLER_AUFTRAG.md",
   "docs/projektfuehrung/UEBERGABE.md"
  ],
  "unverfolgt": [
   "docs/auftraege/MAC_TB-132_register_fable_02c.md",
   "docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt",
   "docs/belege/TB-132/vormessung/ausgabe_pandas_3.0.5.txt",
   "docs/belege/TB-132/vormessung/p3_probe.py",
   "docs/belege/TB-132/vormessung/r71_probe.py",
   "docs/belege/TB-132/vormessung/v1_register.md",
   "docs/belege/TB-132/vormessung/v2_code.md",
   "docs/belege/TB-132/vormessung/v3_daten.md",
   "docs/belege/TB-132/vormessung/v4_register_02c.md",
   "docs/belege/TB-132/vormessung/v5_code_02c.md",
   "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md",
   "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-02c_messung_vor_eintrag_r66_r71.md",
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02b_zeitachse_vertrag_benchmarkdatei.md",
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-02c_kalender_dsr_embargo_lueckentag.md",
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02b_eroeffnung.md",
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-02c_eroeffnung.md"
  ],
  "spaeter": [
   "docs/auftraege/MAC_TB-132_register_fable_02c.md",
   "docs/auftraege/AKTUELLER_AUFTRAG.md"
  ]
 },
 "probe": {
  "skript": "docs/belege/TB-132/vormessung/r71_probe.py",
  "ausgabe": "docs/belege/TB-132/probe_lock_r71.txt",
  "vergleich": "docs/belege/TB-132/vormessung/ausgabe_pandas_2.3.3.txt",
  "ab_zeile": "A - Faelle",
  "kopfzeile_3": "  pandas 2.3.3, numpy 2.0.2, Python 3.9.6",
  "pandas": "pandas 2.3.3",
  "schluss": "Rueckgabewert 0"
 }
}
DATEN-ENDE
```
