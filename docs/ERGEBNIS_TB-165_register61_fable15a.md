# ERGEBNIS TB-165 — Register 61: Fable 15a (R98–R99), drei Marken, Voraussetzungen und Befunde

**Sitzung:** TB-165, Mac (Claude Code, Opus 5.5), 15.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-165_register61_fable15a.md` · **Zweig:** `main`
**Commits:** `4edd877` (S0, Schritt 0: Stand des steuernden Chats und Fable 15.10.a) · `173368f` (R, Register 61 und drei Marken) · `e941e61` (K, Registerkopie, Index, Dialog-Index) · F = der Abgabe-Commit „TB-165 Abgabe: Ergebnis, BACKLOG, Journal FB“, der dieses Ergebnis enthält · danach „TB-165 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-165/` · **Journal:** FB · **Kein Abbruch.**

## Kurz

Übergabe, Anfrage und Antwort 15.10.a sind nach md5-Prüfung (3/3) mit `4edd877` im Repo. Register 61 ist angehängt: 61.1 R98 und 61.2 R99 je mit Quellenzeile zeichengleich aus dem Codeblock der Antwort (Z. 46–49; vom Werkzeug nach dem Schreiben Zeichen für Zeichen verglichen), je eine Kettenzeile, dazu 61.3 Voraussetzungen und Befunde. Drei Marken nach R99 (d) stehen an 56.3, 57.1 und 57.2; sonst ist das Register append-only (numstat 78/0). Die Voraussetzungen ergaben 20 Prüfungen ohne NEIN. Befund nach R99 (g): Der Verfahrensprüfer hat 56 in einer Fassung ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ gelesen. Nach R99 (b) steht „25c (1)“ in zwölf Zeilen ausserhalb 57; die Lesart „25c (1) ist 42.3 F1 (a)“ trifft an allen zwölf, Stellen „Frage an Fable“ gibt es keine. Alle acht Schritte in K endeten mit rc 0. BACKLOG (Rang 1) und Journal FB sind eingetragen. Kein Lauf auf Kursdaten, kein Abbild, kein Code geändert.

## Schritt 0

`git status --porcelain` zeigte genau die sieben Soll-Einträge (`docs/belege/TB-165/0a_status.txt`); HEAD war `a9bf4a7c1865348b2c4f37be2fc67b92251ae920` auf `main`. Holbefehl: `tb165_werkzeug.py 200abc0c09620658c98061f9b12cc86bc7316fe83d6b8f1035a153279b5c1834`, wie Soll. S0 = `4edd877`, gepusht. Die drei Kopien (`0a_status.txt`, `0a_md5.txt`, `tb165_werkzeug.py`) waren laut `diff` gleich (keine Ausgabe).

`0a_md5.txt`, wörtlich:

```
ja    md5 docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md = 9bc9e2f1ccf3e14804549b23662a2caf
ja    md5 docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md = 26108d4fe8474e8035d500a78371ed21
ja    md5 docs/projektfuehrung/FABLE_UEBERGABE_2026-10-15a_eroeffnung.md = 4821ff1958955d333585c839b007dbe7
Pruefungen: 3, NEIN: 0
rc 0
```

## Voraussetzungen (`v_voraussetzung.txt`, wörtlich)

```
ja    R99 (g)/R56 (b): docs/projektfuehrung/FABLE_ANTWORT_2026-10-15a_schranke_je_bot_parameterweg_abnahme_am_erzeuger.md verfolgt, gleich HEAD, md5 9bc9e2f1ccf3e14804549b23662a2caf
ja    R99 (g)/R56 (b): docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15a_schranke_im_signalpfad.md verfolgt, gleich HEAD, md5 26108d4fe8474e8035d500a78371ed21
ja    R99 (g)/R56 (b): docs/projektfuehrung/FABLE_UEBERGABE_2026-10-15a_eroeffnung.md verfolgt, gleich HEAD, md5 4821ff1958955d333585c839b007dbe7
ja    Registerblock 15a: genau R98, Quelle, R99, Quelle im Codeblock (Z. 46–49)
ja    Register: 60 da, 61 nicht; R98/R99 0 Treffer
ja    Register endet mit genau einer Leerzeile
ja    Ort 57.1 R90: genau einmal, Einfuegestelle Z. 11980, R98 dort noch nicht genannt
ja    Ort 56.3 R86: genau einmal, Einfuegestelle Z. 11885, R98 dort noch nicht genannt
ja    Ort 57.2 R91: genau einmal, Einfuegestelle Z. 11987, R99 dort noch nicht genannt
ja    R99 (g): Abschnitt 37 am 35dae90 = HEAD = gelesene Kopie (d950e03), Endleerzeilen nicht gezaehlt
ja    R99 (g): Abschnitt 55 am 35dae90 = HEAD = gelesene Kopie (3f2e97e), Endleerzeilen nicht gezaehlt
ja    R99 (g) Befund: 56 am 35dae90 = HEAD; gelesene Kopie (3f2e97e) ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ (+3 Zeilen, TB-162), sonst zeichengleich
ja    R99 (g): Abschnitt 57 am 35dae90 = HEAD = gelesene Kopie (3f2e97e), Endleerzeilen nicht gezaehlt
ja    R99 (b): Zeilen mit „25c (1)“ ausserhalb 57 = die 12 Zeilen der Urteilsliste
ja    R99 (b): „25c (1)“ in 12 Zeilen ausserhalb 57 (darunter R60 (b) Z. 11352, R63 (c) Z. 11434), 3 in 57
ja    42.3 und F1 (a) genau da
ja    Index: Kopf 0–60, Zeilen 56, 57 (– ), 60, Pflegezeile TB-164, Pflege-Anker je genau einmal; kein Abschnitt 14
ja    Dialog-Index: 15a noch nicht
ja    BACKLOG: Rang 1 (Stand TB-164) genau einmal
ja    Journal: höchste Kennung FA, nächste FB frei
Pruefungen: 20, NEIN: 0
rc 0
```

## Register 61

Datum `15.10.2026`, S0 `4edd877`. Probe (`r_probe.txt`): 6 Prüfungen, NEIN 0, rc 0. Eintrag (`r_eintrag.txt`): 9 Prüfungen, NEIN 0, rc 0 — R98 und R99 mit Quellenzeile je genau einmal zeichengleich; ohne die drei Marken ist das alte Register vorn unverändert und dahinter steht genau Abschnitt 61.

- **Abschnitt 61:** Titel `## 61. Fable 15a — Registerblock R98–R99 (TB-165)` ab **Z. 12204**; 61.3 ab Z. 12222.
- **Marken** (Zeilen aus `r_daten.json`, Stand nach dem Eintrag):

| Ort | Marke | Zeile |
|---|---|---|
| 56.3 R86 | ERGÄNZT durch R98 (61.1), Unterpunkt (d) | Z. 11887 |
| 57.1 R90 | ERGÄNZT durch R98 (61.1) | Z. 11985 |
| 57.2 R91 | PRÄZISIERT durch R99 (61.2), Unterpunkt (b) | Z. 11995 |

- **numstat** (`git diff --numstat` vor dem Commit `173368f`): `78	0	docs/VORREGISTRIERUNG_neuselektion.md` — Spalte 2 = 0. Die 78 Zeilen sind 3 × 3 Markenzeilen und 69 Zeilen Abschnitt 61.

## 61.3 (a) und (b), aus dem Register übernommen

(a) R99 (g): 37, 55 und 57 am Commit `35dae90` = am Stand `4edd877` = gelesene Kopie (37 am Kopf `d950e03`, 55 und 57 am Kopf `3f2e97e`; Leerzeilen am Abschnittsende nicht gezählt). **Befund:** 56 am Kopf `3f2e97e`, den der Verfahrensprüfer gelesen hat (Leseprotokoll 15a), ist ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ (drei Zeilen, gesetzt mit TB-162); sonst zeichengleich. R95 selbst hat er in 58 am Commit `35dae90` gelesen. Übergabe, Anfrage und Antwort 15.10.a liegen seit `4edd877` im Repo (R56 (b)).

(b) R99 (b): „25c (1)“ steht am Stand `4edd877` in 12 Zeilen ausserhalb 57, darunter R60 (b) (Z. 11352) und R63 (c) (Z. 11434), wie 57.5 („auch im Blocktext“); dazu 3 Zeilen in 57 (Z. 11986, 12025, 12035). Gemessen sind zwölf Zeilen einschliesslich R60 (b) und R63 (c), nicht zwölf und zwei dazu. Die Lesart „25c (1) ist 42.3 F1 (a)“ je Stelle ausserhalb 57 (Ausschnitt höchstens 200 Zeichen; Urteil aus der Liste je Zeile im Werkzeug, gemessen vom steuernden Chat am 15.10.2026; 42.3 F1 (a), Register Z. 9310–9312: „unbekannter Bedingungstext ⇒ 2“):

| Z. | Ort | Zeile | Ausschnitt | Urteil |
|---|---|---|---|---|
| 9632 | 43, 43.1 | Quelle des Grundes | … Eingabe, er rechnet auf ihr — kann er das nicht, hat er nicht gemessen), 12 (kein Auffüllen), 25c (1) (Register-Code-Widerspruch ist 2). Kein Ergebnis. Eure Beobachtung, dass die Meldungen „ni… | trifft |
| 10532 | 46, 46.5 | Quelle des Grundes | …2 (nennt `herkunft.json` als Teil des Vertrags), Abschnitt 12 (Vertragsbruch ⇒ Abbruch), 36.5, 25c (1) (Register-Code-Widerspruch ist 2), Prüfprinzip A8. Kein Ergebnis. | trifft |
| 10760 | 47, 47.8 | Quelle des Grundes | > *Quelle des Grundes:* 12, 5e/19, 42.2 E5, R10 (dieselbe Bauart), 25c (1). Kein Ergebnis. | trifft (42.3 F1 (a): unbekannter Bedingungstext ⇒ 2; R25: endet mit 2) |
| 11031 | 48, 48.16 | andere Zeile | …wertung.py in diesem Fall ausgegebene Zelle; Abweichung ist ein Register-Code-Widerspruch nach 25c (1).] M48. | trifft |
| 11073 | 48, 48.18 | R-Zeile | …0“; 4.2; 9), die gemessene Übereinstimmung; eine Abweichung ist ein Register-Code-Widerspruch (25c (1)) und wird gemeldet, nicht eingetragen. Der Registertext legt keine dieser Definitionen neu… | trifft |
| 11074 | 48, 48.18 | Quelle des Grundes | > Quelle des Grundes: 13 („Das Urteil ist Code“), 12, Sperrliste 3/5/7/9, 38.2, 25c (1), 2.1, Messung TB-121. Kein Ergebnis. | trifft |
| 11352 | 51, 51.5 | R-Zeile | …gen die Selektionsfalten des Gewinners; eine Abweichung ist ein Register-Code-Widerspruch nach 25c (1) und wird gemeldet.] (c) Der Zellen-Erzeuger schreibt beide Träger aus einer Rechnung: mitt… | trifft |
| 11434 | 52, 52.1 | R-Zeile | …d kein Mittel daraus rechnet.] Trifft sie nicht zu, ist das ein Register-Code-Widerspruch nach 25c (1) zur Bewertung in R48 (d) und R60 (b) und wird gemeldet, nicht eingetragen. (d) Der Zellen-… | trifft |
| 11435 | 52, 52.1 | Quelle des Grundes | …ch R49 (e)), R45 (kein zweiter Rechenweg), 24.4 (bewertet zum Marktpreis, nicht zum Einstand), 25c (1). Kein Ergebnis. | trifft |
| 11555 | 53, 53.4 | R-Zeile | …k_tagesreihen/<markt>.csv liest und R39 <bot>.csv verlangt, ist ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50). Er wird zugunsten von R39 aufgelöst; R39 ist damit b… | trifft |
| 11891 | 56, 56.4 | R-Zeile | …achennotiz, und die Wache bleibt. Kann er es bei einem, ist das ein Register-Code-Widerspruch (25c (1), nach der Wiedergabe in R48 und R50) und kommt vor dem Bau mit der Fundstelle als Frage an… | trifft |
| 11966 | 56, 56.8 | andere Zeile | \| 14 \| R87 (d) verweist auf „25c (1), nach der Wiedergabe in R48 und R50“; 42.3 („Aus Fable 25c“) führt keinen Eintrag „(1)“, d… | trifft |

Stellen mit „Frage an Fable“: keine.

*Die Zeilenangaben in (a) und (b) gelten am Stand `4edd877` (vor dem Eintrag); im Register nach `173368f` liegen die Zeilen hinter Z. 11885 um drei, hinter Z. 11980 um sechs und hinter Z. 11987 um neun höher (nachgemessen: 11986 → 11992, 12025 → 12034, 12035 → 12044; Zeilen bis Z. 11885, darunter alle der Tabelle ausser 11891 und 11966, unverändert).*

## Schritt K

| Beleg | Werkzeug | rc |
|---|---|---|
| `k_registerkopie.txt` | `registerkopie.py` | 0 — sechs Teile, 61 in T6 (Abschnitte 58–61, 43 858 B), Bodies bytegleich zum Register am `173368f` |
| `k_abschnitte.txt` | `registerkopie.py --abschnitte` | 0 — 62 Dateien (0–61), bytegleich |
| `k_pruefen.txt` | `registerkopie.py --pruefen` | 0 |
| `k_index_zeilen.txt` | `c2_index_zeilen.py 4edd877 173368f` | 0 — 452 Zahlen umgeschrieben, davon 14 geändert |
| `k_index.txt` | `WZ index 4edd877 15.10.2026` | 0 — 8 Prüfungen, NEIN 0 |
| `k_handfelder.txt` | `WZ handfelder` | 0 |
| `k_dialog_index.txt` | `dialog_index.py --handfelder` | 0 — 62 Zeilen, offen 10, ohne Registertext 12, registriert 40 |
| `k_dialog_pruefen.txt` | `dialog_index.py --pruefen` | 0 |

Keine neue Teildatei.

## BACKLOG

Rang 1 (`a_backlog_probe.txt`, `a_backlog.txt`, je rc 0) trägt jetzt hinter dem Stand TB-164: „Register 61 (Fable 15a: R98 Schranke je Bot, Parameterweg, eine Freigabe je Bauauftrag, Abnahme am Erzeuger; R99) mit TB-165 (15.10.2026, Journal FB); als Nächstes TB-30b E-3, mit der Messung nach R98 (b)“. Journal: Kennung FB (`a_kennung.txt`), Probe und Eintrag je rc 0.

## Offen

- **R98 (b)** mit dem Bau E-3: ob `entry_cutoff` in den sechs Backtests die drei Bedingungen erfüllt und welche Stelle es bei elliott_wave, elliott_wave_stocks und t3_supertrend ist (61.3 (c)).
- **F4** (Punkte 10–12 der Anfrage 10.10.a) mit Wortlaut in die nächste Fable-Anfrage (61.3 (d)). Stellen „Frage an Fable“ aus 61.3 (b): keine.
- **Befund zu 56** (R99 (g)): zur Kenntnis an den Verfahrensprüfer — die von ihm gelesene Kopie von 56 (`3f2e97e`) war ohne die Marke „56.1 R84 PRÄZISIERT durch R95 (58.2)“ aus TB-162.

## Abweichungen

Keine. Alle Soll-Werte trafen zu; kein Schritt verlangte eine Bestätigung.

## In einfacher Sprache

Die neue Antwort des Verfahrensprüfers liegt jetzt mit seiner Anfrage und der Übergabe im Repo, und ihre zwei Regeltexte stehen wortgleich am Ende des Registers. Die erste Regel sagt, dass die Sperre gegen zu frühe Käufe bei jedem Bot dort sitzt, wo er seine Käufe bildet, und dass sie an dem Baustein geprüft wird, der die Ergebnisse erzeugt. An drei älteren Stellen steht nun ein Hinweis, dass sie ergänzt oder genauer gefasst wurden. Bei der Vorprüfung fiel auf, dass der Prüfer einen Abschnitt in einer Fassung ohne einen später gesetzten Hinweis gelesen hat; das ist festgehalten. Es lief nichts auf Kursdaten, und kein Code wurde geändert.
