import json, os, sys
sys.path.insert(0, "research/universum_trockenlauf")
import universum_trockenlauf as ut
aus = {}
for bot in ut.BOTS:
    roh = ut.messe_bot(bot, ["2026-08-31T23:59:59", "9999-12-31T23:59:59"])
    if roh["fehler"]:
        aus[bot] = {"fehler": roh["fehler"]}; continue
    m = {l["stichtag"]: sorted(l["symbole"]) for l in roh["laeufe"]}
    fe, de = m["2026-08-31T23:59:59"], m["9999-12-31T23:59:59"]
    aus[bot] = {"faltenende_2026-08-31T23:59:59": len(fe), "datenende": len(de),
                "gleiche_menge": fe == de, "nur_datenende": sorted(set(de) - set(fe)),
                "nur_faltenende": sorted(set(fe) - set(de)), "universum": len(roh["schranken"]["SYMBOLE"])}
    print(bot, aus[bot], flush=True)
json.dump(aus, open(sys.argv[1], "w"), indent=1)
