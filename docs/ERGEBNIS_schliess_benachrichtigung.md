# Ergebnis — Telegram-Nachricht bei geschlossenem Trade

**PR #78** · Branch `claude/new-session-uqjk8h`, Basis `origin/main`
(`3c1fbbf`, nach Merge von #77).

---

## ⚠️ Befund zuerst: Schließungen wurden schon gemeldet

Die Prämisse der Aufgabe traf nicht zu. `monitor.check_for_events()` erzeugte
je geschlossenem Trade ein Ereignis, `telegram_bot.poll_job` schickte es alle
5 Minuten raus — **empirisch geprüft**, nicht nur im Code gelesen:

```
🛑 *T3/ADX/SuperTrend (Krypto)*: STOP-LOSS ausgeloest
Symbol: `BTCUSDT`  |  Ergebnis: stop_loss  |  PnL: -5.3%
```

Die **Absicht** der Aufgabe traf trotzdem: dieser Nachricht fehlt alles, was
gefordert war — Ein-/Ausstiegskurs, Haltedauer, und der Grund stand als roher
Feldwert da.

Nach Rücksprache: **neues Skript bauen UND die alte Meldung entfernen.** Sonst
zwei Pushes je Schließung.

## Warum die alte Meldung weg ist

1. **Inhalt** — roher Feldwert, keine Kurse, keine Haltedauer.
2. **Kein Vermerk je Trade** — Mengenvergleich gegen `state.json`. Geht die
   Datei verloren, schreibt die Baseline-Logik still einen neuen Anfangszustand
   und jede Schließung des Fensters ist weg.
3. **Ein fehlgeschlagener Versand galt als erledigt** — `poll_job` prüft den
   Rückgabewert von `send_alert` nicht und speichert den Zustand danach in
   jedem Fall. ← **der Anlass.** Bei einer Cronjob-Warnung verzeihlich, bei
   „dein Stop-Loss hat ausgelöst" nicht.

**13 Zeilen entfernt, kein Test prüfte sie.** Eröffnungen, Cronjob-Fehler,
Staleness und alle Befehle unberührt — es ist ein Sendeweg **weniger**, keiner
mehr.

---

## Die neue Nachricht

```
🔴 *Trade geschlossen* – Turtle Soup (Aktien)
*AAPL*  ·  *-4.80 %*
Einstieg 200 → Ausstieg 190.4
Gehalten: 3 Tage 5 Std.
Grund: Stop-Loss ausgelöst
```

Gebündelt (umschaltbar, geprüft):

```
*2 Trades geschlossen*

🟢 T3/ADX/SuperTrend (Krypto) · *BTCUSDT* *+1.70 %* – Trendwechsel (SuperTrend hat gedreht)
🔴 Volatility Breakout (Aktien) · *MSFT* *-3.20 %* – Stop-Loss ausgelöst
```

Prozent, **keine** Euro- oder Dollarbeträge.

---

## Die drei Entscheidungen, die Erklärung brauchen

**Doppelversand: Anspruch nehmen → senden → bestätigen.** Die beiden
Forderungen („ein abgebrochener Lauf darf nicht erneut senden" und „ein
fehlgeschlagener Versand darf nicht als gemeldet gelten") gehen mit *zwei*
Schritten nicht beide. Also drei: erst eine Zeile `wird_gesendet` einfügen
(Sperre `UNIQUE(bot, trade_id)`, strukturell — auch gegen zwei gleichzeitige
Läufe), dann senden, dann bestätigen bzw. die Zeile **wieder löschen**.

*Der eine offene Grenzfall, bewusst:* bricht ein Lauf zwischen Senden und
Bestätigen ab, bleibt `wird_gesendet` stehen und der Trade wird **nicht**
erneut gemeldet — so verlangt es die erste Forderung. Ob die Nachricht rausging,
ist dann unbekannt; `--status` zeigt genau das an, statt es zu verschweigen.

**Erstlauf: zwei Bedingungen, eine Transaktion.** Der Modus greift nur, wenn
keine Marke `erstlauf_am` da ist **und** die Tabelle leer ist. Beides entsteht
in derselben Transaktion. Fehlt die Marke bei vorhandenen Vermerken, wird der
Erstlauf **abgelehnt** und laut gemeldet — sonst würde er echte Schließungen
verschlucken.

**Cron: alle 15 Minuten.** Ein eigener Takt statt neun Einträgen hinter neun
Bot-Zeilen — neun Einträge wären neun Stellen, an denen ein Bot vergessen wird,
und bei drei Rhythmen neun Zeitpunkte, die mit jeder Cron-Änderung neu stimmen
müssen. 15 und nicht 5: der schnellste Bot schließt höchstens stündlich, ein
Leerlauf kostet nichts messbares (neun SQLite-Abfragen, kein Netz). 15 und
nicht 60: sonst wäre eine Schließung des Tages-Bots bis zu einer Stunde alt.

---

## Tests

| Suite | Ergebnis |
|---|---|
| `notifications/test_schliess_benachrichtigung.py` *(neu)* | **99 / 99** ✅ |
| `dashboard/test_dashboard.py` | 784 / 784 ✅ |
| `broker/test_broker.py` | 163 ✅ |
| `broker/test_ibkr.py` | 200 ✅ |
| `notifications/test_manual_close.py` | alle ✅ |
| `shared/test_empfehlung_format.py` | 70 / 70 ✅ |
| `system/test_caffeinate_plist.py` | 52 ✅ |

**Kein echter Netzaufruf** — der Sendeweg ist ein Parameter. Test-DB aus dem
**echten** `CREATE TABLE` eines Bots; das hat sich sofort bezahlt (mein erster
Fixture-Entwurf lief in `UNIQUE(symbol, signal_time)`).

Geprüft: Bot-DB **byteweise unverändert** nach Erstlauf, Lauf und Fehlschlag ·
`mode=ro` verweigert den Schreibversuch **aktiv** · AST-Nachweis, dass kein
`forward_test`/`live_params`/`equity_simulation` importiert wird · Erstlauf mit
300 Bestandstrades → **eine** Nachricht · beide Modi · Obergrenze 30 → 25
einzeln + eine Sammelnachricht, kein Trade verloren.

**16 Mutationsproben, 16 erkannt.** Zwei mussten nachgeschärft werden:

- **M2** (Anspruch erst nach dem Senden) ging zuerst durch — mein Test stellte
  den Zustand von Hand her. Jetzt beobachtet eine Attrappe die Nachverfolgung
  *während* des Sendens.
- **M1** wurde zunächst nur über einen SQL-Syntaxfehler erkannt, was kein
  Nachweis ist. Die Mutation ist jetzt semantisch gültig und wird von der
  Zusicherung selbst erkannt.

---

## ⚠️ Was du noch tun musst

**1. Den Erstlauf von Hand auslösen.** Der einzige Schritt, der sich nicht
wiederholen lässt — deshalb bewusst kein Nebeneffekt des Cronjobs:

```bash
cd ~/trading-bot && mkdir -p logs/notifications
python3 notifications/schliess_benachrichtigung.py --status       # zeigt: Erstlauf noch offen
python3 notifications/schliess_benachrichtigung.py --trockenlauf  # zeigt die Zahl N
python3 notifications/schliess_benachrichtigung.py                # DER Erstlauf
```

Erwartet: **genau eine** Telegram-Nachricht „Schliess-Benachrichtigung aktiv,
N bestehende Trades wurden als erledigt vermerkt". Kommen mehr, ist das ein
Befund.

**2. Den Cronjob eintragen**, falls gewünscht (Zeile im README, nicht
eingetragen):

```cron
*/15 * * * * cd ~/trading-bot && /usr/bin/python3 notifications/schliess_benachrichtigung.py >> logs/notifications/schliess_benachrichtigung.log 2>&1
```

**3. Entscheiden, ob `einzeln` bleibt.** Umstellen auf `gebuendelt` ist eine
Zeile oder ein `--modus`-Argument — kein neuer PR.

Der vollständige Ablauf steht in
`docs/TESTAUFTRAG_schliess_benachrichtigung.md`; dort ist der Erstlauf **Schritt
5** und ausdrücklich als freigabepflichtig gekennzeichnet.

---

## Offene Punkte

- **Der Grenzfall `wird_gesendet`** ist bewusst nicht auflösbar gemacht.
  Auflösen ließe er sich nur, indem man Telegram nach der Nachricht fragt — ein
  Lesezugriff auf den Nachrichtenverlauf, deutlich mehr Apparat als der Fall
  wert ist. Tritt er auf, zeigt `--status` ihn.
- **Die 5-Minuten-Lücke der Eröffnungs-Meldung** bleibt: öffnet und schließt
  ein Bot einen Trade zwischen zwei `poll_job`-Läufen, wird die *Eröffnung* nie
  gemeldet. Die Schließung jetzt schon, weil das neue Skript nicht auf „war mal
  offen" angewiesen ist. Bestehender Zustand, nicht Teil dieser Aufgabe — aber
  aufgefallen und notiert.

## Geänderte Dateien

```
notifications/schliess_benachrichtigung.py       (neu)
notifications/test_schliess_benachrichtigung.py  (neu, 99 Prüfungen)
notifications/monitor.py                         (13 Zeilen entfernt + Begründung)
notifications/README.md                          (Cron-Vorschlag, Erstlauf, Modi)
```

Nicht angefasst: keine `forward_test.py`, keine `live_params.py`, keine
`equity_simulation.py` (auch nicht importiert — per AST geprüft), kein
`trades`-Schema, nichts unter `broker/` (`bot_db.py` wird **benutzt**), keine
Crontab, keine launchd-Vorlage.
