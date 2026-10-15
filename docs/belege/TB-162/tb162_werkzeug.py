#!/usr/bin/env python3
"""TB-162 Werkzeug (Anhang B): Voraussetzungen F5/F11, Register 58 (R94-R97) mit Marken (R96 (d), R97 (e)), Index-Eintraege, Handfelder, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  voraussetzung                         F5/F11: Voraussetzungen aus R94-R97 messen (rc 0 = alle ja)
  register <DATUM> <S0> <BELEG> [--probe]  Abschnitt 58 (R94-R96 aus 14a, R97 aus 14b zeichengleich) und 8 Marken
  index <S0> <DATUM> [--probe]          REGISTER_INDEX.md: Kopf, Tabelle 4, Zeile 58, Abschnitt 13, Pflege (nach c2_index_zeilen.py)
  handfelder <ZIEL>                     Handfelder 14a fuer dialog_index.py
  kennung | journal <BLOCK> [--probe]   naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, os, re, subprocess, sys
REG, IDX, JO = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md"
FA = "docs/projektfuehrung/FABLE_ANTWORT_2026-10-14a_wf_kapital_dd_versuch_vor_dem_tag.md"
DREI = [FA, "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14a_wf_kapital_dd_vor_dem_tag.md", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14_eroeffnung.md"]
FB = "docs/projektfuehrung/FABLE_ANTWORT_2026-10-14b_doppellauf_verstoesst_gegen_a9_positionen_nach_r45.md"
SECHS = DREI + [FB, "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-14b_positionen_ohne_kennung.md", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-14b_eroeffnung.md"]
FA_MD5, FB_MD5 = "c33799567a0205f66c502dbf5aaff5c5", "4b02ae62279294f5b1df4b1472cc2435"
KOPF_A, KOPF_B = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R94)", "## Registerblock — zeichengleich kopierbar, nummeriert (ab R97)"
TITEL58 = "## 58. Fable 14a und 14b — Registerblock R94–R97 (TB-162)"
# (Ort, Bereich-Anfang, Wort, R, Unterabschnitt, Fable, Unterpunkte) - R96 (d) (14a) und R97 (e) (14b); je Ort in dieser Reihenfolge
MARKEN = [("Abschnitt 27", "## 27. ", "ERGÄNZT", "R94", "58.1", "14a", "Unterpunkte (a) und (b) (zu 27.2)"),
          ("Abschnitt 27", "## 27. ", "ERGÄNZT", "R97", "58.4", "14b", "Unterpunkt (b) (zu R94 (b) und 27.2)"),
          ("48.13 R45", "### 48.13 ", "PRÄZISIERT", "R95", "58.2", "14a", "Unterpunkte (a) und (b)"),
          ("48.13 R45", "### 48.13 ", "ERGÄNZT", "R97", "58.4", "14b", "Unterpunkt (b)"),
          ("48.14 R46", "### 48.14 ", "ERGÄNZT", "R94", "58.1", "14a", "Unterpunkte (a) und (b)"),
          ("56.1 R84", "### 56.1 ", "PRÄZISIERT", "R95", "58.2", "14a", "Unterpunkte (a) und (b)")]
# Marken in 58 selbst (R97 (e)): an R95 (58.2) und R96 (58.3), nach der Quellenzeile
MARKEN58 = [("58.2 R95", 1, "BERICHTIGT", "R97", "58.4", "14b", "Unterpunkt (a)"), ("58.3 R96", 2, "BERICHTIGT", "R97", "58.4", "14b", "Unterpunkt (d)")]
ZEICHENGLEICH = "> Eintrag und Stand oben bleiben zeichengleich."
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
def gitrc(*a): r = subprocess.run(["git"] + list(a), capture_output=True, text=True); return r.returncode, r.stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def abschnitt(txt, n):
    z = txt.split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## %d. " % n)]
    if len(a) != 1: return None
    e = next((i for i in range(a[0] + 1, len(z)) if re.match(r"## \d+\. ", z[i])), len(z)); return "\n".join(z[a[0]:e])
def bloecke_aus(datei, kopf, rr):
    z = lies(datei).split("\n"); a = z.index(kopf) + 1
    while z[a] == "": a += 1
    assert z[a] == "```"; e = z.index("```", a + 1); b = [l for l in z[a + 1:e] if l]
    soll = [x for r in rr for x in (r + " — ", "Quelle")]
    assert [l[:6] for l in b] == soll, [l[:6] for l in b]
    return [(b[i], b[i + 1], a + 2 + z[a + 1:e].index(b[i])) for i in range(0, len(b), 2)]
def bloecke():
    """[(R-Zeile, Quellenzeile, Zeile in der Fable-Datei, Datei)] fuer R94, R95, R96 (14a) und R97 (14b)."""
    return [x + (FA,) for x in bloecke_aus(FA, KOPF_A, ("R94", "R95", "R96"))] + [x + (FB,) for x in bloecke_aus(FB, KOPF_B, ("R97",))]
def voraussetzung():
    hk = lies("research/vorregistrierung/herkunft.py").split("\n")[101:106]
    for m in ("shared/messkette.py", "shared/zuteilung.py", "strategies/*/equity_simulation.py", "strategies/*/multi_symbol_optimise.py", "strategies/*/multi_symbol_walk_forward.py"):
        p(any('"%s"' % m in l for l in hk), "R94: Sperrliste herkunft.py Z. 102-106 nennt %s" % m)
    p(len(git("ls-files", "strategies/*/multi_symbol_walk_forward.py").split()) == 9, "R94: neun Walk-Forward-Rechner verfolgt (die sechs Rechner und drei Erben)")
    A, D = git("show", "3f2e97e:" + REG), git("show", "d950e03:" + REG)
    for n in (9, 11, 24, 37, 41, 51, 54):
        x, y = abschnitt(A, n), abschnitt(D, n); p(x is not None and x == y, "R94/R96 (b)/R97 (f): Abschnitt %d am Stand 3f2e97e zeichengleich mit d950e03" % n)
    rc, aus = gitrc("log", "--format=%h", "3f2e97e..HEAD", "--", REG); p(rc == 0 and aus.strip() == "", "Register seit 3f2e97e unveraendert")
    for f in ("research/tb24_haltedauern/positionen_holen.py", "shared/zuteilung.py"):
        rc, aus = gitrc("log", "--format=%h", "7b9f9ac..HEAD", "--", f); rc2, aus2 = gitrc("diff", "--name-only", "HEAD", "--", f)
        p(rc == 0 and rc2 == 0 and aus.strip() == "" and aus2.strip() == "", "F11 (3)/R97 (f): %s am HEAD unveraendert gegen 7b9f9ac (Verhalten nach der Wiedergabe in 14.10.b)" % f)
    for f in SECHS:
        p(bool(git("ls-files", "--error-unmatch", f).strip()) and git("diff", "--name-only", "HEAD", "--", f).strip() == "", "F11 (1)/R56 (b): %s verfolgt, gleich HEAD" % f)
    p(md5(lies(FA)) == FA_MD5, "Fable-Datei 14.10.a md5 %s" % FA_MD5); p(md5(lies(FB)) == FB_MD5, "Fable-Datei 14.10.b md5 %s" % FB_MD5)
    reg = lies(REG); p(not re.search(r"^## 58\. ", reg, re.M) and not re.search(r"\bR9[4567]\b", reg), "R94-R97 und Abschnitt 58 noch nicht im Register")
    ende()
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    z = lies(REG).split("\n"); bl = bloecke(); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1] == "Pruefungen: %d, NEIN: 0" % sum(1 for l in vb if l.startswith(("ja ", "NEIN"))), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    einf = []
    for ort, anfang, wort, rr, ua, fb, up in MARKEN:
        a = [i for i, l in enumerate(z) if l.startswith(anfang)]
        if not p(len(a) == 1, "Ort %s (%s): Anfang genau einmal" % (ort, rr)): continue
        tief = "## " if anfang.startswith("## ") else "### "
        e = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or (tief == "### " and z[i].startswith("### ")))
        zg = [i for i in range(a[0], e) if z[i] == ZEICHENGLEICH]
        p(bool(zg) and not any(rr in z[i] for i in range(a[0], e)), "Ort %s: letzte Marke Z. %s, %s dort noch nicht genannt" % (ort, zg[-1] + 1 if zg else "?", rr))
        if zg: einf.append((zg[-1] + 1, ["", "> ⭐ **%s %s durch %s (%s)** (Fable %s %s, %s, TB-162, %s)." % (ort, wort, rr, ua, fb, rr, up, datum), ZEICHENGLEICH]))
    titel = []
    for zeile, _, _, _ in bl:
        t = zeile.split(". (a) ")[0] if ". (a) " in zeile else zeile.split(" (a) ")[0]; t = t[:-1] if t.endswith(".") else t
        if len(t) > 140: t = t[:139].rsplit(" ", 1)[0] + "…"
        titel.append(t)
    kette = ["**Kette:** Marken: Abschnitt 27; 48.14 (R46). Indexzeilen ohne Marke (R96 (d)): 48.20 (R52); 54.3 (R76). Zu (b): R97 (b) (58.4); R94 bleibt unverändert (R97 (c)).",
             "**Kette:** Marken: 48.13 (R45); 56.1 (R84). Unterpunkt (a) BERICHTIGT durch R97 (a) (58.4).",
             "**Kette:** Marken: keine. Unterpunkt (c) BERICHTIGT durch R97 (d) (58.4): gezählt sind fünfzehn Fälle.",
             "**Kette:** Marken nach R97 (e): 58.2 (R95); 58.3 (R96); 48.13 (R45); Abschnitt 27. Indexzeilen 48.20 (R52) und 54.3 (R76): fünfzehn Fälle (R97 (d)); Abschnitt 10, Punkt 10: R97 (b). Voraussetzungen und Befunde: 58.5."]
    gr = lambda f: format(len(lies(f).encode("utf-8")), ",").replace(",", " ")
    kopf = ("Reines Eintragen von Registertext, Bauart wie 57. Quellen sind allein `%s`, md5 `%s`, %s B, Abschnitt "
            "„Registerblock — zeichengleich kopierbar, nummeriert (ab R94)“, Z. %d–%d (58.1–58.3), und `%s`, md5 `%s`, %s B, Abschnitt "
            "„Registerblock — zeichengleich kopierbar, nummeriert (ab R97)“, Z. %d–%d (58.4), beide im Repo seit Commit `%s`. Nicht eingetragen werden Leseprotokoll, Teile und „Unsicher“ der Antworten. "
            "Zum Dialog gehören die Anfragen 14.10.a und 14.10.b und die Übergaben vom 14.10.2026 (a und b; alle seit `%s`). Eingetragen am %s mit TB-162 "
            "(Entscheide F5 vom 14.10.2026, 21:58, und F10–F12 vom 15.10.2026, 08:08, des steuernden Chats).") % (
            FA, FA_MD5, gr(FA), bl[0][2], bl[2][2] + 1, FB, FB_MD5, gr(FB), bl[3][2], bl[3][2] + 1, s0, s0, datum)
    neu = ["", TITEL58, "", kopf, ""]
    m58 = {k: ["", "> ⭐ **%s %s durch %s (%s)** (Fable %s %s, %s, TB-162, %s)." % (ort, wort, rr, ua, fb, rr, up, datum), ZEICHENGLEICH] for ort, k, wort, rr, ua, fb, up in MARKEN58}
    for k, ((zeile, quelle, _, _), t) in enumerate(zip(bl, titel)):
        neu += ["### 58.%d %s" % (k + 1, t), "", "> " + zeile, "> " + quelle] + m58.get(k, []) + ["", kette[k], ""]
    neu += ["### 58.5 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `docs/belege/TB-162/v_voraussetzung.txt` (Werkzeug `voraussetzung`, Anhang B des Auftrags TB-162), Zeilen wörtlich:", ""]
    neu += ["    " + l for l in vb] + [""]
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    p(len(einf) == len(MARKEN), "%d Marken am alten Ort (R96 (d), R97 (e)), 2 in 58 (R97 (e))" % len(einf))
    if probe or any(l.startswith("NEIN") for l in OUT): ende()
    for at in sorted(set(x[0] for x in einf), reverse=True): z[at:at] = [l for a2, zz in einf if a2 == at for l in zz]
    z = z[:-1] + neu; schreibe(REG, "\n".join(z))
    r2 = lies(REG).split("\n"); mz = [(i + 1, l) for i, l in enumerate(r2) if l.startswith("> ⭐ **") and ("(Fable 14a R9" in l or "(Fable 14b R97" in l) and "TB-162" in l]
    soll = ["> ⭐ **%s %s durch %s (%s)**" % (m[0], m[2], m[3], m[4]) for m in MARKEN + MARKEN58]
    zu = {s: [n for n, l in mz if l.startswith(s)] for s in soll}
    json.dump({"marken": [[m[0], m[2], m[3], m[4], (zu[s] or [0])[0]] for m, s in zip(MARKEN + MARKEN58, soll)], "abschnitt_58": r2.index(TITEL58) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(len(mz) == 8 and all(len(v) == 1 for v in zu.values()), "nachher: 8 Marken Z. %s; Abschnitt 58 Z. %d" % ([n for n, _ in mz], r2.index(TITEL58) + 1))
    p(all(r2.count("> " + b[0]) == 1 and r2.count("> " + b[1]) == 1 for b in bl), "R94-R97 mit Quellenzeile je genau einmal zeichengleich im Register")
    ende()
def index(s0, datum, probe):
    d = json.load(open("docs/belege/TB-162/r_daten.json", encoding="utf-8")); mk = d["marken"]; mz = [m[4] for m in mk]
    p(len(mk) == 8 and all(mz), "r_daten.json: 8 Marken mit Zeile")
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 58. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 58 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    x = lies(IDX); z = x.split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–57" in z[k[0]], "Kopf genau einmal, nennt 0–57"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–57", "Abschnitte 0–58")
    zus = {"| 27 Sichtschutz |": "; Abschnitt 27 ERGÄNZT durch R94 (58.1) (Z. %d); Abschnitt 27 ERGÄNZT durch R97 (58.4) (Z. %d)" % (mz[0], mz[1]),
           "| 48 aus 29b |": "; 48.13 R45 **PRÄZISIERT durch R95 (58.2)** (Z. %d); 48.13 R45 ERGÄNZT durch R97 (58.4) (Z. %d); 48.14 R46 ERGÄNZT durch R94 (58.1) (Z. %d)" % (mz[2], mz[3], mz[4]),
           "| 56 aus 09a |": "; 56.1 R84 **PRÄZISIERT durch R95 (58.2)** (Z. %d)" % mz[5]}
    for anf, t in zus.items():
        i = [j for j, l in enumerate(z) if l.startswith(anf)]
        if p(len(i) == 1 and z[i[0]].endswith(" |"), "Index-Zeile %s genau einmal" % anf): z[i[0]] = z[i[0]][:-2] + t + " |"
    i = [j for j, l in enumerate(z) if l.startswith("| 57 aus 10a |")]
    if p(len(i) == 1, "Zeile 57 genau einmal"): z.insert(i[0] + 1, "| 58 aus 14a und 14b | %s | R94–R96 (58.1–58.3, 14a); R97 (58.4, 14b); 58.5 Voraussetzungen und Befunde | 58.2 R95 **BERICHTIGT durch R97 (58.4)** (Z. %d); 58.3 R96 **BERICHTIGT durch R97 (58.4)** (Z. %d) |" % (T, mz[6], mz[7]))
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    tab = ["## 13. Die Marken aus Fable 14a und 14b (TB-162)", "", "Alle 8 Marken, die TB-162 nach R96 (d) und R97 (e) gesetzt hat (6 am alten Ort, 2 in 58), in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-162/r_daten.json`.", "",
           "| Ort | Marke | Wort | durch | T |", "|---|---|---|---|---|"]
    for ort, wort, rr, ua, zz in sorted(mk, key=lambda m: m[4]): tab.append("| %s | Z. %d | %s | %s (%s) | %s |" % (ort, zz, wort, rr, ua, T))
    tab += ["", "### Indexzeilen aus Fable 14a und 14b", "",
            "- **48.20 (R52):** Zählung der Fälle „Bestand behauptet statt Voraussetzung genannt“ → R96 (c) (58.3) mit R97 (d) (58.4): fünfzehn gezählte Fälle; der fünfzehnte ist „ein solches Modul schreibt keines“ in R95 (a). In R96 (c) lies „Gezählt sind fünfzehn Fälle.“ Ohne Marke (R96 (d), R97 (e)). Der Index ist kein Registertext.",
            "- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R97 (d) (58.4): fünfzehnter Fall. Ohne Marke (R97 (e)). Der Index ist kein Registertext.",
            "- **Abschnitt 10, Punkt 10:** → R97 (b) (58.4): die ausgeführten Positionen aus der Rückgabe nach R45 mit R84 (e), nachdem Punkt 10 nach 37.3 beauftragt und freigegeben ist; bis dahin Rekonstruktion. Ohne Marke (R97 (e)). Der Index ist kein Registertext.", "", "---", ""]
    if p(len(i) == 1 and z[i[0] - 2] == "---", "Pflege-Anker genau einmal, davor '---'"): z[i[0] - 1:i[0] - 1] = [""] + tab[:-2]
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-154 (")]
    if p(len(j) == 1, "Pflegezeile TB-154 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-154 (", "In TB-154 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-162 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-162 (`index`); 58 (R94–R97) kommt zu T%s; neuer Abschnitt 13 (8 Marken)." % (datum, s0, rcm, T))
    if not probe and not any(l.startswith("NEIN") for l in OUT): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"14a": {"frage": "Ist eine Messung des Kapital-Drawdowns im Walk-Forward mit Rastersuche und IS-Sieger vor dem signierten Tag ein Versuch, was darf vor dem Tag gemessen werden, und bindet der Satz zum zweiten Rechenweg aus R45 ein Forschungsmodul ausserhalb des Laufs?",
                       "entscheidung": "Rastersuche und faltenweise Auswahl auf den Kursdaten der Bots sind vor dem Tag Versuch und unterbleiben (R94 (a), (c)); zulässig bleibt E und M der heutigen Parameter, auch in den Fenstern des bot-eigenen Walk-Forward, als Tatsachennotiz (R94 (b)); der Satz aus R45 bindet den Lauf, nicht ein Forschungsmodul ausserhalb (R95); Tatsachennotizen und Marken in R96.",
                       "offen": "ja"},
               "14b": {"frage": "Verstösst der Doppellauf aus positionen_holen.py gegen A9, und woher nimmt eine Messung nach R94 (b) vor dem Tag die ausgeführten Positionen?",
                       "entscheidung": "Ja, der Doppellauf verstösst gegen A9 und ist historischer Stand; R95 (a) in „lies“-Form berichtigt (R97 (a)). Positionen aus der Rückgabe nach R45 mit R84 (e), sobald Punkt 10 nach 37.3 freigegeben ist; bis dahin Rekonstruktion aus Trade-Liste und equity_curve, als solche benannt (R97 (b)); fünfzehnter gezählter Fall (R97 (d)).",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 14a und 14b geschrieben: %s" % ziel)
def kennung():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); print("Kennung %s%s (letzte %s)" % (h[0], chr(ord(h[1]) + 1), h))
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); neu = h[0] + chr(ord(h[1]) + 1)
    b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-162: " % neu), "Kopfzeile ## %s — TB-162: …" % neu); p(len(i) == 1, "Anker genau einmal")
    p(i and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "davor '---' und Leerzeile"); p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---")
    p("### Was gemessen ist" in b, "Teil 'Was gemessen ist'"); p(neu not in k, "Kennung %s frei" % neu)
    if not probe and not any(l.startswith("NEIN") for l in OUT): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["kennung"]: kennung()
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
