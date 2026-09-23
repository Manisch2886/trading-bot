# TB-92 — Vollzug der Sperrlisten-Änderung (Plan-Punkt 8): Tabelle und `registerbericht.py` **in einem Zug**

⚠️⚠️ **DIESER AUFTRAG STARTET NICHT VON SELBST.** Er wird erst gültig, wenn
**zwei** Bedingungen stehen:

| | |
|---|---|
| **(1)** | ✔ **ERFÜLLT (23c, 16:00):** Fable hat den Vollzug ausdrücklich freigegeben — *„Meine Bedingung aus 23b ist erfüllt und übererfüllt. Der Vollzug ist frei"* |
| **(2)** | ⛔ **OFFEN:** Die **Betreiberfreigabe aus 21.9** für diesen konkreten Vollzug |
| **(3)** | ⛔⛔ **OFFEN — NEU, 16:15:** Fables Antwort auf **Anfrage 23e**. ⚠️ Gemessen nach 23c: Es gibt eine **dritte Leserin** der Tabelle, die Fable in 22h, 23a und 23c **nie genannt** hat — `auswertung.py::main` (Z. 590), **eingefroren**, Sperrliste 3+5, fest verdrahtet ohne Schalter. Stellt man nur die zwei genannten Leser um, liest der **Selektionslauf am Tag** weiter die alte Tabelle, die bei fünf Bots keine einzige Falte enthält |

⛔ **Fehlt eine davon: NICHT ANFANGEN.** Melde, welche fehlt, und brich ab.

**Vorbereitet:** 23.09.2026 vom steuernden Chat, nach TB-91
**Messstand:** HEAD `02f2574`

---

## 0. Der Anlass, in drei Sätzen

Plan-Punkt 8 blockiert den Tag, weil `test_vorregistrierung.py` rot ist. ⭐ **Die
Ursache ist gemessen:** Der Test liest `ergebnisse/benchmark_drawdowns.json`, und
diese Datei ist gegenüber dem Faltenplan **unvollständig**. Der Vollzug ersetzt
sie durch die Neurechnung aus TB-91 — aber er reisst dabei `registerbericht.py`
mit, wenn man es nicht gleichzeitig umstellt.

---

## 1. ⭐⭐ Was der steuernde Chat gemessen hat (Vormessung, `A8`)

⚠️ **Gemessen in der Brücken-VM, nicht mit `trading-env`. Du misst nach.**
Weicht etwas ab, **gilt deine Messung**.

### (a) Warum der Test rot ist

`auswertung.py:237`, in `zulaessigkeit`: `falte = eintrag["falten"][z["falte"]]`
→ **`KeyError: '2017'`** beim Testbot `turtle_soup_stocks`.

⭐ **Die Faltenabdeckung, Tabelle gegen Plan:**

| Bot | alt | **neu** | Plan |
|---|---|---|---|
| `elliott_wave` | ⛔ **0** | 5 | 5 |
| `rsi2_crypto` | ⛔ **0** | 8 | 8 |
| `t3_supertrend` | ⛔ **0** | 8 | 8 |
| `turtle_soup_crypto` | ⛔ **0** | 9 | 9 |
| `volatility_breakout_crypto` | ⛔ **0** | 9 | 9 |
| `elliott_wave_stocks` | 8 | 10 | 10 |
| `rsi2_mean_reversion` | 8 | 9 | 9 |
| `turtle_soup_stocks` | 8 | 10 | 10 |
| `volatility_breakout` | 8 | 9 | 9 |

⇒ ⭐⭐ **Die alte Tabelle deckt fünf Bots gar nicht ab. Die neue deckt alle neun
exakt ab.**

### (b) ⭐ Der Test kommt mit der neuen Tabelle über die Abbruchstelle

Gemessen, ohne eine Datei anzufassen (Ladefunktion nur im Speicher getauscht):

| | alte Tabelle | neue Tabelle |
|---|---|---|
| **Teil A** | ⛔ Abbruch `KeyError: '2017'` | ⭐ **durchgelaufen** |
| **Teil B** | (nie erreicht) | ⚠️ **lief noch nach 170 s** |

⚠️⚠️ **Der vollständige Lauf ist NICHT gemessen** (`A2`). Die Brücke bricht nach
180 s ab; der Test braucht länger. **Ob er ganz grün wird, weisst nur du.**

### (c) ⚠️⚠️ Das Henne-Ei — der eigentliche Grund für diesen Auftrag

`registerbericht.py:178` liest `f['symbole_point_in_time']`. Gemessen, je Falte:

| Schlüssel | alte Tabelle | neue Tabelle |
|---|---|---|
| `symbole_point_in_time` | **ja** | ⛔ fehlt |
| `symbole_handelbar_in_falte` | ⛔ fehlt | **ja** |

⇒ ⚠️⚠️ **Jede Reihenfolge bricht, wenn man einzeln vorgeht:**
- Erst `registerbericht.py` umstellen → bricht an der **alten** Tabelle
- Erst die Tabelle tauschen → bricht, weil `registerbericht.py` den alten Namen sucht

⭐ **Beides gehört in EINEN Commit.** Das ist die Hauptaussage dieses Auftrags.

### (d) Was gesperrt ist und was nicht

| Datei | im Sperrlisten-Abbild |
|---|---|
| `ergebnisse/benchmark_drawdowns.json` | ⛔ **JA** (Punkt 4) — der Vollzug braucht 21.9 und 37.3 |
| `auswertung.py` | ⛔ **JA** (Punkte 3 und 5) — ⚠️ **wird NICHT geändert**, liest nur |
| `registerbericht.py` | ✔ nein — darf geändert werden |
| `test_vorregistrierung.py` | ✔ nein — ⚠️ wird trotzdem **nicht** geändert |

---

## 2. Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt.** Der steuernde Chat hat `ARBEITSWEISE.md`
(Abschnitt 16) und die Fable-Anfrage 23d abgelegt. **Committen, nicht verwerfen.**

⭐ Prüfe zusätzlich, ob verwaiste git-Sperrdateien im Scratchpad liegen (TB-91
fand zwei). Sie stammen aus Commits über die Brücke.

---

## 3. Block A ⭐⭐ — der Vollzug, in EINEM Commit

⚠️ **Reihenfolge innerhalb des Commits ist gleichgültig — aber er muss beides
enthalten.** Ein Zwischenstand, in dem nur eines von beidem steht, ist ein
kaputter Arbeitsbaum.

| | |
|---|---|
| **A1** | Hashes **vorher**: `benchmark_drawdowns.json`, `…_nach_wegA.json`, `registerbericht.py` |
| **A2** | ⭐ Die Neurechnung `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` wird die registrierte Datei. ⚠️ **Nicht** mit `benchmark.py` neu erzeugen — die vorhandene Datei nehmen; sie ist der Gegenstand des Determinismusnachweises |
| **A3** | `registerbericht.py:178`: `symbole_point_in_time` → `symbole_handelbar_in_falte`. ⚠️ **Nur diese eine Stelle** — gemessen: genau **1** Treffer im Modul |
| **A4** | `registerbericht.py` laufen lassen: `rc=0`, und der Bericht nennt die Falten **aller neun** Bots |
| **A5** | Hashes **nachher**, und die Marke am alten Ort: **Abschnitt 10, Punkt 4** trägt *„Form steht fest, Vollzug steht aus"* — ⭐ **dieser Satz wird jetzt berichtigt** |
| **A6** | ⚠️ Tatsachennotiz nach **37.3**: Der Sondenbefund an Punkt 4 ändert sich, weil sich die registrierte Datei ändert. **Das ist planmässig, kein Fehler** |

⛔ **`auswertung.py` wird nicht angefasst.** Es liest nur.

## 4. Block B ⭐⭐⭐ — ist der Test jetzt grün?

**Das ist die Frage, an der Plan-Punkt 8 hängt.**

| | |
|---|---|
| **B1** | `test_vorregistrierung.py` **vollständig** laufen lassen, mit `trading-env`. ⚠️ Er braucht lange — nicht abbrechen |
| **B2** | ⭐ Das Ergebnis **so melden, wie es ist**: grün, oder rot mit Stelle und Meldung. ⛔ Nicht nachbessern, nicht „reparieren" |
| **B3** | Ist er rot: **Abbruch von Block C und D**, Befund melden. Das ist kein Scheitern, sondern das Messergebnis |
| **B4** | Ist er grün: die Laufzeit nennen (für künftige Aufträge) |

## 5. Block C — `G6` und `H3`

Aus TB-88/TB-90 steht **163 bestanden / 2 gescheitert** (`G6`, `H3`).

| | |
|---|---|
| **C1** | Stehen die zwei noch? Zahl **und** Namen |
| **C2** | ⭐ Hat der Vollzug daran etwas geändert — in **beide** Richtungen? Eine neu rote Prüfung ist ein Befund, eine neu grüne auch |

## 5b. ⭐⭐ Fables fünf Schritte (23c, Abschnitt 4) — verbindlich

⚠️ **Sie gehen über die Blöcke A–C hinaus.** Ein Vollzug ohne sie ist unfertig.

| | |
|---|---|
| **1** | Registertext zu Sperrlistenpunkt 4, **Form (ii)**: `benchmark_drawdowns.json` bleibt **gesperrt und unverändert** als registrierter historischer Stand mit Tatsachennotiz; die Neurechnung ist die, die der Lauf liest |
| **2** | Tatsachennotizen zu `_vt.json` (TB-66, Planstand vor 25) und `_tb72.json` (TB-72, Planstand 25, alter Name). ⭐ **Beide bleiben liegen, kommen nicht auf die Liste.** „bestimmt" in 37.2 wechselt auf die neue Tabelle; **mit dem Vollzug wird sie Punkt** |
| **3** | `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5); `test_vorregistrierung.py` läuft **bis zur Schlusszeile** durch; ⭐ `G6`/`H3` bleiben der eigene Punkt aus 23a |
| **4** | ⭐ **Neues Abbild** — schliesst zugleich die planmässigen `1` an `faltenplan.py` und `benchmark.py`. Sonde gegen das Abbild: **kein Pfad-Bestandteil `1`** |
| **5** | Determinismusnachweis (9750/9750, bytegleich) als **Tatsachennotiz mit Beleg** — *„er ist der Grund, warum der Vollzug keine Wahl ist"* |

⭐ **Und Fables Handwerksregel dazu:** Die Sonde soll zusätzlich **je Datei**
zusammenfassen, welche Punkte sie berührt — *„dann liest niemand ‚drei Befunde',
wo einer ist."*

## 6. Block D — der Registertext

⭐ **Erst wenn B grün ist.** Register Zeile 6775: *„Vollzug fertig, wenn:
Registertext eingetragen, `registerbericht.py` liest `symbole_handelbar_in_falte`
(23.5), `test_vorregistrierung.py` grün."*

⚠️ `numstat` zweite Spalte **muss `0`** sein. Marke am alten Ort. Zitate zeichengleich.

---

## 7. ⛔ Was NICHT geschieht

- **Kein** Lauf von `benchmark.py` — die Tabelle ist da, sie wird nicht neu gerechnet
- **Keine** Änderung an `auswertung.py`, `benchmark.py`, `faltenplan.py`, `messgroessen.py`
- ⚠️ **BERICHTIGT 16:15:** Hier stand *„Kein neues Sperrlisten-Abbild — der Befund soll sichtbar bleiben"*. **Das war falsch.** Fable 23c, Schritt 4: *„Neues Abbild (schliesst zugleich die planmässigen 1 an `faltenplan.py` und `benchmark.py`); Sonde gegen das Abbild: kein Pfad-Bestandteil 1."* ⇒ **Das neue Abbild gehört zum Vollzug**, es beendet ihn
- **Keine** Änderung an `test_vorregistrierung.py`, auch wenn er rot bleibt
- ⛔ **Nichts** aus `messgroessen.py` — das liegt bei Fable (23c, unbeantwortet)

## 8. ⛔ Abbruchkriterien

| | |
|---|---|
| **1** | Fables Bestätigung zu 23d fehlt, oder die Freigabe nach 21.9 fehlt |
| **2** | Block A lässt sich nicht in **einem** Commit ablegen |
| **3** | `registerbericht.py` hat an der Stelle **nicht genau einen** Treffer |
| **4** | Eine gesperrte Datei ausser `benchmark_drawdowns.json` würde berührt |
| **5** | Der Arbeitsbaum ist nach Schritt 0 nicht leer |

---

## In einfacher Sprache

**Der Stichtag ist blockiert, weil ein Prüfprogramm rot ist.** Der Grund ist
jetzt gefunden: Die Vergleichstabelle, die es liest, ist veraltet — bei fünf von
neun Bots enthält sie **gar keine** Zeitabschnitte. Die in TB-91 neu gerechnete
Tabelle enthält bei allen neun genau die richtigen.

**Der Austausch ist aber keine reine Ersetzung.** Die neue Tabelle benennt ein
Feld anders als die alte, und ein zweites Programm liest noch den alten Namen.
Wer nur eines von beidem ändert, bekommt in jedem Fall einen Absturz — **egal in
welcher Reihenfolge**. Deshalb gehört beides in einen einzigen Arbeitsschritt.

**Was danach kommt, ist offen und soll offen bleiben:** Ob das Prüfprogramm dann
wirklich grün wird, konnte hier nicht zu Ende gemessen werden — der Lauf dauert
länger, als die Anbindung erlaubt. Das misst erst das MacBook. Bleibt es rot,
ist auch das ein Ergebnis und wird gemeldet, nicht weggebügelt.
