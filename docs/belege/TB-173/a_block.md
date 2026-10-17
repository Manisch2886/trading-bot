## FJ — TB-173: Register 66 (Fable 17a, R106: Lesart „spätere Welle“, Test-Snapshot, Stand), vier Marken, Voraussetzung R106 (c) am Code gemessen, Tatsachennotiz TB-172
*Quelle: `docs/ERGEBNIS_TB-173_register66_fable17a.md`, Commits `f79f239` (S0, Fable 17.10.a und Auftrag), `7fe6342` (R, Register 66 und vier Marken), `ae5c151` (K, Registerkopie, Index, Dialog-Index), danach der Abgabe-Commit „TB-173 Abgabe: Ergebnis, BACKLOG, Journal FJ“, der diesen Block enthält.*

**Quelle:** Fable-Antwort 17.10.a (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-17a_r105c_elliott_geschlossen_t3_weg1.md`, md5 `e222920f…`), Registerblock Z. 28–31; R56 (b); Bauart 65 (TB-170). Alles über `WZ` (Anhang A des Auftrags, sha256 `2a0fc391…`). Freigabe: Karte des Betreibers im Chat 33, 17.10.2026, 16:27 („Freigeben“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `d81ef20`, genau fünf Einträge wie Soll, Karte gefüllt; Anhang mit Soll-sha256 (`Dateien 1`); `WZ md5` 3/0, rc 0. S0 = `f79f239` mit den drei Fable-Dateien 17.10.a unverändert, porcelain danach leer.
- V: 34 Prüfungen, NEIN 0, rc 0. Darunter R106 (c), Voraussetzung, nur das Ob: Stand der Probe (sha256 von Probe, Test, Erzeuger wie TB-171); in Prüfung 1 ruft die Probe den Erzeuger mit leerem Modus, der Test ersetzt die Wachen nur in „wache1_aus“/„wachen_aus“, `positionen_holen.main` ruft `wache_zeilen` und `wache_trades` ohne Bedingung — Wachen eingeschaltet: ja. Die Probe bildet den Kursabschnitt selbst (`bauplan`, `einsetzen`) im Temp-Ordner; 9 Lesestellen, Wurzel nur Temp-Ordner, Repo oder Speicher; kein absoluter Pfad, kein `data/` des Repos — ja. **Teilmessung am Code**, keine Lesespur des Laufs.
- R: Register 66 ab Z. 12531 (66.1 Z. 12535, 66.2 Z. 12542), R106 und Quellenzeile je genau einmal zeichengleich; vier Marken an 57.1 (Z. 12006), 61.1 (Z. 12240), 64.1 (Z. 12455), 65.2 (Z. 12476); append-only bis auf die Marken; numstat Register 78/0. 8/0, rc 0.
- K: Registerkopie, Abschnittskopien (0–66, 67 Dateien) und Prüfung je BYTEGLEICH, rc 0; Index-Zeilen 471 Zahlen, 11 geändert; Index 5/0 (Zeile 66 zu T6, neuer Abschnitt 17 mit 4 Marken); Dialog-Index 67 von 67, rc 0.

### Was offen bleibt
- `t3_supertrend` nach R106 (d): Weg 1 (Fall auf dem Test-Snapshot herbeiführen) oder eine Tatsachennotiz, die `use_t3_exit` und den Gleichstand mit Fundstelle schliesst — Handelscode, eigener Auftrag mit Bau-Helfer und frischem Gegenleser.
- R102 (d)-Befund aus TB-172 als Frage an den Verfahrensprüfer mit der nächsten Anfrage.
- Vor der Neuerzeugung vier Leser von `<bot>_positionen.csv` auf `<bot>_alle_trades.csv` umstellen; ob `research/exposure_messung/auswertung.py` (eigene Liste) dazugehört, ist offen.
- Index-Kopf mischt weiter Stände (BACKLOG Rang 1, seit TB-170).

### In einfacher Sprache
Die neue Antwort des Verfahrensprüfers liegt jetzt mit Anfrage und Übergabe im Repo. Ihr Regeltext steht wortgleich als neuer Abschnitt im Register, nur angehängt, und an vier älteren Stellen weist ein Vermerk auf ihn hin. Er hält fest, dass bei den zwei Elliott-Bots ein zu früher Kauf keinen späteren mehr verdrängt. Vorher wurde am Programmtext der Probe geprüft, dass die Wächter dabei eingeschaltet waren und die Probe ihre Testkurse selbst baut. Für den T3-Bot ist noch ein eigener Code-Auftrag nötig, und vor dem Neuerzeugen der Listen müssen vier Leseprogramme umgestellt werden.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-173. Quellenvermerk: siehe Kopf.*
