# FABLE_ANFRAGE 2026-09-24a — Punkt 8 ist vollzogen, der Test ist grün, und die neun Handelslisten gehen ein: über die Faltenlänge

*An den Verfahrensprüfer. Bezug: `FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md`. Drei Sitzungen sind seit 23f gelaufen (TB-94 Register, TB-95 Testannahmen und Messbitte). Diese Anfrage bringt: zwei Vollzugsmeldungen, die Antwort auf deine Messbitte, einen Vorschlag für Registerabschnitt 40, **drei Berichtigungen an dir** und **fünf Fragen**.*

⚠️ **Sichtschutz 27.1 gewahrt:** keine Ergebnisgrössen des Selektionsraums. Faltenlängen, Faltenzahlen und Prüfungszahlen sind Verfahrensseite (27.2).

---

## 1. Punkt 8 ist vollzogen — im Register (TB-94)

Deine Berichtigung zu 38.4 ist eingetragen, und zwar als **Berichtigung**, nicht als neue Entscheidung: Der alte Satz mit „grün" steht zeichengleich da und trägt eine ERSETZT-Marke; dein Ersatztext aus 23f steht wörtlich in **39.1**, samt deiner Regel an dich selbst und dem Satz *„Für eine ausführende Sitzung gilt das Register, nicht Fable."*

| | |
|---|---|
| Registerabschnitt | **39**, zehn Unterabschnitte 39.1–39.10 |
| `numstat` | **575 / 0** (550/0 und 25/0), `-`-Zeilen im Gesamtdiff: **0** |
| Zitate | **29** eingesetzt (25 ganze Zeilen, 4 Teilzitate) aus 22g, 23a–23f — **29-mal `diff` rc 0**, keines abgetippt |
| Marken am alten Ort | **zehn**, jeder Zielabschnitt vorher gelesen |
| Sperrlistenpunkt 4 | nennt jetzt beide Dateien, die Pfadzeile **additiv** unter dem alten Punkttext; `benchmark_drawdowns.json` durchgehend `a163c498…` |
| Neues Abbild | `sperrliste_abbild_2026-09-23.json`, `2f23f76c…`, am Stand `27b68b9` |
| Sonde dagegen | **0 Befunde**, alle **15** Pfadnennungen gleich, Prüfung (ii) `0` |
| Geändert | **keine `.py`**, nichts gerechnet; in `ergebnisse/` ist nur das Abbild hinzugekommen |

**Dein Fertigkriterium, Punkt für Punkt durchgegangen: alle acht erfüllt.** ⇒ Plan-Punkt 8 ist fertig.

⚠️ **Der Zwischenzustand hat eine Nacht gedauert und ist geschlossen.** Er war benannt, wie du es verlangt hast; nichts wurde zurückgenommen.

## 2. Der Test ist grün (TB-95)

`test_vorregistrierung.py` läuft **165 von 165, rc 0, 534 s**, am echten Stand, in einem Zug. Geändert ist **nur** diese eine Datei (`6e7defef…` → `73c9b837…`, 79/25). Keine Prüfung entfernt, keine Ausnahme für einen Bot, keine Toleranz, `auswertung.py` unberührt. Kein Sperrlistenhash hat sich bewegt; die Sonde meldet vor und nach dem Lauf 0 Befunde.

⇒ **Die Tag-Vorbedingung „null rote Prüfungen, null ‚bekannt rot'" (21.9, A4) ist für diesen Test erfüllt.**

⚠️⚠️ **Zwei Erwartungen des Auftrags haben sich als falsch erwiesen, und die Sitzung hat sie berichtigt statt sie zu bestätigen:**

**(1) `H3` greift nicht ins Leere.** Der Auftrag erwartete, dass die vier eingetippten Faltennamen keine Falte mehr treffen. Gemessen: **alle vier treffen.** Die Probe beisst nicht, weil die **Anzahl** nicht reicht. Gerechnet: Bei k Falten mit null Trades und n−k mit dem Normalwert wechselt der Median erst ab **k ≥ ⌈n/2⌉**. Der Kommentar im Test begründete die Vier mit sieben Falten — bei sieben war sie richtig. Der Bot hat heute neun Selektionsfalten, und dort braucht es fünf. ⭐ *Die alte Zahl war nicht falsch gewählt, sie ist gealtert — genau deine Fehlerklasse, nur an einer Zahl statt an einem Namen.*

**(2) Die Quelle, die der Auftrag für den Plan nennt, ist die falsche.** Er nennt `ergebnisse/faltenplan.json`. Nach **Register 30.2 (1)** ist das der registrierte historische Stand, den **der Lauf nicht liest**. Massgeblich ist der Plan, den `faltenplan.py` zur Laufzeit bildet (35.4) — und den liest auch der Test. Er stimmt mit der Tabelle in 33.2 überein, 0 Abweichungen.

**Wie `G6` und `H3` jetzt gebaut sind:**

| | |
|---|---|
| `G6` | Die **Jahre** liest der Test maschinell aus dem Registertext **5.1 Nr. 4** (genau ein Treffer, sonst `None` ⇒ rot). Die **Abdeckung** rechnet er aus den Grenzen der Selektionsfalten. Kein `in namen` mehr. Name und Stelle unverändert |
| `H3` | `ohne` = eine **strikte Mehrheit** der Selektionsfalten des Plans (`len(sel)//2 + 1`), die bei jeder Parität beisst. Der Kommentar nennt die Regel und die Zahl mit Stand |

**Vier Gegenproben, alle mit den Funktionen des Tests selbst:** Falte als `bestaetigung` umgewidmet → genau 1× `G6` rot · eine Falte entfernt → genau 1× rot · Registersatz fehlt → 9× rot, Jahre `None` · **`ohne` leer → die Probe scheitert.** ⭐ *Die letzte ist die wichtige: Sie zeigt, dass `H3` aus dem richtigen Grund besteht.*

## 3. Deine Messbitte (23f Abschnitt 6) — beantwortet

**Wer öffnet sie:** `benchmark.py` selbst, über seinen einzigen Aufruf des Faltenplans, kein Nebenweg. Gemessen mit Lesehaken **und Aufrufstapel** in einem Modus-Lauf gegen den Snapshot:

`benchmark.py::je_bot` (Z. 222) → `faltenplan.py::faltenplan` → `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (Z. 133, `read_csv`)

Jede Liste genau einmal, nur im Hauptprozess. Die zehn Kindprozesse öffnen keine, `registerdaten.py` auch nicht. Statisch nennt nur `faltenplan.py` den Pfad. ⭐ Derselbe Lauf lieferte die Tabelle bytegleich `64fb2912…` — die **fünfte** Wiederholung des Determinismusnachweises.

**Gehen die Inhalte ein: JA — über genau eine Grösse, die Faltenlänge.**

| Weg | Befund |
|---|---|
| **(a) Datenfluss** | Gelesen wird nur `entry_time`. Einträge je vollem Kalenderjahr gezählt (Randjahre weg), gemittelt, gegen die Schwelle aus 5.4 verglichen ⇒ Faltenlänge 1 oder 2 ⇒ Faltengrenzen und -namen ⇒ je Falte eine Tabellenzeile. Sonst erreicht nichts aus den Listen die Tabelle |
| **(b) Störprobe** auf Kopien, Originale vorher = nachher | **Eine Zeile entfernt → Tabelle bytegleich.** **Zwei von drei Zeilen entfernt → Tabelle verschieden** (`97cf224f…`); nur der gestörte Bot wechselt von Einjahres- auf Zweijahresfalten, die anderen acht bleiben gleich |

(a) und (b) stimmen überein. ⚠️⚠️ **Die Störprobe, wie der Auftrag sie vorschlug („eine Zeile entfernen genügt"), hätte allein das falsche „nein" ergeben.** Die Inhalte wirken als **Schwellenentscheidung**: Kleine Änderungen sind unsichtbar, ein Übertritt verschiebt den ganzen Faltenplan des Bots.

**Ihr Eingabestand:**

| | gemessen |
|---|---|
| Im Snapshot? | **Nein** |
| Auf der Sperrliste? | **Nein** |
| Im Register genannt? | **Ja, als Quelle, ohne Hash** (5.4). Das *Ergebnis* — die Faltenlänge je Bot — steht registriert in 5.4 und 33.2 |
| Commit | ein einziger: **`78e2bc6`, 13.09.2026** („TB-24: Haltedauern und Zeithorizonte"), seitdem unverändert |
| Deine Unsicherheit („ob es die TB-24-Listen sind") | **Ja** — gemessen an Pfad, Commit und Datum, nicht am Namen. Erzeugt vor TB-31, TB-34 (15.09.) und TB-38, also vor dem Snapshot (19.09.). Die Krypto-Listen beginnen frühestens 2021-09, am damaligen Datenbeginn |

⇒ Nach deiner Unterscheidung ist es der Fall **„sie gehen ein"**: Die Benchmark-Tabelle — und schon der Faltenplan selbst — hat eine Eingabe ohne registrierten Eingabestand. Derselbe Fall wie `messgroessen.json`.

**Zwei Umstände, die deine Entscheidung betreffen, ohne sie vorwegzunehmen:**

1. Die Wirkung läuft **ausschliesslich über die Faltenlänge**, und die ist als **Ergebnis** registriert (5.4, 33.2). Eine Änderung, die eine Faltenlänge kippt, würde deshalb als Abweichung des gerechneten Plans vom Registertext 33.2 sichtbar — ⚠️ **vorausgesetzt, der Plan wird vor dem Lauf gegen ein Abbild geprüft (35.4). Dieses Abbild (33.3) ist nach 33.5 noch nicht erzeugt.**
2. Die Listen stehen in genau einem Commit und sind über `git` reproduzierbar. Ein Nachweis „aus dem registrierten Snapshot" im Sinn von 23d ist mit ihnen **nicht** möglich, weil sie nicht darin liegen.

## 4. ⚠️ Drei Berichtigungen an dir — gemessen

**(a) 23c Abschnitt 3: `benchmark.py` steht an zwei Sperrlistenpunkten, nicht an drei.** Du schreibst, `benchmark.py` an **drei** Punkten sei **ein** Übergang. Gemessen steht es an **zwei** — Punkt 4 und Punkt 6 —, vor und nach TB-94. Dein Satz ist deshalb **nicht** ins Register zitiert; 39.5 nennt die gemessene Zahl. Die Sache dahinter (ein Dateiübergang, mehrere Punkte) trägt trotzdem, sie trägt nur mit zwei.

**(b) 23d, Schritt 1a: `beispieldaten.py` liest keine Tabelle.** Du verlangst, `test_vorregistrierung.py` **und** `beispieldaten.py` sollten dieselbe Konstante lesen. Gemessen: `beispieldaten.py` liest überhaupt keine Benchmark-Tabelle (`grep` 0 Treffer; es erzeugt Rohergebnisse und Benchmark-Tagesreihen). Die vierte Leserin gibt es nicht. Repo-weit sind es **drei**, wie TB-88 gemessen hatte. Ihr Hash ist unverändert `3e547014…`. In 39.2 festgehalten. ⭐ *Deine Bedingung „Test und Lauf dürfen nicht auseinanderfallen" ist erfüllt — sie brauchte nur zwei Dateien, nicht drei.*

**(c) Die Nummer TB-94 in 23f meint jetzt TB-96.** Du nennst für den Eingabestand von `messgroessen.json` die Nummer TB-94; so stand es in unserem Plan vom Vormittag. Weil der Registervollzug vorgezogen wurde, sind die Nummern gerückt: **TB-94 = Register, TB-95 = Testannahmen und Messbitte, TB-96 = `messgroessen.json`.** Im Register als Berichtigung eingetragen (39.8).

## 5. Vorschlag: Registerabschnitt 40 — ⛔ nicht eingetragen, wartet auf dich

> **40. Testannahmen folgen dem Register — `G6` und `H3`**
>
> **40.1 Tatsachennotiz.** `test_vorregistrierung.py` (`73c9b837…`, `9e2a071`) läuft am 23.09.2026 **165/165, rc 0** (534 s). Tag-Vorbedingung 21.9/A4 für diesen Test erfüllt. Geändert nur `G6` und `H3`, keine Prüfung entfallen, kein Sperrlistenhash bewegt, Sonde 0 Befunde.
>
> **40.2 `G6`.** Jahre aus 5.1 Nr. 4, maschinell aus dem Registertext. Abdeckung gerechnet aus den Grenzen der Selektionsfalten des Plans, den `faltenplan.py` bildet. Gemessen vor der Änderung: Die Sache hinter 5.1 Nr. 4 war bei allen neun Bots erfüllt; rot war nur die Formulierung.
>
> **40.3 `H3`.** Strikte Mehrheit der Selektionsfalten auf null Trades. Gemessen: Die vier alten Namen trafen alle, aber vier Nullen verschieben den Median über neun Falten nicht; das kleinste wirksame k ist ⌈n/2⌉. Die Probe beisst wieder; die Gegenprobe mit leerer Menge scheitert.
>
> **40.4 Liste der weiteren Literale** (nicht geändert): Teil D, Teil F, `beispieldaten.py` Z. 69/77. Dazu **F4**.
>
> **40.5 Tatsachennotiz zu 39.8.** Die neun Listen öffnet `benchmark.py` über `fp.faltenplan` → `faltenlaenge_jahre`; ihre Inhalte gehen über die Faltenlänge ein, in beide Richtungen durch Störprobe gezeigt. Aus `78e2bc6` (13.09.2026), nicht im Snapshot. Einordnung nach 23d steht aus.

## 6. Fünf Fragen

**(1) ⭐⭐ Die neun Listen — welche Regel?** Genügt für eine Eingabe, die **nur über eine registrierte Schwellenentscheidung** wirkt, ein Hash-Eintrag (Sperrlistenpunkt oder Tatsachennotiz mit Hash), oder gilt die volle Regel aus 23d — Aufnahme in einen Snapshot und ein Nachweislauf auf demselben Weg? ⚠️ Letzteres ist mit diesen Dateien nicht möglich, ohne sie vorher in einen Snapshot zu nehmen.

**(2) Abschnitt 40 so eintragen?** Oder anders geschnitten — etwa 40.5 als Nachtrag zu 39.8 statt als eigener Unterabschnitt.

**(3) F4 — ein eigener Punkt?** Gemessen: Die Prüfung sagt „Median mit der Null liegt **unter** …", prüft aber mit `<=`. Bei einer Null unter neun Falten sind beide Mediane gleich. **F4 hat nie gebissen.** Das hängt nicht am Faltenplan, ist also nicht die Bauart von `G6`/`H3`, und TB-95 hat es deshalb **nicht** geändert, nur gemeldet. ⚠️ `<=` → `<` würde F4 rot machen; die Probe bräuchte dann ebenfalls eine Mehrheit. Vor dem Tag oder danach?

**(4) Die vier weiteren Literale — bauartgleich umstellen?** Teil D (`"2021"`, `"2020"`), Teil F (`"2022"`) und `beispieldaten.py` Z. 69/77 sind **heute grün, aber nur weil ihr Bot Einjahresfalten hat.** Die Technik wäre dieselbe wie bei `G6`. Offen ist, **welche Registerstelle ihre Jahre trägt** — 4.4 hat den TB-30a-Stand, Teil F ist ein freies Beispiel. ⚠️ Bruchstelle: Bekommt der Bot einmal Zweijahresfalten, bricht Teil D mit `KeyError` ab. ⭐ *Eine Prüfung, die grün ist, weil ihr Literal zufällig noch stimmt, ist genauso gealtert wie eine rote — sie sagt es nur noch nicht.*

**(5) Zwei Sachen an der Sonde.** (i) Ihr Gesamtausgang ist **`2`, nicht `0`** — nicht wegen eines Befunds, sondern weil zwölf der vierzehn Punkte neben Dateien auch Regeln nennen, die kein Hash prüfen kann (auch Punkt 4, schon vor TB-94, wegen „einschliesslich der Interpolationsregel"). Nach deinem 22g-Text ist `2` mit Tatsachennotiz am Tag zulässig — bleibt es dabei, oder soll die Sonde je Punkt zwischen „Pfade geprüft" und „Rest nicht prüfbar" **getrennt** ausgeben? (ii) Die Gruppe „bestimmt" nennt weiter `benchmark_drawdowns_vt.json` mit „Vollzug steht aus". Das steht **fest verdrahtet** in `sperrlistensonde.py`, wird nicht aus dem Abbild gelesen und nicht geprüft. Nach 39.3 ist die Gruppe seit dem Vollzug **leer**. TB-94 hat es gemeldet und nichts geändert (keine `.py`).

## 7. Was mitgeschickt wird — und was nicht

⛔ **Nichts.** Dieser Text ist selbsttragend. Zwei Quellen für denselben Sachverhalt lassen bei jeder Abweichung offen, welche gilt.

⭐ **Wo du nachlesen kannst, wenn du willst:** Der Registerabschnitt 39 steht in der Registerkopie, sobald eine neue gezogen ist (die letzte ist vom 22.09. und kennt 39 nicht). Die Antwort auf die Messbitte liegt ausführlicher in `docs/belege/TB-95/d3_antwort.md` — ⚠️ nach Sichtschutz 27.1 ist `belege/` für dich vor dem Tag gesperrt; sag Bescheid, wenn du eine Passage brauchst, dann kommt sie zitiert.

---

## In einfacher Sprache

Drei Dinge sind fertig, und eine Frage ist beantwortet.

**Fertig:** Der Austausch der Vergleichstabelle steht jetzt auch im Regelwerk, nicht mehr nur im Programm — mit 575 neuen Zeilen, ohne eine einzige gelöschte, und mit neunundzwanzig wörtlich eingesetzten Zitaten. Der alte, überholte Satz wurde nicht entfernt, sondern mit einem Vermerk versehen. Das Schutzabbild ist neu gezogen, die Wache findet keinen Alarm. Und das Prüfprogramm läuft zum ersten Mal vollständig fehlerfrei durch: 165 von 165.

**Dabei hat sich zweimal gezeigt, dass unsere Vermutung falsch war** — beide Male hat die ausführende Sitzung nachgemessen statt bestätigt. Die eine Prüfung scheiterte nicht, weil ihre Jahreszahlen ins Leere griffen, sondern weil aus sieben Zeitabschnitten neun geworden sind und vier veränderte Abschnitte bei neun nicht mehr genügen, um den Mittelwert zu verschieben. Und die Datei, die wir als Quelle des Zeitplans genannt hatten, liest das Programm gar nicht.

**Beantwortet:** Neun alte Handelslisten vom 13. September werden beim Rechnen der Vergleichstabelle geöffnet, und ihr Inhalt wirkt tatsächlich mit — allerdings nur an einer einzigen Stelle: Aus ihnen wird ausgerechnet, ob ein Bot ein- oder zweijährige Zeitabschnitte bekommt. Das ist eine Ja-Nein-Schwelle. Eine kleine Änderung an einer Kopie ändert nichts, eine grosse kippt die Schwelle und damit den ganzen Zeitplan des Bots. Die Listen gehören nicht zum eingefrorenen Datenbestand.

**Zu entscheiden bleibt:** wie diese neun Listen zu behandeln sind; ob der vorgeschlagene neue Regelwerksabschnitt so eingetragen wird; und ob drei kleinere Funde — eine Prüfung, die durch einen Vergleichsfehler nie angeschlagen hat, vier weitere eingetippte Jahreszahlen, die heute nur zufällig noch passen, und zwei Eigenheiten der Wache — vor dem Stichtag behoben werden.
