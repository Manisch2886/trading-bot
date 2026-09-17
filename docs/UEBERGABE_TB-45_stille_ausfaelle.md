# Übergabe TB-45 — Stille Ausfälle

**Cloud-Sitzung, 17.09.2026. Zweig `claude/new-session-l4l5k1`, frisch von
`main` (`97aea88`).**
**Umgebung: Python 3.11.15, pandas 2.3.3, numpy 2.0.2 — bewusst auf die
Mac-Fassungen gesetzt. Zusätzlich gemessen auf 3.9.23, 3.10.20, 3.12.3,
3.13.12.**

---

## Die drei Dinge zuerst

### 1. Welcher Test welchen Befund auf dem unveränderten Stand findet

Jeder der fünf Befunde wurde **zuerst reproduziert, dann behoben**, und jeder
Test wurde gegen den unveränderten Stand aus `origin/main` laufen gelassen.

| Befund | Der Test, der ihn findet | Auf dem unveränderten Stand |
|---|---|---|
| **Teil 1** `shared/test_kursdaten.py` meldet bei git-Fehler still „bestanden" | `shared/test_stille_ausfaelle.py`, Abschnitt 1 | ⚠️ **3 Prüfungen rot** — u. a. `Lage B (origin/main fehlt, rc 128) - ROT` schlägt fehl |
| **Teil 2** `dashboard/test_portfolio_sicht.py` behandelt Fehler als Erfolg | dito | ⚠️ **3 Prüfungen rot** |
| *(beide zusammen)* | dito, Abschnitt 2 (Gegenprobe) | der alte Stand meldet in Lage B **28 bzw. 6 grüne Prüfungen, ohne etwas gemessen zu haben** |
| **Teil 3** `_ist_geraet` heißt nicht, was es tut | `research/universum_trockenlauf/…`, Teil N | ⚠️ **5 Prüfungen rot**, darunter `N5 vorhanden: der makedirs-Versuch wird aufgezeichnet` |
| **Teil 4** leerer Kursrahmen beendet zwei Bots hart | `shared/test_leeres_symbol.py` | ⚠️ **23 von 35, 12 rot**, darunter `elliott_wave: der Lauf kommt trotz des leeren Symbols durch` |
| **Teil 5** `fromisoformat` | `research/fromisoformat_registerfrage/messung.py` | — misst und berichtet, **ändert nichts** |

**Gemessen, nicht behauptet:**

```
$ git checkout origin/main -- shared/test_kursdaten.py dashboard/test_portfolio_sicht.py
$ python3 shared/test_stille_ausfaelle.py
  [FEHLER] test_kursdaten.py: Lage B (origin/main fehlt, rc 128) - ROT   []
  [FEHLER] test_kursdaten.py: Lage B nennt den gescheiterten Vergleich beim Namen   []
  [FEHLER] test_kursdaten.py: Lage B meldet nichts faelschlich als unveraendert   28 gruene statt 28
  … dasselbe für test_portfolio_sicht.py
```

```
$ git checkout origin/main -- strategies/elliott_wave/… strategies/elliott_wave_stocks/…
$ python3 shared/test_leeres_symbol.py
23 von 35 Pruefungen bestanden, 12 fehlgeschlagen.
  - elliott_wave: der Lauf kommt trotz des leeren Symbols durch        <- der ganze Lauf endet
  - elliott_wave_stocks: der Lauf kommt trotz des leeren Symbols durch
```

### 2. Ob die Negativ-Prüfungen unverändert grün bleiben

**Ja — und das ist getrennt geprüft, in beide Richtungen.**

Die Unterscheidung aus TB-43 (`daten_unberuehrt` gegen Parameter-Prüfung) war
der Kern von Teil 1. **Das Ergebnis der verlangten Sortierung, ehrlich
berichtet:**

> ⭐ **In `shared/test_kursdaten.py` sind ALLE FÜNF git-gestützten Prüfungen von
> der `daten_unberuehrt`-Sorte.** Es gibt dort keine Prüfung der zweiten Sorte.

Auch die beiden Schleifen über `forward_test.py` und `live_params.py` gehören
zur ersten Sorte: Läuft keine Runde, weil die Datei unverändert ist, dann ist
damit auch kein Handelsparameter verändert — **der Nachweis trägt.** Ein
leerer Diff aus einem *gelungenen* Aufruf bleibt deshalb grün.

**Verschärft wurde ausschließlich der FEHLGESCHLAGENE Aufruf.** Wer „leer =
immer Fehler" geschrieben hätte, hätte alle fünf kaputtgemacht.

Der Nachweis steht als **Lage A** in `shared/test_stille_ausfaelle.py` und ist
auf dem alten wie auf dem neuen Stand grün:

```
[OK ] test_kursdaten.py: Lage A (origin/main da, nichts veraendert) - gruen   29 Pruefungen
[OK ] test_portfolio_sicht.py: Lage A (origin/main da, nichts veraendert) - gruen   7 Pruefungen
```

Und **Lage C** zeigt, dass die Wache weiter beißt: `STOP_LOSS_PCT = 4.0 → 9.9`
in `t3_supertrend/live_params.py` wird gefunden.

### 3. Was an `fromisoformat` tatsächlich ankommt

**Mitgeschrieben, nicht angenommen** — `dt.datetime.fromisoformat` wurde im
Namensraum von `entscheidungskerze` ersetzt, danach lief `lade()` für fünf
echte Symbole beider Märkte samt Rückfallweg.

| | |
|---|---|
| Aufrufe | **4** |
| **verschiedene Werte** | **genau 1** |
| Der Wert | **`'2026-09-16T00:00:00'`**, Typ `str` |
| Woher | Der Code baut ihn selbst: `f"{tag}T00:00:00"`, `tag` = letzter NYSE-Handelstag aus dem Börsenkalender |

⭐ **Zwei Dinge, die vorher nicht festgehalten waren:**

1. **Die Zeitstempel der Kursdateien kommen hier gar nicht an.** Sie gehen
   über `pandas` und `abrufschutz.oeffnungszeiten_ms`. Der Datenordner-Umbau
   berührt damit **nicht** diesen Weg, sondern nur den des Börsenkalenders.
2. **Der Krypto-Pfad erreicht `fromisoformat` überhaupt nicht.** Betroffen
   sind **vier von neun Bots**, nicht neun.

Einzelheiten, Katalog und Registervorlage:
[`research/fromisoformat_registerfrage/BERICHT.md`](../research/fromisoformat_registerfrage/BERICHT.md).

---

## Was geändert wurde

| Datei | Was | Zeilen |
|---|---|---|
| `shared/test_kursdaten.py` | Teil 1: neuer Helfer `_geaenderte_dateien()`, der den Rückgabewert prüft; die Prüfungen darunter werden bei einem Fehlschlag **rot** statt grün | +69 −2 |
| `dashboard/test_portfolio_sicht.py` | Teil 2: `returncode != 0` ist kein Erfolg mehr; zusätzliche Prüfung „der Vergleich kam zustande" | +23 −3 |
| `research/universum_trockenlauf/loaderlauf.py` | Teil 3: `_ist_geraet` auf `S_ISCHR`/`S_ISBLK`/`S_ISFIFO` eingeschränkt; `wach_makedirs`/`wach_mkdir` zeichnen jeden Versuch auf und werten `exist_ok` selbst aus | +60 −5 |
| `research/universum_trockenlauf/test_universum_trockenlauf.py` | B2 verschärft (nennt jetzt die Pfade statt nur den Schlüssel) + **neuer Teil N**, beide Lagen in eigenen Prozessen | +169 −8 |
| `shared/ladeprotokoll.py` | Teil 4: fünfter Grund `ohne_kursrahmen()` — der Wortlaut bleibt an **einer** Stelle | +23 −1 |
| `strategies/elliott_wave/forward_test.py` | Teil 4: leeres Symbol wird übersprungen **und gemeldet** | +19 −1 |
| `strategies/elliott_wave_stocks/forward_test.py` | dito | +19 −1 |
| `strategies/elliott_wave/zigzag_indicator.py` | Teil 4: der harte Stopp an seiner Entstehungsstelle | +34 |
| `strategies/elliott_wave_stocks/zigzag_indicator.py` | dito | +34 |

**Neu:**

* `shared/test_stille_ausfaelle.py` — Teil 1, 2 und die T38.9-Messung (27 Prüfungen)
* `shared/test_leeres_symbol.py` — Teil 4 samt Umfrage über alle neun Bots (45 Prüfungen)
* `research/fromisoformat_registerfrage/messung.py` + `BERICHT.md` — Teil 5

> ⚠️ **`shared/entscheidungskerze.py` ist unberührt** — `git diff` darauf ist
> leer. `live_params.py` ebenso, `broker/` ebenso, `data/` ebenso.
> **Datenstand vor und nach der Aufgabe: `d9449faf51bffaaa…`, 223 Dateien** —
> als Test nachgewiesen (`shared/test_stille_ausfaelle.py`, Abschnitt 4).

---

## Die Entscheidungen, mit Begründung

### T38.9 — Drei-Punkt-Form: geprüft, **nicht** übernommen

Die Aufgabe bat zu prüfen, ob `origin/main...HEAD` das Problem löst, und
**zu berichten statt zu ändern**, falls die Form hier etwas anderes bedeutet
als in `research/fib_score_stufen/test_stufen.py:244`.

**Sie bedeutet hier etwas anderes. Gemessen an einem eigens gebauten Repo:**

| Form | `main` ist weitergezogen (T38.9) | unkommittierte Änderung sichtbar |
|---|---|---|
| Zwei Punkte `origin/main` | ⚠️ **falsch rot** | ✅ ja |
| Drei Punkte `origin/main...HEAD` | ✅ still | ⚠️ **nein** |
| Zwei Punkte gegen die **Merge-Basis** | ✅ still | ✅ ja |

Die Drei-Punkt-Form vergleicht **zwei Commits**; der Arbeitsbaum kommt darin
nicht vor. In `test_stufen.py` ist das unschädlich, weil dort **direkt daneben**
ein `git status --porcelain` steht, der den Arbeitsbaum abdeckt. **In
`shared/test_kursdaten.py` gibt es diese Begleitprüfung nicht** — die
Drei-Punkt-Form allein hätte die Wache blind gemacht für genau den Fall, in dem
eine Sitzung sie benutzt: vor dem Commit.

⭐ **Der gemessene Ausweg, der beides löst:** der Vergleich gegen die
**Merge-Basis** (`git diff $(git merge-base origin/main HEAD)`). Er ist bei
T38.9 still **und** sieht den Arbeitsbaum.
⚠️ **Nicht übernommen** — er ändert, was die Wache sieht, und das war nicht
freigegeben. **Vorlage für eine eigene Aufgabe.**

Der Vorbehalt aus T43.2 ist ebenfalls gemessen: Ist der Zweig **gemergt**, ist
die Merge-Basis der eigene Commit, und **beide** Formen sehen die eigene
Änderung nicht mehr. Der Vorbehalt trifft Drei-Punkt-Form und Merge-Basis
gleichermaßen.

### Teil 3 — beide Wege geprüft, Weg 1 gewählt (mit dem Zusatz aus Weg 2)

| Weg | Was er tut | Urteil |
|---|---|---|
| **1** | `_ist_geraet` auf `S_ISCHR`/`S_ISBLK`/`S_ISFIFO` einschränken | ⭐ **gewählt** |
| **2** | den Versuch in `wach_makedirs` **vor** der Erlaubnisprüfung aufzeichnen | als Wirkung in Weg 1 enthalten |

**Warum Weg 1:** Er behebt den **Entwurfsfehler**, nicht nur dessen Symptom.
Weg 2 hätte den Beleg für B2 hergestellt und die irreführende Funktion stehen
gelassen — „und würde den nächsten in die Irre führen, der die Wache
erweitert" ist genau das, was die Aufgabe als eigentlichen Schaden benennt.
Mit Weg 1 ergibt sich die Aufzeichnung von selbst: Ein bestehendes Verzeichnis
außerhalb von `_ERLAUBT` gilt nicht mehr als „Gerät", kommt also in
`wach_makedirs` an und wird verzeichnet.

**Der Zusatz, den die Aufgabe für Weg 1 vorhergesagt hat, war nötig:**
`exist_ok` wertet `wach_makedirs` jetzt selbst aus, und `wach_mkdir` wirft
weiterhin `FileExistsError`. Sonst bekäme ein Aufrufer, der darauf baut, still
ein `None` — der Trockenlauf bildete den Betrieb an dieser Stelle nicht mehr
nach. Geprüft als `N11`/`N12`/`N13`.

**Sockets bleiben draußen.** Netzverkehr läuft über das `socket`-Modul, nicht
über `open(pfad)`; die engere Liste lässt höchstens eine Meldung zu viel zu,
nie eine zu wenig.

**B2 hing wirklich an der Umgebung — in der Cloud nachgestellt:**

```
=== ohne logs/rsi2_crypto (Cloud-Lage) ===     ok   B2 …
=== mit  logs/rsi2_crypto (Mac-Lage)   ===     FEHL B2 …
```

Nach der Reparatur ist B2 in **beiden** Lagen grün, und der volle Trockenlauf
läuft in beiden Lagen mit **356/356** durch.

⭐ **Nebenbefund beim Umbau von B2:** Die Prüfung hieß
`any("makedirs_unterdrueckt" in e …)` — sie sah nur nach, **ob der Schlüssel
da ist**. Sie nennt jetzt für jeden Bot beide erwarteten Pfade.

### Teil 4 — wo die Reparatur sitzt, und warum an zwei Stellen

1. **In der Ladeschleife beider `forward_test.py`** — `if df.empty:` →
   überspringen **und melden**, genau wie bei den sieben anderen Bots.
2. **In `calculate_zigzag` / `calculate_zigzag_with_confirmation`** — dort, wo
   der harte Stopp entstand. Damit ist er auch für Backtest und Optimierer
   weg, die dieselbe Funktion rufen.

**Der Wortlaut steht in `shared/ladeprotokoll.py`**, nicht in den Bots — dessen
erklärter Zweck ist „Ein Lauf, der ein Symbol auslässt, sagt es. Immer."
Der fünfte Grund `ohne_kursrahmen()` war nötig, weil die vier vorhandenen den
**Backtest-Lader** beschreiben (CSV); im Papierpfad kommt der Rahmen aus
`entscheidungskerze.lade` und damit aus `data/` **oder** dem Live-Abruf —
welche Quelle leer blieb, weiß das Modul nicht. `leer()` hätte im Bericht
„leere Kursdatei" behauptet, wo vielleicht der Abruf ausfiel.

**`melde()` wird bewusst nicht gerufen.** Die Summenzeile gibt es in keinem
der neun `forward_test.py`; sie hier einzuführen wäre ein struktureller
Unterschied zu den anderen sieben, den niemand bestellt hat. Die
Summenzeile bleibt dort, wo TB-42 sie hingestellt hat: in den Backtest-Ladern.

**Am Signal ändert sich nichts** — nachgewiesen, nicht zugesagt: auf echten
Kursdateien liefern beide Zigzag-Funktionen **Pivot für Pivot, Spalte für
Spalte** dasselbe wie die Fassung aus `origin/main` (84 bzw. 830 Pivots), und
die Trades der übrigen Symbole sind zwischen „mit leerem Symbol" und „ohne
dieses Symbol" **Spalte für Spalte identisch**.

---

## Die Umfrage: gibt es weitere Stellen? — Ja, eine, und sie ist eingefangen

**Alle neun Bots, am Ablauf gemessen** (`shared/test_leeres_symbol.py`,
Abschnitt 3), nicht aus dem Quelltext geschlossen:

| Bot | Ladeschleife | leeres Symbol in der Signalsuche |
|---|---|---|
| `elliott_wave` | ⚠️ **hatte keine Schranke** → `price_data` bekam den leeren Rahmen | **jetzt: übersprungen + gemeldet** |
| `elliott_wave_stocks` | dito | dito |
| **`t3_supertrend`** | ⚠️ **hat ebenfalls keine `df.empty`-Schranke** | ⭐ **`compute_indicators` bricht auf einem leeren Rahmen mit `IndexError` ab** |
| die sechs übrigen | `if df.empty: continue` | überspringen **still** |

⭐ **Der neue Befund: `t3_supertrend` überlebt aus Versehen.** Seine
Indikatorrechnung bricht bei einem leeren Rahmen ab — aber sie steht **im
`try` der Ladeschleife**, deren `except Exception` das Symbol überspringt.
Der Lauf überlebt also, und er meldet auch etwas — aber die Meldung nennt das
**Symptom** (`index 0 is out of bounds`) statt der Ursache (kein Kursrahmen).

⚠️ **Nicht repariert — das wäre eine eigene Freigabe.** Festgehalten, damit es
nicht wieder unbemerkt bleibt; der Test hält es als eigene Prüfung fest, so
dass ein *zweiter* solcher Fall sofort auffiele.

⚠️ **Und der zweite, kleinere Punkt:** Die sechs übrigen Bots überspringen ein
leeres Symbol **still**. Das widerspricht dem Satz „Ein Lauf, der ein Symbol
auslässt, sagt es. Immer." **Nicht geändert** — die Freigabe von Teil 4 gilt
ausdrücklich nur für die beiden Elliott-Bots. **Vorschlag für eine eigene,
sehr kleine Aufgabe:** dieselbe eine Zeile `_prot.ohne_kursrahmen(...)` in den
sechs übrigen Ladeschleifen.

---

## Der Basislauf

| | |
|---|---|
| `shared/test_stille_ausfaelle.py` (neu) | **27 / 27** |
| `shared/test_leeres_symbol.py` (neu) | **45 / 45** |
| `shared/test_kursdaten.py` | **88 / 88** (vorher 81/81 — die Parameter-Schleife läuft jetzt wirklich) |
| `research/universum_trockenlauf/test_universum_trockenlauf.py` | **356 / 356** (vorher 332/332), in **beiden** Ordner-Lagen |
| `dashboard/test_portfolio_sicht.py` | **91 / 91** |

⚠️ **Korrektur an der Liste „bekannt rot" aus der Aufgabenstellung** — in der
Cloud gemessen, mit Angabe des Rechners (Regel aus `docs/UMGEBUNGEN.md`):

| Test | laut Aufgabe | **in dieser Cloud gemessen** |
|---|---|---|
| `dashboard/test_portfolio_sicht.py` | „bekannt rot, **beide**" | ⚠️ **grün, 91/91** — er wird auf dem Mac rot, weil dort die Live-Datenbanken liegen |
| `dashboard/test_dashboard.py` | „in der Cloud rot" (ohne `node`: 780/780) | ⚠️ **grün, 784/784** — `node` ist in dieser Cloud vorhanden |

**Vier Tests verlangen ein Argument** und geben ohne eines Rückgabewert 1 —
das ist kein roter Test, sondern eine Nutzungsmeldung:
`research/drawdown_reihenfolge/test_drawdown.py`,
`research/elliott_wave_params/test_params.py`,
`research/fib_score_stufen/test_stufen.py`,
`research/hrp_portfolio/test_hrp_core.py` (dort fehlt zusätzlich `scipy`).

⚠️ **Zwei Untersuchungstests haben eine Wache `git diff HEAD -- strategies/`**
(`research/pnl_2025_fixed_size/test_pnl.py:139`,
`research/elliott_wave_params/test_params.py:221`). Sie werden rot, solange
Änderungen an Bot-Dateien **unkommittiert** im Arbeitsbaum liegen.
**Nachgemessen: nach dem Commit sind beide wieder grün** (93/93 bzw. 18/18).
**Dritte Erscheinung von T38.9** — ein Prüfer, der eine **Auflage** prüft statt
einer **Eigenschaft**. *Anders als die beiden Wachen aus Teil 1 und 2 prüfen
diese beiden ihren Rückgabewert immerhin.*

⚠️ **Ein roter Test, der NICHT von dieser Aufgabe kommt:**
`research/elliott_wave_params/test_params.py elliott_wave` meldet
`Kennzahlen identisch zum Bot-eigenen Raster` als **rot**. **Gegengeprobt mit
den Fassungen aus `origin/main`: derselbe Befund** — er ist also
**vorbestehend** und steht in keiner Liste, weil dieser Test ohne Argument gar
nicht läuft und ein Basislauf ihn deshalb nie erreicht. *Nicht untersucht, das
wäre eine eigene Aufgabe.* Mit `elliott_wave_stocks` ist derselbe Test grün
(18/18).

---

## Was ausdrücklich NICHT passiert ist

* Keine Signallogik, keine Schwelle, kein Stop, keine Positionsgröße, keine
  Symbolliste, keine Zeitbremse. **Keine Zahl aus `live_params.py`.**
* `shared/entscheidungskerze.py` **unberührt** (Teil 5 misst nur).
* `docs/VORREGISTRIERUNG_*.md`, `docs/projektfuehrung/*`, `docs/UMGEBUNGEN.md`
  **unberührt** — die Vorschläge dafür stehen hier, nicht dort.
* `research/vorregistrierung/auswertung.py`, `research/faltenplan_neun/`,
  `research/etf_trendfolge/`, `research/registernachtrag_tb41/` **unberührt**.
* Nichts unter `broker/`, keine Crontab, kein `results/*.csv`, keine
  `equity_simulation.py`, keine `multi_symbol_*`.
* **Kein Bot-Modul importiert** — jeder Lauf in einem eigenen Prozess (TB-40).

---

## Offene Punkte für den Betreiber

1. ⭐ **Registerfrage Teil 5** — drei Wege, keiner gewählt. Vorlage:
   `research/fromisoformat_registerfrage/BERICHT.md`.
2. ⭐ **Merge-Basis statt zwei Punkte** in `shared/test_kursdaten.py` —
   gemessen, dass es T38.9 löst, ohne den Arbeitsbaum aufzugeben. Eigene
   Aufgabe.
3. **`t3_supertrend`: `compute_indicators` bricht auf einem leeren Rahmen ab.**
   Heute eingefangen, aber mit der falschen Meldung.
3a. **`research/elliott_wave_params/test_params.py elliott_wave` ist
   vorbestehend rot** (`Kennzahlen identisch zum Bot-eigenen Raster`) und
   fällt nur auf, wenn man den Test mit Argument aufruft.
4. **Die sechs übrigen Bots überspringen ein leeres Symbol still.** Eine Zeile
   je Bot.
5. **`system/test_log_rotation.py:599`** — der `os.fstat`-Ersatz ist auf allen
   fünf gemessenen Fassungen harmlos, aber aus denselben Umständen heraus wie
   `_ist_geraet`. Die `_Wache`-Hülle aus TB-44 macht die Frage gegenstandslos.
6. **`docs/UMGEBUNGEN.md`**: Die Zeilen zu `dashboard/test_portfolio_sicht.py`
   und `dashboard/test_dashboard.py` sind je Rechner zu präzisieren (siehe
   Basislauf oben). ⚠️ **Nicht selbst eingetragen** — die Datei wird außerhalb
   der Sitzungen gepflegt.
7. **Mindestfassung des Projekts** steht weiterhin nirgends — kein
   `python_requires`, keine `sys.version_info`-Prüfung.

---

## In einfacher Sprache

**Was wir wissen wollten.**
An fünf Stellen im Projekt hörte etwas auf zu arbeiten, ohne es zu sagen. Drei
davon waren Prüfwerkzeuge, die „alles in Ordnung" meldeten, obwohl sie gar
nicht nachgesehen hatten. Eine war eine Hilfsfunktion, deren Name etwas
anderes verspricht als das, was sie tut. Und eine war ein echter Ausfall: Fiel
die Kursquelle für ein einziges Wertpapier aus, hörten **zwei von neun
Handelsprogrammen** an diesem Tag ganz auf zu arbeiten.

**Was herauskam.**
Alle fünf sind behoben. Für jede einzelne gibt es jetzt einen Test, der sie
**findet** — nachgewiesen dadurch, dass dieser Test am alten Stand rot ist und
am neuen grün. Beim fünften Punkt haben wir nur gemessen und nichts geändert:
Dort geht es um den Kern aller neun Programme, und eine Änderung daran musst
du erst freigeben. Die Messung sagt: **Heute ist dort nichts kaputt, und es
ist auch nicht knapp.**

Nebenbei sind zwei Dinge aufgefallen, die niemand gesucht hat. Erstens: Ein
drittes Programm (`t3_supertrend`) hat denselben Fehler — es überlebt ihn aber
zufällig, weil an anderer Stelle ein Auffangnetz hängt. Zweitens: Sechs der
neun Programme lassen ein Wertpapier **stillschweigend** aus, wenn keine Kurse
kommen. Beides ist aufgeschrieben, aber nicht repariert — das war nicht
freigegeben.

**Warum das so ist.**
Ein Prüfwerkzeug, das bei einem Fehler „bestanden" sagt, ist schlimmer als
gar kein Prüfwerkzeug: Man verlässt sich darauf. Deshalb war die eigentliche
Arbeit nicht das Reparieren, sondern das **Vorführen** — jeden Fehler erst
sichtbar machen, dann beheben, dann zeigen, dass er weg ist. Und dabei
aufpassen, dass die Reparatur nicht an anderer Stelle etwas kaputtmacht: Es
gibt Prüfungen, bei denen „nichts gefunden" genau das richtige Ergebnis ist.
Die mussten grün bleiben, und sie sind es.

**Was das für dich heißt.**
An deinen Handelsprogrammen hat sich am Verhalten **nichts** geändert — keine
Zahl, keine Regel, keine Schwelle. Was sich geändert hat: Wenn morgen eine
Kursquelle ausfällt, hören zwei Programme nicht mehr auf zu arbeiten, sondern
lassen genau das eine Wertpapier aus und **schreiben eine Zeile darüber**.
Und drei Prüfwerkzeuge sagen dir ab jetzt Bescheid, wenn sie nicht mehr messen
können, statt „alles gut" zu melden.

**Zwei Dinge brauchen dich:** Der Testauftrag
`docs/TESTAUFTRAG_TB-45_stille_ausfaelle.md` muss auf deinem Rechner laufen —
zwei der fünf Punkte lassen sich in der Cloud gar nicht vollständig prüfen.
Und in `research/fromisoformat_registerfrage/BERICHT.md` steht eine Frage, die
nur du entscheiden kannst.
