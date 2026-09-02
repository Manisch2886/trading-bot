"""
Top-25-Symbole ermitteln
============================
Fragt alle USDT-Handelspaare auf Binance ab, filtert Stablecoins und
gehebelte Token (UP/DOWN, BULL/BEAR) heraus und rankt den Rest nach
24h-Handelsvolumen. Die Top 25 werden in top25_symbols.txt
gespeichert, damit alle anderen Skripte dieselbe Liste nutzen.
"""

import os
from binance.client import Client

from paths import CONFIG_DIR

client = Client()

TOP_N = 25
OUTPUT_FILE = os.path.join(CONFIG_DIR, "top25_symbols.txt")

# Bekannte Stablecoins - gegen diese wollen wir nicht "traden" (kaum Bewegung)
STABLECOINS = {
    "USDC", "BUSD", "TUSD", "DAI", "FDUSD", "USDP", "EUR", "GBP",
    "AEUR", "USTC", "USDD", "USD1", "PYUSD", "GUSD", "USDE", "FRAX",
    "LUSD", "SUSD", "USDX", "EURI", "XUSD",
}


def is_likely_stablecoin(base_asset: str) -> bool:
    """Zusaetzlich zur festen Liste: Symbole, die wie ein Dollar-Pendant
    benannt sind (Muster 'USD...' oder '...USD'), robust abfangen."""
    upper = base_asset.upper()
    return upper.startswith("USD") or upper.endswith("USD")


def is_valid_symbol(symbol_info: dict) -> bool:
    symbol = symbol_info["symbol"]
    base = symbol_info["baseAsset"]

    if not symbol.endswith("USDT"):
        return False
    if symbol_info["status"] != "TRADING":
        return False
    if base in STABLECOINS:
        return False
    if is_likely_stablecoin(base):
        return False
    if any(tag in base for tag in ["UP", "DOWN", "BULL", "BEAR"]):
        return False  # gehebelte Token, keine "echten" Coins

    return True


if __name__ == "__main__":
    print("Lade Symbol-Liste von Binance...")
    exchange_info = client.get_exchange_info()
    valid_symbols = [s["symbol"] for s in exchange_info["symbols"] if is_valid_symbol(s)]
    print(f"{len(valid_symbols)} gueltige USDT-Paare gefunden.\n")

    print("Lade 24h-Handelsvolumen fuer Ranking...")
    tickers = client.get_ticker()  # 24h-Statistik fuer ALLE Symbole in einem Call
    volume_by_symbol = {t["symbol"]: float(t["quoteVolume"]) for t in tickers}

    ranked = sorted(
        valid_symbols,
        key=lambda s: volume_by_symbol.get(s, 0),
        reverse=True,
    )

    top_symbols = ranked[:TOP_N]

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(top_symbols))

    print(f"Top {TOP_N} Symbole nach 24h-Volumen gespeichert in {OUTPUT_FILE}\n")
    print("Top 10 zur Kontrolle:")
    for i, s in enumerate(top_symbols[:10], 1):
        print(f"  {i}. {s}  (Volumen: {volume_by_symbol.get(s, 0):,.0f} USDT)")
