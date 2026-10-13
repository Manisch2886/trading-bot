# TB-157 Regelwerk-Nachtrag 13.10.2026 und Nachtrag zum Ergebnis TB-156 — an: Mac-Sitzung (Claude Code) — 32 Stücke

**Stand: Entwurf vom 13.10.2026, 16:29** (Helfer BAU157, per Skript aus Bausteinen, `$HOME/sc/tb157/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; alle Schritte an einer Kopie simuliert. Urteil und Freigabe liegen beim steuernden Chat; zwei frische Gegenleser sind Pflicht. **Gebaut am HEAD `d9a05fb`.**

**Sitzungstitel:** `TB-157` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `d9a05fbcd729f67a39a006291a7543fecc7b6257` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-157`), nicht von Hand.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), unten kurz `PY`; das Werkzeug `docs/belege/TB-157/tb157_einfuegen.py` (Anhang B) kurz `WZ`. **Belege:** `docs/belege/TB-157/`. **Ergebnis:** `docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md`. **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15); ein Abbruchkriterium führt zu Abbruch und Meldung, nicht zu einer Rückfrage.
**Ziel:** (a) Nachtrag zum Ergebnis TB-156 (Abnahme ABN156: A1, A2, B4; die Ursache `pgrep`) und die Berichtigung des Verweises auf das nicht vorhandene `ERGEBNIS_TB-155_…` in `LIESMICH.md` und `BACKLOG.md`. (b) Regelwerk-Nachtrag 11.–13.10.2026: Fehler Nr. 55 bis 73, die neue Form des Chatnamens, die Regeln des Betreibers vom 11.10.2026 (Eröffnung Punkt 9), die Lehre zu `pgrep`; ein Block im Backlog; der Journalblock der Sitzung.
**Bauart:** Dokumentationsauftrag (ARBEITSWEISE 5b): Text wörtlich mit Ankertext, nur `docs/`, `numstat` je Datei, `porcelain` nach dem letzten Commit. Vorbild gleicher Bauart: `docs/auftraege/MAC_TB-152_regelwerk_nachtrag_1010.md`; bei Widerspruch gilt dieser Auftrag, und es gelten nur die Schritte, die hier stehen. **Anders als in TB-152:** Das Werkzeug steht ganz in Anhang B (keine Ableitung); es gibt zwei Ersetzungen (X1, X2: je eine Zeile, numstat `1	1`) und einen Block am Dateiende (E1); kein Schritt A (Modus) — `ps -o command` liest Kommandozeilen, was ABN156 A2 rügt.
**Reihenfolge:** Schritt 0 → E (Einfügen, Commit) → J (Journalblock) → F (Nachweis, Ergebnis, Abgabe). **Jede Datei, die die Sitzung schreibt, entsteht mit dem Befehl aus dem Anhang „Dateien und ihre Befehle“** — kein anderer Weg.

## ⭐ Freigabe

**Handwerk ohne Sperrlistennähe, pauschal frei (Betreiber 26.09.2026)** — der Auftrag fügt nur Dokumentation ein und ersetzt zwei Verweise; kein Programm wird geändert. Kein Programm ausserhalb des Repos (kein `osascript`, `launchctl`, `kill`).

**Die Sitzung darf ändern, und nichts sonst:**

| Zieldatei | Stücke | numstat-Soll (+ / −) |
|---|---|---|
| `docs/projektfuehrung/ARBEITSWEISE.md` | F55, F56, F57, F58, F59, F60, F61, F62, F63, F64, F65, F66, F67, F68, F69, F70, F71, F72, F73, L1, C1, P9a, P9b, P9c, P9e, P9f, P9d | **27 / 0** |
| `docs/projektfuehrung/UMZUG.md` | U1 | **2 / 0** |
| `docs/projektfuehrung/BACKLOG.md` | X2, B1 | **9 / 1** |
| `docs/werkzeuge/sitzungswaechter/LIESMICH.md` | X1 | **1 / 1** |
| `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md` | E1 | **8 / 0** |
| `docs/projektfuehrung/JOURNAL.md` | Block der Sitzung (Schritt J) | Zeilen des Blocks + 3 / 0 |
| neu: `docs/belege/TB-157/…`, `docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md` | Belege, Werkzeug, Ergebnis | — |

In den Zieldateien wird **nur eingefügt,** ausser X1 und X2 (je genau eine Zeile, nur der Pfad). Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt; das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** jede andere Datei unter `docs/werkzeuge/`; `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` nach Schritt 0; Register und Registerkopie; `research/`, `shared/`, `strategies/`; frühere Belegordner; den Wortlaut eines Stücks umformulieren, kürzen oder zusammenlegen (Sachfehler: melden, nicht berichtigen). Nie `git add -A`, nie `git add .`; jeder Commit nennt seine Dateien mit Namen.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD `d9a05fb` gemessen, Helfer BAU157, 13.10.2026, 16:29): Ausgang der Zieldateien wie in 0b; jeder Anker trifft am HEAD genau eine Zeile (Anhang A, „Am HEAD“). Letzte Journalkennung ES; vor `## Wiederkehrende Lehren` stehen `---` und eine Leerzeile. `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md` fehlt, `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md` ist verfolgt.
- **Lage nach dem Auslegen** (vom steuernden Chat): `docs/auftraege/AKTUELLER_AUFTRAG.md` zeigt auf TB-157 (geändert), dieser Auftrag liegt unverfolgt im Arbeitsbaum, `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` sind geändert. Das ist das Soll von 0a.
- **Wortlaute:** Betreibersätze und Fehlertexte per Skript aus `UEBERGABE.md` und `EROEFFNUNG_STEUERNDER_CHAT.md` im Arbeitsbaum (die Fassung, die Schritt 0 committet); A1, A2, B4 aus dem Abnahmebericht ABN156 (nicht im Repo). Vorgaben des steuernden Chats stehen als „Lesart des steuernden Chats, vorläufig“.
- **Offen — misst die Sitzung, nie raten:** Stand der `UEBERGABE.md` beim Start (kein Sollwert) · Kennung des Journalblocks (erwartet ET).
- **Simulation des Helfers** (Kopie als eigenes git-Repo; Linux, Python 3.10, Werkzeug mit `ast.parse(feature_version=(3,9))` geprüft): alle Befehle dieses Auftrags der Reihe nach; Ergebnis im Bericht BAU157.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-157/` entsteht:** `git status --porcelain > "$TMPDIR/tb157_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `d9a05fbcd729f67a39a006291a7543fecc7b6257` und genau diese 4 Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md
```

Dann das Werkzeug aus Anhang B holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md "$TMPDIR/tb157_einfuegen.py" <<'EOF2'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
a = z.index("```python", z.index("### Werkzeug"))
t = "\n".join(z[a + 1:z.index("```", a + 1)]) + "\n"
open(sys.argv[2], "w", encoding="utf-8").write(t)
print("tb157_einfuegen.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF2
```

Soll: `tb157_einfuegen.py d3148fcf9472949231928401ac96f5f58e1b96c1934bc89ec599fc4becd8d31d`; sonst **ABBRUCH** (vor ⟨S0⟩: nur melden, siehe Abbruchweg). Commit `TB-157 Schritt 0: Stand des steuernden Chats vor TB-157` mit genau den vier Pfaden aus 0a (Block unten), pushen ⇒ **⟨S0⟩**. **Unmittelbar nach dem gepushten ⟨S0⟩:** `mkdir -p docs/belege/TB-157`; erst ab hier gibt es `abbruch.txt` (Abbruchweg). Dann `cp "$TMPDIR/tb157_0a.txt" docs/belege/TB-157/0a_status.txt` (`cmp` gleich), `cp "$TMPDIR/tb157_einfuegen.py" docs/belege/TB-157/tb157_einfuegen.py`, dann `shasum -a 256 docs/belege/TB-157/tb157_einfuegen.py` (Soll wie oben). **Keine Kopfdateien;** an ihre Stelle tritt die Tabelle „Belege“ im Ergebnis.

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md
```

**0b. Ausgang** ⇒ `0b_ausgang.txt`, Befehl:

```
{ wc -l docs/projektfuehrung/ARBEITSWEISE.md docs/projektfuehrung/UMZUG.md docs/projektfuehrung/BACKLOG.md docs/werkzeuge/sitzungswaechter/LIESMICH.md docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md docs/projektfuehrung/UEBERGABE.md; md5 docs/projektfuehrung/ARBEITSWEISE.md docs/projektfuehrung/UMZUG.md docs/projektfuehrung/BACKLOG.md docs/werkzeuge/sitzungswaechter/LIESMICH.md docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md docs/projektfuehrung/UEBERGABE.md; } > docs/belege/TB-157/0b_ausgang.txt
```

Soll (am Bau-HEAD `d9a05fb`): `ARBEITSWEISE.md` 2574 Z., `7e95d77a7a85126314c7bcb922303cc0` · `UMZUG.md` 439 Z., `5694ef86f45ce8527642bf8c614626a9` · `BACKLOG.md` 488 Z., `b55d5992a7b88ff36da120ce80b1bd00` · `LIESMICH.md` 402 Z., `011b0a9759b2e774deb850d2211a395c` · `ERGEBNIS_TB-156_waechter_fensterinhalt.md` 54 Z., `56beb22e19d73ca77e89aa70aed4477b`. Weicht eine ab: vermerken; die Anker entscheiden (Schritt E). `UEBERGABE.md` hat hier keinen festen Sollwert (sie wächst bis zum Start); der in 0b gemessene Wert ist das Soll für Schritt F — nach Schritt 0 ändert die Sitzung sie nicht.

## Verfahren je Stück

Jedes Stück in Anhang A nennt Zieldatei, Art, Form und Anker; sein Text steht wörtlich zwischen zwei Zeilen `~~~`. **Anker:** ein Teil genau einer Zeile der Zieldatei (zwischen ⟦ und ⟧). **Art:** `nach` oder `vor` dieser Zeile; `ende` = am Dateiende; `ersetzen` = in der Ankerzeile genau einmal `Alt` durch `Neu` (sonst nichts an der Zeile). **Form `Zeilen`:** ohne Leerzeile direkt an der Ankerzeile (eine Tabellenzeile bleibt in ihrer Tabelle). **Form `Block`:** genau eine Leerzeile davor und danach, keine verdoppelt. Haben mehrere Stücke denselben Anker, setzt das Werkzeug sie in der Reihenfolge von Anhang A hinter (oder vor) die Ankerzeile. Die Grenze eines Stücks ist allein die Zeile `~~~`. **`[ ]` in einem Stücktext = Einfügung des steuernden Chats, sonst wörtlich** (so in F67 und F70; F55 und F70 beginnen klein, weil der Regeltext der Quelle nach „⇒“ so beginnt).

## Schritt E — Einfügen mit dem Werkzeug

**Probe.** `PY WZ probe > docs/belege/TB-157/e_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/e_probe.txt`. Soll: 32 Zeilen `<Id> · <Datei> · Anker Z. <n> · … · ok`, je Datei `Soll … · Ist … · gleich`, `Stuecke 32 · eingefuegte Zeilen 45`, `Gesamt: wie Soll, nichts geschrieben (Probe)`, `rc 0`. rc ≠ 0 ⇒ **ABBRUCH** (rc 3: die Zeilen `ABBRUCH: …` nennen den Grund; rc 64: falscher Aufruf).

**Einfügen.** `PY WZ einfuegen > docs/belege/TB-157/e_einfuegen.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/e_einfuegen.txt`. Soll: dieselben Zeilen wie in der Probe, je Datei `geschrieben und zurueckgelesen: … · gleich`, `Gesamt: wie Soll, alle eingefuegt, je genau einmal`, `rc 0`. Das Werkzeug prüft alles, bevor es schreibt; endet es mit `ABGEWIESEN, nichts geschrieben`, ist keine Zieldatei geändert. rc ≠ 0 ⇒ **ABBRUCH**.

**Vergleich.** `PY WZ vergleich > docs/belege/TB-157/e_vergleich.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/e_vergleich.txt`. Soll: 32 Zeilen `… · Vorkommen 1 · GLEICH`, `Gesamt: alle zeichengleich, je genau einmal`, `rc 0`.

**Zweiter Lauf.** Befehl:

```
{ md5 docs/projektfuehrung/ARBEITSWEISE.md docs/projektfuehrung/UMZUG.md docs/projektfuehrung/BACKLOG.md docs/werkzeuge/sitzungswaechter/LIESMICH.md docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md; PY WZ einfuegen; echo "rc $?"; md5 docs/projektfuehrung/ARBEITSWEISE.md docs/projektfuehrung/UMZUG.md docs/projektfuehrung/BACKLOG.md docs/werkzeuge/sitzungswaechter/LIESMICH.md docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md; } > docs/belege/TB-157/e_zweitlauf.txt 2>&1
```

Soll: `ABGEWIESEN, nichts geschrieben: schon eingefuegt: …` mit allen 32 Kennungen, `rc 2`, md5 je Datei vorher und nachher gleich. Sonst **ABBRUCH**.

Commit `TB-157 E: Regelwerk-Nachtrag 13.10.2026 und Nachtrag TB-156, 32 Stücke` (Block unten), pushen ⇒ **⟨E⟩**.

```
git add docs/projektfuehrung/ARBEITSWEISE.md
git add docs/projektfuehrung/UMZUG.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/werkzeuge/sitzungswaechter/LIESMICH.md
git add docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md
git add docs/belege/TB-157/0a_status.txt
git add docs/belege/TB-157/tb157_einfuegen.py
git add docs/belege/TB-157/0b_ausgang.txt
git add docs/belege/TB-157/e_probe.txt
git add docs/belege/TB-157/e_einfuegen.txt
git add docs/belege/TB-157/e_vergleich.txt
git add docs/belege/TB-157/e_zweitlauf.txt
```

**Numstat.** `PY WZ numstat ⟨S0⟩ ⟨E⟩ > docs/belege/TB-157/e_numstat.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/e_numstat.txt` (⟨S0⟩ und ⟨E⟩ als Hash). Soll: die Zeilen `Soll … · gleich` wie die Tabelle unter „Freigabe“, `weitere Dateien ausser Belegen, Auftrag und Ergebnis: keine`, `rc 0`. rc 1 ⇒ melden; **keine Zeile von Hand richten.**

## Schritt J — Journalblock

Die Sitzung schreibt ihren Block nach `docs/belege/TB-157/j_block.md` (Gliederung und feste Teile: Anhang C; was TB-157 selbst tat, in eigenen Worten). Dann `PY WZ journal docs/belege/TB-157/j_block.md --probe > docs/belege/TB-157/j_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/j_journal_probe.txt` und ohne `--probe` nach `j_journal.txt` (gleiche Form). Soll: neun Bedingungen `ja`, `Kennung ET (erwartet ET)`, `Zeilen +<n>` mit n = Zeilen des Blocks + 3, `rc 0`. **Rückgabewerte von `journal`** (wie im Werkzeug): 0 gut · 2 eine Bedingung `NEIN` — die Bedingung lesen, den Block richten, neu, kein Abbruch · 64 falscher Aufruf — **ABBRUCH** · eine Python-Ausnahme (Traceback, rc 1) — **ABBRUCH**. Nennt das Werkzeug eine andere Kennung: diese in den Block, melden.

## Schritt F — Nachweis, Ergebnis, Abgabe

**Nachweis.** `PY WZ vergleich > docs/belege/TB-157/f_vergleich.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/f_vergleich.txt` (Soll wie in E). `{ wc -l docs/projektfuehrung/UEBERGABE.md; md5 docs/projektfuehrung/UEBERGABE.md; } > docs/belege/TB-157/f_uebergabe.txt`; Soll: gleich dem in 0b gemessenen Wert.

**Ergebnis** `docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md` (mit dem Schreibwerkzeug von Claude Code): Kopf (Stand, Commits, ⟨S0⟩) · „Kurz“ (Schritt · Soll · Ist) · „Belege“ (Datei · was · Befehl · Bytes · Zeilen · md5; `f_porcelain.txt` und `f_numstat.txt` entstehen erst nach ⟨F⟩ und stehen nicht in dieser Tabelle) · „Ersetzungen“ (für X1 und X2 je die entfernte und die eingefügte Zeile, jede entfernte Zeile einzeln ihrer Ersetzung zugeordnet; ARBEITSWEISE Z. 662 am HEAD `d9a05fb`) · „Abweichungen vom Auftrag“ (jede; sonst „keine“ mit der Liste der geprüften Sollwerte) · „Nicht getan“ (die Posten unter „Nicht in TB-157“) · „Rückfragen“ (keine, oder wörtlich) · „In einfacher Sprache“.

**Abgabe.** Commit `TB-157 Abgabe: Ergebnis, Journal <Kennung>` (erster Block unten), pushen ⇒ **⟨F⟩**. Dann `git status --porcelain > "$TMPDIR/tb157_f.txt"`, `cp "$TMPDIR/tb157_f.txt" docs/belege/TB-157/f_porcelain.txt` (`cmp` gleich; Soll 0 B), erst danach `PY WZ numstat ⟨S0⟩ ⟨F⟩ docs/belege/TB-157/j_block.md > docs/belege/TB-157/f_numstat.txt 2>&1; echo "rc $?" >> docs/belege/TB-157/f_numstat.txt`. Soll `rc 0`: die Dateien wie in E, `JOURNAL.md` mit n aus Schritt J und 0 entfernten Zeilen. Letzter Commit `TB-157 F: porcelain und numstat nach der Abgabe` (zweiter Block unten), pushen. **Danach** `git status --porcelain` noch einmal (genau dieser Befehl, keine Datei); die Rohausgabe steht wörtlich in der Schlussmeldung an den Betreiber (Soll: leer; Vorbild TB-152, Schritt F).

```
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md
git add docs/belege/TB-157/e_numstat.txt
git add docs/belege/TB-157/j_block.md
git add docs/belege/TB-157/j_journal_probe.txt
git add docs/belege/TB-157/j_journal.txt
git add docs/belege/TB-157/f_vergleich.txt
git add docs/belege/TB-157/f_uebergabe.txt
```

```
git add docs/belege/TB-157/f_porcelain.txt
git add docs/belege/TB-157/f_numstat.txt
```

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD), oder der sha256 des Werkzeugs weicht ab.
- Schritt E: `probe` oder `einfuegen` endet mit rc ≠ 0; `vergleich` endet nicht mit rc 0; der zweite Lauf endet nicht mit rc 2 oder ändert einen md5. Kein Stück von Hand einfügen, keinen Anker anpassen.
- Schritt J: `journal` endet mit rc 64 oder mit einer Python-Ausnahme (Traceback, rc 1).
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung:** melden, nicht umgehen; verlangt schon Schritt 0 oder der Abbruchweg eine Bestätigung: nichts weiter versuchen, den Wortlaut der Frage im Chat melden.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal (gilt **nicht** für den Push des Abbruch-Commits, siehe Abbruchweg).

**Kein Abbruch:** `journal` rc 2; eine andere Kennung als ET; 0b weicht ab; `numstat` rc 1; in F weicht `vergleich`, der md5 der `UEBERGABE.md` oder `f_porcelain.txt` ab — je weiter, unter „Abweichungen“ nennen.

**Abbruchweg — so wenig schreiben wie möglich.** **Solange ⟨S0⟩ nicht gepusht ist** (0a weicht ab, der sha256 des Werkzeugs weicht ab, Commit oder Push von ⟨S0⟩ scheitert): nichts schreiben, nichts committen, nur im Chat melden (die Abweichung wörtlich). **Ab dem gepushten ⟨S0⟩** (der Ordner `docs/belege/TB-157/` steht dann): genau eine neue Datei, `printf '%s\n' "<Schritt>: <Grund, ein Satz>" > docs/belege/TB-157/abbruch.txt` (sie beschreibt sich selbst, keine Kopfdatei); dann `git add docs/belege/TB-157/abbruch.txt` und je eine Zeile `git add <Pfad>` **mit dem Namen** jeder Datei aus dem Anhang „Dateien und ihre Befehle“, die im Repo schon entstanden oder geändert und noch nicht committet ist — geschriebene Zieldateien eingeschlossen; die Meldung nennt diese Zieldateien als Erstes. Commit `TB-157 Abbruch: <Schritt>`, pushen, melden. **Scheitert der Push des Abbruch-Commits: nur melden** — kein zweiter Abbruchweg, kein neuer Commit; die Regel „`git push` scheitert zweimal“ unter den Abbruchkriterien gilt nicht für den Abbruch-Commit. Nichts zurückdrehen; die Dateien unter `$TMPDIR` bleiben liegen.

## Nicht in TB-157

- Eröffnung Punkt 6 und der Helferauftrag zum Umzug (Chatname, Nachzug laut UEBERGABE Z. 3790) — nicht im Repo-Auftrag; macht der steuernde Chat.
- Eröffnung Punkt 9 (d) bis auf den Satz mit der Bündelung (P9d) — der `jq`-Weg steht schon in ARBEITSWEISE Abschnitt 0, die zwei übrigen Sätze als Fehler Nr. 56 und 57 (F56, F57).
- Die Formhinweise der Abnahmen TB-151 und TB-152 und „(o) E10“ — nur als offener Posten in B1, nicht eingeordnet.
- ABN156 B1, B2, B3, B5 — nicht Teil von TB-157 (nur A1, A2, B4).
- Die Probe des Wächters (`pgrep -a`) — eigener Auftrag, offen.

## In einfacher Sprache

Seit dem 11.10.2026 sind Fehler, Regeln des Betreibers und eine neue Form für den Chatnamen nur in der Übergabe festgehalten. Dieser Auftrag trägt sie ins Regelwerk ein (Arbeitsweise, Umzugsanleitung, Backlog, Journal). Ausserdem bekommt das Ergebnis von TB-156 einen Nachtrag: Eine Begründung darin war falsch, und die wahre Ursache ist gefunden (`pgrep` übersieht auf dem Mac die eigene Sitzung). Zwei Verweise auf eine Datei, die es nicht gibt, werden auf die richtige Datei gesetzt. Es wird nur ergänzt; geändert werden nur diese zwei Verweise.

## Anhang — Dateien und ihre Befehle

Jede Datei, die die Sitzung schreibt, mit dem einzigen erlaubten Befehl (Einzelheiten im Schritt).

| Datei | Befehl |
|---|---|
| `docs/belege/TB-157/0a_status.txt` | `git status --porcelain > "$TMPDIR/tb157_0a.txt"`, nach ⟨S0⟩ `cp` (Schritt 0a) |
| `docs/belege/TB-157/tb157_einfuegen.py` | Holbefehl aus Schritt 0a nach `$TMPDIR`, nach ⟨S0⟩ `cp` |
| `docs/belege/TB-157/0b_ausgang.txt` | Block in Schritt 0b |
| `docs/belege/TB-157/e_probe.txt` | `PY WZ probe > …` (Schritt E) |
| `docs/belege/TB-157/e_einfuegen.txt` | `PY WZ einfuegen > …` (Schritt E) |
| `docs/belege/TB-157/e_vergleich.txt` | `PY WZ vergleich > …` (Schritt E) |
| `docs/belege/TB-157/e_zweitlauf.txt` | Block „Zweiter Lauf“ (Schritt E) |
| `docs/belege/TB-157/e_numstat.txt` | `PY WZ numstat ⟨S0⟩ ⟨E⟩ > …` (Schritt E) |
| `docs/belege/TB-157/j_block.md` | Schreibwerkzeug von Claude Code, Gliederung Anhang C (Schritt J) |
| `docs/belege/TB-157/j_journal_probe.txt` | `PY WZ journal … --probe > …` (Schritt J) |
| `docs/belege/TB-157/j_journal.txt` | `PY WZ journal … > …` (Schritt J) |
| `docs/belege/TB-157/f_vergleich.txt` | `PY WZ vergleich > …` (Schritt F) |
| `docs/belege/TB-157/f_uebergabe.txt` | `{ wc -l …; md5 …; } > …` (Schritt F) |
| `docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md` | Schreibwerkzeug von Claude Code, Gliederung Schritt F |
| `docs/belege/TB-157/f_porcelain.txt` | `git status --porcelain > "$TMPDIR/tb157_f.txt"`, dann `cp` (Schritt F) |
| `docs/belege/TB-157/f_numstat.txt` | `PY WZ numstat ⟨S0⟩ ⟨F⟩ … > …` (Schritt F) |
| `docs/belege/TB-157/abbruch.txt` | nur bei Abbruch: `printf '%s\n' "…" > …` (Abbruchweg) |
| `docs/projektfuehrung/ARBEITSWEISE.md` | `PY WZ einfuegen` (Schritt E) |
| `docs/projektfuehrung/UMZUG.md` | `PY WZ einfuegen` (Schritt E) |
| `docs/projektfuehrung/BACKLOG.md` | `PY WZ einfuegen` (Schritt E) |
| `docs/werkzeuge/sitzungswaechter/LIESMICH.md` | `PY WZ einfuegen` (Schritt E) |
| `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md` | `PY WZ einfuegen` (Schritt E) |
| $TMPDIR/tb157_0a.txt, $TMPDIR/tb157_einfuegen.py, $TMPDIR/tb157_f.txt | Befehle in Schritt 0a und F; bleiben liegen — nicht löschen (`deny`: `Bash(rm:*)`), nicht committen |
| `docs/projektfuehrung/JOURNAL.md` | `PY WZ journal …` (Schritt J) |

## Anhang A — Stücke (wörtlich)

#### F55 — ARBEITSWEISE Abschnitt 0, „Immer“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschni⟧

Am HEAD `d9a05fb`: Anker Z. 60 · Quelle: UEBERGABE Z. 3613

~~~
| ☐ | an der ganzen Datei messen. (11.10.2026, Fehler Nr. 55: **Nr. 55** (im Nachtrag 01:38, Punkt ENTWURF154): „steht nur in X“ an einem Ausschnitt gemessen) | UEBERGABE, Umzug 11.10.2026, 08:54, Block 7 |
~~~

#### F56 — ARBEITSWEISE Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „gedeckt von“ den Wortlaut der Karte lesen (09.10.2026, Fehl⟧

Am HEAD `d9a05fb`: Anker Z. 154 · Quelle: UEBERGABE Z. 3641

~~~
| ☐ | Eine solche Regel geht nicht in die Träger; der steuernde Chat nennt dem Betreiber den Grund, bevor er etwas einträgt. (11.10.2026, Fehler Nr. 56: **Fehler Nr. 56:** den Satz des Betreibers in Erinnerung, Nachtrag und einen Entscheid getragen, bevor geprüft war, dass er eine Schutzabfrage durch den Chat selbst beantworten lässt) | UEBERGABE, Nachtrag 11.10.2026, 09:08 |
~~~

#### F57 — ARBEITSWEISE Abschnitt 0, „Wenn ich den Betreiber anleite“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor einer Aufgabe an den Betreiber jeden eigenen Weg versuchen (⟧

Am HEAD `d9a05fb`: Anker Z. 172 · Quelle: UEBERGABE Z. 3644

~~~
| ☐ | Vor einer Aufgabe an den Betreiber messen, ob das Werkzeug den Fall schon prüft. (11.10.2026, Fehler Nr. 57: **Fehler Nr. 57:** dem Betreiber zweimal (09:12, 09:20) „Schlüsselbund entsperren“ als Aufgabe gegeben, ohne zu messen, dass `starte_sitzung.sh` (Z. 548–549) den Schlüsselbund bei jedem Start selbst prüft und sonst abbricht; der Start 01:20 lief durch. Um 09:26 zurückgenommen) | UEBERGABE, Nachtrag 11.10.2026, 09:08 |
~~~

#### F58 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3766

~~~
| ☐ | Auch Angaben aus der Übergabe misst das Skript, das den Auftrag schreibt. (11.10.2026, Fehler Nr. 58: **Nr. 58:** Im Helferauftrag GEGEN154 standen ein Pfad (`gen/backlog_e1.txt`) und eine Zahl („sechs Punkte ‚braucht Vorprobe‘“) aus der Notizdatei des Vorgängers statt aus `ls` und Messung; der Pfad fiel vor dem Start auf (richtig: `bau/eingaben/backlog_e1.txt`), die Zahl fand der Gegenleser (acht).) | UEBERGABE, Umzug 11.10.2026, 11:58, Block 7 |
~~~

#### F59 — ARBEITSWEISE Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum g⟧

Am HEAD `d9a05fb`: Anker Z. 220 · Quelle: UEBERGABE Z. 3767

~~~
| ☐ | Handgriffe, die aufeinander aufbauen, einzeln schicken; nach einer Abweisung nichts nachschieben. (11.10.2026, Fehler Nr. 59: **Nr. 59:** Klick ins Feld und Taste Return gingen im selben Schritt an Chrome; der Klick wurde von der Erlaubnisprüfung abgewiesen, Return lief trotzdem und schickte den Satz ab (der Satz stand richtig im Feld, die Folge war die gewollte).) | UEBERGABE, Umzug 11.10.2026, 11:58, Block 7 |
~~~

#### F60 — ARBEITSWEISE Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „gedeckt von“ den Wortlaut der Karte lesen (09.10.2026, Fehl⟧

Am HEAD `d9a05fb`: Anker Z. 154 · Quelle: UEBERGABE Z. 3850

~~~
| ☐ | Eine Folge eines Entscheids erst nennen, wenn der Bau sie gemessen hat. (11.10.2026, Chat 20, Fehler Nr. 60: **Folge behauptet, bevor der Bau sie zeigte:** 12:39 dem Betreiber gesagt, eine der drei Prüfsummen ändere sich (E35 erwartete das); sie blieben gleich, das Soll von 0a steht im Daten-Block. 12:53 berichtigt.) | UEBERGABE, Umzug 11.10.2026, 14:13, Block 7 |
~~~

#### F61 — ARBEITSWEISE Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „gedeckt von“ den Wortlaut der Karte lesen (09.10.2026, Fehl⟧

Am HEAD `d9a05fb`: Anker Z. 154 · Quelle: UEBERGABE Z. 3851

~~~
| ☐ | Eine Betreiberfrage, die an nichts hängt, sofort als Karte stellen. (11.10.2026, Chat 20, Fehler Nr. 61: **Frage gebündelt, die an nichts hing:** Die Frage zu TB-155 stand ab 12:20 fest und wartete auf die Karte R90; der Betreiber fragte 12:59 nach.) | UEBERGABE, Umzug 11.10.2026, 14:13, Block 7 |
~~~

#### F62 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3852

~~~
| ☐ | Beim Start eines Helfers den nächsten Schritt als Skript vorbauen. (11.10.2026, Chat 20, Fehler Nr. 62: **Wartezeit ohne Vorbau:** Während BER154 lief, nichts vorbereitet (Betreiber 12:35).) | UEBERGABE, Umzug 11.10.2026, 14:13, Block 7 |
~~~

#### F63 — ARBEITSWEISE Abschnitt 0, „Immer“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschni⟧

Am HEAD `d9a05fb`: Anker Z. 60 · Quelle: UEBERGABE Z. 3853

~~~
| ☐ | Auch in Nachrichten an laufende Helfer keine Uhrzeit von Hand. (11.10.2026, Chat 20, Fehler Nr. 63: **Uhrzeit ohne Messung in einer Nachricht an einen Helfer:** „13:39“ genannt, die Datei trägt 13:41 (Fehler Nr. 34 und 50 in neuer Gestalt).) | UEBERGABE, Umzug 11.10.2026, 14:13, Block 7 |
~~~

#### F64 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3854

~~~
| ☐ | Ein Grössenziel sagt dazu, dass Prüfungen und Tests nicht gekürzt werden. (11.10.2026, Chat 20, Fehler Nr. 64: **Grössenziel kostete Prüfungen:** Für TB-155 waren 40 000 B gesetzt; der Bau-Helfer strich dafür 7 Testfälle und drei Prüfungen (zurückgeholt mit E10).) | UEBERGABE, Umzug 11.10.2026, 14:13, Block 7 |
~~~

#### F65 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3916

~~~
| ☐ | Jeder Beleg und jede Datei, die eine Sitzung schreiben soll, hat im Auftrag einen vorgegebenen Befehl; die Gegenleser prüfen das als eigenen Punkt. (11.–13.10.2026, Chat 21, Fehler Nr. 65: **Auftrag verlangte Kopfdateien ohne Weg:** TB-155 brach daran ab; sechs Gegenleser fanden es nicht, weil keiner danach gefragt war.) | UEBERGABE, Umzug 13.10.2026, 11:15, Block 7 |
~~~

#### F66 — ARBEITSWEISE Abschnitt 0, „Immer“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschni⟧

Am HEAD `d9a05fb`: Anker Z. 60 · Quelle: UEBERGABE Z. 3917

~~~
| ☐ | Zeilenzahlen mit `wc -l`. (11.–13.10.2026, Chat 21, Fehler Nr. 66: **Zahl im Helferauftrag falsch gemessen:** „621 Zeilen“ (Python-`split`) statt 622 (`wc -l`); vor dem Start berichtigt.) | UEBERGABE, Umzug 13.10.2026, 11:15, Block 7 |
~~~

#### F67 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3918

~~~
| ☐ | Wie Fehler [Nr. 64] im Umzug 11.10.2026, 14:13, Block 7 („Grössenziel kostete Prüfungen“): ein Grössenziel aus dem gemessenen Zuwachs ableiten. (11.–13.10.2026, Chat 21, Fehler Nr. 67: **Grössenziel ohne Messung gesetzt:** 52 000 B für TB-155 Runde 3 — der Bau endete mit rc 1, eine Runde mehr.) | UEBERGABE, Umzug 13.10.2026, 11:15, Block 7 |
~~~

#### F68 — ARBEITSWEISE Abschnitt 0, „Wenn eine Entscheidung beim Betreiber liegt“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „gedeckt von“ den Wortlaut der Karte lesen (09.10.2026, Fehl⟧

Am HEAD `d9a05fb`: Anker Z. 154 · Quelle: UEBERGABE Z. 3919

~~~
| ☐ | Bei einer Schranke aus einer Betreiberfreigabe sagt der Entscheid ausdrücklich, ob ein Verstoss Abbruch ist. (11.–13.10.2026, Chat 21, Fehler Nr. 68: **Entscheid liess Spielraum:** E12 nannte den Kontofund „Befund“; der Berichtiger strich daraufhin das Abbruchkriterium (zurückgeholt mit E23).) | UEBERGABE, Umzug 13.10.2026, 11:15, Block 7 |
~~~

#### F69 — ARBEITSWEISE Abschnitt 0, „Immer“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschni⟧

Am HEAD `d9a05fb`: Anker Z. 60 · Quelle: UEBERGABE Z. 3920

~~~
| ☐ | Datum im Dateinamen aus `date`. (11.–13.10.2026, Chat 21, Fehler Nr. 69: **Dateiname mit falschem Datum:** die Entscheide vom 13.10.2026 zuerst als `2026-10-11_…` gesichert, sofort berichtigt.) | UEBERGABE, Umzug 13.10.2026, 11:15, Block 7 |
~~~

#### F70 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3982

~~~
| ☐ | wie Block 7 vom [Umzug 13.10.2026,] 11:15: Grössenziel aus gemessenem Zuwachs. (13.10.2026, Chat 22, Fehler Nr. 70: **Grössenziel ohne Messung:** 66 000 B gesetzt, gebaut 69 490 → 73 510 B.) | UEBERGABE, Umzug 13.10.2026, 13:03, Block 7 |
~~~

#### F71 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3983

~~~
| ☐ | Im Bauauftrag die Lage nach dem Auslegen ausdrücklich nennen. (13.10.2026, Chat 22, Fehler Nr. 71: **Fehler im eigenen Entwurf erst nach dem Bau gesehen:** 0a ohne `AKTUELLER_AUFTRAG.md` (das Vorbild `auslegen155.py` Z. 15 ändert den Zeiger).) | UEBERGABE, Umzug 13.10.2026, 13:03, Block 7 |
~~~

#### F72 — ARBEITSWEISE Abschnitt 0, „Wenn ich einen Auftrag schreibe“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Das Kriterium „Ergebniszahl vor Augen ⇒ anhalten“ hätte die Sitz⟧

Am HEAD `d9a05fb`: Anker Z. 354 · Quelle: UEBERGABE Z. 3984

~~~
| ☐ | Ein Abbruchweg schreibt so wenig wie möglich; was sich selbst beschreibt (`abbruch.txt`), bekommt keine Kopfdatei. (13.10.2026, Chat 22, Fehler Nr. 72: **Abbruchweg in drei Runden berichtigt, jede Runde erzeugte einen neuen Kreis** (E2, E3).) | UEBERGABE, Umzug 13.10.2026, 13:03, Block 7 |
~~~

#### F73 — ARBEITSWEISE Abschnitt 0, „Wenn ich ein fremdes Ergebnis bewerte (Cloud, Mac, Fable)“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Ein Helferbefund, der eine Aussage über ein fremdes Ergebnis änd⟧

Am HEAD `d9a05fb`: Anker Z. 271 · Quelle: UEBERGABE Z. 3985

~~~
| ☐ | Eine Aussage aus einem Ergebnis, die eine Wache betrifft, vor der Weitergabe an einer eigenen Messung prüfen. (13.10.2026, Chat 22, Fehler Nr. 73: **Befund aus einem fremden Ergebnis ungeprüft an den Betreiber** (12:57: „Wächter blind seit 2.1.296“, gestützt auf das Ergebnis TB-156; widerlegt 13:00 durch den Schliess-Auslöser) — Fehler Nr. 53 in anderer Gestalt.) | UEBERGABE, Umzug 13.10.2026, 13:03, Block 7 |
~~~

#### L1 — ARBEITSWEISE Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum g⟧

Am HEAD `d9a05fb`: Anker Z. 220 · Quelle: UEBERGABE Z. 4011

~~~
| ☐ | `pgrep` ohne `-a` sieht die eigene Sitzung nicht (13.10.2026, Chat 23, wörtlich aus der Übergabe): macOS-`pgrep` schliesst ohne `-a` den eigenen Prozess **und alle seine Vorfahren** aus (pgrep(1): „By default, the current pgrep or pkill process and all of its ancestors are excluded (unless -v is used)“; Option `-a`: „Include process ancestors in the match list“; gelesen in der Handbuchseite, nicht am Mac gemessen). Die Sitzung (PID 25614) ist Vorfahr ihrer eigenen Shell ⇒ `pgrep -x claude` rc 1 in der Sitzung ist zu erwarten; der Wächter unter launchd ist kein Nachfahr ⇒ er fand 25614 (Log Z. 2373, 11:00:30Z, mit `pgrep -x claude`, `starte_sitzung.sh` Z. 586). Damit ist auch die Stütze im Ergebnis TB-156 („Kernel-Name `2.1.296` ⇒ `pgrep -x claude` findet keinen Prozess“, Z. 7) widerlegt, nicht nur „Wache 4a blind“. Wache 4a und Schliess-Auslöser arbeiten. Für die Probe: EIGEN in der Sitzung mit `pgrep -a -x claude` (plus cwd) oder über die Elternkette bestimmen. | UEBERGABE, Nachtrag 13.10.2026, 15:57 |
~~~

#### C1 — ARBEITSWEISE Abschnitt 0, „Wenn ein Arbeitsabschnitt endet oder ein Verlust droht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber (Betreiber 10.10.2026, 09:38, wörtlich)⟧

Am HEAD `d9a05fb`: Anker Z. 132 · Quelle: UEBERGABE Z. 3790

~~~
| ☐ | ⭐⭐ Zusatz zu den zwei Zeilen darüber — Chatname mit ausgeschriebenem Datum (Betreiber 11.10.2026, 12:22, wörtlich; „zukünftig“): „Kleine Korrektur: kannst du die Bezeichnung des Chats, zukünftig das Datum korrekt ausschreiben folgend das Beispiel“ — „Opus Trading Bot-11.10.2026“. **Neue Form des Chatnamens und der ersten Zeile der ersten Nachricht: „Opus Trading Bot-<TT>.<MM>.<JJJJ>“** (Datum mit date abgelesen). Das löst die Form „<TT><Mon><JJJJ>“ und die Monatsliste aus der Anweisung vom 10.10.2026, 09:16 ab; alles Übrige jener Anweisung bleibt. Lesart des steuernden Chats, vorläufig: gilt ab dem nächsten Umzug, für Fable ebenso („Fable Trading Bot-<TT>.<MM>.<JJJJ>“); bestehende Chats werden nicht umbenannt. Lesart des steuernden Chats, vorläufig: UMZUG Abschnitt 6, Zeile „Ziel: …“ (am HEAD `d9a05fb` Z. 271: „von selbst … heißen … Ich benenne nichts von Hand um“) ist abgelöst durch die Karten des Betreibers vom 11.10.2026 (ein Helfer benennt über Chrome um); Z. 275 („Ein Datum mit Punkten …“) bleibt als Beobachtung zur Benennung durch die App; das Umbenennen von Hand mit Punkten gelang (UEBERGABE Z. 3871; Zusatz 13.10.2026, 14:19 im Umzug 13.10.2026, 13:03, UEBERGABE Z. 4004). | UEBERGABE, Nachtrag 11.10.2026, 12:23 |
~~~

#### P9a — ARBEITSWEISE Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum g⟧

Am HEAD `d9a05fb`: Anker Z. 220 · Quelle: EROEFFNUNG Z. 33

~~~
| ☐ | Regel des Betreibers vom 11.10.2026 (Eröffnung Punkt 9 (a), wörtlich; die Eröffnung spricht in seinem Namen): Sätze für Claude-Code-Sitzungen schickst du selbst über Chrome ab, ohne Karte je Start (ich am 11.10.2026, 11:11: „Wieso überträgst du TB 152 nicht wie vereinbart zukünftig und ab jetzt per Chrome selbstständig in die Claude Codes Sitzung bitte prüfe und merke dir das“ und „Dies zählt zukünftig für alle Überträger nach Claude Code“; Lesart des alten steuernden Chats, vorläufig, mir genannt: Das löst meine Karte von 09:58 „Karte je Start“ ab). Weg: Sitzung über den Wächter anlegen, Wächter-Log lesen, in Chrome unter claude.ai/code die eine Sitzung mit der Marke „trading-bot“ und ohne Nachrichten öffnen (über die Adresse zuordnen), prüfen (über Remote-Steuerung verbunden, „Noch keine Nachrichten“, HEAD unverändert), Satz eintragen, Bildschirmfoto, Return genau einmal — jeden Handgriff einzeln, nie zwei im selben Schritt (Fehler Nr. 59). Abfragen der Sitzung beantwortest du nie. Weist die Erlaubnisprüfung das Abschicken ab (so am 11.10.2026, 11:05 bei einem Helfer; um 11:13 ging es beim steuernden Chat durch), umgehst du sie nicht: Dann bekomme ich den Satz als Kopierfeld. Ist der Satz abgeschickt, steht kein Kopierfeld mit dem Satz mehr in der Antwort — sonst droht ein doppelter Start (Vorgabe des alten steuernden Chats, vorläufig). | EROEFFNUNG_STEUERNDER_CHAT.md, Punkt 9 (a) |
~~~

#### P9b — ARBEITSWEISE Abschnitt 0, „Immer“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Vor „passt nicht in Teil Tn“ messen, in welchem Teil der Abschni⟧

Am HEAD `d9a05fb`: Anker Z. 60 · Quelle: EROEFFNUNG Z. 33

~~~
| ☐ | Regel des Betreibers vom 11.10.2026 (Eröffnung Punkt 9 (b), wörtlich; die Eröffnung spricht in seinem Namen): Arbeite immer tokensparend und mach mir Vorschläge, wenn dir etwas auffällt — ohne eigene Analyseläufe (ich am 11.10.2026: „Es wäre schlecht wenn wir für die token optierung mehr Token ausgeben würden als wir je einsparen“). Beobachtungen: eine Zeile in logs/steuernder_chat/TOKEN_BEOBACHTUNGEN.md; die Vorschläge V1 bis V5 stehen in logs/steuernder_chat/2026-10-11_TOKEN_vorschlaege.md (V1 und V2 gelten, V3 bis V5 nach TB-154). | EROEFFNUNG_STEUERNDER_CHAT.md, Punkt 9 (b) |
~~~

#### P9c — ARBEITSWEISE Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum g⟧

Am HEAD `d9a05fb`: Anker Z. 220 · Quelle: EROEFFNUNG Z. 33

~~~
| ☐ | Regel des Betreibers vom 11.10.2026 (Eröffnung Punkt 9 (c), wörtlich; die Eröffnung spricht in seinem Namen): Claude Code am Mac soll angemeldet bleiben (ich am 11.10.2026); halten kannst du die Anmeldung nicht — offen ist der Backlog-Punkt, dass der Sitzungswächter „Not logged in“ und die Ablaufwarnung erkennt. | EROEFFNUNG_STEUERNDER_CHAT.md, Punkt 9 (c) |
~~~

#### P9e — ARBEITSWEISE Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum g⟧

Am HEAD `d9a05fb`: Anker Z. 220 · Quelle: EROEFFNUNG Z. 33

~~~
| ☐ | Regel des Betreibers vom 11.10.2026 (Eröffnung Punkt 9 (e), wörtlich; die Eröffnung spricht in seinem Namen): Die Terminal-Abfrage beantwortest du nie selbst (mir am 11.10.2026, 11:00 genannt). Sie entfällt, sobald der Wächter den Fensterinhalt ins Log schreibt (TB-155); bis dahin forderst du den Blick ins Terminal nur an, wenn du ihn brauchst — ist der Bildschirm gesperrt, gibt es kein Bild (so am 11.10.2026, 10:59), dann tragen das Wächter-Log und die Prüfung in Chrome (am 11.10.2026 bei TB-154 so getragen: die Sitzung über ihre Adresse in Chrome gelesen, kein Blick ins Terminal). | EROEFFNUNG_STEUERNDER_CHAT.md, Punkt 9 (e) |
~~~

#### P9f — ARBEITSWEISE Abschnitt 0, „Wenn eine Mac-Sitzung startet, endet oder abbricht“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: Auslegen prüft, dass der Arbeitsbaum g⟧

Am HEAD `d9a05fb`: Anker Z. 220 · Quelle: EROEFFNUNG Z. 33

~~~
| ☐ | Regel des Betreibers vom 11.10.2026 (Eröffnung Punkt 9 (f), wörtlich; die Eröffnung spricht in seinem Namen): Zur Ordner-Freigabe: Ich habe am 11.10.2026, 12:08 erneut verlangt, dass sie über Chrome bestätigt wird; der steuernde Chat hat es nicht getan und mir den Grund genannt. Dabei bleibt es, bis ich etwas anderes sage: Du beantwortest sie nie selbst, auch kein Helfer. | EROEFFNUNG_STEUERNDER_CHAT.md, Punkt 9 (f) |
~~~

#### X1 — LIESMICH.md Z. 30

Zieldatei: `docs/werkzeuge/sitzungswaechter/LIESMICH.md`
Art: ersetzen
Form: -
Anker: ⟦- **⛔ NICHT ANGEMELDET (TB-<Nr>)** (Rückgabewert 6) oder **⛔ API-ABREC⟧
Alt: ⟦docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md⟧
Neu: ⟦docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md⟧

Am HEAD `d9a05fb`: Anker Z. 30 · Quelle: ABN156 B4

#### X2 — BACKLOG.md Z. 474

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: ersetzen
Form: -
Anker: ⟦- **Erschlossen, nicht gemessen (Lesarten, vorläufig):** Wortlaut und ⟧
Alt: ⟦docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md⟧
Neu: ⟦docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md⟧

Am HEAD `d9a05fb`: Anker Z. 474 · Quelle: ABN156 B4

#### U1 — UMZUG Abschnitt 6

Zieldatei: `docs/projektfuehrung/UMZUG.md`
Art: nach
Form: Block
Anker: ⟦⭐⭐ **Gilt seit 10.10.2026 (eingetragen mit TB-152) — Chatname: Die ers⟧

Am HEAD `d9a05fb`: Anker Z. 264 · Quelle: UEBERGABE Z. 3790

~~~
⭐⭐ **Gilt seit 11.10.2026, 12:22 (eingetragen mit TB-157) — Chatname mit ausgeschriebenem Datum.** Betreiber 11.10.2026, 12:22, wörtlich (UEBERGABE, Nachtrag 11.10.2026, 12:23): „Kleine Korrektur: kannst du die Bezeichnung des Chats, zukünftig das Datum korrekt ausschreiben folgend das Beispiel“ — „Opus Trading Bot-11.10.2026“. **Neue Form des Chatnamens und der ersten Zeile der ersten Nachricht: „Opus Trading Bot-<TT>.<MM>.<JJJJ>“** (Datum mit date abgelesen). Das löst die Form „<TT><Mon><JJJJ>“ und die Monatsliste aus der Anweisung vom 10.10.2026, 09:16 ab; alles Übrige jener Anweisung bleibt. Lesart des steuernden Chats, vorläufig: gilt ab dem nächsten Umzug, für Fable ebenso („Fable Trading Bot-<TT>.<MM>.<JJJJ>“); bestehende Chats werden nicht umbenannt. Damit gilt im Codeblock unten statt „Opus Trading Bot-<TT><Mon><JJJJ>“ und der Monatsliste die Form „Opus Trading Bot-<TT>.<MM>.<JJJJ>“; der Codeblock bleibt als Wortlaut vom 10.10.2026 stehen. Lesart des steuernden Chats, vorläufig: UMZUG Abschnitt 6, Zeile „Ziel: …“ (am HEAD `d9a05fb` Z. 271: „von selbst … heißen … Ich benenne nichts von Hand um“) ist abgelöst durch die Karten des Betreibers vom 11.10.2026 (ein Helfer benennt über Chrome um); Z. 275 („Ein Datum mit Punkten …“) bleibt als Beobachtung zur Benennung durch die App; das Umbenennen von Hand mit Punkten gelang (UEBERGABE Z. 3871; Zusatz 13.10.2026, 14:19 im Umzug 13.10.2026, 13:03, UEBERGABE Z. 4004).
~~~

#### B1 — BACKLOG Abschnitt 5, Ende

Zieldatei: `docs/projektfuehrung/BACKLOG.md`
Art: vor
Form: Block
Anker: ⟦## 6 — Geparkt, null Arbeit *(ins Archiv verschoben 20.09.2026, TB-60)⟧

Am HEAD `d9a05fb`: Anker Z. 477 · Quelle: UEBERGABE Z. 3790, 3752; Bestand

~~~
### Regelwerk-Nachtrag 11.–13.10.2026 — eingetragen mit TB-157

- **Fehler Nr. 55 bis 73:** Regeln in `ARBEITSWEISE.md` Abschnitt 0, eingetragen mit TB-157. Nr. 55 bis 59: UEBERGABE, Umzug 11.10.2026, 08:54, Block 7; Nachtrag 11.10.2026, 09:08; Umzug 11.10.2026, 11:58, Block 7. Nr. 60 bis 64: Chat 20 (Umzug 11.10.2026, 14:13, Block 7). Nr. 65 bis 69: Chat 21 (Umzug 13.10.2026, 11:15, Block 7). Nr. 70 bis 73: Chat 22 (Umzug 13.10.2026, 13:03, Block 7). Nächste freie Nummer: 74.
- **Chatname mit ausgeschriebenem Datum** (Betreiber 11.10.2026, 12:22; UEBERGABE Z. 3790): in `ARBEITSWEISE.md` Abschnitt 0 und `UMZUG.md` Abschnitt 6, eingetragen mit TB-157. Nicht in TB-157: Eröffnung Punkt 6 und der Helferauftrag zum Umzug (nicht im Repo).
- **Regeln des Betreibers vom 11.10.2026** (Eröffnung Punkt 9): (a), (b), (c), (e), (f) in `ARBEITSWEISE.md` Abschnitt 0, eingetragen mit TB-157. (d): Vorgaben des alten steuernden Chats — die Bündelung „gebündelt mit dem letzten Werkzeugaufruf einer Antwort“ als eigene Zeile; der `jq`-Weg steht schon in Abschnitt 0, die zwei übrigen Sätze als Fehler Nr. 56 und 57.
- **`pgrep` ohne `-a`** (UEBERGABE, Nachtrag 13.10.2026, 15:57): Lehre in Abschnitt 0, eingetragen mit TB-157. Offen bleibt die Probe des Wächters (Umzug 13.10.2026, 13:03, Block 4 Nr. 3).
- **Offen, nicht eingeordnet** (UEBERGABE, Umzug 11.10.2026, 11:58, Block 4 Nr. 4; Lesart des steuernden Chats, vorläufig): die Formhinweise der Abnahmen TB-151 (Ergebnis Z. 88, 90, 94) und TB-152 (H1 bis H6); dazu „(o) E10 Ersetzungen in bestehenden Zeilen (UMZUG Z. 228, 260, 270–272; ARBEITSWEISE Z. 118, 212, 2480) — strittig, **Entscheid offen**“
~~~

#### E1 — ERGEBNIS_TB-156, Dateiende

Zieldatei: `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`
Art: ende
Form: Block
Anker: —

Am HEAD `d9a05fb`: Anker Z. 55 · Quelle: ABN156 A1, A2, B4; UEBERGABE Z. 4011

~~~
## Nachtrag 13.10.2026 — Abnahme ABN156 und Ursache `pgrep` (eingetragen mit TB-157; der Text darüber ist unverändert)

- **A1 — Ergebnis, Abschnitt „Zuerst, für den Betreiber“, Punkt Wache 4a:** „obwohl sonst immer mindestens ein Prozess ausserhalb stand“. Gemessen im Log `logs/sitzungswaechter/waechter.log`: alle 147 Zeilen `claude-Prozesse:` haben `0 ausserhalb` (100× „0 im Repo, 0 ausserhalb“, 47× „1 im Repo, 0 ausserhalb“), z. B. Z. 2331 (13.10. 05:20:47Z), Z. 2306, Z. 2281. Ausserdem lief um 10:26:29Z (Z. 2356) noch keine Sitzung im Repo, denn das Fenster von TB-156 ging erst 10:26:31Z auf (Z. 2363). Diese Logzeile belegt die Blindheit also nicht. Erschlossen bleibt die Blindheit nur aus dem eigenen `pgrep -x claude` der Sitzung (rc 1, während sie lief). Dafür gibt es keine Rohausgabe als Beleg. Die Folgerung ist plausibel, die angeführte Stütze ist falsch. Herkunft der „immer“-Aussage vermutlich der Kommentar `starte_sitzung.sh` Z. 575–578 (Stand 23.09.). *(Abnahme ABN156, wörtlich)*
- **Ursache, gemessen vom steuernden Chat** (UEBERGABE, Nachtrag 13.10.2026, 15:57, wörtlich): macOS-`pgrep` schliesst ohne `-a` den eigenen Prozess **und alle seine Vorfahren** aus (pgrep(1): „By default, the current pgrep or pkill process and all of its ancestors are excluded (unless -v is used)“; Option `-a`: „Include process ancestors in the match list“; gelesen in der Handbuchseite, nicht am Mac gemessen). Die Sitzung (PID 25614) ist Vorfahr ihrer eigenen Shell ⇒ `pgrep -x claude` rc 1 in der Sitzung ist zu erwarten; der Wächter unter launchd ist kein Nachfahr ⇒ er fand 25614 (Log Z. 2373, 11:00:30Z, mit `pgrep -x claude`, `starte_sitzung.sh` Z. 586). Damit ist auch die Stütze im Ergebnis TB-156 („Kernel-Name `2.1.296` ⇒ `pgrep -x claude` findet keinen Prozess“, Z. 7) widerlegt, nicht nur „Wache 4a blind“. Wache 4a und Schliess-Auslöser arbeiten. Für die Probe: EIGEN in der Sitzung mit `pgrep -a -x claude` (plus cwd) oder über die Elternkette bestimmen. Die Vorsichtsregel „vor jedem Start in Chrome prüfen, dass keine andere Sitzung im Repo arbeitet“ bleibt bis zur Probe.
- **Ergebnis TB-156 Z. 7, an der Stelle wörtlich** (die Übergabe oben gibt sie verkürzt wieder): „Seit Claude Code 2.1.296 trägt der Prozess den Kernel-Namen `2.1.296` statt `claude` (Programm `~/.local/share/claude/versions/2.1.296`). `pgrep -x claude` findet deshalb **keinen** Prozess mehr.“
- **A2 — Schranke 7, Auftrag Z. 46:** „Frei sind nur lesende Befehle: `ls`, `cat`, `head`, `wc`, `md5`, `shasum`, `cmp`, git `log`, `show`, `rev-parse`, `status`.“ Die Sitzung nutzte zusätzlich `pgrep -lf claude`, `ps -o … args`, `lsof -d txt` und `claude --version`. `pgrep -lf` und `ps -o args=` lesen Kommandozeilen, was der Wächter absichtlich nie tut (Z. 582–583). Das Ergebnis meldet das selbst unter „Abweichungen“. Schreibend war nichts davon, ein Abbruchkriterium ist nicht berührt (das gilt nur für schreibende Befehle). *(Abnahme ABN156, wörtlich)*
- **B4:** L1 (`LIESMICH.md`) und B1 (`BACKLOG.md` Z. 474) verweisen auf `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`. Die Datei fehlt (`ls`: nicht gefunden). Die Sitzung meldet das selbst. *(Abnahme ABN156, wörtlich)* **Berichtigt mit TB-157:** `docs/werkzeuge/sitzungswaechter/LIESMICH.md` Z. 30 und `docs/projektfuehrung/BACKLOG.md` Z. 474 nennen jetzt `docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md`.
~~~

#### P9d — ARBEITSWEISE Abschnitt 0, „Am Ende jeder Antwort“

Zieldatei: `docs/projektfuehrung/ARBEITSWEISE.md`
Art: nach
Form: Zeilen
Anker: ⟦| ☐ | Zusatz zur Zeile darüber: `ampel.py` läuft im Arbeitsbereich⟧

Am HEAD `d9a05fb`: Anker Z. 83 · Quelle: EROEFFNUNG Z. 33

~~~
| ☐ | Zusatz zur Zeile darüber — Vorgabe des alten steuernden Chats (Eröffnung Punkt 9 (d), wörtlich; neu daran ist die Bündelung): Die Ampel misst du mit jq nach der Formel von ampel.py, wenn das Ausführen von ampel.py abgelehnt wird (so am 11.10.2026), gebündelt mit dem letzten Werkzeugaufruf einer Antwort. | EROEFFNUNG_STEUERNDER_CHAT.md, Punkt 9 (d) |
~~~

## Anhang B — Werkzeug und Sollwerte

### Werkzeug

```python
#!/usr/bin/env python3
# TB-157 Werkzeug (Python 3.9): fuegt die Stuecke aus Anhang A des Auftrags ein, nur in die Zieldateien dort.
# Liest nur den Auftrag und die Zieldateien; holt keine Zeile aus UEBERGABE.md. Prueft alles, bevor es schreibt.
# Aufruf im Repo: PY WZ probe | einfuegen | vergleich | numstat <a> <b> [j_block] | journal <j_block> [--probe]
# rc 0 gut · 1 numstat/vergleich abweichend · 2 abgewiesen, nichts geschrieben · 3 ABBRUCH, nichts geschrieben · 64 falscher Aufruf
import hashlib, json, re, subprocess, sys
AUF = "docs/auftraege/MAC_TB-157_regelwerk_nachtrag_1013.md"
JOU = "docs/projektfuehrung/JOURNAL.md"
ERG = "docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md"
BEL = "docs/belege/TB-157/"

def lies(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def md5(p):
    return hashlib.md5(lies(p).encode("utf-8")).hexdigest()

def auftrag():
    z = lies(AUF).split("\n")
    a = z.index("## Anhang A — Stücke (wörtlich)")
    b = z.index("## Anhang B — Werkzeug und Sollwerte")
    st, i = [], a
    while i < b:
        if z[i].startswith("#### "):
            d, j = {"id": z[i][5:].split(" — ")[0]}, i + 1
            while j < b and z[j] != "~~~" and not z[j].startswith("#### "):
                m = re.match(r"^(Zieldatei|Art|Form|Anker|Alt|Neu): (.*)$", z[j])
                if m:
                    d[m.group(1)] = m.group(2)
                j += 1
            d["text"] = []
            if j < b and z[j] == "~~~":
                k = z.index("~~~", j + 1)
                d["text"], j = z[j + 1:k], k + 1
            i = j
            d["datei"] = d["Zieldatei"].strip("`")
            for f in ("Anker", "Alt", "Neu"):
                v = d.get(f, "")
                d[f] = v[1:-1] if v.startswith("⟦") and v.endswith("⟧") else ""
            st.append(d)
        else:
            i += 1
    c = z.index("```json", z.index("### Sollwerte (maschinenlesbar)"))
    return st, json.loads("\n".join(z[c + 1:z.index("```", c + 1)]))

def plan(st, soll):
    fehler, schon, dat, ein, bil, aus = [], [], {}, {}, {}, []
    for d in st:
        if d["datei"] not in dat:
            dat[d["datei"]] = lies(d["datei"]).split("\n")
            ein[d["datei"]], bil[d["datei"]] = {}, [0, 0]
    neutext = "\n".join("\n".join(d["text"]) + "\n" + d["Neu"] for d in st)
    ers = {p: list(z) for p, z in dat.items()}
    for d in st:
        p, z, art = d["datei"], dat[d["datei"]], d["Art"]
        t = [i for i, s in enumerate(z) if d["Anker"] and d["Anker"] in s]
        if art == "ende":
            pos, nz, sch = len(z) - 1 if z[-1] == "" else len(z), "-", d["text"][0] in z
        else:
            if len(t) != 1:
                fehler.append("%s: Anker trifft %d Zeilen" % (d["id"], len(t)))
                aus.append("%s · %s · Anker %d Treffer · FEHL" % (d["id"], p, len(t)))
                continue
            nz = t[0] + 1
            if d["Anker"] in neutext:
                fehler.append("%s: Anker steht in einem neuen Text" % d["id"])
        if art == "ersetzen":
            s = z[t[0]]
            na, nn = "\n".join(z).count(d["Alt"]), "\n".join(z).count(d["Neu"])
            if na == 0 and nn == 1:
                schon.append(d["id"])
            elif s.count(d["Alt"]) != 1 or na != 1 or nn != 0:
                fehler.append("%s: Alt in Ankerzeile %d, in Datei %d, Neu in Datei %d" % (d["id"], s.count(d["Alt"]), na, nn))
            else:
                ers[p][t[0]] = s.replace(d["Alt"], d["Neu"])
                bil[p][0] += 1; bil[p][1] += 1
            aus.append("%s · %s · Anker Z. %d · ersetzen · Alt %d · Neu %d · ok" % (d["id"], p, nz, na, nn))
            continue
        if art in ("nach", "vor"):
            pos = t[0] + 1 if art == "nach" else t[0]
            sch = d["text"][0] in z
            if d["Form"] == "Zeilen" and d["text"][0].startswith("|") and not z[t[0]].startswith("|"):
                fehler.append("%s: Tabellenzeile an einer Zeile ohne Tabelle" % d["id"])
        if sch:
            schon.append(d["id"])
        ein[p].setdefault(pos, []).append(d)
        aus.append("%s · %s · Anker Z. %s · %s · Zeilen %d · erste Zeile schon %d · Anker in neuen Texten %d · ok" % (d["id"], p, nz, art, len(d["text"]), int(sch), int(bool(d["Anker"]) and d["Anker"] in neutext)))
    neu = {}
    for p, z in ers.items():
        z = list(z)
        for pos in sorted(ein[p], reverse=True):
            L = []
            for d in ein[p][pos]:
                if d["Form"] == "Block":
                    if L and L[-1] != "":
                        L.append("")
                    L += [""] + d["text"] + [""] if not L else d["text"] + [""]
                else:
                    L += d["text"]
            if L and L[0] == "" and (pos == 0 or z[pos - 1] == ""):
                L = L[1:]
            if L and L[-1] == "" and pos < len(z) and z[pos] == "":
                L = L[:-1]
            z[pos:pos] = L
            bil[p][0] += len(L)
        neu[p] = "\n".join(z)
    return fehler, schon, neu, bil, aus

def bilanz(bil, soll):
    ok = True
    for p in sorted(bil):
        s = soll["zeilen"].get(p)
        g = s == bil[p]
        ok = ok and g
        print("Datei %s · Soll +%s/-%s · Ist +%d/-%d · %s" % (p, s and s[0], s and s[1], bil[p][0], bil[p][1], "gleich" if g else "UNGLEICH"))
    return ok

def vorkommen(z, t):
    return sum(1 for i in range(len(z) - len(t) + 1) if z[i:i + len(t)] == t)

def main(a):
    if not a or a[0] not in ("probe", "einfuegen", "vergleich", "numstat", "journal"):
        print("Aufruf: probe | einfuegen | vergleich | numstat <a> <b> [j_block] | journal <j_block> [--probe]"); return 64
    st, soll = auftrag()
    if a[0] in ("probe", "einfuegen"):
        if len(a) != 1:
            return main([])
        fehler, schon, neu, bil, aus = plan(st, soll)
        print("\n".join(aus))
        if len(st) != soll["stuecke"]:
            fehler.append("Stuecke %d statt %d" % (len(st), soll["stuecke"]))
        if schon and len(schon) == len(st) and not fehler:
            print("ABGEWIESEN, nichts geschrieben: schon eingefuegt: " + ", ".join(schon)); return 2
        if schon:
            fehler.append("erste Zeile schon da: " + ", ".join(schon))
        gl = bilanz(bil, soll)
        print("Stuecke %d · eingefuegte Zeilen %d" % (len(st), sum(b[0] - b[1] for b in bil.values())))
        if fehler or not gl:
            for f in fehler + ([] if gl else ["Zeilenbilanz nicht wie Soll"]):
                print("ABBRUCH: " + f)
            print("ABGEWIESEN, nichts geschrieben"); return 3
        if a[0] == "probe":
            print("Gesamt: wie Soll, nichts geschrieben (Probe)"); return 0
        for p, t in neu.items():
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
        for p, t in neu.items():
            print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (p, md5(p), "gleich" if lies(p) == t else "UNGLEICH"))
        print("Gesamt: wie Soll, alle eingefuegt, je genau einmal"); return 0
    if a[0] == "vergleich":
        ok = True
        for d in st:
            z = lies(d["datei"]).split("\n")
            n = "\n".join(z).count(d["Neu"]) if d["Art"] == "ersetzen" and "\n".join(z).count(d["Alt"]) == 0 else (vorkommen(z, d["text"]) if d["text"] else 0)
            ok = ok and n == 1
            print("%s · %s · Vorkommen %d · %s" % (d["id"], d["datei"], n, "GLEICH" if n == 1 else "ABWEICHUNG"))
        print("Gesamt: alle zeichengleich, je genau einmal" if ok else "Gesamt: ABWEICHUNG"); return 0 if ok else 1
    if a[0] == "numstat":
        if len(a) not in (3, 4):
            return main([])
        r = subprocess.run(["git", "diff", "--numstat", a[1], a[2]], capture_output=True, text=True)
        print(r.stdout.rstrip("\n"))
        ist = {}
        for s in r.stdout.splitlines():
            x = s.split("\t")
            ist[x[2]] = [int(x[0]), int(x[1])]
        sl = dict(soll["zeilen"])
        if len(a) == 4:
            sl[JOU] = [len(lies(a[3]).split("\n")) - 1 + 3, 0]
        ok = True
        for p in sorted(sl):
            g = ist.get(p) == sl[p]
            ok = ok and g
            print("Soll %s %d\t%d · Ist %s · %s" % (p, sl[p][0], sl[p][1], ist.get(p), "gleich" if g else "UNGLEICH"))
        w = [p for p in ist if p not in sl and not p.startswith(BEL) and p not in (ERG, AUF)]
        print("weitere Dateien ausser Belegen, Auftrag und Ergebnis: " + (", ".join(w) or "keine"))
        return 0 if ok and not w else 1
    if len(a) not in (2, 3) or (len(a) == 3 and a[2] != "--probe"):
        return main([])
    b, z = lies(a[1]), lies(JOU).split("\n")
    bz = b.split("\n")
    L = [i for i, s in enumerate(z) if s == "## Wiederkehrende Lehren"]
    k = [re.match(r"^## ([A-Z]{2}) — TB-", s).group(1) for s in z[:L[0] if L else 0] if re.match(r"^## ([A-Z]{2}) — TB-", s)]
    letzte = k[-1] if k else "??"
    n2 = chr(ord(letzte[1]) + 1) if letzte[1] != "Z" else "A"
    nk = (letzte[0] if letzte[1] != "Z" else chr(ord(letzte[0]) + 1)) + n2
    be = [("endet mit Zeilenende", b.endswith("\n") and not b.endswith("\n\n")),
          ("Kopfzeile ## %s — TB-157: …" % nk, bz[0].startswith("## %s — TB-157: " % nk)),
          ("### Was gemessen ist genau einmal, Leerzeile davor", bz.count("### Was gemessen ist") == 1 and bz[bz.index("### Was gemessen ist") - 1] == ""),
          ("### Was offen bleibt genau einmal", bz.count("### Was offen bleibt") == 1),
          ("keine Zeile ---", "---" not in bz),
          ("Schlusszeile *Geschrieben …", bz[-2].startswith("*Geschrieben ") if len(bz) > 1 else False),
          ("## Wiederkehrende Lehren genau einmal", len(L) == 1),
          ("davor --- und Leerzeile", len(L) == 1 and z[L[0] - 1] == "" and z[L[0] - 2] == "---"),
          ("Kennung noch frei", not any(s.startswith("## %s — " % nk) for s in z))]
    for t, v in be:
        print("%s: %s" % (t, "ja" if v else "NEIN"))
    print("Kennung %s (erwartet %s) · letzte %s" % (nk, soll["journal_kennung"], letzte))
    if not all(v for _, v in be):
        return 2
    neu = bz[:-1] + ["", "---", ""]
    print("Zeilen +%d" % len(neu))
    if len(a) == 3:
        print("Probe: nichts geschrieben"); return 0
    z[L[0]:L[0]] = neu
    t = "\n".join(z)
    with open(JOU, "w", encoding="utf-8") as f:
        f.write(t)
    print("geschrieben und zurueckgelesen: %s · md5 %s · %s" % (JOU, md5(JOU), "gleich" if lies(JOU) == t else "UNGLEICH"))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

### Sollwerte (maschinenlesbar)

```json
{
 "stuecke": 32,
 "journal_kennung": "ET",
 "zeilen": {
  "docs/projektfuehrung/ARBEITSWEISE.md": [
   27,
   0
  ],
  "docs/projektfuehrung/UMZUG.md": [
   2,
   0
  ],
  "docs/projektfuehrung/BACKLOG.md": [
   9,
   1
  ],
  "docs/werkzeuge/sitzungswaechter/LIESMICH.md": [
   1,
   1
  ],
  "docs/ERGEBNIS_TB-156_waechter_fensterinhalt.md": [
   8,
   0
  ]
 }
}
```

## Anhang C — Journalblock (Gliederung; die Sitzung füllt `<…>` in eigenen Worten)

~~~
## ET — TB-157: Regelwerk-Nachtrag 13.10.2026 und Nachtrag zum Ergebnis TB-156
*Quelle: `docs/ERGEBNIS_TB-157_regelwerk_nachtrag_1013.md`, Commits <⟨S0⟩, ⟨E⟩, ⟨F⟩>.*

**Quelle:** <ein Satz: was eingetragen ist, wo>

### Was gemessen ist
- <je Schritt eine Zeile mit Soll und Ist>

### Was offen bleibt
- <offene Posten, mindestens: Probe des Wächters; Formhinweise TB-151/TB-152>

*Geschrieben <Datum, Uhrzeit aus date> von der Mac-Sitzung TB-157. Quellenvermerk: siehe Kopf.*
~~~
