"""TB-113: Registerabschnitt 44 und sieben Marken am alten Ort.

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
  trading-env/bin/python3 docs/belege/TB-113/eintrag_register_44.py
"""
import json
import os
import re
import subprocess

# TB113_PROBE: Probelauf gegen eine Kopie (Pfad), bevor das Register geschrieben wird
REG = os.environ.get("TB113_PROBE") or "docs/VORREGISTRIERUNG_neuselektion.md"
HIER = "docs/belege/TB-113/"
QUELLEN = {
    "ausw": "research/vorregistrierung/auswertung.py",
    "herk": "research/vorregistrierung/herkunft.py",
    "reg": "git:257e7db:docs/VORREGISTRIERUNG_neuselektion.md",
    "e109": "docs/ERGEBNIS_TB-109_nulltrades_ablagen_stummel.md",
    "e111": "docs/ERGEBNIS_TB-111_herkunft_auswertung_oeffnung.md",
    "e112": "docs/ERGEBNIS_TB-112_19_laufbereich_db_sicherung.md",
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
    ("## 19. Registertext 5e, Ergänzung", "> Register, wie Fable es verlangt. Tabelle und Text oben bleiben zeichengleich.", """\
> ⭐⭐ **Vollzogen in TB-112, siehe 44.2 (44-7; TB-113, 26.09.2026):**
> `ARBEITSBAUM_PFADE` trägt seit `9d711dc` 15 Einträge — `shared`,
> `strategies`, `requirements.lock` und die 12 Module des Laufbereichs
> ausserhalb dieser Ordner als Einzeldateien; `herkunft_protokoll.jsonl` ist
> namentlich ausgenommen (`REGISTRIERTE_PROTOKOLLE`, `:(exclude)`), `data/`
> weiter. Nur unter dem Modus wirksam. Die Liste steht als Tatsachennotiz
> neben der Laufbereichsmessung (44-8). Kasten, Tabelle und Text oben bleiben
> zeichengleich.""", True, False, "19"),
    ("### 36.5 ", "> Gegenprobe über 24). Beide Texte oben bleiben zeichengleich.", """\
> ⭐ **`Abbruch` endet mit 2 seit TB-111, siehe 44.1 (44-1; TB-113,
> 26.09.2026):** Vollzogen in `6c98c38` (Zweig `tb-111`, zusammengeführt in
> `257e7db`): `auswertung.py` endet mit 0 oder 2; die zwölf Stellen und die
> Meldung sind zeichengleich. Die Texte oben bleiben zeichengleich.""", True, False, "36.5"),
    ("### 37.4 Tatsachennotiz zu Abschnitt 10", "> bleiben zeichengleich.", """\
> ⭐ **Zweite Öffnung `herkunft.py` vollzogen, TB-111, siehe 44.1 (44-2;
> TB-113, 26.09.2026):** In `6cacfa4` (zusammengeführt in `257e7db`): die
> Prüfansicht übergibt unter dem Modus `paths.DATA_DIR`, `TB30A_BASE_DIR`
> endet unter dem Modus mit 2 vor dem Lesen, `paths.py` kommt aus der eigenen
> Wurzel. `351f24c2…` ⇒ `5bbfc9e0…`. `EINGEFROREN` bleibt; die Entscheidung
> oben, ihre Berichtigung und die Marke darüber bleiben zeichengleich.""", True, False, "37.4"),
    ("### 42.2 Aus Fable 25b", "Marke bei 19.", """\
> ⭐ **Vollzogen, siehe 44.2 (44-7; TB-112 `9d711dc`, TB-113, 26.09.2026):**
> `ARBEITSBAUM_PFADE` hat 15 Einträge (die 12 Module des Laufbereichs
> ausserhalb `shared/`/`strategies/` als Einzeldateien); die Liste steht als
> Tatsachennotiz neben der Laufbereichsmessung (44-8). Eintrag und Stand oben
> bleiben zeichengleich.""", True, False, "42.2 E2"),
    ("### 42.3 Aus Fable 25c", "nicht** (TB-108, `a3_stand.txt` (2)) und wurde nicht angelegt.", """\
> ⭐ **Vollzogen, siehe 44.2 (44-7; TB-112 `9d711dc`, TB-113, 26.09.2026):**
> Die Ausnahme von 19 steht als `REGISTRIERTE_PROTOKOLLE` (genau
> `herkunft_protokoll.jsonl`) in `shared/paths.py` und wirkt als
> `:(exclude)` in der Sauberkeitsprüfung. Das Protokoll existiert weiter
> nicht. Eintrag und Stand oben bleiben zeichengleich.""", True, False, "42.3 F8"),
    ("### 43.1 Aus Fable 25d", "am alten Ort:** unter **36.5** und in **12**, unter dem Satz über den Abbruch.", """\
> ⭐ **Vollzogen, siehe 44.1 (44-1; TB-111 `6c98c38`, TB-113, 26.09.2026):**
> `Abbruch` endet mit 2; zwölf Stellen, Meldung byte-gleich. `auswertung.py`
> `83c6bc3c…` ⇒ `a864b216…`. „Nicht vollzogen“ oben beschreibt den Stand auf
> `main` vor dem Zusammenführen und bleibt zeichengleich.""", True, False, "43-1"),
    ("### 43.1 Aus Fable 25d", "durch 42.3 F2.", """\
> ⭐ **Vollzogen, siehe 44.1 (44-2; TB-111 `6cacfa4`, TB-113, 26.09.2026):**
> Prüfansicht mit `paths.DATA_DIR`, `TB30A_BASE_DIR` unter dem Modus 2 vor
> dem Lesen, in einer Öffnung. `herkunft.py` `351f24c2…` ⇒ `5bbfc9e0…`.
> „noch nicht vollzogen“ oben beschreibt den Stand vor dem Zusammenführen und
> bleibt zeichengleich.""", True, False, "43-4"),
]


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert len(zeilen) == 9472, len(zeilen)
    assert not any(z.startswith("## 44.") for z in zeilen)
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
    assert len(einfuegen) == 7
    assert len({p for p, _, _ in einfuegen}) == 7
    for pos, block, wo in sorted(einfuegen, reverse=True):
        zeilen[pos + 1:pos + 1] = block
    teile = [setze(open(HIER + "abschnitt44_vorlage.md", encoding="utf-8").read().rstrip("\n"), "Abschnitt 44")]
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
    assert neu.split("\n")[k10:k11] == alt[k10:k11], "Abschnitt 10 verschoben"
    open(REG, "w", encoding="utf-8").write(neu)
    json.dump(zitate, open(HIER + "zitate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Marken:", len(einfuegen), " Zitate:", len(zitate),
          "(Zeilen %d, Teile %d)" % (sum(z["art"] == "zeile" for z in zitate),
                                     sum(z["art"] == "teil" for z in zitate)),
          " Registerzeilen:", len(neu.split("\n")) - 1)


if __name__ == "__main__":
    main()
