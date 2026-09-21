# Journal-Nachtrag (m) — 21.09.2026, TB-64: der Wächter für die Bringschuld der Nachträge

**Quelle:** Mac-Sitzung **TB-64 Nachtragswaechter**, 21.09.2026, ab 07:01
Ortszeit, Ausgang `2150318` (= `origin/main` beim Start), Interpreter
`trading-env/bin/python3` 3.9.6. Commits `ff2e5ab` (Schritt 0, zwei
Betreiber-Dateien), `54b27ce` (Schritt 1, Messung), `b220c8f` (Schritt 2, 18
Dateien verschoben), `2c4af5b` (Schritt 3, Wächter und Test), `4ca8af9`
(Schritt 4, Quellenvermerk im Dokumentationsstandard), `3f22443` (Schritt 5
und 5b, Cron-Zeile und `UMGEBUNGEN.md`), `9a51add` (Schritt 6, dieser Nachtrag,
`docs/ERGEBNIS_TB-64_nachtragswaechter.md`). **Einzuarbeiten als nächster
Block nach dem höchsten vorhandenen** (am 21.09.2026 gemessen: `BT`;
`(20g)` bis `(20l)` liegen davor — die Nummer vergibt die einarbeitende
Sitzung). *Der Buchstabe `(m)` ist der nächste freie nach `(20l)`; dass er mit
dem Backlog-Nachtrag `(m)` vom 19.09. zusammenfällt, der der Anlass dieser
Aufgabe war, ist Zufall der Zählung.*

⭐ **Quellenzeile für den Block, wörtlich zu übernehmen:**

```
*Quelle: `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-20m.md`*
```

---

## Was der Auftrag wollte und was er bekam

Der Weg *Nachtrag schreiben → irgendwann einarbeiten* hatte keine Wache
ausser dem Gedächtnis. Der Auftrag wollte einen rein lesenden Wächter mit zwei
Prüfungen — was liegt offen, und ist von den verschobenen wirklich alles
angekommen — samt sieben Mutationsfällen, dazu den Quellenvermerk im Journal
als Regel, die Cron-Zeile zum Kopieren, und (Schritt 5b, Betreiberentscheidung
vom 20.09.) die drei `B`-Zeilen aus Backlog-Nachtrag `(m)` nach
`docs/UMGEBUNGEN.md`.

**Bekommen hat er** `system/nachtragswaechter.py` (518 Zeilen, nur
Standardbibliothek, 0,4 s für 36 Dateien) mit `system/test_nachtragswaechter.py`
(62 Prüfungen in zwölf Fällen, alle sieben des Auftrags wie erwartet; vier
Mutationen am Wächter machen den Test rot mit 3/3/4/3 Prüfungen), den sechsten
Eintrag `nachtraege` in `notifications/waechter_melden.py`, Regel 10 im
Dokumentationsstandard, den neuen Abschnitt in `UMGEBUNGEN.md` — und einen
Nachtragsordner, in dem **nur noch die sechs offenen Journal-Nachträge
`(20g)`–`(20l)` liegen** (plus dieser hier): 19 Backlog-Nachträge sind nach
`_eingearbeitet/` gewandert, jeder mit gemessenem Grund.

---

## Vier Befunde, die keiner bestellt hat

**1. Der Auftrag beschrieb einen Stand, der beim Lesen zwei Aufgaben alt
war.** Abschnitt 0 (Stand `4b85f0e`) nannte 26 offene Dateien, `(v)` nicht
eingearbeitet, `(g)`/`(20a)`/`(20b)` nicht im Journal, `(f)` nicht prüfbar.
Gemessen an `ff2e5ab`: TB-62 und TB-67 waren inzwischen gelaufen — 25 Dateien
im Hauptordner, 11 unter `_eingearbeitet/`, `(v)` mit 22 von 22 im Backlog,
alle elf Journal-Nachträge eingearbeitet, `(f)` prüfbar. Der Auftrag hatte das
selbst vorhergesehen (*„Weicht es ab, gilt deine Messung"*), und die Messung
galt.

**2. ⭐⭐ Ein Wächter, der nur Nummern vergleicht, hätte den Fall, für den er
gebaut wird, grün gemeldet.** Die grep-Zählung meldet für `(m)` 6 von 6
K-Nummern und 2 von 2 Blöcke „im Ziel" — mit fremdem Inhalt: `K2l`–`K2o`
tragen `(s)`/`(t)`, `K2p`/`K2q` tragen `(n)`, Block `2s` ist der Block aus
`(s)`/`(t)`/`(u)`. Deshalb prüft der Wächter je Nummer den **Textkern** (die
ersten 40 Zeichen hinter der Nummernzelle) und akzeptiert einen Vergabevermerk
nur, wenn er **den Nachtrag selbst nennt**. Ein Vermerk ohne diese Bindung war
messbar zu weit: er hatte `B1` über die Zeile `K24` als angekommen gewertet.

**3. Eine vierte Kennungsklasse hätte den Wächter zum Dauermelder gemacht.**
Punktzeilen wie `T46.1a`, `B1`, `F0` hätten `(q)`, `(r)`, `(u)` prüfbar
gemacht — und `(m)` sieben `B`-Zeilen gegeben, von denen nach Schritt 5b drei
in `UMGEBUNGEN.md` und drei in der Übergabe vom 19.09. stehen, beides kein
Ziel des Wächters. `(m)` wäre in `_eingearbeitet/` für immer *falsch
verschoben* gewesen. Gewählt: die drei Klassen des Auftrags; die vier
Nachträge ohne solche Nummer sind **nicht prüfbar (A2)** und wurden einmalig
von Hand gemessen (`KG0`–`KG9` 10/10, `KG-F0`–`F12` 13/13, `RT0`–`RT9` 10/10,
`RT-F0`–`F11` 12/12, `T46.1a`–`d` 4/4, Berichtigung viermal zitiert plus
`K3e`).

**4. Die zwei Zeilen, die per Telegram gehen, dürfen kein Alter tragen.** Der
Wrapper dämpft Wiederholungen über den Fingerabdruck genau dieser Zeilen; ein
Alter, das täglich um eins wächst, wäre täglich ein „geänderter Befund", und
die Dämpfung griffe nie. Das Alter je Datei steht in den Dateizeilen, die
vollständig im Log landen.

---

## Wo der Auftrag danebenlag, und was gilt

| Auftrag | gemessen / gebaut |
|---|---|
| 26 offene Dateien, `_eingearbeitet/` anlegen | 25 + 11; der Ordner existierte seit TB-67 |
| `(c)`, `(d)`, `(e)` ohne Quellenvermerk — nachtragen | seit TB-67 vorhanden; **0** nachzutragen, **0** nicht zuordenbar, `JOURNAL.md` unberührt |
| Meldung über `shared/telegram_*` bzw. den Weg der vier Wächter, „mach es genauso" | genauso — und genauso heisst: ein Registereintrag in `notifications/waechter_melden.py` und die Cron-Zeile im Wrapper-README, **zwei Dateien ausserhalb `system/` und `docs/`** (21 Zeilen, 0 entfernt), im Ergebnisdokument benannt |
| Befund = offener Nachtrag | offener Nachtrag **über der Frist** (Standard 1 Tag, einstellbar) — *„eine Nachricht, wenn eine zu lange liegt"* |
| „Nur verschieben, was nach Nummern geprüft ist" | 14 Dateien über K/Block/Kette; 4 ohne solche Nummer nach Handmessung verschoben — sie liegen für den Wächter als `[?]` unter `_eingearbeitet/`, kein Befund, aber sichtbar |
| `(m)` erst nach Schritt 5b | so gemacht — obwohl der Wächter `(m)` schon vorher als „alles angekommen" führte, weil `K4b`/`K4g` seine Nummern mit `(m)` und „vergeben" nennen |

---

## Fehler → Regel

| Fehler | ⇒ Regel |
|---|---|
| Der erste Vermerk-Entwurf verlangte nur Nummer + „vergeben" in einer Zielzeile; `B1` traf `K24`, `K2p` traf `MI2` | ⭐ Ein Vermerk, der eine Nummer als angekommen erklärt, muss **den Nachtrag nennen**, aus dem sie stammt — sonst ist jede Zeile mit dem Wort „vergeben" ein Vermerk |
| Beim Übertragen von B3 nach `UMGEBUNGEN.md` war ein Punkt vor `**` ergänzt; die Wortlaut-Probe (`in` nach Normierung) hat ihn gefunden | ⭐ Wörtlich übernommener Text wird **maschinell** gegen die Quelle geprüft, nicht mit dem Auge — auch bei drei Zeilen |
| Mutation A (schliessender Balken) liess Fall 4 zunächst grün, weil die Kernsuche „anderswo" die übersehene Zielzeile fand — der Test prüfte das Ergebnis, nicht den Weg | ⭐ Eine Mutationsprobe prüft, **auf welchem Weg** das Ergebnis zustande kam; ein zweiter Mechanismus kann den Ausfall des ersten verdecken |

---

## Der Stand am Morgen des 21.09.

Der Wächter gibt gegen das Repo **0** zurück: nichts über der Frist, nichts
falsch verschoben, keine Nummer doppelt. Ab dem zweiten Morgen nach ihrer
Entstehung wird er die Journal-Nachträge `(20g)`–`(20m)` melden — das ist die
offene Bringschuld an das Journal (Blöcke ab `BU`), kein Fehlalarm. **Die
Cron-Zeile ist nicht eingetragen**; sie steht in drei Dokumenten zum Kopieren.

---

## In einfacher Sprache

**Was wir wissen wollten:** Ob eine Notiz, die neben dem Journal oder der
Aufgabenliste liegt, je wieder auffällt, wenn sie nicht übertragen wird.

**Was herauskam:** Bisher nicht. Jetzt sieht ein Programm jeden Morgen nach:
Was liegt länger als einen Tag im Notizordner? Und was in den Ordner
„erledigt" geschoben wurde — steht das wirklich in der Liste? Dabei hat sich
gezeigt, dass es nicht reicht, die Nummern zu vergleichen: Bei der Notiz vom
19. standen alle sechs Nummern in der Liste, aber mit fremdem Text. Das
Programm vergleicht deshalb auch den Anfang des Textes. Neunzehn erledigte
Notizen sind in den Unterordner gewandert, sechs Journal-Notizen der letzten
zwei Tage warten noch — und das Programm wird das melden, sobald du die
Cron-Zeile einträgst.
