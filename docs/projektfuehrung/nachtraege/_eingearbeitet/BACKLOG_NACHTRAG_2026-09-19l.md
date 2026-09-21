# Backlog-Nachtrag 19.09.2026 (l) — TB-54 und die drei Nummernkollisionen

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(k) voraus.** Einzufügen als **Block 2r**, nach Block 2q.

⭐ **Dieser Nachtrag nennt bewusst KEINE konkreten Nummern für neue Zeilen** —
die vergibt die ausführende Sitzung nach Messung (siehe K2i unten).

---

### 2r — TB-54: die acht Nachträge, und was dabei sichtbar wurde

| # | Punkt |
|---|---|
| **T54.1** | ⭐⭐ **ALLE ACHT BACKLOG-NACHTRÄGE (d)–(k) SIND EINGEARBEITET.** Commits **`d9f3c4b`** (d–g) und **`3121ec2`** (h–k), beide gepusht. `BACKLOG.md` 764 → **929 Zeilen**, **167 hinzu / 2 entfernt** gegen `0fe61d7`; die zwei entfernten (0,84 und 0,85) **stehen darunter weiter**, als ersetzt gekennzeichnet und datiert. Sieben neue Blöcke **2j, 2k, 2m, 2n, 2o, 2p, 2q**, sechs ersetzte Kettenzeilen, eine Kopfzeile vor T34.10 |
| **T54.2** | ⭐⭐ **DIE REGEL AUS T55b.5 HAT SICH EINE STUNDE NACH IHRER FORMULIERUNG BEWÄHRT.** Nachtrag (h) wollte die Faltenschranke als **`0,87`** eintragen — **`0,87` war bereits belegt**. Wortlaut und Zweck fielen auseinander; ⭐ **die Sitzung hat gefragt statt entschieden.** Betreiberentscheidung: **`0,88` mit Vermerk in der Rang-Zelle**. **(d)–(g) waren zu dem Zeitpunkt bereits als Teilerfolg committet** — der Teilerfolg war kein Notbehelf, sondern der eingebaute Weg |
| **T54.3** | ⭐⭐ **EIN A1-FALL, VON DER SITZUNG SELBST GEFUNDEN — mein Auftrag hätte ihn übersehen.** Vier Nachträge ersetzen Kettenzeilen, die **derselbe Arbeitsbaum** erst angelegt hatte; ⚠️ **gegen `HEAD` gemessen sind solche Ersetzungen unsichtbar** — `numstat` hätte „0 entfernt" gemeldet, obwohl ersetzt wurde. ⭐ **Die Sitzung mass deshalb zweifach:** kumulativ gegen `HEAD` **und** gegen eine Kopie des Standes vor dem jeweiligen Nachtrag. **171/6 in Schritten, 167/2 gesamt; die Differenz 4/4 ist vollständig zugeordnet** (0,85a · 0,86 zweimal · 0,86a). ⚠️ *Ein fehlgeschlagener Nachweis und ein leeres Ergebnis hätten gleich ausgesehen* |
| **T54.4** | ⭐ **JEDE EINFÜGUNG LIEF ÜBER EINEN ANKER, DER GENAU EINMAL VORKOMMEN MUSS**, sonst Abbruch **vor dem Schreiben**. Zwei solche Abbrüche gab es (Anführungszeichen bei (d), Zeilenumbruch bei (h)) — **beide folgenlos, Datei unverändert.** ⭐ *Ein Werkzeug, das vor dem Schreiben abbricht, ist besser als eines, das hinterher misst* |
| **T54.5** | ⭐ **SIEBEN NACHTRAGSDATEIEN SIND INS REPO GEWANDERT** (`docs/projektfuehrung/nachtraege/`), byteidentisch per `cmp`, `git check-ignore` rc 1. **Damit ist K2g erfüllt, ohne dass es beauftragt war** — Begründung wörtlich: *„Ein Beleg in `~/Downloads` ist kein Beleg; er existiert auf einem Rechner und in keiner Version."* ⚠️ **Offen: der TB-55-Cloud-Bericht** (T55b.6) liegt weiterhin nur in `~/Downloads` |
| **T54.6** | ⚠️⚠️ **DREI NUMMERNKOLLISIONEN, ALLE AUS NACHTRÄGEN DES BETREUERS.** **(1)** `0,87` doppelt (Nachtrag (h)) — gelöst als `0,88` mit Vermerk. **(2)** ⚠️ **`V1`–`V7` aus Nachtrag (i) kollidieren mit der `V`-Reihe in Abschnitt 2** — `V1` steht jetzt **zweimal** (*„absolute Drawdown-Grenze gestrichen"* und *„leere Doppelgängerin"*). **(3)** ⚠️ **„TB-54" bezeichnet zwei Vorhaben** — `0,85c` nennt *„TB-54 — Lese-Audit"*, `0,86b` *„TB-54 — die acht Backlog-Nachträge"*. ⭐ **Muster, kein Einzelfall: Nummern wurden vergeben, ohne den Zielstand zu messen** — genau die Fehlerklasse, gegen die dieses Projekt Regeln schreibt |
| **T54.7** | ⭐⭐ **DIE KETTE IST NUMERISCH UNSORTIERT — und das ist ein Befund über die Arbeitsweise, nicht über diese Sitzung.** Stand: `0,84 · 0,84alt · 0,85a ERLEDIGT · 0,85a alt · 0,85b · 0,85c · 0,85 alt · 0,87 · 0,86 ERLEDIGT · 0,86a ERLEDIGT · 0,86b · 0,86a alt · 0,86 alt · 0,88 · 0,86 alt · 0,95`. ⭐ **Die Sitzung hat bewusst nicht umsortiert**, weil das entfernte Zeilen erzeugt hätte. ⚠️⚠️ **Die Kette ist eine Rangfolge; unsortiert erfüllt sie ihren Zweck nicht.** ⭐ **Der Kern: Wir wenden Register-Disziplin auf ein Arbeitsdokument an. „Nur hinzufügen" ist richtig für `VORREGISTRIERUNG_neuselektion.md` — dort schützt es die Nachvollziehbarkeit des Laufs. `BACKLOG.md` ist kein Registertext; dort schützt dieselbe Regel nichts und kostet Lesbarkeit.** **Betreiberentscheidung erforderlich** |
| **T54.8** | **Nebenbefunde, ohne Handlung:** `K1n`, `K1o`, `K1q` stehen jetzt **zweimal** in Abschnitt 4 (Original aus (c), Fortschreibung aus (d)) — Folge von „nur hinzufügen", dieselbe Frage wie T54.7 · die Nachtragsdatei (d) im Repo hat keinen Beleg-Kopf, die sieben neuen ebenfalls nicht (damit ihre Grössen gegen `00_INHALT.txt` prüfbar bleiben) · `git rev-parse --short HEAD origin/main` schlug fehl (`--short` nimmt nur eine Revision), nachgeprüft mit zwei Aufrufen — **Werkzeugfehler der Sitzung, benannt, kein Befund am Repo** |

---

## ⚠️ Vermerke — nichts wird umnummeriert

⚠️⚠️ **Es werden NUR Hinweise ergänzt.** Dieselbe Form, die Abschnitt 18 des
Registers für `4fee547d…` benutzt: *die Stelle wird erklärt, nicht geändert.*

| # | Stelle | Zu ergänzen |
|---|---|---|
| **1** | Abschnitt 2, Punkt **`V1`** *(„absolute Drawdown-Grenze gestrichen")* **und** Block **2o**, Punkt **`V1`** *(„leere Doppelgängerin")* | ⭐ **Bei beiden ein Vermerk:** *„Die `V`-Nummern in Block 2o stammen aus der Vorprüfung vom 19.09.2026 und bilden eine **eigene Reihe** — sie sind nicht die `V`-Reihe aus Abschnitt 2. Beide Nummerierungen bleiben; keine wird geändert."* |
| **2** | Kette **`0,85c`** *(„TB-54 — Lese-Audit")* | **Vermerk:** *„Die Aufgabennummer TB-54 wurde am 19.09.2026 für die Einarbeitung der Backlog-Nachträge verbraucht. Das hier gemeinte Vorhaben (Lese-Audit) bekommt bei seiner Formulierung eine neue Nummer."* ⭐ **Keine neue Nummer erfinden** |
| **3** | Kette **`0,88`** | ⭐ **Prüfen, ob der Vermerk aus TB-54 dort steht** *(„im Nachtrag (h) als 0,87 vergeben; 0,87 war bereits belegt — Betreiberentscheidung 19.09.2026")*. **Steht er: nur bestätigen.** Sonst ergänzen |

---

## Neue Kettenzeile

⭐ **Die nächste freie Nummer unterhalb von 0,86b, gemessen** — dieser Nachtrag
nennt sie ausdrücklich **nicht**:

```
| ⟨nächste freie⟩ | ⭐ **Die Kette sortieren** (T54.7): aktive Zeilen numerisch, ersetzte Zeilen vollständig erhalten unter einer eigenen Überschrift „Ersetzte Kettenzeilen" am Abschnittsende. ⚠️ **Maschinell zu prüfen: jede entfernte Zeile taucht unten wörtlich wieder auf.** ⚠️ **Setzt eine Betreiberentscheidung voraus** | offen |
```

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2i** | ⚠️⚠️ **EIN NACHTRAG NENNT KEINE KONKRETE NUMMER, DIE ER NICHT SELBST GEMESSEN HAT.** Er sagt *„die nächste freie Nummer, gemessen"* und begründet nur die **Einordnung**; die Nummer vergibt die ausführende Sitzung. ⭐ **Herkunft: drei Kollisionen am 19.09. (0,87 · V1 · TB-54), alle aus Nachträgen, die eine Nummer nannten, ohne den Zielstand zu kennen** — der Betreuer kann das Repo nicht lesen und darf nicht so tun, als könnte er es |
| **K2j** | ⭐ **Eine Ersetzung im selben Arbeitsbaum ist gegen `HEAD` unsichtbar.** Wer Zeilen ersetzt, die dieselbe Sitzung angelegt hat, misst **zusätzlich** gegen eine Kopie des Standes davor (T54.3) |
| **K2k** | ⭐ **Ein Werkzeug, das vor dem Schreiben abbricht, ist besser als eines, das hinterher misst** — Anker müssen genau einmal vorkommen (T54.4) |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte
   Zeilen: 0.** *Dieser Nachtrag ersetzt nichts; er fügt ein und ergänzt
   Vermerke.* **Weicht es ab, ist das ein Befund.**
2. ⚠️ **Prüfen, dass keine Nummer geändert wurde** — beide `V1` stehen noch,
   `0,85c` heisst noch `0,85c`.
3. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.
