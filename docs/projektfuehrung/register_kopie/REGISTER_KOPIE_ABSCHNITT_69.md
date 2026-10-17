# REGISTER-KOPIE Abschnitt 69 (von 0–71) — Register-Z. 12820–12880 — Commit fd8f27705d7c47212587c0d7b475c3be206dd989 — 2026-10-17 — Original sha256 df17ea87835b662c960e35a530035f06359fb7ac6d0042bef5d37fe0c00ef837 — KOPIE, nicht das Register

## 69. Fable 17d — Registerblock R109 (TB-178)

Reines Eintragen von Registertext, Bauart wie 67 und 68. Quelle ist allein `docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md`, md5 `3b886ee769174d7c474679dd4452c9eb`, 6 141 B, Abschnitt „Registerblock — zeichengleich kopierbar, nummeriert (ab R109)“, Z. 15–18, im Repo seit Commit `14833dd`. Nicht eingetragen werden „Kurz“, Erschlossenes, Leseprotokoll und Ampel der Antwort. Zum Dialog gehören die Anfrage 17.10.d (`docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md`) und die Übergabe 17.10.d (`docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md`), beide seit `14833dd`. Marken nach R109 (c). Karte des Betreibers (Auftrag TB-178, Abschnitt Freigabe, wörtlich): „Karte des Betreibers im Chat 35 („Opus Trading Bots-17.10.2026 b“), 17.10.2026, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript, Zeit 2026-10-17T20:15:56.508Z UTC): Your questions have been answered: "Gibst du TB-178 frei? Der Auftrag macht drei Dinge. (1) Er bringt Anfrage, Übergabe und Antwort von Fable 17.10.d und 17.10.e unverändert ins Repo, mit md5 vorher und nachher. (2) Er schreibt Register 69 (R109) und 70 (R110) zeichengleich aus den Antworten, dazu zehn Marken, Index und Kopien. (3) Er prüft am Mac den späten Symbolfall für t3_supertrend, elliott_wave und elliott_wave_stocks: mit und ohne Schranke bytegleich, dazu die Gegenprobe in beide Richtungen. Die Probe liegt mit Prüfzahl im Repo. In der Simulation lief t3 58/58 und elliott_wave 11/11 bytegleich, und die Gegenproben schlugen an. Ist die Prüfung grün, ist die Bedingung des Tags aus R105 (c) für alle drei Bots erfüllt. Kein Handelscode, keine Kursdaten aus data/, kein Geld. Das Startkapital (Sperrliste, Konstante, Test-Anpassung) ist Handelscode und kommt als eigener Auftrag TB-180 mit frischem Gegenleser. bau.sh endet mit rc 0, simuliert auf dem Gerät mit Python 3.10, am Mac läuft 3.9. Gesendet wird erst nach einer eigenen Karte „Senden?“. TB-179 (Regeln der KI-Forschung) folgt danach; ich passe ihn an den neuen Stand an. Empfehlung: freigeben."="Freigeben (Recommended)". You can now continue with these answers in mind.“ Eingetragen am 17.10.2026 mit TB-178.

### 69.1 R109 — Berichtigung („lies“) und Ergänzung zu R108 (d) (Startkapital: 59.1 ist Beleg, kein Ort); Ergänzung zu R108 (e) und R107 (b)…

> R109 — Berichtigung („lies“) und Ergänzung zu R108 (d) (Startkapital: 59.1 ist Beleg, kein Ort); Ergänzung zu R108 (e) und R107 (b) (67.1), Berichtigung („lies“) zu R106 (c) (66.1) (der späte Symbolfall). (a) Startkapital. In R108 (d) lies „dass am Stand 7fe6342 kein Abschnitt einen Wert für das Startkapital nennt; nennt einer ihn, ist er der Ort“ als „dass am Stand 7fe6342 kein Registertext und keine Festlegung einen Wert für das Startkapital festlegt; eine Tatsachennotiz, die den Wert nennt, ist Beleg, kein Ort“. So gelesen ist sie gemessen erfüllt (Anfrage 17.10.d: einziger Treffer mit Wert ist 59.1; 29.2: 0). 59.1 legt nichts fest: sie berichtet den Parameter einer Messung ausserhalb des Laufcodes (24.6) und nennt weder Modul noch Konstante (37.5 (1)); sie bleibt zeichengleich, ohne Marke (R96 (d)). Die Reihenfolge aus R108 (d) bleibt. Der Registertext nach (1) lautet als Ergänzung zu 29.3: „Das registrierte Startkapital ist 10 000, wie der Code es am Commit der Tatsachennotiz in den neun strategies/<bot>/equity_simulation.py trägt; sein Ort ist eine Konstante im Modul aus 38.5, mit Hash auf der Sperrliste; die Sonde prüft Datei und Wert (37.5 (1)).“ Eingetragen wird er, wenn die Tatsachennotiz nach R108 (d) (1) die neun Fundstellen mit Commit nennt; bis dahin ist ihre Gleichheit Vormessung an einer Kopie. Die dritte Konstante im Modul aus 38.5 ist eine beauftragte Änderung nach 37.3; Name und Docstring sind Handwerk. 59.1 ist Beleg, nicht Grund. (b) Später Symbolfall. Die Prüfung nach R108 (e) läuft an einem Symbol, dessen Reihe vor seinem Handelbar-Tag (R87 (a): je Symbol, aus der Rechnung nach 23.5, R87 (c)) kein Einstiegssignal des Bots trägt (R90 (g) nach R107 (b)); der Tag gilt nur diesem Symbol. Der Fall wird herbeigeführt (R106 (b)): ein eingesetztes Symbol mit spätem Datenbeginn, ohne Signal bis zum Handelbar-Tag. Beide Läufe mit Wachen nach R86 (d) und R87 (c): mit Schranke rc 0, Zählzeile 0; ohne Schranke rc 0, Ausgaben bytegleich. Endet der Lauf ohne Schranke mit 2 oder entfernt die Schranke Zeilen, trägt das Symbol Signale vor dem Tag; das ist der Verdrängungsfall nach R105 (c) (TB-171, TB-174), nicht dieser. Ein von einem Test gesetzter Tag ist kein Handelbar-Tag nach R87 (a). [Voraussetzung, zu messen, nur das Wie: woher TB-169 3b und die Probe den Tag des späten Symbols nehmen — aus der Rechnung nach 23.5 oder gesetzt.] Stand: elliott_wave_stocks erfüllt mit TB-169 3b (6 von 6, bytegleich, 0 entfernt), unter dieser Voraussetzung; t3_supertrend und elliott_wave am gebauten Fall. In R106 (c) lies „Die Gleichheit der Ausgaben mit und ohne Schranke an einem Symbol ohne Signal vor dem Tag steht mit TB-169 (Prüfung 3b, nach der Wiedergabe in der Anfrage 17.10.a).“ als „… steht für elliott_wave_stocks mit TB-169 3b; für elliott_wave wird sie am gebauten Fall gezeigt (R109 (b)).“ Weg 1 bleibt für alle drei Bots geschlossen; die Bedingung des Tags aus R105 (c) ist für elliott_wave_stocks erfüllt, für t3_supertrend und elliott_wave offen bis zur Prüfung. Die Voraussetzung in R107 (b) ist gemessen nicht erfüllt. R106 (c) im Übrigen und R107 (b) bleiben zeichengleich. Zählung: kein Fall; sechzehn. (c) Marken, der alte Satz bleibt zeichengleich: R108 (sobald eingetragen) — BERICHTIGT durch R109, Unterpunkt (a); ERGÄNZT durch R109, Unterpunkte (a) und (b). 29.3 — ERGÄNZT durch R109, Unterpunkt (a). 66.1 (R106) — BERICHTIGT durch R109, Unterpunkt (b). 67.1 (R107) — ERGÄNZT durch R109, Unterpunkt (b). Ohne Marke: 59.1, 29.2, 24.6, 37.3, 37.5, 38.5, 23.5, 56.3 (R86), 56.4 (R87), 57.1 (R90), 65.2 (R105), 66.2, 67.2, Abschnitt 10.
> Quelle des Grundes: 29.2, 29.3, 37.5, 38.5, 59 und 59.1 im Wortlaut, 24.6 und R96 (d) nach 59, R86 (d), R87 (a), (c), R106 (b), (c), R107 (b), (e), 67.2, R108 (d), (e), R90 (g), R105 (c) und 23.5 nach Wiedergabe, die Anfrage 17.10.d (Treffer, Code, BAU176 nach Wiedergabe). 23, 57, 65 und Code nicht gelesen. Kein Ergebnis.

> ⭐ **69.1 R109 BERICHTIGT und ERGÄNZT durch R110 (70.1)** (Fable 17e R110, Unterpunkte (a) und (b): BERICHTIGT („lies“); Unterpunkte (a) bis (c): ERGÄNZT, TB-178, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Kette:** Marken nach R109 (c): 68.1 (R108), Unterpunkt (a) berichtigt, Unterpunkte (a) und (b) ergänzt; 29.3, Unterpunkt (a); 66.1 (R106), Unterpunkt (b), berichtigt; 67.1 (R107), Unterpunkt (b). Ohne Marke: 59.1, 29.2, 24.6, 37.3, 37.5, 38.5, 23.5, 56.3 (R86), 56.4 (R87), 57.1 (R90), 65.2 (R105), 66.2, 67.2, Abschnitt 10. Zählung: kein Fall; sechzehn (R109 (b)).

### 69.2 Voraussetzungen und Befunde

Gemessen vor dem Eintrag mit `docs/belege/TB-178/v_voraussetzung.txt` (Werkzeug `voraussetzung`, Anhang A des Auftrags TB-178), Zeilen wörtlich:

    ja    unveraendert: research/exposure_messung/bot_lauf.py md5 01fd9282ded2
    ja    unveraendert: research/faltenplan_neun/faltenschranke_messung.py md5 584d9ff959da
    ja    unveraendert: research/tb24_haltedauern/haltedauer_kern.py md5 60942de99b32
    ja    unveraendert: research/tb24_haltedauern/positionen_holen.py md5 006375593b4b
    ja    unveraendert: research/tb24_haltedauern/test_listen_erzeuger.py md5 d77e73ed5ff7
    ja    unveraendert: strategies/elliott_wave/multi_symbol_optimise.py md5 bf11370b140d
    ja    unveraendert: strategies/elliott_wave_stocks/multi_symbol_optimise.py md5 571076168d56
    ja    unveraendert: strategies/t3_supertrend/multi_symbol_optimise.py md5 dc85993e8d42
    ja    BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-178
    ja    Journal: hoechste FN (FN am Bau-HEAD)
    ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17d_r108d_startkapital_r108e_spaetes_symbol.md verfolgt, gleich HEAD, md5 007196934a22163335439c2888886047
    ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-17d_59_1_beleg_kein_ort_spaetes_symbol_gebaut.md verfolgt, gleich HEAD, md5 3b886ee769174d7c474679dd4452c9eb
    ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17d_eroeffnung.md verfolgt, gleich HEAD, md5 b968fc124c5361f03e0f1118fdec1994
    ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANFRAGE_2026-10-17e_r109_tag_gesetzt_sperrliste_sonde.md verfolgt, gleich HEAD, md5 36389b7829a6e77c3ebe327fc58b7d25
    ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_ANTWORT_2026-10-17e_drei_bots_am_fall_punkt9_pfad_sonde_wert_probe_handwerk.md verfolgt, gleich HEAD, md5 1d964b3107485a44ba29467ebc56c34a
    ja    R56 (b)/S0-Datei: docs/projektfuehrung/FABLE_UEBERGABE_2026-10-17e_eroeffnung.md verfolgt, gleich HEAD, md5 a204bed16a9f30adda7c2b34489856ba
    ja    Registerblock 17d: genau R109 und Quelle im Codeblock (Z. 15–18)
    ja    Registerblock 17e: genau R110 und Quelle im Codeblock (Z. 17–20)
    ja    Register: 68 da, 69 und 70 nicht; R109/R110 0 Treffer
    ja    Register endet mit genau einer Leerzeile
    ja    Ort 68.1 (R109): Einfuegestelle vor Z. 12725 eindeutig, R109 dort noch nicht genannt
    ja    Ort 29.3 (R109): Einfuegestelle vor Z. 5458 eindeutig, R109 dort noch nicht genannt
    ja    Ort 66.1 (R109): Einfuegestelle vor Z. 12590 eindeutig, R109 dort noch nicht genannt
    ja    Ort 67.1 (R109): Einfuegestelle vor Z. 12659 eindeutig, R109 dort noch nicht genannt
    ja    Ort 66.1 (R110): Einfuegestelle vor Z. 12590 eindeutig, R110 dort noch nicht genannt
    ja    Ort 37.2 (R110): Einfuegestelle vor Z. 7034 eindeutig, R110 dort noch nicht genannt
    ja    Ort 37.5 (R110): Einfuegestelle vor Z. 7288 eindeutig, R110 dort noch nicht genannt
    ja    Ort 29.3 (R110): Einfuegestelle vor Z. 5458 eindeutig, R110 dort noch nicht genannt
    ja    Ort 38.5 (R110): Einfuegestelle vor Z. 7554 eindeutig, R110 dort noch nicht genannt
    ja    Index-Kopf Z. 3 nennt 0–68
    ja    Index: Zeile 68, Pflegezeile TB-176a, Pflege-Anker, Abschnitt 19 je genau einmal; kein Abschnitt 20
    ja    Dialog-Index: 17d und 17e noch nicht
    ja    R109 (b) Voraussetzung lesbar: research/tb24_haltedauern/test_listen_erzeuger.py hb() und Pruefung 3b je genau eine Zeile
    info  R109 (b) Voraussetzung (Messung, kein Urteil; R110 (a): gesetzt): research/tb24_haltedauern/test_listen_erzeuger.py Z. [76] `x.update(t)` in hb() - die vom Test uebergebenen Tage ueberschreiben die Rechnung; Z. [161] Pruefung 3b setzt den Tag von CCC (`json.dumps({"CCC": ...})`)
    ja    Probe noch nicht im Repo (docs/belege/TB-178/tb178_probe_spaetes_symbol.py)
    Pruefungen: 34, NEIN: 0

(a) R109 (b), Voraussetzung (nur das Wie), gemessen durch Lesen am Commit `14833dd`: `research/tb24_haltedauern/test_listen_erzeuger.py` setzt den Tag selbst — `hb()` überschreibt die Rechnung mit den vom Test übergebenen Tagen (`x.update(t)`, Z. 76), Prüfung 3b übergibt den Tag von CCC (Z. 161). Ergebnis: gesetzt; so eingetragen in R110 (a) (70.1).

(b) R109 (a): Der Registertext zu 29.3 wird mit TB-178 nicht eingetragen; er folgt dem Bauauftrag nach 37.3 aus R110 (b) (70.1) in der dort berichtigten Fassung.

(c) R56 (b): Anfrage, Antwort und Übergabe 17.10.d liegen seit `14833dd` im Repo (aus `data_sicherung/steuernder_chat_tmp/f17d/`, md5 vorher = nachher, `docs/belege/TB-178/0a_md5.txt`).

