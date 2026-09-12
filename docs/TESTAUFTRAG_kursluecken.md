# Testauftrag: Kurslücken im Trade-Pfad

**Für eine lokale Claude-Code-Sitzung auf dem Mac.**

Geprüfter Stand: Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`94e0d7f`, nach Merge von #80), **PR #81**.

> ## Was diese Sitzung darf
>
> **Alle Schritte laufen ohne Rückfragen durch.** Diese Änderung fasst keine
> Bot-Datenbank an, löst keinen Trade aus und verändert keine Kursdatei.
>
> **Nicht anfassen:** `live_params.py`, `forward_test.py`,
> `equity_simulation.py`, alles unter `broker/`, Crontab, launchd-Vorlagen,
> die Dateien unter `data/`. Kein `--echt` irgendwo.
>
> Schritt 4 lädt **keine** Daten aus dem Netz — `fetch_stock_data.py` wird
> nicht als Programm gestartet, nur seine Funktion mit einer Attrappe geprüft.

---

## Schritt 0 — Umgebung

```bash
cd ~/trading-bot
git status --short              # muss LEER sein
git rev-parse --abbrev-ref HEAD
python3 -c "import pandas; print('pandas', pandas.__version__)"
```

---

## Schritt 1 — Selbsttests

```bash
python3 shared/test_kursdaten.py | tail -3
```

Erwartet: **83 von 83 Prüfungen bestanden.**

Der Lauf dauert einige Minuten: mehrere Abschnitte starten echte Bot-Loader in
eigenen Prozessen (nötig, weil neun Bots gleichnamige Module haben) und lassen
sie über 147 Aktien-Symbole laufen.

```bash
git status --short              # nach dem Testlauf wieder LEER
```

Ist die Arbeitskopie nicht leer, ist das ein Befund — kein Test dieser
Änderung darf eine Datei verändern.

---

## Schritt 2 — Den Befund selbst sehen

```bash
python3 shared/kursdaten.py
echo "Rueckgabewert: $?"
```

Erwartet auf **diesem** Datenstand:

```
Geprueft: 242 Datei(en) in /Users/…/trading-bot/data

1 Datei(en) mit Befund:
  APH_1d.csv             1 von 8764 Kerze(n)  <- betrifft die LETZTE Kerze
      2026-09-01
```

Rückgabewert **1** — ein Befund soll in einem Cronjob-Log auffallen.

**Bitte die Ausgabe vollständig zurückmelden.** Auf dem Mac können die
Kursdaten neuer sein als in der Cloud-Sitzung; kommen dort **mehr** betroffene
Symbole heraus, ist das die interessanteste Zahl dieses Auftrags — dann ist
`APH` kein Einzelfall, sondern ein Muster.

```bash
tail -3 data/APH_1d.csv          # die leere Zeile ist absichtlich noch da
```

---

## Schritt 3 — Der Ist-Zustand ohne Absicherung

Zeigt, was der Befund tatsächlich anrichtet. Verändert nichts.

```bash
cd ~/trading-bot/strategies/elliott_wave_stocks
python3 - <<'PY'
import pandas as pd, multi_symbol_optimise as mso, backtest_elliott as be
import equity_simulation as es

# Absicherung ausschalten = Zustand VOR dieser Aenderung
mso.entferne_unvollstaendige = lambda df, symbol=None, melden=True: (df, 0)
daten = mso.load_all_symbol_data()
aph = daten["APH"]
print("letzte Kerze:", aph["open_time"].max().date(),
      "| NaN in Kursen:", aph[["open","high","low","close"]].isna().any().any())

be.STOP_LOSS_PCT = 16.0
t = mso.get_trades_for_symbol(aph, 6.0, False)
t["symbol"] = "APH"
print(t[["entry_time","exit_time","exit_price","result","pnl_pct"]].to_string(index=False))
erg = es.simulate_portfolio(t, 10_000.0, 0.10, None)
print("Endkapital:", erg["final_capital"], " <- nan erwartet")
PY
cd ~/trading-bot
```

Erwartet: letzte Kerze `2026-09-01`, ein Trade mit `exit_price` und `pnl_pct`
leer, **Endkapital `nan`**.

Dann dasselbe **mit** Absicherung (also ohne die erste Zeile):

```bash
cd ~/trading-bot/strategies/elliott_wave_stocks
python3 - <<'PY'
import pandas as pd, multi_symbol_optimise as mso, backtest_elliott as be
import equity_simulation as es
daten = mso.load_all_symbol_data()          # meldet die Streichung
aph = daten["APH"]
print("letzte Kerze:", aph["open_time"].max().date(),
      "| NaN in Kursen:", aph[["open","high","low","close"]].isna().any().any())
be.STOP_LOSS_PCT = 16.0
t = mso.get_trades_for_symbol(aph, 6.0, False); t["symbol"] = "APH"
print(t[["entry_time","exit_time","exit_price","result","pnl_pct"]].to_string(index=False))
print("Endkapital:", es.simulate_portfolio(t, 10_000.0, 0.10, None)["final_capital"])
PY
cd ~/trading-bot
```

Erwartet: letzte Kerze `2026-08-31`, kein NaN, **Endkapital ≈ 10.868,40**, und
in der Ausgabe die Zeile

```
Datenqualitaet: insgesamt 1 unvollstaendige Kerze(n) in 1 Symbol(en) gestrichen - APH (1).
```

**Bleibt diese Zeile aus, ist das ein Befund** — Streichen ohne Meldung ist
genau der Zustand, den diese Änderung beseitigt.

---

## Schritt 4 — Ändert sich eine Live-Kennzahl? (der wichtigste Schritt)

```bash
cd ~/trading-bot/strategies/elliott_wave_stocks
python3 - <<'PY'
import pandas as pd, multi_symbol_optimise as mso, backtest_elliott as be
import equity_simulation as es, live_params, kursdaten

def lade(absichern):
    if not absichern:
        mso.entferne_unvollstaendige = lambda df, symbol=None, melden=True: (df, 0)
    else:
        mso.entferne_unvollstaendige = kursdaten.entferne_unvollstaendige
    return mso.load_all_symbol_data()

def kennzahlen(daten, dev, stop, tp=True):
    be.STOP_LOSS_PCT = stop
    teile = []
    for s, d in daten.items():
        t = mso.get_trades_for_symbol(d, dev, tp)
        if not t.empty:
            t = t.copy(); t["symbol"] = s; teile.append(t)
    c = pd.concat(teile, ignore_index=True)
    erg = es.simulate_portfolio(c.sort_values("entry_time"), 10_000.0, 0.10, None)
    return {"Trades": len(c), "NaN": int(c["pnl_pct"].isna().sum()),
            "win_rate": round((c["pnl_pct"] > 0).mean()*100, 2),
            "avg": round(c["pnl_pct"].mean(), 4),
            "summe": round(c["pnl_pct"].sum(), 2),
            "Endkapital": erg["final_capital"]}

roh, sauber = lade(False), lade(True)
for titel, dev, stop, tp in (("LIVE", live_params.DEVIATION_PCT, live_params.STOP_LOSS_PCT, True),
                              ("Befund 6,0/16,0 ohne Ziel", 6.0, 16.0, False)):
    a, b = kennzahlen(roh, dev, stop, tp), kennzahlen(sauber, dev, stop, tp)
    print(f"\n{titel}")
    for k in a:
        print(f"  {k:12} {str(a[k]):>14} -> {str(b[k]):>14}"
              f"{'' if a[k]==b[k] else '   ANDERS'}")
PY
cd ~/trading-bot
```

Erwartet:

| | vorher | nachher |
|---|---|---|
| **LIVE**: Trades / win_rate / Endkapital | 510 / 31,57 / 17.197,86 | **identisch** |
| Befund: Endkapital | `nan` | 59.939,87 |
| Befund: win_rate | 55,08 | 55,35 |

**Weicht die LIVE-Zeile ab, ist das die wichtigste Rückmeldung des ganzen
Auftrags** — dann ändert sich eine Zahl, auf deren Grundlage der Bot aktiviert
wurde. Der Lauf dauert einige Minuten (zweimal 147 Symbole).

---

## Schritt 5 — Alle neun Loader laufen weiterhin

```bash
for bot in elliott_wave elliott_wave_stocks rsi2_crypto rsi2_mean_reversion \
           t3_supertrend turtle_soup_crypto turtle_soup_stocks \
           volatility_breakout volatility_breakout_crypto; do
  printf "%-28s " "$bot"
  (cd strategies/$bot && python3 -c "
import sys, os; sys.path.insert(0, os.getcwd())
import multi_symbol_optimise as mso
d = mso.load_all_symbol_data()
print('OK', len(d), 'Symbole')" 2>&1 | grep -E "^OK|Error" | tail -1)
done
```

Erwartet: **neun Mal `OK`**. In der Cloud-Sitzung scheiterten `elliott_wave`
und `t3_supertrend` an einem fehlenden `binance`-Paket — auf dem Mac ist es
installiert, dort müssen alle neun laufen. Tun sie es nicht, bitte den Fehler
wörtlich melden.

---

## Schritt 6 — Mutationsproben

Baut 14 plausible Fehler ein und prüft, dass der Selbsttest jeden erkennt. Der
Urzustand wird in jedem Fall wiederhergestellt. Dauer: 30–60 Minuten, weil jede
Mutation die ganze Suite mit echten Bot-Läufen durchlaufen lässt.

```bash
cat > /tmp/mut_kursdaten.py <<'PY'
"""Mutationsproben der Kurslücken-Absicherung."""
import subprocess, sys

TEST = "shared/test_kursdaten.py"
K = "shared/kursdaten.py"
L = "strategies/elliott_wave_stocks/multi_symbol_optimise.py"
H = "strategies/elliott_wave_stocks/fetch_stock_data.py"

MUTATIONEN = [
    (K, "M1  nur 'close' wird geprueft - fehlendes 'open' rutscht durch",
     'KURSSPALTEN = ["open", "high", "low", "close"]',
     'KURSSPALTEN = ["close"]'),

    (K, "M2  Volumen zaehlt mit - vollstaendige Kerzen wuerden gestrichen",
     'KURSSPALTEN = ["open", "high", "low", "close"]',
     'KURSSPALTEN = ["open", "high", "low", "close", "volume"]'),

    (K, "M3  gestrichen wird, aber nicht gezaehlt",
     '    bereinigt = df[~maske].reset_index(drop=True)',
     '    bereinigt = df[~maske].reset_index(drop=True)\n    anzahl = 0'),

    (K, "M4  Index wird nicht neu durchnummeriert",
     '    bereinigt = df[~maske].reset_index(drop=True)',
     '    bereinigt = df[~maske]'),

    (K, "M5  der Zaehler meldet nie etwas",
     '    def bericht(self):\n        if not self.je_symbol:\n            return None',
     '    def bericht(self):\n        if True:\n            return None'),

    (K, "M6  der Bericht nennt die Symbole nicht",
     '        teile = ", ".join(f"{s} ({n})" for s, n in sorted(self.je_symbol.items()))',
     '        teile = "einige"'),

    (K, "M7  der Bericht verschweigt, dass die Kerzen in keine Kennzahl eingehen",
     '                f"{teile}. Diese Kerzen gehen in KEINE Kennzahl ein.")',
     '                f"{teile}.")'),

    (K, "M8  das Werkzeug meldet Befunde mit Rueckgabewert 0",
     '    # Rueckgabewert 1: ein Befund ist kein Fehler des Programms, aber etwas,\n'
     '    # das ein Cronjob-Aufruf sichtbar machen soll.\n    return 1',
     '    return 0'),

    (K, "M9  das Werkzeug meldet nie die letzte Kerze",
     '                "letzte_betroffen": bool(maske.iloc[-1]),',
     '                "letzte_betroffen": False,'),

    (L, "M10 der Lader verwirft das Ergebnis der Absicherung",
     '            df, _gestrichen = entferne_unvollstaendige(df, symbol=symbol,\n'
     '                                                        melden=False)',
     '            _, _gestrichen = entferne_unvollstaendige(df, symbol=symbol,\n'
     '                                                        melden=False)'),

    (L, "M11 der Lader meldet die Gesamtzahl nicht",
     '    _luecken.melde()\n    return data',
     '    return data'),

    (L, "M12 die Absicherung greift erst NACH dem Zeitraumfilter",
     '            df, _gestrichen = entferne_unvollstaendige(df, symbol=symbol,\n'
     '                                                        melden=False)\n'
     '            _luecken.erfasse(symbol, _gestrichen)',
     '            _gestrichen = 0\n            _luecken.erfasse(symbol, _gestrichen)'),

    (H, "M13 der Holer filtert nicht - der Live-Pfad bleibt offen",
     '    df, _gestrichen = entferne_unvollstaendige(df, symbol=ticker)\n'
     '    return df.reset_index(drop=True)',
     '    return df.reset_index(drop=True)'),

    (H, "M14 der Holer filtert, verwirft aber das Ergebnis",
     '    df, _gestrichen = entferne_unvollstaendige(df, symbol=ticker)\n'
     '    return df.reset_index(drop=True)',
     '    _unbenutzt, _gestrichen = entferne_unvollstaendige(df, symbol=ticker)\n'
     '    return df.reset_index(drop=True)'),
]


def main():
    dateien = {K, L, H}
    urzustand = {d: open(d, encoding="utf-8").read() for d in dateien}
    erkannt, entgangen = [], []
    try:
        for datei, name, alt, neu in MUTATIONEN:
            if urzustand[datei].count(alt) != 1:
                entgangen.append(f"{name} (Vorlage {urzustand[datei].count(alt)}x)")
                print(f"[?        ] {name}: Vorlage nicht eindeutig")
                continue
            open(datei, "w", encoding="utf-8").write(urzustand[datei].replace(alt, neu))
            lauf = subprocess.run([sys.executable, TEST], capture_output=True,
                                  text=True, timeout=2400)
            open(datei, "w", encoding="utf-8").write(urzustand[datei])
            if lauf.returncode != 0:
                erkannt.append(name)
                print(f"[erkannt  ] {name}")
                for z in [z for z in lauf.stdout.splitlines() if "[FEHLER]" in z][:2]:
                    print(f"            {z.strip()[:140]}")
            else:
                entgangen.append(name)
                print(f"[ENTGANGEN] {name}")
    finally:
        for datei, inhalt in urzustand.items():
            open(datei, "w", encoding="utf-8").write(inhalt)

    print(f"\n{len(erkannt)} von {len(MUTATIONEN)} Mutationen erkannt.")
    for n in entgangen:
        print(f"  NICHT erkannt: {n}")
    return 1 if entgangen else 0


if __name__ == "__main__":
    sys.exit(main())
PY
python3 /tmp/mut_kursdaten.py
git status --short              # muss wieder LEER sein
```

Erwartet: **14 von 14 erkannt.**

M13 und M14 sind die interessanten: beide entfernen die Absicherung aus dem
Holer, M14 lässt den Aufruf aber stehen und verwirft nur sein Ergebnis. Eine
Textsuche hätte M14 durchgelassen — erkannt wird sie ausschliesslich von der
Verhaltensprüfung mit der yfinance-Attrappe.

---

## Schritt 7 — Keine Regression

```bash
python3 dashboard/test_dashboard.py            | tail -1
python3 dashboard/test_portfolio_sicht.py      | tail -2
python3 notifications/test_schliess_benachrichtigung.py | tail -2
python3 system/test_log_rotation.py            | tail -2
python3 broker/test_broker.py                  | tail -1
python3 broker/test_ibkr.py                    | tail -1
python3 shared/test_empfehlung_format.py       | tail -1
python3 system/test_caffeinate_plist.py        | tail -1
python3 notifications/test_manual_close.py     | tail -1
```

| Suite | Erwartet |
|---|---|
| `dashboard/test_dashboard.py` | 784/784 (780 ohne `node`) |
| `dashboard/test_portfolio_sicht.py` | 90 von 90 (23 ohne `node`) |
| `notifications/test_schliess_benachrichtigung.py` | 99 von 99 |
| `system/test_log_rotation.py` | 117 von 117 |
| `broker/test_broker.py` · `test_ibkr.py` | 163 · 200 |
| `shared/test_empfehlung_format.py` | 70/70 |
| `system/test_caffeinate_plist.py` | 52 von 52 |
| `notifications/test_manual_close.py` | alle bestanden |

---

## Rückmeldung

1. Zahlen aus Schritt 1 (erwartet 83/83) und Schritt 6 (14/14).
2. **Aus Schritt 2: die vollständige Ausgabe.** Sind auf dem Mac mehr Symbole
   betroffen als das eine hier?
3. Aus Schritt 3: beide Endkapital-Werte (`nan` → Zahl) und ob die
   Datenqualitäts-Zeile erschien.
4. **Aus Schritt 4: die LIVE-Zeile.** Identisch oder nicht — das ist die
   wichtigste Einzelaussage.
5. Aus Schritt 5: ob alle neun Loader liefen.
6. Jede entgangene Mutation, wörtlich.
