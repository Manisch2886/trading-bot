#!/usr/bin/env python3
"""TB-140 Z1 - je Tagesreihe (*_1d.csv) des Snapshots: Zeilen, Zeilen ohne close,
Datum der letzten Zeile, Datum der letzten Zeile mit close; getrennt nach Aktien und Krypto.
Liest die Dateien als Text; kein Kurs wird ausgegeben oder in eine Zahl gewandelt.
Rueckgabe: 0 wie der Satz aus R79 (c), 1 anders, 2 nicht messbar (Ordner oder Universumsdatei
fehlt, eine Tagesreihe ist leer oder nicht lesbar, oder eine Ausnahme)."""
import argparse
import csv
import datetime as dt
import os
import sys
import traceback

SNAPSHOT = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
AKTIEN_DATEI = "sp500_top150.txt"      # docs/belege/TB-138/verfahrensmessung_snapshot.py Z. 37
KRYPTO_DATEI = "top25_symbols.txt"     # ebd. Z. 38
SATZ_AKTIEN = [("APH_1d.csv", "2026-09-01")]   # R79 (c): "in genau dieser Zeile"
SATZ_KRYPTO_REIHEN = 24                         # R79 (c): "in den 24 Krypto-Tagesreihen in keiner"
MAX_FAELLE_JE_DATEI = 50

# L5 des Vorgaengers: leer oder ein Text, den pandas.read_csv als Fehlwert liest.
# Die Liste der Umgebung gilt; diese hier ist nur der Rueckfall (Vorgaenger Z. 62-64).
_NA_RUECKFALL = {"", "#N/A", "#N/A N/A", "#NA", "-1.#IND", "-1.#QNAN", "-NaN",
                 "-nan", "1.#IND", "1.#QNAN", "<NA>", "N/A", "NA", "NULL",
                 "NaN", "None", "n/a", "nan", "null"}


def na_texte():
    """Wie der Vorgaenger (Z. 67-73)."""
    try:
        from pandas._libs.parsers import STR_NA_VALUES
        return set(STR_NA_VALUES), "pandas._libs.parsers.STR_NA_VALUES"
    except Exception as e:  # noqa: BLE001
        return set(_NA_RUECKFALL), "Rueckfall im Skript (%s)" % type(e).__name__


def universum(snapshot, datei):
    """Wie der Vorgaenger (Z. 134-137)."""
    with open(os.path.join(snapshot, "config", datei), encoding="utf-8") as f:
        return [z.strip() for z in f if z.strip() and "#" not in z]


def lies(pfad, na):
    """Zaehlt eine Tagesreihe. Rueckgabe dict oder Text mit dem Grund, warum sie nicht lesbar ist."""
    e = {"zeilen": 0, "leer": 0, "natext": 0, "spalte": 0, "ohne_datum": 0,
         "letzte": "-", "letzte_mit_close": "-", "groesstes": "-", "faelle": []}
    with open(pfad, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        try:
            kopf = next(r)
        except StopIteration:
            return "leer"
        if "open_time" not in kopf or "close" not in kopf:
            return "Kopfzeile ohne open_time/close"
        i_t, i_c = kopf.index("open_time"), kopf.index("close")
        for zeile in r:
            if not zeile:
                continue
            e["zeilen"] += 1
            tag = zeile[i_t][:10] if len(zeile) > i_t else ""
            try:
                dt.date.fromisoformat(tag)
            except ValueError:
                e["ohne_datum"] += 1
                tag = "kein_datum"
            if len(zeile) <= i_c:
                art = "spalte"
            elif zeile[i_c] == "":
                art = "leer"
            elif zeile[i_c] in na:
                art = "natext"
            else:
                art = None
            e["letzte"] = tag
            if tag != "kein_datum" and (e["groesstes"] == "-" or tag > e["groesstes"]):
                e["groesstes"] = tag
            if art is None:
                e["letzte_mit_close"] = tag
            else:
                e[art] += 1
                e["faelle"].append((tag, art))
    return e


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", default=SNAPSHOT)
    x = p.parse_args(argv)
    na, na_quelle = na_texte()
    print("# TB-140 Z1")
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("sys.executable   %s" % sys.executable)
    print("snapshot         %s" % x.snapshot)
    print("Fehlwert-Texte   %d aus %s" % (len(na), na_quelle))
    if not os.path.isdir(x.snapshot):
        print("NICHT MESSBAR: Ordner fehlt")
        return 2
    try:
        markt = {s: "aktien" for s in universum(x.snapshot, AKTIEN_DATEI)}
        krypto = universum(x.snapshot, KRYPTO_DATEI)
    except OSError as e:
        print("NICHT MESSBAR: Universumsdatei: %s" % e)
        return 2
    doppelt = sorted(s for s in krypto if s in markt)
    for s in krypto:
        markt.setdefault(s, "krypto")
    dateien = sorted(n for n in os.listdir(x.snapshot) if n.endswith("_1d.csv"))
    print("Universum        aktien %d, krypto %d, in beiden %s" % (
        sum(1 for v in markt.values() if v == "aktien"), len(krypto), doppelt))
    print("Dateien *_1d.csv %d" % len(dateien))
    ohne_reihe = sorted(s for s in markt if s + "_1d.csv" not in dateien)
    print("Symbole ohne _1d-Reihe: %d %s" % (len(ohne_reihe), ohne_reihe))
    if not dateien:
        print("NICHT MESSBAR: keine Datei *_1d.csv")
        return 2

    print("\nDATEI\tmarkt\tdatei\tzeilen\tohne_close\tleer\tfehlwert_text\tspalte_fehlt\tletzte_zeile\tletzte_zeile_mit_close")
    summe, enden, faelle, unlesbar, hinweise = {}, {}, [], [], []
    for n in dateien:
        m = markt.get(n[:-len("_1d.csv")], "ohne_zuordnung")
        try:
            e = lies(os.path.join(x.snapshot, n), na)
        except Exception as f:  # noqa: BLE001
            e = type(f).__name__
        if isinstance(e, str):
            unlesbar.append((n, e))
            print("DATEI\t%s\t%s\tNICHT LESBAR: %s" % (m, n, e))
            continue
        ohne = e["leer"] + e["natext"] + e["spalte"]
        print("DATEI\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%s\t%s" % (
            m, n, e["zeilen"], ohne, e["leer"], e["natext"], e["spalte"], e["letzte"], e["letzte_mit_close"]))
        s = summe.setdefault(m, {"dateien": 0, "zeilen": 0, "ohne": 0})
        s["dateien"] += 1
        s["zeilen"] += e["zeilen"]
        s["ohne"] += ohne
        for art, tag in (("letzte_zeile", e["letzte"]), ("letzte_zeile_mit_close", e["letzte_mit_close"])):
            enden[(m, art, tag)] = enden.get((m, art, tag), 0) + 1
        faelle += [(m, n, tag, art) for tag, art in e["faelle"][:MAX_FAELLE_JE_DATEI]]
        if len(e["faelle"]) > MAX_FAELLE_JE_DATEI:
            hinweise.append("%s: %d weitere Zeilen ohne close nicht einzeln gedruckt" % (n, len(e["faelle"]) - MAX_FAELLE_JE_DATEI))
        if e["ohne_datum"]:
            hinweise.append("%s: %d Zeilen ohne lesbares Datum" % (n, e["ohne_datum"]))
        if e["letzte"] != e["groesstes"]:
            hinweise.append("%s: letzte Zeile %s, groesstes Datum %s" % (n, e["letzte"], e["groesstes"]))

    print("\nEinzelfaelle (Zeile ohne close)")
    for m, n, tag, art in faelle:
        print("FALL\tz1\t%s\t%s\t%s\t%s" % (m, n, tag, art))
    print("Einzelfaelle gedruckt: %d" % len(faelle))
    print("\nSummen je Markt")
    for m in sorted(summe):
        s = summe[m]
        print("SUMME\t%s\tdateien %d\tzeilen %d\tohne_close %d" % (m, s["dateien"], s["zeilen"], s["ohne"]))
    for (m, art, tag), anz in sorted(enden.items()):
        print("ENDE\t%s\t%s\t%s\t%d" % (m, art, tag, anz))
    print("\nHinweise: %d" % len(hinweise))
    for h in hinweise:
        print("HINWEIS\t%s" % h)
    if unlesbar:
        print("\nNICHT MESSBAR: %d Datei(en) nicht lesbar" % len(unlesbar))
        return 2

    ist_aktien = sorted((n, tag) for m, n, tag, _ in faelle if m == "aktien")
    krypto_ohne = summe.get("krypto", {"ohne": 0})["ohne"]
    krypto_reihen = summe.get("krypto", {"dateien": 0})["dateien"]
    fremd_ohne = summe.get("ohne_zuordnung", {"ohne": 0})["ohne"]
    aktien_wie = ist_aktien == sorted(SATZ_AKTIEN) and summe.get("aktien", {"ohne": 0})["ohne"] == len(SATZ_AKTIEN)
    print("\nSATZ R79 (c), Aktien: close fehlt in genau %s -> %s" % (SATZ_AKTIEN, "trifft zu" if aktien_wie else "TRIFFT NICHT ZU"))
    krypto_wie = krypto_ohne == 0 and krypto_reihen == SATZ_KRYPTO_REIHEN
    print("SATZ R79 (c), Krypto: close fehlt in keiner der %d Reihen -> %s (Zeilen ohne close: %d, Reihen: %d)" % (
        SATZ_KRYPTO_REIHEN, "trifft zu" if krypto_wie else "TRIFFT NICHT ZU", krypto_ohne, krypto_reihen))
    print("Dateien ohne Zuordnung: %d, darin Zeilen ohne close: %d" % (
        summe.get("ohne_zuordnung", {"dateien": 0})["dateien"], fremd_ohne))
    wie = aktien_wie and krypto_wie
    print("RUECKGABE %d" % (0 if wie else 1))
    return 0 if wie else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
