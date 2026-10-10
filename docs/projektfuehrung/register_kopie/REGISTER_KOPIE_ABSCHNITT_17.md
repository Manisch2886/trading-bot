# REGISTER-KOPIE Abschnitt 17 (von 0–56) — Register-Z. 2584–3040 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 17. Registernachtrag (TB-48, 18.09.2026)

### 17.0 Was das ist — und was es ausdrücklich nicht ist

**Das ist kein Amendment.** Wie bei den Nachträgen TB-36 (Abschnitt 15) und
TB-41 (Abschnitt 16) gilt: es hat **kein Selektionslauf stattgefunden**, kein
Raster ist gerechnet, kein Parametersatz bewertet. Die Sperrliste (Abschnitt 10)
gilt „ab dem signierten Tag", und der steht in Abschnitt 13 weiterhin als
*offen — Betreiber*. Es ist nichts aufzubrechen; es wird nachgetragen, **bevor**
gerechnet wird.

**Seit dem TB-41-Nachtrag sind neun Festlegungen getroffen worden, die im
Register noch nicht standen.** Der Snapshot soll unmittelbar danach gezogen
werden — und er darf nur auf einem Register stehen, das ihn deckt. Das ist der
Anlass dieses Abschnitts.

**Bestehender Text wird nicht umgeschrieben.** Ersetzte Fassungen bleiben
**wörtlich stehen** und tragen einen eingefügten Vermerk — dieselbe Form, die
15.7 und 16.1/16.3/16.6 schon benutzen. *Der Verlauf soll lesbar bleiben; das
ist der Sinn eines Registers.* Die harte Auflage dieses Nachtrags ist
**null entfernte Zeilen**, maschinell nachgewiesen
(`research/registernachtrag_tb41/pruefe_register.py`, Prüfung
`null_entfernte_zeilen`).

**Herkunft der Zahlen.** Keine Zahl dieses Abschnitts ist abgeschrieben; jede
ist in dieser Arbeit **an ihrer Quelle im Repo nachgerechnet** worden. Die
Einzelnachweise stehen in `docs/ERGEBNIS_TB-48_registernachtrag.md`, Abschnitt
„Welche Zahl wurde wo nachgerechnet".

| | |
|---|---|
| Die zwei Nicht-Kurs-Eingaben | `research/snapshotgrenze/ergebnisse/eingaben.json` |
| Teilkerzen-Befunde, Arten, letzte Kerze | `shared/snapshot.py::teilkerzen` über `data/`, neu ausgeführt |
| Jahresaufteilung 20 / 16 und die 11 Symbole | aus denselben Befunden **selbst nachgezählt** |
| Die Gegenprobe zu den 11 Symbolen | `docs/projektfuehrung/BACKLOG.md`, T34.9 |
| `pandas_market_calendars` 4.6.1, beide Hashes | `docs/MACLAUF_TB-47_snapshotgrenze.md` (TB-47-Maclauf) |
| Re-Adjustierung 9 766 / 1,2e-6 | `docs/projektfuehrung/BACKLOG.md`, T35.4 |
| Datenstand | `d9449faf51bffaaa…`, 223 Kursdateien — vor und nach dieser Arbeit identisch |

---

### 17.1 Registertext 5a — Bestand und Snapshot *(ersetzt die Fassung aus 16.3 (a) vollständig)*

> Es gibt einen **fortgeschriebenen Bestand** (Tatsachennotiz: `data/`) und je
> Lauf einen **eingefrorenen Snapshot** (Tatsachennotiz: `snapshots/<hash>/`),
> der **neben** dem Bestand liegt und nach seiner Erzeugung nicht mehr
> geschrieben wird.
>
> Der Snapshot enthält **alle Eingaben des Laufs, die nicht Code unter dem
> registrierten Commit sind**. ⭐ **Gemessen (TB-47): neben den Kursdateien
> genau zwei** — `config/top25_symbols.txt` und `config/sp500_top150.txt`.
>
> Sein `MANIFEST.json` führt jede Datei mit Inhalts-Hash. Der **Snapshot-Hash**
> ist der Hash der nach Pfad sortierten (Pfad, Inhalts-Hash)-Paare **der
> Dateien** — ⚠️ **nicht des Manifests**, sonst hinge der Name von der
> Metadaten-Formatierung ab.
>
> Der **Datenstand-Hash** wird im Manifest als eigenes Feld geführt, mit der
> unveränderten Regel: `*.csv` der obersten Ebene, Name + Grösse + SHA-256,
> sortiert.
>
> Forward-Tests und Registertext 7 lesen **den Bestand**; der Selektionslauf
> liest **ausschliesslich den Snapshot**. Kein Modul des Laufs ruft Kurse über
> das Netz ab. Das Bezugsdatum des Laufs (`asof`) kommt aus dem Register, **nie
> aus der Uhr**.

⚠️ **Befund zur Fundstelle, nicht stillschweigend geglättet.** Der Auftrag
dieses Nachtrags nennt als ersetzte Stelle „Registertext 5a in **Abschnitt
15**". **Dort steht sie nicht.** Abschnitt 15.7 führt Registertext 5 **ohne
Untergliederung** und ist seinerseits bereits **vollständig durch 16.3
ersetzt** (Vermerk seit TB-41 an Ort und Stelle). Die Fassung mit dem
Buchstaben **(a)** — `data/live/` gegen `data/snapshots/<hash>/` — steht in
**16.3**. Der Ersetzungsvermerk ist deshalb **dort** gesetzt worden, wo der
abgelöste Text tatsächlich steht. Hätte er in 15 gestanden, hätte er auf eine
Stelle gezeigt, die es nicht gibt.

**Was sich gegenüber 16.3 (a) sachlich ändert:** Die Ordnernamen `data/live/`
und `data/snapshots/<hash>/` werden zu **Tatsachennotizen** (`data/` und
`snapshots/<hash>/`) herabgestuft — der Registertext bindet sich nicht mehr an
den Pfad, sondern an die **Rolle**; der Snapshot liegt **neben** dem Bestand,
nicht in ihm. Neu hinzu kommen der Umfang der Eingaben (nicht nur Kursdateien),
die Trennung der **beiden** Hashes samt Bildungsregel und die Herkunft des
Bezugsdatums `asof`. Unverändert bleibt der Kern: **der Selektionslauf liest
ausschliesslich den Snapshot, kein Modul ruft Kurse über das Netz ab.**

---

### 17.2 Registertext 5c — Reihenfolge von Snapshot und Tag *(ersetzt die Fassung aus 16.3 (c))*

> Der Snapshot wird **vor** dem signierten Tag gezogen; **der Tag referenziert
> seinen Hash.** Ein zweiter Snapshot ist ein neuer Lauf.

**Was sich ändert:** 16.3 (c) sagte „**am Tag** des signierten Tags". Das liess
offen, was zuerst geschieht, und machte den Tag nicht überprüfbar. Die
korrigierte Fassung legt die **Reihenfolge** fest und gibt dem Tag einen
Inhalt: er nennt den Hash, den er signiert. *Ein Tag, der auf nichts zeigt,
signiert nichts.* Der zweite Satz ist unverändert.

⚠️ **Fundstelle wie bei 17.1:** der Auftrag nennt Abschnitt 15, die Fassung
„am Tag des signierten Tags" steht in **16.3 (c)**. Der Vermerk ist dort
gesetzt.

---

### 17.3 Registertext 5a, Zusatz — Ausnahme `rand_erste` bei der Teilkerzen-Prüfung

*Wörtlich übernommen aus dem Registereintrag vom 18.09.2026, einschliesslich
Herleitung und der beiden Vorbehalte.*

> **Registertext 5a, Zusatz — Ausnahme `rand_erste`.**
>
> Die vor dem Ziehen eines Snapshots vorgeschriebene Teilkerzen-Prüfung schlägt
> bei **36 der 223 Kursdateien** an, Art **`rand_erste`**: Die **erste** Kerze
> dieser Dateien deckt ihren Zeitraum nicht vollständig ab, weil die Historie
> des Symbols innerhalb der Periode beginnt.
>
> **Diese Befundart ist für das Ziehen eines Snapshots zugelassen**, wenn alle
> drei Bedingungen erfüllt sind:
>
> **(a)** Der Befund betrifft ausschliesslich die **erste** Kerze der Datei.
> ⚠️ **Für `rand_letzte` gilt diese Ausnahme nicht.**
> **(b)** Die Kerze ist nachweislich **das Aggregat genau der vorhandenen
> feineren Kerzen** — sie ist daraus abgeleitet, nicht unvollständig
> geschrieben. Die Prüfung stellt das je Datei fest.
> **(c)** Die Ausnahme wird im **Manifest des Snapshots** je Datei aufgeführt,
> mit Art und erster Kerze.
>
> ⚠️ **Die Prüfung selbst wird nicht abgeschwächt.** Sie schlägt weiter an und
> liefert weiterhin Rückgabewert 1; das Ziehen erfolgt gegen diesen Eintrag,
> nicht gegen ein Schweigen der Prüfung.

#### Die Begründung, als Tatsachennotiz

**1. Der Befund betrifft die Abdeckung, nicht die Richtigkeit.** Die Prüfung
selbst stellt je Datei fest: *„die Kerze ist auf die letzte Stelle das Aggregat
genau dieser Teilmenge: sie ist daraus **abgeleitet**."* Ein Symbol, dessen
erster Handel mitten in der Periode liegt, hat an diesem Tag zwangsläufig
weniger Stunden.

**2. Der gefährliche Rand ist sauber.** Gemessen auf beiden Rechnern:
`LETZTE Kerze betroffen: False` bei **allen 223** Dateien. Die Kerze, in die
ein Abruf mitten hineingeschrieben haben könnte, gibt es hier nicht.

**3. ⭐ Die Ausnahme ist für den Selektionslauf folgenlos — hergeleitet:**

| | |
|---:|---|
| **20 von 36** | erste Kerze **2017–2020**. Die erste Selektionsfalte beginnt **2022** — reiner Vorlauf |
| **16 von 36** | erste Kerze **ab 2023**, gehörend zu **genau 11 Symbolen**: `BMT ENA ENSO PEPE PROM PUMP SUI TRUMP U WLD ZKC` |
| ⭐ | **Diese Menge ist identisch mit der Liste aus T34.9** — den Symbolen, die **in keiner Selektionsfalte vorkommen** |

**Kein Symbol-Jahr-Beitrag des Selektionslaufs hängt an einer der 36 kurzen
ersten Kerzen.**

⭐ **Die Mengengleichheit ist gezeigt, nicht behauptet** (TB-48, beide Mengen
gebildet und gegeneinander gestellt): Differenz in **beide** Richtungen leer,
je **11** Elemente. Nachweis in `docs/ERGEBNIS_TB-48_registernachtrag.md`.
⚠️ Zwischen 2020 und 2023 liegt **keine** erste Kerze — die beiden Gruppen
20 und 16 sind daher lückenlos die vollen 36, nicht zwei Ausschnitte.

⚠️⚠️ **BEFUND zur Begründung in Zeile 1 der Tabelle — gemeldet, nicht
stillschweigend korrigiert (TB-48, 18.09.2026).** Der beschlossene Wortlaut
sagt: *„Die erste Selektionsfalte beginnt **2022** — reiner Vorlauf."*
**Beide Hälften dieses Satzes halten der Nachrechnung nicht stand**; der
Wortlaut bleibt als der beschlossene stehen, massgeblich ist diese Notiz.

| | |
|---|---|
| ⚠️ **Die erste Selektionsfalte beginnt nicht 2022, sondern 2019.** | `research/faltenplan_neun/daten/faltenplan.json`: `frueheste_falte: 2019`; die erste Falte läuft bei **allen neun** Bots von `2019-01-01` bis `2021-01-01` |
| ⚠️ **„Reiner Vorlauf" trifft nur auf 6 der 13 Symbole der Gruppe zu.** | Vor dem 01.01.2019 liegt die erste Kerze nur bei `ADA BNB BTC ETH TRX XRP`. Bei **sieben** Symbolen — `AAVE DOGE LINK NEAR SOL UNI ZEC` — liegt sie **innerhalb** des Fensters der ersten Falte |

⭐ **Die Schlussfolgerung trägt trotzdem — sie trägt nur aus einem anderen
Grund.** Nachgerechnet über **alle neun Bots und alle Falten** (TB-48): Es gibt
**null** Fälle, in denen eine der 36 kurzen ersten Kerzen in ein Faltenfenster
fällt, in dem ihr Symbol **geladen** ist. Die sieben Symbole oben stehen in der
ersten Falte bei allen fünf Krypto-Bots in `symbole_ohne_historie` — der Loader
lässt sie dort gar nicht erst zu. **Nicht der Vorlauf schützt, sondern die
Mindesthistorie des Loaders** (Registertext 3b (a)). Der Satz
*„Kein Symbol-Jahr-Beitrag des Selektionslaufs hängt an einer der 36 kurzen
ersten Kerzen"* ist damit **bestätigt**, und zwar maschinell über den
Faltenplan statt über eine Jahreszahl.

⚠️ **Warum das mehr ist als ein Tippfehler:** Die Begründung „Vorlauf" hängt an
einer **Jahreszahl** und wäre beim nächsten Faltenplan lautlos falsch geworden.
Die Begründung „der Loader lädt das Symbol dort nicht" hängt an einer **Regel,
die im Register steht** — und die sich nachrechnen lässt. Der Vorbehalt am Ende
dieses Zusatzes (*„fällt ein `rand_erste`-Befund an einer Datei an, deren Symbol
in einer Selektionsfalte vorkommt…"*) meint genau diese Prüfung.

**4. Reparieren wäre teurer und nicht dauerhaft.**

| | |
|---|---|
| ⚠️ **Teurer** | Abschneiden oder Neuaufbau ändert `data/` — und damit **`d9449faf…`**, die Tatsachennotiz vom 15.09., **samt der darauf gemessenen Symbolzahlen je Falte (3b)** |
| ⚠️ **Nicht dauerhaft** | **Jedes neu gelistete Symbol bringt den Befund wieder mit.** Eine Reparatur räumt den Bestand einmal auf und setzt die Uhr auf das nächste Listing zurück |

#### Die Messwerte zum Eintrag

| | |
|---|---|
| Gemessen am | **18.09.2026**, Cloud (Python 3.11.15) **und** MacBook (3.9.6) — **beide 36 von 223** |
| Arten | `{'rand_erste': 36}`, keine andere |
| Letzte Kerze betroffen | **nein**, bei keiner Datei |
| Datenstand | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, 223 Dateien |
| Werkzeug | `shared/snapshot.py`, Prüfung vor dem Ziehen, Rückgabewert 1 bei Befund |
| Rohdaten | `research/snapshotgrenze/ergebnisse/` (Cloud) · TB-47-Maclauf `04_teilkerzen.json` |

⚠️ **Zwei Angaben, die eine Prüfung NICHT abdeckt** und die hier stehen, damit
niemand sie später für gemessen hält:

| | |
|---|---|
| **175 von 223** Dateien tragen den Vermerk **`kein_zeuge`** | 150 Aktien und 25 Krypto-1h. *„Die Abdeckung der Randkerzen ist aus den Dateien nicht belegbar"* — es gibt keine feinere Datei zum Vergleich. **Das ist „kein Befund", nicht „geprüft"** |
| Die Vollständigkeit der **letzten** Kerze dieser 175 | ruht auf `shared/abrufschutz.py` (TB-35), **nicht** auf dieser Prüfung. Eine andere Zusicherung, die trägt — aber eine andere |

#### Was dieser Zusatz ausdrücklich NICHT tut

| | |
|---|---|
| ❌ | Er ändert `data/` nicht |
| ❌ | Er schwächt die Prüfung nicht ab — es gibt **keine Übergehen-Flagge** |
| ❌ | Er erlaubt **keinen** Befund ausser `rand_erste` an der **ersten** Kerze |
| ❌ | Er berührt `d9449faf…` nicht — der Wert bleibt unverändert gültig |

> ⚠️ **Fällt in einem künftigen Bestand ein `rand_erste`-Befund an einer Datei
> an, deren Symbol in einer Selektionsfalte vorkommt, greift diese Ausnahme
> nicht automatisch.** Dann ist neu zu entscheiden, und die Herleitung oben ist
> neu zu rechnen.

---

### 17.4 Registertext 5e — der Lese-Audit *(neu)*

> Der Selektionslauf erzeugt einen **Lese-Audit**: die Liste aller Dateien, die
> er gelesen hat, mit Inhalts-Hash. **Ein Lauf ist nur gültig, wenn der Audit
> vorliegt, jede Datei darin im Manifest des Snapshots steht und der
> Snapshot-Hash vor und nach dem Lauf identisch ist.** Ein Lauf ohne Audit oder
> mit einer Datei ausserhalb des Manifests ist **kein Lauf dieses Registers**.
> **Wie der Audit erzeugt wird, ist Umsetzung.**

*Warum das neben 5a steht und nicht in ihm aufgeht:* 5a sagt, **woraus** der
Lauf liest. Der Lese-Audit sagt, **woraus er nachweislich gelesen hat**. Das
erste ist eine Vorschrift, das zweite ein Beleg — und nur das zweite fällt auf,
wenn ein Modul still an `data/` vorbeigreift. ⚠️ Die Prüfung „Snapshot-Hash vor
und nach dem Lauf identisch" deckt zusätzlich den Fall ab, dass der Lauf in
seine eigene Eingabe schreibt.

---

### 17.5 Registertext 5f — die registrierte Umgebung *(neu)*

> Der Selektionslauf findet auf einer **registrierten Umgebung** statt:
> **Python-Fassung** (Tatsachennotiz: 3.9.6), ein **`requirements.lock`** mit
> exakten Versionen aller Pakete, dessen Hash im Register steht, und die
> **Plattform**. Der Lauf beginnt mit einer Prüfung dieser drei Angaben und
> **bricht bei Abweichung ab (Rückgabewert 2)**.
>
> ⭐ **Tatsachennotiz:** Der Handelskalender kommt **nicht aus einer Datei**,
> sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47:
> Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit **Umgebung, nicht
> Eingabe**, und liegt im Lock.
>
> Der Reproduktionstest gilt als bestanden, wenn ein zweiter Lauf **auf
> derselben registrierten Umgebung** auf einer anderen Maschine bitidentisch
> ist. Eine Reproduktion auf anderer Umgebung wird **berichtet**, ist aber
> weder Bedingung noch Widerlegung.

> ⭐ **17.5 ERGÄNZT durch R74 (54.1)** (Fable 04a R74, Unterpunkte (a) und (b), TB-136, 05.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

⚠️ **Das schärft die Prüfung aus 16.3 nach.** Dort stand: der Lauf „muss auf
einer zweiten Maschine bitidentisch reproduzieren". **Ohne Umgebungsbegriff war
das nicht entscheidbar** — eine Abweichung konnte am Snapshot liegen oder an
einer anderen Paketfassung, und beides sah gleich aus. Erst mit der
registrierten Umgebung trennt der Test die beiden Fälle. Der Satz in 16.3
bleibt stehen und gilt weiter; 17.5 sagt, **auf welcher Grundlage** er gemessen
wird.

⭐ **Warum der Kalender eigens genannt ist:** Er ist die einzige Eingabe des
Laufs, die **wie eine Datei aussieht und keine ist**. Wäre er Eingabe, gehörte
er in den Snapshot; als Paket gehört er in den Lock. Die Einordnung ist
gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten.

---

### 17.6 Registertext 7, Ergänzung I — der Kein-Entscheid-Tag *(neu)*

> Ein Tag, an dem ein Bot seine Entscheidungskerze nicht bestimmen konnte, ist
> ein **Kein-Entscheid-Tag**: keine Einstiege, keine Ausstiege, **offene
> Positionen unverändert**, ein **Lauf-Datensatz mit Grund**.
> Kein-Entscheid-Tage gehen **nicht** in die Übereinstimmungsquote ein und
> werden je Bot gezählt. Übersteigt ihr Anteil im Vergleichsfenster **5 %** der
> Handelstage (**als willkürlich gekennzeichnet**), gilt das Fenster als
> „Holdout beeinträchtigt" und wird so berichtet.

*Warum das nötig ist:* Ohne diese Festlegung sieht ein Tag ohne
Entscheidungskerze in den Zahlen **genauso aus wie „kein Signal"** — derselbe
Fehler, den `docs/DATENLUECKEN.md` für ausgefallene Cron-Läufe schon
festhält. Ein solcher Tag zählte dann als Übereinstimmung, wo gar nichts
verglichen wurde. Die Regel macht den Unterschied sichtbar **und** hält fest,
dass ein Kein-Entscheid-Tag am Bestand nichts ändert: **offene Positionen
bleiben offen**, es wird nicht vorsichtshalber geschlossen.

---

### 17.7 Registertext 7, Ergänzung II — Ereignismenge und Mindestzahl *(neu; schliesst die offene Stelle aus 16.11, Zeile 5)*

> Vergleichsmenge sind die **Einstiegs- und Ausstiegsereignisse (Symbol, Tag)
> beider Seiten** im Vergleichsfenster, ohne Kein-Entscheid-Tage.
> Übereinstimmung = |Schnitt| / |Vereinigung|.
> **Mindestzahl n = |Vereinigung| ≥ 20, abgeleitet als 1 / (1 − Schwelle).**
> Unter 20 lautet das Urteil **„unbestimmt"**: Der Bot wird selektiert und nach
> Registertext 6 eingestuft, im Bericht mit dem Vermerk „Backtester unbestimmt
> (n = …)"; ein Aufstieg auf **Bestätigt** setzt n ≥ 20 **und** Übereinstimmung
> ≥ 95 % voraus.

**Die Ableitung, nachgerechnet und Teil des Registertextes:**

> Die Schwelle aus 16.5 ist **95 %**. Gesucht ist das kleinste n, bei dem **eine
> einzige** Abweichung die Schwelle nicht schon reisst. Bei **n = 19** ergibt
> eine Abweichung **18/19 = 94,7 %** — unter der Schwelle. Bei **n = 20** ergibt
> eine Abweichung **19/20 = 95,0 %** — auf der Schwelle, also nicht darunter.
> **n = 20 = 1 / (1 − 0,95).** Unterhalb davon entscheidet ein einzelnes
> Ereignis über das Urteil, und die Schwelle misst dann **Handelsfrequenz statt
> Qualität.**

⚠️ **Damit ist die in 16.5 und in 16.11, Zeile 5, als *offen — Betreiber*
geführte Mindestzahl festgelegt.** Registertext 7 ist ab hier nicht mehr nur
berichtsfähig, sondern **anwendbar** — soweit das Vergleichswerkzeug existiert
(siehe 17.10).

⭐ **Der Unterschied zur Fassung aus 16.5 ist mehr als eine Zahl.** 16.5 kannte
zwei Urteile („bestätigt" / „nicht bestätigt") und darunter den Zustand
**„Backtester nicht geprüft"**. 17.7 benennt den Zustand unterhalb der
Mindestzahl als **„unbestimmt"** und sagt zusätzlich, **was mit dem Bot
geschieht**: er wird selektiert und eingestuft, er bleibt nicht liegen. Die
Sperre wirkt allein am **Aufstieg auf Bestätigt**. *Eine fehlende Messung ist
kein schlechtes Ergebnis — aber sie trägt auch keine Beförderung.*

⚠️ **Und der Vergleichsgegenstand ist jetzt benannt.** 16.5 sprach von
„Anteil übereinstimmender Signale", ohne zu sagen, was ein Signal ist. 17.7
legt ihn fest: **Ereignispaare (Symbol, Tag)**, Einstiege und Ausstiege, beide
Seiten, und die Quote als **Jaccard-Mass** |Schnitt| / |Vereinigung| — nicht als
Anteil an einer der beiden Seiten. *Ein Mass, das nur durch die eine Seite
teilt, belohnt die Seite, die weniger Ereignisse erzeugt.*

---

### 17.8 Registertext 7, Ergänzung III — Drift *(neu)*

> Jeder Forward-Test-Lauf protokolliert **den Datenstand-Hash des Bestands, den
> er gelesen hat**, und **die Werte seiner Entscheidungskerze je Symbol**. Der
> Backtester-Vergleich läuft auf **diesen protokollierten Werten**; weicht der
> Bestand zum Vergleichszeitpunkt vom protokollierten Hash ab, wird die
> Abweichung je Symbol als **„Drift"** ausgewiesen und **nicht** als
> Verfahrensabweichung gezählt.

⭐ **Die Begründung gehört in den Text:** Aktienkurse werden nach jeder
Dividende re-adjustiert. **Gemessen (T35.4, Mac-Lauf TB-35): 9 766 von rund
11 000 Bestandszeilen wichen bei einem einzigen echten Abruf ab, maximal
1,2 × 10⁻⁶ relativ, ausschliesslich vor dem letzten Ex-Dividenden-Tag.** Ohne
diese Regel zählte **jede Dividende im Vergleichsfenster als
Verfahrensabweichung** — der Backtester bekäme eine schlechte Note für ein
Ereignis, das mit seiner Rechenweise nichts zu tun hat.

⚠️ **Das hebt die Zählregel aus 16.5 nicht auf, sondern grenzt sie ab.** 16.5
sagt: Signalabweichungen zwischen Live- und Snapshot-Bestand bis 10⁻⁵ „werden
gezählt — nicht weggerechnet, nicht als Rauschen abgetan". Das bleibt. 17.8
betrifft einen **anderen** Fall: nicht zwei Bestände nebeneinander, sondern
**denselben Bestand zu zwei Zeitpunkten**. Die Unterscheidung ist am
protokollierten Hash **entscheidbar** — genau deshalb verlangt der Text ihn.
*Eine Abweichung, die man erst nachträglich erklärt, ist eine Auslegung; eine,
die am Hash hängt, ist ein Befund.*

---

### 17.9 Nachtrag zur Tatsachennotiz vom 15.09.2026 — was `d9449faf…` bezeichnet

**Datiert angehängt. Nichts entfernt. Der Wert bleibt gültig — nur sein
Referent wird benannt.**

> **Ab Registertext 5a (neu) bezeichnet
> `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`
> den Kursdatenteil des Snapshots (Datenstand-Hash), nicht den Snapshot selbst;
> der Snapshot-Hash ist ein eigener Wert.**

⭐ **Gemessen im TB-47-Maclauf, beide Werte nebeneinander über dieselben 223
Dateien:**

| | |
|---|---|
| `datenstand_hash` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` — **trifft den verankerten Wert** |
| `snapshot_hash` | `4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608` |
| verschieden | **ja** — wie vorgesehen, die beiden Hashes beantworten verschiedene Fragen |

⚠️ **Warum das aufgeschrieben werden musste.** 16.3 (b) sagt: „**Der
Registerhash bezeichnet den Snapshot.**" Zu diesem Zeitpunkt gab es nur *einen*
Hash, und der war `d9449faf…`. Seit TB-47 gibt es **zwei**, und der Satz aus
16.3 (b) liesse sich ohne diesen Nachtrag so lesen, als sei `d9449faf…` der
Snapshot-Hash. Er ist es nicht. **Die Tatsachennotiz vom 15.09.2026
(Abschnitt 10) bleibt in jedem Wort gültig**; sie hat den Bestand gemessen, und
den misst `d9449faf…` weiterhin.

---

### 17.10 Wo Registertext und Umsetzung auseinanderfallen

**Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in
Ordnung — solange es benannt ist.** Dieselbe Form wie 16.11; hier die Stellen,
die **mit Abschnitt 17** hinzukommen, Stand 18.09.2026. Die elf Zeilen aus
16.11 bleiben davon unberührt und gelten weiter.

| # | Registertext | Was der Code heute tut | Wer schliesst die Lücke |
|---:|---|---|---|
| 1 | **5a (neu)** — Snapshot **neben** dem Bestand, `snapshots/<hash>/` | Es gibt **einen** Ordner `data/`; kein Snapshot ist gezogen. Unverändert 16.11, Zeile 1 | eigene Aufgabe (Datenordner-Umbau) |
| 2 | ⚠️ **5a, Zusatz (17.3)** — `rand_erste` ist zum Ziehen **zugelassen** | **Der Code kann den Snapshot heute nicht ziehen.** `shared/snapshot.py::ziehen` wirft bei **jedem** Teilkerzen-Befund (`Snapshotfehler`, vor dem Kopieren) — bei 36 Befunden also immer. Eine registrierte Ausnahme kennt er nicht, und eine Übergehen-Flagge soll es nach 17.3 auch nicht geben. ⭐ **Das Manifest trägt das Feld `teilkerzen` bereits**, es wird nur nie geschrieben, weil der Lauf vorher abbricht | eigene Aufgabe: die Ausnahme **gegen den Registereintrag** prüfen, nicht gegen eine Flagge |
| 3 | **5e (17.4)** — Lese-Audit | **Nicht vorhanden.** Kein Modul führt Buch über gelesene Dateien; im ganzen Quelltext gibt es keine solche Stelle | eigene Aufgabe |
| 4 | **5f (17.5)** — registrierte Umgebung, Abbruch mit Rückgabewert 2 | **Nicht vorhanden.** Es gibt **kein `requirements.lock`** (nur `requirements.txt` ohne feste Versionen), keine Fassungsprüfung und keinen Abbruchpfad. ⚠️ **Auch die Mindestfassung des Projekts steht nirgends** (`docs/UMGEBUNGEN.md`, offen) | eigene Aufgabe, zusammen mit dem Lock |
| 5 | **7, Ergänzung I (17.6)** — Kein-Entscheid-Tag | **Nicht vorhanden.** Die neun `forward_test.py` kennen den Begriff nicht und schreiben keinen Lauf-Datensatz mit Grund | eigene Aufgabe (Änderung am Live-Pfad, eigene Freigabe) |
| 6 | **7, Ergänzung II (17.7)** — Ereignismenge, n ≥ 20 | **Kein Vergleichswerkzeug** — unverändert 16.11, Zeile 4. ⭐ **Zeile 5 aus 16.11 ist mit 17.7 erledigt:** die Mindestzahl ist nicht mehr offen | eigene Aufgabe |
| 7 | **7, Ergänzung III (17.8)** — Drift | **Nicht vorhanden.** Kein `forward_test.py` protokolliert den Datenstand-Hash oder die Werte seiner Entscheidungskerze je Symbol | eigene Aufgabe |

⚠️ **Zeile 2 ist die dringendste.** Sie ist die einzige, die einen Schritt
blockiert, der unmittelbar bevorsteht: **der Snapshot soll gezogen werden, und
mit dem heutigen Code lässt er sich nicht ziehen.** Die übrigen beschreiben
Vorhaben, deren Zeitpunkt offen ist.

---

### 17.11 Was dieser Nachtrag nicht tut

* **Kein Selektionslauf.** Weiterhin kein Raster gerechnet, kein Parametersatz
  bewertet, kein Ergebnis erzeugt. **Kein Amendment.**
* **Kein Snapshot gezogen, kein signierter Tag, kein Zeitanker.** Das ist der
  nächste Schritt und gehört dem Betreiber.
* **Kein Code geändert.** Nichts unter `shared/`, `strategies/`, `research/`,
  `broker/`, `dashboard/`, `notifications/` oder `system/`; keine Crontab.
  Die in 17.10 genannten Lücken sind **Befunde**, nicht Reparaturen.
* **Keine Kursdatei angefasst.** Der Datenstand ist vor und nach dieser Arbeit
  `d9449faf51bffaaa…` bei 223 Dateien — gemessen, nicht angenommen.
* **Keine Parameterübernahme.** `live_params.py` ist in dieser Arbeit nicht
  einmal gelesen worden.
* **Keine Zeile entfernt.** `git diff --numstat` auf dieses Dokument weist die
  Null aus; der Nachweis steht in
  `docs/ERGEBNIS_TB-48_registernachtrag.md`.
* **Nichts zum zweiten Umstellungstag.** ⚠️ **Sein Datum existiert noch
  nicht** — es entsteht erst am ersten Tag, an dem alle neun Bots ohne Rückfall
  aus `data/` lesen. Eigener Eintrag, danach.
* **Keine Gleichheitsprüfung der Entscheidungskerze, kein Datencron, kein
  Resolver-Modus.** Alle drei sind Änderungen am Live-Pfad beziehungsweise der
  grosse Umbau — eigene Aufgaben mit eigener Freigabe.

*Nachgetragen in TB-48, 18.09.2026. Kein Amendment: kein Selektionslauf, kein
signierter Tag, keine Parameterübernahme.*

---

