#!/usr/bin/env python3
"""TB-170 Werkzeug (Anhang A): Fable 16c ins Register (Abschnitt 65, R104-R105 zeichengleich, fuenf Marken, 65.3), Index, Handfelder, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, json, os, re, subprocess, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
IDX, JO, BL, DI = P + "REGISTER_INDEX.md", P + "JOURNAL.md", P + "BACKLOG.md", P + "FABLE_DIALOG_INDEX.md"
AUF, BEL = "docs/auftraege/MAC_TB-170_register65_fable16c.md", "docs/belege/TB-170/"
FA = P + "FABLE_ANTWORT_2026-10-16c_r100c_elliott_abnahme.md"; FQ = P + "FABLE_ANFRAGE_2026-10-16c_r100c_leseprotokoll_elliott_abnahme.md"; FU = P + "FABLE_UEBERGABE_2026-10-16c_eroeffnung.md"
UE, ER = P + "UEBERGABE.md", P + "EROEFFNUNG_STEUERNDER_CHAT.md"
MD5 = { "docs/projektfuehrung/FABLE_ANTWORT_2026-10-16c_r100c_elliott_abnahme.md": "ebde5e999690f5c8ab0e1930ffb81783", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-16c_r100c_leseprotokoll_elliott_abnahme.md": "4021b20db4e9b9899e040fa5b2236b35", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-16c_eroeffnung.md": "7f767820b48fd139690ace13f8ae81e7", "docs/projektfuehrung/UEBERGABE.md": "a5a81d372183bd8127102917df8c1d61", "docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md": "14db36f1fe8f03eebcd75a28dafa1f6e" }
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R104)"
TITEL = "## 65. Fable 16c — Registerblock R104–R105 (TB-170)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
LP, LP_MD5 = "docs/belege/TB-148/leseprotokoll.md", "a1a324e02f06e2fc311ec26ca3b0ba74"
BOTS = ["elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "elliott_wave_stocks", "rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout"]
CODE = {192: '"end_time": times[i + 5],', 341: "traded = set()", 352: 'end_time = wave["end_time"]', 353: "if end_time in traded:", 358: "VOR traded.add: die",
        359: "gesperrte Welle hinterlaesst keinen Zustand", 360: ">= min_entry_idx (noch frisch) einsteigen.", 361: "if min_entry_idx is not None and run_bar < min_entry_idx:", 363: "traded.add(end_time)"}
GL, GL_Z, TK, TK_Z = "research/mtm_drawdown/grundlage.py", 65, "research/tb24_haltedauern/test_haltedauer_kern.py", 362
ALTV, FPOR, ERG169 = "docs/belege/TB-169/e_alt_vergleich.txt", "docs/belege/TB-169/f_porcelain.txt", "docs/ERGEBNIS_TB-169_e3b_listen_erzeuger.md"
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; R102 (d), R92 (c) |"
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | zg | Zeilenanfang, Kopf der Marke, Zusatz) - R104 (c), R105 (e)
MARKEN = [("62.1", "### 62.1 ", "quelle", "62.1 R100 ERGÄNZT durch R104 (65.1)", "Fable 16c R104, Unterpunkt (a): die Voraussetzung in (c) ist gemessen, Befund ohne Folge"),
          ("62.5 (c)", "### 62.5 ", "(c) R100 (a): ", "62.5, Absatz (c) ERGÄNZT durch R104 (65.1)", "Fable 16c R104, Unterpunkt (a)"),
          ("57.1", "### 57.1 ", "zg", "57.1 R90 PRÄZISIERT durch R105 (65.2)", "Fable 16c R105, Unterpunkte (a) und (b)"),
          ("61.1", "### 61.1 ", "quelle", "61.1 R98 ERGÄNZT durch R105 (65.2)", "Fable 16c R105, Unterpunkt (c)"),
          ("64.1", "### 64.1 ", "**Abnahme nach R98 (d)**", "64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R105 (65.2)", "Fable 16c R105, Unterpunkt (c)")]
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def info(t): OUT.append("info  " + t)
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT); m = sum(l.startswith(("ja ", "NEIN")) for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (m, n)); sys.exit(rc if rc is not None else (1 if n else 0))
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def block():
    """([(R-Zeile, Quellenzeile, Z.)] fuer R104 und R105, Z. Zaun auf, Z. Zaun zu) oder None."""
    z = lies(FA).split("\n")
    if z.count(KOPF_A) != 1: return None
    a = z.index(KOPF_A) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [(i + 1, z[i]) for i in range(a + 1, e) if z[i]]; soll = ["R104 — ", "Quelle des Grundes: ", "R105 — ", "Quelle des Grundes: "]
    if len(b) != 4 or [l[:len(s)] for (_, l), s in zip(b, soll)] != soll: return None
    return [(b[0][1], b[1][1], b[0][0]), (b[2][1], b[3][1], b[2][0])], a + 1, e + 1
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m):
    """Index der Einfuegestelle (nach dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any("R104" in z[i] or "R105" in z[i] for i in range(a, e)): return None
    if m[2] == "zg": k = [i for i in range(a, e) if z[i] == ZG][-1:]
    elif m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    else: k = [i for i in range(a, e) if z[i].startswith(m[2])]
    return k[0] + 1 if len(k) == 1 else None
def markenzeilen(m, datum): return ["", "> ⭐ **%s** (%s, TB-170, %s)." % (m[3], m[4], datum), ZG]
def lesepr():
    z = lies(LP).split("\n"); aus = {}
    for b in BOTS:
        aus[b] = [(i + 1, l.split("|")[1].strip().strip("`")) for i, l in enumerate(z) if l.startswith("| `strategies/%s/" % b) and len(l.split("|")) > 4
                  and "multi_symbol_optimise.py" not in l.split("|")[1] and "M3" in l.split("|")[3]]
    return aus
def code_fehlt(bot):
    f = "strategies/%s/elliott_wave_counter.py" % bot; z = lies(f).split("\n") if os.path.exists(f) else []
    return f, [n for n, s in sorted(CODE.items()) if len(z) < n or s not in z[n - 1]]
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
    for f in (FA, FQ, FU, UE, ER): p(md5f(f) == MD5[f], "md5 %s = %s" % (f, MD5[f]))
    ende()
def voraussetzung():
    for f in (FA, FQ, FU, UE, ER): p(verfolgt_gleich(f) and md5f(f) == MD5[f], "R56 (b)/0a-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5[f]))
    b = block(); p(b is not None, "Registerblock 16c: genau R104, Quelle, R105, Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[1], b[2]) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 64. ") for l in z) == 1 and not any(l.startswith("## 65. ") for l in z) and not re.search(r"\bR10[45]\b", reg), "Register: 64 da, 65 nicht; R104/R105 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for m in MARKEN: i = einfuege(z, m); p(i is not None, "Ort %s: Einfuegestelle nach Z. %s eindeutig, R104/R105 dort noch nicht genannt" % (m[0], i if i else "?"))
    p(md5f(LP) == LP_MD5, "R104 (a): Leseprotokoll %s md5 %s (= Stand d9f8489)" % (LP, LP_MD5))
    info("Leseprotokoll zuletzt geaendert in Commit %s" % git("log", "-1", "--format=%h", "--", LP).stdout.decode().strip())
    if md5f(LP) == LP_MD5:
        for bot, fs in lesepr().items(): p(len(fs) > 0, "R104 (a) Voraussetzung, %s: M3 ausserhalb multi_symbol_optimise.py: %s" % (bot, "; ".join("%s (Z. %d)" % (f, n) for n, f in fs) or "KEINE"))
    for bot in ("elliott_wave", "elliott_wave_stocks"):
        f, fehlt = code_fehlt(bot); p(not fehlt, "R105 (c) Code %s: Z. 192 end_time = times[i + 5]; 341 traded; 352–353 Schluessel end_time; 358–360 Kommentar; 361 Schranke; 363 traded.add(end_time)%s" % (f, "; abweichend Z. %s" % fehlt if fehlt else ""))
    gl = lies(GL).split("\n") if os.path.exists(GL) else []; p(len(gl) >= GL_Z and "_positionen.csv" in gl[GL_Z - 1], "BACKLOG-Nachtrag: %s Z. %d liest <bot>_positionen.csv" % (GL, GL_Z))
    tk = lies(TK).split("\n") if os.path.exists(TK) else []; p(len(tk) >= TK_Z and "13. Wache" in tk[TK_Z - 1], "BACKLOG-Nachtrag: %s Z. %d Pruefung 13 (Wache)" % (TK, TK_Z))
    p(os.path.exists(ALTV) and "vorher rc 1, nachher rc 1" in lies(ALTV), "BACKLOG-Nachtrag: %s zeigt den Alt-Test rot (rc 1 vorher und nachher)" % ALTV)
    p(os.path.exists(FPOR) and lies(FPOR) == "?? %s\n" % FPOR, "BACKLOG-Nachtrag: %s nennt nur sich selbst (Selbstbezug)" % FPOR)
    zi, k = stand_kopf(); p(len(k) == 1 and "Abschnitte 0–64" in zi[k[0]] and zi[k[0] + 1].startswith("12 023 Zeilen, sha256 `459be94e"), "BACKLOG-Nachtrag: Index-Kopf Z. %s nennt 0–64 und 12 023 Zeilen/459be94e (gemischter Stand)" % (k[0] + 1 if k else "?"))
    bl = lies(BL); p("grundlage.py" not in bl and "test_haltedauer_kern" not in bl, "BACKLOG: grundlage.py und test_haltedauer_kern noch nicht genannt")
    p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl.split("\n")) == 1, "BACKLOG: Rang 1 (Stand TB-169) genau einmal")
    p(sum(l.startswith("| 64 Vollzug TB-166 |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-169 (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and not any(l.startswith("## 16. ") for l in zi), "Index: Zeile 64, Pflegezeile TB-169, Pflege-Anker je genau einmal; kein Abschnitt 16")
    p(not any(l.startswith("| 16c |") for l in lies(DI).split("\n")), "Dialog-Index: 16c noch nicht")
    kk = kennungen(); p(max(kk) == "FF" and "FG" not in kk, "Journal: hoechste FF, naechste FG frei")
    ende()
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    b = block(); p(b is not None and md5f(FA) == MD5[FA], "Quelle md5 %s, Registerblock R104/R105" % MD5[FA])
    p(not any(l.startswith("## 65. ") for l in z) and z[-1] == "" and z[-2] != "", "65 noch nicht im Register; endet mit einer Leerzeile")
    einf = [(einfuege(z, m), m) for m in MARKEN]; p(all(i is not None for i, _ in einf), "5 Einfuegestellen eindeutig")
    k = karte(); p(k is not None, "Karte TB-170 gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    bl, za, ze = b; z64 = [i for i, l in enumerate(z) if l.startswith("## 64. ")]; so = [i + 1 for i, l in enumerate(z) if l.startswith("**Sperrlisten-Sonde zu Punkt 11**") and z64 and i > z64[0]]
    if not p(len(so) == 1 and "am Stand `69539db`" in z[so[0] - 1], "64: Absatz Sperrlisten-Sonde genau einmal, nennt `69539db` (Z. %s)" % so): ende()
    kopf = ("Reines Eintragen von Registertext, Bauart wie 62. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R104)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Fragen, „Zur Kenntnis“, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 16.10.c und die Übergabe 16.10.c (beide seit `%s`). Marken nach R104 (c) und R105 (e). "
            "Karte des Betreibers (Auftrag TB-170, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-170.") % (FA, MD5[FA], format(os.path.getsize(FA), ",").replace(",", " "), za, ze, s0, s0, k, datum)
    kette = ["**Kette:** Marken nach R104 (c): 62.1 (R100), Unterpunkt (a); 62.5, Absatz (c). R90 bis R92 bleiben zeichengleich, keine Berichtigung. Voraussetzung in (a) gemessen: 65.3 (b).",
             "**Kette:** Marken nach R105 (e): 57.1 (R90), Unterpunkte (a) und (b); 61.1 (R98), Unterpunkt (c); 64.1, Absatz „Abnahme nach R98 (d)“, Unterpunkt (c). Ohne Marke: 56.4 (R87), 55.4 (R81), 54.2 (R75), 48.14 (R46); Abschnitt 10. Stand nach (c): 65.3 (c)."]
    neu = ["", TITEL, "", kopf, ""]
    for n, ((r, q, _), kt) in enumerate(zip(bl, kette)): neu += ["### 65.%d %s" % (n + 1, titel(r)), "", "> " + r, "> " + q, "", kt, ""]
    neu += ["### 65.3 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-170), Zeilen wörtlich:" % beleg, ""] + ["    " + l for l in vb] + ["",
        ("(a) Tatsachennotiz zu 64, Absatz „Sperrlisten-Sonde zu Punkt 11“ (Register Z. %s), 64 bleibt zeichengleich: Die Sonde lief in TB-169 nach der Reihenfolge E ⇒ S am Stand `8520d9e` (Commit E), nicht am Stand `69539db`, wie der Satz sagt "
         "(Abnahme TB-169, Befund B1; die Sitzung TB-169 meldet es selbst in `%s`, Abweichungen). Für Punkt 11 ohne Folge.") % (so[0] if len(so) == 1 else "?", ERG169), "",
        ("(b) R104 (a), Voraussetzung (nur das Ob): gemessen oben (Zeilen „R104 (a) Voraussetzung“) am Leseprotokoll `%s` (md5 `%s`, = Stand `d9f8489`): bei 9 von 9 Bots führt M3 eine Fundstelle ausserhalb der neun "
         "multi_symbol_optimise.py (je `equity_simulation.py` und `backtest_*.py`). **Teilmessung:** Das Protokoll ordnet Dateien Messpunkten zu, nicht Sätzen; dass gerade diese Fundstellen die Sätze in R90 (d) und R91 (b) tragen, ist erschlossen. "
         "Keine Frage an den Verfahrensprüfer; die Marke an 62.1 ist gesetzt.") % (LP, LP_MD5), "",
        ("(c) R105 (c), Stand: Der zweite Weg (Tatsachennotiz, dass der Schlüssel von traded eine andere, spätere Welle nie trifft) trägt am Code nicht. Gemessen oben (Zeilen „R105 (c) Code“), bei beiden Bots gleich: Der Schlüssel von `traded` ist "
         "`end_time` der Welle (`elliott_wave_counter.py` Z. 341, 352–353, 363; `end_time` = Zeit des sechsten Pivots, Z. 192); die Schranke steht in Z. 361 vor `traded.add` (Z. 363); der Kommentar Z. 358–360 sagt, die gesperrte Welle könne an einem späteren Lauf einsteigen. "
         "Erschlossen (Lesung des steuernden Chats, vom Verfahrensprüfer nicht gelesen): ohne Schranke wird dieselbe Welle an ihrem späteren Einstieg verdrängt, keine andere. Damit bleibt Weg 1 (der Fall wird auf dem Test-Snapshot herbeigeführt, mit Gegenprobe nach 40.7), "
         "Handwerk und ein eigener Handelscode-Auftrag (BACKLOG Rang 1), vor dem Tag. Zur Kenntnis an den Verfahrensprüfer mit der nächsten Anfrage."), "",
        "(d) R56 (b): Übergabe, Anfrage und Antwort 16.10.c liegen seit `%s` im Repo." % s0, ""]
    if probe: print("\n".join(neu)); ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m, datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s**" % m[3])] for m in MARKEN}
    json.dump({"marken": [[m[0], m[3], (mz[m[0]] or [0])[0]] for m in MARKEN], "abschnitt_65": r2.index(TITEL) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: 5 Marken Z. %s; Abschnitt 65 Z. %d" % (sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(all(r2.count("> " + x[0]) == 1 and r2.count("> " + x[1]) == 1 for x in bl), "R104, R105 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al):] == neu, "append-only bis auf die fuenf Marken (je Leerzeile, Marke, Zeichengleich-Zeile)")
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 65. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) == 5 and all(m[2] for m in mk), "Abschnitt 65 in genau einer Teildatei: T%s; 5 Marken mit Zeile" % teil); T = str(teil[0]) if teil else "?"
    z, k = stand_kopf(); rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–64" in z[k[0]], "Kopf genau einmal, nennt 0–64"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–64", "Abschnitte 0–65")
    i = [j for j, l in enumerate(z) if l.startswith("| 64 Vollzug TB-166 |")]
    if p(len(i) == 1, "Zeile 64 genau einmal"): z.insert(i[0] + 1, "| 65 aus 16c | %s | R104–R105 (65.1–65.2); 65.3 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 16. Die Marken aus Fable 16c (TB-170)", "", "Alle 5 Marken, die TB-170 nach R104 (c) und R105 (e) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-170/r_daten.json`.", "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, T) for o, kp, n in sorted(mk, key=lambda m: m[2])] + [""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 16. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 16"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-169 (")]
    if p(len(j) == 1, "Pflegezeile TB-169 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-169 (", "In TB-169 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-170 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-170 (`index`); 65 (R104–R105) kommt zu T%s; neuer Abschnitt 16 (5 Marken). Der Kopf mischt weiter Stände (BACKLOG Rang 1, TB-170)." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"16c": {"frage": lies(FQ).split("\n")[0].split(" — ", 1)[1].strip(),
                       "entscheidung": "Frage 1 einverstanden: Tatsachennotiz ohne Folge für R90 bis R92, Voraussetzung zu M3 (R104); Frage 2 anders: der Fall nach R90 (g) bleibt bei den Elliott-Bots am Erzeuger offen, vor dem Tag (R105)",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 16c geschrieben: %s" % ziel)
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-169"):
        z[a[0]] = z[a[0]][:-2] + (" · Register 65 (Fable 16c: R104 Tatsachennotiz zu R100 (c), R105 Lesart und Massstab zu R90 (g), Stand der Abnahme bei den Elliott-Bots) mit TB-170 (%s, Journal %s)"
            "; **Handelscode, eigener Auftrag, vor dem Tag:** R105 (c) Weg 1 bei `elliott_wave` und `elliott_wave_stocks`, den Fall nach R90 (g) auf dem Test-Snapshot herbeiführen (Welle vor dem Handelbar-Tag, deren Eintrag in `traded` ohne Schranke den späteren Einstieg verdrängt; Gegenprobe nach 40.7; Bau-Helfer und frischer Gegenleser), Weg 2 trägt am Code nicht (65.3 (c)); R105 (d) `t3_supertrend` nichts entschieden"
            "; Nachträge: `%s` Z. %d liest `<bot>_positionen.csv` (entfällt mit E-3b); Alt-Test `%s` Prüfung 13 (Z. %d, Wache) rot seit E-3b (vorher = nachher, `%s`); Kopf von `REGISTER_INDEX.md` mischt Stände (Commit und Abschnitte neben „12 023 Zeilen, sha256 `459be94e…`“ vom Stand `3f2e97e`)"
            "; `f_porcelain.txt` in TB-166 und TB-169 mit Selbstbezug (die Umleitung legt die Datei an, bevor `git status` läuft; ab TB-170 über `$TMPDIR`) |") % (datum, kenn, GL, GL_Z, TK, TK_Z, ALTV)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-170: " % neu), "Kopfzeile ## %s — TB-170: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
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
