# Backlog-Nachtrag 19.09.2026 (i) — was die Vorprüfung auf dem Mac gefunden hat

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(h) voraus.** Einzufügen als **Block 2o**, nach Block 2n.

---

### 2o — Vorprüfung vor TB-55 (19.09.2026, rein lesend, kein Code geändert)

| # | Punkt |
|---|---|
| **V1** | ⭐⭐ **EINE LEERE DOPPELGÄNGERIN IST GEFUNDEN — gemessener Einzelfall der Fehlerklasse „eigener Pfadbau".** `strategies/volatility_breakout/paper_trading_volatility_breakout.db`, **0 Bytes, 5.09.2026 21:30**; die echte liegt mit **16K** in der Wurzel (`18.09. 22:50`). ⭐ **Entstanden durch relativen Pfadaufbau:** ein Prozess mit Arbeitsordner `strategies/volatility_breakout/` öffnete die Datenbank relativ, SQLite legte eine neue an. **Null Bytes heisst: kein Schema geschrieben.** ⚠️⚠️ **Das ist die Wirkung, gegen die TB-52/TB-53 gebaut werden — und sie ist keine Vermutung mehr:** dieselbe Falle teilt die OOS-Nachweise eines Bots lautlos in zwei Dateien. ⚠️ **Nicht gelöscht, nicht verschoben, nicht repariert** — Beweismaterial |
| **V2** | ⚠️ **ES SIND ZWÖLF `*.db`, NICHT NEUN.** Neun mit Präfix **`paper_trading_`** in der Wurzel (die OOS-Nachweise) · `benachrichtigungen_schliessung.db` (32K) · `broker_testnet_t3_supertrend.db` (92K) · die 0-Byte-Doppelgängerin aus V1. ⭐ **Folge für alle künftigen Aufträge: „jede `*.db` ausserhalb `trading-env/`", gezählt und namentlich berichtet — nicht „die neun".** *Eine zu grosse Sicherung kostet Sekunden; eine zu kleine kostet die einzigen OOS-Nachweise* |
| **V3** | ⚠️ **DIE NEUN LASSEN SICH NICHT ÜBER EINE NAMENSLISTE FASSEN.** Die Benennung ist unregelmässig: `turtle_soup_crypto` / `turtle_soup_stocks` tragen ein Suffix, `t3_supertrend`, `volatility_breakout`, `elliott_wave` und `rsi2_mean_reversion` nicht. ⭐ **Tragfähiger Selektor: `paper_trading_*.db` in der Wurzel** — D5, als Regel statt als Liste. ⚠️ **Nebenbefund: die Namensschemata der neun Bots sind nicht einheitlich** — kein Eingriff, aber beim nächsten Werkzeug, das Bots über Dateinamen findet, ist das die Falle |
| **V4** | ⚠️⚠️ **AUF DEM MAC LÄUFT ETWAS.** `broker_testnet_t3_supertrend.db` geschrieben **19.09. 08:05**, `paper_trading_t3_supertrend.db` **19.09. 04:00**. ⭐ **Für `data/` folgenlos, solange nichts Kurse abruft — aber genau das muss vor dem Zug geprüft sein**, denn ein Abruf während der Sitzung verschiebt den Datenstand. ⇒ **Schritt −1 von TB-55 v3 prüft jetzt den Crontab**, mit maskierter Ausgabe (`awk` nur auf die fünf Zeitfelder, `grep -c` statt Anzeige) — ⚠️ **`crontab -l` ungefiltert ist verboten: ein Eintrag kann einen Schlüssel als `NAME=wert` tragen** |
| **V5** | ⚠️ **DREI DATENBANKEN SIND SEIT DEM 16.09. UNBERÜHRT**, während andere täglich schreiben: `paper_trading_elliott_wave.db` (16.09. 23:00) · `paper_trading_rsi2_crypto.db` (16.09. 23:20) · `paper_trading_volatility_breakout_crypto.db` (16.09. 23:50). ⭐ **Das gehört zu den stillen Ausfällen (TB-45): entweder laufen diese drei Bots nicht mehr, oder sie laufen und schreiben nichts — beides sieht von aussen gleich aus** (Prüfprinzip **A1**). ⚠️ **NICHT Teil von TB-55.** Eigene, rein lesende Aufgabe: Protokollzeile gegen Crontab-Eintrag je Bot |
| **V6** | ⭐ **Die Umgebung des Mac ist bestätigt, gemessen statt angenommen:** `uname -s` = `Darwin` · `trading-env/bin/python3` = **Python 3.9.6** · Zweig **`main`** = `origin/main` = **`7e48e1f`** · `git status --short` = **0 Zeilen**. ⭐ **Damit ist die Lage vor dem einen unwiederholbaren Zug dokumentiert** — und zwar *vor* der Sitzung, nicht in ihr |
| **V7** | ⭐⭐ **NEU ALS SOLLWERT IN TB-55 v3: der `snapshot_hash` selbst.** `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` — dreimal gerechnet (T55.2). ⚠️ **Meldet der Mac beim Ziehen etwas anderes, wird nicht gezogen.** *Bisher war die Zahl eine Vorhersage im Bericht; jetzt ist sie ein Abbruchkriterium im Auftrag* |

---

## Ergänzung zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2a** | ⚠️ **`crontab -l` wird nie ungefiltert ausgegeben.** Zulässig: `awk '{print $1,$2,$3,$4,$5}'` (nur Zeitfelder) und `grep -c` (zählt, ohne zu zeigen). ⭐ **Gehört zu den Secrets-Regeln: Existenz wird geprüft, nie der Wert** |
| **K2b** | ⭐ **Vorprüfungen gehören vor die Sitzung, nicht in sie** — wenn ihr Ergebnis eine **Betreiberentscheidung** auslösen könnte. *Ein abgebrochener Mac-Lauf kostet eine Sitzung; drei lesende Befehle kosten drei Minuten* |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte Zeilen:
   0.** Dieser Nachtrag ersetzt nichts. **Weicht es ab, ist das ein Befund.**
2. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.
