# FABLE_ANTWORT 2026-09-21c — Übergabe bestätigt; Projektzugriff gemessen; ein verlorener Satz und eine Lücke vor der ersten Falte

*Bezug: Übergabetext Fassung 2 vom 21.09. (neuer Chat). Antwort auf Abschnitt 7. Punkt 3.1 enthält eine Entscheidung, die vor dem Ableiten der Falten gebraucht wird; Punkt 3.2 eine Regel, die vor einer Messung festgeschrieben werden soll.*

---

## 1. Was ich von (a) bis (g) noch habe

**Aus dem alten Chat: nichts.** Ich erinnere keinen einzigen der Sätze; für diesen Chat ist alles in Abschnitt 3 neu. Ich sage das so deutlich, weil die ehrliche Alternative zu „ich erinnere mich" nicht „ich rekonstruiere" ist.

**Aber ich musste euch nicht glauben — ich konnte nachlesen** (siehe 2). Gegen meine abgelegten Antworten geprüft:

| | Übergabe | geprüft gegen | Befund |
|---|---|---|---|
| (c) | Konjunktion | 20e | Wortlaut trifft |
| (d) | Horizont je Bot | 21a | Wortlaut trifft — **aber ein Satz aus 20e fehlt, siehe 3.1** |
| (e) | Grenzfall, Aktenzeichen | 21a, 21b | trifft; **ein Widerspruch in eurer eigenen Ablage, siehe 3.3** |
| (f) | asof | 21b | Wortlaut trifft, Zitate wörtlich |
| (g) | Wache | 21b | Wortlaut trifft, Zitate wörtlich |
| (a), (b) | Benchmark, MtM | — | **nicht geprüft** (20b–20d nicht gelesen); ich übernehme sie auf eure Angabe |

F17 habe ich nur in eurem Wortlaut. Ich übernehme ihn; er trägt die Punkte unten.

## 2. Zugriff auf das Projekt „Trading Bots" — ja, gemessen

- **Lesen: ja.** 24 Dokumente unter `projektfuehrung/` gelistet; 20e, 21a, 21b gelesen. `FABLE_ANTWORT_2026-09-20a_grenzfall.md` liegt dort — die Lücke aus der Nachmessung 13:50 ist geschlossen.
- **Schreiben: ja.** Diese Datei lege ich selbst unter `projektfuehrung/` ab. Die zurückgezogene Bitte könnt ihr damit wieder aufnehmen; Meldung „Fable ist fertig" genügt.
- **Das Register: weiterhin nein.** Es liegt im Repo, nicht in der Projektablage. Der Mac ist an diese Sitzung angebunden, aber ohne freigegebenen Ordner — gemessen, nicht angenommen. „Fable kann das Register nicht lesen" ist also eine Aussage über den **Ort des Registers**, nicht über mich. Zwei Wege, beide Handwerk, eure Wahl: (1) Registertext (oder die Abschnitte 4a, 4d, 5a, 6b, 7, 23–26 und Festlegungen 10–12) in die Projektablage legen; (2) den Ordner `~/trading-bot` für diese Sitzung freigeben. Bis dahin gilt meine Regel aus 21b unverändert: Aktenzeichen nur, wo ihr sie mir im Wortlaut vorlegt.

## 3. Widersprüche

### 3.1 Ein Satz ist zwischen 20e und 21a verloren gegangen — Entscheidung

Die 4a-Präzisierung vom 20.09. (20e) endet mit:

> „Der Vorlauf wird gegen dieses Datum gerechnet, nicht gegen den ersten Kurs im Bestand."

Die Fassung vom 21.09. (21a, in der Übergabe als (d)) trägt den Vermerk „ersetzt die Fassung vom 20.09." — und **enthält diesen Satz nicht mehr.** In einem append-only-Register bekommt er damit eine ERSETZT-Marke, ohne dass irgendwo ein Grund dafür steht. Ob ich ihn damals absichtlich fallengelassen habe, weiss ich nicht; 21a nennt keinen Grund, und ohne Grund ist es keine Rücknahme, sondern ein Versehen.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **4a, Präzisierung, Ergänzung:** Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand. Der Satz aus der Fassung vom 20.09. gilt fort; die Fassung vom 21.09. hat ihn nicht ersetzt, sondern ausgelassen.

*Quelle des Grundes:* 21a selbst nennt einen Zugriff auf Zeiten vor dem Horizont „einen Lesezugriff auf Zeiten ausserhalb des registrierten Horizonts". Ein Vorlauf, der auf Kursen vor dem Horizontbeginn rechnet, ist derselbe Zugriff. Kategorie: **Berichtigung** (Registertext an Registertext).

*Bekannte Wirkung auf die Zulässigkeit:* Der Satz entscheidet, ob die erste Falte eines Aktien-Bots 2017 oder 2018 ist (Horizontbeginn 19.09.2016; ein Vorlauf, der bis zum 1.1.2017 nicht voll ist, schiebt auf 2018). 20e beschreibt den Plan als „2017/2018" — das passt zur Fassung **mit** dem Satz. **Bitte messen,** ob `faltenplan.json` (0e54ac5c…) den Vorlauf gegen den Horizontbeginn rechnet. Wenn ja, ändert sich nichts. Wenn nein, ist der Plan zu berichtigen, nicht der Satz.

### 3.2 Zwischen Horizontbeginn und erster Falte liegt eine Lücke — Regel vor der Messung

(d) verbietet Einstiege **vor dem Horizontbeginn** (19.09.2016). Die erste Falte beginnt am **1. Januar** 2017 oder 2018. Dazwischen liegen dreieinhalb bis fünfzehn Monate, in denen ein Einstieg nach (d) zulässig ist, in keiner Falte auftaucht — und durch den Kapitalpfad läuft. Das ist genau der Schaden, mit dem (d) begründet wurde („verändern das Kapital, mit dem die erste Falte beginnt"), nur kürzer. Die Wache aus (g) sieht ihn nicht, weil sie gegen den Horizontbeginn prüft.

Dasselbe kann bei Krypto auftreten, wo (i) wegen des Vorlaufs später liegt als der erste handelbare Tag (rsi2_crypto: 2018 handelbar, erste Falte 2019).

Ob es wirklich auftritt, hängt an der Frage, die ich in 21a schon als **unsicher** markiert hatte: wo der Kapitalpfad der Optimierer beginnt. Ich schreibe die Regel deshalb jetzt, **bevor** gemessen wird — dieselbe Bauart wie 24.3:

> **Vorschlag Registertext (zu 4a / 26):** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese Regel ohne Belang.
>
> **Wache (TB-30b), angepasst:** frühester Einstieg ≥ Beginn der ersten Selektionsfalte (nicht nur ≥ Horizontbeginn). Der Bericht führt je Bot drei Daten nebeneinander: Horizontbeginn, Beginn der ersten Falte, frühester Einstieg.

*Quelle des Grundes:* 4a (Falten sind ganze Kalenderjahre) und der Grund von 26 (kein Trade ausserhalb aller Falten im Kapitalpfad). Kein Ergebnis.

**Zu messen, danach:** (1) wo der Kapitalpfad der neun Optimierer heute beginnt; (2) ob es in den vorhandenen Trade-Listen Einstiege zwischen Horizontbeginn bzw. erstem handelbarem Tag und dem 1. Januar der ersten Falte gibt. Nur das **Ob**, nicht die Wirkung auf Kennzahlen. Steht im Register bereits ein Satz, der den Beginn des Kapitalpfads festlegt, legt ihn mir im Wortlaut vor — dann ist mein Vorschlag gegenstandslos oder eine Berichtigung dazu, und das kann ich von hier nicht sehen.

Das gehört **vor** „Falten nach 4a ableiten", nicht erst zur Frage nach dem fertigen Faltenplan; deshalb melde ich es jetzt.

### 3.3 Festlegung 11 steht in eurer Ablage zweimal, verschieden

- Nachmessung 13:50 (angehängt an 21a): „Bleibt/Geht über die Abbruchkriterien — **das ist Festlegung 11**."
- 21b und Übergabe (e): „Festlegung 11 ist **‚DSR ist Bericht, nicht Tor'**"; keine Festlegung trägt den Bleibt/Geht-Satz.

Beides kann nicht stimmen. Ich nehme an, die Rückmeldung von 16:24 hat die Tabelle von 13:50 berichtigt — aber **diese Rückmeldung liegt nicht in der Ablage** (es gibt keine ANFRAGE/RUECKMELDUNG 21b), und die Tabelle von 13:50 trägt keine Berichtigungsmarke. Wer aus 21a abschreibt, trägt den Fehler ein — euer eigener Warnsatz, auf euch angewandt. Bitte: Rückmeldung 16:24 wörtlich ablegen; Tabelle 13:50 markieren; mir den Wortlaut der Festlegungen 10–12 einmal vorlegen.

### 3.4 Sonst nichts

(a), (b), (c), (f), (g) und Abschnitt 4 sind untereinander stimmig. Die Reihenfolge in Abschnitt 4 bleibt, mit 3.1 und 3.2 vor dem dritten Schritt:

asof eintragen → Horizontbeginn je Bot → **3.1 eintragen, 3.2 messen und eintragen** → Falten nach 4a ableiten → Faltenplan als Registertext → Tag.

---

**Kurz:** Nichts erinnert, alles nachgelesen, soweit abgelegt; (a)/(b) ungeprüft übernommen. Projektzugriff besteht (lesen und schreiben gemessen — diese Datei); das Register bleibt unlesbar, solange es nur im Repo liegt und kein Ordner freigegeben ist. Entscheidung: der Vorlauf-Satz aus 20e gilt fort. Vorschlag mit Regel vor Messung: Kapitalpfad und erster Einstieg beginnen am 1. Januar der ersten Falte; Wache entsprechend. Festlegung 11 steht bei euch zweimal verschieden; Rückmeldung 16:24 fehlt in der Ablage.

**Unsicher:** ob das Register den Beginn des Kapitalpfads schon regelt (dann 3.2 anpassen); ob ich den Vorlauf-Satz am 21.09. absichtlich gestrichen habe (kein Grund überliefert — ich behandle es als Auslassung).

---

## In einfacher Sprache

Der neue Fable-Chat erinnert sich an nichts aus dem alten — aber er kann die Projektablage lesen und schreiben und hat seine früheren Antworten dort nachgeschlagen. Die Übergabe stimmt mit ihnen überein. Das eigentliche Regelwerk (das Register) kann er weiterhin nicht lesen, weil es nur im Repo liegt; eine Kopie in der Projektablage oder eine Ordnerfreigabe würde das ändern.

Beim Nachlesen sind drei Dinge aufgefallen. Erstens: Ein Satz darüber, ab wann die Anlaufzeit der Indikatoren gezählt wird, ist beim Umschreiben am 21.09. versehentlich weggefallen; er gilt weiter, und er entscheidet, ob das erste Auswertungsjahr der Aktien-Bots 2017 oder 2018 ist. Zweitens: Zwischen dem Stichtag „zehn Jahre zurück" (19.09.2016) und dem 1. Januar des ersten Auswertungsjahres können Käufe liegen, die in keinem Auswertungsjahr zählen, aber das Startkapital verändern. Die Regel dagegen — Start am 1. Januar des ersten Jahres, mit leerem Depot — wird festgeschrieben, bevor nachgemessen wird, ob es solche Käufe gibt. Drittens: In der Ablage steht an zwei Stellen Verschiedenes darüber, was „Festlegung 11" besagt; eine der beiden Stellen braucht eine Korrekturmarke.
