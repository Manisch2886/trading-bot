#!/usr/bin/env python3
"""TB-173 Werkzeug (Anhang A): Fable 17a ins Register (Abschnitt 66, R106 zeichengleich, vier Marken, 66.2), Index, Handfelder, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import ast, hashlib, json, os, re, subprocess, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
IDX, JO, BL, DI = P + "REGISTER_INDEX.md", P + "JOURNAL.md", P + "BACKLOG.md", P + "FABLE_DIALOG_INDEX.md"
AUF, BEL = "docs/auftraege/MAC_TB-173_register66_fable17a.md", "docs/belege/TB-173/"
FA = P + "FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md"; FQ = P + "FABLE_ANFRAGE_2026-10-17a_r105c_weg1_elliott_t3.md"; FU = P + "FABLE_UEBERGABE_2026-10-17a_eroeffnung.md"
MD5 = { "docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md": "e222920fc17f72fb7f516d41a6203457", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17a_r105c_weg1_elliott_t3.md": "fae73317801514cd86be1f9101a1c401", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17a_eroeffnung.md": "2d1b9293fc22e8c79a0111655302ad5c" }
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R106)"
TITEL = "## 66. Fable 17a — Registerblock R106 (TB-173)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
H = "research/tb24_haltedauern/"; PROBE, TLE, PH, EPROBE = H + "test_elliott_verdraengung.py", H + "test_listen_erzeuger.py", H + "positionen_holen.py", "docs/belege/TB-171/e_probe.txt"
SHA = {PROBE: "59f6c90bde98a04da20fd52f314399a6e35443cacbfc3e2225d00eab3227d573", TLE: "e196884a152796e4a9ab6e715de70933ebf7614ecf4f38d763eed24d46cda1bf", PH: "b6d1e2d66eae02a8a546cab15649a4100e3c1b2df0a9a668140f23de3a8573db"}
ERG172, M1, M2 = "docs/ERGEBNIS_TB-172_verfahrensmessung_r102d_r92c.md", "docs/belege/TB-172/m1_r102d.txt", "docs/belege/TB-172/m2_r92c.txt"
LESER = { "research/tb24_haltedauern/auswertung.py": 71, "research/faltenplan_neun/embargo_neun.py": 232, "research/mtm_drawdown/grundlage.py": 65, "research/exposure_messung/auswertung.py": 73 }
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; Befunde gehen als Frage an den Verfahrensprüfer, hier nichts entschieden |"
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | zg | Absatzanfang, Kopf der Marke, Zusatz) - R106 (e)
MARKEN = [("65.2", "### 65.2 ", "quelle", "65.2 R105 PRÄZISIERT und ERGÄNZT durch R106 (66.1)", "Fable 17a R106, Unterpunkt (a) präzisiert, Unterpunkte (b) bis (d) ergänzt"),
          ("57.1", "### 57.1 ", "zg", "57.1 R90 ERGÄNZT durch R106 (66.1)", "Fable 17a R106, Unterpunkt (b)"),
          ("61.1", "### 61.1 ", "zg", "61.1 R98 ERGÄNZT durch R106 (66.1)", "Fable 17a R106, Unterpunkt (b)"),
          ("64.1", "### 64.1 ", "**Abnahme nach R98 (d)**", "64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R106 (66.1)", "Fable 17a R106, Unterpunkt (c)")]
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def info(t): OUT.append("info  " + t)
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def shaf(f): return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT); m = sum(l.startswith(("ja ", "NEIN")) for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (m, n)); sys.exit(rc if rc is not None else (1 if n else 0))
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def block():
    """((R-Zeile, Quellenzeile, Z.), Z. Zaun auf, Z. Zaun zu) oder None."""
    z = lies(FA).split("\n")
    if z.count(KOPF_A) != 1: return None
    a = z.index(KOPF_A) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [(i + 1, z[i]) for i in range(a + 1, e) if z[i]]; soll = ["R106 — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for (_, l), s in zip(b, soll)] != soll: return None
    return (b[0][1], b[1][1], b[0][0]), a + 1, e + 1
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m):
    """Index der Einfuegestelle (nach dieser Zeile) oder None. Bei einem Absatz: nach dem Absatz und nach den Markenpaaren, die schon dahinter stehen."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any("R106" in z[i] for i in range(a, e)): return None
    if m[2] == "zg": k = [i for i in range(a, e) if z[i] == ZG][-1:]
    elif m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    else:
        k = [i for i in range(a, e) if z[i].startswith(m[2])]
        if len(k) == 1:
            while k[0] + 3 < e and z[k[0] + 1] == "" and z[k[0] + 2].startswith("> ⭐ ") and z[k[0] + 3] == ZG: k[0] += 3
    return k[0] + 1 if len(k) == 1 else None
def markenzeilen(m, datum): return ["", "> ⭐ **%s** (%s, TB-173, %s)." % (m[3], m[4], datum), ZG]
def zeile(z, s, nach=None):
    """Zeilennummern (1-basiert) der Zeilen, die genau s sind."""
    return [i + 1 for i, l in enumerate(z) if l == s]
def funktion_von(z, n):
    """Name der Funktion, in der Zeile n (1-basiert) steht."""
    for i in range(n - 1, -1, -1):
        mm = re.match(r"def (\w+)\(", z[i])
        if mm: return mm.group(1)
    return None
def lesestellen(f):
    """Leseaufrufe (open ohne w, read_csv, shutil.copy, os.symlink) mit der Wurzel ihres Pfads; Namen innerhalb der Funktion aufgeloest."""
    baum = ast.parse(lies(f)); aus = []
    def wurzel(x, zuw, tiefe=0):
        if tiefe > 5: return "?"
        if isinstance(x, ast.Call) and ast.unparse(x.func) == "os.path.join" and x.args: return wurzel(x.args[0], zuw, tiefe + 1)
        if isinstance(x, ast.Call) and ast.unparse(x.func) == "io.StringIO": return "Speicher"
        if isinstance(x, ast.BinOp): return wurzel(x.left, zuw, tiefe + 1)
        if isinstance(x, ast.Name) and x.id in zuw: return wurzel(zuw[x.id], zuw, tiefe + 1)
        return ast.unparse(x)
    def flach(w):
        st = list(ast.iter_child_nodes(w))
        while st:
            n = st.pop()
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)): continue
            yield n; st.extend(ast.iter_child_nodes(n))
    for fn in [n for n in ast.walk(baum) if isinstance(n, ast.FunctionDef)] + [baum]:
        zuw = {}
        for n in flach(fn):
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name): zuw.setdefault(n.targets[0].id, n.value)
        for n in flach(fn):
            if not isinstance(n, ast.Call) or not n.args: continue
            nm = ast.unparse(n.func)
            if nm == "open":
                modus = n.args[1] if len(n.args) > 1 else next((k.value for k in n.keywords if k.arg == "mode"), None)
                if modus is not None and isinstance(modus, ast.Constant) and "w" in str(modus.value): continue
            elif not (nm.endswith("read_csv") or nm in ("shutil.copy", "os.symlink")): continue
            aus.append((n.lineno, nm, wurzel(n.args[0], zuw)))
    return sorted(set(aus))
def stand_kopf():
    z = lies(IDX).split("\n"); return z, [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def md5cmd():
    for f in (FA, FQ, FU): p(md5f(f) == MD5[f], "md5 %s = %s" % (f, MD5[f]))
    ende()
def voraussetzung_c():
    """R106 (c), Voraussetzung, nur das Ob: Wachen in Pruefung 1 eingeschaltet; Kursabschnitt selbst gebildet, keine Datei ausserhalb des Repos."""
    for f, s in SHA.items(): p(shaf(f) == s, "R106 (c) Stand: %s sha256 %s… (Stand der Probe TB-171)" % (f, s[:8]))
    pr, tl, ph = lies(PROBE).split("\n"), lies(TLE).split("\n"), lies(PH).split("\n")
    z1 = [i + 1 for i, l in enumerate(pr) if l.startswith('    r = tle.lauf(bot, SEED, False, "", tg)')]
    p(len(z1) == 1 and any('": 1 Erzeuger mit Schranke' in pr[j] for j in range(z1[0], min(z1[0] + 3, len(pr)))),
      "R106 (c) Voraussetzung, Wachen: Pruefung 1 (mit Schranke) ruft den Erzeuger mit leerem Modus (%s Z. %s)" % (PROBE, z1))
    ers = [i + 1 for i, l in enumerate(tl) if "ph.wache_zeilen =" in l or "ph.wache_trades =" in l]
    p(ers and all(tl[n - 1].startswith(('    if "wache1_aus" in modus:', '    if "wachen_aus" in modus:')) for n in ers),
      "R106 (c) Voraussetzung, Wachen: %s ersetzt die Wachen nur in den Modi wache1_aus/wachen_aus (Z. %s)" % (TLE, ers))
    wz, wt = zeile(ph, "    wache_zeilen(all_data)"), zeile(ph, "    wache_trades(trades, handelbar)")
    p(len(wz) == 1 and len(wt) == 1 and funktion_von(ph, wz[0]) == "main" and funktion_von(ph, wt[0]) == "main",
      "R106 (c) Voraussetzung, Wachen: %s main ruft wache_zeilen Z. %s und wache_trades Z. %s ohne Bedingung (Einrueckung 4)" % (PH, wz, wt))
    dz, dt = zeile(ph, "def wache_zeilen(all_data):"), zeile(ph, "def wache_trades(trades, handelbar):")
    tz = "\n".join(ph[dz[0]:dt[0] - 1]) if dz and dt else ""; tt = "\n".join(ph[dt[0]:dt[0] + 16]) if dt else ""
    p(len(dz) == 1 and len(dt) == 1 and "R86 (d)" in tz and "R86 (d)" in tt and "R87 (c)" in tt, "R106 (c) Voraussetzung, Wachen: wache_zeilen (Z. %s) nach R86 (d), wache_trades (Z. %s) nach R86 (d) und R87 (c)" % (dz, dt))
    ep = lies(EPROBE).rstrip("\n").split("\n") if os.path.exists(EPROBE) else []
    for b in ("elliott_wave", "elliott_wave_stocks"):
        e1 = [l for l in ep if l.startswith("ja    %s: 1 Erzeuger mit Schranke: rc 0" % b)]; e2 = [l for l in ep if l.startswith("ja    %s: 2 Gegenprobe 40.7" % b) and "(R87 (c))" in l]
        p(len(e1) == 1 and len(e2) == 1, "R106 (c) Voraussetzung, Beleg %s, %s: Pruefung 1 ja (rc 0); Pruefung 2 ja, Wache R87 (c) beisst ohne Schranke" % (EPROBE, b))
    p(ep[-2:] == ["Ergebnis: 16 von 16 bestanden", "rc 0"], "R106 (c) Beleg %s: 16 von 16, rc 0" % EPROBE)
    ks = all(any(l.startswith(s) for l in pr) for s in ("def bauplan():", "def einsetzen(bot, d):", "tle.snapshot = snapshot")) and pr.count("    df.to_csv(f, index=False)") == 1
    ks2 = any("r = np.random.default_rng(seed + k)" in l for l in tl) and any('df.to_csv(os.path.join(d, "data", "%s_%s.csv" % (s, tf)), index=False)' in l for l in tl)
    p(ks and ks2, "R106 (c) Voraussetzung, Kursabschnitt: die Probe bildet ihn selbst (bauplan, einsetzen) in der Kopie des Test-Snapshots; der Snapshot entsteht aus default_rng(seed + k) im Temp-Ordner")
    ls = lesestellen(PROBE) + lesestellen(TLE); erlaubt = ("d", "z", "t", "tempfile.mkdtemp()", "WURZEL", "tle.WURZEL", "Speicher")
    lp = lesestellen(PROBE)
    for n, nm, w in ls: info("Lesestelle %s Z. %d: %s(…) Wurzel %s" % ("Probe" if (n, nm, w) in lp else "tle", n, nm, w))
    tmp = any("tempfile.mkdtemp()" in l for l in pr) and any("tempfile.TemporaryDirectory()" in l for l in tl)
    p(ls and all(w in erlaubt for _, _, w in ls) and tmp, "R106 (c) Voraussetzung, Lesen: %d Lesestellen in Probe und tle, Wurzel nur Temp-Ordner der Probe (d, z, t, tempfile.mkdtemp()), Repo (WURZEL) oder Speicher" % len(ls))
    lit = [n.value for f in (PROBE, TLE) for n in ast.walk(ast.parse(lies(f))) if isinstance(n, ast.Constant) and isinstance(n.value, str) and (n.value.startswith(("/", "~")) or "/Users/" in n.value or "/home/" in n.value)]
    roh = [x for f in (PROBE, TLE) for x in ("expanduser", '"HOME"', 'WURZEL, "data"') if x in lies(f)]
    kind = any('env=dict(os.environ, TB36_BASE_DIR=d)' in l for l in tl) and any('mso.DATA_DIR = os.path.join(d, "data")' in l for l in tl)
    p(not lit and not roh and kind, "R106 (c) Voraussetzung, Lesen: kein absoluter Pfad, kein expanduser/HOME, kein data/ des Repos; Kindprozess mit TB36_BASE_DIR und DATA_DIR im Temp-Ordner (Teilmessung am Code; e_probe.txt fuehrt keine Lesespur)")
def voraussetzung():
    for f in (FA, FQ, FU): p(verfolgt_gleich(f) and md5f(f) == MD5[f], "R56 (b)/0a-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5[f]))
    b = block(); p(b is not None, "Registerblock 17a: genau R106 und Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[1], b[2]) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 65. ") for l in z) == 1 and not any(l.startswith("## 66. ") for l in z) and not re.search(r"\bR106\b", reg), "Register: 65 da, 66 nicht; R106 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for m in MARKEN: i = einfuege(z, m); p(i is not None, "Ort %s: Einfuegestelle nach Z. %s eindeutig, R106 dort noch nicht genannt" % (m[0], i if i else "?"))
    voraussetzung_c()
    m1 = lies(M1).rstrip("\n").split("\n") if os.path.exists(M1) else []; m2 = lies(M2).rstrip("\n").split("\n") if os.path.exists(M2) else []
    p(os.path.exists(ERG172) and all(("URTEIL R102 (d) %s: ja" % b) in m1 for b in ("rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout")) and m1[-1:] == ["rc 0"],
      "TB-172: %s und %s: R102 (d) ja bei rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout; rc 0" % (ERG172, M1))
    p(any(l.startswith("URTEIL R92 (c): erfüllt (150 von 150") for l in m2) and m2[-1:] == ["rc 0"], "TB-172: %s: R92 (c) erfüllt (150 von 150), rc 0" % M2)
    for f, n in sorted(LESER.items()):
        lz = lies(f).split("\n") if os.path.exists(f) else []; p(len(lz) >= n and "_positionen.csv" in lz[n - 1], "BACKLOG-Leser: %s Z. %d liest <bot>_positionen.csv" % (f, n))
    zi, k = stand_kopf(); p(len(k) == 1 and "Abschnitte 0–65" in zi[k[0]], "Index-Kopf Z. %s nennt 0–65" % (k[0] + 1 if k else "?"))
    bl = lies(BL); p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl.split("\n")) == 1, "BACKLOG: Rang 1 (Stand TB-172) genau einmal")
    p(sum(l.startswith("| 65 aus 16c |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-170 (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and not any(l.startswith("## 17. ") for l in zi), "Index: Zeile 65, Pflegezeile TB-170, Pflege-Anker je genau einmal; kein Abschnitt 17")
    p(not any(l.startswith("| 17a |") for l in lies(DI).split("\n")), "Dialog-Index: 17a noch nicht")
    kk = kennungen(); p(max(kk) == "FI" and "FJ" not in kk, "Journal: hoechste FI, naechste FJ frei")
    ende()
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    b = block(); p(b is not None and md5f(FA) == MD5[FA], "Quelle md5 %s, Registerblock R106" % MD5[FA])
    p(not any(l.startswith("## 66. ") for l in z) and z[-1] == "" and z[-2] != "", "66 noch nicht im Register; endet mit einer Leerzeile")
    einf = [(einfuege(z, m), m) for m in MARKEN]; p(all(i is not None for i, _ in einf), "4 Einfuegestellen eindeutig")
    k = karte(); p(k is not None, "Karte TB-173 gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    (r, q, _), za, ze = b
    kopf = ("Reines Eintragen von Registertext, Bauart wie 65. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R106)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Fragen, Kenntnisse, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.a und die Übergabe 17.10.a (beide seit `%s`). Marken nach R106 (e). "
            "Karte des Betreibers (Auftrag TB-173, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-173.") % (FA, MD5[FA], format(os.path.getsize(FA), ",").replace(",", " "), za, ze, s0, s0, k, datum)
    kette = ("**Kette:** Marken nach R106 (e): 65.2 (R105), Unterpunkt (a) präzisiert, Unterpunkte (b) bis (d) ergänzt; 57.1 (R90) und 61.1 (R98), Unterpunkt (b); 64.1, Absatz „Abnahme nach R98 (d)“, Unterpunkt (c). "
             "Ohne Marke: 56.4 (R87), 55.4 (R81), 54.2 (R75), 48.14 (R46); 65.3; Abschnitt 10. Voraussetzung in (c) gemessen: 66.2 (a). Stand t3_supertrend nach (d): BACKLOG Rang 1.")
    neu = ["", TITEL, "", kopf, "", "### 66.1 " + titel(r), "", "> " + r, "> " + q, "", kette, ""]
    neu += ["### 66.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-173), Zeilen wörtlich:" % beleg, ""] + ["    " + l for l in vb] + ["",
        ("(a) R106 (c), Voraussetzung (nur das Ob), gemessen oben (Zeilen „R106 (c)“) am Code der Probe `%s` (sha256 `%s…`), an `%s` und `%s` (Stand der Probe TB-171) und am Beleg `%s`: "
         "In der Prüfung mit Schranke (Prüfung 1) ruft die Probe den Erzeuger mit leerem Modus; die Wachen nach R86 (d) (`wache_zeilen`, `wache_trades`) und R87 (c) (`wache_trades`) ersetzt der Test nur in den Modi „wache1_aus“ und „wachen_aus“, "
         "der Erzeuger ruft beide ohne Bedingung — eingeschaltet: ja. Die Probe bildet den Kursabschnitt selbst (`bauplan`, `einsetzen`) in der Kopie des Test-Snapshots, der aus Zufallszahlen mit festem Seed im Temp-Ordner entsteht; "
         "gelesen werden nur Dateien dieses Temp-Ordners und des Repos, keine Datei ausserhalb — ja. **Teilmessung:** am Code, nicht an einer Lesespur des Laufs (`e_probe.txt` führt keine); den Code der Bots im Kindprozess verfolgt die Messung nicht "
         "(dort nur `TB36_BASE_DIR` und `DATA_DIR` auf den Temp-Ordner gesetzt).") % (PROBE, SHA[PROBE][:8], TLE, PH, EPROBE), "",
        ("(b) Tatsachennotiz TB-172 (`%s`; Belege `%s`, `%s`): R102 (d) ja bei rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout (Indikatorwerte aus Zeilen vor dem Horizontbeginn, nur das Ob, durch Lesen des Codes); "
         "R92 (c) erfüllt (150 von 150 Aktien-Dateien, nur die Form von open_time). Der Befund zu R102 (d) geht als Frage an den Verfahrensprüfer; hier nichts entschieden.") % (ERG172, M1, M2), "",
        "(c) R56 (b): Übergabe, Anfrage und Antwort 17.10.a liegen seit `%s` im Repo." % s0, ""]
    if probe: print("\n".join(neu)); ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m, datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s**" % m[3])] for m in MARKEN}
    json.dump({"marken": [[m[0], m[3], (mz[m[0]] or [0])[0]] for m in MARKEN], "abschnitt_66": r2.index(TITEL) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: 4 Marken Z. %s; Abschnitt 66 Z. %d" % (sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "R106 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al):] == neu, "append-only bis auf die vier Marken (je Leerzeile, Marke, Zeichengleich-Zeile)")
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 66. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) == 4 and all(m[2] for m in mk), "Abschnitt 66 in genau einer Teildatei: T%s; 4 Marken mit Zeile" % teil); T = str(teil[0]) if teil else "?"
    z, k = stand_kopf(); rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–65" in z[k[0]], "Kopf genau einmal, nennt 0–65"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–65", "Abschnitte 0–66")
    i = [j for j, l in enumerate(z) if l.startswith("| 65 aus 16c |")]
    if p(len(i) == 1, "Zeile 65 genau einmal"): z.insert(i[0] + 1, "| 66 aus 17a | %s | R106 (66.1); 66.2 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 17. Die Marken aus Fable 17a (TB-173)", "", "Alle 4 Marken, die TB-173 nach R106 (e) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-173/r_daten.json`.", "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, T) for o, kp, n in sorted(mk, key=lambda m: m[2])] + [""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 17. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 17"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-170 (")]
    if p(len(j) == 1, "Pflegezeile TB-170 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-170 (", "In TB-170 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-173 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-173 (`index`); 66 (R106) kommt zu T%s; neuer Abschnitt 17 (4 Marken). Der Kopf mischt weiter Stände (BACKLOG Rang 1, TB-170)." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"17a": {"frage": lies(FQ).split("\n")[0].split(" — ", 1)[1].strip(),
                       "entscheidung": "Frage 1 einverstanden: TB-171 schliesst R105 (c) Weg 1 bei elliott_wave und elliott_wave_stocks; Kenntnis 2 anders: t3_supertrend Weg 1 oder eine Notiz, die use_t3_exit und den Gleichstand mit Fundstelle schliesst (R106)",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17a geschrieben: %s" % ziel)
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    le = ", ".join("`%s` Z. %d" % (f, n) for f, n in sorted(LESER.items()))
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-172"):
        z[a[0]] = z[a[0]][:-2] + (" · Register 66 (Fable 17a: R106 Lesart „spätere Welle“, Test-Snapshot, Stand) mit TB-173 (%s, Journal %s): **R105 (c) Weg 1 bei `elliott_wave` und `elliott_wave_stocks` geschlossen** (R106 (c); Voraussetzung gemessen, 66.2 (a), Teilmessung am Code)"
            "; **Handelscode, eigener Punkt, vor dem Tag:** `t3_supertrend` nach R106 (d) — Weg 1 (Fall auf dem Test-Snapshot herbeiführen: Einstieg vor dem Tag, Position über den Tag offen, danach ein zweites Kreuzen nach oben, z. B. über den Gleichstand mit konstanten Kursen; ohne Schranke fehlt es oder die Wache nach R87 (c) endet mit 2, mit Schranke erscheint es; 40.7; Bau-Helfer und frischer Gegenleser) "
            "oder eine Tatsachennotiz mit Fundstelle, dass `use_t3_exit` im Lauf und bei der Neuerzeugung nie False ist und der Gleichstand keinen Einstieg ohne Ausstieg bildet"
            "; R102 (d)-Befund aus TB-172 (ja bei rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout; 66.2 (b)) als Frage an den Verfahrensprüfer mit der nächsten Anfrage"
            "; vor der Neuerzeugung der Listen vier Leser auf `<bot>_alle_trades.csv` umstellen (am HEAD gemessen): %s; `research/exposure_messung/auswertung.py` liest dabei die eigene Liste aus `research/exposure_messung/daten/` (von `bot_lauf.py`), ob sie zur Neuerzeugung gehört, ist offen |") % (datum, kenn, le)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-173: " % neu), "Kopfzeile ## %s — TB-173: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["md5"]: md5cmd()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
