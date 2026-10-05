# REGISTER-KOPIE Abschnitt 37 (von 0–54) — Register-Z. 6897–7261 — Commit 9b7b06065ebdae3f36f3102306c76bb844300e90 — 2026-10-05 — Original sha256 8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc — KOPIE, nicht das Register

## 37. Die Sonde meldet je Bestandteil, das Abbild führt zwei Gruppen, was ein Befund `1` bedeutet, hängt vom Tag ab, die Tatsachennotiz zu den zwei Listen in `herkunft.py` und der Ort registrierter Werte (Fable 22d und 22g, TB-87, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 bis 36. Fünf Einträge — zwei
Präzisierungen bzw. Ergänzungen zu 36.5 und 36.6 (37.1, 37.2), eine Ergänzung
zu 36.2/36.6 (37.3), eine Tatsachennotiz zu Abschnitt 10 (37.4) und ein
Ersteintrag (37.5) —, alle Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22d_wert_ohne_ort.md` (Antwort auf
die Anfragen 22c und 22d) und
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md` (Antwort
auf die Meldung des steuernden Chats zu TB-86 und zum Sondenbefund an
Sperrlistenpunkt 2). Auftrag `docs/auftraege/MAC_TB-87_register_37.md` (Stufe I,
Punkt 4 aus `PLAN_VOR_DEM_TAG.md`); Messungen `docs/belege/TB-87/` (M1–M6),
M1–M4 **vor** dem Eintrag gemessen, HEAD `40aa715`. ⛔ **Keine `.py` geändert,
kein neues Abbild, keine Sonde angepasst, keine Werte verschoben** — 37.6.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (36.5; 36.6 zweimal;
36.2; Überschrift von Abschnitt 10; Sperrlistenpunkte 7 und 9). Die alten Sätze
bleiben zeichengleich; `git diff --numstat` auf dieses Register zeigt für TB-87
in der zweiten Spalte `0`. ⚠️ Die Marken in Abschnitt 10 stehen als eingerückte
`>`-Zeilen **ohne Leerzeile** unter dem Punkt — so liest die Sperrlisten-Sonde
sie als Notiz und nicht als Punkttext (`shared/sperrlistensonde.py`
`lies_abschnitt_10`, R2); die Sonde ist vor und nach dem Eintrag lesend
gelaufen, Prüfung (ii) beide Male `0`, Listentext wie bei Erzeugung (37.6).

⚠️ **Die Fable-Texte stehen hier in voller Quellform**, auch wo der Auftrag sie
gekürzt zitiert (der Zusatz „, Vorschlag" in den Kopfzeilen von 22d Abschnitt 1
und 22g; „Folge für `herkunft.py`, Entscheidung:"; zwei Begründungen mit „…"):
Eingetragen wird der Quellwortlaut, nicht die Kurzform.

### 37.1 Präzisierung zu 36.5 — die Sonde meldet je Punkt je Bestandteil

**Fable, 22d Abschnitt 1, zeichengleich:**

> **Präzisierung zu 36.5 (Sonden-Ausgänge), Vorschlag:** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil**: für jeden genannten Pfad 0 oder 1 (Hash gegen Abbild), für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts. Der Gesamtwert eines Punktes ist 1, wenn ein Bestandteil 1 ist; sonst 2, wenn ein Bestandteil 2 ist; sonst 0. Der Gesamtwert des Laufs entsprechend. Am Tag gilt: Kein Pfad-Bestandteil darf 1 sein, und jeder Bestandteil mit 2 hat eine Tatsachennotiz, die sagt, wie er stattdessen geprüft wurde (Lesen, Beleg im Auftrag) — oder der Punkt wird bis zum Tag so nachgetragen, dass er messbar ist.

**Fables Grund, 22d Abschnitt 1, zeichengleich:**

> **Eine Präzisierung zur Sonde, damit die `2` nicht mehr verdeckt als sie zeigt:** Ein Punkt wie 14 („`auswertung.py` … Docstring") hat einen messbaren Teil (der Datei-Hash) und einen unmessbaren (der Docstring-Anteil). Eine Sonde, die den ganzen Punkt mit `2` meldet, macht den messbaren Teil unsichtbar.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A2 (nicht prüfbar ist ein eigenes Ergebnis — aber je Sache, nicht je Punkt) und 22c. Kein Ergebnis.

**Tatsachennotiz (TB-87, M1, `m1_sonde_je_bestandteil.txt`):** Die Sonde aus
TB-85 (`shared/sperrlistensonde.py`) **gibt bereits je Bestandteil aus** — im
Nullpunkt-Lauf `docs/belege/TB-85/nullpunkt.txt` zeigt Punkt 1 in einer Zeile
den Datei-Hash (`research/vorregistrierung/registerdaten.py`, `gleich`,
`141fa14b…`) und in der nächsten daneben den unmessbaren Teil (`-> nennt
Nicht-Dateibezogenes - nicht messbar: …`). ⚠️ **Was ihr fehlt, ist der
Rückgabewert je Bestandteil:** Sie meldet den Ausgang je Punkt (Punkt 1 steht
auf `2 NICHT PRUEFBAR`, obwohl sein einziger Pfad `gleich` ist) und einmal je
Lauf. Genau das ist der Fall, den Fables Grund beschreibt — der messbare Teil
verschwindet im Ausgang hinter dem unmessbaren. Das nachzuziehen ist Handwerk
mit eigener Freigabe, **nicht** dieser Eintrag.

**Marke am alten Ort:** in **36.5**, direkt unter dem Registertext.

### 37.2 Ergänzung zu 36.6 — das Abbild führt zwei Gruppen

**Fable, 22d Abschnitt 2, zeichengleich:**

> **Ergänzung zu 36.6 (Abbild der Sperrliste):** Das Abbild führt zwei Gruppen: die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade — Dateien, die das Register für die Sperrliste vorsieht, deren Vollzug aber aussteht (heute: `ergebnisse/benchmark_drawdowns_vt.json`, 21.9/23.7). Die Sonde prüft beide Gruppen gleich (Hash gegen Abbild) und weist die Gruppe im Bericht aus. **Am Tag ist die zweite Gruppe leer:** Jeder bestimmte Pfad hat bis dahin seinen Punkt in Abschnitt 10, oder das Register sagt, warum nicht.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* Schreibregel 22b (1) („oder für sie bestimmt ist") — was die Schreibregel schützt, muss die Sonde sehen; sonst ist der Schutz eine Regel ohne Wache (A8). Und die Sperrliste ist am Tag vollständig oder sie ist keine. Kein Ergebnis.

**Tatsachennotiz (TB-87, M1):** Das Abbild `sperrliste_abbild_2026-09-22.json`
(`6a1b732e…`) führt heute die Punkte; die Sonde **nennt** den bestimmten Pfad
`ergebnisse/benchmark_drawdowns_vt.json` am Ende ihres Berichts mit Hash
`4549395f…`, **prüft ihn aber nicht** — ihr eigener Wortlaut: „Bestimmt, nicht
eingetragen (kein Punkt des Abschnitts 10; nicht geprueft, nur genannt)".
Der Unterschied zum Registertext oben (beide Gruppen gleich prüfen, Gruppe
ausweisen) ist Handwerk mit eigener Freigabe; hier nur festgehalten.

> ⭐ **Gruppenwechsel und Vollzug (39.3/39.2, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Gruppe „bestimmt" **wechselt** von
> `ergebnisse/benchmark_drawdowns_vt.json` auf die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`) —
> und deren Pfad steht seit 39.2 in Sperrlistenpunkt 4. **Nach dem
> Registertext ist die Gruppe damit leer.** `_vt.json` und `_tb72.json` kommen
> nicht auf die Liste (Tatsachennotizen in 39.3). ⚠️ Die Sonde führt die
> Gruppe als feste Konstante und nennt weiter `_vt.json` mit „Vollzug steht
> aus" (39.3, Ausgabe in 39.9); das zu ändern ist Handwerk mit eigener
> Freigabe.

> ⭐ **Die Gruppen kommen aus dem Abbild (40.8 (e), Fable 24a, TB-96,
> 24.09.2026):** Dass die Sonde die Gruppe „bestimmt" als feste Konstante führt
> (`BESTIMMT_NICHT_EINGETRAGEN`), ist nach Fable „ein Befund, vor dem Tag zu beheben"
> — nicht mehr Handwerk ohne Frist. Die Sonde liest alle drei Gruppen aus dem
> Abbild; das Abbild führt „bestimmt" heute leer (39.3). Gegenprobe: Abbild mit
> erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn. TB-97.

**Marke am alten Ort:** in **36.6**, direkt unter dem Registertext.

### 37.3 ⭐⭐ Ergänzung zu 36.2/36.6 — was ein Befund `1` bedeutet, hängt vom Tag ab

⚠️ **Das ist die Lücke, die TB-86 sichtbar gemacht hat:** Die Sonde meldet
seit TB-86 an Sperrlistenpunkt 2 den Befund `1` — und bis hier stand nirgends,
ob das ein Sperrlistenbruch ist.

**Fable, 22g, zeichengleich:**

> **Ergänzung zu 36.2/36.6, Vorschlag:** Ein Befund 1 der Sperrlisten-Sonde **vor dem signierten Tag** ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein **neues Abbild unter neuem Namen** geschlossen, nie durch Anpassung des alten. Ein Befund 1 **nach dem Tag** ist ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Das **letzte Abbild vor dem Tag** wird nach der letzten Codeänderung erzeugt, trägt die Hashes des Tag-Commits und steht selbst mit Hash im Register; der Tag setzt voraus, dass die Sonde gegen dieses Abbild 0 liefert (oder 2 mit Tatsachennotiz nach 22d).

**Fables Grund, 22g, zeichengleich:**

> **Der Satz, der fehlt — und den der Befund verlangt:** Die Sperrliste sagt „**ab dem signierten Tag** sind unveränderlich". Vor dem Tag ändern sich Sperrlistenpfade planmässig (TB-86 heute, Z. 336 morgen, die Werte-Module nach 22d). Die Sonde kann diesen Unterschied nicht kennen; sie meldet 1, und was 1 **bedeutet**, hängt vom Datum ab. Das gehört ins Register, sonst liest jemand den heutigen Befund als Bruch — oder, schlimmer, einen Bruch nach dem Tag als „planmässig".

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* der Wortlaut von Abschnitt 10 („ab dem signierten Tag") und 36.6 (Abbild einmalig, neu statt angepasst). Kein Ergebnis.

⭐ **Und sein Satz zur Sonde, 22g, zeichengleich:**

> *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

(Aus 22g, Absatz „Punkt 2b — ja, genauso", voller Absatz:)

> **Punkt 2b — ja, genauso:** Sperrlistenpunkt 2 nennt zwei Pfade; `faltenplan.py` hat sich durch beauftragte Änderung bewegt; die Sonde meldet 1 und repariert nichts — richtig, denn das Abbild trägt den alten Hash, und ein Abbild wird nach 36.6 nicht angepasst, sondern **neu** geschrieben, unter neuem Namen, das alte bleibt. Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde.

**Sein Hinweis zum Handwerk, ausdrücklich nicht Verfahren, zeichengleich:**

> *Handwerk daraus, nicht Verfahren:* Nicht nach jeder Änderung ein neues Abbild ziehen, sondern nach Bündeln (etwa nach 2+3 zusammen, nach 6, vor 11) — jedes Abbild bleibt ohnehin liegen. Wie viele es werden, ist gleichgültig; dass das letzte zum Tag-Commit passt, ist alles.

⭐⭐ **Tatsachennotiz — der erste Anwendungsfall (TB-87, M2,
`m2_faltenplan_hash.txt`):** TB-86 hat `research/vorregistrierung/faltenplan.py`
**beauftragt und freigegeben** geändert — Auftrag
`docs/auftraege/MAC_TB-86_faltenplan_schreibsperre.md`, Betreiberfreigabe
22.09.2026, 07:50 (Schritt 1 und 2 aus 36.3), Commit `4daa254`. Der Hash ging
von **`6f96b95d13563f73b11be69c2bd6996037854df794da61315029216ad0b22bd9`** (so im
Abbild `sperrliste_abbild_2026-09-22.json`, `6a1b732e…`, Punkt 2) auf
**`fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79`** (heute,
gemessen). Die Sonde meldet seither an Punkt 2 **`1 BEFUND`**, Lauf gesamt `1`
(`docs/belege/TB-86/schritt8_sonde.txt`; lesend wiederholt vor diesem Eintrag,
`docs/belege/TB-87/sonde_vorher.txt`). ⭐ **Nach dem Registertext oben ist das
der planmässige Fall vor dem Tag** — Auftrag, Freigabe, alter und neuer Hash
stehen hiermit als Tatsachennotiz. **Geschlossen wird er mit einem neuen Abbild
unter neuem Namen** (Plan Punkt 2b); das ist **nicht** Gegenstand dieses
Eintrags, und das alte Abbild bleibt.

> ⭐⭐ **Die weiteren Übergänge und ihr Abbild (39.5/39.9, TB-94,
> 23.09.2026):** Nach TB-86 haben sich planmässig bewegt: `faltenplan.py`
> `fd3e5018…` → `7aa0b8cc…` (TB-90, `303a7fd`, Punkt 2), `benchmark.py`
> `3960375a…` → `d6bdd558…` (TB-91, `31008b6`, Punkte 4 und 6),
> `auswertung.py` `1c2e2dae…` → `c3b4e69d…` (TB-92, `0292e92`, Punkte 3, 5
> und 14); dazu `registerbericht.py` und `test_vorregistrierung.py` (TB-92,
> auf keinem Punkt). Auftrag, Freigabe und volle Hashes stehen in **39.5**.
> Geschlossen werden der Fall oben und diese Übergänge mit **einem** neuen
> Abbild (**39.9**); `sperrliste_abbild_2026-09-22.json` bleibt.

> ⭐⭐ **Die Übergänge seit 39.5 und ihre Abbilder (42.5, TB-108, 25.09.2026):**
> Planmässig bewegt haben sich `messgroessen.py` (TB-103, `EINGEFROREN`),
> `benchmark.py` und `faltenplan.py` (TB-104 und TB-106, Punkte 2, 4, 6),
> `auswertung.py` (TB-106, Punkte 3, 5, 14) und `herkunft.py` (TB-106, Punkte 11
> und 12). Auftrag, Freigabe und volle Hashes stehen in **42.5**. Geschlossen
> durch `sperrliste_abbild_2026-09-25.json` (`cb4eb1b4…`, TB-104) und
> `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`, TB-106); die älteren
> Abbilder bleiben.

**Marken am alten Ort — zwei:** in **36.2**, direkt unter dem Registertext
(unter der Marke aus 36.5), und in **36.6**, direkt unter dem Registertext
(unter der Marke aus 37.2).

### 37.4 Tatsachennotiz zu Abschnitt 10 — die zwei Listen in `herkunft.py`

⭐ Das ist die Tatsachennotiz, die 36.6 als **ausstehend** eingetragen hat
(„wird in diesem Abschnitt NOCH NICHT geschrieben"). **Fables eigene
Tatsachennotiz, 22d Abschnitt 3, zeichengleich:**

> **Tatsachennotiz zu Abschnitt 10 (22.09.2026):** `research/vorregistrierung/herkunft.py` trägt zwei Listen. **`EINGEFROREN`** (Z. 57, zehn Einträge) ist die Eingabe von `register()` (Z. 114): ein Gesamthash über die Registerdatei plus diese zehn Dateien, laut Docstring „über die eingefrorenen Festlegungen" — sie bildet die Menge aus **Abschnitt 0** ab, nicht die Sperrliste aus Abschnitt 10, und weicht von dieser an fünf Stellen ab (fehlend: `benchmark_drawdowns_vt.json`, `config/top25_symbols.txt`, `config/sp500_top150.txt`; zusätzlich: `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`). **`SPERRLISTE_DATEIEN`** (Z. 66) wird von keiner Stelle gelesen — toter Code. Keine der beiden Listen ist das Abbild der Sperrliste (36.6). `herkunft.py` wird in `research/vorregistrierung/` von keinem Modul importiert; `herkunft.json` und `herkunft_protokoll.jsonl` existieren nicht; die einzigen Aufrufer von `block()` gehören zu `research/turn_of_month/`. Sperrlistenpunkte 11 und 12 verweisen damit auf Funktionen, die im Laufbereich heute niemand aufruft; der Datenvertrag (`auswertung.py` Z. 41) verlangt `herkunft.json` als Pflichteingabe. Der Erzeuger (Nachtrag 2) ist die Stelle, an der `register()` und `datenstand()` erstmals aufgerufen werden.

> ⚠️ **ERSETZT (38.6, Fable 22h, TB-89, 23.09.2026) — zwei Stellen dieses
> Satzes, der Satz selbst bleibt zeichengleich:** (a) „`auswertung.py` Z. 41"
> lies **Z. 51** (Fables Berichtigung (a)). (b) Der Halbsatz „weicht von dieser
> an fünf Stellen ab (fehlend: …; zusätzlich: …)" ist ersetzt durch Fables
> Ersatzsatz — acht Stellen, vier fehlend und vier zusätzlich; der Wortlaut
> steht zeichengleich in **38.6**. Beleg ist die Tatsachennotiz TB-87 (M3)
> unten.

**Und seine Entscheidung dazu, zeichengleich:**

> **Folge für `herkunft.py`, Entscheidung:** **Nicht öffnen.** Der Erzeuger ruft `register()` auf und schreibt in `herkunft.json` **auch das Feld `teile`** (das `register()` liefert und `block()` weglässt) — dann ist lesbar, welche Dateien in den Gesamthash eingingen, ohne dass `block()` oder `herkunft.py` geändert wird. `herkunft.json` bezeugt damit die Abschnitt-0-Menge (zehn Dateien plus Register); die Sperrlisten-Sonde bezeugt Abschnitt 10; die Tatsachennotiz oben sagt, welches Dokument was bezeugt. Zwei Nachweise mit verschiedenem Gegenstand sind kein Widerspruch — zwei Nachweise mit demselben Gegenstand und verschiedenem Inhalt wären einer. *Quelle des Grundes:* 21b (3), Einfrieren vor Umbau; der Erzeuger ist neuer Code, dort darf alles stehen. Kein Ergebnis.

> ⭐⭐ **BERICHTIGT durch 42.3 F2 (Fable 25c, TB-108, 25.09.2026):** `herkunft.py`
> ist **einmal planmässig geöffnet** worden (TB-106, `5791b4c`), um
> `datenstand()` den Datenpfad durch `block()` und `anhaengen()` durchzureichen;
> sonst gilt die Entscheidung oben: `EINGEFROREN` bleibt, `register()` bezeugt
> die Abschnitt-0-Menge, die Sonde Abschnitt 10. **Planmässig geöffnet heisst
> nicht offen.** Hash `56a1c2e1…` → `351f24c2…` (42.5). Die Entscheidung oben
> bleibt zeichengleich.

> ⭐ **Zweite planmässige Öffnung geplant (43.1, 43-4, Fable 25d, TB-110,
> 26.09.2026):** `herkunft.py` wird ein zweites Mal geöffnet, für zwei Dinge in
> **einer** Öffnung — die Prüfansicht übergibt unter dem Modus
> `paths.DATA_DIR`, und `TB30A_BASE_DIR` endet unter dem Modus mit 2, bevor
> gelesen wird —, mit dem Erzeuger oder vor ihm. **Noch nicht vollzogen**
> (`351f24c2…` unverändert). Die Entscheidung oben und ihre Berichtigung
> bleiben zeichengleich.

> ⭐ **Zweite Öffnung `herkunft.py` vollzogen, TB-111, siehe 44.1 (44-2;
> TB-113, 26.09.2026):** In `6cacfa4` (zusammengeführt in `257e7db`): die
> Prüfansicht übergibt unter dem Modus `paths.DATA_DIR`, `TB30A_BASE_DIR`
> endet unter dem Modus mit 2 vor dem Lesen, `paths.py` kommt aus der eigenen
> Wurzel. `351f24c2…` ⇒ `5bbfc9e0…`. `EINGEFROREN` bleibt; die Entscheidung
> oben, ihre Berichtigung und die Marke darüber bleiben zeichengleich.

**Tatsachennotiz (TB-87, M3, `m3_herkunft_listen.txt`) — nachgemessen, nicht
übernommen:**

| Aussage in Fables Notiz | gemessen | |
|---|---|---|
| `EINGEFROREN` Z. 57, zehn Einträge | **Z. 57**, zehn Einträge | ✔ |
| `SPERRLISTE_DATEIEN` Z. 66, von keiner Stelle gelesen | **Z. 66**, fünf Muster; ausser der Definition nur in einem **Kommentar** von `shared/sperrlistensonde.py:70` genannt, nirgends gelesen | ✔ |
| Eingabe von `register()` (Z. 114) | **Z. 114** `for rel in ([…REGISTERDATEI…] + EINGEFROREN):` | ✔ |
| `herkunft.py` in `research/vorregistrierung/` von keinem Modul importiert | **0** `import`/`from`; zwei Textfundstellen (Docstring `auswertung.py`, Beispieldaten-Schreiber `beispieldaten.py:142/145`) | ✔ |
| `herkunft.json`, `herkunft_protokoll.jsonl` existieren nicht | **existieren nicht** | ✔ |
| einzige Aufrufer von `block()` in `research/turn_of_month/` | **`auswertung.py:206`, `staging.py:127`**, beide dort | ✔ |
| Datenvertrag `auswertung.py` **Z. 41** | ⚠️ **Z. 51** (`<wurzel>/<bot>/herkunft.json`), Z. 52 „siehe herkunft.py"; Z. 41 ist `mittlere_exposure` | **abweichend** |
| „weicht … an **fünf** Stellen ab (fehlend: drei; zusätzlich: drei)" | ⚠️ siehe unten | **abweichend** |

⚠️ **Die Abweichungszahl, gemessen:** Fable schreibt „fünf Stellen" und nennt
sechs Namen. Der mechanische Mengenvergleich der zehn `EINGEFROREN`-Einträge
(auf Repo-Pfade aufgelöst) gegen die zehn Pfade der vierzehn Punkte (aus dem
Abbild `6a1b732e…`, das die Sonde mit Prüfung (ii) `0` gegen Abschnitt 10 prüft)
ergibt:

- **in Abschnitt 10, nicht in `EINGEFROREN` — vier:** `config/top25_symbols.txt`,
  `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py` (Punkte 11,
  12), `shared/zuteilung.py` (Punkt 10); **dazu** der bestimmte Pfad
  `ergebnisse/benchmark_drawdowns_vt.json` (kein Punkt, 37.2);
- **in `EINGEFROREN`, kein Pfad eines Punktes — vier:** `kennzahlen.py`,
  `messgroessen.py`, `pruefe_grenzsaetze.py` **und**
  `ergebnisse/messgroessen.json`.

Alle sechs Namen in Fables Notiz stimmen; **nicht genannt** sind dort
`herkunft.py`, `shared/zuteilung.py` und `ergebnisse/messgroessen.json`. Das
ändert seine Folgerung nicht — `EINGEFROREN` bildet die Abschnitt-0-Menge ab,
nicht Abschnitt 10 —, aber die Zahl „fünf" gilt so nicht; **eingetragen ist,
was gemessen ist**, Fables Satz bleibt zeichengleich stehen. Gemeldet im
Ergebnisdokument.

**Randbefund aus TB-84, nachgemessen:** `research/etf_trendfolge/datenstand.py`
Z. 43–49 lädt `research/vorregistrierung/herkunft.py` über
`reg.lade_fremdes_modul(…)` und ruft `herkunft.datenstand(…)` auf — ein Nutzer
ausserhalb von `turn_of_month/` und ausserhalb des Laufbereichs der
Vorregistrierung. Fables Satz über den **Laufbereich** bleibt damit richtig;
vollständig beantwortet „wer liest `herkunft.py`" er nicht.

> ⚠️ **Ergänzung (39.7, Fable 23d, TB-94, 23.09.2026) — `EINGEFROREN` ist nach
> dem Vollzug nicht vollständig:** `EINGEFROREN` hasht weiter
> `ergebnisse/benchmark_drawdowns.json` (historischer Stand), **nicht** die
> Tabelle, die der Lauf liest (`ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`,
> 39.2). `herkunft.py` bleibt ungeöffnet (`56a1c2e1…`). Der Satz, um den Fable
> diese Tatsachennotiz ergänzt (23d Abschnitt 1 (2)), zeichengleich:
> „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde."
> Nach Fables Präzisierung zu 36.1 (1) (23c) ist auch jeder Pfad in
> `EINGEFROREN` gesperrt — Wortlaut in **39.7**.

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, unter dem
Hinweis aus 36.2/36.6 (der „ihre Tatsachennotiz steht bei Fable aus" sagt —
bleibt zeichengleich stehen).

### 37.5 Registertext „Ort registrierter Werte" — Ersteintrag

**Fable, 22d Abschnitt 4, zeichengleich:**

> **Registertext, Ersteintrag — Ort registrierter Werte:**
> **(1)** Jeder Sperrlistenpunkt, der einen Zahlenwert registriert (heute 7 und 9), nennt **genau ein** Modul und dort **genau eine** Konstante, aus der der Lauf diesen Wert liest. Dieses Modul steht mit Hash auf der Sperrliste; die Sonde prüft für den Punkt Datei-Hash **und** Wert der Konstante (Bauart „Datei plus Konstante", wie Punkte 3, 4, 10).
> **(2)** Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie. Für den Papierpfad (`forward_test.py`) gilt das nicht als Sperre, aber als Konsistenzprüfung: Die Sonde meldet als Befund, wenn eine Kopie dort vom registrierten Wert abweicht.
> **(3)** Für Punkt 9: `TRADING_FEE_PCT` und `SLIPPAGE_PCT` in einem Modul; für Punkt 7: `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` in einem Modul. Welche Module (Kandidaten nach heutiger Messung: `messgroessen.py` für 9, `registerdaten.py` für 7) und ob eines der beiden Module bereits Abschnitt-0-eingefroren ist und deshalb ein neues kleines Modul die Werte tragen muss — **Handwerk mit Freigabe**, aber die Tatsachennotiz zu 7 und 9 nennt am Ende Modul, Zeile und Wert.
> **(4)** Tatsachennotiz zu 7 und 9, jetzt: die heute gemessenen Orte (neun `forward_test.py`; `messgroessen.py:59`; `registerdaten.py:99`, `:115`) mit dem Vermerk, dass der Registertext keinen davon nennt und der Zustand bis zur Umsetzung von (1)–(3) ungeschützt war.

> ⭐⭐ **Entscheidung zu (2) und (3) (38.5, Fable 22h, TB-89, 23.09.2026):** Es
> bleibt bei (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun
> `backtest_*.py` beziehen `TRADING_FEE_PCT` / `SLIPPAGE_PCT` künftig per
> Import aus einem **neuen** Modul (die Kandidaten aus (3) sind blockiert); der
> Papierpfad und `messgroessen.py` / `GEBUEHR_PCT` bleiben überwachte Kopien.
> **Für Punkt 7 ist (3) schon erfüllt:** `registerdaten.py` ist der Ort, nichts
> wird verschoben. Wortlaut und Begründung in **38.5**.

**Fables Befund, aus dem der Eintrag folgt, zeichengleich** (darin sein
Kernsatz *„Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt
nichts — er legt fest."*):

> **Der Befund in einem Satz:** Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt nichts — er legt fest. Festlegen ist Aufgabe der Festlegungen und des Registertexts; die Sperrliste soll sagen, **was unverändert bleibt**, und das ist immer eine Datei (oder ein Ort in einer). „Ändert jemand `TRADING_FEE_PCT` in einer der neun `forward_test.py`, merkt es kein Sperrlistenpunkt" ist genau der Zustand, den der Tag ausschliessen soll.

**Seine Abwägung der drei Wege, zeichengleich:**

> **Zu den drei Wegen:** *(iii) so lassen und Notiz* — nein: eine Tatsachennotiz macht eine Lücke sichtbar, sie schliesst sie nicht; der Tag friert dann eine Sperrliste ein, von der man weiss, dass sie zwei Werte nicht schützt. *(i) Ort je Punkt nachtragen* allein — nicht ausreichend, denn der Ort, den man heute misst (neun `forward_test.py`), ist nicht notwendig der Ort, aus dem der **Lauf** den Wert liest: `forward_test.py` ist der Papierpfad; die Optimierer und der noch zu schreibende Erzeuger sind der Laufpfad. Neun Kopien eines Werts als Sperrlistenorte einzutragen registriert die Kopien, nicht die Quelle. *(ii) Werte in eine Datei ziehen und sperren* — das ist der Kern, aber „ziehen" darf keine Kopie mehr erzeugen.

**Seine Quelle des Grundes — und der Satz, der Missverständnisse ausschliesst,
zeichengleich:**

> *Quelle des Grundes:* Zweck der Sperrliste (Übergabe Abschnitt 5) und A8; der Grundsatz ein Wert, ein Ort aus 21j. **Kein Ergebnis — und das ist hier wichtig zu sagen:** Die Werte selbst (0,1 / 0,05 / die beiden aus Punkt 7) ändern sich nicht um ein Zeichen; es ändert sich nur, wo sie stehen und dass jemand es merkt, wenn sie sich ändern.

**Tatsachennotiz zu Punkt 7 und 9 nach (4) (TB-87, M4, `m4_werte_orte.txt`) —
die heute gemessenen Orte:**

| Wert (Punkt) | Ort | Zeile | Wert im Code |
|---|---|---|---|
| `TRADING_FEE_PCT` (9) | neun `strategies/*/forward_test.py` | je eine Zuweisung (Z. 57–72) | `0.1` |
| `SLIPPAGE_PCT` (9) | neun `strategies/*/forward_test.py` | je eine Zuweisung (Z. 58–73) | `0.05` |
| `SLIPPAGE_PCT` (9) | `research/vorregistrierung/messgroessen.py` | **:59** | `0.05` |
| ⚠️ Gebühr (9) | `research/vorregistrierung/messgroessen.py` | **:58**, Name **`GEBUEHR_PCT`** — nicht `TRADING_FEE_PCT` | `0.1` |
| `CLUSTER_SCHWELLE` (7) | `research/vorregistrierung/registerdaten.py` | **:99** | `0.90` |
| `N_HISTORISCH_JE_BOT` (7) | `research/vorregistrierung/registerdaten.py` | **:115** (neun Einträge bis Z. 125, Summe 653) | Wörterbuch |

⚠️ **Zwei Abweichungen von Fables (4), gemessen:** (a) `messgroessen.py:59`
trägt nur `SLIPPAGE_PCT`; die Gebühr steht eine Zeile davor unter **anderem
Namen** (`GEBUEHR_PCT`) — für (3) heisst das: in `messgroessen.py` gibt es heute
**keine** Konstante `TRADING_FEE_PCT`. (b) **Nicht genannt, aber gemessen:**
Auch die neun `backtest_*.py` der Bots tragen je eine eigene Zuweisung
`TRADING_FEE_PCT = 0.1` / `SLIPPAGE_PCT = 0.05`
(`elliott_wave/backtest_elliott.py:73–74`,
`elliott_wave_stocks/backtest_elliott.py:77–78`, `rsi2_crypto/backtest_rsi2.py:58–59`,
`rsi2_mean_reversion/backtest_rsi2.py:85–86`, `t3_supertrend/backtest_trend.py:27–28`,
`turtle_soup_crypto/backtest_turtle_soup.py:96–97`,
`turtle_soup_stocks/backtest_turtle_soup.py:92–93`,
`volatility_breakout/backtest_breakout.py:105–106`,
`volatility_breakout_crypto/backtest_breakout.py:73–74`), dazu
`elliott_wave_stocks/signal_quality_test.py:37–38` als Verweis auf
`backtest_elliott`. **Ob der Laufpfad daraus liest, ist die Messung aus Plan
Punkt 5 — hier nicht gemessen.** Alle gemessenen Werte sind zeichengleich
`0.1` / `0.05` / `0.90`.

⚠️ **Vermerk nach (4):** Der Registertext von Punkt 7 und 9 nennt **keinen**
dieser Orte; der Zustand war bis zur Umsetzung von (1)–(3) **ungeschützt**.

**Fables Frage vor der Umsetzung, zeichengleich:**

> *Warum die Optimierer die Kosten heute vielleicht gar nicht aus `forward_test.py` lesen:* Das habe ich nicht gemessen und ihr nicht gefragt. **Nur das Ob, vor der Umsetzung:** Woher beziehen die neun `multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und Slippage — aus einer eigenen Konstante, aus `forward_test.py`, aus `messgroessen.py`, oder gar nicht? Wenn die Antwort „aus einer eigenen Konstante je Bot" lautet, gibt es neun weitere Kopien, und (2) ist grösser als eine Zeile.

⚠️⚠️ **Offen (Fable 22d), zeichengleich:**

> **Unsicher:** ob `messgroessen.py` und `registerdaten.py` als Abschnitt-0-eingefrorene Dateien für (3) noch geändert werden dürfen — wenn nicht, trägt ein neues kleines Modul die vier Werte, und die eingefrorenen Dateien bleiben stehen. Das seht ihr im Register (Abschnitt 0 und 15.8), ich nicht.

⭐ **Dazu gehört die Messung aus Plan Punkt 5:** woher beziehen die neun
`multi_symbol_optimise.py` und `equity_simulation.py` heute Kosten und
Slippage? ⛔ **Beides nicht Gegenstand dieses Eintrags.** Die Werte bleiben, wo
sie sind; Fables Kandidaten-Module (`messgroessen.py`, `registerdaten.py`)
sind Abschnitt-0-eingefroren (`herkunft.py` `EINGEFROREN`, 37.4) — ob sie für
(3) geändert werden dürfen, entscheidet nicht dieser Abschnitt.

**Marken am alten Ort:** bei **Sperrlistenpunkt 7** und bei **Punkt 9**.

### 37.6 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Die Sonde ändern** — sie meldet ihren Ausgang heute je Punkt; 37.1 verlangt ihn je Bestandteil, 37.2 die Prüfung der Gruppe „bestimmt" | Handwerk, eigene Freigabe |
| ⛔ | **Ein neues Abbild erzeugen** (Plan Punkt 2b) — der Befund `1` an Punkt 2 (37.3) bleibt bis dahin stehen; das Abbild `6a1b732e…` bleibt | eigene Aufgabe |
| ⛔ | **Werte verschieben** („ein Wert, ein Ort", 37.5 (1)–(3), Plan Punkt 6) — braucht erst die Messung aus Plan Punkt 5 | Betreiber, Freigabe |
| ⛔ | **`herkunft.py` öffnen** — Fables Entscheidung 37.4: nicht öffnen | — |
| ⛔ | **Irgendeine `.py` ändern** · ⚠️ `python3 faltenplan.py` — nicht aufgerufen | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (M5); die drei Sperrlisten-Hashes `0e54ac5c…`, `a163c498…`, `4549395f…` unverändert (M6); die Sperrlisten-Sonde lesend vor und nach dem Eintrag: Prüfung (ii) `0`, Listentext wie bei Erzeugung, unverändert `1` nur an Punkt 2 | — |
| ⚠️ | **Offen:** die Sonde muss je Bestandteil **zurückgeben** (37.1) · die Gruppe „bestimmt" **prüfen** (37.2) · das neue Abbild (Plan 2b, schliesst 37.3) · die Messung aus Plan 5 (woher lesen die Optimierer Kosten?) · Fables Unsicherheit zu den eingefrorenen Modulen (37.5) · die zwei Messabweichungen in 37.4 (Z. 51 statt 41; vier/vier statt „fünf") und in 37.5 (`GEBUEHR_PCT`; neun `backtest_*.py`) — Fable zur Kenntnis | Betreiber / Fable |

*Dieser Abschnitt ist rein additiv: Er trägt zwei Präzisierungen bzw.
Ergänzungen, eine Ergänzung zur Bedeutung eines Sondenbefunds, eine
Tatsachennotiz und einen Ersteintrag des Verfahrensprüfers zeichengleich ein;
setzt sieben Marken am alten Ort; hält die nachgemessenen Tatsachen samt vier
Abweichungen fest — und entfernt nichts. Gebaut wird nichts.*

