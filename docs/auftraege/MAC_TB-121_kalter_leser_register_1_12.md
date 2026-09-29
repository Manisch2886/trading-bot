# TB-121 Kalter Leser — Register Abschnitte 0–12 ohne Vorwissen lesen und aufschreiben, was sich daraus allein nicht verstehen oder nicht umsetzen lässt (Fable 25f V8/F3)

**Sitzungstitel:** `TB-121` · **Aufwand:** hoch (ARBEITSWEISE 22.1) · **Repo:** `Manisch2886/trading-bot`, Base `main` · **Angelegt:** 27.09.2026, 20:25, vom steuernden Chat
**Vorgänger:** TB-120 (abgegeben `07fcca7`, geschlossen 27.09., 20:10).
**Kein Fable bis Dienstag, 29.09.** Das Ergebnis dieses Auftrags ist Stoff für Fable. Der steuernde Chat überträgt es in die Sammlung; die Sitzung schreibt dort nicht hinein.

## ⭐⭐ Freigabe des Betreibers, wörtlich

- **27.09.2026, 18:08, Chat:** *„bis Dienstag arbeiten wir strukturier ohne fable weiter und sammeln alles für fable soweit möglich“*
- **27.09.2026, ca. 18:25, Auswahlkarte „Was soll bis Dienstag ohne Fable laufen?“**, darin die Option *„Kalter Leser (25f V8/F3) — Eine frische Sitzung liest Registertext 1–12 ohne Vorwissen und schreibt auf, was sie nicht versteht. Das wird Stoff für Fable.“* ⇒ Antwort: **„Wir arbeiten alles strukturiert ab“.**

⛔ **Nicht freigegeben:** Code ändern, irgendetwas laufen lassen, Register oder Regelwerk ändern, `crontab`, Datenbanken.

## ⭐⭐ Die eine Regel dieses Auftrags: kalt lesen

Der Wert dieser Sitzung besteht darin, dass sie **nichts weiss ausser dem, was in den Abschnitten 0–12 des Registers steht**. Fable 25f, F3 (zitiert): *„billigster Test, ob der Text ohne den Verlauf verständlich ist“.*

**Deshalb liest die Sitzung ausser diesem Auftrag nur:**
- `docs/VORREGISTRIERUNG_neuselektion.md`, **Zeilen 1 bis 1225** (vom Anfang bis vor `## 13. Die Verankerung`, gemessen am Stand `07fcca7`). Die Zeilennummer wird in Schritt 0 nachgemessen;
- für Schritt C zusätzlich **nur** die Bezeichner, die die Abschnitte 0–12 selbst nennen (Datei plus Funktion oder Konstante). Diese werden im Code nachgeschlagen, sonst nichts.

**Nicht gelesen werden:**
- Abschnitte ab 13;
- `REGISTER_INDEX.md`, Registerkopien;
- Übergaben, Backlog, `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`;
- `ERGEBNIS_*`, `FABLE_*`, Belege, Journal.

Verweist der Text in 0–12 auf einen späteren Abschnitt, zum Beispiel über eine Marke „⚠️ ERSETZT durch Abschnitt 15“ oder „siehe 45.6“, dann wird der Verweis **nicht verfolgt**. Er wird als Befund aufgenommen: „Verständnis hängt an Abschnitt X“.

`CLAUDE.md` des Repos lädt Claude Code von selbst. Die Sitzung nennt im Ergebnis, dass sie geladen wurde, und stützt kein Verständnis darauf.

**Sichtschutz 27.1:** Das Register hat dieses Tor passiert (27.3). Das Ergebnis enthält keine Ergebnisgrössen des Selektionsraums; es gibt keine.

In einfacher Sprache: Das Regelwerk des grossen Laufs ist über zwei Wochen gewachsen, und alle, die es lesen, kennen seine Geschichte. Diese Sitzung soll es lesen wie jemand, der es zum ersten Mal sieht. Sie schreibt auf, welche Begriffe nicht erklärt sind, wo der Text auf spätere Stellen angewiesen ist, wo er sich widerspricht und was man allein daraus nicht bauen könnte.

## Schritt 0 — Ausgang

0a. `git status --short`. Erwartet sind genau diese fünf Dateien:

| Datei | Zustand | md5 |
|---|---|---|
| `docs/auftraege/MAC_TB-121_kalter_leser_register_1_12.md` | neu | (dieser Auftrag) |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | geändert | Zeiger |
| `docs/projektfuehrung/FABLE_SAMMLUNG_fuer_2026-09-29.md` | geändert | `b363c9485017b00ff42fee5f45585b49`, numstat gegen HEAD **84/0** |
| `docs/auftraege/MAC_TB-122_posten3_achsen_durchreichen.md` | neu | `ad4eca4c255e5cc803be0f785e200c7a` |
| `docs/projektfuehrung/UEBERGABE.md` | geändert | kein md5 (kann sich bis zum Start noch ändern); numstat gegen HEAD mit **0 entfernten Zeilen** |

*Nachgezogen 29.09.2026, 07:20, vom steuernden Chat beim Umzug. Die Sammlung kann sich bis zum Start ebenfalls noch ändern (Fable-Anfrage 29a). Gilt ihr md5 nicht mehr, genügt auch dort numstat mit 0 entfernten Zeilen. Diese Dateien werden **nicht gelesen**, nur geprüft.*

Die Sammlung wird **nicht gelesen**, nur ihr md5 geprüft. Weicht etwas ab ⇒ Abbruch. Danach der Commit `TB-121 Schritt 0`, dann pushen.

0b. In `docs/belege/TB-121/0b_ausgang.txt` festhalten:
- HEAD;
- sha256 des Registers;
- die Zeilennummer von `^## 13\.` (Soll 1226). Weicht sie ab, gilt die gemessene.

## Schritt A — Lesen und Befunde sammeln

`docs/belege/TB-121/a_befunde.md`, eine Tabelle mit diesen Spalten:
- Nr.;
- Zeile(n);
- Abschnitt;
- Art;
- Befund in einem Satz;
- Zitat, höchstens 15 Wörter, zeichengleich.

Arten:
- **B** Begriff wird benutzt, aber in 0–12 nicht erklärt (z. B. ein Kürzel, ein Dateiname ohne Zweck, eine Rolle);
- **V** Verständnis hängt an einem Abschnitt ausserhalb 0–12 (Marke oder Verweis), mit Ziel;
- **W** zwei Stellen in 0–12 sagen Verschiedenes;
- **M** mehrdeutig: zwei Lesarten möglich, beide nennen;
- **A** nicht ausführbar: eine Vorschrift, die sich aus dem Text allein nicht in Code oder Handlung übersetzen lässt;
- **Z** eine Zahl oder Angabe ohne Herkunft im Text.

Gelesen wird Satz für Satz, auch Tabellen und Marken. Es wird nicht bewertet, ob die Regel gut ist, nur, ob sie verständlich und vollständig ist.

## Schritt B — Der Vollständigkeitstest aus Abschnitt 12, kalt angewandt

Abschnitt 12 fragt: *„Lässt sich das Auswertungsskript fertig schreiben, ohne ein einziges Ergebnis gesehen zu haben?“* Die Sitzung beantwortet eine engere Frage: **Liesse sich `auswertung.py` allein aus den Abschnitten 0–12 schreiben?**

`b_vollstaendigkeit.md`:
- je Baustein eine Zeile: Selektionsstatistik, Drawdown-Bedingung, Plateau, Abbruchkriterien (a)–(d), Kapitalregel, Bericht, DSR, Faltenplan, Benchmark;
- Spalten: „aus 0–12 schreibbar ja/nein“ und „was fehlt“, mit Verweis auf die Befunde aus A.

Den Code von `auswertung.py` dafür **nicht** lesen. Die Frage ist, was der Text hergibt, nicht was der Code tut.

## Schritt C — Stichprobe Text gegen Code (nur die genannten Bezeichner)

Für höchstens zwölf Bezeichner, die 0–12 ausdrücklich mit Datei und Funktion oder Konstante nennen, gilt:
- nachschlagen, ob es sie gibt;
- prüfen, ob der Name zum beschriebenen Verhalten passt, nur durch Lesen der Funktion.

Beispiele sind `benchmark.py::erlaubt`, `registerdaten.SPITZEN_SCHWELLE` und `auswertung.py::kapitalregel`. Auswahl: die ersten zwölf in Textreihenfolge.

`c_stichprobe.md` enthält je Bezeichner vier Spalten:
- genannt in Zeile;
- gefunden ja/nein, mit Datei:Zeile am HEAD;
- passt ja/nein;
- Satz.

Für „passt“ genügt Lesen. Nichts ausführen.

## Schritt D — Ergebnis

`docs/ERGEBNIS_TB-121_kalter_leser_register_1_12.md` enthält:
- ein Kurzbefund: Zahl der Befunde je Art;
- die zehn wichtigsten Befunde, ausgewählt nach „ein neuer Leser würde hier falsch bauen“;
- Tabelle B;
- Stichprobe C;
- **„Für Fable“**: jeder Befund der Arten W, M und A als Frage mit Zeile und Zitat, ohne Neigung;
- „Was die Sitzung ausser 0–12 gesehen hat“: `CLAUDE.md`, dieser Auftrag, sonst nichts. Hat sie doch etwas anderes geöffnet, steht es hier;
- „In einfacher Sprache“.

Dazu ein Journal-Eintrag, der Abgabe-Commit und das Pushen.

## Abbruchkriterien (nur für diesen Gegenstand)

- Schritt 0a weicht ab ⇒ Abbruch.
- Eine andere Datei als die erlaubten müsste gelesen werden, um weiterzukommen ⇒ nicht lesen. Als Befund der Art V oder B aufnehmen und weitermachen. Das ist kein Abbruch.
