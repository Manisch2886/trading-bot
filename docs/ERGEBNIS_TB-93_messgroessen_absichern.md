# TB-93 — Ergebnis: `messgroessen.py` nach 36.1 abgesichert — ⛔ Determinismusnachweis NICHT erbracht (Befund), Ursache ausgemessen

**Sitzungstitel:** `TB-93` · **Stand:** 23.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-93_messgroessen_absichern.md` · **Belege:** `docs/belege/TB-93/`
**Eingang:** `02f2574` · Commits: `b11a6f6` (Schritt 0, Arbeitsbaum des steuernden
Chats), Abgabe-Commit (Nachweisdatei, Belege, dieses Dokument, Journalblock CT).
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6).

⛔⛔ **Block B ergibt einen BEFUND: Der Lauf auf einen neuen Pfad reproduziert
`ergebnisse/messgroessen.json` NICHT bytegleich.** Nach Auftrag Abschnitt 6
Punkt 5 ist das kein Abbruch, sondern eine Meldung, und **Block C entfällt**
(keine Tatsachennotiz 37.3, kein Sondenlauf). Nichts wurde nachgebessert.

⭐⭐ **Die Ursache ist ausgemessen, und sie liegt nicht im Code.** Die
eingefrorene Datei wurde am 14.09. (`a2fcf01`) auf Kursdaten gerechnet, die
TB-34 am 15.09. (`90e3cbd`) für alle Krypto-Symbole neu geladen hat. Derselbe
Code ergibt auf den Eingaben von `a2fcf01` **bytegleich** `2a9b9166…`
(Gegenprobe, Abschnitt 3.3). Abweichend sind genau die Krypto-Werte, 48 von
127 Blattwerten; alle Aktien-, Kosten-, Haltedauer-, Universums- und
Frequenzwerte sind gleich.

**Block A:** Alle sechs Nachmessungen stimmen mit der Vormessung überein (A-N6
wie erwartet nicht messbar, mit einem neuen Nebenbefund). Kein
Abbruchkriterium 1–4 hat gegriffen.

---

## 1. Schritt 0 — committen

| | |
|---|---|
| Sperrdateien | `find .git -name '*.lock'`: **keine**, vor und nach dem Commit |
| Commit | `b11a6f6`, 11 Pfade: `messgroessen.py` (66/6), `ARBEITSWEISE.md` (Abschnitt 16), `starte_sitzung.sh`, Zeiger, Anfragen 23d/23e, Antwort 23c, Aufträge TB-92/TB-93, Belege TB-91 A-N6 und TB-93-Vormessung |
| Arbeitsbaum danach | **leer** (0 Zeilen) ⇒ Abbruchkriterium 1 greift nicht |

Beleg: `schritt0_commit_und_sperrdateien.txt`.

## 2. Block A — sechs Nachmessungen

| | Vormessung | Mac-Messung | |
|---|---|---|---|
| **A-N1** | `5f707500…` → `623f8d77…` | `5f7075003c9dc291…` → **`623f8d771ffd5ae9dc1b979fbe383c85268371ba4f1dfeff055379662be41f25`**, numstat 66/6 | ✔ gleich |
| **A-N2** | acht Funktionen gleich | alle acht **GLEICH**, auch die acht `ast.dump`-Kurzhashes sind identisch mit der Vormessung (`2d965f89…` … `0a49da24…`). Neu: `_sha256_datei`, `voreinstellung_ziel`, `schreibe_messgroessen`; geändert nur `main` | ✔ |
| **A-N3** | zeichengleich, 284 → 288 | `json.dump(mess, f, indent=2, ensure_ascii=False, sort_keys=True)` Z. 284 → Z. 288, Quelltext **und** AST gleich; `grep -c indent=2` 1 → 2 (Docstring), `f.write("\n")` 1 → 1 | ✔ |
| **A-N4** | `rc=1` vor der Rechnung | `rc=1` nach **1 s**, Meldung „nichts gerechnet, nichts geschrieben", Hash und mtime von `messgroessen.json` unverändert, `ergebnisse/` 13 → 13 | ✔ |
| **A-N5** | `messgroessen_<UTC-Stempel>.json` | `ergebnisse/messgroessen_2026-09-23-154013.json`, ungleich dem eingefrorenen Namen; Import legt nichts an (13) | ✔ |
| **A-N6** | in der VM nicht messbar | ⛔ **auch auf dem Mac nicht gemessen** — siehe unten | A2 |

⚠️ **Messhinweis zu A-N2:** `rma` ist **in `adx` verschachtelt**. Ein Vergleich
nur über die Funktionen der Modulebene bricht mit `KeyError: 'rma'` ab. Der Beleg
`a_n2_ast_vergleich.py` sammelt deshalb alle `FunctionDef` per `ast.walk`.

⭐ **A-N6, Nebenbefund:** Diese Sitzung hat `messgroessen.py` nicht geändert, nur
committet. Ausserdem gilt: `messgroessen.py` steht in **keiner** `ask`-Regel und
`ergebnisse/messgroessen.json` in **keiner** `deny`-Regel von
`.claude/settings.local.json`. Auch `kennzahlen.py` und `pruefe_grenzsaetze.py`
fehlen dort, obwohl sie in `EINGEFROREN` stehen. Nach Fables Präzisierung 23c
(„gesperrt" umfasst `EINGEFROREN`) deckt die Berechtigungsdatei damit nicht jeden
gesperrten Pfad ab. Eine Mac-Sitzung, die `messgroessen.py` ändert, bekäme
heute **keinen** Dialog. ⛔ Nicht geändert (Betreibersache). Beleg:
`a_n6_genehmigungsdialog.txt`.

## 3. Block B ⭐⭐⭐ — der Determinismusnachweis

### 3.1 Messung

| | |
|---|---|
| **B1** | `messgroessen.json` `2a9b91660a42f06a33e3582b52359a3fba305c2e0da3b0a383fe5338036928c8`, 4567 B; `ergebnisse/` **13** Dateien |
| **B2** | `trading-env/bin/python3 messgroessen.py --ziel ergebnisse/messgroessen_2026-09-23_nachweis.json` (cwd `research/vorregistrierung`), **rc 0**, ca. 12 s |
| **B3** | neu `7f46d5f511dde6825dd33bfa88a7175aafe6bda9e93c8c29aa8790388dce7fa6`, 4569 B · `cmp`: **differ: char 260, line 11** |
| **B4** | ⛔ **NICHT BYTEGLEICH ⇒ BEFUND UND STOPP** |
| **B5** | `messgroessen.json` Hash und mtime unverändert; die 13 alten Dateien sind alle hashgleich, `ergebnisse/` jetzt 14 (die Nachweisdatei daneben) |

### 3.2 Was sich unterscheidet

**Erste abweichende Stelle:** Byte 260, Zeile 11:
`datenbereiche.krypto_1d.frueheste`, alt `"2021-09-01"`, neu `"2017-08-17"`.

| Gruppe | Blätter | abweichend |
|---|---|---|
| `datenbereiche.krypto_{1d,4h,1h}` | je 5 | je **3** (`frueheste` 2021-09-01 → 2017-08-17, `median_beginn` 2021-09-01 → 2020-10-14, `letzter_balken` 2026-08-31 → 2026-09-14/-15); `symbole`, `spaeteste_beginn` gleich |
| `volatilitaet.krypto_{1d,4h,1h}` | je 14 | je **13**: alle Quantile und Mediane; nur `symbole_gemessen` gleich |
| `datenbereiche.aktien_1d`, `volatilitaet.aktien_1d` | 5 + 14 | **0** |
| `kosten`, `datenfrequenz`, `haltedauer`, `universum` | 51 | **0** |
| **Summe** | **127** | **48** |

Grössenordnung (Krypto 1d): `balken_sigma_pct` 5,2782 → 5,9591,
`spanne20_median_pct` 34,2726 → 35,8546, `atr14_median_pct` 7,2669 → 7,6262. Der
volle Diff steht in `b3_b5_bytevergleich.txt`, die Gruppenzählung in
`b4_schluesselvergleich_ergebnis.txt`.

### 3.3 ⭐⭐ Gegenprobe: Code oder Eingaben? *(Zusatz dieser Sitzung, nicht im Auftrag)*

Das ist keine Nachbesserung, sondern eine Messung der Ursache: Es wird nichts im
Repo geschrieben und nichts verändert.

| | |
|---|---|
| Eingaben | `git archive a2fcf01 data config research/tb24_haltedauern/ergebnisse` ins Scratchpad, umgelenkt mit `TB30A_BASE_DIR` |
| Code | HEAD, `messgroessen.py` `623f8d77…` (die neue, abgesicherte Fassung) |
| Ziel | Scratchpad, **nicht** `ergebnisse/` (`ergebnisse/` blieb bei 14) |
| Ergebnis | **`2a9b91660a42f06a…` — BYTEGLEICH** mit der eingefrorenen Datei, rc 0, 11 s |

Eingabeunterschied `a2fcf01` → HEAD: Nur ein Commit berührt `data/`, nämlich
`90e3cbd` (TB-34, 15.09., „BTC/ETH ab 2017-08-17"). Er änderte oder entfernte 91
Dateien, **keine davon eine Aktiendatei**. `haltedauern_je_bot.csv` ist
unverändert. In `config/` kam nur `groessenfaktor.beispiel.json` hinzu, das
`messgroessen.py` nicht liest.

⇒ **Code und Ausgabeformat sind deterministisch, auch in der abgesicherten
Fassung.** Der Befund heisst: **Die Eingaben der eingefrorenen Datei stehen nicht
mehr in `data/`.** Die Datei ist nur noch aus der Git-Historie reproduzierbar,
nicht aus dem heutigen Arbeitsstand. Die Kursdaten sind nicht Teil von
`EINGEFROREN`, und der Register-Hash in `herkunft.json` bezeugt sie nicht.

Belege: `b4_gegenprobe.sh`, `b4_gegenprobe_ergebnis.txt`.

## 4. Block C — entfällt

Nach Abbruchkriterium 5 gilt: **keine** Tatsachennotiz 37.3, **kein** Sondenlauf,
**kein** Abbild.

⚠️ **Zustand, der damit offen steht:** Die Änderung an `messgroessen.py` ist mit
`b11a6f6` auf `main` committet (Schritt 0 verlangte committen, nicht verwerfen).
Ihr Hash `5f707500…` → `623f8d77…` steht damit **ohne Tatsachennotiz** im Repo,
und der Register-Gesamthash in `herkunft.json` wandert mit, sobald er gerechnet
wird. Die Sonde wird `messgroessen.py` als Abweichung der Abschnitt-0-Gruppe
melden (nicht gemessen, Erwartung aus dem Auftrag). Die Notiz nachzuholen oder
die Änderung zurückzunehmen, entscheidet Fable bzw. der Betreiber.

## 5. ⭐ Was zu entscheiden ist (nicht von dieser Sitzung)

Fables Bedingung (23c) lautete wörtlich „reproduziert `ergebnisse/messgroessen.json`
bytegleich — sonst Befund und Stopp". Gemessen ist: Gegen `data/` von heute
ist das nicht erreichbar. Gegen die Eingaben von `a2fcf01` ist es erfüllt. Drei
Fragen gehen damit an Fable:

1. **Gilt die Gegenprobe als Determinismusnachweis?** Also: bytegleich bei
   gleichen Eingaben, belegt mit dem Code-Stand nach der Absicherung. Oder
   verlangt 23c ausdrücklich die Reproduktion aus dem heutigen Arbeitsstand?
2. **Worauf ruhen die Rastergrenzen?** `registerdaten.py:64` liest die
   eingefrorene Datei, also Krypto-Messgrössen **vor** TB-34. Die Bots und die
   Neuselektion rechnen heute auf den neu geladenen Daten (BTC/ETH ab
   2017-08-17). Ob das eine Inkonsistenz ist oder bewusst so eingefroren wurde,
   kann diese Sitzung nicht beurteilen.
3. **Gehören die Eingaben von `messgroessen.py` in die Bezeugung am Tag?**
   (Commit-Hash von `data/` oder ein Datenstand-Hash in `herkunft.json`.)

## 6. ⛔ Was NICHT geschah

- `ergebnisse/messgroessen.json` nicht ersetzt, nicht gelöscht, nicht angefasst (Hash und mtime gleich)
- keine Änderung an Messfunktionen, Ausgabeformat, `GEBUEHR_PCT`, `herkunft.py`, Berechtigungen
- keine Tatsachennotiz, kein Registertext, kein Abbild, kein Sondenlauf
- nichts aus Punkt 8 / TB-92

## Belege (`docs/belege/TB-93/`)

`vormessung_absicherung_messgroessen.txt` (steuernder Chat) ·
`schritt0_commit_und_sperrdateien.txt` · `a_n1_n3_nachmessung.txt` ·
`a_n2_ast_vergleich.py` · `a_n4_n5_nachmessung.txt` · `a_n6_genehmigungsdialog.txt` ·
`b1_hashes_vorher.txt` · `b2_lauf.txt` · `b3_b5_bytevergleich.txt` ·
`b4_schluesselvergleich.py` · `b4_schluesselvergleich_ergebnis.txt` ·
`b4_gegenprobe.sh` · `b4_gegenprobe_ergebnis.txt` · `b5_hashes_nachher.txt`.
Die Nachweisdatei `research/vorregistrierung/ergebnisse/messgroessen_2026-09-23_nachweis.json`
(`7f46d5f5…`) ist mit committet. Sie ist der Befund.

---

## In einfacher Sprache

Die Absicherung des Messprogramms ist in Ordnung. Es kann die geschützte Datei
nicht mehr überschreiben. Das haben wir absichtlich versucht, und es hat sich
geweigert. An den eigentlichen Rechnungen wurde nichts verändert.

Der Kernversuch ist aber **nicht bestanden**: Das Programm sollte die alte Datei
Byte für Byte wiederholen. Es kamen andere Zahlen heraus, und zwar bei allen
Krypto-Werten. Bei den Aktien war alles gleich.

Die Ursache ist gefunden, und sie liegt nicht im Programm: Die alte Datei wurde
am 14.09. berechnet. Am 15.09. wurden die Krypto-Kursdaten neu und länger
heruntergeladen, Bitcoin zum Beispiel jetzt ab 2017 statt ab 2021. Mit den
Kursdaten vom 14.09. liefert das Programm die alte Datei tatsächlich Byte für
Byte. Das Programm rechnet also verlässlich. Die eingefrorenen Messwerte passen
aber nicht mehr zu den Kursdaten, die heute im Projekt liegen.

Ob das so gewollt ist und ob der Nachweis damit als erbracht gilt, entscheidet
der Verfahrensprüfer. Bis dahin ist nichts weiter geändert. Die Vorbereitung für
das Register (Block C) ist ausgesetzt.
