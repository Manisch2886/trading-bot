# REGISTER-KOPIE Abschnitt 49 (von 0–53) — Register-Z. 10975–11005 — Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff — KOPIE, nicht das Register

## 49. Fable 30a — Registerblock R53–R55 (TB-126)

Reines Eintragen von Registertext, Bauart wie 47. Quelle: `docs/projektfuehrung/FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md`, md5 `f9cdbbef543ec54ed07ee0566c336dde`, 12 925 B, am Commit `0f56aeb`, Z. 25–32. Die Datei ist eine Abschrift aus einem Text-Anhang ohne Markdown-Auszeichnung. Die drei Blöcke sind bytegleich mit Fables Ablage-Fassung (`FABLE_ANTWORT_2026-09-30a_vorlauf_aggregation_leere_menge.md`, md5 `5e5401bcc6b5551a7a61a8a1b4331fee`), geprüft vom steuernden Chat am 30.09.2026 (R53 `cbaeea5b…`, R54 `914ddd1d…`, R55 `1f3e534b…`). R54 berichtigt 2a und R48 (g) (48.16); die Marken stehen an 15.4 und unter 48.16.

### 49.1 R53 — Präzisierung zu 4a (i) (25.3, 28.6): Indikator-Vorlauf bei achsenabhängigem Rückblick

> R53 — Präzisierung zu 4a (i) (25.3, 28.6): Indikator-Vorlauf bei achsenabhängigem Rückblick. Der Indikator-Vorlauf eines Bots nach 4a (i) ist der grösste Vorlauf über alle Zellen seines Rasters: je Rückblick-Achse die oberste registrierte Stufe (Abschnitt 3) zuzüglich der festen Fenster des Bots (etwa Bollinger-Fenster, Donchian-Zusatz), gerechnet gegen den Horizontbeginn (28.6). Er wird aus registerdaten.py gerechnet, nicht als Voreinstellung geführt und nicht als Literal gesetzt; der Faltenplan trägt ihn je Bot als Feld. Der Scanbeginn einer Zelle liegt nie vor ihrem Vorlauf (TB-122 F1, Handwerk). Tatsachennotiz: Die Nachmessungen in 25.2 (rsi2_crypto, 150 Balken), 15.5 und 21.4 stammen aus der Zeit vor TB-30b Posten 3; die erste Falte ist nach dieser Präzisierung neu abzuleiten (Verfahrensmessung nach 27.2; Wirkung bekannt und kein Grund).
> Quelle des Grundes: 2.7 (ein Raster je Bot, identisch über alle Falten), 29.3 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte), 4a (i), 24.3 (Bauart). Kein Ergebnis.

> ⭐ **49.1 R53 PRÄZISIERT durch R57 (51.2)** (Fable 01a R57, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **49.1 R53 ERGÄNZT durch R59 (51.4)** (Fable 01a R59, TB-129, 02.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken: 15.5; 21.4; 25.2; 25.3, Ersatztext (Bedingung (i) steht in dessen erster Zeile); 28.6. Voraussetzung gemessen: 50.1. Zählweise: 50.5.

### 49.2 R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen)

> R54 — Berichtigung zu Registertext 2a (15.4) und zu R48 (g) (Aggregation von Tagesrenditen). „Die Falten-Rendite ist die Summe der täglichen Netto-Mark-to-Market-Renditen dieser Tage“ lies „Die Falten-Rendite ist die verkettete Rendite dieser Tage, ∏(1 + r_t) − 1 über die täglichen Netto-Mark-to-Market-Renditen“. Renditen über mehrere Tage — je Falte, über die Selektionsfalten (7 (c)), im Zufalls-Timing (8.1), für die konstante Exposure — werden überall verkettet; Drawdowns stehen auf dem verketteten Kapitalpfad (24.2). In R48 (g) lies „die Summe der täglichen Renditen (2a)“ als „die verkettete Rendite (2a)“. Der Falten-Sharpe (15.3: Mittel und Standardabweichung der täglichen Renditen) und die Faltenzuordnung (2a, 2b) sind unberührt. kennzahlen.py (gesamtrendite_pct, Zufalls-Timing, cumprod) bleibt unverändert; es rechnet, was das Register nach dieser Berichtigung sagt. Kategorie: Berichtigung (Registertext an Registertext — Kapitalpfad und Drawdown waren schon verkettet).
> Quelle des Grundes: 29.3 (Startkapital, durchgehender Pfad), 2a zweiter Satz (Kapitalstand über die Faltengrenzen), 24.2, 7 (c) (Calmar gegen Calmar auf einer Rechenart), 13 (das Urteil ist Code). Kein Ergebnis.

**Kette:** Marken: 15.4 (a); 48.16 (R48), neu in TB-126. Voraussetzung gemessen: 50.1.

### 49.3 R55 — Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz

> R55 — Ergänzung zu 7 (d) (leere Menge) und Tatsachennotiz. Gibt es keinen zulässigen Nicht-Spitzen-Punkt, ist Abbruchkriterium (d) nicht erfüllt; der Bot bleibt mit dem Plateau-Gewinner (R48 (c)), markiert als Spitze, und der Bericht führt die Zeile „Spitze ohne zulässigen Nicht-Spitzen-Punkt“ — Bericht, kein Tor. Ist keine Zelle zulässig, greift (b); der beste Nicht-Spitzen-Punkt wird dann über alle Zellen bestimmt und berichtet, wie der Plateau-Gewinner in 7. Tatsachennotiz: Der Schlüssel d_spitze_ohne_tragfaehige_alternative in auswertung.py ist ein Name, keine Regel; Umbenennung mit der nächsten planmässigen Öffnung. Eine Prüfung für die leere Menge mit Gegenprobe (40.7) wird ergänzt (Handwerk); heute prüft kein Test den Fall.
> Quelle des Grundes: Wortlaut von 7 (d) und der Präzisierung (Und-Bedingung), 6 („Ist N(x) leer, ist x keine Spitze“), 12 Lesart 4 (kein undefinierter Fall), 22.5 (ein nicht registriertes Kriterium disqualifiziert nicht), 7.1, 22.1. Kein Ergebnis.

**Kette:** Marken: 7, Tabelle, Zeile (d). Voraussetzung gemessen: 50.1.

