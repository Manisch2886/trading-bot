# TB-116 — Prüfung vor dem Tag zu 16.4: Ergibt das Regelwerk für jede der 3⁹ = 19 683 Stufentabellen genau einen Multiplikatorvektor? Nur ein Prüfwerkzeug, keine Lesart festlegen

**Sitzungstitel:** `TB-116` · **Angelegt:** 26.09.2026, 20:55, vom steuernden Chat
**Vorgänger:** TB-115 (`10e9697`) · **Aufwand:** hoch (ARBEITSWEISE 22.1)
**Grundlage:** Register **16.4** (Registertext 6, (a)–(m)), dort der Absatz „Prüfung vor dem Tag“, zeichengleich: *„Das Leiter-Skript muss aus **jeder** möglichen Stufentabelle — **3⁹ = 19 683**, trivial aufzählbar — einen **eindeutigen** Multiplikatorvektor erzeugen, **ohne Eingabe des Betreibers**. … Auch das ist eine Prüfung mit Befund, kein Abbruchkriterium.“* Dazu 16.11 Zeile 3 und Fable 26a 2 (a): Das Zellenbudget steht im Register, offen ist nur der Vollzug (Stufe IV).

## ⭐⭐ Freigabe des Betreibers, wörtlich

**26.09.2026, ca. 20:50, Auswahlkarte im steuernden Chat:** *„Soll ich heute noch TB-116 starten? Das ist ein Prüfauftrag für die Kapitalverteilung, die schon im Regelwerk steht (16.4). Die Sitzung prüft alle 19 683 möglichen Stufen-Kombinationen der neun Bots. Für jede stellt sie fest, ob das Regelwerk genau eine Verteilung ergibt. … Die Sitzung baut nur ein Prüfwerkzeug. Sie ändert keinen Bot und kein eingefrorenes Programm, und sie legt keine Lesart fest; das entscheidet Fable.“* ⇒ **„Ja, TB-116 starten (Empfohlen)“**

| freigegeben | Pfad / Handlung |
|---|---|
| ✔ | **neu:** `research/leiter_pruefung/leiter_lesarten.py` und `research/leiter_pruefung/test_leiter_lesarten.py` (neuer Ordner; nicht im Laufbereich, auf keiner Liste) |
| ✔ | `docs/belege/TB-116/`, `docs/ERGEBNIS_TB-116_leiter_lesarten.md`, `docs/projektfuehrung/JOURNAL.md` (Block **DO**) |
| ✔ | Schritt 0: die Dateien des steuernden Chats committen (Liste unten) |

⛔ **Nicht freigegeben:**
- jede Änderung an Bots (`strategies/*`), `shared/*`, `research/vorregistrierung/*`, Register, Abbild;
- das **eigentliche** Leiter-Skript. Dieses Werkzeug ist ein Prüfwerkzeug, kein Vorgriff: Es legt **keine** Lesart fest und wird nicht vom Lauf geladen;
- jede Ergebnisgrösse des Selektionsraums (27.1). Die Stufentabellen sind **hypothetisch**, aufgezählt, nicht aus einem Lauf;
- Datenbanken, `crontab`.

---

## 0. Schritt 0

**0a — committen.** Erwartet uncommittet, sonst nichts:

| Datei | Stand |
|---|---|
| `docs/auftraege/MAC_TB-116_leiter_lesarten_pruefung.md` | dieser Auftrag |
| `docs/auftraege/AKTUELLER_AUFTRAG.md` | Zeiger TB-116 |
| `docs/projektfuehrung/FABLE_ANFRAGE_2026-09-27a_tagesanfrage_tb114_tb115.md` | neu, md5 `93a677c11d13a608fe4416ab4ca23242` |
| `docs/projektfuehrung/UEBERGABE_2026-09-25.md` | Nachtrag 5 angehängt, md5 `a1fb9cb23391e4d7e24c54b309ccf819` |
| `docs/projektfuehrung/AUFGABEN_BETREIBER_2026-09-26.md` | Nachtrag 20:50 angehängt, md5 `405c77c4126094921d1d95d83c447d5e` |

Für beide angehängten Dateien: `git diff --numstat`, zweite Spalte 0. Weitere Dateien melden, nicht mitcommitten. Commit „TB-116 Schritt 0: Auftrag, Zeiger, Fable-Anfrage 27a, Übergabe Nachtrag 5, Aufgabenliste“, Push.

**0b — Ausgangswerte** (am Ende wiederholen, müssen gleich sein):
- `register()` `5acb4c19…`;
- Sonde gegen `5e5ad109…` 34/0/0;
- Arbeitsbaum ausserhalb `docs/` und `research/leiter_pruefung/` leer.

## Block A — Der Registertext, den das Werkzeug benutzt

- 16.4 ganz lesen.
- Dann im ganzen Register nach späteren Stellen suchen, die 16.4 ändern, ergänzen oder auslegen. Suchmuster: `16.4`, `Registertext 6`, `Zellenbudget`, `Stufenfaktor`, `m_b`, `Klassenschlüssel`, `80/20`, `Leiter`. Muster und Treffer kommen in `a_fundstellen.txt`.
- ⭐ **Jede Regel, die das Werkzeug anwendet, steht in `a_regeln.md` als zeichengleiches Zitat mit Fundstelle.** Geprüft wird per `diff` rc 0, Bauart TB-110.
- Was das Werkzeug tut und nicht im Zitat steht, ist eine **Lesart** und bekommt einen Namen (L1, L2, …).

## Block B — Das Prüfwerkzeug

`leiter_lesarten.py`:

- **Eingabe:** eine Stufentabelle, je Bot eines von `schatten`, `grund`, `bestaetigt`; die Zellenzuordnung aus 16.4 (g) als Literal mit Fundstelle.
- **Aufzählung:** alle 3⁹ = 19 683 Tabellen.
- **Je Tabelle und je Lesart:**
  - der Vektor `m_b` (9 Werte);
  - je Anlageklasse der Anteil in der statischen Benchmark-Position (16.4 (b), (j));
  - die Summe *Σ m_b × (1/9) + Benchmark-Anteile* (Exposure-Summe des Buchs);
  - ob die Lesart den Fall **überhaupt** beantwortet (sonst „keine Antwort“ mit dem Satz, der fehlt).
- **Mindestens diese Stellen als Lesarten führen**, nicht entscheiden. Der steuernde Chat hat sie beim Lesen gesehen, **nicht gemessen**; die Sitzung prüft, ob sie wirklich zwei Lesarten sind, und ergänzt weitere:
  1. **Zellenanteil und Klassenschlüssel:**
     - Teilen aktive Zellen „das Buch“ über **alle** Zellen (h), und skaliert (l) danach je Klasse?
     - Oder teilen sie **innerhalb** ihrer Anlageklasse, und (l) teilt das Buch vorher 80/20?
     
     Die Formel in (m) nennt beides nebeneinander.
  2. **Klasse ohne aktive Zelle:** Geht ihr Klassenanteil in die Benchmark ihrer Anlage (j, zellenweise gelesen), oder zur anderen Klasse?
  3. **Schatten-Bot in einer aktiven Zelle:** (b) sagt, sein Budgetanteil halte die Benchmark-Position; (i)/(j) geben ihm Faktor 0, und die übrigen teilen das Zellenbudget. Gilt (b) nur direkt nach dem Selektionslauf, oder immer?
- **Keine Lesart ist die „richtige“.** Das Werkzeug meldet nur.

`test_leiter_lesarten.py`:
- Proben mit Hand-Beispielen je Lesart, darunter alle Grundbudget, alle Schatten, nur Krypto aktiv, eine Zelle mit Schatten + Bestätigt.
- Je Probe eine Mutationsgegenprobe.
- Eine Probe, dass die Aufzählung genau 19 683 verschiedene Tabellen liefert.

## Block C — Die Prüfung

Das Werkzeug läuft über alle 19 683 Tabellen und legt `c_pruefung.txt` und `c_pruefung.json` ab. Darin:

| Kennzahl | je Lesart-Kombination |
|---|---|
| Tabellen mit eindeutigem Vektor | Zahl |
| Tabellen, in denen die Lesarten **verschiedene** Vektoren ergeben | Zahl, dazu 3 Beispiele je Unterschiedsklasse |
| Tabellen ohne Antwort | Zahl, Klassen, je 1 Beispiel mit dem fehlenden Satz |
| Exposure-Summe ≠ 1 | Zahl und Spanne; nur benennen, ob Absicht oder Lücke, entscheidet Fable |
| max. `m_b` | Wert und Tabelle (ein Bot mit dem Mehrfachen seiner heutigen Grösse ist eine Tatsache für Fable) |

⭐ **Ergebnisform für Fable:** eine Tabelle „Lesart-Stelle × Folge“ und je Stelle ein Satz, welcher Registertext sie schliessen würde. Der Wortlaut ist **Vorschlag**, als solcher markiert.

## Block D — Journal, Ergebnis

- Journalblock `## DO — TB-116: …`.
- `docs/ERGEBNIS_TB-116_leiter_lesarten.md` mit „Für Fable“ und „In einfacher Sprache“.
- 0b am Ende gleich.

## Commits

1. Schritt 0;
2. Werkzeug und Test;
3. Belege, Ergebnis, Journal.

Nach jedem Commit Push.

## ⚠️ Abbruchkriterien — melden, nicht reparieren

- Eine Messung verlangte eine Ergebnisgrösse des Selektionsraums.
- Ein 0b-Wert ist am Ende anders.
- Das Werkzeug ginge nur mit einer Änderung ausserhalb von `research/leiter_pruefung/`.

**Lesarten, Lücken und Summen ≠ 1 sind Befunde, kein Abbruch** (16.4: *„eine Prüfung mit Befund, kein Abbruchkriterium“*).

## In einfacher Sprache

Das Regelwerk sagt schon, wie das Geld auf die neun Bots verteilt wird, je nachdem, auf welcher Stufe jeder Bot steht. Diese Sitzung spielt alle 19 683 möglichen Kombinationen durch und prüft, ob der Text jedes Mal genau eine Verteilung ergibt. Wo der Text zwei Deutungen zulässt oder keine Antwort gibt, schreibt sie das auf. Welche Deutung gilt, entscheidet danach Fable; erst dann wird das eigentliche Programm gebaut.
