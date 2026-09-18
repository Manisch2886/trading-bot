# Prüfprinzipien-Nachtrag 18.09.2026

> ⚠️ EINGEARBEITET am 18.09.2026 in `docs/PRUEFPRINZIPIEN.md`, Commit 02de1f7.
> Dieses Dokument bleibt als Beleg des Nachtrags stehen und wird nicht
> mehr fortgeschrieben.

**Einzufügen in `docs/PRUEFPRINZIPIEN.md`.** Ein neues Prinzip, eine
Berichtigung an einer Tabellenzeile.

---

## Einfügung — neues Prinzip A6

**Ankertext** — diese Zeile existiert genau einmal:

```
## B — Wie eine Probe sich selbst täuscht
```

**Der folgende Text kommt UNMITTELBAR DAVOR**, mit einer Leerzeile Abstand nach
unten:

--- ANFANG EINFÜGETEXT A6 ---
### A6 — Eine Einzelmessung kann die ABWESENHEIT eines flackernden Fehlers nicht belegen

**Der Fall (TB-49, Mac-Lauf 18.09.2026):** `system/test_log_rotation.py` war in
TB-47 aus `BEKANNT_ROT` gestrichen worden, mit der Begründung *„auf BEIDEN
Rechnern grün, 117/117"* — je **eine** Messung pro Rechner.

**Zehn Einzelläufe auf dem Mac:**

| Lauf | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| | ⚠️ **116** | 117 | ⚠️ **116** | 117 | ⚠️ **116** | 117 | 117 | 117 | 117 | 117 |

**Immer `116 von 117`, immer eine zeitabhängige Probe zum Restfenster beim
Rotieren, ein bis zwei fehlende Zeilen von 238–512 — und die gefallene Probe
wechselt.** Rate **~30 %**.

> ⭐ ***„Die Streichung stützt sich auf je EINE Messung pro Rechner; bei ~30 %
> Flackerrate trifft eine Einzelmessung mit 70 % Wahrscheinlichkeit grün."***

⚠️ **Und der Befund stand längst im Backlog** (T38.10, 15.09.: *„flattert —
Rennbedingung zwischen Sichern und Leeren"*). **Eine dokumentierte Aussage wurde
mit einer Einzelmessung überstimmt, ohne nachzusehen, ob es dazu schon etwas
gibt.**

**Die Regel, zweiteilig:**

| | |
|---|---|
| ⭐ **Grün einmal ist kein Nachweis** | Wer einen Eintrag aus einer Rot-Liste streicht, braucht **mehrere** Läufe — bei einem Verdacht auf Zeitabhängigkeit zehn |
| ⚠️ **Vor dem Streichen im Backlog nachsehen** | *Eine geprüfte Aussage ungeprüft zu verwerfen ist derselbe Fehler wie eine Zahl ungeprüft zu übernehmen (**C1**), nur in die andere Richtung* |

**Und die richtige Formulierung für solche Fälle:** nicht „rot" und nicht „grün",
sondern ⭐ **„grün im Regelfall, zeitabhängig flackernd"** — mit der gemessenen
Rate dabei. *Ein flatternder Test untergräbt sonst die Aussagekraft jedes
Basislaufs, ohne dass jemand weiss, wie oft.*
--- ENDE EINFÜGETEXT A6 ---

---

## Berichtigung — eine Zeile in der Tabelle von C1

⚠️ **Nichts wird entfernt.** Die Tabelle in **C1** („Jede Zahl wird an ihrer
Quelle nachgerechnet") bekommt eine Zeile **angefügt**:

**Ankertext** — die letzte Zeile der C1-Tabelle:

```
| „die erste Selektionsfalte beginnt 2022" | der Faltenplan sagt **2019** (TB-48) |
```

**Unmittelbar danach einzufügen:**

--- ANFANG EINFÜGETEXT C1 ---
| „2022 ist die früheste **Krypto**-Falte" | **alle neun Bots beginnen 2019**; die 2022 stammt aus einem überholten Faltenplan (TB-49) |
| „`system/test_log_rotation.py` ist auf beiden Rechnern grün" | ⚠️ **3 von 10 Läufen rot** — eine Einzelmessung je Rechner belegte nichts (TB-49, siehe **A6**) |
--- ENDE EINFÜGETEXT C1 ---

---

## Was dabei NICHT passiert

| | |
|---|---|
| ❌ | **Keine bestehende Zeile wird geändert oder entfernt** — `git diff --numstat` muss `<n> 0` zeigen |
| ❌ | **Keine Umnummerierung.** `A6` ist neu; `B4` und `C7` behalten ihre Bedeutung, weil Journalblöcke darauf verweisen |
