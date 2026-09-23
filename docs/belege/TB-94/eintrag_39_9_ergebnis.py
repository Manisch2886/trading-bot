"""TB-94 Block D: traegt das Ergebnis von D1/D2 additiv in 39.9 ein (nach der
eindeutigen Ankerzeile am Ende des Absatzes "Reihenfolge"). Keine bestehende
Zeile wird veraendert; Abschnitt 10 wird nicht beruehrt.
Aufruf aus der Repo-Wurzel."""
REG = "docs/VORREGISTRIERUNG_neuselektion.md"
ANKER = "Commit — additiv, der Listentext von Abschnitt 10 wird dabei nicht berührt."
TEXT = """
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
`sperrliste_abbild_2026-09-23.json`, `2f23f76c…`.**"""

zeilen = open(REG, encoding="utf-8").read().split("\n")
idx = [i for i, z in enumerate(zeilen) if z == ANKER]
assert len(idx) == 1, len(idx)
zeilen[idx[0] + 1:idx[0] + 1] = TEXT.split("\n")
open(REG, "w", encoding="utf-8").write("\n".join(zeilen))
print("ok")
