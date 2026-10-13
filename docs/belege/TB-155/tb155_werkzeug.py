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
