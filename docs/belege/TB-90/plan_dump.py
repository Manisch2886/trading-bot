#!/usr/bin/env python3
"""TB-90 Block A - den Plan im Speicher rechnen und als JSON ausgeben.

Ruft NUR faltenplan.faltenplan() auf, nie main(); schreibt nichts nach
ergebnisse/. Ausgabe: das Plan-Dict als sortiertes JSON nach argv[1].
"""
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "research", "vorregistrierung"))

import faltenplan as fp  # noqa: E402

plan = fp.faltenplan()
with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump(plan, f, indent=1, sort_keys=True, ensure_ascii=False)
    f.write("\n")
for bot, p in plan.items():
    print(bot, p["faltenlaenge_jahre"], p["selektionsfalten"], p["bestaetigungsperiode"])
