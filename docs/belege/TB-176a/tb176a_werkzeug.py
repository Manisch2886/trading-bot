#!/usr/bin/env python3
"""TB-176a Werkzeug (Anhang A): Fable 17c ins Register (Abschnitt 68, R108 zeichengleich, neun Marken, 68.2) und in die S-B1-Vorregistrierung (Nachtrag 10a.5, Marke an 10a.2);
Index, Handfelder; Voraussetzungen, Nachher-Pruefung E2, Kennung, BACKLOG, Journal. Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | nachher2 | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, json, os, re, subprocess, sys
P = "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-176a/"
REG, IDX, DI, SB1 = "docs/VORREGISTRIERUNG_neuselektion.md", P + "REGISTER_INDEX.md", P + "FABLE_DIALOG_INDEX.md", "docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md"
AUF, QU = "docs/auftraege/MAC_TB-176a_register68_fable17c_leser.md", "data_sicherung/steuernder_chat_tmp/f17c/"
FA = P + "FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md"
FQ = P + "FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md"
FU = P + "FABLE_UEBERGABE_2026-10-17c_eroeffnung.md"
MD5F = {"docs/projektfuehrung/FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md": "a2b38226f683d8d106a5dec61fa5f325", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17c_r101_sb1_sammler_t3_embargo.md": "0a559c880aa422ca0d77f03c5aa240bc", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17c_eroeffnung.md": "db41d912f05314a47dcc0e501c3aed5a"}
CODE = {"research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/tb24_haltedauern/auswertung.py": "c15e6375520e1aeccc41ce152ca3b870", "research/tb24_haltedauern/haltedauer_kern.py": "60942de99b323fa472ae25478a5a6836", "research/tb24_haltedauern/live_haltedauern.py": "7d21a66cd3173a99adff2c9c1346c815", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/test_haltedauer_kern.py": "a482804dde0c24499cef3d972995bb2a", "research/faltenplan_neun/embargo_neun.py": "b93af14604112c427ab1a3f1606fccc6", "research/faltenplan_neun/test_faltenplan_neun.py": "ae43038a02e7b4ad603c116f1683ffe0", "research/mtm_drawdown/grundlage.py": "81cf1c93243a8248b96cf072e07fc289", "research/mtm_drawdown/messung.py": "00eb23079f1b92532f48f099f74dbe2f", "research/mtm_drawdown/test_mtm_kern.py": "80f1511a18d26a61537748c2739d0d79", "research/wf_kapital_dd/messung.py": "94c091f4c4e13ff4aa2e867dd4fd4fa5"}
NEU_E2 = {"research/tb24_haltedauern/auswertung.py": "9de89e6d302454686f490e151237313011993150f2a120acc0bf879e5331d14b", "research/faltenplan_neun/embargo_neun.py": "f35119ba4b89494d211023c598835640d179f5586c566bc732e5a77c49cc6348"}
PROBE_E2, PSHA = BEL + "tb176a_probe_leser.py", "e99c4664e79ac36a756ab3bce04e0a9c0290a265e8b7249553518555323b8cf0"
STAND_D = "7fe6342"
BOTS = ["elliott_wave", "elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion", "t3_supertrend", "turtle_soup_crypto", "turtle_soup_stocks", "volatility_breakout", "volatility_breakout_crypto"]
RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R108)"
TITEL = "## 68. Fable 17c — Registerblock R108 (TB-176a)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | zg | ende, Kopf der Marke, Zusatz) - R108 (f); folgende Marken-Tripel am Ort werden uebersprungen
MARKEN = [("62.2", "### 62.2 ", "quelle", "62.2 R101 ERGÄNZT und BERICHTIGT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (a): ERGÄNZT zu (a) bis (c), BERICHTIGT zu (a) („lies“)"),
          ("16.4", "### 16.4 ", "ende", "16.4 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (b)"),
          ("16.6", "### 16.6 ", "zg", "16.6 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (c)"),
          ("16.8", "### 16.8 ", "ende", "16.8 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (b)"),
          ("29.3", "### 29.3 ", "ende", "29.3 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (d)"),
          ("37.5", "### 37.5 ", "ende", "37.5 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (d)"),
          ("41.3 C2", "### 41.3 ", "zg", "41.3 C2 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (c)"),
          ("66.1", "### 66.1 ", "quelle", "66.1 R106 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkt (e)"),
          ("67.1", "### 67.1 ", "quelle", "67.1 R107 ERGÄNZT durch R108 (68.1)", "Fable 17c R108, Unterpunkte (b) bis (e)")]
MARKE_SB1 = "S-B1 10a.2 ERGÄNZT durch 10a.5"
OHNE = "15.4, 17.1, 24.3, 37.3, 38.5, 40.7, 41.1, 41.2, 58.4, 58.5, 62.5, 66.2, Abschnitt 10, S-B1 2, 3.2, 9, 10a.4"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def info(t): OUT.append("info  " + t)
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (sum(not l.startswith("info") for l in OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def beleg(n): return lies(BEL + n).rstrip("\n").split("\n") if os.path.exists(BEL + n) else [""]
def block():
    """((R-Zeile, Quellenzeile), Z. Zaun auf, Z. Zaun zu) oder None."""
    z = lies(FA if os.path.exists(FA) else QU + os.path.basename(FA)).split("\n")
    if z.count(KOPF_A) != 1: return None
    a = z.index(KOPF_A) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [z[i] for i in range(a + 1, e) if z[i]]; soll = ["R108 — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for l, s in zip(b, soll)] != soll: return None
    return (b[0], b[1]), a + 1, e + 1
def wortlaut(r):
    m = re.findall(r"Wortlaut: „(.*?)“ Der Grund trägt", r); return m[0] if len(m) == 1 else None
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m, frei="R108"):
    """Index der Einfuegestelle (vor dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any(frei in z[i] for i in range(a, e)): return None
    if m[2] == "zg": k = [i for i in range(a, e) if z[i] == ZG][-1:]
    elif m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    else:
        j = e - 1
        while j > a and z[j] in ("", "---"): j -= 1
        k = [j] if j > a else []
    if len(k) != 1: return None
    k = k[0]
    while k + 3 < e and z[k + 1] == "" and z[k + 2].startswith("> ⭐ ") and z[k + 3] == ZG: k += 3
    return k + 1
def c2_ok(z, i):
    c2 = [n for n, l in enumerate(z) if l.startswith("**C2 (b) — Deckel")]; c3 = [n for n, l in enumerate(z) if l.startswith("**C3 (c) — ")]
    return len(c2) == 1 and len(c3) == 1 and c2[0] < i < c3[0]
def markenzeilen(kopf, zusatz, datum): return ["", "> ⭐ **%s** (%s, TB-176a, %s)." % (kopf, zusatz, datum), ZG]
def sb1_stellen(s):
    """(Einfuegestelle Marke 10a.2, Einfuegestelle 10a.5) oder (None, None)."""
    if any(l.startswith("### 10a.5") for l in s) or any("R108" in l for l in s) or sum(l.startswith("## 11. ") for l in s) != 1: return None, None
    a, e = unterabschnitt(s, "### 10a.2 "); b, f = unterabschnitt(s, "### 10a.4 ")
    if a is None or b is None or not s[f].startswith("## 11. "): return None, None
    return einfuege(s, (None, "### 10a.2 ", "ende")), einfuege(s, (None, "### 10a.4 ", "ende"))
def mess_d():
    """R108 (d): Werte des Startkapitals im Register am Stand 7fe6342 und in den neun equity_simulation.py (nur Messung)."""
    r = git("show", STAND_D + ":" + REG); z = r.stdout.decode("utf-8").split("\n") if r.returncode == 0 else []
    kopf, reg = "?", []
    for i, l in enumerate(z):
        if l.startswith("## ") or l.startswith("### "): kopf = l.split(" ")[1]
        for m in re.finditer(r"(Startkapital|STARTING_CAPITAL)[`\s  =:]*\d[\d\s  .,_]*", l): reg.append((i + 1, kopf, l[max(0, m.start() - 40):m.end() + 30].strip()))
    sim = []
    for b in BOTS:
        f = "strategies/%s/equity_simulation.py" % b; t = lies(f).split("\n") if os.path.exists(f) else []
        w = [(i + 1, re.match(r"STARTING_CAPITAL\s*=\s*([^#]+)", l).group(1).strip()) for i, l in enumerate(t) if re.match(r"STARTING_CAPITAL\s*=", l)]
        sim.append((f, w))
    return r.returncode == 0, reg, sim
def code_gleich(ausser=()):
    for f, m in sorted(CODE.items()):
        if f not in ausser: p(md5f(f) == m, "unveraendert: %s md5 %s" % (f, m[:12]))
def voraussetzung():
    code_gleich()
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-176a" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-176a")
    k = kennungen(); p(max(k) in ("FL", "FM"), "Journal: hoechste %s (FL am Bau-HEAD)" % max(k))
    for f in (FA, FQ, FU): p(verfolgt_gleich(f) and md5f(f) == MD5F[f], "R56 (b)/S0-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5F[f]))
    b = block(); p(b is not None, "Registerblock 17c: genau R108 und Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[1], b[2]) if b else "?"))
    p(b is not None and wortlaut(b[0][0]) is not None, "R108 (a): Wortlaut 10a.5 genau einmal zwischen „Wortlaut: „“ und „“ Der Grund trägt“")
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 67. ") for l in z) == 1 and not any(l.startswith("## 68. ") for l in z) and not re.search(r"\bR108\b", reg), "Register: 67 da, 68 nicht; R108 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for m in MARKEN:
        i = einfuege(z, m); p(i is not None and (m[0] != "41.3 C2" or c2_ok(z, i)), "Ort %s: Einfuegestelle vor Z. %s eindeutig, R108 dort noch nicht genannt" % (m[0], i + 1 if i else "?"))
    s = lies(SB1).split("\n"); i1, i2 = sb1_stellen(s)
    p(i1 is not None and i2 is not None and i1 < i2, "S-B1: 10a.2 und 10a.4 je einmal, 10a.5 nicht, R108 nicht; Marke vor Z. %s, 10a.5 vor Z. %s" % (i1 and i1 + 1, i2 and i2 + 1))
    zi = lies(IDX).split("\n"); k = [i for i, l in enumerate(zi) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    p(len(k) == 1 and "Abschnitte 0–67" in zi[k[0]], "Index-Kopf Z. %s nennt 0–67" % (k[0] + 1 if k else "?"))
    p(sum(l.startswith("| 67 aus 17b |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-175 (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and not any(l.startswith("## 19. ") for l in zi), "Index: Zeile 67, Pflegezeile TB-175, Pflege-Anker je genau einmal; kein Abschnitt 19")
    p(not any(l.startswith("| 17c |") for l in lies(DI).split("\n")), "Dialog-Index: 17c noch nicht")
    ok, reg_d, sim = mess_d(); p(ok, "R108 (d): Register am Stand %s lesbar (git show)" % STAND_D)
    info("R108 (d) Voraussetzung (Messung, kein Urteil): Register am Stand %s nennt einen Wert des Startkapitals an %d Stelle(n)%s" % (STAND_D, len(reg_d), ":" if reg_d else ""))
    for n, kp, t in reg_d: info("  Z. %d (%s): %s" % (n, kp, t))
    for f, w in sim: info("R108 (d) Wert: %s %s" % (f, "; ".join("Z. %d STARTING_CAPITAL = %s" % x for x in w) or "kein STARTING_CAPITAL"))
    werte = set(v for _f, w in sim for _n, v in w); info("R108 (d): neun Dateien, %s" % ("alle denselben Wert %s" % werte.pop() if len(werte) == 1 and all(len(w) == 1 for _f, w in sim) else "NICHT derselbe Wert (Befund an 29.3): %s" % sorted(werte)))
    ende()
def md5cmd():
    for f in (FA, FQ, FU): p(md5f(QU + os.path.basename(f)) == MD5F[f] and md5f(f) == MD5F[f], "md5 vorher %s = nachher %s = %s" % (QU + os.path.basename(f), f, MD5F[f]))
    ende()
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg_v, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); salt = lies(SB1); s = salt.split("\n"); va = lies(beleg_v).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg_v)
    b = block(); p(b is not None and md5f(FA) == MD5F[FA], "Quelle md5 %s, Registerblock R108" % MD5F[FA])
    w = wortlaut(b[0][0]) if b else None; p(w is not None, "Wortlaut 10a.5 aus R108 (a) gelesen")
    p(not any(l.startswith("## 68. ") for l in z) and z[-1] == "" and z[-2] != "", "68 noch nicht im Register; endet mit einer Leerzeile")
    einf = [(einfuege(z, m), m) for m in MARKEN]; p(all(i is not None for i, _ in einf) and len(set(i for i, _ in einf)) == len(MARKEN) and c2_ok(z, [i for i, m in einf if m[0] == "41.3 C2"][0] or 0), "%d Einfuegestellen eindeutig (41.3 zwischen C2 und C3)" % len(MARKEN))
    i1, i2 = sb1_stellen(s); p(i1 is not None and i2 is not None and i1 < i2, "S-B1: Einfuegestellen Marke 10a.2 und 10a.5 eindeutig")
    k = karte(); p(k is not None, "Karte TB-176a gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    (r, q), za, ze = b
    ok, reg_d, sim = mess_d(); werte = sorted(set(v for _f, ww in sim for _n, v in ww))
    kopf = ("Reines Eintragen von Registertext, Bauart wie 67. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R108)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.c (`%s`) und die Übergabe 17.10.c (`%s`), beide seit `%s`. Marken nach R108 (f); "
            "der datierte Nachtrag 10a.5 nach R108 (a) steht in `%s`. Karte des Betreibers (Auftrag TB-176a, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-176a.") % (
            FA, MD5F[FA], format(os.path.getsize(FA), ",").replace(",", " "), za, ze, s0, FQ, FU, s0, SB1, k, datum)
    kette = ("**Kette:** Marken nach R108 (f): 62.2 (R101), Unterpunkt (a), ergänzt und berichtigt; 16.4 und 16.8, Unterpunkt (b); 16.6 und 41.3 C2, Unterpunkt (c); 29.3 und 37.5, Unterpunkt (d); 66.1 (R106), Unterpunkt (e); "
             "67.1 (R107), Unterpunkte (b) bis (e); S-B1-Vorregistrierung 10a.2, ergänzt durch den Nachtrag 10a.5 (Unterpunkt (a)). Ohne Marke: " + OHNE + ". Zählung: kein Fall; sechzehn (R108 (f)). "
             "Nicht mit TB-176a: Wert und Ort des Startkapitals (R108 (d) (1) bis (3)) und die nachgeholte Prüfung nach R108 (e) (BACKLOG Rang 1).")
    neu = ["", TITEL, "", kopf, "", "### 68.1 " + titel(r), "", "> " + r, "> " + q, "", kette, ""]
    neu += ["### 68.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-176a), Zeilen wörtlich:" % beleg_v, ""] + ["    " + l for l in vb] + ["",
        ("(a) R108 (d), die zwei Voraussetzungen (nur das Ob), gemessen durch Lesen: Das Register am Stand `%s` nennt einen Wert des Startkapitals an %d Stelle(n)%s. Die neun `strategies/<bot>/equity_simulation.py` tragen %s (Fundstellen je Datei oben). "
         "Ob eine genannte Stelle der Ort im Sinn von R108 (d) und 37.5 ist, ist hier nicht entschieden; Wert und Ort werden mit TB-176a nicht eingetragen.") % (
         STAND_D, len(reg_d), (": " + "; ".join("Z. %d (%s)" % (n, kp) for n, kp, _t in reg_d)) if reg_d else "", ("denselben Wert `%s`" % werte[0]) if len(werte) == 1 else ("verschiedene Werte %s" % werte)), "",
        "(b) R108 (a): Der Nachtrag 10a.5 steht im Wortlaut aus R108 (a) in `%s`; die Tatsachennotiz mit äusserer Quelle und Datum (kein UCITS-Fonds auf ein einzelnes Edelmetall) liegt im Repo nicht vor und ist nicht eingetragen." % SB1, "",
        "(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.c liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `%s0a_md5.txt`)." % (s0, QU, BEL), ""]
    s10a5 = ["", "### 10a.5 Nachtrag vom %s — Ergänzung zu Registertext 3 (10a.2) (R108 (a), TB-176a)" % datum, "", "> " + w, "",
             "*Quelle: R108 (a) (Register `%s`, Abschnitt 68.1), Fable-Antwort 17.10.c (`%s`, md5 `%s`). 10a.2 bleibt zeichengleich (Marke dort). Die Tatsachennotiz mit äusserer Quelle und Datum ist nicht eingetragen (68.2 (b)).*" % (REG, FA, MD5F[FA])]
    if probe: print("\n".join(neu + ["", "--- S-B1 ---"] + markenzeilen(MARKE_SB1, "Fable 17c R108 (68.1), Unterpunkt (a)", datum) + s10a5)); ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m[3], m[4], datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    s[i2:i2] = s10a5; s[i1:i1] = markenzeilen(MARKE_SB1, "Fable 17c R108 (68.1), Unterpunkt (a)", datum); schreibe(SB1, "\n".join(s))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s**" % m[3])] for m in MARKEN}
    s2 = lies(SB1).split("\n"); ms = [i + 1 for i, l in enumerate(s2) if l.startswith("> ⭐ **%s**" % MARKE_SB1)]; n5 = [i + 1 for i, l in enumerate(s2) if l.startswith("### 10a.5 ")]
    json.dump({"marken": [[m[0], m[3], (mz[m[0]] or [0])[0]] for m in MARKEN], "abschnitt_68": r2.index(TITEL) + 1, "sb1_marke": (ms or [0])[0], "sb1_10a5": (n5 or [0])[0]}, open(os.path.dirname(beleg_v) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: %d Marken Z. %s; Abschnitt 68 Z. %d" % (len(MARKEN), sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "R108 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al):] == neu, "Register append-only bis auf die %d Marken (je Leerzeile, Marke, Zeichengleich-Zeile)" % len(MARKEN))
    weg = set(x for n in ms for x in (n - 1, n, n + 1)) | set(range(n5[0] - 1, n5[0] - 1 + len(s10a5))) if len(ms) == 1 and len(n5) == 1 else set()
    p(len(ms) == 1 and len(n5) == 1 and [l for i, l in enumerate(s2) if i + 1 not in weg] == salt.split("\n") and s2.count("> " + w) == 1 and w in r,
      "S-B1: Marke Z. %s, 10a.5 Z. %s; sonst zeichengleich; Wortlaut = R108 (a)" % (ms, n5))
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 68. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) == len(MARKEN) and all(m[2] for m in mk) and d["sb1_marke"] and d["sb1_10a5"], "Abschnitt 68 in genau einer Teildatei: T%s; %d Marken mit Zeile; S-B1 Marke und 10a.5" % (teil, len(mk))); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]; rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–67" in z[k[0]], "Kopf genau einmal, nennt 0–67"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–67", "Abschnitte 0–68")
    i = [j for j, l in enumerate(z) if l.startswith("| 67 aus 17b |")]
    if p(len(i) == 1, "Zeile 67 genau einmal"): z.insert(i[0] + 1, "| 68 aus 17c | %s | R108 (68.1); 68.2 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 19. Die Marken aus Fable 17c (TB-176a)", "", "Alle %d Marken, die TB-176a nach R108 (f) im Register gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-176a/r_daten.json`." % len(mk), "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, T) for o, kp, n in sorted(mk, key=lambda m: m[2])] + ["",
           "Dazu in `%s`: Marke an 10a.2 (Z. %d, „%s“) und der datierte Nachtrag 10a.5 (Z. %d), R108 (a). Der Index ist kein Registertext." % (SB1, d["sb1_marke"], MARKE_SB1, d["sb1_10a5"]), ""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 19. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 19"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-175 (")]
    if p(len(j) == 1, "Pflegezeile TB-175 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-175 (", "In TB-175 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-176a (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-176a (`index`); 68 (R108) kommt zu T%s; neuer Abschnitt 19 (%d Marken, S-B1 10a.2/10a.5)." % (datum, s0, rcm, T, len(mk)))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"17c": {"frage": lies(FQ).split("\n")[0].split(" — ", 1)[-1].strip(),
                       "entscheidung": "(a) einverstanden: S-B1 10a.5 (Gold/Silber als ETC, äussere Quelle nötig), USD/EZB-Referenzkurs, Wochenrenditen; (b) einverstanden: Sammler mit vier Ergänzungen, Leseregel nach 24.3; (c) 16.6 bleibt 13 bis zur Herleitung mit R44, D4 Mechanikprobe; (d) anders: erst Wert und Ort des Startkapitals (37.5), dann die Leser; (e) anders: Prüfung mit gegen ohne Schranke nachholen (R108)",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17c geschrieben: %s" % ziel)
def nachher2():
    code_gleich(ausser=tuple(NEU_E2))
    for f, s in sorted(NEU_E2.items()):
        p(sha(f) == s, "E2 umgestellt: %s = Anhang (sha256 %s)" % (f, s[:12]))
        p(not re.search(r"STARTING_CAPITAL|startkapital", lies(f), re.I), "R108 (d) (2): %s liest kein Startkapital" % f)
    p(sha(PROBE_E2) == PSHA, "Probe E2 = Anhang E")
    pr, te = beleg("e2_probe.txt"), beleg("e2_test.txt")
    p(pr[-2:] == ["Ergebnis: 9 von 9 bestanden", "rc 0"], "e2_probe.txt: 9 von 9, rc 0")
    p(te[-2:] == ["Alle Pruefungen bestanden.", "rc 0"] and any("Gegenprobe 13: auswertung.py schreibt neben ERGEBNIS_DIR -> auswertung.py faellt auf" in l for l in te), "e2_test.txt: Test am neuen auswertung.py gruen, Gegenprobe trifft")
    ende()
BL_TEXT = (" · **Register 68 (Fable 17c, R108) mit TB-176a (%s, Journal %s)**: R108 (a) S-B1 Nachtrag 10a.5 im Wortlaut (Gold/Silber als ETC), Marke an 10a.2, **Tatsachennotiz mit äusserer Quelle und Datum offen**; "
    "Währung USD mit EZB-Referenzkurs, Wochenrenditen; (b) Sammler mit vier Ergänzungen, Leseregel nach 24.3, Auswerteplan vor der ersten Auswertung an den Verfahrensprüfer; (c) 16.6 bleibt 13 bis zur Herleitung aus den neuen Listen (R44), "
    "D4 unverändert bis zur Neuerzeugung, Mechanikprobe auf Beispieldaten; **offen: (d) Startkapital Wert und Ort (TB-176b, Handelscode, nach der Frage zur Voraussetzung, 68.2 (a))** und **(e) nachgeholte Prüfung mit gegen ohne Schranke "
    "(t3_supertrend, zwei Elliott-Bots)**; E2 mit TB-176a: `auswertung.py` und `embargo_neun.py` lesen `<bot>_alle_trades.csv` (R107 (e)) |")
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-176a" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-176a"):
        z[a[0]] = z[a[0]][:-2] + BL_TEXT % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-176a: " % neu), "Kopfzeile ## %s — TB-176a: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
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
    elif a == ["nachher2"]: nachher2()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
