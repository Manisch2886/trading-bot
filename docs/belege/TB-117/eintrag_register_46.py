"""TB-117: Register 45.11 (Fable 27a R11) und Abschnitt 46 (R9, R10, R12-R17) und zehn Marken am alten Ort.

(Kopie von TB-114 eintrag_register_45.py; neu: Quellen, Marken, Vorlage, Eingangswache 10034,
Abschnitt 9 als zweite Sperrzone; Probelauf gegen eine Kopie mit TB117_PROBE=<kopie>.)
Setzt Texte EIN statt sie abzutippen:
  ⟦Z:<q>:n⟧        -> Zeile n der Quelle q, ohne fuehrendes "> " (die Vorlage setzt "> ")
  ⟦T:<q>:n|text⟧   -> text, der wortgleich in Zeile n der Quelle q stehen muss
und schreibt jedes Zitat nach zitate.json fuer a3_zitate.py. Quellen "git:<commit>:<pfad>" werden per
`git show` gelesen (Stand Schritt 0, 753ec11).

Jede Marke wird hinter einer Ankerzeile eingefuegt, die innerhalb ihres Zielabschnitts (Kopfzeile bis zur
naechsten Kopfzeile) GENAU EINMAL vorkommen muss - sonst Abbruch ohne Schreiben. Nichts wird ersetzt oder
entfernt; keine Marke liegt zwischen `## 10.` und `## 11.` (Sonde, Pruefung (ii)) oder in `## 9.`.
Aufruf aus der Repo-Wurzel, genau einmal:
  trading-env/bin/python3 docs/belege/TB-117/eintrag_register_46.py
"""
import json
import os
import re
import subprocess

# TB117_PROBE: Probelauf gegen eine Kopie (Pfad), bevor das Register geschrieben wird
REG = os.environ.get("TB117_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-117/"
QUELLEN = {
    "fab": "git:753ec11:docs/projektfuehrung/FABLE_ANTWORT_2026-09-27a_sonde_zweiseitig_herkunft_in_auswertung.md",
    "auf": "git:753ec11:docs/auftraege/MAC_TB-117_wachen_vor_dem_tag.md",
}


def lies(quelle):
    if quelle.startswith("git:"):
        _, commit, pfad = quelle.split(":", 2)
        return subprocess.run(["git", "show", "%s:%s" % (commit, pfad)], capture_output=True,
                              text=True, check=True).stdout
    return open(quelle, encoding="utf-8").read()


Q = {k: lies(v).split("\n") for k, v in QUELLEN.items()}
zitate = []


def setze(text, wo):
    def zeile(m):
        k, n = m.group(1), int(m.group(2))
        s = Q[k][n - 1]
        assert s.strip() and s.strip() != ">", (k, n)
        s = s[2:] if s.startswith("> ") else s
        zitate.append({"art": "zeile", "quelle": QUELLEN[k], "zeile": n, "text": s, "wo": wo})
        return s

    def teil(m):
        k, n, t = m.group(1), int(m.group(2)), m.group(3)
        assert t in Q[k][n - 1], "Teilzitat nicht in %s Z. %d: %r" % (k, n, t[:60])
        zitate.append({"art": "teil", "quelle": QUELLEN[k], "zeile": n, "text": t, "wo": wo})
        return t
    text = re.sub(r"⟦Z:(\w+):(\d+)⟧", zeile, text)
    text = re.sub(r"⟦T:(\w+):(\d+)\|([^⟧]+)⟧", teil, text)
    assert "⟦" not in text and "⟧" not in text, text[text.find("⟦"):][:80]
    return text


MARKEN = [
    # (Kopfzeile des Zielabschnitts, Ankerzeile (Anfang), Text, Leerzeile davor, Leerzeile danach, Ort)
    ("## 12. Der Vollständigkeitstest", "> (41.1, A7). Die Sätze oben bleiben zeichengleich.", """\
> ⭐ **Herkunftsprüfung in `auswertung.py`: siehe 46.5, Lesart 46.9** (Fable
> 27a R14, TB-117, 26.09.2026). Die Sätze und die Marken oben bleiben
> zeichengleich.""", True, False, "12"),
    ("#### Prüfung vor dem Tag", "⚠️ **Das Leiter-Skript existiert noch nicht.** Siehe 16.11, Zeile 3.", """\
> ⭐ **Evidenz der Leiter: siehe 46.4 (f); Lesarten: TB-116** (Fable 27a R13
> (f), TB-117, 26.09.2026). Die Prüfung vor dem Tag oben bleibt
> zeichengleich.""", True, False, "16.4"),
    ("### 36.5 ", "> Meldung sind zeichengleich. Die Texte oben bleiben zeichengleich.", """\
> ⭐ **Herkunftsprüfung in `auswertung.py`: siehe 46.5, Lesart 46.9** (Fable
> 27a R14, TB-117, 26.09.2026). Die Texte und die Marken oben bleiben
> zeichengleich.""", True, False, "36.5"),
    ("### 40.6 ", "> Zitate und Text oben bleiben zeichengleich.", """\
> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Zitate, Text und die Marke oben bleiben zeichengleich.""", True, False, "40.6"),
    ("### 40.8 ", "| (e) | ⚠️ **Befund:**", """\
| ↳ (e) | ⭐ **Zweite Seite: siehe 46.1** (Fable 27a R9, TB-117, 26.09.2026); die Zeile oben bleibt zeichengleich | 46.1 |""", False, False, "40.8 (e)"),
    ("### 41.1 Aus Fable 24b", "(B) (4) (42.1, D3/D9).", """\
> ⭐ **`fehlend` im Modus: siehe 46.2** (Fable 27a R10, TB-117, 26.09.2026).
> Eintrag und Stand oben bleiben zeichengleich.""", True, False, "41.1 A10"),
    ("### 41.1 Aus Fable 24b", "> 26.09.2026). Eintrag und Stand oben bleiben zeichengleich.", """\
> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Eintrag, Stand und die Marke oben bleiben zeichengleich.""", True, False, "41.1 A12"),
    ("### 45.3 ", "Vollzug steht in **45.11**.", """\
> ⭐ **Zwei Erzeuger; Bindung der Listen: siehe 46.3** (Fable 27a R12, TB-117,
> 26.09.2026). Zitat und Kette oben bleiben zeichengleich.""", True, False, "45.3"),
    ("### 45.7 ", "mit Marke hier.", """\
> ⭐ **Nr. 7: siehe 46.7 (a)** (Fable 27a R16 (a), TB-117, 26.09.2026). Zitat
> und Kette oben bleiben zeichengleich.""", True, False, "45.7"),
    ("### 45.10 ", "· 43.3 · 44.3. ⛔ Keine in Abschnitt 10, keine in 9.", """\
> ⭐ **Beantwortet und fortgeschrieben in 45.11 und 46** (Fable 27a, TB-117,
> 26.09.2026). Tabelle und Text oben bleiben zeichengleich.""", True, False, "45.10"),
]


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert len(zeilen) == 10034, len(zeilen)
    assert not any(z.startswith("## 46.") or z.startswith("### 45.11") for z in zeilen)
    kopf = [i for i, z in enumerate(zeilen) if z.startswith("#")]
    k9 = next(i for i, z in enumerate(zeilen) if z.startswith("## 9. "))
    k10 = next(i for i, z in enumerate(zeilen) if z.startswith("## 10. Die Sperrliste"))
    k11 = next(i for i, z in enumerate(zeilen) if z.startswith("## 11. "))
    einfuegen = []
    for kopfzeile, anker, text, vor, nach, wo in MARKEN:
        k = [i for i in kopf if zeilen[i].startswith(kopfzeile)]
        assert len(k) == 1, (kopfzeile, k)
        ende = min([i for i in kopf if i > k[0]] + [len(zeilen)])
        a = [i for i in range(k[0], ende) if zeilen[i].startswith(anker)]
        assert len(a) == 1, (kopfzeile, anker, a)
        assert not (k10 <= a[0] < k11), ("Marke in Abschnitt 10", wo)
        assert not (k9 <= a[0] < k10), ("Marke in Abschnitt 9", wo)
        block = ([""] if vor else []) + setze(text, wo).split("\n") + ([""] if nach else [])
        einfuegen.append((a[0], block, wo))
    assert len(einfuegen) == 10
    assert len({p for p, _, _ in einfuegen}) == 10
    for pos, block, wo in sorted(einfuegen, reverse=True):
        zeilen[pos + 1:pos + 1] = block
    teile = [setze(open(HIER + "abschnitt46_vorlage.md", encoding="utf-8").read().rstrip("\n"), "45.11 und Abschnitt 46")]
    neu = "\n".join(zeilen) + "\n\n" + "\n\n".join(teile) + "\n"
    # Wachen fuer die Leser des Registers (G6, test_faltenplan_neun E2, TB-41-Test, Sonde)
    g6 = re.compile(r"^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*")
    assert sum(1 for z in neu.split("\n") if g6.match(z)) == 1
    for s in ("ERSETZT durch Abschnitt 15", "| **730** |", "## 10. Die Sperrliste",
              "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert neu.count(s) == reg.count(s), s
    alt = reg.split("\n")
    # additiv: jede alte Zeile steht in derselben Reihenfolge im neuen Text
    it = iter(neu.split("\n"))
    assert all(any(z == y for y in it) for z in alt[:-1]), "nicht additiv"
    # Abschnitt 10 unveraendert an derselben Stelle
    nz = neu.split("\n")
    n10 = next(i for i, z in enumerate(nz) if z.startswith("## 10. Die Sperrliste"))
    n11 = next(i for i, z in enumerate(nz) if z.startswith("## 11. "))
    assert nz[n10:n11] == alt[k10:k11], "Abschnitt 10 veraendert"
    open(REG, "w", encoding="utf-8").write(neu)
    json.dump(zitate, open(HIER + "zitate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Marken:", len(einfuegen), " Zitate:", len(zitate),
          "(Zeilen %d, Teile %d)" % (sum(z["art"] == "zeile" for z in zitate),
                                     sum(z["art"] == "teil" for z in zitate)),
          " Registerzeilen:", len(neu.split("\n")) - 1)


if __name__ == "__main__":
    main()
