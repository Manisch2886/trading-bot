# TB-79 Registerabschnitt 31 — kein Manifest-Feld `asof` — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel fuer Claude Code: `TB-79 Register 31`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, Base `main`. Direkt auf `main`, kein Zweig,
kein PR (Dokumentationsaufgabe, `ARBEITSWEISE.md` Abschnitt 5b).

⛔ **Diese Aufgabe rechnet nicht am Selektionspfad.** Sie aendert **keinen**
Code, **keine** Sperrlisten-Datei, **nichts** unter `research/`, `strategies/`,
`shared/`, `snapshots/`. Sie schreibt ausschliesslich nach `docs/` — und fuehrt
**zwei lesende Messungen** aus (Abschnitt 31.5 und 31.6).

⭐ **Herkunft:** Dieser Auftrag ist der Nachtrag `TB-78b` aus
`logs/auftraege/NACHTRAG_TB-78b_fable_21j.md`, unveraendert im Inhalt. Er hat
die TB-78-Sitzung nicht mehr erreicht (sie war abgeschlossen) und wird deshalb
als eigener Auftrag gefuehrt — `logs/` ist nach `UMZUG.md` Abschnitt 2 **kein
Traeger**.

---

## Schritt 0 — Sichern, was dasteht

`git status --short`. Erwartet ist ein sauberer Baum bis auf
`.claude/settings.local.json` (unversioniert, bleibt liegen) und diese
Auftragsdatei plus den Zeiger. Committe, was da ist, bevor du anfaengst.

**Commit:** `TB-79 Schritt 0: Auftragsdatei und Zeiger`.

⚠️ **Der Stand, auf dem du aufsetzt:** `HEAD` traegt die Registerabschnitte
**27 bis 30** (TB-78, abgeschlossen). Abschnitt **31** fehlt — das ist dein
Gegenstand. Pruefe das zuerst: `grep -cE "^## 31\." docs/VORREGISTRIERUNG_neuselektion.md`
muss **0** sein. Ist es 1, ist der Abschnitt schon da — **brich ab und melde es**.

---

## Schritt 3c — Registerabschnitt 31: das Manifest bekommt kein Feld `asof`

⭐ **Die Vorgeschichte in drei Sätzen.** Fables 5a-Ergänzung aus 21b — heute als
**28.2** eingetragen — verlangte, `asof` als Feld ins `MANIFEST.json` zu
schreiben. Der steuernde Chat hat das als Verfahrensfrage vorgelegt, weil 17.1
sagt, der Snapshot werde *„nach seiner Erzeugung nicht mehr geschrieben"*, und
drei Auswege benannt. **Fable wählt keinen davon, sondern berichtigt die
Ursache.**

⭐⭐ **Sein Satz dazu, wörtlich, weil er die Fehlerklasse benennt:**

> *„Der Fehler ist meiner. In 21b habe ich ein Manifest-Feld `asof`
> vorgeschrieben, ohne das Manifest zu kennen. Eure Messung zeigt: Der Wert
> steht dort bereits, als `zeitpunkt_utc`. Ich habe damit einen **zweiten
> Feldnamen für denselben Wert** angeordnet — genau die Bauart ‚zwei Träger, die
> auseinanderlaufen können', die ich in 21b bei `fensteranker` und ihr heute
> dreimal abgelehnt habt."*

Hänge ans Ende von `docs/VORREGISTRIERUNG_neuselektion.md` an:

```markdown

---

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
| **`datenende`** | ⚠️ **von dir zu messen** — grösstes `open_time` über alle **223** Kursdateien in `snapshots/63e4b6c8…/` | Mac-Lauf, `trading-env/bin/python3` |
| **`asof`** | **2026-09-19** | `zeitpunkt_utc` im Manifest, Abschnitt 18 |
| Abstand | ⚠️ von dir auszurechnen | — |

⚠️⚠️ **Die Zahl steht bewusst NICHT in diesem Nachtrag.** Der steuernde Chat
hat sie über die Geräteanbindung vorab gemessen — **auf Linux, Python 3.10.12,
nicht auf dem Mac**. Nach `K2l` gilt: *die Anbindung liest das Repo, sie rechnet
nicht darin; jede Messung, deren Ergebnis ins Register soll, braucht einen
Mac-Lauf.* ⭐ **Miss selbst und trage deinen Wert ein.** Weicht er von
`2026-09-15` ab, **melde es** — dann hat eine der beiden Messungen etwas anderes
gemessen als sie glaubt.

⭐ **Und nenne im Ergebnisdokument die Umgebung, in der du gemessen hast** —
*eine Messung nennt die Umgebung, in der sie lief, nicht die, in der sie hätte
laufen sollen* (Fehlerregel zu `K2l`).

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

⭐ **Miss die 16 selbst nach**, bevor du sie einträgst, und nenne deine
Zählweise. *`C1`: jede Zahl wird an ihrer Quelle nachgerechnet, nicht aus einem
Bericht übernommen — auch nicht aus diesem.*

### 31.7 Was hier ausdrücklich NICHT getan wird

| | | |
|---|---|---|
| ⛔ | **Das Manifest anfassen** — weder `asof` noch `datenende` | 31.2, 31.3 |
| ⛔ | **Ein Beiblatt neben dem Manifest anlegen** (Weg c der Vorlage) — zweiter Träger | Fable 21j |
| ⛔ | **28.2 oder Abschnitt 26 umschreiben** — append-only | — |
| ⛔ | **Den Snapshot neu ziehen** | — |
| ⭐ | **Was entfällt:** die Manifest-Ergänzung, die in 28.7 als *„nicht getan"* geführt war, ist jetzt *„nicht zu tun"* | Fable 21j |
```

**Nachweise 3c:**

1. `git diff --numstat -- docs/VORREGISTRIERUNG_neuselektion.md` → zweite Spalte
   **`0`**.
2. `grep -nE "^#+ *31\."` → Abschnitt 31 genau einmal als `##`-Überschrift.
3. ⭐ **Deine eigene Messung von `datenende`** und **deine eigene Zählung der
   Manifest-Schlüssel**, beide mit genannter Umgebung, als Beleg unter
   `docs/belege/TB-78/`.
4. `shasum -a 256` auf `snapshots/63e4b6c8…/MANIFEST.json` **vor und nach**
   deiner Arbeit — **identisch**. *Das ist der Nachweis, dass 31.3 eingehalten
   ist, und er gehört in den Beleg.*
5. Die drei Sperrlisten-Hashes unverändert.

**Commit:** `TB-78 Schritt 3c: Registerabschnitt 31, kein Manifest-Feld asof`. **Pushen.**

---

## Zur Abgabe

⚠️ **Du hast bereits abgegeben** (`54bbe66`). Schreibe nach v2 und diesem
Nachtrag **`docs/ERGEBNIS_TB-78_register_27_29.md`** und den **Journalblock
`CG`** fort — **nur anfügen, nichts umschreiben**.

⭐ **Der Dateiname des Ergebnisdokuments bleibt**, obwohl jetzt 27–31 darin
stehen. *Ein Dokument umzubenennen, auf das der Journalblock und der Commit
`54bbe66` zeigen, kostet mehr als der ungenaue Name einbringt — und die
Quellenzeile im Journal muss treffen.* Vermerke das im Dokument.

⚠️ **Drei unversionierte Dateien liegen im Arbeitsbaum und gehören
mitcommittet:**

```
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21i_gesperrter_faltenplan.md
docs/projektfuehrung/FABLE_ANFRAGE_2026-09-21c_einarbeitung_21i_und_manifest.md
docs/projektfuehrung/FABLE_ANTWORT_2026-09-21j_manifest_asof.md
```

*(Die dritte legt der steuernde Chat ab; liegt sie bei deinem Commit noch nicht
da, melde es — dann kommt sie nach.)*

---

## Ein zusätzliches Abbruchkriterium

⛔ **Brich ab und melde, wenn** `shasum -a 256` des Manifests vor und nach
deiner Arbeit **nicht identisch** ist.

---

## In einfacher Sprache

Der Prüfer hat heute Vormittag verlangt, das Stichtagsdatum zusätzlich in die
Beschreibungsdatei des eingefrorenen Datenbestands zu schreiben. Wir haben
nachgemessen: Das Datum steht dort längst, nur unter einem anderen Namen. Er
nimmt seine Anordnung deshalb zurück — ein Wert braucht keinen zweiten Namen.

Und er legt fest, was bisher nirgends stand: Die eingefrorene Beschreibungsdatei
wird nach dem Einfrieren nicht mehr angefasst, auch nicht um harmlose Zusätze.
Alles, was man später über den Datenbestand feststellt, kommt ins Regelwerk,
nicht in den Datenbestand.

Am Ergebnis ändert sich nichts: Stichtag, Zehnjahresgrenze und Prüfsumme bleiben,
wie sie sind. Dazu kommt eine kleine Berichtigung — eine Zahl im Regelwerk sagt
„15 Einträge", gemessen sind es 16.
