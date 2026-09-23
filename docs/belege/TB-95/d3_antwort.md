# Antwort auf die Messbitte 23f Abschnitt 6 — die neun Handelslisten im Modus-Lauf

*TB-95, 23.09.2026, Code-Stand `9e2a071` (für alle Dateien des Laufs gleich `fcc3265`). Belege:
`docs/belege/TB-95/d1_wer_oeffnet.txt`, `d2_stoerprobe.txt`, `d_lauf_log.txt`, `d1_protokoll_auszug.tsv`.
Sichtschutz 27.1: nur Verfahrensseite, keine Ergebnisgrössen.*

**Die Dateien:** `research/tb24_haltedauern/daten/<bot>_alle_trades.csv`, neun Stück, eine je Bot.

## 1. Welcher Schritt öffnet sie

**`benchmark.py` selbst, über seinen einzigen Aufruf des Faltenplans**, nicht über einen Nebenweg.
Gemessen mit Lesehaken und Aufrufstapel in einem Modus-Lauf gegen den Snapshot `63e4b6c8…`:

`benchmark.py::je_bot` (Z. 222, `plan = fp.faltenplan(mess)`) → `faltenplan.py::faltenplan` →
`_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (Z. 133, `pd.read_csv`).

Jede der neun Listen wird genau einmal geöffnet, nur im Hauptprozess. Die zehn Kindprozesse
(Trockenlauf/Loader) öffnen keine davon, `registerdaten.py` ebenfalls nicht. Derselbe Lauf lieferte
die registrierte Tabelle bytegleich (`64fb2912…`) und ist damit die fünfte Wiederholung des
Determinismusnachweises.

## 2. Gehen die Inhalte in die Tabelle ein? — **Ja, über genau eine Grösse: die Faltenlänge**

| Weg | Befund |
|---|---|
| **(a) Datenfluss** | Gelesen wird nur die Spalte `entry_time`. Daraus werden Einträge je vollem Kalenderjahr gezählt (Randjahre weg) und gemittelt, und das Mittel wird mit der Schwelle aus 5.4 (30) verglichen: darunter zwei Jahre Faltenlänge, sonst eines. Die Faltenlänge bestimmt Grenzen und Namen der Falten, und für jede Falte hat die Tabelle eine Zeile. Sonst erreicht nichts aus den Listen die Tabelle |
| **(b) Störprobe** auf Kopien, Originale vorher = nachher | **Eine Zeile entfernt:** Tabelle **bytegleich** (`64fb2912…`), weil die Schwelle nicht überschritten wird. **Zwei von drei Zeilen entfernt** (Mittel unter der Schwelle): Tabelle **verschieden** (`97cf224f…`). Nur der gestörte Bot ändert sich, von Einjahres- auf Zweijahresfalten; die anderen acht bleiben gleich |

(a) und (b) stimmen überein. ⚠️ Eine Störprobe mit nur einer Zeile hätte für sich allein „geht nicht
ein“ ergeben. Die Inhalte wirken als Schwellenentscheidung: Kleine Änderungen sind unsichtbar,
ein Übertritt verschiebt den ganzen Faltenplan des Bots und damit seine Tabellenzeilen.

## 3. Ihr Eingabestand

| | gemessen |
|---|---|
| Liegen sie im Snapshot? | **Nein.** Der Snapshot enthält 223 Kurs-CSV, `config/` und `MANIFEST.json`; die Listen kommen im Modus-Lauf aus dem Repo |
| Auf der Sperrliste? | **Nein** (so auch Register 39.8, „zwei Eingaben ohne registrierten Eingabestand“) |
| Im Register genannt? | **Ja, als Quelle, aber ohne Hash:** 5.4 („Gerechnet aus den gefundenen Trades je vollem Kalenderjahr (`research/tb24_haltedauern/daten/<bot>_alle_trades.csv`)“). Das **Ergebnis** (Faltenlänge je Bot) steht registriert in 5.4 und in der Tabelle von 33.2 |
| Commit und Datum | ein einziger Commit: **`78e2bc6`, 13.09.2026, „TB-24: Haltedauern und Zeithorizonte der neun Bots gemessen“**; seitdem unverändert (`git log -- research/tb24_haltedauern/daten/`) |
| Sind es die TB-24-Listen? | **Ja** — gemessen an Pfad, Commit und Datum, nicht am Namen. Erzeugt von `research/tb24_haltedauern/alle_bots.py` am Code- und Datenstand vom 13.09.2026, also **vor** TB-31 (Krypto-Historie), TB-34 (Kursdaten-Neuaufbau, 15.09.) und TB-38 (Entscheidungskerze) und damit vor dem Snapshot (19.09.). Die Krypto-Listen beginnen frühestens 2021-09, am damaligen Datenbeginn — die Faltenlänge der Krypto-Bots ruht also auf den Jahren ab 2022, obwohl ihre Falten 2018/2019 beginnen |

## 4. Einordnung — für den Verfahrensprüfer

Nach der Unterscheidung in 23f ist es der Fall **„sie gehen ein“**: Die Benchmark-Tabelle — und
schon vorher der Faltenplan selbst — hat eine Eingabe, deren Eingabestand nicht registriert ist.
Das ist derselbe Fall wie `messgroessen.json`, und die Regel aus 23d greift.

Zwei Umstände, die die Entscheidung betreffen, ohne sie vorwegzunehmen:

1. Die Wirkung läuft **ausschliesslich über die Faltenlänge**, und die ist als **Ergebnis**
   registriert (5.4, 33.2). Eine Änderung der Listen, die eine Faltenlänge kippt, würde deshalb als
   Abweichung des gerechneten Plans vom Registertext 33.2 sichtbar — vorausgesetzt, der Plan wird vor
   dem Lauf gegen ein Abbild geprüft (35.4). Dieses Abbild (33.3) ist nach 33.5 noch nicht erzeugt.
2. Die Listen stehen in genau einem Commit, und der ist über `git` reproduzierbar. Ein Nachweis
   „aus dem registrierten Snapshot“ im Sinn von 23d ist mit ihnen aber **nicht** möglich, weil sie
   nicht darin liegen.

**Offene Frage an ihn (nur das Ob):** Genügt für eine Eingabe, die nur über eine registrierte
Schwellenentscheidung wirkt, ein Hash-Eintrag (Sperrliste oder Tatsachennotiz mit Hash), oder
gilt die volle Regel aus 23d: Aufnahme in einen Snapshot und ein Nachweislauf auf demselben Weg?
