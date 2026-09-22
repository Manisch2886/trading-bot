#!/bin/bash
# TB-88 M4 (c) - Was-waere-wenn fuer Punkt 8, OHNE eine Datei im Repo anzufassen.
#
# Wie die Mutationsproben in test_vorregistrierung.py (Teil H, _kopie): der
# Ordner research/vorregistrierung wird in ein Wegwerf-Verzeichnis KOPIERT;
# NUR IN DER KOPIE traegt ergebnisse/benchmark_drawdowns.json den Inhalt von
# benchmark_drawdowns_vt.json.
#
# Warum ein Spiegel mit Symlinks: test_vorregistrierung.py:533 setzt fuer die
# Teil-H-Unterprozesse TB30A_BASE_DIR = zwei Ebenen ueber dem Testordner. Die
# Kopie muss deshalb unter <wurzel>/research/vorregistrierung liegen, und
# <wurzel> muss alles andere des Repos sehen (Kursdaten, Loader,
# research/faltenplan_neun). Alle anderen Eintraege sind Symlinks auf das Repo;
# nur research/vorregistrierung ist eine echte Kopie.
#
# Zwei Faelle: gegenprobe (Kopie unveraendert - muss wie im Repo abbrechen)
# und tausch (benchmark_drawdowns.json := _vt.json, nur in der Kopie).
set -u
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
PY="$REPO/trading-env/bin/python3"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/tb88_m4.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

for fall in gegenprobe tausch; do
    W="$TMP/$fall"
    mkdir -p "$W/research"
    for e in "$REPO"/* "$REPO"/.[!.]*; do
        n=$(basename "$e")
        case "$n" in research|.git) continue ;; esac
        ln -s "$e" "$W/$n"
    done
    for e in "$REPO"/research/*; do
        n=$(basename "$e")
        [ "$n" = vorregistrierung ] && continue
        ln -s "$e" "$W/research/$n"
    done
    K="$W/research/vorregistrierung"
    cp -R "$REPO/research/vorregistrierung" "$K"
    rm -rf "$K/__pycache__"
    if [ "$fall" = tausch ]; then
        cp "$REPO/research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json" \
           "$K/ergebnisse/benchmark_drawdowns.json"
    fi
    echo "=== Fall $fall ($(date -u +%FT%TZ))"
    echo "sha256 benchmark_drawdowns.json in der Kopie: $(shasum -a 256 "$K/ergebnisse/benchmark_drawdowns.json" | cut -d' ' -f1)"
    (cd "$K" && env -u TB30A_BASE_DIR "$PY" -W ignore test_vorregistrierung.py 2>&1)
    echo "rc=$?"
done
