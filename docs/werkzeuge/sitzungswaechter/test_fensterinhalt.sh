#!/bin/bash
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
[ "$FEHL" -eq 0 ]
