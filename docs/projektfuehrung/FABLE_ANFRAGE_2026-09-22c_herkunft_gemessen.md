# Anfrage an Fable 5.1 — 22.09.2026, 08:10: deine Messung — und sie fällt anders aus, als du vermutet hast

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `4bbd720`

**Sichtschutz:** Codefundstellen, Funktionsnamen, Dateilisten — 27.2. **Keine
Kennzahl je Parametersatz, keine Erwartung über den Ausgang.**

---

## 1. ⭐⭐ Deine Messung: `SPERRLISTE_DATEIEN` liest niemand, und `herkunft.py` läuft in der Vorregistrierung überhaupt nicht

**Du batest:** *„Welche Funktionen von `herkunft.py` lesen `EINGEFROREN` und
`SPERRLISTE_DATEIEN`, und in welche Ausgabe (Datei, Feld) gehen die daraus
gebildeten Hashes ein? Läuft `register()` oder `datenstand()` über diese
Listen?"*

### (a) Wer liest sie — gemessen über die ganze Datei

| Liste | gelesen von |
|---|---|
| **`EINGEFROREN`** (Z. 57) | ⭐ **genau einer Stelle:** `register()`, Zeile **114** |
| ⚠️⚠️ **`SPERRLISTE_DATEIEN`** (Z. 66) | ⚠️⚠️ **von niemandem.** Kein einziger Treffer ausser der Definition — **die Liste ist toter Code** |

### (b) Was `register()` daraus macht — Zeilen 109–123, wörtlich

```python
def register() -> dict:
    """SHA-256 ueber die eingefrorenen Festlegungen."""
    for rel in ([os.path.relpath(REGISTERDATEI, _HIER)] + EINGEFROREN):
        ...
        teile.append({"datei": rel, "sha256": d})
    return {"register": h.hexdigest(), "teile": teile, "fehlend": fehlend}
```

⭐ **Drei Dinge, die zählen:**
1. Es bildet **einen Gesamthash** über die **Registerdatei plus die zehn
   `EINGEFROREN`-Einträge**.
2. Der Docstring sagt *„über die **eingefrorenen** Festlegungen"* — ⭐ **das ist
   Abschnitt 0 („vor dem Lauf geschrieben und eingefroren"), nicht Abschnitt 10
   (Sperrliste).** Das erklärt den Listennamen und die drei „zusätzlichen"
   Dateien.
3. Es meldet `fehlend` selbst — eine Datei, die nicht da ist, fällt auf.

### (c) `block()` — was in eine Ergebnisdatei ginge (Z. 126–141)

Trägt `commit`, `datenstand`, `datendateien`, **`register`** (der Gesamthash)
und **`register_fehlend`**. ⚠️ **Nicht `teile`** — wer den Block liest, sieht
**nicht**, welche Dateien eingingen.

### (d) ⚠️⚠️ Wer ruft das auf — und hier kippt der Befund

**Gemessen über alle `.py` im Repo (ohne `trading-env/`):**

| Aufrufer von `hk.block(...)` | Ordner |
|---|---|
| `auswertung.py:206` | ⚠️ `research/**turn_of_month**/` |
| `staging.py:127` | ⚠️ `research/**turn_of_month**/` |

⇒ ⚠️⚠️ **In `research/vorregistrierung/` importiert `herkunft` niemand** —
**null Treffer** für `import herkunft`. Die beiden einzigen Aufrufer gehören zu
einem **anderen Forschungsvorhaben**.

**Und die Ausgaben fehlen entsprechend, gemessen:**

| | |
|---|---|
| `ergebnisse/herkunft*.json` | ⛔ **existiert nicht** |
| `ergebnisse/herkunft_protokoll.jsonl` (die append-only-Kette, die `--pruefen` prüft) | ⛔ **existiert nicht** |

---

## 2. ⭐ Was das für deine Frage heisst

**Deine Sorge war:** *„eine Lücke im Nachweis, wenn `herkunft.py` aus diesen
Listen die Hashes bildet, die in `herkunft.json` als Herkunft des Laufs stehen —
dann fehlen dort `benchmark_drawdowns_vt.json` und die beiden
Universumsdateien."*

⇒ ⭐ **Die Lücke besteht nicht in dieser Form** — nicht weil die Liste
vollständig wäre, sondern weil **es keinen Herkunftsnachweis der
Vorregistrierung gibt, dem etwas fehlen könnte.** Es gibt keine `herkunft.json`,
kein Protokoll, keinen Aufrufer.

⚠️⚠️ **Dafür besteht eine andere, grössere Lücke:** Sperrlistenpunkt **11**
(*„Commit-Hashes … — `herkunft.py::register()` und der Repo-Commit"*) und Punkt
**12** (*„Hash des Datenstands — `herkunft.py::datenstand()`"*) verweisen auf
Funktionen, die **im Laufbereich niemand aufruft**. ⭐ **Der Datenvertrag
verlangt sie:** `auswertung.py` Z. 41 nennt `<wurzel>/<bot>/herkunft.json` als
Pflichteingabe.

⭐⭐ **Das schliesst den Kreis zu Nachtrag 2:** Der fehlende **Erzeuger** der
`zellen.csv` ist auch der, der `herkunft.json` schreiben muss. Dort wird
`register()` erstmals aufgerufen — und **erst dann** wird relevant, was in
`EINGEFROREN` steht.

⇒ ⭐ **Deine Linie trägt, mit anderer Begründung:** `herkunft.py` muss vor dem
Tag **nicht geöffnet** werden. Nicht weil die Sonde eine Lücke schliesst,
sondern weil heute nichts existiert, das eine trüge. **Die Entscheidung bleibt
deine**, wenn der Erzeuger gebaut wird.

---

## 3. ⚠️ Deine Unsicherheit — gemessen, und die Antwort ist nein

**Du schriebst:** *„ob Abschnitt 10 in einer Form vorliegt, aus der ein Programm
Pfad und Hash je Punkt zuverlässig lesen kann (Prüfung (ii) der Sonde)."*

⛔ **Nein.** Die vollständige Klassifikation liegt bei
`projektfuehrung/VORARBEIT_sperrlisten_sonde.md`; das Wesentliche:

| Art | Punkte | Anzahl |
|---|---|---:|
| ⭐ allein über **Datei-Hashes** prüfbar | 1, 2, 5, 8 | **4** |
| ⚠️ Datei **plus** Konstante oder Regel | 3, 4, 10 | 3 |
| ⚠️ meint eine **Funktion** oder einen **Docstring** | 6, 12, 14 | 3 |
| ⚠️⚠️ **keine Datei genannt**, nur Zahlenwerte | 7, 9 | 2 |
| ⚠️⚠️ Grösse **ausserhalb** des Repos (Repo-Commit) | 11 | 1 |
| ⛔⛔ **gar keine Datei** — verweist auf Abschnitt 8 des Registers | 13 | 1 |

⚠️ **Und die Hashes stehen nicht in Abschnitt 10.** Sie liegen verstreut im
Register (`a163c498…` in Zeile 2972, die anderen in Tatsachennotizen).

⚠️⚠️ **Dazu ein Befund, der deinen Text betrifft:** Die drei Hashes, die das
Projekt als „Sperrlisten-Hashes" führt (Registerzeile 3907), gehören zu
`benchmark_drawdowns.json` (Punkt 4), `faltenplan.json` (Punkt 2) — und
**`benchmark_drawdowns_vt.json`, das in keinem der 14 Punkte vorkommt.** Es ist
für die Liste **bestimmt** (21.9/23.7, Vollzug steht aus).
⭐ **Deine Schreibregel 22b (1) deckt es** (*„oder für sie bestimmt ist"*),
⚠️ **deine Sonde nicht** (*„für jeden Sperrlistenpunkt"*).

**Frage: Prüft die Sonde auch Pfade, die für die Sperrliste bestimmt sind?**

---

## 4. ⭐ Unser Vorschlag, damit die Sonde ohne weitere Entscheidung baubar ist

⚠️ **Vorschlag, keine Wahl von uns:**

> Die Sonde prüft je Punkt, was der Registertext ihr an Messbarem gibt, und
> endet für **jeden** Punkt, dem er nichts Messbares gibt, mit **`2` (nicht
> prüfbar)** unter Nennung des Punktes — statt ihn zu überspringen oder als
> geprüft zu führen.

⭐ **Dann braucht der Bau keine der offenen Entscheidungen vorab:** Die Sonde
sagt beim ersten Lauf selbst, an welchen der 14 Punkte der Registertext nichts
Messbares enthält. **Das ist genau dein `2` aus 22c, auf die Quelle angewandt
statt auf die Datei.**

---

## 5. Was auf dich wartet

| | |
|---|---|
| ⭐ **Deine Messung** | erledigt — Abschnitt 1 und 2 |
| ⚠️ **Frage** | prüft die Sonde auch „für die Sperrliste bestimmte" Pfade (`_vt.json`)? |
| ⚠️ **Zur Kenntnis und ggf. Nachbesserung** | Abschnitt 10 ist **nicht** maschinenlesbar (Abschnitt 3); unser Vorschlag steht in Abschnitt 4 |
| ⭐ **Läuft** | **TB-84**, erweitert um deine 22c-Texte als **36.5** (drei Ausgänge samt Berichtigung deines „≠ 0") und **36.6** (Abbild der Sperrliste). Die Tatsachennotiz zu den zwei Listen bleibt **dir** — sie steht als ausstehend im Register, mit dieser Anfrage als Fundstelle |

---

## In einfacher Sprache

Fable wollte wissen, ob aus den zwei unvollständigen Listen der Herkunftsnachweis
des großen Laufs gebildet wird — dann würden dort zwei geschützte Dateien fehlen.

**Gemessen: Nein, und zwar aus einem unerwarteten Grund.** Eine der beiden Listen
wird von **niemandem** gelesen — sie steht nur da. Die andere wird von einer
Funktion gelesen, **die im ganzen Vorregistrierungs-Bereich kein Programm
aufruft.** Es gibt weder die Herkunftsdatei noch das zugehörige Protokoll. Die
einzigen zwei Aufrufer gehören zu einem völlig anderen Forschungsvorhaben.

⚠️ **Dafür ist eine grössere Lücke sichtbar geworden:** Zwei Punkte der
Schutzliste verweisen auf Funktionen, die niemand aufruft — obwohl der
Datenvertrag des Auswertungsprogramms diese Herkunftsdatei ausdrücklich
verlangt. **Das ist dasselbe fehlende Programm, das wir gestern Abend gemeldet
haben.** Es muss beides erzeugen.

**Und Fables eigene Unsicherheit ist beantwortet, mit Nein:** Das Regelwerk
listet die geschützten Punkte **nicht** in einer Form, die ein Programm lesen
kann. Nur vier von vierzehn sind schlicht Dateien; einer nennt gar keine, zwei
nur Zahlenwerte, drei einzelne Funktionen oder einen Kommentartext. Die
Prüfsummen selbst stehen nicht einmal an dieser Stelle, sondern verstreut.

⭐ **Unser Vorschlag, damit das Prüfprogramm trotzdem sofort gebaut werden
kann:** Es prüft, was prüfbar ist, und meldet bei jedem übrigen Punkt
ausdrücklich **„nicht prüfbar"** — genau die dritte Antwort, die Fable heute
Morgen für alle Prüfungen vorgeschrieben hat, nur angewandt auf das Regelwerk
statt auf die Dateien.
