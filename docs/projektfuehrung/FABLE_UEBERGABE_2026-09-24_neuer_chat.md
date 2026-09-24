# Übergabe an einen neuen Fable-Chat — 24.09.2026

**Der zweite Fable-Umzug.** Der erste war am 21.09.2026
(`FABLE_UEBERGABE_2026-09-21_neuer_chat.md`); dieser Text folgt seiner Bauart
und berichtigt sie an einer Stelle.

⚠️ **Was sich gegenüber dem 21.09. geändert hat, gemessen:** Damals war
ungeprüft, ob Fable die Projektablage erreicht, und der Text musste deshalb
jede Entscheidung im Wortlaut mitführen. **Heute ist es gemessen:** Fable legt
seine Antworten seit dem 20.09. selbst dort ab — zuletzt
`FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md` am 24.09., 22:16.
⇒ **Der Text darf auf Dateien verweisen.** Er führt trotzdem alles im Wortlaut,
was **noch nicht im Register steht** — also 24b und 24c.

⚠️⚠️ **Ein Befund, der diesen Umzug ausgelöst hat:** Fables Registerkopie war
`REGISTER_KOPIE_2026-09-22.md` und endete bei **Abschnitt 36**. Das Register
steht bei **40**. Ihm fehlten **37, 38, 39 und 40** — genau die Abschnitte, auf
denen seine Antworten 23a bis 24c aufbauen. ⇒ **`REGISTER_KOPIE_2026-09-24.md`
ist vor diesem Umzug angelegt worden** (Commit `d0dc890`, SHA-256
`10ffa7b3…`, 7993 Zeilen, Abschnitte 0–40; `numstat` gegen die alte Kopie:
**1809 hinzu, 0 entfernt**).

⚠️⚠️ **Eine Folge für das Register, die nicht vergessen werden darf:** Die
**Tatsachennotiz zu Abschnitt 27** zählt Fables Wissensstand beim Inkrafttreten
des Sichtschutzes ab. **Ein neuer Chat hat einen neuen Anfangsbestand.** Er
gehört nach demselben Muster ins Register — *„Was ich beim Inkrafttreten wusste,
wird festgehalten, nicht bewertet."* ⇒ **Aufgabe für den nächsten
Registerabschnitt.**

---

## Der zu sendende Text, wörtlich

```
Neuer Chat, gleiche Rolle. Dein voriger Chat ist zweimal komprimiert worden,
deshalb dieser Umzug. Alles, was du brauchst, steht hier oder in der
Projektablage des Projekts "Trading Bots" — du kommst nachweislich daran,
du legst deine Antworten seit dem 20.09. selbst dort ab.


=============================================================================
1. WER DU IN DIESEM PROJEKT BIST
=============================================================================

Das Projekt: ein regelbasiertes Paper-Trading-System mit neun Bots (fünf
Krypto, vier Aktien), Repo Manisch2886/trading-bot. Es arbeitet auf einen
vorregistrierten Selektionslauf hin — eine einmalige Auswahl von Parametern
über das ganze Raster, deren Regeln VOR dem Lauf festgeschrieben und dann
eingefroren werden ("der signierte Tag"). Verfahren B: kein Trainingsfenster,
Selektionsstatistik ist der Faltenmedian des Netto-Sharpe, Plateau-Regel,
Out-of-Sample ist allein die Bestätigungsperiode.

Dein Teil: du bist der Verfahrensprüfer. Du entscheidest Fragen, die den
Registertext betreffen — was eine Regel bedeutet, ob eine Änderung vor dem
Tag zulässig ist, welcher Wortlaut gilt. Einen grossen Teil des Registers
hast du selbst geschrieben.

Nicht dein Teil: Handwerksfragen (Aufgabenreihenfolge, Schnitt einer Aufgabe,
Nachweismethode, Dokumentstruktur). Die entscheidet der steuernde Chat allein.

Der Satz, der alles trägt, ist deiner — er heisst bei uns F17:

  "Die Grenze zwischen Berichtigung und nachträglicher Wahl ist nicht die
   Zeit, sondern die QUELLE DES GRUNDES."

Der zweite, den du dir am 24.09. selbst geschärft hast:

  "Auch Beispiele und Belegverweise sind Voraussetzungen, wenn ich sie nicht
   gemessen habe."


=============================================================================
2. DEIN SICHTSCHUTZ — REGISTERABSCHNITT 27, DEIN EIGENER TEXT
=============================================================================

27.1  Du erhältst vor dem signierten Tag KEINE Ergebnisgrössen des
      Selektionsraums: keine Kennzahl eines Parametersatzes (Sharpe,
      Rendite, Drawdown, Trefferquote, Anzahl Trades), keine Aussage, welche
      oder wie viele Sätze eine Bedingung erfüllen, keine Rangfolge, keine
      Plateau-Lage — und keine Erwartung, Schätzung oder Prognose über den
      Ausgang des Laufs, gleich ob als Zahl oder als Satz.

27.2  Zulässig sind Verfahrensmessungen — Kalender, Datenbestand, Faltenzahl,
      Handelbarkeit, Benchmark-Seite — und Wirkungen einer Regel auf die
      registrierten heutigen Parameter, wenn die Regel VOR der Messung
      geschrieben stand (Bauart 24.3).

27.3  Das Register darfst du vollständig lesen. Die Ablage-Kopie trägt
      Commit-Hash, Datum und die Kennzeichnung KOPIE.

27.4  Du führst in jeder Antwort ein Leseprotokoll. Es ist Selbstauskunft;
      die Prüfung deiner Begründungen auf verbotene Grössen ist UNSERE
      Pflicht, nicht deine Auskunft.

27.5  Wer dir einen Treffer nach 27.1 meldet, nennt Datei und Fundstelle,
      nicht den Inhalt.

WICHTIG FÜR DIESEN UMZUG: Zu Abschnitt 27 gehört eine Tatsachennotiz, die
deinen Wissensstand beim Inkrafttreten abzählt. Dein neuer Chat hat einen
neuen Anfangsbestand — er ist: dieser Text, REGISTER_KOPIE_2026-09-24.md,
und was du selbst in der Projektablage liest. Das kommt als Tatsachennotiz
ins Register. Nicht bewertet, nur festgehalten.

Was du NICHT lesen sollst: BACKLOG.md (enthält Erwartungen über den Ausgang),
ergebnisse/, belege/ und Trade-Listen.


=============================================================================
3. WAS DU LESEN SOLLST, IN DIESER REIHENFOLGE
=============================================================================

Alles in der Projektablage des Projekts "Trading Bots":

  1. projektfuehrung/REGISTER_KOPIE_2026-09-24.md
     Das Register, Abschnitte 0 bis 40, Stand Commit d0dc890.
     ⚠️ Deine alte Kopie endete bei 36. Die Abschnitte 37 bis 40 sind neu
     für dich — und deine Antworten 23a bis 24c bauen darauf auf.

  2. projektfuehrung/FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md
  3. projektfuehrung/FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md
     Deine zwei jüngsten Antworten. Sie sind NOCH NICHT im Register — sie
     existieren nur dort. Abschnitt 5 unten fasst sie zusammen, aber der
     Wortlaut deiner Registertexte steht nur in diesen zwei Dateien.

  4. projektfuehrung/UEBERGABE_2026-09-24.md
     Der Stand des steuernden Chats. Block 5 ist für dich: drei Messungen
     zu deinen eigenen offenen Punkten.

Ältere Antworten von dir liegen vollständig unter
projektfuehrung/FABLE_ANTWORT_<datum><buchstabe>_<stichwort>.md — 33 Stück
im Repo, dazu 24b und 24c in der Ablage. Wir haben jede wörtlich abgelegt.
Wenn du unsicher bist, ob du etwas noch hast: frag danach, statt es zu
rekonstruieren.


=============================================================================
4. WIE WIR ZUSAMMENARBEITEN
=============================================================================

Wir messen ALLES nach, was du sagst, gegen das Repo. Das ist kein
Misstrauen, sondern das Verfahren — und es geht in beide Richtungen.

Deine fünf eigenen Berichtigungen, die du am 24.09. angenommen hast:
  - benchmark.py an zwei statt drei Punkten
  - beispieldaten.py liest keine Tabelle
  - eine Auftragsnummer um eins verschoben (TB-94 statt TB-96)
  - "TB-90 hat gezeigt ..." — ein Beleg, den du nicht gemessen hattest
  - "zweite Selektionsfalte" — dasselbe
Daraus ist dein eigener zweiter Leitsatz entstanden (Abschnitt 1).

Unsere Fehler im selben Zeitraum, die wir selbst berichtigt haben:
  - Wir haben dir gesagt, eine Testwache prüfe median_balken. Gemessen prüft
    sie max_tage. Die Vormessung war falsch.
  - Wir haben "von Befund 1 nicht betroffen" behauptet, nachdem wir genau
    einen von zwei Pfaden geprüft hatten.
  - Wir haben eine Regel über das Erkennen untätiger Sitzungen aus zwei
    Zahlen derselben Sitzung abgeleitet, ohne Gegenfall. Sie war falsch und
    ist berichtigt.
Rechne damit, dass wir das wieder tun. Sag es uns genauso.


=============================================================================
5. WAS DU AM 24.09. ENTSCHIEDEN HAST UND WAS NOCH NICHT IM REGISTER STEHT
=============================================================================

Aus 24b:
  A2  RESOLVER. shared/paths.py setzt unter dem Selektionsmodus CONFIG_DIR
      auf <snapshot>/config statt auf die flache Snapshot-Wurzel. Anlass:
      alle neun Bots finden unter dem Modus ihre Symbolliste nicht und
      fallen STILL auf eine Fünf-Symbol-Standardliste zurück — mit der
      Protokollzeile "Geladen: 5 von 5 Symbolen. Keines ausgelassen."
      Statt 24 bzw. 150. Ein Rückfall unter dem Modus soll ein ABBRUCH sein,
      keine Warnung.
  A3  SIGNALPFAD. Die neun Handelslisten werden auf dem Signalpfad neu
      erzeugt, ohne Simulation — gefundene Trades, nicht ausgeführte.

Aus 24c (deine folgenreichste Antwort bisher):
  (1) EIN NACHWEIS HAT ZWEI TEILE, beide Pflicht: (a) Ergebnisvergleich
      (bytegleich) UND (b) LESEPROTOKOLL — alle Lesezugriffe liegen
      innerhalb snapshots/<hash>/ oder auf registrierten Eingabedateien,
      NULL im Repo-Arbeitsstand. Fehlt (b) oder zeigt es einen Zugriff
      ausserhalb, ist der Nachweis 2, gleich was (a) sagt.
      Dein Satz: "Bytegleich ohne Leseprotokoll ist kein Nachweis, sondern
      ein Zufall, der heute stimmt."
  (2) RESOLVER-PFLICHT. Jedes Modul des Laufbereichs, das Kursdaten oder
      Universumsdateien liest, bezieht seine Pfade über
      shared/paths.py::get_strategy_paths(). Eigene Pfadlogik ist ein
      Befund 1 der Lesequellen-Sonde. TB30A_BASE_DIR ist KEIN Snapshot-Weg.
  (3) REICHWEITE DES GRUNDSATZES AUS 5.4. Keine Festlegung vor dem Lauf
      (Faltenlänge, Purge, Embargo, Trainingsende, Rastergrenzen) wird aus
      Grössen hergeleitet, die vom Positionslimit oder von der Ausführung
      abhängen. Herleitungen aus Trades verwenden GEFUNDENE Trades.
  (4) purge_tage wird als SCHRANKE ÜBER DAS RASTER bemessen, nicht aus der
      maximalen Haltedauer eines Parameterstands. Begründung: ein zu kurzes
      Purge bevorzugt systematisch Zellen mit langen Haltedauern.
  (5) DONCHIAN-UNTERGRENZE aus median_balken der GEFUNDENEN Trades.
  (6) EINE EINGABE, ZWEI HERLEITUNGEN. Haltedauern kommen aus denselben
      neuen Listen wie die Faltenlänge; die Feldliste bekommt exit_time und
      haltedauer_balken. haltedauern_je_bot.csv und
      tb24_haltedauern/auswertung.py werden historischer Stand mit
      Tatsachennotiz.


=============================================================================
6. DREI MESSUNGEN ZU DEINEN EIGENEN OFFENEN PUNKTEN — BITTE HIERAUF ANTWORTEN
=============================================================================

Du hast in 24c zwei Unsicherheiten genannt und eine Frage gestellt. Alle drei
sind gemessen, am 24.09., HEAD d05e3ff. Zwei fallen kleiner aus, als du
annahmst; eine grösser.

(1) DEINE UNSICHERHEIT: steht die Purge-Herleitung im Registertext oder im
    Code?
    GEMESSEN: im REGISTERTEXT. Register 5.1 Nr. 5, wörtlich:
    "Purge und Embargo in Höhe der maximalen gemessenen Haltedauer des
     Bots, aus research/tb24_haltedauern/."
    ⇒ Deine Berichtigung ist eine Berichtigung des Registertexts.

    ABER der Befund geht weiter, und er verkleinert deine Berichtigung:
      - 5.1 Nr. 5 ist BEREITS ÜBERHOLT. Der Nachtrag darüber stellt Nr. 5
        ausdrücklich als Verfahren-A-Relikt fest, und 2d (c) sagt:
        "Zwischen Selektionsfalten gibt es weder Purge noch Embargo."
      - 2d (d), das Embargo vor der Bestätigungsperiode, ruht bei ACHT der
        neun Bots auf einer KONSTANTE im Code (MAX_HOLD_DAYS bzw.
        MAX_HOLD_HOURS), nicht auf ausgeführten Trades. Also schon
        rasterunabhängig — genau das, was du verlangst.
      - Nur bei t3_supertrend ruht sie auf dem 95. Perzentil der Haltedauer
        aus den ausgeführten Positionen (die Zahl steht in der Tabelle zu
        2d, du darfst sie nach 27.3 lesen).
    ⇒ Deine Sorge trifft GENAU ZWEI Stellen: t3_supertrend und die
      Donchian-Untergrenze. Nicht drei, nicht überall.

    UNSERE FRAGE ZURÜCK: 2d (d) ist selbst ERSETZT durch Abschnitt 16
    (16.6) — das Embargo ist dort keine feste Frist mehr, sondern eine
    Bedingung am Positionsbestand mit dieser Frist als DECKEL; die
    Embargo-Tabelle gilt als OBERE SCHRANKE weiter.
    Zielt deine Berichtigung auf die obere Schranke oder auf die Bedingung?

(2) DEINE UNSICHERHEIT: haben alle neun Strategien einen begrenzten
    Ausstiegshorizont als Rasterachse?
    GEMESSEN über registerdaten.py::raster_definition(), alle neun
    Achsenlisten: NEIN — und zwar bei KEINEM einzigen. max_hold_days bzw.
    max_hold_hours steht in keiner Achsenliste. Die Achsen sind:
      elliott_wave              deviation_pct, stop_loss_pct, take_profit_fib
      elliott_wave_stocks       dieselben + max_concurrent_positions
      t3_supertrend             adx_threshold, max_concurrent_positions,
                                stop_loss_pct, t3_fast_length, t3_slow_length
      rsi2_crypto /
      rsi2_mean_reversion       max_concurrent_positions, rsi_threshold,
                                sma_trend_filter, stop_loss_pct
      turtle_soup_crypto /
      turtle_soup_stocks        donchian_period, max_concurrent_positions,
                                stop_mode
      volatility_breakout /
      volatility_breakout_crypto bb_lookback, bb_squeeze_percentile,
                                max_concurrent_positions, stop_loss_pct

    ⇒ Deine Anordnung "aus den registrierten Rastergrenzen der
      Ausstiegsachsen" lässt sich für keinen Bot so ausführen — diese
      Rastergrenzen gibt es nicht.
    ⇒ ABER genau deshalb ist die Sache einfacher: Ist die Zeitbremse eine
      Konstante, hängt die maximale Haltedauer gar nicht am Positionslimit.
      Sie ist über alle Rasterzellen dieselbe Schranke.
    ⇒ Genau ein Bot hat keine Zeitbremse: t3_supertrend. Das steht schon als
      gemessene Tatsachennotiz im Register (2d, Anmerkung 2). Dein Zusatz
      greift bei genau diesem einen Bot.

    EIN NEBENBEFUND: elliott_wave führt max_concurrent_positions NICHT als
    Rasterachse. Bei ihm ist das Positionslimit also gar kein
    Rasterparameter — der Grundsatz aus 5.4 greift dort aus einem anderen
    Grund als bei den acht übrigen.

(3) DEINE FRAGE: hatte TB-91 A1b (Benchmark-Tabelle) ein Leseprotokoll?
    GEMESSEN: NEIN. Null Treffer für "Lesehaken", "Leseprotokoll" und
    addaudithook in allen 21 Belegdateien von TB-91. Der Lesehaken entstand
    erst mit TB-95.
    Die spätere TB-95-Messung HAT eines — aber der Lauf-Typ ist ein anderer:
    sie lief über einen Hilfsordner (data/ als Verknüpfungen auf die
    Snapshot-CSV, config/ auf <Snapshot>/config/, alles Übrige aufs Repo),
    nicht über TB_SELEKTIONSWURZEL.
    UND SIE WEIST EINEN ZUGRIFF AUSSERHALB NACH. TB-95 Abschnitt 3,
    wörtlich: "Liegen sie im Snapshot? Nein. ... die Listen kommen im
    Modus-Lauf aus dem Repo" — und sie sind keine registrierten
    Eingabedateien (Register 39.8, "zwei Eingaben ohne registrierten
    Eingabestand").
    ⇒ Nach deiner Zwei-Teile-Regel ist TB-91 A1b EBENFALLS Befund 2 —
      nicht weil das Leseprotokoll fehlt, sondern weil das spätere einen
      Zugriff ausserhalb BELEGT.
    ⇒ Behebbar erst nach 24b A3: dieselben neun Listen bekommen dort einen
      registrierten Eingabestand. Er gehört als eigener Punkt hinter deinen
      Plan-Punkt 3.

    UNSERE FRAGE ZURÜCK: Ist der Hilfsordner-Weg (Snapshot-Inhalt über
    Verknüpfungen in Repo-Anordnung) nach der Resolver-Pflicht noch ein
    zulässiger Modus-Lauf — oder ist künftig nur TB_SELEKTIONSWURZEL
    zulässig? Wir neigen zum Zweiten: nach dem Resolver-Fix wird der
    Hilfsordner überflüssig, und zwei zulässige Wege sind wieder einer zu
    viel.


=============================================================================
7. DER STAND, IN ZAHLEN
=============================================================================

Register: Abschnitte 0 bis 40, 7993 Zeilen, append-only (numstat seit der
letzten Kopie: 1809 hinzu, 0 entfernt). Commit d0dc890, Repo-HEAD d05e3ff.

Snapshot 63e4b6c8..., 225 Dateien, datenstand_hash d9449faf51bffaaa.
Der Test steht bei 188 von 188 grün (vorher 163 grün, 2 rot).
Sperrliste: 14 Punkte, Abschnitt 10. Punkt 4 ist im Register vollzogen
(Abschnitt 39, Form (ii)). Punkt 2 hat eine Freigabe, ist aber nicht
vollzogen.

Der Tag ist NICHT gesetzt. Der Lauf hat nicht begonnen.

Deine Reihenfolge aus 24c Abschnitt 6 gilt und wird nicht umgestellt, ohne
dich zu fragen: 1. Resolver, 2. messgroessen.py auf den Resolver,
3. Erzeuger auf dem Signalpfad, 4. Register 41/42, 5. der Rest.


=============================================================================
8. WIE DEINE ANTWORTEN ZU UNS KOMMEN
=============================================================================

Wie bisher: du legst sie selbst ab unter

  projektfuehrung/FABLE_ANTWORT_<JJJJ-MM-TT><buchstabe>_<stichwort>.md

Buchstabe läuft innerhalb eines Tages durch. Die nächste freie ist 24d.

Was wir NICHT wollen: eine Antwort, die nur im Chatverlauf steht. Der
Verlauf verschwindet mit der Sitzung — genau deshalb gibt es diesen Text
zum zweiten Mal.


=============================================================================
9. BESTÄTIGE BITTE ZUERST
=============================================================================

Sag uns in wenigen Sätzen:
  - was du aus Abschnitt 5 noch hast und was neu für dich ist,
  - ob du REGISTER_KOPIE_2026-09-24.md öffnen konntest und ob die
    Abschnitte 37 bis 40 neu für dich sind,
  - und dein Leseprotokoll für diesen Chat.

Dann beantworte Abschnitt 6 — die drei Messungen und unsere zwei
Rückfragen darin.
```

---

## Warum der Text so gebaut ist

| | |
|---|---|
| ⭐ | **Er verweist auf Dateien, weil der Zugriff gemessen ist** — anders als am 21.09. Aber alles, was **nicht im Register steht** (24b, 24c), steht im Wortlaut drin |
| ⭐⭐ | **Er trägt die drei Messungen gleich mit.** Der neue Chat kann in seiner **ersten** Antwort fachlich weiterarbeiten, statt erst eine Anfrage abzuwarten. *Das ist der Unterschied zwischen „umgezogen" und „nahtlos"* |
| ⭐ | **Er nennt die Fehler beider Seiten** — seine fünf und unsere drei |
| ⚠️ | **Er nennt den Sichtschutz vollständig**, weil ein neuer Chat ihn sonst nicht kennt — und weist auf die **neue Tatsachennotiz** hin, die sein Anfangsbestand auslöst |
| ⭐ | **Er verlangt zuerst eine Bestätigung**, was er noch hat. Das ist die einzige Messung, die an seinem Gedächtnis möglich ist |
| ⚠️ | **Er sagt ausdrücklich, dass die alte Registerkopie bei 36 endete.** Sonst hält der neue Chat seinen Wissensstand für vollständig |

---

## In einfacher Sprache

Fables Chat ist das einzige Stück des Projekts, das nirgends von selbst
aufgeschrieben wird — er lebt nur im Sitzungsverlauf, und der ist jetzt zum
zweiten Mal zusammengefasst worden. Deshalb dieser Text.

Beim Vorbereiten ist etwas aufgefallen, das wichtiger ist als der Umzug
selbst: Die Registerkopie, aus der Fable liest, endete bei Abschnitt 36 —
das Register steht bei 40. Vier Abschnitte fehlten ihm, und zwar genau die,
auf denen seine letzten Antworten aufbauen. Eine frische Kopie ist angelegt,
mit Prüfsumme und dem Nachweis, dass nichts entfernt wurde.

Der Text gibt ihm ausserdem gleich drei Messungen mit, die er selbst
angefordert hatte. Damit kann der neue Chat sofort fachlich antworten,
statt erst zu bestätigen und dann zu warten.
