# -*- coding: utf-8 -*-
"""TB-125 B2/B3: Nachweis gegen den Auftragstext.

B3: Liest je Einfuegung den Text erneut aus dem Auftrag (eigener Parser, nicht
der von einfuegen.py) und prueft, dass er in der Zieldatei genau einmal als
zusammenhaengender Block auf Zeilengrenzen vorkommt. Bytevergleich, keine
Normalisierung. -> b3_vergleich.txt

B2: git diff --numstat je Datei, Soll aus der Ausgangsfassung (HEAD) gezaehlt,
und Abgleich der entfernten Zeilen (git diff -U0) gegen die Zeilen, die die
Ersetzungen treffen. -> b2_numstat.txt

Aufruf (Repo-Wurzel): trading-env/bin/python3 docs/belege/TB-125/b3_vergleich.py
"""
import io
import subprocess

AUFTRAG = "docs/auftraege/MAC_TB-125_regelwerk_nachtrag_29_30_09.md"
A = "docs/projektfuehrung/ARBEITSWEISE.md"
U = "docs/projektfuehrung/UMZUG.md"
B = "docs/projektfuehrung/BACKLOG.md"
# Zieldatei je Einfuegung (E24: ARBEITSWEISE, siehe einfuegen.py DATEI_KORREKTUR)
ZIEL = {}
for n in range(1, 7):
    ZIEL[n] = U
for n in range(7, 22):
    ZIEL[n] = A
ZIEL[22] = B
ZIEL[23] = B
ZIEL[24] = A
ERSETZUNGEN = {U: [4, 5], A: [10, 11, 12, 13, 24], B: []}


def lies(pfad):
    with io.open(pfad, "r", encoding="utf-8", newline="") as f:
        return f.read()


def git(*args):
    return subprocess.check_output(("git",) + args).decode("utf-8")


def auftrag_bloecke():
    zeilen = lies(AUFTRAG).split("\n")
    bloecke, anker = {}, {}
    n = None
    zaun = None
    puffer = None
    for z in zeilen:
        if z.startswith("#### E") and zaun is None:
            n = int(z[6:].split(" ")[0])
            continue
        if n is None:
            continue
        if zaun is None and z.startswith("Anker") and n not in anker:
            anker[n] = z
        if zaun is None and n not in bloecke and z in ("```", "~~~"):
            zaun, puffer = z, []
            continue
        if zaun is not None:
            if z == zaun:
                bloecke[n] = puffer
                zaun = None
            else:
                puffer.append(z)
    return bloecke, anker


def backtick_spannen(zeile):
    teile = zeile.split("Art: ")[0].split("`")
    return [teile[i] for i in range(1, len(teile), 2)]


def b3(bloecke):
    aus = ["TB-125 B3 — Zeichengleichheit (Bytevergleich, keine Normalisierung)",
           "Je Einfügung: Text aus dem Auftrag (Codeblock unter „#### E<n>“, ohne Zäune),",
           "gesucht als zusammenhängender Block auf Zeilengrenzen in der Zieldatei. Soll: genau 1.",
           ""]
    alle = True
    for n in range(1, 25):
        text = "\n".join(bloecke[n]) + "\n"
        roh = lies(ZIEL[n])
        hay = "\n" + roh
        treffer = hay.count("\n" + text)
        if treffer == 1:
            urteil = "gleich"
        else:
            alle = False
            # erste abweichende Stelle ab der ersten Zeile des Texts
            erste = bloecke[n][0]
            pos = roh.find(erste)
            if pos < 0:
                urteil = "abweichend (erste Zeile fehlt)"
            else:
                k = 0
                while k < len(text) and pos + k < len(roh) and roh[pos + k] == text[k]:
                    k += 1
                urteil = "abweichend bei Zeichen %d des Texts (Treffer %d)" % (k, treffer)
        aus.append("E%d · %s · %d Zeilen · %d Bytes · Treffer %d · %s"
                   % (n, ZIEL[n], len(bloecke[n]), len(text.encode("utf-8")), treffer, urteil))
    aus.append("")
    aus.append("Gesamt: " + ("24/24 gleich" if alle else "NICHT alle gleich"))
    return aus


def b2(bloecke, anker):
    aus = ["TB-125 B2 — git diff --numstat gegen HEAD (Ausgangsfassung) und Herkunft der entfernten Zeilen", ""]
    aus.append(git("diff", "--numstat", "HEAD", "--", A, U, B).rstrip("\n"))
    aus.append("")
    ok = True
    for pfad in (U, A, B):
        alt = git("show", "HEAD:" + pfad).split("\n")
        soll = []
        for n in ERSETZUNGEN[pfad]:
            sp = backtick_spannen(anker[n])
            if n == 5:
                a = [i for i, z in enumerate(alt) if sp[0] in z]
                e = [i for i, z in enumerate(alt) if sp[1] in z]
                soll.extend(alt[a[0]:e[0] + 1])
                aus.append("%s E5: Anfangsanker Zeile %d, Endanker Zeile %d -> Soll %d Zeilen (einschliesslich)"
                           % (pfad, a[0] + 1, e[0] + 1, e[0] - a[0] + 1))
            else:
                t = [z for z in alt if sp[0] in z]
                soll.extend(t)
        diff = git("diff", "-U0", "HEAD", "--", pfad).split("\n")
        ist = [z[1:] for z in diff if z.startswith("-") and not z.startswith("--- a/")]
        gleich = sorted(ist) == sorted(soll)
        ok = ok and gleich
        aus.append("%s: entfernt Soll %d (aus E%s), Ist %d, Zeilen identisch: %s"
                   % (pfad, len(soll), ",".join(str(n) for n in ERSETZUNGEN[pfad]) or "–",
                      len(ist), "ja" if gleich else "NEIN"))
    aus.append("")
    aus.append("Gesamt: " + ("entfernte Zeilen stammen nur aus den Ersetzungen" if ok else "ABWEICHUNG"))
    return aus


def main():
    bloecke, anker = auftrag_bloecke()
    assert sorted(bloecke) == list(range(1, 25)), sorted(bloecke)
    r3 = "\n".join(b3(bloecke)) + "\n"
    r2 = "\n".join(b2(bloecke, anker)) + "\n"
    io.open("docs/belege/TB-125/b3_vergleich.txt", "w", encoding="utf-8").write(r3)
    io.open("docs/belege/TB-125/b2_numstat.txt", "w", encoding="utf-8").write(r2)
    print(r2)
    print(r3)


if __name__ == "__main__":
    main()
