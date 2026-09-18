#!/usr/bin/env python3
"""
TB-48/TB-49 - Pruefwerkzeug fuer Abschnitt 17 der Vorregistrierung
==============================================================================
Abschnitt 17 der Vorregistrierung traegt **neunzehn Zahlen**, die woanders
gemessen wurden. Genau da geht so etwas kaputt: jemand traegt eine Zahl ein,
die einmal gestimmt hat, und niemand merkt, dass ihre Quelle inzwischen etwas
anderes sagt.

Dieses Werkzeug schreibt keine Zahl ab. Es rechnet jede einzelne **an ihrer
Quelle** nach und stellt sie gegen den Registertext.

⚠️ **Warum es ein zweites Werkzeug gibt.** `research/registernachtrag_tb41/
pruefe_register.py` ist das **TB-41**-Werkzeug; im ganzen Quelltext kommt
Abschnitt 17 nicht vor. Sein "KEIN BEFUND" ist ein Nachweis ueber Abschnitt 15
und 16 - nicht ueber die Richtigkeit von Abschnitt 17. *Ein Pruefer, der die
neuen Texte nicht sieht, meldet gruen ueber den alten Stand.*

HERKUNFT DIESER DATEI (TB-49, gehoert in den Bericht)
------------------------------------------------------------------------------
⚠️ Dieses Werkzeug ist in **TB-48** entstanden und blieb **unversioniert**,
weil der damalige Auftrag Aenderungen unter `research/` untersagte. In den
Unterlagen der TB-49-Sitzung lag es **nicht** bei - nur der Auftragstext. Es
ist deshalb aus der Belegtabelle in `docs/ERGEBNIS_TB-48_registernachtrag.md`,
Abschnitt 4, **neu geschrieben**: dieselben neunzehn Zahlen, dieselben
Quellen, dieselbe Erwartung (genau **eine** Abweichung, Rueckgabewert **1**).
**Ein neu geschriebenes Werkzeug ist kein wiederhergestelltes** - dass es
dieselben Zahlen trifft, ist gemessen und steht in
`docs/ERGEBNIS_TB-49_ausnahme.md`, nicht behauptet.

DIE EINE ERWARTETE ABWEICHUNG
------------------------------------------------------------------------------
⚠️ Pruefung **15** (`frueheste_selektionsfalte`) ist **rot, und das ist
richtig so.** Der beschlossene Wortlaut in 17.3 sagt *"die erste
Selektionsfalte beginnt 2022"*; `research/faltenplan_neun/daten/
faltenplan.json` sagt **2019**. Der Wortlaut bleibt als der registrierte
stehen (so behandelt TB-48 ihn, und 16.7 behandelt die "vierte falsche Zahl"
genauso); massgeblich ist die Befundnotiz darunter. **Dieses Werkzeug meldet
die Abweichung weiter** - ein Werkzeug, das sie wegdefiniert, waere die
stillschweigende Korrektur, die der Auftrag ausdruecklich nicht wollte.

WAS ES NICHT PRUEFT - und warum das hier steht
------------------------------------------------------------------------------
Zwei Zahlen aus Abschnitt 17 sind in der Cloud **strukturell** nicht
nachrechenbar und werden deshalb gar nicht erst angefasst:

  * `pandas_market_calendars` **4.6.1** (17.5) - der Registertext sagt
    ausdruecklich "auf dem Betriebsrechner". Gehoert in den Mac-Testauftrag.
  * **9 766 von ~11 000 Zeilen, max. 1,2e-6** (17.8) - setzt einen echten
    yfinance-Abruf voraus. In der Cloud gesperrt, nach T35.4 bis TB-30b
    ohnehin untersagt. ⚠️ Die Quelle ist selbst nicht reproduzierbar; genau
    das ist der Inhalt des Befunds.

⚠️ Eine Pruefung, die nicht laufen konnte, meldet **`nicht pruefbar`** und
nicht "in Ordnung" - dieselbe Trennung, die `shared/snapshot.py` mit der **2**
macht (Lehre aus TB-45).

DIESES WERKZEUG SCHREIBT NICHTS ausser der optionalen --json-Datei.
`data/` wird ausschliesslich gelesen.

Rueckgabewerte
------------------------------------------------------------------------------
    0   keine Abweichung
    1   mindestens eine Abweichung  (heute: genau eine, siehe oben)
    2   mindestens eine Pruefung war NICHT PRUEFBAR

Nutzung:
    python3 research/registernachtrag_tb48/pruefe_abschnitt17.py
    python3 research/registernachtrag_tb48/pruefe_abschnitt17.py --nur 15
    python3 research/registernachtrag_tb48/pruefe_abschnitt17.py --schnell
"""

import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_HIER))

REGISTER = os.path.join(BASE_DIR, "docs", "VORREGISTRIERUNG_neuselektion.md")
BACKLOG = os.path.join(BASE_DIR, "docs", "projektfuehrung", "BACKLOG.md")
FALTENPLAN = os.path.join(BASE_DIR, "research", "faltenplan_neun", "daten",
                          "faltenplan.json")
EINGABEN_JSON = os.path.join(BASE_DIR, "research", "snapshotgrenze",
                             "ergebnisse", "eingaben.json")
HERKUNFT = os.path.join(BASE_DIR, "research", "vorregistrierung", "herkunft.py")
SNAPSHOT = os.path.join(BASE_DIR, "shared", "snapshot.py")
ZEITABDECKUNG = os.path.join(BASE_DIR, "shared", "zeitabdeckung.py")
DATEN = os.path.join(BASE_DIR, "data")

# Die Sollwerte, wie sie in Abschnitt 17 stehen. ⚠️ Sie sind hier das
# GEPRUEFTE, nicht das Ergebnis: gerechnet wird je Zahl an ihrer Quelle.
SOLL_DATENSTAND = "d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84"
SOLL_KURSDATEIEN = 223
SOLL_SNAPSHOT_HASH = "4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608"
SOLL_BEFUNDE = 36
SOLL_2017_2020 = 20
SOLL_AB_2023 = 16
SOLL_2021_2022 = 0
SOLL_KEIN_ZEUGE = 175
SOLL_KEIN_ZEUGE_AKTIEN = 150
SOLL_KEIN_ZEUGE_KRYPTO_1H = 25
SOLL_SCHWELLE = 0.95

OK = "ok"
ABWEICHUNG = "abweichung"
NICHT_PRUEFBAR = "nicht pruefbar"

# Rueckgabewerte - "konnte nicht messen" ist ein eigener, roter Ausgang
# (dieselbe Trennung wie in shared/snapshot.py, Lehre aus TB-45).
OK_RC = 0
BEFUND_RC = 1
NICHT_PRUEFBAR_RC = 2


# ---------------------------------------------------------------------------
# Module ueber den Dateipfad laden - nicht ueber sys.path
# ---------------------------------------------------------------------------
def _lade(pfad, name):
    """Wie `shared/snapshot.py::lade_herkunft`, und aus demselben Grund:
    `research/` fuehrt gleichnamige Module, die sich ueber den Suchpfad
    gegenseitig verdecken (TB-40)."""
    if not os.path.exists(pfad):
        raise RuntimeError("%s fehlt" % pfad)
    spez = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spez)
    spez.loader.exec_module(modul)
    return modul


def _lies(pfad):
    with open(pfad, "r", encoding="utf-8") as f:
        return f.read()


def _zeitpunkt(text):
    """`2020-10-15` oder `2020-10-15 00:00:00` -> datetime."""
    for form in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(text, form)
        except ValueError:
            continue
    raise ValueError("unlesbarer Zeitpunkt: %r" % text)


# ---------------------------------------------------------------------------
# Die Messungen - je eine, zwischengespeichert, weil mehrere Pruefungen
# dieselbe brauchen und der Lauf ueber 223 Dateien rund eine Minute kostet.
# ---------------------------------------------------------------------------
class Messungen:
    def __init__(self, daten=DATEN, schnell=False):
        self.daten = daten
        self.schnell = schnell
        self._roh = None
        self._stand = None

    def datenstand(self):
        h = _lade(HERKUNFT, "tb48_herkunft")
        return h.datenstand(self.daten)

    def snapshot_hash(self):
        """⚠️ Wie TB-48 ihn gemessen hat: ueber die **Kursdateien**, ohne die
        zwei Symbollisten. Ein Snapshot nach TB-47 nimmt die Listen mit auf
        und traegt deshalb einen **anderen** Namen - das ist kein
        Widerspruch, sondern eine andere Frage. Steht so im Bericht."""
        s = _lade(SNAPSHOT, "tb48_snapshot")
        liste = s.eingabeliste(self.daten, BASE_DIR, ())
        paare = {e["im_snapshot"]: s.quersumme(e["herkunft"]) for e in liste}
        return s.snapshot_hash(paare), len(paare)

    def roh(self):
        """Die Teilkerzen-Pruefung ueber `data/` - einmal, nicht siebenmal."""
        if self._roh is None:
            z = _lade(ZEITABDECKUNG, "tb48_zeitabdeckung")
            self._stand = z.jetzt_utc()
            self._roh = z.pruefe_ordner(self.daten, stand=self._stand)
        return self._roh

    def befunde(self):
        return [e for e in self.roh() if e.get("befunde")]

    def kein_zeuge(self):
        return [e for e in self.roh()
                if any(h.get("art") == "kein_zeuge"
                       for h in e.get("hinweise", []))]

    def faltenplan(self):
        return json.loads(_lies(FALTENPLAN))


# ---------------------------------------------------------------------------
# Die neunzehn Pruefungen
# ---------------------------------------------------------------------------
def p01_nicht_kurs_eingaben(m):
    """Nicht-Kurs-Eingaben im Snapshot: genau zwei, beide Symbollisten."""
    roh = json.loads(_lies(EINGABEN_JSON))
    eingaben = {name for name, e in roh["dateien"].items()
                if e.get("einstufung") == "Eingabe"
                and not name.endswith(".csv")}
    soll = {"sp500_top150.txt", "top25_symbols.txt"}
    return (OK if eingaben == soll else ABWEICHUNG,
            "genau zwei: %s" % ", ".join(sorted(soll)),
            "%d: %s" % (len(eingaben), ", ".join(sorted(eingaben))))


def p02_datenstand_hash(m):
    """Der registrierte Datenstand-Hash ueber `data/`."""
    stand = m.datenstand()
    return (OK if stand["datenstand"] == SOLL_DATENSTAND else ABWEICHUNG,
            SOLL_DATENSTAND[:16] + "…", stand["datenstand"][:16] + "…")


def p03_kursdateien(m):
    """Die Zahl der Kursdateien - dieselbe Funktion."""
    stand = m.datenstand()
    return (OK if stand["dateien"] == SOLL_KURSDATEIEN else ABWEICHUNG,
            SOLL_KURSDATEIEN, stand["dateien"])


def p04_snapshot_hash(m):
    """Der zweite Hash - ueber die Dateien, nicht ueber das Manifest."""
    wert, anzahl = m.snapshot_hash()
    return (OK if wert == SOLL_SNAPSHOT_HASH else ABWEICHUNG,
            "%s… (%d Dateien)" % (SOLL_SNAPSHOT_HASH[:16], SOLL_KURSDATEIEN),
            "%s… (%d Dateien)" % (wert[:16], anzahl))


def p05_teilkerzen_befunde(m):
    """Teilkerzen-Befunde: 36 von 223."""
    b, alle = len(m.befunde()), len(m.roh())
    return (OK if (b, alle) == (SOLL_BEFUNDE, SOLL_KURSDATEIEN)
            else ABWEICHUNG,
            "%d von %d" % (SOLL_BEFUNDE, SOLL_KURSDATEIEN),
            "%d von %d" % (b, alle))


def p06_arten(m):
    """Die Arten der Befunde: ausschliesslich `rand_erste`."""
    arten = {}
    for e in m.befunde():
        for b in e["befunde"]:
            arten[b["art"]] = arten.get(b["art"], 0) + 1
    return (OK if arten == {"rand_erste": SOLL_BEFUNDE} else ABWEICHUNG,
            "{'rand_erste': %d}" % SOLL_BEFUNDE, str(arten))


def p07_letzte_kerze_frei(m):
    """⚠️ Der gefaehrliche Rand: keine Datei mit `rand_letzte`."""
    betroffen = [e["datei"] for e in m.befunde()
                 if any(b["art"] == "rand_letzte" for b in e["befunde"])]
    return (OK if not betroffen else ABWEICHUNG,
            "keine Datei", "%d: %s" % (len(betroffen), betroffen[:5]))


def _jahre(m):
    return [e["erste"][:4] for e in m.befunde()]


def p08_erste_kerze_2017_2020(m):
    """Erste Kerze 2017-2020 - selbst nachgezaehlt, nicht abgeschrieben."""
    n = sum(1 for j in _jahre(m) if "2017" <= j <= "2020")
    return (OK if n == SOLL_2017_2020 else ABWEICHUNG, SOLL_2017_2020, n)


def p09_erste_kerze_ab_2023(m):
    """Erste Kerze ab 2023."""
    n = sum(1 for j in _jahre(m) if j >= "2023")
    return (OK if n == SOLL_AB_2023 else ABWEICHUNG, SOLL_AB_2023, n)


def p10_luecke_2021_2022(m):
    """Zwischen 2020 und 2023 liegt keine erste Kerze - und 20+16 = 36.

    ⚠️ Die Zusatzpruefung gehoert dazu: ohne sie waeren 20 und 16 zwei
    Ausschnitte, die zufaellig 36 ergeben, statt der lueckenlosen Aufteilung,
    als die 17.3 sie fuehrt."""
    jahre = _jahre(m)
    n = sum(1 for j in jahre if j in ("2021", "2022"))
    summe = (sum(1 for j in jahre if "2017" <= j <= "2020")
             + sum(1 for j in jahre if j >= "2023"))
    gut = n == SOLL_2021_2022 and summe == SOLL_BEFUNDE
    return (OK if gut else ABWEICHUNG,
            "0 in 2021/2022, und 20 + 16 = %d" % SOLL_BEFUNDE,
            "%d in 2021/2022, Summe %d" % (n, summe))


def p11_elf_symbole(m):
    """Die 16 Befunde ab 2023 gehoeren zu genau den 11 Symbolen aus T34.9.

    ⚠️ Mengengleichheit, in **beide** Richtungen gezeigt - eine blosse
    Zahlengleichheit ("beide 11") waere keine."""
    gemessen = {e["datei"].rsplit("_", 1)[0] for e in m.befunde()
                if e["erste"][:4] >= "2023"}
    text = _lies(BACKLOG)
    treffer = re.search(r"T34\.9.*?\(([A-Z, ]+)[ ]*[—-]", text)
    if not treffer:
        return (NICHT_PRUEFBAR, "die Liste aus T34.9",
                "T34.9 ist in %s nicht auffindbar" % os.path.basename(BACKLOG))
    aus_backlog = {s.strip() + "USDT" for s in treffer.group(1).split(",")
                   if s.strip()}
    gut = gemessen == aus_backlog and len(gemessen) == 11
    return (OK if gut else ABWEICHUNG,
            "11 Symbole, Differenz in beide Richtungen leer",
            "gemessen %d, T34.9 %d, nur gemessen %s, nur T34.9 %s"
            % (len(gemessen), len(aus_backlog),
               sorted(gemessen - aus_backlog), sorted(aus_backlog - gemessen)))


def p12_kein_zeuge(m):
    """Dateien ohne feineren Zeugen: 175 von 223."""
    n = len(m.kein_zeuge())
    return (OK if n == SOLL_KEIN_ZEUGE else ABWEICHUNG,
            "%d von %d" % (SOLL_KEIN_ZEUGE, SOLL_KURSDATEIEN),
            "%d von %d" % (n, len(m.roh())))


def p13_kein_zeuge_aktien(m):
    """Davon Aktien-Tagesdateien: 150."""
    n = sum(1 for e in m.kein_zeuge()
            if e.get("intervall") == "1d"
            and not str(e.get("symbol", "")).endswith("USDT"))
    return (OK if n == SOLL_KEIN_ZEUGE_AKTIEN else ABWEICHUNG,
            SOLL_KEIN_ZEUGE_AKTIEN, n)


def p14_kein_zeuge_krypto_1h(m):
    """Davon Krypto-Stundendateien: 25. Sie sind der feinste Zeitrahmen -
    fuer sie gibt es per Aufbau keinen feineren Zeugen."""
    n = sum(1 for e in m.kein_zeuge() if e.get("intervall") == "1h")
    return (OK if n == SOLL_KEIN_ZEUGE_KRYPTO_1H else ABWEICHUNG,
            SOLL_KEIN_ZEUGE_KRYPTO_1H, n)


def p15_frueheste_selektionsfalte(m):
    """⚠️⚠️ **Die eine erwartete Abweichung.**

    Der beschlossene Wortlaut in 17.3 sagt 2022. Der Faltenplan sagt 2019 -
    bei **allen neun** Bots, nicht nur bei einem Teil.

    ⚠️ Die Jahreszahl wird **aus dem Registertext gelesen**, nicht hier
    hinterlegt. Sonst pruefte dieses Werkzeug seine eigene Abschrift: wuerde
    der Wortlaut eines Tages berichtigt, meldete es weiter die alte
    Abweichung.
    """
    text = _lies(REGISTER)
    treffer = re.search(r"Die erste Selektionsfalte beginnt \*{0,2}(\d{4})",
                        text)
    if not treffer:
        return (NICHT_PRUEFBAR, "die Jahreszahl aus 17.3",
                "der Satz 'Die erste Selektionsfalte beginnt …' steht nicht "
                "mehr in %s" % os.path.basename(REGISTER))
    im_register = int(treffer.group(1))
    plan = m.faltenplan()
    gemessen = plan.get("frueheste_falte")
    je_bot = sorted({p["erstes_faltenjahr"] for p in plan["plaene"].values()})
    return (OK if gemessen == im_register else ABWEICHUNG,
            "%d (Wortlaut in 17.3)" % im_register,
            "%s (faltenplan.json; erstes Faltenjahr je Bot: %s)"
            % (gemessen, je_bot))


def p16_kurze_kerze_in_geladener_falte(m):
    """⭐ Die Schlussfolgerung, maschinell statt ueber eine Jahreszahl.

    Ueber **alle neun Bots und alle Falten**: faellt eine der kurzen ersten
    Kerzen in ein Faltenfenster, in dem ihr Symbol **geladen** ist? Das ist
    die Frage, an der der Satz *"Kein Symbol-Jahr-Beitrag des Selektionslaufs
    haengt an einer der 36 kurzen ersten Kerzen"* wirklich haengt.
    """
    plan = m.faltenplan()
    kerzen = [(e["datei"].rsplit("_", 1)[0], _zeitpunkt(e["erste"]),
               e["datei"]) for e in m.befunde()]
    treffer = []
    for bot, p in sorted(plan["plaene"].items()):
        for nummer, falte in enumerate(p["selektionsfalten"]):
            von = _zeitpunkt(falte["von"])
            bis = _zeitpunkt(falte["bis_ausschliesslich"])
            geladen = set(falte.get("symbole_a") or [])
            geladen |= set(falte.get("symbole_b") or [])
            for symbol, kerze, datei in kerzen:
                if von <= kerze < bis and symbol in geladen:
                    treffer.append("%s/Falte %d/%s" % (bot, nummer, datei))
    return (OK if not treffer else ABWEICHUNG, 0,
            "%d%s" % (len(treffer),
                      (" - " + ", ".join(treffer[:4])) if treffer else ""))


def p17_schwelle_18_von_19(m):
    """18/19 = 94,7 % reisst die 95-%-Schwelle."""
    quote = 18.0 / 19.0
    return (OK if quote < SOLL_SCHWELLE else ABWEICHUNG,
            "unter 95 %", "%.1f %%" % (quote * 100))


def p18_schwelle_19_von_20(m):
    """19/20 = 95,0 % reisst sie nicht - sie liegt auf der Schwelle."""
    quote = 19.0 / 20.0
    return (OK if quote >= SOLL_SCHWELLE else ABWEICHUNG,
            "nicht unter 95 %", "%.1f %%" % (quote * 100))


def p19_mindestzahl(m):
    """n = 1 / (1 − 0,95) = 20."""
    n = round(1.0 / (1.0 - SOLL_SCHWELLE))
    return (OK if n == 20 else ABWEICHUNG, 20, n)


PRUEFUNGEN = [
    (1, "nicht_kurs_eingaben", p01_nicht_kurs_eingaben),
    (2, "datenstand_hash", p02_datenstand_hash),
    (3, "kursdateien", p03_kursdateien),
    (4, "snapshot_hash", p04_snapshot_hash),
    (5, "teilkerzen_befunde", p05_teilkerzen_befunde),
    (6, "arten_der_befunde", p06_arten),
    (7, "letzte_kerze_frei", p07_letzte_kerze_frei),
    (8, "erste_kerze_2017_2020", p08_erste_kerze_2017_2020),
    (9, "erste_kerze_ab_2023", p09_erste_kerze_ab_2023),
    (10, "luecke_2021_2022", p10_luecke_2021_2022),
    (11, "elf_symbole", p11_elf_symbole),
    (12, "kein_zeuge", p12_kein_zeuge),
    (13, "kein_zeuge_aktien", p13_kein_zeuge_aktien),
    (14, "kein_zeuge_krypto_1h", p14_kein_zeuge_krypto_1h),
    (15, "frueheste_selektionsfalte", p15_frueheste_selektionsfalte),
    (16, "kurze_kerze_in_geladener_falte", p16_kurze_kerze_in_geladener_falte),
    (17, "schwelle_18_von_19", p17_schwelle_18_von_19),
    (18, "schwelle_19_von_20", p18_schwelle_19_von_20),
    (19, "mindestzahl_n", p19_mindestzahl),
]

# Welche Pruefungen den (teuren) Lauf ueber alle 223 Kursdateien brauchen.
BRAUCHT_KURSDATEN = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16}


def pruefe(auswahl=None, daten=DATEN, schnell=False):
    m = Messungen(daten=daten, schnell=schnell)
    bericht = {"werkzeug": "research/registernachtrag_tb48/"
                           "pruefe_abschnitt17.py",
               "daten": os.path.realpath(daten),
               "geprueft": [], "uebersprungen": [], "zeilen": [],
               "befunde": [], "nicht_pruefbar": []}
    for nummer, name, funktion in PRUEFUNGEN:
        if auswahl and nummer not in auswahl and name not in auswahl:
            bericht["uebersprungen"].append(name)
            continue
        if schnell and nummer in BRAUCHT_KURSDATEN:
            bericht["uebersprungen"].append(name)
            continue
        try:
            urteil, soll, ist = funktion(m)
        except Exception as fehler:                       # noqa: BLE001
            urteil, soll, ist = (NICHT_PRUEFBAR, "-",
                                 "%s: %s" % (type(fehler).__name__, fehler))
        zeile = {"nummer": nummer, "pruefung": name, "urteil": urteil,
                 "soll": str(soll), "ist": str(ist),
                 "was": (funktion.__doc__ or "").strip().splitlines()[0]}
        bericht["zeilen"].append(zeile)
        bericht["geprueft"].append(name)
        if urteil == ABWEICHUNG:
            bericht["befunde"].append(zeile)
        elif urteil == NICHT_PRUEFBAR:
            bericht["nicht_pruefbar"].append(zeile)
    return bericht


def drucke(bericht):
    br = "=" * 78
    print(br)
    print("ABSCHNITT 17 DER VORREGISTRIERUNG - die neunzehn Zahlen")
    print(br)
    print("  Daten:     %s" % bericht["daten"])
    print("  geprueft:  %d von %d" % (len(bericht["geprueft"]),
                                      len(PRUEFUNGEN)))
    if bericht["uebersprungen"]:
        print("  uebersprungen: %s" % ", ".join(bericht["uebersprungen"]))
    print()
    zeichen = {OK: "OK ", ABWEICHUNG: "!! ", NICHT_PRUEFBAR: " ? "}
    for z in bericht["zeilen"]:
        print("  [%s] %2d %-32s Soll %-28s Ist %s"
              % (zeichen[z["urteil"]], z["nummer"], z["pruefung"],
                 z["soll"][:28], z["ist"]))
    print()
    if bericht["nicht_pruefbar"]:
        print("  ⚠️ %d Pruefung(en) NICHT PRUEFBAR - das ist nicht 'in "
              "Ordnung':" % len(bericht["nicht_pruefbar"]))
        for z in bericht["nicht_pruefbar"]:
            print("      %d %s: %s" % (z["nummer"], z["pruefung"], z["ist"]))
    if not bericht["befunde"]:
        print("  KEIN BEFUND - jede gepruefte Zahl stimmt mit ihrer Quelle "
              "ueberein.")
    else:
        print("  %d ABWEICHUNG(EN):" % len(bericht["befunde"]))
        for z in bericht["befunde"]:
            print("    [%d %s] Soll %s / Ist %s"
                  % (z["nummer"], z["pruefung"], z["soll"], z["ist"]))
        if [z["nummer"] for z in bericht["befunde"]] == [15]:
            print()
            print("  ⭐ Genau die eine erwartete Abweichung (siehe Kopf "
                  "dieser Datei und Abschnitt 17.3): der beschlossene "
                  "Wortlaut")
            print("     bleibt stehen, massgeblich ist die Befundnotiz "
                  "darunter.")
    print(br)


def falten_je_bot(pfad=FALTENPLAN):
    """Je Bot die frueheste Selektionsfalte - gelesen, nicht abgeschrieben.

    ⚠️ **TB-49, Teil 4.** Zu klaeren war, ob die beiden Zahlen 2022 und 2019
    zwei verschiedene Fragen beantworten (*"2022 ist die frueheste
    **Krypto**-Falte, 2019 die ueber alle neun"*). Diese Ausgabe beantwortet
    das: sie nennt Markt und erstes Faltenjahr je Bot nebeneinander.
    """
    plan = json.loads(_lies(pfad))
    zeilen = []
    for bot, p in sorted(plan["plaene"].items()):
        erste = p["selektionsfalten"][0]
        zeilen.append({
            "bot": bot,
            "markt": p.get("markt"),
            "erstes_faltenjahr": p["erstes_faltenjahr"],
            "erstes_faltenjahr_ohne_schranke":
                p.get("erstes_faltenjahr_ohne_schranke"),
            "schranke_bindet": p.get("schranke_bindet"),
            "von": erste["von"],
            "bis_ausschliesslich": erste["bis_ausschliesslich"],
            "anzahl_selektionsfalten": p.get("anzahl_selektionsfalten"),
            "symbole_in_falte_1": len(erste.get("symbole_a") or []),
        })
    return {"frueheste_falte_datei": plan.get("frueheste_falte"),
            "je_bot": zeilen}


def drucke_falten(f):
    br = "=" * 78
    print(br)
    print("FRUEHESTE SELEKTIONSFALTE JE BOT  (research/faltenplan_neun/daten/"
          "faltenplan.json)")
    print(br)
    print("  %-28s %-7s %6s %8s %6s  %s"
          % ("Bot", "Markt", "1. Jahr", "o.Schr.", "Falten", "Fenster"))
    for z in f["je_bot"]:
        print("  %-28s %-7s %6s %8s %6s  %s bis %s"
              % (z["bot"], z["markt"], z["erstes_faltenjahr"],
                 z["erstes_faltenjahr_ohne_schranke"],
                 z["anzahl_selektionsfalten"], z["von"],
                 z["bis_ausschliesslich"]))
    jahre = {z["erstes_faltenjahr"] for z in f["je_bot"]}
    krypto = {z["erstes_faltenjahr"] for z in f["je_bot"]
              if z["markt"] == "krypto"}
    print()
    print("  frueheste_falte (Feld der Datei): %s" % f["frueheste_falte_datei"])
    print("  erstes Faltenjahr ueber alle neun Bots: %s" % sorted(jahre))
    print("  erstes Faltenjahr ueber die fuenf Krypto-Bots: %s"
          % sorted(krypto))
    if krypto == jahre:
        print("  ⚠️ BEFUND: Krypto und Gesamtheit liefern DIESELBE Zahl - "
              "eine Trennung")
        print("     'Krypto 2022 / alle neun 2019' gibt dieser Faltenplan "
              "nicht her.")
    print(br)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--nur", action="append", type=int, default=None,
                   help="nur diese Pruefung (Nummer, mehrfach moeglich)")
    p.add_argument("--daten", default=DATEN)
    p.add_argument("--schnell", action="store_true",
                   help="die Pruefungen ueberspringen, die den Lauf ueber "
                        "alle 223 Kursdateien brauchen (rund eine Minute)")
    p.add_argument("--falten-je-bot", action="store_true",
                   help="je Bot die frueheste Selektionsfalte ausgeben und "
                        "sonst nichts tun (TB-49, Teil 4)")
    p.add_argument("--json", default=None)
    a = p.parse_args(argv)

    if a.falten_je_bot:
        f = falten_je_bot()
        drucke_falten(f)
        if a.json:
            with open(a.json, "w", encoding="utf-8") as datei:
                json.dump(f, datei, ensure_ascii=False, indent=1)
                datei.write("\n")
        return OK_RC

    bericht = pruefe(set(a.nur) if a.nur else None, a.daten, a.schnell)
    drucke(bericht)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(bericht, f, ensure_ascii=False, indent=1)
            f.write("\n")
    if bericht["nicht_pruefbar"]:
        return NICHT_PRUEFBAR_RC
    return BEFUND_RC if bericht["befunde"] else OK_RC


if __name__ == "__main__":
    sys.exit(main())
