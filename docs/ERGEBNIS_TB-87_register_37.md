# ERGEBNIS TB-87 — Registerabschnitt 37: die Sonde meldet je Bestandteil, das Abbild führt zwei Gruppen, was ein Befund `1` bedeutet, hängt vom Tag ab, die Tatsachennotiz zu den zwei Listen in `herkunft.py`, der Ort registrierter Werte — und vier Messabweichungen (Mac-Sitzung, 22.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-87_register_37.md` (Zeiger
`AKTUELLER_AUFTRAG.md` nannte TB-87, gleich der vorangestellten Nummer).
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `40aa715` (= `origin/main`
beim Start; erwartet `5ead288` oder jünger). Commits `b6b3a61` (Schritt 0/1),
`bd15895` (Schritt 2), `c474da7` (Schritt 3/4) und der Abgabe-Commit — jeder
einzeln gepusht. Belege `docs/belege/TB-87/`. Geändert: **nur `docs/`** — das
Register (append- und insert-only, **317 / 0**), dreizehn Belegdateien, dieses
Dokument, ein Journalblock. ⛔ **Keine `.py` geändert, kein neues Abbild, keine
Sonde angepasst, keine Werte verschoben, kein `python3 faltenplan.py`.**

⚠️⚠️ **Drei Sperrlisten-Hashes, vorweg:** `0e54ac5c…` · `a163c498…` ·
`4549395f…` — **vor** der Arbeit (17:09Z), **nach** Schritt 3 (17:15Z) und in
der Abschlussprüfung (17:16Z) gleich; 0 Commits auf `research/`, `git status`
auf `research/ shared/ strategies/` leer. Abbruchkriterium 5 nicht eingetreten.

*In einfacher Sprache, zu Beginn:* Fünf Texte des Prüfers stehen jetzt im
Regelwerk (Abschnitt 37) und als Hinweis an sieben alten Stellen. Der
wichtigste: Meldet das Prüfprogramm vor dem Stichtag eine geänderte geschützte
Datei, ist das normal, wenn die Änderung beauftragt war — nach dem Stichtag
wäre es ein Regelbruch. Beim Nachmessen stimmten vier Einzelheiten aus den
Vorlagen nicht; eingetragen ist, was gemessen wurde.

---

## Die fünf Einträge im Register (Zeilen nach `c474da7`)

| Eintrag | Z. | Inhalt |
|---|---:|---|
| Kopf Abschnitt 37 | 6224 | Herkunft, Regel „Marke am alten Ort", Hinweis zur Quellform der Zitate und zur Sondenverträglichkeit der Marken |
| **37.1** | 6254 | Präzisierung zu 36.5: die Sonde meldet je Punkt je Bestandteil (22d Z. 13), Grund (Z. 11), Quelle (Z. 15); Tatsachennotiz M1 |
| **37.2** | 6282 | Ergänzung zu 36.6: zwei Gruppen im Abbild (22d Z. 21), Quelle (Z. 23); Tatsachennotiz: die Sonde nennt den bestimmten Pfad heute nur |
| **37.3** | 6302 | ⭐⭐ Ergänzung zu 36.2/36.6: was ein Befund `1` bedeutet, hängt vom Tag ab (22g Z. 13), Grund (Z. 11), Quelle (Z. 15), der Sondensatz (aus Z. 9, dazu der volle Absatz), Handwerkshinweis (Z. 17); Tatsachennotiz M2 — der erste Anwendungsfall TB-86 |
| **37.4** | 6352 | Fables Tatsachennotiz zu Abschnitt 10 (22d Z. 27) und seine Entscheidung (Z. 29); Nachmess-Tabelle M3 mit **zwei Abweichungen**; Randbefund aus TB-84 |
| **37.5** | 6410 | Ersteintrag „Ort registrierter Werte" (22d Z. 39–43), Befund mit Kernsatz (Z. 33), drei Wege (Z. 35), Quelle und „Kein Ergebnis"-Satz (Z. 45); Tatsachennotiz (4) M4 mit **zwei Abweichungen**; Fables Frage (Z. 47); **Offen** (Z. 59) |
| 37.6 | 6485 | Was nicht getan wird, und das Offene |

**Die sieben Marken am alten Ort** (nur eingefügt, 38 / 0):

| Marke für | Z. | Ort | Form |
|---|---:|---|---|
| 37.1–37.5 (v. a. 37.4, 37.3) | 822 | unter der Überschrift von Abschnitt 10, als zweiter Block unter dem Hinweis aus 36.2/36.6 | `>`-Block, elf Zeilen |
| 37.5 | 867 | Sperrlistenpunkt 7 | `   >`, **ohne Leerzeile** (sondenverträglich) |
| 37.5 | 884 | Sperrlistenpunkt 9 | `   >`, ohne Leerzeile |
| 37.3 | 5996 | 36.2, unter der Marke aus 36.5 | `> >`, eine Zeile |
| 37.1 | 6130 | 36.5, unter dem Registertext | `> >`, eine Zeile |
| 37.2 | 6162 | 36.6, unter dem Registertext | `> >`, eine Zeile |
| 37.3 | 6164 | 36.6, unter der Marke aus 37.2 | `> >`, eine Zeile |

## M1–M6 — gemessen, nicht erwartet

| # | Messung | erwartet | **gemessen** |
|---:|---|---|---|
| **M1** | Gibt die Sonde je Bestandteil aus? | ja | **ja** — `TB-85/nullpunkt.txt` Punkt 1: Datei-Hash (`registerdaten.py`, `gleich`, `141fa14b…`) und daneben der unmessbare Teil. Der **Rückgabewert** steht je Punkt (Punkt 1 = `2`, obwohl sein Pfad `gleich` ist) und je Lauf. ⚠️ Nebenbefund: den bestimmten Pfad `_vt.json` **nennt** die Sonde nur („nicht geprueft, nur genannt") — in 37.2 eingetragen |
| **M2** | Hash `faltenplan.py` heute · im Abbild | `fd3e5018…` · `6f96b95d…` | **`fd3e5018…`** (letzter Commit `4daa254`, TB-86) · **`6f96b95d…`** im Abbild `6a1b732e…`, Punkt 2. Sonde: Punkt 2 `1 BEFUND`, Lauf `1` |
| **M3** | `herkunft.py` Z. 57/66/114 · fünf Abweichungen | 57, 66, 114 · drei fehlend, drei zusätzlich | **57, 66, 114** ✔. ⚠️ **Abweichung (a):** der Datenvertrag steht in `auswertung.py` **Z. 51**, nicht Z. 41. ⚠️ **Abweichung (b):** Fable zählt „fünf" und nennt sechs Namen; der mechanische Mengenvergleich gegen die zehn Pfade der vierzehn Punkte ergibt **vier fehlend** (`top25`, `sp500`, **`herkunft.py`**, **`shared/zuteilung.py`**) plus den bestimmten `_vt.json`, und **vier zusätzlich** (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, **`ergebnisse/messgroessen.json`**). Alle anderen Aussagen der Notiz bestätigt |
| **M4** | Orte der vier Werte | neun `forward_test.py` · `messgroessen.py:59` · `registerdaten.py:99`, `:115` | neun `forward_test.py` ✔ (`0.1`/`0.05`) · `registerdaten.py:99` `CLUSTER_SCHWELLE = 0.90` ✔ · `:115` `N_HISTORISCH_JE_BOT` (neun Einträge) ✔ · ⚠️ **Abweichung (c):** `messgroessen.py:59` ist nur `SLIPPAGE_PCT`; die Gebühr steht in **Z. 58 als `GEBUEHR_PCT`** — ein `TRADING_FEE_PCT` gibt es dort nicht. ⚠️ **Abweichung (d):** auch **neun `backtest_*.py`** tragen je eine eigene Zuweisung, dazu `signal_quality_test.py:37–38` als Verweis |
| **M5** | Faltenliste 33.2 vor/nach | identisch | **identisch** — 9 Zeilen, SHA-256 `e5ab322e…` beide Male (= TB-82 bis TB-84), `diff` leer |
| **M6** | drei Sperrlisten-Hashes vor/nach | unverändert | **unverändert** (siehe oben) |
| Zusatz | Sperrlisten-Sonde lesend vor und nach den Marken | — | Prüfung (ii) beide Male **`0`**, „Listentext wie bei Erzeugung: **ja**"; einziger Unterschied die Zeilenlage (Z. 824–871 → 836–901). Bilanz `1 / 1 / 12`, rc `1` — unverändert |

Belege: `m1_sonde_je_bestandteil.txt` … `m6_hashes.txt`, `sonde_vorher.txt`,
`sonde_nachher.txt`, Befehl jeweils in Zeile 1.

## Der `numstat`-Nachweis

`git diff --numstat 40aa715..c474da7`: Register **`317 0`**, elf Belegdateien
je `n 0`; **0 Dateien ausserhalb `docs/`, 0 Zeilen mit Spalte 2 ≠ 0**
(`schritt5_abschluss.txt`). Der Abgabe-Commit fügt dieses Dokument, den
Journalblock (insert-only) und einen Abschlussbeleg hinzu — nachgetragen in
`schritt9_abgabe.txt`.

Zeichengleichheit (`schritt2_nachweise.txt`): **22 Quellzeilen** (17 aus 22d,
5 aus 22g) je **genau 1×** als Registerzeile, im ganzen Register 1×; die drei
Teilzeichenketten des Auftrags (Kernsatz, Sondensatz, „Die Werte selbst …")
je in Quelle und Abschnitt; Positivkontrolle ohne Präfix 0.

## Abweichungen vom Auftrag — mit Begründung

| | Abweichung | Begründung |
|---|---|---|
| 1 | Fable-Texte in **voller Quellform** statt der Auftragsform („, Vorschlag" in zwei Kopfzeilen; „Folge für `herkunft.py`, Entscheidung:"; die Gründe zu 37.1 und 37.3 ohne „…"; „Kein Ergebnis — …" samt Quellenvorsatz) | Der Auftrag zitiert Kurzformen; zeichengleich ist nur die Quelle (`C1`, wie TB-81–84). Abbruchkriterium 3 greift nicht — die Quelle **ist** zeichengleich übernehmbar |
| 2 | Zusätzlich eingetragen: Fables Abwägung der drei Wege (22d Z. 35), seine Frage nach den Optimierern (Z. 47), sein Handwerkshinweis zu Abbild-Bündeln (22g Z. 17) | gehören zum Stand der Sache; Z. 47 ist die Quelle der Messung aus Plan Punkt 5, auf die der Auftrag verweist |
| 3 | „Offen (Fable 22d)" als **Fables Wortlaut** (22d Z. 59, „Unsicher: …"), der Messhinweis zu Plan 5 als eigener Satz darunter | der Kasten im Auftrag mischt Fables Satz mit einem Zusatz des steuernden Chats |
| 4 | **Vier Messabweichungen** (a)–(d) eingetragen, Fables Sätze zeichengleich daneben | Auftrag M3/M4: „eintragen, was du misst, und melden" |
| 5 | **Zwei Zusatzbelege** (lesender Sondenlauf vor/nach) | die Marken in Abschnitt 10 verändern den Text, den die Sonde liest; ohne diese Messung wäre offen, ob die Marken Prüfung (ii) brechen. Die Sonde wurde **nicht** geändert, nur ausgeführt |
| 6 | Die Marken an Punkt 7 und 9 stehen **ohne Leerzeile** unter dem Punkt | `lies_abschnitt_10` beendet die Liste an einer Leerzeile vor einer eingerückten Zeile; eine Leerzeile hätte Punkte 8–14 aus der Sondenlesung geschnitten |
| 7 | Ein zunächst gesetzter **achter** Hinweis (37.4 in 36.6, am Satz „an fünf Stellen …") wurde **vor** dem Commit wieder herausgenommen | nicht im Auftrag, und 37.6 sagt „sieben Marken"; im Commit nie enthalten |
| 8 | Ergebnisdokument unter `docs/ERGEBNIS_TB-87_register_37.md` | Reihe seit TB-80; Journal-Quellenzeile |
| 9 | Belege heissen `m1_sonde_je_bestandteil.txt` usw. statt `m1…m6.txt` | sprechende Namen, Präfix `m1`–`m6` wie verlangt |

## Was NICHT getan wurde — ausdrücklich

⛔ Keine `.py` geändert (`git diff --name-only 40aa715..HEAD`: nur `docs/`).
⛔ **Kein neues Abbild** — das Abbild `6a1b732e…` bleibt, der Befund `1` an
Punkt 2 bleibt stehen. ⛔ **Keine Sonde angepasst** — nur zweimal lesend
ausgeführt. ⛔ **Keine Werte verschoben.** ⛔ `herkunft.py` nicht geöffnet
(nur `grep`/`sed`/`ast`). ⛔ Kein `python3 faltenplan.py`. ⛔ Keine Freigabe
erteilt oder unterstellt.

## ⚠️ Offen und benannt — nicht Teil dieses Auftrags

| | | bei wem |
|---|---|---|
| 1 | Die Sonde muss je Bestandteil **zurückgeben** (37.1) und die Gruppe „bestimmt" **prüfen** statt nur nennen (37.2) | Handwerk, Freigabe |
| 2 | **Das neue Abbild** unter neuem Namen (Plan 2b) — schliesst den Befund `1` aus 37.3. Der Hash des geltenden Abbilds `6a1b732e…` steht nur in Tatsachennotizen, **nicht** als eigener Registereintrag nach 36.6 („Das aktuelle Abbild steht selbst mit Hash im Register"); ⚠️ Journal CN hatte das TB-87 zugeschrieben — der Auftrag TB-87 enthielt es nicht | eigene Aufgabe |
| 3 | **Die Messung aus Plan Punkt 5:** woher lesen die neun `multi_symbol_optimise.py` und `equity_simulation.py` Kosten und Slippage? ⭐ M4 (d) liefert einen Hinweis — neun `backtest_*.py` tragen eigene Kopien —, beantwortet die Frage aber **nicht** | eigener Auftrag |
| 4 | **Fables Unsicherheit** (37.5): dürfen die Abschnitt-0-eingefrorenen `messgroessen.py`/`registerdaten.py` für (3) geändert werden, oder trägt ein neues kleines Modul die vier Werte? Dazu (c): in `messgroessen.py` heisst die Gebühr `GEBUEHR_PCT` | Fable / Betreiber |
| 5 | **Die vier Messabweichungen** (a)–(d) — Fable zur Kenntnis | steuernder Chat → Fable |
| 6 | Unverändert: Schritt 3 aus 36.3 (Z. 336, eigene Freigabe), 35.5, 33.5, TB-30b, 32.5, (20g)–(20m), `K4t` | — |

## In einfacher Sprache

**Was gemacht wurde:** Fünf Texte des Prüfers stehen jetzt im Regelwerk und an
sieben alten Stellen als Hinweis. Der wichtigste sagt, was eine Meldung des
Prüfprogramms bedeutet: vor dem Stichtag — wenn beauftragt — ein normaler
Vorgang, der mit einer neuen Prüfliste erledigt wird; nach dem Stichtag ein
Regelbruch. Der erste solche Fall (die heute geänderte Datei) steht mit alter
und neuer Prüfsumme drin.

**Was gemessen wurde:** Die geschützten Dateien sind unverändert, die
Auswertungsjahre auch. Das Prüfprogramm liest die Schutzliste nach den neuen
Hinweisen genauso wie vorher.

**Was aufgefallen ist:** Vier Einzelheiten aus den Vorlagen stimmten nicht
genau: eine Zeilennummer (51 statt 41), eine Zählung (es sind je vier
Unterschiede, nicht „fünf"), ein Name (die Gebühr heisst an einer Stelle
anders) und ein fehlender Ort (auch die neun Backtest-Programme tragen die
Kosten selbst). Eingetragen ist jeweils die Messung, neben dem
unveränderten Satz des Prüfers.

**Was nicht gemacht wurde:** Kein Programm geändert, keine neue Prüfliste,
keine Werte verschoben.

---

## Deine Aufgaben

1. **Fable vorlegen:** Abschnitt 37 (Z. 6224 ff.) mit den vier Messabweichungen — *Wo:* `docs/VORREGISTRIERUNG_neuselektion.md` 37.4 und 37.5, Belege `docs/belege/TB-87/m3_herkunft_listen.txt` und `m4_werte_orte.txt` — *Woran:* ob „fünf Stellen" und die Orte in (4) berichtigt werden sollen, und ob `GEBUEHR_PCT` und die neun `backtest_*.py` seine Entscheidung zu (3) berühren.
2. **Beauftragen, wenn gewollt:** Plan Punkt 2b (neues Abbild) und Plan Punkt 5 (woher lesen die Optimierer Kosten?) — beide ohne Auftrag.

Nicht von dir abhängig: nichts weiter aus diesem Auftrag; alle Commits sind gepusht.
