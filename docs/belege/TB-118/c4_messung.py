#!/usr/bin/env python3
"""
TB-118 C4 - Sind BACKLOG_NACHTRAG_2026-09-18.md und JOURNAL_NACHTRAG_2026-09-18.md eingearbeitet? (DOKUMENTATIONS-
STANDARD 10: Nummer und Textkern im Ziel.) Der Nachtragswaechter kann beide nicht pruefen: sein RE_DATEINAME kennt
Dateinamen ohne Buchstaben nach dem Datum nicht, und er sucht nur unter nachtraege/. Deshalb diese Messung von Hand,
nach seiner Regel: je Nummer (Tabellenzeile | **X** | bzw. | ~~X~~ |) Nummer im Ziel UND Textkern (die ersten 40
Zeichen der zweiten Zelle ohne Auszeichnung) irgendwo im Ziel; je Journalblock Titel und erste Inhaltszeile im Journal.
Ziel Backlog: BACKLOG.md und jede dort genannte BACKLOG_<name>.md (wie der Waechter); Ziel Journal: JOURNAL.md.
Rein lesend. Aufruf aus der Repo-Wurzel.
"""
import os
import re

P = "docs/projektfuehrung"
RE_NENNUNG = re.compile(r"(?<![\w/])(BACKLOG_[\w.-]+\.md)\b")


def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def kern(s):
    s = re.sub(r"[*~`⭐⚠️⛔]", "", s).strip()
    return re.sub(r"\s+", " ", s)[:40]


def ziel_backlog():
    haupt = lies(os.path.join(P, "BACKLOG.md"))
    namen = sorted(n for n in set(RE_NENNUNG.findall(haupt)) if "_NACHTRAG_" not in n)
    dateien = ["BACKLOG.md"] + [n for n in namen if os.path.isfile(os.path.join(P, n))]
    return dateien, "\n".join(lies(os.path.join(P, d)) for d in dateien)


def main():
    dateien, ziel = ziel_backlog()
    ziel_kern = re.sub(r"\s+", " ", re.sub(r"[*~`⭐⚠️⛔]", "", ziel))
    print("# TB-118 C4 - Messung nach DOKUMENTATIONSSTANDARD 10")
    print("Ziel Backlog: " + ", ".join(dateien))
    fehlt = 0
    n = 0
    for z in lies(os.path.join(P, "BACKLOG_NACHTRAG_2026-09-18.md")).split("\n"):
        m = re.match(r"^\| (?:\*\*|~~)([^*~|]+)(?:\*\*|~~)[^|]*\| ([^|]*)\|", z)
        if not m:
            continue
        n += 1
        nummer, zelle = m.group(1).strip(), m.group(2)
        nr_da = re.search(r"^\| (?:\*\*|~~)" + re.escape(nummer) + r"(?:\*\*|~~)", ziel, re.M) is not None
        k = kern(zelle)
        kern_da = k in ziel_kern
        ok = nr_da and kern_da
        fehlt += 0 if ok else 1
        print("  %-4s %-8s Nummer %-4s Kern %-4s '%s'" % ("OK" if ok else "FEHLT", nummer, "ja" if nr_da else "NEIN",
                                                          "ja" if kern_da else "NEIN", k))
    print("Backlog-Nachtrag: %d Nummern, nicht angekommen %d" % (n, fehlt))
    journal = lies(os.path.join(P, "JOURNAL.md"))
    jf, jn = 0, 0
    text = lies(os.path.join(P, "JOURNAL_NACHTRAG_2026-09-18.md")).split("\n")
    for i, z in enumerate(text):
        m = re.match(r"^## Block ([A-Z]{2}) — (.+)$", z)
        if not m:
            continue
        jn += 1
        titel = m.group(2).strip()
        erste = next((t for t in text[i + 1:] if t.strip()), "")
        treffer = re.findall(r"^## ([A-Z]{1,2}) — " + re.escape(titel) + r"\s*$", journal, re.M)
        k = kern(erste)
        kern_da = k in re.sub(r"\s+", " ", re.sub(r"[*~`⭐⚠️⛔]", "", journal))
        ok = len(treffer) == 1 and kern_da
        jf += 0 if ok else 1
        print("  %-4s Block %s -> Journal %s, Titel '%s', Kern %s" % ("OK" if ok else "FEHLT", m.group(1),
              ",".join(treffer) or "-", titel[:50], "ja" if kern_da else "NEIN"))
    print("Journal-Nachtrag: %d Bloecke, nicht angekommen %d" % (jn, jf))
    return 0 if fehlt == 0 and jf == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
