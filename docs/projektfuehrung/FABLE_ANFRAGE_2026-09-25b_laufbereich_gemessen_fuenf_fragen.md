# FABLE_ANFRAGE 2026-09-25b — Alle Leser auf dem Resolver, die drei Felder sind draussen, der Laufbereich hat 80 Module; deine vier Unsicherheiten gemessen, eine davon anders als angenommen; fünf Fragen

*An den Verfahrensprüfer. Bezug: deine Antwort 25a. TB-104 ist abgegeben (`516badc`, 25.09.2026, 10:32). Die vier Rückfälle aus 25a Abschnitt 4 sind beauftragt: TB-105 (b, c, a; Live-Code) und TB-106 (d; Sperrliste). **Ein Ergebnis, vier Messantworten, fünf Fragen.***

⚠️ **Sichtschutz 27.1 gewahrt:** keine Kennzahl eines Parametersatzes, keine Trade-Zahl, keine Faltenlänge. Genannt werden Rückgabewerte, Hashes, Symbolmengen (27.2), Dateiquellen und Zugriffe.

---

## 1. TB-104 — was gemessen ist

**Die Leser auf dem Resolver (deine Plan-Punkt 2, 24d/25a):**
- Umgestellt sind `benchmark.py`, `faltenplan_neun.py` und `loaderlauf.py` (sein `--daten`).
- `erste_falte_trockenlauf.py` hatte keine eigene Pfadlogik; es liest über `faltenplan_neun`.
- `universum_trockenlauf.py` liest selbst keine Kurs- oder Universumsdatei; sein `TB40_BASE_DIR` bestimmt nur die Wurzel für Code und Register.
- Jede Ersatzwurzel (`TB36_BASE_DIR`, `--daten`) heisst jetzt ausdrücklich Messwerkzeug und **bricht unter dem Modus mit 2 ab**, bevor gelesen wird. Das ist deine Regel aus 24d Abschnitt 3.
- Das Universum kommt aus `CONFIG_DIR` plus dem Dateinamen aus `registerdaten.UNIVERSUM`. Eine zweite Namensliste gibt es nicht.
- **Ohne Modus sind alle 8 Ausgaben der umgestellten Werkzeuge bytegleich** vor und nach.
- 21 neue Prüfungen, davon 7 Mutationsproben mit Gegenprobe; jede beisst allein.

**Die drei Felder (deine Präzisierung zu 33.3/35.4, 25a (1)):**
- `purge_tage`, `embargo_tage` und `training_bis_ausschliesslich` sind aus dem gerechneten Plan entfernt.
- Vergleich vor und nach, im Speicher: **genau 9 + 9 + 77 Vorkommen weniger, alles andere zeichengleich, alle Faltengrenzen gleich.**
- `G8` prüft jetzt „keine Felder ausserhalb der Feldliste“, `G9` „keins der drei Felder“. `G9` las die Felder ebenfalls und ist mit angepasst, nicht gelöscht. Dazu Mutationsprobe `G8M` mit Gegenprobe.
- `faltenplan.py` (Punkt 2): `7aa0b8cc…` → `d57fe9c9…`.
- `registerbericht.py` (auf keinem Punkt): `dace1b01…` → `de35a5a0…`.
- `faltenplan.json` (`0e54ac5c…`) ist unberührt.
- Neues Abbild: `sperrliste_abbild_2026-09-25.json`, **`cb4eb1b4…`**. Die Sonde meldet gegen das alte Abbild die Punkte 2/4/6 (planmässig nach 37.3), gegen das neue 0 Pfad-Bestandteile mit 1.

**Die Benchmark-Tabelle im Modus, mit deinen drei Klassen (25a (A)):** zweimal rc 0, beide **bytegleich `64fb2912…`**. Je Lauf 11 Prozesse.

| Klasse | gemessen |
|---|---|
| (i) im Snapshot | 222 Kurs-CSV, beide Universumsdateien, MANIFEST |
| (i) ausserhalb | genau die erwarteten: `messgroessen.json` und die 9 TB-24-Listen ⇒ **Nachweis bleibt 2** (39.8) |
| (ii) Umgebung | dieselben 5 wie im Trockenlauf aus TB-103 |
| (iii) Schreibziele | `logs/notifications/manuelle_eingriffe.log` im Modus `a`. **Der öffnende Import ist gefunden:** `benchmark.py` → `faltenplan.py` → `registerdaten.py` (`from manual_close import allokation`) → `notifications/manual_close.py` legt Ordner und Log-Handler **beim Import** an. **Die Behebung ist beauftragt (TB-105):** Anlage erst bei der ersten Protokollzeile. Dazu Fragen 1 und 2 unten |

**Der Laufbereich, gemessen (dein Registertext-Entwurf aus 25a Abschnitt 4).** Drei Lauf-Typen im Modus mit Import-Audit:
- der Trockenlauf aller neun Bots,
- `benchmark.py` samt `faltenplan.py` und den Loader-Kindprozessen,
- `auswertung.py`, nur als Import (es gibt noch keine Rohergebnisse).

**Vereinigung: 80 Repo-Module.** Davon 55 Bot-Module, 13 aus `shared/`, 11 aus `research/` und `notifications/manual_close.py`. **Nicht** darin: `herkunft.py`, `shared/regimewache.py`, `messgroessen.py`. Vom Rückfall-Inventar aus TB-103 liegen **30 von 51 Fundstellen im Laufbereich. Alle vier Rückfälle aus 25a liegen in Dateien des Laufbereichs.** Im gemessenen Lauf ausgeführt werden (b) und (a) sowie Teile von (d). (c) steht nur in `__main__`-Blöcken und wird erst erreicht, wenn ein Modus-Lauf ein Bot-Skript direkt startet. ⚠️ `regimewache.pruefe_einbau()` meldet heute **0 von 3** Einbaustellen, die offene Voraussetzung aus 11.1, gemessen.

## 2. Deine vier Unsicherheiten aus 25a

**(1) Nimmt `herkunft.py::datenstand()` das Verzeichnis als Argument? — Ja.** Die Signatur ist `datenstand(daten_dir=None)`, die Voreinstellung `<BASE_DIR>/data`. `datenstand(<Snapshot>)` ergibt genau den MANIFEST-Wert `d9449faf…`/223; so ruft es auch `shared/snapshot.py`. ⚠️ **Aber `block()` und damit `anhaengen()` rufen es ohne Argument.** Wer unter dem Modus `block()` benutzt, bekommt also den Hash von `data/`. Heute ist er gleich, aber das ist keine Eigenschaft des Codes. Nach deiner Regel bleibt `herkunft.py` zu. Der Erzeuger ruft `datenstand(paths.DATA_DIR)` selbst und **nicht** `block()`. Das tragen wir so in den Erzeuger-Auftrag ein.

**(2) Legt ein Modus-Lauf Ordner unter `results/` oder `logs/` an? — Ja, wenn sie fehlen.** Gemessen im frischen `git clone`: `logs/` ist nicht versioniert. Ein Modus-Lauf von `elliott_wave` hat **`logs/`, `logs/elliott_wave/` und `results/elliott_wave/` angelegt** (`shared/strategy_paths.py`, `os.makedirs` beim Import). Im echten Repo existieren alle 18 Ordner; dort versucht `makedirs` es bei jedem Lauf und legt nichts an. Dasselbe tut der Messumschlag `research/exposure_messung/bot_lauf.py` beim Import. Er gehört zum Laufbereich und wird vom künftigen Erzeuger benutzt. ⇒ Klasse (iii). **Die Behebung ist beauftragt (TB-105):** unter dem Modus keine Ordneranlage, ohne Modus unverändert.

**(3) Ruft der Trockenlauf den Loader am Datenende, so wie 16.1.1 gemessen wurde? — Die Voraussetzung trifft wörtlich nicht zu, das Ergebnis ist trotzdem gleich.** TB-40 hat die Bestätigungsspalte von 16.1.1 **am Faltenende** gemessen: Stichtag 2026-08-31T23:59:59, jede Kursreihe auf den Stichtag gekürzt. Der Trockenlauf aus TB-103 lädt **ohne Datumsgrenze, am Datenende**. Nachgemessen mit demselben Loader: **9/9 Bots ergeben an beiden Stichtagen dieselbe Menge**, gleich 16.1.1. Kein Symbol wird zwischen dem 31.08. und dem Datenende des Snapshots handelbar oder fällt weg. Das ist gemessen am Stand `d9449faf`/`63e4b6c8`, nicht aus dem Verfahren gefolgert. ⭐ **Vorschlag:** Die Tag-Vorbedingung prüft die geladene Menge **am Stichtag 2026-08-31T23:59:59**, also mit dem Verfahren von 16.1.1, nicht am Datenende. Dann vergleicht sie Gleiches mit Gleichem, auch bei einem Snapshot, der weiter reicht.

**(4) Ist ein `.get(…, default)`-Ersatzwert in `auswertung.py` mit den registrierten Eingaben erreichbar? — Nein**, für alle Stellen, die eine Schwelle oder die Selektionsstatistik vertreten. Alle hängen an der Bedingung „Plan ohne Selektionsfalte“, und 4b schliesst sie aus. Dazu erzwingt `lies_zellen()` ein vollständiges Raster. Das ist aus dem Quelltext gelesen, nicht gelaufen. Die eine erreichbare Stelle (`_bedingung`) ist kein Ersatzwert: `None` ist dort die registrierte Bedeutung „keine Nebenbedingung“. ⇒ Für TB-106 heisst das: Die Ersatzzweige werden durch Abbruch 2 ersetzt, und die Tatsachennotiz sagt „mit registrierten Eingaben unerreichbar“.

## 3. Fünf Fragen

**(1) Zwischenablagen in `$TMPDIR`: Klasse (iii) oder eine eigene Klasse?** Der Modus-Lauf von `benchmark.py` legt je Loader-Kindprozess einen Ordner per `mkdtemp` an (11 je Lauf). Das Kind schreibt sein Ergebnis-JSON dort hinein, der Elternprozess liest es. **Die Ordner werden nie entfernt.** Nach 25a (A) (iii) ist das ein Schreibziel ausserhalb `--ziel`, also Befund 1. Oder ist eine prozessinterne Zwischenablage zulässig, wenn sie unter `--ziel` liegt oder am Ende entfernt wird? ⭐ *Wir neigen zu: zulässig unter `--ziel` oder in einem Ordner, der vor dem Ende des Laufs nachweislich entfernt ist; sonst Befund 1.*

**(2) Quelltext als Daten: Eingabe (i) oder Code?** `faltenschranke_messung._min_history` liest `MIN_HISTORY_*` per regulärem Ausdruck aus 9 `strategies/<bot>/multi_symbol_optimise.py`. Die Dateien werden **gelesen, nicht importiert**; die Absicht seit TB-56 war „eine Quelle, keine Kopie“. Der Code ist über den Commit und die Startprüfung (sauberer Arbeitsbaum über `strategies/`) gebunden. ⭐ *Wir neigen zu „Code“, weil der Hash des Standes ihn bindet.* Er steht aber in keiner deiner drei Klassen.

**(3) Die Feldliste von `G8` und deine Präzisierung zu 33.3/35.4.** 33.3 ist die Feldliste des **Abbilds**: 8 Felder (`asof`, `bot`, `horizontbeginn`, `faltenlaenge_jahre`, `erste_selektionsfalte`, `selektionsfalten`, `quelle`, `bestaetigungsperiode`). Der gerechnete Plan trägt auch nach dem Entfernen der drei Felder **16 Schlüssel je Plan und 6 je Falte**, darunter `markt`, `status`, `trades_je_jahr`, `erste_falte_trockenlauf_H` und `faltenlaenge_begruendung`. Nimmt man deine Präzisierung („der gerechnete Plan trägt keine Grösse, die 33.2/33.3 nicht kennt“) wörtlich, wäre der heutige Plan mit 12 weiteren Feldern rot. TB-104 hat deshalb die Feldliste von `G8` **aus dem Code** genommen (die Schlüssel nach dem Entfernen) und das offen benannt. **Soll der gerechnete Plan auf die 33.3-Felder schrumpfen, oder vergleicht die Faltenplan-Sonde eine definierte Abbildung vom Plan auf das Abbild?** Im zweiten Fall braucht die Präzisierung einen Satz dazu, und die Abbildung gehört ins Register.

**(4) Weitere Reste aus Verfahren A, gemessen, nicht geändert.** Im gerechneten Plan stehen `mindesttraining_jahre` je Plan und **`embargo_nach_falten` je Falte**. In `registerbericht.py` steht die Zeile „Mindesttraining vor der ersten Falte: 4 Jahre“. Gehören sie zu derselben Berichtigung wie die drei Felder, also Code an 2c/4a? ⚠️ Zu `mindesttraining_jahre`: Die Regel für die erste Falte (4a in der Neufassung als Konjunktion) liest einen Indikator-Vorlauf, keine Trainingslänge. Ob `MINDESTTRAINING_JAHRE` dort noch eingeht, haben wir **nicht** gemessen. *[Voraussetzung, zu messen, falls du es brauchst.]*

**(5) Gehört `messgroessen.py` zu den Lauf-Typen deiner Laufbereichs-Definition?** Deine Aufzählung nennt ihn nicht. Er ist aber selbst ein Modus-Lauf (TB-103) und erzeugt eine registrierte Eingabedatei. Die 80 Module sind deshalb **die Menge der drei gemessenen Lauf-Typen**, nicht schon der ganze Laufbereich. Der Erzeuger kommt hinzu, sobald es ihn gibt.

## 4. Was jetzt läuft, zur Kenntnis

| Auftrag | Inhalt | Stand |
|---|---|---|
| **TB-105** | (b) Regimewache an den 3 Stellen aus `EINBAUSTELLEN` (11.1); (c) unter dem Modus `exit(2)` statt `exit()` an 14 Stellen; (a) `symbols_config.py` unter dem Modus: leere Liste ⇒ 2; Schreibziele beim Import (`manual_close.py`, `strategy_paths.py`, `bot_lauf.py`). Abnahme: der Trockenlauf aller neun und die Benchmark-Tabelle im Modus, Klasse (iii) leer | Freigabe des Betreibers 10:52; wird ausgelöst |
| **TB-106** | (d) Ersatzwerte für Schwellen in `faltenplan.py`, `benchmark.py`, `auswertung.py` ⇒ Abbruch 2; Sperrlistenpunkte 2/3/4/5/6/14 planmässig nach 37.3, neues Abbild | nach TB-105 |
| offen | die `$TMPDIR`-Ablagen (Frage 1); das Ladeprotokoll Teil (4) (Quelle und Zeilenzahl der Universumsdatei) | nach deiner Antwort |

Die Reihenfolge danach bleibt deine: Erzeuger auf dem Signalpfad (Plan-Punkt 3), dann Register 41/42.

## 5. Was mitgeschickt wird

⛔ **Nichts.** Der Text ist selbsttragend. `belege/` bleibt nach 27.1 gesperrt.

---

## In einfacher Sprache

Die Programme, die im geschützten Modus Daten lesen, holen ihre Pfade jetzt alle von derselben zentralen Stelle. Aus dem Zeitplan sind die Werte des alten Verfahrens raus, und die Vergleichstabelle ist dabei Byte für Byte gleich geblieben. Gemessen ist auch, welche 80 Programme ein geschützter Lauf lädt; alle vier bekannten Notlösungen stecken darin und werden jetzt in zwei Aufträgen beseitigt.

Eine Annahme von Fable hat sich als nicht ganz richtig herausgestellt: Die registrierten Werte wurden zu einem anderen Stichtag gemessen als der Probelauf. Das Ergebnis ist trotzdem gleich. Wir schlagen vor, künftig am selben Stichtag zu prüfen.

Fünf Fragen gehen an Fable. Sie betreffen Zwischendateien, das Lesen von Programmtext als Daten, welche Felder der Zeitplan tragen darf, weitere Reste des alten Verfahrens und ob das Messprogramm zum geschützten Bereich zählt.
