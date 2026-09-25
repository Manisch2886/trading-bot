"""TB-110: Registerabschnitt 43 und sechs Marken am alten Ort.

Bauart TB-108 (`docs/belege/TB-108/eintrag_register_41_42.py`), unveraendert bis
auf Quellen, Marken, Vorlage und die Wachen fuer den Eingangsstand. Setzt Fables Texte EIN statt sie abzutippen:
  ⟦Z:<q>:n⟧        -> Zeile n der Quelle q, ohne fuehrendes "> " (die Vorlage setzt "> ")
  ⟦T:<q>:n|text⟧   -> text, der wortgleich in Zeile n der Quelle q stehen muss
und schreibt jedes Zitat nach zitate.json fuer d2_zitate.py.

Jede Marke wird hinter einer Ankerzeile eingefuegt, die innerhalb ihres
Zielabschnitts (Kopfzeile bis zur naechsten Kopfzeile) GENAU EINMAL vorkommen
muss - sonst Abbruch ohne Schreiben. Nichts wird ersetzt oder entfernt; keine
Marke liegt zwischen `## 10.` und `## 11.` (Sonde, Pruefung (ii)).
Aufruf aus der Repo-Wurzel, genau einmal:
  trading-env/bin/python3 docs/belege/TB-110/eintrag_register_43.py
"""
import json
import os
import re

# TB110_PROBE: Probelauf gegen eine Kopie (Pfad), bevor das Register geschrieben wird
REG = os.environ.get("TB110_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-110/"
P = "docs/projektfuehrung/"
QUELLEN = {
    "25d": P + "FABLE_ANTWORT_2026-09-25d_kopie_pruefansicht_abbruch_zwei.md",
    "25e": P + "FABLE_ANTWORT_2026-09-25e_ablagen_nulltrades_shim.md",
}
Q = {k: open(v, encoding="utf-8").read().split("\n") for k, v in QUELLEN.items()}
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
    ("### 5.1 Die Regeln", '   in schweren Jahren nicht handeln."*', """\
   > ⭐ **Null Trades ist ein Wert — auch für den Lauf (43.2, 43-7, Fable 25e,
   > TB-110, 26.09.2026):** Aus Nr. 8 und 1c (15.3) folgt für jeden Lauf des
   > Laufbereichs: Findet oder führt er keine Trades aus, schreibt er dieses
   > Ergebnis und endet mit 0; er endet nie ohne Ausgabe. Unter dem Modus endet
   > ein `exit()` ohne geschriebenes Ergebnis mit 2. Wortlaut in **43.2, 43-7**;
   > vollzogen an zehn Stellen in TB-109. Der Satz oben bleibt zeichengleich.""", True, False, "5.1 Nr. 8"),
    ("## 12. Der Vollständigkeitstest", "ab — es füllt nichts auf und überspringt nichts.", """\
> ⭐ **Mit welchem Wert es abbricht (43.1, 43-1, Fable 25d, TB-110,
> 26.09.2026):** `auswertung.py` hat zwei Ausgänge — 0, wenn es gerechnet und
> berichtet hat; **2**, wenn es nicht rechnen konnte (jeder Bruch des
> Datenvertrags). Einen Ausgang 1 hat es nicht; die Abbruchkriterien (a)–(d)
> sind Ergebnisse eines gelungenen Laufs. Wortlaut in **43.1, 43-1**. Heute
> endet `Abbruch` noch mit 1 (zwölf Stellen); die Umstellung kommt mit der
> nächsten planmässigen Öffnung von `auswertung.py`. Der Satz oben bleibt
> zeichengleich.""", True, False, "12"),
    ("### 15.3 Registertext 1 — Bootstrap", '> („Falten ohne Trade zählen mit Sharpe 0"), die hier unberührt weitergilt.', """\
> ⭐ **Folge für den Lauf (43.2, 43-7, Fable 25e, TB-110, 26.09.2026):** 1c
> und 5.1 Nr. 8 machen „keine Trades" zu einem **Wert**, der in die Statistik
> eingeht — nicht zu einem Grund, aufzuhören. Deshalb schreibt ein Lauf, der
> keine Trades findet, dieses Ergebnis und endet nie ohne Ausgabe (Wortlaut in
> **43.2, 43-7**). Registertext und Tatsachennotiz oben bleiben
> zeichengleich.""", True, False, "15.3 (1c)"),
    ("### 36.5 ", "> Text oben bleibt zeichengleich.", """\
> ⭐⭐ **Ergänzungen zu 36.5 — Ausgänge von `auswertung.py` und null Trades
> (43.1, 43-1; 43.2, 43-7; Fable 25d/25e, TB-110, 26.09.2026):** Die offene
> Frage in der Marke darüber ist beantwortet: `auswertung.py` endet mit 0 oder
> **2**, nie mit 1 (**43-1**; vollzogen erst mit der nächsten Öffnung von
> `auswertung.py`). Und: ein Lauf des Laufbereichs, der keine Trades findet,
> schreibt dieses Ergebnis und endet mit 0; unter dem Modus endet ein `exit()`
> ohne geschriebenes Ergebnis mit 2 (**43-7**; zehn weitere Stellen in TB-109,
> Gegenprobe über 24). Beide Texte oben bleiben zeichengleich.""", True, False, "36.5"),
    ("### 37.4 Tatsachennotiz zu Abschnitt 10", "> bleibt zeichengleich.", """\
> ⭐ **Zweite planmässige Öffnung geplant (43.1, 43-4, Fable 25d, TB-110,
> 26.09.2026):** `herkunft.py` wird ein zweites Mal geöffnet, für zwei Dinge in
> **einer** Öffnung — die Prüfansicht übergibt unter dem Modus
> `paths.DATA_DIR`, und `TB30A_BASE_DIR` endet unter dem Modus mit 2, bevor
> gelesen wird —, mit dem Erzeuger oder vor ihm. **Noch nicht vollzogen**
> (`351f24c2…` unverändert). Die Entscheidung oben und ihre Berichtigung
> bleiben zeichengleich.""", True, False, "37.4"),
    ("### 42.6 Was offen bleibt", "| (12) |", """\
> ⭐ **Beantwortet (TB-110, 26.09.2026):** (1) Fable 25d in **43.1**, (2) Fable
> 25e in **43.2** — dazu eine vorläufige Berichtigung des steuernden Chats an
> 25e (3) in **43.3**. (3) Fable 25f bleibt offen (43.5 (9)). Die Tabelle oben
> bleibt zeichengleich.""", True, False, "42.6"),
]


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert len(zeilen) == 9127, len(zeilen)
    assert not any(z.startswith("## 43.") for z in zeilen)
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
    assert len(einfuegen) == 6
    for pos, block, wo in sorted(einfuegen, reverse=True):
        zeilen[pos + 1:pos + 1] = block
    teile = [setze(open(HIER + "abschnitt43_vorlage.md", encoding="utf-8").read().rstrip("\n"), "Abschnitt 43")]
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
    open(REG, "w", encoding="utf-8").write(neu)
    json.dump(zitate, open(HIER + "zitate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Marken:", len(einfuegen), " Zitate:", len(zitate),
          "(Zeilen %d, Teile %d)" % (sum(z["art"] == "zeile" for z in zitate),
                                     sum(z["art"] == "teil" for z in zitate)),
          " Registerzeilen:", len(neu.split("\n")) - 1)


if __name__ == "__main__":
    main()
