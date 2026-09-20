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
| **TB-65** | `docs/auftraege/MAC_TB-65_benchmarkschranke_pruefen.md` | ⭐⭐ **Welche Schranke gilt für den Benchmark?** Rein lesend, entscheidet nichts — ⚠️ **blockiert das Amendment für die fünf Krypto-Bots** |
| **TB-62** | `docs/auftraege/MAC_TB-62_nachtraege_m_v.md` | Einarbeitung der Nachträge (m) und (v) — reine Dokumentation, rechnet nicht |
| **TB-63** | `docs/auftraege/MAC_TB-63_epics_auslagern.md` | Die fünf Epics nach `BACKLOG_EPICS.md` — ⚠️ **setzt TB-62 voraus**, rechnet nicht |
| **TB-64** | `docs/auftraege/MAC_TB-64_nachtragswaechter.md` | ⭐⭐ Wächter für die Bringschuld der Nachträge — **unabhängig**, fässt Backlog und Journal nicht an |

*Gesetzt 20.09.2026 (zuvor TB-60, erledigt mit `c04b348`, nachgemessen und
geschlossen mit `79742d1`). Bei jedem neuen Auftrag wird **nur diese Tabelle**
gepflegt — erledigte Zeilen werden entfernt, nicht durchgestrichen.*

### Geplant, noch nicht formuliert — die Dokumentationskette

⭐ **Betreiberentscheidung 20.09.2026:** Alle fünf Punkte der Bestandsaufnahme
werden umgesetzt, in dieser Reihenfolge. **TB-64 ist bereits formuliert und
steht oben in der Auftragstabelle.** ⚠️ **Umnummeriert am 20.09.2026, 14:40:**
Die Planungsnummern `TB-65`–`TB-67` sind zu `TB-66`–`TB-68` geworden, weil `TB-65`
an den Prüfauftrag zur Benchmark-Schranke ging — er ist dringender und blockiert
das Amendment. *Kein Auftragsdokument trug diese Nummern, gemessen; nichts bricht.*

| | Vorhaben | hängt an | Art |
|---|---|---|---|
| **TB-66** | Entdoppelung: der Eröffnungstext und *"In einfacher Sprache"* stehen je mehrfach | TB-62 | Dokumentation |
| **TB-67** | `ARBEITSWEISE.md` neu ordnen — 24 Abschnitte, sieben davon nachträglich eingeschoben (`5b`, `6b`, `6bb`, `6c`, `6d`, `7b`, `7c`) | TB-62, TB-66 | Dokumentation |
| **TB-68** | `BACKLOG.md` Abschnitt 2 aufräumen — **107 135 B**, grösster Einzelposten; Aktives und Erledigtes vermischt | TB-63 | Dokumentation, **vorsichtig** |

⚠️⚠️ **Die Aufträge werden ERST GESCHRIEBEN, WENN IHR VORGÄNGER DURCH IST.**
*Gemessen am 20.09.2026: Der TB-62-Auftrag trug eine Nummer und eine Anzahl, die
beim Schreiben richtig und eine halbe Stunde später falsch waren, weil der
Nachtrag weiterwuchs. Ein Auftrag, der auf einen Stand zeigt, der sich noch
ändert, veraltet — und sein SOLL liest die nächste Sitzung als Anweisung.*

⚠️ **Der Anlass, gemessen am 20.09.2026, 12:58:** Fünf Einarbeitungen sind
offen, und **keine davon war irgendwo als offen geführt** — Backlog-Nachträge
`(m)` und `(v)`, Journal-Nachträge `(g)`, `(20a)` und `(20b)`; `(f)` ist mit dem
verwendeten Muster **nicht prüfbar**, weil sein Titel keine TB-Nummer nennt.

---

⚠️⚠️ **VIER AUFTRÄGE — NIE ZWEI GLEICHZEITIG IM SELBEN ARBEITSBAUM.**
Alle vier schreiben nach `docs/`. Läuft eine Sitzung, warten die anderen.
⚠️ **Und TB-63 setzt TB-62 voraus** — beide ändern `BACKLOG.md`; TB-63 bricht
ab, wenn TB-62 nicht auf `origin/main` steht.
⭐ *Deshalb steht die Nummer dem Einfügesatz voran: sie wählt die Zeile aus,
und kommt sie nicht vor, bricht die Sitzung ab, statt zu raten.*

---

⚠️ **Schritt 0 gilt für jeden Auftrag, auch wenn er ihn nicht wiederholt:**
Committe, was im Arbeitsbaum liegt, bevor du anfängst. Der Nachweis
„Arbeitsbaum sauber" wird **danach** geprüft.
