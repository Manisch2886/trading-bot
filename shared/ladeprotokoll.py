"""
Ein Lauf, der ein Symbol auslaesst, sagt es. Immer. (TB-42, Teil 1)
==============================================================================
Dieses Modul haelt die MELDUNGEN des Ladevorgangs an einer Stelle - je
ausgelassenem Symbol eine Zeile mit dem Grund, am Ende eine Summenzeile.

    from ladeprotokoll import Ladeprotokoll

    def load_all_symbol_data() -> dict:
        data = {}
        _prot = Ladeprotokoll(SYMBOLS)
        for symbol in SYMBOLS:
            ...
            except FileNotFoundError:
                _prot.fehlt(symbol, csv_path);            continue
            if df.empty:
                _prot.leer(symbol, csv_path);             continue
            if tage < MIN_HISTORY_DAYS:
                _prot.zu_kurz(symbol, tage, MIN_HISTORY_DAYS); continue
            data[symbol] = df
        _prot.melde(data)
        return data

DER ANLASS (TB-40, gemessen)
------------------------------------------------------------------------------
`rsi2_mean_reversion`, `turtle_soup_stocks` und `volatility_breakout` haben
**keine einzige Zeile** geschrieben, wenn sie ein Symbol wegen zu kurzer
Historie oder fehlender Kursdatei ausgelassen haben - drei von 150 Aktien
fielen bei jedem Lauf lautlos weg. Und bei **acht von neun** Bots war eine
LEERE Kursdatei ein stiller Ausfall (`if df.empty: continue`).

Der Befund, der den ganzen Trockenlauf ausgeloest hat, war nur deshalb
sichtbar, weil `rsi2_crypto` ihn meldet. Bei den anderen dreien waere
dieselbe Sache unbemerkt geblieben - auch im laufenden Betrieb. Eine Luecke
sieht in den Zahlen genauso aus wie "kein Signal".

WARUM EIN GEMEINSAMER BAUSTEIN UND NICHT NEUN EINZELMELDUNGEN
------------------------------------------------------------------------------
Weil der Wortlaut sonst neunmal dasteht - und genau das ist in diesem Projekt
schon einmal auseinandergelaufen (doppelt gefuehrte Zahlen, siehe CLAUDE.md).
Sechs der neun Loader melden die zu kurze Historie heute schon, und zwar
zeichengleich; zwei Gruende meldet keiner einheitlich. Der Baustein macht aus
"neun Stellen, an denen es wieder auseinanderlaeuft" eine.

Der Eingriff je Loader bleibt dabei klein und betrifft **nur das Melden**: die
Ladefunktion selbst - welche Datei gelesen, welche Schranke geprueft, welches
Symbol aufgenommen wird - wird nicht angefasst und wandert nicht hierher. Das
Vorbild ist `shared/kursdaten.Zaehler`, der in denselben neun Loadern genau so
steht.

WAS DIESER BAUSTEIN NICHT TUT
------------------------------------------------------------------------------
Er entscheidet nichts. Er laedt nichts, er schliesst nichts aus, er bricht
nichts ab. **Melden, nicht stoppen** - der Live-Betrieb wird nie blockiert.
Deshalb ist TB-42 ein Bug-Fix und kein Amendment: die geladene Symbolliste ist
vor und nach der Aenderung identisch (nachgewiesen in
`shared/test_ladeprotokoll.py`).

DAS ZEILENFORMAT - GEPRUEFT, NICHT ANGENOMMEN
------------------------------------------------------------------------------
Die Aufgabe nennt `rsi2_crypto` als Massstab, "sofern es taugt". Geprueft:

* Die **Form** taugt und bleibt deshalb zeichengleich erhalten:
  `Hinweis: <SYMBOL> <Grund>, wird uebersprungen.`
  Genau diese Zeile steht heute in sechs Loadern, und
  `research/drawdown_reihenfolge/TESTAUFTRAG.md` nennt sie dem Betreiber als
  erwartete Ausgabe. Sie zu veraendern haette einen Nutzen von null und
  wuerde eine lebende Anleitung falsch machen.
* Zwei ihrer vier Auspraegungen taugen **nicht** und werden angeglichen:
  - die fehlende Datei meldete `Warnung: <PFAD> nicht gefunden` - anderer
    Rang ("Warnung" statt "Hinweis") und, schwerer wiegend, sie nennt den
    **Pfad statt des Symbols**. Wer wissen will, welche Symbole ein Lauf
    ausgelassen hat, braucht damit zwei verschiedene Leseregeln.
  - die leere Datei meldete gar nichts.
* Eine **Summenzeile** gab es nirgends. Sie ist der eigentliche Gewinn: sie
  steht auch dann da, wenn nichts ausgelassen wurde, und beantwortet die
  Frage "hat dieser Lauf ueberhaupt vollstaendig geladen?" ohne Zaehlen.
"""


class Ladeprotokoll:
    """Sammelt die ausgelassenen Symbole eines Ladevorgangs und meldet sie.

    `universum` ist die Symbolliste, die der Loader durchgeht - nicht die
    Zahl, sondern die Liste: nur so kann `melde()` am Ende auffallen lassen,
    dass ein Symbol weder geladen noch ausgelassen wurde.
    """

    def __init__(self, universum):
        self.universum = list(universum)
        # Reihenfolge = Reihenfolge des Auslassens. Kein Set: dieselbe
        # Meldung zweimal waere selbst ein Befund und soll sichtbar bleiben.
        self.ausgelassen = []

    # -- die vier Gruende ---------------------------------------------------
    # Jeder Grund steht hier genau einmal. Die kurze Bezeichnung (zweites
    # Feld) ist die, die in der Summenzeile gezaehlt wird.

    def fehlt(self, symbol, pfad):
        """Es gibt keine Kursdatei fuer dieses Symbol."""
        return self._aus(symbol, "Kursdatei fehlt",
                         f"hat keine Kursdatei ({pfad})")

    def leer(self, symbol, pfad):
        """Die Kursdatei ist da, enthaelt aber keine Kerze."""
        return self._aus(symbol, "Kursdatei leer",
                         f"hat eine leere Kursdatei ({pfad})")

    def zu_kurz(self, symbol, tage, mindest):
        """Die Historie deckt zu wenige Tage ab."""
        return self._aus(symbol, "Historie zu kurz",
                         f"deckt nur {tage} Tage ab (< {mindest} noetig)")

    def zu_wenige_kerzen(self, symbol, kerzen, mindest):
        """Die Historie hat zu wenige Kerzen (Bots mit Kerzenzahl-Schranke)."""
        return self._aus(symbol, "Kerzenzahl zu klein",
                         f"hat nur {kerzen} Kerzen (< {mindest} noetig)")

    # -- Innenleben ---------------------------------------------------------
    def _aus(self, symbol, kurz, grund):
        self.ausgelassen.append((symbol, kurz))
        zeile = f"Hinweis: {symbol} {grund}, wird uebersprungen."
        print(zeile)
        return zeile

    def summenzeile(self, geladen):
        """Die Summenzeile als Text. `geladen` ist das Ergebnis des Loaders
        (dict oder Zahl) - der Loader muss nichts zusaetzlich mitzaehlen."""
        n_geladen = geladen if isinstance(geladen, int) else len(geladen)
        n_gesamt = len(self.universum)
        text = f"Geladen: {n_geladen} von {n_gesamt} Symbolen."

        if self.ausgelassen:
            zaehlung = {}
            for _symbol, kurz in self.ausgelassen:
                zaehlung[kurz] = zaehlung.get(kurz, 0) + 1
            teile = ", ".join(f"{n}x {kurz}" for kurz, n in sorted(zaehlung.items()))
            text += f" {len(self.ausgelassen)} ausgelassen: {teile}."
        else:
            text += " Keines ausgelassen."

        # Der Wachposten: geladen + ausgelassen muss das Universum ergeben.
        # Schlaegt er an, hat der Loader ein Symbol fallen lassen, ohne einen
        # Grund zu nennen - also genau der Fehler, gegen den TB-42 gebaut ist,
        # nur an einer Stelle, die es hier noch nicht gibt. Die Zeile nennt
        # ihn, statt ihn wieder still werden zu lassen.
        rest = n_gesamt - n_geladen - len(self.ausgelassen)
        if rest:
            text += (f" ACHTUNG: {rest} Symbol(e) sind weder geladen noch mit "
                     f"Grund ausgelassen - hier faellt etwas ohne Meldung weg.")
        return text

    def melde(self, geladen):
        """Druckt die Summenzeile. Gibt sie ausserdem zurueck, damit ein Test
        sie pruefen kann, ohne stdout abzufangen."""
        text = self.summenzeile(geladen)
        print(text)
        return text
