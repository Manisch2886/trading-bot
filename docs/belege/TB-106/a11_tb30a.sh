#!/bin/bash
# TB-106 A11 - TB30A_BASE_DIR in herkunft.py:51: wer setzt sie, greift sie unter dem Modus? Nur messen.
PY=/Users/jaquelineloffler/trading-bot/trading-env/bin/python3
echo "# TB-106 A11, HEAD $(git rev-parse --short HEAD), $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "== (1) Setzer und Leser im Repo ausserhalb docs/ (git grep)"
git grep -n "TB30A_BASE_DIR" -- ':!docs' | cut -c1-160
echo "== (2) herkunft.py liest paths / selektionsmodus? (Zeilen mit 'paths' oder 'selektion')"
grep -n "paths\|selektion" research/vorregistrierung/herkunft.py || echo "   keine"
echo "== (3) Wirkung: TB30A_BASE_DIR=/gibt/es/nicht, zusaetzlich die drei Modus-Variablen gesetzt (herkunft importiert paths nicht)"
env TB30A_BASE_DIR=/gibt/es/nicht TB_SELEKTIONSWURZEL=/gibt/es/nicht/snap TB_SELEKTIONSHASH=x TB_SELEKTIONSCOMMIT=y \
  $PY -W ignore -c "
import sys; sys.path.insert(0,'research/vorregistrierung'); import herkunft as h
print('   BASE_DIR      ', h.BASE_DIR); print('   REGISTERDATEI ', h.REGISTERDATEI)
print('   paths geladen ', 'paths' in sys.modules)
r = h.register(); print('   register fehlend', r['fehlend'])
print('   commit()      ', h.commit())"
echo "   rc=$?"
