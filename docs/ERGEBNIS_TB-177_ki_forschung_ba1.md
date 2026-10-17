# Ergebnis TB-177 — KI-Forschung BA1: `ki_forschung/` (Abruf- und Einfrierschicht, Aufrufbuch mit Kostenbremse, Wachen-Test)

**Sitzung:** Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-177_ki_forschung_ba1.md` · **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9.6) · **Belege:** `docs/belege/TB-177/`

**Commits (alle auf `main`, gepusht):**

| Schritt | Commit | Inhalt |
|---|---|---|
| S0 | `8d739b7` | Auftrag (und `AKTUELLER_AUFTRAG.md`) |
| B | `57637b4` | `ki_forschung/` (pfade, abrufe, aufrufe, test_ki_wachen) und Belege 0a, V, B, T |
| A | dieser Commit | Ergebnis, BACKLOG, Journal FN |
| F | folgt | porcelain und numstat |

## Kurz

Alle Schritte liefen ohne Abbruch und ohne Nachfrage. Die vier Dateien unter `ki_forschung/` sind sha256-gleich mit den Anhängen. Der Wachen-Test meldet auf 3.9.6 `Pruefungen: 50, FEHLT: 0` mit rc 0, alle 17 Gegenproben werden rot. Es wurde keine `abrufe.db`/`aufrufe.db` und kein `__pycache__` angelegt. Kein echter Abruf, kein API-Aufruf, kein Schlüssel gelesen, kein Handelscode berührt.

**Eine Abweichung im Wortlaut, nicht im Ergebnis (T):** Das Soll nennt `Pruefungen: 50, FEHLT: 0` als *vorletzte* Zeile von `t_wachen.txt`. Tatsächlich ist es die drittletzte: Der `finally`-Block des Tests selbst (`ki_forschung/test_ki_wachen.py` Z. 646, so auch im Anhang D) gibt danach noch `temporaere Ordner entfernt: 18` aus, und erst dann folgt `rc 0`. Der Test ist also wie gebaut gelaufen; das Soll beschreibt seine Ausgabe nur ungenau. Die Sitzung hat das nicht als „T nicht wie Soll“ gewertet und weitergemacht. Der A-Befehl liest die Zeile per Regex aus der ganzen Datei (`N = 50`).

## Schritt 0

0a: `0a gut (2 Eintraege)` (` M docs/auftraege/AKTUELLER_AUFTRAG.md`, `?? docs/auftraege/MAC_TB-177_ki_forschung_ba1.md`). Holbefehl: vier Anhänge mit den Soll-sha256, `Dateien 4`. Nach S0 war `git status --porcelain` leer.

## Schritt V

`v_voraussetzung.txt` wörtlich:

```
ja   md5 shared/claude_client.py = Bau
ja   md5 notifications/monitor.py = Bau
ja   md5 shared/paths.py = Bau
ja   ki_forschung/ fehlt
ja   kein Modul in shared/strategies/notifications nennt ki_forschung []
Pruefungen: 5, NEIN: 0
rc 0
```

## Schritt B

`b_sha.txt` wörtlich:

```
pfade.py aa64fab44b4be80a8b2a74d55487ac91ff202ba01fdd6811ba2afe11db6b47a6
abrufe.py 8e18fc3ccf60dc4fd561c5e118ce8eff5444da2a432c8ee71d32d78051a8d83c
aufrufe.py 88dfdb05b0f972dc3ed93abaa1c28c3858a3ed0e8362388c2e12c30687a0f337
test_ki_wachen.py 40b7a2b9c525495a5a5bb1f897b84ed42b56dcf7877dc8d9b1acc0c126bfaa46
rc 0
```

## Schritt T

`t_wachen.txt` wörtlich:

```
Wachen-Test KI-Forschung (TB-177)  Repo /Users/jaquelineloffler/trading-bot

W1 Importe
  ok   W1 nur Importe der Positivliste (4 Dateien)

W2 Schreibziele (statisch)
  ok   W2 keine fremden Schreibziele, connect nur in verbinden(), kein open()
  ok   W2b abrufe.db und aufrufe.db liegen in ki_forschung/   ('/Users/jaquelineloffler/trading-bot/ki_forschung/abrufe.db', '/Users/jaquelineloffler/trading-bot/ki_forschung/aufrufe.db')

W3 Erkennung und Laufbereich
  ok   W3 nicht in strategies/, ASSET_CLASS, Laufbereich; kein Modul in shared/strategies/notifications nennt ki_forschung

W5 Schluessel und Websuche
  ok   W5 kein os.environ, keine .env, kein email_config, keine Websuche

W4/W6 Laufzeit mit Attrappe (temporaere DBs)
Agent ki_bots abgeschaltet (config/agenten_aus.txt)
  ok   W4a normaler Aufruf: abgerechnet, Monatssumme = echter Preis
  ok   W4b Modell = MODEL_HAIKU, tools=None an call_claude
  ok   W4c Bremse stoppt vor dem Deckel (Summe <= 3 $, nicht zu frueh, gebremster Aufruf ohne Attrappe)
  ok   W4d Aufruf, dessen Hoechstpreis den Rest uebersteigt, wird gebremst; Attrappe nicht gerufen
  ok   W4e Toepfe getrennt: voller Topf sammler bremst ki_bots nicht
  ok   W4f Monatswechsel (UTC): neuer Monat beginnt bei 0
  ok   W4g Notschalter ki_bots: kein Aufruf
  ok   W4h Fehlerpfad: Reservierung bleibt stehen (zu viel, nie zu wenig)
  ok   W4i aufrufe.db nur anfuegend (UPDATE und DELETE abgewiesen)
  ok   W4k max_tokens negativ, 0, Kommazahl, bool, None, Text und Nicht-Text-Eingaben: ValueError vor jeder Buchung, Attrappe nie gerufen
  ok   W4l aufrufe.db CHECK: negative Kosten, max_tokens 0/-5/2.5 abgewiesen
  ok   W4j unbekannter Topf abgelehnt
  ok   W6a einfrieren: sha256 der Rohkopie
  ok   W6b Vintage: Stand am 17.10. ist der Abruf vom 17.10., vorher keiner
  ok   W6c Ausfall wird gebucht, nicht geworfen; Stand bleibt beim letzten guten
  ok   W6d abrufen mit Attrappe friert ein
  ok   W6e abrufe.db nur anfuegend
  ok   W6f unbekannte Quelle abgelehnt
  ok   W6h Zeitgrenze als Zeitpunkt (Abruf 12:00:00,5; Z, +02:00, Komma, datetime, ohne Zone abgewiesen)
  ok   W6j Abrufzeit und Buchungszeit nicht vom Aufrufer setzbar
  ok   W6g abrufe.db: INSERT OR REPLACE mit vorhandener id abgewiesen, Zeile 1 unveraendert
  ok   W6i abrufe.db: Abrufzeit ausserhalb des festen Formats abgewiesen (CHECK)
  ok   W6g aufrufe.db: INSERT OR REPLACE auf eine Abrechnungszeile abgewiesen, Summe unveraendert
  ok   W2c Laufzeit: jedes connect/open zum Schreiben im temporaeren Ordner (175 Zugriffe)
  ok   W2e Laufzeit: kein Netz (urlopen nie gerufen)
  ok   W2f Code unter shared/, strategies/, notifications/ vorher = nachher (239 Dateien, Groesse/mtime/sha256)
  ok   W2d Laufzeit: echte abrufe.db/aufrufe.db nicht angelegt

G Gegenproben (verfaelschte Kopien muessen rot werden)
  ok   G1 Import aus strategies/ -> rot   ['aufrufe.py:36 strategies.t3_supertrend']
  ok   G1b Import zuteilung -> rot   ['abrufe.py:26 zuteilung']
  ok   G2 Schreibziel Bot-DB -> rot   ["pfade.py:14 nennt 'paper_trading'"]
  ok   G2b connect ausserhalb verbinden() -> rot   ['abrufe.py:162 sqlite3.connect ausserhalb verbinden()']
  ok   G2c os.open -> rot   ['abrufe.py:106 .open']
  ok   G2d getattr(os, 'open') -> rot   ["abrufe.py:106 getattr(..., 'open')"]
  ok   G2e getattr mit Namen aus einer Variablen -> rot   ['abrufe.py:107 getattr mit Namen aus einer Variablen']
  ok   G5 Schluessel aus der Umgebung -> rot   ['aufrufe.py:174 os.environ']
  ok   G5b Websuche als Werkzeug -> rot   ['aufrufe.py:204 tools= nicht None', "aufrufe.py:204 nennt 'web_search'"]
  ok   G4 Bremse ausgebaut -> Summe ueber dem Deckel (rot)
  ok   W4m Code-Pruefung ausgebaut: CHECK in aufrufe.db weist die negative Reserve allein ab
  ok   G7 Pruefung und CHECK ausgebaut -> negative Buchung, danach mehr als 3 $ echt ausgegeben (rot)   (7, 7.000006999999999)
  ok   G2f Laufzeit: os.open ausserhalb des temporaeren Ordners -> rot   ['/var/folders/b_/yqcfpq996cxb1_v02m180f580000gn/T/tb177_gp_h7om5t14/fremd_g2f.txt']
  ok   G6 abrufe ohne Ersetzungsschutz -> W6g rot   (True, False)
  ok   G6c aufrufe ohne Ersetzungsschutz -> W6g rot   (True, 0.003852, 0.003502)
  ok   G6b Zeitgrenze als Text -> W6h rot   ['12:00:00Z', '12:00:00,5Z', '14:00:00+02:00', 'datetime 12:00:00.5 UTC', 'ohne Zeitzone -> ValueError']
  ok   G3 Laufbereichsmodul nennt ki_forschung -> rot
  ok   G3b ki_forschung unter strategies/ -> rot

Pruefungen: 50, FEHLT: 0
temporaere Ordner entfernt: 18
rc 0
```

`t_status.txt`: genau `?? docs/belege/TB-177/` und `?? ki_forschung/`. `ki_forschung/` enthielt nach dem Test nur die vier `.py`-Dateien.

## Schritt A

`a_backlog_journal.txt`: `Kennung FN`, `Pruefungen: 6, NEIN: 0`, `rc 0`. Die BACKLOG-Zeile hängt an der Rang-1-Zelle nach dem TB-176a-Anker, der Journal-Block FN steht vor `## Wiederkehrende Lehren`. Die nächste Kennung ist FO.

## Offene Entscheide (nicht in diesem Auftrag entschieden)

- **E1 Preis:** Haiku 1 $ / 5 $ je Million Token steht als Konstante in `aufrufe.py`. Er stammt aus der Preisliste und ist nicht im Repo gemessen. Der Betreiber bestätigt ihn vor dem Erstlauf (BA7). Steht ein Modell nicht in der Tabelle, wird nicht aufgerufen.
- **E2 Notschalter-Namen:** `ki_sammler` und `ki_bots` in `config/agenten_aus.txt`; BA1 ändert die Datei nicht.
- **E3 Höchstpreis:** Eingabe-Bytes als Token-Obergrenze plus `FORMAT_ZUSCHLAG_TOKEN` = 500 (gewählt, nicht gemessen; BA7 misst `usage.input_tokens` gegen die Bytes). Abgerechnet wird der echte Preis, deshalb kann ein einzelner Aufruf den Deckel um den Fehler seiner Schätzung überschreiten (bewusst so).
- **E4 Monatsgrenze:** UTC-Monat, nicht Berlin.
- **E5 Laufbereich:** `ki_forschung/` liegt bewusst ausserhalb von `ARBEITSBAUM_PFADE` (`shared/paths.py` Z. 239); die Sauberkeitsprüfungen der neun sehen es nicht.
- **E6 Kollisionen aus PLAN_KIBOTS** (MI1 (b)/K24, R107 (d), 16.8/16.9) betreffen BA4, nicht BA1.
- **E7 R108 (b)** (BACKLOG Rang 1, TB-176a) betrifft BA2/BA3, nicht BA1.
- **Neu, für den steuernden Chat:** Das Soll zur T-Ausgabe (siehe Kurz) sollte in Folgeaufträgen „drittletzte Zeile“ oder „Zeile vor `temporaere Ordner entfernt`“ heissen.

## In einfacher Sprache

Der neue Ordner für die KI-Versuche steht jetzt im Repo, getrennt von den neun Bots. Er enthält einen Datenspeicher, der festhält, was wann bekannt war, und ein Kostenbuch, das jede Anfrage an das KI-Modell vorher gegen einen Monatsdeckel von 3 $ prüft, getrennt für Sammler und KI-Bots. Heute wurde nichts abgerufen und nichts bezahlt. Der Selbsttest hat mit Attrappen 50 Punkte geprüft, alle grün: Der Ordner berührt die neun Bots nicht, liest keinen Schlüssel und sucht nicht im Netz, und die Bremse greift. An absichtlich verfälschten Kopien schlägt der Test wie gewollt an. Auffällig war nur eine Kleinigkeit im Auftragstext: Er hatte eine Ausgabezeile des Tests an der falschen Stelle erwartet.
