# Backlog-Nachtrag 18.09.2026 (f) — TB-52 Mac-Lauf

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(e) voraus.** (a)–(c) sind eingearbeitet; **(d), (e) und (f)
liegen uneingearbeitet im Repo** — ⭐ **alle drei in EINER Sitzung, in dieser
Reihenfolge.**

---

## Ergänzung zu Block 2k

**Anzufügen an die Tabelle von Block 2k:**

| # | Punkt |
|---|---|
| **T52.14** | ⭐ **MAC-LAUF 18.09., 22:29–23:03, Python 3.9.6: ALLE SOLLWERTE GETROFFEN.** Pfadvergleich **99 / 0 Unterschiede**, Selbstprobe **beisst (9)** · `shared/test_paths.py` **24/24** · `kindprozess.py` **alle 7 Messungen** · Mass 1 **6/6**, Mass 2 **29/29**, Mutationsproben **7/7** und **5/5** · Datenstand `d9449faf…`/223 `TRIFFT: True` · `git status` leer, **kein Snapshot-Ordner**. ⭐ **Zwei Sprachdetails tragen auf 3.9.6**, die die Cloud nicht prüfen konnte: Modul-`__getattr__` (PEP 562) und `Subscript.slice` ohne `ast.Index` |
| **T52.15** | ⭐⭐ **DER CRON TRÄGT DEN MODUS NICHT — vierfach geprüft, mit Gegenbeweis.** `crontab -l \| grep -c TB_SELEKTION` = **0** · **keine** `SHELL=`/`BASH_ENV=`/`source`-Zeile im Crontab · `~/.bash_profile` = 0, die anderen drei Profildateien **existieren nicht** · Gegenbeweis: `Modus: None`, `DATA_DIR: …/trading-bot/data`. **Das waren die vier Wege, auf denen eine Umgebungsvariable hineinkäme — keiner trägt sie** |
| **T52.16** | ⭐ **EINE DATENBANK ÄNDERTE SICH — und die Prüfung war die richtige.** 22:30:58 **9 von 9 identisch**; nach dem Basislauf 23:02:34 **8 von 9**. `paper_trading_volatility_breakout.db`, geändert **22:50:43** ⇒ Crontab-Zeile `50 22 * * 1-5 … volatility_breakout/forward_test.py`, Bot-Protokoll `Forward-Test-Lauf: 2026-09-18T20:50:01` **(UTC)**. ⭐ **Gegen den Crontab-Eintrag desselben Bots UND gegen dessen Protokoll gerechnet, Ortszeit gegen UTC — beides auf die Minute.** *Erster Einsatz der Regel aus `ARBEITSWEISE.md` §7 (ergänzt 18.09.), und sie hat gehalten* |
| **T52.17** | ⭐ **BASISLAUF: 59 grün / 5 rot / 1 flackernd / 3 ungeprüft / 1 Zeitgrenze = 69, UNERWARTET 0.** Gegen die Cloud (11 rot, 8 UNERWARTET): **die sechs zusätzlichen waren fehlende Pakete** — auf dem Mac sind `binance 1.0.37` und `yfinance 1.2.0` vorhanden. ⭐ **Die Cloud hatte es bereits gegen die Basis gegengeprüft; der Mac bestätigt es unabhängig.** Die Flackerstufe arbeitet im echten Lauf: `[~~~~] … flackernd (Mac ~30 %, …): heute gruen`, **nicht UNERWARTET**. Kein Enkelprozess nach der Zeitgrenze |
| **T52.18** | ⭐⭐ **PRÜFPRINZIP A6 HAT HEUTE ABEND DEN FEHLER VERHINDERT, AUS DEM ES HEUTE MITTAG ENTSTAND.** `UMGEBUNGEN.md` sagt, `test_drawdown_beide_masse.py` hinterlasse einen Kindprozess; in diesem Lauf tat sie es **nicht** (Prozessgruppen-Abbruch aus TB-47 griff). **Die Sitzung hat den Vermerk NICHT gestrichen**, sondern geschrieben: ⭐ ***„Eine Einzelmessung, kein Gegenbeweis."*** ⚠️ *Genau das war mein Fehler bei `test_log_rotation.py` (T49.17) — ein dokumentierter Befund, mit einer Einzelmessung überstimmt* |
| **T52.19** | ⚠️ **`UMGEBUNGEN.md` sagt „65 Testdateien" — es sind 69.** Die Zahl wurde **am selben Tag** von 62 auf 65 berichtigt; seither kamen `test_paths.py`, `test_wanduhr.py`, `test_eigener_pfadbau.py` (TB-52) und `test_flackerstufe.py` (TB-51) dazu. ⭐ **Empfehlung: die Zahl ersatzlos streichen und durch die Regel ersetzen** — *„der Basislauf zählt die Dateien selbst und nennt sie in der Summenzeile."* **Dritte Berichtigung derselben Zahl in vier Tagen; eine Zahl, die bei jeder Aufgabe altert, ist keine Umgebungstatsache, sondern eine Wartungsschuld** |
| **T52.20** | **Nicht dokumentiert: `urllib3` warnt beim Import** — `NotOpenSSLWarning`, weil das System-`ssl` gegen **LibreSSL 2.8.3** gebaut ist und urllib3 v2 OpenSSL ≥ 1.1.1 verlangt. **Nur eine Warnung, kein Fehler** — aber sie steht auf jeder Importzeile und gehört in die Umgebungstabelle, **damit sie niemand für einen Befund hält** |

---

## Ergänzung zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K1u** | ⚠️ **Die Testdatei-Zahl in `UMGEBUNGEN.md` durch eine Regel ersetzen** — siehe **T52.19** |
| **K1v** | **`urllib3`/LibreSSL-Warnung in die Umgebungstabelle** — siehe **T52.20** |

---

## Ersetzung — Kettenzeile 0,85a nach dem Merge

**Zu finden** (die Zeile mit `0,85a`, die `Mac-Lauf und Merge offen` enthält):

**Zu ersetzen durch:**

```
| ~~0,85a~~ | ~~Resolver-Modus in `shared/paths.py` + zwei AST-Masse~~ | ⭐ **ERLEDIGT 18.09.** — Cloud, Mac-Lauf (22:29–23:03, Python 3.9.6) und Merge. **99 Pfade, 0 Unterschiede, auf beiden Rechnern.** Siehe Block **2k** |
```

⚠️ **Den Merge-Commit setzt die einarbeitende Sitzung selbst ein** (`git log`)
— er steht beim Schreiben dieses Nachtrags noch nicht fest.

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. ⚠️ **Reihenfolge (d) → (e) → (f).** Jeder setzt den vorigen voraus.
2. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — entfernte Zeilen nur
   aus den benannten Ersetzungen, jede zugeordnet.
3. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.
