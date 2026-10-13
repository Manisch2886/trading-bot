# Ergebnis TB-157 — Regelwerk-Nachtrag 13.10.2026 und Nachtrag zum Ergebnis TB-156

**Stand:** 13.10.2026, 16:36 (aus `date`) · **Sitzung:** Mac, Claude Code, Opus 5.5 · **Auftrag:** `docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md` · **Ausgang:** HEAD `d9a05fbcd729f67a39a006291a7543fecc7b6257`
**Commits:** ⟨S0⟩ `0f2664ee65c23fea7a63824d050da7c9249bf109` (Schritt 0) · ⟨E⟩ `18fb519f335f5db1babaf0a32114e6cdd5090d08` (32 Stücke) · ⟨F⟩ „TB-157 Abgabe: Ergebnis, Journal ET“ (dieser Commit) · danach „TB-157 F: porcelain und numstat nach der Abgabe“.
Kein Abbruch. Kein Aufruf wurde abgelehnt, keine Bestätigung verlangt.

## Kurz

| Schritt | Soll | Ist |
|---|---|---|
| 0a | HEAD `d9a05fb`, genau 4 Einträge | HEAD `d9a05fb…6257`, die 4 Einträge — **gleich** |
| 0a Werkzeug | sha256 `d3148fcf…becd8d31d` | `d3148fcf9472949231928401ac96f5f58e1b96c1934bc89ec599fc4becd8d31d` — **gleich**; Kopie im Belegordner ebenso; `cmp` 0a gleich |
| 0b | ARBEITSWEISE 2574 / `7e95d77a…`, UMZUG 439 / `5694ef86…`, BACKLOG 488 / `b55d5992…`, LIESMICH 402 / `011b0a97…`, Ergebnis TB-156 54 / `56beb22e…` | alle fünf **gleich**; UEBERGABE 4019 Z., `d2c799505b73a032d815fc973c5aced8` (Soll für F) |
| E probe | 32 Zeilen `ok`, je Datei `gleich`, 32 Stücke / 45 Zeilen, rc 0 | so, rc 0 |
| E einfuegen | dieselben Zeilen, je Datei zurückgelesen `gleich`, rc 0 | so (32 Stückzeilen identisch mit der Probe), rc 0 |
| E vergleich | 32 × `Vorkommen 1 · GLEICH`, rc 0 | 32, rc 0 |
| E zweiter Lauf | `ABGEWIESEN …` mit 32 Kennungen, rc 2, md5 gleich | so, rc 2, alle fünf md5 vorher = nachher |
| E numstat ⟨S0⟩..⟨E⟩ | 27/0, 2/0, 9/1, 1/1, 8/0; keine weiteren Dateien; rc 0 | so, rc 0 |
| J probe | 9 × `ja`, ET, `Zeilen +21` (Block 18 Z. + 3), rc 0 | so, rc 0 |
| J journal | wie Probe, geschrieben und zurückgelesen | so, `JOURNAL.md` md5 `84b2246ef95ad1616b1ded56287b3ae9` · gleich, rc 0 |
| F vergleich | wie E | 32 × GLEICH, rc 0 (bytegleich mit `e_vergleich.txt`) |
| F UEBERGABE | gleich 0b | 4019 Z., `d2c799505b73a032d815fc973c5aced8` — **gleich** |

## Belege

Alle unter `docs/belege/TB-157/`. Gemessen mit `wc -c`, `wc -l`, `md5 -q` vor dem Commit ⟨F⟩.

| Datei | was | Befehl | Bytes | Zeilen | md5 |
|---|---|---|---|---|---|
| `0a_status.txt` | `git status --porcelain` vor allem | `git status --porcelain > "$TMPDIR/tb157_0a.txt"`, nach ⟨S0⟩ `cp` | 186 | 4 | `1045837bf2998d2812e93ec4b19a88a9` |
| `tb157_einfuegen.py` | Werkzeug aus Anhang B | Holbefehl Schritt 0a, nach ⟨S0⟩ `cp` | 10564 | 214 | `d2f44a2e271ad97f654cbdc72bb0b58f` |
| `0b_ausgang.txt` | Ausgang der Zieldateien und der UEBERGABE | Block 0b | 763 | 13 | `a28d253f0addd9ecc0f85e6ded901e85` |
| `e_probe.txt` | Probe | `PY WZ probe` | 4748 | 40 | `a2b5b29eb92473cf908734f5405b7499` |
| `e_einfuegen.txt` | Einfügen | `PY WZ einfuegen` | 5354 | 45 | `ee78aa7352b1d12485821241ab418eed` |
| `e_vergleich.txt` | Vergleich nach E | `PY WZ vergleich` | 2250 | 34 | `4e78712ca007a9c25bd136731fa1bbed` |
| `e_zweitlauf.txt` | zweiter Lauf mit md5 davor und danach | Block „Zweiter Lauf“ | 5252 | 44 | `cacdb99d6bf0f6b06ff3f46b86a2036a` |
| `e_numstat.txt` | numstat ⟨S0⟩..⟨E⟩ | `PY WZ numstat ⟨S0⟩ ⟨E⟩` | 909 | 19 | `9949474e9b2471373c0b9af431f7e9e5` |
| `j_block.md` | Journalblock ET | Schreibwerkzeug von Claude Code | 2240 | 18 | `02a128fc6545912401edcff39fff88f3` |
| `j_journal_probe.txt` | Journal, Probe | `PY WZ journal … --probe` | 380 | 13 | `46c62ca7416795566c06690cd1a83fc6` |
| `j_journal.txt` | Journal, geschrieben | `PY WZ journal …` | 468 | 13 | `225de7c60f6cd270c4a547ed699b3f52` |
| `f_vergleich.txt` | Vergleich in F | `PY WZ vergleich` | 2250 | 34 | `4e78712ca007a9c25bd136731fa1bbed` |
| `f_uebergabe.txt` | UEBERGABE in F | `{ wc -l …; md5 …; }` | 118 | 2 | `e8f58ce90600a292af456af0d94f69fc` |

## Ersetzungen

Je genau eine Zeile; entfernt und eingefügt nur der Pfad `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md` → `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md` (gelesen mit `git diff -U0 ⟨S0⟩ ⟨E⟩`).

**X1 — `docs/werkzeuge/sitzungswaechter/LIESMICH.md` Z. 30**

entfernt:

```
- **⛔ NICHT ANGEMELDET (TB-<Nr>)** (Rückgabewert 6) oder **⛔ API-ABRECHNUNG (TB-<Nr>)** (Rückgabewert 7) statt „⭐ EINGABEBEREIT“, wenn die Eingabezeile steht, das Fenster aber `Not logged in` oder `API Usage Billing` nennt (über die API liefe die Sitzung auf Rechnung statt über das Abo). Beim echten Start bleibt das Fenster offen; die Probe versucht bei jeder Rückgabe der Prüfung, ihr Fenster zu schliessen — ob es geschlossen ist oder offen bleibt, steht im Log. „Anmeldung: unklar“ bleibt „⭐ EINGABEBEREIT“. Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing` sind erschlossen, nicht gemessen (Stand: `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`).
```

eingefügt an ihrer Stelle:

```
- **⛔ NICHT ANGEMELDET (TB-<Nr>)** (Rückgabewert 6) oder **⛔ API-ABRECHNUNG (TB-<Nr>)** (Rückgabewert 7) statt „⭐ EINGABEBEREIT“, wenn die Eingabezeile steht, das Fenster aber `Not logged in` oder `API Usage Billing` nennt (über die API liefe die Sitzung auf Rechnung statt über das Abo). Beim echten Start bleibt das Fenster offen; die Probe versucht bei jeder Rückgabe der Prüfung, ihr Fenster zu schliessen — ob es geschlossen ist oder offen bleibt, steht im Log. „Anmeldung: unklar“ bleibt „⭐ EINGABEBEREIT“. Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing` sind erschlossen, nicht gemessen (Stand: `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`).
```

**X2 — `docs/projektfuehrung/BACKLOG.md` Z. 474**

entfernt:

```
- **Erschlossen, nicht gemessen (Lesarten, vorläufig):** Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing`; „Abo“ = `Claude Max`; Ablaufwarnung = Zeile mit `expire`; die Kontoregel (Merkmalliste, kein Beweis: ein Name ohne Merkmal oder ein umbrochener Mailrest bleibt stehen). Gemessenes: `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`.
```

eingefügt an ihrer Stelle:

```
- **Erschlossen, nicht gemessen (Lesarten, vorläufig):** Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing`; „Abo“ = `Claude Max`; Ablaufwarnung = Zeile mit `expire`; die Kontoregel (Merkmalliste, kein Beweis: ein Name ohne Merkmal oder ein umbrochener Mailrest bleibt stehen). Gemessenes: `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`.
```

(Die Form folgt ARBEITSWEISE Z. 662 am HEAD `d9a05fb`.)

## Abweichungen vom Auftrag

- **Kopf des Journalblocks:** Anhang C verlangt „Commits <⟨S0⟩, ⟨E⟩, ⟨F⟩>“. ⟨F⟩ ist der Commit, der den Block enthält, und kann seinen eigenen Hash nicht tragen. Der Block nennt ⟨S0⟩ `0f2664e` und ⟨E⟩ `18fb519` als Hash und ⟨F⟩ über seine Commit-Nachricht. Sonst keine.

Geprüfte Sollwerte, alle eingehalten: HEAD und vier Einträge in 0a; sha256 des Werkzeugs (geholt und kopiert); `cmp` 0a; 0b Zeilenzahl und md5 der fünf Zieldateien; Probe (32 Stücke, 45 Zeilen, Bilanz je Datei, rc 0); Einfügen (rc 0, zurückgelesen gleich); Vergleich in E und F (32 × 1, rc 0); zweiter Lauf (rc 2, 32 Kennungen, md5 unverändert); numstat ⟨S0⟩..⟨E⟩ (rc 0, keine weiteren Dateien); Journal-Probe und -Einfügen (9 × ja, ET, +21, rc 0); UEBERGABE in F gleich 0b. `f_porcelain.txt` und `f_numstat.txt` entstehen nach ⟨F⟩ und stehen in der Schlussmeldung.

## Nicht getan

- Eröffnung Punkt 6 und der Helferauftrag zum Umzug (Chatname, Nachzug laut UEBERGABE Z. 3790) — macht der steuernde Chat.
- Eröffnung Punkt 9 (d) bis auf den Satz mit der Bündelung (P9d).
- Die Formhinweise der Abnahmen TB-151 und TB-152 und „(o) E10“ — nur als offener Posten in B1.
- ABN156 B1, B2, B3, B5.
- Die Probe des Wächters (`pgrep -a`) — eigener Auftrag, offen.

## Rückfragen

Keine.

## In einfacher Sprache

Die Fehler Nr. 55 bis 73, die Regeln des Betreibers vom 11.10.2026, die neue Form des Chatnamens („Opus Trading Bot-TT.MM.JJJJ“) und die Lehre, dass `pgrep` ohne `-a` die eigene Sitzung nicht sieht, stehen jetzt im Regelwerk, nicht mehr nur in der Übergabe. Das Ergebnis von TB-156 hat einen Nachtrag bekommen, der die falsche Begründung richtigstellt. Zwei Verweise auf eine Datei, die es nie gab, zeigen jetzt auf die richtige. Alles lief mit dem vorgegebenen Werkzeug; jede Zahl stimmte mit dem Soll überein, nichts wurde von Hand eingefügt.
