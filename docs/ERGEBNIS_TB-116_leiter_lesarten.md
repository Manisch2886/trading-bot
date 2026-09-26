# TB-116: Ergebnis. Prüfung vor dem Tag zu 16.4 — der Registertext ergibt **nicht** für jede der 3⁹ = 19 683 Stufentabellen genau einen Multiplikatorvektor: fünf Lesart-Stellen, alle fünf echt (jede ändert den Vektor in 322 bis 19 682 Tabellen); unter den 144 Kombinationen beantworten 72 jede Tabelle, 24 davon mit Buchsumme 1, und auch diese 24 ergeben nur in 17 Tabellen denselben Vektor; die Lesart, die (m) und (h) wörtlich zusammensetzt, lässt in **jeder** Tabelle Buch unverteilt (bei festen vier Zellen genau die Hälfte); der grösste Multiplikator liegt je nach Lesart zwischen 1,8 und 9

**Sitzungstitel:** `TB-116` · **Stand:** 26.09.2026, ca. 21:40 · **Auftrag:**
`docs/auftraege/MAC_TB-116_leiter_lesarten_pruefung.md` · **Belege:** `docs/belege/TB-116/`
**Eingang:** `10e9697` (Abgabe TB-115). Commits: `50afdbf` (Schritt 0), `e414f79` (Werkzeug und Test), `ce982c9`
(Nachtrag Werkzeug, siehe 2.3), der Abgabe-Commit (Belege, Journal DO, dieses Dokument). Nach jedem Commit gepusht.
**Grundlage:** Register 16.4 (Registertext 6, (a)–(m)), Absatz „Prüfung vor dem Tag“; 16.11 Zeile 3; Fable 26a 2 (a);
45.8 R8 (e). Freigabe des Betreibers 26.09.2026, ca. 20:50 (Auswahlkarte, wörtlich im Auftrag).
**Umgebung:** Mac, `trading-env/bin/python3` (3.9.6).

⛔ **Sichtschutz 27.1 eingehalten:** Die Stufentabellen sind **aufgezählt**, nicht aus einem Lauf. Das Werkzeug liest
keine Datei des Selektionsraums. Die „statische Benchmark-Position in Höhe des mittleren Exposures“ wird nur als
**Budgetanteil** geführt; die Exposure-Höhe ist eine Ergebnisgrösse und ist **nicht** gerechnet (Lesart L0.1). Kein
Abbruchkriterium des Auftrags ist eingetreten.

⭐ **Kurz:**

| | Ergebnis |
|---|---|
| **0** | Schritt 0 committet (`50afdbf`, md5 der drei Betreiberdateien ✔, numstat zweite Spalte 0 bei beiden Anhängen), keine weiteren uncommitteten Dateien. 0b vorher = nachher: `register()` `5acb4c19…`, Sonde gegen `5e5ad109…` 34/0/0 (rc 2 wie immer), Arbeitsbaum ausserhalb `docs/` und `research/leiter_pruefung/` leer |
| **A** | 18 Suchmuster (8 aus dem Auftrag, 10 ergänzt), Treffer in `a_fundstellen.txt`. **Keine spätere Stelle ändert 16.4 (g)–(m)**; 17.7, 22.4, 26.7, 16.10 und 45.8 R8 (e) ergänzen, verweisen oder wirken nur auf die Stufe. 20 Zitate in `a_regeln.md`, `diff` rc 0 für alle 20, Mutationsprobe rc 1 |
| **B** | `research/leiter_pruefung/leiter_lesarten.py` (Prüfwerkzeug, exakte Brüche) und `test_leiter_lesarten.py`: 17 Hand-Proben je mit Mutationsgegenprobe, **34/34** |
| ⭐⭐ **C** | 19 683 Tabellen, alle verschieden, × 144 Lesart-Kombinationen. **Fünf Lesart-Stellen, jede echt.** 72 Kombinationen beantworten jede Tabelle, 72 haben Lücken (L2c: 8 606 bzw. 8 866 Tabellen ohne Antwort, L4d: 496). 24 beantworten jede Tabelle mit Buchsumme 1 — sie fallen auf **16** verschiedene Regeln zusammen und ergeben nur in **17** Tabellen denselben Vektor. Über alle 144 Kombinationen: **1** Tabelle mit genau einem Vektor (alle Schatten), bis zu 24 verschiedene Vektoren je Tabelle |
| ⚠️ **C** | **L1a** (Formel (m) mit (h) „teilen das Buch“ wörtlich): Buchsumme ≠ 1 in **allen** 19 683 Tabellen (mit L2b genau 1/2, mit L2a 0 bis 0,8) |
| ⚠️ **C** | max. `m_b`: **9** (ein Bot trägt das ganze Buch; L3b oder L1c mit L2a), **7,2** (L1b/L2a/L3a: ein Bot trägt die 80 % Aktien), **3,6** unter L1b/L2b/L3a — dort hat `volatility_breakout` schon in der Tabelle „alle Grundbudget“ das **3,6-Fache** seiner heutigen Grösse (seine Zelle hat nur ihn) |

---

## 0. Schritt 0 und Ausgangswerte

- **0a:** Die fünf erwarteten Dateien lagen uncommittet vor, sonst nichts. md5: Fable-Anfrage 27a
  `93a677c1…` ✔, Übergabe `a1fb9cb2…` ✔, Aufgabenliste `405c77c4…` ✔. `git diff --numstat`: Übergabe 29/0,
  Aufgabenliste 13/0 (zweite Spalte 0), Zeiger 1/1. Commit `50afdbf`, gepusht.
- **0b** (`0b_ausgang.sh` → `0b_ausgang.txt`, Bauart TB-115): HEAD `50afdbf`, letzter Nicht-docs-Commit `e07fefd`;
  `herkunft.py` `ed521ac1…`, Abbild `5e5ad109…`, `sperrlistensonde.py` `f88e54ee…`; `register()` `5acb4c19…`,
  fehlend `[]`, 20 Teile; Sonde rc 2, Pfad-Bestandteile 34/0/0, Listentext Z. 905–1018 wie bei Erzeugung;
  Arbeitsbaum ausserhalb `docs/` und `research/leiter_pruefung/` leer.

## 1. Block A — der Registertext, den das Werkzeug benutzt

**Suche** (`a_fundstellen.sh` → `a_fundstellen.txt`, `grep -n -F` über das ganze Register, 10 034 Zeilen): die acht
Muster des Auftrags (`16.4` 4, `Registertext 6` 7, `Zellenbudget` 5, `Stufenfaktor` 1, `m_b` 4, `Klassenschlüssel` 1,
`80/20` 2, `Leiter` 9 Zeilen) und zehn ergänzte (`Benchmark-Position`, `mittleren Exposure`, `Budgetanteil`,
`Budgetstufe`, `Grundbudget`, `Zellenanteil`, `Stufentabelle`, `3⁹`, `Netting`, `Crash-Knopf`).

**Befund:** Keine Stelle nach 16.4 **ändert** Registertext 6. Es **ergänzen**: 22.4 (Notbremse auf In-Sample-Befund,
kein Aufstieg dadurch), 17.7 („unbestimmt“ → eingestuft; Aufstieg auf Bestätigt erst ab n ≥ 20). Es **verweisen**:
26.7 (Kette (b) → Schatten), 45.8 R8 (e) (Zellenbudget steht in 16.4, offen ist der Vollzug). 16.11 Zeilen 3 und 9
**benennen die Lücke im Code**. 16.5, 16.10 (e), 17.7 wirken auf die **Stufe**, die für das Werkzeug Eingabe ist.
Ausserhalb von 16.4 trägt die Rechnung von der Stufe zum Geld nur 7.1 (*„nicht in Kasse, nicht zu den
Überlebenden“*) und 15.6 (c) (unterbestimmter Bot: Budget hält Benchmark).

**Regeln** (`a_regeln.md`): 20 Zitate (Z1–Z20) zeichengleich mit Zeilenangabe, eingesetzt von `a_einsetzen.py`,
geprüft von `a_zitate.py` (liest Kopfzeile und Block, holt die Registerzeilen mit `sed -n`, vergleicht mit `diff`):
**20/20 rc 0** (`a_zitate.txt`). Mutationsprobe: ein Wort in Z9 geändert → Z9 `diff` rc 1, Gesamt rc 1
(`a_zitate_mutation.txt`). Abschnitt 2 dort ordnet jede Regel ihrer Stelle im Code zu, Abschnitt 3 benennt jede
Lesart.

**Lesarten:** neun feste (L0.1–L0.9, nicht variiert, je mit Grund, warum sie nicht im Zitat steht) und fünf
variierte Stellen:

| Stelle | Optionen | woher |
|---|---|---|
| **L1** Zellenanteil × Klassenschlüssel | L1a Buch über alle, Schlüssel multipliziert · L1b Buch erst 80/20, dann je Anlage · L1c über alle, mit Schlüssel gewichtet und normiert | Auftrag Stelle 1 (L1a/L1b); L1c ergänzt |
| **L2** Bezugsmenge der Zellen (Nenner in (h)) | L2a jetzt aktive Zellen · L2b alle vier Zellen aus (g) · L2c seit der letzten Zulassung aktive Zellen (Vorgeschichte) | ergänzt — beim Lesen von (h) gegen (j)/(k) gefunden |
| **L3** Anlage ohne aktive Zelle | L3a Benchmark der eigenen Anlage · L3b zur anderen Anlage | Auftrag Stelle 2 |
| **L4** Schatten in aktiver Zelle | L4a (i)/(j) immer · L4b (b) immer, Anteil wie Grundbudget · L4c (b) immer, Anteil = heutige 1/9 · L4d (b) nur direkt nach dem Lauf | Auftrag Stelle 3 (L4a/L4b/L4d); L4c ergänzt |
| **L5** Faktor „Bestätigt“ vor Netting | L5a 2 · L5b 1, bis Netting existiert | ergänzt — (a) „Rang-5-Gewichtung, sobald Netting existiert“ gegen (i) |

## 2. Block B — das Prüfwerkzeug

### 2.1 `leiter_lesarten.py`

- **Eingabe:** eine Stufentabelle (je Bot `schatten`/`grund`/`bestaetigt`); die Zellenzuordnung aus 16.4 (g) als
  Literal `ZELLEN` mit Fundstelle Z. 1968–1978; Faktoren (i), Schlüssel (l), Nenner (m) je als Literal mit Fundstelle.
- **Aufzählung:** `alle_tabellen()` = `itertools.product` über 9 Bots, 19 683 Stück.
- **Je Tabelle und Lesart** (`rechne`): Vektor `m_b` (9 Brüche), Benchmark-Anteil je Anlage, Buchsumme
  Σ `m_b` × (1/9) + Benchmark-Anteile, Rest = 1 − Buchsumme — oder **„keine Antwort“** mit der Stelle, deren Satz
  fehlt (`L2c`, `L4d`, `L2c-benchmark`). Das Werkzeug **fragt nie**; ein Fall ohne Antwort ist genau der Fall, den 16.4
  als „unvollständig“ benennt.
- **L2c** rechnet jede mögliche Vorgeschichte (jede Menge R mit aktiv ⊆ R ⊆ alle vier) und antwortet nur, wenn alle
  denselben Vektor geben. **L4d** rechnet L4a und L4b und antwortet nur, wenn ein Bestätigt in der Tabelle steht
  (dann ist mindestens eine Quartalsprüfung vorbei, (c)/(e)) oder beide gleich sind.
- **Pruefung** (`pruefung`): alle Tabellen × alle 144 Kombinationen; je Kombination die Kennzahlen aus Block C; je
  Stelle die Tabellen, in denen die Optionen bei festen übrigen Stellen verschiedene Vektoren geben, nach
  Unterschiedsklasse (Optionspaar × aktive Zellen je Anlage × Schatten in aktiver Zelle × Bestätigt vorhanden) mit drei
  Beispielen.
- Liegt in `research/leiter_pruefung/`, **nicht** im Laufbereich, auf keiner Liste, von keinem Lauf geladen; schreibt
  nur mit `--aus` seine zwei Ergebnisdateien.

### 2.2 `test_leiter_lesarten.py` — 34/34 (`b_test.txt`)

17 Proben, jede mit vorher von Hand gerechnetem Soll (Rechnung im Kommentar) und jede mit einer
**Mutationsgegenprobe** (Quelltext an genau einer Stelle geändert, als eigenes Modul geladen, dieselbe Probe muss
scheitern — alle 17 scheitern):

| Probe | Fall | Soll |
|---|---|---|
| P1 | alle Grundbudget, L1a (L2a/b/c) | `m` = 9/5, 3/5 ×3, 9/40 ×2, 3/20 ×3; Buchsumme 1/2 |
| P2 | alle Grundbudget, L1b und L1c | `m` = 18/5, 6/5 ×3, 9/20 ×2, 3/10 ×3; Buchsumme 1 |
| P3 | alle Schatten | `m` = 0; Benchmark je Lesart (4/5 + 1/5; L1a/L2a Summe 0; L1a/L2c nur Benchmark mehrdeutig) |
| P4, P5 | nur Krypto aktiv | L3a: `m`(FK) 9/20, Aktien-Benchmark 4/5; L3b: 9/4; L2c mit L1b Antwort, mit L1a keine |
| P6a–d | Zelle mit Schatten + Bestätigt | L4a 9/10 · L4b 3/5 und Benchmark 1/30 · L4c Buchsumme 10/9 · L4d = L4a |
| P7 | Zelle mit Schatten + Grundbudget | L4d ohne Antwort |
| P8 | L5b | Bestätigt zählt 1 |
| P9 | L1c ≠ L1b | `m`(VB) 6 gegen 36/5 |
| P10 | Aufzählung | genau 19 683, alle verschieden |
| P11 | Schreibweise | hin und zurück für alle Tabellen |
| P12 | Zellenzuordnung | `ZELLEN` = Tabelle in Register Z. 1972–1975 |
| P13, P14 | Prüfung und Ausgabe | Unterschiedsklassen, Text- und JSON-Zeile |

### 2.3 Ein Fehler im Werkzeug, behoben

Der erste Volllauf brach nach 311 s in der **Textausgabe** ab (`als_text` zählte mit `len()` auf einer Zahl, die
`pruefung` schon verdichtet hatte; `c_lauf_1_abgebrochen.txt`). Die Rechnung war davon nicht berührt, geschrieben
wurde nichts. Behoben in `ce982c9`, dazu Probe P14 für die Ausgabe (vorher ungeprüft). Zweiter Volllauf 323 s, rc 0
(`c_lauf.txt`).

## 3. Block C — die Prüfung

Belege: `c_pruefung.txt` (933 Zeilen) und `c_pruefung.json`; Zusätze `c_paare.py` → `c_paare.json` (je Optionspaar),
`c_vollstaendig.py` → `.txt`, `c_beispiele.py` → `.txt`.

### 3.1 Die Kennzahlen je Lesart-Kombination (Auszug; alle 144 in `c_pruefung.txt`)

| Kombinationen | Tabellen mit eindeutigem Vektor | ohne Antwort | Buchsumme ≠ 1 | Spanne | max. `m_b` |
|---|---:|---:|---:|---|---|
| L1a · L2a · (L4a/b) | 19 683 | 0 | 19 683 (L3a) / 19 361 (L3b) | 0 … 0,8 (L3a), 0 … 1 (L3b) | 7,2 (L3a) · 9 (L3b) |
| L1a · L2b · (L4a/b) | 19 683 | 0 | **19 683** | **genau 1/2** | 1,8 (L3a) · 2,25 (L3b) |
| L1a · L2c | 10 816 | 8 867 | alle beantworteten | 1/2 | 1,8 |
| L1b · L2a · (L4a/b) | 19 683 | 0 | 0 | 1 | 7,2 (L3a) · 9 (L3b) |
| L1b · L2b · (L4a/b) | 19 683 | 0 | 0 | 1 | 3,6 (L3a) · 4,5 (L3b) |
| L1b · L2c · (L4a/b) | 11 077 | 8 606 | 0 | 1 | 3,6 (L3a) · 4,5 (L3b) |
| L1c · L2a · (L4a/b) | 19 683 | 0 | 1 (alle Schatten) | 0 … 1 | 9 |
| L1c · L2b · (L4a/b) | 19 683 | 0 | 0 | 1 | wie L1b · L2b |
| jede · L4c | wie L4a | | +18 468 (Schatten in aktiver Zelle) | bis **14/9 = 1,556** | wie L4a |
| jede · L4d | −496 gegenüber L4a | +496 | wie L4a | | wie L4a |
| L5a gegen L5b | | | | | in keiner Zeile verschieden |

- **„ohne Antwort“ nach Klasse**, je ein Beispiel mit dem fehlenden Satz (`c_pruefung.txt`, Abschnitt „Ohne Antwort“):
  - **L2c** (8 606 bzw. 8 866 Tabellen), Beispiel `FA:S UA:SSS FK:SS UK:SSG` — *fehlt: welche Zellen seit der letzten
    Zulassung aktiv waren; (j) verbietet, dass der Nenner beim Inaktivwerden fällt, (h) zählt nur die aktiven Zellen —
    die Tabelle trägt die Vorgeschichte nicht.*
  - **L4d** (496 Tabellen: kein Bestätigt, aber ein Schatten in einer aktiven Zelle), Beispiel
    `FA:S UA:SSS FK:SS UK:SSG` — *fehlt: ob die Tabelle der Stand direkt nach dem Selektionslauf ist; die Tabelle trägt
    Zeitpunkt und Herkunft der Stufe nicht (Lauf (b), Abstieg (d), Notbremse (e)/22.4, 16.5).*
  - **L2c-benchmark** (1 Tabelle, alle Schatten, nur unter L1a/L1c): `m` eindeutig (0), Benchmark-Anteile nicht.
- **Buchsumme ≠ 1 — nur benannt, ob Absicht oder Lücke entscheidet Fable:** L1a in **jeder** Tabelle (mit L2b genau
  1/2, mit L2a 0 bis 0,8); L4c über 1 in jeder Tabelle mit Schatten in aktiver Zelle (bis 14/9); L1c/L2a in der einen
  Tabelle „alle Schatten“ (0, weil keine Zelle in R). **Alle übrigen Kombinationen: genau 1 in jeder beantworteten
  Tabelle.** ⚠️ Die Buchsumme ist eine **Budget**summe (L0.1); über die Exposure sagt sie nichts.
- **max. `m_b`** (je Kombination Wert, Bot, Tabelle in `c_pruefung.txt`): **9** (ein einzelner aktiver Bot trägt das
  ganze Buch: L3b mit L2a, oder L1c mit L2a, z. B. `elliott_wave` in `FA:S UA:SSS FK:SS UK:SSG`) · **7,2** (L1b/L2a/L3a:
  ein Bot trägt die 80 % Aktien) · **4,5** (L2b/L3b) · **3,6** (L1b/L2b/L3a) · **1,8** (L1a/L2b). ⭐ **Tatsache für
  Fable:** Unter L1b/L2b/L3a hat `volatility_breakout` schon in der Tabelle „alle Grundbudget“ **`m_b` = 18/5 = 3,6**,
  weil er allein in seiner Zelle steht; die Krypto-Bots fallen dort auf 0,45 bzw. 0,3 (`c_beispiele.txt`).

### 3.2 Je Stelle: in wie vielen Tabellen die Optionen verschiedene Vektoren ergeben

(übrige Stellen fest, mindestens eine Belegung; `c_paare.json`; Unterschiedsklassen mit je drei Beispielen in
`c_pruefung.txt`)

| Optionspaar | Tabellen mit verschiedenem `m` | wann |
|---|---:|---|
| L1a ≠ L1b | **19 682** | jede Tabelle ausser „alle Schatten“ |
| L1a ≠ L1c | 19 682 | ebenso |
| L1b ≠ L1c | 7 914 | nur unter L2a; unter L2b sind L1b und L1c **in allen Tabellen gleich** (0 Abweichungen, `c_vollstaendig.txt`) |
| L2a ≠ L2b | **8 866** | mindestens eine Zelle aktiv und mindestens eine inaktiv (19 683 − 10 816 ganz aktive − 1 ganz inaktive) |
| L3a ≠ L3b | **322** | genau eine Anlage ohne aktive Zelle (80 + 242 Tabellen) |
| L4a ≠ L4b | **18 468** | jede Tabelle mit einem Schatten in einer aktiven Zelle |
| L4a ≠ L4c | 0 in `m` | nur Benchmark verschieden (18 468 Tabellen) — L4c ändert nie einen Multiplikator, nur die Buchsumme |
| L4a ≠ L4d | 0 | wo L4d antwortet, ist es L4a |
| L5a ≠ L5b | **18 468** | ein Bestätigt mit einem anderen Bot in derselben aktiven Zelle |

*18 468 zweimal ist kein Zufall der Rechnung, sondern der Zählung:* Die Tabellen ohne Unterschied sind bei L4 die,
in denen jede Zelle ganz Schatten oder ganz ohne Schatten ist, bei L5 die, in denen jede Zelle ganz Bestätigt oder
ohne Bestätigt ist — je 3 × 9 × 5 × 9 = 1 215; 19 683 − 1 215 = 18 468.

### 3.3 Über alle Kombinationen

- Verschiedene Vektoren je Tabelle über alle 144 Kombinationen: **1** Vektor in **1** Tabelle (alle Schatten), sonst
  2 bis 24; am häufigsten 8 (8 050 Tabellen) und 20 (5 040). Keine Tabelle bleibt unter allen Kombinationen ohne
  Antwort.
- **Kombinationen, die jede Tabelle beantworten:** 72 von 144 (alle ohne L2c und ohne L4d).
- **Davon mit Buchsumme 1 in jeder Tabelle: 24** — L1b mit L2a oder L2b, L1c mit L2b, je × L3a/b × L4a/b × L5a/b
  (`c_vollstaendig.txt`). Weil L1c/L2b ≡ L1b/L2b, sind das **16** verschiedene Regeln. Sie ergeben in **17**
  Tabellen denselben Vektor (alle Schatten und die 16 Tabellen, in denen jede Zelle ganz Grundbudget oder ganz
  Bestätigt ist) und sonst 2 bis 16 verschiedene.

**Folge, nur benannt:** Selbst wer L1a (Buch halb unverteilt), L4c (Buchsumme über 1) und die zwei Lücken-Lesarten
(L2c, L4d) ausschliesst, hat noch **vier** offene Entscheidungen — L2 (a/b), L3, L4 (a/b), L5 —, und jede ändert in
einem Teil der Tabellen den Vektor. Ein Leiter-Skript, das heute gebaut würde, müsste an diesen vier Stellen
wählen — nach 16.4 ist jede solche Wahl ein Fall, in dem das Register unvollständig ist. Sind sie entschieden, besteht
jede der 16 Regeln die Prüfung (eindeutig in 19 683 von 19 683 Tabellen, Buchsumme 1).

## 4. Abschluss — 0b wiederholt

`0b_nachher.txt`: gleich `0b_ausgang.txt` bis auf HEAD und die Zeile „letzter Nicht-docs-Commit“ (jetzt `ce982c9`,
dieser Sitzung, nur `research/leiter_pruefung/`). `register()` `5acb4c19…`, fehlend `[]`, 20 Teile; Sonde rc 2,
34/0/0; Arbeitsbaum ausserhalb `docs/` und `research/leiter_pruefung/` leer. `diff` der beiden Dateien ohne diese
Zeilen: rc 0.

## 5. Für Fable

⭐ **Die Tabelle „Lesart-Stelle × Folge“.** Die Spalte „Satz, der sie schliessen würde“ ist **VORSCHLAG** der Sitzung,
kein Registertext; sie nennt je Stelle **eine** Richtung, damit die Folge messbar ist — die andere Richtung wäre
ebenso ein Satz. Die Sitzung hat keine Lesart festgelegt.

| Stelle | Folge (gemessen) | ⚠️ VORSCHLAG — Satz, der die Stelle schliessen würde |
|---|---|---|
| **L1** Zellenanteil × Schlüssel | L1a gegen L1b/L1c: anderer Vektor in 19 682 Tabellen; unter L1a Buchsumme ≠ 1 in **allen** 19 683 (mit festen vier Zellen genau die Hälfte des Buchs nirgends) | *VORSCHLAG:* „Das Buch wird zuerst nach dem Schlüssel (l) auf die Anlagen geteilt; der Zellenanteil in (m) ist der Anteil der Zelle am Budget **ihrer Anlage**, zu gleichen Teilen unter den Zellen dieser Anlage.“ (schliesst zu L1b) |
| **L2** Nenner in (h) | L2a gegen L2b: anderer Vektor in 8 866 Tabellen; L2c (Vorgeschichte, strenges (j)) ohne Antwort in 8 606 bzw. 8 866 Tabellen. Beispiel `FA:G UA:SSS FK:GG UK:GGG`: L2a gibt `volatility_breakout` 7,2 (die 40 % der inaktiven Umkehr-Zelle wandern zu ihm), L2b 3,6 und 40 % in die Aktien-Benchmark | *VORSCHLAG:* „Die Zahl der Zellen in (h) ist die Zahl der Zeilen in (g), nicht die Zahl der aktiven Zellen; eine inaktive Zelle behält ihren Anteil und hält ihn nach (j) in der Benchmark ihrer Anlage. Nur eine neue Zeile in (g) ändert die Zahl ((k)).“ (schliesst zu L2b; macht L1b und L1c gleich) |
| **L3** Anlage ohne aktive Zelle | 322 Tabellen; unter L3b trägt eine Anlage das ganze Buch (max. `m_b` 4,5 bzw. 9). Beispiel `FA:S UA:SSS FK:GG UK:GGG`: L3a Krypto-Bots 0,45/0,3 und 80 % Aktien-Benchmark; L3b 2,25/1,5 | *VORSCHLAG:* „Der Schlüssel (l) gilt auch, wenn eine Anlage keine aktive Zelle hat: Ihr Anteil hält die statische Benchmark-Position dieser Anlage.“ (schliesst zu L3a; folgt (j) „nicht an andere Zellen“ auf Anlage-Ebene) |
| **L4** Schatten in aktiver Zelle | L4a gegen L4b: anderer Vektor in 18 468 Tabellen; L4c ändert kein `m_b`, hebt aber die Buchsumme bis 14/9; L4d ohne Antwort in 496 Tabellen | *VORSCHLAG:* „Der Budgetanteil in (b) ist der, den (i) gibt: Ein Schatten hat Faktor 0. In einer aktiven Zelle teilen die übrigen deren Budget ((j)); die statische Benchmark-Position aus (b) entsteht nur, wo eine Zelle oder Anlage ganz ohne aktive Bots ist.“ (schliesst zu L4a; schliesst auch L0.9) |
| **L5** Faktor Bestätigt vor Netting | 18 468 Tabellen. Beispiel `FA:G UA:GGB FK:GG UK:GGG`: L5a `elliott_wave_stocks` 1,8 und die zwei anderen 0,9; L5b alle drei 1,2 | *VORSCHLAG:* „Der Faktor 2 in (i) gilt ab der ersten Quartalsprüfung; ‚sobald Netting existiert‘ in (a) betrifft die Rang-5-Gewichtung, nicht den Stufenfaktor.“ (schliesst zu L5a) |

**Fragen, die die Sitzung nicht beantworten kann:**

1. **Die vier Entscheidungen L2, L3, L4, L5** (L1 folgt aus L2b, wenn L1a nicht gewollt ist). Gilt eine andere
   Richtung als die vorgeschlagene, bleibt das Werkzeug gleich — es zählt dann dieselben Tabellen mit der anderen
   Option.
2. **L1a ist die wörtlichste Zusammensetzung von (h) und (m)** und lässt Buch unverteilt. Ist (m) so zu lesen, dass
   „Zellenanteil“ schon der Anteil innerhalb der Anlage ist (dann ist L1a keine Lesart), oder ist die Hälfte bewusst
   Kasse? 7.1 sagt „nicht in Kasse“.
3. **L0.1 — die Höhe der Benchmark-Position.** (b), 7.1 und 15.6 (c) sagen „in Höhe seines mittleren Exposures“. Ist
   ein Budgetanteil, der die Benchmark nur zu einem Bruchteil hält, dann zum Rest Kasse? Das Werkzeug führt nur den
   Budgetanteil; die Exposure-Höhe ist eine Ergebnisgrösse und ist nicht gerechnet.
4. **(k) und die Zulassung.** Ist eine neue Zelle „aktiv“ nur durch eine neue Zeile in (g) (neuer Bot, neue Quelle)
   oder auch, wenn ein Bot einer bestehenden Zelle nach einem neuen registrierten Lauf wieder Grundbudget hat? Das
   entscheidet, ob L2b genügt oder die Zahl der Zellen doch eine Vorgeschichte hat.
5. **Tatsache, nicht Frage:** Unter den vorgeschlagenen Sätzen trägt `volatility_breakout` in der Tabelle „alle
   Grundbudget“ das **3,6-Fache** seiner heutigen Grösse, die drei Umkehr-Aktien-Bots je 1,2, die Krypto-Bots 0,45
   bzw. 0,3. Das folgt aus Gleichteilung der Zellen (h) bei ungleicher Besetzung (g), nicht aus einer Lesart.

## 6. In einfacher Sprache

Das Regelwerk sagt, wie das Geld auf die neun Bots verteilt wird, je nachdem, auf welcher Stufe jeder Bot steht. Die
Sitzung hat alle 19 683 möglichen Kombinationen durchgerechnet und geprüft, ob der Text jedes Mal genau eine
Verteilung ergibt.

**Er tut es nicht.** An fünf Stellen lässt der Text zwei oder mehr Deutungen zu, und jede davon verändert die
Verteilung in vielen Fällen, nicht nur in Randfällen. Zwei Beispiele: Nimmt man die Formel ganz wörtlich, wird immer
nur ein Teil des Geldes verteilt, bei allen vier Gruppen im Spiel genau die Hälfte. Und wenn eine Gruppe von Bots
ganz ausfällt, sagt ein Satz „das Geld geht in eine feste Marktposition“, ein anderer lässt es den übrigen Gruppen
zufallen.

Die gute Nachricht: Mit vier klaren Sätzen im Regelwerk ist die Verteilung in allen 19 683 Fällen eindeutig, und
das Geld geht immer genau auf. Die Sitzung hat für jede Stelle einen solchen Satz **vorgeschlagen**, aber nicht
entschieden. Das tut Fable. Erst danach wird das eigentliche Programm gebaut.

Eine Zahl sollte man kennen: Weil `volatility_breakout` als einziger Bot in seiner Gruppe steht, bekäme er schon
im Normalfall gut das Dreieinhalbfache seiner heutigen Grösse.

*Geschrieben 26.09.2026 von der Mac-Sitzung TB-116.*
