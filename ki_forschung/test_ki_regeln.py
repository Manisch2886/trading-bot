"""
Regel-Test der KI-Forschung (TB-179, BA3)
=========================================
Prueft, dass Regelblaetter und Prompts vor jedem Start fest im Repo liegen,
ohne Netz und ohne API-Aufruf; das Repo wird nur gelesen.

R1  manifest.json: Version v1, Modell = MODEL_HAIKU aus shared/claude_client.py
    (gelesen per ast, nicht importiert).
R2  Prompts: jede Datei unter prompts/ (ausser manifest.json) steht genau einmal
    im Manifest, jeder Eintrag hat eine Datei, sha256 gleich; Topf je Eintrag
    ist ein Topf aus aufrufe.DECKEL_USD (per ast) und passt zum Verbraucher.
R3  Regelblaetter: genau die fuenf Blaetter unter regeln/, je im Manifest mit
    gleichem sha256.
R4  Pflichtfelder: jedes Blatt traegt jedes Pflichtfeld genau einmal und nicht
    leer; das Feld Prompts nennt nur Dateien des Manifests, und jeder Prompt
    gehoert zu genau einem Blatt mit gleichem Topf.
R5  Inhalt: Sammler zwei Maerkte und F1..F6 mit Prompt je Frage; Filter an
    F1 Risikoneigung, Schwelle -2, "nie Zulassungsgrund"; Bots: Modell Haiku,
    Startkapital 10 000, Auswertedatum TT.MM.JJJJ, jede ISIN mit gueltiger
    Pruefziffer und nicht aus den USA (nur UCITS), Krypto-Symbole ...USDT,
    Rotation genau zehn ETF und zehn Krypto.
R6  Prompts verlangen JSON und nennen weder Websuche noch eine Adresse.
G   Gegenproben: jede Wache wird an einer verfaelschten Kopie in einem
    temporaeren Ordner rot.

Nutzung:  python3 -B ki_forschung/test_ki_regeln.py      (Ausgang 0 = gruen)
"""
import ast
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

KI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(KI_DIR)
ERGEBNIS = []
TEMP = []

BLAETTER = ("sammler.md", "filter.md", "regime_bot.md", "rotations_bot.md", "nachrichten_bot.md")
PFLICHT_BOT = ("Version", "Modell", "Topf", "Universum", "Entscheidungsregel", "Positionsgrösse", "Ausstieg", "Startkapital",
               "Kosten", "Ausführung", "Ausfall", "Auswertedatum", "Abbruchregel", "Speicher", "Prompts")
PFLICHT = {"sammler.md": ("Version", "Modell", "Topf", "Märkte", "Fragen", "Skala", "Antwortformat", "Quellen", "Vintage", "Lauf",
                          "Ausfall", "Speicher", "Leseregel", "Prompts"),
           "filter.md": ("Version", "Frage", "Schwelle", "Märkte", "Startzeitpunkt", "Ausfall", "Messgrössen",
                         "Quelle der Bot-Zahlen", "Auswertedatum", "Status", "Prompts"),
           "regime_bot.md": PFLICHT_BOT, "rotations_bot.md": PFLICHT_BOT, "nachrichten_bot.md": PFLICHT_BOT + ("Nachrichtenquelle",)}
TOPF_SOLL = {"sammler.md": "sammler", "regime_bot.md": "bots", "rotations_bot.md": "bots", "nachrichten_bot.md": "bots"}
FRAGEN = ("F1 Risikoneigung", "F2 Trend", "F3 Vola-Regime", "F4 Makro", "F5 Liquidität", "F6 Ereignisrisiko")
ISIN_RX = re.compile(r"\b((?:IE|LU|DE|FR|NL|GB|CH|AT|JE|US)[A-Z0-9]{9}[0-9])\b")
KRYPTO_RX = re.compile(r"`([A-Z0-9]{2,10}USDT)`")


def pruefe(name, ok, detail=""):
    ERGEBNIS.append((name, bool(ok)))
    print("  %s %s%s" % ("ok  " if ok else "FEHLT", name, ("   " + str(detail)[:300]) if detail else ""))


def lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def sha_datei(pfad):
    with open(pfad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def konstante(pfad, name):
    for k in ast.walk(ast.parse(lies(pfad))):
        if isinstance(k, ast.Assign) and any(isinstance(z, ast.Name) and z.id == name for z in k.targets):
            return ast.literal_eval(k.value)
    return None


def isin_gueltig(isin):
    """Pruefziffer nach ISO 6166 (Luhn auf den in Ziffern gewandelten Zeichen)."""
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}[0-9]", isin):
        return False
    ziffern = "".join(str(int(c, 36)) for c in isin[:-1])
    summe = 0
    for i, c in enumerate(reversed(ziffern)):
        d = int(c) * (2 if i % 2 == 0 else 1)
        summe += d // 10 + d % 10
    return (10 - summe % 10) % 10 == int(isin[-1])


def felder(text):
    """Pflichtfelder: Zeilen '- **Name:** Wert' im Abschnitt '## Pflichtfelder'."""
    teil = text.split("\n## Pflichtfelder\n", 1)[1].split("\n## ", 1)[0] if "\n## Pflichtfelder\n" in text else ""
    f = {}
    for name, wert in re.findall(r"(?m)^- \*\*([^*]+):\*\* ?(.*)$", teil):
        f.setdefault(name, []).append(wert.strip())
    return f


def befunde_manifest(ki_dir, wurzel):
    b = []
    pd = os.path.join(ki_dir, "prompts")
    try:
        m = json.loads(lies(os.path.join(pd, "manifest.json")))
    except (OSError, ValueError) as e:
        return ["manifest.json nicht lesbar: %s" % e]
    haiku = konstante(os.path.join(wurzel, "shared", "claude_client.py"), "MODEL_HAIKU")
    toepfe = konstante(os.path.join(ki_dir, "aufrufe.py"), "DECKEL_USD") or {}
    if m.get("version") != "v1":
        b.append("Version %r" % m.get("version"))
    if not haiku or m.get("modell") != haiku:
        b.append("Modell %r statt %r" % (m.get("modell"), haiku))
    if m.get("deckel_usd_je_monat") != toepfe:
        b.append("Deckel im Manifest %r statt %r" % (m.get("deckel_usd_je_monat"), toepfe))
    pr = m.get("prompts", {})
    da = sorted(x for x in os.listdir(pd) if x != "manifest.json")
    b += ["Prompt ohne Eintrag: " + x for x in da if x not in pr]
    for name, e in sorted(pr.items()):
        p = os.path.join(pd, name)
        if not os.path.isfile(p):
            b.append("Eintrag ohne Datei: " + name)
            continue
        if sha_datei(p) != e.get("sha256"):
            b.append("sha256 weicht ab: prompts/" + name)
        if e.get("topf") not in toepfe:
            b.append("Topf %r unbekannt: %s" % (e.get("topf"), name))
        if (e.get("topf") == "sammler") != (e.get("verbraucher") == "sammler"):
            b.append("Topf passt nicht zum Verbraucher: " + name)
    rg = m.get("regeln", {})
    rd = os.path.join(ki_dir, "regeln")
    da = sorted(os.listdir(rd)) if os.path.isdir(rd) else []
    if da != sorted(BLAETTER):
        b.append("regeln/ enthaelt %s" % da)
    if sorted(rg) != sorted(BLAETTER):
        b.append("Manifest-Regeln %s" % sorted(rg))
    for name in BLAETTER:
        p = os.path.join(rd, name)
        if os.path.isfile(p) and sha_datei(p) != rg.get(name, {}).get("sha256"):
            b.append("sha256 weicht ab: regeln/" + name)
    return b


def befunde_blaetter(ki_dir, wurzel):
    b = []
    try:
        m = json.loads(lies(os.path.join(ki_dir, "prompts", "manifest.json")))
    except (OSError, ValueError) as e:
        return ["manifest.json nicht lesbar: %s" % e]
    haiku = konstante(os.path.join(wurzel, "shared", "claude_client.py"), "MODEL_HAIKU") or "?"
    pr = m.get("prompts", {})
    besitzer = {}
    for name in BLAETTER:
        p = os.path.join(ki_dir, "regeln", name)
        if not os.path.isfile(p):
            b.append("Blatt fehlt: " + name)
            continue
        t = lies(p)
        f = felder(t)
        for feld in PFLICHT[name]:
            w = f.get(feld, [])
            if len(w) != 1 or len(w[0]) < 2:
                b.append("%s: Pflichtfeld %s %s" % (name, feld, "fehlt" if not w else ("doppelt" if len(w) > 1 else "leer")))
        pz = f.get("Prompts", [""])[0]
        for d in re.findall(r"`([^`]+\.txt)`", pz):
            if d not in pr:
                b.append("%s nennt %s, nicht im Manifest" % (name, d))
            besitzer.setdefault(d, []).append(name)
            if name in TOPF_SOLL and pr.get(d, {}).get("topf") != TOPF_SOLL[name]:
                b.append("%s: Topf von %s ist %r" % (name, d, pr.get(d, {}).get("topf")))
        for i in ISIN_RX.findall(t):
            if not isin_gueltig(i):
                b.append("%s: ISIN %s Pruefziffer falsch" % (name, i))
            elif i.startswith("US"):
                b.append("%s: US-ISIN %s (nur UCITS)" % (name, i))
        if name in TOPF_SOLL:
            if haiku not in f.get("Modell", [""])[0]:
                b.append("%s: Modell nicht %s" % (name, haiku))
            if "`%s`" % TOPF_SOLL[name] not in f.get("Topf", [""])[0]:
                b.append("%s: Topf nicht %s" % (name, TOPF_SOLL[name]))
        if name.endswith("_bot.md"):
            if "10 000" not in f.get("Startkapital", [""])[0]:
                b.append("%s: Startkapital nicht 10 000" % name)
            if not re.search(r"\b\d{2}\.\d{2}\.\d{4}\b", f.get("Auswertedatum", [""])[0]):
                b.append("%s: Auswertedatum ohne Datum" % name)
            u = f.get("Universum", [""])[0]
            if not KRYPTO_RX.findall(u) and not ISIN_RX.findall(u):
                b.append("%s: Universum ohne Symbol" % name)
            if name == "rotations_bot.md" and (len(set(ISIN_RX.findall(u))) != 10 or len(set(KRYPTO_RX.findall(u))) != 10):
                b.append("rotations_bot.md: nicht genau 10 ETF und 10 Krypto")
        if name == "sammler.md":
            fr = f.get("Fragen", [""])[0]
            b += ["sammler.md: Frage fehlt: " + q for q in FRAGEN if q not in fr]
            mk = f.get("Märkte", [""])[0]
            b += ["sammler.md: Markt fehlt: " + q for q in ("`krypto`", "`aktien`") if q not in mk]
            for n in range(1, 7):
                if not [d for d in pr if d.startswith("sammler_f%d_" % n)]:
                    b.append("sammler.md: kein Prompt fuer F%d" % n)
        if name == "filter.md":
            if "nie Zulassungsgrund" not in f.get("Status", [""])[0]:
                b.append("filter.md: Status ohne 'nie Zulassungsgrund'")
            if "F1 Risikoneigung" not in f.get("Frage", [""])[0]:
                b.append("filter.md: Frage nicht F1 Risikoneigung")
            if "−2" not in f.get("Schwelle", [""])[0]:
                b.append("filter.md: Schwelle nicht −2")
            if not re.search(r"\b\d{2}\.\d{2}\.\d{4}\b", f.get("Auswertedatum", [""])[0]):
                b.append("filter.md: Auswertedatum ohne Datum")
    for d in pr:
        if len(besitzer.get(d, [])) != 1:
            b.append("Prompt %s gehoert zu %s" % (d, besitzer.get(d, [])))
    return b


def befunde_prompts(ki_dir):
    b = []
    pd = os.path.join(ki_dir, "prompts")
    for d in sorted(x for x in os.listdir(pd) if x.endswith(".txt")):
        t = lies(os.path.join(pd, d))
        if d.startswith("sammler_f"):
            continue
        if "JSON" not in t:
            b.append(d + ": verlangt kein JSON")
    for d in sorted(x for x in os.listdir(pd) if x.endswith(".txt")):
        t = lies(os.path.join(pd, d)).lower()
        b += ["%s nennt %r" % (d, w) for w in ("web_search", "websuche", "http://", "https://") if w in t]
    return b


def verfaelschen(datei, alt, neu):
    k = tempfile.mkdtemp(prefix="tb179_gp_")
    TEMP.append(k)
    ziel = os.path.join(k, "ki_forschung")
    shutil.copytree(KI_DIR, ziel, ignore=shutil.ignore_patterns("__pycache__", "*.db"))
    p = os.path.join(ziel, datei)
    if alt is None:
        with open(p, "w", encoding="utf-8") as f:
            f.write(neu)
    else:
        t = lies(p)
        assert t.count(alt) == 1, (datei, alt)
        with open(p, "w", encoding="utf-8") as f:
            f.write(t.replace(alt, neu))
    return ziel


def main():
    print("Regel-Test KI-Forschung (TB-179)")
    b = befunde_manifest(KI_DIR, REPO)
    pruefe("R1-R3 Manifest: Modell, Prompts und Regelblaetter mit sha256", not b, b)
    b = befunde_blaetter(KI_DIR, REPO)
    pruefe("R4-R5 Regelblaetter: Pflichtfelder und Inhalt (%d Blaetter)" % len(BLAETTER), not b, b)
    b = befunde_prompts(KI_DIR)
    pruefe("R6 Prompts: JSON verlangt, keine Websuche, keine Adresse", not b, b)
    gp = [("G1 Prompt um ein Zeichen geaendert", befunde_manifest, ("prompts/regime_bot.txt", "von -2 bis +2", "von -2 bis +3")),
          ("G2 Prompt ohne Manifest-Eintrag", befunde_manifest, ("prompts/zusatz.txt", None, "Antworte als JSON.\n")),
          ("G3 Modell im Manifest getauscht", befunde_manifest, ("prompts/manifest.json", '"modell": "', '"modell": "claude-sonnet-5x')),
          ("G4 Regelblatt nach dem Hash geaendert", befunde_manifest, ("regeln/filter.md", "36 Stunden", "37 Stunden")),
          ("G5 Pflichtfeld Ausstieg entfernt", befunde_blaetter, ("regeln/regime_bot.md", "- **Ausstieg:**", "- Ausstieg:")),
          ("G6 ISIN mit falscher Pruefziffer", befunde_blaetter, ("regeln/regime_bot.md", "`IE00B5BMR087`", "`IE00B5BMR088`")),
          ("G7 US-ETF im Universum", befunde_blaetter, ("regeln/regime_bot.md", "`IE00B5BMR087`", "`US78462F1030`")),
          ("G8 'nie Zulassungsgrund' entfernt", befunde_blaetter, ("regeln/filter.md", "nie Zulassungsgrund", "kein Zulassungsgrund")),
          ("G9 Rotation mit neun Krypto", befunde_blaetter, ("regeln/rotations_bot.md", ", `DOTUSDT`", "")),
          ("G10 Pflichtfeld doppelt", befunde_blaetter, ("regeln/sammler.md", "- **Version:** v1\n", "- **Version:** v1\n- **Version:** v2\n")),
          ("G11 Websuche im Prompt", befunde_prompts, ("prompts/nachrichten_bot.txt", "Kein Wissen", "Nutze web_search. Kein Wissen"))]
    for name, fn, (datei, alt, neu) in gp:
        k = verfaelschen(datei, alt, neu)
        b = fn(k, REPO) if fn is not befunde_prompts else fn(k)
        pruefe(name + " wird rot", bool(b), b[:1])
    n = len(ERGEBNIS)
    fehlt = sum(1 for _n, ok in ERGEBNIS if not ok)
    print("Pruefungen: %d, FEHLT: %d" % (n, fehlt))
    return 1 if fehlt else 0


if __name__ == "__main__":
    try:
        rc = main()
    finally:
        for d in TEMP:
            shutil.rmtree(d, ignore_errors=True)
    sys.exit(rc)
