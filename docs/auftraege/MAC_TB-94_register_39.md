# TB-94 — Der Vollzug von Punkt 8 **im Register**: Berichtigung 38.4, Abschnitt 39, neues Abbild

**Sitzungstitel:** `TB-94` · **Angelegt:** 23.09.2026 vom steuernden Chat
**Grundlage:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md`
**Vorgänger:** TB-92 (`fcc3265`) — der Vollzug **im Code** ist erbracht und belegt.
**Aufwand:** hoch. Dies ist reine Registerarbeit: **kein `.py` wird geändert, nichts gerechnet.**

---

## ⭐⭐ Worum es geht, in drei Sätzen

TB-92 hat den Vollzug von Plan-Punkt 8 **im Code** vollständig ausgeführt und
belegt — und dann **richtig abgebrochen**, weil der Registertext 38.4 „grün"
verlangt, während Fables jüngere Antwort 23a „läuft bis zur Schlusszeile"
verlangt. Fable hat den Widerspruch in **23f** als **seinen eigenen** anerkannt:
**23a gilt, und 38.4 ist zu berichtigen.** Dieser Auftrag trägt den Vollzug ins
Register nach, berichtigt 38.4 und schliesst die planmässigen Hash-Übergänge mit
einem **neuen Abbild**.

⚠️ **Repo und Register stehen seit `fcc3265` auseinander.** Fable 23f,
Abschnitt 3, zeichengleich:

> **Zum Zwischenzustand über Nacht:** Er ist zulässig, weil er **benannt** ist — diese Anfrage und diese Antwort liegen beide in der Ablage, der Commit `fcc3265` ist der Stand, und der Registerauftrag ist der nächste Schritt. Was das Verfahren nicht duldet, ist ein **stiller** Abstand zwischen Repo und Register; ein benannter mit Datum und Folgeauftrag ist ein Zwischenstand wie jeder andere vor dem Tag. Nichts zurücknehmen.

⇒ **Nichts von TB-92 wird zurückgenommen.** Dieser Auftrag schliesst den Abstand.

---

## ⛔ Was in diesem Auftrag NICHT geschieht

| | |
|---|---|
| ⛔ | **Keine `.py` wird geändert.** Nicht `auswertung.py`, nicht `registerbericht.py`, nicht `test_vorregistrierung.py`, nicht `benchmark.py`, nicht `faltenplan.py`, nicht `messgroessen.py`, nicht `herkunft.py`, nicht `shared/sperrlistensonde.py` |
| ⛔ | **Nichts wird gerechnet.** `benchmark.py` wird nicht aufgerufen, `faltenplan.py main()` nicht, `messgroessen.py` nicht. Keine Datei in `research/vorregistrierung/ergebnisse/` wird geschrieben oder geändert — **ausser** dem neuen Abbild (Block D) |
| ⛔ | **`G6` und `H3` werden nicht angefasst.** Sie sind nach 23a und 23f ein **eigener Punkt** („Testannahmen folgen dem Register") und Gegenstand von **TB-95**. Weder messen noch anpassen noch erklären |
| ⛔ | **Der Sonden-Entwurf `sonde_je_datei_entwurf.patch` bleibt liegen.** Er ist Handwerk mit eigener Freigabe, nicht Teil dieses Auftrags |
| ⛔ | **Kein bestehender Registersatz wird umgeschrieben.** Auch nicht der falsche Satz in 38.4 — er bleibt zeichengleich stehen und bekommt eine Marke. Das Register ist **append-only** |

⭐ *Wenn du beim Arbeiten den Eindruck bekommst, eine Codeänderung sei nötig,
damit der Registertext stimmt: **Dann stimmt der Registertext nicht, und du
meldest das.** Der Text folgt dem gemessenen Stand, nie umgekehrt.*

---

## 0. Schritt 0 — Arbeitsbaum committen

Im Arbeitsbaum liegen **drei** Dateien des steuernden Chats:

| | |
|---|---|
| `docs/projektfuehrung/ARBEITSWEISE.md` | geändert (Abschnitt 17 und die Nachträge zu 15/16) |
| `docs/werkzeuge/sitzungswaechter/LIESMICH.md` | geändert |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-23h_vollzug_im_code_nicht_im_register.md` | neu |

Dazu die Dateien, die dieser Auftrag mitbringt (dieser Auftrag selbst, Fables
Antworten 23d/23e/23f, TB-95).

⚠️⚠️ **Berichtigung an uns selbst — TB-92 hat richtig gehandelt und wir falsch:**
TB-92 hat `ARBEITSWEISE.md` und `LIESMICH.md` **nicht** committet, weil „eine
Datei ohne Anweisung keine Sitzungsentscheidung ist". Das war korrekt. Der Fehler
lag beim steuernden Chat, der **während einer laufenden Sitzung** nach `docs/`
geschrieben hat. **Hier ist die Anweisung, die damals fehlte: committe alles
drei mit.**

⚠️ **Eine Hilfsdatei ist zu entfernen, bevor du committest:**
`docs/projektfuehrung/_anhang_arbeitsweise_22.md`. Ihr Inhalt ist bereits an
`ARBEITSWEISE.md` angehängt (Abschnitt 22); sie liegt nur noch da, weil die
Brücke aus der VM nicht löschen darf. ⭐ **Prüfe vor dem Löschen, dass ihr
Inhalt wirklich in `ARBEITSWEISE.md` steht** (`grep -c "^## 22\. Drei
Festlegungen"` → **1**), dann `rm`. ⛔ Nicht committen.

Danach: `find .git -name '*.lock'` → keine. Arbeitsbaum leer.

## 0b. ⚠️ Die Freigaben, die dieser Auftrag voraussetzt — prüfe sie am Text

| | prüfen an | erwartet |
|---|---|---|
| **F1** | `docs/projektfuehrung/FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md` **liegt im Repo** | ja — ⭐ diesmal wirklich; TB-92 musste ohne 23d/23e arbeiten |
| **F2** | 23d und 23e liegen ebenfalls im Repo (TB-92 hat ihr Fehlen gemeldet) | ja |
| **F3** | Betreiberfreigabe 21.9 für den Vollzug: erteilt 23.09., 18:12 (in `MAC_TB-92` zitiert) | ja |
| **F4** | 23f Abschnitt 3 nennt den Folgeauftrag „sofort" | ja |

**Fehlt F1, brich ab und melde es.** Ohne 23f gibt es keine Berichtigung zu 38.4.

---

## Block A — Messen, bevor geschrieben wird

⚠️ **Alles, was unten als Zahl im Registertext steht, ist eine Vormessung des
steuernden Chats aus dem Ergebnisdokument von TB-92 und TB-91.** Nach
Prüfprinzip `A8` misst du jede einzelne nach. **Weicht eine ab, gilt deine
Messung**, du trägst deine ein, und die Abweichung kommt ausdrücklich ins
Ergebnisdokument.

**A1 — Hashes, alle mit `sha256` am HEAD-Stand (`fcc3265`):**

| Datei | erwartet |
|---|---|
| `research/vorregistrierung/ergebnisse/benchmark_drawdowns.json` | `a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee` |
| `…/ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` | `64fb2912f1a2ffb02a36834857fe9a91529b7517a8a7185f5fd7b11642f873b7` |
| `…/ergebnisse/benchmark_drawdowns_vt.json` | `4549395fb3ac30f852362ba586b3ac73cdb6b32e5e944a921f0adb239818745d` |
| `…/ergebnisse/benchmark_drawdowns_tb72.json` | `e4ba341d3177d455b1c3151f4bb2e0cf7f16fbd516d9b30edd45d0c7dc005e56` |
| `…/ergebnisse/faltenplan.json` | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` |
| `research/vorregistrierung/auswertung.py` | `c3b4e69d8f207d0c1982a538203dcf184072554fdc1beb0f612bf054cd2a0062` |
| `research/vorregistrierung/registerbericht.py` | `dace1b01…` (voll messen) |
| `research/vorregistrierung/test_vorregistrierung.py` | `6e7defef…` (voll messen) |
| `research/vorregistrierung/benchmark.py` | `d6bdd558…` (voll messen) |
| `research/vorregistrierung/faltenplan.py` | `7aa0b8cc…` (voll messen) |
| `research/vorregistrierung/herkunft.py` | `56a1c2e1…` (voll messen) |
| `…/ergebnisse/sperrliste_abbild_2026-09-22.json` | `6a1b732e…` (voll messen) |

⭐ **Volle Hashes, nicht Kürzel, in den Beleg.** Ins Register kommen die Kürzel
in der Form, die dort üblich ist (`a163c498…`), **ausser** bei den
Hash-Übergängen nach 37.3 — dort steht der volle Hash, wie 37.3 es vorgemacht hat.

**A2 — die Sonde lesend, vor jeder Änderung:**

```
trading-env/bin/python3 shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-22.json
```

Erwartet: `rc 1`, Befund an den Punkten **2, 3, 4, 5, 6, 14**, Prüfung (ii)
(Listentext) **0**. Beleg: `a2_sonde_vorher.txt`.

⚠️ **Prüfung (ii) muss hier `0` sein.** Ist sie es nicht, hat jemand den
Listentext von Abschnitt 10 bereits verändert — dann **abbrechen und melden**,
denn Block B baut darauf auf.

**A3 — `numstat` des Registers am Eingang festhalten** (`git --no-optional-locks
log -1 --numstat -- docs/VORREGISTRIERUNG_neuselektion.md`) und die aktuelle
Zeilenzahl (`wc -l`, erwartet **6955**).

---

## Block B — Der Vollzug im Punkttext von Abschnitt 10

⭐⭐ **Das ist der eigentliche Vollzug.** Bis heute steht in 38.4 ausdrücklich:
*„Der Punkttext oben ist NICHT geändert."* Jetzt wird er geändert — **additiv**.

**B1 — Die Pfadzeile.** Punkt 4 lautet heute (Z. 867–870):

```
4. **Drawdown-Bedingung, `DD_Toleranz` und die vorab berechneten
   Benchmark-Drawdowns** — `benchmark.py`,
   `ergebnisse/benchmark_drawdowns.json`, **einschliesslich der
   Interpolationsregel**
```

⭐ **Füge nach der Zeile `   Interpolationsregel**` (heute Z. 870) ein — und
ändere an den vier Zeilen oben *kein Zeichen*:**

```
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)
```

⚠️ **Zeilennummern sind flüchtig.** Suche die Stelle über den **Text**
(`Interpolationsregel**` gefolgt von `   > ⭐ **Form (ii)`), nicht über die Zahl,
und prüfe mit `grep -c`, dass `Interpolationsregel\*\*` genau **einmal**
vorkommt. Kommt sie öfter vor, abbrechen und melden.

**B2 — Die Vollzugsmarke.** Der Blockzitat-Kasten Z. 871–880 (Fables Form-(ii)-Text
aus 22h) **bleibt zeichengleich stehen**. Setze **danach**, vor `5. **Abbruchkriterien`,
eine neue Marke:

```
   > ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026).** Der Punkt nennt jetzt beide
   > Dateien. ⚠️ **Zwei Berichtigungen am Kasten darüber:** (1) Die Tabelle,
   > die der Lauf liest, ist **nicht** `benchmark_drawdowns_vt.json`, sondern
   > die Neurechnung `benchmark_drawdowns_2026-09-23_nach_wegA.json`
   > (`64fb2912…`) — so entschieden in **23b**, nachdem 23a die Bedingung
   > „die Tabelle folgt dem registrierten Faltenplan" gesetzt hatte; `_vt.json`
   > trägt bei `t3_supertrend` eine Falte `2018`, die der Plan seit TB-72 nicht
   > mehr hat. (2) Die zwei offenen Fragen aus 22i sind **beide beantwortet**:
   > das Fertigkriterium in **23a** (berichtigt in 39.1), die Tabelle in
   > **23a/23b** (vollzogen hier). Der Kasten oben ist als Zitat richtig und
   > bleibt unverändert; überholt ist an ihm nur der Dateiname und der Satz
   > „Vollzug steht aus".
```

**B3 — Prüfen, bevor weitergegangen wird:**

| | |
|---|---|
| `numstat` des Registers nach B1+B2 | zweite Spalte **`0`** |
| Der alte Kasten | `git --no-optional-locks diff` zeigt **keine** `-`-Zeile im Bereich 867–880 |
| `benchmark_drawdowns.json` | Hash unverändert `a163c498…` — ⚠️ **jetzt messen, nicht später** |

⚠️⚠️ **Ändert sich der Hash von `benchmark_drawdowns.json` an irgendeiner Stelle
dieses Auftrags, brich sofort ab.** Form (ii) lebt davon, dass diese Datei
byteweise dieselbe bleibt.

---

## Block C — Registerabschnitt 39

**Neuer Abschnitt `## 39 …` am Ende des Registers**, mit den Unterabschnitten
`### 39.1` bis `### 39.10`. Bauart wie Abschnitt 38: Fables Texte als
**eingesetzte Blockzitate** (nie abgetippt — `diff` gegen die Quelldatei mit
`rc 0` als Beleg), darunter Grund und Tatsachennotizen, am Ende die Marken.

### 39.1 ⭐⭐ Berichtigung zu 38.4 — das Fertigkriterium von Punkt 8

Der Anlass gehört in den Text: **38.4 trägt Fables Satz aus 22h („grün"), den
23a zurückgenommen hat — die Rücknahme ist nie als Ersatztext eingetragen
worden.** TB-92 hat sich an das Register gehalten und abgebrochen; das ist das
richtige Verhalten und wird hier ausdrücklich festgehalten.

Fables Ersatztext aus **23f Abschnitt 2**, zeichengleich als Blockzitat
einsetzen (beginnend mit *„Berichtigung zu 38.4, Ersatztext (aus 23a,
zeichengleich in der Sache): Punkt 8 ist fertig, wenn: …"*), dazu seinen Grund
(*„ein Fertigkriterium hängt an dem, was der Punkt ändert; sonst haftet ein
Punkt für fremde Fehler und wird nie fertig"*) und seine neue Regel an sich
selbst, zeichengleich:

> **Und eine Regel für mich, damit das nicht wieder passiert:** Wenn eine Antwort von mir einen Registertext ändert, den eine frühere Antwort gesetzt hat, **nennt sie ihn als Berichtigung mit Abschnittsnummer** — nicht als neue Entscheidung. Eure Regel „nicht übernehmen, nachmessen" gilt für meine Texte gegen das Register genauso wie für eure gegen den Code.

⭐ **Und der Satz, der die Rangfolge festhält** (23f Abschnitt 2, zeichengleich):
*„Für eine ausführende Sitzung gilt das Register, nicht Fable."*

⛔ **Der alte Satz in 38.4 (Z. 6775) wird NICHT umgeschrieben.** Er bleibt
zeichengleich und bekommt eine Marke (siehe Marken unten).

### 39.2 ⭐⭐ Vollzug von Sperrlistenpunkt 4, Form (ii)

Was Punkt 4 ab jetzt nennt, mit Hash:

| Datei | Rolle | sha256 |
|---|---|---|
| `ergebnisse/benchmark_drawdowns.json` | **registrierter historischer Stand**, gesperrt und unverändert, wie Punkt 2 (30.3) | `a163c498…` |
| `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` | **die Tabelle, die der Lauf liest** | `64fb2912…` |

**Warum diese Datei und nicht `_vt.json`:** 23a hat die Bedingung gesetzt (die
Faltenmenge der Tabelle ist je Bot gleich der Menge der Selektionsfalten nach
33.2, plus Bestätigungsperiode; Benchmark tagesgenau nach 23; keine Mischung aus
zwei Tabellen), 23b hat entschieden, dass sie **einmal neu gerechnet** wird, und
TB-91 hat sie gerechnet. ⇒ **Die zweite offene Frage aus 38.4 („welche Tabelle
für `t3_supertrend`") ist hiermit beantwortet.**

**Wie die drei Leser sie lesen** (TB-92, `0292e92`): über **eine** Konstante
`auswertung.BENCHMARK_TABELLE`, ⛔ **keinen Schalter** (Abschnitt 12).
`registerbericht.py` und `test_vorregistrierung.py::_tabellen` lesen
`aw.BENCHMARK_TABELLE`. `registerbericht.py` liest dort den Schlüssel
`symbole_handelbar_in_falte` (23.5) statt `symbole_point_in_time`; der alte
Schlüssel kam genau **einmal** vor.
⚠️ **Tatsache, die ins Register gehört:** `beispieldaten.py` liest **keine**
Tabelle (Hash `3e547014…` unverändert) — die im Auftrag TB-92 erwartete vierte
Leserin gibt es nicht. Repo-weit sind es **drei** Leser, wie TB-88 gemessen hat.

### 39.3 Tatsachennotizen zu `_vt.json` und `_tb72.json`

Nach 23b, zeichengleich als Blockzitat einsetzen (*„`benchmark_drawdowns_vt.json`
und `benchmark_drawdowns_tb72.json` bleiben unverändert liegen, erhalten je eine
Tatsachennotiz …"*). Dazu die Tatsachen:

| Datei | Planstand | sha256 | Sperrliste |
|---|---|---|---|
| `…_vt.json` | TB-66 | `4549395f…` | ⛔ **nicht** |
| `…_tb72.json` | TB-72 | `e4ba341d…` | ⛔ **nicht** |

⭐ **Folge für 37.2 (Gruppe „bestimmt"):** Die Gruppe nannte bisher
`ergebnisse/benchmark_drawdowns_vt.json`. Sie **wechselt auf die neue Tabelle** —
und weil deren Pfad mit Block B in Punkt 4 steht, ist die Gruppe „bestimmt"
danach **leer**. 37.2 verlangt genau das für den Tag: *„Am Tag ist die zweite
Gruppe leer."*
⚠️ **Halte im Registertext fest, ob die Sonde das auch so meldet** — TB-87 hat
gemessen, dass sie den bestimmten Pfad bisher nur **nennt** und nicht prüft. Was
nach dem neuen Abbild dort steht, ist Block D.

### 39.4 ⭐⭐ Determinismusnotiz (TB-91, Bedingung aus 23b)

Fables Bedingung aus 23b zeichengleich als Blockzitat, darunter das Ergebnis —
⚠️ **ohne Werte, Sichtschutz 27.1:**

> Neurechnung mit `benchmark.py` `d6bdd558…` reproduziert `benchmark_drawdowns_tb72.json` in **allen** Werten: **9 Bots, 77 Falten, 63 Botfelder, 9750 Blattwerte**, rekursiv bis zum Blatt, Typ **und** Wert. **0 Abweichungen ausser dem Namen der Bestätigungszeile** (9/9: `2026` bzw. `2026-2027` → `2026-01-01/2026-09-01`). `dd_toleranz` 9/9 gleich, `status` 9/9 `endgueltig`. **Gegenprobe auf Textebene:** `_tb72.json` geladen, Bestätigungsfalte umbenannt, mit `indent=1, ensure_ascii=False, sort_keys=True` und Schluss-`"\n"` geschrieben → sha256 `64fb2912…`, **bytegleich** mit der Neurechnung. Lauf 56 s, `rc 0`, HEAD `31008b6`.

⭐ **Selbsttest des Vergleichers, weil ein Vergleich, der nichts finden kann,
keiner ist:** `_tb72` gegen sich selbst 0 Abweichungen, `_tb72` gegen `_vt`
**101** Abweichungen.

⭐ **Die Wache aus 23a, gemessen (TB-91 Block D):** Faltenmenge der vollzogenen
Tabelle je Bot gegen den Plan im Speicher — **18/18 gleich** (9 Bots × 2
Einstufungen: alle, sel), Bestätigungszeile 9/9. Keine Falte fehlt, keine ist
zusätzlich.

⇒ **Damit ist zugleich Festlegung 32 an der Tabelle gemessen:** Zwischen TB-72
und heute hat sich an den Benchmark-Drawdowns nichts bewegt ausser dem Namen.

### 39.5 ⭐⭐ Tatsachennotizen zu 37.3 — die fünf Hash-Übergänge

⚠️ **Keiner davon steht bisher im Register.** 37.3 verlangt für jeden
planmässigen Befund vor dem Tag: Auftrag, Freigabe, alter und neuer Hash. Trage
alle fünf ein, mit **vollem** Hash:

| Datei | von → nach | Auftrag / Commit | Freigabe | Sperrlistenpunkte |
|---|---|---|---|---|
| `faltenplan.py` | `6f96b95d…` → `fd3e5018…` | TB-86, `4daa254` | 22.09., 07:50 | 2 — *bereits in 37.3 notiert* |
| `faltenplan.py` | `fd3e5018…` → `7aa0b8cc…` | TB-90, `303a7fd` | 22.09. | 2 — **neu** |
| `benchmark.py` | `3960375a…` → `d6bdd558…` | TB-91, `31008b6` | 23.09., 10:40 | **4 und 6** — neu |
| `auswertung.py` | `1c2e2dae…` → `c3b4e69d…` | TB-92, `0292e92` | 23.09., 18:12 + Fable 23d | **3, 5 und 14** — neu |
| `registerbericht.py` / `test_vorregistrierung.py` | `2b1ce24a…` → `dace1b01…` / `55553739…` → `6e7defef…` | TB-92, `0292e92` | dieselbe | ⭐ **stehen auf keinem Punkt** — nur Tatsachennotiz |

⭐ **Ein Fund aus TB-91, der ins Register gehört und nicht auf TB-91 beschränkt
ist:** Ein Sondenpunkt kann von `2 NICHT PRUEFBAR` auf `1 BEFUND` **hochstufen**,
sobald eine der dort genannten Dateien im Hash abweicht. ⇒ `A2` („konnte nicht
messen ist ein eigenes Ergebnis") heisst **nicht** „bleibt für immer unmessbar",
und die Zahl der nicht prüfbaren Punkte ist keine feste Grösse. Deshalb ist die
Bilanz `1/3/10` nicht schlechter als `1/1/12`.

⚠️ **Zählweise, damit niemand einen Widerspruch liest:** Die sechs Befunde
(2, 3, 4, 5, 6, 14) stammen aus **drei** Dateiübergängen, nicht aus sechs
Änderungen. `auswertung.py` allein steht an 3, 5 und 14.

### 39.6 ⭐ Der Modus-Nachweis (Fable 23e)

Fables Forderung aus 23e zeichengleich als Blockzitat, darunter das Ergebnis:

| | |
|---|---|
| Wurzel | Snapshot `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2`, MANIFEST-`datenstand_hash` `d9449faf…`, **225/225** Dateien byteweise gleich |
| Umlenkung | `TB30A_BASE_DIR` auf einen Hilfsordner; ⚠️ `TB_SELEKTIONSWURZEL` wirkt in `research/vorregistrierung/` **nicht** (0 Treffer) |
| Code-Commit | `d136251` (`benchmark.py` `d6bdd558…`, `faltenplan.py` `7aa0b8cc…`) |
| Ergebnis | **Vier Läufe, alle `rc 0`, je 51–52 s, alle bytegleich** `64fb2912…` mit der vollzogenen Tabelle. Nichts in `ergebnisse/` geschrieben |
| Lesequellen (Lesehaken `sys.addaudithook`, 11 Prozesse über `sitecustomize`) | **0 Lesezugriffe auf `data/` oder `config/` des Repos**; 222 CSV und 2 Universumsdateien aus dem Snapshot |

⇒ **Die vollzogene Tabelle ist aus dem eingefrorenen Datenstand byteweise
wiederherstellbar.**

### 39.7 ⚠️ Tatsachennotiz — `herkunft.py::EINGEFROREN` zeigt weiter auf den historischen Stand

`herkunft.py` ist **unverändert** (`56a1c2e1…`). Seine Liste `EINGEFROREN` hasht
damit weiter `ergebnisse/benchmark_drawdowns.json` — **nicht** die Tabelle, die
der Lauf liest. Nach Fable 23d schützen **Punkt 4** und **das Abbild** die neue
Tabelle; beides ist mit diesem Abschnitt und Block D erfüllt. ⭐ **Deshalb ist
das eine Tatsachennotiz und kein Befund** — aber sie gehört ins Register, damit
niemand später `EINGEFROREN` für vollständig hält.

⚠️ **Nimm auch Fables Präzisierung zu 36.1 (1) aus 23c zeichengleich auf:**
„gesperrt" umfasst **jeden Pfad, dessen Hash am Tag bezeugt wird — auch
`herkunft.py::EINGEFROREN`**.

### 39.8 ⭐⭐ Der Lesehaken — zwei Eingaben ohne registrierten Eingabestand

Der Modus-Lauf hat neben dem Snapshot **zwei weitere Eingabequellen** geöffnet:

| | |
|---|---|
| `research/vorregistrierung/ergebnisse/messgroessen.json` | ⚠️ beschreibt nach TB-93 einen Datenstand, den es nicht mehr gibt (Commit `90e3cbd`, „BTC/ETH ab 2017-08-17"). Wird mit **TB-96** geschlossen |

⚠️ **Berichtigung einer Nummer, damit die Ablage lesbar bleibt:** Fable nennt in
23f für den Eingabestand von `messgroessen.json` die Nummer **TB-94**; so stand
es in unserem Plan vom Vormittag. Die Nummern sind danach gerückt, weil der
Registervollzug vorgezogen wurde: **TB-94 ist dieser Auftrag, TB-95 sind G6/H3
und die Messbitte, TB-96 ist `messgroessen.json`.** Trage das so ein — eine
Nummer, die zwei Sachen meint, ist schlimmer als eine verschobene.
| **neun** `research/tb24_haltedauern/daten/*_alle_trades.csv` | ⚠️ Ergebnisdateien, keine Kursdaten; weder auf der Sperrliste noch im Snapshot. Der Weg führt über den Faltenplan |

⭐ **Fables Messbitte aus 23f Abschnitt 6 (nur das Ob) ist Gegenstand von
TB-95** — hier wird sie nur als **offene Sache** eingetragen, mit ihrem Wortlaut
als Blockzitat. ⛔ **Sie wird in TB-94 nicht beantwortet.**

⚠️ **Zwei weitere gemessene Tatsachen aus TB-92, die hierher gehören:**
(1) `benchmark.py` und `messgroessen.py` lesen an `shared/paths.py` **vorbei**
(`TB30A_BASE_DIR` bzw. `<BASE>/data`); die Kindprozesse des Faltenplans folgen
**eigenen** Variablen (`TB36_BASE_DIR`, `TB40_BASE_DIR`). (2) Der Lauf öffnet
`logs/notifications/manuelle_eingriffe.log` im Modus `a`; die Datei blieb
unverändert (mtime 11.09.).

### 39.9 Das neue Abbild und die Sonde

Ergebnis von Block D, mit Name und Hash des neuen Abbilds, der Bilanz der Sonde
davor und danach, und dem Satz aus 37.3, dass ein Abbild **neu** geschrieben und
nie angepasst wird. ⭐ Fables Satz aus 22g gehört dazu, falls er in Abschnitt 39
noch nicht steht: *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre
keine Sonde."*

### 39.10 Was hier ausdrücklich NICHT getan wird

Tabelle wie 38.8. Mindestens: keine `.py` geändert · nichts gerechnet · `G6`/`H3`
nicht angefasst (TB-95) · `messgroessen.json` nicht angefasst (TB-96) ·
Fables Messbitte zu den Trade-Listen nicht beantwortet (TB-95) · der
Sonden-Entwurf nicht angewandt · kein alter Registersatz umgeschrieben ·
`benchmark_drawdowns.json` byteweise unverändert · N = 653 (Festlegung 10)
unberührt, Zellenzahl je Bot 80/384/400/96/320/320/400/96/320, **Summe 2416**,
wie Register Z. 380.

### ⭐ Marken am alten Ort

| Marke | wohin |
|---|---|
| Vollzug | **Abschnitt 10, Punkt 4** — bereits mit B2 gesetzt |
| Berichtigung des Fertigkriteriums | **38.4**, direkt unter dem Zitat mit „grün" (heute Z. 6775) |
| Berichtigung des Fertigkriteriums | **21.9**, unter der Tabelle der Folgen |
| Berichtigung des Fertigkriteriums | **38.7 (d)**, wo die offene Frage geführt wird |
| Vollzug und Gruppenwechsel | **37.2**, unter dem Registertext |
| Die fünf Hash-Übergänge | **37.3**, unter der Tatsachennotiz zu TB-86 |
| Die Tabelle folgt dem Plan | **23.7** und **33.2** |
| `EINGEFROREN` unvollständig | **37.4** (die zwei Listen in `herkunft.py`) |
| Form (ii) vollzogen | **38.4**, am Ende |

⚠️ **Setze keine Marke, deren Zielabschnitt du nicht gelesen hast.** Passt eine
nicht, lass sie weg und **melde, welche und warum** — eine Marke an der falschen
Stelle ist schlimmer als keine.

---

## Block D — Das neue Abbild und die Sonde

⚠️⚠️ **Reihenfolge ist hier alles.** Das Abbild liest den **Listentext** von
Abschnitt 10. Block B und C müssen **vollständig geschrieben und committet**
sein, bevor das Abbild gezogen wird — sonst bezeugt es einen Registerstand, den
es nicht mehr gibt.

**D1 — Abbild ziehen.** `--ziel` ist Pflicht, es gibt keine Voreinstellung,
`O_EXCL`:

```
trading-env/bin/python3 research/vorregistrierung/sperrliste_abbild.py --ziel research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json
```

⚠️ **Existiert die Datei schon, bricht der Erzeuger ab — das ist richtig, nicht
umgehen.** Dann einen Namen mit Zeitstempel wählen und **melden**.

**D2 — Sonde gegen das neue Abbild:**

```
trading-env/bin/python3 shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-23.json
```

| erwartet | |
|---|---|
| Punkte **2, 3, 4, 5, 6, 14** | von `1 BEFUND` auf `0` — die planmässigen Übergänge sind geschlossen |
| Prüfung (ii), Listentext | `0` — das Abbild trägt den neuen Punkt-4-Text |
| Gesamtausgang | ⭐ **`0`**, sofern kein Punkt aus anderem Grund `1` meldet |
| Gruppe „bestimmt" | **leer** oder nur noch mit Pfaden, die einen Punkt haben |

⚠️⚠️ **Meldet die Sonde weiter `1`, ist das ein Ergebnis und wird gemeldet, nicht
wegrepariert.** Dann: Punkt und Datei nennen, Hash vorher/nachher, und ob der
Übergang in 39.5 steht. ⛔ **Das alte Abbild `sperrliste_abbild_2026-09-22.json`
wird nicht gelöscht und nicht geändert** (36.6).

**D3 — Fertigkriterium nach der Berichtigung 38.4 durchgehen**, Punkt für Punkt,
als Tabelle im Ergebnisdokument:

| | erfüllt? | wo |
|---|---|---|
| Registertext eingetragen (Form (ii)) | | 39.2 + Block B |
| Tatsachennotiz mit altem und neuem Hash | | 39.5 |
| Die drei Leser lesen über eine Konstante | | TB-92, `0292e92`; hier nur bezeugt |
| `registerbericht.py` liest `symbole_handelbar_in_falte` | | TB-92 |
| Absturz weg, Test läuft bis zur Schlusszeile | | TB-92 (163/2, `rc 1`, 501 s) |
| Modus-Nachweis bytegleich | | 39.6 |
| Neues Abbild | | D1 |
| Sonde `0` für die Pfade | | D2 |

⭐ **Ist die Spalte vollständig ja, ist Plan-Punkt 8 fertig — sage das in einem
Satz.** Fehlt etwas, sage **was** und lass es offen; nicht nachbessern.

---

## Block E — Nachweise und Abgabe

**E1 — Der `numstat`-Nachweis für das Register.** ⭐⭐ Nach dem Commit:

```
git --no-optional-locks log -1 --numstat -- docs/VORREGISTRIERUNG_neuselektion.md
```

⚠️ **Die zweite Spalte MUSS `0` sein.** Ist sie es nicht, hast du irgendwo eine
Zeile entfernt oder umgebrochen — such die Stelle über
`git --no-optional-locks diff` und stelle sie wieder her, **bevor** du abgibst.
Der Nachweis kommt zeichengleich ins Ergebnisdokument.

**E2 — Die eingesetzten Zitate belegen.** Für jedes Blockzitat aus einer
Fable-Datei ein `diff` gegen die Quelle mit `rc 0`, wie in TB-89 (dort 22 Zitate).
Zahl der Zitate und Zahl der `rc 0` ins Ergebnisdokument. ⭐ *Eingesetzt, nicht
abgetippt — das schliesst Zuschreibungsfehler aus.*

**E3 — Belege** nach `docs/belege/TB-94/`: `a1_hashes.txt`, `a2_sonde_vorher.txt`,
`d1_abbild.txt`, `d2_sonde_nachher.txt`, `e1_numstat.txt`, `e2_zitate.txt`.

**E4 — Ergebnisdokument** `docs/ERGEBNIS_TB-94_register_39.md`, Bauart wie
TB-89/TB-92, mit einem Abschnitt **„In einfacher Sprache"** am Ende und einem
Abschnitt **„Für die Folgesitzung vorbereitet (gemessen, nicht eingetragen)"**,
falls dir dabei etwas auffällt.

**E5 — Journalblock** wie üblich.

**E6 — Commit-Aufteilung:**

| Commit | Inhalt |
|---|---|
| 1 | Schritt 0 — Arbeitsbaum des steuernden Chats |
| 2 | ⭐ **Block B und C in EINEM Commit** — Punkttext und Abschnitt 39 gehören zusammen; ein Register, dessen Punkt 4 die Tabelle nennt, aber dessen Abschnitt 39 fehlt, ist ein Zwischenstand, den niemand lesen kann |
| 3 | Block D — neues Abbild, Sonde, Belege |
| 4 | Abgabe — Ergebnisdokument, Journalblock |

---

## ⚠️ Abbruchkriterien — melde und höre auf

1. **23f liegt nicht im Repo** (F1).
2. **Prüfung (ii) der Sonde ist vor Block B nicht `0`** (A2).
3. **Ein gemessener Hash weicht von der Vormessung ab** — melden, deine Messung
   gilt, und **frag nicht nach, sondern trage deine ein und schreib es auf**.
4. **`benchmark_drawdowns.json` ändert seinen Hash** (B3).
5. **`numstat` zweite Spalte ≠ 0** nach einem Versuch, es zu richten.
6. **Der Punkttext an Z. 867–870 oder der Kasten 871–880 müsste geändert werden,
   damit etwas aufgeht** — dann stimmt eine Annahme dieses Auftrags nicht.
7. **Die Sonde meldet nach dem neuen Abbild `1`** — melden, nicht reparieren.

⭐ *Punkt 3 und 7 sind keine Fehler, sondern Ergebnisse. Der Auftrag ist auch
dann abgearbeitet, wenn sie eintreten — er ist nur dann nicht abgearbeitet, wenn
du sie verschweigst oder wegrechnest.*

---

## In einfacher Sprache

Vorgestern wurde beschlossen, welche Vergleichstabelle die Programme künftig
lesen sollen. Gestern wurde das im Programm umgesetzt und nachgewiesen. **Im
Regelwerk steht davon noch nichts** — und genau das holt dieser Auftrag nach.

Drei Dinge sind zu tun. **Erstens** eine Berichtigung: Im Regelwerk steht noch
ein älterer Satz des Verfahrensprüfers, der für diesen Arbeitspunkt „das
Prüfprogramm muss fehlerfrei sein" verlangt. Er hat diesen Satz inzwischen
zurückgenommen und durch „das Prüfprogramm muss bis zum Ende durchlaufen"
ersetzt, vergessen aber, die Ersetzung im Regelwerk anzuordnen. Die vorige
Sitzung hat sich deshalb ans Regelwerk gehalten und aufgehört — richtig. Der
alte Satz wird nicht gelöscht, sondern bekommt einen Hinweis daneben, dass er
überholt ist.

**Zweitens** der eigentliche Eintrag: In der Liste der geschützten Sachen wird
bei der Drawdown-Zeile die neue Tabelle **zusätzlich** genannt. Die alte Datei
bleibt Byte für Byte unangetastet — sie ist der historische Stand. Dazu kommt
ein neuer Abschnitt, der festhält, was gemessen wurde: dass die neue Tabelle der
alten in allen 9750 Zahlen gleicht und nur ein Zeilenname anders ist, dass sie
sich aus dem eingefrorenen Datenbestand Byte für Byte wiederherstellen lässt,
und dass fünf Programmdateien sich planmässig geändert haben.

**Drittens** ein neues Schutzabbild: eine Aufnahme aller geschützten Dateien mit
ihren Prüfsummen zum heutigen Stand. Danach darf die Wache keinen Alarm mehr
schlagen. Schlägt sie doch einen, wird er gemeldet und nicht abgestellt.

Zwei Dinge bleiben ausdrücklich liegen: die beiden fehlschlagenden Prüfungen und
eine Frage des Verfahrensprüfers zu neun Handelslisten, die der Vergleichslauf
öffnet. Beides ist der nächste Auftrag.
