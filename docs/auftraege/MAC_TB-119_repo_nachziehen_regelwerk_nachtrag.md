# TB-119 Repo nachziehen und Regelwerk-Nachtrag nach 27b Teil E — 15 Dateien committen, `UEBERGABE.md` berichtigen und auf den 27.09. fortschreiben, Teil E und 13 D2-Regeln ins Regelwerk

**Sitzungstitel:** `TB-119` · **Aufwand:** hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 27.09.2026, 18:35, vom steuernden Chat
**Grundlagen (in Schritt 0 prüfen):**
- `docs/projektfuehrung/FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md`, md5 `ad35734f99414c982741b0c3f5b27862`, Teil E (Tabelle „Was sich am Regelwerk ändert“)
- `docs/ERGEBNIS_TB-118_projektwissen_aufraeumen.md`, Abschnitte 8 und 9
- `docs/belege/TB-118/d2_fehlende_regeln.txt`
**Vorgänger:** TB-118 (abgegeben `2a0893b`, geschlossen 27.09., 12:03).
**Kein Fable bis Dienstag, 29.09.** Fragen an Fable gehen nur in `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md`, Abschnitt D.

## ⭐⭐ Freigabe des Betreibers, wörtlich

**27.09.2026, 18:08, Chat:** *„ich habe bis Dienstag kein fable Wochen Volumen mehr. bitte sammle alles für fable damit wir die fragen dann Dienstag stellen können. bis Dienstag arbeiten wir strukturier ohne fable weiter und sammeln alles für fable soweit möglich“*

**27.09.2026, ca. 18:25, Auswahlkarte „Was soll bis Dienstag ohne Fable laufen?“**, mit diesen zwei Optionen für diesen Auftrag:
- *„TB-119 Repo nachziehen (Empfohlen) — Die 15 neuen Dateien committen; in UEBERGABE.md Z. 99 streichen und den Stand auf den 27.09. fortschreiben, mit der Zeile zum Räumen der Ablage.“*
- *„Regelwerk-Nachtrag 27b Teil E (Empfohlen) — Fables Teil E und die 14 D2-Regeln ins Regelwerk. Die eine D2-Regel, die ARBEITSWEISE 6d widerspricht, geht als Frage in die Sammlung.“*

⇒ Antwort: **„Wir arbeiten alles strukturiert ab“.**

⛔ **Nicht freigegeben:**
- das Register (`docs/VORREGISTRIERUNG_neuselektion.md`); Code des Laufs; Sperrliste und Abbilder; `crontab`; Datenbanken;
- die acht D2-Regeln mit Status TEILWEISE: sie bleiben, wie sie sind, und werden im Ergebnis nur aufgeführt;
- D2 19/6 (Abbruchkriterium: fragen statt abbrechen): widerspricht ARBEITSWEISE 6d. Die Regel wird nicht eingetragen, sondern kommt als Frage in die Sammlung;
- Löschen, Verschieben oder Umbenennen im Repo.

**Sichtschutz 27.1:** Dokumente dieses Auftrags gehen in die Projektablage. Keine Ergebnisgrösse des Selektionsraums und keine Erwartung über den Ausgang hineinschreiben. Treffer werden nach 27.5 nur mit Fundstelle genannt.

In einfacher Sprache: Diese Sitzung macht das Repo wieder vollständig. Sie committet 15 Dateien, die der steuernde Chat heute gesichert hat, berichtigt eine Zeile in der Übergabe und schreibt den heutigen Stand dazu. Danach trägt sie die Regeln ins Regelwerk ein, die Fable für die Projektablage vorgeschlagen hat, dazu 13 Regeln aus alten Übergaben, die dort noch fehlten.

## Schritt 0 — Sicherung und Ausgang

0a. `git status --short`. Erlaubt ist das in der Mac-Sitzung; verboten ist es nur über die Brücke des steuernden Chats. Erwartet sind genau diese uncommitteten Dateien, jede mit md5 zu prüfen:

| Datei | md5 |
|---|---|
| `docs/auftraege/MAC_TB-119_repo_nachziehen_regelwerk_nachtrag.md` | (dieser Auftrag) |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | (Zeiger, geändert) |
| `docs/belege/TB-91/TB-91_vormessung_blockA_absicherung.md` | `0b76c226136104f2934ce4bd9c555a3d` |
| `docs/belege/TB-93/TB-93_vormessung_absicherung_messgroessen.md` | `a8c3f58fc7d3c5258f76bcdc231cd681` |
| `docs/projektfuehrung/ERINNERUNG_2026-09-25_speicher_export.md` | `c9455ae6ef6dcacac92a0b82ff1e18e3` |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-27c_tagesanfrage_tb116_tb117.md` | `fcf5ffa1f577b7a86213d70cd2b4faef` |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-22f_plan_gegengelesen.md` | `46d5224712969c726b7429a7acbe7066` |
| `docs/projektfuehrung/FABLE_ANTWORT_2026-09-25f_gesamtanalyse_und_ideen.md` | `1d2e7e8abaca522f82ff13d3a4537ca1` |
| `docs/projektfuehrung/FABLE_WOCHENRUECKMELDUNG_2026-09-19.md` | `1eb5720446a5b482619a450958bfbb73` |
| `docs/projektfuehrung/PROJEKTSTAND_2026-09-26_einfache_sprache.md` | `590316944640f5b3a9de3b398398d7f8` |
| `docs/projektfuehrung/PRUEFUNG_2026-09-25_drei_festlegungen_im_speicher.md` | `3b489150817561bcbfee4e4af111a4c4` |
| `docs/projektfuehrung/REGISTER_KOPIE_2026-09-21.md` | `9da9a2f6f5ab0af2ee477b5c85a7e119` |
| `docs/projektfuehrung/REGISTER_KOPIE_2026-09-24_teil1_0_bis_23.md` | `8a592847c4988f11a7be74ba4e02f0be` |
| `docs/projektfuehrung/REGISTER_KOPIE_2026-09-24_teil2_24_bis_36.md` | `5084a08c0dd4741e238809ea8d9ecd7b` |
| `docs/projektfuehrung/REGISTER_KOPIE_2026-09-24_teil3_37_bis_40.md` | `b966446cf111f76fe81799b013b0bd1a` |
| `docs/projektfuehrung/SITZUNGSWAECHTER_ausloeser_statt_tippen.md` | `6daacc8f763fca9dcc2402a57356168f` |
| `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md` | `ff2714141d65ae85589696436178c572` |

Herkunft: Die ersten 14 lagen bis zum 27.09. nur in der Projektablage. Der steuernde Chat hat sie vor dem Entfernen ins Repo geholt, aus der Ablage gelesen und md5-geprüft (27b G1). Die letzte Datei ist die Sammelstelle für Fable. Weicht ein md5 ab oder gibt es eine weitere Datei ⇒ Abbruch.
Commit `TB-119 Schritt 0: 15 gesicherte Dateien, Auftrag, Zeiger`, danach pushen.

0b. Ausgangswerte in `docs/belege/TB-119/0b_ausgang.txt`:
- HEAD;
- `wc -l` und `sha256sum` für `projektfuehrung/ARBEITSWEISE.md`, `projektfuehrung/UMZUG.md`, `projektfuehrung/DOKUMENTATIONSSTANDARD.md`, `docs/PRUEFPRINZIPIEN.md`, `projektfuehrung/UEBERGABE.md`;
- die Liste der Überschriften `^## ` von ARBEITSWEISE, mit Zeilennummer;
- `sha256sum docs/VORREGISTRIERUNG_neuselektion.md`.

0c. db-Sicherung nach 7c Schritt 0.

## Schritt A — `UEBERGABE.md`: Zeile 99 berichtigen, dann fortschreiben

A1. In `docs/projektfuehrung/UEBERGABE.md`, Zeile 99, genau diese eine Ersetzung vornehmen, sonst nichts:
- alt: `eine Trade-Zahl (656), die`
- neu: `eine Trade-Zahl (Wert nach 27.5 hier nicht wiederholt), die`

Nachweis:
- `grep -c '656' docs/projektfuehrung/UEBERGABE.md` ⇒ 0;
- md5 der Datei nach A1 **= `2b61283b190a3a90069207b2b3226758`**. Das ist die Fassung, die seit 27.09. in der Projektablage liegt. Weicht der Wert ab ⇒ Befund, nicht weiter.

Commit `TB-119 A1 UEBERGABE Z. 99 (27.5)`.

A2. Neuen Block ans Ende anhängen: `## Stand 27.09.2026 (TB-119)`. Jede Zahl wird am HEAD gemessen, nicht hierher abgeschrieben. Die Werte in Klammern sind die Erwartung des steuernden Chats; weicht eine Messung ab, steht der gemessene Wert im Block und die Abweichung im Ergebnis.
- Register: höchster Abschnitt (46), sha256 der Registerdatei.
- Gültiges Abbild: `sperrliste_abbild_2026-09-26_tb117.json` (`46f0ad5d…`). Sonde dagegen (37/0/0, `eingefroren` 22). ⚠️ Die Sonde nur laufen lassen, wenn sie nichts schreibt; sonst den Wert aus `ERGEBNIS_TB-117` mit Fundstelle nennen.
- sha256 von `research/vorregistrierung/herkunft.py`, `auswertung.py` und `shared/sperrlistensonde.py`.
- Fable:
  - 27a und 27b sind beantwortet und im Repo.
  - 27c ist offen.
  - **Kein Fable-Volumen bis Dienstag, 29.09.** Gesammelt wird in `FABLE_SAMMLUNG_fuer_2026-09-29.md`.
- Projektablage, gemessen vom steuernden Chat am 27.09. gegen 18:15:
  - vorher 148 Dateien, 1 570 315 Tokens (79 %);
  - nachher 40 Dateien, 638 044 Tokens (32 %);
  - Reihenfolge nach 27b C4: erst 13 Dateien abgelegt, dann 120 entfernt, dann gemessen.
  - Das ist die eine Zeile, die 27b C4 in `UEBERGABE.md` verlangt.
- Plan bis Dienstag:
  1. TB-119, dieser Auftrag.
  2. TB-120: Erzeuger (Stufe V), Bestandsaufnahme, nur lesend.
  3. TB-121: kalter Leser für Registertext 1–12 (Fable 25f V8/F3).
  - Was an 27c hängt, wartet: Leiter L2–L5, Öffnung `paths.py` (T117-5), Registerauftrag zu 27c.
- Betreiber: Speicher-Export des alten Projektspeichers, Frist **Dienstag, 29.09.2026**.
- Freie Nummern: TB frei ab 122, sobald TB-120/121 vergeben sind. Fable-Anfrage am Dienstag: `29a`.

Commit `TB-119 A2 UEBERGABE Stand 27.09.`

## Schritt B — Regelwerk-Nachtrag nach 27b Teil E

Umgesetzt wird die Tabelle aus 27b Teil E, Zeile für Zeile. Jede Änderung trägt die Herkunft „(27b Teil E, TB-119, 27.09.2026)“. Drei Abweichungen vom Wortlaut von Teil E sind vom Betreiber entschieden und werden so umgesetzt:

1. Überall, wo 27b `ENTSCHEIDUNGEN.md` sagt, gilt `BACKLOG_ENTSCHEIDUNGEN.md`. Das ist die Auswahlkarte in TB-118; siehe `ERGEBNIS_TB-118` Abschnitt 9, Punkt 2.
2. Für ARBEITSWEISE 7b gilt: „db-Sicherung sichert zusätzlich `docs/` als `docs.tar.gz`“. Nicht `git bundle`; das ist G7, ERGEBNIS_TB-118 Abschnitt 9, Punkt 8.
3. Der neue Abschnitt „Projektablage“ in ARBEITSWEISE bekommt die **nächste freie Abschnittsnummer, gemessen** (K2i). Nummer 19 ist schon vergeben (Sitzungswächter).

Die Lesarten, die bei Fable offen sind, stehen im Nachtrag so, wie `ablage_soll.py` heute arbeitet, und tragen den Zusatz „Lesart offen, Fable-Sammlung B4 bzw. B5“:
- B4: Wochenrückmeldung und Fable-Übergabe, B6 gegen C3;
- B5: „die zwei jüngsten Paare“.

B1. ARBEITSWEISE:
- neuer Abschnitt „Projektablage“ mit den Klassen aus Teil B, G1–G8, C1 und C2;
- Ergänzung in 15: Indexpflicht für `FABLE_DIALOG_INDEX.md`;
- Ergänzung in 8: Kennzahlen der Wochenrückmeldung;
- Ergänzung in 7b: `docs.tar.gz`.

B2. UMZUG, drei Stellen:
- 1, Schritt 3: `UEBERGABE.md` ohne Datum;
- 2: Träger;
- Schritt 4: Soll/Ist-Abgleich und Füllstand.

B3. DOKUMENTATIONSSTANDARD 6 und 9: nach Teil E. In Regel 9 heisst die Ausnahme „Backlog Abschnitt 8“ jetzt `BACKLOG_ERLEDIGT_2026-09.md` (Abschnitt 8).

B4. PRUEFPRINZIPIEN und Register: **keine Änderung** aus Teil E.

Ist eine Stelle aus Teil E im Regelwerk nicht auffindbar oder nicht eindeutig ⇒ nicht raten. Die Stelle in `b_offen.txt` nennen und im Ergebnis unter „Für Fable“ eintragen.

Nachweis: je geänderter Stelle der Satz davor und danach in `docs/belege/TB-119/b_stellen.md`. Dazu `numstat` je Datei. Entfernt werden dürfen nur Sätze, die Teil E ausdrücklich ersetzt, und jede entfernte Zeile steht in `b_stellen.md`.

Commit `TB-119 B Regelwerk nach 27b Teil E`.

## Schritt C — 13 fehlende Regeln aus D2

Eingetragen werden alle Regeln mit Status **FEHLT** aus `d2_fehlende_regeln.txt`, **ausser 19/6**. Das sind 13:
- 19/5, 21/1, 21/2, 21/3, 21/4, 21/6, 21/7;
- 21b/1, 21b/5;
- 24/4, 24/5, 24/6, 24/R2.

Zielorte nach dem Vorschlag am Ende der Datei:
- Messen und Belege ⇒ PRUEFPRINZIPIEN (19/5, 21/4, 24/4, 24/5);
- Umgang mit Fable ⇒ ARBEITSWEISE 15 oder 21 (21/1, 21/2, 21/3, 21/7, 24/R2);
- Schreiben auf Dateien und Nachträge ⇒ ARBEITSWEISE 14 (21b/1, 21b/5, 24/6);
- Sichtschutz-Meldung ⇒ ein Verweis auf Register 27.5 (21/6), ohne den Registertext zu wiederholen.

Den Wortlaut jeder Regel vorher in der Übergabe an der genannten Stelle nachlesen, nicht aus der Kurzfassung in `d2_…txt` übernehmen. Jede Regel trägt ihre Herkunft: Übergabe, Block, Nr.

Fundstelle von 19/5 und 24/5: Die Kurzbeschreibung in D2 ist knapp. Ist der Sinn nach dem Nachlesen nicht eindeutig ⇒ nicht eintragen, in `c_offen.txt` nennen und im Ergebnis unter „Für Fable“ eintragen.

C2. **19/6** nicht eintragen. Stattdessen an `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md`, Abschnitt D, anhängen, nur anhängen:
- Eintrag „27.09., TB-119: D2 19/6 gegen ARBEITSWEISE 6d“;
- die beiden Wortlaute mit Fundstelle;
- den Hinweis, dass K2h im Backlog auf „ARBEITSWEISE §7c“ verweist, wo nichts steht;
- die Frage, welche Regel gilt.

Nachweis: `numstat` der Sammlung zeigt `n/0`.

C3. Die acht Regeln mit Status **TEILWEISE** (19/2, 19/3, 19/7, 19/K, 21/5, 21b/4, 24/1, 24/7) bleiben unverändert. Sie werden im Ergebnis mit ihrer Fundstelle aufgeführt.

Commit `TB-119 C 13 Regeln aus D2`.

## Schritt D — Ergebnis

`docs/ERGEBNIS_TB-119_repo_nachziehen_regelwerk_nachtrag.md` mit diesen Teilen:
- Schritte 0–C mit Nachweisen;
- Abschnitt „Für Fable“: alles, was offen blieb. Das kommt am Dienstag in die Sammlung;
- „Nicht getan, und warum“;
- „In einfacher Sprache“.

Journal-Eintrag wie üblich. Abgabe-Commit, danach pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- Ein md5 in Schritt 0 oder A1 weicht ab.
- Eine Änderung würde das Register, Code des Laufs, die Sperrliste, `crontab` oder eine Datenbank berühren.
- Eine Stelle aus Teil E setzt eine Entscheidung voraus, die weder Teil E noch dieser Auftrag trifft ⇒ nicht entscheiden, melden. Die übrigen Stellen werden trotzdem umgesetzt.
