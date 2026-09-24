"""TB-96: Registerabschnitt 40, Nachtrag zu 39.8 und neun Marken am alten Ort.

Setzt Fables Texte aus 24a EIN statt sie abzutippen: Platzhalter
  ⟦Z:n⟧        -> Zeile n der Quelle, ohne fuehrendes "> " (die Vorlage setzt "> ")
  ⟦T:n|text⟧   -> text, der wortgleich in Zeile n der Quelle stehen muss
und schreibt jedes Zitat nach zitate.json fuer d2_zitate.py.

Jede Marke wird hinter einer Ankerzeile eingefuegt, die innerhalb ihres
Zielabschnitts (Kopfzeile bis zur naechsten Kopfzeile) GENAU EINMAL vorkommen
muss - sonst Abbruch ohne Schreiben. Nichts wird ersetzt oder entfernt.
Aufruf aus der Repo-Wurzel, genau einmal.
"""
import json
import re

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
QUELLE = "docs/projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md"
HIER = "docs/belege/TB-96/"
q = open(QUELLE, encoding="utf-8").read().split("\n")
zitate = []


def setze(text, wo):
    def zeile(m):
        n = int(m.group(1))
        s = q[n - 1]
        s = s[2:] if s.startswith("> ") else s
        zitate.append({"art": "zeile", "zeile": n, "text": s, "wo": wo})
        return s

    def teil(m):
        n, t = int(m.group(1)), m.group(2)
        assert t in q[n - 1], "Teilzitat nicht in Quellzeile %d: %r" % (n, t)
        zitate.append({"art": "teil", "zeile": n, "text": t, "wo": wo})
        return t
    text = re.sub(r"⟦Z:(\d+)⟧", zeile, text)
    text = re.sub(r"⟦T:(\d+)\|([^⟧]+)⟧", teil, text)
    assert "⟦" not in text and "⟧" not in text
    return text


MARKEN = [
    # (Kopfzeile des Zielabschnitts, Ankerzeile, Text, Leerzeile davor, Leerzeile danach, Ort)
    ("### 5.1 Die Regeln", "   Teil G prüft es maschinell.", """\
   > ⭐⭐ **`G6` liest diese Zeile maschinell — Wortlaut nicht ändern (40.2,
   > Fable 24a, TB-96, 24.09.2026).** `test_vorregistrierung.py`
   > (`_testjahre_aus_register`, Teil G) sucht im ganzen Register genau eine
   > Zeile, die mit `4. **JJJJ und JJJJ sind Testfalten, keine Trainingsjahre.**`
   > beginnt, und liest die Jahre daraus. Umformuliert — auch nur Satzzeichen
   > oder Hervorhebung — oder eine zweite Zeile mit diesem Anfang ⇒ `None` ⇒
   > `G6` rot für alle neun Bots. Eine Änderung der Sache braucht einen eigenen
   > Registereintrag **und** die Anpassung von `G6` im selben Auftrag.""", True, True, "5.1 Nr. 4"),
    ("### 5.4 Welche Bots Zweijahres-Falten bekommen", "Abschnitt 3.", """\
> ⭐⭐ **Eingabedateien nach 23d (40.6, Fable 24a, TB-96, 24.09.2026):** Die
> neun Listen oben (`78e2bc6`, 13.09.2026) sind Eingabe einer Herleitung von
> Registertext (33.2) und fallen unter 23d in voller Form. Sie werden vor dem
> Tag **einmal auf dem registrierten Snapshot mit dem registrierten Code neu
> erzeugt** (Erzeuger unter 36.1), kommen als Punkt auf die Sperrliste, und die
> Faltenlänge wird danach nach dieser Regel neu abgeleitet und gegen 33.2
> verglichen (TB-98). Die alten Listen bleiben als historischer Stand liegen.
> ⚠️ **Nicht registriert ist der Parameterstand, mit dem die Listen erzeugt
> wurden** — dieser Abschnitt nennt ihn nicht; die Neu-Erzeugung trägt ihn als
> Tatsachennotiz hierher (Parameterdateien, Commit, Snapshot, Modus, Hash je
> Liste). Die Schwelle selbst ist registriert (Festlegung 7, 5.1 Nr. 6). Der
> Regeltext oben bleibt zeichengleich.""", True, False, "5.4"),
    ("## 12. Der Vollständigkeitstest", "ab — es füllt nichts auf und überspringt nichts.", """\
> ⭐ **Ergänzung (40.7, Fable 24a, TB-96, 24.09.2026) — jede Mutationsprobe
> hat eine Gegenprobe**, die zeigt, dass sie rot werden kann; eine
> Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung. Vor dem Tag wird
> die Gegenprobe für alle acht einmal geführt und als Tatsachennotiz
> festgehalten (TB-97). Anlass: `F4` hat mit `<=` statt `<` drei Wochen
> „bestanden", ohne je gemessen zu haben. Wortlaut in **40.7**. Die Zahlen
> oben („150 Prüfungen, davon acht Mutationsproben") bleiben zeichengleich;
> der Test zählt heute 165 Prüfungen (40.1).""", True, False, "12"),
    ("### 21.9 Ergänzung", "> erzeugt, TB-92 A4). Ersatztext in **39.1**.", """\
> ⭐⭐ **Tag-Vorbedingung für diesen Test erfüllt (40.1, TB-95/TB-96,
> 24.09.2026):** `test_vorregistrierung.py` (`73c9b837…`, `9e2a071`) läuft
> **165/165, rc 0** — die erste Zeile der Tabelle oben („bleibt **rot** …
> blockierend für den Tag") ist für den Stand vom 23.09.2026 **geschlossen**,
> mit dem Planpunkt „Testannahmen folgen dem Register" (`G6`, `H3`). ⚠️ Weitere
> Änderungen an diesem Test sind beschlossen (40.8 (a)–(c), TB-97); jede muss
> ihn grün hinterlassen. Die Tabelle bleibt zeichengleich.""", True, False, "21.9"),
    ("### 33.2 Der Registertext", "> zeichengleich.", """\
> ⭐⭐ **Die Faltenlänge wird neu abgeleitet und gegen diesen Text verglichen
> (40.6, Fable 24a, TB-96, 24.09.2026):** Die Faltenlänge je Bot oben ruht auf
> den neun TB-24-Listen (`78e2bc6`), die nicht auf dem registrierten Snapshot
> erzeugt sind. Sie werden neu erzeugt (TB-98), die Faltenlänge wird nach 5.4
> abgeleitet und **gegen diesen Text verglichen**: gleich ⇒ Tatsachennotiz;
> verschieden ⇒ **Berichtigung dieses Texts** und allem, was daran hängt
> (Benchmark-Tabelle, Abbild), mit dem Grund „⟦T:33|Eingabe war auf nicht-registriertem Datenstand erzeugt⟧"
> — keine Wahl. Text und Tabelle oben bleiben bis dahin zeichengleich.""", True, False, "33.2"),
    ("### 33.5 Was hier ausdrücklich NICHT getan wird",
     "| ⚠️ | **Entscheidungsvorlage, nicht vollzogen:** ob die Abbild-Datei", """\
> ⭐⭐ **Plan-Punkt 7 rückt vor (40.6/40.8 (g), Fable 24a, TB-96,
> 24.09.2026):** Das Abbild des Faltenplans (33.3) und die Faltenplan-Sonde
> sind die Wache gegen einen Schwellenübertritt, der den Faltenplan eines Bots
> verschiebt — und sie fehlen. ⚠️ **Erzeugt wird das Abbild NACH der
> Neu-Ableitung der Faltenlänge (TB-98), nicht vorher** — sonst bildet es einen
> Stand ab, der gerade geprüft wird (TB-100). Die Tabelle oben bleibt
> zeichengleich; die Freigaben, die sie verlangt, gelten weiter.""", True, False, "33.5"),
    ("### 36.6 Das Abbild der Sperrliste", "> > ⚠️⚠️ **Ergänzt durch 37.3 (Fable 22g", """\
>
> > ⭐ **Ergänzt durch 40.8 (e) (Fable 24a, TB-96, 24.09.2026):** Die Sonde liest **alle drei Gruppen** — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) und `herkunft.py::EINGEFROREN` (39.7) — **aus dem Abbild**, nicht aus ihrem eigenen Code; „⟦T:65|Eine Gruppe, die im Code der Sonde steht, ist ein Literal in einer Wache⟧". Vollzug TB-97, mit Gegenprobe. Der Satz oben bleibt zeichengleich.""", False, False, "36.6"),
    ("### 37.2 Ergänzung zu 36.6", "> Freigabe.", """\
> ⭐ **Die Gruppen kommen aus dem Abbild (40.8 (e), Fable 24a, TB-96,
> 24.09.2026):** Dass die Sonde die Gruppe „bestimmt" als feste Konstante führt
> (`BESTIMMT_NICHT_EINGETRAGEN`), ist nach Fable „⟦T:65|ein Befund, vor dem Tag zu beheben⟧"
> — nicht mehr Handwerk ohne Frist. Die Sonde liest alle drei Gruppen aus dem
> Abbild; das Abbild führt „bestimmt" heute leer (39.3). Gegenprobe: Abbild mit
> erfundenem „bestimmt"-Pfad ⇒ Sonde meldet ihn. TB-97.""", True, False, "37.2"),
    ("### 39.6 ", "Benchmark-Tabelle verlangt.", """\
> ⭐⭐ **Zweiter Anwendungsfall (40.6, Fable 24a, TB-96, 24.09.2026):** Neben
> `messgroessen.json` fallen die **neun TB-24-Listen** unter 23d
> („Eingabestand") in voller Form — Fables Registertext „Ergänzung zu 23d und
> zu 5.4" steht in **40.6**. Der Registertext „Eingabestand eingefrorener
> Ergebnisdateien" selbst ist weiter **nicht** eingetragen. ⚠️ Die Nummer oben
> ist gerückt: `messgroessen.json` ist **TB-101**, nicht TB-96 (40.9 (c)).""", True, False, "39.6"),
    ("### 39.8 ", "diesen Eintrag.", None, True, False, "39.8"),
]


def main():
    reg = open(REG, encoding="utf-8").read()
    assert reg.endswith("\n")
    zeilen = reg[:-1].split("\n")
    assert not any(z.startswith("## 40.") for z in zeilen), "Abschnitt 40 existiert schon"
    kopf = [i for i, z in enumerate(zeilen) if z.startswith("#")]
    einfuegen = []
    for kopfzeile, anker, text, vor, nach, wo in MARKEN:
        k = [i for i in kopf if zeilen[i].startswith(kopfzeile)]
        assert len(k) == 1, (kopfzeile, k)
        ende = min([i for i in kopf if i > k[0]] + [len(zeilen)])
        a = [i for i in range(k[0], ende) if zeilen[i].startswith(anker)]
        assert len(a) == 1, (kopfzeile, anker, a)
        if text is None:
            text = open(HIER + "nachtrag_39_8_vorlage.md", encoding="utf-8").read().rstrip("\n")
        text = setze(text, wo)
        block = ([""] if vor else []) + text.split("\n") + ([""] if nach else [])
        einfuegen.append((a[0], block, wo))
    for pos, block, wo in sorted(einfuegen, reverse=True):
        zeilen[pos + 1:pos + 1] = block
    abschnitt = setze(open(HIER + "abschnitt40_vorlage.md", encoding="utf-8").read().rstrip("\n"),
                      "Abschnitt 40")
    neu = "\n".join(zeilen) + "\n\n" + abschnitt + "\n"
    # Wache fuer G6: genau eine Zeile mit dem Anfang von 5.1 Nr. 4
    g6 = re.compile(r"^4\. \*\*(\d{4}) und (\d{4}) sind Testfalten, keine Trainingsjahre\.\*\*")
    assert sum(1 for z in neu.split("\n") if g6.match(z)) == 1
    open(REG, "w", encoding="utf-8").write(neu)
    json.dump(zitate, open(HIER + "zitate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Marken/Nachtrag:", len(einfuegen), " Zitate:", len(zitate))


if __name__ == "__main__":
    main()
