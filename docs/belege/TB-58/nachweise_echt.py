#!/usr/bin/env python3
"""TB-58, Schritt 3: die Nachweise 3-8 gegen den ECHTEN Arbeitsbaum.

Die Mutationsgegenproben (Nachweis 9) stehen in shared/test_startpruefungen.py
(Wegwerf-Repos). Hier wird gegen /Users/jaquelineloffler/trading-bot gemessen,
mit dem echten Snapshot und dem echten HEAD. Der Arbeitsbaum wird dabei nur
mit einer untracked Datei an der Wurzel (Einstiegspunkt, ausserhalb der
geprueften Pfade) und - fuer Nachweis 7 - einer untracked Datei unter shared/
fuer wenige Sekunden beruehrt; beide werden im finally entfernt.
"""
import json, os, shutil, subprocess, sys, tempfile

WURZEL = "/Users/jaquelineloffler/trading-bot"
SNAP_HASH = "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
SNAP = os.path.join(WURZEL, "snapshots", SNAP_HASH)
PY = sys.executable
HEAD = subprocess.run(["git", "-C", WURZEL, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
BOTS = ("elliott_wave", "elliott_wave_stocks", "rsi2_crypto",
        "rsi2_mean_reversion", "t3_supertrend", "turtle_soup_crypto",
        "turtle_soup_stocks", "volatility_breakout", "volatility_breakout_crypto")

_LAUF = '''import json, os, sys
sys.path.insert(0, %r)
import paths
json.dump({"DATA_DIR": paths.DATA_DIR, "start": paths.startpruefung(),
           "zeilen": paths.audit_zeilen()}, sys.stdout)
''' % os.path.join(WURZEL, "shared")


def lauf(einstieg, commit=HEAD, python=PY, modus=True):
    umg = dict(os.environ)
    for n in ("TB_SELEKTIONSWURZEL", "TB_SELEKTIONSHASH", "TB_SELEKTIONSCOMMIT"):
        umg.pop(n, None)
    if modus:
        umg["TB_SELEKTIONSWURZEL"] = SNAP
        umg["TB_SELEKTIONSHASH"] = SNAP_HASH
        if commit is not None:
            umg["TB_SELEKTIONSCOMMIT"] = commit
    e = subprocess.run([python, einstieg], capture_output=True, text=True, env=umg)
    return e.returncode, e.stdout, e.stderr


def zeile(nr, name, ok, detail):
    print("  [%s] %-2s %s - %s" % ("ok " if ok else "FEHL", nr, name, detail))
    return ok


def main():
    print("HEAD =", HEAD, " Python =", PY)
    einstieg = os.path.join(WURZEL, "tb58_lauf.py")
    schmutz = os.path.join(WURZEL, "shared", "tb58_unfertig.tmp")
    fremd = tempfile.mkdtemp(prefix="tb58_fremd_")
    fremd_repo = tempfile.mkdtemp(prefix="tb58_fremdrepo_")
    alle = []
    try:
        with open(einstieg, "w") as f:
            f.write(_LAUF)
        # 3 vollstaendig, richtig
        rc, out, err = lauf(einstieg)
        w = json.loads(out) if out.strip() else {}
        alle.append(zeile(3, "vollstaendiger Modus -> rc 0, Audit",
                          rc == 0 and w.get("DATA_DIR") == SNAP
                          and len(w.get("zeilen", [])) == 8,
                          "rc=%d, DATA_DIR im Snapshot=%s, %d Auditzeilen"
                          % (rc, w.get("DATA_DIR") == SNAP, len(w.get("zeilen", [])))))
        for z in [z for z in err.splitlines() if z.startswith("[paths]")]:
            print("        " + z)
        # 4 falscher Commit
        rc, out, err = lauf(einstieg, commit="0123456789abcdef")
        alle.append(zeile(4, "falscher Commit -> rc 2", rc == 2 and not out.strip()
                          and "TB_SELEKTIONSCOMMIT nennt aber" in err,
                          "rc=%d, stdout leer=%s" % (rc, not out.strip())))
        # 5 fehlende Variable
        rc, out, err = lauf(einstieg, commit=None)
        alle.append(zeile(5, "TB_SELEKTIONSCOMMIT fehlt -> rc 2", rc == 2
                          and "TB_SELEKTIONSCOMMIT fehlt" in err, "rc=%d" % rc))
        # 6 gespaltener Baum: Aufrufer im Wegwerfordner (ohne Git / mit eigenem Git)
        for ordner in (fremd, fremd_repo):
            with open(os.path.join(ordner, "lauf.py"), "w") as f:
                f.write(_LAUF)
        subprocess.run(["git", "-C", fremd_repo, "init", "-q"], check=True)
        subprocess.run(["git", "-C", fremd_repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", fremd_repo, "-c", "user.name=x", "-c",
                        "user.email=x@x", "commit", "-q", "-m", "fremd"], check=True)
        rc1, out1, err1 = lauf(os.path.join(fremd, "lauf.py"))
        rc2, out2, err2 = lauf(os.path.join(fremd_repo, "lauf.py"))
        alle.append(zeile(6, "gespaltener Baum (ohne Git / eigenes Git) -> rc 2/2",
                          rc1 == 2 and rc2 == 2 and "keinem Git-Arbeitsbaum" in err1
                          and "Gespaltener Baum" in err2
                          and os.path.realpath(WURZEL) in err2
                          and os.path.realpath(fremd_repo) in err2,
                          "rc=%d/%d, Meldung 2 nennt beide Wurzeln" % (rc1, rc2)))
        print("        " + [z for z in err2.splitlines() if "VERLETZT" in z][0][:230] + "...")
        # 7 schmutziger Arbeitsbaum: untracked Datei unter shared/
        with open(schmutz, "w") as f:
            f.write("# liegt herum\n")
        rc, out, err = lauf(einstieg)
        os.remove(schmutz)
        rc_danach, out_d, _ = lauf(einstieg)
        alle.append(zeile(7, "schmutziger Arbeitsbaum -> rc 2, danach sauber -> rc 0",
                          rc == 2 and "tb58_unfertig.tmp" in err and rc_danach == 0,
                          "rc=%d (nennt die Datei=%s), zurueckgesetzt rc=%d"
                          % (rc, "tb58_unfertig.tmp" in err, rc_danach)))
        # 8 abweichendes Paket: die echte Pruefunktion gegen einen verfaelschten Lock
        sys.path.insert(0, os.path.join(WURZEL, "shared"))
        import paths
        lock = open(os.path.join(WURZEL, "requirements.lock")).read()
        pz = [z for z in lock.splitlines() if z.startswith("pandas==")][0]
        falsch = os.path.join(fremd, "requirements.lock")
        with open(falsch, "w") as f:
            f.write(lock.replace(pz, "pandas==0.0.1"))
        try:
            paths._pruefe_lock(falsch); meldung = ""
        except paths.Startpruefungsfehler as fe:
            meldung = str(fe)
        alle.append(zeile(8, "verfaelschte Lock-Zeile -> Startpruefungsfehler nennt pandas",
                          "pandas: Lock 0.0.1, installiert" in meldung,
                          meldung[meldung.find("pandas"):][:60] if meldung else "NICHTS geworfen"))
        # 8b ein anderer Interpreter (Bordmittel /usr/bin/python3) -> rc 2
        if os.path.exists("/usr/bin/python3"):
            rc, out, err = lauf(einstieg, python="/usr/bin/python3")
            v = [z for z in err.splitlines() if "VERLETZT" in z]
            alle.append(zeile("8b", "/usr/bin/python3 unter dem Modus -> rc 2",
                              rc == 2 and v and "Abweichung" in v[0],
                              "rc=%d: %s" % (rc, (v[0][v[0].find("("):][:170] + "...") if v else "")))
        # 9 Bots: die echten Einstiegspunkte liegen unter derselben Wurzel
        gut = 0
        for bot in BOTS:
            e = os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py")
            try:
                wz, hd, ab = paths._pruefe_codeherkunft(HEAD, einstiegspunkt=e)
                gut += (os.path.realpath(wz) == os.path.realpath(WURZEL)
                        and hd == HEAD and ab == "sauber")
            except paths.Startpruefungsfehler as fe:
                print("        %s: %s" % (bot, str(fe)[:120]))
        alle.append(zeile("9b", "neun echte Bot-Einstiegspunkte: Codeherkunft bestanden",
                          gut == 9, "%d von 9 (Wurzel, HEAD, sauber)" % gut))
        # 2 ohne Modus: rc 0, Live-Pfad, keine [paths]-Zeile
        rc, out, err = lauf(einstieg, modus=False)
        w = json.loads(out)
        alle.append(zeile(2, "ohne Modus: Live-Pfad, keine Zeile auf stderr, startpruefung None",
                          rc == 0 and w["DATA_DIR"] == os.path.join(WURZEL, "data")
                          and w["start"] is None and w["zeilen"] == [] and not err.strip(),
                          "rc=%d, DATA_DIR=%s, stderr leer=%s" % (rc, w["DATA_DIR"], not err.strip())))
    finally:
        for p in (einstieg, schmutz):
            if os.path.exists(p):
                os.remove(p)
        shutil.rmtree(fremd, ignore_errors=True)
        shutil.rmtree(fremd_repo, ignore_errors=True)
    st = subprocess.run(["git", "-C", WURZEL, "status", "--short"],
                        capture_output=True, text=True).stdout
    print("git status --short danach: %d Zeilen" % len(st.splitlines()))
    print("%d von %d Nachweisen erbracht" % (sum(alle), len(alle)))
    return 0 if all(alle) else 1


if __name__ == "__main__":
    sys.exit(main())
