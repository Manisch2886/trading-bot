# Übergabe: Telegram-Nachricht bei jedem geschlossenen Trade

**Für die Review-Sitzung.** Branch `claude/new-session-uqjk8h`, Basis
`origin/main` (`3c1fbbf`).

---

## ⚠️ Zuerst: die Prämisse der Aufgabe traf nicht zu

Die Aufgabe beginnt mit „Der Nutzer bekommt derzeit **keine** Push-Nachricht,
wenn eine Position geschlossen wird." Das war nicht so. Ich habe es
**empirisch** geprüft, nicht nur im Code gelesen — ein Wegwerf-Projekt gebaut,
einen Trade schließen lassen, `monitor.check_for_events()` aufgerufen:

```
Lauf 1 (Baseline, Trade offen):   0 Ereignis(se)
Lauf 2 (Trade geschlossen):       1 Ereignis(se)
  🛑 *T3/ADX/SuperTrend (Krypto)*: STOP-LOSS ausgeloest
  Symbol: `BTCUSDT`  |  Ergebnis: stop_loss  |  PnL: -5.3%
```

`telegram_bot.poll_job` schickte das alle 300 Sekunden raus.

**Die Absicht der Aufgabe traf trotzdem genau.** Dieser Nachricht fehlt alles,
was die Aufgabe auflistet: Ein- und Ausstiegskurs, Haltedauer, und der Grund
stand als **roher Feldwert** da (`Ergebnis: stop_loss`). Wer sie liest, erfährt
nicht, was der Trade gebracht hat — nur, dass etwas passiert ist.

Deshalb habe ich nicht einfach gebaut, sondern gefragt: ein zweiter Sendeweg
hätte je Schließung **zwei** Nachrichten bedeutet, und das zu verhindern heißt
`monitor.py` anzufassen, was die Aufgabe ausschloss. Der Nutzer hat sich für
**Option A** entschieden: neues Skript, alte Meldung entfernen.

---

## Warum die alte Meldung weg ist

Drei Gründe. Der dritte war der Anlass.

**1. Der Inhalt.** Roher Feldwert, keine Kurse, keine Haltedauer.

**2. Kein Vermerk je Trade.** Erkannt wurde über einen Mengenvergleich gegen
`notifications/state.json` — eine Momentaufnahme „welche Trades waren offen".
Geht die Datei verloren, greift die Baseline-Logik: ein neuer Anfangszustand
wird still geschrieben, und **jede Schließung dieses Fensters ist weg**. Es
gibt nichts, woraus sich rekonstruieren ließe, was schon gemeldet war.

**3. Ein fehlgeschlagener Versand galt als erledigt.** In `poll_job`:

```python
for event_text in events:
    await asyncio.to_thread(notify.send_alert, event_text)
await asyncio.to_thread(monitor._save_state, new_state)
```

`send_alert` gibt `True`/`False` zurück — der Rückgabewert wird **nicht
geprüft**, der Zustand danach in jedem Fall gespeichert. Ist das Netz im
falschen Moment weg, ist die Nachricht verloren und der Trade gilt als
gemeldet. Bei einer Cronjob-Warnung ist das verzeihlich. Bei „dein Stop-Loss
hat ausgelöst" nicht.

**Der Eingriff:** 13 Zeilen entfernt, **kein einziger Test prüfte sie** (das
ganze Repo durchsucht). An ihrer Stelle steht jetzt ein Kommentar, der die drei
Gründe und den Umzugsort nennt — damit niemand sie in zwei Jahren als
„vergessen" wieder einbaut.

Unberührt: Eröffnungs-Meldungen, Cronjob-Fehler, Staleness-Warnung, alle
Befehle. Der Telegram-Bot bleibt rein lesend — es ist ein Sendeweg **weniger**,
nicht einer mehr. Vier Prüfungen halten das fest, und eine fünfte belegt es am
Verhalten: eine Schließung erzeugt kein Ereignis mehr, eine Eröffnung schon.

Eine Kleinigkeit am Rand: `known_open_ids` wurde durch den Wegfall zur toten
Leseoperation. Der Schlüssel wird weiter **geschrieben** (er beschreibt, was
beim letzten Check offen war, und ist damit die Angabe, an der sich ein
verlorener Zustand erkennen lässt), aber nicht mehr gelesen — das steht dort
als Kommentar.

---

## Das neue Skript

`notifications/schliess_benachrichtigung.py`, dasselbe Muster wie
`broker/spiegel.py`: liest die neun Bot-Datenbanken schreibgeschützt über
`broker/bot_db.py` (benutzt, nicht nachgebaut), vermerkt in einer **eigenen**
Datenbank `benachrichtigungen_schliessung.db`.

`forward_test.py` und `live_params.py` werden weder verändert noch importiert —
das ist **strukturell per AST geprüft**, nicht behauptet. Erwünschter
Nebeneffekt: fällt die Benachrichtigung aus, ist der Bot-Betrieb unberührt, und
umgekehrt hält ein hängender Bot-Lauf die Benachrichtigung nicht auf.

### Die Nachricht

```
🔴 *Trade geschlossen* – Turtle Soup (Aktien)
*AAPL*  ·  *-4.80 %*
Einstieg 200 → Ausstieg 190.4
Gehalten: 3 Tage 5 Std.
Grund: Stop-Loss ausgelöst
```

Gebündelt:

```
*2 Trades geschlossen*

🟢 T3/ADX/SuperTrend (Krypto) · *BTCUSDT* *+1.70 %* – Trendwechsel (SuperTrend hat gedreht)
🔴 Volatility Breakout (Aktien) · *MSFT* *-3.20 %* – Stop-Loss ausgelöst
```

---

## Entscheidungsgrundlage

### Doppelversand: Anspruch nehmen, senden, bestätigen

Zwei Forderungen der Aufgabe widersprechen sich auf den ersten Blick:

- „Ein abgebrochener Lauf darf beim nächsten Mal nicht dieselben Nachrichten
  erneut schicken."
- „Schlägt der Versand fehl, darf der Trade **nicht** als gemeldet vermerkt
  werden."

Mit **zwei** Schritten geht nur eines davon: „erst senden, dann vermerken"
dupliziert bei einem Abbruch; „erst vermerken, dann senden" verschluckt einen
Fehlschlag. Deshalb **drei**:

1. **Anspruch nehmen** — eine Zeile mit `zustand='wird_gesendet'` einfügen. Die
   Sperre ist `UNIQUE(bot, trade_id)`, also strukturell und nicht eine
   if-Abfrage: laufen zwei Läufe gleichzeitig, bekommt genau einer den
   Anspruch, der andere einen `IntegrityError` und geht weiter.
2. **Senden.**
3. Erfolg → `zustand='gesendet'`. Fehlschlag → die Zeile wird **wieder
   gelöscht**, der Trade ist unvermerkt und kommt beim nächsten Lauf erneut.

**Der eine Fall, der offen bleibt — bewusst:** bricht ein Lauf zwischen 2 und 3
ab, steht die Zeile als `wird_gesendet` da. Sie zählt dann als vermerkt, der
Trade wird **nicht** erneut gemeldet — so verlangt es die erste Forderung. Ob
die Nachricht rausging, ist in diesem einen Fall nicht bekannt; der Zustand
sagt genau das, statt es zu verschweigen, und `--status` zeigt ihn an. Das ist
die ehrlichste Auflösung, die ich sehe: eine der beiden Forderungen muss in
diesem Grenzfall weichen, und die Aufgabe sagt, welche.

Geprüft wird die **Reihenfolge**, nicht der Zustand danach: eine Sender-Attrappe
sieht während des Sendens in die Nachverfolgung. Das war nötig, weil die
Gegenprobe M2 („Anspruch erst nach dem Senden") zuerst **unentdeckt** durchging
— mein erster Test stellte den Zustand von Hand her, statt die Reihenfolge zu
beobachten.

### Der Erstlauf

Beim ersten Lauf wird der Bestand still vermerkt (`erstlauf_uebersprungen`) und
**eine** Bestätigung geschickt. Geprüft mit 300 Bestandstrades: eine Nachricht,
nicht 300.

Dass der Modus nicht versehentlich erneut greift, hängt an **zwei** Bedingungen,
die beide erfüllt sein müssen:

- keine Marke `erstlauf_am` in der Zustandstabelle, **und**
- die Tabelle `gemeldet` ist vollständig leer.

Marke und Bestandszeilen entstehen in **derselben Transaktion** — es gibt
keinen Zwischenzustand, in dem das eine da ist und das andere fehlt.

Und der Fall, vor dem die Aufgabe warnt („sonst verschluckt er echte
Schließungen"): fehlt die Marke, sind aber Vermerke da — das kann der Erstlauf
nicht erzeugt haben, also hat jemand die Tabelle angefasst. Dann wird der
Erstlauf **abgelehnt** und laut gemeldet, und der Lauf meldet normal weiter.
Geprüft, in beide Richtungen.

**Scheitert die Bestätigungsnachricht**, bleibt der Vermerk trotzdem stehen.
Hätte ich ihn zurückgerollt, würde der nächste Lauf hunderte Nachrichten
schicken — genau das, was der Erstlauf verhindern soll. Die Bestätigung ist
eine Höflichkeit, der Vermerk ist die Sache. Steht so im Code.

### Der Ausstiegsgrund

Die Werte stammen aus den `forward_test.py` der neun Bots — dort **gelesen**
(per AST, ohne Import), nicht geraten. Alle sieben sind übersetzt:

| Feldwert | Nachricht |
|---|---|
| `stop_loss` | Stop-Loss ausgelöst |
| `take_profit` | Kursziel erreicht (Take-Profit) |
| `time_exit` | maximale Haltedauer erreicht |
| `sma_exit` | Ausstiegssignal: Kurs zurück über dem gleitenden Durchschnitt |
| `trend_flip` | Trendwechsel (SuperTrend hat gedreht) |
| `t3_crossunder` | Ausstiegssignal: T3-Linien gekreuzt |
| `manual_close` | von Hand geschlossen (Dashboard) |

Ein **unbekannter** Wert wird nicht verschluckt und nicht geraten, sondern
wörtlich durchgereicht und gekennzeichnet: `xyz_exit (unbekannter
Ausstiegsweg)`. Kommt ein zehnter Bot mit einem neuen Ausstiegsweg, steht in
der Nachricht der echte Wert — nicht ein beruhigendes „Ausstieg".

### Keine Beträge

Prozent, keine Euro- oder Dollarzahlen. Die Bots tracken kein echtes Kapital;
jeder Betrag wäre aus einer Annahme abgeleitet und würde echter wirken, als er
ist. Eine Prüfung hält fest, dass keine Währung in der Nachricht steht.

### Markdown — eine Falle, die dieses Projekt schon kennt

`notify.send_alert` benutzt Telegrams **Legacy**-Markdown, und das kennt laut
Bot-API **kein Backslash-Escaping** (ausführlich im Docstring von
`notify.send_report` — dort hat genau das einmal wörtliche Backslashes beim
Nutzer erzeugt). Ein Sternchen in einem Symbolnamen würde die Formatierung der
ganzen Nachricht zerreißen, und escapen lässt es sich nicht.

Deshalb werden die drei wirksamen Zeichen (`*`, `_`, `` ` ``) aus eingesetzten
Werten **entfernt**. Die Prüfung dazu vergleicht nicht auf Abwesenheit, sondern
auf **gleiche Markdown-Paarung** wie bei einem harmlosen Symbol — das ist die
Eigenschaft, auf die es ankommt.

### Der Cron-Takt: alle 15 Minuten

Vom Nutzer bestätigt. Die Begründung, die im README steht:

**Ein eigener Takt statt neun Einträgen hinter neun Bot-Zeilen.** Neun
Einträge wären neun Stellen, an denen ein Bot vergessen wird — und bei drei
Rhythmen (stündlich, alle 4 h, täglich abends) neun Zeitpunkte, die mit jeder
Cron-Änderung neu stimmen müssen. Ein eigener Takt kennt die Bot-Rhythmen gar
nicht: er sieht nach, was seit dem letzten Mal geschlossen wurde.

**Warum 15 und nicht 5 oder 60.** Der schnellste Bot (`elliott_wave`) schließt
höchstens stündlich — ein engerer Takt bringt nichts. Ein Leerlauf kostet
nichts messbares: neun SQLite-Abfragen und ein Mengenvergleich, kein Netz. 96
Leerläufe am Tag fallen nicht ins Gewicht. Der bestehende Telegram-Dienst pollt
alle 5 Minuten, aber der läuft ohnehin dauerhaft; ein Cronjob mit demselben
Takt wären 288 Prozessstarts am Tag für keinen Gewinn. Stündlich wäre sparsam,
aber eine Schließung des 4-Stunden- oder Tages-Bots könnte bis zu einer Stunde
alt sein.

### Abbruch nach dem ersten Fehlschlag

Scheitert ein Versand, bricht der Lauf ab statt weiterzumachen. Begründung:
`send_alert` scheitert an Netz oder API, nicht am Inhalt einer einzelnen
Nachricht — der nächste Versuch scheitert also mit hoher Wahrscheinlichkeit
genauso, und 24 weitere Versuche mit je 10 Sekunden Zeitgrenze würden den Lauf
minutenlang blockieren. Verloren geht dabei nichts: die übrigen Trades bleiben
unvermerkt und kommen beim nächsten Lauf dran. Geprüft.

---

## Tests

`notifications/test_schliess_benachrichtigung.py` → **99 Prüfungen**, zehn
Abschnitte.

**Kein echter Netzaufruf.** Der Sendeweg ist ein Parameter; die Attrappe zählt,
hält den Text fest und lässt sich gezielt kaputtmachen (`scheitert_ab`,
`scheitert_immer`) — nur so sind die Fälle prüfbar, auf die es hier ankommt.

Die Test-Datenbank entsteht aus dem **echten** `CREATE TABLE` eines Bots. Das
hat sich sofort bezahlt: mein erster Fixture-Entwurf lief in
`UNIQUE(symbol, signal_time)` — eine Bedingung des echten Schemas, die ein
selbst erfundenes Schema nicht gehabt hätte.

Abgedeckt:

| Abschnitt | Was |
|---|---|
| 1 | Erkennen, melden, vermerken; alle sechs Inhaltsangaben; keine Währung |
| 2 | Doppelversand — zweiter Lauf sendet nichts; UNIQUE lehnt direkten Zweit-INSERT ab; **die Reihenfolge während des Sendens**; abgebrochener Lauf sendet nicht erneut |
| 3 | Fehlgeschlagener Versand → kein Vermerk, nächster Lauf holt nach; Fehlschlag beim zweiten von drei |
| 4 | Erstlauf mit 300 Bestandstrades; danach wird gemeldet; greift kein zweites Mal; der Widerspruchsfall |
| 5 | Beide Modi mit erzeugter Nachricht; gebündelt mit Fehlschlag; unbekannter Modus wird abgelehnt |
| 6 | Obergrenze: 30 → 25 einzeln + eine Sammelnachricht, kein Trade verloren; Sammelnachricht scheitert |
| 7 | Bot-DB **byteweise unverändert**; `mode=ro` verweigert aktiv; kein neues Feld im Bot-Schema; AST-Nachweis kein verbotener Import |
| 8 | Alle sieben Gründe; unbekannter Wert; Haltedauer in sechs Formen; Markdown-Paarung |
| 9 | Randfälle: nichts zu melden, fehlende Bot-DB, Bot-Liste aus der einen Quelle |
| 10 | Die alte Meldung ist weg — statisch **und** am Verhalten |

**16 Mutationsproben, 16 erkannt.** Zwei mussten nachgeschärft werden:

- **M2** (Anspruch erst nach dem Senden) ging zuerst durch, weil mein Test den
  Zustand von Hand herstellte. Jetzt beobachtet eine Attrappe die
  Nachverfolgung *während* des Sendens.
- **M1** wurde zunächst nur über einen SQL-Syntaxfehler erkannt — das ist kein
  Nachweis. Die Mutation ist jetzt semantisch gültig
  (`UNIQUE(bot, trade_id, zeitpunkt)`, also wirkungslos) und wird von der
  Zusicherung selbst erkannt.

**Keine Regression:** `dashboard/test_dashboard.py` 784, `broker/test_broker.py`
163, `broker/test_ibkr.py` 200, `notifications/test_manual_close.py`,
`shared/test_empfehlung_format.py` 70, `system/test_caffeinate_plist.py` 52.

---

## Was der Nutzer noch tun muss

1. **Den Erstlauf von Hand auslösen** — das ist der einzige Schritt, der sich
   nicht wiederholen lässt, und deshalb bewusst kein Nebeneffekt des Cronjobs.
   Schritte im README und im Testauftrag (Schritt 5).
2. **Den Cronjob eintragen**, falls gewünscht. Zeile steht im README, nicht
   eingetragen.
3. **Entscheiden, ob `einzeln` bleibt.** Umstellen auf `gebuendelt` ist eine
   Zeile oder ein `--modus`-Argument, kein neuer PR.

## Offene Punkte

- **Der Grenzfall `wird_gesendet`** (Abbruch zwischen Senden und Bestätigen)
  ist bewusst nicht auflösbar gemacht. Auflösen ließe er sich nur, indem man
  Telegram nach der Nachricht fragt — das wäre ein Lesezugriff auf den
  Nachrichtenverlauf und deutlich mehr Apparat als der Fall wert ist. Wenn er
  in der Praxis auftritt, zeigt `--status` ihn; dann kann man entscheiden.
- **Die 5-Minuten-Lücke der Eröffnungs-Meldung** bleibt wie sie ist: öffnet und
  schließt ein Bot einen Trade zwischen zwei `poll_job`-Läufen, wird die
  *Eröffnung* nie gemeldet (die Schließung jetzt schon, weil das neue Skript
  nicht auf „war mal offen" angewiesen ist). Das ist ein bestehender Zustand,
  nicht Teil dieser Aufgabe — aber es ist mir aufgefallen und gehört notiert.
