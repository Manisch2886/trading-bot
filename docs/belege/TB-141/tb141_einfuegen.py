#!/usr/bin/env python3
"""TB-141: Einfügungen E1–E26, Prüfungen S1–S4, Journalblock und J1 — alles aus dem Auftrag gelesen.

Liest je Einfügung Zieldatei, Anker, Art, Form und Text (erster Codeblock ohne Zäune) aus dem
Auftrag, nicht aus dem Gedächtnis; Überschriften zählen nur ausserhalb von Codeblöcken.
Anker in doppelten Backticks (`` x ``) werden als Codespanne gelesen.
Jede Belegdatei wird ganz neu geschrieben, trägt eine Kopfzeile und wird zurückgelesen
(kein Reststück). Aufruf aus der Repo-Wurzel mit trading-env/bin/python3 -B:

  tb141_einfuegen.py probe                        nur lesen        -> a_probe.txt
  tb141_einfuegen.py einfuegen                    E1–E26           -> a_einfuegungen.txt
  tb141_einfuegen.py vergleich                    C3               -> c3_vergleich.txt
  tb141_einfuegen.py numstat <von> <bis>          C2 (git diff)    -> c2_numstat.txt
  tb141_einfuegen.py journal --kennung K --block DATEI [--probe]   -> d2_journal.txt (Probe: d2_journal_probe.txt)
  tb141_einfuegen.py j1 --kennung K [--probe]                      -> d2_j1.txt (Probe: d2_j1_probe.txt)
  tb141_einfuegen.py j1vergleich --kennung K                       -> d2_j1_vergleich.txt

rc 0: wie Soll. rc 1: Abweichung, die Ausgabe nennt sie. rc 2: Bedingung verletzt, nichts geändert
(journal und j1 schreiben dann *_abgewiesen.txt und lassen einen früheren Beleg stehen).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md")
BELEG = Path("docs/belege/TB-141")
JOURNAL = Path("docs/projektfuehrung/JOURNAL.md")
JANKER = "\n---\n\n## Wiederkehrende Lehren\n"
SKRIPT = "tb141_einfuegen.py"

RE_KOPF = re.compile(r"^#### ([ESJ]\d+) — ")
RE_DATEI = re.compile(r"^Zieldatei: `([^`]+)`$")
RE_ANKER = re.compile(r"^Anker: (?:`` (.+?) ``|`([^`]+)`) · Art: \*\*(nach der Zeile|vor der Zeile)\*\*$")
RE_FORM = re.compile(r"^Form: \*\*(Zeilen|Block)\*\*$")
RE_PRUEF = re.compile(r"^Prüfanker: (?:`` (.+?) ``|`([^`]+)`)$")


def lies_auftrag():
    zeilen = AUFTRAG.read_text(encoding="utf-8").split("\n")
    abschnitte, cur, zaun = [], None, False
    for z in zeilen:
        if not zaun and z.startswith("```"):
            zaun = True
        elif zaun and z == "```":
            zaun = False
        elif not zaun:
            m = RE_KOPF.match(z)
            if m:
                cur = {"nr": m.group(1), "zeilen": []}
                abschnitte.append(cur)
                continue
            if re.match(r"^#{1,4} ", z):
                cur = None
                continue
        if cur is not None:
            cur["zeilen"].append(z)
    eintraege = []
    for a in abschnitte:
        e = {"nr": a["nr"], "datei": None, "anker": None, "art": None, "form": None,
             "pruef": [], "text": None}
        zl = a["zeilen"]
        i = 0
        while i < len(zl):
            z = zl[i]
            if m := RE_DATEI.match(z):
                e["datei"] = m.group(1)
            elif m := RE_ANKER.match(z):
                e["anker"] = m.group(1) if m.group(1) is not None else m.group(2)
                e["art"] = m.group(3)
            elif m := RE_FORM.match(z):
                e["form"] = m.group(1)
            elif m := RE_PRUEF.match(z):
                e["pruef"].append(m.group(1) if m.group(1) is not None else m.group(2))
            elif z == "```" and e["text"] is None:
                k = zl.index("```", i + 1)
                e["text"] = zl[i + 1:k]
                i = k
            i += 1
        eintraege.append(e)
    E = [e for e in eintraege if e["nr"].startswith("E")]
    S = [e for e in eintraege if e["nr"].startswith("S")]
    J = [e for e in eintraege if e["nr"].startswith("J")]
    # Sollwerte: der json-Block unter "### Sollwerte (maschinenlesbar)"
    i = zeilen.index("### Sollwerte (maschinenlesbar)")
    a = next(k for k in range(i + 1, len(zeilen)) if zeilen[k] == "```json")
    b = next(k for k in range(a + 1, len(zeilen)) if zeilen[k] == "```")
    soll = json.loads("\n".join(zeilen[a + 1:b]))
    for e in E:
        if None in (e["datei"], e["anker"], e["art"], e["form"], e["text"]):
            sys.exit(f"{e['nr']}: Abschnitt unvollständig gelesen")
    for e in S:
        if e["datei"] is None or not e["pruef"]:
            sys.exit(f"{e['nr']}: Prüfung unvollständig gelesen")
    if [e["nr"] for e in E] != [f"E{n}" for n in range(1, soll["einfuegungen"] + 1)]:
        sys.exit(f"Einfügungen nicht wie Soll gelesen: {[e['nr'] for e in E]}")
    if [e["nr"] for e in S] != [f"S{n}" for n in range(1, soll["pruefungen"] + 1)]:
        sys.exit(f"Prüfungen nicht wie Soll gelesen: {[e['nr'] for e in S]}")
    if [e["nr"] for e in J] != ["J1"] or J[0]["text"] is None:
        sys.exit("J1 nicht gelesen")
    return E, S, J[0], soll


def schreibe(name, kopf, zeilen):
    BELEG.mkdir(parents=True, exist_ok=True)
    pfad = BELEG / name
    text = kopf + "\n" + "\n".join(zeilen) + "\n"
    pfad.write_text(text, encoding="utf-8")
    assert pfad.read_text(encoding="utf-8") == text, f"{pfad}: Rücklesen ungleich"
    print(text, end="")


def sperrliste(soll):
    """Zieldateien gegen die Sperrliste: Register Abschnitt 10 und ARBEITSWEISE-Tabelle."""
    aus, treffer = [], 0
    reg = Path(soll["sperrliste"]["register"]).read_text(encoding="utf-8")
    a = reg.index("\n## 10. Die Sperrliste\n")
    b = reg.index("\n## ", a + 5)
    abschnitt10 = reg[a:b]
    aw = Path("docs/projektfuehrung/ARBEITSWEISE.md").read_text(encoding="utf-8")
    c = aw.index(soll["sperrliste"]["arbeitsweise_kopf"])
    d = aw.index("\n\n", aw.index("| Datei | seit |", c))
    tabelle = aw[c:d]
    for name in soll["sperrliste"]["suchworte"]:
        n10, nt = abschnitt10.count(name), tabelle.count(name)
        treffer += n10 + nt
        aus.append(f"Sperrliste · {name!r} · Register Abschnitt 10 ({abschnitt10.count(chr(10))} Zeilen) {n10} · "
                   f"ARBEITSWEISE-Tabelle ({tabelle.count(chr(10)) + 1} Zeilen) {nt}")
    return aus, treffer


def ankerzeilen(inhalt, anker):
    return [n for n, z in enumerate(inhalt.split("\n")) if anker in z]


def einsetzen(inhalt, e):
    zeilen = inhalt.split("\n")
    n = ankerzeilen(inhalt, e["anker"])[0]
    block = list(e["text"])
    if e["form"] == "Block":
        if e["art"] == "nach der Zeile":
            vor = [] if zeilen[n] == "" else [""]
            nach = [] if n + 1 < len(zeilen) and zeilen[n + 1] == "" else [""]
            zeilen[n + 1:n + 1] = vor + block + nach
        else:
            vor = [] if n > 0 and zeilen[n - 1] == "" else [""]
            nach = [] if zeilen[n] == "" else [""]
            zeilen[n:n] = vor + block + nach
    else:
        if e["art"] == "nach der Zeile":
            zeilen[n + 1:n + 1] = block
        else:
            zeilen[n:n] = block
    return "\n".join(zeilen), n + 1


def probe_zeilen(E, S, soll, inhalte):
    aus, gut = [], True
    alle_texte = "\n".join("\n".join(e["text"]) for e in E)
    for e in E:
        inh = inhalte[e["datei"]]
        vorher = inh.count(e["anker"])
        az = ankerzeilen(inh, e["anker"])
        schon = inh.count(e["text"][0])
        im_text = alle_texte.count(e["anker"])
        ok = vorher == 1 and len(az) == 1 and schon == 0 and im_text == 0
        gut &= ok
        aus.append(f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · Ankerzeile "
                   f"{az[0] + 1 if len(az) == 1 else az} · Art {e['art']} · Form {e['form']} · "
                   f"Textzeilen {len(e['text'])} · erste Textzeile schon {schon} · Anker in neuen Texten {im_text} · "
                   f"{'ok' if ok else 'ABWEICHUNG'}")
    for s in S:
        inh = inhalte[s["datei"]]
        for p in s["pruef"]:
            c = inh.count(p)
            gut &= c == 1
            aus.append(f"{s['nr']} · {s['datei']} · Prüfanker {p[:60]!r} · {c} · {'ok' if c == 1 else 'ABWEICHUNG'}")
    return aus, gut


def main():
    arg = sys.argv[1:]
    if not arg:
        sys.exit(__doc__)
    modus = arg[0]
    E, S, J1, soll = lies_auftrag()
    dateien = sorted({e["datei"] for e in E} | {s["datei"] for s in S})
    inhalte = {d: Path(d).read_text(encoding="utf-8") for d in dateien}

    if modus in ("probe", "einfuegen"):
        aus, gut = probe_zeilen(E, S, soll, inhalte)
        sp, treffer = sperrliste(soll)
        aus += sp
        if modus == "probe":
            aus.append(f"Einfügungen {len(E)} · Prüfungen {len(S)} · Sperrliste Treffer {treffer} · "
                       f"Gesamt: {'wie Soll' if gut and treffer == 0 else 'ABWEICHUNG'}")
            schreibe("a_probe.txt", "# TB-141 0c — Probe, nur gelesen (tb141_einfuegen.py probe)", aus)
            sys.exit(0 if gut and treffer == 0 else 1)
        if treffer:
            print("Sperrliste getroffen — nichts geschrieben"); sys.exit(2)
        if all(inhalte[e["datei"]].count(e["text"][0]) == 1 for e in E):
            print("Alle Einfügungen stehen schon — nichts geschrieben"); sys.exit(2)
        neu, aus, gut = dict(inhalte), [], True
        for e in E:
            inh = neu[e["datei"]]
            vorher = inh.count(e["anker"])
            if vorher != 1 or len(ankerzeilen(inh, e["anker"])) != 1 or inh.count(e["text"][0]) != 0:
                gut = False
                aus.append(f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · ausgeführt nein · "
                           f"Text nachher {inh.count(e['text'][0])}")
                continue
            z_vor = inh.count("\n")
            inh, az = einsetzen(inh, e)
            neu[e["datei"]] = inh
            nachher = inh.count(e["text"][0])
            gut &= nachher == 1
            aus.append(f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · ausgeführt ja · "
                       f"Text nachher {nachher} · Zeilen +{inh.count(chr(10)) - z_vor}")
        for d in dateien:
            if neu[d] != inhalte[d]:
                Path(d).write_text(neu[d], encoding="utf-8")
                assert Path(d).read_text(encoding="utf-8") == neu[d]
        for d in dateien:
            aus.append(f"Datei {d} · Zeilen vorher {inhalte[d].count(chr(10))} · nachher {neu[d].count(chr(10))}")
        aus.append(f"Gesamt: {'alle ausgeführt, je genau einmal' if gut else 'ABWEICHUNG'}")
        schreibe("a_einfuegungen.txt", "# TB-141 A — Einfügungen (tb141_einfuegen.py einfuegen); "
                 "E<n> · Datei · Anker vorher · ausgeführt · Text nachher · Zeilen", aus)
        sys.exit(0 if gut else 1)

    if modus == "vergleich":
        aus, gut = [], True
        for e in E:
            ziel = inhalte[e["datei"]].encode("utf-8")
            text = "\n".join(e["text"]).encode("utf-8")
            gesamt = ziel.count(text)
            grenzen = ziel.count(b"\n" + text + b"\n")
            ok = gesamt == 1 and grenzen == 1
            if ok and e["form"] == "Block":
                ok = ziel.count(b"\n\n" + text + b"\n\n") == 1
            gut &= ok
            aus.append(f"{e['nr']} · {e['datei']} · {len(text)} Bytes · {len(e['text'])} Zeile(n) · "
                       f"Vorkommen {gesamt} · an Zeilengrenzen {grenzen} · {'GLEICH' if ok else 'ABWEICHUNG'}")
        for s in S:
            for p in s["pruef"]:
                c = inhalte[s["datei"]].count(p)
                gut &= c == 1
                aus.append(f"{s['nr']} · Prüfanker {p[:60]!r} · nachher {c} · {'ok' if c == 1 else 'ABWEICHUNG'}")
        aus.append(f"Anzahl Einfügungen: {len(E)} · Gesamt: "
                   f"{'alle zeichengleich, je genau einmal' if gut else 'ABWEICHUNG'}")
        schreibe("c3_vergleich.txt", "# TB-141 C3 — Zeichengleichheit (tb141_einfuegen.py vergleich)", aus)
        sys.exit(0 if gut else 1)

    if modus == "numstat":
        von, bis = arg[1], arg[2]
        roh = subprocess.run(["git", "diff", "--numstat", von, bis], capture_output=True, text=True, check=True).stdout
        ist = {}
        for z in roh.splitlines():
            plus, minus, pfad = z.split("\t")
            ist[pfad] = [int(plus), int(minus)]
        aus, gut = [f"roh: {z}" for z in roh.splitlines()], True
        for pfad, (p, m) in soll["numstat_a"].items():
            ok = ist.get(pfad) == [p, m]
            gut &= ok
            aus.append(f"Soll {pfad} {p}\t{m} · Ist {ist.get(pfad)} · {'gleich' if ok else 'ABWEICHUNG'}")
        fremd = [p for p in ist if p not in soll["numstat_a"] and not p.startswith(str(BELEG) + "/")]
        gut &= not fremd
        aus.append(f"weitere Dateien ausser Belegen: {fremd if fremd else 'keine'}")
        aus.append(f"Gesamt: {'wie Soll, keine entfernte Zeile' if gut else 'ABWEICHUNG'}")
        schreibe("c2_numstat.txt", f"# TB-141 C2 — git diff --numstat {von} {bis} (tb141_einfuegen.py numstat)", aus)
        sys.exit(0 if gut else 1)

    if modus in ("journal", "j1", "j1vergleich"):
        k = arg[arg.index("--kennung") + 1]
        probe = "--probe" in arg
        j = JOURNAL.read_text(encoding="utf-8")
        kopf = f"## {k} — TB-141"
        if modus == "journal":
            block = Path(arg[arg.index("--block") + 1]).read_text(encoding="utf-8").rstrip("\n")
            bed = [("Ankertext genau 1", j.count(JANKER) == 1),
                   (f"Kopfzeile {kopf!r} im Journal noch 0", j.count("\n" + kopf) == 0),
                   ("Block beginnt mit der Kopfzeile", block.startswith(kopf)),
                   ("Block hat genau einen Absatz **Quelle:**", block.count("\n**Quelle:**") == 1),
                   ("Block hat genau eine Zeile ### Was gemessen ist", (block + "\n").count("\n### Was gemessen ist\n") == 1),
                   ("Block ohne Trennstrich und ohne J1", "\n---\n" not in block and J1["text"][0] not in block)]
            aus = [f"{t} · {'ja' if ok else 'NEIN'}" for t, ok in bed]
            if not all(ok for _, ok in bed):
                schreibe("d2_journal_abgewiesen.txt", "# TB-141 D2 — Journalblock (tb141_einfuegen.py journal), abgewiesen, nichts geschrieben", aus)
                sys.exit(2)
            neu = j.replace(JANKER, "\n---\n\n" + block + "\n\n---\n\n## Wiederkehrende Lehren\n")
            aus.append(f"Zeilen Journal vorher {j.count(chr(10))} · nachher {neu.count(chr(10))} · "
                       f"{'Probe, nichts geschrieben' if probe else 'geschrieben'}")
            if not probe:
                JOURNAL.write_text(neu, encoding="utf-8")
                assert JOURNAL.read_text(encoding="utf-8") == neu
            schreibe("d2_journal_probe.txt" if probe else "d2_journal.txt", "# TB-141 D2 — Journalblock (tb141_einfuegen.py journal"
                     + (" --probe)" if probe else ")"), aus)
            sys.exit(0)
        a = j.find("\n" + kopf)
        b = j.find(JANKER, a + 1)
        blk = j[a + 1:b] if a >= 0 and b > a else ""
        bz = blk.split("\n")
        q = [n for n, z in enumerate(bz) if z.startswith("**Quelle:**")]
        w = [n for n, z in enumerate(bz) if z == "### Was gemessen ist"]
        text = "\n".join(J1["text"])
        if modus == "j1":
            bed = [("Ankertext genau 1", j.count(JANKER) == 1),
                   (f"Kopfzeile {kopf!r} genau 1, vor dem Ankertext", j.count("\n" + kopf) == 1 and 0 <= a < b),
                   ("im Block genau ein **Quelle:** und genau ein ### Was gemessen ist, in dieser Folge",
                    len(q) == 1 and len(w) == 1 and q[0] < w[0]),
                   ("erste Zeile von J1 im Journal noch 0", j.count(J1["text"][0]) == 0)]
            aus = [f"{t} · {'ja' if ok else 'NEIN'}" for t, ok in bed]
            if not all(ok for _, ok in bed):
                schreibe("d2_j1_abgewiesen.txt", "# TB-141 D2 — J1 (tb141_einfuegen.py j1), abgewiesen, nichts geschrieben", aus)
                sys.exit(2)
            p = w[0]
            einsatz = J1["text"] + [""] if bz[p - 1] == "" else [""] + J1["text"] + [""]
            bz[p:p] = einsatz
            neu = j[:a + 1] + "\n".join(bz) + j[b:]
            aus.append(f"J1 · {JOURNAL} · Block {k} · Textzeilen {len(J1['text'])} · Zeilen +{neu.count(chr(10)) - j.count(chr(10))} · "
                       f"{'Probe, nichts geschrieben' if probe else 'eingesetzt'}")
            if not probe:
                JOURNAL.write_text(neu, encoding="utf-8")
                assert JOURNAL.read_text(encoding="utf-8") == neu
            schreibe("d2_j1_probe.txt" if probe else "d2_j1.txt", "# TB-141 D2 — J1 (tb141_einfuegen.py j1"
                     + (" --probe)" if probe else ")"), aus)
            sys.exit(0)
        gesamt = j.count(text)
        grenzen = j.count("\n" + text + "\n")
        im_block = text in blk and (len(w) == 1 and blk.find(text) < blk.find("\n### Was gemessen ist\n"))
        ok = gesamt == 1 and grenzen == 1 and im_block
        aus = [f"J1 · {JOURNAL} · {len(text.encode('utf-8'))} Bytes · {len(J1['text'])} Zeile(n) · Vorkommen {gesamt} · "
               f"an Zeilengrenzen {grenzen} · im Block {k} vor ### Was gemessen ist {'ja' if im_block else 'nein'} · "
               f"{'GLEICH' if ok else 'ABWEICHUNG'}"]
        schreibe("d2_j1_vergleich.txt", "# TB-141 D2 — J1 Zeichengleichheit (tb141_einfuegen.py j1vergleich)", aus)
        sys.exit(0 if ok else 1)
    sys.exit(f"unbekannter Modus {modus!r}")


if __name__ == "__main__":
    main()
