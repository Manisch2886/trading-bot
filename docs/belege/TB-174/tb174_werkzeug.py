#!/usr/bin/env python3
"""TB-174 Werkzeug (Anhang A): R106 (d) Weg 1 bei t3_supertrend - Voraussetzungen, Nachher-Pruefung (Handelscode unveraendert, Probe gruen), Kennung, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-174/"
TEST, TSHA = "research/tb24_haltedauern/test_t3_verdraengung.py", "492421a7fe0c6ffc63b0856d3c0e8ed13af8e1346c95db37e6e5007a6d3ab805"
CODE = { "strategies/t3_supertrend/backtest_trend.py": "896948ee3eca909cded1e68e1c471310", "strategies/t3_supertrend/indicators.py": "8452ad509b7ae9ad9b4ec656995f975c", "strategies/t3_supertrend/multi_symbol_optimise.py": "dc85993e8d42647dea2eb2593335aab8", "strategies/t3_supertrend/equity_simulation.py": "be665a734328d8a1d8231ff211a55a85", "strategies/t3_supertrend/live_params.py": "f28553e8deba39ea68329af10ecd19d6", "strategies/t3_supertrend/regime_filter.py": "b02087926d7d6b376a47b19115f1ca58", "shared/regimewache.py": "82cd933f9ba9b3a3c26ab23b87c1cb69", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/test_listen_erzeuger.py": "d77e73ed5ff7a737a22e53879ff72575", "research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "research/faltenplan_neun/faltenschranke_messung.py": "584d9ff959dab7428a97a945b091e118" }
R106D = "Vor dem Tag schliesst ihn deshalb Weg 1 (der Fall wird auf dem Test-Snapshot herbeigeführt"
RANG1, N = "| **1** | **TB-30b Mass-Reparatur**", 8
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "Handelscode/Erzeuger unveraendert: %s md5 %s" % (f, m[:12]))
def voraussetzung():
    code_gleich(); p(not os.path.exists(TEST), "Probe noch nicht im Repo: " + TEST)
    reg = lies(REG).split("\n"); r106 = [l for l in reg if l.startswith("> R106 — ")]
    p(len(r106) == 1 and R106D in r106[0] and "use_t3_exit" in r106[0], "Register: R106 genau einmal, (d) Weg 1 bei t3_supertrend im Wortlaut (nach TB-173)")
    p(sum(l.startswith("> R105 — ") for l in reg) == 1, "Register: R105 genau einmal")
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-174" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-174")
    k = kennungen(); p(max(k) in ("FI", "FJ"), "Journal: hoechste %s (FI am Bau-HEAD, FJ falls TB-173 eine Kennung setzt)" % max(k))
    ende()
def nachher():
    code_gleich()
    p(os.path.exists(TEST) and hashlib.sha256(open(TEST, "rb").read()).hexdigest() == TSHA, "Probe im Repo = Anhang (sha256 %s)" % TSHA[:12])
    e = lies(BEL + "e_probe.txt").rstrip("\n").split("\n") if os.path.exists(BEL + "e_probe.txt") else [""]
    p(e[-1] == "rc 0" and len(e) > 1 and e[-2] == "Ergebnis: %d von %d bestanden" % (N, N), "e_probe.txt endet mit 'Ergebnis: %d von %d bestanden' und 'rc 0'" % (N, N))
    p(not any(l.startswith("NEIN") for l in e) and sum(l.startswith("ja    ") for l in e) == N, "e_probe.txt: %d ja-Zeilen, keine NEIN-Zeile" % N)
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-174" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-174"):
        z[a[0]] = z[a[0]][:-2] + (" · **TB-174 (%s, Journal %s): R106 (d) Weg 1 bei `t3_supertrend`, Probe `%s` am Listen-Erzeuger, 8 von 8** "
            "(Fall nach R90 (g) über den Gleichstand auf dem Test-Snapshot herbeigeführt durch einen eingesetzten Kursabschnitt: Einstieg vor dem Tag, Position über den Tag offen, "
            "danach ein Kreuzen nach oben am Gleichstand T3 fast = T3 slow ohne Kreuzen nach unten; mit Schranke erscheint der zweite Einstieg; Gegenprobe 40.7: Schranke aus ⇒ Wache R87 (c) endet mit 2, "
            "Schranke und Wachen aus ⇒ der zweite Einstieg fehlt; Mutante mit der Schranke hinter der Zustandsmaschine an einer Kopie von `backtest_trend.py` ⇒ der zweite Einstieg fehlt; "
            "`use_t3_exit` im Lauf True, vom Erzeuger nicht übergeben); offen, an den Verfahrensprüfer: ob R106 (d) damit geschlossen und die Abnahme nach R98 (d) in 64.1 für t3_supertrend vollständig ist |") % (datum, kenn, TEST)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-174: " % neu), "Kopfzeile ## %s — TB-174: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif a == ["nachher"]: nachher()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
