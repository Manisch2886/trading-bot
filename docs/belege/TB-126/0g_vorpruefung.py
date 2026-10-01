#!/usr/bin/env python3
"""TB-126 0g - Vorpruefungen vor jedem Registereintrag, alles am Commit S0 (git show).

Aufruf aus der Repo-Wurzel:  trading-env/bin/python3 docs/belege/TB-126/0g_vorpruefung.py <S0>
1. Anhang A, Daten-Block: jeder Anker genau 1-mal im Register, Ankerzeile und Einfuegestelle beginnen wie angegeben
   (je Marke einzeln; Abweichung einzelner Marken = Marke auslassen, Abbruch erst ab mehr als fuenf).
2./3. Grenzen der Entwuerfe TB-122 und TB-124.
4. Docstring von auswertung.py: Grenzzeilen je 1, Zaehlungen im Zitatbereich.
rc 0 = alles wie angegeben; rc 1 = Abbruch (Nr. 2-4 abweichend oder mehr als fuenf Marken); rc 3 = 1-5 Marken weichen ab.
"""
import json, re, subprocess, sys

S0 = sys.argv[1]
def show(p): return subprocess.run(["git", "show", f"{S0}:{p}"], capture_output=True, text=True, check=True).stdout

fehler, marken_ab = [], []
auftrag = show("docs/auftraege/MAC_TB-126_register_e2.md")
daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
reg = show("docs/VORREGISTRIERUNG_neuselektion.md")
L = reg.split("\n")

print(f"# TB-126 0g Vorpruefung am Commit {S0}")
print("## 1. Anhang A, Daten-Block: Anker und Einfuegestellen")
for m in daten["marken"]:
    n = reg.count(m["anker"])
    ok_a = L[m["ankerzeile"] - 1].startswith(m["anker"])
    ok_n = L[m["nach"] - 1].startswith(m["anfang40"])
    gut = n == 1 and ok_a and ok_n
    if not gut: marken_ab.append(m["nr"])
    print(f"Nr {m['nr']:2d} R{m['R'] or '-'}: Anker {n}x, Ankerzeile {m['ankerzeile']} {'ja' if ok_a else 'NEIN'}, "
          f"nach Z. {m['nach']} {'ja' if ok_n else 'NEIN'} -> {'gut' if gut else 'ABWEICHUNG'}")
print(f"Marken geprueft: {len(daten['marken'])}, abweichend: {len(marken_ab)} {marken_ab}")
r54 = daten["r54_unter_48_16"]["anker"]
print(f"R54-Anker unter 48.16 im Register vor dem Eintrag: {reg.count(r54)} (Soll 0)")
if reg.count(r54) != 0: fehler.append("R54-Anker schon im Register")
if len(marken_ab) > 5: fehler.append("mehr als fuenf Marken weichen ab")

def grenzen(pfad, a, b, anfang, ende, nr):
    z = show(pfad).split("\n")
    ok1, ok2 = z[a - 1].startswith(anfang), z[b - 1].endswith(ende)
    print(f"## {nr}. {pfad} Z. {a} beginnt mit {anfang!r}: {'ja' if ok1 else 'NEIN'}; Z. {b} endet mit {ende!r}: {'ja' if ok2 else 'NEIN'}")
    if not (ok1 and ok2): fehler.append(f"Nr {nr}: Grenzen weichen ab")
grenzen("docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md", 235, 275,
        "> **Vollzug TB-30b Posten 3 (11.3) in TB-122", "TB-122 Befund F1).", 2)
grenzen("docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md", 289, 323,
        "> **Vollzug TB-30b Posten 3 (11.3), Teil Scanbeginn", "nie früher, nicht später.", 3)

print("## 4. Docstring research/vorregistrierung/auswertung.py")
A = show("research/vorregistrierung/auswertung.py").split("\n")
ia = [i for i, s in enumerate(A) if "DIE ROHERGEBNISSE - DER VERTRAG" in s]
ib = [i for i, s in enumerate(A) if "ZWEI DEFINITIONEN, DIE SONST SCHWEIGEND AUSEINANDERLAUFEN" in s]
print(f"Zeile 'DIE ROHERGEBNISSE - DER VERTRAG': {len(ia)}x {[i + 1 for i in ia]}; "
      f"Zeile 'ZWEI DEFINITIONEN ...': {len(ib)}x {[i + 1 for i in ib]} (Soll je 1)")
if len(ia) != 1 or len(ib) != 1:
    fehler.append("Nr 4: Grenzzeilen nicht je 1")
else:
    za = ia[0]; zb = ib[0] - 1
    while A[zb].strip() == "": zb -= 1
    bereich = "\n".join(A[za:zb + 1])
    print(f"Zitatbereich: Z. {za + 1}-{zb + 1} (Erwartung des steuernden Chats 36-67, kein Soll)")
    z = {"<markt>.csv": bereich.count("<markt>.csv")}
    for w in ("zellenbericht", "symbole_je_falte", "audit"):
        z[w] = bereich.lower().count(w)
    print("Zaehlungen:", z, "(Soll <markt>.csv 1, sonst je 0)")
    if z["<markt>.csv"] != 1 or any(z[w] for w in ("zellenbericht", "symbole_je_falte", "audit")):
        fehler.append("Nr 4: Zaehlungen weichen ab")

if fehler:
    print("ABBRUCH:", fehler); sys.exit(1)
if marken_ab:
    print(f"rc 3: {len(marken_ab)} Marke(n) weichen ab, werden nicht gesetzt: {marken_ab}"); sys.exit(3)
print("rc 0: alles wie angegeben")
