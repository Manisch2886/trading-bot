# FABLE_ANTWORT 2026-09-24d — Bestätigung des Umzugs; die Purge-Berichtigung schrumpft auf einen Deckel bei einem Bot; ein sechster eigener Fall; der Benchmark-Nachweis ist schon nach 39.8 ein 2; ein Modus-Weg, nicht zwei

*Bezug: `FABLE_UEBERGABE_2026-09-24_neuer_chat.md` (Abschnitte 6 und 9), `UEBERGABE_2026-09-24.md` Block 5, meine Antworten 24b und 24c. Neuer Chat, gleiche Rolle. Reihenfolge: erst die drei Bestätigungen aus Abschnitt 9, dann die drei Messungen mit den zwei Rückfragen.*

---

## 0. Bestätigung (Abschnitt 9)

**Was ich aus Abschnitt 5 „noch habe":** nichts aus eigener Erinnerung — dieser Chat beginnt bei null. Ich habe 24b und 24c in der Ablage vollständig gelesen; eure Zusammenfassung in Abschnitt 5 trifft beide in der Sache. Zwei Stellen sind in der Zusammenfassung kürzer als im Wortlaut, und beide werden unten wichtig: (4) — 24c sagt zum Purge zusätzlich *„wo eine Strategie keinen begrenzten Ausstiegshorizont hat, aus dem Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag"*; und 24c führt am Ende zwei **Unsicherheiten** und in Abschnitt 5 **eine Frage** — genau die drei, die ihr gemessen habt.

**Registerkopie:** `REGISTER_KOPIE_2026-09-24.md` liess sich öffnen. ⚠️ **Aber mein Lesewerkzeug hat nur die ersten 262 144 von 552 130 Bytes geliefert** — das ist der Kopf der Kopie und das Register vollständig von Abschnitt 0 bis in den Anfang von **25.1**. Die Abschnitte 25.1 (Rest) bis 40 habe ich **nur als Suchausschnitte** gelesen, nicht am Stück: 38.2, den Kopf von 39, 39.5, 39.6, 39.8 samt Nachtrag, 39.10, 40.5, 40.6, Teile von 40.7 und 40.9, 40.8, 40.10. Ob 37 bis 40 „neu für mich" sind, kann ich nur so beantworten: in diesem Chat ist alles neu; dass die alte Kopie bei 36 endete, nehme ich als eure Tatsache. **Für die Tatsachennotiz zu 27 gilt deshalb: mein Anfangsbestand ist der Umzugstext, die Kopie bis 25.1 vollständig, 25.1–40 in Ausschnitten, dazu 24b, 24c und die Übergabe.** Handwerksbitte, keine Anordnung: legt die Kopie in zwei Teilen ab (0–25 und 26–40), dann lese ich den Rest ganz.

**Leseprotokoll dieses Chats, Stand jetzt:** vollständig gelesen — der Umzugstext (Anhang), `REGISTER_KOPIE_2026-09-24.md` bis 25.1, `FABLE_ANTWORT_2026-09-24b_…`, `FABLE_ANTWORT_2026-09-24c_…`, `UEBERGABE_2026-09-24.md`. Als Suchausschnitte gelesen — Register 25.1–40 wie oben; dazu Ausschnitte aus `auftraege/MAC_TB-89_register_38.md` und `auftraege/MAC_TB-94_register_39.md` (Auftragstext, keine Ergebnisgrössen), `FABLE_ANTWORT_2026-09-23e`, `…23f`, `FABLE_ANFRAGE_2026-09-24a`, `…24b`, `…24e`. **Nicht gelesen:** `BACKLOG.md`, `belege/`, `ergebnisse/`, Trade-Listen, `SITZUNGSWAECHTER_…`, `NACHTRAG_ARBEITSWEISE_6d_…`, `PLAN_VOR_DEM_TAG.md`, `ARBEITSWEISE.md`, `UMZUG.md`. Ergebnisgrössen nach 27.1 sind mir in keinem Ausschnitt begegnet; was ich an Zahlen gesehen habe, ist Benchmark-, Falten- und Datenbestandsseite (27.2) und die MtM-Wirkung in 24.6, die nach Bauart 24.3 zulässig ist.

---

## 1. Messung (1) — die Purge-Herleitung: eure Messung verkleinert meine Berichtigung, und ich verkleinere sie weiter

**Angenommen, in allen vier Punkten:** 5.1 Nr. 5 ist Registertext; er ist als Verfahren-A-Relikt überholt (Marke am Kopf von 5.1, und 2c: *„Zwischen Selektionsfalten gibt es weder Purge noch Embargo"*); bei acht Bots ist der Deckel aus 2d eine Konstante im Code; nur bei `t3_supertrend` und der Donchian-Untergrenze hängt eine Grösse an ausgeführten Trades.

**Dann geht der Befund aber noch einen Schritt weiter, und er kostet meine Berichtigung ihren Gegenstand.** Ich habe in 24c „Purge" mit „Deckel" verwechselt. Ein Purge ist eine **Lücke**, die Beobachtungen aus dem Test entfernt — und meine Sorge war, dass eine zu kurze Lücke Zellen mit langen Haltedauern bevorzugt, weil deren Trades über die Lücke hinweg lecken. **2d in der Fassung 16.6 hat keine Lücke.** Es hat eine Bedingung am Bestand (die Periode beginnt, wenn keine vor der Grenze eröffnete Position mehr offen ist), einen Deckel — und den entscheidenden zweiten Absatz: *„Ist am Deckeltag noch eine vor Go-Live eröffnete Position offen, beginnt die Bestätigungsperiode trotzdem — diese Position wird in der Bestätigungsstatistik jedoch nicht gezählt."* Das Leck schliesst die **Attribution je Position**, nicht die Länge des Deckels. Eine Zelle mit längeren Haltedauern als der Deckel verliert nichts und gewinnt nichts: ihre grenzüberschreitende Position zählt nicht, ihre Periode beginnt am Deckeltag. Der Deckel bestimmt nur, **wie spät** die Periode spätestens beginnt. Meine Begründung aus 24c („ein zu kurzes Purge bevorzugt systematisch Zellen mit langen Haltedauern") trifft 2d also nicht — sie träfe ein Purge, und das gibt es unter Verfahren B nicht mehr.

> **Rücknahme (zu 24c, „Berichtigung zu 2d (Purge/Embargo), Herleitung"):** Der Satz *„`purge_tage` wird … als Schranke über das registrierte Raster bemessen"* ist zurückgenommen. Unter Verfahren B gibt es zwischen Selektionsfalten weder Purge noch Embargo (2c) und vor der Bestätigungsperiode keine Lücke, sondern Bedingung plus Deckel mit Attribution je Position (16.6). Eine Grösse, die eine Trainingsgrenze oder eine Lücke bemisst, gehört zu Verfahren A und wird **nicht neu hergeleitet**.

*Quelle des Grundes:* 2c und 16.6 im Wortlaut. Kein Ergebnis.

**Was von der Berichtigung bleibt, ist der Deckel — und nur dort, wo er aus ausgeführten Trades stammt.** Bei acht Bots ist er die Zeitbremse, und 2.6 nennt sie eine *„festgeschriebene Konstante des Laufs"*: dieselbe Zahl in jeder Zelle, weder vom Positionslimit noch von der Ausführung abhängig. **Das ist bereits die Schranke über das Raster, die ich verlangt hatte** — ihr habt es richtig gesehen, und es steht als Registertext, nicht nur im Code. *[Voraussetzung, zu messen: dass die Zeitbremse in jeder Rasterzelle wirkt — kein Stufenwert einer Achse, etwa „kein Stop", schaltet sie ab. Das ist am Backtest-Code lesbar, nicht am Ergebnis.]* Bei `t3_supertrend` ist der Deckel das 95. Perzentil der Haltedauer plus 1 aus 656 **ausgeführten** Positionen (15.4, Tabelle zu 2d; Anmerkung 4 zur Aufrundung). Der Registertext 16.6 sagt *„95. Perzentil der Haltedauer"* — er sagt nicht, welcher Trades. Dort gehört das Wort hin:

> **Präzisierung zu 2d (Fassung 16.6), Deckel für Bots ohne Zeitbremse:** Das 95. Perzentil der Haltedauer wird aus den **gefundenen** Trades gerechnet (Signalpfad, die neuen Listen nach 24b A3 / 24c), plus 1, aufgerundet wie in 15.4 Anmerkung 4; Tatsachennotiz mit Hash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Position —, und er ist deshalb ausdrücklich **nicht** als Maximum über alle Rasterzellen zu bemessen. Der Zusatz aus 24c *„Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag"* ist zurückgenommen.

*Quelle des Grundes:* 24c, Registertext „Reichweite des Grundsatzes aus 5.4" (Herleitungen aus Trades verwenden gefundene Trades) — und TB-98 Befund 2: ausgeführte Positionen sind seit TB-26 nicht reproduzierbar erzeugbar, gefundene sind es. Die Wirkung kenne ich nicht (der Wert 13 kann sich bewegen); sie beschränkt sich auf den spätesten Beginn der Bestätigungsperiode des Gewinners. Kein Ergebnis.

**Damit zu eurer Rückfrage — obere Schranke oder Bedingung:** **Die obere Schranke**, und nur bei dem einen Bot, bei dem sie nicht Konstante ist. Die Bedingung ist keine Herleitung, sondern eine Beobachtung je Position; auf sie wendet man keine Schranke an. Aber die Frage hat mir eine Lücke gezeigt, die ich schliessen will, bevor jemand den Laufcode schreibt: 16.6 sagt *„Der Tag wird aus den Positionsdaten bestimmt und im Journal vermerkt."* Das lässt zwei Lesarten zu — aus dem Papierjournal des Live-Bots (heutige Parameter, ein Parameterstand, **ausgeführte** Positionen) oder aus den Positionen der Zelle, die bewertet wird. Nur die zweite passt zu Verfahren B: Die Bestätigungsperiode wird einmal ausgewertet, nachdem die Auswahl steht (5.1 Nr. 7), also für den Gewinner — und dessen Positionen kennt der Lauf, nicht das Journal.

> **Präzisierung zu 2d (Fassung 16.6), Auswertungsebene:** Die Bedingung wird im Selektionslauf **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet; der Deckel ist je Bot eine Konstante über alle Zellen. Das Journal des Papierpfads ist dafür keine Quelle. *(Ob der heutige Code eine der beiden Lesarten schon umsetzt, ist nicht gemessen; nach 24.5 existiert der Laufcode, der die Tagesreihe je Zelle erzeugt, nicht.)*

*Quelle des Grundes:* 5.1 Nr. 7 und 15.1 (Verfahren B: Out-of-Sample ist allein die Bestätigungsperiode — des gewählten Satzes). Kein Ergebnis.

**Und `purge_tage` in `messgroessen.json` → „Trainingsende":** Unter Verfahren B gibt es kein Trainingsfenster (4a, 15.1). Ein Wert namens Trainingsende ist ein Verfahren-A-Rest; `faltenplan.json` (`0e54ac5c…`) ist registrierter historischer Stand, den *„der Lauf nicht liest"* (Sperrliste Punkt 2, Tatsachennotiz 30). **Messbitte, nur das Ob:** Liest irgendeine Grösse, die der Lauf oder die Benchmark-Tabelle verwendet, heute `purge_tage`? Wenn nein — Tatsachennotiz „historischer Stand", und `G8` prüft ein Relikt; ob man die Prüfung dann ehrlich beschriftet oder stilllegt, ist Handwerk (nicht löschen — 23a gilt, aber eine Prüfung eines Relikts ist als solche zu benennen). Wenn ja — der Leser ist ein Verfahren-A-Rest im Laufbereich und wird an 2c/4a angeglichen (Berichtigung Code an Registertext), **nicht** mit einer neuen Herleitung versorgt. Meine Zeile in 24c Abschnitt 5 („G8 prüft künftig das aus dem Raster geschrankte `purge_tage`") ist damit zurückgenommen.

**Donchian-Untergrenze (zwei Bots):** bleibt wie in 24c — `median_balken` der gefundenen Trades. Das ist keine Schranke über das Raster und muss keine sein: Die Haltedauer ist eine der vier zulässigen Grundlagen aus 2.2, und Grundlagen werden nach 2.1 auf dem registrierten heutigen Parameterstand gemessen, wie σ und ATR. Nur die Eingabe wechselt auf den Signalpfad.

**Bilanz eurer Zählung „genau zwei Stellen":** Ich komme auf **zwei plus eine Präzisierung** — `t3_supertrend`-Deckel, Donchian-Eingabe, und die Auswertungsebene der Bedingung. Das dritte ist keine Herleitung, sondern eine Lesart, die vor dem Laufcode festgezurrt gehört.

---

## 2. Messung (2) — kein Bot hat einen Ausstiegshorizont als Rasterachse

**Angenommen.** Meine Anordnung *„aus den registrierten Rastergrenzen der Ausstiegsachsen"* war für keinen Bot ausführbar. Ich hatte die Voraussetzung in der Unsicher-Zeile genannt — aber der Registertext-Entwurf selbst trug sie unmarkiert. Das ist der **sechste** Fall meiner Klasse, in einer neuen Form: Die Voraussetzung stand ausserhalb des Textes, der ins Register gegangen wäre.

> **Regel an mich, ergänzt:** Eine Voraussetzung, von der ein Registertext-Entwurf abhängt, steht **im Entwurf selbst** als *[Voraussetzung, zu messen]* — nicht nur in der Unsicher-Zeile darunter. Ein Entwurf, der ohne die Zeile darunter ins Register gelangt, trägt die Annahme als Tatsache.

Die Folge ist die, die ihr genannt habt, und ich habe sie in Abschnitt 1 gezogen: Bei acht Bots ist die Zeitbremse Konstante und damit dieselbe Schranke in jeder Zelle; bei `t3_supertrend` kommt der Deckel aus gefundenen Trades — nicht als Maximum, sondern nach der Regel, die 16.6 schon hat (P95 + 1), weil der Deckel kein Leckschutz ist.

**Zum Nebenbefund `elliott_wave`:** richtig — bei ihm ist das Positionslimit keine Achse (2.4: keine Limitachse, Kapitalschranke `floor(1/ALLOCATION_PCT) = 10`). Der Grundsatz greift dort über das zweite Wort im Registertext aus 24c, *„oder von der Ausführung"*: Die Zuteilung entscheidet auch bei ihm, welche gefundenen Trades ausgeführt werden, und die Kapitalschranke ist eine Ausführungsgrösse. Der Registertext braucht keine Ergänzung; die Tatsachennotiz zu 5.4 sollte den anderen Grund nennen, damit niemand bei diesem Bot „gefundene" für überflüssig hält.

---

## 3. Messung (3) — der Nachweis für die Benchmark-Tabelle, und ein Widerspruch zwischen eurer Messung und dem Register

**Erst mein Fehler, dann der Widerspruch.** Ich habe in 24c „TB-91 A1b" geschrieben. Das Register nennt den Modus-Nachweis der Benchmark-Tabelle **TB-92 A1b** (Kopf von 39.6: *„Fable 23e, TB-92 A1b"*; 39.5: `benchmark.py` `3960375a…` → `d6bdd558…` ist TB-91, die Neurechnung). Eine Auftragsnummer, nicht gemessen — dieselbe Klasse wie TB-94/TB-96 in 24a. **Angenommen; siebter Fall.** Ihr habt konsequenterweise in den TB-91-Belegen gesucht.

**Der Widerspruch:** Ihr schreibt *„Der Lesehaken entstand erst mit TB-95."* Das Register sagt in 39.6 (Tabelle, Zeile „Lesequellen") über TB-92 A1b: *„Lesehaken über `sys.addaudithook`, in Lauf 3 und 4 prozessübergreifend über `sitecustomize` (11 Prozesse): 0 Lesezugriffe auf `data/` oder `config/` des Repos; 222 CSV und 2 Universumsdateien aus dem Snapshot. Dazu Eingaben ausserhalb des Snapshots — 39.8"* — und 39.8 heisst *„Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand"* und nennt als Beleg `docs/belege/TB-92/a1b_lesequellen_kinder.txt`. **Das habe ich im Register gelesen, nicht im Repo gemessen.** Eines von beiden stimmt nicht: entweder existiert dieser Beleg mit diesem Inhalt (dann ist eure Aussage falsch und der Haken ist vom 23.09., TB-92), oder er existiert nicht (dann ist 39.6 falsch, und das wäre ein Registerbefund). *[Voraussetzung, zu messen: `docs/belege/TB-92/a1b_lesequellen_kinder.txt`, Lauf 3 und 4.]*

**Für die Sache ändert das die Grundlage, nicht das Ergebnis — und es macht das Ergebnis fester:** Wenn 39.6/39.8 stimmen, hatte der Nachweis der Benchmark-Tabelle ein Leseprotokoll, **und dieses eigene Protokoll zeigt zwei Eingaben ausserhalb des Snapshots** (`messgroessen.json` und die neun Listen). Nach der Zwei-Teile-Regel aus 24c ist er damit **2** — unmittelbar aus 39.8, ohne den Umweg über TB-95. Eure Schlussfolgerung ist dieselbe; sie hängt dann nicht mehr an einer Messung, die einen anderen Lauf-Typ betrifft.

**Behebbar wann — eine Korrektur an eurem „hinter Plan-Punkt 3":** Der Nachweis hat **zwei** Eingaben ohne registrierten Eingabestand, nicht eine. Die neun Listen bekommen ihren Stand mit Plan-Punkt 3; `messgroessen.json` bekommt ihn erst mit „`messgroessen.json` neu" in Plan-Punkt 5 (TB-101). Der Nachweis der Benchmark-Tabelle gehört deshalb **hinter beide** — und er ist dann nicht nur ein Nachweis, sondern eine Neurechnung: Die Tabelle `64fb2912…` wurde mit den alten Eingaben gerechnet; nach 39.8 erreicht sie aus den Listen nur die Faltenlänge, was aus `messgroessen.json` sie erreicht, ist nicht gemessen. Also: Eingaben registriert → Tabelle neu erzeugt (Erzeuger unter 36.1, `--ziel`) → Vergleich gegen `64fb2912…` → beide Nachweisteile → Tatsachennotiz. Bytegleich ist der erwartete, nicht der geforderte Ausgang; verschieden ist der planmässige Fall nach 37.3 mit neuem Hash und neuem Abbild. Das ist derselbe Vorgang wie „Faltenlänge gegen 33.2" — eine Tabelle, die dem Plan folgt (39.2–39.4), wird mit dem Plan neu geprüft.

**Zu eurer Rückfrage — Hilfsordner oder nur `TB_SELEKTIONSWURZEL`:** **Nur der Resolver-Modus.** Ihr neigt zum Zweiten; ich entscheide es so, aus drei Gründen, von denen keiner die Bequemlichkeit ist:

> **Registertext, Ergänzung zu 5e und zur Resolver-Pflicht (24c):** Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers (`shared/paths.py`, `TB_SELEKTIONSWURZEL`). Eine Anordnung des Snapshot-Inhalts in Repo-Form — Verknüpfungen, Hilfsordner, Ersatzwurzeln wie `TB30A_BASE_DIR`, `TB36_BASE_DIR`, `TB40_BASE_DIR` — ist **kein Modus-Lauf** und trägt keinen Nachweisteil (b). Ein Modul, das den Resolver nicht kennt, hat keinen Nachweis (2), bis es ihn kennt; ein Hilfsordner ersetzt den Resolver nicht. Als **Messwerkzeug** ausserhalb eines Nachweises (Störproben, Diagnose) bleibt die Anordnung zulässig und wird als solche benannt.

*Quelle des Grundes:* (1) 23e: *„der Nachweis muss denselben Weg gehen wie der Lauf"* — der Lauf am Tag geht durch den Resolver; ein Hilfsordner prüft den **Inhalt** des Snapshots, nicht den **Weg** dorthin, und TB-98 Befund 1 war ein Fehler des Weges bei richtigem Inhalt. (2) Das Verknüpfungsskript des Hilfsordners ist selbst Pfadlogik ausserhalb des Resolvers — genau der Befund 1 der Lesequellen-Sonde, nur ausserhalb des Repos, wo die Sonde ihn nicht sieht. (3) 24c: eine Anordnung, ein Ort, der sie kennt. Kein Ergebnis.

**Tatsachennotiz dazu, damit niemand alte Läufe umdeutet:** TB-92 A1b (39.6: *„`TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` nicht (0 Treffer)"*) und TB-95 D1 waren nach dieser Regel beide Hilfsordner-Läufe. Ihre Ergebnisvergleiche bleiben Tatsachen (fünfmal `64fb2912…`); als Nachweise sind sie 2 — aus zwei Gründen, von denen 39.8 der ältere ist.

**Und eine Folge für Plan-Punkt 2, die keine Umstellung ist:** 39.8 nennt vier Leser, die am Resolver vorbeigehen — `benchmark.py` (`TB30A_BASE_DIR`), `messgroessen.py`, `faltenplan_neun.py` (`TB36_BASE_DIR`), `universum_trockenlauf.py`/`loaderlauf.py` (`TB40_BASE_DIR`). Plan-Punkt 2 heisst „`messgroessen.py` auf den Resolver"; nach der Resolver-Pflicht heisst er **„alle Leser des Laufbereichs auf den Resolver"**, und die vier sind die gemessenen. Ob es mehr sind, sagt die Lesequellen-Sonde; das ist Handwerk. Die Reihenfolge 1–5 bleibt.

---

## 4. Was daraus auf den Plan und in Register 41/42 kommt

**Plan (Reihenfolge aus 24c unverändert, drei Präzisierungen):**

1. Resolver — unverändert (24b A2).
2. **Alle** Leser des Laufbereichs auf den Resolver (gemessen vier, 39.8); Haltedauer-Quelle auf die neuen Listen.
3. Erzeuger auf dem Signalpfad — unverändert (24b A3, 24c: `exit_time`, `haltedauer_balken`).
4. Register 41/42 — Liste unten.
5. Danach: Faltenlänge gegen 33.2 · `messgroessen.json` neu · Raster nachziehen · **Benchmark-Tabelle neu und Nachweis mit beiden Teilen (nach 3 und nach `messgroessen.json` neu)** · `t3_supertrend`-Deckel neu als Tatsachennotiz · Abbild.

**Register 41/42, zusätzlich zu 24c Abschnitt 6 Punkt 4:**

| | Eintrag | Art |
|---|---|---|
| a | Rücknahme „`purge_tage` als Schranke über das Raster" (Abschnitt 1) | Rücknahme eines noch nicht eingetragenen Textes — mit Grund eintragen, damit die Ablage nicht zwei Fassungen führt |
| b | Präzisierung 2d/16.6, Deckel aus gefundenen Trades (P95 + 1), kein Maximum über das Raster | Registertext |
| c | Präzisierung 2d/16.6, Auswertung der Bedingung für den Gewinner auf dessen Positionen | Registertext |
| d | Tatsachennotiz zu 5.4: bei `elliott_wave` greift „gefundene" über die Ausführung, nicht über das Positionslimit | Tatsachennotiz |
| e | `purge_tage`/„Trainingsende": nach Messbitte entweder historischer Stand oder Leser an 2c/4a angeglichen | hängt an der Messung |
| f | Registertext „Modus-Lauf = Resolver-Modus; Hilfsordner kein Nachweis" (Abschnitt 3) | Registertext |
| g | Tatsachennotiz: TB-92 A1b und TB-95 D1 waren Hilfsordner-Läufe; als Nachweise 2 (39.8; Abschnitt 3) | Tatsachennotiz |
| h | Berichtigung an 24c: „TB-91 A1b" lies „TB-92 A1b" | Berichtigung |
| i | Der Widerspruch „Lesehaken erst TB-95" gegen 39.6/39.8 — nach Messung eingetragen, in welche Richtung er aufgeht | nach Messung |

---

**Kurz:** Umzug bestätigt; die Registerkopie war für mich nur bis 25.1 am Stück lesbar, 25–40 in Ausschnitten — das gehört in die Tatsachennotiz zu 27. Eure drei Messungen sind angenommen, und die erste verkleinert meine Berichtigung stärker, als ihr sie verkleinert habt: Unter Verfahren B gibt es kein Purge, und 2d schliesst das Leck durch Attribution je Position, nicht durch einen Deckel — meine Begründung aus 24c traf ein Purge, das es nicht mehr gibt. Übrig bleibt der Deckel bei `t3_supertrend` (aus gefundenen Trades, P95 + 1, kein Rastermaximum), die Donchian-Eingabe, und eine Präzisierung, dass die Bedingung für den Gewinner auf dessen Positionen ausgewertet wird. Zwei eigene Fälle dazu: die Voraussetzung „Ausstiegsachsen" stand nicht im Entwurf selbst (sechs), und „TB-91 A1b" hiess TB-92 A1b (sieben). Zu (3): Das Register sagt in 39.6/39.8, dass TB-92 A1b einen Lesehaken **hatte** — das widerspricht eurem „erst mit TB-95"; messen. So oder so ist der Benchmark-Nachweis ein 2, und zwar schon aus seinem eigenen Protokoll; behebbar erst, wenn **beide** Eingaben ausserhalb des Snapshots registriert sind, dann als Neurechnung mit beiden Nachweisteilen. Hilfsordner: kein Modus-Lauf mehr, nur der Resolver-Modus; als Messwerkzeug zulässig, als Nachweis nicht.

**Unsicher:** (1) ob `purge_tage` heute irgendeinen Leser im Laufbereich hat — davon hängt Eintrag e ab; (2) ob die Zeitbremse in jeder Rasterzelle der acht Bots wirkt; (3) ob `docs/belege/TB-92/a1b_lesequellen_kinder.txt` das enthält, was 39.6 sagt; (4) ob 16.6 mit „Journal" den Papierpfad meinte — dann ist Eintrag c eine Berichtigung, nicht nur eine Präzisierung.

---

## In einfacher Sprache

Der neue Chat hat gelesen, was er lesen sollte — mit einer Einschränkung: Das Regelwerk war für ihn nur bis etwa zur Mitte am Stück lesbar, der Rest in Ausschnitten. Das steht hier, damit es festgehalten wird.

Zur Sache: Ich hatte am Abend eine Regel über die „Sperrfrist" zwischen Zeitabschnitten geschrieben. Eure Nachmessung zeigt: Diese Sperrfrist gibt es im heutigen Verfahren gar nicht mehr, und dort, wo eine ähnliche Frist noch existiert, wird das Problem, das mich beunruhigt hat, schon anders gelöst — jede Position, die über die Grenze hängt, wird einfach nicht mitgezählt. Meine Regel wird zurückgenommen. Was bleibt, ist klein: Bei einem einzigen Bot wird eine Frist aus Zahlen berechnet, die vom Ausführungsweg abhängen; sie wird künftig aus den gefundenen Signalen berechnet. Und ein Satz im Regelwerk lässt zwei Lesarten zu, welche Positionen gemeint sind — das wird festgelegt, bevor das Programm geschrieben wird.

Zwei eigene Fehler kommen dazu: eine Annahme, die ich nur unter dem Text statt im Text genannt hatte, und eine falsche Auftragsnummer. Und ein Widerspruch zwischen eurer Messung und dem Regelwerk: Das Regelwerk sagt, ein Protokoll, das ihr für nicht existent haltet, habe existiert. Das muss jemand nachsehen. Am Ergebnis ändert es nichts — der fragliche Nachweis gilt so oder so als nicht geführt, und er kann erst wiederholt werden, wenn beide seiner ungeregelten Eingaben geregelt sind. Schliesslich: Es gibt künftig nur noch einen zulässigen Weg, ein Programm im geschützten Modus laufen zu lassen — den zentralen Pfadgeber. Behelfsordner sind als Messwerkzeug erlaubt, als Nachweis nicht.
