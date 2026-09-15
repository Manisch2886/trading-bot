#!/usr/bin/env python3
"""
TB-33 - Selbsttest des Nulltests
==============================================================================
Geprueft wird, was die beiden Registereintraege verlangen. Jeder Teil
gehoert zu einem PFADKRITERIUM aus `docs/VORREGISTRIERUNG_S-E1_pfadkriterien.md`:

  A (P1)  Das Auswertungsskript LAEUFT ohne menschliche Entscheidung durch -
          gegen erzeugte Beispieldaten, BEVOR echte Ergebnisse existieren.
  B (P6)  Die Handelstags-Regel greift bei Feiertagen UND verkuerzten Tagen.
  C (P5)  Die Sweep-Regel greift: Kern faellt, Sweep-Variante besteht ->
          das Ergebnis lautet DURCHGEFALLEN, nicht "Variante uebernommen".
  D (P4,P9) Der Staging-Bot geht in KEINE Portfolio-Zahl ein - am VERHALTEN
          geprueft. Und Frist und Kriterium standen beim Anlegen fest.
  E (P7)  Wiederholbarkeit: zweiter Lauf, gleiche Zahlen.
  F (P3)  Herkunft in JEDER Ergebnisdatei.
  G (P2)  Jede berichtete Kennzahl ist aus dem Register ableitbar.
  H       Mutationsproben.

Rueckgabewert 0 heisst: der Weg ist sauber gelaufen.

ZU DEN MUTATIONSPROBEN - WARUM SIE SO GEBAUT SIND
------------------------------------------------------------------------------
Zwei Fallen sind in diesem Projekt wiederholt aufgetreten (#73, #77, #78,
#79, #81, #86, TB-15, TB-20, TB-22, TB-26, TB-30a) und stehen in der
Aufgabenstellung ausdruecklich:

1. **Eine Probe, deren Zustand der Test von Hand herstellt, bestaetigt sich
   selbst.** Deshalb wird hier nirgends ein Ergebnis gesetzt und dann
   dasselbe Ergebnis abgefragt. Gesetzt werden **Kurse**; alles Weitere -
   welcher Tag "-1" ist, was die Kosten abziehen, wie der Bootstrap streut,
   welche Bedingung faellt - macht die Auswertung selbst. Die Proben kopieren
   den GANZEN Ordner in ein Wegwerf-Verzeichnis, aendern dort EINE Zeile und
   starten `auswertung.py` als eigenen Prozess auf DENSELBEN Beispieldaten.
   Beobachtet wird der **Ablauf**: kommt ein anderes Urteil heraus?

2. **Eine zweite Wache verdeckt das Fehlen der ersten.** Das Urteil haengt an
   DREI Bedingungen (B1, B2, B3). Ein Test, der nur "faellt durch" prueft,
   waere schon gruen, wenn zwei davon fehlten. Teil H entfernt deshalb jede
   einzeln - auf einem Datensatz, in dem NUR diese eine faellt - und weist
   nach, dass das Urteil dann kippt. Eine Bedingung, deren Wegfall nichts
   aendert, waere keine. Dasselbe fuer die beiden Datenqualitaets-Wachen
   (unvollstaendige Kerzen / entfallene Ereignisse), die verschiedene Dinge
   pruefen und sich deshalb nicht gegenseitig tragen duerfen.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import date

_HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HIER)

import auswertung as aw  # noqa: E402
import beispieldaten as bd  # noqa: E402
import handelstage as ht  # noqa: E402
import herkunft as hk  # noqa: E402
import register as reg  # noqa: E402
import staging as st  # noqa: E402

VON, BIS = 2006, 2025

bestanden = 0
gescheitert = []
# Welcher Teil gehoert zu welchem Pfadkriterium - das Pfadurteil am Ende
# wird daraus gebildet, nicht von Hand gesetzt.
KRITERIUM_JE_TEIL = {"A": ["P1"], "B": ["P6"], "C": ["P5"], "D": ["P4", "P9"],
                     "E": ["P7"], "F": ["P3"], "G": ["P2"], "H": ["P1", "P5"]}
fehler_je_teil = {}


def pruefe(name, bedingung, zusatz=""):
    global bestanden
    if bedingung:
        bestanden += 1
    else:
        gescheitert.append(f"{name}{(' - ' + zusatz) if zusatz else ''}")
        fehler_je_teil.setdefault(name.split(":")[0][0], []).append(name)


def _daten(ziel, lage_name, **kwargs):
    """Kursdateien fuer alle vier Instrumente einer Lage."""
    kf, tf = bd.lage(lage_name)
    sonder = kwargs.pop("sonder_tage", None)
    for sym in [reg.KERNINSTRUMENT] + reg.SWEEP_INSTRUMENTE:
        bd.erzeuge(ziel, sym, VON, BIS, kf, tf, sonder_tage=sonder, **kwargs)
    return ziel


def _umgebung():
    u = dict(os.environ)
    u["TB33_BASE_DIR"] = reg.BASE_DIR
    return u


def _auswerten_in(ordner, daten, json_ziel=None):
    befehl = [sys.executable, os.path.join(ordner, "auswertung.py"),
              "--daten", daten]
    if json_ziel:
        befehl += ["--json", json_ziel]
    return subprocess.run(befehl, capture_output=True, text=True,
                          env=_umgebung())


def _urteilszeile(text):
    for z in text.splitlines():
        if "URTEIL" in z:
            return z.strip()
    return ""


# ===========================================================================
# A (P1)  Das Auswertungsskript laeuft ohne menschliche Entscheidung durch
# ===========================================================================
def teil_a():
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        ziel = os.path.join(t, "ergebnis.json")
        # stdin geschlossen: haette das Skript irgendwo eine Rueckfrage,
        # bekaeme es hier EOF und stuerzte ab. Genau das soll es nicht.
        r = subprocess.run(
            [sys.executable, os.path.join(_HIER, "auswertung.py"),
             "--daten", daten, "--json", ziel],
            capture_output=True, text=True, env=_umgebung(),
            stdin=subprocess.DEVNULL)
        pruefe("A1: auswertung.py laeuft gegen erzeugte Beispieldaten durch",
               r.returncode == 0, r.stderr[-300:])
        pruefe("A2: es schreibt eine Ergebnisdatei", os.path.exists(ziel))
        pruefe("A3: das Urteil steht im Bericht",
               any(u in r.stdout for u in (reg.URTEIL_BESTANDEN,
                                           reg.URTEIL_DURCHGEFALLEN,
                                           reg.URTEIL_NICHT_AUSWERTBAR)))

    # Keine Rueckfrage im Quelltext - maschinell, nicht durch Hinsehen.
    for name in ("auswertung.py", "handelstage.py", "kennzahlen.py",
                 "staging.py", "register.py"):
        quelle = open(os.path.join(_HIER, name), encoding="utf-8").read()
        pruefe(f"A4: {name} enthaelt keine Rueckfrage an einen Menschen",
               "input(" not in quelle and "getpass" not in quelle)

    # Und keine Stelle, an der ein Ergebnis von Hand einzusetzen waere.
    quelle = open(os.path.join(_HIER, "auswertung.py"), encoding="utf-8").read()
    pruefe("A5: auswertung.py enthaelt keinen Platzhalter zum Eintragen",
           "TODO" not in quelle and "FIXME" not in quelle
           and "XXX" not in quelle)


# ===========================================================================
# B (P6)  Die Handelstags-Regel - Feiertage UND verkuerzte Tage
# ===========================================================================
def teil_b():
    with tempfile.TemporaryDirectory() as t:
        kf, tf = bd.lage("effekt_deutlich")
        info = bd.erzeuge(t, "SPY", VON, BIS, kf, tf)
        df, _ = ht.lies_kursreihe(info["pfad"])
        ereignisse, _ = ht.ereignisse(df)
        tage = set(info["tage"])
        feiertage, _ = bd.feiertagsplan(range(VON, BIS + 1))

        # --- Feiertag am Monatsende: "-1" muss davor liegen -------------
        # Gesucht wird ein Jahr, in dem der 31.12. auf einen WOCHENTAG
        # faellt und Feiertag ist. Nur dann sagt der Fall etwas aus: an
        # einem Samstag waere "-1" ohnehin frueher, und die Probe wuerde
        # sich selbst bestaetigen, ohne die Regel zu beruehren.
        geprueft = 0
        for j in range(VON, BIS):
            silvester = date(j, 12, 31)
            if silvester.weekday() >= 5 or silvester not in feiertage:
                continue
            geprueft += 1
            zeile = ereignisse[
                (ereignisse["datum_einstieg"].dt.year == j)
                & (ereignisse["datum_einstieg"].dt.month == 12)]
            pruefe(f"B1: {j} - Einstieg liegt nicht auf dem Feiertag 31.12.",
                   len(zeile) == 1
                   and zeile["datum_einstieg"].iloc[0].date() != silvester)
            pruefe(f"B2: {j} - Einstieg ist der letzte HANDELSTAG davor",
                   len(zeile) == 1
                   and zeile["datum_einstieg"].iloc[0].date()
                   == max(d for d in tage if d < silvester))
        pruefe("B3: es gab ueberhaupt einen Feiertag am Monatsende zu pruefen",
               geprueft >= 3, f"nur {geprueft} Faelle")

        # --- Verkuerzte Tage zaehlen als volle Handelstage ---------------
        halbtage = set(info["halbtage"])
        pruefe("B4: die Beispieldaten enthalten verkuerzte Tage",
               len(halbtage) > 0)
        pruefe("B5: jeder verkuerzte Tag steht in der Kursreihe",
               all(d in tage for d in halbtage))

        # Der Freitag nach Thanksgiving ist ein Halbtag und liegt NICHT am
        # Monatsende - aber der 24.12. schon fast. Entscheidend ist: wenn
        # ein Halbtag in ein Fenster faellt, muss er als voller Tag
        # mitzaehlen. Das zeigt sich daran, dass das Fenster dann NICHT
        # laenger wird.
        betroffen = 0
        for _, e in ereignisse.iterrows():
            offen = df[(df["datum"] >= e["datum_einstieg"])
                       & (df["datum"] <= e["datum_ausstieg"])]
            if any(d.date() in halbtage for d in offen["datum"]):
                betroffen += 1
                pruefe(f"B6: Fenster mit Halbtag am "
                       f"{e['datum_einstieg'].date()} haelt trotzdem genau "
                       f"{e['gehaltene_tage']} Handelstage",
                       len(offen) == e["gehaltene_tage"])
        pruefe("B7: mindestens ein Fenster enthielt einen verkuerzten Tag",
               betroffen >= 3, f"nur {betroffen}")

        # --- Streichen UND zaehlen ---------------------------------------
        info2 = bd.erzeuge(os.path.join(t, "b"), "SPY", VON, BIS, kf, tf,
                           luecken=3, fehlende_monate=[(2011, 5), (2017, 9)])
        df2, gestrichen = ht.lies_kursreihe(info2["pfad"])
        _, entfallen = ht.ereignisse(df2)
        pruefe("B8: unvollstaendige Kerzen werden gestrichen UND gezaehlt",
               gestrichen == 3, f"gezaehlt {gestrichen}")
        pruefe("B9: Ereignisse an einer Monatsluecke entfallen UND werden "
               "gezaehlt", entfallen == 2, f"gezaehlt {entfallen}")


# ===========================================================================
# C (P5)  Die Sweep-Regel
# ===========================================================================
def teil_c():
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "kern_faellt_sweep_besteht",
                       sonder_tage={d: 0.012
                                    for d in bd.zweitletzte_tage(VON, BIS)})
        e = aw.lauf(daten)
        kern, u = e["test1_test2_kern"], e["urteil"]

        pruefe("C1: der Kern faellt in dieser Lage wirklich durch",
               u["urteil"] == reg.URTEIL_DURCHGEFALLEN,
               f"{u['urteil']} / {kern['mittlere_netto_rendite_pct']}")

        # Die Sweep-Variante -2/+3 haette bestanden - das ist die
        # Voraussetzung, ohne die die Probe nichts zeigt.
        variante = [c for c in e["test3_sweep"] if c["fenster"] == "-2/+3"][0]
        wuerde_bestehen = aw.urteil(variante)
        pruefe("C2: die Sweep-Variante -2/+3 haette bestanden",
               wuerde_bestehen["urteil"] == reg.URTEIL_BESTANDEN,
               wuerde_bestehen["grund"])

        pruefe("C3: das Ergebnis lautet trotzdem DURCHGEFALLEN",
               e["urteil"]["urteil"] == reg.URTEIL_DURCHGEFALLEN)

        bericht = aw.bericht(e)
        pruefe("C4: der Bericht nennt kein uebernommenes Fenster",
               "uebernommen" not in bericht.lower()
               or "NICHT uebernommen" in bericht)

        # Strukturell, nicht nur im Ergebnis: urteil() hat genau EINEN
        # Parameter. Eine Sweep-Zelle kann dort nicht ankommen.
        import inspect
        pruefe("C5: urteil() nimmt genau ein Argument - der Sweep kann "
               "strukturell nicht hineinreichen",
               list(inspect.signature(aw.urteil).parameters) == ["kern"])


# ===========================================================================
# D (P4, P9)  Staging geht in KEINE Portfolio-Zahl ein - am Verhalten
# ===========================================================================
def _portfolio_zustand():
    """Die Listen, aus denen Portfolio-Zahlen und Crash-Knopf entstehen.

    Gelesen wird, was das Projekt WIRKLICH benutzt - nicht eine Kopie
    davon. Eine nachgebaute Liste wuerde die Frage nicht beantworten.
    """
    zustand = {}
    sys.path.insert(0, os.path.join(reg.BASE_DIR, "shared"))
    sys.path.insert(0, os.path.join(reg.BASE_DIR, "notifications"))
    import ergebniskurven  # noqa: PLC0415
    import manual_close  # noqa: PLC0415
    zustand["bots"] = sorted(ergebniskurven.finde_bots())
    zustand["crash_knopf"] = sorted(manual_close.SCHLIESSBARE_BOTS)
    zustand["datenbanken"] = sorted(
        f for f in os.listdir(reg.BASE_DIR) if f.startswith("paper_trading_"))
    ergebnisordner = os.path.join(reg.BASE_DIR, "results")
    zustand["results"] = sorted(os.listdir(ergebnisordner)) if os.path.isdir(
        ergebnisordner) else []
    zustand["strategien"] = sorted(os.listdir(
        os.path.join(reg.BASE_DIR, "strategies")))
    return zustand


def teil_d():
    vorher = _portfolio_zustand()
    pruefe("D1: vor dem Lauf sind es neun Bots",
           len(vorher["bots"]) == 9, str(vorher["bots"]))
    pruefe("D2: vor dem Lauf hat der Crash-Knopf neun Bots",
           len(vorher["crash_knopf"]) == 9, str(vorher["crash_knopf"]))

    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        protokoll = os.path.join(t, "signale.jsonl")
        echtes_protokoll = st.SIGNALE
        st.SIGNALE = protokoll
        st.STAGING_DIR = t
        try:
            # WIRKLICH laufen lassen - an mehreren Stichtagen, darunter
            # Fenstertage und Tage ausserhalb. Eine Probe, die den Lauf
            # ueberspringt, bestaetigt nur, dass nichts passiert ist.
            laeufe = 0
            for stand in ("2019-12-30", "2020-01-02", "2020-01-03",
                          "2020-01-06", "2020-01-20"):
                st.protokolliere(daten, stand)
                laeufe += 1
            pruefe("D3: der Staging-Lauf hat wirklich protokolliert",
                   os.path.exists(protokoll)
                   and len(open(protokoll, encoding="utf-8").readlines()) == laeufe)

            zeilen = [json.loads(z) for z in
                      open(protokoll, encoding="utf-8").read().splitlines()]
            pruefe("D4: mindestens ein Signal stand auf LONG",
                   any(z["position"] == "long" for z in zeilen))
            pruefe("D5: jedes Signal traegt Portfoliogewicht 0",
                   all(z["portfoliogewicht"] == 0.0 for z in zeilen))
            pruefe("D6: kein Signal behauptet, im Crash-Knopf zu stehen",
                   all(z["im_crash_knopf"] is False for z in zeilen))

            nachher = _portfolio_zustand()
            for schluessel in ("bots", "crash_knopf", "datenbanken",
                               "results", "strategien"):
                pruefe(f"D7: '{schluessel}' ist nach dem Staging-Lauf "
                       f"unveraendert",
                       vorher[schluessel] == nachher[schluessel],
                       f"{set(nachher[schluessel]) ^ set(vorher[schluessel])}")
            pruefe("D8: S-E1 taucht in keiner der Listen auf",
                   not any("turn_of_month" in x or "S-E1" in x or "s_e1" in x
                           for liste in nachher.values() for x in liste))
        finally:
            st.SIGNALE = echtes_protokoll

    # --- P9: Frist und Kriterium standen BEIM ANLEGEN fest ---------------
    pruefe("D9: die Frist steht im Register, nicht im Lauf",
           isinstance(reg.STAGING_FRIST_EREIGNISSE, int)
           and reg.STAGING_FRIST_EREIGNISSE > 0
           and len(reg.STAGING_FRIST_DATUM) == 10)
    pruefe("D10: das Entscheidungskriterium nennt alle drei Bedingungen",
           set(reg.STAGING_KRITERIEN) == {"S1", "S2", "S3"})
    pruefe("D11: Frist und Kriterium gehen in den Register-Hash ein",
           "register.py" in hk.EINGEFROREN)
    # Und das Staging-Modul stellt sich seine Freigabe NICHT selbst aus.
    z = st.status()
    pruefe("D12: staging.status() behauptet S1 und S2 nicht selbst",
           z["s1_rang3_entschieden"] is None
           and z["s2_backtest_bestanden"] is None)
    pruefe("D13: staging.status() weist Portfoliogewicht 0 aus",
           z["portfoliogewicht"] == 0.0)


# ===========================================================================
# E (P7)  Wiederholbarkeit
# ===========================================================================
def teil_e():
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        a, b = os.path.join(t, "a.json"), os.path.join(t, "b.json")
        r1 = _auswerten_in(_HIER, daten, a)
        r2 = _auswerten_in(_HIER, daten, b)
        pruefe("E1: beide Laeufe gehen durch",
               r1.returncode == 0 and r2.returncode == 0)

        def ohne_zeit(pfad):
            d = json.load(open(pfad, encoding="utf-8"))
            # Der Zeitstempel MUSS sich unterscheiden - alles andere nicht.
            for teil in (d["herkunft"],):
                teil.pop("zeitpunkt_utc", None)
            return d

        eins, zwei = ohne_zeit(a), ohne_zeit(b)
        pruefe("E2: zweiter Lauf, bitweise gleiche Zahlen",
               json.dumps(eins, sort_keys=True) == json.dumps(zwei, sort_keys=True))
        # Aussen vor bleiben genau zwei Zeilen, und beide aus gutem Grund:
        # der Zeitstempel (er MUSS sich unterscheiden) und der Name der
        # geschriebenen JSON-Datei (sie heisst in beiden Laeufen anders,
        # weil der Test sie anders nennt).
        def bericht_ohne_lauf(text):
            return [z for z in text.splitlines()
                    if "Herkunft" not in z
                    and not z.startswith("JSON geschrieben")]

        pruefe("E3: auch der Bericht ist Zeile fuer Zeile gleich",
               bericht_ohne_lauf(r1.stdout) == bericht_ohne_lauf(r2.stdout),
               "\n".join(a for a, b in zip(bericht_ohne_lauf(r1.stdout),
                                            bericht_ohne_lauf(r2.stdout))
                         if a != b)[:200])
        pruefe("E4: der feste Startwert steht im Register, nicht im Skript",
               "BOOTSTRAP_SEED" in open(
                   os.path.join(_HIER, "register.py"), encoding="utf-8").read())


# ===========================================================================
# F (P3)  Herkunft in JEDER Ergebnisdatei
# ===========================================================================
def teil_f():
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        ziel = os.path.join(t, "ergebnis.json")
        _auswerten_in(_HIER, daten, ziel)
        d = json.load(open(ziel, encoding="utf-8"))
        fehlt = hk.vollstaendig(d.get("herkunft"))
        pruefe("F1: die Ergebnisdatei traegt einen vollstaendigen "
               "Herkunftsblock", not fehlt, str(fehlt))
        pruefe("F2: alle drei Hashes sind da",
               all(d["herkunft"].get(k) for k in
                   ("commit", "datenstand", "register")))
        pruefe("F3: der Datenstand-Hash haengt an DIESEN Daten",
               d["herkunft"]["datendateien"] == 4)

        # Auch das Staging-Signal traegt Herkunft - es ist eine
        # Ergebnisdatei wie jede andere.
        s = st.signal(daten, "2020-01-02")
        pruefe("F4: auch das Staging-Signal traegt Herkunft",
               not hk.vollstaendig(s.get("herkunft")))

        # Ein anderer Datenstand muss einen anderen Hash geben - sonst
        # beantwortet der Hash die Frage nicht, fuer die er da ist.
        daten2 = _daten(os.path.join(t, "daten2"), "kein_effekt")
        ziel2 = os.path.join(t, "e2.json")
        _auswerten_in(_HIER, daten2, ziel2)
        d2 = json.load(open(ziel2, encoding="utf-8"))
        pruefe("F5: andere Daten, anderer Datenstand-Hash",
               d["herkunft"]["datenstand"] != d2["herkunft"]["datenstand"])
        pruefe("F6: gleicher Code, gleicher Register-Hash",
               d["herkunft"]["register"] == d2["herkunft"]["register"])

        # Das append-only-Protokoll haelt seine Kette.
        pruefe("F7: das Herkunftsprotokoll hat keine Kettenfehler",
               hk.kette_pruefen() == [], str(hk.kette_pruefen()))


# ===========================================================================
# G (P2)  Jede berichtete Kennzahl ist aus dem Register ableitbar
# ===========================================================================
def teil_g():
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        ziel = os.path.join(t, "ergebnis.json")
        _auswerten_in(_HIER, daten, ziel)
        d = json.load(open(ziel, encoding="utf-8"))

        kern = d["test1_test2_kern"]
        ohne_herkunft = [k for k in kern
                         if k not in reg.HERKUNFT_JE_KENNZAHL
                         and k not in ("je_falte_pct", "n_handelstage",
                                       "n_vergleichsfenster", "gehaltene_tage")]
        pruefe("G1: jede Kennzahl des Kerns hat einen Registereintrag",
               not ohne_herkunft, str(ohne_herkunft))

        for b in ("b1", "b2", "b3"):
            pruefe(f"G2: {b.upper()} steht im Bericht und im Register",
                   b in d["urteil"] and b.upper() in reg.BEDINGUNGEN)

        # Die Schwellen im Bericht sind DIESELBEN Objekte wie im Register -
        # nicht zufaellig gleiche Zahlen.
        r = d["register"]
        pruefe("G3: die Kostenkonvention im Bericht stammt aus dem Register",
               r["kosten_je_roundtrip_pct"] == reg.KOSTEN_JE_ROUNDTRIP_PCT)
        pruefe("G4: die Kostenschranke ist gerechnet, nicht abgeschrieben",
               abs(r["kostenschranke_pct_pa"]
                   - reg.KOSTEN_JE_ROUNDTRIP_PCT * reg.RUNDEN_JE_JAHR) < 1e-12)
        pruefe("G5: Seed und Ziehungen im Bericht stammen aus dem Register",
               r["bootstrap_seed"] == reg.BOOTSTRAP_SEED
               and r["platzhalter_ziehungen"] == reg.PLATZHALTER_ZIEHUNGEN)
        pruefe("G6: die Perzentil-Schwelle steht nur an einer Stelle",
               r["perzentil_schwelle"] == reg.PERZENTIL_SCHWELLE)
        pruefe("G7: die Sweep-Regel steht woertlich im Bericht",
               r["sweep_regel"] == reg.SWEEP_REGEL)
        pruefe("G8: die Faltenzuordnung (A4) steht im Bericht",
               r["ereignis_zuordnung"] == reg.EREIGNIS_ZUORDNUNG)
        pruefe("G9: die N-Buchfuehrung steht im Bericht",
               r["n_versuchsregister"] == 1 and r["n_dsr"] == 0)

        # Keine Schwelle taucht als Zahlenliteral im Auswertungsskript auf -
        # sonst stuende sie zweimal, und in diesem Projekt sind doppelt
        # gefuehrte Zahlen schon auseinandergelaufen.
        quelle = open(os.path.join(_HIER, "auswertung.py"),
                      encoding="utf-8").read()
        rechenteil = quelle[quelle.index("def eine_zelle"):]
        for zahl in (str(reg.PERZENTIL_SCHWELLE), str(reg.MINDEST_EREIGNISSE),
                     str(reg.BOOTSTRAP_SEED),
                     str(reg.KOSTEN_JE_ROUNDTRIP_PCT)):
            pruefe(f"G10: die Zahl {zahl} steht nicht als Literal im "
                   f"Rechenteil von auswertung.py",
                   zahl not in rechenteil)


# ===========================================================================
# H  Mutationsproben - am Ablauf, nicht an einer gesetzten Variablen
# ===========================================================================
def _kopie(ziel):
    shutil.copytree(_HIER, ziel, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "daten",
                                                  "ergebnisse", "staging"))
    return ziel


def _ersetze(pfad, alt, neu):
    with open(pfad, encoding="utf-8") as f:
        s = f.read()
    if alt not in s:
        raise AssertionError(f"Mutationsstelle nicht gefunden in {pfad}: {alt!r}")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(s.replace(alt, neu, 1))


def _probe(name, lage_name, datei, alt, neu, erwartet_kippt=True,
           sonder=None, **kwargs):
    """Eine Probe: EINE Zeile aendern, DENSELBEN Datensatz, eigener Prozess."""
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), lage_name,
                       sonder_tage=sonder, **kwargs)
        original = _auswerten_in(_HIER, daten)
        if original.returncode != 0:
            pruefe(name, False, f"Originallauf scheitert: {original.stderr[-200:]}")
            return
        m = _kopie(os.path.join(t, "mutiert"))
        _ersetze(os.path.join(m, datei), alt, neu)
        mutiert = _auswerten_in(m, daten)
        if mutiert.returncode != 0:
            pruefe(name, False, f"mutierter Lauf scheitert: {mutiert.stderr[-200:]}")
            return
        gekippt = _urteilszeile(original.stdout) != _urteilszeile(mutiert.stdout)
        pruefe(name, gekippt == erwartet_kippt,
               f"original {_urteilszeile(original.stdout)!r} / "
               f"mutiert {_urteilszeile(mutiert.stdout)!r}")


def teil_h():
    # --- H0: der unveraenderte Ordner wertet aus ------------------------
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        r = _auswerten_in(_HIER, daten)
        pruefe("H0: der unveraenderte Ordner wertet aus", r.returncode == 0,
               r.stderr[-300:])

    # --- H1 bis H3: JEDE der drei Bedingungen einzeln -------------------
    # Auf einem Datensatz, in dem NUR diese eine faellt. Wuerde eine
    # zweite Bedingung dasselbe tragen, bliebe das Urteil stehen - und die
    # Probe waere rot. Genau darum geht es.
    _probe("H1: ohne B1 kippt das Urteil in der Lage 'nur B1 faellt'",
           "nur_b1_faellt", "auswertung.py",
           'b1 = kern["falten_median_pct"] is not None and kern["falten_median_pct"] > 0',
           'b1 = True')
    _probe("H2: ohne B2 kippt das Urteil in der Lage 'nur B2 faellt'",
           "nur_b2_faellt", "auswertung.py",
           'b2 = kern["bootstrap_unten_pct"] is not None and kern["bootstrap_unten_pct"] > 0',
           'b2 = True')
    _probe("H3: ohne B3 kippt das Urteil in der Lage 'nur B3 faellt'",
           "nur_b3_faellt", "auswertung.py",
           'b3 = kern["perzentil"] is not None and kern["perzentil"] > reg.PERZENTIL_SCHWELLE',
           'b3 = True')

    # --- Gegenprobe: jede Bedingung traegt NUR ihren eigenen Fall -------
    # Ohne B1 darf sich in der Lage "nur B3 faellt" NICHTS aendern. Sonst
    # waere B1 dort heimlich mit im Spiel, und H3 haette den falschen Grund.
    _probe("H1b: ohne B1 aendert sich in der Lage 'nur B3 faellt' nichts",
           "nur_b3_faellt", "auswertung.py",
           'b1 = kern["falten_median_pct"] is not None and kern["falten_median_pct"] > 0',
           'b1 = True', erwartet_kippt=False)
    _probe("H3b: ohne B3 aendert sich in der Lage 'nur B1 faellt' nichts",
           "nur_b1_faellt", "auswertung.py",
           'b3 = kern["perzentil"] is not None and kern["perzentil"] > reg.PERZENTIL_SCHWELLE',
           'b3 = True', erwartet_kippt=False)

    # --- H4: die Sweep-Regel traegt -------------------------------------
    _probe("H4: laesst man eine Sweep-Zelle ins Urteil, kippt es",
           "kern_faellt_sweep_besteht", "auswertung.py",
           '    u = urteil(kern)                      # <- nur der Kern. Siehe Docstring.',
           '    u = urteil(kern)\n'
           '    if u["urteil"] != reg.URTEIL_BESTANDEN:\n'
           '        for _c in sweep(daten_dir, reg.SELEKTIONSFALTEN_BIS):\n'
           '            if "fehlt" in _c:\n'
           '                continue\n'
           '            _u = urteil(_c)\n'
           '            if _u["urteil"] == reg.URTEIL_BESTANDEN:\n'
           '                u = _u\n'
           '                break',
           sonder={d: 0.012 for d in bd.zweitletzte_tage(VON, BIS)})

    # --- H5: die Kosten werden wirklich abgezogen -----------------------
    _probe("H5: ohne Kosten kippt das Urteil in der Lage 'kein Effekt'",
           "kein_effekt", "register.py",
           "KOSTEN_JE_ROUNDTRIP_PCT = 0.30", "KOSTEN_JE_ROUNDTRIP_PCT = 0.0")

    # --- H6/H7: die beiden Datenqualitaets-Wachen decken sich NICHT -----
    # Sie pruefen Verschiedenes: die eine streicht unvollstaendige Kerzen,
    # die andere zaehlt Ereignisse an Monatsluecken. Faellt eine weg, muss
    # sich GENAU ihre Zahl aendern - und die der anderen nicht.
    with tempfile.TemporaryDirectory() as t:
        kf, tf = bd.lage("effekt_deutlich")
        for sym in [reg.KERNINSTRUMENT] + reg.SWEEP_INSTRUMENTE:
            bd.erzeuge(os.path.join(t, "daten"), sym, VON, BIS, kf, tf,
                       luecken=3, fehlende_monate=[(2011, 5), (2017, 9)])
        daten = os.path.join(t, "daten")
        ziel = os.path.join(t, "o.json")
        _auswerten_in(_HIER, daten, ziel)
        o = json.load(open(ziel, encoding="utf-8"))["test1_test2_kern"]
        pruefe("H6a: der Originallauf sieht beide Befunde",
               o["n_kerzen_gestrichen"] == 3 and o["n_ereignisse_entfallen"] == 2,
               f"{o['n_kerzen_gestrichen']}/{o['n_ereignisse_entfallen']}")

        # Wache 1 weg: unvollstaendige Kerzen bleiben drin.
        m1 = _kopie(os.path.join(t, "m1"))
        _ersetze(os.path.join(m1, "handelstage.py"),
                 "    df, gestrichen = kursdaten.entferne_unvollstaendige(\n"
                 "        df, symbol=os.path.basename(pfad), melden=melden)",
                 "    gestrichen = 0")
        z1 = os.path.join(t, "m1.json")
        _auswerten_in(m1, daten, z1)
        a1 = json.load(open(z1, encoding="utf-8"))["test1_test2_kern"]
        pruefe("H6: ohne die Kerzen-Wache aendert sich GENAU ihre Zahl",
               a1["n_kerzen_gestrichen"] != o["n_kerzen_gestrichen"])
        pruefe("H6b: die zweite Wache traegt sie nicht mit - die Zahl der "
               "entfallenen Ereignisse bleibt",
               a1["n_ereignisse_entfallen"] == o["n_ereignisse_entfallen"],
               f"{a1['n_ereignisse_entfallen']} statt "
               f"{o['n_ereignisse_entfallen']}")

        # Wache 2 weg: entfallene Ereignisse werden nicht mehr gezaehlt.
        #
        # Wichtig ist, WELCHE der Streich-Wachen hier mutiert wird. Es gibt
        # zwei: die Monatsfolge-Pruefung (greift, wenn ein ganzer Monat
        # fehlt) und die Lueckenlosigkeits-Pruefung (greift, wenn die Reihe
        # mitten im Monat abreisst). Ein erster Versuch mutierte die
        # zweite - und die Probe blieb gruen, weil in dieser Lage die
        # ERSTE anschlaegt. Das ist genau die Falle, um die es hier geht:
        # eine zweite Wache verdeckt das Fehlen der ersten. Deshalb wird
        # jetzt die mutiert, die in dieser Lage wirklich traegt.
        m2 = _kopie(os.path.join(t, "m2"))
        _ersetze(os.path.join(m2, "handelstage.py"),
                 "                                 else (jahr_m, monat_m + 1)):\n"
                 "            entfallen += 1\n"
                 "            continue",
                 "                                 else (jahr_m, monat_m + 1)):\n"
                 "            continue")
        z2 = os.path.join(t, "m2.json")
        _auswerten_in(m2, daten, z2)
        a2 = json.load(open(z2, encoding="utf-8"))["test1_test2_kern"]
        pruefe("H7: ohne die Luecken-Wache aendert sich GENAU ihre Zahl",
               a2["n_ereignisse_entfallen"] != o["n_ereignisse_entfallen"])
        pruefe("H7b: die erste Wache traegt sie nicht mit - die Zahl der "
               "gestrichenen Kerzen bleibt",
               a2["n_kerzen_gestrichen"] == o["n_kerzen_gestrichen"])

        # H7c: und die dritte Wache (Lueckenlosigkeit mitten im Monat)
        # traegt in dieser Lage NICHTS. Das ist kein Mangel, sondern der
        # Nachweis, dass jede Wache ihren eigenen Fall hat: waere sie hier
        # mit im Spiel, haette H7 den falschen Grund.
        m3 = _kopie(os.path.join(t, "m3"))
        _ersetze(os.path.join(m3, "handelstage.py"),
                 "        if idx_n[0] != idx_m[-1] + 1:\n"
                 "            entfallen += 1\n"
                 "            continue",
                 "        if idx_n[0] != idx_m[-1] + 1:\n"
                 "            continue")
        z3 = os.path.join(t, "m3.json")
        _auswerten_in(m3, daten, z3)
        a3 = json.load(open(z3, encoding="utf-8"))["test1_test2_kern"]
        pruefe("H7c: die Lueckenlosigkeits-Wache greift in dieser Lage "
               "nicht - jede Wache hat ihren eigenen Fall",
               a3["n_ereignisse_entfallen"] == o["n_ereignisse_entfallen"])

    # --- H8: die Handelstags-Regel traegt -------------------------------
    # Wer "-1" auf den letzten KALENDERTAG legt, bekommt andere Ereignisse.
    with tempfile.TemporaryDirectory() as t:
        daten = _daten(os.path.join(t, "daten"), "effekt_deutlich")
        ziel = os.path.join(t, "o.json")
        _auswerten_in(_HIER, daten, ziel)
        o = json.load(open(ziel, encoding="utf-8"))["test1_test2_kern"]
        m = _kopie(os.path.join(t, "m"))
        # Ein Monat gilt nur noch dann als vollstaendig, wenn sein letzter
        # Handelstag zugleich der letzte Kalendertag ist - der Fehler, den
        # die Regel verhindert.
        _ersetze(os.path.join(m, "handelstage.py"),
                 "        erster = idx_m[-anzahl_vor]",
                 "        import calendar as _cal\n"
                 "        if df['datum'].iloc[idx_m[-1]].day != _cal.monthrange(\n"
                 "                jahr_m, monat_m)[1]:\n"
                 "            entfallen += 1\n"
                 "            continue\n"
                 "        erster = idx_m[-anzahl_vor]")
        z = os.path.join(t, "m.json")
        _auswerten_in(m, daten, z)
        a = json.load(open(z, encoding="utf-8"))["test1_test2_kern"]
        pruefe("H8: auf Kalendertage statt Handelstage umgestellt, "
               "aendert sich die Zahl der Ereignisse",
               a["n_ereignisse"] != o["n_ereignisse"],
               f"{a['n_ereignisse']} gegen {o['n_ereignisse']}")


# ===========================================================================
def main():
    print(__doc__.strip().split("\n")[0])
    for name, fn in (("A", teil_a), ("B", teil_b), ("C", teil_c),
                     ("D", teil_d), ("E", teil_e), ("F", teil_f),
                     ("G", teil_g), ("H", teil_h)):
        print(f"  Teil {name} ...")
        fn()

    print("\n" + "=" * 78)
    if gescheitert:
        print(f"{bestanden}/{bestanden + len(gescheitert)} Pruefungen "
              f"bestanden. GESCHEITERT:")
        for g in gescheitert:
            print(f"  - {g}")
    else:
        print(f"{bestanden}/{bestanden} Pruefungen bestanden.")

    # --- Das Pfadurteil - gebildet, nicht gesetzt ------------------------
    gefallen = set()
    for teil, kriterien in KRITERIUM_JE_TEIL.items():
        if teil in fehler_je_teil:
            gefallen |= set(kriterien)
    print("=" * 78)
    if gefallen:
        print(f"WEG NICHT SAUBER - gefallene Pfadkriterien: "
              f"{', '.join(sorted(gefallen))}")
        print("An diesen Stellen wurde eine Entscheidung noetig, die nicht "
              "im Register stand.")
    else:
        print("WEG SAUBER - alle neun Pfadkriterien P1 bis P9 bestanden.")
        print("Keine Stelle, an der eine Entscheidung ausserhalb des "
              "Registers noetig war.")
    return 1 if gescheitert else 0


if __name__ == "__main__":
    sys.exit(main())
