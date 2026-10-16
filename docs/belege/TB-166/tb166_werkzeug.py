#!/usr/bin/env python3
"""TB-166 Werkzeug (Anhang D): Voraussetzungen, E-3a (20 Dateien ueber e3a_patch.py), Entwurf Tatsachennotiz nach 37.3, BACKLOG, Journal.
Stdlib, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | e3a [--probe] | notiz <E> | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, subprocess, sys
REG, BL, JO = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/BACKLOG.md", "docs/projektfuehrung/JOURNAL.md"
BEL = "docs/belege/TB-166/"
PUNKT = {"research/exposure_messung/bot_lauf.py": "\u2014", "research/faltenplan_neun/faltenschranke_messung.py": "\u2014", "strategies/elliott_wave/elliott_wave_counter.py": "11", "strategies/elliott_wave/equity_simulation.py": "11", "strategies/elliott_wave/multi_symbol_optimise.py": "11", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "11", "strategies/elliott_wave_stocks/equity_simulation.py": "11", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "11", "strategies/rsi2_crypto/backtest_rsi2.py": "9/11", "strategies/rsi2_crypto/equity_simulation.py": "11", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "9/11", "strategies/t3_supertrend/backtest_trend.py": "9/11", "strategies/t3_supertrend/equity_simulation.py": "11", "strategies/t3_supertrend/multi_symbol_optimise.py": "11", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "9/11", "strategies/turtle_soup_crypto/equity_simulation.py": "11", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "9/11", "strategies/volatility_breakout/backtest_breakout.py": "9/11", "strategies/volatility_breakout_crypto/backtest_breakout.py": "9/11", "strategies/volatility_breakout_crypto/equity_simulation.py": "11"}
VOR = {"research/exposure_messung/bot_lauf.py": "203d96203aa8e86a32610bbae40fcca911554f56a98b971f5cc8c475c766f50a", "research/faltenplan_neun/faltenschranke_messung.py": "049bb657ff9d4f81e8fcfda94559d4e40668bcca7a76bc07488dce80510cf91b", "strategies/elliott_wave/elliott_wave_counter.py": "8209e503b2f979f8900f49d458ff538009c2da94bb86240cce710f3870fb66fe", "strategies/elliott_wave/equity_simulation.py": "f45e92cdac5a4f03d3bd2f10165034d27b20603846e3072d02a7baf807cd127b", "strategies/elliott_wave/multi_symbol_optimise.py": "ba3f5fdcf42537d586144174401c6dbf1e93a1f62476083fb3184028c3b2ce6c", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "ed97e0f1bfbcb8c1fe5676b64f5d8a4cbdaf8be8448062616edfe20bdda62cbf", "strategies/elliott_wave_stocks/equity_simulation.py": "80ea2a331538bbe6270a97c03627c3393c56848bfff00d9a9d44024fc0768a21", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232", "strategies/rsi2_crypto/backtest_rsi2.py": "84930445e34940775f6fcc6715616eb77589fc960f988a19b26199f1393e1aca", "strategies/rsi2_crypto/equity_simulation.py": "1406de58ad920116d15a08384b88b78d37ee4944c925ff36fddedd123963e9ab", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "836b032a5962c7766e7ed00a75b90ded4155b769fce54a84fead3c4cd5f3b7fc", "strategies/t3_supertrend/backtest_trend.py": "7a764353d092e521cc24b80ae97193d624224b38a6a62a45394360fe50cb04bb", "strategies/t3_supertrend/equity_simulation.py": "0aed45b7e8d1a0386c381fc462f96233723ff9036e863e70741e2c224fc6ef1b", "strategies/t3_supertrend/multi_symbol_optimise.py": "e314d7bf7bb35854c9280a5b51362f2c8a6c33771a06188a14afee7c8ff39f14", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "0704c9a96898ede99e9cf2b153da33d0cb885bf16c89e642d8514f277e8a0089", "strategies/turtle_soup_crypto/equity_simulation.py": "f0638e8e92ae98683385ea3082fbc8c56db4bc74631001c147eef54f70d7ea03", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "0de39bf20bbbd3c0988b270262728a08cddc79a448fd0300c2f6b94998df50bb", "strategies/volatility_breakout/backtest_breakout.py": "3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76", "strategies/volatility_breakout_crypto/backtest_breakout.py": "3c7ccbe792ea5eb8dcbc76ae27079f4d7c47ca34bd3ad5edd332d4fdad3c403e", "strategies/volatility_breakout_crypto/equity_simulation.py": "1109438768c00e10710740775a30de8f3ac9f4309e24b3c54b13266d07df9fad"}
NACH = {"research/exposure_messung/bot_lauf.py": "95e4c567680b15889b1d80b6827dcbac6cdde8de639767eb7521546dc2876e71", "research/faltenplan_neun/faltenschranke_messung.py": "5383f4ed41a86b7bc0e3ba15c51adf96520bb1e54d58507f2503cab70301572f", "strategies/elliott_wave/elliott_wave_counter.py": "a57ab89413968aee9dbe5f256f44e0dde11131cb373b357de0da2d4c9a57a3a1", "strategies/elliott_wave/equity_simulation.py": "79d0a611bc8b4caed00db798e625f71e46b551af5e70a194323933d7b103ba00", "strategies/elliott_wave/multi_symbol_optimise.py": "d470a8b3d877dcd91b9e33ea40ba390e19200a4923140b54a532a561b5d9d209", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "6ce7966f07d3bb3348f0f6ab1d335a547707da088010c740a0427b5a312755e5", "strategies/elliott_wave_stocks/equity_simulation.py": "1ebde5ec7c067e73639c00495d481c09f130ebec23e51c3e90a3f79ea447dd5b", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "4f1ed9c0f2d149377be3568b016adec33d1f452eec43dd3aae63cbc102da1829", "strategies/rsi2_crypto/backtest_rsi2.py": "8de8a3fe35c31624d2a85495f9d73cf88a08d537fd0c22b3e889e55e09266691", "strategies/rsi2_crypto/equity_simulation.py": "30d3b2873883a6a2b2dc09e72d01bbd6b0db82551a745882481e1fec810c0b5a", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "484a964c0b80c0260d81e0a49195466f4f3d6aab1c0121a8abbd6cca840cc10b", "strategies/t3_supertrend/backtest_trend.py": "aade6aa8effc3fa9e095e8b57d6059ffb51d12091bbfa03dc937ab4f7c31797e", "strategies/t3_supertrend/equity_simulation.py": "2ffe378ff0b67efb63490f70a1bfae384044d096da40825788568e37db0c970a", "strategies/t3_supertrend/multi_symbol_optimise.py": "af458d97fd77d8057e292f500e8b9c7584d93bccc8d43274a0b541a6f35932cb", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "3f5faf8d3e00e9a92e6d61caa7684513343c99972693c497cf1cadf539e2ab3f", "strategies/turtle_soup_crypto/equity_simulation.py": "836f985229284f703a9a915434a60fa8b24579e63ddca9a303e8c3fd9c43237f", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "b7922129a00d2917d1d0750fb796f3e939e075c9f95cf5988b1849f8bb05b0f2", "strategies/volatility_breakout/backtest_breakout.py": "feb8875d484513b0289f563aee964387063b0cc413be612db43e2b3e8b0931fd", "strategies/volatility_breakout_crypto/backtest_breakout.py": "3743abd82984359328b125f9c3c221fe5d0e70ef5f2a2b066a6f40879df1b30c", "strategies/volatility_breakout_crypto/equity_simulation.py": "e16cf02297e2a6161307c4d398b3ac73db3db6fa249afa06185ead1b6e9bdc62"}
NEU = ["research/faltenplan_neun/test_handelbar_tag.py", "shared/test_schranke_signalpfad.py"]
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def lies(f): return open(f, encoding="utf-8").read()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def ende():
    n = sum(l.startswith("NEIN") for l in OUT); print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); print("rc %d" % (1 if n else 0)); sys.exit(1 if n else 0)
def voraussetzung():
    for f in sorted(VOR): p(os.path.exists(f) and sha(f) == VOR[f], "sha256 vorher %s" % f)
    r = lies(REG); z = r.split("\n")
    p(any(l.startswith("## 61. ") for l in z) and not any(l.startswith("## 62. ") for l in z), "Register endet mit 61, 62 fehlt")
    p(r.count("> R98 — Ergänzung zu R90 (c), (f) und (g)") == 1, "R98 genau einmal im Register")
    for f in NEU: p(not os.path.exists(f), "%s noch nicht da" % f)
    p("TB-166" not in lies(BL) and "TB-166" not in lies(JO), "TB-166 weder in BACKLOG noch in JOURNAL")
    ende()
def e3a(probe):
    r = subprocess.run([sys.executable, "-B", BEL + "e3a_patch.py", "."] + (["--probe"] if probe else []), capture_output=True, text=True)
    print(r.stdout.rstrip()); p(r.returncode == 0, "e3a_patch.py rc %d" % r.returncode)
    for l in r.stdout.split("\n"):
        m = re.match(r"(\S+)  vorher ([0-9a-f]{64})  nachher ([0-9a-f]{64})$", l)
        if m: p(VOR.get(m.group(1)) == m.group(2) and NACH.get(m.group(1)) == m.group(3), "%s vorher/nachher wie im Bau" % m.group(1))
    p(sum(1 for l in OUT if " vorher/nachher " in l) == len(VOR), "alle %d Dateien" % len(VOR))
    if not probe:
        for f in sorted(NACH): p(sha(f) == NACH[f], "auf der Platte nachher %s" % f)
    ende()
def notiz(e):
    if not re.fullmatch(r"[0-9a-f]{7}", e): sys.exit(2)
    z = ["**Hash-Übergänge nach 37.3** (R98 (c): eine Freigabe je Bauauftrag; Sperrlistenpunkte 9/11) — Entwurf, nicht eingetragen; volle Hashes (39.5):", "",
         "| Datei | Punkt | vorher | nachher | Commit | vollzieht |", "|---|---|---|---|---|---|"]
    for f in sorted(VOR): z.append("| `%s` | %s | `%s` | `%s` | `%s` | E-3a (R90 (c)–(e), R98 (a), (b)) |" % (f, PUNKT[f], VOR[f], sha(f), e))
    z += ["", "Neu (kein Vorher), Commit `%s`: " % e + ", ".join("`%s` `%s`" % (f, sha(f)) for f in NEU) + ".",
          "Abnahme: nach R98 (d) erst mit E-3b am Listen-Erzeuger (Probe nach R86 (d) mit Gegenprobe über die Wache nach R87 (c)); die Prüfung am Signalpfad in diesem Auftrag ist Handwerk daneben und ersetzt sie nicht.",
          "Abbild: ein neues Abbild unter neuem Namen schliesst den Befund (37.3; Bauart 50.3) — erst vor dem Tag, nicht in diesem Auftrag.",
          "Vorab gemessen (`docs/belege/TB-166/s0_vorab.txt`): 30 Symbole wechseln von einem Handelbar-Tag am oder nach dem Schnitt auf None, keines liegt vor dem Schnitt; `benchmark_drawdowns.json` (Punkt 4) bleibt unberührt (letzte Falte endet am Schnitt; `handelbar_ab` steht nicht in der Datei)."]
    print("\n".join(z))
def kennung():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k)
    n = h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"; print("Kennung %s (letzte %s)" % (n, h)); return n
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("| **1** | **TB-30b Mass-Reparatur**")]
    if p(len(a) == 1 and z[a[0]].endswith("mit der Messung nach R98 (b) |"), "BACKLOG Rang 1 genau einmal, endet mit 'R98 (b) |'"):
        z[a[0]] = z[a[0]][:-2] + " · E-3a (Schranke je Symbol, gemeinsame Tag-Rechnung `handelbar_ab`, Wache statt Filter; 20 Dateien, 18 auf der Sperrliste) gebaut mit TB-166 (%s, Journal %s); Abnahme nach R98 (d) mit E-3b, Tatsachennotiz 37.3 als Entwurf im Ergebnis |" % (datum, kenn)
    if not probe and not any(l.startswith("NEIN") for l in OUT): open(BL, "w", encoding="utf-8").write("\n".join(z))
    ende()
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); neu = kennung(); b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-166: " % neu), "Kopfzeile ## %s — TB-166: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---"); p("### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Teile vorhanden")
    if not probe and not any(l.startswith("NEIN") for l in OUT): z[i[0] - 2:i[0] - 2] = b + [""]; open(JO, "w", encoding="utf-8").write("\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif a == ["e3a"]: e3a(pr)
    elif len(a) == 2 and a[0] == "notiz": notiz(a[1])
    elif a == ["kennung"]: kennung()
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
