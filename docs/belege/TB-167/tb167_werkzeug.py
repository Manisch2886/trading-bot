#!/usr/bin/env python3
"""TB-167 Werkzeug (Anhang A): Sicherung des Arbeitsbaums TB-166, Register 62 (R100-R103, Marken nach R100 (a) und R103 (c)), Index, Handfelder,
Reihenfolge in strategies/elliott_wave_stocks/multi_symbol_optimise.py (R102 (c)), Messungen R102 (c), Uebergang, BACKLOG, Journal.
Reine Standardbibliothek (plan: Repo-Module), Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts.
  sichere <ZIEL> | zurueck <ZIEL>          22 Dateien TB-166 nach <ZIEL> (ausserhalb) sichern, 20 auf 5167e96 zuruecksetzen, 2 Tests verschieben | Rueckweg
  md5                                      md5 der Fable-Dateien 15b und 16b
  voraussetzung                            Anker und Voraussetzungen vor dem Eintrag (rc 0 = alle ja)
  register <DATUM> <S0> <BELEG> [--probe]  Abschnitt 62 (R100-R103 zeichengleich), 62.5, Marken nach R100 (a) und R103 (c)
  index <S0> <DATUM> [--probe] | handfelder <ZIEL>
  code [--probe]                           Laengenpruefung vor den Zeilenschnitt (nur Reihenfolge, Schnitt bleibt)
  g6 <BELEG> rot|gruen                     Ausgabe von test_vorregistrierung.py lesen (Gegenprobe / Messung)
  plan rot|gruen                           Faltenplan elliott_wave_stocks ueber den echten Loader (entferne_unvollstaendige)
  uebergang <C> <DATUM>                    Entwurf Tatsachennotiz nach 37.3 (alter/neuer Hash) nach stdout
  backlog <DATUM> <KENNUNG> [--probe] | kennung | journal <BLOCK> [--probe]
Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch."""
import hashlib, json, os, re, shutil, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
P = "docs/projektfuehrung/"; BASIS = "5167e966763bd257feb2cfd96070f390f330bb62"
FA15, FA16 = P + "FABLE_ANTWORT_2026-10-15b_marken_tb150_etc_kein_ucits_korrelation_vor_pruefung.md", P + "FABLE_ANTWORT_2026-10-16b_g6_ews_schranke_vor_schnitt.md"
MD5 = {FA15: "c0f3e3ef60b22e6b750ad59c59ca7e03", FA16: "811fa8b7a9ff6403862385ce498593bc"}
EWS = "strategies/elliott_wave_stocks/multi_symbol_optimise.py"; EWS_ALT = "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232"
SOLL = {"sha_head": {"research/exposure_messung/bot_lauf.py": "203d96203aa8e86a32610bbae40fcca911554f56a98b971f5cc8c475c766f50a", "research/faltenplan_neun/faltenschranke_messung.py": "049bb657ff9d4f81e8fcfda94559d4e40668bcca7a76bc07488dce80510cf91b", "strategies/elliott_wave/elliott_wave_counter.py": "8209e503b2f979f8900f49d458ff538009c2da94bb86240cce710f3870fb66fe", "strategies/elliott_wave/equity_simulation.py": "f45e92cdac5a4f03d3bd2f10165034d27b20603846e3072d02a7baf807cd127b", "strategies/elliott_wave/multi_symbol_optimise.py": "ba3f5fdcf42537d586144174401c6dbf1e93a1f62476083fb3184028c3b2ce6c", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "ed97e0f1bfbcb8c1fe5676b64f5d8a4cbdaf8be8448062616edfe20bdda62cbf", "strategies/elliott_wave_stocks/equity_simulation.py": "80ea2a331538bbe6270a97c03627c3393c56848bfff00d9a9d44024fc0768a21", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232", "strategies/rsi2_crypto/backtest_rsi2.py": "84930445e34940775f6fcc6715616eb77589fc960f988a19b26199f1393e1aca", "strategies/rsi2_crypto/equity_simulation.py": "1406de58ad920116d15a08384b88b78d37ee4944c925ff36fddedd123963e9ab", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "836b032a5962c7766e7ed00a75b90ded4155b769fce54a84fead3c4cd5f3b7fc", "strategies/t3_supertrend/backtest_trend.py": "7a764353d092e521cc24b80ae97193d624224b38a6a62a45394360fe50cb04bb", "strategies/t3_supertrend/equity_simulation.py": "0aed45b7e8d1a0386c381fc462f96233723ff9036e863e70741e2c224fc6ef1b", "strategies/t3_supertrend/multi_symbol_optimise.py": "e314d7bf7bb35854c9280a5b51362f2c8a6c33771a06188a14afee7c8ff39f14", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "0704c9a96898ede99e9cf2b153da33d0cb885bf16c89e642d8514f277e8a0089", "strategies/turtle_soup_crypto/equity_simulation.py": "f0638e8e92ae98683385ea3082fbc8c56db4bc74631001c147eef54f70d7ea03", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "0de39bf20bbbd3c0988b270262728a08cddc79a448fd0300c2f6b94998df50bb", "strategies/volatility_breakout/backtest_breakout.py": "3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76", "strategies/volatility_breakout_crypto/backtest_breakout.py": "3c7ccbe792ea5eb8dcbc76ae27079f4d7c47ca34bd3ad5edd332d4fdad3c403e", "strategies/volatility_breakout_crypto/equity_simulation.py": "1109438768c00e10710740775a30de8f3ac9f4309e24b3c54b13266d07df9fad"}, "sha_jetzt": {"research/exposure_messung/bot_lauf.py": "95e4c567680b15889b1d80b6827dcbac6cdde8de639767eb7521546dc2876e71", "research/faltenplan_neun/faltenschranke_messung.py": "5383f4ed41a86b7bc0e3ba15c51adf96520bb1e54d58507f2503cab70301572f", "research/faltenplan_neun/test_handelbar_tag.py": "d90934f89a686c008bcb9e36ae8fac2ab76e9e2f564a51d19f659cd4acee23ce", "shared/test_schranke_signalpfad.py": "fc4581dc4486b34847d2c34ad5ef001af5c9136650db7ca0d42ba2fb74417c6f", "strategies/elliott_wave/elliott_wave_counter.py": "a57ab89413968aee9dbe5f256f44e0dde11131cb373b357de0da2d4c9a57a3a1", "strategies/elliott_wave/equity_simulation.py": "79d0a611bc8b4caed00db798e625f71e46b551af5e70a194323933d7b103ba00", "strategies/elliott_wave/multi_symbol_optimise.py": "d470a8b3d877dcd91b9e33ea40ba390e19200a4923140b54a532a561b5d9d209", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "6ce7966f07d3bb3348f0f6ab1d335a547707da088010c740a0427b5a312755e5", "strategies/elliott_wave_stocks/equity_simulation.py": "1ebde5ec7c067e73639c00495d481c09f130ebec23e51c3e90a3f79ea447dd5b", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "4f1ed9c0f2d149377be3568b016adec33d1f452eec43dd3aae63cbc102da1829", "strategies/rsi2_crypto/backtest_rsi2.py": "8de8a3fe35c31624d2a85495f9d73cf88a08d537fd0c22b3e889e55e09266691", "strategies/rsi2_crypto/equity_simulation.py": "30d3b2873883a6a2b2dc09e72d01bbd6b0db82551a745882481e1fec810c0b5a", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "484a964c0b80c0260d81e0a49195466f4f3d6aab1c0121a8abbd6cca840cc10b", "strategies/t3_supertrend/backtest_trend.py": "aade6aa8effc3fa9e095e8b57d6059ffb51d12091bbfa03dc937ab4f7c31797e", "strategies/t3_supertrend/equity_simulation.py": "2ffe378ff0b67efb63490f70a1bfae384044d096da40825788568e37db0c970a", "strategies/t3_supertrend/multi_symbol_optimise.py": "af458d97fd77d8057e292f500e8b9c7584d93bccc8d43274a0b541a6f35932cb", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "3f5faf8d3e00e9a92e6d61caa7684513343c99972693c497cf1cadf539e2ab3f", "strategies/turtle_soup_crypto/equity_simulation.py": "836f985229284f703a9a915434a60fa8b24579e63ddca9a303e8c3fd9c43237f", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "b7922129a00d2917d1d0750fb796f3e939e075c9f95cf5988b1849f8bb05b0f2", "strategies/volatility_breakout/backtest_breakout.py": "feb8875d484513b0289f563aee964387063b0cc413be612db43e2b3e8b0931fd", "strategies/volatility_breakout_crypto/backtest_breakout.py": "3743abd82984359328b125f9c3c221fe5d0e70ef5f2a2b066a6f40879df1b30c", "strategies/volatility_breakout_crypto/equity_simulation.py": "e16cf02297e2a6161307c4d398b3ac73db3db6fa249afa06185ead1b6e9bdc62"}, "unverfolgt": ["research/faltenplan_neun/test_handelbar_tag.py", "shared/test_schranke_signalpfad.py"]}
TITEL = "## 62. Fable 15b und 16b — Registerblöcke R100–R103 (TB-167)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
NR4 = "4. **2020 und 2022 sind Testfalten, keine Trainingsjahre.**"; NR4_ENDE = "   > Die Warnung oben gilt für beide Leser."
KOMMENTAR = "        # TB-167 (R102 (c)): Schranke 16.7 (b) an der Reihe, vor dem Zeilenschnitt am Horizontbeginn (28.6); Bauart rsi2_mean_reversion"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True).stdout
def sha_b(b): return hashlib.sha256(b).hexdigest()
def sha(f): return sha_b(open(f, "rb").read())
def md5(f): return hashlib.md5(open(f, "rb").read()).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT)
    print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
# --- Sicherung ---------------------------------------------------------------------------------
def sichere(ziel):
    ziel = os.path.abspath(os.path.expanduser(ziel)); wurzel = os.path.abspath(".")
    p(not (ziel + "/").startswith(wurzel + "/"), "Ziel ausserhalb des Repos: %s" % ziel)
    p(not os.path.exists(ziel), "Ziel existiert noch nicht")
    p(git("rev-parse", "HEAD").decode().strip() == BASIS, "HEAD = 5167e96")
    for f, s in SOLL["sha_jetzt"].items(): p(os.path.isfile(f) and sha(f) == s, "%s = TB-166-Stand %s…" % (f, s[:12]))
    if nein(): ende()
    zeilen = []
    for f in SOLL["sha_jetzt"]:
        os.makedirs(os.path.dirname(os.path.join(ziel, f)), exist_ok=True); shutil.copy2(f, os.path.join(ziel, f))
        zeilen.append("%s  %s" % (sha(os.path.join(ziel, f)), f))
    schreibe(os.path.join(ziel, "SHA256SUMS"), "\n".join(zeilen) + "\n")
    for f, s in SOLL["sha_jetzt"].items(): p(sha(os.path.join(ziel, f)) == s, "Kopie gegengelesen: %s" % f)
    if nein(): ende()
    for f, s in SOLL["sha_head"].items():
        b = git("show", "%s:%s" % (BASIS, f)); p(sha_b(b) == s, "Stand 5167e96 gelesen: %s" % f)
    if nein(): ende()
    for f in SOLL["sha_head"]: open(f, "wb").write(git("show", "%s:%s" % (BASIS, f)))
    for f in SOLL["unverfolgt"]: os.replace(f, os.path.join(ziel, "unverfolgt_" + f.replace("/", "__")))
    for f, s in SOLL["sha_head"].items(): p(sha(f) == s, "zurueckgesetzt auf 5167e96: %s" % f)
    for f in SOLL["unverfolgt"]: p(not os.path.exists(f), "verschoben (nicht mehr im Repo): %s" % f)
    ende()
def zurueck(ziel):
    ziel = os.path.abspath(os.path.expanduser(ziel))
    for f, s in SOLL["sha_head"].items(): p(sha(f) == s, "Repo-Datei auf Stand 5167e96: %s" % f)
    for f, s in SOLL["sha_jetzt"].items():
        q = os.path.join(ziel, f if f in SOLL["sha_head"] else "unverfolgt_" + f.replace("/", "__")); p(os.path.isfile(q) and sha(q) == s, "Sicherung da: %s" % f)
    if nein(): ende()
    for f in SOLL["sha_jetzt"]: shutil.copy2(os.path.join(ziel, f if f in SOLL["sha_head"] else "unverfolgt_" + f.replace("/", "__")), f)
    for f, s in SOLL["sha_jetzt"].items(): p(sha(f) == s, "zurueck: %s" % f)
    ende()
# --- Register ----------------------------------------------------------------------------------
def bloecke(f, nrn):
    """[(R-Zeile, Quellenzeile, Zeilennummer R)] aus dem einen Codeblock, der mit 'R<nrn[0]> — ' beginnt."""
    z = lies(f).split("\n"); f_ = [i for i, l in enumerate(z) if l == "```"]
    for a, e in zip(f_[0::2], f_[1::2]):
        b = [(i + 1, z[i]) for i in range(a + 1, e) if z[i]]
        if b and b[0][1].startswith("R%d — " % nrn[0]):
            soll = sum((["R%d — " % n, "Quelle des Grundes: "] for n in nrn), [])
            if [l[:len(s)] for (_, l), s in zip(b, soll)] != soll or len(b) != len(soll): return None
            return [(b[2 * k][1], b[2 * k + 1][1], b[2 * k][0]) for k in range(len(nrn))]
    return None
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    e = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")); return a[0], e
def einfuege(z, ort):
    """Einfuegestelle (Index) je Ort; None wenn nicht eindeutig."""
    if ort == "5.1 Nr. 4":
        a, e = unterabschnitt(z, "### 5.1 "); i = [k for k in range(a, e) if z[k] == NR4_ENDE] if a is not None else []
        return i[0] + 1 if len(i) == 1 and sum(l.startswith(NR4) for l in z) == 1 else None
    a, e = unterabschnitt(z, "### %s " % ort.split(" ")[0])
    if a is None: return None
    zg = [i for i in range(a, e) if z[i] == ZG]
    if zg: return zg[-1] + 1
    q = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    if len(q) == 1: return q[0] + 1
    k = e - 1
    while z[k] == "": k -= 1
    return k + 1
M103 = [("5.1 Nr. 4", "5.1 Nr. 4 ERGÄNZT durch R103 (62.4)", "Fable 16b R103, Unterpunkt (a); die Zeile „4. …“ oben bleibt zeichengleich"),
        ("55.4", "55.4 R81 PRÄZISIERT durch R102 (62.3)", "Fable 16b R102, Unterpunkte (a) und (c)"),
        ("60.1", "60.1 ERGÄNZT durch R102 (62.3) und R103 (62.4)", "Fable 16b R103 (c): R102 Unterpunkte (b) und (c), R103 Unterpunkt (b)")]
def m100():
    """Die drei Marken aus R100 (a), Kopf zeichengleich aus dem Wortlaut von R100 (a) (Satz ab „55.2 (R79) — “ usw.)."""
    b = bloecke(FA15, (100, 101))
    if not b: return None
    t = b[0][0]; k = [t.find(x) for x in ("55.2 (R79) — ", "55.1 (R78) — ", "53.7 (R72) — ", " [Voraussetzung, zu messen: dass der Wortlaut von R72 (c)")]
    if min(k) < 0 or k != sorted(k) or any(t.count(x) != 1 for x in ("55.2 (R79) — ", "55.1 (R78) — ", "53.7 (R72) — ")): return None
    seg = [t[k[i]:k[i + 1]].strip() for i in range(3)]
    return [(o, x[:-1] if x.endswith(".") else x, "Fable 15b R100 (a)") for o, x in zip(("55.2", "55.1", "53.7"), seg)]
def r72c(z):
    """Wortlaut von R72 Unterpunkt (c) allein; (Text, nennt Go-Live-Schnitt)."""
    a, e = unterabschnitt(z, "### 53.7 ")
    l = [x for x in z[a:e] if x.startswith("> R72 — ")] if a is not None else []
    if len(l) != 1: return None, None
    m = re.search(r"[.\]] (\(c\) .*?)(?: \(d\) |$)", l[0])
    if not m: return None, None
    return m.group(1), ("Go-Live-Schnitt" in m.group(1) or "Go-Live" in m.group(1))
def marken(z):
    t, nennt = r72c(z); m = m100() or []
    return M103 + [x for x in m if x[0] != "53.7" or nennt is False], t, nennt
def markenzeilen(m, datum):
    o, kopf, zus = m; e = "   " if o == "5.1 Nr. 4" else ""
    return ["", e + "> ⭐ **%s** (%s, TB-167, %s)." % (kopf, zus, datum), e + ZG]
def r100c():
    """R100 (c): Fundstellen (Messpunkte TB-148 M1..M5 und Pfade) aus R90 (e), R91 (a)-(c), R92 (a) gegen die in d9f8489 geaenderten Zeilen von docs/belege/TB-148/leseprotokoll.md."""
    z = lies(REG).split("\n"); fund = set()
    for nr, ks in (("R90", "e"), ("R91", "abc"), ("R92", "a")):
        l = [x for x in z if x.startswith("> %s — " % nr)]
        if len(l) != 1: return None
        for t in re.split(r"(?<=[.\]]) (?=\([a-h]\) )", l[0]):
            if t[:3] in ["(%s)" % k for k in ks]: fund |= set(re.findall(r"(?:research|shared|strategies)/[\w/]+\.py", t)) | set("TB-148 " + x for x in re.findall(r"TB-148, (M\d)", t))
    d = git("show", "d9f8489", "--", "docs/belege/TB-148/leseprotokoll.md").decode("utf-8", "replace").split("\n")
    def zeilen(v):
        r = {}
        for x in d:
            if x.startswith(v + "|"): c = [y.strip() for y in x[1:].strip().strip("|").split("|")]; r.setdefault(c[0], c)
        return r
    alt, neu = zeilen("-"), zeilen("+"); kopf = alt.get("Datei", [])
    # geaendert = eine Zelle einer Spalte, die es vorher schon gab (neue Spalten sind neue Zellen, keine geaenderten)
    geaendert = {k: [(kopf[i], alt[k][i], neu[k][i]) for i in range(1, len(kopf)) if i < len(alt[k]) and i < len(neu[k]) and alt[k][i] != neu[k][i]] for k in set(alt) & set(neu) if k not in ("Datei", "---")}
    geaendert = {k: v for k, v in geaendert.items() if v}
    treffer = []
    for f_ in sorted(fund):
        if f_.startswith("TB-148 "):
            mx = f_.split(" ")[1]; treffer += ["%s: %s %s→%s" % (k, sp, x, y) for k, v in sorted(geaendert.items()) for sp, x, y in v if sp == "Messpunkt" and (re.search(r"\b%s\b" % mx, x) is None) != (re.search(r"\b%s\b" % mx, y) is None)]
        else: treffer += ["%s: %s %s→%s" % (f_, sp, x, y) for sp, x, y in geaendert.get("`%s`" % f_, [])]
    return sorted(fund), sum(len(v) for v in geaendert.values()), sorted(set(treffer))
def r101a():
    t = lies("docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md").split("\n")
    def ab(n):
        a = [i for i, l in enumerate(t) if l.startswith("## %s. " % n)]
        if len(a) != 1: return ""
        e = next((i for i in range(a[0] + 1, len(t)) if t[i].startswith("## ")), len(t)); return "\n".join(t[a[0]:e])
    g = lambda x: ("GLD" in x or "Gold" in x, "SLV" in x or "Silber" in x)
    return g(ab(9)), g(ab(2)), (t[[i for i, l in enumerate(t) if l.startswith("## 9. ")][0]] if any(l.startswith("## 9. ") for l in t) else "?")
def voraussetzung():
    for f, m in MD5.items():
        p(bool(git("ls-files", "--error-unmatch", f).strip()) and git("diff", "--name-only", "HEAD", "--", f).strip() == b"" and md5(f) == m, "R100 (e)/R56 (b): %s verfolgt, gleich HEAD, md5 %s" % (f, m))
    b1, b2 = bloecke(FA15, (100, 101)), bloecke(FA16, (102, 103))
    p(b1 is not None and b2 is not None, "Codebloecke: R100, Quelle, R101, Quelle (15b Z. %s); R102, Quelle, R103, Quelle (16b Z. %s)" % (b1 and b1[0][2], b2 and b2[0][2]))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 61. ") for l in z) == 1 and not re.search(r"^## 62\. ", reg, re.M) and not re.search(r"\bR10[0-3]\b", reg), "Register: 61 da, 62 nicht; R100–R103 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    p(sum(l.startswith(NR4) for l in z) == 1, "Zeile 5.1 Nr. 4 (G6-Anker) genau einmal")
    p(m100() is not None, "R100 (a): drei Marken-Saetze 55.2 (R79), 55.1 (R78), 53.7 (R72) je genau einmal im Wortlaut")
    t72, nennt = r72c(z); p(t72 is not None, "R100 (a) Voraussetzung: R72 Unterpunkt (c) allein gelesen; nennt den Go-Live-Schnitt: %s ⇒ Marke 53.7 %s" % ("ja" if nennt else "nein", "entfaellt (gemeldet)" if nennt else "wird gesetzt"))
    OUT.append("info  R72 (c) Wortlaut: %s" % (t72 or "?"))
    ms, _, _ = marken(z)
    for m in ms:
        i = einfuege(z, m[0]); p(i is not None and not any(l.lstrip().startswith("> ⭐ **%s**" % m[1]) for l in z), "Ort %s: Einfuegestelle Z. %s, Marke noch nicht da" % (m[0], i + 1 if i is not None else "?"))
    rc = r100c(); p(rc is not None, "R100 (c) gemessen: Fundstellen %s; geaenderte Zellen (bestehende Spalten) in d9f8489 (leseprotokoll.md): %s; Fundstellen in geaenderten Zellen: %s" % (rc and rc[0], rc and rc[1], rc and (rc[2] or "keine")))
    if rc and rc[2]: OUT.append("info  R100 (c) BEFUND, zu melden (kein Abbruch): %s" % rc[2])
    s9, s2, h9 = r101a(); OUT.append("info  R101 (a) Voraussetzung (Messung, kein Urteil): S-B1 Abschnitt 9 („%s“) fuehrt Gold/Silber: %s/%s; Abschnitt 2 (Die Kandidatenliste) fuehrt Gold/Silber: %s/%s; ob ein UCITS-Fonds auf ein einzelnes Edelmetall besteht: im Repo nicht messbar, offen" % (h9[:60], *s9, *s2))
    OUT.append("info  R101: nennt keine Marke (Wortlaut ohne ERGÄNZT/PRÄZISIERT an einem Ort)")
    p(sha(EWS) == EWS_ALT and git("diff", "--name-only", "HEAD", "--", EWS).strip() == b"", "%s = 60.1 nachher %s…, gleich HEAD" % (EWS, EWS_ALT[:12]))
    ende()
QZ = (92, 99)
def quellzeilen():
    z = git("show", "11a267f~1:" + EWS).decode("utf-8").split("\n")[QZ[0] - 1:QZ[1]]
    return ["Z. %d: %s" % (QZ[0] + i, l) for i, l in enumerate(z)]
def titel(zeile):
    t = zeile.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith("NEIN: 0"), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    bl = (bloecke(FA15, (100, 101)) or []) + (bloecke(FA16, (102, 103)) or [])
    p(len(bl) == 4 and all(md5(f) == m for f, m in MD5.items()), "Quellen md5 wie Soll, vier Bloecke")
    p(not any(l.startswith("## 62. ") for l in z) and z[-1] == "" and z[-2] != "", "62 noch nicht im Register; endet mit einer Leerzeile")
    ms, t72, nennt = marken(z); einf = [(einfuege(z, m[0]), m) for m in ms]; p(all(i is not None for i, _ in einf) and len(ms) in (5, 6), "%d Einfuegestellen eindeutig" % len(ms))
    if nein(): ende()
    gr = lambda f: format(os.path.getsize(f), ",").replace(",", " ")
    kopf = ("Reines Eintragen von Registertext, Bauart wie 61. Quellen sind allein `%s`, md5 `%s`, %s B, Codeblock ab Z. %d, im Repo seit Commit `83591b2`, und `%s`, md5 `%s`, %s B, "
            "Codeblock ab Z. %d, im Repo seit Commit `%s`. Nicht eingetragen werden Leseprotokoll, Teile und „Unsicher“ der Antworten. Zum Dialog gehören die Anfragen 15.10.b (seit `83591b2`) "
            "und 16.10.b (seit `%s`). Marken nach R100 (a) und R103 (c). Eingetragen am %s mit TB-167.") % (
            FA15, MD5[FA15], gr(FA15), bl[0][2], FA16, MD5[FA16], gr(FA16), bl[2][2], s0, s0, datum)
    kette = ["**Kette:** Marken nach R100 (a): 55.2 (R79); 55.1 (R78); 53.7 (R72) %s. Ohne Marke: 48.7 (R39). Voraussetzungen: (a) und (c) 62.5 (c), (e) 62.5 (Messung oben)." % ("entfällt, R72 (c) nennt den Go-Live-Schnitt (R89 (c))" if nennt else "(Voraussetzung gemessen: R72 (c) nennt den Go-Live-Schnitt nicht)"),
             "**Kette:** Ohne Marke (R101 nennt keine); Lesung zu S-B1 Registertext 3 (10a.2), die Vorregistrierung S-B1 bleibt unberührt. Voraussetzung (a): 62.5 (d).",
             "**Kette:** Marken nach R103 (c): 55.4 (R81), Unterpunkte (a) und (c); 60.1, Unterpunkte (b) und (c). Voraussetzung (c): Schritt M von TB-167 (62.5 (a)); (d) offen (62.5 (b)).",
             "**Kette:** Marken nach R103 (c): 5.1 Nr. 4, Unterpunkt (a) (unter den zwei Kästen, Z. 613 zeichengleich); 60.1, Unterpunkt (b)."]
    neu = ["", TITEL, "", kopf, ""]
    for k, (zeile, quelle, _) in enumerate(bl): neu += ["### 62.%d %s" % (k + 1, titel(zeile)), "", "> " + zeile, "> " + quelle, "", kette[k], ""]
    neu += ["### 62.5 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-167), Zeilen wörtlich:" % beleg, ""]
    neu += ["    " + l for l in vb] + ["",
            "(a) R102 (c): gemessen nach diesem Eintrag in Schritt M von TB-167, vor dem Commit der Abhilfe (Belege `docs/belege/TB-167/m1_*` bis `m6_*`); Vollzug und Hash-Übergang nach 37.3 kommen als Tatsachennotiz mit einem Folgeauftrag (Bauart 60). Bis dahin offen.",
            "", "(b) R102 (d): offen; vor der Neuerzeugung der Listen (R44) zu messen, nur das Ob. Nicht Teil von TB-167.",
            "", "(c) R100 (a): R72 Unterpunkt (c) allein gelesen (Zeile „info“ oben); er nennt den Go-Live-Schnitt %s, die Marke an 53.7 ist %s. R100 (c): Fundstellen und geänderte Zeilen wie oben gemessen; %s. R100 (e): gemessen oben." % ("" if nennt else "nicht", "entfallen (gemeldet)" if nennt else "gesetzt", ("Befund, zu melden: " + "; ".join((r100c() or [0, 0, ["?"]])[2])) if (r100c() or [0, 0, 1])[2] else "keine Fundstelle in einer geänderten Zelle"),
            "", "(d) R101 (a): gemessen wie in der Zeile „info“ oben (Abschnitt 9 der S-B1-Vorregistrierung ist die Sperrliste; Gold und Silber führt Abschnitt 2, Die Kandidatenliste); ob ein UCITS-Fonds auf ein einzelnes Edelmetall besteht, ist im Repo nicht messbar und bleibt offen.",
            "", "(e) Tatsachennotiz zu R102 (b), R102 bleibt zeichengleich: Auf `11a267f~1` stand in `strategies/elliott_wave_stocks/multi_symbol_optimise.py` die Längenprüfung schon hinter dem Schnitt `RECENT_YEARS_ONLY` (Dateiende − 10 Jahre); E-6 (`11a267f`) hat nur die Schnittzeile auf den Horizontbeginn umgestellt und die Reihenfolge damit wirksam gemacht. Quellenzeilen (`git show 11a267f~1:strategies/elliott_wave_stocks/multi_symbol_optimise.py`, Z. %d–%d):" % QZ, ""] + ["    " + l for l in quellzeilen()] + [""]
    if probe: ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m, datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.lstrip().startswith("> ⭐ **%s**" % m[1])] for m in ms}
    json.dump({"marken": [[m[0], m[1], m[2], (mz[m[0]] or [0])[0]] for m in ms], "abschnitt_62": r2.index(TITEL) + 1, "r72c_nennt_schnitt": nennt}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: %d Marken Z. %s; Abschnitt 62 Z. %d" % (len(ms), sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(r2[QZ[0] - 1 + 0:QZ[0]] is not None and "if RECENT_YEARS_ONLY is not None:" in quellzeilen()[0] and "timespan_days" in quellzeilen()[4], "Quellenzeilen 11a267f~1: Schnitt Z. 92–94, Pruefung Z. 96–99")
    p(all(r2.count("> " + b[0]) == 1 and r2.count("> " + b[1]) == 1 for b in bl), "R100–R103 mit Quellenzeile je genau einmal zeichengleich")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al)] == "" and r3[len(al) + 1] == TITEL, "append-only bis auf die Marken (je Leerzeile, Marke, Zeichengleich-Zeile)")
    p(sum(l.startswith(NR4) for l in r2) == 1, "G6-Anker 5.1 Nr. 4 weiter genau einmal")
    ende()
def index(s0, datum, probe):
    d = json.load(open("docs/belege/TB-167/r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 62. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) in (5, 6) and all(m[3] for m in mk), "Abschnitt 62 in genau einer Teildatei: T%s; %d Marken mit Zeile" % (teil, len(mk))); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").decode().strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–61" in z[k[0]], "Kopf genau einmal, nennt 0–61"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–61", "Abschnitte 0–62")
    i = [j for j, l in enumerate(z) if l.startswith("| 61 aus 15a |")]
    if p(len(i) == 1, "Zeile 61 genau einmal"): z.insert(i[0] + 1, "| 62 aus 15b und 16b | %s | R100–R103 (62.1–62.4); 62.5 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 15. Die Marken aus Fable 15b und 16b (TB-167)", "", "Alle %d Marken, die TB-167 nach R100 (a) und R103 (c) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-167/r_daten.json`." % len(mk), "",
           "| Ort | Marke | Kopf | nach | T |", "|---|---|---|---|---|"] + ["| %s | Z. %d | %s | %s | %s |" % (o, n, k.replace("|", "\\|"), zz, T) for o, k, zz, n in sorted(mk, key=lambda m: m[3])] + [""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 15. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 15"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-165 (")]
    if p(len(j) == 1, "Pflegezeile TB-165 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-165 (", "In TB-165 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-167 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-167 (`index`); 62 (R100–R103) kommt zu T%s; neuer Abschnitt 15 (%d Marken)." % (datum, s0, rcm, T, len(mk)))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    h = {}
    for k, an, aw, off in (("15b", "FABLE_ANFRAGE_2026-10-15b_f4_wortlaut_sb1_paare_10a.md", FA15, "ja"), ("16b", "FABLE_ANFRAGE_2026-10-16b_g6_ews_testfalte_2020.md", FA16, "ja")):
        f = lies(P + an).split("\n")[0].split(" — ", 1)[1].strip(); e = lies(aw).split("\n")[0].split(" — ", 1)[1].strip()
        h[k] = {"frage": f, "entscheidung": e, "offen": off}
    h["16a"] = {"frage": lies(P + "FABLE_ANFRAGE_2026-10-16a_mehrmodell_grok_pruefung.md").split("\n")[0].split(" — ", 1)[1].strip(), "entscheidung": "–", "offen": "–"}
    json.dump(h, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("Handfelder 15b, 16b (aus den Kopfzeilen), 16a (–) geschrieben: %s" % ziel)
# --- Code und Messungen ------------------------------------------------------------------------
def code(probe):
    t = lies(EWS); z = t.split("\n"); p(sha(EWS) == EWS_ALT, "vorher %s (60.1 nachher)" % EWS_ALT)
    i = [k for k, l in enumerate(z) if l == "        if RECENT_YEARS_ONLY is not None:"]
    ok = len(i) == 1
    if ok:
        i = i[0]; w = z[i:i + 9]
        ok = (w[1].startswith("            cutoff = horizontbeginn_ts(df[\"open_time\"])") and w[2] == "            df = df[df[\"open_time\"] >= cutoff].reset_index(drop=True)" and w[3] == ""
              and w[4] == "        timespan_days = (df[\"open_time\"].max() - df[\"open_time\"].min()).days" and w[5] == "        if timespan_days < MIN_HISTORY_DAYS:"
              and w[6] == "            _prot.zu_kurz(symbol, timespan_days, MIN_HISTORY_DAYS)" and w[7] == "            continue" and w[8] == "")
    p(ok, "Block Z. %s: Schnitt (3 Zeilen), Leerzeile, Laengenpruefung (4 Zeilen), Leerzeile - genau einmal" % (i + 1 if ok else "?"))
    if nein(): ende()
    neu = z[:i] + [KOMMENTAR] + z[i + 4:i + 8] + [""] + z[i:i + 3] + [""] + z[i + 9:]
    p(neu[i + 6:i + 9] == z[i:i + 3] and neu[i + 1:i + 5] == z[i + 4:i + 8] and len(neu) == len(z) + 1, "nur Reihenfolge und eine Kommentarzeile; Schnitt zeichengleich")
    n = "\n".join(neu); OUT.append("info  %s  vorher %s  nachher %s" % (EWS, EWS_ALT, sha_b(n.encode("utf-8"))))
    if not probe and not nein(): schreibe(EWS, n)
    ende()
def g6(beleg, soll):
    z = lies(beleg).rstrip("\n").split("\n"); rc = z[-1]; fail = [l for l in z if l.startswith("  - ")]
    g = [l for l in fail if l.startswith("  - G6: elliott_wave_stocks")]
    if soll == "rot": p(rc == "rc 1" and len(fail) == 1 and len(g) == 1, "Gegenprobe: rc 1, genau ein Fehler, G6 elliott_wave_stocks (%s; %s)" % (rc, g[0][:160] if g else fail[:1]))
    else: p(rc == "rc 0" and not fail, "Messung: rc 0, kein Fehler (%s)" % rc)
    ende()
def plan(soll):
    vor = git("status", "--porcelain"); sys.path.insert(0, "research/vorregistrierung"); import faltenplan as fp  # noqa: E402
    mess = fp.rd._mess(); pl = fp.plan_aktien("elliott_wave_stocks", mess)
    sel = [f["name"] for f in pl["falten"] if f["rolle"] == "selektion"]
    OUT.append("info  status %s; falten %s" % (pl.get("status"), [(f["name"], f["rolle"]) for f in pl["falten"]]))
    try: OUT.append("info  erste_falte_4a_messung %s" % str(fp.erste_falte_4a_messung("elliott_wave_stocks"))[:600])
    except Exception as x: OUT.append("info  erste_falte_4a_messung nicht lesbar: %s" % x)
    p(git("status", "--porcelain") == vor, "rd._mess()/plan_aktien schreiben nichts ins Repo (porcelain vorher = nachher)")
    ziel = [str(j) for j in range(2017, 2026)]
    if soll == "gruen": p(sel == ziel, "Selektionsfalten 2017–2025 (R102 (c)): %s" % sel)
    else: p(sel[:1] != ["2017"], "Gegenprobe: Selektionsfalten beginnen nicht 2017: %s" % sel)
    ende()
def uebergang(c, datum):
    neu = sha(EWS); print("| Datei | vorher | nachher | Commit | vollzieht |\n|---|---|---|---|---|\n| `%s` | `%s` | `%s` | `%s` | R102 (c) (Posten 4; R44, R81 (d); E-6 berichtigt) |" % (EWS, EWS_ALT, neu, c))
    print("\nEntwurf, nicht eingetragen (TB-167, %s). Freigabe: Karte im Auftrag TB-167. Sonde Punkt 11: nicht gemessen (Abbild führt keinen Optimierer, 60.1)." % datum)
# --- BACKLOG, Journal --------------------------------------------------------------------------
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("| **1** | **TB-30b Mass-Reparatur**")]
    if p(len(a) == 1 and z[a[0]].endswith(" |"), "BACKLOG Rang 1 genau einmal"):
        z[a[0]] = z[a[0]][:-2] + " · Register 62 (R100–R103) und Abhilfe G6 elliott_wave_stocks (R102 (c), Schranke vor dem Schnitt) mit TB-167 (%s, Journal %s); als Nächstes Vollzug nach 37.3 (Bauart 60) und TB-166 E-3a neu auf diesem Stand |" % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); k = kennungen(); neu = naechste(max(k))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-167: " % neu), "Kopfzeile ## %s — TB-167: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if len(a) == 2 and a[0] in ("sichere", "zurueck"): (sichere if a[0] == "sichere" else zurueck)(a[1])
    elif a == ["md5"]:
        for f, m in MD5.items(): p(os.path.exists(f) and md5(f) == m, "md5 %s = %s" % (f, m))
        ende()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["code"]: code(pr)
    elif len(a) == 3 and a[0] == "g6" and a[2] in ("rot", "gruen"): g6(a[1], a[2])
    elif len(a) == 2 and a[0] == "plan" and a[1] in ("rot", "gruen"): plan(a[1])
    elif len(a) == 3 and a[0] == "uebergang": uebergang(a[1], a[2])
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
