"""
Sanity-Checks der Untersuchung
===================================
Ohne Test-Framework, wie in allen Untersuchungen dieses Projekts.

Prueft die drei Stellen, an denen diese Untersuchung falsch liegen koennte:
die nachgebildeten Signalbedingungen, die Zeitzonen-Rechnung und die
Aussage, dass die Menge der Signal-Balken durch die Wurzelkorrektur nicht
kleiner wird.

Nutzung:  python3 test_wurzelkorrektur.py
"""

import os
import sys
from datetime import datetime, time
from zoneinfo import ZoneInfo

import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

import cron_zeitfenster as cz
import datenlage as dl

BESTANDEN = FEHLER = 0


def check(label, bedingung, detail=""):
    global BESTANDEN, FEHLER
    if bedingung:
        BESTANDEN += 1
        print(f"  OK    {label}")
    else:
        FEHLER += 1
        print(f"  FEHLER {label}   {detail}")


# ---------------------------------------------------------------------------
print("\n1) Zeitzonen-Rechnung")
# ---------------------------------------------------------------------------
# Sommer: USA und Europa beide in der Sommerzeit -> 6 Stunden Versatz.
juli = cz.schluss_utc(datetime(2026, 7, 15).date())
check("16:00 New York im Juli sind 20:00 UTC", juli.strftime("%H:%M") == "20:00",
      juli.isoformat())
check("und 22:00 Berliner Zeit",
      juli.astimezone(cz.BERLIN).strftime("%H:%M") == "22:00")

# Winter: beide in der Normalzeit -> weiterhin 6 Stunden Versatz, aber 21:00 UTC.
januar = cz.schluss_utc(datetime(2026, 1, 15).date())
check("16:00 New York im Januar sind 21:00 UTC", januar.strftime("%H:%M") == "21:00")
check("und ebenfalls 22:00 Berliner Zeit",
      januar.astimezone(cz.BERLIN).strftime("%H:%M") == "22:00")

# Uebergangsfenster: USA hat umgestellt, Europa noch nicht (Mitte Maerz).
maerz = cz.schluss_utc(datetime(2026, 3, 12).date())
check("im Maerz-Uebergangsfenster liegt der Schluss eine Stunde frueher (21:00 Berlin)",
      maerz.astimezone(cz.BERLIN).strftime("%H:%M") == "21:00",
      maerz.astimezone(cz.BERLIN).isoformat())

e = cz.auswerten()
check("ueber den ganzen Zeitraum kommen nur zwei Berliner Uhrzeiten vor",
      set(e["schluss_in_berliner_zeit"]) == {"21:00", "22:00"},
      str(e["schluss_in_berliner_zeit"]))
kandidat = {k["cron"]: k for k in e["kandidaten"]}
check("ein Cronjob um 22:00 Berliner Zeit laeuft an keinem Tag VOR Boersenschluss",
      kandidat["22:00 Berliner Zeit (Protokoll: 'werktags 22 Uhr')"]["tage_vor_boersenschluss"] == 0)
check("hat aber an der Mehrzahl der Tage weniger als 30 Minuten Abstand",
      kandidat["22:00 Berliner Zeit (Protokoll: 'werktags 22 Uhr')"]["tage_unter_30_min_nach_schluss"] > 700)
check("ab 22:30 Berliner Zeit hat kein Tag mehr weniger als 30 Minuten Abstand",
      kandidat["22:30 Berliner Zeit"]["tage_unter_30_min_nach_schluss"] == 0)

# ---------------------------------------------------------------------------
print("\n2) Datenlage")
# ---------------------------------------------------------------------------
d = dl.auswerten()
check("genau ein Balken mit fehlenden Preisen ueber alle Aktien-Dateien",
      len(d["luecken"]) == 1, str(d["luecken"]))
check("und das ist der bekannte APH-Fall",
      d["luecken"][0]["symbol"] == "APH" and d["luecken"][0]["datum"] == "2026-09-01",
      str(d["luecken"][0]))
check("bei diesem Balken fehlen ALLE vier Preise, das Volumen ist aber da",
      d["luecken"][0]["alle_preise_fehlen"] and d["luecken"][0]["volumen"] > 0)
v = d["volumen_des_letzten_balkens_zum_median_der_vortage"]
check("das Volumen der letzten Balken liegt im ueblichen Bereich (Median nahe 1)",
      0.9 < v["median"] < 1.2, str(v["median"]))
check("kein einziges Symbol zeigt ein Teiltagesvolumen unter der Haelfte",
      v["anteil_unter_0_5"] == 0.0, str(v["anteil_unter_0_5"]))

# ---------------------------------------------------------------------------
print("\n3) Nachgebildete Signalbedingungen")
# ---------------------------------------------------------------------------
# Die Bedingungen werden hier gegen von Hand gerechnete Miniatur-Faelle
# geprueft, nicht gegen sich selbst.
import signalverschiebung as sv

rahmen = pd.DataFrame({
    "open_time": pd.date_range("2026-01-01", periods=4),
    "close": [100.0, 100.0, 100.0, 100.0],
    "sma_trend": [90.0, 110.0, 90.0, float("nan")],
    "rsi": [3.0, 3.0, 9.0, 3.0],
})
maske = sv.signal_maske
# forward_test.py des Bots importieren, um die ECHTE Signalschwelle zu lesen -
# der Test soll nicht gegen eine hier abgetippte Zahl pruefen. Die
# Netzwerk-Module werden dabei durch Stubs ersetzt (dieselbe Vorkehrung wie
# in signalverschiebung.py).
sv._stubs_setzen()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(DIR)), "shared"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(DIR)), "strategies",
                                 "rsi2_mean_reversion"))
import forward_test as ft_rsi2
ergebnis = list(maske("rsi2_mean_reversion", rahmen))
check("RSI-2: Kurs ueber SMA und RSI unter der Schwelle ergibt ein Signal",
      ergebnis[0] is True or ergebnis[0] == True, str(ergebnis))
check("RSI-2: Kurs UNTER dem Trendfilter ergibt kein Signal", not ergebnis[1])
check(f"RSI-2: RSI ueber der Schwelle ({ft_rsi2.RSI_THRESHOLD}) ergibt kein Signal",
      not ergebnis[2])
check("RSI-2: fehlender Indikatorwert ergibt kein Signal", not ergebnis[3])

turtle = pd.DataFrame({
    "open_time": pd.date_range("2026-01-01", periods=3),
    # Zeile 2 war im ersten Entwurf 95.0 - das UNTERSCHREITET das
    # Donchian-Tief von 100 und war damit sehr wohl ein Setup. Der Test hat
    # den Fehler in der eigenen Vorgabe gefunden, nicht in der Bedingung.
    "low": [90.0, 101.0, 90.0],
    "close": [101.0, 101.0, 99.0],
    "donchian_low": [100.0, 100.0, 100.0],
})
ergebnis = list(maske("turtle_soup_stocks", turtle))
check("Turtle Soup: Tief unter dem Donchian-Tief und Schluss darueber ergibt ein Signal",
      ergebnis[0])
check("Turtle Soup: ohne Unterschreitung des Tiefs kein Signal", not ergebnis[1])
check("Turtle Soup: ohne Rueckeroberung des Schlusskurses kein Signal", not ergebnis[2])

breakout = pd.DataFrame({
    "open_time": pd.date_range("2026-01-01", periods=4),
    "close": [100.0, 105.0, 105.0, 105.0],
    "bb_upper": [104.0, 104.0, 104.0, 104.0],
    "is_squeeze": [True, True, False, True],
})
ergebnis = list(maske("volatility_breakout", breakout))
check("Breakout: Squeeze am Vortag und Ausbruch heute ergibt ein Signal", ergebnis[1])
check("Breakout: ohne Squeeze am Vortag kein Signal", not ergebnis[3])
check("Breakout: der erste Balken hat keinen Vortag und kann kein Signal sein",
      not ergebnis[0])

# ---------------------------------------------------------------------------
print("\n4) Die zentrale Behauptung: kein Signal geht verloren")
# ---------------------------------------------------------------------------
# Die Wurzelkorrektur prueft an Tag D den Balken D-1 statt D. Ueber die
# gesamte Historie wird damit jeder Balken weiterhin genau einmal geprueft -
# die MENGE der Signalbalken ist identisch, nur der Handelstag verschiebt
# sich. Das wird hier an einer Reihe mit bekannten Signalen nachgerechnet.
lang = pd.DataFrame({
    "open_time": pd.date_range("2026-01-01", periods=10),
    "close": [100.0] * 10,
    "sma_trend": [90.0] * 10,
    "rsi": [3.0, 9.0, 3.0, 9.0, 3.0, 9.0, 3.0, 9.0, 3.0, 9.0],
})
heute = maske("rsi2_mean_reversion", lang)
mit_korrektur = heute.shift(1).fillna(False)   # an Tag D wird Balken D-1 geprueft
check("gleich viele Signalbalken in beiden Varianten (nur um einen Tag versetzt)",
      int(heute.sum()) == int(mit_korrektur.sum()) + int(bool(heute.iloc[-1])),
      f"heute {int(heute.sum())}, verschoben {int(mit_korrektur.sum())}")

print("\n" + "=" * 60)
print(f"{BESTANDEN} Checks bestanden, {FEHLER} fehlgeschlagen.")
print("=" * 60)
if FEHLER:
    raise SystemExit(1)
