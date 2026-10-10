# REGISTER-KOPIE Abschnitt 20 (von 0–56) — Register-Z. 3221–3301 — Commit d950e0365e3d73f5feaaab79f8e2fb750e54add9 — 2026-10-10 — Original sha256 b2d569495e133762b65f035b284af83fc3cb7795563910abcede9e0487a19687 — KOPIE, nicht das Register

## 20. Tatsachennotiz zu Registertext 5f — der Lock (TB-58b, 19.09.2026)

**Datiert angehängt. Nichts entfernt. Kein Registertext wird geändert — hier
wird eine Messung festgehalten**, in der Form von Abschnitt 18. Registertext 5f
(Abschnitt 17.5) verlangt ein `requirements.lock`, „dessen Hash im Register
steht"; bis zu diesem Eintrag stand er nirgends, und 17.10, Zeile 4 hielt
fest, dass es die Datei nicht gab. Seit TB-58 gibt es sie; hier ist ihr Hash.

> **Tatsachennotiz zu Registertext 5f — der Lock. Datum: 19.09.2026.**
>
> Die Umgebung, in der der Selektionslauf rechnet, ist in
> **`requirements.lock`** im Projektwurzelverzeichnis festgehalten, versioniert
> unter Commit `d852bce637ba82ddb60330a7219c6e36a40539c3`.
>
> | | |
> |---|---|
> | SHA-256 der Datei | **`96a5c572a67c65afc66a18d51341330c341e76ee6fe4c250273c59e5988fdfe5`** |
> | Pakete | **67**, sämtlich mit `==` |
> | Interpreter | `3.9.6 (default, Apr 30 2025, 02:07:18) [Clang 17.0.0 (clang-1700.0.13.5)]` |
> | Plattform | `macOS-15.7.9-x86_64-i386-64bit` |
>
> Der Lauf prüft bei Start Interpreter, Paketfassungen und Plattform gegen
> diese Datei und bricht bei Abweichung ab (**Rückgabewert 2**).
>
> ⚠️ **`requirements.txt` ist kein Lock** — es nennt, was installierbar ist;
> `requirements.lock` nennt, was gelaufen ist.

**Jede Zahl der Tabelle wurde in TB-58b selbst gemessen, keine abgeschrieben:**

| | Messung |
|---|---|
| SHA-256 | zweimal unabhängig gerechnet — `shasum -a 256` und `hashlib.sha256` unter `trading-env/bin/python3` — beide `96a5c572…`; derselbe Wert steht in der Auditzeile `lock_sha256` eines bestandenen Starts |
| Versioniert | `git log -- requirements.lock` nennt genau einen Commit, `d852bce`, auf `origin/main`; der Blob im Arbeitsbaum ist byteweise der Blob unter `HEAD` (`git hash-object` = `git rev-parse HEAD:requirements.lock`, `863197fb…`) |
| 67 Pakete, sämtlich `==` | 83 Zeilen, davon 67 Paketzeilen; 0 Paketzeilen ohne `==`; gegen `importlib.metadata` unter `trading-env/bin/python3`: **0 Abweichungen** |
| Interpreter, Plattform | Kopfzeilen `interpreter_voll` und `plattform` der Datei, gleichlautend mit `sys.version` und `platform.platform()` des Betriebsinterpreters; dazu `maschine x86_64` |
| Der Kalender | `pandas-market-calendars==4.6.1` — dieselbe Fassung, die die Tatsachennotiz in 17.5 (gemessen TB-47) nennt; `pandas==2.3.3` |

**Die Probe, die diesen Eintrag erst wahr macht** — in einem Wegwerf-Klon des
Repos (kein Objekt und keine Datei im Arbeitsbaum von `~/trading-bot`
berührt), Interpreter `trading-env/bin/python3`, Snapshot `63e4b6c8…`,
`TB_SELEKTIONSCOMMIT` = `HEAD` des Klons, Einstiegspunkt eine committete
Datei:

| Zustand | Rückgabewert | Meldung |
|---|---|---|
| Lock unverändert (Kontrolle) | **0** | acht Auditzeilen, `lock_sha256 96a5c572…` |
| eine Zeile verfälscht (`pandas==0.0.1`), **committet**, Baum sauber | **2** | „1 Abweichung/en … pandas: Lock 0.0.1, installiert 2.3.3" |
| dieselbe Verfälschung **nicht** committet | **2** | „Arbeitsbaum … nicht sauber (1 Eintrag …  M requirements.lock)" — Abschnitt 19, Bedingung 3, greift **vor** der Lock-Prüfung |
| Lock gelöscht und committet | **2** | „requirements.lock fehlt … `nicht pruefbar` ist nicht gruen" |
| Lock richtig, Interpreter `/usr/bin/python3` (gleicher Build, andere Pakete) | **2** | „24 Abweichung/en", die ersten drei „installiert NICHT" |

Drei Punkte, die diese Tabellen tragen:

1. **Was geprüft wird, ist die Umgebung gegen die Datei — nicht die Datei gegen
   diesen Eintrag.** Der Lauf liest den Lock, der unter dem verlangten Commit
   im Baum liegt, vergleicht Interpreter, Plattform und jede Paketzeile mit
   dem, was `importlib.metadata` tatsächlich findet (kein `pip`, kein
   Kindprozess, keine Netzverbindung), und schreibt den SHA-256 der Datei in
   die Auditzeile `lock_sha256`. Ob diese Zeile `96a5c572…` lautet, ist am
   Audit abzulesen; ein anderer Lock wäre ein anderer Commit und scheiterte
   schon an Abschnitt 19.
2. ⚠️ **Nichts wird installiert, nachgezogen oder repariert.** Der Lauf meldet
   die Zahl der Abweichungen und die ersten drei, dann bricht er ab.
3. **Die Interpreter- und die Plattformzeile allein hätten den fremden
   Interpreter nicht bemerkt** — `/usr/bin/python3` ist derselbe Build wie
   `trading-env/bin/python3`; erst die Paketzeilen unterscheiden die beiden
   (24 Abweichungen). Deshalb sind alle drei Achsen im Lock, nicht nur die
   Fassung.

**Was diese Notiz nicht tut:** kein Selektionslauf, kein signierter Tag, kein
Amendment, kein `pip install`; der Wortlaut von 5f in 17.5 ist nicht
umformuliert. 17.10, Zeile 4 bleibt als Befund vom 18.09.2026 stehen; dass sie
mit `d852bce` und `6518e41` geschlossen ist, steht hier. Die Mindestfassung des
Projekts (`docs/UMGEBUNGEN.md`, in 17.10, Zeile 4 mitgenannt) ist **nicht**
Gegenstand dieser Notiz und bleibt offen.

*Nachgetragen in TB-58b, 19.09.2026. Tatsachennotiz: eine Messung, keine
Festlegung.*

---

