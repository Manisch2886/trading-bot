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

# ⭐⭐ SEIT TB-144 (Waechter-Reparatur). Anlass: Fehler Nr. 23 - 20 Starts in
#    Folge meldeten das VORDERSTE Fenster (15501) statt des neu geoeffneten,
#    und der Satz ging samt Zeilenende in eine bash-Shell.
# ⛔ Der Waechter legt KEINEN Satz mehr in ein Fenster, schickt nichts ab und
#    drueckt keine Taste. Den Fensterinhalt LIEST er nur, ueber Terminal selbst.
# ⛔ Ins Log gehen hoechstens die letzten 8 Zeilen (je 160 Zeichen) des NEU
#    GEOEFFNETEN Fensters, und nur, wenn die Pruefung scheitert. Sonst gilt der
#    Kopf dieser Datei: keine Umgebungsvariablen, Schluessel, Dateiinhalte.
# ⚠️ /bin/bash des Macs ist 3.2: nur Mittel, die es dort gibt.
# ⚠️ Solange ein Wert mit <<M…>> dasteht, oeffnet der Waechter KEIN Fenster.
# --------------------------------------------------------------------------
STARTZEILE="cd ~/trading-bot && exec claude --permission-mode manual --effort high --remote-control --no-chrome"
MERKMAL_FRAGE="Enter to confirm"
MERKMAL_EINGABEZEILE="? for shortcuts"
LESE_EIGENSCHAFT="contents"
STUFEN="3 3 4 5 5 10 10 10 10"
FENSTER_SCHLIESSEN="ja"
FENSTERDATEI="$LOGDIR/letztes_fenster.txt"
FENSTER=""
TABNR=""

ziffern() {
    case "$1" in ''|*[!0-9]*) return 1 ;; esac
    return 0
}

# PIDs aller claude-Prozesse mit cwd im Repo; gelesen wird nur das cwd (wie Wache 4a).
claude_im_repo() {
    local pid cwd
    for pid in $(pgrep -x claude 2>/dev/null); do
        cwd=$(lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | grep '^n' | cut -c2-)
        case "$cwd" in "$REPO"|"$REPO"/*) echo "$pid" ;; esac
    done
}

fensterliste() {
    osascript <<OSA 2>>"$LOG"
tell application "Terminal" to return id of every window
OSA
}

fenster_starten() {
    osascript <<OSA 2>>"$LOG"
tell application "Terminal"
    set neu to do script "$STARTZEILE"
    return neu
end tell
OSA
}

# Nur lesen. M2: LESE_EIGENSCHAFT am Funktionsverzeichnis von Terminal pruefen.
fenster_lesen() {
    osascript <<OSA 2>>"$LOG"
with timeout of 10 seconds
    tell application "Terminal" to return $LESE_EIGENSCHAFT of tab $TABNR of window id $FENSTER
end timeout
OSA
}

fenster_tty() {
    osascript <<OSA 2>>"$LOG"
with timeout of 10 seconds
    tell application "Terminal" to return tty of tab $TABNR of window id $FENSTER
end timeout
OSA
}

# M4: schliesst Terminal ein Fenster ohne laufenden Prozess ohne Rueckfrage?
fenster_zu() {
    osascript <<OSA 2>>"$LOG"
with timeout of 10 seconds
    tell application "Terminal"
        if not (exists window id $1) then return "fehlt"
        if (count of tabs of window id $1) is not 1 then return "mehrere"
        if busy of tab 1 of window id $1 then return "arbeitet"
        close window id $1
        delay 1
        if exists window id $1 then return "offen"
        return "zu"
    end tell
end timeout
OSA
}

# V1: Die Fensternummer kommt aus dem Tab, den Terminal beim Oeffnen liefert.
# M1: Form der Rueckgabe "tab <k> of window id <n>" - belegt nur fuer den alten
#     zweiten Aufruf (launchd_aus.log, 51 Zeilen); fuers Oeffnen misst TB-144.
fenster_oeffnen() {
    local vorher nachher tab rest
    FENSTER=""
    TABNR=""
    case "$MERKMAL_EINGABEZEILE$FENSTER_SCHLIESSEN$STARTZEILE" in
        *"<<"*)
            sage "⛔ MESSWERTE FEHLEN in starte_sitzung.sh (TB-144). Kein Fenster geoeffnet."
            return 1 ;;
    esac
    vorher=$(fensterliste) || {
        sage "⛔ FENSTERLISTE NICHT LESBAR: Terminal nennt seine Fenster nicht. Kein Fenster geoeffnet."
        return 1
    }
    vorher=" $(printf '%s' "$vorher" | tr -c '0-9' ' ') "
    tab=$(fenster_starten) || {
        sage "⛔ osascript konnte Terminal nicht ansteuern. Fehlt die Automation-Berechtigung?"
        return 1
    }
    nachher=" $(fensterliste | tr -c '0-9' ' ') "
    case "$tab" in
        "tab "*" of window id "*)
            rest="${tab#tab }"
            TABNR="${rest%% of window id *}"
            FENSTER="${tab##* of window id }" ;;
    esac
    if ! ziffern "$TABNR" || ! ziffern "$FENSTER"; then
        sage "⛔ FENSTER NICHT BESTIMMBAR: Terminal lieferte keinen Tab der Form 'tab <k> of window id <n>'. Ein Fenster kann trotzdem offen sein."
        FENSTER=""
        return 1
    fi
    case "$vorher" in *" $FENSTER "*)
        sage "⛔ FENSTER NICHT NEU: Fenster $FENSTER gab es schon vor dem Oeffnen. Es wird weder gelesen noch gemerkt."
        FENSTER=""
        return 1 ;;
    esac
    case "$nachher" in *" $FENSTER "*) : ;; *)
        sage "⛔ FENSTER FEHLT: Fenster $FENSTER steht nach dem Oeffnen nicht in der Fensterliste."
        FENSTER=""
        return 1 ;;
    esac
    printf '%s\n' "$FENSTER" > "$FENSTERDATEI"
    sage "Fenster $FENSTER neu geoeffnet (Tab $TABNR). Gemerkt in $FENSTERDATEI"
    return 0
}

# ⛔ Begrenzt: hoechstens 8 Zeilen, je 160 Zeichen, nur vom neu geoeffneten Fenster.
fensterzeilen() {
    local z
    sage "   Letzte Zeilen von Fenster $FENSTER (hoechstens 8, je 160 Zeichen):"
    printf '%s\n' "$1" | tr '\r' '\n' | grep -v '^[[:space:]]*$' | tail -n 8 | cut -c1-160 | while IFS= read -r z; do
        sage "   | $z"
    done
}

# V3: Pruefung statt Wartezeit. $1 = Kennung fuers Log (TB-Nummer oder PROBE).
# Rueckgabe: 0 eingabebereit · 3 Startfrage · 4 keine Eingabezeile.
warte_auf_eingabezeile() {
    local kenn="$1" summe=0 lesung=0 gelesen=0 bereit=0 inhalt="" s
    for s in $STUFEN; do
        sleep "$s"
        summe=$((summe+s))
        lesung=$((lesung+1))
        inhalt=$(fenster_lesen) || { inhalt=""; bereit=0; continue; }
        gelesen=$((gelesen+1))
        case "$inhalt" in
            *"$MERKMAL_FRAGE"*)
                sage "⛔ STARTFRAGE ($kenn): Fenster $FENSTER zeigt nach $summe s eine Frage (\"$MERKMAL_FRAGE\"). Die Sitzung ist NICHT eingabebereit."
                fensterzeilen "$inhalt"
                return 3 ;;
            *"$MERKMAL_EINGABEZEILE"*)
                bereit=$((bereit+1))
                if [ "$bereit" -ge 2 ]; then
                    sage "⭐ EINGABEBEREIT ($kenn): Fenster $FENSTER, Eingabezeile steht, keine Frage offen (nach $summe s, Lesung $lesung). ⚠️ KEIN SATZ IM FENSTER."
                    return 0
                fi ;;
            *)  bereit=0 ;;
        esac
    done
    sage "⛔ KEINE EINGABEZEILE ($kenn): Fenster $FENSTER zeigt nach $summe s keine Eingabezeile von Claude Code (verlangt: zwei Lesungen in Folge). Die Sitzung gilt als NICHT eingabebereit."
    sage "   Lesbar waren $gelesen von $lesung Lesungen (0 = Terminal hat nicht geantwortet; dann liegt es nicht am Merkmal)."
    fensterzeilen "$inhalt"
    return 4
}

# V5: nur das EINE gemerkte Fenster; nur ohne claude-Sitzung im Repo (ausser der
# PID in $1, die die Probe ausloest), nur ein Tab, nur ohne laufenden Prozess.
fenster_aufraeumen() {
    local ausser="${1:-}" f pid antwort
    if [ ! -f "$FENSTERDATEI" ]; then
        sage "  Kein gemerktes Fenster. Nichts aufzuraeumen."
        return 0
    fi
    f=$(head -n 1 "$FENSTERDATEI" | tr -d '\r')
    if ! ziffern "$f"; then
        sage "  ⚠️ $FENSTERDATEI nennt keine Fensternummer. Nichts geschlossen."
        return 0
    fi
    for pid in $(claude_im_repo); do
        [ "$pid" = "$ausser" ] && continue
        sage "  ⚠️ Fenster $f bleibt offen: im Repo laeuft noch eine claude-Sitzung (PID $pid)."
        return 0
    done
    if [ "$FENSTER_SCHLIESSEN" != "ja" ] && [ "$FENSTER_SCHLIESSEN" != "nein" ]; then
        sage "  ⚠️ Fenster $f bleibt offen: FENSTER_SCHLIESSEN steht weder auf ja noch auf nein (Messwert M4 fehlt)."
        return 0
    fi
    if [ "$FENSTER_SCHLIESSEN" != "ja" ]; then
        sage "  ⚠️ Fenster $f bleibt offen: Terminal schliesst es nicht ohne Rueckfrage (gemessen in TB-144)."
        return 0
    fi
    antwort=$(fenster_zu "$f")
    case "$antwort" in
        zu)
            mv "$FENSTERDATEI" "$LOGDIR/letztes_fenster_geschlossen.txt" 2>/dev/null
            sage "  Fenster $f geschlossen (das beim Start gemerkte, kein laufender Prozess)." ;;
        fehlt)    sage "  Fenster $f gibt es nicht mehr. Nichts geschlossen." ;;
        arbeitet) sage "  ⚠️ Fenster $f bleibt offen: dort laeuft noch ein Prozess." ;;
        mehrere)  sage "  ⚠️ Fenster $f bleibt offen: es hat mehr als einen Tab." ;;
        *)        sage "  ⚠️ Fenster $f bleibt offen: Terminal hat das Schliessen nicht bestaetigt." ;;
    esac
    return 0
}

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
    # ⭐ Seit TB-144 (V5): das beim Start gemerkte Fenster aufraeumen.
    fenster_aufraeumen
    sage "----- fertig (schliessen) -----"
    exit 0
fi


# --------------------------------------------------------------------------
# 1. Die Ausloeserdatei finden. Nur der NAME zaehlt.
# --------------------------------------------------------------------------

# ⭐ 1a. PROBE-AUSLOESER (seit TB-144): Datei probe_<PID>
#    Oeffnet ein Fenster wie ein echter Start (gleicher Ordner, gleiche
#    Startzeile, dieselben Funktionen), prueft die Eingabezeile, beendet GENAU
#    DIE EINE dabei entstandene Sitzung mit TERM und raeumt das Fenster auf.
#    KEIN Auftrag, KEIN Satz. <PID> ist die eine claude-Sitzung im Repo, die
#    die Probe ausloest; nur sie wird nicht gezaehlt. Laeuft im Repo eine
#    andere, oder ist <PID> keine claude-Sitzung im Repo: ABBRUCH, kein Fenster.
# ⚠️ Die Wache 4a fuer echte Starts steht unveraendert weiter unten.
# ⚠️ Auch hier wird nur der DATEINAME gelesen, nie der Inhalt.
PROBE=""
for f in "$AUSLOESER"/probe_*; do
    [ -e "$f" ] || continue
    PROBE="$f"
    break
done
if [ -n "$PROBE" ]; then
    EIGEN="$(basename "$PROBE")"
    EIGEN="${EIGEN#probe_}"
    STEMPEL="$(date -u '+%Y%m%dT%H%M%SZ')"
    if ! ziffern "$EIGEN" || [ ${#EIGEN} -gt 7 ]; then
        mv "$PROBE" "$ERLEDIGT/ABGEWIESEN_${STEMPEL}_probe" 2>/dev/null
        sage "⛔ ABGEWIESEN: Der Probe-Ausloeser nennt keine gueltige PID."
        exit 1
    fi
    mv "$PROBE" "$ERLEDIGT/${STEMPEL}_probe_$EIGEN" || { sage "⛔ Konnte Probe-Ausloeser nicht wegraeumen. Abbruch."; exit 1; }
    sage "----- Probe-Ausloeser: probe_$EIGEN -----"
    GENANNT=0
    ANDERE=0
    for pid in $(claude_im_repo); do
        if [ "$pid" = "$EIGEN" ]; then GENANNT=1; else ANDERE=$((ANDERE+1)); fi
    done
    if [ "$GENANNT" -ne 1 ] || [ "$ANDERE" -ne 0 ]; then
        sage "⛔ ABBRUCH (Probe): PID $EIGEN als claude-Sitzung im Repo: $GENANNT (verlangt 1), andere claude-Sitzungen im Repo: $ANDERE (verlangt 0). Kein Fenster geoeffnet."
        exit 1
    fi
    if ! security show-keychain-info "$HOME/Library/Keychains/login.keychain-db" > /dev/null 2>&1; then
        sage "⛔ ABBRUCH (Probe): Schluesselbund gesperrt. Kein Fenster geoeffnet."
        exit 1
    fi
    FENSTERDATEI="$LOGDIR/letztes_fenster_probe.txt"
    fenster_oeffnen || { sage "----- fertig (probe), rc 1 -----"; exit 1; }
    warte_auf_eingabezeile "PROBE"
    RC=$?
    # Beendet wird nur, was im Repo laeuft, NICHT die genannte PID ist und am
    # Terminal des neuen Tabs haengt.
    TTY_TAB="$(fenster_tty)"
    for pid in $(claude_im_repo); do
        [ "$pid" = "$EIGEN" ] && continue
        TTY_PID="$(ps -o tty= -p "$pid" 2>/dev/null | tr -d ' ')"
        if [ -n "$TTY_PID" ] && [ "/dev/$TTY_PID" = "$TTY_TAB" ]; then
            sage "  Probe: beende PID $pid ($TTY_PID) mit TERM. PID $EIGEN bleibt unberuehrt."
            kill -TERM "$pid" 2>/dev/null
        else
            sage "  ⚠️ Probe: PID $pid haengt nicht am neuen Tab (${TTY_PID:-?} gegen ${TTY_TAB:-?}). NICHT beendet."
            [ "$RC" -eq 0 ] && RC=5    # 5: eingabebereit, aber eine Probe-Sitzung steht noch
        fi
    done
    sleep 5
    fenster_aufraeumen "$EIGEN"
    sage "----- fertig (probe), rc $RC -----"
    exit "$RC"
fi

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

sage "Starte Terminal-Fenster (seit TB-142: ohne Satz) ..."
fenster_oeffnen || abbruch "Das neue Terminal-Fenster ist nicht offen oder nicht bestimmbar - siehe die Zeile davor im Protokoll."

# --------------------------------------------------------------------------
# 7. Steht die Eingabezeile? Lesen statt warten (seit TB-144).
# --------------------------------------------------------------------------
# ⛔ Der Satz wird NICHT mehr ins Fenster gelegt (V4): Der Terminal-Befehl,
#   der Text in ein vorhandenes Fenster gibt, schickt eine Befehlszeile samt
#   Zeilenende - im richtigen Fenster waere das das Abschicken, das
#   ARBEITSWEISE 19 ausschliesst. Der Satz steht in der Datei.
printf '%s\n' "$SATZ" > "$LOGDIR/letzter_satz.txt"
warte_auf_eingabezeile "$NUMMER"
RC=$?
sage "   Der Waechter legt keinen Satz ins Fenster. Wortlaut: $LOGDIR/letzter_satz.txt"
if [ "$RC" -eq 0 ]; then
    sage "   Der Betreiber schickt ihn ab - in der Claude-App unter der"
    sage "   Geraetesitzung (Laptop-Symbol) oder im Terminal-Fenster $FENSTER."
else
    sage "   Fenster $FENSTER bleibt offen. Schliessen: _ausloeser/schliesse_<HEAD> (ARBEITSWEISE 22.8)."
    printf '%s\n' "Start $NUMMER: Fenster $FENSTER ist nicht eingabebereit (Rueckgabe $RC). Siehe waechter.log." > "$LOGDIR/letzter_abbruch.txt"
fi
sage "----- fertig -----"
exit "$RC"
