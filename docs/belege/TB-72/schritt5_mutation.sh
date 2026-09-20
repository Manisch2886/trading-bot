#!/bin/bash
# TB-72 Nachweis 7: Mutation am ECHTEN faltenplan.py - die Ableitung durch die
# 4a-Nachrechnung ersetzen -, Test laufen lassen, Mutation zuruecknehmen.
cd "$(dirname "$0")/../../.."
F=research/vorregistrierung/faltenplan.py
ALT='    jahr, messung = eft.erste_falte_nach_3b(bot, kandidaten)'
NEU='    jahr, messung = erste_4a, []  # MUTATION Nachweis 7: 4a allein, ohne Trockenlauf'
echo "== Mutation: in $F"
echo "   alt: $ALT"
echo "   neu: $NEU"
trading-env/bin/python3 - "$F" "$ALT" "$NEU" <<'PY'
import sys; p, alt, neu = sys.argv[1:4]
s = open(p, encoding="utf-8").read(); assert s.count(alt + "\n") == 1
open(p, "w", encoding="utf-8").write(s.replace(alt + "\n", neu + "\n", 1))
PY
echo "== git diff --numstat nach der Mutation:"; git diff --numstat -- "$F"
echo "== Testlauf mit Mutation:"
trading-env/bin/python3 research/faltenplan_neun/test_erste_falte_trockenlauf.py; echo "rc=$?"
echo "== Mutation zurueckgenommen (git checkout):"
git checkout -- "$F"; git diff --numstat -- "$F"; echo "numstat leer = zurueckgenommen"; grep -c "MUTATION" "$F"
