# Backlog-Nachtrag (u) — T46.1, die Ausstiegspfade (19.09.2026)

⚠️ **Nummern nach K2i.** Gemessener Stand unverändert (`BACKLOG.md`, 951 Zeilen,
`fef279c`): höchster Block **`2r`**, höchste K-Nummer **`K2k`**. Dieser Nachtrag
gehört in **denselben Block wie (s) und (t)** — die Befunde stammen aus derselben
Sitzung desselben Abends. **Die Vergabe gehört der einarbeitenden Sitzung.**

---

## Für Abschnitt 2, Block `2s` — Fortsetzung

| # | Punkt |
|---|---|
| **T46.1a** | ⭐⭐ **DER SICHERHEITSPUNKT IST GESCHLOSSEN — 9 von 9 gemessen.** Fables Frage: *„Schliesst der Bot offene Positionen, weil er sie ohne Kerze nicht bewerten kann?"* **Nein.** Jeder der neun `forward_test.py` trägt in der Ausstiegsschleife dieselbe Wache: `if symbol not in indicator_data: continue` (bei den beiden Elliott-Bots `price_data`). Zweite unabhängige Messung: **0 Treffer** für einen Schliess-Aufruf in einem Zweig, der einen leeren oder fehlenden Kursrahmen behandelt. ⇒ **Ein Parsing-Fehler oder eine fehlende Kursdatei macht bei keinem der neun einen Trade.** Beleg: `docs/ERGEBNIS_T46-1_ausstiegspfade.md`. ⚠️ Nebenbefund bestätigt: `t3_supertrend` hat den Leer-Zweig auf der **Ladeseite** nicht und überlebt nur durch das `try` (T45.3/T45.4) |
| **T46.1b** | ⚠️⚠️ **DIESELBE WACHE, ANDERE RICHTUNG — neu, niemand hat danach gesucht.** Wird der Trade übersprungen, wird an diesem Tag auch **sein Stop nicht geprüft**: Stop-Loss, Zeitbremse und Ausstiegssignal liegen sämtlich **hinter** dem `continue`. **Und die Wache ist still** — gemessen ein nacktes `continue` in **allen neun**, keine Protokollzeile, keine Meldung, kein Zähler. ⇒ **Fehlt die Kursdatei eines Symbols, ist die Verlustbegrenzung für dessen offene Position an diesem Tag ausser Kraft, und nichts sagt es.** ⭐ **Dieselbe Familie wie D1** (*„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."*) — TB-45 hat die Regel auf der **Eingangsseite** durchgesetzt; die **Ausstiegsseite** hat sie nie erreicht. ⚠️ *Erschlossen, nicht gemessen: Datenausfälle und Marktbewegungen sind nicht unabhängig.* ⚠️ **Nicht gemessen: wie oft es real eingetreten ist** — das stünde in den Bot-Logs |
| **T46.1c** | ⭐ **Der Vorschlag, und ausdrücklich nicht der naheliegende.** ⛔ **Nicht** den `continue` entfernen — ohne Kerze liesse sich der Stop nur auf einem veralteten Kurs bewerten, **genau der Trade, den Fables Frage verhindern will**. ⭐ **Stattdessen melden:** eine Zeile über `shared/ladeprotokoll.py` mit Symbol, Trade-Kennung und Grund. **Ändert kein Verhalten, nur Sichtbarkeit** — dieselbe Klasse wie TB-42 Teil 1, **kein Amendment**. ⚠️ **Berührt alle neun `forward_test.py`, Sperrliste, freigabepflichtig — Betreiberentscheidung** |
| **T46.1d** | ⚠️ **REGISTERFRAGE, offen:** Registertext 7, Ergänzung I (Abschnitt 17.6) kennt den **Kein-Entscheid-Tag**. Ob ein Tag, an dem ein Symbol keine Kerze hatte und sein Stop deshalb ungeprüft blieb, darunter fällt, **steht nirgends**. Gehört geklärt, **bevor** der Backtester-Vergleich solche Tage zählt — sonst entscheidet es sich beim ersten Auftreten, und dann ist der Sieger bekannt |
