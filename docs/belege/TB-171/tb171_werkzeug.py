#!/usr/bin/env python3
"""TB-171 Werkzeug (Anhang A): R105 (c) Weg 1 - Voraussetzungen, Nachher-Pruefung (Handelscode unveraendert, Probe gruen), Kennung, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, sys
REG, P = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-171/"
TEST, TSHA = "research/tb24_haltedauern/test_elliott_verdraengung.py", "59f6c90bde98a04da20fd52f314399a6e35443cacbfc3e2225d00eab3227d573"
CODE = { "strategies/elliott_wave/elliott_wave_counter.py": "75b26dd79237cd61c0cf04b45cf93098", "strategies/elliott_wave/multi_symbol_optimise.py": "bf11370b140d3e61488ad81599b45b37", "strategies/elliott_wave/backtest_elliott.py": "df5c314e9268bf5c51a5210113e27082", "strategies/elliott_wave/zigzag_indicator.py": "6e9a91ccc131937079b602be875fa0dd", "strategies/elliott_wave/equity_simulation.py": "a058c69a7a6c25e7239381bfab96fb05", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "b7fd099124b4801aecd68ba1e0fb1a05", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "571076168d56f9e809ef0595f53d6e7d", "strategies/elliott_wave_stocks/backtest_elliott.py": "f1979557a945822dfbe623e0d80ca531", "strategies/elliott_wave_stocks/zigzag_indicator.py": "407cd69fb5c2181c5316e008ea7b7d81", "strategies/elliott_wave_stocks/equity_simulation.py": "4ff525c50514fc25f43f50437148a7bd", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/test_listen_erzeuger.py": "d77e73ed5ff7a737a22e53879ff72575", "research/tb24_haltedauern/alle_bots.py": "7bb90ef438d5b3539cd72ac2e904524e", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "research/faltenplan_neun/faltenschranke_messung.py": "584d9ff959dab7428a97a945b091e118" }
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; ab TB-170 über `$TMPDIR`) |"
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
    reg = lies(REG).split("\n"); r105 = [l for l in reg if l.startswith("> R105 — ")]
    p(len(r105) == 1 and "Der Fall wird auf dem Test-Snapshot herbeigeführt" in r105[0], "Register: R105 genau einmal, (c) Weg 1 im Wortlaut")
    p(sum("Damit bleibt Weg 1" in l for l in reg) == 1, "Register 65 (c): Weg 2 traegt nicht, Weg 1 bleibt (genau einmal)")
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(RANG1E) and "R105 (c) Weg 1" in z[0], "BACKLOG Rang 1 genau einmal, Stand TB-170, nennt R105 (c) Weg 1")
    k = kennungen(); p(max(k) == "FG", "Journal: hoechste FG (naechste FH)")
    ende()
def nachher():
    code_gleich()
    p(os.path.exists(TEST) and hashlib.sha256(open(TEST, "rb").read()).hexdigest() == TSHA, "Probe im Repo = Anhang (sha256 %s)" % TSHA[:12])
    e = lies(BEL + "e_probe.txt").rstrip("\n").split("\n") if os.path.exists(BEL + "e_probe.txt") else [""]
    p(e[-1] == "rc 0" and len(e) > 1 and e[-2] == "Ergebnis: 16 von 16 bestanden", "e_probe.txt endet mit 'Ergebnis: 16 von 16 bestanden' und 'rc 0'")
    p(not any(l.startswith("NEIN") for l in e) and sum(l.startswith("ja    ") for l in e) == 16, "e_probe.txt: 16 ja-Zeilen, keine NEIN-Zeile")
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-170"):
        z[a[0]] = z[a[0]][:-2] + (" · **TB-171 (%s, Journal %s): R105 (c) Weg 1, Probe `%s` am Listen-Erzeuger, `elliott_wave` und `elliott_wave_stocks`, 16 von 16** "
            "(Fall nach R90 (g) auf dem Test-Snapshot herbeigeführt durch einen eingesetzten Kursabschnitt; mit Schranke steigt die Welle am Tag oder später ein; "
            "Gegenprobe 40.7: Schranke aus ⇒ Wache R87 (c) beisst an der Welle und endet mit 2, Schranke und Wachen aus ⇒ der spätere Einstieg fehlt; Mutante mit der Schranke hinter `traded.add` an einer Kopie des Counters ⇒ die Welle fehlt); offen, an den Verfahrensprüfer: ob R105 (c) damit "
            "für beide Bots geschlossen ist und ob „eine spätere Welle“ in R105 (c) den späteren Einstieg derselben Welle trägt (Schlüssel end_time, Register 65 (c)); R105 (d) t3_supertrend unberührt |") % (datum, kenn, TEST)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-171: " % neu), "Kopfzeile ## %s — TB-171: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
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
