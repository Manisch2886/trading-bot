#!/usr/bin/env python3
# tb142_werkzeug.py - Werkzeug zum Auftrag TB-142, ausgelesen aus Anhang C.
# Liest Stuecke (W, E, J), Anker und Texte aus dem Auftrag; prueft alles, bevor
# es schreibt; weist einen zweiten Lauf ab; schreibt nur die Zieldateien.
import hashlib, os, re, subprocess, sys

D, P = "docs/werkzeuge/sitzungswaechter/", "docs/projektfuehrung/"
AUF = "docs/auftraege/MAC_TB-142_waechter_reparatur.md"
SH, LIES, UEB, JOU = D + "starte_sitzung.sh", D + "LIESMICH.md", P + "UEBERGABE.md", P + "JOURNAL.md"
MESS = "docs/belege/TB-142/messwerte.txt"
ZIELE = (SH, LIES, P + "ARBEITSWEISE.md", P + "BACKLOG.md", JOU)
START_HEAD = "cd ~/trading-bot && exec claude --effort high --remote-control"
KONST = ("STARTZEILE", "STUFEN", "MERKMAL_EINGABEZEILE", "MERKMAL_FRAGE", "FENSTER_SCHLIESSEN", "LESE_EIGENSCHAFT")
LOGTEILE = ("⭐ EINGABEBEREIT (", "Eingabezeile steht, keine Frage offen (nach ", "⛔ STARTFRAGE (", "⛔ KEINE EINGABEZEILE (",
            "neu geoeffnet (Tab ", "geschlossen (das beim Start gemerkte, kein laufender Prozess).", "bleibt offen: ",
            "⛔ FENSTERLISTE NICHT LESBAR", " Lesungen (0 = Terminal hat nicht geantwortet; dann liegt es nicht am Merkmal).",
            "⛔ MESSWERTE FEHLEN", "⛔ FENSTER NICHT BESTIMMBAR", "⛔ FENSTER NICHT NEU", "⛔ FENSTER FEHLT", "⛔ ABBRUCH",
            "⛔ osascript konnte Terminal nicht ansteuern", "NICHT beendet")
VERBOTEN = ("keystroke", "System Events")
BASH4 = r"declare\s+-\w*A|\bmapfile\b|\breadarray\b|\$\{[^}]*(,,|\^\^)|&>>|\|&|\bcoproc\b|;;&|;&"
ZAUN, KL, KR = "~" * 3, "⟦", "⟧"


def zeilen(p):
    assert os.path.isfile(p), p + " fehlt"
    with open(p, encoding="utf-8") as f:
        t = f.read()
    assert t.endswith("\n"), p + ": kein Zeilenende am Schluss"
    return t[:-1].split("\n")


def stuecke():
    # Kopf '#### <Id> — …', Felder, dann der Text zwischen zwei Tilde-Zaeunen
    z, aus, i = zeilen(AUF), {}, 0
    while i < len(z):
        m = re.match(r"#### ([WEJ]\d+) — ", z[i])
        i += 1
        if not m:
            continue
        s = {"id": m.group(1), "bed": "", "for": "", "art": "", "bis": ""}
        while z[i] != ZAUN:
            for name in ("Zieldatei", "Art", "Form", "Bedingung", "Anker", "Bis"):
                if z[i].startswith(name + ": "):
                    v = z[i][len(name) + 2:]
                    if name in ("Anker", "Bis"):
                        assert v[0] == KL and v[-1] == KR, s["id"] + ": Anker ohne Klammern"
                    s[name[:3].lower()] = v.strip("`") if name == "Zieldatei" else v[1:-1] if name in ("Anker", "Bis") else v
            i += 1
        j = z.index(ZAUN, i + 1)
        s["text"] = z[i + 1:j]
        assert s["text"] and s["zie"] in ZIELE and s["id"] not in aus, s["id"]
        aus[s["id"]] = s
        i = j + 1
    return aus


def treffer(zl, anker, ganz):
    return [k for k, x in enumerate(zl) if (x == anker if ganz else anker in x)]


def wende_an(zl, s, text, ur):
    # .sh: der Anker ist die ganze Zeile; sonst ein Teil der Zeile. Jeder Anker genau einmal.
    # Gemeldet wird die Ankerzeile in der Datei vor dem Lauf (ur).
    ganz = s["zie"].endswith(".sh")
    t, u = treffer(zl, s["ank"], ganz), treffer(ur, s["ank"], ganz)
    assert len(t) == 1 and len(u) == 1, "%s: Anker trifft %d-mal statt 1" % (s["id"], len(t))
    a, art = t[0], s["art"]
    if art.startswith("ersetze"):
        b = treffer(zl, s["bis"], ganz) if art == "ersetze" else [len(zl) - 1]
        assert art in ("ersetze", "ersetze-bis-ende") and len(b) == 1 and b[0] >= a, s["id"] + ": Bis-Anker"
        return zl[:a] + text + zl[b[0] + 1:], "Anker Z. %d · %d Zeilen ersetzt durch %d" % (u[0] + 1, b[0] - a + 1, len(text))
    assert art in ("nach", "vor"), s["id"] + ": Art " + art
    k, ein = (a + 1 if art == "nach" else a), list(text)
    if s["for"] == "Block":  # genau eine Leerzeile davor und danach, keine verdoppelt
        ein = ([""] if k > 0 and zl[k - 1] != "" else []) + ein + ([""] if k < len(zl) and zl[k] != "" else [])
    return zl[:k] + ein + zl[k:], "Anker Z. %d · %s der Zeile · Zeilen +%d" % (u[0] + 1, art, len(ein))


def schreibe(p, zl):
    assert p in ZIELE, p + " ist keine Zieldatei"
    with open(p + ".tb142_neu", "w", encoding="utf-8") as f:
        f.write("\n".join(zl) + "\n")
    os.chmod(p + ".tb142_neu", os.stat(p).st_mode & 0o7777)
    os.replace(p + ".tb142_neu", p)  # ein Schritt: ein laufender Waechter liest seine alte Datei zu Ende


def pruefe_sh(zl, teil):
    # bash -n an einer Kopie im Scratch, dann die Schranken des Auftrags
    t = os.path.join(os.environ.get("TMPDIR", "/tmp"), "tb142_pruef.sh")
    with open(t, "w", encoding="utf-8") as f:
        f.write("\n".join(zl) + "\n")
    r = subprocess.run(["/bin/bash", "-n", t], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    code = [x for x in zl if not x.lstrip().startswith("#")]
    ds = [x for x in code if "do script" in x]
    vb = [w for w in VERBOTEN if any(w in x for x in zl)]
    b4 = [x for x in code if re.search(BASH4, x)]
    f = ["bash -n: " + r.stdout.decode("utf-8", "replace")[:300]] if r.returncode else []
    if len(ds) != 1 or " in window" in ds[0] or " in tab" in ds[0]:
        f.append("'do script' in %d Befehlszeilen (Soll 1, ohne 'in window')" % len(ds))
    f += ["verbotenes Wort: " + w for w in vb] + ["bash-4-Mittel: " + x.strip()[:60] for x in b4]
    if teil == "nachweis":
        f += ["Platzhalter offen: " + x[:50] for x in code if re.match(r'[A-Z_]+="<<', x)]
    if teil != "v4":
        f += ["Logzeile fehlt: " + w for w in LOGTEILE if not any(w in x for x in zl)]
    print("starte_sitzung.sh · %d Zeilen · bash -n rc %d · 'do script' in Befehlszeilen %d · verbotene Woerter %d · bash-4 %d"
          % (len(zl), r.returncode, len(ds), len(vb), len(b4)))
    return f


def waechter(teil, probe, setze):
    print("# TB-142 waechter %s%s — Stuecke aus Anhang A auf %s" % (teil, " (Probe)" if probe else "", SH))
    zl = zeilen(SH)
    ur = list(zl)
    ws = [s for s in stuecke().values() if s["id"][0] == "W" and (s["id"] == "W1") == (teil == "v4")]
    schon = [s["id"] for s in ws if s["text"][0] in zl]
    if schon:
        print("ABGEWIESEN, nichts geschrieben: steht schon in der Datei (zweiter Lauf?): " + " ".join(schon))
        return 2
    for s in ws:
        zl, was = wende_an(zl, s, s["text"], ur)
        print("%s · %s · ok" % (s["id"], was))
    for paar in setze:
        n, v = paar.split("=", 1)
        t = [k for k, x in enumerate(zl) if x.startswith(n + '="') and x.endswith('"')]
        assert n in KONST and len(t) == 1 and v and not re.search(r'["$`\\\n]|<<', v), "setze " + n
        zl[t[0]] = '%s="%s"' % (n, v)
        print("gesetzt · %s · Z. %d" % (n, t[0] + 1))
    fehler = pruefe_sh(zl, teil)
    for x in fehler:
        print("FEHLER, nichts geschrieben · " + x)
    if not fehler and not probe:
        schreibe(SH, zl)
        print("geschrieben · sha256 " + hashlib.sha256(("\n".join(zl) + "\n").encode("utf-8")).hexdigest())
    return 1 if fehler else 0


def werte():
    # Konstanten aus starte_sitzung.sh; M1–M5 und PROBE aus der Messwertdatei (je eine Zeile 'M1: …')
    w, zl = {}, zeilen(SH)
    for n in KONST:
        t = [x for x in zl if x.startswith(n + '="') and x.endswith('"')]
        assert len(t) == 1, "%s steht %d-mal in %s" % (n, len(t), SH)
        w[n] = t[0][len(n) + 2:-1]
    for x in zeilen(MESS):
        m = re.match(r"(M[1-5]|PROBE): (.+)$", x)
        if m:
            assert m.group(1) not in w, m.group(1) + " doppelt"
            w[m.group(1)] = m.group(2).strip()
    for n in ("M1", "M2", "M3", "M4", "M5", "PROBE"):
        assert n in w, n + " fehlt in " + MESS
    for n, v in w.items():
        assert v and "<<" not in v and KL not in v and "|" not in v and len(v) <= 400, n + ": leer, Platzhalter, '|' oder zu lang"
    return w


def fertig(s, w, nur_ueb=False):
    # Platzhalter fuellen; eine Zeile '⟦UEBERGABE: <Anfang> |md5 <12 Zeichen>⟧' kommt unveraendert aus dem Nachtrag 21:47
    aus = []
    for x in s["text"]:
        if x.startswith(KL + "UEBERGABE: "):
            anfang, soll = x[len(KL) + 11:-1].split(" |md5 ")
            zl = zeilen(UEB)
            a = treffer(zl, "## Nachtrag 08.10.2026, 21:47", False)
            assert len(a) == 1, "Nachtrag 21:47 trifft %d-mal" % len(a)
            e = next(k for k in range(a[0] + 1, len(zl)) if zl[k].startswith("## "))
            t = [y for y in zl[a[0]:e] if y.startswith(anfang)]
            assert len(t) == 1 and hashlib.md5(t[0].encode("utf-8")).hexdigest()[:12] == soll, "UEBERGABE-Zeile '%s': %d Treffer oder md5 anders" % (anfang, len(t))
            aus.append(t[0])
        elif not nur_ueb:
            for n, v in w.items():
                x = x.replace(KL + n + KR, v)
            assert KL not in x, s["id"] + ": Platzhalter offen: " + x[:60]
            aus.append(x)
    return aus


def gewaehlt(w):
    # ein Stueck mit Bedingung nur, wenn die Startzeile vom HEAD abweicht
    return [(s, fertig(s, w)) for s in stuecke().values() if s["id"][0] == "E" and not (s["bed"] and w["STARTZEILE"] == START_HEAD)]


def vorkommen(zl, text):
    return sum(1 for k in range(len(zl) - len(text) + 1) if zl[k:k + len(text)] == text)


def doku(probe):
    print("# TB-142 doku%s — Einfuegungen E aus Anhang B" % (" (Probe)" if probe else ""))
    w = werte()
    print("Startzeile: %s · %s" % (w["STARTZEILE"], "wie HEAD" if w["STARTZEILE"] == START_HEAD else "geaendert"))
    wahl, dat, vor = gewaehlt(w), {}, {}
    for s, text in wahl:
        if s["zie"] not in dat:
            dat[s["zie"]] = zeilen(s["zie"])
            vor[s["zie"]] = list(dat[s["zie"]])
    schon = [s["id"] for s, text in wahl if text[0] in dat[s["zie"]]]
    if schon:
        print("ABGEWIESEN, nichts geschrieben: steht schon in der Datei (zweiter Lauf?): " + " ".join(schon))
        return 2
    for s, text in wahl:
        dat[s["zie"]], was = wende_an(dat[s["zie"]], s, text, vor[s["zie"]])
        print("%s · %s · %s · ok" % (s["id"], s["zie"].split("/")[-1], was))
    for s, text in wahl:
        assert vorkommen(dat[s["zie"]], text) == 1, s["id"] + ": Text nachher nicht genau einmal"
    for p in sorted(dat):
        print("Datei %s · Zeilen vorher %d · nachher %d · +%d" % (p, len(vor[p]), len(dat[p]), len(dat[p]) - len(vor[p])))
        if not probe:
            schreibe(p, dat[p])
    print("Gesamt: %d Einfuegungen, %s" % (len(wahl), "nichts geschrieben (Probe)" if probe else "geschrieben, je genau einmal"))
    return 0


def journal(blockpfad, probe):
    print("# TB-142 journal%s — Block der Sitzung samt J1 vor '## Wiederkehrende Lehren'" % (" (Probe)" if probe else ""))
    w, zl, b, st = werte(), zeilen(JOU), zeilen(blockpfad), stuecke()
    j1 = fertig(st["J1"], w) + fertig(st["E11"], w, True)
    k = treffer(zl, "## Wiederkehrende Lehren", True)
    assert len(k) == 1, "Schlussueberschrift trifft %d-mal" % len(k)
    k, was = k[0], "### Was gemessen ist"
    alt = [m.group(1) for m in (re.match(r"## ([A-Z]{2}) — ", x) for x in zl[:k]) if m][-1]
    neu = alt[0] + chr(ord(alt[1]) + 1) if alt[1] != "Z" else chr(ord(alt[0]) + 1) + "A"
    g = b.index(was) if was in b else 0
    bed = (("letzte Kennung %s, Kopfzeile beginnt mit '## %s — TB-142'" % (alt, neu), b[0].startswith("## %s — TB-142" % neu)),
           ("genau eine Zeile '%s', Leerzeile davor" % was, b.count(was) == 1 and g > 0 and b[g - 1] == ""),
           ("genau eine Zeile '### Was offen bleibt'", b.count("### Was offen bleibt") == 1),
           ("kein Trennstrich im Block, Schlusszeile beginnt mit '*Geschrieben'", "---" not in b and b[-1].startswith("*Geschrieben")),
           ("J1 weder im Journal noch im Block", j1[0] not in zl and j1[0] not in b),
           ("vor der Schlussueberschrift stehen '---' und eine Leerzeile", zl[k - 2:k] == ["---", ""]))
    for name, ok in bed:
        print("%s · %s" % (name, "ja" if ok else "NEIN"))
    if not all(ok for name, ok in bed):
        print("ABGEWIESEN, nichts geschrieben")
        return 2
    ein = b[:g] + j1 + [""] + b[g:] + ["", "---", ""]
    print("Kennung %s · Blockzeilen %d · J1-Zeilen %d · Zeilen +%d (= Block + J1 + 1 + 3)" % (neu, len(b), len(j1), len(ein)))
    if not probe:
        schreibe(JOU, zl[:k] + ein + zl[k:])
    return 0


def nachweis():
    print("# TB-142 nachweis — Zustand der Zieldateien gegen den Auftrag")
    zl, w, lies = zeilen(SH), werte(), zeilen(LIES)
    f = pruefe_sh(zl, "nachweis") + ["Logzeile fehlt in LIESMICH: " + t for t in LOGTEILE if not any(t in x for x in lies)]
    for n in KONST:
        print("Konstante %s = %s" % (n, w[n]))
    for s in stuecke().values():
        if s["id"][0] == "W" and s["id"] != "W1":
            anders = [x for x in s["text"] if x not in zl]
            print("%s · %d von %d Zeilen woertlich in der Datei%s" % (s["id"], len(s["text"]) - len(anders), len(s["text"]), "".join("\n   anders: " + x[:90] for x in anders)))
    for s, text in gewaehlt(w):
        n = vorkommen(zeilen(s["zie"]), text)
        f += [] if n == 1 else [s["id"] + ": Vorkommen %d" % n]
        print("%s · %s · Vorkommen %d · %s" % (s["id"], s["zie"].split("/")[-1], n, "GLEICH" if n == 1 else "ABWEICHUNG"))
    for x in f:
        print("FEHLER · " + x)
    print("Gesamt: " + ("ABWEICHUNG" if f else "wie Soll"))
    return 1 if f else 0


def main(a):
    probe = "--probe" in a
    if a[:1] == ["waechter"] and a[1:2] in (["v4"], ["bau"]):
        return waechter(a[1], probe, [x for x in a[2:] if "=" in x])
    if a[:1] == ["doku"]:
        return doku(probe)
    if a[:1] == ["journal"] and len(a) >= 2:
        return journal(a[1], probe)
    if a[:1] == ["nachweis"]:
        return nachweis()
    print("Aufruf: waechter v4|bau [NAME=WERT …] [--probe] | doku [--probe] | journal <Blockdatei> [--probe] | nachweis")
    return 64


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except AssertionError as fehler:
        print("ABBRUCH, nichts geschrieben · " + str(fehler))
        sys.exit(3)
