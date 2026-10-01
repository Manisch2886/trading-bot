#!/usr/bin/env python3
"""
registerkopie.py - die Registerkopie fuer die Projektablage, in Teilen mit festen Namen (TB-118, Fable 27b B3/Teil D A1)
======================================================================================================================
Das Register `docs/VORREGISTRIERUNG_neuselektion.md` ist zu gross, um in der Projektablage als eine Datei
vollstaendig gelesen zu werden (gemessen 24.09.2026: eine Kopie kam bei 262 144 Bytes abgeschnitten an).
Dieses Skript schneidet es deshalb in Teile, **nur an Abschnittsgrenzen** (Zeilen `^## <n>\\.`), jeder Teil
hoechstens 240 000 Bytes gross (Kopf eingerechnet, der Body ist damit erst recht darunter), und schreibt

    docs/projektfuehrung/REGISTER_KOPIE_teil<n>.md

Zeile 1 jeder Datei ist der Kopf, Zeile 2 leer, ab Zeile 3 steht der Body unveraendert (bytegleich):

    # REGISTER-KOPIE Teil <n> von <m> — Abschnitte <a>–<b> — Commit <hash> — <Datum> — Original sha256 <…> — KOPIE, nicht das Register

<hash> ist der letzte Commit, der das Register geaendert hat (`git log -1 -- <register>`), <Datum> sein
Commit-Datum. Damit ergibt ein zweiter Lauf ohne Registeraenderung dieselben Dateien, gleich an welchem HEAD.
Gelesen wird das Register **am HEAD** (`git show HEAD:<register>`); weicht die Datei im Arbeitsbaum davon ab,
bricht das Skript mit 2 ab - eine Kopie eines uncommitteten Stands waere keine Kopie eines Commits.
Die Vorrede vor Abschnitt 0 gehoert zu Teil 1.

Aufrufe (aus der Repo-Wurzel):
    python3 docs/werkzeuge/registerkopie.py                 Teile schreiben, danach selbst pruefen
    python3 docs/werkzeuge/registerkopie.py --pruefen       nur pruefen: Bodies aneinandergehaengt == Original am
                                                            Commit aus dem Kopf (bytegleich), jeder Teil <= Grenze
    python3 docs/werkzeuge/registerkopie.py --marken        alle Marken "ERSETZT durch"/"PRÄZISIERT durch" (Art MARKE),
                                                            Zeilen mit ERSETZT/PRÄZISIERT/BERICHTIGT/ERGÄNZT/KORRIGIERT
                                                            in anderer Form (MARKE+) und Ueberschriften mit Rueckverweis
                                                            (UEBERSCHRIFT), je mit Zeile, Abschnitt, Teil - die Grundlage
                                                            fuer docs/projektfuehrung/REGISTER_INDEX.md
    python3 docs/werkzeuge/registerkopie.py --abschnitte    eine Datei je Abschnitt (F1, Betreiber 01.10.2026), danach
                                                            selbst pruefen; Standardziel docs/projektfuehrung/register_kopie
    python3 docs/werkzeuge/registerkopie.py --abschnitte --pruefen
                                                            nur pruefen: jede Datei 00..<m> da, Kopf in der Form unten,
                                                            Bodies aneinander == Original am Commit aus dem Kopf (bytegleich)
    --ziel <ordner>                                         anderer Ausgabeordner (Probe); Standard je Modus:
                                                            Teile docs/projektfuehrung, Abschnitte .../register_kopie

Abschnitts-Modus (`--abschnitte`, TB-127, aus der Vorlage `registerkopie_abschnitte.py`): je Abschnitt eine Datei

    <ziel>/REGISTER_KOPIE_ABSCHNITT_<nn>.md        (nn zweistellig, 00 .. letzter Abschnitt)

Zeile 1 Kopf, Zeile 2 leer, ab Zeile 3 der Body unveraendert (bytegleich); die Vorrede gehoert zu Abschnitt 00:

    # REGISTER-KOPIE Abschnitt <n> (von 0–<m>) — Register-Z. <a>–<b> — Commit <hash> — <Datum> — Original sha256 <…> — KOPIE, nicht das Register

<hash>/<Datum> wie im Teile-Modus. Die Abschnittsnummern muessen bei 0 beginnen und fortlaufend sein (sonst 2);
`--marken` zusammen mit `--abschnitte` ergibt 2.

Wann laufen lassen: im Registerauftrag nach dem Registercommit (27b C2), danach Teile committen; der steuernde
Chat legt sie in der Ablage ab und ersetzt die vorigen gleichen Namens. Seit 01.10.2026 fuehrt die Ablage die
Abschnittsdateien (`--abschnitte`, F1); REGISTER_INDEX.md nennt je Abschnitt die Datei.

Rueckgabewert: 0 in Ordnung; 1 Pruefung gescheitert (Body ungleich, Teil zu gross, Teil fehlt);
2 Eingabe unbrauchbar (Arbeitsbaum != HEAD, Abschnittsnummern nicht fortlaufend, kein Commit,
--marken mit --abschnitte);
3 geschrieben, aber ein Abschnitt allein ist groesser als die Grenze (Befund, Teil trotzdem geschrieben).
Das Skript loescht nichts. Liegen aeltere Teile (bzw. Abschnittsdateien) mit hoeherer Nummer als <m> im Ziel,
werden sie gemeldet (VERALTET), nicht entfernt. Reine Standardbibliothek, laeuft auf Python 3.9.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

REGISTER = "docs/VORREGISTRIERUNG_neuselektion.md"
ZIEL = "docs/projektfuehrung"
NAME = "REGISTER_KOPIE_teil{}.md"
GRENZE = 240000
ZIEL_ABSCHNITTE = "docs/projektfuehrung/register_kopie"
NAME_ABSCHNITT = "REGISTER_KOPIE_ABSCHNITT_{:02d}.md"
ABSCHNITT = re.compile(rb"^## (\d+)\.", re.M)
KOPF = re.compile(r"^# REGISTER-KOPIE Teil (\d+) von (\d+) — Abschnitte (\d+)–(\d+) — Commit ([0-9a-f]{40}) — "
                  r"(\d{4}-\d{2}-\d{2}) — Original sha256 ([0-9a-f]{64}) — KOPIE, nicht das Register$")
KOPF_ABSCHNITT = re.compile(r"^# REGISTER-KOPIE Abschnitt (\d+) \(von 0–(\d+)\) — Register-Z\. (\d+)–(\d+) — "
                            r"Commit ([0-9a-f]{40}) — (\d{4}-\d{2}-\d{2}) — Original sha256 ([0-9a-f]{64}) — "
                            r"KOPIE, nicht das Register$")
MARKE = re.compile(r"ERSETZT durch|PRÄZISIERT durch")              # das Suchmuster aus dem Auftrag (27b Teil D A4)
MARKE_WEITER = re.compile(r"\b(ERSETZT|PRÄZISIERT|BERICHTIGT|ERGÄNZT|KORRIGIERT)\b")  # weitere Markenwoerter
RUECKVERWEIS = re.compile(r"Berichtigung zu|Präzisierung zu|ersetzt die|Ergänzung zu|, Ergänzung|, Präzisierung|"
                          r"Berichtigung$|Berichtigung —")


def git(*args):
    return subprocess.run(["git"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def original_am_head():
    """(Bytes am HEAD, letzter Registercommit, dessen Datum). Abbruch 2, wenn der Arbeitsbaum abweicht."""
    daten = git("show", "HEAD:" + REGISTER)
    with open(REGISTER, "rb") as f:
        if f.read() != daten:
            print("ABBRUCH: %s im Arbeitsbaum weicht vom HEAD ab - erst committen." % REGISTER)
            sys.exit(2)
    zeile = git("log", "-1", "--format=%H %cd", "--date=short", "--", REGISTER).decode().split()
    if len(zeile) != 2:
        print("ABBRUCH: kein Commit fuer %s gefunden." % REGISTER)
        sys.exit(2)
    commit, datum = zeile
    if git("show", commit + ":" + REGISTER) != daten:
        print("ABBRUCH: Register am HEAD != Register am letzten Registercommit %s." % commit)
        sys.exit(2)
    return daten, commit, datum


def abschnitte(daten):
    """Liste (nummer, start, ende) in Bytes; die Vorrede gehoert zum ersten Abschnitt."""
    treffer = [(int(m.group(1)), m.start()) for m in ABSCHNITT.finditer(daten)]
    nummern = [n for n, _ in treffer]
    if not treffer or nummern != list(range(nummern[0], nummern[0] + len(nummern))):
        print("ABBRUCH: Abschnittsnummern nicht fortlaufend: %s" % nummern)
        sys.exit(2)
    grenzen = [0] + [s for _, s in treffer[1:]] + [len(daten)]
    return [(nummern[i], grenzen[i], grenzen[i + 1]) for i in range(len(nummern))]


def kopf(n, m, a, b, commit, datum, sha):
    return ("# REGISTER-KOPIE Teil %d von %d — Abschnitte %d–%d — Commit %s — %s — Original sha256 %s — "
            "KOPIE, nicht das Register\n\n" % (n, m, a, b, commit, datum, sha)).encode("utf-8")


def schneiden(daten, commit, datum):
    """Gierig: Abschnitte in Reihenfolge, solange Kopf + Body <= GRENZE. Liefert (teile, befunde)."""
    sha = hashlib.sha256(daten).hexdigest()
    reserve = len(kopf(99, 99, 999, 999, commit, datum, sha))
    gruppen, aktuell, befunde = [], [], []
    for nr, s, e in abschnitte(daten):
        if e - s + reserve > GRENZE:
            befunde.append("BEFUND: Abschnitt %d allein %d Bytes - groesser als die Grenze %d; eigener Teil."
                           % (nr, e - s, GRENZE))
        if aktuell and aktuell[-1][2] - aktuell[0][1] + (e - s) + reserve > GRENZE:
            gruppen.append(aktuell)
            aktuell = []
        aktuell.append((nr, s, e))
    gruppen.append(aktuell)
    m = len(gruppen)
    teile = []
    for i, g in enumerate(gruppen, 1):
        body = daten[g[0][1]:g[-1][2]]
        teile.append((i, g[0][0], g[-1][0], kopf(i, m, g[0][0], g[-1][0], commit, datum, sha) + body))
    return teile, befunde


def pfad(ziel, n):
    return os.path.join(ziel, NAME.format(n))


def pruefen(ziel):
    """Bodies aneinander == Original am Commit aus dem Kopf; jeder Teil <= GRENZE. rc 0/1."""
    fehler = 0
    erster = pfad(ziel, 1)
    if not os.path.exists(erster):
        print("FEHLT: %s" % erster)
        return 1
    with open(erster, "rb") as f:
        k = KOPF.match(f.readline().decode("utf-8").rstrip("\n"))
    if not k:
        print("KOPF unlesbar: %s" % erster)
        return 1
    m, commit, sha_kopf = int(k.group(2)), k.group(5), k.group(7)
    original = git("show", commit + ":" + REGISTER)
    bodies = []
    for n in range(1, m + 1):
        p = pfad(ziel, n)
        if not os.path.exists(p):
            print("FEHLT: %s" % p)
            return 1
        with open(p, "rb") as f:
            inhalt = f.read()
        kopfzeile, _, body = inhalt.partition(b"\n\n")
        kk = KOPF.match(kopfzeile.decode("utf-8"))
        if not kk or int(kk.group(1)) != n or int(kk.group(2)) != m or kk.group(5) != commit:
            print("KOPF passt nicht: %s" % p)
            fehler += 1
        groesse = len(inhalt)
        ok = groesse <= GRENZE
        fehler += 0 if ok else 1
        print("Teil %d: %s  %d Bytes gesamt, Body %d Bytes, Abschnitte %s–%s  %s"
              % (n, p, groesse, len(body), kk.group(3) if kk else "?", kk.group(4) if kk else "?",
                 "<= %d" % GRENZE if ok else "ZU GROSS"))
        bodies.append(body)
    zusammen = b"".join(bodies)
    gleich = zusammen == original
    print("Bodies aneinander: %d Bytes, Original %s am %s: %d Bytes, sha256 %s (Kopf %s) - %s"
          % (len(zusammen), REGISTER, commit[:12], len(original), hashlib.sha256(original).hexdigest()[:16],
             sha_kopf[:16], "BYTEGLEICH" if gleich else "UNGLEICH"))
    if hashlib.sha256(original).hexdigest() != sha_kopf:
        print("sha256 im Kopf passt nicht zum Original am Commit")
        fehler += 1
    fehler += 0 if gleich else 1
    n = m + 1
    while os.path.exists(pfad(ziel, n)):
        print("VERALTET: %s liegt noch (Teil %d > m=%d) - nicht Teil dieser Kopie, nicht entfernt" % (pfad(ziel, n), n, m))
        n += 1
    return 0 if fehler == 0 else 1


def pfad_abschnitt(ziel, n):
    return os.path.join(ziel, NAME_ABSCHNITT.format(n))


def kopf_abschnitt(n, m, za, zb, commit, datum, sha):
    return ("# REGISTER-KOPIE Abschnitt %d (von 0–%d) — Register-Z. %d–%d — Commit %s — %s — Original sha256 %s — "
            "KOPIE, nicht das Register\n\n" % (n, m, za, zb, commit, datum, sha)).encode("utf-8")


def je_abschnitt(daten, commit, datum):
    """Liste (nummer, inhalt) mit Kopf; Register-Zeilen a–b wie in der Vorlage (1-basiert, b einschliesslich)."""
    liste = abschnitte(daten)
    if liste[0][0] != 0:
        print("ABBRUCH: Abschnittsnummern beginnen nicht bei 0: %d" % liste[0][0])
        sys.exit(2)
    sha = hashlib.sha256(daten).hexdigest()
    m = liste[-1][0]
    ergebnis = []
    for nr, s, e in liste:
        za = daten.count(b"\n", 0, s) + 1
        zb = daten.count(b"\n", 0, e) + (1 if e == len(daten) and not daten.endswith(b"\n") else 0)
        ergebnis.append((nr, kopf_abschnitt(nr, m, za, zb, commit, datum, sha) + daten[s:e]))
    return ergebnis


def pruefen_abschnitte(ziel):
    """Jede Datei 00..<m> da, Kopf in der Form, Bodies aneinander == Original am Commit aus dem Kopf. rc 0/1."""
    erster = pfad_abschnitt(ziel, 0)
    if not os.path.exists(erster):
        print("FEHLT: %s" % erster)
        return 1
    with open(erster, "rb") as f:
        k = KOPF_ABSCHNITT.match(f.readline().decode("utf-8").rstrip("\n"))
    if not k:
        print("KOPF unlesbar: %s" % erster)
        return 1
    m, commit, datum, sha_kopf = int(k.group(2)), k.group(5), k.group(6), k.group(7)
    original = git("show", commit + ":" + REGISTER)
    fehler = 0
    bodies = []
    zeile = 1
    for n in range(0, m + 1):
        p = pfad_abschnitt(ziel, n)
        if not os.path.exists(p):
            print("FEHLT: %s" % p)
            return 1
        with open(p, "rb") as f:
            inhalt = f.read()
        teile = inhalt.split(b"\n", 2)
        kk = KOPF_ABSCHNITT.match(teile[0].decode("utf-8")) if len(teile) == 3 else None
        body = teile[2] if len(teile) == 3 else b""
        za_soll, zb_soll = zeile, zeile + body.count(b"\n") - 1
        if (not kk or teile[1] != b"" or int(kk.group(1)) != n or int(kk.group(2)) != m or kk.group(5) != commit
                or kk.group(6) != datum or kk.group(7) != sha_kopf
                or int(kk.group(3)) != za_soll or int(kk.group(4)) != zb_soll):
            print("KOPF passt nicht: %s" % p)
            fehler += 1
        zeile = zb_soll + 1
        bodies.append(body)
    zusammen = b"".join(bodies)
    gleich = zusammen == original
    print("Abschnitte 0–%d: %d Dateien in %s; Bodies aneinander: %d Bytes, Original %s am %s: %d Bytes, "
          "sha256 %s (Kopf %s) - %s" % (m, m + 1, ziel, len(zusammen), REGISTER, commit[:12], len(original),
                                         hashlib.sha256(original).hexdigest()[:16], sha_kopf[:16],
                                         "BYTEGLEICH" if gleich else "UNGLEICH"))
    if hashlib.sha256(original).hexdigest() != sha_kopf:
        print("sha256 im Kopf passt nicht zum Original am Commit")
        fehler += 1
    fehler += 0 if gleich else 1
    n = m + 1
    while os.path.exists(pfad_abschnitt(ziel, n)):
        print("VERALTET: %s liegt noch (Abschnitt %d > m=%d) - nicht Teil dieser Kopie, nicht entfernt"
              % (pfad_abschnitt(ziel, n), n, m))
        n += 1
    return 0 if fehler == 0 else 1


def abschnitte_schreiben(ziel):
    daten, commit, datum = original_am_head()
    liste = je_abschnitt(daten, commit, datum)
    os.makedirs(ziel, exist_ok=True)
    for nr, inhalt in liste:
        with open(pfad_abschnitt(ziel, nr), "wb") as f:
            f.write(inhalt)
        print("geschrieben: %s  %d Bytes" % (pfad_abschnitt(ziel, nr), len(inhalt)))
    return pruefen_abschnitte(ziel)


def marken():
    """Alle Marken und Rueckverweis-Ueberschriften mit Zeile, Abschnitt, Teil (Zuschnitt wie beim Schreiben)."""
    daten, commit, datum = original_am_head()
    teile, _ = schneiden(daten, commit, datum)
    teil_von = {}
    for i, a, b, _ in teile:
        for nr in range(a, b + 1):
            teil_von[nr] = i
    abschnitt, unter = None, "-"
    print("# Marken im Register am Commit %s (%s); Spalten: Zeile | Abschnitt | Teil | Art | unter | Text (gekuerzt)"
          % (commit[:12], datum))
    print("# 'unter' = der letzte Unterabschnitt (### n.m) oder Eintrag (**A1 —, > **R1 —) vor der Zeile")
    for znr, zeile in enumerate(daten.decode("utf-8").split("\n"), 1):
        m = re.match(r"^## (\d+)\.", zeile)
        if m:
            abschnitt, unter = int(m.group(1)), m.group(1)
        u = re.match(r"^#{3,4} (\d+\.\d+(?:\.\d+)?)\b", zeile)
        e = re.match(r"^(?:> )?\*\*([A-Z]\d{1,2}(?:/[A-Z]\d{1,2})?)(?: \([a-z]+\))? —", zeile)
        if u:
            unter = u.group(1)
        elif e and abschnitt is not None:
            unter = "%s %s" % (unter.split(" ")[0], e.group(1))
        art = None
        if MARKE.search(zeile):
            art = "MARKE"
        elif MARKE_WEITER.search(zeile):
            art = "MARKE+"
        elif re.match(r"^#{2,4} ", zeile) and RUECKVERWEIS.search(zeile):
            art = "UEBERSCHRIFT"
        if art:
            print("%5d | %s | %s | %s | %s | %s" % (znr, abschnitt if abschnitt is not None else "-",
                                                    teil_von.get(abschnitt, 1), art, unter, zeile.strip()[:230]))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--pruefen", action="store_true")
    ap.add_argument("--marken", action="store_true")
    ap.add_argument("--abschnitte", action="store_true")
    ap.add_argument("--ziel", default=None)
    a = ap.parse_args()
    if a.abschnitte:
        if a.marken:
            print("ABBRUCH: --marken und --abschnitte zusammen sind nicht vorgesehen.")
            return 2
        ziel = a.ziel if a.ziel is not None else ZIEL_ABSCHNITTE
        return pruefen_abschnitte(ziel) if a.pruefen else abschnitte_schreiben(ziel)
    a.ziel = a.ziel if a.ziel is not None else ZIEL
    if a.marken:
        return marken()
    if a.pruefen:
        return pruefen(a.ziel)
    daten, commit, datum = original_am_head()
    teile, befunde = schneiden(daten, commit, datum)
    os.makedirs(a.ziel, exist_ok=True)
    for i, von, bis, inhalt in teile:
        with open(pfad(a.ziel, i), "wb") as f:
            f.write(inhalt)
        print("geschrieben: %s  Abschnitte %d–%d  %d Bytes" % (pfad(a.ziel, i), von, bis, len(inhalt)))
    for b in befunde:
        print(b)
    rc = pruefen(a.ziel)
    if rc == 0 and befunde:
        return 3
    return rc


if __name__ == "__main__":
    sys.exit(main())
