# TB-155 Sitzungswächter schreibt den Fensterinhalt ins Log — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 13.10.2026, 07:14** (Helfer BAU155, per `bau.sh` aus Bausteinen), gebaut ausserhalb des Repos und an einer Kopie simuliert. Urteil und Freigabe liegen beim steuernden Chat; ein frischer Gegenleser ist Pflicht.

**Sitzungstitel:** `TB-155` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main` am HEAD `fb8d3894948b2609b5ce4891937225b14e81c241` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-155`); den Satz fügt der Betreiber ein.
**Dieser Auftrag:** `docs/auftraege/MAC_TB-155_waechter_fensterinhalt.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9), kurz `PY`; das Werkzeug `docs/belege/TB-155/tb155_werkzeug.py` (Anhang A) kurz `WZ`, seine letzte Zeile ist `rc <n>`. „`PY WZ x` ⇒ `datei`“ heisst: Ausgabe samt Fehlerausgabe nach `docs/belege/TB-155/datei`.
**Ziel:** Das Wächter-Log sagt nach jedem Start, was im neuen Fenster steht (Anmeldung, Ablaufwarnung, 12 Zeilen ohne Kontozeile); „nicht angemeldet“ und „API-Abrechnung“ heissen nicht mehr „eingabebereit“.
**Bauart wie TB-144** (`docs/auftraege/MAC_TB-144_waechter_reparatur_rest.md`), aber klein; bei Widerspruch gilt dieser Auftrag. **Anders:** Diese Sitzung ruft weder `osascript` noch `launchctl` auf; gemessen wird am Wächter-Log.

## ⭐⭐ Freigabe: Karte des Betreibers, Vorgaben des steuernden Chats

**Freigabeklasse: Handwerk mit Einzelfreigabe** — der Wächter und seine Schranke 3 werden geändert (`docs/projektfuehrung/BACKLOG.md` Z. 360).

**(a) Die Karte des Betreibers, wörtlich:** Auswahlkarte im steuernden Chat, 11.10.2026, gestellt 13:00, Antwort eingetragen 13:02. Frage: „TB-155 ändert den Sitzungswächter und seine Schranke 3; deine Antwort ist die Einzelfreigabe dafür. Was darf der Wächter bei „EINGABEBEREIT“ ins Log schreiben?“ — Antwort: „Zeilen, Konto geschwärzt (Recommended)“ (auf der Karte: „Die letzten 12 Fensterzeilen; die Zeile mit Konto oder Mailadresse wird ersetzt. Dazu Anmeldestatus und Ablaufwarnung als eigene Zeilen. Preis: eine Schwärzungsregel mehr, die getestet werden muss.“). Davor, Karte 11.10.2026, 11:01, zur Frage, ob der Wächter den Fensterinhalt ins Log schreibt: „Ja, nach TB-154 (Recommended)“.

**(b) Vorgaben des steuernden Chats, dem Betreiber genannt, ohne Widerspruch** (nicht auf der Karte; `docs/projektfuehrung/UEBERGABE.md`, Umzug 11.10.2026, 14:13, Block 4 Nr. 2 und Block 6): API-Abrechnung und „Not logged in“ sind ⛔; 12 Zeilen und das Ersetzen der Kontozeile auch bei ⛔; Adresse der Sitzung im Klartext; erster Test im Repo; „`ARBEITSWEISE.md` ändert erst der Regelwerk-Nachtrag“.

**(c) Wie im Vorbild TB-144** (dort Z. 109, 157 und 191): `kill -TERM` nur für eine stehen gebliebene Probe-Sitzung oder eine andere `claude`-Sitzung ohne Auftrag im Repo (wie Vorbild Z. 157).

**Die Sitzung darf ändern, und nichts sonst** (Ordner des Wächters: `docs/werkzeuge/sitzungswaechter/`):
- dort `starte_sitzung.sh` (Stücke S1–S4c) und neu `test_fensterinhalt.sh` — nur über `WZ waechter`;
- dort `LIESMICH.md` (L1, L2) und `docs/projektfuehrung/BACKLOG.md` (B1) — nur einfügen, über `WZ doku`;
- `docs/projektfuehrung/JOURNAL.md` — der Block der Sitzung, über `WZ journal`;
- neu: `docs/belege/TB-155/…` und `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`;
- nicht in git: `docs/auftraege/_ausloeser/probe_<PID>` (Probe-Auslöser anlegen).

**Nicht erlaubt:** `einschalten.sh`, die plist, `ARBEITSWEISE.md`, `UEBERGABE.md`, Register; bestehende Zeilen in `LIESMICH.md`, `BACKLOG.md`, `JOURNAL.md` ändern oder entfernen.

## Belegt · erschlossen · offen

- **Belegt** (am HEAD gemessen): `starte_sitzung.sh` (622 Zeilen) schreibt Fensterzeilen nur über `fensterzeilen()` (Z. 177–184: höchstens 8, je 160 Zeichen), nur unter „⛔ STARTFRAGE“ und „⛔ KEINE EINGABEZEILE“, nicht unter „⭐ EINGABEBEREIT“ (Z. 204–205); der Kopf schreibt das fest (Z. 50–52). Die Anmeldung prüft der Wächter nicht; einen versionierten Test hat er nicht. `logs/` wird nicht gepusht (`.gitignore` Z. 27), Belege schon. Fenster am 09.10.2026 (`docs/belege/TB-144/b_m2_3.txt`): 10 nicht-leere Zeilen, 2 dort ersetzt (Abo-Name, Ablauf der Anmeldung), keine mit `@` (`docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md` Z. 73); Ablaufwarnung „Your login expires in 1 day · run /login to renew“ (Z. 83). „Claude Max“ in der Kopfzeile: Handnotiz vom 23.09.2026 (`LIESMICH.md` Z. 309). Zur API-Abrechnung sagt der Wächter selbst (Kommentar zur Schlüsselbund-Wache, Z. 546): „sie KOSTET dann Geld“.
- **Erschlossen:** Wortlaut und Stelle von `Not logged in`, und dass dann die Eingabezeile steht; die Kopfzeile bei `API Usage Billing`; dass die Abo-Zeile heute `Claude Max` trägt; dass jede Ablaufwarnung `expire` enthält; dass `cut` unter `LC_ALL=en_US.UTF-8` am Mac Zeichen zählt (misst der Test in 0b). **Die Sitzung meldet sich dafür nicht ab und ruft kein `/login` auf.** Die Kontoregel (`KONTO` in Anhang A, 26 Merkmale) ist eine Merkmalliste, kein Beweis (Schranke 3); die Fenster im Test sind nachgebaut, Konto-, Anmelde-, API-Zeile und Ablaufwarnung dort erfunden.
- **Offen — misst die Sitzung an der Probe (Schritt B), nie raten:** was unter „⭐ EINGABEBEREIT (PROBE)“ steht; ob der Schnitt unter launchd Zeichen zerschneidet (`WZ beleg` zählt sie); ob der Test unter bash 3.2 grün ist. **Bleibt offen:** Rückgabewert 6 und 7 laufen nur im Test, mit Attrappen (`sage`, `sleep`, `fenster_lesen`); Probe-Zweig und echten Start um `warte_auf_eingabezeile` herum prüft kein Test. Ob BSD-`cut` unter `LC_ALL=en_US.UTF-8` an ungültigen Bytes abbricht (dann fehlen Zeilen), ist erschlossen; „Schnitt: 202 Striche“ misst unter Linux nur die Attrappe.
- **Simulation des Helfers** (Kopien aus `git show HEAD:<pfad>`; Linux, bash 5.1 statt 3.2, Python 3.10): jeder Anker 1; `bash -n` rc 0; Test 113 ok, 0 FEHL; 55 Mutationen (20 im Block, 9 ausserhalb: `fensterzeilen`, Zweige rc 3, 6, 7, 26 je Merkmal der Kontoregel), gemessen rot: 54 von 55 (grün: `aws_secret` — enthält ein anderes Merkmal); `nachweis` rc 0; der Probe-Zweig mit Attrappen in 10 Läufen an 9 Fenstern (nicht angemeldet: rc 6, API-Abrechnung: rc 7; die Lesung vom 09.10.2026 in voller Breite bis `WZ beleg`: 2 zerschnittene Zeichen, rc 0). Linux-`cut` zählt Bytes: der Test lief mit einer Attrappe, die Zeichen zählt; ohne sie ist nur „Schnitt: 202 Striche“ rot. **Nicht simuliert:** was `osascript`, Terminal, launchd und Claude Code wirklich tun; bash 3.2 und die Werkzeuge des Macs; der Zweig des echten Starts. Die Sitzung zählt selbst nach; ihre Zahl gilt.

## Schranken — je mit dem, wovor sie schützen

1. **Kein Enter, kein `keystroke`, kein System Events, kein Text in ein Fenster** — weder im Wächter noch in dieser Sitzung. *Schützt:* Betreiberentscheidung 23.09.2026 (ARBEITSWEISE 19).
2. **Diese Sitzung ruft weder `osascript` noch `launchctl` auf, meldet sich nicht ab und ruft kein `/login` auf;** das Fenster liest nur der Wächter, über die Probe. *Schützt:* die Anmeldung des Betreibers.
3. **Schranke 3, neu (Freigabe oben):** Ins Log gehen höchstens 12 nicht-leere Zeilen je 160 Zeichen des **neu geöffneten** Fensters, bei ⛔ und bei ⭐, Kontozeilen ersetzt, dazu „Anmeldung: …“ und „Ablaufwarnung: …“; die Adresse der Sitzung bleibt im Klartext (Vorgabe des steuernden Chats, dem Betreiber um 13:00 genannt); unverändert keine Umgebungsvariablen, Schlüssel, Dateiinhalte. **Die Kontoregel ist eine Merkmalliste, kein Beweis** — ein Name ohne Merkmal oder ein umbrochener Mailrest bleibt stehen; deshalb sieht die Sitzung vor jedem Beleg nach Konto, Name und Schlüssel (Schritt B) und committet bei einem Fund den Beleg nicht (Rückweg, Abbruch). **Belege:** Log-Ausschnitte zuerst nach `$TMPDIR`, dann nur über `WZ beleg` nach `docs/belege/TB-155/` — es ersetzt Kontozeilen, `/Users/<name>` in jeder Zeile und, wie TB-144, die Zeile der Ablaufwarnung; im Ergebnis steht zu ihr nur ja oder nein (Rüge der Abnahme TB-144, `BACKLOG.md` Z. 371). *Schützt:* Kontodaten (Belege werden gepusht).
4. **Die sechs Wachen, Schliess- und Probe-Auslöser, `fenster_oeffnen` und die Startzeile bleiben unverändert;** geändert werden nur S1–S4c. *Schützt:* „nie zwei Aufträge im selben Arbeitsbaum“, Abo statt API-Abrechnung.
5. **`/bin/bash` des Macs ist 3.2; `starte_sitzung.sh` speichert nur `WZ`** (fertige Kopie in `$TMPDIR`, `bash -n`, Test, dann in einem Schritt). *Schützt:* launchd führt die Datei aus dem Arbeitsbaum aus — eine gespeicherte Änderung ist sofort scharf.
6. **Nie `git add -A`, nie `git add .`;** jeder Commit nennt seine Dateien mit Namen. *Schützt:* vor Auslöser oder Log im Commit.

## Schritt 0 — Sicherung, Ausgang

**0a. Zuerst, bevor `docs/belege/TB-155/` entsteht:** `git status --porcelain > "$TMPDIR/tb155_0a.txt"` und `git rev-parse HEAD`. Soll: HEAD `fb8d3894948b2609b5ce4891937225b14e81c241` und genau diese vier Einträge (Reihenfolge egal); sonst **ABBRUCH**.

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-155_waechter_fensterinhalt.md
```

*Soll: Vorgabe des steuernden Chats; beim Bau geändert: `EROEFFNUNG_STEUERNDER_CHAT.md`, `UEBERGABE.md`; unverfolgt: nichts.*

Dann das Werkzeug auslesen:

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-155_waechter_fensterinhalt.md "$TMPDIR" <<'EOF'
import hashlib, sys
z = open(sys.argv[1], encoding="utf-8").read().split("\n")
i = z.index("### Werkzeug")
a = next(k for k in range(i + 1, len(z)) if z[k] == "```python")
b = next(k for k in range(a + 1, len(z)) if z[k] == "```")
t = "\n".join(z[a + 1:b]) + "\n"
open(sys.argv[2] + "/tb155_werkzeug.py", "w", encoding="utf-8").write(t)
print("tb155_werkzeug.py", hashlib.sha256(t.encode("utf-8")).hexdigest())
EOF
```

Soll: `tb155_werkzeug.py fc69bc899e595842504ba528cabf25e621b65d68cb2b7fb10e3e4027f0ff26e5`; sonst ABBRUCH. Commit `TB-155 Schritt 0: Stand des steuernden Chats (Auftrag TB-155)` mit genau den vier Pfaden (mit Namen hinzufügen), pushen ⇒ **⟨S0⟩**. Erst jetzt: `$TMPDIR/tb155_0a.txt` unverändert nach `docs/belege/TB-155/0a_status.txt` (`cmp` gleich) und das Werkzeug nach `docs/belege/TB-155/tb155_werkzeug.py` (sha256 noch einmal). **Jede Rohausgabe bleibt roh;** die Beschreibung (was, Befehl, Bytes, Zeilen, md5) steht in `<name>.kopf.txt`.

**0b. Ausgang und Vorprüfung** (schreibt nur nach `$TMPDIR`): `PY WZ waechter --probe` ⇒ `0b_waechter_probe.txt`, `PY WZ doku --probe` ⇒ `0b_doku_probe.txt`. Soll je rc 0 und:
- `Ausgang … starte_sitzung.sh · 622 Zeilen · … · md5 464ac93c53829935e479c5f14121c574`, `LIESMICH.md` 371 Zeilen, md5 `61353389b9c2a1a66ce2bd669932937a`, `BACKLOG.md` 480, md5 `1b020860a28912cf9b281a017ae9d33b` (weicht ein Wert ab: vermerken, die Anker entscheiden);
- neun Zeilen `… · Anker 1 (Soll 1) · …`; am HEAD: S1 Z. 50–52, S2 Z. 177–184, S3 Z. 187, S4a Z. 196–197, S4b Z. 201–202, S4c Z. 204–205 (`starte_sitzung.sh`); L1 vor Z. 10, L2 nach Z. 41 (`LIESMICH.md`); B1 vor Z. 469 (`BACKLOG.md`). Ein Anker ≠ 1 ⇒ ABBRUCH;
- `bash -n rc 0`, 113 Zeilen `ok   …`, `Test Fensterinhalt: 113 ok, 0 FEHL`, `Test rc 0` — der Test läuft hier zum ersten Mal unter bash 3.2, gegen die fertige Kopie in `$TMPDIR`; „Schnitt: 202 Striche …“ misst, ob `cut` am Mac Zeichen zählt;
- `Zeilen + 31 (entfernt 0)` (`LIESMICH.md`) und `Zeilen + 8 (entfernt 0)` (`BACKLOG.md`).

**`FEHL` oder rc ≠ 0 ⇒ ABBRUCH, nichts richten** (nichts ist gebaut): die Zeile `FEHL …` samt `Ist:` und `Soll:` ins Ergebnis. Danach zeigt `git status --porcelain` nichts ausserhalb von `docs/belege/TB-155/`. Commit `TB-155 0: Ausgang, Vorprüfung, Werkzeug` (Dateien unter `docs/belege/TB-155/`, mit Namen), pushen.

## Schritt A — Bau: Wächter und Test

**Was sich ändert (wörtlich in Anhang A):** S1 Kopf, Schranke 3 neu · S2 Block „TB-155 FENSTERINHALT“ (sieben Funktionen, die von der Standardeingabe lesen) und ein neues `fensterzeilen()` · S3–S4b `warte_auf_eingabezeile` fragt `fenster_lage` statt zweier Muster (die Frage geht weiter vor) · S4c `Not logged in` ⇒ „⛔ NICHT ANGEMELDET“ (Rückgabewert 6), `API Usage Billing` ⇒ „⛔ API-ABRECHNUNG“ (Rückgabewert 7), je statt „⭐ EINGABEBEREIT“; Fensterzeilen auch unter „⭐ EINGABEBEREIT“. **„Anmeldung: unklar“ bleibt „⭐ EINGABEBEREIT“.**

**A1.** `PY WZ waechter` ⇒ `a1_bau.txt`. Soll wie in 0b, dazu `gespeichert … starte_sitzung.sh · 723 Zeilen · … · md5 8ea9eaaa2b6a1be8ca5587b21a7fcd7f` und `neu … test_fensterinhalt.sh · 158 Zeilen · … · md5 b05e0644e15b78e58383bb5879db9cbf`. **Ab hier ist der neue Wächter scharf.**
**A2.** `/bin/bash docs/werkzeuge/sitzungswaechter/test_fensterinhalt.sh > docs/belege/TB-155/a2_test.txt 2>&1; echo "rc $?"` ⇒ Soll rc 0, letzte Zeile `Test Fensterinhalt: 113 ok, 0 FEHL`. Die erste Zeile von `/bin/bash --version` in die Kopfdatei. **Abweichung: Rückweg (Abbruchkriterien), dann ABBRUCH.**
**A3.** `git diff --numstat` ⇒ Soll `112	11	docs/werkzeuge/sitzungswaechter/starte_sitzung.sh`, sonst keine verfolgte Datei. **Abweichung: Rückweg, dann ABBRUCH.** Commit `TB-155 A: Waechter schreibt den Fensterinhalt ins Log, Test` (die zwei Dateien des Wächters und die Belege, mit Namen), pushen.

## Schritt B — Probe über den echten Weg

Auslöserdatei → launchd → Skript (wie TB-144, Schritt D): Die Probe ruft dieselbe `warte_auf_eingabezeile` wie ein echter Start.

**EIGEN** ist die PID dieser Sitzung: `pgrep -x claude`, je PID `lsof -a -p <pid> -d cwd -Fn` — genau **eine** mit cwd im Repo; sonst keine Probe: melden, weiter mit Schritt C.

**Mindestens zwei Läufe** (Abstand mindestens 35 s: `ThrottleInterval` 30, plist Z. 36–37):
1. `wc -l < logs/sitzungswaechter/waechter.log` (Z0), dann `: > docs/auftraege/_ausloeser/probe_<EIGEN>`.
2. `PY WZ warte <Z0> "$TMPDIR/tb155_b_probe<i>.txt"` — sieht alle 10 s nach (höchstens 100 s), ob das Log **hinter Zeile Z0** `----- fertig (probe), rc <r> -----`, `⛔ ABBRUCH (Probe)`, `⛔ ABGEWIESEN: Der Probe-Ausloeser …` oder `⛔ Konnte Probe-Ausloeser nicht wegraeumen` trägt (eine fremde `⛔ ABGEWIESEN` beendet das Warten nicht), und schreibt dann die Log-Zeilen ab Z0+1 roh in die Datei. rc 3: **einmal** wiederholen. Kommt dann keine: melden, nicht wiederholen; liegt `probe_<EIGEN>` noch in `_ausloeser/`, mit `mv` nach `_ausloeser/_erledigt/` legen (nicht löschen).
3. **Dort nachsehen, vor jedem Beleg:** Steht in einer Zeile `   | …` ein Konto, ein Personenname (auch als Teil eines Rechner- oder Ordnernamens; `~/trading-bot` und die Ordner des Repos sind kein Fund), eine Mailadresse, eine Organisation oder ein Schlüssel unersetzt? **Fund ⇒ kein Beleg von diesem Lauf, nichts committen, was die Zeile trägt, nichts zitieren; Rückweg, dann ABBRUCH (Abbruchkriterien).** Sonst `PY WZ beleg "$TMPDIR/tb155_b_probe<i>.txt" docs/belege/TB-155/b_probe<i>_log.txt`; es nennt die Zahl zerschnittener Zeichen (> 0: Befund).

**Soll je Lauf:** `Fenster <n> neu geoeffnet`; `⭐ EINGABEBEREIT (PROBE)`; darunter `   Anmeldung: Abo`, `   Ablaufwarnung: nein` oder `   Ablaufwarnung: ja | …`, `   Letzte Zeilen von Fenster <n> (hoechstens 12, je 160 Zeichen, Kontozeilen ersetzt):`, höchstens 12 Zeilen `   | …`, davon mindestens eine `   | <<entfernt: Kontozeile>>` und keine mit `@`; `Probe: beende PID <p> …`; `Fenster <n> geschlossen`; `----- fertig (probe), rc 0 -----`; danach im Repo nur EIGEN. Bei leerem oder nicht lesbarem Fensterinhalt steht unter „⛔ KEINE EINGABEZEILE“ nur `   Fensterinhalt leer oder nicht lesbar: …` (Befund). Die Probe versucht bei jeder Rückgabe der Prüfung, ihr Fenster zu schliessen; ob es geschlossen ist oder offen bleibt, steht im Log (`Fenster <n> geschlossen` oder `bleibt offen: <Grund>`).

**Befund, kein Abbruch — ins Ergebnis, nichts richten:** `Anmeldung: unklar` (dazu, ohne zu zitieren: ob eine Zeile `   | …` das Wort `Claude` trägt); keine ersetzte Zeile; die Adresse `https://claude.ai/code/session_` fehlt; zerschnittene Zeichen am Zeilenende; `⛔ NICHT ANGEMELDET (PROBE)`, rc 6 (**kein `/login`**; im Ergebnis als Erstes sagen, dass der Betreiber sich anmelden muss); `⛔ API-ABRECHNUNG (PROBE)`, rc 7 (im Ergebnis als Erstes sagen; nichts umstellen); `⛔ STARTFRAGE`; `⛔ KEINE EINGABEZEILE`. **Probe nicht gelaufen — kein Abbruch, zählt nicht als Lauf** (wie TB-144, dort Z. 157): nach `⛔ ABBRUCH (Probe)`, `⛔ ABGEWIESEN` oder rc 1 den Grund aus der Zeile lesen; steht eine andere `claude`-Sitzung ohne Auftrag im Repo, sie beenden wie eine stehen gebliebene Probe-Sitzung (nächster Satz) und **einmal** neu proben; sonst, und nach `⛔ Konnte Probe-Ausloeser nicht wegraeumen`: melden, `PROBE: nicht gelaufen, <Grund>` nach `b_probe.txt`. Bleibt eine Probe-Sitzung stehen (`NICHT beendet`, rc 5): ihre PID bestimmen wie EIGEN (cwd im Repo, ≠ EIGEN, nach dieser Sitzung gestartet: `ps -o lstart= -p <pid>` gegen die eigene; sonst nicht beenden, melden), dann `kill -TERM <pid>`; ihr Fenster bleibt offen und steht im Ergebnis.

Je Lauf eine Zeile nach `docs/belege/TB-155/b_probe.txt`: `PROBE:` Fensternummer, Sekunden, Anmeldung, Ablaufwarnung ja oder nein, Zeilen `   | …`, davon ersetzt, Adresse ja oder nein, rc. Commit `TB-155 B: Probe`, pushen.

## Schritt C — Unterlagen

`PY WZ doku` ⇒ `c_doku.txt`. Soll rc 0, wie in 0b: `LIESMICH.md` L1 (Abschnitt „Gilt seit TB-155“) und L2 (eine Zeile „⭐ Gilt seit TB-155 …“), `Zeilen + 31 (entfernt 0)`; `BACKLOG.md` B1, `Zeilen + 8 (entfernt 0)`. Ein zweiter Lauf endet mit rc 2. Commit `TB-155 C: LIESMICH, BACKLOG`, pushen. **Nur gemeldet:** `LIESMICH.md` Z. 68 („Der steuernde Chat sieht nach jedem Start weiter selbst ins Fenster“) gilt weiter.

## Schritt D — Nachweis, Ergebnis, Journal, Abgabe

**D1.** `PY WZ nachweis` ⇒ `d1_nachweis.txt`. Soll rc 0, vierzehn Zeilen `…: ja`. **Abweichung: ABBRUCH, nichts richten.**
**D2.** `git diff ⟨S0⟩ HEAD -- docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` ⇒ `d2_diff_waechter.txt` (roh). Soll: Änderungen nur an S1–S4c. **Abweichung: ABBRUCH, nichts richten.**
**D3. Ergebnis** `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`, gegliedert wie das Ergebnis TB-144: Kopf · „Kurz“ (Soll | Ist je Schritt) · „Gemessen“ (Test unter bash 3.2; je Probelauf die Werte aus `b_probe.txt`; welcher erschlossene Wortlaut bestätigt ist, welcher offen bleibt) · „Abweichungen vom Auftrag“ (jede; sonst „keine“ mit den geprüften Sollwerten) · „Nicht getan“ (die Posten unter „Nicht in TB-155“; der Zweig des echten Starts lief nie; Aufgaben für den Betreiber) · „In einfacher Sprache“.
**D4. Journal.** Block nach `docs/belege/TB-155/d4_journal_block.md`: **Wortlaut aus Anhang B** (Gliederung wie Block ER), jede Stelle `<…>` durch den Wert der Sitzung ersetzt, sonst nichts geändert. Dann `PY WZ journal docs/belege/TB-155/d4_journal_block.md --probe` ⇒ `d4_journal_probe.txt`, ohne `--probe` ⇒ `d4_journal.txt`. Soll: `Ausgang … JOURNAL.md · 10910 Zeilen · … · md5 0ec0e4480a8adbb2b2cb14f83ab7a550` (weicht es ab: vermerken), sieben Bedingungen `ja`, rc 0, Kennung **ES** (beim Bau gemessen; nennt `WZ` eine andere, gilt die von `WZ`). rc 1: Bedingung lesen, Block richten, neu.
**D5.** Commit `TB-155 Abgabe: Ergebnis, Journal <Kennung>`, pushen. Dann `git status --porcelain > "$TMPDIR/tb155_d5.txt"`, unverändert nach `d5_porcelain.txt` (`cmp` gleich; Soll 0 B), und `git diff --numstat ⟨S0⟩ <Abgabe>` roh ⇒ `d5_numstat.txt`. Soll: `starte_sitzung.sh` `112	11` · `test_fensterinhalt.sh` `158	0` · `LIESMICH.md` `31	0` · `BACKLOG.md` `8	0` · `JOURNAL.md` Zeilen des eigenen Blocks + 3 · sonst nur Ergebnis und Belege. Letzter Commit `TB-155 D5: porcelain und numstat nach der Abgabe`, pushen; danach `git status --porcelain` noch einmal, Rohausgabe wörtlich in der Schlussmeldung.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab (Einträge oder HEAD); der sha256 des Werkzeugs weicht ab; ein Anker steht nicht genau einmal.
- 0b endet mit `FEHL` oder rc ≠ 0: nichts ist gebaut — **das in der Meldung als Erstes sagen.**
- **Claude Code lehnt einen Aufruf ab oder verlangt eine Bestätigung:** melden, nicht umgehen.
- Ein Schritt verlangte `osascript`, `launchctl`, eine Taste, ein Abmelden oder `/login`.
- A2 oder A3 weicht ab: erst der Rückweg, dann Abbruch. D1 oder D2 weicht ab: Abbruch, nichts richten.
- **Kontofund (Schritt B, Nr. 3):** Beleg nicht committen, nichts zitieren, Rückweg, Abbruch; als Erstes die Art der Angabe (ohne sie zu zitieren) in `docs/belege/TB-155/abbruch.txt`. *Grund:* Freigabe „Zeilen, Konto geschwärzt“ — ein Wächter, der das Konto stehen lässt, bleibt nicht scharf.
- Eine Datei ausserhalb der Liste müsste geändert werden; `git push` scheitert zweimal.

**Nach jedem Abbruch** steht `starte_sitzung.sh` am Stand ⟨S0⟩ oder am Stand aus A1. **Rückweg (A2, A3, Kontofund):** `git show ⟨S0⟩:docs/werkzeuge/sitzungswaechter/starte_sitzung.sh > "$TMPDIR/tb155_s0.sh"`, dann `PY WZ zurueck "$TMPDIR/tb155_s0.sh"` (prüft `bash -n`, speichert in einem Schritt). Danach gleicht `starte_sitzung.sh` ⟨S0⟩ und wird **nicht** committet (nach dem Commit A zeigt `git status` sie dann als geändert: so lassen); die Sitzung committet nur Belege, ruft `WZ waechter` nicht erneut, bricht ab und meldet. `test_fensterinhalt.sh` bleibt unverfolgt liegen (nach dem Commit A: verfolgt) und scheitert; die Sitzung löscht nichts und nennt die Datei in `docs/belege/TB-155/abbruch.txt`; aufgeräumt wird ausserhalb der Sitzung. **Kein Abbruch:** `doku` oder `journal` mit rc ≠ 0 (nichts geschrieben; melden); jeder andere Befund aus Schritt B; eine andere Kennung. Bei Abbruch: Belege committen, Grund in `docs/belege/TB-155/abbruch.txt`, pushen, melden.

## Nicht in TB-155

`ARBEITSWEISE.md` (nächster Regelwerk-Nachtrag); der Satz für die Sitzung; Chrome; `einschalten.sh` und die plist; die Ablage.

## In einfacher Sprache

Der kleine Wächter auf dem Mac startet für dich die Claude-Code-Sitzung und schreibt ins Protokoll, ob sie bereit ist. Bisher stand dort nur „eingabebereit“ — nicht, ob sie über dein Abo läuft oder ob deine Anmeldung bald abläuft. Künftig schreibt er die letzten zwölf Zeilen des neuen Fensters dazu (ohne die Zeile mit deinem Konto — eine Wortliste, kein Beweis) und sagt: Abo oder nicht, Ablaufwarnung ja oder nein. Ist Claude Code gar nicht angemeldet oder würde die Sitzung über die bezahlte API statt über dein Abo laufen, meldet er einen Fehler statt „eingabebereit“. Die Sitzung probiert das mindestens zweimal aus; dabei erscheinen in der Claude-App kurz Gerätesitzungen, die gleich wieder verschwinden. Die Sitzung meldet sich nie selbst an. Schreibt der Wächter „nicht angemeldet“, musst du dich selbst anmelden; was du danach tun musst, steht im Ergebnis.

## Anhang A — Werkzeug (darin wörtlich: Stücke S1–S4c, Test, L1, L2, B1)

### Werkzeug

```python
#!/usr/bin/env python3
"""TB-155 Werkzeug (Anhang A). Aendert nur die genannten Stellen, jeder Anker genau einmal; starte_sitzung.sh erst,
wenn die fertige Kopie bash -n und den Test besteht, dann in einem Schritt. Im Wurzelordner des Repos: waechter [--probe] |
doku [--probe] | journal <block> [--probe] | warte <Z0> <ziel> | beleg <quelle> <ziel> | zurueck <kopie> | nachweis.
rc 0 gut · 1 nichts gespeichert · 2 schon getan · 3 (nur warte) noch keine Schlusszeile."""
import hashlib, os, re, shutil, subprocess, sys, time
W = "docs/werkzeuge/sitzungswaechter/"
SH, LM, TEST = W + "starte_sitzung.sh", W + "LIESMICH.md", W + "test_fensterinhalt.sh"
BL, JO = "docs/projektfuehrung/BACKLOG.md", "docs/projektfuehrung/JOURNAL.md"
TMP = os.environ.get("TMPDIR", "/tmp").rstrip("/")
ERSATZ = "<<entfernt: Kontozeile>>"
KONTO = ("@", "claude max", "api usage billing", "claude pro", "claude team", "claude enterprise", "organization", "organisation", "welcome back", "logged in as", "account", "konto", "sk-", "api key", "api-key", "token", "secret", "password", "passwort", "api_key", "apikey", "bearer ", "ghp_", "github_pat_", "xoxb-", "aws_secret")
LOG = "logs/sitzungswaechter/waechter.log"
ENDE = ("----- fertig (probe), rc ", "⛔ ABBRUCH (Probe)", "⛔ ABGEWIESEN: Der Probe-Ausloeser", "⛔ Konnte Probe-Ausloeser nicht wegraeumen")  # nur die eigene Probe
JANKER = "\n---\n\n## Wiederkehrende Lehren\n"
A4 = r'''                    sage "⭐ EINGABEBEREIT ($kenn): Fenster $FENSTER, Eingabezeile steht, keine Frage offen (nach $summe s, Lesung $lesung). ⚠️ KEIN SATZ IM FENSTER."
                    return 0'''
S = [("S1 Kopf", r'''# ⛔ Ins Log gehen hoechstens die letzten 8 Zeilen (je 160 Zeichen) des NEU
#    GEOEFFNETEN Fensters, und nur, wenn die Pruefung scheitert. Sonst gilt der
#    Kopf dieser Datei: keine Umgebungsvariablen, Schluessel, Dateiinhalte.''', r'''# ⛔ SEIT TB-155 (Schranke 3 neu): Ins Log gehen hoechstens die letzten 12
#    nicht-leeren Zeilen (je 160 Zeichen) des NEU GEOEFFNETEN Fensters - bei
#    jeder ⛔-Zeile der Fensterpruefung UND bei ⭐ EINGABEBEREIT. Jede Zeile mit
#    einem Merkmal der Kontoregel (konto_ersetzen, Gross/Klein egal) wird vorher
#    durch "<<entfernt: Kontozeile>>" ersetzt, "/Users/<name>" durch "~".
#    ⚠️ Die Kontoregel ist eine Merkmalliste, kein Beweis: Ein Name ohne Merkmal
#    oder ein umbrochener Mailrest bleibt stehen. Dazu zwei eigene Zeilen:
#    "Anmeldung: …" und "Ablaufwarnung: …". Sonst gilt der Kopf dieser Datei:
#    keine Umgebungsvariablen, Schluessel, Dateiinhalte.'''),
     ("S2 Block", r'''# ⛔ Begrenzt: hoechstens 8 Zeilen, je 160 Zeichen, nur vom neu geoeffneten Fenster.
fensterzeilen() {
    local z
    sage "   Letzte Zeilen von Fenster $FENSTER (hoechstens 8, je 160 Zeichen):"
    printf '%s\n' "$1" | tr '\r' '\n' | grep -v '^[[:space:]]*$' | tail -n 8 | cut -c1-160 | while IFS= read -r z; do
        sage "   | $z"
    done
}''', r'''# >>> TB-155 FENSTERINHALT ANFANG (test_fensterinhalt.sh liest genau diesen Block)
# ⛔ Hoechstens 12 nicht-leere Zeilen, je 160 Zeichen, nur vom neu geoeffneten
#    Fenster, Kontozeilen ersetzt. Jede Funktion liest den Fensterinhalt von der
#    Standardeingabe und schreibt nur auf die Standardausgabe.
MERKMAL_ABO="Claude Max"
MERKMAL_API="API Usage Billing"
MERKMAL_ABGEMELDET="Not logged in"
MERKMAL_ABLAUF="expire"
ERSATZ_KONTO="<<entfernt: Kontozeile>>"

# Ein Wort: frage | eingabezeile | nichts. Die Frage geht vor (wie seit TB-144).
fenster_lage() {
    local t
    t=$(cat)
    case "$t" in
        *"$MERKMAL_FRAGE"*)        echo "frage" ;;
        *"$MERKMAL_EINGABEZEILE"*) echo "eingabezeile" ;;
        *)                         echo "nichts" ;;
    esac
}

# Abo | API | nicht angemeldet | unklar. Nicht angemeldet geht vor API, API vor Abo.
anmeldung_einordnen() {
    local t
    t=$(cat)
    case "$t" in
        *"$MERKMAL_ABGEMELDET"*) echo "nicht angemeldet" ;;
        *"$MERKMAL_API"*)        echo "API" ;;
        *"$MERKMAL_ABO"*)        echo "Abo" ;;
        *)                       echo "unklar" ;;
    esac
}

# Urteil fuer ein Fenster MIT Eingabezeile: bereit | nicht angemeldet | api.
# Nur "bereit" (Abo oder unklar) heisst EINGABEBEREIT.
eingabe_urteil() {
    case "$(anmeldung_einordnen)" in
        "nicht angemeldet") echo "nicht angemeldet" ;;
        API)                echo "api" ;;
        *)                  echo "bereit" ;;
    esac
}

# Kontoregel: eine MERKMALLISTE, kein Beweis - ein Name ohne Merkmal oder ein
# umbrochener Mailrest bleibt stehen. Vergleich ohne Gross/Klein (bash 3.2: ueber
# tr); in jeder Zeile wird "/Users/<name>" zu "~" (Name bis zum naechsten "/").
konto_ersetzen() {
    local z k
    LC_ALL=C sed 's|/Users/[^/]*|~|g' | while IFS= read -r z || [ -n "$z" ]; do
        k=$(printf '%s\n' "$z" | LC_ALL=C tr 'A-Z' 'a-z')
        case "$k" in
            *"@"*|*"claude max"*|*"api usage billing"*|*"claude pro"*|*"claude team"*|*"claude enterprise"*|*"organization"*|*"organisation"*|*"welcome back"*|*"logged in as"*|*"account"*|*"konto"*|*"sk-"*|*"api key"*|*"api-key"*|*"token"*|*"secret"*|*"password"*|*"passwort"*|*"api_key"*|*"apikey"*|*"bearer "*|*"ghp_"*|*"github_pat_"*|*"xoxb-"*|*"aws_secret"*)
                printf '%s\n' "$ERSATZ_KONTO" ;;
            *)  printf '%s\n' "$z" ;;
        esac
    done
}

# Schnitt auf 160 ZEICHEN. LC_ALL, damit cut auch unter launchd (dort ohne
# Sprachumgebung) Zeichen zaehlt und keines zerschneidet: ERSCHLOSSEN, nur am
# Mac messbar (der Test misst es: "Schnitt: 202 Striche").
schnitt() {
    LC_ALL=en_US.UTF-8 cut -c1-160
}

# Die erste Zeile mit der Ablaufwarnung (Kontozeile ersetzt); leer, wenn keine.
ablaufwarnung() {
    tr '\r' '\n' | grep -i -- "$MERKMAL_ABLAUF" | head -n 1 | konto_ersetzen | sed 's/^[[:space:]]*//' | schnitt
}

# Die letzten 12 Zeilen, die NACH Kontoregel und Schnitt nicht leer sind. Die
# Kontoregel laeuft vor dem Schnitt (ein "@" hinter Spalte 160 zaehlt).
fenster_ausschnitt() {
    tr '\r' '\n' | grep -v '^[[:space:]]*$' | konto_ersetzen | schnitt | LC_ALL=C grep -v '^[[:space:]]*$' | tail -n 12
}
# <<< TB-155 FENSTERINHALT ENDE

# Schreibt Anmeldung, Ablaufwarnung und den Ausschnitt ins Log. $1 = Fensterinhalt.
fensterzeilen() {
    local z w
    case "$1" in *[![:space:]]*) : ;; *)
        sage "   Fensterinhalt leer oder nicht lesbar: keine Anmeldung, keine Ablaufwarnung, keine Zeilen."
        return 0 ;;
    esac
    sage "   Anmeldung: $(printf '%s\n' "$1" | anmeldung_einordnen)"
    w=$(printf '%s\n' "$1" | ablaufwarnung)
    if [ -n "$w" ]; then sage "   Ablaufwarnung: ja | $w"; else sage "   Ablaufwarnung: nein"; fi
    sage "   Letzte Zeilen von Fenster $FENSTER (hoechstens 12, je 160 Zeichen, Kontozeilen ersetzt):"
    printf '%s\n' "$1" | fenster_ausschnitt | while IFS= read -r z; do
        sage "   | $z"
    done
}'''),
     ("S3 Rueckgabe", r'''# Rueckgabe: 0 eingabebereit · 3 Startfrage · 4 keine Eingabezeile.''', r'''# Rueckgabe: 0 eingabebereit · 3 Startfrage · 4 keine Eingabezeile · 6 nicht angemeldet · 7 API-Abrechnung (6, 7 seit TB-155).'''),
     ("S4a Frage", r'''        case "$inhalt" in
            *"$MERKMAL_FRAGE"*)''', r'''        case "$(printf '%s\n' "$inhalt" | fenster_lage)" in
            frage)'''),
     ("S4b Eingabezeile", r'''            *"$MERKMAL_EINGABEZEILE"*)
                bereit=$((bereit+1))''', r'''            eingabezeile)
                bereit=$((bereit+1))'''),
     ("S4c angemeldet", A4, r'''                    case "$(printf '%s\n' "$inhalt" | eingabe_urteil)" in
                        "nicht angemeldet")
                            sage "⛔ NICHT ANGEMELDET ($kenn): Fenster $FENSTER zeigt nach $summe s die Eingabezeile, nennt aber \"$MERKMAL_ABGEMELDET\" (Lesung $lesung). Die Sitzung ist NICHT eingabebereit."
                            fensterzeilen "$inhalt"
                            return 6 ;;
                        api)
                            sage "⛔ API-ABRECHNUNG ($kenn): Fenster $FENSTER zeigt nach $summe s die Eingabezeile, nennt aber \"$MERKMAL_API\" (Lesung $lesung). Die Sitzung liefe ueber API-Abrechnung statt ueber das Abo und ist NICHT eingabebereit."
                            fensterzeilen "$inhalt"
                            return 7 ;;
                    esac''' + "\n" + A4.replace("\n", '\n                    fensterzeilen "$inhalt"\n'))]
L1A, L2A, B1A = "\n" + r'''## ⭐⭐ Gilt seit TB-144 (Wächter-Reparatur)''' + "\n", r'''und in keiner `Enter to confirm`.''' + "\n", "\n" + r'''## 6 — Geparkt'''
L1 = r'''## ⭐⭐ Gilt seit TB-155 (Fensterinhalt im Log)

**Dieser Abschnitt geht dem Abschnitt „Gilt seit TB-144“ vor, wo beide sich widersprechen** (dort: „höchstens 8, je 160 Zeichen“, nur bei ⛔).

Unter „⭐ EINGABEBEREIT“ und unter jeder ⛔-Zeile der Fensterprüfung („⛔ STARTFRAGE“, „⛔ KEINE EINGABEZEILE“, „⛔ NICHT ANGEMELDET“, „⛔ API-ABRECHNUNG“) stehen jetzt:

%%%
   Anmeldung: Abo                 (oder: API · nicht angemeldet · unklar)
   Ablaufwarnung: nein            (oder: Ablaufwarnung: ja | <die Zeile im Wortlaut>)
   Letzte Zeilen von Fenster <n> (hoechstens 12, je 160 Zeichen, Kontozeilen ersetzt):
   | <Zeile>
%%%

Bei leerem oder nicht lesbarem Fensterinhalt steht unter „⛔ KEINE EINGABEZEILE“ nur: `   Fensterinhalt leer oder nicht lesbar: keine Anmeldung, keine Ablaufwarnung, keine Zeilen.`

**Die drei folgenden Regeln sind Lesarten — erschlossen, vorläufig:**

- **Anmeldung:** „Abo“ bei `Claude Max`, „API“ bei `API Usage Billing`, „nicht angemeldet“ bei `Not logged in`, sonst „unklar“; treffen mehrere zu: nicht angemeldet vor API vor Abo.
- **Ablaufwarnung:** die erste Zeile mit `expire` (Gross- und Kleinschreibung egal).
- **Kontozeilen — eine Merkmalliste, kein Beweis:** Trägt eine Zeile (Gross/Klein egal) eines der Merkmale `@`, `claude max`, `api usage billing`, `claude pro`, `claude team`, `claude enterprise`, `organization`, `organisation`, `welcome back`, `logged in as`, `account`, `konto`, `sk-`, `api key`, `api-key`, `token`, `secret`, `password`, `passwort`, `api_key`, `apikey`, `bearer `, `ghp_`, `github_pat_`, `xoxb-`, `aws_secret`, wird sie durch `<<entfernt: Kontozeile>>` ersetzt, bei ⭐ und bei ⛔; `/Users/<name>` wird zu `~` (Name bis zum nächsten `/`; im Beleg in jeder Zeile). **Ein Name ohne Merkmal oder ein umbrochener Mailrest bleibt stehen** — vor dem Weitergeben eines Log-Ausschnitts selbst nach Konto, Name und Schlüssel sehen. Die Adresse der Sitzung (`https://claude.ai/code/session_…`) bleibt im Klartext.
- **⛔ NICHT ANGEMELDET (TB-<Nr>)** (Rückgabewert 6) oder **⛔ API-ABRECHNUNG (TB-<Nr>)** (Rückgabewert 7) statt „⭐ EINGABEBEREIT“, wenn die Eingabezeile steht, das Fenster aber `Not logged in` oder `API Usage Billing` nennt (über die API liefe die Sitzung auf Rechnung statt über das Abo). Beim echten Start bleibt das Fenster offen; die Probe versucht bei jeder Rückgabe der Prüfung, ihr Fenster zu schliessen — ob es geschlossen ist oder offen bleibt, steht im Log. „Anmeldung: unklar“ bleibt „⭐ EINGABEBEREIT“. Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing` sind erschlossen, nicht gemessen (Stand: `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`).

**Schranke 3, neu:** höchstens 12 nicht-leere Zeilen je 160 Zeichen des **neu geöffneten** Fensters, Kontozeilen ersetzt (nach dem Kürzen leere Zeilen zählen nicht); unverändert keine Umgebungsvariablen, Schlüssel, Dateiinhalte. Das Log wird nicht gepusht; in Belegen wird zusätzlich die Zeile der Ablaufwarnung ersetzt.

**Test ohne Fenster:** `/bin/bash docs/werkzeuge/sitzungswaechter/test_fensterinhalt.sh`; Soll: letzte Zeile `Test Fensterinhalt: <n> ok, 0 FEHL`, Rückgabewert 0.

**In einfacher Sprache:** Der Wächter schreibt jetzt immer ins Protokoll, was im neuen Fenster steht (zwölf Zeilen, ohne die Zeile mit deinem Konto), ob die Sitzung über dein Abo läuft und ob die Anmeldung bald abläuft. Ist Claude Code nicht angemeldet oder liefe die Sitzung über die bezahlte API statt über dein Abo, meldet er einen Fehler. Die Zeile mit deinem Konto erkennt er an einer Wortliste — das ist kein Beweis.'''.replace("%%%", "`" * 3)
L2 = r'''⭐ **Gilt seit TB-155 (Abschnitt „Gilt seit TB-155“ oben):** höchstens 12 Zeilen, auch unter „⭐ EINGABEBEREIT“, Kontozeilen ersetzt.'''
B1 = r'''### Sitzungswächter schreibt den Fensterinhalt ins Log (11.10.2026) — eingetragen mit TB-155

- **Freigabe:** Einzelfreigabe des Betreibers, Auswahlkarten vom 11.10.2026, 11:01 und 13:00 (Antwort 13:02): 12 Fensterzeilen unter „⭐ EINGABEBEREIT“, Kontozeile ersetzt, Anmeldung und Ablaufwarnung als eigene Zeilen; Wortlaut in `docs/auftraege/MAC_TB-155_waechter_fensterinhalt.md`.
- **Vorgaben des steuernden Chats, dem Betreiber genannt, ohne Widerspruch:** „⛔ NICHT ANGEMELDET“ (Rückgabewert 6) und „⛔ API-ABRECHNUNG“ (7) statt „⭐ EINGABEBEREIT“; 12 Zeilen und Ersetzen auch bei ⛔; Adresse der Sitzung im Klartext; erster versionierter Test (`test_fensterinhalt.sh`). Quelle: `UEBERGABE.md`, Umzug 11.10.2026, 14:13, Block 4 Nr. 2 und Block 6.
- **Geändert:** `docs/werkzeuge/sitzungswaechter/starte_sitzung.sh` schreibt unter „⭐ EINGABEBEREIT“ und unter jeder ⛔-Zeile der Fensterprüfung „Anmeldung: …“, „Ablaufwarnung: …“ und die letzten 12 nicht-leeren Zeilen des neu geöffneten Fensters ins Log, Kontozeilen ersetzt; dazu die zwei neuen ⛔-Zeilen. Schranke 3, Kontoregel und Test: `LIESMICH.md` dort, „Gilt seit TB-155“.
- **Erschlossen, nicht gemessen (Lesarten, vorläufig):** Wortlaut und Stelle von `Not logged in` und der Zeile bei `API Usage Billing`; „Abo“ = `Claude Max`; Ablaufwarnung = Zeile mit `expire`; die Kontoregel (Merkmalliste, kein Beweis: ein Name ohne Merkmal oder ein umbrochener Mailrest bleibt stehen). Gemessenes: `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`.
- **Nicht in TB-155:** `ARBEITSWEISE.md` (nächster Regelwerk-Nachtrag), der Satz für die Sitzung, Chrome, `einschalten.sh`, die plist.'''
D = {LM: [("L1 Abschnitt", L1A, "\n" + L1 + "\n\n---\n" + L1A), ("L2 Zeile", L2A, L2A + L2 + "\n")],
     BL: [("B1 Block", B1A, "\n" + B1 + "\n" + B1A)]}
TESTTEXT = r'''#!/bin/bash
# Test des Sitzungswaechters (seit TB-155), OHNE Fenster: liest aus
# starte_sitzung.sh zwei Merkmale, den Block "TB-155 FENSTERINHALT" und die
# Funktionen fensterzeilen und warte_auf_eingabezeile und fuehrt genau diese
# Bytes aus; schreibt keine Datei. ATTRAPPEN: sage, sleep, fenster_lesen.
# Fenster NACHGEBAUT (docs/belege/TB-144/b_m2_3.txt); Konto-, Anmelde-,
# API-Zeile und Ablaufwarnung ERFUNDEN (Wortlaut des Erbauers, nicht gemessen).
# Aufruf: /bin/bash docs/werkzeuge/sitzungswaechter/test_fensterinhalt.sh [starte_sitzung.sh]
set -u
S="${1:-$(dirname "$0")/starte_sitzung.sh}"
eval "$(grep -E '^MERKMAL_(FRAGE|EINGABEZEILE)=' "$S")"
BLOCK=$(sed -n '/^# >>> TB-155 FENSTERINHALT ANFANG/,/^# <<< TB-155 FENSTERINHALT ENDE/p' "$S")
[ -n "$BLOCK" ] || { echo "FEHL: Block TB-155 nicht gefunden in $S"; echo "Test Fensterinhalt: 0 ok, 1 FEHL"; exit 2; }
eval "$BLOCK"
funktion() { sed -n "/^$1() {\$/,/^}\$/p" "$S"; }
eval "$(funktion fensterzeilen)"
eval "$(funktion warte_auf_eingabezeile)"
sage() { printf '%s\n' "$*"; }
sleep() { :; }
fenster_lesen() { "$FX"; }
lauf() { FX="$1"; warte_auf_eingabezeile TEST; }
logzahl() { printf '%s\n' "$AUS" | grep -c "$@"; }
STUFEN="0 0 0"; FENSTER=4711; FX=fx_abo; AUS=""
OK=0; FEHL=0
gleich() {
    if [ "$2" = "$3" ]; then OK=$((OK+1)); echo "ok   $1"
    else FEHL=$((FEHL+1)); echo "FEHL $1"; echo "     Ist:  $2"; echo "     Soll: $3"; fi
}
zahl() { wc -l | tr -d ' '; }
ersetzt() { fenster_ausschnitt | grep -c "^$ERSATZ_KONTO\$"; }

# >>> FENSTER (nachgebaut)
# Quelle b_m2_3.txt: L1, L3, fuss, ADR ohne Kennung; fx_frage: Auftrag TB-144.
# Wortlaut des Erbauers, nicht gemessen: "Opus 5.5 ·" vor Claude Max und vor
# API Usage Billing, "Not logged in · Run /login", WARN, jede Zeile mit "@",
# "Welcome back", fx_shell, fx_ablaufkonto, die Kennung in ADR.
L1='▗ ▗   ▖ ▖  Claude Code v2.1.295'
L3=' ▘▘   ▝▝   ~/trading-bot · /rc'
ADR='  /remote-control is active · Continue here, on your phone, or at https://claude.ai/code/session_01TESTtestTESTtestTESTtest'
WARN='Login expires soon'
fuss() { printf '%s\n' '' '────────' '❯ Try "fix typecheck errors"' '────────' '  ⏸ manual mode on · ? for shortcuts · ← for agents' ''; }
fx_abo() { printf '%s\n' '' "$L1" '           Opus 5.5 · Claude Max' "$L3" '' "$ADR"; fuss; }
fx_api() { printf '%s\n' '' "$L1" '           Opus 5.5 · API Usage Billing' "$L3" '' "$ADR"; fuss; }
fx_abgemeldet() { printf '%s\n' '' "$L1" '           Not logged in · Run /login' "$L3"; fuss; }
fx_ablauf() { printf '%s\n' '' "$L1" '           Opus 5.5 · Claude Max' "$L3" '' "  $WARN" '' "$ADR"; fuss; }
fx_konto() { printf '%s\n' '' "$L1" '           Opus 5.5 · Claude Max · vorname.name@example.org' "$L3" '  Welcome back Vorname!' "  $(printf '%0170d' 0) spaet@example.org" "$ADR"; fuss; }
fx_frage() { printf '%s\n' '' ' Teach auto mode about your environment?' '' ' Enter to confirm · Esc to cancel'; }
fx_lang() { local i=1; while [ "$i" -le 20 ]; do echo "Zeile $i"; i=$((i+1)); done; fuss; }
fx_shell() { printf '%s\n' 'Last login: Sun Oct 11 12:00:00 on ttys017' 'rechner:trading-bot nutzer$ '; }
fx_leer() { :; }
fx_ablaufkonto() { fx_abo; printf '%s\n' '  Login of a@example.org expires soon'; }
fx_rand() { local i=1; while [ "$i" -le 13 ]; do echo "Zeile $i"; i=$((i+1)); done; printf '%0170d\n' 0 | sed 's/0/ /g; s/$/spaet/'; }
striche() { printf "%0$1d\n" 0 | sed 's/0/─/g'; }
# <<< FENSTER

gleich "Abo" "$(fx_abo | anmeldung_einordnen)" "Abo"
gleich "Abo, Gegenprobe" "$(fx_abo | grep -v "$MERKMAL_ABO" | anmeldung_einordnen)" "unklar"
gleich "Abo: eine Zeile ersetzt" "$(fx_abo | ersetzt)" "1"
gleich "Abo: Adresse im Klartext" "$(fx_abo | fenster_ausschnitt | grep -c "^$ADR\$")" "1"
gleich "API" "$(fx_api | anmeldung_einordnen)" "API"
gleich "API, Gegenprobe" "$(fx_api | sed "s/$MERKMAL_API/$MERKMAL_ABO/" | anmeldung_einordnen)" "Abo"
gleich "API vor Abo" "$( { fx_abo; fx_api; } | anmeldung_einordnen)" "API"
gleich "Nicht angemeldet" "$(fx_abgemeldet | anmeldung_einordnen)" "nicht angemeldet"
gleich "Nicht angemeldet, Gegenprobe" "$(fx_abgemeldet | grep -v "$MERKMAL_ABGEMELDET" | anmeldung_einordnen)" "unklar"
gleich "Nicht angemeldet vor Abo und API" "$( { fx_abo; fx_api; fx_abgemeldet; } | anmeldung_einordnen)" "nicht angemeldet"
gleich "Nicht angemeldet: Lage eingabezeile" "$(fx_abgemeldet | fenster_lage)" "eingabezeile"
gleich "Ablauf: Zeile im Wortlaut" "$(fx_ablauf | ablaufwarnung)" "$WARN"
gleich "Ablauf, Gegenprobe" "$(fx_abo | ablaufwarnung)" ""
gleich "Ablauf: Warnung mit @ ersetzt" "$(printf '%s\n' "  Login of a@example.org EXPIRED" | ablaufwarnung)" "$ERSATZ_KONTO"
gleich "Konto: Fenster hat zwei Zeilen mit @" "$(fx_konto | grep -c '@')" "2"
gleich "Konto: Ausschnitt hat keine" "$(fx_konto | fenster_ausschnitt | grep -c '@')" "0"
gleich "Konto: drei ersetzt (auch @ hinter Spalte 160, Welcome back)" "$(fx_konto | ersetzt)" "3"
gleich "Konto, Gegenprobe ohne Kontozeile" "$(fx_frage | fenster_ausschnitt)" "$(fx_frage | grep -v '^[[:space:]]*$')"
gleich "Startfrage" "$(fx_frage | fenster_lage)" "frage"
gleich "Startfrage, Gegenprobe" "$(fx_frage | grep -v "$MERKMAL_FRAGE" | fenster_lage)" "nichts"
gleich "Startfrage vor Eingabezeile" "$( { fx_frage; fuss; } | fenster_lage)" "frage"
gleich "Grenze: 12 Zeilen" "$(fx_lang | fenster_ausschnitt | zahl)" "12"
gleich "Grenze: die LETZTEN 12" "$(fx_lang | fenster_ausschnitt | head -n 1)" "Zeile 13"
LANG_Z=$(printf '%0200d\n' 0 | fenster_ausschnitt)
gleich "Grenze: 160 Zeichen" "${#LANG_Z}" "160"
gleich "Abo: Lage eingabezeile" "$(fx_abo | fenster_lage)" "eingabezeile"
gleich "API: eine Zeile ersetzt" "$(fx_api | ersetzt)" "1"
gleich "Nicht angemeldet: nichts ersetzt" "$(fx_abgemeldet | ersetzt)" "0"
gleich "Konto: Adresse im Klartext" "$(fx_konto | fenster_ausschnitt | grep -c "^$ADR\$")" "1"
gleich "Startfrage: Anmeldung unklar" "$(fx_frage | anmeldung_einordnen)" "unklar"
gleich "Grenze: CR trennt Zeilen" "$(printf 'a\rb\r' | fenster_ausschnitt | zahl)" "2"
gleich "Grenze: leerer Inhalt, keine Zeile" "$(printf '\n  \n' | fenster_ausschnitt | zahl)" "0"
gleich "Urteil Abo: bereit" "$(fx_abo | eingabe_urteil)" "bereit"
gleich "Urteil API: api (nicht eingabebereit)" "$(fx_api | eingabe_urteil)" "api"
gleich "Urteil API, Gegenprobe mit Abo-Zeile: bereit" "$(fx_api | sed "s/$MERKMAL_API/$MERKMAL_ABO/" | eingabe_urteil)" "bereit"
gleich "Urteil nicht angemeldet" "$(fx_abgemeldet | eingabe_urteil)" "nicht angemeldet"
gleich "Urteil unklar: bereit" "$(fx_abo | grep -v "$MERKMAL_ABO" | eingabe_urteil)" "bereit"
gleich "Schnitt: 202 Striche werden 160 ganze Zeichen" "$(striche 202 | fenster_ausschnitt)" "$(striche 160)"
gleich "Leer nach dem Schnitt: zaehlt nicht mit (12 Zeilen)" "$(fx_rand | fenster_ausschnitt | zahl)" "12"
gleich "Leer nach dem Schnitt: die LETZTEN 12 ohne sie" "$(fx_rand | fenster_ausschnitt | head -n 1)" "Zeile 2"
gleich "Leer nach dem Schnitt: keine leere Zeile im Ausschnitt" "$(fx_rand | fenster_ausschnitt | grep -c '^[[:space:]]*$')" "0"
gleich "Pfad: /Users/<name> wird ~" "$(printf '%s\n' '  cwd: /Users/vorname.nachname/trading-bot und /Users/zwei' | konto_ersetzen)" "  cwd: ~/trading-bot und ~"
gleich "Pfad, Gegenprobe" "$(printf '%s\n' '  /Usersicht und Users/name' | konto_ersetzen)" "  /Usersicht und Users/name"
gleich "Pfad mit Leerzeichen im Namen" "$(printf '%s\n' '  /Users/Vorname Nachname/a' | konto_ersetzen)" "  ~/a"

# Kontoregel: je Merkmal ein Testfall (GROSS) und eine Gegenprobe (dem Merkmal
# fehlt das letzte Zeichen). Eigene Liste: fehlt eines im Skript, wird es rot
# (ausser aws_secret: es enthaelt secret).
while IFS= read -r m; do
    g=$(printf '%s\n' "$m" | LC_ALL=C tr 'a-z' 'A-Z')
    gleich "Kontoregel '$m'" "$(printf '%s\n' "  vor [$g] nach" | konto_ersetzen)" "$ERSATZ_KONTO"
    gleich "Kontoregel '$m', Gegenprobe" "$(printf '%s\n' "  vor [${m%?}] nach" | konto_ersetzen)" "  vor [${m%?}] nach"
done <<'MERKMALE'
@
claude max
api usage billing
claude pro
claude team
claude enterprise
organization
organisation
welcome back
logged in as
account
konto
sk-
api key
api-key
token
secret
password
passwort
api_key
apikey
bearer 
ghp_
github_pat_
xoxb-
aws_secret
MERKMALE

# Verdrahtung: fensterzeilen und warte_auf_eingabezeile, mit den Attrappen.
AUS=$(lauf fx_abo); gleich "Lauf Abo: rc 0" "$?" "0"
gleich "Lauf Abo: EINGABEBEREIT und Anmeldung Abo" "$(logzahl -e '^⭐ EINGABEBEREIT (TEST)' -e '^   Anmeldung: Abo$')" "2"
gleich "Lauf Abo: Kontozeile im Log ersetzt" "$(logzahl "^   | $ERSATZ_KONTO\$")" "1"
gleich "Lauf Abo: Abo-Zeile steht nicht im Log" "$(printf '%s\n' "$AUS" | grep '^   | ' | grep -c "$MERKMAL_ABO")" "0"
AUS=$(lauf fx_api); gleich "Lauf API: rc 7" "$?" "7"
gleich "Lauf API: API-ABRECHNUNG statt EINGABEBEREIT" "$(logzahl -e 'API-ABRECHNUNG (TEST)' -e 'EINGABEBEREIT (TEST)')" "1"
AUS=$(lauf fx_abgemeldet); gleich "Lauf nicht angemeldet: rc 6" "$?" "6"
gleich "Lauf nicht angemeldet: NICHT ANGEMELDET statt EINGABEBEREIT" "$(logzahl -e 'NICHT ANGEMELDET (TEST)' -e 'EINGABEBEREIT (TEST)')" "1"
AUS=$(lauf fx_frage); gleich "Lauf Startfrage: rc 3" "$?" "3"
AUS=$(lauf fx_shell); gleich "Lauf ohne Eingabezeile: rc 4" "$?" "4"
AUS=$(lauf fx_leer); gleich "Lauf leeres Fenster: rc 4" "$?" "4"
gleich "Lauf leeres Fenster: 'leer oder nicht lesbar', keine Fensterzeile" "$(logzahl -e 'Fensterinhalt leer oder nicht lesbar' -e '^   | ')" "1"
AUS=$(lauf fx_lang); gleich "Lauf langes Fenster: rc 0" "$?" "0"
gleich "Lauf langes Fenster: 12 Fensterzeilen im Log" "$(logzahl '^   | ')" "12"
AUS=$(lauf fx_api); gleich "Lauf API: fensterzeilen gerufen" "$(logzahl '^   Anmeldung: API$')" "1"
AUS=$(lauf fx_abgemeldet); gleich "Lauf nicht angemeldet: fensterzeilen gerufen" "$(logzahl '^   Anmeldung: nicht angemeldet$')" "1"
AUS=$(lauf fx_frage); gleich "Lauf Startfrage: fensterzeilen gerufen" "$(logzahl '^   Anmeldung: unklar$')" "1"
AUS=$(lauf fx_ablaufkonto); gleich "Lauf Ablaufwarnung mit @: im Log ersetzt" "$(logzahl -F "   Ablaufwarnung: ja | $ERSATZ_KONTO")" "1"

echo "Test Fensterinhalt: $OK ok, $FEHL FEHL"
[ "$FEHL" -eq 0 ]''' + "\n"
LOGTEILE = ("⛔ NICHT ANGEMELDET (", "⛔ API-ABRECHNUNG (", "Anmeldung: ", "Ablaufwarnung: ja | ", "Ablaufwarnung: nein", "(hoechstens 12, je 160 Zeichen, Kontozeilen ersetzt):", "Fensterinhalt leer oder nicht lesbar")

def lies(p):
    with open(p, encoding="utf-8", newline="") as f: return f.read()
def kenn(t): return "%d Zeilen · %d B · md5 %s" % (t.count("\n"), len(t.encode("utf-8")), hashlib.md5(t.encode("utf-8")).hexdigest())
def setze(t, stuecke, wo):
    u = t
    for name, alt, neu in stuecke:
        n, m = t.count(alt), u.count(alt)
        print("%s · %s · Anker %d (Soll 1) · Zeilen %d -> %d" % (wo, name, n, alt.strip("\n").count("\n") + 1, neu.strip("\n").count("\n") + 1))
        if n != 1 or m != 1: raise SystemExit("rc 1: Anker '%s' steht nicht genau einmal (%d, %d). Nichts gespeichert." % (name, n, m))
        u = u.replace(alt, neu)
    return u
def speichere(p, t):
    with open(p + ".tb155_neu", "w", encoding="utf-8", newline="") as f: f.write(t)
    if os.path.exists(p): shutil.copymode(p, p + ".tb155_neu")
    os.replace(p + ".tb155_neu", p)
def bash(*a):
    r = subprocess.run(["/bin/bash"] + list(a), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.rstrip("\n")
def letzte(t): return re.findall(r"(?m)^## ([A-Z]{2}) — ", t[:t.index(JANKER)])[-1]
def nach(k): return k[0] + chr(ord(k[1]) + 1) if k[1] != "Z" else chr(ord(k[0]) + 1) + "A"
def zw(s, a, b):
    i = s.find(a); j = s.find(b, i + 1)
    return s[i:j] if i >= 0 and j >= 0 else ""

def waechter(probe):
    alt = lies(SH)
    print("Ausgang %s · %s" % (SH, kenn(alt)))
    if "TB-155 FENSTERINHALT ANFANG" in alt or os.path.exists(TEST):
        print("schon gebaut. Nichts getan."); return 2
    neu = setze(alt, S, "starte_sitzung.sh")
    k, t = TMP + "/tb155_starte_sitzung.sh", TMP + "/tb155_test_fensterinhalt.sh"
    for p, x in ((k, neu), (t, TESTTEXT)):
        with open(p, "w", encoding="utf-8", newline="") as f: f.write(x)
    (r1, a1), (r2, a2) = bash("-n", k), bash(t, k)
    print("Kopie %s · %s" % (k, kenn(neu))); print("bash -n rc %d %s" % (r1, a1)); print(a2); print("Test rc %d" % r2)
    if r1 or r2: print("Die Kopie besteht bash -n oder den Test nicht. Nichts gespeichert."); return 1
    if probe: print("Probe: im Repo nichts geschrieben."); return 0
    speichere(TEST, TESTTEXT); speichere(SH, neu)
    print("gespeichert %s · %s" % (SH, kenn(lies(SH)))); print("neu %s · %s" % (TEST, kenn(lies(TEST))))
    return 0

def doku(probe):
    neu = {}
    for p, st in D.items():
        t = lies(p)
        print("Ausgang %s · %s" % (p, kenn(t)))
        if any(n in t for _, _, n in st): print("schon eingetragen in %s. Nichts getan." % p); return 2
        neu[p] = setze(t, st, os.path.basename(p))
        print("%s · Zeilen + %d (entfernt 0)" % (p, neu[p].count("\n") - t.count("\n")))
    if probe: print("Probe: nichts geschrieben."); return 0
    for p, t in neu.items(): speichere(p, t)
    return 0

def journal(datei, probe):
    t, z = lies(JO), lies(datei).strip("\n").split("\n")
    soll = nach(letzte(t))
    print("Ausgang %s · %s" % (JO, kenn(t)))
    bed = [("Anker genau einmal", t.count(JANKER) == 1),
           ("Kopfzeile '## %s — TB-155: …'" % soll, z[0].startswith("## %s — TB-155: " % soll)),
           ("'### Was gemessen ist', '### Was offen bleibt' je einmal", z.count("### Was gemessen ist") == 1 and z.count("### Was offen bleibt") == 1),
           ("kein '---', keine zweite '## '-Zeile", "---" not in z and sum(x.startswith("## ") for x in z) == 1),
           ("Schlusszeile '*Geschrieben … von der Mac-Sitzung TB-155. Quellenvermerk: siehe Kopf.*'", z[-1].startswith("*Geschrieben ") and z[-1].endswith(" von der Mac-Sitzung TB-155. Quellenvermerk: siehe Kopf.*")),
           ("Block noch nicht im Journal", z[0] not in t),
           ("keine offene Stelle '<…>' im Block", not re.search(r"(?<!<)<[^<>`\n]+>(?!>)", "\n".join(z)))]
    for n, ok in bed: print("%s: %s" % (n, "ja" if ok else "NEIN"))
    print("Kennung %s · Zeilen + %d (entfernt 0)" % (soll, len(z) + 3))
    if not all(ok for _, ok in bed): return 1
    if probe: print("Probe: nichts geschrieben."); return 0
    speichere(JO, t.replace(JANKER, "\n---\n\n" + "\n".join(z) + "\n" + JANKER))
    return 0

def beleg(quelle, ziel):
    if os.path.exists(ziel): print("gibt es schon: %s. Nichts getan." % ziel); return 2
    with open(quelle, "rb") as f: roh = f.read()
    text = roh.decode("utf-8", errors="replace")  # zerschnittene Zeichen brechen nicht ab, sie werden gezaehlt
    kaputt = text.count("�") - roh.count("�".encode("utf-8"))
    aus, n, marke, fz = [], 0, "Ablaufwarnung: ja | ", "   | "
    for z in text.split("\n"):
        k = z.lower()
        if marke in z and not z.endswith(marke + ERSATZ): z = z[:z.index(marke) + len(marke)] + ERSATZ; n += 1
        elif marke not in z and not z.endswith(fz + ERSATZ) and ("@" in z or (fz in z and ("expire" in k or any(m in k for m in KONTO)))): z = ERSATZ; n += 1  # Fensterzeilen tragen "   | "
        aus.append(re.sub(r"/Users/[^/\n]*", "~", z))  # Heimordner in JEDER Zeile, Name bis zum naechsten "/"
    t = "\n".join(aus)
    t += ("" if t.endswith("\n") or not t else "\n") + "WZ beleg: zerschnittene Zeichen (kein gueltiges UTF-8), durch U+FFFD ersetzt: %d\n" % kaputt
    speichere(ziel, t)
    print("%s · %s · ersetzt %d Zeilen · Zeilen mit '@' danach %d · zerschnittene Zeichen %d" % (ziel, kenn(t), n, sum("@" in z for z in aus), kaputt))
    if kaputt: print("BEFUND, kein Abbruch: %d zerschnittene Zeichen im Log-Ausschnitt (der Schnitt zaehlt Bytes). Ins Ergebnis." % kaputt)
    return 0

def warte(z0, ziel):
    if not z0.isdigit() or os.path.dirname(os.path.abspath(ziel)) != os.path.abspath(TMP) or os.path.exists(ziel):
        print("Aufruf: warte <Z0> <neue Datei in $TMPDIR>. Nichts geschrieben."); return 1
    for i in range(11):
        with open(LOG, "rb") as f: neu = f.read().split(b"\n")[int(z0):]
        e = [x for x in ENDE if any(x.encode("utf-8") in z for z in neu)]
        if e or i == 10: break
        time.sleep(10)
    if not e: print("nach 100 s keine Schlusszeile hinter Zeile %s (%d neue Zeilen). Nichts geschrieben." % (z0, len(neu) - 1)); return 3
    with open(ziel, "wb") as f: f.write(b"\n".join(neu))
    print("%s · %d Zeilen ab Zeile %d · Schlusszeile: %s" % (ziel, len(neu) - 1, int(z0) + 1, " | ".join(e)))
    return 0

def zurueck(datei):
    r, a = bash("-n", datei)
    print("bash -n rc %d %s" % (r, a))
    if r: return 1
    speichere(SH, lies(datei)); print("gespeichert %s · %s" % (SH, kenn(lies(SH))))
    return 0

def nachweis():
    t, lm = lies(SH), lies(LM)
    c = "\n".join(z for z in t.split("\n") if not z.lstrip().startswith("#"))
    (r1, _), (r2, a2) = bash("-n", SH), bash(TEST)
    pr = [("bash -n rc 0", r1 == 0), ("Test rc 0 · " + a2.split("\n")[-1], r2 == 0),
          ("'do script' in Befehlszeilen 1", c.count("do script") == 1),
          ("'--permission-mode manual' in Befehlszeilen 1", c.count("--permission-mode manual") == 1),
          ("kein offener Platzhalter (der Ersatztext der Kontozeile zaehlt nicht)", [z for z in c.split("\n") if '="<<' in z] == ['ERSATZ_KONTO="%s"' % ERSATZ]),
          ("keystroke, System Events, ' in window' 0", not any(w in c for w in ("keystroke", "System Events", " in window"))),
          ("bash-4-Mittel 0", not re.search(r"declare -A|mapfile|readarray|\$\{\w+(,,|\^\^)|&>>|\|&|coproc", c)),
          ("'tail -n 12' 1, 'tail -n 8' 0", c.count("tail -n 12") == 1 and "tail -n 8" not in c),
          ("Marken ANFANG und ENDE je 1", t.count("\n# >>> TB-155 FENSTERINHALT ANFANG") == 1 and t.count("\n# <<< TB-155 FENSTERINHALT ENDE\n") == 1),
          ("jedes neue Stueck genau einmal", all(t.count(n) == 1 for _, _, n in S)),
          ("neue Log-Zeilen in Skript und LIESMICH", all(x in c and x in lm for x in LOGTEILE)),
          ("jede Einfuegung genau einmal", all(lies(p).count(n) == 1 for p, st in D.items() for _, _, n in st)),
          ("Test gleich dem Anhang", lies(TEST) == TESTTEXT),
          ("Kontoregel: Skript, Test und Werkzeug nennen dieselben %d Merkmale" % len(KONTO), sorted(re.findall(r'\*"([^"$]+)"\*', zw(t, "\nkonto_ersetzen() {", "esac"))) == sorted(KONTO) == sorted(zw(TESTTEXT, "<<'MERKMALE'\n", "\nMERKMALE\n").split("\n")[1:]))]
    for n, ok in pr: print("%s: %s" % (n, "ja" if ok else "NEIN"))
    return 0 if all(ok for _, ok in pr) else 1

def main(a):
    probe = "--probe" in a
    a = [x for x in a if x != "--probe"]
    f = {"waechter": (waechter, 0, probe), "doku": (doku, 0, probe), "journal": (journal, 1, probe), "warte": (warte, 2), "beleg": (beleg, 2), "zurueck": (zurueck, 1), "nachweis": (nachweis, 0)}.get(a[0] if a else "")
    if not f or len(a) != f[1] + 1 or not os.path.exists(SH): print(__doc__); return 1
    return f[0](*(a[1:] + list(f[2:])))

if __name__ == "__main__":
    rc = main(sys.argv[1:])
    print("rc %d" % rc)
    sys.exit(rc)
```

## Anhang B — Journalblock (Wortlaut; die Sitzung ersetzt nur die Stellen `<…>`)

```markdown
## ES — TB-155: Sitzungswächter schreibt den Fensterinhalt ins Log; „nicht angemeldet“ und „API-Abrechnung“ heissen nicht mehr „eingabebereit“

*Quelle: `docs/ERGEBNIS_TB-155_waechter_fensterinhalt.md`*

**Quelle:** Mac-Sitzung **TB-155**, <Datum>; Belege `docs/belege/TB-155/`; Freigabe und Vorgaben im Auftrag `docs/auftraege/MAC_TB-155_waechter_fensterinhalt.md`. <Abbruch oder nicht; abgelehnte Aufrufe>

### Was gemessen ist

- **Bau:** `starte_sitzung.sh` 622 → 723 Zeilen, neu `test_fensterinhalt.sh` (113 Fälle); unter `/bin/bash` <Version>: <n> ok, <n> FEHL (zählt `cut` Zeichen: <ja oder nein>).
- **Probe über launchd:** <n> Läufe; je Lauf <Anmeldung, Ablaufwarnung ja oder nein, Fensterzeilen, davon ersetzt, rc>; zerschnittene Zeichen <Zahl>; vor den Belegen nachgesehen: kein Fund.
- **Unterlagen:** `LIESMICH.md` + 31, `BACKLOG.md` + 8 Zeilen; `nachweis` <n> von 14 `ja`.

### Was offen bleibt

- `Not logged in` und die Zeile bei `API Usage Billing`: <erschlossen, nicht gemessen; rc 6 und 7 nur im Test> oder <in der Probe gesehen: rc …>. Der echte Start lief nicht.
- Die Kontoregel ist eine Merkmalliste, kein Beweis.
- <Abweichungen und Aufgaben für den Betreiber, oder „keine“>

*Geschrieben <Datum> von der Mac-Sitzung TB-155. Quellenvermerk: siehe Kopf.*
```
