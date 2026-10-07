#!/usr/bin/env python3
"""TB-140 Teil 2 - baut fundstellen.tsv aus den Quelldateien, nicht abgetippt.

Je Fundstelle steht hier nur Kennung, Datei, Zeile und ein Pruefstueck (das in der Zeile
stehen muss, sonst bricht das Skript ab: so trifft keine Kennung eine verschobene Zeile);
den Wortlaut liest das Skript aus der Datei. art `zeile`: die ganze Zeile ohne fuehrende und
schliessende Leerzeichen. art `teil` (nur Registerzeilen): der Ausschnitt vom Anfangs- bis
einschliesslich zum Endstueck, hoechstens 300 Zeichen.
Schreibt nur docs/belege/TB-140/fundstellen.tsv. Importiert nichts aus dem Repo.

Aufruf aus der Repo-Wurzel: trading-env/bin/python3 -B docs/belege/TB-140/fundstellen_bauen.py"""
import sys

AUS = "docs/belege/TB-140/fundstellen.tsv"
REG = "docs/VORREGISTRIERUNG_neuselektion.md"
BM = "research/vorregistrierung/benchmark.py"
AW = "research/vorregistrierung/auswertung.py"
BD = "research/vorregistrierung/beispieldaten.py"
RD = "research/vorregistrierung/registerdaten.py"
FP = "research/vorregistrierung/faltenplan.py"
TE = "research/vorregistrierung/test_ersatzwerte.py"
TV = "research/vorregistrierung/test_vorregistrierung.py"
PH = "research/tb24_haltedauern/positionen_holen.py"
MK = "research/mtm_drawdown/mtm_kern.py"
GL = "research/mtm_drawdown/grundlage.py"
MS = "research/mtm_drawdown/messung.py"
RF = "research/mtm_drawdown/richtungsfall.py"
TM = "research/mtm_drawdown/test_mtm_kern.py"
EX = "research/exposure_messung/auswertung.py"
PA = "shared/paths.py"
KD = "shared/kursdaten.py"

# (kennung, datei, zeile, pruefstueck) fuer art zeile;
# (kennung, datei, zeile, "teil", anfang, ende) fuer art teil
FUNDSTELLEN = [
    # --- V1 Nr. 0: Erzeuger-Suche -------------------------------------------------------
    ("V1-01", REG, 10857, "teil", "Ausgaben des Zellen-Erzeugers je Bot: zellen.csv", "herkunft.json mit teile (37.4)"),
    ("V1-02", AW, 3, "TB-30a - Das eingefrorene Auswertungsskript"),
    ("V1-03", AW, 5, "Dieses Programm liest die ROHERGEBNISSE eines Selektionslaufs"),
    ("V1-04", AW, 321, 'pfad = os.path.join(wurzel, bot, "zellen.csv")'),
    ("V1-05", AW, 379, 'pfad = os.path.join(wurzel, "benchmark_tagesreihen", f"{markt}.csv")'),
    ("V1-06", BD, 3, "TB-30a - Beispieldaten: Rohergebnisse mit frei erfundenen Werten"),
    ("V1-07", BD, 200, 'df.to_csv(os.path.join(ordner, "zellen.csv"), index=False)'),
    ("V1-08", BD, 210, 'with open(os.path.join(ordner, "herkunft.json"), "w", encoding="utf-8") as f:'),
    ("V1-09", BD, 233, 'os.path.join(wurzel, "benchmark_tagesreihen", f"{markt}.csv"), index=False)'),
    ("V1-10", TE, 3, "TB-106 - Rueckfall (d): stille Ersatzwerte"),
    ("V1-11", TE, 775, 'with open(os.path.join(w, {BOT!r}, "zellen.csv"), "w") as f:'),
    ("V1-12", TV, 3, "TB-30a - Selbsttest der Vorregistrierung"),
    ("V1-13", TV, 206, 'p = os.path.join(d, BOT, "zellen.csv")'),
    ("V1-14", PH, 2, "Ein Bot, ein Prozess: Positionen MIT Ausstiegsart und Kerzenzahl herausholen"),
    ("V1-15", PH, 219, '_schreibe_einmal(f"{BOT}_herkunft.json",'),
    # --- V1 Nr. 1: Benchmark --------------------------------------------------------------
    ("V1-16", BM, 120, "DATA_DIR = paths.DATA_DIR"),
    ("V1-17", BM, 121, "CONFIG_DIR = paths.CONFIG_DIR"),
    ("V1-18", BM, 139, "return os.path.join(CONFIG_DIR, os.path.basename(rd.UNIVERSUM[markt]))"),
    ("V1-19", BM, 145, 'return [x for x in s if x not in {"XAUTUSDT", "PAXGUSDT"}]'),
    ("V1-20", BM, 148, "def tagesschluss(markt: str) -> dict:"),
    ("V1-21", BM, 152, 'pfad = os.path.join(DATA_DIR, f"{s}_1d.csv")'),
    ("V1-22", BM, 155, 'df = pd.read_csv(pfad, parse_dates=["open_time"])'),
    ("V1-23", BM, 156, 'df = df.dropna(subset=["close"])'),
    ("V1-24", BM, 159, 'reihen[s] = pd.Series(df["close"].to_numpy(dtype=float),'),
    ("V1-25", BM, 253, 'kurse = {markt: tagesschluss(markt) for markt in ("aktien", "krypto")}'),
    ("V1-26", BM, 271, 'reihen = tagesgenau(kurse[eig["markt"]], handelbar)'),
    ("V1-27", TV, 1172, "print(markt, sorted(bm.tagesschluss(markt)))"),
    ("V1-28", TE, 225, '"bm.tagesschluss = lambda markt: {}\\n"'),
    ("V1-29", RD, 131, '"elliott_wave":               {"markt": "krypto", "zeitrahmen": "1h"},'),
    ("V1-30", RD, 132, '"t3_supertrend":              {"markt": "krypto", "zeitrahmen": "4h"},'),
    ("V1-31", RD, 133, '"rsi2_crypto":'),
    ("V1-32", RD, 134, '"turtle_soup_crypto":'),
    ("V1-33", RD, 135, '"volatility_breakout_crypto":'),
    ("V1-34", RD, 136, '"elliott_wave_stocks":'),
    ("V1-35", RD, 137, '"rsi2_mean_reversion":'),
    ("V1-36", RD, 138, '"turtle_soup_stocks":'),
    ("V1-37", RD, 139, '"volatility_breakout":'),
    # --- V1 Nr. 2: Kern -------------------------------------------------------------------
    ("V1-38", MK, 55, "* Er liest und schreibt keine Datei."),
    ("V1-39", MK, 135, "def tagesraster(schlusskurse: dict, von=None, bis=None) -> pd.DatetimeIndex:"),
    ("V1-40", MK, 139, "(Registertext 3b (c)): die 1d-Kursdateien in data/."),
    ("V1-41", MK, 151, "def kurse_auf_raster(schlusskurse: dict, tage: pd.DatetimeIndex):"),
    ("V1-42", GL, 34, "REPO_ROOT = os.path.dirname(os.path.dirname(_HIER))"),
    ("V1-43", GL, 35, 'DATA_DIR = os.path.join(REPO_ROOT, "data")'),
    ("V1-44", GL, 82, 'def lade_schlusskurse(symbole, zeitrahmen="1d") -> dict:'),
    ("V1-45", GL, 87, 'pfad = os.path.join(DATA_DIR, f"{s}_{zeitrahmen}.csv")'),
    ("V1-46", GL, 90, 'df = pd.read_csv(pfad, parse_dates=["open_time"]).dropna(subset=["close"])'),
    ("V1-47", GL, 91, 'reihen[s] = pd.Series(df["close"].to_numpy(dtype=float),'),
    ("V1-48", GL, 211, 'kerzen = lade_schlusskurse(symbole, meta.get("zeitrahmen", "1d"))'),
    ("V1-49", GL, 212, 'tages = lade_schlusskurse(symbole, "1d")'),
    ("V1-50", MS, 147, 'tages = grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")'),
    ("V1-51", MS, 153, "tage = mtm_kern.tagesraster("),
    ("V1-52", MS, 157, "kurse, fort = mtm_kern.kurse_auf_raster(tages, tage)"),
    ("V1-53", RF, 135, 'tages = grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")'),
    ("V1-54", TM, 121, 'kurse = grundlage.lade_schlusskurse(pos["symbol"].unique(), "1d")'),
    ("V1-55", EX, 32, 'DATA_DIR = os.path.join(_REPO_ROOT, "data")'),
    ("V1-56", EX, 86, 'pfad = os.path.join(DATA_DIR, f"{sym}_1d.csv")'),
    ("V1-57", EX, 96, 'kurse[sym] = df.set_index("open_time")["close"].sort_index()'),
    ("V1-58", EX, 305, "def mtm_reihen(bot, positionen, kurse, reihen):"),
    ("V1-59", EX, 323, "preis = reihe.reindex(tage.union(reihe.index)).ffill().reindex(tage).ffill().bfill()"),
    ("V1-60", REG, 11493, "teil", "Welchen Kern der Zellen-Erzeuger übernimmt", "legt kein Registertext fest"),
    # --- V1 Nr. 4: der Weg zum Snapshot -----------------------------------------------------
    ("V1-61", PA, 194, '_LIVE_DATA_DIR = os.path.join(BASE_DIR, "data")'),
    ("V1-62", PA, 205, 'UMGEBUNG_WURZEL = "TB_SELEKTIONSWURZEL"'),
    ("V1-63", PA, 679, "_MODUS = _modus_aus_umgebung()"),
    ("V1-64", PA, 685, "DATA_DIR = _LIVE_DATA_DIR"),
    ("V1-65", PA, 692, "DATA_DIR = _MODUS[0]"),
    ("V1-66", PA, 693, "CONFIG_DIR = os.path.join(_MODUS[0], CONFIG_UNTERORDNER)"),
    ("V1-67", REG, 8932, "teil", "Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des Resolvers", "`TB_SELEKTIONSWURZEL`)."),
    ("V1-68", EX, 91, "df, gestrichen = entferne_unvollstaendige(df, symbol=sym, melden=False)"),
    ("V1-69", GL, 46, "BOTS = ("),
    ("V1-70", "research/mtm_drawdown/alle_bots.py", 30, "for bot in BOTS:"),
    ("V1-71", "research/mtm_drawdown/alle_bots.py", 32, 'lauf = subprocess.run([sys.executable, os.path.join(_HIER, "messung.py"), bot],'),
    ("V1-72", MS, 110, "bot = botenv.setup(argv[0])"),

    # --- V3 Nr. 1: Register --------------------------------------------------------------------
    ("V3-01", REG, 11066, "zelle_id, <je Rasterachse eine Spalte>, falte, rolle, n_trades,"),
    ("V3-02", REG, 11067, "netto_sharpe, netto_rendite_pct, kapital_drawdown_pct,"),
    ("V3-03", REG, 11068, "mittlere_exposure"),
    ("V3-04", REG, 10797, "teil", "Eine (Zelle, Falte) ohne Trades trägt die Nullzeile", "nie nichts."),
    ("V3-05", REG, 1442, "Ist die Standardabweichung 0 (kein Trade in der Falte), ist der"),
    ("V3-06", REG, 1443, "Falten-Sharpe 0."),
    ("V3-07", REG, 1455, "*Formel für den Falten-Sharpe: Mittel / Standardabweichung der täglichen"),
    ("V3-08", REG, 10827, "teil", "zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct", "auf den Tagen des Benchmarks (3b (c))"),
    ("V3-09", REG, 10827, "teil", "und kapital_drawdown_ereignis_pct", "berichtet, nicht bewertet (24.2)."),
    ("V3-10", REG, 10827, "teil", "Die Spalte kapital_drawdown_pct wird", "nicht umgedeutet."),
    ("V3-11", REG, 10827, "teil", "Der Drawdown je Falte ist der Ausschnitt", "ohne Neustart des Kapitals."),
    ("V3-12", REG, 10936, "teil", "Mittlere Exposure = Mittel über die Handelstage des Zeitraums", "bewertet wie die MtM-Reihe (1a)."),
    ("V3-13", REG, 11342, "teil", "(a) „Handelstage des Zeitraums“ in R48 (d) lies:", "wie benchmark_tagesreihen/<bot>.csv sie führt (R39)"),
    ("V3-14", REG, 11431, "teil", "Alle Grössen dieser Zeile stehen auf den Tagen ab bestaetigung_ab_effektiv", "bis zum Ende der Spanne (35.1)."),
    ("V3-15", REG, 10810, "teil", "Der Zellen-Erzeuger schreibt je Bot eine Datei zellenbericht.csv", "und den Feldern:"),
    ("V3-16", REG, 10810, "teil", "die drei Werte aus 22.2", "bestaetigung_ab_effektiv (R37)."),
    ("V3-17", REG, 10810, "teil", "Anteil = Beitrag ÷ Gesamtertrag;", "das Feld trägt „nicht definiert“."),
    ("V3-18", REG, 10880, "teil", "haltedauer_balken ist die Zahl der Kerzen des Zeitrahmens des Bots", "beide eingeschlossen"),
    ("V3-19", REG, 1435, "Blocklänge L = max(mediane Haltedauer des Parametersatzes in Handelstagen,"),
    ("V3-20", REG, 10837, "teil", "Die Bestätigungsstatistik des Gewinners beginnt am ersten Handelstag", "mehr offen ist"),
    ("V3-21", REG, 10837, "teil", "Der Zellen-Erzeuger bestimmt diesen Tag für jede Zelle", "(bestaetigung_ab_effektiv, R34)"),
    ("V3-22", REG, 11424, "teil", "In jeder Tagesreihe (tagesreihen/<zelle>.csv)", "jeder Zahlenwert endlich."),
    ("V3-23", REG, 11424, "teil", "Für zellen.csv gilt R33.", "Für zellen.csv gilt R33."),
    ("V3-24", REG, 11097, "teil", "Für `zellenbericht.csv` (R34)", "führt der Docstring heute keine Feldliste"),
    ("V3-25", REG, 11052, "teil", "gelesen nur für die Bestätigungsperiode (Z. 624)", "trifft zu: Berichtsgrösse ohne Leser im Urteil"),
    # --- V3 Nr. 2: auswertung.py --------------------------------------------------------------
    ("V3-26", AW, 133, 'PFLICHTSPALTEN = ["zelle_id", "falte", "rolle", "n_trades", "netto_sharpe",'),
    ("V3-27", AW, 134, '"netto_rendite_pct", "kapital_drawdown_pct", "mittlere_exposure"]'),
    ("V3-28", AW, 137, "class Abbruch(SystemExit):"),
    ("V3-29", AW, 146, "super().__init__(paths.RUECKGABEWERT_STARTPRUEFUNG)"),
    ("V3-30", PA, 220, "RUECKGABEWERT_STARTPRUEFUNG = 2"),
    ("V3-31", AW, 320, "def lies_zellen(bot: str, wurzel: str, mess: dict, plan: dict) -> pd.DataFrame:"),
    ("V3-32", AW, 326, 'df = pd.read_csv(pfad, dtype={"falte": str, "zelle_id": str, "rolle": str})'),
    ("V3-33", AW, 329, 'raise Abbruch(f"{bot}: Spalten fehlen in zellen.csv: {fehlend}")'),
    ("V3-34", AW, 353, 'df["netto_sharpe"] = np.where(df["n_trades"].to_numpy() == 0, 0.0,'),
    ("V3-35", AW, 354, 'df["netto_sharpe"].to_numpy(dtype=float))'),
    ("V3-36", AW, 355, 'if df["netto_sharpe"].isna().any():'),
    ("V3-37", AW, 356, 'raise Abbruch(f"{bot}: netto_sharpe enthaelt Leerwerte in Falten MIT "'),
    ("V3-38", AW, 395, 'return teil.groupby("zelle_id")["netto_sharpe"].median()'),
    ("V3-39", AW, 405, 'e = float(z["mittlere_exposure"])'),
    ("V3-40", AW, 413, '"dd_satz": float(z["kapital_drawdown_pct"]),'),
    ("V3-41", AW, 414, '"bestanden": float(z["kapital_drawdown_pct"]) >= grenze,'),
    ("V3-42", AW, 577, 'values="netto_sharpe", aggfunc="first")'),
    ("V3-43", AW, 621, '"n_trades": int(z["n_trades"]),'),
    ("V3-44", AW, 624, '"netto_rendite_pct": float(z["netto_rendite_pct"]),'),
    ("V3-45", AW, 625, '"kapital_drawdown_pct": float(z["kapital_drawdown_pct"]),'),
    ("V3-46", AW, 626, '"mittlere_exposure": float(z["mittlere_exposure"]),'),
    ("V3-47", AW, 681, 'kz.drei_tiefste_drawdowns(gew_falten["kapital_drawdown_pct"]),'),
    ("V3-48", AW, 684, '"falten_sharpe": {r["falte"]: float(r["netto_sharpe"])'),
    ("V3-49", AW, 687, 'if int(r["n_trades"]) == 0],'),
    ("V3-50", AW, 179, "except (OSError, ValueError) as e:"),
    ("V3-51", AW, 140, "Ausgaenge von `auswertung.py`: 0 oder 2, kein 1"),
]

# V2 kommt aus einer zweiten Liste (fundstellen_v2.py), damit die zwei Teile getrennt pruefbar sind.
try:
    sys.path.insert(0, "docs/belege/TB-140")
    from fundstellen_v2 import FUNDSTELLEN_V2  # noqa: E402  (eigene Datei im Belegordner, kein Modul des Repos)
except ImportError:
    FUNDSTELLEN_V2 = []


def main():
    cache, aus, fehler = {}, [], []
    for f in FUNDSTELLEN + FUNDSTELLEN_V2:
        kennung, datei, zeile = f[0], f[1], f[2]
        if datei not in cache:
            with open(datei, encoding="utf-8") as h:
                cache[datei] = h.read().split("\n")
        text = cache[datei][zeile - 1]
        if len(f) == 4:
            if f[3] not in text:
                fehler.append("%s %s:%d Pruefstueck fehlt: %r" % (kennung, datei, zeile, f[3]))
                continue
            aus.append((kennung, datei, zeile, "zeile", text.strip()))
        else:
            assert f[3] == "teil" and datei.endswith(".md"), kennung
            a = text.find(f[4])
            e = text.find(f[5], a)
            if a < 0 or e < 0:
                fehler.append("%s %s:%d Anfang oder Ende fehlt" % (kennung, datei, zeile))
                continue
            stueck = text[a:e + len(f[5])]
            if len(stueck) > 300:
                fehler.append("%s Ausschnitt %d Zeichen" % (kennung, len(stueck)))
                continue
            aus.append((kennung, datei, zeile, "teil", stueck))
    kenn = [a[0] for a in aus]
    if len(set(kenn)) != len(kenn):
        fehler.append("Kennung doppelt")
    if fehler:
        for z in fehler:
            print("FEHLER", z)
        print("nichts geschrieben")
        return 2
    with open(AUS, "w", encoding="utf-8") as h:
        for a in aus:
            h.write("%s\t%s\t%d\t%s\t%s\n" % a)
    print("geschrieben: %s, %d Fundstellen (V1 %d, V2 %d, V3 %d)" % (
        AUS, len(aus), sum(k.startswith("V1") for k in kenn), sum(k.startswith("V2") for k in kenn),
        sum(k.startswith("V3") for k in kenn)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
