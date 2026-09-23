"""TB-92 Block D (Fable 23e): Zellenzahl je Bot und Summe - der Vollzug beruehrt sie nicht."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "research", "vorregistrierung"))
import registerdaten as rd
mess = rd._mess()
s = 0
for b in rd.BOTS:
    z = rd.zellen(b, mess); s += z
    print(f"{b:28s} {z}")
print(f"{'Summe':28s} {s}")
