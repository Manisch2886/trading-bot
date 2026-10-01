# TB-126 Register E-2 — Fable 27c, 29b, 30a (R18–R55) als Abschnitte 47–49, Tatsachennotizen in 50, Marken am alten Ort; Registerkopie und Index neu

**Sitzungstitel:** `TB-126` · **Modell:** Opus, Aufwand hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 01.10.2026 vom steuernden Chat
**Vorgänger:** TB-125 (`41864d4`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-126_register_e2.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** immer `trading-env/bin/python3` (7c). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15). Ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Prüfwerkzeuge:** Jedes Skript, das diese Sitzung schreibt (Einsetzen, Prüfen, Vergleichen, Messen), liegt unter `docs/belege/TB-126/` und wird mitcommittet. Das gilt ausdrücklich auch für Vergleichsskripte (`cmp`, `diff`); in TB-124 fehlte eines.
**Hilfen, keine Quelle:** `docs/projektfuehrung/VORARBEIT_TB-126_bauplan_registerauftrag.md` (Bauart TB-114/TB-117 mit Fundstellen) und `docs/projektfuehrung/VORARBEIT_TB-126_inventar_r18_r55.md` (Inventar je R-Block), beide von Helfern des steuernden Chats am 01.10.2026. Sie kommen in Schritt 0 ins Repo. Wo sie und dieser Auftrag sich widersprechen, gilt dieser Auftrag. **Massgeblich für Überschriften und Marken ist Anhang A** am Ende dieses Auftrags (gebaut von einem Helfer des steuernden Chats am 01.10.2026 am Register `41864d4`; jeder Anker dort genau 1, Prüfskript in Anhang A).

## ⭐⭐ Freigabe des Betreibers, wörtlich

**01.10.2026, ca. 08:22, Auswahlkarte im steuernden Chat.** Kartentext: *„Gibst du TB-126 frei? Das umfasst: Register Abschnitte 47–50 anhängen (R18–R55 zeichengleich, Tatsachennotizen), 88 Marken am alten Ort einschliesslich einer in Abschnitt 9 (R51), Registerkopie und Index neu, BACKLOG-Block, Journal DX und das Entfernen der zwei Worktrees. Kein Code, kein neues Abbild.“* Gewählt: **„Freigeben wie beschrieben (Empfohlen)“**.

| freigegeben | Pfad / Handlung |
|---|---|
| Register **anhängen** (Abschnitte 47, 48, 49, 50), **Marken additiv** am alten Ort, einschliesslich **einer Marke in Abschnitt 9** (R48 (b), verlangt in R51) | `docs/VORREGISTRIERUNG_neuselektion.md` |
| neu erzeugen, nachziehen | `docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md` (über `docs/werkzeuge/registerkopie.py`), `docs/projektfuehrung/REGISTER_INDEX.md` |
| committen in Schritt 0 | dieser Auftrag, `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/projektfuehrung/UEBERGABE.md`, die zwei `VORARBEIT_TB-126_*.md` |
| ein Block in Schritt 0 | `docs/projektfuehrung/BACKLOG.md` |
| Journalblock **DX** | `docs/projektfuehrung/JOURNAL.md` |
| Belege, Ergebnis | `docs/belege/TB-126/`, `docs/ERGEBNIS_TB-126_register_e2.md` |
| verwerfen, nur nach rotem Nachweis in A6 und nachdem der Diff als `abbruch_register.diff` gesichert ist | die eigene, uncommittete Änderung am Register (`git checkout -- docs/VORREGISTRIERUNG_neuselektion.md`) |
| entfernen (Betreiberentscheid 30.09.2026, ca. 22:40, per Karte: „TB-126 löscht sie (Empfohlen)“) | die zwei Worktrees `$TMPDIR/tb123_vorher` und `$TMPDIR/tb123_vorher2`, nur mit `git worktree remove` |

⛔ **Nicht freigegeben, mit Grund:**
- **Jede Zeile im Listentext von Abschnitt 10.** *Grund:* Die Sperrlisten-Sonde vergleicht ihn mit dem Abbild (36.6, Prüfung (ii)). Was nach Fable dorthin gehört (R42, R45, R48 (k), R49 (g)), steht als Verweis in der Kette und als Indexzeile in `REGISTER_INDEX.md`.
- **Jede Zeile im ERZEUGT-Block von Abschnitt 3** (zwischen `<!-- ERZEUGT: registerbericht.py -->` und `<!-- ENDE ERZEUGT -->`). *Grund:* `registerbericht.py --pruefen` vergleicht ihn mit dem Erzeuger. Die Marke „3, Zahlenteil“ aus R51 steht unmittelbar **nach** `<!-- ENDE ERZEUGT -->`.
- **Jede Änderung oder Löschung einer bestehenden Registerzeile.** *Grund:* Das Register ist append-only; Marken sind neue Zeilen (34). Nachweis: numstat zweite Spalte 0.
- **Code jeder Art**, insbesondere `research/vorregistrierung/*.py`, `shared/`, `strategies/`. *Grund:* E-2 ist ein Textauftrag; eingefrorener Code bleibt zu.
- **Ein neues Abbild der Sperrliste.** *Grund:* Keine Sperrlistendatei bewegt sich (vgl. 42.7: „Kein neues Abbild — keine Sperrlistendatei hat sich bewegt“).
- **Läufe von `auswertung.py`, Erzeugern oder Backtests.** *Grund:* Sichtschutz; keine Voraussetzung dieses Auftrags braucht einen Lauf.
- **`git worktree remove --force`** und jedes andere Löschen oder Verwerfen. *Grund:* Ein Worktree, den `remove` verweigert, trägt Ungesichertes; darüber entscheidet der Betreiber.
- `crontab`, Datenbanken, `UEBERGABE.md` und `UEBERGABE_ARCHIV.md` (ausser dem Commit in Schritt 0).

**Sichtschutz 27.1:** Diese Sitzung liest keine Kennzahl, keine Trade- und keine Zeilenzahl aus Ergebnisdateien. Aus Testausgaben nur rc, Dauer und Schlusszeile. Code wird nur gelesen, wo dieser Auftrag eine Fundstelle nennt.

## Belegt · erschlossen · offen

*Gemessen vom steuernden Chat am 01.10.2026 über die Geräteanbindung, nur lesend, an HEAD `41864d4`.*

**Belegt:**
- Register: 10 347 Zeilen, sha256 `18e39ee29b9bd4f03a2ad4953c85c2e59558de3aaab26844ae58fb7590fca93c` (= `REGISTER_INDEX.md` Z. 4, `docs/belege/TB-124/0d_ausgang.txt`), md5 `c8a32c0f0037c6c65bd08aae6be5a7c1`. Letzter Abschnitt: 46 (letzter Unterabschnitt 46.11).
- Quellen der R-Blöcke:

| Kürzel | Datei | md5 | Bytes | Registerblock |
|---|---|---|---|---|
| 27c | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md` | `ff96392ed654fdcae2e991e51e424dc5` | 48 420 | Codezaun ```` ```markdown ```` Z. 160 bis ```` ``` ```` Z. 210; Blöcke R18–R32 in Z. 161–209 |
| 29b | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md` | `898d5bd53b6617209b7ce4f7e8992941` | 73 703 | Codezaun ```` ``` ```` Z. 189 bis Z. 268; Blöcke R33–R52 in Z. 190–267 |
| 30a | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md` | `f9cdbbef543ec54ed07ee0566c336dde` | 12 925 | kein Zaun; Überschrift Z. 24, Blöcke R53–R55 in Z. 25–32 (bis Dateiende) |

- 27c und 29b sind Abschriften aus Fables Ablage, je zweifach unabhängig mit `cmp` rc 0 (UEBERGABE_ARCHIV, Nachtrag 29.09.2026, 14:52). 30a ist eine Abschrift aus einem Text-Anhang ohne Markdown; die Blöcke R53–R55 sind **bytegleich** mit der Ablage-Fassung `FABLE_ANTWORT_2026-09-30a_vorlauf_aggregation_leere_menge.md` (md5 `5e5401bc…`), geprüft am 30.09.2026 (UEBERGABE, Nachtrag 23:20).
- **Schnittregel (maschinell geprüft, 38/38):** Ein Block beginnt mit der Zeile, die mit `R<n> — ` beginnt (in 27c fett: `**R<n> — `), und endet einschliesslich der ersten folgenden Zeile, die mit `Quelle des Grundes:` beginnt (in 27c: `*Quelle des Grundes:*`). Diese Zeile ist in jedem Block die einzige, die auf „Kein Ergebnis.“ endet. Die Leerzeilen zwischen Blöcken gehören zu keinem Block. 38 Blöcke ohne Lücke und ohne Dopplung (27c: 15, 29b: 20, 30a: 3). ⚠️ In 29b stehen R-Nummern auch ausserhalb des Zauns (z. B. „→ **R48 (d)**“); geschnitten wird **nur** innerhalb der genannten Zeilenbereiche.
- Ausgangswerte mit Fundstelle: `herkunft.register()` `01f5997a9a13b4b30162e2a04965670a9ffa8d725a93d579e530dc0708ec2a70`, `fehlend []`, 23 Teile (`docs/belege/TB-124/c5_nachher.txt`) · gültiges Abbild `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, sha256 `46f0ad5d…` (Register 46.11) · Sonde dagegen: rc 2 (Normalfall), Pfad-Bestandteile 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“ (`docs/belege/TB-124/0d_ausgang.txt`) · `test_vorregistrierung` 196/196, Laufzeit rund 900 s (`docs/belege/TB-117/f_test_vorregistrierung.txt`).
- Diese Code-Dateien sind zwischen `0034960` (Stand der Vormessung) und `41864d4` unverändert (`git diff --name-only` leer): `research/vorregistrierung/{auswertung,kennzahlen,registerdaten,messgroessen,registerbericht,pruefe_grenzsaetze}.py`, `research/mtm_drawdown/mtm_kern.py`, `research/faltenplan_neun/embargo_neun.py`, `research/registernachtrag_tb48/pruefe_abschnitt17.py`, `shared/snapshot.py`, `research/exposure_messung/auswertung.py`, `research/exposure_messung/exposure_kern.py`. `auswertung.py` ist seit `852f253` unverändert, md5 `4f4b455e2d33aa46b309bbd2ff3bba33`. Die Zeilenangaben in Abschnitt 50 gelten deshalb weiter.
- Nummern: TB frei ab 127 · Journal **DX** · R-Blöcke frei ab R56.

**Erschlossen:** Mit jeder Marke vor Z. 905 verschiebt sich Abschnitt 10; der Text der Sonde ist dann nicht mehr bytegleich, der JSON-Bericht **ohne das Feld `zeilen`** schon (ERGEBNIS_TB-114, Abnahme Block A). Die Teile der Registerkopie bekommen neue Grenzen: Teil 1 hat nur rund 466 B Luft.

**Offen (die Sitzung misst, nimmt nichts an):** `registerbericht.py --pruefen` vorher (kein Beleg mit diesem Wert gefunden); die Zahl der Marken; die genauen Zeilen des Docstring-Zitats in A4 (erwartet `auswertung.py` Z. 36–67).

## Schritt 0 — Sicherung, Ausgang, Aufräumen

**0a.** `git status --short` — genau diese Einträge, eingetragen vom steuernden Chat beim Ablegen:
*Eingetragen vom steuernden Chat am 01.10.2026, ca. 18:55, gemessen über die Geräteanbindung mit `git --no-optional-locks diff --name-only HEAD` und `ls-files --others --exclude-standard`: zwei geänderte, drei neue Dateien.*

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-126_register_e2.md
?? docs/projektfuehrung/VORARBEIT_TB-126_bauplan_registerauftrag.md
?? docs/projektfuehrung/VORARBEIT_TB-126_inventar_r18_r55.md
```

Weicht etwas ab ⇒ Abbruch. Commit `TB-126 Schritt 0: Stand 01.10. gesichert`, pushen. Danach steht für alle Quellenangaben der Commit von Schritt 0, im Folgenden **⟨S0⟩** (kurz, 7 Zeichen).

**0b. Worktrees.** `git worktree list --porcelain` ⇒ `docs/belege/TB-126/0b_worktrees.txt` (vorher). Für jeden der beiden Pfade `…/tb123_vorher` und `…/tb123_vorher2`: `git worktree remove <pfad>` **ohne** `--force`. Danach erneut `git worktree list --porcelain` und `test -d <pfad>` je Pfad, beides in dieselbe Datei. Verweigert `remove` einen Pfad: nicht erzwingen, Ausgabe festhalten, im Ergebnis melden. Das ist **kein** Abbruch.

**0c. BACKLOG.** Anker: die Zeile `## 6 — Geparkt, null Arbeit *(ins Archiv verschoben 20.09.2026, TB-60)*` in `docs/projektfuehrung/BACKLOG.md`. Den Anker vorher zählen, Soll genau 1 (gezählt vom steuernden Chat am 01.10.2026: 1). Den folgenden Text **vor** der Ankerzeile einfügen, zeichengleich. Er endet mit einer Leerzeile, sodass zwischen ihm und der Ankerzeile genau eine Leerzeile steht.

```
### Aus der Abnahme TB-124 (30.09.2026)

- **Scan-Schleifen in `research/`:** `research/trailing_stops/run_one_bot.py:379` und `research/vbc_deepdive/run_deepdive.py:145` beginnen ihren Scan bei `WARMUP_PERIOD + 1`, unabhängig vom Vorlauf der Zelle (Fundstellen vom Gegenleser der Abnahme, vom steuernden Chat nicht nachgelesen). Binden oder begründet lassen, vor E-6 bzw. Posten 5. Handwerk.
- **Belegpflicht für Vergleichsskripte:** Das `cmp`-Skript von TB-124 C1 lag nicht im Belegordner. Aufträge nennen ausdrücklich: Jedes Prüf- und Vergleichsskript liegt unter `docs/belege/TB-<n>/` und wird mitcommittet.

```

Nachweis in `0c_backlog.txt`: Ankerzahl vorher, erste Textzeile nachher genau 1, `git diff --numstat` der Datei (Soll `5	0`: Überschrift, Leerzeile, zwei Punkte, Leerzeile).

**0d. Ausgangswerte** ⇒ `docs/belege/TB-126/0d_ausgang.txt`, mit einem Skript `0d_ausgang.sh` in der Bauart von `docs/belege/TB-117/0b_ausgang.sh` und `docs/belege/TB-117/b_sonde.sh` (dort die Aufrufe von `herkunft.register()` und der Sonde übernehmen, nicht neu erfinden). **Messen, nicht annehmen.** Soll, je mit Fundstelle oben:
- Register: Zeilen 10 347, sha256 `18e39ee2…`, md5 `c8a32c0f…`;
- `herkunft.register()` `01f5997a…`, `fehlend []`, 23 Teile;
- Sonde gegen `sperrliste_abbild_2026-09-26_tb117.json`: rc 2, 37/0/0, (ii) 0, „Listentext wie bei Erzeugung: ja“. Dazu der sha256 des JSON-Berichts **ohne das Feld `zeilen`** (Vergleichswert für nachher) und `git status --porcelain` gezählt vor und nach der Sonde;
- `trading-env/bin/python3 research/vorregistrierung/registerbericht.py --pruefen`: rc und Schlusszeile, als Vergleichswert für nachher;
- md5 der drei Quellen 27c, 29b, 30a am Commit ⟨S0⟩ (Soll: Tabelle oben);
- Schreibe dazu den Listentext von Abschnitt 10 (von der Zeile `## 10.` bis vor `## 11.`) und den ERZEUGT-Block von Abschnitt 3 (einschliesslich der beiden Kommentarzeilen) als Dateien `0d_abschnitt10_vorher.txt` und `0d_erzeugt_vorher.txt` in den Belegordner (Vergleich in A4).

Weicht ein Wert mit Fundstelle ab ⇒ Abbruch. `registerbericht.py --pruefen` hat kein Soll: Den Wert festhalten; verglichen wird nachher gegen vorher.

**0e. Basis `test_vorregistrierung`**, am sauberen Stand nach dem Commit aus 0, **ohne Zeitgrenze** (Laufzeit rund 900 s; in TB-117 war eine Grenze von 900 s zu knapp) ⇒ `0e_test_vorregistrierung.txt` (rc, Dauer, Schlusszeile). Soll 196/196.

**0f. Unverändert seit der Vormessung:** `git diff --name-only 0034960 HEAD --` für die zwölf Code-Dateien aus „Belegt“ ⇒ `0f_unveraendert.txt`, Soll leer. Dazu `git log --oneline 852f253..HEAD -- research/vorregistrierung/auswertung.py`, Soll leer, und md5 von `auswertung.py`, Soll `4f4b455e…`. Weicht etwas ab ⇒ Abbruch, denn die Zeilenangaben in Abschnitt 50 stimmten dann nicht mehr.

**0g. Vorprüfungen vor jedem Registereintrag** ⇒ `docs/belege/TB-126/0g_vorpruefung.txt`, Skript `0g_vorpruefung.py`. Alles am Commit ⟨S0⟩. Weicht etwas ab ⇒ **Abbruch vor Schritt A**; das Register bleibt unberührt.
1. Anhang A, Daten-Block: jeder Anker kommt im Register genau 1-mal vor, und jede Einfügestelle „nach Zeile N“ beginnt mit dem angegebenen Anfang. Das Prüfskript aus Anhang A darf übernommen werden. Abweichung einzelner Marken ist **kein** Abbruch: Diese Marken werden nicht gesetzt und genannt (A2). Abbruch nur, wenn mehr als fünf Marken abweichen.
2. Entwurf TB-122: Z. 235 von `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` beginnt mit `> **Vollzug TB-30b Posten 3 (11.3) in TB-122`, Z. 275 endet mit `TB-122 Befund F1).`
3. Entwurf TB-124: Z. 289 von `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` beginnt mit `> **Vollzug TB-30b Posten 3 (11.3), Teil Scanbeginn`, Z. 323 endet mit `nie früher, nicht später.`
4. Docstring von `research/vorregistrierung/auswertung.py`: Die Zeile `DIE ROHERGEBNISSE - DER VERTRAG` und die Zeile `ZWEI DEFINITIONEN, DIE SONST SCHWEIGEND AUSEINANDERLAUFEN` kommen je genau 1-mal vor. Im Bereich dazwischen (das Zitat aus A4) zählen: `<markt>.csv` genau 1; `zellenbericht`, `symbole_je_falte` und `audit` (ohne Rücksicht auf Gross- und Kleinschreibung) je 0. Sonst stimmt ein Satz in 50.2 nicht.

Commit `TB-126 0: Worktrees, BACKLOG, Ausgang, Vorprüfung`, pushen.

## Schritt A — Abschnitte 47–50 in einem Lauf: R18–R55 zeichengleich, Tatsachennotizen, Marken

**A1. Gliederung (vom steuernden Chat vergeben):**

| Abschnitt | Quelle | Unterabschnitte |
|---|---|---|
| 47 | 27c | 47.0 Kopf · 47.1–47.15 = R18–R32 in der Reihenfolge des Codezauns (47.n = R(17 + n)) |
| 48 | 29b | 48.0 Kopf · 48.1–48.20 = R33–R52 (48.n = R(32 + n)) |
| 49 | 30a | 49.0 Kopf · 49.1 = R53, 49.2 = R54, 49.3 = R55 |
| 50 | steuernder Chat | 50.0–50.7, Text in A3 |

**Form je R-Block** (Bauart 46; die Überschriftzeile steht exakt in Anhang A, Tabelle 1):

```
### <x.n> R<nn> — <Bezug aus Anhang A, Tabelle 1>

> <Zeile 1 des Blocks, zeichengleich>
> <Zeile 2 des Blocks, zeichengleich>
> …

**Kette:** <siehe A2>
```

Jede Zeile des Blocks wird zu `> ` plus der Zeile, unverändert, auch Fettung, Kursivschrift und Anführungszeichen. Leerzeile vor und nach jedem Unterabschnitt. Die Köpfe x.0 sind die folgenden Texte, zeichengleich, mit ⟨S0⟩ ersetzt (dieselbe Ersetzung macht das Prüfskript in A6):

````
## 47. Fable 27c — Registerblock R18–R32 (TB-126)

Reines Eintragen von Registertext, Bauart wie 46 (46.0). Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md`, md5 `ff96392ed654fdcae2e991e51e424dc5`, 48 420 B, am Commit ⟨S0⟩, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert“, Z. 161–209. Die Datei hat der steuernde Chat am 29.09.2026 aus Fables Ablage übertragen, zweifach unabhängig, `cmp` rc 0; Bytegleichheit mit der Ablage war mit dem Werkzeug nicht messbar. Je Block ein Unterabschnitt in der Reihenfolge des Codeblocks, der Block als Blockzitat, darunter die Kette. Die Nummern hat der steuernde Chat vergeben (Auftrag TB-126, Einzelfreigabe des Betreibers), nicht Fable. Die Regel aus 34 gilt weiter: Marke am alten Ort, der alte Satz bleibt zeichengleich. ⛔ In Abschnitt 10 steht keine Marke; was dorthin gehört, steht in der Kette und als Indexzeile in `REGISTER_INDEX.md`. Die Voraussetzungen, die Fable „zu messen“ nennt, stehen mit Befund in 50.1.
````

````
## 48. Fable 29b — Registerblock R33–R52 (TB-126)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md`, md5 `898d5bd53b6617209b7ce4f7e8992941`, 73 703 B, am Commit ⟨S0⟩, Abschnitt „Registerblock … (ab R33)“, Z. 190–267. Übertragen wie 27c (47). Die Marken für Register 0–12 setzt dieser Abschnitt nach R51 (48.19); darunter steht **eine Marke in Abschnitt 9** (R48 (b)), die R51 ausdrücklich verlangt. Der Verweis aus R8 (d) in Register 9 (45.8) ist ein anderer und kommt weiter nach dem Tag; die Sätze „in 9 steht … keine Marke“ in 45.8 und 46.0 (und die Listen in 45.10, 46.10) beschreiben den damaligen Stand, ihr einziger Grund war dieser Verweis. Für R48, R49 und R50 stehen Marken an allen Orten, die der Unterpunkt nennt, und an denen der R51-Liste (Vereinigung). Für Abschnitt 10 und den vollen Datenstand-Hash (17.3, 17.9, 18) verlangt R51 Indexzeilen statt Marken.
````

````
## 49. Fable 30a — Registerblock R53–R55 (TB-126)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md`, md5 `f9cdbbef543ec54ed07ee0566c336dde`, 12 925 B, am Commit ⟨S0⟩, Z. 25–32. Die Datei ist eine Abschrift aus einem Text-Anhang ohne Markdown-Auszeichnung. Die drei Blöcke sind bytegleich mit Fables Ablage-Fassung (`FABLE_ANTWORT_2026-09-30a_vorlauf_aggregation_leere_menge.md`, md5 `5e5401bcc6b5551a7a61a8a1b4331fee`), geprüft vom steuernden Chat am 30.09.2026 (R53 `cbaeea5b…`, R54 `914ddd1d…`, R55 `1f3e534b…`). R54 berichtigt 2a und R48 (g) (48.16); die Marken stehen an 15.4 und unter 48.16.
````

**A2. Marken am alten Ort.** Überschriften, Marken und Indexzeilen stehen fertig in **Anhang A**; massgeblich ist dessen Daten-Block. Die Sitzung baut die Tabelle **nicht** selbst. Sie
1. setzt jede Marke aus Anhang A, Tabelle 2, an ihrer Einfügestelle ein, nachdem 0g Anker und Einfügestelle bestätigt hat; ⟨DATUM⟩ ist der Tag des Eintrags (TT.MM.JJJJ); eingesetzt wird von unten nach oben, weil die Zeilennummern am Original gelten;
2. setzt eine Marke, deren Anker oder Einfügestelle in 0g abwich, nicht und nennt sie im Ergebnis (kein Abbruch, ausser bei mehr als fünf, siehe 0g);
3. setzt keine Marke aus den Listen „B — nicht gesetzt“ und „C — ohne Bezugsform“ in Anhang A; das Ergebnis nennt sie unter „Für Fable“;
4. führt die Indexzeilen aus Anhang A, Liste A, in C3 aus.

„B3“ in Anhang A bezeichnet die Marken für Abschnitt 50 (an 15.4, 11.3 und der Zusatz an den R24-Marken in 16.4); „Liste B“ und „Liste C“ sind die Orte ohne Marke. Die Namen stammen aus einer früheren Fassung dieses Auftrags.

Regeln, nach denen Anhang A gebaut ist (zur Prüfung, nicht zum Neubauen): Ziele sind die Orte, die Fable im Block als Bezug nennt; für R48, R49 und R50 die Vereinigung aus Unterpunkt und R51-Liste; keine Marke in Abschnitt 10 und im ERZEUGT-Block; in Abschnitt 9 genau eine (R48 (b), R51); „3, Zahlenteil“ unmittelbar nach `<!-- ENDE ERZEUGT -->`; nie in ein Zitat oder einen Codeblock hinein. Wortlaut (zwei Zeilen, davor eine Leerzeile):

```
> ⭐ **<Ort> <PRÄZISIERT|ERGÄNZT|BERICHTIGT> durch R<nn> (<x.n>)** (Fable <27c|29b|30a> R<nn>, TB-126, ⟨DATUM⟩).
> Eintrag und Stand oben bleiben zeichengleich.
```

Die Markenwörter sind die, die `docs/werkzeuge/registerkopie.py --marken` erkennt (Z. 56–57). Anhang A nutzt zusätzlich die Varianten „…, Unterpunkt (x)“, „(Verweis)“ und für Abschnitt 50 die Form ohne R-Block („durch 50.3 und 50.4“); massgeblich ist der Wortlaut in Anhang A.

**Kette je Block:** `**Kette:** Marken: <Orte dieses Blocks aus Anhang A, Spalte „Registerstelle“ ohne den Klammerzusatz, kommagetrennt, in der Reihenfolge von Tabelle 2> | keine.` Dahinter, je wo zutreffend: „Voraussetzung gemessen: 50.1.“ (R25, R26, R28, R33, R36, R41, R48, R49, R50, R53, R54, R55) · „Feldliste: 50.2.“ (R39) · „Zählweise: 50.5.“ (R53) · „Entscheid: 50.6.“ (R24) · „Abschnitt 10: Indexzeile, keine Marke.“ (Ziel in Abschnitt 10, Anhang A Liste A).

**A3. Text von Abschnitt 50** — wird nach 49 angehängt, zeichengleich, mit ⟨S0⟩ ersetzt; die Platzhalter füllt A4:

````
## 50. Tatsachennotizen zu E-2 (TB-126)

Tatsachennotizen des steuernden Chats zu den Voraussetzungen, die Fable in 27c, 29b und 30a „zu messen“ nennt, dazu die Vollzugsnotizen TB-122 und TB-124 nach 37.3. Gemessen über die Geräteanbindung, nur lesend, am 29. und 30.09.2026 (`docs/projektfuehrung/VORMESSUNG_E-2_2026-09-29.md` samt Nachträgen); die Sitzung TB-126 hat in Schritt 0 gemessen, dass die genannten Code-Dateien seither unverändert sind (`docs/belege/TB-126/0f_unveraendert.txt`). Zeilenangaben gelten am Commit ⟨S0⟩. Kein Ergebnis gelesen (27.1). Eine Voraussetzung, deren Messung abweicht, steht hier mit dem Befund. Der Block steht trotzdem in 47–49, wo Fable den Abweichungsfall im Block selbst regelt oder beantwortet hat (R41: 30a, Teil 0; R48 (g): R54). Wo ein Befund eine Lesart des steuernden Chats braucht, steht das ausdrücklich da; sie geht mit der nächsten Anfrage an Fable (R48 (d), 50.5). Die Nummer hat der steuernde Chat vergeben, nicht Fable.

### 50.1 Voraussetzungen und Befunde

| R | Voraussetzung (Fable) | gemessen | Stand |
|---|---|---|---|
| R25 (47.8) | Docstring trägt „unter dem Modus“ seit TB-117 Block D | `research/vorregistrierung/auswertung.py:53–62` (nicht 51–52): „unter dem Selektionsmodus fuer JEDEN der neun Bots geprueft, sonst Abbruch mit 2“ | passt; Fundstelle berichtigt |
| R26 (47.9) | `--bot` läuft unter dem Modus bis zum Bericht (Fable nannte J-7) | Gemessen in TB-117 E (`docs/belege/TB-117/e_auswertung_modus.txt`, HEAD `852f253`, „modus_gut: rc 0“), nicht in J-7; `auswertung.py` seither unverändert (TB-126, 0f). Ein Laufwrapper nach 35.4 wurde nicht gefunden | passt in der Sache am Stand `852f253` (Fundstelle E statt J-7, von Fable bestätigt, 30a, Teil 0); an ⟨S0⟩ ohne Lauf nicht neu gemessen (50.7) |
| R28 (47.11) | Probe von `snapshot.py` gegen Register 18 | fehlte am 29.09.2026; gebaut in TB-124 D: `shared/test_verankerter_datenstand.py`, 3/3, Commit `7453469` (`docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Abschnitt 5, `docs/belege/TB-124/d_probe.txt`). Nebenbefund: ein weiteres Literal des Datenstands, `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97`, ohne eigene Registerprobe; R28 nennt es nicht | erfüllt; Nebenbefund offen (50.7) |
| R33 (48.1) | der Vertrag führt die Trade-Zahl je (Zelle, Falte) | `n_trades`, `auswertung.py:39`, Pflichtspalte Z. 133 | passt |
| R36 (48.4) | MtM-Drawdown in der Falte, Basis Faltenbeginn | `research/mtm_drawdown/mtm_kern.py:296–304` (Basis: letzter Rastertag vor `von`), Raster Z. 135–139. Der Vertrag führt heute nur `kapital_drawdown_pct`; die zwei Spalten nach R36 kommen mit dem Zellen-Erzeuger | passt |
| R41 (48.9) | Haltedauer in 15.4: Kerzenzahl oder Zeitstempeldifferenz? | Zeitstempeldifferenz: `research/faltenplan_neun/embargo_neun.py:36–37, 236–238` | weicht ab ⇒ Abweichungsfall nach R41, von Fable bestätigt (30a, Teil 0); Marke an 15.4; Neurechnung nach 41.3 C2 offen (50.7) |
| R48 (c) (48.16) | die von `auswertung.py` im Fall Spitze ausgegebene Zelle | `auswertung.py:554–556`; ausgegeben wird immer der Plateau-Gewinner mit Markierung (Z. 710–719) | passt; den Randfall ohne zulässigen Nicht-Spitzen-Punkt regelt R55 (49.3) |
| R48 (d) (48.16) | Bildung von `mittlere_exposure` im Vertrag, in `auswertung.py` und in `mtm_kern.py` | nicht gebildet: `auswertung.py:405` liest sie als Eingabe; `mtm_kern.py` führt keine Exposure (nur `gebunden`, zum Einstand, Z. 186–188); `research/exposure_messung/exposure_kern.py` und `research/exposure_messung/auswertung.py:234` teilen `gebunden / kapital_start`, bewertet zum Einstand | An den drei Orten, die R48 (d) nennt, nicht gebildet; ausserhalb davon zum Einstand bewertet. **Lesart des steuernden Chats:** Wo der Code die Grösse nicht hat, gilt der Registertext (R48 (d): „der Registertext folgt dem Code, wo er ihn hat“). An Fable (50.7); offen bis zum Zellen-Erzeuger |
| R48 (f) (48.16) | Markierungen in `auswertung.py`: Kante einschliesslich der Zusatzstufen | Kante nach Position (`auswertung.py:466`); „kein“ ist immer die letzte Stufe, „structural“ wird nach Weite einsortiert (`research/vorregistrierung/registerdaten.py:574–583`) | passt nach Fables Lesart „eingeschlossen = zählt als Stufe mit“ (30a, Teil 0) |
| R48 (g) (48.16) | Perzentilbildung im Code | T − 1 Verschiebungen (`research/vorregistrierung/kennzahlen.py:197`), `np.percentile` (Z. 201); die Rendite wird verkettet (`np.prod`, Z. 199) | T − 1 und Perzentil passen; „Summe“ berichtigt durch R54 (49.2) |
| R48 (i) (48.16) | `pruefe_grenzsaetze.py` prüft die Satzfelder | `research/vorregistrierung/pruefe_grenzsaetze.py:100–148` | passt |
| R49 (b) (48.17) | eine Funktion in `registerdaten.py` bildet die Quantil-Stufen | gebildet in `research/vorregistrierung/messgroessen.py::je_zeitrahmen` (Z. 169–219); `registerdaten.py:558–565` (`achse_werte`) liest nur. Universum aus `config/sp500_top150.txt` und `config/top25_symbols.txt`; der Zeitraum steht nur in `datenbereiche`, nicht in einem eigenen Feld | gemessen; der Ort weicht ab (nicht `registerdaten.py`) |
| R50 (48.18) | Grenzsatz je Rastergrenze; fasst `registerbericht.py` gleiche Sätze zusammen? | Jede Grenze trägt `satz` über `_grenze` (`registerdaten.py:270`); Dubletten werden zusammengefasst (`research/vorregistrierung/registerbericht.py:111–120`). Der Zellenname steht in `auswertung.py::zelle_id` (Z. 272–274), die Cluster in `kennzahlen.py::cluster_anzahl` | Ob: ja und ja; Orte teils anders als in R50; die Zahl „34“ nicht gemessen (50.7) |
| R53 (49.1) | oberste Stufe jeder Rückblick-Achse und feste Fenster je Bot maschinell aus `registerdaten.py` lesbar? | Stufen: `registerdaten.raster()` über `achse_werte`, die oberste ist der letzte Wert je Achse; Bollinger-Fenster: `regel_wert({"regel": "bollinger_fenster"}, …)` gibt 20.0 (Z. 213–216). Für weitere feste Fenster (`VOLUME_AVG_PERIOD`, fester Warm-up der Turtle-Soup-Bots) gibt es keinen Eintrag; `donchian_period` ist eine Rasterachse | teilweise. R53 sagt „nicht als Literal“; „Literal mit Test nach 32.5 (c)“ nennt Fable nur unter „Unsicher“ (30a) — Reibung, an Fable; entschieden wird mit R53 (a) (50.7). Zählweise: 50.5 |
| R54 (49.2) | liest und rechnet irgendein Code `netto_rendite_pct` aus dem Vertrag? | Pflichtspalte `auswertung.py:134`; gelesen nur für die Bestätigungsperiode (Z. 624), berichtet in Z. 823; `netto_rendite_pct_ueber_selektionsfalten` (Z. 675) kommt aus `bereinigung["strategie_rendite_pct"]`, nicht aus der Spalte | trifft zu: Berichtsgrösse ohne Leser im Urteil |
| R55 (49.3) | Nebenfall „keine Zelle zulässig“ | nicht gemessen; im Hauptfall rechnet der Code `None ⇒ False` | Hauptfall passt; Nebenfall erschlossen, Probe offen (50.7) |

### 50.2 R39 (48.7) — Feldliste der Ausgaben, gemessen aus dem Docstring von `auswertung.py`

R39 verlangt, die Feldliste jeder Ausgabe des Zellen-Erzeugers als Registertext „aus dem Docstring von auswertung.py gemessen“ einzutragen, nicht abgeschrieben. Gemessen am Commit ⟨S0⟩, `research/vorregistrierung/auswertung.py` Z. ⟨Z_A⟩–⟨Z_B⟩, zeichengleich:

```
⟨ZITAT_DOCSTRING⟩
```

„`benchmark_tagesreihen/<markt>.csv`“ im Zitat lies „`<bot>.csv`“ (R39). Für `zellenbericht.csv` (R34), `symbole_je_falte.csv` (R38) und das Lese-Audit führt der Docstring heute keine Feldliste; sie kommt mit dem Zellen-Erzeuger (R46) und wird dann hier nachgetragen.

### 50.3 Vollzug TB-122 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` Z. 235–275 (Commit ⟨S0⟩). Der „Stand 11.3“ darin ist der vom 29.09.2026; den dort offenen Scanbeginn hat TB-124 geschlossen (50.4).*

⟨ENTWURF_TB122⟩

### 50.4 Vollzug TB-124 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` Z. 289–323 (Commit ⟨S0⟩). Abgenommen vom steuernden Chat am 30.09.2026; die Befunde der Abnahme berühren keinen Satz dieses Entwurfs. Der Schlusssatz („Der Scanbeginn der Zelle liegt an ihrem Vorlauf …“) folgt der Lesart in 50.5.*

⟨ENTWURF_TB124⟩

### 50.5 Lesart des steuernden Chats zu R53 (49.1) — Zählweise des Vorlaufs

⚠️ **Vorläufig, bis Fable bestätigt** (Bauart 46.9).

R53 nennt die Regel, nicht die Werte (30a, „Unsicher“ zu Frage 1). Wörtlich addiert ergäbe „oberste Stufe zuzüglich der festen Fenster“ bei den zwei Volatility-Breakout-Bots L + 20 (Bollinger-Fenster 20). Aus dem Code hergeleitet ist der erste Balken, an dem die Einstiegsbedingung einer Zelle definiert ist, `BB_PERIOD + L − 1`, also L + 19. Das Bollinger-Fenster über `close` und das Squeeze-Fenster L über `bb_width` sind zwei hintereinanderliegende rollende Fenster ohne `min_periods`, die sich einen Balken teilen (`docs/belege/TB-124/b1_herleitung.txt`, je Stufe von `bb_lookback` und Voreinstellung; Nachtrag 1 zu TB-124). Dieser Eintrag liest R53 als den hergeleiteten Wert, also den ersten definierten Index, nicht als Summe von Fensterlängen. Das ist eine Lesart des steuernden Chats; sie geht mit der nächsten Anfrage an Fable zur Bestätigung. Für die übrigen sieben Bots ist der Vorlauf noch nicht hergeleitet; das geschieht mit R53 (a) (50.7).

### 50.6 Tatsachennotiz zu R24 (47.7) — Entscheid des Betreibers

Zur Entscheidungsvorlage in R24 hat der Betreiber am 29.09.2026 per Auswahlkarte „(a) So lassen“ gewählt, die Empfehlung des Verfahrensprüfers (T116-5; `docs/projektfuehrung/UEBERGABE_ARCHIV.md`, Nachtrag 29.09.2026, 12:25, und Umzug 29.09.2026, 20:48, Block 6). Ein Deckel je Bot vor dem Netting ist damit nicht registriert.

### 50.7 Was offen bleibt

| | offen | wann, wo |
|---|---|---|
| 1 | R41: Neurechnung von 15.4 nach 41.3 C2 (Kerzenzählung) | Mac-Messung vor dem Tag |
| 2 | R48 (d): `mittlere_exposure` im Vertrag bilden, bewertet wie die MtM-Reihe | mit dem Zellen-Erzeuger (R46) |
| 3 | R50: die Zahl „34“ (Zählweise), die Ausstiegskonvention der neun `backtest_*.py`; Nebenbefund DSR-Einheiten `kennzahlen.py:222–224` (Vormessung 29.09.2026, Abschnitt 2) | vor dem Tag |
| 4 | R53 (a): Vorlauf je Bot aus `registerdaten.py` rechnen; feste Fenster ohne Eintrag; Herleitung für die übrigen sieben Bots | Handwerk (BACKLOG „Aus Fable 30a“) |
| 5 | R55: Probe „leere Menge ⇒ (d) nicht erfüllt“ mit Gegenprobe, dazu der Nebenfall | Handwerk (BACKLOG „Aus Fable 30a“) |
| 6 | R28: das Literal in `pruefe_abschnitt17.py:97` | Fable zur Kenntnis, dann Handwerk |
| 7 | R39: Feldlisten für `zellenbericht.csv`, `symbole_je_falte.csv`, Lese-Audit | mit dem Zellen-Erzeuger |
| 8 | R42: Punkt 15 im Listentext von Abschnitt 10 | vor dem Tag, nach R42 |
| 9 | R21: Anforderung an das Leiter-Skript, Stufe IV | mit dem Leiter-Skript |
| 10 | R8 (d): Verweis aus Register 9 (45.8) | nach dem Tag; die Marke in 9 aus R51 ist eine andere |
| 11 | R31 (b), R49 (e): Regeln für das Regelwerk (Freigabe nennt die Tests; Marken nennen Bezeichner) | Dokumentationsauftrag |
| 12 | Lesarten und Reibung: 50.5 (Zählweise), R48 (d) (Registertext gilt, wo der Code die Grösse nicht hat), R53 („Literal mit Test“ gegen „nicht als Literal“) | nächste Anfrage an Fable |
| 13 | R26: Lauf von `auswertung.py --bot` unter dem Modus an einem Stand nach ⟨S0⟩ | vor dem Tag, mit den Tag-Vorbedingungen |
````

**A4. Füllen der Platzhalter** (Grenzen und Zählungen geprüft in 0g):
- ⟨ZITAT_DOCSTRING⟩: die Zeilen von `research/vorregistrierung/auswertung.py` am Commit ⟨S0⟩ von der Zeile `DIE ROHERGEBNISSE - DER VERTRAG` bis einschliesslich der letzten nicht leeren Zeile vor der Zeile `ZWEI DEFINITIONEN, DIE SONST SCHWEIGEND AUSEINANDERLAUFEN`, unverändert (Einrückung bleibt). ⟨Z_A⟩ und ⟨Z_B⟩ sind deren Zeilennummern. Erwartung des steuernden Chats: Z. 36–67 (gelesen am 01.10.2026, nicht als Soll).
- ⟨ENTWURF_TB122⟩: die Zeilen 235–275 von `docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md` am Commit ⟨S0⟩, unverändert (sie sind schon Blockzitat). Erste Zeile beginnt mit `> **Vollzug TB-30b Posten 3 (11.3) in TB-122`, letzte endet mit `TB-122 Befund F1).`.
- ⟨ENTWURF_TB124⟩: die Zeilen 289–323 von `docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md` am Commit ⟨S0⟩, unverändert. Erste Zeile beginnt mit `> **Vollzug TB-30b Posten 3 (11.3), Teil Scanbeginn`, letzte endet mit `nie früher, nicht später.`.

**A5. Einsetzen.** Eine Vorlage (`a5_vorlage_47_50.md`) mit Platzhaltern und ein Einsetzskript (`a5_eintrag.py`) in der Bauart von `docs/belege/TB-117/abschnitt46_vorlage.md` und `eintrag_register_46.py`. Quellen, Köpfe, Text von 50 und den Daten-Block aus Anhang A liest das Skript aus dem Commit ⟨S0⟩ (`git show ⟨S0⟩:<pfad>`), mit den Zeilenbereichen und der Schnittregel von oben, nicht aus dem Gedächtnis. **Zuerst ein Probelauf gegen eine Kopie; an der Kopie laufen die Textprüfungen aus A6** (R-Diff, Zitate, Überschriften, Marken, numstat gegen das Original, Abschnitt 10 und ERZEUGT-Block). Erst wenn sie grün sind, einmal echt; danach muss das Register `cmp`-gleich mit der Kopie sein. Sonde, `registerbericht.py --pruefen`, `herkunft.register()` und `test_vorregistrierung` lesen das Register am festen Pfad und laufen deshalb am echten Arbeitsbaum, **vor** dem Commit. **Wachen im Skript:** Eingangszeilenzahl 10 347 · jede alte Zeile steht in derselben Reihenfolge im neuen Text · keine neue Zeile zwischen `## 10.` und `## 11.` · keine neue Zeile im ERZEUGT-Block · in Abschnitt 9 **höchstens eine** neue Marke · 47 ist noch nicht vergeben. Die Abschnitte 47–50 werden ans Dateiende angehängt.

**A6. Nachweis** (je ein Skript unter `docs/belege/TB-126/`, unabhängig vom Einsetzskript):
- `a6_r_diff.py`: liest Quellen und Register getrennt und vergleicht jeden der 38 Blöcke mit `diff` ⇒ **38/38 rc 0**. Mutationsprobe an einer **Kopie** des Registers (ein Wort in einem Block geändert) ⇒ rc 1. Belege `a6_r_diff.txt`, `a6_r_diff_mutation.txt`.
- `a6_zitate.py`: die Köpfe 47.0, 48.0, 49.0 und der Text von 50 aus **diesem Auftrag** (am Commit ⟨S0⟩; ⟨S0⟩, ⟨Z_A⟩, ⟨Z_B⟩ und die drei Zitat-Platzhalter durch ihre Werte bzw. Quellen ersetzt) gegen das Register ⇒ 4/4 rc 0; das Docstring-Zitat und die zwei Entwürfe zusätzlich je einzeln gegen ihre Quelle ⇒ 3/3 rc 0.
- Überschriften gegen Anhang A, Tabelle 1 ⇒ 38/38 gleich; Marken: gesetzt / nicht gesetzt gegen Anhang A, je gesetzte Marke die Zeile nachher.
- `git diff --numstat` des Registers ⇒ zweite Spalte **0**.
- Abschnitt 10 und ERZEUGT-Block nachher gegen `0d_*_vorher.txt` ⇒ **bytegleich** (inhaltlich; die Zeilennummern dürfen wandern).
- `registerbericht.py --pruefen` nachher = vorher (0d).
- Sonde: JSON-Bericht ohne `zeilen` nachher = vorher, (ii) 0, „Listentext wie bei Erzeugung: ja“.
- `herkunft.register()` nachher: ≠ vorher, `fehlend []`, 23 Teile. Der neue Wert steht **nur im Ergebnis**, nie im Register (Selbstbezug, 42.5).
- **`test_vorregistrierung`** am echten Register, ohne Zeitgrenze ⇒ 196/196 (`a6_test_vorregistrierung.txt`).

Ist ein Nachweis am echten Register rot: den Diff als `docs/belege/TB-126/abbruch_register.diff` sichern, das Register mit `git checkout -- docs/VORREGISTRIERUNG_neuselektion.md` auf ⟨S0⟩ zurücksetzen, Abbruch. **Das Register wird nur committet, wenn alle Nachweise grün sind.**

Commit `TB-126 A: Register 47–50 (R18–R55 zeichengleich, Tatsachennotizen E-2), Marken`, pushen. **Das ist der einzige Commit, der das Register ändert.**

## Schritt C — Registerkopie und Index

**C1.** Nach dem Commit aus A, am sauberen Stand: `trading-env/bin/python3 docs/werkzeuge/registerkopie.py`, dann `--pruefen`, dann `--marken` ⇒ Ausgaben in `c1_registerkopie.txt`, `c1_pruefen.txt`, `c1_marken.txt`. Jeder Teil höchstens 240 000 B. Meldet das Skript einen Teil als VERALTET: nicht löschen, im Ergebnis nennen. `--pruefen` rc ≠ 0 ⇒ die Teile nicht committen, melden.

**C2.** `docs/projektfuehrung/REGISTER_INDEX.md` nachziehen, nach der Bauart der vorhandenen Zeilen (Kopf Z. 3–4 mit Zeilenzahl, sha256 und Kopf-Commit; Abschnittstabelle um 47–50; Spalte T neu nach C1; Marken neu aus `--marken`; Hinweis Z. 133–135).

**C3. Indexzeilen statt Marken:** die sechs Zeilen aus Anhang A, Liste A, je an der Stelle des alten Orts im Index (Abschnitt 10 bzw. 17.3/17.9/18), mit Verweis auf den neuen Ort. Wo der Index keine passende Stelle hat: als eigener kleiner Block „Indexzeilen aus E-2“.

Commit `TB-126 C: Registerkopie und Index nach E-2`, pushen.

## Schritt D — Abgabe

**D1.** `docs/ERGEBNIS_TB-126_register_e2.md`:
- Kopfzeile mit Inhalt in einem Satz (numstat, Zahl der Marken, Teile der Kopie); Sitzungstitel, Stand, Auftrag, Belege; Eingang und alle Commits; Quellen mit md5 „geprüft“; Freigabe; Umgebung; „Kein Abbruchkriterium ausgelöst“ oder der Grund.
- Kurz-Tabelle je Schritt (Soll | Ist).
- Markentabelle: gesetzt und nicht gesetzt gegen Anhang A, mit Grund (aus 0g und A6).
- `herkunft.register()` vorher und nachher.
- **Für Fable** (nur Verfahrensfragen; der steuernde Chat prüft sie nach dem Fable-Filter vor): die Lesarten 50.5 und R48 (d) und die Reibung R53 (50.7 Nr. 12); der Nebenbefund R28 (50.7 Nr. 6); die Vereinigung der Markenorte für R48–R50 (A2); die Orte aus Anhang A, Listen B und C, ohne Marke (u. a. R21: die „Prüfung vor dem Tag“ in 16.4); jede Reibung zwischen Fable-Text und Register, die beim Setzen der Marken auffiel.
- **Nicht getan:** 50.7; der Status von 27c, 29b und 30a im `FABLE_DIALOG_INDEX.md` (macht der steuernde Chat); die Ablage (macht der steuernde Chat).
- **In einfacher Sprache.**

**D2. Journal:** Block ans Ende von `docs/projektfuehrung/JOURNAL.md`, wie bei den vorhandenen Blöcken hinter den letzten Buchstabenblock. Den Buchstaben vorher messen (erwartet **DX**), mit Quellenzeile auf das Ergebnis. Er enthält zusätzlich diesen Satz, zeichengleich:

```
Tatsachennotiz zu DV: Es sind zehn Paper-Trading-DBs (neun im Wurzelordner, eine unter `strategies/volatility_breakout/`), nicht elf; „11/12 sha256-identisch“ bleibt richtig (Abnahme TB-124 durch den steuernden Chat, 30.09.2026).
```

**D3.** Abgabe-Commit `TB-126 Abgabe: Ergebnis, Journal DX`, pushen. Danach `git status --porcelain` ⇒ `docs/belege/TB-126/d3_porcelain.txt`, kleiner letzter Commit, pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab; ein Ausgangswert aus 0d mit Fundstelle weicht ab; 0f nicht leer; 0e nicht 196/196.
- Ein R-Block-diff rc ≠ 0; ein Zitat-diff rc ≠ 0; die Mutationsprobe gibt nicht rc 1.
- numstat des Registers mit zweiter Spalte ≠ 0; eine alte Zeile fehlt oder steht in anderer Reihenfolge.
- Abschnitt 10 oder ERZEUGT-Block nicht bytegleich; `registerbericht.py --pruefen` nachher ≠ vorher; Sonde: JSON ohne `zeilen` ≠ vorher oder (ii) ≠ 0.
- `test_vorregistrierung` nach dem Einsetzen nicht 196/196.
- Eine Vorprüfung aus 0g (Nr. 2–4) weicht ab, oder mehr als fünf Marken weichen ab (0g Nr. 1).
- Eine Datei ausserhalb der Freigabetabelle müsste geändert werden.
- `git push` scheitert zweimal.

**Kein Abbruch:** ein Anker ≠ 1 (Marke auslassen, nennen) · `git worktree remove` verweigert (nennen) · `registerkopie.py --pruefen` rc ≠ 0 (Teile nicht committen, nennen) · eine Reibung zwischen Fable-Text und Code oder Register (unter „Für Fable“ nennen).

**Bei Abbruch:** committen, was an Belegen da ist, **nie** `JOURNAL.md` mit Platzhalter, Grund in `docs/belege/TB-126/abbruch.txt`, pushen, melden. Kein Registertext mit einem Befund, den dieser Auftrag nicht vorsieht.

## In einfacher Sprache

Fable hat in drei Antworten 38 Regeltexte geschrieben. Diese Sitzung kopiert sie per Skript ins Register, Zeichen für Zeichen, und setzt an den alten Stellen kleine Hinweise auf die neuen. Dazu kommt ein Abschnitt mit dem, was vorher im Code nachgemessen wurde, und die zwei Notizen zu den Code-Änderungen vom 29. und 30.09. Danach wird die Kopie des Registers für Fable neu erzeugt. Am Code ändert sich nichts. Maschinell geprüft wird, dass jeder Text genau so angekommen ist und kein alter Satz verändert wurde.

---

## Anhang A — TB-126: Überschriften und Marken für die Abschnitte 47–49 (Vorlage für die Mac-Sitzung)

**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `41864d4` (10 347 Zeilen, md5 `c8a32c0f0037c6c65bd08aae6be5a7c1`). Quellen: 27c Z. 161–209, 29b Z. 190–267, 30a Z. 25–32, geschnitten nach der Schnittregel des Auftrags (38/38). Gebaut vom Helfer des steuernden Chats am 01.10.2026, nur lesend. **Alle Zeilennummern gelten am Original `41864d4`, vor jeder Einfügung.** Einsetzen deshalb von unten nach oben (grösste Zeilennummer zuerst) oder über eine Abbildung der Originalzeilen.

**Gelesene Regeln, wo der Auftrag Spielraum liess (so angewandt, nicht geraten):**

1. **Überschrift als Anker** (Fable nennt einen ganzen Abschnitt oder Unterabschnitt, z. B. „zu 12“, „zu 22.2“): Einfügestelle ist das **Ende** dieses Abschnitts — nach der letzten nicht leeren Zeile vor der nächsten Überschrift gleicher oder höherer Ebene (`##` umfasst seine `###`; `###` umfasst seine `####`), vor `---`. Damit steht die Marke nach allen dort schon stehenden Marken. So haben es TB-114/TB-117 gehalten („Marken am Ende von 12 und am Ende von 36.5“, 46.5; „am Ende von 40.6“, 46.3).
2. **Eintrag als Anker** (`**B6/B7 — …**`, `**E5 (e) — …**`, `**44-6 — …**`): Ende des Eintrags, vor dem nächsten Eintrag oder der nächsten Überschrift.
3. **Punkt in einem Zitat** (16.4 (a)–(m), 15.3 (b), 15.4 (a), 15.6 (c), 16.7 (d), 25.3 (i), 27.3, R4, R5 (a)/(b), R14): Die Marke geht nie ins Zitat, sondern hinter den ganzen Zitatblock, der den Punkt enthält, und hinter die dort stehenden Marken. Darum stehen z. B. alle Marken zu 16.4 (g)–(m) gesammelt nach Z. 2012, alle zu 16.4 (a)–(d) nach Z. 1968.
4. **Tabellenzeile** (Festlegung 2/3/4, 7 (a)/(d)): nach der Tabelle und den dort stehenden Marken. **Listenpunkt** (5.1 Nr. 7): nach dem Punkt, vor Nr. 8; die Marke steht wie vorgegeben ohne Einrückung bei Spalte 0.
5. **Abschnitt 3, Zahlenteil:** unmittelbar nach `<!-- ENDE ERZEUGT -->` (Z. 430).
6. **Nennt Fable „R14“, „R4“, „R5 (a)“**, ist der Anker die erste Zeile dieses Blocks im Zitat (`> **R14 — …`), nicht die Überschrift 46.5; nennt Fable „46.3“ oder „45.5“, ist es die Überschrift.
7. **Wort:** PRÄZISIERT (Präzisierung, Lesart, also auch alle Unterpunkte von R48), ERGÄNZT (Ergänzung, Tatsachennotiz, Bestätigung), BERICHTIGT (Berichtigung, „lies“). R51-eigene Orte (die nicht an R48/R49/R50 hängen): `ERGÄNZT (Verweis)`, weil „Marke am alten Ort“ keine Entsprechung hat.
8. **R51-Liste und R48/R49/R50:** Ein R51-Ort, dessen Ziel R48/R49/R50 ist (Festlegung 4 über R48 (a) „Marke an Festlegung 4 (R51)“; 9 → R48 (b); 3, Zahlenteil und 4.4 → R49 (c); 11 → R49 (h); 12 → R50; Kopf → R49 (f)), bekommt **eine** Marke dieses R-Blocks (Vereinigung, keine Doppelung). Die übrigen R51-Orte (Festlegung 2 und 7 (a) [A63], 4.2 [A70], 5.3 und 15.6 [A66]) bekommen eine Marke „durch R51“; 29b Teil 2 ordnet A63, A66, A70 ausdrücklich R51 zu (Blöcke III und VI).
9. **B3 im Wortlaut:** Der Auftrag gibt dafür keine eigene Form. 15.4: `durch R41 (48.9) und 50.1`. 16.4: als Ergänzung an den beiden R24-Marken: `durch R24 (47.7) und 50.6` (keine eigene Marke). 11.3: `durch 50.3 und 50.4`, ohne Fable-Teil, weil kein R-Block dahintersteht.
10. Ein Ort, der im Block nur als Fundstelle, als Gegenstand einer Aussage oder in der „Quelle des Grundes“ vorkommt, ohne die Bezugsformen aus Regel 1 („… zu X“, „Zu X:“, „lies“, „Tatsachennotiz zu X“, „Marke an X“, R49, R51), bekommt keine Marke. Diese Orte stehen unten unter **C** zur Entscheidung des steuernden Chats.

## Tabelle 1 — Überschriften (38)

Bezug wörtlich ab „R<n> — “ bis vor den Satzpunkt, ohne `**` und Backticks. Bei R40, R41, R46 ist das vorangestellte „Registertext, “ weggelassen, damit die Zeile mit der Art beginnt. Länge ≤ 120 Zeichen für die **ganze Zeile**; gekürzt nur am Ende, an einer Wortgrenze, mit „…“ (zweimal: R21, R39).

| x.n | R | Quelle | Überschriftzeile (exakt) | Zeichen |
|---|---|---|---|---|
| 47.1 | R18 | 27c | `### 47.1 R18 — Präzisierung zu 16.4 (m), (h) und (l) (Zellenanteil und Klassenschlüssel; L1)` | 92 |
| 47.2 | R19 | 27c | `### 47.2 R19 — Präzisierung zu 16.4 (h), (j) und (k) (Zahl der Zellen; L2; T116-4)` | 82 |
| 47.3 | R20 | 27c | `### 47.3 R20 — Ergänzung zu 16.4 (l) und (j) (Anlage ohne aktive Zelle; L3)` | 75 |
| 47.4 | R21 | 27c | `### 47.4 R21 — Präzisierung zu 16.4 (b), (i) und (j) und Ergänzung zu 7.1 (Schatten nach der Herkunft der Stufe; L4…` | 116 (gekürzt) |
| 47.5 | R22 | 27c | `### 47.5 R22 — Präzisierung zu 16.4 (a) und (i) (Faktor „Bestätigt" vor Netting; L5)` | 84 |
| 47.6 | R23 | 27c | `### 47.6 R23 — Präzisierung zu 16.4 (b), 7.1 und 15.6 (c) (Budgetanteil und Höhe der Benchmark-Position; L0.1; T116-3)` | 118 |
| 47.7 | R24 | 27c | `### 47.7 R24 — Tatsachennotiz zu 16.4 (h) und (g) (Folge der Gleichteilung bei ungleicher Besetzung; T116-5)` | 108 |
| 47.8 | R25 | 27c | `### 47.8 R25 — Bestätigung von 46.9 als Ergänzung zu 12 und R14 (Herkunftsprüfung ohne Modus; T117-1)` | 101 |
| 47.9 | R26 | 27c | `### 47.9 R26 — Ergänzung zu 12, R14 und 35.4 (alle neun unter dem Modus; --bot; T117-2)` | 87 |
| 47.10 | R27 | 27c | `### 47.10 R27 — Tatsachennotiz zu R14 Bedingung 5 und Ergänzung zu den Tag-Vorbedingungen (voller Commit-Hash; T117-3)` | 118 |
| 47.11 | R28 | 27c | `### 47.11 R28 — Tatsachennotiz zu Register 18 und Plan-Punkt 6 (drei Orte des Datenstands; T117-4)` | 98 |
| 47.12 | R29 | 27c | `### 47.12 R29 — Ergänzung zu 42.2 E5, R4 und R5 (a); Tatsachennotiz zu 44-6 (herkunft.py im Laufbereich; T117-5)` | 112 |
| 47.13 | R30 | 27c | `### 47.13 R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen (Erzeuger und Auswertung am Tag-Commit; T117-6)` | 109 |
| 47.14 | R31 | 27c | `### 47.14 R31 — Tatsachennotizen 27c` | 36 |
| 47.15 | R32 | 27c | `### 47.15 R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026)` | 107 |
| 48.1 | R33 | 29b | `### 48.1 R33 — Berichtigung zu 45.5 (b) (Zeilen in zellen.csv)` | 62 |
| 48.2 | R34 | 29b | `### 48.2 R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht)` | 57 |
| 48.3 | R35 | 29b | `### 48.3 R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz` | 63 |
| 48.4 | R36 | 29b | `### 48.4 R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt)` | 99 |
| 48.5 | R37 | 29b | `### 48.5 R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 (zwei Zeiträume, ein Name)` | 93 |
| 48.6 | R38 | 29b | `### 48.6 R38 — Ergänzung zu 16.7 (d) (Ort der Berichtsgrössen)` | 62 |
| 48.7 | R39 | 29b | `### 48.7 R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags (Ausgaben des Zellen-Erzeugers; Feldliste als…` | 120 (gekürzt) |
| 48.8 | R40 | 29b | `### 48.8 R40 — Ersteintrag — Schreibregel für Ausgaben der Erzeuger` | 67 |
| 48.9 | R41 | 29b | `### 48.9 R41 — Ergänzung zu 41.2 B6/B7 und 15.3 (b) (haltedauer_balken)` | 71 |
| 48.10 | R42 | 29b | `### 48.10 R42 — Ergänzung zu 40.6, 45.3, 46.3 (Bindung der neuen Listen)` | 72 |
| 48.11 | R43 | 29b | `### 48.11 R43 — Registertext zum Zellen-Kern; Berichtigung zu 29.4/34.5 (Ort der Wache); Tatsachennotiz zu 11.2` | 111 |
| 48.12 | R44 | 29b | `### 48.12 R44 — Ergänzung zu 40.6 (Reihenfolge der Neuerzeugung)` | 64 |
| 48.13 | R45 | 29b | `### 48.13 R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen)` | 76 |
| 48.14 | R46 | 29b | `### 48.14 R46 — Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag` | 70 |
| 48.15 | R47 | 29b | `### 48.15 R47 — Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“)` | 80 |
| 48.16 | R48 | 29b | `### 48.16 R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle` | 69 |
| 48.17 | R49 | 29b | `### 48.17 R49 — Tatsachennotizen zu Register 0–12 (TB-121), Marke je am alten Ort` | 81 |
| 48.18 | R50 | 29b | `### 48.18 R50 — Ergänzung zu 12 (Kennzahlendefinitionen im Code) und Tatsachennotiz zu TB-121` | 93 |
| 48.19 | R51 | 29b | `### 48.19 R51 — Marken am alten Ort für Register 0–12 (Handwerk im Registerauftrag; der alte Satz bleibt zeichengleich)` | 119 |
| 48.20 | R52 | 29b | `### 48.20 R52 — Tatsachennotizen 29b` | 36 |
| 49.1 | R53 | 30a | `### 49.1 R53 — Präzisierung zu 4a (i) (25.3, 28.6): Indikator-Vorlauf bei achsenabhängigem Rückblick` | 100 |
| 49.2 | R54 | 30a | `### 49.2 R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen)` | 100 |
| 49.3 | R55 | 30a | `### 49.3 R55 — Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz` | 66 |

## Tabelle 2 — Marken (87 am alten Ort + 1 unter 48.16 = 88)

Sortiert nach Einfügestelle, an derselben Stelle nach R aufsteigend (Regel 6); B3 ohne R-Block zuletzt. Jede Marke: Leerzeile, Markenzeile 1, Markenzeile 2 `> Eintrag und Stand oben bleiben zeichengleich.` „Zahl“ = `str.count` des Ankers über den ganzen Registertext am `41864d4`. In Ankern steht `\|` für `|` (Tabellensyntax); Anker mit Backtick stehen in doppelten Backticks mit je einem Leerzeichen innen. **Massgeblich für Skripte ist der JSON-Block am Ende.**

| Nr | R (x.n) | Ziel laut Fable (wörtlich, kurz) | Registerstelle | Anker | Zahl | Einfügestelle | Markenzeile 1 (exakt) |
|---|---|---|---|---|---|---|---|
| 1 | R49 (48.17) (f) | Zum Kopf des Registers: „Stand: 14.09.2026“ (R51: Kopf →) | Kopf, Absatz „Stand: 14.09.2026“ (Ankerzeile 3) | `**Stand: 14.09.2026. Dies` | 1 | nach Zeile 4 (am 41864d4): `und danach nicht mehr verhandelt.**` | `> ⭐ **Kopf (Stand 14.09.2026) ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (f), TB-126, ⟨DATUM⟩).` |
| 2 | R48 (48.16) (a) | Festlegung 4 … Marke an Festlegung 4 (R51); R51: Festlegung 4 → | 1, Tabelle, Zeile 4 (Ankerzeile 59) | `\| 4 \| Drawdown-Bedingung` | 1 | nach Zeile 69 (am 41864d4): `> ⭐ **Festlegung 1 PRÄZISIERT durch Absc` | `> ⭐ **Festlegung 4 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (a), TB-126, ⟨DATUM⟩).` |
| 3 | R48 (48.16) (j) | Festlegung 3 bei weniger als drei Selektionsfalten: | 1, Tabelle, Zeile 3 (Ankerzeile 58) | `\| 3 \| Beurteilung \| Netto-Calmar,` | 1 | nach Zeile 69 (am 41864d4): `> ⭐ **Festlegung 1 PRÄZISIERT durch Absc` | `> ⭐ **Festlegung 3 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (j), TB-126, ⟨DATUM⟩).` |
| 4 | R51 (48.19) | Festlegung 2 und 7 (a) → 15.3 (c) und Formelzeile [A63] | 1, Tabelle, Zeile 2 (Ankerzeile 57) | `\| 2 \| Selektionsstatistik` | 1 | nach Zeile 69 (am 41864d4): `> ⭐ **Festlegung 1 PRÄZISIERT durch Absc` | `> ⭐ **Festlegung 2 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).` |
| 5 | R48 (48.16) (i) | Die Ziffernregel aus 2.1 | 2.1 (Ankerzeile 86) | `### 2.1 Wie sie entstehen` | 1 | nach Zeile 113 (am 41864d4): `nicht später versehentlich verschärft wi` | `> ⭐ **2.1 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (i), TB-126, ⟨DATUM⟩).` |
| 6 | R48 (48.16) (h) | haltedauer (2.2) | 2.2 (Ankerzeile 115) | `### 2.2 Die vier zulässigen` | 1 | nach Zeile 127 (am 41864d4): `Beide Sätze nennen **keine Zahl**; die W` | `> ⭐ **2.2 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (h), TB-126, ⟨DATUM⟩).` |
| 7 | R49 (48.17) (a) | Zu 2.2: | 2.2 (Ankerzeile 115) | `### 2.2 Die vier zulässigen` | 1 | nach Zeile 127 (am 41864d4): `Beide Sätze nennen **keine Zahl**; die W` | `> ⭐ **2.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (a), TB-126, ⟨DATUM⟩).` |
| 8 | R48 (48.16) (f) | Kante (2.5): | 2.5 (Ankerzeile 165) | `### 2.5 Die Kantenregel` | 1 | nach Zeile 180 (am 41864d4): `unverändert bleibt.` | `> ⭐ **2.5 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (f), TB-126, ⟨DATUM⟩).` |
| 9 | R49 (48.17) (b) | Zu 2.7: | 2.7 (Ankerzeile 207) | `### 2.7 Stufung` | 1 | nach Zeile 218 (am 41864d4): `Bots gelten.` | `> ⭐ **2.7 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (b), TB-126, ⟨DATUM⟩).` |
| 10 | R49 (48.17) (c) | Zu 3 und 4.4: (R51: 3, Zahlenteil und 4.4 →) | 3, Zahlenteil (nach ENDE ERZEUGT) (Ankerzeile 430) | `<!-- ENDE ERZEUGT -->` | 1 | nach Zeile 430 (am 41864d4): `<!-- ENDE ERZEUGT -->` | `> ⭐ **Abschnitt 3 (Zahlenteil) ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (c), TB-126, ⟨DATUM⟩).` |
| 11 | R51 (48.19) | 4.2 → 43-2 (Interpolation an den Rändern) [A70] | 4.2 (Ankerzeile 451) | `` ### 4.2 Warum `DD_Benchmark` `` | 1 | nach Zeile 484 (am 41864d4): `Exposure-Argument, nicht über die Tabell` | `> ⭐ **4.2 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).` |
| 12 | R49 (48.17) (c) | Zu 3 und 4.4: | 4.4 (Ankerzeile 509) | `### 4.4 Ist die Bedingung` | 1 | nach Zeile 536 (am 41864d4): `darüber.` | `> ⭐ **4.4 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (c), TB-126, ⟨DATUM⟩).` |
| 13 | R37 (48.5) | Präzisierung zu … 5.1 Nr. 7 | 5.1, Nr. 7 (Ankerzeile 593) | `7. **Die letzte Falte wird` | 1 | nach Zeile 596 (am 41864d4): `   Selektion. **Und sie wächst jeden Mon` | `> ⭐ **5.1 Nr. 7 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).` |
| 14 | R51 (48.19) | 5.3 und 15.6 → 33.2 (gültiger Faltenplan, alle neun Bots) [A66] | 5.3 (Ankerzeile 621) | `### 5.3 Krypto: Platzhalter` | 1 | nach Zeile 646 (am 41864d4): `auszuwerten — es gibt dann keine Zahl, d` | `> ⭐ **5.3 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).` |
| 15 | R48 (48.16) (c) | Abschnitt 7 (d): | 7, Tabelle, Zeile (d) (Ankerzeile 753) | `\| **(d)** \| Der Gewinner` | 1 | nach Zeile 753 (am 41864d4): `\| **(d)** \| Der Gewinner ist eine **Spit` | `> ⭐ **7 (d) PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (c), TB-126, ⟨DATUM⟩).` |
| 16 | R51 (48.19) | Festlegung 2 und 7 (a) → 15.3 (c) und Formelzeile [A63] | 7, Tabelle, Zeile (a) (Ankerzeile 750) | `\| **(a)** \| Falten-Median` | 1 | nach Zeile 753 (am 41864d4): `\| **(d)** \| Der Gewinner ist eine **Spit` | `> ⭐ **7 (a) ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).` |
| 17 | R55 (49.3) | Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz | 7, Tabelle, Zeile (d) (Ankerzeile 753) | `\| **(d)** \| Der Gewinner` | 1 | nach Zeile 753 (am 41864d4): `\| **(d)** \| Der Gewinner ist eine **Spit` | `> ⭐ **7 (d) ERGÄNZT durch R55 (49.3)** (Fable 30a R55, TB-126, ⟨DATUM⟩).` |
| 18 | R21 (47.4) | Ergänzung zu 7.1 | 7.1 (Ankerzeile 777) | `### 7.1 Die drei Regeln für` | 1 | nach Zeile 793 (am 41864d4): `> zeichengleich.` | `> ⭐ **7.1 ERGÄNZT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).` |
| 19 | R23 (47.6) | Präzisierung zu … 7.1 | 7.1 (Ankerzeile 777) | `### 7.1 Die drei Regeln für` | 1 | nach Zeile 793 (am 41864d4): `> zeichengleich.` | `> ⭐ **7.1 PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, ⟨DATUM⟩).` |
| 20 | R48 (48.16) (g) | Zufalls-Timing (8.1): | 8.1 (Ankerzeile 821) | `### 8.1 Der Zufalls-Timing-Test` | 1 | nach Zeile 839 (am 41864d4): `Bots tut sie das.` | `> ⭐ **8.1 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (g), TB-126, ⟨DATUM⟩).` |
| 21 | R48 (48.16) (b) | Abschnitt 9: … „N = 653 plus …“ ist die Kurzform; R51: 9 → R48 (b) | 9, erster Absatz (Ankerzeile 845) | `**N = 653 plus die Zellen` | 1 | nach Zeile 848 (am 41864d4): `` `registerdaten.N_HISTORISCH_JE_BOT` und  `` | `> ⭐ **Abschnitt 9 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (b), TB-126, ⟨DATUM⟩).` |
| 22 | R43 (48.11) | Tatsachennotiz zu 11.2 | 11.2 (Ankerzeile 1119) | `### 11.2 Agent 2 — Auswahl` | 1 | nach Zeile 1141 (am 41864d4): `Prüfungen aus TB-22 bestehen unverändert` | `> ⭐ **11.2 ERGÄNZT durch R43 (48.11)** (Fable 29b R43, TB-126, ⟨DATUM⟩).` |
| 23 | R49 (48.17) (h) | Zu 11: (R51: 11 →) | Abschnitt 11 (Ankerzeile 1087) | `## 11. Voraussetzungen des` | 1 | nach Zeile 1157 (am 41864d4): `> zeichengleich.` | `> ⭐ **Abschnitt 11 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (h), TB-126, ⟨DATUM⟩).` |
| 24 | B3 (50.3/50.4) | Vollzug Posten 3 (11.3): Tatsachennotizen 50.3 und 50.4 | 11.3 (Ankerzeile 1143) | `### 11.3 Zwei Achsen brauchen` | 1 | nach Zeile 1157 (am 41864d4): `> zeichengleich.` | `> ⭐ **11.3 ERGÄNZT durch 50.3 und 50.4** (Tatsachennotiz, Vollzug TB-122 und TB-124 nach 37.3, TB-126, ⟨DATUM⟩).` |
| 25 | R25 (47.8) | als Ergänzung zu 12 | Abschnitt 12 (Ankerzeile 1161) | `## 12. Der Vollständigkeitstest` | 1 | nach Zeile 1222 (am 41864d4): `> zeichengleich.` | `> ⭐ **Abschnitt 12 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, ⟨DATUM⟩).` |
| 26 | R26 (47.9) | Ergänzung zu 12 | Abschnitt 12 (Ankerzeile 1161) | `## 12. Der Vollständigkeitstest` | 1 | nach Zeile 1222 (am 41864d4): `> zeichengleich.` | `> ⭐ **Abschnitt 12 ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, ⟨DATUM⟩).` |
| 27 | R49 (48.17) (d) | Zu 12: | Abschnitt 12 (Ankerzeile 1161) | `## 12. Der Vollständigkeitstest` | 1 | nach Zeile 1222 (am 41864d4): `> zeichengleich.` | `> ⭐ **Abschnitt 12 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (d), TB-126, ⟨DATUM⟩).` |
| 28 | R50 (48.18) | Ergänzung zu 12 (R51: 12 → R50) | Abschnitt 12 (Ankerzeile 1161) | `## 12. Der Vollständigkeitstest` | 1 | nach Zeile 1222 (am 41864d4): `> zeichengleich.` | `> ⭐ **Abschnitt 12 ERGÄNZT durch R50 (48.18)** (Fable 29b R50, TB-126, ⟨DATUM⟩).` |
| 29 | R41 (48.9) | Ergänzung zu … 15.3 (b) | 15.3 (b) (Ankerzeile 1328) | `> **(b)** Verfahren: stationärer` | 1 | nach Zeile 1338 (am 41864d4): `> Trades je Falte wird für den Gewinner ` | `> ⭐ **15.3 (b) ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, ⟨DATUM⟩).` |
| 30 | R35 (48.3) | Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz | 15.3 (Ankerzeile 1322) | `### 15.3 Registertext 1 —` | 1 | nach Zeile 1356 (am 41864d4): `> zeichengleich.` | `> ⭐ **15.3 ERGÄNZT durch R35 (48.3)** (Fable 29b R35, TB-126, ⟨DATUM⟩).` |
| 31 | R54 (49.2) | Berichtigung zu Registertext 2a (15.4) … lies | 15.4 (a) (Ankerzeile 1362) | `> **(a)** Selektionsfalten` | 1 | nach Zeile 1381 (am 41864d4): `> als **obere Schranke** weiter.` | `> ⭐ **2a (15.4 (a)) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, ⟨DATUM⟩).` |
| 32 | R41 (48.9) · B3 | „15.4 erhält eine Tatsachennotiz“ (Abweichungsfall, 30a Teil 0; Befund 50.1) | 15.4 (Ankerzeile 1360) | `### 15.4 Registertext 2 —` | 1 | nach Zeile 1423 (am 41864d4): `> (42.6 (5)). Die Tabelle bleibt zeichen` | `> ⭐ **15.4 ERGÄNZT durch R41 (48.9) und 50.1** (Fable 29b R41, TB-126, ⟨DATUM⟩).` |
| 33 | R53 (49.1) | Tatsachennotiz: … 15.5 … | 15.5 (Ankerzeile 1427) | `### 15.5 Registertext 3 —` | 1 | nach Zeile 1535 (am 41864d4): `hätte jeder Bot seine eigene, wie die Ta` | `> ⭐ **15.5 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).` |
| 34 | R23 (47.6) | Präzisierung zu … 15.6 (c) | 15.6 (c) (Ankerzeile 1553) | `> **(c)** *[ersetzt „behält` | 1 | nach Zeile 1562 (am 41864d4): `> geschrieben.` | `> ⭐ **15.6 (c) PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, ⟨DATUM⟩).` |
| 35 | R51 (48.19) | 5.3 und 15.6 → 33.2 (gültiger Faltenplan, alle neun Bots) [A66] | 15.6 (Ankerzeile 1539) | `### 15.6 Registertext 4 —` | 1 | nach Zeile 1609 (am 41864d4): `   Werkzeug führt beide Listen und der S` | `> ⭐ **15.6 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).` |
| 36 | R21 (47.4) | Präzisierung zu 16.4 (b) | 16.4 (b) (Ankerzeile 1943) | `> **(b)** Nach dem Selektionslauf` | 1 | nach Zeile 1968 (am 41864d4): `> **Bestätigt seit mindestens zwei Quart` | `> ⭐ **16.4 (b) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).` |
| 37 | R22 (47.5) | Präzisierung zu 16.4 (a) | 16.4 (a) (Ankerzeile 1938) | `> **(a)** Jeder Bot steht` | 1 | nach Zeile 1968 (am 41864d4): `> **Bestätigt seit mindestens zwei Quart` | `> ⭐ **16.4 (a) PRÄZISIERT durch R22 (47.5)** (Fable 27c R22, TB-126, ⟨DATUM⟩).` |
| 38 | R23 (47.6) | Präzisierung zu 16.4 (b) | 16.4 (b) (Ankerzeile 1943) | `> **(b)** Nach dem Selektionslauf` | 1 | nach Zeile 1968 (am 41864d4): `> **Bestätigt seit mindestens zwei Quart` | `> ⭐ **16.4 (b) PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, ⟨DATUM⟩).` |
| 39 | R37 (48.5) | Präzisierung zu … 16.4 (c) | 16.4 (c) (Ankerzeile 1949) | `> **(c)** **Aufstieg** Grundbudget` | 1 | nach Zeile 1968 (am 41864d4): `> **Bestätigt seit mindestens zwei Quart` | `> ⭐ **16.4 (c) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).` |
| 40 | R37 (48.5) | Präzisierung zu … 16.4 …/(d) | 16.4 (d) (Ankerzeile 1958) | `> **(d)** **Abstieg** auf` | 1 | nach Zeile 1968 (am 41864d4): `> **Bestätigt seit mindestens zwei Quart` | `> ⭐ **16.4 (d) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).` |
| 41 | R18 (47.1) | Präzisierung zu 16.4 (m) | 16.4 (m) (Ankerzeile 2006) | `> **(m)** **Umsetzung ohne` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (m) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, ⟨DATUM⟩).` |
| 42 | R18 (47.1) | Präzisierung zu 16.4 … (h) | 16.4 (h) (Ankerzeile 1984) | `> **(h)** Eine Zelle ist` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (h) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, ⟨DATUM⟩).` |
| 43 | R18 (47.1) | Präzisierung zu 16.4 … (l) | 16.4 (l) (Ankerzeile 2002) | `> **(l)** ⭐ **Anlageklassen-Schlüssel,` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (l) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, ⟨DATUM⟩).` |
| 44 | R19 (47.2) | Präzisierung zu 16.4 (h) | 16.4 (h) (Ankerzeile 1984) | `> **(h)** Eine Zelle ist` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (h) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, ⟨DATUM⟩).` |
| 45 | R19 (47.2) | Präzisierung zu 16.4 … (j) | 16.4 (j) (Ankerzeile 1993) | `> **(j)** **Aufstieg:** mehr` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (j) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, ⟨DATUM⟩).` |
| 46 | R19 (47.2) | Präzisierung zu 16.4 … (k) | 16.4 (k) (Ankerzeile 1998) | `> **(k)** Wird eine **neue` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (k) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, ⟨DATUM⟩).` |
| 47 | R20 (47.3) | Ergänzung zu 16.4 (l) | 16.4 (l) (Ankerzeile 2002) | `> **(l)** ⭐ **Anlageklassen-Schlüssel,` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (l) ERGÄNZT durch R20 (47.3)** (Fable 27c R20, TB-126, ⟨DATUM⟩).` |
| 48 | R20 (47.3) | Ergänzung zu 16.4 … (j) | 16.4 (j) (Ankerzeile 1993) | `> **(j)** **Aufstieg:** mehr` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (j) ERGÄNZT durch R20 (47.3)** (Fable 27c R20, TB-126, ⟨DATUM⟩).` |
| 49 | R21 (47.4) | Präzisierung zu 16.4 … (i) | 16.4 (i) (Ankerzeile 1989) | `> **(i)** Innerhalb einer` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (i) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).` |
| 50 | R21 (47.4) | Präzisierung zu 16.4 … (j) | 16.4 (j) (Ankerzeile 1993) | `> **(j)** **Aufstieg:** mehr` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (j) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).` |
| 51 | R22 (47.5) | Präzisierung zu 16.4 … (i) | 16.4 (i) (Ankerzeile 1989) | `> **(i)** Innerhalb einer` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (i) PRÄZISIERT durch R22 (47.5)** (Fable 27c R22, TB-126, ⟨DATUM⟩).` |
| 52 | R24 (47.7) | Tatsachennotiz zu 16.4 (h) | 16.4 (h) (Ankerzeile 1984) | `> **(h)** Eine Zelle ist` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (h) ERGÄNZT durch R24 (47.7) und 50.6** (Fable 27c R24, TB-126, ⟨DATUM⟩).` |
| 53 | R24 (47.7) | Tatsachennotiz zu 16.4 … (g) | 16.4 (g) (Ankerzeile 1972) | `> **(g)** **Zellen sind Quelle` | 1 | nach Zeile 2012 (am 41864d4): `` > **Die Bots lesen `m_b`; sonst ändert s `` | `> ⭐ **16.4 (g) ERGÄNZT durch R24 (47.7) und 50.6** (Fable 27c R24, TB-126, ⟨DATUM⟩).` |
| 54 | R37 (48.5) | Präzisierung zu 16.6 | 16.6 (Ankerzeile 2110) | `### 16.6 Registertext 2d` | 1 | nach Zeile 2155 (am 41864d4): `> Registertext oben bleibt zeichengleich` | `> ⭐ **16.6 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).` |
| 55 | R38 (48.6) | Ergänzung zu 16.7 (d) | 16.7 (d) (Ankerzeile 2207) | `> **(d)** **Berichtet je` | 1 | nach Zeile 2216 (am 41864d4): `> (Tatsachennotiz in 16.1.2).` | `> ⭐ **16.7 (d) ERGÄNZT durch R38 (48.6)** (Fable 29b R38, TB-126, ⟨DATUM⟩).` |
| 56 | R28 (47.11) | Tatsachennotiz zu Register 18 | Abschnitt 18 (Ankerzeile 2833) | `## 18. Tatsachennotiz zu` | 1 | nach Zeile 2891 (am 41864d4): `Festlegung.*` | `> ⭐ **Abschnitt 18 ERGÄNZT durch R28 (47.11)** (Fable 27c R28, TB-126, ⟨DATUM⟩).` |
| 57 | R53 (49.1) | Tatsachennotiz: … und 21.4 … | 21.4 (Ankerzeile 3187) | `### 21.4 Die berichtigte` | 1 | nach Zeile 3230 (am 41864d4): `Falte für unwürdig erklärt.` | `> ⭐ **21.4 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).` |
| 58 | R34 (48.2) | Ergänzung zu 22.2 | 22.2 (Ankerzeile 3484) | `### 22.2 Registertext, Kill-Test-Berichtswerte` | 1 | nach Zeile 3502 (am 41864d4): `registrieren. **Das ist kein Nachteil di` | `> ⭐ **22.2 ERGÄNZT durch R34 (48.2)** (Fable 29b R34, TB-126, ⟨DATUM⟩).` |
| 59 | R36 (48.4) | Präzisierung zu 24.2 | 24.2 (Ankerzeile 4100) | `### 24.2 Der Registertext` | 1 | nach Zeile 4116 (am 41864d4): `entscheidet nicht.` | `> ⭐ **24.2 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, ⟨DATUM⟩).` |
| 60 | R53 (49.1) | Tatsachennotiz: Die Nachmessungen in 25.2 … | 25.2 (Ankerzeile 4427) | `` ### 25.2 Die Instanz — `t3_supertrend` `` | 1 | nach Zeile 4451 (am 41864d4): `**2018-01-14**. Fables Nachrechnung trif` | `> ⭐ **25.2 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).` |
| 61 | R53 (49.1) | Präzisierung zu 4a (i) (25.3, …) | 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile) (Ankerzeile 4461) | `> **Registertext 4a / 21.3` | 1 | nach Zeile 4468 (am 41864d4): `> ⭐ **(i) „im registrierten Datenhorizon` | `> ⭐ **4a (i) in 25.3 PRÄZISIERT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).` |
| 62 | R31 (47.14) (d) | Zu 27.3: | 27.3 (im Zitatblock 27.1 bis 27.5) (Ankerzeile 4931) | `> **27.3** Das Register darf` | 1 | nach Zeile 4938 (am 41864d4): `> Der Chat des Verfahrensprüfers wurde a` | `> ⭐ **27.3 ERGÄNZT durch R31 (47.14)** (Fable 27c R31, Unterpunkt (d), TB-126, ⟨DATUM⟩).` |
| 63 | R32 (47.15) | Tatsachennotiz zu 27 | Abschnitt 27 (Ankerzeile 4910) | `## 27. Sichtschutz des Verfahrensprüfers` | 1 | nach Zeile 4974 (am 41864d4): `> 26a R6/R7, TB-114, 26.09.2026). Abschn` | `> ⭐ **Abschnitt 27 ERGÄNZT durch R32 (47.15)** (Fable 27c R32, TB-126, ⟨DATUM⟩).` |
| 64 | R53 (49.1) | Präzisierung zu 4a (i) (…, 28.6) | 28.6 (Ankerzeile 5082) | `### 28.6 Registertext 4a,` | 1 | nach Zeile 5103 (am 41864d4): `der Satz ist zwischen zwei Antworten ver` | `> ⭐ **28.6 PRÄZISIERT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).` |
| 65 | R43 (48.11) | Berichtigung zu 29.4 … lies | 29.4 (Ankerzeile 5167) | `### 29.4 Die Wache in TB-30b` | 1 | nach Zeile 5182 (am 41864d4): `> Gemessen (TB-82, Beleg M4): heute in k` | `> ⭐ **29.4 BERICHTIGT durch R43 (48.11)** (Fable 29b R43, TB-126, ⟨DATUM⟩).` |
| 66 | R43 (48.11) | Berichtigung zu …/34.5 … lies | 34.5 (Ankerzeile 6006) | `### 34.5 Berichtigung zu` | 1 | nach Zeile 6030 (am 41864d4): `` `multi_symbol_optimise.py`". `` | `> ⭐ **34.5 BERICHTIGT durch R43 (48.11)** (Fable 29b R43, TB-126, ⟨DATUM⟩).` |
| 67 | R37 (48.5) | Präzisierung zu … 35.1 | 35.1 (Ankerzeile 6115) | `### 35.1 Ergänzung zu 33.2` | 1 | nach Zeile 6185 (am 41864d4): `21.4 — 21.4 bleibt unberührt, 35.1 zitie` | `> ⭐ **35.1 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).` |
| 68 | R26 (47.9) | Ergänzung zu … 35.4 | 35.4 (Ankerzeile 6230) | `### 35.4 Präzisierung zu` | 1 | nach Zeile 6262 (am 41864d4): `> Der Text oben bleibt zeichengleich.` | `> ⭐ **35.4 ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, ⟨DATUM⟩).` |
| 69 | R49 (48.17) (e) | Zu 38.2: | 38.2 (Ankerzeile 7088) | `### 38.2 ⭐ Registertext,` | 1 | nach Zeile 7124 (am 41864d4): `**35.1** (die Tatsachennotiz 38.7 (a), a` | `> ⭐ **38.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (e), TB-126, ⟨DATUM⟩).` |
| 70 | R42 (48.10) | Ergänzung zu 40.6 | 40.6 (Ankerzeile 8048) | `### 40.6 ⭐⭐ Die neun Handelslisten` | 1 | nach Zeile 8158 (am 41864d4): `> 26.09.2026). Zitate, Text und die Mark` | `> ⭐ **40.6 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, ⟨DATUM⟩).` |
| 71 | R44 (48.12) | Ergänzung zu 40.6 | 40.6 (Ankerzeile 8048) | `### 40.6 ⭐⭐ Die neun Handelslisten` | 1 | nach Zeile 8158 (am 41864d4): `> 26.09.2026). Zitate, Text und die Mark` | `> ⭐ **40.6 ERGÄNZT durch R44 (48.12)** (Fable 29b R44, TB-126, ⟨DATUM⟩).` |
| 72 | R47 (48.15) | Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“) | 40.6 (Ankerzeile 8048) | `### 40.6 ⭐⭐ Die neun Handelslisten` | 1 | nach Zeile 8158 (am 41864d4): `> 26.09.2026). Zitate, Text und die Mark` | `> ⭐ **40.6 (Tatsachennotiz zu 5.4) PRÄZISIERT durch R47 (48.15)** (Fable 29b R47, TB-126, ⟨DATUM⟩).` |
| 73 | R41 (48.9) | Ergänzung zu 41.2 B6/B7 | 41.2, Eintrag B6/B7 (Ankerzeile 8572) | `` **B6/B7 — `haltedauern_je_bot.csv` `` | 1 | nach Zeile 8580 (am 41864d4): `Umstellung auf die neue Quelle hängt am ` | `> ⭐ **41.2 B6/B7 ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, ⟨DATUM⟩).` |
| 74 | R29 (47.12) | Ergänzung zu 42.2 E5 | 42.2, Eintrag E5 (e) (Ankerzeile 8946) | `**E5 (e) — Berichtigung zu` | 1 | nach Zeile 8963 (am 41864d4): `steht aus (42.6).` | `> ⭐ **42.2 E5 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).` |
| 75 | R29 (47.12) | Tatsachennotiz zu 44-6 | 44.1, Eintrag 44-6 (Ankerzeile 9717) | `**44-6 — Nach dem Zusammenführen` | 1 | nach Zeile 9734 (am 41864d4): `Laufbereichsmessung, und die Liste wird ` | `> ⭐ **44-6 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).` |
| 76 | R42 (48.10) | Ergänzung zu … 45.3 | 45.3 (Ankerzeile 9940) | `### 45.3 R3 — Ergänzung zu` | 1 | nach Zeile 9951 (am 41864d4): `> 26.09.2026). Zitat und Kette oben blei` | `> ⭐ **45.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, ⟨DATUM⟩).` |
| 77 | R29 (47.12) | Ergänzung zu … R4 | 45.4, Block R4 (Ankerzeile 9955) | `> **R4 — Ergänzung zu 19` | 1 | nach Zeile 9956 (am 41864d4): `> *Quelle des Grundes:* Prüfprinzip B3 (` | `> ⭐ **45.4 (R4) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).` |
| 78 | R29 (47.12) | Ergänzung zu … R5 (a) | 45.5, Block R5, Punkt (a) (Ankerzeile 9967) | `> (a) Die Laufbereichsmessung` | 1 | nach Zeile 9970 (am 41864d4): `> *Quelle des Grundes:* 24b A10 (kein Fa` | `> ⭐ **45.5 (R5) (a) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).` |
| 79 | R33 (48.1) | Berichtigung zu 45.5 (b) … lies | 45.5, Block R5, Punkt (b) (Ankerzeile 9968) | `` > (b) `zellen.csv` enthält `` | 1 | nach Zeile 9970 (am 41864d4): `> *Quelle des Grundes:* 24b A10 (kein Fa` | `> ⭐ **45.5 (b) BERICHTIGT durch R33 (48.1)** (Fable 29b R33, TB-126, ⟨DATUM⟩).` |
| 80 | R34 (48.2) | Ergänzung zu … 45.5 | 45.5 (Ankerzeile 9964) | `### 45.5 R5 — Abnahmebedingungen` | 1 | nach Zeile 9976 (am 41864d4): `Zeile (5).` | `> ⭐ **45.5 ERGÄNZT durch R34 (48.2)** (Fable 29b R34, TB-126, ⟨DATUM⟩).` |
| 81 | R36 (48.4) | Präzisierung zu … 45.5 | 45.5 (Ankerzeile 9964) | `### 45.5 R5 — Abnahmebedingungen` | 1 | nach Zeile 9976 (am 41864d4): `Zeile (5).` | `> ⭐ **45.5 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, ⟨DATUM⟩).` |
| 82 | R39 (48.7) | Ergänzung zu 46.3 (R12) | 46.3 (Ankerzeile 10154) | `### 46.3 R12 — Tatsachennotiz` | 1 | nach Zeile 10164 (am 41864d4): `die neun heutigen Listen.` | `> ⭐ **46.3 ERGÄNZT durch R39 (48.7)** (Fable 29b R39, TB-126, ⟨DATUM⟩).` |
| 83 | R42 (48.10) | Ergänzung zu … 46.3 | 46.3 (Ankerzeile 10154) | `### 46.3 R12 — Tatsachennotiz` | 1 | nach Zeile 10164 (am 41864d4): `die neun heutigen Listen.` | `> ⭐ **46.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, ⟨DATUM⟩).` |
| 84 | R25 (47.8) | als Ergänzung zu … R14 | 46.5, Block R14 (Ankerzeile 10188) | `> **R14 — Ergänzung zu 12` | 1 | nach Zeile 10189 (am 41864d4): `` > *Quelle des Grundes:* Docstring von `a `` | `> ⭐ **46.5 (R14) ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, ⟨DATUM⟩).` |
| 85 | R26 (47.9) | Ergänzung zu … R14 | 46.5, Block R14 (Ankerzeile 10188) | `> **R14 — Ergänzung zu 12` | 1 | nach Zeile 10189 (am 41864d4): `` > *Quelle des Grundes:* Docstring von `a `` | `> ⭐ **46.5 (R14) ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, ⟨DATUM⟩).` |
| 86 | R27 (47.10) | Tatsachennotiz zu R14 Bedingung 5 | 46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile) (Ankerzeile 10188) | `> **R14 — Ergänzung zu 12` | 1 | nach Zeile 10189 (am 41864d4): `` > *Quelle des Grundes:* Docstring von `a `` | `> ⭐ **46.5 (R14), Bedingung 5 ERGÄNZT durch R27 (47.10)** (Fable 27c R27, TB-126, ⟨DATUM⟩).` |
| 87 | R25 (47.8) | Bestätigung von 46.9 | 46.9 (Ankerzeile 10239) | `### 46.9 Lesart des steuernden` | 1 | nach Zeile 10251 (am 41864d4): `` `auswertung.py`. `` | `> ⭐ **46.9 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, ⟨DATUM⟩).` |
| 88 | R54 (49.2) | Berichtigung zu … R48 (g) … In R48 (g) lies | 48.16 (R48), neu in TB-126 | `> R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle.` | am 41864d4: 0; nach Anhängen von 48: 1 (Simulation) | am Ende von 48.16, nach dem Zitatblock R48, vor der Zeile `**Kette:**` | `> ⭐ **48.16 R48 (g) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, ⟨DATUM⟩).` |

## A — Indexzeilen statt Marken (6)

| # | R | Ort im Register | Grund | neuer Ort |
|---|---|---|---|---|
| 1 | R42 | 10, künftiger Punkt 15 (die neun neuen Trade-Listen) | Abschnitt 10 | 48.10 |
| 2 | R45 | 10, Sperrlistenpunkt 10 (Zuteilungskaskade, `shared/zuteilung.py`), Z. 1010 | Abschnitt 10 | 48.13 |
| 3 | R48 (k) | 10.1, „Stichproben-Hash-Vergleich“ (lies „Hash-Vergleich aller Ausgabedateien …“) | Abschnitt 10 | 48.16 |
| 4 | R49 (g), R51 | 10, „Fortschreibung derselben Tatsache (15.09.2026, nach dem Lauf)“, Z. 1035 | Abschnitt 10 | 48.17 (R51: 48.19) |
| 5 | R51 | Datenstand-Hash voll: 17.3, 17.9, 18 | R51 verlangt Indexzeile | 48.19 |
| 6 | **R30** | 10, **Sperrlistenpunkt 14** („Die Reihenfolge Selektion → Bestätigungsperiode → Bericht“), Z. 1017 | Abschnitt 10. ⚠️ **Nicht im Auftragsentwurf C3.** „Ergänzung zu 14“ in R30 ist Sperrlistenpunkt 14, nicht Abschnitt 14 (der ist der Nulltest S-E1); R30 nennt als Quelle „14 (Reihenfolge)“, R34 schreibt „Punkt 14 (Reihenfolge Selektion → Bestätigung → Bericht)“ | 47.13 |

## B — Ziel nach Regel 1, aber nicht gesetzt (4)

| R | Ziel laut Fable | Grund |
|---|---|---|
| R27 (47.10) | „Ergänzung zu den Tag-Vorbedingungen“ | Das Register hat keinen Ort „Tag-Vorbedingungen“; das Wort steht verstreut (u. a. 41.1 A11, 42.1 D4, 46.6 R15, 39.1). Vorbild: R15 (46.6) hat dafür auch keine Marke bekommen. |
| R28 (47.11) | „Tatsachennotiz zu … Plan-Punkt 6“ | Der Plan steht nicht im Register; „Plan-Punkt 6“ ist dort kein Ort (nur Fundstelle in 46.4 R13). |
| R30 (47.13) | „Ergänzung zu … den Tag-Vorbedingungen“ | wie R27. |
| R48 (48.16) (d), (e) | Lesarten „Exposure: …“ und „Benchmark: …“ | Der Unterpunkt nennt keinen Bezugsort, nur Fundstellen in Klammern (4.2, 7 (c), 7.1, 16.4 (b), 15.6 (c), 23.3, 23.5, 23.7); R51 nennt für (d)/(e) keine Marke (29b Block III: M50/M51/M54/A69 → R48 (d)/(e), nur A70 → R51 = 4.2, Nr. 11 der Tabelle). |

## C — im Block genannte Orte ohne Bezugsform (keine Marke nach Regel 1; zur Entscheidung)

- R21: „Die Prüfung vor dem Tag in 16.4 zählt jede mögliche Eingabe auf — 4⁹ …, nicht nur die 3⁹“ — ändert inhaltlich 16.4 „#### Prüfung vor dem Tag“ (Z. 2040–2046, 3⁹ = 19 683). Die R21-Marken stehen hinter den Zitatblöcken (Z. 1968/2012), nicht dort. Kandidat für eine zusätzliche Marke am Ende von 16.4 (nach Z. 2052).
- R36: „Festlegung 3 und Abschnitt 8 … beziehen sich auf kapital_drawdown_mtm_pct“; R37: „„Alle Falten“ in Abbruchkriterium (b) sind die Selektionsfalten“ (7 (b)); R54: „je Falte, über die Selektionsfalten (7 (c)), im Zufalls-Timing (8.1) … verkettet“; R55: „Ist keine Zelle zulässig, greift (b)“. Inhaltlich Lesarten zu 0–12, aber ohne Bezugsform.
- R33: „„leere Trade-Liste“ in 45.5 (b) und 43-7 bezeichnet …“ (43-7); R52 (b): 45.5 (b) (dort steht schon die Marke aus R33).
- R38: „16.11 Zeile 7 wird damit geschlossen“.
- R41: „Die Donchian-Untergrenze (41.2 B3, median_balken) nutzt dieselbe Einheit“.
- R47: „Tatsachennotiz zu 5.4“ — als Teil von 40.6 gelesen (40.6 trägt den Absatz „Tatsachennotiz zu 5.4 — Fables Unsicherheit“, Z. 8094–8109, mit „Parameterdateien“); 5.4 selbst ohne Marke. Die Marke steht am Ende von 40.6 mit dem Ort „40.6 (Tatsachennotiz zu 5.4)“.
- R48 (h): „„Hypothese“ im Kopf von 3 ist erzeugter Text und bleibt“ — liegt im ERZEUGT-Block, dort nie eine Marke.
- R49 (c): „die in 40.8 (b) verlangte Tatsachennotiz an 4.4“ (40.8 (b)); R49 (e): „Die Marke in 6 nennt registerdaten.py:605“ (Abschnitt 6).
- R31 (a): R8 (a) und R14 („„Streichung“ … war Handwerk am Wortlaut“); R31 (e): „ihr Registertext steht zeichengleich in 45“.
- R39 „Berichtigung des Datenvertrags … lies „<bot>.csv““, R43 „die neun Optimierer erhalten eine Tatsachennotiz“, „Posten 5 des Plans“, R25 „Der Docstring …“: Code bzw. Plan, kein Registerort (R39 steht in 50.2).

## Prüfsumme

- Überschriften: **38** (47.1–47.15, 48.1–48.20, 49.1–49.3), alle eindeutig, längste 120 Zeichen.
- Marken: **87 am alten Ort** an **54 Einfügestellen**, dazu **1 unter 48.16** (R54) = **88**. PRÄZISIERT 32, ERGÄNZT 51 (davon „(Verweis)“ 5), BERICHTIGT 4 (+1 unter 48.16).
- Je Abschnitt (Abschnitt der Einfügestelle): Kopf: 1, 1: 3, 2: 5, 3: 1, 4: 2, 5: 2, 7: 5, 8: 1, 9: 1, 11: 3, 12: 4, 15: 7, 16: 20, 18: 1, 21: 1, 22: 1, 24: 1, 25: 2, 27: 2, 28: 1, 29: 1, 34: 1, 35: 2, 38: 1, 40: 3, 41: 1, 42: 1, 44: 1, 45: 6, 46: 6, 48: 1.
- Abschnitt 9: genau **1** Marke (R48 (b)). Abschnitt 10: **0**. ERZEUGT-Block: **0** (die Marke zu 3 steht nach Z. 430). Abschnitt 3: **1**.
- Anker: **87/87 mit Zahl 1** am `41864d4` (`str.count` über den ganzen Text), und nach simuliertem Einsetzen (alle Marken + angehängte Blöcke 47–49 als Zitat) ebenfalls 87/87; der R54-Anker unter 48.16 zählt nach der Simulation 1.
- Indexzeilen: **6** (Liste A). Nicht gesetzt: **4** (Liste B). Ohne Bezugsform, zur Entscheidung: Liste C.

Prüfskript (liest den JSON-Block unten; Aufruf `python3 pruefe_markentabelle_tb126.py markentabelle_tb126.md <repo>`; rc 0 = alles wie angegeben):

```python
#!/usr/bin/env python3
"""Prueft die Markentabelle TB-126 gegen das Register am Stand 41864d4.

Aufruf:  python3 pruefe_markentabelle_tb126.py <markentabelle_tb126.md> <repo-wurzel>
Liest den JSON-Block der Markentabelle (zwischen den Zeilen 'DATEN-ANFANG' und 'DATEN-ENDE'),
zaehlt jeden Anker mit str.count ueber den ganzen Registertext, prueft Ankerzeile und
Einfuegestelle, simuliert das Einsetzen (Marken + angehaengte Bloecke 47-49) und zaehlt erneut.
rc 0 = alles wie angegeben, rc 1 = Abweichung.
"""
import hashlib, json, re, sys

md, repo = sys.argv[1], sys.argv[2].rstrip("/") + "/"
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
reg = open(repo + "docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read()
L = reg.split("\n")
fehler = []
def f(x): fehler.append(x)

if hashlib.md5(reg.encode()).hexdigest() != "c8a32c0f0037c6c65bd08aae6be5a7c1": f("Register-md5 weicht ab")
if len(reg.splitlines()) != 10347: f("Register-Zeilenzahl weicht ab")
a10 = next(i for i, s in enumerate(L, 1) if s.startswith("## 10."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))

marken = daten["marken"]
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker {m['anker']!r} zaehlt {n}")
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f(f"Nr {m['nr']}: Anker beginnt nicht Zeile {m['ankerzeile']}")
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f(f"Nr {m['nr']}: Zeile {m['nach']} beginnt nicht wie angegeben")
    if a10 <= m["nach"] < a11: f(f"Nr {m['nr']}: Einfuegestelle in Abschnitt 10")
    if ea <= m["nach"] < ee: f(f"Nr {m['nr']}: Einfuegestelle im ERZEUGT-Block")
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f(f"Nr {m['nr']}: mitten im Zitat")
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f(f"Nr {m['nr']}: mitten in Tabelle")
    if not re.match(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT)( \(Verweis\))? durch .+\*\* \(.+, TB-126, ⟨DATUM⟩\)\.$", m["m1"]):
        f(f"Nr {m['nr']}: Markenzeile 1 nicht in der Form")
    if m["m2"] != "> Eintrag und Stand oben bleiben zeichengleich.": f(f"Nr {m['nr']}: Markenzeile 2")
# Reihenfolge: nach Einfuegestelle, dann R aufsteigend (B3 ohne R zuletzt)
schl = [(m["nach"], m["R"] or 999) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")

# Simulation: Marken von unten nach oben einsetzen, Bloecke 47-49 anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"] or 999, m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
QUELLEN = {"27c": ("FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md", 161, 209),
           "29b": ("FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md", 190, 267),
           "30a": ("FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md", 25, 32)}
bl = {}
for q, (dat, a, b) in QUELLEN.items():
    z = open(repo + "docs/projektfuehrung/" + dat, encoding="utf-8").read().split("\n")
    cur = None
    for i in range(a, b + 1):
        s = z[i - 1]
        mm = re.match(r"^(\*\*)?R(\d+) — ", s)
        if mm: cur = int(mm.group(2)); bl[cur] = [s]; continue
        if cur is not None:
            bl[cur].append(s)
            if s.startswith("Quelle des Grundes:") or s.startswith("*Quelle des Grundes:*"): cur = None
if sorted(bl) != list(range(18, 56)): f("Schnitt ergibt nicht R18-R55")
anhang = []
for u in daten["ueberschriften"]:
    anhang += ["", u["zeile"], ""] + ["> " + z for z in bl[u["R"]]] + ["", "**Kette:** …"]
    if u["R"] == 48:
        r54 = daten["r54_unter_48_16"]
        anhang[-1:-1] = ["", r54["m1"], r54["m2"], ""]
sim = "\n".join(neu + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker nach Simulation {n}")
n54 = sim.count(daten["r54_unter_48_16"]["anker"])
if n54 != 1: f(f"R54-Anker (48.16) nach Simulation {n54}")
zz = [u["zeile"] for u in daten["ueberschriften"]]
if len(set(zz)) != 38 or any(sim.count(z) != 1 for z in zz): f("Ueberschriften nicht eindeutig")
if any(len(z) > 120 for z in zz): f("Ueberschrift laenger als 120 Zeichen")
# Altzeilen unveraendert und in Reihenfolge (append-only)
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")

je = {}
for m in marken:
    k = next((int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1])), -1)
    je[k] = je.get(k, 0) + 1
print("Marken am alten Ort:", len(marken), "+ 1 unter 48.16 =", len(marken) + 1)
print("je Abschnitt:", ", ".join(f"{'Kopf' if k < 0 else k}: {v}" for k, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Ueberschriften:", len(zz), "max. Laenge", max(len(z) for z in zz))
if fehler:
    print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
print("rc 0: alles wie angegeben")
```

Ausgabe am `41864d4`:

```
Marken am alten Ort: 87 + 1 unter 48.16 = 88
je Abschnitt: Kopf: 1, 1: 3, 2: 5, 3: 1, 4: 2, 5: 2, 7: 5, 8: 1, 9: 1, 11: 3, 12: 4, 15: 7, 16: 20, 18: 1, 21: 1, 22: 1, 24: 1, 25: 2, 27: 2, 28: 1, 29: 1, 34: 1, 35: 2, 38: 1, 40: 3, 41: 1, 42: 1, 44: 1, 45: 6, 46: 6
Anker mit Zahl 1 (Original): 87 von 87
Anker mit Zahl 1 (nach Simulation): 87 von 87
Ueberschriften: 38 max. Laenge 120
rc 0: alles wie angegeben
```

## Daten (maschinenlesbar, massgeblich für Skripte)

```
DATEN-ANFANG
{
 "stand": "41864d4",
 "register_md5": "c8a32c0f0037c6c65bd08aae6be5a7c1",
 "ueberschriften": [
  {
   "xn": "47.1",
   "R": 18,
   "quelle": "27c",
   "zeile": "### 47.1 R18 — Präzisierung zu 16.4 (m), (h) und (l) (Zellenanteil und Klassenschlüssel; L1)"
  },
  {
   "xn": "47.2",
   "R": 19,
   "quelle": "27c",
   "zeile": "### 47.2 R19 — Präzisierung zu 16.4 (h), (j) und (k) (Zahl der Zellen; L2; T116-4)"
  },
  {
   "xn": "47.3",
   "R": 20,
   "quelle": "27c",
   "zeile": "### 47.3 R20 — Ergänzung zu 16.4 (l) und (j) (Anlage ohne aktive Zelle; L3)"
  },
  {
   "xn": "47.4",
   "R": 21,
   "quelle": "27c",
   "zeile": "### 47.4 R21 — Präzisierung zu 16.4 (b), (i) und (j) und Ergänzung zu 7.1 (Schatten nach der Herkunft der Stufe; L4…"
  },
  {
   "xn": "47.5",
   "R": 22,
   "quelle": "27c",
   "zeile": "### 47.5 R22 — Präzisierung zu 16.4 (a) und (i) (Faktor „Bestätigt\" vor Netting; L5)"
  },
  {
   "xn": "47.6",
   "R": 23,
   "quelle": "27c",
   "zeile": "### 47.6 R23 — Präzisierung zu 16.4 (b), 7.1 und 15.6 (c) (Budgetanteil und Höhe der Benchmark-Position; L0.1; T116-3)"
  },
  {
   "xn": "47.7",
   "R": 24,
   "quelle": "27c",
   "zeile": "### 47.7 R24 — Tatsachennotiz zu 16.4 (h) und (g) (Folge der Gleichteilung bei ungleicher Besetzung; T116-5)"
  },
  {
   "xn": "47.8",
   "R": 25,
   "quelle": "27c",
   "zeile": "### 47.8 R25 — Bestätigung von 46.9 als Ergänzung zu 12 und R14 (Herkunftsprüfung ohne Modus; T117-1)"
  },
  {
   "xn": "47.9",
   "R": 26,
   "quelle": "27c",
   "zeile": "### 47.9 R26 — Ergänzung zu 12, R14 und 35.4 (alle neun unter dem Modus; --bot; T117-2)"
  },
  {
   "xn": "47.10",
   "R": 27,
   "quelle": "27c",
   "zeile": "### 47.10 R27 — Tatsachennotiz zu R14 Bedingung 5 und Ergänzung zu den Tag-Vorbedingungen (voller Commit-Hash; T117-3)"
  },
  {
   "xn": "47.11",
   "R": 28,
   "quelle": "27c",
   "zeile": "### 47.11 R28 — Tatsachennotiz zu Register 18 und Plan-Punkt 6 (drei Orte des Datenstands; T117-4)"
  },
  {
   "xn": "47.12",
   "R": 29,
   "quelle": "27c",
   "zeile": "### 47.12 R29 — Ergänzung zu 42.2 E5, R4 und R5 (a); Tatsachennotiz zu 44-6 (herkunft.py im Laufbereich; T117-5)"
  },
  {
   "xn": "47.13",
   "R": 30,
   "quelle": "27c",
   "zeile": "### 47.13 R30 — Ergänzung zu 14 und zu den Tag-Vorbedingungen (Erzeuger und Auswertung am Tag-Commit; T117-6)"
  },
  {
   "xn": "47.14",
   "R": 31,
   "quelle": "27c",
   "zeile": "### 47.14 R31 — Tatsachennotizen 27c"
  },
  {
   "xn": "47.15",
   "R": 32,
   "quelle": "27c",
   "zeile": "### 47.15 R32 — Tatsachennotiz zu 27 — Anfangsbestand des Verfahrensprüfers beim dritten Umzug (29.09.2026)"
  },
  {
   "xn": "48.1",
   "R": 33,
   "quelle": "29b",
   "zeile": "### 48.1 R33 — Berichtigung zu 45.5 (b) (Zeilen in zellen.csv)"
  },
  {
   "xn": "48.2",
   "R": 34,
   "quelle": "29b",
   "zeile": "### 48.2 R34 — Ergänzung zu 22.2 und 45.5 (Zellenbericht)"
  },
  {
   "xn": "48.3",
   "R": 35,
   "quelle": "29b",
   "zeile": "### 48.3 R35 — Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz"
  },
  {
   "xn": "48.4",
   "R": 36,
   "quelle": "29b",
   "zeile": "### 48.4 R36 — Präzisierung zu 24.2 und 45.5 (zwei Drawdown-Spalten; Konsistenzprüfung; Ausschnitt)"
  },
  {
   "xn": "48.5",
   "R": 37,
   "quelle": "29b",
   "zeile": "### 48.5 R37 — Präzisierung zu 16.6, 35.1, 16.4 (c)/(d), 5.1 Nr. 7 (zwei Zeiträume, ein Name)"
  },
  {
   "xn": "48.6",
   "R": 38,
   "quelle": "29b",
   "zeile": "### 48.6 R38 — Ergänzung zu 16.7 (d) (Ort der Berichtsgrössen)"
  },
  {
   "xn": "48.7",
   "R": 39,
   "quelle": "29b",
   "zeile": "### 48.7 R39 — Ergänzung zu 46.3 (R12) und Berichtigung des Datenvertrags (Ausgaben des Zellen-Erzeugers; Feldliste als…"
  },
  {
   "xn": "48.8",
   "R": 40,
   "quelle": "29b",
   "zeile": "### 48.8 R40 — Ersteintrag — Schreibregel für Ausgaben der Erzeuger"
  },
  {
   "xn": "48.9",
   "R": 41,
   "quelle": "29b",
   "zeile": "### 48.9 R41 — Ergänzung zu 41.2 B6/B7 und 15.3 (b) (haltedauer_balken)"
  },
  {
   "xn": "48.10",
   "R": 42,
   "quelle": "29b",
   "zeile": "### 48.10 R42 — Ergänzung zu 40.6, 45.3, 46.3 (Bindung der neuen Listen)"
  },
  {
   "xn": "48.11",
   "R": 43,
   "quelle": "29b",
   "zeile": "### 48.11 R43 — Registertext zum Zellen-Kern; Berichtigung zu 29.4/34.5 (Ort der Wache); Tatsachennotiz zu 11.2"
  },
  {
   "xn": "48.12",
   "R": 44,
   "quelle": "29b",
   "zeile": "### 48.12 R44 — Ergänzung zu 40.6 (Reihenfolge der Neuerzeugung)"
  },
  {
   "xn": "48.13",
   "R": 45,
   "quelle": "29b",
   "zeile": "### 48.13 R45 — Registertext zu Sperrlistenpunkt 10 (ausgeführte Positionen)"
  },
  {
   "xn": "48.14",
   "R": 46,
   "quelle": "29b",
   "zeile": "### 48.14 R46 — Ersteintrag — Abnahme des Zellen-Erzeugers vor dem Tag"
  },
  {
   "xn": "48.15",
   "R": 47,
   "quelle": "29b",
   "zeile": "### 48.15 R47 — Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“)"
  },
  {
   "xn": "48.16",
   "R": 48,
   "quelle": "29b",
   "zeile": "### 48.16 R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle"
  },
  {
   "xn": "48.17",
   "R": 49,
   "quelle": "29b",
   "zeile": "### 48.17 R49 — Tatsachennotizen zu Register 0–12 (TB-121), Marke je am alten Ort"
  },
  {
   "xn": "48.18",
   "R": 50,
   "quelle": "29b",
   "zeile": "### 48.18 R50 — Ergänzung zu 12 (Kennzahlendefinitionen im Code) und Tatsachennotiz zu TB-121"
  },
  {
   "xn": "48.19",
   "R": 51,
   "quelle": "29b",
   "zeile": "### 48.19 R51 — Marken am alten Ort für Register 0–12 (Handwerk im Registerauftrag; der alte Satz bleibt zeichengleich)"
  },
  {
   "xn": "48.20",
   "R": 52,
   "quelle": "29b",
   "zeile": "### 48.20 R52 — Tatsachennotizen 29b"
  },
  {
   "xn": "49.1",
   "R": 53,
   "quelle": "30a",
   "zeile": "### 49.1 R53 — Präzisierung zu 4a (i) (25.3, 28.6): Indikator-Vorlauf bei achsenabhängigem Rückblick"
  },
  {
   "xn": "49.2",
   "R": 54,
   "quelle": "30a",
   "zeile": "### 49.2 R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen)"
  },
  {
   "xn": "49.3",
   "R": 55,
   "quelle": "30a",
   "zeile": "### 49.3 R55 — Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz"
  }
 ],
 "marken": [
  {
   "nr": 1,
   "R": 49,
   "unterpunkt": "(f)",
   "ziel": "Zum Kopf des Registers: „Stand: 14.09.2026“ (R51: Kopf →)",
   "stelle": "Kopf, Absatz „Stand: 14.09.2026“",
   "ankerzeile": 3,
   "anker": "**Stand: 14.09.2026. Dies",
   "zahl": 1,
   "nach": 4,
   "anfang40": "und danach nicht mehr verhandelt.**",
   "m1": "> ⭐ **Kopf (Stand 14.09.2026) ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (f), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 2,
   "R": 48,
   "unterpunkt": "(a)",
   "ziel": "Festlegung 4 … Marke an Festlegung 4 (R51); R51: Festlegung 4 →",
   "stelle": "1, Tabelle, Zeile 4",
   "ankerzeile": 59,
   "anker": "| 4 | Drawdown-Bedingung",
   "zahl": 1,
   "nach": 69,
   "anfang40": "> ⭐ **Festlegung 1 PRÄZISIERT durch Absc",
   "m1": "> ⭐ **Festlegung 4 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (a), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 3,
   "R": 48,
   "unterpunkt": "(j)",
   "ziel": "Festlegung 3 bei weniger als drei Selektionsfalten:",
   "stelle": "1, Tabelle, Zeile 3",
   "ankerzeile": 58,
   "anker": "| 3 | Beurteilung | Netto-Calmar,",
   "zahl": 1,
   "nach": 69,
   "anfang40": "> ⭐ **Festlegung 1 PRÄZISIERT durch Absc",
   "m1": "> ⭐ **Festlegung 3 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (j), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 4,
   "R": 51,
   "unterpunkt": "",
   "ziel": "Festlegung 2 und 7 (a) → 15.3 (c) und Formelzeile [A63]",
   "stelle": "1, Tabelle, Zeile 2",
   "ankerzeile": 57,
   "anker": "| 2 | Selektionsstatistik",
   "zahl": 1,
   "nach": 69,
   "anfang40": "> ⭐ **Festlegung 1 PRÄZISIERT durch Absc",
   "m1": "> ⭐ **Festlegung 2 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 5,
   "R": 48,
   "unterpunkt": "(i)",
   "ziel": "Die Ziffernregel aus 2.1",
   "stelle": "2.1",
   "ankerzeile": 86,
   "anker": "### 2.1 Wie sie entstehen",
   "zahl": 1,
   "nach": 113,
   "anfang40": "nicht später versehentlich verschärft wi",
   "m1": "> ⭐ **2.1 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (i), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 6,
   "R": 48,
   "unterpunkt": "(h)",
   "ziel": "haltedauer (2.2)",
   "stelle": "2.2",
   "ankerzeile": 115,
   "anker": "### 2.2 Die vier zulässigen",
   "zahl": 1,
   "nach": 127,
   "anfang40": "Beide Sätze nennen **keine Zahl**; die W",
   "m1": "> ⭐ **2.2 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (h), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 7,
   "R": 49,
   "unterpunkt": "(a)",
   "ziel": "Zu 2.2:",
   "stelle": "2.2",
   "ankerzeile": 115,
   "anker": "### 2.2 Die vier zulässigen",
   "zahl": 1,
   "nach": 127,
   "anfang40": "Beide Sätze nennen **keine Zahl**; die W",
   "m1": "> ⭐ **2.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (a), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 8,
   "R": 48,
   "unterpunkt": "(f)",
   "ziel": "Kante (2.5):",
   "stelle": "2.5",
   "ankerzeile": 165,
   "anker": "### 2.5 Die Kantenregel",
   "zahl": 1,
   "nach": 180,
   "anfang40": "unverändert bleibt.",
   "m1": "> ⭐ **2.5 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (f), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 9,
   "R": 49,
   "unterpunkt": "(b)",
   "ziel": "Zu 2.7:",
   "stelle": "2.7",
   "ankerzeile": 207,
   "anker": "### 2.7 Stufung",
   "zahl": 1,
   "nach": 218,
   "anfang40": "Bots gelten.",
   "m1": "> ⭐ **2.7 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (b), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 10,
   "R": 49,
   "unterpunkt": "(c)",
   "ziel": "Zu 3 und 4.4: (R51: 3, Zahlenteil und 4.4 →)",
   "stelle": "3, Zahlenteil (nach ENDE ERZEUGT)",
   "ankerzeile": 430,
   "anker": "<!-- ENDE ERZEUGT -->",
   "zahl": 1,
   "nach": 430,
   "anfang40": "<!-- ENDE ERZEUGT -->",
   "m1": "> ⭐ **Abschnitt 3 (Zahlenteil) ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (c), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 11,
   "R": 51,
   "unterpunkt": "",
   "ziel": "4.2 → 43-2 (Interpolation an den Rändern) [A70]",
   "stelle": "4.2",
   "ankerzeile": 451,
   "anker": "### 4.2 Warum `DD_Benchmark`",
   "zahl": 1,
   "nach": 484,
   "anfang40": "Exposure-Argument, nicht über die Tabell",
   "m1": "> ⭐ **4.2 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 12,
   "R": 49,
   "unterpunkt": "(c)",
   "ziel": "Zu 3 und 4.4:",
   "stelle": "4.4",
   "ankerzeile": 509,
   "anker": "### 4.4 Ist die Bedingung",
   "zahl": 1,
   "nach": 536,
   "anfang40": "darüber.",
   "m1": "> ⭐ **4.4 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (c), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 13,
   "R": 37,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 5.1 Nr. 7",
   "stelle": "5.1, Nr. 7",
   "ankerzeile": 593,
   "anker": "7. **Die letzte Falte wird",
   "zahl": 1,
   "nach": 596,
   "anfang40": "   Selektion. **Und sie wächst jeden Mon",
   "m1": "> ⭐ **5.1 Nr. 7 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 14,
   "R": 51,
   "unterpunkt": "",
   "ziel": "5.3 und 15.6 → 33.2 (gültiger Faltenplan, alle neun Bots) [A66]",
   "stelle": "5.3",
   "ankerzeile": 621,
   "anker": "### 5.3 Krypto: Platzhalter",
   "zahl": 1,
   "nach": 646,
   "anfang40": "auszuwerten — es gibt dann keine Zahl, d",
   "m1": "> ⭐ **5.3 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 15,
   "R": 48,
   "unterpunkt": "(c)",
   "ziel": "Abschnitt 7 (d):",
   "stelle": "7, Tabelle, Zeile (d)",
   "ankerzeile": 753,
   "anker": "| **(d)** | Der Gewinner",
   "zahl": 1,
   "nach": 753,
   "anfang40": "| **(d)** | Der Gewinner ist eine **Spit",
   "m1": "> ⭐ **7 (d) PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (c), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 16,
   "R": 51,
   "unterpunkt": "",
   "ziel": "Festlegung 2 und 7 (a) → 15.3 (c) und Formelzeile [A63]",
   "stelle": "7, Tabelle, Zeile (a)",
   "ankerzeile": 750,
   "anker": "| **(a)** | Falten-Median",
   "zahl": 1,
   "nach": 753,
   "anfang40": "| **(d)** | Der Gewinner ist eine **Spit",
   "m1": "> ⭐ **7 (a) ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 17,
   "R": 55,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz",
   "stelle": "7, Tabelle, Zeile (d)",
   "ankerzeile": 753,
   "anker": "| **(d)** | Der Gewinner",
   "zahl": 1,
   "nach": 753,
   "anfang40": "| **(d)** | Der Gewinner ist eine **Spit",
   "m1": "> ⭐ **7 (d) ERGÄNZT durch R55 (49.3)** (Fable 30a R55, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 18,
   "R": 21,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 7.1",
   "stelle": "7.1",
   "ankerzeile": 777,
   "anker": "### 7.1 Die drei Regeln für",
   "zahl": 1,
   "nach": 793,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **7.1 ERGÄNZT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 19,
   "R": 23,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 7.1",
   "stelle": "7.1",
   "ankerzeile": 777,
   "anker": "### 7.1 Die drei Regeln für",
   "zahl": 1,
   "nach": 793,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **7.1 PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 20,
   "R": 48,
   "unterpunkt": "(g)",
   "ziel": "Zufalls-Timing (8.1):",
   "stelle": "8.1",
   "ankerzeile": 821,
   "anker": "### 8.1 Der Zufalls-Timing-Test",
   "zahl": 1,
   "nach": 839,
   "anfang40": "Bots tut sie das.",
   "m1": "> ⭐ **8.1 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (g), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 21,
   "R": 48,
   "unterpunkt": "(b)",
   "ziel": "Abschnitt 9: … „N = 653 plus …“ ist die Kurzform; R51: 9 → R48 (b)",
   "stelle": "9, erster Absatz",
   "ankerzeile": 845,
   "anker": "**N = 653 plus die Zellen",
   "zahl": 1,
   "nach": 848,
   "anfang40": "`registerdaten.N_HISTORISCH_JE_BOT` und ",
   "m1": "> ⭐ **Abschnitt 9 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (b), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 22,
   "R": 43,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu 11.2",
   "stelle": "11.2",
   "ankerzeile": 1119,
   "anker": "### 11.2 Agent 2 — Auswahl",
   "zahl": 1,
   "nach": 1141,
   "anfang40": "Prüfungen aus TB-22 bestehen unverändert",
   "m1": "> ⭐ **11.2 ERGÄNZT durch R43 (48.11)** (Fable 29b R43, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 23,
   "R": 49,
   "unterpunkt": "(h)",
   "ziel": "Zu 11: (R51: 11 →)",
   "stelle": "Abschnitt 11",
   "ankerzeile": 1087,
   "anker": "## 11. Voraussetzungen des",
   "zahl": 1,
   "nach": 1157,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **Abschnitt 11 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (h), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 24,
   "R": 0,
   "unterpunkt": "B3",
   "ziel": "Vollzug Posten 3 (11.3): Tatsachennotizen 50.3 und 50.4",
   "stelle": "11.3",
   "ankerzeile": 1143,
   "anker": "### 11.3 Zwei Achsen brauchen",
   "zahl": 1,
   "nach": 1157,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **11.3 ERGÄNZT durch 50.3 und 50.4** (Tatsachennotiz, Vollzug TB-122 und TB-124 nach 37.3, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 25,
   "R": 25,
   "unterpunkt": "",
   "ziel": "als Ergänzung zu 12",
   "stelle": "Abschnitt 12",
   "ankerzeile": 1161,
   "anker": "## 12. Der Vollständigkeitstest",
   "zahl": 1,
   "nach": 1222,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **Abschnitt 12 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 26,
   "R": 26,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 12",
   "stelle": "Abschnitt 12",
   "ankerzeile": 1161,
   "anker": "## 12. Der Vollständigkeitstest",
   "zahl": 1,
   "nach": 1222,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **Abschnitt 12 ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 27,
   "R": 49,
   "unterpunkt": "(d)",
   "ziel": "Zu 12:",
   "stelle": "Abschnitt 12",
   "ankerzeile": 1161,
   "anker": "## 12. Der Vollständigkeitstest",
   "zahl": 1,
   "nach": 1222,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **Abschnitt 12 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (d), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 28,
   "R": 50,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 12 (R51: 12 → R50)",
   "stelle": "Abschnitt 12",
   "ankerzeile": 1161,
   "anker": "## 12. Der Vollständigkeitstest",
   "zahl": 1,
   "nach": 1222,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **Abschnitt 12 ERGÄNZT durch R50 (48.18)** (Fable 29b R50, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 29,
   "R": 41,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … 15.3 (b)",
   "stelle": "15.3 (b)",
   "ankerzeile": 1328,
   "anker": "> **(b)** Verfahren: stationärer",
   "zahl": 1,
   "nach": 1338,
   "anfang40": "> Trades je Falte wird für den Gewinner ",
   "m1": "> ⭐ **15.3 (b) ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 30,
   "R": 35,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 15.3 (Bootstrap) und Tatsachennotiz",
   "stelle": "15.3",
   "ankerzeile": 1322,
   "anker": "### 15.3 Registertext 1 —",
   "zahl": 1,
   "nach": 1356,
   "anfang40": "> zeichengleich.",
   "m1": "> ⭐ **15.3 ERGÄNZT durch R35 (48.3)** (Fable 29b R35, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 31,
   "R": 54,
   "unterpunkt": "",
   "ziel": "Berichtigung zu Registertext 2a (15.4) … lies",
   "stelle": "15.4 (a)",
   "ankerzeile": 1362,
   "anker": "> **(a)** Selektionsfalten",
   "zahl": 1,
   "nach": 1381,
   "anfang40": "> als **obere Schranke** weiter.",
   "m1": "> ⭐ **2a (15.4 (a)) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 32,
   "R": 41,
   "unterpunkt": "B3",
   "ziel": "„15.4 erhält eine Tatsachennotiz“ (Abweichungsfall, 30a Teil 0; Befund 50.1)",
   "stelle": "15.4",
   "ankerzeile": 1360,
   "anker": "### 15.4 Registertext 2 —",
   "zahl": 1,
   "nach": 1423,
   "anfang40": "> (42.6 (5)). Die Tabelle bleibt zeichen",
   "m1": "> ⭐ **15.4 ERGÄNZT durch R41 (48.9) und 50.1** (Fable 29b R41, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 33,
   "R": 53,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz: … 15.5 …",
   "stelle": "15.5",
   "ankerzeile": 1427,
   "anker": "### 15.5 Registertext 3 —",
   "zahl": 1,
   "nach": 1535,
   "anfang40": "hätte jeder Bot seine eigene, wie die Ta",
   "m1": "> ⭐ **15.5 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 34,
   "R": 23,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 15.6 (c)",
   "stelle": "15.6 (c)",
   "ankerzeile": 1553,
   "anker": "> **(c)** *[ersetzt „behält",
   "zahl": 1,
   "nach": 1562,
   "anfang40": "> geschrieben.",
   "m1": "> ⭐ **15.6 (c) PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 35,
   "R": 51,
   "unterpunkt": "",
   "ziel": "5.3 und 15.6 → 33.2 (gültiger Faltenplan, alle neun Bots) [A66]",
   "stelle": "15.6",
   "ankerzeile": 1539,
   "anker": "### 15.6 Registertext 4 —",
   "zahl": 1,
   "nach": 1609,
   "anfang40": "   Werkzeug führt beide Listen und der S",
   "m1": "> ⭐ **15.6 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 36,
   "R": 21,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 (b)",
   "stelle": "16.4 (b)",
   "ankerzeile": 1943,
   "anker": "> **(b)** Nach dem Selektionslauf",
   "zahl": 1,
   "nach": 1968,
   "anfang40": "> **Bestätigt seit mindestens zwei Quart",
   "m1": "> ⭐ **16.4 (b) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 37,
   "R": 22,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 (a)",
   "stelle": "16.4 (a)",
   "ankerzeile": 1938,
   "anker": "> **(a)** Jeder Bot steht",
   "zahl": 1,
   "nach": 1968,
   "anfang40": "> **Bestätigt seit mindestens zwei Quart",
   "m1": "> ⭐ **16.4 (a) PRÄZISIERT durch R22 (47.5)** (Fable 27c R22, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 38,
   "R": 23,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 (b)",
   "stelle": "16.4 (b)",
   "ankerzeile": 1943,
   "anker": "> **(b)** Nach dem Selektionslauf",
   "zahl": 1,
   "nach": 1968,
   "anfang40": "> **Bestätigt seit mindestens zwei Quart",
   "m1": "> ⭐ **16.4 (b) PRÄZISIERT durch R23 (47.6)** (Fable 27c R23, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 39,
   "R": 37,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 16.4 (c)",
   "stelle": "16.4 (c)",
   "ankerzeile": 1949,
   "anker": "> **(c)** **Aufstieg** Grundbudget",
   "zahl": 1,
   "nach": 1968,
   "anfang40": "> **Bestätigt seit mindestens zwei Quart",
   "m1": "> ⭐ **16.4 (c) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 40,
   "R": 37,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 16.4 …/(d)",
   "stelle": "16.4 (d)",
   "ankerzeile": 1958,
   "anker": "> **(d)** **Abstieg** auf",
   "zahl": 1,
   "nach": 1968,
   "anfang40": "> **Bestätigt seit mindestens zwei Quart",
   "m1": "> ⭐ **16.4 (d) PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 41,
   "R": 18,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 (m)",
   "stelle": "16.4 (m)",
   "ankerzeile": 2006,
   "anker": "> **(m)** **Umsetzung ohne",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (m) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 42,
   "R": 18,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (h)",
   "stelle": "16.4 (h)",
   "ankerzeile": 1984,
   "anker": "> **(h)** Eine Zelle ist",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (h) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 43,
   "R": 18,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (l)",
   "stelle": "16.4 (l)",
   "ankerzeile": 2002,
   "anker": "> **(l)** ⭐ **Anlageklassen-Schlüssel,",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (l) PRÄZISIERT durch R18 (47.1)** (Fable 27c R18, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 44,
   "R": 19,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 (h)",
   "stelle": "16.4 (h)",
   "ankerzeile": 1984,
   "anker": "> **(h)** Eine Zelle ist",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (h) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 45,
   "R": 19,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (j)",
   "stelle": "16.4 (j)",
   "ankerzeile": 1993,
   "anker": "> **(j)** **Aufstieg:** mehr",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (j) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 46,
   "R": 19,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (k)",
   "stelle": "16.4 (k)",
   "ankerzeile": 1998,
   "anker": "> **(k)** Wird eine **neue",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (k) PRÄZISIERT durch R19 (47.2)** (Fable 27c R19, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 47,
   "R": 20,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 16.4 (l)",
   "stelle": "16.4 (l)",
   "ankerzeile": 2002,
   "anker": "> **(l)** ⭐ **Anlageklassen-Schlüssel,",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (l) ERGÄNZT durch R20 (47.3)** (Fable 27c R20, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 48,
   "R": 20,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 16.4 … (j)",
   "stelle": "16.4 (j)",
   "ankerzeile": 1993,
   "anker": "> **(j)** **Aufstieg:** mehr",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (j) ERGÄNZT durch R20 (47.3)** (Fable 27c R20, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 49,
   "R": 21,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (i)",
   "stelle": "16.4 (i)",
   "ankerzeile": 1989,
   "anker": "> **(i)** Innerhalb einer",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (i) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 50,
   "R": 21,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (j)",
   "stelle": "16.4 (j)",
   "ankerzeile": 1993,
   "anker": "> **(j)** **Aufstieg:** mehr",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (j) PRÄZISIERT durch R21 (47.4)** (Fable 27c R21, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 51,
   "R": 22,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.4 … (i)",
   "stelle": "16.4 (i)",
   "ankerzeile": 1989,
   "anker": "> **(i)** Innerhalb einer",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (i) PRÄZISIERT durch R22 (47.5)** (Fable 27c R22, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 52,
   "R": 24,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu 16.4 (h)",
   "stelle": "16.4 (h)",
   "ankerzeile": 1984,
   "anker": "> **(h)** Eine Zelle ist",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (h) ERGÄNZT durch R24 (47.7) und 50.6** (Fable 27c R24, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 53,
   "R": 24,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu 16.4 … (g)",
   "stelle": "16.4 (g)",
   "ankerzeile": 1972,
   "anker": "> **(g)** **Zellen sind Quelle",
   "zahl": 1,
   "nach": 2012,
   "anfang40": "> **Die Bots lesen `m_b`; sonst ändert s",
   "m1": "> ⭐ **16.4 (g) ERGÄNZT durch R24 (47.7) und 50.6** (Fable 27c R24, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 54,
   "R": 37,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 16.6",
   "stelle": "16.6",
   "ankerzeile": 2110,
   "anker": "### 16.6 Registertext 2d",
   "zahl": 1,
   "nach": 2155,
   "anfang40": "> Registertext oben bleibt zeichengleich",
   "m1": "> ⭐ **16.6 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 55,
   "R": 38,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 16.7 (d)",
   "stelle": "16.7 (d)",
   "ankerzeile": 2207,
   "anker": "> **(d)** **Berichtet je",
   "zahl": 1,
   "nach": 2216,
   "anfang40": "> (Tatsachennotiz in 16.1.2).",
   "m1": "> ⭐ **16.7 (d) ERGÄNZT durch R38 (48.6)** (Fable 29b R38, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 56,
   "R": 28,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu Register 18",
   "stelle": "Abschnitt 18",
   "ankerzeile": 2833,
   "anker": "## 18. Tatsachennotiz zu",
   "zahl": 1,
   "nach": 2891,
   "anfang40": "Festlegung.*",
   "m1": "> ⭐ **Abschnitt 18 ERGÄNZT durch R28 (47.11)** (Fable 27c R28, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 57,
   "R": 53,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz: … und 21.4 …",
   "stelle": "21.4",
   "ankerzeile": 3187,
   "anker": "### 21.4 Die berichtigte",
   "zahl": 1,
   "nach": 3230,
   "anfang40": "Falte für unwürdig erklärt.",
   "m1": "> ⭐ **21.4 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 58,
   "R": 34,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 22.2",
   "stelle": "22.2",
   "ankerzeile": 3484,
   "anker": "### 22.2 Registertext, Kill-Test-Berichtswerte",
   "zahl": 1,
   "nach": 3502,
   "anfang40": "registrieren. **Das ist kein Nachteil di",
   "m1": "> ⭐ **22.2 ERGÄNZT durch R34 (48.2)** (Fable 29b R34, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 59,
   "R": 36,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 24.2",
   "stelle": "24.2",
   "ankerzeile": 4100,
   "anker": "### 24.2 Der Registertext",
   "zahl": 1,
   "nach": 4116,
   "anfang40": "entscheidet nicht.",
   "m1": "> ⭐ **24.2 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 60,
   "R": 53,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz: Die Nachmessungen in 25.2 …",
   "stelle": "25.2",
   "ankerzeile": 4427,
   "anker": "### 25.2 Die Instanz — `t3_supertrend`",
   "zahl": 1,
   "nach": 4451,
   "anfang40": "**2018-01-14**. Fables Nachrechnung trif",
   "m1": "> ⭐ **25.2 ERGÄNZT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 61,
   "R": 53,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 4a (i) (25.3, …)",
   "stelle": "25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile)",
   "ankerzeile": 4461,
   "anker": "> **Registertext 4a / 21.3",
   "zahl": 1,
   "nach": 4468,
   "anfang40": "> ⭐ **(i) „im registrierten Datenhorizon",
   "m1": "> ⭐ **4a (i) in 25.3 PRÄZISIERT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 62,
   "R": 31,
   "unterpunkt": "(d)",
   "ziel": "Zu 27.3:",
   "stelle": "27.3 (im Zitatblock 27.1 bis 27.5)",
   "ankerzeile": 4931,
   "anker": "> **27.3** Das Register darf",
   "zahl": 1,
   "nach": 4938,
   "anfang40": "> Der Chat des Verfahrensprüfers wurde a",
   "m1": "> ⭐ **27.3 ERGÄNZT durch R31 (47.14)** (Fable 27c R31, Unterpunkt (d), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 63,
   "R": 32,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu 27",
   "stelle": "Abschnitt 27",
   "ankerzeile": 4910,
   "anker": "## 27. Sichtschutz des Verfahrensprüfers",
   "zahl": 1,
   "nach": 4974,
   "anfang40": "> 26a R6/R7, TB-114, 26.09.2026). Abschn",
   "m1": "> ⭐ **Abschnitt 27 ERGÄNZT durch R32 (47.15)** (Fable 27c R32, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 64,
   "R": 53,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 4a (i) (…, 28.6)",
   "stelle": "28.6",
   "ankerzeile": 5082,
   "anker": "### 28.6 Registertext 4a,",
   "zahl": 1,
   "nach": 5103,
   "anfang40": "der Satz ist zwischen zwei Antworten ver",
   "m1": "> ⭐ **28.6 PRÄZISIERT durch R53 (49.1)** (Fable 30a R53, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 65,
   "R": 43,
   "unterpunkt": "",
   "ziel": "Berichtigung zu 29.4 … lies",
   "stelle": "29.4",
   "ankerzeile": 5167,
   "anker": "### 29.4 Die Wache in TB-30b",
   "zahl": 1,
   "nach": 5182,
   "anfang40": "> Gemessen (TB-82, Beleg M4): heute in k",
   "m1": "> ⭐ **29.4 BERICHTIGT durch R43 (48.11)** (Fable 29b R43, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 66,
   "R": 43,
   "unterpunkt": "",
   "ziel": "Berichtigung zu …/34.5 … lies",
   "stelle": "34.5",
   "ankerzeile": 6006,
   "anker": "### 34.5 Berichtigung zu",
   "zahl": 1,
   "nach": 6030,
   "anfang40": "`multi_symbol_optimise.py`\".",
   "m1": "> ⭐ **34.5 BERICHTIGT durch R43 (48.11)** (Fable 29b R43, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 67,
   "R": 37,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 35.1",
   "stelle": "35.1",
   "ankerzeile": 6115,
   "anker": "### 35.1 Ergänzung zu 33.2",
   "zahl": 1,
   "nach": 6185,
   "anfang40": "21.4 — 21.4 bleibt unberührt, 35.1 zitie",
   "m1": "> ⭐ **35.1 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 68,
   "R": 26,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … 35.4",
   "stelle": "35.4",
   "ankerzeile": 6230,
   "anker": "### 35.4 Präzisierung zu",
   "zahl": 1,
   "nach": 6262,
   "anfang40": "> Der Text oben bleibt zeichengleich.",
   "m1": "> ⭐ **35.4 ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 69,
   "R": 49,
   "unterpunkt": "(e)",
   "ziel": "Zu 38.2:",
   "stelle": "38.2",
   "ankerzeile": 7088,
   "anker": "### 38.2 ⭐ Registertext,",
   "zahl": 1,
   "nach": 7124,
   "anfang40": "**35.1** (die Tatsachennotiz 38.7 (a), a",
   "m1": "> ⭐ **38.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (e), TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 70,
   "R": 42,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 40.6",
   "stelle": "40.6",
   "ankerzeile": 8048,
   "anker": "### 40.6 ⭐⭐ Die neun Handelslisten",
   "zahl": 1,
   "nach": 8158,
   "anfang40": "> 26.09.2026). Zitate, Text und die Mark",
   "m1": "> ⭐ **40.6 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 71,
   "R": 44,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 40.6",
   "stelle": "40.6",
   "ankerzeile": 8048,
   "anker": "### 40.6 ⭐⭐ Die neun Handelslisten",
   "zahl": 1,
   "nach": 8158,
   "anfang40": "> 26.09.2026). Zitate, Text und die Mark",
   "m1": "> ⭐ **40.6 ERGÄNZT durch R44 (48.12)** (Fable 29b R44, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 72,
   "R": 47,
   "unterpunkt": "",
   "ziel": "Präzisierung zu 40.6 (Tatsachennotiz zu 5.4: „Parameterdateien“)",
   "stelle": "40.6",
   "ankerzeile": 8048,
   "anker": "### 40.6 ⭐⭐ Die neun Handelslisten",
   "zahl": 1,
   "nach": 8158,
   "anfang40": "> 26.09.2026). Zitate, Text und die Mark",
   "m1": "> ⭐ **40.6 (Tatsachennotiz zu 5.4) PRÄZISIERT durch R47 (48.15)** (Fable 29b R47, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 73,
   "R": 41,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 41.2 B6/B7",
   "stelle": "41.2, Eintrag B6/B7",
   "ankerzeile": 8572,
   "anker": "**B6/B7 — `haltedauern_je_bot.csv`",
   "zahl": 1,
   "nach": 8580,
   "anfang40": "Umstellung auf die neue Quelle hängt am ",
   "m1": "> ⭐ **41.2 B6/B7 ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 74,
   "R": 29,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 42.2 E5",
   "stelle": "42.2, Eintrag E5 (e)",
   "ankerzeile": 8946,
   "anker": "**E5 (e) — Berichtigung zu",
   "zahl": 1,
   "nach": 8963,
   "anfang40": "steht aus (42.6).",
   "m1": "> ⭐ **42.2 E5 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 75,
   "R": 29,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu 44-6",
   "stelle": "44.1, Eintrag 44-6",
   "ankerzeile": 9717,
   "anker": "**44-6 — Nach dem Zusammenführen",
   "zahl": 1,
   "nach": 9734,
   "anfang40": "Laufbereichsmessung, und die Liste wird ",
   "m1": "> ⭐ **44-6 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 76,
   "R": 42,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … 45.3",
   "stelle": "45.3",
   "ankerzeile": 9940,
   "anker": "### 45.3 R3 — Ergänzung zu",
   "zahl": 1,
   "nach": 9951,
   "anfang40": "> 26.09.2026). Zitat und Kette oben blei",
   "m1": "> ⭐ **45.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 77,
   "R": 29,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … R4",
   "stelle": "45.4, Block R4",
   "ankerzeile": 9955,
   "anker": "> **R4 — Ergänzung zu 19",
   "zahl": 1,
   "nach": 9956,
   "anfang40": "> *Quelle des Grundes:* Prüfprinzip B3 (",
   "m1": "> ⭐ **45.4 (R4) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 78,
   "R": 29,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … R5 (a)",
   "stelle": "45.5, Block R5, Punkt (a)",
   "ankerzeile": 9967,
   "anker": "> (a) Die Laufbereichsmessung",
   "zahl": 1,
   "nach": 9970,
   "anfang40": "> *Quelle des Grundes:* 24b A10 (kein Fa",
   "m1": "> ⭐ **45.5 (R5) (a) ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 79,
   "R": 33,
   "unterpunkt": "",
   "ziel": "Berichtigung zu 45.5 (b) … lies",
   "stelle": "45.5, Block R5, Punkt (b)",
   "ankerzeile": 9968,
   "anker": "> (b) `zellen.csv` enthält",
   "zahl": 1,
   "nach": 9970,
   "anfang40": "> *Quelle des Grundes:* 24b A10 (kein Fa",
   "m1": "> ⭐ **45.5 (b) BERICHTIGT durch R33 (48.1)** (Fable 29b R33, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 80,
   "R": 34,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … 45.5",
   "stelle": "45.5",
   "ankerzeile": 9964,
   "anker": "### 45.5 R5 — Abnahmebedingungen",
   "zahl": 1,
   "nach": 9976,
   "anfang40": "Zeile (5).",
   "m1": "> ⭐ **45.5 ERGÄNZT durch R34 (48.2)** (Fable 29b R34, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 81,
   "R": 36,
   "unterpunkt": "",
   "ziel": "Präzisierung zu … 45.5",
   "stelle": "45.5",
   "ankerzeile": 9964,
   "anker": "### 45.5 R5 — Abnahmebedingungen",
   "zahl": 1,
   "nach": 9976,
   "anfang40": "Zeile (5).",
   "m1": "> ⭐ **45.5 PRÄZISIERT durch R36 (48.4)** (Fable 29b R36, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 82,
   "R": 39,
   "unterpunkt": "",
   "ziel": "Ergänzung zu 46.3 (R12)",
   "stelle": "46.3",
   "ankerzeile": 10154,
   "anker": "### 46.3 R12 — Tatsachennotiz",
   "zahl": 1,
   "nach": 10164,
   "anfang40": "die neun heutigen Listen.",
   "m1": "> ⭐ **46.3 ERGÄNZT durch R39 (48.7)** (Fable 29b R39, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 83,
   "R": 42,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … 46.3",
   "stelle": "46.3",
   "ankerzeile": 10154,
   "anker": "### 46.3 R12 — Tatsachennotiz",
   "zahl": 1,
   "nach": 10164,
   "anfang40": "die neun heutigen Listen.",
   "m1": "> ⭐ **46.3 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 84,
   "R": 25,
   "unterpunkt": "",
   "ziel": "als Ergänzung zu … R14",
   "stelle": "46.5, Block R14",
   "ankerzeile": 10188,
   "anker": "> **R14 — Ergänzung zu 12",
   "zahl": 1,
   "nach": 10189,
   "anfang40": "> *Quelle des Grundes:* Docstring von `a",
   "m1": "> ⭐ **46.5 (R14) ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 85,
   "R": 26,
   "unterpunkt": "",
   "ziel": "Ergänzung zu … R14",
   "stelle": "46.5, Block R14",
   "ankerzeile": 10188,
   "anker": "> **R14 — Ergänzung zu 12",
   "zahl": 1,
   "nach": 10189,
   "anfang40": "> *Quelle des Grundes:* Docstring von `a",
   "m1": "> ⭐ **46.5 (R14) ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 86,
   "R": 27,
   "unterpunkt": "",
   "ziel": "Tatsachennotiz zu R14 Bedingung 5",
   "stelle": "46.5, Block R14 (Bedingung 5 steht in dessen erster Zeile)",
   "ankerzeile": 10188,
   "anker": "> **R14 — Ergänzung zu 12",
   "zahl": 1,
   "nach": 10189,
   "anfang40": "> *Quelle des Grundes:* Docstring von `a",
   "m1": "> ⭐ **46.5 (R14), Bedingung 5 ERGÄNZT durch R27 (47.10)** (Fable 27c R27, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  },
  {
   "nr": 87,
   "R": 25,
   "unterpunkt": "",
   "ziel": "Bestätigung von 46.9",
   "stelle": "46.9",
   "ankerzeile": 10239,
   "anker": "### 46.9 Lesart des steuernden",
   "zahl": 1,
   "nach": 10251,
   "anfang40": "`auswertung.py`.",
   "m1": "> ⭐ **46.9 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, ⟨DATUM⟩).",
   "m2": "> Eintrag und Stand oben bleiben zeichengleich."
  }
 ],
 "r54_unter_48_16": {
  "anker": "> R48 — Lesarten zu Register 0–12 (TB-121), je mit Fundstelle.",
  "stelle": "am Ende von 48.16, nach dem Zitatblock R48, vor **Kette:**",
  "m1": "> ⭐ **48.16 R48 (g) BERICHTIGT durch R54 (49.2)** (Fable 30a R54, TB-126, ⟨DATUM⟩).",
  "m2": "> Eintrag und Stand oben bleiben zeichengleich."
 }
}
DATEN-ENDE
```
