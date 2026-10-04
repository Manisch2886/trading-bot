# TB-132 — Messung vor dem Eintrag zu R66, R71, R72 (Anfrage 02.10.c) — Messhelfer, 02.10.2026

Stand des Repos: `git --no-optional-locks rev-parse HEAD` = `077945307bc3f0c3eff9a9e05ba61ec799f4cb5c` (wie v2).
Gelesen wurde nur Code, Register und `docs/`; nichts unter `ergebnisse/` (auch nicht `research/snapshotgrenze/ergebnisse/eingaben.json`), keine Trade-Listen, kein `BACKLOG*.md`, keine echten Kurse.
Im Repo wurde nichts angelegt oder geändert: Proben unter `/tmp/tb132_p3/` der Geräte-Shell, `PYTHONDONTWRITEBYTECODE=1`; nach den Läufen `find … -newer <Marke>`: 0 neue Dateien (zweiter Lauf: ganzes Repo ohne `.git`, `trading-env/` eingeschlossen).

Umgebung der Proben: Geräte-Shell pandas 2.3.3, numpy 2.2.6, Python 3.10.12 (Lock: pandas 2.3.3, numpy 2.0.2, Python 3.9.6, macOS). Das ist **nicht** die Lock-Umgebung.

Hashes (SHA-256) der gelesenen Dateien:

| Datei | SHA-256 |
|---|---|
| `research/vorregistrierung/kennzahlen.py` | `d130e15cf2c9b9c1359610aeac715c39c43823314273d8c9f8c78d555e2ea137` (Repo = Container-Kopie = v2) |
| `notifications/boersenkalender.py` | `894249dfcacdba52c91212388de521760372384b53067dcdcf2bac265c98e0a6` |
| `research/mtm_drawdown/mtm_kern.py` | `35c37049142db2c32a7204a3ca5e44cbe518b7322ea9fd3dc2cbd2738dc71d74` |
| `research/exposure_messung/exposure_kern.py` | `7e32a2ee28297639e419d1627b592f657070685752e5d8cd8733f89dbb3a9b29` |
| `research/exposure_messung/auswertung.py` | `ceef1dac9e4b6692d7b7c57f872dcf364b7bdab3214ad0a1e4fb8edbc2df6435` |
| `research/exposure_messung/bot_lauf.py` | `203d96203aa8e86a32610bbae40fcca911554f56a98b971f5cc8c475c766f50a` |
| Probe `p3_probe.py` | `b15bb6903f09a0ffcfd04ae6d5c6ccffbc6797fa8cebc066747936814c460296` (Geräte-Shell `/tmp/tb132_p3/` = Container `/home/claude/tb132/p3_probe.py`) |

Abgrenzung (wie v2): Sperrliste = `registerdaten.py`, `faltenplan.py`, `auswertung.py`, `benchmark.py`, `herkunft.py` (alle `research/vorregistrierung/`), `shared/zuteilung.py`; Gruppe „eingefroren“ zusätzlich `kennzahlen.py`, `messgroessen.py`, `pruefe_grenzsaetze.py`. Laufbereich = `shared/paths.py:239–253` (`ARBEITSBAUM_PFADE`: Ordner `shared`, `strategies`, Lock, 12 Einzeldateien) bzw. die gemessene Hülle `docs/belege/TB-112/a2_laufbereich.txt` (84 Pfadzeilen, davon 3 Messumschläge).

---

## P1 (R66 (b)) — welchen Kalender des Pakets benutzt der Code des Laufs?

**Urteil: nicht entscheidbar aus dem Code des Laufs — er benutzt heute keinen Kalender.** Die einzige Stelle im Repo, die einen Kalender des Pakets baut, nennt `"NYSE"`; sie liegt ausserhalb von Laufbereich und Sperrliste. Das Feld `kalender` aus TB-47 nennt keinen Kalendernamen.

### 1.1 Einzige Aufrufstelle im Repo

`grep -E 'import pandas_market_calendars|import exchange_calendars|get_calendar\('` über alle `*.py` (ohne `ergebnisse/`, `trading-env/`, `.git/`): genau zwei Zeilen, beide in einer Datei.

- `notifications/boersenkalender.py:70` `KALENDER_NAME = "NYSE"` (Kommentar Z. 65–69: „Der NASDAQ-Kalender waere fuer diesen Zweck identisch“)
- `:81` `import pandas_market_calendars as mcal`
- `:106–110` `def _kalender(): … _KALENDER = mcal.get_calendar(KALENDER_NAME)`
- `:157`, `:231` `"kalender": KALENDER_NAME` — Schlüssel im Zustands-Dict von `status()` (Betrieb: „ist die Börse offen“), keine Snapshot- oder Herkunftsdatei.

„XNYS“ kommt in keiner `*.py` des Repos vor.

### 1.2 Die genannten Dateien: Laufbereich, Sperrliste?

| Datei | was dort steht | `ARBEITSBAUM_PFADE` | gemessene Hülle (a2, 84 Zeilen) | Sperrliste |
|---|---|---|---|---|
| `notifications/boersenkalender.py` | der Aufruf, `"NYSE"` | nein (aus `notifications/` nur `manual_close.py`) | nein | nein |
| `shared/entscheidungskerze.py` | `:384` `import boersenkalender` (verzögert, in `_boersenkalender()`), `:344–371` `letzter_handelstag` | ja, über den Ordner `shared` | **nein** | nein |
| `shared/snapshot.py` | nur Docstring `:130–134` („Der Handelskalender ist KEINE Eingabe … `mcal.get_calendar` … Umgebung und gehoert ins Lock“) | ja, über den Ordner | nein | nein |
| `research/snapshotgrenze/erhebung_eingaben.py` | TB-47-Erhebung, `:560`, `:564–610` | nein | nein | nein |
| `research/registernachtrag_tb48/pruefe_abschnitt17.py` | nur Docstring `:47` (Fassung 4.6.1 „nicht nachrechenbar“) | nein | nein | nein |

`shared/entscheidungskerze.py` wird nur von den neun `strategies/*/forward_test.py`, von Tests und Forschungsskripten importiert (Live-Pfad), nicht von einem Modul der gemessenen Hülle.

Gegenprobe über die 84 Pfade der Hülle (`grep -E 'pandas_market_calendars|exchange_calendars|\bmcal\b|get_calendar|boersenkalender|entscheidungskerze|KALENDER_NAME|\bkalender\b'`): vier Treffer, alle Kommentar oder Docstring (`shared/abrufschutz.py:59`, `:218`; `shared/ladeprotokoll.py:120`; `strategies/elliott_wave_stocks/fetch_stock_data.py:27`). `shared/abrufschutz.py:57` sagt ausdrücklich „warum hier **kein** Boersenkalender“.
Sperrliste und Gruppe „eingefroren“ (neun Dateien): 0 Treffer für Paket, `mcal`, `get_calendar`, `boersenkalender`; „Kalender“ nur als „Kalenderjahr“/„Kalendertag“.

Deckt sich mit `docs/ERGEBNIS_TB-47_snapshotgrenze.md:124–129`: „der Kalender liegt **nicht in der Hülle der 90**. Der Selektionslauf erreicht ihn überhaupt nicht; er hängt am Live-Pfad (`shared/entscheidungskerze.py` → `notifications/boersenkalender.py`)“.

Einen Zellen-Erzeuger gibt es im Repo nicht (`git ls-files | grep -Ei 'zellen|erzeug'`: nur Dokumente und Belege). Der Code, der die Tagesreihe nach R66 (a) auf Kalendertagen führen soll, ist also noch nicht geschrieben. Die vorhandenen Stellen, die Aktien-Tage bilden, nehmen sie aus den Kursdateien, nicht aus dem Paket: `benchmark.py:204–205` (Vereinigung der Kursindizes, v2 M4), `mtm_kern.py:135–148` (`tagesraster`: „Vereinigung der Kurstage aller Symbole“), `research/turn_of_month/handelstage.py:17` („Ein zweiter Kalender waere eine zweite Quelle“), `beispieldaten.py` (`freq "B"`, v2).

### 1.3 Feld `kalender` (TB-47)

- Register 17.5, Z. 2826–2829: „Der Handelskalender kommt **nicht aus einer Datei**, sondern aus dem Paket **`pandas_market_calendars`** (gemessen TB-47: Fassung **4.6.1** auf dem Betriebsrechner). Er ist damit **Umgebung, nicht Eingabe**, und liegt im Lock.“ Z. 2844–2847: „Die Einordnung ist gemessen worden (TB-47, `eingaben.json`, Feld `kalender`) und nicht geraten.“ Abschnitt 17 (Z. 2600–3200) nennt weder „NYSE“ noch „XNYS“.
- Was das Feld schreibt — `research/snapshotgrenze/erhebung_eingaben.py:606–610`:
  ```python
  return {
      "in_selektionshuelle": sorted(in_huelle, key=lambda e: e["modul"]),
      "im_repo": sorted(im_repo, key=lambda e: (e["modul"], e["zeile"])),
      "paket_vorhanden": _paketfassung("pandas_market_calendars"),
  }
  ```
  Also: Importstellen in der Hülle, Importstellen im Repo (Modul, Import, Zeile), Paketfassung. **Kein Kalendername.** Das Feld beantwortet „Datei oder Paket“ (Docstring `:565–570`), nicht „welcher Kalender“.
- Ein Feld `kalender` in einer Snapshot- oder Herkunftsdatei gibt es nicht: `shared/snapshot.py` und `research/vorregistrierung/herkunft.py` haben 0 Treffer für `"kalender"` als Schlüssel (`snapshot.py` nur den Docstring `:130–134`).
- Die Datei `eingaben.json` selbst liegt unter `research/snapshotgrenze/ergebnisse/` und wurde wegen der Leseregel nicht geöffnet; ihr Inhalt ist hier aus dem Erzeuger und aus `docs/ERGEBNIS_TB-47_snapshotgrenze.md:59`, `:89`, `:102–129` erschlossen.

### 1.4 Lock

`requirements.lock:51` `pandas-market-calendars==4.6.1`; `:37` `exchange-calendars==4.5.6`. `requirements.txt:65` `pandas_market_calendars>=4.1,<5`.

### 1.5 Zusatzmessung: Der Name ist nicht gleichgültig (Ersatzmessung, ausserhalb der Regelbedingung)

In der Geräte-Shell ist das Paket nicht installiert (`ModuleNotFoundError`). Wie in v3 (e) wurde `trading-env/lib/python3.9/site-packages` **hinten** an `sys.path` gehängt (pandas 2.3.3 des Systems; Paket 4.6.1, `exchange_calendars` 4.5.6 — die Lock-Fassungen; Python 3.10 lädt ein für 3.9 installiertes Paket). Nur Kalendertage, keine Kurse.

| Name | Klasse | `valid_days` 2000-01-01 … 2026-09-30 |
|---|---|---|
| `"NYSE"` | `pandas_market_calendars.calendars.nyse.NYSEExchangeCalendar` | 6 726 |
| `"NASDAQ"` | dieselbe Klasse (`name: NYSE`) | 6 726, 0 Unterschiede |
| `"XNYS"` | `pandas_market_calendars.class_registry.XNYS` (Spiegel von `exchange_calendars`) | 6 727 |

`"XNYS"` führt gegenüber `"NYSE"` **einen Tag mehr: 2025-01-09** (in beiden Fenstern, 2010… und 2000…); kein Tag nur in `"NYSE"`. Das Paket kennt 193 Kalendernamen. v3 (e) hat `"NYSE"` gegen die Kurstage gemessen (0 Unterschiede in beiden Richtungen); mit `"XNYS"` wäre der 09.01.2025 ein Handelstag ohne Kurs, also ein Befund nach R66 (b).

Folge für den Wortlaut (Tatsache, kein Vorschlag zur Entscheidung): „die Tage des Handelskalenders nach 17.5 (Umgebung, im Lock)“ legt den Kalender nicht fest, solange kein Name steht; das Lock hält die Paketfassung, nicht den Namen.

---

## P2 (R66 (c)) — trifft der Aufruf mit 252 bzw. 365 die Formel aus 15.3?

**Urteil: trifft — mit einer Unbestimmtheit im Register (Nenner der Standardabweichung) und einer Tatsache zum Aufruf (er existiert noch nicht).**

### 2.1 Wortlaute

`research/vorregistrierung/kennzahlen.py:95–108`:
```python
def sharpe(renditen, perioden_je_jahr: int) -> float:
    """Annualisierter Sharpe ohne Zinsabzug.

    Ohne Zinsabzug, weil eine Zinsannahme eine weitere Wahl waere - und die
    Vorregistrierung will genau die nicht. Eine Reihe ohne Streuung hat
    keinen Sharpe; sie liefert 0,0, nicht unendlich.
    """
    r = np.asarray(renditen, dtype=float)
    if r.size < 2:
        return 0.0
    s = float(np.std(r, ddof=1))
    if s == 0.0 or not np.isfinite(s):
        return 0.0
    return float(np.mean(r)) / s * math.sqrt(perioden_je_jahr)
```

Register 15.3, Z. 1449–1450 (ganze Formelzeile): „*Formel für den Falten-Sharpe: Mittel / Standardabweichung der täglichen Netto-Renditen der Falte × √252 (Krypto: √365 auf Kalendertagen).*“
Register 15.3 (c), Z. 1439–1444: „Der Falten-Sharpe wird für jeden Parametersatz in jeder Falte aus den täglichen Netto-Renditen des Kapitalpfads gerechnet, **unabhängig von der Anzahl Trades**. Ist die Standardabweichung 0 (kein Trade in der Falte), ist der Falten-Sharpe 0. **Es gibt keine Mindestzahl Trades je Falte.**“

### 2.2 Vergleich

| Bestandteil | Register | Code | Urteil |
|---|---|---|---|
| Mittel | „Mittel“ | `np.mean(r)` (arithmetisch) | passt |
| Standardabweichung | „Standardabweichung“, ohne Angabe des Nenners | `np.std(r, ddof=1)` (Stichprobe, n − 1) | Register sagt es nicht; Code legt ddof = 1 fest. Im ganzen Register 0 Treffer für `ddof`, „Stichprobenstandard…“. Unterschied zu ddof = 0 bei 250 Tagen: Faktor √(249/250), rund 0,2 % |
| Annualisierung | × √252, Krypto × √365 | `* math.sqrt(perioden_je_jahr)` — Zahl kommt vom Aufrufer | passt, wenn 252 bzw. 365 übergeben wird |
| Zinsabzug | keiner genannt | keiner (`registerdaten.py:110` `RISIKOFREIER_SATZ = 0.0`, in `sharpe` nicht benutzt) | passt |
| Standardabweichung 0 | Sharpe 0 | `s == 0.0` → `0.0` | passt |
| zusätzlich im Code | — | weniger als zwei Werte → 0,0; `s` nicht endlich → 0,0 | im Register nicht genannt |

Probe an der hashgleichen Kopie (Container, pandas 3.0.5/numpy 2.5.3; synthetische Zufallsreihe, 250 Werte): `sharpe(r, 252)` und `sharpe(r, 365)` sind bitgleich mit `r.mean()/r.std(ddof=1)*sqrt(pj)`, nicht gleich mit ddof = 0. Nur Nullen → 0,0. Ein Wert → 0,0. Leer → 0,0.

Zwei Randfälle (Tatsachen):
- **NaN in der Reihe → 0,0, ohne Meldung** (`not np.isfinite(s)`). Die Wache nach R67 („jeder Zahlenwert endlich“) fängt das vor dem Aufruf ab, wenn sie vor der Sharpe-Bildung prüft; R67 sagt „nachdem er sie geschrieben hat“.
- Eine konstante Reihe ungleich 0 hat rechnerisch nicht genau Streuung 0 (252 × 0,001: `np.std` = 2,2e-19) und liefert dann einen Sharpe der Grössenordnung 1e16 statt 0. Für eine Falte ohne Trade (lauter Nullen) ist die Streuung exakt 0; der Fall betrifft nur eine konstante Rendite ungleich 0 und ist für einen Kapitalpfad praktisch nicht zu erwarten.

### 2.3 Registrierte Konstanten für 252 und 365

- `research/vorregistrierung/registerdaten.py:109` `HANDELSTAGE_JE_JAHR = 252` (Sperrliste).
- **365 ist keine benannte Konstante in `registerdaten.py`.** Die Zahl steht als Literal in `auswertung.py:264–265`:
  ```python
  def perioden_je_jahr(bot: str) -> int:
      return (rd.HANDELSTAGE_JE_JAHR if rd.BOTS[bot]["markt"] == "aktien" else 365)
  ```
  Aufrufer heute: `auswertung.py:526` (Beta-Bereinigung), `beispieldaten.py:243`.
- `messgroessen.py:68–72` `BALKEN_JE_JAHR` führt `("krypto","1d"): 365`, `("krypto","4h"): 365 * 6`, `("krypto","1h"): 365 * 24`, `("aktien","1d"): 252`. Das sind Balken je Jahr im Zeitrahmen des Bots, **nicht** Tage der Tagesreihe: für `elliott_wave` (1h) und `t3_supertrend` (4h; `registerdaten.py:131–132`) wäre dieser Wert als `perioden_je_jahr` falsch; die Tagesreihe ist täglich, also 365.
- `registerdaten.py:117` `"elliott_wave": 252` ist eine Zahl historischer Kombinationen (`N_HISTORISCH_JE_BOT`), keine Periodenzahl.

### 2.4 Zum Aufruf

Die Funktion hat heute keinen Aufrufer (v2 M1 Nr. 2; hier nachgezählt: `grep -E 'kz\.sharpe\(|kennzahlen\.sharpe\(|[^_a-zA-Z.]sharpe\('` über `research/vorregistrierung`, `shared`, `strategies`, `docs/belege` trifft nur die Definition; die übrigen Treffer sind `sharpe_fn=` in Beispieldaten und Tests). Die Voraussetzung prüft also die Funktion und den naheliegenden Zahlengeber `auswertung.perioden_je_jahr`, nicht einen vorhandenen Aufruf. Der Schnitt der Reihe auf die Falte (halboffen, alle Tage der Tagesreihe) liegt beim künftigen Aufrufer; `sharpe` filtert nichts.

---

## P3 (R72, zweite Voraussetzung) — bewertet ein vorhandener Kern den Lückentag anders als (c)?

**Urteil: trifft** für den einzigen vorhandenen Kern der täglichen MtM-Reihe (`research/mtm_drawdown/mtm_kern.py`): letzter Kurs, Änderung 0, Position bleibt offen und gebunden, Positionstage werden gezählt. Mit Probe bestätigt. Drei Dinge daneben, die der Zellen-Erzeuger nicht von selbst erbt (3.4).

### 3.1 Welche Kerne gibt es?

| Kandidat | bewertet er offene Positionen je Tag? | Laufbereich / Sperrliste |
|---|---|---|
| `research/mtm_drawdown/mtm_kern.py` (TB-73) | **ja** — `kurse_auf_raster` Z. 151–169, `mtm_pfad` Z. 176–256 | nein / nein |
| `research/exposure_messung/auswertung.py::mtm_reihen` Z. 305–341 | ja, als Näherung („Kapital zu Marktpreisen“, Kalendertage) | nein / nein |
| `research/exposure_messung/exposure_kern.py` | nein — nur `gebunden`/`n_offen` zum Einstand auf Kalendertagen (`taegliche_reihen`, Z. 44–82), kein Kurs | nein / nein |
| `research/exposure_messung/bot_lauf.py` | nein — holt Positionen aus `collect_all_trades`/`simulate_portfolio` (Z. 103–137), keine Tagesbewertung, kein Kurszugriff je Tag | Laufbereich (`paths.py:242`, a2 Z. 8) / nein |
| Zellen-Kern nach R43 (Register Z. 10843): `collect_all_trades` + `simulate_portfolio` → `shared/zuteilung.py::simuliere_portfolio` | nein — ereignisindiziert; `strategies/elliott_wave*/equity_simulation.py:21–22` „Offene Positionen werden nicht "mark-to-market" bewertet“ | Laufbereich, `zuteilung.py` Sperrliste |

Das Register nennt keinen Kern, den der Zellen-Erzeuger für die MtM-Reihe „übernimmt“ (Suche ab Z. 9000 nach „übernimmt/übernommen“ bei „Kern“/„MtM“: 0 Treffer). `mtm_kern.py` ist im Register die Messgrundlage zu R36 (Z. 10985: `mtm_kern.py:296–304`, „Raster Z. 135–139“; „die zwei Spalten nach R36 kommen mit dem Zellen-Erzeuger“) und in der Voraussetzung zu R48 (d) genannt (Z. 10882).

### 3.2 `mtm_kern.py` — Wortlaut der Stellen

`:151–169`
```python
def kurse_auf_raster(schlusskurse: dict, tage: pd.DatetimeIndex):
    """Schlusskurs je Symbol auf dem Raster, fehlende Tage fortgeschrieben.
    … True, wo kein eigener Kurs des Tages vorlag und der letzte bekannte genommen wurde).
    Vor dem ersten Kurs eines Symbols bleibt NaN; eine Position dort ist ein Datenfehler
    und wird gemeldet, nicht geraten (`mtm_pfad` bricht ab).
    """
    …
        eigene = r.reindex(tage)
        spalten[symbol] = eigene.ffill()
        fort[symbol] = eigene.isna() & spalten[symbol].notna()
```
`:240–247`
```python
        schluss = kurs_np[s][a:b + 1]
        if np.isnan(schluss).any():
            raise ValueError(f"{s}: Kurs fehlt zwischen …")
        unreal[a:b + 1] += allokation[i] * (schluss / einstand[i] - faktor_kosten)
        n_offen[a:b + 1] += 1
        gebunden[a:b + 1] += allokation[i]
        fort_zaehler[a:b + 1] += fort_np[s][a:b + 1].astype(int)
```

Am Lückentag also: kein `KeyError`, kein Auslassen des Tages, keine Bewertung zum Einstand, sondern Fortschreiben des letzten Kurses mit ausdrücklichem `ffill()` (nicht über die Voreinstellung von `pct_change`; die Abhängigkeit aus R72 (e) besteht hier nicht). Der unrealisierte Betrag der Position bleibt gleich, ihr Beitrag zur Änderung des Tages ist 0; sie bleibt in `n_offen` und `gebunden`; die Spalte `fortgeschrieben` zählt den Positionstag (das, was (c) als Bericht „je Bot die Zahl solcher Positionstage“ verlangt; heute summiert in `grundlage.py:139`, `messung.py:200`; Register Z. 4471 berichtet die Zählung der früheren Messung).

### 3.3 Mini-Probe (synthetisch, ausserhalb des Repos)

`/tmp/tb132_p3/p3_probe.py` der Geräte-Shell, zeichengleich `/home/claude/tb132/p3_probe.py`. Aufruf aus der Repo-Wurzel: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/tb132_p3/p3_probe.py "$PWD"`. Lädt `mtm_kern.py` und `exposure_kern.py` lesend; `mtm_reihen` wird per `ast` aus `exposure_messung/auswertung.py` herausgelöst (das Modul selbst wird nicht ausgeführt). Zwei Symbole X, Y, acht Börsentage D1–D8, eine Position in X von D2 bis D7. Rückgabewert **0**, pandas 2.3.3.

| Fall | Ergebnis |
|---|---|
| A (X ohne Zeile an D4, D5; Y mit Kurs) — und dasselbe mit leerem `close` | Lückentage stehen im Raster; Kurs X = Kurs von D3; `mtm` an D4 und D5 gleich `mtm` an D3 (Differenz 0,0); `n_offen` = 1, `gebunden` = Allokation; `fortgeschrieben` = 1 an D4, D5, Summe 2; D6 trägt die Bewegung über die Lücke |
| B (kein Symbol hat an D4 einen Kurs) | Das eigene Raster des Kerns (`tagesraster`) führt D4 **nicht**. Mit einem von aussen gegebenen Kalender-Raster steht D4, Kurs fortgeschrieben, `mtm` wie D3, `n_offen` 1, gezählt |
| C (Position vor dem ersten Kurs des Symbols) | `ValueError` („Kurs fehlt zwischen …“), kein Auffüllen rückwärts |
| D (Reihe von X endet nach D5, Position offen bis D8) | weiter zum letzten Kurs bewertet, offen, an jedem Folgetag gezählt |
| E (`exposure_messung/auswertung.py::mtm_reihen`) | Lückentage und Wochenende: Wert wie am letzten Kurstag; Position bleibt in `gebunden`/`n_offen` |

### 3.4 Was daneben steht (Tatsachen, für den Bau des Erzeugers)

1. **Raster.** `tagesraster` (Z. 135–148) ist die Vereinigung der Kurstage der übergebenen Symbole; der vorhandene Aufrufer übergibt nur die **gehandelten** Symbole (`messung.py:147` `grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")`). Ein Handelstag, an dem keines dieser Symbole einen Kurs trägt, fehlt dann in der Reihe (Fall B1). Das ist kein Widerspruch zu (c) (dort geht es um den Tag, der in der Reihe steht), berührt aber R66 (a) („ohne Lücke“): Der Erzeuger muss das Raster selbst geben; `kurse_auf_raster(schlusskurse, tage)` nimmt jedes Raster an (Fall B2).
2. **Exposure.** `mtm_kern` führt `gebunden` zum **Einstand** (Docstring Z. 186–188, Rechnung Z. 246), keine Exposure „bewertet wie die MtM-Reihe“ (Register Z. 10988 hält das schon fest). Am Lückentag bleibt die Position darin; die Bewertung der Exposure zum letzten Kurs wäre `gebunden + unrealisiert` (plus Kostenseite) und ist im Kern nicht gebildet.
3. **Tagesgrenze.** In `mtm_kern` ist eine Position am Ausstiegstag nicht mehr offen (`letzter = searchsorted(tagesende, exit, 'right') - 1`, Z. 219; Docstring Z. 28–39). `exposure_kern.taegliche_reihen` zählt Einstiegs- und Ausstiegstag mit und rechnet auf Kalendertagen (`freq="D"`, Z. 58; Schleife Z. 63–67). Kein Lückentag-Unterschied, aber zwei verschiedene Mengen „offen am Tag“.
4. **Zweite MtM-Stelle** `exposure_messung/auswertung.py::mtm_reihen` (Z. 305–341) schreibt am Lückentag ebenfalls fort (`.ffill()`, Z. 323), weicht aber sonst ab: Bezug ist der Schlusskurs des Einstiegstages statt `entry_price` (Docstring Z. 308–312), vor dem ersten Kurs wird rückwärts aufgefüllt (`.bfill()`, Z. 323) statt abgebrochen, und ein Symbol ganz ohne Kursreihe wird übersprungen (`continue`, Z. 320–322) — die Position fällt dann mit Wert 0 aus dem Kapital zu Marktpreisen, bleibt aber in `gebunden` (Probe E3). Würde diese Stelle übernommen, träfe die Voraussetzung am Lückentag selbst zu, an den Rändern nicht.
5. **Gegenbeispiel im Repo, nicht für die Bewertung:** `shared/zuteilung.py:306–312` rechnet für die Korrelation in der Zuteilung `kurse.pct_change(fill_method=None)` („Eine Luecke bleibt hier eine Luecke“). Das ist Sperrliste und Laufbereich, betrifft aber die Zuteilung, keine Tagesbewertung.
6. `test_mtm_kern.py` prüft das Fortschreiben am Lückentag nicht (Proben 1–3 und Gegenproben; einzig `:243–244` der Fall „vor dem ersten Kurs“). Die Eigenschaft ist heute nur durch die Probe oben belegt.

---

## P4 (R66 (f), Tatsachen) — aus v2 bestätigt, nicht neu gemessen

**Urteil: trifft; in v2 belegt.**

- v2 M1, Kopfzeile: „Kein Code auf der Sperrliste oder im Laufbereich bildet den Falten-Sharpe aus der Tagesreihe oder rechnet ihn nach.“
- v2 M1 Nr. 2: „**Kein Aufrufer.** `grep -E 'kz\.sharpe\(|kennzahlen\.sharpe\(|[^_a-z]sharpe\('` über `research/vorregistrierung/*.py` (Tests eingeschlossen) trifft nur die Definition.“
- v2 M1 Nr. 3: „`auswertung.py` liest `netto_sharpe` **nur aus `zellen.csv`**“ mit den Stellen `:353–354`, `:355–357`, `:395`, `:575–578`, `:622–623`, `:684`; „Nirgends wird der Wert gegen `tagesreihen/` geprüft.“
- Einschränkung, die v2 selbst nennt (M1 Nr. 4): `dsr_drei_werte` bildet einen nicht annualisierten Sharpe je Beobachtung aus der Tagesreihe des Gewinners auf den gemeinsamen Tagen (`auswertung.py:670` → `kennzahlen.py:226–234`). Das ist kein Falten-Sharpe; R66 (d) und (f) führen es als DSR-Eingabe und Nebenbefund.

Beiläufig beim Messen von P2 mitgesehen (kein Neumessen von P4): derselbe `grep`, erweitert auf `shared`, `strategies`, `docs/belege`, trifft ebenfalls nur die Definition.

---

## Nicht geprüft

1. **Lock-Umgebung.** Alle Proben liefen unter Python 3.10.12/numpy 2.2.6 (Geräte-Shell) bzw. pandas 3.0.5 (Container, nur P2). Die Wiederholung auf dem Betriebsrechner (Python 3.9.6, Lock) steht aus; das gilt auch für die Probe zu R71/R72 (a) aus v2.
2. **Kalendervergleich `"NYSE"` gegen `"XNYS"`** (1.5): Ersatzmessung mit dem Paket aus `trading-env/` unter fremdem Interpreter; nicht gegen die Kursdaten gehalten (das tat v3 nur für `"NYSE"`), und nur für das Fenster 2000–2026.
3. **`research/snapshotgrenze/ergebnisse/eingaben.json`** nicht geöffnet (Leseregel); der Inhalt des Feldes `kalender` ist aus dem Erzeuger und dem Ergebnisdokument erschlossen, nicht aus der Datei.
4. **P3 unter pandas 3.0.5** nicht gelaufen (`mtm_kern.py` liegt nicht im Container). Die Stelle benutzt ausdrückliches `ffill()`, nicht die Voreinstellung von `pct_change`; eine Abhängigkeit von der Fassung ist nicht zu erwarten, aber nicht gemessen.
5. **Welchen Kern der Zellen-Erzeuger tatsächlich übernimmt**, ist nicht prüfbar: Es gibt den Erzeuger nicht, und das Register nennt für die MtM-Reihe keinen. P3 gilt für die vorhandenen Kandidaten.
6. **Echte Daten:** Ob und wie oft ein Lückentag mit offener Position vorkommt, wurde nicht gemessen (keine Trade-Listen, keine Kurse gelesen).
7. P2: Der Schnitt der Tagesreihe auf die Falte und die Wahl der Periodenzahl liegen beim künftigen Aufrufer; geprüft sind nur die Funktion und `auswertung.perioden_je_jahr`.
