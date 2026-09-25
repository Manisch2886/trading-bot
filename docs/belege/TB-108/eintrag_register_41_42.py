"""TB-108: Registerabschnitte 41 und 42 und zwanzig Marken am alten Ort.

Bauart TB-96 (`docs/belege/TB-96/eintrag_register_40.py`), erweitert auf
mehrere Quellen. Setzt Fables Texte EIN statt sie abzutippen:
  ⟦Z:<q>:n⟧        -> Zeile n der Quelle q, ohne fuehrendes "> " (die Vorlage setzt "> ")
  ⟦T:<q>:n|text⟧   -> text, der wortgleich in Zeile n der Quelle q stehen muss
und schreibt jedes Zitat nach zitate.json fuer d2_zitate.py.

Jede Marke wird hinter einer Ankerzeile eingefuegt, die innerhalb ihres
Zielabschnitts (Kopfzeile bis zur naechsten Kopfzeile) GENAU EINMAL vorkommen
muss - sonst Abbruch ohne Schreiben. Nichts wird ersetzt oder entfernt; keine
Marke liegt zwischen `## 10.` und `## 11.` (Sonde, Pruefung (ii)).
Aufruf aus der Repo-Wurzel, genau einmal:
  trading-env/bin/python3 docs/belege/TB-108/eintrag_register_41_42.py
"""
import json
import os
import re

# TB108_PROBE: Probelauf gegen eine Kopie (Pfad), bevor das Register geschrieben wird
REG = os.environ.get("TB108_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-108/"
P = "docs/projektfuehrung/"
QUELLEN = {
    "23f": P + "FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md",
    "24b": P + "FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md",
    "24c": P + "FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md",
    "24d": P + "FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md",
    "25a": P + "FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md",
    "25b": P + "FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md",
    "25c": P + "FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md",
}
Q = {k: open(v, encoding="utf-8").read().split("\n") for k, v in QUELLEN.items()}
zitate = []


def setze(text, wo):
    def zeile(m):
        k, n = m.group(1), int(m.group(2))
        s = Q[k][n - 1]
        assert s.strip() and s.strip() != ">", (k, n)
        s = s[2:] if s.startswith("> ") else s
        zitate.append({"art": "zeile", "quelle": QUELLEN[k], "zeile": n, "text": s, "wo": wo})
        return s

    def teil(m):
        k, n, t = m.group(1), int(m.group(2)), m.group(3)
        assert t in Q[k][n - 1], "Teilzitat nicht in %s Z. %d: %r" % (k, n, t[:60])
        zitate.append({"art": "teil", "quelle": QUELLEN[k], "zeile": n, "text": t, "wo": wo})
        return t
    text = re.sub(r"⟦Z:(\w+):(\d+)⟧", zeile, text)
    text = re.sub(r"⟦T:(\w+):(\d+)\|([^⟧]+)⟧", teil, text)
    assert "⟦" not in text and "⟧" not in text, text[text.find("⟦"):][:80]
    return text


MARKEN = [
    # (Kopfzeile des Zielabschnitts, Ankerzeile (Anfang), Text, Leerzeile davor, Leerzeile danach, Ort)
    ("### 5.1 Die Regeln", "   > Registereintrag **und** die Anpassung von `G6` im selben Auftrag.", """\
   > ⭐ **Zwei Leser, ein Parser (41.1 A6, Fable 24b, TB-108, 25.09.2026):**
   > Diese Zeile lesen seit TB-97 **zwei** Stellen — `G6` in
   > `test_vorregistrierung.py` und die Krisenfalten in `beispieldaten.py` —
   > über **eine** Funktion, `beispieldaten.py::jahre_aus_register_5_1_nr_4`.
   > Ein zweiter Parser derselben Zeile wäre ein zweiter Ort (Fable 24b B4).
   > Die Warnung oben gilt für beide Leser.""", True, False, "5.1 Nr. 4"),
    ("### 5.4 Welche Bots Zweijahres-Falten bekommen", "> Regeltext oben bleibt zeichengleich.", """\
> ⭐⭐ **Reichweite und `elliott_wave` (41.2 B1, 41.3 C4, Fable 24c/24d, TB-108,
> 25.09.2026):** Der Grundsatz dieses Abschnitts — keine Festlegung vor dem Lauf
> aus Grössen, die vom Positionslimit **oder von der Ausführung** abhängen — gilt
> für **alle** Festlegungen, die vor dem Lauf stehen (Faltenlänge, Purge,
> Embargo, Trainingsende, Rastergrenzen); Herleitungen aus Trades verwenden
> gefundene Trades (Registertext in **41.2, B1**). Bei `elliott_wave`, dessen
> Positionslimit keine Rasterachse ist (2.4), greift „gefundene" über die
> Ausführung (Kapitalschranke) — Tatsachennotiz in **41.3, C4**. Der Regeltext
> oben bleibt zeichengleich.""", True, False, "5.4"),
    ("## 6. Die Plateau-Regel", "1.024 auf 384.", """\
> ⭐ **Benennung dieses Zustands und unbekannter Bedingungstext (42.3 F1, Fable
> 25c, TB-108, 25.09.2026):** Ein Bot, bei dem alle Zellen existieren, hat
> „keine Rasterbedingung (Abschnitt 6)" — nicht „keine Nebenbedingung" und
> nicht „Abschnitt 4" (Abschnitt 4 ist die Drawdown-Bedingung). Ein nicht
> leerer Bedingungstext, den der Code nicht als Rasterbedingung erkennt, endet
> mit **2**, unabhängig vom Modus; gedeutet wird er an **einer** Stelle.
> Wortlaut in **42.3, F1**; die zweite Deutungsstelle (`registerdaten.py:605`)
> bleibt bis 40.8 (h). Der Absatz oben bleibt zeichengleich.""", True, False, "6"),
    ("### 11.3 Zwei Achsen brauchen eine Durchreichung", "  nicht im Optimierer.", """\
> ⭐⭐ **Stand der Voraussetzungen aus Abschnitt 11 (42.3 F3, 42.4 G1, Fable 25c,
> TB-108, 25.09.2026):** **11.1 ist geschlossen** (TB-105, `f524327`:
> `regimewache.pruefe_einbau()` 3 von 3; vorher rechnete `t3_supertrend` ohne
> BTCUSDT still weiter, gemessen). **11.2 und 11.3 sind offen** (TB-30b). Wer
> „Abschnitt 11 erfüllt" liest, liest zu viel. Der Text oben bleibt
> zeichengleich.""", True, False, "11"),
    ("## 12. Der Vollständigkeitstest", "> der Test zählt heute 165 Prüfungen (40.1).", """\
> ⭐⭐ **Berichtigung und zwei Regeln (41.1 A1, A4, A5, A7, Fable 24b, TB-108,
> 25.09.2026):** „davon acht Mutationsproben" lies nach Fables Berichtigung
> „davon **sieben Mutationsproben, H1 bis H7** (Teil H)"; H0 ist der Grundlauf,
> F4 keine Mutationsprobe. Die **Namen** sind Registertext, die Zahl der
> Prüfungen eine Tatsachennotiz mit Stand (heute 196, 41.1 A1). Jede
> Mutationsprobe beisst **allein** (41.1, A4) — ⚠️ H6 tut es bis heute nicht,
> vor dem Tag offen. Störproben werden in **beide** Richtungen geführt (41.1,
> A5). Der Testrahmen (`beispieldaten.py`) deckt seit 24c beide Faltenlängen ab
> (41.1, A7). Die Sätze oben bleiben zeichengleich.""", True, False, "12"),
    ("### 15.4 Registertext 2", "   die Messung ihn ausweist. Bei `t3_supertrend`: 11,21 → 12 → **13**.", """\
> ⭐ **Der Deckel von `t3_supertrend` wird aus gefundenen Trades neu gerechnet
> (41.3 C2, Fable 24d, TB-108, 25.09.2026):** Die Zeile `t3_supertrend` oben
> stammt aus **ausgeführten** Positionen. Nach Fables Präzisierung zu 2d
> (Fassung 16.6) wird das 95. Perzentil der Haltedauer aus den **gefundenen**
> Trades gerechnet (Signalpfad), plus 1, aufgerundet nach Anmerkung 4; **kein**
> Maximum über das Raster. Neu gerechnet wird, wenn die neuen Listen vorliegen
> (42.6 (5)). Die Tabelle bleibt zeichengleich.""", True, False, "15.4"),
    ("### 16.6 Registertext 2d", "> Zeitraum — das ist kein Fehler, sondern seine Haltedauer.", """\
> ⭐⭐ **Zwei Präzisierungen zu 2d und eine Rücknahme (41.3 C1–C3, Fable 24d,
> TB-108, 25.09.2026):** (1) Der Deckel für Bots ohne Zeitbremse — das 95.
> Perzentil der Haltedauer plus 1 — wird aus den **gefundenen** Trades
> gerechnet, nicht als Maximum über das Raster; er ist keine Leckschranke, das
> Leck schliesst die Attribution je Position (**41.3, C2**). (2) Die Bedingung
> („keine vor Go-Live eröffnete Position mehr offen") wird im Selektionslauf
> **für den Gewinner auf dessen eigenen simulierten Positionen** ausgewertet;
> das Journal des Papierpfads ist dafür keine Quelle (**41.3, C3**). (3) Fables
> Berichtigung aus 24c, `purge_tage` als Schranke über das Raster zu bemessen,
> ist zurückgenommen und nie eingetragen worden (**41.2 B2, 41.3 C1**). Der
> Registertext oben bleibt zeichengleich.""", True, False, "16.6"),
    ("## 19. Registertext 5e", "> Selektionsmodus unzulässig.**", """\
> ⭐⭐ **Ergänzungen zu 5e (41.1 A10, 41.2 B5, 41.3 C6, 42.1 D1, Fable 24b–25a,
> TB-108, 25.09.2026):** Unter dem Selektionsmodus gibt es **keinen Rückfall
> auf eingebaute Voreinstellungen**, gleich welcher Art; eine fehlende Eingabe
> ist Rückgabewert 2 (**41.1, A10**). Jedes Modul des Laufbereichs bezieht
> Kurs- und Universumspfade **über den Resolver** (`shared/paths.py`, direkt
> oder über `strategy_paths.get_strategy_paths()`) (**41.2 B5**, Fundstelle
> nach **42.1 D1**). Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des
> Resolvers; Hilfsordner und Ersatzwurzeln tragen keinen Nachweisteil
> (**41.3, C6**). Der Registertext oben bleibt zeichengleich.""", True, False, "19 (5e)"),
    ("## 19. Registertext 5e", "| Im Regelbetrieb gilt nichts davon |", """\
> ⭐⭐ **Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen; und die
> Ausnahme für registrierte Protokolle (42.2 E2, 42.3 F8, Fable 25b/25c, TB-108,
> 25.09.2026):** Die Sauberkeitsprüfung des Arbeitsbaums erstreckt sich künftig
> auf **jeden Pfad des Laufbereichs**, nicht nur auf die drei Pfade in der
> Zeile „Arbeitsbaum sauber" oben (Registertext in **42.2, E2**; `data/` bleibt
> ausgenommen). ⚠️ **Heute nicht vollzogen** — `ARBEITSBAUM_PFADE` ist
> unverändert; die Erweiterung ist Tag-Vorbedingung und eigener Auftrag.
> **Registrierte Protokolle** (heute nur
> `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`) sind davon
> ausgenommen wie `data/`; der Kettenhash ersetzt dort die Sauberkeit
> (**42.3, F8**). Diese Ausnahme steht damit **vor** dem Erweiterungsauftrag im
> Register, wie Fable es verlangt. Tabelle und Text oben bleiben zeichengleich.""", True, False, "19 (Tabelle)"),
    ("### 23.5 Was der Code seit heute tut", "| `registerdaten.MINDESTTRAINING_JAHRE` |", """\
> ⭐ **Stand der letzten Zeile (42.2 E4, Fable 25b/25c, TB-108, 25.09.2026):**
> `faltenplan.py` schreibt `mindesttraining_jahre` **nicht mehr** in den Plan,
> und `registerbericht.py` druckt die Zeile „Mindesttraining vor der ersten
> Falte" **nicht mehr** (TB-106, `abeca36`; ebenso `embargo_nach_falten` je
> Falte). Die Konstante `registerdaten.MINDESTTRAINING_JAHRE` steht weiter, ohne
> Leser — tot bis 40.8 (h). Die Tabelle bleibt zeichengleich.""", True, False, "23.5"),
    ("### 33.3 Die Feldliste des Abbilds", "Ebene weder `asof` noch `quelle`.", """\
> ⭐⭐ **Gerechneter Plan und Abbild — die registrierte Abbildung (42.1 D5,
> 42.2 E3, 42.3 F4, Fable 25a–25c, TB-108, 25.09.2026):** Diese Feldliste ist
> die des **Abbilds**. Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt
> mehr — seine Herleitungsfelder (25.3/32.1) — und **schrumpft nicht**; er trägt
> aber keine Grösse, die das Verfahren nicht kennt (Trainingsgrenzen, Embargo,
> Purge, Mindesttraining; entfernt in TB-104 und TB-106). Die Sonde vergleicht
> Plan und Abbild über eine **registrierte Abbildung**; die **Feldliste des
> gerechneten Plans** ist Registertext (**42.2, E3** — die Zuordnung je
> Schlüssel steht aus, 42.6). Mit dem Abbild wird die **Erzeugerkette des
> Trockenlaufs** registriert (**42.3, F4**). Tabelle und Text oben bleiben
> zeichengleich.""", True, False, "33.3"),
    ("### 35.4 Präzisierung zu 30.2 (3)", "Registertext-Blocks — wie die Marke aus 34.3 unter (2).", """\
> ⭐ **„Feldmenge und Werte" heisst: über die registrierte Abbildung (42.2 E3,
> Fable 25b, TB-108, 25.09.2026):** Die Sonde vergleicht den gerechneten Plan
> mit dem Abbild je Feld des Abbilds über den Planschlüssel, aus dem es gebildet
> wird; ein Planschlüssel ausserhalb der registrierten Feldliste des Plans ist
> ein Befund, ein fehlender ebenso. Fables erste Fassung dazu (25a, „trägt keine
> Grösse, die 33.2/33.3 nicht kennt") ist berichtigt (**42.1 D5 → 42.2 E3**).
> Der Text oben bleibt zeichengleich.""", True, False, "35.4"),
    ("### 36.5 ", "≠ 0)", """\
> ⭐ **Wofür die drei Ausgänge gelten, und was seitdem mit 2 endet (42.1 D8/D12,
> 42.2 E5, 42.3 F4, Fable 25a–25c, TB-108, 25.09.2026):** Die drei Ausgänge
> gelten mit „kein Fallback" und der Resolver-Pflicht für den **Laufbereich** —
> die Vereinigung aller registrierten Lauf-Typen, gemessen am Tag-Commit
> (**42.2, E5**). In TB-105 bis TB-107 sind Stellen, die still weiterrechneten
> oder mit 0 endeten, auf 2 umgestellt: unter dem Modus „Keine Daten gefunden"
> (14 Stellen) und eine leere Symbolliste; die stillen Ersatzwerte in
> `faltenplan.py`, `benchmark.py`, `auswertung.py` und `faltenplan_neun.py`;
> `_min_history` bei Fehltreffer (**42.1 D12, 42.3 F4**). Ob
> `auswertung.Abbruch` mit 1 statt 2 endet, ist offen (25d (4), 42.4 G5). Der
> Text oben bleibt zeichengleich.""", True, False, "36.5"),
    ("### 37.3 ", "> Abbild (**39.9**); `sperrliste_abbild_2026-09-22.json` bleibt.", """\
> ⭐⭐ **Die Übergänge seit 39.5 und ihre Abbilder (42.5, TB-108, 25.09.2026):**
> Planmässig bewegt haben sich `messgroessen.py` (TB-103, `EINGEFROREN`),
> `benchmark.py` und `faltenplan.py` (TB-104 und TB-106, Punkte 2, 4, 6),
> `auswertung.py` (TB-106, Punkte 3, 5, 14) und `herkunft.py` (TB-106, Punkte 11
> und 12). Auftrag, Freigabe und volle Hashes stehen in **42.5**. Geschlossen
> durch `sperrliste_abbild_2026-09-25.json` (`cb4eb1b4…`, TB-104) und
> `sperrliste_abbild_2026-09-25b.json` (`40ffe18d…`, TB-106); die älteren
> Abbilder bleiben.""", True, False, "37.3"),
    ("### 37.4 Tatsachennotiz zu Abschnitt 10", "> **Folge für `herkunft.py`, Entscheidung:** **Nicht öffnen.**", """\
> ⭐⭐ **BERICHTIGT durch 42.3 F2 (Fable 25c, TB-108, 25.09.2026):** `herkunft.py`
> ist **einmal planmässig geöffnet** worden (TB-106, `5791b4c`), um
> `datenstand()` den Datenpfad durch `block()` und `anhaengen()` durchzureichen;
> sonst gilt die Entscheidung oben: `EINGEFROREN` bleibt, `register()` bezeugt
> die Abschnitt-0-Menge, die Sonde Abschnitt 10. **Planmässig geöffnet heisst
> nicht offen.** Hash `56a1c2e1…` → `351f24c2…` (42.5). Die Entscheidung oben
> bleibt zeichengleich.""", True, False, "37.4"),
    ("### 39.6 ", "> ist gerückt: `messgroessen.json` ist **TB-101**, nicht TB-96 (40.9 (c)).", """\
> ⭐⭐ **Dieser Nachweis ist nach der Zwei-Teile-Regel 2 (41.2 B4, 41.3 C6/C7,
> Fable 24c/24d, TB-108, 25.09.2026):** Ein Nachweis besteht aus
> Ergebnisvergleich **und** Leseprotokoll; zeigt das Protokoll einen Zugriff
> ausserhalb, ist er 2 (**41.2, B4**). Das eigene Protokoll dieses Laufs zeigt
> zwei Eingaben ausserhalb des Snapshots (39.8). Zudem war TB-92 A1b ein
> **Hilfsordner-Lauf** (`TB30A_BASE_DIR`, Zeile „Umlenkung" oben) — nach 41.3
> (C6) kein Modus-Lauf; der Ergebnisvergleich bleibt Tatsache, als Nachweis 2
> (**41.3, C7**). Die Tabelle ist seitdem im Resolver-Modus bytegleich
> reproduziert (TB-104 bis TB-107, 42.4 G10) — als Nachweis weiter 2, bis
> beide Eingaben registriert sind. Tabelle und Text oben bleiben zeichengleich.""", True, False, "39.6"),
    ("### 39.7 ", "`shared/sperrlistensonde.py`). Offen, Handwerk mit eigener Freigabe.", """\
> ⭐ **Stand (42.3 F2, 42.5, TB-108, 25.09.2026):** „`herkunft.py` ist
> unverändert (`56a1c2e1…`)" beschreibt den Stand von TB-94. Seit TB-106
> (`5791b4c`) ist es planmässig geöffnet (`351f24c2…`); `EINGEFROREN` ist dabei
> zeichengleich geblieben und zeigt weiter auf
> `ergebnisse/benchmark_drawdowns.json`. Die dritte Gruppe führt die Sonde seit
> TB-97 aus dem Abbild (Gruppe „eingefroren" in `cb4eb1b4…` und `40ffe18d…`).
> Der Text oben bleibt zeichengleich.""", True, False, "39.7"),
    ("### 39.8 ", "Nummer 40.5 verweist hierher.", """\
> ⭐⭐ **Zwei Nachträge (41.3 C9, 42.1 D10/D11, Fable 24d/25a, TB-108,
> 25.09.2026):** (1) Der Lesehaken dieses Abschnitts ist **von TB-92** — der
> Satz „erst mit TB-95" des steuernden Chats war falsch, dieses Register hatte
> recht (Messung in **41.3, C9**). (2) Das Öffnen von
> `logs/notifications/manuelle_eingriffe.log` im Modus `a` ist ein Schreibziel
> ausserhalb `--ziel` (Klasse (iii), 42.1 D6); **behoben in TB-105**
> (`d48a195`), der Benchmark-Lauf im Modus öffnet es seither nicht mehr
> (**42.1, D11**). Der Text oben bleibt zeichengleich.""", True, False, "39.8"),
    ("### 40.6 ", "Ableitung), bei **39.6** (Eingabestand: zweiter Anwendungsfall).", """\
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
> Zitate und Text oben bleiben zeichengleich.""", True, False, "40.6"),
    ("### 40.7 ", "**Marke am alten Ort:** bei **12**, unter dem Absatz über den Schalter.", """\
> ⭐⭐ **„alle acht" lies „alle sieben (H1–H7)" (41.1 A2, A4, Fable 24b,
> TB-108, 25.09.2026):** berichtigt durch Fable 24b B2; H0 ist der Grundlauf,
> F4 keine Mutationsprobe. Jede Probe beisst **allein** — ⚠️ H6 trägt bis heute
> nur zusammen mit H5 (TB-97) und ist vor dem Tag eigenständig zu machen oder
> als Paar zu zählen (**41.1, A4**). Der Registertext oben bleibt
> zeichengleich.""", True, False, "40.7"),
]


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert len(zeilen) == 7993, len(zeilen)
    assert not any(z.startswith("## 41.") or z.startswith("## 42.") for z in zeilen)
    kopf = [i for i, z in enumerate(zeilen) if z.startswith("#")]
    k10 = next(i for i, z in enumerate(zeilen) if z.startswith("## 10. Die Sperrliste"))
    k11 = next(i for i, z in enumerate(zeilen) if z.startswith("## 11. "))
    einfuegen = []
    for kopfzeile, anker, text, vor, nach, wo in MARKEN:
        k = [i for i in kopf if zeilen[i].startswith(kopfzeile)]
        assert len(k) == 1, (kopfzeile, k)
        ende = min([i for i in kopf if i > k[0]] + [len(zeilen)])
        a = [i for i in range(k[0], ende) if zeilen[i].startswith(anker)]
        assert len(a) == 1, (kopfzeile, anker, a)
        assert not (k10 <= a[0] < k11), ("Marke in Abschnitt 10", wo)
        block = ([""] if vor else []) + setze(text, wo).split("\n") + ([""] if nach else [])
        einfuegen.append((a[0], block, wo))
    assert len(einfuegen) == 20
    for pos, block, wo in sorted(einfuegen, reverse=True):
        zeilen[pos + 1:pos + 1] = block
    teile = []
    for n, datei in (("41", "abschnitt41_vorlage.md"), ("42", "abschnitt42_vorlage.md")):
        teile.append(setze(open(HIER + datei, encoding="utf-8").read().rstrip("\n"), "Abschnitt " + n))
    neu = "\n".join(zeilen) + "\n\n" + "\n\n".join(teile) + "\n"
    # Wachen fuer die Leser des Registers (G6, test_faltenplan_neun E2, TB-41-Test, Sonde)
    g6 = re.compile(r"^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*")
    assert sum(1 for z in neu.split("\n") if g6.match(z)) == 1
    for s in ("ERSETZT durch Abschnitt 15", "| **730** |", "## 10. Die Sperrliste",
              "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert neu.count(s) == reg.count(s), s
    alt = reg.split("\n")
    # additiv: jede alte Zeile steht in derselben Reihenfolge im neuen Text
    it = iter(neu.split("\n"))
    assert all(any(z == y for y in it) for z in alt[:-1]), "nicht additiv"
    open(REG, "w", encoding="utf-8").write(neu)
    json.dump(zitate, open(HIER + "zitate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Marken:", len(einfuegen), " Zitate:", len(zitate),
          "(Zeilen %d, Teile %d)" % (sum(z["art"] == "zeile" for z in zitate),
                                     sum(z["art"] == "teil" for z in zitate)),
          " Registerzeilen:", len(neu.split("\n")) - 1)


if __name__ == "__main__":
    main()
