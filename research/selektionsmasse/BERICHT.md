# Die zwei Selektionsmasse — TB-52, Teil 2

**Gemessen 18.09.2026.** Zwei Masse über die **90 Selektionsmodule**, gebaut als
**Sperrklinke**, nicht als Wache.

> ⚠️ **Beide Masse ändern nichts.** Sie lesen Quelltext und zählen. Kein Modul
> wird verdrahtet, keine Zeile ersetzt — das ist TB-53.

| Datei | |
|---|---|
| `masse.py` | die Messwerkzeuge (Syntaxbaum). Trägt keine Zahl |
| `test_wanduhr.py` | **Mass 1**, Ausgangszahl **6** |
| `test_eigener_pfadbau.py` | **Mass 2**, Ausgangszahl **29** |
| `ergebnisse/mass_wanduhr.json` · `ergebnisse/mass_pfadbau.json` | die Trefferlisten |

**Beide laufen ohne Argument** (Prüfprinzip **A3**) und heissen `test_*.py`, also
laufen sie im Basislauf mit.

---

## Die Bauform: Sperrklinke

| | |
|---|---|
| **heute** | Ausgangszahl = gemessener Stand ⇒ **grün** |
| **TB-53** | senkt die Zahl; die Ausgangszahl wird **im selben Commit** mitgesenkt |
| ⚠️ **ein Verstoss kommt dazu** | **rot**, sofort |
| ⚠️ **jemand erhöht die Ausgangszahl** | ⭐ steht als **eigene Zeile im Diff** und braucht eine Begründung im Commit |
| **Erhebung fehlt** | **NICHT PRÜFBAR** (rc 2), nicht grün (**A2**) |

**Nachgemessen, nicht behauptet** — die vier Ausgänge der Sperrklinke:

| Ausgangszahl gegen Stand 29 | Rückgabewert | |
|---|---|---|
| 29 (gleich) | **0** | grün |
| 28 (zu klein) | **1** | ⚠️ rot — *sie beisst* |
| 30 (zu gross) | **0** | grün, mit dem Hinweis, sie zu senken |
| Erhebung fehlt | **2** | NICHT PRÜFBAR |

**Die Ausgabe nennt immer Ausgangszahl, heutigen Stand und die Trefferliste mit
Datei und Zeile.** ⚠️ *Eine Zahl ohne Liste ist kein Mass, sondern ein Gefühl.*

---

## Mass 1 — keine Wanduhr im Selektionspfad

**Ausgangszahl 6.** Gesucht am Syntaxbaum (**B5**), nicht per Textsuche.

**Alle sechs Treffer, von Hand nachgesehen:**

| Datei | Zeile | Was | Wozu der Wert dient |
|---|---|---|---|
| `strategies/elliott_wave/quarterly_review.py` | 119 | `datetime.utcnow()` | **Berichtskopfzeile** — `lines.append(…)`, das `build_report` zu Text fügt |
| `strategies/elliott_wave/quarterly_review.py` | 205 | `datetime.utcnow()` | **Protokollzeile** (`print`) |
| `strategies/elliott_wave_stocks/quarterly_review.py` | 124 | `datetime.utcnow()` | **Berichtskopfzeile** |
| `strategies/elliott_wave_stocks/quarterly_review.py` | 210 | `datetime.utcnow()` | **Protokollzeile** (`print`) |
| `strategies/t3_supertrend/quarterly_review.py` | 146 | `datetime.utcnow()` | **Berichtskopfzeile** |
| `strategies/t3_supertrend/quarterly_review.py` | 232 | `datetime.utcnow()` | **Protokollzeile** (`print`) |

> ⭐ **Null Treffer im Datenschnitt.** Keine der sechs Wanduhren kappt die
> Historie, bestimmt ein „letztes vollständiges Jahr" oder macht eine
> Frischeprüfung. **Derselbe Snapshot ergibt an zwei Tagen dasselbe Ergebnis** —
> soweit Mass 1 reicht.

⚠️ **Der Test stuft drei davon als `zu prüfen` ein, nicht als `nur
Protokollzeile`.** Das ist Absicht: die automatische Einstufung sieht
`lines.append(…)` und weiss nicht, wohin `lines` geht. *Eine Einstufung, die im
Zweifel entwarnt, macht aus einem Befund ein Schweigen.* **Der Test unterscheidet
das nicht — dieser Bericht tut es**, durch Nachsehen an der Quelle: `build_report`
fügt `lines` mit `"\n".join(lines)` zu einem Textbericht.

**Gesucht wurde über die Auftragsliste hinaus.** Zusätzlich aufgenommen, weil
dieselbe Wirkung:

`datetime.today` · `Timestamp.utcnow` · `date.fromtimestamp` ·
`datetime.fromtimestamp` · **`os.path.getmtime` / `getctime`** (Frischeprüfung
über den Dateizeitstempel) · `time.time_ns` · `time.monotonic`

Dazu die Bauform mit verräterischem **Argument** statt Namen:
`np.datetime64("now")`, `pd.Timestamp("today")`.

⚠️ **Auch die blosse Referenz zählt** — `f = datetime.utcnow` und später `f()`
ist dieselbe Wanduhr, nur eine Zeile weiter.

---

## Mass 2 — kein eigener Datenpfad

**Ausgangszahl 29** Fundstellen in **29** Modulen.

### ⚠️ Der Befund, der grösser ist als die Zahl

> ⭐ **Keines der 90 Selektionsmodule importiert `shared/paths.py`. Nicht eines.**

**71 von 90** beziehen ihre Pfade aus `shared/strategy_paths.py` — und das
leitet `DATA_DIR` **selbst** ab, ohne `paths.py` je zu berühren:

```python
"DATA_DIR": os.path.join(base_dir, "data")     # strategy_paths.py:49
```

| Wie die 90 an Pfade kommen | Anzahl |
|---|---|
| über `strategy_paths`, **ohne** `DATA_DIR`/`CONFIG_DIR` zu ziehen | 42 |
| über `strategy_paths`, **mit** Datenpfad ⇒ **die 29 Treffer** | 29 |
| weder noch (keine Pfade) | 18 |
| nennt `DATA_DIR`, ohne eine der beiden Quellen | 1 |
| ⭐ **über `shared/paths.py`** | **0** |

⚠️⚠️ **Der Selektionsmodus aus TB-52 erreicht damit heute kein einziges der 90
Module.** Er wäre gesetzt, und alle 90 läsen weiter aus dem Live-Bestand —
**still**. Das ist Fables Einwand eine Ebene höher: *die Wache steht nicht dort,
wo gefragt wird.*

> ⭐ **Das entwertet Schicht (1) nicht — es bestimmt, was TB-53 zu tun hat.**
> Der Modus ist die Stelle, an der ein Pfad zentral umgebogen werden *kann*;
> dass heute niemand dort fragt, ist genau der Umbau, den Mass 2 misst.
> ⚠️ **Ob TB-53 die 90 auf `paths.py` umzieht oder `strategy_paths.py` an den
> Resolver hängt, ist dort zu entscheiden** — hier wird es nur sichtbar gemacht.

### Die 29 Treffer

Alle von **einer** Art: `DATA_DIR = _P["DATA_DIR"]` bzw. `_P["CONFIG_DIR"]`,
je einmal im Modulkopf. **Null Modul setzt einen Datenpfad im eigenen Quelltext
zusammen** — kein `os.path.join`, kein f-String, kein `Path(…)`.

### ⚠️ Zwei Zahlen 29, zwei Fragen (Prüfprinzip C7)

**Sie sind NICHT dieselben 29, und die Mengen sind disjunkt:**

| | `research/datenordner_schnitt` | **hier** |
|---|---|---|
| **Frage** | welche Module bauen einen Pfad **selbst**? | welche **Selektionsmodule** beziehen einen Datenpfad **ausserhalb `paths.py`**? |
| **Anzahl** | 29 | 29 |
| **Wer** | 16 Untersuchung · 7 Prüfwerkzeug · 6 Betrieb | **90/90 Selektion** |
| **Schnittmenge mit den 90** | ⭐ **0** | — |

⚠️ **Dass beide Male 29 herauskommt, ist Zufall.** Der Auftrag nennt die 29 aus
der Erhebung als Ausgangszahl für dieses Mass — **nachgerechnet trifft das nicht
zu**: von jenen 29 ist **kein einziges** ein Selektionsmodul. Siehe
`docs/ERGEBNIS_TB-52_resolver.md`, Abschnitt „Wo unsere Zahlen abweichen".

---

## Beissen die Masse? (Prüfprinzip B1)

**Beide laufen vor jeder Messung gegen zwei erfundene Module** — eines mit
bekannten Verstössen, eines ohne. Finden sie dort nicht genau das Erwartete, ist
der Ausgang **NICHT PRÜFBAR** (rc 2), **nicht grün**.

| | eingebaute Verstösse | gefunden | sauberes Modul |
|---|---|---|---|
| **Mass 1** | 7 (Datenschnitt, letztes Jahr, Frischeprüfung, `time.time`, `Timestamp.now`, blosse Referenz, `Timestamp("today")`) | **7** — davon 2 als Datenschnitt eingestuft | **0 Treffer** |
| **Mass 2** | 5 (`os.path.join`, f-String, `Path(…)`, %-Formatierung, blanke Konstante) | **5**, alle 5 Bauarten | **0 Treffer** — weder der Pfad über den Resolver noch die Ergebnisdatei zählen |

---

## ⚠️ Was beim Bauen schiefging — benannt statt still berichtigt

**Mass 2 meldete im ersten Entwurf 127 statt 29 Treffer.** Zwei Fehler, beide im
Mass, keiner im Quelltext der 90:

1. **`RESULTS_DIR`, `LOGS_DIR`, `DB_FILE` galten nicht als zentral bezogen.**
   Sie kommen aus `strategy_paths.get_strategy_paths()`. Dadurch zählte jedes
   gewöhnliche `os.path.join(RESULTS_DIR, "equity_curve.csv")` als eigener
   Datenpfad — **eine Ergebnisdatei ist kein Datenpfad.**
2. **Innere Knoten wurden doppelt gezählt.** Bei
   `os.path.join(DATA_DIR, f"{symbol}_1d.csv")` fiel der äussere Ausdruck
   richtigerweise durch (er geht über den Resolver), der f-String **darin** aber
   wurde eigens gezählt — er sieht für sich genommen keinen Resolver. Jetzt
   zählt nur der **äusserste** Ausdruck.

> ⚠️ **Hätte niemand hingesehen, wäre 127 die festgeschriebene Ausgangszahl für
> TB-53 geworden** — und TB-53 hätte 98 Treffer „gesenkt", die nie ein Problem
> waren.
