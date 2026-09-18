# Registernachtrag TB-48 — Prüfwerkzeug für Abschnitt 17

**Abgeschlossene Arbeit.** Dieser Ordner enthält **kein** Untersuchungsergebnis,
sondern das Werkzeug, mit dem die neunzehn Zahlen aus **Abschnitt 17** der
Vorregistrierung nachgerechnet werden. Er fasst **keinen** Bot-Code an, ändert
keine Kursdatei, keinen Parameter und keinen Registertext. `data/` wird
ausschliesslich gelesen.

Registereintrag: `docs/VORREGISTRIERUNG_neuselektion.md`, **Abschnitt 17**
Entstanden in: **TB-48** (unversioniert) · ins Repo gelegt in **TB-49**
Ergebnis zum Nachlesen: `docs/ERGEBNIS_TB-48_registernachtrag.md`, Abschnitt 4
und `docs/ERGEBNIS_TB-49_ausnahme.md`, Teil 3

---

## 1. Warum es das gibt

`research/registernachtrag_tb41/pruefe_register.py` ist das **TB-41**-Werkzeug.
Im ganzen Quelltext kommt Abschnitt 17 nicht vor — sein „KEIN BEFUND" ist ein
Nachweis über **Abschnitt 15 und 16** und über die null entfernten Zeilen, nicht
über die Richtigkeit von Abschnitt 17.

⚠️ *Ein Prüfer, der die neuen Texte nicht sieht, meldet grün über den alten
Stand.* Genau dafür gibt es dieses zweite Werkzeug. **Ob der TB-41-Prüfer um
Abschnitt 17 erweitert wird, ist damit weiterhin eine eigene Entscheidung** —
diese Arbeit legt ein zweites Werkzeug daneben, sie baut das erste nicht um.

## 2. ⚠️ Herkunft dieser Dateien — gehört in die Beurteilung

Das Werkzeug ist in **TB-48** entstanden und blieb **unversioniert**, weil der
damalige Auftrag Änderungen unter `research/` untersagte. Es lag in der
TB-48-ZIP-Datei.

⚠️ **In den Unterlagen der TB-49-Sitzung lag es nicht bei** — nur der
Auftragstext. Es ist deshalb aus der Belegtabelle in
`docs/ERGEBNIS_TB-48_registernachtrag.md`, Abschnitt 4, **neu geschrieben**:
dieselben neunzehn Zahlen, dieselben Quellen, dieselbe Erwartung.

**Ein neu geschriebenes Werkzeug ist kein wiederhergestelltes.** Dass es
dieselben neunzehn Ergebnisse liefert wie TB-48 — 18 grün, eine Abweichung,
Rückgabewert 1 — ist **gemessen** und in `docs/ERGEBNIS_TB-49_ausnahme.md`
belegt, nicht behauptet. Wer die TB-48-ZIP-Datei noch hat, kann beide Fassungen
nebeneinanderlegen; nötig ist das für das Ergebnis nicht.

## 3. Die neunzehn Zahlen

```bash
python3 research/registernachtrag_tb48/pruefe_abschnitt17.py
python3 research/registernachtrag_tb48/pruefe_abschnitt17.py --nur 15
python3 research/registernachtrag_tb48/pruefe_abschnitt17.py --falten-je-bot
python3 research/registernachtrag_tb48/test_abschnitt17.py
```

| # | Zahl | Quelle |
|---:|---|---|
| 1 | Nicht-Kurs-Eingaben im Snapshot: genau zwei | `research/snapshotgrenze/ergebnisse/eingaben.json` |
| 2 | `datenstand_hash` `d9449faf…` | `research/vorregistrierung/herkunft.py::datenstand` |
| 3 | 223 Kursdateien | dieselbe Funktion |
| 4 | `snapshot_hash` `4fee547d…` | `shared/snapshot.py::snapshot_hash` |
| 5 | Teilkerzen-Befunde 36 von 223 | `shared/zeitabdeckung.py::pruefe_ordner` |
| 6 | Arten: `{'rand_erste': 36}` | dieselbe Funktion |
| 7 | letzte Kerze nicht betroffen | dieselbe Funktion |
| 8–10 | erste Kerze 2017–2020 / ab 2023 / 2021–2022 → 20 / 16 / 0 | selbst nachgezählt aus den Befunden |
| 11 | die 11 Symbole aus T34.9 | `docs/projektfuehrung/BACKLOG.md` |
| 12–14 | `kein_zeuge` 175 / Aktien 150 / Krypto-1h 25 | `shared/zeitabdeckung.py::pruefe_ordner` |
| 15 | ⚠️ früheste Selektionsfalte | `research/faltenplan_neun/daten/faltenplan.json` |
| 16 | kurze erste Kerze in einer **geladenen** Falte: 0 | Faltenplan × Befunde, 9 Bots × alle Falten |
| 17–19 | 18/19, 19/20, `1/(1−0,95)` | nachgerechnet |

⚠️ **Zwei Zahlen aus Abschnitt 17 fasst das Werkzeug gar nicht erst an**, weil
sie in der Cloud strukturell nicht nachrechenbar sind: die Fassung von
`pandas_market_calendars` (17.5 sagt ausdrücklich „auf dem Betriebsrechner") und
die Drift-Messung aus 17.8 (braucht einen echten yfinance-Abruf; gesperrt und
nach T35.4 bis TB-30b ohnehin untersagt). Beide stehen im Mac-Testauftrag
beziehungsweise sind selbst nicht reproduzierbar — das ist der Inhalt des
Befunds, nicht seine Umgehung.

## 4. ⚠️ Prüfung 15 ist rot — und das ist richtig so

Der beschlossene Wortlaut in 17.3 sagt: *„Die erste Selektionsfalte beginnt
**2022**."* Der Faltenplan sagt **2019**, und zwar bei **allen neun** Bots.

Das Werkzeug **meldet die Abweichung weiter** und endet mit **Rückgabewert 1**.
Ein Prüfer, der sie wegdefiniert, wäre die stillschweigende Korrektur, die
TB-48 ausdrücklich nicht vornehmen sollte. Der Wortlaut bleibt als der
registrierte stehen; massgeblich ist die Befundnotiz darunter — dieselbe
Behandlung wie bei der „vierten falschen Zahl" in 16.7.

⚠️ **Die Jahreszahl wird aus dem Registertext gelesen, nicht im Werkzeug
hinterlegt.** Sonst prüfte es seine eigene Abschrift und meldete nach einer
Berichtigung des Wortlauts weiter die alte Abweichung.

**TB-49, Teil 4 hat den Befund aufgeklärt:** `--falten-je-bot` stellt Markt und
erstes Faltenjahr je Bot nebeneinander. Die Vermutung *„2022 ist die früheste
**Krypto**-Falte, 2019 die über alle neun"* trägt **nicht** — beide Mengen
liefern 2019. Die 2022 stammt aus dem **überholten** Faltenplan
`research/krypto_historie/daten/faltenplan_nach_tb34.json` (`mindesttraining: 4`,
nur Krypto). Einzelheiten in `docs/ERGEBNIS_TB-49_ausnahme.md`, Teil 4.

## 5. Die drei Rückgabewerte

| | |
|---|---|
| **0** | keine Abweichung |
| **1** | mindestens eine Abweichung — **heute: genau eine** |
| **2** | ⚠️ mindestens eine Prüfung war **nicht ausführbar** |

Die **2** gibt es aus demselben Grund wie in `shared/snapshot.py`: in TB-45
haben zwei Wachen „bestanden" gemeldet, ohne etwas gemessen zu haben. *Wer nicht
messen konnte, sagt es mit einem eigenen Wert.*
