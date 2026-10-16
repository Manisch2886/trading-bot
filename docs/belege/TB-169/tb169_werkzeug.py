#!/usr/bin/env python3
"""TB-169 Werkzeug (Anhang A): Voraussetzungen, E-3b (2 Dateien + Test), Abnahme R98 (d), Sonde-Auswahl, Register 64 (Vollzug TB-166 nach 37.3), Index, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | e3b [--probe] | abnahme <BELEG> | altvergleich <VOR> <NACH> | sonde <BELEG> <VOR> <NACH> | register <DATUM> <S0> <E> <SONDE> <ABNAHME> [--probe]
  index <S0> <DATUM> [--probe] | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
BEL, AUF = "docs/belege/TB-169/", "docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md"
E3B = {"research/tb24_haltedauern/alle_bots.py": ["6e9ddce913b555a1598514225c1f24d31bb5ddcdd1444e3bac2bcf2a393ae525", "4246b577bfc486e3f872ea5132412fe5e23092e23b737182d765373118666964"], "research/tb24_haltedauern/positionen_holen.py": ["a9e81f02dd69d946ff3724fa741d179155a13449194d404828eb1831d6333961", "b6d1e2d66eae02a8a546cab15649a4100e3c1b2df0a9a668140f23de3a8573db"], "research/tb24_haltedauern/test_listen_erzeuger.py": [None, "e196884a152796e4a9ab6e715de70933ebf7614ecf4f38d763eed24d46cda1bf"]}
NOTIZ, NOTIZ_MD5, NOTIZ_COMMIT = "docs/belege/TB-166/e_notiz.md", "e28885ae5e10e158860fb457671ce900", "4a51876"
M166, M166_MD5, M166_COMMIT = "docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md", "57d05b949318d95e5ef28a5692ef1241", "57a1062"
E3A_COMMIT, N_E3A = "15f28e4", 20
AB, AB_SHA, SO, SO_SHA = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json", "46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f", "shared/sperrlistensonde.py", "98c02e0e9b42831d88e0cd9cbdc39d64c458691fdbf1e650aa4e32c933cc0d71"
SONDE_BEFEHL = "trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild " + AB
TITEL63, TITEL631 = "## 63. Vollzug TB-167 (Tatsachennotiz nach 37.3; Abhilfe G6 elliott_wave_stocks) (TB-168)", "### 63.1 Vollzug TB-167 (Tatsachennotiz nach 37.3)"
TITEL64 = "## 64. Vollzug TB-166 (Tatsachennotiz nach 37.3; E-3a Schranke je Symbol) mit Abnahme nach R98 (d) (TB-169)"
S373, Z373 = "Ein Befund 1 der Sperrlisten-Sonde", 7025
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; Abnahme nach R98 (d) mit E-3b, Tatsachennotiz 37.3 als Entwurf im Ergebnis |"
N_JE_BOT, N_ALLE = 13, 117
E_BELEGE = ["v_voraussetzung.txt", "e_alt_vergleich.txt", "e_e3b_probe.txt", "e_e3b.txt", "e_kerzen.txt", "e_abnahme.txt", "e_abnahme_pruefung.txt"]
BOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout", "t3_supertrend", "elliott_wave", "elliott_wave_stocks"]
FASSUNG = {"2": "nicht prüfbar", "1": "Befund 1 (beauftragt)"}
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True, text=True).stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT); print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def notiz():
    t = lies(NOTIZ); z = t.split("\n"); rows = [l for l in z if l.startswith("| `")]
    return t, z, [(r.split(" | ")[0][3:-1], r.split(" | ")[2].strip("`"), r.split(" | ")[3].strip("`"), r.split(" | ")[4].strip("`")) for r in rows]
def karte(datei, titel):
    if not os.path.exists(datei): return None, None
    z = lies(datei).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(titel)]
    if len(a) != 1: return None, None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [(i, l) for i, l in enumerate(z[a[0] + 1:b], a[0] + 2) if l.startswith("> ")]
    if len(k) != 1 or ("⟨⟨" + "FREIGABE") in k[0][1]: return None, None
    return k[0][1][2:].strip(), k[0][0]
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def voraussetzung():
    reg = lies(REG); z = reg.split("\n")
    p(sum(l == TITEL63 for l in z) == 1 and not re.search(r"^## 64\. ", reg, re.M), "Register: 63 genau einmal, 64 noch nicht")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    t631 = [i + 1 for i, l in enumerate(z) if l == TITEL631]; p(len(t631) == 1, "Vorbild 63.1 genau einmal, Z. %s" % t631)
    t373 = [i + 1 for i, l in enumerate(z) if S373 in l.replace("**", "")]; p(t373[:1] == [Z373], "37.3 zuerst Z. %d" % Z373)
    for f, (vor, nach) in sorted(E3B.items()):
        p((vor is None and not os.path.exists(f)) or (vor is not None and os.path.exists(f) and sha(f) == vor), "vorher %s: %s" % (f, (vor or "fehlt")[:16]))
        p(os.path.exists(BEL + "e3b_" + os.path.basename(f)) and sha(BEL + "e3b_" + os.path.basename(f)) == nach, "Anhang %se3b_%s = nachher %s…" % (BEL, os.path.basename(f), nach[:16]))
    t, nz, rows = notiz(); p(md5(t) == NOTIZ_MD5 and git("log", "--format=%h", "-1", "--", NOTIZ).strip()[:7] == NOTIZ_COMMIT, "e_notiz.md md5 %s, Commit %s" % (NOTIZ_MD5, NOTIZ_COMMIT))
    p(len(rows) == N_E3A and len({r[0] for r in rows}) == N_E3A, "e_notiz.md: %d Zeilen, %d Dateien" % (len(rows), len({r[0] for r in rows})))
    for f, vor, nach, c in rows:
        p(c == E3A_COMMIT and os.path.exists(f) and sha(f) == nach and git("log", "--format=%h", "-1", "--", f).strip()[:7] == E3A_COMMIT, "heute = nachher, zuletzt in %s: %s" % (E3A_COMMIT, f))
    ab = lies(AB); p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild %s… und Sonde %s…" % (AB_SHA[:16], SO_SHA[:16]))
    p(not any(r[0] in ab for r in rows), "Abbild fuehrt keine der %d Dateien" % N_E3A)
    k, kz = karte(M166, "## Freigabe"); m = lies(M166); p(k is not None and md5(m) == M166_MD5 and git("log", "--format=%h", "-1", "--", M166).strip()[:7] == M166_COMMIT, "Karte TB-166: Z. %s, md5 %s, Commit %s" % (kz, M166_MD5, M166_COMMIT))
    k9, _ = karte(AUF, "## Freigabe"); p(k9 is not None, "Karte TB-169 gefuellt")
    ix = lies(IDX).split("\n")
    p(sum("Abschnitte 0–63" in l for l in ix if l.startswith("**Stand:** Register")) == 1 and sum(l.startswith("| 63 Vollzug TB-167 |") for l in ix) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-168 (") for l in ix) == 1, "Index: Kopf 0–63, Zeile 63, Pflegezeile TB-168")
    bl = lies(BL).split("\n"); p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl) == 1, "BACKLOG Rang 1 (Stand TB-166) genau einmal")
    k = kennungen(); p(max(k) == "FE" and "FF" not in k, "Journal hoechste FE, naechste FF frei")
    ende()
def e3b(probe):
    for f, (vor, nach) in sorted(E3B.items()):
        q = BEL + "e3b_" + os.path.basename(f)
        p((vor is None and not os.path.exists(f)) or (vor is not None and sha(f) == vor), "vorher " + f); p(sha(q) == nach, "Quelle %s = nachher" % q)
    if probe or nein(): ende()
    for f in sorted(E3B): schreibe(f, lies(BEL + "e3b_" + os.path.basename(f)))
    for f, (vor, nach) in sorted(E3B.items()): p(sha(f) == nach, "nachher %s %s" % (f, nach))
    ende()
def abnahme(beleg):
    z = lies(beleg).rstrip("\n").split("\n")
    for b in BOTS: p(sum(l.startswith("ja    %s: " % b) for l in z) == N_JE_BOT, "%s: %d Pruefungen ja" % (b, N_JE_BOT))
    p(not any(l.startswith("NEIN") for l in z), "keine NEIN-Zeile"); p(z[-2:] == ["Ergebnis: %d von %d bestanden" % (N_ALLE, N_ALLE), "rc 0"], "Ergebnis %d von %d, rc 0" % (N_ALLE, N_ALLE))
    ende()
def altvergleich(vor, nach):
    """Alter Test test_haltedauer_kern.py vor und nach E-3b: dieselben Fehlzeilen, derselbe Rueckgabewert (Pruefung 13 ist schon am HEAD rot)."""
    a, b = lies(vor).rstrip("\n").split("\n"), lies(nach).rstrip("\n").split("\n")
    fa, fb = sorted(l for l in a if l.startswith("  - ")), sorted(l for l in b if l.startswith("  - "))
    p(a[-1] == b[-1] and a[-1] in ("rc 0", "rc 1"), "Rueckgabewert vorher %s, nachher %s" % (a[-1], b[-1]))
    p(fa == fb, "Fehlzeilen vorher %d = nachher %d%s" % (len(fa), len(fb), (": " + fa[0][:120]) if fa else ""))
    ende()
def belege():
    for f in E_BELEGE:
        z = lies(BEL + f).rstrip("\n").split("\n") if os.path.exists(BEL + f) else ["fehlt"]
        p(z[-1] == "rc 0" and not any(l.startswith("NEIN") for l in z), "Beleg %s: letzte Zeile %s, NEIN-Zeilen %d" % (f, z[-1], sum(l.startswith("NEIN") for l in z)))
def fassung(beleg):
    z = lies(beleg).rstrip("\n").split("\n"); m = [re.match(r"^  Punkt 11  \[(\d) ", l) for l in z]; m = [x.group(1) for x in m if x]
    rw = [l for l in z if l.startswith("RUECKGABEWERT ")]; rc = z[-1] if z else ""
    if len(m) != 1 or len(rw) != 1: return None, m, rw, rc
    if m[0] == "2" and rc == "rc 2" and rw[0].startswith("RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [") and re.search(r"[\[ ]11[,\]]", rw[0]): return "2", m, rw, rc
    if m[0] == "1" and rc == "rc 1" and rw[0] == "RUECKGABEWERT 1 BEFUND - BEFUND in Punkt(en) [11]": return "1", m, rw, rc
    return None, m, rw, rc
def satz(f, s0):
    kopf = "**Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-169 am Stand `%s`; Aufruf wie TB-168 Schritt S: `%s`, Abbild `%s…`; Beleg `%ss_sonde.txt`): " % (s0, SONDE_BEFEHL, AB_SHA[:8], BEL)
    if f == "2": return kopf + "Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keine der 20 Dateien — wie bei 60.1 und 63.1. Der Übergang steht deshalb nur hier und in den Commits."
    return kopf + "Punkt 11 „Befund 1 (beauftragt)“ (`1`). Vor dem Tag zulässig nach 37.3, weil beauftragt (Freigabe: Karten unten); geschlossen wird er durch ein neues Abbild unter neuem Namen (37.3), das TB-169 nicht zieht."
def sonde(beleg, vor, nach):
    p(lies(vor) == lies(nach), "git status --porcelain vor und nach der Sonde gleich"); p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild und Sonde")
    f, m, rw, rc = fassung(beleg); p(f is not None, "Punkt 11 im Beleg: %s · %s · %s" % (m, rw[0][:160] if rw else "kein RUECKGABEWERT", rc))
    if f: print("Fassung: %s" % FASSUNG[f])
    ende()
def register(datum, s0, ec, sb, ab, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0) or not re.fullmatch(r"[0-9a-f]{7}", ec): sys.exit(2)
    f = fassung(sb)[0]; p(f is not None, "Fassung Sonde: %s" % FASSUNG.get(f, "keine"))
    za = lies(ab).rstrip("\n").split("\n"); p(za[-2:] == ["Ergebnis: %d von %d bestanden" % (N_ALLE, N_ALLE), "rc 0"] and not any(l.startswith("NEIN") for l in za), "Abnahme-Beleg %d von %d, rc 0" % (N_ALLE, N_ALLE))
    belege()   # B5: alle V- und E-Belege rc 0, keine NEIN-Zeile
    t, nz, rows = notiz(); p(md5(t) == NOTIZ_MD5 and len(rows) == N_E3A, "Quelle e_notiz.md md5 %s, %d Zeilen" % (NOTIZ_MD5, N_E3A))
    for fl, vor, nach, c in rows: p(sha(fl) == nach, "heute = nachher: " + fl)
    k9, _ = karte(AUF, "## Freigabe"); p(k9 is not None, "Karte TB-169 gefuellt"); k6, kz = karte(M166, "## Freigabe"); p(k6 is not None and md5(lies(M166)) == M166_MD5, "Karte TB-166 Z. %s" % kz)
    z = lies(REG).split("\n"); p(not any(l.startswith("## 64. ") for l in z) and z[-1] == "" and z[-2] != "", "64 noch nicht; Register endet mit einer Leerzeile")
    t631 = [i + 1 for i, l in enumerate(z) if l == TITEL631]
    if nein(): ende()
    kopf = ("Reines Eintragen, Bauart 63.1 (Register Z. %d ff.); Karte des Betreibers (Auftrag TB-169, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-169 (Stand `%s`). "
            "Nichts entfernt, kein bestehender Satz umgeschrieben; kein neues Abbild; keine Marke.") % (t631[0], k9, datum, s0)
    q1 = ("*Übernommen zeichengleich aus `%s` (Commit `%s`, md5 `%s`), dem Entwurf aus TB-166 (Ergebnis TB-166, Abschnitt „Entwurf Tatsachennotiz nach 37.3“). Vollzogen in Commit `%s` (TB-166 E). "
          "„Entwurf, nicht eingetragen“ darin beschreibt den Stand in TB-166; eingetragen ist der Übergang mit diesem Abschnitt.*") % (NOTIZ, NOTIZ_COMMIT, NOTIZ_MD5, E3A_COMMIT)
    fk = "**Freigabe-Karte TB-166, wörtlich** (zu R98 (c); aus `%s` Z. %d, Commit `%s`, md5 `%s`):" % (M166, kz, M166_COMMIT, M166_MD5)
    an = ("**Abnahme nach R98 (d)** (gemessen in TB-169 Schritt E am Erzeuger, Commit `%s`): `research/tb24_haltedauern/test_listen_erzeuger.py` auf einem Test-Snapshot, geprüft an den Ausgaben von "
          "`positionen_holen.py` (Probe nach R86 (d) mit und ohne Zeilen ab dem Schnitt; Wachen nach R86 (d) und R87 (c) je allein beissend, 41.1 A5; Fall nach R90 (g), Tatsachennotiz für t3_supertrend und die zwei Elliott-Bots im Beleg; Symbol nach R81 (h); offene Position nach R86 (c)); Beleg `%se_abnahme.txt`: „%s“, `rc 0`; Kerzen-Probe `%se_kerzen.txt`: „%s“.") % (ec, BEL, za[-2], BEL, lies(BEL + "e_kerzen.txt").rstrip("\n").split("\n")[-2])
    neu = ["", TITEL64, "", kopf, "", "### 64.1 Vollzug TB-166 (Tatsachennotiz nach 37.3)", "", q1, ""] + t.rstrip("\n").split("\n") + ["", fk, "", "> " + k6, "", an, "", satz(f, s0), ""]
    if probe: print("\n".join(neu)); ende()
    alt = lies(REG); schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG); p(r2.startswith(alt[:-1]) and r2.count("\n" + TITEL64 + "\n") == 1, "nachher: append-only, 64 genau einmal, Z. %d" % (r2.split("\n").index(TITEL64) + 1))
    p(t.rstrip("\n") in r2 and r2.endswith("\n") and not r2.endswith("\n\n"), "e_notiz.md zeichengleich; Register endet mit einer Leerzeile"); ende()
def index(s0, datum, probe):
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 64. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 64 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–63" in z[k[0]], "Kopf genau einmal, nennt 0–63"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–63", "Abschnitte 0–64")
    i = [j for j, l in enumerate(z) if l.startswith("| 63 Vollzug TB-167 |")]
    if p(len(i) == 1, "Zeile 63 genau einmal"):
        z.insert(i[0] + 1, "| 64 Vollzug TB-166 | %s | 64.1 Hash-Übergänge nach 37.3 (E-3a, 20 Dateien, Commit `%s`; aus docs/belege/TB-166/e_notiz.md) mit Freigabe-Karten, Abnahme nach R98 (d) am Listen-Erzeuger (TB-169) und Sonde zu Punkt 11 | – |" % (T, E3A_COMMIT))
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-168 (")]
    if p(len(j) == 1, "Pflegezeile TB-168 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-168 (", "In TB-168 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-169 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-169 (`index`); 64 (Vollzug TB-166) kommt zu T%s." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-166"):
        z[a[0]] = z[a[0]][:-2] + (" · E-3b (Listen-Erzeuger: Schnitt an der Eingabe, Wachen, Doppellauf weg; kerzen_je_trade mit datetime64) und Abnahme nach R98 (d) mit TB-169 (%s, Journal %s); Register 64 (Vollzug TB-166 nach 37.3)"
            "; vor der Neuerzeugung der Listen: `auswertung.py` (Z. 71, 325) und `embargo_neun.py` (Z. 35) lesen noch `<bot>_positionen.csv` bzw. `trades_ausgefuehrt` (entfallen mit E-3b); das Abbild tb117 führt die neun `daten/<bot>_alle_trades.csv` (Neuerzeugung trifft das Abbild); R102 (d), R92 (c) |") % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-169: " % neu), "Kopfzeile ## %s — TB-169: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif a == ["e3b"]: e3b(pr)
    elif len(a) == 2 and a[0] == "abnahme": abnahme(a[1])
    elif len(a) == 3 and a[0] == "altvergleich": altvergleich(a[1], a[2])
    elif len(a) == 4 and a[0] == "sonde": sonde(a[1], a[2], a[3])
    elif len(a) == 6 and a[0] == "register": register(a[1], a[2], a[3], a[4], a[5], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif a == ["kennung"]: print("Kennung %s (letzte %s)" % (naechste(max(kennungen())), max(kennungen()))); sys.exit(0)
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
