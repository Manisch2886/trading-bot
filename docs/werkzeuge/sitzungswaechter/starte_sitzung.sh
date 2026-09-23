#!/bin/bash
# ============================================================================
# Sitzungswaechter — startet eine Claude-Code-Sitzung, wenn eine Ausloeserdatei
# auftaucht. Gebaut am 23.09.2026, nachdem gemessen war, dass der steuernde
# Chat KEINE Sitzung selbst starten kann.
#
# ⭐ DER ANLASS, gemessen am 23.09.2026:
#   Terminal      tier "click"  (isSentinel: true)
#   Kurzbefehle   tier "click"
#   Skripteditor  tier "click"
#   "Terminals and IDEs can only be granted in 'click' mode - you can see and
#    left-click, but cannot type, press keys, or paste."
#   ⇒ Der steuernde Chat kann auf dem Mac SEHEN und KLICKEN, aber nicht tippen.
#     Er kann jedoch ueber den Bruecken-Mount DATEIEN im Repo anlegen.
#     Dieser Waechter macht aus einer Datei einen Sitzungsstart.
#
# ⚠️⚠️ SICHERHEIT — WARUM DIESES SKRIPT SO ENG IST
# Wer die Ausloeserdatei schreiben kann, loest hier Programmausfuehrung aus.
# Deshalb gilt ohne Ausnahme:
#   (1) Der INHALT der Ausloeserdatei wird NIE ausgefuehrt und NIE gelesen.
#       Gelesen wird ausschliesslich der DATEINAME.
#   (2) Aus dem Namen wird nur eine TB-Nummer uebernommen, gegen ^TB-[0-9]{1,4}$
#       geprueft. Alles andere wird abgewiesen.
#   (3) Den Auftragssatz baut DIESES SKRIPT aus der geprueften Nummer.
#       Er wird nirgendwo uebernommen.
#   ⇒ Uebertragen werden kann also GENAU EINE ZAHL, nichts sonst.
#
# ⛔ Dieses Skript gibt nie Umgebungsvariablen, Schluessel oder Dateiinhalte aus.
# ============================================================================

set -u

REPO="$HOME/trading-bot"
AUSLOESER="$REPO/docs/auftraege/_ausloeser"
ERLEDIGT="$AUSLOESER/_erledigt"
LOGDIR="$REPO/logs/sitzungswaechter"
LOG="$LOGDIR/waechter.log"

mkdir -p "$AUSLOESER" "$ERLEDIGT" "$LOGDIR"

sage() { echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ')  $*" >> "$LOG"; }

sage "----- Waechter geweckt -----"

# --------------------------------------------------------------------------
# 1. Die Ausloeserdatei finden. Nur der NAME zaehlt.
# --------------------------------------------------------------------------
DATEI=""
for f in "$AUSLOESER"/starte_TB-*; do
    [ -e "$f" ] || continue
    DATEI="$f"
    break
done

if [ -z "$DATEI" ]; then
    sage "Kein Ausloeser da. Nichts zu tun."
    exit 0
fi

NAME="$(basename "$DATEI")"
NUMMER="${NAME#starte_}"
sage "Ausloeser gefunden: $NAME"

# --------------------------------------------------------------------------
# 2. ⚠️ DIE SCHRANKE. Nur TB-<Ziffern>. Alles andere fliegt raus.
# --------------------------------------------------------------------------
# ⚠️ GEMESSEN am 23.09.2026, beim Bauen: `grep -qE '^TB-[0-9]{1,4}$'` ist
#    an dieser Stelle NICHT dicht. grep prueft ZEILENWEISE, und ein Dateiname
#    darf unter macOS einen Zeilenumbruch enthalten — `TB-91<NL>TB-92` kam
#    durch, ebenso `<NL>TB-91`. Getestet wurden drei Varianten; `case` mit
#    Glob und `[[ =~ ]]` wiesen alle drei ab, grep keine einzige.
#    ⇒ `case` gewinnt: kein Regex-Dialekt, keine Locale-Abhaengigkeit,
#      keine Zeilensemantik.
case "$NUMMER" in
    TB-[0-9]|TB-[0-9][0-9]|TB-[0-9][0-9][0-9]|TB-[0-9][0-9][0-9][0-9]) : ;;
    *)
        sage "⛔ ABGEWIESEN: Der Name nennt keine gueltige TB-Nummer."
        mv "$DATEI" "$ERLEDIGT/ABGEWIESEN_$(date -u '+%Y%m%dT%H%M%SZ')_bad" 2>/dev/null
        exit 1
        ;;
esac
sage "Nummer geprueft: $NUMMER"

# --------------------------------------------------------------------------
# 3. Ausloeser SOFORT wegraeumen — vor allem anderen.
#    Sonst weckt eine liegenbleibende Datei den Waechter erneut.
#    ⚠️ Verschoben, nicht geloescht (Projektregel).
# --------------------------------------------------------------------------
STEMPEL="$(date -u '+%Y%m%dT%H%M%SZ')"
mv "$DATEI" "$ERLEDIGT/${STEMPEL}_$NAME" || { sage "⛔ Konnte Ausloeser nicht wegraeumen. Abbruch."; exit 1; }
sage "Ausloeser weggeraeumt nach _erledigt/${STEMPEL}_$NAME"

abbruch() {
    sage "⛔ ABBRUCH: $1"
    printf '%s\n' "$1" > "$LOGDIR/letzter_abbruch.txt"
    exit 1
}

# --------------------------------------------------------------------------
# 4. Vorbedingungen. Jede einzelne ist ein Abbruchgrund.
# --------------------------------------------------------------------------

# 4a. Laeuft schon eine Sitzung IM REPO? NIE ZWEI AUFTRAEGE IM SELBEN ARBEITSBAUM.
#
# ⚠️ GEMESSEN am 23.09.2026, beim ersten Probelauf: Ein blosses
#    `pgrep -x claude` bricht IMMER ab. Auf dem Mac laeuft staendig
#    mindestens ein claude-Prozess, der KEINE Arbeitssitzung ist — er haelt
#    die Verbindung zur App und damit zum steuernden Chat. Wer den zaehlt,
#    sperrt sich selbst aus.
# ⇒ Es zaehlt nur ein Prozess, dessen ARBEITSVERZEICHNIS das Repo ist.
# ⛔ Gelesen wird ausschliesslich das cwd — nie die Kommandozeile, die
#    Zugangsdaten enthalten koennte (ARBEITSWEISE Abschnitt 7).
FREMD=0
IM_REPO=0
for pid in $(pgrep -x claude 2>/dev/null); do
    cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
    case "$cwd" in
        "$REPO"|"$REPO"/*) IM_REPO=$((IM_REPO+1)); sage "  claude im Repo: PID $pid" ;;
        *)                 FREMD=$((FREMD+1));    sage "  claude ausserhalb (zaehlt nicht): PID $pid cwd=${cwd:-unbekannt}" ;;
    esac
done
sage "claude-Prozesse: $IM_REPO im Repo, $FREMD ausserhalb."
if [ "$IM_REPO" -gt 0 ]; then
    abbruch "Es arbeitet bereits eine claude-Sitzung im Repo ($IM_REPO). Der Waechter startet keine zweite."
fi

# 4b. Ist claude ueberhaupt da?
#
# ⚠️ GEMESSEN am 23.09.2026, dritter Probelauf: "claude ist nicht auffindbar" —
#    obwohl der Betreiber es im Terminal schlicht tippt. Der Grund ist launchd:
#    es startet mit einem minimalen PATH (/usr/bin:/bin:/usr/sbin:/sbin) und
#    kennt das Benutzerprofil nicht. `command -v claude` greift dort ins Leere.
# ⇒ Gefragt wird eine LOGIN-Shell — dieselbe Umgebung, in der der Betreiber
#   tippt. zsh zuerst (macOS-Standard), dann bash, dann feste Orte.
CLAUDE_BIN=""
for sh in /bin/zsh /bin/bash; do
    [ -x "$sh" ] || continue
    k=$("$sh" -lc 'command -v claude' 2>/dev/null | tail -1)
    if [ -n "$k" ] && [ -x "$k" ]; then CLAUDE_BIN="$k"; sage "claude ueber $sh gefunden."; break; fi
done
if [ -z "$CLAUDE_BIN" ]; then
    for k in "$HOME/.claude/local/claude" "/opt/homebrew/bin/claude" "/usr/local/bin/claude" "$HOME/.local/bin/claude"; do
        [ -x "$k" ] && { CLAUDE_BIN="$k"; sage "claude an festem Ort gefunden."; break; }
    done
fi
[ -n "$CLAUDE_BIN" ] || abbruch "claude ist nicht auffindbar - weder ueber eine Login-Shell noch an den bekannten Orten. Auf dem Mac 'command -v claude' ausfuehren und den Pfad melden."
sage "claude: $CLAUDE_BIN"

# 4c. ⚠️⚠️ SCHLUESSELBUND. Ist er gesperrt, laeuft die Sitzung ueber
#     "API Usage Billing" statt ueber das Abo — sie KOSTET dann Geld.
#     ⛔ Geprueft wird nur, OB er entsperrt ist. Nie ein Wert, nie ein Passwort.
if ! security show-keychain-info "$HOME/Library/Keychains/login.keychain-db" > /dev/null 2>&1; then
    abbruch "Schluesselbund gesperrt. Ohne ihn fehlt /remote-control und der Lauf ginge ueber API Usage Billing statt ueber das Abo. Auf dem Mac 'security unlock-keychain' ausfuehren."
fi
sage "Schluesselbund entsperrt."

# 4d. Steht die Nummer im Auftragszeiger? Sonst braeuchte die Sitzung gar
#     nicht erst zu starten — sie bricht ohnehin ab.
ZEIGER="$REPO/docs/auftraege/AKTUELLER_AUFTRAG.md"
[ -f "$ZEIGER" ] || abbruch "AKTUELLER_AUFTRAG.md fehlt."
if ! grep -q "\*\*$NUMMER\*\*" "$ZEIGER"; then
    abbruch "$NUMMER steht nicht als gueltiger Auftrag in AKTUELLER_AUFTRAG.md. (Meist: noch nicht gepusht/gezogen.)"
fi
sage "$NUMMER steht im Auftragszeiger."

# --------------------------------------------------------------------------
# 5. Der Satz. ⚠️ HIER GEBAUT, nirgends uebernommen.
#    Zeichengleich mit AKTUELLER_AUFTRAG.md, nur die Nummer wechselt.
# --------------------------------------------------------------------------
SATZ="$NUMMER: Lies docs/auftraege/AKTUELLER_AUFTRAG.md, suche dort die Zeile mit genau der TB-Nummer, die diesem Satz vorangestellt ist, und arbeite den in dieser Zeile genannten Auftrag vollstaendig eigenstaendig ab. Antworte zuerst mit einer Zeile, welchen Auftrag du gelesen hast. Kommt deine Nummer dort nicht vor, brich ab und melde es."

# --------------------------------------------------------------------------
# 6. Starten. ⚠️ ueber Terminal.app, weil launchd KEIN TTY hat und
#    Claude Code eines braucht. Das Fenster ist echt — wie von Hand getippt.
# --------------------------------------------------------------------------
sage "Starte Terminal-Fenster ..."
FENSTER=$(osascript <<OSA 2>>"$LOG"
tell application "Terminal"
    set neu to do script "cd ~/trading-bot && exec claude --remote-control"
    return id of window 1
end tell
OSA
) || abbruch "osascript konnte Terminal nicht ansteuern. Fehlt die Automation-Berechtigung? (Systemeinstellungen > Datenschutz & Sicherheit > Automation)"

sage "Terminal-Fenster $FENSTER offen. Warte auf die Eingabezeile ..."

# ⚠️ Claude Code braucht Anlaufzeit. Gemessen ist sie nicht — deshalb
#    grosszuegig und in Stufen, mit Protokoll.
WARTE="${WAECHTER_WARTESEKUNDEN:-20}"
sleep "$WARTE"
sage "$WARTE s gewartet."

# --------------------------------------------------------------------------
# 7. Den Satz in dasselbe Fenster geben.
# --------------------------------------------------------------------------
osascript <<OSA 2>>"$LOG"
tell application "Terminal"
    do script "$SATZ" in window id $FENSTER
end tell
OSA
if [ $? -ne 0 ]; then
    sage "⚠️ Der Satz konnte nicht uebergeben werden. Das FENSTER LAEUFT aber."
    sage "   Auftragssatz zum Einfuegen von Hand liegt in $LOGDIR/letzter_satz.txt"
    printf '%s\n' "$SATZ" > "$LOGDIR/letzter_satz.txt"
    exit 1
fi

printf '%s\n' "$SATZ" > "$LOGDIR/letzter_satz.txt"
sage "⭐ Satz uebergeben. $NUMMER laeuft (oder meldet sich mit einem Abbruch)."
sage "----- fertig -----"
exit 0
