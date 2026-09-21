# Backlog-Nachtrag 19.09.2026 (j) — TB-55: der Snapshot ist gezogen

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(i) voraus.** Einzufügen als **Block 2p**, nach Block 2o.

---

### 2p — TB-55 Mac-Lauf: der registrierte Eingabezustand existiert

| # | Punkt |
|---|---|
| **T55.13** | ⭐⭐⭐ **DER SNAPSHOT IST GEZOGEN.** `63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2` · **225 Dateien**, **211 040 678 Bytes** · Zeitpunkt **2026-09-19T06:49:32+00:00** · Datenstand `d9449faf…`/223, **dreimal gemessen** · **36** zugelassene Befunde, alle `rand_erste`, Abschnitt 17.3, `nicht_zugelassen` leer · `GEZOGEN - 225 Datei(en), 211.0 MB, jede byteweise gegen die Quelle geprueft` · Nachprüfung **`UNVERAENDERT`**, rc 0 · Commit **`1075dec`** auf `main`, gepusht · Ergebnisdokument `4c80588`. ⚠️ **Ab jetzt gilt F1a scharf: ein zweiter Snapshot ist ein neuer Lauf** |
| **T55.14** | ⭐⭐ **FÜNF UNABHÄNGIGE BELEGE, und der stärkste war nicht bestellt.** (1) byteweise Prüfung beim Kopieren · (2) `--pruefen` danach `UNVERAENDERT` · ⭐⭐ **(3) `git rev-list` + `cat-file`: 1 Commit, 4 Trees, 1 Blob — und der eine Blob ist das Manifest. Für KEINE der 225 Dateien wurde ein neuer Blob angelegt.** *git adressiert über den Inhalt: git selbst bezeugt die Byte-Gleichheit mit `data/`, ohne unser Werkzeug zu benutzen* · (4) der Registerprüfer lief in einem Worktree auf `7e48e1f` und mass dort ebenfalls `d9449faf…`/223 — **der versionierte Inhalt ist gleich dem Arbeitsbaum**, eine Kette, die vorher nie gemessen war · (5) der Name ist **viermal** gerechnet: TB-49 Cloud (echter Zug, 3.11), TB-49 Mac (3.9.6), TB-55 Cloud (3.11.15), TB-55 Mac (3.9.6, dieser Zug) |
| **T55.15** | ⚠️ **DER ZUWACHS WEICHT VON TB-46 AB — erklärt, kein Befund.** Erwartet +0,001 %; gemessen **+6 lose Objekte**, `count-objects size` +0,04 MiB (**0,026 %**), `du -sk .git` +80 KiB (**0,048 %**), `size-pack` **unverändert**. ⭐ **Erklärung:** TB-46 mass den *Packfile*-Zuwachs von 30 Dateien **ohne Manifest**; hier kommen ein 133-KB-Manifest und vier Tree-Objekte für 226 Einträge mit 64-stelligen Pfadnamen hinzu, und der Nenner ist ein Repo aus **156 MiB losen** Objekten bei nur 3,4 MiB Packfile. ⭐⭐ **Der richtige Schluss, von der Sitzung selbst gezogen:** *„Die strukturelle Aussage — gleiche Inhalte einmal — ist mit ‚1 Blob' direkt belegt."* **Der Prozentsatz war nie die Aussage, nur ihr Stellvertreter** |
| **T55.16** | ⭐⭐ **NEUES PRÜFPRINZIP A7 — aus einem offengelegten Fehler der Sitzung.** Der „vorher"-Lauf des Registerprüfers wurde **übersprungen** und **nach** dem Commit nachgeholt: Stand `7e48e1f` als Worktree ausgecheckt, Prüfer dort laufen lassen, Worktree entfernt. ⭐ **Nicht als „gemacht" verbucht, nicht als gleichwertig behauptet, sondern rekonstruiert und als Rekonstruktion benannt.** ⇒ **A7:** *„Eine nachgeholte Vorher-Messung ist nur dann eine Vorher-Messung, wenn der Zustand inhaltsadressiert wiederherstellbar ist — und sie muss sagen, dass sie nachgeholt wurde."* ⚠️ **Bei einem Zustand, der nicht aus dem Inhalt bestimmt ist — Uhrzeit, Umgebung, laufende Prozesse — wäre dasselbe Vorgehen wertlos** |
| **T55.17** | ⭐ **DIE CRON-PRÜFUNG HAT T46.4 BESTÄTIGT — gemessen statt vermutet.** **22 aktive Einträge** (nur Zeitfelder ausgegeben, kein Befehl), Abruf-Zähler **0**. `*/5` und `*/15` feuerten um 08:45 und 08:50 **während** der Sitzung — ⭐ **ohne Wirkung: 12/12 Datenbanken vorher = nach dem Ziehen = am Ende, byteweise.** `broker_testnet_t3_supertrend.db` um 08:05 passt zu `5 */4 * * *`, **erklärbar**. ⚠️ **Offen und klein: was tun `*/5` und `*/15`, wenn sie in keine `*.db` schreiben?** Gehört zur Aufgabe über die stillen Ausfälle (V5) |
| **T55.18** | ⚠️ **ZWEI FREMDE `MANIFEST.json` IM BAUM — die Abbruchregel hätte falsch auslösen können.** `data_sicherung/2026-09-15_115131/` (TB-34-Sicherung, gitignoriert) und `research/hrp_portfolio/corrected_curves_original/` (versioniert, Forschungsbeleg). ⭐ **Die Sitzung hat beide gefunden und eingeordnet, statt abzubrechen oder zu übersehen.** ⚠️ **Für künftige Aufträge: „existiert schon ein Snapshot?" darf nicht über `MANIFEST.json` allein gehen** — der Name `snapshots/<64 Hex>/` ist das Kennzeichen |
| **T55.19** | ⭐ **F1b/Q2 IST JETZT BILLIG ZU BELEGEN.** Der Snapshot liegt versioniert in `1075dec`. **Die Cloud checkt ihn aus und lässt `--pruefen` dagegen laufen** — das ist die Reproduktion auf der zweiten Maschine, und sie kostet eine halbe Sitzung. ⭐ **Zusammen mit den vier Hash-Rechnungen aus T55.14 wäre Q2 damit erledigt** |
| **T55.20** | ⚠️ **`git gc` STEHT AN, ABER NICHT JETZT.** **2 618 lose Objekte, 156,5 MiB lose gegen 3,4 MiB Packfile.** ⚠️ **Ein `gc` verändert jede künftige Zuwachsmessung und damit die Vergleichbarkeit mit TB-46 und T55.15.** ⭐ **Eigener Punkt, eigene Entscheidung, mit Messung vorher und nachher** |
| **T55.21** | **Klein, offen:** der Remote-Zweig `claude/new-session-9qrb42` (der Cloud-Lauf vom 19.09., der nicht ziehen durfte) liegt auf `origin`. **Nicht geholt, nicht angesehen.** Aufräumen, wenn es sonst nichts zu tun gibt |

---

## Ergänzung zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2c** | ⭐⭐ **Prüfprinzip A7 gehört nach `docs/PRUEFPRINZIPIEN.md`, Gruppe A** (T55.16) |
| **K2d** | ⭐ **Eine Kostenmessung ist nie die Aussage, sondern ihr Stellvertreter.** Weicht der Stellvertreter ab, wird die eigentliche Aussage direkt geprüft — hier: „1 Blob" statt „+0,001 %" (T55.15) |
| **K2e** | ⚠️ **„Existiert schon ein Snapshot?" prüft den Ordnernamen `snapshots/<64 Hex>/`, nicht die Anwesenheit einer `MANIFEST.json`** (T55.18) |

---

## Kettenzeile — 0,86 ist erledigt

**Zu finden** (Abschnitt 3, Rang **0,86**, in der Fassung aus Nachtrag (h)).
⚠️ **Ersetzen, alter Wortlaut bleibt darunter als ersetzt gekennzeichnet:**

```
| **0,86** | ⭐⭐ **TB-55 — den Snapshot ziehen: ERLEDIGT 19.09.2026.** `63e4b6c8…cb2ceb2`, 225 Dateien, Commit `1075dec` auf `main`. Nachprüfung `UNVERAENDERT` | ✅ **abgeschlossen** |
| **0,86a** | ⭐⭐ **TB-55b — der Registereintrag zum Snapshot** (Tatsachennotiz, keine Änderung eines Registertexts) | ⚠️ **als nächstes** |
```

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte
   Zeilen: die der ersetzten Kettenzeile 0,86, sonst keine.**
2. ⚠️ **Prüfen, dass der alte Wortlaut von 0,86 als ersetzt gekennzeichnet
   darunter steht** — nicht gelöscht.
3. `git status --short` vor dem Commit, `add`+`commit`+`push` in einem Zug,
   `git status` **danach**.
