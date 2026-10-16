## FE — TB-166: E-3a Schranke je Symbol im Signalpfad und gemeinsame Tag-Rechnung `handelbar_ab` (Neubau auf e654b08)
*Quelle: `docs/ERGEBNIS_TB-166_e3a_schranke_je_symbol.md`, Commits `57a1062` (S0), `ad6ea95` (S), `15f28e4` (E), F = der Abgabe-Commit „TB-166 Abgabe: Ergebnis, BACKLOG, Journal FE“, der diesen Block enthält.*

**Quelle:** E-3a nach PLAN_E3 Teil E-3a, Register R90 (c)–(e), R98 (a)–(c), 37.3; Neubau nach dem Abbruch in E (`5167e96`) und der Abhilfe TB-167 (`b6aaa24`, Register 63). 20 Dateien geändert, nur über `WZ e3a` (18 davon auf der Sperrliste, Punkte 9/11), zwei neue Tests. Freigabe: Karte des Betreibers im Chat 31, 16.10.2026, 15:12 („Neu, bedingt“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD `e654b08`, zwei Einträge wie Soll, Karte gefüllt; die fünf Anhänge mit den Soll-sha256.
- V: 25 Prüfungen, NEIN 0, rc 0.
- S: `s0_vorab.txt` zeilengleich mit dem Bau: 30 Wechsel, alle von einem Tag am oder nach dem Schnitt auf None, `alte Rechnung >= Schnitt: 30`; rc 0.
- E: Referenz der alten Bahn vor dem Patch (9 Bots, rc 0; `e_ref_alt.json` bytegleich zum Lauf von `5167e96`); `WZ e3a --probe` 22/0, `WZ e3a` 42/0, alle 20 Hashes vorher/nachher wie im Bau.
- E: neue Tests `test_handelbar_tag.py` 11 von 11, `test_schranke_signalpfad.py` 47 von 47; elf alte Tests rc 0, darunter `test_vorregistrierung.py` 196/196 (G6 grün, im Hintergrund, über 600 s), `test_arbeitsbaum_laufbereich.py` 26/26 (K0 rc 0).
- Entwurf der Tatsachennotiz nach 37.3 (`e_notiz.md`, Commit `15f28e4`) steht im Ergebnis.
- BACKLOG: Rang 1 nachgetragen.

### Was offen bleibt
- Registereintrag der Tatsachennotiz (Folgeauftrag, wie TB-122 → 50.3).
- Ein neues Sperrlisten-Abbild unter neuem Namen erst vor dem Tag (37.3).
- E-3b (Listen-Erzeuger); die Abnahme nach R98 (d) erfolgt erst mit E-3b am Erzeuger.

### In einfacher Sprache
Die neun Bots rechnen jetzt den Tag, ab dem ein Symbol handelbar ist, mit einer einzigen gemeinsamen Funktion und nur aus Kursdaten vor dem 01.09.2026. Im Scan lässt jeder Bot vor diesem Tag keinen Einstieg zu. Wo früher zu frühe Trades hinterher gestrichen wurden, bricht der Lauf jetzt mit einem Fehler ab. Alle Tests mit erfundenen Kursreihen und alle alten Tests sind grün. Kein Bot lief auf echten Daten. Alte und neue Prüfsummen der geänderten Dateien stehen als Entwurf im Ergebnis; ins Register kommen sie in einem eigenen Auftrag.

*Geschrieben 16.10.2026 von der Mac-Sitzung TB-166. Quellenvermerk: siehe Kopf.*
