# LÖSCHLISTE TB-118 — was die Projektablage verlassen darf, mit Bytes und geschätzten Tokens

*Erzeugt von `docs/belege/TB-118/f1_loeschliste.py` (TB-118 Schritt F, Fable 27b Teil D F1/F2), 27.09.2026. Geht in die Projektablage, damit der Betreiber per Auswahlkarte freigibt, und verlässt sie nach dem Vollzug (`ablage_ereignisse.json`).*

## ⚠️ Vor dem Vollzug

1. **Die Liste beruht auf einer rekonstruierten Ist-Liste**, nicht auf der Projektschnittstelle: Die Mac-Sitzung liest die Ablage nicht (`docs/belege/TB-118/e3_ist_rekonstruiert.txt`, 145 Pfade aus der Gruppentabelle der Anfrage 27b; einige Namen sind Annahmen). **Der steuernde Chat holt die echte Ist-Liste und lässt `python3 docs/werkzeuge/ablage_soll.py --ist <ist.txt> --aus <ordner>` laufen; entfernt wird nur, was in dessen `entfernen.txt` steht.** Diese Liste ist die Freigabegrundlage für die Klassen und Gründe, nicht für die einzelne Datei.
2. **Reihenfolge nach 27b C4:** zuerst ablegen (Tabelle „Rein“), dann entfernen, dann `knowledge_size` messen und eine Zeile in `UEBERGABE.md` schreiben. Nr. 2 (die drei Teile vom 24.09.) erst, wenn die vier neuen Teile liegen.
3. ⚠️ **Nicht im Repo** (G1: das Repo ist der Träger): `REGISTER_KOPIE_2026-09-21.md`, die drei Teile vom 24.09. und die zwei Belege `belege/TB-91_…`, `belege/TB-93_…` liegen nur in der Ablage. Die Registerkopien sind aus dem Registerstand ihres Tages rekonstruierbar (Register am `5ff34a4` bzw. an der Kopie vom 24.09. im Repo), nicht bytegleich (Kopf). **Vor dem Entfernen entscheiden: ins Repo holen oder ohne Kopie entfernen.** Auch `FABLE_ANTWORT_2026-09-25f` liegt nur in der Ablage — sie bleibt (Ereignis offen).
4. **Tokens sind geschätzt**, nicht gemessen — die Projektschnittstelle liefert nur Gruppensummen. *kalibriert* = Bytes ÷ 2.337 (Verhältnis aus vier Gruppen der Betreibermessung vom 26.09., die ganz im Repo liegen: `BACKLOG.md`, `UEBERGABE_*`, `ARBEITSWEISE.md`, `ERGEBNIS_TB-114…116`; Gegenprobe an der Register-Gruppe: dort rund 7 % zu hoch). *÷ 4* = die Näherung aus dem Auftrag; sie liegt gegen die Betreibermessung rund 40 % zu tief. Bytes: Fassung am `753ec11` (26.09., 22:34, der letzte Stand vor der Messung).

## Summen je Gruppe der Sofortliste (27b C3)

| Nr. | Gruppe | Dateien | Bytes | Tokens kalibriert | Tokens ÷ 4 |
|---|---|---:|---:|---:|---:|
| 1 | Registerkopien 21./22./24.09. (Ganzfassung) | 3 | 1 292 039 | ≈ 552 968 | 323 009 |
| 2 | Registerkopie 24.09. in drei Teilen | 3 | 552 129 | ≈ 236 301 | 138 032 |
| 3 | Fable-Dialog bis 25e | 81 | 727 700 | ≈ 311 442 | 181 925 |
| 4 | Aufträge MAC_TB-* und Nachtrag | 22 | 286 577 | ≈ 122 649 | 71 644 |
| 5 | Belege — davon 2 nicht messbar | 2 | 0 | ≈ 0 | 0 |
| 6 | Übergaben mit Datum | 2 | 101 254 | ≈ 43 334 | 25 313 |
| 7 | ereignisgebunden, Ereignis eingetreten | 3 | 39 743 | ≈ 17 009 | 9 935 |
| – | nicht in der Sofortliste C3 (Abweichung, e3_probe.txt) | 5 | 104 613 | ≈ 44 772 | 26 153 |
| | **Summe raus** | **121** | **3 104 055** | **≈ 1 328 478** | **776 013** |

## Rein (vorher ablegen)

| Datei | Bytes | Tokens kalibriert | Grund |
|---|---:|---:|---|
| `BACKLOG_ENTSCHEIDUNGEN.md` | 67 596 | ≈ 28 929 | B2 Stand |
| `FABLE_ANFRAGE_2026-09-27b_konzept_projektwissen.md` | 10 632 | ≈ 4 550 | B6 Dialog: Anfrage zur gehaltenen Antwort |
| `FABLE_ANTWORT_2026-09-27b_konzept_projektwissen.md` | 36 823 | ≈ 15 759 | B6 Dialog: Antwort 27b offen |
| `FABLE_DIALOG_INDEX.md` | 17 881 | ≈ 7 652 | B2 Stand |
| `KANDIDATEN_DURCHGANG_2.md` | fehlt im Repo | – | B2 Stand - FEHLT IM REPO |
| `MAC_TB-117_wachen_vor_dem_tag.md` | 13 868 | ≈ 5 935 | B4 Auftrag offen: zugehoerige Antwort 27a im Index offen |
| `MAC_TB-118_projektwissen_aufraeumen.md` | 11 423 | ≈ 4 888 | B4 Auftrag offen: kein ERGEBNIS_TB-118 |
| `REGISTER_INDEX.md` | 13 423 | ≈ 5 744 | B3 Register, Index |
| `REGISTER_KOPIE_teil1.md` | 239 529 | ≈ 102 514 | B3 Register, Teil |
| `REGISTER_KOPIE_teil2.md` | 220 905 | ≈ 94 543 | B3 Register, Teil |
| `REGISTER_KOPIE_teil3.md` | 227 107 | ≈ 97 197 | B3 Register, Teil |
| `REGISTER_KOPIE_teil4.md` | 59 998 | ≈ 25 678 | B3 Register, Teil |
| `UEBERGABE.md` | 27 632 | ≈ 11 825 | B2 Stand |
| `LOESCHLISTE_TB-118.md` (diese Datei) | 27 592 | ≈ 11 808 | F2, verlässt die Ablage nach dem Vollzug |
| `BACKLOG.md` wird **ersetzt** (gleicher Name) | 206 166 → 53 236 | ≈ −65 451 | Teilung, Schritt C |

## Erwarteter Stand danach (Schätzung, kalibriert)

`knowledge_size` am 26.09.: **1 540 610** von 2 000 000 (77 %). Danach ≈ 1 540 610 − 1 328 478 (raus) + 417 029 (rein) − 65 451 (`BACKLOG.md` kleiner) ≈ **563 709 ≈ 28 %**. Ziel ≤ 50 % (27b C2). *Nicht eingerechnet: was seit dem 26.09., 22:40 in die Ablage kam (z. B. Anfrage und Antwort 27b, falls schon abgelegt) — der steuernde Chat misst vorher und nachher.*

## Die Dateien, je mit Grund (Austrittsereignis nach 27b Teil B)

| Datei | Bytes | Tokens kalibriert | Tokens ÷ 4 | Nr. | Grund |
|---|---:|---:|---:|---|---|
| `projektfuehrung/REGISTER_KOPIE_2026-09-21.md` | 339 179 | ≈ 145 162 | 84 794 | 1 | B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md ⚠️ nicht im Repo |
| `projektfuehrung/REGISTER_KOPIE_2026-09-22.md` | 400 730 | ≈ 171 505 | 100 182 | 1 | B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md |
| `projektfuehrung/REGISTER_KOPIE_2026-09-24.md` | 552 130 | ≈ 236 301 | 138 032 | 1 | B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md |
| `projektfuehrung/REGISTER_KOPIE_2026-09-24_teil1.md` | ≈ 184 043 | ≈ 78 767 | 46 010 | 2 | B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md ⚠️ nicht im Repo |
| `projektfuehrung/REGISTER_KOPIE_2026-09-24_teil2.md` | ≈ 184 043 | ≈ 78 767 | 46 010 | 2 | B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md ⚠️ nicht im Repo |
| `projektfuehrung/REGISTER_KOPIE_2026-09-24_teil3.md` | ≈ 184 043 | ≈ 78 767 | 46 010 | 2 | B3 datierte Registerkopie - ersetzt durch REGISTER_KOPIE_teil<n>.md ⚠️ nicht im Repo |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-19_pruefungsregistrierung.md` | 5 467 | ≈ 2 339 | 1 366 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-20_benchmarkfenster.md` | 5 279 | ≈ 2 259 | 1 319 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-20b_wortlaut_nulltage.md` | 7 675 | ≈ 3 284 | 1 918 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-20c_kapitalpfad.md` | 8 154 | ≈ 3 489 | 2 038 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-20d_tagesreihe.md` | 6 453 | ≈ 2 761 | 1 613 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-20e_erste_falte.md` | 6 787 | ≈ 2 904 | 1 696 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-20f_nebenbedingung.md` | 5 547 | ≈ 2 374 | 1 386 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21a_horizont_und_grenzfall.md` | 8 169 | ≈ 3 496 | 2 042 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21b_messmeldung_vorlauf_und_kapitalpfad.md` | 5 201 | ≈ 2 225 | 1 300 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21c_einarbeitung_21i_und_manifest.md` | 11 868 | ≈ 5 079 | 2 967 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21d_21j_beauftragt_und_gemessen.md` | 6 696 | ≈ 2 865 | 1 674 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21e_abbilddatei_felder.md` | 8 125 | ≈ 3 477 | 2 031 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21f_registertext_und_feldliste.md` | 11 090 | ≈ 4 746 | 2 772 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md` | 8 599 | ≈ 3 680 | 2 149 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md` | 8 313 | ≈ 3 557 | 2 078 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md` | 6 610 | ≈ 2 828 | 1 652 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22c_herkunft_gemessen.md` | 9 059 | ≈ 3 877 | 2 264 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22d_klassifikation_berichtigt.md` | 6 029 | ≈ 2 580 | 1 507 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22e_zwei_messungen.md` | 6 175 | ≈ 2 642 | 1 543 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22f_kosten_gemessen.md` | 7 690 | ≈ 3 291 | 1 922 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22h_bezeichner_ist_schluessel.md` | 9 498 | ≈ 4 064 | 2 374 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-22i_slippage_ja_und_gruen_nein.md` | 10 053 | ≈ 4 302 | 2 513 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23b_tb72_erfuellt_es_aber.md` | 8 123 | ≈ 3 476 | 2 030 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23c_zwei_erzeuger_ungesichert.md` | 8 134 | ≈ 3 481 | 2 033 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23d_determinismus_erfuellt.md` | 7 249 | ≈ 3 102 | 1 812 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23e_dritte_leserin_eingefroren.md` | 6 700 | ≈ 2 867 | 1 675 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23f_eingefroren_ohne_eingaben.md` | 8 504 | ≈ 3 639 | 2 126 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23g_zwei_messbitten_beantwortet.md` | 7 512 | ≈ 3 214 | 1 878 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-23h_vollzug_im_code_nicht_im_register.md` | 6 583 | ≈ 2 817 | 1 645 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-24a_punkt8_vollzogen_test_gruen_neun_listen.md` | 15 663 | ≈ 6 703 | 3 915 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-24b_vierter_fall_und_ein_satz.md` | 7 813 | ≈ 3 343 | 1 953 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-24c_sieben_statt_acht.md` | 9 196 | ≈ 3 935 | 2 299 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-24d_stiller_rueckfall_im_modus.md` | 9 568 | ≈ 4 094 | 2 392 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-24e_richtiges_ergebnis_falscher_ort.md` | 8 564 | ≈ 3 665 | 2 141 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-25a_tagblocker_weg_zwei_lesarten.md` | 14 597 | ≈ 6 247 | 3 649 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-25b_laufbereich_gemessen_fuenf_fragen.md` | 12 438 | ≈ 5 323 | 3 109 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-25c_rasterbedingung_und_tb105.md` | 13 416 | ≈ 5 741 | 3 354 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-25d_tb106_abgegeben_vier_fragen.md` | 12 019 | ≈ 5 143 | 3 004 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-25e_tb107_abgegeben_drei_fragen.md` | 8 292 | ≈ 3 548 | 2 073 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-20_benchmarkfenster.md` | 7 144 | ≈ 3 057 | 1 786 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-20a_grenzfall.md` | 4 205 | ≈ 1 799 | 1 051 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-20b_kalender.md` | 4 634 | ≈ 1 983 | 1 158 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-20c_kapitalpfad.md` | 6 444 | ≈ 2 757 | 1 611 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-20d_mtm_messung.md` | 6 103 | ≈ 2 611 | 1 525 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-20e_konjunktion.md` | 6 329 | ≈ 2 708 | 1 582 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md` | 7 955 | ≈ 3 404 | 1 988 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21b_asof_und_wache.md` | 6 044 | ≈ 2 586 | 1 511 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21c_uebergabe_und_vorlauf.md` | 9 611 | ≈ 4 113 | 2 402 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21d_sichtschutz.md` | 7 397 | ≈ 3 165 | 1 849 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21e_fassung_gemessen.md` | 1 173 | ≈ 502 | 293 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21f_fassungsvergleich.md` | 2 305 | ≈ 986 | 576 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21g_sichtschutz_nullpunkt.md` | 7 885 | ≈ 3 374 | 1 971 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21h_festlegung_11.md` | 3 790 | ≈ 1 622 | 947 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21i_gesperrter_faltenplan.md` | 7 202 | ≈ 3 082 | 1 800 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21j_manifest_asof.md` | 6 107 | ≈ 2 613 | 1 526 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21k_abbild_schema.md` | 7 713 | ≈ 3 301 | 1 928 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21l_standpruefung.md` | 6 582 | ≈ 2 816 | 1 645 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-21m_faltenplan_pruefung.md` | 9 316 | ≈ 3 987 | 2 329 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md` | 8 253 | ≈ 3 532 | 2 063 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md` | 7 998 | ≈ 3 422 | 1 999 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22c_drei_ausgaenge_und_abbild.md` | 8 502 | ≈ 3 638 | 2 125 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22d_wert_ohne_ort.md` | 11 992 | ≈ 5 132 | 2 998 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22e_liste_vor_dem_tag.md` | 12 190 | ≈ 5 217 | 3 047 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22g_sonde_vor_dem_tag.md` | 3 616 | ≈ 1 547 | 904 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-22h_schluessel_und_vollzug.md` | 12 245 | ≈ 5 240 | 3 061 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-23a_gruen_und_tabelle.md` | 10 093 | ≈ 4 319 | 2 523 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-23b_neurechnung_nach_a.md` | 7 376 | ≈ 3 156 | 1 844 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-23c_messgroessen_und_vollzug.md` | 10 374 | ≈ 4 439 | 2 593 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-23d_dritte_leserin_und_eingabestand.md` | 14 382 | ≈ 6 155 | 3 595 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-23e_nachweislauf_im_modus.md` | 7 158 | ≈ 3 063 | 1 789 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-23f_fertigkriterium_38_4.md` | 8 324 | ≈ 3 562 | 2 081 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-24a_neun_listen_und_testannahmen.md` | 14 874 | ≈ 6 365 | 3 718 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-24b_rueckfall_mutationen_erzeuger.md` | 18 190 | ≈ 7 784 | 4 547 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-24c_nachweis_hat_zwei_teile.md` | 14 391 | ≈ 6 159 | 3 597 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-24d_deckel_statt_purge_ein_weg.md` | 22 967 | ≈ 9 829 | 5 741 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25a_umgebung_liste_laufbereich.md` | 23 224 | ≈ 9 939 | 5 806 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25b_zwischenablage_abbildung_lauftypen.md` | 19 685 | ≈ 8 424 | 4 921 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25c_rasterbedingung_abschnitt6_protokoll.md` | 15 624 | ≈ 6 686 | 3 906 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25d_kopie_pruefansicht_abbruch_zwei.md` | 7 790 | ≈ 3 333 | 1 947 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-25e_ablagen_nulltrades_shim.md` | 5 435 | ≈ 2 326 | 1 358 | 3 | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_UEBERGABE_2026-09-21_neuer_chat.md` | 12 170 | ≈ 5 208 | 3 042 | 3 | B6 Sonderfall: nicht die juengste Fassung |
| `auftraege/MAC_TB-102_messgroessen_im_modus.md` | 9 724 | ≈ 4 161 | 2 431 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-103_resolver_und_trockenlauf.md` | 19 714 | ≈ 8 437 | 4 928 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-104_leser_auf_resolver_und_altfelder.md` | 19 176 | ≈ 8 206 | 4 794 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-105_rueckfaelle_und_schreibziele.md` | 14 109 | ≈ 6 038 | 3 527 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-106_ersatzwerte_eingefroren_und_herkunft.md` | 18 786 | ≈ 8 040 | 4 696 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-107_nicht_gesperrte_rueckfaelle.md` | 16 112 | ≈ 6 895 | 4 028 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-108_register_41_42.md` | 15 522 | ≈ 6 643 | 3 880 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-109_nulltrades_ablagen_stummel.md` | 13 060 | ≈ 5 589 | 3 265 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-110_register_43.md` | 7 204 | ≈ 3 083 | 1 801 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-111_herkunft_auswertung_oeffnung.md` | 11 602 | ≈ 4 965 | 2 900 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-112_19_laufbereich_db_sicherung.md` | 12 876 | ≈ 5 510 | 3 219 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-113_zusammenfuehrung_tb111_register_44.md` | 8 748 | ≈ 3 743 | 2 187 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-114_register_45_herkunft_pfadregel_tb24_listen.md` | 11 418 | ≈ 4 886 | 2 854 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-115_drei_verfahrensmessungen.md` | 8 584 | ≈ 3 673 | 2 146 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `projektfuehrung/MAC_TB-82_register_34.md` | 16 040 | ≈ 6 864 | 4 010 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `projektfuehrung/MAC_TB-83_register_35.md` | 11 997 | ≈ 5 134 | 2 999 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `projektfuehrung/MAC_TB-85_sperrlisten_sonde.md` | 13 503 | ≈ 5 779 | 3 375 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `projektfuehrung/MAC_TB-86_faltenplan_schreibsperre.md` | 10 386 | ≈ 4 445 | 2 596 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-96_register_40.md` | 16 541 | ≈ 7 079 | 4 135 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-97_testannahmen_zweite_runde.md` | 12 965 | ≈ 5 548 | 3 241 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/MAC_TB-98_neun_listen_auf_dem_snapshot.md` | 12 633 | ≈ 5 406 | 3 158 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `auftraege/NACHTRAG_1_MAC_TB-91_blockA_vorgemessen.md` | 5 877 | ≈ 2 515 | 1 469 | 4 | B4 Auftrag angenommen bzw. abgegeben (ERGEBNIS liegt, zugehoerige Antwort nicht offen) |
| `belege/TB-91_beleg.md` | nicht messbar | – | – | 5 | B7 Beleg - vor dem Tag nie in der Ablage ⚠️ nicht im Repo |
| `belege/TB-93_beleg.md` | nicht messbar | – | – | 5 | B7 Beleg - vor dem Tag nie in der Ablage ⚠️ nicht im Repo |
| `projektfuehrung/UEBERGABE_2026-09-19.md` | 76 704 | ≈ 32 827 | 19 176 | 6 | B2 datierte Fassung - UEBERGABE.md liegt im Repo |
| `projektfuehrung/UEBERGABE_2026-09-24.md` | 24 550 | ≈ 10 506 | 6 137 | 6 | B2 datierte Fassung - UEBERGABE.md liegt im Repo |
| `projektfuehrung/AF-F0_BESTANDSAUFNAHME_2026-09-26.md` | 8 552 | ≈ 3 660 | 2 138 | 7 | B8 Ereignis eingetreten: Epic AF geparkt bis nach dem Tag; Bestandsaufnahme liegt vor (27b B8, C3 Nr. 7) |
| `projektfuehrung/JOURNAL_NACHTRAG_2026-09-18.md` | 17 817 | ≈ 7 625 | 4 454 | 7 | B8 Ereignis eingetreten: nach Regel 10 als eingearbeitet gemessen (27b B2) |
| `projektfuehrung/STOFFSAMMLUNG_REGISTER_41_42.md` | 13 374 | ≈ 5 723 | 3 343 | 7 | B8 Ereignis eingetreten: Registerauftrag TB-108 abgegeben (27b B8) |
| `projektfuehrung/ERGEBNIS_TB-116_leiter_lesarten.md` | 22 410 | ≈ 9 591 | 5 602 | – | B5 Ergebnis ohne offene Anfrage |
| `projektfuehrung/FABLE_ANFRAGE_2026-09-26a_tagesanfrage_tb109_bis_113.md` | 25 534 | ≈ 10 928 | 6 383 | – | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/FABLE_ANTWORT_2026-09-26a_dreizehn_fragen_nullbefund_registerblock.md` | 22 331 | ≈ 9 557 | 5 582 | – | B6 Dialogpaar geschlossen (Index: nicht offen, nicht unter den zwei juengsten) |
| `projektfuehrung/NACHTRAG_ARBEITSWEISE_6d_richtungsweisend.md` | 7 015 | ≈ 3 002 | 1 753 | – | B8 Ereignis eingetreten: in ARBEITSWEISE eingearbeitet (27b B1, Regel 10) |
| `projektfuehrung/UEBERGABE_2026-09-25.md` | 27 323 | ≈ 11 693 | 6 830 | – | B2 datierte Fassung - UEBERGABE.md liegt im Repo |

## In einfacher Sprache

Diese Liste sagt, welche Dateien aus der Projektablage herausdürfen, wie gross sie sind und warum sie gehen. Die Tokenzahlen sind geschätzt, weil die Ablage keine Zahl je Datei nennt. Geschätzt verschwindet rund 86 Prozent des heutigen Inhalts; mit den neuen Dateien wäre die Ablage danach zu gut einem Viertel gefüllt statt zu drei Vierteln. Vorher legt der steuernde Chat die neuen Dateien ab, holt die echte Liste der Ablage und lässt das Skript darüber laufen; gelöscht wird nur, was dort auch steht. Vier Registerkopien und zwei Belege gibt es nur in der Ablage, nicht im Repo — über sie wird vorher entschieden.
