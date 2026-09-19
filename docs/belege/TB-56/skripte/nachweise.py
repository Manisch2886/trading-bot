#!/usr/bin/env python3
"""
TB-56 Schritt 3 - Nachweise 1, 3, 4 und 8, gemessen statt behauptet
==============================================================================
    trading-env/bin/python3 docs/belege/TB-56/skripte/nachweise.py

1  Der neue Plan (research/faltenplan_neun/daten/faltenplan_ohne_schranke.json)
   stimmt je Bot mit der Messung aus Teil A (docs/belege/TB-56/
   teil_a_messung.json, Zweig `ohne_schranke`) ueberein - Soll 9/9.
2  Zulassung nach 4b: je Bot mit/ohne, jede Aenderung namentlich.
3  `ERSTE_MOEGLICHE_FALTE` im Quelltext: grep ueber research/, shared/,
   strategies/ - Code-Treffer (ausserhalb von Docstring/Kommentar) Soll 0.
4  Mutationsgegenprobe (B1), zweifach:
   a) faltenplan_neun im Speicher: Schranke bei 2019 wieder eingesetzt -
      der Plan muss sich messbar aendern.
   b) research/vorregistrierung/faltenplan.py als Wegwerf-Kopie mit EINER
      geaenderten Zeile (`erste = max(2019, erste_falte(bot))`), eigener
      Prozess - die Aktienplaene muessen sich aendern.
8  research/faltenplan_neun/daten/faltenplan.json byteweise unveraendert:
   SHA-256 gegen den Blob unter HEAD~ (vor dieser Arbeit) und `git status`.
"""
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

WURZEL = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BELEGE = os.path.join(WURZEL, "docs", "belege", "TB-56")
NEU = os.path.join(WURZEL, "research", "faltenplan_neun", "daten",
                   "faltenplan_ohne_schranke.json")
ALT = os.path.join(WURZEL, "research", "faltenplan_neun", "daten", "faltenplan.json")
MESSUNG = os.path.join(BELEGE, "teil_a_messung.json")
PY = sys.executable

sys.path.insert(0, os.path.join(WURZEL, "research", "faltenplan_neun"))
import faltenplan_neun as fp            # noqa: E402
import faltenschranke_messung as fm     # noqa: E402

ok_zahl = 0
fehl = []


def pruefe(name, bedingung, zusatz=""):
    global ok_zahl
    if bedingung:
        ok_zahl += 1
        print(f"  ok   {name}  {zusatz}".rstrip())
    else:
        fehl.append(name)
        print(f"  FEHL {name}  {zusatz}".rstrip())


# --- 1: neuer Plan = Messung Teil A -----------------------------------------
print("Nachweis 1 - neuer Plan gegen Messung Teil A, je Bot")
with open(NEU, encoding="utf-8") as f:
    neu = json.load(f)
with open(MESSUNG, encoding="utf-8") as f:
    messung = json.load(f)
gleich = 0
for bot in fp.BOTS:
    a = fm._kern(neu["plaene"][bot])
    b = messung["je_bot"][bot]["ohne_schranke"]
    if a == b:
        gleich += 1
    else:
        print(f"    ABWEICHUNG {bot}: {a} != {b}")
pruefe("1: neuer Plan stimmt je Bot mit Teil A ueberein", gleich == 9, f"{gleich}/9")
pruefe("1b: die Datei traegt keine Schranke",
       neu.get("frueheste_falte") is None, str(neu.get("frueheste_falte")))

# --- 2: Zulassung nach 4b --------------------------------------------------
print("Nachweis 2 - Zulassung nach 4b (mindestens 3 Selektionsfalten)")
aenderungen = []
for bot in fp.BOTS:
    e = messung["je_bot"][bot]
    m, o = e["mit_schranke"], e["ohne_schranke"]
    print(f"    {bot:<28}mit {m['anzahl_selektionsfalten']} ({'ja' if m['zulassung_4b'] else 'nein'})"
          f"  ohne {o['anzahl_selektionsfalten']} ({'ja' if o['zulassung_4b'] else 'nein'})"
          f"  Trockenlauf H: {neu['trockenlauf_3b']['je_bot'][bot]['selektionsfalten_mit_loader_symbol_H']}"
          f" ({'ja' if neu['trockenlauf_3b']['je_bot'][bot]['zulassung_4b_nach_H'] else 'nein'})")
    if m["zulassung_4b"] != o["zulassung_4b"]:
        aenderungen.append(bot)
pruefe("2: kein Bot aendert seine Zulassung nach 4b", not aenderungen, str(aenderungen))

# --- 3: grep im Quelltext --------------------------------------------------
print("Nachweis 3 - ERSTE_MOEGLICHE_FALTE im Quelltext")
NAME = "ERSTE_MOEGLICHE_FALTE"
code_treffer, doku_treffer = [], []
for ordner in ("research", "shared", "strategies"):
    for pfad, unter, dateien in os.walk(os.path.join(WURZEL, ordner)):
        unter[:] = [u for u in unter if u not in ("__pycache__", "trading-env")]
        for d in dateien:
            voll = os.path.join(pfad, d)
            rel = os.path.relpath(voll, WURZEL)
            if d.endswith(".py"):
                quelle = open(voll, encoding="utf-8", errors="replace").read()
                if NAME not in quelle:
                    continue
                # Am Syntaxbaum (B5): kommt der Name als Bezeichner vor?
                baum = ast.parse(quelle)
                namen = [n.lineno for n in ast.walk(baum)
                         if isinstance(n, ast.Name) and n.id == NAME]
                attr = [n.lineno for n in ast.walk(baum)
                        if isinstance(n, ast.Attribute) and n.attr == NAME]
                if namen or attr:
                    code_treffer.append((rel, sorted(namen + attr)))
                zeilen = [i + 1 for i, z in enumerate(quelle.splitlines()) if NAME in z]
                doku_treffer.append((rel, zeilen, "Docstring/Kommentar" if not (namen or attr) else "CODE"))
            elif d.endswith((".md", ".txt", ".json", ".sh")) and "belege/TB-56" not in rel:
                inhalt = open(voll, encoding="utf-8", errors="replace").read()
                if NAME in inhalt:
                    zeilen = [i + 1 for i, z in enumerate(inhalt.splitlines()) if NAME in z]
                    doku_treffer.append((rel, zeilen, "Dokument"))
for rel, zeilen, art in doku_treffer:
    print(f"    {art:<20}{rel}:{','.join(map(str, zeilen))}")
pruefe("3: 0 Treffer als Bezeichner im Code (research/, shared/, strategies/)",
       not code_treffer, str(code_treffer))

# --- 4a: Mutation im Speicher (faltenplan_neun) -------------------------------
print("Nachweis 4a - Schranke 2019 kuenstlich wieder eingesetzt (faltenplan_neun)")
r = fm.mutation(2019)
pruefe("4a: die Schranke veraendert den Plan messbar",
       r["beisst"] and r["anzahl_geaendert"] == 8,
       f"{r['anzahl_geaendert']} von 9 Plaene: {r['bots_geaendert']}")

# --- 4b: Mutation als Wegwerf-Kopie (vorregistrierung/faltenplan.py) ---------
print("Nachweis 4b - Wegwerf-Kopie von research/vorregistrierung mit Schranke")
QUELLE = os.path.join(WURZEL, "research", "vorregistrierung")
LAUF = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
import registerdaten as rd, faltenplan as fp
mess = rd._mess()
plan = fp.faltenplan(mess)
print(json.dumps({b: [f["name"] for f in p["falten"]] for b, p in plan.items()},
                 sort_keys=True))
"""


def _plan_in(ordner):
    lauf = subprocess.run([PY, "-c", LAUF, ordner], capture_output=True, text=True,
                          env=dict(os.environ, TB30A_BASE_DIR=WURZEL))
    if lauf.returncode != 0:
        return None, lauf.stderr[-600:]
    return json.loads(lauf.stdout.strip().splitlines()[-1]), ""


with tempfile.TemporaryDirectory() as tmp:
    orig = os.path.join(tmp, "orig")
    mut = os.path.join(tmp, "mut")
    shutil.copytree(QUELLE, orig, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(QUELLE, mut, ignore=shutil.ignore_patterns("__pycache__"))
    pfad = os.path.join(mut, "faltenplan.py")
    quelle = open(pfad, encoding="utf-8").read()
    alt = "    erste = erste_falte(bot)\n"
    neu_zeile = "    erste = max(2019, erste_falte(bot))\n"
    assert quelle.count(alt) == 1, "Mutationsstelle nicht genau einmal gefunden"
    open(pfad, "w", encoding="utf-8").write(quelle.replace(alt, neu_zeile, 1))
    p_orig, e1 = _plan_in(orig)
    p_mut, e2 = _plan_in(mut)
    pruefe("4b-0: unmutierte Kopie laeuft", p_orig is not None, e1)
    pruefe("4b-1: mutierte Kopie laeuft", p_mut is not None, e2)
    if p_orig and p_mut:
        aktien = [b for b, eig in fp.BOTS.items() if eig["markt"] == "aktien"]
        anders = [b for b in aktien if p_orig[b] != p_mut[b]]
        for b in aktien:
            print(f"    {b:<28}ohne {p_orig[b][0]}..  mit {p_mut[b][0]}..")
        pruefe("4b-2: die wieder eingesetzte Schranke veraendert die Aktienplaene",
               len(anders) == 4, f"{len(anders)}/4: {anders}")
        pruefe("4b-3: unmutiert beginnt kein Aktienplan mit 2019",
               all(p_orig[b][0] != "2019" for b in aktien),
               str({b: p_orig[b][0] for b in aktien}))
        pruefe("4b-4: mutiert beginnen alle vier mit 2019",
               all(p_mut[b][0] == "2019" for b in aktien))

# --- 8: faltenplan.json byteweise unveraendert -----------------------------
print("Nachweis 8 - faltenplan.json byteweise unveraendert")
sha_jetzt = hashlib.sha256(open(ALT, "rb").read()).hexdigest()
rel = os.path.relpath(ALT, WURZEL)
blob_basis = subprocess.run(["git", "show", "d66a2ce:" + rel], cwd=WURZEL,
                            capture_output=True).stdout
sha_basis = hashlib.sha256(blob_basis).hexdigest()
status = subprocess.run(["git", "status", "--short", "--", rel], cwd=WURZEL,
                        capture_output=True, text=True).stdout.strip()
print(f"    SHA-256 jetzt        {sha_jetzt}")
print(f"    SHA-256 unter d66a2ce {sha_basis}")
pruefe("8: identisch mit dem Stand vor dieser Arbeit (d66a2ce) und git status leer",
       sha_jetzt == sha_basis and status == "", repr(status))

print(f"\n{ok_zahl} bestanden, {len(fehl)} gescheitert {fehl}")
sys.exit(0 if not fehl else 1)
