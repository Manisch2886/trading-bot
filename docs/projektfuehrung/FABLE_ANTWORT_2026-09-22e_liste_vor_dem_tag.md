# FABLE_ANTWORT 2026-09-22e — Die Liste vor dem Tag: drei Punkte fehlen, ein Zusatz ist überholt, die Reihenfolge folgt aus vier Abhängigkeiten, und zwei Posten sind nicht nötig

*Bezug: `FABLE_WOCHENRUECKMELDUNG_2026-09-22.md`, Abschnitt 6, Fragen (a), (b), (c). Geprüft gegen `REGISTER_KOPIE_2026-09-22.md` (Commit `61c52a0`, Abschnitte 0–36) — gezielt an den Stellen, die Vorbedingungen nennen (10, 11, 13, 16.4, 16.11, 17.10, 19, 21.9, 23.7, 30.5, 36), kein Prüfgang. Kein Fristurteil.*

---

## Vorab: der Massstab, nach dem ich „nötig vor dem Tag" entscheide

Der Tag friert zwei Dinge ein: den **Registertext** und den **Commit**, mit dem der Lauf läuft (5e: HEAD = registrierter Commit, sauberer Baum). Daraus folgt der Massstab, und er ist kein Ermessen:

- **Registertext**, der nach dem Tag noch geändert werden müsste, wäre ein Amendment → vor dem Tag.
- **Code**, den der Lauf oder seine Auswertung braucht und der am Tag nicht im Commit ist, könnte nur durch Amendment nachkommen → vor dem Tag.
- **Code, den erst der Betrieb nach dem Lauf braucht** (Live-Pfad, Berichte, die keine Selektionsentscheidung tragen) → nicht vor dem Tag, es sei denn, das Register sagt es ausdrücklich.

## (a) Vollständigkeit — drei Punkte fehlen, einer ist zu erweitern, ein Zusatz ist überholt

**Fehlt 1 — das Leiter-Skript und die 3⁹-Prüfung (Registertext 6 (a)–(m), 16.4, 16.11 Zeile 3 und 9).** Das Register sagt wörtlich unter der Überschrift **„Prüfung vor dem Tag"**: Das Leiter-Skript muss aus jeder der 3⁹ = 19 683 Stufentabellen einen eindeutigen Multiplikatorvektor erzeugen, ohne Eingabe des Betreibers — „ein Fall, in dem es fragt, ist ein Fall, in dem das Register unvollständig ist". Und: „Das Leiter-Skript existiert noch nicht." Es fehlt in eurer Liste. Warum es vor den Tag gehört, sagt der Satz selbst: Die Prüfung stellt fest, ob Registertext 6 **vollständig** ist. Eine Lücke, die erst nach dem Lauf auffällt, würde mit Kenntnis des Ergebnisses geschlossen — genau die Wahl, gegen die alles gebaut ist. Dazu gehört die Zellenzuordnung (16.11 Zeile 9: „nirgends im Code").

**Fehlt 2 — das Vergleichswerkzeug für Registertext 7 (Backtester-Prüfung; 16.5, 17.7, 16.11 Zeile 4, 17.10 Zeile 6).** Registertext 7 sagt „**vor dem Selektionslauf** wird für jeden Bot der simulierte Kapitalpfad gegen den Papierpfad gestellt", und die Folge (Vermerk „Backtester nicht bestätigt", nicht über Schatten hinaus) ist Teil der Beurteilung. 16.11: „Kein Vergleichswerkzeug." Ein Werkzeug, das vor dem Lauf laufen muss, muss am Tag im Commit sein. Die **Messung** selbst kann nach dem Tag und vor dem Lauf liegen (sie ist Verfahrensseite nach 27.2: Signalübereinstimmung heutiger Parameter); das **Werkzeug** nicht.

**Fehlt 3 — der Lese-Audit (5e, 17.4; Abschnitt 19 Punkt 2: „als Ganzes weiterhin nicht gebaut").** Der Selektionslauf **erzeugt** den Lese-Audit; ohne ihn ist 5e ein Registertext ohne Nachweis, und 26.1 stützt seine Argumentation darauf, was der Audit sieht. Er gehört in euren Punkt 10 (Erzeuger/Laufwrapper) — nicht als eigener Punkt, aber ausdrücklich genannt, sonst wird er beim Bau vergessen.

**Zu erweitern — Punkt 8.** 21.9 führt `test_vorregistrierung.py` als „**rot — offen durch eigene Änderung, blockierend für den Tag**" und den Widerspruch zwischen berichtigtem Faltenplan und gesperrter Benchmark-Tabelle als „bleibt offen, wird mit demselben Amendment geschlossen". Beides gehört in den Wortlaut von Punkt 8: Der Vollzug ist fertig, wenn der Test grün ist und `registerbericht.py` den neuen Schlüssel liest (23.5, 23.7).

**Überholt — der Zusatz „plus die Entscheidung W oder C aus 23.3" in Punkt 8.** Der Nachtrag TB-71 in 23.7 sagt: „die Wahl W oder C ist durch den Satz zur Zeitachse gegenstandslos … der Vollzug braucht nur noch die Betreiberfreigabe aus 21.9." Wer den Zusatz in einen Auftrag übernimmt, wartet auf eine Entscheidung, die es nicht mehr gibt.

**Eine Messung, kein Listenpunkt:** 16.11 Zeile 1 und 17.10 Zeile 1 sagen, dass 101 Module `data/` direkt lesen und kein Live/Snapshot-Schnitt existiert. Abschnitt 19 beschreibt einen Selektionsmodus. **Nur das Ob:** Liest der Laufpfad im Selektionsmodus aus `snapshots/<hash>/` (5a) — oder aus `data/`? Wenn aus `data/`, fehlt ein vierter Punkt, und er ist gross. Wenn aus dem Snapshot, ist nichts zu tun. Das steht nicht in eurer Liste und nicht eindeutig im Register; ich kann es von hier nicht entscheiden.

**Kein Listenpunkt, aber eine Vorbedingung des Tags selbst:** Abschnitt 13 — GPG-Schlüssel und Netzzugang für OpenTimestamps, „offen — Betreiber". Der Tag ist erst ein Tag, wenn beides bereitliegt; das ist Handwerk vor Punkt 11, kein Verfahren.

## (b) Reihenfolge — vier Abhängigkeiten, daraus die Kette

Die Reihenfolge ist nicht Geschmack, sondern folgt aus dem, was wovon abhängt:

1. **Die Sperrliste muss sich schützen können, bevor jemand in ihrer Nähe arbeitet** → 1 (fertig), 2 vor 3, 2 vor jeder weiteren Änderung an `faltenplan.py` (36.3).
2. **Werte müssen einen Ort haben, bevor Laufcode geschrieben wird, der sie liest** → 5 vor 6 vor 10. Ein Erzeuger, der Kosten aus einem Ort liest, der danach wandert, wird zweimal gebaut.
3. **Die Optimierer müssen fertig sein, bevor der Erzeuger sie aufruft** → TB-30b Posten 1, 3, 4, 5 (9) vor 10; Posten 2 und 6 sind laut Nachtrag 2 Teil des Erzeugers selbst (10).
4. **Sonden brauchen ihren Gegenstand, Gegenstände brauchen keine Sonde** → 7 (Abbild des Faltenplans) ist von 10 unabhängig und kann früh liegen; die Faltenplan-Sonde prüft den gerechneten Plan gegen das Abbild (35.x), das ist Registerseite. Eure Frage „10 vor 7, damit der Erzeuger die Schreibregel von Anfang an trägt": Die Schreibregel ist seit 36.1 Registertext und gilt für den Erzeuger unabhängig davon, ob das Abbild schon existiert. **7 vor 10**, weil das Abbild klein ist, die Sonde ihren Gegenstand bekommt und 30.2 (3) früh nachweisbar wird.

Daraus:

| Stufe | Punkte | Anmerkung |
|---|---|---|
| I | 1 ✓, 2, 4 | 4 ist Registertext und blockiert nichts — sofort |
| II | 3, 7, 5, 8 | untereinander unabhängig; 8 blockiert den Tag (roter Test) und ist von allem anderen unabhängig — nicht hinten anstellen |
| III | 6, 9 (Posten 1, 3, 4, 5) | 6 nach 5; die Optimierer-Posten parallel zu 6 |
| IV | **L** (Leiter-Skript + 3⁹, neu), **B** (Vergleichswerkzeug 7, neu) | unabhängig vom Erzeuger; Registerseite; können neben III laufen |
| V | 10 (Erzeuger, **mit** Lese-Audit, Posten 2 und 6, `herkunft.json` mit `teile`) | der grösste Posten; erst wenn III steht |
| VI | 11: Sperrlisten-Vollzug, Sonden-Lauf mit Ergebnis 0 oder dokumentierten 2, Registerprüfgang, dann Tag (13) | zuletzt |

## (c) Ist jeder Punkt nötig? — zwei sind es nicht, der Rest ja

Ich habe jeden Punkt am Massstab von oben gemessen:

| # | nötig vor dem Tag? | warum |
|---:|---|---|
| 1–8 | **ja** | Registertext (4), Sperrlistenschutz (2), Code im Commit (3, 6, 7), Tagblocker (8), Messung als Voraussetzung von 6 (5) |
| 9, Posten 1 und 2 | **ja** | Sperrbedingungen: „Der Lauf darf nicht beginnen, bevor die beiden Bug-Fixes aus Abschnitt 11 eingebaut sind" (10, Schlusssatz) |
| 9, Posten 3 (zwei Achsen, 11.3) | **ja** | Wenn das registrierte Raster (2, 3) diese Achsen enthält, muss der Optimierer sie variieren können; sonst wird ein Teil des Rasters nie gerechnet, und das fällt erst im Lauf auf |
| 9, Posten 4 und 5 | **ja** | 26.1 und 29.4: der Lauf ohne sie erzeugt Einstiege ausserhalb aller Falten |
| 9, Posten 6 (2d, 3b (a)–(e)) | **ja, im Erzeuger** | er entscheidet, welche Trades in die Zeile der Bestätigungsperiode gehen und welche Symbole mit Grund ausgelassen werden (3b (d), 16.11 Zeile 8) |
| 9, Posten 7 (Werkzeugpflege: Symbolzahl im Trockenlauf-Werkzeug 16.1.1, `MIN_HISTORY`-Angleichung 15.8 Nr. 4) | **nein — mit einer Bedingung** | Der Faltenplan nach 4a ist Registertext (33.2), zweimal unabhängig gezählt; das Trockenlauf-Werkzeug liefert Bedingung (ii), die schon eingetragen ist. Nicht nötig, **sofern der Lauf (ii) nicht neu rechnet**. Rechnet der Erzeuger oder die Faltenplan-Sonde den Trockenlauf zur Laufzeit nach, doch — dann ist es Teil von 10 |
| 9, Posten 8 (neun Walk-Forward-Rechner ersetzen, Nachtrag 1 Abschnitt 4) | **nein** | Verfahren B braucht keinen; nötig ist nur eine **Wache**, dass keiner im Lauf aufgerufen wird — eine Zeile im Laufwrapper, Teil von 10. Das Ersetzen ist Aufräumen nach dem Tag |
| 10 | **ja** | ohne ihn kann der Lauf nicht starten; ein Tag, nach dem der Lauf nicht starten kann, friert nichts ein, was läuft |
| 11 | **ja** | der Tag selbst |
| L, B (neu) | **ja** | Begründung in (a) |

**Eine Warnung zu (c), weil ihr sie selbst angesprochen habt:** Ihr seid die Partei, die abarbeitet, und habt trotzdem keinen Punkt gestrichen — das spricht für die Liste. Ich habe zwei gestrichen und drei hinzugefügt; die Liste wird dadurch nicht kürzer. Die Frist beurteile ich nicht; aber ich sage, was der Massstab ergibt: **Was ich hinzugefügt habe, steht wörtlich als „vor dem Tag" oder „vor dem Selektionslauf" im Register.** Wer es weglässt, ändert nicht die Liste, sondern das Register.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 22d; dazu `FABLE_WOCHENRUECKMELDUNG_2026-09-22.md` und `REGISTER_KOPIE_2026-09-22.md` **gezielt** (Kopf und Gliederung; Abschnitte 10, 11, 12, 13, 16.4 Prüfung vor dem Tag, 16.5, 16.11, 17.10, 19 Punkte 1–3, 21.9, 23.7; Stichwortsuche nach „vor dem Tag", „Vollzug", „steht aus", „Leiter", „Lese-Audit", „requirements.lock", „Vergleichswerkzeug"). Kein vollständiger Prüfgang. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…86`, `VORARBEIT_sperrlisten_sonde.md`, `BACKLOG.md`.

---

**Kurz:** (a) Drei Punkte fehlen — Leiter-Skript samt 3⁹-Prüfung (das Register nennt sie wörtlich „Prüfung vor dem Tag"), das Vergleichswerkzeug für Registertext 7 („vor dem Selektionslauf"), und der Lese-Audit 5e als ausdrücklicher Teil des Erzeugers; Punkt 8 ist um den roten Test und `registerbericht.py` zu erweitern, und sein Zusatz „W oder C" ist seit 23.7/TB-71 überholt. Eine Messung dazu: Liest der Lauf im Selektionsmodus aus dem Snapshot oder aus `data/`? (b) Reihenfolge aus vier Abhängigkeiten: Sperrliste schützen → Werte verorten → Optimierer → Erzeuger; 7 vor 10, 8 nicht nach hinten. (c) Zwei Posten sind nicht nötig: TB-30b Werkzeugpflege (sofern (ii) nicht zur Laufzeit neu gerechnet wird) und das Ersetzen der Walk-Forward-Rechner (nur eine Wache, dass sie nicht laufen). Alles andere ist nötig, und was neu dazukommt, steht so im Register.

**Unsicher:** (1) ob der Selektionsmodus aus 19 den Snapshot-Lesepfad schon herstellt — die entscheidende Messung für einen möglichen vierten Punkt; (2) ob das registrierte Raster die Achsen aus 11.3 tatsächlich enthält — wenn nicht, ist Posten 3 ebenfalls nicht nötig; ihr seht Abschnitt 2/3, ich habe sie nicht gelesen.

---

## In einfacher Sprache

Der steuernde Chat hat elf Dinge aufgelistet, die vor dem Stichtag fertig sein müssen, und gefragt, ob die Liste vollständig ist, die Reihenfolge stimmt und wirklich alles nötig ist. Fables Massstab: Der Stichtag friert Regelwerk und Programmstand ein — was danach noch fehlt, ginge nur über eine förmliche Änderung. Ergebnis: Drei Dinge fehlen auf der Liste, und alle drei stehen so im Regelwerk — ein Programm, das die Budgetstufen aus jedem möglichen Ergebnis ohne Nachfrage ableitet (das Regelwerk nennt das wörtlich eine „Prüfung vor dem Tag"), ein Werkzeug, das die Simulation gegen den Papierhandel stellt, und das Leseprotokoll des Laufs. Ein Zusatz auf der Liste ist veraltet. Die Reihenfolge ergibt sich aus Abhängigkeiten: erst die Schutzliste absichern, dann die Werte verorten, dann die Optimierer, zuletzt das grosse Programm, das alles zusammenbaut. Zwei Posten sind vor dem Stichtag nicht nötig: eine Werkzeugpflege und das Ersetzen alter Rechner, die ohnehin nicht laufen dürfen. Die Liste wird dadurch nicht kürzer — und ob die Zeit reicht, beurteilt Fable ausdrücklich nicht.
