# REGISTER-KOPIE Abschnitt 0 (von 0–55) — Register-Z. 1–51 — Commit ad1fc0d3e5397cec6eb75c5e62de3b1bb7868c24 — 2026-10-07 — Original sha256 ab97ae1e31da161bc1aebed6b00bb2ec6eec07f760c45c645b9801e6e916b9cd — KOPIE, nicht das Register

# Vorregistrierung der Neuselektion (TB-30a)

**Stand: 14.09.2026. Dies ist das Register. Es wird vor dem Lauf eingefroren
und danach nicht mehr verhandelt.**

> ⭐ **Kopf (Stand 14.09.2026) ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (f), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> **Hier wurde kein Selektionslauf gestartet.** Kein Raster gerechnet, kein
> Parametersatz bewertet, kein Ergebnis erzeugt. Wer in diesem Dokument oder
> in `research/vorregistrierung/ergebnisse/` ein Rasterergebnis sucht, sucht
> vergeblich — dort liegen ausschliesslich Vorab-Berechnungen aus Kursdaten
> und Handelskosten.

---

## 0. Warum es dieses Dokument gibt

> ⭐ **Registertext, Ersteintrag — Fundstellen (38.2, Fable 22h, TB-89,
> 23.09.2026):** Ein Registertext nennt Fundstellen im Code als **Datei und
> Bezeichner** (Funktion, Konstante, Zuweisung, Feldname), nicht als
> Zeilennummer. Zeilennummern stehen nur in Tatsachennotizen, zusammen mit dem
> Commit, an dem sie gemessen wurden. *Eine Zeilennummer ohne Commit ist keine
> Fundstelle.* Gilt für jeden Registertext ab Abschnitt 38; ältere Abschnitte
> bleiben zeichengleich, ihre Zeilenangaben gelten für ihren Commit-Stand
> (30.3). Wortlaut, Herkunft und Grund in **38.2**.

Die anstehende Neuselektion ist die **erste echte Optimierung in der
Geschichte dieses Projekts**. Bis hierher wurde auf einem Mass ausgewählt,
das mit dem Zielmass unkorreliert (sechs Bots) oder **negativ** korreliert
war (drei Bots, gemessen in `research/drawdown_reihenfolge/`).

> Datenausbeutung entsteht nicht dort, wo ein Mensch die Zukunft kennt,
> sondern dort, wo ein Mensch **nach** dem Ergebnis noch eine Wahl hat. Jede
> Stelle, an der nach dem Lauf jemand entscheidet — eine Schwelle
> „nachjustiert", ein Rastersegment „ergänzt", ein Bot „vorerst behalten" —,
> ist eine zusätzliche Selektion, **die in keinem N auftaucht**.
>
> **Ziel: Nach dem Lauf gibt es keine Entscheidung mehr, nur eine Lektüre.**

Der Weg dorthin ist Code. Das Skript, das aus den Rohergebnissen die Auswahl
und die Bleibt-Geht-Liste berechnet, ist **vor** dem Lauf geschrieben und
eingefroren: `research/vorregistrierung/auswertung.py`.

**Der Vollständigkeitstest lautete:** *Lässt sich das Auswertungsskript
fertig schreiben, ohne ein einziges Ergebnis gesehen zu haben?* Die Antwort
und die Stellen, an denen dafür eine Lesart festgelegt werden musste, stehen
in Abschnitt 12.

---

