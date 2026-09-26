"""TB-114: Registerabschnitt 45 (Fable 26a, R1-R8) und elf Marken am alten Ort.

(Kopie von TB-113 eintrag_register_44.py; neu: Quellen, Marken, Vorlage, Eingangswache 9816,
Abschnitt 10 wird nach Inhalt statt nach Zeilenlage verglichen, weil die Marke unter 7.1 davor liegt.)
Bauart TB-110 (`docs/belege/TB-110/eintrag_register_43.py`), unveraendert bis
auf Quellen, Marken, Vorlage und die Wachen fuer den Eingangsstand. Setzt Texte EIN statt sie abzutippen:
  ⟦Z:<q>:n⟧        -> Zeile n der Quelle q, ohne fuehrendes "> " (die Vorlage setzt "> ")
  ⟦T:<q>:n|text⟧   -> text, der wortgleich in Zeile n der Quelle q stehen muss
und schreibt jedes Zitat nach zitate.json fuer c2_zitate.py.
Neu gegenueber TB-110: eine Quelle "git:<commit>:<pfad>" wird per `git show`
gelesen (das Register selbst am Merge-Commit, dessen Zeilennummern sich durch
die Marken verschieben).

Jede Marke wird hinter einer Ankerzeile eingefuegt, die innerhalb ihres
Zielabschnitts (Kopfzeile bis zur naechsten Kopfzeile) GENAU EINMAL vorkommen
muss - sonst Abbruch ohne Schreiben. Nichts wird ersetzt oder entfernt; keine
Marke liegt zwischen `## 10.` und `## 11.` (Sonde, Pruefung (ii)).
Aufruf aus der Repo-Wurzel, genau einmal:
  trading-env/bin/python3 docs/belege/TB-114/eintrag_register_45.py
"""
import json
import os
import re
import subprocess

# TB114_PROBE: Probelauf gegen eine Kopie (Pfad), bevor das Register geschrieben wird
REG = os.environ.get("TB114_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-114/"
QUELLEN = {
    "fab": "git:79c2dfa:docs/projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md",
    "herk": "git:79c2dfa:research/vorregistrierung/herkunft.py",
    "sonde": "git:79c2dfa:shared/sperrlistensonde.py",
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
    ("### 7.1 Die drei Regeln", "jeder Bleibt-Geht-Liste ausgegeben — auch dann, wenn kein Bot ausscheidet.", """\
> ⭐ **Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7** (Fable
> 26a R6/R7, TB-114, 26.09.2026). Die drei Regeln und der Satz oben bleiben
> zeichengleich.""", True, False, "7.1"),
    ("## 19. Registertext 5e, Ergänzung", "> zeichengleich.", """\
> ⭐ **Pflege von `ARBEITSBAUM_PFADE`: siehe 45.4** (Fable 26a R4, TB-114,
> 26.09.2026). Kasten, Tabelle, Text und die Marken oben bleiben
> zeichengleich.""", True, False, "19"),
    ("### 27.8 Was hier ausdrücklich NICHT getan wird", "| ⚠️ | **Die Prüfung nach 27.4**", """\
> ⭐ **Messungen auf dem Selektionsraum nach dem Tag: siehe 45.6/45.7** (Fable
> 26a R6/R7, TB-114, 26.09.2026). Abschnitt 27 oben bleibt zeichengleich.""", True, False, "27"),
    ("### 30.2 Der Registertext, zeichengleich", "> **(4)** Ob `faltenplan_tb72.json`", """\
> ⭐ **Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11**
> (Fable 26a R3, TB-114, 26.09.2026). Der Registertext oben bleibt
> zeichengleich.""", True, False, "30.2"),
    ("### 33.3 Die Feldliste des Abbilds", "> zeichengleich.", """\
> ⭐ **Eingaben in der Gruppe `eingefroren`: siehe 45.3, vollzogen in 45.11**
> (Fable 26a R3, TB-114, 26.09.2026). Tabelle, Text und die Marke oben bleiben
> zeichengleich.""", True, False, "33.3"),
    ("### 41.1 Aus Fable 24b", "(Plan-Punkt 3); die neun Listen sind nicht neu erzeugt.", """\
> ⭐ **Abnahmebedingungen des Erzeugers: siehe 45.5** (Fable 26a R5, TB-114,
> 26.09.2026). Eintrag und Stand oben bleiben zeichengleich.""", True, False, "41.1 A12"),
    ("### 42.2 Aus Fable 25b", "42.6.", """\
> ⭐ **Reichweite: siehe 45.2** (Fable 26a R2, TB-114, 26.09.2026). Eintrag
> und Stand oben bleiben zeichengleich.""", True, False, "42.2 E1"),
    ("### 42.2 Aus Fable 25b", "> bleiben zeichengleich.", """\
> ⭐ **Pflege von `ARBEITSBAUM_PFADE`: siehe 45.4** (Fable 26a R4, TB-114,
> 26.09.2026). Eintrag, Stand und die Marke oben bleiben zeichengleich.""", True, False, "42.2 E2"),
    ("### 42.6 Was offen bleibt", "| (5) | **Der Erzeuger auf dem Signalpfad**", """\
| ↳ (5) | ⭐ **Abnahmebedingungen des Erzeugers: siehe 45.5** (Fable 26a R5, TB-114, 26.09.2026); die Zeile oben bleibt zeichengleich | 45.5 |""", False, False, "42.6 (5)"),
    ("### 43.3 ", "Stummel zurückgebaut, mit Grund.", """\
> ⭐ **Von Fable bestätigt (26a 3 (1)), siehe 45.1** (TB-114, 26.09.2026).
> Überschrift und Text oben bleiben zeichengleich.""", True, False, "43.3"),
    ("### 44.3 Was offen bleibt", "in (1) oben aufgegangen.", """\
> ⭐ **Beantwortet in Fable 26a, siehe 45** (TB-114, 26.09.2026): die Fragen
> aus TB-109, TB-111 und TB-112 in 45.1 bis 45.8, die Bestätigung von 43-11 in
> 45.1. Fragen und Tabelle oben bleiben zeichengleich.""", True, False, "44.3"),
]


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert len(zeilen) == 9816, len(zeilen)
    assert not any(z.startswith("## 45.") for z in zeilen)
    kopf = [i for i, z in enumerate(zeilen) if z.startswith("#")]
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
        block = ([""] if vor else []) + setze(text, wo).split("\n") + ([""] if nach else [])
        einfuegen.append((a[0], block, wo))
    assert len(einfuegen) == 11
    assert len({p for p, _, _ in einfuegen}) == 11
    for pos, block, wo in sorted(einfuegen, reverse=True):
        zeilen[pos + 1:pos + 1] = block
    teile = [setze(open(HIER + "abschnitt45_vorlage.md", encoding="utf-8").read().rstrip("\n"), "Abschnitt 45")]
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
