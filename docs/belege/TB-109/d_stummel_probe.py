"""TB-109 D - Verhaltensbeleg zum Widerspruch in Fable 25e (3): Stummel `None` gegen `False`.

Fuer beide Stummel-Fassungen (an die alte paths.py aus dem Bezugscommit angehaengt):
  (1) das Werkzeug selbst: `pfadvergleich.vergleiche(alt + stummel, neu)` - Zahl der Unterschiede,
      verglichene Pfade, und das Urteil, das main() daraus faellen wuerde (GRUEN nur bei 0 Unterschieden
      und beissender Selbstprobe);
  (2) was `strategy_paths` im Wegwerfbaum TUT: nach der Probe je Bot - existieren results/<bot> und
      logs/<bot>? (Ohne Modus legt get_strategy_paths beide an; haelt es den Modus fuer aktiv, nicht.)
Rein lesend gegen das Repo; die Wegwerfbaeume legt pfadvergleich._baum im TMPDIR an, sie werden entfernt.

Aufruf aus der Repo-Wurzel, ohne Modus:
  trading-env/bin/python3 -W ignore docs/belege/TB-109/d_stummel_probe.py
"""
import os
import shutil
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(_REPO, "research", "resolver_selektion"))
import pfadvergleich as pv  # noqa: E402

STUMMEL = {
    "None (gebaut, wie test_paths Probe A)": "\n\ndef selektionsmodus():\n    return None\n",
    "False (Fable 25e (3): selektionsmodus = lambda: False)": "\n\nselektionsmodus = lambda: False\n",
}

alt = pv.alte_fassung()
if alt is None:
    raise SystemExit("NICHT PRUEFBAR: Bezugscommit fehlt")
neu = open(os.path.join(_REPO, "shared", "paths.py"), encoding="utf-8").read()
print("# gebauter Stummel im Werkzeug: pv.STUMMEL == None-Fassung: %s" % (pv.STUMMEL == STUMMEL[list(STUMMEL)[0]]))
for name, stummel in STUMMEL.items():
    print("\n== Stummel %s" % name)
    e = pv.vergleiche(alt + stummel, neu)
    verstellt = (alt + stummel).replace('"data"', '"daten_verstellt"')
    g = pv.vergleiche(verstellt, neu)
    gut = not e["unterschiede"] and bool(g["unterschiede"])
    print("   (1) verglichen %d, Unterschiede %d, Selbstprobe beisst %s => main() urteilte %s"
          % (e["verglichen"], len(e["unterschiede"]), bool(g["unterschiede"]),
             "GRUEN (rc 0)" if gut else "ABBRECHEN (rc 1)"))
    for u in e["unterschiede"]:
        print("       %s / %s: %r -> %r" % (u["bot"], u["name"], u["alt"], u["neu"]))
    baum = pv._baum(alt + stummel)
    try:
        angelegt = []
        for bot in pv.BOTS:
            pv._messen(baum, bot)
            angelegt.append((bot, os.path.isdir(os.path.join(baum, "results", bot)),
                             os.path.isdir(os.path.join(baum, "logs", bot))))
    finally:
        shutil.rmtree(baum, ignore_errors=True)
    ja = sum(1 for _, r, l in angelegt if r and l)
    print("   (2) strategy_paths legt results/<bot> und logs/<bot> an: %d von %d Bots (%s)"
          % (ja, len(angelegt), "wie ohne Modus" if ja == len(angelegt)
             else "haelt den Modus fuer AKTIV" if ja == 0 else "gemischt"))
