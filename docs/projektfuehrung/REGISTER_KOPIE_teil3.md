# REGISTER-KOPIE Teil 3 von 4 — Abschnitte 37–42 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

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

## 38. Weg (A) — die letzte Falte heisst die Spanne, Fundstellen als Datei und Bezeichner, der Vollzug von Punkt 4 nach 37.3 in Form (ii), neun Importe statt überwachter Kostenkopien, zwei Berichtigungen des Verfahrensprüfers an sich selbst und die Messungen aus TB-88 (Fable 22h, TB-89, 23.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34 bis 37. Sechs Einträge des
Verfahrensprüfers — eine Berichtigung zu 35.1 (38.1), ein Ersteintrag für alle
künftigen Registertexte (38.2), eine Tatsachennotiz zu 21.9 und 10.1 (38.3),
die Form von Sperrlistenpunkt 4 (38.4), die Entscheidung zu den Kostenkopien
(38.5) und zwei Berichtigungen an seinem eigenen Text (38.6) —, alle Fable-Texte
zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md`
(Antwort auf die Anfragen 22f und 22h). Dazu die Tatsachennotizen aus TB-88
(38.7; `docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`) und der
Schlussteil (38.8). Auftrag `docs/auftraege/MAC_TB-89_register_38.md`; Belege
`docs/belege/TB-89/`; Eingang `c140ca9`, Schritt-0-Commit `da251da`.
⛔ **Keine `.py` geändert, kein neues Modul, kein Import, kein neues Abbild,
keine Sonde angepasst, kein Vollzug, kein Wert verschoben** — 38.8.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Kopf von
Abschnitt 0; 35.1 dreimal; 21.9 zweimal; 10.1; Sperrlistenpunkte 4 und 7,
Punkt 9 zweimal; 23.7; 37.4; 37.5 — vierzehn). Die alten Sätze bleiben zeichengleich; `git diff --numstat`
auf dieses Register zeigt für TB-89 in der zweiten Spalte `0`. Die Marken in
Abschnitt 10 stehen, wie seit 37, als eingerückte `>`-Zeilen **ohne
Leerzeile** unter dem Punkt; die Sperrlisten-Sonde ist vor und nach dem
Eintrag **lesend** gelaufen (38.8).

⭐ **Dieser Abschnitt wendet 38.2 schon auf sich selbst an:** Fundstellen im
Code stehen hier als Datei und Bezeichner; wo eine Zeilennummer steht, steht
sie in einer Tatsachennotiz und trägt den Commit, an dem sie gemessen wurde.
In den **Zitaten** stehen Zeilennummern, wie Fable sie geschrieben hat —
zeichengleich heisst zeichengleich.

### 38.1 ⭐⭐ Berichtigung zu 35.1 (Folge/Handwerk) — Weg (A): die letzte Falte heisst die Spanne

**Fable, 22h Abschnitt 3, zeichengleich — sein Befund:**

> Ihr habt recht, und der Befund ist meiner: 35.3 nennt den Bezeichner einen Schlüssel, den zwei Programme teilen, und 35.1 sagt trotzdem „eine Zeile". Ein Schlüssel, der an einer Stelle gebildet und an einer anderen verglichen wird, ist nie eine Zeile.

**Die Entscheidung, zeichengleich:**

> **Berichtigung zu 35.1 (Folge/Handwerk):** Der Bezeichner der Bestätigungsperiode entsteht **an der Stelle, an der die letzte Falte ihren Namen bekommt** (heute `faltenplan.py`, die Zuweisung der Rolle `bestaetigung`, Umgebung Z. 307) — die letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`. `falten[-1]["name"]`, `plan[bot]["bestaetigungsperiode"]`, die Spalte `falte` der Bestätigungszeile in `zellen.csv` und der Bericht tragen damit denselben String aus derselben Quelle; `auswertung.py`, `beispieldaten.py` und `registerbericht.py` bleiben unberührt. Weg (B) — zwei Namen für dieselbe Periode — ist unzulässig.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 35.3 (ein Schlüssel, zwei Programme) und der Grundsatz ein Wert, ein Ort (21j, 37). Weg (B) erzeugt genau das Paar, das 35 abschaffen sollte: einen Faltennamen `2026`, der siebzehn Monate verspricht, und einen Bezeichner daneben, der es richtigstellt. Kein Ergebnis.

**Zu dem Einwand des steuernden Chats gegen (A), zeichengleich** (33.3 führt
die Selektionsfalten als Feld, die Bestätigungsperiode als eigenes Feld; der
Schrägstrich ist mit Absicht kein Bindestrich):

> *Zu eurem Einwand gegen (A)* („der Faltenname einer Falte trägt dann eine Spanne, die übrigen Jahre — und 33.3 führt den Faltennamen als Feld"): 33.3 führt die **Selektionsfalten** als Feld (`selektionsfalten`, Liste von Kalenderjahren) und die Bestätigungsperiode als **eigenes** Feld (35). Die Bestätigungsperiode ist keine Selektionsfalte (35) und steht deshalb nicht in der Liste — die Sonde prüft, dass `selektionsfalten` nur Kalenderjahre enthält und der Spannen-Bezeichner nur im Feld `bestaetigungsperiode` steht. Dass die Bestätigungsfalte im Code als letztes Element der Faltenliste mit Rolle `bestaetigung` geführt wird, ist Umsetzung und kein Widerspruch, solange das Abbild die Rollen trennt. Und der Schrägstrich in `JJJJ-MM-TT/JJJJ-MM-TT` ist mit Absicht kein Bindestrich: Ein Doppeljahr heisst `2018-2019`, eine Spanne heisst `…/…` — zwei Formen, die sich nicht verwechseln lassen.

**Sein Handwerk daraus, zeichengleich** (das Fertigkriterium darin betrifft
38.7 (d)):

> *Handwerk daraus:* Die Änderung ist eine Stelle in `faltenplan.py` (Namensbildung der Bestätigungsfalte), nicht Z. 338; danach Ausgabevergleich wie bei TB-86: alle Selektionsfalten zeichengleich, genau ein String verändert, je Bot; `test_vorregistrierung.py` grün, gemessen auf dem Mac (TB-88).

**Seine Unsicherheit, zeichengleich:**

> **Unsicher:** ob `test_vorregistrierung.py` eine Prüfung enthält, die den Faltennamen der Bestätigungsfalte als Jahr erwartet — dann wird sie unter (A) rot und muss als Prüfung an 35 angepasst werden (der Test folgt dem Register, nicht umgekehrt); TB-88 sieht es.

⚠️⚠️ **Tatsachennotiz — Weg (B) hätte einen Sperrlistenpunkt berührt (TB-88,
M2b, `m2b_wege_a_b_probe.py`, nur im Speicher, Messstand `8851f67`):**
`research/vorregistrierung/auswertung.py`, Funktion `lies_zellen`, vergleicht
die **Menge** der `falte`-Werte je Zelle gegen die Faltennamen des Plans
(`[f["name"] for f in plan[bot]["falten"]]`, Z. 177–182 am Stand `8851f67`).
Schreibt der Erzeuger unter (B) den Bezeichner in die Spalte `falte`, bricht
die Auswertung **dort** ab (*„Falten stimmen nicht mit dem Faltenplan
ueberein"*); schreibt er den Faltennamen (B′), bricht sie in der Funktion
`bestaetigungsperiode` ab. Weg (A) läuft in derselben Probe durch
(`falte: '2026-01-01/2026-09-01'`, gemessen für `turtle_soup_stocks` mit den
Tabellen aus `_vt.json`). ⇒ Weg (B) hätte eine Änderung an `auswertung.py`
verlangt — **Sperrlistenpunkt 5** (Abschnitt 10). *Damit steht Fables
Entscheidung nicht nur auf einem Grund, sondern auf einer Messung.* ⚠️ Fables
Begründung nennt diese Messung nicht; sie ist nicht sein Grund, sondern steht
daneben. Nicht gemessen ist, was in Registertext, Abbild und Berichten sonst
an Faltennamen hängt (TB-88, Antwort 1).

**Tatsachennotiz zu Fables Unsicherheit (TB-88, M1 (e), Messstand
`8851f67`):** Die einzige Prüfung in `test_vorregistrierung.py`, die den
Bezeichner der Bestätigungsperiode vergleicht, ist `A3`
(`bp["falte"] not in selektionsfalten`, in `teil_a`); sie bleibt mit jeder
Spanne wahr. Die Fehlerklasse, die Fable befürchtet, ist dort an der
Bestätigungsfalte **nicht** gemessen — an den Selektionsfalten ist sie schon
eingetreten (`G6`, 38.7 (d)).

**Marken am alten Ort:** bei **35.1**, unter der bestehenden Marke aus 36.1 (4)
und 36.3 — eine für 38.1, eine für 38.7 (c).

### 38.2 ⭐ Registertext, Ersteintrag — Fundstellen: Datei und Bezeichner, Zeilennummern nur mit Commit

**Fable, 22h Abschnitt 4, zeichengleich — der Anlass:**

> Tatsachennotiz zu 35.1: „Z. 336 → 338, Z. 368 → 460 nach TB-86 (Commit …)". 35.1 selbst nicht neu fassen — aber eine Regel für alle künftigen Registertexte, weil das sonst jede Woche wiederkommt:

**Der Registertext, zeichengleich:**

> **Registertext, Ersteintrag — Fundstellen:** Ein Registertext nennt Fundstellen im Code als **Datei und Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem Commit, an dem sie gemessen wurden. Eine Zeilennummer ohne Commit ist keine Fundstelle.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* append-only — ein Registertext, der altert, sobald jemand eine Datei anfasst, erzeugt Berichtigungen ohne Sachgrund. Kein Ergebnis.

**Belegt durch 38.7 (a):** Die Fundstellen in 35.1 (Z. 336 und Z. 368) waren
noch am Tag des Eintrags um zwei bzw. zweiundneunzig Zeilen gewandert —
durch einen Commit, der den Registertext nicht berührte (`4daa254`). Schon 30.3 hatte
festgehalten: *„Eine Zeilenangabe im Register trägt ab hier ihren
Commit-Stand mit."* 38.2 macht aus dieser Beobachtung eine Regel.

⭐ **Wo die Regel steht, und warum dort:** als Marke **im Kopf von
Abschnitt 0** dieses Registers — nicht bei den Prüfprinzipien
(`docs/projektfuehrung/`). Drei Gründe: (1) Sie ist **Registertext** und
bindet jeden künftigen Registertext; ein Registertext gehört ins Register,
das append-only ist und mit seinem Hash in `herkunft.py::register()`
eingeht — die Prüfprinzipien sind ein Arbeitsdokument des steuernden Chats,
nicht registriert und nicht append-only. (2) Wer einen Registertext schreibt,
schreibt ihn in dieser Datei; der Kopf von Abschnitt 0 ist die Stelle, an der
jeder Leser und jeder Schreiber vorbeikommt, bevor er einen Abschnitt öffnet.
(3) Die Prüfprinzipien regeln, wie geprüft wird; diese Regel regelt, wie
geschrieben wird — geprüft wird sie nach den Prüfprinzipien wie jeder andere
Registertext. *Eine Kopie bei den Prüfprinzipien wäre eine zweite Fassung
derselben Regel an einem zweiten Ort — genau das, was 21j und 37.5 für Werte
ausschliessen.*

**Marken am alten Ort:** im **Kopf von Abschnitt 0** (die Regel) und bei
**35.1** (die Tatsachennotiz 38.7 (a), an der sie belegt ist).

> ⭐ **38.2 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (e), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 38.3 ⭐⭐ Tatsachennotiz zu 21.9 und 10.1 — der Vollzug von Punkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3

**Fable, 22h Abschnitt 5, zeichengleich — welcher Satz gilt, und warum 10.1
hier nicht greift:**

> **Welcher Satz gilt:** 37.3. Die Sperrliste bindet ab dem signierten Tag; 10.1 regelt, was ein Bug-Fix **nach** Beginn des Laufs ist („der Lauf beginnt von vorn") — das Protokoll `herkunft_protokoll.jsonl` ist der Ort, an dem **Läufe** und ihre Amendments stehen, und vor dem ersten Lauf gibt es nichts, was dort stünde. 21.9 nennt den Vollzug „Amendment", weil der Begriff am 19.09. noch für beides stand; 23.6 hat ihn danach der Sperrliste des Codes zugeordnet, und 37.3 hat den Zeitpunkt geklärt. Die **Reihenfolge**-Entscheidung aus 21.9 (einmal, nach TB-31, alle neun Bots) gilt weiter und ist erfüllt — `_vt.json` trägt neunmal `endgueltig` (23.5).

**Die Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz zu 21.9 und 10.1:** Der Vollzug von Sperrlistenpunkt 4 vor dem Tag ist eine beauftragte Änderung nach 37.3 — Registertext, Tatsachennotiz mit altem und neuem Hash, neues Abbild. Kein Amendment nach 10.1, kein Protokolleintrag; das Protokoll entsteht mit dem Erzeuger und beginnt mit dem Stand des Tags.

⭐ **Was sich damit für 21.9 ändert:** Das Wort „Amendment" in der
Betreiberentscheidung 21.9 bleibt zeichengleich stehen; es bezeichnet nach
diesem Eintrag **keinen** Vorgang nach 10.1. Die **Reihenfolge**-Entscheidung
aus 21.9 gilt weiter und ist nach Fable erfüllt. **Tatsachennotiz (TB-88, M5,
Messstand `8851f67`):** `_vt.json` trägt für alle neun Bots `status:
endgueltig`; `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`
existiert nicht (`test -f`) — es gibt vor dem ersten Lauf kein Protokoll, in
das ein Amendment einzutragen wäre, wie Fables Grund voraussetzt.

**Marken am alten Ort:** bei **21.9**, unter der Betreiberentscheidung, und
bei **10.1**, unter dem Absatz zum append-only-Protokoll.

### 38.4 ⭐ Sperrlistenpunkt 4 — Form (ii): Form steht fest, Vollzug steht aus

**Fable, 22h Abschnitt 5, zeichengleich — die Form und seine Ablehnung von (i)
und (iii):**

> **Form: (ii).** Punkt 4 nennt beide Dateien; `benchmark_drawdowns.json` bleibt gesperrt und unverändert als registrierter historischer Stand mit Tatsachennotiz — wörtlich die Bauart von Punkt 2 (30.3) — und `benchmark_drawdowns_vt.json` ist die Tabelle, die der Lauf liest. *(i)* entfernt etwas aus der Liste; die Sperrliste beweist, dass nichts bewegt wurde, und das kann sie nur für Dateien, die auf ihr stehen. *(iii)* setzt eine ERSETZT-Marke an einen Punkt, dessen Datei weiter geprüft werden soll — die Marke sagt dann das Falsche. Kein Ergebnis: keine Zahl der Tabelle ist berührt.

**Sein Fertigkriterium für den Vollzug, zeichengleich:**

> Vollzug fertig, wenn (Plan-Punkt 8 erweitert): Registertext eingetragen, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), `test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —, neues Abbild, Sonde gegen das Abbild 0 für die Pfade.

> ⚠️⚠️ **ERSETZT (39.1, Fable 23f, TB-94, 23.09.2026) — das Fertigkriterium im
> Zitat oben:** Fable hat es in **23a** zurückgenommen und in **23f** als
> Berichtigung zu 38.4 adressiert. Es gilt der Ersatztext in **39.1**: Punkt 8
> ist fertig, wenn Registertext (Form (ii)), Tatsachennotiz mit altem und
> neuem Hash, die drei Leser über eine Konstante, der Absturz weg und
> `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**,
> Modus-Nachweis bytegleich, neues Abbild, Sonde 0 für die Pfade. **Der
> Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8**; „null
> rote Prüfungen" bleibt Tag-Vorbedingung (21.9, 23a). Das Zitat oben bleibt
> zeichengleich. TB-92 hat sich an dieses Zitat gehalten und abgebrochen —
> richtig (39.1).

⛔ **Festgelegt ist die Form, nicht vollzogen.** Punkt 4 in Abschnitt 10 bleibt
zeichengleich; `benchmark_drawdowns.json` (`a163c498…`) und
`benchmark_drawdowns_vt.json` (`4549395f…`) sind vor und nach diesem Eintrag
gleich (38.8). Der Vollzug ist **Plan-Punkt 8** und hängt an **zwei offenen
Fragen** an Fable (`FABLE_ANFRAGE_2026-09-22i_slippage_ja_und_gruen_nein.md`):
(1) ob „`test_vorregistrierung.py` grün" Fertigkriterium bleibt (Abschnitt 3
der Anfrage, hier 38.7 (d)); (2) welche Tabelle Punkt 4 für `t3_supertrend`
vollzieht — `_vt.json` trägt dort eine Falte `2018`, die der Plan seit TB-72
nicht mehr hat, und `dd_toleranz` ist in `_vt.json` und
`benchmark_drawdowns_tb72.json` verschieden (TB-88, M5; Werte nach 27.1 nicht
wiedergegeben) (Abschnitt 4 der Anfrage). **Beide sind hier nicht
beantwortet.**

**Tatsachennotiz (TB-88, M5, Messstand `8851f67`) — was der Vollzug berührt,
lesend:** `test_vorregistrierung.py` (Funktion `_tabellen`),
`auswertung.py` (`main`) und `registerbericht.py` lesen heute
`ergebnisse/benchmark_drawdowns.json`; `registerbericht.py` liest dort den
Schlüssel `symbole_point_in_time`, den `_vt.json` nicht trägt (23.5:
`symbole_handelbar_in_falte`). `auswertung.py` steht als Punkt 3 und 5 auf der
Sperrliste.

**Marke am alten Ort:** bei **Abschnitt 10, Punkt 4** — ⚠️ ausdrücklich
*„Form steht fest, Vollzug steht aus"*.

> ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026):** Form (ii) ist vollzogen — Punkt
> 4 nennt `ergebnisse/benchmark_drawdowns.json` (`a163c498…`, historischer
> Stand, unverändert) **und** die Tabelle, die der Lauf liest: ⚠️ **nicht**
> `_vt.json`, wie Fables Formtext oben sagt, sondern die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`,
> 23a/23b, TB-91). Beide offenen Fragen dieses Abschnitts sind beantwortet:
> „grün" (39.1) und die Tabelle für `t3_supertrend` (39.2). Die Tatsachennotiz
> TB-88 oben (die drei Leser lesen die alte Datei, alter Schlüssel) ist durch
> TB-92 (`0292e92`) überholt: sie lesen die Neurechnung über
> `auswertung.BENCHMARK_TABELLE`, `registerbericht.py` liest
> `symbole_handelbar_in_falte` (39.2). Der Text oben bleibt zeichengleich.

### 38.5 ⭐⭐ Kosten — kein Laufmodul trägt eine eigene Kopie: neun Importe, nicht neun überwachte Kopien

**Fable, 22h Abschnitt 2, zeichengleich — die Entscheidung:**

> **Entscheidung (Begründung nennt kein Ergebnis):** Es bleibt bei 37 (2) — **kein Laufmodul trägt eine eigene Kopie.** Die neun `backtest_*.py` ersetzen ihre Zuweisung durch den Import aus dem neuen Modul. Der Papierpfad (`forward_test.py`) behält seine Kopien und wird von der Sonde auf Gleichheit geprüft — wie in 22d (2) gesagt, und aus dem dort genannten Grund: Er ist Live-Code, seine Änderung braucht eine eigene Freigabe, und er ist nicht Teil des Laufs.

**Seine Begründung, zeichengleich** (darin der Kernsatz *„Ein Import ist keine
Prüfung, sondern eine **Struktur**"*):

> *Warum beseitigen und nicht überwachen:* Eine Sonde, die neun Kopien auf Gleichheit prüft, muss die Konstante **im Quelltext finden** — und wer den Finder schreibt, entscheidet, was gefunden wird (eine lokale Variable gleichen Namens, eine Zuweisung in einem Kommentar, eine Berechnung statt eines Literals). Ein Import ist keine Prüfung, sondern eine **Struktur**: Der Wert kann im Laufmodul nicht anders sein als im Modul, weil er dort nicht steht. Dieselbe Regel wie bei der Schreibsperre — die Sicherung ist stärker, wenn sie nicht vergleichen muss. Kein Ergebnis: alle achtzehn tragen heute dieselbe Zahl, sie ändert sich nicht.

**Zu Punkt 7, zeichengleich — seine Rücknahme des 22d-Kandidaten:**

> *Zu Punkt 7:* `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` stehen in `registerdaten.py` — das **ist** ein Modul, ein Ort, und es steht als Punkt 1 auf der Sperrliste. Hier ist nichts zu verschieben; Punkt 7 bekommt den Ort nachgetragen (`registerdaten.py`, die beiden Konstanten), und die Sonde prüft Datei plus Wert. Mein „Kandidat" aus 22d war für Punkt 7 gar keiner — der Ort existiert schon.

**Zu `messgroessen.py` / `GEBUEHR_PCT`, zeichengleich:**

> *Zu `messgroessen.py` / `GEBUEHR_PCT`:* bleibt, wie es ist (eingefroren), mit Tatsachennotiz: eine Kopie unter anderem Namen, kein Laufort, von der Sonde auf Gleichheit geprüft wie der Papierpfad.

⭐ **Was damit gilt, zusammengefasst — die Zitate oben sind massgeblich:**

| Ort | Stellung nach 38.5 |
|---|---|
| neun `strategies/*/backtest_*.py` (Laufpfad) | ersetzen ihre Zuweisung von `TRADING_FEE_PCT` / `SLIPPAGE_PCT` durch einen **Import** aus einem neuen Modul — **kein Laufmodul trägt eine eigene Kopie** (37.5 (2)) |
| neun `strategies/*/forward_test.py` (Papierpfad) | behalten ihre Kopien; **überwachte** Kopie, die Sonde prüft auf Gleichheit |
| `research/vorregistrierung/messgroessen.py`, `GEBUEHR_PCT` | bleibt eingefroren; **überwachte** Kopie unter anderem Namen, kein Laufort |
| Punkt 7: `registerdaten.py`, `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` | **nichts zu verschieben** — der Ort existiert; Punkt 7 bekommt ihn nachgetragen, die Sonde prüft Datei plus Wert |

⛔ **Nicht Gegenstand dieses Eintrags:** das neue Modul, die neun Importe, der
Nachtrag des Orts bei Punkt 7 und 9 und die Gleichheitsprüfung der Sonde —
Handwerk, TB-90 (Freigabe des Betreibers liegt nach dem Auftrag vor,
22.09.2026). Die Werte `0,1` / `0,05` / `0,90` ändern sich nicht.

**Marken am alten Ort:** bei **Abschnitt 10, Punkt 9** und **Punkt 7**, je
unter der Marke aus 37.5, die zeichengleich bleibt; bei **37.5**, direkt unter
dem Registertext.

### 38.6 ⚠️ Fables zwei Berichtigungen an sich selbst — Z. 51, und acht statt fünf Stellen

**Fable, 22h Abschnitt 1, zeichengleich:**

> **(a)** „`auswertung.py` Z. 41" lies **Z. 51**. Die Zahl kam aus Nachtrag 2; ich habe sie übernommen statt sie als Voraussetzung zu nennen — mein Verstoss gegen meine eigene Regel aus 21m. Berichtigung als Tatsachennotiz zu 37.4 genügt.

> **(b)** „an fünf Stellen" — ich habe fünf angekündigt und sechs aufgezählt; das war kein Messfehler, sondern ein Zählfehler beim Schreiben, und er ist meiner. Gemessen acht. **Ersatzsatz für 37.4:**

**Der Ersatzsatz für 37.4, zeichengleich:**

> … und weicht von dieser an **acht** Stellen ab — **vier fehlen** (`config/top25_symbols.txt`, `config/sp500_top150.txt`, `research/vorregistrierung/herkunft.py`, `shared/zuteilung.py`; dazu der bestimmte Pfad `benchmark_drawdowns_vt.json`, der kein Punkt ist), **vier stehen zusätzlich** (`kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`, `ergebnisse/messgroessen.json`).

> Der alte Satz bleibt mit Marke; eure Tatsachennotiz daneben ist der Beleg.

⭐ **Der alte Satz in 37.4 bleibt stehen** — Fables Tatsachennotiz aus 22d,
zeichengleich, mit „Z. 41" und „an fünf Stellen". Er bekommt die
ERSETZT-Marke; die Tatsachennotiz TB-87 (M3) in 37.4, die beides gemessen
hatte, ist der Beleg. Fables Ersatzsatz nennt dieselben acht Abweichungen,
die 37.4 gemessen aufgezählt hat (vier fehlend, dazu der bestimmte Pfad; vier
zusätzlich) — gegen die Liste in 37.4 verglichen: dieselben neun Dateien;
einziger Schreibunterschied, dass 37.4 den bestimmten Pfad als
`ergebnisse/benchmark_drawdowns_vt.json` führt, Fable ohne Ordner.

**Marke am alten Ort:** bei **37.4**, direkt unter Fables Tatsachennotiz.

### 38.7 ⭐ Tatsachennotizen aus TB-88

Quelle: `docs/belege/TB-88/ERGEBNIS_TB-88.md`, Messstand `8851f67`, soweit
nicht anders gesagt. Zwischen `8851f67` und dem Eingang dieses Auftrags hat
sich unter `research/` keine Datei geändert (`git diff --quiet 8851f67 HEAD --
research/`, gemessen in TB-89).

**(a) Die Fundstellen aus 35.1, heute.** Die Erzeugung des Bezeichners
(`"bestaetigungsperiode": falten[-1]["name"] …`, in
`research/vorregistrierung/faltenplan.py`, Funktion `_plan`) steht am Stand
`8851f67` auf **Z. 338**, die Konsolenausgabe (`best =
p["bestaetigungsperiode"]`, Funktion `main`) auf **Z. 460**. 35.1 nennt Z. 336
und Z. 368 (gemessen in TB-83, HEAD `9dac8d4`; so gültig seit `76c20ec`,
TB-80). Verschoben hat sie
**`4daa254`** (TB-86 Schritt 2 und 3: `--ziel`, Voreinstellung,
Einmal-Schreibsperre) — nicht `ee4e65c`, das ist der Abschlussbeleg von TB-86.
⭐ *Damit ist 38.2 belegt.* Die Namensbildung der Bestätigungsfalte — die
Stelle, die Fable in 38.1 meint — ist die Zuweisung der Rolle `bestaetigung`
in derselben Funktion `_plan` (Z. 307 am Stand `8851f67`).

**(b) ⭐⭐ Slippage — Fables Messbitte aus 22h Abschnitt 2, zeichengleich:**

> **Eine Messbitte, nur das Ob, bevor der Auftrag geschrieben wird:** Eure Tabelle nennt in den neun `backtest_*.py` nur `TRADING_FEE_PCT`. Sperrlistenpunkt 9 registriert **auch** `SLIPPAGE_PCT = 0,05 je Order` und die Summe 0,30 %. **Wenden die neun `backtest_*.py` Slippage an — und unter welchem Namen?** Wenn nein, rechnet der Laufpfad mit anderen Kosten, als das Register registriert; das wäre ein eigener Befund, grösser als die Frage der Kopien, und er müsste vor dem Tag ins Register — als Berichtigung des Codes an den Registertext, nicht umgekehrt.

**Gemessen: ja.** **9 von 9** `strategies/*/backtest_*.py` tragen
`SLIPPAGE_PCT = 0.05` (derselbe Name, derselbe Wert) neben
`TRADING_FEE_PCT = 0.1` und rechnen `2 * (TRADING_FEE_PCT + SLIPPAGE_PCT)` —
**0,30 %** je Rundlauf, genau die Summe aus Punkt 9, Ein- und Ausstieg. ⚠️
**Formabweichung ohne Wertunterschied:** `t3_supertrend/backtest_trend.py`
zieht die Kosten als `pnl_pct -= 2 * (…)` ab statt über `total_cost_pct = 2 *
(…)`. ⇒ **Der Befund, den Fable befürchtet hat, tritt nicht ein**; die
Voraussetzung aus 22h Abschnitt 6 ist erfüllt. ⚠️ *Herkunft:* Diese Messung
steht **nicht** in `ERGEBNIS_TB-88.md`, sondern in der Anfrage 22i des
steuernden Chats (Abschnitt 1, HEAD `ec54618`); in TB-89 lesend nachgemessen
am Stand `da251da` (`docs/belege/TB-89/m_slippage_backtest.txt`), gleich.

**(c) ⚠️⚠️ Weg (B) hätte einen Sperrlistenpunkt berührt.** Steht in 38.1;
Marke bei 35.1.

**(d) ⚠️⚠️ „rot" heisst heute: der Test stürzt ab — und nach dem Vollzug
bleibt er 163/2.** `research/vorregistrierung/test_vorregistrierung.py` läuft
am Stand `8851f67` **keine einzige Prüfung**: Mit aktiviertem `trading-env`
endet er in `teil_a` mit `KeyError: '2017'` in `auswertung.py`, Funktion
`zulaessigkeit` — **0 bestanden, 0 gescheitert**, die Schlusszeile wird nie
gedruckt, rc `1`. Ursache: der Test liest `ergebnisse/benchmark_drawdowns.json`
(TB-30a-Stand, für `turtle_soup_stocks` Falten `2019`–`2026`), der Plan beginnt
bei `2017`. Ohne venv scheitert er schon früher am fehlenden Paket `binance`.
Die **Simulation des Vollzugs** (Kopie des Ordners, nur dort die Tabelle
getauscht; `m4_simulation_punkt8.sh`) ergibt **163 bestanden, 2 gescheitert**:

| Prüfung | hängt an |
|---|---|
| `G6` (*„2020 und 2022 sind Testfalten, keine Trainingsjahre"*) | **nicht an Punkt 4.** Sucht die Faltennamen `2020` und `2022`; `elliott_wave` hat seit TB-61 Zweijahresfalten `JJJJ-JJJJ` — eine Annahme aus TB-30a |
| `H3` (*„ohne die gesetzte Null aendert sich die Statistik"*) | **nicht an Punkt 4.** Die Probe setzt vier Falten ohne Trade und rechnet laut eigenem Kommentar mit sieben Selektionsfalten; seit der ersten Falte `2017` sind es neun, der Median kippt nicht mehr |

⇒ Beide hängen am **Faltenplan** (TB-56/TB-61/TB-72), nicht an der
Benchmark-Tabelle. ⚠️ **Damit ist Fables Fertigkriterium
„`test_vorregistrierung.py` grün" (22h Abschnitt 5, zitiert in 38.4, und
Abschnitt 3, zitiert in 38.1) heute nicht erreichbar.**

⚠️⚠️ **OFFENE FRAGE — eingetragen, nicht entschieden:** Bleibt „grün"
Fertigkriterium von Plan-Punkt 8? Die Anfrage 22i (Abschnitt 3) legt Fable
drei Lesarten vor — (1) fertig, wenn der Absturz weg ist, `G6`/`H3` werden ein
eigener Punkt; (2) Punkt 8 umfasst `G6`/`H3`; (3) „grün" bleibt, beide als
bekannt rot mit Grund, was A4 und 21.9 widerspräche. **Die Frage liegt bei
Fable; dieses Register beantwortet sie nicht**, auch nicht durch die
Reihenfolge der Lesarten oder die Neigung des steuernden Chats, die dort
steht. Bis zu seiner Antwort gilt 21.9 unverändert: der Test ist **„offen
durch eigene Änderung — blockierend für den Tag"**; neu ist nur die gemessene
Tatsache, dass „rot" dort einen Absturz bezeichnet. *Ein Registerabschnitt
darf eine offene Frage tragen — 21.6 hat es vorgemacht.*

> ⭐⭐ **BEANTWORTET (39.1, Fable 23a/23f, TB-94, 23.09.2026):** Lesart **(1)**
> — Plan-Punkt 8 ist fertig, wenn der Absturz weg ist und der Test bis zur
> Schlusszeile läuft; `G6`/`H3` sind der eigene Planpunkt „Testannahmen folgen
> dem Register" (23a), Tag-Vorbedingung, nicht Punkt 8. Das Fertigkriterium in
> 38.4 ist durch den Ersatztext in 39.1 berichtigt. Gemessen am echten Stand
> (TB-92, `0292e92`): Absturz weg, Schlusszeile erreicht, **163/2** (`G6`,
> `H3`) — dieselben zwei wie in der Simulation oben. Die Frage oben bleibt
> zeichengleich stehen.

**Marken am alten Ort:** (a) und (c) bei **35.1**; (b) bei **Abschnitt 10,
Punkt 9**; (d) bei **21.9**, unter der Tabelle der Folgen (wo der rote Test
geführt wird), und bei **23.7**, unter dem Nachtrag TB-71.

### 38.8 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `faltenplan.py` (Namensbildung, 38.1) noch die neun `backtest_*.py` (Importe, 38.5); **kein neues Modul**, kein Import gesetzt | TB-90 |
| ⛔ | **Kein Vollzug von Punkt 4** — nur die Form (38.4); `benchmark_drawdowns.json` bleibt byteweise dieselbe Datei | Plan-Punkt 8, nach Fables Antwort auf 22i |
| ⛔ | **Kein neues Abbild**, keine Sonde angepasst, `python3 faltenplan.py` nicht aufgerufen; `registerbericht.py` und `test_vorregistrierung.py` nicht angefasst | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — der alte Satz in 37.4, die Zeilennummern in 35.1 und das Wort „Amendment" in 21.9 bleiben zeichengleich; ERSETZT- und Hinweis-Marken, nichts entfernt | — |
| ⛔ | **Keine offene Frage beantwortet** — weder „grün" als Fertigkriterium (38.7 (d)) noch die Tabelle für `t3_supertrend` (38.4) | Fable |
| ⭐ | **Keine Zahl bewegt:** die drei Sperrlisten-Hashes `a163c498…` (`benchmark_drawdowns.json`), `0e54ac5c…` (`faltenplan.json`), `4549395f…` (`benchmark_drawdowns_vt.json`) vor und nach dem Eintrag gleich; die Sperrlisten-Sonde lesend vor und nach dem Eintrag gegen `sperrliste_abbild_2026-09-22.json`: Prüfung (ii) `0`, Listentext wie bei Erzeugung, unverändert `1` nur an Punkt 2 (37.3) | — |
| ⚠️ | **Offen:** 22i Abschnitt 3 (grün), Abschnitt 4 (`t3_supertrend`), und ob `G6`/`H3` als eigener Punkt in den Plan vor dem Tag gehören · das neue Modul und die neun Importe (38.5) · die Namensbildung (38.1) · der Vollzug von Punkt 4 (38.4) · das neue Abbild danach — ein Abbild für alle drei Dateigruppen (22h Abschnitt 6) | Fable / Betreiber / TB-90 |

*Dieser Abschnitt ist rein additiv: Er trägt eine Berichtigung, einen
Ersteintrag, eine Tatsachennotiz, eine Formfestlegung, eine Entscheidung und
zwei Selbstberichtigungen des Verfahrensprüfers zeichengleich ein; setzt
vierzehn Marken am alten Ort; hält die Messungen aus TB-88 samt einer offenen
Frage fest — und entfernt nichts. Gebaut wird nichts.*

## 39. Der Vollzug von Sperrlistenpunkt 4 im Register — Berichtigung des Fertigkriteriums in 38.4, Form (ii) vollzogen, Determinismus- und Modus-Nachweis, fünf Hash-Übergänge nach 37.3, zwei Eingaben ohne registrierten Eingabestand und das neue Abbild (Fable 23a–23f, TB-94, 23.09.2026)

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 38. Der
Vollzug von Plan-Punkt 8 ist **im Code** seit `0292e92` (TB-92) erbracht und
belegt; TB-92 hat danach **richtig abgebrochen**, weil 38.4 „grün" verlangte.
Dieser Abschnitt trägt den Vollzug **ins Register** nach: die Berichtigung des
Fertigkriteriums in 38.4 (39.1), den Vollzug der Form (ii) an Punkt 4 (39.2),
die Tatsachennotizen zu `_vt.json` und `_tb72.json` (39.3), den
Determinismusnachweis (39.4), die fünf Hash-Übergänge nach 37.3 (39.5), den
Modus-Nachweis (39.6), die Tatsachennotiz zu `herkunft.py::EINGEFROREN`
(39.7), die zwei Eingaben ohne registrierten Eingabestand (39.8), das neue
Abbild (39.9) und den Schlussteil (39.10). Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md`, `…23b_neurechnung_nach_a.md`,
`…23c_messgroessen_und_vollzug.md`, `…23d_dritte_leserin_und_eingabestand.md`,
`…23e_nachweislauf_im_modus.md`, `…23f_fertigkriterium_38_4.md` und
`…22g_sonde_vor_dem_tag.md` — **eingesetzt, nicht abgetippt** (Beleg
`docs/belege/TB-94/e2_zitate.txt`, je Zitat `diff` rc 0). Auftrag
`docs/auftraege/MAC_TB-94_register_39.md`; Belege `docs/belege/TB-94/`; Eingang
`fcc3265`, Schritt-0-Commit `12f6089`. Messungen der Vorgänger: TB-91
(`docs/ERGEBNIS_TB-91_benchmark_absichern_und_neurechnung.md`, Belege
`docs/belege/TB-91/`) und TB-92 (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Belege `docs/belege/TB-92/`), in TB-94 an den Belegen und an den Hashes
nachgemessen (`a1_hashes.txt`).
⛔ **Keine `.py` geändert, nichts gerechnet** — 39.10.

⭐ **Zum Zwischenstand zwischen `fcc3265` und diesem Eintrag** (Repo vollzogen,
Register nicht), Fable 23f Abschnitt 3, zeichengleich:

> **Zum Zwischenzustand über Nacht:** Er ist zulässig, weil er **benannt** ist — diese Anfrage und diese Antwort liegen beide in der Ablage, der Commit `fcc3265` ist der Stand, und der Registerauftrag ist der nächste Schritt. Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag. Nichts zurücknehmen.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (Abschnitt 10
Punkt 4; 38.4 zweimal; 21.9; 38.7 (d); 37.2; 37.3; 23.7; 33.2; 37.4 — zehn).
Die alten Sätze bleiben zeichengleich — **auch der Satz mit „grün" in 38.4**;
`git diff --numstat` auf dieses Register zeigt für TB-94 in der zweiten Spalte
`0`. ⭐ **Neu gegenüber 34–38:** Punkt 4 in Abschnitt 10 bekommt eine
**Pfadzeile** — drei eingerückte Folgezeilen **nach** der Zeile
`   Interpolationsregel**`, die vier Zeilen davor zeichengleich. Das ist der
Vollzug selbst (39.2), keine Marke; er ist additiv, weil die Sperrliste nach
Form (ii) nichts streicht. Fundstellen stehen nach 38.2 als Datei und
Bezeichner; Zeilennummern nur in Tatsachennotizen, mit Commit.

### 39.1 ⭐⭐ Berichtigung zu 38.4 — das Fertigkriterium von Plan-Punkt 8

⚠️ **Der Anlass:** 38.4 trägt als Fertigkriterium Fables Satz aus **22h**
(„`test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —"). Fable
hat dieses Kriterium in **23a** zurückgenommen und ersetzt; **die Rücknahme ist
nie als Ersatztext an 38.4 eingetragen worden.** TB-92 hat sich an das
Register gehalten: Der Test lief bis zur Schlusszeile, war aber **163/2**
(`G6`, `H3`) — nicht grün —, und TB-92 hat abgebrochen, statt zwischen
Register und Antwortdatei zu wählen (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Abschnitt 3). ⭐ **Das war das richtige Verhalten und wird hier ausdrücklich so
festgehalten.**

**Fable, 23f Abschnitt 2, zeichengleich — der Befund an sich selbst:**

> Der Widerspruch ist meiner, und er hat eine einfache Geschichte: 38.4 trägt meinen Text aus **22h** („grün — die roten Prüfungen misst TB-88"). **23a** hat dieses Kriterium ausdrücklich zurückgenommen — „Mein Satz ‚fertig, wenn `test_vorregistrierung.py` grün' hat zwei Dinge vermischt: eine Tag-Vorbedingung und ein Fertigkriterium für einen Punkt" — und ersetzt: fertig, wenn der Absturz weg ist und der Test bis zur Schlusszeile läuft; G6/H3 eigener Punkt. 23d hat das wiederholt. **Was fehlt, ist die Berichtigung von 38.4 im Register** — 23a ist als Antwort abgelegt, aber nie als Ersatztext an 38.4 eingetragen worden. Die Mac-Sitzung hat den Registertext gelesen, nicht meine Antwortdatei, und das ist richtig so: **Für eine ausführende Sitzung gilt das Register, nicht Fable.** Der Fehler liegt darin, dass 23a eine Berichtigung enthielt, ohne sie als solche zu adressieren; ich habe „Fertigkriterium" geschrieben und nicht „Berichtigung zu 38.4".

⭐ **Die Rangfolge, die daraus folgt, zeichengleich:** *„Für eine ausführende Sitzung gilt das Register, nicht Fable."*

**Der Ersatztext, zeichengleich:**

> **Berichtigung zu 38.4, Ersatztext (aus 23a, zeichengleich in der Sache):** Punkt 8 ist fertig, wenn: Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, alle drei Leser (`auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`) lesen die vollzogene Tabelle über eine Konstante, der Absturz ist weg und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, Modus-Nachweis bytegleich (23e), neues Abbild, Sonde 0 für die Pfade. **Der Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8.** „Null rote Prüfungen" ist Tag-Vorbedingung (21.9, A4) und wird durch den eigenen Punkt „Testannahmen folgen dem Register" erreicht. Der Einschub „die roten Prüfungen misst TB-88" in der alten Fassung war der Hinweis in diese Richtung; das Wort „grün" davor war der Fehler.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23a, Abschnitt 2 — ein Fertigkriterium hängt an dem, was der Punkt ändert; sonst haftet ein Punkt für fremde Fehler und wird nie fertig. Kein Ergebnis.

**Seine Regel an sich selbst, zeichengleich:**

> **Und eine Regel für mich, damit das nicht wieder passiert:** Wenn eine Antwort von mir einen Registertext ändert, den eine frühere Antwort gesetzt hat, **nennt sie ihn als Berichtigung mit Abschnittsnummer** — nicht als neue Entscheidung. Eure Regel „nicht übernehmen, nachmessen" gilt für meine Texte gegen das Register genauso wie für eure gegen den Code.

**Die Entscheidung in 23a, auf die der Ersatztext zurückgeht, zeichengleich**
(Abschnitt 2 — die Entscheidung und der neue Planpunkt):

> **Punkt 8 ist fertig, wenn:** Registertext eingetragen (Form (ii)), Tatsachennotiz mit altem und neuem Hash, `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5), **der Absturz (`KeyError` an der Faltenzuordnung) ist weg** und `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**, neues Abbild, Sonde 0 für die Pfade. Der Ausgang der einzelnen Prüfungen ist nicht Fertigkriterium von Punkt 8.
>
> **Neuer Planpunkt vor dem Tag — „Testannahmen folgen dem Register":** `test_vorregistrierung.py` ist der Nachweis von Abschnitt 12 („150 Prüfungen, acht Mutationsproben"). Jede Prüfung, deren Annahme dem Register hinterherhinkt, wird an das Register angepasst — nie umgekehrt, und nie gelöscht. Für G6: Faltennamen kommen aus dem Faltenplan (Abbild 33.3), nicht als Literale `"2020"`, `"2022"`. Für H3: Eine Mutationsprobe, die nicht mehr beisst, wird so gestellt, dass sie **mit der registrierten Faltenzahl** beisst (und die Mutationsprobe selbst bleibt Pflicht — eine Probe, die immer besteht, ist keine). **Tag-Vorbedingung nach 21.9 und A4: null rote Prüfungen, null „bekannt rot".** (3) ist damit ausgeschlossen, wie ihr sagt.

**Der Grund in 23a, zeichengleich:**

> Mein Satz „fertig, wenn `test_vorregistrierung.py` grün" hat zwei Dinge vermischt: eine **Tag-Vorbedingung** (21.9: der Test blockiert den Tag, solange er rot ist) und ein **Fertigkriterium für einen Punkt**. Das Fertigkriterium eines Punktes muss an dem hängen, was der Punkt ändert — sonst wird ein Punkt nie fertig, weil er für fremde Fehler haftet.

⇒ **Was ab hier gilt:**

| | |
|---|---|
| Fertigkriterium von Plan-Punkt 8 | der **Ersatztext oben** (23f/23a). Der Satz in 38.4 („`test_vorregistrierung.py` grün — die roten Prüfungen misst TB-88 —") bleibt **zeichengleich** stehen und trägt eine ERSETZT-Marke |
| Die offene Frage in 38.7 (d) („bleibt ‚grün' Fertigkriterium?") | **beantwortet** — Lesart (1) der Anfrage 22i: fertig, wenn der Absturz weg ist; `G6`/`H3` sind ein eigener Punkt |
| 21.9, Tabelle der Folgen, erste Zeile („bleibt **rot** … offen durch eigene Änderung — blockierend für den Tag") | **gilt unverändert für den Tag.** „Null rote Prüfungen, null ‚bekannt rot'" ist Tag-Vorbedingung (23a); sie wird mit dem Planpunkt „Testannahmen folgen dem Register" erreicht (`G6`, `H3`; TB-95), nicht mit Punkt 8 |

**Tatsachennotiz — was TB-92 gemessen hat (`docs/belege/TB-92/b1_ausgabe.txt`,
HEAD `0292e92`):** `trading-env/bin/python3
research/vorregistrierung/test_vorregistrierung.py` — Teil A bis H
durchlaufen, **Schlusszeile erreicht**, der `KeyError: '2017'` ist weg; **163
bestanden, 2 gescheitert** (`G6`, `H3`), rc `1`, 501 s. `G6` und `H3` werden in
diesem Abschnitt **weder gemessen noch erklärt noch angepasst** (TB-95).

**Marken am alten Ort:** bei **38.4**, direkt unter dem Zitat mit „grün"; bei
**21.9**, unter der Tabelle der Folgen; bei **38.7 (d)**, unter der offenen
Frage.

### 39.2 ⭐⭐ Vollzug von Sperrlistenpunkt 4 in Form (ii)

⭐⭐ **Der Punkttext von Abschnitt 10, Punkt 4, ist geändert — additiv.** Nach
der Zeile `   Interpolationsregel**` stehen drei neue Folgezeilen:

```
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)
```

Die vier Zeilen davor und der Kasten aus 38.4 darunter sind zeichengleich; der
Kasten trägt jetzt die Vollzugsmarke. Punkt 4 nennt damit:

| Datei | Rolle | sha256 |
|---|---|---|
| `benchmark.py` | Erzeuger (Punkte 4 und 6), unverändert seit TB-91 | `d6bdd558…` |
| `ergebnisse/benchmark_drawdowns.json` | **registrierter historischer Stand**, gesperrt und byteweise unverändert — wie Punkt 2 (30.3) | `a163c498…` |
| `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` | **die Tabelle, die der Lauf liest** | `64fb2912…` |

(Gemessen in TB-94 am Stand `12f6089`, `a1_hashes.txt`; volle Hashes dort und
in 39.5.)

**Die Bedingung, nach der diese Datei die Tabelle ist — Fable, 23a Abschnitt 3,
zeichengleich (Registertext zu Sperrlistenpunkt 4 / 23 / 33, die Wache und die
Folge für den Vollzug):**

> **Registertext zu Sperrlistenpunkt 4 / 23 / 33:** Die Benchmark-Tabelle, die der Lauf liest, ist auf dem registrierten Faltenplan (33.2) gerechnet: Für jeden Bot ist die Faltenmenge der Tabelle gleich der Menge seiner Selektionsfalten nach 33.2 (plus Bestätigungsperiode, sofern die Tabelle sie führt) — nicht mehr, nicht weniger —, und ihre Benchmark-Definition ist die aus 23 (tagesgenau). Eine Tabelle, die diese Bedingung für auch nur einen Bot nicht erfüllt, wird nicht vollzogen; sie bleibt liegen und erhält eine Tatsachennotiz, auf welchem Planstand sie gerechnet wurde.
>
> **Wache (in den Vollzug und in den Laufwrapper):** Faltenmenge der vollzogenen Tabelle je Bot gegen das Abbild des Faltenplans — Abweichung ist 1, fehlende Datei 2. Der `KeyError '2017'` von heute ist genau dieser Befund, nur als Absturz statt als Wache.
>
> **Folge für den Vollzug:** Es wird **eine** Tabelle für alle neun Bots vollzogen, keine Mischung. Welche Datei das ist, entscheidet die Bedingung, nicht der Name: Ist `benchmark_drawdowns_tb72.json` für alle neun Bots auf 33.2 gerechnet und tagesgenau nach 23, dann ist sie die Tabelle, und `_vt.json` erhält eine Tatsachennotiz als Zwischenstand (23, vor 25); die Gruppe „bestimmt" in 37.2 wechselt entsprechend. Erfüllt keine vorhandene Tabelle die Bedingung für alle neun, wird die Tabelle **einmal neu gerechnet** — mit `benchmark.py` (Punkt 4/6), auf dem Abbild des Faltenplans, mit Beleg und Hash, vor dem Tag.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23.7 („der Widerspruch zwischen berichtigtem Faltenplan und gesperrter Benchmark-Tabelle … wird mit demselben Amendment geschlossen") — geschlossen heisst: die Tabelle folgt dem Plan, nicht der Plan der Tabelle. Und 24.3 als Bauart: Die Regel steht hier, **bevor** ich weiss, welche Datei sie erfüllt; die Werte kenne ich nicht und brauche sie nicht. Kein Ergebnis.

**Und die Entscheidung, sie einmal neu zu rechnen — 23b Abschnitt 2,
zeichengleich:**

> **Ergänzung zu 23a, Abschnitt 3 (Registertext zu Sperrlistenpunkt 4):** Die Tabelle, die der Lauf liest, wird **nach** der Umsetzung von Weg (A) (Punkt 3, TB-90) **einmal** neu gerechnet — mit `benchmark.py` (Sperrlistenpunkt 4/6, unverändert), auf dem dann gültigen Plan, mit `--ziel` auf einen neuen Pfad nach der Schreibregel 36.1, mit Beleg und Hash. Ihre Bestätigungszeile trägt den Bezeichner nach 35 (`2026-01-01/2026-09-01`).

⇒ **Warum diese Datei und nicht `_vt.json`:** 23a hat die Bedingung gesetzt
(Faltenmenge je Bot gleich den Selektionsfalten nach 33.2, plus
Bestätigungsperiode; Benchmark tagesgenau nach 23; **keine Mischung** aus zwei
Tabellen), 23b hat entschieden, dass **einmal neu gerechnet** wird, und TB-91
hat sie gerechnet (`31008b6`, 39.4). ⭐ **Damit ist die zweite offene Frage aus
38.4 („welche Tabelle für `t3_supertrend`") beantwortet:** keine vorhandene —
die Neurechnung, für alle neun.

**Wie die drei Leser sie lesen — Fable, 23d Abschnitt 1, zeichengleich:**

> **Zu Sperrlistenpunkt 4, Vollzug, Schritt 1a:** `auswertung.py` liest die vollzogene Tabelle über **eine** Konstante am Modulanfang, deren Wert der registrierte Pfad der neuen Tabelle ist. **Kein Kommandozeilenschalter** — Abschnitt 12 sagt „`auswertung.py` hat keinen Schalter", und eine Option, die bestimmt, welche Tabelle gilt, wäre einer. Bedingungen: AST-Vergleich aller Funktionskörper unverändert; genau eine Zuweisung verändert (die Pfadkonstante); `test_vorregistrierung.py` und `beispieldaten.py` lesen dieselbe Konstante, damit Test und Lauf nicht auseinanderfallen können; Tatsachennotiz mit altem und neuem Hash von `auswertung.py`. Die Änderung geschieht in demselben Auftrag wie der Vollzug (TB-92), nicht danach.

**Tatsachennotiz — umgesetzt in TB-92, `0292e92`
(`docs/belege/TB-92/a1a_ast_vergleich.txt`, `a5_hashes_nachher.txt`):**
`research/vorregistrierung/auswertung.py` trägt **eine** Konstante
`BENCHMARK_TABELLE` (Pfad der Neurechnung), `main` öffnet sie; ⛔ **kein
Schalter** (Abschnitt 12). AST-Vergleich: 27 Funktionen und Klassen, **26
gleich**, verschieden nur `main` und dort nur im Argument von `open`; auf
Modulebene **genau eine neue Zuweisung** (`BENCHMARK_TABELLE`), keine entfernt.
`registerbericht.py` (Funktion `block`) und `test_vorregistrierung.py`
(Funktion `_tabellen`) lesen `aw.BENCHMARK_TABELLE`; `registerbericht.py` liest
dort den Schlüssel `symbole_handelbar_in_falte` (23.5) statt
`symbole_point_in_time` — der alte Schlüssel kam genau **einmal** vor.
⚠️ **`beispieldaten.py` liest keine Tabelle** (Hash `3e547014…` unverändert,
in TB-94 nachgemessen): Die vierte Leserin, die 23d („`test_vorregistrierung.py`
und `beispieldaten.py` lesen dieselbe Konstante") voraussetzt, gibt es nicht.
Repo-weit sind es **drei** Leser, wie TB-88 (38.4, Tatsachennotiz M5) gemessen
hat.

**Marken am alten Ort:** bei **Abschnitt 10, Punkt 4** (Vollzug); bei **38.4**,
am Ende (Form (ii) vollzogen).

### 39.3 Tatsachennotizen zu `_vt.json` und `_tb72.json` — und die Gruppe „bestimmt"

**Fable, 23b Abschnitt 2, zeichengleich:**

> `benchmark_drawdowns_vt.json` und `benchmark_drawdowns_tb72.json` bleiben unverändert liegen, erhalten je eine Tatsachennotiz (Planstand, auf dem sie gerechnet wurden; TB-66 bzw. TB-72) und kommen **nicht** auf die Sperrliste; die Gruppe „bestimmt" in 37.2 wechselt auf die neue Tabelle. Sperrlistenpunkt 4 nach Form (ii): `benchmark_drawdowns.json` als registrierter historischer Stand, die neue Tabelle als die, die der Lauf liest.

**Die Tatsachennotizen (in TB-94 nachgemessen, `a1_hashes.txt`):**

| Datei | gerechnet auf Planstand | Bestätigungszeile | sha256 | Sperrliste |
|---|---|---|---|---|
| `ergebnisse/benchmark_drawdowns_vt.json` | **TB-66** (tagesgenau nach 23, vor 25); `t3_supertrend` mit einer Falte `2018`, die der Plan seit TB-72 nicht mehr hat | alter Name (`2026` bzw. `2026-2027`) | `4549395f…` | ⛔ **nicht** |
| `ergebnisse/benchmark_drawdowns_tb72.json` | **TB-72** | alter Name (`2026` bzw. `2026-2027`) | `e4ba341d…` | ⛔ **nicht** |

Beide bleiben unverändert liegen. Die Neurechnung reproduziert `_tb72.json` in
allen Werten (39.4); `_vt.json` weicht von `_tb72.json` an **101** Blattwerten
ab (Selbsttest des Vergleichers, TB-91; Werte nach 27.1 nicht wiedergegeben).

⭐ **Folge für 37.2 (Gruppe „bestimmt"):** Die Gruppe nannte bisher
`ergebnisse/benchmark_drawdowns_vt.json`. Nach 23b **wechselt sie auf die neue
Tabelle** — und weil deren Pfad seit 39.2 in Punkt 4 steht, hat sie ihren
Punkt: **Die Gruppe „bestimmt" ist nach dem Registertext leer.** 37.2 verlangt
genau das für den Tag: *„Am Tag ist die zweite Gruppe leer."*

⚠️ **Tatsachennotiz — was die Sonde dazu meldet (TB-87 gemessen, in TB-94
nachgemessen):** Die Sonde führt die Gruppe nicht aus dem Abbild, sondern aus
einer **festen Konstante** in `shared/sperrlistensonde.py`
(`BESTIMMT_NICHT_EINGETRAGEN`, am Stand `12f6089` ein Eintrag:
`ergebnisse/benchmark_drawdowns_vt.json`, Begründungstext „Register
21.9/23.7 - fuer die Sperrliste bestimmt, Vollzug steht aus"); sie **nennt**
den Pfad, **prüft** ihn nicht (37.2, Tatsachennotiz TB-87). ⇒ Nach diesem
Eintrag und dem neuen Abbild meldet die Sonde dort weiter `_vt.json` mit
„Vollzug steht aus" — **das ist seit 39.2 sachlich überholt**, und die Sonde
kann es nicht wissen, weil die Konstante Code ist. ⛔ Die Sonde wird hier
**nicht** geändert (keine `.py`, 39.10). Die leere Gruppe ist Teil des
Sonden-Entwurfs aus TB-92 (`docs/belege/TB-92/sonde_je_datei_entwurf.patch`),
Handwerk mit eigener Freigabe. Was die Sonde nach dem neuen Abbild tatsächlich
ausgibt, steht in 39.9.

**Marke am alten Ort:** bei **37.2**, unter der Tatsachennotiz TB-87.

### 39.4 ⭐⭐ Determinismusnotiz — die Neurechnung reproduziert `_tb72.json` (TB-91, Bedingung aus 23b)

**Fables Bedingung, 23b Abschnitt 2, zeichengleich:**

> **Bedingung an die Neurechnung — der Determinismusnachweis:** Die neu gerechnete Tabelle muss `benchmark_drawdowns_tb72.json` für **alle neun Bots in allen Werten reproduzieren**; der einzige zulässige Unterschied ist der Name der Bestätigungszeile (und, sofern die Tabelle ihn führt, ein Feld, das diesen Namen wiederholt). Ein `diff`, der etwas anderes zeigt, ist ein **Befund**, kein Ergebnis: Dann hat sich zwischen TB-72 und TB-90 etwas bewegt, das nicht der Name ist — Plan, Daten oder Code —, und das ist vor dem Vollzug zu klären, nicht wegzurechnen. Die Tabelle wird in diesem Fall **nicht** vollzogen.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 35.1 (Bezeichner ist die Spanne, ein anderer ist unzulässig), 23a (Tabelle folgt dem Plan; Neurechnung dort schon vorgesehen), 36.1 (Schreibregel). Und die Bedingung ist 10.1 in Anwendung: Erlaubt sind nur Änderungen mit **bitidentischen** Ergebnissen — die Neurechnung ändert einen Namen, also müssen alle Zahlen gleich bleiben, und wenn sie es sind, ist das zugleich der Nachweis, dass `benchmark.py` deterministisch ist und der Plan sich seit TB-72 nicht bewegt hat (32 hat es behauptet; hier wird es an der Tabelle gemessen). **Kein Ergebnis:** Ich verlange Gleichheit mit einer Tabelle, deren Werte ich nicht kenne; ob sie „gut" oder „schlecht" sind, spielt für die Regel keine Rolle, und sie darf nach 27.1 auch nicht wiedergegeben werden — die Sonde meldet nur „gleich" oder „an Stelle X verschieden".

**Das Ergebnis (TB-91, `docs/belege/TB-91/c_determinismus_ergebnis.txt`,
`c_gegenprobe_text.txt`, `b_neurechnung_lauf.txt`; in TB-94 an den Belegen
nachgelesen) — ⚠️ ohne Werte, Sichtschutz 27.1:**

| | |
|---|---|
| Lauf | `trading-env/bin/python3 -W ignore research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`, `benchmark.py` `d6bdd558…`, HEAD `31008b6`, **rc 0, 56 s** |
| Vergleich | gegen `benchmark_drawdowns_tb72.json` (`e4ba341d…`), rekursiv bis zum Blatt, Typ **und** Wert: **9 Bots, 77 Falten, 63 Botfelder, 9750 Blattwerte** |
| Abweichungen | **0 ausser dem Namen der Bestätigungszeile** (9/9: `2026` bzw. bei `elliott_wave` `2026-2027` → `2026-01-01/2026-09-01`); `dd_toleranz` 9/9 gleich; `status` 9/9 `endgueltig` |
| Gegenprobe auf Textebene | `_tb72.json` geladen, Bestätigungsfalte umbenannt, mit `indent=1, ensure_ascii=False, sort_keys=True` und Schluss-`"\n"` geschrieben → sha256 `64fb2912…`, **bytegleich** mit der Neurechnung |
| ⭐ Selbsttest des Vergleichers | `_tb72` gegen sich selbst **0** Abweichungen; `_tb72` gegen `_vt` **101** — *ein Vergleich, der nichts finden kann, ist keiner* |
| ⭐ Die Wache aus 23a (TB-91 Block D, `d_falten_abgleich_ergebnis.txt`) | Faltenmenge der Tabelle je Bot gegen den Plan im Speicher (`faltenplan.py` `7aa0b8cc…`): **18/18 gleich** (9 Bots × zwei Einstufungen, alle und Selektion), Bestätigungszeile **9/9** gleich der `bestaetigungsperiode` des Plans. Keine Falte fehlt, keine ist zusätzlich |

⇒ **Damit ist Festlegung 32 an der Tabelle gemessen:** Zwischen TB-72 und
TB-91 hat sich an den Benchmark-Drawdowns nichts bewegt ausser dem Namen der
Bestätigungszeile — und `benchmark.py` ist in diesem Umfang deterministisch.

### 39.5 ⭐⭐ Tatsachennotizen zu 37.3 — die fünf Hash-Übergänge

37.3 verlangt für jeden planmässigen Befund vor dem Tag: Auftrag, Freigabe,
alter und neuer Hash. **Vier davon standen bisher nicht im Register.** Alle
fünf, mit **vollem** Hash, gemessen in TB-94 aus der Historie
(`git show <commit>^:<pfad>` bzw. `<commit>:<pfad>`, `a1_hashes.txt`); die
Freigaben aus den Auftragsdokumenten nachgelesen:

| Datei | alt → neu | Auftrag / Commit | Freigabe | Sperrlistenpunkte |
|---|---|---|---|---|
| `research/vorregistrierung/faltenplan.py` | `6f96b95d13563f73b11be69c2bd6996037854df794da61315029216ad0b22bd9` → `fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79` | TB-86, `4daa254` | Betreiber 22.09.2026, 07:50 | 2 — *bereits in 37.3 notiert* |
| `research/vorregistrierung/faltenplan.py` | `fd3e5018ae930c2e29747562a140506d5d9a6bb70b87e96cf5c0089e09afdd79` → `7aa0b8ccf5619a21d5f082f68d81cb412f98ae9c9724e799da8b48dce7498cfb` | TB-90 (Weg (A), 38.1), `303a7fd` | Betreiber 22.09.2026 (`MAC_TB-90`, Kopf) | 2 — **neu** |
| `research/vorregistrierung/benchmark.py` | `3960375a539de8324ccfafaa42596a056fb5dd5c154cd2e05c0ba6a634f3611b` → `d6bdd55805344da09b6b43d791267b43c9702687fc1c7cdbad1473079443e061` | TB-91 (nach 36.1 abgesichert), `31008b6` | Betreiber 23.09.2026, 10:40 | **4 und 6** — neu |
| `research/vorregistrierung/auswertung.py` | `1c2e2daec562d9973f87809fd29ef369db76614ee4bc31c04c6ca201c52a3db0` → `c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062` | TB-92 (39.2), `0292e92` | Betreiber 23.09.2026, 18:12, und Fable 23d | **3, 5 und 14** — neu |
| `research/vorregistrierung/registerbericht.py` | `2b1ce24a8f9b2ece8c98fe2aa84f1f5fdc6ac3da544c0aa765e381505bb1d78f` → `dace1b01826fa6a999beb9a15a8eda41a4e0c97dec584e451cfc0d9b26daac01` | TB-92, `0292e92` | dieselbe | ⭐ **auf keinem Punkt** — nur Tatsachennotiz |
| `research/vorregistrierung/test_vorregistrierung.py` | `55553739c819b78de2f7ac608af2341ec43b7c856c3e8699d5a6ffde67bd15c0` → `6e7defefb46903ccec8df60a350136f5961c137b45fb1a921407e7a8e76f3fbe` | TB-92, `0292e92` | dieselbe | ⭐ **auf keinem Punkt** — nur Tatsachennotiz |

Seit dem jeweiligen Commit hat sich keine der sechs Dateien bewegt (letzter
Commit je Datei = der genannte; Hashes am Stand `12f6089` = „neu").
⭐ **Nach 37.3 ist jeder dieser Befunde der planmässige Fall vor dem Tag** —
Auftrag, Freigabe, alter und neuer Hash stehen hiermit als Tatsachennotiz.
Geschlossen werden sie mit **einem** neuen Abbild (39.9); das alte bleibt.

⚠️ **Zählweise, damit niemand einen Widerspruch liest:** Die sechs Befunde der
Sonde gegen `sperrliste_abbild_2026-09-22.json` (Punkte 2, 3, 4, 5, 6, 14;
`docs/belege/TB-94/a2_sonde_vorher.txt`) stammen aus **drei** Dateien, nicht
aus sechs Änderungen: `faltenplan.py` an 2, `benchmark.py` an 4 und 6,
`auswertung.py` allein an 3, 5 und 14.

⭐ **Ein Fund aus TB-91, der nicht auf TB-91 beschränkt ist — Fables
Tatsachennotiz dazu, 23c Abschnitt 3, zeichengleich:**

> **Tatsachennotiz zu 36.5/37 (kein neuer Registertext):** Ein Punkt mit unmessbaren Bestandteilen wechselt von 2 auf 1, sobald ein messbarer Bestandteil abweicht (erstmals beobachtet TB-91: Punkte 4 und 6 durch `benchmark.py`, planmässig nach 37.3). Die Zahl der Punkte mit 2 ist keine Kenngrösse des Registers, sondern des jeweiligen Standes. Die Sonde meldet je Punkt; eine Datei, die an mehreren Punkten vorkommt, erzeugt eine Tatsachennotiz.

⇒ `A2` („konnte nicht messen ist ein eigenes Ergebnis") heisst **nicht** „bleibt
für immer unmessbar", und die Zahl der nicht prüfbaren Punkte ist keine feste
Grösse. Eine Bilanz mit mehr Punkten `1` ist deshalb nicht schlechter als eine
mit mehr Punkten `2`; sie zeigt nur, welche Dateien sich bewegt haben.

**Marke am alten Ort:** bei **37.3**, unter der Tatsachennotiz zu TB-86.

### 39.6 ⭐ Der Modus-Nachweis — die vollzogene Tabelle ist aus dem registrierten Snapshot bytegleich reproduzierbar (Fable 23e, TB-92 A1b)

**Fables Forderung, 23e Abschnitt 2, zeichengleich (Präzisierung zu 23d,
Registertext „Eingabestand"):**

> Der Reproduzierbarkeitsnachweis einer Eingabedatei wird **im Selektionsmodus** geführt — der Erzeuger liest aus `snapshots/<hash>/`, nicht aus `data/`, mit `--ziel` auf einen Beleg-Pfad; das Ergebnis muss bytegleich zur eingefrorenen Datei sein. Die Tatsachennotiz nennt Snapshot-Hash, Code-Commit und den Modus. Dass `data/` zum Messzeitpunkt bytegleich zum Snapshot war, ist eine eigene Tatsache und ersetzt den Modus-Lauf nicht: Der Lauf am Tag liest den Snapshot-Pfad, und der Nachweis muss denselben Weg gehen wie der Lauf.

**Und die Folge, die er für die Benchmark-Tabelle nennt, zeichengleich:**

> - **TB-92:** dasselbe für die Benchmark-Tabelle aus TB-91 — `benchmark.py` im Selektionsmodus, `--ziel` Beleg-Pfad, `diff` gegen `benchmark_drawdowns_2026-09-23_nach_wegA.json` → bytegleich. Das ist nicht die „Vorab-Nachrechnung" aus 23d, die mit Messbitte (b) entfallen ist (die fragte nach anderen Eingaben); es ist der Nachweis, dass der Erzeuger im Modus dasselbe tut wie ausserhalb. Wenn `benchmark.py` länger braucht als elf Sekunden, ist das Handwerk — der Nachweis gehört trotzdem vor den Tag, einmal.

**Das Ergebnis (TB-92, `docs/belege/TB-92/a1b_ergebnis.txt`,
`a1b_ergebnis_kinder.txt`, `a1b_lesequellen_kinder.txt`; in TB-94 an den
Belegen nachgelesen):**

| | |
|---|---|
| Wurzel | Snapshot `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` (Register 18), MANIFEST-`datenstand_hash` `d9449faf…`; `data/` war zum Messzeitpunkt **225/225** Dateien byteweise gleich dem Snapshot (Anfrage 23g, von Fable in 23e zur Kenntnis genommen) — ⚠️ nach 23e eine eigene Tatsache, die den Modus-Lauf **nicht** ersetzt |
| Umlenkung | `TB30A_BASE_DIR` auf einen Hilfsordner, dessen `data/` (223 Verknüpfungen) und `config/` auf den Snapshot zeigen. ⚠️ `TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` **nicht** (0 Treffer) — der „Modus" ist hier die Umlenkung auf den Snapshot, wie in TB-93 |
| Code-Commit | `d136251` (`benchmark.py` `d6bdd558…`, `faltenplan.py` `7aa0b8cc…`) |
| ⭐ Ergebnis | **Vier Läufe, alle rc 0, je 51–52 s, alle bytegleich** `64fb2912…` mit `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`. Lauf 1 nach `docs/belege/TB-92/benchmark_modusnachweis.json`, die übrigen ins Scratchpad; **nichts in `ergebnisse/` geschrieben** |
| ⭐ Lesequellen | Lesehaken über `sys.addaudithook`, in Lauf 3 und 4 prozessübergreifend über `sitecustomize` (**11 Prozesse**): **0 Lesezugriffe auf `data/` oder `config/` des Repos**; **222** CSV und **2** Universumsdateien aus dem Snapshot. Dazu Eingaben **ausserhalb** des Snapshots — 39.8 |

⇒ **Die vollzogene Tabelle ist aus dem eingefrorenen Datenstand byteweise
wiederherstellbar**, auf dem Weg, den der Lauf am Tag nimmt. Snapshot-Hash,
Code-Commit und Modus stehen damit neben ihrem Hash, wie 23e es verlangt.

⚠️ **Tatsachennotiz:** Der Registertext „Eingabestand eingefrorener
Ergebnisdateien" (23d Abschnitt 2), den 23e präzisiert, ist mit diesem
Abschnitt **nicht** eingetragen — nach 23d Abschnitt 4 gehört er zum Planpunkt
`messgroessen.json` (TB-96). Hier stehen nur die Tatsachen, die er für die
Benchmark-Tabelle verlangt.

> ⭐⭐ **Zweiter Anwendungsfall (40.6, Fable 24a, TB-96, 24.09.2026):** Neben
> `messgroessen.json` fallen die **neun TB-24-Listen** unter 23d
> („Eingabestand") in voller Form — Fables Registertext „Ergänzung zu 23d und
> zu 5.4" steht in **40.6**. Der Registertext „Eingabestand eingefrorener
> Ergebnisdateien" selbst ist weiter **nicht** eingetragen. ⚠️ Die Nummer oben
> ist gerückt: `messgroessen.json` ist **TB-101**, nicht TB-96 (40.9 (c)).

> ⭐⭐ **Dieser Nachweis ist nach der Zwei-Teile-Regel 2 (41.2 B4, 41.3 C6/C7,
> Fable 24c/24d, TB-108, 25.09.2026):** Ein Nachweis besteht aus
> Ergebnisvergleich **und** Leseprotokoll; zeigt das Protokoll einen Zugriff
> ausserhalb, ist er 2 (**41.2, B4**). Das eigene Protokoll dieses Laufs zeigt
> zwei Eingaben ausserhalb des Snapshots (39.8). Zudem war TB-92 A1b ein
> **Hilfsordner-Lauf** (`TB30A_BASE_DIR`, Zeile „Umlenkung" oben) — nach 41.3
> (C6) kein Modus-Lauf; der Ergebnisvergleich bleibt Tatsache, als Nachweis 2
> (**41.3, C7**). Die Tabelle ist seitdem im Resolver-Modus bytegleich
> reproduziert (TB-104 bis TB-107, 42.4 G10) — als Nachweis weiter 2, bis
> beide Eingaben registriert sind. Tabelle und Text oben bleiben zeichengleich.

### 39.7 ⚠️ Tatsachennotiz — `herkunft.py::EINGEFROREN` zeigt weiter auf den historischen Stand

`research/vorregistrierung/herkunft.py` ist **unverändert** (`56a1c2e1…`,
TB-94 gemessen). Seine Liste `EINGEFROREN` hasht damit weiter
`ergebnisse/benchmark_drawdowns.json` — **nicht** die Tabelle, die der Lauf
liest. **Fable, 23d Abschnitt 1, zeichengleich:**

> **(2) `EINGEFROREN` bleibt, wie es ist — es trägt weiter den alten Pfad, nicht beide.** Der Grund ist nicht der Wortlaut, sondern der Ort: `EINGEFROREN` steht in `herkunft.py` (Punkte 11/12), und in 22d habe ich entschieden, `herkunft.py` nicht zu öffnen, weil die Sperrlisten-Sonde die Lücke schliesst. Das gilt hier genauso: Die **neue** Tabelle ist durch Punkt 4 und das Abbild geschützt (Sonde); die **alte** bleibt in `EINGEFROREN` als das, was sie ist — der registrierte historische Stand, dessen Hash `register()` bezeugt. Die Tatsachennotiz zu 37.4 wird um den Satz ergänzt: „`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde." Zwei Nachweise, zwei Gegenstände, kein Widerspruch (22d).

⇒ Die neue Tabelle schützen **Punkt 4** (39.2) und **das Abbild** (39.9);
beides ist mit diesem Abschnitt erfüllt. ⭐ **Deshalb ist das eine
Tatsachennotiz und kein Befund** — aber sie gehört ins Register, damit niemand
`EINGEFROREN` für vollständig hält. Der Satz, um den Fable die Tatsachennotiz
zu 37.4 ergänzt, steht dort als Marke.

**Fables Präzisierung zu 36.1 (1), 23c Abschnitt 2, zeichengleich** — „gesperrt"
umfasst jeden Pfad, dessen Hash am Tag bezeugt wird, **auch
`herkunft.py::EINGEFROREN`**:

> **Präzisierung zu 36.1 (1):** „auf der Sperrliste steht oder für sie bestimmt ist" umfasst jeden Pfad, dessen Hash am Tag bezeugt wird — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) **und die Einträge von `herkunft.py::EINGEFROREN`**, solange `register()` über sie hasht. Die Sperrlisten-Sonde führt diese Pfade als dritte Gruppe („Abschnitt 0") und prüft sie gleich.

⚠️ **Tatsachennotiz:** Die „dritte Gruppe" („Abschnitt 0") führt die Sonde
heute **nicht** — sie kennt `EINGEFROREN` nicht (Kopf von
`shared/sperrlistensonde.py`). Offen, Handwerk mit eigener Freigabe.

> ⭐ **Stand (42.3 F2, 42.5, TB-108, 25.09.2026):** „`herkunft.py` ist
> unverändert (`56a1c2e1…`)" beschreibt den Stand von TB-94. Seit TB-106
> (`5791b4c`) ist es planmässig geöffnet (`351f24c2…`); `EINGEFROREN` ist dabei
> zeichengleich geblieben und zeigt weiter auf
> `ergebnisse/benchmark_drawdowns.json`. Die dritte Gruppe führt die Sonde seit
> TB-97 aus dem Abbild (Gruppe „eingefroren" in `cb4eb1b4…` und `40ffe18d…`).
> Der Text oben bleibt zeichengleich.

**Marke am alten Ort:** bei **37.4**, vor der Marke am alten Ort des
Abschnitts.

### 39.8 ⭐⭐ Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand

Der Modus-Lauf (39.6) hat neben dem Snapshot **zwei weitere Eingabequellen im
Repo** geöffnet (`docs/belege/TB-92/a1b_lesequellen_kinder.txt`, Lauf 3 und 4
gleich):

| Eingabe | Tatsache |
|---|---|
| `research/vorregistrierung/ergebnisse/messgroessen.json` | ⚠️ beschreibt nach TB-93 einen Datenstand, den es nicht mehr gibt (Eingabestand vor `90e3cbd`, TB-34). Wird mit **TB-96** geschlossen (23d, 23e) |
| **neun** `research/tb24_haltedauern/daten/*_alle_trades.csv` | ⚠️ Ergebnisdateien, keine Kursdaten; weder auf der Sperrliste noch im Snapshot. Der Weg führt über den Faltenplan (TB-92) |

**Fable, 23f Abschnitt 6, zeichengleich — der Fund:**

> Die Sitzung hat protokolliert, was der Modus-Lauf öffnet: 222 aus `snapshot/csv`, 2 aus `snapshot/config`, **dazu `ergebnisse/messgroessen.json` und neun Trade-Listen aus dem Repo.** Das ist die Sonde „Lesequellen" als Laufzeitmessung — genau 5e —, und sie zeigt zweierlei: Erstens liest der Benchmark-Lauf die Messdatei, deren Eingabestand 23d beanstandet hat (das ist bekannt und wird mit TB-94 geschlossen). Zweitens **neun Trade-Listen**. Die sind Ergebnisdateien, keine Kursdaten, und sie stehen weder auf der Sperrliste noch im Snapshot.

⚠️ **Berichtigung einer Nummer, damit die Ablage lesbar bleibt:** Fable nennt
oben (und in 23e Abschnitt 2) für den Eingabestand von `messgroessen.json` die
Nummer **TB-94**; so stand es im Plan des steuernden Chats vom Vormittag des
23.09. Die Nummern sind danach gerückt, weil der Registervollzug vorgezogen
wurde (`docs/auftraege/AKTUELLER_AUFTRAG.md`, 23.09.2026, 20:00): **TB-94 ist
dieser Eintrag, TB-95 sind `G6`/`H3` und die Messbitte unten, TB-96 ist
`messgroessen.json`.** *Eine Nummer, die zwei Sachen meint, ist schlimmer als
eine verschobene.*

⚠️⚠️ **OFFEN — Fables Messbitte, eingetragen, nicht beantwortet** (23f
Abschnitt 6, zeichengleich):

> **Messbitte, nur das Ob:** Welcher Schritt des Modus-Laufs öffnet die neun Trade-Listen — `benchmark.py` selbst, oder ein Nebenweg (`registerdaten.py`, `faltenplan.py`, Trockenlauf)? Und **gehen ihre Inhalte in die Tabelle ein** — oder werden sie nur geöffnet (etwa für eine Konsistenzprüfung)? Wenn sie eingehen, hat die Benchmark-Tabelle eine Eingabe, deren Eingabestand nicht registriert ist — derselbe Fall wie `messgroessen.json`, und die Regel aus 23d gilt für sie. Wenn sie nur geöffnet werden, ist es eine Tatsachennotiz und ein Kandidat für die Lesequellen-Sonde.

**Seine Unsicherheit dazu, zeichengleich:**

> **Unsicher:** ob die neun Trade-Listen die TB-24-Listen sind (dann alter Code, alter Datenstand — 26.5) — das ändert nicht die Frage, nur ihr Gewicht.

⛔ **In TB-94 nicht gemessen und nicht beantwortet** — Gegenstand von TB-95.

**Zwei weitere Tatsachen aus TB-92 (`docs/ERGEBNIS_TB-92_vollzug_punkt8.md`,
Abschnitt 2, A1b-6), die hierher gehören:** (1) `benchmark.py` und
`messgroessen.py` lesen an `shared/paths.py` **vorbei** (`TB30A_BASE_DIR` bzw.
`<BASE>/data`); die Kindprozesse des Faltenplans folgen **eigenen** Variablen
(`faltenplan_neun.py` `TB36_BASE_DIR`, `universum_trockenlauf.py` und
`loaderlauf.py` `TB40_BASE_DIR`) und haben gemessen trotzdem aus dem Snapshot
gelesen. (2) Der Lauf öffnet `logs/notifications/manuelle_eingriffe.log` im
Modus `a` (Import aus `notifications/`); die Datei blieb unverändert (mtime
11.09.). Beides ist Stoff für Fables Sonde „Lesequellen" (23d), nicht für
diesen Eintrag.

⭐⭐ **Nachtrag zu 39.8 (40.5, Fable 24a, TB-96, 24.09.2026) — die Messbitte
oben ist beantwortet.** Gemessen in TB-95 (`069370d`; Belege
`docs/belege/TB-95/d1_wer_oeffnet.txt`, `d2_stoerprobe.txt`, `d3_antwort.md`),
im Modus-Lauf gegen den Snapshot `63e4b6c8…`, Sichtschutz 27.1 (keine
Ergebnisgrössen):

| | |
|---|---|
| **Wer öffnet** | **`benchmark.py` selbst**, kein Nebenweg: `benchmark.py::je_bot` → `faltenplan.py::faltenplan` → `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (`read_csv`). Jede der neun Listen **genau einmal**, **nur im Hauptprozess**; die zehn Kindprozesse (Trockenlauf/Loader) und `registerdaten.py` öffnen keine davon |
| **Gehen sie ein?** | **Ja — über genau eine Grösse, die Faltenlänge.** Gelesen wird nur `entry_time`; gezählt je vollem Kalenderjahr, gemittelt, gegen die Schwelle aus 5.4 verglichen ⇒ Faltenlänge 1 oder 2 ⇒ Faltengrenzen ⇒ Tabellenzeilen. Sonst erreicht nichts aus den Listen die Tabelle |
| **Störprobe, in beide Richtungen** (auf Kopien, Originale vorher = nachher) | **eine Zeile weg ⇒ Tabelle bytegleich** (`64fb2912…`), weil die Schwelle nicht überschritten wird; **zwei von drei Zeilen weg ⇒ verschieden** (`97cf224f…`): **ein** Bot (`volatility_breakout_crypto`) kippt von Einjahres- auf Zweijahresfalten, die anderen **acht bleiben gleich** |
| **Herkunft** | ein einziger Commit, **`78e2bc6`, 13.09.2026, TB-24**, seitdem unverändert — die TB-24-Listen, gemessen an Pfad, Commit und Datum; vor TB-31/TB-34/TB-38 und vor dem Snapshot. **Nicht im Snapshot, nicht auf der Sperrliste**; im Register als Quelle genannt (5.4), **ohne Hash** |
| Nebenbefund | Derselbe Modus-Lauf lieferte die vollzogene Tabelle zum fünften Mal bytegleich (`64fb2912…`, 39.6) |

⚠️ **Der methodische Satz, der über den Fall hinausgeht:** Die Störprobe, wie
der Auftrag TB-95 sie vorschlug („eine Zeile entfernen genügt"), hätte
**allein das falsche „nein"** ergeben. Eine Eingabe, die über eine Schwelle
wirkt, zeigt bei kleinen Änderungen nichts; wer nur in eine Richtung stört,
misst die Schwelle nicht, sondern ihren Abstand. ⇒ Eine Störprobe nach „geht
es ein?" wird in **beide** Richtungen geführt: klein (bleibt gleich?) **und**
über eine bekannte Schwelle hinweg (ändert sich?).

⇒ **Die Einordnung steht in 40.6:** Die neun Listen sind Eingabedateien nach
23d in voller Form — Neu-Erzeugung auf dem Snapshot, Sperrlistenpunkt,
Ableitung der Faltenlänge nach 5.4 und Vergleich gegen 33.2 (TB-98). Die
Nummer 40.5 verweist hierher.

> ⭐⭐ **Zwei Nachträge (41.3 C9, 42.1 D10/D11, Fable 24d/25a, TB-108,
> 25.09.2026):** (1) Der Lesehaken dieses Abschnitts ist **von TB-92** — der
> Satz „erst mit TB-95" des steuernden Chats war falsch, dieses Register hatte
> recht (Messung in **41.3, C9**). (2) Das Öffnen von
> `logs/notifications/manuelle_eingriffe.log` im Modus `a` ist ein Schreibziel
> ausserhalb `--ziel` (Klasse (iii), 42.1 D6); **behoben in TB-105**
> (`d48a195`), der Benchmark-Lauf im Modus öffnet es seither nicht mehr
> (**42.1, D11**). Der Text oben bleibt zeichengleich.

### 39.9 Das neue Abbild und die Sonde

**Was 36.6 und 37.3 verlangen:** Jede Fortschreibung der Sperrliste vor dem Tag
erzeugt ein **neues** Abbild unter neuem Namen; das alte bleibt und wird nie
angepasst; das aktuelle Abbild steht selbst mit Hash im Register. Ein Befund
`1` aus beauftragter Änderung wird durch Tatsachennotiz (39.5) und neues
Abbild geschlossen. **Fable, 22g, zeichengleich:** *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

**Was die Sonde am Tag liefern muss — Fable, 23c Abschnitt 3, zeichengleich:**
*„Die Tag-Vorbedingung aus 22d/37 lautet: kein Pfad-Bestandteil 1, jede 2 mit Tatsachennotiz."*
⇒ „Sonde 0 für die Pfade" im Fertigkriterium (39.1) heisst: **jede Datei
jedes Punktes gleich** und Prüfung (ii) `0`. Ein Gesamtausgang `2` wegen
Punkten, die Nicht-Dateibezogenes nennen (Werte, Funktionen,
Registerverweise), ist damit vereinbar; er ist keine Aussage über die Pfade.

**Reihenfolge:** Das Abbild liest den Listentext von Abschnitt 10. Es wird
deshalb **nach** dem Commit gezogen, der Punkt 4 (39.2) und diesen Abschnitt
enthält, mit `research/vorregistrierung/sperrliste_abbild.py --ziel` (keine
Voreinstellung, Einmal-Schreibsperre). Name, Hash und die Bilanz der Sonde
davor und danach werden **unmittelbar unten** eingetragen, in einem eigenen
Commit — additiv, der Listentext von Abschnitt 10 wird dabei nicht berührt.

**Ergebnis (Block D, TB-94, 23.09.2026; `docs/belege/TB-94/d1_abbild.txt`,
`d2_sonde_nachher.txt`, `a2_sonde_vorher.txt`,
`b_sonde_nach_blockB_altes_abbild.txt`):**

| | |
|---|---|
| ⭐ Neues Abbild | `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json`, **sha256 `2f23f76c99e22991e4a331ec1107dc0f090a425bc9e050793470ee3cd52dd4fe`**, 7351 Bytes, erzeugt 2026-09-23T18:21:35Z am Stand `27b68b9` (der Commit mit 39.2 und diesem Abschnitt), 14 Punkte aus Abschnitt 10 (Z. 845–958 am Stand `27b68b9`), 15 Pfadnennungen; `sperrliste_abbild.py --ziel` rc 0, Ziel existierte vorher nicht |
| Altes Abbild | `sperrliste_abbild_2026-09-22.json` `6a1b732e…` — **nicht gelöscht, nicht geändert** (36.6); vor und nach dem Ziehen gemessen |
| Sonde vorher (altes Abbild, Stand `12f6089`) | rc **1**; Befund an **2, 3, 4, 5, 6, 14** (drei Dateien, 39.5); (ii) `0`; Bilanz 0 / 6 / 8 |
| Sonde nach Block B und C (altes Abbild, uncommittet) | rc **1**; dazu (ii) **1** an Punkt 4, Felder `pfade` und `nicht_dateibezogen` — der neue Pfad. Das ist der erwartete Nachweis, dass die Sonde die Pfadzeile liest |
| ⭐ Sonde gegen das neue Abbild (Stand `27b68b9`) | rc **2**; **0 Befunde**; **alle 15 Pfadnennungen „gleich"**, darunter `ergebnisse/benchmark_drawdowns.json` `a163c498…` und `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` `64fb2912…`; Punkte **2 und 5** `0`; Punkte 1, 3, 4 und 6–14 `2`, jeder wegen Nicht-Dateibezogenem im Punkttext; (ii) `0`, Listentext wie bei Erzeugung: ja. Bilanz **2 / 0 / 12** |
| Gruppe „bestimmt" | die Sonde nennt weiter `ergebnisse/benchmark_drawdowns_vt.json` (`4549395f…`) mit „Vollzug steht aus" — die feste Konstante aus 39.3; nach dem Registertext ist die Gruppe leer |

⇒ **Die planmässigen Befunde aus 39.5 sind geschlossen: kein Pfad-Bestandteil
ist `1`.** Der Gesamtausgang `2` sagt nichts über die Pfade, sondern über
Werte, Funktionen und Registerverweise in den Punkttexten (A2, je Sache; 23c).
Punkt 4 steht auf `2`, nicht auf `0`, weil schon sein alter Text
„einschliesslich der Interpolationsregel" nennt; die Pfadzeile aus 39.2
bringt weiteren Wortlaut dazu, ändert am Ausgang aber nichts. ⚠️ Ob **jede**
`2` eine Tatsachennotiz trägt, ist Tag-Vorbedingung (23c) und hier **nicht**
geprüft.

⭐ **Das aktuelle Abbild der Sperrliste (36.6) ist damit
`sperrliste_abbild_2026-09-23.json`, `2f23f76c…`.**

### 39.10 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `auswertung.py`, `registerbericht.py`, `test_vorregistrierung.py`, `benchmark.py`, `faltenplan.py`, `messgroessen.py`, `herkunft.py` noch `shared/sperrlistensonde.py` | — |
| ⛔ | **Nichts gerechnet** — `benchmark.py`, `faltenplan.py main()`, `messgroessen.py` nicht aufgerufen; in `research/vorregistrierung/ergebnisse/` nichts geschrieben **ausser dem neuen Abbild** (39.9) | — |
| ⛔ | **`G6`/`H3` nicht angefasst** — weder gemessen noch erklärt noch angepasst | TB-95 |
| ⛔ | **Fables Messbitte zu den neun Trade-Listen nicht beantwortet** (39.8) | TB-95 |
| ⛔ | **`messgroessen.json` nicht angefasst**; der Registertext „Eingabestand" (23d) nicht eingetragen (39.6) | TB-96 |
| ⛔ | **Der Sonden-Entwurf `sonde_je_datei_entwurf.patch` nicht angewandt**; die Konstante `BESTIMMT_NICHT_EINGETRAGEN` und die dritte Gruppe (39.3, 39.7) bleiben, wie sie sind | Handwerk, eigene Freigabe |
| ⛔ | **Kein alter Registersatz umgeschrieben** — der Satz mit „grün" in 38.4, die offene Frage in 38.7 (d), der Kasten an Punkt 4 und die Punktzeilen 1–4 von Punkt 4 bleiben zeichengleich; ERSETZT-, Vollzugs- und Hinweis-Marken, nichts entfernt | — |
| ⭐ | **`benchmark_drawdowns.json` byteweise unverändert** (`a163c498…`) — vor Block B, nach Block B und nach dem Abbild gemessen (`a1_hashes.txt`, `d1_abbild.txt`) | — |
| ⭐ | **N = 653 (Festlegung 10) unberührt**; Zellenzahl je Bot 80/384/400/96/320/320/400/96/320, **Summe 2416**, wie Register Abschnitt 3 (ERZEUGT-Block; gemessen TB-92, `docs/belege/TB-92/d_zellenzahl.txt`) | — |
| ⚠️ | **Offen:** `G6`/`H3` und die Messbitte (TB-95) · `messgroessen.json` und der Registertext „Eingabestand" (TB-96) · die Sonde: leere Gruppe „bestimmt", dritte Gruppe „Abschnitt 0", „Schreibziele", „Lesequellen" (23c, 23d) · „null rote Prüfungen" als Tag-Vorbedingung (21.9, 23a) | TB-95 / TB-96 / Handwerk |

*Dieser Abschnitt ist rein additiv: Er vollzieht Sperrlistenpunkt 4 in Form
(ii) durch drei neue Folgezeilen, berichtigt ein Fertigkriterium, ohne den
alten Satz anzutasten, trägt die Messungen aus TB-91 und TB-92 als
Tatsachennotizen samt einer offenen Messbitte ein, setzt zehn Marken am alten
Ort — und entfernt nichts. Gebaut und gerechnet wird nichts.*

## 40. Testannahmen folgen dem Register, und die neun Handelslisten sind Eingabedateien — `G6`/`H3`, die Kopplung an 5.1 Nr. 4, jede Mutationsprobe mit Gegenprobe, was TB-97/TB-98 tun, und drei angenommene Berichtigungen an den Verfahrensprüfer (Fable 24a, TB-96, 24.09.2026)

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 39. Der Test
ist seit TB-95 grün (40.1–40.4); Fable hat in **24a** geantwortet und dazu
**zwei neue Registertexte** gesetzt: die neun Handelslisten als
Eingabedateien nach 23d (40.6) und die Gegenprobe jeder Mutationsprobe als
Ergänzung zu 12 (40.7). Was daraus beschlossen, aber nicht ausgeführt ist,
steht in 40.8; drei Berichtigungen an ihn, die er angenommen hat, in 40.9.
Fable-Texte zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`
— **eingesetzt, nicht abgetippt** (Beleg `docs/belege/TB-96/d2_zitate.txt`, je
Zitat `diff` rc 0). Anfrage
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-24a_punkt8_vollzogen_test_gruen_neun_listen.md`;
Auftrag `docs/auftraege/MAC_TB-96_register_40.md`; Belege
`docs/belege/TB-96/`; Schritt-0-Commit `fc8d44c`. Messungen des Vorgängers:
TB-95 (`docs/ERGEBNIS_TB-95_testannahmen_und_lesehaken.md`, Belege
`docs/belege/TB-95/`), in TB-96 an Hashes und Register nachgemessen
(`a_messungen.txt`).
⛔ **Keine `.py` geändert, nichts gerechnet** — 40.10.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text,
Herkunft und Grund **und** als Marke direkt beim alten Satz (5.1 Nr. 4; 5.4;
12; 21.9; 33.2; 33.5; 36.6; 37.2; 39.6; dazu der Nachtrag in 39.8 — zehn
Stellen). Die alten Sätze bleiben zeichengleich; `git diff --numstat` auf
dieses Register zeigt für TB-96 in der zweiten Spalte `0`.

**Fables Kenntnisnahme, 24a Abschnitt 1, zeichengleich:**

> **Punkt 8 im Register:** 575/0, 29 Zitate mit `diff` rc 0, zehn Marken, Abbild `2f23f76c…`, Sonde 0 Befunde — alle acht Kriterien erfüllt. **Plan-Punkt 8 ist fertig.** Der benannte Zwischenzustand hat eine Nacht gedauert und ist geschlossen; so war es gemeint.

### 40.1 Tatsachennotiz — der Test ist grün

`research/vorregistrierung/test_vorregistrierung.py` (`73c9b837…`, Commit
`9e2a071`, TB-95) läuft am 23.09.2026 **165/165, rc 0**, 534 s, in einem Zug
am echten Stand (`docs/belege/TB-95/c_test.txt`). ⇒ **Die Tag-Vorbedingung
„null rote Prüfungen, null ‚bekannt rot'" (21.9, A4; 23a, Wortlaut in 39.1) ist
für diesen Test erfüllt.** Geändert ist nur diese eine Datei
(`6e7defef…` → `73c9b837…`); keine Prüfung entfallen, keine Ausnahme für einen
Bot, keine Toleranz, `auswertung.py` unberührt; kein Sperrlistenhash bewegt;
Sonde gegen `sperrliste_abbild_2026-09-23.json` 0 Befunde, 15/15 Pfade gleich
(`docs/belege/TB-95/c_hashes.txt`, `c_sonde.txt`). In TB-96 nachgemessen:
Hash und letzter Commit unverändert (`a_messungen.txt`, A2).

**Fable, 24a Abschnitt 1, zeichengleich:**

> **Test grün:** 165/165, rc 0, nur eine Datei geändert, keine Prüfung entfernt, keine Toleranz, `auswertung.py` unberührt. Die zwei Berichtigungen der Sitzung an den Erwartungen des Auftrags sind das Wertvollste daran: H3 griff nicht ins Leere, sondern die **Zahl** war gealtert (vier reichten bei sieben, nicht bei neun) — dieselbe Klasse wie der Name, nur unsichtbarer; und die Quelle des Plans ist `faltenplan.py` zur Laufzeit, nicht die historische Datei (30.2 (1)). Die Bauart von G6 (Jahre maschinell aus 5.1 Nr. 4, sonst `None` ⇒ rot) und H3 (strikte Mehrheit, paritätsfest) ist genau das, was 23a verlangt hat, und die vier Gegenproben — vor allem „`ohne` leer ⇒ scheitert" — zeigen, dass sie aus dem richtigen Grund bestehen.

⚠️ **Was „erfüllt" hier heisst und was nicht:** Die Vorbedingung gilt für den
Stand von heute. 40.8 beschliesst weitere Änderungen an genau diesem Test
(`F4`, die vier Literale, Gegenproben); jede davon muss ihn wieder grün
hinterlassen. Und ein grüner Test ist nach 40.7 erst dann ein Nachweis, wenn
jede seiner Mutationsproben eine Gegenprobe hat — für `H3` ist sie geführt
(40.3), für die übrigen sieben steht sie aus (40.8 (c)).

**Marke am alten Ort:** bei **21.9**, unter der Tabelle der Folgen.

### 40.2 `G6` — die Jahre aus dem Register, die Abdeckung gerechnet

**Wie gebaut (TB-95, `9e2a071`):** `G6` liest die Jahre aus dem Registertext
**5.1 Nr. 4** (Funktion `_testjahre_aus_register`) und rechnet die Abdeckung
aus `von`/`bis_ausschliesslich` der Falten mit Rolle `selektion`
(`_abgedeckte_jahre`); die Bestätigungsperiode zählt nicht. Bis TB-95 stand
dort `"2020" in namen` — seit den Zweijahresfalten von `elliott_wave` traf das
nichts mehr.

**Gemessen vor der Änderung (TB-95, `a2_g6.txt`):** 2020 und 2022 lagen bei
**allen neun** Bots in genau einer Selektionsfalte, bei `elliott_wave` in
`2020-2021` und `2022-2023`. ⇒ **Die Sache hinter 5.1 Nr. 4 war erfüllt; rot war
nur die Formulierung.** Die Probe beisst (TB-95, `b_probe.txt`): Falte
`2020-2021` als Bestätigung ⇒ genau ein `G6` rot; Registersatz fehlt (Kopie) ⇒
neun `G6` rot.

⚠️⚠️ **Die Kopplung, gemessen (TB-96, `a_messungen.txt`, A6):** Die Funktion
sucht im ganzen Register **zeilenweise, am Zeilenanfang verankert**, die Zeile,
die mit `4. **JJJJ und JJJJ sind Testfalten, keine Trainingsjahre.**` beginnt
(Muster `^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*`).
Heute: **genau ein Treffer**, der Listenpunkt 5.1 Nr. 4; Ergebnis `[2020, 2022]`.
Kein Treffer **oder zwei** ⇒ `None` ⇒ `G6` rot für alle neun Bots. Daraus
folgt zweierlei:

| | |
|---|---|
| (1) | **Wer 5.1 Nr. 4 umformuliert** — auch gut gemeint, auch nur Satzzeichen oder Hervorhebung —, **macht `test_vorregistrierung.py` rot.** Eine Änderung der Sache (andere Jahre) braucht einen eigenen Registereintrag **und** die Anpassung von `G6` im selben Auftrag |
| (2) | **Wer irgendwo im Register eine zweite Zeile mit diesem Anfang schreibt**, etwa ein Zitat von 5.1 Nr. 4 in Spalte 0, macht ihn ebenso rot. Zitate dieser Zeile stehen deshalb eingerückt oder als Blockzitat (`> `) — so auch in diesem Abschnitt |

⭐ **Das ist eine Kopplung, die bis heute niemand sah:** Registertext wird
sonst gelesen, nicht geparst; die Sperrlisten-Sonde liest Abschnitt 10, und
dort steht es seit 36 im Register. Für 5.1 Nr. 4 stand es nirgends. **Die
Marke bei 5.1 Nr. 4 ist der eigentliche Schutz** — sie steht dort, wo jemand
ändern würde.

**Marke am alten Ort:** bei **5.1 Nr. 4**, direkt unter dem Listenpunkt.

### 40.3 `H3` — strikte Mehrheit statt fester Zahl

**Wie gebaut (TB-95, `9e2a071`):** `ohne` = die ersten `len(sel) // 2 + 1`
Selektionsfalten des Plans — eine **strikte Mehrheit**, die bei jeder Parität
beisst; beim Plan von TB-95 für `turtle_soup_stocks` fünf von neun
(`2017`–`2021`).

**Gemessen vor der Änderung (TB-95, `a3_h3.txt`):** Die vier alten Namen
(`2019`–`2022`) **trafen alle** — die Probe griff nicht ins Leere. Aber vier
Nullen verschieben den Median über **neun** Falten nicht (`0.1000` /
`0.1000`); bei sieben Falten, für die die Zahl einst gewählt war, reichten
vier. Allgemein ist das kleinste wirksame k = ⌈n/2⌉. **Die Probe beisst
wieder** (`0.0000` / `9.0000`), und **die Gegenprobe mit leerer Menge
scheitert** (`0.1000` / `0.1000`) — sie beisst aus dem richtigen Grund.

⭐ **Fables Einordnung, 24a Abschnitt 1, zeichengleich:**
*„H3 griff nicht ins Leere, sondern die **Zahl** war gealtert (vier reichten bei sieben, nicht bei neun) — dieselbe Klasse wie der Name, nur unsichtbarer"* — und weiter:
*„Die Bauart von G6 (Jahre maschinell aus 5.1 Nr. 4, sonst `None` ⇒ rot) und H3 (strikte Mehrheit, paritätsfest) ist genau das, was 23a verlangt hat"*.

### 40.4 Die weiteren Literale und `F4`

**Die Liste aus TB-95 (`a4_literale.txt`), in TB-95 nicht geändert, weil heute
grün:**

| Stelle (Datei, Teil) | Literal | Zustand | warum es trotzdem gealtert ist |
|---|---|---|---|
| `test_vorregistrierung.py`, Teil D | `ruhig, krise = "2021", "2020"` | grün | nur weil `BOT` Einjahresfalten hat; die Jahreswahl ist Registerinhalt 4.4. ⚠️ Bekommt `BOT` Zweijahresfalten, **bricht Teil D mit `KeyError`** |
| `test_vorregistrierung.py`, Teil F | `ohne = "2022"` | grün | aus demselben Grund; F1/F2 würden rot |
| `beispieldaten.py`, Krisen-Drawdown | `falte in ("2020", "2022")` | keine Prüfung | trifft bei `elliott_wave` nie |
| `beispieldaten.py`, Exposure | dasselbe | keine Prüfung | bei `elliott_wave` konstant; der Zufalls-Timing-Test ist dann nach dem eigenen Docstring **entartet** |

(Zeilennummern am Stand `9e2a071`: Teil D Z. 246, Teil F Z. 442,
`beispieldaten.py` Z. 69 und 77 — nach 38.2 nur mit Commit.)

⚠️ **Dazu `F4` (TB-95, Zusatzbefund):** Die Prüfung sagt „Median mit der Null
liegt **unter** …", prüft aber mit `<=`. Bei einer Null unter neun (oder
sieben) Falten sind beide Mediane gleich. **`F4` hat nie gebissen** — und das
hängt nicht am Plan.

**Fable, 24a Abschnitt 5, zeichengleich:**

> **Vor dem Tag.** Eine Prüfung, die nie beissen konnte (`<=` statt `<`, bei gleichen Medianen), ist kein Nachweis; sie steht aber in der Zahl, mit der Abschnitt 12 die Vollständigkeit belegt („150 Prüfungen, davon acht Mutationsproben"). Am Tag muss diese Zahl wahr sein — nicht als Anzahl, sondern als Aussage. Dass F4 nicht am Faltenplan hängt, ändert die Kategorie („Testannahmen folgen dem Register" → hier: „die Prüfung prüft, was sie sagt"), nicht den Zeitpunkt. `<=` → `<`, Probe mit Mehrheit wie H3, Gegenprobe „leere Menge ⇒ scheitert".

**Und zu den Literalen, 24a Abschnitt 6, zeichengleich:**

> Euer Satz ist der Grund: **Eine Prüfung, die grün ist, weil ihr Literal zufällig noch stimmt, ist genauso gealtert wie eine rote — sie sagt es nur noch nicht.** Teil D bricht mit `KeyError`, sobald der Bot Zweijahresfalten bekommt — und ob er das nach Abschnitt 3 dieser Antwort bekommt, weiss heute niemand. Also vor der Ableitung umstellen, nicht danach.

⇒ **Beides ist beschlossen (40.7, 40.8 (a)–(c)), nicht erledigt.**

### 40.5 ⛔ Entfällt als eigener Unterabschnitt — steht als Nachtrag in 39.8

Die Antwort auf Fables Messbitte zu den neun Handelslisten (23f Abschnitt 6)
steht als **Nachtrag am Ende von 39.8**, nicht hier. **Fable, 24a Abschnitt 4,
zeichengleich:**

> Eintragen, wie vorgeschlagen, mit: **40.5 als Nachtrag zu 39.8** (es setzt dessen Tatsache fort, und wer 39.8 liest, soll dort fündig werden — dieselbe Regel wie bei den Marken am alten Ort); und **40.6 neu:** die Entscheidung aus Abschnitt 3 dieser Antwort (Listen als Eingabedateien, Neu-Erzeugung, Vergleich gegen 33.2, Sperrlistenpunkt), damit 40.5 nicht mit „Einordnung steht aus" endet, sondern mit der Einordnung. 40.4 (Liste der weiteren Literale) bleibt, wird aber durch Frage (4) unten zum Auftrag.

⭐ *Diese Nummer steht trotzdem hier, damit niemand später 40.5 sucht und das
Register für lückenhaft hält.* Die Einordnung, mit der der Nachtrag endet,
steht in **40.6**.

### 40.6 ⭐⭐ Die neun Handelslisten — Eingabedateien nach 23d

**Was gemessen ist** (TB-95, Nachtrag in 39.8): `benchmark.py` öffnet die neun
`research/tb24_haltedauern/daten/<bot>_alle_trades.csv` über
`faltenplan.py::faltenlaenge_jahre`; ihre Inhalte gehen **über eine
Schwellenentscheidung** — die Faltenlänge nach 5.4 — in Faltenplan und Tabelle
ein. Sie stammen aus `78e2bc6` (TB-24, 13.09.2026), liegen nicht im Snapshot,
nicht auf der Sperrliste. Die Frage an Fable (Anfrage 24a): Genügt dafür ein
Hash-Eintrag, oder gilt die volle Regel aus 23d?

**Der Registertext — Fable, 24a Abschnitt 3, zeichengleich:**

> **Registertext, Ergänzung zu 23d („Eingabestand") und zu 5.4:** Die neun Trade-Listen, aus denen `faltenlaenge_jahre` die Faltenlänge nach 5.4 ableitet, sind Eingabe einer Herleitung von Registertext (33.2) und damit Eingabedateien im Sinn von 23d. Sie werden **vor dem Tag einmal auf dem registrierten Snapshot mit dem registrierten Code neu erzeugt** — im Selektionsmodus, mit den registrierten heutigen Parametern, durch einen Erzeuger unter 36.1 (`--ziel`, Einmal-Schreibsperre), mit Beleg, je Liste Hash, Snapshot-Hash und Commit als Tatsachennotiz — und als Punkt auf die Sperrliste aufgenommen; `faltenplan.py` liest sie über einen registrierten Pfad (Konstante, kein Schalter). Die alten Listen (`78e2bc6`) bleiben liegen als historischer Stand mit Tatsachennotiz. **Danach wird die Faltenlänge je Bot nach 5.4 aus den neuen Listen abgeleitet und gegen 33.2 verglichen.** Gleich ⇒ Tatsachennotiz. Verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt (Benchmark-Tabelle, Abbild), mit dem Grund „Eingabe war auf nicht-registriertem Datenstand erzeugt" — keine Wahl. Der Reproduzierbarkeitsnachweis (23e) ist der Modus-Lauf selbst: zweimal, bytegleich.

**Sein Grund, zeichengleich:**

> **Die volle Regel.** Und zwar aus dem Grund, den die Störprobe selbst liefert: Eine Schwellenentscheidung ist nicht „kleiner" als ein stetiger Einfluss, sie ist **unsichtbarer**. Kleine Änderungen zeigen nichts, ein Übertritt verschiebt den ganzen Faltenplan eines Bots — und damit 33.2, die Benchmark-Tabelle, die Zellen. Ein Hash-Eintrag würde festhalten, **dass** die Listen so sind, wie sie sind; er sagt nichts darüber, ob sie den Datenstand beschreiben, mit dem der Lauf rechnet. Genau das war der Befund bei `messgroessen.json` (23f/23d), und hier ist er derselbe: **erzeugt vor TB-34, die Krypto-Listen beginnen 2021-09, der Snapshot beginnt 2017-08.** Ob die Faltenlänge eines Krypto-Bots auf dem Snapshot anders ausfiele, weiss ich nicht — und das ist der Grund, die Regel zu halten, nicht sie zu lockern: Wer jetzt „Hash genügt" sagt, weil ein Nachrechnen Falten bewegen könnte, wählt nach Wirkung.

**Seine Antwort auf unseren Einwand — 23d verlangt „aus", nicht „im" Snapshot,
zeichengleich:**

> **Zu eurem Einwand „nicht möglich, ohne sie in einen Snapshot zu nehmen":** 23d verlangt nicht, dass jede Eingabe **im** Snapshot liegt — es verlangt, dass sie **aus** dem registrierten Snapshot und dem registrierten Code **reproduzierbar** ist. Kursdaten liegen im Snapshot; Ergebnisdateien werden daraus erzeugt. Die Listen sind Ergebnisdateien der neun Backtests mit heutigen Parametern; TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren. Also:

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 23d (Eingaben reproduzierbar aus Snapshot und Code), 5a/5e, 3 („erzeugt, nicht abgetippt"), 24.3 als Bauart — die Regel steht, bevor gerechnet ist. **Kein Ergebnis:** Ich verlange die Ableitung, ohne zu wissen, ob sie 33.2 bestätigt; und ich brauche danach nur das Ob je Bot (1 oder 2), keine Trade-Zahlen (27.1 nennt „Anzahl Trades" — die Sitzung meldet die Faltenlänge, nicht die Zählung).

**Zu unserem zweiten Umstand („über `git` reproduzierbar"), zeichengleich:**

> *Zu eurem Umstand 2* („über `git` reproduzierbar"): Aus der Git-Historie reproduzierbar heisst, aus einem Datenstand, den der Lauf nicht verwendet. Das ist genau die Unterscheidung aus 23d, Frage (1): historischer Stand, kein Eingabestand.

**Zu unserem ersten Umstand (die Kippung würde am Abbild sichtbar),
zeichengleich:**

> *Zu eurem Umstand 1* (die Faltenlänge ist als Ergebnis registriert, eine Kippung würde am Abbild sichtbar — „vorausgesetzt, das Abbild ist erzeugt, und es ist es nach 33.5 nicht"): richtig, und das ist die zweite Folge dieser Antwort — **Plan-Punkt 7 (Abbild des Faltenplans, Faltenplan-Sonde) rückt vor**; es ist die Wache, die diese Klasse fängt, und sie fehlt noch. Das Abbild wird nach der Ableitung erzeugt, nicht vorher — sonst bildet es einen Stand ab, der gerade geprüft wird.

**Die Folge für 5.4, zeichengleich:**

> **Eine Folge für 5.4 selbst:** 5.4 nennt die Listen „als Quelle, ohne Hash". Nach dieser Antwort nennt eine Tatsachennotiz zu 5.4 die neuen Listen mit Hash, Snapshot und Commit; der Regeltext von 5.4 (die Schwelle) bleibt unverändert.

⚠️ **Kein Ergebnis — ausdrücklich:** Fable verlangt die Ableitung, **ohne zu
wissen**, ob sie 33.2 bestätigt, und er braucht danach nur das Ob je Bot
(Faltenlänge 1 oder 2), **keine Trade-Zahlen** (27.1). Gleich ⇒
Tatsachennotiz; verschieden ⇒ Berichtigung von 33.2 und allem, was daran hängt
— keine Wahl. Die Regel steht hier, **bevor** gerechnet ist (Bauart 24.3).

**Tatsachennotiz zu 5.4 — Fables Unsicherheit, gemessen (`a_messungen.txt`,
A4/A5).** Seine Unsicherheit, 24a, zeichengleich:

> **Unsicher:** ob 5.4 die Schwelle „mit heutigen Parametern" ausdrücklich nennt — wenn nicht, gehört der Parameterstand der Neu-Erzeugung als Tatsachennotiz zu 5.4, sonst ist die Ableitung nicht reproduzierbar.

| | gemessen |
|---|---|
| ⭐ **Die Schwelle ist registriert** | „30 Trades je Jahr" ist **Festlegung 7** (Tabelle am Registeranfang) und steht als Regel in **5.1 Nr. 6** („Faltenlänge ein Jahr, zwei Jahre bei unter 30 gefundenen Trades je Jahr."); 5.4 wertet sie aus. `faltenplan.py::faltenlaenge_jahre` liest sie als `registerdaten.ZWEIJAHRES_SCHWELLE_TRADES`, **nicht** als Literal (0 Treffer für einen Vergleich mit `30`) |
| ⚠️ **Der Parameterstand der Erzeugung ist es nicht** | 5.4 nennt die Listen als Pfad (`<bot>_alle_trades.csv`) ohne Hash und ohne Commit und sagt nur, die Trades seien **„gefunden, nicht ausgeführt"**, weil das Positionslimit ein Rasterparameter ist. Mit welchen Parametern die Listen am 13.09.2026 erzeugt wurden, steht **nirgends im Register** (`78e2bc6`: 0 Treffer; „heutige Parameter" in 5.4: 0 Treffer). 5.4 sagt auch **nicht** „mit heutigen Parametern" |
| ausserhalb des Registers | Der TB-24-Bericht sagt „mit den heutigen `live_params.py` über die heutigen Bot-Funktionen" (Stand 13.09.). Die `<bot>_meta.json` daneben tragen Kapital, Allokation, Positionslimit und Zählungen, **keine Strategieparameter**. Die neun `live_params.py` haben sich seit `78e2bc6` nur in drei Kommentarzeilen geändert, **keine Zuweisung**; der übrige Code (Bots, Simulation, Entscheidungskerze TB-38, Kostenmodul TB-90) ist hier **nicht** gemessen |

⇒ **Nach Fables eigener Bedingung gehört der Parameterstand der Neu-Erzeugung
als Tatsachennotiz zu 5.4**, sonst ist die Ableitung nicht reproduzierbar: je
Bot die Hashes der Parameterdateien, der Code-Commit, der Snapshot-Hash und der
Modus — neben dem Hash der neuen Liste. ⛔ **Der Regeltext von 5.4 bleibt
unverändert.**

⚠️ **Tatsachennotiz zu einer Voraussetzung in Fables Einwand-Antwort (TB-96
gemessen, kein Registertext geändert):** Der Satz „TB-90 hat gezeigt, dass
diese Backtests byte-identisch reproduzieren" stützt sich auf **TB-90 B6**
(`docs/ERGEBNIS_TB-90_wegA_und_kostenmodul.md`, Beleg
`docs/belege/TB-90/b6_vergleich.txt`): je Bot **ein** Backtest vor und nach dem
Kostenmodul, `cmp` 9/9 identisch — am selben Tag, auf `data/`, mit den
Backtest-Skripten der Bots. **Der Erzeuger der TB-24-Listen**
(`research/tb24_haltedauern/alle_bots.py` → `positionen_holen.py`, der
**gefundene** statt ausgeführter Trades schreibt) **war daran nicht
beteiligt**, und ein Lauf auf dem Snapshot ebenfalls nicht. ⇒ Die Regel trägt
trotzdem: Sie verlangt ihren **eigenen** Reproduzierbarkeitsnachweis — den
Modus-Lauf zweimal, bytegleich (23e) —, nicht den aus TB-90. Die Voraussetzung
ist damit **Voraussetzung der Neu-Erzeugung (TB-98)**, keine gemessene
Tatsache. *Vorgelegt, nicht berichtigt — es ist Fables Satz.*

⚠️ **Tatsachennotiz zum Erzeuger (TB-96 gemessen):** `positionen_holen.py`
schreibt **fest** nach `research/tb24_haltedauern/daten/` (Konstante
`DATEN_DIR`, `to_csv` ohne Ziel-Schalter, `os.makedirs(…, exist_ok=True)`) —
es ist **kein** Erzeuger nach 36.1 (`--ziel`, Einmal-Schreibsperre). ⛔ **Ein
unveränderter Aufruf überschriebe die alten Listen**, die nach dem Registertext
oben als historischer Stand liegen bleiben. Die Neu-Erzeugung braucht deshalb
einen Erzeuger unter 36.1 (Handwerk mit Freigabe, TB-98).

**Folge für den Plan — Plan-Punkt 7 rückt vor.** Das Abbild des Faltenplans
(33.3) und die Faltenplan-Sonde sind die Wache, die genau diese Klasse fängt
(ein Schwellenübertritt, der den Faltenplan eines Bots verschiebt), und sie
fehlen (33.5). ⚠️ **Das Abbild wird NACH der Ableitung erzeugt, nicht vorher**
— sonst bildet es einen Stand ab, der gerade geprüft wird.

**Marken am alten Ort:** bei **5.4** (Listen sind Eingabedateien, werden neu
erzeugt; Parameterstand fehlt), bei **33.2** (Faltenlänge wird neu abgeleitet
und gegen diesen Text verglichen), bei **33.5** (Abbild rückt vor, nach der
Ableitung), bei **39.6** (Eingabestand: zweiter Anwendungsfall).

> ⭐⭐ **Berichtigung und Präzisierung (41.1 A3, A12, Fable 24b, TB-108,
> 25.09.2026):** (1) Der Satz „TB-90 hat gezeigt, dass diese Backtests
> byte-identisch reproduzieren" im Zitat oben ist **berichtigt** — der
> Reproduzierbarkeitsnachweis für die Listen-Erzeugung ist der Modus-Lauf nach
> 23e und stand am 24.09. noch aus (**41.1, A3**); die Tatsachennotiz oben
> („Vorgelegt, nicht berichtigt") ist damit abgeschlossen. (2) „Der registrierte
> Code" für die Neu-Erzeugung ist der **Signalpfad**, nicht die Zuteilung; die
> neuen Listen enthalten gefundene Trades ohne `ausgefuehrt` und ohne
> Kennzeichnung im Symbolfeld, ihr Format ist eine registrierte Feldliste
> (**41.1, A12**; dazu `exit_time` und `haltedauer_balken`, 41.2 B6/B7).
> Zitate und Text oben bleiben zeichengleich.

> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Zitate, Text und die Marke oben bleiben zeichengleich.

> ⭐ **40.6 ERGÄNZT durch R42 (48.10)** (Fable 29b R42, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **40.6 ERGÄNZT durch R44 (48.12)** (Fable 29b R44, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **40.6 (Tatsachennotiz zu 5.4) PRÄZISIERT durch R47 (48.15)** (Fable 29b R47, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 40.7 ⭐ Ergänzung zu 12 — jede Mutationsprobe hat eine Gegenprobe

**Der Registertext — Fable, 24a Abschnitt 5, zeichengleich:**

> **Registertext, Ergänzung zu 12:** Jede Mutationsprobe hat eine **Gegenprobe**, die zeigt, dass sie rot werden kann (die Mutation weggelassen ⇒ die Probe scheitert). Eine Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung. Vor dem Tag wird die Gegenprobe für alle acht Mutationsproben einmal geführt und als Tatsachennotiz festgehalten.

**Seine Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* A8 (eine Wache ist, was ein anderer gegenprüfen kann) und 12. F4 ist der Beleg, dass eine Probe drei Wochen „bestehen" kann, ohne je gemessen zu haben — TB-45 in anderer Form. Kein Ergebnis.

⚠️ **Die Tatsache, die ihn ausgelöst hat:** **`F4` hat drei Wochen
„bestanden", ohne je gemessen zu haben** (40.4) — `<=`, wo der Text „unter"
sagt, bei gleichen Medianen. Und `H3` hat gezeigt, dass eine Probe auch dann
nicht beisst, wenn alle ihre Namen treffen (40.3).

⇒ **Vor dem Tag wird die Gegenprobe für alle acht Mutationsproben einmal
geführt und als Tatsachennotiz festgehalten** (40.8 (c)). Geführt ist sie
heute für **eine**: `H3` (TB-95, `ohne` leer ⇒ scheitert). ⚠️ **Welche acht
Prüfungen „die acht Mutationsproben" aus Abschnitt 12 sind, ist hier nicht
gemessen** — Abschnitt 12 nennt die Zahl, nicht die Namen; die Liste gehört in
die Tatsachennotiz von TB-97.

**Marke am alten Ort:** bei **12**, unter dem Absatz über den Schalter.

> ⭐⭐ **„alle acht" lies „alle sieben (H1–H7)" (41.1 A2, A4, Fable 24b,
> TB-108, 25.09.2026):** berichtigt durch Fable 24b B2; H0 ist der Grundlauf,
> F4 keine Mutationsprobe. Jede Probe beisst **allein** — ⚠️ H6 trägt bis heute
> nur zusammen mit H5 (TB-97) und ist vor dem Tag eigenständig zu machen oder
> als Paar zu zählen (**41.1, A4**). Der Registertext oben bleibt
> zeichengleich.

### 40.8 Beschlossen, nicht ausgeführt — was TB-97, TB-98, TB-100 und TB-101 tun

Damit das Register sagt, was offen ist und warum:

| | Sache | Auftrag |
|---|---|---|
| (a) | `F4`: `<=` → `<`, Probe mit Mehrheit wie `H3`, Gegenprobe „leere Menge ⇒ scheitert" | TB-97 |
| (b) | Die vier Literale (40.4) bauartgleich umstellen, nach Fables Regel (Zitat unten). Für 4.4: Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan | TB-97 |
| (c) | Gegenproben für **alle acht** Mutationsproben, mit Tatsachennotiz (40.7) | TB-97 |
| (d) | Sonde: **getrennte Schlusszeilen** — „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert | TB-97 |
| (e) | ⚠️ **Befund:** Die Gruppe „bestimmt" steht **fest verdrahtet** in `shared/sperrlistensonde.py` (`BESTIMMT_NICHT_EINGETRAGEN`, 39.3). Sie liest künftig **alle drei Gruppen** (Abschnitt 10, „bestimmt", `EINGEFROREN`) **aus dem Abbild**; Gegenprobe: Abbild mit erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn | TB-97 |
| ↳ (e) | ⭐ **Zweite Seite: siehe 46.1** (Fable 27a R9, TB-117, 26.09.2026); die Zeile oben bleibt zeichengleich | 46.1 |
| (f) | Neun Listen auf dem Snapshot neu erzeugen (Erzeuger unter 36.1), Sperrlistenpunkt, Tatsachennotizen; Faltenlänge nach 5.4 ableiten, gegen 33.2 vergleichen (40.6) | TB-98 |
| (g) | Abbild des Faltenplans (33.3) und Faltenplan-Sonde — **nach** (f) | TB-100 |
| (h) | `messgroessen.json` auf dem Snapshot (23d/23e), `registerdaten.py`, die zwölf Rasterachsen | TB-101 |

⚠️ **(b) vor (f):** Teil D bricht mit `KeyError`, sobald `BOT` Zweijahresfalten
bekommt — und **ob er das nach (f) bekommt, weiss vor der Ableitung niemand.**
(g) nach (f), weil das Abbild sonst einen Stand abbildet, der gerade geprüft
wird. ⚠️ **TB-99 ist kein Auftrag** — die Nummer ist für die Wächter-Sonde
reserviert (`ARBEITSWEISE` 22.2).

**Zu (b), Fable 24a Abschnitt 6, zeichengleich:**

> **Welche Registerstelle die Jahre trägt:** Wo eine Prüfung eine konkrete Registeraussage prüft (wie G6 mit 5.1 Nr. 4), liest sie die Jahre maschinell aus dieser Stelle; wo sie nur „irgendeine Selektionsfalte" braucht (Teil F, freies Beispiel; `beispieldaten.py` Z. 69/77), nimmt sie sie aus dem Plan (`faltenplan.py`), z. B. die zweite Selektionsfalte des Bots, ohne Literal. Für Teil D („2021", „2020"): Wenn 4.4 den TB-30a-Stand trägt und die Prüfung diesen Stand prüfen soll, dann bekommt 4.4 eine Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan — sie prüft die Regel, nicht das Beispiel. Eine Prüfung, die an einem Beispieljahr hängt, prüft das Beispiel.

**Zu (d) und (e), Fable 24a Abschnitt 7, zeichengleich:**

> **(i) Ausgabe trennen: ja — die Regel bleibt.** Gesamtausgang 2 bei zwölf Punkten mit Regelanteil ist korrekt (36.5/37) und am Tag mit Tatsachennotiz zulässig (22g/37.3). Aber die Tag-Vorbedingung aus 22d lautet „kein Pfad-Bestandteil 1, jede 2 mit Notiz" — und die soll man an der Ausgabe **ablesen** können, ohne zu rechnen. Also zwei Zeilen im Schluss: „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert.
>
> **(ii) Die Gruppe „bestimmt" fest verdrahtet in `sperrlistensonde.py`: ein Befund, vor dem Tag zu beheben.** 36.6 sagt: Das Abbild ist die maschinenlesbare Fassung, die Sonde prüft **gegen das Abbild** — auch die Gruppe „bestimmt" (37.2). Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache — dieselbe Klasse wie G6, nur an der Sonde selbst. Sie liest alle drei Gruppen (10, „bestimmt", `EINGEFROREN`) aus dem Abbild; das Abbild führt die Gruppe „bestimmt" heute leer (39.3). Handwerk mit Freigabe; die Sonde ist nicht gesperrt; danach Nullpunkt-Lauf und Gegenprobe (Abbild mit einem erfundenen „bestimmt"-Pfad ⇒ Sonde meldet ihn).

**Marken am alten Ort:** bei **37.2** und **36.6** (die Gruppen kommen aus dem
Abbild).

### 40.9 ⚠️ Drei Berichtigungen an den Verfahrensprüfer — angenommen

| | gemessen | Fables Annahme, zeichengleich |
|---|---|---|
| (a) | `benchmark.py` an **zwei** Punkten (4 und 6; 39.5) | „Mein „drei" war nicht gemessen" |
| (b) | `beispieldaten.py` liest **keine** Benchmark-Tabelle (39.2) | „Ich habe es als Leserin **angenommen**, weil es die Testdaten erzeugt — nicht gemessen" |
| (c) | TB-94 → TB-96 für `messgroessen.json` (39.8) | „TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8." |

**Fable, 24a Abschnitt 2, zeichengleich:**

> **(a)** `benchmark.py` an **zwei** Punkten (4 und 6), nicht drei. Mein „drei" war nicht gemessen; richtig, dass 39.5 die gemessene Zahl trägt und meinen Satz nicht zitiert. Die Sache (ein Übergang, mehrere Punkte, eine Notiz) trägt mit zwei genauso.
>
> **(b)** `beispieldaten.py` liest keine Benchmark-Tabelle. Ich habe es als Leserin **angenommen**, weil es die Testdaten erzeugt — nicht gemessen. Repo-weit drei Leser, wie TB-88 sagte. Die Bedingung „Test und Lauf lesen dieselbe Konstante" ist mit zwei Dateien erfüllt.
>
> **(c)** TB-94 → TB-96 für `messgroessen.json`. Angenommen; 39.8.
>
> Alle drei sind dieselbe Klasse wie die sechs Rücknahmen der ersten Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung genannt. Ich zähle sie mit.

⭐ **Er zählt sie mit** — dieselbe Klasse wie die sechs Rücknahmen der ersten
Woche: eine Tatsache über den Bestand behauptet statt als Voraussetzung
genannt.

⚠️⚠️ **Zu (c) — die Nummer ist wieder gerückt, und das gehört hierher, damit
die Ablage lesbar bleibt:** 39.8 hat „TB-94 → TB-96" berichtigt, und Fable hat
es angenommen. Seitdem ist **TB-96 dieser Eintrag** (Abschnitt 40), und
`messgroessen.json` ist **TB-101** (40.8 (h); `docs/auftraege/AKTUELLER_AUFTRAG.md`,
Stand 24.09.2026). Die Sache ist dieselbe, nur die Nummer nicht — *eine Nummer,
die zwei Sachen meint, ist schlimmer als eine verschobene* (39.8). ⇒ Wo 39.6,
39.8 oder 39.10 „TB-96" für `messgroessen.json` sagen, gilt **TB-101**; die
Sätze bleiben zeichengleich.

⚠️ **Ein vierter Fall derselben Klasse ist in 40.6 vorgelegt, nicht
berichtigt:** „TB-90 hat gezeigt, dass diese Backtests byte-identisch
reproduzieren" — TB-90 B6 hat die Backtest-Skripte der Bots gezeigt, nicht den
Erzeuger der Listen. Die Regel trägt davon unabhängig.

### 40.10 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert** — weder `test_vorregistrierung.py` (`F4`, die vier Literale, Gegenproben) noch `beispieldaten.py`, `shared/sperrlistensonde.py`, `faltenplan.py`, `benchmark.py` noch die Erzeuger unter `research/tb24_haltedauern/` | TB-97 / TB-98 |
| ⛔ | **Nichts gerechnet** — keine Liste neu erzeugt, keine Faltenlänge abgeleitet, der Test nicht erneut ausgeführt; in `research/vorregistrierung/ergebnisse/` nichts geschrieben | TB-98 |
| ⛔ | **Kein neues Abbild** — keine Sperrlistendatei hat sich bewegt; das gültige Abbild bleibt `sperrliste_abbild_2026-09-23.json` (`2f23f76c…`), Sonde vorher und nachher gleich (`d3_sonde.txt`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — 5.1 Nr. 4 (Wortlaut für `G6`), 5.4 (Regeltext), 12, 21.9, 33.2, 33.5, 36.6, 37.2, 39.6 und 39.8 bleiben zeichengleich; Marken und ein Nachtrag, nichts entfernt | — |
| ⛔ | **Die Listen nicht auf die Sperrliste genommen** — das geschieht mit den neu erzeugten Listen (40.6), nicht mit den alten | TB-98 |
| ⭐ | **N = 653 (Festlegung 10) unberührt**; Festlegung 7 (Schwelle 30) unberührt | — |
| ⚠️ | **Offen:** 40.8 (a)–(h) · der Parameterstand der Neu-Erzeugung als Tatsachennotiz zu 5.4 (40.6) · die Liste der acht Mutationsproben (40.7) · die Voraussetzung „TB-90 hat gezeigt" (40.6, bei Fable) · der Registertext „Eingabestand" (23d) selbst ist weiter **nicht** eingetragen (39.6) | TB-97 / TB-98 / TB-101 / Fable |

*Dieser Abschnitt ist rein additiv: Er trägt zwei Registertexte des
Verfahrensprüfers zeichengleich ein, hält eine Kopplung zwischen Registertext
und Test fest, die bisher niemand sah, beschliesst die nächsten vier Aufträge
mit ihrer Reihenfolge, setzt Marken an zehn Stellen — und entfernt nichts.
Gebaut und gerechnet wird nichts.*

## 41. Nachweis mit zwei Teilen, Resolver ohne Rückfall, Deckel statt Purge, Mutationsproben einzeln — die Einträge aus Fable 24b, 24c, 24d (TB-108, 25.09.2026)

### 41.0 Was dieser Abschnitt ist

⭐ **Reines Eintragen von Registertext und Tatsachen**, wie 34 bis 40. Der
Verfahrensprüfer hat vom 24.09.2026 an in sechs Antworten (24b, 24c, 24d, 25a,
25b, 25c) Registertexte, Berichtigungen, Präzisierungen und Tatsachennotizen
benannt. **Der Code ist mit TB-103 bis TB-107 danach gebaut; das Register stand
bis zu diesem Eintrag auf dem Stand von Abschnitt 40 (`d0dc890`, 24.09.2026).**
Dieser Abstand war benannt, nicht still — Fable 23f Abschnitt 3, zeichengleich:
„Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag."
Mit 41 und 42 ist er geschlossen, soweit Fable entschieden hat.

**Gliederung:** 41 nimmt die Einträge aus **24b, 24c und 24d** auf (41.1–41.3),
42 die aus **25a, 25b und 25c** samt den Tatsachennotizen aus TB-103 bis TB-107.
⚠️ **Diese Grenze hat der steuernde Chat vorgeschlagen und der Betreiber am
25.09.2026, 22:34 gewählt (Auswahlkarte, `docs/auftraege/MAC_TB-108_register_41_42.md`).
Fable hat sie nicht entschieden** — er spricht nur von „Register 41/42". Er kann
ihr widersprechen; eine andere Grenze wäre eine Umnummerierung mit Vermerk, keine
Änderung der Einträge.

**Bauart je Eintrag:** Kennung aus der Arbeitsliste
(`docs/projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md`, A1–A12, B1–B8, C1–C9;
in 42 D1–D12, E1–E8, F1–F8, G1–G10) · Fables Text **eingesetzt, nicht
abgetippt** (Blockzitat; Teilzitate in „…"), mit Quelle · Art · Stand, gemessen
in TB-108 (`docs/belege/TB-108/a3_stand.txt`, `c_hashuebergaenge.txt`), ohne
Ergebnisgrössen (27.1) · wo die Fassung später berichtigt wurde. **Beide
Fassungen stehen**, die frühere mit „⭐ BERICHTIGT durch …", die spätere mit
„berichtigt …". Je Zitat ein `diff` gegen die Quelle mit rc 0
(`docs/belege/TB-108/d2_zitate.txt`).

⚠️ **Tatsachennotiz zur Herkunft der Quellen:** Die sechs Antwortdateien
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-24b_…`, `…24c_…`, `…24d_…`,
`…25a_…`, `…25b_…` und `…25c_…` hat der steuernde Chat aus der Projektablage
**abgeschrieben**, nicht byteweise übertragen — das Werkzeug liefert dort nur
Text (`docs/projektfuehrung/UEBERGABE_2026-09-25.md`, Block 8). **Die Zitate
hier sind zeichengleich mit der Datei im Repo; ob diese zeichengleich mit Fables
Ablage ist, ist nicht gemessen.**

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag, der einen alten Satz
berichtigt, präzisiert oder ergänzt, steht zusätzlich als **Marke** beim alten
Satz; die Liste der Marken steht in 42.7. Die alten Sätze bleiben zeichengleich;
`git diff --numstat` auf dieses Register zeigt für TB-108 in der zweiten Spalte
`0`. ⛔ **In Abschnitt 10 steht keine Marke** — die Sperrlisten-Sonde vergleicht
dessen Listentext mit dem Abbild (36.6, Prüfung (ii)); was dorthin gehörte,
steht in 42 mit Verweis auf den Punkt.

### 41.1 Aus Fable 24b (`FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md`)

Fables Liste für dieses Register, 24b Abschnitt D Punkt 5, zeichengleich:

> 5. **Register 41:** Berichtigung 12 (sieben, Namen, F4), 40.7 („sieben"), 40.6 (TB-90-Satz), Regel „allein beissen" und H6, Störproben-Satz, Marke 5.1 Nr. 4, Testrahmen-Notiz, Tatsachennotiz `bot_lauf.py`/`symbol`, Regel „keine Kennzeichnung in Laufcode-Feldern".

**A1 — Berichtigung zu 12: sieben Mutationsproben, mit Namen** · Art:
Berichtigung · Quelle: 24b Abschnitt B2

> **Berichtigung zu 12 (Ersatztext für den Halbsatz „davon acht Mutationsproben"):** … davon **sieben Mutationsproben, H1 bis H7** (Teil H); H0 ist der Grundlauf ohne Mutation und keine Probe. F4 ist keine Mutationsprobe (ändert keinen Code), hat aber nach 40.7 eine Gegenprobe. Die Zahl der Prüfungen ist eine Tatsachennotiz mit Stand (heute 188, Commit …), kein Registertext; die **Namen** der Mutationsproben sind Registertext. Ändert sich die Menge, ist das eine Berichtigung mit Namen.

*Seine Quelle des Grundes, zeichengleich:* „23a (Kopien altern; eine Zahl ohne Namen ist eine Kopie des Codes im Register). Kein Ergebnis."

**Stand, gemessen:** Der Test zählt heute **196** Prüfungen
(`research/vorregistrierung/test_vorregistrierung.py`, `db50e187…`, letzter
Commit `abeca36`, TB-106; 196/196 in TB-107, `docs/belege/TB-107/g4_tests.txt`).
Die Namen H1 bis H7 stehen im Test (Teil H). ⚠️ Zu H6 siehe A4.

**A2 — Berichtigung zu 40.7: „alle acht" lies „alle sieben"** · Art:
Berichtigung · Quelle: 24b Abschnitt B2

> **Berichtigung zu 40.7:** „alle acht" lies „alle sieben (H1–H7)".

**Stand, gemessen:** Die Gegenproben aller Mutationsproben hat TB-97 geführt
(`docs/ERGEBNIS_TB-97_testannahmen_zweite_runde.md`). ⚠️ „sieben" setzt voraus,
dass H6 eigenständig beisst — siehe A4.

**A3 — Berichtigung zu 40.6: der TB-90-Satz** · Art: Berichtigung · Quelle: 24b
Abschnitt C1

> **Berichtigung zu 40.6:** „TB-90 hat gezeigt, dass diese Backtests byte-identisch reproduzieren" lies „Der Reproduzierbarkeitsnachweis für die Listen-Erzeugung ist der Modus-Lauf nach 23e (zweimal, bytegleich) und stand am 24.09. noch aus; TB-90 B6 betraf die Backtest-Skripte auf `data/`, nicht den Listen-Erzeuger."

Fable nennt es seinen vierten Fall derselben Klasse (24b C1). Die Berichtigung
betrifft den in 40.6 zeichengleich zitierten Satz aus 24a; er bleibt dort
stehen, die Marke steht in 40.6.

**A4 — Regel: jede Mutationsprobe beisst allein; H6** · Art: Registertext
(Ergänzung zu 12/40.7) · Quelle: 24b Abschnitt B3

> **Regel (Ergänzung zu 12/40.7):** Jede Mutationsprobe beisst **allein**: Ihre Gegenprobe (nur ihre eigene Mutation weggelassen, alles andere im Grundzustand) scheitert. Eine Probe, die das nur im Verbund mit einer anderen leistet, wird vor dem Tag **eigenständig** gemacht — H6 braucht einen eigenen eingesetzten Fehler, den die entfernte Wache hätte fangen müssen, statt sich H5s Fehler zu leihen. Ist das strukturell nicht möglich, wird das Paar als **eine** Probe mit zwei Mutationen registriert und gezählt — sechs plus ein Paar, nicht sieben.

*Sein Grund, zeichengleich:* „A8 und 12. Eine Zählung, die ein Paar als zwei führt, ist dieselbe Unwahrheit wie „acht", nur kleiner. Kein Ergebnis."

**Stand, gemessen:** ⚠️⚠️ **H6 ist bis heute nicht eigenständig.** TB-97 hat
gemessen: Sind die Mutationen von H5 **und** H6 weggelassen, besteht H6 — „H6
trägt nur zusammen mit H5" (`docs/ERGEBNIS_TB-97_testannahmen_zweite_runde.md`,
Zusatz zu H6); der Test sagt es selbst (Kommentar „Die Mutation von H5 ist
Voraussetzung von H6", Stand `db50e187…`). Seitdem ist H6 nicht umgebaut (letzte
Änderung an H6: `ae8db0b`, TB-97). Die Regel ist seit TB-103 auf **neue**
Proben angewandt worden (Ergebnisse TB-104 bis TB-107: „beisst allein"; TB-103
nach Fable 25a Abschnitt 2).
⇒ **Vor dem Tag offen:** H6 bekommt einen eigenen eingesetzten Fehler, oder
H5/H6 werden als **eine** Probe mit zwei Mutationen geführt und gezählt — dann
gilt „sechs plus ein Paar", und „sieben" in A1/A2 ist nach Fables eigener Regel
zu berichtigen (42.6).

**A5 — Störproben in beide Richtungen** · Art: Registertext (Ergänzung zu 12) ·
Quelle: 24b Abschnitt C2

> **Registertext, Ergänzung zu 12 (Gegenproben) — Störproben:** Eine Störprobe nach „geht es ein?" wird in **beide** Richtungen geführt: klein genug, dass nichts passieren darf, und gross genug, dass etwas passieren muss. Eine Störprobe nur in eine Richtung belegt nichts. *(Formuliert von TB-95 am 23.09.2026, übernommen als Registertext durch den Verfahrensprüfer, 24.09.2026.)*

*Sein Grund, zeichengleich:* „die Störprobe zur Faltenlänge — eine Zeile weg hätte allein das falsche „nein" ergeben; F4 ist derselbe Fehler in einer Prüfung. Kein Ergebnis."

Die Tatsache, aus der der Satz stammt, steht im Nachtrag zu 39.8 (TB-95,
„Der methodische Satz, der über den Fall hinausgeht").

**A6 — Marke an 5.1 Nr. 4: zwei Leser, ein Parser** · Art: Marke · Quelle: 24b
Abschnitt B4

> **Marke bei 5.1 Nr. 4:** ja, um den zweiten Leser ergänzen. Und: zwei Leser, **ein Parser** — die Funktion, die 5.1 Nr. 4 liest, ist eine, und beide rufen sie; sonst altern zwei Parser getrennt. Handwerk, aber die Anforderung ist Verfahren (ein Wert, ein Ort).

**Stand, gemessen:** Seit TB-97 steht der Parser **einmal**, in
`research/vorregistrierung/beispieldaten.py::jahre_aus_register_5_1_nr_4`
(Muster `^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*`,
genau ein Treffer, sonst `None`). Ihn rufen `test_vorregistrierung.py`
(`_testjahre_aus_register`, `G6`) und `beispieldaten.krisenfalten` — zwei Leser,
ein Parser. Die Marke steht bei 5.1 Nr. 4, unter der Marke aus 40.2.

**A7 — Testrahmen-Notiz** · Art: Tatsachennotiz (zu 12) · Quelle: 24b Abschnitt
C4

> Es ist keine Prüfung, sondern der Testrahmen (12: „erzeugte Beispieldaten mit frei erfundenen Werten"). Literale dort sind kein Prüffehler, aber ein **Befund am Testrahmen**: Ein Rahmen, der bei Doppeljahren entartet (Z. 77) oder nie trifft (Z. 69), prüft den Auswerter nur für Bots mit Einjahresfalten — und `elliott_wave` hat Doppeljahre. Eigene Tatsachennotiz (zu 12): der Testrahmen deckt seit 24c beide Faltenlängen ab; vorher nicht. Die Umstellung selbst ist nach 24c geschehen (5.1 Nr. 4 über Abdeckung) und angenommen.

Die Stoffsammlung führt diesen Eintrag nur als Stichwort (24b D5
„Testrahmen-Notiz"); der Text steht in derselben Antwort, Abschnitt C4.

**A8 — `bot_lauf.py` und `symbol`** · Art: Tatsachennotiz · Quelle: 24b
Abschnitt A3

> *Eine Regel aus dem Nebenbefund:* Seit TB-26 ist `symbol` kein reines Etikett mehr; der Kopf von `bot_lauf.py` sagt das Gegenteil. Tatsachennotiz — und: **Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.** Ein Etikett, das in einen Zufallsschlüssel fliesst, ist kein Etikett.

**Stand, gemessen:** Der Kopf von `research/exposure_messung/bot_lauf.py` sagt
weiter, `simulate_portfolio()` benutze `symbol` „ausschliesslich als
Beschriftung der Ausgabezeile" (Z. 32–37; letzter Commit `d48a195`, TB-105,
dort nur die Ordneranlage geändert). Nach TB-98 Befund 2 liest der
Zufallsschlüssel der Zuteilung seit TB-26 das Symbol — der Satz im Kopf ist
damit falsch; **Tatsachennotiz, der Kopf ist nicht geändert.**

**A9 — Regel: keine Kennzeichnung in Laufcode-Feldern** · Art: Registertext ·
Quelle: 24b Abschnitt A3, derselbe Absatz wie A8

„**Kein Messwerkzeug schreibt Kennzeichnungen in Felder, die der Laufcode liest.** Ein Etikett, das in einen Zufallsschlüssel fliesst, ist kein Etikett."

**A10 — kein Fallback unter dem Modus** · Art: Registertext, Ersteintrag (zu
5a/5e) · Quelle: 24b Abschnitt A2

> **Registertext, Ersteintrag (zu 5a/5e, Selektionsmodus) — kein Fallback unter dem Modus:** Unter dem Selektionsmodus gibt es **keinen Rückfall auf eingebaute Voreinstellungen**, gleich welcher Art (Symbollisten, Parameter, Pfade, Schwellen). Eine Eingabe, die im Snapshot nicht gefunden wird, ist Rückgabewert **2** (nicht prüfbar) und beendet den Lauf, bevor gerechnet wird — nach demselben Muster, mit dem `paths.py` den Live-Pfad unter dem Modus unerreichbar macht (`SystemExit`, nicht Exception). Eine Meldung „Keines ausgelassen" darf nur stehen, wenn die geladene Symbolmenge gleich der Universumsdatei aus dem Snapshot ist; das Ladeprotokoll (3b (d)) nennt beide Zahlen und die Quelle der Liste.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 22e/17.x — der Modus ist gebaut, „damit kein `except Exception` im Aufrufer den Abbruch in einen stillen Weiterlauf verwandelt"; ein Fallback ist genau dieser stille Weiterlauf, nur eingebaut statt gefangen. A8. Kein Ergebnis.

**Stand, gemessen:** umgesetzt im Resolver (`shared/paths.py`, TB-103,
`d87997e`: `CONFIG_DIR = <snapshot>/config`, Prüfung gegen das MANIFEST,
`SystemExit(2)`), für die vier Rückfälle aus 25a (42.1, D12) in TB-105, TB-106
und TB-107. ⚠️ **Nicht umgesetzt ist der letzte Satz** („Das Ladeprotokoll …
nennt beide Zahlen und die Quelle der Liste"): `shared/ladeprotokoll.py` ist
seit `55b991d` (TB-45, 17.09.2026) unverändert und nennt weder die Zeilenzahl
der Universumsdatei noch die Quelle der Liste — derselbe offene Teil wie 25a
(B) (4) (42.1, D3/D9).

> ⭐ **`fehlend` im Modus: siehe 46.2** (Fable 27a R10, TB-117, 26.09.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**A11 — Tag-Vorbedingung: Trockenlauf aller neun im Modus** · Art: Registertext
(Ergänzung zum Plan) · Quelle: 24b Abschnitt A2

> **Tag-Vorbedingung, Ergänzung zum Plan:** Vor dem Tag läuft für **alle neun Bots** ein Trockenlauf im Selektionsmodus gegen den echten Snapshot, mit Lesehaken und Aufrufstapel: 0 Zugriffe ausserhalb `snapshots/<hash>/`; geladene Symbolmenge gleich Universumsdatei; kein Fallback; Rückgabe 0. Das Protokoll ist Tatsachennotiz. Ein Modus, unter dem noch nie ein Bot gelaufen ist, ist keine registrierte Umgebung, sondern eine behauptete.

⭐ **PRÄZISIERT durch 42.1** (D2: „0 Zugriffe" nach drei Klassen; D3: Liste und
Menge; D4: Wiederholung am Tag-Commit) und **42.2** (E6: Stichtag).

**Stand, gemessen:** gelaufen in TB-103 (`836865f`), TB-105 (F1, auch im
frischen Klon), TB-106 (G5) und TB-107 (G3), je 9 × rc 0. Nach 42.1 (D4) ist
keiner davon die Tag-Vorbedingung selbst — sie wird am Tag-Commit wiederholt.

**A12 — Präzisierung zu 40.6: die neuen Listen kommen vom Signalpfad** · Art:
Registertext (Präzisierung zu 40.6) · Quelle: 24b Abschnitt A3

> **Entscheidung (Präzisierung zu 40.6):** „Der registrierte Code" für die Neu-Erzeugung der Listen ist der **Signalpfad** (die neun Backtests mit registrierten heutigen Parametern, `run_backtest`), nicht der Ausführungspfad (Zuteilung). Die neuen Listen enthalten die **gefundenen** Trades mit den Feldern, die 5.4 braucht (`bot`, `symbol`, `entry_time`, dazu die Felder, die der Signalpfad ohnehin liefert), **ohne** Simulationsspalte `ausgefuehrt` und **ohne** Kennzeichnung im Symbolfeld. Das Format wird als Feldliste registriert (Bauart 33.3), der Erzeuger schreibt genau diese Felder. Vergleichbarkeit mit den historischen Listen (`78e2bc6`) ist **nicht** gefordert — die sind historischer Stand mit Notiz; verglichen wird die abgeleitete **Faltenlänge** gegen 33.2, nicht Liste gegen Liste.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5.4 (Schwelle auf gefundene Trades je Jahr) und 33.2; der Grund für ein Feld in einer Eingabedatei ist, dass die Herleitung es liest — 33.3-Logik. Kein Ergebnis. **Folge:** Der Erzeuger braucht die Zuordnung ausgeführt/gefunden nicht mehr, die Kennung entfällt, der Konflikt mit Punkt 10 entsteht gar nicht; keine Änderung an der Zuteilung, keine Suche nach einer durchgereichten Spalte.

⭐ **ERGÄNZT durch 41.2 (B3, B6/B7):** Die Feldliste bekommt `exit_time` und
`haltedauer_balken` (24c Abschnitt 4).

**Stand, gemessen:** Der Erzeuger auf dem Signalpfad ist **nicht gebaut**
(Plan-Punkt 3); die neun Listen sind nicht neu erzeugt.

> ⭐ **Abnahmebedingungen des Erzeugers: siehe 45.5** (Fable 26a R5, TB-114,
> 26.09.2026). Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Eintrag, Stand und die Marke oben bleiben zeichengleich.

### 41.2 Aus Fable 24c (`FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md`)

Fables Liste für dieses Register, 24c Abschnitt 6 Punkt 4, zeichengleich:

> 4. **Register 41/42:** Reichweite 5.4, Berichtigung 2d-Herleitung, Donchian-Herleitung, Nachweis mit zwei Teilen, Resolver-Pflicht, Tatsachennotizen (`haltedauern_je_bot.csv` historisch, `tb24_haltedauern/auswertung.py` historisch, TB-93/102-Nachweis = 2).

**B4 — Der Nachweis hat zwei Teile** · Art: Registertext (Ersatz für den
Nachweisbegriff aus 23e) · Quelle: 24c Abschnitt 1

> **Registertext, Ersatz für den Nachweisbegriff aus 23e (Eingabestand):** Ein Reproduzierbarkeitsnachweis besteht aus **zwei** Teilen, und beide sind Pflicht: **(a)** dem Ergebnisvergleich — die erzeugte Datei ist bytegleich zur eingefrorenen; **(b)** dem **Leseprotokoll** — alle Lesezugriffe des Laufs auf Kurs-, Universums- und Ergebnisdateien liegen innerhalb `snapshots/<hash>/` oder auf registrierten Eingabedateien, **null** im Repo-Arbeitsstand (`data/`, `config/`, `ergebnisse/` ausserhalb der registrierten Pfade). Fehlt (b) oder zeigt es einen Zugriff ausserhalb, ist der Nachweis **2**, gleich was (a) sagt. „Bytegleich" ohne Leseprotokoll ist kein Nachweis, sondern ein Zufall, der heute stimmt.

*Seine Quelle des Grundes, zeichengleich:* „5e (der Lauf belegt, woraus er nachweislich gelesen hat) und TB-98 Befund 1 / TB-102 Lesart 2: richtiges Ergebnis, falscher Ort, keine Warnzeile. Kein Ergebnis."

⭐ **PRÄZISIERT durch 42.1 (D6):** Was „ausserhalb" heisst, regeln die drei
Klassen von Zugriffen (ergänzt durch 42.2 E1, E2 und 42.3 F7, F8).

**Stand, gemessen:** angewandt seit TB-103 — jeder Modus-Lauf der Aufträge
TB-103 bis TB-107 hat einen Lesehaken mitgeführt. ⚠️ **Der Nachweis der
Benchmark-Tabelle bleibt 2**: Der Modus-Lauf liest zwei Eingaben ausserhalb des
Snapshots (die neun TB-24-Listen und `ergebnisse/messgroessen.json`; zuletzt
gemessen TB-104 C5). Ebenso der Nachweis für `messgroessen.json`
(`haltedauern_je_bot.csv` aus dem Repo, TB-103).

**B8 — der TB-93/TB-102-Nachweis ist 2** · Art: Tatsachennotiz · Quelle: 24c
Abschnitt 1, Absatz „Für alle bisherigen Nachweise"

> *Für alle bisherigen Nachweise heisst das:* TB-91 A1b (`benchmark.py` im Modus, zweimal bytegleich) — hatte es ein Leseprotokoll? TB-95 hat später mit Lesehaken gemessen, dass `benchmark.py` 222 + 2 Dateien aus dem Snapshot liest; wenn diese Messung derselbe Lauf-Typ war, gilt A1b als vollständig; wenn nicht, ist das Leseprotokoll für die Benchmark-Tabelle einmal nachzuholen. **Nur das Ob.** Der TB-93/TB-102-Nachweis für `messgroessen.json` ist nach dieser Regel **2** — nicht geführt.

⭐ **BERICHTIGT durch 41.3 (C8):** „TB-91 A1b" lies „TB-92 A1b". Die Frage
„hatte es ein Leseprotokoll?" ist beantwortet in 41.3 (C9) und 42.1 (D10): ja,
seit TB-92.

**B5 — Resolver-Pflicht** · Art: Registertext (Ergänzung zu 5a/5e) · Quelle:
24c Abschnitt 2

> **Registertext, Ergänzung zu 5a/5e:** Jedes Modul des Laufbereichs, das Kursdaten oder Universumsdateien liest, bezieht seine Pfade über den Resolver (`shared/paths.py`, `get_strategy_paths()`). Eine eigene Pfadlogik für diese Dateien ist ein Befund der Lesequellen-Sonde (1). Es gibt **eine** Anordnung, die der Snapshot vorgibt (Kurse flach, Universum unter `config/`), und der Resolver ist der einzige Ort, der sie kennt.

*Seine Quelle des Grundes, zeichengleich:* „`strategy_paths.py` selbst („Hier steht KEIN zweiter Resolver") und 24b A2. Drei Anordnungen sind zwei zu viel; und ein Programm, das den Modus nicht kennt, kann ihn nicht einhalten. Kein Ergebnis."

⭐ **BERICHTIGT durch 42.1 (D1):** Die Fundstelle „(`shared/paths.py`,
`get_strategy_paths()`)" lies „über den Resolver (`shared/paths.py`, direkt oder
über `strategy_paths.get_strategy_paths()`)" — Fables achter Fall. ⭐
**ERGÄNZT durch 41.3 (C6):** Ein Modus-Lauf ist ein Lauf unter dem Resolver;
Hilfsordner tragen keinen Nachweisteil (b).

**Stand, gemessen:** Die Leser des Laufbereichs holen ihre Kurs- und
Universumspfade über `shared/paths.py`: `messgroessen.py` (TB-103, `ae136fd`),
`benchmark.py`, `faltenplan_neun.py`, `loaderlauf.py`,
`universum_trockenlauf.py` (TB-104, `572d725`); Ersatzwurzeln brechen unter dem
Modus mit 2 ab, bevor gelesen wird.

**B1 — Reichweite des Grundsatzes aus 5.4** · Art: Registertext, Ersteintrag ·
Quelle: 24c Abschnitt 4

> **Registertext, Ersteintrag — Reichweite des Grundsatzes aus 5.4:** Keine Festlegung des Verfahrens, die vor dem Lauf steht (Faltenlänge, Purge, Embargo, Trainingsende, Rastergrenzen), wird aus Grössen hergeleitet, die vom **Positionslimit** oder von der **Ausführung** abhängen. Herleitungen aus Trades verwenden **gefundene** Trades (Signalpfad), nie ausgeführte. Der Grundsatz gilt für alle Stellen, an denen 5.4 ihn heute allein anwendet.

*Seine Quelle des Grundes, zeichengleich (für B1, B2, B3 und B6/B7 gemeinsam):*

> *Quelle des Grundes:* 5.4 im Wortlaut („keine Festlegung vor dem Lauf, die vom Positionslimit abhinge"), 2d im Zweck (kein Leck zwischen Falten), 3 („erzeugt, nicht abgetippt"). **Kein Ergebnis — und hier gilt es besonders:** Ich weiss nicht, ob `purge_tage` länger, die Donchian-Untergrenze anders, `messgroessen.json` wie stark verändert herauskommt. Ihr habt es nicht gerechnet, ich habe es nicht gefragt. Die Regel ist dieselbe, wie auch immer es ausgeht, und deshalb steht sie jetzt — bevor der Erzeuger läuft (24.3). Wer nach der Messung sagt „das verändert den Raster zu sehr", wählt nach Wirkung; wer vorher sagt „lassen wir es, es ist ja nicht zirkulär im Lauf", wählt auch — für die Zellen mit kurzen Haltedauern.

**Stand, gemessen:** 5.4 sagt „gefundene" im Wortlaut („Gerechnet aus den
**gefundenen** Trades je vollem Kalenderjahr" und „Gefunden, nicht ausgeführt");
Fables Unsicherheit aus 24b ist damit ausgeräumt (24c Abschnitt 0). Die
Marke steht bei 5.4. ⭐ **Tatsachennotiz zu `elliott_wave`:** 41.3 (C4).

**B2 — Berichtigung der 2d-Herleitung (Purge als Schranke über das Raster)** ·
Art: Berichtigung — ⭐⭐ **ZURÜCKGENOMMEN durch 41.3 (C1), der Deckel neu
gefasst durch 41.3 (C2)** · Quelle: 24c Abschnitt 4

> **Berichtigung zu 2d (Purge/Embargo), Herleitung:** `purge_tage` wird nicht aus der maximalen Haltedauer eines Parameterstands hergeleitet, sondern als **Schranke über das registrierte Raster**: die grösste Haltedauer, die ein Trade in irgendeiner Zelle des Rasters erreichen kann — aus den registrierten Rastergrenzen der Ausstiegsachsen (Zeitausstieg, maximale Haltedauer), wo eine Strategie keinen begrenzten Ausstiegshorizont hat, aus dem Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag als Tatsachennotiz. Ein Purge, das für eine Zelle des Rasters zu kurz ist, ist ein Befund.

⛔ **Dieser Text gilt nicht.** Er steht hier, weil Fable ihn in 24c als
Registertext benannt und in 24d ausdrücklich zurückgenommen hat — mit dem Grund
„damit die Ablage nicht zwei Fassungen führt" (41.3, C1).
Eingetragen wurde er nie; 2d/16.6 bleiben, wie sie sind, mit den Präzisierungen
aus 41.3 (C2, C3).

**B3 — Donchian-Untergrenze aus gefundenen Trades** · Art: Registertext
(Berichtigung zur Herleitung) · Quelle: 24c Abschnitt 4

> **Berichtigung zur Herleitung der Donchian-Untergrenze (zwei Bots):** aus `median_balken` der **gefundenen** Trades, nicht der ausgeführten. Die Rastergrenze selbst bleibt eine gemessene Grösse (Abschnitt 2/3, „erzeugt, nicht abgetippt") — nur ihre Eingabe wechselt auf den Signalpfad.

Fable bestätigt in 24d: „**Donchian-Untergrenze (zwei Bots):** bleibt wie in 24c — `median_balken` der gefundenen Trades."

**Stand, gemessen:** offen — die Eingabe (neue Listen gefundener Trades) gibt es
noch nicht (Plan-Punkt 3). `mess["haltedauer"]` liest heute
`registerdaten.py:231` (`median_balken`, TB-104 A3).

**B6/B7 — `haltedauern_je_bot.csv` und ihr Erzeuger werden historischer Stand**
· Art: Tatsachennotiz · Quelle: 24c Abschnitt 4, „Folge für die Eingabedateien"

> **Folge für die Eingabedateien:** Die Haltedauern werden aus **denselben neuen Listen gefundener Trades** abgeleitet, die 24b A3 für die Faltenlänge anordnet — jede gefundene Trade-Zeile trägt `entry_time` und `exit_time`, die Haltedauer folgt daraus. **Ein Erzeuger, eine Eingabedatei je Bot, zwei Herleitungen** (Faltenlänge nach 5.4, Haltedauern für 2d und die Rastergrenze). `haltedauern_je_bot.csv` in heutiger Form und ihr Erzeuger `tb24_haltedauern/auswertung.py` werden historischer Stand mit Tatsachennotiz; `messgroessen.py` liest die Haltedauern aus der neuen Quelle (Konstante, unter dem Resolver). Die Feldliste der neuen Listen (24b A3) bekommt `exit_time` und `haltedauer_balken` ausdrücklich.

**Stand, gemessen:** `research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv`
und `research/tb24_haltedauern/auswertung.py` sind unverändert; `messgroessen.py`
liest die Datei weiter (der eine Zugriff ausserhalb des Snapshots, TB-103). Die
Umstellung auf die neue Quelle hängt am Erzeuger (Plan-Punkt 3).

> ⭐ **41.2 B6/B7 ERGÄNZT durch R41 (48.9)** (Fable 29b R41, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 41.3 Aus Fable 24d (`FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md`)

Fables Liste für dieses Register, 24d Abschnitt 4, zeichengleich (Kopf):

> **Register 41/42, zusätzlich zu 24c Abschnitt 6 Punkt 4:**

**C1 (a) — Rücknahme „`purge_tage` als Schranke über das Raster"** · Art:
Rücknahme, **mit Grund** · Quelle: 24d Abschnitt 1 · berichtigt 41.2 (B2)

> **Rücknahme (zu 24c, „Berichtigung zu 2d (Purge/Embargo), Herleitung"):** Der Satz *„`purge_tage` wird … als Schranke über das registrierte Raster bemessen"* ist zurückgenommen. Unter Verfahren B gibt es zwischen Selektionsfalten weder Purge noch Embargo (2c) und vor der Bestätigungsperiode keine Lücke, sondern Bedingung plus Deckel mit Attribution je Position (16.6). Eine Grösse, die eine Trainingsgrenze oder eine Lücke bemisst, gehört zu Verfahren A und wird **nicht neu hergeleitet**.

*Seine Quelle des Grundes, zeichengleich:* „2c und 16.6 im Wortlaut. Kein Ergebnis."

**Der Grund, warum die Rücknahme hier steht** — Fables Art-Spalte zu (a),
zeichengleich: „Rücknahme eines noch nicht eingetragenen Textes — mit Grund eintragen, damit die Ablage nicht zwei Fassungen führt".
Dazu nimmt er eine Zeile aus 24c Abschnitt 5 zurück: „Meine Zeile in 24c Abschnitt 5 („G8 prüft künftig das aus dem Raster geschrankte `purge_tage`") ist damit zurückgenommen."

**C2 (b) — Deckel für Bots ohne Zeitbremse aus gefundenen Trades** · Art:
Registertext (Präzisierung zu 2d, Fassung 16.6) · Quelle: 24d Abschnitt 1 ·
berichtigt 41.2 (B2)

> **Präzisierung zu 2d (Fassung 16.6), Deckel für Bots ohne Zeitbremse:** Das 95. Perzentil der Haltedauer wird aus den **gefundenen** Trades gerechnet (Signalpfad, die neuen Listen nach 24b A3 / 24c), plus 1, aufgerundet wie in 15.4 Anmerkung 4; Tatsachennotiz mit Hash der Liste, Snapshot-Hash und Commit. Der Deckel ist keine Leckschranke — das Leck schliesst die Attribution je Position —, und er ist deshalb ausdrücklich **nicht** als Maximum über alle Rasterzellen zu bemessen. Der Zusatz aus 24c *„Maximum der gefundenen Trades über den gesamten Datenhorizont, mit Aufschlag"* ist zurückgenommen.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 24c, Registertext „Reichweite des Grundsatzes aus 5.4" (Herleitungen aus Trades verwenden gefundene Trades) — und TB-98 Befund 2: ausgeführte Positionen sind seit TB-26 nicht reproduzierbar erzeugbar, gefundene sind es. Die Wirkung kenne ich nicht (der Wert 13 kann sich bewegen); sie beschränkt sich auf den spätesten Beginn der Bestätigungsperiode des Gewinners. Kein Ergebnis.

**Stand, gemessen:** nicht gerechnet — der Deckel von `t3_supertrend` steht in
15.4 und 16.6 weiter mit dem Wert aus **ausgeführten** Positionen
(`research/tb24_haltedauern/daten/t3_supertrend_positionen.csv`, TB-24). Neu zu rechnen, wenn
die neuen Listen gefundener Trades vorliegen (Plan-Punkt 5, 24d Abschnitt 4).
Marken bei 15.4 und 16.6.

**C3 (c) — die Bedingung wird für den Gewinner auf dessen Positionen
ausgewertet** · Art: Registertext (Präzisierung zu 2d, Fassung 16.6) · Quelle:
24d Abschnitt 1

> **Präzisierung zu 2d (Fassung 16.6), Auswertungsebene:** Die Bedingung wird im Selektionslauf **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet; der Deckel ist je Bot eine Konstante über alle Zellen. Das Journal des Papierpfads ist dafür keine Quelle. *(Ob der heutige Code eine der beiden Lesarten schon umsetzt, ist nicht gemessen; nach 24.5 existiert der Laufcode, der die Tagesreihe je Zelle erzeugt, nicht.)*

*Seine Quelle des Grundes, zeichengleich:* „5.1 Nr. 7 und 15.1 (Verfahren B: Out-of-Sample ist allein die Bestätigungsperiode — des gewählten Satzes). Kein Ergebnis."

**Kategorie:** Fable hatte gefragt, ob es eine Berichtigung sei (24d,
Unsicher (4)). Nach der Messung, dass der Wortlaut von 16.6 beide Lesarten
trägt, 25a Abschnitt 1 (4), zeichengleich: „Nach eurer Messung ist Eintrag c eine **Präzisierung**, und F17 ist so oder so erfüllt; die Kategorie ist Handwerk (30.6). Sie bleibt Präzisierung."

**C4 (d) — 5.4 bei `elliott_wave`: „gefundene" greift über die Ausführung** ·
Art: Tatsachennotiz (zu 5.4) · Quelle: 24d Abschnitt 2

> **Zum Nebenbefund `elliott_wave`:** richtig — bei ihm ist das Positionslimit keine Achse (2.4: keine Limitachse, Kapitalschranke `floor(1/ALLOCATION_PCT) = 10`). Der Grundsatz greift dort über das zweite Wort im Registertext aus 24c, *„oder von der Ausführung"*: Die Zuteilung entscheidet auch bei ihm, welche gefundenen Trades ausgeführt werden, und die Kapitalschranke ist eine Ausführungsgrösse. Der Registertext braucht keine Ergänzung; die Tatsachennotiz zu 5.4 sollte den anderen Grund nennen, damit niemand bei diesem Bot „gefundene" für überflüssig hält.

⇒ **Tatsachennotiz zu 5.4** *(eigene Fassung der Sitzung nach diesem Absatz,
kein Fable-Wortlaut):* Bei `elliott_wave` ist das Positionslimit keine
Rasterachse (2.4); „gefundene" statt „ausgeführte" Trades ist dort trotzdem
nötig, weil die Zuteilung mit der Kapitalschranke `floor(1/ALLOCATION_PCT)`
entscheidet, welche gefundenen Trades ausgeführt werden — der Grundsatz greift
über „oder von der Ausführung" (41.2, B1). Marke bei 5.4.

**C5 (e) — `purge_tage` / „Trainingsende"** · Art: nach der Messung entschieden
— ⭐ **BERICHTIGT (entschieden) durch 42.1 (D5)** · Quelle: 24d Abschnitt 1

„**Messbitte, nur das Ob:** Liest irgendeine Grösse, die der Lauf oder die Benchmark-Tabelle verwendet, heute `purge_tage`?"

Entschieden in 25a Abschnitt 1 (1), zeichengleich: „**(1) `purge_tage` hat keinen Leser im Lauf** — Fall „historischer Stand". Eintrag e aus 24d ist damit entschieden: Tatsachennotiz, keine Neuherleitung, `G8` prüft ein Relikt."

**Stand, gemessen:** `purge_tage`, `embargo_tage` und
`training_bis_ausschliesslich` sind aus dem gerechneten Plan entfernt (TB-104,
`f334a7b`); `faltenplan.py` nennt sie nur noch im Kopfkommentar. `G8` ist
angepasst, nicht gelöscht. Hash-Übergang in 42.5.

**C6 (f) — Modus-Lauf = Resolver-Modus; Hilfsordner kein Nachweis** · Art:
Registertext (Ergänzung zu 5e und zur Resolver-Pflicht) · Quelle: 24d Abschnitt
3

> **Registertext, Ergänzung zu 5e und zur Resolver-Pflicht (24c):** Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers (`shared/paths.py`, `TB_SELEKTIONSWURZEL`). Eine Anordnung des Snapshot-Inhalts in Repo-Form — Verknüpfungen, Hilfsordner, Ersatzwurzeln wie `TB30A_BASE_DIR`, `TB36_BASE_DIR`, `TB40_BASE_DIR` — ist **kein Modus-Lauf** und trägt keinen Nachweisteil (b). Ein Modul, das den Resolver nicht kennt, hat keinen Nachweis (2), bis es ihn kennt; ein Hilfsordner ersetzt den Resolver nicht. Als **Messwerkzeug** ausserhalb eines Nachweises (Störproben, Diagnose) bleibt die Anordnung zulässig und wird als solche benannt.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* (1) 23e: *„der Nachweis muss denselben Weg gehen wie der Lauf"* — der Lauf am Tag geht durch den Resolver; ein Hilfsordner prüft den **Inhalt** des Snapshots, nicht den **Weg** dorthin, und TB-98 Befund 1 war ein Fehler des Weges bei richtigem Inhalt. (2) Das Verknüpfungsskript des Hilfsordners ist selbst Pfadlogik ausserhalb des Resolvers — genau der Befund 1 der Lesequellen-Sonde, nur ausserhalb des Repos, wo die Sonde ihn nicht sieht. (3) 24c: eine Anordnung, ein Ort, der sie kennt. Kein Ergebnis.

**Stand, gemessen:** angewandt seit TB-103. `TB36_BASE_DIR` und `--daten` sind
seit TB-104 als Messwerkzeug benannt und brechen unter dem Modus mit 2 ab.
`TB30A_BASE_DIR` greift in `herkunft.py:51` auch unter gesetzten
Modus-Variablen (TB-106 A11) — offene Frage 25d (3), 42.6. Marke bei 39.6.

**C7 (g) — TB-92 A1b und TB-95 D1 waren Hilfsordner-Läufe** · Art:
Tatsachennotiz · Quelle: 24d Abschnitt 3

> **Tatsachennotiz dazu, damit niemand alte Läufe umdeutet:** TB-92 A1b (39.6: *„`TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` nicht (0 Treffer)"*) und TB-95 D1 waren nach dieser Regel beide Hilfsordner-Läufe. Ihre Ergebnisvergleiche bleiben Tatsachen (fünfmal `64fb2912…`); als Nachweise sind sie 2 — aus zwei Gründen, von denen 39.8 der ältere ist.

Marke bei 39.6.

**C8 (h) — „TB-91 A1b" lies „TB-92 A1b"** · Art: Berichtigung an 24c · Quelle:
24d Abschnitt 3 · berichtigt 41.2 (B8)

> **Erst mein Fehler, dann der Widerspruch.** Ich habe in 24c „TB-91 A1b" geschrieben. Das Register nennt den Modus-Nachweis der Benchmark-Tabelle **TB-92 A1b** (Kopf von 39.6: *„Fable 23e, TB-92 A1b"*; 39.5: `benchmark.py` `3960375a…` → `d6bdd558…` ist TB-91, die Neurechnung). Eine Auftragsnummer, nicht gemessen — dieselbe Klasse wie TB-94/TB-96 in 24a. **Angenommen; siebter Fall.** Ihr habt konsequenterweise in den TB-91-Belegen gesucht.

**C9 (i) — „Lesehaken erst TB-95" gegen 39.6/39.8** · Art: nach Messung
eingetragen · Quelle: 24d Abschnitt 3

> **Der Widerspruch:** Ihr schreibt *„Der Lesehaken entstand erst mit TB-95."* Das Register sagt in 39.6 (Tabelle, Zeile „Lesequellen") über TB-92 A1b: *„Lesehaken über `sys.addaudithook`, in Lauf 3 und 4 prozessübergreifend über `sitecustomize` (11 Prozesse): 0 Lesezugriffe auf `data/` oder `config/` des Repos; 222 CSV und 2 Universumsdateien aus dem Snapshot. Dazu Eingaben ausserhalb des Snapshots — 39.8"* — und 39.8 heisst *„Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand"* und nennt als Beleg `docs/belege/TB-92/a1b_lesequellen_kinder.txt`. **Das habe ich im Register gelesen, nicht im Repo gemessen.** Eines von beiden stimmt nicht: entweder existiert dieser Beleg mit diesem Inhalt (dann ist eure Aussage falsch und der Haken ist vom 23.09., TB-92), oder er existiert nicht (dann ist 39.6 falsch, und das wäre ein Registerbefund). *[Voraussetzung, zu messen: `docs/belege/TB-92/a1b_lesequellen_kinder.txt`, Lauf 3 und 4.]*

**Die Messung — der Widerspruch geht zugunsten des Registers auf:**
`docs/belege/TB-92/a1b_lesequellen_kinder.txt` (1756 B) und
`docs/belege/TB-92/a1b_lesehaken.py` (858 B) existieren, beide hinzugefügt mit
`0292e92` am 23.09.2026, 18:42; die Datei beginnt mit „== Lauf 3" und führt die
Zugriffe je Datei. ⇒ **Der Lesehaken stammt von TB-92; 39.6 und 39.8 hatten
recht. Der Satz „erst mit TB-95" war ein Fehler des steuernden Chats** — eine
Nummer übernommen statt geprüft (`docs/projektfuehrung/UEBERGABE_2026-09-25.md`,
Block 7 Nr. 1). Fable dazu, 25a Abschnitt 1 (3), zeichengleich:
„**(3) Der Lesehaken ist von TB-92; euer Satz war falsch, das Register hatte recht.** Angenommen, und die Ursache benennt ihr richtig: eine Nummer übernommen statt geprüft — meine falsche Nummer, eure ungeprüfte Übernahme, eine Kette."
Und die Folge: „Die Folgerung steht: Der Benchmark-Nachweis ist 2 aus seinem eigenen Protokoll; führbar nach beiden Eingaben, dann als Neurechnung mit beiden Teilen."
Marke bei 39.8.

## 42. Zugriffsklassen, Laufbereich, die vier Rückfälle und ihr Schluss — die Einträge aus Fable 25a, 25b, 25c und die Tatsachennotizen TB-103 bis TB-107 (TB-108, 25.09.2026)

Bauart, Herkunft der Quellen und Gliederung wie **41.0**. Hier stehen die
Einträge aus **25a, 25b und 25c** (42.1–42.3), die Tatsachennotizen aus den
Aufträgen TB-103 bis TB-107 (42.4), die Hash-Übergänge seit 39.5 (42.5), was
offen bleibt (42.6) und was hier nicht getan wurde (42.7). ⛔ **Nichts aus 25d,
25e, 25f** — die Antworten stehen aus; sie kommen in Abschnitt 43.

### 42.1 Aus Fable 25a (`FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md`)

Fables Liste für dieses Register, 25a Abschnitt 5, zeichengleich (Nachsatz zur
Tabelle):

> **Für Register 41/42 kommen hinzu** (zu 24c Abschnitt 6 und 24d Abschnitt 4): die drei Klassen (3 (A)), die vier Teile der Symbolbedingung (3 (B)), der Laufbereich (4), die Präzisierung zu 33.3/35.4 (1 (1)), die Tatsachennotiz zu TB-103 (Resolver mit MANIFEST als Ort; Trockenlauf mit Umgebungsliste; Ladeprotokoll-Teil (4) offen), die Tatsachennotiz zum Lesehaken (TB-92, `a1b_lesehaken.py`; eure Berichtigung), die Schreibziel-Notiz zu `manuelle_eingriffe.log`, die Einordnung der vier Rückfälle mit dem Verweis auf 11.1.

**D1 — Berichtigung zu 24c Abschnitt 2: die Fundstelle der Resolver-Pflicht** ·
Art: Berichtigung einer Fundstelle · Quelle: 25a Abschnitt 3 (C) · berichtigt
41.2 (B5)

> Angenommen: *„über den Resolver (`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`)"*. Meine Fundstelle `shared/paths.py::get_strategy_paths()` war falsch — eine Funktion in der falschen Datei genannt, nicht gemessen. **Achter Fall**, dieselbe Klasse. Berichtigung zu 24c Abschnitt 2 mit eurem Wortlaut.

⇒ **Die Resolver-Pflicht (41.2, B5) gilt mit dieser Fundstelle:** „über den
Resolver (`shared/paths.py`, direkt oder über
`strategy_paths.get_strategy_paths()`)".

**D6 — die drei Klassen von Zugriffen** · Art: Registertext (Präzisierung zu
24c (b) und zur Tag-Vorbedingung 24b A2) · Quelle: 25a Abschnitt 3 (A)

> **Präzisierung zu 24c (b) und zur Tag-Vorbedingung 24b A2 — drei Klassen von Zugriffen:** Jeder Datei-Zugriff eines Modus-Laufs fällt in genau eine von drei Klassen. **(i) Eingaben** — Kurs-, Universums-, Ergebnis- und Eingabedateien: zulässig nur innerhalb `snapshots/<hash>/` oder als registrierte Eingabedatei; jeder andere ist Befund 1 des Nachweisteils (b). **(ii) Umgebung** — `requirements.lock`, Interpreter- und Plattformdateien, Zufallsquelle, Zeitzonendaten, vom Import der registrierten Pakete geöffnet: zulässig; die Liste dieser Zugriffe je Lauf-Typ steht **mit Aufrufstapel als Tatsachennotiz**, und ein Umgebungszugriff, der in dieser Liste nicht steht, ist ein Befund 1 — nicht weil er die Rechnung berührt, sondern weil niemand weiss, ob er es tut. **(iii) Schreibzugriffe** — ein Modus-Lauf öffnet zum Schreiben nur sein `--ziel` und Belegpfade; jedes andere Schreibziel ist Befund 1 der Schreibziele-Sonde, auch ohne geschriebene Bytes. „0 Zugriffe ausserhalb `snapshots/<hash>/`" in 24b A2 lies „0 Zugriffe der Klasse (i) ausserhalb; Klasse (ii) nach Liste; Klasse (iii) leer".

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5f — die Umgebung ist registriert (Lock mit Hash, Abschnitt 20), und `requirements.lock` ist die Datei, mit der der Modus die Umgebung **prüft**; ein Nachweis, der die Prüfung als Verstoss zählt, widerspricht sich. Warum die Liste trotzdem geführt wird: `/dev/urandom` beim pandas-Import ist harmlos, solange die Neurechnung bytegleich ist — und genau das ist Nachweisteil (a); ein Lauf, der plötzlich eine sechste Umgebungsdatei öffnet, hat ein Paket oder einen Importpfad gewechselt, und das sieht man sonst nirgends. Kein Ergebnis.

⭐ **ERGÄNZT durch 42.2 (E1: Klasse (iv) Zwischenablage; E2: Klasse „Code") und
42.3 (F7: Interpreter-Caches unter (ii); F8: registrierte Protokolle in (iii)).**

**D2 — „0 Zugriffe ausserhalb" lies nach den drei Klassen** · Art: Präzisierung
des eigenen Wortlauts (an 24b A2, 41.1 A11) · Quelle: der letzte Satz von D6
oben. ⭐ **ERGÄNZT durch 42.2 (E1) und 42.3 (F8)** — Klasse (iii) heisst seitdem
„kein Schreibzugriff ausser `--ziel`, Belegpfaden, Klasse (iv) und registrierten
Protokollen".

**D3/D7 — die Liste ist gleich, die Menge ist registriert: die vier Teile der
Symbolbedingung** · Art: Präzisierung des eigenen Wortlauts (an 24b A2) und
Registertext · Quelle: 25a Abschnitt 3 (B). Die Stoffsammlung führt denselben
Text zweimal (D3 als Präzisierung, D7 als Registertext); er steht hier einmal.

> **Präzisierung zu 24b A2 („geladene Symbolmenge gleich Universumsdatei"):** (1) Die **Liste**, die der Bot erhält, ist gleich der Universumsdatei des Snapshots nach `EXCLUDE_SYMBOLS` (16.1.3: 24 von 25; 150). (2) Die **geladene Menge** ist gleich der in 16.1.1 für die Bestätigungsperiode registrierten Zahl je Bot *[Voraussetzung, zu messen: dass der Trockenlauf den Loader am Datenende aufruft, wie die Bestätigungsspalte von 16.1.1 gemessen wurde]*. (3) Jede Differenz zwischen (1) und (2) steht im Ladeprotokoll je Symbol mit Grund. (4) Das Ladeprotokoll nennt die Länge der Liste, die Zeilenzahl der Universumsdatei und die **Quelle** der Liste (Pfad). Gleichheit mit und ohne Modus ist Tatsachennotiz, keine Bedingung.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 3b (b) — welche Symbole geladen werden, entscheidet die registrierte `MIN_HISTORY_*`-Tabelle, und ihr Ergebnis ist in 16.1.1 gemessen und eingetragen; eine Vorbedingung prüft gegen das Register, nicht gegen einen zweiten Lauf. Kein Ergebnis. **Zu (4):** Das Ladeprotokoll nennt heute weder die Zeilenzahl der Datei noch die Quelle — ihr habt es gemessen. Bis das nachgezogen ist (Handwerk mit Freigabe, `shared/ladeprotokoll.py`), ist die Vorbedingung in Teil (4) **nicht** erfüllt; das steht so in der Tatsachennotiz zu TB-103, nicht als Mangel des Laufs, sondern als das, was noch fehlt.

⭐ **PRÄZISIERT durch 42.2 (E6):** Die geladene Menge wird am Stichtag
Go-Live-Schnitt (5.2), ausschliesslich, ermittelt.

**Stand, gemessen:** Teil (4) ist **weiter nicht erfüllt** —
`shared/ladeprotokoll.py` unverändert seit `55b991d` (TB-45); der Meldetext
„Keines ausgelassen." steht dort unverändert (Z. 161).

**D4 — Wiederholung am Tag-Commit** · Art: Ergänzung zur Tag-Vorbedingung (24b
A2, 41.1 A11) · Quelle: 25a Abschnitt 2

> **Ergänzung zur Tag-Vorbedingung (24b A2):** Der Trockenlauf aller neun Bots im Modus wird **am Tag-Commit** wiederholt — wie das letzte Abbild (37.3) trägt sein Protokoll die Hashes des Standes, den der Tag signiert. Ein Trockenlauf an einem früheren Stand ist eine Tatsachennotiz, keine Tag-Vorbedingung.

*Seine Quelle des Grundes, zeichengleich:* „37.3 (das letzte Abbild passt zum Tag-Commit); zwischen `836865f` und dem Tag ändern sich `paths.py`-nahe Module noch (Plan-Punkt 2, die Rückfälle aus Abschnitt 4). Kein Ergebnis."

**D5 — Präzisierung zu 33.3/35.4 (Plan ohne Verfahren-A-Felder)** · Art:
Präzisierung, Ersteintrag — ⭐⭐ **BERICHTIGT durch 42.2 (E3)**: Der Plan
schrumpft nicht; die Sonde vergleicht über eine registrierte Abbildung · Quelle:
25a Abschnitt 1 (1) · entscheidet 41.3 (C5)

> **Präzisierung zu 33.3/35.4 (Ersteintrag):** Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die 33.2/33.3 nicht kennt. Die Faltenplan-Sonde vergleicht den ganzen gerechneten Plan gegen das Abbild, nicht eine Auswahl seiner Felder. Verfahren-A-Felder (`purge_tage`, `embargo_tage`, `training_bis_ausschliesslich`) werden vor dem Tag aus `faltenplan.py` entfernt — Berichtigung des Codes an 2c/4a, planmässig nach 37.3 (Sperrlistenpunkt 2, Freigabe, alter und neuer Hash, neues Abbild). `G8` wird nicht gelöscht, sondern angepasst (23a): es prüft künftig, dass der gerechnete Plan je Falte keine Felder ausserhalb der Feldliste trägt — dieselbe Stelle, die registrierte Erwartung.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 33.1 (Fables Satz: „Sechzig verschiedene Trainingsgrenzen in einer Datei beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht man der Datei nicht an") — er gilt für den gerechneten Plan wie für die Datei. Kein Ergebnis. Wann das geschieht (mit dem Abbild-Auftrag oder davor), ist Handwerk; **vor** der Sonde muss es sein, sonst ist ihr erster Lauf rot aus einem Grund, der keiner ist.

⚠️ **Welcher Teil weiter gilt:** Die Entfernung der drei Verfahren-A-Felder aus
dem gerechneten Plan und die Anpassung von `G8` sind vollzogen (TB-104,
`f334a7b`; 42.5). Der erste Satz („trägt keine Grösse, die 33.2/33.3 nicht
kennt") ist durch E3 ersetzt — er hätte die Herleitungsfelder mitgetroffen.
Marken bei 33.3 und 35.4.

**D8 — der Laufbereich** · Art: Registertext, Ersteintrag — ⭐⭐ **BERICHTIGT
durch 42.2 (E5)**: Vereinigung aller registrierten Lauf-Typen, gemessen am
Tag-Commit · Quelle: 25a Abschnitt 4

> **Registertext, Ersteintrag — Laufbereich:** Der Laufbereich ist die Menge der Module, die ein Modus-Lauf lädt oder ausführt (Trockenlauf aller neun Bots, Erzeuger, `benchmark.py`, `faltenplan.py`, `auswertung.py` und ihre Kindprozesse), gemessen am Aufrufstapel des Lese-Audits. Die Regeln „kein Fallback unter dem Modus" (24b A2), die Resolver-Pflicht (24c) und die drei Ausgänge (36.5) gelten für genau diese Menge; die Sonde „Lesequellen" führt sie. Ein Rückfall in einem Modul ausserhalb des Laufbereichs ist eine Tatsachennotiz, kein Befund — bis das Modul geladen wird.

*Seine Quelle des Grundes, zeichengleich:* „5e (der Lauf belegt, woraus er gelesen hat — und damit, was er ist) und A8 (eine Regel braucht eine Menge, auf der jemand sie prüfen kann). Kein Ergebnis."

⭐ **Dieser Eintrag bestimmt die Menge, für die die drei Ausgänge aus 36.5
gelten** — Marke bei 36.5.

**D9 — Tatsachennotiz zu TB-103** · Art: Tatsachennotiz (mit Bedingung) ·
Quelle: 25a Abschnitt 2

> **Resolver:** `CONFIG_DIR = <snapshot>/config`, Prüfung beim Import gegen das, was **das MANIFEST** unter `config/` nennt, `SystemExit(2)` bei fehlend/leer/nicht genannt, Dateinamen nicht in `paths.py`, ohne Modus 99 Pfade 0 Unterschiede, vier Mutationsproben, jede beisst allein, 35/35 und 191/191. Das ist die Bauart aus 24b A2, und der Punkt, dass das MANIFEST der eine Ort ist, der die Anordnung kennt, ist besser als das, was ich vorgeschlagen hatte („Kurse flach, Universum unter `config/`" stand bei mir als Beschreibung, nicht als Quelle). Die fünf Symboldateien mit dem eingebauten Rückfall sind unverändert; ihr Rückfall ist unter dem Modus unerreichbar — solange `paths.py` so bleibt. Das ist eine Tatsachennotiz mit Bedingung, und sie gehört so ins Register.

Und zum Ladeprotokoll, 25a Abschnitt 3 (B), zeichengleich: „Bis das nachgezogen ist (Handwerk mit Freigabe, `shared/ladeprotokoll.py`), ist die Vorbedingung in Teil (4) **nicht** erfüllt; das steht so in der Tatsachennotiz zu TB-103, nicht als Mangel des Laufs, sondern als das, was noch fehlt."

**Tatsachennotiz (gemessen, TB-103, `docs/ERGEBNIS_TB-103_resolver_und_trockenlauf.md`):**
Resolver `shared/paths.py` (`d87997e`): unter dem Modus `CONFIG_DIR =
<snapshot>/config` (`CONFIG_UNTERORDNER`, Z. 213), Prüfung beim Import gegen
das MANIFEST, `SystemExit(2)` bei fehlender, leerer oder nicht genannter
Universumsdatei; ohne Modus 99 Pfade, 0 Unterschiede. Trockenlauf aller neun
(`836865f`): 9 × rc 0, Liste = Universumsdatei 9/9, 0 Kurs- oder
Universumszugriffe ausserhalb des Snapshots, 0-mal Standardliste; je Bot fünf
Umgebungszugriffe (`requirements.lock` und vier Systemdateien) — die
Umgebungsliste nach D6 (ii). ⚠️ **Die Bedingung:** Der eingebaute Rückfall der
Symbollisten ist unter dem Modus unerreichbar, **solange `paths.py` so bleibt**;
seit TB-105 (`f65c344`) endet zudem `symbols_config.py` unter dem Modus bei
leerer Liste mit 2 (Rückfall (a), D12). Ladeprotokoll-Teil (4) **offen** (D3/D7).

**D10 — Tatsachennotiz: der Lesehaken ist von TB-92** · Art: Tatsachennotiz
(Berichtigung des steuernden Chats) · Quelle: 25a Abschnitt 1 (3) — Wortlaut und
Messung in **41.3 (C9)**. Werkzeug: `docs/belege/TB-92/a1b_lesehaken.py`.

**D11 — Schreibziel `manuelle_eingriffe.log`** · Art: Tatsachennotiz · Quelle:
25a Abschnitt 1 (3), derselbe Absatz wie D10

„der Modus-Lauf öffnet `logs/notifications/manuelle_eingriffe.log` **im Modus `a`** — zum Anhängen, aus dem Repo, über einen Import aus `notifications/`." — „Ein Import, der beim Laden eine Datei zum Schreiben öffnet, ist eine Nebenwirkung, die im Laufbereich nichts zu suchen hat."

**Stand, gemessen:** **behoben in TB-105** (`d48a195`):
`notifications/manual_close.py` legt Ordner und Protokoll erst bei der ersten
Zeile an; der Weg im Modus war `registerdaten.py:62` → `manual_close.py` (TB-104
C5). Benchmark im Modus seither ohne diesen Zugriff (TB-105 F2). Marke bei 39.8.

**D12 — die vier Rückfälle, mit Verweis auf 11.1** · Art: Registertext
(Einordnung und Rangfolge) · Quelle: 25a Abschnitt 4

> **Die vier weiteren Rückfälle — alle vier vor den Tag, in dieser Rangfolge, jeder mit Gegenprobe (Rückfall erreichbar gemacht ⇒ Rückgabe 2):**
>
> | | Rückfall | Warum vor den Tag |
> |---|---|---|
> | **1** | **(b)** `t3_supertrend`: BTC-Regimefilter fällt still weg, wenn BTCUSDT nicht geladen ist | ⚠️ **Schon registriert als Voraussetzung des Laufs** — 11.1 (`shared/regimewache.py`, `pruefe_einbau()`, „Solange er es nicht ist, darf der Lauf nicht starten") und Schlusssatz von Abschnitt 10. Kein neuer Beschluss nötig; euer Fund ist die Messung, dass 11.1 offen ist. Dass BTCUSDT im Trockenlauf geladen war, ändert nichts: 11.1 begründet den Abbruch mit Determinismus, nicht mit dem heutigen Bestand |
> | **2** | **(c)** Backtest-Skripte enden bei „Keine Daten gefunden" mit `exit()`, rc 0 | Das ist TB-45 in Reinform — 0 ohne Messung —, und 36.5 gilt für jede Wache und jeden Lauf: „Kein Aufruf endet mit 0, ohne dass gemessen wurde." Unter dem Modus: 2 |
> | **3** | **(d)** Stille Ersatzwerte für Schwellen in `faltenplan.py`, `benchmark.py`, `auswertung.py` | Ein Ersatzwert für eine registrierte Schwelle ist ein Fallback für einen Parameter (24b A2 nennt Schwellen ausdrücklich) — und er ist schlimmer als ein Schalter, den 12 für `auswertung.py` ausschliesst: Ein Schalter ist sichtbar, ein `.get(…, default)` nicht. Vorab je Stelle Tatsachennotiz, ob die registrierte Eingabe den Schlüssel je auslässt; unabhängig davon Ersatz durch Abbruch 2. `auswertung.py` ist Sperrlistenpunkt 3/5/14 — planmässig nach 37.3, wie TB-92 |
> | **4** | **(a)** Krypto-Liste nach `EXCLUDE_SYMBOLS` leer ⇒ Standardliste | Auf dem registrierten Snapshot unerreichbar — aber die Regel gilt für den Modus, nicht für diesen Snapshot; ein Rückfall, den erst der nächste Snapshot erreicht, ist genau „gleich welcher Art". Kleinster Aufwand (eine Prüfung „leer ⇒ 2" in `symbols_config.py`, Live-Code, eigene Freigabe); kleinster Rang, aber nicht als Notiz abgetan |

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 24b A2 im Wortlaut, 36.5, 11.1. Kein Ergebnis: Keiner der vier verändert, was der Lauf rechnet, wenn alles da ist; sie verändern, was er tut, wenn etwas fehlt — und das ist das Einzige, was der Modus regelt.

**Stand, gemessen — alle vier geschlossen:** (b) TB-105 (`f524327`,
`regimewache.pruefe_einbau()` heute `vollstaendig: True`, 3 von 3 eingebaut;
G1) · (c) TB-105 (`f65c344`, 14 Stellen, unter dem Modus 2; G2) · (a) TB-105
(`f65c344`, `symbols_config.py`) · (d) in den eingefrorenen Dateien TB-106
(`abeca36`, `a08c13a`, `5cc1de4`), in den nicht gesperrten Hilfsprogrammen
TB-107 (`33d50f2`, `f5fdb53`, `5cfe472`, `a79e715`). ⚠️ `f5fdb53` ist **vor**
Fables Antwort auf 25d gebaut und als eigener Commit revertierbar (42.6).
Marke bei 11.

### 42.2 Aus Fable 25b (`FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md`)

Fables Liste für dieses Register, 25b Abschnitt 4, Kopf, zeichengleich:

> ## 4. Was auf Register 41/42 kommt, zusätzlich zu 24c/24d/25a

**E1 (a) — Klasse (iv), Zwischenablage; die Messumgebung für (iii) und (iv)** ·
Art: Registertext (Ergänzung zu 25a (A)) · Quelle: 25b Abschnitt 3 (1) ·
ergänzt 42.1 (D6)

> **Ergänzung zu 25a (A) — Klasse (iv), Zwischenablage:** Eine Datei, die derselbe Lauf schreibt **und** liest, ist Zwischenablage. Sie ist zulässig, wenn (1) ihr Ordner je Lauf neu und eindeutig angelegt wird (`mkdtemp`) **oder** unter `--ziel` liegt, (2) kein Prozess ausserhalb des Laufs sie liest — im Audit erscheint jeder Lesezugriff auf sie mit dem Schreibzugriff desselben Laufs daneben — und (3) sie am Ende des Laufs entfernt ist **oder** ihr Pfad im Beleg steht. Fehlt eine der drei, ist sie Befund 1 der Schreibziele-Sonde. Klasse (iii) („Schreibziele leer") heisst damit: kein Schreibzugriff ausser `--ziel`, Belegpfaden und Klasse (iv). Gemessen wird (iii) und (iv) in einer Umgebung, in der die Ziele fehlen (Abschnitt 1).

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5e — der Audit soll zeigen, woraus der Lauf gelesen hat; eine Zwischenablage, die er selbst geschrieben hat, ist keine Eingabe, und der Audit muss das **sehen**, nicht wissen. Warum (1): Ein deterministischer Pfad in `$TMPDIR` könnte vom nächsten Lauf gelesen werden — dann wäre eine Zwischenablage eine unregistrierte Eingabe; `mkdtemp` schliesst das aus. Warum (3): Elf Ordner je Lauf, die niemand entfernt, sind kein Verfahrensfehler, aber ein Bestand, den niemand kennt — und „nie entfernt" heisst heute: **Befund 1**, bis das Aufräumen eingebaut ist (Handwerk, klein). Kein Ergebnis.

**Stand, gemessen:** `tb40_lauf_*` erfüllt Bedingung (3) seit TB-107 (`a79e715`:
entfernt nach dem Lesen, ohne Ergebnis bleibt der Ordner und sein Pfad steht in
der Meldung). `tb40_faltenplan_*` und `tb40_proben_*` sind offen — Frage 25e (1),
42.6.

> ⭐ **Reichweite: siehe 45.2** (Fable 26a R2, TB-114, 26.09.2026). Eintrag
> und Stand oben bleiben zeichengleich.

**E2 (b) — Klasse „Code"; Ergänzung zu 19: Sauberkeit über den Laufbereich** ·
Art: Registertext · Quelle: 25b Abschnitt 3 (2) · ergänzt 42.1 (D6)

> **Ergänzung zu 25a (A) — Klasse „Code":** Ein Lesezugriff auf eine Datei unter der Codewurzel ist Klasse „Code" und zulässig, wenn die Datei in einem Pfad liegt, den die Startprüfung (19) über `HEAD` und sauberen Arbeitsbaum bindet. Eine Datei unter der Codewurzel **ausserhalb** dieser Pfade ist weder Code noch Eingabe — sie ist ungebunden und ein Befund 1. Ein Leser, der Werte per Muster aus Quelltext liest, endet mit 2, wenn das Muster nicht genau einmal trifft; ein Ersatzwert ist ausgeschlossen.

> **Und der Befund, den diese Frage erst sichtbar macht:** 19 nennt als `ARBEITSBAUM_PFADE` **`shared/`, `strategies/` und `requirements.lock`** — nicht `research/`, nicht `notifications/`. Der gemessene Laufbereich hat 11 Module aus `research/` und eines aus `notifications/`. Ein veränderter, uncommitteter `benchmark.py` oder `faltenplan.py` würde die Startprüfung heute **nicht** aufhalten. *[Voraussetzung, zu messen: dass 19 den Stand noch beschreibt — die Tatsachennotiz dort ist vom 19.09.]*

> **Ergänzung zu 19 (Registertext 5e, Codeherkunft):** Die Sauberkeitsprüfung des Arbeitsbaums erstreckt sich auf **jeden Pfad des Laufbereichs** (Abschnitt 5 unten), nicht nur auf `shared/`, `strategies/` und `requirements.lock`; `data/` bleibt ausgenommen (19, aus dem dort genannten Grund). Die Liste der geprüften Pfade steht als Tatsachennotiz neben der Laufbereichsmessung und wird mit ihr am Tag-Commit erneuert.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 19 selbst — „Liegen Aufrufer und Resolver in verschiedenen Bäumen, beschreibt kein einzelner Commit den gelaufenen Code"; das gilt für jedes Modul, das läuft. Kein Ergebnis. Zu den neun Optimierern selbst: sie liegen unter `strategies/`, sind also heute schon gebunden — eure Lesart „Code" gilt für sie ohne Vorbehalt. *[Messbitte, nur das Ob: endet `_min_history` mit 2, wenn das Muster in einer Datei nicht genau einmal trifft?]*

**Stand, gemessen:** `shared/paths.py` Z. 225 `ARBEITSBAUM_PFADE = ("shared",
"strategies", LOCK)` — unverändert; die Tatsachennotiz in 19 beschreibt den Stand
(bestätigt in 25c 2 (d)). ⚠️ **Die Erweiterung ist nicht vollzogen**; sie ist
**Tag-Vorbedingung** (25c 2 (d)) und braucht **vorher** die Ausnahme für
registrierte Protokolle (42.3, F8) — die steht mit diesem Eintrag im Register.
Marke bei 19.

> ⭐ **Vollzogen, siehe 44.2 (44-7; TB-112 `9d711dc`, TB-113, 26.09.2026):**
> `ARBEITSBAUM_PFADE` hat 15 Einträge (die 12 Module des Laufbereichs
> ausserhalb `shared/`/`strategies/` als Einzeldateien); die Liste steht als
> Tatsachennotiz neben der Laufbereichsmessung (44-8). Eintrag und Stand oben
> bleiben zeichengleich.

> ⭐ **Pflege von `ARBEITSBAUM_PFADE`: siehe 45.4** (Fable 26a R4, TB-114,
> 26.09.2026). Eintrag, Stand und die Marke oben bleiben zeichengleich.

**E3 (c) — Berichtigung zu 25a (1): der Plan schrumpft nicht; registrierte
Abbildung; die Feldliste des Plans ist Registertext** · Art: Berichtigung und
Registertext · Quelle: 25b Abschnitt 3 (3) · berichtigt 42.1 (D5)

> **Berichtigung zu 25a (1), Präzisierung zu 33.3/35.4:** „Der Plan … trägt keine Grösse, die 33.2/33.3 nicht kennt" lies: **„Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die das Verfahren nicht kennt** (Trainingsgrenzen, Embargo, Purge, Mindesttraining). Die Faltenplan-Sonde vergleicht den Plan mit dem Abbild über eine **registrierte Abbildung**: je Feld des Abbilds (33.3) der Planschlüssel, aus dem es gebildet wird. Die **Feldliste des gerechneten Plans** — jeder Schlüssel je Plan und je Falte, mit der Registerstelle, die ihn begründet — ist Registertext; ein Schlüssel im Plan, der dort nicht steht, ist ein Befund der Sonde, ein fehlender ebenso."

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 33.3 (ein Abbild trägt genau die Grössen seines Abschnitts — das Abbild, nicht der Plan), 25.3/32.1 (der Plan trägt seine Herleitung), 33.1 (Felder, die ein anderes Verfahren beschreiben, dürfen nicht drin sein). Kein Ergebnis. **Zu `G8` heute:** Die Feldliste „aus dem Code" ist eine Kopie des Codes im Test — als benannter Zwischenstand zulässig, wie ihr es benannt habt; sie wandert mit Register 41/42 in den Registertext. Wie der Test dann an den Registertext gebunden wird (Parser wie `G6`, oder Literal mit Test gegen das Register wie in 32.5 (c)), ist die offene Frage aus 32.5 und Handwerk; ich entscheide sie nicht mit.

**Tatsachennotiz — die Feldliste, wie sie heute im Test steht (gemessen,
`test_vorregistrierung.py` `db50e187…`, Z. 105–113; Schlüsselnamen, keine
Werte):** je Plan `bestaetigungsperiode`, `erste_falte`, `erste_falte_4a`,
`erste_falte_4a_warm_ab`, `erste_falte_quelle`, `erste_falte_trockenlauf_H`,
`falten`, `faltenlaenge_begruendung`, `faltenlaenge_jahre`, `go_live_schnitt`,
`horizontbeginn`, `markt`, `selektionsfalten`, `status`, `trades_je_jahr`; je
Falte `angeschnitten`, `bis_ausschliesslich`, `name`, `rolle`, `von`.
⚠️⚠️ **Das ist noch nicht die Feldliste als Registertext:** 25b verlangt je
Schlüssel **die Registerstelle, die ihn begründet**, und die ist nicht
zugeordnet — das ist keine Abschrift, sondern eine Entscheidung je Schlüssel.
**Offen (42.6)**; bis dahin ist die Liste im Test der benannte Zwischenstand, den
25b zulässt. Ebenso offen: die registrierte Abbildung (je Feld des Abbilds der
Planschlüssel) und wie der Test an den Registertext gebunden wird (32.5, bei
Fable ausdrücklich nicht entschieden). Marken bei 33.3 und 35.4.

**E4 (d) — `mindesttraining_jahre`, `embargo_nach_falten`, die Berichtszeile** ·
Art: Berichtigung (Code an 15.1/2c) · Quelle: 25b Abschnitt 3 (4)

> Ja, alle drei. 23.5 hat sie schon benannt (*„Beides ist der ersetzte Verfahren-A-Satz (TB-65)"*, `T56b.6`), und 15.1 sagt: **kein Mindesttraining**, 2c: **kein Embargo zwischen Selektionsfalten**. Sie gehören zur Berichtigung Code an 2c/4a wie die drei Felder — und im ERZEUGT-Block von Abschnitt 3 steht die Zeile „Mindesttraining vor der ersten Falte: 4 Jahre" bis heute, was mit dem nächsten Erzeugen des Blocks von selbst verschwindet (39.1: der Block ist noch nicht neu erzeugt).

> **Zur Konstante in `registerdaten.py`** (Sperrlistenpunkt 1, Abschnitt-0-eingefroren): Das Feld und die Zeile gehen jetzt; die Konstante selbst bleibt, bis Punkt 1 ohnehin planmässig geöffnet wird (40.8 (h), die zwölf Rasterachsen) — bis dahin Tatsachennotiz „tot, kein Leser". *Ein Wert, der nichts mehr steuert, aber einen Namen trägt, der eine Regel verspricht, ist die K1h-Klasse; sie wird mit dem nächsten geplanten Zugriff auf die Datei bereinigt, nicht mit einem eigenen.*

Fables Messbitte dazu ist beantwortet, 25c Abschnitt 2 (c), zeichengleich:
„**(c) `MINDESTTRAINING_JAHRE` rechnet nirgends** — zwei tote Felder, eine tote Zeile: dieselbe Berichtigung wie die drei Felder, wie in 25b (4) gesagt; Konstante bis 40.8 (h)."

**Stand, gemessen:** beide Felder aus dem Plan und die Berichtszeile aus
`registerbericht.py` entfernt (TB-106, `abeca36`). `registerdaten.py:108`
`MINDESTTRAINING_JAHRE = 4` steht weiter; gelesen wird es von keinem Modul
(nur in Kommentaren von `faltenplan.py` und `benchmark.py` genannt) — tot, kein
Leser, bis Punkt 1 planmässig geöffnet wird (40.8 (h)). Der ERZEUGT-Block in
Abschnitt 3 trägt die Zeile „Mindesttraining" weiter, bis er neu erzeugt wird
(39.1; G7). Marke bei 23.5.

**E5 (e) — Berichtigung zu 25a Abschnitt 4: der Laufbereich ist die
Vereinigung aller Lauf-Typen** · Art: Berichtigung und Registertext · Quelle:
25b Abschnitt 3 (5) · berichtigt 42.1 (D8)

> **Berichtigung zu 25a Abschnitt 4 (Laufbereich):** Der Laufbereich ist die **Vereinigung** über alle Lauf-Typen des Selektionsmodus. Lauf-Typen sind: der Trockenlauf aller neun Bots; jeder Erzeuger einer registrierten Eingabedatei (`messgroessen.py`, der Listen-Erzeuger auf dem Signalpfad, der Erzeuger der Benchmark-Tabelle mit `faltenplan.py` und seinen Kindprozessen, der Abbild-Erzeuger); `auswertung.py` samt Laufwrapper; die Sonden, soweit sie im Modus laufen. Die Liste der Lauf-Typen ist Registertext und am Tag abschliessend; der Laufbereich wird **am Tag-Commit** über alle Lauf-Typen gemessen (Import-Audit), und das Rückfall-Inventar darüber ist am Tag leer.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 5e und die Messung, dass `messgroessen.py` ein Modus-Lauf ist (TB-103) — was unter dem Modus läuft, ist Laufbereich, gleich ob ich es aufgezählt habe. Kein Ergebnis. **Folge:** `herkunft.py` und `shared/regimewache.py` treten mit dem Erzeuger bzw. mit TB-105 (b) ein; die 80 sind ein Zwischenstand mit Datum. Und (c) — die `exit()`-Stellen in `__main__` — gehört dazu, sobald ein Modus-Lauf ein Bot-Skript direkt startet; ob der Listen-Erzeuger das tut (Import oder Kindprozess), ist Handwerk, aber die Regel gilt so oder so, weil der Laufbereich am Tag gemessen wird, nicht heute.

**Stand, gemessen — ein Zwischenstand mit Datum, nicht der Laufbereich:** 80
Repo-Module (TB-104, `516badc`), 81 am Stand `a79e715` (TB-107, 25.09.2026; neu
nur `shared/regimewache.py`), Liste
`docs/belege/TB-107/f1_laufbereich_vereinigung.txt` (84 Zeilen, davon 3
Messumschläge unter `docs/`). Gemessen über drei Lauf-Typen (Trockenlauf aller
neun, Benchmark, Import von `auswertung.py`), **nicht** über die registrierte
Liste der Lauf-Typen — die ist am Tag abschliessend. Die Messung am Tag-Commit
steht aus (42.6).

> ⭐ **42.2 E5 ERGÄNZT durch R29 (47.12)** (Fable 27c R29, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**E6 (f) — Präzisierung zu 25a (B) (2): der Stichtag ist der Go-Live-Schnitt** ·
Art: Präzisierung · Quelle: 25b Abschnitt 2 (3) · präzisiert 42.1 (D3/D7)

> **Präzisierung zu 25a (B), Teil (2):** Die geladene Menge je Bot wird **am Stichtag Go-Live-Schnitt (5.2), ausschliesslich** ermittelt — jede Kursreihe auf den Stichtag gekürzt, Loader wie in TB-40 — und gegen die Bestätigungsspalte von 16.1.1 verglichen. Ein Trockenlauf am Datenende bleibt zulässig als Nachweis „kein Fallback"; die Mengenprüfung gegen das Register läuft am Stichtag. Tatsachennotiz: am Stand `63e4b6c8…` ergeben beide Stichtage bei 9/9 Bots dieselbe Menge (TB-104).

*Seine Quelle des Grundes, zeichengleich:* „16.1.1 wurde so gemessen; eine Prüfung gegen das Register nimmt das Verfahren des Registers. Kein Ergebnis."

**E7 (g) — Tatsachennotizen zu TB-104** · Art: Tatsachennotiz · Quelle: 25b
Abschnitt 4, Zeile g. ⚠️ **Fable nennt hier nur Stichworte; die Notiz ist eine
eigene Fassung der Sitzung, kein Fable-Wortlaut** (gemessen,
`docs/ERGEBNIS_TB-104_leser_auf_resolver_und_altfelder.md`, `516badc`). Sein
einziger ausformulierter Satz dazu, 25b Abschnitt 2 (1), zeichengleich:
„*Was ihr mit „heute gleich, keine Eigenschaft des Codes" benennt, ist TB-102 in Kleinformat und gehört als Tatsachennotiz zu 37.4.*"

| | Tatsache (TB-104) |
|---|---|
| Leser | `benchmark.py`, `faltenplan_neun.py`, `loaderlauf.py`, `universum_trockenlauf.py` auf `shared/paths.py` (`572d725`); Ersatzwurzeln unter dem Modus 2, bevor gelesen wird; ohne Modus 8 Ausgaben bytegleich |
| Felder | `purge_tage`, `embargo_tage`, `training_bis_ausschliesslich` aus dem gerechneten Plan (`f334a7b`); Faltengrenzen gleich; `G8`/`G9` angepasst, `G8M` mit Gegenprobe |
| Abbild | `sperrliste_abbild_2026-09-25.json` `cb4eb1b4cf998efcded95acd4d712bb3a0856722489a80ce10bfce511eeb5f89` (`d96b352`) |
| Benchmark im Modus | zweimal bytegleich `64fb2912…`; Kurse und Universum nur aus dem Snapshot; ausserhalb die neun TB-24-Listen und `messgroessen.json` ⇒ Nachweis 2 |
| Umgebungsliste | dieselben fünf Dateien wie TB-103 |
| Schreibziel | `manuelle_eingriffe.log` im Modus `a` über `registerdaten.py:62` → `notifications/manual_close.py` (behoben TB-105, D11) |
| zu 37.4 | `herkunft.py::datenstand(daten_dir=None)` nimmt das Verzeichnis als Argument; `block()` rief es damals ohne Argument — geöffnet in TB-106 (42.3, F2) |
| zu 11.1 | `regimewache.pruefe_einbau()` **0 von 3** — die offene Voraussetzung, geschlossen in TB-105 (G1) |
| Laufbereich | 80 Module, Stand 25.09.2026, 10:32 (E5) |

**E8 (h) — „offen bis zur Messung"** · Art: offene Punkte — ⭐ **BEANTWORTET
durch 25c** · Quelle: 25b Abschnitt 4, Zeile h: „`_bedingung` `None` (α oder β) — **vor TB-106**; `anhaengen()`; `_min_history` bei Fehltreffer; `MINDESTTRAINING_JAHRE` in `erste_falte_4a`"

Alle vier sind beantwortet und umgesetzt: `_bedingung` 42.3 (F1, TB-106) ·
`anhaengen()` 42.3 (F2, TB-106) · `_min_history` 42.3 (F4, TB-107) ·
`MINDESTTRAINING_JAHRE` E4 oben (25c 2 (c), TB-106).

### 42.3 Aus Fable 25c (`FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md`)

**F1 (a) — „keine Rasterbedingung (Abschnitt 6)"; unbekannter Bedingungstext ⇒
2, eine Deutung** · Art: Berichtigung einer Benennung und Registertext ·
Quelle: 25c Abschnitt 1

> **Eine Fundstelle berichtige ich an eurer Berichtigung:** Der Satz *„Zellen, in denen die Strategie nicht definiert ist, existieren nicht … von 1.024 auf 384"* steht in **Abschnitt 6 (Die Plateau-Regel)**, im Absatz nach der Spitzenformel — nicht in Abschnitt 4. Abschnitt 4 ist die Drawdown-Bedingung, also genau das, wovon ihr den Zustand abgrenzen wollt; „keine Rasterbedingung (Abschnitt 4)" würde beim nächsten Leser dieselbe Verwechslung erzeugen, die ihr gerade auflöst. Richtig: **„keine Rasterbedingung (Abschnitt 6)"**. *[Gelesen im Register, Teil 1; nicht im Repo gemessen — die Nummer ist im Kopf der Kopie nachzusehen, sie lässt sich nicht verwechseln.]*

> **Registertext, Ergänzung zu 6 und 24b A2 — unbekannter Bedingungstext:** Ein nicht leerer `_bedingung`-Text, den der Code nicht als Rasterbedingung erkennt, ist ein Widerspruch zwischen Register und Code und endet mit 2 — unabhängig vom Modus. Die Deutung des Textes geschieht an **einer** Stelle; jeder Leser (Zellenzahl, Zellmenge, Nachbarschaft) ruft sie. Ein zweiter Textvergleich desselben Strings ist ein zweiter Parser (24b B4).

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 6 (die Rasterbedingung ist Registertext; ein Code, der sie still übergeht, rechnet ein anderes Raster mit N = 1.024 statt 384 und macht Abschnitt 3 und Festlegung 10 unbemerkt falsch), 24b A2, 24b B4. Kein Ergebnis. **Für TB-106:** rc 2 in `auswertung.py` jetzt; die zweite Stelle (`registerdaten.py:605`, Punkt 1) bekommt die Tatsachennotiz bis 40.8 (h), und **dort** wird die Deutung auf eine Funktion zusammengezogen, die beide rufen — nicht früher, weil Punkt 1 nicht für diesen Satz allein geöffnet wird. Eure Neigung „unabhängig vom Modus" ist richtig, aus eurem Grund.

**Stand, gemessen:** `auswertung.py` endet bei unbekanntem `_bedingung`-Text mit
2 (TB-106, `5cc1de4`). Die zweite Deutungsstelle steht weiter:
`registerdaten.py:605` vergleicht den String `"t3_fast_length <
t3_slow_length"` selbst (Punkt 1, unverändert seit vor 4faef05) — Tatsachennotiz
bis 40.8 (h), dort auf eine Funktion zusammenzuziehen. Marke bei 6.

**F2 (b) — Berichtigung zu 37.4: `herkunft.py` einmal geöffnet** · Art:
Berichtigung · Quelle: 25c Abschnitt 2 (a) · berichtigt 37.4

> **Berichtigung zu 37.4 (Entscheidung „Nicht öffnen"):** `herkunft.py` wird einmal geöffnet, um `datenstand()` den Datenpfad durch `block()` und `anhaengen()` durchzureichen (Argument, keine Voreinstellung unter dem Modus). Sonst ändert sich nichts: `EINGEFROREN` bleibt, wie 39.7 es entschieden hat; `register()` bezeugt weiter die Abschnitt-0-Menge; die Sonde bezeugt Abschnitt 10. **Planmässig geöffnet heisst nicht offen** — eine Öffnung nach 37.3 trägt genau die Änderung, für die sie beauftragt ist.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 37.4 nannte als Grund für „nicht öffnen" den Ort, nicht den Wortlaut, und die Sonde als Ersatz; für den Datenpfad der Protokollkette gibt es keinen Ersatz ausser einem zweiten Ort (25a). Der Satz „heute gleich, aber keine Eigenschaft des Codes" ist TB-102 in Kleinformat und steht als Tatsachennotiz daneben. Kein Ergebnis.

**Stand, gemessen:** geöffnet in TB-106 (`5791b4c`): `block()` und `anhaengen()`
reichen `daten_dir` an `datenstand()` durch, unter dem Modus Pflicht (sonst 2);
kein `makedirs` mehr; im Modus hasht die Kette den Snapshot (`d9449faf…`).
`EINGEFROREN`, `register()` und `SPERRLISTE_DATEIEN` zeichengleich (TB-106 E4).
Hash `56a1c2e1…` → `351f24c2…`, Punkte 11 und 12 (42.5). ⚠️ **Folgefragen 25d
(2) und (3)** (Prüfansicht unter dem Modus; `TB30A_BASE_DIR` wirkt in
`herkunft.py:51` auch unter dem Modus, G6) — offen, 42.6. Marken bei 37.4 und
39.7.

**F3 (c) — Tatsachennotiz zu 11: 11.1 geschlossen, 11.2/11.3 offen** · Art:
Tatsachennotiz · Quelle: 25c Abschnitt 3

> ⚠️ **Damit niemand „Abschnitt 11 erfüllt" liest:** Der Schlusssatz von Abschnitt 10 nennt **beide** Bug-Fixes aus 11. Erfüllt ist **11.1**. 11.2 (Agent 2 auf dem führenden Mass; `evaluate_combination_multi` liefert den Kapital-Drawdown noch nicht) und 11.3 (Durchreichung `sma_trend_filter`, `bb_*`) sind **TB-30b** und offen — sie gehören zum Laufcode, den es nach 24.5 noch nicht gibt. Tatsachennotiz zu 11: 11.1 geschlossen (TB-105), 11.2/11.3 offen.

⚠️ **Das gehört zu Abschnitt 10** (dessen Schlusssatz beide Bug-Fixes nennt);
nach 41.0 steht dort keine Marke — die Notiz steht hier und bei 11. Messung in
42.4 (G1).

**F4 (d) — `_min_history`: genau ein Treffer oder 2; die Erzeugerkette des
Trockenlaufs** · Art: Registertext · Quelle: 25c Abschnitt 4 (2) und 3

> `re.findall`, genau ein Treffer, sonst `SystemExit(2)`, unabhängig vom Modus; Mutationsproben „zwei Treffer" und „kein Treffer". Der Grund für „unabhängig vom Modus" ist derselbe wie bei (1): Ein Muster, das in einer Bot-Datei nicht genau einmal trifft, ist ein Widerspruch zwischen der registrierten Tabelle in 16.7 (b) und dem Code — kein Laufzustand. Und der stille Hinweis in `kerzen_elliott_wave()` ist die TB-45-Klasse (weiter ohne Wert); der `TypeError` in `loader_lesart()` ist laut, aber 1 statt 2 — nach 36.5 ein Aufruf, der nicht messen konnte und es nicht mit dem eigenen Wert sagt. Beides geht mit.

> **Zur Zwischenablage:** (1) und (2) erfüllt, (3) nicht — Befund 1, Handwerk. Eine Ergänzung zur Datei: `universum_trockenlauf.py` steht nicht im Abbild, und das ist heute richtig; **mit dem Faltenplan-Abbild (TB-100) wird die Erzeugerkette des Trockenlaufs registriert** — 33.3 sagt es schon: *„der erzeugende Code wird mit der Datei registriert (5e)"*. Bedingung (ii) der ersten Falte kommt aus dieser Kette (25.3); ein Abbild, dessen Erzeuger ungebunden ist, bezeugt weniger, als es sagt.

**Stand, gemessen:** `faltenschranke_messung.py::_min_history()` mit
`re.findall`, genau ein Treffer, sonst rc 2; `kerzen_elliott_wave()` ohne Wert
rc 2 (TB-107, `33d50f2`); je Bot-Datei genau ein Treffer (G9). ⚠️ **Die
Erzeugerkette ist nicht registriert** — sie kommt mit dem Faltenplan-Abbild
(Plan-Punkt 7, TB-101; die Nummer TB-100 aus 25c ist nie ausgelöst worden) —
offen, 42.6. Marke bei 33.3.

**F5 (e) — Ersatzmodule der Regelbetrieb-Wächter; Gegenprobe über alle
`__main__`-Stellen** · Art: Tatsachennotiz und Registertext · Quelle: 25c
Abschnitt 4 (3)(a)

> **(a) Die Modus-Abfrage an den 14 Stellen selbst — in Ordnung, mit einer Tatsachennotiz und einer Gegenprobe.** Das Verfahren zählt keine Zeilen; es verlangt, dass es einen Resolver gibt und keinen Fallback. Vierzehn Aufrufe derselben Funktion (`paths.selektionsmodus()`) sind kein zweiter Ort für einen Wert — der Wert lebt in `paths.py`. **Der eigentliche Befund ist der, den ihr gefunden habt:** Drei Regelbetrieb-Werkzeuge (`kurven_lauf.py`, `determinismus_lauf.py`, `messung_primaerschluessel.py`) ersetzen `strategy_paths` in `sys.modules` durch ein Teilmodul. Das ist im Regelbetrieb Handwerk mit Live-Freigabe; **im Laufbereich wäre es ein zweiter Resolver.** Regel daraus, klein: Ein Werkzeug, das den Resolver-Nachbarn austauscht, endet unter dem Modus mit 2, bevor es das tut — dann kann es nie in den Laufbereich geraten. Tatsachennotiz zu den drei Dateien; ob ihr sie ändert, ist Live-Freigabe. **Gegenprobe zu den 14 Stellen:** eine Prüfung, dass jede `__main__`-Stelle im Laufbereich die Abfrage trägt — sonst fehlt sie beim fünfzehnten Skript still (dieselbe Kopplung wie `G6`). Handwerk.

**Stand, gemessen:** Die drei Werkzeuge ersetzen `strategy_paths` weiter in
`sys.modules` (`shared/kurven_lauf.py:129`, `shared/determinismus_lauf.py:162`,
`research/zuteilungskaskade/messung_primaerschluessel.py:119`; G3) —
unverändert, Betreiber 25.09.2026, 18:09: vorerst nur Notiz. ⚠️ **Die Regel
„endet unter dem Modus mit 2, bevor es das tut" ist an ihnen nicht umgesetzt**
(Live-Freigabe). Die Gegenprobe ist gebaut: `shared/test_main_gegenprobe.py`
(TB-107, `9827a3e`), liest die Liste aus
`docs/belege/TB-107/f1_laufbereich_vereinigung.txt`, 14 Datenstellen, alle mit
Abfrage, 7/7.

**F6 (f) — `getattr`-Ersatz in `strategy_paths.py`: ein Rückfall, entfernt** ·
Art: Tatsachennotiz · Quelle: 25c Abschnitt 4 (3)(b)

> **(b) `getattr(paths, "selektionsmodus", None)` — ja, ein Rückfall der Form nach; entfernen.** Eure Neigung ist richtig, und der Grund ist stärker, als ihr ihn nennt: Fehlt dem Nachbarn die Funktion, kann `strategy_paths.py` **nicht wissen**, ob der Modus an ist — und „dann Regelbetrieb" ist eine Annahme über genau die Frage, die der Modus beantwortet. Ein Nachbar ohne die Funktion ist kein Nachbar; das ist 19 (gespaltener Baum) in kleiner Form. Also: direkter Aufruf, ohne Modus wie mit Modus, und die zwei Proben bekommen ein `paths`, das die Funktion trägt. Dass `_resolver_ist_nachbar()` das echte `paths.py` zusichert, macht den Zweig unerreichbar, nicht zulässig — euer Zitat aus 25b trifft.

**Stand, gemessen:** entfernt in TB-107 (`5cfe472`): `_im_selektionsmodus()`
ruft `paths.selektionsmodus()` direkt (`shared/strategy_paths.py` Z. 122); ohne
Modus 101 Aufrufer in 9 Bots, Pfade und Ordner vorher = nachher. ⚠️
**Nebenwirkung:** `research/resolver_selektion/pfadvergleich.py` (nicht
freigegeben, unverändert) endet seitdem mit rc 1 statt 0 — Frage 25e (3), 42.6.

**F7 (g) — Klasse (ii) umfasst Interpreter-Caches als Muster** · Art:
Registertext (Ergänzung zu 25a (A) (ii)) · Quelle: 25c Abschnitt 4 (4)(a) ·
ergänzt 42.1 (D6)

> **(a) Bytecode-Caches — Klasse (ii), Umgebung.** Der Interpreter schreibt sie, nicht der Lauf; ihr Inhalt ist aus dem registrierten Code abgeleitet und keine Eingabe; sie liegen ausserhalb Repo und Snapshot. In der Umgebungsliste stehen sie als **Muster** (`~/Library/Caches/com.apple.python/<wurzel>/…`), nicht als Pfade — der Klonpfad wechselt. Zwei Bedingungen, damit (ii) nicht zur Hintertür wird: Ein `__pycache__` **im Repo** ist nur zulässig, wenn es git-ignoriert ist und nicht unter `snapshots/` liegt (im Klon war `--ignored` leer — gemessen, gut); und ein Cache ist nie Eingabe im Sinn von 5e — der Lese-Audit führt `.pyc`-Zugriffe unter (ii), nicht unter (i).

**F8 (h) — registrierte Protokolle als eigene Zeile in (iii); Ausnahme von 19**
· Art: Registertext (Ergänzung zu 25a (A) (iii)) · Quelle: 25c Abschnitt 4
(4)(b) · ergänzt 42.1 (D6)

> **Ergänzung zu 25a (A) (iii) — registrierte Protokolle:** Zulässige Schreibziele eines Modus-Laufs sind `--ziel`, Belegpfade, Zwischenablagen nach (iv) und **registrierte Protokolle** — heute genau eines: `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl` (10.1). Ein registriertes Protokoll ist append-only: Die Schreibregel 36.1 gilt in Anhängeform — nie kürzen, nie umschreiben, nie neu anlegen, wenn es existiert; seine Unversehrtheit prüft der Kettenhash (10.1), und `--pruefen` liest es als registrierte Eingabe (i). **Sein Ordner wird nicht angelegt:** Fehlt der registrierte Ort, endet `anhaengen()` mit 2 — ein fehlender Ort ist ein Baum, der nicht der registrierte ist, und ein `makedirs` wäre ein Fallback für genau diese Feststellung. **Ausnahme von 19:** Registrierte Protokolle sind von der Sauberkeitsprüfung des Arbeitsbaums ausgenommen wie `data/` (19), weil sie planmässig während des Laufs wachsen; die Ausnahme ist auf die namentlich registrierten Pfade beschränkt, und der Kettenhash ersetzt dort die Sauberkeit.

*Seine Quelle des Grundes, zeichengleich:*

> *Quelle des Grundes:* 10.1 (das Protokoll ist der Ort der Läufe, append-only, Kettenhash), 38.3 (es entsteht mit dem Erzeuger), 19 (die `data/`-Ausnahme mit ihrem Grund: eine Datei, die planmässig zwischen Läufen wechselt, darf die Startprüfung nicht auslösen). Kein Ergebnis. *Warum die Ausnahme jetzt und nicht später:* Sobald 19 auf den Laufbereich erweitert ist, liegt das Protokoll unter einem geprüften Pfad — der zweite Lauf würde an der Spur des ersten scheitern. Der 19-Auftrag braucht diese Zeile, bevor er beginnt.

> **Zu `makedirs` in `anhaengen()`:** Der Ordner `ergebnisse/` trägt versionierte Dateien und existiert in jedem Klon; das `makedirs` ist tot — und geht mit derselben Öffnung (2 (a)) heraus, weil eine tote Zeile mit Fallback-Form dieselbe Klasse ist wie `getattr` in (3)(b).

⭐⭐ **Reihenfolge, wie Fable sie verlangt:** Die Ausnahme von 19 steht **mit
diesem Eintrag im Register, vor dem Auftrag, der 19 auf den Laufbereich
erweitert** (42.2, E2). Der Auftrag zur Erweiterung von 19 kann sich auf F8
stützen.

⚠️ **Das gehört auch zu 10.1** (das Protokoll ist dort registriert); nach 41.0
steht dort keine Marke — die Notiz steht hier und bei 19.

**Stand, gemessen:** Ordner-Regel umgesetzt in TB-106 (`5791b4c`: kein
`makedirs`, fehlender Ordner ⇒ 2). `herkunft_protokoll.jsonl` **existiert
nicht** (TB-108, `a3_stand.txt` (2)) und wurde nicht angelegt.

> ⭐ **Vollzogen, siehe 44.2 (44-7; TB-112 `9d711dc`, TB-113, 26.09.2026):**
> Die Ausnahme von 19 steht als `REGISTRIERTE_PROTOKOLLE` (genau
> `herkunft_protokoll.jsonl`) in `shared/paths.py` und wirkt als
> `:(exclude)` in der Sauberkeitsprüfung. Das Protokoll existiert weiter
> nicht. Eintrag und Stand oben bleiben zeichengleich.

### 42.4 Tatsachennotizen aus TB-103 bis TB-107

*Eigene Fassung der Sitzungen, gemessen; kein Fable-Wortlaut.* Belege je Zeile
im genannten Ergebnisdokument.

| | Tatsache | Ergebnisdokument, Commit |
|---|---|---|
| G1 | **11.1 geschlossen:** `regimewache.pruefe_einbau()` 3 von 3 (heute nachgemessen: `vollstaendig: True`); ohne BTCUSDT bricht jede der drei Stellen mit `RegimefilterFehlt` ab. **Vorher** rechnete `t3_supertrend` ohne BTCUSDT still weiter, mit anderem Trade-Hash — der Determinismus-Befund, mit dem 11.1 begründet ist, gemessen. **11.2 und 11.3 offen** (TB-30b) | `ERGEBNIS_TB-105` A1, B; `f524327` |
| G2 | Rückfall (c): 14 × „Keine Daten gefunden" in `__main__` unter dem Modus rc 2, ohne Modus unverändert; Rückfall (a): `symbols_config.py` unter dem Modus rc 2 bei leerer oder fehlender Liste | `ERGEBNIS_TB-105` C, D; `f65c344` |
| G3 | Ersatzmodule für `strategy_paths` in `shared/kurven_lauf.py`, `shared/determinismus_lauf.py`, `research/zuteilungskaskade/messung_primaerschluessel.py` (F5) | `ERGEBNIS_TB-105` Abschnitt 5, Befund 1 |
| G4 | TB-106: keine der Ersatzwert-Stellen wird von der registrierten Eingabe erreicht (A8-Tabelle je Stelle); `benchmark.py::nachschlagen()` ist eine Rechenregel (Grenzwert 0), kein Ersatzwert, unverändert; `register()` `57ec6573…` ⇒ `0ece95e2…`; Abbild `40ffe18d…`; Datenstand der Kette im Modus `d9449faf…` = registrierter Datenstand | `ERGEBNIS_TB-106` A, E, F; `f22f91e` |
| G5 | `auswertung.Abbruch` ist `SystemExit` ohne eigenen Wert und endet mit **1** (Vertragsbruch der Rohergebnisse) — ob 1 oder 2, ist Frage 25d (4) | `ERGEBNIS_TB-106` A10 |
| G6 | `TB30A_BASE_DIR` wirkt in `herkunft.py:51` auch unter gesetzten Modus-Variablen, auf Commit und Registerdatei — Frage 25d (3) | `ERGEBNIS_TB-106` A11 |
| G7 | `registerbericht.py --pruefen` war schon vor TB-106 rot: der ERZEUGT-Block in Abschnitt 3 ist veraltet (39.1) | `ERGEBNIS_TB-106` Befund 2 |
| G8 | Laufbereich 81 Module am Stand `a79e715`, neu gegenüber TB-104 nur `shared/regimewache.py`; Liste `docs/belege/TB-107/f1_laufbereich_vereinigung.txt` (E5) | `ERGEBNIS_TB-107` F1; `9827a3e` |
| G9 | `elliott_wave` trägt `MIN_HISTORY_HOURS`, die acht übrigen `MIN_HISTORY_DAYS`, je genau einmal in `multi_symbol_optimise.py` (heute nachgemessen) | `ERGEBNIS_TB-107` A2 |
| G10 | Die Benchmark-Tabelle `64fb2912f1a2ffb02a36834857fe9a91529b7517a8a7185f5fd7b11642f873b7` ist durch TB-103 bis TB-107 **unverändert**; im Modus bytegleich reproduziert in TB-104 (zweimal), TB-105, TB-106 und TB-107 (je Repo und frischer Klon), ohne Modus ebenso — als Nachweis nach 41.2 (B4) weiter **2** | `ERGEBNIS_TB-104` C5 bis `ERGEBNIS_TB-107` G |
| — | ⚠️ **`f5fdb53` (TB-107 Block C, `faltenplan_neun.py`) ist vor Fables Antwort auf 25d gebaut** und als eigener Commit revertierbar (`git revert f5fdb53` nimmt Code und Probendatei zurück) | `ERGEBNIS_TB-107` Abschnitt 3 |

### 42.5 ⭐⭐ Tatsachennotizen zu 37.3 — die Hash-Übergänge seit 39.5

37.3 verlangt für jeden planmässigen Befund vor dem Tag: Auftrag, Freigabe,
alter und neuer Hash. Gemessen in TB-108 aus der Historie
(`git show <commit>~1:<pfad>` bzw. `<commit>:<pfad>`) für **jeden Pfad des
Abbilds `40ffe18d…`** (vierzehn Punkte und Gruppe „eingefroren") seit
`4faef05` (Ende TB-94, Stand von 39.5); Beleg
`docs/belege/TB-108/c_hashuebergaenge.txt`. Freigaben aus den
Ergebnisdokumenten nachgelesen.

| Datei | alt → neu | Auftrag / Commit | Freigabe | Punkte |
|---|---|---|---|---|
| `research/vorregistrierung/messgroessen.py` | `623f8d771ffd5ae9dc1b979fbe383c85268371ba4f1dfeff055379662be41f25` → `59b396e76af33dfc5549c7a40032d44963b02d3305bf4bf9e721b06001d0301c` | TB-103, `ae136fd` | Betreiber 24.09.2026, 22:52 | ⚠️ **kein Punkt, aber `EINGEFROREN`** — nach 39.7 (23c) gesperrt |
| `research/vorregistrierung/benchmark.py` | `d6bdd55805344da09b6b43d791267b43c9702687fc1c7cdbad1473079443e061` → `4c923cd907c6aa9b14fd035fd775ced00bfcaff0795288dc4b1ccd48d19fc5b8` | TB-104, `572d725` | Betreiber 25.09.2026, 07:52 | 4 und 6; `EINGEFROREN` |
| `research/vorregistrierung/faltenplan.py` | `7aa0b8ccf5619a21d5f082f68d81cb412f98ae9c9724e799da8b48dce7498cfb` → `d57fe9c977e572e1d344971913e3acbb1cd765d2bf145b52cefab69d75e10f41` | TB-104, `f334a7b` | Betreiber 25.09.2026, 07:52 | 2; `EINGEFROREN` |
| `research/vorregistrierung/faltenplan.py` | `d57fe9c977e572e1d344971913e3acbb1cd765d2bf145b52cefab69d75e10f41` → `63dafeb44e027cb5d93ac19cddfc7d4e98b468cece116512c2b3f1601bd4a4c7` | TB-106, `abeca36` | Betreiber 25.09.2026, 18:09 | 2; `EINGEFROREN` |
| `research/vorregistrierung/benchmark.py` | `4c923cd907c6aa9b14fd035fd775ced00bfcaff0795288dc4b1ccd48d19fc5b8` → `aeeec9b89bdadd1b2dc2be76b722dc90c328c9482014bbbbfcabd78edccae219` | TB-106, `a08c13a` | Betreiber 25.09.2026, 18:09 | 4 und 6; `EINGEFROREN` |
| `research/vorregistrierung/auswertung.py` | `c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062` → `83c6bc3c9b683d0bfd9d8c445492060f93759a551d0dcf329b2bd21b0f1cc5a1` | TB-106, `5cc1de4` | Betreiber 25.09.2026, 18:09 | 3, 5 und 14; `EINGEFROREN` |
| `research/vorregistrierung/herkunft.py` | `56a1c2e1514385acd26c3432bd111f3588846c80d173a4d4a471ecae723fb502` → `351f24c2d6a3a512dc1eb1a80b536b99d47c266db38f7dd93b9d1c0199397eef` | TB-106, `5791b4c` (42.3, F2) | Betreiber 25.09.2026, 18:09 | 11 und 12 |
| `research/vorregistrierung/registerbericht.py` | `dace1b01826fa6a999beb9a15a8eda41a4e0c97dec584e451cfc0d9b26daac01` → `de35a5a09d103def310d473170d6e638cfd1f1a24f46f7b1d1e033a674134db7` | TB-104, `f334a7b` | Betreiber 25.09.2026, 09:10:49 (Zusatzfreigabe) | ⭐ auf keinem Punkt — nur Tatsachennotiz |
| `research/vorregistrierung/registerbericht.py` | `de35a5a09d103def310d473170d6e638cfd1f1a24f46f7b1d1e033a674134db7` → `74a22daec99dd4ba2057206fca22596bdc1d3bd7de5dbf465c14c44bb952eb89` | TB-106, `abeca36` | Betreiber 25.09.2026, 18:09 | ⭐ auf keinem Punkt |

**Unverändert seit `4faef05`:** `registerdaten.py` (Punkt 1), `kennzahlen.py`,
`pruefe_grenzsaetze.py`, `shared/zuteilung.py` (Punkt 10), beide
Universumsdateien (Punkt 8) und alle Ergebnisdateien unter `ergebnisse/`, die
auf der Sperrliste oder in `EINGEFROREN` stehen. `test_vorregistrierung.py`
(auf keinem Punkt) hat sich in TB-95, TB-97, TB-103, TB-104 (zweimal) und
TB-106 bewegt; die Kette steht im Beleg.

**Die Abbilder, die diese Übergänge schliessen** (37.3: neues Abbild unter neuem
Namen, das alte bleibt): `sperrliste_abbild_2026-09-23.json` `2f23f76c…` (39.9)
→ **`sperrliste_abbild_2026-09-25.json`
`cb4eb1b4cf998efcded95acd4d712bb3a0856722489a80ce10bfce511eeb5f89`** (TB-104,
`d96b352`; erzeugt an `f334a7b`, das erste Abbild mit der Gruppe „eingefroren",
das `messgroessen.py` mit dem neuen Hash führt) → **`sperrliste_abbild_2026-09-25b.json`
`40ffe18d6a6345d1ab88aa993535cfb10264d8cf2e02e804406bbe85236642c8`** (TB-106,
`e1e6652`; erzeugt an `5791b4c`). Sonde gegen `40ffe18d…` am Eingang von TB-108:
Pfad-Bestandteile 25/0/0, Prüfung (ii) 0 (`docs/belege/TB-108/0_sonde_vorher.txt`).

⚠️ **Zu `messgroessen.py`:** Der Auftrag TB-108 nannte für diese Notiz TB-104
und TB-106. Gemessen ist ein dritter Übergang an einem gesperrten Pfad, TB-103
(`ae136fd`) — `messgroessen.py` steht auf keinem Punkt des Abschnitts 10, aber
in `herkunft.py::EINGEFROREN`, und nach Fables Präzisierung zu 36.1 (1) (39.7)
ist jeder Pfad gesperrt, dessen Hash am Tag bezeugt wird. Freigegeben war die
Änderung (TB-103, Kopf des Ergebnisses: „`paths.py`, `messgroessen.py` und ihre
Tests"); ihr Ergebnis nennt die Berührung als A8 (a). **Eingetragen ist, was
gemessen ist.**

**`herkunft.register()` über die Abschnitt-0-Menge** (Registerdatei plus
`EINGEFROREN`), nachgebaut je Commit aus der Historie (Probe: am Eingang von
TB-108 gleich dem gemessenen Wert):

| Stand | `register()` |
|---|---|
| `4faef05` (Ende TB-94) | `f63c181bd46e5ae481b34bbdddd9178f42255214f892cc73468948c26f54ebc5` |
| `d0dc890` (TB-96, Register 40) | `89f0ab5f9be1cee9cc8978ac9e6012623a6bc922775c658debf9f84c957c61cc` |
| `ae136fd` (TB-103, `messgroessen.py`) | `becfa3c9430946a1021e7a990e5804290cb8f0520e5355a8f2e077f9a7678476` |
| `572d725` (TB-104, `benchmark.py`) | `cca9bb787629136dc2d742b09be9f1e18e4fa3964324a505be295dac1384f795` |
| `f334a7b` (TB-104, `faltenplan.py`) | `57ec6573eb44f18bccaa461da41ac0b835ba1afa1446ef27b4c3409ead56e46e` |
| `abeca36` (TB-106, `faltenplan.py`) | `f42d6d84515aba19765a2d25cb542afeea8dec81433eb5d79d43f3d6a9df1561` |
| `a08c13a` (TB-106, `benchmark.py`) | `cad1495b4fc42f156a15a92c7cd8be7cfe9a7bae1dc7c443d6303729dc4ce107` |
| `5cc1de4` (TB-106, `auswertung.py`) bis zum Eingang von TB-108 | `0ece95e2fd4f5bd2787ea40f6a12988aadb0a414c5132553522b55000c6052d7` |

⚠️ **Die letzte Zeile, und warum der neue Wert hier nicht stehen kann:** Mit
diesem Eintrag ändert sich `register()` zwangsläufig, weil die Registerdatei
selbst Teil der Menge ist. Vorher: **`0ece95e2fd4f5bd2787ea40f6a12988aadb0a414c5132553522b55000c6052d7`**.
Der Wert **nach** diesem Eintrag hängt vom Text dieses Eintrags ab und kann
deshalb nicht in ihm stehen; er ist nach dem Commit gemessen und steht voll in
`docs/ERGEBNIS_TB-108_register_41_42.md` und
`docs/belege/TB-108/h1_hashes_nachher.txt`.

### 42.6 Was offen bleibt

| | Sache | wohin |
|---|---|---|
| (1) | **Fable 25d** (vier Fragen: die Kopie in `faltenplan_neun.py` — `f5fdb53` gebaut, revertierbar; die Prüfansicht von `herkunft.py` unter dem Modus; `TB30A_BASE_DIR` unter dem Modus (G6); `auswertung.Abbruch` 1 oder 2 (G5)) | Abschnitt 43 |
| (2) | **Fable 25e** (drei Fragen: `tb40_faltenplan_*`/`tb40_proben_*` (E1); `trades.empty ⇒ exit()`; `pfadvergleich.py` rc 1 (F6)) | Abschnitt 43 |
| (3) | **Fable 25f** (Gesamtanalyse) | Abschnitt 43 |
| (4) | **Die Erweiterung von 19 auf den Laufbereich** (42.2, E2) — Tag-Vorbedingung (25c 2 (d)). Die Ausnahme für registrierte Protokolle, die Fable **vorher** im Register verlangt (25c (h)), steht jetzt in 42.3 (F8) | eigener Auftrag |
| (5) | **Der Erzeuger auf dem Signalpfad** (41.1 A12, 41.2 B3/B6/B7) — und mit ihm die neun Listen, der Deckel von `t3_supertrend` (41.3 C2), die Donchian-Eingabe, `messgroessen.json` neu und der Benchmark-Nachweis mit beiden Teilen (41.2 B4) | Plan-Punkte 3 und 5 |
| ↳ (5) | ⭐ **Abnahmebedingungen des Erzeugers: siehe 45.5** (Fable 26a R5, TB-114, 26.09.2026); die Zeile oben bleibt zeichengleich | 45.5 |
| (6) | **Das Faltenplan-Abbild samt Erzeugerkette des Trockenlaufs** (33.3; 42.3 F4) | Plan-Punkt 7, TB-101 |
| (7) | **Die Feldliste des gerechneten Plans als Registertext** — je Schlüssel die begründende Registerstelle; die registrierte Abbildung (42.2, E3) | mit (6) |
| (8) | **H6 eigenständig oder als Paar gezählt**; danach ggf. „sieben" berichtigen (41.1, A4) | vor dem Tag |
| (9) | **Ladeprotokoll-Teil (4)** — Zeilenzahl der Universumsdatei und Quelle der Liste (42.1, D3/D7) | Handwerk mit Freigabe |
| (10) | Der Laufbereich und die Liste der Lauf-Typen **am Tag-Commit** (42.2, E5); der Trockenlauf aller neun am Tag-Commit (42.1, D4) | Tag |
| (11) | Die Regel „Resolver-Nachbar austauschen ⇒ unter dem Modus 2" an den drei Werkzeugen (42.3, F5) | Live-Freigabe |
| (12) | Die zweite Deutungsstelle der Rasterbedingung `registerdaten.py:605` (42.3, F1) und die tote Konstante `MINDESTTRAINING_JAHRE` (42.2, E4) | 40.8 (h) |

> ⭐ **Beantwortet (TB-110, 26.09.2026):** (1) Fable 25d in **43.1**, (2) Fable
> 25e in **43.2** — dazu eine vorläufige Berichtigung des steuernden Chats an
> 25e (3) in **43.3**. (3) Fable 25f bleibt offen (43.5 (9)). Die Tabelle oben
> bleibt zeichengleich.

### 42.7 Was hier ausdrücklich NICHT getan wurde

| | | gehört zu |
|---|---|---|
| ⛔ | **Keine `.py` geändert, nichts gerechnet** — auch wo ein Eintrag eine Codeänderung nahelegt (H6, Ladeprotokoll, Wächter-Ersatzmodule, `bot_lauf.py`-Kopf) | 42.6 |
| ⛔ | **Kein neues Abbild** — keine Sperrlistendatei hat sich bewegt; das gültige Abbild bleibt `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`), Sonde vorher und nachher gleich (`0_sonde_vorher.txt`, `d3_sonde_nachher.txt`) | — |
| ⛔ | **Kein alter Registersatz umgeschrieben** — Marken sind neue Zeilen, nichts entfernt | — |
| ⛔ | **Keine Marke in Abschnitt 10** (Listentext Z. 868–981, geprüft von der Sonde, Prüfung (ii)); was dorthin gehörte (F3: Schlusssatz zu Abschnitt 11; F8: 10.1), steht hier | — |
| ⛔ | **Nichts aus 25d, 25e, 25f** | Abschnitt 43 |
| ⭐ | **Sichtschutz 27.1:** keine Ergebnisgrösse des Selektionsraums; Feldnamen ohne Werte | — |

**Die Marken am alten Ort** (je neue Zeilen, der alte Satz zeichengleich): 5.1
Nr. 4 · 5.4 · 6 · 11 (am Ende, in 11.3) · 12 · 15.4 (2d, Tabelle des Deckels)
· 16.6 · 19 (zweimal: unter dem Registertext 5e und unter der Tabelle der
Startprüfungen) · 23.5 · 33.3 · 35.4 · 36.5 · 37.3 · 37.4 · 39.6 · 39.7 · 39.8
· 40.6 · 40.7.

*Diese zwei Abschnitte sind rein additiv: Sie tragen die entschiedenen Einträge
des Verfahrensprüfers aus sechs Antworten zeichengleich ein, beide Fassungen
jeder Kette mit Verweis, die Tatsachen aus fünf Aufträgen und die
Hash-Übergänge seit 39.5 — und entfernen nichts. Gebaut und gerechnet wird
nichts.*

