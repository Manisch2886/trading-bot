#!/usr/bin/env python3
"""TB-119 Schritt C - 13 Regeln mit Status FEHLT aus docs/belege/TB-118/d2_fehlende_regeln.txt (ohne 19/6) ins
Regelwerk, Wortlaut an der Fundstelle in der Uebergabe nachgelesen (nicht aus der Kurzfassung in d2). C2: 19/6 als
Frage an die Fable-Sammlung, Abschnitt D, nur angehaengt. Aufruf aus der Repo-Wurzel: [--probe | --nur-protokoll <c>]
Nummern in PRUEFPRINZIPIEN gemessen (K2i): hoechste vorhandene A8, B6, C7 -> A9, A10, B7, C8."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from einsetzen_lib import einsetzen  # noqa: E402

AW = "docs/projektfuehrung/ARBEITSWEISE.md"
PP = "docs/PRUEFPRINZIPIEN.md"
FS = "docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md"
U19 = "`projektfuehrung/UEBERGABE_2026-09-19.md`"
U24 = "`projektfuehrung/UEBERGABE_2026-09-24.md`"

# ---------------------------------------------------------------- ARBEITSWEISE 14: 21b/1, 21b/5, 24/6
AW_14_ALT = "über die Frage selbst existiert nicht.\n\n---\n\n## 15. Was mit"
AW_14_NEU = """über die Frage selbst existiert nicht.

### ⭐ Schreiben auf Dateien und Nachträge — drei Regeln aus den Übergaben (TB-119, 27.09.2026)

*Sie standen bis zum 27.09.2026 nur in den Fehlertabellen alter Übergaben
(Bestandsaufnahme TB-118 D2, `docs/belege/TB-118/d2_fehlende_regeln.txt`, Status
FEHLT). Der Wortlaut ist an der Fundstelle nachgelesen, nicht aus der Kurzfassung
übernommen.*

| | Regel | Anlass | Herkunft |
|---|---|---|---|
| **1** | ⭐⭐ **Vor jedem Schreiben auf eine vorhandene Datei wird sie gelesen, nicht angenommen.** | `AKTUELLER_AUFTRAG.md` hatte 87 Zeilen und wurde mit einer Zeile überschrieben, ohne sie anzusehen (`numstat` `1 86`). *Verloren war nichts, weil git die Fassung hielt — das war Glück, nicht Verfahren* | %(u19)s, Block 7 (Fassung 21.09. abends), Nr. 1 — D2 21b/1 |
| **2** | ⭐ **Ein Nachtrag, der eine Sitzung nicht mehr erreicht, wird zum Auftrag** und geht nach `docs/auftraege/`, **bevor** er in `logs/` altert | Der Nachtrag TB-78b erreichte eine bereits abgeschlossene Sitzung nicht; er lag in `logs/auftraege/`, **kein Träger**. Aus ihm wurde TB-79 | ebd., Nr. 5 — D2 21b/5 |
| **3** | **Hilfsdateien werden nicht im Repo gelassen; aufgeräumt wird über `device_request_delete_permission`** | Hilfsdateien im Repo gelassen | %(u24)s, Block 8, Nr. 6 — D2 24/6 |

⚠️ *Zu 1:* Die Schwesterregel „nie überschreiben, immer neuer Dateiname, danach
mit `wc -c` und `grep` nachprüfen“ (%(u19)s, Block 7, Nr. 7 — D2 19/7) steht
im Regelwerk nur **teilweise** und bleibt nach dem Auftrag TB-119 so, wie sie ist.
*Zu 3:* `device_request_delete_permission` ist ein Werkzeug der Geräteanbindung;
Block 8 der Übergabe vom 24.09. führt die Fehler des steuernden Chats — die Regel
richtet sich an ihn (erschlossen aus der Herkunft, nicht gemessen). Für eine
Mac-Sitzung gilt weiter Abschnitt 6: nichts löschen, ohne vorher zu fragen.

---

## 15. Was mit""" % {"u19": U19, "u24": U24}

# ---------------------------------------------------------------- ARBEITSWEISE 15: 21/1, 21/2, 21/3, 21/7, 24/R2, 21/6
AW_15_ALT = "stillschweigend getroffen.\n\n---\n\n## 16. Dokumentation aktuell halten"
AW_15_NEU = """stillschweigend getroffen.

### ⭐ Der Austausch mit dem Verfahrensprüfer — sechs Regeln aus den Übergaben (TB-119, 27.09.2026)

*Sie standen bis zum 27.09.2026 nur in den Fehlertabellen alter Übergaben
(Bestandsaufnahme TB-118 D2, `docs/belege/TB-118/d2_fehlende_regeln.txt`, Status
FEHLT). Der Wortlaut ist an der Fundstelle nachgelesen, nicht aus der Kurzfassung
übernommen.*

| | Regel | Anlass | Herkunft |
|---|---|---|---|
| **1** | ⭐ **Nach jeder Fable-Antwort werden die laufenden Aufträge gegen sie geprüft, nicht nur die kommenden.** Ein Nachtrag in die laufende Sitzung ist billiger als eine Berichtigung im Register | Ein Auftrag lief mit einer überholten Prämisse: TB-77 wies einen Platzhalter fürs append-only-Register an, während der Wert dort seit dem 19.09. als Tatsache stand. Fables Antwort 21b hob den Blocker auf, als der Auftrag schon lief | %(u19)s, Block 7 (Fassung 21.09.), Nr. 1 — D2 21/1 |
| **2** | ⭐ **Wo ein Aktenzeichen genannt wird, steht der Wortlaut daneben** — Fables eigene Regel, auf uns angewandt | Eine Kette mit falschem Aktenzeichen in einem Auftrag; Fable stellte in 21b klar, dass keine Festlegung den Satz trägt | ebd., Nr. 2 — D2 21/2 |
| **3** | ⭐ **Ein Übergabetext bekommt eine Fassungszeile im Sendetext selbst**, nicht nur im Rahmendokument. Sonst ist von aussen nicht unterscheidbar, welche Fassung jemand hat | Ein Übergabetext an Fable ging hinaus, dessen vier Fragen er schon beantwortet hatte; die Antwort lag seit einer Stunde vor | ebd., Nr. 3 — D2 21/3 |
| **4** | ⭐⭐ **Eine Berichtigung von Fable wird gemessen wie jede andere Behauptung — gerade dann, wenn sie uns berichtigt.** Wer sagt „ich kann die Quelle nicht lesen“, liefert damit den Grund, seine Quellenangabe zu prüfen, nicht sie zu übernehmen | Fables Berichtigung einer Kette ungeprüft in einen Auftrag geschrieben, obwohl er im selben Absatz sagte, er könne das Register nicht lesen. Der Auftrag hätte die richtige Kette zerstört | ebd., Ergänzung „Ein siebter Fehler für Block 7“, Nr. 7 — D2 21/7 |
| **5** | ⭐ **Eine Fable-Anfrage ist erst übergeben, wenn sie als Kopierblock in der Antwort stand.** Das Ablegen fühlt sich wie Erledigung an; es ist keine | Rüge des Betreibers, 24.09.2026, 21:15: *„wieso schickst du mir die fable anfragen nicht?“* | %(u24)s, Block 8, „Die zwei Rügen des Betreibers“, Nr. 2 — D2 24/R2 |
| **6** | ⭐⭐ **Ein Sichtschutz-Treffer wird mit Fundstelle gemeldet, nicht mit Inhalt.** Das ist **Registertext 27.5**; er bindet — hier steht nur der Verweis, nicht der Text | Beim Melden eines Sichtschutz-Verstosses an Fable die betroffene Zeile selbst zitiert — den Sichtschutz beim Melden verletzt | %(u19)s, Block 7 (Fassung 21.09.), Ergänzung „Ein sechster Fehler für Block 7“, Nr. 6 — D2 21/6 |

---

## 16. Dokumentation aktuell halten""" % {"u19": U19, "u24": U24}

# ---------------------------------------------------------------- PRUEFPRINZIPIEN A9, A10 (19/5, 24/5)
PP_A_ALT = "gehört die Prüfung an die Stelle, wo eine Spur entsteht.\n\n---\n\n## B —"
PP_A_NEU = """gehört die Prüfung an die Stelle, wo eine Spur entsteht.

### A9 — Ein Nachweis gilt für den Gegenstand, den er berührt

*Ein Nachweis gilt für den Gegenstand, den er berührt, nicht für den Zweck, dem
er dienen sollte.*

**Der Fall (19.09.2026):** „F1b/Q2 ist erledigt“ gemeldet. Fable korrigierte:
**für die Daten** bewiesen (SHA-256 ist pandas-unabhängig), **nicht für den
Lauf**.

⭐ **Die Prüffrage:** Was hat die Messung berührt — und ist das derselbe
Gegenstand wie der, über den der Satz etwas behauptet?

**Herkunft:** %(u19)s, Block 7 (Fassung 19.09.), Nr. 5 — D2 19/5. Eingetragen
TB-119, 27.09.2026.

### A10 — Weicht die Nachmessung von der Vormessung ab, gilt die Nachmessung

*Eine Vormessung ist eine Selbstauskunft im Sinn von **A8**: Der steuernde Chat
misst, bevor er den Auftrag schreibt; die Sitzung misst nach, und bei Abweichung
gilt **ihre** Messung. Die falsche Vormessung ist kein Schaden, sondern der
Beweis, dass das Verfahren greift.*

**Der Fall (Übergabe 24.09.2026):** Die Vormessung sagte, `G8` prüfe
`median_balken`; nachgemessen prüft es `max_tage`.

**So steht es in den Aufträgen**, z. B. `docs/auftraege/MAC_TB-103_resolver_und_trockenlauf.md`,
Z. 54: *„Alles unten ist **Vormessung** des steuernden Chats … Nach `A8` misst du
nach. **Wenn etwas abweicht, gilt deine Messung.**“* ⚠️ *Die Bestandsaufnahme D2
fand „Vormessung“ im Regelwerk mit 0 Treffern und hielt `A8` für eine andere
Regel; die Aufträge zitieren A8 als Grund des Nachmessens.*

**Herkunft:** %(u24)s, Block 8, Nr. 5 — D2 24/5. Eingetragen TB-119, 27.09.2026.

---

## B —""" % {"u19": U19, "u24": U24}

# ---------------------------------------------------------------- PRUEFPRINZIPIEN B7 (21/4)
PP_B_ALT = "Import `data/` an** (T46.8).\n\n---\n\n## C —"
PP_B_NEU = """Import `data/` an** (T46.8).

### B7 — Gleiche Sonde, beide Dateien

*Die Prüfung, die wir von einer Datei verlangen, gilt auch für die Datei, die
wir für unverdächtig halten.*

**Der Fall (21.09.2026):** Fables Annahme *„das Register hat sein Tor schon“*
wurde fast ungeprüft übernommen. Sie stimmte — aber das war beim Übernehmen
nicht gemessen.

**Herkunft:** %(u19)s, Block 7 (Fassung 21.09.), Nr. 4 — D2 21/4. Eingetragen
TB-119, 27.09.2026.

---

## C —""" % {"u19": U19}

# ---------------------------------------------------------------- PRUEFPRINZIPIEN C8 (24/4)
PP_C_ALT = "verschiedene Fragen? **Und steht dabei, welche?**\n\n---\n\n## D —"
PP_C_NEU = """verschiedene Fragen? **Und steht dabei, welche?**

### C8 — Eine Kette ist erst geprüft, wenn alle ihre Eingaben geprüft sind

**Der Fall (Übergabe 24.09.2026):** Für `messgroessen.json` wurde „von Befund 1
nicht betroffen“ behauptet, nachdem nur **ein** Pfad geprüft war — die zweite
Kette lag daneben.

**Herkunft:** %(u24)s, Block 8, Nr. 4 — D2 24/4. Eingetragen TB-119, 27.09.2026.

---

## D —""" % {"u24": U24}

# ---------------------------------------------------------------- C2: Fable-Sammlung, Abschnitt D, nur anhaengen
FS_ALT = "*(wird fortgeschrieben — je Eintrag: Datum, Herkunft, Frage, Neigung)*\n"
FS_NEU = FS_ALT + """
### 27.09., TB-119: D2 19/6 gegen ARBEITSWEISE 6d

*Herkunft: `docs/ERGEBNIS_TB-119_repo_nachziehen_regelwerk_nachtrag.md`, Schritt C2; Vorlage
`docs/belege/TB-118/d2_fehlende_regeln.txt`, Zeile 19/6. Nach Auftrag TB-119 nicht ins Regelwerk eingetragen.*

**Wortlaut 1** — `projektfuehrung/UEBERGABE_2026-09-19.md`, Block 7 (Fassung 19.09.), Nr. 6, Spalte „Regel“:
> ⭐ **Ein Abbruchkriterium benennt die Sache, nie ihr Merkmal.** Und: fallen Wortlaut und Zweck auseinander und ist
> jemand erreichbar — **fragen**, nicht entscheiden

**Wortlaut 2** — `projektfuehrung/ARBEITSWEISE.md` 6d, Unterabschnitt „Nur richtungsweisende Rückfragen — und die als
Multiple Choice (22.09.2026)“, Tabelle „NICHT richtungsweisend“, Z. 898 (Stand `df825b6`):
> ⚠️⚠️ **Ein Abbruchkriterium.** Es führt zu **ABBRUCH und Meldung** — nie zu einer Rückfrage. *Wer bei einem
> Abbruchkriterium fragt, verwandelt eine Wache in eine Verhandlung*

**Hinweis:** `projektfuehrung/BACKLOG_ENTSCHEIDUNGEN.md`, Eintrag **K2h** (Z. 111), führt den zweiten Satz von
Wortlaut 1 als Regel (T55b.5) mit dem Zusatz „— in ARBEITSWEISE §7c“. In ARBEITSWEISE 7c steht dazu nichts: 7c nennt
das Abbruchkriterium nur als Zeile „gilt nur für Fehlschläge, **die den Gegenstand der Aufgabe betreffen** (T44.11)“.
Gemessen: `grep -n -i abbruchkriterium` in ARBEITSWEISE, vier Treffer (Z. 155, 898, 1118, 1129 am Stand `7eadc7a`),
keiner mit „fragen“. — Die erste Hälfte von Wortlaut 1 steht als **K2f** (Z. 109, „gehört auch in
`docs/PRUEFPRINZIPIEN.md`“) und widerspricht 6d nicht; sie ist mit 19/6 nach Auftrag ebenfalls nicht eingetragen.

**Frage:** Welche Regel gilt, wenn Wortlaut und Zweck eines Abbruchkriteriums auseinanderfallen und jemand erreichbar
ist: **fragen** (Übergabe 19.09., K2h, T55b.5) oder **Abbruch und Meldung** (ARBEITSWEISE 6d, 22.09.)? Und soll die
erste Hälfte (K2f) getrennt davon eingetragen werden — wenn ja, wohin?

**Neigung:** keine — Mac-Sitzung; die Neigung gibt der steuernde Chat. Zwei Tatsachen dazu: 6d ist die jüngere
Regel und nennt ihre Fälle „abschliessend“; `BACKLOG_ARCHIV.md` T54.2 führt einen Fall, in dem Fragen nach K2h eine
Nummernkollision verhindert hat.
"""

STELLEN = [
    (AW, "14: 21b/1, 21b/5, 24/6", AW_14_ALT, AW_14_NEU),
    (AW, "15: 21/1, 21/2, 21/3, 21/7, 24/R2, 21/6 (Verweis 27.5)", AW_15_ALT, AW_15_NEU),
    (PP, "A9 (19/5), A10 (24/5)", PP_A_ALT, PP_A_NEU),
    (PP, "B7 (21/4)", PP_B_ALT, PP_B_NEU),
    (PP, "C8 (24/4)", PP_C_ALT, PP_C_NEU),
    (FS, "C2: Abschnitt D, 19/6 als Frage (nur angehaengt)", FS_ALT, FS_NEU),
]

if __name__ == "__main__":
    lesen = None
    if "--nur-protokoll" in sys.argv:
        basis = sys.argv[sys.argv.index("--nur-protokoll") + 1]
        lesen = lambda d: subprocess.run(["git", "show", "%s:%s" % (basis, d)], capture_output=True,  # noqa: E731
                                         check=True).stdout.decode("utf-8")
    sys.exit(einsetzen(STELLEN, "docs/belege/TB-119/c_stellen.md",
                       "TB-119 Schritt C — 13 Regeln aus D2 und die Frage zu 19/6", "--probe" in sys.argv, lesen))
