<!-- TEILKOPIE 3/3 der Datei REGISTER_KOPIE_2026-09-24.md -->
# Registerkopie 24.09.2026, Teil 3 von 3: Abschnitte 37 bis 40

⚠️ **KOPIE einer KOPIE, in drei Teile geschnitten**, damit sie in einem Stück lesbar ist (Fable 24d: das Lesewerkzeug liefert höchstens 262 144 Bytes). Geschnitten wurde nur an Abschnittsgrenzen (`## <Nummer>`), nichts wurde verändert.

| | |
|---|---|
| Quelle | `docs/projektfuehrung/REGISTER_KOPIE_2026-09-24.md`, 552 130 Bytes, SHA-256 `7e70e0f055493efbd8e00e8d8f1932b82d989022ce47c43ac05e7dd016c2473f` |
| Dieser Teil | Bytes 419718 bis 552130 der Quelle (132412 Bytes), SHA-256 `7d86131f766714fb27e1bafd02c54d2f82d199da7a918e631b0da273aa469126` |
| Register | `docs/VORREGISTRIERUNG_neuselektion.md`, Stand laut Kopf der Kopie; bei Abweichung gilt die Quelle |
| Geschnitten | 24.09.2026, 23:35, steuernder Chat; die drei Teile ohne diesen Kopf aneinandergehängt sind bytegleich zur Quelle |

---

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

### 40.8 Beschlossen, nicht ausgeführt — was TB-97, TB-98, TB-100 und TB-101 tun

Damit das Register sagt, was offen ist und warum:

| | Sache | Auftrag |
|---|---|---|
| (a) | `F4`: `<=` → `<`, Probe mit Mehrheit wie `H3`, Gegenprobe „leere Menge ⇒ scheitert" | TB-97 |
| (b) | Die vier Literale (40.4) bauartgleich umstellen, nach Fables Regel (Zitat unten). Für 4.4: Tatsachennotiz, dass seine Beispieljahre der Stand vom 14.09. sind, und die Prüfung liest den **heutigen** Plan | TB-97 |
| (c) | Gegenproben für **alle acht** Mutationsproben, mit Tatsachennotiz (40.7) | TB-97 |
| (d) | Sonde: **getrennte Schlusszeilen** — „Pfad-Bestandteile: n geprüft, davon 0 / 1 / 2" und „Regel-Bestandteile: m nicht prüfbar (2), je mit Verweis auf die Tatsachennotiz". Der Gesamtwert bleibt, wie 36.5 ihn definiert | TB-97 |
| (e) | ⚠️ **Befund:** Die Gruppe „bestimmt" steht **fest verdrahtet** in `shared/sperrlistensonde.py` (`BESTIMMT_NICHT_EINGETRAGEN`, 39.3). Sie liest künftig **alle drei Gruppen** (Abschnitt 10, „bestimmt", `EINGEFROREN`) **aus dem Abbild**; Gegenprobe: Abbild mit erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn | TB-97 |
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
