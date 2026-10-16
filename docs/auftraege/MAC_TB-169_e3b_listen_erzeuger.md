# TB-169 E-3b: Listen-Erzeuger (Schnitt an der Eingabe, Wachen, Doppellauf weg), Abnahme nach R98 (d), Vollzug TB-166 nach 37.3 (Register 64) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 16.10.2026, 21:31** (Helfer BAU169, per Skript aus Bausteinen, `$HOME/sc/tb169/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `b9a6202`.**

**Sitzungstitel:** `TB-169` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `b9a620273e2d412d0fc6d12d55fbecfd04bd9ac8` (kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-169`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY` (numpy 2.0.2, pandas 2.3.3, Python 3.9 nach `requirements.lock`); Werkzeug `docs/belege/TB-169/tb169_werkzeug.py` (Anhang A), kurz `WZ`. **Belege:** `docs/belege/TB-169/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-169_e3b_listen_erzeuger.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FE ⇒ FF).
**Grundlage:** PLAN_E3 Teil 2b (E-3b), Register R86 (b)–(d), R87 (c), R81 (c), R90 (g), R97 (a), R98 (d) (Register Z. 12228), 37.3; Entwurf der Tatsachennotiz `docs/belege/TB-166/e_notiz.md` (md5 `e28885ae5e10e158860fb457671ce900`); Vorbild Vollzug: TB-168 (Register 63). **Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ E (E-3b und **Abnahme nach R98 (d)**) ⇒ S (Sonde, lesend) ⇒ N (Register 64, **nur nach grüner Abnahme**) ⇒ K (Kopien, Index) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 32 („Opus Trading Bots-16.10.2026 b“), 16.10.2026, 20:25, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-169 frei? E-3b ändert zwei Dateien ausserhalb der Sperrliste (positionen_holen.py, alle_bots.py): Schnitt an der Eingabe, Wachen mit Ausgang 2, der Doppellauf fällt weg. Die neue Probe test_listen_erzeuger.py ist die Abnahme von E-3a nach R98 (d). Danach folgt der Vollzug nach 37.3: Die 20 Hash-Übergänge aus TB-166 (e_notiz.md, Hashes nachgemessen) kommen als Register 64 ins Register, Bauart 60/63. Bedingungen: Der frische Gegenleser findet keinen A-Befund, alle Tests sind grün, die Simulation ist gut. Der Vollzug läuft nur, wenn die Abnahme grün ist. Es werden keine Listen neu erzeugt, es gibt keinen Lauf auf Kursdaten, kein Live und kein Geld. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: bedingt freigeben. Das spart eine Mac-Runde, und der Vollzug hängt maschinell an der grünen Abnahme."="Bedingt freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. `WZ register` übernimmt diese Zeile wörtlich in den Kopfsatz von 64. E-3b ändert keine Datei der Sperrliste (Abschnitt 10 und Abbild tb117 nennen `positionen_holen.py`, `alle_bots.py` nicht; gemessen am Bau). Die Karte trägt den Vollzug nach 37.3 („Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz“), Bauart 60/63 (je eigene Karte für den Vollzug).

R98 (d) (Register Z. 12228): „(d) Abnahme. Die Prüfung nach R90 (g) läuft am Erzeuger: für den Zellen-Erzeuger in der Abnahme nach R46, für den Listen-Erzeuger in der Probe nach R86 (d), je auf dem Test-Snapshot, geprüft an den Ausgaben des Erzeugers, mit der Gegenprobe über die Wache nach R87 (c); sie steht neben der Probe des Schnitts nach R86 (d), jede beisst allein (41.1 A5). Eine Prüfung unmittelbar am Signalpfad ist Handwerk daneben und ersetzt sie nicht.“

## Verboten

Kein Lauf auf Kursdaten; `data/` wird nicht gelesen (die Abnahme rechnet auf einem synthetischen Test-Snapshot im Temp-Ordner). **Keine Neuerzeugung der neun Listen** (`alle_bots.py` und `positionen_holen.py` laufen nicht gegen `data/`; R102 (d) und R92 (c) bleiben offen, sie gelten vor der Neuerzeugung). **Kein neues Abbild.** Nichts unter `strategies/`, `shared/`, `data/`, `config/` ändern; unter `research/` nur die drei Dateien aus Schritt E. Kein Live, kein Broker, kein Geld. Kein `git add -A`, kein `-f`.

## Die Dateien (E-3b, keine auf der Sperrliste)

| Datei | sha256 vorher | sha256 nachher (Bau) |
|---|---|---|
| `research/tb24_haltedauern/alle_bots.py` | `6e9ddce913b555a1…` | `4246b577bfc486e3…` |
| `research/tb24_haltedauern/positionen_holen.py` | `a9e81f02dd69d946…` | `b6d1e2d66eae02a8…` |
| `research/tb24_haltedauern/test_listen_erzeuger.py` | `neu` | `e196884a152796e4…` |

`positionen_holen.py`: Lesesicht an der Eingabe — `read_csv` liefert für den ganzen Lauf nur Zeilen mit `open_time` < Go-Live-Schnitt (`faltenplan_neun.GO_LIVE`, dieselbe Quelle wie `handelbar_ab`; R86 (b), eine Stelle für neun Bots); Wache 1: Zeile ab dem Schnitt im Signalpfad ⇒ 2 (R86 (d)); `hole_trades(es, all_data, handelbar_ab(BOT))` (Schranke aus E-3a; geladenes Symbol ohne Tag ⇒ 2, R81 (c)); Wache 2: Trade mit Ein- oder Ausstieg am Schnitt oder später ⇒ 2 (R86 (d)); Wache 3: Einstieg vor dem Handelbar-Tag ⇒ 2 (R87 (c)); Doppellauf, `simuliere`, Zeilenkennung im `symbol`, `<bot>_positionen.csv` und der Abgleich mit der Exposure-Messung entfallen (R97 (a), A9); Ausgaben `<bot>_alle_trades.csv`, `<bot>_meta.json`, `<bot>_herkunft.json`; Einmal-Schreibsperre und `--ziel` unverändert. `kerzen_je_trade`: an den zwei `searchsorted`-Stellen `pd.Timestamp(…).to_datetime64()` statt `pd.Timestamp(…)` — sonst nichts. `alle_bots.py`: Rückgabe 2 eines Bots ⇒ Ende mit 2. `test_listen_erzeuger.py` (neu): je Bot 13 Prüfungen an den **Ausgaben des Erzeugers** auf Test-Snapshots (A mit, B ohne Zeilen ab dem Schnitt; Bauart R81 (h): Zeitachse je Bot so versetzt, dass A ein Einstiegssignal ab dem Schnitt und eine vor dem Schnitt eröffnete, am Ende von B offene Position enthält) — 0 Snapshot nach R81 (h); 1 Probe A = B (R86 (d)); 2a Schnitt aus ⇒ Wache 1 beisst allein; 2b Schnitt und Wachen aus ⇒ Listen weichen ab, Einstiege ab dem Schnitt; 2c Schnitt und Wache 1 aus ⇒ Wache 2 beisst allein; 3a R90 (g) Tag in einer offenen Position ⇒ kein Einstieg davor, der verdrängte zweite Einstieg erscheint; 3b spätes Symbol gleich mit/ohne Schranke; 4 Gegenprobe Schranke aus ⇒ Wache 3 beisst (R87 (c)); 5a eigenes Symbol `SPAET`, das die Schranke nur mit Zeilen ab dem Schnitt erreicht (R81 (h)) ⇒ Tag None, nicht in der Liste; 5b dasselbe mit Schnitt und Wache 1 aus ⇒ R81 (c) beisst, ohne Eingriff in den Tag; 6 A9; 7 offene Position am Ende von B nach der Ausstiegskonvention des Signalpfads, keine leere Ausstiegszeit (R86 (c), R83 (c)); 8 nur Dateien des Test-Snapshots gelesen (auch BTC-Regimefilter). Soll **117 von 117**.

**Tatsachennotiz nach R90 (g)** (`t3_supertrend`: Fall kann nicht entstehen; `elliott_wave`, `elliott_wave_stocks`: am Erzeuger nicht herstellbar, Teilmessung; im Test als Prüfung 3a mit diesem Wortlaut): `t3_supertrend` — Einstieg nur am Kreuzen nach oben (`backtest_trend.py` Z. 111–112), die Position endet am Kreuzen nach unten, am Trend-Flip des Supertrend (Z. 123) oder am Stop: solange sie offen ist, entsteht kein zweites Einstiegssignal, das verdrängt werden könnte. `elliott_wave`, `elliott_wave_stocks` — **Teilmessung:** die Trade-Schleife führt keinen Positionszustand (`backtest_elliott.py` Z. 113 bzw. Z. 122: je Welle ein Trade); verdrängt wird nur in der Wellenauswahl (`traded`, `elliott_wave_counter.py` Z. 363), die Schranke `min_entry_idx` steht davor (Z. 361; `multi_symbol_optimise.py` bei `elliott_wave` Z. 97–98 und 110–112, bei `elliott_wave_stocks` Z. 131–132 und 144–146). Dass eine gesperrte Welle keinen Zustand hinterlässt und danach einsteigt, ist am Signalpfad belegt (TB-166, `shared/test_schranke_signalpfad.py` Prüfung 5 mit Mutation, `docs/belege/TB-166/e_test_schranke.txt`); am Erzeuger ist der Fall im Test-Snapshot nicht herstellbar (am Bau gesucht: kein Paar alter Einstiege eines Symbols innerhalb `SIGNAL_FRESHNESS_BARS`, 48 bzw. 5, über einen Tageswechsel). Geprüft wird dort: kein Einstieg vor dem Tag, alle alten Trades ab dem Tag bleiben.

**Warum `kerzen_je_trade` geändert wird (am Bau gemessen):** unverändert wirft die Funktion unter den Fassungen aus `requirements.lock` (numpy 2.0.2, pandas 2.3.3) `TypeError: '<' not supported between instances of 'int' and 'Timestamp'` — `ndarray[datetime64[ns]].searchsorted(pd.Timestamp)`; gemessen am Gerät mit echten Zeilen des Snapshots `63e4b6c8…` und echten Trades aus `daten/` unter Python 3.9.25 und 3.10.12 (numpy 2.0.2, pandas 2.3.3) und Python 3.9.25 mit numpy 1.26.4; mit pandas 3.0.6 läuft sie. TB-24 lief unter pandas 3.0.5 (`research/tb24_haltedauern/BERICHT.md` Z. 466); TB-98 brach in allen 18 Läufen vorher ab (`docs/belege/TB-98/a1_neun_lauf.txt`). Mit `.to_datetime64()` ergab die Kerzen-Probe (Anhang E) am Gerät für alle 25 861 Trades der neun `daten/<bot>_alle_trades.csv` dieselben Kerzenzahlen wie die Spalte `kerzen` (0 abweichend), und der Test 117 von 117 (Python 3.10.12, numpy 2.0.2, pandas 2.3.3). In `trading-env` (Python 3.9.6) wird beides in E zum ersten Mal am Mac gemessen.

## Lage nach dem Auslegen

Beim Start genau 4 Einträge (Soll in 0a).

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `b9a620273e2d412d0fc6d12d55fbecfd04bd9ac8`, genau diese 4 Einträge, Karte gefüllt; sonst **ABBRUCH**, vor ⟨S0⟩ und vor jedem Push):

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md
```

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb169_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', ' M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md', ' M docs/projektfuehrung/UEBERGABE.md', '?? docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "b9a620273e2d412d0fc6d12d55fbecfd04bd9ac8": f.append("HEAD " + g("rev-parse", "HEAD").strip())
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Soll: letzte Zeile `0a gut (4 Eintraege)`. Anhänge holen (genau dieser Befehl):

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Soll genau: `tb169_werkzeug.py 42524d3177367318cc320b5267d5dc5462c82623a58283ee6606ddff5f101245`; `e3b_positionen_holen.py b6d1e2d66eae02a8a546cab15649a4100e3c1b2df0a9a668140f23de3a8573db`; `e3b_alle_bots.py 4246b577bfc486e3f872ea5132412fe5e23092e23b737182d765373118666964`; `e3b_test_listen_erzeuger.py e196884a152796e4a9ab6e715de70933ebf7614ecf4f38d763eed24d46cda1bf`; `kerzen_probe.py b1cb10f799395f924db957f36bde1cb1c845e85b0512025abbb3c74a9b1711de`; `Dateien 5`; sonst **ABBRUCH**. Dann genau diese `git add` (alle 0a-Pfade mit Namen), Commit `TB-169 Schritt 0: Stand des steuernden Chats vor TB-169`, pushen ⇒ **⟨S0⟩** (7 Zeichen):

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md
```

Danach `git status --porcelain` — Soll: keine Ausgabe. Erst dann:

```
mkdir -p docs/belege/TB-169/
cp "$TMPDIR/tb169_0a.txt" docs/belege/TB-169/0a_status.txt
cp "$TMPDIR/tb169_werkzeug.py" docs/belege/TB-169/tb169_werkzeug.py
cp "$TMPDIR/e3b_positionen_holen.py" docs/belege/TB-169/e3b_positionen_holen.py
cp "$TMPDIR/e3b_alle_bots.py" docs/belege/TB-169/e3b_alle_bots.py
cp "$TMPDIR/e3b_test_listen_erzeuger.py" docs/belege/TB-169/e3b_test_listen_erzeuger.py
cp "$TMPDIR/kerzen_probe.py" docs/belege/TB-169/kerzen_probe.py
```

## Schritt V — Voraussetzungen

```
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py voraussetzung > docs/belege/TB-169/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/v_voraussetzung.txt
```

**Abbruch in V:** dann liegt im Arbeitsbaum nur der unverfolgte Ordner `BEL` (Belege aus Schritt 0 und `v_voraussetzung.txt`); kein Code ist geändert. `printf '%s\n' "V: <letzte NEIN-Zeile>" > docs/belege/TB-169/abbruch.txt`, dann `git add` mit Namen für `abbruch.txt`, `0a_status.txt`, die fünf Anhänge und `v_voraussetzung.txt`, Commit `TB-169 Abbruch: V`, pushen, `git status --porcelain` leer; melden. Soll: letzte Zeile `rc 0` (Register endet mit 63; vorher-Hashes der zwei Dateien, Test noch nicht da; Anhänge = nachher; `e_notiz.md` md5 und Commit, 20 Zeilen, jede Datei heute = nachher und zuletzt in `15f28e4`; Abbild und Sonde; Karten TB-166 und TB-169; Index 0–63; BACKLOG Rang 1 Stand TB-166; Journal FE ⇒ FF). Sonst **ABBRUCH**. Kein Commit in V; der Beleg geht mit E.

## Schritt E — E-3b und Abnahme nach R98 (d)

```
trading-env/bin/python3 -B -W ignore research/tb24_haltedauern/test_haltedauer_kern.py > docs/belege/TB-169/e_alt_vorher.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_alt_vorher.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py e3b --probe > docs/belege/TB-169/e_e3b_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_e3b_probe.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py e3b > docs/belege/TB-169/e_e3b.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_e3b.txt
trading-env/bin/python3 -B -W ignore research/tb24_haltedauern/test_haltedauer_kern.py > docs/belege/TB-169/e_alt_nachher.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_alt_nachher.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py altvergleich docs/belege/TB-169/e_alt_vorher.txt docs/belege/TB-169/e_alt_nachher.txt > docs/belege/TB-169/e_alt_vergleich.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_alt_vergleich.txt
trading-env/bin/python3 -B docs/belege/TB-169/kerzen_probe.py snapshots/63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2 > docs/belege/TB-169/e_kerzen.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_kerzen.txt
trading-env/bin/python3 -B -W ignore research/tb24_haltedauern/test_listen_erzeuger.py > docs/belege/TB-169/e_abnahme.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_abnahme.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py abnahme docs/belege/TB-169/e_abnahme.txt > docs/belege/TB-169/e_abnahme_pruefung.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/e_abnahme_pruefung.txt
```

Soll: jede dieser Belegdateien endet mit `rc 0` — ausgenommen `e_alt_vorher.txt` und `e_alt_nachher.txt`: der alte Test `test_haltedauer_kern.py` ist schon am HEAD in Prüfung 13 rot (AST-Prüfung der Schreibziele nennt `positionen_holen.py`, am Bau alt wie neu gemessen); `e_alt_vergleich.txt` (`WZ altvergleich`) verlangt vorher und nachher denselben Rückgabewert und dieselben Fehlzeilen. `e_kerzen.txt` endet mit `Ergebnis: 25861 Trades verglichen, 0 abweichend oder ohne Kursreihe` (je Bot `ja`, nur bei voller Abdeckung: jeder Trade der Liste hat eine Kursreihe im Snapshot); `e_abnahme.txt` mit `Ergebnis: 117 von 117 bestanden` und `rc 0`; `e_abnahme_pruefung.txt` (9 × 13 ja, keine NEIN-Zeile) `rc 0`. **Endet eine nicht mit `rc 0`: ABBRUCH ohne E-Commit** — kein `git add` der Liste unten; S, N, K, A laufen nicht — **der Vollzug nach 37.3 (Register 64) läuft nur nach grüner Abnahme.** Abbruchweg (Vorbild TB-167): zuerst die letzten 30 Zeilen des roten Belegs melden, dann genau diese Befehle (`<Grund>` = Name des roten Belegs und seine letzte Zeile):

```
printf '%s\n' "E: <Grund>" > docs/belege/TB-169/abbruch.txt
git show HEAD:research/tb24_haltedauern/positionen_holen.py > research/tb24_haltedauern/positionen_holen.py
git show HEAD:research/tb24_haltedauern/alle_bots.py > research/tb24_haltedauern/alle_bots.py
trading-env/bin/python3 -B -c "import os; q, z = 'research/tb24_haltedauern/test_listen_erzeuger.py', 'docs/belege/TB-169/abbruch_test_listen_erzeuger.py'; e = os.path.exists(q); e and os.replace(q, z); open('docs/belege/TB-169/abbruch.txt', 'a', encoding='utf-8').write('Arbeitsbaum: positionen_holen.py und alle_bots.py auf HEAD zurückgesetzt, ' + ('Test nach BEL verschoben' if e else 'Test nicht vorhanden') + ' (Abbruch in E).\n')"
git add docs/belege/TB-169/abbruch.txt
git add docs/belege/TB-169/abbruch_test_listen_erzeuger.py
git add docs/belege/TB-169/0a_status.txt
git add docs/belege/TB-169/tb169_werkzeug.py
git add docs/belege/TB-169/e3b_positionen_holen.py
git add docs/belege/TB-169/e3b_alle_bots.py
git add docs/belege/TB-169/e3b_test_listen_erzeuger.py
git add docs/belege/TB-169/kerzen_probe.py
git add docs/belege/TB-169/v_voraussetzung.txt
git add docs/belege/TB-169/e_alt_vorher.txt
git add docs/belege/TB-169/e_e3b_probe.txt
git add docs/belege/TB-169/e_e3b.txt
git add docs/belege/TB-169/e_alt_nachher.txt
git add docs/belege/TB-169/e_alt_vergleich.txt
git add docs/belege/TB-169/e_kerzen.txt
git add docs/belege/TB-169/e_abnahme.txt
git add docs/belege/TB-169/e_abnahme_pruefung.txt
git commit -q -m "TB-169 Abbruch: E" && git push -q
git status --porcelain
```

Endet E schon bei `e_e3b_probe.txt` (vor `WZ e3b`), gibt es den Test im Arbeitsbaum noch nicht: der Python-Aufruf prüft das selbst, überspringt dann `os.replace` und schreibt als zweite Zeile von `abbruch.txt` „Test nicht vorhanden“ statt „Test nach BEL verschoben“. Ein `git add` eines Belegs, der vor dem roten Schritt nicht entstanden ist, meldet `pathspec … did not match` und wird übergangen. Soll: `git status --porcelain` ohne Ausgabe (die zwei Dateien wieder auf HEAD; der Test liegt als `abbruch_test_listen_erzeuger.py` unter `BEL` im Abbruch-Commit); scheitert der Push: melden, nicht wiederholen. Sonst (alle grün) genau diese `git add`, Commit `TB-169 E: E-3b Listen-Erzeuger und Abnahme nach R98 (d)`, pushen ⇒ **⟨E⟩**:

```
git add research/tb24_haltedauern/positionen_holen.py
git add research/tb24_haltedauern/alle_bots.py
git add research/tb24_haltedauern/test_listen_erzeuger.py
git add docs/belege/TB-169/0a_status.txt
git add docs/belege/TB-169/tb169_werkzeug.py
git add docs/belege/TB-169/e3b_positionen_holen.py
git add docs/belege/TB-169/e3b_alle_bots.py
git add docs/belege/TB-169/e3b_test_listen_erzeuger.py
git add docs/belege/TB-169/kerzen_probe.py
git add docs/belege/TB-169/v_voraussetzung.txt
git add docs/belege/TB-169/e_alt_vorher.txt
git add docs/belege/TB-169/e_e3b_probe.txt
git add docs/belege/TB-169/e_e3b.txt
git add docs/belege/TB-169/e_alt_nachher.txt
git add docs/belege/TB-169/e_alt_vergleich.txt
git add docs/belege/TB-169/e_kerzen.txt
git add docs/belege/TB-169/e_abnahme.txt
git add docs/belege/TB-169/e_abnahme_pruefung.txt
```

## Schritt S — Sperrlisten-Sonde, lesend (Aufruf wie TB-168 Schritt S)

```
git status --porcelain > "$TMPDIR/tb169_s_vor.txt"
trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json > "$TMPDIR/tb169_sonde.txt" 2>&1; echo "rc $?" >> "$TMPDIR/tb169_sonde.txt"
git status --porcelain > "$TMPDIR/tb169_s_nach.txt"
cp "$TMPDIR/tb169_sonde.txt" docs/belege/TB-169/s_sonde.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py sonde docs/belege/TB-169/s_sonde.txt "$TMPDIR/tb169_s_vor.txt" "$TMPDIR/tb169_s_nach.txt" > docs/belege/TB-169/s_auswahl.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/s_auswahl.txt
```

Soll: `s_auswahl.txt` endet mit `rc 0` und nennt `Fassung: nicht prüfbar` oder `Fassung: Befund 1 (beauftragt)`. Sonst **ABBRUCH**. Kein Commit in S; die Belege gehen mit N.

## Schritt N — Register 64 (Vollzug TB-166 nach 37.3)

Datum `⟨DATUM⟩` = `TZ=Europe/Berlin date +%d.%m.%Y`. Genau diese zwei Befehle nacheinander (⟨S0⟩, ⟨E⟩, ⟨DATUM⟩ einsetzen):

```
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ ⟨E⟩ docs/belege/TB-169/s_sonde.txt docs/belege/TB-169/e_abnahme.txt --probe > docs/belege/TB-169/n_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/n_probe.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py register ⟨DATUM⟩ ⟨S0⟩ ⟨E⟩ docs/belege/TB-169/s_sonde.txt docs/belege/TB-169/e_abnahme.txt > docs/belege/TB-169/n_eintrag.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/n_eintrag.txt
```

Soll je `rc 0`; endet die Probe nicht mit `rc 0`: den zweiten nicht ausführen, **ABBRUCH**. `WZ register` prüft selbst, dass `e_abnahme.txt` 117 von 117 zeigt und alle V- und E-Belege mit `rc 0` enden und keine NEIN-Zeile tragen, und hängt an: Titel `## 64. Vollzug TB-166 (Tatsachennotiz nach 37.3; E-3a Schranke je Symbol) mit Abnahme nach R98 (d) (TB-169)`, Kopfsatz mit der Karte oben wörtlich, 64.1 mit `e_notiz.md` **zeichengleich** (20 Hash-Übergänge, Commit `15f28e4`), die Karte TB-166 wörtlich, der Satz zur Abnahme und der Satz zur Sonde. Append-only. Dann genau diese `git add`, Commit `TB-169 N: Register 64 (Vollzug TB-166 nach 37.3)`, pushen ⇒ **⟨N⟩**:

```
git add docs/VORREGISTRIERUNG_neuselektion.md
git add docs/belege/TB-169/s_sonde.txt
git add docs/belege/TB-169/s_auswahl.txt
git add docs/belege/TB-169/n_probe.txt
git add docs/belege/TB-169/n_eintrag.txt
```

## Schritt K — Kopien und Index (wie TB-168 Schritt K, ohne Handfelder)

```
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py > docs/belege/TB-169/k_registerkopie.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/k_registerkopie.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --abschnitte > docs/belege/TB-169/k_abschnitte.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/k_abschnitte.txt
trading-env/bin/python3 -B docs/werkzeuge/registerkopie.py --pruefen > docs/belege/TB-169/k_pruefen.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/k_pruefen.txt
trading-env/bin/python3 -B docs/belege/TB-154/c2_index_zeilen.py ⟨S0⟩ ⟨N⟩ > docs/belege/TB-169/k_index_zeilen.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/k_index_zeilen.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py index ⟨S0⟩ ⟨DATUM⟩ > docs/belege/TB-169/k_index.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/k_index.txt
```

Soll: jede Belegdatei endet mit `rc 0`. Dann genau diese `git add`, Commit `TB-169 K: Registerkopie, Index`, pushen; danach `git status --porcelain` leer, sonst melden:

```
git add docs/projektfuehrung/REGISTER_INDEX.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil1.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil2.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil3.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil4.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil5.md
git add docs/projektfuehrung/REGISTER_KOPIE_teil6.md
git add docs/projektfuehrung/register_kopie
git add docs/belege/TB-169/k_registerkopie.txt
git add docs/belege/TB-169/k_abschnitte.txt
git add docs/belege/TB-169/k_pruefen.txt
git add docs/belege/TB-169/k_index_zeilen.txt
git add docs/belege/TB-169/k_index.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ kennung` (Soll „Kennung FF …“). Block nach `docs/belege/TB-169/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-169: …`, Quellenzeile, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`; kein `---`). Ergebnis `docs/ERGEBNIS_TB-169_e3b_listen_erzeuger.md` mit: Kurz; V wörtlich; E (letzte Zeilen je Beleg, 9 × 8); Sonde-Fassung; Register 64 (Zeile, ⟨N⟩); Offen (vor der Neuerzeugung der Listen: R102 (d), R92 (c); `auswertung.py` Z. 71/325 und `embargo_neun.py` Z. 35 lesen `<bot>_positionen.csv`/`trades_ausgefuehrt`, die mit E-3b entfallen; das Abbild tb117 führt die neun `daten/<bot>_alle_trades.csv`; neues Abbild vor dem Tag); Abweichungen; In einfacher Sprache. Dann:

```
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py kennung > docs/belege/TB-169/a_kennung.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe > docs/belege/TB-169/a_backlog_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/a_backlog_probe.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ > docs/belege/TB-169/a_backlog.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/a_backlog.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py journal docs/belege/TB-169/a_block.md --probe > docs/belege/TB-169/a_journal_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/a_journal_probe.txt
trading-env/bin/python3 -B docs/belege/TB-169/tb169_werkzeug.py journal docs/belege/TB-169/a_block.md > docs/belege/TB-169/a_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-169/a_journal.txt
```

`WZ backlog` schreibt in Rang 1 zusätzlich, fällig vor der Neuerzeugung der Listen: `auswertung.py` (Z. 71, 325) und `embargo_neun.py` (Z. 35) lesen `<bot>_positionen.csv` bzw. `trades_ausgefuehrt`, die mit E-3b entfallen (C1); das Abbild tb117 führt die neun `daten/<bot>_alle_trades.csv`, die Neuerzeugung trifft das Abbild (C3); R102 (d), R92 (c). Soll je `rc 0`. Genau diese `git add`, Commit `TB-169 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen:

```
git add docs/ERGEBNIS_TB-169_e3b_listen_erzeuger.md
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/belege/TB-169/a_kennung.txt
git add docs/belege/TB-169/a_backlog_probe.txt
git add docs/belege/TB-169/a_backlog.txt
git add docs/belege/TB-169/a_block.md
git add docs/belege/TB-169/a_journal_probe.txt
git add docs/belege/TB-169/a_journal.txt
```

**F.** `git status --porcelain > docs/belege/TB-169/f_porcelain.txt` und `git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-169/f_numstat.txt`; `git add` beider, Commit `TB-169 F: porcelain und numstat`, pushen. Soll: `f_porcelain.txt` leer; unter `research/` im numstat genau die drei Dateien aus E.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V nicht `rc 0`; ein Beleg aus E nicht `rc 0` (dann Abbruchweg E, **kein E-Commit**, kein Vollzug); S ohne Fassung; N, K, A nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. Vor ⟨S0⟩ nichts schreiben.

## In einfacher Sprache

Das Programm, das die Handelslisten der neun Bots erzeugt, liest künftig nur noch Kurse vor dem Go-Live-Tag und hält an, sobald etwas Späteres oder ein zu früher Einstieg durchrutscht. Ein Test auf erfundenen Kursen prüft das an den fertigen Listen. Erst wenn dieser Test grün ist, werden die 20 Hash-Wechsel aus TB-166 ins Register eingetragen. Die echten Listen werden hier noch nicht neu erzeugt.

## Anhänge

### Anhang A — `tb169_werkzeug.py` (sha256 `42524d3177367318cc320b5267d5dc5462c82623a58283ee6606ddff5f101245`)

<!-- DATEI tb169_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-169 Werkzeug (Anhang A): Voraussetzungen, E-3b (2 Dateien + Test), Abnahme R98 (d), Sonde-Auswahl, Register 64 (Vollzug TB-166 nach 37.3), Index, BACKLOG, Journal.
Reine Standardbibliothek, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | e3b [--probe] | abnahme <BELEG> | altvergleich <VOR> <NACH> | sonde <BELEG> <VOR> <NACH> | register <DATUM> <S0> <E> <SONDE> <ABNAHME> [--probe]
  index <S0> <DATUM> [--probe] | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, subprocess, sys
REG, IDX, JO, BL = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/REGISTER_INDEX.md", "docs/projektfuehrung/JOURNAL.md", "docs/projektfuehrung/BACKLOG.md"
BEL, AUF = "docs/belege/TB-169/", "docs/auftraege/MAC_TB-169_e3b_listen_erzeuger.md"
E3B = {"research/tb24_haltedauern/alle_bots.py": ["6e9ddce913b555a1598514225c1f24d31bb5ddcdd1444e3bac2bcf2a393ae525", "4246b577bfc486e3f872ea5132412fe5e23092e23b737182d765373118666964"], "research/tb24_haltedauern/positionen_holen.py": ["a9e81f02dd69d946ff3724fa741d179155a13449194d404828eb1831d6333961", "b6d1e2d66eae02a8a546cab15649a4100e3c1b2df0a9a668140f23de3a8573db"], "research/tb24_haltedauern/test_listen_erzeuger.py": [None, "e196884a152796e4a9ab6e715de70933ebf7614ecf4f38d763eed24d46cda1bf"]}
NOTIZ, NOTIZ_MD5, NOTIZ_COMMIT = "docs/belege/TB-166/e_notiz.md", "e28885ae5e10e158860fb457671ce900", "4a51876"
M166, M166_MD5, M166_COMMIT = "docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md", "57d05b949318d95e5ef28a5692ef1241", "57a1062"
E3A_COMMIT, N_E3A = "15f28e4", 20
AB, AB_SHA, SO, SO_SHA = "research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json", "46f0ad5d1d83a253baa5523f5657881e0d825cebd734f24a42ef5d4fa74f281f", "shared/sperrlistensonde.py", "98c02e0e9b42831d88e0cd9cbdc39d64c458691fdbf1e650aa4e32c933cc0d71"
SONDE_BEFEHL = "trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild " + AB
TITEL63, TITEL631 = "## 63. Vollzug TB-167 (Tatsachennotiz nach 37.3; Abhilfe G6 elliott_wave_stocks) (TB-168)", "### 63.1 Vollzug TB-167 (Tatsachennotiz nach 37.3)"
TITEL64 = "## 64. Vollzug TB-166 (Tatsachennotiz nach 37.3; E-3a Schranke je Symbol) mit Abnahme nach R98 (d) (TB-169)"
S373, Z373 = "Ein Befund 1 der Sperrlisten-Sonde", 7025
RANG1, RANG1E = "| **1** | **TB-30b Mass-Reparatur**", "; Abnahme nach R98 (d) mit E-3b, Tatsachennotiz 37.3 als Entwurf im Ergebnis |"
N_JE_BOT, N_ALLE = 13, 117
E_BELEGE = ["v_voraussetzung.txt", "e_alt_vergleich.txt", "e_e3b_probe.txt", "e_e3b.txt", "e_kerzen.txt", "e_abnahme.txt", "e_abnahme_pruefung.txt"]
BOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout", "t3_supertrend", "elliott_wave", "elliott_wave_stocks"]
FASSUNG = {"2": "nicht prüfbar", "1": "Befund 1 (beauftragt)"}
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def nein(): return any(l.startswith("NEIN") for l in OUT)
def lies(f): return open(f, encoding="utf-8").read()
def schreibe(f, t): open(f, "w", encoding="utf-8", newline="").write(t)
def git(*a): return subprocess.run(["git", "--no-optional-locks"] + list(a), capture_output=True, text=True).stdout
def md5(t): return hashlib.md5(t.encode("utf-8")).hexdigest()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def ende(rc=None):
    print("\n".join(OUT)); n = sum(l.startswith("NEIN") for l in OUT); print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); sys.exit(rc if rc is not None else (1 if n else 0))
def notiz():
    t = lies(NOTIZ); z = t.split("\n"); rows = [l for l in z if l.startswith("| `")]
    return t, z, [(r.split(" | ")[0][3:-1], r.split(" | ")[2].strip("`"), r.split(" | ")[3].strip("`"), r.split(" | ")[4].strip("`")) for r in rows]
def karte(datei, titel):
    if not os.path.exists(datei): return None, None
    z = lies(datei).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(titel)]
    if len(a) != 1: return None, None
    b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## ")); k = [(i, l) for i, l in enumerate(z[a[0] + 1:b], a[0] + 2) if l.startswith("> ")]
    if len(k) != 1 or ("⟨⟨" + "FREIGABE") in k[0][1]: return None, None
    return k[0][1][2:].strip(), k[0][0]
def kennungen(): return re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M)
def naechste(h): return h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"
def voraussetzung():
    reg = lies(REG); z = reg.split("\n")
    p(sum(l == TITEL63 for l in z) == 1 and not re.search(r"^## 64\. ", reg, re.M), "Register: 63 genau einmal, 64 noch nicht")
    p(z[-1] == "" and z[-2] != "", "Register endet mit genau einer Leerzeile")
    t631 = [i + 1 for i, l in enumerate(z) if l == TITEL631]; p(len(t631) == 1, "Vorbild 63.1 genau einmal, Z. %s" % t631)
    t373 = [i + 1 for i, l in enumerate(z) if S373 in l.replace("**", "")]; p(t373[:1] == [Z373], "37.3 zuerst Z. %d" % Z373)
    for f, (vor, nach) in sorted(E3B.items()):
        p((vor is None and not os.path.exists(f)) or (vor is not None and os.path.exists(f) and sha(f) == vor), "vorher %s: %s" % (f, (vor or "fehlt")[:16]))
        p(os.path.exists(BEL + "e3b_" + os.path.basename(f)) and sha(BEL + "e3b_" + os.path.basename(f)) == nach, "Anhang %se3b_%s = nachher %s…" % (BEL, os.path.basename(f), nach[:16]))
    t, nz, rows = notiz(); p(md5(t) == NOTIZ_MD5 and git("log", "--format=%h", "-1", "--", NOTIZ).strip()[:7] == NOTIZ_COMMIT, "e_notiz.md md5 %s, Commit %s" % (NOTIZ_MD5, NOTIZ_COMMIT))
    p(len(rows) == N_E3A and len({r[0] for r in rows}) == N_E3A, "e_notiz.md: %d Zeilen, %d Dateien" % (len(rows), len({r[0] for r in rows})))
    for f, vor, nach, c in rows:
        p(c == E3A_COMMIT and os.path.exists(f) and sha(f) == nach and git("log", "--format=%h", "-1", "--", f).strip()[:7] == E3A_COMMIT, "heute = nachher, zuletzt in %s: %s" % (E3A_COMMIT, f))
    ab = lies(AB); p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild %s… und Sonde %s…" % (AB_SHA[:16], SO_SHA[:16]))
    p(not any(r[0] in ab for r in rows), "Abbild fuehrt keine der %d Dateien" % N_E3A)
    k, kz = karte(M166, "## Freigabe"); m = lies(M166); p(k is not None and md5(m) == M166_MD5 and git("log", "--format=%h", "-1", "--", M166).strip()[:7] == M166_COMMIT, "Karte TB-166: Z. %s, md5 %s, Commit %s" % (kz, M166_MD5, M166_COMMIT))
    k9, _ = karte(AUF, "## Freigabe"); p(k9 is not None, "Karte TB-169 gefuellt")
    ix = lies(IDX).split("\n")
    p(sum("Abschnitte 0–63" in l for l in ix if l.startswith("**Stand:** Register")) == 1 and sum(l.startswith("| 63 Vollzug TB-167 |") for l in ix) == 1 and sum(l.startswith("Zuletzt nachgezogen in TB-168 (") for l in ix) == 1, "Index: Kopf 0–63, Zeile 63, Pflegezeile TB-168")
    bl = lies(BL).split("\n"); p(sum(l.startswith(RANG1) and l.endswith(RANG1E) for l in bl) == 1, "BACKLOG Rang 1 (Stand TB-166) genau einmal")
    k = kennungen(); p(max(k) == "FE" and "FF" not in k, "Journal hoechste FE, naechste FF frei")
    ende()
def e3b(probe):
    for f, (vor, nach) in sorted(E3B.items()):
        q = BEL + "e3b_" + os.path.basename(f)
        p((vor is None and not os.path.exists(f)) or (vor is not None and sha(f) == vor), "vorher " + f); p(sha(q) == nach, "Quelle %s = nachher" % q)
    if probe or nein(): ende()
    for f in sorted(E3B): schreibe(f, lies(BEL + "e3b_" + os.path.basename(f)))
    for f, (vor, nach) in sorted(E3B.items()): p(sha(f) == nach, "nachher %s %s" % (f, nach))
    ende()
def abnahme(beleg):
    z = lies(beleg).rstrip("\n").split("\n")
    for b in BOTS: p(sum(l.startswith("ja    %s: " % b) for l in z) == N_JE_BOT, "%s: %d Pruefungen ja" % (b, N_JE_BOT))
    p(not any(l.startswith("NEIN") for l in z), "keine NEIN-Zeile"); p(z[-2:] == ["Ergebnis: %d von %d bestanden" % (N_ALLE, N_ALLE), "rc 0"], "Ergebnis %d von %d, rc 0" % (N_ALLE, N_ALLE))
    ende()
def altvergleich(vor, nach):
    """Alter Test test_haltedauer_kern.py vor und nach E-3b: dieselben Fehlzeilen, derselbe Rueckgabewert (Pruefung 13 ist schon am HEAD rot)."""
    a, b = lies(vor).rstrip("\n").split("\n"), lies(nach).rstrip("\n").split("\n")
    fa, fb = sorted(l for l in a if l.startswith("  - ")), sorted(l for l in b if l.startswith("  - "))
    p(a[-1] == b[-1] and a[-1] in ("rc 0", "rc 1"), "Rueckgabewert vorher %s, nachher %s" % (a[-1], b[-1]))
    p(fa == fb, "Fehlzeilen vorher %d = nachher %d%s" % (len(fa), len(fb), (": " + fa[0][:120]) if fa else ""))
    ende()
def belege():
    for f in E_BELEGE:
        z = lies(BEL + f).rstrip("\n").split("\n") if os.path.exists(BEL + f) else ["fehlt"]
        p(z[-1] == "rc 0" and not any(l.startswith("NEIN") for l in z), "Beleg %s: letzte Zeile %s, NEIN-Zeilen %d" % (f, z[-1], sum(l.startswith("NEIN") for l in z)))
def fassung(beleg):
    z = lies(beleg).rstrip("\n").split("\n"); m = [re.match(r"^  Punkt 11  \[(\d) ", l) for l in z]; m = [x.group(1) for x in m if x]
    rw = [l for l in z if l.startswith("RUECKGABEWERT ")]; rc = z[-1] if z else ""
    if len(m) != 1 or len(rw) != 1: return None, m, rw, rc
    if m[0] == "2" and rc == "rc 2" and rw[0].startswith("RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [") and re.search(r"[\[ ]11[,\]]", rw[0]): return "2", m, rw, rc
    if m[0] == "1" and rc == "rc 1" and rw[0] == "RUECKGABEWERT 1 BEFUND - BEFUND in Punkt(en) [11]": return "1", m, rw, rc
    return None, m, rw, rc
def satz(f, s0):
    kopf = "**Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-169 am Stand `%s`; Aufruf wie TB-168 Schritt S: `%s`, Abbild `%s…`; Beleg `%ss_sonde.txt`): " % (s0, SONDE_BEFEHL, AB_SHA[:8], BEL)
    if f == "2": return kopf + "Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keine der 20 Dateien — wie bei 60.1 und 63.1. Der Übergang steht deshalb nur hier und in den Commits."
    return kopf + "Punkt 11 „Befund 1 (beauftragt)“ (`1`). Vor dem Tag zulässig nach 37.3, weil beauftragt (Freigabe: Karten unten); geschlossen wird er durch ein neues Abbild unter neuem Namen (37.3), das TB-169 nicht zieht."
def sonde(beleg, vor, nach):
    p(lies(vor) == lies(nach), "git status --porcelain vor und nach der Sonde gleich"); p(sha(AB) == AB_SHA and sha(SO) == SO_SHA, "sha256 Abbild und Sonde")
    f, m, rw, rc = fassung(beleg); p(f is not None, "Punkt 11 im Beleg: %s · %s · %s" % (m, rw[0][:160] if rw else "kein RUECKGABEWERT", rc))
    if f: print("Fassung: %s" % FASSUNG[f])
    ende()
def register(datum, s0, ec, sb, ab, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[0-9a-f]{7}", s0) or not re.fullmatch(r"[0-9a-f]{7}", ec): sys.exit(2)
    f = fassung(sb)[0]; p(f is not None, "Fassung Sonde: %s" % FASSUNG.get(f, "keine"))
    za = lies(ab).rstrip("\n").split("\n"); p(za[-2:] == ["Ergebnis: %d von %d bestanden" % (N_ALLE, N_ALLE), "rc 0"] and not any(l.startswith("NEIN") for l in za), "Abnahme-Beleg %d von %d, rc 0" % (N_ALLE, N_ALLE))
    belege()   # B5: alle V- und E-Belege rc 0, keine NEIN-Zeile
    t, nz, rows = notiz(); p(md5(t) == NOTIZ_MD5 and len(rows) == N_E3A, "Quelle e_notiz.md md5 %s, %d Zeilen" % (NOTIZ_MD5, N_E3A))
    for fl, vor, nach, c in rows: p(sha(fl) == nach, "heute = nachher: " + fl)
    k9, _ = karte(AUF, "## Freigabe"); p(k9 is not None, "Karte TB-169 gefuellt"); k6, kz = karte(M166, "## Freigabe"); p(k6 is not None and md5(lies(M166)) == M166_MD5, "Karte TB-166 Z. %s" % kz)
    z = lies(REG).split("\n"); p(not any(l.startswith("## 64. ") for l in z) and z[-1] == "" and z[-2] != "", "64 noch nicht; Register endet mit einer Leerzeile")
    t631 = [i + 1 for i, l in enumerate(z) if l == TITEL631]
    if nein(): ende()
    kopf = ("Reines Eintragen, Bauart 63.1 (Register Z. %d ff.); Karte des Betreibers (Auftrag TB-169, Abschnitt Freigabe, wörtlich): „%s“ Eingetragen am %s mit TB-169 (Stand `%s`). "
            "Nichts entfernt, kein bestehender Satz umgeschrieben; kein neues Abbild; keine Marke.") % (t631[0], k9, datum, s0)
    q1 = ("*Übernommen zeichengleich aus `%s` (Commit `%s`, md5 `%s`), dem Entwurf aus TB-166 (Ergebnis TB-166, Abschnitt „Entwurf Tatsachennotiz nach 37.3“). Vollzogen in Commit `%s` (TB-166 E). "
          "„Entwurf, nicht eingetragen“ darin beschreibt den Stand in TB-166; eingetragen ist der Übergang mit diesem Abschnitt.*") % (NOTIZ, NOTIZ_COMMIT, NOTIZ_MD5, E3A_COMMIT)
    fk = "**Freigabe-Karte TB-166, wörtlich** (zu R98 (c); aus `%s` Z. %d, Commit `%s`, md5 `%s`):" % (M166, kz, M166_COMMIT, M166_MD5)
    an = ("**Abnahme nach R98 (d)** (gemessen in TB-169 Schritt E am Erzeuger, Commit `%s`): `research/tb24_haltedauern/test_listen_erzeuger.py` auf einem Test-Snapshot, geprüft an den Ausgaben von "
          "`positionen_holen.py` (Probe nach R86 (d) mit und ohne Zeilen ab dem Schnitt; Wachen nach R86 (d) und R87 (c) je allein beissend, 41.1 A5; Fall nach R90 (g), Tatsachennotiz für t3_supertrend und die zwei Elliott-Bots im Beleg; Symbol nach R81 (h); offene Position nach R86 (c)); Beleg `%se_abnahme.txt`: „%s“, `rc 0`; Kerzen-Probe `%se_kerzen.txt`: „%s“.") % (ec, BEL, za[-2], BEL, lies(BEL + "e_kerzen.txt").rstrip("\n").split("\n")[-2])
    neu = ["", TITEL64, "", kopf, "", "### 64.1 Vollzug TB-166 (Tatsachennotiz nach 37.3)", "", q1, ""] + t.rstrip("\n").split("\n") + ["", fk, "", "> " + k6, "", an, "", satz(f, s0), ""]
    if probe: print("\n".join(neu)); ende()
    alt = lies(REG); schreibe(REG, "\n".join(z[:-1] + neu))
    r2 = lies(REG); p(r2.startswith(alt[:-1]) and r2.count("\n" + TITEL64 + "\n") == 1, "nachher: append-only, 64 genau einmal, Z. %d" % (r2.split("\n").index(TITEL64) + 1))
    p(t.rstrip("\n") in r2 and r2.endswith("\n") and not r2.endswith("\n\n"), "e_notiz.md zeichengleich; Register endet mit einer Leerzeile"); ende()
def index(s0, datum, probe):
    teil = [t for t in range(1, 10) if os.path.exists("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t) and "\n## 64. " in lies("docs/projektfuehrung/REGISTER_KOPIE_teil%d.md" % t)]
    p(len(teil) == 1, "Abschnitt 64 in genau einer Teildatei: T%s" % teil); T = str(teil[0]) if teil else "?"
    z = lies(IDX).split("\n"); rcm = git("rev-parse", "--short", "HEAD").strip()
    k = [i for i, l in enumerate(z) if l.startswith("**Stand:** Register `docs/VORREGISTRIERUNG_neuselektion.md` am Commit `")]
    if p(len(k) == 1 and "Abschnitte 0–63" in z[k[0]], "Kopf genau einmal, nennt 0–63"):
        z[k[0]] = re.sub(r"am Commit `[0-9a-f]{7}` \([^)]*\)", "am Commit `%s` (%s)" % (rcm, datum), z[k[0]]).replace("Abschnitte 0–63", "Abschnitte 0–64")
    i = [j for j, l in enumerate(z) if l.startswith("| 63 Vollzug TB-167 |")]
    if p(len(i) == 1, "Zeile 63 genau einmal"):
        z.insert(i[0] + 1, "| 64 Vollzug TB-166 | %s | 64.1 Hash-Übergänge nach 37.3 (E-3a, 20 Dateien, Commit `%s`; aus docs/belege/TB-166/e_notiz.md) mit Freigabe-Karten, Abnahme nach R98 (d) am Listen-Erzeuger (TB-169) und Sonde zu Punkt 11 | – |" % (T, E3A_COMMIT))
    j = [n for n, l in enumerate(z) if l.startswith("Zuletzt nachgezogen in TB-168 (")]
    if p(len(j) == 1, "Pflegezeile TB-168 genau einmal"):
        z[j[0]] = z[j[0]].replace("Zuletzt nachgezogen in TB-168 (", "In TB-168 (")
        e = next(n for n in range(j[0] + 1, len(z) + 1) if n == len(z) or z[n] == "")
        z.insert(e, "Zuletzt nachgezogen in TB-169 (%s): Zeilenangaben mit `docs/belege/TB-154/c2_index_zeilen.py %s %s`; Einträge mit dem Werkzeug aus Anhang A des Auftrags TB-169 (`index`); 64 (Vollzug TB-166) kommt zu T%s." % (datum, s0, rcm, T))
    if not probe and not nein(): schreibe(IDX, "\n".join(z))
    ende()
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith(RANG1)]
    if p(len(a) == 1 and z[a[0]].endswith(RANG1E), "BACKLOG Rang 1 genau einmal, Stand TB-166"):
        z[a[0]] = z[a[0]][:-2] + (" · E-3b (Listen-Erzeuger: Schnitt an der Eingabe, Wachen, Doppellauf weg; kerzen_je_trade mit datetime64) und Abnahme nach R98 (d) mit TB-169 (%s, Journal %s); Register 64 (Vollzug TB-166 nach 37.3)"
            "; vor der Neuerzeugung der Listen: `auswertung.py` (Z. 71, 325) und `embargo_neun.py` (Z. 35) lesen noch `<bot>_positionen.csv` bzw. `trades_ausgefuehrt` (entfallen mit E-3b); das Abbild tb117 führt die neun `daten/<bot>_alle_trades.csv` (Neuerzeugung trifft das Abbild); R102 (d), R92 (c) |") % (datum, kenn)
    if not probe and not nein(): schreibe(BL, "\n".join(z))
    ende()
def journal(blk, probe):
    b = lies(blk).rstrip("\n").split("\n"); z = lies(JO).split("\n"); neu = naechste(max(kennungen()))
    i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-169: " % neu), "Kopfzeile ## %s — TB-169: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b and "### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Block: eine ## -Zeile, kein ---, Teile da")
    if not probe and not nein(): z[i[0] - 2:i[0] - 2] = b + [""]; schreibe(JO, "\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif a == ["e3b"]: e3b(pr)
    elif len(a) == 2 and a[0] == "abnahme": abnahme(a[1])
    elif len(a) == 3 and a[0] == "altvergleich": altvergleich(a[1], a[2])
    elif len(a) == 4 and a[0] == "sonde": sonde(a[1], a[2], a[3])
    elif len(a) == 6 and a[0] == "register": register(a[1], a[2], a[3], a[4], a[5], pr)
    elif len(a) == 3 and a[0] == "index": index(a[1], a[2], pr)
    elif a == ["kennung"]: print("Kennung %s (letzte %s)" % (naechste(max(kennungen())), max(kennungen()))); sys.exit(0)
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

### Anhang B — `e3b_positionen_holen.py` (sha256 `b6d1e2d66eae02a8a546cab15649a4100e3c1b2df0a9a668140f23de3a8573db`)

<!-- DATEI e3b_positionen_holen.py -->
````python
"""
Ein Bot, ein Prozess: Positionen MIT Ausstiegsart und Kerzenzahl herausholen
==============================================================================
Untersuchung TB-24 (Haltedauern und Zeithorizonte). **Liest nur.** An
Bot-, Backtest- oder Live-Dateien wird nichts geaendert; geschrieben wird
ausschliesslich in den Ordner, den `--ziel` nennt.

ZIEL UND EINMAL-SCHREIBSPERRE (TB-98, Register 36.1 und 40.6)
------------------------------------------------------------------------------
Bis TB-98 schrieb dieses Skript fest nach `research/tb24_haltedauern/daten/`.
Die neun `<bot>_alle_trades.csv` dort sind seit Register 40.6 Eingabedateien
einer Herleitung von Registertext (33.2) und bleiben als historischer Stand
(`78e2bc6`) liegen - ein Aufruf haette sie ueberschrieben. Seitdem:

  (3)  `--ziel ORDNER` ist **Pflicht**, es gibt **keine Voreinstellung**. Ohne
       Argument endet der Aufruf mit 2, bevor irgendetwas geladen wird. Der
       Ordner muss bestehen; er wird nicht angelegt (sonst 2).
  (2)  **Einmal-Schreibsperre, vor der Rechnung:** Besteht eine der vier
       Zieldateien des Bots schon, endet der Aufruf mit 1, nennt Pfad und
       SHA-256 der vorhandenen Datei(en) und hat weder gerechnet noch
       geschrieben. Geschrieben wird mit `O_CREAT|O_EXCL`; entsteht eine Datei
       waehrend des Laufs, ebenfalls 1. Nie ueberschreiben, auch nicht mit
       identischem Inhalt (36.1: "Die Sperre ist staerker, wenn sie duemmer ist").
  B5   Neben die drei Dateien kommt `<bot>_herkunft.json`: Erzeuger, Zeit,
       Code-Commit, Selektionsmodus (Audit aus `shared/paths.py`, sonst null)
       und je geschriebener Datei der SHA-256. **Keine Trade-Zahlen** (27.1).

⚠️ Die Rechenwege sind unveraendert (TB-98 B3, AST-Vergleich gegen
`e87b06f`): anders sind nur die Zielbestimmung und die Schreibaufrufe. Das
Ausgabeformat ist bytegleich - `to_csv(index=False)` und
`json.dumps(indent=2, default=str)` erzeugen denselben Text wie vorher der
Aufruf mit Dateipfad bzw. Dateiobjekt.

WAS DIESES SKRIPT ANDERS MACHT ALS `research/exposure_messung/bot_lauf.py`
------------------------------------------------------------------------------
Die Exposure-Messung brauchte je Position `allocation` und `capital_after`.
Fuer Haltedauern kommen drei Angaben hinzu, die dort weggefallen sind:

* `result`  - die Ausstiegsart des Bots selbst (`stop_loss`, `take_profit`,
              `time_exit`, `sma_exit`, `trend_flip`). Sie steht in den
              Trade-Tabellen der Backtests und ueberlebt
              `collect_all_trades()`, weil das die Spalten unveraendert
              durchreicht. Ohne sie laesst sich ein Stop-Loss nach zwei Tagen
              nicht von einem Zeitausstieg nach fuenfzehn unterscheiden -
              genau die Trennung, die die Aufgabe verlangt.
* `kerzen`  - Anzahl der Kerzen zwischen Einstieg und Ausstieg, aus der
              Kursreihe des jeweiligen Symbols GEZAEHLT (nicht aus
              Kalendertagen umgerechnet). Die neun Bots laufen auf drei
              Zeitrahmen; nur so ist "Haltedauer" zwischen 1h, 4h und 1d
              vergleichbar.
* `entry_price` / `exit_price` - nur zur Nachvollziehbarkeit im Datensatz.

DIE BOT-SPEZIFISCHEN AUFRUFE WERDEN NICHT NEU GESCHRIEBEN
------------------------------------------------------------------------------
`hole_trades()` und `simuliere()` kommen per Import aus
`research/exposure_messung/bot_lauf.py`. Dort steht, mit welchen Argumenten
`collect_all_trades()` je Bot aufzurufen ist - inklusive des
BTC-Regimefilters, den `volatility_breakout_crypto` bewusst erst danach
anwendet. Diese Zuordnung ein zweites Mal hinzuschreiben waere genau die
Doppelfuehrung, an der dieses Projekt schon einmal unbemerkt auseinander-
gelaufen ist (Uebergabeprotokoll Prinzip 11). Mitimportiert werden dabei
auch die Stubs fuer `binance`, `yfinance` und `fetch_binance_data`, die in
dieser Umgebung fehlen bzw. Zugangsdaten enthalten.

Der Import fuehrt den Modulkopf von `bot_lauf.py` aus. Der liest `sys.argv[1]`
(darum steht der Bot-Name auch hier an erster Stelle) und legt
`research/exposure_messung/daten/` an, falls es fehlt - geschrieben wird dort
nichts, `bot_lauf.main()` wird nie aufgerufen.

DIE ZUORDNUNG "WELCHER TRADE WURDE AUSGEFUEHRT"
------------------------------------------------------------------------------
Uebernommen aus `bot_lauf.py`, weil es keinen zweiten korrekten Weg gibt:
`simulate_portfolio()` gibt seine Liste der offenen Positionen nicht heraus.
Sie wird deshalb zweimal mit demselben Trade-Satz aufgerufen - einmal
unveraendert, einmal mit einer Zeilenkennung in der `symbol`-Spalte
(`AAPL#417`), die dort reine Beschriftung ist. Dass die Kennzeichnung die
Simulation nicht veraendert hat, wird geprueft, nicht angenommen.

Nutzung:
    python3 positionen_holen.py <bot_name> --ziel <ordner>

Rueckgabewerte (Register 36.5): 0 geschrieben, 1 Ziel existiert (Befund),
2 Aufruf unvollstaendig oder Zielordner fehlt.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_DIR))
_EXPOSURE_DIR = os.path.join(_REPO_ROOT, "research", "exposure_messung")

if len(sys.argv) < 2:
    raise SystemExit("Aufruf: python3 positionen_holen.py <bot_name> --ziel <ordner>")
BOT = sys.argv[1]

# Rueckgabewerte nach 36.5. BEFUND: das Ziel existiert; NICHT_MOEGLICH: ohne
# Ziel oder ohne Zielordner laesst sich nicht erzeugen.
BEFUND = 1
NICHT_MOEGLICH = 2

# ⚠️ 36.1 (3): das Ziel nur durch ausdrueckliches Argument, KEINE
# Voreinstellung. Geprueft wird hier, vor dem Import von bot_lauf.py und vor
# jedem Laden - ein Aufruf ohne Ziel verbraucht nichts.
_aufruf = argparse.ArgumentParser(
    description="Positionen und alle gefundenen Trades eines Bots (TB-24). "
                "Schreibt einmalig in den Ordner aus --ziel (Register 36.1).")
_aufruf.add_argument("bot")
_aufruf.add_argument("--ziel", required=True, metavar="ORDNER",
                     help="bestehender Ordner; vorhandene Zieldateien werden NIE "
                          "ueberschrieben - der Lauf endet dann mit 1")
_args = _aufruf.parse_args(sys.argv[1:])
if _args.bot != BOT:
    # bot_lauf.py liest den Bot-Namen fest aus sys.argv[1].
    sys.stderr.write("ABBRUCH: der Bot-Name muss das erste Argument sein.\n")
    sys.exit(NICHT_MOEGLICH)
ZIEL_DIR = os.path.abspath(_args.ziel)
if not os.path.isdir(ZIEL_DIR):
    sys.stderr.write("ABBRUCH: Zielordner fehlt: %s - er wird nicht angelegt.\n" % ZIEL_DIR)
    sys.exit(NICHT_MOEGLICH)

# TB-169 (E-3b, R97 (a)): der Doppellauf ist weg, `<bot>_positionen.csv` entfaellt.
ZIELDATEIEN = [f"{BOT}_alle_trades.csv", f"{BOT}_meta.json", f"{BOT}_herkunft.json"]

# Der Modulkopf von bot_lauf.py setzt sys.path fuer strategies/<BOT> und
# shared/ und legt die Stubs an; er liest den Bot-Namen aus sys.argv[1].
sys.path.insert(0, _EXPOSURE_DIR)
import bot_lauf as basis                                    # noqa: E402
sys.path.insert(0, os.path.join(_REPO_ROOT, "research", "faltenplan_neun"))
import faltenschranke_messung as fsm                        # noqa: E402

assert basis.BOT == BOT, f"bot_lauf.py hat '{basis.BOT}' gelesen, erwartet '{BOT}'"

TRENNER = basis.TRENNER

# Zeitrahmen je Bot - nur als Beschriftung der Ausgabe. Die Kerzenzahl wird
# gezaehlt, nicht daraus berechnet; eine falsche Angabe hier veraendert also
# keine Messung. Quelle: Uebergabeprotokoll Abschnitt 2.
ZEITRAHMEN = {
    "elliott_wave": "1h",
    "t3_supertrend": "4h",
    "rsi2_crypto": "1d",
    "turtle_soup_crypto": "1d",
    "volatility_breakout_crypto": "1d",
    "elliott_wave_stocks": "1d",
    "rsi2_mean_reversion": "1d",
    "turtle_soup_stocks": "1d",
    "volatility_breakout": "1d",
}

ANLAGEKLASSE = {
    "elliott_wave": "krypto",
    "t3_supertrend": "krypto",
    "rsi2_crypto": "krypto",
    "turtle_soup_crypto": "krypto",
    "volatility_breakout_crypto": "krypto",
    "elliott_wave_stocks": "aktien",
    "rsi2_mean_reversion": "aktien",
    "turtle_soup_stocks": "aktien",
    "volatility_breakout": "aktien",
}


def _sha256(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sperre_vor_der_rechnung() -> bool:
    """36.1 (2), vor der Rechnung: True (und Meldung), wenn eine Zieldatei
    schon besteht. Dann wird nichts geladen, gerechnet oder geschrieben."""
    vorhanden = [os.path.join(ZIEL_DIR, n) for n in ZIELDATEIEN
                 if os.path.lexists(os.path.join(ZIEL_DIR, n))]
    for pfad in vorhanden:
        print("ABBRUCH (36.1 (2)): Ziel existiert, nichts gerechnet, nichts geschrieben."
              "\n  Pfad:    %s\n  SHA-256: %s" % (pfad, _sha256(pfad)))
    return bool(vorhanden)


def _schreibe_einmal(name: str, inhalt: str) -> str:
    """Genau einmal schreiben (`O_CREAT|O_EXCL`); SHA-256 des Geschriebenen.

    `newline=""`: kein Uebersetzen von Zeilenenden - der Text geht so auf die
    Platte, wie `to_csv`/`json.dumps` ihn liefern."""
    pfad = os.path.join(ZIEL_DIR, name)
    try:
        fd = os.open(pfad, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        print("ABBRUCH (36.1 (2)): Ziel entstand waehrend des Laufs, nichts "
              "ueberschrieben.\n  Pfad:    %s\n  SHA-256: %s" % (pfad, _sha256(pfad)))
        sys.exit(BEFUND)
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        f.write(inhalt)
    return _sha256(pfad)


def _schreibe_herkunft(hashes: dict):
    """B5: die Herkunftsnotiz neben den Listen. Keine Trade-Zahlen (27.1)."""
    import paths
    audit = paths.startpruefung()
    lauf = subprocess.run(["git", "-C", _REPO_ROOT, "rev-parse", "HEAD"],
                          capture_output=True, text=True)
    notiz = {
        "erzeuger": "research/tb24_haltedauern/positionen_holen.py",
        "bot": BOT,
        "zeit_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "code_commit": lauf.stdout.strip() if lauf.returncode == 0 else None,
        "selektionsmodus": audit,
        "dateien_sha256": hashes,
    }
    _schreibe_einmal(f"{BOT}_herkunft.json",
                     json.dumps(notiz, indent=2, ensure_ascii=False, sort_keys=True) + "\n")


def kursreihe(eintrag):
    """`load_all_symbol_data()` liefert je Bot entweder den DataFrame direkt
    oder das Paar (DataFrame, entry_cutoff) - beides kommt vor (Aktien-Bots
    mit RECENT_YEARS_ONLY liefern das Paar)."""
    if isinstance(eintrag, tuple):
        return eintrag[0]
    return eintrag


def kerzen_je_trade(trades: pd.DataFrame, all_data: dict) -> pd.Series:
    """Anzahl der Kerzen von Einstieg bis Ausstieg, je Trade aus der
    Kursreihe des Symbols GEZAEHLT: Kerzen mit
    entry_time <= open_time <= exit_time, beide Enden eingeschlossen.

    Eine Position, die auf derselben Kerze eroeffnet und geschlossen wuerde,
    ergibt damit 1. Fehlt die Kursreihe (kann nicht vorkommen, weil die
    Trades daraus entstanden sind), bleibt der Wert leer statt geraten.
    """
    zeiten = {}
    for symbol, eintrag in all_data.items():
        df = kursreihe(eintrag)
        zeiten[symbol] = pd.to_datetime(df["open_time"]).sort_values().to_numpy()

    werte = []
    for symbol, ein, aus in zip(trades["symbol"], trades["entry_time"], trades["exit_time"]):
        reihe = zeiten.get(symbol)
        if reihe is None:
            werte.append(pd.NA)
            continue
        # TB-169: datetime64 statt Timestamp - unter pandas 2.3.3/numpy 2.0.2 wirft searchsorted sonst TypeError
        links = reihe.searchsorted(pd.Timestamp(ein).to_datetime64(), side="left")
        rechts = reihe.searchsorted(pd.Timestamp(aus).to_datetime64(), side="right")
        werte.append(int(rechts - links))
    return pd.Series(werte, index=trades.index, dtype="Int64")


# --- TB-169 (E-3b): Schnitt an der Eingabe, Wachen, kein Doppellauf ---------
# Go-Live-Schnitt (ausschliesslich) aus derselben Quelle wie der Handelbar-Tag
# (faltenschranke_messung.handelbar_ab rechnet mit faltenplan_neun.GO_LIVE).
SCHNITT = pd.Timestamp(fsm.fp.GO_LIVE)
WACHE = 2   # 36.5: Befund ueber den Erzeuger, kein Ausgang (R81 (g), R86 (d), R87 (c))


def _abbruch(text):
    sys.stderr.write("[positionen_holen] ABBRUCH %s: %s\n" % (BOT, text))
    sys.exit(WACHE)


def _vor_schnitt(zeiten) -> pd.Series:
    """Maske 'Zeit < Schnitt' in der Zeitzone der Spalte (R86 (e): beide gleich gelesen)."""
    t = pd.to_datetime(zeiten)
    s = SCHNITT.tz_localize(t.dt.tz) if t.dt.tz is not None else SCHNITT
    return t < s


def lesesicht_an():
    """R86 (b), eine Stelle fuer neun Bots: `read_csv` liefert nur Zeilen mit
    open_time < Schnitt (Bauart loaderlauf.stichtagssicht_an, aber '<').
    Gilt fuer den ganzen Lauf, also auch fuer Dateien, die collect_all_trades
    selbst liest (BTC-Regimefilter)."""
    echt = pd.read_csv

    def sicht(*a, **k):
        df = echt(*a, **k)
        if isinstance(df, pd.DataFrame) and "open_time" in df.columns:
            df = df[_vor_schnitt(df["open_time"]).values].reset_index(drop=True)
        return df
    pd.read_csv = sicht


def wache_zeilen(all_data):
    """R86 (d) Wache 1: keine Zeile ab dem Schnitt erreicht den Signalpfad."""
    for symbol, eintrag in all_data.items():
        df = kursreihe(eintrag)
        if len(df) and not _vor_schnitt(df["open_time"]).all():
            _abbruch("Zeile ab dem Schnitt %s im Signalpfad (%s, R86 (d))" % (SCHNITT.date(), symbol))


def wache_trades(trades, handelbar):
    """R86 (d) Wache 2 und R87 (c): keine Ein-/Ausstiegszeit am Schnitt oder spaeter,
    kein Einstieg vor dem Handelbar-Tag des Symbols (Tag aus derselben Rechnung)."""
    for spalte in ("entry_time", "exit_time"):
        if not _vor_schnitt(trades[spalte]).all():
            _abbruch("Trade mit %s am Schnitt oder spaeter (R86 (d))" % spalte)
    for symbol, gruppe in trades.groupby(trades["symbol"].astype(str)):
        tag = handelbar.get(symbol)
        if tag is None:
            _abbruch("Trade fuer %s ohne Handelbar-Tag (R81 (c))" % symbol)
        t = pd.to_datetime(gruppe["entry_time"]); h = pd.Timestamp(tag)
        if t.dt.tz is not None:
            h = h.tz_localize(t.dt.tz)
        if (t.dt.normalize() < h).any():
            _abbruch("Einstieg %s vor dem Handelbar-Tag %s bei %s (R87 (c))" % (t.min(), tag, symbol))


def main():
    import equity_simulation as es

    lesesicht_an()
    all_data = es.load_all_symbol_data()
    if not all_data:
        raise SystemExit(f"{BOT}: keine Kursdaten gefunden.")
    wache_zeilen(all_data)

    handelbar = fsm.handelbar_ab(BOT)
    trades = basis.hole_trades(es, all_data, handelbar)
    if trades is None or trades.empty:
        raise SystemExit(f"{BOT}: keine Trades.")

    trades = trades.copy()
    trades["entry_time"] = pd.to_datetime(trades["entry_time"])
    trades["exit_time"] = pd.to_datetime(trades["exit_time"])
    wache_trades(trades, handelbar)

    # --- Alle gefundenen Trades, mit Kerzenzahl und Ausstiegsart ------------
    # A9 (41.1, R97 (a)): `symbol` bleibt unveraendert, keine Kennung.
    trades["kerzen"] = kerzen_je_trade(trades, all_data)
    ausgabespalten = [s for s in ("symbol", "entry_time", "exit_time", "result",
                                   "pnl_pct", "entry_price", "exit_price", "kerzen")
                      if s in trades.columns]
    alle = trades[ausgabespalten].copy()
    alle.insert(0, "trade_zeile", trades.index)
    if (alle["entry_time"] > alle["exit_time"]).any():
        raise SystemExit(f"{BOT}: Einstieg nach Ausstieg - Abbruch.")

    alle = alle.sort_values("entry_time", kind="stable").reset_index(drop=True)
    hashes = {}
    hashes[f"{BOT}_alle_trades.csv"] = _schreibe_einmal(
        f"{BOT}_alle_trades.csv", alle.to_csv(index=False))

    fehlende_kerzen = int(alle["kerzen"].isna().sum())
    ohne_result = "result" not in trades.columns
    meta = {
        "bot": BOT,
        "zeitrahmen": ZEITRAHMEN.get(BOT),
        "anlageklasse": ANLAGEKLASSE.get(BOT),
        "go_live_schnitt": str(SCHNITT.date()),
        "trades_gefunden": int(len(trades)),
        "symbole_gefunden": int(trades["symbol"].nunique()),
        "symbole_geladen": int(len(all_data)),
        "erster_einstieg": str(alle["entry_time"].min()),
        "letzter_ausstieg": str(alle["exit_time"].max()),
        "ausstiegsarten": (None if ohne_result
                            else {str(k): int(v) for k, v
                                  in alle["result"].value_counts().items()}),
        "spalte_result_vorhanden": not ohne_result,
        "kerzen_ohne_wert": fehlende_kerzen,
    }
    hashes[f"{BOT}_meta.json"] = _schreibe_einmal(
        f"{BOT}_meta.json", json.dumps(meta, indent=2, default=str))
    _schreibe_herkunft(hashes)
    print(f"{BOT}: {meta['trades_gefunden']} Trades gefunden, "
          f"{meta['symbole_gefunden']} Symbole, Ausstiegsarten: {meta['ausstiegsarten']}, "
          f"Kerzen ohne Wert: {fehlende_kerzen}")


if __name__ == "__main__":
    if sperre_vor_der_rechnung():
        sys.exit(BEFUND)
    main()
````

### Anhang C — `e3b_alle_bots.py` (sha256 `4246b577bfc486e3f872ea5132412fe5e23092e23b737182d765373118666964`)

<!-- DATEI e3b_alle_bots.py -->
````python
"""
Alle neun Bots nacheinander, je in einem eigenen Prozess.

Ein eigener Prozess je Bot ist nicht Vorsicht, sondern Notwendigkeit: alle
neun Bots haben gleichnamige, inhaltlich verschiedene Module
(`equity_simulation.py`, `live_params.py`, `multi_symbol_optimise.py`) - im
selben Prozess liefert das sys.modules-Caching ab dem zweiten Bot die falsche
Fassung. Vorbild: `shared/portfolio_overview.py` und
`research/exposure_messung/alle_bots.py`.

Nutzung:
    python3 alle_bots.py --ziel <ordner> [bot ...]

`--ziel` ist Pflicht und wird an jeden `positionen_holen.py`-Aufruf
durchgereicht (TB-98 B4, Register 36.1): keine Voreinstellung, und ein Bot,
dessen Zieldateien schon bestehen, endet dort mit 1, ohne zu rechnen. Der
Pfad wird hier absolut gemacht, weil die Kindprozesse in diesem Ordner laufen.
"""

import argparse
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))

BOTS = [
    "elliott_wave",
    "t3_supertrend",
    "rsi2_crypto",
    "turtle_soup_crypto",
    "volatility_breakout_crypto",
    "elliott_wave_stocks",
    "rsi2_mean_reversion",
    "turtle_soup_stocks",
    "volatility_breakout",
]


def main():
    aufruf = argparse.ArgumentParser(description="positionen_holen.py fuer mehrere Bots.")
    aufruf.add_argument("--ziel", required=True, metavar="ORDNER")
    aufruf.add_argument("bots", nargs="*")
    args = aufruf.parse_args()
    ziel = os.path.abspath(args.ziel)
    bots = args.bots or BOTS
    fehler, wache = [], []
    for bot in bots:
        print(f"\n=== {bot}", flush=True)
        ergebnis = subprocess.run(
            [sys.executable, os.path.join(_DIR, "positionen_holen.py"), bot,
             "--ziel", ziel], cwd=_DIR)
        if ergebnis.returncode == 2:
            wache.append(bot)   # TB-169 (E-3b): Wache eines Bots bleibt 2 (36.5)
        elif ergebnis.returncode != 0:
            fehler.append(bot)

    if wache:
        print(f"\nWACHE (2): {', '.join(wache)}" + (f"; FEHLGESCHLAGEN: {', '.join(fehler)}" if fehler else ""))
        sys.exit(2)
    if fehler:
        print(f"\nFEHLGESCHLAGEN: {', '.join(fehler)}")
        sys.exit(1)
    print(f"\nAlle {len(bots)} Bots durchgelaufen.")


if __name__ == "__main__":
    main()
````

### Anhang D — `e3b_test_listen_erzeuger.py` (sha256 `e196884a152796e4a9ab6e715de70933ebf7614ecf4f38d763eed24d46cda1bf`)

<!-- DATEI e3b_test_listen_erzeuger.py -->
````python
#!/usr/bin/env python3
"""TB-169 (E-3b; R86 (b)-(d), R87 (c), R81 (c)/(h), R90 (g), R98 (d), R97 (a)): Probe am Listen-Erzeuger
research/tb24_haltedauern/positionen_holen.py auf Test-Snapshots (Ersatzwurzel TB36_BASE_DIR im Temp-Ordner, DATA_DIR/SYMBOLS
des Laders umgebogen, Bauart loaderlauf.lade_botmodul). data/ wird nicht gelesen. Geprueft an den AUSGABEN des Erzeugers
(<bot>_alle_trades.csv, Rueckgabewert), je Bot im eigenen Prozess; Snapshot A mit, B ohne Zeilen ab dem Schnitt (B = A gekuerzt).
Die Zeitachse wird je Bot um eine Zahl Balken versetzt (gleiche Kursfolge), bis A (Schnitt aus) ein Einstiegssignal ab dem
Schnitt und eine vor dem Schnitt eroeffnete, am letzten Tag von B offene Position enthaelt (Bauart R81 (h)).
   1 Probe R86 (d): Listen aus A und B byte-gleich, rc 0
  2a Schnitt aus -> Wache 1 (Zeile ab Schnitt im Signalpfad) beisst allein (2)
  2b Schnitt und Wachen aus -> Listen weichen von B ab, ein Einstieg ab dem Schnitt erscheint (R81 (h))
  2c Schnitt und Wache 1 aus -> Wache 2 (Trade-Zeit am Schnitt oder spaeter) beisst allein (2)
  3a R90 (g): Tag in einer offenen Position -> kein Einstieg davor; der ohne Schranke verdraengte zweite Einstieg erscheint
     (vor dem alten Ausstieg). Tatsachennotiz nach R90 (g) bei t3_supertrend (Fall kann nicht entstehen) und den zwei Elliott-Bots
     (Teilmessung, Wortlaut in OHNE_R90G); dort geprueft: kein Einstieg vor dem Tag, alle alten Trades ab dem Tag bleiben
  3b spaetes Symbol (Tag am ersten alten Einstieg) gleich mit/ohne Schranke
   4 Gegenprobe R87 (c): Schranke aus (hole_trades ohne handelbar) -> Wache 3 beisst (2)
  5a R81 (h), eigener Snapshot mit Symbol SPAET (erreicht die Schranke nur mit Zeilen ab dem Schnitt): rc 0, Tag None, nicht in der Liste
  5b derselbe Snapshot, Schnitt und Wache 1 aus -> SPAET geladen ohne Tag -> Wache R81 (c) beisst (2), ohne Eingriff in den Tag
   6 A9: Spalte symbol unveraendert, keine positionen.csv
   7 R86 (c)/R83 (c): die am Ende von B offene Position wird nach der Ausstiegskonvention des Signalpfads behandelt (kein Trade, oder
     Ausstieg am letzten Balken vor dem Schnitt); B rc 0, keine leere Ausstiegszeit (NaT), kein Ausstieg am Schnitt oder spaeter
   8 nur Dateien des Test-Snapshots gelesen (read_csv), auch fuer den BTC-Regimefilter
Aufruf aus der Repo-Wurzel: python3 -B research/tb24_haltedauern/test_listen_erzeuger.py [bot ...]  (rc 0 = alle bestanden)"""
import json, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "rsi2_mean_reversion", "turtle_soup_stocks",
        "volatility_breakout", "t3_supertrend", "elliott_wave", "elliott_wave_stocks"]
AKTIEN = ("rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout", "elliott_wave_stocks")
TF = {"elliott_wave": "1h", "t3_supertrend": "4h"}
SCHNITT = "2026-09-01"
OHNE_R90G = {"t3_supertrend": "Einstieg nur am Kreuzen nach oben (backtest_trend.py Z. 111-112), die Position endet am Kreuzen nach unten, "
                              "am Trend-Flip des Supertrend (Z. 123) oder am Stop: solange sie offen ist, entsteht kein zweites "
                              "Einstiegssignal, das verdraengt werden koennte",
             "elliott_wave": "Teilmessung - die Trade-Schleife fuehrt keinen Positionszustand (backtest_elliott.py Z. 113: je Welle ein Trade); "
                             "verdraengt wird nur in der Wellenauswahl (traded, elliott_wave_counter.py Z. 363), die Schranke steht davor (Z. 361): "
                             "eine gesperrte Welle hinterlaesst keinen traded-Eintrag - belegt am Signalpfad in TB-166 (test_schranke_signalpfad "
                             "Pruefung 5 und Mutation, docs/belege/TB-166/e_test_schranke.txt); am Erzeuger nicht herstellbar (kein Paar alter "
                             "Einstiege innerhalb SIGNAL_FRESHNESS_BARS 48 im Test-Snapshot); geprueft: kein Einstieg vor dem Tag, alte Trades ab dem Tag bleiben",
             "elliott_wave_stocks": "Teilmessung - wie elliott_wave (backtest_elliott.py Z. 122, elliott_wave_counter.py Z. 361/363, "
                                    "SIGNAL_FRESHNESS_BARS 5; TB-166 Pruefung 5 und Mutation); geprueft: kein Einstieg vor dem Tag, alte Trades ab dem Tag bleiben"}
def achse(bot, versatz):
    import pandas as pd
    tf = TF.get(bot, "1d")
    if bot in AKTIEN:
        n = len(pd.bdate_range("2008-01-02", "2027-12-31")); return pd.bdate_range(pd.Timestamp("2008-01-02") + pd.offsets.BDay(versatz), periods=n)
    a = {"1d": "2019-01-01", "4h": "2021-06-01", "1h": "2022-01-01"}[tf]; f = tf.replace("d", "D"); n = len(pd.date_range(a, "2027-12-31 23:00", freq=f))
    return pd.date_range(pd.Timestamp(a) + versatz * pd.Timedelta(f), periods=n, freq=f)
def snapshot(bot, d, ab_schnitt, seed, spaet=False, versatz=0):
    import numpy as np, pandas as pd
    tf = TF.get(bot, "1d"); t = achse(bot, versatz)
    syms = ["AAA", "BBB", "CCC"] + ([] if bot in AKTIEN else ["BTCUSDT"]) + (["SPAET"] if spaet else [])
    for u in ("data", "config", "strategies/" + bot, "research"): os.makedirs(os.path.join(d, u), exist_ok=True)
    shutil.copy(os.path.join(WURZEL, "strategies", bot, "multi_symbol_optimise.py"), os.path.join(d, "strategies", bot))
    os.symlink(os.path.join(WURZEL, "research", "universum_trockenlauf"), os.path.join(d, "research", "universum_trockenlauf"))   # Aktien-Horizont (TB-163)
    open(os.path.join(d, "config", "top25_symbols.txt"), "w").write("" if bot in AKTIEN else "\n".join(syms) + "\n")
    open(os.path.join(d, "config", "sp500_top150.txt"), "w").write("\n".join(syms) + "\n" if bot in AKTIEN else "")
    for k, s in enumerate(syms):
        r = np.random.default_rng(seed + k); v = 0.012 if tf != "1d" else 0.025
        c = 50 * np.exp(np.cumsum(r.normal(0.0001, v, len(t)))); o = c * (1 + r.normal(0, v / 5, len(t)))
        h = np.maximum(o, c) * (1 + np.abs(r.normal(0, v / 3, len(t)))); lo = np.minimum(o, c) * (1 - np.abs(r.normal(0, v / 3, len(t))))
        df = pd.DataFrame({"open_time": t.strftime("%Y-%m-%d" if tf == "1d" else "%Y-%m-%d %H:%M:%S"), "open": o, "high": h, "low": lo, "close": c,
                           "volume": r.integers(10**5, 10**6, len(t))})
        if s == "SPAET": df = df[t >= pd.Timestamp("2022-01-03" if bot in AKTIEN else "2025-06-01" if tf == "1d" else "2025-01-01")]
        if not ab_schnitt: df = df[pd.to_datetime(df["open_time"]) < pd.Timestamp(SCHNITT)]
        df.to_csv(os.path.join(d, "data", "%s_%s.csv" % (s, tf)), index=False)
def kind(bot, d, ziel, modus, tags):
    import importlib.util
    sys.argv = ["positionen_holen.py", bot, "--ziel", ziel]
    spec = importlib.util.spec_from_file_location("ph", os.path.join(WURZEL, "research", "tb24_haltedauern", "positionen_holen.py"))
    ph = importlib.util.module_from_spec(spec); spec.loader.exec_module(ph)
    import multi_symbol_optimise as mso
    mso.DATA_DIR = os.path.join(d, "data"); tf = TF.get(bot, getattr(mso, "INTERVAL", "1d"))
    mso.SYMBOLS = [s for s in ("AAA", "BBB", "CCC", "BTCUSDT", "SPAET") if os.path.exists(os.path.join(d, "data", "%s_%s.csv" % (s, tf)))]
    echt = ph.fsm.handelbar_ab; t = json.loads(tags); spur = {"gelesen": [], "spaet": "fehlt"}
    def hb(b, schnitt=None):
        x = dict(echt(b, schnitt)); spur["spaet"] = x.get("SPAET", "fehlt"); x.update(t); return x
    ph.fsm.handelbar_ab = hb
    rc_echt = ph.pd.read_csv
    def lies(*a, **k):
        try: spur["gelesen"].append(os.path.realpath(os.fspath(a[0])))
        except TypeError: spur["gelesen"].append(repr(a[0])[:80])
        return rc_echt(*a, **k)
    ph.pd.read_csv = lies
    if "schnitt_aus" in modus: ph.lesesicht_an = lambda: None
    if "wache1_aus" in modus: ph.wache_zeilen = lambda a: None
    if "wachen_aus" in modus: ph.wache_zeilen = lambda a: None; ph.wache_trades = lambda tr, h: None
    if "schranke_aus" in modus:
        alt = ph.basis.hole_trades; ph.basis.hole_trades = lambda es, a, h=None: alt(es, a)
    try: ph.main()
    finally: json.dump(spur, open(os.path.join(d, "spur.json"), "w"))
def lauf(bot, seed, ab_schnitt, modus="", tags="{}", spaet=False):
    with tempfile.TemporaryDirectory() as d:
        snapshot(bot, d, ab_schnitt, seed[0], spaet, seed[1]); z = os.path.join(d, "ziel"); os.makedirs(z)
        r = subprocess.run([sys.executable, "-B", "-W", "ignore", os.path.abspath(__file__), "--kind", bot, d, z, modus, tags], capture_output=True, text=True,
                           cwd=WURZEL, env=dict(os.environ, TB36_BASE_DIR=d))
        f = os.path.join(z, bot + "_alle_trades.csv"); sp = json.load(open(os.path.join(d, "spur.json"))) if os.path.exists(os.path.join(d, "spur.json")) else {}
        fremd = [x for x in sp.get("gelesen", []) if not x.startswith(os.path.realpath(d) + os.sep)]
        return {"rc": r.returncode, "liste": open(f).read() if os.path.exists(f) else None, "dateien": sorted(os.listdir(z)), "fehler": r.stderr.strip().split("\n")[-1][:170],
                "fremd": fremd, "gelesen": len(sp.get("gelesen", [])), "spaet": sp.get("spaet")}
n = [0, 0]
def pruefe(name, ok, info=""):
    n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + name + (" · " + str(info) if info else ""), flush=True)
    return ok
def tab(liste):
    import io, pandas as pd
    return pd.read_csv(io.StringIO(liste), parse_dates=["entry_time", "exit_time"]) if liste else None
def bot_pruefen(bot):
    import pandas as pd
    S = pd.Timestamp(SCHNITT); seed = voll = None
    def passt(sd):
        v = lauf(bot, sd, True, "schnitt_aus+wachen_aus"); x = tab(v["liste"])
        return (x if v["rc"] == 0 and x is not None and (x["entry_time"] >= S).any() and ((x["entry_time"] < S) & (x["exit_time"] >= S)).any() else None), x
    ok, x0 = passt((169, 0))
    if ok is not None: seed, voll = (169, 0), ok
    elif x0 is not None:   # Bauart R81 (h): Zeitachse versetzen, bis ein Trade ueber den Schnitt offen ist (gleiche Kursfolge)
        t0 = achse(bot, 0); i_s = int(t0.searchsorted(S))
        x0 = x0[x0["symbol"] != "BTCUSDT"].assign(dauer=lambda q: q["exit_time"] - q["entry_time"], spaet=lambda q: q["entry_time"] >= S)
        x0 = x0.sort_values(["spaet", "dauer"], ascending=False)   # zuerst Trades ab dem Schnitt: Achse rueckt nach vorn, die Historie bleibt
        for _, z in x0.head(8).iterrows():
            vs = i_s - (int(t0.searchsorted(z["entry_time"])) + int(t0.searchsorted(z["exit_time"]))) // 2
            ok, _ = passt((169, vs))
            if ok is not None: seed, voll = (169, vs), ok; break
    if not pruefe(bot + ": 0 Snapshot nach R81 (h): Signal ab dem Schnitt und offene Position am Ende von B", seed is not None, "Seed/Versatz %s" % (seed,)): return
    A, B = lauf(bot, seed, True), lauf(bot, seed, False)
    pruefe(bot + ": 1 Probe R86 (d): Listen A = B, rc 0", A["rc"] == B["rc"] == 0 and A["liste"] is not None and A["liste"] == B["liste"], (A["rc"], B["rc"], A["fehler"] if A["rc"] else B["fehler"] if B["rc"] else ""))
    b = tab(B["liste"])
    if b is None: return
    r = lauf(bot, seed, True, "schnitt_aus"); pruefe(bot + ": 2a Schnitt aus -> Wache 1 beisst allein (2)", r["rc"] == 2 and "Zeile ab dem Schnitt" in r["fehler"], (r["rc"], r["fehler"]))
    pruefe(bot + ": 2b Schnitt und Wachen aus -> Listen weichen von B ab, %d Einstiege ab dem Schnitt" % int((voll["entry_time"] >= S).sum()), voll.to_csv(index=False) != b.to_csv(index=False) and (voll["entry_time"] >= S).any())
    r = lauf(bot, seed, True, "schnitt_aus+wache1_aus"); pruefe(bot + ": 2c Schnitt und Wache 1 aus -> Wache 2 beisst allein (2)", r["rc"] == 2 and "Trade mit" in r["fehler"] and "R86 (d)" in r["fehler"], (r["rc"], r["fehler"]))
    gefunden, verletzt, versuche = None, [], 0
    if bot.startswith("elliott"):   # Tatsachennotiz (OHNE_R90G): Tag nach einem alten Einstieg; kein Einstieg davor, alle alten Trades ab dem Tag bleiben
        for sym in ("AAA", "BBB", "CCC"):
            for _, z in b[b["symbol"] == sym].sort_values("entry_time").iterrows():
                if versuche >= 3: break
                tag = z["entry_time"].normalize() + pd.Timedelta(days=1); versuche += 1
                r = lauf(bot, seed, False, "", json.dumps({sym: str(tag.date())})); x = tab(r["liste"])
                if r["rc"] != 0 or x is None: verletzt.append((sym, str(tag.date()), r["rc"], r["fehler"])); continue
                xs = x[x["symbol"] == sym]; alt_ab = b[(b["symbol"] == sym) & (b["entry_time"] >= tag)]
                if (xs["entry_time"].dt.normalize() < tag).any(): verletzt.append((sym, str(tag.date()), "Einstieg davor"))
                if not set(map(tuple, alt_ab[["entry_time", "exit_time"]].astype(str).values)) <= set(map(tuple, xs[["entry_time", "exit_time"]].astype(str).values)):
                    verletzt.append((sym, str(tag.date()), "alter Trade ab Tag fehlt"))
    else:
      for sym in ("AAA", "BBB", "CCC"):
        for _, z in b[b["symbol"] == sym].sort_values("entry_time").iterrows():
            tag = z["entry_time"].normalize() + pd.Timedelta(days=1)
            if not tag < z["exit_time"] or versuche >= 14: continue
            versuche += 1; r = lauf(bot, seed, False, "", json.dumps({sym: str(tag.date())})); x = tab(r["liste"])
            if r["rc"] != 0 or x is None: verletzt.append((sym, str(tag.date()), r["rc"], r["fehler"])); continue
            xs = x[x["symbol"] == sym]
            if (xs["entry_time"].dt.normalize() < tag).any(): verletzt.append((sym, str(tag.date()), "Einstieg davor"))
            alt = set(b[b["symbol"] == sym]["entry_time"]); neu = xs[(xs["entry_time"] >= tag) & (xs["entry_time"] <= z["exit_time"]) & ~xs["entry_time"].isin(alt)]
            if len(neu): gefunden = (sym, str(tag.date()), "alte Position bis %s" % z["exit_time"], "verdraengter Einstieg %s" % neu["entry_time"].min()); break
        if gefunden: break
    if bot in OHNE_R90G:
        pruefe(bot + ": 3a R90 (g) Tatsachennotiz: " + OHNE_R90G[bot], gefunden is None and not verletzt and versuche > 0, "%d Versuche, kein verdraengter Einstieg; kein Einstieg vor dem Tag" % versuche)
    else:
        pruefe(bot + ": 3a R90 (g): Tag in offener Position -> kein Einstieg davor, verdraengter zweiter Einstieg erscheint", gefunden is not None and not verletzt, gefunden or ("%d Versuche" % versuche, verletzt[:2]))
    c0 = b[b["symbol"] == "CCC"]
    if len(c0):
        r = lauf(bot, seed, False, "", json.dumps({"CCC": str(c0["entry_time"].min().date())})); x = tab(r["liste"])
        y = x[x["symbol"] == "CCC"].reset_index(drop=True)[["entry_time", "exit_time"]] if x is not None else None
        pruefe(bot + ": 3b spaetes Symbol CCC gleich mit/ohne Schranke", y is not None and y.equals(c0.reset_index(drop=True)[["entry_time", "exit_time"]]), "%s/%d" % (None if y is None else len(y), len(c0)))
    else: pruefe(bot + ": 3b CCC hat Trades", False)
    a = b[b["symbol"] == "AAA"].sort_values("entry_time"); tag = str((a["entry_time"].iloc[len(a) // 2] + pd.Timedelta(days=1)).date())
    r = lauf(bot, seed, False, "schranke_aus", json.dumps({"AAA": tag})); pruefe(bot + ": 4 Gegenprobe R87 (c): Schranke aus -> Wache 3 beisst (2)", r["rc"] == 2 and "R87 (c)" in r["fehler"], (r["rc"], r["fehler"]))
    r = lauf(bot, seed, True, "", "{}", True); x = tab(r["liste"])
    pruefe(bot + ": 5a R81 (h) Symbol SPAET: rc 0, Tag None, nicht in der Liste", r["rc"] == 0 and r["spaet"] is None and x is not None and "SPAET" not in set(x["symbol"]), (r["rc"], r["spaet"], r["fehler"] if r["rc"] else ""))
    r = lauf(bot, seed, True, "schnitt_aus+wache1_aus", "{}", True); pruefe(bot + ": 5b SPAET mit Zeilen ab dem Schnitt geladen, ohne Tag -> R81 (c) beisst (2)", r["rc"] == 2 and "R81 (c)" in r["fehler"], (r["rc"], r["fehler"]))
    pruefe(bot + ": 6 A9 symbol unveraendert, keine positionen.csv", set(b["symbol"].astype(str)) <= {"AAA", "BBB", "CCC", "BTCUSDT"} and not any("positionen" in f for f in B["dateien"]), B["dateien"])
    offen = voll[(voll["entry_time"] < S) & (voll["exit_time"] >= S)]; art = []
    for _, o in offen.iterrows():
        m = b[(b["symbol"] == o["symbol"]) & (b["entry_time"] == o["entry_time"])]
        art.append("kein Trade" if m.empty else "Ausstieg %s (%s)" % (m["exit_time"].iloc[0], m["result"].iloc[0] if "result" in m else "?"))
    pruefe(bot + ": 7 R86 (c): offene Position am Ende von B (%d) nach der Konvention des Signalpfads, keine leere Ausstiegszeit, rc 0" % len(offen),
           B["rc"] == 0 and len(offen) > 0 and not b["exit_time"].isna().any() and (b["exit_time"] < S).all(), art[:2])
    pruefe(bot + ": 8 nur Dateien des Test-Snapshots gelesen (%d read_csv)" % (A["gelesen"] + B["gelesen"]), not A["fremd"] and not B["fremd"] and A["gelesen"] > 0, (A["fremd"] + B["fremd"])[:2])
if __name__ == "__main__":
    if len(sys.argv) == 7 and sys.argv[1] == "--kind":
        kind(*sys.argv[2:]); sys.exit(0)
    for bot in (sys.argv[1:] or BOTS): bot_pruefen(bot)
    print("Ergebnis: %d von %d bestanden" % (n[1], n[0])); sys.exit(0 if n[0] and n[0] == n[1] else 1)
````

### Anhang E — `kerzen_probe.py` (sha256 `b1cb10f799395f924db957f36bde1cb1c845e85b0512025abbb3c74a9b1711de`)

<!-- DATEI kerzen_probe.py -->
````python
#!/usr/bin/env python3
"""TB-169 (A1): Probe kerzen_je_trade. Die Kerzenzahlen des neuen Codes (research/tb24_haltedauern/positionen_holen.py,
Funktionen kursreihe und kerzen_je_trade unveraendert per ast geladen) gleich der Spalte kerzen in
research/tb24_haltedauern/daten/<bot>_alle_trades.csv (TB-24) - fuer alle Trades, deren Symbol im Snapshot eine Kursreihe hat.
Liest nur open_time der Kursreihen aus dem Snapshot (kein Lauf, kein Bot-Code, data/ nicht gelesen).
Aufruf aus der Repo-Wurzel: python3 -B kerzen_probe.py <SNAPSHOT-ORDNER> [<positionen_holen.py>]   (rc 0 = alle gleich)"""
import ast, os, sys
import pandas as pd
TF = {"elliott_wave": "1h", "t3_supertrend": "4h", "rsi2_crypto": "1d", "turtle_soup_crypto": "1d", "volatility_breakout_crypto": "1d",
      "elliott_wave_stocks": "1d", "rsi2_mean_reversion": "1d", "turtle_soup_stocks": "1d", "volatility_breakout": "1d"}
q = open(sys.argv[2] if len(sys.argv) > 2 else "research/tb24_haltedauern/positionen_holen.py", encoding="utf-8").read()
ns = {"pd": pd}; exec(compile(ast.Module(body=[n for n in ast.parse(q).body if isinstance(n, ast.FunctionDef) and n.name in ("kursreihe", "kerzen_je_trade")], type_ignores=[]), "positionen_holen", "exec"), ns)
snap = sys.argv[1]; fehler = 0; summe = 0
for bot, tf in TF.items():
    tr = pd.read_csv("research/tb24_haltedauern/daten/%s_alle_trades.csv" % bot)
    tr["entry_time"] = pd.to_datetime(tr["entry_time"]); tr["exit_time"] = pd.to_datetime(tr["exit_time"])
    syms = sorted(s for s in tr["symbol"].astype(str).unique() if os.path.exists(os.path.join(snap, "%s_%s.csv" % (s, tf))))
    daten = {s: pd.read_csv(os.path.join(snap, "%s_%s.csv" % (s, tf)), usecols=["open_time"], parse_dates=["open_time"]) for s in syms}
    t = tr[tr["symbol"].astype(str).isin(syms)].copy(); neu = ns["kerzen_je_trade"](t, daten)
    ab = int((neu.astype("Int64") != t["kerzen"].astype("Int64")).fillna(True).sum()); summe += len(t); fehler += ab
    voll = len(t) == len(tr) and len(syms) == tr["symbol"].nunique(); fehler += 0 if voll else 1   # B3: volle Abdeckung, sonst Teilmessung = NEIN
    print("%s %s: Trades in der Liste %d, mit Kursreihe im Snapshot %d (Symbole %d von %d), kerzen gleich %d, abweichend %d"
          % ("ja  " if ab == 0 and len(t) and voll else "NEIN", bot, len(tr), len(t), len(syms), tr["symbol"].nunique(), len(t) - ab, ab))
print("Ergebnis: %d Trades verglichen, %d abweichend oder ohne Kursreihe" % (summe, fehler)); sys.exit(0 if fehler == 0 and summe else 1)
````
