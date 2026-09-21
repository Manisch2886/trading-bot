# ERGEBNIS TB-80 — Bedingung (i) rechnet gegen den Horizontbeginn aus Register 28.4 (Mac-Sitzung, 21.09.2026)

**Auftrag:** `docs/auftraege/MAC_TB-80_bedingung_i_auf_asof.md` (Zeiger
`AKTUELLER_AUFTRAG.md` Z. 39 nannte TB-80, gleich der vorangestellten Nummer).
**Ausgeführt am MacBook**, Zweig `main`, Ausgang `41db199` (= `origin/main`
beim Start), **`trading-env/bin/python3`, Python 3.9.6** — jede Messung in
diesem Dokument lief in dieser Umgebung. Commits `120a39d` (Vorgefundenes),
`fd0d505` (Schritt 0), `76c20ec` (1), `cadb968` (2), `4c26e25` (3), `cb7f495`
(4), `62c587e` (5) und der Abgabe-Commit — jeder einzeln gepusht. Belege
`docs/belege/TB-80/`. Geändert: **eine** freigegebene Datei
(`research/vorregistrierung/faltenplan.py`), zwei Tests unter
`research/faltenplan_neun/`, ein neuer Plan **daneben**, `docs/`. ⛔ **Kein
Bot-Code, keine Sperrlisten-Datei, kein `registerdaten.py`, kein Tag, kein
Lauf.**

*In einfacher Sprache, zu Beginn:* Das Programm, das die Auswertungsjahre der
Bots bestimmt, nahm für die vier Aktien-Bots bisher den letzten Kurstag minus
zehn Jahre als Startpunkt. Das Regelwerk nennt seit gestern Abend ein festes
Datum, den 19. September 2016. Das Programm nimmt jetzt dieses Datum. Gemessen,
was sich dadurch ändert: an den Jahren nichts, auf Tagesebene 15 bis 18 Tage.

---

## Schritt 0 — Sichern und Ausgangsstand messen (`120a39d`, `fd0d505`)

| geprüft | Ergebnis |
|---|---|
| `git status --short` beim Start | `M docs/projektfuehrung/ARBEITSWEISE.md` (27/0: Regel „Jeder Kopierblock nennt seinen Empfänger", Abschnitt 0 und 6b) und `M docs/projektfuehrung/UEBERGABE_2026-09-19.md` (1/1: die Zeile „Aktive Freigabe für eine Sperrlisten-Datei" von **keine** auf `faltenplan.py`, TB-80). Vom Betreiber, vor der Sitzung; als eigener Commit `120a39d` gesichert. ⚠️ **Das ist die einzige Zeile mit zweiter Spalte ≠ 0 ausserhalb von `faltenplan.py` und dem TB-72-Test** — siehe Abschlussprüfung 1 |
| `.claude/settings.local.json` | erscheint im Status **nicht** (global ignoriert, wie in TB-78 gemessen) |
| `shasum -a 256`, voller Pfad | `a163c498…36d1ee` `benchmark_drawdowns.json` · `0e54ac5c…32339` `faltenplan.json` · `4549395f…8745d` `benchmark_drawdowns_vt.json` · `19e8cbca…9d24` `faltenplan_tb72.json` — `schritt0_ausgangsstand.txt`. Sechs Dateien `faltenplan*.json` im Repo (ohne `trading-env/`) gezählt, wie der Auftrag warnt |
| `fn.fensteranker(markt)` heute | **`aktien 2016-09-01`**, **`krypto None`** |
| `erste_falte_4a` / `erste_falte` je Bot, aus dem Code gerechnet | `elliott_wave` 2018/2018 · `t3_supertrend` 2018/**2019** · `rsi2_crypto` 2019/2019 · `turtle_soup_crypto` 2018/2018 · `volatility_breakout_crypto` 2018/2018 · `elliott_wave_stocks` 2017/2017 · `rsi2_mean_reversion` 2018/2018 · `turtle_soup_stocks` 2017/2017 · `volatility_breakout` 2018/2018 |
| Speicherstand `faltenplan_stand_vor_tb80.json` | SHA-256 **`19e8cbca…`** — **byteweise gleich `faltenplan_tb72.json`**: der TB-72-Plan war am Ausgang aus dem Code reproduzierbar |
| ⭐ Zusatz, nicht bestellt: frühestes Warm-Datum je Bot (`schritt0_warm_ab.txt`) | Aktien: 2016-09-01 / 2017-06-20 / 2016-10-14 / 2017-03-07; Krypto: 2017-08-17 / 2017-08-17 / 2018-01-14 / 2017-09-16 / 2017-12-22. **Grund:** Die Jahresebene war voraussichtlich stumm (18 Tage Anker-Verschiebung gegen Monate Abstand zum Jahreswechsel); ohne eine Messung darunter hätte die Mutationsprobe in Richtung 1 nichts verwerfen können |

Belegskript `schritt0_ausgangsstand.py` ruft `faltenplan.faltenplan()` auf und
schreibt mit denselben `json.dump`-Einstellungen wie `faltenplan.py::main` —
**ohne `main()`**, das immer nach `faltenplan.json` (Sperrliste Punkt 2)
schreibt.

## Schritt 1 — Die Umstellung (`76c20ec`)

**Registertext, selbst nachgelesen (Fundstellen):** 26.2 Z. 4323–4329
(*„absolutes Datum je Bot … Bots ohne diese Konstante haben keinen Horizont
(Krypto)"*), 28.4 Z. 4684–4687 (**2016-09-19** bei allen vier Aktien-Bots),
Z. 4679–4683 (fünf Krypto-Bots **kein Horizont**), 28.3 (`asof` =
2026-09-19). Abbruchkriterium 5 (Horizontbeginn ≠ 2016-09-19) nicht
eingetreten.

**Was geändert wurde:**

| | |
|---|---|
| `HORIZONTBEGINN = {"aktien": date(2016, 9, 19), "krypto": None}` | ein benanntes Literal je Markt, davor 33 Kommentarzeilen mit Registerfundstelle (26.2, 28.4, 28.3), der Abgrenzung zur Datenuhr, dem Verbot der Konstantenkopie (`T56b.6`) und dem Vermerk **Zwischenstand** (32.5) |
| `horizontbeginn(bot)` | neu — der Wert je Bot über den Markt |
| `erste_falte_4a_messung(bot)` | neu — `{horizontbeginn, warm_ab_fruehestes, erste_falte_4a}`; die bisherige Rechnung von `erste_falte_4a`, mit dem Anker aus `horizontbeginn(bot)` statt `fn.fensteranker(eig["markt"])` |
| `erste_falte_4a(bot)` | **Signatur unverändert**, gibt jetzt `erste_falte_4a_messung(bot)["erste_falte_4a"]` zurück |
| `erste_falte()` | **Konjunktion unverändert** (25.3); nimmt (i) aus `erste_falte_4a_messung` und führt zwei Felder mehr in `herkunft` |
| `_plan()` | zwei neue Felder je Bot: `horizontbeginn`, `erste_falte_4a_warm_ab`; `erste_falte_quelle` nennt 26.2 / 28.4 |
| Modulkopf, Regel 2 (i) | ein Satz ergänzt: Datenhorizont = absolutes Datum aus 26.2 / 28.4, nicht mehr die Datenuhr |
| **Bedingung (ii)** | unberührt — `erste_falte_trockenlauf.erste_falte_nach_3b` wird aufgerufen wie vorher |
| **`fensteranker`** | **nicht entfernt.** Gemessen (`grep -rn fensteranker --include=*.py`): `faltenplan_neun.py:271` (Definition), `:415` und `:445` (`plan_fuer_bot`), `embargo_neun.py:65, 176`, `faltenschranke_messung.py:220, 236`; `faltenplan.py:175` war der einzige Aufrufer im Vorregistrierungs-Pfad |

`numstat` **78 / 16**. ⭐ **Jede der 16 entfernten Zeilen, der Änderung
zugeordnet** (Abschlussprüfung 1):

| entfernte Zeile(n) | Anzahl | verursacht durch |
|---|---:|---|
| Modulkopf Z. 23 `nicht aus einer Konstante; UND (ii) der Loader des Bots macht in ihm an` | 1 | Satz zum Horizontbeginn eingeschoben, Zeile neu umbrochen (Inhalt bleibt, verteilt auf Z. 23–26) |
| Docstring `erste_falte_4a`, Z. 167–172 (`Zehnjahresfenster der Aktien-Bots …` bis `der Aufruf wechselt dorthin.`) | 6 | „Zehnjahresfenster der Aktien-Bots" durch den Horizontbeginn ersetzt, Absatz neu umbrochen; der TB-56b-Satz steht wörtlich weiter |
| Rumpf `erste_falte_4a`, Z. 174–179 (`eig = …`, `beginn = …fensteranker…`, `jahr = …`, `if jahr is None:`, `raise …`, `return jahr`) | 6 | Rechnung nach `erste_falte_4a_messung` verschoben, dort mit `horizontbeginn(bot)` als Anker; `erste_falte_4a` wird Hülle |
| `erste_falte`, Z. 198 `erste_4a = erste_falte_4a(bot)` | 1 | nimmt jetzt `m4a = erste_falte_4a_messung(bot)`, damit `herkunft` Horizont und Warm-Datum führt |
| `_plan`, `erste_falte_quelle` Z. 262–263 (`"Datenhorizont liegt und am 1. Januar den "`, `"Indikator-Vorlauf erfuellt (Datenlage, "`) | 2 | Registerfundstelle 26.2 / 28.4 in den Quellentext eingeschoben, zwei Zeilen neu umbrochen |
| **Summe** | **16** | |

### ⭐ Der Diff von `faltenplan.py`, vollständig (`git diff 41db199..HEAD`)

```diff
diff --git a/research/vorregistrierung/faltenplan.py b/research/vorregistrierung/faltenplan.py
index 66185a8..8a8c3c2 100644
--- a/research/vorregistrierung/faltenplan.py
+++ b/research/vorregistrierung/faltenplan.py
@@ -20,7 +20,10 @@ DIE REGELN (eingefroren)
    (i) es liegt im Datenhorizont des Bots und am 1. Januar ist der
    Indikator-Vorlauf erfuellt - JE BOT aus der Datenlage gerechnet
    (`erste_falte_4a()`, mit der Regel aus `research/faltenplan_neun/`),
-   nicht aus einer Konstante; UND (ii) der Loader des Bots macht in ihm an
+   nicht aus einer Konstante; der Datenhorizont ist seit TB-80
+   (21.09.2026) das absolute Datum je Bot aus Register 26.2 / 28.4
+   (`HORIZONTBEGINN`, unten), nicht mehr die Datenuhr; UND (ii) der
+   Loader des Bots macht in ihm an
    mindestens einem Handelstag mindestens ein Symbol handelbar - gemessen
    im Trockenlauf des Laufcodes (Registertext 3b (a), Lesart H;
    `research/faltenplan_neun/erste_falte_trockenlauf.py`), nicht
@@ -158,25 +161,78 @@ def faltenlaenge_jahre(bot: str) -> tuple:
                        f"{rd.ZWEIJAHRES_SCHWELLE_TRADES}")
 
 
+# ==============================================================================
+# Der Horizontbeginn - Bedingung (i), "im registrierten Datenhorizont des Bots"
+# ==============================================================================
+# Register 26.2 (TB-77, 21.09.2026), Registertext 4a, Praezisierung: "Der
+# Datenhorizont eines Bots ist ein absolutes Datum je Bot: Horizontbeginn =
+# asof (5a) minus RECENT_YEARS_ONLY des Bots; Bots ohne diese Konstante haben
+# keinen Horizont (Krypto). [...] Es gilt fuer alle Symbole des Bots gleich."
+# Der Wert steht in Register 28.4 (TB-78, gueltige Fassung der Tatsachennotiz
+# zu 4d; asof = 2026-09-19 nach 28.3): elliott_wave_stocks, rsi2_mean_reversion,
+# turtle_soup_stocks, volatility_breakout -> 2016-09-19; die fuenf Krypto-Bots
+# -> kein Horizont.
+#
+# Er steht hier so, wie 28.4 ihn fuehrt - als absolutes Datum. NICHT als
+# `asof - RECENT_YEARS_ONLY` gerechnet und NICHT aus
+# strategies/*/multi_symbol_optimise.py gelesen: die vier Dateien stehen auf
+# der Sperrliste, und eine Kopie ihrer Konstante waere der Fehler aus T56b.6
+# (Konstantenkopien). Eine Quelle, keine Kopie.
+#
+# Bis TB-80 (21.09.2026) nahm `erste_falte_4a()` hier
+# `fn.fensteranker(markt)`: zehn Jahre vor dem SPAETESTEN letzten Kurstag des
+# Marktes - die Datenuhr, 2016-09-01 am Stand vom 21.09.2026 (Messung
+# docs/belege/TB-80/schritt0_ausgangsstand.txt). Das ist genau der Bezug, den
+# 26.2 abloest (28.4, "Abgegrenzt, damit es niemand verwechselt").
+# `fensteranker` bleibt in faltenplan_neun bestehen; andere Stellen benutzen
+# ihn (embargo_neun.py, faltenschranke_messung.py, plan_fuer_bot).
+#
+# ⚠️ Zwischenstand: ein benanntes Literal mit Registerfundstelle. Wo der
+# Horizontbeginn dauerhaft lebt (registerdaten.py als registrierte Groesse,
+# Register 26.6 letzte Zeilen / 28.7; aus dem Registertext gelesen; Literal
+# mit Test gegen das Register), ist Entscheidungsvorlage in Register 32.5.
+# research/faltenplan_neun/test_horizontbeginn.py liest den Wert aus dem
+# Registertext 28.4 und vergleicht ihn mit diesem Literal.
+HORIZONTBEGINN = {"aktien": date(2016, 9, 19), "krypto": None}
+
+
+def horizontbeginn(bot: str):
+    """Der Horizontbeginn des Bots (Register 26.2 / 28.4): ein absolutes
+    Datum je Bot; None fuer Bots ohne Horizont (Krypto)."""
+    return HORIZONTBEGINN[fn.BOTS[bot]["markt"]]
+
+
+def erste_falte_4a_messung(bot: str) -> dict:
+    """Bedingung (i) mit ihrer Messung: {horizontbeginn, warm_ab_fruehestes,
+    erste_falte_4a} - damit im Plan steht, gegen welches Datum (i) gerechnet
+    wurde und ab welchem Tag das erste Symbol warm ist, nicht nur das Jahr."""
+    horizont = horizontbeginn(bot)
+    beginn = fn.symbolbeginn(bot, horizont)
+    jahr = fn._ungebremstes_faltenjahr(beginn)
+    if jahr is None:
+        raise ValueError(f"{bot}: kein Symbol mit Kursdaten - keine erste Falte")
+    warm = min(w for _, w in beginn.values() if w is not None)
+    return {"horizontbeginn": horizont.isoformat() if horizont else None,
+            "warm_ab_fruehestes": warm.isoformat(),
+            "erste_falte_4a": jahr}
+
+
 def erste_falte_4a(bot: str) -> int:
     """Bedingung (i): das erste Kalenderjahr, in dem am 1. Januar Universum
     und Indikator-Vorlauf vorliegen - Registertext 4a, je Bot aus der
     Datenlage. Bis TB-72 hiess diese Funktion `erste_falte`.
 
     Gerechnet mit der Regel aus `faltenplan_neun` (Kursdaten am 1. Januar,
-    Zehnjahresfenster der Aktien-Bots, Indikator-Vorlauf in Balken). Bis zur
-    Registerberichtigung TB-56b traegt `faltenplan_neun.erstes_faltenjahr`
-    selbst noch die Schranke `FRUEHESTE_FALTE`; deshalb wird hier die
-    ungebremste Fassung derselben Regel aufgerufen. Sobald TB-56b die
-    Schranke dort entfernt hat, ist `erstes_faltenjahr` diese Funktion, und
-    der Aufruf wechselt dorthin.
+    Indikator-Vorlauf in Balken) ab dem Horizontbeginn des Bots
+    (`HORIZONTBEGINN`, Register 26.2 / 28.4 - seit TB-80; bis dahin ab der
+    Datenuhr `fn.fensteranker`, dem Zehnjahresfenster vor dem letzten
+    Kurstag). Bis zur Registerberichtigung TB-56b traegt
+    `faltenplan_neun.erstes_faltenjahr` selbst noch die Schranke
+    `FRUEHESTE_FALTE`; deshalb wird hier die ungebremste Fassung derselben
+    Regel aufgerufen. Sobald TB-56b die Schranke dort entfernt hat, ist
+    `erstes_faltenjahr` diese Funktion, und der Aufruf wechselt dorthin.
     """
-    eig = fn.BOTS[bot]
-    beginn = fn.symbolbeginn(bot, fn.fensteranker(eig["markt"]))
-    jahr = fn._ungebremstes_faltenjahr(beginn)
-    if jahr is None:
-        raise ValueError(f"{bot}: kein Symbol mit Kursdaten - keine erste Falte")
-    return jahr
+    return erste_falte_4a_messung(bot)["erste_falte_4a"]
 
 
 def erste_falte(bot: str, laenge: int = None, schnitt: date = None) -> tuple:
@@ -195,13 +251,16 @@ def erste_falte(bot: str, laenge: int = None, schnitt: date = None) -> tuple:
         laenge = faltenlaenge_jahre(bot)[0]
     if schnitt is None:
         schnitt = date.fromisoformat(rd.GO_LIVE_SCHNITT)
-    erste_4a = erste_falte_4a(bot)
+    m4a = erste_falte_4a_messung(bot)
+    erste_4a = m4a["erste_falte_4a"]
     kandidaten = _jahresfalten(erste_4a, schnitt, laenge)
     jahr, messung = eft.erste_falte_nach_3b(bot, kandidaten)
     if jahr is None:
         raise ValueError(f"{bot}: der Loader macht in keiner Falte ab {erste_4a} "
                          f"ein Symbol handelbar - keine erste Falte")
     return jahr, {"erste_falte_4a": erste_4a,
+                  "horizontbeginn": m4a["horizontbeginn"],
+                  "erste_falte_4a_warm_ab": m4a["warm_ab_fruehestes"],
                   "H_je_gepruefter_falte": [{"falte": f["name"], "H": f["H"]}
                                             for f in messung]}
 
@@ -259,8 +318,9 @@ def _plan(bot: str, mess: dict, markt: str) -> dict:
         "erste_falte": erste,
         "erste_falte_quelle": ("Registertext 4a in der Neufassung als Konjunktion "
                                "(TB-72, 20.09.2026): erstes Kalenderjahr, das (i) im "
-                               "Datenhorizont liegt und am 1. Januar den "
-                               "Indikator-Vorlauf erfuellt (Datenlage, "
+                               "Datenhorizont liegt - dem absoluten Datum je Bot aus "
+                               "Register 26.2 / 28.4 (TB-80, 21.09.2026) - und am "
+                               "1. Januar den Indikator-Vorlauf erfuellt (Datenlage, "
                                "research/faltenplan_neun; keine Konstante) UND (ii) in "
                                "dem der Loader des Bots mindestens ein Symbol "
                                "handelbar macht - Trockenlauf des Laufcodes, "
@@ -268,6 +328,8 @@ def _plan(bot: str, mess: dict, markt: str) -> dict:
                                "Regel, der Trockenlauf ihre operative Form, der Plan "
                                "eine Ableitung daraus"),
         "erste_falte_4a": herkunft["erste_falte_4a"],
+        "horizontbeginn": herkunft["horizontbeginn"],
+        "erste_falte_4a_warm_ab": herkunft["erste_falte_4a_warm_ab"],
         "erste_falte_trockenlauf_H": herkunft["H_je_gepruefter_falte"],
         "falten": falten,
         "selektionsfalten": [f["name"] for f in falten if f["rolle"] == "selektion"],
```

## Schritt 2 — Die Wirkung, gemessen (`cadb968`)

> ⭐⭐ **Die Regel stand vor der Messung.** Abschnitt 26.2: Commit `729443c`,
> 21.09.2026 **17:13** Ortszeit (der Auftrag nennt 19:19; der Commit liegt
> früher); 28.4: Commit `003f894`, **19:20**. Diese Messung: 21.09.2026,
> 20:21 UTC = **22:21** Ortszeit. **Was herauskommt, ist keine Wahl** — Bauart
> 24.3.

`research/vorregistrierung/ergebnisse/faltenplan_tb80.json`, SHA-256
**`2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794`**, zwei
Läufe (20:21 und 20:23 UTC) byteweise gleich; Belegskript
`schritt2_faltenplan_tb80.py`, ohne `main()`. `faltenplan.json`
(`0e54ac5c…`) und `faltenplan_tb72.json` (`19e8cbca…`) **byteweise
unverändert**.

| Bot | `erste_falte_4a` vorher | nachher | `erste_falte` vorher | nachher | Selektionsfalten vorher → nachher |
|---|---:|---:|---:|---:|---|
| `elliott_wave` | 2018 | 2018 | 2018 | 2018 | 4 → 4 |
| `t3_supertrend` | 2018 | 2018 | 2019 | 2019 | 7 → 7 |
| `rsi2_crypto` | 2019 | 2019 | 2019 | 2019 | 7 → 7 |
| `turtle_soup_crypto` | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `volatility_breakout_crypto` | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `elliott_wave_stocks` | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `rsi2_mean_reversion` | 2018 | 2018 | 2018 | 2018 | 8 → 8 |
| `turtle_soup_stocks` | 2017 | 2017 | 2017 | 2017 | 9 → 9 |
| `volatility_breakout` | 2018 | 2018 | 2018 | 2018 | 8 → 8 |

**0 Bots mit Änderung** an `erste_falte_4a` / `erste_falte` /
Selektionsfalten; **0** geänderte, neue oder entfallene Falten (Grenzen,
Rolle, Training, Embargo). Ohne die zwei neuen Felder und ohne den Text
`erste_falte_quelle` sind alle neun Bots **zeichengleich** mit Schritt 0.

**Eine Ebene tiefer** (frühestes Warm-Datum ab dem Anker):

| Bot | Anker vorher | Horizontbeginn nachher | warm ab vorher | nachher | Verschiebung |
|---|---|---|---|---|---:|
| fünf Krypto-Bots | `None` | `None` | wie Schritt 0 | gleich | **+0 Tage** |
| `elliott_wave_stocks` | 2016-09-01 | 2016-09-19 | 2016-09-01 | 2016-09-19 | +18 |
| `rsi2_mean_reversion` | 2016-09-01 | 2016-09-19 | 2017-06-20 | 2017-07-06 | +16 |
| `turtle_soup_stocks` | 2016-09-01 | 2016-09-19 | 2016-10-14 | 2016-10-31 | +17 |
| `volatility_breakout` | 2016-09-01 | 2016-09-19 | 2017-03-07 | 2017-03-22 | +15 |

⭐ **Krypto: kein Jahr, kein Tag verändert** — Abbruchkriterium 4 nicht
eingetreten. Die Einträge der fünf Krypto-Bots unterscheiden sich vom
Ausgangsstand nur im Text `erste_falte_quelle` und im neuen Feld
`erste_falte_4a_warm_ab` (Feld-für-Feld-Vergleich in `schritt2_wirkung.txt`).
⚠️ Die erste Fassung des Belegskripts meldete für diesen Vergleich `False`,
weil sie den geänderten Quellentext mitverglich; die zweite Fassung nennt die
abweichenden Felder einzeln — der Befund ist derselbe, die Zeile lügt nicht
mehr durch Weglassen.

⛔ **Nicht gemessen:** keine Kennzahl eines Parametersatzes (27.1).

## Schritt 3 — Mutationsprobe in beide Richtungen (`4c26e25`)

`schritt3_mutationsprobe.py`, **im Speicher** (`HORIZONTBEGINN` ersetzt,
`faltenplan.py` unverändert — `git status` vor und nach dem Lauf ohne `M`),
**49/49**, `rc 0`, 20:25 UTC.

| Richtung | Ergebnis |
|---|---|
| **1 — Datenuhr wieder eingesetzt** (`{markt: fn.fensteranker(markt)}` = `aktien 2016-09-01`) | **Alter Stand Bot für Bot**: `erste_falte_4a`, `erste_falte`, Selektionsfalten, alle Falten, Warm-Daten auf Tagesebene = Schritt 0 (27 Proben). Gegen `faltenplan_tb80.json`: **alle vier Aktien-Bots** anders in `horizontbeginn` und `erste_falte_4a_warm_ab`; fünf Krypto-Bots zeichengleich |
| ⚠️ **Wo sie nicht beisst** | Auf **Jahresebene** sind alter und neuer Stand gleich — dort kann Richtung 1 nichts verwerfen. Sie beisst **auf Tagesebene**, und genau dafür wurde das Warm-Datum in Schritt 0 vorher gemessen und in den Plan aufgenommen. **Das steht so in 32.4; es wird nicht als Jahresbefund verkauft** |
| **2 — Horizontbeginn +1 Jahr** (`aktien 2017-09-19`) | **Vier erste Falten bewegen sich**: `elliott_wave_stocks` 2017→2018, `rsi2_mean_reversion` 2018→2019, `turtle_soup_stocks` 2017→2018, `volatility_breakout` 2018→2019 — `erste_falte_4a` **und** `erste_falte` (Trockenlauf `H` 136/137 in der ersten Kandidatenfalte, Konjunktion hält); Krypto unverändert |
| Original wiederhergestellt | `erste_falte_4a_messung` je Bot = `faltenplan_tb80.json`, 9/9 |

Abbruchkriterium 3 (eine Richtung beisst nicht) **nicht eingetreten** — mit
der Einschränkung zur Jahresebene, wie oben benannt.

## Schritt 4 — Der Test (`cb7f495`)

**Wahl, begründet:** ein **eigener Test** `research/faltenplan_neun/test_horizontbeginn.py`
neben `test_erste_falte_trockenlauf.py`. Der bestehende Test prüft Bedingung
(ii) — die Ableitung aus dem Trockenlauf — und läuft drei Minuten mit neun
Kindprozessen; sein Docstring sagt ausdrücklich, dass (i) *„nicht Gegenstand
dieses Tests (TB-74)"* ist. Ein Test je Bedingung hält die beiden Gegenstände
auseinander und den (i)-Test schnell (rund 40 s, davon 35 s der Plan mit
Trockenlauf für Prüfung 3).

| Nr. | zu prüfen | wie | Ergebnis |
|---|---|---|---|
| 1 | Aktien-Bots gegen **2016-09-19**, nicht gegen die Datenuhr | `erste_falte_4a_messung` nennt 2016-09-19; Warm-Datum ≥ 2016-09-19; **im Speicher** mit der Datenuhr als Anker ändert sich das Warm-Datum jedes Aktien-Bots (falls Datenuhr und Horizont an einem künftigen Datenstand zusammenfallen, meldet der Test das als FEHL statt zu raten); Quelltext von `erste_falte_4a_messung` ohne `fensteranker`; `HORIZONTBEGINN` ist ein `date`-Literal | 14/14 |
| 2 | fünf Krypto-Bots unverändert gegenüber Schritt 0 | liest `faltenplan_stand_vor_tb80.json` und `schritt0_warm_ab.txt`; Jahr, Warm-Datum, `horizontbeginn is None` | 16/16 |
| 3 | Konjunktion `erste_falte ≥ erste_falte_4a` bei allen neun | `faltenplan()` mit Trockenlauf; dazu Plan = Messung in Horizont und Warm-Datum | 18/18 |
| 4 | ⭐ **Literal = Register** | liest die Tabelle unter `### 28.4` (Spalte Horizontbeginn, Datum bzw. „kein Horizont" → `None`) je Bot und vergleicht mit `faltenplan.horizontbeginn(bot)`; Gegenrichtung +1 Jahr bewegt vier erste Falten, Krypto nicht; Original wiederhergestellt | 13/13 |

**61/61**, `trading-env/bin/python3` 3.9.6 (`schritt4_test_horizontbeginn.txt`).
⭐ **Gegenprobe (`B1`, Prinzip 12):** Literal per `sed` auf `2016-09-01`
gesetzt → **rot, 15 Prüfungen** (1: Horizont, Warm-Datum = Datenuhr, kein
Literal-Muster; 4: Code 2016-09-01 ≠ Register 2016-09-19, Original nicht
wiederhergestellt) — `schritt4_gegenprobe_test_rot.txt`; Datei danach mit
`git checkout` zurückgesetzt, `git status` ohne `M`.

⚠️ **Ein Umgebungsstolperstein, wie `docs/UMGEBUNGEN.md` warnt:** der erste
Entwurf brach auf 3.9.6 mit `SyntaxError: f-string: unmatched '['` — ein
f-String mit denselben Anführungszeichen innen (`f'{plan[b]['erste_falte']}'`),
das 3.12 erlaubt und 3.9 nicht. Behoben mit `%`-Formatierung, vor dem Commit.

**`test_erste_falte_trockenlauf.py`** (8/2): die Mutation in Teil D füllt jetzt
die zwei neuen `herkunft`-Schlüssel, sonst wäre die mutierte Kopie mit
`KeyError` in `_plan` gescheitert statt an der Mutation — eine Probe, die aus
dem falschen Grund scheitert, belegt nichts. Gelaufen: **50/50** (3 min,
`schritt4_test_erste_falte_trockenlauf.txt`); Teil D beisst weiter
(`t3_supertrend` 2018 statt 2019). Die zwei entfernten Zeilen sind die alte
zweizeilige `MUTATION`-Konstante.

## Schritt 5 — Registerabschnitt 32 (`62c587e`)

`grep -cE "^## 32\."` vorher **0** (Abbruchkriterium 6 nicht eingetreten).
`numstat` **211 / 0**, append-only nach `---` hinter 31.7. Inhalt nach
Auftrag: 32.1 Befund mit Fundstellen (gemessen, mit Zeilennummern am Stand
`41db199`), 32.2 Wirkung als Tabelle ohne Bewertung, 32.3 Hashes, 32.4
Mutationsprobe mit dem Vermerk zur Jahresebene, 32.5 Entscheidungsvorlage
(drei Wege mit Preis, keine Empfehlung), 32.6 nicht getan, „In einfacher
Sprache". Die Commit-Zeiten von 26 und 28 stehen **gemessen** (17:13 / 19:20),
nicht aus dem Auftrag übernommen (19:19).

## Schritt 6 — Abschlussprüfung (`schritt6_abschluss.txt`)

| | Soll | Ist |
|---|---|---|
| 1 | `numstat` zweite Spalte 0 überall ausser `faltenplan.py` | `faltenplan.py` **78 / 16**, jede der 16 Zeilen oben zugeordnet. ⚠️ Zwei weitere Dateien mit zweiter Spalte ≠ 0: `UEBERGABE_2026-09-19.md` **1 / 1** (Betreiber, vor der Sitzung, `120a39d`) und `test_erste_falte_trockenlauf.py` **8 / 2** (alte `MUTATION`-Konstante, Schritt 4 — der Test ist im Auftrag zur Erweiterung freigegeben). Alle anderen 16 Dateien **0** |
| 2 | Diff von `faltenplan.py` vollständig hier | oben, 146 Zeilen |
| 3 | drei Sperrlisten-Hashes, voller Pfad | `a163c498…` · `0e54ac5c…` · `4549395f…` **unverändert** (Schritt 0, 2, 6) |
| 4 | `faltenplan_tb72.json` | `19e8cbca…` **unverändert** gegen Schritt 0 |
| 5 | nichts ausserhalb `docs/`, `faltenplan.py`, `research/faltenplan_neun/`, neuer Plan | `git diff --stat 41db199..HEAD` mit diesen vier Ausschlüssen: **leer** |
| 6 | `##` 26…32 je genau einmal | `grep`: 1/1/1/1/1/1/1 |
| 7 | `git status --porcelain` nach dem letzten Commit | siehe Abgabe-Commit unten — erwartet leer (`settings.local.json` global ignoriert, erscheint nicht) |
| 8 | zweite unabhängige Zählung für 6 | python über `^## (\d+)\.`: `{26:1 … 32:1}`, doppelt `[]`, höchste **32** |

Kein Basislauf, keine Datenstand-Messung, keine DB-Quersummen — nicht
bestellt; der Auftrag rechnet nur den Faltenplan.

## Abweichungen vom Auftrag — mit Begründung

| | Auftrag | tatsächlich |
|---|---|---|
| 1 | „zweite Spalte 0 überall ausser `faltenplan.py`" | zusätzlich `UEBERGABE_2026-09-19.md` 1/1 (Betreiber-Änderung, in Schritt 0 zum Commit bestellt) und `test_erste_falte_trockenlauf.py` 8/2 (Testanpassung, nötig, damit dessen Mutationsprobe nicht am neuen Feld statt an der Mutation scheitert). Beide gemeldet, keine Löschung dieser Sitzung an fremdem Inhalt |
| 2 | Mutationsprobe Richtung 1 „beisst" | beisst **nur auf Tagesebene** — auf Jahresebene sind alt und neu identisch (0 Bots mit Änderung). Deshalb zwei nicht bestellte Zutaten: die Warm-Datum-Messung in Schritt 0 und zwei neue Planfelder (`horizontbeginn`, `erste_falte_4a_warm_ab`). Ohne sie hätte die Probe nichts verwerfen können, und der Auftrag hätte nach Kriterium 3 abgebrochen werden müssen — für eine Umstellung, die das Register verlangt und die nachweislich wirkt. **Nicht abgebrochen**, im Register 32.4 als Einschränkung ausgewiesen |
| 3 | „Ein Literal je Markt" | so gebaut (`HORIZONTBEGINN` je Markt); Register 28.4 führt das Datum **je Bot** — `horizontbeginn(bot)` bildet den Bot über seinen Markt ab. Der Test vergleicht je Bot |
| 4 | Test nennt die Umgebung | genannt: `trading-env/bin/python3`, Python 3.9.6, in jeder Beleg-Ausgabe erste Zeilen |
| 5 | Abschnitt 32 nennt 26.2 „19:19 Ortszeit eingetragen" | Commit-Zeit gemessen: 17:13 (`729443c`); 28.4: 19:20 (`003f894`). Die gemessene Zeit steht im Register, die Auftragszeit daneben |
| 6 | Belege als `.txt` | zusätzlich die Belegskripte (`.py`) committet, Muster TB-72 — damit die Zahl reproduzierbar ist, nicht nur abgelegt |

**Rückfragen an den Betreiber: keine** — also auch keine Antwort, die wörtlich
hineingehörte.

## Fehler → Regel

| Fehler dieser Sitzung | Regel |
|---|---|
| Der erste Testentwurf nutzte eine f-String-Form, die 3.9 nicht kennt (`SyntaxError`) | **Ein Test wird in der Betriebsumgebung geschrieben und dort zuerst gestartet** — auch Syntax ist versionsabhängig, nicht nur Bibliotheken (`docs/UMGEBUNGEN.md`) |
| Die erste Fassung des Schritt-2-Skripts meldete „Krypto zeichengleich: False", weil sie einen geänderten Beschreibungstext mitzählte | **Ein Gleichheitsvergleich nennt die Felder, die abweichen** — ein `False` ohne Feldliste ist derselbe Fehler wie eine Kennzahl ohne Bezugsmenge (`K4d`) |
| `pgrep -f`-Warteschleifen trafen ihren eigenen Shell-Umschlag und liefen endlos (dreimal) | bekannt aus TB-46b („`pkill -f` trifft eigene Shell"); **ein Prozess wird über `ps` mit `[x]`-Muster oder über seine Ausgabedatei erkannt, nicht über `pgrep -f`** |

## ⚠️ Offen — nicht Teil dieses Auftrags

- **32.5, Entscheidungsvorlage:** wo der Horizontbeginn dauerhaft lebt — `registerdaten.py` (Registeränderung, Betreiber) · Registertext-Parser · Literal mit Test (heute). Ohne Empfehlung.
- **Der Plan nach 4a ins Register** (Abschnitt 30: genau eine Abbild-Datei als neuer Sperrlistenpunkt) — `faltenplan_tb80.json` liegt daneben, ist kein Registertext; Freigabe Betreiber.
- **`fensteranker`** in `plan_fuer_bot`, `embargo_neun.py`, `faltenschranke_messung.py`: dort weiter die Datenuhr — ob das für diese Messwerkzeuge richtig bleibt, ist eine eigene Frage.
- **TB-30b:** die vier Optimierer (`entry_cutoff` je Bot aus dem Register) und die Wache gegen den Beginn der ersten Falte (29).
- **Journal-Nachträge** (20g)–(20m) und die Backlog-Zeile (`K4t`, nach `K4s`): nicht bestellt.
- `test_vorregistrierung.py` nicht gelaufen (nicht bestellt; laut Memory seit TB-56b an der Sperrliste 10.4 rot, unabhängig von dieser Änderung).

## In einfacher Sprache

**Was gemacht wurde:** Das Programm, das für jeden Bot festlegt, welche
Kalenderjahre ausgewertet werden, nahm für die vier Aktien-Bots bisher einen
beweglichen Startpunkt: den letzten Kurstag in den Daten, zehn Jahre zurück.
Das Regelwerk nennt seit dem 21.09. ein festes Datum — den 19. September 2016.
Das Programm nimmt jetzt dieses Datum, und zwar so, wie es im Regelwerk steht:
nicht ausgerechnet, nicht aus den Bot-Programmen abgeschrieben. Ein Test liest
die Tabelle im Regelwerk und prüft, dass beide übereinstimmen; setzt man das
alte Datum wieder ein, wird er rot.

**Was sich ändert:** An den Jahren nichts. Alle neun Bots beginnen in
denselben Jahren wie vorher, mit denselben Auswertungsjahren. Achtzehn Tage
weniger Vorlauf reichten bei keinem Bot, um ein Jahr zu verlieren. Auf
Tagesebene sieht man es: der Tag, an dem das erste Wertpapier eines
Aktien-Bots bereit ist, liegt jetzt 15 bis 18 Tage später. Bei den fünf
Krypto-Bots, die kein Fenster haben, ändert sich nicht ein Tag — das war der
Nachweis, dass die Änderung nur trifft, was sie treffen soll.

**Was ehrlich gesagt werden muss:** Weil sich an den Jahren nichts ändert,
kann die Probe „altes Datum wieder einsetzen" auf Jahresebene nichts
beweisen. Sie beweist es eine Ebene tiefer, an den Tagen — und dafür wurde
diese Ebene vor der Änderung gemessen und in den Plan aufgenommen. Die
Gegenprobe in die andere Richtung (Datum ein Jahr später) bewegt alle vier
Aktien-Bots um ein Jahr; die Umstellung wirkt also, sie kostet heute nur
nichts.

**Was nicht gemacht wurde:** Kein Bot-Programm angefasst, keine gesperrte
Datei verändert, kein Lauf, keine Bewertung von Einstellungen. Die Frage, wo
das Datum dauerhaft hingehört, ist aufgeschrieben, mit drei Wegen und ihrem
Preis — entschieden wird sie vom Betreiber.

*Geschrieben 21.09.2026 von der Mac-Sitzung TB-80 selbst. Abgabe-Commit und
`porcelain`-Nachweis: siehe Journalblock CH und der letzte Commit dieser
Aufgabe.*
