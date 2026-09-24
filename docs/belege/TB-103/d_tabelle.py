"""TB-103 D: die Tabelle je Bot aus den Zusammenfassungen des Umschlags
(d_trockenlauf.py) und dem Lesehaken (d_lesequellen.py-Klassen), fuer eine Art
(modus|ohne), und - mit zwei Arten - der Vergleich der geladenen Mengen.
Keine Trade-Zahl, keine Kennzahl (Sichtschutz 27.1).

Aufruf:  python3 d_tabelle.py <scratch>/d <repo> <scratch>
"""
import json
import os
import sys

wurzel, repo, scratch = sys.argv[1], os.path.realpath(sys.argv[2]), os.path.realpath(sys.argv[3])
SNAP = os.path.join(repo, "snapshots", "63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2")
BOTS = ("elliott_wave t3_supertrend rsi2_crypto turtle_soup_crypto volatility_breakout_crypto "
        "elliott_wave_stocks rsi2_mean_reversion turtle_soup_stocks volatility_breakout").split()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def klasse(echt):
    if echt.endswith((".py", ".pyc")) or "/__pycache__/" in echt:
        return "code"
    if echt.startswith(os.path.join(repo, "trading-env") + os.sep) or "/lib/python" in echt \
            or "site-packages" in echt or "/Library/Caches/com.apple.python" in echt:
        return "pakete"
    if echt.startswith(SNAP + os.sep):
        return "snapshot"
    if echt.startswith(scratch + os.sep):
        return "scratch"
    for unter in ("data", "config", "research", "results", "logs"):
        if echt.startswith(os.path.join(repo, unter) + os.sep):
            return "repo_" + unter
    if echt.startswith(repo + os.sep):
        return "repo_sonst"
    return "system"


def zugriffe(prot):
    k = {}
    for name in os.listdir(prot):
        for zeile in open(os.path.join(prot, name), encoding="utf-8"):
            if zeile.startswith("#argv"):
                continue
            teile = zeile.rstrip("\n").split("\t")
            echt = os.path.realpath(teile[1])
            k.setdefault(klasse(echt), set()).add(echt)
    return k


def zeile(art, bot):
    o = os.path.join(wurzel, art, bot)
    rc = open(os.path.join(o, "rc")).read().strip()
    zf = os.path.join(o, "ziel", "zusammenfassung.json")
    z = json.load(open(zf, encoding="utf-8")) if os.path.exists(zf) else {}
    k = zugriffe(os.path.join(o, "prot"))
    ausgabe = open(os.path.join(o, "ausgabe.txt"), encoding="utf-8").read()
    daten_aussen = sorted(p.replace(repo, "<repo>") for kl in ("repo_data", "repo_config", "repo_research",
                                                              "repo_results", "repo_logs")
                          for p in k.get(kl, ()))
    umgebung = sorted(p.replace(repo, "<repo>") for kl in ("repo_sonst", "system") for p in k.get(kl, ()))
    return {
        "bot": bot, "rc": rc,
        "datei": os.path.relpath(z.get("symbolliste_datei", "?"), repo).replace(
            os.path.relpath(SNAP, repo), "<snapshot>"),
        "zeilen": z.get("universum_zeilen"), "exclude": z.get("exclude_symbols"),
        "erwartet": z.get("erwartet_nach_exclude"), "liste": z.get("symbolliste_n"),
        "liste_gleich": z.get("symbolliste_gleich_universum"),
        "geladen": z.get("geladen_n"), "nicht_geladen": z.get("nicht_geladen"),
        "standardliste": ausgabe.count("Standardliste"),
        "summe": (z.get("summenzeile") or ["-"])[0],
        "snap_csv": sum(p.endswith(".csv") for p in k.get("snapshot", ())),
        "daten_aussen": daten_aussen, "umgebung": umgebung,
        "code": len(k.get("code", ())), "code_repo": sum(p.startswith(repo) for p in k.get("code", ())),
        "geladen_menge": z.get("_geladen_menge"),
        "signal": z.get("signalpfad_gelaufen"), "sim": z.get("simulation_gelaufen"),
        "_z": z,
    }


arten = [a for a in ("modus", "ohne") if os.path.isdir(os.path.join(wurzel, a))]
tab = {a: {b: zeile(a, b) for b in BOTS} for a in arten}
for a in arten:
    print("=" * 110)
    print("Art: %s" % a)
    print("%-27s %-3s %-34s %-6s %-9s %-6s %-5s %-8s %-5s %-8s %-6s %-6s" % (
        "Bot", "rc", "Universumsdatei", "Zeilen", "nach Excl", "Liste", "=Uni", "geladen", "Std.", "SnapCSV",
        "Daten", "Umgeb."))
    for b in BOTS:
        r = tab[a][b]
        print("%-27s %-3s %-34s %-6s %-9s %-6s %-5s %-8s %-5s %-8s %-6s %-6s" % (
            b, r["rc"], r["datei"], r["zeilen"], r["erwartet"], r["liste"], "ja" if r["liste_gleich"] else "NEIN",
            r["geladen"], r["standardliste"], r["snap_csv"], len(r["daten_aussen"]), len(r["umgebung"])))
    print()
    for b in BOTS:
        r = tab[a][b]
        print("  %-27s Summenzeile: %s" % (b, r["summe"]))
        print("  %-27s nicht geladen: %s" % ("", ", ".join(r["nicht_geladen"] or []) or "-"))
        print("  %-27s Signalpfad gelaufen: %s, eine Simulation gelaufen: %s" % ("", r["signal"], r["sim"]))
        d = r["daten_aussen"]
        print("  %-27s Daten ausserhalb Snapshot (data/config/research/results/logs): %s" % (
            "", ("%d: %d x <repo>/data/*.csv, %s" % (
                len(d), sum(x.startswith("<repo>/data/") for x in d),
                [x for x in d if not x.startswith("<repo>/data/")])) if d else "keine"))
        print("  %-27s Laufumgebung ausserhalb (Repo sonst, System): %s" % ("", r["umgebung"]))
        print("  %-27s Code-Dateien: %d (davon im Repo %d) - getrennt gezaehlt, nicht Daten" % (
            "", r["code"], r["code_repo"]))
if len(arten) == 2:
    print("=" * 110)
    print("Vergleich der geladenen Menge mit und ohne Modus")
    for b in BOTS:
        m, o = tab["modus"][b]["_z"], tab["ohne"][b]["_z"]
        gl = (m.get("geladen_n") == o.get("geladen_n")
              and m.get("nicht_geladen") == o.get("nicht_geladen")
              and m.get("symbolliste_n") == o.get("symbolliste_n"))
        print("  %-27s modus %s von %s / ohne %s von %s  -> %s" % (
            b, m.get("geladen_n"), m.get("symbolliste_n"), o.get("geladen_n"), o.get("symbolliste_n"),
            "GLEICH" if gl else "VERSCHIEDEN"))
