# REGISTER-KOPIE Abschnitt 31 (von 0–53) — Register-Z. 5577–5708 — Commit ee43f5f1339549238c0da023db7c9f324b26d28e — 2026-10-04 — Original sha256 9a2cefb77a394a0a1c87c63cb9437d5693f054e4516333f656fae97668ef71ff — KOPIE, nicht das Register

## 31. Berichtigung zu 28.2 — das Manifest bekommt kein Feld `asof` (Fable 21j, 21.09.2026)

⭐ **Berichtigung eines Registersatzes, der am selben Tag eingetragen wurde**,
plus eine Präzisierung zu 5a / 17.1 (Ersteintrag) und zwei Tatsachennotizen.

**Herkunft:** `docs/projektfuehrung/FABLE_ANTWORT_2026-09-21j_manifest_asof.md`,
Abschnitt 2, zeichengleich. Anlass:
`docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21c_einarbeitung_21i_und_manifest.md`,
Punkt 5.

⚠️ **28.2 bleibt zeichengleich stehen.** Der Halbsatz, der ersetzt wird, ist
hier benannt.

### 31.1 Der Befund — der Wert steht im Manifest, unter einem anderen Namen

**Gemessen am `MANIFEST.json` des registrierten Snapshots
(`snapshots/63e4b6c8…/MANIFEST.json`):**

| | |
|---|---|
| Das Feld, das `asof` tragen sollte | existiert bereits als **`zeitpunkt_utc`** = `2026-09-19T06:49:32+00:00` |
| Ein Feld `asof` | **gibt es nicht** |

⇒ **Es fehlte kein Wert, nur ein zweiter Feldname für denselben Wert.**

### 31.2 Der Ersatztext zu 28.2, zeichengleich

> **Berichtigung zu 28.2 (Registertext 5a, Ergänzung), Ersatztext:**
> asof ist das UTC-Datum des Felds `zeitpunkt_utc` im `MANIFEST.json` des registrierten Snapshots. Es wird im Register als Tatsachennotiz neben dem Snapshot-Hash eingetragen. Ein neuer Snapshot (5c) setzt ein neues asof. **Das Manifest erhält kein Feld `asof`**; der Halbsatz „Es wird im `MANIFEST.json` als Feld `asof` geführt" ist ersetzt.

⚠️ **Der ersetzte Halbsatz steht in 28.2 und bleibt dort stehen**, mit dieser
Marke. **Der Wert von `asof` ändert sich nicht:** weiterhin **2026-09-19**.

### 31.3 Präzisierung zu 5a / 17.1 — Ersteintrag, zeichengleich

> **Präzisierung zu 5a / 17.1 (Ersteintrag):** „Wird nach seiner Erzeugung nicht mehr geschrieben" gilt für den Snapshot **einschliesslich seines Manifests**. Tatsachen über einen Snapshot, die nach seiner Erzeugung festgestellt werden — darunter `datenende` (grösstes `open_time` über alle Kursdateien des Snapshots) — stehen als Tatsachennotiz im Register, nicht im Snapshot. Ein Manifest darf `datenende` nur tragen, wenn es **bei der Erzeugung** geschrieben wird (5c, künftige Snapshots).

**Quelle des Grundes,** Fable wörtlich: *„17.1 im Wortlaut … und die Rolle des
Manifests als Träger, aus dem Abschnitt 18 seine Zahlen liest — ein Träger, der
nach der Registrierung noch beschrieben wird, kann nicht mehr bezeugen, was bei
der Registrierung galt, auch wenn der Hash ihn nicht deckt. Und der Grundsatz
ein Wert, ein Ort."* Kein Ergebnis.

**Seine Begründung gegen die drei vorgelegten Wege, wörtlich:**

> *„Warum nicht a: a lässt 28.2 stehen und liest es ‚für den nächsten Snapshot' — ein Registertext, der den Bestand nicht beschreibt, mit einer Lesart daneben. Das ist derselbe Zustand wie beim Vorlauf-Satz heute Vormittag, nur absichtlich. Warum nicht b: Der Preis ist genau der, den ihr nennt: ‚unverändert seit Erzeugung' gilt danach nicht mehr wörtlich, und ein Register, das wörtlich gelesen wird, verträgt keine folgenlosen Ausnahmen. Warum nicht c: zweiter Träger."*

### 31.4 Tatsachennotiz — seine Unsicherheit, gemessen

Fable markiert in 21j als unsicher, *„ob 17.1 den Begriff ‚Snapshot' an anderer
Stelle so verwendet, dass das Manifest ausdrücklich ausgenommen ist — dann wäre
meine Präzisierung eine Berichtigung dazu, und ihr seht das im Register, ich
nicht."*

**Gemessen 21.09.2026 im Register und am Dateisystem:**

| | Befund |
|---|---|
| 17.1 definiert den Snapshot als | **Ordner**: *„je Lauf einen eingefrorenen Snapshot (Tatsachennotiz: `snapshots/<hash>/`), der neben dem Bestand liegt und nach seiner Erzeugung nicht mehr geschrieben wird"* |
| Ort des Manifests | `snapshots/63e4b6c8…/MANIFEST.json` — **im Ordner** |
| Stelle, die es ausnimmt | **keine.** Alle Manifest-Erwähnungen im Register betreffen seine *Rolle* (führt Dateien mit Inhalts-Hash, trägt `datenstand_hash`, `teilkerzen`, zugelassene Befunde), nicht seine Unantastbarkeit |
| ⭐ **Die einzige Ausnahme, und sie ist eine andere Frage** | Der **Snapshot-Hash** deckt das Manifest nicht (17.1: *„der Hash der … (Pfad, Inhalts-Hash)-Paare **der Dateien** — nicht des Manifests"*) |

⇒ ⭐⭐ **Seine Präzisierung ist ein Ersteintrag, keine Berichtigung — und der
Wortlaut von 17.1 stützt sie.** ⚠️ *„Gehört zum Snapshot-Ordner" und „wird vom
Snapshot-Hash gedeckt" sind **zwei Fragen**, nicht eine (`C7`). Das Manifest
gehört dazu und wird nicht gedeckt; genau deshalb wäre eine Ergänzung folgenlos
für den Hash — und genau deshalb ist sie trotzdem ausgeschlossen.*

### 31.5 Tatsachennotiz — `datenende` des registrierten Snapshots

| | Wert | Herkunft |
|---|---|---|
| **`datenende`** | **2026-09-15** — grösstes `open_time` über alle **223** Kursdateien in `snapshots/63e4b6c8…/` (letzte Kerze `2026-09-15 08:00:00`, in 24 Krypto-1h-Dateien) | Mac-Lauf, `trading-env/bin/python3` (Python 3.9.6, macOS 15.7.9), Mac-Sitzung TB-79, 21.09.2026; zwei Zählungen (`csv`-Modul und pandas 2.3.3) gleich — `docs/belege/TB-78/schritt3c_messung_31_5_31_6.txt` |
| **`asof`** | **2026-09-19** | `zeitpunkt_utc` im Manifest, Abschnitt 18 |
| Abstand | **4 Tage** (2026-09-19 − 2026-09-15) | — |

⭐ **Messnotiz der Mac-Sitzung (TB-79), nicht Teil des Nachtrags:** Die 223
Kursdateien enden nicht am selben Tag — die **150 Aktien-Tagesdateien** enden
am **2026-09-01**, die 24 Krypto-Tagesdateien am 2026-09-14, die 48
Krypto-4h- und -1h-Dateien am 2026-09-15 (Ausnahme `XAUTUSDT_1h.csv`:
2026-08-30). `datenende` ist das Maximum über alle Dateien; das Datenende der
vier Aktien-Bots liegt **18 Tage** vor `asof`. Eine Kalenderaussage, keine
Ergebnisaussage.

### 31.6 ⚠️ Berichtigung einer Zahl aus Abschnitt 26 — 15 Schlüssel sind 16

**Abschnitt 26 (TB-77) sagt:** *„es steht nirgends als Wert — gemessen
21.09.2026 in allen `.py` …, im **Snapshot-Manifest (15 Schlüssel, keiner
`asof`)**, in `registerdaten.py` und in `docs/`"*.

**Nachgemessen 21.09.2026 am selben Manifest:** **16 Schlüssel.**

```
bytes_gesamt · dateien · dateien_gesamt · datenstand_hash · eingabeliste ·
kursdateien · quelle · snapshot_hash · teilkerzen · verfahren · werkzeug ·
wurzel · zeitpunkt_utc · zugelassene_befunde · zugelassene_befunde_anzahl ·
zugelassene_befunde_herkunft
```

⭐ **Eigene Nachmessung der Mac-Sitzung (TB-79), Zählweise genannt:** gezählt
sind die Schlüssel der **obersten Ebene** des JSON-Objekts, `dateien` (die
Dateiliste mit 225 Einträgen) **mitgezählt** — **16**; ohne `dateien` **15**.
Zwei Zählungen (`json.load`, Textmuster auf Einrückung 2) gleich; `asof` kommt
weder als Schlüssel noch sonst im Text vor. `trading-env/bin/python3`
(Python 3.9.6), 21.09.2026.

| | |
|---|---|
| ✅ **Die Aussage trifft** | **keiner** der Schlüssel heisst `asof` — der Befund von TB-77 steht |
| ⚠️ **Die Zahl trifft nicht** | 16, nicht 15 |
| ⭐ **Mutmassliche Ursache, nicht gemessen** | `dateien` ist die Dateiliste, die übrigen 15 sind Metadaten. Wer die Liste nicht mitzählt, kommt auf 15 — **aber die Zählweise steht nicht dabei** |

⭐⭐ **Fehlerklasse `K4d`: eine Kennzahl, die ihre Bezugsmenge nicht nennt.**
*Die Zahl war womöglich richtig gerechnet — über eine Menge, die niemand
benennt. Eine Kennzahl nennt die Menge, über die sie läuft.*

⚠️ **Abschnitt 26 bleibt zeichengleich stehen**; die Zahl gilt als berichtigt
durch diesen Unterabschnitt.

### 31.7 Was hier ausdrücklich NICHT getan wird

| | | |
|---|---|---|
| ⛔ | **Das Manifest anfassen** — weder `asof` noch `datenende` | 31.2, 31.3 |
| ⛔ | **Ein Beiblatt neben dem Manifest anlegen** (Weg c der Vorlage) — zweiter Träger | Fable 21j |
| ⛔ | **28.2 oder Abschnitt 26 umschreiben** — append-only | — |
| ⛔ | **Den Snapshot neu ziehen** | — |
| ⭐ | **Was entfällt:** die Manifest-Ergänzung, die in 28.7 als *„nicht getan"* geführt war, ist jetzt *„nicht zu tun"* | Fable 21j |

---

