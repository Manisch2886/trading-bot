#!/usr/bin/env python3
"""
Woran haengt das System, das es nur einmal gibt? (TB-37)
==============================================================================
`shared/fetch_binance_data.py` war der Anlass: eine Datei, die **fuenf Bots
im Live-Betrieb** brauchen, die aber gitignoriert war und deshalb genau
einmal existierte - auf einem Rechner, ungesichert. Die Frage dahinter ist
groesser als die Datei:

**Gibt es noch mehr Stellen, an denen Betriebscode etwas liest, das nur
einmal existiert?**

Und die Gegenfrage, die TB-34 und TB-35 aufwerfen, weil beide `.gitignore`
erweitert haben: **wurde dabei etwas ausgeschlossen, das ins Repo gehoert?**

Wie das hier festgestellt wird
------------------------------------------------------------------------------
Mechanisch, in drei Schritten - nicht aus dem Gedaechtnis:

1. **Was ist ignoriert?** Die Eintraege aus `.gitignore`, wie git sie sieht.
   Jeder Eintrag wird ueber `git check-ignore` gegengeprueft, damit die
   Auslegung der Muster nicht nachgebaut wird.
2. **Wer liest es?** Ueber den **Syntaxbaum** aller Projektdateien: ein
   Import, dessen Modulname zu einem ignorierten `.py` passt, und jede
   Zeichenkette, die einen ignorierten Namen enthaelt. Ein Name in einem
   Kommentar zaehlt dabei nicht mit - Kommentare stehen nicht im Baum.
3. **Ist der Leser Betrieb oder Untersuchung?** Das ist der Unterschied
   zwischen "ein Bot steht" und "ein Bericht laesst sich nicht wiederholen".
   `research/` und `test_*.py` zaehlen als Untersuchung, alles andere als
   Betrieb.

Was hier NICHT mechanisch geht
------------------------------------------------------------------------------
Ob ein Verlust **ersetzbar** ist, steht in keiner Datei. Ein Zwischenspeicher
rechnet sich neu, eine Handelshistorie nicht. Diese Einschaetzung steht unten
in `ERSETZBARKEIT` als **Text** und ist als Einschaetzung gekennzeichnet -
nicht als Messung.

Die Untersuchung aendert nichts, fasst keinen Bot-Code an und **liest keine
ignorierte Datei** - sie stellt nur fest, dass und von wem sie gelesen wird.
Insbesondere oeffnet sie weder `.env` noch `config/email_config.py`.
Rueckgabewert 0 - sie ist ein Bericht, kein Waechter.

    python3 research/zugangsdaten/gitignoriert.py
    python3 research/zugangsdaten/gitignoriert.py --json daten/ignoriert.json
"""

import argparse
import ast
import json
import os
import subprocess
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
_WURZEL = os.path.dirname(os.path.dirname(_HIER))

# Betriebsordner zuerst - an ihnen haengt der taegliche Lauf.
BETRIEB = ["shared", "strategies", "notifications", "dashboard", "broker",
           "system", "config"]
UNTERSUCHUNG = ["research"]
ALLE_ORDNER = BETRIEB + UNTERSUCHUNG

# Die Einschaetzung, die sich NICHT aus dem Quelltext ergibt: was waere
# verloren, wenn die Datei verschwaende? Je Eintrag aus `.gitignore`.
# Ausdruecklich eine Einschaetzung, keine Messung.
ERSETZBARKEIT = {
    "config/email_config.py": (
        "UNERSETZLICH", "Zugangsdaten im Klartext, wie fetch_binance_data.py "
        "bis TB-37. Dieselbe Risikoklasse, derselbe Schnitt waere moeglich - "
        "ist aber NICHT Teil von TB-37."),
    "shared/fetch_binance_data.py": (
        "ERLEDIGT", "Bis TB-37 unersetzlich; seitdem ist der Code im Repo "
        "und nur noch die `.env` liegt draussen."),
    ".env": (
        "UNERSETZLICH", "Traegt seit TB-37 die Binance-Schluessel. Das ist "
        "Absicht - aber es ist damit die neue einzige Kopie. Sie gehoert in "
        "die Passwortverwaltung des Betreibers, nicht nur auf die Platte."),
    "*.db": (
        "UNERSETZLICH", "Die Handelsdatenbanken der neun Bots. Sie sind der "
        "gesamte Forward-Test-Verlauf seit Beginn - jede Papier-Position, "
        "jeder Ausstieg. Neu berechnen laesst sich das nicht: die Signale "
        "entstanden zu Zeitpunkten, die vorbei sind. Nach Umfang der groesste "
        "Posten dieser Liste."),
    "notifications/warteauftraege.json": (
        "HEIKEL", "Wartende Ausstiegsauftraege, die ein Cronjob spaeter ohne "
        "Rueckfrage ausfuehrt. Geht die Datei verloren, verschwindet der "
        "Auftrag - ohne Meldung, weil 'keine Warteauftraege' der Normalfall "
        "ist."),
    "notifications/state.json": (
        "ERSETZBAR", "Laufzeitzustand des Telegram-Dienstes. Neu aufgebaut "
        "waere hoechstens eine Meldung doppelt."),
    "notifications/waechter_zustand.json": (
        "ERSETZBAR", "Welcher Befund wurde wann zuletzt gemeldet. Verlust "
        "heisst: einmal zu viel gemeldet."),
    "results/portfolio_overview/dashboard_snapshot.json": (
        "ERSETZBAR", "Zwischenspeicher. Wird per Knopf oder Cron neu "
        "gerechnet."),
    "logs/": (
        "ERSETZBAR", "Protokolle. Der Verlust kostet Nachvollziehbarkeit, "
        "keinen Betrieb."),
    "data_sicherung/": (
        "ERSETZBAR", "Sicherungen von data/, das selbst im Repo liegt."),
    "trading-env/": (
        "ERSETZBAR", "Virtuelle Umgebung. requirements.txt baut sie neu."),
}


def gitignore_eintraege(wurzel):
    """Die Eintraege aus `.gitignore` - Text, Zeile, Art."""
    pfad = os.path.join(wurzel, ".gitignore")
    eintraege = []
    with open(pfad, encoding="utf-8") as datei:
        for nummer, zeile in enumerate(datei, 1):
            gestutzt = zeile.strip()
            if not gestutzt or gestutzt.startswith("#"):
                continue
            eintraege.append({
                "muster": gestutzt,
                "zeile": nummer,
                "art": ("Ordner" if gestutzt.endswith("/")
                        else "Muster" if "*" in gestutzt else "Datei"),
                "python": gestutzt.endswith(".py"),
            })
    return eintraege


def _pruefe_mit_git(wurzel, muster):
    """Haelt git diesen Namen wirklich fuer ignoriert?

    Nicht Kosmetik: `*.env` trifft `.env` und NICHT `.env.beispiel`, und das
    haengt an einer Auslegungsregel, die man nachbauen koennte - oder eben
    git fragen. Rueckgabe: True/False, oder None ohne git.
    """
    # Der abschliessende Schraegstrich bleibt stehen: `trading-env/` ist fuer
    # git ein Ordnermuster, `trading-env` ein Pfad, den es hier nicht gibt -
    # ohne den Schraegstrich meldete die Probe faelschlich "nicht ignoriert".
    probe = muster
    if "*" in probe:
        probe = probe.replace("*", "beispiel")
    try:
        lauf = subprocess.run(["git", "check-ignore", "-q", "--no-index",
                               probe],
                              cwd=wurzel, capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return lauf.returncode == 0


def _namen_aus_muster(muster):
    """Woran erkennt man im Quelltext, dass dieser Eintrag gemeint ist?

    Fuer `notifications/state.json` sind das `notifications/state.json` und
    `state.json`; fuer `*.db` die Endung; fuer `shared/xyz.py` zusaetzlich
    der Modulname `xyz`.
    """
    gestutzt = muster.rstrip("/")
    namen = {gestutzt}
    grundname = os.path.basename(gestutzt)
    if grundname and grundname != gestutzt:
        namen.add(grundname)
    if gestutzt.startswith("*."):
        namen = {gestutzt[1:]}                    # "*.db" -> ".db"
    modul = None
    if gestutzt.endswith(".py"):
        modul = os.path.basename(gestutzt)[:-3]
    return {n for n in namen if n}, modul


def leser(wurzel, muster):
    """Wer liest diesen Eintrag? Ueber den Syntaxbaum, nicht ueber Textsuche."""
    namen, modul = _namen_aus_muster(muster)
    treffer = {}

    for teil in ALLE_ORDNER:
        ordner = os.path.join(wurzel, teil)
        if not os.path.isdir(ordner):
            continue
        for pfad, _, dateien in os.walk(ordner):
            if "__pycache__" in pfad:
                continue
            for dateiname in sorted(dateien):
                if not dateiname.endswith(".py"):
                    continue
                voll = os.path.join(pfad, dateiname)
                rel = os.path.relpath(voll, wurzel)
                try:
                    with open(voll, encoding="utf-8") as datei:
                        text = datei.read()
                    baum = ast.parse(text)
                except (OSError, UnicodeDecodeError, SyntaxError):
                    continue

                # Docstrings sind zwar Zeichenketten im Baum, aber sie
                # sind Prosa: `.env` in einer Beschreibung heisst nicht,
                # dass die Datei gelesen wird. Sie werden hier ausgelassen -
                # sonst zaehlte jede Erwaehnung als Leser, und die Liste
                # saehe dramatischer aus, als sie ist.
                docstrings = set()
                for traeger in ast.walk(baum):
                    if isinstance(traeger, (ast.Module, ast.ClassDef,
                                            ast.FunctionDef,
                                            ast.AsyncFunctionDef)):
                        koerper = getattr(traeger, "body", None)
                        if (koerper and isinstance(koerper[0], ast.Expr)
                                and isinstance(koerper[0].value, ast.Constant)
                                and isinstance(koerper[0].value.value, str)):
                            docstrings.add(id(koerper[0].value))

                stellen = []
                for knoten in ast.walk(baum):
                    # a) Ein Import des ignorierten Moduls.
                    if modul:
                        if (isinstance(knoten, ast.ImportFrom)
                                and (knoten.module or "").endswith(modul)):
                            stellen.append((knoten.lineno, "import"))
                        elif isinstance(knoten, ast.Import):
                            for eintrag in knoten.names:
                                if eintrag.name.endswith(modul):
                                    stellen.append((knoten.lineno, "import"))
                    # b) Eine Zeichenkette, die den Namen enthaelt.
                    if (isinstance(knoten, ast.Constant)
                            and isinstance(knoten.value, str)
                            and id(knoten) not in docstrings):
                        if any(name in knoten.value for name in namen):
                            stellen.append((knoten.lineno, "Zeichenkette"))
                if stellen:
                    treffer[rel] = sorted(set(stellen))
    return treffer


def art_des_lesers(rel):
    if os.path.basename(rel).startswith("test_"):
        return "Selbsttest"
    if rel.split(os.sep)[0] in UNTERSUCHUNG:
        return "Untersuchung"
    return "Betrieb"


def sammle(wurzel=_WURZEL):
    befunde = []
    for eintrag in gitignore_eintraege(wurzel):
        gefunden = leser(wurzel, eintrag["muster"])
        nach_art = {}
        for rel, stellen in gefunden.items():
            nach_art.setdefault(art_des_lesers(rel), []).append(
                (rel, stellen))
        bewertung, begruendung = ERSETZBARKEIT.get(
            eintrag["muster"], ("(nicht eingeschaetzt)", ""))
        befunde.append({
            **eintrag,
            "git_bestaetigt": _pruefe_mit_git(wurzel, eintrag["muster"]),
            "leser": {art: sorted(eintraege)
                      for art, eintraege in sorted(nach_art.items())},
            "betrieb": len(nach_art.get("Betrieb", [])),
            "bewertung": bewertung,
            "begruendung": begruendung,
        })
    return befunde


def berichte(befunde, wurzel=_WURZEL):
    vom_betrieb = [b for b in befunde if b["betrieb"]]
    python_muster = [b for b in befunde if b["python"]]
    unersetzlich = [b for b in befunde
                    if b["bewertung"] in ("UNERSETZLICH", "HEIKEL")]

    print("=" * 78)
    print("WORAN HAENGT DAS SYSTEM, DAS ES NUR EINMAL GIBT? (TB-37)")
    print("=" * 78)
    print(f"\n{len(befunde)} Eintraege in .gitignore, "
          f"{len(vom_betrieb)} davon werden von Betriebscode gelesen.\n")

    print("1. IGNORIERT UND VOM BETRIEB GELESEN")
    print("   Das ist die Liste, um die es geht: hier liest laufender Code")
    print("   etwas, das in keinem Commit steht.\n")
    for eintrag in vom_betrieb:
        print(f"   {eintrag['muster']}   [{eintrag['bewertung']}]")
        for art in ("Betrieb", "Untersuchung", "Selbsttest"):
            for rel, stellen in eintrag["leser"].get(art, []):
                zeilen = ", ".join(str(z) for z, _ in stellen[:4])
                print(f"        {art:13s} {rel}  (Zeile {zeilen})")
        if eintrag["begruendung"]:
            for zeile in _umbruch(eintrag["begruendung"], 64):
                print(f"           {zeile}")
        print()

    print("2. IGNORIERT, ABER VOM BETRIEB NICHT GELESEN")
    for eintrag in befunde:
        if not eintrag["betrieb"]:
            gelesen = sum(len(v) for v in eintrag["leser"].values())
            print(f"   {eintrag['muster']:52s} "
                  f"{gelesen} Leser ausserhalb des Betriebs")

    print("\n3. DER SMELL, DER TB-37 AUSGELOEST HAT: IGNORIERTER QUELLTEXT")
    print("   Ein ignorierter `.py`-Eintrag ist die Form des Problems: "
          "Quelltext,")
    print("   der nicht im Repo steht. Zustandsdateien und Protokolle sind "
          "etwas")
    print("   anderes - sie entstehen neu.\n")
    if not python_muster:
        print("   Keiner mehr. Seit TB-37 ist shared/fetch_binance_data.py "
              "versioniert.")
    for eintrag in python_muster:
        print(f"   {eintrag['muster']}  (Zeile {eintrag['zeile']} der "
              f".gitignore)  [{eintrag['bewertung']}]")
        for zeile in _umbruch(eintrag["begruendung"], 68):
            print(f"      {zeile}")

    print("\n4. WURDE VERSEHENTLICH ETWAS AUSGESCHLOSSEN, DAS INS REPO "
          "GEHOERT?")
    print("   Geprueft wird die FORM, nicht der Inhalt: ein Eintrag, der "
          "Quelltext")
    print("   meint, faellt auf; ein Eintrag, der Zustand meint, nicht.")
    verdacht = [b for b in python_muster]
    if not verdacht:
        print("   Kein Eintrag nennt mehr eine Quelltextdatei.")
    else:
        for eintrag in verdacht:
            print(f"   VERDACHT: {eintrag['muster']}")
    ohne_git = [b for b in befunde if b["git_bestaetigt"] is False]
    if ohne_git:
        print("\n   Eintraege, bei denen git die Auslegung NICHT bestaetigt "
              "(pruefen):")
        for eintrag in ohne_git:
            print(f"      Zeile {eintrag['zeile']}: {eintrag['muster']}")
    elif all(b["git_bestaetigt"] is None for b in befunde):
        print("\n   (git nicht verfuegbar - die Muster wurden nicht "
              "gegengeprueft.)")
    else:
        print("\n   Alle Muster von `git check-ignore` bestaetigt.")

    print("\n5. EINSCHAETZUNG - KEINE MESSUNG")
    print("   Ob ein Verlust ersetzbar ist, steht in keiner Datei. Diese "
          "Spalte ist")
    print("   Text aus ERSETZBARKEIT in dieser Untersuchung, nicht "
          "erschlossen.\n")
    for eintrag in sorted(unersetzlich,
                          key=lambda b: (b["bewertung"], b["muster"])):
        print(f"   [{eintrag['bewertung']}] {eintrag['muster']}")

    print("\n" + "=" * 78)
    print(f"Zusammenfassung: {len(vom_betrieb)} von {len(befunde)} "
          f"gitignorierten Eintraegen werden")
    print(f"vom Betrieb gelesen; {len(unersetzlich)} davon waeren bei Verlust "
          f"nicht oder nur")
    print(f"schwer zu ersetzen. Ignorierten Quelltext gibt es "
          f"{'noch: ' + ', '.join(b['muster'] for b in python_muster) if python_muster else 'nicht mehr'}.")


def _umbruch(text, breite):
    zeilen, laufend = [], ""
    for wort in text.split():
        if len(laufend) + len(wort) + 1 > breite:
            zeilen.append(laufend)
            laufend = wort
        else:
            laufend = f"{laufend} {wort}".strip()
    if laufend:
        zeilen.append(laufend)
    return zeilen


def main(argv=None) -> int:
    zerleger = argparse.ArgumentParser(
        description="Welche gitignorierten Dateien liest Betriebscode?")
    zerleger.add_argument("--wurzel", default=_WURZEL)
    zerleger.add_argument("--json", default=None)
    argumente = zerleger.parse_args(argv)

    befunde = sammle(argumente.wurzel)
    berichte(befunde, argumente.wurzel)

    if argumente.json:
        ziel = (argumente.json if os.path.isabs(argumente.json)
                else os.path.join(_HIER, argumente.json))
        if os.path.dirname(ziel):
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
        with open(ziel, "w", encoding="utf-8") as datei:
            json.dump(befunde, datei, indent=2, ensure_ascii=False,
                      sort_keys=True, default=str)
        print(f"\nJSON: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
