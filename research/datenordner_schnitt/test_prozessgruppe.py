#!/usr/bin/env python3
"""
TB-47, Teil 4: beendet der Basislauf die ganze Prozessgruppe?
==============================================================================
`research/datenordner_schnitt/basislauf.py` schickte nach der Zeitgrenze
`kill()` an den **Kindprozess**. Mehrere Tests dieses Projekts starten sich
aber selbst einen Unterprozess - und dieser **Enkel** ueberlebte den `kill`:
er verlor nur seinen Elternprozess, haengte sich an PID 1 und rechnete weiter.

⚠️ **Gemessen, nicht vermutet.** In beiden Mac-Laeufen blieb nach der
Zeitgrenze von `shared/test_drawdown_beide_masse.py` ein
`--bot elliott_wave` zurueck, zuletzt **22 Minuten bei 99 % CPU**, bis ihn
ein Mensch von Hand beendet hat.

WARUM DIESER TEST UEBERHAUPT EXISTIERT
------------------------------------------------------------------------------
Der Auftrag sagt: *"Und ein Nachweis, der zeigt, dass es wirkt. Ohne diesen
Nachweis ist die Reparatur eine Behauptung."*

Eine Reparatur, die man nur liest, ist geraten. Dieser Test stellt die Lage
**her**: ein Wegwerf-Programm, das sich selbst ein Kind startet, beide
rechnen endlos. Dann laeuft `basislauf.fuehre_aus` mit einer kurzen
Zeitgrenze darueber - und danach wird nachgesehen, ob **noch irgendein
Prozess der Gruppe lebt**.

⚠️ **Und die Gegenprobe gehoert dazu.** Dieselbe Lage wird ein zweites Mal
hergestellt, diesmal mit dem **alten** Verfahren (`kill()` auf den
Kindprozess, ohne eigene Prozessgruppe). Dort **muss** der Enkel
ueberleben - sonst misst dieser Test etwas anderes als die Reparatur, und
sein Gruen waere wertlos. Das ist dieselbe Bauform wie die Mutationsproben
in `shared/test_snapshot.py`.

Nutzung:  python3 research/datenordner_schnitt/test_prozessgruppe.py
"""

import importlib.util
import os
import signal
import subprocess
import sys
import tempfile
import time

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))
BASISLAUF_PFAD = os.path.join(_HIER, "basislauf.py")

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print("  [OK ] %s%s" % (name, "   " + detail if detail else ""))
    else:
        FEHLER.append(name)
        print("  [FEHLER] %s%s" % (name, "   " + detail if detail else ""))


def lade_basislauf():
    """`basislauf.py` ueber den Dateipfad laden, nicht ueber den Suchpfad.

    ⚠️ TB-40: gleichnamige Module werden in diesem Projekt nicht ueber
    `sys.path` importiert.
    """
    spez = importlib.util.spec_from_file_location("tb47_basislauf",
                                                  BASISLAUF_PFAD)
    modul = importlib.util.module_from_spec(spez)
    spez.loader.exec_module(modul)
    return modul


# ---------------------------------------------------------------------------
# Das Wegwerf-Programm: es startet sich selbst ein Kind und rechnet endlos
# ---------------------------------------------------------------------------

ELTERN = '''\
import os, subprocess, sys, time
kind = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kind.py")
p = subprocess.Popen([sys.executable, kind])
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "pids.txt"), "w") as f:
    f.write("%d\\n%d\\n" % (os.getpid(), p.pid))
    f.flush()
    os.fsync(f.fileno())
while True:            # der Elternprozess terminiert ebenfalls nicht
    time.sleep(0.05)
'''

KIND = '''\
import time
while True:            # ⚠️ der Enkel - er ueberlebte bisher den kill()
    time.sleep(0.05)
'''


def _baue(ordner):
    """Das Elternprogramm und sein Kind in ein Wegwerf-Verzeichnis legen."""
    eltern = os.path.join(ordner, "test_endlos_mit_kind.py")
    with open(eltern, "w", encoding="utf-8") as f:
        f.write(ELTERN)
    with open(os.path.join(ordner, "kind.py"), "w", encoding="utf-8") as f:
        f.write(KIND)
    return eltern


def _pids(ordner, frist=20):
    """Auf die beiden PIDs warten, die das Elternprogramm hinterlegt."""
    pfad = os.path.join(ordner, "pids.txt")
    ende = time.time() + frist
    while time.time() < ende:
        if os.path.exists(pfad):
            try:
                with open(pfad, encoding="utf-8") as f:
                    zeilen = [z.strip() for z in f if z.strip()]
                if len(zeilen) == 2:
                    return int(zeilen[0]), int(zeilen[1])
            except (OSError, ValueError):
                pass
        time.sleep(0.05)
    return None, None


def lebt(pid, frist=5):
    """Lebt dieser Prozess noch?

    ⚠️ `os.kill(pid, 0)` allein genuegt nicht: ein beendetes Kind bleibt als
    **Zombie** stehen, bis jemand es abholt, und ein Zombie nimmt Signal 0
    noch an. Ein Zombie rechnet aber nicht - er ist genau das, was diese
    Reparatur erreichen will. Deshalb wird kurz gewartet und danach der
    Zustand gelesen.
    """
    ende = time.time() + frist
    while time.time() < ende:
        try:
            os.kill(pid, 0)
        except OSError:
            return False                      # es gibt ihn nicht mehr
        if _ist_zombie(pid):
            return False
        time.sleep(0.1)
    return True


def _ist_zombie(pid):
    """Steht dieser Prozess auf `Z` (beendet, noch nicht abgeholt)?"""
    # Linux: /proc. Mac: `ps`. Beide Wege, denn der Betrieb laeuft auf dem Mac
    # und dieser Test wird dort ebenfalls laufen.
    pfad = "/proc/%d/stat" % pid
    if os.path.exists(pfad):
        try:
            with open(pfad, encoding="utf-8") as f:
                teile = f.read().rsplit(")", 1)[-1].split()
            return bool(teile) and teile[0] == "Z"
        except OSError:
            return True
    try:
        lauf = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)],
                              capture_output=True, text=True)
    except OSError:
        return False
    zustand = (lauf.stdout or "").strip()
    return zustand.startswith("Z") or not zustand


def _aufraeumen(*pids):
    """Was dieser Test gestartet hat, beendet er auch - komme, was wolle."""
    for pid in pids:
        if not pid:
            continue
        for sig in (signal.SIGKILL,):
            try:
                os.kill(pid, sig)
            except OSError:
                pass


# ===========================================================================
# 1 - Die Reparatur: nach der Zeitgrenze lebt kein Prozess der Gruppe mehr
# ===========================================================================

def teil_1_reparatur(basislauf):
    print("\n1. NACH DER ZEITGRENZE LEBT KEIN PROZESS DER GRUPPE MEHR")
    arbeit = tempfile.mkdtemp(prefix="tb47_gruppe_")
    eltern_pid = kind_pid = None
    try:
        eltern = _baue(arbeit)
        rel = os.path.relpath(eltern, arbeit)

        beginn = time.time()
        ergebnis = basislauf.fuehre_aus(rel, arbeit, grenze=5)
        dauer = time.time() - beginn

        eltern_pid, kind_pid = _pids(arbeit)
        check("1.1 die beiden Prozesse haben sich gemeldet",
              bool(eltern_pid) and bool(kind_pid),
              "Eltern %s, Enkel %s" % (eltern_pid, kind_pid))
        if not eltern_pid:
            return

        check("1.2 der Lauf ist an der Zeitgrenze abgebrochen",
              ergebnis.get("art") == "zeitgrenze", str(ergebnis.get("art")))
        check("1.3 und er hat dafuer nicht wesentlich laenger gebraucht",
              dauer < 40, "%.1f s" % dauer)

        # ⭐ Der Kern der Sache.
        check("1.4 der Kindprozess lebt nicht mehr", not lebt(eltern_pid),
              "PID %d" % eltern_pid)
        check("1.5 ⭐ DER ENKELPROZESS LEBT EBENFALLS NICHT MEHR",
              not lebt(kind_pid), "PID %d" % kind_pid)
    finally:
        _aufraeumen(eltern_pid, kind_pid)
        import shutil
        shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
# 2 - Die Gegenprobe: mit dem alten Verfahren ueberlebt der Enkel
# ===========================================================================

def teil_2_gegenprobe():
    print("\n2. GEGENPROBE - mit dem ALTEN Verfahren ueberlebt der Enkel")
    print("   (sonst misst Teil 1 etwas anderes als die Reparatur)")
    arbeit = tempfile.mkdtemp(prefix="tb47_alt_")
    eltern_pid = kind_pid = None
    try:
        eltern = _baue(arbeit)

        # Genau das alte Verfahren: KEINE eigene Prozessgruppe, und `kill()`
        # auf den Kindprozess statt `killpg` auf die Gruppe.
        prozess = subprocess.Popen(
            [sys.executable, eltern], cwd=arbeit,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            prozess.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        eltern_pid, kind_pid = _pids(arbeit)
        check("2.1 die beiden Prozesse haben sich gemeldet",
              bool(eltern_pid) and bool(kind_pid),
              "Eltern %s, Enkel %s" % (eltern_pid, kind_pid))
        if not eltern_pid:
            return

        prozess.kill()                        # ⚠️ das alte Verfahren
        try:
            prozess.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            pass

        check("2.2 der Kindprozess ist auch so beendet",
              not lebt(prozess.pid), "PID %d" % prozess.pid)
        # ⚠️ Das ist der Befund, den TB-47 repariert. Er MUSS hier auftreten.
        check("2.3 ⭐ der Enkelprozess ueberlebt das alte Verfahren - genau "
              "das war der Befund", lebt(kind_pid, frist=3),
              "PID %d" % kind_pid)
    finally:
        _aufraeumen(eltern_pid, kind_pid)
        import shutil
        shutil.rmtree(arbeit, ignore_errors=True)


# ===========================================================================
# 3 - Die Reparatur steht wirklich im Quelltext
# ===========================================================================

def teil_3_quelltext():
    print("\n3. DIE REPARATUR STEHT IM QUELLTEXT")
    with open(BASISLAUF_PFAD, "r", encoding="utf-8") as f:
        text = f.read()
    check("3.1 der Kindprozess bekommt eine eigene Prozessgruppe",
          "start_new_session=True" in text)
    check("3.2 beendet wird ueber die Gruppe, nicht ueber den Prozess",
          "os.killpg" in text)
    check("3.3 und `fuehre_aus` benutzt sie auch",
          "beende_gruppe(prozess)" in text)


def main():
    print("=" * 78)
    print("TB-47, Teil 4: der Enkelprozess im Basislauf")
    print("=" * 78)

    if not hasattr(os, "killpg"):
        # Kein stillschweigendes Ueberspringen: hier gibt es nichts zu
        # messen, und das ist ein roter Ausgang, kein gruener.
        check("dieses Betriebssystem kennt Prozessgruppen", False,
              "os.killpg fehlt")
    else:
        basislauf = lade_basislauf()
        for teil in (lambda: teil_1_reparatur(basislauf), teil_2_gegenprobe,
                     teil_3_quelltext):
            try:
                teil()
            except Exception as fehler:                      # noqa: BLE001
                import traceback
                FEHLER.append("%s (Ausnahme)" % getattr(teil, "__name__",
                                                        "teil"))
                print("  [FEHLER] Ausnahme: %s" % fehler)
                traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print("%d von %d Pruefungen bestanden, %d fehlgeschlagen."
          % (BESTANDEN, gesamt, len(FEHLER)))
    for name in FEHLER:
        print("  - %s" % name)
    if gesamt == 0:
        print("KEINE EINZIGE PRUEFUNG GELAUFEN - das ist ein Fehler, "
              "kein Bestehen.")
        return 1
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
