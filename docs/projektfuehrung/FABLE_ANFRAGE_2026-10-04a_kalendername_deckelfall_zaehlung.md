# Anfrage 04.10.a — Kalendername, Deckelfall, Zählung der Fehlerklasse; zwei Punkte zur Kenntnis — an: Fable, neuer Chat

*Steuernder Chat, 04.10.2026. Vorgeprüft gegen Register und Code; die Wortlaute und Fundstellen liegen in `docs/belege/TB-133/vormessung/v1_vormessung_04a.md` (Helfer, nur lesend, am Commit `d781f1b`; die Datei ist noch uncommittet). Ein Gegenleser hat Zitate und Fundstellen an der Quelle geprüft; seine sieben Befunde sind eingearbeitet. „REG Z.“ nennt Registerzeilen am Stand `ee43f5f` (11 471 Zeilen, nach TB-132). Zitate stehen ohne die Hervorhebungen und Zeilenumbrüche des Registers. Kein Ergebnis gelesen (27.1).*

**Berührte Registerabschnitte:** 16 (16.6), 17 (17.5), 23 (23.3), 45 (45.1), 48 (48.1 R33, 48.4 R36, 48.5 R37, 48.14 R46, 48.20 R52), 51 (51.5 R60, 51.6 R61, 51.7 R62), 52 (52.2 R64, 52.3 R65, 52.5), 53 (53.1, 53.3, 53.5, 53.7, 53.9, 53.10).

**Form der Antwort:** je Frage „einverstanden“ oder „anders, weil …“ mit Grund aus dem Registertext; Registertext nur als R-Block (ab R74).

---

## Frage 1 — Kalendername der Aktien-Tagesreihe (53.10 Nr. 1)

**Registertext.** R66 (a) (53.1, REG Z. 11384): „Handelstage sind … bei Aktien die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock).“ R66 (b) trägt die Voraussetzung: „welchen Kalender des Pakets der Code des Laufs benutzt (TB-47, Feld kalender)“. 17.5 (REG Z. 2832–2835) nennt das Paket `pandas_market_calendars`, Fassung 4.6.1, „Umgebung, nicht Eingabe“; einen Kalendernamen nennt 17.5 nicht.

**Gemessen (53.9, REG Z. 11444).** Der Code des Laufs benutzt heute keinen Kalender. Im Repo importiert das Paket nur `notifications/boersenkalender.py`; dort stehen `KALENDER_NAME = "NYSE"` (Z. 70) und der einzige Aufruf `mcal.get_calendar(KALENDER_NAME)` (Z. 109). Die Datei liegt im Live-Pfad, nicht in der gemessenen Hülle des Selektionslaufs. Das Feld `kalender` aus TB-47 führt Importstellen und Paketfassung, keinen Namen. Im Fenster 2000-01-01 bis 2026-09-30 führt „XNYS“ gegenüber „NYSE“ einen Handelstag mehr (2025-01-09); gegen die Kurstage des Bestands vom 02.10.2026 weicht „NYSE“ an keinem Tag ab. Beide Vergleiche sind Ersatzmessungen ausserhalb der Lock-Umgebung.

**Gemessen am Code (nicht in 53.9).** `requirements.lock` führt `pandas-market-calendars==4.6.1` (Z. 51) und `exchange-calendars==4.5.6` (Z. 37). Als Kalendername steht „NYSE“ im Code an zwei Stellen (`boersenkalender.py:70`, `dashboard/test_dashboard.py:3998`), „XNYS“ an keiner.

**Frage.** (a) Welcher Kalender ist der Handelskalender nach R66 (a)? (b) Wo steht der Name: als Tatsachennotiz zu 17.5 oder als Präzisierung zu R66 (a)?

**Neigung.** (a) Der Kalender „NYSE“ des Pakets `pandas_market_calendars` in der Fassung des Locks. Grund: „NYSE“ ist der einzige Kalendername, den der Code des Repos führt, und 53.9 findet den einzigen Aufruf des Pakets in dieser Datei. Ein zweiter Name für den Selektionslauf gäbe demselben Begriff zwei Quellen (der Gegengrund aus der Anfrage 02.10.c, den 02c in Z. 51 annimmt). Die Deckung mit den Kurstagen ist nicht der Grund, sondern das, was die Wache nach R66 (b) im Lauf ohnehin prüft. (b) Präzisierung zu R66 (a), mit Marke an 17.5; 17.5 selbst bleibt zeichengleich. [Voraussetzung, vor dem Eintrag zu messen: der Vergleich „NYSE“ gegen „XNYS“ in der Lock-Umgebung.]

**Handwerk, zur Kenntnis:** Der Zellen-Erzeuger ruft das Paket selbst mit dem registrierten Namen auf; `boersenkalender.py` bleibt ausserhalb der Hülle.

---

## Frage 2 — Deckelfall: Proben und Nachrechnung (53.10 Nr. 2)

**Registertext.** 16.6 (REG Z. 2309–2312): „Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt die Bestätigungsperiode trotzdem — diese Position wird in der Bestätigungsstatistik jedoch nicht gezählt (Attribution je Position, ausdrückliche und seltene Ausnahme von der Ein-Pfad-Regel).“ R37 (i) (48.5, REG Z. 10822): „eine am Deckeltag noch offene solche Position zählt nicht (Attribution je Position)“. R68 (c) (53.3, REG Z. 11398): Eine solche Position „geht in keine Grösse der Zeile ein, auch nicht in ihre Exposure“. R68 (d): „Im Fall nach (c) ist die Zeile nicht der blosse Ausschnitt der Tagesreihe … Wie die Gleichheitsproben nach R60 (c) und R64 (d) und die Nachrechnung nach R36 diesen Fall behandeln, ist offen und geht vor der Öffnung nach R69 (b) als Frage an den Verfahrensprüfer.“

**Was im Deckelfall bricht (Lesart, vorläufig).** `zellen.csv` trägt je Zelle eine Zeile für die Bestätigungsperiode (R33, REG Z. 10791). Für diese Zeile verlangt R60 (c) (REG Z. 11229), dass `mittlere_exposure` dem Mittel der Spalte `exposure` der Tagesreihe gleicht, und R36 (REG Z. 10815), dass `auswertung.py` `kapital_drawdown_mtm_pct` aus `tagesreihen/<zelle>.csv` nachrechnet und bei Abweichung mit 2 endet. Die Tagesreihe ist der eine Kapitalpfad und enthält die nicht gezählte Position; die Zeile enthält sie nicht. Beide Proben schlagen in diesem Fall an, obwohl nichts falsch ist. R64 (d), zweiter Satz, spricht vom Gewinner „je Selektionsfalte“; nach meiner Lesart berührt der Deckelfall ihn nicht (R37: „die Bestätigungsperiode ist keine Falte im Sinn von 4a“), wohl aber den ersten Satz für die Zeile der Bestätigungsperiode.

**Frage.** (a) Bleiben R60 (c) und R36 im Deckelfall als Proben bestehen, und wogegen wird dann geprüft? (b) Heisst „Attribution je Position“: der Beitrag der Position wird aus Rendite und Exposure der betroffenen Tage herausgerechnet (die übrigen Positionen bleiben, wie der eine Pfad sie geführt hat), oder ein zweiter Lauf ohne diese Position? (c) Trifft meine Lesart zu R64 (d)?

**Neigung.** (a) Die Proben bleiben. Im Deckelfall schreibt der Zellen-Erzeuger für die Tage ab `bestaetigung_ab_effektiv` einen zweiten, attribuierten Träger (Rendite und Exposure ohne die nicht gezählte Position); die Zeile der Bestätigungsperiode ist dessen Ausschnitt, und R60 (c) und R36 prüfen diese Zeile gegen ihn. Grund: 16.6 nennt den Fall ausdrücklich eine Ausnahme von der Ein-Pfad-Regel, also gibt es für diese Zeile einen zweiten Pfad; eine Ausnahme von den Proben nennt kein Block. Ob der Träger eine eigene Datei oder ein Spaltenpaar in der Tagesreihe ist, berührt die Feldlisten nach R39 und gehört in denselben R-Block. (b) Herausrechnen, kein zweiter Lauf. Grund: 16.6 und R37 sprechen vom Zählen einer Position, nicht von einem anderen Pfad der übrigen; die Marke an 16.6 (REG Z. 2335–2345) sagt, das Leck schliesse „die Attribution je Position (41.3, C2)“. [Voraussetzung, nicht gemessen: 41.3 C2 habe ich nur über diese Marke gelesen, nicht im Wortlaut.] (c) Ja.

---

## Frage 3 — Zählung der Fehlerklasse „Bestand behauptet statt Voraussetzung genannt“

**Stand im Register.** Neunter Fall: 45.1 (REG Z. 10205). Zehnter und elfter Fall: R52 (48.20, REG Z. 10970); der elfte steht auch in 48.1 (REG Z. 10792: „R5 (b) war Kurzform ohne Nachlesen“). In den Abschnitten 51 bis 53 zählt nichts weiter (0 Treffer).

**Überlassen wurden mir** aus 01a Nr. 6 (Z. 108) der Satz in 25.2 und die „14“ in R26/R30, aus 02c Nr. 4 (Z. 41) die ersetzte Fassung in R68 und „beide Träger“ in R60 (c); dazu nennt die Übergabe deines Vorgängers vom 04.10. (Ablage: `projektfuehrung/FABLE_UEBERGABE_2026-10-04_neuer_chat.md`) die eigene Kalenderquelle in R66 (a) der Fassung 02b.

**Meine Zählung.**
1. **Zwölfter Fall:** 02b, R68 (c) führt R60 (c) für den Satz „beide kommen aus einer Rechnung“ (Rendite und Exposure der Zeile). R60 (c) spricht von den zwei Trägern der Exposure. Das ist eine Aussage über den Wortlaut des Registers ohne Nachlesen, Bauart des elften Falls.
2. **Nicht gezählt:** 02b, R68 und die ersetzte Fassung 2d. 02b hat die Stelle als „[Voraussetzung, zu messen: dass 16.6 den Satz … aus 2d (15.4 (d)) nicht aufhebt; …]“ geführt (02b, Z. 144; die Klammer nennt danach eine zweite Voraussetzung). Die Voraussetzung war genannt; die Messung hat sie widerlegt. Das ist der Weg, den die Klasse verlangt.
3. **Nicht gezählt:** 02b, R66 (a), eigene Kalenderquelle. 02b hat nichts über den Bestand behauptet; es hat 17.5 nicht gesucht. Das fällt unter deinen dritten Satz („Bevor ich sage, etwas stehe nicht im Register, suche ich im Text …“), nicht unter die Klasse.
4. **Nicht gezählt:** die zwei Stellen aus 01a Nr. 6. R62 (a) (51.7) führt den Satz in 25.2 als um einen Balken ungenaue Zählung. R61 (c) (51.6, REG Z. 11245) berichtigt die „14“ in R26 und R30 als Verweis: „lies „14“ als „Sperrlistenpunkt 14 (Abschnitt 10)““. Beides ist Ungenauigkeit einer Zählung oder eines Verweises, keine Aussage über den Bestand von Repo oder Register.

**Frage.** Einverstanden mit zwölf gezählten Fällen? Dann bitte eine Tatsachennotiz in der Bauart von R52.

---

## Zur Kenntnis (je eine Zeile; „einverstanden“ genügt)

- **K1 (53.10 Nr. 8).** An 23.3, Registertext 3b (c), steht die Marke „PRÄZISIERT durch R72 (53.7)“, Unterpunkt (b) (REG Z. 3947). R70 (c) nennt an 23.3 nur die Marke an der Tatsachennotiz; diese hier hat der steuernde Chat nach R65 (a) bestimmt und im Auftrag als seine ausgewiesen.
- **K2 (53.10 Nr. 9).** Zehn Verweise in 02c treffen nur sinngemäss; sie stehen einzeln in 53.9, letzte Tabellenzeile (REG Z. 11454). Keiner trifft nicht.
- **K3.** TB-132 hat R66–R73 am 04.10.2026 als 53.1–53.8 eingetragen (Commit `ee43f5f`); die Probe zu R71 in der Lock-Umgebung gleicht der Vormessung (rc 0, 20 von 20 Zeilen).
