#!/usr/bin/env python3
# TB-118 C1 - Zuordnungsliste: je Inhaltszeile der alten BACKLOG.md (am Commit 8a3f6f6) Zeile, Kennung, Klasse, Grund.
# Die Klasse kommt aus c1_teilen.py (ZUORDNUNG Z); der Grund ist der Regelgrund der Klasse, bei gelesenen Sonderfaellen
# die Notiz unten. Aufruf aus der Repo-Wurzel; schreibt auf stdout.
import importlib.util, re, subprocess
spec = importlib.util.spec_from_file_location("t", "docs/belege/TB-118/c1_teilen.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
alt = subprocess.run(["git", "show", "8a3f6f6:docs/projektfuehrung/BACKLOG.md"], stdout=subprocess.PIPE,
                     check=True).stdout.decode("utf-8").split("\n")
GRUND = {"O": "offen: Aufgabe, Frage oder Entscheidung steht aus (bei Mischzeilen: mindestens ein offener Teil)",
         "E": "Festlegung, Regel, Lehre oder Betreiberentscheid mit Datum; keine offene Handlung",
         "D": "erledigt, beantwortet, abgeloest oder Verweis auf Archiv; Abschnitt 8 vollstaendig",
         "S": "Groesse oder Erwartung nach Register 27.1"}
NOTIZ = {
    143: "F4: 'Wirkung von 60/40 gegen 80/20 mit hoher Wahrscheinlichkeit groesser als die des gesamten Dezember-Laufs' - Erwartung ueber den Lauf",
    167: "K8: Erwartung netto-Sharpe als Spanne (Einschaetzung) - Erwartung nach 27.1",
    170: "T39.2: Sharpe-Schwelle bei N = 653 und Satz ueber den Ausgang - vom Auftrag genannt (Z. 170)",
    190: "W14: Erwartung, wie viele Bots auf Schatten landen - vom Auftrag genannt (Z. 190), Register 27 Tatsachennotiz",
    222: "V5i: Vorhersage zu den heutigen Einstellungen fuer den Ausgang der Neuselektion",
    224: "V5k: Sharpe-Werte (Grenze bei vier Trades, Unterscheidbarkeitsschwelle) - dieselbe Schwelle wie Z. 170",
    440: "P2: Papierpfad-Ergebnis als Summe in Prozentpunkten - Rendite der heutigen Parameter; offen, bleibt offen",
    441: "Regel: Rendite-Kennzahlen aus live_params.py (Code-Kopf) im Wortlaut - Regel selbst ist E, Zeile wegen der Zahlen S",
    510: "K4m: MtM-/ereignisindizierte Drawdowns je Bot und Falte - Kennzahl eines Parametersatzes",
    531: "P4: 'hat bei 8 von 9 Bots geschadet' - Aussage wie viele Saetze eine Bedingung erfuellen; offen, bleibt offen",
    47: "Waechter-Zeile: erledigt, aber 'Offen: fuenf Crontab-Zeilen auf den Wrapper umstellen'",
    392: "Kette 0: TB-30a erledigt, 'Offen: GPG-Tag + Zeitanker' - der signierte Tag steht aus",
    414: "Kette 0,88: TB-56 erledigt, die Drei-Kategorien-Regel zu Registertext 0 nicht (T56b.14)",
    72: "R1: Registertexte 6 und 7 stehen seit TB-41 im Register (16.4, 16.5) - gemessen im Register",
    73: "T39.3: Familienbuchfuehrung steht in 16.8 (c), aber Q3 fuehrt T39.3 weiter als Punkt fuer die Querpruefung - offen",
    378: "K4a: Lehre (E) plus offene Handlung 'beim naechsten Durchgang zusammenfuehren' - O",
    384: "K4g: Rueckblick-Ort und 'Laufreproduktion gegen den Lock' offen (heute Kette 0,99) - O",
    506: "K4i: 'Offen beim Betreiber' (UEBERGABEPROTOKOLL im Lesepfad, Platzhalter oder fester Name) - O",
    509: "K4l: die dort offen benannten Punkte sind erledigt (Vollzug TB-92/TB-94, TB-74 -> TB-80) - D",
    511: "K4n: 'Offen: die Regel eintragen - ARBEITSWEISE 14, DOKUMENTATIONSSTANDARD 10' - O",
    514: "K4q: Folgen fuer den steuernden Chat (Ablage, Erinnerung, N1-N5) - O",
    515: "K4r: 'offen (asof, Ablage, TB-30b)'; asof ist gesetzt (Register 28), TB-30b offen - O",
    454: "K1m: beantwortet durch Register 21 (T56b.1: kein Registertext nennt eine Jahreszahl) - D",
    471: "K2c: A7 steht seit TB-54b in PRUEFPRINZIPIEN.md - D",
    422: "Kette 0,96: AF-F0_BESTANDSAUFNAHME_2026-09-26.md liegt vor - D",
    424: "Kette 0,98: Recherche liegt vor, die Entscheidung D1 daraus nicht - O",
    102: "U1: docs/UMGEBUNGEN.md existiert und CLAUDE.md verweist darauf - D",
    358: "Kopfnotiz Block 2z: der Block ist ueberwiegend Regel/Lehre (E)",
    278: "Notiz zu T56b.3 (E) - folgt ihrer Zeile",
    265: "Kopfnotiz Block 2s (Einarbeitung TB-59) - D",
}
KNR = re.compile(r"^\| (?:\*\*|~~)?([^*~|]+?)(?:\*\*|~~)?\s*(?:\*\([^|]*\)\*)?\s*\|")
print("# TB-118 C1 Zuordnung: Zeile | Kennung | Klasse | Grund. Klassen: O offen -> BACKLOG.md, E -> BACKLOG_ENTSCHEIDUNGEN.md,")
print("# D -> BACKLOG_ERLEDIGT_2026-09.md, S -> BACKLOG_SICHTSCHUTZ.md. K-Nummern werden nach Inhalt eingeordnet, nicht nach")
print("# dem Praefix: der K-Namensraum gehoert zu Abschnitt 4 'Laufend, klein' und mischt offene Punkte, Regeln und Lehren.")
zaehl = {}
for n in sorted(t.Z):
    z = alt[n - 1]
    if not z.strip():
        continue
    m = KNR.match(z)
    kenn = m.group(1).strip() if m else "(Absatz)"
    k = t.Z[n]
    zaehl[k] = zaehl.get(k, 0) + 1
    print("%4d | %-14s | %s | %s" % (n, kenn[:14], k, NOTIZ.get(n, GRUND[k])))
print("# Summe: " + ", ".join("%s %d" % kv for kv in sorted(zaehl.items())))
