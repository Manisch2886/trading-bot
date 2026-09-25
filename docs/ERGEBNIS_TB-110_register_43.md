# TB-110: Ergebnis. Register 43 eingetragen — die Einträge aus Fable 25d und 25e, eine vorläufige Berichtigung an 25e (3) mit Verhaltensbeleg und die Tatsachennotizen TB-107 bis TB-109; 31 Zitate mit `diff` rc 0, 6 Marken, numstat 345/0

**Sitzungstitel:** `TB-110` (Anschluss in der Sitzung TB-109, Block H) · **Stand:** 26.09.2026, ca. 01:00 · **Auftrag:**
`docs/auftraege/MAC_TB-110_register_43.md` · **Belege:** `docs/belege/TB-110/`
**Eingang:** `723281f` (Abgabe TB-109). Commits: `474ced1` (Abschnitt 43 und alle Marken in einem Commit) und der
Abgabe-Commit (Belege, dieses Dokument, Journalblock DI).
**Grundlage:** Fable 25d (Abschnitt 1, 2, 3 a–e), Fable 25e (Abschnitt 1, 2, 3 a–d), Ergebnisse TB-108 und TB-109.
Freigabe des Betreibers 25.09.2026, 23:04 (Auswahlkarte, wörtlich im Auftrag).
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6).

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Vorbedingungen erfüllt: Abgabe TB-109 `723281f`, `git status` leer, TB-109 ohne Abbruchkriterium. Register 9127 Zeilen, `register()` `c85dd6c3…`, Sonde 25/0/0 und (ii) 0 (`0_stand.txt`, `0_sonde_vorher.txt`) |
| ⭐⭐ **A/B** | Abschnitt 43 mit 43.0–43.6: die 15 Einträge der Arbeitsliste (43-1 bis 43-15) je mit eingesetztem Zitat, Art, gemessenem Stand und Kette; **43-11 als vorläufige Berichtigung des steuernden Chats** gekennzeichnet. **6 Marken** am alten Ort: 5.1 Nr. 8 · 12 · 15.3 (unter der Tatsachennotiz zu 1c) · 36.5 · 37.4 · 42.6. **Keine in Abschnitt 10** |
| ⭐ **C** | numstat **345/0**; **31/31 Zitate** `diff` rc 0 (23 Zeilen, 8 Teile); Sonde vorher = nachher (25/0/0, (ii) 0; nur die angezeigten Zeilen des Listentexts 894–1007 ⇒ 901–1014); `register()` `c85dd6c3…` ⇒ `c92900a8…`; `test_vorregistrierung` **196/196 rc 0** (876 s); außerhalb `docs/` 1539 Dateien und 12 `*.db` gleich |
| ⚠️ | Kein Abbruchkriterium. Zwei Stellen, an denen der Eintrag vom Auftrag abweicht: Abschnitt 5 |

---

## 1. Vorbedingungen

`docs/belege/TB-110/0_stand.txt`, `0_sonde_vorher.txt`.

| | |
|---|---|
| Abgabe TB-109 | `723281f` = HEAD am Eingang; `git status --porcelain` leer bis auf den neuen Belegordner; `.git/*.lock` keine |
| Register | 9127 Zeilen, `ed20408c…`, numstat gegen HEAD leer |
| `herkunft.register()` | `c85dd6c3…`, `fehlend []` |
| Sonde gegen `40ffe18d…` | 25/0/0, Prüfung (ii) 0, rc 2 nur NICHT PRÜFBAR |
| Stand je Eintrag | `auswertung.py` `83c6bc3c…` (12 × `raise Abbruch`, `class Abbruch(SystemExit)` Z. 118); `herkunft.py` `351f24c2…` (`TB30A_BASE_DIR` Z. 51); `benchmark.py` `aeeec9b8…`; `faltenplan_neun.py` `251029be…` (letzter Commit `f5fdb53`, kein `revert`); `pfadvergleich.py` `bb609d08…` (`8570ce8`); `registerbericht.py --pruefen` rc 1 |

## 2. Block A/B: Abschnitt 43

Gebaut mit `docs/belege/TB-110/eintrag_register_43.py`, Bauart TB-108: Vorlage
`abschnitt43_vorlage.md` mit Platzhaltern ⟦Z:q:n⟧ (ganze Quellzeile) und
⟦T:q:n|…⟧ (Teil einer Quellzeile), vom Skript **eingesetzt**, nicht abgetippt.
Jede Marke wird hinter einer Ankerzeile eingefügt, die im Zielabschnitt genau
einmal vorkommt. Wachen: Eingangslänge 9127, kein `## 43.` vorhanden, 6 Marken,
keine Marke zwischen `## 10.` und `## 11.`, Parser-Zeilen (G6, `ERSETZT durch
Abschnitt 15`, `| **730** |`, `## 10. Die Sperrliste`, ERZEUGT-Block) gleich
oft wie vorher, jede alte Zeile in derselben Reihenfolge (additiv). **Probelauf
gegen eine Kopie** (`probelauf.sh`, `TB110_PROBE`): Einsetzen rc 0, 31/31 Zitate
rc 0, Sonde gegen die Kopie (ii) 0; erst dann einmal gegen das Register.

| Unterabschnitt | Inhalt |
|---|---|
| 43.0 | Anlass (25d/25e überschreiben „Auf Register 41/42, zusätzlich“, 41/42 waren eingetragen ⇒ 43), Kette „beantwortet in 43.1/43.2“ zu 42.6 (1)/(2), 25f bleibt offen, Herkunftsnotiz der Quellen wie 41.0, Bauart, Marken-Regel |
| 43.1 | 25d: Fables Liste; **43-1** Ersteintrag Ausgänge von `auswertung.py` (Stand: nicht vollzogen, 12 Stellen, heute rc 1); **43-2** Tatsachennotiz zu Punkt 4 (Interpolation, Grenzwert 0), mit Verweis auf Punkt 4, ohne Marke in 10; **43-3** Kopie in `faltenplan_neun.py`, `f5fdb53` steht; **43-4** zweite Öffnung `herkunft.py` (Plan, nicht vollzogen; Auftrag TB-111 im Worktree, nicht auf `main`); **43-5** Tatsachennotizen TB-106; **43-6** `registerbericht --pruefen` rot |
| 43.2 | 25e: Fables Liste; **43-7** Ergänzung „null Trades“ (vollzogen TB-109, Nullzeile im Erzeuger offen); **43-8** zwei weitere Ablagen (vollzogen); **43-9** (iv) im Audit, mit Tatsachennotiz zur Reichweite (11 statt 21, offen bei Fable); **43-10** Stummel |
| 43.3 | **43-11** Berichtigung `None` statt `False`, Verhaltensbeleg TB-109 D (9/9 gegen 0/9 Ordnerpaare; das Werkzeug meldet in beiden Fällen 0 Unterschiede), **„vorläufig, von Fable nicht bestätigt“** |
| 43.4 | **43-12** TB-107 (Verweis auf 42.4, nichts doppelt), **43-13** TB-108 (67 Einträge, 108 Zitate, 20 Marken, numstat 1134/0, `register()` alt/neu, nicht gesetzte Marken), **43-14a–f** TB-109 |
| 43.5 | **43-15** Offenes, neun Zeilen |
| 43.6 | Nicht Getanes und die Liste der Marken |

**Die sechs Marken**, je neue Zeilen unter einem unveränderten Satz:

| Ort | Anker (Zeile bleibt zeichengleich) | verweist auf |
|---|---|---|
| 5.1 Nr. 8 | „in schweren Jahren nicht handeln.“ | 43-7 |
| 12 | „ab — es füllt nichts auf und überspringt nichts.“ | 43-1 |
| 15.3 (1c) | Schluss der Tatsachennotiz zu 1c | 43-7 |
| 36.5 | Schluss der Marke aus TB-108 („Text oben bleibt zeichengleich.“) | 43-1, 43-7 |
| 37.4 | Schluss der Berichtigung durch 42.3 F2 | 43-4 |
| 42.6 | letzte Tabellenzeile `(12)` | 43.1, 43.2, 43.3 |

## 3. Block C: Nachweise

| | | Beleg |
|---|---|---|
| numstat | `345	0	docs/VORREGISTRIERUNG_neuselektion.md` — zweite Spalte 0 | `c1_numstat.txt` |
| Zitate | 31 (23 Zeilen, 8 Teile), `diff` rc 0: 31, Abweichungen 0 | `d2_zitate.txt`, `zitate.json` |
| Sonde | vorher = nachher bis auf die angezeigte Lage des Listentexts (Z. 894–1007 ⇒ 901–1014; die Marke in 5.1 steht davor); 25/0/0, (ii) 0 | `0_sonde_vorher.txt`, `c_sonde_nachher.txt` |
| `register()` | `c85dd6c3…` ⇒ **`c92900a8b6792eadcc138ad7f56b8cb0e9993e4c73e4732b3dcb2f974cc52031`** (der Hash umfasst das Register; er kann deshalb nicht im Register stehen, wie in TB-108) | `c_register_nachher.txt` |
| `test_vorregistrierung` | **196/196 rc 0** (876 s) | `c_test_vorregistrierung_roh.txt` |
| Hashes | `git diff --stat 723281f..HEAD` außerhalb `docs/` leer; 1539 versionierte Dateien außerhalb `docs/` gleich; 12 `*.db` gleich | `c_hashes.txt` |

## 4. Für Fable (ohne Kontext lesbar) ⭐⭐

**Stand.** Deine Antworten 25d und 25e stehen im Register, Abschnitt **43**. Der
Grund für die Nummer: Beide überschreiben ihre Liste mit „Auf Register 41/42,
zusätzlich“, aber 41 und 42 waren schon eingetragen (TB-108). Die Nummer hat
der steuernde Chat vergeben, mit Freigabe des Betreibers. Deine Texte sind
eingesetzt, nicht abgetippt; 31 Zitate, je `diff` rc 0 gegen die Datei im Repo.
Die Herkunftsnotiz aus 41.0 gilt auch hier: Die Dateien sind aus der Ablage
abgeschrieben, der Abgleich mit deiner Ablage ist nicht byteweise gemessen.

**Was als vollzogen und was als Plan steht.**
- Vollzogen, mit Commit: 43-7 null Trades (`53896e4`, Gegenprobe `a02f035`), 43-8 Ablagen (`29640ca`), 43-9 Audit (`a02f035`), 43-10 Stummel (`8570ce8`), 43-3 `f5fdb53` steht.
- Als Plan, nicht vollzogen:
  - 43-1: `auswertung.Abbruch` ⇒ 2. Heute rc 1, zwölf Stellen.
  - 43-4: zweite Öffnung von `herkunft.py`. Als TB-111 in einem eigenen Arbeitsbaum formuliert, auf `main` nicht vollzogen.
  - die Nullzeile im Erzeuger (TB-30b).
- Die Tatsachennotiz zu Punkt 4 (43-2) steht in 43.1, nicht in Abschnitt 10; dort steht keine Marke.

**Die vorläufige Berichtigung (43.3).** Dein Stummel `selektionsmodus = lambda: False` passt nicht zu `strategy_paths` (seit TB-107 `… is not None`): Mit `False` hält es den Modus für aktiv. Gebaut und eingetragen ist `None`, gekennzeichnet als **Berichtigung des steuernden Chats, von dir nicht bestätigt**. Der Beleg ist ein Verhalten: 9 von 9 gegen 0 von 9 angelegte Ordnerpaare. Die Ausgabe des Werkzeugs taugt nicht als Beleg, sie meldet in beiden Fällen 0 Unterschiede. Dein Satz in 43-10 bleibt zeichengleich stehen.

**Zwei Tatsachen, die du beim Lesen von 43 brauchst:**
1. **Reichweite von (iv) im Audit (43-9).** Dein Satz in 25e nennt das Aufräumen (die zehn Verzeichnis-Öffnungen). Gebaut ist mehr: Auch das Lesen des Ergebnisses in der eigenen Ablage steht unter (iv). Deshalb fällt (i) außerhalb auf 11, nicht auf 21. Eingetragen ist das als Tatsachennotiz, **offen bei dir** (Ergebnis TB-109, Frage 2).
2. **`register()` nach diesem Eintrag:** `c92900a8…`. Der Wert steht nur hier, nicht im Register, weil `register()` das Register mit hasht.

**Fragen:** keine neuen; offen bleiben die drei aus dem Ergebnis TB-109 (Berichtigung `None`, Reichweite von (iv), Gegenprobe über `main()`) und 25f.

## 5. Abweichungen vom Auftrag

| | |
|---|---|
| 1 | **Arbeitsliste 43-5 und 43-12 ohne eigene Messung**, mit Verweis: Die Werte aus 25d 3 (e) und 25e 3 (a) stehen gemessen in 42.4/42.5. Nachgemessen und eingetragen ist nur, was sich seitdem bewegt hat (`register()` durch TB-108) |
| 2 | **Marke „Interpolation unter 1 %“:** wie verlangt keine in Abschnitt 10; der Eintrag steht in 43.1 (43-2) mit Verweis „Sperrlistenpunkt 4“. Eine eigene Marke zusätzlich gibt es nicht |
| 3 | **Die Marke in 36.5 steht unter der Marke aus TB-108**, nicht unmittelbar unter dem Registertext: Die TB-108-Marke nennt die offene Frage, die 43-1 beantwortet. So steht die Antwort bei der Frage |

## 6. Was NICHT geschah

- Keine `.py` geändert, nichts gerechnet, kein neues Abbild.
- Kein bestehender Registersatz geändert (numstat zweite Spalte 0); keine Zeile im Listentext von Abschnitt 10.
- Nichts aus 25f.

---

## In einfacher Sprache

Der Prüfer hat zwei weitere Antworten gegeben. Die Auswertung soll nur zwei Ausgänge kennen: gerechnet oder nicht gerechnet. Und „keine Geschäfte“ ist ein Ergebnis, kein Grund aufzuhören. Beides steht jetzt wortgleich im Regelwerk. Daneben steht, was in den Aufträgen TB-106 bis TB-109 gemessen und umgesetzt wurde, und was noch offen ist. Ein kleiner Denkfehler des Prüfers beim Aufsatz für das alte Prüfwerkzeug steht dort als vorläufige Berichtigung, bis er sie bestätigt. Nichts Altes wurde verändert, nur ergänzt.
