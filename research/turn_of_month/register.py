#!/usr/bin/env python3
"""
TB-33 - Die eingefrorenen Festlegungen als Code
==============================================================================
Jede Zahl, die im Bericht auftaucht, steht HIER - genau einmal. Das ist keine
Formsache: das Projekt hat schon einmal eine doppelt gefuehrte Zahl leise
auseinanderlaufen lassen (CLAUDE.md), und ein Nulltest, dessen Schwelle an
zwei Stellen steht, prueft am Ende die falsche.

Aus diesem Modul leitet sich das Pfadkriterium **P2** ab: *jede berichtete
Kennzahl ist aus dem Register ableitbar*. Der Selbsttest gleicht den Bericht
maschinell gegen `HERKUNFT_JE_KENNZAHL` ab; eine Zahl, die dort keinen
Eintrag hat, laesst ihn durchfallen.

DIE BEIDEN REGISTERDATEIEN
------------------------------------------------------------------------------
  docs/VORREGISTRIERUNG_S-E1_strategiekriterien.md   was gerechnet wird
  docs/VORREGISTRIERUNG_S-E1_pfadkriterien.md        was ein sauberer Weg ist

Sie bauen auf docs/VORREGISTRIERUNG_S-E1_nulltest.md (TB-30a) auf. Aendert
sich eine von ihnen, aendert sich der Register-Hash in `herkunft.py` - und
das Protokoll zeigt, dass zwei Laeufe NICHT unter derselben Vorregistrierung
liefen.
"""

import os

_HIER = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.environ.get("TB33_BASE_DIR") or os.path.dirname(
    os.path.dirname(_HIER))

# ---------------------------------------------------------------------------
# Instrument und Daten
# ---------------------------------------------------------------------------
KERNINSTRUMENT = "SPY"
SWEEP_INSTRUMENTE = ["QQQ", "IWM", "EFA"]

# Eigener Datenordner, NICHT data/: TB-31 aendert dort parallel die
# Krypto-Kursdateien. Beruehrungspunkte vermeiden heisst hier: getrennt
# ablegen, nicht vorsichtig sein.
DATEN_DIR = os.path.join(_HIER, "daten")
ERGEBNIS_DIR = os.path.join(_HIER, "ergebnisse")

# ---------------------------------------------------------------------------
# Das Kernfenster und die Sweep-Zellen
# ---------------------------------------------------------------------------
# (vor, nach): "vor" ist die Zahl der Handelstage BIS zum Monatsende
# einschliesslich des letzten (-1 => nur der letzte), "nach" die Zahl der
# ersten Handelstage des Folgemonats.
KERNFENSTER = (-1, 3)

# Ausdruecklich Robustheit, NICHT Auswahl. Siehe SWEEP_REGEL.
SWEEP_FENSTER = [(-2, 3), (-1, 2), (-1, 4)]

SWEEP_REGEL = (
    "Faellt das Kernfenster (-1/+3 auf SPY) durch und besteht eine "
    "Sweep-Variante, wird die Variante NICHT uebernommen. Das Ergebnis "
    "lautet dann DURCHGEFALLEN. Sonst sind es acht Versuche und nicht "
    "einer, und die Ausnahme von 'Kandidaten nach Rang 3' waere keine mehr."
)

# ---------------------------------------------------------------------------
# Kosten
# ---------------------------------------------------------------------------
# Dieselbe Konvention wie ueberall: TRADING_FEE_PCT 0,1 + SLIPPAGE_PCT 0,05
# je Order, Ein- und Ausstieg. GENAU EIN Round-Trip je Ereignis.
KOSTEN_JE_ROUNDTRIP_PCT = 0.30
RUNDEN_JE_JAHR = 12
KOSTENSCHRANKE_PCT_PA = KOSTEN_JE_ROUNDTRIP_PCT * RUNDEN_JE_JAHR   # 3,6

# ---------------------------------------------------------------------------
# Falten
# ---------------------------------------------------------------------------
SELEKTIONSFALTEN_BIS = 2025          # Kalenderjahre bis einschliesslich
BESTAETIGUNG_VON = "2026-01-01"
BESTAETIGUNG_BIS = "2026-09-01"      # Go-Live-Schnitt

# ---------------------------------------------------------------------------
# Test 1 - Bootstrap
# ---------------------------------------------------------------------------
BOOTSTRAP_ZIEHUNGEN = 10_000
BOOTSTRAP_SEED = 20260915
BOOTSTRAP_NIVEAU = 0.95
MINDEST_EREIGNISSE = 120             # zehn Jahre Monatswechsel

# ---------------------------------------------------------------------------
# Test 2 - die Platzhalter-Verteilung (Beta-Bereinigung)
# ---------------------------------------------------------------------------
PLATZHALTER_ZIEHUNGEN = 10_000
PLATZHALTER_SEED = 20260915
PERZENTIL_SCHWELLE = 95

# ---------------------------------------------------------------------------
# Die drei bindenden Bedingungen
# ---------------------------------------------------------------------------
BEDINGUNGEN = {
    "B1": "Falten-Median der Netto-Rendite des Kernfensters > 0",
    "B2": "untere Grenze des 95-%-Bootstrap-Intervalls des "
          "Ereignis-Mittelwerts > 0",
    "B3": f"Perzentil in Test 2 > {PERZENTIL_SCHWELLE}",
}

# Die drei Urteile. "nicht auswertbar" ist KEIN "durchgefallen": zu wenig
# Daten ist kein Befund ueber den Effekt.
URTEIL_BESTANDEN = "BESTANDEN"
URTEIL_DURCHGEFALLEN = "DURCHGEFALLEN"
URTEIL_NICHT_AUSWERTBAR = "NICHT AUSWERTBAR"

# ---------------------------------------------------------------------------
# Handelstags-Regel - vor dem Lauf, nicht wenn sie gebraucht wird
# ---------------------------------------------------------------------------
HANDELSTAGSREGEL = [
    "Ein Handelstag ist ein Tag, an dem die Kursdatei des Instruments eine "
    "VOLLSTAENDIGE Kerze traegt (shared/kursdaten). Kein zweiter Kalender.",
    "Feiertage stehen damit gar nicht erst in der Reihe; das Fenster "
    "verschiebt sich von selbst. Kein Sonderfall.",
    "Verkuerzte Handelstage sind VOLLE Handelstage und zaehlen als einer: "
    "die Strategie handelt zum Schluss, und ein verkuerzter Tag hat einen "
    "Schluss.",
    "'-1' ist der letzte Handelstag des Kalendermonats, '+k' der k-te "
    "Handelstag des Folgemonats.",
    "Die Einstiegsrendite des Tages -1 misst gegen den Schluss des "
    "DAVORLIEGENDEN Handelstags; ein Ereignis braucht diesen Tag ebenfalls.",
    "Unvollstaendige Ereignisse werden gestrichen UND gezaehlt. Die Zahl "
    "steht in der Ergebnisdatei.",
    "Ein Ereignis gehoert zu der Falte, in der sein EINSTIEGSTAG liegt "
    "(Tag -1). Siehe EREIGNIS_ZUORDNUNG.",
]

# Nachgetragen beim Schreiben des Auswertungsskripts, VOR jeder Rechnung -
# siehe Abweichung A4 in den Strategiekriterien. Ein Ereignis um den
# Jahreswechsel liegt in zwei Kalenderjahren; ohne diese Festlegung haette
# das Skript an genau einer Stelle eine Wahl gehabt, und der Nulltest waere
# an sich selbst gescheitert.
EREIGNIS_ZUORDNUNG = (
    "Ein Ereignis gehoert zu dem Kalenderjahr, in dem sein EINSTIEGSTAG "
    "(Tag -1) liegt. Der Wechsel Dezember->Januar faellt damit in das alte "
    "Jahr. Das ist die konservative Richtung: sie schiebt keine Beobachtung "
    "in die Bestaetigungsperiode hinein, die dort nicht anfaengt."
)

# ---------------------------------------------------------------------------
# Staging-Ebene - Frist und Kriterium, beim Anlegen
# ---------------------------------------------------------------------------
STAGING_FRIST_EREIGNISSE = 12
STAGING_FRIST_DATUM = "2027-09-30"
STAGING_KRITERIEN = {
    "S1": "Rang 3 hat ueber die neun Bots entschieden.",
    "S2": "Der Backtest hat bestanden (B1, B2, B3).",
    "S3": f"Die Forward-Periode hat mindestens {STAGING_FRIST_EREIGNISSE} "
          f"Ereignisse, und die untere Grenze ihres 95-%-Bootstrap-"
          f"Intervalls der Netto-Rendite je Ereignis liegt > 0.",
}

# ---------------------------------------------------------------------------
# N-Buchfuehrung
# ---------------------------------------------------------------------------
N_VERSUCHSREGISTER = 1
N_DSR = 0
N_BEGRUENDUNG = (
    "Zum Versuchsregister zaehlt dieser Lauf als EIN Eintrag: ein Versuch "
    "ohne Wahl ist trotzdem ein Versuch. Zur DSR zaehlt er nicht: "
    "Multiplizitaet entsteht, wo unter Alternativen gewaehlt wird, und dort "
    "ist N = 1. Die Sweep-Zellen zaehlen in keines von beiden, solange die "
    "SWEEP_REGEL gilt."
)

# ---------------------------------------------------------------------------
# P2 - woher jede berichtete Kennzahl stammt
# ---------------------------------------------------------------------------
# Der Selbsttest gleicht die Schluessel der Ergebnisdatei gegen diese Tabelle
# ab. Eine Kennzahl ohne Eintrag hier ist eine Zahl ohne Register - und genau
# das soll P2 verhindern.
HERKUNFT_JE_KENNZAHL = {
    "instrument": "register.KERNINSTRUMENT",
    "fenster": "register.KERNFENSTER",
    "n_ereignisse": "Handelstags-Regel, register.HANDELSTAGSREGEL",
    "n_ereignisse_entfallen": "Handelstags-Regel Punkt 6 (streichen UND zaehlen)",
    "n_kerzen_gestrichen": "shared/kursdaten.entferne_unvollstaendige",
    "mittlere_netto_rendite_pct": "register.KOSTEN_JE_ROUNDTRIP_PCT",
    "bootstrap_unten_pct": "register.BOOTSTRAP_* (Ziehungen, Seed, Niveau)",
    "bootstrap_oben_pct": "register.BOOTSTRAP_* (Ziehungen, Seed, Niveau)",
    "falten_median_pct": "register.SELEKTIONSFALTEN_BIS und "
                         "register.EREIGNIS_ZUORDNUNG",
    "perzentil": "register.PLATZHALTER_* (Ziehungen, Seed)",
    "b1": "register.BEDINGUNGEN['B1']",
    "b2": "register.BEDINGUNGEN['B2']",
    "b3": "register.BEDINGUNGEN['B3']",
    "urteil": "register.URTEIL_* und register.SWEEP_REGEL",
}


def als_text() -> str:
    """Die Festlegungen zum Mitlesen - dieselbe Quelle wie die Rechnung."""
    z = []
    z.append(f"Kerninstrument            {KERNINSTRUMENT}")
    z.append(f"Kernfenster               {KERNFENSTER[0]:+d} bis "
             f"{KERNFENSTER[1]:+d} Handelstage")
    z.append(f"Sweep-Fenster             "
             f"{', '.join(f'{a:+d}/{b:+d}' for a, b in SWEEP_FENSTER)}")
    z.append(f"Sweep-Instrumente         {', '.join(SWEEP_INSTRUMENTE)}")
    z.append(f"Kosten je Round-Trip      {KOSTEN_JE_ROUNDTRIP_PCT:.2f} "
             f"Prozentpunkte  (= {KOSTENSCHRANKE_PCT_PA:.1f} p.a.)")
    z.append(f"Bootstrap                 {BOOTSTRAP_ZIEHUNGEN} Ziehungen, "
             f"Seed {BOOTSTRAP_SEED}, Niveau {BOOTSTRAP_NIVEAU:.2f}")
    z.append(f"Platzhalter (Test 2)      {PLATZHALTER_ZIEHUNGEN} Ziehungen, "
             f"Seed {PLATZHALTER_SEED}, Schwelle {PERZENTIL_SCHWELLE}. Pz.")
    z.append(f"Mindest-Ereigniszahl      {MINDEST_EREIGNISSE}")
    z.append(f"Selektionsfalten          Kalenderjahre bis "
             f"{SELEKTIONSFALTEN_BIS}")
    z.append(f"Bestaetigungsperiode      {BESTAETIGUNG_VON} bis "
             f"{BESTAETIGUNG_BIS}")
    for k, v in BEDINGUNGEN.items():
        z.append(f"  {k}                      {v}")
    return "\n".join(z)


if __name__ == "__main__":
    print(__doc__.strip().split("\n")[0])
    print()
    print(als_text())
    print()
    print("Sweep-Regel:")
    print(f"  {SWEEP_REGEL}")
    print()
    print("Handelstags-Regel:")
    for i, s in enumerate(HANDELSTAGSREGEL, 1):
        print(f"  {i}. {s}")
