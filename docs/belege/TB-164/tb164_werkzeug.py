#!/usr/bin/env python3
"""TB-164 Werkzeug (Anhang B): Voraussetzungen, Auswahl aus dem Sonden-Beleg, Register 60 (Vollzug TB-163 nach 37.3; Tatsachennotiz Posten 5 nach R43), Index, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  voraussetzung                           Voraussetzungen messen (rc 0 = alle ja)
  sonde <BELEG> <VOR> <NACH>              Fassung des Sondensatzes aus dem Beleg waehlen; Richtigstellung zu ERGEBNIS_TB-163 Z. 129
  register <DATUM> <S0> <BELEG> [--probe] Abschnitt 60 am Registerende anhaengen (60.1 zeichengleich aus ERGEBNIS_TB-163 Z. 111-123; 60.2 Posten 5)
  index <S0> <DATUM> [--probe]            REGISTER_INDEX.md: Kopf 0-60, Zeile 60, Pflegezeile (nach c2_index_zeilen.py)
  backlog <DATUM> <KENNUNG> [--probe]     BACKLOG: Rang 1; zwei Zeilen nach 'Scan-Schleifen in research/'
  kennung | journal <BLOCK> [--probe]     naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, os, re, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
ERG, ERG_MD5, ERG_COMMIT, UEB = "docs/ERGEBNIS_TB-163_register59_posten4_horizont.md", "9e4c8f7df087bb25f3b7dba93e51119e", "d81dc88", "docs/belege/TB-163/e_uebergang.md"
AB, AB_SHA, SO, SO_SHA = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json", "46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f", "shared/sperrlistensonde.py", "98c02e0e9b42831d88e0cd9cbdc39d64c458691fdbf1e650aa4e32c933cc0d71"
KARTE, Z503, E6 = "TB-164 bauen — Registerabschnitt 60 „Vollzug TB-163“ (Hash-Übergang 37.3, Bauart 50.3, Entwurf ERGEBNIS_TB-163 Z. 109–123 zeichengleich) + Tatsachennotiz Posten 5 (R43); vorher Sonde lesend messen, Z. 129 richtigstellen; kein neues Abbild; ohne Prüferrunde (Ja, Recommended).", "11198–11242", "11a267f"
SONDE_BEFEHL = "trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild " + AB
TITEL59 = "## 59. Tatsachennotiz TB-162 — "
TITEL60 = "## 60. Vollzug TB-163 (Tatsachennotiz nach 37.3) und Tatsachennotiz Posten 5 (TB-164)"
R43A, R43E, R43P = "Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“", "die neun Optimierer erhalten eine Tatsachennotiz „nicht im Laufpfad“.", "Posten 5 des Plans ist neu zu fassen (Handwerk)."
S373 = "Ein Befund 1 der Sperrlisten-Sonde"
P5F, P5Z, P5B = "docs/auftraege/MAC_TB-120_erzeuger_bestandsaufnahme.md", "- Posten 5: Wache 29.4 in allen neun Optimierern (34.5).", "docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md"
BB, BBZ = "strategies/volatility_breakout/backtest_breakout.py", "entry_time >= np.datetime64(entry_cutoff)"
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", " · Posten 4 (E-6, Horizont je Bot) erledigt mit TB-163 (15.10.2026, Journal EZ) |"
SCAN = "- **Scan-Schleifen in `research/`:**"
Z129 = "Bis dahin meldet die Sperrlisten-Sonde zu Punkt 11 einen zulässigen Befund `1` (beauftragt, Freigabe dritte Karte)."
FASSUNG = {"2": "nicht prüfbar", "1": "Befund 1 (beauftragt)"}
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def neun(): return sorted(x for x in git("ls-files", "strategies/*/multi_symbol_optimise.py").split("\n") if x)
def quelle():
    e = lies(ERG); z = e.split("\n"); return e, z, z[110:123]
def zeile(pred):
    t = [i for i, l in enumerate(lies(REG).split("\n")) if pred(l)]; return t[0] + 1 if len(t) == 1 else None
def r43():
    z = lies(REG).split("\n"); t = [i for i, l in enumerate(z) if l.startswith("> R43 — ")]
    if len(t) != 1: return None
    s = z[t[0]]; a, b = s.find(R43A), s.find(R43E)
    if s.count(R43A) != 1 or s.count(R43E) != 1 or s.count(R43P) != 1 or b < a: return None
    return t[0] + 1, s[a:b + len(R43E)]
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def fassung(beleg):
    """Punkt 11 aus dem Beleg: '2' (nicht pruefbar, Rueckgabe 2 ohne Befund) oder '1' (Befund nur an Punkt 11); sonst None."""
    z = lies(beleg).rstrip("\n").split("\n"); m = [re.match(r"^  Punkt 11  \[(\d) ", l) for l in z]; m = [x.group(1) for x in m if x]
    rw = [l for l in z if l.startswith("RUECKGABEWERT ")]; rc = z[-1] if z else ""
    if len(m) != 1 or len(rw) != 1: return None, m, rw, rc
    if m[0] == "2" and rc == "rc 2" and rw[0].startswith("RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [") and re.search(r"[\[ ]11[,\]]", rw[0]): return "2", m, rw, rc
    if m[0] == "1" and rc == "rc 1" and rw[0] == "RUECKGABEWERT 1 BEFUND - BEFUND in Punkt(en) [11]": return "1", m, rw, rc
    return None, m, rw, rc
def satz(f, s0):
    kopf = "**Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-164 am Stand `%s`; Aufruf wie TB-122 0b: `%s`, Abbild `%s…`; Beleg `docs/belege/TB-164/s_sonde.txt`): " % (s0, SONDE_BEFEHL, AB_SHA[:8])
    if f == "2": return kopf + "Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keinen der Optimierer (kein Pfad `strategies/*/multi_symbol_optimise.py` darin) — wie bei 50.3. Der Übergang steht deshalb nur hier und in den Commits."
    return kopf + "Punkt 11 „Befund 1 (beauftragt)“ (`1`). Vor dem Tag zulässig nach 37.3, weil beauftragt (Freigabe: dritte Karte des Betreibers, 15.10.2026, 18:24); geschlossen wird er durch ein neues Abbild unter neuem Namen (37.3), das TB-164 nicht zieht (Karte 15.10.2026, 19:27)."
def richtig(f):
    z373 = zeile(lambda l: S373 in l.replace("**", ""))
    a = "Richtigstellung zu `%s` Z. 129 (dort: „%s“): gemessen in TB-164 (`docs/belege/TB-164/s_sonde.txt`) " % (ERG, Z129)
    if f == "2": a += "meldet die Sonde zu Punkt 11 `2` „nicht prüfbar“, nicht `1`: das Abbild `sperrliste_abbild_2026-09-26_tb117.json` führt die Optimierer nicht (wie Register 50.3). Der Satz in Z. 129 war erschlossen, nicht gemessen."
    else: a += "meldet die Sonde zu Punkt 11 `1` — der Satz in Z. 129 ist bestätigt."
    return a + " Der Übergang steht mit Register 60 im Register; ein neues Abbild zieht TB-164 nicht (Karte 15.10.2026, 19:27; 37.3, Register Z. %s). ERGEBNIS_TB-163 bleibt unverändert." % z373
def voraussetzung():
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith(TITEL59) for l in z) == 1 and not re.search(r"^## 60\. ", reg, re.M), "Register: 59 genau einmal, 60 noch nicht")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    p(str(zeile(lambda l: l.startswith("### 50.3 Vollzug TB-122 (Tatsachennotiz nach 37.3)"))) == Z503.split("–")[0], "Register: Vorbild 50.3 genau einmal, Z. %s" % Z503)
    r = r43(); p(r is not None, "Register: R43-Wortlaut (Wache, „nicht im Laufpfad“, Posten 5 neu zu fassen) genau einmal (Z. %s)" % (r[0] if r else "?"))
    p(zeile(lambda l: S373 in l.replace("**", "")) is not None, "Register: 37.3 „%s“ genau einmal" % S373)
    e, ez, q = quelle()
    p(md5(e) == ERG_MD5, "ERGEBNIS_TB-163 md5 %s" % ERG_MD5)
    p(git("log", "--format=%h", "-1", "--", ERG).strip()[:7] == ERG_COMMIT, "ERGEBNIS_TB-163 zuletzt in Commit %s" % ERG_COMMIT)
    p(ez[108].startswith("### Entwurf Tatsachennotiz Hash-Übergang nach 37.3") and ez[109] == "" and q[0].startswith("Freigabe: dritte Karte des Betreibers, 15.10.2026, 18:24") and q[1] == ""
      and q[2].startswith("**Hash-Übergänge nach 37.3**") and q[-1].startswith("Unverändert: ") and ez[123] == "" and ez[124].startswith("**`herkunft.register()`**"), "ERGEBNIS_TB-163: Grenzen Z. 109 Kopf, Z. 111-123 Entwurf, Z. 124 leer, Z. 125 herkunft.register()")
    p("\n".join(q[2:]) + "\n" == lies(UEB), "ERGEBNIS_TB-163 Z. 113-123 = %s" % UEB)
    p(Z129 in ez[128], "ERGEBNIS_TB-163 Z. 129 enthält den Satz zur Sonde")
    for l in q[6:10]:
        f, nach = l.split(" | ")[0][3:-1], l.split(" | ")[2].strip("`")
        p(sha(f) == nach and l.split(" | ")[3] == "`%s`" % E6, "sha256 heute = nachher %s (%s…, %s)" % (f, nach[:16], E6))
    p(git("log", "--format=%h", "-1", E6).strip()[:7] == E6, "Commit %s vorhanden" % E6)
    p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild %s… und Sonde %s…" % (AB_SHA[:16], SO_SHA[:16]))
    p("multi_symbol_optimise" not in lies(AB), "Abbild führt keinen Optimierer")
    p(len(neun()) == 9, "neun Optimierer verfolgt")
    p(lies(P5F).split("\n")[127] == P5Z and "Posten 5: **0/9**" in lies(P5B).split("\n")[100], "Posten 5 alt (MAC_TB-120 Z. 128), Bestand 0/9 (ERGEBNIS_TB-120 Z. 101)")
    p(BBZ in lies(BB).split("\n")[210], "backtest_breakout.py Z. 211 enthält %s" % BBZ)
    ix = lies(IDX).split("\n")
    p(sum(l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `") and "Abschnitte 0–59" in l for l in ix) == 1 and sum(l.startswith("| 59 Tatsachennotiz TB-162 |") for l in ix) == 1
      and sum(l.startswith("Zuletzt nachgezogen in TB-163 (") for l in ix) == 1, "Index: Kopf 0–59, Zeile 59, Pflegezeile TB-163 je genau einmal")
    bl = lies(BL).split("\n")
    p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl) == 1 and sum(l.startswith(SCAN) and "vor E-6 bzw. Posten 5" in l for l in bl) == 1, "BACKLOG: Rang 1 (Stand TB-163) und Scan-Schleifen je genau einmal")
    k = kennungen(); p(max(k) == "EZ" and naechste(max(k)) not in k, "Journal: höchste Kennung %s, nächste %s frei" % (max(k), naechste(max(k))))
    ende()
def sonde(beleg, vor, nach):
    p(lies(vor) == lies(nach), "git status --porcelain vor und nach der Sonde gleich (%d Zeilen)" % len([l for l in lies(vor).split("\n") if l]))
    p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild %s… und Sonde %s…" % (AB_SHA[:16], SO_SHA[:16]))
    f, m, rw, rc = fassung(beleg)
    p(f is not None, "Punkt 11 im Beleg: %s · %s · %s" % (m, rw[0][:160] if rw else "kein RUECKGABEWERT", rc))
    if f:
        print("Fassung: %s" % FASSUNG[f]); print("Satz 60.1 (⟨S0⟩ setzt WZ register): " + satz(f, "⟨S0⟩")); print(richtig(f))
    ende()
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    f = fassung(beleg)[0]; p(f is not None, "Fassung aus dem Beleg: %s" % FASSUNG.get(f, "keine"))
    e, ez, q = quelle(); p(md5(e) == ERG_MD5 and len(q) == 13, "Quelle ERGEBNIS_TB-163 md5 %s, Z. 111-123 (13 Zeilen)" % ERG_MD5)
    r = r43(); p(r is not None, "R43-Wortlaut genau einmal"); nn = neun(); p(len(nn) == 9, "neun Optimierer")
    z = lies(REG).split("\n"); p(not any(l.startswith("## 60. ") for l in z) and z[-1] == "" and z[-2] != "", "60 noch nicht im Register; endet mit einer Leerzeile")
    p("multi_symbol_optimise" not in lies(AB), "Abbild führt keinen Optimierer")
    if nein(): ende()
    kopf = ("Reines Eintragen, Bauart 50.3 (Register Z. %s); Karte des Betreibers 15.10.2026, 19:27: „%s“ Eingetragen am %s mit TB-164 (Stand `%s`). "
            "Nichts entfernt, kein bestehender Satz umgeschrieben; kein neues Abbild; keine Marke.") % (Z503, KARTE, datum, s0)
    q1 = ("*Übernommen zeichengleich aus dem Entwurf in `%s` Z. 111–123 (Commit `%s`, md5 `%s`); Z. 109 ist die Überschrift des Entwurfs und gehört nicht dazu; Z. 113–123 sind `%s`. Vollzogen in Commit `%s` (TB-163 E). "
          "„Entwurf, nicht eingetragen“ darin beschreibt den Stand im Ergebnis; eingetragen ist der Übergang mit diesem Abschnitt.*") % (ERG, ERG_COMMIT, ERG_MD5, UEB, E6)
    p5 = ("R43 (Register Z. %d): „%s“ — „%s“ Posten 5 lautete (`%s` Z. 128): „%s“ Bestand: 0 von 9 (`%s` Z. 101).") % (r[0], r[1], R43P, P5F, P5Z[2:], P5B)
    n5 = ("**Tatsachennotiz „nicht im Laufpfad“:** Die neun `multi_symbol_optimise.py` stehen nicht im Laufpfad der Neuselektion; die Wache 29.4/34.5 kommt in keinen von ihnen. "
          "Posten 5 heisst nach R43: die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ im Zellen-Erzeuger, an einer Stelle, für alle neun Bots, mit dem Bericht je Bot aus 34.5; "
          "sie kommt mit dem Bau des Zellen-Erzeugers. Stand der neun Dateien am `%s` (sha256, 39.5):") % s0
    tab = ["| Datei | sha256 |", "|---|---|"] + ["| `%s` | `%s` |" % (x, sha(x)) for x in nn]
    neu = ["", TITEL60, "", kopf, "", "### 60.1 Vollzug TB-163 (Tatsachennotiz nach 37.3)", "", q1, ""] + q + ["", satz(f, s0), "",
           "### 60.2 Tatsachennotiz Posten 5 (R43)", "", p5, "", n5, ""] + tab + [""]
    if probe: ende()
    alt = lies(REG); schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG); p(r2.startswith(alt[:-1]) and r2.count("\n" + TITEL60 + "\n") == 1, "nachher: altes Register unverändert vorn (append-only), 60 genau einmal, Z. %d" % (r2.split("\n").index(TITEL60) + 1))
    p("\n" + "\n".join(q) + "\n" in r2, "Z. 111-123 zeichengleich im Register"); p(r2.endswith("|\n"), "Register endet mit genau einer Leerzeile")
    ende()
def index(s0, datum, probe):
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 60. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 60 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–59" in z[k[0]], "Kopf genau einmal, nennt 0–59"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–59", "Abschnitte 0–60")
    i = [j for j, l in enumerate(z) if l.startswith("| 59 Tatsachennotiz TB-162 |")]
    if p(len(i) == 1, "Zeile 59 genau einmal"):
        z.insert(i[0] + 1, "| 60 Vollzug TB-163 | %s | 60.1 Hash-Übergang nach 37.3 (E-6, vier Aktien-Optimierer, Commit `%s`; aus ERGEBNIS_TB-163 Z. 111–123) mit Sonde zu Punkt 11; 60.2 Tatsachennotiz Posten 5 nach R43 („nicht im Laufpfad“, neun Optimierer) | – |" % (T, E6))
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-163 (")]
    if p(len(j) == 1, "Pflegezeile TB-163 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-163 (", "In TB-163 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-164 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-164 (`index`); 60 (Vollzug TB-163, Posten 5) kommt zu T%s." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n")
    a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-163"):
        z[a[0]] = z[a[0]][:-2] + " · Register 60 (Vollzug TB-163 nach 37.3; Posten 5 nach R43 neu gefasst) mit TB-164 (%s, Journal %s) |" % (datum, kenn)
    s = [i for i, l in enumerate(z) if l.startswith(SCAN)]
    if p(len(s) == 1 and "vor E-6 bzw. Posten 5" in z[s[0]], "BACKLOG-Zeile 'Scan-Schleifen in research/' genau einmal"):
        z[s[0] + 1:s[0] + 1] = [
            "- **Scan-Schleifen (Zeile oben), Bindung offen:** „vor E-6“ ist überholt — E-6 ist mit TB-163 erledigt, ohne dass die zwei Scan-Schleifen gebunden oder begründet wurden; offen bleibt „vor Posten 5“, und Posten 5 ist nach R43 die Wache im Zellen-Erzeuger (Register 60.2). (TB-164, %s)" % datum,
            "- **`backtest_breakout.py` Z. 211 bei tz-behaftetem `open_time`:** `%s` wirft TypeError (Befund TB-163, Abnahme B1; `%s` Z. 137–138); am Stand vor E-6 ebenso, heute sind alle Aktien-1d-Dateien naiv. In der Probe von TB-163 liefen deshalb für `volatility_breakout` mit tz-behaftetem `open_time` zwei Prüfungen nicht. Binden mit dem Zellen-/Listen-Erzeuger oder begründet lassen. Handwerk. (TB-164, %s)" % (BBZ, ERG, datum)]
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def kennung():
    h = max(kennungen()); print("Kennung %s (letzte %s)" % (naechste(h), h))
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); k = kennungen(); neu = naechste(max(k))
    b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-164: " % neu), "Kopfzeile ## %s — TB-164: …" % neu); p(len(i) == 1, "Anker genau einmal")
    p(i and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "davor '---' und Leerzeile"); p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---")
    p("### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Teile 'Was gemessen ist', 'In einfacher Sprache'"); p(neu not in k, "Kennung %s frei" % neu)
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "sonde": sonde(a[1], a[2], a[3])
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif a == ["kennung"]: kennung()
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
