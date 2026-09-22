# Aktueller Auftrag

⚠️ **Diese Datei enthält nichts als den Pfad des gerade gültigen Auftrags.**
Sie existiert, damit der Satz, den der Betreiber in eine wartende
Claude-Code-Eingabezeile einfügt, **bis auf ein einziges Zeichenpaar identisch**
ist und deshalb weder getippt noch umformuliert werden muss.

⚠️⚠️ **Vor allem anderen: Schlüsselbund entsperren.** In einem zweiten
Terminalfenster `security unlock-keychain`, Passwort an der Eingabeaufforderung
tippen. **Sonst fehlt `/remote-control`**, die Sitzung ist in App und Web
unsichtbar und läuft über „API Usage Billing" statt über das Abo.
⭐ **Kopfzeile muss „Claude Max" nennen.** Bleibt es danach bei „Not logged in",
**erst dann** `/login` (`ARBEITSWEISE.md` Abschnitt 14, Regel 0).

**Der einzufügende Satz. Nur die TB-Nummer am Anfang wechselt:**

```
TB-<Nummer>: Lies docs/auftraege/AKTUELLER_AUFTRAG.md, suche dort die Zeile mit genau der TB-Nummer, die diesem Satz vorangestellt ist, und arbeite den in dieser Zeile genannten Auftrag vollstaendig eigenstaendig ab. Antworte zuerst mit einer Zeile, welchen Auftrag du gelesen hast. Kommt deine Nummer dort nicht vor, brich ab und melde es.
```

⭐ **Warum die Nummer vorn steht und nicht im Auftrag allein:** Der Betreiber
führt mehrere Sitzungen parallel und muss sie **in der Historie**
auseinanderhalten. `ARBEITSWEISE.md` verlangt den Sitzungstitel seit dem
15.09.2026 — **bisher aber nur im Dateikopf des Aufgabendokuments**, und der
erreicht die Sitzungsliste nicht. Vorangestellt steht die Nummer an der Stelle,
an der sie am schwersten verlorengeht und am leichtesten zu ändern ist.

⭐⭐ **Und der letzte Satz macht aus dem Titel eine Wache:** Wurde diese Datei
nicht umgestellt, nennt sie eine andere Nummer als die vorangestellte — **dann
bricht die Sitzung ab, statt den falschen Auftrag abzuarbeiten.** *Der häufigste
Fehler bei einem Zeiger ist ein Zeiger, den jemand zu aktualisieren vergisst.*

---

## Gültiger Auftrag

| TB | Auftragsdokument | kurz |
|---|---|---|
| **TB-87** | `docs/auftraege/MAC_TB-87_register_37.md` | ⭐⭐ **Registerabschnitt 37 — Stufe I, Punkt 4 aus `PLAN_VOR_DEM_TAG.md`.** Fuenf Eintraege aus Fables 22d und 22g, ⛔ **nur Text, keine neue Freigabe noetig.** Die Sonde meldet kuenftig **je Punkt je Bestandteil** (37.1) · das Abbild fuehrt **zwei Gruppen**, Punkte und „bestimmte" Pfade (37.2) · ⭐⭐ **was ein Befund `1` bedeutet, haengt vom Tag ab** — davor planmaessig mit Tatsachennotiz und neuem Abbild, danach Sperrlistenbruch nach 10.1 (37.3, schliesst die Luecke, die TB-86 sichtbar gemacht hat) · Tatsachennotiz zu den zwei Listen in `herkunft.py` (37.4) · **„Ort registrierter Werte"** — jeder registrierte Zahlenwert bekommt genau ein Modul und eine Konstante (37.5). ⛔ **Keine `.py` aendern**, kein neues Abbild, keine Sonde anpassen, keine Werte verschieben. Drei Hashes vorher UND nachher |

*Gesetzt 22.09.2026 (zuvor TB-86, erledigt mit `ee4e65c`, 22.09.2026; davor
TB-85 `755b3c4`, TB-84 `03e544e`, TB-83 `fdb181a`, TB-82 `f1a0dc7`, TB-81 `6071f32`). Bei jedem neuen Auftrag wird **nur diese Tabelle**
gepflegt — erledigte Zeilen werden entfernt, nicht durchgestrichen.*

### Geplant, noch nicht formuliert — die Dokumentationskette

⭐ **Betreiberentscheidung 20.09.2026:** Alle fünf Punkte der Bestandsaufnahme
werden umgesetzt, in dieser Reihenfolge. **TB-64 ist bereits formuliert und
steht oben in der Auftragstabelle.** ⚠️ **Dreimal umnummeriert (14:40, 15:30, 15:55):**
Die Planungsnummern sind jetzt `TB-68`–`TB-70`. `TB-65` ging an den Prüfauftrag
zur Benchmark-Schranke, `TB-66` an die Umsetzung von Fables Festlegung — beide stehen vor dem Tag —
und `TB-67` an die Journal-Einarbeitung, die TB-62 als Rueckstand aufgedeckt hat. *Kein Auftragsdokument trug die verschobenen Nummern,
gemessen; nichts bricht.*

| | Vorhaben | hängt an | Art |
|---|---|---|---|
| **TB-70** | `BACKLOG.md` Abschnitt 2 aufräumen — **107 135 B**, grösster Einzelposten; Aktives und Erledigtes vermischt | TB-63 | Dokumentation, **vorsichtig** |

⚠️⚠️ **Die Aufträge werden ERST GESCHRIEBEN, WENN IHR VORGÄNGER DURCH IST.**
*Gemessen am 20.09.2026: Der TB-62-Auftrag trug eine Nummer und eine Anzahl, die
beim Schreiben richtig und eine halbe Stunde später falsch waren, weil der
Nachtrag weiterwuchs. Ein Auftrag, der auf einen Stand zeigt, der sich noch
ändert, veraltet — und sein SOLL liest die nächste Sitzung als Anweisung.*

⚠️ **Der Anlass, gemessen am 20.09.2026, 12:58:** Fünf Einarbeitungen waren
offen, und **keine davon war irgendwo als offen geführt**. ⭐ **Erledigt durch
TB-67 (`a15746f`):** elf Journal-Nachträge gemessen, acht eingearbeitet (Blöcke
`BK`–`BT`), Quellenzeile eingeführt, alle elf nach `nachtraege/_eingearbeitet/`
verschoben. ⚠️ **Offen bleiben die Backlog-Nachträge** — das ist `TB-64`,
Prüfung B; `(m)` hängt zusätzlich an der Betreiberentscheidung zu seinen sieben
`B`-Zeilen (TB-67, Nachweis 6).

---

⚠️⚠️ **NIE ZWEI AUFTRÄGE GLEICHZEITIG IM SELBEN ARBEITSBAUM.**
Läuft eine Sitzung, warten die anderen. *(Hier stand bis 21.09.2026 „DREI
AUFTRÄGE" mit der Abhängigkeit TB-63 → TB-62 über `BACKLOG.md`; beide sind
erledigt (`437428d`, `6e29eec`), der Satz war überholt und ist nach
`DOKUMENTATIONSSTANDARD.md` Abschnitt 9 entfernt statt danebengestellt.)*
⭐ *Deshalb steht die Nummer dem Einfügesatz voran: sie wählt die Zeile aus,
und kommt sie nicht vor, bricht die Sitzung ab, statt zu raten.*

---

⚠️ **Schritt 0 gilt für jeden Auftrag, auch wenn er ihn nicht wiederholt:**
Committe, was im Arbeitsbaum liegt, bevor du anfängst. Der Nachweis
„Arbeitsbaum sauber" wird **danach** geprüft.
