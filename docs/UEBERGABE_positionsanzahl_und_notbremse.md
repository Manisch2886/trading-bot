# Übergabe: Positionsanzahl je Bot im PnL-Dialog + Notbremse zu Beginn

**Für die Review-Sitzung.** Zwei unabhängige Änderungen in einem PR; sie
berühren verschiedene Dateien und lassen sich getrennt prüfen.

Branch `claude/new-session-uqjk8h`, Basis `origin/main` (`c2b6995`).

---

## Was geändert wurde, in einem Absatz

**Teil 1** weist im gewichteten Gesamt-PnL zusätzlich aus, wie viele
Positionen je Bot in die Zahl eingehen — als sichtbare Zeile, in allen vier
bot-übergreifenden Ansichten. Reine Anzeige, keine Backend-Änderung.
**Teil 2** prüft die Notbremse in beiden Broker-Brücken zusätzlich **zu
Beginn** jedes echten Laufs, mit sichtbarer Meldung und Abbruch — auch wenn
null Aufgaben offen sind. Die bestehende Prüfung je Aufgabe bleibt
unverändert.

| Datei | Teil | Art |
|---|---|---|
| `dashboard/static/app.js` | 1 | neue Funktion `positionsanzahlZeilen()`, Einhängung in `gewichtungsZeilen()` |
| `dashboard/static/bot.html` | 1 | eine Zeile: `notfallErgebnisAnzeigen()` holt sie eigens |
| `broker/spiegel.py` | 2 | Prüfung zu Beginn von `lauf()`, `notbremse_grund()`, `_meldung()` |
| `broker/ibkr_spiegel.py` | 2 | dasselbe für IBKR |
| `broker/README.md`, `broker/README_IBKR.md` | 2 | Sicherungs-Tabelle und Anleitung nachgezogen |
| die vier Testdateien | 1+2 | **nur Hinzufügungen**, keine entfernte Zeile |

---

# Teil 1 — Positionsanzahl je Bot

## Das Problem

Der gewichtete Gesamt-PnL aus PR #67 rechnet korrekt. Er sagt aber nicht,
**woraus** die Zahl besteht. `elliott_wave` hat als einziger Bot kein
`MAX_CONCURRENT_POSITIONS` und kann deshalb deutlich mehr Positionen
gleichzeitig stellen als die anderen. Steht dann „Ø gewichtet −8,05 %" da,
kann das der Durchschnitt über sieben Elliott-Positionen und eine einzige
fremde sein — rechnerisch richtig, faktisch die Aussage **eines** Bots. Und
zwar genau in dem Moment, in dem eine Notfallentscheidung fällt.

## Die Lösung

Neue Zeile, direkt unter der gewichteten Zahl:

```
Ø gewichtet -8.05%  (Positionsgröße 5 % / 2 %; dieselben Positionen ungewichtet -7.40%)
Gewichtet nach der je Bot im Backtest angenommenen Positionsgröße – keine echte
Kapitalbindung und keine Portfolio-Rendite.
Eingegangene Positionen je Bot – Elliott Wave (Krypto): 7; Turtle Soup (Aktien): 1.
Bots ohne Obergrenze für gleichzeitige Positionen können die gewichtete Zahl allein tragen.
```

## Entscheidungsgrundlage

**Nichts wird neu berechnet.** `gewichteter_pnl()` zählt die Positionen je Bot
für die Gewichtung ohnehin schon und legt sie in `gewichte[].anzahl` ab. Es
ging ums Ausweisen, nicht ums Rechnen — `dashboard/schliessen.py` ist
deshalb **byteweise unverändert** (`git diff origin/main HEAD --
dashboard/schliessen.py` ist leer). Das ist auch die konservativste Variante:
eine zweite Zählung wäre die Stelle gewesen, an der die Zahlen später
auseinanderlaufen.

**Sichtbare Zeile, kein `title`-Tooltip.** Dieselbe Begründung, die schon über
`GEWICHTUNG_ERLAEUTERUNG` steht: das Dashboard wird überwiegend am iPhone
benutzt, und dort gibt es kein Hover. Ein Tooltip wäre eine Angabe, die der
eigentliche Nutzer nie sieht. Die neue Zeile trägt dieselbe CSS-Klasse
`hinweis-gewichtung` und damit dieselbe, im Browser gemessene Block-Regel.

**Eine Quelle, in `app.js`.** `POSITIONSANZAHL_ERLAEUTERUNG` und
`positionsanzahlZeilen()` stehen dort, weil `bot.html` und `index.html` sie
beide brauchen — analog zu `gewichtungsZeilen()`. Zwei Fassungen desselben
Textes wären die Doppelführung, bei der irgendwann nur noch eine Seite sagt,
worauf die Zahl beruht.

**Vier Ansichten, fünf Einhängepunkte.** Drei der vier Ansichten erreichen die
Zeile über `gewichtungsZeilen()`. Die vierte nicht:
`notfallErgebnisAnzeigen()` in `bot.html` baut sein HTML selbst auf und ruft
`gewichtungsZeilen()` gar nicht. Genau diese Asymmetrie ist die Fehlerklasse
aus PR #62, #66 und #67 — dort war eine Suche über das ganze Dokument jedes
Mal grün, obwohl eine der beiden Ansichten die Angabe nicht zeigte. Sie wird
hier **je Funktion** geprüft, in `test_dashboard.py` statisch und in
`test_gewichtung.js` an der wirklich erzeugten Ausgabe.

**Blockiert den Notfallweg nicht.** Dieselbe Regel wie bei der Positionsgröße
in PR #67. Fehlt das Feld (älteres Backend), ist die Liste leer oder kaputt,
bleibt die Zeile weg; fehlt die Anzahl *eines* Bots, steht dort ein Strich;
fehlt der Name, steht „unbekannt". Geschlossen wird in jedem Fall.
Gegengeprüft mit Mutation M5 (eine Fassung, die bei fehlender Anzahl wirft) —
sie macht die Suite rot.

## Ausdrücklich nicht geändert

* die Gewichtungsformel
* die Felder `pnl_gewichtet`, `pnl_schnitt_pct`, `pnl_bestes_pct`,
  `pnl_schlechtestes_pct`
* die Entscheidung, `elliott_wave` **nicht** auszuschließen; der
  Ausschluss-Mechanismus (`nicht_gewichtbar`) bleibt, wie er ist — Bots ohne
  dokumentierte Positionsgröße werden weiterhin benannt, mit Grund, Anzahl und
  eigenem ungewichtetem Durchschnitt

---

# Teil 2 — Notbremse zusätzlich zu Beginn

## Das Problem

Die Notbremse (`broker/STOP`, `broker/STOP_IBKR`) wurde **je Aufgabe**
geprüft, also unmittelbar vor jeder einzelnen Order. Lag keine Aufgabe an, kam
die Prüfung nie dran: keine Zeile, Rückgabewert 0 — ein gebremster Lauf war
von einem gewöhnlichen Leerlauf nicht zu unterscheiden. Das hat bereits zu der
falschen Meldung geführt, die Bremse greife nicht: ein Fehlalarm ausgerechnet
an der Sicherung, der man am meisten glauben muss.

## Die Lösung

`lauf(echt=True)` prüft die Bremse nun **zusätzlich zu Beginn**, meldet sie
sichtbar und beendet den Lauf:

```
NOTBREMSE aktiv (/…/broker/STOP) - dieser Lauf wird sofort beendet, ohne das
Testnet auch nur zu kontaktieren. Offene Aufgaben: 0. Datei entfernen gibt den
Weg wieder frei.
```

Es gibt damit **drei** Ebenen:

| Ebene | Wo | Greift wann |
|---|---|---|
| 1 (**neu**) | `lauf(echt=True)`, zu Beginn | die Bremse lag schon vor dem Lauf |
| 2 (unverändert) | `spiegle_eine()`, je Aufgabe | die Datei wird **mitten im Lauf** angelegt |
| 3 (unverändert) | `binance_testnet.marktorder()` / `ibkr_paper.marktorder()` | letzte Rückfallebene |

**Ebene 2 ist ausdrücklich geblieben.** Sie ist die eigentliche Sicherung —
und genau dann wird die Datei angelegt: mitten im Lauf, von einem Menschen,
der etwas gesehen hat. Ebene 1 kommt hinzu, sie ersetzt nichts. Ergebnis:
doppelte Absicherung plus sichtbare Meldung.

## Entscheidungsgrundlage

### Der Rückgabewert bei gezogener Bremse ohne offene Aufgaben: **0**

Das ist die zu begründende Festlegung.

Eine gezogene Notbremse ist für sich genommen **kein Fehlschlag**. Sie ist
eine Anweisung des Nutzers, und sie wurde befolgt. Lag keine Aufgabe an, ist
auch nichts liegengeblieben: es gibt nichts, worüber Alarm zu schlagen wäre.

Der Alarmweg von Cron ist die Fehlermail. Die Bremse bleibt im Zweifel **Tage**
gezogen — beim 4-Stunden-Takt der Binance-Brücke wären das sechs Mails am Tag,
bei den Aktien-Bots eine je Werktag, alle mit demselben Inhalt und alle
erwartet. Genau so entwertet man die Mails, auf die es ankommt: wer täglich
sechs Fehlermails wegklickt, die keine sind, liest die siebte nicht mehr.

Dass die Bremse wirkt, gehört ins **Protokoll**, nicht in den Rückgabewert.
Dort steht sie jetzt zweimal: als `logger.warning` in `lauf()` und an erster
Stelle in der Zusammenfassung von `_meldung()`.

**Mit** offener Aufgabe bleibt es beim bisherigen **1**. Da ist tatsächlich
etwas nicht ausgeführt worden, was ausgeführt werden sollte, und das
unterscheidet sich für den Cronjob nicht von einem anderen Fehlschlag.

Beide Werte sind geprüft, nicht behauptet — und beide Mutationen, die daraus
ein pauschales 1 machen (M8, M13), machen die Suiten rot.

### Weitere Festlegungen

**Der Abbruch kommt vor jedem Netzzugriff.** Bei gezogener Bremse wird das
Testnet nicht gepingt, nicht zeitabgeglichen, und zu TWS wird gar nicht erst
verbunden. Das ist keine Nebenwirkung, sondern der Punkt: eine gezogene Bremse
soll die Brücke vollständig ruhigstellen. Geprüft über `boerse.anfragen == []`
bzw. `z["konto"] is None`.

**Offene Aufgaben verschwinden nicht.** Liegen beim Abbruch Aufgaben an,
bekommt jede denselben Eintrag in der Nachverfolgung und denselben Grund, den
auch Ebene 2 geschrieben hätte (`notbremse_grund()`, der Wortlaut steht für
beide Ebenen an *einer* Stelle). Sonst stünde in der Nachverfolgung eine Lücke
genau dort, wo später jemand nachliest, warum nichts passiert ist. Gegenprobe
M9.

**IBKR, ein Sonderfall:** Aufgaben außerhalb der Handelszeiten stehen beim
Abbruch als `fehlgeschlagen` statt als `wartet`. Die Handelszeit wäre der
Grund, warum eine Order *später* käme — bei gezogener Bremse kommt sie
überhaupt nicht, und der gewichtigere der beiden Gründe gehört in die Anzeige.
`z["konto"]` ist in diesem Fall `None`, kein erfundener Platzhalter: es wurde
nicht verbunden, und genau das sagt der Wert.

**Kein neues Schema, keine neue Datei.** Die Zusammenfassung bekommt ein Feld
`notbremse` (bool); die Tabellen `spiegelungen` und `versuche` bleiben
unverändert.

---

## Tests

Keine bestehende Prüfung wurde geändert oder entfernt:
`git diff origin/main HEAD -- <die vier Testdateien> | grep -c '^-[^-]'` → **0**.

| Suite | vorher | nachher |
|---|---|---|
| `broker/test_broker.py` | 149 | **163** |
| `broker/test_ibkr.py` (mit `ib_async`) | 186 | **200** |
| `broker/test_ibkr.py` (ohne) | 154 | **168** |
| `dashboard/test_dashboard.py` | 738 | **753** |
| `dashboard/test_gewichtung.js` | 27 | **35** |

Unberührt und weiterhin grün: `notifications/test_manual_close.py` (118),
`shared/test_empfehlung_format.py` (70), `system/test_caffeinate_plist.py`
(52), `dashboard/test_zustandsmaschine.js` (27), `dashboard/test_zeitzone.js`
(24).

**13 Mutationsproben, 13 erkannt.** Das vollständige, ausführbare Skript steht
in `docs/TESTAUFTRAG_positionsanzahl_und_notbremse.md`, Schritt 5.

Zwei davon sind nachträglich entstanden und verdienen eine Erwähnung, weil sie
zuerst **unentdeckt** durchgingen: M7 und M12 (Ebene 2 entfernt). Ebene 3
verdeckte sie — nimmt man die Prüfung je Aufgabe heraus, bleibt trotzdem jede
Order aus, weil die unterste Ebene sie abfängt. Der Test unterscheidet die
Ebenen deshalb jetzt daran, **wie oft der Client überhaupt gefragt wurde** und
ob der Grund der Wortlaut von Ebene 2 ist. Ohne diese Schärfung hätte der Test
eine Zusicherung behauptet, die er nicht prüft — und das an der Sicherung.

## Nicht angefasst

Keine `live_params.py`, keine `forward_test.py`, keine
`equity_simulation.py`; kein Schema der `trades`-Tabelle; keine launchd-Vorlage
und keine Crontab. Nachweis: `git diff origin/main HEAD --name-only` listet
genau die zehn Dateien der Tabelle oben plus die drei Dokumente unter `docs/`.

## Offene Punkte

* Der Dialog ist in dieser Sitzung **nicht im Browser** gesehen worden — die
  Anzeige ist über die erzeugte Ausgabe geprüft (Node, ohne Browser), nicht am
  iPhone. Ein Blick auf die fertige Seite bei der nächsten Gelegenheit wäre
  trotzdem gut, insbesondere auf den Zeilenumbruch der neuen Zeile bei vielen
  Bots.
* Die neue Zeile wird bei neun gleichzeitig getroffenen Bots entsprechend
  lang. Sie bleibt lesbar (Block-Regel, kein Flex), aber ob eine Kürzung ab
  einer bestimmten Anzahl sinnvoll wäre, ist eine Gestaltungsfrage für später
  — und keine, die ohne echte Crash-Daten zu beantworten ist.
* `docs/UEBERGABEPROTOKOLL.md` ist **nicht** angefasst worden: es beschreibt
  ausdrücklich den Stand von `main`. Nach dem Merge gehören dorthin zwei
  Sätze — die dreistufige Notbremse in Abschnitt 8 und die Anzeige im
  Crash-Dialog.
