"""
Alternative zur Wurzelkorrektur: reicht der Cronjob-Zeitpunkt aus?
======================================================================
Rechnet fuer jeden US-Handelstag der letzten Jahre aus, wann der
Boersenschluss (16:00 America/New_York) in Berliner Zeit und in UTC lag,
und wie viel Vorlauf verschiedene Cron-Zeitpunkte davor oder danach haben.

Hintergrund: Europa und die USA stellen die Uhr an unterschiedlichen
Terminen um. In den Zwischenzeiten verschiebt sich der Boersenschluss in
Berliner Zeit um eine Stunde - eine Cron-Zeit, die elf Monate im Jahr
sicher nach Schluss liegt, kann in diesen Wochen davor liegen. Genau
solche Wochen sind der Kandidat fuer einen "manchmal unvollstaendigen"
letzten Balken.

Rein rechnerisch, keine Netzabfrage, keine Datei ausserhalb dieses
Verzeichnisses. Feiertage sind NICHT beruecksichtigt (sie verschieben den
Schluss nicht, sie lassen den Tag ganz ausfallen); der Handelsschluss um
13:00 an halben Handelstagen ebenfalls nicht - beides macht den Vorlauf
groesser, nie kleiner, die Rechnung ist also die konservative Seite.

Nutzung:  python3 cron_zeitfenster.py
"""

import json
import os
from collections import Counter
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(DIR, "results")

NEW_YORK = ZoneInfo("America/New_York")
BERLIN = ZoneInfo("Europe/Berlin")
UTC = ZoneInfo("UTC")

SCHLUSS = time(16, 0)          # regulaerer US-Boersenschluss
VON = datetime(2023, 9, 1)
BIS = datetime(2026, 9, 1)

# Kandidaten: (Beschriftung, Stunde, Minute, Zeitzone des Cron-Eintraegs)
KANDIDATEN = [
    ("22:00 Berliner Zeit (Protokoll: 'werktags 22 Uhr')", 22, 0, BERLIN),
    ("22:05 Berliner Zeit", 22, 5, BERLIN),
    ("22:30 Berliner Zeit", 22, 30, BERLIN),
    ("23:00 Berliner Zeit", 23, 0, BERLIN),
    ("23:30 Berliner Zeit", 23, 30, BERLIN),
    ("22:05 UTC", 22, 5, UTC),
]


def handelstage():
    tag = VON
    while tag <= BIS:
        if tag.weekday() < 5:
            yield tag.date()
        tag += timedelta(days=1)


def schluss_utc(datum):
    return datetime.combine(datum, SCHLUSS, tzinfo=NEW_YORK).astimezone(UTC)


def auswerten():
    tage = list(handelstage())
    schluss_in_berlin = Counter()
    schluss_in_utc = Counter()

    for d in tage:
        ende = schluss_utc(d)
        schluss_in_berlin[ende.astimezone(BERLIN).strftime("%H:%M")] += 1
        schluss_in_utc[ende.strftime("%H:%M")] += 1

    kandidaten = []
    for label, stunde, minute, zone in KANDIDATEN:
        vorlauf = []
        for d in tage:
            lauf = datetime.combine(d, time(stunde, minute), tzinfo=zone).astimezone(UTC)
            vorlauf.append((lauf - schluss_utc(d)).total_seconds() / 60)
        vor_schluss = [v for v in vorlauf if v < 0]
        knapp = [v for v in vorlauf if 0 <= v < 30]
        kandidaten.append({
            "cron": label,
            "tage": len(tage),
            "minimaler_abstand_min": round(min(vorlauf)),
            "maximaler_abstand_min": round(max(vorlauf)),
            "tage_vor_boersenschluss": len(vor_schluss),
            "tage_unter_30_min_nach_schluss": len(knapp),
        })

    return {"zeitraum": f"{VON.date()} bis {BIS.date()}", "handelstage": len(tage),
            "schluss_in_berliner_zeit": dict(schluss_in_berlin),
            "schluss_in_utc": dict(schluss_in_utc),
            "kandidaten": kandidaten}


if __name__ == "__main__":
    e = auswerten()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "cron_zeitfenster.json"), "w") as fh:
        json.dump(e, fh, indent=1, ensure_ascii=False)

    print(f"US-Boersenschluss (16:00 New York) im Zeitraum {e['zeitraum']}, "
          f"{e['handelstage']} Wochentage\n")
    print("In Berliner Zeit:")
    for uhrzeit, n in sorted(e["schluss_in_berliner_zeit"].items()):
        print(f"  {uhrzeit} Uhr an {n} Tagen ({n / e['handelstage'] * 100:.1f} %)")
    print("In UTC:")
    for uhrzeit, n in sorted(e["schluss_in_utc"].items()):
        print(f"  {uhrzeit} an {n} Tagen ({n / e['handelstage'] * 100:.1f} %)")

    print(f"\n{'Cron-Zeitpunkt':52} {'Abstand min':>12} {'max':>7} "
          f"{'VOR Schluss':>12} {'<30 min':>9}")
    print("-" * 96)
    for k in e["kandidaten"]:
        print(f"{k['cron']:52} {k['minimaler_abstand_min']:>10} m "
              f"{k['maximaler_abstand_min']:>5} m {k['tage_vor_boersenschluss']:>12} "
              f"{k['tage_unter_30_min_nach_schluss']:>9}")
    print("\nNegativer Abstand = der Cronjob laeuft, waehrend die Boerse noch offen ist.")
