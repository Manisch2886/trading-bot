"""TB-94: traegt den Vollzug von Sperrlistenpunkt 4 (Pfadzeile), die Vollzugsmarke,
neun weitere Marken und Abschnitt 39 in das Register ein.

Rein additiv: jede Einfuegung steht NACH einer eindeutigen Ankerzeile, keine
bestehende Zeile wird veraendert. Zitate werden aus den Fable-Dateien
eingesetzt, nicht abgetippt:
  «Q:<k>:<zeile>»          ganze Zeile als Blockzitat (eigene Zeile der Vorlage)
  «S:<k>:<zeile>:<text>»   Teilzitat; <text> muss in der Quellzeile stehen
Die eingesetzten Zitate werden nach zitate.json geschrieben (fuer e2_zitate.py).

Aufruf aus der Repo-Wurzel:
  trading-env/bin/python3 docs/belege/TB-94/eintrag_register_39.py
"""
import json
import re

REG = "docs/VORREGISTRIERUNG_neuselektion.md"
BELEG = "docs/belege/TB-94/"
VORLAGE = BELEG + "abschnitt39_vorlage.md"
P = "docs/projektfuehrung/"
QUELLEN = {
    "a": P + "FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md",
    "b": P + "FABLE_ANTWORT_2026-09-23b_neurechnung_nach_a.md",
    "c": P + "FABLE_ANTWORT_2026-09-23c_messgroessen_und_vollzug.md",
    "d": P + "FABLE_ANTWORT_2026-09-23d_dritte_leserin_und_eingabestand.md",
    "e": P + "FABLE_ANTWORT_2026-09-23e_nachweislauf_im_modus.md",
    "f": P + "FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md",
    "g": P + "FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md",
}
Q = {k: open(v, encoding="utf-8").read().split("\n") for k, v in QUELLEN.items()}
zitate = []


def _zeile(k, n):
    z = Q[k][int(n) - 1]
    assert z.strip(), (k, n)
    return z


def einsetzen(text, wo):
    def ganz(m):
        k, n = m.group(1), m.group(2)
        z = _zeile(k, n)
        zitate.append({"art": "zeile", "quelle": QUELLEN[k], "zeile": int(n), "wo": wo})
        return z if z.startswith("> ") else "> " + z

    def teil(m):
        k, n, t = m.group(1), m.group(2), m.group(3)
        assert t in _zeile(k, n), (k, n, t[:40])
        zitate.append({"art": "teil", "quelle": QUELLEN[k], "zeile": int(n), "text": t, "wo": wo})
        return t

    text = re.sub(r"^«Q:([a-g]):(\d+)»$", ganz, text, flags=re.M)
    text = re.sub(r"«S:([a-g]):(\d+):(.+?)»", teil, text)
    assert "«" not in text, text[text.index("«"):][:80]
    return text


zeilen = open(REG, encoding="utf-8").read().split("\n")
assert sum("Interpolationsregel**" in z for z in zeilen) == 1


def nach(anker, text, wo, start=None):
    """Fuegt text nach der einzigen Zeile == anker ein (ab Zeile start)."""
    idx = [i for i, z in enumerate(zeilen) if z == anker and (start is None or i >= start)]
    assert len(idx) == 1, (anker[:60], len(idx))
    i = idx[0]
    zeilen[i + 1:i + 1] = einsetzen(text, wo).split("\n")


# --- B1: die Pfadzeile an Punkt 4 (Vollzug, keine Marke) --------------------
nach("   Interpolationsregel**", """\
   — und, als die Tabelle, die der Lauf liest,
   `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (Vollzug der
   Form (ii), 39.2, 23.09.2026)""", "Abschnitt 10 Punkt 4, Pfadzeile")

# --- B2: Vollzugsmarke unter dem Kasten aus 38.4, ohne Leerzeile ------------
nach("   > für `t3_supertrend`).", """\
   >
   > ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026).** Der Punkt nennt jetzt beide
   > Dateien. ⚠️ **Zwei Berichtigungen am Kasten darüber:** (1) Die Tabelle,
   > die der Lauf liest, ist **nicht** `benchmark_drawdowns_vt.json`, sondern
   > die Neurechnung `benchmark_drawdowns_2026-09-23_nach_wegA.json`
   > (`64fb2912…`) — so entschieden in **23b**, nachdem 23a die Bedingung
   > „die Tabelle folgt dem registrierten Faltenplan" gesetzt hatte; `_vt.json`
   > trägt bei `t3_supertrend` eine Falte `2018`, die der Plan seit TB-72 nicht
   > mehr hat. (2) Die zwei offenen Fragen aus 22i sind **beide beantwortet**:
   > das Fertigkriterium in **23a** (berichtigt in 39.1), die Tabelle in
   > **23a/23b** (vollzogen hier). Der Kasten oben ist als Zitat richtig und
   > bleibt unverändert; überholt ist an ihm nur der Dateiname und der Satz
   > „Vollzug steht aus".""", "Abschnitt 10 Punkt 4, Vollzugsmarke")

# --- Marke: 21.9, unter der Tabelle der Folgen (nach der Marke aus 38.7 (d)) -
nach("> Tag. Einzelheiten in **38.7 (d)**.", """
> ⭐⭐ **Berichtigung des Fertigkriteriums (39.1, Fable 23a/23f, TB-94,
> 23.09.2026):** Die offene Frage der Tatsachennotiz darüber ist beantwortet —
> „grün" ist **nicht** Fertigkriterium des Vollzugs, sondern
> **Tag-Vorbedingung**. Der Vollzug (Plan-Punkt 8) ist fertig, wenn unter
> anderem der Absturz weg ist und der Test bis zur Schlusszeile läuft; beides
> ist seit TB-92 erfüllt (`0292e92`: 163/2, `G6`, `H3`). ⚠️ **Die erste Zeile
> der Tabelle oben gilt für den Tag unverändert:** `test_vorregistrierung.py`
> ist rot, offen durch eigene Änderung, blockierend für den Tag — geschlossen
> wird das mit dem Planpunkt „Testannahmen folgen dem Register" (23a; TB-95),
> nicht mit Punkt 8. Die zweite Zeile (Widerspruch zwischen Faltenplan und
> Tabelle) ist mit dem Vollzug geschlossen (39.2, 39.4). Die dritte Zeile ist
> mit 39 **nicht** erledigt (der ERZEUGT-Block in Abschnitt 3 ist nicht neu
> erzeugt, TB-92 A4). Ersatztext in **39.1**.""", "21.9")

# --- Marke: 23.7, unter der Marke aus 38.7 (d) ------------------------------
nach("> bei Fable (Anfrage 22i), nicht entschieden.** Einzelheiten in **38.7 (d)**.", """
> ⭐⭐ **Die Tabelle folgt dem Plan (39.2–39.4, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Sperrlisten-Änderung ist vollzogen — in Form (ii), aber
> **nicht** mit `benchmark_drawdowns_vt.json`: Nach 23a ist die Tabelle, die
> der Lauf liest, auf dem registrierten Faltenplan (33.2) gerechnet, für alle
> neun Bots, ohne Mischung; `_vt.json` trägt bei `t3_supertrend` die leere
> Falte 2018 (vierte Zeile oben). Gelesen wird die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`),
> die `_tb72.json` in allen 9750 Blattwerten reproduziert (39.4). Erledigt sind
> damit die erste Zeile (Vollzug) und die sechste (`registerbericht.py` liest
> `symbole_handelbar_in_falte`, TB-92); aus der fünften ist `G6`/`H3` der
> eigene Planpunkt „Testannahmen folgen dem Register" (39.1, TB-95).
> `benchmark_drawdowns.json` ist byteweise dieselbe Datei (`a163c498…`).""", "23.7")

# --- Marke: 33.2, am Ende des Unterabschnitts -------------------------------
nach("die Marke am Satz selbst steht unter 30.2 (2).", """
> ⭐⭐ **Die Benchmark-Tabelle folgt diesem Plan (39.2/39.4, Fable 23a, TB-94,
> 23.09.2026):** Registertext zu Sperrlistenpunkt 4 / 23 / 33 (23a, Wortlaut in
> **39.2**): Die Tabelle, die der Lauf liest, hat je Bot genau die
> Selektionsfalten dieses Registertexts (plus Bestätigungsperiode) — nicht
> mehr, nicht weniger. Gemessen an der vollzogenen Tabelle gegen den Plan aus
> `faltenplan.py` (`7aa0b8cc…`) im Speicher (TB-91 Block D): **18/18 gleich**,
> Bestätigungszeile 9/9 `2026-01-01/2026-09-01`. Text und Tabelle oben bleiben
> zeichengleich.""", "33.2")

# --- Marke: 37.2, unter der Tatsachennotiz TB-87 ----------------------------
nach("ausweisen) ist Handwerk mit eigener Freigabe; hier nur festgehalten.", """
> ⭐ **Gruppenwechsel und Vollzug (39.3/39.2, Fable 23a/23b, TB-94,
> 23.09.2026):** Die Gruppe „bestimmt" **wechselt** von
> `ergebnisse/benchmark_drawdowns_vt.json` auf die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`) —
> und deren Pfad steht seit 39.2 in Sperrlistenpunkt 4. **Nach dem
> Registertext ist die Gruppe damit leer.** `_vt.json` und `_tb72.json` kommen
> nicht auf die Liste (Tatsachennotizen in 39.3). ⚠️ Die Sonde führt die
> Gruppe als feste Konstante und nennt weiter `_vt.json` mit „Vollzug steht
> aus" (39.3, Ausgabe in 39.9); das zu ändern ist Handwerk mit eigener
> Freigabe.""", "37.2")

# --- Marke: 37.3, unter der Tatsachennotiz zu TB-86 -------------------------
nach("Eintrags, und das alte Abbild bleibt.", """
> ⭐⭐ **Die weiteren Übergänge und ihr Abbild (39.5/39.9, TB-94,
> 23.09.2026):** Nach TB-86 haben sich planmässig bewegt: `faltenplan.py`
> `fd3e5018…` → `7aa0b8cc…` (TB-90, `303a7fd`, Punkt 2), `benchmark.py`
> `3960375a…` → `d6bdd558…` (TB-91, `31008b6`, Punkte 4 und 6),
> `auswertung.py` `1c2e2dae…` → `c3b4e69d…` (TB-92, `0292e92`, Punkte 3, 5
> und 14); dazu `registerbericht.py` und `test_vorregistrierung.py` (TB-92,
> auf keinem Punkt). Auftrag, Freigabe und volle Hashes stehen in **39.5**.
> Geschlossen werden der Fall oben und diese Übergänge mit **einem** neuen
> Abbild (**39.9**); `sperrliste_abbild_2026-09-22.json` bleibt.""", "37.3")

# --- Marke: 37.4, nach dem Randbefund, vor der Marke am alten Ort -----------
nach("vollständig beantwortet „wer liest `herkunft.py`\" er nicht.", """
> ⚠️ **Ergänzung (39.7, Fable 23d, TB-94, 23.09.2026) — `EINGEFROREN` ist nach
> dem Vollzug nicht vollständig:** `EINGEFROREN` hasht weiter
> `ergebnisse/benchmark_drawdowns.json` (historischer Stand), **nicht** die
> Tabelle, die der Lauf liest (`ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json`,
> 39.2). `herkunft.py` bleibt ungeöffnet (`56a1c2e1…`). Der Satz, um den Fable
> diese Tatsachennotiz ergänzt (23d Abschnitt 1 (2)), zeichengleich:
> „«S:d:21:`register()` bezeugt die Abschnitt-0-Menge vom 14.09.; die vollzogene Benchmark-Tabelle bezeugt Sperrlistenpunkt 4 über die Sonde.»"
> Nach Fables Präzisierung zu 36.1 (1) (23c) ist auch jeder Pfad in
> `EINGEFROREN` gesperrt — Wortlaut in **39.7**.""", "37.4")

# --- Marke: 38.4, direkt unter dem Zitat mit „grün" -------------------------
nach([z for z in zeilen if z.startswith("> Vollzug fertig, wenn (Plan-Punkt 8 erweitert):")][0], """
> ⚠️⚠️ **ERSETZT (39.1, Fable 23f, TB-94, 23.09.2026) — das Fertigkriterium im
> Zitat oben:** Fable hat es in **23a** zurückgenommen und in **23f** als
> Berichtigung zu 38.4 adressiert. Es gilt der Ersatztext in **39.1**: Punkt 8
> ist fertig, wenn Registertext (Form (ii)), Tatsachennotiz mit altem und
> neuem Hash, die drei Leser über eine Konstante, der Absturz weg und
> `test_vorregistrierung.py` **läuft durch bis zur Schlusszeile**,
> Modus-Nachweis bytegleich, neues Abbild, Sonde 0 für die Pfade. **Der
> Ausgang einzelner Prüfungen ist nicht Fertigkriterium von Punkt 8**; „null
> rote Prüfungen" bleibt Tag-Vorbedingung (21.9, 23a). Das Zitat oben bleibt
> zeichengleich. TB-92 hat sich an dieses Zitat gehalten und abgebrochen —
> richtig (39.1).""", "38.4, unter dem Zitat mit grün")

# --- Marke: 38.4, am Ende ---------------------------------------------------
nach("*„Form steht fest, Vollzug steht aus\"*.", """
> ⭐⭐ **VOLLZOGEN (39.2, TB-94, 23.09.2026):** Form (ii) ist vollzogen — Punkt
> 4 nennt `ergebnisse/benchmark_drawdowns.json` (`a163c498…`, historischer
> Stand, unverändert) **und** die Tabelle, die der Lauf liest: ⚠️ **nicht**
> `_vt.json`, wie Fables Formtext oben sagt, sondern die Neurechnung
> `ergebnisse/benchmark_drawdowns_2026-09-23_nach_wegA.json` (`64fb2912…`,
> 23a/23b, TB-91). Beide offenen Fragen dieses Abschnitts sind beantwortet:
> „grün" (39.1) und die Tabelle für `t3_supertrend` (39.2). Die Tatsachennotiz
> TB-88 oben (die drei Leser lesen die alte Datei, alter Schlüssel) ist durch
> TB-92 (`0292e92`) überholt: sie lesen die Neurechnung über
> `auswertung.BENCHMARK_TABELLE`, `registerbericht.py` liest
> `symbole_handelbar_in_falte` (39.2). Der Text oben bleibt zeichengleich.""", "38.4, am Ende")

# --- Marke: 38.7 (d), unter der offenen Frage -------------------------------
nach("darf eine offene Frage tragen — 21.6 hat es vorgemacht.*", """
> ⭐⭐ **BEANTWORTET (39.1, Fable 23a/23f, TB-94, 23.09.2026):** Lesart **(1)**
> — Plan-Punkt 8 ist fertig, wenn der Absturz weg ist und der Test bis zur
> Schlusszeile läuft; `G6`/`H3` sind der eigene Planpunkt „Testannahmen folgen
> dem Register" (23a), Tag-Vorbedingung, nicht Punkt 8. Das Fertigkriterium in
> 38.4 ist durch den Ersatztext in 39.1 berichtigt. Gemessen am echten Stand
> (TB-92, `0292e92`): Absturz weg, Schlusszeile erreicht, **163/2** (`G6`,
> `H3`) — dieselben zwei wie in der Simulation oben. Die Frage oben bleibt
> zeichengleich stehen.""", "38.7 (d)")

# --- Abschnitt 39 anhaengen ---------------------------------------------------
abschnitt = einsetzen(open(VORLAGE, encoding="utf-8").read(), "Abschnitt 39")
text = "\n".join(zeilen)
assert text.endswith("\n")
text = text + "\n" + abschnitt.lstrip("\n")
assert text.endswith("\n") and not text.endswith("\n\n")
open(REG, "w", encoding="utf-8").write(text)
json.dump(zitate, open(BELEG + "zitate.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok: %d Zitate (%d Zeilen, %d Teilzitate)" % (
    len(zitate), sum(z["art"] == "zeile" for z in zitate), sum(z["art"] == "teil" for z in zitate)))
