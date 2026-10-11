# Recherche 10.10.2026 — Kerzenformationen als Handelssignal: Bestand und Evidenz

Verweise [Qn] führen zum Link im Abschnitt „Quellen“. Alle Zahlen stammen von den genannten Seiten. Keine Anlageempfehlung.

## 1. Überblick

**Familien.** Ein-Kerzen-Muster: Doji (Dragonfly, Gravestone, Long-legged), Hammer/Hanging Man, Shooting Star/Inverted Hammer, Marubozu. Zwei-Kerzen-Muster: Engulfing, Harami, Piercing Line/Dark Cloud Cover, Tweezer Top/Bottom. Drei-Kerzen-Muster: Morning/Evening Star, Three White Soldiers/Three Black Crows, Three Inside Up/Down (Harami plus Bestätigungskerze), Three Outside Up/Down (Engulfing plus Bestätigungskerze). Fortsetzungsmuster: Rising/Falling Three Methods, Rising/Falling Window (Kurslücke). Die „Confirmation Candle“ der Grafik ist somit nichts Neues: Engulfing plus Bestätigung ist „Three Outside“, die Sterne enthalten sie bereits.

**Anzahl.** TA-Lib: 61 CDL-Funktionen [Q1][Q2]; Bulkowski: 103 Muster [Q3]; in Studien getestet: 28 [Q4], 83 Regeln [Q5], 68 [Q6]. Zahl bei Nison: nicht gefunden.

**Schärfe.** TA-Lib misst „lang“, „kurz“ und „Doji“ relativ zum Durchschnitt der letzten N Kerzen (Doji: Körper unter 10 % der mittleren Spanne von 10 Kerzen; langer Docht: länger als der Körper); alles ist einstellbar. Im Dokumentationsbeispiel ändert sich die Doji-Zahl einer BTC-Reihe je Einstellung von 56 auf 61 bzw. 109 [Q2]. TA-Lib prüft keinen Trend: Laut Quelltext muss der Hammer im Abwärtstrend stehen, die Funktion berücksichtigt das aber nicht; beim Morning Star verlangt die zweite Kerze eine Kurslücke [Q7][Q8]. Etschberger u. a. (2006): bis dahin kein automatisches, deterministisches Klassifikationsverfahren [Q9]. Der Trend wird je Studie anders gefasst (3-Tage-Durchschnitt, sechs Tage fallend [Q12]; 10-Tage-EMA [Q4]); das entscheidet mit über das Ergebnis [Q11].

*Eigene Anmerkung:* In 24/7-Kryptomärkten liegt die Eröffnung praktisch auf dem Vorschluss; Definitionen mit Kurslücke treffen dort kaum zu oder müssen umdefiniert werden.

## 2. Evidenz

| Studie | Markt, Zeitraum, Zeitrahmen | Ergebnis | Kosten | Quelle |
|---|---|---|---|---|
| Caginalp & Laurent 1998 | S&P-500-Aktien 1/1992–6/1996; Tag | Acht Drei-Tage-Umkehrmuster mit Trendbedingung signifikant (Z rund 36); rund 0,9 % je Kauf über etwa zwei Tage vor Kosten | geschätzt (Spanne 0,1–0,3 %), danach 0,56–0,76 %; Korrelation der Aktien bläht Z auf | [Q10][Q12] |
| Fock, Klein & Zwergel 2005 | DAX- und Bund-Future; Intraday; Zeitraum, Kerzenlänge: nicht gefunden | Keine Vorhersagekraft, auch nicht mit Momentum | nicht gefunden | [Q13] |
| Marshall, Young & Rose 2006 | DJIA-Aktien 1992–2002; Tag | 28 Muster, Bootstrap gegen vier Nullmodelle: kein Mehrwert | nicht modelliert; schon brutto nichts | [Q14][Q15][Q4] |
| Marshall, Young & Cahan 2008 | Japan, Aktien 1975–2004; Tag | Nicht profitabel, auch nicht in Teilperioden | schon vor Kosten nichts | [Q16] |
| Horton 2009 | 349 Aktien; Markt, Zeitraum nicht genannt | „little value“ | nicht genannt | [Q17] |
| Lu, Shiu & Liu 2012 | Taiwan, Top-50-Aktien, 10/2002–12/2008; Tag | Drei bullische Zwei-Tage-Umkehrmuster profitabel (Halten bis Gegensignal) | nicht genannt | [Q18] |
| Lu 2014 | Taiwan 1992–2009; Tag | Vier Ein-Kerzen-Muster profitabel | laut Abstract nach Kosten | [Q19] |
| Duvinage, Mazza & Petitjean 2013 | 30 DJIA-Aktien, 4/2010–4/2011; 5 Minuten | Brutto schlägt rund ein Drittel der 83 Regeln Buy-and-hold, netto wenige, nach Data-Snooping-Korrektur keine | 0,05 % je Richtung | [Q5][Q20] |
| Lu, Chen & Hsu 2015 | DJIA-Aktien; Tag; Zeitraum nicht genannt | Acht Drei-Tage-Umkehrmuster mit Haltestrategie nach Caginalp/Laurent profitabel trotz Data-Snooping-Korrektur; mit jener nach Marshall u. a. nicht | 0,5 % (und 0,1 %) | [Q11] |
| Chen, Bao & Zhou 2016 | China; Tag | Drei von acht Zwei-Tage-Mustern mit Vorhersagekraft; fällt mit dem Horizont; Step-SPA-Test | nicht genannt | [Q21] |
| Chin u. a. 2016 | Malaysia 2000–2014 | Nur bullische Umkehrmuster profitabel, auch Out-of-Sample | ja | [Q23] |
| Tharavanij u. a. 2017 | Thailand SET50, 7/2006–6/2016; Tag | Meist kein Ertrag ungleich null; Filter (Stochastik, RSI, MFI) helfen nicht | nicht genannt | [Q24] |

**Kryptowährungen**

| Studie | Markt, Zeitraum, Zeitrahmen | Ergebnis | Kosten | Quelle |
|---|---|---|---|---|
| Ho u. a. 2021 (IEEE-Konferenz) | 23 grösste Coins; Tag | 68 Muster „of little use“ | nicht genannt | [Q6] |
| Cohen 2021 (Rev. Quant. Finance & Accounting) | Bitcoin 2012–7/2020; Zeitrahmen nicht genannt | Engulfing als einziges klassisches Muster brauchbar (Profit-Faktor 3,54), Harami nicht; Long besser als Short; Varianten nachträglich optimiert | nicht genannt | [Q26] |
| Senanayaka & Pathberiya 2024 | Ethereum; Stunde | Trefferquote aus Kerzenmerkmalen rund 50 % | nicht behandelt | [Q27] |
| Financial Research Journal 2026 (Kharazmi-Universität) | Bitcoin 9/2017–5/2025; Stunde | Fuzzy-Codes einzelner Kerzen: Trefferquote 54,1 bzw. 55,8 %, im Rücktest über Buy-and-hold | nicht genannt, daher nicht belastbar | [Q28] |
| Kuna 2025 (Bachelorarbeit) | Kryptowährungen, 41 Muster | Acht Muster auffällig, zwei davon gegen die Lehrbuchrichtung; „limited applicability“ | nicht genannt | [Q29] |

**Überblick.** Park und Irwin (2007): 95 neuere Studien zur technischen Analyse (56 positiv, 20 negativ, 19 gemischt); als verbreitete Mängel nennen sie Data-Snooping, nachträgliche Regelauswahl und unsichere Kostenschätzung [Q31]. Überblicksarbeit nur zu Kerzenmustern: nicht gefunden; am nächsten kommt der Literaturteil in [Q24].

**Bulkowski.** Grundlage: 103 Muster, über 4,7 Millionen Kursbalken, 500 Aktien über zehn Jahre [Q3]. „Reversal“ heisst dort, dass der Kurs zuerst jenseits des Musterrands schliesst, auf der Seite, von der er kam. Werte: Bullish Engulfing 63 % (Gesamtrang 84 von 103) [Q32], Bearish Engulfing 79 % (Rang 91) [Q33], Hammer 60 % („not far from random (50%)“) [Q34], Shooting Star 59 % [Q35], Morning Star 78 % [Q36], Evening Star 72 % [Q37]. Grenzen: nicht begutachtet; „hundreds of perfect trades“; keine Kosten; keine Korrektur für Mehrfachtests; die Quote misst einen Ausbruch, keinen Handelsertrag; nur US-Aktien auf Tagesbasis. *Eigene Anmerkung:* Endet ein Muster mit einer grossen Kerze, liegt der Schluss schon nahe am Musterrand; der Ausbruch dorthin ist rechnerisch begünstigt.

## 3. Warum Muster oft besser aussehen, als sie sind

- **Mehrfachtests:** Bei 61 bis 103 Mustern, mehreren Zeitrahmen und Haltedauern sind Zufallstreffer sicher; nach der Korrektur bleibt bei Duvinage u. a. keine Regel übrig [Q5] (Verfahren nach Sullivan, Timmermann und White [Q38]).
- **Auswahl im Rückblick:** Lehrgrafiken zeigen gelungene Beispiele; Bulkowski wertet „perfect trades“ aus [Q32].
- **Unscharfe Definitionen:** Kleine Schwellenänderungen ändern die Trefferzahl [Q2]; jede Stellschraube ist ein weiterer Test.
- **Kosten und Slippage:** 0,05 % je Richtung zehren bei Duvinage u. a. fast alles auf [Q20].
- **Trendfilter:** Ohne Vergleich gegen den Trendfilter allein bleibt offen, ob das Muster wirkt oder nur die Gegenbewegung nach einem Rückgang (eigene Folgerung aus [Q11]).

## 4. Was die Befunde eher stützen

Belegt, jeweils nur in einzelnen Studien:
- Drei-Kerzen-Umkehrmuster mit Trendbedingung und kurzer, fester Haltedauer [Q10][Q11]; mit anderer Trend- und Ausstiegsregel verschwindet der Effekt [Q4].
- Bullische Signale besser als bearische [Q20][Q18][Q23][Q26].
- Kleinere, weniger effiziente Märkte (Taiwan, China, Malaysia) [Q18][Q19][Q21][Q22][Q23]; volatile Phasen [Q11].
- Kurzer Horizont [Q21].
- Volumen und Eröffnung des Folgetags als Bestätigung: nur Shiu und Lu 2011, Taiwan, Kosten nicht genannt [Q39].
- Doji: Hinweis auf niedrigere Markteinflusskosten, nicht auf die Richtung [Q30].

Nicht belegt: Nutzen im Intraday-Handel [Q13][Q5]; Zusatzfilter mit Oszillatoren oder Momentum [Q24][Q13]. Nur Lehrmeinung (keine Studie gefunden): Eine besonders grosse Bestätigungskerze erhöhe die Trefferquote; höhere Zeitrahmen seien verlässlicher; ein Muster sei ohne Trendbezug ein Kauf- oder Verkaufssignal.

## 5. Zu den Mustern der Grafik

- **Engulfing (mit Bestätigung: Three Outside):** Marshall u. a. testen Engulfing und Three Outside Up/Down ohne signifikanten Befund [Q4]; bei Caginalp/Laurent zählen Three Outside Up/Down zur signifikanten Achtergruppe [Q12]. Zhu u. a. (China 1999–2008): Engulfing nur bei liquiden kleinen Titeln profitabel [Q22]. Cohen: bei Bitcoin positiv, ohne Kostenangabe [Q26].
- **Morning/Evening Star:** Teil der Achtergruppe [Q12]; bei Mukansi (Masterarbeit, Johannesburg 2010–2019) nur im Industriesektor auf 10-%-Niveau, nach Gebühren ohne Vorteil [Q25]. Für Kryptowährungen: nicht gefunden.
- **Hammer, Shooting Star, Tweezer Top:** Bei Marshall u. a. ohne Befund [Q4]; Bulkowski 60 % und 59 % [Q34][Q35]; bei Kuna für Kryptowährungen auffällig, ohne Kosten [Q29].
- **Doji mit Bestätigung:** Dragonfly und Gravestone Doji als Einzelkerzen bei Marshall u. a. ohne Befund [Q4]. Doji plus Bestätigungskerze als eigenes Muster, Long-legged Doji und Bulkowskis Doji-Werte: nicht gefunden.

## 6. Folgerung für ein regelbasiertes System mit Vorregistrierung

Prüfbar ist nur, was vorab festliegt: das Muster als Ungleichungen über Open, High, Low und Close (etwa nach Caginalp/Laurent oder mit eingefrorenen TA-Lib-Einstellungen), Trenddefinition, Einstieg zur Eröffnung der Folgekerze, feste Haltedauer, Kostenansatz, Markt und Zeitrahmen. Hypothese 1 (S&P 500, Tag): Einstiege nach „Three Outside Up“ oder Morning Star im definierten Abwärtstrend erzielen nach Kosten einen höheren mittleren Ertrag als Einstiege an allen übrigen Tagen mit derselben Trendbedingung in denselben Titeln. Hypothese 2 (Filter statt Strategie): Einstiege der bestehenden RSI-2- oder Turtle-Soup-Regel mit einem vorab definierten bullischen Muster am Signaltag haben nach Kosten einen höheren Erwartungswert je Trade als die übrigen Einstiege derselben Regel; das lässt sich an vorhandenen Trade-Listen prüfen. Hypothese 3 (Krypto, 4 Stunden und Tag): dieselbe Prüfung mit einer Definition ohne Kurslücke, je Zeitrahmen getrennt. Muster, Zeitrahmen und Haltedauern sind vorab klein zu halten und gemeinsam auf Mehrfachtests zu korrigieren; bearische Signale sind getrennt auszuweisen. Nicht zu erwarten sind eine eigenständige, nach Kosten tragfähige Strategie aus Einzelmustern, Trefferquoten in Bulkowskis Höhe als Handelsergebnis, Stabilität über Märkte und Zeiträume sowie ein Nutzen auf Stundenkerzen. Ein Nullbefund wäre mit der Mehrheit der Studien an liquiden Märkten vereinbar und für sich verwertbar.

## Quellen

Seite aufgerufen:
- Q1 https://ta-lib.org/functions/
- Q2 https://cran.r-project.org/web/packages/talib/vignettes/candlestick.html
- Q3 https://traders.com/Documentation/FEEDbk_docs/2011/11/Bulkowski.html
- Q4 Begleitarbeit Marshall/Young/Rose, gleiche Daten: https://c.mql5.com/forextsd/forum/211/Market%20Timing%20with%20Candlestick%20Technical%20Analysis.pdf
- Q5 https://ideas.repec.org/a/taf/quantf/v13y2013i7p1059-1070.html
- Q6 https://repository.eduhk.hk/en/publications/do-candlestick-patterns-work-in-cryptocurrency-trading/
- Q7 https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_CDLHAMMER.c
- Q8 https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_CDLMORNINGSTAR.c
- Q9 https://link.springer.com/chapter/10.1007/3-540-31314-1_64
- Q10 https://ideas.repec.org/a/taf/apmtfi/v5y1998i3-4p181-205.html
- Q11 https://ideas.repec.org/a/eee/jbfina/v61y2015icp172-183.html
- Q12 https://c.mql5.com/forextsd/forum/210/The%20Predictive%20Power%20of%20Price%20Patterns.pdf
- Q13 Zitat der Autoren: https://improbable.com/2015/06/28/fock-performance-of-candlestick-analysis
- Q14 ohne Abstract: https://ideas.repec.org/a/eee/jbfina/v30y2006i8p2303-2323.html
- Q15 Dissertation Marshall: https://mro.massey.ac.nz/handle/10179/1604
- Q16 https://link.springer.com/article/10.1007/s11156-007-0068-1
- Q17 https://ideas.repec.org/a/eee/quaeco/v49y2009i2p283-294.html
- Q18 https://ideas.repec.org/a/wly/revfec/v21y2012i2p63-68.html
- Q19 https://ideas.repec.org/a/eee/pacfin/v26y2014icp65-78.html
- Q20 Zusammenfassung Dritter: https://cxoadvisory.com/technical-trading/testing-japanese-candlesticks-intraday-on-liquid-stocks
- Q21 https://ideas.repec.org/a/eee/phsmap/v457y2016icp148-165.html
- Q22 https://ideas.repec.org/a/eee/pacfin/v37y2016icp116-127.html
- Q23 https://ir.unimas.my/id/eprint/18130
- Q24 https://journals.sagepub.com/doi/10.1177/2158244017736799
- Q25 https://open.uct.ac.za/handle/11427/35958
- Q26 https://ideas.repec.org/a/kap/rqfnac/v57y2021i3d10.1007_s11156-021-00973-6.html
- Q27 https://sljastats.sljol.info/articles/10.4038/sljas.v25i1.8131
- Q28 https://jfr.ut.ac.ir/article_107529_en.html
- Q29 https://dspace.cuni.cz/handle/20.500.11956/197060
- Q30 https://ideas.repec.org/a/eee/jbfina/v48y2014icp386-395.html
- Q31 https://ideas.repec.org/a/bla/jecsur/v21y2007i4p786-826.html
- Q32 https://thepatternsite.com/BullEngulfing.html
- Q33 https://thepatternsite.com/BearEngulfing.html
- Q34 https://thepatternsite.com/Hammer.html
- Q35 https://thepatternsite.com/ShootingStar.html
- Q36 https://thepatternsite.com/MorningStar.html
- Q37 https://thepatternsite.com/EveningStar.html
- Q38 Arbeitspapier: https://ideas.repec.org/p/fmg/fmgdps/dp303.html
- Q39 https://nccur.lib.nccu.edu.tw/handle/140.119/61657

Nur Suchtreffer (nicht lesbar, nicht für Aussagen verwendet):
- Marshall u. a. 2006, Abruf abgewiesen (HTTP 429): https://doi.org/10.1016/j.jbankfin.2005.08.001
- Fock u. a., Serverfehler: https://www.pm-research.com/content/iijderiv/13/1/28
- Ho u. a., leer geliefert: https://ieeexplore.ieee.org/document/9671826

Nicht gefunden: Zeitraum und Kerzenlänge bei Fock u. a.; Kostenbehandlung im Zeitschriftenartikel von Marshall u. a. 2006; Markt und Zeitraum bei Horton; Zahl der Muster bei Nison; Bulkowskis Doji-Werte; Überblicksarbeit nur zu Kerzenmustern; begutachtete Krypto-Studie klassischer Muster auf Stundenkerzen mit Kosten und Data-Snooping-Korrektur; Studie zur Grösse der Bestätigungskerze als eigener Bedingung.

## In einfacher Sprache

Kerzenmuster sind Formen im Kursbild, denen Lehrbücher eine Richtung zuschreiben. Sorgfältige Untersuchungen an grossen, liquiden Märkten finden meist keinen Vorteil, der nach Gebühren übrig bleibt. Wo ein Vorteil gemessen wurde, hing er an genauen Regeln für Trend, Haltedauer und Markt, nicht an der Form allein. Für die Bots heisst das: höchstens als klar definierte Zusatzbedingung prüfen, vorab festgelegt, und mit einem Nullergebnis rechnen.
