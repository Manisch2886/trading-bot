#!/usr/bin/env python3
"""TB-172 Werkzeug (Anhang A): Verfahrensmessung R102 (d) (Lesen des Codes, nur das Ob) und R92 (c) (Form von open_time am Snapshot, je Datei gezaehlt, kein Kurs).
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel; importiert und startet kein Programm des Repos. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | r102d <BELEG> | r92c <BELEG> | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import ast, csv, datetime, hashlib, json, os, re, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-172/"
SNAP = "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2"
CODE = { "strategies/rsi2_mean_reversion/multi_symbol_optimise.py": "b325d38f55279e6b80839b6e12857849", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "58589cfbdc50a5e0c602014f88fe73ae", "strategies/rsi2_mean_reversion/equity_simulation.py": "774e7fecad93bdad38bcba5e568b7243", "strategies/turtle_soup_stocks/multi_symbol_optimise.py": "0d7398e704778a0cfb84424ff4d76486", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "d8f24c681d39e300a8bfd28580b446d6", "strategies/turtle_soup_stocks/equity_simulation.py": "f45e55aadcb9d03b4342ec32e8644914", "strategies/volatility_breakout/multi_symbol_optimise.py": "3ec15ddc4140e51e452ec0cddd43f18f", "strategies/volatility_breakout/backtest_breakout.py": "ea48150ccab663f981bd4fa3f772a06a", "strategies/volatility_breakout/equity_simulation.py": "dd5fa96bb927aecb26051fbaefb4a0cd", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "571076168d56f9e809ef0595f53d6e7d", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/MANIFEST.json": "e0f647ce41f55a918547bb505eb5ecbf", "snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2/config/sp500_top150.txt": "bf54515b89f6e6e9e458ff6e6c8dcae9" }
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; R105 (d) t3_supertrend unberührt |"
BOTS = (("rsi2_mean_reversion", "backtest_rsi2.py"), ("turtle_soup_stocks", "backtest_turtle_soup.py"), ("volatility_breakout", "backtest_breakout.py"), ("elliott_wave_stocks", None))
W102 = "(d) [Voraussetzung, vor der Neuerzeugung der Listen (R44) zu messen, nur das Ob (27.2): ob rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout Indikatorwerte aus Zeilen vor dem Horizontbeginn bilden."
W92 = "als Verfahrensmessung am Datenbestand des Snapshots (27.2), nur die Form: ob open_time in jeder Aktien-Tagesreihe als Kalenderdatum steht, ohne Zonenangabe und ohne Uhrzeit, die den Tag verschiebt; gezählt je Datei, kein Kurs wird gelesen oder genannt."
RC, HZ, CI, AB, RB = r"pd\.read_csv\(", r"horizontbeginn_ts\(", r"compute_indicators\(", r"data\[symbol\]\s*=", r"run_backtest\("
CUT, ST = r"\[\s*\w+\[\s*[\"']open_time[\"']\s*\]\s*>=", r"start_i\s*=\s*max\(\s*start_i\s*,.*entry_cutoff"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def kurz(s): s = s.strip(); return s if len(s) <= 200 else s[:199] + "…"
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "unveraendert seit dem Bau: %s md5 %s" % (f, m[:12]))
def funktion(datei, name):
    q = lies(datei); z = q.split("\n")
    for k in ast.walk(ast.parse(q)):
        if isinstance(k, ast.FunctionDef) and k.name == name:
            a = k.lineno
            if k.body and isinstance(k.body[0], ast.Expr) and isinstance(getattr(k.body[0], "value", None), ast.Constant) and isinstance(k.body[0].value.value, str): a = k.body[0].end_lineno + 1
            return [(n, z[n - 1]) for n in range(a, k.end_lineno + 1)]
    return []
def treffer(zeilen, muster): return [(n, l) for n, l in zeilen if re.search(muster, l) and not l.strip().startswith("#")]
def voraussetzung():
    code_gleich(); p(not os.path.exists(BEL + "m1_r102d.md") and not os.path.exists(BEL + "m2_r92c.md"), "Messbelege m1/m2 noch nicht da")
    reg = lies(REG).split("\n"); r102 = [l for l in reg if l.startswith("> R102 — ")]; r92 = [l for l in reg if l.startswith("> R92 — ")]
    p(len(r102) == 1 and W102 in r102[0], "Register: R102 genau einmal, (d) im Wortlaut"); p(len(r92) == 1 and W92 in r92[0], "Register: R92 genau einmal, (c) im Wortlaut")
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]; p(len(z) == 1 and z[0].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-171")
    p(max(kennungen()) == "FH", "Journal: hoechste FH (naechste FI)"); p(os.path.exists(SNAP + "/MANIFEST.json"), "Snapshot mit MANIFEST.json: " + SNAP[:22] + "…")
    ende()
def r102d(beleg):
    L = ["# TB-172 M1 — R102 (d), nur das Ob: bilden rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout Indikatorwerte aus Zeilen vor dem Horizontbeginn?", "",
         "Gelesen per `ast` und Zeilensuche (Werkzeug `r102d`); nichts ausgeführt, nichts importiert, kein Kurs. Wortlaut je Zeile höchstens 200 Zeichen; Kommentar- und Docstring-Zeilen zählen nicht als Code.", "",
         "Regel (vor der Messung im Auftrag geschrieben): **ja**, wenn weder in `load_all_symbol_data` (Optimierer) noch in `run_backtest` (Backtest-Modul) ein Zeilenschnitt an `open_time >=` steht und `entry_cutoff` im Backtest nur den Startindex `start_i` setzt; dann geht die eingelesene Reihe mit den Zeilen vor dem Horizontbeginn in `compute_indicators`. **nein**, wenn ein Zeilenschnitt vor der Übergabe `data[symbol] =` steht (Kontrolle: `elliott_wave_stocks`, E-6/TB-163).", "",
         "| Bot | Datei | Z. | Rolle | Wortlaut |", "|---|---|---|---|---|"]
    U = []
    def zeile(bot, datei, tr, rolle):
        for n, l in tr: L.append("| %s | `%s` | %d | %s | `%s` |" % (bot, datei, n, rolle, kurz(l).replace("|", "\\|").replace("`", "'")))
    for bot, bm in BOTS:
        mso = "strategies/%s/multi_symbol_optimise.py" % bot; f = funktion(mso, "load_all_symbol_data"); rc_, hz, cut, ci, ab = [treffer(f, m) for m in (RC, HZ, CUT, CI, AB)]
        for t, r in ((rc_, "Einlesen"), (hz, "Horizontbeginn"), (cut, "Zeilenschnitt"), (ci, "Indikatoren beim Laden"), (ab, "Übergabe")): zeile(bot, mso, t, r)
        da = p(bool(f and rc_ and hz and ab), "%s: load_all_symbol_data mit Einlesen, Horizontbeginn, Übergabe gefunden" % bot)
        schnitt = bool(cut and ab) and cut[0][0] < ab[0][0]
        if bm is None:
            p(schnitt, "Kontrolle %s: Zeilenschnitt vor der Übergabe erkannt" % bot); U.append("KONTROLLE %s: %s" % (bot, ("nein (Zeilenschnitt Z. %d)" % cut[0][0]) if schnitt else "kein Schnitt erkannt")); continue
        g = funktion(mso, "get_trades_for_symbol"); ci2, rb = treffer(g, CI), treffer(g, RB); zeile(bot, mso, ci2, "Indikatoren je Lauf"); zeile(bot, mso, rb, "Backtest")
        bd = "strategies/%s/%s" % (bot, bm); r = funktion(bd, "run_backtest"); st, cut2 = treffer(r, ST), treffer(r, CUT); zeile(bot, bd, st, "entry_cutoff setzt Startindex"); zeile(bot, bd, cut2, "Zeilenschnitt")
        p(bool((ci or ci2) and rb and st), "%s: compute_indicators, run_backtest, start_i aus entry_cutoff gefunden" % bot)
        U.append("URTEIL R102 (d) %s: %s" % (bot, "ja" if da and not cut and not cut2 else "nein"))
    for datei, fn, m, rolle in (("research/tb24_haltedauern/positionen_holen.py", "lesesicht_an", r"_vor_schnitt\(", "Erzeuger: Sicht nur am Schnitt"), ("research/exposure_messung/bot_lauf.py", "_schranke_je_symbol", r"neu\[symbol\]\s*=\s*\(df,", "Erzeuger: df unverändert")):
        f = funktion(datei, fn); t, c = treffer(f, m), treffer(f, CUT); zeile("Erzeuger", datei, t + c, rolle); p(bool(t) and not c, "%s %s: gefunden, kein Zeilenschnitt an open_time >=" % (datei, fn))
    L += ["", "## Urteil (erschlossen am Code, nicht durch Lauf)", ""] + ["- " + u for u in U] + ["", "Bei **ja**: Befund zu 28.6 und R57, kommt als Frage an den Verfahrensprüfer (R102 (d)); hier ist nichts entschieden."]
    schreibe(beleg, "\n".join(L) + "\n"); print("\n".join(U)); ende()
KL = (("D", re.compile(r"^\d{4}-\d{2}-\d{2}$")), ("M", re.compile(r"^\d{4}-\d{2}-\d{2}[ T]00:00(:00(\.0+)?)?$")),
      ("Z", re.compile(r"^\d{4}-\d{2}-\d{2}([ T][0-9:.]+)?\s*(Z|UTC|[+-]\d{2}:?\d{2})$")), ("U", re.compile(r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2}(\.\d+)?)?$")))
def klasse(v):
    for k, r in KL:
        if r.match(v):
            try: datetime.date(int(v[:4]), int(v[5:7]), int(v[8:10]))
            except ValueError: return "X"
            return k
    return "X"
def r92c(beleg):
    m = json.loads(lies(SNAP + "/MANIFEST.json")); dat = m.get("dateien", {}); a = sorted(k for k in dat if k.endswith("_1d.csv") and "USDT" not in k and "/" not in k)
    sp = set(s.strip() + "_1d.csv" for s in lies(SNAP + "/config/sp500_top150.txt").split("\n") if s.strip() and not s.strip().startswith("#"))
    p(len(a) > 0, "MANIFEST: %d Aktien-Tagesreihen (Name *_1d.csv ohne USDT; Art %s)" % (len(a), sorted(set(dat[k].get("art", "?") for k in a))))
    L = ["# TB-172 M2 — R92 (c), nur die Form von open_time je Aktien-Tagesreihe des Snapshots", "", "Snapshot `%s`. Gelesen je Zeile nur das Feld `open_time` (csv, Standardbibliothek); kein Kurs gelesen oder genannt. Klassen: D nur Kalenderdatum `JJJJ-MM-TT` · M Datum mit `00:00[:00]` ohne Zone · Z mit Zonenangabe · U andere Uhrzeit ohne Zone · X sonst (leer, ungültig). Form erfüllt, wenn Spalte da, Zeilen > 0 und Z + U + X = 0." % SNAP, "",
         "Abgleich mit `config/sp500_top150.txt`: nur im MANIFEST %s · nur in der Liste %s" % (sorted(set(a) - sp)[:10], sorted(sp - set(a))[:10]), "",
         "| Datei | Zeilen | D | M | Z | U | X | doppelte Tage | sha256 = MANIFEST | Form |", "|---|---|---|---|---|---|---|---|---|---|"]
    S = dict.fromkeys("NDMZUX", 0); abw, sha_ok, dup_s = [], 0, 0
    for n in a:
        f = SNAP + "/" + n; z = dict.fromkeys("NDMZUX", 0); tage, dup, spalte = set(), 0, False; h = hashlib.sha256()
        with open(f, "rb") as fb:
            for blk in iter(lambda: fb.read(1 << 20), b""): h.update(blk)
        ok_sha = h.hexdigest() == dat[n].get("sha256"); sha_ok += ok_sha
        with open(f, encoding="utf-8", newline="") as fh:
            r = csv.reader(fh); kopf = next(r, [])
            if "open_time" in kopf:
                spalte, i = True, kopf.index("open_time")
                for row in r:
                    v = row[i].strip() if len(row) > i else ""; k = klasse(v); z["N"] += 1; z[k] += 1
                    if k in "DM": dup += v[:10] in tage; tage.add(v[:10])
        form = spalte and z["N"] > 0 and z["Z"] + z["U"] + z["X"] == 0
        if not form: abw.append(n)
        for k in S: S[k] += z[k]
        dup_s += dup
        L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %s | %s |" % (n, z["N"], z["D"], z["M"], z["Z"], z["U"], z["X"], dup, "ja" if ok_sha else "NEIN", "ja" if form else ("NEIN (keine Spalte open_time)" if not spalte else "NEIN")))
    L.append("| **Summe %d Dateien** | %d | %d | %d | %d | %d | %d | %d | %d ja | %d ja |" % (len(a), S["N"], S["D"], S["M"], S["Z"], S["U"], S["X"], dup_s, sha_ok, len(a) - len(abw)))
    p(sha_ok == len(a), "sha256 je Aktien-Datei = MANIFEST (%d von %d)" % (sha_ok, len(a)))
    u = ("URTEIL R92 (c): erfüllt (%d von %d Dateien: open_time Kalenderdatum, ohne Zone, ohne verschiebende Uhrzeit; D %d, M %d)" % (len(a), len(a), S["D"], S["M"])) if not abw else ("URTEIL R92 (c): nicht erfüllt (%d von %d Dateien weichen ab: %s)" % (len(abw), len(a), ", ".join(abw[:10])))
    L += ["", "## Urteil (gezählt)", "", "- " + u, "", "Nicht erfüllt: kommt mit der Fundstelle als Frage an den Verfahrensprüfer (R92 (c)); hier ist nichts entschieden."]
    schreibe(beleg, "\n".join(L) + "\n"); print("Summe: Dateien %d, Zeilen %d, D %d, M %d, Z %d, U %d, X %d, doppelte Tage %d" % (len(a), S["N"], S["D"], S["M"], S["Z"], S["U"], S["X"], dup_s)); print(u); ende()
def nachher():
    code_gleich()
    for b, n in (("m1_r102d", 3), ("m2_r92c", 1)):
        t = lies(BEL + b + ".txt").rstrip("\n").split("\n") if os.path.exists(BEL + b + ".txt") else [""]; md = lies(BEL + b + ".md") if os.path.exists(BEL + b + ".md") else ""
        p(t[-1] == "rc 0", "%s.txt endet mit rc 0" % b); p(len(re.findall(r"^- URTEIL R", md, re.M)) == n, "%s.md: %d Urteilszeile(n)" % (b, n))
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    m1 = lies(BEL + "m1_r102d.md") if os.path.exists(BEL + "m1_r102d.md") else ""; m2 = lies(BEL + "m2_r92c.md") if os.path.exists(BEL + "m2_r92c.md") else ""
    u1 = re.findall(r"^- URTEIL R102 \(d\) (\w+): (\w+)$", m1, re.M); u2 = re.findall(r"^- URTEIL R92 \(c\): (.*)$", m2, re.M)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    p(len(u1) == 3 and len(u2) == 1, "Urteile aus m1 (3) und m2 (1) gelesen")
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-171") and not nein():
        z[a[0]] = z[a[0]][:-2] + (" · **TB-172 (%s, Journal %s): Verfahrensmessung R102 (d) und R92 (c) (R86 (e) für die Aktien-Bots)** (R102 (d) durch Lesen des Codes, nur das Ob, ob Indikatorwerte aus Zeilen vor dem Horizontbeginn gebildet werden: %s; "
            "R92 (c) am Snapshot 63e4b6c8…, nur die Form von open_time je Aktien-Datei, kein Kurs: %s); Befunde gehen als Frage an den Verfahrensprüfer, hier nichts entschieden |") % (datum, kenn, ", ".join("%s %s" % x for x in u1), u2[0][:300])
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen())); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-172: " % neu), "Kopfzeile ## %s — TB-172: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 2 and a[0] == "r102d": r102d(a[1])
    elif len(a) == 2 and a[0] == "r92c": r92c(a[1])
    elif a == ["nachher"]: nachher()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
