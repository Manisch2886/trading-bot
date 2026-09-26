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
# 0. ⭐⭐ SCHLIESS-AUSLOESER (seit 24.09.2026) — eine Sitzung beenden,
#    ohne Tastenkombination. Anlass: Betreiberanweisung 24.09., 08:41 —
#    `Strg`+`D` ist vom iPhone aus nicht tippbar.
#
#    Dateiname:  schliesse_<40 Hex-Zeichen>
#    Die vierzig Zeichen sind der Commit, den der steuernde Chat zuletzt
#    GELESEN hat. Stimmt HEAD damit nicht ueberein, wird NICHT geschlossen.
#
#    ⚠️ Auch hier wird NUR DER DATEINAME gelesen, nie der Inhalt (Zusage (1)
#       im Kopf dieser Datei). Uebertragen wird genau ein Bezeichner.
#
#    ⭐ Warum der Hash und nicht die Rechenzeit: GEMESSEN am 24.09.2026 ist
#       die Rechenzeit KEIN Unterscheidungsmerkmal. Eine untaetige Sitzung
#       verbrauchte 1,6 % (45 s in 48 min), eine ARBEITENDE 4,8 % (24 s in
#       8,5 min) — beide im Zustand S+. Wer daraus "untaetig" schliesst,
#       raet. Belastbar ist: Der Abgabe-Commit liegt vor, ist gelesen, und
#       seitdem hat sich HEAD nicht bewegt.
# --------------------------------------------------------------------------
SCHLIESSER=""
for f in "$AUSLOESER"/schliesse_*; do
    [ -e "$f" ] || continue
    SCHLIESSER="$f"
    break
done

if [ -n "$SCHLIESSER" ]; then
    SNAME="$(basename "$SCHLIESSER")"
    ERWARTET="${SNAME#schliesse_}"
    STEMPEL="$(date -u '+%Y%m%dT%H%M%SZ')"
    mv "$SCHLIESSER" "$ERLEDIGT/${STEMPEL}_$SNAME" 2>/dev/null
    sage "----- Schliess-Ausloeser: $SNAME -----"

    # Schranke: genau 40 Zeichen, nur 0-9a-f. Ein Zeilenumbruch im Namen
    # faellt durch beide Pruefungen (Laenge und Zeichenklasse).
    case "$ERWARTET" in
        *[!0-9a-f]*) ERWARTET="" ;;
    esac
    if [ -z "$ERWARTET" ] || [ ${#ERWARTET} -ne 40 ]; then
        sage "⛔ ABGEWIESEN: Der Name nennt keinen gueltigen Commit. Nichts geschlossen."
        exit 1
    fi

    IST="$(cd "$REPO" && git --no-optional-locks rev-parse HEAD 2>/dev/null || true)"
    CTIME="$(cd "$REPO" && git --no-optional-locks log -1 --format=%ct 2>/dev/null || echo 0)"
    ALTER=$(( $(date +%s) - CTIME ))
    sage "  erwartet: $ERWARTET"
    sage "  HEAD:     ${IST:-<unbekannt>}  (Alter ${ALTER}s)"

    if [ "$ERWARTET" != "$IST" ]; then
        sage "⛔ ABBRUCH: HEAD ist nicht der gelesene Stand. Die Sitzung hat seither"
        sage "   committet - sie arbeitet oder hat gerade abgegeben. Nichts geschlossen."
        exit 1
    fi
    if [ "$ALTER" -lt 600 ]; then
        sage "⛔ ABBRUCH: Der letzte Commit ist erst ${ALTER}s alt (Schwelle 600)."
        sage "   Eine Sitzung, die eben committet hat, arbeitet womoeglich weiter."
        exit 1
    fi

    ANZ=0
    for pid in $(pgrep -x claude 2>/dev/null); do
        cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
        case "$cwd" in
            "$REPO"|"$REPO"/*) : ;;
            *) continue ;;
        esac
        daten=$(ps -o etime=,time=,stat= -p "$pid" 2>/dev/null | tr -s ' ')
        sage "  schliesse PID $pid (Laufzeit/Rechenzeit/Zustand:${daten})"
        kill -TERM "$pid" 2>/dev/null
        ANZ=$((ANZ+1))
    done

    if [ "$ANZ" -eq 0 ]; then
        sage "  Keine claude-Sitzung im Repo. Nichts zu schliessen."
    else
        sleep 5
        UEBRIG=0
        for pid in $(pgrep -x claude 2>/dev/null); do
            cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
            case "$cwd" in "$REPO"|"$REPO"/*) UEBRIG=$((UEBRIG+1)) ;; esac
        done
        sage "  $ANZ Sitzung(en) mit TERM beendet, $UEBRIG noch da."
        if [ "$UEBRIG" -gt 0 ]; then
            sage "  ⚠️ Nicht alle sind weg. KEIN -KILL: Was TERM nicht annimmt,"
            sage "     haengt an etwas, das ein Mensch ansehen sollte."
        fi
    fi
    sage "----- fertig (schliessen) -----"
    exit 0
fi


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
IM_REPO_INFO=""
for pid in $(pgrep -x claude 2>/dev/null); do
    cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
    case "$cwd" in
        "$REPO"|"$REPO"/*)
            IM_REPO=$((IM_REPO+1))
            # ⭐ Seit 23.09.2026, 16:45: nicht nur MELDEN, dass eine laeuft,
            #    sondern SEIT WANN und OB SIE NOCH ARBEITET. Zweimal an einem
            #    Tag stand eine fertige Sitzung im Weg, deren Fenster nur
            #    offen geblieben war - einmal seit zwei Tagen und 18 Stunden.
            # ⛔ Gelesen werden nur Prozesszeiten, NIE die Kommandozeile.
            daten=$(ps -o etime=,time=,stat= -p "$pid" 2>/dev/null | tr -s ' ')
            IM_REPO_INFO="${IM_REPO_INFO}PID $pid:${daten} · "
            sage "  claude im Repo: PID $pid  (Laufzeit/Rechenzeit/Zustand:${daten})"
            ;;
        *)                 FREMD=$((FREMD+1));    sage "  claude ausserhalb (zaehlt nicht): PID $pid cwd=${cwd:-unbekannt}" ;;
    esac
done
sage "claude-Prozesse: $IM_REPO im Repo, $FREMD ausserhalb."
if [ "$IM_REPO" -gt 0 ]; then
    hinweis=""
    case "$IM_REPO_INFO" in
        *" S+ "*|*" S "*|*"S+ ·"*)
            # ⚠⚠ BERICHTIGT 24.09.2026 (ARBEITSWEISE 22.7): Hier stand
            #    "Ist die Rechenzeit klein gegen die Laufzeit, ist sie fertig."
            #    GEMESSEN ist das FALSCH: untaetige Sitzung 1,6 % (45 s in 48 min),
            #    ARBEITENDE Sitzung 4,8 % (24 s in 8,5 min) - beide Zustand S+.
            #    Die Rechenzeit trennt "arbeitet" nicht von "wartet".
            hinweis=" ⭐ Zustand 'S' heisst SCHLAFEND - die Sitzung wartet auf Eingabe."
            hinweis="$hinweis ⚠ Das heisst NICHT, dass sie fertig ist: eine arbeitende"
            hinweis="$hinweis Sitzung wartet die meiste Zeit auf Antworten und steht ebenso auf S."
            hinweis="$hinweis ⭐ Belastbar ist das ALTER DES LETZTEN COMMITS. Ist die Abgabe da,"
            hinweis="$hinweis gelesen und mindestens 10 min alt, schliesst der Schliess-Ausloeser"
            hinweis="$hinweis die Sitzung: Datei _ausloeser/schliesse_<HEAD-Hash> (ARBEITSWEISE 22.8)."
            ;;
    esac
    abbruch "Es arbeitet bereits eine claude-Sitzung im Repo ($IM_REPO). Der Waechter startet keine zweite. ${IM_REPO_INFO}${hinweis}"
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
# ⛔⛔ ZURUECKGENOMMEN am 23.09.2026, 18:25 — ZWEITER GEGENBEFUND.
#   Der Versuch, den Auftrag als Argument mitzugeben (`claude --remote-control
#   "<Satz>"`), ist GEMESSEN GESCHEITERT: Die Sitzung startete, die App zeigte
#   sie leer, kein Auftrag angekommen. Das deckt sich mit der Messung vom
#   19.09. (ARBEITSWEISE Abschnitt 14, v2.1.278) — der Verdacht, dort habe
#   Termius die Anfuehrungszeichen zerlegt, ist damit WIDERLEGT: Hier lief
#   nichts ueber Termius, der Satz lag in einer Datei, und er kam trotzdem
#   nicht an. `claude --help` nennt `[prompt]` als Argument; die interaktive
#   Sitzung nimmt ihn offenbar nicht an.
# ⚠️ Und der Waechter meldete faelschlich Erfolg: Die Schwelle "arbeitet ab
#   2 s Rechenzeit" war GERATEN. Das blosse Hochfahren verbraucht 3 s. Dadurch
#   griff der Rueckfall nicht. Gemessen: nach 6 Minuten erst 7 s CPU, S+.
# ⇒ Der Satz wird wieder ins Fenster GETIPPT, ohne Enter (Betreiberentscheidung
#   23.09.2026 Mittag). Die Datei bleibt - sie dient dem Rueckfall.
#
# (ueberholt) Der Auftrag geht als ARGUMENT mit.
#   `claude --help` nennt `[prompt]` als positionales Argument. Damit entfaellt
#   das Tippen per AppleScript UND das Enter des Betreibers.
# ⚠️ ARBEITSWEISE Abschnitt 14 nennt einen Gegenbefund (19.09., v2.1.278: Text
#   kam nicht an). Der lief ueber Termius/SSH, wo mehrzeilige Bloecke und
#   Anfuehrungszeichen zerfallen. Hier geht nichts durch eine fremde Zeile:
#   Der Satz liegt in einer DATEI, die Shell liest sie selbst. Durch AppleScript
#   laeuft nur der Dateipfad.
# ⇒ Schlaegt es fehl, faellt der Waechter auf den alten Weg zurueck (Schritt 7).
SATZDATEI="$LOGDIR/auftragssatz_$NUMMER.txt"
printf '%s' "$SATZ" > "$SATZDATEI" || abbruch "Konnte den Auftragssatz nicht ablegen."
sage "Auftragssatz abgelegt: $(wc -c < "$SATZDATEI") Bytes"

sage "Starte Terminal-Fenster (Auftrag als Argument) ..."
FENSTER=$(osascript <<OSA 2>>"$LOG"
tell application "Terminal"
    set neu to do script "cd ~/trading-bot && exec claude --effort high --remote-control"
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
# 7. Hat der Auftrag gegriffen? Messen statt annehmen.
# --------------------------------------------------------------------------
# ⭐ Wenn der Prompt als Argument ankam, ARBEITET die Sitzung bereits - sie
#   verbraucht Rechenzeit. Bleibt sie bei fast null, wartet sie auf Eingabe.
printf '%s\n' "$SATZ" > "$LOGDIR/letzter_satz.txt"
osascript <<OSA 2>>"$LOG"
tell application "Terminal"
    do script "$SATZ" in window id $FENSTER
end tell
OSA
if [ $? -ne 0 ]; then
    sage "⚠️ Der Satz konnte nicht uebergeben werden. Das FENSTER LAEUFT aber."
    sage "   Auftragssatz zum Einfuegen von Hand: $LOGDIR/letzter_satz.txt"
    exit 1
fi
sage "⭐ Satz ins Fenster gelegt. ⚠️ ER IST NICHT ABGESCHICKT."
sage "   Der Betreiber schickt ihn ab - in der Claude-App unter der"
sage "   Geraetesitzung (Laptop-Symbol, noch OHNE TB-Nummer im Titel)"
sage "   oder im Terminalfenster mit Enter."
sage "   Der Satz steht auch in $LOGDIR/letzter_satz.txt"
sage "----- fertig -----"
exit 0
