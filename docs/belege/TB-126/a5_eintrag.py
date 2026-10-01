#!/usr/bin/env python3
"""TB-126 A5: Register-Abschnitte 47-50 anhaengen (R18-R55 zeichengleich, Tatsachennotizen E-2) und
die Marken aus Anhang A am alten Ort setzen.

Bauart TB-117 eintrag_register_46.py (Vorlage mit Platzhaltern, Texte werden EINGESETZT, nicht abgetippt).
Alle Texte kommen per `git show <S0>:<pfad>` aus dem Commit von Schritt 0:
  - Koepfe 47.0/48.0/49.0 und der Text von 50: die ````-Zaeune im Auftrag (A1 bzw. A3);
  - Ueberschriften und Marken: der Daten-Block (JSON) aus Anhang A; die Orte fuer die Kette aus
    Anhang A, Tabelle 2, Spalte "Registerstelle" ohne den Klammerzusatz "(Ankerzeile N)";
  - R-Bloecke: 27c Z. 161-209, 29b Z. 190-267, 30a Z. 25-32, Schnittregel des Auftrags;
  - Docstring-Zitat: auswertung.py von 'DIE ROHERGEBNISSE - DER VERTRAG' bis zur letzten nicht leeren
    Zeile vor 'ZWEI DEFINITIONEN, ...'; Entwuerfe TB-122 Z. 235-275, TB-124 Z. 289-323.
Platzhalter der Vorlage a5_vorlage_47_50.md:  ⟦KOPF:<n>⟧  ⟦BLOCK:<R>⟧  ⟦TEXT:50⟧

Marken: je Marke Leerzeile + zwei Markenzeilen nach der Einfuegestelle (Zeilennummer am Original);
mehrere an derselben Stelle in der Reihenfolge von Tabelle 2. Kette: Orte mit "; " getrennt, weil die Orte
selbst Kommas tragen ("1, Tabelle, Zeile 4"). Einzige Abweichung von der reinen Markenform:
nach Nr. 13 (5.1 Nr. 7) folgt eine zusaetzliche Leerzeile, weil die Folgezeile "8. **..." sonst als
Fortsetzung in das Blockzitat der Marke gezogen wuerde (Markdown, lazy continuation).

Wachen: Eingang 10347 Zeilen; '## 47.' noch nicht vergeben; jede alte Zeile in derselben Reihenfolge;
keine neue Zeile zwischen '## 10.' und '## 11.'; keine neue Zeile im ERZEUGT-Block; in Abschnitt 9
hoechstens eine neue Marke; 87 Anker je genau 1.

Aufruf aus der Repo-Wurzel:
  Probelauf:  TB126_PROBE=<kopie> trading-env/bin/python3 docs/belege/TB-126/a5_eintrag.py
  echt:                           trading-env/bin/python3 docs/belege/TB-126/a5_eintrag.py
Schreibt ausserdem docs/belege/TB-126/a5_eintrag_daten.json (gesetzte Marken mit Zeile nachher).
"""
import json
import os
import re
import subprocess
import sys

S0 = "0f56aeb"
DATUM = "01.10.2026"
REG = os.environ.get("TB126_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-126/"
AUFTRAG = "docs/auftraege/MAC_TB-126_register_e2.md"
FD = "docs/projektfuehrung/"
QUELLEN = {"27c": (FD + "FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md", 161, 209),
           "29b": (FD + "FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md", 190, 267),
           "30a": (FD + "FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md", 25, 32)}
NR_LEERZEILE_DANACH = {13}
VORAUSSETZUNG = {25, 26, 28, 33, 36, 41, 48, 49, 50, 53, 54, 55}
FELDLISTE = {39}
ZAEHLWEISE = {53}
ENTSCHEID = {24}
ABSCHNITT10 = {30, 42, 45, 48, 49, 51}


def show(pfad):
    return subprocess.run(["git", "show", "%s:%s" % (S0, pfad)], capture_output=True, text=True,
                          check=True).stdout


def zaeune(text, ab, n):
    """Die ersten n ````-Zaeune nach der Zeile, die mit `ab` beginnt; Inhalt ohne Zaunzeilen."""
    z = text.split("\n")
    i = next(k for k, s in enumerate(z) if s.startswith(ab))
    erg, inhalt = [], None
    for s in z[i + 1:]:
        if s == "````":
            if inhalt is None:
                inhalt = []
            else:
                erg.append("\n".join(inhalt))
                inhalt = None
                if len(erg) == n:
                    return erg
        elif inhalt is not None:
            inhalt.append(s)
    raise SystemExit("Zaeune nicht gefunden: %r" % ab)


def bloecke():
    bl = {}
    for q, (pfad, a, b) in QUELLEN.items():
        z = show(pfad).split("\n")
        cur = None
        for i in range(a, b + 1):
            s = z[i - 1]
            m = re.match(r"^(\*\*)?R(\d+) — ", s)
            if m:
                assert cur is None, ("Block ohne Ende", q, i)
                cur = int(m.group(2))
                assert cur not in bl, ("Dopplung", cur)
                bl[cur] = (q, [s])
                continue
            if cur is not None:
                bl[cur][1].append(s)
                if s.startswith("Quelle des Grundes:") or s.startswith("*Quelle des Grundes:*"):
                    assert s.endswith("Kein Ergebnis."), (cur, s[-40:])
                    cur = None
            else:
                assert s.strip() == "", ("Zeile ausserhalb eines Blocks", q, i, s[:60])
        assert cur is None
    assert sorted(bl) == list(range(18, 56)), sorted(bl)
    return bl


def main():
    auftrag = show(AUFTRAG)
    daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
    marken = daten["marken"]
    assert len(marken) == 87
    t2 = auftrag.split("## Tabelle 2", 1)[1].split("## A — Indexzeilen", 1)[0]
    zeilen_t2 = [s for s in t2.split("\n") if re.match(r"^\| \d+ \|", s)]
    assert len(zeilen_t2) == 88
    stelle = {}
    for s in zeilen_t2:
        sp = [x.strip() for x in re.split(r"(?<!\\)\|", s)[1:-1]]
        stelle[int(sp[0])] = re.sub(r" \(Ankerzeile \d+\)$", "", sp[3])
    for m in marken:
        assert stelle[m["nr"]] == m["stelle"], m["nr"]
    koepfe = zaeune(auftrag, "Jede Zeile des Blocks wird zu `> ` plus der Zeile", 3)
    text50 = zaeune(auftrag, "**A3. Text von Abschnitt 50**", 1)[0]
    kopf = {47: koepfe[0], 48: koepfe[1], 49: koepfe[2]}
    for n, k in kopf.items():
        assert k.startswith("## %d. " % n), k[:30]
    assert text50.startswith("## 50. ")
    bl = bloecke()
    ueber = {u["R"]: u for u in daten["ueberschriften"]}
    assert sorted(ueber) == list(range(18, 56))

    # Platzhalter von 50
    A = show("research/vorregistrierung/auswertung.py").split("\n")
    ia = [i for i, s in enumerate(A) if "DIE ROHERGEBNISSE - DER VERTRAG" in s]
    ib = [i for i, s in enumerate(A) if "ZWEI DEFINITIONEN, DIE SONST SCHWEIGEND AUSEINANDERLAUFEN" in s]
    assert len(ia) == 1 and len(ib) == 1
    za, zb = ia[0], ib[0] - 1
    while A[zb].strip() == "":
        zb -= 1
    doc = "\n".join(A[za:zb + 1])
    e122 = show("docs/ERGEBNIS_TB-122_posten3_achsen_durchreichen.md").split("\n")[234:275]
    e124 = show("docs/ERGEBNIS_TB-124_scanbeginn_sync_r28.md").split("\n")[288:323]
    assert e122[0].startswith("> **Vollzug TB-30b Posten 3 (11.3) in TB-122") and e122[-1].endswith("TB-122 Befund F1).")
    assert e124[0].startswith("> **Vollzug TB-30b Posten 3 (11.3), Teil Scanbeginn") and e124[-1].endswith("nie früher, nicht später.")
    s0 = "`%s`" % S0
    text50 = (text50.replace("⟨S0⟩", s0).replace("⟨Z_A⟩", str(za + 1)).replace("⟨Z_B⟩", str(zb + 1))
              .replace("⟨ZITAT_DOCSTRING⟩", doc).replace("⟨ENTWURF_TB122⟩", "\n".join(e122))
              .replace("⟨ENTWURF_TB124⟩", "\n".join(e124)))
    kopf = {n: k.replace("⟨S0⟩", s0) for n, k in kopf.items()}
    for t in list(kopf.values()) + [text50]:
        assert "⟨" not in t and "⟩" not in t, t[t.find("⟨"):][:60]

    def block(r):
        u = ueber[r]
        q, zz = bl[r]
        assert u["quelle"] == q
        aus = [u["zeile"], ""] + ["> " + s for s in zz]
        if r == 48:
            r54 = daten["r54_unter_48_16"]
            aus += ["", r54["m1"].replace("⟨DATUM⟩", DATUM), r54["m2"]]
        orte = [stelle[m["nr"]] for m in marken if m["R"] == r]
        if r == 54:
            orte.append(stelle[88])
        kette = "**Kette:** Marken: %s." % ("; ".join(orte) if orte else "keine")
        if r in VORAUSSETZUNG:
            kette += " Voraussetzung gemessen: 50.1."
        if r in FELDLISTE:
            kette += " Feldliste: 50.2."
        if r in ZAEHLWEISE:
            kette += " Zählweise: 50.5."
        if r in ENTSCHEID:
            kette += " Entscheid: 50.6."
        if r in ABSCHNITT10:
            kette += " Abschnitt 10: Indexzeile, keine Marke."
        return "\n".join(aus + ["", kette])

    vorlage = open(HIER + "a5_vorlage_47_50.md", encoding="utf-8").read().rstrip("\n")
    anhang = re.sub(r"⟦KOPF:(\d+)⟧", lambda m: kopf[int(m.group(1))], vorlage)
    anhang = re.sub(r"⟦BLOCK:(\d+)⟧", lambda m: block(int(m.group(1))), anhang)
    anhang = anhang.replace("⟦TEXT:50⟧", text50)
    assert "⟦" not in anhang and "⟧" not in anhang and "⟨" not in anhang

    # Register
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    alt = reg[:-1].split("\n")
    assert len(alt) == 10347, len(alt)
    assert not any(s.startswith("## 47.") for s in alt), "47 schon vergeben"
    k9 = next(i for i, s in enumerate(alt) if s.startswith("## 9. "))
    k10 = next(i for i, s in enumerate(alt) if s.startswith("## 10."))
    k11 = next(i for i, s in enumerate(alt) if s.startswith("## 11."))
    ea = next(i for i, s in enumerate(alt) if s.startswith("<!-- ERZEUGT:"))
    ee = next(i for i, s in enumerate(alt) if s.startswith("<!-- ENDE ERZEUGT -->"))
    je_stelle = {}
    for m in marken:
        assert reg.count(m["anker"]) == 1, m["nr"]
        assert alt[m["ankerzeile"] - 1].startswith(m["anker"]), m["nr"]
        assert alt[m["nach"] - 1].startswith(m["anfang40"]), m["nr"]
        p = m["nach"] - 1                     # 0-basiert: Zeile, NACH der eingefuegt wird
        assert not (k10 <= p < k11), ("Abschnitt 10", m["nr"])
        assert not (ea <= p < ee), ("ERZEUGT-Block", m["nr"])
        zus = ["", m["m1"].replace("⟨DATUM⟩", DATUM), m["m2"]]
        if m["nr"] in NR_LEERZEILE_DANACH:
            zus.append("")
        je_stelle.setdefault(p, []).append((m, zus))
    in9 = sum(len(v) for p, v in je_stelle.items() if k9 <= p < k10)
    assert in9 <= 1, in9
    neu, gesetzt = [], []
    for i, s in enumerate(alt):
        neu.append(s)
        for m, zus in je_stelle.get(i, []):
            neu.extend(zus)
            gesetzt.append((m, len(neu) - len(zus) + 2))   # 1-basierte Zeile der Markenzeile 1
    text = "\n".join(neu) + "\n\n" + anhang + "\n"

    # Wachen
    nz = text[:-1].split("\n")
    it = iter(nz)
    assert all(any(x == y for y in it) for x in alt), "alte Zeilen nicht in Reihenfolge"
    n10 = next(i for i, s in enumerate(nz) if s.startswith("## 10."))
    n11 = next(i for i, s in enumerate(nz) if s.startswith("## 11."))
    assert nz[n10:n11] == alt[k10:k11], "Abschnitt 10 veraendert"
    nea = next(i for i, s in enumerate(nz) if s.startswith("<!-- ERZEUGT:"))
    nee = next(i for i, s in enumerate(nz) if s.startswith("<!-- ENDE ERZEUGT -->"))
    assert nz[nea:nee + 1] == alt[ea:ee + 1], "ERZEUGT-Block veraendert"
    for m in marken:
        assert text.count(m["anker"]) == 1, ("Anker nachher", m["nr"])
    assert text.count(daten["r54_unter_48_16"]["anker"]) == 1
    for u in daten["ueberschriften"]:
        assert nz.count(u["zeile"]) == 1, u["zeile"]
    for n in (47, 48, 49, 50):
        assert sum(1 for s in nz if s.startswith("## %d. " % n)) == 1, n
    for s in ("## 10. Die Sperrliste", "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert text.count(s) == reg.count(s), s

    open(REG, "w", encoding="utf-8").write(text)
    json.dump({"register": REG, "S0": S0, "datum": DATUM, "docstring_zeilen": [za + 1, zb + 1],
               "marken": [{"nr": m["nr"], "R": m["R"], "nach_alt": m["nach"], "zeile_neu": z,
                           "m1": m["m1"].replace("⟨DATUM⟩", DATUM)} for m, z in gesetzt]},
              open(HIER + "a5_eintrag_daten.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Register:", REG)
    print("Marken gesetzt am alten Ort:", len(gesetzt), "an", len(je_stelle), "Einfuegestellen; davon in Abschnitt 9:", in9)
    print("Marke unter 48.16 (R54): 1")
    print("R-Bloecke:", len(bl), " Docstring Z. %d-%d" % (za + 1, zb + 1))
    print("Zeilen vorher:", len(alt), " nachher:", len(nz))


if __name__ == "__main__":
    main()
