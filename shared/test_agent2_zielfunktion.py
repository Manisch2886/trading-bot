"""
Selbsttests: die Zielfunktion von Agent 2 (TB-22)
==============================================================================
Geprueft wird das VERHALTEN von `shared/param_search_agent.py` - also welche
Kombination am Ende gewinnt und was im Prompt steht, der tatsaechlich
abgeschickt wird. Nicht geprueft wird, ob irgendwo ein Feldname im Quelltext
vorkommt.

DIE EIGENTLICHE ZUSICHERUNG (Abschnitt 1)
------------------------------------------------------------------------------
Agent 2 waehlt nach `robustness_score_chronologisch` - dem robustness_score,
gerechnet auf `max_drawdown_chronologisch_pct` statt auf dem Drawdown der
aneinandergehaengten Symbol-Bloecke. Bei einem Datensatz, in dem beide Masse
zu VERSCHIEDENEN Rangfolgen fuehren, muss die chronologische gewinnen.

KEINE ECHTEN API-AUFRUFE
------------------------------------------------------------------------------
Der Sendeweg ist seit TB-22 ein Parameter (`run_agent_search(..., call_fn=)`).
Der Test reicht eine Attrappe herein, die jeden Prompt mitschreibt. Zusaetzlich
wird `param_search_agent.call_claude` durch eine Funktion ersetzt, die beim
Aufruf sofort eine Ausnahme wirft: kaeme irgendein Pfad doch am Parameter
vorbei, faellt der Test hart durch, statt still ins Netz zu gehen.

Zwei wiederkehrende Fallen aus #73, #77, #78, #79, #81, #86, TB-15 und TB-20
sind bewusst umgangen:

**Falle 1 - die selbstbestaetigende Probe.** Nirgends wird ein Gewinner von
Hand hingeschrieben und anschliessend wiedererkannt. Die Datensaetze entstehen
aus einem Zufallsgenerator mit festem Startwert; welche Zeile gewinnen muss,
rechnet eine im Test getrennt geschriebene Rangfolge aus - und der Test
verlangt vorab den NACHWEIS, dass die beiden Rangfolgen in diesem Datensatz
ueberhaupt auseinandergehen (Abschnitt 1a). Abschnitt 1b kommt zusaetzlich
ganz ohne die Formel aus: zwei Zeilen mit gleicher Rendite und gleicher
Trade-Zahl, die sich nur im Drawdown unterscheiden - da muss die Zeile mit
dem kleineren chronologischen Rueckgang gewinnen, ohne dass man dafuer
irgendetwas ausrechnen muesste. Abschnitt 5 beobachtet den Ablauf schliesslich
an MUTIERTEN Kopien der Datei: jede Wache wird einzeln entfernt, und die
zugehoerige Pruefung MUSS dann anschlagen.

**Falle 2 - die zweite Wache verdeckt das Fehlen der ersten.** Die vier
Zusicherungen sind so getrennt, dass je nur eine greifen kann:
  * Abschnitt 1 haengt ausschliesslich an der Auswahl (`max(...)`) und ist
    voellig unabhaengig davon, was im Prompt steht - die Attrappe schlaegt
    ohnehin JEDE Kombination des Datensatzes der Reihe nach vor, das Modell
    entscheidet also nichts.
  * Abschnitt 3 haengt ausschliesslich am abgeschickten Prompt und sagt
    nichts darueber, wer am Ende gewinnt.
  * Abschnitt 2 (Gegenprobe) kann nur ueber Gleichheit beider Masse bestehen
    und faellt durch, sobald die Umstellung mehr aendert als beabsichtigt.
  * Abschnitt 4 haengt an der Unvalidiert-Kennzeichnung im fertigen Bericht -
    einer Konstanten aus shared/empfehlung_format.py, die mit der Zielgroesse
    nichts zu tun hat.

Kein Test-Framework, wie in allen uebrigen Selbsttests dieses Projekts.

Ein Prozess je Bot: die drei Bots mit Quartals-Review haben gleichnamige,
inhaltlich verschiedene Module (`quarterly_review.py`, `live_params.py`, ...).
Zwei davon im selben Prozess zu importieren, wuerde ueber `sys.modules` still
den falschen Bot laden.

Dieser Test veraendert nichts im Repo: er verschickt nichts, schreibt keine
Datei und fasst keine Datenbank an; die Mutationen entstehen ausschliesslich
in Kopien unterhalb des Temporaerverzeichnisses. Abschnitt 6 weist das per
`git status` nach.

Nutzung:
    python3 shared/test_agent2_zielfunktion.py
    python3 shared/test_agent2_zielfunktion.py --bot <name>        # intern
    python3 shared/test_agent2_zielfunktion.py --mutation <name>   # intern
"""

import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile

_SHARED = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_SHARED)


def stubs_anlegen() -> str:
    """Platzhalter-Module, ohne die die Skripte nicht importierbar waeren
    (config/email_config.py und shared/fetch_binance_data.py liegen bewusst
    nicht im Repo). Wortgleich zum Vorgehen in test_empfehlung_format.py.
    Alles, was verschicken oder laden wuerde, wirft AssertionError - faellt
    der Test also versehentlich in einen echten Aufruf, bricht er ab, statt
    still etwas zu tun."""
    d = tempfile.mkdtemp(prefix="tb22_stubs_")

    open(os.path.join(d, "email_config.py"), "w").write(
        "# Stub - keine echten Zugangsdaten\n"
        "EMAIL_ADDRESS = 'stub@example.invalid'\n"
        "RECIPIENT_EMAIL = 'stub@example.invalid'\n"
        "EMAIL_PASSWORD = ''\n"
        "SMTP_SERVER = 'localhost'\n"
        "SMTP_PORT = 465\n"
        "USE_SSL = True\n")

    open(os.path.join(d, "telegram_config.py"), "w").write(
        "def get_credentials():\n"
        "    raise AssertionError('Stub: es darf nichts an Telegram gehen')\n")

    open(os.path.join(d, "anthropic.py"), "w").write(
        "class Anthropic:\n"
        "    def __init__(self, *a, **k):\n"
        "        raise AssertionError('Stub: keine Claude-API-Aufrufe im Test')\n")

    os.makedirs(os.path.join(d, "binance"), exist_ok=True)
    open(os.path.join(d, "binance", "__init__.py"), "w").write("from .client import Client\n")
    open(os.path.join(d, "binance", "client.py"), "w").write(
        "class _Meta(type):\n"
        "    def __getattr__(cls, name):\n"
        "        return name\n"
        "class Client(metaclass=_Meta):\n"
        "    def __init__(self, *a, **k):\n"
        "        pass\n"
        "    def __getattr__(self, name):\n"
        "        raise AssertionError('Stub: keine Netzwerkzugriffe im Test')\n")

    for name in ("fetch_binance_data", "fetch_stock_data", "fetch_multi_data",
                 "fetch_4h_data", "yfinance"):
        open(os.path.join(d, name + ".py"), "w").write(
            "API_KEY = ''\nAPI_SECRET = ''\nINTERVAL = '1d'\n"
            "def _boom(*a, **k):\n"
            "    raise AssertionError('Stub: es duerfen keine Kursdaten geladen werden')\n"
            "fetch_historical_data = _boom\n"
            "fetch_all_symbols = _boom\n"
            "download = _boom\n"
            "Ticker = _boom\n")

    return d


STUB_DIR = stubs_anlegen()
for _pfad in (STUB_DIR, os.path.join(BASE_DIR, "notifications"), _SHARED):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

# Die drei Bots, die Agent 2 ueberhaupt aufrufen (agent_optimise.py und
# quarterly_review.py gibt es nur bei ihnen - Uebergabeprotokoll 6.2).
BOTS = ("elliott_wave", "elliott_wave_stocks", "t3_supertrend")


# ===========================================================================
# Protokoll
# ===========================================================================
class Protokoll:
    def __init__(self, titel=""):
        self.titel = titel
        self.ok = 0
        self.fehler = []

    def pruefe(self, name, bedingung, hinweis=""):
        if bedingung:
            self.ok += 1
            print(f"  [OK ] {name}" + (f"   {hinweis}" if hinweis else ""))
        else:
            self.fehler.append(name)
            print(f"  [FEHLER] {name}{(' - ' + hinweis) if hinweis else ''}")
        return bool(bedingung)


# ===========================================================================
# Unabhaengige Rangfolge - getrennt vom Modul geschrieben
# ===========================================================================
def referenz_score(avg_return_pct, num_trades, drawdown):
    """Der robustness_score, wie multi_symbol_optimise ihn definiert, hier
    eigenstaendig hingeschrieben. Welcher Drawdown hineingeht, entscheidet
    der Aufrufer - genau darum geht es in dieser Aufgabe."""
    strafe = abs(drawdown) if drawdown != 0 else 1.0
    return round((avg_return_pct * (num_trades ** 0.5)) / strafe, 3)


def referenz_sieger(zeilen, drawdown_feld):
    """Die Zeile, die eine Auswahl auf diesem Drawdown-Mass gewinnen muesste.
    `max` nimmt bei Gleichstand die erste - die Datensaetze sind so gebaut,
    dass es keinen gibt (siehe `erzeuge_datensatz`)."""
    return max(zeilen, key=lambda z: referenz_score(
        z["avg_return_pct"], z["num_trades"], z[drawdown_feld]))


def schluesselpaar(zeile):
    """Die Kombination als vergleichbares Paar - die Ergebniszeile selbst
    traegt spaeter Zusatzfelder und laesst sich nicht direkt vergleichen."""
    return (zeile["deviation_pct"], zeile["stop_loss_pct"])


# ===========================================================================
# Datensaetze
# ===========================================================================
def erzeuge_datensatz(rng, anzahl=8, gleiche_masse=False):
    """Eine Ergebnistabelle, wie `evaluate_combination_multi` sie liefert:
    beide Drawdown-Masse, der robustness_score auf dem BLOCK-Mass.

    Datensaetze mit Gleichstand in einer der beiden Rangfolgen werden
    verworfen - bei Gleichstand haengt der Gewinner an der Reihenfolge und
    die Pruefung wuerde etwas anderes messen als gemeint."""
    while True:
        zeilen = []
        for i in range(anzahl):
            avg = round(rng.uniform(0.2, 3.0), 2)
            trades = rng.randint(40, 400)
            dd_block = round(-rng.uniform(5.0, 300.0), 2)
            dd_chrono = dd_block if gleiche_masse else round(-rng.uniform(5.0, 300.0), 2)
            zeile = {
                "deviation_pct": round(1.0 + i * 0.5, 2),
                "stop_loss_pct": round(2.0 + i * 0.25, 2),
                "num_trades": trades,
                "avg_return_pct": avg,
                "max_drawdown_pct": dd_block,
                "max_drawdown_chronologisch_pct": dd_chrono,
            }
            zeile["robustness_score"] = referenz_score(avg, trades, dd_block)
            zeilen.append(zeile)

        eindeutig = True
        for feld in ("max_drawdown_pct", "max_drawdown_chronologisch_pct"):
            werte = sorted((referenz_score(z["avg_return_pct"], z["num_trades"], z[feld])
                            for z in zeilen), reverse=True)
            if werte[0] == werte[1]:
                eindeutig = False
        if eindeutig:
            return zeilen


PARAM_SPEC = {
    "deviation_pct": {"type": "float", "range": [1.0, 6.0], "step": 0.5},
    "stop_loss_pct": {"type": "float", "range": [2.0, 4.0], "step": 0.25},
}


# ===========================================================================
# Die Attrappe: der Sendeweg, ohne Netz
# ===========================================================================
class Attrappe:
    """Schlaegt der Reihe nach JEDE Kombination des Datensatzes vor und
    stoppt dann. Dass alle Kombinationen getestet werden, ist Absicht: so
    entscheidet ueber den Gewinner allein die Auswahl im Code, nicht die
    Laune eines Modells - und Abschnitt 1 misst genau diese Auswahl."""

    def __init__(self, zeilen):
        self.vorschlaege = [{"deviation_pct": z["deviation_pct"],
                              "stop_loss_pct": z["stop_loss_pct"]} for z in zeilen]
        self.index = 0
        self.prompts = []

    def __call__(self, system_prompt, user_message, max_tokens=1000, **kwargs):
        self.prompts.append({"system": system_prompt, "user": user_message})
        if self.index < len(self.vorschlaege):
            entscheidung = {"action": "test", "params": self.vorschlaege[self.index],
                            "reasoning": "Attrappe"}
            self.index += 1
        else:
            entscheidung = {"action": "stop", "reasoning": "Attrappe fertig"}
        return {"success": True, "text": json.dumps(entscheidung),
                "stop_reason": "end_turn", "raw": None}


def kein_echter_aufruf(*args, **kwargs):
    raise AssertionError("Es wurde ein ECHTER API-Aufruf versucht "
                         "(param_search_agent.call_claude).")


def lauf(psa, zeilen, seeds=False):
    """Ein vollstaendiger Agenten-Lauf auf einem Datensatz. Gibt das Ergebnis
    und die Attrappe (mit allen mitgeschriebenen Prompts) zurueck."""
    nach_schluessel = {schluesselpaar(z): z for z in zeilen}

    def evaluate(params):
        schluessel = (round(float(params["deviation_pct"]), 2),
                      round(float(params["stop_loss_pct"]), 2))
        treffer = nach_schluessel.get(schluessel)
        return dict(treffer) if treffer else None

    attrappe = Attrappe(zeilen)
    original = psa.call_claude
    psa.call_claude = kein_echter_aufruf
    try:
        ergebnis = psa.run_agent_search(
            evaluate, PARAM_SPEC,
            seed_combos=[{"deviation_pct": zeilen[0]["deviation_pct"],
                          "stop_loss_pct": zeilen[0]["stop_loss_pct"]}] if seeds else None,
            max_iterations=len(zeilen) + 1, call_fn=attrappe)
    finally:
        psa.call_claude = original
    return ergebnis, attrappe


# ===========================================================================
# Abschnitt 1 - Die Zusicherung
# ===========================================================================
def abschnitt1(psa, p: Protokoll) -> bool:
    print("\n1) Die Zusicherung: bei verschiedenen Rangfolgen gilt die chronologische")

    rng = random.Random(20260913)
    faelle = 0
    getrennt = 0
    alle_richtig = True
    beispiel = ""

    for _ in range(40):
        zeilen = erzeuge_datensatz(rng)
        sieger_block = referenz_sieger(zeilen, "max_drawdown_pct")
        sieger_chrono = referenz_sieger(zeilen, "max_drawdown_chronologisch_pct")
        faelle += 1
        if schluesselpaar(sieger_block) == schluesselpaar(sieger_chrono):
            continue  # hier sagen beide Masse dasselbe - nicht der Prueffall
        getrennt += 1

        ergebnis, _ = lauf(psa, zeilen)
        gewaehlt = ergebnis["best"]
        if gewaehlt is None or schluesselpaar(gewaehlt) != schluesselpaar(sieger_chrono):
            alle_richtig = False
            beispiel = (f"gewaehlt {schluesselpaar(gewaehlt) if gewaehlt else None}, "
                        f"chronologisch waere {schluesselpaar(sieger_chrono)}, "
                        f"auf Bloecken waere {schluesselpaar(sieger_block)}")
            break

    if not p.pruefe("Abschnitt 1a: es gibt ueberhaupt Datensaetze, in denen die beiden "
                    "Masse auseinandergehen", getrennt > 0,
                    f"{getrennt} von {faelle} Datensaetzen"):
        return False

    ok = p.pruefe(f"Abschnitt 1a: in ALLEN {getrennt} Faellen gewinnt die chronologische "
                  "Rangfolge", alle_richtig, beispiel)

    # --- 1b: derselbe Befund ohne jede Formel ------------------------------
    # Gleiche Rendite, gleiche Trade-Zahl, nur die Drawdowns unterscheiden
    # sich - und zwar ueber Kreuz. Welche Zeile gewinnen muss, ergibt sich
    # aus "kleinerer Rueckgang ist besser", ohne dass man etwas ausrechnet.
    ueber_kreuz = [
        {"deviation_pct": 1.0, "stop_loss_pct": 2.0, "num_trades": 100,
         "avg_return_pct": 1.0, "max_drawdown_pct": -10.0,
         "max_drawdown_chronologisch_pct": -200.0},
        {"deviation_pct": 2.0, "stop_loss_pct": 3.0, "num_trades": 100,
         "avg_return_pct": 1.0, "max_drawdown_pct": -200.0,
         "max_drawdown_chronologisch_pct": -10.0},
    ]
    for zeile in ueber_kreuz:
        zeile["robustness_score"] = referenz_score(
            zeile["avg_return_pct"], zeile["num_trades"], zeile["max_drawdown_pct"])

    ergebnis, _ = lauf(psa, ueber_kreuz)
    gewaehlt = ergebnis["best"]
    ok = p.pruefe("Abschnitt 1b: bei gleicher Rendite und gleicher Trade-Zahl gewinnt der "
                  "kleinere CHRONOLOGISCHE Rueckgang",
                  gewaehlt is not None and schluesselpaar(gewaehlt) == (2.0, 3.0),
                  f"gewaehlt {schluesselpaar(gewaehlt) if gewaehlt else None}") and ok

    ok = p.pruefe("Abschnitt 1b: das Ergebnis benennt das Mass, auf dem ausgewaehlt wurde",
                  ergebnis.get("zielmass", {}).get("drawdown_feld")
                  == "max_drawdown_chronologisch_pct",
                  str(ergebnis.get("zielmass"))) and ok
    return ok


# ===========================================================================
# Abschnitt 2 - Gegenprobe
# ===========================================================================
def abschnitt2(psa, p: Protokoll) -> bool:
    print("\n2) Gegenprobe: fuehren beide Masse zur selben Rangfolge, aendert sich nichts")

    rng = random.Random(770077)
    ok = True
    geprueft = 0
    for _ in range(10):
        zeilen = erzeuge_datensatz(rng, gleiche_masse=True)
        sieger_block = referenz_sieger(zeilen, "max_drawdown_pct")
        ergebnis, _ = lauf(psa, zeilen)
        gewaehlt = ergebnis["best"]
        geprueft += 1
        if gewaehlt is None or schluesselpaar(gewaehlt) != schluesselpaar(sieger_block):
            ok = p.pruefe("Abschnitt 2: derselbe Gewinner wie auf dem alten Mass", False,
                          f"gewaehlt {schluesselpaar(gewaehlt) if gewaehlt else None}, "
                          f"erwartet {schluesselpaar(sieger_block)}") and ok
            break
    else:
        ok = p.pruefe(f"Abschnitt 2: in allen {geprueft} Datensaetzen derselbe Gewinner wie "
                      "auf dem alten Mass", True) and ok

    # Und der Score selbst ist derselbe, wenn beide Drawdowns gleich sind -
    # die Umstellung erfindet keine neue Zahl, sie nimmt einen anderen Nenner.
    zeilen = erzeuge_datensatz(random.Random(4711), gleiche_masse=True)
    ergebnis, _ = lauf(psa, zeilen)
    gleich = all(h.get("robustness_score_chronologisch") == h.get("robustness_score")
                 for h in ergebnis["history"] if h.get("robustness_score") is not None)
    ok = p.pruefe("Abschnitt 2: bei gleichem Drawdown ist auch der Score Zeile fuer Zeile "
                  "gleich", gleich) and ok

    # --- 2c: der Ersatzweg greift NUR, wenn der Wert wirklich fehlt -------
    # Eine zweite Wache darf das Fehlen der ersten nicht verdecken: der
    # Ersatzweg auf das alte Mass ist da, weil `run_agent_search` auch
    # ausserhalb der neun Bots aufrufbar ist - er darf aber weder still
    # greifen noch dann, wenn der chronologische Wert vorliegt.
    ohne_chrono = [{k: v for k, v in z.items()
                    if k != "max_drawdown_chronologisch_pct"}
                   for z in erzeuge_datensatz(random.Random(5150))]
    ergebnis, attrappe = lauf(psa, ohne_chrono)
    ok = p.pruefe("Abschnitt 2c: fehlt der chronologische Wert, wird der Ersatzweg benannt",
                  ergebnis["zielmass"]["modus"] == "ersatzweise",
                  str(ergebnis["zielmass"])) and ok
    ok = p.pruefe("Abschnitt 2c: der Ersatzweg steht auch im Prompt",
                  all("ersatzweise" in pr["user"] for pr in attrappe.prompts[1:])) and ok
    ok = p.pruefe("Abschnitt 2c: und er waehlt dann nach dem alten Mass",
                  schluesselpaar(ergebnis["best"])
                  == schluesselpaar(referenz_sieger(ohne_chrono, "max_drawdown_pct"))) and ok

    mit_chrono = erzeuge_datensatz(random.Random(5150))
    ergebnis_mit, _ = lauf(psa, mit_chrono)
    ok = p.pruefe("Abschnitt 2c: liegt der Wert vor, greift der Ersatzweg NICHT",
                  ergebnis_mit["zielmass"]["modus"] == "chronologisch",
                  str(ergebnis_mit["zielmass"])) and ok
    return ok


# ===========================================================================
# Abschnitt 3 - Der Prompt sagt, worauf ausgewaehlt wird
# ===========================================================================
def abschnitt3(psa, p: Protokoll) -> bool:
    print("\n3) Der abgeschickte Prompt nennt das Mass")

    zeilen = erzeuge_datensatz(random.Random(31415))
    ergebnis, attrappe = lauf(psa, zeilen)

    ok = p.pruefe("Abschnitt 3: es wurde ueberhaupt etwas abgeschickt",
                  len(attrappe.prompts) > 0, f"{len(attrappe.prompts)} Aufrufe")
    if not ok:
        return False

    benutztes_feld = ergebnis["zielmass"]["feld"]
    nachrichten = [pr["user"] for pr in attrappe.prompts]

    # Der Prompt muss GENAU das Feld nennen, nach dem tatsaechlich
    # ausgewaehlt wurde - nicht irgendeinen Feldnamen. Damit koennen Prompt
    # und Auswahl nicht auseinanderlaufen.
    ok = p.pruefe("Abschnitt 3: jeder Prompt nennt das Feld, nach dem ausgewaehlt wurde",
                  all(benutztes_feld in n for n in nachrichten), benutztes_feld) and ok

    ok = p.pruefe("Abschnitt 3: jeder Prompt hat einen ausgewiesenen Zielgroessen-Abschnitt",
                  all("ZIELGROESSE DER AUSWAHL" in n for n in nachrichten)) and ok

    ok = p.pruefe("Abschnitt 3: der Prompt sagt, dass das Blockmass NICHT das "
                  "Auswahlkriterium ist",
                  all("NICHT das Auswahlkriterium" in n for n in nachrichten)) and ok

    # Beide Zahlen stehen dem Modell vor Augen (Uebergangsregel: ausweisen,
    # nicht verschweigen) - entschieden wird trotzdem auf einer davon.
    ok = p.pruefe("Abschnitt 3: beide Drawdown-Masse stehen in der Ergebnistabelle",
                  all("max_drawdown_pct" in n and "max_drawdown_chronologisch_pct" in n
                      for n in nachrichten[1:] or nachrichten)) and ok

    ok = p.pruefe("Abschnitt 3: der System-Prompt verweist auf den Zielgroessen-Abschnitt",
                  "ZIELGROESSE DER AUSWAHL" in attrappe.prompts[0]["system"]) and ok

    # Und die Ausgabe sagt es auch - nicht nur der Prompt.
    zeile = psa.zielmass_zeile(ergebnis)
    ok = p.pruefe("Abschnitt 3: die Ausgabe benennt die Zielgroesse",
                  benutztes_feld in zeile, zeile[:90] + "...") and ok
    return ok


# ===========================================================================
# Abschnitt 4 - Die Unvalidiert-Kennzeichnung bleibt (End-to-End je Bot)
# ===========================================================================
def bericht_je_bot(psa, bot: str):
    """Baut den echten Quartals-Bericht dieses Bots - mit und ohne die
    Zielgroessen-Angabe. Laeuft im Kindprozess, ein Bot je Prozess."""
    sys.path.insert(0, os.path.join(BASE_DIR, "strategies", bot))
    import quarterly_review as qr
    import empfehlung_format as ef

    zeilen = erzeuge_datensatz(random.Random(99))
    ergebnis, _ = lauf(psa, zeilen)
    hinweis = psa.zielmass_zeile(ergebnis)

    wf = {"in_sample": {"num_trades": 60, "win_rate": 41.0, "avg_return_pct": 1.2,
                        "robustness_score": 0.9},
          "out_of_sample": {"num_trades": 31, "win_rate": 38.7, "avg_return_pct": 0.8,
                             "robustness_score": 0.4}}
    real = {"num_trades": 0}
    vorschlag = {k: v for k, v in list(qr.CURRENT_PARAMS.items())}

    mit = qr.build_report(wf, vorschlag, wf, real, "", zielmass_hinweis=hinweis)
    ohne = qr.build_report(wf, vorschlag, wf, real, "")
    return ef, mit, ohne


def abschnitt4(psa, p: Protokoll, bot: str) -> bool:
    print(f"\n4) [{bot}] Unvalidiert-Kennzeichnung und Zielgroesse im fertigen Bericht")
    ef, mit, ohne = bericht_je_bot(psa, bot)

    ok = p.pruefe(f"Abschnitt 4 [{bot}]: Typ-B-Ueberschrift kennzeichnet den Vorschlag als "
                  "unvalidiert", ef.HEADER_TYP_B in mit and "UNVALIDIERT" in ef.HEADER_TYP_B)
    ok = p.pruefe(f"Abschnitt 4 [{bot}]: der Pflichthinweis steht im Bericht",
                  ef.UNVALIDIERT_HINWEIS in mit) and ok
    ok = p.pruefe(f"Abschnitt 4 [{bot}]: der Schlusshinweis ist unveraendert",
                  "WICHTIG: Es wurde NICHTS automatisch geaendert." in mit) and ok
    ok = p.pruefe(f"Abschnitt 4 [{bot}]: der Bericht nennt die Zielgroesse der Auswahl",
                  "robustness_score_chronologisch" in mit) and ok

    # Die Probe, die anschlaegt, wenn die Angabe fehlt: derselbe Bericht ohne
    # die Angabe darf sie auch nicht enthalten - sonst pruefte die Zeile
    # darueber nichts.
    ok = p.pruefe(f"Abschnitt 4 [{bot}]: ohne die Angabe fehlt sie auch im Bericht "
                  "(die Pruefung darueber kann also durchfallen)",
                  "robustness_score_chronologisch" not in ohne) and ok
    ok = p.pruefe(f"Abschnitt 4 [{bot}]: der Pflichthinweis haengt NICHT an der Zielgroesse",
                  ef.UNVALIDIERT_HINWEIS in ohne) and ok
    return ok


# ===========================================================================
# Abschnitt 5 - Mutationsproben
# ===========================================================================
MUTATIONEN = {
    "auswahl_auf_blockmass": (
        "    schluessel = FELD_SCORE_CHRONO if modus == \"chronologisch\" else FELD_SCORE_BLOCK",
        "    schluessel = FELD_SCORE_BLOCK",
        "abschnitt1",
    ),
    "score_auf_blockdrawdown": (
        "    drawdown = zeile.get(FELD_DRAWDOWN_CHRONO)",
        "    drawdown = zeile.get(FELD_DRAWDOWN_BLOCK)",
        "abschnitt1",
    ),
    "zielgroesse_nicht_im_prompt": (
        "            f\"{zielmass_baustein(zielmass_modus(history))}\\n\\n\"\n",
        "",
        "abschnitt3",
    ),
    "prompt_nennt_falsches_mass": (
        "            f\"Massgeblich ist ausschliesslich '{FELD_SCORE_CHRONO}' \"",
        "            f\"Massgeblich ist ausschliesslich '{FELD_SCORE_BLOCK}' \"",
        "abschnitt3",
    ),
    "ausgabe_ohne_zielgroesse": (
        "def zielmass_zeile(ergebnis: dict) -> str:",
        "def zielmass_zeile(ergebnis: dict) -> str:\n    return \"\"",
        "abschnitt4",
    ),
}


def lade_modul(pfad, name="param_search_agent"):
    spec = importlib.util.spec_from_file_location(name, pfad)
    modul = importlib.util.module_from_spec(spec)
    sys.modules[name] = modul
    spec.loader.exec_module(modul)
    return modul


def mutiere(name: str, ziel_dir: str) -> str:
    alt, neu, _ = MUTATIONEN[name]
    quelle = open(os.path.join(_SHARED, "param_search_agent.py")).read()
    if quelle.count(alt) != 1:
        raise SystemExit(f"Mutation '{name}': Anker kommt {quelle.count(alt)}x vor, "
                          f"erwartet genau 1x")
    pfad = os.path.join(ziel_dir, "param_search_agent.py")
    open(pfad, "w").write(quelle.replace(alt, neu))
    return pfad


def abschnitt5(p: Protokoll) -> bool:
    print("\n5) Mutationsproben: jede Wache einzeln entfernt, die Pruefung MUSS anschlagen")
    ok = True
    for name in MUTATIONEN:
        ergebnis = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--mutation", name],
            capture_output=True, text=True)
        angeschlagen = ergebnis.returncode != 0
        hinweis = "" if angeschlagen else "die Pruefung bestand TROTZ Mutation"
        ok = p.pruefe(f"Abschnitt 5: Mutation '{name}' faellt durch "
                      f"({MUTATIONEN[name][2]})", angeschlagen, hinweis) and ok
        if not angeschlagen:
            print("      " + "\n      ".join(ergebnis.stdout.strip().splitlines()[-6:]))
    return ok


def fuehre_mutation_aus(name: str) -> int:
    """Kindprozess: laedt die MUTIERTE Datei unter dem kanonischen Modulnamen
    und laesst die zugehoerige Pruefung darauf laufen. Rueckgabe 0, wenn die
    Pruefung trotz Mutation bestanden hat - genau das darf nicht passieren."""
    with tempfile.TemporaryDirectory() as tmp:
        pfad = mutiere(name, tmp)
        psa = lade_modul(pfad)
        p = Protokoll()
        welche = MUTATIONEN[name][2]
        if welche == "abschnitt1":
            bestanden = abschnitt1(psa, p)
        elif welche == "abschnitt3":
            bestanden = abschnitt3(psa, p)
        else:
            bestanden = abschnitt4(psa, p, BOTS[0])
        return 0 if bestanden else 1


# ===========================================================================
# Abschnitt 6 - Der Test veraendert nichts
# ===========================================================================
def abschnitt6(p: Protokoll, vorher: str) -> bool:
    print("\n6) Der Testlauf veraendert nichts im Repo")
    nachher = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                              capture_output=True, text=True).stdout
    return p.pruefe("Abschnitt 6: git status unveraendert gegenueber dem Start",
                    nachher == vorher,
                    "\n".join(sorted(set(nachher.splitlines()) ^ set(vorher.splitlines()))))


# ===========================================================================
def main() -> int:
    if "--mutation" in sys.argv:
        return fuehre_mutation_aus(sys.argv[sys.argv.index("--mutation") + 1])

    import param_search_agent as psa

    if "--bot" in sys.argv:
        bot = sys.argv[sys.argv.index("--bot") + 1]
        p = Protokoll(bot)
        abschnitt4(psa, p, bot)
        print(f"\n[{bot}] {p.ok} bestanden, {len(p.fehler)} fehlgeschlagen")
        return 1 if p.fehler else 0

    vorher = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR,
                             capture_output=True, text=True).stdout

    print("=" * 78)
    print("Selbsttest: Zielfunktion von Agent 2 (TB-22)")
    print("=" * 78)

    p = Protokoll()
    abschnitt1(psa, p)
    abschnitt2(psa, p)
    abschnitt3(psa, p)

    # Ein Prozess je Bot - sonst laedt sys.modules still den falschen.
    for bot in BOTS:
        ergebnis = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--bot", bot],
            capture_output=True, text=True)
        print(ergebnis.stdout.rstrip())
        if ergebnis.returncode != 0 and ergebnis.stderr:
            print(ergebnis.stderr.rstrip())
        # Die Einzelpruefungen des Kindes zaehlen mit.
        for zeile in ergebnis.stdout.splitlines():
            if zeile.strip().startswith("[OK ]"):
                p.ok += 1
            elif zeile.strip().startswith("[FEHLER]"):
                p.fehler.append(zeile.strip())
        if ergebnis.returncode != 0 and not any(
                z.strip().startswith("[FEHLER]") for z in ergebnis.stdout.splitlines()):
            p.fehler.append(f"Abschnitt 4 [{bot}]: Kindprozess abgebrochen")

    abschnitt5(p)
    abschnitt6(p, vorher)

    print("\n" + "=" * 78)
    print(f"{p.ok} von {p.ok + len(p.fehler)} Pruefungen bestanden, "
          f"{len(p.fehler)} fehlgeschlagen.")
    for f in p.fehler:
        print(f"  - {f}")
    print("=" * 78)
    return 1 if p.fehler else 0


if __name__ == "__main__":
    sys.exit(main())
