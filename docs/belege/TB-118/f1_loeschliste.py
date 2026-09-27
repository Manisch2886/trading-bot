#!/usr/bin/env python3
"""
TB-118 F1/F2 - Loeschliste mit Bytes und Tokenschaetzung je Datei (Fable 27b Teil D Schritt F).

Eingabe: e3_ausgabe/entfernen.txt und ablegen.txt (ablage_soll.py auf der REKONSTRUIERTEN Ist-Liste, Schritt E).
Bytes: die Fassung am Commit 753ec11 (26.09.2026 22:34, der letzte Stand vor der Betreibermessung um 22:40), sonst
HEAD; Dateien, die nicht im Repo liegen, rekonstruiert (Registerkopien aus dem Registerstand ihres Tages) oder
"nicht messbar". Tokens: die Projektschnittstelle liefert keine Zahl je Datei (Anfrage 27b: nur Gruppensummen), also
Schaetzung, zweifach und so gekennzeichnet:
  (1) kalibriert: Bytes / 2,337 - Verhaeltnis aus vier Gruppen der Betreibermessung, die vollstaendig im Repo liegen
      (BACKLOG.md 105k, UEBERGABE_* 54k, ARBEITSWEISE.md 33k, ERGEBNIS_TB-114..116 32k; 523 387 B / 224 000 Tok);
      Gegenprobe an der Register-Gruppe (735k gemessen): 2,509 B/Tok, die Kalibrierung schaetzt dort rund 7 % zu hoch;
  (2) Naeherung nach Auftrag F1: Bytes / 4.
Schreibt f1_tokens.txt (Tabelle je Datei) und docs/projektfuehrung/LOESCHLISTE_TB-118.md. Aufruf aus der Repo-Wurzel.
"""
import os
import re
import subprocess

B = "docs/belege/TB-118"
K = 523387 / 224000
STAND = "753ec11"
C3 = {1: "Registerkopien 21./22./24.09. (Ganzfassung)", 2: "Registerkopie 24.09. in drei Teilen",
      3: "Fable-Dialog bis 25e", 4: "Aufträge MAC_TB-* und Nachtrag", 5: "Belege", 6: "Übergaben mit Datum",
      7: "ereignisgebunden, Ereignis eingetreten", 0: "nicht in der Sofortliste C3 (Abweichung, e3_probe.txt)"}


def git_bytes(pfad):
    for rev in (STAND, "HEAD"):
        r = subprocess.run(["git", "cat-file", "-s", "%s:%s" % (rev, pfad)], stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL)
        if r.returncode == 0:
            return int(r.stdout), rev
    return None, None


def repo_pfad(name):
    for wurzel in ("docs/projektfuehrung", "docs/auftraege", "docs", "docs/projektfuehrung/nachtraege/_eingearbeitet"):
        p = os.path.join(wurzel, name)
        if os.path.exists(p):
            return p
    return None


def gruppe(name, pfad):
    if name in ("REGISTER_KOPIE_2026-09-21.md", "REGISTER_KOPIE_2026-09-22.md", "REGISTER_KOPIE_2026-09-24.md"):
        return 1
    if name.startswith("REGISTER_KOPIE_2026-09-24_teil"):
        return 2
    m = re.match(r"^FABLE_(?:ANFRAGE|ANTWORT|WOCHENRUECKMELDUNG|UEBERGABE)_2026-09-(\d\d)([a-z]?)", name)
    if m and (m.group(1), m.group(2)) <= ("25", "e"):
        return 3
    if re.match(r"^(NACHTRAG_1_)?MAC_TB-", name):
        return 4
    if pfad.startswith("belege/"):
        return 5
    if name in ("UEBERGABE_2026-09-19.md", "UEBERGABE_2026-09-24.md"):
        return 6
    if name in ("STOFFSAMMLUNG_REGISTER_41_42.md", "AF-F0_BESTANDSAUFNAHME_2026-09-26.md",
                "BACKLOG_NACHTRAG_2026-09-18.md", "JOURNAL_NACHTRAG_2026-09-18.md"):
        return 7
    return 0


def zeilen(datei):
    aus = []
    for z in open(os.path.join(B, "e3_ausgabe", datei), encoding="utf-8"):
        if not z.startswith("#") and z.strip():
            p, _, g = z.rstrip("\n").partition("\t")
            aus.append((p, g))
    return aus


def messen(ablagepfad):
    name = os.path.basename(ablagepfad)
    if name == "REGISTER_KOPIE_2026-09-21.md":
        r = subprocess.run(["git", "cat-file", "-s", "5ff34a4:docs/VORREGISTRIERUNG_neuselektion.md"],
                           stdout=subprocess.PIPE, check=True)
        return int(r.stdout), "rekonstruiert: Register am 5ff34a4 (21.09.), ohne Kopf"
    if name.startswith("REGISTER_KOPIE_2026-09-24_teil"):
        return None, "nicht im Repo; die drei Teile zusammen ~ Ganzfassung 24.09. (552 130 B), je Teil unbekannt"
    alt = {"JOURNAL_NACHTRAG_2026-09-18.md": "docs/projektfuehrung/JOURNAL_NACHTRAG_2026-09-18.md"}
    p = alt.get(name) or repo_pfad(name)
    if p is None:
        return None, "nicht im Repo - nicht messbar"
    b, rev = git_bytes(p)
    if b is None:
        b, rev = os.path.getsize(p), "Arbeitsbaum"
    return b, "%s @ %s" % (p, rev)


def main():
    ent = zeilen("entfernen.txt")
    zeilen_aus, summen = [], {}
    for p, grund in ent:
        n = os.path.basename(p)
        b, herkunft = messen(p)
        g = gruppe(n, p)
        if n.startswith("REGISTER_KOPIE_2026-09-24_teil"):
            b_schaetz = 552130 // 3
        else:
            b_schaetz = b
        zeilen_aus.append((n, p, b, b_schaetz, g, grund, herkunft))
        s = summen.setdefault(g, [0, 0, 0])
        s[0] += 1
        s[1] += b_schaetz or 0
        s[2] += 0 if b_schaetz else 1
    # f1_tokens.txt
    with open(os.path.join(B, "f1_tokens.txt"), "w", encoding="utf-8") as f:
        f.write("# TB-118 F1 - je Datei aus entfernen.txt: Bytes, Tokens kalibriert (Bytes/%.3f), Tokens Bytes/4, C3-Gruppe, Herkunft der Bytezahl\n" % K)
        for n, p, b, bs, g, grund, herk in sorted(zeilen_aus, key=lambda x: (x[4] or 9, x[0])):
            f.write("%-70s %9s %8s %8s  Nr.%d  %s\n" % (n, b if b is not None else ("~%d" % bs if bs else "-"),
                    int(bs / K) if bs else "-", bs // 4 if bs else "-", g, herk))
        tb = sum(s[1] for s in summen.values())
        f.write("# Summe: %d Dateien, %d Bytes (davon geschaetzt: die drei Teile vom 24.09. je 552130/3), Tokens kalibriert %d, Bytes/4 %d; nicht messbar: %d\n"
                % (len(zeilen_aus), tb, tb / K, tb // 4, sum(s[2] for s in summen.values())))
    return zeilen_aus, summen


if __name__ == "__main__":
    z, s = main()
    for g in sorted(s):
        print("Nr.%d %-45s %3d Dateien %9d B  ~%7d Tok (kal.)  %7d Tok (/4)  nicht messbar %d"
              % (g, C3[g], s[g][0], s[g][1], s[g][1] / K, s[g][1] // 4, s[g][2]))
    tb = sum(v[1] for v in s.values())
    print("Summe %d Dateien %d B ~%d Tok (kal.) %d Tok (/4)" % (len(z), tb, tb / K, tb // 4))


def loeschliste(zeilen_aus, summen):
    """docs/projektfuehrung/LOESCHLISTE_TB-118.md - geht in die Ablage (keine Groessen nach 27.1, nur Dateien)."""
    ablegen = zeilen("ablegen.txt")
    rein = []
    for p, grund in ablegen:
        pfad = repo_pfad(os.path.basename(p))
        if pfad is None:
            rein.append((os.path.basename(p), None, grund))
        else:
            rein.append((os.path.basename(p), os.path.getsize(pfad), grund))
    alt_backlog = git_bytes("docs/projektfuehrung/BACKLOG.md")[0]
    neu_backlog = os.path.getsize("docs/projektfuehrung/BACKLOG.md")
    raus_b = sum(s[1] for s in summen.values())
    rein_b = sum(b for _, b, _ in rein if b)
    ziel = "docs/projektfuehrung/LOESCHLISTE_TB-118.md"
    for durchgang in (1, 2):                    # zweiter Durchgang: die Loeschliste selbst zaehlt beim Ablegen mit
        eigen = os.path.getsize(ziel) if os.path.exists(ziel) else 0
        vorher = 1540610
        nachher = vorher - raus_b / K + (rein_b + eigen) / K - (alt_backlog - neu_backlog) / K
        L = []
        L.append("# LÖSCHLISTE TB-118 — was die Projektablage verlassen darf, mit Bytes und geschätzten Tokens")
        L.append("")
        L.append("*Erzeugt von `docs/belege/TB-118/f1_loeschliste.py` (TB-118 Schritt F, Fable 27b Teil D F1/F2), 27.09.2026. "
                 "Geht in die Projektablage, damit der Betreiber per Auswahlkarte freigibt, und verlässt sie nach dem Vollzug "
                 "(`ablage_ereignisse.json`).*")
        L.append("")
        L.append("## ⚠️ Vor dem Vollzug")
        L.append("")
        L.append("1. **Die Liste beruht auf einer rekonstruierten Ist-Liste**, nicht auf der Projektschnittstelle: Die Mac-Sitzung "
                 "liest die Ablage nicht (`docs/belege/TB-118/e3_ist_rekonstruiert.txt`, 145 Pfade aus der Gruppentabelle der "
                 "Anfrage 27b; einige Namen sind Annahmen). **Der steuernde Chat holt die echte Ist-Liste und lässt "
                 "`python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner>` laufen; entfernt wird nur, was in "
                 "dessen `entfernen.txt` steht.** Diese Liste ist die Freigabegrundlage für die Klassen und Gründe, nicht für "
                 "die einzelne Datei.")
        L.append("2. **Reihenfolge nach 27b C4:** zuerst ablegen (Tabelle „Rein“), dann entfernen, dann `knowledge_size` messen "
                 "und eine Zeile in `UEBERGABE.md` schreiben. Nr. 2 (die drei Teile vom 24.09.) erst, wenn die vier neuen "
                 "Teile liegen.")
        L.append("3. ⚠️ **Nicht im Repo** (G1: das Repo ist der Träger): `REGISTER_KOPIE_2026-09-21.md`, die drei Teile vom "
                 "24.09. und die zwei Belege `belege/TB-91_…`, `belege/TB-93_…` liegen nur in der Ablage. Die Registerkopien "
                 "sind aus dem Registerstand ihres Tages rekonstruierbar (Register am `5ff34a4` bzw. an der Kopie vom 24.09. "
                 "im Repo), nicht bytegleich (Kopf). **Vor dem Entfernen entscheiden: ins Repo holen oder ohne Kopie "
                 "entfernen.** Auch `FABLE_ANTWORT_2026-09-25f` liegt nur in der Ablage — sie bleibt (Ereignis offen).")
        L.append("4. **Tokens sind geschätzt**, nicht gemessen — die Projektschnittstelle liefert nur Gruppensummen. "
                 "*kalibriert* = Bytes ÷ %.3f (Verhältnis aus vier Gruppen der Betreibermessung vom 26.09., die ganz im Repo "
                 "liegen: `BACKLOG.md`, `UEBERGABE_*`, `ARBEITSWEISE.md`, `ERGEBNIS_TB-114…116`; Gegenprobe an der Register-"
                 "Gruppe: dort rund 7 %% zu hoch). *÷ 4* = die Näherung aus dem Auftrag; sie liegt gegen die Betreibermessung "
                 "rund 40 %% zu tief. Bytes: Fassung am `753ec11` (26.09., 22:34, der letzte Stand vor der Messung)." % K)
        L.append("")
        L.append("## Summen je Gruppe der Sofortliste (27b C3)")
        L.append("")
        L.append("| Nr. | Gruppe | Dateien | Bytes | Tokens kalibriert | Tokens ÷ 4 |")
        L.append("|---|---|---:|---:|---:|---:|")
        for g in sorted(summen, key=lambda x: (x == 0, x)):
            s = summen[g]
            L.append("| %s | %s%s | %d | %s | ≈ %s | %s |" % (g if g else "–", C3[g],
                     " — davon %d nicht messbar" % s[2] if s[2] else "", s[0], "{:,}".format(s[1]).replace(",", " "),
                     "{:,}".format(int(s[1] / K)).replace(",", " "), "{:,}".format(s[1] // 4).replace(",", " ")))
        L.append("| | **Summe raus** | **%d** | **%s** | **≈ %s** | **%s** |" % (len(zeilen_aus),
                 "{:,}".format(raus_b).replace(",", " "), "{:,}".format(int(raus_b / K)).replace(",", " "),
                 "{:,}".format(raus_b // 4).replace(",", " ")))
        L.append("")
        L.append("## Rein (vorher ablegen)")
        L.append("")
        L.append("| Datei | Bytes | Tokens kalibriert | Grund |")
        L.append("|---|---:|---:|---|")
        for n, b, grund in rein:
            L.append("| `%s` | %s | %s | %s |" % (n, "{:,}".format(b).replace(",", " ") if b else "fehlt im Repo",
                     "≈ " + "{:,}".format(int(b / K)).replace(",", " ") if b else "–", grund))
        L.append("| `LOESCHLISTE_TB-118.md` (diese Datei) | %s | ≈ %s | F2, verlässt die Ablage nach dem Vollzug |"
                 % ("{:,}".format(eigen).replace(",", " "), "{:,}".format(int(eigen / K)).replace(",", " ")))
        L.append("| `BACKLOG.md` wird **ersetzt** (gleicher Name) | %s → %s | ≈ −%s | Teilung, Schritt C |" % (
                 "{:,}".format(alt_backlog).replace(",", " "), "{:,}".format(neu_backlog).replace(",", " "),
                 "{:,}".format(int((alt_backlog - neu_backlog) / K)).replace(",", " ")))
        L.append("")
        L.append("## Erwarteter Stand danach (Schätzung, kalibriert)")
        L.append("")
        L.append("`knowledge_size` am 26.09.: **1 540 610** von 2 000 000 (77 %%). Danach ≈ 1 540 610 − %s (raus) + %s (rein) "
                 "− %s (`BACKLOG.md` kleiner) ≈ **%s ≈ %d %%**. Ziel ≤ 50 %% (27b C2). *Nicht eingerechnet: was seit dem 26.09., "
                 "22:40 in die Ablage kam (z. B. Anfrage und Antwort 27b, falls schon abgelegt) — der steuernde Chat misst "
                 "vorher und nachher.*" % ("{:,}".format(int(raus_b / K)).replace(",", " "),
                 "{:,}".format(int((rein_b + eigen) / K)).replace(",", " "),
                 "{:,}".format(int((alt_backlog - neu_backlog) / K)).replace(",", " "),
                 "{:,}".format(int(nachher)).replace(",", " "), round(nachher / 20000)))
        L.append("")
        L.append("## Die Dateien, je mit Grund (Austrittsereignis nach 27b Teil B)")
        L.append("")
        L.append("| Datei | Bytes | Tokens kalibriert | Tokens ÷ 4 | Nr. | Grund |")
        L.append("|---|---:|---:|---:|---|---|")
        for n, p, b, bs, g, grund, herk in sorted(zeilen_aus, key=lambda x: (x[4] == 0, x[4], x[0])):
            bt = "{:,}".format(b).replace(",", " ") if b is not None else ("≈ " + "{:,}".format(bs).replace(",", " ") if bs else "nicht messbar")
            L.append("| `%s` | %s | %s | %s | %s | %s%s |" % (p, bt, "≈ " + "{:,}".format(int(bs / K)).replace(",", " ") if bs else "–",
                     "{:,}".format(bs // 4).replace(",", " ") if bs else "–", g if g else "–", grund.replace("|", "/"),
                     " ⚠️ nicht im Repo" if ("nicht im Repo" in herk or "rekonstruiert" in herk) else ""))
        L.append("")
        L.append("## In einfacher Sprache")
        L.append("")
        L.append("Diese Liste sagt, welche Dateien aus der Projektablage herausdürfen, wie gross sie sind und warum sie "
                 "gehen. Die Tokenzahlen sind geschätzt, weil die Ablage keine Zahl je Datei nennt. Geschätzt verschwindet "
                 "rund 86 Prozent des heutigen Inhalts; mit den neuen Dateien wäre die Ablage danach zu gut einem Viertel "
                 "gefüllt statt zu drei Vierteln. Vorher legt der steuernde Chat die neuen Dateien ab, holt die echte Liste der Ablage und lässt "
                 "das Skript darüber laufen; gelöscht wird nur, was dort auch steht. Vier Registerkopien und zwei Belege "
                 "gibt es nur in der Ablage, nicht im Repo — über sie wird vorher entschieden.")
        with open(ziel, "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
    return nachher


if __name__ == "__main__":
    z, s = main()
    print("erwartet danach ~%d Tokens" % loeschliste(z, s))
