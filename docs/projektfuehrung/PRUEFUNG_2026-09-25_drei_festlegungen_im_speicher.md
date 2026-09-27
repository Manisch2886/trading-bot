# Prüfung: Stehen die drei Festlegungen im neuen Projektspeicher?

**Geprüft:** 25.09.2026, Cloud-Lauf (geplante Erinnerung)
**Geprüft gegen:** die Speicherdateien des Projekts „Trading Bots"
(`overview.md`, `methodology-and-learnings.md`, `ways-of-working.md`,
`preferences.md`, `dashboard-roadmap.md`, `index.md`)
**Gegengelesen an:** `projektfuehrung/BACKLOG.md` und den Register-Kopien
in der Projektablage.

## Ergebnis in einem Satz

**Alle drei Festlegungen sind im neuen Speicher vorhanden** — eine
Nebenzeile ist überholt, drei Ergänzungen fehlen. Kein Verlust, der den
Export dringlicher machen würde; der Export bleibt trotzdem sinnvoll, weil
er der einzige vollständige Stand des alten Speichers ist.

---

## 1. Elliott Wave Aktien — Prüfkriterium  ✅ vorhanden

`overview.md` führt es wörtlich:

> „Elliott Wave Aktien decision: bot keeps running but under a review
> criterion — judged on portfolio drawdown contribution (does removing it
> noticeably increase combined drawdown?), not individual return"

⚠️ **Die Zeile daneben ist überholt:**

> „Elliott Wave Aktien review timeline: October quarterly review is the
> checkpoint, real judgment in January"

`BACKLOG.md`, Abschnitt 8 (gestrichen am 14.09.2026 nach Fables Prüfung),
hat den **Oktober-Prüftermin gestrichen**: ein Urteil über den Bot **vor**
dem vorregistrierten Lauf wäre eine Entscheidung ausserhalb des Registers.
Zulässig im Oktober ist nur, was keine Parameteränderung ist — der
Zufalls-Timing-Test als vorregistrierte Messung, Ergebnis ins Journal.
**Wer im Speicher nur die Zeitplan-Zeile liest, hält den Oktober-Termin für
gültig.** Die Zeile gehört nach dem Export berichtigt.

## 2. Termin des Selektionslaufs  ✅ vorhanden

`overview.md` hat einen eigenen Abschnitt:

> „Der Selektionslauf wird gestartet, **sobald die Vorarbeit steht** — der
> 13.12.2026 ist eine **Obergrenze, kein Termin**; er stammt aus der
> Reparaturfrist und sollte nur verhindern, dass die kaputte Kennzahl
> liegenbleibt"

Fehlt gegenüber `BACKLOG.md` E3: die **eigentliche Schranke ist nicht der
Dezember, sondern 2027.** Der Selektionslauf sagt, welche Bots ausscheiden
und mit welchen Parametern die übrigen laufen — nicht, ob sie Geld
verdienen. Dafür braucht es OOS-Evidenz: frühestens 30 geschlossene Trades
und sechs Monate. *„Der Dezember ist der Punkt, an dem die Grundlage
stimmt — nicht der, an dem eine Antwort vorliegt."*

## 3. Regulatorische Handelsgrenzen  ✅ vorhanden

`overview.md` hat einen eigenen Abschnitt „Regulatorische
Handelsbeschränkungen (Wohnsitz)": keine Derivate/Futures auf Binance wegen
Wohnsitz in Deutschland, Funding-Carry (`S-B2`, „Zelle 7") damit endgültig
verworfen.

Drei Ergänzungen fehlen:

- **`methodology-and-learnings.md` nennt für B2 Funding-Carry weiterhin nur
  den methodischen Grund** („requires /fapi/, earns nothing in 2022") — ohne
  das regulatorische Aus. `BACKLOG.md` K10 vermerkt ausdrücklich „nicht
  erneut vorschlagen". Wer nur diese Datei liest, kann den Kandidaten
  wieder aufmachen.
- **PRIIPs fehlt ganz:** US-domizilierte ETFs sind für EU-Privatanleger
  gesperrt, auch die gehebelten und inversen (Register 16.9 b; betrifft
  `S-B1` und `S-A2`).
- **Die Zeile „Gehebelte Produkte auf Aktien stehen ihm offen" ist ohne
  Vorbehalt:** `BACKLOG.md` K13 hält fest, dass Optionsscheine, Knock-outs
  und Faktor-Zertifikate zwar **handelbar, aber nicht registrierbar** sind
  (keine durchgehende Kurshistorie, Emittent stellt den Preis selbst,
  Spanne hat mit den 0,30 pp nichts zu tun).

---

## Was daraus folgt

Nichts davon ist verloren — alles steht in `BACKLOG.md` und in den
Register-Kopien, also in Dateien, die den Speicherwechsel überdauern. Die
vier Punkte sind **Nachträge in den neuen Speicher**, keine Rettungsarbeit,
und sie hängen nicht an der Frist vom 29.09. Der steuernde Chat trägt sie
beim nächsten Kontakt nach; dieser geplante Lauf ändert den Speicher nicht
von sich aus.
