# TB-161 Werkzeug (Anhang B des Auftrags): manifest, kennung, backlog, journal. Nur Standardbibliothek, Python 3.9.
# Liest nur; schreibt allein mit `backlog` (BACKLOG.md) und `journal` (JOURNAL.md), jeweils erst nach bestandener Probe; ein Anker muss genau einmal vorkommen, sonst wird nichts geschrieben.
import hashlib, json, os, re, sys
DATEN = "research/etf_trendfolge/daten"
BL = "docs/projektfuehrung/BACKLOG.md"
R4_ANFANG, R4_ALT, R4_NEU = '| **4** | **`S-B1` Multi-Asset-ETF-Trend** ', "| vorbereiten |", '| vorbereiten · Datenlauf TB-161: `docs/ERGEBNIS_TB-161_sb1_datenlauf.md`; UCITS-Paare (Register S-B1 10a) offen |'
K15_ANFANG, K15_NEU = "| **K15** | ", '**Vermerk TB-161: durch TB-41 erledigt, Paare offen** (Register `docs/VORREGISTRIERUNG_neuselektion.md` 16.9 (b), Commit `1bc2d57`; Proxy-Tabelle Register S-B1 10a.4 leer). '
JO, JO_ANKER = "docs/projektfuehrung/JOURNAL.md", "## Wiederkehrende Lehren"


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def schreib(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def manifest(aus):
    p = os.path.join(DATEN, "manifest.json")
    if not os.path.isfile(p):
        print("NEIN: %s fehlt" % p)
        return 3
    roh = open(p, "rb").read()
    m = json.loads(roh.decode("utf-8"))
    csv = sorted(x for x in os.listdir(DATEN) if x.endswith(".csv"))
    z = ["manifest.json · %d B · sha256 %s · erzeugt %s · auto_adjust %s · intervall %s" % (
        len(roh), hashlib.sha256(roh).hexdigest(), m.get("erzeugt"), m.get("auto_adjust"), m.get("intervall")),
         "Kursdateien (*.csv) in %s: %d · Eintraege im Manifest: %d · davon vorhanden: %d" % (
        DATEN, len(csv), len(m["dateien"]), sum(1 for e in m["dateien"] if e.get("vorhanden")))]
    for e in m["dateien"]:
        if not e.get("vorhanden"):
            z.append("%-5s FEHLT" % e["symbol"])
        else:
            z.append("%-5s %s bis %s · %d B · sha256 %s" % (e["symbol"], e["erstes_datum"], e["letztes_datum"], e["groesse"], e["sha256"]))
    schreib(aus, "\n".join(z) + "\n")
    print("\n".join(z))
    return 0


def backlog(probe):
    z = lies(BL).split("\n")
    r4 = [i for i, l in enumerate(z) if l.startswith(R4_ANFANG)]
    k15 = [i for i, l in enumerate(z) if l.startswith(K15_ANFANG)]
    c = [("Rang-4-Zeile genau einmal", len(r4) == 1),
         ("Rang-4-Zeile endet auf '%s'" % R4_ALT, len(r4) == 1 and z[r4[0]].endswith(R4_ALT)),
         ("K15-Zeile genau einmal", len(k15) == 1),
         ("Vermerke noch nicht da", R4_NEU not in "\n".join(z) and K15_NEU not in "\n".join(z))]
    for n, g in c:
        print("%s: %s" % (n, "ja" if g else "nein"))
    if not all(g for _, g in c):
        print("NEIN - nichts geschrieben")
        return 3
    if not probe:
        i, k = r4[0], k15[0]
        z[i] = z[i][:-len(R4_ALT)] + R4_NEU
        z[k] = K15_ANFANG + K15_NEU + z[k][len(K15_ANFANG):]
        schreib(BL, "\n".join(z))
    print("%s: Rang 4 Z. %d, K15 Z. %d" % ("probe" if probe else "geschrieben", r4[0] + 1, k15[0] + 1))
    return 0


def naechste():
    m = max(re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M))
    return m, (m[0] + chr(ord(m[1]) + 1)) if m[1] != "Z" else chr(ord(m[0]) + 1) + "A"


def kennung(aus):
    letzte, nx = naechste()
    t = "Kennung %s (naechste freie; hoechste vorhandene %s)" % (nx, letzte)
    schreib(aus, t + "\n")
    print(t)
    return 0


def journal(block, probe):
    b, t = lies(block).rstrip("\n").split("\n"), lies(JO)
    z, k = t.split("\n"), re.findall(r"^## ([A-Z]{2}) — TB-", t, re.M)
    letzte, KENNUNG = naechste()
    i = z.index(JO_ANKER) if z.count(JO_ANKER) == 1 else -1
    c = [("Block beginnt mit '## %s — TB-161: ' (naechste freie nach %s)" % (KENNUNG, letzte), b[0].startswith("## %s — TB-161: " % KENNUNG)),
         ("keine weitere '## '-Zeile im Block", sum(l.startswith("## ") for l in b) == 1),
         ("kein '---' im Block", "---" not in b),
         ("Kennung %s noch frei" % KENNUNG, KENNUNG not in k),
         ("Anker einmal", i >= 0),
         ("vor dem Anker '---' und Leerzeile", i >= 2 and z[i - 1] == "" and z[i - 2] == "---")]
    for n, g in c:
        print("%s: %s" % (n, "ja" if g else "nein"))
    if not all(g for _, g in c):
        print("NEIN - nichts geschrieben")
        return 64
    if not probe:
        z[i - 1:i - 1] = [""] + b + ["", "---"]
        schreib(JO, "\n".join(z))
    print("%s: Kennung %s, %d Zeilen Block" % ("probe" if probe else "eingefuegt", KENNUNG, len(b)))
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "manifest":
        sys.exit(manifest(a[1]))
    if len(a) == 2 and a[0] == "kennung":
        sys.exit(kennung(a[1]))
    if a in (["backlog"], ["backlog", "--probe"]):
        sys.exit(backlog(len(a) == 2))
    if len(a) in (2, 3) and a[0] == "journal" and a[2:] in ([], ["--probe"]):
        sys.exit(journal(a[1], len(a) == 3))
    print("Aufruf: manifest <beleg> | kennung <beleg> | backlog [--probe] | journal <block> [--probe]")
    sys.exit(2)
