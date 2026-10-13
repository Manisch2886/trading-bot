# TB-159 Werkzeug (Anhang B des Auftrags): probe, kopie, einbau, vergleich, basis, backlog, kennung, journal. Nur Standardbibliothek, Python 3.9.
# Liest die Stuecke wortlich aus dem Auftrag (Anhang A); jeder Anker muss genau einmal als ganze Zeile vorkommen, sonst wird nichts geschrieben.
import os, re, shutil, subprocess, sys, time
AUFTRAG = "docs/auftraege/MAC_TB-159_agenten_aus.md"
PLAN = [['A1', 'config/agenten_aus.txt', 'neu', None], ['A2', 'shared/test_agenten_aus.py', 'neu', None], ['A3', 'shared/claude_client.py', 'danach', 'MODEL_HAIKU = "claude-haiku-4-5-20251001"'], ['A4a', 'shared/daily_interpreter.py', 'ersetzen', 'from claude_client import call_claude, MODEL_HAIKU'], ['A4b', 'shared/daily_interpreter.py', 'davor', '    user_message = f"Strategie: {strategy_name}\\n\\nTages-Zusammenfassung:\\n{summary_text}"'], ['A5a', 'shared/market_context_agent.py', 'ersetzen', 'from claude_client import call_claude'], ['A5b', 'shared/market_context_agent.py', 'davor', '    if not symbols:'], ['A6a', 'shared/portfolio_interpreter_agent.py', 'ersetzen', 'from claude_client import call_claude, MODEL_SONNET'], ['A6b', 'shared/portfolio_interpreter_agent.py', 'davor', '    if not overview_text or not overview_text.strip():']]
TESTS = ["shared/test_empfehlung_format.py", "shared/test_agent2_kapitalmass.py", "shared/test_agent2_zielfunktion.py"]
NEU_TEST = "shared/test_agenten_aus.py"
OHNE = ("docs/", "data/", "snapshots/")  # Kopie ohne Doku und ohne die beiden grossen Datenordner (zusammen rund 420 MB)
BL, BL_ANKER, BL_ZEILE = "docs/projektfuehrung/BACKLOG.md", "## 5 — Nach TB-30b", "A7"
JO, JO_ANKER = "docs/projektfuehrung/JOURNAL.md", "## Wiederkehrende Lehren"
_ST = {}


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def schreib(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def stuecke():
    if _ST:
        return _ST
    z, s = lies(AUFTRAG).split("\n"), _ST
    for i, l in enumerate(z):
        m = re.match(r"^#### (A\d+[a-z]?) — ", l)
        if m:
            a = next(j for j in range(i + 1, len(z)) if z[j].startswith("```") and len(z[j]) > 3)
            assert m.group(1) not in s, "Stueck doppelt: " + m.group(1)
            s[m.group(1)] = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
    return s


def zeilen(t):
    return t[:-1].split("\n")


def entwurf():
    st, fehler, neu, soll = stuecke(), [], {}, {}
    for sid, pfad, art, anker in PLAN:
        if sid not in st:
            fehler.append("%s fehlt im Auftrag" % sid)
            continue
        tz = zeilen(st[sid])
        if art == "neu":
            if os.path.exists(pfad):
                fehler.append("%s gibt es schon" % pfad)
            neu[pfad] = st[sid]
            soll[pfad] = [len(tz), 0]
            print("%s %s neu · %d Zeilen" % (sid, pfad, len(tz)))
            continue
        z = (neu[pfad] if pfad in neu else lies(pfad)).split("\n")
        n = z.count(anker)
        print("%s %s %s · Anker Vorkommen %d%s" % (sid, pfad, art, n, " · Z. %d" % (z.index(anker) + 1) if n == 1 else ""))
        if n != 1:
            fehler.append("%s Anker %d-mal" % (sid, n))
            continue
        i = z.index(anker)
        if art == "ersetzen":
            z[i:i + 1] = tz
        elif art == "davor":
            z[i:i] = tz
        else:
            z[i + 1:i + 1] = tz
        neu[pfad] = "\n".join(z)
        s = soll.setdefault(pfad, [0, 0])
        s[0] += len(tz)
        s[1] += 1 if art == "ersetzen" else 0
    for p, t in neu.items():
        if p.endswith(".py"):
            try:
                compile(t, p, "exec")
            except SyntaxError as e:
                fehler.append("%s nicht uebersetzbar: %s" % (p, e))
    return neu, soll, fehler


def kopie(ziel):
    if os.path.exists(ziel):
        print("NEIN: %s gibt es schon - nichts kopiert" % ziel)
        return 3
    ls = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"], capture_output=True, check=True).stdout.decode("utf-8")
    n = b = 0
    for p in ls.split("\0"):
        if not p or p.startswith(OHNE) or not os.path.isfile(p):
            continue
        os.makedirs(os.path.join(ziel, os.path.dirname(p)), exist_ok=True)
        shutil.copy2(p, os.path.join(ziel, p))
        n, b = n + 1, b + os.path.getsize(p)
    print("kopie: %d verfolgte Dateien ohne docs/, data/, snapshots/, %d B, nach %s" % (n, b, ziel))
    return 0


def einbau(probe):
    neu, soll, fehler = entwurf()
    for p in sorted(soll):
        print("Soll numstat %s %d / %d" % (p, soll[p][0], soll[p][1]))
    if fehler:
        print("NEIN: " + "; ".join(fehler) + " - nichts geschrieben")
        return 3
    if not probe:
        for p, t in neu.items():
            schreib(p, t)
    print("probe: alles gleich, nichts geschrieben" if probe else "einbau: %d Dateien geschrieben" % len(neu))
    return 0


def vergleich():
    st, ok = stuecke(), True
    for sid, pfad, art, anker in PLAN:
        t, z = lies(pfad), lies(pfad).split("\n")
        if art == "neu":
            g = t == st[sid]
        elif art == "ersetzen":
            g = z.count(anker) == 0 and z.count(zeilen(st[sid])[0]) == 1
        else:
            block = zeilen(st[sid])
            i = z.index(anker) if z.count(anker) == 1 else -1
            k = i - len(block) if art == "davor" else i + 1
            g = i >= 0 and z[k:k + len(block)] == block and t.count("\n".join(block)) == 1
        ok = ok and g
        print("%s %s · %s" % (sid, pfad, "GLEICH" if g else "NEIN"))
    return 0 if ok else 3


def basis(name, aus, datei):
    liste = TESTS + ([NEU_TEST] if name in ("nachher", "kopie") else [])
    if datei not in liste:
        print("NEIN: %s gehoert nicht zum Lauf %s (%s)" % (datei, name, ", ".join(liste)))
        return 2
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    env.pop("ANTHROPIC_API_KEY", None)
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "-B", datei], capture_output=True, text=True, timeout=540, env=env)
        rc, ausgabe = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        rc, ausgabe = "Zeitgrenze 540 s", ""
    z = ausgabe.rstrip("\n").split("\n")
    zeile = "Lauf %s · %s · %s · %s · rc %s · %.1f s · [OK ] %d · [FEHLER] %d · letzte Zeile: %s" % (
        name, sys.executable, time.strftime("%d.%m.%Y %H:%M:%S"), datei, rc, time.time() - t0,
        sum("[OK ]" in l for l in z), sum("[FEHLER]" in l for l in z), z[-1][:200])
    with open(aus, "a", encoding="utf-8") as f:
        f.write(zeile + "\n")
    print(zeile)
    return 0 if rc == 0 else 1


def backlog(probe):
    z, zeile = lies(BL).split("\n"), zeilen(stuecke()[BL_ZEILE])[0]
    b = [z.count(BL_ANKER) == 1, z.count(zeile) == 0, "| **K4v** |" not in "\n".join(z)]
    if b[0]:
        i = z.index(BL_ANKER)
        b.append(z[i - 1] == "" and z[i - 2].startswith("| "))
    print("Anker einmal: %s · Zeile neu: %s · K4v frei: %s · Tabellenende davor: %s" % tuple(["ja" if x else "nein" for x in b] + ["?"] * (4 - len(b))))
    if not all(b) or len(b) < 4:
        print("NEIN - nichts geschrieben")
        return 3
    if not probe:
        z.insert(i - 1, zeile)
        schreib(BL, "\n".join(z))
    print("%s: Zeile als Z. %d" % ("probe" if probe else "eingefuegt", i))
    return 0


def naechste():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
    m = max(k)
    return m, (m[0] + chr(ord(m[1]) + 1)) if m[1] != "Z" else chr(ord(m[0]) + 1) + "A"


def kennung(aus):
    letzte, nx = naechste()
    t = "Kennung %s (naechste freie; hoechste vorhandene %s)" % (nx, letzte)
    schreib(aus, t + "\n")
    print(t)
    return 0


def journal(block, probe):
    b, t = lies(block).rstrip("\n").split("\n"), lies(JO)
    z, k = t.split("\n"), re.findall(r"^## ([A-Z]{2}) — TB-", t, re.M)
    letzte, KENNUNG = naechste()
    i = z.index(JO_ANKER) if z.count(JO_ANKER) == 1 else -1
    c = [("Block beginnt mit '## %s — TB-159: ' (naechste freie nach %s)" % (KENNUNG, letzte), b[0].startswith("## %s — TB-159: " % KENNUNG)),
         ("keine weitere '## '-Zeile im Block", sum(l.startswith("## ") for l in b) == 1),
         ("kein '---' im Block", "---" not in b),
         ("Kennung %s noch frei" % KENNUNG, KENNUNG not in k),
         ("Anker einmal", i >= 0),
         ("vor dem Anker '---' und Leerzeile", i >= 2 and z[i - 1] == "" and z[i - 2] == "---")]
    for n, g in c:
        print("%s: %s" % (n, "ja" if g else "nein"))
    if not all(g for _, g in c):
        print("NEIN - nichts geschrieben")
        return 64
    if not probe:
        z[i - 1:i - 1] = [""] + b + ["", "---"]
        schreib(JO, "\n".join(z))
    print("%s: Kennung %s, %d Zeilen Block" % ("probe" if probe else "eingefuegt", KENNUNG, len(b)))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 3 and a[-2] == "--in":
        stuecke()
        a, wurzel = a[:-2], a[-1]
        if a[0] == "basis" and len(a) == 4:
            a[2] = os.path.abspath(a[2])
        os.chdir(wurzel)
    if len(a) == 2 and a[0] == "kopie":
        sys.exit(kopie(a[1]))
    if len(a) == 2 and a[0] == "kennung":
        sys.exit(kennung(a[1]))
    if a == ["probe"]:
        sys.exit(einbau(True))
    if a == ["einbau"]:
        sys.exit(einbau(False))
    if a == ["vergleich"]:
        sys.exit(vergleich())
    if len(a) == 4 and a[0] == "basis" and a[1] in ("vorher", "nachher", "kopie"):
        sys.exit(basis(a[1], a[2], a[3]))
    if a in (["backlog"], ["backlog", "--probe"]):
        sys.exit(backlog(len(a) == 2))
    if len(a) in (2, 3) and a[0] == "journal" and a[2:] in ([], ["--probe"]):
        sys.exit(journal(a[1], len(a) == 3))
    print("Aufruf: probe | einbau | vergleich | basis vorher|nachher|kopie <beleg> <testdatei> [--in <wurzel>] | kopie <ziel> | backlog [--probe] | kennung <datei> | journal <block> [--probe]")
    sys.exit(2)
