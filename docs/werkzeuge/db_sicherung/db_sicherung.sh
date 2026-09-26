#!/bin/bash
# db_sicherung.sh - taegliche Sicherung der SQLite-Datenbanken des Projekts (TB-112, Fable 25f O6)
# ==============================================================================================
# Die Paper-Trading-Datenbanken existieren nur auf diesem MacBook und sind die einzige Evidenz
# aus dem Paper-Betrieb (Pruefprinzip D6). Dieses Skript hat EINE Aufgabe: sie lesend kopieren.
#
#   bash docs/werkzeuge/db_sicherung/db_sicherung.sh [<basisordner>]
#
# <basisordner> ohne Angabe:
#   ~/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung   (iCloud Drive)
# Die Sicherung landet in <basisordner>/<JJJJ-MM-TT>/. Gibt es den Ordner schon (zweiter Lauf am
# selben Tag), in <basisordner>/<JJJJ-MM-TT>_<HHMMSS>/ - eine vorhandene Sicherung wird nie
# ueberschrieben.
#
# Ablauf je Datenbank (*.db im Repo-Wurzelordner und unter strategies/*/):
#   1. `sqlite3 -readonly <db> ".backup '<zwischenkopie>'"` - die Backup-API von SQLite, lesend,
#      mit Lesesperre; sicher, auch wenn gerade ein Cron schreibt. ⛔ Kein `cp`.
#      Die Zwischenkopie liegt in einem eigenen Ordner unter $TMPDIR, NICHT im Sicherungsziel.
#   2. Schluessel-Pruefung an der Zwischenkopie: nur das SCHEMA (Tabellen- und Spaltennamen).
#      Gezaehlt werden Spaltennamen, die wie key, secret, token, api, passw aussehen.
#      ⛔ Es wird nie ein Wert gelesen oder ausgegeben - nur Namen und Zahlen.
#      Treffer: die Datei wird NICHT gesichert, bis der Betreiber entscheidet; die Zwischenkopie
#      bleibt liegen (Pfad steht in der Meldung).
#   3. Ohne Treffer: Zwischenkopie ins Ziel verschieben (`mv -n`), dort `PRAGMA integrity_check`
#      (erwartet `ok`) und sha256 der Kopie in <ziel>/SHA256SUMS.
#
# ⛔ Das Skript loescht nichts: keine Sicherung, keine Datenbank, keine Zwischenkopie. Entfernt
#    wird am Ende nur der eigene, dann LEERE Zwischenordner (`rmdir`, scheitert bei Inhalt).
#    Aufbewahrung alter Saetze ist eine offene Frage an den Betreiber.
# ⛔ Die Originaldatenbanken werden nur ueber `sqlite3 -readonly ... .backup` gelesen.
#
# Rueckgabewert: 0 nur, wenn jede gefundene Datenbank gesichert ist und jede Kopie `ok` meldet.
#                1 sonst - die Meldung nennt die Datei (auch: Schluessel-Verdacht, Ziel nicht
#                beschreibbar, z. B. "Operation not permitted" ohne Festplattenvollzugriff).
# Protokoll: auf stdout und als <ziel>/PROTOKOLL.txt.

set -u
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"
umask 077

HIER="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HIER/../../.." && pwd)"
BASIS="${1:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/trading-bot-db-sicherung}"
MUSTER='key|secret|token|api|passw'

TAG="$(date '+%Y-%m-%d')"
ZIEL="$BASIS/$TAG"
[ -e "$ZIEL" ] && ZIEL="$BASIS/${TAG}_$(date '+%H%M%S')"

PROTOKOLL_ZEILEN=()
p() { echo "$*"; PROTOKOLL_ZEILEN+=("$*"); }

p "# db_sicherung $(date '+%Y-%m-%d %H:%M:%S %z')"
p "# Repo:  $REPO"
p "# Ziel:  $ZIEL"

if [ -e "$ZIEL" ]; then
    p "FEHLER: $ZIEL existiert schon - es wird nichts ueberschrieben."
    exit 1
fi
if ! FEHLER_MKDIR="$(mkdir -p "$ZIEL" 2>&1)"; then
    p "FEHLER: Zielordner nicht anlegbar: $FEHLER_MKDIR"
    p "        Bei 'Operation not permitted': Cron bzw. Terminal braucht 'Festplattenvollzugriff'"
    p "        (Systemeinstellungen > Datenschutz & Sicherheit). Siehe LIESMICH.md."
    exit 1
fi
if ! ZWISCHEN="$(mktemp -d "${TMPDIR:-/tmp}/db_sicherung.XXXXXX")"; then
    p "FEHLER: Zwischenordner nicht anlegbar."
    exit 1
fi

# Die Datenbanken, sortiert, relativ zum Repo (Wurzelordner und strategies/*/).
DBS=()
while IFS= read -r f; do DBS+=("$f"); done < <(
    cd "$REPO" && { ls -1 ./*.db strategies/*/*.db 2>/dev/null; } | sed 's#^\./##' | sort)
p "# gefunden: ${#DBS[@]} Datenbanken"
for f in "${DBS[@]}"; do p "#   $f"; done

FEHLERZAHL=0
GESICHERT=0
for rel in "${DBS[@]}"; do
    quelle="$REPO/$rel"
    zwischen="$ZWISCHEN/$(echo "$rel" | tr '/' '_')"
    # 1. lesend kopieren
    if ! aus="$(sqlite3 -readonly "$quelle" ".backup '$zwischen'" 2>&1)"; then
        p "FEHLER  $rel: .backup scheiterte: $aus"
        FEHLERZAHL=$((FEHLERZAHL + 1)); continue
    fi
    # 2. Schluessel-Pruefung - nur Namen, nie Werte
    spalten="$(sqlite3 -readonly "$zwischen" \
        "SELECT m.name || '.' || c.name FROM sqlite_master m JOIN pragma_table_info(m.name) c
         WHERE m.type = 'table' ORDER BY 1;" 2>&1)" || {
        p "FEHLER  $rel: Schema nicht lesbar: $spalten"
        FEHLERZAHL=$((FEHLERZAHL + 1)); continue; }
    n_spalten=$(printf '%s\n' "$spalten" | grep -c . )
    treffer="$(printf '%s\n' "$spalten" | awk -F. -v m="$MUSTER" 'tolower($2) ~ m' )"
    n_treffer=$(printf '%s\n' "$treffer" | grep -c . )
    if [ "$n_treffer" -gt 0 ]; then
        p "NICHT GESICHERT  $rel: Schluessel-Verdacht in $n_treffer von $n_spalten Spaltennamen:" \
          "$(printf '%s\n' "$treffer" | tr '\n' ' ')- Entscheidung des Betreibers noetig." \
          "Zwischenkopie bleibt liegen: $zwischen"
        FEHLERZAHL=$((FEHLERZAHL + 1)); continue
    fi
    # 3. ins Ziel, pruefen, Quersumme
    mkdir -p "$ZIEL/$(dirname "$rel")"
    if ! aus="$(mv -n "$zwischen" "$ZIEL/$rel" 2>&1)" || [ ! -f "$ZIEL/$rel" ] || [ -e "$zwischen" ]; then
        p "FEHLER  $rel: Verschieben ins Ziel scheiterte: $aus"
        FEHLERZAHL=$((FEHLERZAHL + 1)); continue
    fi
    ic="$(sqlite3 -readonly "$ZIEL/$rel" "PRAGMA integrity_check;" 2>&1)"
    if [ "$ic" != "ok" ]; then
        p "FEHLER  $rel: integrity_check der Kopie: $(echo "$ic" | head -3 | tr '\n' ' ')"
        FEHLERZAHL=$((FEHLERZAHL + 1)); continue
    fi
    (cd "$ZIEL" && shasum -a 256 "$rel") >> "$ZIEL/SHA256SUMS"
    groesse=$(wc -c < "$ZIEL/$rel" | tr -d ' ')
    p "ok      $rel  ($groesse B, $n_spalten Spalten, 0 Schluessel-Verdacht, integrity_check ok)"
    GESICHERT=$((GESICHERT + 1))
done

rmdir "$ZWISCHEN" 2>/dev/null || p "# Zwischenordner nicht leer, bleibt: $ZWISCHEN"
SATZ=$(du -sk "$ZIEL" | cut -f1)
p "# gesichert ${GESICHERT} von ${#DBS[@]}, Fehler ${FEHLERZAHL}, Satzgroesse ${SATZ} KiB"
if [ "$FEHLERZAHL" -eq 0 ] && [ "$GESICHERT" -eq "${#DBS[@]}" ] && [ "$GESICHERT" -gt 0 ]; then
    RC=0
else
    RC=1
fi
p "# Rueckgabewert $RC"
printf '%s\n' "${PROTOKOLL_ZEILEN[@]}" > "$ZIEL/PROTOKOLL.txt"
exit $RC
