#!/usr/bin/env python3
"""TB-180 Werkzeug (Anhang A des Auftrags TB-180). Aufruf aus der Repo-Wurzel mit PY:
  voraussetzung | kurven <etikett> | vergleich <a> <b> | code [--probe] | code_pruefen | nachtrag <DATUM> <C> [--probe]
  register <DATUM> <S0> <C> <ABBILD> [--probe] | index <S0> <DATUM> | handfelder <ZIEL> | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]
Schreibt nur: kurven -> $TMPDIR; code -> die zwoelf Dateien aus UMBAU; nachtrag/register -> das Register; index -> REGISTER_INDEX.md;
handfelder -> ZIEL; backlog/journal -> BACKLOG.md/JOURNAL.md (Bauart TB-178)."""
import ast, hashlib, json, os, re, subprocess, sys
AUFTRAG = "docs/auftraege/MAC_TB-180_startkapital_am_ort_punkt9_abbild_probe.md"; REG = "docs/VORREGISTRIERUNG_neuselektion.md"; BEL = "docs/belege/TB-180/"; PJ = "docs/projektfuehrung/"
IDX, JO, BL = PJ + "REGISTER_INDEX.md", PJ + "JOURNAL.md", PJ + "BACKLOG.md"; RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
CODE = {
"shared/handelskosten.py": "a1baa909d0e56035077e42775dc3807a",
"shared/test_ergebniskurven.py": "326ce323f4648609fade8144f7ac7650",
"research/tb27_kapitalsimulation/vergleich.py": "3a3c3d01497d00bba0bd2253ff2e87ac",
"strategies/elliott_wave/equity_simulation.py": "a058c69a7a6c25e7239381bfab96fb05",
"strategies/elliott_wave_stocks/equity_simulation.py": "4ff525c50514fc25f43f50437148a7bd",
"strategies/rsi2_crypto/equity_simulation.py": "1dc8f5f5e57a1260446de77581a90f57",
"strategies/rsi2_mean_reversion/equity_simulation.py": "774e7fecad93bdad38bcba5e568b7243",
"strategies/t3_supertrend/equity_simulation.py": "be665a734328d8a1d8231ff211a55a85",
"strategies/turtle_soup_crypto/equity_simulation.py": "0680a092cf49a651771617b21ceea7fa",
"strategies/turtle_soup_stocks/equity_simulation.py": "f45e55aadcb9d03b4342ec32e8644914",
"strategies/volatility_breakout/equity_simulation.py": "dd5fa96bb927aecb26051fbaefb4a0cd",
"strategies/volatility_breakout_crypto/equity_simulation.py": "f5168c0f865af159a8859ae7d3f44978",
"research/tb27_kapitalsimulation/test_vergleich.py": "e01c1b1f747e26251f4492a3ee109b6d",
"shared/kurven_lauf.py": "e7fdff7dd9ec07935c30b50f186ac02f",
"shared/ergebniskurven.py": "2b2c30457eb363c418f03d9fb50e0fef",
"shared/sperrlistensonde.py": "a8a47c882f32df565f4d3fa29c4d7fc6",
"research/vorregistrierung/sperrliste_abbild.py": "0dd8c6e00bf94886abbb98c17f90bd60"
}
NACH = {
"shared/handelskosten.py": "af7023efc2c2125528ec96d083271832",
"strategies/elliott_wave/equity_simulation.py": "6afca6962d34eb77ba1a52987d868e40",
"strategies/elliott_wave_stocks/equity_simulation.py": "30b869d449fb5bd45cad35c38db44f20",
"strategies/rsi2_crypto/equity_simulation.py": "b238ba4c97794f1477a8f450344c4924",
"strategies/rsi2_mean_reversion/equity_simulation.py": "cd8300caf45e84270a2aac132bc1e566",
"strategies/t3_supertrend/equity_simulation.py": "93167e43f228421d87ef2eb58ce2c4e1",
"strategies/turtle_soup_crypto/equity_simulation.py": "c470c8364d3da1e5fddc112cc42a1c06",
"strategies/turtle_soup_stocks/equity_simulation.py": "3494f4536a4fce189a111889ebeafcef",
"strategies/volatility_breakout/equity_simulation.py": "0094cbe01f99da98b9ff86169cfe3dc8",
"strategies/volatility_breakout_crypto/equity_simulation.py": "d7db54736e99079a750a0366f68a3495",
"shared/test_ergebniskurven.py": "d05674ddafa6e3e95228cf2796692bc1",
"research/tb27_kapitalsimulation/vergleich.py": "9a4589524ec8439813f4eb5f4712c08b"
}
SHA_HK = "b2efabe4a51b26d6b9f34b1b8b9d0f5bc45b463aabd6b9bbd95237f560273a5e"
FUND = {"elliott_wave": 66, "elliott_wave_stocks": 71, "rsi2_crypto": 51, "rsi2_mean_reversion": 62, "t3_supertrend": 54, "turtle_soup_crypto": 45, "turtle_soup_stocks": 68, "volatility_breakout": 61, "volatility_breakout_crypto": 61}
SATZ = "Das registrierte Startkapital ist 10 000, wie der Code es am Commit der Tatsachennotiz in den neun strategies/<bot>/equity_simulation.py trägt; sein Ort ist die Konstante STARTING_CAPITAL in shared/handelskosten.py (38.5), sobald dieses Modul nach 38.5 als Nachtrag zu Punkt 9 mit Pfad und Hash auf der Sperrliste steht; die Sonde prüft Datei und Wert (37.5 (1))."
# TB-180 Umbau (Schritt C), rein textuell: dieselbe Funktion rechnet am Bau das Soll (md5 nachher) und schreibt am Mac.
BOTS = ["elliott_wave", "elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion", "t3_supertrend", "turtle_soup_crypto",
        "turtle_soup_stocks", "volatility_breakout", "volatility_breakout_crypto"]
HK, TEK = "shared/handelskosten.py", "shared/test_ergebniskurven.py"
ES = {b: "strategies/%s/equity_simulation.py" % b for b in BOTS}
ALT, NEU = "\nSTARTING_CAPITAL = 10_000.0\n", "\nfrom handelskosten import STARTING_CAPITAL\n"
HK_DOC = ("\nDazu das registrierte Startkapital je Bot (Ergaenzung zu 29.3 nach R109 (a) in\n"
          "der Fassung R110 (b), TB-180):\n\n"
          "    STARTING_CAPITAL    10 000   Startkapital des Kapitalpfads, gleich fuer alle neun\n\n"
          "Die neun `strategies/*/equity_simulation.py` importieren es von hier und tragen\n"
          "keine eigene Kopie (Bauart 38.5); bis TB-180 stand es dort neunmal als Zuweisung.\n")
HK_KONST = "STARTING_CAPITAL = 10_000.0    # Startkapital je Bot (29.3, R110 (b))\n"
TEK_ERS = [
    ("    `shared/`, `data/` und `config/` werden verknuepft (nur gelesen),\n    `strategies/<bot>/` wird KOPIERT - nur dort wird mutiert. `results/`\n",
     "    `data/`, `config/`, `research/` und `notifications/` werden verknuepft\n    (nur gelesen), `shared/` Datei\n    fuer Datei - nur `handelskosten.py`, der Ort des Startkapitals (29.3,\n"
     "    R110 (c)), wird KOPIERT. `strategies/<bot>/` wird KOPIERT - nur dort\n    und am Ort wird mutiert. `results/`\n", 1),
    ("def probe_umgebung(bot=BOT):\n", "def probe_umgebung(bot=BOT, bots=None):\n", 1),
    ('    for name in ("shared", "data", "config"):\n        os.symlink(os.path.join(BASE_DIR, name), os.path.join(ordner, name))\n'
     '    os.makedirs(os.path.join(ordner, "strategies"))\n    shutil.copytree(os.path.join(BASE_DIR, "strategies", bot),\n'
     '                    os.path.join(ordner, "strategies", bot))\n    os.makedirs(os.path.join(ordner, "results", bot))\n',
     '    # `research/` und `notifications/` braucht die Kurve von fuenf Bots (Importe\n'
     '    # im __main__-Pfad); nur gelesen, wie `data/` und `config/`.\n'
     '    for name in ("data", "config", "research", "notifications"):\n        os.symlink(os.path.join(BASE_DIR, name), os.path.join(ordner, name))\n'
     '    # Eine Verknuepfung von `shared/` liesse die Mutation am Ort (R110 (c))\n    # bis ins Repo durchschlagen - deshalb Datei fuer Datei, der Ort als Kopie.\n'
     '    os.makedirs(os.path.join(ordner, "shared"))\n    for name in os.listdir(_SHARED):\n        if name == "__pycache__":\n            continue\n'
     '        quelle, ziel = os.path.join(_SHARED, name), os.path.join(ordner, "shared", name)\n'
     '        if name == ORT:\n            shutil.copy2(quelle, ziel)\n        else:\n            os.symlink(quelle, ziel)\n'
     '    os.makedirs(os.path.join(ordner, "strategies"))\n    for b in (bots or [bot]):\n'
     '        shutil.copytree(os.path.join(BASE_DIR, "strategies", b),\n                        os.path.join(ordner, "strategies", b))\n'
     '        os.makedirs(os.path.join(ordner, "results", b))\n', 1),
    ('BOT = "volatility_breakout_crypto"\n',
     'BOT = "volatility_breakout_crypto"\n\n# Der Ort des Startkapitals (29.3 nach R110 (b), TB-180): eine Konstante in\n'
     '# `shared/handelskosten.py`; die neun `equity_simulation.py` importieren sie.\nORT = "handelskosten.py"\n'
     'ALLE_NEUN = ("elliott_wave", "elliott_wave_stocks", "rsi2_crypto", "rsi2_mean_reversion",\n'
     '             "t3_supertrend", "turtle_soup_crypto", "turtle_soup_stocks",\n             "volatility_breakout", "volatility_breakout_crypto")\n', 1),
    ("        f.write(text.replace(alt, neu))\n    return anzahl\n",
     "        f.write(text.replace(alt, neu))\n    return anzahl\n\n\n"
     "def mutiere_ort(ordner, alt, neu):\n"
     '    """Aendert das Startkapital AM ORT (`shared/handelskosten.py`) im Klon,\n'
     "    R110 (c). Gibt zurueck, wie oft ersetzt wurde - verlangt ist genau 1.\n"
     '    Eine Verknuepfung statt der Kopie waere das Repo: dann Abbruch."""\n'
     '    pfad = os.path.join(ordner, "shared", ORT)\n    if os.path.islink(pfad):\n'
     '        raise RuntimeError("shared/%s ist im Klon verknuepft - keine Mutation" % ORT)\n'
     "    with open(pfad) as f:\n        text = f.read()\n    anzahl = text.count(alt)\n"
     "    with open(pfad, \"w\") as f:\n        f.write(text.replace(alt, neu))\n    return anzahl\n", 1),
    ('        ersetzt = mutiere(ordner, "STARTING_CAPITAL = 10_000.0",\n                          "STARTING_CAPITAL = 20_000.0")\n',
     '        ersetzt = mutiere_ort(ordner, "STARTING_CAPITAL = 10_000.0",\n                              "STARTING_CAPITAL = 20_000.0")\n', 1),
    ('        mutiere(ordner, "STARTING_CAPITAL = 10_000.0", "STARTING_CAPITAL = 20_000.0")\n',
     '        mutiere_ort(ordner, "STARTING_CAPITAL = 10_000.0", "STARTING_CAPITAL = 20_000.0")\n', 2),
    ("             test_werkzeugverhalten, test_vergleichsregeln]\n",
     "             test_werkzeugverhalten, test_vergleichsregeln, test_ort_alle_neun]\n", 1),
    ("def main():\n",
     "def test_ort_alle_neun():\n"
     '    print("\\n11) Der Ort des Startkapitals traegt alle neun (R110 (c))")\n'
     "    ordner = probe_umgebung(bots=ALLE_NEUN)\n    ort = os.path.join(ordner, \"shared\", ORT)\n"
     "    repo_ort = os.path.join(_SHARED, ORT)\n"
     "    with open(ort, \"rb\") as f:\n        original = f.read()\n    with open(repo_ort, \"rb\") as f:\n        repo_vorher = f.read()\n\n"
     "    def kurven(etikett):\n        ziel = tempfile.mkdtemp(prefix=\"kurven_%s_\" % etikett)\n        inhalt = {}\n"
     "        for b in ALLE_NEUN:\n            os.makedirs(os.path.join(ziel, b))\n"
     "            r = subprocess.run([sys.executable, os.path.join(ordner, \"shared\", \"kurven_lauf.py\"), b,\n"
     "                                os.path.join(ziel, b)], capture_output=True, text=True, cwd=ordner, timeout=600)\n"
     "            datei = os.path.join(ziel, b, \"equity_curve.csv\")\n"
     "            inhalt[b] = None\n            if r.returncode == 0 and os.path.exists(datei):\n"
     "                with open(datei, \"rb\") as f:\n                    inhalt[b] = f.read()\n"
     "        shutil.rmtree(ziel, ignore_errors=True)\n        return inhalt\n\n"
     "    try:\n        vorher = kurven(\"vorher\")\n        fehlt = [b for b in ALLE_NEUN if vorher[b] is None]\n"
     "        check(\"neun Kurven vor der Mutation erzeugt\", not fehlt, \"fehlt: %s\" % fehlt if fehlt else \"%d von %d\" % (len(ALLE_NEUN), len(ALLE_NEUN)))\n"
     "        ersetzt = mutiere_ort(ordner, \"STARTING_CAPITAL = 10_000.0\", \"STARTING_CAPITAL = 20_000.0\")\n"
     "        check(\"Mutation am Ort, genau einmal\", ersetzt == 1, ersetzt)\n"
     "        mutiert = kurven(\"mutiert\")\n"
     "        gleich = [b for b in ALLE_NEUN if mutiert[b] is None or mutiert[b] == vorher[b]]\n"
     "        check(\"alle neun Kurven weichen ab\", not gleich and not fehlt,\n"
     "              \"gleich oder fehlend: %s\" % gleich if gleich else \"%d von %d\" % (len(ALLE_NEUN), len(ALLE_NEUN)))\n"
     "        with open(ort, \"wb\") as f:\n            f.write(original)\n"
     "        zurueck = kurven(\"zurueck\")\n        anders = [b for b in ALLE_NEUN if zurueck[b] is None or zurueck[b] != vorher[b]]\n"
     "        check(\"zurueckgesetzt: alle neun bytegleich\", not anders and not fehlt,\n"
     "              \"abweichend: %s\" % anders if anders else \"%d von %d\" % (len(ALLE_NEUN), len(ALLE_NEUN)))\n"
     "        with open(repo_ort, \"rb\") as f:\n"
     "            check(\"der Ort im Repo blieb unberuehrt\", f.read() == repo_vorher)\n"
     "    finally:\n        shutil.rmtree(ordner, ignore_errors=True)\n\n\n"
     "# ---------------------------------------------------------------------------\ndef main():\n", 1)]


def umbau(alt):
    """alt: {pfad: text am Stand vorher} -> {pfad: text nachher}; wirft AssertionError, wenn ein Anker nicht genau so oft steht."""
    neu = {}
    t = alt[HK]
    assert t.count("EIN Ort, zwei Konstanten") == 1 and "STARTING_CAPITAL" not in t and t.count("\nKeine Funktion,") == 1, "Anker handelskosten.py"
    t = t.replace("EIN Ort, zwei Konstanten", "EIN Ort, drei Konstanten", 1).replace("\nKeine Funktion,", HK_DOC + "\nKeine Funktion,", 1)
    assert t.endswith("\n"); neu[HK] = t + HK_KONST
    for b in BOTS:
        t = alt[ES[b]]; assert t.count(ALT) == 1 and "handelskosten import STARTING_CAPITAL" not in t, "Anker " + ES[b]
        neu[ES[b]] = t.replace(ALT, NEU, 1)
    t = alt[TEK]
    for a, n, k in TEK_ERS:
        assert t.count(a) == k, "Anker %s: %d statt %d" % (TEK, t.count(a), k); t = t.replace(a, n)
    neu[TEK] = t
    return neu


VG = "research/tb27_kapitalsimulation/vergleich.py"
VG_ERS = [
    ('DATEINAME = "equity_simulation.py"\n',
     'DATEINAME = "equity_simulation.py"\n\n'
     "# Der Ort des Startkapitals (29.3 nach R110 (b), TB-180): Seit TB-180 importieren\n"
     "# die neun `equity_simulation.py` STARTING_CAPITAL aus `shared/handelskosten.py`.\n"
     "# Fuer den Vergleich wird es dort gelesen (ast, ohne Import); eine eigene\n"
     "# Zuweisung in der Bot-Datei gilt weiterhin. `TB27_HANDELSKOSTEN` zeigt fuer die\n"
     "# Gegenprobe auf eine andere Datei. Der Waechter prueft den Wert (STARTKAPITAL).\n"
     '_HANDELSKOSTEN = (os.environ.get("TB27_HANDELSKOSTEN")\n'
     '                  or os.path.join(_WURZEL, "shared", "handelskosten.py"))\n'
     "STARTKAPITAL = 10_000.0\n", 1),
    ("def bots(dateiname=DATEINAME):\n",
     "def _ort_konstanten():\n"
     '    """Modulweite Zuweisungen in `shared/handelskosten.py`: Name -> (Quelltext, Wert)."""\n'
     "    with open(_HANDELSKOSTEN, encoding=\"utf-8\") as f:\n        text = f.read()\n    gefunden = {}\n"
     "    for knoten in ast.parse(text).body:\n        if isinstance(knoten, ast.Assign):\n"
     "            for ziel in knoten.targets:\n                if isinstance(ziel, ast.Name):\n"
     "                    gefunden[ziel.id] = (ast.unparse(knoten), ast.literal_eval(knoten.value))\n"
     "    return gefunden\n\n\ndef bots(dateiname=DATEINAME):\n", 1),
    ("        self.importe = []      # (modul, [namen])\n",
     "        self.importe = []      # (modul, [namen])\n        self.werte = {}        # Name -> Wert (nur Literale; 29.3)\n", 1),
    ("                        self.konstanten[ziel.id] = ast.unparse(knoten)\n",
     "                        self.konstanten[ziel.id] = ast.unparse(knoten)\n"
     "                        try:\n                            self.werte[ziel.id] = ast.literal_eval(knoten.value)\n"
     "                        except ValueError:\n                            pass\n", 1),
    ("                self.importe.append((modul, [a.name for a in knoten.names]))\n",
     "                self.importe.append((modul, [a.name for a in knoten.names]))\n"
     '                if modul == "handelskosten":\n                    ort = _ort_konstanten()\n'
     "                    for a in knoten.names:\n                        if a.name in ort:\n"
     '                            self.konstanten[a.asname or a.name] = ort[a.name][0] + "  (aus shared/handelskosten.py)"\n'
     "                            self.werte[a.asname or a.name] = ort[a.name][1]\n", 1),
    ("\n    if abweichungen:\n        print(\"ABWEICHUNG gegenueber",
     "\n    for datei in dateien:\n        wert = datei.werte.get(\"STARTING_CAPITAL\")\n"
     "        if not (type(wert) is float and wert == STARTKAPITAL):\n            abweichungen.append(\n"
     '                f"STARTKAPITAL  {datei.bot}: {wert!r}, Soll {STARTKAPITAL!r} "\n'
     '                f"(Ort shared/handelskosten.py, 29.3)")\n'
     "\n    if abweichungen:\n        print(\"ABWEICHUNG gegenueber", 1)]
_umbau_alt = umbau


def umbau(alt):
    neu = _umbau_alt(alt)
    t = alt[VG]
    for a, n, k in VG_ERS:
        assert t.count(a) == k, "Anker %s: %d statt %d" % (VG, t.count(a), k); t = t.replace(a, n)
    neu[VG] = t
    return neu

P9 = ["9. **Kosten (0,30 %) und Fill-Konvention** — `TRADING_FEE_PCT = 0,1` und", "   `SLIPPAGE_PCT = 0,05` je Order, Ein- und Ausstieg; Einstieg zum",
      "   Schlusskurs des Bestätigungsbalkens"]
md5 = lambda f: hashlib.md5(open(f, "rb").read()).hexdigest(); sha = lambda b: hashlib.sha256(b).hexdigest()
git = lambda *a: subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True, text=True).stdout
lies = lambda f: open(f, encoding="utf-8").read()
N = [0, 0]
def p(ok, text):
    N[0] += 1; N[1] += (not ok); print(("ja    " if ok else "NEIN  ") + text); return ok
def ende():
    print("Pruefungen: %d, NEIN: %d" % tuple(N)); sys.exit(1 if N[1] else 0)
def werte(text):
    w = {}
    for k in ast.parse(text).body:
        if isinstance(k, ast.Assign) and len(k.targets) == 1 and isinstance(k.targets[0], ast.Name) and isinstance(k.value, ast.Constant):
            w[k.targets[0].id] = k.value.value
    return w
def punkte(text):
    sys.path.insert(0, "shared"); import sperrlistensonde as s
    tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"), "tb180_reg_probe.md"); open(tmp, "w", encoding="utf-8").write(text)
    return s.lies_abschnitt_10(tmp)[0]
def nachtragzeilen(datum, c):
    return ["   — Ort: `shared/handelskosten.py` mit `TRADING_FEE_PCT`, `SLIPPAGE_PCT`",
            "   und `STARTING_CAPITAL` (sha256 `%s…` am Commit `%s`; Nachtrag" % (SHA_HK[:8], c), "   nach 38.5 und R110 (b), 71.1, TB-180, %s)" % datum]
def p9_ort(z):
    i = z.index("## 10. Die Sperrliste"); j = next(k for k in range(i, len(z)) if z[k] == P9[0]); return j

def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
BL_TEXT = (" · **TB-180 (%s, Journal %s)**: Bauauftrag nach 37.3 aus R110 (b) vollzogen — Nachtrag zu Punkt 9 (`shared/handelskosten.py`, drei Bezeichner, Hash), "
    "`STARTING_CAPITAL` am Ort (neun Importe, Kurven der neun vorher/nachher bytegleich), neues Abbild, Ergänzung zu 29.3 (Register 71); Probe nach R110 (c) in `shared/test_ergebniskurven.py` (Prüffall 11) |")
def index(s0, datum):
    tl = [t for t in range(1, 10) if os.path.exists(PJ + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 71. " in lies(PJ + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(tl) == 1, "Abschnitt 71 in genau einer Teildatei: %s" % tl); T = str(tl[0]) if len(tl) == 1 else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–70" in z[k[0]], "Kopf genau einmal, nennt 0–70"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–70", "Abschnitte 0–71")
    i = [j for j, l in enumerate(z) if l.startswith("| 70 aus 17e |")]
    if p(len(i) == 1, "Zeile 70 genau einmal"):
        z[i[0] + 1:i[0] + 1] = ["| 71 aus TB-180 | %s | Bauauftrag nach R110 (b) und Probe nach R110 (c): 71.1 Nachtrag zu Punkt 9, 71.2 Tatsachennotiz, 71.3 Ergänzung zu 29.3, 71.4 Abbild, 71.5 Probe | – |" % T]
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-178 (")]
    if p(len(j) == 1, "Pflegezeile TB-178 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-178 (", "In TB-178 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-180 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-180 (`index`); 71 kommt zu T%s; Nachtrag zu Punkt 9 (Abschnitt 10) und Marke an 29.3 (71.3)." % (datum, s0, rcm, T))
    if not N[1]: open(IDX, "w", encoding="utf-8").write("\n".join(z))
    ende()

if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "voraussetzung":
        for f, m in sorted(CODE.items()): p(os.path.exists(f) and md5(f) == m, "unveraendert: %s md5 %s" % (f, m[:12]))
        for b in BOTS:
            z = lies(ES[b]).split("\n"); k = [i + 1 for i, l in enumerate(z) if l == "STARTING_CAPITAL = 10_000.0"]
            p(k == [FUND[b]], "Fundstelle %s Z. %s STARTING_CAPITAL = 10_000.0 (Bau: Z. %d)" % (ES[b], k, FUND[b]))
        r = lies(REG); z = r.split("\n")
        p("R110 — Berichtigung" in r and "## 70. " in r and "\n## 71. " not in r, "Register: R110 eingetragen (TB-178), Abschnitt 70 da, 71 nicht")
        j = p9_ort(z); p(z[j:j + 3] == P9 and z[j + 3].startswith("   > ⚠️ **Ort registrierter Werte"), "Abschnitt 10 Punkt 9 Z. %d-%d wie am Bau, Kasten direkt darunter" % (j + 1, j + 3))
        p("handelskosten" not in "\n".join(z[z.index("## 10. Die Sperrliste"):next(k for k in range(z.index("## 10. Die Sperrliste") + 1, len(z)) if z[k].startswith("## "))]), "Abschnitt 10 nennt handelskosten noch nicht (kein Nachtrag zu Punkt 9)")
        p("71.1, TB-180" not in r and "ERGÄNZT durch 71.3" not in r, "Register: noch kein Nachtrag und keine Marke von TB-180 (TB-180 dort nur als Vorschlag)")
        ab = sorted(f for f in os.listdir("research/vorregistrierung/ergebnisse") if f.startswith("sperrliste_abbild_"))
        p(ab[-1] == "sperrliste_abbild_2026-09-26_tb117.json" and not [f for f in ab if "tb180" in f], "letztes Abbild sperrliste_abbild_2026-09-26_tb117.json, keines mit tb180")
        p("STARTING_CAPITAL" not in lies(HK), "shared/handelskosten.py traegt STARTING_CAPITAL noch nicht")
        p(not os.path.exists(BEL + "t_test.txt"), "keine Belege TB-180 aus einem frueheren Lauf")
        ix = lies(IDX).split("\n"); p(sum("Abschnitte 0–70" in l for l in ix if l.startswith("**Stand:**")) == 1 and sum(l.startswith("| 70 aus 17e |") for l in ix) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-178 (") for l in ix) == 1, "Index: Kopf 0–70, Zeile 70, Pflegezeile TB-178")
        info = max(kennungen()); print("info  Journal: hoechste Kennung %s, naechste %s" % (info, naechste(info)))
        z = lies(BL).split("\n"); r1 = [l for l in z if l.startswith(RANG1)]; p(len(r1) == 1 and r1[0].endswith(" |") and "TB-180 (" not in r1[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne Eintrag TB-180")
        ende()
    if cmd == "kurven":
        d = os.path.join(os.environ["TMPDIR"], "tb180_kurven_" + a[0]); erg = {}
        for b in BOTS:
            os.makedirs(os.path.join(d, b), exist_ok=True); f = os.path.join(d, b, "equity_curve.csv")
            r = subprocess.run([sys.executable, "-B", "shared/kurven_lauf.py", b, os.path.join(d, b)], capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            h = sha(open(f, "rb").read()) if r.returncode == 0 and os.path.exists(f) else None; erg[b] = h
            p(h is not None, "%s rc %d sha256 %s Zeilen %s" % (b, r.returncode, h, len(open(f).read().split("\n")) - 2 if h else "-") + ("" if h else " " + r.stderr.strip()[-200:]))
        json.dump(erg, open(d + ".json", "w"), indent=1); ende()
    if cmd == "vergleich":
        x, y = (json.load(open(os.path.join(os.environ["TMPDIR"], "tb180_kurven_%s.json" % e))) for e in a[:2]); g = 0
        for b in BOTS:
            ok = x.get(b) is not None and x.get(b) == y.get(b); g += ok; p(ok, "%s bytegleich %s / %s" % (b, (x.get(b) or "-")[:16], (y.get(b) or "-")[:16]))
        print("Ergebnis: %d von 9 bytegleich (%s gegen %s)" % (g, a[0], a[1])); ende()
    if cmd == "code":
        alt = {f: lies(f) for f in CODE if f in [HK, TEK, VG] + list(ES.values())}
        for f in alt: p(md5(f) == CODE[f], "vorher md5 = Bau: " + f)
        neu = umbau(alt)
        for f, t in neu.items(): p(hashlib.md5(t.encode("utf-8")).hexdigest() == NACH[f], "nachher md5 = Bau-Soll %s: %s" % (NACH[f][:12], f))
        if N[1] == 0 and "--probe" not in a:
            for f, t in neu.items(): open(f, "w", encoding="utf-8").write(t)
            for f in neu: p(md5(f) == NACH[f], "geschrieben: " + f)
        ende()
    if cmd == "code_pruefen":
        for f, m in NACH.items(): p(md5(f) == m, "md5 = Bau-Soll: " + f)
        w = werte(lies(HK)); p(w.get("STARTING_CAPITAL") == 10000.0 and type(w.get("STARTING_CAPITAL")) is float and w.get("TRADING_FEE_PCT") == 0.1 and w.get("SLIPPAGE_PCT") == 0.05,
                               "Werte am Ort: STARTING_CAPITAL %r, TRADING_FEE_PCT %r, SLIPPAGE_PCT %r" % (w.get("STARTING_CAPITAL"), w.get("TRADING_FEE_PCT"), w.get("SLIPPAGE_PCT")))
        p(lies(HK).count("STARTING_CAPITAL = 10_000.0") == 1, "Literal am Ort genau einmal (Mutation R110 (c))")
        for b in BOTS:
            t = lies(ES[b]); p("STARTING_CAPITAL" not in werte(t) and t.count("\nfrom handelskosten import STARTING_CAPITAL\n") == 1, "%s: keine eigene Zuweisung, ein Import" % ES[b])
            c = ("import sys, types; sys.path.insert(0, 'strategies/%s'); sys.argv = ['x']\nfor n in ('binance', 'binance.client', 'yfinance'): sys.modules.setdefault(n, types.ModuleType(n))\n"
                 "sys.modules['binance.client'].Client = type('_C', (), {'__getattr__': lambda s, n: n, '__call__': lambda s, *a, **k: s})()\nimport equity_simulation as es, handelskosten as hk, os\nprint(es.STARTING_CAPITAL is hk.STARTING_CAPITAL, os.path.relpath(hk.__file__))") % b
            r = subprocess.run([sys.executable, "-B", "-c", c], capture_output=True, text=True); s = (r.stdout.strip().split("\n") or [""])[-1]
            p(r.returncode == 0 and s == "True shared/handelskosten.py", "%s importiert STARTING_CAPITAL aus shared/handelskosten.py (%s)" % (b, s or r.stderr.strip()[-150:]))
        vg = lambda *x, **e: subprocess.run([sys.executable, "-B", VG] + list(x), capture_output=True, text=True, env=dict(os.environ, **e))
        r = vg("--pruefen"); v = lies(BEL + "v_vergleich.txt") if os.path.exists(BEL + "v_vergleich.txt") else None
        p(v is not None and r.stdout + r.stderr + "rc %d\n" % r.returncode == v, "vergleich.py --pruefen nach dem Umbau = vorher (v_vergleich.txt), rc %d" % r.returncode)
        u = vg().stdout; p(u.count("STARTING_CAPITAL = 10000.0  (aus shared/handelskosten.py)") == 9, "vergleich.py Uebersicht: STARTING_CAPITAL 9x aus shared/handelskosten.py")
        m = os.path.join(os.environ.get("TMPDIR", "/tmp"), "tb180_hk_gegenprobe.py"); open(m, "w", encoding="utf-8").write(lies(HK).replace("STARTING_CAPITAL = 10_000.0", "STARTING_CAPITAL = 20_000.0"))
        g = vg("--pruefen", TB27_HANDELSKOSTEN=m); n = g.stdout.count("STARTKAPITAL  ")
        p(g.returncode == 1 and n == 9 and r.stdout.count("STARTKAPITAL  ") == 0, "Gegenprobe vergleich.py: Ort auf 20_000.0 -> rc %d, %d STARTKAPITAL-Zeilen (Soll 1, 9); Ort echt: 0" % (g.returncode, n))
        ende()
    if cmd == "nachtrag":
        datum, c = a[0], a[1]; r = lies(REG); z = r.split("\n"); j = p9_ort(z)
        p(sha(open(HK, "rb").read()) == SHA_HK and sha(git("show", "%s:%s" % (c, HK)).encode("utf-8")) == SHA_HK, "sha256 shared/handelskosten.py = Bau-Soll = Commit %s: %s" % (c, SHA_HK))
        p(z[j:j + 3] == P9 and z[j + 3].startswith("   > ⚠️"), "Punkt 9 Z. %d-%d zeichengleich, Kasten darunter" % (j + 1, j + 3))
        nz = z[:j + 3] + nachtragzeilen(datum, c) + z[j + 3:]; neu = "\n".join(nz)
        v, n = punkte(r), punkte(neu)
        p(len(v) == len(n) == 14 and all(v[i] == n[i] for i in range(14) if i != 8), "Sonden-Parser: 14 Punkte, ausser Punkt 9 unveraendert")
        p(n[8]["pfade"] == ["shared/handelskosten.py"] and n[8]["titel"] == v[8]["titel"] and v[8]["pfade"] == [], "Punkt 9: Pfad shared/handelskosten.py, Titel gleich (vorher pfade %s)" % v[8]["pfade"])
        p(nz[:j + 3] == z[:j + 3] and nz[j + 6:] == z[j + 3:], "additiv: drei Folgezeilen nach Z. %d, sonst zeichengleich" % (j + 3))
        print("\n".join(nachtragzeilen(datum, c)))
        if N[1] == 0 and "--probe" not in a: open(REG, "w", encoding="utf-8").write(neu); p(lies(REG) == neu, "geschrieben, Z. %d-%d" % (j + 4, j + 6))
        ende()
    if cmd == "register":
        datum, s0, c, abb = a[:4]; r = lies(REG); z = r.split("\n")
        t = lies(AUFTRAG).split("\n"); i0 = [i for i, l in enumerate(t) if l.startswith("## Freigabe")]; i1 = next(i for i in range(i0[0] + 1, len(t)) if t[i].startswith("## "))
        karte = [l for l in t[i0[0] + 1:i1] if l.startswith("> ")]; p(len(karte) == 1 and "⟨⟨" not in karte[0], "Karte des Betreibers gefuellt")
        fund = []
        for b in BOTS:
            q = git("show", "%s:%s" % (s0, ES[b])).split("\n"); k = [i + 1 for i, l in enumerate(q) if l == "STARTING_CAPITAL = 10_000.0"]
            p(k == [FUND[b]], "Fundstelle am %s: %s Z. %s" % (s0, ES[b], k)); fund.append("- `%s` Z. %d `STARTING_CAPITAL = 10_000.0`" % (ES[b], FUND[b]))
        hk = git("show", "%s:%s" % (c, HK)); w = werte(hk); zk = [i + 1 for i, l in enumerate(hk.split("\n")) if l.startswith("STARTING_CAPITAL = ")]
        p(sha(hk.encode("utf-8")) == SHA_HK and w.get("STARTING_CAPITAL") == 10000.0 and len(zk) == 1, "Ort am Commit %s: Z. %s, Wert %r" % (c, zk, w.get("STARTING_CAPITAL")))
        bl = lambda f: lies(BEL + f).split("\n") if os.path.exists(BEL + f) else []
        verg = [l for l in bl("n_vergleich.txt") if l.startswith("Ergebnis: ")]; p(verg == ["Ergebnis: 9 von 9 bytegleich (vorher gegen nachher)"], "Kurven vorher/nachher: %s" % verg)
        tt = bl("t_test.txt"); tz = [l.strip() for l in tt if re.search(r"(neun Kurven|Mutation am Ort|alle neun Kurven|zurueckgesetzt: alle neun|Ort im Repo)", l)]
        ts = [l for l in tt if "Pruefungen bestanden" in l]; p(len(tz) == 5 and all(l.startswith("[OK ]") for l in tz) and ts and ts[-1].endswith(", 0 fehlgeschlagen."), "Probe R110 (c): %s; %s" % (len(tz), ts[-1:] ))
        sn = bl("b_sonde_neu.txt"); sa = bl("b_sonde_alt.txt"); pb = [l for l in sn if l.startswith("Pfad-Bestandteile:")]; rn = [l for l in sn if l.startswith("RUECKGABEWERT")]; ra = [l for l in sa if l.startswith("RUECKGABEWERT")]
        p(os.path.exists(abb) and pb and rn and not rn[0].startswith("RUECKGABEWERT 1") and ra and ra[0].startswith("RUECKGABEWERT 1"), "Abbild da; Sonde neu ohne Befund, alt mit Befund")
        j = p9_ort(z); p(z[j + 3:j + 6] == nachtragzeilen(datum, c), "Nachtrag zu Punkt 9 steht (Z. %d-%d)" % (j + 4, j + 6))
        ka = [i for i, l in enumerate(z) if l.startswith("### 29.4 ")]; p(len(ka) == 1 and z[ka[0] - 1] == "", "29.4 eindeutig, Leerzeile davor")
        m = ["", "> ⭐ **29.3 ERGÄNZT durch 71.3** (Bauauftrag nach R110 (b), Schritt (4), TB-180, %s)." % datum, "> Eintrag und Stand oben bleiben zeichengleich."]
        hab = sha(open(abb, "rb").read()) if os.path.exists(abb) else "-"
        s71 = ["", "## 71. Bauauftrag nach R110 (b) und Probe nach R110 (c) — Startkapital am Ort (TB-180)", "",
               "Eingetragen mit TB-180 am %s (Auftrag `%s`): Bauauftrag nach 37.3 aus R110 (b) (70.1, Fable 17e), vier Schritte, dann die Probe nach R110 (c). Handelscode mit Freigabe des Betreibers, Karte wörtlich:" % (datum, AUFTRAG), "",
               karte[0] if karte else "> -", "", "Commits: Stand vor dem Umbau `%s`, Umbau `%s`. R109 und R110 bleiben zeichengleich." % (s0, c), "",
               "### 71.1 Nachtrag zu Punkt 9 (Schritt (1))", "",
               "⭐ **Der Punkttext von Abschnitt 10, Punkt 9, ist geändert — additiv** (Bauart 39.2). Die drei Zeilen davor und die Kästen darunter sind zeichengleich (38.4). Nach der Zeile `   Schlusskurs des Bestätigungsbalkens` stehen drei neue Folgezeilen:", "",
               "```"] + nachtragzeilen(datum, c) + ["```", "", "| Datei | Bezeichner | Werte am Commit `%s` | sha256 (Stand nach Schritt (2)) |" % c, "|---|---|---|---|",
               "| `shared/handelskosten.py` | `TRADING_FEE_PCT`, `SLIPPAGE_PCT`, `STARTING_CAPITAL` | %r / %r / %r | `%s` |" % (w.get("TRADING_FEE_PCT"), w.get("SLIPPAGE_PCT"), w.get("STARTING_CAPITAL"), SHA_HK), "",
               "### 71.2 Tatsachennotiz zu Schritt (2) und zur Sonde", "",
               "**(a)** `STARTING_CAPITAL = 10_000.0` steht am Commit `%s` in `shared/handelskosten.py` Z. %s; die neun `strategies/<bot>/equity_simulation.py` tragen keine eigene Zuweisung mehr, sondern an deren Stelle `from handelskosten import STARTING_CAPITAL` (Fundstellen vorher in 71.3)." % (c, zk[0] if zk else "?"),
               "**(b)** Kurven der neun mit `shared/kurven_lauf.py` (ohne neue Kursdaten) am Stand `%s` und nach dem Umbau, sha256 je Bot (`%sm_vorher.txt`, `%sn_nachher.txt`, `%sn_vergleich.txt`): %s" % (s0, BEL, BEL, BEL, verg[0] if verg else "-"),
               "**(c)** Sonde (R110 (b), 37.5 (1)): Der Datei-Hash ist die Sperre. Bis zum Tag bleibt Punkt 9 bei 2 (Regel-Bestandteil), mit dieser Notiz (37.1): Wert in Datei gleich Registerwert, am Commit `%s` — `STARTING_CAPITAL` %r = 10 000 (71.3), `TRADING_FEE_PCT` %r = 0,1, `SLIPPAGE_PCT` %r = 0,05 (Punkt 9). Keine neue Bauart der Sonde." % (c, w.get("STARTING_CAPITAL"), w.get("TRADING_FEE_PCT"), w.get("SLIPPAGE_PCT")), "",
               "### 71.3 Ergänzung zu 29.3 (Schritt (4), Fassung R110 (b))", "", "> " + SATZ, "",
               "**Tatsachennotiz (R108 (d) (1), 68.2 (a)) — die neun Fundstellen am Commit der Tatsachennotiz `%s`:**" % s0, ""] + fund + ["",
               "Der Nachtrag zu Punkt 9 steht (71.1); damit ist die Bedingung „sobald“ erfüllt.", "",
               "### 71.4 Neues Abbild (Schritt (3))", "",
               "`%s` (%s B, sha256 `%s`), einmalig geschrieben mit `research/vorregistrierung/sperrliste_abbild.py` (36.6), nach 71.1. Sonde dagegen (`%sb_sonde_neu.txt`), wörtlich: `%s` · `%s`. Gegenprobe, das Abbild davor (`sperrliste_abbild_2026-09-26_tb117.json`) gegen das Register nach 71.1 (`%sb_sonde_alt.txt`): `%s`." % (
                   abb, os.path.getsize(abb) if os.path.exists(abb) else "-", hab, BEL, pb[0] if pb else "-", rn[0] if rn else "-", BEL, ra[0] if ra else "-"), "",
               "### 71.5 Probe nach R110 (c)", "",
               "`shared/test_ergebniskurven.py` (Handwerk in der Freigabe, R31 (b)), Prüffall 11 (`%st_test.txt`), wörtlich:" % BEL, ""] + ["    " + l for l in tz] + ["    " + (ts[-1] if ts else "-"), "",
               "**Kette:** R109 (a) → R110 (b) → 37.3 → 71.1 bis 71.4; R110 (c) → 71.5. Ohne Marke: R109, R110, 37.5, 38.5, Abschnitt 10 ausser dem Nachtrag."]
        nz = z[:ka[0] - 1] + m + z[ka[0] - 1:]
        while nz and nz[-1] == "": nz.pop()
        neu = "\n".join(nz + s71) + "\n"
        p(neu.startswith("\n".join(z[:ka[0] - 1])) and "\n".join(z[ka[0] - 1:]).rstrip("\n") in neu, "append-only bis auf die Marke an 29.3")
        if N[1] == 0 and "--probe" not in a: open(REG, "w", encoding="utf-8").write(neu); p(lies(REG) == neu, "geschrieben: Marke vor Z. %d, Abschnitt 71" % (ka[0] + 1))
        ende()
    if cmd == "index": index(a[0], a[1])
    if cmd == "handfelder":
        h = json.load(open("docs/belege/TB-178/k_handfelder.json", encoding="utf-8"))
        for d in ("17d", "17e"): h[d]["offen"] = "nein"; h[d]["entscheidung"] += "; vollzogen mit TB-178 und TB-180 (Register 69–71)"
        json.dump(h, open(a[0], "w", encoding="utf-8"), ensure_ascii=False, indent=1); print("Handfelder 17d, 17e (offen: nein) geschrieben: %s" % a[0]); sys.exit(0)
    if cmd == "kennung": k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k))); sys.exit(0)
    if cmd == "backlog":
        datum, kenn = a[0], a[1]
        if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
        z = lies(BL).split("\n"); i = [n for n, l in enumerate(z) if l.startswith(RANG1)]
        if p(len(i) == 1 and z[i[0]].endswith(" |") and "TB-180 (" not in z[i[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne Eintrag TB-180"): z[i[0]] = z[i[0]][:-2] + BL_TEXT % (datum, kenn)
        if not N[1] and "--probe" not in a: open(BL, "w", encoding="utf-8").write("\n".join(z))
        ende()
    if cmd == "journal":
        b = lies(a[0]).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen())); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
        p(b[0].startswith("## %s — TB-180: " % neu), "Kopfzeile ## %s — TB-180: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
        p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
        if not N[1] and "--probe" not in a: z[i[0] - 2:i[0] - 2] = b + [""]; open(JO, "w", encoding="utf-8").write("\n".join(z))
        ende()
    print("unbekannter Befehl", cmd); sys.exit(2)
