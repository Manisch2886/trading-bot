# FABLE_ANTWORT 2026-09-23b — (ii): einmal neu rechnen, nach Weg (A) — und die Neurechnung ist zugleich der Determinismusnachweis, weil sie `_tb72.json` bis auf einen Namen reproduzieren muss

*Bezug: `FABLE_ANFRAGE_2026-09-23b_tb72_erfuellt_es_aber.md` (23.09., 07:30). Kenntnisnahme zu 0 und 1; Entscheidung zu 2; eine Bedingung, die (ii) billiger und schärfer macht.*

---

## 1. Kenntnisnahme

**Abschnitt 38:** 454/0, vierzehn Marken, 22 Blockzitate mit `diff` rc 0 — dass die Zitate eingesetzt und nicht abgetippt wurden, ist genau die Bauart, die Zuschreibungsfehler wie den aus 22f ausschliesst. **38.2 im Kopf von Abschnitt 0:** richtig entschieden, und die Begründung ist die richtige — eine Regel über das Schreiben von Registertext gehört dorthin, wo jeder vorbeikommt, der einen schreibt.

**Messbitten:** `_tb72.json` tagesgenau nach 23, neunmal `endgueltig`, identisch mit `_vt.json` bis auf die leere Falte 2018 bei `t3_supertrend` — also `_vt.json` nach meiner Berichtigung zu 21.3 (b). Kandidat, wie ihr sagt; ob die Faltenmenge je Bot gleich 33.2 ist, misst TB-90 — und erst diese Messung macht ihn zur Tabelle, nicht der Name. In keiner Sperrlisten-Gruppe: zur Kenntnis, das wird sich mit dem Vollzug ändern (37.2, Gruppe „bestimmt").

## 2. Die Bestätigungszeile (Abschnitt 2) — Entscheidung: (ii), mit einer Bedingung

**(i)** fällt aus dem Grund, den ihr selbst nennt: Es stünde ein Name in einer registrierten Datei, den 35.1 unzulässig nennt, und bei `elliott_wave` ein Doppeljahr ausserhalb der Spanne. „An einer Zeile, die niemand liest" ist kein Argument — heute liest sie niemand; ob der Erzeuger oder ein Bericht sie morgen liest, weiss keiner, und die Regel, dass Bezeichner die Spanne nennen, darf nicht davon abhängen, wer gerade hinsieht. Eine Wache mit Ausnahme für den einen Fall, der ihr widerspricht, ist keine Wache. **(iii)** friert eine Tabelle ein, die drei Tage später wieder falsch ist — zwei Läufe statt einem, und dazwischen ein registrierter Zustand, der dem Register widerspricht.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Ergänzung zu 23a, Abschnitt 3 (Registertext zu Sperrlistenpunkt 4):** Die Tabelle, die der Lauf liest, wird **nach** der Umsetzung von Weg (A) (Punkt 3, TB-90) **einmal** neu gerechnet — mit `benchmark.py` (Sperrlistenpunkt 4/6, unverändert), auf dem dann gültigen Plan, mit `--ziel` auf einen neuen Pfad nach der Schreibregel 36.1, mit Beleg und Hash. Ihre Bestätigungszeile trägt den Bezeichner nach 35 (`2026-01-01/2026-09-01`).
>
> **Bedingung an die Neurechnung — der Determinismusnachweis:** Die neu gerechnete Tabelle muss `benchmark_drawdowns_tb72.json` für **alle neun Bots in allen Werten reproduzieren**; der einzige zulässige Unterschied ist der Name der Bestätigungszeile (und, sofern die Tabelle ihn führt, ein Feld, das diesen Namen wiederholt). Ein `diff`, der etwas anderes zeigt, ist ein **Befund**, kein Ergebnis: Dann hat sich zwischen TB-72 und TB-90 etwas bewegt, das nicht der Name ist — Plan, Daten oder Code —, und das ist vor dem Vollzug zu klären, nicht wegzurechnen. Die Tabelle wird in diesem Fall **nicht** vollzogen.
>
> `benchmark_drawdowns_vt.json` und `benchmark_drawdowns_tb72.json` bleiben unverändert liegen, erhalten je eine Tatsachennotiz (Planstand, auf dem sie gerechnet wurden; TB-66 bzw. TB-72) und kommen **nicht** auf die Sperrliste; die Gruppe „bestimmt" in 37.2 wechselt auf die neue Tabelle. Sperrlistenpunkt 4 nach Form (ii): `benchmark_drawdowns.json` als registrierter historischer Stand, die neue Tabelle als die, die der Lauf liest.

*Quelle des Grundes:* 35.1 (Bezeichner ist die Spanne, ein anderer ist unzulässig), 23a (Tabelle folgt dem Plan; Neurechnung dort schon vorgesehen), 36.1 (Schreibregel). Und die Bedingung ist 10.1 in Anwendung: Erlaubt sind nur Änderungen mit **bitidentischen** Ergebnissen — die Neurechnung ändert einen Namen, also müssen alle Zahlen gleich bleiben, und wenn sie es sind, ist das zugleich der Nachweis, dass `benchmark.py` deterministisch ist und der Plan sich seit TB-72 nicht bewegt hat (32 hat es behauptet; hier wird es an der Tabelle gemessen). **Kein Ergebnis:** Ich verlange Gleichheit mit einer Tabelle, deren Werte ich nicht kenne; ob sie „gut" oder „schlecht" sind, spielt für die Regel keine Rolle, und sie darf nach 27.1 auch nicht wiedergegeben werden — die Sonde meldet nur „gleich" oder „an Stelle X verschieden".

*Warum die Bedingung (ii) billiger macht statt teurer:* Ohne sie wäre die Neurechnung eine neue Tabelle, die man gegen das Register prüfen müsste, Falte für Falte. Mit ihr ist sie ein `diff` gegen eine vorhandene Datei mit erwartetem Ergebnis „eine Zeile je Bot". Der Aufwand ist ein Lauf und ein Vergleich; das Ergebnis ist ein Nachweis, den es bisher nicht gibt.

*Zu eurer Reihenfolge-Überlegung* („Weg (A) vorher, dann ein Lauf statt zwei"): richtig, und sie ist schon in 22h angelegt (Punkt 3 vor Punkt 8, Bündelung mit einem Abbild danach). TB-90 setzt (A) um und misst (a) und (b); die Neurechnung ist der Schritt danach, im selben Auftrag oder im nächsten — Handwerk.

## 3. Eine Folge für die Wache aus 23a

Die Wache „Faltenmenge der Tabelle = Abbild" prüft nach dieser Entscheidung **beides**: Selektionsfalten gegen `selektionsfalten` und die Bestätigungszeile gegen `bestaetigungsperiode` (35, Feld des Abbilds). Keine Ausnahme, keine Sonderbehandlung — genau deshalb (ii) und nicht (i).

**Leseprotokoll dieses Chats, Stand jetzt:** wie 23a; dazu ANFRAGE 23b. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…90`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** (ii) — einmal neu rechnen, nach Weg (A), mit `--ziel` auf neuen Pfad. Bedingung: Die neue Tabelle muss `_tb72.json` in allen Werten für alle neun Bots reproduzieren, einziger Unterschied der Name der Bestätigungszeile; jede andere Abweichung ist ein Befund und stoppt den Vollzug. Damit ist die Neurechnung zugleich der Determinismusnachweis für `benchmark.py` und die Bestätigung von 32 an der Tabelle. (i) fällt, weil eine Wache mit Ausnahme keine ist; (iii) fällt, weil es zwei Läufe und einen falschen Zwischenzustand erzeugt. `_vt` und `_tb72` bleiben liegen mit Tatsachennotiz, kommen nicht auf die Liste; „bestimmt" wechselt auf die neue Tabelle.

**Unsicher:** ob `benchmark.py` die Bestätigungszeile aus dem Plan bezieht (dann trägt sie nach (A) automatisch die Spanne) oder den Namen selbst bildet (dann ist eine Stelle in `benchmark.py` — Sperrlistenpunkt 4/6 — zu ändern, vor dem Tag zulässig nach 37.3, aber mit Freigabe und neuem Abbild). TB-90 (b) zeigt es.

---

## In einfacher Sprache

Die Vergleichstabelle muss nach der Umbenennung des Bestätigungszeitraums einmal neu gerechnet werden — die Prüfung soll keine Ausnahme bekommen, und eine Tabelle vor der Umbenennung einzufrieren wäre doppelte Arbeit. Fable macht aus der Neurechnung zugleich eine Probe: Die neue Tabelle muss der vorhandenen TB-72-Tabelle in jeder Zahl gleichen, nur der eine Zeilenname darf anders sein. Stimmt das, ist bewiesen, dass der Rechenweg reproduzierbar ist und sich seit TB-72 nichts bewegt hat. Stimmt es nicht, wird nichts eingefroren, sondern nachgesehen, was sich bewegt hat. Die beiden älteren Tabellen bleiben mit Vermerk liegen.
