"""
Wer bekommt den Platz, wenn er knapp wird? Die Zuteilungskaskade
==============================================================================
Dieses Modul enthaelt die Kapitalsimulation aller neun Bots an EINER Stelle -
und mit ihr die Regel, nach der entschieden wird, wenn mehrere Signale zum
selben Zeitpunkt um denselben Platz konkurrieren.

    from zuteilung import simuliere_portfolio

Die neun `strategies/*/equity_simulation.py` rufen es ueber ihre eigene
`simulate_portfolio()` auf; dort steht nur noch, welcher Primaerschluessel
fuer diesen Bot gilt.

DER ANLASS (TB-23)
------------------------------------------------------------------------------
`shared/determinismus.py` hat gemessen: werden nur die ZEILEN von
`config/sp500_top150.txt` umsortiert, aendert sich bei acht von neun Bots das
Ergebnis - bei `volatility_breakout` schwankt die Rendite ueber zwanzig
Permutationen zwischen 145,16 % und 269,47 %. Die Signalerzeugung ist dabei
bitidentisch; abweichend ist allein, WER das Kapital bekommt.

Die Ursache sass an genau einer Stelle: in der alten `simulate_portfolio()`
wurden die Einstiegsereignisse mit `events.sort(key=(zeit, kein_ausstieg))`
sortiert. Pythons Sortierung ist stabil - bei gleichem Zeitpunkt blieb also
die Einfuegereihenfolge stehen, und die ist die Zeilenreihenfolge des
zusammengehaengten Trade-DataFrames, also die Symbolreihenfolge der
Konfigurationsdatei. **Ein Zweitkriterium gab es nicht.** Die Datei entschied
mit, ohne dass irgendwo stand, dass sie das tut.

DIE KASKADE
------------------------------------------------------------------------------
Vier Stufen, lexikographisch. Jede Stufe bekommt nur die Kandidaten, die auf
allen vorherigen Stufen gleichauf liegen:

  1. **Strategieeigene stetige Signalstaerke** - falls der Bot eine fuehrt.
     Staerkeres Signal zuerst. Welche Spalte das ist (und in welcher
     Richtung), steht als `SIGNALSPALTE` in der `equity_simulation.py` des
     jeweiligen Bots - und nirgendwo sonst.
  2. **Diversifikationsbeitrag** - Korrelation der Tagesrenditen des
     Kandidaten mit dem aktuellen, allokationsgewichteten Buch des Bots ueber
     die letzten 60 Handelstage. **Niedriger zuerst.** Bei leerem Buch
     entfaellt die Stufe.
  3. **Liquiditaet** - Median des Dollar-Volumens der letzten 20 Handelstage.
     Hoeher zuerst.
  4. **Seeded Zufall** - ein Fingerabdruck aus dem Inhalt des Trades und dem
     protokollierten Startwert `SEED`.

**Warum diese Reihenfolge** (die Begruendungen bestimmen die Umsetzung, sie
sind keine Zierde):

* *Diversifikation an zweiter Stelle*, weil das Mass stetig, point-in-time und
  oekonomisch bestimmt ist - bei gleicher Signalstaerke ist der Kandidat
  besser, der das Buch weniger konzentriert - und weil es **keinen Titel
  systematisch bevorzugt**: welcher Kandidat gewinnt, haengt davon ab, was
  gerade im Buch liegt, nicht davon, wie er heisst.
* *Liquiditaet erst an dritter Stelle*, weil sie ein reines
  Ausfuehrungskriterium ohne Alpha-Anspruch ist - und weil sie eine
  **Schlagseite zu Mega-Caps** hat. An zweiter Stelle wuerde sie AAPL und
  MSFT einen dauerhaften Vorrang geben.
* *Seeded Zufall statt Symbolname* auf der letzten Stufe: **ehrliche
  Beliebigkeit schlaegt versteckte.** Ein protokollierter Zufall ist sichtbar
  willkuerlich und reproduzierbar; die Dateireihenfolge war unsichtbar
  willkuerlich. Nach dem Symbolnamen zu sortieren waere zwar ebenfalls
  reproduzierbar, wuerde aber A-Titel dauerhaft bevorzugen - also genau die
  systematische Bevorzugung einfuehren, die Stufe 2 und 3 vermeiden.

WAS BEI FEHLENDER INFORMATION GESCHIEHT - UND WARUM NICHT "ANS ENDE"
------------------------------------------------------------------------------
Auf jeder der Stufen 1 bis 3 kann der Wert fuer einen einzelnen Kandidaten
fehlen: eine Strategie, die den Signalwert bei manchen Trades nicht
mitschreibt; ein Symbol mit weniger als `MIN_KORRELATIONSTAGE` Tagen
Vorgeschichte; ein Symbol ohne Volumendaten.

Die Behandlung ist auf allen drei Stufen **dieselbe und benannt**: der
Kandidat bekommt den **Median der Kandidaten, fuer die der Wert an diesem
Zeitpunkt vorliegt** - er steht damit in der Mitte des Feldes und gewinnt
weder noch verliert er durch die Luecke. Koennen es alle nicht, entfaellt die
Stufe und die Kaskade rueckt auf.

Die drei naheliegenden Alternativen sind verworfen, jede aus einem Grund:

* *Ans Ende stellen* - benachteiligt junge Symbole systematisch. Genau das
  soll die Kaskade nicht tun.
* *Korrelation 0 einsetzen* - 0 ist der BESTE erreichbare Wert auf Stufe 2.
  Ein Symbol ohne Historie wuerde dadurch bevorzugt, und zwar umso mehr, je
  weniger man ueber es weiss.
* *Stufe fuer dieses Paar ueberspringen* - ergaebe einen nicht-transitiven
  Vergleich. Eine Sortierung darauf ist nicht wohldefiniert und waere
  ihrerseits reihenfolgeabhaengig: derselbe Fehler in Gruen.

WAS DIESES MODUL NICHT TUT
------------------------------------------------------------------------------
* **Es erfindet keine Signalstaerke.** Wo eine Strategie keine stetige Groesse
  fuehrt, beginnt die Kaskade bei Stufe 2. Eine neue Groesse einzufuehren
  waere eine Strategieaenderung, keine Rangregel.
* **Es aendert keinen Parameter** - weder Allokation noch Positionslimit noch
  Stop. Es entscheidet ausschliesslich die Reihenfolge unter Gleichzeitigen.
* **Es erzeugt und streicht keine Trades.** Welche Signale entstehen, ist
  unveraendert Sache der Strategie; die Menge der erzeugten Trades ist
  dieselbe wie vorher.
* **Es blickt nicht voraus.** Stufe 2 und 3 lesen ausschliesslich Tage, die
  VOR dem Kalendertag des Einstiegs liegen (siehe `fensterende`). Der
  Einstiegstag selbst bleibt aussen vor - bei den Stundenbots waere sein
  Tagesaggregat sonst aus Kerzen gebaut, die zum Einstiegszeitpunkt noch
  nicht existierten.

WAS SICH AM ERGEBNIS AENDERT - UND WAS NICHT
------------------------------------------------------------------------------
Die MENGE der erzeugten Trades ist unveraendert. Veraendert ist, welche davon
Kapital bekommen, wenn es knapp wird - und damit jede Kennzahl, die darauf
beruht. Die heutige Zahl war eine von zwanzig moeglichen; die neue ist eine
bestimmte. Ein Bot, bei dem nie etwas knapp wird (`elliott_wave`: null
abgelehnte Trades), behaelt seine Zahlen.

Ebenfalls festgelegt ist jetzt die Reihenfolge der AUSSTIEGE bei gleichem
Zeitstempel (`ausstiegsreihenfolge`). Sie entscheidet ueber niemandes Platz,
aber ueber die Zwischenstaende der Kapitalkurve und damit ueber den
gemessenen Drawdown. Auch dort galt vorher die Dateireihenfolge; jetzt gilt
derselbe seeded Zufall wie auf Stufe 4 - ein oekonomisches Kriterium gibt es
hier nicht, und eines zu erfinden waere schlimmer als eine offengelegte
Muenze.

REIHENFOLGE-INVARIANZ - DIE OPERATIVE DEFINITION
------------------------------------------------------------------------------
`python3 shared/determinismus.py --voll --perms 20` muss fuer alle neun Bots
`DETERMINISTISCH` melden. Damit das gilt, darf **kein** Zwischenwert von der
Symbolreihenfolge abhaengen. Zwei Stellen verlangen dafuer ausdruecklich
Sorgfalt, beide sind unten kommentiert:

* Die Buchreihe wird ueber die **alphabetisch sortierten** Buchsymbole
  summiert. Gleitkomma-Addition ist nicht assoziativ; ohne feste
  Summationsreihenfolge koennte die letzte Bitstelle einer Korrelation
  kippen und damit einen Gleichstand aufloesen.
* Alle Vergleichswerte werden auf `RUNDUNG` Stellen gerundet, bevor sie
  verglichen werden. Ohne das entschiede Rechenrauschen ueber Gleichstaende.

RECHENAUFWAND
------------------------------------------------------------------------------
Die Korrelation faellt bei jeder umstrittenen Zuteilung an, und zwar nach
jeder Vergabe neu (das Buch hat sich geaendert). Drei Massnahmen halten das
klein; wie gut, steht nach jedem Lauf im Protokoll (`protokoll()`):

1. Die Tagesreihen aller Symbole werden EINMAL je Lauf zu zwei breiten
   Tabellen (Tage x Symbole) verdichtet. Ein Fenster ist danach ein
   Array-Schnitt, kein Neuaufbau.
2. Gerechnet wird nur, wenn ueberhaupt etwas knapp ist. Passen alle
   Kandidaten eines Zeitpunkts ohnehin hinein, ist ihre Reihenfolge fuer das
   Ergebnis bedeutungslos - dann wird die Kaskade gar nicht erst befragt.
3. Zwischenspeicher je (Symbol, Tag) fuer die Liquiditaet. Fuer die
   KORRELATION gibt es bewusst keinen: sie haengt am Buch, und das ist nach
   jeder Vergabe ein anderes - gemessen 27.854 Korrelationen und 0 Treffer
   auf `turtle_soup_stocks`. Ein Speicher haette dort nur Arbeitsspeicher
   gekostet.
"""

import hashlib
import time as _uhr

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Die Stellschrauben der Kaskade. KEIN Handelsparameter steht hier - diese
# Zahlen entscheiden ueber die Rangfolge unter gleichzeitigen Signalen, nicht
# ueber Einstieg, Ausstieg oder Positionsgroesse. Die Handelsparameter stehen
# weiterhin ausschliesslich in live_params.py.
# ---------------------------------------------------------------------------

# Der protokollierte Startwert des Zufalls auf Stufe 4. Derselbe Startwert
# liefert dieselbe Zuteilung; ein anderer eine andere. Genau das ist der
# Punkt: die Willkuer ist sichtbar und benannt, statt in einer Textdatei zu
# stecken. Die Zahl ist das Datum der Messung aus TB-23 - sie hat keine
# inhaltliche Bedeutung und soll auch keine bekommen.
SEED = 20260913

# Stufe 2: Laenge des Korrelationsfensters in HANDELSTAGEN (nicht
# Kalendertagen - gezaehlt werden vorhandene Tagesreihen).
KORRELATIONSFENSTER_TAGE = 60

# Stufe 2: so viele gemeinsame Beobachtungen muss ein Kandidat mit dem Buch
# haben, damit seine Korrelation benutzt wird. Darunter gilt die
# Median-Behandlung oben. 20 statt 60, weil das Mass hier ein Gleichstand-
# Aufloeser ist und keine Renditeprognose - und weil ein Symbol mit 40 Tagen
# Historie mehr Information traegt als gar keine.
MIN_KORRELATIONSTAGE = 20

# Stufe 3: Fenster des Medians des Dollar-Volumens, in Handelstagen.
LIQUIDITAETSFENSTER_TAGE = 20

# Stufe 3: Mindestzahl vorhandener Volumentage. Ein Median aus zwei Werten
# ist keiner.
MIN_LIQUIDITAETSTAGE = 5

# Auf so viele Nachkommastellen werden alle Vergleichswerte gebracht, bevor
# ueber Gleichstand entschieden wird. Weit jenseits jeder inhaltlichen
# Aussage und zugleich robust gegen die letzte Bitstelle - dieselbe
# Begruendung wie fuer RUNDUNG in shared/determinismus_lauf.py.
RUNDUNG = 12

AUFSTEIGEND = "aufsteigend"
ABSTEIGEND = "absteigend"

# Die Namen der Stufen, so wie sie im Protokoll erscheinen.
STUFE_SIGNAL = "signalstaerke"
STUFE_DIVERSIFIKATION = "diversifikation"
STUFE_LIQUIDITAET = "liquiditaet"
STUFE_ZUFALL = "zufall"
STUFEN = (STUFE_SIGNAL, STUFE_DIVERSIFIKATION, STUFE_LIQUIDITAET, STUFE_ZUFALL)


# ---------------------------------------------------------------------------
# Kursdaten: aus dem, was der Bot ohnehin geladen hat
# ---------------------------------------------------------------------------
def kursrahmen(all_data) -> dict:
    """Vereinheitlicht die `load_all_symbol_data()`-Rueckgaben der neun Bots.

    Fuenf Bots liefern `{symbol: df}`, vier `{symbol: (df, entry_cutoff)}`,
    teils mit bereits berechneten Indikatorspalten. Gebraucht werden hier nur
    `open_time`, `close` und `volume`, und die stehen in beiden Faellen im
    ersten Element.

    Bewusst wird NICHT selbst aus `data/` gelesen: das waere eine zweite
    Wahrheit ueber dieselben Kurse. Benutzt wird genau der Datensatz, mit dem
    der Bot auch seine Trades erzeugt hat - einschliesslich der Bereinigung
    durch `shared/kursdaten.entferne_unvollstaendige()`, die dort beim Laden
    bereits gelaufen ist.
    """
    if not all_data:
        return {}
    rahmen = {}
    for symbol, wert in all_data.items():
        df = wert[0] if isinstance(wert, tuple) else wert
        if isinstance(df, pd.DataFrame) and "open_time" in df.columns:
            rahmen[str(symbol)] = df
    return rahmen


class Kursvorrat:
    """Zwei breite Tabellen (Tage x Symbole): Tagesrenditen und Dollar-Volumen.

    Beide werden EINMAL je Lauf gebaut. Intraday-Bots (1h, 4h) werden dabei
    auf Kalendertage verdichtet - Schlusskurs des Tages, Volumen des Tages -,
    weil Stufe 2 und 3 in TAGEN definiert sind. Fuer die Tagesbots ist das
    die Identitaet.

    Das Dollar-Volumen ist `close * volume`. Bei Aktien ist `volume` die
    Stueckzahl, bei den Binance-Paaren die Menge der Basiswaehrung - in
    beiden Faellen ergibt die Multiplikation mit dem Kurs einen Umsatz in der
    Notierungswaehrung, und nur der ist ueber Symbole hinweg vergleichbar
    (Eigenschaft 3: skalenfrei). Die reine Stueckzahl waere es nicht: eine
    Million PEPE ist nicht eine Million BTC.
    """

    def __init__(self, kursdaten):
        self.symbole = []
        self._tage = np.array([], dtype="datetime64[ns]")
        self._renditen = np.zeros((0, 0))
        self._volumen = np.zeros((0, 0))
        self._spalte = {}
        self.bauzeit_s = 0.0
        if kursdaten:
            self._bauen(kursrahmen(kursdaten))

    # -- Aufbau ------------------------------------------------------------
    @staticmethod
    def _tagesreihen(df):
        """(Tagesschlusskurse, Tages-Dollar-Volumen) eines Symbols."""
        tag = pd.to_datetime(df["open_time"]).dt.normalize()
        close = pd.to_numeric(df["close"], errors="coerce")
        schluss = close.groupby(tag).last()
        if "volume" in df.columns:
            menge = pd.to_numeric(df["volume"], errors="coerce")
            umsatz = (close * menge).groupby(tag).sum(min_count=1)
        else:
            umsatz = pd.Series(np.nan, index=schluss.index)
        return schluss, umsatz

    def _bauen(self, rahmen):
        begonnen = _uhr.time()
        schluss_je_symbol = {}
        umsatz_je_symbol = {}
        for symbol in sorted(rahmen):
            df = rahmen[symbol]
            if df is None or len(df) == 0:
                continue
            schluss, umsatz = self._tagesreihen(df)
            if schluss.empty:
                continue
            schluss_je_symbol[symbol] = schluss
            umsatz_je_symbol[symbol] = umsatz

        if not schluss_je_symbol:
            self.bauzeit_s = _uhr.time() - begonnen
            return

        # Sortierte Symbolreihenfolge - damit haengt weder der Spaltenaufbau
        # noch (weiter unten) die Summationsreihenfolge der Buchreihe an der
        # Reihenfolge, in der der Bot die Symbole geladen hat.
        self.symbole = sorted(schluss_je_symbol)
        kurse = pd.DataFrame(schluss_je_symbol).sort_index()
        umsaetze = pd.DataFrame(umsatz_je_symbol).reindex(
            index=kurse.index, columns=self.symbole)
        kurse = kurse[self.symbole]

        self._tage = kurse.index.to_numpy(dtype="datetime64[ns]")
        # fill_method=None ausdruecklich: die Voreinstellung von pandas fuellt
        # Luecken vorwaerts auf und erzeugt damit an jedem fehlenden Tag eine
        # Rendite von exakt 0 %. Das ist keine Beobachtung, sondern eine
        # erfundene - und sie senkt die gemessene Korrelation ausgerechnet bei
        # den Symbolen, ueber die am wenigsten bekannt ist. Eine Luecke bleibt
        # hier eine Luecke und faellt unten aus dem Fenster.
        self._renditen = kurse.pct_change(fill_method=None).to_numpy(dtype=float)
        self._volumen = umsaetze.to_numpy(dtype=float)
        self._spalte = {s: i for i, s in enumerate(self.symbole)}
        self.bauzeit_s = _uhr.time() - begonnen

    def __bool__(self):
        return bool(self.symbole)

    # -- Fenster -----------------------------------------------------------
    def fensterende(self, zeit) -> int:
        """Zahl der Tagesreihen, die STRIKT VOR dem Kalendertag von `zeit`
        liegen.

        Der Einstiegstag selbst bleibt aussen vor. Fuer die Tagesbots ist das
        der uebliche Vorlauf; fuer `elliott_wave` (1h) und `t3_supertrend`
        (4h) ist es die Bedingung dafuer, dass hier kein Blick nach vorn
        entsteht - ihr Tagesaggregat enthielte sonst Kerzen, die zum
        Einstiegszeitpunkt noch nicht geschlossen waren.
        """
        if self._tage.size == 0:
            return 0
        tag = pd.Timestamp(zeit).normalize().to_datetime64()
        return int(np.searchsorted(self._tage, tag, side="left"))

    def buchreihe(self, buch, ende: int):
        """Allokationsgewichtete Tagesrendite des Buches im Fenster vor `ende`.

        `buch` ist eine Liste `(symbol, allokation)`. Gewichtet wird mit der
        Allokation, weil genau sie beschreibt, wie stark eine Position das
        Buch praegt - ein gleichgewichteter Mittelwert waere eine zweite,
        stillere Annahme ueber dasselbe Buch.

        Fehlt fuer einen Tag der Kurs einer Buchposition (juengeres Symbol,
        Handelsruhe), werden die Gewichte an diesem Tag auf die vorhandenen
        Positionen NEU NORMIERT, statt den Tag ganz zu verwerfen. Sonst
        wuerde eine einzige junge Position das Fenster fuer das gesamte Buch
        leeren.
        """
        if ende <= 0 or not buch:
            return None
        anfang = max(0, ende - KORRELATIONSFENSTER_TAGE)
        # Alphabetisch sortiert: feste Summationsreihenfolge (siehe Kopf).
        paare = sorted((s, float(a)) for s, a in buch if s in self._spalte)
        if not paare:
            return None
        spalten = [self._spalte[s] for s, _ in paare]
        gewichte = np.array([a for _, a in paare], dtype=float)
        if gewichte.sum() <= 0:
            gewichte = np.ones_like(gewichte)

        block = self._renditen[anfang:ende, spalten]
        vorhanden = ~np.isnan(block)
        nenner = vorhanden * gewichte
        summe_gewichte = nenner.sum(axis=1)
        zaehler = np.nansum(np.where(vorhanden, block, 0.0) * gewichte, axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            reihe = np.where(summe_gewichte > 0, zaehler / summe_gewichte, np.nan)
        return reihe

    def korrelation(self, symbol: str, buchreihe, ende: int):
        """Korrelation der Tagesrenditen des Kandidaten mit der Buchreihe.

        Rueckgabe `None`, wenn zu wenig gemeinsame Beobachtungen vorliegen
        oder eine der beiden Reihen im Fenster konstant ist (dann ist die
        Korrelation nicht definiert - kein Grund, eine Zahl zu erfinden).
        """
        if buchreihe is None or symbol not in self._spalte or ende <= 0:
            return None
        anfang = max(0, ende - KORRELATIONSFENSTER_TAGE)
        kandidat = self._renditen[anfang:ende, self._spalte[symbol]]
        gueltig = ~np.isnan(kandidat) & ~np.isnan(buchreihe)
        if int(gueltig.sum()) < MIN_KORRELATIONSTAGE:
            return None
        a = kandidat[gueltig]
        b = buchreihe[gueltig]
        if np.std(a) == 0.0 or np.std(b) == 0.0:
            return None
        with np.errstate(invalid="ignore", divide="ignore"):
            wert = float(np.corrcoef(a, b)[0, 1])
        if not np.isfinite(wert):
            return None
        return round(wert, RUNDUNG)

    def liquiditaet(self, symbol: str, ende: int):
        """Median des Dollar-Volumens der letzten `LIQUIDITAETSFENSTER_TAGE`
        Tage vor `ende`. `None`, wenn zu wenige Tage vorliegen."""
        if symbol not in self._spalte or ende <= 0:
            return None
        anfang = max(0, ende - LIQUIDITAETSFENSTER_TAGE)
        werte = self._volumen[anfang:ende, self._spalte[symbol]]
        werte = werte[~np.isnan(werte)]
        if werte.size < MIN_LIQUIDITAETSTAGE:
            return None
        return round(float(np.median(werte)), RUNDUNG)


# ---------------------------------------------------------------------------
# Der seeded Zufall (Stufe 4 - und die Ausstiegsreihenfolge)
# ---------------------------------------------------------------------------
def zufallsschluessel(seed: int, felder) -> str:
    """Ein reproduzierbarer Fingerabdruck aus dem INHALT eines Trades.

    Nicht aus seiner Zeilennummer - die ist genau die Groesse, die hier
    beseitigt wird. Aus dem Inhalt gebildet ist der Schluessel unabhaengig
    davon, an welcher Stelle der Trade im DataFrame steht, und bei gleichem
    Startwert ueber Laeufe hinweg derselbe.

    blake2b statt `hash()`: Pythons eingebautes `hash()` fuer Zeichenketten
    ist prozessweise zufaellig gesalzen (PYTHONHASHSEED) und liefert in zwei
    Laeufen verschiedene Werte. Damit waere die Zuteilung zwischen zwei
    Programmstarts nicht reproduzierbar - der Fehler waere schwerer zu finden
    als der, den dieses Modul behebt.
    """
    roh = "|".join([str(seed)] + [str(f) for f in felder])
    return hashlib.blake2b(roh.encode("utf-8"), digest_size=16).hexdigest()


# ---------------------------------------------------------------------------
# Die Kaskade
# ---------------------------------------------------------------------------
def _median_ersatz(werte: dict):
    """Der Median der vorliegenden Werte - die benannte Behandlung fuer
    fehlende Angaben (siehe Kopfkommentar). `None`, wenn keiner vorliegt;
    dann entfaellt die Stufe."""
    vorhanden = [w for w in werte.values() if w is not None]
    if not vorhanden:
        return None
    return round(float(np.median(vorhanden)), RUNDUNG)


def _beste(gruppe, werte: dict, groesser_ist_besser: bool):
    """Die Kandidaten mit dem besten Wert - oder die ganze Gruppe, wenn die
    Stufe nichts beitragen kann."""
    ersatz = _median_ersatz(werte)
    if ersatz is None:
        return gruppe
    gefuellt = {i: (werte[i] if werte[i] is not None else ersatz) for i in gruppe}
    ziel = max(gefuellt.values()) if groesser_ist_besser else min(gefuellt.values())
    return [i for i in gruppe if gefuellt[i] == ziel]


class Zuteiler:
    """Entscheidet, welcher von mehreren gleichzeitigen Kandidaten den knappen
    Platz bekommt - und protokolliert, welche Stufe es war.

    Ein Zuteiler gehoert zu genau einer Trade-Tabelle; die je Trade festen
    Groessen (Symbol, Signalwert, Zufallsschluessel) werden einmal berechnet.
    """

    def __init__(self, trades: pd.DataFrame, kursdaten=None,
                 signalspalte=None, seed: int = SEED):
        self.seed = int(seed)
        self.signalspalte = None
        self.signalrichtung = None
        self.vorrat = Kursvorrat(kursdaten)

        self._symbol = []
        self._signal = []
        self._zufall = []
        self._korrelationen = 0
        self._buchreihen = 0
        self._treffer = 0
        self._rechenzeit_s = 0.0
        self._entschieden = {stufe: 0 for stufe in STUFEN}
        self._umstrittene = 0
        self._liqspeicher = {}

        if trades is None or len(trades) == 0:
            return

        spalte, richtung = self._signalspalte_pruefen(trades, signalspalte)
        self.signalspalte, self.signalrichtung = spalte, richtung

        self._symbol = trades["symbol"].astype(str).tolist()

        # Der Fingerabdruck wird aus den Spalten gebaut, die einen Trade
        # inhaltlich beschreiben - dieselben, an denen auch
        # shared/determinismus_lauf.py zwei Laeufe vergleicht. Spaltenweise
        # als Text, damit die Schleife ueber 12.000 Trades nicht 12.000
        # pandas-Zeilen baut.
        felder = [s for s in ("symbol", "entry_time", "exit_time", "entry_price",
                              "exit_price", "pnl_pct") if s in trades.columns]
        texte = [trades[s].astype(str).tolist() for s in felder]
        self._zufall = [zufallsschluessel(self.seed, werte)
                        for werte in zip(*texte)] if texte else [
            zufallsschluessel(self.seed, [i]) for i in range(len(trades))]

        if spalte is not None:
            werte = pd.to_numeric(trades[spalte], errors="coerce")
            self._signal = [None if pd.isna(w) else round(float(w), RUNDUNG)
                            for w in werte]

    @staticmethod
    def _signalspalte_pruefen(trades, signalspalte):
        """`SIGNALSPALTE` des Bots aufloesen - und schweigend uebergehen ist
        hier ausdruecklich NICHT vorgesehen.

        Nennt ein Bot eine Spalte, die seine Trade-Tabelle nicht fuehrt, dann
        ist entweder der Name falsch oder die Strategie hat sich geaendert.
        Beides muss auffallen: sonst rutschte der Bot lautlos auf eine
        Kaskade ohne Stufe 1, und die Kennzahlen verschoeben sich ohne
        erkennbaren Anlass.
        """
        if signalspalte is None:
            return None, None
        spalte, richtung = signalspalte
        if richtung not in (AUFSTEIGEND, ABSTEIGEND):
            raise ValueError(
                f"SIGNALSPALTE: unbekannte Richtung {richtung!r} - erwartet "
                f"{AUFSTEIGEND!r} oder {ABSTEIGEND!r}.")
        if spalte not in trades.columns:
            raise KeyError(
                f"SIGNALSPALTE nennt die Spalte {spalte!r}, die Trade-Tabelle "
                f"fuehrt sie nicht (vorhanden: {sorted(trades.columns)}).")
        return spalte, richtung

    # -- Stufe 4 / Ausstiege ----------------------------------------------
    def ausstiegsreihenfolge(self, positionen):
        """Die Reihenfolge, in der Ausstiege mit gleichem Zeitstempel
        abgerechnet werden.

        Sie entscheidet ueber keinen Platz - alle diese Positionen werden
        geschlossen. Sie entscheidet aber ueber die Zwischenstaende der
        Kapitalkurve und damit ueber den gemessenen Drawdown. Vorher stand
        hier die Dateireihenfolge; jetzt derselbe protokollierte Zufall wie
        auf Stufe 4. Ein oekonomisches Kriterium gibt es an dieser Stelle
        nicht, und eines zu erfinden waere die schlechtere Antwort.
        """
        return sorted(positionen, key=lambda p: self._zufall[p])

    # -- Die Entscheidung --------------------------------------------------
    def waehle(self, kandidaten, buch, zeit):
        """Der Gewinner unter `kandidaten` - und die Stufe, die entschied."""
        begonnen = _uhr.time()
        self._umstrittene += 1
        gruppe = list(kandidaten)

        # Stufe 1 - strategieeigene Signalstaerke
        if self.signalspalte is not None and len(gruppe) > 1:
            werte = {i: self._signal[i] for i in gruppe}
            gruppe = _beste(gruppe, werte,
                            groesser_ist_besser=(self.signalrichtung == ABSTEIGEND))
            if len(gruppe) == 1:
                return self._fertig(gruppe[0], STUFE_SIGNAL, begonnen)

        # Stufe 2 - Diversifikationsbeitrag
        if len(gruppe) > 1 and buch and self.vorrat:
            ende = self.vorrat.fensterende(zeit)
            reihe = self.vorrat.buchreihe(buch, ende)
            self._buchreihen += 1
            werte = {i: self._korrelation(self._symbol[i], reihe, ende)
                     for i in gruppe}
            gruppe = _beste(gruppe, werte, groesser_ist_besser=False)
            if len(gruppe) == 1:
                return self._fertig(gruppe[0], STUFE_DIVERSIFIKATION, begonnen)

        # Stufe 3 - Liquiditaet
        if len(gruppe) > 1 and self.vorrat:
            ende = self.vorrat.fensterende(zeit)
            werte = {i: self._liquiditaet(self._symbol[i], ende) for i in gruppe}
            gruppe = _beste(gruppe, werte, groesser_ist_besser=True)
            if len(gruppe) == 1:
                return self._fertig(gruppe[0], STUFE_LIQUIDITAET, begonnen)

        # Stufe 4 - seeded Zufall
        gewinner = min(gruppe, key=lambda i: self._zufall[i])
        return self._fertig(gewinner, STUFE_ZUFALL, begonnen)

    def _fertig(self, gewinner, stufe, begonnen):
        self._entschieden[stufe] += 1
        self._rechenzeit_s += _uhr.time() - begonnen
        return gewinner

    # -- Zwischenspeicher --------------------------------------------------
    # GEMESSEN, nicht vermutet: ein Zwischenspeicher je (Symbol, Buch, Tag)
    # fuer die KORRELATION trifft nie. Der Grund liegt in der Sache: nach
    # jeder Vergabe ist das Buch ein anderes, also ist auch der Schluessel ein
    # anderer. Auf `turtle_soup_stocks` waren es 27.854 Korrelationen und 0
    # Treffer - der Speicher haette nur Arbeitsspeicher gekostet (27.854
    # Schluessel mit je bis zu 51 Buchpositionen) und nichts gespart. Er ist
    # deshalb nicht vorhanden.
    #
    # Was den Aufwand tatsaechlich klein haelt, ist der Speicher eine Ebene
    # tiefer: die Tagesreihen JE SYMBOL werden einmal je Lauf zu zwei breiten
    # Tabellen verdichtet (`Kursvorrat`), danach ist ein 60-Tage-Fenster ein
    # Array-Schnitt. Gemessen 3,1 s Kaskade gegen 2,4 s fuer diesen Aufbau.
    #
    # Die LIQUIDITAET dagegen haengt nur an (Symbol, Tag) und wird bei einem
    # Zeitpunkt mehrfach angefragt - dieser Speicher trifft und bleibt.
    def _korrelation(self, symbol, reihe, ende):
        self._korrelationen += 1
        return self.vorrat.korrelation(symbol, reihe, ende)

    def _liquiditaet(self, symbol, ende):
        schluessel = (symbol, ende)
        if schluessel in self._liqspeicher:
            self._treffer += 1
            return self._liqspeicher[schluessel]
        wert = self.vorrat.liquiditaet(symbol, ende)
        self._liqspeicher[schluessel] = wert
        return wert

    # -- Protokoll ---------------------------------------------------------
    def protokoll(self) -> dict:
        """Was die Kaskade getan hat. Der Startwert steht hier, weil ein
        Zufall, der nirgends aufgeschrieben ist, kein reproduzierbarer ist."""
        return {
            "seed": self.seed,
            "primaerschluessel": (None if self.signalspalte is None else
                                  f"{self.signalspalte} ({self.signalrichtung})"),
            "kursdaten_symbole": len(self.vorrat.symbole),
            "umstrittene_zuteilungen": self._umstrittene,
            "entschieden_durch": dict(self._entschieden),
            "korrelationen_gerechnet": self._korrelationen,
            "buchreihen_gerechnet": self._buchreihen,
            "liquiditaet_speichertreffer": self._treffer,
            "rechenzeit_kaskade_s": round(self._rechenzeit_s, 2),
            "rechenzeit_tagesreihen_s": round(self.vorrat.bauzeit_s, 2),
        }


def protokollzeilen(protokoll: dict) -> list:
    """Das Protokoll als Textblock fuer die Ausgabe der Bots."""
    if not protokoll:
        return []
    e = protokoll.get("entschieden_durch") or {}
    entschieden = ", ".join(f"{stufe} {e.get(stufe, 0)}" for stufe in STUFEN)
    zeilen = [
        "ZUTEILUNG (shared/zuteilung.py)",
        f"  Startwert (Seed):        {protokoll['seed']}",
        f"  Primaerschluessel:       {protokoll['primaerschluessel'] or 'keiner (Kaskade beginnt bei Stufe 2)'}",
        f"  Kursdaten fuer Stufe 2/3: {protokoll['kursdaten_symbole']} Symbole",
        f"  Umstrittene Zuteilungen: {protokoll['umstrittene_zuteilungen']}",
        f"  entschieden durch:       {entschieden}",
        f"  Korrelationen gerechnet: {protokoll['korrelationen_gerechnet']} "
        f"auf {protokoll['buchreihen_gerechnet']} Buchreihen",
        f"  Rechenzeit:              {protokoll['rechenzeit_kaskade_s']:.2f}s Kaskade, "
        f"{protokoll['rechenzeit_tagesreihen_s']:.2f}s Tagesreihen",
    ]
    return zeilen


# ---------------------------------------------------------------------------
# Die Kapitalsimulation - an EINER Stelle fuer alle neun Bots
# ---------------------------------------------------------------------------
def simuliere_portfolio(trades: pd.DataFrame, starting_capital: float,
                        allocation_pct: float,
                        max_concurrent_positions: int = None,
                        kursdaten=None, signalspalte=None,
                        seed: int = SEED) -> dict:
    """Ereignisbasierte Kapitalsimulation mit der Zuteilungskaskade.

    Bis auf die Reihenfolgeentscheidung ist die Rechnung Zeile fuer Zeile
    dieselbe wie zuvor in den neun `equity_simulation.py`:

    * Ausstiege werden bei gleichem Zeitstempel VOR den Einstiegen verbucht
      (das Kapital wird frei, bevor darum konkurriert wird).
    * Ein Einstieg wird abgelehnt, wenn das Positionslimit erreicht ist ODER
      die Allokation das freie Kapital uebersteigt. Beide Ablehnungen landen
      wie bisher in derselben Zaehlung; eine Aufschluesselung gibt die
      Funktion weiterhin nicht zurueck.
    * `allocation = capital * allocation_pct` wird zum Einstiegszeitpunkt
      bestimmt, also auf dem Kapitalstand nach den Ausstiegen desselben
      Zeitpunkts.

    Dass beim ersten abgelehnten Kandidaten eines Zeitpunkts auch alle
    weiteren dieses Zeitpunkts abgelehnt werden, ist keine neue Regel,
    sondern dieselbe: waehrend der Einstiege eines Zeitpunkts aendert sich
    weder `capital` noch die Zahl der offenen Positionen zugunsten eines
    spaeteren Kandidaten - die Pruefung faellt fuer jeden folgenden genauso
    aus.

    `kursdaten` ist die `load_all_symbol_data()`-Rueckgabe des Bots. Fehlt
    sie, ruhen Stufe 2 und 3 der Kaskade; das Ergebnis bleibt reproduzierbar
    (Stufe 1 und 4 genuegen dafuer), verliert aber den oekonomischen Gehalt
    der beiden mittleren Stufen. Das Protokoll weist das mit
    `kursdaten_symbole: 0` aus - eine Zuteilung, die stillschweigend auf
    Zufall zurueckfaellt, waere genau der Fehler, den diese Aufgabe behebt.
    """
    zuteiler = Zuteiler(trades, kursdaten, signalspalte, seed)

    leeres_ergebnis = {
        "final_capital": round(float(starting_capital), 2),
        "num_executed": 0,
        "num_skipped": 0,
        "equity_curve": pd.DataFrame(),
        "zuteilung": zuteiler.protokoll(),
    }
    if trades is None or len(trades) == 0:
        return leeres_ergebnis

    einstieg = pd.to_datetime(trades["entry_time"]).to_numpy()
    ausstieg = pd.to_datetime(trades["exit_time"]).to_numpy()
    symbole = trades["symbol"].astype(str).to_numpy()
    ergebnisse = trades["pnl_pct"].to_numpy()

    einstiege_je_zeit = {}
    ausstiege_je_zeit = {}
    for pos in range(len(trades)):
        einstiege_je_zeit.setdefault(einstieg[pos], []).append(pos)
        ausstiege_je_zeit.setdefault(ausstieg[pos], []).append(pos)

    zeitpunkte = sorted(set(einstiege_je_zeit) | set(ausstiege_je_zeit))

    capital = float(starting_capital)
    open_positions = {}
    num_skipped = 0
    num_executed = 0
    equity_curve = []

    for zeit in zeitpunkte:
        # --- Ausstiege zuerst: das Kapital wird frei -----------------------
        for pos in zuteiler.ausstiegsreihenfolge(ausstiege_je_zeit.get(zeit, ())):
            if pos not in open_positions:
                continue
            allocation = open_positions.pop(pos)
            pnl_pct = ergebnisse[pos]
            result_value = allocation * (1 + pnl_pct / 100)
            capital += (result_value - allocation)
            equity_curve.append({
                "time": zeit, "symbol": symbole[pos], "pnl_pct": pnl_pct,
                "allocation": round(allocation, 2),
                "capital_after": round(capital, 2),
            })

        # --- Einstiege: hier greift die Kaskade ----------------------------
        rest = list(einstiege_je_zeit.get(zeit, ()))
        if not rest:
            continue

        # Wird ueberhaupt etwas knapp? Passen alle Kandidaten dieses
        # Zeitpunkts ohnehin hinein, ist ihre Reihenfolge fuer JEDE Zahl des
        # Ergebnisses bedeutungslos: Einstiege schreiben keine Kurvenzeile,
        # und die gebundene Summe ist von der Reihenfolge unabhaengig. Dann
        # wird die Kaskade nicht befragt - das spart die Korrelationen, ohne
        # das Ergebnis zu aendern.
        #
        # Der Vergleich ist bewusst zu SCHARF angesetzt (Faktor 1 - 1e-9):
        # im Zweifel gilt der Zeitpunkt als umstritten und die Kaskade wird
        # befragt. Das kostet Rechenzeit und aendert nichts; die umgekehrte
        # Unschaerfe wuerde eine Zuteilung in beliebiger Reihenfolge
        # durchgehen lassen.
        if len(rest) > 1:
            allocation = capital * allocation_pct
            gebunden = sum(open_positions.values())
            genug_plaetze = (max_concurrent_positions is None or
                             len(open_positions) + len(rest) <= max_concurrent_positions)
            genug_kapital = (len(rest) * allocation
                             <= (capital - gebunden) * (1.0 - 1e-9))
            umstritten = not (genug_plaetze and genug_kapital)
        else:
            umstritten = False

        if not umstritten:
            rest = zuteiler.ausstiegsreihenfolge(rest)

        while rest:
            if (max_concurrent_positions is not None
                    and len(open_positions) >= max_concurrent_positions):
                num_skipped += len(rest)
                break

            gebunden = sum(open_positions.values())
            free_capital = capital - gebunden
            allocation = capital * allocation_pct
            if allocation > free_capital:
                num_skipped += len(rest)
                break

            gewinner = (rest[0] if not umstritten
                        else zuteiler.waehle(rest, _buch(open_positions, symbole), zeit))
            rest.remove(gewinner)
            open_positions[gewinner] = allocation
            num_executed += 1

    return {
        "final_capital": round(capital, 2),
        "num_executed": num_executed,
        "num_skipped": num_skipped,
        "equity_curve": pd.DataFrame(equity_curve),
        "zuteilung": zuteiler.protokoll(),
    }


def _buch(open_positions: dict, symbole) -> list:
    """Das aktuelle Buch als `(symbol, allokation)` - die Eingabe von Stufe 2."""
    return [(symbole[pos], betrag) for pos, betrag in open_positions.items()]
