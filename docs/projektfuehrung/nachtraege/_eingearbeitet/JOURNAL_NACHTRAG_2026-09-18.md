# Journal-Nachtrag 18.09.2026

> ⚠️ EINGEARBEITET am 18.09.2026 in `docs/projektfuehrung/JOURNAL.md` (als Blöcke BA–BE — der höchste vorhandene Block war AZ, nicht AX; alle fünf um zwei Stellen verschoben), Commit 02de1f7.
> Dieses Dokument bleibt als Beleg des Nachtrags stehen und wird nicht
> mehr fortgeschrieben.

**Anzufügen am Ende von `docs/projektfuehrung/JOURNAL.md`. Nichts wird
umgeschrieben.**

> ⚠️ **Zu den Blockbuchstaben:** Der letzte mir bekannte Block ist **AX** (die
> Fehlerliste vom 17.09.). Die fünf Blöcke hier heissen deshalb **AY bis BC**.
> **Vor dem Einfügen prüfen, welcher Buchstabe wirklich der letzte ist** — steht
> dort schon ein AY, wandern alle fünf um eine Stelle weiter. *Ein Verweis aus
> dem Backlog muss treffen.*

---

## Block AY — TB-46 gemergt, Zuschnitt B entschieden, zwei Fable-Runden

**17.09.2026. Gemergt `135c306`.**

`shared/snapshot.py` und `shared/test_snapshot.py` (69 Prüfungen, dreizehn
Mutationsproben) sind im Repo. **Erhebung, Werkzeug, Wache — kein Umbau.**

**Die Messung, die alles Weitere trägt:**

| | |
|---:|---|
| **182** | Module erreichen `data/` — die frühere Zahl **101** ist exakt reproduziert und **nicht falsch**, sie zählt eine engere Frage |
| ⭐ **0** | **Bot-Dateien bauen einen Pfad.** Der Umbau kommt ohne `forward_test.py`, `live_params.py` und `equity_simulation.py` aus |
| **90** | Module der Selektionsseite, die auf den Snapshot zu zeigen sind |

⭐ **Gemessen über den Syntaxbaum, nicht mit Textsuche** — zwei `forward_test.py`
**nennen** `data/` in einer Protokollzeile. Eine Textsuche hätte gemeldet, der
Umbau müsse genau die Dateien anfassen, die er nicht anfassen darf.
**Prüfprinzip B5.**

### Die Entscheidung: Zuschnitt B

**`data/` bleibt der lebende Bestand, `snapshots/<hash>/` kommt daneben.**
Fable hat das bestätigt — *„nicht als Abweichung, sondern als die bessere
Erfüllung"* von Registertext 5.

### Die zweite Fable-Runde: der Hash

**Frage:** Worüber läuft der Snapshot-Hash — über das Manifest oder über die
Dateien?

**Antwort, angenommen:** ⭐ **über die sortierten (Pfad, Inhalts-Hash)-Paare der
DATEIEN.** *Liefe er über das Manifest, hinge der Name des Snapshots an der
Formatierung seiner Metadaten — und ein geänderter Zeitstempelformat erzeugte
einen anderen Snapshot bei identischen Daten.*

### Und der Vorschlag von mir, der verworfen wurde

**Ich hatte eine „Eingangswache" vorgeschlagen:** beim Start des Laufs das
Manifest prüfen. **Fable:** *„Die Wache prüft die Eingabe, nicht das Verhalten."*
Ein Modul, das seinen Pfad selbst baut, sieht die übergebene Wurzel nie.

⭐ **Angenommen stattdessen: drei Schichten.** **(1)** Resolver-Modus in
`shared/paths.py`, der die Snapshot-Wurzel liefert und bei jeder Anfrage nach dem
Live-Bestand **wirft** · **(2)** **AST-Test**, dass kein Selektionsmodul einen
Datenpfad ausserhalb des Resolvers baut — ⭐ *er ist rot, bis die 90 verdrahtet
sind, und das ist gewollt: er misst den Umbau* · **(3)** **Lese-Audit** als
Ausgangsnachweis.

### In einfacher Sprache

**Was wir wissen wollten:** Wie viele Programmteile lesen die Kursdaten, und
müssen wir dafür die Bot-Dateien anfassen, die nicht angefasst werden dürfen?

**Was herauskam:** 182 Programmteile lesen die Daten, aber **kein einziger der
neun Bots baut selbst einen Dateipfad**. Der Umbau kommt ohne sie aus.

**Warum das so ist:** Gemessen wurde nicht mit einer Textsuche, sondern an der
Struktur des Programms. Zwei Bots **erwähnen** den Datenordner in einer
Protokollzeile — eine Textsuche hätte daraus geschlossen, man müsse sie ändern.

**Was das für dich heisst:** Der grosse Umbau ist ungefährlicher als befürchtet.
Und die eingefrorene Kopie der Daten kommt **neben** den lebenden Bestand, nicht
an seine Stelle.

---

## Block AZ — TB-46b: der Sicherheitspunkt ist beantwortet

**18.09.2026. Gemergt `c5ad722`.**

**Die Frage kam von Fable, und wir hatten sie nicht gestellt:**
*„‚Hält null Positionen' — heisst das **keine neuen** Positionen, oder
**schliesst** der Bot offene, weil er sie ohne Kerze nicht bewerten kann?"*
⚠️ *„Ein Bot, der bei fehlender Kerze verkauft, hat kein Holdout-Problem,
sondern ein Sicherheitsproblem."*

### Die Antwort

> ⭐⭐⭐ **KEIN Bot schliesst eine Position, weil Kursdaten fehlen. Nicht
> „wurde nicht beobachtet", sondern strukturell unmöglich.**

**Gelesen an neun von neun Bots über fünf Ausstiegspfade. Die gemeinsame
Bauform:**

```
__main__          für jedes Symbol:  df = entscheidungskerze.lade(...)
                                     → in price_data / indicator_data
                  alles in einem try/except Exception je Symbol

check_open_trades  für jeden offenen Trade:
                     if symbol not in <daten>:  continue     ← die Tür
                     future = df[df["open_time"] > entry_time]
                     nur bei Treffer:  UPDATE ... status='closed'
```

⭐ **Es gibt kein `else`.** Ein Symbol ohne Kursdaten erreicht die UPDATE-Zeile
nicht.

### Der offene Punkt, der aus der Prüfung entstand

⚠️⚠️ **`shared/entscheidungskerze.py`, `lade()`: der Rückfall auf die zweite
Quelle wird nicht auf Frische geprüft.**

```
658    if art is not None:                       # data/ fehlt, veraltet oder unklar
659        sammler.erfasse(symbol, art, grund)
663        df = abruf()                          # ← die zweite Quelle
667    gefiltert, _verworfen, hinweis = nur_entscheidbar(df, …)
```

`_aus_datei()` fragt `ist_frisch()` (Zeile 690). **`abruf()` fragt niemand.**
⚠️ *Das ist der einzige Weg, auf dem eine falsche Kerze bis zur Entscheidung
kommt.*

### Fables Antwort darauf: Gleichheit statt Frische

**Mein Vorschlag war eine Frischeprüfung. Verworfen.**

⭐ **Angenommen: der `close_time` der gelieferten Kerze muss dem erwarteten Wert
GLEICHEN — aus jeder Quelle, ohne Ausnahme. Stimmt er nicht, ist es ein
Kein-Entscheid.**

> *„Die Gleichheit braucht keinen Parameter. Eine Toleranz wäre eine zweite
> willkürliche Zahl an genau der Stelle, an der das Register keine mehr
> verträgt."*

**Vier Dinge gehören deshalb in EINEN Zug** — und der braucht die
Betreiberfreigabe für `shared/entscheidungskerze.py`: Gleichheitsprüfung ·
Datencron mit Prüfung vor den Bot-Läufen (`TZ=UTC`) · Kein-Entscheid-Datensatz in
`melde()` · Datenstand-Hash und Kerzenwerte je Lauf ins Protokoll.

### Der Mac-Lauf und die eine abweichende Datenbank

**Eine** der neun Datenbanken wich ab. ⭐ **Die Erklärung ist belegt, nicht
plausibilisiert:** `turtle_soup_crypto` hat einen Cronjob `15 0 * * *`; die
Änderungszeit 00:15:24 Ortszeit = **22:15:24 UTC** liegt im Prüffenster, und der
Inhaltsunterschied deckt sich **Zeile für Zeile** mit der Logzeile desselben
Laufs.

### In einfacher Sprache

**Was wir wissen wollten:** Kann es passieren, dass ein Bot eine offene Position
verkauft, nur weil die Kursdaten für dieses Wertpapier gerade fehlen?

**Was herauskam:** **Nein, und zwar nicht zufällig.** In allen neun Bots führt
der Weg zur Verkaufszeile über eine Abfrage, die ein Wertpapier ohne Kursdaten
vorher überspringt. Es gibt keinen Zweig, der „sonst verkaufe" sagt.

**Warum das so ist:** Der Code ist so gebaut, dass fehlende Daten den Bot beim
betroffenen Wertpapier weitergehen lassen. Das war nicht als Sicherheitsmassnahme
gedacht, wirkt aber wie eine.

**Was das für dich heisst:** Der Punkt, der vor allem anderen stand, ist vom
Tisch. **Geblieben ist ein kleinerer:** Wenn die gespeicherten Daten veraltet
sind, holt der Bot sie live nach — und **dabei prüft niemand, ob das Gelieferte
wirklich die richtige Kerze ist.** Das wird behoben, sobald du die Änderung an
dieser einen Datei freigibst.

---

## Block BA — TB-47: die Snapshotgrenze, gemessen

**18.09.2026. Gemergt `a1e7fb4`.**

| | |
|---|---|
| ⭐ **Die Grenze** | **transitive Hülle über 142 Module ⇒ genau ZWEI** Nicht-Kursdaten-Eingaben: `config/top25_symbols.txt` und `config/sp500_top150.txt`. Kein Handelskalender als Datei — er kommt aus dem Paket, also aus dem Lock |
| ⭐ **Die zwei Hashes** | `datenstand` = `d9449faf…` bei 223 Dateien, **trifft den Anker vom 15.09.** · `snapshot_hash` = `4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608`, **verschieden**. *Zwei Zahlen, zwei Fragen* |
| ⚠️ **36 von 223** | Kursdateien mit Befund **`rand_erste`** — die **erste** Kerze deckt ihren Zeitraum nicht voll ab. ⭐ **Die Prüfung stellt je Datei fest, dass die Kerze auf die letzte Stelle das Aggregat genau der vorhandenen feineren Kerzen ist: abgeleitet, nicht unvollständig geschrieben** |
| ⭐ **Letzte Kerze** | **bei keiner Datei betroffen** — der gefährliche Rand ist sauber |
| ⚠️ **175 von 223** | tragen **`kein_zeuge`** — 150 Aktien, 25 Krypto-1h. **Keine feinere Datei zum Vergleich ⇒ nicht belegbar.** Das ist *„kein Befund"*, nicht *„geprüft"* |
| **Prüfungen** | `shared/test_snapshot.py` **69 → 110**, dreizehn Mutationsproben, jede mit Gegenprobe |

**Beide Rechner, dieselben Zahlen** — Cloud 3.11.15, Mac 3.9.6.

### Prüfprinzip B4, neue Variante: eine Probe kann sich selbst SEHEN

**Die Zählung überlebender Enkelprozesse meldete zuerst `4`.** Das wäre der
Gegenbeweis gewesen. **Die Sitzung hat nicht weitergemacht, sondern
nachgesehen — die Zählung zählte sich selbst:** Das Suchmuster stand in der
eigenen Befehlszeile, also fand `ps` die eigene Shell.

| Gegenprobe | Ergebnis |
|---|---|
| nur Python-Prozesse | 1 |
| Zählung aus einer **Datei** heraus, eigener Prozess ausgeschlossen | 1 |
| ⭐ **Aufruf ohne Heredoc — das Muster steht nicht mehr in der Befehlszeile** | **0** |

> ⭐ **Wir kannten: „eine Probe kann sich selbst blind machen." Hier galt: eine
> Probe kann sich selbst sehen — und meldet dann einen Fehler, den es nicht
> gibt.**

### Zwei Korrekturen am Rand

- ⚠️ **`system/test_log_rotation.py` stand als „bekannt rot" — er ist 117/117
  grün auf beiden Rechnern.** Der Eintrag kam aus einem Lauf auf einem alten
  Checkout. **Gestrichen, mit Kommentar:** *„Ein falscher Eintrag in dieser Liste
  ist teurer als gar keiner."*
- **`pandas_market_calendars` 4.6.1** auf dem Mac — ⭐ die Fassung, von der der
  Handelskalender kommt, und damit eine Zahl für `requirements.lock` und den
  Registereintrag nach 5f.

### In einfacher Sprache

**Was wir wissen wollten:** Was genau muss in die eingefrorene Kopie hinein,
damit der Selektionslauf später bitgenau wiederholbar ist?

**Was herauskam:** Ausser den Kursdateien nur **zwei** weitere Dateien — zwei
Symbollisten. Alles andere kommt entweder aus dem Programmcode oder aus einem
Paket, dessen Version wir festschreiben.

**Warum das so ist:** Gemessen wurde nicht „welche Dateien fallen uns ein",
sondern was die Programme wirklich lesen, über alle Aufrufwege hinweg.

**Was das für dich heisst:** Die Kopie ist überschaubar und vollständig
beschreibbar. **Ein Vorbehalt bleibt ehrlich benannt:** Bei 175 der 223
Kursdateien lässt sich nicht beweisen, dass die Randkerzen vollständig sind — es
gibt keine feinere Datei zum Vergleich. Dafür bürgt eine andere Schutzschicht,
und das steht so im Register.

---

## Block BB — Registertext 5a: die Ausnahme `rand_erste`

**18.09.2026. Registereintrag, eingetragen mit TB-48 als Abschnitt 17.3.**

**Die Teilkerzen-Prüfung schlägt bei 36 der 223 Kursdateien an und verweigert
damit jeden Snapshot. Die Ausnahme ist registriert — nach drei Bedingungen:**

| | |
|---|---|
| **(a)** | Der Befund betrifft ausschliesslich die **erste** Kerze. ⚠️ **Für `rand_letzte` gilt die Ausnahme nicht** |
| **(b)** | Die Kerze ist nachweislich **das Aggregat genau der vorhandenen feineren Kerzen** |
| **(c)** | Die Ausnahme wird **im Manifest des Snapshots** je Datei aufgeführt |

> ⚠️ **Die Prüfung selbst wird nicht abgeschwächt. Es gibt keine
> Übergehen-Flagge.** Sie schlägt weiter an und liefert weiter Rückgabewert 1;
> das Ziehen erfolgt **gegen diesen Eintrag**, nicht gegen ein Schweigen der
> Prüfung.

**Die Folgenlosigkeit ist hergeleitet, nicht behauptet:**

| | |
|---:|---|
| **20 von 36** | erste Kerze **2017–2020** — reiner Vorlauf vor der ersten Selektionsfalte |
| **16 von 36** | erste Kerze **ab 2023**, gehörend zu **genau 11 Symbolen**: `BMT ENA ENSO PEPE PROM PUMP SUI TRUMP U WLD ZKC` |
| ⭐ | **Diese Menge ist identisch mit der Liste aus T34.9** — den Symbolen, die **in keiner Selektionsfalte vorkommen** |

**Kein Symbol-Jahr-Beitrag des Selektionslaufs hängt an einer der 36 kurzen
ersten Kerzen.** ⭐ **Und TB-48 hat das direkt gemessen statt hergeleitet:**
*„kurze erste Kerze in einer GELADENEN Falte: Soll 0, Ist 0"*, über alle neun
Bots.

**Warum nicht reparieren:**

| | |
|---|---|
| ⚠️ **Teurer** | Abschneiden oder Neuaufbau ändert `data/` — und damit `d9449faf…`, die Tatsachennotiz vom 15.09. samt der darauf gemessenen Symbolzahlen je Falte |
| ⚠️ **Nicht dauerhaft** | **Jedes neu gelistete Symbol bringt den Befund wieder mit** |

> ⚠️ **Fällt künftig ein `rand_erste`-Befund an einer Datei an, deren Symbol in
> einer Selektionsfalte vorkommt, greift diese Ausnahme nicht automatisch.**

### In einfacher Sprache

**Was wir wissen wollten:** 36 von 223 Kursdateien haben eine erste Kerze, die
ihren Zeitraum nicht ganz abdeckt. Ist das ein Fehler, der die eingefrorene
Kopie unbrauchbar macht?

**Was herauskam:** **Nein.** Die kurze erste Kerze entsteht, weil die Geschichte
eines Wertpapiers mitten in einem Tag oder einer Stunde beginnt — der erste
Handelstag hat dann weniger Stunden. Das Prüfprogramm rechnet selbst nach, dass
die Kerze genau die Summe der vorhandenen feineren Kerzen ist.

**Warum das so ist:** Der gefährliche Fall wäre die **letzte** Kerze — dort
könnte ein Abruf mitten hineingeschrieben haben. Die ist bei **keiner** der 223
Dateien betroffen.

**Was das für dich heisst:** Die Ausnahme steht im Register, eng gefasst und
begründet. Sie gilt nur für die erste Kerze und nur, wenn nachgerechnet ist, dass
die Zahlen stimmen. **Und das Prüfprogramm wird nicht weicher gemacht** — es
meldet weiter; erlaubt wird die Ausnahme durch einen Eintrag daneben, den ein
Prüfer lesen kann.

---

## Block BC — TB-48: der Registernachtrag, und zwei Fehler von mir

**18.09.2026. Gemergt `db8913a`.**

⭐ **`git diff --numstat`: `506 0`.** 506 Zeilen hinzugefügt, **null entfernt**,
genau eine Datei berührt. Der Registerprüfer aus TB-41 läuft über alle neun
Prüfungen einschliesslich `null_entfernte_zeilen`: **kein Befund.**

**19 Zahlen an ihrer Quelle nachgerechnet, je mit Datei und Fundstelle. 18
stimmen.** Darunter: die 11 Symbole als Menge identisch mit T34.9 · beide Hashes ·
36 Befunde der Art `rand_erste` · letzte Kerze nicht betroffen · 175 `kein_zeuge`,
davon 150 Aktien und 25 Krypto-1h · `18/19 = 94,7 %` reisst die Schwelle,
`19/20 = 95,0 %` nicht, `1/(1−0,95) = 20`.

### Fehler 1 — meine Jahreszahl

**Ich hatte geschrieben: „die erste Selektionsfalte beginnt 2022."**
**`research/faltenplan_neun/daten/faltenplan.json` sagt 2019.**

⭐ **Die Sitzung hat nicht still korrigiert, sondern als BEFUND gemeldet — und
mein indirektes Argument durch eine direkte Messung ersetzt.** Statt *„2017–2020
liegt vor 2022, also Vorlauf"* steht jetzt die Messung selbst im Register: **keine
der 36 kurzen ersten Kerzen liegt in einer Falte, in der ihr Symbol geladen
ist.**

> ⭐ **Die Schlussfolgerung hängt damit nicht mehr an meiner Jahreszahl.**

⚠️ **Woher meine 2022 vermutlich kam** — und *vermutlich*, weil ich es nicht
nachgemessen habe: T34.9 nennt *„Symbole je Falte: 3 (2022) → 6 → 9 → 13
(2025)"*, und das ist der **Krypto**-Faltenplan. **2019 dürfte die früheste
Falte über alle neun sein.** ⚠️ **Zwei Zahlen, zwei Fragen — TB-49 Teil 4
misst es.**

### Fehler 2 — meine Regel

**Ich hatte verboten, unter `research/` etwas zu ändern.** Die Sitzung hat sich
daran gehalten — und **den Prüfer, der die neunzehn Zahlen nachrechnet, deshalb
NICHT ins Repo gelegt:**

> *„`pruefe_abschnitt17.py` — **absichtlich nicht im Repo**: der Auftrag
> untersagt Änderungen unter `research/`."*

⚠️ **Folge: Der einzige Prüfer, der Abschnitt 17 nachrechnet, existiert nur in
einem ZIP-Archiv.** ⭐ **Die Sitzung hat sich korrekt verhalten; meine Regel war
zu breit.** **Daraus `ARBEITSWEISE.md` §11 (neu):** Ein Änderungsverbot nennt,
wovor es schützt — und Prüfwerkzeuge, die eine Aufgabe erzeugt, gehören
ausdrücklich ins Repo.

### Fehler 3, zum zweiten Mal — `git status` vor dem letzten Commit

**Wie in TB-46:** Die Statusausgabe im Beleg war **vor** dem abschliessenden
Commit entstanden. Beide Male trug der Zweig die aktuellen Fassungen; **beide
Male war der Beleg wertlos.** **Daraus die Regel in `ARBEITSWEISE.md` §7.**

### In einfacher Sprache

**Was wir wissen wollten:** Kommen die neuen Register-Festlegungen sauber in das
2065 Zeilen lange Vorregistrierungs-Dokument, ohne dass eine alte Zeile
verschwindet?

**Was herauskam:** **Ja — 506 Zeilen hinzugefügt, keine einzige entfernt.** Das
ist mit der git-Zeile belegt, und das eigene Prüfprogramm des Registers findet
keinen Fehler.

**Warum das so ist:** Neunzehn Zahlen wurden nicht abgeschrieben, sondern an
ihrer Quelle nachgerechnet.

**Was das für dich heisst:** ⚠️ **Eine der neunzehn war meine, und sie war
falsch.** Ich hatte geschrieben, der Auswahlzeitraum beginne 2022; der Plan sagt
2019. Die Sitzung hat das gemeldet statt stillschweigend auszubessern — und meine
indirekte Begründung durch eine direkte Messung ersetzt. **Die Aussage, auf die
es ankommt, gilt jetzt unabhängig davon, welche Jahreszahl richtig ist.**
