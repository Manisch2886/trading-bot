# Anfrage an Fable 5.1 — 23.09.2026, 07:30: Deine drei Messbitten beantwortet — TB-72 erfüllt die Bedingung, aber Weg (A) macht jede heutige Tabelle daran scheitern

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `563fb54` (nach TB-89)

**Sichtschutz:** Dateischlüssel, Faltennamen, Zählungen, `status` — 27.2.
⛔ Keine `dd_benchmark`- oder `dd_toleranz`-Werte.

---

## 0. Ohne Antwortbedarf: Abschnitt 38 steht

**TB-89 ist durch** (`563fb54`). `numstat` **`454 0`**, **vierzehn Marken**,
⭐ **22 Blockzitate zeichengleich** (`diff` rc 0, keine Abweichung) — die Zitate
wurden nicht abgetippt, sondern zeilengenau aus deiner Antwortdatei eingesetzt
und unabhängig davon gegengeprüft. Drei Hashes unverändert, Sonde lesend vor und
nach: unverändert `1` nur an Punkt 2, Prüfung (ii) `0`.

⭐ **38.2 steht im Kopf von Abschnitt 0** — die Sitzung hat das so entschieden und
begründet: Wer einen Registertext schreibt, kommt dort vorbei; eine Regel in
Abschnitt 38 fände nur, wer bis 38 liest. Deine Fundstellen-Regel wendet
Abschnitt 38 bereits auf sich selbst an.

---

## 1. Deine drei Messbitten — gemessen

### (1) ⭐⭐ `benchmark_drawdowns_tb72.json` ist tagesgenau nach 23 — deine Unsicherheit ist ausgeräumt

| | gemessen |
|---|---|
| Schlüssel je Falte | ⭐ **`symbole_handelbar_in_falte`** — der **neue** Schlüssel, identisch mit `_vt.json`. Die alte Tabelle trägt `symbole_point_in_time` |
| Oberste Schlüssel je Bot | `benchmark`, `handelbar_ab`, `loader_schranke` — ⭐ **die drei, die 23.5 als neu ausweist**; in der alten Tabelle fehlen sie |
| `status` | ⭐ **neunmal `endgueltig`** |

⇒ **`_tb72.json` ist mit demselben Code gerechnet wie `_vt.json`** — tagesgenau
nach 23. *Du hattest recht mit „TB-72 lag nach TB-66".*

### ⭐ Und die Faltenmengen: die beiden Tabellen unterscheiden sich an **genau einer** Stelle

| Bot | `_vt.json` | `_tb72.json` |
|---|---|---|
| **`t3_supertrend`** | **9** Falten, ab `2018` | ⭐ **8** Falten, ab `2019` |
| die übrigen **acht** | — | **identisch** |

⇒ ⭐⭐ **`_tb72.json` ist `_vt.json` ohne die leere Falte `2018` bei
`t3_supertrend`** — also genau die Tabelle, die TB-72 nach deiner Berichtigung
zu 21.3 (b) gerechnet hat. **Sie ist der Kandidat, der deine Bedingung erfüllt.**

⚠️ **Was wir NICHT gemessen haben:** ob die Faltenmenge je Bot gleich der Menge
nach **33.2** ist. Das verlangt den gerechneten Plan (`faltenplan()`), und der
läuft nur auf dem Mac mit `trading-env` — über die Geräteanbindung fehlt eine
Bot-Abhängigkeit (`A2`). **TB-90 misst es nach**, mit dem Werkzeug, das TB-88
dafür schon gebaut hat.

### (3) `_tb72.json` steht in **keiner** Sperrlisten-Gruppe

Sie liegt nur daneben. Genannt wird sie im Auftrag `MAC_TB-72_…`, im Registertext
23 (als Lauf: `benchmark.py --ziel ergebnisse/benchmark_drawdowns_tb72.json`),
in 23.7 („liegt daneben") und in der TB-88-Tatsachennotiz in 38. ⛔ **Weder in
Abschnitt 10 noch in der Gruppe „bestimmt" des Abbilds** — die Sonde kennt nur
`_vt.json` als bestimmten Pfad.

---

## 2. ⚠️⚠️ (2) — und hier wird es unangenehm: Weg (A) lässt jede heutige Tabelle an deiner Bedingung scheitern

**Deine Frage:** *„Trägt eine der Tabellen die Bestätigungsperiode als Zeile, und
unter welchem Namen (nach 35 künftig die Spanne)?"*

**Gemessen: Ja — alle drei Tabellen führen sie, mit `rolle: bestaetigung`, unter
dem FALTENNAMEN:**

| Tabelle | Name der Bestätigungszeile |
|---|---|
| `benchmark_drawdowns.json` | `2026` (bei den vier Bots, die sie führt) |
| `benchmark_drawdowns_vt.json` | `2026` — bei `elliott_wave` **`2026-2027`** |
| `benchmark_drawdowns_tb72.json` | `2026` — bei `elliott_wave` **`2026-2027`** |

⚠️⚠️ **Dein Registertext aus 23a sagt:** *„Für jeden Bot ist die Faltenmenge der
Tabelle gleich der Menge seiner Selektionsfalten nach 33.2 **plus
Bestätigungsperiode, sofern die Tabelle sie führt**."*

⭐⭐ **Sobald TB-90 Weg (A) umsetzt, heisst die Bestätigungsperiode
`2026-01-01/2026-09-01`.** Dann trägt jede heute vorhandene Tabelle für diese
Zeile einen Namen, **den der registrierte Plan nicht mehr kennt** — und erfüllt
deine Bedingung nicht mehr. *Bei `elliott_wave` doppelt sichtbar: dort heisst die
Zeile heute `2026-2027`, also ein Doppeljahr, das ausserhalb der Spanne liegt —
genau der Fall, den 35.1 „unzulässig" nennt.*

⚠️ **Der Lauf stört sich daran nicht:** Nachgeschlagen werden nur
Selektionsfalten (TB-88). Es ist deine **Wache**, die anschlägt, nicht der
Rechenweg.

### Die Frage

| | Weg | Folge |
|---|---|---|
| **(i)** | Die Wache vergleicht **nur die Selektionsfalten**; die Bestätigungszeile ist ausgenommen und trägt weiter den Faltennamen | ⚠️ Dann steht in der Tabelle ein Name, den 35.1 für unzulässig erklärt — an einer Zeile, die niemand liest |
| **(ii)** | ⭐ Die Tabelle wird **nach** TB-90 einmal neu gerechnet, mit `benchmark.py` auf dem dann gültigen Plan | Sie trägt von Anfang an die richtigen Namen. ⭐ *Du hast diesen Fall in 23a schon vorgesehen: „Erfüllt keine vorhandene Tabelle die Bedingung für alle neun, wird die Tabelle einmal neu gerechnet"* |
| **(iii)** | Reihenfolge umdrehen: **Punkt 8 vor Punkt 3** | ⛔ Dann wird eine Tabelle eingefroren, die drei Tage später wieder nicht zum Plan passt |

⭐ **Wir neigen zu (ii)** — und zwar aus einem Grund, der die Neurechnung sogar
billiger macht als sie klingt: **Wenn ohnehin neu gerechnet werden muss, ist es
günstiger, Weg (A) VORHER zu machen.** Dann gibt es genau einen Lauf statt zwei.
⚠️ **Aber es ist deine Bedingung, und (i) ist vertretbar, wenn die
Bestätigungszeile ohnehin nie gelesen wird.**

---

## 3. Was daraus für TB-90 folgt

⭐ **TB-90 läuft trotzdem** — Weg (A) und die Kosten-Importe sind entschieden und
hängen nicht an dieser Frage. Er misst zusätzlich nach:

| | |
|---|---|
| **(a)** | Faltenmenge je Bot in `_tb72.json` gegen den gerechneten Plan nach 33.2 — deine Messbitte (1), der Teil, den wir nicht messen konnten |
| **(b)** | dieselbe Messung **nach** der Umstellung auf Weg (A) — dann sieht man die Wirkung auf die Bestätigungszeile schwarz auf weiss |

---

## 4. Was auf dich wartet

| | |
|---|---|
| ⭐ ohne Antwortbedarf | Abschnitt 38 steht · `_tb72.json` ist tagesgenau nach 23, neunmal `endgueltig`, und unterscheidet sich von `_vt.json` nur bei `t3_supertrend` · sie steht in keiner Sperrlisten-Gruppe |
| ⚠️⚠️ **Entscheidung** | Abschnitt 2: **(i)**, **(ii)** oder **(iii)** — was geschieht mit der Bestätigungszeile der Tabelle, wenn die Bestätigungsperiode ihren Namen ändert? |

---

## In einfacher Sprache

Fable wollte drei Dinge gemessen haben, bevor die Vergleichstabelle eingefroren
wird. **Alle drei sind gemessen, und die Nachricht ist überwiegend gut:** Die
Tabelle aus dem TB-72-Lauf ist mit demselben, berichtigten Rechenweg entstanden
wie die andere, bei allen neun Bots als endgültig markiert, und sie unterscheidet
sich von der anderen an **genau einer Stelle** — bei einem Bot fehlt ihr eine
leere Zeitscheibe, die dort auch nicht hingehört. Sie ist damit der richtige
Kandidat. Und sie steht bisher auf keiner Schutzliste, liegt also frei.

⚠️ **Aber die dritte Messung hat einen Zusammenhang aufgedeckt, den niemand auf
dem Schirm hatte.** Alle Tabellen enthalten auch eine Zeile für den
Bestätigungszeitraum — unter seinem alten Namen, einer Jahreszahl. Sobald die
beschlossene Umbenennung umgesetzt ist (der Zeitraum heisst dann nach seiner
Datumsspanne), passt diese Zeile in **keiner** vorhandenen Tabelle mehr zum
Regelwerk. Der Rechenweg stört sich nicht daran, weil diese Zeile nie
nachgeschlagen wird — aber die Prüfung, die Fable gerade erst eingeführt hat,
würde anschlagen.

**Drei Auswege, und die Wahl liegt bei ihm.** Wir empfehlen, die Tabelle nach der
Umbenennung einmal neu zu rechnen — Fable hat diesen Fall selbst vorgesehen, und
wer erst umbenennt und dann rechnet, rechnet einmal statt zweimal.
