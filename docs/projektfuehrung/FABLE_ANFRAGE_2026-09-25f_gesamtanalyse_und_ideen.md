# FABLE_ANFRAGE 2026-09-25f — Gesamtanalyse des Projektverlaufs und neue Ideen für den weiteren Weg

**Vom Betreiber beauftragt, 25.09.2026, 22:28.** Diese Anfrage ist **anders als die übrigen**: keine Prüfung eines einzelnen Auftrags, sondern ein Blick auf das ganze Projekt. Sie steht **neben** den offenen Anfragen 25d und 25e und ersetzt sie nicht. Bitte beantworte 25d/25e getrennt, wenn du sie noch nicht beantwortet hast.

---

## 0. Deine Rolle für diese eine Antwort

Du bleibst Verfahrensprüfer. Für diese Antwort bekommst du eine zweite Rolle dazu: **kritischer Berater des Betreibers**, der das Projekt von aussen ansieht, als würde er es zum ersten Mal übernehmen. Wo sich die beiden Rollen reiben, sag es offen.

## 1. Freigabe für Recherchen, wörtlich vom Betreiber

> Bei Recherchen soll Fable Zugriff auf alle Webseiten erhalten, ohne dass ich dies gesondert bestätigen muss. Diese Freigabe wird nach diesem Vorgang wieder aufgehoben.

Also: Recherchiere frei im Netz, wo es der Antwort dient: Fachliteratur, Studien, Börsen- und Broker-Dokumentation, Regulierung, Kosten, Datenquellen, Werkzeuge. **Jede Aussage aus einer Recherche bekommt eine Quelle mit Link.** Die Freigabe gilt nur für diese Antwort.

## 2. Was du lesen sollst

Die Projektablage „Trading Bots“ **vollständig**, soweit sie dir zugänglich ist. Mindestens:
- **Grundlagen:** `PRUEFPRINZIPIEN.md`, `ARBEITSWEISE.md`, `DOKUMENTATIONSSTANDARD.md`, `BACKLOG.md` (+ Nachträge), `PLAN_VOR_DEM_TAG.md`, `RECHERCHE_vintage_datenlage.md`, `BESTANDSAUFNAHME_TB-30b.md` (+ Nachträge), `JOURNAL_NACHTRAG_2026-09-18.md`.
- **Register:** `REGISTER_KOPIE_2026-09-24_teil1_0_bis_23.md`, `…teil2_24_bis_36.md`, `…teil3_37_bis_40.md`.
- **Übergaben:** `UEBERGABE_2026-09-19.md`, `UEBERGABE_2026-09-24.md`, `UEBERGABE_2026-09-25.md` (mit Nachträgen), `UMZUG.md`, `FABLE_UEBERGABE_*`, `FABLE_WOCHENRUECKMELDUNG_*`.
- **Verlauf:** alle `FABLE_ANFRAGE_*` und `FABLE_ANTWORT_*` seit dem 18.09., alle Aufträge `MAC_TB-*` unter `auftraege/`, `STOFFSAMMLUNG_REGISTER_41_42.md`.
- **Aussenseite:** `PRUEFUNG_2026-09-25_drei_festlegungen_im_speicher.md` (regulatorische Ausschlüsse: Funding-Carry, PRIIPs, gehebelte Produkte handelbar, aber nicht registrierbar).

Führe wie immer ein **Leseprotokoll**: was gelesen, was nicht, was nur in Ausschnitten.

## 3. ⛔ Was unverändert gilt, auch in dieser Antwort

- **Sichtschutz 27.1:** keine Ergebnisgrössen des Selektionsraums vor dem signierten Tag. Du forderst keine an und leitest keine her. Ideen zur Profitabilität stützen sich auf Verfahren, Literatur, Kosten, Marktstruktur und Regulierung, **nicht** auf die Ergebnisse dieser Selektion. Hältst du eine Zahl für nötig, benenne sie als **Messbitte für nach dem Tag**.
- **Die laufende Vorregistrierung wird durch diese Antwort nicht geändert.** Jede neue Strategie, Achse oder Regel ist ein Kandidat für einen **späteren, eigenen, vorab registrierten Durchgang**. Sie ist kein Eingriff in den jetzigen. Wo eine Idee den laufenden Durchgang berühren würde, markiere sie ausdrücklich und begründe, warum sie trotzdem vor den Tag gehört, oder warum nicht.
- **Keine Anlageberatung** im rechtlichen Sinn. Kennzeichne regulatorische und steuerliche Aussagen (Betreiber wohnt in Deutschland) als Einordnung mit Quelle, nicht als Rechtsrat.

## 4. Teil A — Analyse und Prüfung des bisherigen Verlaufs

1. **Der Weg in Kürze:** Was wurde seit Projektbeginn gebaut, entschieden und verworfen? Eine Zeitleiste der Wendepunkte, nicht jedes Detail.
2. **Stand gegen Ziel:** Wie weit ist das Projekt vom signierten Tag und vom ersten Selektionslauf entfernt? Welche Punkte liegen **wirklich** auf dem kritischen Pfad, welche nicht? Schätze den Restaufwand in Aufträgen.
3. **Verhältnis Verfahren zu Fortschritt:** Die letzten Tage bestanden fast nur aus Verfahrensarbeit (Resolver, Rückfälle, Klassen, Sonden). Wo war das nötig? Wo ist es inzwischen **mehr Absicherung, als das Risiko rechtfertigt**? Benenne konkret, was man vereinfachen, bündeln oder nach dem Tag verschieben könnte, ohne die Aussagekraft des Laufs zu gefährden. Und umgekehrt: Wo fehlt noch etwas Wesentliches?
4. **Methodische Prüfung:** Hält das Selektionsdesign der Fachliteratur stand? Zu prüfen sind Walk-forward mit Falten, Plateau-Regel, Drawdown-Nebenbedingung gegen Benchmark, DSR/N-Buchführung, Beta-Bereinigung, Bestätigungsperiode, Kostenmodell, Universumsauswahl, Survivorship, Look-ahead. Wo ist es stark, wo gibt es blinde Flecken? Mit Quellen.
5. **Die neun Bots:** Sind sie als Portfolio sinnvoll, oder messen mehrere dasselbe (z. B. Trendfolge in Krypto und Aktien, Mean Reversion)? Welche Lücken hat das Portfolio (Anlageklassen, Zeithorizonte, Marktphasen)?
6. **Arbeitsweise:** Steuernder Chat, Mac-Sitzungen, Sitzungswächter, Fable als Prüfer, der Betreiber als Engpass bei Freigaben. Was funktioniert, was kostet unverhältnismässig Zeit? Konkrete Verbesserungen.
7. **Risiken:** die fünf grössten Risiken für das Projekt (technisch, methodisch, operativ, regulatorisch, persönlich-zeitlich), je mit Gegenmassnahme.

## 5. Teil B — Neue Ideen für den weiteren Weg (umfangreich)

Der Betreiber wünscht **viele neue Ideen**. Bitte **mindestens 25**, gegliedert nach:

- **Strategien und Signale:** neue Strategiefamilien oder Varianten, die das Portfolio ergänzen (z. B. Carry, Saisonalität, Cross-Asset-Momentum, Volatilitäts-Regime, Paar-/Spread-Handel, Ereignisse, On-Chain-Daten bei Krypto); was in der Literatur nach Kosten robust ist.
- **Portfolio und Risiko:** Zuteilung über die Bots (Risk Parity, Volatilitätsziel, Korrelationsdeckel, Kelly-Bruchteile), Drawdown-Steuerung auf Portfolioebene, Regime-Schalter.
- **Ausführung und Kosten:** Ordertypen, Slippage, Gebührenstufen, Maker/Taker, Zeitpunkt der Ausführung, Broker- und Börsenwahl (für einen Betreiber in Deutschland), Steuerlast als Kostenfaktor.
- **Daten:** zusätzliche oder bessere Datenquellen (Qualität, Kosten, Point-in-Time, Survivorship-frei), Datenprüfung.
- **Verfahren und Forschung:** Wie kommen neue Ideen künftig schneller und trotzdem sauber vom Einfall zum registrierten Test? Zum Beispiel ein schlanker „Vorregistrierungs-Baukasten“, Standard-Sonden, Paper-Trading-Stufen, Abbruchregeln.
- **Betrieb und Überwachung:** Dashboard, Alarme, Live-Drift gegen Backtest, Notfallabschaltung, Übergang Paper ⇒ Live mit kleinen Beträgen.
- **Wirtschaftlichkeit des Projekts:** Aufwand gegen Ertrag, ab welchem Kapital sich was lohnt, Kosten der Werkzeuge (auch der KI-Nutzung), Zeitbedarf des Betreibers.
- **Frei:** alles, was dir darüber hinaus sinnvoll scheint, auch unbequeme Vorschläge („das hier weglassen“).

**Je Idee:**
- kurze Beschreibung;
- warum sie hier passt;
- Evidenz mit Quelle;
- erwarteter Nutzen (qualitativ: gering/mittel/hoch);
- Aufwand (in Aufträgen oder Tagen);
- Risiko und Nebenwirkung;
- ob sie **vor** oder **nach** dem signierten Tag gehört und warum;
- was als Erstes zu tun wäre.

## 6. Teil C — Priorisierung und Fahrplan

1. **Top 10** aus Teil B, begründet gereiht (Nutzen gegen Aufwand, Abhängigkeiten).
2. **Fahrplan in drei Horizonten:**
   - bis zum signierten Tag;
   - die ersten vier Wochen danach;
   - die nächsten drei Monate.
3. **Was der Betreiber selbst entscheiden muss:** als Liste mit je zwei, drei Optionen und deiner Empfehlung.

## 7. Form

- Ablage als `projektfuehrung/FABLE_ANTWORT_2026-09-25f_gesamtanalyse_und_ideen.md`. Die Buchstaben 25d und 25e bleiben für die Antworten auf die Anfragen 25d/25e reserviert.
- Gliederung wie oben (A, B, C), vorn eine **Zusammenfassung auf einer Seite**, hinten **„In einfacher Sprache“** und **„Quellen“** (alle Links).
- Kennzeichne jede Aussage als **gelesen** (mit Datei), **recherchiert** (mit Link) oder **eigene Einschätzung**.
- Wo du unsicher bist, schreib es dazu (wie bisher unter „Unsicher“).
- Länge: so ausführlich, wie es die Sache verlangt. Der Betreiber hat ausdrücklich eine umfangreiche Analyse gewünscht.

## In einfacher Sprache

Diese Anfrage bittet dich, einmal vom Einzelfall zurückzutreten. Lies alles, was im Projekt liegt. Sag ehrlich, wo das Projekt steht und was gut läuft. Sag auch, wo wir uns in Absicherung verlieren. Und bring viele neue, gut begründete Ideen, wie aus dem System etwas Tragfähiges und Profitables werden kann. Die Regeln des laufenden Auswahlverfahrens bleiben dabei unangetastet: keine Ergebniszahlen vor dem Tag, und neue Ideen kommen in einen späteren, eigenen Durchgang.
