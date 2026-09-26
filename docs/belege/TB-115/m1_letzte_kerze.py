#!/usr/bin/env python3
"""TB-115 M1, Selektionspfad - kann die LETZTE Kerze einer Snapshot-Datei eine
Teilkerze sein? Rein lesend: je Kursdatei nur die Kopfzeile und die LETZTE
Zeile (Zeitstempel), dazu Datei-mtime und Manifest. Keine Kurswerte, keine
Zeilenzahlen, kein Lauf eines Bots oder Selektionsskripts.

Pruefung je Datei:
  schluss  = letzter Augenblick der letzten Kerze
             Krypto: open + Laenge - 1 ms (Binance-Lesart, wie abrufschutz)
             Aktien: sichere Schranke D 23:59:59.999 UTC (wie abrufschutz;
                     liegt nach jedem NYSE-Schluss - kein Kalender noetig)
  mtime    = Aenderungszeit der Snapshot-Kopie (snapshot.py kopiert mit
             Zeitstempel; gegengeprueft an data/ in m1_letzte_kerze.txt)
  Befund "SICHER TEILKERZE", wenn schluss >= mtime (Datei geschrieben, bevor
  die letzte Kerze vorbei war). schluss < mtime ist notwendig, nicht
  hinreichend - der Abrufzeitpunkt liegt vor dem Schreiben; deshalb zusaetzlich
  die Gleichlaeufigkeit: alle Dateien eines Intervalls enden auf derselben
  Kerze, und die drei Krypto-Intervalle vertragen EINEN gemeinsamen Stand.

Aufruf aus der Repo-Wurzel: python3 docs/belege/TB-115/m1_letzte_kerze.py
"""
import collections
import datetime as dt
import json
import os
import sys

SNAP = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
LAENGE = {"1h": dt.timedelta(hours=1), "4h": dt.timedelta(hours=4),
          "1d": dt.timedelta(days=1)}
MS = dt.timedelta(milliseconds=1)


def letzte_zeile(pfad):
    with open(pfad, "rb") as d:
        kopf = d.readline().decode().strip()
        d.seek(0, os.SEEK_END)
        pos = d.tell() - 1
        while pos > 0:
            d.seek(pos)
            if d.read(1) == b"\n" and pos != d.seek(0, os.SEEK_END) - 1:
                break
            pos -= 1
        d.seek(pos + 1)
        return kopf, d.read().decode().strip().split(",")[0]


def main():
    m = json.load(open(os.path.join(SNAP, "MANIFEST.json")))
    snap_zeit = dt.datetime.fromisoformat(m["zeitpunkt_utc"]).replace(tzinfo=None)
    kurs = sorted(n for n, e in m["dateien"].items() if e["art"] == "Kursdatei")
    print(f"# TB-115 M1 Selektion - letzte Kerze je Snapshot-Kursdatei")
    print(f"Snapshot {SNAP.split('/')[1][:16]}..., gezogen {m['zeitpunkt_utc']}, "
          f"Kursdateien laut Manifest {m['kursdateien']}, gezaehlt {len(kurs)}")
    gruppen = collections.defaultdict(list)
    befunde, koepfe = [], collections.Counter()
    for name in kurs:
        pfad = os.path.join(SNAP, name)
        symbol, intervall = name[:-4].rsplit("_", 1)
        markt = "krypto" if symbol.endswith("USDT") else "aktien"
        kopf, letzte = letzte_zeile(pfad)
        koepfe[kopf] += 1
        oeffnung = dt.datetime.fromisoformat(letzte)
        schluss = oeffnung + LAENGE[intervall] - MS
        mtime = dt.datetime.utcfromtimestamp(os.stat(pfad).st_mtime)
        mtime_data = None
        if os.path.exists(os.path.join("data", name)):
            mtime_data = dt.datetime.utcfromtimestamp(
                os.stat(os.path.join("data", name)).st_mtime)
        gruppen[(markt, intervall)].append((name, oeffnung, schluss, mtime,
                                            mtime_data))
        if schluss >= mtime:
            befunde.append(name)
    print(f"\n## Spaltenkoepfe (Anzahl Dateien je Kopfzeile)")
    for kopf, n in koepfe.items():
        print(f"  {n:>4}  {kopf}")
    print(f"\n## je Markt und Intervall")
    for (markt, intervall), liste in sorted(gruppen.items()):
        letzte = collections.Counter(str(o) for _n, o, _s, _m, _d in liste)
        mt = sorted(m_ for _n, _o, _s, m_, _d in liste)
        gleich_data = sum(1 for *_x, m_, d_ in liste if d_ is not None
                          and abs((m_ - d_).total_seconds()) < 1)
        abstand = min(m_ - s for _n, _o, s, m_, _d in liste)
        print(f"  {markt:<6} {intervall}: {len(liste):>3} Dateien; letzte Kerze "
              f"(open_time): {dict(letzte)}")
        print(f"         mtime (UTC) {mt[0]:%Y-%m-%d %H:%M:%S} .. "
              f"{mt[-1]:%Y-%m-%d %H:%M:%S}; mtime gleich data/: "
              f"{gleich_data}/{len(liste)}; kleinster Abstand mtime - Schluss "
              f"der letzten Kerze: {abstand}")
    # gemeinsamer Stand der Krypto-Intervalle: die letzte Kerze muss vor dem
    # Stand geendet haben, die naechste darf es noch nicht.
    def stand(ohne=()):
        unten, oben = dt.datetime.min, dt.datetime.max
        for (markt, intervall), liste in gruppen.items():
            if markt != "krypto":
                continue
            for n, o, s, _m, _d in liste:
                if n in ohne:
                    continue
                unten = max(unten, s + MS)                    # Stand > Schluss
                oben = min(oben, o + 2 * LAENGE[intervall] - MS)  # naechste lief noch
        return unten, oben
    for titel, ohne in (("alle Krypto-Dateien", ()),
                        ("ohne die Dateien mit SICHER TEILKERZE", tuple(befunde))):
        unten, oben = stand(ohne)
        print(f"\n## gemeinsamer Stand, {titel}: [{unten} , {oben}] UTC -> "
              f"{'vertraeglich' if unten <= oben else 'NICHT vertraeglich'}")
    print(f"\n## SICHER TEILKERZE (Schluss der letzten Kerze >= mtime): "
          f"{len(befunde)} {befunde[:10]}")
    for n in befunde:
        for liste in gruppen.values():
            for n2, o, s, m_, _d in liste:
                if n2 == n:
                    print(f"   {n}: letzte Kerze {o}, Schluss {s}, geschrieben "
                          f"(mtime) {m_} - {s - m_} VOR dem Kerzenschluss")
    print(f"## Snapshot-Zeitpunkt minus spaetester Schluss: "
          f"{snap_zeit - max(s for l in gruppen.values() for _n, _o, s, _m, _d in l)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
