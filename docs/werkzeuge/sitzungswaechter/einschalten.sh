#!/bin/bash
# Sitzungswaechter ein- oder ausschalten. ⛔ NUR auf dem MacBook.
#
#   Einschalten:  bash docs/werkzeuge/sitzungswaechter/einschalten.sh
#   Ausschalten:  bash docs/werkzeuge/sitzungswaechter/einschalten.sh aus
#   Nachsehen:    bash docs/werkzeuge/sitzungswaechter/einschalten.sh stand
#
# ⛔ Gibt nie Schluessel, Umgebungsvariablen oder fremde launchd-Eintraege aus.
#    Geprueft wird ausschliesslich die Existenz DIESES einen Eintrags.

set -u
LABEL="de.trading-bot.sitzungswaechter"
HIER="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HIER/../../.." && pwd)"
AGENTS="$HOME/Library/LaunchAgents"
PLIST="$AGENTS/$LABEL.plist"
MODUS="${1:-ein}"

if [ "$(uname -s)" != "Darwin" ]; then
    echo "⛔ ABBRUCH: Das ist nicht das MacBook. Der Waechter gehoert dorthin."
    exit 1
fi
if [ "$REPO" != "$HOME/trading-bot" ]; then
    echo "⛔ ABBRUCH: Erwartet wird ~/trading-bot, gefunden: $REPO"
    echo "   Der Waechter ist auf diesen Pfad festgelegt (launchd kennt kein ~)."
    exit 1
fi

stand() {
    echo "== Stand =="
    if [ -f "$PLIST" ]; then echo "  Agent-Datei:  da"; else echo "  Agent-Datei:  fehlt"; fi
    n=$(launchctl list 2>/dev/null | grep -c "$LABEL")
    if [ "$n" -gt 0 ]; then echo "  Geladen:      ja"; else echo "  Geladen:      nein"; fi
    echo "  Ausloeserordner: $(ls -1 "$REPO/docs/auftraege/_ausloeser"/starte_TB-* 2>/dev/null | wc -l | tr -d ' ') wartende Datei(en)"
    if [ -f "$REPO/logs/sitzungswaechter/waechter.log" ]; then
        echo "  Letzte Zeilen des Protokolls:"
        tail -5 "$REPO/logs/sitzungswaechter/waechter.log" | sed 's/^/    /'
    else
        echo "  Protokoll:    noch keines"
    fi
}

case "$MODUS" in
  aus)
    launchctl unload "$PLIST" 2>/dev/null
    if [ -f "$PLIST" ]; then mv "$PLIST" "$PLIST.aus_$(date -u '+%Y%m%dT%H%M%SZ')"; fi
    echo "✔ Ausgeschaltet. Der Waechter reagiert auf nichts mehr."
    stand
    ;;
  stand)
    stand
    ;;
  ein)
    mkdir -p "$AGENTS" "$REPO/docs/auftraege/_ausloeser/_erledigt" "$REPO/logs/sitzungswaechter"

    # ⚠️ Nie ueberschreiben: eine vorhandene Fassung wird beiseitegelegt.
    if [ -f "$PLIST" ]; then
        launchctl unload "$PLIST" 2>/dev/null
        mv "$PLIST" "$PLIST.vorher_$(date -u '+%Y%m%dT%H%M%SZ')"
        echo "  (vorhandene Fassung beiseitegelegt)"
    fi

    sed "s|__HOME__|$HOME|g" "$HIER/$LABEL.plist" > "$PLIST" || { echo "⛔ Konnte Agent-Datei nicht schreiben."; exit 1; }
    grep -q "__HOME__" "$PLIST" && { echo "⛔ Platzhalter nicht ersetzt. Abbruch."; rm -f "$PLIST"; exit 1; }
    chmod 644 "$PLIST"

    launchctl load "$PLIST" || { echo "⛔ launchctl load fehlgeschlagen."; exit 1; }
    echo "✔ Eingeschaltet."
    echo
    stand
    echo
    echo "⚠️ ZWEI DINGE, DIE NUR DU PRUEFEN KANNST:"
    echo "   1. Beim ERSTEN Lauf fragt macOS, ob Terminal gesteuert werden darf."
    echo "      Kommt die Frage nicht, steht die Erlaubnis in"
    echo "      Systemeinstellungen > Datenschutz & Sicherheit > Automation."
    echo "   2. Der Schluesselbund muss entsperrt sein, sonst bricht der Waechter"
    echo "      ab (und das ist Absicht - sonst laeuft die Sitzung ueber"
    echo "      API Usage Billing statt ueber dein Abo)."
    ;;
  *)
    echo "Unbekannt: $MODUS   (ein | aus | stand)"
    exit 1
    ;;
esac
