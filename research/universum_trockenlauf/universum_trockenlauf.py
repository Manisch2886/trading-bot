#!/usr/bin/env python3
"""
Universum-Trockenlauf (TB-40) - welche Symbole macht der Loader je Falte handelbar?
==============================================================================
Rein lesend. Es wird keine Datei unter `data/`, `results/` oder
`research/*/ergebnisse/` geschrieben oder veraendert; der Schreibschutz im
Kindprozess erzwingt das und meldet jeden Versuch.

    python3 research/universum_trockenlauf/universum_trockenlauf.py --nur-universum
    python3 research/universum_trockenlauf/universum_trockenlauf.py --nur-universum --json bericht.json
    python3 research/universum_trockenlauf/universum_trockenlauf.py --stille-filter

WARUM ES DIESES WERKZEUG GIBT
------------------------------------------------------------------------------
Zwei Implementierungen beantworten heute dieselbe Frage, und sie sind bereits
auseinandergelaufen:

* `research/faltenplan_neun/faltenplan_neun.py` fragt **"liegen Kursdaten
  vor?"** (Registertext 3a, Lesart A) und kommt fuer die Krypto-Tagesbots auf
  6 / 9 / 13 / 13 / 13 / 17 / 18, Bestaetigung 23. Diese Zahlen stehen heute
  als Tatsachennotiz in `docs/VORREGISTRIERUNG_neuselektion.md`, Abschnitt
  16.1.1 (bis zum Registernachtrag TB-41: 15.5).
* Der **Loader des Bots** fragt etwas anderes: **"reicht die Historie?"**
  (`MIN_HISTORY_DAYS`, bei `elliott_wave` `MIN_HISTORY_HOURS`). Am 16.09.2026
  laedt `strategies/rsi2_crypto/multi_symbol_optimise.py` deshalb **20 von 24**
  Symbolen und nicht 23.

Registertext 3b (Beratungsantwort vom 15.09.2026) entscheidet die Frage:

    "Ein Symbol gehoert zu einer Selektionsfalte, wenn der Loader des Bots es
    mit den registrierten Einstellungen (MIN_HISTORY_DAYS, Indikator-Vorlauf,
    Symboldatei) an mindestens einem Handelstag der Falte handelbar macht. Die
    Symbolzahl je Falte wird durch einen Trockenlauf des Laufcodes
    (--nur-universum) erzeugt und eingetragen; ein anderes Werkzeug ist dafuer
    nicht zulaessig."

WOHIN DAS WERKZEUG GEHOERT - DIE ENTSCHEIDUNG UND IHRE BEGRUENDUNG
------------------------------------------------------------------------------
Die Festlegung nennt `--nur-universum`. Ob das ein Argument eines vorhandenen
Programms ist oder ein eigenes Werkzeug, ist offen gelassen. Entschieden ist:
**eigenstaendiges Werkzeug unter `research/`, aufgerufen mit `--nur-universum`.**

Drei Gruende:

1. **Das Programm, an das die Option gehoert haette, gibt es noch nicht.** Der
   spaetere Auswerter des Selektionslaufs ist `research/vorregistrierung/
   auswertung.py` - und der ist **eingefroren** (Register 15.8 Nr. 3), rechnet
   noch nach Verfahren A und wird erst in TB-30b umgestellt. Eine Option an eine
   eingefrorene Datei zu haengen, ist kein Entwurf, sondern ein Verstoss.
2. **Die Frage wird vor dem Lauf gebraucht, nicht waehrend.** Die Symbolzahl je
   Falte ist eine **Tatsachennotiz**, die vor dem signierten Tag ins Register
   kommt. Sie muss ohne Raster, ohne Kennzahl und ohne Auswerter erzeugbar
   sein.
3. **Die Option bleibt trotzdem die registrierte.** `--nur-universum` ist hier
   die Aufrufform; wenn der Auswerter in TB-30b entsteht, ruft er dieses
   Werkzeug auf oder importiert `messe_bot()`, statt die Frage ein viertes Mal
   zu beantworten. Genau dafuer gibt es die Funktion.

DIE ZWEI LESARTEN VON "JE FALTE" - UND WARUM BEIDE AUSGEWIESEN WERDEN
------------------------------------------------------------------------------
Die Aufgabenbeschreibung und der Registertext sagen nicht dasselbe, und das
aendert Zahlen:

  **H - "an mindestens einem Handelstag der Falte"** (Registertext 3b,
      woertlich). Gemessen am **letzten** Zeitpunkt der Falte.
  **F - "die Schranke wird am Faltenbeginn geprueft"** (Aufgabenbeschreibung
      TB-40, Abschnitt "Nicht verhandelbar"). Gemessen am **ersten** Zeitpunkt
      der Falte.

F ist strenger als H. Beide werden gemessen und nebeneinander ausgewiesen; die
Entscheidung, welche eingetragen wird, ist eine **Registerfrage** und wird hier
nicht getroffen. Dass H am Faltenende genuegt, ist keine Annahme, sondern folgt
daraus, dass jede der neun Schranken eine **nicht fallende** Groesse mit einer
Konstanten vergleicht (Zeitspanne bzw. Kerzenzahl der sichtbaren Daten). Das
Werkzeug prueft diese Monotonie ueber alle Stichtage nach und meldet, wenn sie
irgendwo verletzt ist - es verlaesst sich nicht darauf.

WAS "JE FALTE" TECHNISCH HEISST
------------------------------------------------------------------------------
Der Loader sieht die Kursdatei **bis zum Stichtag** und sonst nichts. Alles
andere - Schranke, Leerlauf-Test, Streichung unvollstaendiger Kerzen,
Zehnjahresfenster der Aktien-Bots - laeuft unveraendert im Bot-Code ab. Wie das
gemacht ist und warum es kein Nachbau ist, steht im Kopf von `loaderlauf.py`.

GEGENSTAND DES VERGLEICHS
------------------------------------------------------------------------------
* die **eingetragene Zahl** aus `docs/VORREGISTRIERUNG_neuselektion.md`,
  Abschnitt **16.1.1** (gelesen, nie geschrieben). Seit dem Registernachtrag
  TB-41 gibt es zwei Tabellen mit derselben Kopfzeile: 16.1.1 ist die
  gueltige, 15.5 die als "ERSETZT" gekennzeichnete Vorfassung. Welche benutzt
  wurde, steht in der Ausgabe; mit `--register-abschnitt` laesst sich die
  andere waehlen,
* die **namentlichen Listen** aus `research/faltenplan_neun/faltenplan_neun.py`
  (Lesart A). Dieses Werkzeug wird aufgerufen, nicht veraendert.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

BASIS = os.environ.get("TB40_BASE_DIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIER = os.path.dirname(os.path.abspath(__file__))
REGISTER = os.path.join(BASIS, "docs", "VORREGISTRIERUNG_neuselektion.md")
FALTENPLAN = os.path.join(BASIS, "research", "faltenplan_neun", "faltenplan_neun.py")

BOTS = [
    "elliott_wave", "t3_supertrend", "rsi2_crypto", "turtle_soup_crypto",
    "volatility_breakout_crypto", "elliott_wave_stocks", "rsi2_mean_reversion",
    "turtle_soup_stocks", "volatility_breakout",
]

# Registertext 4b: Mindestzahl Selektionsfalten je Bot.
MINDESTFALTEN = 3


# ---------------------------------------------------------------------------
# 1. Das Register lesen
# ---------------------------------------------------------------------------
_ZEILE = re.compile(r"^\|\s*`([a-z0-9_]+)`\s*\|(.+)$")
_UEBERSCHRIFT = re.compile(r"^#{1,6}\s")

# Es gibt ZWEI Tabellen mit derselben Kopfzeile. Welche gilt, steht hier -
# einmal, benannt, und nicht als "die erste, die wir finden".
TABELLE_GUELTIG = "16.1.1"       # Registernachtrag TB-41: die korrigierten Zahlen
TABELLE_HISTORISCH = "15.5"      # als "ERSETZT" gekennzeichnete Vorfassung


def _ohne_zitat(zeile):
    """Streift die Blockzitat-Zeichen ab.

    Noetig, weil die GUELTIGE Tabelle in 16.1.1 als Blockzitat steht (`> |`),
    die historische in 15.5 dagegen nicht. Ohne das findet der Parser nur die
    historische - das war TB-43, Fehler 3.
    """
    s = zeile.strip()
    while s.startswith(">"):
        s = s[1:].lstrip()
    return s


def lies_register(pfad=REGISTER, abschnitt=TABELLE_GUELTIG):
    """Liest die Tatsachennotiz zu 3b: Symbolzahl je Falte, Bestaetigung,
    Universum - aus einem BENANNTEN Registerabschnitt.

    Bis TB-43 nahm diese Funktion schlicht die erste Tabelle, deren Kopfzeile
    'Symbolzahl je Selektionsfalte' enthaelt. Seit dem Registernachtrag TB-41
    ist das die HISTORISCHE, als ersetzt gekennzeichnete Fassung in 15.5; die
    gueltigen Zahlen stehen in 16.1.1. Ein Lauf gegen 15.5 meldet deshalb
    wieder acht Abweichungen, obwohl das Register stimmt.

    Der Abschnitt ist jetzt ein Argument, sein Standard ist die gueltige
    Tabelle, und welcher benutzt wurde, steht in der Ausgabe. Ein Werkzeug,
    das gegen eine von zwei Tabellen prueft, ohne zu sagen gegen welche, ist
    die naechste blinde Wache.

    Nicht abgetippt: aendert jemand eine Zahl im Register, aendert sich das
    Ergebnis dieses Werkzeugs. Genau das verlangt der Test 'Der Vergleich
    meldet eine Abweichung'.
    """
    with open(pfad, encoding="utf-8") as f:
        zeilen = f.read().splitlines()

    # 1. Die Ueberschrift des verlangten Abschnitts.
    kopf = re.compile(r"^#{1,6}\s+" + re.escape(abschnitt) + r"(\s|$)")
    beginn = None
    for i, z in enumerate(zeilen):
        if kopf.match(z.strip()):
            beginn = i
            break
    if beginn is None:
        raise ValueError("Registerabschnitt %s nicht gefunden in %s"
                         % (abschnitt, pfad))

    # 2. Die Tabelle DARIN - und nur darin: bei der naechsten Ueberschrift ist
    #    Schluss, sonst griffe der Parser stillschweigend auf die Tabelle des
    #    folgenden Abschnitts durch.
    start = None
    for i in range(beginn + 1, len(zeilen)):
        s = _ohne_zitat(zeilen[i])
        if _UEBERSCHRIFT.match(zeilen[i].strip()):
            break
        if "Symbolzahl je Selektionsfalte" in s and s.startswith("|"):
            start = i
            break
    if start is None:
        raise ValueError("Tabelle 'Symbolzahl je Selektionsfalte' steht nicht "
                         "in Abschnitt %s von %s" % (abschnitt, pfad))

    eintraege = {}
    for z in zeilen[start + 1:]:
        s = _ohne_zitat(z)
        if not s.startswith("|"):
            if eintraege:
                break
            continue
        m = _ZEILE.match(s)
        if not m:
            continue
        bot = m.group(1)
        felder = [t.strip() for t in m.group(2).split("|")]
        felder = [t for t in felder if t != ""]
        if len(felder) < 3:
            continue
        falten = [int(x) for x in re.findall(r"\d+", felder[0])]
        eintraege[bot] = {
            "falten": falten,
            "bestaetigung": int(re.findall(r"\d+", felder[1])[0]),
            "universum": int(re.findall(r"\d+", felder[2])[0]),
        }
    if not eintraege:
        raise ValueError("Tabelle in Abschnitt %s gefunden, aber keine "
                         "Bot-Zeile gelesen" % abschnitt)
    return eintraege


def lies_register_faltenliste(pfad=REGISTER):
    """Liest die Tatsachennotiz zu 4d: die Faltenjahre je Bot (Abschnitt 15.6).
    Dient allein der Gegenprobe gegen den Faltenplan - dieses Werkzeug rechnet
    die Falten NICHT selbst aus."""
    with open(pfad, encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    start = None
    for i, z in enumerate(zeilen):
        if "Selektionsfalten" in z and "Faltenl" in z and z.lstrip().startswith("|"):
            start = i
            break
    if start is None:
        return {}
    eintraege = {}
    for z in zeilen[start + 1:]:
        if not z.lstrip().startswith("|"):
            if eintraege:
                break
            continue
        m = _ZEILE.match(z.strip())
        if not m:
            continue
        felder = [t.strip() for t in m.group(2).split("|")]
        felder = [t for t in felder if t != ""]
        if len(felder) < 4:
            continue
        eintraege[m.group(1)] = {"falten_text": felder[2],
                                 "anzahl": int(re.findall(r"\d+", felder[3])[0])}
    return eintraege


# ---------------------------------------------------------------------------
# 2. Den Faltenplan holen (Vergleichsgegenstand, unveraendert aufgerufen)
# ---------------------------------------------------------------------------
def hole_faltenplan(pfad_json=None):
    if pfad_json:
        with open(pfad_json, encoding="utf-8") as f:
            return json.load(f)
    ordner = tempfile.mkdtemp(prefix="tb40_faltenplan_")
    ziel = os.path.join(ordner, "faltenplan.json")
    r = subprocess.run([sys.executable, FALTENPLAN, "--json", ziel],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if r.returncode != 0 or not os.path.exists(ziel):
        raise RuntimeError("faltenplan_neun.py fehlgeschlagen:\n%s"
                           % r.stdout.decode("utf-8", "replace")[-3000:])
    with open(ziel, encoding="utf-8") as f:
        return json.load(f)


def falten_des_bots(plan):
    """[(bezeichnung, von, bis_ausschliesslich, symbole_lesart_a), ...] -
    Selektionsfalten zuerst, Bestaetigungsperiode als letzter Eintrag."""
    raus = []
    for f in plan["selektionsfalten"]:
        jahre = f["jahre"]
        name = str(jahre[0]) if len(jahre) == 1 else "%d-%d" % (jahre[0], jahre[-1])
        raus.append((name, f["von"], f["bis_ausschliesslich"], f["symbole_a"]))
    b = plan["bestaetigungsperiode"]
    raus.append(("Bestaetigung", b["von"], b["bis_ausschliesslich"], b["symbole_a"]))
    return raus


def stichtage_der_falte(von, bis_ausschliesslich):
    """(Faltenbeginn, letzter Zeitpunkt der Falte).

    Die Falte ist halboffen [von, bis). Der letzte Zeitpunkt ist deshalb eine
    Sekunde vor `bis` - nicht `bis` selbst. Das ist kein Schoenheitsfehler: der
    Go-Live-Schnitt 2026-09-01 ist im Register ausdruecklich 'ausschliesslich'.
    """
    import datetime as dt
    b = dt.datetime.strptime(bis_ausschliesslich, "%Y-%m-%d") - dt.timedelta(seconds=1)
    return von + "T00:00:00", b.strftime("%Y-%m-%dT%H:%M:%S")


# ---------------------------------------------------------------------------
# 3. Den Loader messen
# ---------------------------------------------------------------------------
def messe_bot(bot, stichtage, datenordner=None,
              ohne_schreibschutz=False, zeige_ausgabe=False):
    """Ruft den Loader des Bots in einem EIGENEN PROZESS auf und gibt zurueck,
    welche Symbole er je Stichtag handelbar macht.

    Eigener Prozess, weil neun gleichnamige Module sich sonst in `sys.modules`
    verdraengen - siehe Kopf von `loaderlauf.py`.
    """
    import shutil
    ordner = tempfile.mkdtemp(prefix="tb40_lauf_")
    ziel = os.path.join(ordner, "%s.json" % bot)
    befehl = [sys.executable, os.path.join(HIER, "loaderlauf.py"),
              "--bot", bot, "--aus", ziel,
              "--stichtage", ",".join(stichtage)]
    if datenordner:
        # Messwerkzeug (stille_filter, Probelaeufe) - unter dem Selektionsmodus
        # lehnt loaderlauf.py `--daten` mit 2 ab (TB-104).
        befehl += ["--daten", datenordner]
    if ohne_schreibschutz:
        befehl += ["--ohne-schreibschutz"]
    r = subprocess.run(befehl, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if zeige_ausgabe:
        sys.stdout.write(r.stdout.decode("utf-8", "replace"))
    if not os.path.exists(ziel):
        # Die Ablage bleibt stehen, ihr Pfad steht in der Meldung (TB-107,
        # Fable 25b 3 (1) Bedingung (3): "entfernt oder Pfad im Beleg").
        raise RuntimeError("Kindprozess %s ohne Ergebnis (Rueckgabe %d), Ablage bleibt stehen: %s\n%s"
                           % (bot, r.returncode, ordner,
                              r.stdout.decode("utf-8", "replace")[-3000:]))
    # TB-107: die Zwischenablage `tb40_lauf_*` wird entfernt, sobald das
    # Ergebnis gelesen ist (Klasse (iv), Fable 25b 3 (1)); bis TB-107 blieb
    # sie nach jedem Lauf liegen.
    try:
        with open(ziel, encoding="utf-8") as f:
            return json.load(f)
    finally:
        shutil.rmtree(ordner)


# ---------------------------------------------------------------------------
# 4. Der Trockenlauf
# ---------------------------------------------------------------------------
def trockenlauf(faltenplan_json=None, register_pfad=REGISTER, bots=None,
                fortschritt=None, register_abschnitt=TABELLE_GUELTIG):
    bots = bots or BOTS
    plan_alle = hole_faltenplan(faltenplan_json)["plaene"]
    register = lies_register(register_pfad, register_abschnitt)

    # Gegen WELCHE Tabelle verglichen wurde, steht im Bericht - nicht nur im
    # Quelltext.
    bericht = {"bots": {}, "monotonie_verletzt": [], "schreibversuche": [],
               "register_abschnitt": register_abschnitt}
    for bot in bots:
        if fortschritt:
            fortschritt(bot)
        plan = plan_alle[bot]
        falten = falten_des_bots(plan)

        stichtage = []
        for _name, von, bis, _sym in falten:
            a, e = stichtage_der_falte(von, bis)
            stichtage += [a, e]
        stichtage.append("")                      # voller Datenstand = "heute"

        roh = messe_bot(bot, [s for s in stichtage if s] + ["9999-12-31T23:59:59"])
        if roh["fehler"]:
            raise RuntimeError("Loader %s: %s\n%s" % (bot, roh["fehler"],
                                                      roh.get("spur", "")))
        gemessen = {l["stichtag"]: set(l["symbole"]) for l in roh["laeufe"]}
        heute = gemessen["9999-12-31T23:59:59"]

        # Monotonie: die Menge darf ueber die geordneten Stichtage nur wachsen.
        geordnet = sorted(s for s in gemessen if s)
        for frueher, spaeter in zip(geordnet, geordnet[1:]):
            verloren = gemessen[frueher] - gemessen[spaeter]
            if verloren:
                bericht["monotonie_verletzt"].append(
                    {"bot": bot, "von": frueher, "nach": spaeter,
                     "verloren": sorted(verloren)})

        eintrag = {
            "markt": plan["markt"],
            "zeitrahmen": plan["zeitrahmen"],
            "schranken": {k: v for k, v in roh["schranken"].items() if k != "SYMBOLE"},
            "universum": len(roh["schranken"]["SYMBOLE"]),
            "universum_symbole": sorted(roh["schranken"]["SYMBOLE"]),
            "heute_geladen": sorted(heute),
            "register": register.get(bot),
            "falten": [],
        }
        if roh["makedirs_unterdrueckt"]:
            eintrag["makedirs_unterdrueckt"] = roh["makedirs_unterdrueckt"]

        eingetragen = list(register.get(bot, {}).get("falten", []))
        eingetragen_best = register.get(bot, {}).get("bestaetigung")

        for i, (name, von, bis, sym_a) in enumerate(falten):
            a, e = stichtage_der_falte(von, bis)
            menge_f = gemessen[a]
            menge_h = gemessen[e]
            ist_best = (name == "Bestaetigung")
            zahl_reg = eingetragen_best if ist_best else (
                eingetragen[i] if i < len(eingetragen) else None)
            eintrag["falten"].append({
                "falte": name, "von": von, "bis_ausschliesslich": bis,
                "bestaetigung": ist_best,
                "register": zahl_reg,
                "lesart_a_faltenplan": sorted(sym_a),
                "gemessen_H": sorted(menge_h),
                "gemessen_F": sorted(menge_f),
                "H_zusaetzlich": sorted(menge_h - set(sym_a)),
                "H_entfaellt": sorted(set(sym_a) - menge_h),
                "F_zusaetzlich": sorted(menge_f - set(sym_a)),
                "F_entfaellt": sorted(set(sym_a) - menge_f),
                "differenz_H": (len(menge_h) - zahl_reg) if zahl_reg is not None else None,
                "differenz_F": (len(menge_f) - zahl_reg) if zahl_reg is not None else None,
            })
        # Tatsachennotiz 3b, zweiter Halbsatz: "Symbole, die in KEINER
        # Selektionsfalte vorkommen, werden namentlich vermerkt; der gewaehlte
        # Parametersatz gilt fuer sie live ohne Faltenevidenz." Auch diese
        # Liste haengt an der Lesart und wird deshalb mitgemessen.
        univ = set(roh["schranken"]["SYMBOLE"])
        sel = [f for f in eintrag["falten"] if not f["bestaetigung"]]
        best = [f for f in eintrag["falten"] if f["bestaetigung"]][0]
        for lesart in ("H", "F"):
            k = "gemessen_" + lesart
            ver = set()
            for f in sel:
                ver |= set(f[k])
            eintrag["ohne_faltenevidenz_" + lesart] = sorted(univ - ver)
            eintrag["nie_dabei_" + lesart] = sorted(univ - (ver | set(best[k])))
        bericht["bots"][bot] = eintrag

    bericht["register_faltenliste"] = lies_register_faltenliste(register_pfad)
    return bericht


# ---------------------------------------------------------------------------
# 5. Die Mindestgrenze aus Registertext 4b
# ---------------------------------------------------------------------------
def faltenbilanz(eintrag, lesart):
    """Wie viele Selektionsfalten traegt der Bot noch, wenn leere Falten nicht
    zaehlen? Gibt (anzahl_mit_symbolen, anzahl_leer, anzahl_hoechstens_eins)
    zurueck. Was davon 'zaehlt', entscheidet das Register, nicht dieses
    Werkzeug - hier wird nur ausgezaehlt."""
    schluessel = "gemessen_" + lesart
    sel = [f for f in eintrag["falten"] if not f["bestaetigung"]]
    leer = sum(1 for f in sel if len(f[schluessel]) == 0)
    hoechstens_eins = sum(1 for f in sel if len(f[schluessel]) <= 1)
    return len(sel) - leer, leer, hoechstens_eins


# ---------------------------------------------------------------------------
# 6. Ausgabe
# ---------------------------------------------------------------------------
def _reihe(zahlen):
    return " / ".join(str(z) for z in zahlen)


def drucke(bericht):
    br = "=" * 118
    print(br)
    print("TB-40 UNIVERSUM-TROCKENLAUF - Symbole je Bot und Falte, gemessen am Loader des Bots")
    print(br)
    print()
    print("Lesart H = Registertext 3b woertlich: handelbar an mindestens einem Handelstag der Falte")
    print("           (gemessen am letzten Zeitpunkt der Falte)")
    print("Lesart F = Aufgabenbeschreibung TB-40: Schranke am Faltenbeginn geprueft")
    print("           (gemessen am ersten Zeitpunkt der Falte)")
    abschnitt = bericht.get("register_abschnitt", TABELLE_GUELTIG)
    print("Eingetragen = Tatsachennotiz zu 3b, docs/VORREGISTRIERUNG_neuselektion.md "
          "Abschnitt %s (Lesart A)" % abschnitt)
    if abschnitt != TABELLE_GUELTIG:
        print("  ACHTUNG: %s ist NICHT die gueltige Tabelle. Gueltig ist %s; "
              "%s ist die als ERSETZT" % (abschnitt, TABELLE_GUELTIG, abschnitt))
        print("  gekennzeichnete Vorfassung. Abweichungen hier sind zu erwarten "
              "und KEIN Registerfehler.")
    print()

    print("-" * 118)
    print("Die Schranken der neun Loader - GEMESSEN am geladenen Modul, nicht angenommen")
    print("-" * 118)
    print("%-28s %-6s %-22s %-18s %s" % ("Bot", "Raster", "Schranke", "Zehnjahresfenster", "Universum"))
    for bot, e in bericht["bots"].items():
        s = e["schranken"]
        if "MIN_HISTORY_DAYS" in s:
            schranke = "MIN_HISTORY_DAYS %d" % s["MIN_HISTORY_DAYS"]
        elif "MIN_HISTORY_HOURS" in s:
            schranke = "MIN_HISTORY_HOURS %d" % s["MIN_HISTORY_HOURS"]
        else:
            schranke = "keine"
        fenster = s.get("RECENT_YEARS_ONLY")
        print("%-28s %-6s %-22s %-18s %d" % (
            bot, e["zeitrahmen"], schranke,
            "-" if fenster in (None, "None") else "%s Jahre" % fenster, e["universum"]))
    print()

    print("-" * 118)
    print("Symbolzahl je Falte: eingetragen gegen gemessen")
    print("-" * 118)
    print("%-28s %-34s %-34s %s" % ("Bot", "eingetragen (Lesart A)", "gemessen H (Registertext 3b)",
                                    "gemessen F (Faltenbeginn)"))
    for bot, e in bericht["bots"].items():
        sel = [f for f in e["falten"] if not f["bestaetigung"]]
        best = [f for f in e["falten"] if f["bestaetigung"]][0]
        reg = _reihe([f["register"] for f in sel]) + "  | B: %s" % best["register"]
        h = _reihe([len(f["gemessen_H"]) for f in sel]) + "  | B: %d" % len(best["gemessen_H"])
        fz = _reihe([len(f["gemessen_F"]) for f in sel]) + "  | B: %d" % len(best["gemessen_F"])
        print("%-28s %-34s %-34s %s" % (bot, reg, h, fz))
    print()
    print("B = Bestaetigungsperiode.")
    print()

    print("-" * 118)
    print("Differenz je Falte (gemessen minus eingetragen)")
    print("-" * 118)
    for bot, e in bericht["bots"].items():
        sel = [f for f in e["falten"] if not f["bestaetigung"]]
        best = [f for f in e["falten"] if f["bestaetigung"]][0]
        dh = _reihe(["%+d" % f["differenz_H"] for f in sel]) + "  | B: %+d" % best["differenz_H"]
        df = _reihe(["%+d" % f["differenz_F"] for f in sel]) + "  | B: %+d" % best["differenz_F"]
        print("%-28s H: %-40s F: %s" % (bot, dh, df))
    print()

    print("-" * 118)
    print("Namentlich: was gegenueber der eingetragenen Lesart A hinzukommt (+) und wegfaellt (-)")
    print("-" * 118)
    for bot, e in bericht["bots"].items():
        print("\n%s" % bot)
        for f in e["falten"]:
            marke = "B " if f["bestaetigung"] else "  "
            print("  %s%-12s eingetr. %-4s  H %-4s  F %-4s" % (
                marke, f["falte"], f["register"], len(f["gemessen_H"]), len(f["gemessen_F"])))
            for lesart in ("H", "F"):
                plus = f["%s_zusaetzlich" % lesart]
                minus = f["%s_entfaellt" % lesart]
                if plus:
                    print("      %s +  %s" % (lesart, ", ".join(plus)))
                if minus:
                    print("      %s -  %s" % (lesart, ", ".join(minus)))
                if not plus and not minus:
                    print("      %s    (gleiche Liste)" % lesart)
    print()

    print("-" * 118)
    print("Tatsachennotiz 3b, zweiter Halbsatz: Symbole OHNE Faltenevidenz - namentlich")
    print("-" * 118)
    print("Eingetragen sind heute ZWEI Listen, eine je Markt (krypto 6, aktien 1).")
    print("Gemessen am Loader sind es Listen JE BOT - sie fallen auseinander:")
    print()
    for bot, e in bericht["bots"].items():
        for lesart in ("H", "F"):
            ohne = e["ohne_faltenevidenz_" + lesart]
            print("%-28s %s: %2d  %s" % (bot if lesart == "H" else "", lesart,
                                         len(ohne), ", ".join(ohne)))
    print()

    print("-" * 118)
    print("Registertext 4b: mindestens 3 Selektionsfalten je Bot")
    print("-" * 118)
    print("%-28s %-26s %-14s %-16s %s" % ("Bot", "Falten mit >=1 Symbol",
                                          "davon leer", "hoechstens 1",
                                          "kleinste Falte"))
    for bot, e in bericht["bots"].items():
        for lesart in ("H", "F"):
            mit, leer, eins = faltenbilanz(e, lesart)
            sel = [f for f in e["falten"] if not f["bestaetigung"]]
            gesamt = len(sel)
            kleinste = min(len(f["gemessen_" + lesart]) for f in sel)
            warn = ""
            if mit < MINDESTFALTEN:
                warn = "  <-- UNTER 3"
            elif gesamt - eins < MINDESTFALTEN:
                warn = "  <-- unter 3, wenn Ein-Symbol-Falten nicht zaehlen"
            print("%-28s %s: %-23s %-14s %-16s %d Symbol(e)%s" % (
                bot if lesart == "H" else "", lesart,
                "%d von %d" % (mit, gesamt), "%d" % leer, "%d" % eins,
                kleinste, warn))
    print()
    print("'kleinste Falte' ist die Registerfrage aus der Aufgabe: faellt eine fruehe Falte")
    print("auf null oder ein Symbol, ist sie faktisch keine Falte mehr - ist sie dann noch")
    print("zu zaehlen? Die Festlegung sagt dazu nichts. Hier wird nur ausgezaehlt.")
    print()

    if bericht["monotonie_verletzt"]:
        print("!! MONOTONIE VERLETZT - Lesart H am Faltenende ist dann nicht gleichbedeutend")
        print("   mit 'an mindestens einem Handelstag der Falte':")
        for v in bericht["monotonie_verletzt"]:
            print("   %s: %s -> %s verliert %s" % (v["bot"], v["von"], v["nach"],
                                                   ", ".join(v["verloren"])))
    else:
        print("Monotonie geprueft: ueber alle Stichtage waechst die Menge der handelbaren")
        print("Symbole nur. Lesart H am Faltenende ist damit gleichbedeutend mit")
        print("'an mindestens einem Handelstag der Falte'.")
    print()
    print("Rein lesend - es wurde nichts geaendert.")


# ---------------------------------------------------------------------------
# 7. Stille Filter - gemessen, nicht am Quelltext gelesen
# ---------------------------------------------------------------------------
PROBEN = ["voll", "genau_an_der_grenze", "eins_zu_kurz", "datei_fehlt",
          "datei_leer", "nur_leere_kerzen", "luecke_gleiche_spanne"]


def baue_probendaten(ordner, symbole, interval, schranke, einheit):
    """Erzeugt Beispieldaten fuer die Probenrollen. Kein Bot-Code, keine echte
    Kursdatei - und ausdruecklich NICHT der Zustand, den der Test hinterher
    behauptet: was der Loader daraus macht, wird beobachtet."""
    import datetime as dt

    schritt = {"1h": dt.timedelta(hours=1), "4h": dt.timedelta(hours=4),
               "1d": dt.timedelta(days=1)}[interval]
    ende = dt.datetime(2026, 9, 1)

    def schreibe(name, zeilen):
        with open(os.path.join(ordner, "%s_%s.csv" % (name, interval)), "w") as f:
            f.write("open_time,open,high,low,close,volume\n")
            for zeit, leer in zeilen:
                if leer:
                    f.write("%s,,,,,1\n" % zeit.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    f.write("%s,100,101,99,100,1\n" % zeit.strftime("%Y-%m-%d %H:%M:%S"))

    def reihe(n, leer_am_ende=0):
        z = []
        for i in range(n):
            zeit = ende - schritt * (n - 1 - i)
            z.append((zeit, i >= n - leer_am_ende))
        return z

    if einheit == "kerzen":
        n_grenze, n_kurz = schranke, schranke - 1
    else:                                           # Tage-Spanne
        n_grenze = int(schranke / (schritt.total_seconds() / 86400.0)) + 1
        n_kurz = n_grenze - 1

    zuordnung = {}
    for rolle, symbol in zip(PROBEN, symbole):
        zuordnung[rolle] = symbol
        if rolle == "voll":
            schreibe(symbol, reihe(n_grenze * 2))
        elif rolle == "genau_an_der_grenze":
            schreibe(symbol, reihe(n_grenze))
        elif rolle == "eins_zu_kurz":
            schreibe(symbol, reihe(n_kurz))
        elif rolle == "datei_fehlt":
            pass
        elif rolle == "datei_leer":
            schreibe(symbol, [])
        elif rolle == "nur_leere_kerzen":
            schreibe(symbol, [(z, True) for z, _ in reihe(n_grenze * 2)])
        elif rolle == "luecke_gleiche_spanne":
            # Gleiche Zeitspanne wie 'voll', aber nur jede zehnte Kerze. Trennt
            # eine Spannen-Schranke von einer Kerzenzahl-Schranke - am
            # Verhalten, nicht am Quelltext.
            alle = reihe(n_grenze * 2)
            schreibe(symbol, [alle[0]] + alle[1:-1][::10] + [alle[-1]])
    return zuordnung


def stille_filter(bots=None):
    """Haelt jedem der neun Loader dieselben sieben Faelle hin und schaut zu,
    welche er schluckt. Antwortet damit auf 'Gibt es weitere stille Filter?'
    ohne den Quelltext zu befragen."""
    bots = bots or BOTS
    ergebnis = {}
    for bot in bots:
        vorlauf = messe_bot(bot, [])            # nur um Schranken zu erfahren
        if vorlauf["fehler"]:
            raise RuntimeError("%s: %s" % (bot, vorlauf["fehler"]))
        s = vorlauf["schranken"]
        symbole = s["SYMBOLE"]
        interval = s["INTERVAL"]
        if "MIN_HISTORY_HOURS" in s:
            schranke, einheit = s["MIN_HISTORY_HOURS"], "kerzen"
        elif "MIN_HISTORY_DAYS" in s:
            schranke, einheit = s["MIN_HISTORY_DAYS"], "tage"
        else:
            schranke, einheit = 0, "tage"
        if len(symbole) < len(PROBEN):
            raise RuntimeError("%s: Universum zu klein fuer die Proben" % bot)

        ordner = tempfile.mkdtemp(prefix="tb40_proben_")
        zuordnung = baue_probendaten(ordner, symbole[:len(PROBEN)], interval,
                                     schranke, einheit)
        lauf = messe_bot(bot, [], datenordner=ordner)
        if lauf["fehler"]:
            raise RuntimeError("%s (Proben): %s\n%s" % (bot, lauf["fehler"],
                                                        lauf.get("spur", "")))
        geladen = set(lauf["laeufe"][0]["symbole"])
        ausgabe = lauf["laeufe"][0].get("ausgabe", "")
        ergebnis[bot] = {
            "schranke": schranke, "einheit": einheit, "zeitrahmen": interval,
            "proben": {rolle: (zuordnung[rolle] in geladen) for rolle in PROBEN},
            # "still" heisst: aussortiert, ohne dass der Loader das Symbol
            # ueberhaupt erwaehnt. Gemessen an seiner eigenen Ausgabe.
            "still": {rolle: (zuordnung[rolle] not in geladen
                              and zuordnung[rolle] not in ausgabe)
                      for rolle in PROBEN},
            "zuordnung": zuordnung,
        }
    return ergebnis


def drucke_stille_filter(ergebnis):
    print("=" * 118)
    print("STILLE FILTER - was der Loader ausserdem noch aussortiert, gemessen an Beispieldaten")
    print("=" * 118)
    print()
    print("Jedem Loader werden dieselben sieben Faelle hingehalten. 'geladen' heisst: der")
    print("Loader macht das Symbol handelbar. Kein Quelltext gelesen - nur beobachtet.")
    print()
    kopf = "%-28s %-10s %s" % ("Bot", "Schranke", "  ".join("%-14s" % p[:14] for p in PROBEN))
    print(kopf)
    print("-" * len(kopf))
    for bot, e in ergebnis.items():
        def marke(p):
            if e["proben"][p]:
                return "geladen"
            return "STILL raus" if e["still"][p] else "raus, gemeldet"
        marken = "  ".join("%-14s" % marke(p) for p in PROBEN)
        print("%-28s %-10s %s" % (bot, "%d %s" % (e["schranke"], e["einheit"][:4]), marken))
    print()
    print("'STILL raus' = aussortiert, ohne dass der Loader das Symbol in seiner Ausgabe")
    print("ueberhaupt nennt. Auch das ist gemessen, nicht gelesen: mitgeschrieben wurde,")
    print("was der Loader waehrend des Laufs ausgegeben hat.")
    print()
    print("Lesehilfe der sieben Faelle:")
    print("  voll                   Historie weit ueber der Schranke")
    print("  genau_an_der_grenze    exakt die Schranke - hier kippen solche Regeln")
    print("  eins_zu_kurz           eine Einheit darunter")
    print("  datei_fehlt            keine Kursdatei vorhanden")
    print("  datei_leer             Kursdatei nur mit Kopfzeile")
    print("  nur_leere_kerzen       lange Historie, aber alle vier Kursspalten leer")
    print("  luecke_gleiche_spanne  gleiche Zeitspanne wie 'voll', nur jede zehnte Kerze")
    print()
    print("Rein lesend - es wurde nichts geaendert.")


# ---------------------------------------------------------------------------
def main(argv=None):
    p = argparse.ArgumentParser(
        description="TB-40 Universum-Trockenlauf - rein lesend",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--nur-universum", action="store_true",
                   help="Symbole je Bot und Falte (Registertext 3b). Voreinstellung.")
    p.add_argument("--stille-filter", action="store_true",
                   help="Welche Faelle der Loader ausserdem aussortiert - an Beispieldaten "
                        "gemessen. Messwerkzeug (Ersatz-Kursdatenordner): unter dem "
                        "Selektionsmodus nicht moeglich, loaderlauf.py lehnt --daten "
                        "mit 2 ab (TB-104)")
    p.add_argument("--json", default=None, help="Bericht zusaetzlich als JSON ablegen")
    p.add_argument("--faltenplan-json", default=None,
                   help="fertigen faltenplan_neun-Bericht wiederverwenden statt neu zu rechnen")
    p.add_argument("--register", default=REGISTER, help="Registerdatei (nur gelesen)")
    p.add_argument("--register-abschnitt", default=TABELLE_GUELTIG,
                   help="Registerabschnitt mit der Vergleichstabelle. Standard "
                        "%s (gueltig); %s ist die historische, ersetzte Fassung."
                        % (TABELLE_GUELTIG, TABELLE_HISTORISCH))
    p.add_argument("--bot", action="append", default=None, help="nur diesen Bot (mehrfach moeglich)")
    args = p.parse_args(argv)

    bots = args.bot or BOTS

    if args.stille_filter:
        ergebnis = stille_filter(bots)
        drucke_stille_filter(ergebnis)
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump(ergebnis, f, ensure_ascii=False, indent=1)
            print("\nBericht: %s" % args.json)
        return 0

    def melde(bot):
        sys.stderr.write("  ... %s\n" % bot)
        sys.stderr.flush()

    bericht = trockenlauf(args.faltenplan_json, args.register, bots,
                          fortschritt=melde,
                          register_abschnitt=args.register_abschnitt)
    drucke(bericht)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(bericht, f, ensure_ascii=False, indent=1)
        print("\nBericht: %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
