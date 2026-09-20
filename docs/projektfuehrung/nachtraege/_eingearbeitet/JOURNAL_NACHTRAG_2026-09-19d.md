# Journal-Nachtrag 19.09.2026 (d) — TB-55 Mac-Lauf

**Anzufügen am Ende von `docs/projektfuehrung/JOURNAL.md`, NACH dem Block aus
Nachtrag (c).** Nichts wird umgeschrieben.

> ⚠️ **Zum Blockbuchstaben: messen, nicht raten.** Am 18.09. wurde AX
> angenommen, es war AZ, und TB-50 musste fünf Blöcke verschieben.

---

## Block ⟨nächster⟩ — TB-55: der Eingabezustand existiert

**19.09.2026, auf dem MacBook. `main`, Basis `7e48e1f` → Commits `1075dec`
(Snapshot) und `4c80588` (Ergebnisdokument), beide gepusht.
Interpreter durchgehend `trading-env/bin/python3` = Python 3.9.6.**

⭐⭐ **Die eine Handlung dieses Projekts, die sich nicht wiederholen lässt, ist
vollzogen.**

```
63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
```

---

### Die Zahlen, aus dem Manifest gelesen

| | |
|---|---|
| Dateien | **225** = 223 Kursdateien + `config/sp500_top150.txt` + `config/top25_symbols.txt` — **keine dritte** |
| Bytes gesamt | **211 040 678** |
| Zeitpunkt (UTC) | **2026-09-19T06:49:32+00:00** |
| `datenstand_hash` | `d9449faf…a995f84`, **223** — ⭐ **dreimal gemessen** (06:46, 06:49, 06:52 UTC), dreimal gleich |
| Zugelassene Befunde | **36**, alle `rand_erste`, *Abschnitt 17.3* · `nicht_zugelassen` **leer** |
| Zug | `GEZOGEN - 225 Datei(en), 211.0 MB, **jede byteweise gegen die Quelle geprueft**`, rc 0 |
| Nachprüfung | ⭐ **`UNVERAENDERT`**, Soll = Ist für **beide** Hashes, rc 0 |
| `.gitignore` | **nicht geändert** — `snapshots/` war nie erfasst |
| Datenbanken | **12** gesichert (nicht neun), am Ende **12/12** byteweise identisch |

---

### ⭐⭐ Fünf unabhängige Belege — und der stärkste war nicht bestellt

| # | |
|---|---|
| **1** | Byteweise Prüfung **beim Kopieren**, alle 225 |
| **2** | `--pruefen` **danach**: `UNVERAENDERT` |
| **3** | ⭐⭐ **`git rev-list` + `cat-file`: 1 Commit, 4 Trees, 1 Blob — der eine Blob ist das Manifest.** *Für keine der 225 Dateien wurde ein neuer Blob angelegt. git adressiert über den Inhalt — es bezeugt die Byte-Gleichheit mit `data/`, ohne unser Werkzeug zu kennen* |
| **4** | Der Registerprüfer lief in einem Worktree auf `7e48e1f` und mass dort ebenfalls `d9449faf…`/223 — ⭐ **der versionierte Inhalt ist gleich dem Arbeitsbaum**, vorher nie gemessen |
| **5** | Der Name ist **viermal** gerechnet: TB-49 Cloud (echter Zug, 3.11) · TB-49 Mac (3.9.6) · TB-55 Cloud (3.11.15) · **TB-55 Mac (3.9.6, dieser Zug)** |

⭐ **Beleg 3 entstand aus der Zuwachsmessung, die nur die Kosten prüfen sollte.**

---

### ⚠️ Die Abweichung von TB-46, und wie sie behandelt wurde

**Erwartet +0,001 %. Gemessen: +6 lose Objekte, +0,04 MiB (0,026 %), `du`
+80 KiB (0,048 %), `size-pack` unverändert.**

**Erklärung:** TB-46 mass den *Packfile*-Zuwachs von 30 Dateien **ohne
Manifest**; hier kommen ein 133-KB-Manifest und vier Tree-Objekte für 226
Einträge mit 64-stelligen Pfadnamen hinzu — und der Nenner ist ein Repo aus
**156 MiB losen** Objekten bei 3,4 MiB Packfile.

> ⭐⭐ **Der Schluss, von der Sitzung selbst gezogen:** *„Die strukturelle
> Aussage, auf die es ankam — gleiche Inhalte einmal — ist mit ‚1 Blob' direkt
> belegt."*
>
> ⭐ **Eine Kostenmessung ist nie die Aussage, sondern ihr Stellvertreter.
> Weicht der Stellvertreter ab, wird die Aussage direkt geprüft.**

---

### ⭐⭐ Ein offengelegter Fehler, und daraus ein neues Prüfprinzip

> *„Der ‚vorher'-Lauf wurde erst **nach** dem Commit nachgeholt, weil ich ihn
> vor dem Commit übersprungen hatte. Statt zu behaupten, er wäre gleichwertig,
> habe ich den Stand `7e48e1f` als Worktree ausgecheckt und den Prüfer dort
> laufen lassen."*

⭐ **Nicht als „gemacht" verbucht. Nicht als gleichwertig behauptet.
Rekonstruiert — und als Rekonstruktion benannt.**

⇒ **A7:** *„Eine nachgeholte Vorher-Messung ist nur dann eine Vorher-Messung,
wenn der Zustand inhaltsadressiert wiederherstellbar ist — und sie muss sagen,
dass sie nachgeholt wurde."* ⚠️ **Bei Uhrzeit, Umgebung oder laufenden
Prozessen wäre dasselbe Vorgehen wertlos gewesen.**

**Ein zweiter benannter Fehler:** das erste Leseskript der Sitzung nahm an, die
Kursdateien stünden im Manifest mit Präfix `data/`; sie stehen flach. ⭐ *„Das
Manifest selbst war nie in Frage — nur meine Annahme über seine Form."*

---

### Was die Cron-Prüfung ergab

**22 aktive Einträge**, nur Zeitfelder ausgegeben, **kein Befehl**.
Abruf-Zähler **0**. `*/5` und `*/15` feuerten um 08:45 und 08:50 **während**
der Sitzung — ⭐ **ohne Wirkung auf eine einzige der 12 Datenbanken.**
`broker_testnet_t3_supertrend.db` um 08:05 passt zu `5 */4 * * *`.

⭐ **T46.4 („kein Datencron") war eine Regel. Jetzt ist sie gemessen.**

---

### ⚠️ Zwei fremde `MANIFEST.json`

`data_sicherung/2026-09-15_115131/` (TB-34-Sicherung, gitignoriert) und
`research/hrp_portfolio/corrected_curves_original/` (versioniert). **Beide sind
keine Snapshots.** ⚠️ **Die Abbruchregel „existiert schon einer" hätte hier
falsch auslösen können** — das Kennzeichen ist der Ordnername
`snapshots/<64 Hex>/`, nicht die Anwesenheit einer Manifestdatei.

---

### Der Stand nach dieser Sitzung

| | |
|---|---|
| Snapshot | ⭐ **existiert**, versioniert, gepusht, `UNVERAENDERT` |
| `data/` | unberührt, dreimal gemessen |
| Sperrliste, `shared/snapshot.py`, `shared/paths.py` | **unberührt** |
| Register | ⚠️ **noch kein Eintrag** — TB-55b folgt |
| Die 0-Byte-Doppelgängerin | **mitgesichert, nicht gelöscht** — Beweismaterial für TB-53 |
| Registerprüfer | vorher **und** nachher **KEIN BEFUND** |
| `git status --porcelain` | **0 Zeilen** |

---

### In einfacher Sprache

**Die eingefrorene Kopie aller Kursdaten existiert.** Sie heisst nach ihrem
Inhalt, liegt im Projekt und ist hochgeladen. Ab jetzt ist sie die Grundlage
des Auswahllaufs — und sie lässt sich Jahre später noch nachprüfen.

**Fünf getrennte Gründe sprechen dafür, dass sie stimmt.** Der schönste: beim
Einchecken brauchte git für keine einzige der 225 Dateien neuen Speicher. git
legt gleiche Inhalte nur einmal ab — **dass es nichts Neues anlegte, heisst,
die Kopie ist identisch, und das sagt ein Programm, das unser Werkzeug gar
nicht kennt.**

**Was noch fehlt:** Die Zahl muss ins Regelwerk. Das ist klein — aber es ist
der Schritt, auf den alles andere wartet.
