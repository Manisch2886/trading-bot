# RECHERCHE — Vintage-Datenlage: ist der KI-Layer überhaupt testbar? (21.09.2026)

**Gegenstand:** Kettenzeile **`0,98`** im Backlog — `MI-F0 / MI-T0.1`, *„Vintage-Datenlage
erheben (MI3). Rein lesende Recherche, ortsunabhängig. **Entscheidet, ob der KI-Layer
überhaupt testbar ist.**"*

⚠️⚠️ **Herkunft und Prüfstand dieses Dokuments, zuerst, weil alles andere davon abhängt:**

| | |
|---|---|
| **Erhoben** | 21.09.2026 durch eine Rechercheeinheit des steuernden Chats über Web-Abrufe an den Anbieterseiten |
| ⚠️ **NICHT nachgeprüft** | Der steuernde Chat hat **keine** der Angaben an der Quelle gegengelesen. **Nach `C1` ist dieses Dokument damit kein Beleg, sondern ein Rechercheergebnis mit Fundstellen** |
| ⭐ **Was es trotzdem trägt** | Jede Angabe ist als **[gemessen]** (auf der genannten Seite gelesen) oder **[erschlossen]** gekennzeichnet, und jede URL steht am Ende. **Wer eine Zahl braucht, prüft sie dort nach** |
| ⛔ **Was es nicht ist** | Keine Empfehlung, keine Kostenabwägung, keine Architekturentscheidung |

⭐ **Warum die Frage überhaupt gestellt wurde** (Backlog `MI3`): *Makrodaten werden
nachträglich revidiert; wer mit der revidierten Reihe backtestet, hat Look-ahead **per
Konstruktion** — nicht abgeschwächt, sondern ungültig. Dasselbe für Nachrichten: der
Zeitpunkt, zu dem eine Meldung **handelbar** war, ist nicht ihr Veröffentlichungsstempel.*

---

## 1. Die Antwort in drei Sätzen

⭐⭐ **An der Makrodatenlage scheitert das Vorhaben nicht.** Vintage-Reihen für
Arbeitsmarkt, Inflation, Industrieproduktion und Zinsstruktur gibt es für die USA
kostenlos, per API, mit Historie weit vor 2016; für Deutschland und den Euroraum
kostenlos ab 2005.

⚠️ **Der belegbare Grund, an dem es scheitern *kann*, liegt bei den Nachrichten** — und
er ist kein Verfügbarkeits-, sondern ein **Qualitätsproblem**: kostenlos bekommt man nur
*Crawl-Zeitstempel auf allgemeine Webnachrichten*; die kuratierten Finanz-Feeds mit echter
Zeitstempeldisziplin beginnen erst 2017, zeigen im bezahlbaren Tarif nur drei Monate
Historie oder kosten fünfstellig im Jahr.

⚠️⚠️ **Und ein dritter Punkt, der nicht erfragt war und trotzdem zählt:** Ein aus
Makrodaten abgeleiteter Marktzustand stützt sich ab 2016 auf rund **115 monatliche
Beobachtungen je Reihe**. *Die Vintage-Frage entscheidet, ob der Backtest **gültig** ist;
sie entscheidet nicht, ob er **aussagekräftig** ist.* **[erschlossen]**

---

## 2. Makro-Vintage: die Quellen

| Quelle | Träger | Abdeckung | Historie | Kosten | API |
|---|---|---|---|---|---|
| ⭐ **ALFRED / FRED-API** | Fed St. Louis | >350 000 Real-Time-Reihen | PAYEMS: früheste Vintage **1955-05-06**, ~850 Vintage-Termine | **0 €**, Registrierung | ⭐ **ja** — `realtime_start`/`realtime_end`, `series/vintagedates`; `fredapi` |
| **RTDSM** | Fed Philadelphia | NIPA, Arbeitsmarkt, Preise, **Industrieproduktion**, Kapazitätsauslastung | IP-Vintages ab **Nov. 1962**, monatlich | **0 €** | nein (Excel) |
| **OECD Real-Time Historical Dataset** | Fed Dallas | 26 OECD-Länder × 13 Reihen | Vintages **1962:Q1–1998:Q4** | **0 €** | nein |
| **GERDA** | Bundesbank | ~280 Indikatoren | VGR ab **Mai 2005**, Konjunktur ab Nov. 2005 | **0 €** | ⚠️ im techn. Dokument **nicht erwähnt** |
| **ECB Real Time Database** | EZB | >200 Euroraum-Variablen | seit **Okt. 2005** | **0 €** | SDMX (allgemein) |
| **EABCN RTD** | EABCN | Euroraum + Länder | seit Okt. 2005 | — | ⛔ *„not currently available"* |
| **DBnomics** | Cepremap | >90 Provider | — | **0 €** | ja — ⚠️ **aber keine Vintage-Quelle**, siehe unten |

### ⚠️ Drei Befunde, die man kennen muss

| | |
|---|---|
| ⭐⭐ **ALFRED ist die einzige echte Vintage-API.** | `realtime_start`/`realtime_end` liefern, was am Stichtag bekannt war **[gemessen]** |
| ⚠️ **Aber: Tagesauflösung, keine Uhrzeit.** | Und FRED warnt selbst: *„release dates are published by data sources and do not necessarily represent when data will be available on the FRED or ALFRED websites"* **[gemessen]**. ⇒ *„Vintage-Datum = Entscheidungszeitpunkt" ist eine Näherung, keine Identität* **[erschlossen]** |
| ⚠️⚠️ **DBnomics: Bewerbung ≠ Beleg.** | Die Übersichtsseite sagt, man könne daraus Echtzeit-Datenbanken bauen; die **Data-Model-Doku** beschreibt aber nur *dataset releases* (`WEO:2019-04` gegen `WEO:2020-04`), also getrennte Ausgaben ganzer Datensätze — **keine Vintage-Abfrage je Reihe und Stichtag** **[gemessen]**. ⇒ Für einen Backtest **erschlossen** kein Vintage-Dienst, sondern ein Aggregator revidierter Reihen |

### Abdeckung nach Reihenklasse

| Klasse | US | Euro/DE | |
|---|---|---|---|
| Arbeitsmarkt | ✅ tief (PAYEMS ab 1955) | ✅ GERDA, ECB RTD | stärkste Abdeckung |
| Inflation | ✅ CPI, Kern-CPI, PPI, Deflatoren | ✅ GERDA Preisindizes | |
| Industrieproduktion | ✅ **ab Nov. 1962** | ✅ ab Nov. 2005 | |
| Zinsstruktur | ✅ trivial | ✅ | ⭐ **Marktpreise werden nicht revidiert — hier gibt es kein Revisionsrisiko** |
| ⛔ **Einkaufsmanagerindizes** | ❌ | ❌ | ⚠️ **Die einzige echte Lücke.** Die Fed hat am **24.06.2016** alle 22 ISM-Reihen aus FRED entfernt **[gemessen]**; S&P Global PMI veröffentlicht keine Preise |

⭐ **Für den Auswertungszeitraum ab 2016 reicht die europäische Abdeckung** (Vintage ab
2005) — *ein günstiger Zufall der Fragestellung* **[erschlossen]**.

---

## 3. Nachrichten: wo es wirklich schwierig wird

### ⭐⭐ Die Unterscheidung, um die es geht

Webz.io trennt **vier** Zeitpunkte, und genau darin liegt das Problem **[gemessen]**:

| | |
|---|---|
| **Publication time** | was der Verlag behauptet — Webz.io nennt es ausdrücklich *„a source claim"* |
| **Discovery time** | wann der Anbieter den Artikel gefunden hat |
| **Indexing time** | wann er durchsuchbar wurde |
| **Delivery time** | wann er beim Kunden ankam |

⇒ ⭐ **Nur (2)–(4) sind vom Anbieter messbar; (1) ist eine Fremdangabe.** Ein Backtest
darf nicht auf (1) beruhen **[erschlossen]**.

### Was das Kriterium besteht

| Quelle | Zeitstempel | Historie | Kosten |
|---|---|---|---|
| ⭐ **GDELT** | benutzt für Quellen des offenen Webs ausdrücklich die *retrieval completion time* als autoritativen Zeitstempel; die Verlagsangabe nur als Sekundärfeld **[gemessen]** | 2.0 ab **19.02.2015**, alle 15 Min., 65 Sprachen | **0 €** |
| ⭐ **Common Crawl CC-NEWS** | **Crawl-Zeit im Dateinamen** (`CC-NEWS-20160926211809-…`) **[gemessen]** | ab **Okt. 2016** | 0 € + ggf. AWS |
| **Tiingo** | ⭐ führt **zwei** Felder und erklärt sie selbst: `publishedDate` *„usually reported by the news source"*, `crawlDate` *„always recorded by Tiingo"* — Lücke dazwischen weist auf **Backfill** **[gemessen]** | ⚠️ siehe unten | 30–50 $/Mon. |

### ⚠️ Wo Bewerbung und Beleg auseinanderfallen

| | |
|---|---|
| ⚠️⚠️ **Tiingo** | Die Produktseite wirbt mit Archiv *„going back from 1995"* und 70+ Mio. Artikeln. **Die Tabelle auf derselben Seite:** Power (30 $) = **3 Monate** abfragbare Historie, Commercial (50 $) = **ebenfalls 3 Monate**; „20+ years" nur **Enterprise, Preis auf Anfrage** **[gemessen]**. ⇒ Für einen Backtest ab 2016 im Kleinbudget **unbrauchbar** — nicht wegen der Zeitstempelqualität, sondern wegen der Tiefe |
| ⚠️ **EODHD** | nur ein `date`-Feld, *„Publication date and time"* — die **Verlagsangabe**, kein eigenes Crawl-Feld. **Keine Angabe zur Historientiefe** **[gemessen, negativ]** |
| ⚠️ **Benzinga** | Start **Sept. 2017**, Sekundenauflösung, ~1 250 Artikel/Tag **[gemessen]** — bester Kompromiss im bezahlbaren Bereich, **reicht aber nicht bis 2016** |
| ⚠️ **RavenPack** | Produktseite nennt **keine** Zeitstempelfelder, **keine** Historientiefe, **keine** Point-in-Time-Zusage, **keine** Preise **[gemessen, negativ]**. Alles Bekannte stammt aus Nutzerdokumentation, nicht vom Anbieter. ⇒ Point-in-Time-Eigenschaft **unbelegt, nicht widerlegt** |
| **Dow Jones** *(Drittquelle)* | API-/Feed-Zugang **5 000 bis über 50 000 $**; Median-Jahresvertrag 16 851 $ **[gemessen, Drittquelle Vendr]** |

### ⭐ Ein Fund am Rande, der eigenständig wertvoll ist

**Trading Economics** hat einen dokumentierten Endpunkt *„Economic Calendar
Point-in-Time"*, der Ereignisse liefert *„exactly as they appeared on a specific date,
preserving the original values before any subsequent revisions"* — mit Actual, Previous,
**Forecast**, Revised **[gemessen]**. ⭐⭐ **Das ist konzeptionell genau richtig und
enthält etwas, das ALFRED nicht hat: den Point-in-Time-Konsens.** ⚠️ Historientiefe und
erforderliche Tarifstufe nennt die Doku **nicht**; die Preisseite lieferte nur AGB
**[gemessen, negativ]**.

---

## 4. Was offen bleibt — und wie man es schliesst

⭐ **Jede Zeile ist eine Messung, kein Rechercheauftrag.** Die teuerste kostet einen
Trial-Zugang.

| Offene Frage | Was zu messen ist |
|---|---|
| ⭐ **Historientiefe des Trading-Economics-Point-in-Time-Kalenders** | Trial (100 Requests frei), `initDate=2016-01-01` abfragen, prüfen wie weit zurück Daten kommen und ob `Revised` konsistent gesetzt ist |
| ⭐⭐ **Ob ALFRED-Vintagedatum = Veröffentlichungsdatum ist** | Für 20–30 bekannte Termine (BLS-Kalender) das amtliche Release-Datum gegen das ALFRED-Vintagedatum halten und die **Verteilung der Abweichung** messen. ⭐ *Das liefert die Lag-Konstante für den Backtest* |
| ⭐ **Tatsächliche Crawl-Latenz von GDELT** | Für ~50 bekannte Ereignisse (FOMC-Entscheide) die `DATEADDED`-Zeit gegen die amtliche Veröffentlichungszeit halten. ⚠️ *„15-Minuten-Zyklus" ist die Zykluslänge, nicht die gemessene Latenz* |
| **Herkunft der ALFRED-Vintages vor 2006** | Für eine Reihe ALFRED- gegen RTDSM-Vintages desselben Termins halten. ⭐ *Sind sie identisch, ist die Herkunft geklärt — **und man weiss zugleich, dass man beide nicht als unabhängige Bestätigung zählen darf*** |
| **Ob ECB RTD über SDMX abfragbar ist** · **ob GERDA maschinell abrufbar ist** | Dataflow-Listen abrufen |
| **GDELT-DOC-API-Reichweite** (3 Monate rollend oder ab 2017?) | ⚠️ Die Ankündigung **widerspricht sich selbst** **[gemessen, widersprüchlich]** — eine Abfrage mit `startdatetime=20170101` klärt es |
| **EODHD-News-Historientiefe** | Free-Key, `from=2016-01-01`, ältestes `date` ablesen |
| **Status der OECD-ORD-Datenbank** | Im OECD Data Explorer nach dem Datensatz suchen |

---

## 5. Was daraus für das Epic MI folgt

⚠️ **Einordnung des steuernden Chats, ausdrücklich erschlossen und nicht Teil der
Recherche:**

| | |
|---|---|
| ⭐ | **`MI-T0.3` („Architekturentscheidung: ohne Vintage kein KI-Layer-Backtest") kann beantwortet werden** — für die Makroseite mit **ja, testbar** |
| ⚠️ | **Für die Nachrichtenseite lautet die ehrliche Fassung anders:** testbar auf einem Zeitstempel, der *„spätestens ab hier auffindbar"* bedeutet und nicht *„ab hier handelbar"*. **Das ist eine schwächere Information als die, die `MI-F10` (Ereignisextraktion) voraussetzt** |
| ⚠️⚠️ | **Der Stichprobenbefund aus Abschnitt 1 trifft `MI2` unabhängig von der Vintage-Frage** — und `MI2` war schon vorher als **Hauptrisiko** des Epics benannt (*„Regime-Zellen als Scheinwissen"*). ⭐ *Die Vintage-Antwort räumt ein Hindernis weg und lässt das grössere stehen* |
| ⛔ | **Keine Entscheidung, keine Empfehlung.** Das Epic bleibt hinter dem signierten Tag geparkt (`MI0`); diese Recherche ändert daran nichts |

---

## Quellen

**Makro-Vintage:** `fred.stlouisfed.org/docs/api/fred/realtime_period.html` ·
`…/series_vintagedates.html` · `…/releases_dates.html` · `alfred.stlouisfed.org` (und
`/help`, `/series/downloaddata?seid=PAYEMS`) ·
`fredblog.stlouisfed.org/2021/04/alfred-at-15-archiving-fred-data-since-2006/` ·
`news.research.stlouisfed.org/2016/06/institute-for-supply-management-data-to-be-removed-from-fred/` ·
`philadelphiafed.org/surveys-and-data/real-time-data-research/…` (RTDSM, Full-Time-Series,
`doc_ip.pdf`) · `dallasfed.org/research/international/oecd` ·
`bundesbank.de/en/press/press-releases/new-real-time-database-…-670274` (+ technisches PDF) ·
`eabcn.org/data/eabcn-real-time-database` · `data.ecb.europa.eu/data/datasets/rtd/…` ·
`bankofengland.co.uk/quarterly-bulletin/2002/q1/…` · `oecd.org/en/publications/…` ·
`docs.db.nomics.world/` (+ `/data-model/`) · `pypi.org/project/fredapi`

**Kalender:** `docs.tradingeconomics.com/economic_calendar/point-in-time/` ·
`tradingeconomics.com/api/pricing.aspx`

**Nachrichten:** `gdeltproject.org/` (+ `/data.html`) ·
`blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/` ·
`…/gdelt-doc-2-0-api-debuts/` · `…/a-behind-the-scenes-look-at-how-we-think-about-master-file-formats-and-timestamping/` ·
`commoncrawl.org/blog/news-dataset-available` · `data.commoncrawl.org/crawl-data/CC-NEWS/index.html` ·
`tiingo.com/documentation/news` (+ `/products/news-api`, `/about/pricing`) ·
`eodhd.com/financial-apis/stock-market-financial-news-api` ·
`quantconnect.com/docs/v2/writing-algorithms/datasets/benzinga/benzinga-news-feed` ·
`ravenpack.com/products/edge/data/news-analytics` ·
`webz.io/blog/news-api/latency-in-news-apis-…` · `vendr.com/marketplace/dow-jones` ·
`spglobal.com/market-intelligence/en/solutions/products/resources/pmi-faq`

---

## In einfacher Sprache

**Die Frage war:** Kann man Wirtschaftsdaten so beschaffen, wie sie **damals** zuerst
veröffentlicht wurden? Das klingt kleinlich, entscheidet aber alles — denn solche Daten
werden später nach oben oder unten korrigiert. Wer mit den korrigierten Zahlen
nachrechnet, benutzt Wissen, das es damals nicht gab. Der Test wäre dann nicht ungenau,
sondern wertlos.

**Die Antwort für Wirtschaftsdaten: ja, und kostenlos.** Die US-Notenbank führt ein
Archiv, das für jede Reihe sagt, was an einem bestimmten Tag bekannt war — bei manchen
Reihen bis 1955 zurück, mit einer Programmierschnittstelle. Für Deutschland und den
Euroraum gibt es dasselbe ab 2005, was für einen Zeitraum ab 2016 genügt. Nur eine
Datenart fehlt: die Einkaufsmanager-Umfragen, die die Notenbank 2016 aus ihrem Angebot
genommen hat.

**Die Antwort für Nachrichten: eingeschränkt.** Kostenlos bekommt man nur den Zeitpunkt,
zu dem ein Sammelprogramm einen Artikel im Netz **gefunden** hat — nicht den, zu dem er
handelbar war. Die sauberen Finanzdienste fangen entweder erst 2017 an, zeigen im
bezahlbaren Tarif nur drei Monate zurück, oder kosten fünfstellig im Jahr.

**Und ein Punkt, den niemand gefragt hatte:** Selbst wenn alle Daten sauber sind, gibt es
seit 2016 nur rund 115 Monatswerte je Reihe. Die saubere Datenlage macht einen Test
**gültig** — sie macht ihn nicht **aussagekräftig**. Das war schon vorher das Hauptrisiko
dieses Vorhabens, und es bleibt es.
