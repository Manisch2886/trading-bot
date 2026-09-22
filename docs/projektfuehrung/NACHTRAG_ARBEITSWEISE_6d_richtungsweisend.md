# Nachtrag zu `ARBEITSWEISE.md` Abschnitt 6d — nur richtungsweisende Rückfragen

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**Anlass:** Betreiberanweisung 22.09.2026, 18:11 — *„Es sollen lediglich
richtungsweisende Rückfragen gestellt werden. Wie definiert per multiple
choice."*
**Einzutragen:** als neuer Unterabschnitt **am Ende von 6d**, nichts entfernen.
⚠️ **Konnte am 22.09. nicht sofort eingetragen werden, weil TB-86 lief** —
`docs/` ist gesperrt, solange eine Sitzung arbeitet.

---

## Der einzutragende Text

### ⭐⭐ Nur richtungsweisende Rückfragen — und die als Multiple Choice (22.09.2026)

⚠️ **Die Regel aus 6d sagt, WIE gefragt wird. Dieser Zusatz sagt, WANN.**
*Der Anlass: Der Betreiber musste in den Claude-Code-Sitzungen fortlaufend
Werkzeugaufrufe bestätigen — Bestätigungen, die keine Entscheidung enthalten.*

**Gefragt wird nur, wenn die Frage richtungsweisend ist. Richtungsweisend
heisst — abschliessend:**

| | Fall |
|---|---|
| **1** | ⭐ **Verfahrensfrage vor dem signierten Tag** — geht an den Betreiber oder an Fable (Aufteilung vom 19.09.2026) |
| **2** | ⭐ **Freigabe** für eine Code-Änderung, für sperrlistennahe Arbeit oder für einen Schritt aus Fables Reihenfolge (36.3) |
| **3** | ⚠️ **Eine Entscheidung, die sich nicht rückgängig machen lässt** — ein Commit auf `main`, ein Hash auf der Sperrliste, der Tag selbst |
| **4** | ⭐ **Zwei gleichwertige Wege, deren Wahl das Ergebnis prägt** — nicht: zwei Wege, die zum selben Ergebnis führen |

⛔ **NICHT richtungsweisend — allein entscheiden und weiterarbeiten:**

| | |
|---|---|
| ⛔ | **Handwerk:** Dateiname, Ablageort, Reihenfolge der Schritte, Schnitt eines Auftrags, Nachweismethode, Dokumentstruktur *(so schon in der Aufteilung vom 19.09.2026)* |
| ⛔ | **Jede Werkzeug-Bestätigung.** ⭐ Werkzeuge werden über `.claude/settings.local.json` freigegeben, nicht einzeln bestätigt — siehe unten |
| ⛔ | **Ein Zwischenstand.** Er wird gemeldet, nicht zur Abstimmung gestellt |
| ⛔ | ⚠️⚠️ **Ein Abbruchkriterium.** Es führt zu **ABBRUCH und Meldung** — nie zu einer Rückfrage. *Wer bei einem Abbruchkriterium fragt, verwandelt eine Wache in eine Verhandlung* |

### Die Form bleibt, wie 6d sie festlegt

Möglichkeiten vollständig · **eine** Empfehlung ausdrücklich benannt · Begründung
samt dem, was die Empfehlung schlechter macht · **anklickbar, nicht im
Fließtext.**

### ⭐ Werkzeuge werden konfiguriert, nicht bestätigt

Seit dem 22.09.2026 trägt `.claude/settings.local.json` **67 Erlaubnismuster**
und **55 Sperren**. *Zuvor bestand sie aus Einmal-Genehmigungen — komplette
Commit-Nachrichten aus TB-75, die nur sich selbst genehmigten und bei jedem
neuen Befehl erneut fragten.*

⚠️⚠️ **Zwei Einträge widersprachen dabei den Sicherheitsregeln und sind
entfernt:** `Bash(env)` (gibt alle Umgebungsvariablen aus — Abschnitt 7 verbietet
es ausdrücklich) und `Bash(crontab -l)` (Regel K2a: *„wird nie ungefiltert
ausgegeben"*). **Beide waren dauerhaft genehmigt.**

⭐ **Die Sperren decken:** Schlüsselausgabe (`env`, `printenv`, `security`,
`.env`, `*.key`, `*.pem`) · Zerstörung (`rm`, `git reset --hard`, `git clean`,
`git push --force`) · Netz (`curl`, `wget`, `ssh`) · **Schreibzugriff auf jede
Sperrlisten-Datei** · und `python3 faltenplan.py`, bis TB-86 die Einmal-Schreibsperre
eingebaut hat.

⚠️⚠️ **Die Grenze, die dazugehört:** Eine Berechtigung sperrt den **benannten
Befehl**, nicht dieselbe Wirkung in Python verpackt. `Bash(python3:*)` ist
erlaubt — der Berechtigungsschutz fängt also das Versehen ab, nicht den Umweg.
⭐ **Der eigentliche Schutz ist die Einmal-Schreibsperre im Programm selbst
(36.1 (2)):** Sie wirkt unabhängig davon, wer das Programm aufruft. *Das ist
`A8` in Reinform — eine Regel ist erst eine Wache, wenn sie jemand ausführt.*

**Die alte Fassung ist gesichert:**
`.claude/settings.local.json.2026-09-22_vor_TB86.bak` (5146 B, Stand 21.09.,
19:05). ⛔ Nichts wurde überschrieben.

⭐ **Die Berechtigungsdatei kommt ins Repo** (Betreiberentscheidung 22.09.,
eigener Commit `6278888`). **Grund:** Sie sagt, welche Befehle eine Sitzung vor
dem signierten Tag ausführen durfte — **Nachweis derselben Art wie die
Sperrliste.** Gemessen enthält sie keine Geheimnisfelder (`token`, `key`,
`secret`, `password`: je 0); ein Mac, also kein Maschinenkonflikt. `*.bak`
steht in `.gitignore`.

### ⚠️⚠️ Eine Regel, die am selben Tag ein Problem verursacht hat

**Der Vorfall, 22.09.2026, 18:26:** Der steuernde Chat legte drei Dateien in den
Arbeitsbaum (`.claude/settings.local.json`, eine `.bak`-Sicherung, einen
`.vorschlag`) — kurz bevor TB-86 startete. **Die Sitzung fand sie vor, erkannte
sie als nicht von ihr stammend und konnte ihren Schritt „Status leer" nicht
herstellen, ohne über fremde Dateien zu entscheiden.** Sie hat richtig gehandelt
und gefragt; die Frage kostete einen Umlauf.

> ⭐⭐ **Regel:** Wer eine Datei in den Arbeitsbaum legt, gibt **im selben Zug**
> an, was damit geschehen soll — committen, ignorieren oder vor dem nächsten
> Auftrag entfernen. **Eine Datei ohne Anweisung ist für die nächste Sitzung
> eine Entscheidung, die sie nicht treffen darf.**
>
> ⚠️ Und: Die Regel *„nichts nach `docs/` schreiben, solange eine Sitzung
> läuft"* gilt **sinngemäss für den ganzen Arbeitsbaum**, nicht nur für `docs/`.

---

## In einfacher Sprache

Bisher stand in der Arbeitsweise, **wie** eine Frage gestellt wird: mit allen
Möglichkeiten, einer Empfehlung und zum Anklicken. Jetzt steht auch dabei,
**wann** überhaupt gefragt wird — nämlich nur bei vier Arten von Fragen:
Verfahrensfragen vor dem Stichtag, Freigaben, Unumkehrbares, und echte
Weggabelungen.

Alles andere wird entschieden und gemacht: Dateinamen, Reihenfolgen, wie etwas
belegt wird. Und Werkzeugbestätigungen verschwinden ganz — die sind jetzt vorab
konfiguriert statt einzeln abgenickt.

⚠️ **Ein Satz ist dabei besonders wichtig:** Wenn ein Abbruchkriterium greift,
wird **nicht gefragt**, sondern abgebrochen und gemeldet. Eine Sitzung, die bei
einem Abbruchkriterium nachfragt, macht aus einer Sicherung eine Verhandlung.

**Beim Aufräumen der Werkzeugliste kam noch etwas heraus:** Zwei Befehle waren
dauerhaft freigegeben, die die Sicherheitsregeln des Projekts ausdrücklich
verbieten — einer davon gibt sämtliche Umgebungsvariablen aus, also auch
Zugangsschlüssel. Beide sind jetzt gesperrt.
