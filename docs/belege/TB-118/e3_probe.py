#!/usr/bin/env python3
# TB-118 E3 - Probe: ablage_soll.py auf der rekonstruierten Ist-Liste (e3_ist_rekonstruiert.txt, 145 Pfade) gegen die
# Sofortliste 27b C3 Nr. 1-7. Die C3-Gruppen werden hier aus ihrem Wortlaut auf dieselbe Ist-Liste angewandt; jede
# Abweichung wird mit dem Grund aus ablage_soll.py genannt - nicht angepasst (Auftrag E3).
# Aufruf: python3 e3_probe.py <ausgabeordner von ablage_soll.py>
import os, re, sys
aus = sys.argv[1]
def lies(d):
    z = {}
    for zeile in open(os.path.join(aus, d), encoding="utf-8"):
        if zeile.startswith("#"):
            continue
        p, _, g = zeile.rstrip("\n").partition("\t")
        z[os.path.basename(p)] = (p, g)
    return z
ent, soll = lies("entfernen.txt"), lies("soll.txt")
ist = [l.strip() for l in open("docs/belege/TB-118/e3_ist_rekonstruiert.txt", encoding="utf-8") if l.strip() and not l.startswith("#")]
def schl(n):
    m = re.match(r"^FABLE_(?:ANFRAGE|ANTWORT|WOCHENRUECKMELDUNG|UEBERGABE)_2026-09-(\d\d)([a-z]?)", n)
    return (m.group(1), m.group(2)) if m else None
c3 = {}
for p in ist:
    n = os.path.basename(p)
    if n in ("REGISTER_KOPIE_2026-09-21.md", "REGISTER_KOPIE_2026-09-22.md", "REGISTER_KOPIE_2026-09-24.md"):
        c3[n] = 1
    elif n.startswith("REGISTER_KOPIE_2026-09-24_teil"):
        c3[n] = 2
    elif schl(n) and schl(n) <= ("25", "e") and "2026-09-25f" not in n:
        c3[n] = 3
    elif re.match(r"^(NACHTRAG_1_)?MAC_TB-", n):
        c3[n] = 4
    elif p.startswith("belege/"):
        c3[n] = 5
    elif n in ("UEBERGABE_2026-09-19.md", "UEBERGABE_2026-09-24.md"):
        c3[n] = 6
    elif n in ("STOFFSAMMLUNG_REGISTER_41_42.md", "AF-F0_BESTANDSAUFNAHME_2026-09-26.md",
               "BACKLOG_NACHTRAG_2026-09-18.md", "JOURNAL_NACHTRAG_2026-09-18.md"):
        c3[n] = 7
print("# TB-118 E3 - Probe ablage_soll.py gegen 27b C3 (Ist-Liste REKONSTRUIERT, 145 Pfade - siehe Kopf der Ist-Datei)")
print("Ist %d, entfernen (Skript) %d, Sofortliste C3 Nr. 1-7 auf derselben Liste %d" % (len(ist), len(ent), len(c3)))
for g in range(1, 8):
    teil = [n for n, k in c3.items() if k == g]
    print("  C3 Nr. %d: %3d Dateien, davon im Skript-entfernen %3d" % (g, len(teil), sum(1 for n in teil if n in ent)))
nur_c3 = sorted(n for n in c3 if n not in ent)
nur_skript = sorted(n for n in ent if n not in c3)
print("\n## (a) in C3, vom Skript NICHT entfernt: %d" % len(nur_c3))
for n in nur_c3:
    print("  C3 Nr. %d  %-60s Skript: bleibt - %s" % (c3[n], n, soll.get(n, ("", "?"))[1]))
print("\n## (b) vom Skript entfernt, in C3 NICHT: %d" % len(nur_skript))
for n in nur_skript:
    print("  %-62s Skript: %s" % (n, ent[n][1]))
print("\nErgebnis: %d von %d C3-Dateien entfernt das Skript; %d Abweichungen (a), %d Abweichungen (b)."
      % (len(c3) - len(nur_c3), len(c3), len(nur_c3), len(nur_skript)))
