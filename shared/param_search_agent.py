"""
Agent 2: Intelligente Parameter-Suche
==========================================
Ersetzt das erschoepfende Grid-Search (jede Kombination durchprobieren)
durch einen iterativen Ansatz: Claude bekommt die bisherigen Testergebnisse
gezeigt und schlaegt gezielt die naechste, vielversprechendste Kombination
vor - aehnlich wie ein erfahrener Quant, der nicht stur jede Zahl testet,
sondern aus Zwischenergebnissen lernt.

Vorteil ggue. Grid-Search: bei grossen Parameterraeumen (z.B. 5+ Parameter)
waechst die Anzahl Kombinationen exponentiell - der Agent kann oft mit
deutlich weniger Testlaeufen zu einem guten Ergebnis kommen.

Nachteil: nicht erschoepfend - der Agent koennte eine gute Kombination
uebersehen, die Grid-Search gefunden haette. Fuer eine finale,
vertrauenswuerdige Validierung bleibt Grid-Search + Walk-Forward der
Goldstandard - dieser Agent eignet sich gut, um VOR einem vollen
Grid-Search schnell einen vielversprechenden Bereich einzugrenzen.

ZIELGROESSE DER AUSWAHL (TB-22)
------------------------------------------------------------------------
Bis TB-22 lief die Auswahl ueber `robustness_score` - und der steckt den
Drawdown der aneinandergehaengten SYMBOL-BLOECKE ein, nicht den der
chronologischen Reihenfolge. `research/drawdown_reihenfolge/` hat gemessen,
dass dieses Mass bei drei Bots NEGATIV mit dem echten Kapital-Drawdown aus
`equity_simulation.py` rangkorreliert (rsi2_mean_reversion -0,314,
volatility_breakout -0,200, turtle_soup_crypto -0,333), waehrend die
chronologische Reihenfolge dort 0,69 bis 0,83 erreicht. Bei keinem Bot lag
das alte Mass naeher am Kapital-Drawdown.

Fuer AUSGABEN und BERICHTE gilt im Repo die Uebergangsregel "beide Masse
ausweisen". Agent 2 ist davon die benannte Ausnahme: er gibt keine Zahl
aus, er trifft eine AUSWAHL. Eine Auswahl auf einem Mass, das dem Ziel
entgegenlaeuft, ist kein Informationsverlust, sondern ein Fehler mit
Vorzeichen. Er waehlt deshalb nach `robustness_score_chronologisch` -
derselben Formel, nur auf `max_drawdown_chronologisch_pct` gerechnet, das
`multi_symbol_optimise.evaluate_combination_multi` seit PR #90 mitliefert.

Beide Zahlen stehen dem Modell in der Ergebnistabelle vor Augen, und der
Prompt sagt ausdruecklich, welche gilt - ein Modell, das den Unterschied
sieht, kann in seiner Begruendung darauf eingehen. Die AUSWAHL selbst
trifft aber Code (`max(...)` am Ende von `run_agent_search`), nicht das
Modell, und genau derselbe Wert steht im Prompt: Prompt und Auswahl
koennen so nicht auseinanderlaufen.

DIE ZIELGROESSE SEIT TB-30a (14.09.2026) - DER KAPITAL-DRAWDOWN FUEHRT
------------------------------------------------------------------------
Seit TB-22 waehlt dieser Agent auf dem CHRONOLOGISCHEN Drawdown, und der
Satz "es gilt das chronologische" stand fest verdrahtet im Prompt. Mit der
Festlegung des Betreibers vom 14.09.2026 ist das ueberholt: fuehrendes Mass
ist der **Kapital-Drawdown aus `equity_simulation.py`** - der Drawdown des
Kapitalpfades, den jemand tatsaechlich erlebt haette, einschliesslich
Positionsgroessen, Positionslimit und Zuteilung.

Der chronologische Drawdown war der beste verfuegbare STELLVERTRETER dafuer
(`research/drawdown_reihenfolge/` misst Rangkorrelationen von 0,69 bis 0,83
gegen den Kapital-Drawdown, waehrend das Block-Mass bei drei Bots NEGATIV
korreliert). Ein Stellvertreter bleibt er trotzdem, und wo das Original
vorliegt, waehlt man nicht auf dem Stellvertreter.

Die Auswahl laeuft deshalb jetzt ueber eine dreistufige Kaskade, und der
Prompt sagt in jeder Stufe, WELCHES Mass gilt und WARUM nicht das
fuehrende:

  1. `robustness_score_kapital`        auf `max_drawdown_kapital_pct`
     - das fuehrende Mass. Gilt, sobald das Feld in den Ergebnissen steht.
  2. `robustness_score_chronologisch`  auf `max_drawdown_chronologisch_pct`
     - der Stellvertreter. Gilt, solange das fuehrende Feld fehlt.
  3. `robustness_score`                auf `max_drawdown_pct`
     - der Notweg, wenn auch der Stellvertreter fehlt.

**Heute greift Stufe 2**, weil `multi_symbol_optimise.evaluate_combination_multi`
den Kapital-Drawdown noch nicht mitliefert; das nachzuruesten ist TB-30b und
faellt nicht in eine Aenderung an `shared/`. Der Unterschied zu vorher ist
nicht die Zahl, sondern dass der Agent den Ersatz jetzt ALS Ersatz ausweist
statt ihn als Zielgroesse zu behaupten - und dass er von selbst auf das
fuehrende Mass umschaltet, sobald es da ist, ohne dass jemand daran denken
muss.

Was diese Aenderung NICHT anfasst: der Agent aendert weiterhin nichts
automatisch. Seine Vorschlaege sind und bleiben UNVALIDIERT (der
Pflichthinweis dazu steht fest verdrahtet in `shared/empfehlung_format.py`)
und brauchen Walk-Forward, bevor etwas uebernommen wird. Geaendert hat
sich, WORAUF er schaut - nicht, was er darf.
"""

import json
import pandas as pd

from claude_client import call_claude, extract_json

# --- Die Zielgroesse, an genau einer Stelle ------------------------------
# Feldnamen als Konstanten, weil sie an drei Stellen gebraucht werden:
# in der Rechnung, im Prompt und in der Ausgabe. Ein von Hand abgetippter
# Feldname im Prompt koennte von der Rechnung wegdriften - in diesem Repo
# sind doppelt gefuehrte Zahlen schon einmal unbemerkt auseinandergelaufen.
FELD_DRAWDOWN_BLOCK = "max_drawdown_pct"
FELD_DRAWDOWN_CHRONO = "max_drawdown_chronologisch_pct"
FELD_DRAWDOWN_KAPITAL = "max_drawdown_kapital_pct"
FELD_SCORE_BLOCK = "robustness_score"
FELD_SCORE_CHRONO = "robustness_score_chronologisch"
FELD_SCORE_KAPITAL = "robustness_score_kapital"

# Die Kaskade der Zielgroessen, vom fuehrenden Mass abwaerts. Die Reihenfolge
# steht an genau EINER Stelle; Prompt, Auswahl und Ausgabe lesen sie von hier.
# Jede Stufe: (Modus, Score-Feld, Drawdown-Feld, kurze Kennzeichnung).
ZIELMASS_KASKADE = (
    ("kapital", FELD_SCORE_KAPITAL, FELD_DRAWDOWN_KAPITAL,
     "der Kapital-Drawdown aus equity_simulation.py"),
    ("chronologisch", FELD_SCORE_CHRONO, FELD_DRAWDOWN_CHRONO,
     "der Drawdown auf der chronologischen Reihenfolge der Trades"),
    ("ersatzweise", FELD_SCORE_BLOCK, FELD_DRAWDOWN_BLOCK,
     "der Drawdown auf den aneinandergehaengten Symbol-Bloecken"),
)

# Kurzform der Formel - dieselbe wie multi_symbol_optimise.calculate_
# robustness_score, nur mit einem anderen Drawdown im Nenner. WELCHER
# Drawdown, entscheidet die Kaskade; `zielmass_baustein()` und
# `zielmass_zeile()` setzen ihn deshalb selbst ein statt diese Konstante zu
# benutzen. Sie bleibt fuer Aufrufer von aussen erhalten und nennt
# ausdruecklich das fuehrende Mass.
FORMEL_TEXT = (f"avg_return_pct x Wurzel(num_trades) / |{FELD_DRAWDOWN_KAPITAL}|")


def chronologischer_score(zeile: dict):
    """Der robustness_score auf der CHRONOLOGISCHEN Reihenfolge.

    Wortgleich zu multi_symbol_optimise.calculate_robustness_score - bis
    auf den Drawdown im Nenner. Bewusst hier gerechnet und nicht in
    multi_symbol_optimise ergaenzt: dort wuerde eine zweite Score-Spalte
    in jede Rasterausgabe und jede results/*.csv wandern und damit die
    Rangfolge der Rastersuche beruehren, die TB-18 ausdruecklich
    unveraendert gelassen hat. Alle Bestandteile stehen in der
    Ergebniszeile.

    Gibt None zurueck, wenn die Zeile die noetigen Felder nicht hat -
    dann ist der Wert nicht ableitbar, und der Aufrufer muss das sehen,
    statt eine stillschweigend falsche Zahl zu bekommen.
    """
    return score_auf(zeile, FELD_DRAWDOWN_CHRONO)


def kapital_score(zeile: dict):
    """Derselbe Score auf dem KAPITAL-Drawdown - dem fuehrenden Mass.

    Er ist erst berechenbar, wenn die Ergebniszeile
    `max_drawdown_kapital_pct` mitbringt. Dass sie das heute nicht tut, ist
    kein Grund, ihn wegzulassen: sobald TB-30b das Feld nachruestet, waehlt
    der Agent ohne weiteres Zutun auf dem fuehrenden Mass.
    """
    return score_auf(zeile, FELD_DRAWDOWN_KAPITAL)


def score_auf(zeile: dict, drawdown_feld: str):
    """Die Score-Formel, an einer Stelle, mit dem Drawdown-Feld als Argument.

    Gibt None zurueck, wenn die Zeile die noetigen Felder nicht hat - dann
    ist der Wert nicht ableitbar, und der Aufrufer muss das sehen, statt
    eine stillschweigend falsche Zahl zu bekommen.
    """
    drawdown = zeile.get(drawdown_feld)
    avg_return = zeile.get("avg_return_pct")
    num_trades = zeile.get("num_trades")
    if drawdown is None or avg_return is None or num_trades is None:
        return None
    drawdown_penalty = abs(drawdown) if drawdown != 0 else 1.0
    return round((avg_return * (num_trades ** 0.5)) / drawdown_penalty, 3)


def mit_zielgroesse(zeile: dict) -> dict:
    """Ergebniszeile plus ALLEN Zielgroessen der Kaskade.

    Die Zeile des Bots bleibt unveraendert - die neuen Werte kommen als
    zusaetzliche Felder dazu, damit die Masse nebeneinander in der Tabelle
    stehen, die das Modell zu sehen bekommt. Welches davon GILT, sagt der
    Prompt; die Auswahl selbst trifft Code."""
    ergaenzt = dict(zeile)
    ergaenzt[FELD_SCORE_KAPITAL] = kapital_score(zeile)
    ergaenzt[FELD_SCORE_CHRONO] = chronologischer_score(zeile)
    return ergaenzt


def zielmass_verfuegbar(history: list, feld: str = FELD_SCORE_CHRONO) -> bool:
    """Traegt mindestens eine Ergebniszeile diesen Score?"""
    return any(h.get(feld) is not None for h in history)


def zielmass_modus(history: list) -> str:
    """Die hoechste Stufe der Kaskade, die in DIESEN Ergebnissen vorliegt.

    Ohne Ergebnisse gilt die zweite Stufe: das fuehrende Mass steht heute in
    keiner Rasterausgabe, und die erste Stufe zu behaupten, bevor das Feld
    existiert, waere ein Prompt, der auf eine leere Spalte zeigt. Sobald eine
    einzige Zeile `max_drawdown_kapital_pct` mitbringt, schaltet der Agent um
    - ohne dass jemand daran denken muss.

    Der Ersatzweg ist nie stillschweigend: die gewaehlte Stufe steht im
    Prompt, in der Ausgabe und im Rueckgabewert von `run_agent_search`.
    """
    for modus, feld, _, _ in ZIELMASS_KASKADE:
        if zielmass_verfuegbar(history, feld):
            return modus
    return "chronologisch" if not history else "ersatzweise"


def kaskadenstufe(modus: str) -> tuple:
    """(Score-Feld, Drawdown-Feld, Kennzeichnung) zu einem Modus."""
    for m, score, drawdown, text in ZIELMASS_KASKADE:
        if m == modus:
            return score, drawdown, text
    raise ValueError(f"Unbekannter Zielmass-Modus: {modus}")


def zielmass_baustein(modus: str) -> str:
    """Der Abschnitt im Prompt, der sagt, welches Mass gilt - und, wenn es
    nicht das fuehrende ist, WARUM nicht.

    Aus den Feldnamen-Konstanten gebaut, nicht abgetippt: ein von Hand
    geschriebener Feldname im Prompt koennte von der Rechnung wegdriften.
    """
    score, drawdown, kennzeichnung = kaskadenstufe(modus)
    fuehrend_score, fuehrend_dd, fuehrend_text = kaskadenstufe("kapital")

    kopf = ("ZIELGROESSE DER AUSWAHL:\n"
            f"Massgeblich ist ausschliesslich '{score}' - der Score "
            f"avg_return_pct x Wurzel(num_trades) / |{drawdown}|. "
            "Je hoeher dieser Wert, desto besser.\n")

    if modus == "kapital":
        return kopf + (
            f"'{drawdown}' ist das FUEHRENDE MASS: {kennzeichnung} - der "
            "Drawdown des Kapitalpfades, den jemand tatsaechlich erlebt "
            "haette, einschliesslich Positionsgroessen, Positionslimit und "
            "Zuteilung.\n"
            f"'{FELD_SCORE_CHRONO}', '{FELD_SCORE_BLOCK}' und die "
            "zugehoerigen Drawdowns stehen in der Tabelle weiterhin zum "
            "Vergleich. Sie sind NICHT das Auswahlkriterium; wenn die Masse "
            "in verschiedene Richtungen zeigen, gilt das fuehrende.")

    if modus == "chronologisch":
        return kopf + (
            f"ACHTUNG: '{fuehrend_dd}' - das fuehrende Mass, {fuehrend_text} "
            "- liegt in diesen Ergebnissen NICHT vor. Gewaehlt wird deshalb "
            f"auf dem STELLVERTRETER, und das ist {kennzeichnung}. Er ist der "
            "beste verfuegbare "
            "Naeherungswert (Rangkorrelation 0,69 bis 0,83 gegen den "
            "Kapital-Drawdown, gemessen in research/drawdown_reihenfolge/), "
            "aber er ist nicht das Ziel selbst.\n"
            f"'{FELD_SCORE_BLOCK}' und '{FELD_DRAWDOWN_BLOCK}' stehen in der "
            "Tabelle weiterhin zum Vergleich. Sie rechnen den Drawdown auf "
            "der Reihenfolge der aneinandergehaengten Symbol-Bloecke - das "
            "ist kein Verlauf, den jemand haette erleben koennen, sondern ein "
            "Nebenprodukt der Art, wie die Teilergebnisse zusammengefuegt "
            "werden. Sie sind NICHT das Auswahlkriterium.")

    return kopf + (
        f"ACHTUNG: Weder '{fuehrend_dd}' (das fuehrende Mass, {fuehrend_text}) "
        f"noch '{FELD_DRAWDOWN_CHRONO}' (der Stellvertreter) liegen in diesen "
        f"Ergebnissen vor. Gewaehlt wird deshalb ersatzweise auf dem NOTWEG, "
        f"und das ist {kennzeichnung}. Dieses Mass ist nachweislich "
        "schlechter auf den "
        "echten Kapitalverlauf ausgerichtet - bei drei der neun Bots "
        "korreliert es sogar NEGATIV mit ihm. Die Auswahl ist entsprechend "
        "schwaecher begruendet, und das gehoert in jede Begruendung hinein.")


SYSTEM_PROMPT = f"""Du bist ein erfahrener quantitativer Trading-Analyst, der
eine Trading-Strategie durch iteratives Testen von Parameter-Kombinationen
optimiert.

Du bekommst:
1. Eine Beschreibung der Parameter (Name, Typ, erlaubter Bereich)
2. Die Zielgroesse, nach der ausgewaehlt wird
3. Eine Tabelle bereits getesteter Kombinationen mit ihren Ergebnissen

Deine Aufgabe: schlage die NAECHSTE Kombination vor, die am ehesten zu
einer robusten Verbesserung fuehrt. Beruecksichtige dabei:
- Richte dich nach dem Abschnitt "ZIELGROESSE DER AUSWAHL" und der dort
  genannten Groesse - nicht nach der hoechsten Rendite und nicht nach
  einem anderen Drawdown-Mass in der Tabelle
- Auch die Trade-Anzahl zaehlt (mehr = verlaesslicher)
- Wenn ein Parameter-Bereich durchgehend schlecht abschneidet, meide ihn
- Wenn sich ein Muster abzeichnet (z.B. "kleinere Stop-Loss-Werte werden
  konsistent besser"), verfeinere in diese Richtung
- Vermeide, eine bereits getestete Kombination zu wiederholen

Antworte NUR mit einem JSON-Objekt, kein zusaetzlicher Text:
{{
  "action": "test" oder "stop",
  "params": {{<parametername>: <wert>, ...}},
  "reasoning": "kurze Begruendung, maximal 15 Woerter"
}}

WICHTIG: Halte "reasoning" WIRKLICH kurz (max. 15 Woerter) - eine zu
lange Begruendung kann dazu fuehren, dass die Antwort abgeschnitten
wird und nicht mehr als gueltiges JSON gelesen werden kann.

"stop" nur waehlen, wenn du nach mehreren Iterationen ueberzeugt bist,
dass keine weitere Verbesserung mehr zu erwarten ist.
"""


def format_param_spec(param_spec: dict) -> str:
    lines = []
    for name, spec in param_spec.items():
        if "options" in spec:
            lines.append(f"- {name} ({spec['type']}): eine der Optionen {spec['options']}")
        else:
            lines.append(f"- {name} ({spec['type']}): Bereich {spec['range']}, "
                          f"Schrittweite {spec.get('step', 'beliebig')}")
    return "\n".join(lines)


def format_history(history: list) -> str:
    if not history:
        return "(noch keine Ergebnisse - das ist der erste Test)"
    df = pd.DataFrame(history)
    return df.to_string(index=False)


def zielmass_zeile(ergebnis: dict) -> str:
    """Ein Satz fuer die Ausgabe: worauf wurde ausgewaehlt, und mit welchen
    Zahlen. Fest verdrahtet, nicht vom Modell formuliert - aus demselben
    Grund, aus dem der Unvalidiert-Pflichthinweis in
    shared/empfehlung_format.py eine Konstante ist: ein Modell koennte die
    Angabe variieren, abschwaechen oder vergessen, ein Konstanten-String
    nicht. Ohne diese Angabe entstuende eine Ebene hoeher dasselbe Problem:
    ein Vorschlag, dessen Grundlage niemand mehr nachvollziehen kann."""
    zielmass = ergebnis.get("zielmass") or {}
    modus = zielmass.get("modus", "chronologisch")
    best = ergebnis.get("best")
    score, drawdown, kennzeichnung = kaskadenstufe(modus)

    satz = (f"Auswahl-Zielgroesse: {score} "
            f"(avg_return_pct x Wurzel(num_trades) / |{drawdown}|); "
            f"im Nenner steht {kennzeichnung}.")
    if modus != "kapital":
        satz += (f" ERSATZWEISE: {FELD_DRAWDOWN_KAPITAL}, das fuehrende Mass, "
                 f"lag in diesen Ergebnissen nicht vor.")

    if best is None:
        return satz + " Kein gueltiges Ergebnis, also keine Auswahl getroffen."

    vergleich = ", ".join(
        f"{feld}={best.get(feld)}" for _, feld, _, _ in ZIELMASS_KASKADE)
    return (f"{satz} Gewaehlt mit {best.get(score)}; zum Vergleich "
            f"{vergleich} - die uebrigen sind NICHT Auswahlgrundlage.")


def run_agent_search(evaluate_fn, param_spec: dict, seed_combos: list = None,
                      max_iterations: int = 15, call_fn=None) -> dict:
    """
    evaluate_fn: Funktion, die ein dict von Parametern annimmt und ein
                 Ergebnis-dict zurueckgibt (oder None, falls die
                 Kombination die Mindestkriterien nicht erfuellt).
    param_spec:  Beschreibung des Parameterraums (siehe format_param_spec).
    seed_combos: optionale Start-Kombinationen, die zuerst getestet werden,
                 bevor der Agent uebernimmt (z.B. sinnvolle Standardwerte).
    call_fn:     der Sendeweg zum Modell. Standard ist call_claude; der
                 Selbsttest reicht hier eine Attrappe herein und kommt damit
                 ohne einen einzigen echten API-Aufruf aus.

    Rueckgabe: {"history": [...alle Ergebnisse...],
                "best": {...bestes Ergebnis...},
                "zielmass": {...worauf ausgewaehlt wurde...}}

    Ausgewaehlt wird nach der chronologischen Zielgroesse - siehe
    Modul-Docstring. Der Agent aendert dabei weiterhin nichts automatisch.
    """
    senden = call_fn if call_fn is not None else call_claude
    history = []

    # Start-Kombinationen testen (falls angegeben)
    if seed_combos:
        print(f"Teste {len(seed_combos)} Start-Kombinationen...")
        for combo in seed_combos:
            result = evaluate_fn(combo)
            if result is not None:
                result = mit_zielgroesse(result)
                history.append(result)
                print(f"  {combo} -> {result.get(FELD_SCORE_CHRONO, 'n/a')}")

    param_spec_text = format_param_spec(param_spec)

    for iteration in range(1, max_iterations + 1):
        print(f"\n--- Agent-Iteration {iteration}/{max_iterations} ---")

        user_message = (
            f"PARAMETER-RAUM:\n{param_spec_text}\n\n"
            f"{zielmass_baustein(zielmass_modus(history))}\n\n"
            f"BISHERIGE ERGEBNISSE:\n{format_history(history)}\n\n"
            f"Schlage die naechste Kombination vor."
        )

        # thinking bewusst deaktiviert: reine JSON-Textsynthese ohne Tool-Use.
        # MODEL_SONNET (claude-sonnet-5, Standardmodell von call_claude())
        # faehrt sonst automatisch "adaptive" Extended Thinking, deren
        # Tokens sich das max_tokens-Budget mit der sichtbaren Antwort
        # teilen - bei knappem Limit kann das Modell dadurch das komplette
        # Budget "wegdenken", bevor ueberhaupt JSON-Text entsteht (siehe
        # portfolio_interpreter_agent.py, wo genau dieser Fall live auftrat).
        response = senden(SYSTEM_PROMPT, user_message, max_tokens=1000,
                           thinking={"type": "disabled"})

        if not response["success"]:
            print(f"  Agent-Aufruf fehlgeschlagen: {response['error']}")
            print("  Breche Agent-Suche ab, nutze bisher gefundene Ergebnisse.")
            break

        if response.get("stop_reason") == "max_tokens":
            raw = response.get("raw")
            block_types = ([getattr(b, "type", "?") for b in raw.content] if raw is not None
                            else "unbekannt (kein raw-Objekt)")
            print(f"  Warnung: Antwort bei max_tokens abgeschnitten ({len(response['text'])} "
                  f"Zeichen sichtbarer Text, Content-Block-Typen: {block_types}) - kann kein "
                  f"gueltiges JSON sein, ueberspringe diese Iteration.")
            continue

        decision = extract_json(response["text"])
        if decision is None:
            print(f"  Konnte Antwort nicht als JSON lesen.")
            print(f"  Textlaenge: {len(response['text'])} Zeichen, "
                  f"stop_reason: {response.get('stop_reason', 'unbekannt')}")
            if response["text"]:
                print(f"  Roher Text: {response['text'][:300]}")
            continue

        if decision.get("action") == "stop":
            print(f"  Agent stoppt: {decision.get('reasoning', '(keine Begruendung)')}")
            break

        params = decision.get("params", {})
        reasoning = decision.get("reasoning", "")
        print(f"  Teste: {params}")
        print(f"  Begruendung: {reasoning}")

        result = evaluate_fn(params)
        if result is None:
            print("  -> Kombination erfuellt Mindestkriterien nicht (z.B. zu wenige Trades)")
            history.append({**params, FELD_SCORE_BLOCK: None, FELD_SCORE_CHRONO: None,
                             "note": "unterhalb Mindestkriterien"})
        else:
            result = mit_zielgroesse(result)
            history.append(result)
            print(f"  -> Score: "
                  f"{result.get(FELD_SCORE_KAPITAL, 'n/a')} (Kapital) / "
                  f"{result.get(FELD_SCORE_CHRONO, 'n/a')} (chronologisch)")

    # Die Auswahl. Sie laeuft ueber die hoechste Stufe der Kaskade, die in
    # DIESEN Ergebnissen vorliegt - fuehrendes Mass, sonst Stellvertreter,
    # sonst Notweg. Keine Stufe wird stillschweigend genommen: sie steht im
    # Prompt, in der Ausgabe und im Rueckgabewert.
    modus = zielmass_modus(history)
    schluessel, drawdown_feld, kennzeichnung = kaskadenstufe(modus)
    valid_results = [h for h in history if h.get(schluessel) is not None]
    best = max(valid_results, key=lambda r: r[schluessel]) if valid_results else None

    ergebnis = {
        "history": history,
        "best": best,
        "zielmass": {
            "modus": modus,
            "feld": schluessel,
            "drawdown_feld": drawdown_feld,
            "kennzeichnung": kennzeichnung,
            "ist_fuehrendes_mass": modus == "kapital",
        },
    }
    print(f"\n{zielmass_zeile(ergebnis)}")
    return ergebnis
