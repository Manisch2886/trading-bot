#!/usr/bin/env python3
"""TB-140 V4 - die Umgebung dieses Interpreters gegen requirements.lock:
jede Paketzeile, Interpreter, Plattform. Liest nur, schreibt nur nach stdout.
Rueckgabe: 0 Kopf und W1 gleich, 1 Abweichung in Kopf oder W1, 2 nicht messbar (der Lock fehlt
oder traegt keine Paketzeile, oder eine Ausnahme). W2 wird gedruckt und geht nicht in die
Rueckgabe ein (N1 und O3: vom Werkzeug abhaengig)."""
import argparse
import datetime as dt
import hashlib
import importlib.metadata as md
import os
import platform
import re
import sys
import traceback

LOCK = "requirements.lock"
LOCK_SHA256 = "96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5"  # Register Z. 3231
PAKETE_SOLL = 67                                                                    # Register Z. 3232


def norm(name):
    """Schreibweise nach PEP 503."""
    return re.sub(r"[-_.]+", "-", name).lower()


def lies_lock(pfad):
    """Gelesen wie shared/paths.py::_lies_lock (Z. 499): Kopf `# schluessel wert`, erste Nennung gilt."""
    kopf, pakete, fremd = {}, [], []
    with open(pfad, encoding="utf-8") as f:
        for nr, zeile in enumerate(f, 1):
            zeile = zeile.strip()
            if not zeile:
                continue
            if zeile.startswith("#"):
                teile = zeile[1:].split()
                if len(teile) >= 2:
                    kopf.setdefault(teile[0], " ".join(teile[1:]))
                continue
            if "==" not in zeile:
                fremd.append((nr, zeile))
                continue
            name, fassung = zeile.split("==", 1)
            pakete.append((nr, name.strip(), fassung.strip()))
    return kopf, pakete, fremd


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--lock", default=LOCK)
    x = a.parse_args(argv)
    if not os.path.isfile(x.lock):
        print("NICHT MESSBAR: %s fehlt" % x.lock)
        return 2
    kopf, pakete, fremd = lies_lock(x.lock)
    if not pakete:
        print("NICHT MESSBAR: keine Paketzeile in %s" % x.lock)
        return 2
    with open(x.lock, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    abw = 0
    print("# TB-140 V4")
    print("zeit             %s" % dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print("sys.executable   %s" % sys.executable)
    print("sys.prefix       %s" % sys.prefix)
    print("lock             %s  sha256 %s  %s" % (
        x.lock, sha, "gleich Register" if sha == LOCK_SHA256 else "UNGLEICH Register"))
    print("Paketzeilen      %d (Register: %d), Zeilen ohne `==`: %d" % (len(pakete), PAKETE_SOLL, len(fremd)))

    print("\n## Kopf des Locks gegen die Umgebung")
    paare = (("interpreter_voll", " ".join(sys.version.split()), "prueft der Lauf"),
             ("plattform", platform.platform(), "prueft der Lauf"),
             ("interpreter_venv", sys.version.split()[0], "prueft der Lauf nicht; erstes Wort"),
             ("maschine", platform.machine(), "prueft der Lauf nicht; ohne Urteil"))
    for schluessel, ist, wer in paare:
        soll = kopf.get(schluessel)
        if schluessel == "interpreter_venv" and soll:
            soll = soll.split()[0]
        gleich = soll == ist
        if not gleich and schluessel != "maschine":
            abw += 1
        print("KOPF\t%s\t%r\t%r\t%s\t(%s)" % (schluessel, soll, ist, "gleich" if gleich else "ABWEICHUNG", wer))

    print("\n## W1  importlib.metadata.version(name) je Lock-Zeile (der Weg des Laufs)")
    w1_gleich = 0
    for nr, name, soll in pakete:
        try:
            ist = md.version(name)
        except md.PackageNotFoundError:
            ist = None
        if ist == soll:
            w1_gleich += 1
        else:
            abw += 1
            print("PAKET\tW1\t%d\t%s\t%s\t%s" % (nr, name, soll, ist if ist is not None else "FEHLT"))
    print("W1 gleich %d von %d" % (w1_gleich, len(pakete)))

    print("\n## W2  alle installierten Distributionen, Namen nach PEP 503 (ohne Einfluss auf die Rueckgabe)")
    w2 = "nicht messbar"
    try:
        inst = {}
        for d in md.distributions():
            n = d.metadata["Name"]
            if n:
                inst.setdefault(norm(n), set()).add(d.version)
        w2_gleich = 0
        for nr, name, soll in pakete:
            ist = inst.get(norm(name), set())
            if ist == {soll}:
                w2_gleich += 1
            else:
                print("PAKET\tW2\t%d\t%s\t%s\t%s" % (nr, name, soll, ",".join(sorted(ist)) or "FEHLT"))
        print("W2 gleich %d von %d" % (w2_gleich, len(pakete)))
        im_lock = {norm(n) for _, n, _ in pakete}
        nur_inst = sorted(n for n in inst if n not in im_lock)
        doppelt = sorted(n for n, v in inst.items() if len(v) > 1)
        print("installiert, nicht im Lock (ohne Urteil): %d %s" % (len(nur_inst), nur_inst))
        print("mehr als eine Fassung installiert (ohne Urteil): %d %s" % (len(doppelt), doppelt))
        w2 = "gleich" if w2_gleich == len(pakete) else "ABWEICHEND in %d Zeilen" % (len(pakete) - w2_gleich)
    except Exception as e:  # noqa: BLE001
        print("W2 NICHT MESSBAR: %s: %s" % (type(e).__name__, e))

    erfuellt = abw == 0 and not fremd
    print("\nURTEIL V4 gegen %s, Kopf und W1: %s" % (x.lock, "gleich" if erfuellt else "NICHT gleich"))
    print("W2 (ohne Einfluss auf die Rueckgabe): %s" % w2)
    print("RUECKGABE %d" % (0 if erfuellt else 1))
    return 0 if erfuellt else 1


if __name__ == "__main__":
    try:
        RC = main()
    except Exception:  # noqa: BLE001
        traceback.print_exc(file=sys.stdout)
        print("NICHT MESSBAR: ungefangene Ausnahme (Traceback oben)")
        print("RUECKGABE 2")
        RC = 2
    sys.exit(RC)
