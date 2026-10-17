# ERGEBNIS TB-180 — Startkapital am Ort (R110 (b) Schritte 1–4, Probe R110 (c))

**Auftrag:** `docs/auftraege/MAC_TB-180_startkapital_am_ort_punkt9_abbild_probe.md` · **Sitzung:** Mac, Opus 5.5, 17.10.2026 (23:44–23:5x) · **Interpreter:** `trading-env/bin/python3 -B` (3.9.6)

| | Commit |
|---|---|
| HEAD vorher | `dc2e6b3` |
| ⟨S0⟩ Auftrag | `ebee3ef` |
| ⟨C⟩ Handelscode, Probe | `f60f92b` |
| ⟨R⟩ Nachtrag, Abbild, Abschnitt 71 | `fd8f277` |
| ⟨K⟩ Registerkopie, Index, Dialog-Index | `321757e` |
| HEAD nachher | Abgabe-Commit `TB-180 Abgabe: …`, danach `TB-180 F: porcelain und numstat` |

**Gesamturteil: alle Schritte nach Soll, keine Abweichung, kein Abbruch.**

## Je Schritt

| Schritt | Soll | Ist | Beleg |
|---|---|---|---|
| 0a | `0a gut`, Werkzeug-sha256 `8a6887d2…` | `0a gut (2 Eintraege)`, sha256 `8a6887d2beccea2b170e9b967fdb9a70be4200af1cfda2f643cdb8b260ed7dc0`, `Dateien 1`; Status nach S0 leer | `0a_status.txt` |
| V | `rc 0`; Sonde ohne `RUECKGABEWERT 1`; vergleich rc 1 | 35 Prüfungen, NEIN 0, `rc 0`; Sonde `RUECKGABEWERT 2`, `Pfad-Bestandteile: 37 geprueft, davon 37 mit 0 / 0 mit 1 / 0 mit 2`; vergleich `rc 1` (`_cutoff_je_symbol`); Journal: höchste FP, nächste FQ | `v_voraussetzung.txt`, `v_sonde.txt`, `v_vergleich.txt` |
| M | neun `ja`, `rc 0` | 9/9, `rc 0` | `m_vorher.txt` |
| C | je `rc 0` | Probe 24/0, Code 36/0, Prüfen 35/0, je `rc 0` | `c_probe.txt`, `c_code.txt`, `c_pruefen.txt` |
| N | 9 von 9 bytegleich | siehe unten | `n_nachher.txt`, `n_vergleich.txt` |
| T | `… 0 fehlgeschlagen.`, Prüffall 11 fünfmal `[OK ]` | 49 von 49, `rc 0`, Laufzeit ~216 s (23:44:35–23:48:11) | `t_test.txt` |
| R1 | Probe und Schreiben `rc 0` | 5/0 und 6/0; geschrieben Z. 1080–1082 | `r_nachtrag_probe.txt`, `r_nachtrag.txt` |
| B | Abbild `rc 0`; Sonde neu ohne 1, +1 Bestandteil; Sonde alt `RUECKGABEWERT 1` | siehe unten | `b_abbild.txt`, `b_sonde_neu.txt`, `b_sonde_alt.txt` |
| R2 | Probe und Schreiben `rc 0` | 17/0 und 18/0; Marke vor Z. 5468, Abschnitt 71 | `r_register_probe.txt`, `r_register.txt` |
| K | jede Datei `rc 0`; Kopf 0–71, Zeile 71, Pflegezeile TB-180; 17d/17e `offen: nein` | alle acht `rc 0`; Registerkopie BYTEGLEICH (1 281 183 B, 6 Teile, 72 Abschnittsdateien, keine neue Teildatei); Index Z. 3 „Abschnitte 0–71“, Z. 230 `| 71 aus TB-180 | 6 |`, Pflegezeile TB-180; Dialog-Index 71/71 | `k_*.txt`, `k_handfelder.json` |

## Wörtlich

`n_vergleich.txt`, letzte zwei Zeilen vor `rc`:

```
Ergebnis: 9 von 9 bytegleich (vorher gegen nachher)
Pruefungen: 9, NEIN: 0
```

Prüffall 11 aus `t_test.txt`:

```
11) Der Ort des Startkapitals traegt alle neun (R110 (c))
  [OK ] neun Kurven vor der Mutation erzeugt   9 von 9
  [OK ] Mutation am Ort, genau einmal   1
  [OK ] alle neun Kurven weichen ab   9 von 9
  [OK ] zurueckgesetzt: alle neun bytegleich   9 von 9
  [OK ] der Ort im Repo blieb unberuehrt

49 von 49 Pruefungen bestanden, 0 fehlgeschlagen.
```

`b_sonde_neu.txt`:

```
Pfad-Bestandteile: 38 geprueft, davon 38 mit 0 / 0 mit 1 / 0 mit 2  (punkte 16, bestimmt 0, eingefroren 22)
RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]
```

`b_sonde_alt.txt` (Gegenprobe):

```
Pfad-Bestandteile: 37 geprueft, davon 37 mit 0 / 0 mit 1 / 0 mit 2  (punkte 15, bestimmt 0, eingefroren 22)
RUECKGABEWERT 1 BEFUND - BEFUND in Punkt(en) [] und in (ii) Abbild/Registertext
```

**Abbild:** `research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-10-17_tb180.json`, 11 780 Bytes, sha256 `f83f0323ed2e900406f908b8ba39155fd6c6472696a1b454d2bbf238a8a2d6d9` (14 Punkte aus Register Z. 999–1115, 16 Pfadnennungen, HEAD `f60f92b`).

**Ort:** `shared/handelskosten.py` am `f60f92b`, sha256 `b2efabe4a51b26d6b9f34b1b8b9d0f5bc45b463aabd6b9bbd95237f560273a5e`, `STARTING_CAPITAL = 10_000.0` Z. 39.

## Abweichungen und Hinweise

- **Keine Abweichung vom Soll.**
- `vergleich.py --pruefen` meldet weiter `rc 1` wegen `_cutoff_je_symbol` (Ausgangslage am Bau-HEAD, im Auftrag benannt; nach dem Umbau zeichengleich).
- Im Arbeitsbaum liegen alte `__pycache__`-Ordner (`cpython-310`, Dateien vom September/Oktober, per `.gitignore` ignoriert). Sie stammen nicht aus diesem Lauf (alle Aufrufe mit `-B`); nicht entfernt, weil `rm` verboten ist.
- Der Lauf lag kurz vor Mitternacht; ⟨DATUM⟩ `17.10.2026` und ⟨ISO⟩ `2026-10-17` wurden einmal um 23:49 bestimmt und in allen Schritten gleich verwendet.
