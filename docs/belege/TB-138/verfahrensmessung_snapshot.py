#!/usr/bin/env python3
"""TB-138 Verfahrensmessung am Snapshot, nur lesend.

  m1  Bedingung aus R66 (b) fuer den Kalender "NYSE", je Aktien-Bot
      (R74 (e); Register 54.6 Nr. 1)
  m2  Reihenenden und Symbol-Tage Luecke (R72 (d); 53.10 Nr. 3), dazu
      doppelte open_time und Zeitanteile (53.10 Nr. 10)
  m3  Paketfassung des Kalenders gegen requirements.lock (54.6 Nr. 8, Nr. 1)

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 -B docs/belege/TB-138/verfahrensmessung_snapshot.py m1
      [--snapshot ORDNER] [--bis JJJJ-MM-TT]

Liest nur, schreibt nur nach stdout. Die Kursdateien werden als Text gelesen;
`close` wird nur darauf geprueft, ob es nach Lesart L5 fehlt, und nie in eine
Zahl gewandelt (Sichtschutz, Register 27.1). Ausgegeben werden nur Tage,
Symbole, Dateinamen, Zaehlungen, Paketfassungen und Pfade.

Zeilen, die mit "FALL" beginnen, sind Einzelfaelle (Messung, Art, Symbol,
Datum); die Gegenprobe vergleicht nur diese Zeilen.

Rueckgabe: 0 gemessen ohne Befund, 1 gemessen mit Befund, 2 nicht messbar.
"""
import argparse
import csv
import datetime as dt
import importlib.metadata as md
import os
import platform
import sys
from collections import defaultdict

STANDARD_SNAPSHOT = ("snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058"
                     "eacb440653cb2ceb2")       # Lesart L1
STANDARD_BIS = "2026-08-31"                     # Lesart L3, einschliesslich
KALENDER_NAME = "NYSE"                          # R74 (a); kein anderer Name
AKTIEN_DATEI = "sp500_top150.txt"
KRYPTO_DATEI = "top25_symbols.txt"
LOCK = "requirements.lock"
# Lock-Zeilen nach Auftrag (Z. 37, 50, 51, 52; Interpreter Z. 6-7)
PAKETE = (("pandas_market_calendars", "pandas-market-calendars", 51),
          ("pandas", "pandas", 52),
          ("exchange_calendars", "exchange-calendars", 37),
          ("numpy", "numpy", 50))
# Lesart L4: 1. Januar des ersten Jahres aus Register 33.2, Spalte "erste Falte"
BOTS = (("elliott_wave_stocks", "aktien", 2017),
        ("rsi2_mean_reversion", "aktien", 2018),
        ("turtle_soup_stocks", "aktien", 2017),
        ("volatility_breakout", "aktien", 2018),
        ("elliott_wave", "krypto", 2018),
        ("t3_supertrend", "krypto", 2019),
        ("rsi2_crypto", "krypto", 2019),
        ("turtle_soup_crypto", "krypto", 2018),
        ("volatility_breakout_crypto", "krypto", 2018))
# Register Z. 1583-1586: XAUTUSDT zaehlt nicht zu den 24 Krypto-Symbolen
NICHT_BEWERTET = {"XAUTUSDT"}
MAX_SYMBOLE_JE_TAG = 20
MAX_FAELLE_JE_SYMBOL = 50

# Lesart L5: Fehlwert-Texte, wie pandas.read_csv sie liest (Standardliste).
# Die Liste der Umgebung gilt; diese hier ist nur der Rueckfall.
_NA_RUECKFALL = {"", "#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN",
                 "-nan", "1.#IND", "1.#QNAN", "<NA>", "N/A", "NA", "NULL",
                 "NaN", "None", "n/a", "nan", "null"}


def na_texte():
    try:
        from pandas._libs.parsers import STR_NA_VALUES
        return set(STR_NA_VALUES), "pandas._libs.parsers.STR_NA_VALUES"
    except Exception as e:  # noqa: BLE001
        return set(_NA_RUECKFALL), "Rueckfall im Skript (%s)" % type(e).__name__


# ---------------------------------------------------------------- Kopf

def lock_werte():
    with open(LOCK, encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    werte = {"zeilen": zeilen}
    for name, lockname, nr in PAKETE:
        z = zeilen[nr - 1] if len(zeilen) >= nr else ""
        soll = None
        if z.lower().startswith(lockname + "=="):
            soll = z.split("==", 1)[1].strip()
        werte[name] = (nr, z, soll)
    vz = zeilen[5] if len(zeilen) > 5 else ""
    vv = zeilen[6] if len(zeilen) > 6 else ""
    # Z. 6 traegt hinter der Fassung die Quelle in Klammern; gilt das erste Wort
    werte["venv"] = vz.split("interpreter_venv", 1)[1].split()[0] \
        if "interpreter_venv" in vz else None
    werte["voll"] = vv.split("interpreter_voll", 1)[1].strip() \
        if "interpreter_voll" in vv else None
    return werte


def fassung(name):
    try:
        return md.version(name)
    except Exception as e:  # noqa: BLE001
        return "nicht installiert (%s)" % type(e).__name__


def kopf(messung, snapshot):
    print("# TB-138 Verfahrensmessung %s" % messung)
    print("sys.executable   %s" % sys.executable)
    print("sys.version      %s" % " ".join(sys.version.split()))
    print("platform         %s" % platform.platform())
    ist = {}
    for name, _, _ in PAKETE:
        ist[name] = fassung(name)
        print("%-24s %s" % (name, ist[name]))
    print("snapshot         %s" % snapshot)
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(
        timespec="seconds"))
    lw = lock_werte()
    gleich = True
    for name, _, _ in PAKETE:
        nr, z, soll = lw[name]
        if soll is None or ist[name] != soll:
            gleich = False
    voll_ist = " ".join(sys.version.split())
    voll_soll = " ".join((lw["voll"] or "").split())
    venv_ist = sys.version.split()[0]
    if lw["venv"] != venv_ist or voll_soll != voll_ist:
        gleich = False
    print("Fassungen gleich Lock: %s" % ("ja" if gleich else "nein"))
    print()
    return gleich, ist, lw


# ---------------------------------------------------------------- Lesen

def universum(snapshot, datei):
    pfad = os.path.join(snapshot, "config", datei)
    with open(pfad, encoding="utf-8") as f:
        return [z.strip() for z in f if z.strip() and "#" not in z]


def lies_reihe(pfad, na):
    """Liest eine Kursdatei als Text.

    Rueckgabe: dict mit
      zeilen  Liste (open_time, tag oder None, status) mit status in
              ok | leer | natext | spalte  (spalte: Zeile ohne close-Spalte)
      fehler  None oder Grund, warum die Datei nicht lesbar ist
    """
    erg = {"zeilen": [], "fehler": None}
    with open(pfad, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        try:
            kopfzeile = next(r)
        except StopIteration:
            erg["fehler"] = "leer"
            return erg
        if "open_time" not in kopfzeile or "close" not in kopfzeile:
            erg["fehler"] = "Kopfzeile ohne open_time/close"
            return erg
        i_t = kopfzeile.index("open_time")
        i_c = kopfzeile.index("close")
        for zeile in r:
            if not zeile:
                continue
            ot = zeile[i_t] if len(zeile) > i_t else ""
            try:
                tag = dt.date.fromisoformat(ot[:10])
            except ValueError:
                tag = None
            if len(zeile) <= i_c:
                st = "spalte"
            elif zeile[i_c] == "":
                st = "leer"
            elif zeile[i_c] in na:
                st = "natext"
            else:
                st = "ok"
            erg["zeilen"].append((ot, tag, st))
    return erg


def nach_letztem_kurstag(snapshot, symbol, letzter):
    """Zeilen der _1d-Reihe nach dem letzten Kurstag: Datum und die Zahl der
    leeren Wertzellen (welche Spalten leer sind, keine Werte)."""
    aus = []
    with open(os.path.join(snapshot, symbol + "_1d.csv"), encoding="utf-8",
              newline="") as f:
        r = csv.reader(f)
        kopfzeile = next(r)
        i_t = kopfzeile.index("open_time")
        for zeile in r:
            if not zeile:
                continue
            try:
                tag = dt.date.fromisoformat(zeile[i_t][:10])
            except ValueError:
                continue
            if tag > letzter:
                leer = [k for k, v in zip(kopfzeile, zeile)
                        if k != "open_time" and v == ""]
                aus.append("%s, %d Spalten, leer: %s"
                           % (tag, len(zeile), ",".join(leer) or "-"))
    return aus


def lies_markt(snapshot, symbole, na):
    reihen = {}
    for s in symbole:
        p = os.path.join(snapshot, s + "_1d.csv")
        if os.path.isfile(p):
            reihen[s] = lies_reihe(p, na)
    return reihen


def kurstage(reihe):
    return {t for _, t, st in reihe["zeilen"] if st == "ok" and t is not None}


# ---------------------------------------------------------------- Kalender

def lade_kalender():
    try:
        import pandas_market_calendars as mcal
        return mcal.get_calendar(KALENDER_NAME), None
    except Exception as e:  # noqa: BLE001
        return None, "%s: %s" % (type(e).__name__, e)


def sitzungen(kal, von, bis):
    """Index von schedule(start_date, end_date) als Menge von Tagen (L6)."""
    plan = kal.schedule(start_date=von.isoformat(), end_date=bis.isoformat())
    return plan, {ts.date() for ts in plan.index}


def tage_zwischen(von, bis):
    n = (bis - von).days
    return {von + dt.timedelta(days=i) for i in range(n + 1)}


def jahr_ab(abw, jahre, bis):
    """Fruehestes Jahr Y, ab dem in [Y-01-01, bis] kein Tag aus abw liegt."""
    beste = None
    for y in sorted(jahre, reverse=True):
        if y > bis.year:
            continue
        if any(dt.date(y, 1, 1) <= t <= bis for t in abw):
            break
        beste = y
    return beste


# ---------------------------------------------------------------- M1

def m1(snapshot, bis, na):
    gleich, _, _ = kopf("m1", snapshot)
    if not gleich:
        print("HINWEIS: Fassungen ungleich Lock - M1 gilt nicht als Messung "
              "in der Lock-Umgebung.\n")
    symbole = universum(snapshot, AKTIEN_DATEI)
    reihen = lies_markt(snapshot, symbole, na)
    print("## Eingaben")
    print("Universumsdatei config/%s: %d Symbole, davon mit _1d-Reihe %d"
          % (AKTIEN_DATEI, len(symbole), len(reihen)))
    for s in symbole:
        if s not in reihen:
            print("FALL\tm1\tohne_1d\t%s\t-" % s)
    for s, r in reihen.items():
        if r["fehler"]:
            print("FALL\tm1\tunlesbar\t%s\t%s" % (s, r["fehler"]))
    kal, fehler = lade_kalender()
    if kal is None:
        print("\nKalender %r nicht ladbar: %s" % (KALENDER_NAME, fehler))
        print("M1 NICHT GEMESSEN")
        return 2

    ktage = {s: kurstage(r) for s, r in reihen.items()}
    je_tag = defaultdict(list)
    for s in symbole:
        for t in ktage.get(s, ()):
            je_tag[t].append(s)
    K = set(je_tag)
    if not K:
        print("Keine Kurstage - M1 NICHT GEMESSEN")
        return 2
    k_von, k_bis = min(K), max(K)
    h_bis = max(k_bis, bis)
    _, H = sitzungen(kal, k_von, h_bis)

    print("\n## Nr. 1  K (Tage mit mindestens einem Kurs, L5)")
    print("erster Tag %s, letzter Tag %s, Anzahl %d" % (k_von, k_bis, len(K)))
    print("\n## Nr. 2  H (Sitzungstage %r von %s bis %s)" % (KALENDER_NAME,
                                                             k_von, h_bis))
    print("Anzahl %d" % len(H))

    nur_h = sorted(H - K)
    nur_k = sorted(K - H)
    print("\n## Nr. 3  je Kalenderjahr")
    print("Jahr  H     K     nur_H nur_K Symbol-Tage_kein_Handelstag")
    jahre = sorted({t.year for t in H | K})
    for y in jahre:
        hy = sum(1 for t in H if t.year == y)
        ky = sum(1 for t in K if t.year == y)
        nh = sum(1 for t in nur_h if t.year == y)
        nk = sum(1 for t in nur_k if t.year == y)
        st = sum(len(je_tag[t]) for t in nur_k if t.year == y)
        print("%d  %5d %5d %5d %5d %5d" % (y, hy, ky, nh, nk, st))
    print("Summe nur_H %d, nur_K %d, Symbol-Tage an Nicht-Handelstagen %d"
          % (len(nur_h), len(nur_k), sum(len(je_tag[t]) for t in nur_k)))
    print("\nEinzelfaelle:")
    for t in nur_h:
        print("FALL\tm1\tnur_in_H\t-\t%s" % t)
    for t in nur_k:
        sy = sorted(je_tag[t])
        teil = ",".join(sy[:MAX_SYMBOLE_JE_TAG])
        if len(sy) > MAX_SYMBOLE_JE_TAG:
            teil += " (+%d weitere)" % (len(sy) - MAX_SYMBOLE_JE_TAG)
        print("FALL\tm1\tnur_in_K\t%s\t%s\t(%s, %d Symbole)"
              % (teil, t, t.strftime("%a"), len(sy)))
    abw = set(nur_h) | set(nur_k)
    ab_jahr = jahr_ab(abw, jahre, bis)
    print("Fruehestes Jahr, ab dem bis %s keine Abweichung liegt: %s"
          % (bis, ab_jahr))

    print("\n## Nr. 4  je Aktien-Bot, Zeitraum Beginn (L4) bis Ende (L3)")
    befund = False
    for bot, markt, jahr in BOTS:
        if markt != "aktien":
            continue
        von = dt.date(jahr, 1, 1)
        Hp = {t for t in H if von <= t <= bis}
        Kp = {t for t in K if von <= t <= bis}
        nh = sorted(Hp - Kp)
        nk = sorted(Kp - Hp)
        st = sum(len(je_tag[t]) for t in nk)
        erfuellt = not nh and not nk
        befund = befund or not erfuellt
        print("%s: Zeitraum %s..%s, Sitzungstage %d, nur_H %d, nur_K %d, "
              "Symbol-Tage an Nicht-Handelstagen %d"
              % (bot, von, bis, len(Hp), len(nh), len(nk), st))
        print("    erster Tag aus K %s (Beginn %s), letzter Tag aus K %s "
              "(Ende %s)" % (min(Kp) if Kp else "-", von,
                             max(Kp) if Kp else "-", bis))
        print("    erster Sitzungstag %s, letzter Sitzungstag %s"
              % (min(Hp) if Hp else "-", max(Hp) if Hp else "-"))
        print("    URTEIL R66 (b), Kalender %r: %s"
              % (KALENDER_NAME, "erfuellt" if erfuellt else "NICHT erfuellt"))
        print("    fruehestes Jahr, ab dem bis Ende erfuellt: %s" % ab_jahr)

    print("\n## Nr. 5  Zeilen, in denen close fehlt (L5)")
    na_liste, quelle = na_texte()
    print("Fehlwert-Texte (%s): %s" % (quelle, sorted(na_liste)))
    summe = defaultdict(int)
    for s in symbole:
        r = reihen.get(s)
        if not r:
            continue
        faelle = [(t, ot, st) for ot, t, st in r["zeilen"] if st != "ok"]
        if not faelle:
            continue
        z = defaultdict(int)
        for _, _, st in faelle:
            z[st] += 1
            summe[st] += 1
        print("%s: leer %d, Fehlwert-Text %d, ohne close-Spalte %d"
              % (s, z["leer"], z["natext"], z["spalte"]))
        for t, ot, st in faelle[:MAX_FAELLE_JE_SYMBOL]:
            print("FALL\tm1\tclose_fehlt_%s\t%s\t%s" % (st, s, t or ot))
        if len(faelle) > MAX_FAELLE_JE_SYMBOL:
            print("    (+%d weitere)" % (len(faelle) - MAX_FAELLE_JE_SYMBOL))
    print("Summe: leer %d, Fehlwert-Text %d, ohne close-Spalte %d"
          % (summe["leer"], summe["natext"], summe["spalte"]))
    unles = sum(1 for r in reihen.values() for _, t, _ in r["zeilen"]
                if t is None)
    print("Zeilen mit unlesbarem Datum in open_time: %d" % unles)
    for s in symbole:
        r = reihen.get(s)
        for ot, t, _ in (r["zeilen"] if r else ()):
            if t is None:
                print("FALL\tm1\tdatum_unlesbar\t%s\t%s" % (s, ot))

    print("\n## Nr. 6  Verkuerzte Sitzungen (L6)")
    fb = min(dt.date(j, 1, 1) for _, m, j in BOTS if m == "aktien")
    plan, Hs = sitzungen(kal, fb, h_bis)
    tz = getattr(kal, "tz", None)
    print("Kalenderklasse %s, Zeitzone %s, regulaerer Schluss (close_time) %s"
          % (type(kal).__name__, tz, getattr(kal, "close_time", "?")))
    print("schedule-Spalten: %s" % list(plan.columns))
    regulaer = getattr(kal, "close_time", None)
    lokal = plan["market_close"].dt.tz_convert(tz)
    frueh = [ts.date() for ts, c in zip(plan.index, lokal)
             if regulaer is not None and c.time() < regulaer.replace(tzinfo=None)]
    try:
        ec = kal.early_closes(plan)
        ec_tage = sorted(ts.date() for ts in ec.index)
        ec_text = "%d" % len(ec_tage)
    except Exception as e:  # noqa: BLE001
        ec_tage, ec_text = None, "nicht aufrufbar (%s)" % type(e).__name__
    print("Sitzungstage %s..%s: %d, davon Schluss vor dem regulaeren: %d"
          % (fb, h_bis, len(Hs), len(frueh)))
    print("kal.early_closes(schedule): %s; gleich der eigenen Zaehlung: %s"
          % (ec_text, "ja" if ec_tage == sorted(frueh) else "nein"))
    print("alle verkuerzten in H: %s" % ("ja" if set(frueh) <= H else "nein"))
    schluss = {ts.date(): c for ts, c in zip(plan.index, lokal)}
    for t in frueh[:3]:
        print("    Beispiel %s, Schluss %s Ortszeit"
              % (t, schluss[t].strftime("%H:%M")))
    print("Jahre mit verkuerzten Sitzungen: %s" % dict(sorted(
        {y: sum(1 for t in frueh if t.year == y)
         for y in {t.year for t in frueh}}.items())))

    rc = 1 if befund else 0
    print("\nRUECKGABE %d (%s)" % (rc, "Befund: R66 (b) bei mindestens einem "
                                   "Aktien-Bot nicht erfuellt" if befund
                                   else "kein Befund"))
    return rc


# ---------------------------------------------------------------- M2

def m2(snapshot, bis, na):
    kopf("m2", snapshot)
    aktien = universum(snapshot, AKTIEN_DATEI)
    krypto = universum(snapshot, KRYPTO_DATEI)
    alle = set(aktien) | set(krypto)
    dateien = sorted(f for f in os.listdir(snapshot) if f.endswith(".csv"))

    print("## Nr. 1  Reihen je Zeile der Universumsdateien")
    for name, liste, tfs in (("aktien", aktien, ("1d",)),
                             ("krypto", krypto, ("1d", "1h", "4h"))):
        zaehl = defaultdict(int)
        for s in liste:
            da = [tf for tf in tfs if os.path.isfile(
                os.path.join(snapshot, "%s_%s.csv" % (s, tf)))]
            for tf in da:
                zaehl[tf] += 1
            fehlt = [tf for tf in tfs if tf not in da]
            if fehlt:
                print("FALL\tm2\treihe_fehlt_%s\t%s\t-"
                      % ("_".join(fehlt), s))
        print("%s: %d Zeilen; Reihen %s"
              % (name, len(liste), dict(sorted(zaehl.items()))))
    ohne = [f for f in dateien if f.rsplit("_", 1)[0] not in alle]
    print("Reihen ohne Zeile in einer der zwei Dateien: %d" % len(ohne))
    for f in ohne:
        print("FALL\tm2\treihe_ohne_zeile\t%s\t-" % f)

    kal, fehler = lade_kalender()
    if kal is None:
        print("\nKalender %r nicht ladbar: %s -> Aktien mit ERSATZ "
              "(Tage K statt H)" % (KALENDER_NAME, fehler))

    befund = False
    for name, liste in (("aktien", aktien), ("krypto", krypto)):
        print("\n" + "=" * 70)
        print("# Markt %s" % name)
        reihen = lies_markt(snapshot, liste, na)
        ktage = {s: kurstage(r) for s, r in reihen.items()}
        bewertet = [s for s in liste if s in reihen
                    and s not in NICHT_BEWERTET]
        K = set().union(*(ktage[s] for s in bewertet)) if bewertet else set()
        if not K:
            print("Keine Kurstage - nicht messbar")
            return 2
        k_von, k_bis = min(K), max(K)
        if name == "aktien":
            if kal is not None:
                _, H = sitzungen(kal, k_von, max(k_bis, bis))
                h_art = "Sitzungstage %r" % KALENDER_NAME
            else:
                H, h_art = set(K), "ERSATZ: Tage K"
        else:
            H = tage_zwischen(k_von, max(k_bis, bis))
            h_art = "Kalendertage"
        print("Handelstage: %s, %s..%s, %d" % (h_art, k_von,
                                               max(k_bis, bis), len(H)))

        print("\n## Nr. 2  Reihenenden")
        letzter = k_bis
        print("letzter Kurstag des Marktes (L7): %s" % letzter)
        frueh = 0
        for s in bewertet:
            if not ktage[s]:
                print("FALL\tm2\tohne_kurstag\t%s\t-" % s)
                frueh += 1
                continue
            e = max(ktage[s])
            if e < letzter:
                frueh += 1
                print("FALL\tm2\tfrueher_endend_1d\t%s\t%s" % (s, e))
                print("    letzter Kurstag %s Ende nach L3 (%s)"
                      % ("vor dem" if e < bis else "am oder nach dem", bis))
                for z in nach_letztem_kurstag(snapshot, s, e):
                    print("    danach: %s" % z)
        print("_1d-Reihen, die vor %s enden: %d von %d"
              % (letzter, frueh, len(bewertet)))
        if frueh:
            befund = True
        if name == "krypto":
            print("_1h/_4h (Tag des letzten Zeitstempels, ohne Urteil):")
            for tf in ("1h", "4h"):
                n = fr = 0
                for s in liste:
                    p = os.path.join(snapshot, "%s_%s.csv" % (s, tf))
                    if not os.path.isfile(p):
                        continue
                    r = lies_reihe(p, na)
                    tage = [t for _, t, _ in r["zeilen"] if t is not None]
                    n += 1
                    if not tage:
                        print("    %s_%s: ohne Zeile" % (s, tf))
                        continue
                    e = max(tage)
                    zus = " (nicht bewertet, Register Z. 1583-1586)" \
                        if s in NICHT_BEWERTET else ""
                    if e < letzter:
                        fr += 1
                        print("    %s_%s: letzter Tag %s%s" % (s, tf, e, zus))
                print("    %s: %d Reihen, davon vor %s endend: %d"
                      % (tf, n, letzter, fr))

        print("\n## Nr. 3  Symbol-Tage Luecke (L8) auf _1d")
        luecken = []
        vorher = defaultdict(int)
        for s in bewertet:
            if not ktage[s]:
                continue
            a, e = min(ktage[s]), max(ktage[s])
            for t in sorted(H):
                if t < a:
                    vorher[t.year] += 1
                elif t <= e and t not in ktage[s]:
                    luecken.append((s, t))
        luecken.sort(key=lambda x: (x[1], x[0]))
        je_jahr = defaultdict(int)
        for _, t in luecken:
            je_jahr[t.year] += 1
        print("Summe %s: %d" % (name, len(luecken)))
        print("je Kalenderjahr: %s" % dict(sorted(je_jahr.items())))
        for s, t in luecken:
            print("FALL\tm2\tluecke\t%s\t%s" % (s, t))
        for bot, markt, jahr in BOTS:
            if markt != name:
                continue
            von = dt.date(jahr, 1, 1)
            n = sum(1 for _, t in luecken if von <= t <= bis)
            print("%s: Zeitraum %s..%s, Symbol-Tage Luecke %d"
                  % (bot, von, bis, n))
        print("Symbol-Tage vor dem ersten Kurstag eines Symbols, ab %s "
              "(ohne Einzelliste), je Kalenderjahr:" % k_von)
        print("    %s; Summe %d" % (dict(sorted(vorher.items())),
                                    sum(vorher.values())))

        print("\n## Nr. 4  doppelte open_time, doppelte Tage, Zeitanteile "
              "(53.10 Nr. 10)")
        sd = st = sz = 0
        for s in liste:
            if s not in reihen:
                continue
            gesehen = {}
            for ot, t, _ in reihen[s]["zeilen"]:
                if ot in gesehen:
                    sd += 1
                    print("FALL\tm2\tdoppelt_open_time\t%s\t%s" % (s, ot))
                gesehen.setdefault(ot, t)
            je_t = defaultdict(set)
            for ot, t in gesehen.items():
                if t is not None:
                    je_t[t].add(ot)
            for t, ots in sorted(je_t.items()):
                if len(ots) > 1:
                    st += 1
                    print("FALL\tm2\tdoppelt_tag\t%s\t%s" % (s, t))
            for ot, t, _ in reihen[s]["zeilen"]:
                rest = ot[10:].strip()
                if rest and rest not in ("00:00:00", "00:00", "00:00:00+00:00"):
                    sz += 1
                    print("FALL\tm2\tzeitanteil\t%s\t%s" % (s, ot[:10]))
        print("Summe %s: doppelte open_time %d, doppelte Tage %d, "
              "Zeitanteil ungleich Mitternacht %d" % (name, sd, st, sz))

    rc = 1 if befund else 0
    print("\nRUECKGABE %d (%s)" % (rc, "Befund: mindestens eine _1d-Reihe "
                                   "endet frueher" if befund else "kein Befund"))
    return rc


# ---------------------------------------------------------------- M3

def m3(snapshot, bis, na):
    gleich, ist, lw = kopf("m3", snapshot)
    print("## Nr. 1  Fassungen gegen requirements.lock")
    abw = False
    for name, _, _ in PAKETE:
        nr, z, soll = lw[name]
        ok = soll is not None and ist[name] == soll
        abw = abw or not ok
        print("%-24s Ist %-10s Lock Z. %d %-40s %s"
              % (name, ist[name], nr, repr(z), "gleich" if ok else "ABWEICHUNG"))
    print("Interpreter venv: Ist %s, Lock Z. 6 %s"
          % (sys.version.split()[0], lw["venv"]))
    print("Interpreter voll: gleich Lock Z. 7: %s"
          % ("ja" if " ".join(sys.version.split()) ==
             " ".join((lw["voll"] or "").split()) else "nein"))
    try:
        import pandas_market_calendars as mcal
        print("pandas_market_calendars.__file__ %s" % mcal.__file__)
    except Exception as e:  # noqa: BLE001
        print("pandas_market_calendars nicht importierbar: %s" % e)
        abw = True
    rc = 1 if abw or not gleich else 0
    print("\nRUECKGABE %d (%s)" % (rc, "Befund: Abweichung vom Lock" if rc
                                   else "kein Befund"))
    return rc


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("messung", choices=("m1", "m2", "m3"))
    a.add_argument("--snapshot", default=STANDARD_SNAPSHOT)
    a.add_argument("--bis", default=STANDARD_BIS)
    x = a.parse_args(argv)
    bis = dt.date.fromisoformat(x.bis)
    if not os.path.isfile(LOCK):
        print("%s nicht gefunden - aus der Repo-Wurzel aufrufen" % LOCK)
        return 2
    if not os.path.isdir(x.snapshot):
        print("Snapshot-Ordner nicht gefunden: %s" % x.snapshot)
        return 2
    na, _ = na_texte()
    return {"m1": m1, "m2": m2, "m3": m3}[x.messung](x.snapshot, bis, na)


if __name__ == "__main__":
    sys.exit(main())
