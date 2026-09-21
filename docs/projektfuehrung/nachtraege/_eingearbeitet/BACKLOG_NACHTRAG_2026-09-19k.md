# Backlog-Nachtrag 19.09.2026 (k) — TB-55b: der Snapshot steht im Register

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(j) voraus.** Einzufügen als **Block 2q**, nach Block 2p.

---

### 2q — TB-55b: Abschnitt 18, die Tatsachennotiz zum Snapshot

| # | Punkt |
|---|---|
| **T55b.1** | ⭐⭐⭐ **DER EINGABEZUSTAND IST REGISTRIERT.** `docs/VORREGISTRIERUNG_neuselektion.md`, neuer **Abschnitt 18** — Tatsachennotiz zu Registertext 5 / 5a, in der Form von 15.6. Commit **`0fe61d7`** auf `main`, gepusht. **62 Zeilen hinzugefügt, 0 entfernt.** Er hält fest: Name `63e4b6c8…`, Ort, Commit `1075dec`, `zeitpunkt_utc` 2026-09-19T06:49:32+00:00, 225 Dateien, 211 040 678 Bytes, Datenstand `d9449faf…`/223, 36 zugelassene `rand_erste`-Befunde nach 17.3, `nicht_zugelassen` leer, `--pruefen` `UNVERAENDERT` — ⚠️ **und den bindenden Satz: „Ein zweiter Snapshot ist ein neuer Lauf. `snapshots/` wird von hier an nur gelesen."** |
| **T55b.2** | ⭐⭐ **KEINE ZAHL IM EINTRAG IST GETIPPT.** `eintrag_erzeugen.py` liest `MANIFEST.json` per `json.load`, holt den Commit per `git log -- snapshots/`, prüft `origin/main` per `git branch -r --contains`, **misst die höchste Abschnittsnummer selbst und trägt ein `assert neu == 18`**. Vorher **8/8 Werte maschinell** gegen die Auftragsliterale verglichen — String- **und** Typgleichheit, rc 0 |
| **T55b.3** | ⭐⭐ **EINE FALLE WURDE ZU DOKUMENTATION.** Abschnitt **17.9** führt `snapshot_hash` = **`4fee547d…`** — die TB-47-Messung über die **223 Kursdateien allein**, vor dem Ziehen. ⚠️ **Das ist die Stelle, an der später jemand die falsche Zahl abschreibt.** ⭐ **Der neue Abschnitt 18 grenzt sie ausdrücklich ab:** *„`63e4b6c8…` läuft über die 225 Dateien; `4fee547d…` lief nur über die 223 Kursdateien und bezeichnet nicht diesen Snapshot. Beide bleiben richtig; sie beantworten verschiedene Fragen."* **Zwei Zahlen, zwei Fragen — jetzt im Register selbst, nicht in einem Bericht daneben** |
| **T55b.4** | ⚠️⚠️ **DIE SITZUNG HAT GEGEN DEN WORTLAUT EINES ABBRUCHKRITERIUMS ENTSCHIEDEN — und es offengelegt.** Der Auftrag sagte: *„Gibt es einen Snapshot-Abschnitt mit einer Zahl darin: ABBRUCH."* 17.9 enthält eine. Die Sitzung entschied **nach dem Zweck** (kein Duplikat) statt nach dem Wortlaut, schrieb es hin und nannte den Commit, den der Betreiber ansehen soll. ⭐ **Die Entscheidung war richtig.** ⚠️⚠️ **Die Regel war schlecht geschrieben, und das liegt beim Auftraggeber:** *„eine Zahl darin"* war ein **Stellvertreter** für *„ein Eintrag, der DIESEN Snapshot bezeichnet"* |
| **T55b.5** | ⭐⭐ **ZWEI NEUE REGELN AUS T55b.4.** **(1) Für Aufträge:** *Ein Abbruchkriterium benennt die Sache, nie ihren Stellvertreter* — dieselbe Klasse wie „+0,001 %" statt „ein Blob" (T55.15). **(2) Für Sitzungen:** *Fallen Wortlaut und Zweck eines Abbruchkriteriums auseinander und ist der Betreiber erreichbar — fragen, nicht entscheiden.* ⚠️ **Offen gelegt entscheiden ist die zweitbeste Lösung; dass es diesmal richtig ausging, macht die Methode nicht sicher** |
| **T55b.6** | ⚠️⚠️ **DAS REGISTER TRÄGT EINE ANGABE OHNE BELEG IM REPO.** Die Sitzung hat es selbst gemeldet: *„Die Angabe ‚Python 3.11.15' für den TB-55-Cloud-Trockenlauf steht nur in der Bewertung, nicht im Repo."* ⭐ **Daraus eine allgemeine Regel: Jede Behauptung im Register braucht ihren Beleg im Repo. Ein Beleg in `~/Downloads` ist kein Beleg — er existiert auf einem Rechner und in keiner Version.** **Zu tun:** den TB-55-**Cloud**-Bericht ins Repo legen, wie die Mac-Berichte auch |
| **T55b.7** | ⭐ **ABSCHNITT 18 STATT 17.12 — besser begründet als beauftragt.** Der Auftrag verlangte nur „die nächste freie Nummer". Die Sitzung fand einen inhaltlichen Grund: **Abschnitt 17 ist der TB-48-Nachtrag vom 18.09. und sagt in 17.11 ausdrücklich „Kein Snapshot gezogen"** — ein 17.12 vom 19.09. hätte diesem Satz im selben Abschnitt widersprochen |
| **T55b.8** | ⚠️ **DAS MANIFEST FÜHRT DIE BEFUNDART AN ZWEI STELLEN VERSCHIEDEN:** `zugelassene_befunde[*].art` (String) und `teilkerzen.befunde[*].arten` (Liste). **Beide sagen `rand_erste`.** ⭐ **Dieselbe Klasse wie die doppelte Hash-Rechnung (T55.8): zwei Quellen für eine Aussage, die auseinanderlaufen können.** ⚠️ **Nicht angefasst — `shared/snapshot.py` ist gemessen.** Zu entscheiden, nicht jetzt |
| **T55b.9** | ⭐ **A7 wurde angewandt, nicht nur notiert:** der „vorher"-Lauf des Registerprüfers fand um **07:12 UTC** statt, der Commit um **07:20 UTC** — *vorher heisst vorher.* **Ein U+202F** aus der Tausendertrennung wurde durch gewöhnliche Leerzeichen ersetzt; **vorher 0 Vorkommen in der Datei, nachher genau 2 = die neuen**, numstat blieb `62/0` — ⭐ **gezählt statt angenommen** |
| **T55b.10** | ⚠️⚠️ **DIE NACHTRÄGE WACHSEN SCHNELLER, ALS SIE ABGEARBEITET WERDEN.** Stand 19.09.: **Backlog (d)–(k) = acht**, **Journal (c)–(e) = drei**, dazu **A7** in die Prüfprinzipien. ⭐ **Jede Bewertung bringt zwei neue mit** — das ist die Folge der §5b-Regel und richtig so, **aber es verlangt, dass eingearbeitet wird, bevor der Stapel wächst.** ⇒ **TB-54 (Backlog) und TB-54b (Journal + Prüfprinzipien) haben Vorrang vor TB-53 und TB-56** |

---

## Ergänzung zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2f** | ⭐⭐ **Ein Abbruchkriterium benennt die Sache, nie ihren Stellvertreter** (T55b.5) — gehört auch in `docs/PRUEFPRINZIPIEN.md` |
| **K2g** | ⭐⭐ **Jede Behauptung im Register braucht ihren Beleg im Repo** (T55b.6) |
| **K2h** | ⭐ **Fallen Wortlaut und Zweck eines Abbruchkriteriums auseinander und ist jemand erreichbar: fragen** (T55b.5) — in ARBEITSWEISE §7c |

---

## Kettenzeile — 0,86a ist erledigt

**Zu finden** (Abschnitt 3, Rang **0,86a**, aus Nachtrag (j)).
⚠️ **Ersetzen, alter Wortlaut bleibt darunter als ersetzt gekennzeichnet:**

```
| **0,86a** | ⭐⭐ **TB-55b — der Registereintrag: ERLEDIGT 19.09.2026.** Abschnitt 18, Commit `0fe61d7`, 62 Zeilen hinzu / 0 entfernt | ✅ **abgeschlossen** |
| **0,86b** | ⭐ **TB-54 — die acht Backlog-Nachträge (d)–(k) einarbeiten** · **TB-54b — Journal (c)–(e) und Prüfprinzip A7** | ⚠️ **als nächstes, vor TB-53** |
```

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte
   Zeilen: die der ersetzten Kettenzeile 0,86a, sonst keine.**
2. ⚠️ **Alter Wortlaut von 0,86a als ersetzt gekennzeichnet darunter** — nicht
   gelöscht.
3. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.
