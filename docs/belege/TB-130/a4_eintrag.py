#!/usr/bin/env python3
"""TB-130 A4: Register-Abschnitt 52 anhaengen (R63-R65 zeichengleich, Text des steuernden Chats 52.0 und
52.4-52.5) und die 12 Marken aus Anhang A am alten Ort setzen.

Bauart TB-126 a5_eintrag.py (Vorlage mit Platzhaltern, Texte werden EINGESETZT, nicht abgetippt).
Alle Texte kommen per `git show <S0>:<pfad>` aus dem Commit von Schritt 0:
  - Kopf 52.0 und Schluss 52.4-52.5: die beiden ````-Zaeune im Auftrag nach "Kopf:" bzw. "Schluss:" (A3);
  - Ueberschriften, Ketten und Marken: der Daten-Block (JSON) aus Anhang A;
  - R-Bloecke: FABLE_ANTWORT_2026-10-02a Z. 112-119, Schnittregel des Auftrags (Beginn 'R<n> — ',
    Ende einschliesslich der ersten Zeile 'Quelle des Grundes:').
Platzhalter der Vorlage a4_vorlage_52.md:  ⟦KOPF⟧  ⟦BLOCK:<R>⟧  ⟦SCHLUSS⟧
Ersetzt werden im Text des steuernden Chats ⟨S0⟩ -> `<S0>` und in den Marken ⟨DATUM⟩ -> Datum.

Marken: je Marke Leerzeile + zwei Markenzeilen nach der Einfuegestelle (Zeilennummer am Original);
mehrere an derselben Stelle in der Reihenfolge des Daten-Blocks (dort nach R aufsteigend).

Wachen: Eingang 11225 Zeilen; '## 52.' noch nicht vergeben; keine Zeile beginnt mit '> R63 — ';
jede alte Zeile in derselben Reihenfolge; keine neue Zeile zwischen '## 9.' und '## 11.'; keine neue Zeile
im ERZEUGT-Block; 12 Anker je genau 1 vorher und nachher.

Aufruf aus der Repo-Wurzel:
  Probelauf:  TB130_PROBE=<kopie> trading-env/bin/python3 docs/belege/TB-130/a4_eintrag.py
  echt:                           trading-env/bin/python3 docs/belege/TB-130/a4_eintrag.py
Schreibt ausserdem docs/belege/TB-130/a4_eintrag_daten.json (gesetzte Marken mit Zeile nachher).
"""
import json
import os
import re
import subprocess

S0 = "b0c7a35"
DATUM = "02.10.2026"
REG = os.environ.get("TB130_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-130/"
AUFTRAG = "docs/auftraege/MAC_TB-130_register_fable_02a.md"


def show(pfad):
    return subprocess.run(["git", "show", "%s:%s" % (S0, pfad)], capture_output=True, text=True,
                          check=True).stdout


def zaun(text, ab):
    """Inhalt des ersten ````-Zauns nach der Zeile, die genau `ab` ist."""
    z = text.split("\n")
    i = z.index(ab)
    a = next(k for k in range(i + 1, len(z)) if z[k] == "````")
    b = next(k for k in range(a + 1, len(z)) if z[k] == "````")
    return "\n".join(z[a + 1:b])


def bloecke(q):
    z = show(q["pfad"]).split("\n")
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
    assert sorted(bl) == list(range(63, 66)), sorted(bl)
    assert all(len(v) == 2 for v in bl.values())
    return bl


def main():
    auftrag = show(AUFTRAG)
    daten = json.loads(auftrag.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
    marken = daten["marken"]
    assert len(marken) == 12
    assert [m["nr"] for m in marken] == list(range(1, 13))
    kopf = zaun(auftrag, "Kopf:")
    schluss = zaun(auftrag, "Schluss:")
    assert kopf.startswith("## 52. "), kopf[:30]
    assert schluss.startswith("### 52.4 "), schluss[:30]
    s0 = "`%s`" % S0
    kopf, schluss = kopf.replace("⟨S0⟩", s0), schluss.replace("⟨S0⟩", s0)
    for t in (kopf, schluss):
        assert "⟨" not in t and "⟩" not in t, t[t.find("⟨"):][:60]
    bl = bloecke(daten["quelle"])
    ueber = {u["R"]: u for u in daten["ueberschriften"]}
    assert sorted(ueber) == list(range(63, 66))
    for r, u in ueber.items():
        assert u["zeile"] == "### 52.%d R%d — " % (r - 62, r) + u["zeile"].split(" — ", 1)[1]
        assert bl[r][0].startswith(u["zeile"].split(" ", 2)[2] + "."), r

    def block(r):
        u = ueber[r]
        return "\n".join([u["zeile"], ""] + ["> " + s for s in bl[r]] + ["", u["kette"]])

    vorlage = open(HIER + "a4_vorlage_52.md", encoding="utf-8").read().rstrip("\n")
    anhang = vorlage.replace("⟦KOPF⟧", kopf).replace("⟦SCHLUSS⟧", schluss)
    anhang = re.sub(r"⟦BLOCK:(\d+)⟧", lambda m: block(int(m.group(1))), anhang)
    assert "⟦" not in anhang and "⟧" not in anhang and "⟨" not in anhang

    # Register
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n") and not reg.endswith("\n\n")
    alt = reg[:-1].split("\n")
    assert len(alt) == 11225, len(alt)
    assert reg.count("## 52.") == 0, "52 schon vergeben"
    assert not any(s.startswith("> R63 — ") for s in alt), "R63 schon im Register"
    k9 = next(i for i, s in enumerate(alt) if s.startswith("## 9."))
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
        assert not (k9 <= p < k11), ("Abschnitt 9 oder 10", m["nr"])
        assert not (ea <= p < ee), ("ERZEUGT-Block", m["nr"])
        assert alt[p + 1] == "", ("keine Leerzeile nach der Einfuegestelle", m["nr"])
        zus = ["", m["m1"].replace("⟨DATUM⟩", DATUM), m["m2"]]
        je_stelle.setdefault(p, []).append((m, zus))
    for p, v in je_stelle.items():
        assert [m["R"] for m, _ in v] == sorted(m["R"] for m, _ in v), ("Reihenfolge an Stelle", p + 1)
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
    n9 = next(i for i, s in enumerate(nz) if s.startswith("## 9."))
    n11 = next(i for i, s in enumerate(nz) if s.startswith("## 11."))
    assert nz[n9:n11] == alt[k9:k11], "Abschnitt 9/10 veraendert"
    nea = next(i for i, s in enumerate(nz) if s.startswith("<!-- ERZEUGT:"))
    nee = next(i for i, s in enumerate(nz) if s.startswith("<!-- ENDE ERZEUGT -->"))
    assert nz[nea:nee + 1] == alt[ea:ee + 1], "ERZEUGT-Block veraendert"
    for m in marken:
        assert text.count(m["anker"]) == 1, ("Anker nachher", m["nr"])
    for u in daten["ueberschriften"]:
        assert nz.count(u["zeile"]) == 1, u["zeile"]
    assert sum(1 for s in nz if s.startswith("## 52. ")) == 1
    for s in ("## 10. ", "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert text.count(s) == reg.count(s), s

    open(REG, "w", encoding="utf-8").write(text)
    json.dump({"register": REG, "S0": S0, "datum": DATUM,
               "marken": [{"nr": m["nr"], "R": m["R"], "stelle": m["stelle"], "nach_alt": m["nach"],
                           "zeile_neu": z, "m1": m["m1"].replace("⟨DATUM⟩", DATUM)} for m, z in gesetzt]},
              open(HIER + "a4_eintrag_daten.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Register:", REG)
    print("Marken gesetzt am alten Ort:", len(gesetzt), "an", len(je_stelle), "Einfuegestellen")
    print("R-Bloecke:", len(bl))
    print("Zeilen vorher:", len(alt), " nachher:", len(nz))


if __name__ == "__main__":
    main()
