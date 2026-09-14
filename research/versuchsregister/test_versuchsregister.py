#!/usr/bin/env python3
"""
Tests fuer TB-29 - Versuchsregister
====================================
    python3 research/versuchsregister/test_versuchsregister.py

Laeuft ohne pandas, ohne Kursdaten, ohne Netz. Schreibt nur in ein
temporaeres Verzeichnis; das Arbeitsverzeichnis bleibt unberuehrt (der
letzte Test weist das per `git status` nach).

Zwei Fallen aus #73, #77, #78, #79, #81, #86, TB-15, TB-20, TB-22, TB-26
sind hier ausdruecklich adressiert:

**Falle 1 - eine Probe bestaetigt sich selbst.** Ein Test, der eine Datei
veraendert und danach prueft, dass die Datei veraendert ist, misst seine
eigene Vorbereitung. Deshalb wird hier nie ein hergestellter *Zustand*
geprueft, sondern immer ein *Ablauf*: derselbe Sandkasten wird VOR der
Mutation geprueft (muss schweigen), dann mutiert (muss anschlagen), dann
zurueckgesetzt (muss wieder schweigen). Der Uebergang ist der Nachweis -
nur er kann nicht aus der Vorbereitung folgen.

**Falle 2 - eine zweite Wache verdeckt das Fehlen der ersten.** Der
Waechter hat drei Wachen (Raster, Ergebnisdateien, Forschungsraster).
Wuerde man alle drei gleichzeitig stoeren, bliebe ein Test auch dann
gruen, wenn eine davon ersatzlos entfernt waere. Die Proben sprechen
deshalb GENAU EINE Wache an - moeglich, weil `pruefen()` drei getrennte
Wurzeln annimmt - und pruefen nicht nur, DASS ein Befund kommt, sondern
dass es GENAU EINER ist und welcher.
"""

import ast
import os
import shutil
import subprocess
import sys
import tempfile

_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(_DIR))
sys.path.insert(0, _DIR)

import raster as R                                          # noqa: E402
import versuchsregister as V                                # noqa: E402

_FEHLER = []
_OK = 0


def pruefe(bedingung, beschreibung):
    global _OK
    if bedingung:
        _OK += 1
        print(f"  OK    {beschreibung}")
    else:
        _FEHLER.append(beschreibung)
        print(f"  FEHLT {beschreibung}")


def abschnitt(titel):
    print(f"\n{titel}\n{'-' * len(titel)}")


# ===========================================================================
def test_zaehler_kennt_alle_vier_rasterformen():
    """Die neun Bots bilden ihr Raster in vier verschiedenen Formen.

    Ein Zaehler, der nur `itertools.product` kennt, meldet fuer die
    anderen drei stillschweigend nichts - und 'nichts' sieht in einer
    Summe aus wie 'null Versuche'. Jede Form bekommt hier eine eigene
    Zusicherung, damit der Ausfall EINER Form sichtbar wird.
    """
    abschnitt("1. Der Zaehler erfasst alle vier Rasterformen")
    faelle = [
        ("itertools.product", "elliott_wave", "multi_symbol_optimise.py", 36),
        ("Anhaengen in Schleife", "elliott_wave_stocks", "multi_symbol_optimise.py", 64),
        ("verschachtelte for-Schleifen", "rsi2_crypto", "multi_symbol_optimise.py", 18),
        ("List-Comprehension", "rsi2_mean_reversion", "multi_symbol_optimise.py", 6),
    ]
    for form, bot, datei, erwartet in faelle:
        wert, grund = R.raster(os.path.join(BASE_DIR, "strategies", bot, datei))
        pruefe(wert == erwartet,
               f"{form}: {bot} -> {erwartet} (gezaehlt: {wert}{'' if wert else ' / ' + str(grund)})")


def test_zaehler_loest_nachbarimport_auf():
    """`multi_symbol_walk_forward.py` holt sein Raster per Import.

    Wer die Datei fuer sich betrachtet, findet dort keine Rastergrenzen
    und meldete 1 statt 19. Der Fall ist echt: er ist bei der Entwicklung
    dieses Werkzeugs genau so aufgetreten.
    """
    abschnitt("2. Raster aus dem Nachbarmodul")
    wert, grund = R.raster(os.path.join(
        BASE_DIR, "strategies", "rsi2_crypto", "multi_symbol_walk_forward.py"))
    pruefe(wert == 19, f"rsi2_crypto Walk-Forward -> 19 (18 IS + 1 OOS), gezaehlt: {wert}")
    wert, _ = R.raster(os.path.join(
        BASE_DIR, "strategies", "elliott_wave", "multi_symbol_walk_forward.py"))
    pruefe(wert == 37, f"elliott_wave Walk-Forward -> 37 (ruft run_multi_optimisation), gezaehlt: {wert}")


def test_zaehler_meldet_unklar_statt_null():
    """Eine Null waere die gefaehrlichste Ausgabe dieses Werkzeugs.

    Sie faellt in einer Summe nicht auf. Wo der Zaehler die Stelle nicht
    findet, muss `unklar` samt Grund herauskommen - nicht 0.
    """
    abschnitt("3. Unzaehlbares wird gemeldet, nicht auf 0 gesetzt")
    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, "ohne_stelle.py")
        with open(pfad, "w", encoding="utf-8") as fh:
            fh.write("WERTE = [1, 2, 3]\n"
                     "if __name__ == '__main__':\n"
                     "    for w in WERTE:\n"
                     "        print(w)\n")
        wert, grund = R.raster(pfad)
        pruefe(wert is None and "keine Auswertungsstelle" in (grund or ""),
               f"Datei ohne Auswertungsstelle -> unklar (bekommen: {wert} / {grund})")

        pfad2 = os.path.join(ordner, "unbekannte_schleife.py")
        with open(pfad2, "w", encoding="utf-8") as fh:
            fh.write("import json\n"
                     "def evaluate_combination_multi(x):\n"
                     "    return x\n"
                     "if __name__ == '__main__':\n"
                     "    for w in json.load(open('raster.json')):\n"
                     "        evaluate_combination_multi(w)\n")
        wert, grund = R.raster(pfad2)
        pruefe(wert is None and "statisch Unbekanntes" in (grund or ""),
               f"Schleife ueber Unbekanntes mit Auswertung -> unklar (bekommen: {wert} / {grund})")


def test_zaehler_folgt_einer_erweiterung():
    """Gegenprobe zum Zaehler selbst: wird ein Raster erweitert, muss die
    NEUE Zahl herauskommen. Ein Zaehler, der die alte Zahl faende (etwa
    aus einem Kommentar oder einer zweiten Fundstelle), waere hier gruen,
    obwohl er das Falsche liest."""
    abschnitt("4. Der Zaehler liest den Code, nicht eine Nebenquelle")
    quelle = os.path.join(BASE_DIR, "strategies", "volatility_breakout_crypto",
                          "multi_symbol_optimise.py")
    with tempfile.TemporaryDirectory() as ordner:
        ziel = os.path.join(ordner, "multi_symbol_optimise.py")
        text = open(quelle, encoding="utf-8").read()
        vorher, _ = R.raster(quelle)
        with open(ziel, "w", encoding="utf-8") as fh:
            fh.write(text.replace("STOP_LOSS_RANGE = [3.0, 5.0, 8.0, None]",
                                  "STOP_LOSS_RANGE = [3.0, 5.0, 8.0, 11.0, None]", 1))
        nachher, grund = R.raster(ziel)
        pruefe(vorher == 4, f"Ausgangsstand 4 (gezaehlt: {vorher})")
        pruefe(nachher == 5, f"nach Erweiterung 5 (gezaehlt: {nachher} / {grund})")


# ===========================================================================
def _sandkasten_strategien(ordner):
    """`strategies/`-Abbild: ein echter Ordner, die Bots als Verweise.

    Nur der Bot, der mutiert wird, wird kopiert - alle anderen bleiben
    Verweise auf das Original. So kann die Probe nichts anderes
    verstellen, und die uebrigen 20 Rasterstellen sind nachweislich
    unveraendert.
    """
    abbild = os.path.join(ordner, "strategies")
    os.makedirs(abbild)
    for bot in os.listdir(os.path.join(BASE_DIR, "strategies")):
        quelle = os.path.join(BASE_DIR, "strategies", bot)
        if os.path.isdir(quelle):
            os.symlink(quelle, os.path.join(abbild, bot))
    return abbild


def _ersetze_bot_durch_kopie(abbild, bot):
    verweis = os.path.join(abbild, bot)
    os.unlink(verweis)
    shutil.copytree(os.path.join(BASE_DIR, "strategies", bot), verweis)
    return verweis


def test_waechter_ablauf_raster():
    """Die Kernprobe - als ABLAUF, nicht als Zustand.

    schweigt -> mutiert -> schlaegt an -> zurueckgesetzt -> schweigt.
    Der mittlere Schritt allein bewiese nichts (ein Waechter, der IMMER
    anschlaegt, bestuende ihn auch); erst zusammen mit den beiden
    schweigenden Schritten ist die Aussage vollstaendig.

    Der Sandkasten ist so gebaut, dass NUR die Rasterwache anspringen
    kann: Ergebnisdateien und Forschungsraster zeigen unveraendert auf
    das Original.
    """
    abschnitt("5. Waechter, Rasterwache: schweigt - schlaegt an - schweigt")
    with tempfile.TemporaryDirectory() as ordner:
        abbild = _sandkasten_strategien(ordner)

        code, befunde, _ = V.pruefe_befunde(strategien=abbild)
        pruefe(code == 0 and not befunde,
               f"VORHER: unveraenderter Sandkasten -> RC 0, keine Befunde "
               f"(RC {code}, {len(befunde)} Befunde)")

        bot = "volatility_breakout_crypto"
        kopie = _ersetze_bot_durch_kopie(abbild, bot)
        datei = os.path.join(kopie, "multi_symbol_optimise.py")
        text = open(datei, encoding="utf-8").read()
        assert "STOP_LOSS_RANGE = [3.0, 5.0, 8.0, None]" in text
        with open(datei, "w", encoding="utf-8") as fh:
            fh.write(text.replace("STOP_LOSS_RANGE = [3.0, 5.0, 8.0, None]",
                                  "STOP_LOSS_RANGE = [3.0, 5.0, 8.0, 11.0, None]", 1))

        code, befunde, ausgabe = V.pruefe_befunde(strategien=abbild)
        pruefe(code == 1, f"MUTIERT: Rueckgabewert 1 (bekommen: {code})")

        # ZWEI Befunde, und das ist richtig so: multi_symbol_walk_forward.py
        # holt sein Raster per Import aus multi_symbol_optimise.py, waechst
        # also mit. Genau EIN Befund zu erwarten waere hier der Fehler -
        # der Waechter soll die Fortpflanzung ja sehen. Entscheidend fuer
        # die Aussage ist, dass AUSSCHLIESSLICH die Rasterwache anspricht.
        arten = sorted({b[0] for b in befunde})
        pruefe(arten == [V.RASTER_GEAENDERT],
               f"MUTIERT: ausschliesslich {V.RASTER_GEAENDERT} - keine zweite "
               f"Wache traegt das Ergebnis mit (bekommen: {arten})")
        stellen = sorted(b[1].split(":")[0].split()[-1] for b in befunde)
        pruefe(stellen == [f"{bot}/multi_symbol_optimise.py",
                           f"{bot}/multi_symbol_walk_forward.py"],
               f"MUTIERT: genau die beiden Stellen dieses Bots (bekommen: {stellen})")
        text_optimise = next((b[1] for b in befunde
                              if "multi_symbol_optimise.py" in b[1]), "")
        pruefe("Register 4, heute 5" in text_optimise,
               f"MUTIERT: Befund nennt alte und neue Zahl ({text_optimise})")
        text_wf = next((b[1] for b in befunde
                        if "multi_symbol_walk_forward.py" in b[1]), "")
        pruefe("Register 5, heute 6" in text_wf,
               f"MUTIERT: die Fortpflanzung in den Walk-Forward wird mitgemeldet "
               f"({text_wf})")

        with open(datei, "w", encoding="utf-8") as fh:
            fh.write(text)
        code, befunde, _ = V.pruefe_befunde(strategien=abbild)
        pruefe(code == 0 and not befunde,
               f"NACHHER: zurueckgesetzt -> RC 0, keine Befunde "
               f"(RC {code}, {len(befunde)} Befunde)")


def test_waechter_ablauf_ergebnisdatei():
    """Dieselbe Probe fuer die zweite Wache - und der Gegenbeweis zu
    Falle 2: hier darf KEIN Rasterbefund kommen. Kaeme einer, waere nicht
    die Zeilenwache nachgewiesen, sondern nur irgendeine."""
    abschnitt("6. Waechter, Zeilenwache: greift allein")
    with tempfile.TemporaryDirectory() as ordner:
        abbild = os.path.join(ordner, "results")
        os.makedirs(abbild)
        quelle = os.path.join(BASE_DIR, "results")
        for eintrag in os.listdir(quelle):
            os.symlink(os.path.join(quelle, eintrag), os.path.join(abbild, eintrag))

        code, befunde, _ = V.pruefe_befunde(ergebnisse=abbild)
        pruefe(code == 0 and not befunde,
               f"VORHER: Abbild ohne Aenderung -> RC 0 ({code}, {len(befunde)})")

        bot = "turtle_soup_stocks"
        os.unlink(os.path.join(abbild, bot))
        shutil.copytree(os.path.join(quelle, bot), os.path.join(abbild, bot))
        datei = os.path.join(abbild, bot, "multi_symbol_optimisation_results.csv")
        with open(datei, "a", encoding="utf-8") as fh:
            fh.write("99,99,0,0,0,0,0,0,0,0\n")

        code, befunde, _ = V.pruefe_befunde(ergebnisse=abbild)
        pruefe(code == 1, f"MUTIERT: Rueckgabewert 1 (bekommen: {code})")
        pruefe(len(befunde) == 1, f"MUTIERT: genau ein Befund ({len(befunde)})")
        art = befunde[0][0] if befunde else None
        pruefe(art == V.ZEILEN_GEAENDERT,
               f"MUTIERT: Befundart ist {V.ZEILEN_GEAENDERT} (bekommen: {art})")
        pruefe(all(b[0] != V.RASTER_GEAENDERT for b in befunde),
               "MUTIERT: KEIN Rasterbefund - die Zeilenwache steht fuer sich")


def test_waechter_bemerkt_fehlende_datei():
    """Eine geloeschte Ergebnisdatei ist ein Befund, kein Schweigen.

    Der Fall ist nicht theoretisch: eine fehlende Datei zaehlt in einer
    naiven Summe als 0 - und 0 faellt nicht auf.
    """
    abschnitt("7. Waechter: fehlende Ergebnisdatei")
    with tempfile.TemporaryDirectory() as ordner:
        abbild = os.path.join(ordner, "results")
        os.makedirs(abbild)
        quelle = os.path.join(BASE_DIR, "results")
        for eintrag in os.listdir(quelle):
            if eintrag == "rsi2_crypto":
                continue
            os.symlink(os.path.join(quelle, eintrag), os.path.join(abbild, eintrag))
        code, befunde, _ = V.pruefe_befunde(ergebnisse=abbild)
        pruefe(code == 1, f"Rueckgabewert 1 (bekommen: {code})")
        pruefe(len(befunde) == 1 and befunde[0][0] == V.ZEILEN_FEHLT,
               f"genau ein Befund vom Typ {V.ZEILEN_FEHLT} "
               f"(bekommen: {[b[0] for b in befunde]})")


def test_waechter_auf_dem_echten_stand():
    """Gegenprobe am Original: der Waechter darf HEUTE nicht anschlagen.

    Diese Zusicherung ist die Voraussetzung dafuer, dass die Proben oben
    ueberhaupt etwas aussagen.
    """
    abschnitt("8. Gegenprobe: unveraenderter Arbeitsstand")
    code, befunde, ausgabe = V.pruefe_befunde()
    pruefe(code == 0, f"Rueckgabewert 0 (bekommen: {code})")
    pruefe(not befunde, f"keine Befunde (bekommen: {[b[0] for b in befunde]})")
    pruefe("53 Angaben geprueft" in ausgabe,
           "es werden tatsaechlich 53 Angaben geprueft, nicht null "
           "(ein leerer Waechter waere ebenfalls gruen)")


def test_wiederholbar():
    """Zweimal derselbe Lauf, zeichengleiche Ausgabe."""
    abschnitt("9. Wiederholbarkeit")
    laeufe = []
    for _ in range(2):
        ergebnis = subprocess.run(
            [sys.executable, os.path.join(_DIR, "versuchsregister.py")],
            capture_output=True, text=True, cwd=BASE_DIR)
        laeufe.append(ergebnis.stdout)
    pruefe(laeufe[0] == laeufe[1], "zwei Laeufe, zeichengleiche Ausgabe")
    pruefe("SUMME" in laeufe[0] and "636" in laeufe[0],
           "die Ausgabe enthaelt die Rastersumme 636")


def test_summen_der_erhebung():
    """Die Zahlen, auf denen REGISTER.md steht - hier festgenagelt.

    Nicht als Wiederholung des Waechters, sondern als Bruecke: aendert
    sich eine davon, ist auch das Dokument falsch, nicht nur die Tabelle
    im Programm.
    """
    abschnitt("10. Summen, auf denen REGISTER.md steht")
    raster_ist = V.erhebe_raster()
    summe = sum(w for w, _ in raster_ist.values() if w is not None)
    unklar = [k for k, (w, _) in raster_ist.items() if w is None]
    pruefe(not unklar, f"alle 21 Rasterstellen zaehlbar (unklar: {unklar})")
    pruefe(summe == 636, f"Rastersumme 636 (gezaehlt: {summe})")

    nur_optimise = sum(w for (b, d), (w, _) in raster_ist.items()
                       if d == "multi_symbol_optimise.py" and w is not None)
    pruefe(nur_optimise == 237, f"neun Bot-Raster = 237 (gezaehlt: {nur_optimise})")

    zeilen = V.erhebe_ergebniszeilen()
    summe_bots = sum(zeilen[b] for b in V.BOTS)
    pruefe(summe_bots == 163, f"abgelegte Ergebniszeilen der neun Bots = 163 "
                              f"(gezaehlt: {summe_bots})")

    forschung = sum(v for v in V.erhebe_forschungszeilen().values() if v is not None)
    pruefe(forschung == 1886, f"Rasterzeilen unter research/ = 1886 (gezaehlt: {forschung})")

    text = open(os.path.join(_DIR, "REGISTER.md"), encoding="utf-8").read()
    for zahl in ("2 798", "653", "237", "246", "153"):
        pruefe(zahl in text, f"REGISTER.md nennt {zahl}")


PRODUKTIVORDNER = ("strategies", "shared", "results", "broker", "config",
                   "dashboard", "notifications", "system")


def _arbeitsbaum() -> str:
    """Der Zustand des Arbeitsbaums als Zeichenkette - Inhalt, nicht nur Namen.

    `git status --porcelain` allein wuerde eine Aenderung uebersehen, die eine
    Datei veraendert und wieder zuruecksetzt oder die eine bereits geaenderte
    Datei weiter veraendert. Der Hash der Arbeitsbaum-Unterschiede sieht auch das.
    """
    status = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True, cwd=BASE_DIR)
    diff = subprocess.run(["git", "diff", "--", *PRODUKTIVORDNER],
                          capture_output=True, text=True, cwd=BASE_DIR)
    return status.stdout + "\n---\n" + diff.stdout


def test_nichts_veraendert():
    """Die Untersuchung fasst keinen Bot-Code an - AM ABLAUF belegt.

    Bis TB-30a stand hier eine andere Pruefung: `git status` durfte nichts
    ausserhalb von `research/` und `docs/` melden. Die war falsch gebaut, und
    zwar auf eine Art, die erst auffiel, als sie zum ersten Mal anschlug.

    Sie prueft naemlich nicht diese Untersuchung, sondern den ARBEITSBAUM -
    und der enthaelt alles, woran gerade sonst noch gearbeitet wird. TB-30a
    aendert `shared/param_search_agent.py` und legt `shared/regimewache.py`
    an, beides ausdruecklich beauftragt und mit TB-29 nicht verwandt. Die alte
    Fassung meldete das als Verstoss von TB-29. Ein Waechter, der bei fremder
    Arbeit rot wird, wird abgeschaltet - und dann faengt er auch den Fall
    nicht mehr, fuer den er da ist.

    Was TB-29 zugesichert hat, ist eng und pruefbar: **ein Lauf dieser
    Untersuchung veraendert nichts.** Genau das steht jetzt hier. Der Zustand
    des Arbeitsbaums wird vorher und nachher aufgenommen, dazwischen laeuft
    die Untersuchung in allen ihren Betriebsarten. Beobachtet wird der
    ABLAUF, nicht ein hingelegter Zustand - und die Probe kann rot werden:
    wer der Erhebung eine Schreibzeile hinzufuegt, sieht sie hier scheitern.
    """
    abschnitt("11. Ein Lauf der Untersuchung veraendert nichts")
    ergebnis = subprocess.run(["git", "status", "--porcelain"],
                              capture_output=True, text=True, cwd=BASE_DIR)
    if ergebnis.returncode != 0:
        pruefe(False, "git status ausfuehrbar")
        return

    vorher = _arbeitsbaum()
    for schalter in ([], ["--pruefen"], ["--dsr"]):
        subprocess.run([sys.executable,
                        os.path.join(_DIR, "versuchsregister.py"), *schalter],
                       capture_output=True, text=True, cwd=BASE_DIR)
    nachher = _arbeitsbaum()
    pruefe(vorher == nachher,
           "ein Lauf der Erhebung laesst den Arbeitsbaum unveraendert")

    # Und die zweite Haelfte derselben Zusicherung, am Quelltext: wo ueberhaupt
    # geschrieben wird, geht es in ein Wegwerf-Verzeichnis. Geprueft ueber den
    # Syntaxbaum, nicht ueber eine Textsuche - `open(..., "w")` kommt sonst
    # auch in einem Kommentar vor, und ein Waechter, der auf Kommentare
    # anschlaegt, wird abgeschaltet.
    schreibend = []
    for name in sorted(os.listdir(_DIR)):
        if not name.endswith(".py") or name.startswith("test_"):
            continue
        pfad = os.path.join(_DIR, name)
        baum = ast.parse(open(pfad, encoding="utf-8").read())
        for funktion in ast.walk(baum):
            if not isinstance(funktion, (ast.FunctionDef, ast.AsyncFunctionDef,
                                         ast.Module)):
                continue
            quelle = ast.dump(funktion)
            schreibt = False
            for knoten in ast.walk(funktion):
                if not isinstance(knoten, ast.Call):
                    continue
                ziel = getattr(knoten.func, "id", None) or getattr(
                    knoten.func, "attr", None)
                if ziel == "open":
                    modi = [a.value for a in knoten.args[1:2]
                            if isinstance(a, ast.Constant)]
                    modi += [k.value.value for k in knoten.keywords
                             if k.arg == "mode" and isinstance(k.value, ast.Constant)]
                    if any(m and ("w" in m or "a" in m or "x" in m) for m in modi):
                        schreibt = True
                if ziel in ("to_csv", "to_json", "remove", "rmtree", "unlink"):
                    schreibt = True
            if schreibt and "TemporaryDirectory" not in quelle:
                stelle = getattr(funktion, "name", "<modulebene>")
                schreibend.append(f"{name}:{stelle}")
    pruefe(not schreibend,
           f"wo die Untersuchung schreibt, schreibt sie in ein "
           f"Wegwerf-Verzeichnis (aussen vor: {schreibend})")


def main():
    print("=" * 72)
    print("TB-29 - Tests fuer Versuchsregister und Waechter")
    print("=" * 72)
    for pruefung in (test_zaehler_kennt_alle_vier_rasterformen,
                     test_zaehler_loest_nachbarimport_auf,
                     test_zaehler_meldet_unklar_statt_null,
                     test_zaehler_folgt_einer_erweiterung,
                     test_waechter_ablauf_raster,
                     test_waechter_ablauf_ergebnisdatei,
                     test_waechter_bemerkt_fehlende_datei,
                     test_waechter_auf_dem_echten_stand,
                     test_wiederholbar,
                     test_summen_der_erhebung,
                     test_nichts_veraendert):
        pruefung()

    print("\n" + "=" * 72)
    if _FEHLER:
        print(f"{len(_FEHLER)} von {_OK + len(_FEHLER)} Zusicherungen FEHLGESCHLAGEN:")
        for f in _FEHLER:
            print(f"  - {f}")
        return 1
    print(f"Alle {_OK} Zusicherungen bestanden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
