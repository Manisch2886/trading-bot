#!/usr/bin/env python3
"""TB-178 Werkzeug (Anhang A): Fable 17d und 17e ins Register (Abschnitt 69 = R109, Abschnitt 70 = R110, je zeichengleich, Marken nach R109 (c)
und R110 (d), 69.2 und 70.2); Index, Handfelder; Voraussetzungen, Nachher-Pruefung der Probe (P), Kennung, BACKLOG, Journal.
Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  md5 | voraussetzung | register <DATUM> <S0> <BELEG> [--probe] | index <S0> <DATUM> [--probe] | handfelder <ZIEL> | nachher | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, json, os, re, subprocess, sys
P = "docs/projektfuehrung/"
JO, BL, BEL = P + "JOURNAL.md", P + "BACKLOG.md", "docs/belege/TB-178/"
REG, IDX, DI = "docs/VORREGISTRIERUNG_neuselektion.md", P + "REGISTER_INDEX.md", P + "FABLE_DIALOG_INDEX.md"
AUF = "docs/auftraege/MAC_TB-178_register69_70_fable17d17e_spaetes_symbol.md"
QU = {"17d": "data_sicherung/steuernder_chat_tmp/f17d/", "17e": "data_sicherung/steuernder_chat_tmp/f17e/"}
FA = {"17d": P + "FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md", "17e": P + "FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md"}
FQ = {"17d": P + "FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md", "17e": P + "FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md"}
FU = {"17d": P + "FABLE_UEBERGABE_2026-10-17d_eroeffnung.md", "17e": P + "FABLE_UEBERGABE_2026-10-17e_eroeffnung.md"}
DATEIEN = [(d, f) for d in ("17d", "17e") for f in (FQ[d], FA[d], FU[d])]
MD5F = {"docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md": "007196934a22163335439c2888886047", "docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md": "3b886ee769174d7c474679dd4452c9eb", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md": "b968fc124c5361f03e0f1118fdec1994", "docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md": "36389b7829a6e77c3ebe327fc58b7d25", "docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md": "1d964b3107485a44ba29467ebc56c34a", "docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md": "a204bed16a9f30adda7c2b34489856ba"}
CODE = {"research/tb24_haltedauern/test_listen_erzeuger.py": "d77e73ed5ff7a737a22e53879ff72575", "research/tb24_haltedauern/positionen_holen.py": "006375593b4bad4465e22dd3b4268bdd", "research/tb24_haltedauern/haltedauer_kern.py": "60942de99b323fa472ae25478a5a6836", "research/exposure_messung/bot_lauf.py": "01fd9282ded2ccca6fbb1e95edafc101", "research/faltenplan_neun/faltenschranke_messung.py": "584d9ff959dab7428a97a945b091e118", "strategies/t3_supertrend/multi_symbol_optimise.py": "dc85993e8d42647dea2eb2593335aab8", "strategies/elliott_wave/multi_symbol_optimise.py": "bf11370b140d3e61488ad81599b45b37", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "571076168d56f9e809ef0595f53d6e7d"}
PROBE, PSHA = BEL + "tb178_probe_spaetes_symbol.py", "1fe6f12ef5f47603743524f5567cbf84f8edae81c459349d6284a1eeafe0fa88"
KOPF_A = {"17d": "## Registerblock — zeichengleich kopierbar, nummeriert (ab R109)", "17e": "## Registerblock — zeichengleich kopierbar (ab R110)"}
RN = {"17d": "R109", "17e": "R110"}; NR = {"17d": "69", "17e": "70"}
TITEL = {"17d": "## 69. Fable 17d — Registerblock R109 (TB-178)", "17e": "## 70. Fable 17e — Registerblock R110 (TB-178)"}
RANG1 = "| **1** | **TB-30b Mass-Reparatur**"
ZG = "> Eintrag und Stand oben bleiben zeichengleich."
TLE = "research/tb24_haltedauern/test_listen_erzeuger.py"
# (Ort, Anfang des Unterabschnitts, Einfuegestelle: quelle | ende, Kopf der Marke, Zusatz); vorhandene Marken-Tripel am Ort werden uebersprungen
MARKEN = {"17d": [("68.1", "### 68.1 ", "quelle", "68.1 R108 BERICHTIGT und ERGÄNZT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (a): BERICHTIGT („lies“); Unterpunkte (a) und (b): ERGÄNZT"),
                  ("29.3", "### 29.3 ", "ende", "29.3 ERGÄNZT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (a)"),
                  ("66.1", "### 66.1 ", "quelle", "66.1 R106 BERICHTIGT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (b) („lies“)"),
                  ("67.1", "### 67.1 ", "quelle", "67.1 R107 ERGÄNZT durch R109 (69.1)", "Fable 17d R109, Unterpunkt (b)")],
          "17e": [("69.1", "### 69.1 ", "quelle", "69.1 R109 BERICHTIGT und ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkte (a) und (b): BERICHTIGT („lies“); Unterpunkte (a) bis (c): ERGÄNZT"),
                  ("66.1", "### 66.1 ", "quelle", "66.1 R106 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (a)"),
                  ("37.2", "### 37.2 ", "ende", "37.2 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)"),
                  ("37.5", "### 37.5 ", "ende", "37.5 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)"),
                  ("29.3", "### 29.3 ", "ende", "29.3 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)"),
                  ("38.5", "### 38.5 ", "ende", "38.5 ERGÄNZT durch R110 (70.1)", "Fable 17e R110, Unterpunkt (b)")]}
OHNE = {"17d": "59.1, 29.2, 24.6, 37.3, 37.5, 38.5, 23.5, 56.3 (R86), 56.4 (R87), 57.1 (R90), 65.2 (R105), 66.2, 67.2, Abschnitt 10",
        "17e": "36.1, 37.1, 37.3, 37.6, 38.4, 56.4, 64.1, 67.1, 68.2, Abschnitt 10 (Indexzeile Punkt 9)"}
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def info(t): OUT.append("info  " + t)
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def md5f(f): return hashlib.md5(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest() if os.path.exists(f) else None
def ende():
    print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (sum(not l.startswith("info") for l in OUT), sum(l.startswith("NEIN") for l in OUT))); sys.exit(1 if nein() else 0)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True)
def verfolgt_gleich(f):
    r = git("show", "HEAD:" + f); return r.returncode == 0 and os.path.exists(f) and r.stdout == open(f, "rb").read()
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def beleg(n): return lies(BEL + n).rstrip("\n").split("\n") if os.path.exists(BEL + n) else [""]
def block(d):
    """((R-Zeile, Quellenzeile), Z. Zaun auf, Z. Zaun zu) oder None."""
    f = FA[d]; z = lies(f if os.path.exists(f) else QU[d] + os.path.basename(f)).split("\n")
    if z.count(KOPF_A[d]) != 1: return None
    a = z.index(KOPF_A[d]) + 1
    while a < len(z) and z[a] == "": a += 1
    if a >= len(z) or z[a] != "```": return None
    e = z.index("```", a + 1); b = [z[i] for i in range(a + 1, e) if z[i]]; soll = [RN[d] + " — ", "Quelle des Grundes: "]
    if len(b) != 2 or [l[:len(s)] for l, s in zip(b, soll)] != soll: return None
    return (b[0], b[1]), a + 1, e + 1
def unterabschnitt(z, anfang):
    a = [i for i, l in enumerate(z) if l.startswith(anfang)]
    if len(a) != 1: return None, None
    return a[0], next((i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ") or z[i].startswith("### ")), len(z))
def einfuege(z, m, frei):
    """Index der Einfuegestelle (vor dieser Zeile) oder None."""
    a, e = unterabschnitt(z, m[1])
    if a is None or any(re.search(r"\b%s\b" % frei, z[i]) for i in range(a, e)): return None
    if m[2] == "quelle": k = [i for i in range(a, e) if z[i].startswith("> Quelle des Grundes")]
    else:
        j = e - 1
        while j > a and z[j] in ("", "---"): j -= 1
        k = [j] if j > a else []
    if len(k) != 1: return None
    k = k[0]
    while k + 3 < e and z[k + 1] == "" and z[k + 2].startswith("> ⭐ ") and z[k + 3] == ZG: k += 3
    return k + 1
def markenzeilen(kopf, zusatz, datum): return ["", "> ⭐ **%s** (%s, TB-178, %s)." % (kopf, zusatz, datum), ZG]
def mess_b():
    """R109 (b), Voraussetzung (nur das Wie): woher TB-169 3b den Tag des spaeten Symbols nimmt - Zeilen in test_listen_erzeuger.py."""
    t = lies(TLE).split("\n") if os.path.exists(TLE) else []
    u = [i + 1 for i, l in enumerate(t) if "x.update(t)" in l and "def hb" in t[i - 1]]
    c = [i + 1 for i, l in enumerate(t) if 'json.dumps({"CCC": str(c0["entry_time"].min().date())})' in l]
    return u, c
def code_gleich():
    for f, m in sorted(CODE.items()): p(md5f(f) == m, "unveraendert: %s md5 %s" % (f, m[:12]))
def voraussetzung():
    code_gleich()
    z = [l for l in lies(BL).split("\n") if l.startswith(RANG1)]
    p(len(z) == 1 and z[0].endswith(" |") and "TB-178" not in z[0], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-178")
    k = kennungen(); p(max(k) in ("FN", "FO"), "Journal: hoechste %s (FN am Bau-HEAD)" % max(k))
    for d, f in DATEIEN: p(verfolgt_gleich(f) and md5f(f) == MD5F[f], "R56 (b)/S0-Datei: %s verfolgt, gleich HEAD, md5 %s" % (f, MD5F[f]))
    for d in ("17d", "17e"):
        b = block(d); p(b is not None, "Registerblock %s: genau %s und Quelle im Codeblock (Z. %s)" % (d, RN[d], "%d–%d" % (b[1], b[2]) if b else "?"))
    reg = lies(REG); z = reg.split("\n")
    p(sum(l.startswith("## 68. ") for l in z) == 1 and not any(l.startswith("## 69. ") or l.startswith("## 70. ") for l in z) and not re.search(r"\bR109\b|\bR110\b", reg), "Register: 68 da, 69 und 70 nicht; R109/R110 0 Treffer")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    for d in ("17d", "17e"):
        for m in MARKEN[d]:
            if m[0] == "69.1": continue
            i = einfuege(z, m, RN[d]); p(i is not None, "Ort %s (%s): Einfuegestelle vor Z. %s eindeutig, %s dort noch nicht genannt" % (m[0], RN[d], i + 1 if i else "?", RN[d]))
    zi = lies(IDX).split("\n"); k = [i for i, l in enumerate(zi) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    p(len(k) == 1 and "Abschnitte 0–68" in zi[k[0]], "Index-Kopf Z. %s nennt 0–68" % (k[0] + 1 if k else "?"))
    p(sum(l.startswith("| 68 aus 17c |") for l in zi) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-176a (") for l in zi) == 1 and sum(l.startswith("**Pflege:**") for l in zi) == 1
      and sum(l.startswith("## 19. ") for l in zi) == 1 and not any(l.startswith("## 20. ") for l in zi), "Index: Zeile 68, Pflegezeile TB-176a, Pflege-Anker, Abschnitt 19 je genau einmal; kein Abschnitt 20")
    dl = lies(DI).split("\n"); p(not any(l.startswith("| 17d |") or l.startswith("| 17e |") for l in dl), "Dialog-Index: 17d und 17e noch nicht")
    u, c = mess_b(); p(len(u) == 1 and len(c) == 1, "R109 (b) Voraussetzung lesbar: %s hb() und Pruefung 3b je genau eine Zeile" % TLE)
    info("R109 (b) Voraussetzung (Messung, kein Urteil; R110 (a): gesetzt): %s Z. %s `x.update(t)` in hb() - die vom Test uebergebenen Tage ueberschreiben die Rechnung; Z. %s Pruefung 3b setzt den Tag von CCC (`json.dumps({\"CCC\": ...})`)" % (TLE, u, c))
    p(not os.path.exists(PROBE), "Probe noch nicht im Repo (%s)" % PROBE)
    ende()
def md5cmd():
    for d, f in DATEIEN: p(md5f(QU[d] + os.path.basename(f)) == MD5F[f] and md5f(f) == MD5F[f], "md5 vorher %s = nachher %s = %s" % (QU[d] + os.path.basename(f), f, MD5F[f]))
    ende()
def karte():
    z = lies(AUF).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]
    if len(a) != 1: return None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
    return k[0][2:].strip() if len(k) == 1 and ("⟨⟨" + "FREIGABE") not in k[0] else None
def titel(t):
    t = t.split(". (a) ")[0]; t = t[:-1] if t.endswith(".") else t
    return t[:139].rsplit(" ", 1)[0] + "…" if len(t) > 140 else t
def abschnitt(d, s0, k, datum, b, beleg_v, vb):
    (r, q), za, ze = b; n = NR[d]
    kopf = ("Reines Eintragen von Registertext, Bauart wie 67 und 68. Quelle ist allein `%s`, md5 `%s`, %s B, Abschnitt „%s“, Z. %d–%d, im Repo seit Commit `%s`. "
            "Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.%s (`%s`) und die Übergabe 17.10.%s (`%s`), beide seit `%s`. "
            "Marken nach %s. Karte des Betreibers (Auftrag TB-178, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-178.") % (
            FA[d], MD5F[FA[d]], format(os.path.getsize(FA[d]), ",").replace(",", " "), KOPF_A[d][3:], za, ze, s0, d[-1], FQ[d], d[-1], FU[d], s0, "R109 (c)" if d == "17d" else "R110 (d)", k, datum)
    if d == "17d":
        u, c = mess_b()
        kette = ("**Kette:** Marken nach R109 (c): 68.1 (R108), Unterpunkt (a) berichtigt, Unterpunkte (a) und (b) ergänzt; 29.3, Unterpunkt (a); 66.1 (R106), Unterpunkt (b), berichtigt; 67.1 (R107), Unterpunkt (b). "
                 "Ohne Marke: " + OHNE[d] + ". Zählung: kein Fall; sechzehn (R109 (b)).")
        mitte = ["### 69.2 Voraussetzungen und Befunde", "", "Gemessen vor dem Eintrag mit `%s` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-178), Zeilen wörtlich:" % beleg_v, ""] + ["    " + l for l in vb] + ["",
            ("(a) R109 (b), Voraussetzung (nur das Wie), gemessen durch Lesen am Commit `%s`: `%s` setzt den Tag selbst — `hb()` überschreibt die Rechnung mit den vom Test übergebenen Tagen (`x.update(t)`, Z. %s), "
             "Prüfung 3b übergibt den Tag von CCC (Z. %s). Ergebnis: gesetzt; so eingetragen in R110 (a) (70.1).") % (s0, TLE, ", ".join(map(str, u)), ", ".join(map(str, c))), "",
            "(b) R109 (a): Der Registertext zu 29.3 wird mit TB-178 nicht eingetragen; er folgt dem Bauauftrag nach 37.3 aus R110 (b) (70.1) in der dort berichtigten Fassung.", "",
            "(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.d liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `%s0a_md5.txt`)." % (s0, QU[d], BEL), ""]
    else:
        kette = ("**Kette:** Marken nach R110 (d): 69.1 (R109), Unterpunkte (a) und (b) berichtigt, (a) bis (c) ergänzt; 66.1 (R106), Unterpunkt (a); 37.2, 37.5, 29.3 und 38.5, Unterpunkt (b). "
                 "Ohne Marke: " + OHNE[d] + ". Zählung: kein Fall; sechzehn (R110).")
        mitte = ["### 70.2 Voraussetzungen und Befunde", "", "Voraussetzungen: dieselbe Messung wie 69.2 (`%s`)." % beleg_v, "",
            "(a) R110 (a): Die Abnahme am Erzeuger (Probe mit sha256 im Repo, 6 von 6 je Bot, Gegenprobe beide Seiten) folgt in TB-178 nach diesem Eintrag (Schritt P); ihr Ergebnis steht im Ergebnis TB-178, nicht hier. Bis dahin offen.", "",
            "(b) R110 (b) und (c): Der Bauauftrag nach 37.3 (Nachtrag zu Punkt 9, Konstante, neues Abbild, Ergänzung zu 29.3) und die Probe in `shared/test_ergebniskurven.py` sind Handelscode und nicht Teil von TB-178.", "",
            "(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.e liegen seit `%s` im Repo (aus `%s`, md5 vorher = nachher, `%s0a_md5.txt`)." % (s0, QU[d], BEL), ""]
    return ["", TITEL[d], "", kopf, "", "### %s.1 " % n + titel(r), "", "> " + r, "> " + q, "", kette, ""] + mitte
def register(datum, s0, beleg_v, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0): sys.exit(2)
    alt = lies(REG); z = alt.split("\n"); va = lies(beleg_v).rstrip("\n").split("\n"); vb = va[:-1]
    p(va[-1] == "rc 0" and vb[-1].endswith(", NEIN: 0") and not any(l.startswith("NEIN") for l in vb), "Beleg der Voraussetzung: rc 0, ohne NEIN (%s)" % beleg_v)
    bb = {d: block(d) for d in ("17d", "17e")}
    for d in bb: p(bb[d] is not None and md5f(FA[d]) == MD5F[FA[d]], "Quelle %s md5 %s, Registerblock %s" % (d, MD5F[FA[d]], RN[d]))
    p(not any(l.startswith("## 69. ") or l.startswith("## 70. ") for l in z) and z[-1] == "" and z[-2] != "", "69 und 70 noch nicht im Register; endet mit einer Leerzeile")
    k = karte(); p(k is not None, "Karte TB-178 gefuellt (Abschnitt Freigabe des Auftrags)")
    if nein(): ende()
    neu = {}; ganz = z
    for d in ("17d", "17e"):
        einf = [(einfuege(ganz, m, RN[d]), m) for m in MARKEN[d]]
        if not p(all(i is not None for i, _ in einf) and len(set(i for i, _ in einf)) == len(einf), "%s: %d Einfuegestellen eindeutig (%s)" % (RN[d], len(einf), ", ".join("%s vor Z. %s" % (m[0], i and i + 1) for i, m in einf))): ende()
        for i, m in sorted(einf, key=lambda x: -x[0]): ganz[i:i] = markenzeilen(m[3], m[4], datum)
        neu[d] = abschnitt(d, s0, k, datum, bb[d], beleg_v, vb); ganz = ganz[:-1] + neu[d]
    if probe: print("\n".join(neu["17d"] + neu["17e"])); ende()
    schreibe(REG, "\n".join(ganz))
    r2 = lies(REG).split("\n"); alle = MARKEN["17d"] + MARKEN["17e"]
    mz = [(m, [i + 1 for i, l in enumerate(r2) if l.startswith("> ⭐ **%s** (" % m[3])]) for m in alle]
    json.dump({"marken": [[m[0], m[3], (n or [0])[0]] for m, n in mz], "abschnitt_69": r2.index(TITEL["17d"]) + 1, "abschnitt_70": r2.index(TITEL["17e"]) + 1},
              open(os.path.dirname(beleg_v) + "/r_daten.json", "w"), ensure_ascii=False)
    p(all(len(n) == 1 for _m, n in mz), "nachher: %d Marken Z. %s; Abschnitt 69 Z. %d, 70 Z. %d" % (len(alle), sorted(x for _m, n in mz for x in n), r2.index(TITEL["17d"]) + 1, r2.index(TITEL["17e"]) + 1))
    for d in ("17d", "17e"):
        (r, q), _a, _e = bb[d]; p(r2.count("> " + r) == 1 and r2.count("> " + q) == 1, "%s mit Quellenzeile je genau einmal zeichengleich (Zeichenvergleich mit dem Codeblock)" % RN[d])
    weg = set(x for _m, v in mz for n in v for x in (n - 1, n, n + 1)); r3 = [l for i, l in enumerate(r2) if i + 1 not in weg]
    al = alt.split("\n")[:-1]; soll = al + neu["17d"][:-1] + neu["17e"]
    p(r3 == soll, "Register append-only bis auf die %d Marken (je Leerzeile, Marke, Zeichengleich-Zeile)" % len(alle))
    ende()
def index(s0, datum, probe):
    d = json.load(open(BEL + "r_daten.json", encoding="utf-8")); mk = d["marken"]; alle = MARKEN["17d"] + MARKEN["17e"]
    tl = {}
    for n in ("69", "70"):
        tl[n] = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t) and ("\n## %s. " % n) in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]
    p(all(len(v) == 1 for v in tl.values()) and len(mk) == len(alle) and all(m[2] for m in mk), "Abschnitte 69 und 70 in je genau einer Teildatei: %s; %d Marken mit Zeile" % (tl, len(mk)))
    T = {n: (str(v[0]) if len(v) == 1 else "?") for n, v in tl.items()}
    z = lies(IDX).split("\n"); k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]; rcm = git("rev-parse", "--short", "HEAD").stdout.decode().strip()
    if p(len(k) == 1 and "Abschnitte 0–68" in z[k[0]], "Kopf genau einmal, nennt 0–68"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–68", "Abschnitte 0–70")
    i = [j for j, l in enumerate(z) if l.startswith("| 68 aus 17c |")]
    if p(len(i) == 1, "Zeile 68 genau einmal"):
        z[i[0] + 1:i[0] + 1] = ["| 69 aus 17d | %s | R109 (69.1); 69.2 Voraussetzungen und Befunde | – |" % T["69"], "| 70 aus 17e | %s | R110 (70.1); 70.2 Voraussetzungen und Befunde | – |" % T["70"]]
    tab = ["---", "", "## 20. Die Marken aus Fable 17d und 17e (TB-178)", "", "Alle %d Marken, die TB-178 nach R109 (c) und R110 (d) im Register gesetzt hat, in der Reihenfolge des Registers; Zeilen aus `docs/belege/TB-178/r_daten.json`." % len(mk), "",
           "| Ort | Marke | Kopf | T |", "|---|---|---|---|"] + ["| %s | Z. %d | %s | %s |" % (o, n, kp, "?") for o, kp, n in sorted(mk, key=lambda m: m[2])] + ["", "Der Index ist kein Registertext.", ""]
    tt = [t for t in range(1, 10) if os.path.exists(P + "REGISTER_KOPIE_teil%d.md" % t)]
    for j, row in enumerate(tab):
        m = re.match(r"\| (\S+) \| Z\. (\d+) \| (.*) \| \? \|$", row)
        if m:
            hit = [t for t in tt if ("> ⭐ **%s** (" % m.group(3)) in lies(P + "REGISTER_KOPIE_teil%d.md" % t)]; tab[j] = row[:-3] + ("%s |" % hit[0] if len(hit) == 1 else "? |")
    p(not any(r.endswith("| ? |") for r in tab), "jede Marke in genau einer Teildatei")
    i = [j for j, l in enumerate(z) if l.startswith("**Pflege:**")]
    if p(len(i) == 1 and z[i[0] - 1] == "" and not any(l.startswith("## 20. ") for l in z), "Pflege-Anker genau einmal, davor Leerzeile; kein Abschnitt 20"):
        j = i[0] - 1
        while z[j] == "": j -= 1
        z[j + 1:j + 1] = [""] + tab
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-176a (")]
    if p(len(j) == 1, "Pflegezeile TB-176a genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-176a (", "In TB-176a (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-178 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-178 (`index`); 69 (R109) kommt zu T%s, 70 (R110) zu T%s; neuer Abschnitt 20 (%d Marken)." % (datum, s0, rcm, T["69"], T["70"], len(mk)))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def handfelder(ziel):
    f = lambda d: lies(FQ[d]).split("\n")[0].split(" — ", 1)[-1].strip()
    json.dump({"17d": {"frage": f("17d"), "entscheidung": "(a) anders: 59.1 ist Beleg, kein Ort; Registertext zu 29.3 nach der Tatsachennotiz mit neun Fundstellen; Ort im Modul aus 38.5 (R109 (a)); (b) anders bei der Fallwahl: später Symbolfall wird gebaut, Tag aus der Rechnung nach 23.5; Voraussetzung zu 3b zu messen (R109 (b))", "offen": "ja"},
               "17e": {"frage": f("17e"), "entscheidung": "(a) einverstanden: 3b setzt den Tag, alle drei Bots am gebauten Fall, Abnahme am Erzeuger; (b) anders: Pfad zuerst ins Register (Nachtrag zu Punkt 9 nach 38.5), Bauauftrag nach 37.3 in vier Schritten, Sonde bis zum Tag 2 mit Tatsachennotiz; (c) einverstanden: test_ergebniskurven.py Handwerk in der Freigabe (R110)", "offen": "ja"}},
              open(ziel, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Handfelder 17d, 17e geschrieben: %s" % ziel)
def nachher():
    code_gleich()
    p(sha(PROBE) == PSHA, "Probe im Repo = Anhang B (sha256 %s)" % PSHA[:16])
    pr = beleg("p_probe.txt"); n = [l for l in pr if l.startswith("ja    ") or l.startswith("NEIN  ")]
    for b in ("t3_supertrend", "elliott_wave", "elliott_wave_stocks"):
        nb = [l for l in n if l[6:].startswith(b + ": ")]; p(len(nb) == 6 and all(l.startswith("ja") for l in nb), "R110 (a) %s: %d von 6 (Abnahme am Erzeuger)" % (b, sum(l.startswith("ja") for l in nb)))
    p(any(l.startswith("Zaehlzeile Gegenprobe") for l in pr) and pr[-2:] == ["Ergebnis: 18 von 18 bestanden", "rc 0"], "p_probe.txt: 18 von 18, rc 0; Gegenprobe beide Seiten mit Zaehlzeile")
    ende()
BL_TEXT = (" · **Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110) mit TB-178 (%s, Journal %s)**: R109 (a) 59.1 ist Beleg, kein Ort; R110 (b) Ort ist `STARTING_CAPITAL` in `shared/handelskosten.py`, sobald das Modul "
    "als Nachtrag zu Punkt 9 mit Pfad und Hash auf der Sperrliste steht; **offen: Bauauftrag nach 37.3 in vier Schritten und die Probe in `shared/test_ergebniskurven.py` (R110 (b), (c); Handelscode, Vorschlag TB-180)**; "
    "R110 (a) später Symbolfall: Abnahme am Erzeuger mit TB-178 (Probe `docs/belege/TB-178/tb178_probe_spaetes_symbol.py`, Ergebnis siehe `p_probe.txt`) |")
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(" |") and "TB-178" not in z[a[0]], "BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-178"):
        z[a[0]] = z[a[0]][:-2] + BL_TEXT % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-178: " % neu), "Kopfzeile ## %s — TB-178: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["md5"]: md5cmd()
    elif a == ["voraussetzung"]: voraussetzung()
    elif len(a) == 4 and a[0] == "register": register(a[1], a[2], a[3], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "handfelder": handfelder(a[1])
    elif a == ["nachher"]: nachher()
    elif a == ["kennung"]: k = kennungen(); print("Kennung %s (hoechste %s)" % (naechste(max(k)), max(k)))
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
