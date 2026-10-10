# REGISTER-KOPIE Abschnitt 19 (von 0–56) — Register-Z. 3106–3220 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 19. Registertext 5e, Ergänzung — die Codeherkunft (TB-58b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein bestehender Registertext wird
umgeschrieben — hier wird Registertext 5e (Abschnitt 17.4) ergänzt**, in der
Form von Abschnitt 18. Das ist der Nachtrag, den
`docs/ERGEBNIS_TB-58_startpruefungen.md` angekündigt hat: TB-58 hat die
Prüfungen gebaut und ausdrücklich keinen Registertext angefasst.

**Art der Änderung nach der Drei-Kategorien-Regel (F17): eine Entscheidung.**
Sie trifft etwas, das im Register offen war — 5e sagt, welche **Daten** ein
Lauf gelesen hat; nichts sagte, welcher **Code** sie gelesen hat. Sie ist vor
dem Tag zulässig, ihre Begründung nennt kein Ergebnis, und sie hat keine
bekannte Wirkung auf die Zulassung eines Bots: sie entscheidet, wann ein
**Lauf** ein Lauf dieses Registers ist, nicht, welcher Bot durchkommt.

> **Registertext 5e, Ergänzung Codeherkunft. Datum: 19.09.2026.**
>
> Der Selektionslauf prüft bei Start, dass sein **Einstiegspunkt** und der
> **Resolver** unter derselben Git-Wurzel liegen, dass deren `HEAD` der
> registrierte Commit ist und dass der **Arbeitsbaum sauber** ist; bei
> Verletzung bricht er ab (**Rückgabewert 2**). Wurzel, Commit und Sauberkeit
> werden im Lese-Audit protokolliert. **Ein Lauf ohne diese Angaben oder mit
> abweichender Wurzel ist kein Lauf dieses Registers.**
> ⚠️ **Im Regelbetrieb gilt keine dieser Bedingungen.**
>
> **Begründung:** Liegen Aufrufer und Resolver in verschiedenen Bäumen,
> beschreibt kein einzelner Commit den gelaufenen Code. Das Lese-Audit belegt,
> **welche Daten** gelesen wurden; es sagt nichts darüber, **welcher Code**
> gelesen hat.
>
> ⭐ **Das Wegwerfbaum-Muster** — eine Bot-Kopie in einem temporären Verzeichnis
> mit der echten `shared/` — **ist eine Testtechnik des Regelbetriebs und im
> Selektionsmodus unzulässig.**

> ⭐⭐ **Ergänzungen zu 5e (41.1 A10, 41.2 B5, 41.3 C6, 42.1 D1, Fable 24b–25a,
> TB-108, 25.09.2026):** Unter dem Selektionsmodus gibt es **keinen Rückfall
> auf eingebaute Voreinstellungen**, gleich welcher Art; eine fehlende Eingabe
> ist Rückgabewert 2 (**41.1, A10**). Jedes Modul des Laufbereichs bezieht
> Kurs- und Universumspfade **über den Resolver** (`shared/paths.py`, direkt
> oder über `strategy_paths.get_strategy_paths()`) (**41.2 B5**, Fundstelle
> nach **42.1 D1**). Ein Modus-Lauf ist ein Lauf unter dem Selektionsmodus des
> Resolvers; Hilfsordner und Ersatzwurzeln tragen keinen Nachweisteil
> (**41.3, C6**). Der Registertext oben bleibt zeichengleich.

**Was der Code am Tag dieses Eintrags tut** (`shared/paths.py`, Commit
`6518e413b17dd4b7f5c624549aa145f94fca3a96` auf `main`; jede Zeile gemessen,
Nachweise in `docs/ERGEBNIS_TB-58_startpruefungen.md` und
`shared/test_startpruefungen.py`, 44 Proben mit Mutationsgegenprobe):

| Satz des Registertexts | Umsetzung | Gemessen |
|---|---|---|
| Einstiegspunkt und Resolver unter derselben Git-Wurzel | `sys.modules["__main__"].__file__` und `shared/paths.py`, beide über `realpath` und `git rev-parse --show-toplevel` | gespaltener Baum aus einem anderen Repo **und** aus einem Ordner ohne Git: rc 2, die Meldung nennt beide Wurzeln; `python -c` (kein Einstiegspunkt): rc 2 |
| `HEAD` ist der registrierte Commit | der Modus **trägt** den erwarteten Commit in der dritten Umgebungsvariablen `TB_SELEKTIONSCOMMIT` (7–40 Hex-Zeichen; Zweignamen wie `main` werden abgewiesen); `git rev-parse HEAD` muss damit beginnen | falscher Commit rc 2; fehlende Variable bei gesetzten anderen beiden rc 2; Variable allein `Selektionsfehler` |
| Arbeitsbaum sauber | `git status --porcelain` über `shared/`, `strategies/` und `requirements.lock` (`ARBEITSBAUM_PFADE`), untracked zählt; ⚠️ **nicht** über `data/` — die ist versioniert und wird vom Abruf-Cron laufend verändert, ein Lauf aus dem Snapshot darf daran nicht scheitern | veränderte Datei unter `shared/`, neue Datei unter `strategies/`, veränderter Lock: je rc 2 mit Nennung; neue Datei unter `data/` stört nicht |
| Rückgabewert 2 | `SystemExit(2)` beim Import, nicht `Exception` — ein `except Exception` im Aufrufer kann den Abbruch nicht in einen stillen Weiterlauf verwandeln; der Wert steht genau einmal | rc 2 in jeder Probe, `stdout` leer |
| Wurzel, Commit, Sauberkeit protokolliert | drei der acht Auditzeilen `[paths] codewurzel / commit / arbeitsbaum` auf `stderr` nach bestandener Prüfung, dieselben Werte über `paths.startpruefung()` und `paths.audit_zeilen()` | `stderr`-Zeilen == `audit_zeilen()`; gegen den echten Arbeitsbaum 9 / 9 Bot-Einstiegspunkte |
| Im Regelbetrieb gilt nichts davon | alles im `else`-Zweig des Modus; `subprocess`, `importlib.metadata`, `platform`, `hashlib` werden erst innerhalb der Prüffunktionen importiert | ohne Modus **0 / 0 / 0** `git`-, Paket- und `os.system`-Aufrufe (zählende Attrappe), 144 Pfade über 9 Bots zeichengleich wie vor TB-58 |

> ⭐⭐ **Sauberkeit über den Laufbereich — beschlossen, nicht vollzogen; und die
> Ausnahme für registrierte Protokolle (42.2 E2, 42.3 F8, Fable 25b/25c, TB-108,
> 25.09.2026):** Die Sauberkeitsprüfung des Arbeitsbaums erstreckt sich künftig
> auf **jeden Pfad des Laufbereichs**, nicht nur auf die drei Pfade in der
> Zeile „Arbeitsbaum sauber" oben (Registertext in **42.2, E2**; `data/` bleibt
> ausgenommen). ⚠️ **Heute nicht vollzogen** — `ARBEITSBAUM_PFADE` ist
> unverändert; die Erweiterung ist Tag-Vorbedingung und eigener Auftrag.
> **Registrierte Protokolle** (heute nur
> `research/vorregistrierung/ergebnisse/herkunft_protokoll.jsonl`) sind davon
> ausgenommen wie `data/`; der Kettenhash ersetzt dort die Sauberkeit
> (**42.3, F8**). Diese Ausnahme steht damit **vor** dem Erweiterungsauftrag im
> Register, wie Fable es verlangt. Tabelle und Text oben bleiben zeichengleich.

> ⭐⭐ **Vollzogen in TB-112, siehe 44.2 (44-7; TB-113, 26.09.2026):**
> `ARBEITSBAUM_PFADE` trägt seit `9d711dc` 15 Einträge — `shared`,
> `strategies`, `requirements.lock` und die 12 Module des Laufbereichs
> ausserhalb dieser Ordner als Einzeldateien; `herkunft_protokoll.jsonl` ist
> namentlich ausgenommen (`REGISTRIERTE_PROTOKOLLE`, `:(exclude)`), `data/`
> weiter. Nur unter dem Modus wirksam. Die Liste steht als Tatsachennotiz
> neben der Laufbereichsmessung (44-8). Kasten, Tabelle und Text oben bleiben
> zeichengleich.

> ⭐ **Pflege von `ARBEITSBAUM_PFADE`: siehe 45.4** (Fable 26a R4, TB-114,
> 26.09.2026). Kasten, Tabelle, Text und die Marken oben bleiben
> zeichengleich.

Drei Punkte, die diese Tabelle tragen:

1. **„Der registrierte Commit" ist heute der Wert, den der Modus mitbringt.**
   Der signierte Tag (Abschnitt 13) existiert noch nicht; bis dahin sagt
   `TB_SELEKTIONSCOMMIT`, welcher Commit verlangt ist, und die Prüfung misst,
   ob der Baum ihn hat. Sobald der Tag steht, ist es sein Commit. Die Bauart
   ist dieselbe wie beim Snapshot-Hash: der Modus **trägt** den Sollwert, statt
   ihn irgendwo zu suchen, und ein Kindprozess erbt ihn.
2. ⚠️ **Der Lese-Audit als Ganzes (5e, 17.4) ist weiterhin nicht gebaut** —
   17.10, Zeile 3 gilt fort. Was heute existiert, sind die acht Auditzeilen des
   Starts; der spätere Lese-Audit übernimmt sie über `audit_zeilen()`, ohne
   eine zweite Fassung zu pflegen. Der Registertext beschreibt damit etwas, das
   der Code zum Teil noch nicht kann — benannt, nicht verschwiegen (dieselbe
   Regel wie 16.11 und 17.10).
3. **Das Wegwerfbaum-Muster** wird von Bedingung 1 getroffen: eine Bot-Kopie in
   einem temporären Ordner, die die echte `shared/` importiert, hat einen
   anderen Einstiegspunkt als Resolver-Wurzel — im Selektionsmodus rc 2. Im
   Regelbetrieb bleibt es erlaubt und wird weiter gemessen
   (`shared/test_strategy_paths.py`, Probe E, ohne Modus).

**Was diese Ergänzung nicht tut:** kein Selektionslauf, kein signierter Tag,
kein Amendment; der Wortlaut von 5e in 17.4 bleibt stehen und gilt weiter;
17.10 wird nicht umgeschrieben — seine Zeilen beschreiben den Stand vom
18.09.2026, und ob eine davon inzwischen geschlossen ist, steht hier und in
Abschnitt 20, nicht dort.

*Nachgetragen in TB-58b, 19.09.2026. Entscheidung nach F17: vor dem Tag, ohne
Ergebnis in der Begründung, ohne Wirkung auf die Zulassung eines Bots.*

---

