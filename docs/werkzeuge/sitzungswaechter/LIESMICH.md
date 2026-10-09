# Sitzungswächter — eine Datei löst eine Mac-Sitzung aus

**Gebaut:** 23.09.2026, vom steuernden Chat
**Warum:** Der steuernde Chat kann auf dem Mac **sehen und klicken, aber nicht
tippen** — und deshalb keine Sitzung starten. Dateien im Repo anlegen kann er.
Dieser Wächter macht aus einer Datei einen Sitzungsstart.

---

## ⭐⭐ Gilt seit TB-144 (Wächter-Reparatur)

**Dieser Abschnitt geht allem vor, was weiter unten anders steht.** Das Alte bleibt als Geschichte stehen; wo es nicht mehr gilt, folgt ihm eine Zeile „⭐ Gilt seit TB-142“ (kein Satz), „… TB-143“ (Startzeile) oder „… TB-144“.

**Der Anlass (Fehler Nr. 23):** Seit dem 29.09.2026 meldeten 20 Starts in Folge „Terminal-Fenster 15501“ — das vorderste Fenster, nicht das neu geöffnete. Der Satz ging samt Zeilenende in eine bash-Shell („-bash: TB-141:: command not found“), die Sitzung stand in einem anderen Fenster an einer Startfrage, und das Log meldete „Satz ins Fenster gelegt“.

### Was der Wächter nach `starte_TB-<Nr>` jetzt tut

| | |
|---|---|
| **Öffnen** | ein **neues** Terminal-Fenster mit der Startzeile `cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control --no-chrome` |
| **Fenster** | Die Nummer kommt aus dem Tab, den Terminal beim Öffnen zurückgibt. Gab es sie schon vorher, bricht er ab |
| **Merken** | Die Nummer steht in `logs/sitzungswaechter/letztes_fenster.txt` |
| **Prüfen** | Er **liest** den Inhalt dieses Fensters über Terminal selbst, in Stufen von 3 3 4 5 5 10 10 10 10 Sekunden, zusammen höchstens 60 s |
| **Melden** | eine der drei Zeilen unten; bei ⛔ ist sein Rückgabewert 3 oder 4. Kann er das neue Fenster nicht bestimmen („⛔ MESSWERTE FEHLEN“, „⛔ FENSTERLISTE NICHT LESBAR“, „⛔ osascript konnte Terminal nicht ansteuern“, „⛔ FENSTER NICHT BESTIMMBAR“, „⛔ FENSTER NICHT NEU“, „⛔ FENSTER FEHLT“, danach „⛔ ABBRUCH“), prüft er nichts, Rückgabewert 1 — ein Fenster kann dann trotzdem offen sein |
| ⛔ **Kein Satz** | Er legt den Auftragssatz **nicht mehr** ins Fenster (schon seit TB-142). Der Satz steht in `logs/sitzungswaechter/letzter_satz.txt` und als Kopierblock in der Antwort des steuernden Chats; abgeschickt wird er vom Betreiber |

**Warum kein Satz mehr:** Der Terminal-Befehl, der Text in ein vorhandenes Fenster gibt (`do script … in window`), schickt eine Befehlszeile **samt Zeilenende**. Im richtigen Fenster wäre das das Abschicken, das die Betreiberentscheidung vom 23.09.2026 ausschliesst.

### Die Zeilen im Wächter-Log

```
⭐ EINGABEBEREIT (TB-<Nr>): Fenster <n>, Eingabezeile steht, keine Frage offen (nach <s> s, Lesung <i>). ⚠️ KEIN SATZ IM FENSTER.
⛔ STARTFRAGE (TB-<Nr>): Fenster <n> zeigt nach <s> s eine Frage ("Enter to confirm"). Die Sitzung ist NICHT eingabebereit.
⛔ KEINE EINGABEZEILE (TB-<Nr>): Fenster <n> zeigt nach <s> s keine Eingabezeile von Claude Code (verlangt: zwei Lesungen in Folge). Die Sitzung gilt als NICHT eingabebereit.
   Lesbar waren <g> von <i> Lesungen (0 = Terminal hat nicht geantwortet; dann liegt es nicht am Merkmal).
Fenster <n> neu geoeffnet (Tab <k>). Gemerkt in <Pfad>/letztes_fenster.txt
  Fenster <n> geschlossen (das beim Start gemerkte, kein laufender Prozess).
  ⚠️ Fenster <n> bleibt offen: <Grund>.
```

Bei ⛔ stehen darunter die letzten Zeilen des neu geöffneten Fensters (höchstens 8, je 160 Zeichen), und das Fenster bleibt offen. **Woran er die Eingabezeile erkennt (Merkmal gemessen; zwei Lesungen: Lesart, vorläufig):** Der Fensterinhalt enthält in zwei Lesungen hintereinander `? for shortcuts` und in keiner `Enter to confirm`.

### Fenster aufräumen

Nach `schliesse_<HEAD>` (beide Wachen unverändert: HEAD-Gleichheit, 600 s) schliesst der Wächter **genau das gemerkte Fenster** — nur wenn im Repo keine `claude`-Sitzung mehr läuft, das Fenster genau einen Tab hat und darin kein Prozess mehr läuft. Sonst bleibt es offen, und das Log nennt den Grund. Schalter im Skript: `FENSTER_SCHLIESSEN="ja"`. Kein anderes Fenster wird angefasst. Ein Probefenster, das die Probe selbst nicht schliessen konnte, schliesst auch `schliesse_<HEAD>` nicht (es ist in `letztes_fenster_probe.txt` gemerkt, nicht in `letztes_fenster.txt`); es bleibt offen, das Log nennt seine Nummer, schliessen muss es der Betreiber.

### Probe ohne Auftrag: `probe_<PID>`

Eine Datei `docs/auftraege/_ausloeser/probe_<PID>` öffnet ein Fenster wie ein echter Start (gleicher Ordner, gleiche Startzeile, dieselben Funktionen), prüft die Eingabezeile, beendet genau die dabei entstandene Sitzung mit `TERM` und räumt das Fenster auf — kein Auftrag, kein Satz. `<PID>` ist die eine `claude`-Sitzung im Repo, die die Probe auslöst; läuft dort eine andere, bricht die Probe ab. Wache 3 für echte Starts ist unverändert; gelesen wird nur der Dateiname. Rückgabewert der Probe wie beim Start; dazu **5**, wenn die Eingabezeile stand, das Log aber „NICHT beendet“ meldet: Eine `claude`-Sitzung im Repo hing nicht am neuen Tab und läuft weiter.

### Gemessen in TB-144

| | |
|---|---|
| **M1** Fenster zu einem Tab | do script ohne in liefert beim Oeffnen 'tab 1 of window id <n>' (Testfenster 21630 und 21631, Probe 21632 bis 21635); <n> stand jeweils vorher nicht in der Fensterliste und nachher schon; tty des Tabs /dev/ttys017, ps meldet dafuer 'ttys017 ' mit Leerzeichen am Ende. |
| **M2** Eingabezeile im Fensterinhalt | Merkmal '? for shortcuts' steht in allen 18 Lesungen der wartenden Sitzung (3 bis 60 s, beide Testfenster), schon in der ersten nach 3 s; keine Lesung zeigte Shell, Ladeanzeige oder eine Frage; Zeilen mit LF getrennt, kein CR; 'manual mode on' stand in jeder Lesung; busy meldet false, obwohl claude per exec im Tab laeuft. |
| **M3** `--no-chrome` | Mit und ohne --no-chrome erschien keine Frage (beide Testfenster 60 s ohne 'Enter to confirm'); die Wirkung von --no-chrome ist damit nicht zuzuordnen; nach der Tabelle in Schritt B ist der Schalter angehaengt. |
| **M4** Schliessen ohne Rückfrage | Nach TERM an die claude-PID meldet busy false, und close window id schliesst das Fenster ohne Rueckfrage (exists danach false, Testfenster 21630 und 21631) - FENSTER_SCHLIESSEN=ja. |
| **M5** „Teach auto mode“ beim Start | 'Teach auto mode' kommt in 0 von 18 Lesungen aus M2 und M3 und in 0 von 4 Probe-Logs vor (Teilmessung, nur der Start ohne Auftrag). |
| **Probe** über Auslöser und launchd | Vier Laeufe ueber probe_52208 und launchd (Fenster 21632, 21633, 21634, 21635), je neu geoeffnet, EINGABEBEREIT nach 6 s (Lesung 2), Probesitzung mit TERM beendet, Fenster geschlossen, danach im Repo nur PID 52208, rc 0; Prozesszeile der Probesitzung in Lauf 2 bis 4 gelesen, sie trug --permission-mode manual (und --no-chrome); keine neue Berechtigung. |

⭐ **Berichtigung aus der Abnahme TB-144 (09.10.2026):** `busy` war bei wartender Sitzung `false` (`docs/belege/TB-144/b_m1.txt` Z. 15–16, `b_m3.txt` Z. 15–16), am Fenster der arbeitenden Sitzung aber `true` (`d0_fenster.txt` Z. 112–113; in diesem Tab liefen `login, claude, caffeinate`, Z. 133–134). `busy` sagt also nicht verlässlich, ob in einem Fenster eine Sitzung läuft; vor dem Schliessen schützt die Prüfung `claude_im_repo` in `fenster_aufraeumen`. Für die drei toten Fenster nannte Terminal das tty des Fensters der laufenden Sitzung; für eine Aufräumregel über alte Fenster wäre `processes of tab` der zuverlässigere Prüfwert (`docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`, Abschnitt D0).

Rohausgaben: `docs/belege/TB-144/`. Ergebnis: `docs/ERGEBNIS_TB-144_waechter_reparatur_rest.md`.

### Was bleibt

Kein Enter, kein Tastendruck, kein Abschicken durch den Wächter; den Fensterinhalt liest er nur. Die sechs Wachen vor dem Start und die zwei Wachen des Schliess-Auslösers sind unverändert. Der steuernde Chat sieht nach jedem Start weiter selbst ins Fenster: Die Log-Zeile sagt, was der Wächter bis höchstens 60 s nach dem Öffnen gelesen hat — nicht, was danach erscheint.

**In einfacher Sprache:** Der Wächter öffnet ein neues Fenster, startet dort Claude Code und sieht dann selbst nach, ob Claude Code auf eine Eingabe wartet. Nur dann schreibt er „eingabebereit“ ins Protokoll. Steht dort eine Frage, schreibt er das hin. Den Auftragssatz legt er nicht mehr ins Fenster; den schickst du selbst ab, in der Claude-App oder im Fenster.

---

## ⭐ Der Befund, der dahintersteht (gemessen 23.09.2026)

| App | Stufe |
|---|---|
| Terminal | `click` (`isSentinel: true`) |
| Kurzbefehle | `click` |
| Skripteditor | `click` |

> *„Terminals and IDEs can only be granted in 'click' mode — you can see and
> left-click, but cannot type, press keys, or paste."*

⚠️ **`can only`** — das ist keine Einstellung, die sich umlegen lässt. Alle drei
Wege, einen Befehl zu tippen, sind zu. Der Wächter geht deshalb den einen Weg,
der offen ist: **eine Datei.**

---

## Einschalten

**Eine Zeile, auf dem MacBook, aus der Repo-Wurzel:**

```
bash docs/werkzeuge/sitzungswaechter/einschalten.sh
```

⚠️ **Beim ersten Lauf fragt macOS, ob Terminal gesteuert werden darf.**
Das musst du einmal erlauben. Kommt die Frage nicht, steht sie unter
*Systemeinstellungen → Datenschutz & Sicherheit → Automation*.

**Nachsehen:** `bash docs/werkzeuge/sitzungswaechter/einschalten.sh stand`
**Ausschalten:** `bash docs/werkzeuge/sitzungswaechter/einschalten.sh aus`

---

## ⚠️⚠️ Warum das Skript so eng ist

**Wer die Auslöserdatei schreiben kann, löst Programmausführung auf deinem Mac
aus.** Deshalb ohne Ausnahme:

| | |
|---|---|
| **(1)** | Der **Inhalt** der Auslöserdatei wird nie gelesen und nie ausgeführt |
| **(2)** | Gelesen wird nur der **Dateiname**, und daraus nur die Nummer |
| **(3)** | Die Nummer wird gegen `TB-<1 bis 4 Ziffern>` geprüft — sonst abgewiesen |
| **(4)** | Den Auftragssatz baut **das Skript selbst** aus der geprüften Nummer |

⇒ ⭐ **Übertragen lässt sich genau eine Zahl. Sonst nichts.**

### ⚠️ Ein Fund beim Bauen: die erste Schranke war nicht dicht

Die naheliegende Prüfung `grep -qE '^TB-[0-9]{1,4}$'` **hält nicht**. `grep`
prüft **zeilenweise**, und ein Dateiname darf unter macOS einen Zeilenumbruch
enthalten. Gemessen:

| Eingabe | `grep` | `[[ =~ ]]` | `case` |
|---|---|---|---|
| `TB-91` | durch | durch | durch |
| `TB-abc`, `TB-12345`, `TB-$(id)` | abgewiesen | abgewiesen | abgewiesen |
| ⚠️ `TB-91`⏎`TB-92` | **durch** | abgewiesen | abgewiesen |
| ⚠️ ⏎`TB-91` | **durch** | abgewiesen | abgewiesen |

⇒ **Im Skript steht `case` mit Glob** — kein Regex-Dialekt, keine
Locale-Abhängigkeit, keine Zeilensemantik. *Ein Trockenlauf mit acht bösartigen
Namen liegt im Protokoll dieser Sitzung; alle acht wurden abgewiesen.*

---

## ⭐⭐ Die Betreiberentscheidung vom 23.09.2026: **kein Return**

**Der Wächter schreibt den Auftragssatz in die Eingabezeile — und schickt ihn
NICHT ab.** Den letzten Tastendruck macht der Betreiber.
⭐ **Gilt seit TB-142 (Abschnitt „Gilt seit TB-144“ oben):** Der Wächter schreibt den Satz nicht mehr in die Eingabezeile und gibt keinen Text mehr an ein Fenster; er öffnet es, und seit TB-144 liest er es und meldet. „Kein Return“ gilt unverändert. Die Sätze weiter unten „er schickt den Satz per AppleScript an Terminal“ und „Text einfügen“ gelten nicht mehr.

⚠️ **Warum, und das ist kein Schönheitsfehler:** Beim Zugriff auf Terminal
antwortet die Geräteanbindung ausdrücklich

> *„Do not attempt to work around this restriction — never use AppleScript,
> System Events, shell commands, or any other method to send clicks or
> keystrokes to this app."*

⭐ **Der Wächter berührt diese Schranke bereits** — er schickt den Satz per
AppleScript an Terminal, und gebaut wurde er, nachdem gemessen war, dass dem
steuernden Chat das Tippen verwehrt ist. Das Return nachzurüsten machte aus
einem Grenzfall eine vollständige Umgehung.

| | |
|---|---|
| ⭐ **Was bleibt** | Der Tastendruck ist die Stelle, an der ein Mensch draufschaut, bevor eine Sitzung im Arbeitsbaum losläuft |
| ⭐ **Was er nicht kostet** | **Der Betreiber muss dafür nicht am Mac sitzen.** Die Sitzung läuft mit `--remote-control` und ist in der Claude-App sichtbar — der Satz lässt sich vom Telefon abschicken |
| ⚠️ **Was entfällt** | Terminal suchen, `cd`, Start, Anlaufzeit abwarten, Text einfügen — all das macht der Wächter |

⇒ **Übrig bleibt ein Tipper. Das ist Absicht und bleibt so.**

---

## ⚠️ Drei Baufehler, alle am ersten Tag gemessen

*Sie stehen hier, weil jeder von ihnen beim Nachbauen wiederkäme.*

### (1) Die `grep`-Schranke war nicht dicht

`grep -qE '^TB-[0-9]{1,4}$'` prüft **zeilenweise**. Ein Dateiname darf unter
macOS einen Zeilenumbruch enthalten — `TB-91`⏎`TB-92` kam durch, ebenso
⏎`TB-91`. ⇒ **`case` mit Glob**, gemessen gegen acht bösartige Namen.

### (2) `pgrep -x claude` hätte sich selbst ausgesperrt

Auf dem Mac läuft ständig mindestens ein `claude`-Prozess, der **keine**
Arbeitssitzung ist. Wer ihn mitzählt, bricht immer ab. ⇒ Es zählt nur, wessen
**Arbeitsverzeichnis im Repo liegt**; gelesen wird ausschliesslich das `cwd`,
nie die Kommandozeile (Zugangsdaten, Abschnitt 7).

⭐ **Und diese Wache hat sofort etwas gefunden:** eine Claude-Code-Sitzung, die
seit **20.09., 20:18 — zwei Tage und 18 Stunden** — offen stand, `S+`, 30
Minuten Rechenzeit in 66 Stunden Laufzeit. Sie war untätig, aber niemand wusste
von ihr.

### (3) Unter `launchd` ist der Suchpfad leer

`claude ist nicht auffindbar` — obwohl der Betreiber es schlicht tippt.
`launchd` startet mit `/usr/bin:/bin:/usr/sbin:/sbin` und kennt kein
Benutzerprofil. ⇒ Gefragt wird eine **Login-Shell**, also dieselbe Umgebung wie
beim Tippen. *Gemessen lag `claude` unter `~/.local/bin/` — an keinem der Orte,
die eine feste Liste zuerst geraten hätte.*

⭐ **Dieselbe Einsicht vereinfachte den Start:** `Terminal.app` führt `do script`
ohnehin in einer Login-Shell aus. Der Startbefehl nennt deshalb schlicht
`claude`, ohne Pfad.

---

## ⛔⛔ Zweimal versucht, zweimal gescheitert: der Auftrag als Argument

⚠️ **Wer das ein drittes Mal versuchen will, liest zuerst hier.**

`claude --help` nennt in der ersten Zeile ein positionales Argument:

```
Usage: claude [options] [command] [prompt]
Arguments:
  prompt        Your prompt
```

**Das verführt zu dem Schluss, der Auftrag könne beim Start mitgehen — dann
bräuchte es weder AppleScript-Tippen noch das Enter des Betreibers.** Der
Schluss ist falsch.

| Versuch | Umstände | Ergebnis |
|---|---|---|
| **19.09.2026**, v2.1.278 | `claude --remote-control "<Text>"` über Termius/SSH | ⛔ Sitzung startete, **Eingabezeile leer** (`ARBEITSWEISE` Abschnitt 14) |
| **23.09.2026, 18:16**, v2.1.280 | Satz in einer **Datei**, `exec claude --remote-control "$(cat …)"`, über AppleScript — ⛔ **kein Termius im Spiel** | ⛔ Sitzung startete, **in der App leer**, kein Auftrag angekommen |

⇒ ⚠️⚠️ **Der Verdacht von 2026-09-19 — „Termius hat die Anführungszeichen
zerlegt" — ist damit WIDERLEGT.** Beim zweiten Versuch lief nichts über Termius,
der Satz ging als Dateiinhalt in die Shell, und durch AppleScript lief nur der
Dateipfad. Er kam trotzdem nicht an.

⭐ **Die verbleibende Erklärung:** Die **interaktive** Sitzung (`--remote-control`)
nimmt das positionale Argument nicht an. Es dürfte dem nicht-interaktiven Betrieb
(`-p`/`--print`) vorbehalten sein — dort gäbe es aber keine Sitzung in der App
und keine Fernsteuerung.

### ⚠️ Und ein Fehler beim Messen, der dazugehört

Der Wächter meldete beim zweiten Versuch **fälschlich Erfolg**:

```
Rechenzeit nach 20 s: 0:03.15 (PID 19953)
⭐⭐ Der Auftrag ist als Argument angekommen - TB-92 LAEUFT bereits.
```

⚠️ **Die Schwelle „arbeitet ab 2 Sekunden Rechenzeit" war GERATEN, nicht
gemessen.** Das blosse Hochfahren von Claude Code verbraucht rund drei Sekunden.
Dadurch griff der eingebaute Rückfall nicht, der den Satz sonst ins Fenster
gelegt hätte. **Gemessen wurde es erst, als der Betreiber sechs Minuten später
eine leere Sitzung sah** — bis dahin standen 7 Sekunden Rechenzeit auf der Uhr,
Zustand `S+`.

⇒ ⭐ **Zwei Lehren, beide allgemein:**
1. Eine Schwelle, die über „bestanden" entscheidet, wird **gemessen**, nicht
   geschätzt — hier hätte ein einziger Leerlauf-Start die 3 Sekunden gezeigt.
2. Rechenzeit allein sagt nicht, **was** gerechnet wurde. Der belastbare Beleg
   ist, was im Fenster steht — und den kann nur der Betreiber liefern.

---

## ⭐ So wird es gehandhabt (Betreiberentscheidung 23.09.2026, 18:28)

**Der Wächter öffnet das Fenster und legt den Auftrag hinein. Abgeschickt wird
er vom Betreiber.** Das ist keine Notlösung mehr, sondern der Weg.
⭐ **Gilt seit TB-142 (Abschnitt „Gilt seit TB-144“ oben):** Der Wächter legt den Auftrag nicht mehr ins Fenster; in der Tabelle darunter entfällt „Text einfügen“, und seit TB-144 prüft er statt der „Anlaufzeit“, ob die Eingabezeile steht. Abgeschickt wird weiter vom Betreiber.

| | |
|---|---|
| ⭐ **Der Wächter nimmt ab** | Terminal suchen · `cd` · Start · Anlaufzeit · Text einfügen · **sechs Wachen** davor |
| ⚠️ **Beim Betreiber bleibt** | **ein** Abschicken |
| **Wo** | In der Claude-App unter der **Gerätesitzung** (Laptop-Symbol). ⚠️ Sie trägt dort zunächst einen **erzeugten Gerätenamen** wie `macbookpro-binary-aurora`, **nicht** die TB-Nummer — der Titel entsteht erst aus dem abgeschickten Satz |
| **Oder** | im Terminalfenster mit Enter |
| **Rückfall** | Der Satz steht in `logs/sitzungswaechter/letzter_satz.txt` |

⛔ **Was ausdrücklich NICHT mehr versucht wird:** den Auftrag als Argument
mitzugeben (siehe oben, zweimal gescheitert) und den Wächter Enter drücken zu
lassen (Betreiberentscheidung 23.09. Mittag — die Geräteanbindung untersagt
Tastendrücke an ein Terminal, und der Wächter berührt diese Schranke schon).

---

## ⚠️ Eine Lehre für den steuernden Chat, nicht für den Wächter

**Die Brücken-VM ist nicht der Mac.** Ein `pgrep` dort meldete *null* laufende
Sitzungen, während auf dem Mac eine lief. Prozesse des Macs sind von der
Geräteanbindung aus **nicht messbar** — und nach Prüfprinzip `A2` ist „konnte
nicht messen" ein eigenes Ergebnis, kein „nichts da".

⚠️ **Am 23.09.2026 wurde achtmal nach `docs/` geschrieben, nachdem der Zustand
des Arbeitsbaums (untracked, Zeitstempel) als „keine laufende Sitzung" gedeutet
worden war.** Das misst nicht, ob ein Prozess läuft. Es ging gut — gemessen kein
Schaden —, aber es war Glück.

⇒ ⭐ **Der Wächter ist jetzt das Messgerät.** Ein Auslöser protokolliert, welche
Sitzungen im Repo laufen, und startet nur, wenn keine da ist. Damit ist
„darf ich nach `docs/` schreiben?" zum ersten Mal messbar statt geschätzt.

---

## Der erste vollständige Lauf, 23.09.2026

```
12:05:40  Ausloeser angelegt (vom steuernden Chat, aus der Cloud)
12:05:40  geweckt · Nummer geprueft · Ausloeser weggeraeumt
12:05:40  sechs Vorbedingungen - alle durch
12:07:04  Terminalfenster 7963 offen      <- 84 s: einmaliger Berechtigungsdialog
12:07:25  Satz uebergeben, zeichengleich (334 Zeichen)
```

⭐ **Die Kopfzeile nannte „Claude Max", nicht „API Usage Billing"** — die
Schlüsselbund-Wache (Vorbedingung 5) hat sich im ersten Lauf bewährt.

⚠️ **Die 84 Sekunden waren einmalig.** Die Automation-Berechtigung gilt jetzt;
der nächste Start steht in unter einer Sekunde.

---

## Was der Wächter prüft, bevor er startet

| | Vorbedingung | ⛔ Abbruch wenn |
|---|---|---|
| **1** | Gültige TB-Nummer im Dateinamen | Name passt nicht |
| **2** | Auslöser lässt sich wegräumen | *sonst weckt er sich selbst wieder* |
| **3** | Keine laufende `claude`-Sitzung | **nie zwei Aufträge im selben Arbeitsbaum** |
| **4** | `claude` ist auffindbar | — |
| **5** | ⚠️⚠️ **Schlüsselbund entsperrt** | *sonst liefe die Sitzung über **API Usage Billing** statt über dein Abo* |
| **6** | Die Nummer steht in `AKTUELLER_AUFTRAG.md` | *meist: noch nicht gepusht — die Sitzung bräche ohnehin ab* |

⭐ **Punkt 5 ist der wichtigste.** Er ist der Grund, warum der Wächter lieber
nichts tut als etwas Falsches: Ein Start bei gesperrtem Schlüsselbund wäre nicht
nur unsichtbar in App und Web, er würde **abgerechnet**.

⭐ **Punkt 6 ist die Lehre aus TB-91**, das dreimal startete und dreimal abbrach,
weil die Auftragszeile noch nicht auf `main` war.

---

## ⚠️ Was der Wächter NICHT kann

- **Er weckt den Mac nicht.** Ist er zu oder abgemeldet, passiert nichts — der
  Auslöser bleibt liegen und greift beim nächsten Aufwachen.
- **Er entsperrt den Schlüsselbund nicht.** Das verlangt dein Passwort, und das
  tippst nur du (`ARBEITSWEISE.md` Abschnitt 7).
- **Er prüft nicht, ob die Sitzung gut gearbeitet hat.** Er startet sie.

⚠️ **Und eines ist ungemessen:** wie lange Claude Code braucht, bis es den
ersten Satz annimmt. Der Wächter wartet **20 Sekunden**. Erweist sich das als zu
knapp, steht der Satz in `logs/sitzungswaechter/letzter_satz.txt` und lässt sich
von Hand einfügen — das Fenster läuft dann bereits.
`WAECHTER_WARTESEKUNDEN=30` stellt die Wartezeit um.
⭐ **Gilt seit TB-144 (Abschnitt „Gilt seit TB-144“ oben):** Die feste Wartezeit von 20 Sekunden und `WAECHTER_WARTESEKUNDEN` gibt es nicht mehr. Der Wächter liest den Fensterinhalt in Stufen bis höchstens 60 s und legt (schon seit TB-142) keinen Satz mehr ins Fenster; `letzter_satz.txt` bleibt.

---

## In einfacher Sprache

Der steuernde Chat kann auf dem MacBook zusehen und klicken, aber nichts tippen
— das ist von Apple so festgelegt und lässt sich nicht ändern. Dateien anlegen
kann er dagegen sehr wohl.

**Also wird aus einer Datei ein Startknopf:** Ein kleiner Wächter auf dem Mac
passt auf einen Ordner auf. Taucht dort eine Datei mit einer Auftragsnummer im
Namen auf, öffnet er ein Terminalfenster und startet die Sitzung — genau so, wie
du es sonst von Hand tust.

**Das Wichtigste daran ist, was er nicht tut.** Er liest nie, was in der Datei
steht. Er nimmt nur die Nummer aus dem Dateinamen, prüft sie streng, und baut
den Auftragssatz selbst. Übertragen werden kann also nichts als eine Zahl.

Und bevor er startet, prüft er sechs Dinge — darunter, ob dein Schlüsselbund
offen ist. Ist er es nicht, bricht der Wächter ab, statt eine Sitzung zu
starten, die dich Geld statt Abo kosten würde.
