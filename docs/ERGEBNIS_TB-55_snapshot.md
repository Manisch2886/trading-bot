# TB-55 — Den Snapshot ziehen: Ergebnis

**Stand: 19.09.2026** · Repo `Manisch2886/trading-bot`, Basis **`7e48e1f`**
· Auftrag: `MAC_TB-55_snapshot_ziehen.md` (formuliert 18.09.2026)

---

## ⚠️ Ergebnis in einem Satz

**Der Snapshot wurde NICHT gezogen.** Nicht, weil ein Sollwert verfehlt worden
wäre — **der Trockenlauf hat jeden einzelnen getroffen** —, sondern weil die
**Umgebung** abweicht: dieser Lauf fand in der **Cloud** statt, der Auftrag ist
an **Claude Code am Mac** gerichtet und bezeichnet sich selbst als *„der
Mac-Lauf"*.

> **Die Auftragsregel, die hier greift:** *„Bei jeder Abweichung von einem
> Sollwert wird NICHT gezogen, sondern berichtet."* — und:
> *„Ein nicht gezogener Snapshot kostet eine Sitzung; ein falsch gezogener
> kostet den Lauf."*

⭐ **Der Betreiber hat diese Entscheidung am 19.09.2026 ausdrücklich bestätigt**
(Rückfrage vor dem Ziehen, Antwort: *„Nicht ziehen, nur berichten"*).

**`data/` ist unberührt. `snapshots/` existiert nicht. Kein Code geändert,
keine `.gitignore` geändert, kein Registertext geändert.**

---

## 1. Warum nicht gezogen wurde — die gemessenen Abweichungen

Nicht eine einzige Abweichung betrifft eine **Zahl**. Alle vier betreffen die
**Umgebung**, in der die Zahl entstanden ist.

| # | Sollzustand laut Auftrag | Tatsächlich in dieser Sitzung | Gewicht |
|---|---|---|---|
| 1 | ⭐ Interpreter **durchgehend `trading-env/bin/python3`** | `trading-env/` **existiert hier nicht**. Benutzt: `/usr/local/bin/python3`, **Python 3.11.15** | ⚠️ Der Mac fährt **3.9.6** (`docs/UMGEBUNGEN.md`). CLAUDE.md: *„Grün in der Cloud heisst strukturell nicht grün auf dem Mac."* |
| 2 | Schritt 0: **neun Datenbanken** quersummen **und kopieren**, *„nur auf diesem Mac, nicht neu berechenbar"* | **Keine einzige `*.db` vorhanden** — sie sind per `.gitignore` gitignoriert und liegen ausschliesslich auf dem Mac | ⚠️ Die **Sicherung vor dem Ziehen ist hier strukturell nicht ausführbar** |
| 3 | Zweig **`main`**, kein eigener Zweig, kein Pull Request | Sitzungsmandat dieser Cloud-Sitzung: Zweig **`claude/new-session-9qrb42`**, Push auf `main` ohne ausdrückliche Erlaubnis untersagt | Der Push-Ziel-Widerspruch wäre beim Ziehen sofort scharf geworden (Schritt 4) |
| 4 | *„**Kein Mac-Testauftrag** — diese Aufgabe **ist** der Mac-Lauf."* | Dies ist **kein** Mac-Lauf | ⚠️ Der Auftrag definiert seinen eigenen Ausführungsort |

### Was gegen diese Abweichungen spricht — ehrlich benannt

Es wäre unredlich, die Gegenargumente zu verschweigen, denn sie sind stark:

- Der Snapshot-Inhalt ist eine **reine Funktion von `data/` plus zwei
  Konfigurationsdateien**. Alle 225 sind **versioniert**; der Arbeitsbaum ist
  sauber und steht auf demselben Commit wie `origin/main`.
- `.gitattributes` **existiert nicht**, es findet also keine
  Zeilenenden-Umschreibung statt — die Dateien sind byteweise dieselben wie im
  Commit.
- **Der `datenstand_hash` trifft den verankerten Registerwert exakt.** Genau
  das ist der Beleg, dass der hier sichtbare Bestand *der registrierte* ist.
- `shared/snapshot.py`, `research/vorregistrierung/herkunft.py` und
  `shared/zeitabdeckung.py` benutzen **ausschliesslich die
  Standardbibliothek** — die Hash-Rechnung hängt nicht an `pandas`.

⭐ **Daraus folgt: ein Zug auf dem Mac wird sehr wahrscheinlich denselben
`snapshot_hash` ergeben** (siehe Abschnitt 3). Es folgt aber **nicht**, dass
dieser Lauf ihn ziehen durfte — die Absicherung aus Schritt 0 (die neun
Datenbanken) und der vorgeschriebene Interpreter fehlen hier, und der Auftrag
lässt für den Zweifelsfall **keinen** Ermessensspielraum.

---

## 2. Schritt 1 — der Trockenlauf, Sollwert für Sollwert

```
python3 shared/snapshot.py --quelle data
```

⭐ **Jeder einzelne Sollwert getroffen. Kein einziger verfehlt.**

| Sollwert laut Auftrag | Soll | Gemessen | |
|---|---|---|---|
| `datenstand_hash` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | ✅ |
| Kursdateien | 223 | **223** | ✅ |
| Dateien gesamt | 225 | **225** | ✅ |
| Weitere Eingabe 1 | `config/sp500_top150.txt` | `config/sp500_top150.txt` | ✅ |
| Weitere Eingabe 2 | `config/top25_symbols.txt` | `config/top25_symbols.txt` | ✅ |
| Weitere Eingabe 3 | *darf es nicht geben* | **keine dritte** | ✅ |
| Teilkerzen | 36 Datei(en) mit Befund (223 geprüft) | **36 Befunde, 223 geprüft** | ✅ |
| davon zugelassen | ⭐ 36, Verweis auf *Abschnitt 17.3* | **36**, `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3` | ✅ |
| `NICHT zugelassen` | ⚠️ **kommt NICHT vor** | **kommt nicht vor** (`nicht_zugelassen == []`; `grep -c` auf der Ausgabe: **0**) | ✅ |
| Rückgabewert | 0 | **0** | ✅ |
| Schlusszeile | `TROCKENLAUF - nichts kopiert.` | `TROCKENLAUF - nichts kopiert. Mit --ziehen wirklich ziehen.` | ✅ |
| Standardfehlerkanal | — | **0 Byte** | ✅ |

### Die 36 Befunde, an ihrer Quelle nachgezählt

Nicht aus der Bildschirmausgabe abgeschrieben, sondern aus
`shared/snapshot.py::teilkerzen` gelesen:

| Feld | Wert |
|---|---|
| `dateien_geprueft` | **223** |
| `befunde` | **36** |
| `zugelassen_anzahl` | **36** |
| `zugelassen_dateien` | **36** (36 eindeutige Dateinamen) |
| ⚠️ `nicht_zugelassen` | **`[]` — leer** |
| Arten der 36 Befunde | ⭐ **`rand_erste`: 36** — kein einziges `rand_letzte` |
| Urteile der 36 Befunde | ⭐ **`abgeleitete_teilkerze`: 36** — Bedingung (c) bei allen belegt |
| `ausfuehrbar` | `True` |
| `zieht_trotz_befunden` | `True` |
| `werkzeug` | `shared/zeitabdeckung.py::pruefe_ordner` |
| Herkunft der Erlaubnis | Registertext **5a, Zusatz**, `docs/VORREGISTRIERUNG_neuselektion.md, Abschnitt 17.3`, beschlossen **18.09.2026**, umgesetzt in `shared/snapshot.py::_zulassung` (TB-49) |

⭐ **Damit ist die Ausnahme aus 17.3 vollständig gedeckt:** alle drei
Bedingungen (a) `rand_erste`, (b) erste Kerze, (c) nachweisliches Aggregat der
feineren Kerzen treffen bei **allen 36** zu. Es gibt **keinen** Befund, der
ohne die Ausnahme durchgerutscht wäre, und **keinen**, den die Ausnahme nicht
deckt.

---

## 3. Der `snapshot_hash` — was er wäre, und was er nicht ist

```
63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
```

⚠️⚠️ **Diese Zahl geht NICHT ins Register.** Sie ist der Name, den der Ordner
**bekommen hätte**, berechnet vom Trockenlauf über die 225 Dateien. **Es wurde
nichts gezogen, also existiert dieser Snapshot nicht.**

⭐ **Wozu sie trotzdem taugt:** als **Vorhersage, gegen die der Mac-Lauf
gerechnet werden kann.** Zieht der Mac aus demselben Commit und meldet er
denselben Namen, ist damit zugleich **F1b/Q2 belegt** — die Reproduzierbarkeit
auf einer zweiten Maschine, und zwar *bevor* der Snapshot im Repo liegt statt
danach. Weicht er ab, ist das ein **Befund von erheblichem Gewicht**, und dann
ist gut, dass hier nichts gezogen wurde.

| Grösse | Wert | Quelle |
|---|---|---|
| `snapshot_hash` (vorhergesagt) | `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` | Trockenlauf |
| `datenstand_hash` | `d9449faf…a995f84` | `herkunft.py::datenstand`, direkt aufgerufen |
| Kursdateien / gesamt | 223 / 225 | Trockenlauf |
| `zugelassene_befunde_anzahl` | 36, Abschnitt 17.3 | `snapshot.py::teilkerzen` |
| Zeitpunkt (UTC) / Bytes gesamt | ⚠️ **nicht vorhanden** | stünden im `MANIFEST.json` — das entsteht erst beim Ziehen |

---

## 4. Der Datenstand — dreimal gemessen, dreimal derselbe

| # | Wann | Verfahren | Ergebnis |
|---|---|---|---|
| 1 | vor dem Trockenlauf | `snapshot.py --nur-hash` | `d9449faf…a995f84` · **223** |
| 2 | direkt an der Quelle | `herkunft.py::datenstand('data')` importiert und aufgerufen | `d9449faf…a995f84` · **223** |
| 3 | am Ende der Sitzung | `snapshot.py --nur-hash` | `d9449faf…a995f84` · **223** |

⭐ **Dreimal identisch, und Messung 2 rechnet an der registrierten Funktion
selbst** — nicht über das Werkzeug, das sie benutzt. `data/` hat sich nicht
bewegt: `git status --porcelain -- data` ist **leer**.

---

## 5. Die übrigen Prüfungen

| Prüfung | Soll | Ergebnis |
|---|---|---|
| Bestehender Snapshot in `snapshots/` | darf nicht existieren | **existiert nicht** |
| Bestehender Snapshot in `data/snapshots/` | darf nicht existieren | **existiert nicht** |
| `git status --short` vorher | leer | **leer** |
| Zweig / Stand | `main`, aktuell mit `origin` | `main` = `origin/main` = **`7e48e1f`** |
| `data/` versioniert und vollständig | — | `git ls-files data` = **223**, `find data -type f` = **223** — deckungsgleich |
| Registerprüfer **vorher** | KEIN BEFUND | **KEIN BEFUND**, Rückgabewert **0** |
| Registerprüfer **nachher** | KEIN BEFUND | **KEIN BEFUND** |
| Sperrliste unberührt | — | **unberührt** (nichts geändert ausser diesem Dokument) |
| `shared/snapshot.py`, `shared/paths.py` | nicht ändern | **nicht geändert** |
| Netzabruf / Order / Bot-Lauf | keiner | **keiner** |
| Secrets | nie `cat` | **kein `cat` auf `config/email_config.py` oder `.env`** |

---

## 6. `.gitignore` — musste nicht angefasst werden

⭐ **Nein.** Gemessen, nicht vermutet:

```
git check-ignore -v snapshots/                       -> Rückgabewert 1
git check-ignore -v snapshots/<hash>/AAPL_1d.csv     -> Rückgabewert 1
```

**Rückgabewert 1 heisst: von keinem Muster erfasst.** `snapshots/` ist in
`.gitignore` nicht vorgesehen — weder als Treffer noch als Ausnahme. **Es ist
also keine Änderung nötig, und es wurde keine vorgenommen.**

⚠️ **Zur Vorsicht mitgeprüft:** das bestehende Muster `data_sicherung/` greift
nicht auf `snapshots/`, und `*.db`/`*.log` können in einem Ordner aus reinen
`.csv`- und `.txt`-Dateien nicht zuschlagen.

---

## 7. Der Repo-Zuwachs — Ausgangswert festgehalten, Messung offen

| | Wert |
|---|---|
| `size-pack` **vor** der Sitzung | **114.77 MiB** (`in-pack`: 2496 Objekte) |
| `size-pack` **nach** der Sitzung | **114.77 MiB** — unverändert |
| Erwartung aus TB-46 | **+0,001 %** |
| ⚠️ Tatsächlicher Zuwachs durch den Snapshot | **nicht messbar — es wurde nichts gezogen** |

⭐ **Der Ausgangswert ist damit für den Mac-Lauf festgehalten.** Bleibt der
Zuwachs dort nahe +0,001 %, hat git die Inhalte als gleich erkannt; ein
deutlich grösserer Wert wäre nach Auftrag ein Befund.

---

## 8. `git diff --numstat` für das Committete

Committet wird in dieser Sitzung **ausschliesslich dieses Ergebnisdokument**.
Die 225 Snapshot-Dateien sind **nicht** dabei, weil sie nicht entstanden sind.

⭐ **Entfernte Zeilen: null** — eine neue Datei entfernt nichts.

---

## 9. Die Fragen des Auftrags, der Reihe nach

**⭐ Wie lautet der `snapshot_hash`?**
> `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` —
> ⚠️ **als Vorhersage des Trockenlaufs, nicht als gezogener Snapshot.**
> **Diese Zahl geht nicht ins Register.**

**Hat der Trockenlauf jeden Sollwert getroffen — einzeln aufgeführt?**
> **Ja — jeder einzelne.** Vollständig aufgeführt in Abschnitt 2. Kein einziger verfehlt, auch die
> Dateizahl nicht.

**Sind die 225 Dateien byteweise gegen die Quelle geprüft, und meldet die
Nachprüfung `UNVERAENDERT`?**
> ⚠️ **Nein — beides konnte nicht stattfinden.** Die byteweise Prüfung führt
> `--ziehen` beim Kopieren durch, und `--pruefen` setzt einen vorhandenen
> Snapshot voraus. Es wurde nichts kopiert, also gibt es nichts nachzuprüfen.
> **Dass diese Frage offen bleibt, ist die unmittelbare Folge des
> Nicht-Ziehens und kein Nebenbefund.**

**⚠️ Welche zwei Nicht-Kursdateien liegen im Snapshot?**
> `config/sp500_top150.txt` und `config/top25_symbols.txt` — **genau diese
> zwei, keine dritte.** Sie stehen als **Liste** (`EINGABEN` in
> `shared/snapshot.py`), nicht als Regel, und wären im Manifest mitgeführt
> worden.

**Datenstand dreimal gemessen — dreimal derselbe?**
> **Ja.** Dreimal `d9449faf…a995f84` bei 223 Dateien; siehe Abschnitt 4.

**⚠️ Musste `.gitignore` geändert werden?**
> **Nein.** `snapshots/` wird von keinem Muster erfasst — mit
> `git check-ignore` gemessen, Rückgabewert 1. Abschnitt 6.

**⭐ Wie gross ist der gemessene Zuwachs des Repos wirklich?**
> **Nicht messbar.** Ausgangswert **114.77 MiB** ist festgehalten; die Messung
> gehört zum Mac-Lauf. Abschnitt 7.

**Welche Beobachtungen hast du gemacht, die du NICHT ausgeführt hast?**
> Abschnitt 10.

---

## 10. Beobachtungen, die ich NICHT ausgeführt habe

1. ⚠️ **Die Hash-Rechnung steht zeichengleich zweimal im Repo.**
   `shared/snapshot.py` nennt es selbst im Kopf: ein Duplikat von
   `herkunft.py::datenstand` liegt in
   `research/registernachtrag_tb41/pruefe_register.py:319`. Heute liefern
   beide dasselbe — **wer eines ändert, merkt den Unterschied nicht.**
   *Nicht angefasst:* beide Dateien sind gemessen bzw. Prüfwerkzeug, und der
   Auftrag verbietet Codeänderungen.

2. ⭐ **Der Registerprüfer konnte seinen eigenen Trockenlauf-Beleg hier nicht
   rechnen.** Er meldet
   `Quelle beleg: dokument (Trockenlauf nicht lauffaehig: ModuleNotFoundError:
   No module named 'pandas')` und fällt auf das Dokument zurück — **das
   Urteil KEIN BEFUND bleibt gültig, aber ein Teil der Kette ist hier
   Papier statt Messung.** Auf dem Mac mit `trading-env` fällt das weg.
   *Nichts installiert* — das hätte die Umgebung verändert, die der Auftrag
   festlegt.

3. ⚠️ **Die neun Datenbanken existieren in der Cloud nicht** (`*.db` ist
   gitignoriert). Die Schutzmassnahme aus Schritt 0 — Quersummen **und**
   Kopie vor dem Ziehen — ist hier **strukturell nicht herstellbar**, nicht
   bloss übersprungen. Für einen Lauf, der `data/` nur liest, ist das
   folgenlos; als Absicherung fehlt sie trotzdem.

4. **Der vorhergesagte `snapshot_hash` ist eine kostenlose Gegenprobe für
   F1b/Q2.** Er liegt vor, **bevor** der Mac zieht — die Reproduktion auf
   einer zweiten Maschine lässt sich damit prüfen, ohne dass der Snapshot
   schon im Repo liegen muss. *Nicht ins Register eingetragen*, nicht als
   Beleg verbucht: Registertexte werden in dieser Aufgabe nicht geändert.

5. **`data/` enthält keine Unterordner** — `find` und `git ls-files` liefern
   beide exakt 223 Dateien. Die im Modulkopf beschriebene Falle („ein
   `data/snapshots/` innerhalb von `data/` zählt der Hash nicht mit") ist
   heute nicht scharf. ⚠️ **Sie würde es, wenn jemand das Standardziel von
   `--ziel` auf `data/snapshots` legte** — das Werkzeug bricht dann zwar ab
   („Ziel liegt innerhalb der Quelle"), aber die Falle ist eine Option
   entfernt.

6. **Nicht eingerichtet:** kein Datencron (T46.4), kein Mac-Testauftrag, kein
   Registereintrag, kein zweiter Snapshot, keine Übergehen-Flagge.

---

## 11. Was der Mac-Lauf noch zu tun hat

⚠️ **Der Auftrag `MAC_TB-55_snapshot_ziehen.md` bleibt unverändert gültig und
ist unverbraucht.** Er kann Wort für Wort auf dem Mac ausgeführt werden.
Zwei Dinge nimmt diese Sitzung ihm ab:

- **Der Trockenlauf ist inhaltlich vorab bestätigt** — sämtliche Sollwerte
  treffen auf dem Bestand des Commits `7e48e1f`.
- ⭐ **Der zu erwartende Name ist bekannt:** `63e4b6c8…3cb2ceb2`. **Meldet der
  Mac einen anderen, ist vor dem Ziehen zu klären, warum** — dann hat einer
  der beiden Rechner einen anderen Bestand, und das ist genau die Frage, die
  hinterher niemand mehr stellen kann.

⚠️ **Auf dem Mac gilt Schritt 0 vollständig**, einschliesslich der neun
Datenbanken — **hier war er nicht herstellbar.**

---

## In einfacher Sprache

**Was zu tun war:** eine eingefrorene Kopie aller Kursdaten anlegen — die
Grundlage, auf der später der Auswahllauf rechnet.

**Was geschehen ist:** Die Kopie wurde **nicht** angelegt. Alle Vorprüfungen
sind durchgelaufen und **alle waren in Ordnung** — der Kennwert der Daten
stimmt auf die Stelle, es sind genau 223 Kursdateien und genau zwei weitere
Dateien, und alle 36 Auffälligkeiten sind solche, die ausdrücklich erlaubt
sind.

**Warum trotzdem nicht:** Dieser Lauf fand auf dem falschen Rechner statt. Der
Auftrag ist für den Mac des Betreibers geschrieben und sagt das auch von sich
selbst. In der Cloud fehlen zwei Dinge: das vorgeschriebene Python und die
neun Datenbanken, die vorher gesichert werden sollen. **Und der Auftrag sagt
für genau diesen Fall: dann lieber gar nicht — und berichten.**

**Warum das kein Verlust ist:** Die Kopie lässt sich **nur einmal** anlegen.
Wird sie später noch einmal gezogen, fängt alles von vorn an. Eine
ausgelassene Sitzung kostet eine Sitzung. Eine falsch angelegte Kopie kostet
den ganzen Lauf.

**Was diese Sitzung wert war:** Der Name, den die Kopie tragen wird, steht
schon fest: er beginnt mit `63e4b6c8`. **Zieht der Mac die Kopie und nennt sie
genauso, ist damit nebenbei bewiesen, dass zwei verschiedene Rechner aus
denselben Daten dasselbe Ergebnis bekommen** — eine Prüfung, die sonst
aufwendig gewesen wäre. **Nennt er sie anders, ist etwas grundlegend falsch —
und dann ist es gut, dass hier nichts gezogen wurde.**
