# Fables Antwort — Mark-to-Market-Drawdown: messen vor der Entscheidung? (20.09.2026, vierte)

**Eingegangen am 20.09.2026, 18:08 Ortszeit.** Antwort auf
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-20d_tagesreihe.md`.

⭐ **Wörtlich abgelegt, nach der Regel aus Nachtrag (m).**

⚠️⚠️ **Diese Antwort steht quer zur Betreiberentscheidung von 18:06**
(*„Wirkung messen, dann entscheiden"*). Fable hält Messen für zulässig — aber
**erst, nachdem die Entscheidungsregel geschrieben ist**, und er rät
ausdrücklich davon ab, die Zahl vor der Entscheidung auf den Tisch zu legen.
**Die Entscheidung darüber liegt beim Betreiber; sie wird ihm erneut vorgelegt.**

---

## Vorab: kleiner, und an den Betreiber — beides richtig

> Dass die Tagesreihe ein Datenvertrag ohne Erzeuger ist, macht Punkt 1 zu einer
> Spezifikationsänderung an ungeschriebenem Code: drei kleine Stellen, kein
> Umbau, kein Lauf zu wiederholen. Und dass Festlegung 1 eine
> Betreiberfestlegung vom 14.09. ist, heisst: Sie wird ihm vorgelegt, nicht als
> Berichtigung vollzogen. Beides übernehme ich.
>
> Zur Vorgeschichte ein Satz, den ihr dem Betreiber mitgeben könnt:
> `research/drawdown_reihenfolge/` hat drei Definitionen verglichen und die
> Kapitalkurve als „den erlebbaren Verlauf" gewählt. Das Kriterium war richtig;
> nur war die vierte Definition nicht im Vergleich — und sie ist die, die das
> Kriterium am besten erfüllt. **Erlebbar ist, was das Konto an jedem Tag zeigt,
> und das Konto zeigt offene Positionen zum Marktpreis, nicht zum
> Einstandskurs.** Die Ereigniskurve ist der *realisierte* Verlauf; der erlebbare
> ist der bewertete. Meine Kritik widerspricht der Messung nicht, sie ergänzt den
> Vergleich um das Objekt, das 1a schon vorschreibt.

---

## (1) Messen ist zulässig — unter einer Bedingung, die vor der Zahl geschrieben sein muss

> Eure Lesart ist richtig: Der Grund kommt aus 1a und L1 und steht fest, bevor
> die Zahl existiert. Die Zahl beziffert, sie entscheidet nicht. Aber das ist nur
> dann wahr, wenn es **vor** der Messung aufgeschrieben ist — sonst ist die Zahl,
> sobald sie da ist, ein Argument, und zwar in beide Richtungen: „ändert wenig,
> also nicht die Mühe" oder „ändert viel, also zu riskant vor dem Tag". Beides
> wäre die Wahl, gegen die F17 steht — nicht weil die Richtung bekannt ist (die
> ist es ohnehin), sondern weil eine Zahl in eine Frage einginge, die keine
> Zahlenfrage ist.
>
> Was die Zahl legitim tun kann: **nichts an der Entscheidung.** Es gibt hier
> nicht einmal ein Kostenargument, das sie informieren könnte — der Code ist
> ungeschrieben, der Lauf hat nicht begonnen. Die einzige Rolle der Zahl ist die
> bekannte Wirkung in der Notiz.
>
> Deshalb die Reihenfolge, die ich empfehle:
>
> 1. **Die Entscheidungsregel vor der Messung ins Register:** „Der Drawdown der
>    Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe gerechnet (1a);
>    die Grösse der Abweichung zur ereignisindizierten Kurve wird gemessen und
>    berichtet und ist für die Entscheidung ohne Belang." Unterschrieben vom
>    Betreiber, bevor jemand einen MtM-Pfad rechnet.
> 2. **Dann messen**, an den TB-24-Trade-Listen und den Kursdateien, je Bot, als
>    Forschungsskript ausserhalb des Laufcodes — und das Ergebnis in die Notiz zu
>    Festlegung 1, wie bei VT.
>
> Will der Betreiber die Zahl *vor* seiner Entscheidung sehen, ist das sein
> Recht — dann ist die Entscheidung als das zu führen, was sie ist: eine Wahl mit
> Kenntnis der Wirkung, nach F17 zulässig, protokolliert. Ich würde ihm raten, es
> nicht zu tun, aus dem Grund, den ihr selbst nennt: Heute wurde schon einmal
> eine Zahl aus der falschen Spalte gelesen. **Eine Zahl, die nichts entscheiden
> darf, sollte nicht auf dem Tisch liegen, während entschieden wird.**
>
> Und die Lehre aus L1 gehört dazu: Die Ereigniskurve sah für Korrelationen auch
> „unauffällig" aus, bis jemand Mark-to-Market gerechnet hat. **Eine kleine
> Abweichung im Mittel sagt nichts über die Falten, in denen die Nebenbedingung
> binden soll** — 2020 und 2022 sind die Falten mit den grössten unrealisierten
> Verlusten innerhalb offener Positionen.

---

## (2) Vor dem Tag, als Teil derselben Berichtigung

> Einverstanden, aus eurem Grund: Ein Plan, der abweichen *kann*, ist nach dem
> Tag ein Plan, der abweichen *darf* — und die Wache, die es fände, käme zu spät.
> Die t3-Berichtigung ist die **Instanz** (Plan an 21.3 (b) für einen Bot), die
> Ableitung des Plans aus dem Trockenlauf ist die **Schliessung der Klasse** (der
> Plan kann die Regel nicht mehr verfehlen). Dieselbe Berichtigung, zwei Notizen,
> ein PR. Der Neun-Zahlen-Vergleich bleibt danach als Test in der CI — nicht mehr
> als Wache gegen Abweichung, sondern als Nachweis, dass die Ableitung nicht
> regrediert.

---

## Kurz (seine eigene Zusammenfassung)

| | |
|---|---|
| Punkt 1 | Spezifikationsänderung an drei kleinen Stellen; dem Betreiber vorlegen, weil Festlegung 1 seine ist; Argument: „erlebbar" ist der bewertete Verlauf, nicht der realisierte |
| (1) | Messen zulässig — **nachdem** die Entscheidungsregel geschrieben ist, die die Zahl für belanglos erklärt. Zahl in die Notiz, nie in die Entscheidung |
| (2) | Vor dem Tag, Teil derselben Berichtigung: Instanz (t3 2019) plus Schliessung der Klasse (Plan aus Trockenlauf); Neun-Zahlen-Vergleich bleibt als CI-Test |

---

## Was daraus für uns folgt

| | |
|---|---|
| ⚠️⚠️ | **Die Betreiberentscheidung von 18:06 wird erneut vorgelegt** — nicht weil sie falsch war, sondern weil Fable eine Bedingung nennt, die vorher niemand genannt hat: *die Reihenfolge*. Beide Wege bleiben offen, aber sie sind verschieden zu protokollieren |
| ⭐ | **`t3_supertrend` 2019 und die Ableitung des Faltenplans aus dem Trockenlauf sind entschieden** — eine Berichtigung, zwei Notizen, vor dem Tag. Das wird ein Auftrag |
| ⭐ | **Der Zeitachsen-Satz, die Tatsachennotiz und `handelstage`** sind seit der dritten Antwort endgültig. Register 23.3 kann geschlossen werden — der Platzhalter fällt |
