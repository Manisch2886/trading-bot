# REGISTER-KOPIE Abschnitt 29 (von 0–52) — Register-Z. 5342–5424 — Commit ad351d5f0351d8a25479547edb96a32dd6cf3bd5 — 2026-10-02 — Original sha256 a749678043f32e5c6bf7034205bc7176550ec4ea35d08171b43d40401aec7ece — KOPIE, nicht das Register

## 29. Der Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte (TB-78, 21.09.2026)

⭐ **Neuer Registertext, keine Berichtigung** — gemessen: das Register regelt
den Beginn des Kapitalpfads bisher nicht (siehe 29.2).
⭐ **Bauart 24.3: die Regel steht vor der Messung.**

### 29.1 Der Befund — eine Lücke zwischen Horizontbeginn und erster Falte

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md`,
Abschnitt 3.2.

Abschnitt 26 verbietet Einstiege **vor dem Horizontbeginn** (28.4: `2016-09-19`
für die vier Aktien-Bots). Die erste Selektionsfalte beginnt nach 4a am
**1. Januar**. Dazwischen liegen dreieinhalb bis fünfzehn Monate, in denen ein
Einstieg nach 26 **zulässig** ist, in **keiner Falte** auftaucht — und durch den
Kapitalpfad läuft.

⭐ **Fable, wörtlich:** *„Das ist genau der Schaden, mit dem (d) begründet wurde
(‚verändern das Kapital, mit dem die erste Falte beginnt'), nur kürzer."*

⚠️ **Dasselbe kann bei Krypto auftreten**, wo Bedingung (i) wegen des Vorlaufs
später liegt als der erste handelbare Tag — `rsi2_crypto`: 2018 handelbar, erste
Falte 2019.

⚠️⚠️ **Und die Wache aus 21b sieht es nicht**, weil sie gegen den Horizontbeginn
prüft. Deshalb ändert sich mit diesem Abschnitt auch die Wache (29.4).

### 29.2 Die Messung — das Register regelt es nicht

| gesucht | Treffer | was der Treffer sagt |
|---|---:|---|
| `Kapitalpfad` + Beginn/Start/1. Januar/erste Falte | **1** (Z. 4296) | beschreibt den **Schaden**: *„der Kapitalpfad (Registertext 1a) beginnt die erste Falte mit einem Kapitalstand, der aus nicht registrierten Jahren stammt"* |
| `Startkapital` | **0** | — |

⇒ **Der Text unten ist eine Neuaufnahme.** *Fable hatte das in 21c ausdrücklich
offengelassen: „Steht im Register bereits ein Satz, der den Beginn des
Kapitalpfads festlegt, legt ihn mir im Wortlaut vor — dann ist mein Vorschlag
gegenstandslos oder eine Berichtigung dazu, und das kann ich von hier nicht
sehen."*

### 29.3 Der Registertext, zeichengleich

> **Zu 4a / 26:** Der Kapitalpfad eines Bots beginnt am 1. Januar seiner ersten Selektionsfalte mit dem registrierten Startkapital und ohne offene Position. Kein Einstieg liegt vor diesem Datum. Die Grösse der Wirkung ist für diese Regel ohne Belang.

**Quelle des Grundes:** 4a (Falten sind ganze Kalenderjahre) und der Grund von
26 (kein Trade ausserhalb aller Falten im Kapitalpfad). Kein Ergebnis.

⭐ **Der letzte Satz ist Absicht.** Er schliesst aus, dass die Regel später mit
dem Hinweis *„die Wirkung ist ja klein"* aufgeweicht wird — dieselbe Bauart wie
24.3.

### 29.4 Die Wache in TB-30b — geändert gegenüber 21b

⚠️ **Die Fassung aus 21b (Prüfung gegen den Horizontbeginn) ist ERSETZT.** Es
gilt:

> **Wache (TB-30b), angepasst:** frühester Einstieg ≥ **Beginn der ersten Selektionsfalte** (nicht nur ≥ Horizontbeginn). Der Bericht führt je Bot drei Daten nebeneinander: Horizontbeginn, Beginn der ersten Falte, frühester Einstieg.

⚠️ **Ort der Wache unverändert:** in den vier `multi_symbol_optimise.py`, **nicht**
in `auswertung.py` (eingefroren, Abschnitt 0 Z. 31; Fables Rücknahme in 21b).

> ⚠️ **Berichtigt (34.5, TB-82, 22.09.2026):** „in den vier `multi_symbol_optimise.py`"
> lies **„in allen neun"** — Fable 21l, Punkt 4 (b), zeichengleich: *„Die Wache
> „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun**
> `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern."*
> Der Absatz oben bleibt zeichengleich; unverändert gilt: **nicht** in `auswertung.py`.
> Gemessen (TB-82, Beleg M4): heute in keinem der neun eine Wache — Ersteinbau, TB-30b.

> ⭐ **29.4 BERICHTIGT durch R43 (48.11)** (Fable 29b R43, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 29.5 Was noch zu messen ist — nur das Ob, nicht die Wirkung

| | zu messen | ⚠️ |
|---|---|---|
| 1 | Wo der Kapitalpfad der neun Optimierer **heute** beginnt | — |
| 2 | Ob es in den vorhandenen Trade-Listen Einstiege zwischen Horizontbeginn (bzw. erstem handelbarem Tag) und dem 1. Januar der ersten Falte **gibt** | ⛔ **Nur das Ob, nicht die Wirkung auf Kennzahlen** — eine Zahl über Kennzahlen fiele unter 27.1 |
| | | ⚠️ **Und jede Messung an den neun `paper_trading_*.db` läuft auf einer KOPIE** |

⛔ **Nicht Gegenstand dieser Aufgabe.** Eigene Aufgabe, nach TB-78.

---

