#!/bin/bash
# TB-98 Block B, Proben B1/B2/B4 am umgebauten Erzeuger. Ohne Selektionsmodus
# (geprueft wird die Zielbestimmung, nicht die Datenquelle). Alle Ziele liegen
# im Scratchpad - AUSSER B2c, das die Sperre gegen den historischen Ordner
# research/tb24_haltedauern/daten/ selbst prueft (Hashes vorher/nachher, mtime).
# Aufruf aus der Repo-Wurzel:  bash docs/belege/TB-98/b_proben.sh <scratch>
set -u
SP="$1/b_proben"; mkdir -p "$SP"
PY=trading-env/bin/python3
PH=research/tb24_haltedauern/positionen_holen.py
AB=research/tb24_haltedauern/alle_bots.py
D=research/tb24_haltedauern/daten
echo "# TB-98 B-Proben, HEAD $(git rev-parse --short HEAD) + Arbeitsbaum (Block B), $(date '+%Y-%m-%d %H:%M:%S %z')"
zeige() { sed "s#$1/##g; s#$PWD/##g" | sed 's/^/    | /'; }
inhalt() { echo "    Inhalt $1: [$(ls -A "$1" | tr '\n' ' ')]"; }

echo; echo "## B1a ohne --ziel"
$PY -W ignore $PH rsi2_crypto 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"
echo; echo "## B1b ganz ohne Argument"
$PY -W ignore $PH 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"
echo; echo "## B1c --ziel auf einen fehlenden Ordner"
$PY -W ignore $PH rsi2_crypto --ziel "$SP/gibt_es_nicht" 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"
test -e "$SP/gibt_es_nicht" && echo "    FEHLER: Ordner wurde angelegt" || echo "    Ordner nicht angelegt"
echo; echo "## B1d Bot-Name nicht an erster Stelle"
mkdir -p "$SP/b1d"
$PY -W ignore $PH --ziel "$SP/b1d" rsi2_crypto 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"; inhalt "$SP/b1d"

echo; echo "## B2a Zieldatei besteht (Kopie der alten Liste) - mit Lesehaken: wird gerechnet?"
mkdir -p "$SP/b2a" "$SP/b2a_prot"; cp -p "$D/rsi2_crypto_alle_trades.csv" "$SP/b2a/"
V=$(shasum -a 256 "$SP/b2a/rsi2_crypto_alle_trades.csv"); VM=$(stat -f %m "$SP/b2a/rsi2_crypto_alle_trades.csv")
T0=$(date +%s)
env PYTHONPATH=docs/belege/TB-98/haken TB98_PROTOKOLL="$SP/b2a_prot" \
    $PY -W ignore $PH rsi2_crypto --ziel "$SP/b2a" 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}, $(( $(date +%s) - T0 )) s"
N=$(shasum -a 256 "$SP/b2a/rsi2_crypto_alle_trades.csv"); NM=$(stat -f %m "$SP/b2a/rsi2_crypto_alle_trades.csv")
[ "$V" = "$N" ] && [ "$VM" = "$NM" ] && echo "    vorhandene Datei: Hash und mtime unveraendert" || echo "    FEHLER: vorhandene Datei veraendert"
inhalt "$SP/b2a"
echo "    Kursdateien geoeffnet (Lesehaken, *_1d.csv/_4h.csv/_1h.csv): $(cat "$SP"/b2a_prot/*.tsv | cut -f2 | grep -c '_1[dh]\.csv$\|_4h\.csv$')"
echo "    equity_simulation geladen (Lesehaken): $(cat "$SP"/b2a_prot/*.tsv | cut -f2 | grep -c 'equity_simulation')"

echo; echo "## B2b _schreibe_einmal auf eine Datei, die waehrend des Laufs entsteht (Import, im Speicher)"
mkdir -p "$SP/b2b"
$PY -W ignore - "$SP/b2b" <<'PYEOF' 2>&1 | zeige "$SP"
import os, sys, hashlib
z = sys.argv[1]
sys.argv = ["research/tb24_haltedauern/positionen_holen.py", "rsi2_crypto", "--ziel", z]
sys.path.insert(0, "research/tb24_haltedauern")
import positionen_holen as ph
h = ph._schreibe_einmal("neu.txt", "a,b\n1,2\n")
print("neu geschrieben, Hash stimmt mit dem Inhalt:", h == hashlib.sha256(b"a,b\n1,2\n").hexdigest())
open(os.path.join(z, "da.txt"), "w").write("vorher\n")
try:
    ph._schreibe_einmal("da.txt", "nachher\n")
    print("FEHLER: kein Abbruch")
except SystemExit as e:
    print("SystemExit", e.code, "- Inhalt danach:", repr(open(os.path.join(z, "da.txt")).read()))
PYEOF

echo; echo "## B2c --ziel auf den historischen Ordner $D"
bash docs/belege/TB-98/hashes.sh "B2c vorher" | grep "$D/" | sort > "$SP/b2c_vorher.txt"
stat -f '%m %N' $D/* > "$SP/b2c_mtime_vorher.txt"
$PY -W ignore $PH rsi2_crypto --ziel "$D" 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"
bash docs/belege/TB-98/hashes.sh "B2c nachher" | grep "$D/" | sort > "$SP/b2c_nachher.txt"
stat -f '%m %N' $D/* > "$SP/b2c_mtime_nachher.txt"
diff "$SP/b2c_vorher.txt" "$SP/b2c_nachher.txt" >/dev/null && echo "    $(wc -l < "$SP/b2c_vorher.txt" | tr -d ' ') Dateien unter daten/: Hash vorher = nachher" || echo "    FEHLER: Hash veraendert"
diff "$SP/b2c_mtime_vorher.txt" "$SP/b2c_mtime_nachher.txt" >/dev/null && echo "    mtime vorher = nachher, Dateizahl $(ls $D | wc -l | tr -d ' ')" || echo "    FEHLER: mtime veraendert"

echo; echo "## B4a alle_bots.py ohne --ziel"
$PY -W ignore $AB rsi2_crypto 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"
echo; echo "## B4b alle_bots.py --ziel (relativ) auf einen Ordner mit vorhandener Zieldatei"
mkdir -p "$SP/b4b"; : > "$SP/b4b/turtle_soup_crypto_meta.json"
REL=$(python3 -c "import os,sys; print(os.path.relpath(sys.argv[1]))" "$SP/b4b")
$PY -W ignore $AB --ziel "$REL" turtle_soup_crypto 2>&1 | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"; inhalt "$SP/b4b"
echo; echo "## B4c alle_bots.py --ziel auf einen leeren Ordner: Kind laeuft bis Befund 2 (a1), schreibt nichts"
mkdir -p "$SP/b4c"
$PY -W ignore $AB --ziel "$SP/b4c" rsi2_crypto 2>&1 | grep -v '^Hinweis' | zeige "$SP"; echo "    rc=${PIPESTATUS[0]}"; inhalt "$SP/b4c"
echo FERTIG
