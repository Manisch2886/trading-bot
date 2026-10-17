# FABLE-Anfrage 17.10.a — R105 (c) Weg 1: Schliesst die Probe TB-171 die Abnahme nach R98 (d) bei elliott_wave und elliott_wave_stocks?

*Steuernder Chat, 17.10.2026, Repo-Stand `12a47f8`. Erste Anfrage im neuen Chat „Fable Trading Bots-17.10.2026 a“; Übergabe 17.10.a gilt. **Registerfrage.** Dateien in der Projektablage unter projektfuehrung/ (Projekt-Werkzeug, nicht der Mac-Ordner). Zitate per Skript aus dem Register (Commit `7aecfe6`, 12 517 Zeilen, sha256 `08b07267…` = Stand HEAD).*

## Teil 0 — Kenntnis

1. Register 0–65, eingetragen bis R105 (65.2, Z. 12464). Dein Block hier beginnt bei **R106**.
2. Seit 16.10.c: TB-170 (Register 65 = R104, R105) und TB-171 (Probe `research/tb24_haltedauern/test_elliott_verdraengung.py`, 16 von 16, rc 0) abgenommen.

## Frage 1 — R105 (c) Weg 1 bei beiden Elliott-Bots

1. R105 (c), Z. 12464: „Vor dem Tag schliesst ihn je Bot einer von zwei Wegen, mit Gegenprobe (40.7): Der Fall wird auf dem Test-Snapshot herbeigeführt (eine Welle vor dem Handelbar-Tag, deren Eintrag in traded ohne Schranke eine spätere Welle verdrängt;“ — und: „ohne Schranke fehlt der zweite Einstieg oder die Wache nach R87 (c) endet mit 2, mit Schranke erscheint er)“; ferner „64.1 bleibt zeichengleich; der Hash-Übergang ist vollzogen, die Abnahme ist Bedingung des Tags.“
2. Ergebnis TB-171 (belegt, `e_probe.txt`): In eine Kopie des Test-Snapshots von TB-169 ist je Bot ein Kursabschnitt eingesetzt: eine Welle W vor dem Handelbar-Tag. Je Bot acht Prüfungen:
   - Signalpfad (0, 0b): ohne Schranke steigt W bei k+1 vor dem Tag ein, mit Schranke dieselbe Welle (signal_time = P5, fib_score 1.0) bei k+4 ab dem Tag; Ausstieg ohne Schranke 2025-03-14 23:00 bzw. 2025-08-08.
   - Erzeuger (1): rc 0, kein Einstieg von AAA vor dem Tag, W erscheint bei k+4.
   - Gegenproben (2, 3, 6): Schranke aus ⇒ Wache R87 (c) endet an W mit 2; Schranke und Wachen aus ⇒ W vor dem Tag, Einstieg k+4 fehlt (verdrängt); Mutante (Kopie des Counters, Schranke hinter `traded.add`) ⇒ W fehlt bei k+4.
   - Kontrollen (4, 5): ohne Eingriff kein Einstieg bei k+1 und k+4; BBB/CCC mit und ohne Tag für AAA gleich.
3. Ohne Eingriff kam der Fall nicht vor: Prüfung 4 (Snapshot TB-169) und Helfer BAU171 (nicht im Ergebnis, nicht im Repo; Teilmessung nur am Signalpfad, Zufalls-Seeds): 0 Fälle bei rund 990 Trades (~530 + ~460). R105 (b): „Ein Ort, an dem verdrängt wird, und Versuche, die den Fall nicht herbeigeführt haben, heben den Fall nicht auf.“
4. Wortlaut: R105 (c) sagt „eine spätere Welle“. Am Code (beide `elliott_wave_counter.py` gleich) ist der Schlüssel von `traded` das Wellenende: Z. 192 `"end_time": times[i + 5]`, Z. 341 `traded = set()`, Z. 352–353 `if end_time in traded`, Z. 361 Schranke, Z. 363 `traded.add(end_time)`. 65.3 (c), Z. 12515: „Erschlossen (Lesung des steuernden Chats, vom Verfahrensprüfer nicht gelesen): ohne Schranke wird dieselbe Welle an ihrem späteren Einstieg verdrängt, keine andere.“ Die Probe zeigt genau diesen Fall.

**Frage:** Schliesst TB-171 R105 (c) Weg 1 für beide Bots, und trägt „eine spätere Welle“ den späteren Einstieg derselben Welle? **Neigung:** schliesst — Fall nach R90 (g) am Listen-Erzeuger herbeigeführt, Gegenprobe über die Wache nach R87 (c), Lage der Schranke durch die Mutante gezeigt (R105 (b): „Dass die Schranke vor der Verdrängung steht, ist die Wirkung, die die Abnahme zeigt, nicht das Entfallen des Falls.“). **Gegen die Neigung:** (i) R90 (g), Z. 11997: „Der Test-Snapshot führt ein Symbol, dessen Reihe vor seinem Handelbar-Tag ein Einstiegssignal trägt, dessen Position über den Handelbar-Tag hinaus offen wäre, und danach ein zweites Einstiegssignal, das ohne die Schranke verdrängt würde.“ — herbeigeführt ist der Fall an einer Kopie mit eingesetztem Abschnitt, nicht am Test-Snapshot selbst; (ii) Prüfung 5 vergleicht mit und ohne Tag, nicht, wie R90 (g) sagt, „an einem Symbol, dessen Einstiegssignale alle am Handelbar-Tag oder später liegen, dass die Ausgaben mit und ohne Schranke gleich sind.“ (das zeigt für beide Bots TB-169, `e_abnahme.txt` Prüfung 3b); (iii) Prüfung 6 zeigt nur „kein k+4, nichts vor dem Tag“, nicht, dass W an der Mutante verdrängt wird (Gegenleser GEGEN171B, C-a).

## Zur Kenntnis

1. Prüfungen 0b/3 messen „Ausstieg am Tag oder später“ (`exit_time >= T`, T = Tag 00:00); R90 (g) sagt „über den Handelbar-Tag hinaus offen“. Die Messwerte (2025-03-14 23:00, 2025-08-08) erfüllen beides.
2. R105 (d), Z. 12464: „(d) Für t3_supertrend ist nichts entschieden; derselbe Massstab gilt.“ Massstab R105 (b): „Die Tatsachennotiz nach R90 (g) sagt mit Fundstelle, warum ein Einstieg vor dem Handelbar-Tag keinen späteren verdrängen kann.“ TB-169 3a (`e_abnahme.txt` Z. 84): Einstieg nur am Kreuzen nach oben (`backtest_trend.py` Z. 111–112), Ende am Kreuzen nach unten, Trend-Flip (Z. 123) oder Stop; „14 Versuche, kein verdraengter Einstieg“. Am HEAD: Einstieg nur bei `position is None` (Z. 111); das Kreuzen nach unten steht in Z. 124 und greift nur mit `use_t3_exit` (Vorgabe True, Z. 70). Erschlossen (Helfer): mit `use_t3_exit` setzt ein zweites Kreuzen nach oben in offener Position ein Kreuzen nach unten voraus, das sie schliesst; Grenzfall Gleichstand (Z. 112 `<=`, Z. 124 `<`). **Frage:** Was ist vor dem Tag für t3_supertrend nötig: Tatsachennotiz nach R105 (b) mit diesen Fundstellen, oder Weg 1?

## Lesen und Antwort

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_51 (R56), _57 (R90), _61 (R98), _64, _65; ERGEBNIS_TB-171_r105c_elliott_fall.md; die Übergabe 17.10.a. Fehlt eine Kopie, melde das. Nicht lesen: BACKLOG*, ergebnisse/, docs/belege/ (Brauchst du etwas, nenne es). Antwort höchstens 10 KB als projektfuehrung/FABLE_ANTWORT_2026-10-17a_<stichwort>.md: Kurz (je Frage „einverstanden“ oder „anders, weil …“), Registerblock zeichengleich kopierbar ab R106, Leseprotokoll nach R56 (b), Ampel.
