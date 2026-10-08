# TB-141 Regelwerk-Nachtrag 06.–08.10.2026 — 38 Regeln aus dem Bestand, fünf Regeln aus dem Umzug 07.10.2026, 23:39, Entscheide und Vorgaben W1–W8; Abnahme TB-139 in BACKLOG und Journal — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 08.10.2026,** gebaut vom Helfer BAU141 ausserhalb des Repos (Entscheid W1), nur lesend am Repo (HEAD `d4a28e9`), alle Schritte an Kopien simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht (W1).

**Sitzungstitel:** `TB-141` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main`, frisch von `main` am HEAD `d4a28e91f359cdd7fba4baa62f0ba1f8d430badb` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Angelegt:** 08.10.2026 vom steuernden Chat
**Vorgänger:** TB-139 (`d4a28e9`). **Dieser Auftrag:** `docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md`, er wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.

**Bauart wie TB-133** (`docs/auftraege/MAC_TB-133_regelwerk_nachtrag_umzug_sitzung_bruecke.md`, erledigt mit `0c70853`): Verfahren je Einfügung, Schritt 0, Nachweis und Abgabe gelten wie dort, mit den Werten von hier; wo beide sich widersprechen, gilt dieser Auftrag. **Anders als TB-133:** (1) Die Sitzung leitet keine Skripte aus Vorlagen ab. **Ein** Skript steht in Anhang A (`tb141_einfuegen.py`); es liest Einfügungen, Prüfanker, J1 und Sollwerte aus diesem Auftrag. (2) Neben den Einfügungen E1–E26 stehen die Prüfungen S1–S4: Regeln, die im Regelwerk schon stehen; dort wird nur der Verweis gezählt. (3) Der Journalblock trägt den Absatz J1 wie in TB-139 (dort „Schritt B, zweiter Teil“). (4) Die Anmerkungen (1) bis (3) der Abnahme TB-139 sind hier Vorgabe: Rohausgaben von git bleiben roh, ihre Beschreibung steht in einer Begleitdatei; jede Belegdatei des Skripts trägt eine Kopfzeile, wird ganz neu geschrieben und zurückgelesen; das Ergebnis nennt jede Abweichung vom Auftrag.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei** (Betreiberentscheid 26.09.2026; so auch TB-127, TB-128, TB-131 und TB-133). **Keine Zieldatei steht auf der Sperrliste** — gemessen am HEAD `d4a28e9`: Register `docs/VORREGISTRIERUNG_neuselektion.md` Abschnitt 10 „Die Sperrliste“ (Z. 971–1177, bis vor die nächste Überschrift zweiter Ebene in Z. 1178) und die Tabelle „Die Sperrliste, Stand 18.09.2026“ in `ARBEITSWEISE.md` Abschnitt 7 (Z. 1100–1109; sie nennt sechs Muster unter `strategies/` und `shared/`) enthalten die Wörter `projektfuehrung`, `ARBEITSWEISE`, `BACKLOG`, `JOURNAL` und `docs/` je 0-mal. Das Skript misst das in 0c noch einmal (Sperrlisten-Wache).

Was dieser Auftrag einträgt, haben entschieden: der **Betreiber** — am 07.10.2026, 19:44: „Ich fand deine selbstständige Arbeitsweise heute super und möchte das du zukünftig immer so arbeitest!“ (U1); per Karte am 07.10.2026, 22:44: „Ja, ab 20 KB als Datei (Empfohlen)“ (W3); per Karte, gestellt 08.10.2026, 00:34: „Helfer bauen Entwürfe (Empfohlen)“ (W1), „Nur wörtlicher Auszug (Empfohlen)“ (W2), „Wichtiges ja, Form als Hinweis (Empfohlen)“ (W7) — und der **steuernde Chat** mit den Vorgaben W4, W5, W6 und W8 (Antwort 08.10.2026, 00:33; sie gelten, da nicht widersprochen). Die übrigen Regeln sind Folgerungen des steuernden Chats aus eigenen Fehlern (⇒ in der Übergabe) oder Lesarten, als solche gekennzeichnet.

Geändert werden nur: `docs/projektfuehrung/ARBEITSWEISE.md`, `docs/projektfuehrung/BACKLOG.md`, `docs/projektfuehrung/JOURNAL.md`, dazu Belege unter `docs/belege/TB-141/` und das Ergebnis.

⛔ **Nicht erlaubt, mit Grund:**
- Den vorgegebenen Text umformulieren, kürzen, glätten oder zusammenlegen. *Grund:* Die Wortlaute kommen per Skript aus den Quellen und sind gegengelesen; die Sitzung trägt sie ein (5b). Findet die Sitzung einen Sachfehler: melden, nicht berichtigen.
- Register, `docs/VORREGISTRIERUNG_*`, `research/`, `shared/`, `strategies/`, jede Sperrlisten-Datei, jedes Werkzeug unter `docs/werkzeuge/`. *Grund:* nicht Gegenstand.
- `UEBERGABE.md`, `UEBERGABE_ARCHIV.md`, `UMZUG.md`, die `FABLE_*`-Dateien, `REGISTER_INDEX.md` und die Registerkopie ändern. *Grund:* Übergabe und `FABLE_*` sind die Quellen; `UMZUG.md` bleibt, wie es ist (W4 lässt die Regel vom 05.10.2026, 23:58, unverändert gelten); Index und Kopie gehören zum Register.
- Bestehende Zeilen in `ARBEITSWEISE.md`, `BACKLOG.md` und `JOURNAL.md` ändern oder entfernen. *Grund:* Dieser Auftrag fügt nur ein; es gibt **keine** Ersetzung. Wo eine neue Zeile einer alten vorgeht, sagt sie es selbst (E7, E25).

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt (auch `UEBERGABE.md` und `AKTUELLER_AUFTRAG.md`); das ist kein Ändern im Sinn der Verbote und des Abbruchkriteriums.

**Sichtschutz:** entfällt, es werden keine Ergebnisse gelesen.

## Belegt · erschlossen · offen

- **Belegt:** Die Regeln U1–U38 stehen mit Wortlaut, Fundstelle und Einstufung (S steht schon · E zu ergänzen · N neu) im Bestand `logs/steuernder_chat/TB-141_bestand_REGELN.md` (29 249 B, md5 `1ce37cfe7f3296866fa6664d79699ad5`), gegengeprüft in `logs/steuernder_chat/TB-141_KARTE_W_bericht.md` (beide von git ignoriert, nicht Gegenstand dieses Auftrags). Die Quellen in `docs/projektfuehrung/UEBERGABE.md`: Umzüge 06.10.2026, 07:08, 13:43 und 16:40; 07.10.2026, 06:59, 19:45 (mit Zusatz 19:46) und 23:39, je Block 7; Nachträge 06.10.2026, 14:25 und 21:00; 07.10.2026, 10:32, Abschnitt 8. **Jeder als wörtlich übernommene Teil (98) und jede Anführung (38) in E1–E26 ist per Skript an der Quelle geprüft** (Leerraum normalisiert) (Übergabe im Arbeitsbaum vom 08.10.2026, 354 645 B, md5 `1ee81aa1550268047e6762ed7b2596bc`; `ARBEITSWEISE.md` und `UMZUG.md` am HEAD; Text des steuernden Chats zu W1–W8 und zur Abnahme TB-139, Stand 08.10.2026, 06:55). Die Spiegelstriche zu Abnahme, Fehlern und Reihenfolge in E26 und J1 setzt das Bauskript zeichengleich aus diesem Text ein, mit `assert` auf jede Ausgangszeile. **Nicht aus Übergabe, Regelwerk oder Baustein:** der Halbsatz „was auch ortsunabhängig ginge, ist ortsunabhängig“ in E4 ist Wortlaut der Projekt-Erinnerung (19.09.2026, auf Bitte des Betreibers gemerkt); die Quellenprüfung findet ihn dort nicht.
- **Vorzählung** (Helfer BAU141, 08.10.2026, Python `str.count` an Kopien `git show HEAD:<pfad>`): jeder Anker genau 1, jeder Prüfanker genau 1, die erste Zeile jedes neuen Texts 0-mal, kein Anker und kein Prüfanker in einem neuen Text. `ARBEITSWEISE.md` 2 413 Zeilen, md5 `e85163e98db7f0b9387f4c990b67f8ca`; `BACKLOG.md` 349 Zeilen, md5 `583b4049aca0bd9e9aa12c97580c21c5`; `JOURNAL.md` 10 528 Zeilen, md5 `1eb65c7e9fbc378b8713fef7af4e1160`, letzte Kennung EI. **Simulation:** alle Schritte mit dem Skript aus Anhang A in einem Git-Verzeichnis ausserhalb des Repos (Kopien am HEAD): Probe, Einfügen, numstat, Vergleich, Journalblock mit Platzhalterblock, J1, J1-Vergleich — alle rc 0, Werte wie unten. Die Sitzung zählt selbst nach; ihre Zahl gilt.
- **Erschlossen:** „E — zu ergänzen“ setzt dieser Auftrag als **neue Zeile** an dem Ort um, den der Bestand vorschlägt; die bestehende Zeile bleibt unverändert (Bauart TB-133: nur einfügen). Abschnitt 0 bekommt Checklistenzeilen mit Zeiger; die Begründung steht im Abschnitt, auf den sie zeigt (13, 15, 22.5, 22.10) oder, bei Folgerungen aus Fehlern, in der Übergabe (wie TB-133). Eine eigene Gruppe für Helfer bekommt Abschnitt 0 nicht.
- **Offen:** Die Entscheide W1, W2 und W7 des Betreibers, die Vorgaben W4, W5, W6 und W8 des steuernden Chats und die Abnahme TB-139 stehen beim Bau nur im Text des steuernden Chats, noch nicht in `UEBERGABE.md` (Arbeitsbaum endet mit dem Umzug 07.10.2026, 23:39); der steuernde Chat trägt sie vor dem Start nach, Schritt 0 committet sie mit. W3 steht schon dort (Nachtrag 07.10.2026, 22:45, und Umzug 07.10.2026, 23:39, Block 6).

## Zuordnung — jede Regel und wo sie eingetragen wird

Bestand: S = steht schon (nur Prüfung S1–S4) · E = zu ergänzen · N = neu. „B7.n“ = Block 7 des Umzugs 07.10.2026, 23:39, Nr. n. Wo ein Entscheid eine Regel anders fasst als der Bestand, gilt der Entscheid; die letzte Spalte nennt die Stelle.

| Regel | Bestand | eingetragen in | Entscheid ändert den Bestand |
|---|---|---|---|
| U1 | N | E3, E21 | — |
| U2 | E | E20, E25 | W1: Helfer bauen Entwürfe ausserhalb des Repos, Urteil und Freigabe beim steuernden Chat (statt „Grosses bauen und prüfen Helfer … holt nur Kurzberichte“) |
| U3 | S | S1 | — |
| U4 | E | E5 | — |
| U5 | E | E5 | — |
| U6 | E | E6 | — |
| U7 | N | E4 | — |
| U8 | S | E15, E24, S2 | W5: beide Zeilen gelten, Klarstellung neben der Zeile „Nach dem Auslöser“ und in 22.5 |
| U9 | E | E20 | — |
| U10 | E | E20 | — |
| U11 | E | E20 | — |
| U12 | E | E20 | — |
| U13 | E | E2 | — |
| U14 | E | E2 | — |
| U15 | E | E17 | — |
| U16 | E | E20, E25 | W6: T1 bleibt; was in Registertext oder eine Vorgabe geht, an der Tabelle des Berichts |
| U17 | N | E11 | — |
| U18 | E | E10 | — |
| U19 | N | E14 | — |
| U20 | E | E20 | — |
| U21 | N | E18 | — |
| U22 | N | E20, E25 | W2: nur wörtlicher Auszug mit Zeile, F1 bleibt für Registertext (statt „kürzen lassen“) |
| U23 | E | E20 | — |
| U24 | N | E12 | — |
| U25 | N | E11 | — |
| U26 | N | E8 | — |
| U27 | N | E9 | — |
| U28 | N | E8, E25 | W4: ein frischer Helfer baut, ein zweiter liest gegen; frischer Chat nur nach dem Ja zum Umzug (statt „ein frischer Chat“); W3: ab rund 20 KB die Datei |
| U29 | N | E20, E25 | — |
| U30 | N | E7, E23 | W3: ab rund 20 KB als Datei — die Frage an den Betreiber entfällt |
| U31 | N | E20, E25 | W7: eingearbeitet wird, was Messung, Sollwert, Fundstelle oder Registertext ändert; Formlücken als Hinweis, dem Betreiber genannt (statt „Lücken, die keine Messung ändern“) |
| U32 | N | E19 | — |
| U33 | N | E1 | — |
| U34 | E | E13, E22 | W8: ohne die Bedingung „Ist der Betreiber unterwegs“; Zusatz zu den Sätzen „kein Haltepunkt“ |
| U35 | E | E16 | — |
| U36 | E | E20 | — |
| U37 | S | S3 | — |
| U38 | S | S4 | — |
| B7.1 — Messungen bündeln, Helfer parallel, eine Nachmessung | Umzug 07.10.2026, 23:39, Block 7 Nr. 1 | E3 | — |
| B7.2 — Tabelle des Berichts statt Kurzantwort (mit W6) | Umzug 07.10.2026, 23:39, Block 7 Nr. 2 | E20 | — |
| B7.3 — bei Widerspruch zweier Helfer selbst messen | Umzug 07.10.2026, 23:39, Block 7 Nr. 3 | E19 | — |
| B7.4 — Bauläufe über die Brücke in Einzelschritten | Umzug 07.10.2026, 23:39, Block 7 Nr. 4 | E14 | — |
| B7.5 — vor einem Helferstart den Zielordner prüfen | Umzug 07.10.2026, 23:39, Block 7 Nr. 5 | E20 | — |
| W1 | Betreiber, Karte | E20, E25 | — |
| W2 | Betreiber, Karte | E20, E25 | — |
| W3 | Betreiber, Karte | E7, E23 | — |
| W4 | Vorgabe des steuernden Chats | E8, E25 | — |
| W5 | Vorgabe des steuernden Chats | E15, E24 | — |
| W6 | Vorgabe des steuernden Chats | E20, E25 | — |
| W7 | Betreiber, Karte | E20, E25 | — |
| W8 | Vorgabe des steuernden Chats | E13, E22 | — |

## Verfahren je Einfügung (E1–E26) und je Prüfung (S1–S4)

*Vorgezählt wie unter „Belegt“. Die Sitzung zählt selbst nach; ihre Zahl gilt.*

1. **Werkzeug:** `docs/belege/TB-141/tb141_einfuegen.py` aus Anhang A (in 0a ausgelesen, sha256 geprüft). Es liest je Einfügung Zieldatei (Zeile `Zieldatei:`), Anker, Art, Form und Text (Codeblock ohne Zäune) aus **diesem Auftrag**, je Prüfung die Zeilen `Prüfanker:`, dazu J1 und den Block „Sollwerte“ — nicht aus dem Gedächtnis. Überschriften zählt es nur ausserhalb von Codeblöcken (der Codeblock von E26 trägt eine Zeile mit `### `).
2. **Vorher:** Anker zählen, **Soll genau 1**; erste Zeile des neuen Texts, **Soll 0**. Weicht eins ab: diese Einfügung nicht ausführen, vermerken, weitermachen (kein Abbruch; das Skript tut genau das und endet mit rc 1).
3. **Ausführen** wie unter „Art“ („nach der Zeile“/„vor der Zeile“ bezieht sich auf die ganze Zeile mit dem Anker). **Form Zeilen:** ohne Leerzeilen (Tabellenzeilen; bei E22 vier Zeilen Fliesstext, die den Absatz davor fortsetzen). **Form Block:** genau eine Leerzeile davor und danach, eine vorhandene wird nicht verdoppelt.
4. **Nachher:** erste Zeile des neuen Texts, **Soll genau 1**. Prüfanker S1–S4 vorher und nachher **genau 1**.
5. Alle Einfügungen einer Datei rechnet das Skript im Speicher und schreibt jede Datei einmal; Belegdateien schreibt es ganz neu, mit Kopfzeile, und liest sie zurück.

Zeilenbilanz je Einfügung (gerechnet am HEAD, unabhängig vom Skript; in der Simulation vom Skript bestätigt):

| E | Zieldatei | Ort | Ankerzeile am HEAD | Zeilen + |
|---|---|---|---|---|
| E1 | `ARBEITSWEISE.md` | Abschnitt 0, „Immer“ | 42 | 1 |
| E2 | `ARBEITSWEISE.md` | Abschnitt 0, „Immer“ | 43 | 2 |
| E3 | `ARBEITSWEISE.md` | Abschnitt 0, „Immer“ | 51 | 2 |
| E4 | `ARBEITSWEISE.md` | Abschnitt 0, „Am Ende jeder Antwort“ | 64 | 1 |
| E5 | `ARBEITSWEISE.md` | Abschnitt 0, „Am Ende jeder Antwort“ | 66 | 2 |
| E6 | `ARBEITSWEISE.md` | Abschnitt 0, „Am Ende jeder Antwort“ | 67 | 1 |
| E7 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ein Dokument mitgeht“ | 79 | 1 |
| E8 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ein Dokument mitgeht“ | 83 | 2 |
| E9 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ein Dokument mitgeht“ | 85 | 1 |
| E10 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ein Arbeitsabschnitt endet“ | 97 | 1 |
| E11 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ein Arbeitsabschnitt endet“ | 98 | 2 |
| E12 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“ | 104 | 1 |
| E13 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“ | 110 | 1 |
| E14 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn Terminalbefehle drin sind“ | 135 | 2 |
| E15 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn eine Mac-Sitzung startet“ | 151 | 1 |
| E16 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn eine Mac-Sitzung startet“ | 155 | 1 |
| E17 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn Dateien abgelegt … werden“ | 171 | 1 |
| E18 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn Dateien abgelegt … werden“ | 176 | 1 |
| E19 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ich ein fremdes Ergebnis bewerte“ | 188 | 2 |
| E20 | `ARBEITSWEISE.md` | Abschnitt 0, „Wenn ich einen Auftrag schreibe“ | 226 | 13 |
| E21 | `ARBEITSWEISE.md` | Abschnitt 13 | 1317 | 2 |
| E22 | `ARBEITSWEISE.md` | Abschnitt 13 | 1339 | 5 |
| E23 | `ARBEITSWEISE.md` | Abschnitt 15, Austausch mit dem Verfahrensprüfer | 1721 | 1 |
| E24 | `ARBEITSWEISE.md` | Abschnitt 22.5 | 2084 | 2 |
| E25 | `ARBEITSWEISE.md` | Abschnitt 22.10 | 2263 | 9 |
| E26 | `BACKLOG.md` | BACKLOG, Abschnitt 5 | 338 | 13 |
| **Summe** | | `ARBEITSWEISE.md` **58** · `BACKLOG.md` **13** | | 71 |

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-141/` entsteht:** `git status --porcelain > "$TMPDIR/tb141_0a.txt"` und `git rev-parse HEAD`. Soll: genau die drei Einträge unten (Reihenfolge egal) und HEAD `d4a28e91f359cdd7fba4baa62f0ba1f8d430badb`. Weicht etwas ab ⇒ Abbruch. `docs/belege/TB-141/` gibt es noch nicht.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md
```

Dann das Skript aus Anhang A auslesen, mit genau diesem Aufruf:

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
i = z.index("### Einfügeskript")
a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
t = "\n".join(z[a + 1:b]) + "\n"
open(sys.argv[2] + "/tb141_einfuegen.py", "w", encoding="utf-8").write(t)
print("tb141_einfuegen.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb141_einfuegen.py 1af78b614412a698a30658e2d556390ca802bd1fb3e7218b47d23903d2445d6c`. Weicht er ab ⇒ Abbruch.

Commit `TB-141 Schritt 0: Stand des steuernden Chats 08.10.2026` mit genau den drei Pfaden aus 0a (mit Namen hinzufügen, nicht mit `git add -A`), pushen. Der Commit heisst im Folgenden **⟨S0⟩** (7 Zeichen). Erst jetzt:
- `$TMPDIR/tb141_0a.txt` **unverändert** nach `docs/belege/TB-141/0a_status.txt` kopieren (`cmp` gleich) — Rohausgabe, ohne Kopfzeile;
- `docs/belege/TB-141/0a_status.kopf.txt` mit genau einer Zeile: `# TB-141 0a — git status --porcelain vor ⟨S0⟩ am HEAD d4a28e9, Rohausgabe in 0a_status.txt: <Bytes> B, <Zeilen> Zeilen, md5 <md5>`;
- `$TMPDIR/tb141_einfuegen.py` nach `docs/belege/TB-141/tb141_einfuegen.py` (sha256 danach noch einmal, Soll wie oben).

**0b. Ausgang** ⇒ `docs/belege/TB-141/0b_ausgang.txt`: erste Zeile `# TB-141 0b — Ausgang der Zieldateien an ⟨S0⟩ (sha256 · md5 · Zeilen)`, danach je Zieldatei (`ARBEITSWEISE.md`, `BACKLOG.md`, `JOURNAL.md`) eine Zeile. Soll: md5 und Zeilen wie unter „Belegt“ (sha256 nur messen). Weicht eine Datei ab ⇒ ihre Einfügungen trotzdem nach dem Verfahren (der Anker entscheidet), die Abweichung vermerken, kein Abbruch.

**0c. Probe:** `trading-env/bin/python3 -B docs/belege/TB-141/tb141_einfuegen.py probe; echo "rc $?"` ⇒ `docs/belege/TB-141/a_probe.txt`. Soll: rc 0; 26 Zeilen `E<n> · … · Anker vorher 1 · … · erste Textzeile schon 0 · Anker in neuen Texten 0 · ok` (Ankerzeilen am HEAD in der Zeilenbilanz oben); 10 Zeilen `S<n> · … · 1 · ok` (S1 1, S2 1, S3 5, S4 3 Prüfanker); fünf Zeilen `Sperrliste · … 0 · … 0`; Schlusszeile `Einfügungen 26 · Prüfungen 4 · Sperrliste Treffer 0 · Gesamt: wie Soll`. **Sperrliste Treffer ≠ 0 ⇒ Abbruch.** Jede andere Abweichung: weiter mit Schritt A (das Skript lässt die betroffene Einfügung aus), im Ergebnis nennen.

## Schritt A — Die Einfügungen

`trading-env/bin/python3 -B docs/belege/TB-141/tb141_einfuegen.py einfuegen; echo "rc $?"` ⇒ `docs/belege/TB-141/a_einfuegungen.txt`. Soll: rc 0; 26 Zeilen `E<n> · <Datei> · Anker vorher 1 · ausgeführt ja · Text nachher 1 · Zeilen +<k>` mit k aus der Zeilenbilanz; `Datei docs/projektfuehrung/ARBEITSWEISE.md · Zeilen vorher 2413 · nachher 2471`; `Datei docs/projektfuehrung/BACKLOG.md · Zeilen vorher 349 · nachher 362`; Schlusszeile `Gesamt: alle ausgeführt, je genau einmal`. rc 2 heisst: nichts geschrieben (Sperrliste getroffen oder alles stand schon) — dann Abbruch mit Meldung.

Commit `TB-141 A: Einfügungen E1–E26 (ARBEITSWEISE, BACKLOG)`, pushen — mit `0a_status.txt`, `0a_status.kopf.txt`, `0b_ausgang.txt`, `tb141_einfuegen.py`, `a_probe.txt` und `a_einfuegungen.txt`.

#### E1 — Abschnitt 0, „Immer“: vor einer Folgerung die Stelle lesen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Fundstellen nur, wenn sie vor mir liegen; sonst steht` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Vor einer Folgerung die Stelle lesen, die sie regelt (07.10.2026, Nachtrag 15:59: die Stelle war die Eröffnung, R56 (d)) | UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 5 |
```

#### E2 — Abschnitt 0, „Immer“: Uhrzeit über die Geräteanbindung, Helferläufe

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `im selben Schritt, in dem sie in einen Text gehen — nie schätzen` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Über die Geräteanbindung: `date` liefert dort UTC ⇒ `TZ=Europe/Berlin date` (07.10.2026) | UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 7 |
| ☐ | Für Helferläufe Anfang und Ende messen oder die Spanne zwischen zwei Messungen nennen (06.10.2026: geschätzte Uhrzeit („13:24–13:31“) im Nachtrag 13:33) | UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 1 |
```

#### E3 — Abschnitt 0, „Immer“: selbstständig arbeiten (Betreiber „zukünftig“), Messungen bündeln

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Was der Betreiber abgeschickt hat, wird nicht behauptet` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | ⭐⭐ Selbstständig arbeiten, zukünftig immer (Betreiber 07.10.2026, 19:44: „Ich fand deine selbstständige Arbeitsweise heute super und möchte das du zukünftig immer so arbeitest!“); was „so“ heisst, steht als Lesart des steuernden Chats, vorläufig, in 13 | 13; UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46 |
| ☐ | Messungen bündeln (ein Aufruf, mehrere Fragen); Helfer parallel starten; nach jedem Helferbericht nur eine Nachmessung (07.10.2026: Teuer war die Zahl der eigenen Schritte (69)) | UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 1 |
```

#### E4 — Abschnitt 0, „Am Ende jeder Antwort“: Kennzeichnung der Aufgaben

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Abgesetzter Block „Deine Aufgaben": nummeriert` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Jede Aufgabe an den Betreiber trägt die Kennzeichnung [ortsunabhängig] / [Mac-pflichtig]; was auch ortsunabhängig ginge, ist ortsunabhängig (Erinnerung, 19.09.2026; am 07.10.2026 versäumt: „Beides gilt weiter.“) | UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46 |
```

#### E5 — Abschnitt 0, „Am Ende jeder Antwort“: kein Startzeichen, Zwischenmeldungen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Kein Stillstand: der nächste Handwerksschritt ist getan` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Nach jedem Schritt folgt ohne Startzeichen der nächste, auch über mehrere Aufträge und während eine Mac-Sitzung läuft; die Grenzen bleiben: nach Schritt 0 nichts im Arbeitsbaum anfassen (Gruppe „Wenn ich einen Auftrag schreibe“), kein Umzug, während eine Sitzung läuft (10) (Lesart des steuernden Chats, vorläufig, zum Betreibersatz vom 07.10.2026, 19:44) | 13; UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46 |
| ☐ | Zwischenmeldungen mit Ergebnis statt Rückfragen (Lesart des steuernden Chats, vorläufig, zum Betreibersatz vom 07.10.2026, 19:44) | 13; UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46 |
```

#### E6 — Abschnitt 0, „Am Ende jeder Antwort“: Aufgaben nur, wo seine Hand nötig ist

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Die Aufgabenliste so kurz wie möglich` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Aufgaben an den Betreiber nur, wo seine Hand nötig ist (Lesart des steuernden Chats, vorläufig, zum Betreibersatz vom 07.10.2026, 19:44) | 13; UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46 |
```

#### E7 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Fable-Anfrage ab rund 20 KB als Datei (W3)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Fable-Anfrage: Steht ihr voller Text als Kopierblock in DIESER Antwort?` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | ⭐ Eine Fable-Anfrage ab rund 20 KB geht als Datei in den Chat, der Betreiber lädt sie im Fable-Chat hoch; kürzere bleiben Kopierblock. Diese Zeile geht der Zeile darüber und der Ausnahme in der ersten Zeile dieser Gruppe vor (Betreiber, Karte 07.10.2026, 22:44: „Ja, ab 20 KB als Datei (Empfohlen)“; 07.10.2026: Kopierblock von 34 882 B einmal gelesen und einmal ausgegeben) | 15, Austausch Nr. 5a |
```

#### E8 — Abschnitt 0, „Wenn ein Dokument mitgeht“: wer eine Fable-Anfrage baut (W4), Datum der Anfrage

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Dokumente für Fable legt der steuernde Chat selbst ab, in Projektablage und Repo, ohne Aufgabe an den Betreiber` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Eine Fable-Anfrage baut ein frischer Helfer (Vorprüfung und Entwurf), ein zweiter liest gegen. Ein frischer Chat nur nach dem Ja des Betreibers zum Umzug (Regel 05.10.2026, 23:58, geht vor); der Kopierblock kommt aus einer Datei, die ein Skript gebaut hat, und wird nur einmal in den Chat geholt — ab rund 20 KB geht die Datei selbst (Zeile „ab rund 20 KB“ oben) (Vorgabe W4, 08.10.2026; 06.10.2026: Rund 82 000 kostete die Fable-Anfrage) | 22.10; UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 5 |
| ☐ | Beim Ausgeben einer Anfrage spät am Tag den Betreiber fragen, wann er sendet, oder das Datum offen lassen (06.10.2026: wann der Betreiber sie abgeschickt hat, ist nicht gemessen) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 3 |
```

#### E9 — Abschnitt 0, „Wenn ein Dokument mitgeht“: Zeilenlängen nach dem Ersetzen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `als Nachtrag (neue Blöcke, benannte Ersetzungen mit Stelle), nie ganz neu` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Nach dem Ersetzen in umbrochenem Text die Zeilenlängen prüfen (06.10.2026: die Eröffnung trägt zwei unschöne Zeilenumbrüche) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 4 |
```

#### E10 — Abschnitt 0, „Wenn ein Arbeitsabschnitt endet“: Zeitpunkt der Umzugskarte

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Umgezogen wird nur, wenn der Betreiber es sagt oder genehmigt. Der steuernde Chat zieht nicht von sich aus um` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Die Karte zum Umzug kommt vor dem grossen Block statt danach und vor dem Warten statt danach (06.10.2026, so getragen) | UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 4; UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 5 |
```

#### E11 — Abschnitt 0, „Wenn ein Arbeitsabschnitt endet“: überholter Eröffnungstext, Arbeitsstände

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Beim Umzug: der Eröffnungstext als ERSTE Nachricht im laufenden Chat` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Arbeitet ein Chat nach dem Eröffnungstext weiter, kennzeichnet er den alten Text in derselben Antwort als überholt und gibt beim Umzug einen neuen aus (06.10.2026: Der Eröffnungstext von 16:41 lag drei Stunden im Chat) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 2 |
| ☐ | Arbeitsstände sofort nach `logs/steuernder_chat/`; der Ordner ist von git ignoriert und zählt nicht als Träger nach 10 Nr. 2 (06.10.2026, so getragen; Lesart des steuernden Chats, vorläufig, zum Träger) | UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 4 |
```

#### E12 — Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“: Vorgabe zur Reihenfolge

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Karte nur für echte Betreiberentscheide: Freigaben` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Vor einer Vorgabe zur Reihenfolge das Vorbild im Register messen lassen (06.10.2026, 20:19: die Vorgabe „als Nächstes der Registereintrag“ stand vor der Messung) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 1; UEBERGABE, Nachtrag 06.10.2026, 21:00 |
```

#### E13 — Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“: Zusatz zur offenen Karte (W8)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Die Frage ist kein Haltepunkt — die Arbeit läuft daneben weiter` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Zusatz zur Zeile darüber (W8): Eine offene Karte hält den Chat technisch an — vor der Karte wird alles Unabhängige angestossen, auch langlaufende Helfer (Vorgabe 08.10.2026; 07.10.2026: Die Karte stand von 11:37 bis 14:55 offen; solange arbeitet der Chat nicht.) | 13; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 6 |
```

#### E14 — Abschnitt 0, „Wenn Terminalbefehle drin sind“: Ausgaben begrenzen, Bauläufe in Einzelschritten

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Über die Geräteanbindung auch kein` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Jede `ls`- und `grep`-Ausgabe mit `head` begrenzen (06.10.2026: zwei Werkzeugausgaben ohne Grenze) | UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 1; UEBERGABE, Nachtrag 06.10.2026, 14:25 |
| ☐ | Bauläufe über die Brücke in Einzelschritten, nichts im Hintergrund, kein Aufruf über 150 s (07.10.2026: die Geräteanbindung fiel 21:31 weg, während ein Helfer einen langen Bau im Hintergrund laufen liess) | UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 4 |
```

#### E15 — Abschnitt 0, „Wenn eine Mac-Sitzung startet“: Klarstellung Nachschau (W5)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Nach dem Auslöser: Ist Schritt 0 committet?` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Klarstellung zur Zeile darüber (W5): Beide Zeilen gelten: nach jedem Start-Auslöser plant der steuernde Chat eine Nachschau per `send_later` (unter einer Stunde); ohne Commit von Schritt 0 ein Hinweis an den Betreiber, dann warten, keine Nachschau-Kette (Vorgabe 08.10.2026; 07.10.2026: nach dem Auslöser für TB-140 war keine Nachschau per `send_later` geplant) | 22.5; UMZUG 3 |
```

#### E16 — Abschnitt 0, „Wenn eine Mac-Sitzung startet“: Sonde vor dem Zeigerwechsel

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Ein abgewiesener Start-Auslöser taugt als Sonde` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Die Sonde `starte_TB-99` vor dem Zeigerwechsel legen (07.10.2026, so getragen; ebenso die Sonde vor dem Zeigerwechsel im Umzug 23:39) | UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8; UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 6 |
```

#### E17 — Abschnitt 0, „Wenn Dateien abgelegt … werden“: Backlog-Übersichten

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Grosse Dokumente nicht im Chat zusammensetzen` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Backlog-Übersichten in eine Datei schreiben und nur die Kandidaten in den Chat holen (06.10.2026: 17 KB Zeilenanfänge des Backlogs im Chat) | UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 2 |
```

#### E18 — Abschnitt 0, „Wenn Dateien abgelegt … werden“: Ablege-Skript

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Die Suche der Ablage liefert Ausschnitte auch aus gesperrten Dateien` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Ein Ablege-Skript prüft erst alles und schreibt dann; es ist wiederholbar gebaut (06.10.2026: Das Ablege-Skript scheiterte an einer falschen Zählung im Zeiger, nachdem es den Auftrag schon kopiert hatte) | UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 2 |
```

#### E19 — Abschnitt 0, „Wenn ich ein fremdes Ergebnis bewerte“: Sammelwort, Widerspruch zweier Helfer

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Die Abnahme macht ein eng zugeschnittener Helfer, nur lesend` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | Ein Sammelwort für Befunde erst wählen, wenn jeder Befund einzeln eingeordnet ist (07.10.2026: „acht formale Befunde“ für eine Liste, in der zwei Aussagen ohne Beleg standen) | UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 3; UEBERGABE, Nachtrag 07.10.2026, 10:32, Abschnitt 8 Nr. 1 |
| ☐ | Bei Widerspruch misst der steuernde Chat die eine Tatsache selbst, mit einem Skript (07.10.2026: Zwei Helfer widersprachen sich, K13) | UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 3 |
```

#### E20 — Abschnitt 0, „Wenn ich einen Auftrag schreibe“: Helfer bauen (W1), Auszug (W2), Tabelle statt Kurzantwort (W6), Befunde (W7), acht Regeln aus den Umzügen

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `Unveränderte Textteile übernimmt ein Skript aus der Quelle, mit` · Art: **nach der Zeile**
Form: **Zeilen**

```
| ☐ | ⭐ Helfer bauen ausserhalb des Repos (Aufträge, Registerentwürfe); Urteil und Freigabe bleiben beim steuernden Chat; ins Repo schreibt nur die Mac-Sitzung; ein frischer Gegenleser ist Pflicht (Betreiber, Karte 08.10.2026: „Helfer bauen Entwürfe (Empfohlen)“) | 22.10 |
| ☐ | Die Bestandsaufnahme vor dem Bau (zwei Helfer, getrennter Zuschnitt); Bestand und Entwurf in einem Helfer, danach Gegenleser mit getrenntem Zeilenbereich (06. und 07.10.2026, so getragen) | UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 6; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8 |
| ☐ | F1 bleibt für Registertext. Helferberichte darf ein Helfer auf die Stellen schneiden, die der Bau braucht: wörtlich, mit Zeile, nichts umformuliert; der Chat, der einen Auftrag baut, liest die Kernlektüre und sonst nur Ausschnitte (Betreiber, Karte 08.10.2026: „Nur wörtlicher Auszug (Empfohlen)“; 06.10.2026: Kernlektüre 43 KB, Bestandsbericht 30 KB) | 22.10; UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 3 |
| ☐ | T1 bleibt (aus Helferberichten nur die Abweichungen in den Chat); was in Registertext oder eine Vorgabe geht, liest der steuernde Chat an der Tabelle des Berichts, nicht an der Kurzantwort; der Gegenleser bekommt genau diese Stellen genannt (Vorgabe W6, 08.10.2026; 07.10.2026: „zwei zu zwei“ und „keiner zwingend“ ungeprüft übernommen) | 22.10; UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 2 |
| ☐ | Befunde, die eine Messung, einen Sollwert, eine Fundstelle oder Registertext ändern, werden immer eingearbeitet; reine Formlücken dürfen als Hinweis im Auftrag stehen bleiben, der steuernde Chat nennt sie dem Betreiber bei der Übergabe; dem Berichtiger ein Grössenziel geben (Betreiber, Karte 08.10.2026: „Wichtiges ja, Form als Hinweis (Empfohlen)“; 07.10.2026: TB-140 wuchs über drei Gegenleserunden von 58 709 B auf 159 021 B) | 22.10; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 2 |
| ☐ | Zählungen im Auftrag kommen aus dem Skript; zwei Runden Gegenlesen bleiben (06.10.2026: beim Bau von TB-133 die Zeilen einer Einfügung falsch gezählt) | UEBERGABE, Umzug 06.10.2026, 07:08, Block 7 Nr. 3 |
| ☐ | Helferberichte auf rund 3 KB begrenzen, das Übrige in Dateien; enge Helfer mit Berichtsgrenze und Berichtsdatei (06.10.2026; ergänzt T1 in 22.10) | UEBERGABE, Umzug 06.10.2026, 07:08, Block 7 Nr. 4; UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 4 |
| ☐ | Lange Auftragstexte aus Bausteindateien per Skript bauen; Helferaufträge aus Bausteindateien bauen — der Helfer liest seinen Auftrag selbst (07.10.2026: rund 20 Aufträge zu 3 bis 6 KB von Hand geschrieben) | UEBERGABE, Umzug 06.10.2026, 07:08, Block 7 Nr. 4; UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 2; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 1; UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 1 |
| ☐ | Vorzählung als Skript vor und nach jeder Berichtigung; Berichtigungen per Skript mit `assert` auf genau einen Treffer (06.10.2026, so getragen) | UEBERGABE, Umzug 06.10.2026, 07:08, Block 7 Nr. 5; UEBERGABE, Umzug 06.10.2026, 13:43, Block 7 Nr. 4; UEBERGABE, Umzug 07.10.2026, 06:59, Block 7 Nr. 6 |
| ☐ | Vor einer Lesart den Index nach „gilt“ und „dazu“ fragen (06.10.2026: der Beginn je Bot zuerst nur auf 21.5 gestützt) | UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 1; UEBERGABE, Nachtrag 06.10.2026, 14:25 |
| ☐ | Ein Bauskript prüft an der Quelle; zwei gleichzeitige Gegenleser mit getrenntem Zuschnitt (Quellen, Logik) und ein dritter für die Nachlese (06.10.2026: Bauskript mit 139 Prüfungen an der Quelle; 07.10.2026: zwei Gegenleser mit getrenntem Bereich) | UEBERGABE, Umzug 06.10.2026, 16:40, Block 7 Nr. 5; UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8; UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 6 |
| ☐ | Die Simulation an Kopien samt Gegenprobe; den nächsten Auftrag vorbauen, während eine Sitzung misst (07.10.2026: der Vorbau von TB-139 während der Messung) | UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 8 |
| ☐ | Vor einem Helferstart prüfen, ob der Zielordner schon existiert (07.10.2026: Ein Helferaufruf lief, ohne dass sein Bericht ankam; der zweite fand dessen `v3/` vor) | UEBERGABE, Umzug 07.10.2026, 23:39, Block 7 Nr. 5 |
```

#### E21 — Abschnitt 13: der Betreibersatz vom 07.10.2026, 19:44, und die Lesart

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `direkt weiter ohne das ich dich fragen muss wie geht es weiter."*` · Art: **nach der Zeile**
Form: **Block**

```
⚠️⚠️ **Ergänzung, Betreiber 07.10.2026, 19:44 („zukünftig“):** *„Ich fand deine selbstständige Arbeitsweise heute super und möchte das du zukünftig immer so arbeitest!“* Lesart des steuernden Chats, vorläufig — „so“ heisst: Grosses bauen und prüfen Helfer mit eigenem Kontext, der steuernde Chat holt nur Kurzberichte; Handwerk entscheidet er als Vorgabe, Karten nur für echte Betreiberentscheide; nach jedem Schritt folgt ohne Startzeichen der nächste, auch über mehrere Aufträge und während eine Mac-Sitzung läuft; Zwischenmeldungen mit Ergebnis statt Rückfragen; Aufgaben an den Betreiber nur, wo seine Hand nötig ist. Was Helfer bauen und was der steuernde Chat aus Helferberichten liest, regelt seit dem 08.10.2026 die Ergänzung in 22.10 (W1, W2, W6); sie geht der Lesart vor (UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46).
```

#### E22 — Abschnitt 13: Zusatz zu „kein Haltepunkt“ (W8)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `läuft daneben weiter. **Gefragt wird nebenher, nicht statt zu arbeiten.**` · Art: **nach der Zeile**
Form: **Zeilen**

```
⭐ **Zusatz 08.10.2026 (W8; Vorgabe des steuernden Chats, gilt, da nicht
widersprochen):** Eine offene Karte hält den Chat technisch an. Am 07.10.2026
stand eine Karte von 11:37 bis 14:55 offen; solange arbeitete der Chat nicht
(UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 6). Deshalb gilt:
vor der Karte wird alles Unabhängige angestossen, auch langlaufende Helfer.
```

#### E23 — Abschnitt 15, Austausch mit dem Verfahrensprüfer: Regel 5a (W3)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `**Eine Fable-Anfrage ist erst übergeben, wenn sie als Kopierblock in der Antwort stand.**` · Art: **nach der Zeile**
Form: **Zeilen**

```
| **5a** | ⭐ **Eine Fable-Anfrage ab rund 20 KB geht als Datei in den Chat, der Betreiber lädt sie im Fable-Chat hoch; kürzere bleiben Kopierblock.** Für die Datei gilt Regel 5 entsprechend: übergeben ist sie erst, wenn sie als Datei im Chat stand (Lesart des steuernden Chats, vorläufig) | Anfrage 07.10.a: der Kopierblock (34 882 B einmal gelesen und einmal ausgegeben) | Betreiber, Karte 07.10.2026, 22:44: „Ja, ab 20 KB als Datei (Empfohlen)“ (W3); UEBERGABE, Umzug 07.10.2026, 19:45, Block 7 Nr. 1 |
```

#### E24 — Abschnitt 22.5: Klarstellung 08.10.2026 (W5)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `### 22.6 ⭐ Eine untätige Sitzung ist kein Schreibverbot` · Art: **vor der Zeile**
Form: **Block**

```
⭐ **Klarstellung 08.10.2026 (W5; Vorgabe des steuernden Chats, gilt, da nicht widersprochen):** Beide Zeilen gelten: nach jedem Start-Auslöser plant der steuernde Chat eine Nachschau per `send_later` (unter einer Stunde); ohne Commit von Schritt 0 ein Hinweis an den Betreiber, dann warten, keine Nachschau-Kette. Gemeint sind die Regel oben und die Zeile in Abschnitt 0, Gruppe „Wenn eine Mac-Sitzung startet, endet oder abbricht“ („keine Nachschau-Kette (29.09.2026)“). „Unter einer Stunde“: Eine Nachschau liegt unter einer Stunde (UMZUG 3, S7). Anlass: nach dem Auslöser für TB-140 war keine Nachschau per `send_later` geplant (UEBERGABE, Umzug 07.10.2026, 19:45, Zusatz 19:46).
```

#### E25 — Abschnitt 22.10: Ergänzung 08.10.2026 — W1, W2, W7, W4, W6

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Anker: `### 22.11 Fable-Filter` · Art: **vor der Zeile**
Form: **Block**

```
⭐ **Ergänzung 08.10.2026 — Entscheide W1, W2 und W7 (Betreiber per Karte, gestellt 08.10.2026, 00:34; beantwortet vor 08.10.2026, 06:55) und Vorgaben W4 und W6 des steuernden Chats (Antwort 08.10.2026, 00:33; gelten, da nicht widersprochen):**
- **W1** „Helfer bauen Entwürfe (Empfohlen)“: 22.10 wird ergänzt — Helfer bauen ausserhalb des Repos (Aufträge, Registerentwürfe); Urteil und Freigabe bleiben beim steuernden Chat; ins Repo schreibt nur die Mac-Sitzung; ein frischer Gegenleser ist Pflicht.
  Das geht dem Grundsatz „nie deuten“ und dem Satz „Nie für Register, Commits, Aufträge schreiben oder Freigaben“ oben vor, soweit es um Entwürfe ausserhalb des Repos geht; Anlass ist der Betreibersatz vom 07.10.2026, 19:44, in 13 (Lesart des steuernden Chats, vorläufig).
- **W2** „Nur wörtlicher Auszug (Empfohlen)“: F1 bleibt für Registertext. Helferberichte darf ein Helfer auf die Stellen schneiden, die der Bau braucht: wörtlich, mit Zeile, nichts umformuliert; was in Registertext oder eine Vorgabe geht, liest der steuernde Chat an der Tabelle des Berichts. Das geht dem Satz „liest der Auftraggeber selbst im Wortlaut an der Fundstelle“ oben vor, soweit der Bericht den Wortlaut mit Zeile trägt (Lesart des steuernden Chats, vorläufig).
- **W7** „Wichtiges ja, Form als Hinweis (Empfohlen)“: Befunde, die eine Messung, einen Sollwert, eine Fundstelle oder Registertext ändern, werden immer eingearbeitet; reine Formlücken dürfen als Hinweis im Auftrag stehen bleiben, der steuernde Chat nennt sie dem Betreiber bei der Übergabe.
  Das präzisiert den Satz „Befunde werden vor dem Übergeben eingearbeitet“ oben.
- **W4:** Eine Fable-Anfrage baut ein frischer Helfer (Vorprüfung und Entwurf), ein zweiter liest gegen. Ein frischer Chat nur nach dem Ja des Betreibers zum Umzug (Regel 05.10.2026, 23:58, geht vor).
- **W6:** T1 bleibt (aus Helferberichten nur die Abweichungen in den Chat); was in Registertext oder eine Vorgabe geht, liest der steuernde Chat an der Tabelle des Berichts, nicht an der Kurzantwort (Block 7 Nr. 2 des Umzugs 07.10.2026, 23:39).
```

#### E26 — BACKLOG, Abschnitt 5: Abnahme TB-139, Reihenfolge, Fehler Nr. 21 und 22, TB-141

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Anker: `## 6 — Geparkt, null Arbeit` · Art: **vor der Zeile**
Form: **Block**

```
### Aus der Abnahme TB-139 (08.10.2026), den Entscheiden vom 07. und 08.10.2026 und den Fehlern Nr. 21 und 22 — eingetragen mit TB-141

- **TB-139 abgenommen** (08.10.2026; Helfer ABNAHME139, Kernzahlen vom steuernden Chat mit eigenem Skript nachgemessen, 00:11): Abgenommen. Register 11 581 → 11 733 Zeilen, 998 257 B, sha256 beginnt `ab97ae1e31da161b`, Stand `ad1fc0d`, an HEAD gleich; 152 hinzu, 0 entfernt; 20 Marken an 14 Einfügestellen (PRÄZISIERT 4, BERICHTIGT 1, ERGÄNZT 15); 55.1–55.8; höchster Block R83; Blöcke 6/6 zeichengleich (12/12 Zeilen). Prüfungen P1 14/14, P2 6/6, P3 10/10, P4 20/20, P5 3/3, P6 6/6, P9 7/7, P10 3/3.
- **Anmerkungen zur Abnahme:** (1) `docs/belege/TB-139/d3_porcelain.txt` (78 B) trägt eine Kommentarzeile „(0 Zeilen)“ statt der Rohausgabe; „leer“ nur erschlossen. (2) `b_vergleich.txt` Z. 4, `j1_einsetzen.txt` Z. 2, `j1_vergleich.txt` Z. 2: Kopfzeile fehlt, Reststück am Ende. (3) Das Ergebnis (Z. 20) nennt keine Abweichungen; (1) und (2) fehlen dort. (4) Nicht nachgerechnet, nur an der Rohausgabe gelesen: Test, Sonde, `register()`, Werkzeugläufe; Zahlenprüfung Teilmessung: 594 Zahlen, 36 in keiner Rohausgabe.
- **Fehler Nr. 21 (steuernder Chat, Auftrag TB-139):** Register Z. 11727 (55.8) nennt die unsichere Marke einmal „48.7 (R39) zu R81 (a)“ (Sp. 310, gezählt ab 1) und einmal „48.7 (R39) zu R81 (a) und (b)“ (Sp. 1029); der Text kam zeichengleich aus dem Auftrag (Auftrag Z. 12 nur „(a)“). Am Register wird nichts geändert; geht mit 55.8 Nr. 10 an Fable (zweite Anfrage).
- **Fehler Nr. 22 (steuernder Chat, Umzugsblock 07.10.2026, 23:39, Block 4 Nr. 7):** „Backlog E-7/E-8“ — E-7 und E-8 stehen nicht im Backlog, sondern in `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 122/123. **Berichtigung:** Wo `UEBERGABE.md` im Umzug 07.10.2026, 23:39, Block 4 Nr. 7, „Backlog E-7/E-8“ nennt, sind E-7 (Zellen-Kern) und E-8 (Zellen-Erzeuger) der Tabelle in `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 122/123 gemeint; `UEBERGABE.md` selbst wird nicht geändert.
- Ablage erneuert (Helfer ABLAGE139): 63 Dateien (61 ersetzt, 2 neu: `REGISTER_KOPIE_ABSCHNITT_55.md`, `ERGEBNIS_TB-139_register_fable_07a.md`); vorher 104 Einträge, 54,2 %; nachher 106, 56,5 %; md5 über die md5-Liste `acef90519ecef4ed36f112b06ed281b1`; nicht zurückgelesen.
- Reihenfolge danach (Bestand Helfer BESTAND_ERZEUGER): Bauauftrag Zellen-Erzeuger nach R81/R82 erst nach der zweiten Fable-Anfrage (55.8 Nr. 5 „vor dem Bau des Schnitts im Zellen-Erzeuger“); er berührt Sperrlisten-Dateien, der Signalpfad braucht eine Einzelfreigabe nach 37.3 (55.8 Nr. 3). Reihenfolge: TB-141 → Abnahme TB-137 → Fable-Anfrage → Bauauftrag.
- Streichliste der Erinnerung: Bilanz bestätigt (72: 5/8/34/25); die vier Arten decken 19 der 25; zwei Inhalte stehen teilweise im Repo (Paar-Rotation nur auf `origin/claude/pair-rotation-prototype`, Commit `d7ab671`). Entscheid des Betreibers steht aus; nichts gestrichen.
- Berichte: `logs/steuernder_chat/TB-139_ABNAHME_bericht.md`, `TB-139_ABLAGE_bericht.md`, `TB-141_KARTE_W_bericht.md`, `TB-139_ERINNERUNG_karte_bericht.md`, `TB-139_ERINNERUNG_suche_zwei_bericht.md`, `ERZEUGER_bestand_R81_R82_bericht.md` (von git ignoriert).
- **Ins Regelwerk eingetragen mit TB-141:** die 38 Regeln U1–U38 aus `logs/steuernder_chat/TB-141_bestand_REGELN.md` (4 standen schon und sind nur geprüft, 18 ergänzt, 16 neu), die fünf Regeln aus Block 7 des Umzugs 07.10.2026, 23:39, die Entscheide W1, W2, W3 und W7 des Betreibers und die Vorgaben W4, W5, W6 und W8 — `ARBEITSWEISE.md` Abschnitt 0 (39 Zeilen), 13, 15 (Regel 5a), 22.5 und 22.10. Wo ein Entscheid eine Regel des Bestands anders fasst, gilt der Entscheid (U2, U16, U22, U28, U30, U31, U34).
- **Nicht in TB-141:** die übrigen Posten, die die Übergabe dem Regelwerk-Nachtrag zuweist (Bestand Abschnitt 7: `diff --name-only` in `ARBEITSWEISE.md` Abschnitt 0 und in `UMZUG.md` Abschnitt 6, der Fliesstext in 6b und 10, die Regel zu Cloud-Sitzungen, der Entwurf aus Paket 15, die zwei Befunde aus der Abnahme TB-133); eine eigene Gruppe für Helfer in Abschnitt 0; die Kennzeichnung der Aufgaben im Text von 6bb; U25 in `UMZUG.md` Abschnitt 4, Schritt 6. Ob ein eigener Nachtrag sie trägt, ist offen.
```

### Prüfungen S1–S4 — Regeln, die schon stehen (nur der Verweis wird gezählt)

Je Prüfanker Soll **genau 1** in der Zieldatei, vor und nach Schritt A (Probe und C3). Weicht einer ab: nicht berichtigen, im Ergebnis nennen.

#### S1 — U3: Handwerk als Vorgabe, Karten nur für echte Betreiberentscheide

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Prüfanker: `Karte nur für echte Betreiberentscheide: Freigaben`

#### S2 — U8: Nachschau per `send_later` (22.5)

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Prüfanker: `Nach jedem ausgelösten Auftrag plant der steuernde Chat eine`

#### S3 — U37: Abschriften mit `cmp`, md5 und Bytes beidseitig, md5 über die md5-Liste, Start über den Wächter, Uhrzeit mit `date`

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Prüfanker: `Abschriften aus der Ablage zweifach unabhängig`
Prüfanker: `` md5 und `wc -c` auf beiden Seiten ``
Prüfanker: `Statt vieler md5-Zeilen im Chat ein md5 über die md5-Liste`
Prüfanker: `Ist ein Mac-Auftrag startklar, legt der steuernde Chat die Claude-Code-Sitzung selbst über den Sitzungswächter an`
Prüfanker: `im selben Schritt, in dem sie in einen Text gehen — nie schätzen`

#### S4 — U38: Umzug nur auf Ansage, kein `git check-ignore`, Uhrzeit gemessen, Ablage durch einen Helfer

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Prüfanker: `Umgezogen wird nur, wenn der Betreiber es sagt oder genehmigt. Der steuernde Chat zieht nicht von sich aus um`
Prüfanker: `` und kein `git check-ignore` ``
Prüfanker: `Die Erneuerung der Ablage (Abschnittsdateien, Index, Dialog-Index) macht ein Helfer`

## Schritt C — Nachweis

**C1.** `a_einfuegungen.txt` aus Schritt A (Soll dort).

**C2.** `trading-env/bin/python3 -B docs/belege/TB-141/tb141_einfuegen.py numstat <⟨S0⟩> HEAD; echo "rc $?"` ⇒ `docs/belege/TB-141/c2_numstat.txt` (die Rohzeilen von `git diff --numstat` stehen darin mit `roh:` davor). Soll: rc 0; `ARBEITSWEISE.md` `58	0`, `BACKLOG.md` `13	0`; ausser Belegen unter `docs/belege/TB-141/` keine weitere Datei; **keine entfernte Zeile** (es gibt keine benannte Ersetzung).

**C3.** `trading-env/bin/python3 -B docs/belege/TB-141/tb141_einfuegen.py vergleich; echo "rc $?"` ⇒ `docs/belege/TB-141/c3_vergleich.txt`. Soll: rc 0; je Einfügung `Vorkommen 1 · an Zeilengrenzen 1 · GLEICH` (bei Form Block zusätzlich je genau eine Leerzeile davor und danach); 10 Prüfanker `nachher 1 · ok`; Schlusszeile `Anzahl Einfügungen: 26 · Gesamt: alle zeichengleich, je genau einmal`.

Commit `TB-141 C: Nachweis`, pushen.

## Schritt D — Abgabe

**D1.** `docs/ERGEBNIS_TB-141_regelwerk_nachtrag_0807.md`: Kopf (Stand, Commits, ⟨S0⟩), **„Kurz“** (Tabelle Soll | Ist für 0a, 0b, 0c, A, C1, C2, C3, D2, J1, D3), **„Abweichungen vom Auftrag“** — jede, auch kleine: jede Rohausgabe, die nicht wie Soll aussieht, jede ausgelassene Einfügung, jeder Sachfehler im vorgegebenen Text, jede Belegdatei ohne Kopfzeile; gibt es keine, steht dort „keine“ mit der Liste der geprüften Sollwerte (Abnahme TB-139, Anm. 3) —, **„Nicht getan“** (die Ablage von `ARBEITSWEISE.md` und `BACKLOG.md` macht der steuernde Chat; die Posten unter „Nicht in TB-141“ in E26; `UEBERGABE.md` und `UMZUG.md` unverändert) und **„In einfacher Sprache“**.

**D2. Journal.** Kennung vorher messen (letzter Buchstabenblock vor `## Wiederkehrende Lehren`; erwartet **EJ**, weil EI der Block von TB-139 ist; trägt das Journal eine andere, die gemessene nehmen und im Ergebnis nennen). Die Sitzung schreibt ihren Block nach `docs/belege/TB-141/d2_journal_block.md`, in der Gliederung des Blocks EI: Kopfzeile `## <Kennung> — TB-141: …`, Quellenzeile `*Quelle: `docs/ERGEBNIS_TB-141_regelwerk_nachtrag_0807.md`*`, Absatz „**Quelle:**“ (Sitzung, Datum, Eingang `d4a28e9`, Commits, Belege, keine Rückfrage, kein Abbruch — oder was war), `### Was gemessen ist`, `### Was offen bleibt`, Schlusszeile `*Geschrieben … von der Mac-Sitzung TB-141. Quellenvermerk: siehe Kopf.*`. Der Block trägt keinen Trennstrich `---` und nicht den Nachtrag J1; was die Sitzung selbst gemessen hat, steht in ihrem Block, den Nachtrag gibt sie dort nicht in eigenen Worten wieder. Dann, je mit `trading-env/bin/python3 -B docs/belege/TB-141/tb141_einfuegen.py`:
1. `journal --kennung <Kennung> --block docs/belege/TB-141/d2_journal_block.md --probe` ⇒ `d2_journal_probe.txt`, dann ohne `--probe` ⇒ `d2_journal.txt` (Soll je: sechs Bedingungen `ja`, rc 0; der Block steht danach vor `## Wiederkehrende Lehren`, mit `---` davor und danach wie EI);
2. `j1 --kennung <Kennung> --probe` ⇒ `d2_j1_probe.txt`, dann ohne `--probe` ⇒ `d2_j1.txt` (Soll je: vier Bedingungen `ja`, `Textzeilen 11`, rc 0; J1 steht dann nach dem Absatz „**Quelle:**“ und vor `### Was gemessen ist`, mit je einer Leerzeile davor und danach);
3. `j1vergleich --kennung <Kennung>` ⇒ `d2_j1_vergleich.txt` (Soll: `Vorkommen 1 · an Zeilengrenzen 1 · im Block <Kennung> vor ### Was gemessen ist ja · GLEICH`, rc 0).

rc 2 bei 1. oder 2. heisst: nichts geschrieben; die Bedingungen stehen dann in `d2_journal_abgewiesen.txt` bzw. `d2_j1_abgewiesen.txt`, ein früherer Beleg bleibt stehen. Dann die Bedingung lesen, den eigenen Block richten und neu laufen lassen; scheitert J1 auch so, schreibt die Sitzung in ihren Block nur, dass der Nachtrag aussteht und warum, und nennt es im Ergebnis (kein Abbruch).

#### J1 — JOURNAL: der Nachtrag im Journalblock der Sitzung

Zieldatei: `docs/projektfuehrung/JOURNAL.md`

```
**Nachtrag des steuernden Chats zum Stand vor TB-141, wie in `BACKLOG.md` Abschnitt 5 eingetragen:**
- **TB-139 abgenommen** (08.10.2026; Helfer ABNAHME139, Kernzahlen vom steuernden Chat mit eigenem Skript nachgemessen, 00:11): Abgenommen. Register 11 581 → 11 733 Zeilen, 998 257 B, sha256 beginnt `ab97ae1e31da161b`, Stand `ad1fc0d`, an HEAD gleich; 152 hinzu, 0 entfernt; 20 Marken an 14 Einfügestellen (PRÄZISIERT 4, BERICHTIGT 1, ERGÄNZT 15); 55.1–55.8; höchster Block R83; Blöcke 6/6 zeichengleich (12/12 Zeilen). Prüfungen P1 14/14, P2 6/6, P3 10/10, P4 20/20, P5 3/3, P6 6/6, P9 7/7, P10 3/3.
- **Anmerkungen zur Abnahme:** (1) `docs/belege/TB-139/d3_porcelain.txt` (78 B) trägt eine Kommentarzeile „(0 Zeilen)“ statt der Rohausgabe; „leer“ nur erschlossen. (2) `b_vergleich.txt` Z. 4, `j1_einsetzen.txt` Z. 2, `j1_vergleich.txt` Z. 2: Kopfzeile fehlt, Reststück am Ende. (3) Das Ergebnis (Z. 20) nennt keine Abweichungen; (1) und (2) fehlen dort. (4) Nicht nachgerechnet, nur an der Rohausgabe gelesen: Test, Sonde, `register()`, Werkzeugläufe; Zahlenprüfung Teilmessung: 594 Zahlen, 36 in keiner Rohausgabe.
- **Fehler Nr. 21 (steuernder Chat, Auftrag TB-139):** Register Z. 11727 (55.8) nennt die unsichere Marke einmal „48.7 (R39) zu R81 (a)“ (Sp. 310, gezählt ab 1) und einmal „48.7 (R39) zu R81 (a) und (b)“ (Sp. 1029); der Text kam zeichengleich aus dem Auftrag (Auftrag Z. 12 nur „(a)“). Am Register wird nichts geändert; geht mit 55.8 Nr. 10 an Fable (zweite Anfrage).
- **Fehler Nr. 22 (steuernder Chat, Umzugsblock 07.10.2026, 23:39, Block 4 Nr. 7):** „Backlog E-7/E-8“ — E-7 und E-8 stehen nicht im Backlog, sondern in `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 122/123. **Berichtigung:** Wo `UEBERGABE.md` im Umzug 07.10.2026, 23:39, Block 4 Nr. 7, „Backlog E-7/E-8“ nennt, sind E-7 (Zellen-Kern) und E-8 (Zellen-Erzeuger) der Tabelle in `docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 122/123 gemeint; `UEBERGABE.md` selbst wird nicht geändert.
- Ablage erneuert (Helfer ABLAGE139): 63 Dateien (61 ersetzt, 2 neu: `REGISTER_KOPIE_ABSCHNITT_55.md`, `ERGEBNIS_TB-139_register_fable_07a.md`); vorher 104 Einträge, 54,2 %; nachher 106, 56,5 %; md5 über die md5-Liste `acef90519ecef4ed36f112b06ed281b1`; nicht zurückgelesen.
- Reihenfolge danach (Bestand Helfer BESTAND_ERZEUGER): Bauauftrag Zellen-Erzeuger nach R81/R82 erst nach der zweiten Fable-Anfrage (55.8 Nr. 5 „vor dem Bau des Schnitts im Zellen-Erzeuger“); er berührt Sperrlisten-Dateien, der Signalpfad braucht eine Einzelfreigabe nach 37.3 (55.8 Nr. 3). Reihenfolge: TB-141 → Abnahme TB-137 → Fable-Anfrage → Bauauftrag.
- Streichliste der Erinnerung: Bilanz bestätigt (72: 5/8/34/25); die vier Arten decken 19 der 25; zwei Inhalte stehen teilweise im Repo (Paar-Rotation nur auf `origin/claude/pair-rotation-prototype`, Commit `d7ab671`). Entscheid des Betreibers steht aus; nichts gestrichen.
- Berichte: `logs/steuernder_chat/TB-139_ABNAHME_bericht.md`, `TB-139_ABLAGE_bericht.md`, `TB-141_KARTE_W_bericht.md`, `TB-139_ERINNERUNG_karte_bericht.md`, `TB-139_ERINNERUNG_suche_zwei_bericht.md`, `ERZEUGER_bestand_R81_R82_bericht.md` (von git ignoriert).
- **Ins Regelwerk eingetragen mit TB-141:** die 38 Regeln U1–U38 aus `logs/steuernder_chat/TB-141_bestand_REGELN.md` (4 standen schon und sind nur geprüft, 18 ergänzt, 16 neu), die fünf Regeln aus Block 7 des Umzugs 07.10.2026, 23:39, die Entscheide W1, W2, W3 und W7 des Betreibers und die Vorgaben W4, W5, W6 und W8 — `ARBEITSWEISE.md` Abschnitt 0 (39 Zeilen), 13, 15 (Regel 5a), 22.5 und 22.10. Wo ein Entscheid eine Regel des Bestands anders fasst, gilt der Entscheid (U2, U16, U22, U28, U30, U31, U34).
- **Nicht in TB-141:** die übrigen Posten, die die Übergabe dem Regelwerk-Nachtrag zuweist (Bestand Abschnitt 7: `diff --name-only` in `ARBEITSWEISE.md` Abschnitt 0 und in `UMZUG.md` Abschnitt 6, der Fliesstext in 6b und 10, die Regel zu Cloud-Sitzungen, der Entwurf aus Paket 15, die zwei Befunde aus der Abnahme TB-133); eine eigene Gruppe für Helfer in Abschnitt 0; die Kennzeichnung der Aufgaben im Text von 6bb; U25 in `UMZUG.md` Abschnitt 4, Schritt 6. Ob ein eigener Nachtrag sie trägt, ist offen.
```

Die Spiegelstriche von J1 sind die von E26, Zeichen für Zeichen (das Bauskript hat beide aus einer Quelle gesetzt); nur die erste Zeile ist eine andere.

**D3.** Abgabe-Commit `TB-141 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Danach:
- `git status --porcelain > "$TMPDIR/tb141_d3.txt"`; unverändert nach `docs/belege/TB-141/d3_porcelain.txt` kopieren (`cmp` gleich) — **Rohausgabe**, ohne Kommentarzeile (Abnahme TB-139, Anm. 1); Soll 0 B. Dazu `docs/belege/TB-141/d3_porcelain.kopf.txt` mit genau einer Zeile: `# TB-141 D3 — git status --porcelain nach dem Abgabe-Commit <Hash>, Rohausgabe in d3_porcelain.txt: <Bytes> B, <Zeilen> Zeilen, md5 <md5>`.
- `git diff --numstat ⟨S0⟩ <Abgabe-Commit> > docs/belege/TB-141/d3_numstat.txt` (roh) und `d3_numstat.kopf.txt` (eine Zeile wie oben). Soll: `ARBEITSWEISE.md` `58	0`, `BACKLOG.md` `13	0`, `JOURNAL.md` `<n>	0` mit n = Zeilen des eigenen Blocks + 3 (`d2_journal.txt`) + 11 + 1 (`d2_j1.txt`); dazu nur Ergebnis und Belege; nirgends eine entfernte Zeile.
- Kleiner letzter Commit `TB-141 D3: porcelain und numstat nach der Abgabe`, pushen.
- Danach `git status --porcelain` noch einmal; die Rohausgabe (Soll leer) steht wörtlich in der Schlussmeldung der Sitzung, mit dem Hash des letzten Commits.

## Abbruchkriterien (nur für diesen Gegenstand)

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Skripts weicht ab.
- Sperrlisten-Wache in 0c mit Treffer, oder `einfuegen` endet mit rc 2.
- Eine Datei ausserhalb von `ARBEITSWEISE.md`, `BACKLOG.md`, `JOURNAL.md`, Belegen, Ergebnis und Auftrag müsste geändert werden.
- `git push` scheitert zweimal.

**Kein Abbruch:** ein Anker ≠ 1 oder eine erste Textzeile schon vorhanden (nicht einfügen, nennen); 0b weicht ab (vermerken); `journal` oder `j1` mit rc 2 (wie in D2 beschrieben); eine Kennung ≠ EJ.

Bei Abbruch: committen, was an Belegen da ist, Grund in `docs/belege/TB-141/abbruch.txt` (mit Kopfzeile), pushen, melden.

## In einfacher Sprache

Seit dem 6. Oktober sind in der Zusammenarbeit viele kleine Regeln entstanden, die bisher nur in der Übergabe stehen, dazu Entscheide des Betreibers vom 7. und 8. Oktober: Helfer dürfen Entwürfe bauen, aber nicht ins Repo schreiben; Helferberichte werden nur wörtlich gekürzt; grosse Fable-Anfragen gehen als Datei. Dieser Auftrag schreibt diese Regeln an die richtigen Stellen der Arbeitsregeln (39 Zeilen in der Checkliste, dazu Absätze in den Abschnitten 13, 15, 22.5 und 22.10) und hält die Abnahme von TB-139 in der Aufgabenliste und im Journal fest. Am Code, am Register und an den Werkzeugen ändert er nichts; alte Zeilen bleiben stehen.

## Anhang A — Einfügeskript und Sollwerte

### Einfügeskript

sha256 des ausgelesenen Texts (mit abschliessendem Zeilenende): `1af78b614412a698a30658e2d556390ca802bd1fb3e7218b47d23903d2445d6c`.

```python
#!/usr/bin/env python3
"""TB-141: Einfügungen E1–E26, Prüfungen S1–S4, Journalblock und J1 — alles aus dem Auftrag gelesen.

Liest je Einfügung Zieldatei, Anker, Art, Form und Text (erster Codeblock ohne Zäune) aus dem
Auftrag, nicht aus dem Gedächtnis; Überschriften zählen nur ausserhalb von Codeblöcken.
Anker in doppelten Backticks (`` x ``) werden als Codespanne gelesen.
Jede Belegdatei wird ganz neu geschrieben, trägt eine Kopfzeile und wird zurückgelesen
(kein Reststück). Aufruf aus der Repo-Wurzel mit trading-env/bin/python3 -B:

  tb141_einfuegen.py probe                        nur lesen        -> a_probe.txt
  tb141_einfuegen.py einfuegen                    E1–E26           -> a_einfuegungen.txt
  tb141_einfuegen.py vergleich                    C3               -> c3_vergleich.txt
  tb141_einfuegen.py numstat <von> <bis>          C2 (git diff)    -> c2_numstat.txt
  tb141_einfuegen.py journal --kennung K --block DATEI [--probe]   -> d2_journal.txt (Probe: d2_journal_probe.txt)
  tb141_einfuegen.py j1 --kennung K [--probe]                      -> d2_j1.txt (Probe: d2_j1_probe.txt)
  tb141_einfuegen.py j1vergleich --kennung K                       -> d2_j1_vergleich.txt

rc 0: wie Soll. rc 1: Abweichung, die Ausgabe nennt sie. rc 2: Bedingung verletzt, nichts geändert
(journal und j1 schreiben dann *_abgewiesen.txt und lassen einen früheren Beleg stehen).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

AUFTRAG = Path("docs/auftraege/MAC_TB-141_regelwerk_nachtrag_0807.md")
BELEG = Path("docs/belege/TB-141")
JOURNAL = Path("docs/projektfuehrung/JOURNAL.md")
JANKER = "\n---\n\n## Wiederkehrende Lehren\n"
SKRIPT = "tb141_einfuegen.py"

RE_KOPF = re.compile(r"^#### ([ESJ]\d+) — ")
RE_DATEI = re.compile(r"^Zieldatei: `([^`]+)`$")
RE_ANKER = re.compile(r"^Anker: (?:`` (.+?) ``|`([^`]+)`) · Art: \*\*(nach der Zeile|vor der Zeile)\*\*$")
RE_FORM = re.compile(r"^Form: \*\*(Zeilen|Block)\*\*$")
RE_PRUEF = re.compile(r"^Prüfanker: (?:`` (.+?) ``|`([^`]+)`)$")


def lies_auftrag():
    zeilen = AUFTRAG.read_text(encoding="utf-8").split("\n")
    abschnitte, cur, zaun = [], None, False
    for z in zeilen:
        if not zaun and z.startswith("```"):
            zaun = True
        elif zaun and z == "```":
            zaun = False
        elif not zaun:
            m = RE_KOPF.match(z)
            if m:
                cur = {"nr": m.group(1), "zeilen": []}
                abschnitte.append(cur)
                continue
            if re.match(r"^#{1,4} ", z):
                cur = None
                continue
        if cur is not None:
            cur["zeilen"].append(z)
    eintraege = []
    for a in abschnitte:
        e = {"nr": a["nr"], "datei": None, "anker": None, "art": None, "form": None,
             "pruef": [], "text": None}
        zl = a["zeilen"]
        i = 0
        while i < len(zl):
            z = zl[i]
            if m := RE_DATEI.match(z):
                e["datei"] = m.group(1)
            elif m := RE_ANKER.match(z):
                e["anker"] = m.group(1) if m.group(1) is not None else m.group(2)
                e["art"] = m.group(3)
            elif m := RE_FORM.match(z):
                e["form"] = m.group(1)
            elif m := RE_PRUEF.match(z):
                e["pruef"].append(m.group(1) if m.group(1) is not None else m.group(2))
            elif z == "```" and e["text"] is None:
                k = zl.index("```", i + 1)
                e["text"] = zl[i + 1:k]
                i = k
            i += 1
        eintraege.append(e)
    E = [e for e in eintraege if e["nr"].startswith("E")]
    S = [e for e in eintraege if e["nr"].startswith("S")]
    J = [e for e in eintraege if e["nr"].startswith("J")]
    # Sollwerte: der json-Block unter "### Sollwerte (maschinenlesbar)"
    i = zeilen.index("### Sollwerte (maschinenlesbar)")
    a = next(k for k in range(i + 1, len(zeilen)) if zeilen[k] == "```json")
    b = next(k for k in range(a + 1, len(zeilen)) if zeilen[k] == "```")
    soll = json.loads("\n".join(zeilen[a + 1:b]))
    for e in E:
        if None in (e["datei"], e["anker"], e["art"], e["form"], e["text"]):
            sys.exit(f"{e['nr']}: Abschnitt unvollständig gelesen")
    for e in S:
        if e["datei"] is None or not e["pruef"]:
            sys.exit(f"{e['nr']}: Prüfung unvollständig gelesen")
    if [e["nr"] for e in E] != [f"E{n}" for n in range(1, soll["einfuegungen"] + 1)]:
        sys.exit(f"Einfügungen nicht wie Soll gelesen: {[e['nr'] for e in E]}")
    if [e["nr"] for e in S] != [f"S{n}" for n in range(1, soll["pruefungen"] + 1)]:
        sys.exit(f"Prüfungen nicht wie Soll gelesen: {[e['nr'] for e in S]}")
    if [e["nr"] for e in J] != ["J1"] or J[0]["text"] is None:
        sys.exit("J1 nicht gelesen")
    return E, S, J[0], soll


def schreibe(name, kopf, zeilen):
    BELEG.mkdir(parents=True, exist_ok=True)
    pfad = BELEG / name
    text = kopf + "\n" + "\n".join(zeilen) + "\n"
    pfad.write_text(text, encoding="utf-8")
    assert pfad.read_text(encoding="utf-8") == text, f"{pfad}: Rücklesen ungleich"
    print(text, end="")


def sperrliste(soll):
    """Zieldateien gegen die Sperrliste: Register Abschnitt 10 und ARBEITSWEISE-Tabelle."""
    aus, treffer = [], 0
    reg = Path(soll["sperrliste"]["register"]).read_text(encoding="utf-8")
    a = reg.index("\n## 10. Die Sperrliste\n")
    b = reg.index("\n## ", a + 5)
    abschnitt10 = reg[a:b]
    aw = Path("docs/projektfuehrung/ARBEITSWEISE.md").read_text(encoding="utf-8")
    c = aw.index(soll["sperrliste"]["arbeitsweise_kopf"])
    d = aw.index("\n\n", aw.index("| Datei | seit |", c))
    tabelle = aw[c:d]
    for name in soll["sperrliste"]["suchworte"]:
        n10, nt = abschnitt10.count(name), tabelle.count(name)
        treffer += n10 + nt
        aus.append(f"Sperrliste · {name!r} · Register Abschnitt 10 ({abschnitt10.count(chr(10))} Zeilen) {n10} · "
                   f"ARBEITSWEISE-Tabelle ({tabelle.count(chr(10)) + 1} Zeilen) {nt}")
    return aus, treffer


def ankerzeilen(inhalt, anker):
    return [n for n, z in enumerate(inhalt.split("\n")) if anker in z]


def einsetzen(inhalt, e):
    zeilen = inhalt.split("\n")
    n = ankerzeilen(inhalt, e["anker"])[0]
    block = list(e["text"])
    if e["form"] == "Block":
        if e["art"] == "nach der Zeile":
            vor = [] if zeilen[n] == "" else [""]
            nach = [] if n + 1 < len(zeilen) and zeilen[n + 1] == "" else [""]
            zeilen[n + 1:n + 1] = vor + block + nach
        else:
            vor = [] if n > 0 and zeilen[n - 1] == "" else [""]
            nach = [] if zeilen[n] == "" else [""]
            zeilen[n:n] = vor + block + nach
    else:
        if e["art"] == "nach der Zeile":
            zeilen[n + 1:n + 1] = block
        else:
            zeilen[n:n] = block
    return "\n".join(zeilen), n + 1


def probe_zeilen(E, S, soll, inhalte):
    aus, gut = [], True
    alle_texte = "\n".join("\n".join(e["text"]) for e in E)
    for e in E:
        inh = inhalte[e["datei"]]
        vorher = inh.count(e["anker"])
        az = ankerzeilen(inh, e["anker"])
        schon = inh.count(e["text"][0])
        im_text = alle_texte.count(e["anker"])
        ok = vorher == 1 and len(az) == 1 and schon == 0 and im_text == 0
        gut &= ok
        aus.append(f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · Ankerzeile "
                   f"{az[0] + 1 if len(az) == 1 else az} · Art {e['art']} · Form {e['form']} · "
                   f"Textzeilen {len(e['text'])} · erste Textzeile schon {schon} · Anker in neuen Texten {im_text} · "
                   f"{'ok' if ok else 'ABWEICHUNG'}")
    for s in S:
        inh = inhalte[s["datei"]]
        for p in s["pruef"]:
            c = inh.count(p)
            gut &= c == 1
            aus.append(f"{s['nr']} · {s['datei']} · Prüfanker {p[:60]!r} · {c} · {'ok' if c == 1 else 'ABWEICHUNG'}")
    return aus, gut


def main():
    arg = sys.argv[1:]
    if not arg:
        sys.exit(__doc__)
    modus = arg[0]
    E, S, J1, soll = lies_auftrag()
    dateien = sorted({e["datei"] for e in E} | {s["datei"] for s in S})
    inhalte = {d: Path(d).read_text(encoding="utf-8") for d in dateien}

    if modus in ("probe", "einfuegen"):
        aus, gut = probe_zeilen(E, S, soll, inhalte)
        sp, treffer = sperrliste(soll)
        aus += sp
        if modus == "probe":
            aus.append(f"Einfügungen {len(E)} · Prüfungen {len(S)} · Sperrliste Treffer {treffer} · "
                       f"Gesamt: {'wie Soll' if gut and treffer == 0 else 'ABWEICHUNG'}")
            schreibe("a_probe.txt", "# TB-141 0c — Probe, nur gelesen (tb141_einfuegen.py probe)", aus)
            sys.exit(0 if gut and treffer == 0 else 1)
        if treffer:
            print("Sperrliste getroffen — nichts geschrieben"); sys.exit(2)
        if all(inhalte[e["datei"]].count(e["text"][0]) == 1 for e in E):
            print("Alle Einfügungen stehen schon — nichts geschrieben"); sys.exit(2)
        neu, aus, gut = dict(inhalte), [], True
        for e in E:
            inh = neu[e["datei"]]
            vorher = inh.count(e["anker"])
            if vorher != 1 or len(ankerzeilen(inh, e["anker"])) != 1 or inh.count(e["text"][0]) != 0:
                gut = False
                aus.append(f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · ausgeführt nein · "
                           f"Text nachher {inh.count(e['text'][0])}")
                continue
            z_vor = inh.count("\n")
            inh, az = einsetzen(inh, e)
            neu[e["datei"]] = inh
            nachher = inh.count(e["text"][0])
            gut &= nachher == 1
            aus.append(f"{e['nr']} · {e['datei']} · Anker vorher {vorher} · ausgeführt ja · "
                       f"Text nachher {nachher} · Zeilen +{inh.count(chr(10)) - z_vor}")
        for d in dateien:
            if neu[d] != inhalte[d]:
                Path(d).write_text(neu[d], encoding="utf-8")
                assert Path(d).read_text(encoding="utf-8") == neu[d]
        for d in dateien:
            aus.append(f"Datei {d} · Zeilen vorher {inhalte[d].count(chr(10))} · nachher {neu[d].count(chr(10))}")
        aus.append(f"Gesamt: {'alle ausgeführt, je genau einmal' if gut else 'ABWEICHUNG'}")
        schreibe("a_einfuegungen.txt", "# TB-141 A — Einfügungen (tb141_einfuegen.py einfuegen); "
                 "E<n> · Datei · Anker vorher · ausgeführt · Text nachher · Zeilen", aus)
        sys.exit(0 if gut else 1)

    if modus == "vergleich":
        aus, gut = [], True
        for e in E:
            ziel = inhalte[e["datei"]].encode("utf-8")
            text = "\n".join(e["text"]).encode("utf-8")
            gesamt = ziel.count(text)
            grenzen = ziel.count(b"\n" + text + b"\n")
            ok = gesamt == 1 and grenzen == 1
            if ok and e["form"] == "Block":
                ok = ziel.count(b"\n\n" + text + b"\n\n") == 1
            gut &= ok
            aus.append(f"{e['nr']} · {e['datei']} · {len(text)} Bytes · {len(e['text'])} Zeile(n) · "
                       f"Vorkommen {gesamt} · an Zeilengrenzen {grenzen} · {'GLEICH' if ok else 'ABWEICHUNG'}")
        for s in S:
            for p in s["pruef"]:
                c = inhalte[s["datei"]].count(p)
                gut &= c == 1
                aus.append(f"{s['nr']} · Prüfanker {p[:60]!r} · nachher {c} · {'ok' if c == 1 else 'ABWEICHUNG'}")
        aus.append(f"Anzahl Einfügungen: {len(E)} · Gesamt: "
                   f"{'alle zeichengleich, je genau einmal' if gut else 'ABWEICHUNG'}")
        schreibe("c3_vergleich.txt", "# TB-141 C3 — Zeichengleichheit (tb141_einfuegen.py vergleich)", aus)
        sys.exit(0 if gut else 1)

    if modus == "numstat":
        von, bis = arg[1], arg[2]
        roh = subprocess.run(["git", "diff", "--numstat", von, bis], capture_output=True, text=True, check=True).stdout
        ist = {}
        for z in roh.splitlines():
            plus, minus, pfad = z.split("\t")
            ist[pfad] = [int(plus), int(minus)]
        aus, gut = [f"roh: {z}" for z in roh.splitlines()], True
        for pfad, (p, m) in soll["numstat_a"].items():
            ok = ist.get(pfad) == [p, m]
            gut &= ok
            aus.append(f"Soll {pfad} {p}\t{m} · Ist {ist.get(pfad)} · {'gleich' if ok else 'ABWEICHUNG'}")
        fremd = [p for p in ist if p not in soll["numstat_a"] and not p.startswith(str(BELEG) + "/")]
        gut &= not fremd
        aus.append(f"weitere Dateien ausser Belegen: {fremd if fremd else 'keine'}")
        aus.append(f"Gesamt: {'wie Soll, keine entfernte Zeile' if gut else 'ABWEICHUNG'}")
        schreibe("c2_numstat.txt", f"# TB-141 C2 — git diff --numstat {von} {bis} (tb141_einfuegen.py numstat)", aus)
        sys.exit(0 if gut else 1)

    if modus in ("journal", "j1", "j1vergleich"):
        k = arg[arg.index("--kennung") + 1]
        probe = "--probe" in arg
        j = JOURNAL.read_text(encoding="utf-8")
        kopf = f"## {k} — TB-141"
        if modus == "journal":
            block = Path(arg[arg.index("--block") + 1]).read_text(encoding="utf-8").rstrip("\n")
            bed = [("Ankertext genau 1", j.count(JANKER) == 1),
                   (f"Kopfzeile {kopf!r} im Journal noch 0", j.count("\n" + kopf) == 0),
                   ("Block beginnt mit der Kopfzeile", block.startswith(kopf)),
                   ("Block hat genau einen Absatz **Quelle:**", block.count("\n**Quelle:**") == 1),
                   ("Block hat genau eine Zeile ### Was gemessen ist", (block + "\n").count("\n### Was gemessen ist\n") == 1),
                   ("Block ohne Trennstrich und ohne J1", "\n---\n" not in block and J1["text"][0] not in block)]
            aus = [f"{t} · {'ja' if ok else 'NEIN'}" for t, ok in bed]
            if not all(ok for _, ok in bed):
                schreibe("d2_journal_abgewiesen.txt", "# TB-141 D2 — Journalblock (tb141_einfuegen.py journal), abgewiesen, nichts geschrieben", aus)
                sys.exit(2)
            neu = j.replace(JANKER, "\n---\n\n" + block + "\n\n---\n\n## Wiederkehrende Lehren\n")
            aus.append(f"Zeilen Journal vorher {j.count(chr(10))} · nachher {neu.count(chr(10))} · "
                       f"{'Probe, nichts geschrieben' if probe else 'geschrieben'}")
            if not probe:
                JOURNAL.write_text(neu, encoding="utf-8")
                assert JOURNAL.read_text(encoding="utf-8") == neu
            schreibe("d2_journal_probe.txt" if probe else "d2_journal.txt", "# TB-141 D2 — Journalblock (tb141_einfuegen.py journal"
                     + (" --probe)" if probe else ")"), aus)
            sys.exit(0)
        a = j.find("\n" + kopf)
        b = j.find(JANKER, a + 1)
        blk = j[a + 1:b] if a >= 0 and b > a else ""
        bz = blk.split("\n")
        q = [n for n, z in enumerate(bz) if z.startswith("**Quelle:**")]
        w = [n for n, z in enumerate(bz) if z == "### Was gemessen ist"]
        text = "\n".join(J1["text"])
        if modus == "j1":
            bed = [("Ankertext genau 1", j.count(JANKER) == 1),
                   (f"Kopfzeile {kopf!r} genau 1, vor dem Ankertext", j.count("\n" + kopf) == 1 and 0 <= a < b),
                   ("im Block genau ein **Quelle:** und genau ein ### Was gemessen ist, in dieser Folge",
                    len(q) == 1 and len(w) == 1 and q[0] < w[0]),
                   ("erste Zeile von J1 im Journal noch 0", j.count(J1["text"][0]) == 0)]
            aus = [f"{t} · {'ja' if ok else 'NEIN'}" for t, ok in bed]
            if not all(ok for _, ok in bed):
                schreibe("d2_j1_abgewiesen.txt", "# TB-141 D2 — J1 (tb141_einfuegen.py j1), abgewiesen, nichts geschrieben", aus)
                sys.exit(2)
            p = w[0]
            einsatz = J1["text"] + [""] if bz[p - 1] == "" else [""] + J1["text"] + [""]
            bz[p:p] = einsatz
            neu = j[:a + 1] + "\n".join(bz) + j[b:]
            aus.append(f"J1 · {JOURNAL} · Block {k} · Textzeilen {len(J1['text'])} · Zeilen +{neu.count(chr(10)) - j.count(chr(10))} · "
                       f"{'Probe, nichts geschrieben' if probe else 'eingesetzt'}")
            if not probe:
                JOURNAL.write_text(neu, encoding="utf-8")
                assert JOURNAL.read_text(encoding="utf-8") == neu
            schreibe("d2_j1_probe.txt" if probe else "d2_j1.txt", "# TB-141 D2 — J1 (tb141_einfuegen.py j1"
                     + (" --probe)" if probe else ")"), aus)
            sys.exit(0)
        gesamt = j.count(text)
        grenzen = j.count("\n" + text + "\n")
        im_block = text in blk and (len(w) == 1 and blk.find(text) < blk.find("\n### Was gemessen ist\n"))
        ok = gesamt == 1 and grenzen == 1 and im_block
        aus = [f"J1 · {JOURNAL} · {len(text.encode('utf-8'))} Bytes · {len(J1['text'])} Zeile(n) · Vorkommen {gesamt} · "
               f"an Zeilengrenzen {grenzen} · im Block {k} vor ### Was gemessen ist {'ja' if im_block else 'nein'} · "
               f"{'GLEICH' if ok else 'ABWEICHUNG'}"]
        schreibe("d2_j1_vergleich.txt", "# TB-141 D2 — J1 Zeichengleichheit (tb141_einfuegen.py j1vergleich)", aus)
        sys.exit(0 if ok else 1)
    sys.exit(f"unbekannter Modus {modus!r}")


if __name__ == "__main__":
    main()
```

### Sollwerte (maschinenlesbar)

```json
{
 "einfuegungen": 26,
 "pruefungen": 4,
 "numstat_a": {
  "docs/projektfuehrung/ARBEITSWEISE.md": [
   58,
   0
  ],
  "docs/projektfuehrung/BACKLOG.md": [
   13,
   0
  ]
 },
 "sperrliste": {
  "register": "docs/VORREGISTRIERUNG_neuselektion.md",
  "arbeitsweise_kopf": "**Die Sperrliste, Stand 18.09.2026**",
  "suchworte": [
   "projektfuehrung",
   "ARBEITSWEISE",
   "BACKLOG",
   "JOURNAL",
   "docs/"
  ]
 }
}
```
