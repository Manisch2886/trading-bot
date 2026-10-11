import os, re, subprocess, sys, tempfile
SKRIPT, PHASE, ORD, HEUTE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:5]
NAME = "EROEFFNUNG_STEUERNDER_CHAT.md"
PFAD = "projektfuehrung/" + NAME
IM_REPO = os.path.exists(os.path.join("docs", "projektfuehrung", NAME))
LISTEN = ("soll.txt", "entfernen.txt", "ablegen.txt", "ohne_regel.txt")
# drei erfundene Pfade, damit auch entfernen.txt und ohne_regel.txt Zeilen fuer die Gegenprobe tragen
ZUSATZ = ["belege/TB-151/probe_b7.md", "projektfuehrung/BACKLOG_ARCHIV.md", "projektfuehrung/PROBE_TB-151_ohne_regel.md"]
TMP = tempfile.mkdtemp(prefix="tb151_")
fehler = []


def lauf(name, pfade):
    """ablage_soll.py einmal aufrufen; Ist-Liste und die vier Listen liegen im Scratch, der Beleg ist eine Datei."""
    ist, aus = os.path.join(TMP, "ist_%s.txt" % name), os.path.join(TMP, name)
    with open(ist, "w", encoding="utf-8") as f:
        f.write("".join(p + "\n" for p in pfade))
    r = subprocess.run([sys.executable, "-B", SKRIPT, "--ist", ist, "--aus", aus] + (["--heute"] + HEUTE if HEUTE else []),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    teile = ["== stdout ==\n" + r.stdout]
    for l in LISTEN:
        p = os.path.join(aus, l)
        teile.append("== %s ==\n%s" % (l, open(p, encoding="utf-8").read() if os.path.exists(p) else ""))
    with open(os.path.join(ORD, "lauf_%s.txt" % name), "w", encoding="utf-8") as f:
        f.write("".join(teile))
    print("%s | rc %d | %s" % (name, r.returncode, r.stdout.strip().replace("\n", " // ")))
    if r.returncode != 0:
        fehler.append(name + ": rc")


def lies(name):
    """Beleg eines Laufs -> (Zahlen der Schlusszeile, {Liste: Zeilen ohne Kopfzeile})."""
    with open(os.path.join(ORD, "lauf_%s.txt" % name), encoding="utf-8") as f:
        t = re.split(r"^== (.+?) ==\n", f.read(), flags=re.M)
    d = dict(zip(t[1::2], t[2::2]))
    zahlen = dict((k, int(v)) for k, v in re.findall(r"(Ist|Soll|entfernen|bleibt|ablegen|ohne Regel) (\d+)", d["stdout"]))
    return zahlen, dict((l, [x for x in d[l].splitlines() if not x.startswith("# ")]) for l in LISTEN)


def mit_namen(name):
    return [(l, x) for l in LISTEN for x in lies(name)[1][l] if NAME in x]


def soll(text, bedingung):
    print("%s %s" % ("ok  " if bedingung else "FEHL", text))
    if not bedingung:
        fehler.append(text)


def gegenprobe(namen):
    for l in LISTEN:
        rest = [[x for x in lies(n)[1][l] if NAME not in x] for n in namen]
        soll("Gegenprobe %s: die uebrigen %d Zeilen sind gleich in %s" % (l, len(rest[0]), ", ".join(namen)),
             all(r == rest[0] for r in rest))


def ist_listen():
    with open(os.path.join(ORD, "ist_mit.txt"), encoding="utf-8") as f:
        mit = [x.strip() for x in f if x.strip()]
    return mit, [p for p in mit if p != PFAD]


os.makedirs(ORD, exist_ok=True)
if PHASE == "alt":
    soll("Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/", not IM_REPO)
    lauf("0", [])
    basis = [x.split("\t")[0] for x in lies("0")[1]["soll.txt"]]
    soll("Basis: Pfade aus dem Soll der Vorfassung, die Datei ist nicht darunter",
         len(basis) > 0 and NAME not in [os.path.basename(p) for p in basis])
    with open(os.path.join(ORD, "ist_mit.txt"), "w", encoding="utf-8") as f:
        f.write("".join(p + "\n" for p in basis + ZUSATZ + [PFAD]))
    lauf("alt_mit", ist_listen()[0])
    soll("alt_mit: die Datei steht nur in ohne_regel.txt, Grund 'keine Regel'",
         mit_namen("alt_mit") == [("ohne_regel.txt", PFAD + "\tkeine Regel")])
elif PHASE == "fehlt":
    soll("Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/", not IM_REPO)
    lauf("neu_fehlt", ist_listen()[1])
    a, f = lies("alt_mit")[0], lies("neu_fehlt")[0]
    zeile = NAME + "\tB2 Stand - FEHLT IM REPO"
    soll("neu_fehlt: die Datei steht in soll.txt und ablegen.txt, blanker Name, Grund 'B2 Stand - FEHLT IM REPO'",
         mit_namen("neu_fehlt") == [("soll.txt", zeile), ("ablegen.txt", zeile)])
    soll("neu_fehlt: Soll +1, ablegen +1, Ist -1, ohne Regel -1, bleibt und entfernen wie alt_mit",
         (f["Soll"], f["ablegen"], f["Ist"], f["ohne Regel"]) == (a["Soll"] + 1, a["ablegen"] + 1, a["Ist"] - 1, a["ohne Regel"] - 1)
         and all(f[k] == a[k] for k in ("bleibt", "entfernen")))
    gegenprobe(("alt_mit", "neu_fehlt"))
elif PHASE == "neu":
    soll("Voraussetzung: die Datei liegt unter docs/projektfuehrung/", IM_REPO)
    mit, ohne = ist_listen()
    lauf("neu_mit", mit)
    lauf("neu_ohne", ohne)
    a, m, o = lies("alt_mit")[0], lies("neu_mit")[0], lies("neu_ohne")[0]
    zeile = PFAD + "\tB2 Stand"
    soll("neu_mit: die Datei steht nur in soll.txt, mit Ablagepfad, Grund 'B2 Stand'", mit_namen("neu_mit") == [("soll.txt", zeile)])
    soll("neu_mit: bleibt +1, Soll +1, ohne Regel -1, sonst wie alt_mit",
         (m["bleibt"], m["Soll"], m["ohne Regel"]) == (a["bleibt"] + 1, a["Soll"] + 1, a["ohne Regel"] - 1)
         and all(m[k] == a[k] for k in ("Ist", "entfernen", "ablegen")))
    soll("neu_ohne: die Datei steht in soll.txt und ablegen.txt, mit Ablagepfad, ohne 'FEHLT IM REPO'",
         mit_namen("neu_ohne") == [("soll.txt", zeile), ("ablegen.txt", zeile)])
    soll("neu_ohne: ablegen +1, Ist -1, ohne Regel -1, Soll wie neu_mit, bleibt und entfernen wie alt_mit",
         (o["ablegen"], o["Ist"], o["ohne Regel"], o["Soll"]) == (a["ablegen"] + 1, a["Ist"] - 1, a["ohne Regel"] - 1, m["Soll"])
         and all(o[k] == a[k] for k in ("bleibt", "entfernen")))
    gegenprobe(("alt_mit", "neu_fehlt", "neu_mit", "neu_ohne"))
elif PHASE == "datiert":
    # Tatsachennotiz, kein Soll: eine erfundene datierte Fassung steht in der Ist-Liste (ablage_soll.py Z. 224-226 der neuen Fassung)
    datiert = PFAD[:-3] + "_2026-10-10.md"
    print("Notiz Voraussetzung: Datei unter docs/projektfuehrung/ %s" % ("ja" if IM_REPO else "nein"))
    lauf("neu_datiert", ist_listen()[0] + [datiert])
    z, listen = lies("neu_datiert")
    for l in LISTEN:
        for x in listen[l]:
            if x.startswith(datiert):
                print("Notiz %s: %s" % (l, x))
    m = lies("neu_mit")[0]
    print("Notiz Zahlen gegen neu_mit: " + ", ".join("%s %+d" % (k, z[k] - m[k]) for k in ("Ist", "Soll", "entfernen", "bleibt", "ablegen", "ohne Regel")))
else:
    soll("Phase alt, fehlt, neu oder datiert", False)
print("ERGEBNIS %s: %d Fehler | Python %s" % (PHASE, len(fehler), sys.version.split()[0]))
sys.exit(1 if fehler else 0)
