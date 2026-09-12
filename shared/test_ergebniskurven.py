"""
Selbsttests der Ergebniskurven-Pruefung
==============================================================================
Geprueft wird das VERHALTEN, nicht das Vorhandensein von Codestuecken.

DIE EIGENTLICHE ZUSICHERUNG (Abschnitt 3)
------------------------------------------------------------------------------
Die Pruefung muss anschlagen, wenn eine abgelegte Kurve nicht mehr zur
heutigen Konfiguration passt - und zwar **auch dann, wenn die Zeilenzahl
gleich bleibt**. Genau das war der HRP-Fall: gleiche Zahl von Trades, aber
ein nicht angewendeter Regimefilter.

Zwei wiederkehrende Fallen aus #73, #77, #78, #79 und #81 sind dabei bewusst
umgangen:

**Falle 1 - die selbstbestaetigende Probe.** Ein Test, der die veraltete
Kurve von Hand hinschreibt und dann feststellt, dass sie sich von der
frischen unterscheidet, hat nur bewiesen, dass zwei verschiedene CSV-Dateien
verschieden sind. Hier wird deshalb nie eine Kurve von Hand erzeugt: der
Test aendert ausschliesslich die **Konfiguration des Bots** und laesst die
Kurve von dessen eigenem `equity_simulation.py` erzeugen - in einem
vollstaendigen, lauffaehigen Klon des Repos (`probe_umgebung()`).
Beobachtet wird der ABLAUF: derselbe Bot, dieselben Dateien, dieselbe
Pruefung - vorher gruen, nach der Konfigurationsaenderung rot.

**Falle 2 - die zweite Wache verdeckt das Fehlen der ersten.** Wuerde der
Prueffall die Zeilenzahl mitveraendern, koennte ein blosser
Zeilenzahl-Vergleich ihn ebenfalls fangen; die Zusicherung "vergleicht mehr
als die Zeilenzahl" waere dann gar nicht geprueft. Der Kernfall
(Abschnitt 3) ist deshalb so gewaehlt, dass die Zeilenzahl **nachweislich
gleich bleibt**: das Startkapital wird verdoppelt. In `simulate_portfolio()`
skalieren Positionsgroesse und freies Kapital beide linear mit dem Kapital,
die Menge der ausgefuehrten Trades bleibt also dieselbe - jede einzelne
Zeile von `allocation` und `capital_after` aendert sich trotzdem. Der Test
prueft die Gleichheit der Zeilenzahl ausdruecklich mit, statt sie
vorauszusetzen.

Abschnitt 4 stellt zusaetzlich den HRP-Fall selbst nach: der
BTC-Regimefilter von `volatility_breakout_crypto` wird aus dem
`__main__`-Block entfernt - dieselbe Luecke, die PR #57 geschlossen hat.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Nutzung:  python3 shared/test_ergebniskurven.py
"""

import os
import shutil
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)
sys.path.insert(0, _SHARED)

import pandas as pd                                            # noqa: E402

import ergebniskurven as ek                                    # noqa: E402

# Der schnellste der neun Bots (rund zwei Sekunden je Lauf) - und zugleich
# derjenige, an dem der HRP-Bericht gekippt ist.
BOT = "volatility_breakout_crypto"

BESTANDEN = 0
FEHLER = []


def check(name, bedingung, detail=""):
    global BESTANDEN
    if bedingung:
        BESTANDEN += 1
        print(f"  [OK ] {name}" + (f"   {detail}" if detail else ""))
    else:
        FEHLER.append(name)
        print(f"  [FEHLER] {name}" + (f"   {detail}" if detail else ""))


# ---------------------------------------------------------------------------
# Probe-Umgebung
# ---------------------------------------------------------------------------

def probe_umgebung(bot=BOT):
    """Ein vollstaendiger, lauffaehiger Klon des Repos in einem eigenen
    Ordner.

    `shared/`, `data/` und `config/` werden verknuepft (nur gelesen),
    `strategies/<bot>/` wird KOPIERT - nur dort wird mutiert. `results/`
    ist leer und gehoert allein diesem Klon.

    Dass das traegt, haengt an einer Eigenschaft der Projektkonvention:
    sowohl `strategy_paths.get_strategy_paths()` als auch die beiden
    Werkzeuge leiten BASE_DIR ueber `os.path.abspath(__file__)` her, und
    `abspath` loest Verknuepfungen NICHT auf. Der Klon sieht sich deshalb
    selbst als Projektwurzel."""
    ordner = tempfile.mkdtemp(prefix="ergebniskurven_probe_")
    for name in ("shared", "data", "config"):
        os.symlink(os.path.join(BASE_DIR, name), os.path.join(ordner, name))
    os.makedirs(os.path.join(ordner, "strategies"))
    shutil.copytree(os.path.join(BASE_DIR, "strategies", bot),
                    os.path.join(ordner, "strategies", bot))
    os.makedirs(os.path.join(ordner, "results", bot))
    return ordner


def werkzeug(ordner, *argumente):
    """Ruft das Werkzeug im Klon auf - als eigenstaendiges Programm, damit
    auch der Rueckgabewert geprueft ist."""
    return subprocess.run(
        [sys.executable, os.path.join(ordner, "shared", "ergebniskurven.py"),
         "--bot", BOT, *argumente],
        capture_output=True, text=True, cwd=ordner, timeout=600)


def ablage(ordner, bot=BOT):
    return os.path.join(ordner, "results", bot, "equity_curve.csv")


def mutiere(ordner, alt, neu, bot=BOT):
    """Aendert die Konfiguration des Bots IM KLON. Gibt zurueck, wie oft
    ersetzt wurde - 0 waere ein stiller Fehlschlag der Probe."""
    pfad = os.path.join(ordner, "strategies", bot, "equity_simulation.py")
    with open(pfad) as f:
        text = f.read()
    anzahl = text.count(alt)
    with open(pfad, "w") as f:
        f.write(text.replace(alt, neu))
    return anzahl


# ---------------------------------------------------------------------------
def test_erzeugung_wiederholbar():
    print("\n1) Die Erzeugung ist wiederholbar")
    ordner = probe_umgebung()
    try:
        eins = tempfile.mkdtemp(prefix="kurve_a_")
        zwei = tempfile.mkdtemp(prefix="kurve_b_")
        for ziel in (eins, zwei):
            lauf = subprocess.run(
                [sys.executable, os.path.join(ordner, "shared", "kurven_lauf.py"), BOT, ziel],
                capture_output=True, text=True, cwd=ordner, timeout=600)
            check(f"Lauf nach {os.path.basename(ziel)} erfolgreich",
                  lauf.returncode == 0, lauf.stderr[-200:])
        a = os.path.join(eins, "equity_curve.csv")
        b = os.path.join(zwei, "equity_curve.csv")
        with open(a, "rb") as fa, open(b, "rb") as fb:
            gleich = fa.read() == fb.read()
        check("zwei Laeufe ergeben byteweise dieselbe Datei", gleich)
        check("die Datei ist nicht leer", os.path.getsize(a) > 100,
              f"{os.path.getsize(a)} Bytes")
        shutil.rmtree(eins, ignore_errors=True)
        shutil.rmtree(zwei, ignore_errors=True)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ---------------------------------------------------------------------------
def test_gegenprobe_aktuelle_kurve():
    print("\n2) Gegenprobe: bei aktueller Kurve schlaegt die Pruefung NICHT an")
    ordner = probe_umgebung()
    try:
        erzeugt = werkzeug(ordner, "--erzeugen")
        check("Erzeugen laeuft durch", os.path.exists(ablage(ordner)),
              erzeugt.stderr[-200:])

        geprueft = werkzeug(ordner)
        check("Rueckgabewert 0", geprueft.returncode == 0, geprueft.returncode)
        check("meldet AKTUELL", "AKTUELL" in geprueft.stdout
              and "ABWEICHEND" not in geprueft.stdout)
        check("sagt es ausdruecklich",
              "passen zur heutigen Konfiguration" in geprueft.stdout)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ---------------------------------------------------------------------------
def test_kern_gleiche_zeilenzahl():
    print("\n3) KERN: Befund trotz unveraenderter Zeilenzahl")
    ordner = probe_umgebung()
    try:
        # Schritt 1: Kurve ablegen, wie der Bot sie heute erzeugt.
        werkzeug(ordner, "--erzeugen")
        vorher = werkzeug(ordner)
        check("vor der Aenderung gruen", vorher.returncode == 0, vorher.returncode)
        zeilen_vorher = len(pd.read_csv(ablage(ordner)))

        # Schritt 2: NUR die Konfiguration des Bots aendern. Die abgelegte
        # Kurve wird nicht angefasst - sie ist ab jetzt die Kurve eines Bots,
        # den es so nicht mehr gibt.
        ersetzt = mutiere(ordner, "STARTING_CAPITAL = 10_000.0",
                          "STARTING_CAPITAL = 20_000.0")
        check("die Konfigurationsaenderung ist angekommen", ersetzt == 1, ersetzt)

        # Schritt 3: dieselbe Pruefung erneut.
        nachher = werkzeug(ordner)
        check("nach der Aenderung Rueckgabewert 1", nachher.returncode == 1,
              nachher.returncode)
        check("meldet ABWEICHEND", "ABWEICHEND" in nachher.stdout)

        # Die eigentliche Zusicherung: die Zeilenzahl hat sich NICHT
        # geaendert. Ein Zeilenzahl-Vergleich haette hier nichts gefunden -
        # nur der Inhaltsvergleich kann angeschlagen haben.
        frisch = tempfile.mkdtemp(prefix="kurve_mutiert_")
        subprocess.run(
            [sys.executable, os.path.join(ordner, "shared", "kurven_lauf.py"), BOT, frisch],
            capture_output=True, text=True, cwd=ordner, timeout=600)
        zeilen_nachher = len(pd.read_csv(os.path.join(frisch, "equity_curve.csv")))
        check("die Zeilenzahl ist unveraendert geblieben",
              zeilen_vorher == zeilen_nachher,
              f"{zeilen_vorher} vorher, {zeilen_nachher} nachher")

        # Und die Gegenrichtung derselben Aussage: eine Pruefung, die NUR
        # die Zeilenzahl vergleicht, waere hier gruen geblieben.
        alt = pd.read_csv(ablage(ordner))
        neu = pd.read_csv(os.path.join(frisch, "equity_curve.csv"))
        check("eine reine Zeilenzahl-Wache waere hier blind geblieben",
              len(alt) == len(neu))
        check("der Inhaltsvergleich sieht den Unterschied",
              ek.vergleiche(alt, neu)["zustand"] == ek.ABWEICHEND)
        check("und benennt die betroffenen Spalten",
              set(ek.vergleiche(alt, neu)["erste_abweichung"]["spalten"])
              == {"allocation", "capital_after"},
              str(ek.vergleiche(alt, neu)["erste_abweichung"]["spalten"]))
        shutil.rmtree(frisch, ignore_errors=True)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ---------------------------------------------------------------------------
def test_hrp_fall_regimefilter():
    print("\n4) Der HRP-Fall selbst: nicht angewendeter Regimefilter")
    ordner = probe_umgebung()
    try:
        werkzeug(ordner, "--erzeugen")
        check("Ausgangslage gruen", werkzeug(ordner).returncode == 0)

        # Dieselbe Luecke, die PR #57 geschlossen hat: der Filter steht an
        # der Aufrufstelle im __main__-Block und faellt weg, ohne dass sich
        # ein einziger Wert in live_params.py aendert.
        ersetzt = mutiere(ordner,
                          "    trades = apply_btc_regime_filter(trades, all_data)\n",
                          "")
        check("der Filteraufruf ist entfernt", ersetzt == 1, ersetzt)

        nachher = werkzeug(ordner)
        check("Rueckgabewert 1", nachher.returncode == 1, nachher.returncode)
        check("meldet ABWEICHEND", "ABWEICHEND" in nachher.stdout)
        check("live_params.py ist dabei unveraendert geblieben",
              _gleiche_datei(
                  os.path.join(ordner, "strategies", BOT, "live_params.py"),
                  os.path.join(BASE_DIR, "strategies", BOT, "live_params.py")))
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


def _gleiche_datei(a, b):
    with open(a, "rb") as fa, open(b, "rb") as fb:
        return fa.read() == fb.read()


# ---------------------------------------------------------------------------
def test_veraltet_gegen_abweichend():
    print("\n5) Nur laenger geworden ist etwas anderes als auseinandergelaufen")
    ordner = probe_umgebung()
    try:
        werkzeug(ordner, "--erzeugen")
        voll = pd.read_csv(ablage(ordner))

        # Eine Kurve, die frueher einmal genau so erzeugt worden waere: die
        # Kurve ist zeitlich fortlaufend, ein frueherer Lauf mit weniger
        # Kursdaten haette genau diesen Anfang geschrieben. Das ist keine
        # von Hand erfundene Abweichung, sondern eine echte frueherere
        # Fassung derselben Datei.
        voll.head(len(voll) - 20).to_csv(ablage(ordner), index=False)

        lauf = werkzeug(ordner)
        check("meldet VERALTET, nicht ABWEICHEND",
              "VERALTET" in lauf.stdout and "ABWEICHEND" not in lauf.stdout)
        check("Rueckgabewert 1 (Voreinstellung meldet auch das)",
              lauf.returncode == 1, lauf.returncode)

        eng = werkzeug(ordner, "--nur-abweichung")
        check("mit --nur-abweichung Rueckgabewert 0", eng.returncode == 0,
              eng.returncode)

        # Gegenrichtung: derselbe Schalter darf eine echte Abweichung NICHT
        # verschlucken. Ohne diese Probe koennte --nur-abweichung schlicht
        # immer 0 liefern und die Pruefung oben waere wertlos.
        mutiere(ordner, "STARTING_CAPITAL = 10_000.0", "STARTING_CAPITAL = 20_000.0")
        eng2 = werkzeug(ordner, "--nur-abweichung")
        check("--nur-abweichung meldet die echte Abweichung weiterhin",
              eng2.returncode == 1, eng2.returncode)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ---------------------------------------------------------------------------
def test_fehlende_kurve():
    print("\n6) Eine fehlende Kurve ist ein Befund, kein Schweigen")
    ordner = probe_umgebung()
    try:
        lauf = werkzeug(ordner)
        check("Rueckgabewert 1", lauf.returncode == 1, lauf.returncode)
        check("meldet FEHLT", "FEHLT" in lauf.stdout)
        check("nennt die Folge (faellt aus der Summe)",
              "Summe" in lauf.stdout)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ---------------------------------------------------------------------------
def test_pruefen_schreibt_nicht():
    print("\n7) Die Pruefung schreibt nicht in die Ablage")
    ordner = probe_umgebung()
    try:
        werkzeug(ordner, "--erzeugen")
        pfad = ablage(ordner)
        vorher_zeit = os.path.getmtime(pfad)
        with open(pfad, "rb") as f:
            vorher_inhalt = f.read()

        # Auch im Befund-Fall darf nichts geschrieben werden - gerade dann.
        mutiere(ordner, "STARTING_CAPITAL = 10_000.0", "STARTING_CAPITAL = 20_000.0")
        lauf = werkzeug(ordner)
        check("die Pruefung meldet einen Befund", lauf.returncode == 1)

        with open(pfad, "rb") as f:
            nachher_inhalt = f.read()
        check("die abgelegte Datei ist unveraendert", vorher_inhalt == nachher_inhalt)
        check("und wurde nicht einmal neu geschrieben",
              os.path.getmtime(pfad) == vorher_zeit)
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


# ---------------------------------------------------------------------------
def test_pruefung_am_echten_repo_ist_folgenlos():
    print("\n8) Am echten Repo: die Pruefung laesst results/ in Ruhe")
    beobachtet = [ek.ablage_pfad(bot) for bot in ek.finde_bots()]
    vorher = {p: (os.path.getmtime(p), os.path.getsize(p))
              for p in beobachtet if os.path.exists(p)}
    check("es gibt Kurven zu beobachten", len(vorher) >= 5, len(vorher))

    lauf = subprocess.run(
        [sys.executable, os.path.join(_SHARED, "ergebniskurven.py"), "--bot", BOT],
        capture_output=True, text=True, cwd=BASE_DIR, timeout=600)
    check("der Lauf ist durchgelaufen", lauf.returncode in (0, 1),
          lauf.stderr[-200:])

    nachher = {p: (os.path.getmtime(p), os.path.getsize(p))
               for p in beobachtet if os.path.exists(p)}
    check("keine einzige abgelegte Kurve wurde angefasst", vorher == nachher)


# ---------------------------------------------------------------------------
def test_werkzeugverhalten():
    print("\n9) Randfaelle des Werkzeugs")
    lauf = subprocess.run(
        [sys.executable, os.path.join(_SHARED, "ergebniskurven.py"),
         "--bot", "gibt_es_nicht"],
        capture_output=True, text=True, cwd=BASE_DIR, timeout=120)
    check("unbekannter Bot: Rueckgabewert 2 (kein stilles 0)",
          lauf.returncode == 2, lauf.returncode)

    check("alle neun Bots werden automatisch gefunden",
          len(ek.finde_bots()) == 9, ek.finde_bots())
    check("der historische Pfad des Krypto-Elliott-Bots wird beruecksichtigt",
          ek.ablage_pfad("elliott_wave").endswith(
              os.path.join("results", "equity_curve.csv"))
          or os.path.exists(os.path.join(BASE_DIR, "results", "elliott_wave",
                                          "equity_curve.csv")),
          ek.ablage_pfad("elliott_wave"))


# ---------------------------------------------------------------------------
def test_vergleichsregeln():
    print("\n10) Die Einstufung selbst, in beide Richtungen")
    basis = pd.DataFrame({
        "time": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "symbol": ["AAA", "BBB", "CCC"],
        "pnl_pct": [1.0, -2.0, 3.0],
        "allocation": [1000.0, 1010.0, 990.0],
        "capital_after": [10010.0, 9990.0, 10020.0],
    })
    check("identisch -> AKTUELL",
          ek.vergleiche(basis, basis)["zustand"] == ek.AKTUELL)

    laenger = pd.concat([basis, basis.tail(1).assign(
        time="2024-01-04", symbol="DDD", capital_after=10030.0)], ignore_index=True)
    check("nur angewachsen -> VERALTET",
          ek.vergleiche(basis, laenger)["zustand"] == ek.VERALTET)
    check("abgelegte laenger als heute -> ABWEICHEND",
          ek.vergleiche(laenger, basis)["zustand"] == ek.ABWEICHEND)

    anderes_symbol = basis.copy()
    anderes_symbol.loc[1, "symbol"] = "XXX"
    check("gleiches PnL, anderes Symbol -> ABWEICHEND",
          ek.vergleiche(basis, anderes_symbol)["zustand"] == ek.ABWEICHEND)

    winzig = basis.copy()
    winzig.loc[2, "capital_after"] = 10020.0000001
    check("Unterschied unterhalb der Rundung -> AKTUELL (kein Rauschen)",
          ek.vergleiche(basis, winzig)["zustand"] == ek.AKTUELL)

    andere_schreibweise = basis.copy()
    andere_schreibweise["time"] = ["2024-01-01T00:00:00", "2024-01-02T00:00:00",
                                    "2024-01-03T00:00:00"]
    check("andere Zeitschreibweise, gleicher Zeitpunkt -> AKTUELL",
          ek.vergleiche(basis, andere_schreibweise)["zustand"] == ek.AKTUELL)

    echte_verschiebung = basis.copy()
    echte_verschiebung.loc[2, "capital_after"] = 10020.01
    check("Unterschied oberhalb der Rundung -> ABWEICHEND",
          ek.vergleiche(basis, echte_verschiebung)["zustand"] == ek.ABWEICHEND)


# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("Selbsttests der Ergebniskurven-Pruefung")
    print("=" * 78)
    tests = [test_erzeugung_wiederholbar, test_gegenprobe_aktuelle_kurve,
             test_kern_gleiche_zeilenzahl, test_hrp_fall_regimefilter,
             test_veraltet_gegen_abweichend, test_fehlende_kurve,
             test_pruefen_schreibt_nicht, test_pruefung_am_echten_repo_ist_folgenlos,
             test_werkzeugverhalten, test_vergleichsregeln]
    for test in tests:
        try:
            test()
        except Exception as fehler:                            # noqa: BLE001
            import traceback
            FEHLER.append(f"{test.__name__} (Ausnahme)")
            print(f"  [FEHLER] {test.__name__} warf eine Ausnahme: {fehler}")
            traceback.print_exc()

    print("\n" + "=" * 78)
    gesamt = BESTANDEN + len(FEHLER)
    print(f"{BESTANDEN} von {gesamt} Pruefungen bestanden, {len(FEHLER)} fehlgeschlagen.")
    for name in FEHLER:
        print(f"  - {name}")
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
