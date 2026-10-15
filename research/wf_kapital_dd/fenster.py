"""
TB-162 - Fenster des bot-eigenen Walk-Forward, ohne Rastersuche (reine Funktionen)
==============================================================================
Register R94 (b) (Fable 14.10.a): zulaessig vor dem Tag ist E und M der
heutigen Parameter, auch in den Fenstern des bot-eigenen Walk-Forward. Die
Fenster kommen aus `split_all_symbols` des Bots (importiert vom Aufrufer,
`__main__` des Bots laeuft nie; R88 (e), R95 (a)). Hier steht nur, wie aus
dessen Rueckgabe die Grenze je Symbol gelesen wird und wie daraus die drei
Abschnitte EINES durchgehenden Kapitalpfads werden (R36: Ausschnitt, kein
Neustart des Kapitals; Entscheid F2 TB-162):

  IS        vom Pfadbeginn bis zur fruehesten Symbolgrenze
  gemischt  von der fruehesten bis zur spaetesten Symbolgrenze
  OOS       ab der spaetesten Symbolgrenze bis zum Pfadende
  gesamt    der ganze Pfad

Zwei Bauarten der Rueckgabe (gelesen, nicht nachgebaut):
  zeitbasiert   train[s] = (kurse, start|None, split_time), test[s] = (kurse, split_time, None)
  zeilenbasiert train[s] = kurse.iloc[:k], test[s] = kurse.iloc[k:]  -> Grenze = open_time der Zeile k
Kein Raster, kein Score, keine Auswahl: diese Datei rechnet keine Kennzahl.
"""
import pandas as pd

ABSCHNITTE = ("gesamt", "IS", "gemischt", "OOS")


def _ts(x):
    t = pd.Timestamp(x)
    return t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t


def grenze_je_symbol(train: dict, test: dict) -> dict:
    """Grenze je Symbol aus der Rueckgabe von split_all_symbols; None, wenn das Symbol keinen OOS-Teil hat."""
    aus = {}
    for s in sorted(set(train) | set(test)):
        tr, te = train.get(s), test.get(s)
        if isinstance(tr, tuple) or isinstance(te, tuple):
            g_tr = tr[2] if isinstance(tr, tuple) and len(tr) == 3 else None
            g_te = te[1] if isinstance(te, tuple) and len(te) == 3 else None
            if tr is not None and not isinstance(tr, tuple) or te is not None and not isinstance(te, tuple):
                raise ValueError("%s: gemischte Bauart der Rueckgabe" % s)
            if g_tr is not None and g_te is not None and _ts(g_tr) != _ts(g_te):
                raise ValueError("%s: Grenze IS %s ungleich Grenze OOS %s" % (s, g_tr, g_te))
            g = g_te if g_te is not None else g_tr
        elif isinstance(te, pd.DataFrame):
            g = te["open_time"].iloc[0] if len(te) else None
        else:
            raise ValueError("%s: unbekannte Bauart %s" % (s, type(te).__name__))
        aus[s] = None if g is None else _ts(g)
    return aus


def streuung(grenzen: dict) -> dict:
    g = sorted(v for v in grenzen.values() if v is not None)
    if not g:
        raise ValueError("kein Symbol mit Grenze")
    return {"symbole": len(grenzen), "symbole_ohne_grenze": sorted(k for k, v in grenzen.items() if v is None),
            "frueheste": str(g[0]), "spaeteste": str(g[-1]), "median": str(pd.Series(g).median()),
            "spannweite_tage": round((g[-1] - g[0]).total_seconds() / 86400.0, 2)}


def abschnitte(grenzen: dict, von, bis) -> list:
    """Die vier Ausschnitte des einen Pfads [von, bis) in der Form von messe_falten (mtm_kern)."""
    st = streuung(grenzen)
    von, bis = _ts(von), _ts(bis)
    frueh, spaet = pd.Timestamp(st["frueheste"]), pd.Timestamp(st["spaeteste"])
    if not (von <= frueh <= spaet <= bis):
        raise ValueError("Grenzen %s..%s liegen nicht im Pfad %s..%s" % (frueh, spaet, von, bis))
    return [{"name": "gesamt", "rolle": "durchgehender Pfad", "von": von, "bis_ausschliesslich": bis},
            {"name": "IS", "rolle": "bis zur fruehesten Symbolgrenze", "von": von, "bis_ausschliesslich": frueh},
            {"name": "gemischt", "rolle": "zwischen fruehester und spaetester Symbolgrenze", "von": frueh, "bis_ausschliesslich": spaet},
            {"name": "OOS", "rolle": "ab der spaetesten Symbolgrenze", "von": spaet, "bis_ausschliesslich": bis}]
