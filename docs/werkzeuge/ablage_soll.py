#!/usr/bin/env python3
"""
ablage_soll.py - Soll-Liste der Projektablage aus dem Repo-Stand (TB-118, Fable 27b C1 und Teil D Schritt E)
===========================================================================================================
Es gibt keinen Upload und keine Ausschlussliste, sondern eine SOLL-Liste (27b C1). Dieses Skript leitet aus dem
Repo ab, was nach 27b Teil B in der Projektablage liegen soll, vergleicht mit der IST-Liste, die der steuernde Chat
aus der Projektschnittstelle holt, und schreibt drei Listen:

    soll.txt       was in der Ablage liegen soll (ein Pfad je Zeile, relativ zu docs/, Grund dahinter)
    entfernen.txt  was in der Ablage liegt und nach Teil B hinaus soll (mit Klasse und Austrittsgrund)
    ablegen.txt    was fehlt und abgelegt werden soll (Soll minus Ist; "fehlt im Repo" markiert)
    ohne_regel.txt was in der Ablage liegt und zu keiner Regel passt - wird NICHT entfernt, sondern gemeldet

Aufruf (aus der Repo-Wurzel):
    python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner> [--heute JJJJ-MM-TT]
<ist.txt>: ein Pfad je Zeile, wie ihn die Projektschnittstelle nennt (z. B. projektfuehrung/BACKLOG.md,
auftraege/MAC_TB-110_register_43.md); Leerzeilen und Zeilen mit # werden uebergangen. Verglichen wird ueber den
Dateinamen, weil die Ablage Ordner nur als Namensteil fuehrt.

Die Regeln stehen fest hier im Skript, je mit Verweis auf 27b Teil B:
  B1 Regelwerk: feste Namensliste REGELWERK; Nachtraege zum Regelwerk ueber ablage_ereignisse.json.
  B2 Stand: feste Namensliste STAND. Ein datiertes Standdokument (<NAME>_<datum>.md) verlaesst die Ablage, sobald
     es <NAME>.md im Repo gibt; gibt es sie nicht, bleibt das juengste datierte (Uebergang, bis die Datei ohne
     Datum angelegt ist). Nur-Repo: BACKLOG_ERLEDIGT_*, BACKLOG_SICHTSCHUTZ.md, BACKLOG_ARCHIV.md, BACKLOG_EPICS.md.
  B3 Register: REGISTER_KOPIE_teil<n>.md (wie im Repo vorhanden) und REGISTER_INDEX.md; datierte Kopien hinaus.
  B4 Auftraege: MAC_TB-nnn (auch NACHTRAG_<k>_MAC_TB-nnn) ist offen, wenn kein docs/ERGEBNIS_TB-nnn_*.md existiert
     (gesucht auch unter belege/TB-nnn/ und als Nachtrag in einem ERGEBNIS, das den Auftrag mit Namen nennt)
     ODER die zugehoerige Antwort im Index "offen" ist. Zugehoerig = die Fable-Antwort, die der Auftrag in seinen
     ersten acht Zeilen nennt (FABLE_ANTWORT_<datum><b> oder "Fable <tt><b>").
  B5 Ergebnisse: ERGEBNIS_TB-nnn bleibt, wenn eine FABLE_ANFRAGE_* es zitiert, deren Antwort im Index "offen" ist,
     deren Antwort fehlt, oder deren Antwort nicht "registriert" ist (Registerauftrag fehlt).
  B6 Dialog: ein Paar (Antwort + ihre Anfrage laut Index-Spalte "Anfrage") bleibt, wenn der Index "offen" sagt oder
     die Antwort eine der zwei juengsten (Datum und Buchstabe) ist. Eine Anfrage ohne Antwort bleibt, wenn sie
     juenger ist als die juengste Antwort. FABLE_WOCHENRUECKMELDUNG_* und FABLE_UEBERGABE_*: nur die juengste bleibt.
  B7 Belege: alles unter belege/ - vor dem Tag nie in der Ablage.
  B8 ereignisgebunden: nach ablage_ereignisse.json (Datei -> Ereignis -> erfuellt / Frist).
Index: docs/projektfuehrung/FABLE_DIALOG_INDEX.md (dialog_index.py). Reine Standardbibliothek, Python 3.9.
Rueckgabewert 0; 2 bei unbrauchbarer Eingabe. Das Skript loescht und legt nichts ab - das tut der steuernde Chat.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

DOCS = "docs"
PF = os.path.join(DOCS, "projektfuehrung")
INDEX = os.path.join(PF, "FABLE_DIALOG_INDEX.md")
EREIGNISSE = os.path.join(DOCS, "werkzeuge", "ablage_ereignisse.json")

REGELWERK = ["ARBEITSWEISE.md", "PRUEFPRINZIPIEN.md", "DOKUMENTATIONSSTANDARD.md", "UMZUG.md",
             "SITZUNGSWAECHTER_ausloeser_statt_tippen.md"]                                     # 27b B1
STAND = ["UEBERGABE.md", "BACKLOG.md", "BACKLOG_ENTSCHEIDUNGEN.md", "PLAN_VOR_DEM_TAG.md", "AUFGABEN_BETREIBER.md",
         "PROJEKTSTAND_einfache_sprache.md", "FABLE_DIALOG_INDEX.md", "KANDIDATEN_DURCHGANG_2.md"]  # 27b B2
# BACKLOG_ENTSCHEIDUNGEN.md statt "ENTSCHEIDUNGEN.md": Betreiberentscheidung 27.09.2026 (TB-118 C1)
NUR_REPO = re.compile(r"^(BACKLOG_ERLEDIGT_.*|BACKLOG_SICHTSCHUTZ|BACKLOG_ARCHIV|BACKLOG_EPICS)\.md$")  # 27b B2
DATIERT = re.compile(r"^(?P<name>[A-Za-z_]+?)_(?P<datum>\d{4}-\d{2}-\d{2})[a-z]?\.md$")


def repo_dateien():
    """Dateiname -> Pfad relativ zu docs/ (erste Fundstelle; belege/ ausgenommen)."""
    aus = {}
    for p in sorted(glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(p, DOCS)
        if rel.startswith("belege" + os.sep):
            continue
        aus.setdefault(os.path.basename(p), rel)
    return aus


def ergebnis_zu(nr, auftragsname):
    """Das Ergebnis eines Auftrags: docs/ERGEBNIS_TB-<nr>_*.md, docs/belege/TB-<nr>/ERGEBNIS_TB-<nr>*.md, oder ein
    ERGEBNIS_*.md, das den Auftrag mit Dateinamen nennt (Nachtrag in einem anderen Ergebnis). Gemessen 27.09.2026:
    TB-79 steht in ERGEBNIS_TB-78 (Nachtrag TB-78b), TB-88 unter docs/belege/TB-88/."""
    treffer = glob.glob(os.path.join(DOCS, "ERGEBNIS_TB-%s_*.md" % nr)) + \
        glob.glob(os.path.join(DOCS, "belege", "TB-%s" % nr, "ERGEBNIS_TB-%s*.md" % nr))
    if treffer:
        return treffer
    for p in glob.glob(os.path.join(DOCS, "ERGEBNIS_*.md")):
        with open(p, encoding="utf-8") as f:
            if auftragsname in f.read():
                return [p]
    return []


def lies_index():
    """Antwort-Schluessel (z. B. '27a') -> {status, offen, anfragen:[Schluessel], name}."""
    idx = {}
    if not os.path.exists(INDEX):
        print("ABBRUCH: %s fehlt" % INDEX)
        sys.exit(2)
    with open(INDEX, encoding="utf-8") as f:
        for z in f:
            t = [x.strip() for x in z.strip().strip("|").split("|")]
            if len(t) != 9 or not re.match(r"^\d\d[a-z]?$", t[0]):
                continue
            anfr = re.findall(r"\b(\d\d[a-z]?)\b", t[7].split(";")[0])
            idx[t[0]] = {"status": t[4], "offen": t[6] == "ja", "anfragen": anfr, "name": t[8].strip("`")}
    return idx


def schluessel(name, art):
    m = re.match(r"^FABLE_%s_2026-09-(\d\d[a-z]?)_" % art, name)
    return m.group(1) if m else None


def reihenfolge(k):
    return (k[:2], k[2:])


def soll_ableiten(repo, idx, heute):
    soll = {}                                   # Dateiname -> Grund

    def setze(name, grund):
        soll.setdefault(name, grund)

    for n in REGELWERK:
        setze(n, "B1 Regelwerk")
    for n in STAND:
        if n in repo:
            setze(n, "B2 Stand")
        else:
            basis = n[:-3]
            datiert = sorted(d for d in repo if DATIERT.match(d) and DATIERT.match(d).group("name") == basis)
            if datiert:
                setze(datiert[-1], "B2 Stand (Uebergang: %s fehlt im Repo, juengste datierte Fassung)" % n)
            else:
                setze(n, "B2 Stand - FEHLT IM REPO")
    for n in sorted(repo):
        if re.match(r"^REGISTER_KOPIE_teil\d+\.md$", n):
            setze(n, "B3 Register, Teil")
    setze("REGISTER_INDEX.md", "B3 Register, Index")

    # B4 Auftraege
    for n, rel in sorted(repo.items()):
        m = re.match(r"^(?:NACHTRAG_\d+_)?MAC_TB-(\d+[a-z]?)_", n)
        if not m:
            continue
        nr = m.group(1)
        ergebnis = ergebnis_zu(nr, n)
        with open(os.path.join(DOCS, rel), encoding="utf-8") as f:
            kopf = "".join(f.readlines()[:8])
        antw = set(re.findall(r"FABLE_ANTWORT_2026-09-(\d\d[a-z]?)_", kopf)) | set(re.findall(r"Fable (\d\d[a-z])\b", kopf))
        offen_antw = sorted(a for a in antw if idx.get(a, {}).get("offen"))
        if not ergebnis:
            setze(n, "B4 Auftrag offen: kein ERGEBNIS_TB-%s" % nr)
        elif offen_antw:
            setze(n, "B4 Auftrag offen: zugehoerige Antwort %s im Index offen" % ",".join(offen_antw))

    # B6 Dialog
    antworten = sorted(idx, key=reihenfolge)
    juengste = set(antworten[-2:])
    anfragen_gehalten = set()
    for a in antworten:
        if idx[a]["offen"] or a in juengste:
            grund = "B6 Dialog: Antwort %s %s" % (a, "offen" if idx[a]["offen"] else "unter den zwei juengsten")
            setze(idx[a]["name"], grund)
            for q in idx[a]["anfragen"]:
                anfragen_gehalten.add(q)
    anfragen = {schluessel(n, "ANFRAGE"): n for n in repo if schluessel(n, "ANFRAGE")}
    beantwortet = set(q for a in idx for q in idx[a]["anfragen"])
    for q, n in anfragen.items():
        if q in anfragen_gehalten:
            setze(n, "B6 Dialog: Anfrage zur gehaltenen Antwort")
        elif q not in beantwortet and antworten and reihenfolge(q) > reihenfolge(antworten[-1]):
            setze(n, "B6 Dialog: Anfrage ohne Antwort, juenger als die juengste Antwort")
    for praefix in ("FABLE_WOCHENRUECKMELDUNG_", "FABLE_UEBERGABE_"):
        kand = sorted(n for n in repo if n.startswith(praefix))
        if kand:
            setze(kand[-1], "B6 Sonderfall: juengste %s" % praefix.rstrip("_"))

    # B5 Ergebnisse
    for q, n in anfragen.items():
        with open(os.path.join(DOCS, repo[n]), encoding="utf-8") as f:
            text = f.read()
        zitiert = set(re.findall(r"ERGEBNIS_TB-(\d+[a-z]?)_", text))
        antw = [a for a in idx if q in idx[a]["anfragen"]]
        if not antw:
            warum = "Antwort auf Anfrage %s fehlt" % q
        elif any(idx[a]["offen"] for a in antw):
            warum = "Antwort %s offen" % ",".join(a for a in antw if idx[a]["offen"])
        elif any(idx[a]["status"] != "registriert" for a in antw):
            warum = "Registerauftrag zu %s fehlt" % ",".join(a for a in antw if idx[a]["status"] != "registriert")
        else:
            continue
        for nr in sorted(zitiert):
            for p in glob.glob(os.path.join(DOCS, "ERGEBNIS_TB-%s_*.md" % nr)):
                setze(os.path.basename(p), "B5 Ergebnis: zitiert von Anfrage %s, %s" % (q, warum))

    # B8 ereignisgebunden
    with open(EREIGNISSE, encoding="utf-8") as f:
        ereignisse = json.load(f)["eintraege"]
    return soll, ereignisse


def ereignis_fuer(name, ereignisse, heute):
    for e in ereignisse:
        if e.get("datei") == name or (e.get("muster") and name.startswith(e["muster"])):
            if "frist" in e:
                erfuellt = heute >= e["frist"]
            else:
                erfuellt = bool(e.get("erfuellt"))
            return e, erfuellt
    return None, None


def klasse_ist(name, rel_ist, repo, soll, ereignisse, heute):
    """(bleibt?, Grund) fuer eine Datei der Ist-Liste."""
    if rel_ist.startswith("belege/") or "/belege/" in rel_ist or name.startswith("TB-") and "belege" in rel_ist:
        return False, "B7 Beleg - vor dem Tag nie in der Ablage"
    e, erfuellt = ereignis_fuer(name, ereignisse, heute)
    if e is not None:
        return (not erfuellt), "B8 %s: %s" % ("Ereignis eingetreten" if erfuellt else "Ereignis offen", e["ereignis"])
    if name in soll:
        return True, soll[name]
    if NUR_REPO.match(name):
        return False, "B2 nur Repo"
    if re.match(r"^REGISTER_KOPIE_", name):
        return False, "B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md"
    m = DATIERT.match(name)
    if m and m.group("name") + ".md" in STAND:
        return False, "B2 datierte Fassung - %s.md liegt im Repo" % m.group("name")
    if re.match(r"^(?:NACHTRAG_\d+_)?MAC_TB-", name):
        return False, "B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen)"
    if re.match(r"^ERGEBNIS_TB-", name):
        return False, "B5 Ergebnis ohne offene Anfrage"
    if re.match(r"^FABLE_(ANFRAGE|ANTWORT)_", name):
        return False, "B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten)"
    if re.match(r"^FABLE_(WOCHENRUECKMELDUNG|UEBERGABE)_", name):
        return False, "B6 Sonderfall: nicht die juengste Fassung"
    return None, "keine Regel"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--ist", required=True)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--heute", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    repo = repo_dateien()
    idx = lies_index()
    soll, ereignisse = soll_ableiten(repo, idx, a.heute)
    with open(a.ist, encoding="utf-8") as f:
        ist = [z.strip() for z in f if z.strip() and not z.startswith("#")]
    ist_namen = {os.path.basename(p): p for p in ist}
    if len(ist_namen) != len(ist):
        print("HINWEIS: %d Ist-Pfade, %d verschiedene Dateinamen" % (len(ist), len(ist_namen)))
    # ereignisgebundene Dateien des Repos, deren Ereignis offen ist, gehoeren ins Soll
    for e in ereignisse:
        if "datei" in e:
            _, erfuellt = ereignis_fuer(e["datei"], ereignisse, a.heute)
            if not erfuellt and e["datei"] in repo:
                soll.setdefault(e["datei"], "B8 Ereignis offen: %s" % e["ereignis"])
    entfernen, bleibt, ohne = [], [], []
    for p in ist:
        n = os.path.basename(p)
        b, grund = klasse_ist(n, p, repo, soll, ereignisse, a.heute)
        if b is None:
            ohne.append((p, grund))
        elif b:
            bleibt.append((p, grund))
            soll.setdefault(n, grund)
        else:
            entfernen.append((p, grund))
    ablegen = []
    for n, grund in sorted(soll.items()):
        if n not in ist_namen:
            ort = repo.get(n)
            ablegen.append((ort or n, grund if ort or "FEHLT IM REPO" in grund else grund + " - FEHLT IM REPO"))
    os.makedirs(a.aus, exist_ok=True)

    def schreibe(datei, zeilen, kopf):
        with open(os.path.join(a.aus, datei), "w", encoding="utf-8") as f:
            f.write("# %s - ablage_soll.py, Stand %s, Ist-Liste %s (%d Pfade)\n" % (kopf, a.heute, os.path.basename(a.ist), len(ist)))
            for p, g in zeilen:
                f.write("%s\t%s\n" % (p, g))

    schreibe("soll.txt", sorted((repo.get(n, n), g) for n, g in soll.items()), "SOLL (%d)" % len(soll))
    schreibe("entfernen.txt", entfernen, "ENTFERNEN (%d)" % len(entfernen))
    schreibe("ablegen.txt", ablegen, "ABLEGEN (%d)" % len(ablegen))
    schreibe("ohne_regel.txt", ohne, "OHNE REGEL (%d) - nicht entfernen, pruefen" % len(ohne))
    print("Ist %d | Soll %d | entfernen %d | bleibt %d | ablegen %d | ohne Regel %d"
          % (len(ist), len(soll), len(entfernen), len(bleibt), len(ablegen), len(ohne)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
