#!/usr/bin/env python3
# tb146_einfuegen.py - Werkzeug zum Auftrag TB-146, ausgelesen aus Anhang B.
# Abgeleitet von tb145_einfuegen.py (TB-145, Anhang B), ohne Direktiven: jedes Stueck
# steht woertlich im Auftrag. Liest Stuecke, Anker und Texte aus dem Auftrag,
# prueft alles, bevor es schreibt, weist einen zweiten Lauf ab und schreibt nur die
# vier Zieldateien (an Ort und Stelle, mit Ruecklesen; keine Hilfsdatei daneben).
# Die Ausgabe geht nach stdout; die Sitzung leitet sie in den Beleg um.
# Aufruf aus der Repo-Wurzel mit trading-env/bin/python3 -B:
#   probe                                nur lesen
#   einfuegen                            alle Stuecke ausser J1
#   vergleich                            jedes Stueck zeichengleich, genau einmal
#   numstat <von> <bis> [<Blockdatei>]   git diff --numstat gegen die Sollwerte
#   journal <Blockdatei> [--probe]       Block der Sitzung samt J1
# rc 0 wie Soll · rc 1 Abweichung, nichts geschrieben · rc 2 abgewiesen (zweiter Lauf
# oder Bedingung verletzt), nichts geschrieben · rc 3 Abbruch vor dem Schreiben.
import json, re, subprocess, sys

P, A = "docs/projektfuehrung/", "docs/auftraege/"
AUF = A + "MAC_TB-146_regelwerk_dokunachtrag_0910.md"
JOU, BACK = P + "JOURNAL.md", P + "BACKLOG.md"
ZIELE = (P + "ARBEITSWEISE.md", P + "UMZUG.md", BACK, JOU)
FREI = ("docs/belege/TB-146/", "docs/ERGEBNIS_TB-146_regelwerk_dokunachtrag_0910.md")
ZAUN, KL, KR = "~" * 3, "⟦", "⟧"


def zeilen(p):
    with open(p, encoding="utf-8") as f:
        t = f.read()
    assert t.endswith("\n"), p + ": kein Zeilenende am Schluss"
    return t[:-1].split("\n")


def soll():
    z = zeilen(AUF)
    a = z.index("```json", z.index("### Sollwerte (maschinenlesbar)"))
    return json.loads("\n".join(z[a + 1:z.index("```", a + 1)]))


def stuecke():
    # Kopf '#### <Id> — …', Felder, dann der Text zwischen zwei Tilde-Zaeunen
    z, aus, i = zeilen(AUF), {}, 0
    while i < len(z):
        m = re.match(r"#### ([A-Z]\d+) — ", z[i])
        i += 1
        if not m:
            continue
        s = {"id": m.group(1), "zie": "", "art": "", "for": "", "ank": ""}
        while z[i] != ZAUN:
            for name in ("Zieldatei", "Art", "Form", "Anker"):
                if z[i].startswith(name + ": "):
                    v = z[i][len(name) + 2:]
                    if name == "Anker":
                        assert v[0] == KL and v[-1] == KR, s["id"] + ": Anker ohne Klammern"
                    s[name[:3].lower()] = v.strip("`") if name == "Zieldatei" else v[1:-1] if name == "Anker" else v
            i += 1
        j = z.index(ZAUN, i + 1)
        s["text"] = z[i + 1:j]
        assert s["text"] and s["zie"] in ZIELE and s["id"] not in aus, s["id"] + ": Stueck unvollstaendig oder keine Zieldatei"
        assert s["id"] == "J1" or (s["art"] in ("nach", "vor") and s["for"] in ("Zeilen", "Block") and s["ank"]), s["id"] + ": Felder"
        aus[s["id"]] = s
        i = j + 1
    assert list(aus) == soll()["stuecke"], "Stuecke nicht wie Soll gelesen: " + " ".join(aus)
    return aus


def fertig(s):
    # der Text eines Stuecks, wie er im Auftrag steht (TB-146 hat keine Direktiven)
    for x in s["text"]:
        assert KL not in x, s["id"] + ": Klammer im Text"
    return list(s["text"])


def vorkommen(zl, text):
    return [k for k in range(len(zl) - len(text) + 1) if zl[k:k + len(text)] == text]


def plan():
    # prueft jedes Stueck an den Dateien, wie sie liegen, und setzt im Speicher ein; schreibt nichts
    st = [s for s in stuecke().values() if s["id"] != "J1"]
    texte = dict((s["id"], fertig(s)) for s in st)
    vor = dict((p, zeilen(p)) for p in sorted(set(s["zie"] for s in st)))
    neu, aus, schon, gut, so = dict((p, list(vor[p])) for p in vor), [], [], True, soll()["numstat"]
    for s in st:
        p, text = s["zie"], texte[s["id"]]
        u = [k for k, x in enumerate(vor[p]) if s["ank"] in x]
        da = sum(1 for x in vor[p] if x == text[0])
        fremd = sum(1 for t in st if t["zie"] == p for x in texte[t["id"]] if s["ank"] in x)
        ok, tab, plus = len(u) == 1 and da == 0 and fremd == 0, "–", 0
        if da:
            schon.append(s["id"])
        if ok:
            zl = neu[p]
            a = [k for k, x in enumerate(zl) if s["ank"] in x][0]
            k, ein = (a + 1 if s["art"] == "nach" else a), list(text)
            davor, danach = (zl[k - 1] if k > 0 else ""), (zl[k] if k < len(zl) else "")
            if s["for"] == "Block":  # genau eine Leerzeile davor und danach, keine verdoppelt
                ein = ([""] if davor != "" else []) + ein + ([""] if danach != "" else [])
            elif text[0].startswith("|"):  # Tabellenzeile: nur hinter eine Tabellenzeile
                tab = "ja" if all(x.startswith("|") for x in text) and davor.startswith("|") else "NEIN"
            else:  # keine Tabellenzeile: nicht mitten in eine Tabelle
                tab = "NEIN" if davor.startswith("|") and danach.startswith("|") else "–"
            ok, plus = tab != "NEIN", len(ein)
            if ok:
                neu[p] = zl[:k] + ein + zl[k:]
        gut = gut and ok
        aus.append("%s · %s · Anker Z. %s · %s · %s · Textzeilen %d · erste Zeile schon %d · Anker in neuen Texten %d · Tabelle %s · Zeilen +%d · %s"
                   % (s["id"], p, u[0] + 1 if len(u) == 1 else "%d Treffer" % len(u), s["art"], s["for"], len(text), da, fremd, tab, plus, "ok" if ok else "ABWEICHUNG"))
    if gut:
        for s in st:
            n = len(vorkommen(neu[s["zie"]], texte[s["id"]]))
            if n != 1:
                gut = False
                aus.append("%s · Text nach dem Einsetzen %d-mal statt 1 · ABWEICHUNG" % (s["id"], n))
    for p in sorted(vor):
        d, w = len(neu[p]) - len(vor[p]), so.get(p, [None])[0]
        gut = gut and d == w
        aus.append("Datei %s · Zeilen vorher %d · nachher %d · +%d · Soll +%s · %s" % (p, len(vor[p]), len(neu[p]), d, w, "gleich" if d == w else "ABWEICHUNG"))
    if sorted(vor) != sorted(so):
        gut = False
        aus.append("Zieldateien der Stuecke ungleich den Sollwerten · ABWEICHUNG")
    aus.append("Stuecke %d · eingefuegte Zeilen %d" % (len(st), sum(len(neu[p]) - len(vor[p]) for p in vor)))
    return gut, schon, aus, vor, neu, st, texte


def einfuegen(probe):
    print("# TB-146 %s — Stuecke aus Anhang A%s" % ("probe" if probe else "einfuegen", " (nur gelesen)" if probe else ""))
    gut, schon, aus, vor, neu, st, texte = plan()
    print("\n".join(aus))
    if schon and not probe:
        print("ABGEWIESEN, nichts geschrieben: erste Zeile steht schon in der Datei (zweiter Lauf?): " + " ".join(schon))
        return 2
    if not gut:
        print("Gesamt: ABWEICHUNG, nichts geschrieben")
        return 1
    if not probe:
        for p in sorted(vor):
            assert p in ZIELE and p != JOU, p + " ist hier keine Zieldatei"
            t = "\n".join(neu[p]) + "\n"
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
            with open(p, encoding="utf-8") as f:
                assert f.read() == t, p + ": Ruecklesen ungleich (GESCHRIEBEN, Stand pruefen)"
            print("geschrieben und zurueckgelesen: " + p)
    print("Gesamt: wie Soll, " + ("nichts geschrieben (Probe)" if probe else "alle eingefuegt, je genau einmal"))
    return 0


def vergleich():
    print("# TB-146 vergleich — jedes Stueck zeichengleich und genau einmal in seiner Zieldatei")
    gut = True
    for s in stuecke().values():
        if s["id"] == "J1":
            continue
        zl, text = zeilen(s["zie"]), fertig(s)
        v = vorkommen(zl, text)
        ok = len(v) == 1
        if ok and s["for"] == "Block":
            k, e = v[0], v[0] + len(text)
            ok = (k == 0 or zl[k - 1] == "") and (e == len(zl) or zl[e] == "")
        gut = gut and ok
        print("%s · %s · %d Bytes · %d Zeile(n) · Vorkommen %d · %s" % (s["id"], s["zie"], len("\n".join(text).encode("utf-8")), len(text), len(v), "GLEICH" if ok else "ABWEICHUNG"))
    print("Gesamt: " + ("alle zeichengleich, je genau einmal" if gut else "ABWEICHUNG"))
    return 0 if gut else 1


def numstat(von, bis, block):
    print("# TB-146 numstat — git diff --numstat %s %s gegen die Sollwerte" % (von, bis))
    roh = subprocess.run(["git", "diff", "--numstat", von, bis], capture_output=True, universal_newlines=True, check=True).stdout
    so, ist, gut = dict((p, list(v)) for p, v in soll()["numstat"].items()), {}, True
    if block:
        so[JOU] = [len(zeilen(block)) + soll()["j1_zeilen"] + 4, 0]
    for x in roh.splitlines():
        print("roh: " + x)
        a, b, p = x.split("\t")
        ist[p] = [int(a) if a.isdigit() else a, int(b) if b.isdigit() else b]
    for p in sorted(so):
        ok = ist.get(p) == so[p]
        gut = gut and ok
        print("Soll %s %d\t%d · Ist %s · %s" % (p, so[p][0], so[p][1], ist.get(p), "gleich" if ok else "ABWEICHUNG"))
    fremd = sorted(p for p in ist if p not in so and not p.startswith(FREI[0]) and p != FREI[1])
    print("weitere Dateien ausser Belegen und Ergebnis: " + (" ".join(fremd) if fremd else "keine"))
    gut = gut and not fremd
    print("Gesamt: " + ("wie Soll, keine entfernte Zeile in den Zieldateien" if gut else "ABWEICHUNG"))
    return 0 if gut else 1


def journal(blockpfad, probe):
    print("# TB-146 journal%s — Block der Sitzung samt J1 vor '## Wiederkehrende Lehren'" % (" (Probe)" if probe else ""))
    st, so = stuecke(), soll()
    zl, b, b1 = zeilen(JOU), zeilen(blockpfad), fertig(st["B1"])
    j1 = fertig(st["J1"]) + [x for x in b1 if x.startswith("- ")]
    k = [n for n, x in enumerate(zl) if x == "## Wiederkehrende Lehren"]
    assert len(k) == 1, "Schlussueberschrift trifft %d-mal" % len(k)
    k, was = k[0], "### Was gemessen ist"
    alt = [m.group(1) for m in (re.match(r"## ([A-Z]{2}) — ", x) for x in zl[:k]) if m][-1]
    neu = alt[0] + chr(ord(alt[1]) + 1) if alt[1] != "Z" else chr(ord(alt[0]) + 1) + "A"
    g = b.index(was) if was in b else 0
    bed = (("letzte Kennung %s, Kopfzeile beginnt mit '## %s — TB-146'" % (alt, neu), b[0].startswith("## %s — TB-146" % neu)),
           ("genau eine Zeile '%s', Leerzeile davor" % was, b.count(was) == 1 and g > 0 and b[g - 1] == ""),
           ("genau eine Zeile '### Was offen bleibt'", b.count("### Was offen bleibt") == 1),
           ("kein Trennstrich im Block, Schlusszeile beginnt mit '*Geschrieben'", "---" not in b and b[-1].startswith("*Geschrieben")),
           ("J1 weder im Journal noch im Block", j1[0] not in zl and j1[0] not in b),
           ("vor der Schlussueberschrift stehen '---' und eine Leerzeile", zl[k - 2:k] == ["---", ""]),
           ("B1 steht genau einmal im BACKLOG (Schritt E gelaufen)", len(vorkommen(zeilen(BACK), b1)) == 1),
           ("J1-Zeilen %d wie Soll %d" % (len(j1), so["j1_zeilen"]), len(j1) == so["j1_zeilen"]))
    for name, ok in bed:
        print("%s · %s" % (name, "ja" if ok else "NEIN"))
    if not all(ok for name, ok in bed):
        print("ABGEWIESEN, nichts geschrieben")
        return 2
    ein = b[:g] + j1 + [""] + b[g:] + ["", "---", ""]
    print("Kennung %s (erwartet %s) · Blockzeilen %d · J1-Zeilen %d · Zeilen +%d (= Block + J1 + 1 + 3)" % (neu, so["kennung"], len(b), len(j1), len(ein)))
    if not probe:
        t = "\n".join(zl[:k] + ein + zl[k:]) + "\n"
        with open(JOU, "w", encoding="utf-8") as f:
            f.write(t)
        with open(JOU, encoding="utf-8") as f:
            assert f.read() == t, JOU + ": Ruecklesen ungleich (GESCHRIEBEN, Stand pruefen)"
    print("Gesamt: " + ("nichts geschrieben (Probe)" if probe else "geschrieben und zurueckgelesen: " + JOU))
    return 0


def main(a):
    probe = "--probe" in a
    if a == ["probe"] or a == ["einfuegen"]:
        return einfuegen(a[0] == "probe")
    if a == ["vergleich"]:
        return vergleich()
    if a[:1] == ["numstat"] and len(a) in (3, 4):
        return numstat(a[1], a[2], a[3] if len(a) == 4 else "")
    if a[:1] == ["journal"] and len(a) in (2, 3) and (len(a) == 2 or probe):
        return journal(a[1], probe)
    print("Aufruf: probe | einfuegen | vergleich | numstat <von> <bis> [<Blockdatei>] | journal <Blockdatei> [--probe]")
    return 64


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except AssertionError as e:
        print("ABBRUCH: %s" % e)
        sys.exit(3)
