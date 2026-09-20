import re, pathlib
def norm(s): return re.sub(r"\s+"," ",re.sub(r"(?m)^> ?","",s))
Jraw = pathlib.Path("docs/projektfuehrung/JOURNAL.md").read_text(encoding="utf-8")
J = norm(Jraw)
N = pathlib.Path("docs/projektfuehrung/nachtraege")
faelle = [
 ("JOURNAL_NACHTRAG_2026-09-19c.md", ["TB-55"],  ["die Sitzung, deren Ergebnis ein Nichthandeln ist", "Der Zug ist nicht wiederholbar; der Abbruch ist es"]),
 ("JOURNAL_NACHTRAG_2026-09-19d.md", ["TB-55"],  ["der Eingabezustand existiert", "1 Commit, 4 Trees, 1 Blob"]),
 ("JOURNAL_NACHTRAG_2026-09-19e.md", ["TB-55b","TB-54"], ["der Snapshot steht im Register", "acht Nachträge, eine Rückfrage"]),
 ("JOURNAL_NACHTRAG_2026-09-19f.md", [],        ["der Resolver erreicht die Selektionsseite", "Der Engpass war eine Datei, nicht 90 Module", "Codeherkunft und Lock", "Abschnitte 19 und 20"]),
 ("JOURNAL_NACHTRAG_2026-09-19g.md", ["TB-59"],  ["Sichern ist keine Abgabe, sondern ein Schritt", "die Backlog-Einarbeitung"]),
 ("JOURNAL_NACHTRAG_2026-09-20a.md", ["TB-60"],  ["Verschieben ist beweisbarer als Behalten", "das Backlog-Archiv"]),
 ("JOURNAL_NACHTRAG_2026-09-20b.md", ["TB-61","TB-62"], ["ZIP wird überall abgeschafft", "fünf Messfehler derselben Familie"]),
 ("JOURNAL_NACHTRAG_2026-09-20c.md", ["TB-61"],  ["Der Krypto-Benchmark ist bis 2021 leer", "drei Befunde, die keiner bestellt hat"]),
 ("JOURNAL_NACHTRAG_2026-09-20d.md", ["TB-65"],  ["Der Faktor ist nicht die Nachricht", "welche Schranke für den Benchmark gilt"]),
 ("JOURNAL_NACHTRAG_2026-09-20e.md", ["TB-62"],  ["das Ende der ZIP-Pflicht", "die Nachträge (m) und (v)"]),
 ("JOURNAL_NACHTRAG_2026-09-20f.md", ["TB-66"],  ["der Benchmark wird tagesgenau", "Ein Platzhalter im Register ist ehrlicher"]),
]
def kopfzeilen(pat):
    return [m for m in re.finditer(r"^## .*$", Jraw, re.M) if pat in m.group(0)]
print("| Nachtrag | Titel-TB | Muster A: TB-Nr in `## `-Kopfzeile | Muster B: charakteristischer Satz (wörtlich, Treffer im ganzen Journal) | Urteil |")
print("|---|---|---|---|---|")
for name, tbs, saetze in faelle:
    txt = norm((N/name).read_text(encoding="utf-8"))
    assert all(s in txt for s in saetze), (name, [s for s in saetze if s not in txt])
    a = []
    for tb in tbs:
        ks = kopfzeilen(tb+":") + kopfzeilen(tb+" ")
        ks = list({k.group(0):k for k in ks}.values())
        a.append(f"`{tb}`: {len(ks)} ({', '.join(k.group(0)[3:5] for k in ks) or '—'})")
    b = []
    for s in saetze:
        n = J.count(s)
        b.append("„" + s[:38] + "…“: " + str(n))
    hits_a = sum(len(kopfzeilen(tb+":"))+len(kopfzeilen(tb+" ")) for tb in tbs)
    hits_b = sum(J.count(s) for s in saetze)
    if hits_b: u = "EINGEARBEITET (B trifft" + (", A trifft" if hits_a else "") + ")"
    elif tbs and hits_a==0: u = "OFFEN (A 0, B 0, Kennung vorhanden)"
    elif tbs: u = "A trifft, B nicht – prüfen"
    else: u = "OFFEN – aber ohne TB im Titel; B = 0 ⇒ A2? siehe Text"
    print(f"| `{name[16:-3]}` | {', '.join(tbs) or '— (keine)'} | {'; '.join(a) or 'nicht anwendbar'} | {'; '.join(b)} | {u} |")
