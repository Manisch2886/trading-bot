# Mac-Testauftrag TB-52 — Resolver-Modus und die zwei AST-Masse

**Zweig:** `claude/new-session-7xve52` · **Basis:** `062bacf`
**Angefordert VOR dem Merge**, nicht danach.

> ⚠️ **Warum dieser Auftrag nicht optional ist.** `shared/paths.py` wird von
> **145 Modulen** importiert und läuft im **Cron**. Eine kaputte Fassung legt
> neun Bots still — und die neun Datenbanken sind die **einzige OOS-Evidenz**
> des Projekts und **nicht neu berechenbar**.
>
> ⚠️ **Und: grün in der Cloud heisst strukturell nicht grün auf dem Mac.**
> Cloud 3.11.15, Mac **3.9.6**. Drei Punkte dieses Auftrags sind in der Cloud
> **gar nicht** prüfbar.

**Interpreter: immer `trading-env/bin/python3`.** *Der TB-45-Auftrag schrieb an
mehreren Stellen `python3` vor; dort fiel alles rot aus, was `binance` braucht —
ohne dass irgendetwas kaputt war.*

---

## ⚠️ Schritt 0 — Sicherung der neun Datenbanken. VOR allem anderen.

**Prüfprinzip D6:** *`git pull` überschreibt eine gitignorierte Datei
kommentarlos*, wenn ein Commit eine Datei am selben Pfad hinzufügt. Die neun
`*.db` existieren **nur hier** und sind **nicht neu berechenbar**.

```
cd ~/trading-bot
mkdir -p ~/tb52_sicherung
cp -p paper_trading_*.db ~/tb52_sicherung/
ls -l ~/tb52_sicherung/ | wc -l          # erwartet: 10 (9 Dateien + Kopfzeile)
shasum -a 256 paper_trading_*.db > ~/tb52_sicherung/VORHER.sha256
cat ~/tb52_sicherung/VORHER.sha256
```

⚠️ **Erst weitermachen, wenn hier neun Zeilen stehen.**

```
git status --short                        # muss leer sein, sonst STOPP
git fetch origin claude/new-session-7xve52
git checkout claude/new-session-7xve52
```

---

## Schritt 1 — ⭐ Der Pfadvergleich auf Python 3.9.6

**Das Kernstück.** Die Freigabe für `paths.py` hängt an einer Bedingung: *ohne
gesetzten Modus dieselben Zeichenketten wie vorher, für alle neun Bots.*
In der Cloud gemessen: **99 Pfade, 0 Unterschiede** — aber auf **3.11.15**.

```
trading-env/bin/python3 research/resolver_selektion/pfadvergleich.py
```

**Erwartet, und bitte alle vier Zeilen zurückmelden:**

| | erwartet |
|---|---|
| `Verglichene Pfade` | **99** |
| `Unterschiede` | ⭐ **0** |
| `Selbstprobe` | **JA, 9 Unterschiede gefunden** |
| Rückgabewert (`echo $?`) | **0** |

> ⚠️ **Ist `Unterschiede` nicht 0: abbrechen und berichten.** Nicht weitermachen.
> ⚠️ **Sagt die Selbstprobe NEIN**, misst der Vergleich nichts — dann ist auch
> eine 0 wertlos (Prüfprinzip **A5**).

---

## Schritt 2 — Die Wache und die zwei Masse auf 3.9.6

```
trading-env/bin/python3 shared/test_paths.py                        ; echo "rc=$?"
trading-env/bin/python3 research/resolver_selektion/kindprozess.py  ; echo "rc=$?"
trading-env/bin/python3 research/selektionsmasse/test_wanduhr.py    ; echo "rc=$?"
trading-env/bin/python3 research/selektionsmasse/test_eigener_pfadbau.py ; echo "rc=$?"
```

| | erwartet in der Cloud | rc |
|---|---|---|
| `test_paths.py` | **24 von 24 bestanden** | 0 |
| `kindprozess.py` | **alle 7 Messungen wie erwartet** | 0 |
| `test_wanduhr.py` | Ausgangszahl **6**, Stand **6**, Mutationsprobe 7/7 | 0 |
| `test_eigener_pfadbau.py` | Ausgangszahl **29**, Stand **29**, Mutationsprobe 5/5 | 0 |

⚠️ **Weicht eine Zahl ab, ist das ein Befund** — bitte mit der vollen Ausgabe
zurückmelden, nicht nur „rot".

⚠️ **Besonders auf 3.9 im Auge behalten:** `paths.py` benutzt ein
Modul-`__getattr__` (PEP 562, ab 3.7) und die Masse lesen `Subscript.slice`
**ohne** `ast.Index` (ab 3.9). Beides sollte auf 3.9.6 tragen — *sollte* ist
genau der Grund für diesen Schritt.

---

## Schritt 3 — ⚠️ Der Nachweis, dass der echte Cron den Modus nicht trägt

**In der Cloud strukturell nicht prüfbar.** Hier steht die echte Crontab.

> ⚠️ **Die Crontab wird NUR GELESEN.** Kein `crontab -e`, kein `crontab -`.

```
crontab -l | grep -c "TB_SELEKTION"
```

⭐ **Erwartet: `0`** — der Modus steht in keiner Cron-Zeile.

```
crontab -l | grep -c "trading-bot"
```

*(Nur zur Einordnung, wie viele Bot-Zeilen es gibt — die Zahl bitte mitmelden.)*

**Und die zweite Hälfte: trägt ein Cron-Lauf den Modus über die Umgebung?**

```
grep -c "TB_SELEKTIONSWURZEL" ~/.zshrc ~/.zprofile ~/.bash_profile ~/.profile 2>/dev/null
```

⭐ **Erwartet: überall `0`.** *(⚠️ `grep -c`, nicht `cat` — in diesen Dateien
können Zugangsdaten stehen, ARBEITSWEISE §7.)*

**Zum Schluss der Gegenbeweis am laufenden Bot** — ein echter Trockenlauf und
die Frage, ob er etwas vom Modus gesehen hat:

```
trading-env/bin/python3 -c "import sys; sys.path.insert(0,'shared'); import paths; print('Modus:', paths.selektionsmodus()); print('DATA_DIR:', paths.DATA_DIR)"
```

⭐ **Erwartet: `Modus: None`** und `DATA_DIR` = `…/trading-bot/data`.

---

## Schritt 4 — ⚠️ Die neun Datenbanken byteweise, vorher gegen nachher

**Der Punkt, um den es am Ende geht: hat diese Arbeit eine Datenbank angefasst?**
Erwartet: **nein, keine einzige.**

```
shasum -a 256 paper_trading_*.db > ~/tb52_sicherung/NACHHER.sha256
diff ~/tb52_sicherung/VORHER.sha256 ~/tb52_sicherung/NACHHER.sha256 && echo "IDENTISCH (9 von 9)" || echo "⚠️ ABWEICHUNG - SOFORT BERICHTEN"
```

⭐ **Erwartet: `IDENTISCH (9 von 9)`.**

⚠️ **Und byteweise, nicht nur über die Quersumme** — eine Quersumme beantwortet
eine andere Frage als ein Byte-Vergleich, wenn eine Datei **wächst**:

```
for f in paper_trading_*.db; do cmp -s "$f" ~/tb52_sicherung/"$f" && echo "gleich: $f" || echo "⚠️ VERSCHIEDEN: $f"; done
```

⭐ **Erwartet: neun Zeilen `gleich:`.**

> ⚠️ **Läuft währenddessen ein Cronjob, darf sich eine Datenbank ändern** — das
> wäre dann der Bot bei der Arbeit, nicht diese Änderung. **Bitte in dem Fall
> die Uhrzeit mitmelden**, damit es sich gegen `crontab -l` einordnen lässt.

---

## Schritt 5 — Datenstand vorher und nachher

```
trading-env/bin/python3 -c "import sys; sys.path.insert(0,'shared'); import snapshot; h,n = snapshot.gesamthash('data'); print(h, n); print('TRIFFT:', h==snapshot.VERANKERTER_DATENSTAND and n==223)"
```

⭐ **Erwartet:**
`d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84 223`
und `TRIFFT: True`.

---

## Schritt 6 — Basislauf

**GNU `timeout` fehlt auf dem Mac** — der Basislauf bringt seinen eigenen
Python-Runner mit.

```
trading-env/bin/python3 research/datenordner_schnitt/basislauf.py --grenze 300
```

⚠️ **Bekannt rot auf dem Mac, nicht von diesem Zweig verursacht** —
`shared/test_stabile_sortierung.py` (3) · `shared/test_wellenauswahl.py` (1) ·
`research/exposure_messung/test_exposure_kern.py` (1) ·
`research/hrp_portfolio/test_hrp_core.py` (scipy fehlt) ·
`dashboard/test_portfolio_sicht.py` (1).

⚠️ **Flackernd:** `system/test_log_rotation.py` — grün im Regelfall,
zeitabhängig rot, Rate ~30 % (TB-49, zehn Läufe). **Beide Ausgänge sind
erwartet.**

⚠️ **Ungeprüft, nicht grün:** die drei Dateien, die ein Bot-Argument verlangen.

**Neu in diesem Zweig und erwartet grün:** `shared/test_paths.py`,
`research/selektionsmasse/test_wanduhr.py`,
`research/selektionsmasse/test_eigener_pfadbau.py`.

---

## Was zurückkommen sollte

1. Die vier Zeilen aus **Schritt 1** (Pfade, Unterschiede, Selbstprobe, rc).
2. Die vier Rückgabewerte aus **Schritt 2**, bei Abweichung die volle Ausgabe.
3. Die drei Zahlen aus **Schritt 3** — ⭐ besonders `crontab -l | grep -c
   "TB_SELEKTION"`.
4. `IDENTISCH (9 von 9)` und die neun `gleich:`-Zeilen aus **Schritt 4**.
5. Datenstand aus **Schritt 5**.
6. Die Summenzeile des Basislaufs aus **Schritt 6**, mit den vier Stufen.
7. ⚠️ **Jede Abweichung von `docs/UMGEBUNGEN.md`**, die dabei auffällt —
   Paketfassungen, fehlende Werkzeuge. *Die Liste altert; eine Sitzung, die sie
   stillschweigend für falsch hält, hilft niemandem.*
