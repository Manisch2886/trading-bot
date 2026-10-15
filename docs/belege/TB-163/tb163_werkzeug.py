#!/usr/bin/env python3
"""TB-163 Werkzeug (Anhang B): Voraussetzungen, Register 59 (Tatsachennotiz TB-162), Index, E-6 (Horizont je Bot), R81 (d), Hash-Uebergang, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. Schreibt nur die genannten Dateien; --probe schreibt nichts.
  voraussetzung                       Voraussetzungen messen (rc 0 = alle ja)
  register <DATUM> <S0> [--probe]     Abschnitt 59 am Registerende anhaengen (Notiz zeichengleich aus ERGEBNIS_TB-162 Z. 199-232)
  index <S0> <DATUM> [--probe]        REGISTER_INDEX.md: Kopf 0-59, Zeile 59, Pflegezeile (nach c2_index_zeilen.py)
  e6 [--probe]                        E-6: Horizont je Bot aus faltenplan.HORIZONTBEGINN in den vier Aktien-Optimierern
  r81d <TESTBELEG>                    R81 (d) nach E-6 pruefen (Code und Testbeleg)
  uebergang <E>                       Entwurf Tatsachennotiz Hash-Uebergang nach 37.3 (Sperrlistenpunkt 11)
  backlog <DATUM> <KENNUNG> [--probe] BACKLOG: Rang 1 und Zeile 'Vor der Neuerzeugung der Listen' (Posten 4 erledigt)
  kennung | journal <BLOCK> [--probe] naechste Journal-Kennung | Block vor '## Wiederkehrende Lehren' setzen
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, os, re, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
ERG, ERG_MD5, ERG_COMMIT = "docs/ERGEBNIS_TB-162_wf_kapital_dd.md", "210508624458a7287f89888a65304394", "16db5e3"
FP, BB = "research/vorregistrierung/faltenplan.py", "strategies/volatility_breakout/backtest_breakout.py"
TITEL59 = "## 59. Tatsachennotiz TB-162 — Kapital-Drawdown E und M je Abschnitt des bot-eigenen Walk-Forward (TB-163)"
R81D = "[Voraussetzung, mit Posten 4 zu messen: dass danach bei keinem der vier Bots das Ende einer Datei in Fenster, Scanbeginn oder Anfang der geladenen Zeilen eingeht.]"
DEF = "def load_all_symbol_data() -> dict:"
ALT = {"elliott_wave_stocks": '            cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)',
       "rsi2_mean_reversion": '            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)',
       "turtle_soup_stocks": '            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)',
       "volatility_breakout": '            entry_cutoff = df["open_time"].max() - pd.DateOffset(years=RECENT_YEARS_ONLY)'}
VOR = {
 "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "275273776fafb2453cdb41f634b86bacffd5994f8b5508ef034400cd7c5ede9d",
 "strategies/rsi2_mean_reversion/multi_symbol_optimise.py": "777f5cb0a637bb8770d1cd4a89aac03c6b29db98d13ce47eac6de29db279c661",
 "strategies/turtle_soup_stocks/multi_symbol_optimise.py": "e4277f013be6d0af85647f5d32d8cdb60ef086d06c6e041853c6da571c96ddd4",
 "strategies/volatility_breakout/multi_symbol_optimise.py": "f0a4ee43dca133e89272e48d80280d8a22f57d751d2ddac06751fd091198af2d",
 "research/vorregistrierung/faltenplan.py": "63dafeb44e027cb5d93ac19cddfc7d4e98b468cece116512c2b3f1601bd4a4c7",
 "strategies/volatility_breakout/backtest_breakout.py": "3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76"
}
NACH = {
 "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232",
 "strategies/rsi2_mean_reversion/multi_symbol_optimise.py": "61838aca901cabeace70511b71742d10cba4de6575a999aecf5a492f938ad6dc",
 "strategies/turtle_soup_stocks/multi_symbol_optimise.py": "29e7f10c3eb79f8316c53c9a31ee3ea0dd450d44bb9904dc2ba9944df003c0cc",
 "strategies/volatility_breakout/multi_symbol_optimise.py": "24c182ae1cf7c882c9e3aec31c5088348e2fa44c5cc2e99eab54ecf29b337585"
}
OUT = []
def p(ok, text): OUT.append(("ja    " if ok else "NEIN  ") + text); return ok
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def opt(b): return "strategies/%s/multi_symbol_optimise.py" % b
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def hilfe(bot):
    return ["def horizontbeginn_ts(spalte=None) -> pd.Timestamp:",
            '    """TB-163 (E-6, TB-30b Posten 4; R44, R81 (d), Register 26.2/28.4/28.5): der',
            "    Horizontbeginn des Bots aus research/vorregistrierung/faltenplan.py",
            "    (HORIZONTBEGINN ueber faltenplan.horizontbeginn) - ein Datum fuer alle Symbole",
            "    des Bots, nicht die letzte Zeile der Datei. Import erst beim Aufruf. Mit",
            "    `spalte` (open_time) in deren Zeitzone: naiv bleibt naiv, tz-behaftet",
            '    wird der Grenzwert auf die Spaltenzone lokalisiert."""',
            '    _vr = os.path.join(os.path.dirname(os.path.dirname(_STRATEGY_DIR)), "research", "vorregistrierung")',
            "    if _vr not in sys.path:", "        sys.path.insert(0, _vr)",
            "    import faltenplan  # noqa: E402",
            '    h = faltenplan.horizontbeginn("%s")' % bot,
            "    if h is None:", '        raise ValueError("%s: kein Horizontbeginn im Faltenplan")' % bot,
            "    t = pd.Timestamp(h)",
            '    tz = getattr(getattr(spalte, "dt", None), "tz", None) if spalte is not None else None',
            "    return t.tz_localize(tz) if tz is not None else t", "", ""]
def neu_text(bot, t):
    z = t.split("\n"); a = [i for i, l in enumerate(z) if l == ALT[bot]]; d = [i for i, l in enumerate(z) if l == DEF]
    if len(a) != 1 or len(d) != 1 or "horizontbeginn_ts" in t: return None
    var = ALT[bot].split("=")[0].rstrip()
    z[a[0]] = var + ' = horizontbeginn_ts(df["open_time"])  # TB-163 (E-6): Horizont aus faltenplan.HORIZONTBEGINN, nicht aus dem Dateiende (R81 (d), 28.4)'
    z[d[0]:d[0]] = hilfe(bot); return "\n".join(z)
def voraussetzung():
    hk = lies("research/vorregistrierung/herkunft.py").split("\n")[101:106]
    p(any('"strategies/*/multi_symbol_optimise.py"' in l for l in hk), "Sperrliste herkunft.py Z. 102-106 nennt strategies/*/multi_symbol_optimise.py (Punkt 11, 37.3)")
    for f, h in sorted(VOR.items()): p(sha(f) == h, "sha256 vorher %s = %s…" % (f, h[:16]))
    fp = lies(FP); p(fp.count('HORIZONTBEGINN = {"aktien": date(2016, 9, 19), "krypto": None}') == 1, "faltenplan.py: HORIZONTBEGINN-Literal genau einmal (aktien 2016-09-19)")
    reg = lies(REG); z = reg.split("\n")
    p(not re.search(r"^## 59\. ", reg, re.M) and sum(l.startswith("## 58. Fable 14a und 14b") for l in z) == 1, "Register: 58 genau einmal, 59 noch nicht")
    p(reg.count(R81D) == 1, "Register: Voraussetzung R81 (d) genau einmal (Z. %s)" % [i + 1 for i, l in enumerate(z) if R81D in l])
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    e = lies(ERG); ez = e.split("\n")
    p(md5(e) == ERG_MD5, "ERGEBNIS_TB-162 md5 %s" % ERG_MD5)
    p(ez[196].startswith("## Vorschlag Tatsachennotiz") and ez[198].startswith("> **Tatsachennotiz zu 24.2") and ez[232] == "" and ez[233] == "## Abweichungen" and all(l.startswith(">") for l in ez[198:232]),
      "ERGEBNIS_TB-162: Notiz Z. 199-232 (Z. 197 Kopf, Z. 233 leer, Z. 234 Abweichungen)")
    p(git("log", "--format=%h", "-1", "--", ERG).strip()[:7] == ERG_COMMIT, "ERGEBNIS_TB-162 zuletzt in Commit %s" % ERG_COMMIT)
    for b in ALT: p(neu_text(b, lies(opt(b))) is not None, "E-6 Anker in %s genau einmal (Datenuhr-Zeile, %s), horizontbeginn_ts noch nicht da" % (opt(b), DEF))
    ende()
def register(datum, s0, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    e = lies(ERG); notiz = e.split("\n")[198:232]; z = lies(REG).split("\n")
    p(md5(e) == ERG_MD5 and len(notiz) == 34, "Quelle ERGEBNIS_TB-162 md5 %s, 34 Zeilen" % ERG_MD5)
    p(not any(l.startswith("## 59. ") for l in z), "59 noch nicht im Register"); p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    kopf = ("Reines Eintragen einer Tatsachennotiz, Bauart 24.6 (Betreiberkarte 15.10.2026, 18:17: „Tatsachennotiz TB-162 ins Register, als Schritt im nächsten Mac-Auftrag“; Entscheid F2 des steuernden Chats vom 15.10.2026, 18:25). "
            "Quelle ist allein `%s`, md5 `%s`, %s B, Z. 199–232 (Abschnitt „Vorschlag Tatsachennotiz“), im Repo seit Commit `%s`; zeichengleich übernommen. "
            "Eingetragen am %s mit TB-163 (Stand `%s`). Nichts entfernt, kein bestehender Satz umgeschrieben; keine Marke (R96 (d) führt 24.x ohne Marke).") % (
            ERG, ERG_MD5, format(len(e.encode("utf-8")), ",").replace(",", " "), ERG_COMMIT, datum, s0)
    neu = ["", TITEL59, "", kopf, "", "### 59.1 Tatsachennotiz (zeichengleich aus ERGEBNIS_TB-162 Z. 199–232)", ""] + notiz + [""]
    if probe or any(l.startswith("NEIN") for l in OUT): ende()
    alt = lies(REG); schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG); p(r2.startswith(alt[:-1]) and r2.count("\n" + TITEL59 + "\n") == 1, "nachher: altes Register unverändert vorn (append-only), 59 genau einmal, Z. %d" % (r2.split("\n").index(TITEL59) + 1))
    p("\n".join(notiz) in r2, "Notiz zeichengleich im Register")
    ende()
def index(s0, datum, probe):
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 59. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 59 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–58" in z[k[0]], "Kopf genau einmal, nennt 0–58"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–58", "Abschnitte 0–59")
    i = [j for j, l in enumerate(z) if l.startswith("| 58 aus 14a und 14b |")]
    if p(len(i) == 1, "Zeile 58 genau einmal"): z.insert(i[0] + 1, "| 59 Tatsachennotiz TB-162 | %s | 59.1 Tatsachennotiz zu 24.2, 24.3, R36 und 11.2 mit R43 (Kapital-Drawdown E und M je WF-Abschnitt; aus ERGEBNIS_TB-162 Z. 199–232) | – |" % T)
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-162 (")]
    if p(len(j) == 1, "Pflegezeile TB-162 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-162 (", "In TB-162 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-163 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang B des Auftrags TB-163 (`index`); 59 (Tatsachennotiz TB-162) kommt zu T%s." % (datum, s0, rcm, T))
    if not probe and not any(l.startswith("NEIN") for l in OUT): schreibe(IDX, "\n".join(z))
    ende()
def e6(probe):
    neu = {}
    for b in ALT:
        f = opt(b); t = lies(f); p(sha(f) == VOR[f], "vorher %s sha256 %s…" % (f, VOR[f][:16]))
        n = neu_text(b, t); p(n is not None, "%s: Anker genau einmal" % f)
        if n is not None:
            neu[f] = n; h = hashlib.sha256(n.encode("utf-8")).hexdigest()
            p(NACH is None or NACH.get(f) == h, "nachher %s sha256 %s (Soll aus dem Bau)" % (f, h))
    if probe or any(l.startswith("NEIN") for l in OUT): ende()
    for f, n in neu.items(): schreibe(f, n)
    for f in neu: p(sha(f) == (NACH or {}).get(f, sha(f)), "geschrieben %s sha256 %s" % (f, sha(f)))
    ende()
def r81d(beleg):
    t = lies(beleg).rstrip("\n").split("\n")
    p(t[-1] == "rc 0" and re.fullmatch(r"(\d+) von \1 Pruefungen bestanden", t[-2] or "") is not None, "Testbeleg %s: alle bestanden, rc 0 (%s)" % (beleg, t[-2][:60] if len(t) > 1 else "?"))
    for b in ALT:
        s = lies(opt(b))
        p(not re.search(r'\["open_time"\]\.max\(\)\s*-\s*pd\.DateOffset', s), "%s: kein Fenster aus dem Dateiende (open_time.max() - DateOffset)" % b)
        p(len(re.findall(r'^\s+(entry_)?cutoff = horizontbeginn_ts\(df\["open_time"\]\)', s, re.M)) == 1 and ('faltenplan.horizontbeginn("%s")' % b) in s, "%s: Fenster aus faltenplan.horizontbeginn(\"%s\")" % (b, b))
    s = lies(opt("elliott_wave_stocks")); p('df = df[df["open_time"] >= cutoff].reset_index(drop=True)' in s, "elliott_wave_stocks: Anfang der geladenen Zeilen = Horizontbeginn (Kappung an cutoff)")
    p(sha(BB) == VOR[BB] and "start_i = max(start_i, int((df[\"open_time\"] < entry_cutoff).sum()))" in lies(BB), "volatility_breakout: Scanbeginn folgt entry_cutoff (backtest_breakout.py unverändert)")
    p(sha(FP) == VOR[FP], "faltenplan.py unverändert")
    n = sum(l.startswith("NEIN") for l in OUT)
    OUT.append("R81 (d) Voraussetzung: %s" % ("erfuellt (Fenster, Scanbeginn, Anfang der geladenen Zeilen ohne Dateiende)" if n == 0 else "NICHT erfuellt"))
    OUT.append("INFO Befund (kein Teil von R81 (d)): die Aufnahme eines Symbols (timespan_days = max - min gegen MIN_HISTORY_DAYS) haengt weiter vom Dateiende ab; buy_and_hold_benchmark.py der drei Bots rsi2, turtle, vb bildet cutoff weiter aus .max() (nicht E-6)")
    ende()
def uebergang(e):
    if not re.fullmatch(r"[0-9a-f]{7}", e): sys.exit(2)
    zl = ["**Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“) — Entwurf, nicht eingetragen; volle Hashes (39.5):", "",
          "| Datei | vorher | nachher | Commit | vollzieht |", "|---|---|---|---|---|"]
    for b in ALT: zl.append("| `%s` | `%s` | `%s` | `%s` | E-6 (Posten 4; R44, R81 (d)) |" % (opt(b), VOR[opt(b)], sha(opt(b)), e))
    zl += ["", "Neu (kein Vorher), Commit `%s`: `research/posten4_horizont/test_posten4_horizont.py` `%s`." % (e, sha("research/posten4_horizont/test_posten4_horizont.py")),
           "Unverändert: `%s` `%s`, `%s` `%s`." % (FP, sha(FP), BB, sha(BB))]
    print("\n".join(zl))
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n")
    a = [i for i, l in enumerate(z) if l.startswith("| **1** | **TB-30b Mass-Reparatur**")]
    if p(len(a) == 1 and z[a[0]].endswith("| zu formulieren |"), "BACKLOG Rang 1 genau einmal, Stand 'zu formulieren'"):
        z[a[0]] = z[a[0]][:-2] + " · Posten 4 (E-6, Horizont je Bot) erledigt mit TB-163 (%s, Journal %s) |" % (datum, kenn)
    s = "- **Vor der Neuerzeugung der Listen:** Posten 4, das Fenster je Bot aus dem Register (R81 (d); 55.8 Nr. 3)."
    b = [i for i, l in enumerate(z) if l.startswith(s)]
    if p(len(b) == 1, "BACKLOG-Zeile 'Vor der Neuerzeugung der Listen' genau einmal"):
        z[b[0]] = s + " ✅ Erledigt mit TB-163 (%s): Horizont aus `faltenplan.HORIZONTBEGINN` in den vier Aktien-Optimierern; R81 (d) gemessen (`docs/belege/TB-163/e_r81d.txt`)." % datum + z[b[0]][len(s):]
    if not probe and not any(l.startswith("NEIN") for l in OUT): schreibe(BL, "\n".join(z))
    ende()
def kennung():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); print("Kennung %s%s (letzte %s)" % (h[0], chr(ord(h[1]) + 1), h))
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k); neu = h[0] + chr(ord(h[1]) + 1)
    b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-163: " % neu), "Kopfzeile ## %s — TB-163: …" % neu); p(len(i) == 1, "Anker genau einmal")
    p(i and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "davor '---' und Leerzeile"); p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---")
    p("### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Teile 'Was gemessen ist', 'In einfacher Sprache'"); p(neu not in k, "Kennung %s frei" % neu)
    if not probe and not any(l.startswith("NEIN") for l in OUT): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 3 and a[0] == "register": register(a[1], a[2], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif a == ["e6"]: e6(pr)
    elif len(a) == 2 and a[0] == "r81d": r81d(a[1])
    elif len(a) == 2 and a[0] == "uebergang": uebergang(a[1])
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif a == ["kennung"]: kennung()
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
