# Projektstand in einfacher Sprache — 26.09.2026, 08:00

*Geschrieben vom steuernden Chat. Quellen: Regelwerk (Register 0–43), Fables Gesamtanalyse 25f, `BACKLOG.md` und `BACKLOG_EPICS.md` (Stand 18.–21.09.), `PLAN_VOR_DEM_TAG.md` (Stand 22.09.). Die Grafik dazu: `projektstand_2026-09-26.png`.*

---

## 1. Worum es geht

Neun Handelsprogramme („Bots“) handeln seit Wochen auf Papier, also ohne echtes Geld: vier mit Aktien, fünf mit Kryptowährungen. Sie sind in vier Gruppen eingeteilt:

| Gruppe | Aktien oder Krypto | Bots |
|---|---|---|
| Trend | Aktien | volatility_breakout |
| Umkehr | Aktien | rsi2_mean_reversion, turtle_soup_stocks, elliott_wave_stocks |
| Trend | Krypto | t3_supertrend, volatility_breakout_crypto |
| Umkehr | Krypto | rsi2_crypto, turtle_soup_crypto, elliott_wave |

„Trend“ heisst: kaufen, wenn es läuft. „Umkehr“ heisst: kaufen, wenn es gerade gefallen ist.

**Das Ziel** ist ein einziger, fairer Auswahllauf. Er beantwortet für jeden Bot die Frage: Hätte er in der Vergangenheit nach Kosten wirklich etwas taugt, oder war das Zufall? Damit sich hinterher niemand etwas schönrechnen kann, werden **alle Regeln vorher festgeschrieben und digital versiegelt** („der signierte Tag“). Erst dann läuft die Auswahl.

**Dein Zweck laut Karte von heute früh:** Hobby mit Methode. Der saubere Lauf ist das Ziel, echtes Geld ist freiwillig.

## 2. Was fertig ist

- **Die Regeln:** 12 Festlegungen von dir (14.09.) und ein Regelwerk mit 43 Abschnitten. Darin steht, wie gemessen wird, wann ein Bot bleibt oder geht, und was mit dem Geld passiert.
- **Die Daten:** Sie sind eingefroren. Der Lauf rechnet mit genau dem Datenstand vom 19.09., und das ist überprüfbar.
- **Die Technik:** Alle neun Bots haben einen **geschützten Modus**. In diesem Modus bricht ein Bot lieber mit einer Fehlermeldung ab, als still auf falsche Daten oder Ersatzwerte auszuweichen. Die letzten Tage gingen fast ganz in diese Absicherung. Sie hat mehrere solcher stillen Fehler gefunden und geschlossen.
- **Das Geld-Konzept:** Jede aktive Gruppe bekommt gleich viel; Aktien und Krypto teilen sich 80 zu 20. Scheidet eine Gruppe aus, geht ihr Geld in eine einfache Vergleichsanlage (Benchmark), nicht zu den anderen Bots.
- **Die Gesamtprüfung durch Fable (25f):** Das Verfahren hält dem Vergleich mit der Fachliteratur stand. Die Schwächen liegen in den **Eingaben**, nicht im Verfahren (siehe Abschnitt 5).

## 3. Was heute läuft

- **TB-111 (Sitzung B)** läuft seit 07:11. Er stellt ein Protokoll-Programm und die Auswertung so um, dass sie im geschützten Modus nur noch „gerechnet“ oder „abgebrochen“ kennen.
- **TB-112 (Hauptordner)** wartet noch darauf, dass du im Terminalfenster Enter drückst. Er erweitert die Startprüfung auf alle 81 Programme, die im Lauf mitlaufen; heute prüft sie nur zwei Ordner. Dazu kommt eine tägliche Sicherung der Paper-Datenbanken nach iCloud.

## 4. Was bis zum Tag noch fehlt

Nach Fables Schätzung **10 bis 14 Aufträge**. Bei zwei bis drei Aufträgen am Tag sind das grob **ein bis zwei Wochen**; das ist eine Schätzung, keine Zusage. Die äusserste Frist ist der 13.12.2026.

1. TB-111 und TB-112 zusammenführen und ins Regelwerk eintragen.
2. **Der „Erzeuger“:** das Programm, das den Lauf wirklich rechnet. Es ist der grösste offene Brocken, zwei bis vier Aufträge, und sein Umfang ist noch nicht gemessen.
3. Zwei alte Fehlerkorrekturen (TB-30b), die vor dem Lauf eingebaut sein müssen.
4. Die Budget-Leiter als Programm, samt einer Prüfung aller 19 683 möglichen Fälle.
5. Ein Vergleichswerkzeug: Papierhandel gegen Simulation.
6. Einmal die ganze Kette von vorne bis hinten durchspielen.
7. Der Prüfgang mit einem zweiten Leser, dann deine digitale Signatur. Danach ist „der Tag“.

## 5. Kann das live gut laufen? Ehrlich gesagt: offen

Eine Vorhersage kann und darf ich nicht machen. Die Regeln verbieten es sogar, dass der Prüfer Ergebnisse vor dem Tag sieht. Was man sagen kann, ist, **was gegen ein gutes Live-Ergebnis spricht und was dafür**:

**Was dagegen spricht (aus Fables Analyse, mit Quellen dort):**
- **Rückblicke sind fast immer schöner als die Zukunft.** In einer grossen Studie mit 888 Handelsprogrammen erklärte das Rückblick-Ergebnis weniger als 2,5 % des späteren echten Ergebnisses.
- **Die Aktien- und Kryptolisten sind die von heute.** Firmen und Coins, die zwischendurch pleite gingen oder gestrichen wurden, fehlen. Das macht Rückblicke zu gut. Bei Krypto ist der Effekt besonders gross.
- **Die Gebühren im Modell sind Binance-Gebühren.** Binance darf seit 1.7.2026 für Kunden in der EU nicht mehr handeln. Die erlaubten Börsen kosten das Zwei- bis Achtfache je Kauf oder Verkauf.
- **Steuern** fallen bei kurzen Haltedauern voll an und stehen in keinem Kostenmodell.
- **Drei der fünf Krypto-Bots handeln „Umkehr“** auf den liquidesten Coins. Genau dort findet die Forschung eher Trend als Umkehr.

**Was dafür spricht:**
- Das Verfahren ist **strenger als üblich**: kein Nachjustieren, keine Wahl des besten Einzelwerts, alle Versuche gezählt, und „kein Bot schafft es“ ist ausdrücklich ein erlaubtes Ergebnis.
- Ein Bot, der hier besteht, hat einen harten Test bestanden. Das ist mehr, als die meisten Hobby-Systeme je hatten.

**Der Weg zu echtem Geld steht schon im Regelwerk (16.4):**
- Nach dem Lauf läuft der Paper-Betrieb weiter.
- Ein Bot steigt zu „Bestätigt“ auf, frühestens nach 6 Monaten und 30 Trades.
- Echtgeld gibt es erst, wenn er **zwei Quartalsprüfungen in Folge** „Bestätigt“ war, also **nicht vor 2027**.
- Vorher müssen die Börse (Binance fällt weg) und das Kapital entschieden werden.

**Mein Fazit in einem Satz:** Das Projekt misst sehr sauber. Ob am Ende ein Bot echtes Geld verdient, weiss heute niemand, und die Wahrscheinlichkeit ist nach allem, was die Forschung weiss, eher klein. Genau deshalb ist „Hobby mit Methode“ die ehrliche Einordnung.

## 6. Der Backlog — was noch in der Ideensammlung steckt

Der Backlog ist die grosse Sammelliste aller Ideen und Aufgaben, gut 200 KB, grob hundert Seiten Text.

**Nein, die innovativen Themen sind nicht abgearbeitet. Das ist Absicht:** Alles, was die Auswahl verändern würde, darf erst **nach** dem Tag kommen, sonst wäre der Lauf nicht mehr fair.

| Stand | Zahl | Beispiele |
|---|---|---|
| **offen oder geparkt** | 26 (davon 5 grosse Vorhaben) | ETF-Trend über Anlageklassen (Anleihen, Gold, Aktien weltweit) · Insiderkäufe (Form 4) · Short über inverse ETFs · Aktien-Universum ohne Überlebende-Verzerrung · Regime-Filter · variable Positionsgrösse |
| **verworfen** | 18 | Carry/Funding (am Wohnsitz nicht erlaubt) · Hebelprodukte · Sentiment · ein Sprachmodell, das selbst handelt · „mehr Bots“ |
| **erledigt** | 4 | Kalendereffekt (geprüft und durchgefallen) · Aufteilung Aktien/Krypto · Volatilitäts-Skalierung · Kill-Test-Werte |

**Die fünf grossen Vorhaben („Epics“), alle bewusst nach dem Tag, in dieser Reihenfolge:**
1. **Forschungspipeline:** neue Strategien automatisch prüfen, jeder Versuch wird gezählt.
2. **Angriffs-Labor:** Bots gezielt zu brechen versuchen.
3. **Alpha-Labor:** Hypothesen mit Vorhersage-Buch.
4. **Kausalgraph:** Zusammenhänge zwischen Märkten.
5. **KI-Marktbild:** Marktlage erkennen und das Geld darauf verteilen.

**Vor dem Tag** stehen aus dem Backlog nur drei Dinge an: die Budget-Leiter, ein Nachtrag zum ETF-Trend und Vorarbeit zu den Insiderkäufen.

⚠️ Der Backlog ist zuletzt am 21.09. gepflegt worden. Einiges aus den letzten Tagen fehlt dort, etwa der Binance-Wegfall und Fables 51 neue Ideen. Das Nachtragen wäre ein kleiner Auftrag.

## 7. Was wir tun sollten — meine Empfehlung

**Jetzt bis zum Tag:**
- Den Weg aus Abschnitt 4 gehen, gebündelt, zwei bis drei Aufträge am Tag.
- Eine gesammelte Frage an Fable pro Tag.

**Nach dem Tag:**
1. Den Bericht lesen und annehmen, auch wenn er „kein Bot“ sagt.
2. Paper-Betrieb weiterlaufen lassen und die Bestätigung abwarten.
3. **Durchgang 2** vorbereiten, mit den drei grössten Hebeln aus Fables Analyse:
   - echte Gebühren einer erlaubten Börse;
   - Aktien- und Kryptolisten „wie damals“;
   - dazu als neue Gruppe der ETF-Trend über Anleihen, Gold und Aktien. Das ist die Strategiefamilie mit der längsten Erfolgsgeschichte in der Forschung.
4. Erst danach über echtes Geld reden: Börse, Betrag, Steuerberatung.

## 8. Deine nächsten Handgriffe

1. **Im Terminalfenster des Wächters Enter drücken**, damit TB-112 startet.
2. Wenn TB-111 fertig ist, schliesst du sein Fenster. Ich sage dir Bescheid.
3. Bei Gelegenheit: die zwei Crontab-Zahlen und bis 29.09. den Speicher-Export.
