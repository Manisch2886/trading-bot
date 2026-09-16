# Testauftrag TB-41 — Registernachtrag (Mac)

**Autonom ausführbar.** Nichts an diesem Auftrag verlangt eine Entscheidung
während des Laufs. Er ist von oben nach unten abzuarbeiten; jeder Schritt sagt,
was zu erwarten ist und was ein Abbruchgrund wäre.

**Warum auf dem Mac:** In der Cloud fehlen `pandas` und `numpy`, Binance und
yfinance sind mit 403 gesperrt. Der Nachtrag konnte dort nur gegen das
**aufgeschriebene** Messergebnis von TB-40 prüfen. Auf dem Mac läuft die
Messung selbst — und genau das ist der Unterschied, auf den es hier ankommt:
**gegen eine frische Messung statt gegen ein Dokument.**

> ⚠️ **Dieser Auftrag ändert nichts.** Kein `--echt`, keine Order, keine
> Kursdatei, keine Registerdatei, kein `live_params.py`. Wenn ein Schritt
> schreiben will, ist das ein **Abbruchgrund**, kein Zwischenfall.

---

## 0. Voraussetzungen

```bash
cd ~/trading-bot            # Pfad ggf. anpassen
git fetch origin
git checkout claude/new-session-9dx5ul
git pull origin claude/new-session-9dx5ul
python3 --version           # notiert wird, was hier steht
```

**Erwartet:** Der Branch enthält `research/registernachtrag_tb41/` mit
`pruefe_register.py`, `test_registernachtrag_tb41.py` und `BERICHT.md`, und
`docs/VORREGISTRIERUNG_neuselektion.md` enthält einen **Abschnitt 16**.

```bash
ls research/registernachtrag_tb41/
grep -c "^## 16. Registernachtrag (TB-41" docs/VORREGISTRIERUNG_neuselektion.md
```

**Erwartet:** drei Dateien und `1`.

Ein Ergebnisordner wird **ausserhalb des Repos** angelegt — alles, was dieser
Auftrag erzeugt, landet dort:

```bash
mkdir -p ~/Downloads/TB-41_ergebnisse
AUS=~/Downloads/TB-41_ergebnisse
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
Nachtrags gelten für genau diesen Datenstand. Ein abweichender Hash heisst, dass
zwischendurch abgerufen wurde — Registertext 5 untersagt das für Aktiendateien
ausdrücklich zwischen Registereintrag und Selektionslauf.

---

## 2. Die Prüfung gegen das **Dokument** — dasselbe, was die Cloud gemacht hat

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
  --beleg-modus dokument \
  --json $AUS/02_pruefung_dokument.json | tee $AUS/02_pruefung_dokument.txt
echo "Rueckgabewert: $?" | tee -a $AUS/02_pruefung_dokument.txt
```

**Erwartet:** `KEIN BEFUND` und Rückgabewert `0`, neun geprüfte Punkte:
`symbolzahl, faltenevidenz, min_history, umstellungstag, universumsdatei,
datenstand, daten_unberuehrt, null_entfernte_zeilen, ersetzt_gekennzeichnet`.

⚠️ Steht bei `null_entfernte_zeilen` ein Befund, ist der Vergleichsstand falsch
gewählt — dann einmal mit `--basis origin/main` wiederholen und **beides**
ablegen.

---

## 3. Die Prüfung gegen eine **frische Messung** — der eigentliche Grund für den Mac

Das ruft `research/universum_trockenlauf/universum_trockenlauf.py` auf. Das
Werkzeug ist **unverändert**; es wird nur aufgerufen. Der Lauf braucht kein
Netz und dauert wenige Minuten.

```bash
python3 research/registernachtrag_tb41/pruefe_register.py \
  --beleg-modus trockenlauf \
  --arbeitsverzeichnis $AUS \
  --json $AUS/03_pruefung_trockenlauf.json | tee $AUS/03_pruefung_trockenlauf.txt
echo "Rueckgabewert: $?" | tee -a $AUS/03_pruefung_trockenlauf.txt
```

**Erwartet:** `Quelle beleg: trockenlauf` und `KEIN BEFUND`, Rückgabewert `0`.

⚠️ **Das ist der Schritt, der in der Cloud nicht laufen konnte.** Meldet er
einen Befund, während Schritt 2 keinen gemeldet hat, dann weichen die frische
Messung und das aufgeschriebene Ergebnis von TB-40 voneinander ab — **das ist
ein echter Fund und ein Abbruchgrund.** Dann: `$AUS/trockenlauf.json`
mitschicken und nichts reparieren.

---

## 4. Der Selbsttest mit den Mutationsproben

```bash
python3 research/registernachtrag_tb41/test_registernachtrag_tb41.py \
  | tee $AUS/04_selbsttest.txt
echo "Rueckgabewert: $?" | tee -a $AUS/04_selbsttest.txt
```

**Erwartet:** `41/41 Prüfungen bestanden.` und Rückgabewert `0`.

Der Test legt sein eigenes Wegwerf-Verzeichnis an und räumt es wieder ab. Er
schreibt **nicht** ins Repo; Schritt 6 weist das nach.

---

## 5. Die Gegenprobe: eine falsche Zahl wird gefunden

Dieser Schritt ändert **nichts am Repo**. Er legt eine **Kopie** des Registers
an, verdreht dort **eine** Zahl und lässt das Werkzeug darauf los. *Ein Test,
der nur bestätigt, dass alles stimmt, hat nicht gezeigt, dass er etwas findet.*

```bash
KOPIE=$(mktemp -d)
cp docs/VORREGISTRIERUNG_neuselektion.md $KOPIE/register.md
cp docs/ERGEBNIS_TB-40_universum_trockenlauf.md $KOPIE/beleg.md
python3 - "$KOPIE/register.md" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
alt = "> | `elliott_wave_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 147 | 150 |"
neu = "> | `elliott_wave_stocks` | 137 / 137 / 139 / 139 / 140 / 142 / 145 | 150 | 150 |"
assert t.count(alt) == 1, t.count(alt)
open(p, "w", encoding="utf-8").write(t.replace(alt, neu))
print("eine Zahl verdreht: Bestaetigung 147 -> 150")
PY
python3 research/registernachtrag_tb41/pruefe_register.py \
  --nur symbolzahl --register $KOPIE/register.md --beleg $KOPIE/beleg.md \
  --beleg-modus dokument | tee $AUS/05_gegenprobe.txt
echo "Rueckgabewert: $?" | tee -a $AUS/05_gegenprobe.txt
rm -rf $KOPIE
```

**Erwartet:** genau **ein** Befund
(`elliott_wave_stocks bestaetigung: Register 150, gemessen 147`) und
Rückgabewert **`1`**.

⚠️ Kommt hier `KEIN BEFUND`, ist die Prüfung wertlos — **abbrechen und melden.**

---

## 6. Der Nachweis „nichts geändert"

```bash
python3 - <<'PY' | tee $AUS/06_datenstand_nachher.txt
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "research", "vorregistrierung"))
import herkunft
print(herkunft.datenstand())
PY
git status --porcelain | tee $AUS/06_git_status.txt
git status --porcelain -- data | tee $AUS/06_git_status_data.txt
```

**Erwartet:**
* derselbe Hash wie in Schritt 1 — `d9449faf51bffaaa…`, 223 Dateien;
* `06_git_status_data.txt` ist **leer**;
* `06_git_status.txt` ist leer oder zeigt nur unbeteiligte lokale Dateien.

---

## 7. Die bestehenden Tests

```bash
{
for T in research/faltenplan_neun/test_faltenplan_neun.py \
         research/universum_trockenlauf/test_universum_trockenlauf.py \
         research/etf_trendfolge/test_etf_trendfolge.py \
         research/vorregistrierung/test_vorregistrierung.py \
         research/versuchsregister/test_versuchsregister.py; do
  echo "### $T"
  python3 "$T" >/dev/null 2>&1
  echo "Rueckgabewert: $?"
done
} | tee $AUS/07_bestehende_tests.txt
```

**Erwartet:** überall `Rueckgabewert: 0`.

⚠️ **Bekannt rot und TB-41-fremd** (nicht als Fund melden):
`shared/test_drawdown_beide_masse.py` (Zeitüberschreitung),
`shared/test_kursdaten.py`, `shared/test_stabile_sortierung.py`,
`shared/test_wellenauswahl.py`, `dashboard/test_portfolio_sicht.py`,
`research/exposure_messung/test_exposure_kern.py`,
`system/test_log_rotation.py` (flattert). Ohne `node` meldet
`dashboard/test_dashboard.py` 780/780 statt 784.

---

## 8. Alles einpacken

```bash
cd ~/Downloads
zip -r TB-41_registernachtrag_ergebnisse.zip TB-41_ergebnisse
ls -lh ~/Downloads/TB-41_registernachtrag_ergebnisse.zip
```

⚠️ **Die ZIP-Datei liegt in `~/Downloads`, nicht im Repo.** Sie wird
zurückgeschickt; im Repo hat sie nichts zu suchen.

**Inhalt:**

| Datei | Was drinsteht |
|---|---|
| `01_datenstand_vorher.txt` | Kursdatenstand vor dem Lauf |
| `02_pruefung_dokument.txt` / `.json` | die neun Prüfungen gegen das TB-40-Dokument |
| `03_pruefung_trockenlauf.txt` / `.json`, `trockenlauf.json` | dieselben Prüfungen gegen die **frische Messung** |
| `04_selbsttest.txt` | 41/41 |
| `05_gegenprobe.txt` | der Nachweis, dass eine falsche Zahl gefunden wird |
| `06_datenstand_nachher.txt`, `06_git_status*.txt` | der Nachweis „nichts geändert" |
| `07_bestehende_tests.txt` | Rückgabewert je Testdatei |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob die Zahlen, die neu ins Vorab-Dokument („Register") eingetragen wurden,
wirklich mit der Messung übereinstimmen — und zwar mit einer Messung, die auf
**deinem** Rechner frisch läuft, nicht nur mit dem Blatt Papier, auf dem sie
letzte Woche notiert wurde.

**Was herauskam.**
Das weisst du nach Schritt 3. Erwartet wird: **kein Befund**, zweimal — einmal
gegen das Dokument (Schritt 2) und einmal gegen die frische Messung
(Schritt 3). Dazu `41/41` im Selbsttest und ein unveränderter Kursdatenstand.

**Warum das so ist.**
In der Cloud fehlen Programmteile, die die Bots zum Rechnen brauchen, und das
Internet ist gesperrt. Dort konnte nur geprüft werden: *„Steht im Register
dieselbe Zahl wie im Messbericht?"* Auf deinem Mac lässt sich zusätzlich fragen:
*„Und stimmt der Messbericht überhaupt noch?"* Das ist die schärfere Frage,
und deshalb gibt es diesen Auftrag.

**Was das für dich heisst.**
Acht Schritte, von oben nach unten, jeweils den Befehl ins Terminal kopieren.
Jeder Schritt schreibt seine Ausgabe in eine Datei in
`~/Downloads/TB-41_ergebnisse`; Schritt 8 packt alles in **eine ZIP-Datei in
`~/Downloads`** — die schickst du zurück. **Nichts davon verändert etwas**:
keine Kursdatei, keine Einstellung, keine Order. Schritt 5 macht absichtlich
eine Kopie kaputt, um zu zeigen, dass die Prüfung überhaupt etwas findet — die
Kopie wird danach gelöscht, dein Register bleibt unberührt. Wenn irgendwo etwas
anderes steht als „erwartet", brich ab und melde es, statt es zu reparieren.

---

*TB-41, 16.09.2026. Kein Selektionslauf, kein signierter Tag, keine
Parameterübernahme.*
