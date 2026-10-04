#!/usr/bin/env python3
"""TB-132 A4: Register-Abschnitt 53 anhaengen (R66-R73 zeichengleich, Text des steuernden Chats 53.0, 53.9
und 53.10) und die 21 Marken aus Anhang A am alten Ort setzen. Nur Einfuegungen: keine bestehende Zeile
aendert sich, keine faellt weg.

Bauart docs/belege/TB-130/a4_eintrag.py. Alle Texte werden EINGESETZT, nicht abgetippt:
  - Kopf 53.0 und Schluss 53.9-53.10: die beiden ````-Zaeune im Auftrag nach "Kopf:" bzw. "Schluss:" (A3);
  - Ueberschriften, Ketten, Marken und die Angaben zur Quelle: der Daten-Block (JSON) aus Anhang A;
  - R-Bloecke: die Antwortdatei, Zeilen von..bis, Schnittregel des Auftrags (Beginn 'R<n> — ', Ende
    einschliesslich der ersten Zeile 'Quelle des Grundes:').
Ersetzt wird im Text des steuernden Chats nur ⟨S0⟩ -> `<S0>` (Kurzhash in Backticks). Das Datum des Eintrags
steht fest im Auftrag.

Zwei Wachen vor jedem Lauf ohne --vorschau (echter Lauf und Probelauf an einer Kopie):
  - Datum: Der Rechner zeigt das Datum aus dem Daten-Block (Feld "datum"); an jedem anderen Tag wird nichts
    geschrieben.
  - Probe (Schritt 0e; R71: "weicht sie ab, wird gemeldet, nicht eingetragen"): Die Ausgabe der Probe
    (Daten-Block, probe.ausgabe) ist vorhanden, ihre Zeile 3 lautet genau wie probe.kopfzeile_3, und ab der
    Zeile, die mit "A - Faelle" beginnt, ist sie zeilengleich mit der Vergleichsdatei (probe.vergleich, md5 wie
    im Daten-Block). Sonst wird nichts geschrieben.

Der Auftrag und die Antwortdatei werden als Dateien gelesen. Die Sitzung stellt vorher sicher, dass beide
dem Commit von Schritt 0 gleichen (git diff --quiet <S0> -- <auftrag> <quelle>, rc 0).

Marken: je Marke Leerzeile + zwei Markenzeilen nach der Einfuegestelle (Zeilennummer am Original); mehrere
an derselben Stelle in der Reihenfolge des Daten-Blocks (dort nach R aufsteigend, dann nach Nummer).

Wachen: sha256 und Zeilenzahl des Eingangs; '## 53.' noch nicht vergeben; keine Zeile beginnt mit
'> R66 — '; jeder Anker genau einmal, vorher und nachher; jede alte Zeile in derselben Reihenfolge;
Abschnitt 9 und 10 und der ERZEUGT-Block unveraendert; genau 21 neue Markenzeilen, keine doppelt.

Aufruf aus der Repo-Wurzel (Python 3.9, nur Standardbibliothek):
  Probelauf:  trading-env/bin/python3 docs/belege/TB-132/a4_eintrag.py --s0 <S0> --register <kopie>
  echt:       trading-env/bin/python3 docs/belege/TB-132/a4_eintrag.py --s0 <S0>
  weitere:    --auftrag <pfad>   (Standard docs/auftraege/MAC_TB-132_register_fable_02c.md)
              --wurzel <ordner>  (Standard "."; davor stehen Quelle und, ohne --register, das Register)
              --daten <pfad>     (schreibt die gesetzten Marken mit Zeile nachher als JSON)
              --vorschau         (nur fuer den Soll-Bau des steuernden Chats, der Auftrag benutzt das nicht:
                                  ohne die zwei Wachen Datum und Probe; ohne --s0 bleibt `⟨S0⟩` stehen,
                                  mit --s0 <S0> wird der Kurzhash eingesetzt. Nur zusammen mit
                                  --register <Pfad einer Kopie>: Zeigt der Pfad (nach realpath) auf das
                                  echte Register docs/VORREGISTRIERUNG_neuselektion.md im Repo, wird
                                  verweigert; im Vorschau-Modus wird das Register des Repos nie geschrieben)
Rueckgabewert 0 = geschrieben; jede verletzte Wache bricht mit AssertionError ab, bevor geschrieben wird.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

AUFTRAG = "docs/auftraege/MAC_TB-132_register_fable_02c.md"
M2 = "> Eintrag und Stand oben bleiben zeichengleich."


def zaun(text, ab):
    """Inhalt des ersten ````-Zauns nach der Zeile, die genau `ab` ist."""
    z = text.split("\n")
    assert z.count(ab) == 1, ("Zeile nicht genau einmal", ab, z.count(ab))
    i = z.index(ab)
    a = next(k for k in range(i + 1, len(z)) if z[k] == "````")
    b = next(k for k in range(a + 1, len(z)) if z[k] == "````")
    return "\n".join(z[a + 1:b])


def bloecke(wurzel, q, erster, letzter):
    roh = open(os.path.join(wurzel, q["pfad"]), "rb").read()
    assert hashlib.md5(roh).hexdigest() == q["md5"], "Quelle: md5 weicht ab"
    assert len(roh) == q["bytes"], "Quelle: Bytes weichen ab"
    z = roh.decode("utf-8").split("\n")
    bl, cur = {}, None
    for i in range(q["von"], q["bis"] + 1):
        s = z[i - 1]
        m = re.match(r"^R(\d+) — ", s)
        if m:
            assert cur is None, ("Block ohne Ende", i)
            cur = int(m.group(1))
            assert cur not in bl, ("Dopplung", cur)
            bl[cur] = [s]
            continue
        if cur is not None:
            bl[cur].append(s)
            if s.startswith("Quelle des Grundes:"):
                cur = None
        else:
            assert s.strip() == "", ("Zeile ausserhalb eines Blocks", i, s[:60])
    assert cur is None
    assert sorted(bl) == list(range(erster, letzter + 1)), sorted(bl)
    assert all(len(v) == 2 and v[1].endswith("Kein Ergebnis.") for v in bl.values())
    return bl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--auftrag", default=AUFTRAG)
    ap.add_argument("--wurzel", default=".")
    ap.add_argument("--register")
    ap.add_argument("--s0")
    ap.add_argument("--daten")
    ap.add_argument("--vorschau", action="store_true")
    a = ap.parse_args()
    assert a.vorschau or a.s0, "--s0 <7 Hexzeichen> fehlt"
    assert a.s0 is None or re.match(r"^[0-9a-f]{7}$", a.s0), "--s0 <7 Hexzeichen> erwartet"
    s0 = "`%s`" % (a.s0 or "⟨S0⟩")

    auftrag = open(a.auftrag, encoding="utf-8").read()
    daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
    abschnitt = daten["abschnitt"]
    marken = daten["marken"]
    ueber = daten["ueberschriften"]
    erster, letzter = ueber[0]["R"], ueber[-1]["R"]
    assert len(marken) == daten["marken_zahl"] == 21
    assert [m["nr"] for m in marken] == list(range(1, len(marken) + 1))
    assert [u["R"] for u in ueber] == list(range(erster, letzter + 1))
    reg_pfad = a.register or os.path.join(a.wurzel, daten["register"])

    def git(ordner, *arg):
        try:
            r = subprocess.run(["git", "-C", ordner] + list(arg), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        except OSError:
            return 127, ""
        return r.returncode, r.stdout.strip()

    # Vorschau: nur an einer Kopie, nie am Register eines Repos (Pfadvergleich nach realpath)
    if a.vorschau:
        assert a.register, "--vorschau nur zusammen mit --register <Pfad einer Kopie>"
        ziel = os.path.realpath(a.register)
        for echt in (os.path.join(a.wurzel, daten["register"]), daten["register"]):
            assert ziel != os.path.realpath(echt), "--vorschau schreibt nicht in das Register des Repos: " + a.register
        rc, oben = git(os.path.dirname(ziel), "rev-parse", "--show-toplevel")
        if rc == 0 and oben:
            assert os.path.relpath(ziel, os.path.realpath(oben)) != daten["register"], \
                "--vorschau schreibt nicht in das Register eines Repos: " + a.register

    # Wachen Datum und Probe (nicht im Vorschau-Modus)
    if not a.vorschau:
        heute = datetime.date.today().strftime("%d.%m.%Y")
        assert heute == daten["datum"], "Datum ist %s, eingetragen wird nur am %s" % (heute, daten["datum"])
        p = daten["probe"]
        assert os.path.isfile(os.path.join(a.wurzel, p["ausgabe"])), "Probe fehlt (Schritt 0e): " + p["ausgabe"]
        vroh = open(os.path.join(a.wurzel, p["vergleich"]), "rb").read()
        assert [hashlib.md5(vroh).hexdigest()] == [d[1] for d in daten["dateien"] if d[0] == p["vergleich"]], "Vergleichsdatei: md5"

        def ab(pfad):
            z = open(os.path.join(a.wurzel, pfad), encoding="utf-8").read().split("\n")
            k = [n for n, t in enumerate(z) if t.startswith(p["ab_zeile"])]
            assert len(k) == 1, ("Zeile nicht genau einmal", p["ab_zeile"], pfad)
            return z[2] if len(z) > 2 else None, z[k[0]:]
        kopf3, ist = ab(p["ausgabe"])
        assert kopf3 == p["kopfzeile_3"], "Probe: Zeile 3 ist %r, verlangt %r" % (kopf3, p["kopfzeile_3"])
        assert ist == ab(p["vergleich"])[1], "Probe: ab %r nicht zeilengleich mit der Vergleichsdatei" % p["ab_zeile"]

    # Text des steuernden Chats
    kopf = zaun(auftrag, "Kopf:")
    schluss = zaun(auftrag, "Schluss:")
    assert kopf.startswith("## %d. " % abschnitt), kopf[:30]
    assert schluss.startswith("### %d.%d " % (abschnitt, len(ueber) + 1)), schluss[:30]
    assert kopf.count("\n") == 2 and kopf.split("\n")[1] == "", "Kopf: Ueberschrift, Leerzeile, ein Absatz"
    kopf, schluss = kopf.replace("⟨S0⟩", s0), schluss.replace("⟨S0⟩", s0)
    if a.s0:
        for t in (kopf, schluss):
            assert "⟨" not in t and "⟩" not in t, t[t.find("⟨"):][:60]

    # R-Bloecke und Anhang
    bl = bloecke(a.wurzel, daten["quelle"], erster, letzter)
    anhang = [kopf, ""]
    for n, u in enumerate(ueber, 1):
        assert u["zeile"].startswith("### %d.%d R%d — " % (abschnitt, n, u["R"])), u["zeile"][:40]
        kern = u["zeile"].split(" ", 2)[2]
        if kern.endswith("…"):
            assert bl[u["R"]][0].startswith(kern[:-1]), u["R"]
        else:
            assert bl[u["R"]][0].startswith(kern + "."), u["R"]
        assert u["kette"].startswith("**Kette:** ")
        anhang += [u["zeile"], ""] + ["> " + s for s in bl[u["R"]]] + ["", u["kette"], ""]
    anhang = "\n".join(anhang) + "\n" + schluss
    assert "⟦" not in anhang and "⟧" not in anhang

    # Register lesen, Marken einsetzen
    roh = open(reg_pfad, "rb").read()
    assert hashlib.sha256(roh).hexdigest() == daten["register_sha256"], "Register: sha256 weicht ab"
    reg = roh.decode("utf-8")
    assert reg.endswith("\n") and not reg.endswith("\n\n")
    alt = reg[:-1].split("\n")
    assert len(alt) == daten["register_zeilen"], len(alt)
    assert reg.count("## %d." % abschnitt) == 0, "Abschnitt schon vergeben"
    assert not any(s.startswith("> R%d — " % erster) for s in alt), "erster Block schon im Register"
    k9 = next(i for i, s in enumerate(alt) if s.startswith("## 9."))
    k11 = next(i for i, s in enumerate(alt) if s.startswith("## 11."))
    ea = next(i for i, s in enumerate(alt) if s.startswith("<!-- ERZEUGT:"))
    ee = next(i for i, s in enumerate(alt) if s.startswith("<!-- ENDE ERZEUGT -->"))
    je_stelle = {}
    for m in marken:
        assert reg.count(m["anker"]) == 1, ("Anker", m["nr"])
        assert alt[m["ankerzeile"] - 1].startswith(m["anker"]), ("Ankerzeile", m["nr"])
        assert alt[m["nach"] - 1].startswith(m["anfang40"]), ("Einfuegestelle", m["nr"])
        assert m["nach"] > m["ankerzeile"], ("Einfuegestelle vor dem Anker", m["nr"])
        p = m["nach"] - 1                     # 0-basiert: Zeile, NACH der eingefuegt wird
        assert not (k9 <= p < k11), ("Abschnitt 9 oder 10", m["nr"])
        assert not (ea <= p <= ee), ("ERZEUGT-Block", m["nr"])
        assert alt[p + 1] == "", ("keine Leerzeile nach der Einfuegestelle", m["nr"])
        assert m["m2"] == M2 and "⟨" not in m["m1"], ("Markenzeilen", m["nr"])
        je_stelle.setdefault(p, []).append(m)
    for p, v in je_stelle.items():
        assert [(m["R"], m["nr"]) for m in v] == sorted((m["R"], m["nr"]) for m in v), ("Reihenfolge", p + 1)
    assert len(set(m["m1"] for m in marken)) == len(marken), "Markenzeile doppelt"
    for m in marken:
        assert m["m1"] not in alt, ("Marke steht schon im Register", m["nr"])
    neu, gesetzt = [], []
    for i, s in enumerate(alt):
        neu.append(s)
        for m in je_stelle.get(i, []):
            neu.extend(["", m["m1"], m["m2"]])
            gesetzt.append((m, len(neu) - 1))          # 1-basierte Zeile der Markenzeile 1
    text = "\n".join(neu) + "\n\n" + anhang + "\n"

    # Wachen am neuen Text
    nz = text[:-1].split("\n")
    it = iter(nz)
    assert all(any(x == y for y in it) for x in alt), "alte Zeilen nicht in Reihenfolge erhalten"
    n9 = next(i for i, s in enumerate(nz) if s.startswith("## 9."))
    n11 = next(i for i, s in enumerate(nz) if s.startswith("## 11."))
    assert nz[n9:n11] == alt[k9:k11], "Abschnitt 9/10 veraendert"
    nea = next(i for i, s in enumerate(nz) if s.startswith("<!-- ERZEUGT:"))
    nee = next(i for i, s in enumerate(nz) if s.startswith("<!-- ENDE ERZEUGT -->"))
    assert nz[nea:nee + 1] == alt[ea:ee + 1], "ERZEUGT-Block veraendert"
    for m, z in gesetzt:
        assert text.count(m["anker"]) == 1, ("Anker nachher", m["nr"])
        assert nz.count(m["m1"]) == 1 and nz[z - 1] == m["m1"] and nz[z] == M2 and nz[z - 2] == "", m["nr"]
    for u in ueber:
        assert nz.count(u["zeile"]) == 1, u["zeile"]
    assert sum(1 for s in nz if s.startswith("## %d. " % abschnitt)) == 1
    for s in ("## 10. ", "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert text.count(s) == reg.count(s), s
    assert nz.count(M2) == alt.count(M2) + len(marken)
    assert not text.endswith("\n\n")

    open(reg_pfad, "w", encoding="utf-8", newline="\n").write(text)
    if a.daten:
        json.dump({"register": reg_pfad, "S0": s0.strip("`"),
                   "marken": [{"nr": m["nr"], "R": m["R"], "stelle": m["stelle"], "nach_alt": m["nach"],
                               "zeile_neu": z, "m1": m["m1"]} for m, z in gesetzt]},
                  open(a.daten, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Register:", reg_pfad)
    print("Marken gesetzt am alten Ort:", len(gesetzt), "an", len(je_stelle), "Einfuegestellen")
    print("R-Bloecke:", len(bl), "(R%d-R%d)" % (erster, letzter))
    print("Zeilen vorher:", len(alt), " nachher:", len(nz), " eingefuegt:", len(nz) - len(alt))
    print("sha256 nachher:", hashlib.sha256(text.encode("utf-8")).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
