# TB-87 — Registerabschnitt 37: fünf Einträge aus Fables 22d und 22g

**Sitzungstitel:** `TB-87 Register 37 — Sondenausgänge, Abbildgruppen, Ort registrierter Werte`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**Erstellt:** 22.09.2026, 19:10 Ortszeit · **Vorgänger:** TB-86 (`ee4e65c`)
**Erwarteter Ausgangsstand:** `HEAD` = `origin/main` = `5ead288` oder jünger

⭐ **Das ist Stufe I, Punkt 4 aus `PLAN_VOR_DEM_TAG.md`** — reiner Registertext,
blockiert nichts, **braucht keine neue Freigabe.**

---

## 0. Was dieser Auftrag ist

⭐ **Nur Registertext**, wie TB-82 bis TB-84. **Fünf Einträge**, alle aus
`FABLE_ANTWORT_2026-09-22d_wert_ohne_ort.md` und
`FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md`.

| ⛔ | **NICHT Gegenstand** |
|---|---|
| ⛔ | **Die Sonde ändern** — sie meldet heute je Punkt; 37.1 verlangt je Bestandteil. ⚠️ **Das ist Handwerk mit eigener Freigabe, nicht dieser Auftrag** |
| ⛔ | **Ein neues Abbild erzeugen** (Plan Punkt 2b) — eigene Aufgabe |
| ⛔ | **Werte verschieben** („ein Wert, ein Ort") — Plan Punkt 6, braucht erst die Messung aus Punkt 5 |
| ⛔ | **Irgendeine `.py` ändern** |
| ⛔ | ⚠️ `python3 faltenplan.py` — ⭐ *seit TB-86 zwar ungefährlich (Zeitstempel-Voreinstellung, Einmal-Schreibsperre), aber in diesem Auftrag gibt es keinen Grund dafür* |

---

## 1. Schritt 0

1. **Schlüsselbund entsperren**, Kopfzeile „Claude Max".
2. **Committe, was im Arbeitsbaum liegt** (erwartet: leer oder Fables 22g).
3. ⚠️ **Drei Sperrlisten-Hashes messen** → `docs/belege/TB-87/schritt0_hashes_vorher.txt`
   - `ergebnisse/faltenplan.json` → `0e54ac5c…`
   - `ergebnisse/benchmark_drawdowns.json` → `a163c498…`
   - `ergebnisse/benchmark_drawdowns_vt.json` → `4549395f…`
   ⛔ **Weicht einer ab: ABBRUCH.**

---

## 2. Die Regel aus TB-82 bis TB-84 gilt weiter: Marke AM ALTEN ORT

Voller Text in **Abschnitt 37**, dazu ein eingerückter Hinweisblock (`>`) oder
eine Tabellenzeile **direkt beim betroffenen Satz**. ⚠️ **Nur hinzufügen.**
⭐ `numstat` Spalte 2 = **`0`**.

---

## 3. Die fünf Einträge

### 37.1 — Präzisierung zu 36.5: die Sonde meldet je Bestandteil

**Herkunft:** 22d, Abschnitt 1, **zeichengleich:**

> **Präzisierung zu 36.5 (Sonden-Ausgänge):** Die Sperrlisten-Sonde meldet **je Punkt je Bestandteil**: für jeden genannten Pfad 0 oder 1 (Hash gegen Abbild), für jeden nicht messbaren Bestandteil 2 unter Nennung des Wortlauts. Der Gesamtwert eines Punktes ist 1, wenn ein Bestandteil 1 ist; sonst 2, wenn ein Bestandteil 2 ist; sonst 0. Der Gesamtwert des Laufs entsprechend. Am Tag gilt: Kein Pfad-Bestandteil darf 1 sein, und jeder Bestandteil mit 2 hat eine Tatsachennotiz, die sagt, wie er stattdessen geprüft wurde (Lesen, Beleg im Auftrag) — oder der Punkt wird bis zum Tag so nachgetragen, dass er messbar ist.

**Fables Grund, zeichengleich:**

> *„Ein Punkt wie 14 (`auswertung.py` … Docstring) hat einen messbaren Teil (der Datei-Hash) und einen unmessbaren (der Docstring-Anteil). Eine Sonde, die den ganzen Punkt mit `2` meldet, macht den messbaren Teil unsichtbar."*

⭐ **Tatsachennotiz, die du misst (M1):** Die Sonde aus TB-85 gibt **bereits** je
Bestandteil aus — Beleg `docs/belege/TB-85/nullpunkt.txt`, Punkt 1 zeigt den
Datei-Hash **und** daneben den unmessbaren Teil. ⚠️ **Was ihr fehlt, ist der
Rückgabewert je Bestandteil**; das ist Handwerk und **nicht** dieser Auftrag.

**Marke am alten Ort:** in **36.5**.

### 37.2 — Ergänzung zu 36.6: das Abbild führt zwei Gruppen

**Herkunft:** 22d, Abschnitt 2, **zeichengleich:**

> **Ergänzung zu 36.6 (Abbild der Sperrliste):** Das Abbild führt zwei Gruppen: die **Punkte** des Abschnitts 10 und die **bestimmten** Pfade — Dateien, die das Register für die Sperrliste vorsieht, deren Vollzug aber aussteht (heute: `ergebnisse/benchmark_drawdowns_vt.json`, 21.9/23.7). Die Sonde prüft beide Gruppen gleich (Hash gegen Abbild) und weist die Gruppe im Bericht aus. **Am Tag ist die zweite Gruppe leer:** Jeder bestimmte Pfad hat bis dahin seinen Punkt in Abschnitt 10, oder das Register sagt, warum nicht.

**Marke am alten Ort:** in **36.6**.

### 37.3 — ⭐⭐ Ergänzung zu 36.2/36.6: was ein Befund `1` bedeutet, hängt vom Tag ab

⚠️ **Das ist die Lücke, die TB-86 sichtbar gemacht hat.**

**Herkunft:** `FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md`, **zeichengleich:**

> **Ergänzung zu 36.2/36.6:** Ein Befund 1 der Sperrlisten-Sonde **vor dem signierten Tag** ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein **neues Abbild unter neuem Namen** geschlossen, nie durch Anpassung des alten. Ein Befund 1 **nach dem Tag** ist ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Das **letzte Abbild vor dem Tag** wird nach der letzten Codeänderung erzeugt, trägt die Hashes des Tag-Commits und steht selbst mit Hash im Register; der Tag setzt voraus, dass die Sonde gegen dieses Abbild 0 liefert (oder 2 mit Tatsachennotiz nach 22d).

**Fables Grund, zeichengleich:**

> *„Die Sperrliste sagt ‚ab dem signierten Tag sind unveränderlich'. Vor dem Tag ändern sich Sperrlistenpfade planmässig … Die Sonde kann diesen Unterschied nicht kennen; sie meldet 1, und was 1 **bedeutet**, hängt vom Datum ab. Das gehört ins Register, sonst liest jemand den heutigen Befund als Bruch — oder, schlimmer, einen Bruch nach dem Tag als ‚planmässig'."*

⭐ **Und sein Satz zur Sonde, zeichengleich zu übernehmen:**

> *„Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde."*

⭐⭐ **Tatsachennotiz — der erste Anwendungsfall, den du misst (M2):**
TB-86 hat `faltenplan.py` beauftragt und freigegeben geändert; der Hash ging von
**`6f96b95d…`** auf **`fd3e5018…`**. Die Sonde meldet seither **1**. ⭐ Das ist
**der planmässige Fall** nach diesem Registertext — Auftrag `MAC_TB-86_…`,
Freigabe 22.09., 07:50, Beleg `docs/belege/TB-86/schritt8_sonde.txt`.
**Zu schliessen mit einem neuen Abbild; nicht Gegenstand dieses Auftrags.**

**Marken am alten Ort — hier ZWEI:** in **36.2** und in **36.6**.

### 37.4 — Tatsachennotiz zu Abschnitt 10: die zwei Listen in `herkunft.py`

**Herkunft:** 22d, Abschnitt 3 — **Fables eigene Tatsachennotiz, zeichengleich:**

> **Tatsachennotiz zu Abschnitt 10 (22.09.2026):** `research/vorregistrierung/herkunft.py` trägt zwei Listen. **`EINGEFROREN`** (Z. 57, zehn Einträge) ist die Eingabe von `register()` (Z. 114): ein Gesamthash über die Registerdatei plus diese zehn Dateien, laut Docstring „über die eingefrorenen Festlegungen" — sie bildet die Menge aus **Abschnitt 0** ab, nicht die Sperrliste aus Abschnitt 10, und weicht von dieser an fünf Stellen ab (fehlend: `benchmark_drawdowns_vt.json`, `config/top25_symbols.txt`, `config/sp500_top150.txt`; zusätzlich: `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`). **`SPERRLISTE_DATEIEN`** (Z. 66) wird von keiner Stelle gelesen — toter Code. Keine der beiden Listen ist das Abbild der Sperrliste (36.6). `herkunft.py` wird in `research/vorregistrierung/` von keinem Modul importiert; `herkunft.json` und `herkunft_protokoll.jsonl` existieren nicht; die einzigen Aufrufer von `block()` gehören zu `research/turn_of_month/`. Sperrlistenpunkte 11 und 12 verweisen damit auf Funktionen, die im Laufbereich heute niemand aufruft; der Datenvertrag (`auswertung.py` Z. 41) verlangt `herkunft.json` als Pflichteingabe. Der Erzeuger (Nachtrag 2) ist die Stelle, an der `register()` und `datenstand()` erstmals aufgerufen werden.

**Und seine Entscheidung dazu, zeichengleich:**

> **Folge für `herkunft.py`:** **Nicht öffnen.** Der Erzeuger ruft `register()` auf und schreibt in `herkunft.json` **auch das Feld `teile`** (das `register()` liefert und `block()` weglässt) — dann ist lesbar, welche Dateien in den Gesamthash eingingen, ohne dass `block()` oder `herkunft.py` geändert wird. `herkunft.json` bezeugt damit die Abschnitt-0-Menge (zehn Dateien plus Register); die Sperrlisten-Sonde bezeugt Abschnitt 10; die Tatsachennotiz oben sagt, welches Dokument was bezeugt. Zwei Nachweise mit verschiedenem Gegenstand sind kein Widerspruch — zwei Nachweise mit demselben Gegenstand und verschiedenem Inhalt wären einer.

⚠️ **Die Zahlen sind von dir nachzumessen (M3)** — Zeilennummern 57, 66, 114 und
die fünf Abweichungen. Weicht etwas ab: **eintragen, was du misst, und melden.**

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**.

### 37.5 — Registertext „Ort registrierter Werte" (Ersteintrag)

**Herkunft:** 22d, Abschnitt 4, **zeichengleich:**

> **Registertext, Ersteintrag — Ort registrierter Werte:**
> **(1)** Jeder Sperrlistenpunkt, der einen Zahlenwert registriert (heute 7 und 9), nennt **genau ein** Modul und dort **genau eine** Konstante, aus der der Lauf diesen Wert liest. Dieses Modul steht mit Hash auf der Sperrliste; die Sonde prüft für den Punkt Datei-Hash **und** Wert der Konstante (Bauart „Datei plus Konstante", wie Punkte 3, 4, 10).
> **(2)** Der Laufpfad (Optimierer, Equity-Simulation, Erzeuger) liest registrierte Werte ausschliesslich aus diesem Modul — kein Laufmodul trägt eine eigene Kopie. Für den Papierpfad (`forward_test.py`) gilt das nicht als Sperre, aber als Konsistenzprüfung: Die Sonde meldet als Befund, wenn eine Kopie dort vom registrierten Wert abweicht.
> **(3)** Für Punkt 9: `TRADING_FEE_PCT` und `SLIPPAGE_PCT` in einem Modul; für Punkt 7: `CLUSTER_SCHWELLE` und `N_HISTORISCH_JE_BOT` in einem Modul. Welche Module (Kandidaten nach heutiger Messung: `messgroessen.py` für 9, `registerdaten.py` für 7) und ob eines der beiden Module bereits Abschnitt-0-eingefroren ist und deshalb ein neues kleines Modul die Werte tragen muss — **Handwerk mit Freigabe**, aber die Tatsachennotiz zu 7 und 9 nennt am Ende Modul, Zeile und Wert.
> **(4)** Tatsachennotiz zu 7 und 9, jetzt: die heute gemessenen Orte (neun `forward_test.py`; `messgroessen.py:59`; `registerdaten.py:99`, `:115`) mit dem Vermerk, dass der Registertext keinen davon nennt und der Zustand bis zur Umsetzung von (1)–(3) ungeschützt war.

**Fables Kernsatz, zeichengleich:**

> *„Ein Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt nichts — er legt fest."*

⭐ **Und der Satz, der Missverständnisse ausschliesst, zeichengleich:**

> *„Kein Ergebnis — und das ist hier wichtig zu sagen: Die Werte selbst (0,1 / 0,05 / die beiden aus Punkt 7) ändern sich nicht um ein Zeichen; es ändert sich nur, wo sie stehen und dass jemand es merkt, wenn sie sich ändern."*

⚠️ **Die Orte aus (4) misst du selbst (M4)** — neun `forward_test.py`,
`messgroessen.py:59`, `registerdaten.py:99` und `:115`. **Eintragen, was du
misst.**

⚠️⚠️ **Und Fables offene Unsicherheit ist als offen einzutragen:**

> **Offen (Fable 22d):** ob `messgroessen.py` und `registerdaten.py` als
> Abschnitt-0-eingefrorene Dateien für (3) noch geändert werden dürfen — wenn
> nicht, trägt ein **neues kleines Modul** die vier Werte, und die eingefrorenen
> Dateien bleiben stehen. ⭐ **Dazu gehört die Messung aus Plan Punkt 5:** woher
> beziehen die neun `multi_symbol_optimise.py` und `equity_simulation.py` heute
> Kosten und Slippage? ⛔ **Beides nicht Gegenstand dieses Auftrags.**

**Marken am alten Ort:** bei **Sperrlistenpunkt 7** und bei **Punkt 9**.

---

## 4. Die Messungen (bestätigen, nicht übernehmen)

| # | Messung | erwartet |
|---:|---|---|
| **M1** | Gibt die Sonde je Bestandteil aus? (`docs/belege/TB-85/nullpunkt.txt`, Punkt 1) | ⭐ **ja** — Datei-Hash **und** unmessbarer Teil nebeneinander |
| **M2** | Hash von `research/vorregistrierung/faltenplan.py` heute · und der Wert im Abbild aus TB-85 | **`fd3e5018…`** heute · **`6f96b95d…`** im Abbild |
| **M3** | `grep -n "EINGEFROREN\|SPERRLISTE_DATEIEN\|EINGEFROREN)" research/vorregistrierung/herkunft.py` · und die fünf Abweichungen zu Abschnitt 10 | Z. **57**, **66**, **114** · drei fehlend, drei zusätzlich |
| **M4** | Wo stehen `TRADING_FEE_PCT`, `SLIPPAGE_PCT`, `CLUSTER_SCHWELLE`, `N_HISTORISCH_JE_BOT`? | neun `forward_test.py` · `messgroessen.py:59` · `registerdaten.py:99`, `:115` |
| **M5** | ⭐ Die Faltenlisten in 33.2 vor und nach | **identisch** — dieser Auftrag bewegt keine Zahl |
| **M6** | ⚠️ Die drei Sperrlisten-Hashes vor **und** nach | alle drei unverändert |

**Belege:** `docs/belege/TB-87/m1…m6.txt`, Befehl in Zeile 1.

---

## 5. ⛔ Abbruchkriterien

| # | Wenn … | dann |
|---:|---|---|
| **1** | `numstat` Register Spalte 2 ≠ `0` | ⛔ ABBRUCH, kein Commit |
| **2** | Eine Faltenliste in 33.2 unterscheidet sich nachher | ⛔ ABBRUCH |
| **3** | Ein Fable-Zitat nicht zeichengleich übernehmbar | ⛔ Anhalten, melden, **nicht glätten** |
| **4** | Du meinst, eine `.py` ändern zu müssen | ⛔ ABBRUCH |
| **5** | ⚠️ Einer der drei Sperrlisten-Hashes weicht ab | ⛔⛔ **SOFORT ABBRUCH.** Nichts reparieren, nur melden |
| **6** | Abschnitt 37 existiert bereits | ⛔ Anhalten |

⚠️ **Zur Erinnerung aus dem Nachtrag zu ARBEITSWEISE 6d (22.09.):** Ein
Abbruchkriterium führt zu **Abbruch und Meldung**, nie zu einer Rückfrage.
⭐ **Gefragt wird nur bei richtungsweisenden Dingen** — Verfahrensfrage vor dem
Tag, Freigabe, Unumkehrbares, echte Weggabelung. Handwerk entscheidest du.

---

## 6. Schritte

| # | Tun | Nachweis |
|---:|---|---|
| **0** | Schlüsselbund, Arbeitsbaum, **drei Hashes vorher** | `schritt0_hashes_vorher.txt` |
| **1** | **M1–M4** messen | vier Belege |
| **1b** | **M5 vorher**: Faltenlisten festhalten | `m5_faltenlisten.txt` |
| **2** | **Abschnitt 37** schreiben — 37.1 bis 37.5, Fable zeichengleich, dazu ein Schlussteil „Was hier NICHT getan wird" | Commit |
| **3** | **Die Marken am alten Ort**: 36.5 · 36.6 (zweimal: 37.2 und 37.3) · 36.2 · Überschrift Abschnitt 10 · Sperrlistenpunkt 7 · Punkt 9 — ⚠️ **nur einfügen** | Commit |
| **4** | **M5 und M6 nachher** | 0 Abweichungen, drei Hashes gleich |
| **5** | `numstat` Spalte 2 = `0` | Abschlussbeleg |
| **6** | `grep -c "^## 37\."` = `1`, `grep -c "^### 37\."` = **`6`** (37.1–37.5 plus Schlussteil) | Beleg |
| **7** | **`AKTUELLER_AUFTRAG.md`** — ⭐ **bereits auf TB-87 gesetzt, nur lesen** | `grep -c "TB-87"` ≥ 1 |
| **8** | **Journalblock** und `docs/ERGEBNIS_TB-87_register_37.md` | Commit |
| **9** | **Abgabe**: Status leer, `numstat` nachgetragen | Abschlussbeleg |

---

## 7. Ins Ergebnisdokument

1. Die fünf Einträge mit Zeilennummer im Register
2. **M1–M6 mit gemessenem Wert**, nicht mit dem erwarteten
3. Der `numstat`-Nachweis
4. ⭐ **Was NICHT getan wurde:** keine `.py` geändert, kein neues Abbild, keine
   Sonde angepasst, keine Werte verschoben
5. ⚠️ **Offen und benannt:** die Sonde muss noch je Bestandteil **zurückgeben**
   (37.1) · das neue Abbild (Plan 2b) · die Messung aus Plan 5 (woher lesen die
   Optimierer Kosten?) · Fables Unsicherheit zu den eingefrorenen Modulen

---

## In einfacher Sprache

Fünf Einträge ins Regelwerk, alle aus Fables letzten beiden Antworten. **Kein
Programm wird angefasst.**

**Der wichtigste ist der dritte**, und er schliesst eine Lücke, die gestern noch
niemand gesehen hat: Das neue Prüfprogramm meldet seit heute Nachmittag einen
Fund — weil eine geschützte Datei im Auftrag geändert wurde. **Ist das ein
Regelbruch oder nicht?** Bisher stand das nirgends. Jetzt steht es da: Vor dem
Stichtag ist so ein Fund normal, wird vermerkt und mit einer neuen Prüfliste
geschlossen. **Nach dem Stichtag wäre derselbe Fund ein Bruch** — mit förmlicher
Änderung und Lauf von vorn. Und die letzte Prüfliste vor dem Stichtag muss genau
zum eingefrorenen Programmstand passen.

Die anderen vier: Das Prüfprogramm soll künftig **je Bestandteil** melden, damit
eine prüfbare Prüfsumme nicht hinter einem unprüfbaren Kommentartext
verschwindet. Die Prüfliste führt zwei Gruppen — geschützte und *zur Sperrung
vorgesehene* Dateien. Zwei alte Listen in einem Programm bekommen ihren Vermerk,
was sie sind und was nicht. Und: **Jeder geschützte Zahlenwert bekommt genau
einen Ort** — Fables Satz dazu ist der kürzeste der Woche: *„Ein
Sperrlistenpunkt, der einen Wert nennt und keinen Ort, sperrt nichts — er legt
fest."*
