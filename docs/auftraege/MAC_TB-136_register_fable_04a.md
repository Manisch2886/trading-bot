# TB-136 Register — Fable 04a (R74–R77) als Abschnitt 54, 15 Marken am alten Ort; Nachmessung der Voraussetzungen; Registerkopie, Index und Dialog-Index — an: Mac-Sitzung (Claude Code)

**Sitzungstitel:** `TB-136` · **Modell:** Opus 5.5, Aufwand hoch (Registerauftrag, wie TB-132) · **Repo:** `Manisch2886/trading-bot`, Base `main`, frisch von `main` am HEAD `d781f1b` · **Angelegt:** 04.10.2026 vom steuernden Chat
**Vorgänger:** TB-132 (`d781f1b`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-136_register_fable_04a.md`, er wird in Schritt 0 mitcommittet. **Interpreter**, **Rückfragen an den Betreiber** und Abbruch: wie TB-132 (Kopf): immer `trading-env/bin/python3` (7c); Rückfragen stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Datum des Eintrags: zur Laufzeit, nicht fest.** Kopf von 54, Marken und Daten-Block tragen den Platzhalter `⟨DATUM⟩`. Die Sitzung setzt das Datum des Tages ein, an dem Schritt A läuft: Sie misst es einmal zu Beginn von A4 mit `TZ=Europe/Berlin date +%d.%m.%Y`, hält es in `docs/belege/TB-136/a4_datum.txt` fest und gibt diesen einen Wert dem Probelauf, dem echten Lauf und den Nachweisen. Prüfskript und Einfügeskript nehmen ihn mit `--datum TT.MM.JJJJ`, so wie `--s0` den Kurzhash; sie prüfen die Form, keine Uhr. Die drei Datumsprüfungen aus TB-132 (0a.1, im Prüfskript, als Wache im Einfügeskript) gibt es nicht mehr; an keinem Tag bricht die Sitzung wegen des Datums ab. In 0a und 0d bekommt das Prüfskript das Datum des Aufrufs; es prüft damit nur die Form der Markenzeilen. Sollwerte, die am Datum und an ⟨S0⟩ hängen (sha256 und md5 des Registers nachher), stehen nicht im Auftrag: Die Sitzung rechnet sie im Probelauf an einer Kopie und vergleicht nach dem Einfügen (`cmp` gleich). Zeilenzahlen und numstat hängen an keinem von beiden und stehen fest.
**Start:** wie TB-132 (Kopf): über den Sitzungswächter; den Einfügesatz schickt der Betreiber ab. Die Sitzung läuft lokal auf dem Betriebsrechner im Hauptordner `~/trading-bot`, nicht in einem Worktree und nicht in der Cloud; läuft sie woanders, steht TB-136 nicht im Zeiger oder der Arbeitsbaum weicht in 0a ab, und sie hört ohne Commit auf.
**Prüfwerkzeuge:** Jedes Skript dieser Sitzung liegt unter `docs/belege/TB-136/` und wird mitcommittet, auch Vergleichsskripte.
**Bauart: TB-132.** Der Auftrag `docs/auftraege/MAC_TB-132_register_fable_02c.md` und die Skripte unter `docs/belege/TB-132/` sind die Vorlage; sie werden übernommen und angepasst, nicht neu erfunden. Wo dieser Auftrag „wie TB-132“ sagt, gilt der dortige Schritt mit den hier genannten Werten. Wo beide sich widersprechen, gilt dieser Auftrag. Verweist TB-132 an der Stelle weiter auf TB-130 und TB-129, gilt der Schritt von dort mit den Werten dieses Auftrags; solche Stellen nennen hier die ganze Kette. Welche festen Stellen der übernommenen Skripte umzustellen sind, steht in der Tabelle „Übernommene Skripte“ nach Schritt D. **Anders als TB-132:** das Datum zur Laufzeit; keine Probe in der Lock-Umgebung (0e Probe, der Schalter `--probe`, der Schlüssel `probe`, die Probe-Wache und die Rubrik „Probe“ im Ergebnis entfallen); an der Stelle von 0e steht die Nachmessung der Voraussetzungen, und das Einfügeskript trägt dafür eine Wache zur Voraussetzung aus R74 (b). **Massgeblich für Überschriften, Ketten, Marken und Fundstellen ist Anhang A** (Daten-Block), gebaut am 04.10.2026 von einem Helfer des steuernden Chats an geprüften Kopien des Standes `d781f1b` (Register am Commit `ee43f5f`).

## ⭐⭐ Freigabe des Betreibers, wörtlich

**04.10.2026, Auswahlkarte im steuernden Chat (gestellt gegen 21:00, Antwort eingetragen 21:04).** Kartentext: *„Gibst du TB-136 frei? Das umfasst: Register Abschnitt 54 anhängen (R74–R77 zeichengleich aus Fables Antwort 04.10.a, dazu 54.5–54.6 mit den Messungen des steuernden Chats), 15 Marken am alten Ort (13 nach R77 (a), zwei an 48.1 und 48.14 vom steuernden Chat nach R65 (a) bestimmt; keine in Abschnitt 9, Abschnitt 10 und im ERZEUGT-Block), vorher die Nachmessung der Voraussetzungen am Gerät (bei Abweichung kein Eintrag), Registerkopie, Index und Dialog-Index neu, BACKLOG-Block, Journal EE. Prüfungen am Register: test_vorregistrierung vor dem Commit, registerbericht.py --pruefen, numstat 110/0. Kein Code, kein neues Abbild. Datum des Eintrags: der Tag, an dem die Sitzung einträgt.“* Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**.

| freigegeben | Pfad / Handlung |
|---|---|
| Register **anhängen** (Abschnitt 54: 54.0 Kopf, 54.1–54.4 = R74–R77 zeichengleich, 54.5–54.6 Text des steuernden Chats) und **15 Marken additiv** am alten Ort (Anhang A) | `docs/VORREGISTRIERUNG_neuselektion.md` |
| neu erzeugen, nachziehen | `docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_<nn>.md`, `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` (beide über `docs/werkzeuge/registerkopie.py`), `docs/projektfuehrung/REGISTER_INDEX.md` |
| die Zeile für 04a, die Zeile 02c (offen → nein) und die Schlusszeile (das Werkzeug `docs/werkzeuge/dialog_index.py` schreibt die Datei neu; was es dabei sonst ändert, steht im Ergebnis) | `docs/projektfuehrung/FABLE_DIALOG_INDEX.md` |
| ein Block (Schritt B) | `docs/projektfuehrung/BACKLOG.md` |
| Journalblock (Kennung messen, erwartet **EE**) | `docs/projektfuehrung/JOURNAL.md` |
| committen in Schritt 0 | dieser Auftrag, `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/projektfuehrung/UEBERGABE.md`; unter `docs/projektfuehrung/` die vier Dateien `FABLE_ANFRAGE_2026-10-04a_…`, `FABLE_ANTWORT_2026-10-04a_…`, `FABLE_UEBERGABE_2026-10-04_eroeffnung.md`, `FABLE_UEBERGABE_2026-10-04_neuer_chat.md`; `docs/belege/TB-133/vormessung/v1_vormessung_04a.md`; `docs/belege/TB-134/CLOUD_TB-134_antwort_offene_voraussetzungen.md`; `docs/belege/TB-135/CLOUD_TB-135_antwort_anforderungen_zellen_erzeuger.md`; unter `docs/belege/TB-136/vormessung/` die vier Dateien der Vormessung |
| lesen: in 0e einmal, nur an den dort genannten Stellen; `eingaben.json` dazu in A4 durch die Wache des Einfügeskripts, im Probelauf und im echten Lauf | `research/snapshotgrenze/ergebnisse/eingaben.json` (nur das Feld `kalender`; in 0e und in A4), `notifications/boersenkalender.py`, `requirements.lock`, `research/mtm_drawdown/mtm_kern.py`, `research/vorregistrierung/auswertung.py` (diese vier nur in 0e); dazu in 0e `git grep` nach dem Paketnamen in `*.py` |
| Belege, Ergebnis | `docs/belege/TB-136/`, `docs/ERGEBNIS_TB-136_register_fable_04a.md` |
| verwerfen, nur nach rotem Nachweis in A5 und nachdem der Diff als `abbruch_register.diff` gesichert ist | die eigene, uncommittete Änderung am Register (`git checkout -- docs/VORREGISTRIERUNG_neuselektion.md`) |

⛔ **Nicht freigegeben, mit Grund:** wie TB-132 (dort die Liste unter der Freigabetabelle), mit diesen Werten:
- **Jede Zeile im Listentext von Abschnitt 10** und **im ERZEUGT-Block von Abschnitt 3.** *Grund:* wie TB-132; R77 (c) führt Abschnitt 9, Abschnitt 10 und den ERZEUGT-Block unter „Ohne Marke bleiben“.
- **Jede Änderung oder Löschung einer bestehenden Registerzeile.** *Grund und Nachweis:* wie TB-132 (append-only; numstat zweite Spalte 0).
- **Eine Marke, die nicht in Anhang A steht.** *Grund:* wie TB-132.
- **Ein Registereintrag nach einer Abweichung in 0e.** *Grund:* R74 (b) im Wortlaut: „trifft es nicht zu, wird gemeldet, nicht eingetragen“; für die übrigen Messungen aus 0e: 54.5 trüge sonst eine Zahl, die nicht stimmt. Das Einfügeskript trägt die Sperre zu R74 (b) als Wache (A4).
- **Code jeder Art**, insbesondere `research/`, `shared/`, `strategies/`, `notifications/`, `docs/werkzeuge/`. *Grund:* Textauftrag. Der Zellen-Erzeuger, der Kalender nach R74 (c), das zweite Spaltenpaar, die Wache und die Proben nach R75 (b) bis (g) und die Öffnung von `auswertung.py` nach R69 (b) sind **nicht** Gegenstand.
- **Ein neues Abbild der Sperrliste.** *Grund:* wie TB-132.
- **Läufe von `auswertung.py`, Zellen-Erzeugern oder Backtests.** *Grund:* Sichtschutz. `registerbericht.py --pruefen` ist kein solcher Lauf und in 0b und A5 verlangt. Die Messung nach R74 (e) in der Lock-Umgebung am Snapshot ist **nicht** Gegenstand (54.6 Nr. 1).
- Löschen oder Verwerfen ausser dem einen Fall in der Tabelle; `crontab`, Datenbanken; `UEBERGABE.md`, `UEBERGABE_ARCHIV.md`, die Dateien `FABLE_ANTWORT_*`, `FABLE_ANFRAGE_*`, `FABLE_UEBERGABE_*`, die Dateien unter `docs/belege/TB-136/vormessung/` und die drei Dateien unter `docs/belege/TB-133/`, `TB-134/` und `TB-135/` ändern (ausser dem Commit in Schritt 0). *Grund:* Das sind die Quellen.

**Sichtschutz 27.1:** Diese Sitzung liest keine Kennzahl, keine Trade- und keine Zeilenzahl aus Ergebnisdateien. Aus Testausgaben nur rc, Dauer und Schlusszeile. Code wird nur gelesen, wo Schritt 0e eine Zeile nennt. `eingaben.json` ist die Erhebung der Eingaben aus TB-47 (17.5 nennt sie), kein Ergebnis des Laufs; ausgegeben wird daraus nur das Feld `kalender`.

## Belegt · erschlossen · offen

*Gemessen am 04.10.2026 von einem Helfer des steuernden Chats (Erbauer) im Container, an Kopien des Standes `d781f1b`, die der steuernde Chat über die Geräteanbindung gezogen hat. Wo eine andere Quelle gilt, steht sie dabei. Eine Messung an einer Kopie ist kein Nachweis am Gerät; die Sitzung misst in 0a, 0b, 0d und 0e nach.*

**Belegt:**
- Register: 11 471 Zeilen, sha256 `9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff`, md5 `1ce393ae2f07513fa76ccc0b0f927d41` (an der Kopie gemessen; gleich `docs/ERGEBNIS_TB-132_register_fable_02c.md`, „Register nachher“). Letzter Commit, der es änderte: `ee43f5f`. Letzter Abschnitt: 53 (Z. 11378–11471, letzter Unterabschnitt 53.10). Die Datei endet mit einem Zeilenumbruch.
- Quelle der R-Blöcke: `docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md`, md5 `856b2c158e4bb6870876de129ce71f76`, 29 195 B, 167 Zeilen, uncommittet bis Schritt 0. Codezaun Z. 155 bis Z. 167; Blöcke R74–R77 in Z. 156–166 (R74 Z. 156–157, R75 Z. 159–160, R76 Z. 162–163, R77 Z. 165–166), zwischen zwei Blöcken je eine Leerzeile. Zwei unabhängige Abschriften aus der Ablage, `cmp` gleich; md5 auf dem Gerät gleich (`docs/belege/TB-136/vormessung/v1_bewertung_fable_04a.md`, Abschnitt 1).
- **Schnittregel (maschinell geprüft, 4/4):** wie TB-132 (dort nach TB-130 und TB-129). Geschnitten wird **nur** in Z. 156–166.
- Anfrage und Eröffnungstext: `FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md`, md5 `db37f969a557b60a27cbd7ac6b942def`, 9 574 B; `FABLE_UEBERGABE_2026-10-04_eroeffnung.md`, md5 `c96f56c9682d4fb8a37188735edae7ad`, 9 259 B (an den Kopien gemessen).
- Ausgangswerte (`docs/ERGEBNIS_TB-132_register_fable_02c.md`; die Sitzung misst sie in 0b): `herkunft.register()` `664809629137b537d233e19066ac6ab9d422c64be8841ff37c72862e0eb511b3`, `fehlend []`, 23 Teile · gültiges Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f` · Sonde dagegen: rc 2 (Normalfall), 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“, sha256 des JSON-Berichts ohne das Feld `zeilen` `9f7364ef32fd80ffba6931c776f3bdf43dc257a1f6aeac304cf818c89023f35e` · `registerbericht.py --pruefen`: rc 1 (bekannter Befund; verglichen wird nachher gegen vorher) · Abschnitt 10: Z. 965–1171, sha256 `da8697c0be1da37f8c6d1eddbf715e8003ba517c119576766f13c0e6a61889bc`; ERZEUGT-Block: Z. 260–460, `fda8ead14e4cd96e91548078f9e9dbae0c3a0c631b2a483f4bee757da31c9207` (beide an der Kopie nachgerechnet, in der Form der Dateien `0b_*_vorher.txt`) · `test_vorregistrierung` 196/196, rc 0, 892 s, mit diesem Register (`docs/belege/TB-132/a5_test_vorregistrierung.txt`).
- Registerkopie am `d781f1b`: 54 Abschnittsdateien, vier Teile (0–22 / 23–36 / 37–42 / 43–53); T4 hat 232 545 B bei einer Grenze von 240 000 B (ERGEBNIS TB-132, „Nebenbemerkungen“).
- `REGISTER_INDEX.md`: 420 Zeilen; `## 8. Die Marken aus Fable 02c (TB-132)` zählt 1 (Z. 363), eine Überschrift `## 9.` gibt es nicht, `Indexzeilen aus Fable 04a` zählt 0, „Zählung“ zählt 0. `FABLE_DIALOG_INDEX.md`: 54 Antworten, Zeile `02c` mit offen = ja, keine Zeile `04a`. `BACKLOG.md`: 297 Zeilen, der Anker `## 6 — Geparkt, null Arbeit` zählt 1 (Z. 286), `Aus Fable 04a` zählt 0. (Alle an den Kopien gemessen.)
- Vormessung: `docs/belege/TB-136/vormessung/v1_bewertung_fable_04a.md` mit drei Helferberichten; V1 trifft, V2 trifft im Wortlaut nicht, V3 trifft am Bestand; 65 Messpunkte (gemessen von Helfern des steuernden Chats über die Geräteanbindung, nur lesend).
- Prüfskript und Einfügeskript aus Anhang A: im Container gelaufen, an den Kopien und, für die Dateien, die nicht bei den Kopien liegen, an Attrappen (siehe „Prüfsumme“). Einfügen simuliert für zwei Daten: Zeilen 11 471 → 11 581, numstat `110	0`, Abschnitt 9, Abschnitt 10 und ERZEUGT-Block bytegleich, R74–R77 zeichengleich zur Quelle.
- Nummern: TB frei ab 137 · Journal **EE** (die Sitzung misst) · R-Blöcke nach diesem Auftrag frei ab R78.

**Erschlossen:**
- Die erste Einfügestelle ist Z. 2348, Abschnitt 10 endet in Z. 1171: Abschnitt 10 und der ERZEUGT-Block wandern nicht. Verglichen wird trotzdem wie in TB-132: der JSON-Bericht der Sonde ohne das Feld `zeilen`.
- Seit `1e13135` ist unter `research/`, `shared/`, `strategies/`, `config/`, `data/` nichts geändert: TB-132 mass das am Commit `57ae0d8` (0c, leer) und änderte danach nur `docs/`. Die Sitzung misst in 0c.
- Der Wortlaut der Code-Zeilen in 0e stammt aus den Helferberichten der Vormessung (`h1_fundstellen_r74.md`, `h2_fundstellen_r75.md`) und, für `boersenkalender.py` Z. 70, 81 und 109, `requirements.lock` Z. 51 und `mtm_kern.py` Z. 244 und 246, zusätzlich aus dem Daten-Block von TB-132, den TB-132 am Gerät geprüft hat. Im Container lagen diese Dateien nicht vor.
- `git status --porcelain` fasst einen Ordner, in dem nichts verfolgt ist, zu einer Zeile zusammen (im Container mit git 2.43 nachgestellt). Dass unter `docs/belege/TB-133/`, `TB-134/`, `TB-135/` und `TB-136/` nichts verfolgt ist, ist am Gerät nicht gemessen.
- Der Schlüssel der neuen Zeile im Dialog-Index lautet `04a` (Bauart der Zeilen `01a` bis `02c`: Tag und Buchstabe). Das Werkzeug `dialog_index.py` lag im Container nicht vor.
- Die drei Zählungen in `JOURNAL.md` (Daten-Block) stammen aus `docs/belege/TB-132/d2_journal_block.md` und dem Daten-Block von TB-132; `JOURNAL.md` lag im Container nicht vor.

**Offen (die Sitzung misst, nimmt nichts an):** der Ausgang der Nachmessung in 0e; die Journal-Kennung; die neuen Zeilenbereiche und Teilgrenzen der Registerkopie (der Abschnitt 54 und die 13 Marken in 48 bis 53 bringen 26 512 B in die Abschnitte 43 bis 54, in der Simulation gerechnet: 2 042 B in 43 bis 53, 24 470 B für Abschnitt 54. Erwartet ist deshalb ein fünfter Teil, siehe C1; gerechnet, am Werkzeug nachzumessen); welche weiteren Zeilen `dialog_index.py` ändert; sha256 und md5 des Registers nachher.

## Schritt 0 — Sicherung, Ausgang, Vorprüfung, Nachmessung der Voraussetzungen

**0a. Zuerst, bevor irgendetwas geschrieben oder committet wird.** Wie TB-132 0a, ohne dessen Punkt 1 (Datum).

1. **Arbeitsbaum:** `git status --porcelain > "$TMPDIR/tb136_0a.txt"`. Soll: genau die Einträge unten; die Reihenfolge zählt nicht. Weicht etwas ab ⇒ Abbruch.

*Eingetragen vom steuernden Chat beim Ablegen. `docs/belege/TB-133/` enthält nur `vormessung/v1_vormessung_04a.md`, `docs/belege/TB-134/` nur `CLOUD_TB-134_antwort_offene_voraussetzungen.md`, `docs/belege/TB-135/` nur `CLOUD_TB-135_antwort_anforderungen_zellen_erzeuger.md`, `docs/belege/TB-136/` nur `vormessung/` mit vier Dateien (`v1_bewertung_fable_04a.md`, `h1_fundstellen_r74.md`, `h2_fundstellen_r75.md`, `h3_fundstellen_r76_r77_leseprotokoll.md`). Die Liste der einzelnen Dateien prüft das Prüfskript in Punkt 2 (Daten-Block, `arbeitsbaum`: 2 geändert, 12 unverfolgt).*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-136_register_fable_04a.md
?? docs/belege/TB-133/
?? docs/belege/TB-134/
?? docs/belege/TB-135/
?? docs/belege/TB-136/
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_neuer_chat.md
```

2. **Skripte aus Anhang A auslesen und Arbeitsbaum prüfen.** Die zwei Skripte werden mit genau diesem Aufruf aus dem Auftrag gelesen, nicht abgeschrieben:

```
trading-env/bin/python3 - docs/auftraege/MAC_TB-136_register_fable_04a.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
for kopf, name in (("### Prüfskript", "pruefe_anhang_tb136.py"), ("### Einfügeskript", "a4_eintrag.py")):
    i = z.index(kopf)
    a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
    b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
    t = "\n".join(z[a + 1:b]) + "\n"
    open(sys.argv[2] + "/" + name, "w", encoding="utf-8").write(t)
    print(name, hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: die zwei sha256 aus Anhang A. Dann `trading-env/bin/python3 "$TMPDIR/pruefe_anhang_tb136.py" docs/auftraege/MAC_TB-136_register_fable_04a.md . --arbeitsbaum --datum "$(TZ=Europe/Berlin date +%d.%m.%Y)" > "$TMPDIR/tb136_0a_pruefung.txt"; echo "rc $?"` ⇒ Soll rc 0 (Register, Anker, Quelle, md5 der drei gelegten Dateien, Fundstellen, Zählungen, uncommittete Dateien genau wie im Daten-Block). rc ≠ 0 ⇒ Abbruch. Das Prüfskript gibt auch dann rc 1, wenn im Auftrag unter „Freigabe des Betreibers, wörtlich“ noch der Platzhalter statt der Freigabe steht. Der Schalter `--trockenlauf` wird **nicht** benutzt.

Commit `TB-136 Schritt 0: Stand des steuernden Chats (Fable 04a, Vormessung TB-136, Belege TB-133 bis TB-135)`, pushen. Danach steht für alle Quellenangaben der Commit von Schritt 0, im Folgenden **⟨S0⟩** (kurz, 7 Zeichen). Erst jetzt, wie TB-132: `$TMPDIR/tb136_0a.txt` und `$TMPDIR/tb136_0a_pruefung.txt` nach `docs/belege/TB-136/0a_status.txt` und `0a_pruefung.txt` kopieren, die zwei Skripte nach `docs/belege/TB-136/0d_vorpruefung.py` und `docs/belege/TB-136/a4_eintrag.py` (zeichengleich; sha256 danach noch einmal).

**0b. Ausgangswerte** ⇒ `docs/belege/TB-136/0b_ausgang.txt`: wie TB-132 0b, mit `0b_ausgang.sh` nach der Vorlage `docs/belege/TB-132/0b_ausgang.sh`. Soll: die Werte unter „Belegt“; dazu md5 und Bytes der Quelle 04a am Commit ⟨S0⟩ und im Arbeitsbaum, `0b_abschnitt10_vorher.txt` und `0b_erzeugt_vorher.txt` (Soll: die zwei sha256 unter „Belegt“). Weicht ein Wert mit Soll ab ⇒ Abbruch.

**0c. Basis `test_vorregistrierung`:** wie TB-132 0c: `git diff --name-only 1e13135 HEAD -- research/ shared/ strategies/ config/ data/` ⇒ `0c_basis.txt`. Leer ⇒ die Basis ist der Beleg `docs/belege/TB-132/a5_test_vorregistrierung.txt` (196/196). Nicht leer ⇒ Basislauf am Stand ⟨S0⟩ ohne Zeitgrenze, Soll 196/196, sonst Abbruch.

**0d. Vorprüfung vor jedem Registereintrag** ⇒ `docs/belege/TB-136/0d_vorpruefung.txt`: `trading-env/bin/python3 docs/belege/TB-136/0d_vorpruefung.py docs/auftraege/MAC_TB-136_register_fable_04a.md . --datum "$(TZ=Europe/Berlin date +%d.%m.%Y)"` (ohne `--arbeitsbaum`), am Commit ⟨S0⟩. Soll rc 0, die erste Zeile `Datum des Eintrags: <TT.MM.JJJJ> (aus --datum)`, die fünf Zeilen von `Marken:` bis `Bloecke:` wie unter „Prüfsumme“ in Anhang A und die Schlusszeile `rc 0: alles wie angegeben`. Geprüft ist damit, wie in TB-132 0d:
1. **Marken:** Jeder Anker aus dem Daten-Block kommt im Register genau 1-mal vor, steht am Anfang der genannten Ankerzeile, und jede Einfügestelle „nach Zeile N“ beginnt mit dem angegebenen Anfang. Jede Markenzeile 1 trägt den Platzhalter für das Datum genau einmal. Weicht eine Marke ab ⇒ **Abbruch vor Schritt A**.
2. **Quelle:** md5 der Antwortdatei; die Schnittregel ergibt genau R74–R77, je zwei Zeilen, in Z. 156–166.
3. **Noch nicht vergeben:** Im Register zählt `## 54.` 0, und keine Zeile beginnt mit `> R74 — `.
4. **Fundstellen für 54.5 und 54.6 und für die Schritte B und C:** jede Zeile der Liste `fundstellen` (Datei, Zeile, Teilzeichenkette: die Zeile enthält sie) und jede Zählung aus `zaehlungen`. Die Listen `zeilen_mit`, `glob_summen`, `glob_treffer` und `baum_summen` sind leer. **Weicht hier etwas ab ⇒ Abbruch vor Schritt A.** Dazu gehören die zwei Zählungen in `BACKLOG.md` (der Anker zählt 1, `Aus Fable 04a` zählt 0). Weichen sie ab, bricht schon 0a ab, bevor etwas committet ist.
5. **Dateien:** md5 und Bytes der drei Dateien Anfrage, Eröffnungstext und Antwort wie im Daten-Block. `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md` tragen kein Soll; sie ändern sich bis zum Start.
6. **Freigabe:** Im Auftrag steht kein Platzhalter für die Freigabe mehr. Sonst ⇒ Abbruch.

Nicht nachgemessen werden in 0d das Feld `kalender` und die Code-Zeilen; das ist 0e. Nicht nachgemessen werden überhaupt: die Zeilen aus den Antworten 02b und 02c, die 54.5 in der Zeile zu R76 nennt, und die 65 Messpunkte; 54.5 nennt sie als Messung der Helfer.

**0e. Nachmessung der Voraussetzungen (R74 (b), R75 (a), R75 (g)), vor jedem Registereintrag.** Sie tritt an die Stelle der Probe aus TB-132 0e. Aus dem Repo-Wurzelverzeichnis, genau so (nur lesend; die Ausgabe ist der Beleg; `PYTHONIOENCODING=utf-8` wie in TB-132 0e, damit die Ausgabe auch dann geschrieben wird, wenn die Standardausgabe nicht UTF-8 ist):

```
PYTHONIOENCODING=utf-8 trading-env/bin/python3 - . > docs/belege/TB-136/0e_voraussetzungen.txt 2>&1 <<'EOF'
import json, re, subprocess, sys
w = sys.argv[1].rstrip("/") + "/"
v1, ab = [], []
def zeilen(d): return open(w + d, encoding="utf-8").read().split("\n")
def wert(liste, name, ist, soll):
    print("%s | %s | ist %r | Soll %r" % ("ok  " if ist == soll else "FEHL", name, ist, soll))
    if ist != soll: liste.append(name)
def stelle(d, n, *teile):
    z = zeilen(d)
    s = z[n - 1] if n <= len(z) else None
    ok = s is not None and all(t in s for t in teile)
    print("%s | %s:%d enthaelt %s | Zeile: %r" % ("ok  " if ok else "FEHL", d, n, " und ".join(repr(t) for t in teile), s if s is None else s.strip()))
    if not ok: ab.append("%s:%d" % (d, n))
def zahl(d): return open(w + d, encoding="utf-8").read().count("\n")

print("# TB-136 0e: Nachmessung der Voraussetzungen und Tatsachen fuer 54.5 (nur lesend)")
print("## V1 - R74 (b): Feld kalender der Messung TB-47")
k = json.load(open(w + "research/snapshotgrenze/ergebnisse/eingaben.json", encoding="utf-8"))["kalender"]
print("Feld kalender: " + json.dumps(k, ensure_ascii=False, sort_keys=True))
wert(v1, "im_repo[0].modul", k["im_repo"][0]["modul"] if k["im_repo"] else None, "notifications/boersenkalender.py")
wert(ab, "Zahl der Eintraege in im_repo", len(k["im_repo"]), 1)
wert(ab, "im_repo[0].import", k["im_repo"][0].get("import") if k["im_repo"] else None, "pandas_market_calendars")
wert(ab, "im_repo[0].zeile", k["im_repo"][0].get("zeile") if k["im_repo"] else None, 81)
wert(ab, "in_selektionshuelle", k["in_selektionshuelle"], [])
wert(ab, "paket_vorhanden", k["paket_vorhanden"], "5.4.0")
wert(ab, "Kalendername (NYSE, XNYS) im Feld", [n for n in ("NYSE", "XNYS") if n in json.dumps(k)], [])

print("## Tatsachen zu R74 (b): Import, Name, Aufruf, Lock")
B = "notifications/boersenkalender.py"
stelle(B, 70, 'KALENDER_NAME = "NYSE"')
stelle(B, 81, "import pandas_market_calendars as mcal")
stelle(B, 109, "mcal.get_calendar(KALENDER_NAME)")
g = subprocess.run(["git", "--no-optional-locks", "-C", w, "grep", "-n", "pandas_market_calendars", "--", "*.py"],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
treffer = [x for x in g.stdout.decode("utf-8", "replace").split("\n") if x]
print("git grep -n 'pandas_market_calendars' -- '*.py': rc %d, %d Zeilen" % (g.returncode, len(treffer)))
for x in treffer: print("    " + x)
imp = [":".join(x.split(":", 2)[:2]) for x in treffer if re.match(r"^[^:]+:\d+:\s*(import|from)\s+pandas_market_calendars\b", x)]
wert(ab, "Import-Anweisungen des Pakets (Datei:Zeile)", imp, [B + ":81"])
wert(ab, "Treffer unter research/vorregistrierung/", [x for x in treffer if x.startswith("research/vorregistrierung/")], [])
stelle("requirements.lock", 51, "pandas-market-calendars==4.6.1")

print("## V2 - R75 (a): Kern der MtM-Reihe")
M = "research/mtm_drawdown/mtm_kern.py"
wert(ab, M + " Zeilen", zahl(M), 339)
stelle(M, 210, "buch", "kapital_after")
stelle(M, 244, "unreal[a:b + 1] += allokation[i] * (schluss / einstand[i] - faktor_kosten)")
stelle(M, 246, "gebunden[a:b + 1] += allokation[i]")
stelle(M, 251, '"mtm": buch + unreal')

print("## V3 - R75 (g): Abschnitt 8 des Registers")
R = zeilen("docs/VORREGISTRIERUNG_neuselektion.md")
a8 = next(i for i, s in enumerate(R) if s.startswith("## 8."))
a9 = next(i for i, s in enumerate(R) if s.startswith("## 9."))
tab = [s for s in R[a8:a9] if s.startswith("|")]
wert(ab, "Abschnitt 8 (Z. %d-%d): Tabellenzeilen nach Kopfzeile und Trennzeile" % (a8 + 1, a9), len(tab) - 2, 13)
wert(ab, "Abschnitt 8: 'zellenbericht' (ohne Gross/Klein)", sum(s.lower().count("zellenbericht") for s in R[a8:a9]), 0)

print("## Tatsachen zu R75 (b), (d), (g): auswertung.py")
A = "research/vorregistrierung/auswertung.py"
wert(ab, A + " Zeilen", zahl(A), 860)
stelle(A, 46, "datum, netto_rendite, exposure")
at = open(w + A, encoding="utf-8").read()
for b in ("kapital_drawdown_mtm_pct", "zellenbericht", "bestaetigung_ab_effektiv"):
    wert(ab, A + ": " + b, at.count(b), 0)

if v1:
    print("rc 3: V1 TRIFFT NICHT ZU - melden, nicht eintragen (R74 (b))"); sys.exit(3)
if ab:
    print("rc 1: ABWEICHUNG von 54.5 - kein Eintrag, melden: " + "; ".join(ab)); sys.exit(1)
print("rc 0: Voraussetzungen wie in 54.5"); sys.exit(0)
EOF
echo "rc $?" >> docs/belege/TB-136/0e_voraussetzungen.txt
```

Soll: Jede Zeile der Ausgabe, die mit `ok` oder `FEHL` beginnt, beginnt mit `ok`; die zwei letzten Zeilen lauten `rc 0: Voraussetzungen wie in 54.5` und `rc 0`. Gemessen ist damit, was 54.5 für die Sitzung nennt:

| | Messung | Soll |
|---|---|---|
| V1, R74 (b) | `research/snapshotgrenze/ergebnisse/eingaben.json`, Feld `kalender` | `im_repo` hat einen Eintrag: `import` `pandas_market_calendars`, `modul` `notifications/boersenkalender.py`, `zeile` 81; `in_selektionshuelle` ist `[]`; `paket_vorhanden` ist `5.4.0`; weder „NYSE“ noch „XNYS“ im Feld |
| Tatsachen zu R74 (b) | `notifications/boersenkalender.py` Z. 70, 81, 109; `git grep -n 'pandas_market_calendars' -- '*.py'`; `requirements.lock` Z. 51 | Z. 70 enthält `KALENDER_NAME = "NYSE"`, Z. 81 `import pandas_market_calendars as mcal`, Z. 109 `mcal.get_calendar(KALENDER_NAME)`; unter den Treffern ist genau eine Import-Anweisung, `notifications/boersenkalender.py:81`; kein Treffer unter `research/vorregistrierung/`; Z. 51 enthält `pandas-market-calendars==4.6.1` |
| V2, R75 (a) | `research/mtm_drawdown/mtm_kern.py` | 339 Zeilen; Z. 210 enthält `buch` und `kapital_after`; Z. 244 `unreal[a:b + 1] += allokation[i] * (schluss / einstand[i] - faktor_kosten)`; Z. 246 `gebunden[a:b + 1] += allokation[i]`; Z. 251 `"mtm": buch + unreal` |
| V3, R75 (g) | Register, Abschnitt 8 (von `## 8.` bis vor `## 9.`) | 13 Tabellenzeilen nach Kopfzeile und Trennzeile; `zellenbericht` 0-mal |
| Tatsachen zu R75 (b), (d), (g) | `research/vorregistrierung/auswertung.py` | 860 Zeilen; Z. 46 enthält `datum, netto_rendite, exposure`; `kapital_drawdown_mtm_pct`, `zellenbericht` und `bestaetigung_ab_effektiv` je 0-mal |

„Zeilen“ einer Datei zählt die Zeilenumbrüche (wie `wc -l`). V2 ist hier die Messung dessen, was 54.5 nennt; dass die Voraussetzung im Wortlaut nicht trifft, steht in 54.5 und hält den Eintrag nicht auf (R75 (a): gemeldet wird, „bevor der Zellen-Erzeuger die Attribution baut“).

**Abbruchregeln zu 0e:**
- Endet der Aufruf mit `rc 3` (das `modul` aus V1 trifft nicht zu): **Abbruch ohne Eintrag** (R74 (b): „wird gemeldet, nicht eingetragen“).
- Endet er mit `rc 1` oder mit einer Fehlermeldung von Python (eine Datei fehlt, das Feld fehlt): **Abbruch ohne Eintrag, mit Meldung**; 54.5 trüge sonst eine Zahl, die nicht stimmt.
- In beiden Fällen: nichts am Register ändern. Die Ausgabe bleibt als Beleg; Grund nach `docs/belege/TB-136/abbruch.txt`; Commit `TB-136 0: Ausgang, Vorprüfung, Voraussetzung weicht ab (kein Registereintrag)`, pushen, melden, Sitzung beenden. Der Aufruf wird nicht geändert und nicht mit anderen Werten wiederholt.

Danach `git status --porcelain`: Neu sind nur Dateien unter `docs/belege/TB-136/`.

Commit `TB-136 0: Ausgang, Vorprüfung, Nachmessung der Voraussetzungen`, pushen.

## Schritt A — Abschnitt 54 und die Marken, in einem Lauf

**A1. Gliederung (vom steuernden Chat vergeben):** 54.0 Kopf · 54.1–54.4 = R74–R77 in der Reihenfolge des Codezauns (54.n = R(73 + n)) · 54.5–54.6 Text des steuernden Chats (A3). Überschriften und Ketten stehen exakt im Daten-Block von Anhang A. Form je R-Block wie TB-132 A1 (dort nach TB-130 A1 und TB-129 A1): Überschrift, Leerzeile, die zwei Blockzeilen je mit `> ` davor, Leerzeile, Kette. Zwei Überschriften (54.1, 54.2) wären länger als 140 Zeichen; sie sind am Ende an einer Wortgrenze mit „…“ gekürzt (Bauart 47.4 und 48.7). Der Block darunter steht vollständig. Abschnitt 54 wird ans Dateiende angehängt, mit einer Leerzeile nach der letzten bestehenden Zeile.

**A2. Marken am alten Ort.** Wie TB-132 A2, erster Absatz: Die 15 Marken stehen fertig in Anhang A; massgeblich ist der Daten-Block. Die Sitzung baut die Tabelle **nicht** selbst. Je Marke: eine Leerzeile, Markenzeile 1, Markenzeile 2. Anders als in TB-132 steht in der Markenzeile 1 der Platzhalter `⟨DATUM⟩`; das Einfügeskript ersetzt ihn durch das Datum aus `--datum`. Eingesetzt wird nach den Zeilennummern am Original. Die Marken nennen ihren Ort mit Bezeichner, nie mit Zeilennummer (R49 (e)); Zeilennummern stehen nur in diesem Auftrag, als Hilfe.

Regeln, nach denen Anhang A gebaut ist (zur Prüfung, nicht zum Neubauen): 13 Marken zählt R77 (a) auf; jeder der 13 Sätze „Ort — Markenwort durch R…“ steht wörtlich in der Quelle, Z. 165 (maschinell geprüft, 13/13). Zwei weitere hat der steuernde Chat nach R65 (a) bestimmt, R77 (a) nennt sie nicht: 48.1 (R33), PRÄZISIERT durch R75 (c), weil R75 (c) sagt, woraus „Die Zeile der Bestätigungsperiode in zellen.csv (R33, R68)“ gebildet wird, und 48.1 für dieselbe Zeile schon die Marke zu R68 trägt; 48.14 (R46), ERGÄNZT durch R75 (d) und (f), weil diese Unterpunkte der Abnahme nach R46 eine weitere Prüfung und dem Test-Snapshot einen Deckelfall geben. Beide tragen den Zusatz „vom steuernden Chat nach R65 (a) bestimmt“ und gehen zur Kenntnis an Fable (54.6 Nr. 6). Der Ort heisst in der Marke wie in R77 (a), die Blocknummer ohne Klammer („48.5 R37“, Bauart der Marken aus TB-132). Der Unterpunkt des neuen Blocks steht in der Klammer, wo R77 (a) einen nennt. Einfügestellen: Block in 48 bis 53: nach dem Blockzitat und den dort stehenden Marken, vor der Zeile `**Kette:**`. 16.6: nach der dort stehenden Marke zu R37, vor dem Trenner `---`. 17.5: direkt unter dem Blockzitat des Registertexts 5f, in dem die Tatsachennotiz zum Handelskalender steht, vor dem Absatz, der mit „⚠️ **Das schärft“ beginnt (Vorbild 15.3 und 23.3, Registertext). 53.9: nach der Tabelle, vor `### 53.10` (Bauart 52.4). An einem Ort: nach den vorhandenen Marken. Jede Einfügestelle trägt genau eine neue Marke. Keine Marke tragen die Orte aus R77 (c): 48.20 (R52) (Indexzeile, C3), 53.10, 50.2, 29.3, 41.3, 35.1 und 27.2; ⛔ keine in Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3.

**A3. Text des steuernden Chats** — zeichengleich, mit ⟨S0⟩ und ⟨DATUM⟩ ersetzt; ⟨S0⟩ steht im Register in Backticks, wie in 53, das Datum ohne (beide Ersetzungen macht das Einfügeskript). Der Kopf steht vor 54.1, der Schluss nach 54.4. Der Platzhalter für das Datum steht genau einmal im Kopf und nicht im Schluss; die Daten in 54.5 („Gemessen am 04.10.2026“, „führte am 04.10.2026“) sind Daten der Messung und bleiben.

Kopf:

````
## 54. Fable 04a — Registerblock R74–R77 (TB-136)

Reines Eintragen von Registertext, Bauart wie 53. Quelle ist allein `docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md`, md5 `856b2c158e4bb6870876de129ce71f76`, 29 195 B, im Repo seit Commit ⟨S0⟩, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R74)“, Z. 156–166. Zum Dialog gehören die Anfrage 04.10.a (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md`) und der Eröffnungstext (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md`), beide im Repo seit Commit ⟨S0⟩; dieser Kopf nennt Datei, md5 und Commit, das ist die Bindung nach R56 (b). Der Chat des Verfahrensprüfers vom 04.10.2026 ist neu begonnen; sein Anfangsbestand ist der Eröffnungstext und das Leseprotokoll der Antwort (R56 (a)); zum Leseprotokoll 54.6 Nr. 9. Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette, wie in 53. Die Überschriften von 54.1 und 54.2 sind am Ende gekürzt („…“, wie 47.4 und 48.7); der Block darunter steht vollständig. Die Nummern 54.1–54.4 hat der steuernde Chat vergeben (Auftrag TB-136, Einzelfreigabe des Betreibers), nicht Fable. Gesetzt sind 15 Marken: die 13, die R77 (a) aufzählt, und zwei an 48.1 (R33) und 48.14 (R46), die der steuernde Chat nach R65 (a) bestimmt hat (54.6 Nr. 6). Die Marke zur Zeile „R66 (53.1) (b)“ in 53.9 steht nach der Tabelle (Vorbild 52.4). ⛔ In Abschnitt 9, in Abschnitt 10 und im ERZEUGT-Block von Abschnitt 3 steht keine neue Marke. Ohne Marke bleiben 48.20 (R52), 53.10, 50.2, 29.3, 41.3, 35.1 und 27.2 (R77 (c)). Die Voraussetzungen und Tatsachen der Blöcke stehen mit Befund in 54.5; was offen bleibt, steht in 54.6. Die Vormessung des steuernden Chats liegt unter `docs/belege/TB-136/vormessung/`. 54.5 und 54.6 sind Text des steuernden Chats, nicht Fables. Eingetragen am ⟨DATUM⟩.
````

Schluss:

````
### 54.5 Voraussetzungen und Befunde

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 04a „zu messen“ nennt, und zu den Tatsachen, die die Blöcke über Code und Register führen. Gemessen am 04.10.2026 am Stand `d781f1b`, nur lesend, durch Helfer des steuernden Chats; die Berichte liegen unter `docs/belege/TB-136/vormessung/`. Die Sitzung TB-136 hat die Zeilen zu R74 (b), R75 (a) und R75 (g) am Gerät nachgemessen (`docs/belege/TB-136/0e_voraussetzungen.txt`). Gezählt sind Zeilennummern, Vorkommen und Fassungen. Kein Ergebnis gelesen (27.1).

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R74 (54.1) (b) | „dass das Feld kalender der Messung TB-47 als Importstelle notifications/boersenkalender.py führt“ | `research/snapshotgrenze/ergebnisse/eingaben.json`, Feld `kalender`: `im_repo` führt einen Eintrag mit `import` `pandas_market_calendars`, `modul` `notifications/boersenkalender.py`, `zeile` 81; `in_selektionshuelle` ist leer. Ein Kalendername steht im Feld nicht | trifft |
| R74 (54.1) (b), Tatsachen im Block | einziger Import, Name und einziger Aufruf in `notifications/boersenkalender.py` | Z. 70 `KALENDER_NAME = "NYSE"`, Z. 81 `import pandas_market_calendars as mcal`, Z. 109 `mcal.get_calendar(KALENDER_NAME)`; keine weitere Import-Anweisung des Pakets im Repo; unter `research/vorregistrierung/` kein Treffer | trifft |
| R74 (54.1) (e) | keine Voraussetzung; Messung vor dem Tag | Die Messung in der Lock-Umgebung am Snapshot steht aus. Der Lock führt `pandas-market-calendars==4.6.1` (`requirements.lock`, Z. 51); das Feld `kalender` aus TB-47 nennt `paket_vorhanden` 5.4.0 | offen (54.6 Nr. 1 und Nr. 8) |
| R75 (54.2) (a) | „dass der Kern, der die MtM-Reihe bildet, die Tagesrendite als Summe der Beiträge der Positionen über einem Kapitalstand bildet“ | `research/mtm_drawdown/mtm_kern.py` (339 Zeilen), Funktion `mtm_pfad`: Z. 251 bildet `mtm` als `buch + unreal`; Z. 244 summiert in `unreal` den unrealisierten Stand je Position; Z. 210 nimmt `buch` aus `kapital_after`; Z. 246 summiert `gebunden` zum Einstand. Die Datei bildet keine Tagesrendite und keine Exposure und teilt in `mtm_pfad` durch keinen Kapitalstand | trifft im Wortlaut nicht: Der Kern bildet Kapitalreihen, keine Tagesrendite. Unrealisiertes ist je Position summiert; Realisiertes kommt über `kapital_after` und ist dort nicht je Position geführt. Gemeldet (54.6 Nr. 2) |
| R75 (54.2) (g) | „dass der Bericht der Zeile aus zellenbericht.csv nach R34 keine eigene Zeile in der Berichtsliste von Abschnitt 8 verlangt“ | Abschnitt 8 führt eine Tabelle mit 13 Zeilen; `zellenbericht` kommt in Abschnitt 8 nicht vor. R34 (48.2) lässt `auswertung.py` die Zeile des Plateau-Gewinners berichten („Bericht, kein Tor; N unverändert“), ohne dass Abschnitt 8 dafür eine Zeile führt | trifft am Bestand |
| R75 (54.2) (b), (d), (g), Tatsachen im Block | Tagesreihe, Nachrechnung und Bericht in `auswertung.py` | `research/vorregistrierung/auswertung.py` (860 Zeilen): Der Docstring führt die Tagesreihe in Z. 46 als `datum, netto_rendite, exposure`; `kapital_drawdown_mtm_pct`, `zellenbericht` und `bestaetigung_ab_effektiv` kommen in der Datei nicht vor. Einen Zellen-Erzeuger gibt es im Repo nicht | Bestand; was R75 verlangt, kommt mit der Öffnung nach R69 (b) und mit dem Zellen-Erzeuger (54.6 Nr. 3 und Nr. 4) |
| R76 (54.3) | Tatsachen über 02b, 02c und die Zählung | 02b Z. 144 („beide kommen aus einer Rechnung (R60 (c))“), Z. 16–17 (Abschnitte 15 und 51 im Leseprotokoll als gelesen), Z. 124, 127 und 138; 02c Z. 41. Im Register: neunter Fall in 45.1, zehnter in 48.20 (R52 (a)), elfter in 48.1 und 48.20 (R52 (b)) | trifft |
| R77 (54.4) (a) | 13 Orte | alle 13 Orte vorhanden; die Zuordnung Unterabschnitt zu Block stimmt an den zehn Orten, die R77 (a) mit Blocknummer nennt | trifft; dazu zwei Marken des steuernden Chats (54.6 Nr. 6) |
| R74–R77, Zitate und Verweise | — | 65 Messpunkte in drei Berichten. Jedes wörtliche Zitat ist gefunden; vier stehen im Register über einen Zeilenumbruch (je zwei in 17.5 und 16.6), eines davon mit Fettdruck im Zitat. Sinngemäss treffen sechs Stellen der Blöcke: R75 (a) „Die Zuteilung läuft je Zelle einmal (R45)“ (R45 nennt die Rekonstruktion der Positionen aus der equity_curve einen zweiten Rechenweg; „einmal“ und „je Zelle“ stehen dort nicht); R75, Quelle, „29.3 (ein Kapitalpfad)“ (29.3 legt den Beginn des Kapitalpfads eines Bots fest; „ein Kapitalpfad“ steht dort nicht); R74, Quelle, „R28 (Bauart: Kopie mit Probe)“ (R28: „Literal mit Probe gegen den Registertext“; die Wortfolge steht in der Quelle von R59); R75 (b) „nie leer (R67)“ (R67: „kein Feld leer“); R77 (c) „53.10 (Statusliste)“ (53.10 heisst „Was offen bleibt“); R77 (c) „der Index führt die Zählung“ (`REGISTER_INDEX.md` führte am 04.10.2026 keine Zählung der Fälle; Lesart des steuernden Chats, vorläufig: Vorgabe für den Index, kein Bestand) | keine Stelle trifft nicht; die sinngemässen gehen zur Kenntnis an Fable (54.6 Nr. 7) |

### 54.6 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | Verfahrensmessung in der Lock-Umgebung am Snapshot (R74 (e)): die Bedingung aus R66 (b) für den Kalender „NYSE“, je Aktien-Bot; zusammen mit der Messung nach R72 (d) (53.10 Nr. 3) | vor dem signierten Tag |
| 2 | Meldung zu R75 (a) (54.5): Der Kern bildet keine Tagesrendite. Wie der Zellen-Erzeuger den Beitrag einer Position bildet, wenn Realisiertes über `kapital_after` kommt | nächste Anfrage an Fable, vor dem Bau der Attribution |
| 3 | Zellen-Erzeuger, dazu aus R74 und R75: Kalender unter dem Namen nach R74 (a), als Konstante oder als Kopie mit Probe (R74 (c)); zweites Spaltenpaar in jeder Tagesreihe (R75 (b)); Zeile der Bestätigungsperiode aus diesem Paar (R75 (c)); Wache im Lauf (R75 (e)); Zahl der nicht gezählten Positionen in `zellenbericht.csv` (R75 (g)) | mit dem Zellen-Erzeuger, Abnahme nach R46 |
| 4 | Planmässige Öffnung von `auswertung.py` (R69 (b)), dazu aus R75: Nachrechnung von `kapital_drawdown_mtm_pct` für die Zeile der Bestätigungsperiode aus dem Paar (R75 (d)); Bericht der Zahl der nicht gezählten Positionen (R75 (g)); die zwei Spaltennamen im Docstring, danach die Feldliste in 50.2 neu messen (R75 (b), R77 (c)) | eigener Umsetzungsauftrag mit Freigabe, vor der Abnahme nach R46 |
| 5 | Abnahme nach R46, dazu aus R75 (d) und (f): Test-Snapshot mit einer Zelle mit Deckelfall und einer ohne; Prüfung in beide Richtungen; mittlere Exposure der Zeile gegen das Mittel der Exposure der Bestätigung. Aus der Antwort 04.10.a, Frage 1 (b), zur Kenntnis und nicht im Block: Der Test-Snapshot braucht Kurstage, die zum Kalender passen | Abnahme nach R46 |
| 6 | Marken an 48.1 (R33), PRÄZISIERT durch R75 (c), und an 48.14 (R46), ERGÄNZT durch R75 (d) und (f). R77 (a) nennt sie nicht; der steuernde Chat hat sie nach R65 (a) bestimmt. Lesart, vorläufig. Dazu: R60 (c), R64 (c) und (d), R66 (b) und (e) und R67 geben der Abnahme nach R46 ebenfalls eine Prüfung; 48.14 trägt dafür keine Marke | nächste Anfrage an Fable |
| 7 | Die sinngemässen Verweise aus 54.5 (letzte Zeile) | nächste Anfrage an Fable, zur Kenntnis |
| 8 | Das Feld `kalender` aus TB-47 nennt `paket_vorhanden` 5.4.0; der Lock und 17.5 nennen 4.6.1 | mit der Verfahrensmessung nach Nr. 1 |
| 9 | Leseprotokoll der Antwort 04.10.a: ein Ausschnitt aus `BACKLOG.md`, von der Suche der Ablage geliefert, gesehen und nach R56 (b) genannt; die Datei nicht geöffnet. Kein eigener Block nach R56 (c). Lesart des steuernden Chats, vorläufig | nächste Anfrage an Fable, zur Kenntnis |
| 10 | Trade-Zahl und ereignisindizierter Drawdown der Zeile im Deckelfall: R75 (a) gibt den Grundsatz. Welcher Handelstag der Deckeltag ist, bestimmen R37 (i), 16.6 und 41.3 C2; R75 legt dazu nichts fest (Antwort 04.10.a, „Unsicher“ 3 und 4) | mit dem Zellen-Erzeuger; reicht der Grundsatz nicht, Frage an Fable |

Von 53.10 sind damit erledigt: Nr. 1 durch R74 (a), Nr. 2 durch R75 (a) bis (f) und (h), Nr. 8 durch die Antwort 04.10.a („Zur Kenntnis“, K1: einverstanden), Nr. 9 durch R76 (d). Nr. 3 bleibt und nimmt die Messung nach R74 (e) auf (hier Nr. 1). Nr. 4 und Nr. 5 bleiben und sind hier um Nr. 4 und Nr. 3 erweitert. Nr. 6, 7 und 10 bleiben, wie sie dort stehen.
````

**A4. Einsetzen.** Wie TB-132 A4, mit diesen Unterschieden. Das Einfügeskript steht fertig in Anhang A (`### Einfügeskript`); die Sitzung schreibt es nicht selbst und ändert es nicht. Es liegt seit 0a zeichengleich unter `docs/belege/TB-136/a4_eintrag.py`. Es liest Kopf, Schluss und den Daten-Block aus diesem Auftrag und die Blöcke aus der Antwortdatei, beides als Datei. Deshalb vorher: `git diff --quiet ⟨S0⟩ -- docs/auftraege/MAC_TB-136_register_fable_04a.md docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md; echo "rc $?"` ⇒ Soll rc 0. Dann das Datum, einmal: `TZ=Europe/Berlin date +%d.%m.%Y > docs/belege/TB-136/a4_datum.txt`; dieser Wert ist im Folgenden **⟨DATUM⟩**. **Zuerst ein Probelauf gegen eine Kopie** (`cp` des Registers in den Scratch, dann `trading-env/bin/python3 docs/belege/TB-136/a4_eintrag.py --s0 ⟨S0⟩ --datum ⟨DATUM⟩ --register <kopie>`), Vorlage `docs/belege/TB-132/a4_probelauf.sh`; an der Kopie laufen die Textprüfungen aus A5. Erst wenn sie grün sind, einmal echt (`… --s0 ⟨S0⟩ --datum ⟨DATUM⟩ --daten docs/belege/TB-136/a4_eintrag_daten.json`); danach muss das Register `cmp`-gleich mit der Kopie sein, und die Zeile `sha256 nachher:` ist in beiden Läufen dieselbe. **Eine Wache trägt das Skript selbst**, in jedem Lauf ohne `--vorschau`, also im Probelauf und im echten Lauf: Es schreibt nur, wenn in `research/snapshotgrenze/ergebnisse/eingaben.json` im Feld `kalender` der erste Eintrag von `im_repo` als `modul` `notifications/boersenkalender.py` nennt (V1 aus 0e; R74 (b)). Sonst bricht es mit einer Meldung ab, bevor es schreibt; das ist dann ein Abbruch, kein Anlass für einen anderen Aufruf. Ein Datum prüft das Skript nur der Form nach; es schreibt an jedem Tag. Der Schalter `--vorschau` hebt die Wache auf; er gehört dem Soll-Bau des steuernden Chats und wird von der Sitzung **nicht** benutzt (Schutz des Registers im Vorschau-Modus wie in TB-132). Soll der Ausgabe: `Marken gesetzt am alten Ort: 15 an 15 Einfuegestellen` · `R-Bloecke: 4 (R74-R77)` · `Zeilen vorher: 11471  nachher: 11581  eingefuegt: 110`. Die Wachen stehen im Kopf des Skripts; eine verletzte Wache bricht ab, bevor geschrieben wird.

Rechnung 110: 15 Marken × 3 Zeilen (Leerzeile, Markenzeile 1, Markenzeile 2) = 45; Abschnitt 54 = 1 Leerzeile + 3 Zeilen Kopf (Überschrift, Leerzeile, Absatz) + 1 Leerzeile + 4 Blöcke × 7 Zeilen (Überschrift, Leerzeile, zwei Zitatzeilen, Leerzeile, Kette, Leerzeile) + 32 Zeilen Schluss (54.5: 15, eine Leerzeile, 54.6: 16) = 65; 45 + 65 = 110. Abschnitt 54 steht nachher in Z. 11518–11581.

**A5. Nachweis:** wie TB-132 A5, dort nach TB-130 A5 und TB-129 A5 (die Liste der Nachweise steht in TB-129), mit `docs/belege/TB-132/a5_*` als Vorlage, unabhängig vom Einfügeskript, und diesen Werten: R-Diff **4/4** rc 0 (Quelle Z. 156–166 gegen 54.1–54.4), Mutationsprobe an einer Kopie rc 1 · Zitate (Kopf und Schluss aus diesem Auftrag, ⟨S0⟩ und ⟨DATUM⟩ ersetzt) 2/2 rc 0 · Überschriften und Ketten 4/4 · Marken 15/15 gegen Anhang A (⟨DATUM⟩ ersetzt), je mit der Folgezeile und der Zeile nachher; keine Markenzeile doppelt · numstat des Registers **`110	0`** · Zeilenzahl nachher 11581 · Abschnitt 10 und ERZEUGT-Block bytegleich gegen `0b_*_vorher.txt` · `registerbericht.py --pruefen` nachher = vorher · Sonde: JSON ohne `zeilen` nachher = vorher, (ii) 0, „Listentext wie bei Erzeugung: ja“ · `herkunft.register()` nachher ≠ vorher, `fehlend []`, 23 Teile, der neue Wert nur im Ergebnis (42.5) · `test_vorregistrierung` am echten Register vor dem Commit, ohne Zeitgrenze, 196/196 (Vorlage `docs/belege/TB-132/test_vorregistrierung.sh`). Ist ein Nachweis am echten Register rot: Diff als `docs/belege/TB-136/abbruch_register.diff` sichern, Register mit `git checkout -- docs/VORREGISTRIERUNG_neuselektion.md` zurücksetzen, Abbruch. **Das Register wird nur committet, wenn alle Nachweise grün sind.** sha256 und md5 des Registers nachher stehen im Ergebnis, zusammen mit ⟨S0⟩ und ⟨DATUM⟩; der steuernde Chat baut das Soll mit demselben Einfügeskript und diesen zwei Werten nach und vergleicht.

Die Zeilen der 15 Marken nachher (Markenzeile 1; sie hängen weder am Datum noch an ⟨S0⟩; Soll für `a4_eintrag_daten.json`, `a5_marken.py` und C2):

| Nr | Registerstelle | nach Z. (alt) | Marke Z. (neu) |
|---|---|---|---|
| 1 | 16.6 | 2348 | 2350 |
| 2 | 17.5 | 2840 | 2845 |
| 3 | 48.1 (R33) | 10795 | 10803 |
| 4 | 48.2 (R34) | 10802 | 10813 |
| 5 | 48.4 (R36) | 10816 | 10830 |
| 6 | 48.5 (R37) | 10826 | 10843 |
| 7 | 48.7 (R39) | 10846 | 10866 |
| 8 | 48.14 (R46) | 10895 | 10918 |
| 9 | 51.5 (R60) | 11239 | 11265 |
| 10 | 52.2 (R64) | 11331 | 11360 |
| 11 | 53.1 (R66) | 11385 | 11417 |
| 12 | 53.3 (R68) | 11399 | 11434 |
| 13 | 53.4 (R69) | 11406 | 11444 |
| 14 | 53.5 (R70) | 11413 | 11454 |
| 15 | 53.9, nach der Tabelle | 11454 | 11498 |

Commit `TB-136 A: Register 54 (R74–R77 zeichengleich, Tatsachennotizen 04a), Marken`, pushen. **Das ist der einzige Commit, der das Register ändert.**

## Schritt B — BACKLOG (5b)

Verfahren wie TB-132 Schritt B, dort nach TB-130 Schritt B und TB-129 Schritt B (Vorlage `docs/belege/TB-132/b_einfuegen.py` und `b_vergleich.py`; Belege `b_einfuegung.txt`, `b_numstat.txt`, `b_vergleich.txt`): Anker vorher zählen (Soll genau 1, in 0a und 0d schon geprüft; sonst nicht ausführen, vermerken, weitermachen), Text aus **diesem Auftrag** einfügen, erste Textzeile nachher zählen (Soll 1), numstat zweite Spalte 0, Bytevergleich des Blocks.

#### E1 — Abschnitt 5: Bewertung von Fable 04a (5b)

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile** (genau eine Leerzeile davor und danach; eine vorhandene wird nicht verdoppelt)

```
### Aus Fable 04a (04.10.2026) — Bewertung nach 5b, eingetragen mit TB-136

- **Bewertung 04a:** Fable ist mit allen drei Fragen einverstanden. R74–R77 stehen seit TB-136 im Register, Abschnitt 54, mit 15 Marken am alten Ort; Befunde in 54.5, Offenes in 54.6.
- **An Fable, vor dem Bau der Attribution:** Die Voraussetzung zu R75 (a) trifft im Wortlaut nicht: Der Kern (`research/mtm_drawdown/mtm_kern.py`) bildet keine Tagesrendite (54.5, 54.6 Nr. 2). Die Meldung geht an Fable, bevor der Zellen-Erzeuger die Attribution baut; die Anforderung gehört in die Anforderungsliste des Zellen-Erzeugers (TB-135).
- **Vor dem signierten Tag:** Verfahrensmessung nach R74 (e) in der Lock-Umgebung am Snapshot, zusammen mit der Messung nach R72 (d) (54.6 Nr. 1).
- **Fassung des Kalenderpakets:** `eingaben.json` (TB-47) nennt `paket_vorhanden` 5.4.0, der Lock 4.6.1 (54.6 Nr. 8).
- **An Fable, nächste Anfrage, zur Kenntnis:** die zwei Marken des steuernden Chats an 48.1 (R33) und 48.14 (R46) und die sechs sinngemässen Verweise (54.6 Nr. 6 und 7).
- **Fables Chat:** Er stand nach einer einzigen Anfrage bei 468 406 (rot). Das ist ein Befund zur Probe „ein Fable-Chat je Anfrage“ (F4); die nächste Anfrage geht an einen neuen Chat.
- **Für TB-133:** Die Suche der Ablage liefert Ausschnitte gesperrter Dateien (`BACKLOG.md`).
```

Soll numstat: `10	0` (9 Zeilen des Blocks und eine Leerzeile danach). Der Anker steht vorher in Z. 286; davor steht in Z. 285 schon eine Leerzeile.

## Schritt C — Registerkopie, Index, Dialog-Index

**C1. Registerkopie:** wie TB-132 C1, dort nach TB-130 C1 und TB-129 C1 (die fünf Aufrufe stehen in TB-129; Vorlage `docs/belege/TB-132/c1_registerkopie.sh`; je Ausgabe und rc nach `c1_*.txt`). Soll: rc 0 je Aufruf; 55 Abschnittsdateien `_00` bis `_54`. Schreiblauf mit rc 2 oder 3 oder `--pruefen` mit rc ≠ 0 ⇒ festhalten, Kopien nicht committen, melden (kein Abbruch; C2 und C3 entfallen dann). **Erwartet ist ein fünfter Teil** (gerechnet, am Werkzeug nachzumessen): Das Werkzeug schneidet bei jedem Lauf von Abschnitt 0 an, gierig, solange Kopf und Abschnitte unter der Grenze von 240 000 B bleiben (`docs/werkzeuge/registerkopie.py` Z. 124–137; vom Gegenleser des steuernden Chats am Gerät gelesen und nach diesem Verfahren gerechnet, das Werkzeug nicht ausgeführt). Danach bleiben T1 bis T3 gleich zugeschnitten (0–22, 23–36, 37–42), T4 bleibt 43–53 mit rund 234 587 B (vorher 232 545 B), und Abschnitt 54 steht allein in T5 mit rund 24 706 B (der Gegenleser rechnete 24 580 B an der Fassung vor der Korrektur von 54.0, 54.5 und 54.6; die Korrektur bringt 126 B dazu; Kopf einer Teildatei mit 236 B angesetzt). Die Datei `docs/projektfuehrung/REGISTER_KOPIE_teil5.md` ist dann neu und unverfolgt; sie gehört in den Commit B/C. Die Teilgrenzen und Grössen aus `c1_registerkopie.txt` stehen im Ergebnis. Weicht der Zuschnitt ab (ein Abschnitt 0–53 wechselt den Teil, oder es entsteht kein fünfter Teil): im Ergebnis melden, kein Abbruch; C2 führt dann die Teil-Nummern in der Spalte T des Index nach, wo sich die Zuordnung eines Abschnitts ändert (so geschehen in TB-126, Pflegezeile des Index; Vorlage `docs/belege/TB-126/c2_*`).

**C2. `docs/projektfuehrung/REGISTER_INDEX.md` nachziehen**, nach der Bauart von TB-132 C2, dort nach TB-130 C2 und TB-129 C2 (Vorlagen `docs/belege/TB-132/c2_*`): Kopf (Commit, „Abschnitte 0–54“, Zeilenzahl, sha256, „nachgezogen in … TB-132 (Fable 02c) und TB-136 (Fable 04a)“, der Verweis auf die Abschnittsdateien bis `_54.md`, die Zahl der Teile in Index Z. 5: `REGISTER_KOPIE_teil1–4.md` wird zur Zahl aus `c1_registerkopie.txt`, erwartet `REGISTER_KOPIE_teil1–5.md`, das Datum des Laufs statt eines festen Datums) · „Wie gemessen“ (Zahlen je Art und Belegpfad neu aus `c1`) · Abschnittstabelle mit neuer Zeile 54 und der Teil-Zuordnung · der Absatz „*Frühere Vierteilung* (… „T1“ … „T4“ …)“ unter der Abschnittstabelle (Index Z. 75): Die Liste nach „):“ nennt die Teile aus `c1_registerkopie.txt`, erwartet fünf, der letzte T5 mit Abschnitt 54 allein; der Kopf des Absatzes („*Frühere Vierteilung* (… „T1“ … „T4“ …)“) bleibt zeichengleich, auch wenn die Liste danach fünf Teile nennt: An diesem Literal hängen drei übernommene Skripte (`c2_index_eintraege.py` Z. 153, `c2_index_pruefen.py` Z. 24, `c2_index_zeilen.py` Z. 42; Gegenleser). Dass die Bezeichnung nicht mehr zur Zahl der Teile passt, steht im Ergebnis unter „für später“ (TB-133). Was die Sitzung an Index Z. 5 und in diesem Absatz genau geschrieben hat, steht im Ergebnis · alle Zeilenangaben „Z. n“ auf den neuen Stand (`c2_index_zeilen.py ⟨S0⟩ <commit_A>`) · die Einträge der folgenden Liste (Nr. 1 bis 9) · neuer Abschnitt `## 9. Die Marken aus Fable 04a (TB-136)` in der Form von Abschnitt 8, mit den 15 Marken und ihren Zeilen nachher, vor der letzten Trennlinie `---` und dem Pflegeblock · Pflegezeile. Die Pflegezeile nennt den Titel des Blocks aus C3 nicht wörtlich (sonst zählt C3 vorher 1 statt 0; Lehre aus TB-130).

`c2_index_eintraege.py` aus TB-132 besteht fast ganz aus Text für 02c. Die neuen Texte sind diese; „alt“ ist der Anker, der im Index genau einmal vorkommen muss (nach `c2_index_zeilen.py`; an der Kopie vom Stand `d781f1b` gemessen: je 1), `{Zn}` ist die Zeile der Marke Nr. n nachher (`a4_eintrag_daten.json`; Soll in A5), `{T}` der Teil, in dem der Abschnitt nachher liegt (`c1_registerkopie.txt`). PRÄZISIERT steht fett, ERGÄNZT nicht (Regel des Index).

1. **Tabelle 3, Zeile 2d** (Index Z. 137). alt: `| **2d** Embargo | 15.4 (d) | Z. 1496 ERSETZT durch 16.6 → Z. 2347 PRÄZISIERT durch R37 (48.5) | **16.6** (T1) **mit** 48.5 R37 (T4) |` — neu: `| **2d** Embargo | 15.4 (d) | Z. 1496 ERSETZT durch 16.6 → Z. 2347 PRÄZISIERT durch R37 (48.5) → Z. {Z1} **PRÄZISIERT durch R75 (54.2)** | **16.6** (T1) **mit** 48.5 R37 (T4) und 54.2 R75 (a) ({T}) |`
2. **Tabelle 3, Zeile 5f** (Index Z. 156). alt: `| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1) |` — neu: `| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1); Z. {Z2} ERGÄNZT durch R74 (54.1): Name des Handelskalenders ({T}) |`
3. **Tabelle 4, Zeile „48 aus 29b“** (Index Z. 202; Zeilenanfang `| 48 aus 29b |`). Vor dem schliessenden ` |` anhängen: `; 48.1 R33 **PRÄZISIERT durch R75 (54.2)** (Z. {Z3}, vom steuernden Chat nach R65 (a) bestimmt); 48.2 R34 ERGÄNZT durch R75 (54.2) (Z. {Z4}); 48.4 R36 **PRÄZISIERT durch R75 (54.2)** (Z. {Z5}); 48.5 R37 **PRÄZISIERT durch R75 (54.2)** (Z. {Z6}); 48.7 R39 ERGÄNZT durch R75 (54.2) (Z. {Z7}); 48.14 R46 ERGÄNZT durch R75 (54.2) (Z. {Z8}, vom steuernden Chat nach R65 (a) bestimmt); 48.20 R52: Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3), zwölf gezählte Fälle (ohne Marke, R77 (c))`
4. **Tabelle 4, Zeile „51 aus 01a“** (Index Z. 205; Zeilenanfang `| 51 aus 01a |`). Anhängen: `; 51.5 R60 **PRÄZISIERT durch R75 (54.2)** (Z. {Z9})`
5. **Tabelle 4, Zeile „52 aus 02a“** (Index Z. 206; Zeilenanfang `| 52 aus 02a |`). Anhängen: `; 52.2 R64 **PRÄZISIERT durch R75 (54.2)** (Z. {Z10})`
6. **Tabelle 4, Zeile „53 aus 02c“** (Index Z. 207; Zeilenanfang `| 53 aus 02c |`, Zeilenende `| – |`). Das `–` der letzten Spalte ersetzen durch: `53.1 R66 **PRÄZISIERT durch R74 (54.1)** (Z. {Z11}); 53.3 R68 **PRÄZISIERT durch R75 (54.2)** (Z. {Z12}); 53.4 R69 ERGÄNZT durch R75 (54.2) (Z. {Z13}); 53.5 R70 **PRÄZISIERT durch R77 (54.4)** (Z. {Z14}); 53.9, Zeile „R66 (53.1) (b)“ ERGÄNZT durch R74 (54.1) (Z. {Z15})`
7. **Tabelle 4, neue Zeile** direkt nach „53 aus 02c“: `| 54 aus 04a | {T} | R74–R77 (54.1–54.4); 54.5 Voraussetzungen und Befunde; 54.6 Offenes | – |` (in der zweiten Spalte die Nummer des Teils ohne „T“, wie in den Zeilen darüber).
8. **Neuer Abschnitt 9**, vor dem Anker aus Leerzeile, `---`, Leerzeile und `**Pflege:**` (zählt 1): die Zeile `## 9. Die Marken aus Fable 04a (TB-136)`, Leerzeile, der Vorspann unten, Leerzeile, die Markentabelle.
9. **Pflegeblock.** alt: `Zuletzt nachgezogen in TB-132 (04.10.2026):` — neu: `In TB-132 (04.10.2026):`. Am Ende des Blocks neu, in der Form der Zeile zu TB-132: „Zuletzt nachgezogen in TB-136 (Datum des Laufs): Zeilenangaben mit `docs/belege/TB-136/c2_index_zeilen.py` vom Stand `ee43f5f` auf den Commit von Schritt A umgeschrieben (jede Zahl in Listen und Bereichen); 54 kommt zu {T}; Abschnittstabelle aus den Köpfen der Abschnittsdateien; Einträge mit `docs/belege/TB-136/c2_index_eintraege.py`; neuer Abschnitt 9 mit den 15 Marken und zwei Indexzeilen nach R77 (b) und (c) (`c3_indexzeilen.py`).“

Vorspann von Abschnitt 9 des Index (ein Absatz, Zeilenumbruch wie in Abschnitt 8):

```
Alle 15 Marken, die TB-136 gesetzt hat (alle am alten Ort: 13 nach R77 (a), zwei an 48.1 (R33) und 48.14 (R46), vom steuernden Chat nach R65 (a) bestimmt), in der Reihenfolge des Registers. Erzeugt mit `docs/belege/TB-136/c2_index_04a.py` aus `docs/belege/TB-136/c1_marken.txt` (Zeile, Art, Teil) und Anhang A des Auftrags TB-136 (alter Ort), nicht abgetippt. In Tabelle 3 und 4 oben stehen sie zusätzlich an ihrer Stelle. Keine Marke tragen Abschnitt 9, Abschnitt 10 und der ERZEUGT-Block von Abschnitt 3; ohne Marke bleiben 48.20 (R52) (Indexzeile darunter), 53.10, 50.2, 29.3, 41.3, 35.1 und 27.2 (R77 (c)).
```

Soll der Markentabelle von Abschnitt 9 (Spalten wie in Abschnitt 8; Zeile und Art misst `c1_marken.txt`, die Spalte T kommt aus dem Zuschnitt und trägt hier kein Soll; Art: PRÄZISIERT ⇒ `MARKE`, ERGÄNZT ⇒ `MARKE+`):

| alter Ort (Anhang A) | Marke | Wort | durch | Art | T |
|---|---|---|---|---|---|
| 16.6 | Z. 2350 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 17.5 | Z. 2845 | ERGÄNZT | R74 (54.1) | MARKE+ | {T} |
| 48.1 (R33) | Z. 10803 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 48.2 (R34) | Z. 10813 | ERGÄNZT | R75 (54.2) | MARKE+ | {T} |
| 48.4 (R36) | Z. 10830 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 48.5 (R37) | Z. 10843 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 48.7 (R39) | Z. 10866 | ERGÄNZT | R75 (54.2) | MARKE+ | {T} |
| 48.14 (R46) | Z. 10918 | ERGÄNZT | R75 (54.2) | MARKE+ | {T} |
| 51.5 (R60) | Z. 11265 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 52.2 (R64) | Z. 11360 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 53.1 (R66) | Z. 11417 | PRÄZISIERT | R74 (54.1) | MARKE | {T} |
| 53.3 (R68) | Z. 11434 | PRÄZISIERT | R75 (54.2) | MARKE | {T} |
| 53.4 (R69) | Z. 11444 | ERGÄNZT | R75 (54.2) | MARKE+ | {T} |
| 53.5 (R70) | Z. 11454 | PRÄZISIERT | R77 (54.4) | MARKE | {T} |
| 53.9, nach der Tabelle | Z. 11498 | ERGÄNZT | R74 (54.1) | MARKE+ | {T} |

`registerkopie.py --marken` zählt in Abschnitt 54 voraussichtlich drei Zeilen mit, die keine Marken sind: die Blockzeile von R77 (sie nennt „PRÄZISIERT durch“), die Blockzeile von R76 (sie nennt „ERSETZT-Marke“) und 54.6 Nr. 6 (sie nennt „PRÄZISIERT durch R75 (c)“); dazu drei Überschriften mit Rückverweis (54.1, 54.2, 54.4). Erwartet nach der Beschreibung im Kopf des Index („Wie gemessen“), nicht am Werkzeug gemessen und kein Soll: `MARKE` 84 + 9 + 2 = 95, `MARKE+` 121 + 6 + 1 = 128, `UEBERSCHRIFT` 88 + 3 = 91. Wie in TB-132: festhalten, im Index nicht als Marke führen, im Ergebnis unter „Für Fable“ nennen.

**C3. Indexzeilen aus Fable 04a (R77 (b) und (c)).** Ein eigener Block `### Indexzeilen aus Fable 04a` im neuen Abschnitt 9 des Index, nach der Markentabelle, mit genau diesen zwei Zeilen (zeichengleich). Vorher zählen: `Indexzeilen aus Fable 04a` zählt 0. Die Indexzeile zu 17.5 in Abschnitt 8 des Index (Fable 02c) bleibt stehen, wie sie ist; sie ist für R66 richtig (R77 (b)).

```
- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1) und R74 (54.1). Zu R74 mit Marke (R77 (a) und (b), 54.4); zu R66 gilt die Indexzeile aus Fable 02c weiter (R70 (b), 53.5).
- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R76 (54.3): zwölf gezählte Fälle bis zur Antwort 02c. Ohne Marke (R77 (c), 54.4). Lesart des steuernden Chats zu R77 (c), vorläufig; der Index ist kein Registertext.
```

**C4. Dialog-Index.** Die Datei `docs/belege/TB-136/c4_handfelder.json` mit genau diesem Inhalt anlegen:

```
{"02c": {"offen": "nein"}, "04a": {"frage": "Welcher Kalender des Pakets ist der Handelskalender der Aktien-Tagesreihe und wo steht sein Name, bleiben die Proben nach R60 (c) und R36 im Deckelfall und was heisst Attribution je Position, und sind es zwölf gezählte Fälle der Klasse „Bestand behauptet statt Voraussetzung genannt“?", "entscheidung": "Alle drei Fragen einverstanden. Handelskalender ist der Kalender „NYSE“ des Pakets in der Fassung des Locks, gebunden ist der Name; vor dem Tag wird in der Lock-Umgebung am Snapshot gemessen (R74). Attribution heisst Herausrechnen über dem Kapitalstand des einen Pfads; jede Tagesreihe führt ein zweites Spaltenpaar, die Zeile der Bestätigungsperiode kommt aus ihm, die Proben bleiben ohne Ausnahme, die Abnahme führt den Deckelfall herbei (R75). Zwölf gezählte Fälle (R76). 13 Marken, 17.5 trägt jetzt eine (R77). Die Voraussetzung zu R75 (a) trifft im Wortlaut nicht (54.5).", "offen": "ja"}}
```

Dann, wie TB-132 C4, `trading-env/bin/python3 docs/werkzeuge/dialog_index.py --handfelder docs/belege/TB-136/c4_handfelder.json`, danach `--pruefen` ⇒ `c4_dialog_index.txt` (Vorlage `docs/belege/TB-132/c4_dialog_index.sh`). Soll: `--pruefen` rc 0; 55 Antworten; Zeile `04a` mit Fundstelle 54 und Status „offen“ (offen = ja: R74 (e) verlangt eine Messung vor dem Tag, die Meldung zu R75 (a) steht aus, 54.6); Zeile `02c` mit Fundstelle 53 und Status „registriert“ (ihre offenen Punkte sind durch 04a beantwortet oder laufen in 54.6 weiter), Frage und Entscheidung unverändert. Trägt die neue Zeile einen anderen Schlüssel als `04a`: den Schlüssel des Werkzeugs in `c4_handfelder.json` einsetzen, im Ergebnis nennen (kein Abbruch). `git diff --numstat` festhalten; weitere geänderte Zeilen im Ergebnis nennen (kein Abbruch).

Commit `TB-136 B/C: BACKLOG, Registerkopie, Index, Dialog-Index`, pushen.

## Schritt D — Abgabe

**D1.** `docs/ERGEBNIS_TB-136_register_fable_04a.md`, Bau wie ERGEBNIS_TB-132 (dort wie ERGEBNIS_TB-130 und ERGEBNIS_TB-129), ohne die Rubrik „Probe in der Lock-Umgebung“: Kopfzeile, Stand und Commits, ⟨S0⟩ und ⟨DATUM⟩ im Wortlaut, Kurz-Tabelle je Schritt (Soll | Ist), **Nachmessung der Voraussetzungen** (0e: rc, die Zeilen der Ausgabe, das Feld `kalender` im Wortlaut), Markentabelle (15 Marken mit Zeile nachher), Register nachher (Zeilen, sha256, md5), `herkunft.register()` vorher und nachher, **Für Fable** (54.6 Nr. 2, 6, 7, 9 und 10; jede Reibung beim Setzen), **Nicht getan** (54.6; die Ablage macht der steuernde Chat), **In einfacher Sprache**.

**D2. Journal:** wie TB-132 D2: Block nach dem letzten Buchstabenblock von `docs/projektfuehrung/JOURNAL.md`, vor `## Wiederkehrende Lehren`. Kennung vorher messen (erwartet **EE**), mit Quellenzeile. Den Block schreibt die Sitzung, in der Gliederung des Blocks ED (`docs/belege/TB-132/d2_journal_block.md`): Kopfzeile, Quelle, „Was gemessen ist“, „Was aus dieser Sitzung an Regeln bleibt“, „Was offen bleibt“, Schlusszeile.

**D3.** wie TB-132 D3: Abgabe-Commit `TB-136 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach `git status --porcelain` in den Scratch und als `docs/belege/TB-136/d3_porcelain.txt`, kleiner letzter Commit, pushen.

### Übernommene Skripte

Die Skripte der Sitzung ausser Prüfskript und Einfügeskript stehen nicht in diesem Auftrag. Die Sitzung übernimmt sie aus `docs/belege/TB-132/` nach `docs/belege/TB-136/` und stellt die festen Stellen um: Abschnitt 53 → 54, R66–R73 → R74–R77, 02c → 04a, 21 → 15, 8 → 4, TB-132 → TB-136, Journal ED → EE. Die Zeilennummern der vier Skripte mit „gemessen“ sind an Kopien vom Stand `d781f1b` gemessen; die mit „Zerlegung“ nennt die Zerlegung des steuernden Chats, die mit „Gegenleser“ sein Gegenleser (beide am Gerät gelesen); sie sind an der Datei zu prüfen. Jedes Skript, das ein Datum braucht, bekommt ⟨DATUM⟩ als Argument; keines trägt ein festes Datum.

| Skript (Zeilen) | feste Stellen in TB-132 | in TB-136 | Zeilennummern |
|---|---|---|---|
| `0b_ausgang.sh` (53) | Belegordner, Abbild-Pfad, Quelle 02c; dazu Sollwerte als Text in `echo`-Zeilen: Z. 13 Register (`11313 Zeilen`, sha256 `a7496780...`, md5 `80af174f...`), Z. 19 `register()` (`4caf0179...`), Z. 36 Quelle (`6aad30ec...`, `30216 B`) | Belegordner TB-136, Quelle 04a; Abbild-Pfad bleibt. Sollwerte neu: Z. 13 `11471 Zeilen`, sha256 `9a2cefb7...`, md5 `1ce393ae...`; Z. 19 `66480962...`; Z. 36 `856b2c15...`, `29195 B`. Register und Quelle an den Kopien gerechnet; der Wert zu `register()` aus `docs/ERGEBNIS_TB-132_register_fable_02c.md` Z. 72 | Zerlegung; die drei `echo`-Zeilen: Gegenleser |
| `a4_probelauf.sh` (20) | Z. 6 `BL`; Z. 11 Auftrags- und Quellpfad; Z. 12 der Aufruf des Einfügeskripts | `docs/belege/TB-136`; neue Pfade; der Aufruf in Z. 12 bekommt `--datum ⟨DATUM⟩` | Zerlegung (Z. 11); Gegenleser (Z. 6, Z. 12) |
| `a5_r_diff.py` (66) | Z. 20 Quelle und `134, 156`; Z. 39 `### 53\.`; Z. 55 und 66 `range(66, 74)`; Z. 65 `/8`; Z. 66 auch `gut == 8` | Quelle 04a und `156, 166`; `### 54\.`; `range(74, 78)`; `/4`; `gut == 4` | Zerlegung; `gut == 8`: Gegenleser |
| `a5_zitate.py` (70) | Z. 31–32 und 49 `## 53. `, `### 53.9 `, `### 53.1 ` | `## 54. `, `### 54.5 `, `### 54.1 `; im Kopf ⟨S0⟩ und ⟨DATUM⟩ ersetzen (Datum als Argument) | Zerlegung |
| `a5_mutation.py` (21) | Block R66 unter 53.1 | Block R74 unter 54.1 | Zerlegung |
| `a5_marken.py` (100) | Z. 20 `BL`; Z. 21 Auftragspfad; Z. 25 Muster `^\| 53\.\d \|`; Z. 49 `!= 8`; Z. 52 `TB-132, `; Z. 73–74 viermal `21`; Texte in Z. 2, 9, 10, 30 | `docs/belege/TB-136/`; neuer Pfad; `^\| 54\.\d \|`; `!= 4`; `TB-136, `; `15`. Aufruf bleibt `<S0> <datum> [<register>]`; das Skript ersetzt ⟨DATUM⟩ schon (Z. 57). Tabelle 1 behält die Spalte „Zeichen“ (Z. 26 bleibt) | gemessen |
| `a5_nachweis.sh` (11), `test_vorregistrierung.sh` (13) | Belegordner | TB-136 | Zerlegung |
| `b_einfuegen.py` (61), `b_vergleich.py` (32) | Auftragspfad, Belegpfad; sonst aus dem Abschnitt E1 des Auftrags gelesen | neue Pfade | Zerlegung |
| `c1_registerkopie.sh` (17) | Belegordner | TB-136 | Zerlegung |
| `c2_index_zeilen.py` (47) | nichts Inhaltliches (Aufruf `<S0> <commit_A>`) | — | Zerlegung |
| `c2_index_02c.py` (31) | Z. 15 `"TB-132, 04.10.2026"`; Z. 27 `21` | als `c2_index_04a.py`: `"TB-136, "` und ⟨DATUM⟩ als Argument; `15`; Ausgabe `c2_index_04a_tabelle.md` | Zerlegung |
| `c2_index_eintraege.py` (159) | Z. 22 `BL`; Z. 23 Tabellendatei; Z. 25 `range(1, 22)`; Z. 40 `range(54)`; Z. 46 `ab[53]`; Z. 54 `t53` mit `53`; Z. 59 `range(53)`; Z. 61–99 die Liste `E` (Kopf mit festem Datum in Z. 66, „Wie gemessen“, Tabelle 3, Abschnitt 8, Pflege); Z. 108–126 die Liste `ANH` (Tabelle 4); Z. 140–141 neue Zeile nach „52 aus 02a“; Z. 151–152 `"52"` und `tabzeile(53)` | `range(1, 16)`; `range(55)`; `ab[54]`; Teil von 54; `range(54)`; die Texte aus C2 (Liste Nr. 1 bis 9), das Datum des Laufs statt `04.10.2026`; neue Zeile nach „53 aus 02c“; `"53"` und `tabzeile(54)` | gemessen |
| `c2_index_pruefen.py` (85) | Zahlen 14/12/21 je Index-Abschnitt 6/7/8, Abschnitte 0–53; Z. 43–45 je Auftrag ein festes Datum (für TB-132 `"04.10.2026"`); Z. 55 Auftragspfad; Z. 57 Marke `**C3. Indexzeilen statt Marken (R70 (b)).**`; Z. 58–61 `## 8. …` und `### Indexzeilen aus Fable 02c`; „drei“ in Z. 7 und Z. 54; Z. 62 Ausgabetext `(Abschnitt 8)`; Z. 80 `!= 54`; Z. 24 `startswith("*Frühere Vierteilung*")` bleibt | dazu 15 für Abschnitt 9, mit ⟨DATUM⟩ als Argument statt eines festen Datums (der Aufruf nimmt heute nur `<S0>`, neu `<S0> <datum>`); neuer Pfad; der fette Anfang von C3 in diesem Auftrag; `## 9. Die Marken aus Fable 04a (TB-136)`, `### Indexzeilen aus Fable 04a` und „zwei“; Ausgabetext `(Abschnitt 9)`; `!= 55`; Abschnitte 0–54 | Zerlegung; Z. 7, 24, 43–45, 54, 55, 57, 58–62, 80: Gegenleser |
| `c3_indexzeilen.py` (35) | Z. 14 Auftragspfad; Z. 16 Marke `**C3. Indexzeilen statt Marken (R70 (b)).**`; Z. 18 `== 3`; Z. 20 `KOPF8`; Z. 22–33 Titel `Indexzeilen aus Fable 02c` und `/3` | neuer Pfad; der fette Anfang von C3 in diesem Auftrag (von `**C3.` bis `(c)).**`); `== 2`; `## 9. Die Marken aus Fable 04a (TB-136)`; `Indexzeilen aus Fable 04a` und `/2` | gemessen |
| `c4_dialog_index.sh` (17) | Z. 6 `BL`; Z. 8 Auftragspfad; Z. 14 `for b in 02a 02b 02c` | TB-136; neuer Pfad; `for b in 02c 04a` | gemessen |
| `d2_journal.py` (15) | Z. 11–12 `"EC"`, `"## ED "` | `"ED"`, `"## EE "` | Zerlegung |

## Abbruchkriterien (nur für diesen Gegenstand)

Wie TB-132 („Abbruchkriterien“), ohne das Datum und ohne die Probe, mit diesen Werten:

- 0a: Der Arbeitsbaum weicht ab; ein sha256 der zwei Skripte weicht ab; das Prüfskript gibt nicht rc 0 (auch: die Freigabe ist nicht eingesetzt). Abbruch ohne Commit.
- Ein Ausgangswert aus 0b mit Soll weicht ab; der Basislauf in 0c (falls nötig) ist nicht 196/196.
- 0d: rc ≠ 0 (Marken, Quelle, „noch nicht vergeben“, Fundstellen, Zählungen, Dateien, Freigabe; auch eine einzelne Marke).
- 0e: `rc 3` (V1 trifft nicht zu) ⇒ melden, **nicht eintragen**; `rc 1` oder eine Fehlermeldung ⇒ Abbruch ohne Eintrag, mit Meldung.
- A4: Eine Wache des Einfügeskripts schlägt an (Voraussetzung, sha256, Anker, Platzhalter); der Probelauf und der echte Lauf nennen nicht dieselbe Zeile `sha256 nachher:`; das Register ist nach dem echten Lauf nicht `cmp`-gleich mit der Kopie.
- Ein Nachweis aus A5 ist rot, jeder der dort genannten.
- Eine Datei ausserhalb der Freigabetabelle müsste geändert werden.
- `git push` scheitert zweimal.

**Kein Abbruch:** das Datum (die Sitzung läuft an jedem Tag; wechselt der Tag zwischen 0a und A4, gilt das Datum aus `a4_datum.txt`) · der BACKLOG-Anker ≠ 1 erst in Schritt B, also nach bestandenem 0d (nicht einfügen, nennen) · `Indexzeilen aus Fable 04a` zählt in C3 nicht 0 (nicht einfügen, nennen) · `registerkopie.py` mit rc ≠ 0 (Kopien nicht committen, nennen; C2 und C3 entfallen, C4 nicht) · ein fünfter Teil der Registerkopie (erwartet; `REGISTER_KOPIE_teil5.md` in den Commit B/C) oder ein anderer Zuschnitt, als C1 ihn nennt (Teilgrenzen im Ergebnis melden; wechselt ein Abschnitt 0–53 den Teil, die Spalte T im Index nachführen) · ein anderer Schlüssel als `04a` im Dialog-Index (einsetzen, nennen) · weitere geänderte Zeilen im Dialog-Index (nennen) · eine Reibung zwischen Fable-Text und Code oder Register (unter „Für Fable“ nennen).

**Bei Abbruch nach dem Commit von Schritt 0:** wie TB-132: committen, was an Belegen da ist, **nie** `JOURNAL.md` mit Platzhalter, Grund in `docs/belege/TB-136/abbruch.txt`, pushen, melden. Kein Registertext mit einem Befund, den dieser Auftrag nicht vorsieht.

## In einfacher Sprache

Fable hat am 04.10. vier Regeltexte geschrieben (R74–R77). Sie legen fest, welcher Börsenkalender für die tägliche Wertreihe der Aktien-Bots gilt, wie eine alte, noch offene Position aus der Bestätigungszeit herausgerechnet wird und wie viele Fehler einer bestimmten Art bisher gezählt sind. Die Sitzung sichert zuerst die Dateien, die der steuernde Chat bereitgelegt hat, ins Repo (Commit und Push). Dann misst sie am Betriebsrechner nach, ob einige Stellen im Code und im Register so aussehen, wie die Vormessung sie beschreibt. Nur wenn das stimmt, kopiert sie die vier Texte per Skript ins Register, Zeichen für Zeichen, als Abschnitt 54, und setzt 15 Hinweise an alten Stellen. Dazu kommt eine Tabelle mit dem, was nachgemessen wurde, und eine Liste dessen, was offen bleibt. Das Datum des Eintrags ist der Tag, an dem die Sitzung einträgt; sie kann an jedem Tag laufen. Am Code ändert sich nichts.

---

## Anhang A — TB-136: Überschriften, Ketten, Marken, Fundstellen, Prüfskript und Einfügeskript (Vorlage für die Mac-Sitzung)

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `ee43f5f` (11 471 Zeilen, sha256 `9a2cefb7…`), HEAD `d781f1b`. Gebaut am 04.10.2026 von einem Helfer des steuernden Chats mit Skripten, die Ankerzeilen, Einfügestellen und Zeilenanfänge an einer Kopie des Registers messen (sha256 der Kopie wie oben); jeder Anker kommt im Register genau einmal vor. **Alle Zeilennummern gelten am Original, vor jeder Einfügung.** **Massgeblich für Skripte ist der JSON-Block am Ende.**

### Tabelle 1 — Überschriften und Ketten (4)

Die Überschrift ist der Anfang des Blocks bis vor den Satzpunkt. Wo die Zeile länger als 140 Zeichen wäre, ist sie am Ende an einer Wortgrenze mit „…“ gekürzt (54.1, 54.2). Die Kürzungsregel ist an den acht Überschriften von Abschnitt 53 nachgerechnet (8/8 gleich dem Register). Die Ketten folgen den Bausteinen aus TB-132, Tabelle 1; ihre Ortslisten sind aus Tabelle 2 erzeugt.

| x.n | Überschriftzeile (exakt) | Zeichen | Kette (exakt) |
|---|---|---|---|
| 54.1 | `### 54.1 R74 — Präzisierung zu R66 (a) und (b) (53.1) und Ergänzung der Tatsachennotiz in Registertext 5f (17.5) (Name des Handelskalenders…` | 140 | `**Kette:** Marken: 17.5; 53.1 (R66); 53.9, Zeile „R66 (53.1) (b)“. Voraussetzung gemessen: 54.5. Offen: 54.6 Nr. 1, 3 und 8.` |
| 54.2 | `### 54.2 R75 — Präzisierung zu R68 (c) und (d) (53.3), zu 16.6 und R37 (i) (48.5) (Attribution je Position), zu R36 (48.4) und zu R60 (c)…` | 138 | `**Kette:** Marken: 16.6; 48.1 (R33) (vom steuernden Chat bestimmt, 54.6 Nr. 6); 48.2 (R34); 48.4 (R36); 48.5 (R37); 48.7 (R39); 48.14 (R46) (vom steuernden Chat bestimmt, 54.6 Nr. 6); 51.5 (R60); 52.2 (R64); 53.3 (R68); 53.4 (R69). Voraussetzung gemessen: 54.5. Offen: 54.6 Nr. 2 bis 5 und 10.` |
| 54.3 | `### 54.3 R76 — Tatsachennotizen 04a` | 35 | `**Kette:** Marken: keine. Indexzeilen ohne Marke (R77 (c)): 48.20 (R52). Tatsache gemessen: 54.5.` |
| 54.4 | `### 54.4 R77 — Marken zu R74 bis R76; Präzisierung zu R70 (b) (53.5)` | 68 | `**Kette:** Marken: 53.5 (R70). Nach (a) gesetzt: 13 Marken, je in der Kette des Blocks, der sie auslöst. Indexzeilen nach (b): 17.5. Tatsache gemessen: 54.5. Offen: 54.6 Nr. 4, 6 und 7.` |

### Tabelle 2 — Marken (15)

Sortiert nach Einfügestelle; jede Einfügestelle trägt eine Marke. Jede Marke: Leerzeile, Markenzeile 1, Markenzeile 2 `> Eintrag und Stand oben bleiben zeichengleich.` „Zahl“ = `str.count` des Ankers über den ganzen Registertext. „Grund“ nennt den Wortlaut aus R77 (a) oder, bei Nr. 3 und Nr. 8, die Regel R65 (a), die der steuernde Chat angewandt hat. `⟨DATUM⟩` in der Markenzeile ist der Platzhalter für das Datum des Eintrags.

| Nr | Grund | Registerstelle | Anker (Ankerzeile) | Zahl | Einfügestelle | Markenzeile 1 (exakt) |
|---|---|---|---|---|---|---|
| 1 | R77 (a): 16.6 — PRÄZISIERT durch R75, Unterpunkt (a) | 16.6 | `### 16.6 Registertext 2d` (Z. 2300) | 1 | nach Zeile 2348: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **16.6 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (a), TB-136, ⟨DATUM⟩).` |
| 2 | R77 (a): 17.5 — ERGÄNZT durch R74, Unterpunkte (a) und (b) | 17.5 | `### 17.5 Registertext 5f` (Z. 2824) | 1 | nach Zeile 2840: `> weder Bedingung noch Widerlegung.` | `> ⭐ **17.5 ERGÄNZT durch R74 (54.1)** (Fable 04a R74, Unterpunkte (a) und (b), TB-136, ⟨DATUM⟩).` |
| 3 | R65 (a), angewandt vom steuernden Chat: R75 (c) sagt, woraus „Die Zeile der Bestätigungsperiode in zellen.csv (R33, R68)“ gebildet wird; 48.1 trägt für dieselbe Zeile schon die Marke zu R68; R77 (a) nennt den Ort nicht | 48.1 (R33) | `### 48.1 R33` (Z. 10789) | 1 | nach Zeile 10795: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **48.1 R33 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (c), vom steuernden Chat nach R65 (a) bestimmt, TB-136, ⟨DATUM⟩).` |
| 4 | R77 (a): 48.2 (R34) — ERGÄNZT durch R75, Unterpunkt (g) | 48.2 (R34) | `### 48.2 R34` (Z. 10799) | 1 | nach Zeile 10802: `> Quelle des Grundes: 22.2 (Werte des La` | `> ⭐ **48.2 R34 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (g), TB-136, ⟨DATUM⟩).` |
| 5 | R77 (a): 48.4 (R36) — PRÄZISIERT durch R75, Unterpunkte (c) und (d) | 48.4 (R36) | `### 48.4 R36` (Z. 10813) | 1 | nach Zeile 10816: `> Quelle des Grundes: 24.2, 24 (Festlegu` | `> ⭐ **48.4 R36 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkte (c) und (d), TB-136, ⟨DATUM⟩).` |
| 6 | R77 (a): 48.5 (R37) — PRÄZISIERT durch R75, Unterpunkt (a) | 48.5 (R37) | `### 48.5 R37` (Z. 10820) | 1 | nach Zeile 10826: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **48.5 R37 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (a), TB-136, ⟨DATUM⟩).` |
| 7 | R77 (a): 48.7 (R39) — ERGÄNZT durch R75, Unterpunkt (b) | 48.7 (R39) | `### 48.7 R39` (Z. 10837) | 1 | nach Zeile 10846: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **48.7 R39 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (b), TB-136, ⟨DATUM⟩).` |
| 8 | R65 (a), angewandt vom steuernden Chat: R75 (d) und (f) geben der Abnahme nach R46 eine weitere Prüfung und dem Test-Snapshot einen Deckelfall; R77 (a) nennt den Ort nicht | 48.14 (R46) | `### 48.14 R46` (Z. 10892) | 1 | nach Zeile 10895: `> Quelle des Grundes: 27.1, 24.3 (die Re` | `> ⭐ **48.14 R46 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkte (d) und (f), vom steuernden Chat nach R65 (a) bestimmt, TB-136, ⟨DATUM⟩).` |
| 9 | R77 (a): 51.5 (R60) — PRÄZISIERT durch R75, Unterpunkt (d) | 51.5 (R60) | `### 51.5 R60` (Z. 11227) | 1 | nach Zeile 11239: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **51.5 R60 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, ⟨DATUM⟩).` |
| 10 | R77 (a): 52.2 (R64) — PRÄZISIERT durch R75, Unterpunkt (d) | 52.2 (R64) | `### 52.2 R64` (Z. 11313) | 1 | nach Zeile 11331: `> Eintrag und Stand oben bleiben zeichen` | `> ⭐ **52.2 R64 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, ⟨DATUM⟩).` |
| 11 | R77 (a): 53.1 (R66) — PRÄZISIERT durch R74 | 53.1 (R66) | `### 53.1 R66` (Z. 11382) | 1 | nach Zeile 11385: `> Quelle des Grundes: 1c im Wortlaut („a` | `> ⭐ **53.1 R66 PRÄZISIERT durch R74 (54.1)** (Fable 04a R74, TB-136, ⟨DATUM⟩).` |
| 12 | R77 (a): 53.3 (R68) — PRÄZISIERT durch R75 | 53.3 (R68) | `### 53.3 R68` (Z. 11396) | 1 | nach Zeile 11399: `> Quelle des Grundes: R37 (i) („Die Best` | `> ⭐ **53.3 R68 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, TB-136, ⟨DATUM⟩).` |
| 13 | R77 (a): 53.4 (R69) — ERGÄNZT durch R75, Unterpunkt (h) | 53.4 (R69) | `### 53.4 R69` (Z. 11403) | 1 | nach Zeile 11406: `> Quelle des Grundes: R39 mit seinem Gru` | `> ⭐ **53.4 R69 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (h), TB-136, ⟨DATUM⟩).` |
| 14 | R77 (a): 53.5 (R70) — PRÄZISIERT durch R77, Unterpunkt (b) | 53.5 (R70) | `### 53.5 R70` (Z. 11410) | 1 | nach Zeile 11413: `> Quelle des Grundes: R61 (b), erster un` | `> ⭐ **53.5 R70 PRÄZISIERT durch R77 (54.4)** (Fable 04a R77, Unterpunkt (b), TB-136, ⟨DATUM⟩).` |
| 15 | R77 (a): 53.9, Zeile „R66 (53.1) (b)“ — ERGÄNZT durch R74, Unterpunkte (b) und (f) | 53.9, nach der Tabelle | `### 53.9 Voraussetzungen und Befunde` (Z. 11438) | 1 | nach Zeile 11454: `\| R66–R73, Zitate und Verweise \| — \| 98 ` | `> ⭐ **53.9, Zeile „R66 (53.1) (b)“ ERGÄNZT durch R74 (54.1)** (Fable 04a R74, Unterpunkte (b) und (f), TB-136, ⟨DATUM⟩).` |

### Prüfsumme

*Ausgabe des Prüfskripts im Container des Erbauers am 04.10.2026, Aufruf ohne `--arbeitsbaum` und ohne `--trockenlauf`, mit `--datum 04.10.2026`, an einer Kopie dieses Auftrags, in der der Platzhalter der Freigabe durch einen Probetext ersetzt war. Register, Quelle, Anfrage, Eröffnungstext, Index, Dialog-Index und `BACKLOG.md` waren Kopien vom Stand `d781f1b` (sha256 bzw. md5 wie unter „Belegt“); `JOURNAL.md` lag nicht vor und war eine Attrappe mit dem Block ED aus `docs/belege/TB-132/d2_journal_block.md`. Den Trockenlauf am echten Repo über die Geräteanbindung fährt der steuernde Chat vor der Freigabe. Für die Sitzung gilt: Die erste Zeile nennt ihr Datum; die fünf Zeilen von `Marken:` bis `Bloecke:` und die Zeile `Dateien:` bis vor `*.py im Baum` sind Soll; in 0a stehen vor der Zeile `Marken:` die zwei Arbeitsbaum-Zeilen mit `2 (Soll 2)` und `12 (Soll 12)`. Die Zahl `*.py im Baum` ist kein Soll.*

```
Datum des Eintrags: 04.10.2026 (aus --datum)
Marken: 15 an 15 Einfuegestellen
je Abschnitt: 16: 1, 17: 1, 48: 6, 51: 1, 52: 1, 53: 5
Anker mit Zahl 1 (Original): 15 von 15
Anker mit Zahl 1 (nach Simulation): 15 von 15
Bloecke: 4 | Ueberschriften: 4 max. Laenge 140 | gekuerzt: 2
Dateien: 3 | Fundstellen: 45 | Zeilenlisten: 0 | Zaehlungen: 13 | *.py im Baum: 11
rc 0: alles wie angegeben
```

### Prüfskript

`pruefe_anhang_tb136.py`, sha256 des Skripttexts mit Zeilenumbruch am Ende: `2dbc5a55afaecc99c3df35520454720b71dad5ed4d12213f9e91a48532ab15bb`. Abgeleitet aus `docs/belege/TB-132/0d_vorpruefung.py` (dort sha256 `8ef716ac…`): Der Schalter `--probe` und die Datumsprüfung sind entfernt, `--datum` ist neu, die Form der Markenzeile nennt `Fable 04a` und `TB-136`. Liest den JSON-Block unten. Aufruf `trading-env/bin/python3 <skript> <dieser Auftrag> <repo-wurzel> --datum TT.MM.JJJJ [--arbeitsbaum]`; rc 0 = alles wie angegeben, rc 2 = Aufruf unbrauchbar (auch: `--datum` fehlt). Es bricht auch ab, solange der Platzhalter für die Freigabe im Auftrag steht. Der Schalter `--trockenlauf` gehört dem steuernden Chat; die Sitzung benutzt ihn nicht.

```python
#!/usr/bin/env python3
"""Prueft Anhang A von TB-136 gegen das Register am Stand ee43f5f, die Quelle 04a und die Fundstellen fuer 54.5
und 54.6; auf Wunsch den Arbeitsbaum vor Schritt 0. Das Datum des Eintrags steht nicht im Auftrag: es kommt mit --datum.

Aufruf (Python 3.9, nur Standardbibliothek; rein lesend):
  python3 pruefe_anhang_tb136.py <MAC_TB-136_register_fable_04a.md> <repo-wurzel> --datum TT.MM.JJJJ [Schalter]

  ohne Schalter      Freigabe eingesetzt, Register (sha256, Zeilen), Marken (Anker, Einfuegestellen, Form), Quelle (md5,
                     Schnittregel), Ueberschriften, Simulation des Einsetzens, Dateien (md5), Fundstellen,
                     Zaehlungen. Das ist die Vorpruefung 0d.
  --arbeitsbaum      dazu: uncommittete Dateien genau wie im Daten-Block (0a, VOR dem Commit von Schritt 0).
                     Gemessen mit `git --no-optional-locks diff --name-only HEAD` und
                     `git --no-optional-locks ls-files --others --exclude-standard`.
  --datum TT.MM.JJJJ Pflicht. Das Datum des Eintrags; es ersetzt den Platzhalter ⟨DATUM⟩ in den Markenzeilen. Geprueft
                     wird die Form, keine Uhr. Jede Markenzeile 1 im Daten-Block traegt den Platzhalter genau einmal.
  --trockenlauf      NUR fuer den steuernden Chat vor der Sitzung; der Auftrag benutzt diesen Schalter nicht.
                     Uebergeht (a) Zaehlungen in BACKLOG*.md (Leseregel des Helfers),
                     (b) im Arbeitsbaum die Dateien, die erst mit dem Auftrag gelegt werden (Feld "spaeter"),
                     (c) den Platzhalter fuer die Freigabe, solange sie noch nicht eingesetzt ist.
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
datum = None
rest = []
i = 0
while i < len(argv):
    if argv[i] in schalter:
        schalter[argv[i]] = True
    elif argv[i] == "--datum":
        i += 1
        datum = argv[i] if i < len(argv) else None
        if datum is None:
            print("--datum braucht TT.MM.JJJJ"); sys.exit(2)
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
def ende():
    if fehler:
        print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
    print("rc 0: alles wie angegeben"); sys.exit(0)

# ---------------------------------------------------------------- Datum (vom Aufruf, nicht aus dem Auftrag)
try:
    if datum is None or datetime.datetime.strptime(datum, "%d.%m.%Y").strftime("%d.%m.%Y") != datum: raise ValueError
except ValueError:
    print("--datum TT.MM.JJJJ fehlt oder ist kein Datum:", datum); sys.exit(2)
print("Datum des Eintrags: %s (aus --datum)" % datum)
for m in daten["marken"]:
    if m["m1"].count("⟨DATUM⟩") != 1: f("Nr %d: Markenzeile 1 traegt den Platzhalter fuer das Datum nicht genau einmal" % m["nr"])
    m["m1"] = m["m1"].replace("⟨DATUM⟩", datum)
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

FORM = re.compile(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch R(\d+) \(%d\.(\d+)\).*\*\* \(Fable 04a R(\d+)(, .+)?, TB-136, %s\)\.$"
                  % (A, re.escape(datum)))
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
    kern = u["zeile"].split(" ", 2)[2]                      # "R<n> — ..."
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

`a4_eintrag.py`, sha256 des Skripttexts mit Zeilenumbruch am Ende: `99881a1b69b9c72a24948d68b839d1c6664db87005d40c81fc407fd159659ea5`. Abgeleitet aus `docs/belege/TB-132/a4_eintrag.py` (dort sha256 `c75b6e88…`): Die Wachen Datum und Probe sind entfernt, an ihrer Stelle steht die Wache zur Voraussetzung aus R74 (b); `--datum` ist neu und Pflicht; die Zahl der Marken ist 15. Liest Kopf, Schluss und den JSON-Block aus diesem Auftrag und die Blöcke aus der Antwortdatei. Aufruf in A4. Der Schalter `--vorschau` gehört dem steuernden Chat; die Sitzung benutzt ihn nicht.

```python
#!/usr/bin/env python3
"""TB-136 A4: Register-Abschnitt 54 anhaengen (R74-R77 zeichengleich, Text des steuernden Chats 54.0, 54.5
und 54.6) und die 15 Marken aus Anhang A am alten Ort setzen. Nur Einfuegungen: keine bestehende Zeile
aendert sich, keine faellt weg.

Bauart docs/belege/TB-132/a4_eintrag.py. Alle Texte werden EINGESETZT, nicht abgetippt:
  - Kopf 54.0 und Schluss 54.5-54.6: die beiden ````-Zaeune im Auftrag nach "Kopf:" bzw. "Schluss:" (A3);
  - Ueberschriften, Ketten, Marken und die Angaben zur Quelle: der Daten-Block (JSON) aus Anhang A;
  - R-Bloecke: die Antwortdatei, Zeilen von..bis, Schnittregel des Auftrags (Beginn 'R<n> — ', Ende
    einschliesslich der ersten Zeile 'Quelle des Grundes:').
Ersetzt wird im Text des steuernden Chats ⟨S0⟩ -> `<S0>` (Kurzhash in Backticks) und, im Kopf und in den
Markenzeilen, ⟨DATUM⟩ -> das Datum aus --datum. Das Datum steht nicht im Auftrag; geprueft wird die Form, keine Uhr.

Eine Wache vor jedem Lauf ohne --vorschau (echter Lauf und Probelauf an einer Kopie):
  - Voraussetzung (Schritt 0e; R74 (b): "trifft es nicht zu, wird gemeldet, nicht eingetragen"): In der Datei
    voraussetzung.datei (Daten-Block) nennt der erste Eintrag von "im_repo" im Feld voraussetzung.feld als
    "modul" genau voraussetzung.modul. Sonst wird nichts geschrieben.

Der Auftrag und die Antwortdatei werden als Dateien gelesen. Die Sitzung stellt vorher sicher, dass beide
dem Commit von Schritt 0 gleichen (git diff --quiet <S0> -- <auftrag> <quelle>, rc 0).

Marken: je Marke Leerzeile + zwei Markenzeilen nach der Einfuegestelle (Zeilennummer am Original); mehrere
an derselben Stelle in der Reihenfolge des Daten-Blocks (dort nach R aufsteigend, dann nach Nummer).

Wachen: sha256 und Zeilenzahl des Eingangs; '## 54.' noch nicht vergeben; keine Zeile beginnt mit
'> R74 — '; jeder Anker genau einmal, vorher und nachher; jede alte Zeile in derselben Reihenfolge;
Abschnitt 9 und 10 und der ERZEUGT-Block unveraendert; genau 15 neue Markenzeilen, keine doppelt.

Aufruf aus der Repo-Wurzel (Python 3.9, nur Standardbibliothek):
  Probelauf:  trading-env/bin/python3 docs/belege/TB-136/a4_eintrag.py --s0 <S0> --datum <TT.MM.JJJJ> --register <kopie>
  echt:       trading-env/bin/python3 docs/belege/TB-136/a4_eintrag.py --s0 <S0> --datum <TT.MM.JJJJ>
  weitere:    --auftrag <pfad>   (Standard docs/auftraege/MAC_TB-136_register_fable_04a.md)
              --wurzel <ordner>  (Standard "."; davor stehen Quelle und, ohne --register, das Register)
              --daten <pfad>     (schreibt die gesetzten Marken mit Zeile nachher als JSON)
              --vorschau         (nur fuer den Soll-Bau des steuernden Chats, der Auftrag benutzt das nicht:
                                  ohne die Wache zur Voraussetzung; ohne --s0 bleibt `⟨S0⟩` stehen,
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

AUFTRAG = "docs/auftraege/MAC_TB-136_register_fable_04a.md"
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
    ap.add_argument("--datum")
    ap.add_argument("--daten")
    ap.add_argument("--vorschau", action="store_true")
    a = ap.parse_args()
    assert a.vorschau or a.s0, "--s0 <7 Hexzeichen> fehlt"
    assert a.s0 is None or re.match(r"^[0-9a-f]{7}$", a.s0), "--s0 <7 Hexzeichen> erwartet"
    assert a.datum and re.match(r"^\d{2}\.\d{2}\.\d{4}$", a.datum), "--datum <TT.MM.JJJJ> fehlt"
    assert datetime.datetime.strptime(a.datum, "%d.%m.%Y").strftime("%d.%m.%Y") == a.datum, "--datum ist kein Datum"
    s0 = "`%s`" % (a.s0 or "⟨S0⟩")

    auftrag = open(a.auftrag, encoding="utf-8").read()
    daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
    abschnitt = daten["abschnitt"]
    marken = daten["marken"]
    ueber = daten["ueberschriften"]
    erster, letzter = ueber[0]["R"], ueber[-1]["R"]
    assert len(marken) == daten["marken_zahl"] == 15
    for m in marken:
        assert m["m1"].count("⟨DATUM⟩") == 1, ("Platzhalter fuer das Datum nicht genau einmal", m["nr"])
        m["m1"] = m["m1"].replace("⟨DATUM⟩", a.datum)
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

    # Wache Voraussetzung R74 (b) (nicht im Vorschau-Modus)
    if not a.vorschau:
        v = daten["voraussetzung"]
        feld = json.load(open(os.path.join(a.wurzel, v["datei"]), encoding="utf-8"))[v["feld"]]
        assert feld["im_repo"] and feld["im_repo"][0]["modul"] == v["modul"], \
            "Voraussetzung R74 (b) trifft nicht zu (Schritt 0e): %r" % (feld["im_repo"],)

    # Text des steuernden Chats
    kopf = zaun(auftrag, "Kopf:")
    schluss = zaun(auftrag, "Schluss:")
    assert kopf.startswith("## %d. " % abschnitt), kopf[:30]
    assert schluss.startswith("### %d.%d " % (abschnitt, len(ueber) + 1)), schluss[:30]
    assert kopf.count("\n") == 2 and kopf.split("\n")[1] == "", "Kopf: Ueberschrift, Leerzeile, ein Absatz"
    assert kopf.count("⟨DATUM⟩") == 1 and "⟨DATUM⟩" not in schluss, "Datum des Eintrags: genau einmal, im Kopf"
    kopf, schluss = kopf.replace("⟨S0⟩", s0).replace("⟨DATUM⟩", a.datum), schluss.replace("⟨S0⟩", s0)
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
 "stand": "ee43f5f (HEAD d781f1b)",
 "abschnitt": 54,
 "kopfzeile": "## 54. Fable 04a — Registerblock R74–R77 (TB-136)",
 "register": "docs/VORREGISTRIERUNG_neuselektion.md",
 "register_sha256": "9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff",
 "register_zeilen": 11471,
 "quelle": {
  "pfad": "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
  "md5": "856b2c158e4bb6870876de129ce71f76",
  "bytes": 29195,
  "von": 156,
  "bis": 166
 },
 "ueberschriften": [
  {
   "xn": "54.1",
   "R": 74,
   "zeile": "### 54.1 R74 — Präzisierung zu R66 (a) und (b) (53.1) und Ergänzung der Tatsachennotiz in Registertext 5f (17.5) (Name des Handelskalenders…",
   "kette": "**Kette:** Marken: 17.5; 53.1 (R66); 53.9, Zeile „R66 (53.1) (b)“. Voraussetzung gemessen: 54.5. Offen: 54.6 Nr. 1, 3 und 8.",
   "marken_zahl": 3
  },
  {
   "xn": "54.2",
   "R": 75,
   "zeile": "### 54.2 R75 — Präzisierung zu R68 (c) und (d) (53.3), zu 16.6 und R37 (i) (48.5) (Attribution je Position), zu R36 (48.4) und zu R60 (c)…",
   "kette": "**Kette:** Marken: 16.6; 48.1 (R33) (vom steuernden Chat bestimmt, 54.6 Nr. 6); 48.2 (R34); 48.4 (R36); 48.5 (R37); 48.7 (R39); 48.14 (R46) (vom steuernden Chat bestimmt, 54.6 Nr. 6); 51.5 (R60); 52.2 (R64); 53.3 (R68); 53.4 (R69). Voraussetzung gemessen: 54.5. Offen: 54.6 Nr. 2 bis 5 und 10.",
   "marken_zahl": 11
  },
  {
   "xn": "54.3",
   "R": 76,
   "zeile": "### 54.3 R76 — Tatsachennotizen 04a",
   "kette": "**Kette:** Marken: keine. Indexzeilen ohne Marke (R77 (c)): 48.20 (R52). Tatsache gemessen: 54.5.",
   "marken_zahl": 0
  },
  {
   "xn": "54.4",
   "R": 77,
   "zeile": "### 54.4 R77 — Marken zu R74 bis R76; Präzisierung zu R70 (b) (53.5)",
   "kette": "**Kette:** Marken: 53.5 (R70). Nach (a) gesetzt: 13 Marken, je in der Kette des Blocks, der sie auslöst. Indexzeilen nach (b): 17.5. Tatsache gemessen: 54.5. Offen: 54.6 Nr. 4, 6 und 7.",
   "marken_zahl": 1
  }
 ],
 "marken_zahl": 15,
 "marken": [
  {
   "nr": 1,
   "R": 75,
   "ziel": "R77 (a): 16.6 — PRÄZISIERT durch R75, Unterpunkt (a)",
   "stelle": "16.6",
   "anker": "### 16.6 Registertext 2d",
   "ankerzeile": 2300,
   "nach": 2348,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **16.6 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (a), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 2,
   "R": 74,
   "ziel": "R77 (a): 17.5 — ERGÄNZT durch R74, Unterpunkte (a) und (b)",
   "stelle": "17.5",
   "anker": "### 17.5 Registertext 5f",
   "ankerzeile": 2824,
   "nach": 2840,
   "anfang40": "> weder Bedingung noch Widerlegung.",
   "m1": "> ⭐ **17.5 ERGÄNZT durch R74 (54.1)** (Fable 04a R74, Unterpunkte (a) und (b), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 3,
   "R": 75,
   "ziel": "R65 (a), angewandt vom steuernden Chat: R75 (c) sagt, woraus „Die Zeile der Bestätigungsperiode in zellen.csv (R33, R68)“ gebildet wird; 48.1 trägt für dieselbe Zeile schon die Marke zu R68; R77 (a) nennt den Ort nicht",
   "stelle": "48.1 (R33)",
   "anker": "### 48.1 R33",
   "ankerzeile": 10789,
   "nach": 10795,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **48.1 R33 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (c), vom steuernden Chat nach R65 (a) bestimmt, TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 4,
   "R": 75,
   "ziel": "R77 (a): 48.2 (R34) — ERGÄNZT durch R75, Unterpunkt (g)",
   "stelle": "48.2 (R34)",
   "anker": "### 48.2 R34",
   "ankerzeile": 10799,
   "nach": 10802,
   "anfang40": "> Quelle des Grundes: 22.2 (Werte des La",
   "m1": "> ⭐ **48.2 R34 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (g), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 5,
   "R": 75,
   "ziel": "R77 (a): 48.4 (R36) — PRÄZISIERT durch R75, Unterpunkte (c) und (d)",
   "stelle": "48.4 (R36)",
   "anker": "### 48.4 R36",
   "ankerzeile": 10813,
   "nach": 10816,
   "anfang40": "> Quelle des Grundes: 24.2, 24 (Festlegu",
   "m1": "> ⭐ **48.4 R36 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkte (c) und (d), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 6,
   "R": 75,
   "ziel": "R77 (a): 48.5 (R37) — PRÄZISIERT durch R75, Unterpunkt (a)",
   "stelle": "48.5 (R37)",
   "anker": "### 48.5 R37",
   "ankerzeile": 10820,
   "nach": 10826,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **48.5 R37 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (a), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 7,
   "R": 75,
   "ziel": "R77 (a): 48.7 (R39) — ERGÄNZT durch R75, Unterpunkt (b)",
   "stelle": "48.7 (R39)",
   "anker": "### 48.7 R39",
   "ankerzeile": 10837,
   "nach": 10846,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **48.7 R39 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (b), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 8,
   "R": 75,
   "ziel": "R65 (a), angewandt vom steuernden Chat: R75 (d) und (f) geben der Abnahme nach R46 eine weitere Prüfung und dem Test-Snapshot einen Deckelfall; R77 (a) nennt den Ort nicht",
   "stelle": "48.14 (R46)",
   "anker": "### 48.14 R46",
   "ankerzeile": 10892,
   "nach": 10895,
   "anfang40": "> Quelle des Grundes: 27.1, 24.3 (die Re",
   "m1": "> ⭐ **48.14 R46 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkte (d) und (f), vom steuernden Chat nach R65 (a) bestimmt, TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 9,
   "R": 75,
   "ziel": "R77 (a): 51.5 (R60) — PRÄZISIERT durch R75, Unterpunkt (d)",
   "stelle": "51.5 (R60)",
   "anker": "### 51.5 R60",
   "ankerzeile": 11227,
   "nach": 11239,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **51.5 R60 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 10,
   "R": 75,
   "ziel": "R77 (a): 52.2 (R64) — PRÄZISIERT durch R75, Unterpunkt (d)",
   "stelle": "52.2 (R64)",
   "anker": "### 52.2 R64",
   "ankerzeile": 11313,
   "nach": 11331,
   "anfang40": "> Eintrag und Stand oben bleiben zeichen",
   "m1": "> ⭐ **52.2 R64 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (d), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 11,
   "R": 74,
   "ziel": "R77 (a): 53.1 (R66) — PRÄZISIERT durch R74",
   "stelle": "53.1 (R66)",
   "anker": "### 53.1 R66",
   "ankerzeile": 11382,
   "nach": 11385,
   "anfang40": "> Quelle des Grundes: 1c im Wortlaut („a",
   "m1": "> ⭐ **53.1 R66 PRÄZISIERT durch R74 (54.1)** (Fable 04a R74, TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 12,
   "R": 75,
   "ziel": "R77 (a): 53.3 (R68) — PRÄZISIERT durch R75",
   "stelle": "53.3 (R68)",
   "anker": "### 53.3 R68",
   "ankerzeile": 11396,
   "nach": 11399,
   "anfang40": "> Quelle des Grundes: R37 (i) („Die Best",
   "m1": "> ⭐ **53.3 R68 PRÄZISIERT durch R75 (54.2)** (Fable 04a R75, TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 13,
   "R": 75,
   "ziel": "R77 (a): 53.4 (R69) — ERGÄNZT durch R75, Unterpunkt (h)",
   "stelle": "53.4 (R69)",
   "anker": "### 53.4 R69",
   "ankerzeile": 11403,
   "nach": 11406,
   "anfang40": "> Quelle des Grundes: R39 mit seinem Gru",
   "m1": "> ⭐ **53.4 R69 ERGÄNZT durch R75 (54.2)** (Fable 04a R75, Unterpunkt (h), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 14,
   "R": 77,
   "ziel": "R77 (a): 53.5 (R70) — PRÄZISIERT durch R77, Unterpunkt (b)",
   "stelle": "53.5 (R70)",
   "anker": "### 53.5 R70",
   "ankerzeile": 11410,
   "nach": 11413,
   "anfang40": "> Quelle des Grundes: R61 (b), erster un",
   "m1": "> ⭐ **53.5 R70 PRÄZISIERT durch R77 (54.4)** (Fable 04a R77, Unterpunkt (b), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 15,
   "R": 74,
   "ziel": "R77 (a): 53.9, Zeile „R66 (53.1) (b)“ — ERGÄNZT durch R74, Unterpunkte (b) und (f)",
   "stelle": "53.9, nach der Tabelle",
   "anker": "### 53.9 Voraussetzungen und Befunde",
   "ankerzeile": 11438,
   "nach": 11454,
   "anfang40": "| R66–R73, Zitate und Verweise | — | 98 ",
   "m1": "> ⭐ **53.9, Zeile „R66 (53.1) (b)“ ERGÄNZT durch R74 (54.1)** (Fable 04a R74, Unterpunkte (b) und (f), TB-136, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  }
 ],
 "dateien": [
  [
   "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   "db37f969a557b60a27cbd7ac6b942def",
   9574
  ],
  [
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md",
   "c96f56c9682d4fb8a37188735edae7ad",
   9259
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   "856b2c158e4bb6870876de129ce71f76",
   29195
  ]
 ],
 "fundstellen": [
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   153,
   "## Registerblock — zeichengleich kopierbar, nummeriert (ab R74)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   155,
   "```"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   167,
   "```"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   156,
   "dass das Feld kalender der Messung TB-47 als Importstelle notifications/boersenkalender.py führt"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   159,
   "dass der Kern, der die MtM-Reihe bildet, die Tagesrendite als Summe der Beiträge der Positionen über einem Kapitalstand bildet"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   159,
   "dass der Bericht der Zeile aus zellenbericht.csv nach R34 keine eigene Zeile in der Berichtsliste von Abschnitt 8 verlangt"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   159,
   "Die Zuteilung läuft je Zelle einmal (R45)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   160,
   "29.3 (ein Kapitalpfad)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   157,
   "R28 (Bauart: Kopie mit Probe)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   159,
   "nie leer (R67)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   165,
   "53.10 (Statusliste)"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   165,
   "der Index führt die Zählung"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   75,
   "Der Test-Snapshot der Abnahme (R46) braucht Kurstage, die zum Kalender passen"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   116,
   "**K1:** einverstanden"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   134,
   "468 406"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   144,
   "3. **Übrige Grössen der Zeile im Deckelfall.**"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   145,
   "4. **Der Deckeltag selbst.**"
  ],
  [
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   29,
   "**`BACKLOG.md` (gesperrt)**"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10205,
   "neunter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10970,
   "zehnter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10970,
   "berichtigt in R33; elfter Fall"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10792,
   "elfter Fall der Klasse „Bestand behauptet statt Voraussetzung genannt“"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   874,
   "| Kennzahl | Quelle |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   876,
   "| Netto-Sharpe, Median über die Selektionsfalten | Selektionsstatistik |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   888,
   "| Bestätigungsperiode: Sharpe, Rendite, Drawdown, Trades | zuletzt |"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10801,
   "Bericht, kein Tor; N unverändert"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10887,
   "ist ein zweiter Rechenweg und wird nicht gegangen"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   5402,
   "Der Kapitalpfad eines Bots beginnt"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10744,
   "Literal mit Probe gegen den Registertext"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11223,
   "Kopie mit Probe"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11391,
   "kein Feld leer"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11456,
   "### 53.10 Was offen bleibt"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   2833,
   "gemessen TB-47"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   2834,
   "**4.6.1**"
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   10973,
   "**Kette:** Marken: keine."
  ],
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   11444,
   "| R66 (53.1) (b) |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   137,
   "| **2d** Embargo | 15.4 (d) | Z. 1496 ERSETZT durch 16.6 → Z. 2347 PRÄZISIERT durch R37 (48.5) | **16.6** (T1) **mit** 48.5 R37 (T4) |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   156,
   "| **5f** Umgebung | 17.5 | – | **17.5** (T1) | 20 Tatsachennotiz Lock (T1) |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   202,
   "| 48 aus 29b |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   205,
   "| 51 aus 01a |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   206,
   "| 52 aus 02a |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   207,
   "| 53 aus 02c | 4 | R66–R73 (53.1–53.8); 53.9 Voraussetzungen und Befunde; 53.10 Offenes | – |"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   363,
   "## 8. Die Marken aus Fable 02c (TB-132)"
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   399,
   "- **17.5:** Handelskalender der Aktien-Tagesreihe → R66 (a) und (b) (53.1). Ohne Marke (R70 (b), 53.5)."
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   70,
   "54 Antworten."
  ]
 ],
 "zeilen_mit": [],
 "zaehlungen": [
  [
   "docs/VORREGISTRIERUNG_neuselektion.md",
   "zwölfter Fall",
   0
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "Zählung",
   0
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "^## 8\\. Die Marken aus Fable 02c \\(TB-132\\)",
   1
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "^## 9\\. ",
   0
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "Indexzeilen aus Fable 04a",
   0
  ],
  [
   "docs/projektfuehrung/REGISTER_INDEX.md",
   "\\n\\n---\\n\\n\\*\\*Pflege:\\*\\*",
   1
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "^## 6 — Geparkt, null Arbeit",
   1
  ],
  [
   "docs/projektfuehrung/BACKLOG.md",
   "Aus Fable 04a",
   0
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 02c \\|",
   1
  ],
  [
   "docs/projektfuehrung/FABLE_DIALOG_INDEX.md",
   "^\\| 04a \\|",
   0
  ],
  [
   "docs/projektfuehrung/JOURNAL.md",
   "^## ED — TB-132",
   1
  ],
  [
   "docs/projektfuehrung/JOURNAL.md",
   "^## EE ",
   0
  ],
  [
   "docs/projektfuehrung/JOURNAL.md",
   "^## Wiederkehrende Lehren",
   1
  ]
 ],
 "glob_summen": [],
 "glob_treffer": [],
 "baum_summen": [],
 "arbeitsbaum": {
  "head": "d781f1b",
  "geaendert": [
   "docs/auftraege/AKTUELLER_AUFTRAG.md",
   "docs/projektfuehrung/UEBERGABE.md"
  ],
  "unverfolgt": [
   "docs/auftraege/MAC_TB-136_register_fable_04a.md",
   "docs/belege/TB-133/vormessung/v1_vormessung_04a.md",
   "docs/belege/TB-134/CLOUD_TB-134_antwort_offene_voraussetzungen.md",
   "docs/belege/TB-135/CLOUD_TB-135_antwort_anforderungen_zellen_erzeuger.md",
   "docs/belege/TB-136/vormessung/h1_fundstellen_r74.md",
   "docs/belege/TB-136/vormessung/h2_fundstellen_r75.md",
   "docs/belege/TB-136/vormessung/h3_fundstellen_r76_r77_leseprotokoll.md",
   "docs/belege/TB-136/vormessung/v1_bewertung_fable_04a.md",
   "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   "docs/projektfuehrung/FABLE_ANTWORT_2026-10-04a_kalendername_deckelfall_zaehlung.md",
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_eroeffnung.md",
   "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-04_neuer_chat.md"
  ],
  "spaeter": [
   "docs/auftraege/MAC_TB-136_register_fable_04a.md",
   "docs/auftraege/AKTUELLER_AUFTRAG.md"
  ]
 },
 "voraussetzung": {
  "datei": "research/snapshotgrenze/ergebnisse/eingaben.json",
  "feld": "kalender",
  "modul": "notifications/boersenkalender.py"
 }
}
DATEN-ENDE
```
