"""
Zentrale Symbol-Konfiguration
================================
Liest die Top-25-Liste aus top25_symbols.txt (erzeugt durch
get_top_symbols.py). Faellt auf eine kleine Standardliste zurueck,
falls die Datei noch nicht existiert, damit bestehende Skripte nicht
sofort abstuerzen.

Alle anderen Skripte (fetch_multi_data.py, multi_symbol_optimise.py,
forward_test.py) importieren SYMBOLS von hier, statt eine eigene
Liste zu pflegen - so bleibt ueberall dieselbe Coin-Auswahl aktiv.
"""

import os
import sys

from paths import CONFIG_DIR, RUECKGABEWERT_STARTPRUEFUNG, selektionsmodus

SYMBOLS_FILE = os.path.join(CONFIG_DIR, "top25_symbols.txt")
DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]

# Symbole, die zwar durchs Volumen-Ranking rutschen, aber kein "echter"
# Krypto-Coin sind (z.B. an einen realen Rohstoff gekoppelte Token)
EXCLUDE_SYMBOLS = {"XAUTUSDT", "PAXGUSDT"}  # Gold-Tracking-Token


def load_symbols() -> list:
    if os.path.exists(SYMBOLS_FILE):
        with open(SYMBOLS_FILE) as f:
            symbols = [line.strip() for line in f if line.strip()]
        symbols = [s for s in symbols if s not in EXCLUDE_SYMBOLS]
        if symbols:
            return symbols
    # TB-105 Block D (Fable 24b A2): unter dem Selektionsmodus gibt es keinen
    # Rueckfall auf DEFAULT_SYMBOLS - weder bei fehlender Datei noch bei einer
    # Liste, die nach EXCLUDE_SYMBOLS leer ist. Die Meldung sagt, welcher Fall
    # vorliegt. Ohne Modus bleibt alles wie bisher, auch die Meldung
    # "nicht gefunden", die im Fall "leer nach Ausschluss" nicht stimmt
    # (TB-103 A3; nur gemessen, nicht geaendert).
    if selektionsmodus() is not None:
        if os.path.exists(SYMBOLS_FILE):
            grund = ("enthaelt nach dem Ausschluss von %s kein Symbol"
                     % ", ".join(sorted(EXCLUDE_SYMBOLS)))
        else:
            grund = "fehlt"
        sys.stderr.write(
            "[symbols_config] %s %s. Unter dem Selektionsmodus gibt es keinen "
            "Rueckfall auf die Standardliste (Fable 24b A2) - Abbruch mit "
            "Rueckgabewert %d.\n"
            % (SYMBOLS_FILE, grund, RUECKGABEWERT_STARTPRUEFUNG))
        raise SystemExit(RUECKGABEWERT_STARTPRUEFUNG)
    print(f"Warnung: {SYMBOLS_FILE} nicht gefunden. Nutze Standardliste (5 Symbole).")
    print("Fuer die volle Liste erst 'python3 get_top_symbols.py' ausfuehren.\n")
    return DEFAULT_SYMBOLS


SYMBOLS = load_symbols()
