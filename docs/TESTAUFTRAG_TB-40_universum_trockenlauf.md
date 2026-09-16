# Testauftrag TB-40 — Universum-Trockenlauf (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Warum auf dem Mac:** dort liegen die echten Kursdaten, dort läuft die
Python-Umgebung der Bots, und dort ist Binance/yfinance erreichbar. Die
Cloud-Messung ist vollständig, aber sie soll am Rechner des Nutzers bestätigt
werden — die Zahlen dieser Aufgabe gehen als Tatsachennotiz ins Register.

> ⚠️ **Dieser Auftrag ändert nichts.** Kein `--echt`, keine Order, keine
> Kursdatei, keine Registerdatei, kein `live_params.py`. Wenn ein Schritt
> schreiben will, ist das ein Abbruchgrund, kein Zwischenfall.

---

## 0. Voraussetzungen

```bash
cd ~/trading-bot            # Pfad ggf. anpassen
git fetch origin
git checkout claude/new-session-06epnh
git pull origin claude/new-session-06epnh
python3 --version           # notiert wird, was hier steht
```

**Erwartet:** Der Branch enthält den Ordner `research/universum_trockenlauf/`
mit drei Python-Dateien und `BERICHT.md`.

```bash
ls research/universum_trockenlauf/
```

Ein Ergebnisordner wird **ausserhalb des Repos** angelegt — alles, was dieser
Auftrag erzeugt, landet dort:

```bash
mkdir -p ~/Downloads/TB-40_ergebnisse
AUS=~/Downloads/TB-40_ergebnisse
```

---

## 1. Datenstand vorher festhalten

```bash
python3 - <<'PY' | tee $AUS/01_datenstand_vorher.txt
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "research", "vorregistrierung"))
import herkunft
print(herkunft.datenstand())
PY
```

**Erwartet:**
`{'datenstand': 'd9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84', 'dateien': 223}`

⚠️ **Steht dort etwas anderes: abbrechen und melden.** Alle Zahlen dieses
Auftrags gelten für genau diesen Datenstand. Ein abweichender Hash heisst, dass
zwischendurch abgerufen wurde — Registertext 5 untersagt das für Aktiendateien
ausdrücklich zwischen Registereintrag und Selektionslauf.

---

## 2. Der Trockenlauf

Läuft ohne Netz und dauert wenige Minuten.

```bash
python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --nur-universum --json $AUS/02_trockenlauf.json \
    2> $AUS/02_fortschritt.txt | tee $AUS/02_trockenlauf.txt
```

**Erwartet — die Tabelle „Symbolzahl je Falte: eingetragen gegen gemessen"
enthält genau diese gemessenen Reihen (Spalte H):**

| Bot | gemessen H |
|---|---|
| `elliott_wave` | 6 / 13 / 13 · B 18 |
| `t3_supertrend` | 3 / 6 / 9 / 13 / 13 / 13 / 17 · B 18 |
| `rsi2_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20 |
| `turtle_soup_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20 |
| `volatility_breakout_crypto` | 6 / 9 / 10 / 13 / 13 / 17 / 18 · B 20 |
| die vier Aktien-Bots | 137 / 137 / 139 / 139 / 140 / 142 / 145 · B 147 |

und in Spalte F:

| Bot | gemessen F |
|---|---|
| `elliott_wave` | 0 / 6 / 13 · B 13 |
| `t3_supertrend` | 0 / 3 / 6 / 9 / 13 / 13 / 13 · B 17 |
| die drei Krypto-Tagesbots | 2 / 6 / 9 / 10 / 13 / 13 / 17 · B 18 |
| die vier Aktien-Bots | 136 / 137 / 137 / 139 / 139 / 140 / 142 · B 145 |

**Ebenfalls erwartet, am Ende der Ausgabe:**

```
Monotonie geprueft: ueber alle Stichtage waechst die Menge der handelbaren
Symbole nur.
```

⚠️ **Weicht eine Zahl ab: nicht korrigieren, sondern notieren** — mit der
kompletten Zeile aus `02_trockenlauf.txt`. Eine Abweichung zwischen Mac und
Cloud auf demselben Datenstand wäre selbst der wichtigste Befund dieses
Auftrags.

---

## 3. Der Trockenlauf ist wiederholbar

```bash
python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --nur-universum --json $AUS/03_trockenlauf_zweiter.json \
    2>/dev/null > /dev/null
python3 - <<'PY' | tee $AUS/03_wiederholbar.txt
import json, os
a = json.load(open(os.path.expanduser("~/Downloads/TB-40_ergebnisse/02_trockenlauf.json")))
b = json.load(open(os.path.expanduser("~/Downloads/TB-40_ergebnisse/03_trockenlauf_zweiter.json")))
gleich = all(x["gemessen_H"] == y["gemessen_H"] and x["gemessen_F"] == y["gemessen_F"]
             for bot in a["bots"]
             for x, y in zip(a["bots"][bot]["falten"], b["bots"][bot]["falten"]))
print("Zweiter Lauf, gleiche Listen Symbol fuer Symbol:", gleich)
PY
```

**Erwartet:** `Zweiter Lauf, gleiche Listen Symbol fuer Symbol: True`

---

## 4. Die stillen Filter

```bash
python3 research/universum_trockenlauf/universum_trockenlauf.py \
    --stille-filter --json $AUS/04_stille_filter.json \
    2>/dev/null | tee $AUS/04_stille_filter.txt
```

**Erwartet:**

* Spalte `voll` und `genau_an_der_grenze`: bei allen neun **`geladen`**.
* Spalte `eins_zu_kurz`: bei allen neun **nicht geladen**; bei
  `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` steht dort
  **`STILL raus`**.
* Spalte `luecke_gleiche_spanne`: bei `elliott_wave` **raus**, bei den übrigen
  acht **`geladen`**.

---

## 5. Datenstand nachher — der eigentliche Test

```bash
python3 - <<'PY' | tee $AUS/05_datenstand_nachher.txt
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "research", "vorregistrierung"))
import herkunft
print(herkunft.datenstand())
PY
diff $AUS/01_datenstand_vorher.txt $AUS/05_datenstand_nachher.txt \
     && echo "GLEICH — der Trockenlauf hat nichts an data/ veraendert." \
     | tee -a $AUS/05_datenstand_nachher.txt
```

**Erwartet:** `GLEICH — der Trockenlauf hat nichts an data/ veraendert.`

Zusätzlich:

```bash
git status --porcelain | tee $AUS/05_git_status.txt
```

**Erwartet:** leer (oder nur Dateien, die schon vorher geändert waren).
⚠️ Steht dort eine Datei unter `data/`, `results/` oder `docs/` — abbrechen und
melden.

---

## 6. Der Selbsttest des Werkzeugs

```bash
python3 research/universum_trockenlauf/test_universum_trockenlauf.py \
    2>&1 | tee $AUS/06_selbsttest.txt
echo "Rueckgabewert: $?" | tee -a $AUS/06_selbsttest.txt
```

**Erwartet:** `42/42 Pruefungen bestanden.` und Rückgabewert `0`.

Darin enthalten sind die vier verlangten Proben:
* **D** ein künstlich verkürztes Symbol fällt heraus; ein Symbol **genau an der
  Grenze** wird geladen — an zwei Bots mit verschiedener Schranke,
* **E** eine veränderte Registerzahl wird als Abweichung gemeldet,
* **F** ein wirkungslos gemachter Stichtag fällt auf,
* **G/H** die beiden Wachen gegen das Schreiben, **einzeln** geprüft.

---

## 7. Gegenprobe: der Befund, der die Aufgabe ausgelöst hat

```bash
python3 strategies/rsi2_crypto/multi_symbol_optimise.py 2>&1 \
    | head -20 | tee $AUS/07_gegenprobe_rsi2.txt
```

⚠️ Dieses Skript rechnet anschliessend ein Raster; **nach den ersten Zeilen mit
`Ctrl-C` abbrechen** — gebraucht wird nur der Ladeteil.

**Erwartet (die vier Hinweiszeilen und die Summenzeile):**

```
Hinweis: ENSOUSDT deckt nur 335 Tage ab (< 500 noetig), wird uebersprungen.
Hinweis: PUMPUSDT deckt nur 368 Tage ab (< 500 noetig), wird uebersprungen.
Hinweis: ZKCUSDT  deckt nur 364 Tage ab (< 500 noetig), wird uebersprungen.
Hinweis: UUSDT    deckt nur 244 Tage ab (< 500 noetig), wird uebersprungen.

Daten geladen: 20 Symbole
```

Damit ist belegt, dass der Trockenlauf und der Bot dasselbe sagen: **20 von 24**,
und dieselben vier Symbole namentlich.

---

## 8. Alle bestehenden Tests

```bash
: > $AUS/08_alle_tests.txt
for t in $(find . -name "test_*.py" | sort); do
    timeout 900 python3 "$t" > /dev/null 2>&1
    echo "$? $t" >> $AUS/08_alle_tests.txt
done
grep -v '^0 ' $AUS/08_alle_tests.txt
```

**Erwartet:** nur die vorbestehend roten Tests. Bekannt rot und TB-40-fremd:

* `shared/test_drawdown_beide_masse.py` (Zeitüberschreitung)
* `shared/test_kursdaten.py`, `shared/test_stabile_sortierung.py`,
  `shared/test_wellenauswahl.py`
* `dashboard/test_portfolio_sicht.py`
* `research/exposure_messung/test_exposure_kern.py`
* `system/test_log_rotation.py` (flattert)

⚠️ **`research/universum_trockenlauf/test_universum_trockenlauf.py` muss grün
sein.** Ist er es nicht, ist das ein Befund dieser Aufgabe.

*Hinweis:* Ohne `node` meldet `dashboard/test_dashboard.py` 780/780 statt 784.
Auf dem Mac mit `node` sind 784 zu erwarten.

---

## 9. Abgabe — das ZIP

```bash
cd ~/Downloads
zip -r TB-40_universum_trockenlauf_ergebnisse.zip TB-40_ergebnisse
ls -l TB-40_universum_trockenlauf_ergebnisse.zip
```

⚠️ **Das ZIP liegt in `~/Downloads`, nicht im Repo.** Es enthält:

| Datei | Inhalt |
|---|---|
| `01_datenstand_vorher.txt` | Hash und Dateizahl vor dem Lauf |
| `02_trockenlauf.txt` / `.json` | die Messung, lesbar und maschinenlesbar |
| `02_fortschritt.txt` | welcher Bot wann gemessen wurde |
| `03_wiederholbar.txt` / `03_trockenlauf_zweiter.json` | zweiter Lauf |
| `04_stille_filter.txt` / `.json` | die sieben Fälle je Bot |
| `05_datenstand_nachher.txt`, `05_git_status.txt` | der Nachweis „nichts geändert" |
| `06_selbsttest.txt` | 42/42 |
| `07_gegenprobe_rsi2.txt` | der ausgelösende Befund am Bot selbst |
| `08_alle_tests.txt` | Rückgabewert je Testdatei |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob die Messung, die in der Cloud gemacht wurde, auf deinem Mac genauso
herauskommt. In der Cloud fehlen ein paar Programmteile und das Internet ist
gesperrt; auf deinem Mac ist alles vollständig. Eine Zahl, die gleich bleibt,
wenn man sie an zwei verschiedenen Orten misst, ist eine belastbare Zahl.

**Was herauskam.**
Das weisst du nach Schritt 9. Erwartet wird: **dieselben Zahlen wie in der
Tabelle in Schritt 2**, ein unveränderter Kursdatenstand (Schritt 5) und
`42/42 Prüfungen bestanden` (Schritt 6).

**Warum das so ist.**
Der Trockenlauf liest nur Dateien, die schon auf der Platte liegen, und fragt für
jeden Zeitraum: *„Hätte das Programm diesen Handelswert damals überhaupt
mitgerechnet?"* Dafür braucht er kein Internet und keine frischen Kurse. Deshalb
darf die Antwort auf zwei verschiedenen Rechnern nicht auseinandergehen — und
wenn sie es doch tut, ist genau das der Fund, auf den es ankommt.

**Was das für dich heisst.**
Du arbeitest die neun Schritte von oben nach unten ab und kopierst jeweils den
Befehl in den Terminal. Jeder Schritt schreibt seine Ausgabe in eine Datei in
`~/Downloads/TB-40_ergebnisse`. Am Ende packt Schritt 9 alles in **eine
ZIP-Datei in `~/Downloads`** — die schickst du zurück. **Nichts davon verändert
etwas**: keine Kursdatei, keine Einstellung, keine Order. Wenn irgendwo etwas
anderes steht als „erwartet", brich ab und melde es, statt es zu reparieren.

---

*TB-40, 16.09.2026.*
