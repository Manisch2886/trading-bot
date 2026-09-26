"""TB-117 F: Register 46.11 (Vollzug in TB-117, Tatsachennotiz) ans Ende von Abschnitt 46 anhaengen.

Bauart TB-117 A (eintrag_register_46.py), ohne Marken und ohne Zitate: nur Anhaengen. Wachen: Eingangszeilen
10266 (Stand Block A), 46.11 noch nicht vorhanden, 46 ist der letzte Abschnitt, Abschnitt 10 unveraendert an
derselben Stelle, jede alte Zeile in derselben Reihenfolge im neuen Text (additiv), Leser-Wachen wie in A.
Aufruf aus der Repo-Wurzel, genau einmal; Probelauf mit TB117_PROBE=<kopie>:
  trading-env/bin/python3 docs/belege/TB-117/f_eintrag_46_11.py
"""
import os
import re

REG = os.environ.get("TB117_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
VORLAGE = "docs/belege/TB-117/f_46_11_vorlage.md"


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert len(zeilen) == 10266, len(zeilen)
    assert not any(z.startswith("### 46.11") for z in zeilen)
    assert [z for z in zeilen if z.startswith("## ")][-1].startswith("## 46. ")
    text = open(VORLAGE, encoding="utf-8").read().rstrip("\n")
    assert text.startswith("### 46.11 ") and "⟦" not in text and "⟨" not in text
    neu = reg + "\n" + text + "\n"
    g6 = re.compile(r"^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*")
    assert sum(1 for z in neu.split("\n") if g6.match(z)) == 1
    for s in ("ERSETZT durch Abschnitt 15", "| **730** |", "## 10. Die Sperrliste",
              "<!-- ERZEUGT: registerbericht.py", "<!-- ENDE ERZEUGT -->"):
        assert neu.count(s) == reg.count(s), s
    assert neu.startswith(reg), "nicht additiv"
    open(REG, "w", encoding="utf-8").write(neu)
    print("46.11 angehaengt, Registerzeilen:", len(neu.split("\n")) - 1)


if __name__ == "__main__":
    main()
