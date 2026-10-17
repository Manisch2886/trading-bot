#!/usr/bin/env python3
"""TB-175 Werkzeug (Anhang A): Pruefung 13 in test_haltedauer_kern.py erneuern - Fable 17b ins Register (Abschnitt 67, R107 zeichengleich, neun Marken, 67.2), Index, Handfelder; Voraussetzungen, Gegenprobe an Kopien, Nachher-Pruefung, Kennung, BACKLOG, Journal.
Python 3.9, Aufruf aus der Repo-Wurzel. Nur gegenprobe importiert den Test (numpy/pandas). --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | nachher2 | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | gegenprobe | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, sys
P = "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-175/"
GR = "research/tb24_haltedauern/"
TEST, TSHA, BASIS = GR + "test_haltedauer_kern.py", "b73adc87d57c764eb71ee00f725019dcedb70164599a20c7e9c77e6d065f8cba", "807d278e60a953cac40a836d28d13c96"
CODE = { "research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/tb24_haltedauern/auswertung.py": "c15e6375520e1aeccc41ce152ca3b870", "research/tb24_haltedauern/haltedauer_kern.py": "60942de99b323fa472ae25478a5a6836", "research/tb24_haltedauern/live_haltedauern.py": "7d21a66cd3173a99adff2c9c1346c815", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd" }
ALT13 = "  FEHLT wer schreibt, schreibt in den eigenen Ordner (aussen vor: ['positionen_holen.py'])"
KOPF13, N13 = "13. Wache: die Untersuchung fasst nichts ausserhalb ihres Ordners an", 8
RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "Gruppe unveraendert: %s md5 %s" % (f, m[:12]))
def beleg(n): return lies(BEL + n).rstrip("\n").split("\n") if os.path.exists(BEL + n) else [""]
def voraussetzung():
    code_gleich(); p(md5f(TEST) == BASIS, "Test vor E = Bau-Stand (md5 %s, Pruefung 13 alt)" % BASIS[:12])
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-175" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-175")
    k = kennungen(); p(max(k) in ("FK", "FL"), "Journal: hoechste %s (FK am Bau-HEAD)" % max(k))
    voraussetzung_reg(); ende()
def gegenprobe():
    """An Kopien der Gruppe im Temp-Ordner: unveraendert gruen; mit Voreinstellung fuer --ziel bzw. open(..., "w") statt _schreibe_einmal rot."""
    import importlib.util, shutil, tempfile
    sys.dont_write_bytecode = True; sys.path.insert(0, os.path.abspath(GR)); basis = os.environ.get("TMPDIR") or tempfile.gettempdir()
    spec = importlib.util.spec_from_file_location("tb175_test13", os.path.abspath(TEST)); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
    t._ARBEITSBAUM_ZU_BEGINN = t._arbeitsbaum(); t.LEISE = True
    for fall, alt, neu in (("kontrolle", None, None), ("voreinstellung", '_aufruf.add_argument("--ziel", required=True,', '_aufruf.add_argument("--ziel", required=True, default=".",'),
                           ("open_w", 'hashes[f"{BOT}_alle_trades.csv"] = _schreibe_einmal(\n        f"{BOT}_alle_trades.csv", alle.to_csv(index=False))',
                            'open(os.path.join(ZIEL_DIR, f"{BOT}_alle_trades.csv"), "w").write(\n        alle.to_csv(index=False))')):
        o = tempfile.mkdtemp(prefix="tb175_%s_" % fall, dir=basis); n = 1
        for name in sorted(os.listdir(GR)):
            if name.endswith(".py") and not name.startswith("test_"): shutil.copy(GR + name, o)
        if alt:
            q = lies(o + "/positionen_holen.py"); n = q.count(alt); schreibe(o + "/positionen_holen.py", q.replace(alt, neu))
        del t.FEHLER[:]; t.wache_repo_unveraendert(o); fe = list(t.FEHLER)
        if alt is None: p(fe == [], "Kopie %s (%s): Pruefung 13 gruen, FEHLT %d" % (fall, o, len(fe)))
        else: p(n == 1 and any(f.startswith("wer schreibt") and "positionen_holen.py" in f for f in fe), "Kopie %s: Ersetzung %d-mal, Pruefung 13 rot: %s" % (fall, n, [f[:160] for f in fe][:3]))
    ende()
def nachher():
    code_gleich(); p(sha(TEST) == TSHA, "Test im Repo = Anhang (sha256 %s)" % TSHA[:12])
    a, e, g = beleg("e_alt.txt"), beleg("e_neu.txt"), beleg("e_gegenprobe.txt")
    p(a[-1] == "rc 1" and [l for l in a if l.startswith("  FEHLT")] == [ALT13], "e_alt.txt: rc 1, einziges FEHLT = alte Pruefung 13 an positionen_holen.py")
    p(e[-1] == "rc 0" and len(e) > 1 and e[-2] == "Alle Pruefungen bestanden." and not [l for l in e if "FEHLT" in l], "e_neu.txt: 'Alle Pruefungen bestanden.', rc 0, kein FEHLT")
    vor = lambda z: [l for l in z[:z.index(KOPF13)] if l.startswith("  ok")] if KOPF13 in z else None
    va, ve = vor(a), vor(e)
    p(va is not None and va == ve and len(va) > 0, "uebrige Pruefungen (vor 13) unveraendert gruen: alt %s, neu %s ok-Zeilen, gleich" % (len(va or []), len(ve or [])))
    s13 = [l for l in e[e.index(KOPF13) + 1:] if l.startswith("  ok")] if KOPF13 in e else []
    p(len(s13) == N13 and sum("Gegenprobe 13:" in l for l in s13) == N13 - 2 and any("(aussen vor: keine)" in l for l in s13), "e_neu.txt Pruefung 13: %d ok (Arbeitsbaum, Schreibziele, %d Gegenproben)" % (len(s13), N13 - 2))
    p(g[-1] == "rc 0" and sum(l.startswith("ja    Kopie") for l in g) == 3, "e_gegenprobe.txt: 3 Kopien wie Soll, rc 0")
    ende()
BL_TEXT = (" · **Register 67 (Fable 17b, R107) mit TB-175 (%s, Journal %s)**: R107 (a) **Zeilenschnitt** am Horizontbeginn vor der Indikatorbildung bei `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` **vor R44**, je Bot ein eigener Bauauftrag (Handelscode, Bauart E-6, 37.3 mit Hashes je Datei, eine Freigabe je Auftrag, Abnahme mit Gegenprobe 40.7 auf dem Test-Snapshot); R107 (c) **Modus-Wache im Listen-Erzeuger vor R44** (vor dem ersten Lesen Selektionsmodus gesetzt und DATA_DIR = Snapshot-Wurzel, sonst 2; Probe nach R86 (d) mit Gegenprobe); R107 (d) **Sammler zulässig** unter den Bedingungen aus R107 (d), **Kandidaten mit Orders (S-B1, KI-Bot) laufen nicht vor ihrer Zulassung**, auch nicht als Papierpfad; Voraussetzungen R107 (b) (Teilmessung, zur Kenntnis an den Verfahrensprüfer) und (e) gemessen (67.2 (a), (b)); **`research/mtm_drawdown/grundlage.py`** liest die TB-24-Liste und das Startkapital aus der Meta (Z. 189–198) gegen R107 (e) und 37.5 (2): umstellen auf Rekonstruktion nach R97 (b) (Vorbild `research/wf_kapital_dd/messung.py`) mit Startkapital aus Register 29.3 (`messung.py`, `test_mtm_kern.py` mit); Befund `research/wf_kapital_dd/messung.py` Z. 120: Startkapital aus `es.STARTING_CAPITAL` statt aus Register 29.3 → zur nächsten Fable-Anfrage; **nächster Bauauftrag nach der Fable-Antwort zu D4: E2** — `research/tb24_haltedauern/auswertung.py` und `research/faltenplan_neun/embargo_neun.py` auf alle gefundenen Trades (R107 (e); gebaut und an einer Kopie geprobt, nicht im Repo); über alle gefundenen Trades ergäbe D4 (`test_faltenplan_neun.py`) für t3_supertrend P90 8,6833 statt 9,5000, Embargo 12 statt 13 (registrierte Herleitung ändert sich), die übrigen acht Bots gleich; Frage an den Verfahrensprüfer · **TB-175 Teil 1: Prüfung 13 in `" + TEST + "` erneuert** (seit 46e3ed0/TB-98 rot, jetzt grün: je Schreibaufruf ein erlaubter Ort, "
    "ERGEBNIS_DIR/DATEN_DIR aus `_DIR`; `positionen_holen.py`: ZIEL_DIR nur aus Pflicht-`--ziel` ohne Voreinstellung, Schreiben nur über `_schreibe_einmal` mit O_EXCL; "
    "sechs Gegenproben im Test, an Kopien Voreinstellung und `open(..., \"w\")` rot; übrige Prüfungen unverändert grün); Teil (a): git-Aufrufe im Test mit `--no-optional-locks` |")
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-175" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-175"):
        z[a[0]] = z[a[0]][:-2] + BL_TEXT % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-175: " % neu), "Kopfzeile ## %s — TB-175: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
# --- Registerauftrag Fable 17b (R107, Abschnitt 67, neun Marken) - Bauart TB-173 ---
import json, subprocess
REG, IDX, DI = "docs/VORREGISTRIERUNG_neuselektion.md", P + "REGISTER_INDEX.md", P + "FABLE_DIALOG_INDEX.md"
AUF, QU = "docs/auftraege/MAC_TB-175_pruefung13_leser_alle_trades.md", "data_sicherung/steuernder_chat_tmp/f17b/"
FA = P + "FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md"; FQ = P + "FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md"
MD5F = {"docs/projektfuehrung/FABLE_ANTWORT_2026-10-17b_r102d_schnitt_t3_geschlossen_modus_sammler_quelle.md": "d13e691973d3b98528b72c67ac000eb9", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17b_r102d_vorlauf_t3_selektionsmodus.md": "af2c861a88a083dd7652dcbc07650d8f"}
KOPF_A = "## Registerblock — zeichengleich kopierbar, nummeriert (ab R107)"
TITEL = "## 67. Fable 17b — Registerblock R107 (TB-175)"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | zg | ende | Absatzanfang, Kopf der Marke, Zusatz) - R107 (f)
MARKEN = [("62.3", "### 62.3 ", "quelle", "62.3 R102 ERGÄNZT und BERICHTIGT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (a): ERGÄNZT zu (d), BERICHTIGT zu (c) („lies“)"),
          ("55.4", "### 55.4 ", "zg", "55.4 R81 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (a)"),
          ("66.1", "### 66.1 ", "quelle", "66.1 R106 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (b)"),
          ("64.1", "### 64.1 ", "**Abnahme nach R98 (d)**", "64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (b)"),
          ("56.3", "### 56.3 ", "zg", "56.3 R86 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkte (c) und (e)"),
          ("57.3", "### 57.3 ", "quelle", "57.3 R92 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (c): die Voraussetzung in (c) ist gemessen erfüllt"),
          ("16.4", "### 16.4 ", "ende", "16.4 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (d)"),
          ("16.8", "### 16.8 ", "ende", "16.8 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (d)"),
          ("58.4", "### 58.4 ", "quelle", "58.4 R97 ERGÄNZT durch R107 (67.1)", "Fable 17b R107, Unterpunkt (e)")]
CODE_E2 = {"research/faltenplan_neun/embargo_neun.py": "b93af14604112c427ab1a3f1606fccc6", "research/mtm_drawdown/grundlage.py": "81cf1c93243a8248b96cf072e07fc289", "research/mtm_drawdown/messung.py": "00eb23079f1b92532f48f099f74dbe2f", "research/mtm_drawdown/test_mtm_kern.py": "80f1511a18d26a61537748c2739d0d79", "research/wf_kapital_dd/messung.py": "94c091f4c4e13ff4aa2e867dd4fd4fa5"}
NEU_E2 = {"research/tb24_haltedauern/auswertung.py": "fbafe5291c305bb64fa27a216100c006bd6c1c912dc981c69583cfcd70c2eb8d", "research/faltenplan_neun/embargo_neun.py": "ad11bd0ca33d28ca179101cd94f262ca42ba46e9507010578279577b1f4fa58f"}
PROBE_E2, PSHA = BEL + "tb175_probe_leser.py", "adbdd1451eb4270d1e74b4ce30d2914e5511faec3bcfbbbe9463c30159099297"
FUND = {"abn": ["docs/belege/TB-169/e_abnahme.txt", 85, 85, ["ja    t3_supertrend: 3b spaetes Symbol CCC gleich mit/ohne Schranke · 16/16"]], "tle_tag": ["research/tb24_haltedauern/test_listen_erzeuger.py", 159, 163, ["    c0 = b[b[\"symbol\"] == \"CCC\"]", "    if len(c0):", "        r = lauf(bot, seed, False, \"\", json.dumps({\"CCC\": str(c0[\"entry_time\"].min().date())})); x = tab(r[\"liste\"])", "        y = x[x[\"symbol\"] == \"CCC\"].reset_index(drop=True)[[\"entry_time\", \"exit_time\"]] if x is not None else None", "        pruefe(bot + \": 3b spaetes Symbol CCC gleich mit/ohne Schranke\", y is not None and y.equals(c0.reset_index(drop=True)[[\"entry_time\", \"exit_time\"]]), \"%s/%d\" % (None if y is None else len(y), len(c0)))"]], "tle_modus": ["research/tb24_haltedauern/test_listen_erzeuger.py", 161, 161, ["        r = lauf(bot, seed, False, \"\", json.dumps({\"CCC\": str(c0[\"entry_time\"].min().date())})); x = tab(r[\"liste\"])"]], "tle_wachen": ["research/tb24_haltedauern/test_listen_erzeuger.py", 85, 86, ["    if \"wache1_aus\" in modus: ph.wache_zeilen = lambda a: None", "    if \"wachen_aus\" in modus: ph.wache_zeilen = lambda a: None; ph.wache_trades = lambda tr, h: None"]], "tle_aus": ["research/tb24_haltedauern/test_listen_erzeuger.py", 87, 88, ["    if \"schranke_aus\" in modus:", "        alt = ph.basis.hole_trades; ph.basis.hole_trades = lambda es, a, h=None: alt(es, a)"]], "tle_p8": ["research/tb24_haltedauern/test_listen_erzeuger.py", 177, 177, ["    pruefe(bot + \": 8 nur Dateien des Test-Snapshots gelesen (%d read_csv)\" % (A[\"gelesen\"] + B[\"gelesen\"]), not A[\"fremd\"] and not B[\"fremd\"] and A[\"gelesen\"] > 0, (A[\"fremd\"] + B[\"fremd\"])[:2])"]], "aus_lade": ["research/tb24_haltedauern/auswertung.py", 69, 71, ["def lade(bot: str, nur_ausgefuehrt: bool = True) -> pd.DataFrame:", "    if nur_ausgefuehrt:", "        pfad = os.path.join(DATEN_DIR, f\"{bot}_positionen.csv\")"]], "emb": ["research/faltenplan_neun/embargo_neun.py", 232, 232, ["    pfad = os.path.join(basis or BASE_DIR, TB24_DATEN, f\"{bot}_positionen.csv\")"]], "gl_meta": ["research/mtm_drawdown/grundlage.py", 189, 198, ["        \"startkapital_meta\": meta.get(\"startkapital\"),", "        \"allocation_pct_meta\": meta.get(\"allocation_pct\"),", "        \"positionslimit_meta\": meta.get(\"max_concurrent_positions\"),", "        \"abgleich_exposure_messung_identisch\": (meta.get(\"abgleich_exposure_messung\") or {}).get(\"identisch\"),", "    }", "", "    # Kette der Kapitalstaende - schliesst sie, ist die Liste die einer", "    # Kapitalsimulation und die Kurvenreihenfolge rekonstruierbar.", "    try:", "        ereignisse = mtm_kern.ereignisreihenfolge(pos, float(meta[\"startkapital\"]))"]], "wf": ["research/wf_kapital_dd/messung.py", 120, 120, ["    startkapital = float(es.STARTING_CAPITAL)"]], "mg": ["research/vorregistrierung/messgroessen.py", 230, 231, ["    pfad = os.path.join(BASE_DIR, \"research\", \"tb24_haltedauern\",", "                        \"ergebnisse\", \"haltedauern_je_bot.csv\")"]]}
D4 = {"p90a": "8,6833", "p90p": "9,5000", "emba": 12, "embp": 13}
def fz(k): f, a, e, _t = FUND[k]; return "Z. %d" % a if a == e else "Z. %d–%d" % (a, e)
def fund_ok():
    for k, (f, a, e, t) in sorted(FUND.items()):
        z = lies(f).split("\n") if os.path.exists(f) else []; p(z[a - 1:e] == t, "Fundstelle %s: %s %s unveraendert (Bau-Stand)" % (k, f, fz(k)))
def nachher2():
    for f, m in sorted(CODE.items()):
        if not f.endswith("auswertung.py"): p(md5f(f) == m, "E2 unveraendert: %s md5 %s" % (f, m[:12]))
    for f, m in sorted(CODE_E2.items()):
        if not f.endswith("embargo_neun.py"): p(md5f(f) == m, "E2 unveraendert (Messung nach R94 (b), nicht Teil von E2): %s md5 %s" % (f, m[:12]))
    for f, s in sorted(NEU_E2.items()): p(sha(f) == s, "E2 umgestellt: %s = Anhang (sha256 %s)" % (f, s[:12]))
    p(sha(PROBE_E2) == PSHA and sha(TEST) == TSHA, "Probe E2 = Anhang E, Test = Anhang B")
    pr, te = beleg("e2_probe.txt"), beleg("e2_test.txt")
    p(pr[-2:] == ["Ergebnis: 9 von 9 bestanden", "rc 0"], "e2_probe.txt: 9 von 9, rc 0")
    p(te[-2:] == ["Alle Pruefungen bestanden.", "rc 0"] and any("Gegenprobe 13: auswertung.py schreibt neben ERGEBNIS_DIR -> auswertung.py faellt auf" in l for l in te), "e2_test.txt: Test am neuen auswertung.py gruen, Gegenprobe 6 trifft")
    ende()
OHNE = "28.6, 51.2 (R57), 26.2, 16.9, 62.2 (R101), 55.1 (R78), 56.1 (R84), 48.13 (R45), 57.1 (R90), 61.1 (R98), 58.1 (R94), 58.2 (R95), 60.1, 63.1, 24.3, 17.1, 17.2, 29.3, 37.3, 37.5, 40.6, 62.5, 66.2, Abschnitt 9, 10, 41, 42"
def info(t): OUT.append("info  " + t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def block():
    """((R-Zeile, Quellenzeile), Z. Zaun auf, Z. Zaun zu) oder None."""
    z = lies(FA if os.path.exists(FA) else QU + os.path.basename(FA)).split("\n")   # vor Schritt 0 (nur am Bau): die Quelle
    if z.count(KOPF_A) != 1: return None
    a = z.index(KOPF_A) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [z[i] for i in range(a + 1, e) if z[i]]; soll = ["R107 — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for l, s in zip(b, soll)] != soll: return None
    return (b[0], b[1]), a + 1, e + 1
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m):
    """Index der Einfuegestelle (nach dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any("R107" in z[i] for i in range(a, e)): return None
    if m[2] == "zg": k = [i for i in range(a, e) if z[i] == ZG][-1:]
    elif m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    elif m[2] == "ende":
        j = e - 1
        while j > a and z[j] in ("", "---"): j -= 1
        k = [j] if j > a else []
    else:
        k = [i for i in range(a, e) if z[i].startswith(m[2])]
        if len(k) == 1:
            while k[0] + 3 < e and z[k[0] + 1] == "" and z[k[0] + 2].startswith("> ⭐ ") and z[k[0] + 3] == ZG: k[0] += 3
    return k[0] + 1 if len(k) == 1 else None
def markenzeilen(m, datum): return ["", "> ⭐ **%s** (%s, TB-175, %s)." % (m[3], m[4], datum), ZG]
def stand_kopf():
    z = lies(IDX).split("\n"); return z, [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def md5cmd():
    for f in (FA, FQ): p(md5f(QU + os.path.basename(f)) == MD5F[f] and md5f(f) == MD5F[f], "md5 vorher %s = nachher %s = %s" % (QU + os.path.basename(f), f, MD5F[f]))
    ende()
def voraussetzung_reg():
    for f in (FA, FQ): p(verfolgt_gleich(f) and md5f(f) == MD5F[f], "R56 (b)/S0-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5F[f]))
    b = block(); p(b is not None, "Registerblock 17b: genau R107 und Quelle im Codeblock (Z. %s)" % ("%d–%d" % (b[1], b[2]) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 66. ") for l in z) == 1 and not any(l.startswith("## 67. ") for l in z) and not re.search(r"\bR107\b", reg), "Register: 66 da, 67 nicht; R107 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for m in MARKEN: i = einfuege(z, m); p(i is not None, "Ort %s: Einfuegestelle nach Z. %s eindeutig, R107 dort noch nicht genannt" % (m[0], i if i else "?"))
    zi, k = stand_kopf(); p(len(k) == 1 and "Abschnitte 0–66" in zi[k[0]], "Index-Kopf Z. %s nennt 0–66" % (k[0] + 1 if k else "?"))
    p(sum(l.startswith("| 66 aus 17a |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-173 (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and not any(l.startswith("## 18. ") for l in zi), "Index: Zeile 66, Pflegezeile TB-173, Pflege-Anker je genau einmal; kein Abschnitt 18")
    p(not any(l.startswith("| 17b |") for l in lies(DI).split("\n")), "Dialog-Index: 17b noch nicht")
    for f, m in sorted(CODE_E2.items()): p(md5f(f) == m, "E2-Ausgang: %s md5 %s" % (f, m[:12]))
    fund_ok()
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def register(datum, s0, beleg, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg)
    b = block(); p(b is not None and md5f(FA) == MD5F[FA], "Quelle md5 %s, Registerblock R107" % MD5F[FA])
    p(not any(l.startswith("## 67. ") for l in z) and z[-1] == "" and z[-2] != "", "67 noch nicht im Register; endet mit einer Leerzeile")
    einf = [(einfuege(z, m), m) for m in MARKEN]; p(all(i is not None for i, _ in einf) and len(set(i for i, _ in einf)) == len(MARKEN), "9 Einfuegestellen eindeutig")
    k = karte(); p(k is not None, "Karte TB-175 gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    (r, q), za, ze = b
    kopf = ("Reines Eintragen von Registertext, Bauart wie 66. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R107)“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.b (`%s`, seit `%s`) und die Übergabe 17.10.a (zweite Anfrage im selben Chat). Marken nach R107 (f). "
            "Karte des Betreibers (Auftrag TB-175, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-175.") % (FA, MD5F[FA], format(os.path.getsize(FA), ",").replace(",", " "), za, ze, s0, FQ, s0, k, datum)
    kette = ("**Kette:** Marken nach R107 (f): 62.3 (R102), Unterpunkt (a), ergänzt und berichtigt; 55.4 (R81), Unterpunkt (a); 66.1 (R106) und 64.1, Absatz „Abnahme nach R98 (d)“, Unterpunkt (b); "
             "56.3 (R86), Unterpunkte (c) und (e); 57.3 (R92), Unterpunkt (c); 16.4 und 16.8, Unterpunkt (d); 58.4 (R97), Unterpunkt (e). Ohne Marke: " + OHNE + ". "
             "Indexzeilen 48.20 (R52) und 54.3 (R76): sechzehn Fälle (R107 (f)). Voraussetzungen in (b) und (e) gemessen: 67.2 (a) (Teilmessung) und (b); Umstellung der Leser: nach der Frage zu D4 (BACKLOG Rang 1).")
    neu = ["", TITEL, "", kopf, "", "### 67.1 " + titel(r), "", "> " + r, "> " + q, "", kette, ""]
    neu += ["### 67.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-175), Zeilen wörtlich:" % beleg, ""] + ["    " + l for l in vb] + ["",
        ("(a) R107 (b), Voraussetzung (nur das Ob), gemessen durch Lesen am Stand `%s`: TB-169 3b führt t3_supertrend — `%s` %s: „%s“; `%s` %s (Tag des späten Symbols = frühester Einstieg, alle alten Einstiege am Tag oder später). "
         "Wachen eingeschaltet: Modus leer (%s), Ersetzung der Wachen nur in „wache1_aus“/„wachen_aus“ (%s). **Einschränkung:** verglichen wird mit Lauf B (Schranke am natürlichen Tag), nicht mit ausgeschalteter Schranke (%s), "
         "und Prüfung 8 (fremde Lesepfade, %s) prüft den 3b-Lauf nicht. **Teilmessung**, zur Kenntnis an den Verfahrensprüfer.") % (s0, FUND["abn"][0], fz("abn"), FUND["abn"][3][0].strip(), FUND["tle_tag"][0], fz("tle_tag"), fz("tle_modus"), fz("tle_wachen"), fz("tle_aus"), fz("tle_p8")), "",
        ("(b) R107 (e), Voraussetzung (nur das Wie), gemessen durch Lesen am Stand `%s`: die drei Leser aus R107 (e) — `%s` %s (`<bot>_positionen.csv`; 41.2 B6/B7, Quelle von B3), `%s` %s (41.3 C2, P95 t3_supertrend) und `%s` mit `research/mtm_drawdown/messung.py` (TB-24-Liste, Startkapital aus der Meta, %s) — "
         "und dazu `%s` (Rekonstruktion; Startkapital %s aus `es.STARTING_CAPITAL`) lasen ausgeführte Positionen; 41.2 B3, B6/B7 und 41.3 C2 rechneten nicht aus gefundenen Trades (B3 über `%s` %s aus `haltedauern_je_bot.csv`). Noch nicht umgestellt. "
         "Befund vor der Umstellung: über alle gefundenen Trades ergäbe D4 (`research/faltenplan_neun/test_faltenplan_neun.py`) für t3_supertrend P90 %s statt %s, Embargo %d statt %d; die übrigen acht Bots gleich (am Bau auf den abgelegten Listen gerechnet, der Test lief nicht). Frage an den Verfahrensprüfer.")
         % (s0, FUND["aus_lade"][0], fz("aus_lade"), FUND["emb"][0], fz("emb"), FUND["gl_meta"][0], fz("gl_meta"), FUND["wf"][0], fz("wf"), FUND["mg"][0], fz("mg"), D4["p90a"], D4["p90p"], D4["emba"], D4["embp"]), "",
        "(c) Zählung: R107 (a) nennt den sechzehnten Fall; die Indexzeilen an 48.20 (R52) und 54.3 (R76) stehen nur, wie R107 (f) sagt (Index, ohne Marke).", "",
        "(d) R56 (b): Anfrage und Antwort 17.10.b liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `docs/belege/TB-175/0a_md5.txt`)." % (s0, QU), ""]
    if probe: print("\n".join(neu)); ende()
    for i, m in sorted(einf, key=lambda x: -x[0]): z[i:i] = markenzeilen(m, datum)
    schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG).split("\n"); mz = {m[0]: [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s**" % m[3])] for m in MARKEN}
    json.dump({"marken": [[m[0], m[3], (mz[m[0]] or [0])[0]] for m in MARKEN], "abschnitt_67": r2.index(TITEL) + 1}, open(os.path.dirname(beleg) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(v) == 1 for v in mz.values()), "nachher: 9 Marken Z. %s; Abschnitt 67 Z. %d" % (sorted(sum(mz.values(), [])), r2.index(TITEL) + 1))
    p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "R107 mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)")
    weg = set(x for v in mz.values() for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; p(r3[:len(al)] == al and r3[len(al):] == neu, "append-only bis auf die neun Marken (je Leerzeile, Marke, Zeichengleich-Zeile)")
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]
    teil = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and "\n## 67. " in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1 and len(mk) == 9 and all(m[2] for m in mk), "Abschnitt 67 in genau einer Teildatei: T%s; 9 Marken mit Zeile" % teil); T = str(teil[0]) if teil else "?"
    z, k = stand_kopf(); rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–66" in z[k[0]], "Kopf genau einmal, nennt 0–66"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–66", "Abschnitte 0–67")
    i = [j for j, l in enumerate(z) if l.startswith("| 66 aus 17a |")]
    if p(len(i) == 1, "Zeile 66 genau einmal"): z.insert(i[0] + 1, "| 67 aus 17b | %s | R107 (67.1); 67.2 Voraussetzungen und Befunde | – |" % T)
    tab = ["---", "", "## 18. Die Marken aus Fable 17b (TB-175)", "", "Alle 9 Marken, die TB-175 nach R107 (f) gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-175/r_daten.json`.", "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, T) for o, kp, n in sorted(mk, key=lambda m: m[2])] + ["",
           "### Indexzeilen aus Fable 17b", "",
           "- **48.20 (R52):** Zählung → R107 (a) (67.1): sechzehnter Fall („Aussage über das Repo ohne Kennzeichnung, die nicht trifft (R76 (e))“); sechzehn Fälle (R107 (f)). Ohne Marke (R107 (f)). Der Index ist kein Registertext.",
           "- **54.3 (R76):** Massstab der Zählung (R76 (e)) → R107 (a) (67.1): sechzehnter Fall. Ohne Marke (R107 (f)). Der Index ist kein Registertext.", ""]
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 18. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 18"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-173 (")]
    if p(len(j) == 1, "Pflegezeile TB-173 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-173 (", "In TB-173 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-175 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-175 (`index`); 67 (R107) kommt zu T%s; neuer Abschnitt 18 (9 Marken, Indexzeilen 48.20 und 54.3)." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    json.dump({"17b": {"frage": lies(FQ).split("\n")[0].split(" — ", 1)[-1].strip(),
                       "entscheidung": "(a) einverstanden: Zeilenschnitt je Bot vor R44, „lies“ zu R102 (c); (b) einverstanden mit Voraussetzung (t3 geschlossen); (c) Modus-Wache im Erzeuger Pflicht; (d) Sammler ja, Kandidat mit Orders vor der Zulassung nein; (e) Leser auf gefundenen Trades, ausgeführte Positionen nur nach R45/R84 (e) oder R97 (b) (R107)",
                       "offen": "ja"}}, open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17b geschrieben: %s" % ziel)

if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["md5"]: md5cmd()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["gegenprobe"]: gegenprobe()
    elif a == ["nachher"]: nachher()
    elif a == ["nachher2"]: nachher2()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
