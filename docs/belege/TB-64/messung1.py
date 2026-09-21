#!/usr/bin/env python3
"""TB-64, Schritt 1 - messen, was heute offen ist. Rein lesend.

Fuer jede Nachtragsdatei unter docs/projektfuehrung/nachtraege/ und
_eingearbeitet/: welche ihrer Nummern sind im Ziel angekommen?

Kennungen eines BACKLOG_NACHTRAG (Auftrag, Abschnitt 1):
  K-Nummer      ^\| \*\*(K\d[a-z])\*\*                 KEIN schliessender Balken
  Block         ^#{2,3} (2[a-z]+)\b  (Nachtrag)  /  ^## (2[a-z]+)\b  (Ziel)
  Kettenzeile   ^\| (\*\*|~~)?(\d+,\d+[a-z]?)(\*\*|~~)?
  dazu, weil (q), (r), (u) sonst keine Kennung haetten:
  Punkt         ^\| \*\*([A-Z]{1,3}(-[A-Z])?\d+(\.\d+)?[a-z]?)\*\*   (T46.1a, B1, F0, AF1)
                ^#{2,3} ([A-Z]{2,3}\d+) —                          (KG5, RT3)

Angekommen heisst NICHT nur "die Nummer steht im Ziel": (m) hat gezeigt, dass
eine Nummer an ANDEREN Inhalt vergeben sein kann. Deshalb zweistufig:
  1. Zeile derselben Form mit derselben Nummer im Ziel, deren Text den KERN
     des Nachtragstexts enthaelt (erste 40 Zeichen nach Entfernen von
     Markdown-Auszeichnung und Whitespace)                    -> "Zeile"
  2. sonst: der Kern steht in irgendeiner Zielzeile (Nummer bei der
     Einarbeitung geaendert)                                   -> "anderswo"
  3. sonst: eine Zielzeile nennt die Nummer als Wort zusammen mit
     "vorgeschlagen"/"vergeben" (Vergabevermerk, TB-59-Form)   -> "Vermerk"
  4. sonst                                                     -> FEHLT
Ziel fuer K/Block/Kette: BACKLOG.md + BACKLOG_ARCHIV.md; fuer Punkt zusaetzlich
JOURNAL.md (die T-Zeilen aus (m) stehen seit TB-67 im Journal).

JOURNAL_NACHTRAG: Dateiname in einer *Quelle:-Zeile von JOURNAL.md
(Vergleich ueber den Dateinamen; *Messprotokoll:-Zeilen zaehlen nicht).

Kein sort -u. Doppelbelegung = Nummer mehr als einmal im Ziel; bei
Kettenzeilen zaehlen Zeilen mit "alter Wortlaut" oder "Vermerk" in der
Nummernzelle nicht mit (DOKUMENTATIONSSTANDARD Regel 4: die abgeloeste
Fassung bleibt darunter stehen).
"""
import os
import re
import sys
import time

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PF = os.path.join(WURZEL, "docs", "projektfuehrung")
NACHTRAEGE = os.path.join(PF, "nachtraege")
EINGEARBEITET = os.path.join(NACHTRAEGE, "_eingearbeitet")
BACKLOG = os.path.join(PF, "BACKLOG.md")
ARCHIV = os.path.join(PF, "BACKLOG_ARCHIV.md")
JOURNAL = os.path.join(PF, "JOURNAL.md")

RE_K = re.compile(r"^\| \*\*(K\d[a-z])\*\*")
RE_BLOCK_N = re.compile(r"^#{2,3} (2[a-z]+)\b")
RE_BLOCK_Z = re.compile(r"^## (2[a-z]+)\b")
RE_KETTE = re.compile(r"^\| (?:\*\*|~~)?(\d+,\d+[a-z]?)(?:\*\*|~~)?")
RE_PUNKT_ROW = re.compile(r"^\| \*\*([A-Z]{1,3}(?:-[A-Z])?\d+(?:\.\d+)?[a-z]?)\*\*")
RE_PUNKT_H_N = re.compile(r"^#{2,3} ([A-Z]{2,3}\d+) — ")
RE_PUNKT_H_Z = re.compile(r"^#{2,4} ([A-Z]{2,3}\d+) — ")
KERN = 40


def lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read().splitlines()


def norm(text):
    t = re.sub(r"[*_~`]", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def inhalt_nach_nummer(zeile):
    """Text nach der Nummernzelle einer Tabellenzeile (Vergabevermerk in der
    Nummernzelle wird uebersprungen), bzw. nach 'X — ' einer Ueberschrift."""
    if zeile.startswith("|"):
        rest = zeile[1:]
        pos = rest.find(" | ")
        return rest[pos + 3:] if pos >= 0 else rest
    m = re.match(r"^#+ \S+\s*[—-]\s*(.*)$", zeile)
    return m.group(1) if m else zeile


def kern(zeile):
    t = norm(inhalt_nach_nummer(zeile))
    t = re.sub(r"^[^\w(„\"]+", "", t)  # Emoji und Pfeile am Anfang weg
    return t[:KERN]


def kennungen(zeilen):
    """[(art, nummer, kern)] eines Backlog-Nachtrags, in Dateireihenfolge."""
    out = []
    for z in zeilen:
        m = RE_K.match(z)
        if m:
            out.append(("K", m.group(1), kern(z)))
            continue
        m = RE_BLOCK_N.match(z)
        if m:
            out.append(("Block", m.group(1), kern(z)))
            continue
        m = RE_KETTE.match(z)
        if m:
            out.append(("Kette", m.group(1), kern(z)))
            continue
        m = RE_PUNKT_ROW.match(z)
        if m:
            out.append(("Punkt", m.group(1), kern(z)))
            continue
        m = RE_PUNKT_H_N.match(z)
        if m:
            out.append(("Punkt", m.group(1), kern(z)))
    return out


def zielzeilen_mit_nummer(art, nummer, ziel):
    """Alle Zielzeilen derselben Form mit dieser Nummer (ohne sort -u)."""
    treffer = []
    for z in ziel:
        if art == "K":
            m = RE_K.match(z)
        elif art == "Block":
            m = RE_BLOCK_Z.match(z)
        elif art == "Kette":
            m = RE_KETTE.match(z)
        else:
            m = RE_PUNKT_ROW.match(z) or RE_PUNKT_H_Z.match(z)
        if m and m.group(1) == nummer:
            treffer.append(z)
    return treffer


def vergabevermerk(nummer, ziel):
    muster = re.compile(r"(?<![\w,])" + re.escape(nummer) + r"(?![\w,])")
    for z in ziel:
        if ("vorgeschlagen" in z or "vergeben" in z) and muster.search(z):
            return z
    return None


def pruefe_kennung(art, nummer, k, ziel_backlog, ziel_punkt):
    ziel = ziel_punkt if art == "Punkt" else ziel_backlog
    gleiche = zielzeilen_mit_nummer(art, nummer, ziel)
    if k and any(k in norm(z) for z in gleiche):
        return ("Zeile", f"{len(gleiche)} Zielzeile(n), Kern bestaetigt")
    if k:
        for z in ziel:
            if k in norm(z):
                return ("anderswo", "Kern in Zielzeile: " + z[:70])
    v = vergabevermerk(nummer, ziel)
    if v:
        return ("Vermerk", v[:90])
    if gleiche:
        return ("FEHLT", f"Nummer im Ziel vergeben ({len(gleiche)}x), Kern nicht gefunden: '{k}'")
    return ("FEHLT", f"Nummer nicht im Ziel, Kern nicht gefunden: '{k}'")


def doppelbelegungen(ziel):
    zaehl = {}
    for z in ziel:
        for art, rx in (("K", RE_K), ("Block", RE_BLOCK_Z), ("Kette", RE_KETTE)):
            m = rx.match(z)
            if not m:
                continue
            if art == "Kette":
                zelle = z[1:].split(" | ", 1)[0]
                if "alter Wortlaut" in zelle or "Vermerk" in zelle:
                    continue
            zaehl.setdefault((art, m.group(1)), 0)
            zaehl[(art, m.group(1))] += 1
    return sorted((a, n, c) for (a, n), c in zaehl.items() if c > 1)


def main():
    ziel_backlog = lies(BACKLOG) + lies(ARCHIV)
    journal = lies(JOURNAL)
    ziel_punkt = ziel_backlog + journal
    print(f"Stand {time.strftime('%Y-%m-%d %H:%M:%S %z')}")
    print(f"Ziel: BACKLOG.md {len(lies(BACKLOG))} + BACKLOG_ARCHIV.md {len(lies(ARCHIV))} Zeilen; "
          f"JOURNAL.md {len(journal)} Zeilen, *Quelle:-Zeilen "
          f"{sum(1 for z in journal if z.startswith('*Quelle:'))}")
    print(f"Doppelbelegung im Ziel (ohne sort -u): {doppelbelegungen(ziel_backlog) or 'keine'}")
    print()
    for ordner, titel in ((NACHTRAEGE, "OFFEN (Hauptverzeichnis)"), (EINGEARBEITET, "_eingearbeitet/")):
        print("=" * 78)
        print(titel)
        print("=" * 78)
        for name in sorted(os.listdir(ordner)):
            pfad = os.path.join(ordner, name)
            if not os.path.isfile(pfad) or not name.endswith(".md"):
                continue
            alter = (time.time() - os.path.getmtime(pfad)) / 86400.0
            if name.startswith("BACKLOG_NACHTRAG_"):
                ks = kennungen(lies(pfad))
                if not ks:
                    print(f"{name}  Alter {alter:.1f} d  NICHT PRUEFBAR (0 Kennungen)")
                    continue
                erg = [(a, n, k) + pruefe_kennung(a, n, k, ziel_backlog, ziel_punkt) for a, n, k in ks]
                fehlt = [f"{a} {n}" for a, n, _, s, _ in erg if s == "FEHLT"]
                print(f"{name}  Alter {alter:.1f} d  Kennungen {len(erg)}  "
                      f"angekommen {len(erg) - len(fehlt)}  FEHLT {len(fehlt)}"
                      + (f"  -> {', '.join(fehlt)}" if fehlt else ""))
                for a, n, k, s, x in erg:
                    print(f"    {a:5} {n:7} {s:8} {x}")
            elif name.startswith("JOURNAL_NACHTRAG_"):
                t = sum(1 for z in journal if z.startswith("*Quelle:") and name in z)
                print(f"{name}  Alter {alter:.1f} d  *Quelle:-Zeilen im Journal: {t}"
                      + ("" if t else "  FEHLT"))
            else:
                print(f"{name}  Alter {alter:.1f} d  UNBEKANNTE ART")
        print()


if __name__ == "__main__":
    sys.exit(main())
