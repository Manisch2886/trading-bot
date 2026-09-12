# Übergabe: Handelszeiten im Dashboard sichtbar machen

**Für die Review-Sitzung.** Branch `claude/new-session-uqjk8h`, Basis
`origin/main` (`445fbf2`), Pull Request **#77**.

---

## Das Problem

Seit PR #71 wird außerhalb der Handelszeiten **vorgemerkt statt geschlossen**.
Das funktioniert — aber der Nutzer erfuhr es erst **im Bestätigungsdialog**.
Bis dahin sah alles aus wie immer: derselbe Knopf, dieselbe Beschriftung.

Für jemanden in Donaueschingen ist das kein Randfall. Die NYSE öffnet erst um
15:30 Ortszeit; den halben Tag über ist jeder Schließen-Knopf auf den vier
Aktien-Bots in Wahrheit ein Vormerken-Knopf. Und ob gerade Feiertag oder
Halbtag ist, weiß man selten auswendig.

## Was geändert wurde

| Datei | Was |
|---|---|
| `dashboard/app.py` | `/api/portfolio` liefert die Börsenlage mit (`_boersenlage_aktien()`) |
| `dashboard/static/app.js` | die gesamte Darstellungslogik: `boersenLage`, `boersenstatusZeile`, `wirdVorgemerkt`, `crashKnopfText`, `werktageDazwischen`, `boersenZeit` |
| `dashboard/static/index.html` | Platz für die Zeile, `zeichneBoersenstatus()`, Crash-Knopf nach Lage |
| `dashboard/static/bot.html` | Platz für die Zeile, `zeichneBoersenstatus()`, bot-weiter Notfallknopf nach Lage, `boerseGeschlossen()` auf die gemeinsame Quelle umgestellt |
| `dashboard/static/style.css` | `.boersenstatus` und `.boersenstatus-marke` |
| `dashboard/test_dashboard.py` | Abschnitt 16b (Endpunkt + Einhängepunkte je Funktion), Abschnitt 17 (Node-Start) |
| `dashboard/test_boersenstatus.js` | **neu**: Verhaltenstest der erzeugten Ausgabe |

---

# Teil A — Der Börsenstatus

## Wie er aussieht

```
NYSE geöffnet – schließt Donnerstag, 22:00 Uhr
NYSE geschlossen – öffnet Freitag, 15:30 Uhr
NYSE geschlossen (Wochenende) – öffnet Montag, 15:30 Uhr
NYSE geschlossen (Feiertag) – öffnet Freitag, 15:30 Uhr  [verkürzter Handelstag]
NYSE geöffnet – schließt Freitag, 19:00 Uhr              [verkürzter Handelstag]
Börsenstatus unbekannt – der Kalender gibt gerade keine Auskunft. …
```

Alle Zeiten in der **Zeitzone des Geräts**. Der Wochentag steht bewusst dabei:
„öffnet Montag" sagt mehr als „öffnet 14.09.", und die Uhrzeit entscheidet, ob
sich das Warten lohnt.

## Entscheidungsgrundlage

**Der Kalender wird benutzt, nicht nachgebaut.** `/api/portfolio` liefert
`schliessen.boersenlage("aktien")` mit — dieselbe Funktion, an der auch das
Schließen selbst hängt (PR #71). Eine zweite Quelle für Handelszeiten wäre
genau die Stelle, an der die Angaben später auseinanderlaufen; eine Prüfung
schlägt deshalb fehl, sobald `app.py` am Kalender vorbeigreift.

Der Modul-Kopf von `boersenkalender.py` hat diesen Aufbau übrigens schon
vorgezeichnet: dort steht ausdrücklich, dass die Oberfläche ihre Formulierung
aus den **Einzelwerten** baut, damit die Zeitpunkte in der Zeitzone des Geräts
stehen. Genau das passiert hier.

**Kein zusätzlicher Request.** Die Lage reitet auf der Übersichts-Antwort mit,
die ohnehin alle 60 Sekunden geholt wird. Auf der Bot-Seite war sie in
`schliessbare-positionen` sogar schon enthalten — dort musste nur noch etwas
damit gemacht werden.

**Halbtag** kommt direkt aus dem Kalender (`verkuerzter_handelstag`). Wichtig
ist, worauf sich das Feld bezieht: bei **offener** Börse auf den laufenden Tag
(„schließt heute früher"), bei **geschlossener** auf den nächsten Handelstag
(„öffnet, schließt dann aber früher"). Beides ist im Text berücksichtigt — wer
auf die Öffnung wartet, plant sonst mit dem falschen Zeitfenster.

**Feiertag wird abgeleitet — und zwar ohne zweite Kalenderquelle.** Der
Status-Datensatz sagt nicht „heute ist Feiertag". Er sagt, wann zuletzt
geschlossen und wann als Nächstes geöffnet wird. Daraus folgt:

> Liegt zwischen Handelsschluss und nächster Öffnung ein **Werktag** ohne
> Sitzung, war das ein Feiertag.

| Fall | dazwischen | Ergebnis |
|---|---|---|
| Do 20:00 zu → Fr 13:30 auf | nichts | über Nacht |
| Fr 20:00 zu → Mo 13:30 auf | Sa, So | Wochenende |
| Mi 21:00 zu → Fr 14:30 auf | **Do** | Feiertag (Thanksgiving) |
| Do 20:00 zu → Mo 13:30 auf | **Fr**, Sa, So | Feiertag (Karfreitag) |

**Gerechnet wird in UTC-Daten.** Das ist hier nicht Bequemlichkeit, sondern
sicherer als Gerätezeit: eine NYSE-Sitzung läuft 13:30–21:00 UTC und
überschreitet nie eine UTC-Datumsgrenze, das UTC-Datum ist also immer der
Handelstag. Auf Berliner Zeit umgerechnet läge ein Handelsschluss je nach
Jahreszeit schon nach Mitternacht — und der Wochentag wäre um einen daneben.
Genau die Zeitzonen-Falle, die in PR #53 schon einmal zugeschlagen hat.

Die Alternative wäre gewesen, `boersenkalender.py` um ein Feld „heute ist ein
Handelstag" zu erweitern. Das war ausgeschlossen: die Aufgabe verlangt, die
Logik aus PR #71 **nur zu lesen**, und ein neues Feld in einem Modul, an dem
die Schreibentscheidung hängt, ist keine Anzeigeänderung mehr.

**Sichtbarer Text, kein `title`-Tooltip** — dieselbe Begründung wie bei
`GEWICHTUNG_ERLAEUTERUNG` und `POSITIONSANZAHL_ERLAEUTERUNG`: am iPhone gibt
es kein Hover, ein Tooltip wäre eine Angabe, die der eigentliche Nutzer nie
sieht.

---

# Teil B — Die Knopfbeschriftungen

Bei geschlossener Börse sagen jetzt **alle drei** Wege, was der Klick wirklich
auslöst:

| Weg | vorher | nachher (Börse zu) |
|---|---|---|
| Einzelposition | `Vormerken` ✅ (war schon da) | `Vormerken`, dazu `aria-label="Zur Börsenöffnung vormerken"` |
| bot-weit (Notfall) | `⚠ Notfall: alle 2 Positionen schließen` | `⚠ Notfall: alle 2 Positionen zur Börsenöffnung vormerken` |
| global (Crash) | `⚠ ALLE 12 Positionen in 5 Bots schließen` | `⚠ 7 Krypto sofort schließen · 5 Aktien vormerken` |

Der bot-weite Notfallknopf war die eigentliche Lücke: er behauptete „schließen"
und legte Warteaufträge an.

## Die zu begründende Wahl: der Crash-Knopf

Er ist der einzige, der **beide Welten** auf einmal trifft. Krypto handelt
durchgehend, Aktien nicht — bei geschlossener Börse wird ein Teil sofort
geschlossen und ein Teil nur vorgemerkt.

**Gewählt: die Zahlen getrennt nennen, nicht zusammenfassen.**

```
offen         ⚠ ALLE 12 Positionen in 5 Bots schließen
geschlossen   ⚠ 7 Krypto sofort schließen · 5 Aktien vormerken
```

**Verworfen — Variante 1: eine Zahl, zwei Verben.** „ALLE 12 Positionen
schließen bzw. vormerken" ist kürzer und formal nicht falsch. Aber wer sie
liest, weiß hinterher nicht, **wie viele Positionen nach dem Tap noch offen
sind** — und genau das ist im Crash-Fall die Frage. Eine Zahl, die für zwei
verschiedene Vorgänge steht, beantwortet sie nicht.

**Verworfen — Variante 2: Beschriftung lassen, Hinweis erweitern.** Das war der
Zustand vor dieser Änderung, und er ist genau der Grund für die Aufgabe: der
Hinweistext wird im Ernstfall nicht gelesen, der Knopftext schon. Er ist das
Letzte, was vor dem Tap im Blick ist.

**Zwei Randfälle, bewusst behandelt:**

- Ist nur **eine** Welt betroffen, steht auch nur eine Zahl da. Eine Zeile
  „0 Krypto sofort schließen" wäre Rauschen.
- Ergibt die Aufteilung **nicht** die Gesamtzahl (eine dritte Anlageklasse, ein
  fehlendes Feld), bleibt die bisherige, sicher richtige Beschriftung. Lieber
  unspezifisch als falsch aufgeteilt.

Der Hinweis unter dem Knopf nennt den Warteauftrag zusätzlich — über
`warteauftragHinweisKurz()` aus `app.js`, denselben Satz, den auch die
Bot-Seite benutzt.

---

# Architektur

**Eine Stelle für die Krypto/Aktien-Unterscheidung.** Sie fällt serverseitig in
`boersenlage()`: für Krypto steht dort `kalender_gilt: false`, und daran hängt
alles Weitere. Für Krypto-Bots ändert sich **nichts** — keine Statuszeile, kein
Knopfwechsel. Eine Fallunterscheidung je Ansicht wäre je Ansicht die
Gelegenheit gewesen, sie einmal zu vergessen.

`wirdVorgemerkt()` prüft deshalb `kalender_gilt` **und** `warteauftrag_noetig`,
nicht nur das zweite. Der Unterschied sieht nach Haarspalterei aus, ist aber die
ganze Zusicherung: wer nur das Folgefeld prüft, verlässt sich darauf, dass das
Backend für Krypto nie etwas anderes schickt — und hat die Unterscheidung damit
stillschweigend in die Anzeige verlegt. Eine eigene Prüfung sichert das ab
(siehe M6 unten).

**Eine Quelle für die Darstellung**, in `app.js`, wie `gewichtungsZeilen()` und
`positionsanzahlZeilen()`. Eine Prüfung schlägt fehl, sobald
`boersenstatusZeile` oder `wirdVorgemerkt` in `bot.html` oder `index.html`
auftaucht.

**Auto-Refresh.** Statuszeile *und* Knopfbeschriftung hängen an derselben
Antwort und werden zusammen neu gezeichnet — auf der Übersicht in
`zeichneUebersicht()`, auf der Bot-Seite in `ladeSchliessInfo()`. Beide laufen
im 60-s-Datentakt. Der Übergang geschlossen → offen springt damit von selbst
um, ohne Neuladen.

## Ausdrücklich nicht gebaut

**Keine Sperre.** Der Knopf bleibt außerhalb der Handelszeiten bedienbar, der
Warteauftrag entsteht wie bisher. Das ist die Entscheidung des Nutzers: der
Crash-Knopf ist für den Moment gebaut, in dem er schnell reagieren will — ein
vorgemerkter Auftrag ist dann besser als ein deaktivierter Knopf. Eine Prüfung
hält das fest (`disabled` darf in `positionsZeile` nicht auftauchen).

`notifications/boersenkalender.py`, `notifications/warteauftraege.py`,
`dashboard/schliessen.py` und `dashboard/warteauftraege_ausfuehren.py` sind
**unverändert** — `git diff` fasst keine davon an.

---

# Tests

| Suite | vorher | nachher |
|---|---|---|
| `dashboard/test_dashboard.py` | 753 | **784** |
| `dashboard/test_boersenstatus.js` *(neu)* | – | **53** |

**Je Funktion geprüft, nicht im ganzen Dokument.** Diese Fehlerklasse ist in
#62, #66, #67 und #73 viermal aufgetreten. Acht Einhängepunkte werden einzeln
geprüft:

| Ansicht | Funktion | hängt an |
|---|---|---|
| index.html | `zeichneBoersenstatus` | `boersenstatusZeile(` |
| index.html | `zeichneUebersicht` | `zeichneBoersenstatus(` |
| index.html | `zeichneUebersicht` | `crashKnopfText(` |
| bot.html | `zeichneBoersenstatus` | `boersenstatusZeile(` |
| bot.html | `ladeSchliessInfo` | `zeichneBoersenstatus(` |
| bot.html | `positionsZeile` | `boerseGeschlossen(` |
| bot.html | `zeichnePositionen` | `boerseGeschlossen(` |
| bot.html | `boerseGeschlossen` | `wirdVorgemerkt(` |

**Verhaltenstest der erzeugten Ausgabe** (`test_boersenstatus.js`): beide
Ansichten werden mit einem DOM-Ersatz wirklich ausgeführt, für offen, nach
Handelsschluss, Wochenende, Feiertag (Thanksgiving **und** Karfreitag),
Halbtag, unbekannt und Krypto. Die Fälle sind keine erfundenen Zahlen — sie
stammen aus dem echten `boersenkalender.py`, abgefragt zu Zeitpunkten, die der
Test kennt.

**Mit echt entfernter Abhängigkeit geprüft, nicht behauptet.** Ohne
`pandas_market_calendars` (per Import-Blocker wirklich entfernt):

```
[OK ] Das Paket ist wirklich blockiert
[OK ] status() wirft nicht, sondern liefert offen=None
[OK ] Aktien-Lage: unbekannt=True
[OK ] KRYPTO bleibt handelbar - der Notfallweg dort ist unberuehrt
[OK ] /api/portfolio antwortet trotzdem: HTTP 200
[OK ] und benennt die Lage als unbekannt, statt etwas zu behaupten
[OK ] Die Bot-Liste ist vollstaendig da - die Anzeige reisst die Seite nicht mit
```

> **Eine Einordnung dazu, damit sie nicht falsch gelesen wird:** für
> **Aktien**-Bots lehnt PR #71 das Schließen bei unbekanntem Kalender
> ausdrücklich ab (fail closed) — das ist bestehende, dokumentierte
> Entscheidung und wurde nicht angetastet. „Der Notfallweg wird nicht
> blockiert" heißt hier: **die Anzeige** ist nie die Ursache. Die Seite
> rendert, die Bot-Liste ist vollständig, und Krypto bleibt schließbar.

**12 Mutationsproben, 12 erkannt.** Eine (M6, `wirdVorgemerkt` ohne
`kalender_gilt`) ging in der ersten Fassung durch: die Krypto-Vorlage hatte
`warteauftrag_noetig: false`, das Weglassen der Prüfung änderte also nichts.
Die Zusicherung wurde nachgeschärft — jetzt gibt es einen Fall mit einer
widersprüchlichen Lage (`kalender_gilt: false`, aber `warteauftrag_noetig:
true`), an dem sich zeigt, welches Feld wirklich entscheidet.

**Keine Regression:** `broker/test_broker.py` 163, `broker/test_ibkr.py` 200,
`test_gewichtung.js` 35, `test_zeitzone.js` 24, `test_zustandsmaschine.js` 27,
`test_manual_close.py`, `test_empfehlung_format.py` 70,
`test_caffeinate_plist.py` 52.

---

# Was eine Sichtprüfung am iPhone verlangt

Automatisiert ist, **was der Code erzeugt** — nicht, wie es aussieht. Drei
Punkte sind nur am Gerät zu beurteilen und stehen als eigener Schritt im
Testauftrag:

1. **Der Platz der Statuszeile.** Sie steht auf beiden Seiten direkt unter der
   Kopfzeile. Ob sie dort mit dem Ladeindikator kollidiert oder die Kacheln zu
   weit nach unten drückt, zeigt nur das Gerät.
2. **Der längere Crash-Knopftext.** `⚠ 7 Krypto sofort schließen · 5 Aktien
   vormerken` ist deutlich länger als vorher. Auf 390 px muss er umbrechen,
   nicht überlaufen — und der Umbruch sollte nicht zwischen Zahl und Einheit
   fallen.
3. **Die Farbe der „geschlossen"-Zeile.** Sie trägt Bernstein
   (`--warteauftrag`-Ton), nicht Rot: geschlossen ist kein Fehler, sondern der
   Normalfall am halben Tag. Ob das im Dunkelmodus als Hinweis und nicht als
   Warnung gelesen wird, ist eine Beurteilung, keine Messung.

## Offene Punkte

- Die **Wochentagsangabe** lautet auch dann „schließt Donnerstag, 22:00 Uhr",
  wenn Donnerstag heute ist. „schließt heute um 22:00" läse sich flüssiger,
  bräuchte aber einen Bezug auf die aktuelle Uhrzeit und machte die Ausgabe
  vom Zeitpunkt des Testlaufs abhängig. Bewusst zugunsten der Eindeutigkeit
  entschieden; falls es stört, ist es eine kleine, isolierte Änderung in
  `boersenZeit()`.
- Die Statuszeile erscheint auf der **Übersichtsseite immer**, auch wenn dort
  gerade keine Aktien-Position offen ist. Das schien mir richtig — sie
  beantwortet auch die Frage „lohnt es sich, jetzt hinzusehen" —, ist aber eine
  Geschmacksfrage.
