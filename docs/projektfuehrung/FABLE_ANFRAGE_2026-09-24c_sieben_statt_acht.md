# FABLE_ANFRAGE 2026-09-24c — Es sind sieben Mutationsproben, nicht acht; dein Beispiel für `beispieldaten.py` hätte zwei Bots unzulässig gemacht; und die Sonde liest ihre Gruppen jetzt aus dem Abbild

*An den Verfahrensprüfer. Bezug: `FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md`, Abschnitte 5–7. TB-97 ist abgegeben. **Drei Befunde**, davon zwei an deinen Texten, und **vier Fragen**.*

⚠️ **Sichtschutz 27.1 gewahrt.** Prüfungsnamen, Faltennamen und Drawdown-Werte des Testrahmens sind Verfahrensseite (27.2). Die Drawdown-Zahlen in Abschnitt 3 stehen bereits als Registertext in 4.4.

---

## 1. Vollzug

`test_vorregistrierung.py` läuft **188/188, rc 0**, in 781 s. **23 Prüfungen sind
dazugekommen — alle Gegenproben.** Keine entfallen, keine abgeschwächt, keine
Ausnahme, keine Toleranz. Von 28 gemessenen Pfaden haben sich **genau vier**
bewegt; alle Sperrlistendateien, beide Abbilder, `faltenplan.json` und alle
Benchmark-Tabellen sind gleich. Die Sonde meldet gegen das echte Abbild 0 Befunde.

| | |
|---|---|
| `F4` | `<=` → `<`, Menge als strikte Mehrheit aus dem Plan. Gegenprobe: leere Menge ⇒ scheitert ✔ |
| Teil D | liest nicht mehr Jahre, sondern **die Regel am heutigen Plan**: ruhigste Falte ⇒ `DD_Toleranz` bindet, schwerste ⇒ relative Grenze. Gegenproben vertauscht ⇒ beide scheitern ✔ |
| Teil F | Mehrheit aus dem Plan ✔ |
| Sonde | getrennte Schlusszeilen; Gruppen aus dem Abbild; `BESTIMMT_NICHT_EINGETRAGEN` entfernt; Sondentest **59/59** (vorher 49/49) |

## 2. ⚠️⚠️ Befund 1: Es sind **sieben** Mutationsproben, nicht acht — und `F4` ist keine davon

Deine Regel aus 40.7 verlangt Gegenproben für „alle acht". Der Auftrag liess sie
deshalb zuerst **benennen**, statt sie zu zählen. Gemessen nach dem Kriterium
„verändert den Code, wertet neu aus, prüft auf Unterschied":

| | |
|---|---|
| Teil H hat **acht** Prüfungen | **H0 bis H7** |
| **H0 ist der Grundlauf ohne Mutation** | ⇒ **sieben** Mutationsproben |
| ⚠️ **`F4` ändert keinen Code** | Es vergleicht im selben Prozess zwei Mediane derselben Werte |

**Woher die Acht stammt, gemessen:** Am Stand `a2fcf01` (TB-30a) stehen dieselben
acht `pruefe("H…")`-Aufrufe. Der TB-30a-Testauftrag sagt *„Teil H startet acht
eigene Prozesse"*. ⇒ **Gezählt waren Prozesse, nicht Mutationen** — und der
Grundlauf ist mitgezählt.

⇒ **Register 12 („150 Prüfungen, davon acht Mutationsproben") und dein 40.7
(„alle acht") tragen eine Zahl, die als Aussage nicht stimmt.** Beide bleiben
zeichengleich stehen; die Berichtigung gehört in Abschnitt 41.

⭐ **Das ist genau der Fall, den deine Frage-3-Antwort vorhergesagt hat:** *„Am
Tag muss diese Zahl wahr sein — nicht als Anzahl, sondern als Aussage."* Sie war
es nicht, und ohne die Namen hätte es niemand gemerkt. ⇒ **Unsere Frage (3) aus
24b beantwortet sich damit selbst:** Eine Zahl ohne Namen ist nicht prüfbar.

**Alle sieben beissen heute.** `F4` ist der einzige Fall, der nie gebissen hat.

⚠️ **Ein Nebenbefund, der die Sieben erklärt:** **H6 trägt nur zusammen mit H5.**
H6 entfernt eine Wache und prüft auf rc 0 — ohne H5s eingesetzten Fehler ist rc 0
trivial, und H6 besteht auch ohne seine eigene Mutation. Die Gegenprobe lässt
deshalb nur H6s Mutation weg; die Fehlerzahl aus H5 bleibt immer stehen.
⭐ *Zwei Proben, die sich eine Kopie teilen, sind nicht zwei unabhängige Wachen.*

## 3. ⚠️⚠️ Befund 2: Dein Beispiel für `beispieldaten.py` hätte zwei Bots unzulässig gemacht

Du schreibst in 24a Abschnitt 6:

> wo sie nur „irgendeine Selektionsfalte" braucht (Teil F, freies Beispiel; `beispieldaten.py` Z. 69/77), nimmt sie sie aus dem Plan (`faltenplan.py`), **z. B. die zweite Selektionsfalte des Bots**, ohne Literal.

**Gemessen: Für Teil F trifft das zu. Für `beispieldaten.py` Z. 69 nicht.** Die
Zeile setzt in den „Krisenfalten" einen tiefen Benchmark-Drawdown. Damit die
Beispieldaten zulässig bleiben, muss die gewählte Falte einen Drawdown tragen,
der **bei der gesetzten Exposure die Bedingung besteht** — nicht jede tut das.

| Wahl | Ergebnis |
|---|---|
| **Zweite Selektionsfalte** (dein Beispiel) | ⛔ bei **zwei Bots** wären die Beispieldaten **in jeder Zelle unzulässig** |
| Die Falten, die **2020 und 2022 aus 5.1 Nr. 4** abdecken | ✔ bestehen bei **allen neun** |

⇒ Umgestellt ist auf die **zweite** Form — also nicht „irgendeine Falte aus dem
Plan", sondern „die Falte, die das registrierte Testjahr abdeckt", per Abdeckung
gerechnet wie `G6`. **Das weicht vom Wortlaut deiner Regel ab und braucht deine
Kenntnisnahme.**

⭐ **Der Grund, warum es trotzdem deine Regel ist:** Das Literal ist weg, und die
Quelle ist das Register statt des Codes. Nur die Registerstelle ist eine andere
als die, die du vermutet hast.

⚠️ **Eine Folge, die wir melden, weil sie eine Wache betrifft:** **5.1 Nr. 4 hat
jetzt einen zweiten Leser** (`beispieldaten.py`), aber weiterhin nur einen
Parser. Die Marke an dieser Zeile nennt nur `G6`.

## 4. ⚠️ Befund 3: Das echte Abbild führt die Gruppen nicht

Deine Antwort zu Frage (5)(ii) verlangt, dass die Sonde **alle drei** Gruppen aus
dem Abbild liest. Gemessen: Das heutige Abbild führt **nur `punkte`** — weder
`bestimmt` noch `eingefroren`. Der **Erzeuger** musste deshalb mit umgebaut
werden (`bestimmt` aus einem Argument, `eingefroren` per `ast` aus
`herkunft.py`, ⛔ ohne es auszuführen oder zu ändern).

| | |
|---|---|
| Unterschieden wird jetzt | **fehlende Gruppe = 2**, **leere Gruppe = 0** — verschiedene Aussagen |
| Gegen das heutige Abbild | beide Gruppen **2** („nicht im Abbild"). Am Gesamtwert ändert das nichts, er war schon 2 |
| ⛔ | **Ein echtes neues Abbild wurde NICHT erzeugt.** Das gehört zum Sperrlisten-Vollzug und braucht Freigabe (36.6/37.3). Gemeldet, nicht getan |
| ⚠️ | Die Ausgabe nennt `benchmark_drawdowns_vt.json` **nicht mehr**. 39.3 und 39.9 beschreiben die alte Ausgabe; beide bleiben zeichengleich, die Berichtigung gehört in 41 |

⭐ **Und ein Nebenergebnis deiner eigenen Forderung:** Die neue Regelzeile zeigt
für **alle zwölf** Punkte „keine Tatsachennotiz im Abbild". ⇒ Die Tag-Vorbedingung
aus 23c („jede 2 mit Tatsachennotiz") ist **offen** — neu ist das nicht (39.9
sagte „hier nicht geprüft"), aber jetzt **steht es in der Ausgabe**, statt
gerechnet werden zu müssen. Genau das wolltest du.

## 5. Vier Fragen

**(1) ⭐⭐ Die Berichtigung der Zahl.** Register 12 sagt „acht Mutationsproben",
gemessen sind es sieben, und `F4` ist keine. Wie soll 41 das fassen — als
**Berichtigung zu 12 mit Namen** (H1–H7, und `F4` ausdrücklich als Nicht-Mutation
mit eigener Gegenprobe), oder anders? ⭐ *Wir schlagen Namen vor: Die Messung hat
gezeigt, dass eine Zahl ohne Namen drei Wochen falsch sein kann, ohne dass es
auffällt.*

**(2) Befund 2 (Abschnitt 3)** — nimmst du die Abweichung von deinem Beispiel an?
Und soll die **Marke bei 5.1 Nr. 4** um den zweiten Leser ergänzt werden?

**(3) H6 (Abschnitt 2, Ende)** — eine Probe, die nur zusammen mit einer anderen
trägt, ist keine unabhängige Wache. Bleibt sie so, mit Notiz, oder soll sie vor
dem Tag **eigenständig** gemacht werden?

**(4) Das neue echte Abbild.** Es ist Voraussetzung dafür, dass die Gruppen nicht
mehr als „2" gemeldet werden — und **TB-98 braucht ohnehin eines**, weil
`faltenplan.py` (Sperrlistenpunkt 2) dort eine registrierte Pfadkonstante
bekommt. ⇒ Genügt **ein** Abbild nach TB-98, das beides schliesst, oder verlangst
du vorher eines für die Gruppen allein? ⭐ *Wir neigen zu einem: 22g sagt, nicht
nach jeder Änderung ein Abbild, sondern nach Bündeln.*

## 6. Was mitgeschickt wird

⛔ **Nichts.** Der Text ist selbsttragend. `belege/` bleibt nach 27.1 gesperrt.

---

## In einfacher Sprache

Das Prüfprogramm hat jetzt 188 Prüfungen statt 165 — 23 davon sind Gegenproben,
also Nachweise, dass eine Probe überhaupt anschlagen kann. Alles läuft fehlerfrei.

**Dabei sind drei Dinge herausgekommen, die niemand erwartet hatte.**

Das Regelwerk behauptet seit drei Wochen, es gebe **acht** solcher Proben. Es
sind **sieben**. Mitgezählt war ein Durchlauf ohne jede Verfälschung — er prüft,
dass ohne Eingriff alles normal aussieht, aber er ist keine Probe. Und die
Prüfung, wegen der die ganze Regel entstanden ist, gehört gar nicht zu dieser
Gruppe. Aufgefallen ist das nur, weil der Auftrag verlangt hat, die Proben erst
zu **benennen** statt sie zu zählen.

Zweitens hatte der Verfahrensprüfer vorgeschlagen, eine bestimmte eingetippte
Jahreszahl durch „irgendeinen Zeitabschnitt aus dem Plan" zu ersetzen. Gemessen
hätte das bei zwei Bots die Testdaten unbrauchbar gemacht — der Abschnitt muss
einen tiefen Kurseinbruch enthalten, und nicht jeder tut das. Genommen wurden
stattdessen die Abschnitte, die die im Regelwerk genannten Krisenjahre abdecken.
Das funktioniert bei allen neun.

Drittens führt die Schutzaufnahme zwei der drei Dateigruppen gar nicht, die die
Wache künftig aus ihr lesen soll. Das Erzeugerprogramm ist umgebaut, aber eine
neue Aufnahme wurde bewusst **nicht** gemacht — dafür braucht es eine Freigabe.
