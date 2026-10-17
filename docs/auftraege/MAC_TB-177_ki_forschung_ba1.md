# TB-177 KI-Forschung BA1: Abruf- und Einfrierschicht `ki_forschung/`, Kostenbremse, Wachen-Test — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 21:05** (Helfer BAU177, per Skript aus Bausteinen, `/tmp/w36/sc/tb177/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Schritt 0 bis T an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `ad64eab`; Start am HEAD `ad64eabee2369474b522fe196a30aae52152096a`.** Neu gemessen nach TB-176a (`ad64eab`): `shared/`, `strategies/`, `notifications/`, `.gitignore`, Sperrliste (`research/vorregistrierung/herkunft.py`) seit `6da15e0` unverändert (git log --name-only); BACKLOG Rang 1 endet mit dem TB-176a-Eintrag, Journal mit FM.

**Sitzungstitel:** `TB-177` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `ad64eabee2369474b522fe196a30aae52152096a` · **Start:** über den Sitzungswächter (`starte_TB-177`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-177_ki_forschung_ba1.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`. **Belege:** `docs/belege/TB-177/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-177_ki_forschung_ba1.md`.
**Grundlage:** Betreiberentscheide 17.10.2026 (Haiku; Deckel Sammler 3 $/Monat und KI-Bots eigener Deckel 3 $/Monat, getrennt gebucht; keine Websuche; Aktien nur UCITS-ETFs; KI-Bots rein KI im Paper Trade, MI1 (b) vom Betreiber nur für Paper gebrochen; streng getrennt von den neun: eigene DBs, nicht in `discover_bots`, nicht im Selektionslauf). Pläne PLAN_KIBOTS (BA1) und PLAN_KISAMMLER des steuernden Chats, 17.10.2026 (ausserhalb des Repos). Am Bau-HEAD gemessen: `shared/claude_client.py` `MODEL_HAIKU` Z. 31, `agent_abgeschaltet` Z. 42, `call_claude` Z. 103 (md5 `7086e27839e6e2825c0d4df9bc133f58`); `notifications/monitor.py` `ASSET_CLASS` Z. 86, `discover_bots` Z. 126; `shared/paths.py` `ARBEITSBAUM_PFADE` Z. 239; `.gitignore` `*.db` Z. 29.
**Schlüssel (nur Namen, kein Wert gelesen):** `ANTHROPIC_API_KEY` liest `claude_client.get_client()` selbst (Umgebung oder `config/email_config.py`); `.env` nennt ihn nicht (Namen in `.env`: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_USER_ID`, `DASHBOARD_ACCESS_TOKEN`, `DASHBOARD_HOST`, `BINANCE_TESTNET_API_KEY`, `BINANCE_TESTNET_API_SECRET`, `BINANCE_TESTNET_BETRAG_USDT`, `XAI_API_KEY`). `ki_forschung/` liest keinen Schlüssel. Gesetzt wird er erst in BA7.
**Handelscode:** nein. `ki_forschung/` ist kein Bot, öffnet keine Bot-DB, legt keine Order an; geprüft durch W1–W3 des Wachen-Tests.
**Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ B (vier Dateien anlegen) ⇒ T (Wachen-Test) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 35 („Opus Trading Bots-17.10.2026 b“), 17.10.2026, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript, Zeit 2026-10-17T19:08:50.676Z UTC): Your questions have been answered: "Gibst du TB-177 frei? Das ist der erste Bauauftrag der KI-Forschung (BA1). Er legt den neuen Ordner ki_forschung/ ausserhalb des Laufbereichs an, mit vier Dateien. (1) abrufe.py speichert eingefrorene Abrufe nur anfügend, mit Prüfzahl und Zeitstempel. (2) aufrufe.py ist die Kostenbremse: je Topf höchstens 3 $ im Monat, einer für den Sammler und einer für die KI-Bots, geprüft vor jedem Aufruf. (3) pfade.py. (4) Ein Wächter-Test mit 50 Prüfungen: kein Zugriff auf die neun Bots, ihre Datenbanken oder Laufdateien, keine Websuche. Kein Handelscode, keine echten Abrufe, kein API-Aufruf, kein Cron, kein Geld; das kommt erst mit BA7 und eigener Karte. Ein frischer Gegenleser und zwei enge Gegenleser haben den Code geprüft. Gefunden und geschlossen sind sieben Lücken, darunter zwei Wege, den Deckel zu unterlaufen. Bewusst offen bleibt eine Grenze: Gebucht wird der echte Preis, deshalb kann ein einzelner Aufruf den Deckel um seinen Schätzfehler überschreiten. Der Haiku-Preis von 1 $ / 5 $ je Million Token ist eine Annahme und wird in BA7 gemessen. bau.sh endet mit rc 0, die Simulationen waren gut (auf dem Gerät mit Python 3.10, am Mac läuft 3.9). Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Auf dieser Grundlage bauen Sammler, Filtervergleich und die drei KI-Bots auf."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. TB-177 ändert keinen Handelscode und keine Datei der Sperrliste; es legt genau vier neue Dateien unter `ki_forschung/` an.

## Was entsteht

- `ki_forschung/pfade.py` — Pfade; `abrufe.db` und `aufrufe.db` liegen in `ki_forschung/` (git-ignoriert über `*.db`, `.gitignore` Z. 29).
- `ki_forschung/abrufe.py` — Einfrierschicht: je Abruf Rohkopie, sha256, `abgerufen_utc` (= Vintage, nur intern gesetzt, festes UTC-Format mit CHECK) in `abrufe.db`, nur anfügend (Trigger gegen UPDATE, DELETE und INSERT mit vorhandener id, dazu `recursive_triggers` je Verbindung); Ausfall wird gebucht, nicht nachgeholt; `stand()` vergleicht die Grenze als Zeitpunkt (`Z`, `+hh:mm`, Bruchteile; ohne Zeitzone abgewiesen) und liefert nur, was bis dahin eingefroren war. Quellen: alfred, fear_greed, yfinance, binance_spot, rss. Keine Websuche. In BA1 kein echter Abruf.
- `ki_forschung/aufrufe.py` — Aufrufbuch und Bremse: Töpfe `sammler` und `bots` je 3 $ im UTC-Monat; Buchungszeit nur intern; `aufrufe.db` nur anfügend wie `abrufe.db`; vor jedem Aufruf Monatssumme + Höchstpreis (Eingabe-Bytes als Token-Obergrenze + Zuschlag 500 Token für den Formatierungs-Overhead, `max_tokens`) in einer Transaktion; Reservierung, dann Abrechnung aus `usage`; Fehlerpfad lässt die Reservierung stehen (zu viel, nie zu wenig); Notschalter `ki_sammler`/`ki_bots` in `config/agenten_aus.txt` über `agent_abgeschaltet`; nur `MODEL_HAIKU`, `tools=None`; `shared/claude_client.py` nur importiert. Preis Haiku 1 $ (Eingabe) / 5 $ (Ausgabe) je Million Token (Preisliste des Anbieters, **nicht im Repo gemessen**; Bestätigung in BA7).
- `ki_forschung/test_ki_wachen.py` — Wachen-Test, ohne Netz und ohne API-Aufruf (50 Prüfungen, davon 17 Gegenproben an verfälschten Kopien in temporären Ordnern).

## Verboten

Kein echter Abruf, kein API-Aufruf, kein Cron (BA7). Kein `ANTHROPIC_API_KEY` setzen oder lesen. Nichts unter `strategies/`, `shared/`, `notifications/`, `dashboard/`, `broker/`, `data/`, `config/`, `research/` ändern. Kein `git add -A`, kein `-f`, kein `git stash`, kein `rm`, kein `mv`. **Schreiben darf die Sitzung nur:** `ki_forschung/` (genau die vier Dateien, Schritt B, `cp`), `BEL`, das Ergebnis, `BACKLOG.md` und `JOURNAL.md` (Schritt A, nur mit dem A-Befehl).

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `ad64eabee2369474b522fe196a30aae52152096a`, genau die Einträge `[' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-177_ki_forschung_ba1.md']`, `ki_forschung/` gibt es nicht, Karte gefüllt; sonst **ABBRUCH**):

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb177_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-177_ki_forschung_ba1.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "ad64eabee2369474b522fe196a30aae52152096a": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "ad64eabee2369474b522fe196a30aae52152096a": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
if os.path.exists("ki_forschung"): f.append("ki_forschung/ gibt es schon")
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-177_ki_forschung_ba1.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Anhänge holen (genau dieser Befehl). Soll genau: `pfade.py aa64fab44b4be80a8b2a74d55487ac91ff202ba01fdd6811ba2afe11db6b47a6`; `abrufe.py 8e18fc3ccf60dc4fd561c5e118ce8eff5444da2a432c8ee71d32d78051a8d83c`; `aufrufe.py 88dfdb05b0f972dc3ed93abaa1c28c3858a3ed0e8362388c2e12c30687a0f337`; `test_ki_wachen.py 40b7a2b9c525495a5a5bb1f897b84ed42b56dcf7877dc8d9b1acc0c126bfaa46`; `Dateien 4`; sonst **ABBRUCH**:

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-177_ki_forschung_ba1.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/tb177_' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Dann genau diese Zeilen, Commit `TB-177 Schritt 0: Auftrag`, pushen ⇒ **⟨S0⟩**; danach `git status --porcelain` — Soll: keine Ausgabe:

```
trading-env/bin/python3 -B -c "import subprocess, sys; z = [l[3:] for l in open(sys.argv[1], encoding='utf-8').read().split(chr(10)) if l]; print('git add', len(z)); raise SystemExit(subprocess.run(['git', 'add', '--'] + z).returncode)" "$TMPDIR/tb177_0a.txt"
```

## Schritt V — Voraussetzungen

```
mkdir -p docs/belege/TB-177
cp "$TMPDIR/tb177_0a.txt" docs/belege/TB-177/0a_status.txt
{ trading-env/bin/python3 -B - <<'PYEOF'
import hashlib, os
md5 = {"shared/claude_client.py": "7086e27839e6e2825c0d4df9bc133f58", "notifications/monitor.py": "fa8c8a964ab5499fdf729e12f62b2448", "shared/paths.py": "7ee531d0456f2be357192da63995894f"}
n = 0; nein = 0
def p(name, ok):
    global n, nein
    n += 1; nein += 0 if ok else 1; print(('ja   ' if ok else 'NEIN ') + name)
for f, m in md5.items(): p('md5 %s = Bau' % f, hashlib.md5(open(f, 'rb').read()).hexdigest() == m)
p('ki_forschung/ fehlt', not os.path.exists('ki_forschung'))
treffer = [os.path.join(d, x) for o in ('shared', 'strategies', 'notifications') for d, _u, fs in os.walk(o) for x in fs if x.endswith('.py') and 'ki_forschung' in open(os.path.join(d, x), encoding='utf-8', errors='replace').read()]
p('kein Modul in shared/strategies/notifications nennt ki_forschung %s' % treffer[:3], not treffer)
print('Pruefungen: %d, NEIN: %d' % (n, nein)); raise SystemExit(1 if nein else 0)
PYEOF
} > docs/belege/TB-177/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-177/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (md5 von `shared/claude_client.py`, `notifications/monitor.py`, `shared/paths.py` = Bau; `ki_forschung/` fehlt; kein Modul unter `shared/`, `strategies/`, `notifications/` nennt `ki_forschung`). Abbruch: `printf '%s\n' "V: <Zeile>" > docs/belege/TB-177/abbruch.txt`, `git add` mit Namen für `BEL`-Dateien, Commit `TB-177 Abbruch: V`, pushen, melden.

## Schritt B — vier Dateien anlegen

```
mkdir ki_forschung
cp "$TMPDIR/tb177_pfade.py" ki_forschung/pfade.py
cp "$TMPDIR/tb177_abrufe.py" ki_forschung/abrufe.py
cp "$TMPDIR/tb177_aufrufe.py" ki_forschung/aufrufe.py
cp "$TMPDIR/tb177_test_ki_wachen.py" ki_forschung/test_ki_wachen.py
{ trading-env/bin/python3 -B - <<'PYEOF'
import hashlib
soll = {"pfade.py": "aa64fab44b4be80a8b2a74d55487ac91ff202ba01fdd6811ba2afe11db6b47a6", "abrufe.py": "8e18fc3ccf60dc4fd561c5e118ce8eff5444da2a432c8ee71d32d78051a8d83c", "aufrufe.py": "88dfdb05b0f972dc3ed93abaa1c28c3858a3ed0e8362388c2e12c30687a0f337", "test_ki_wachen.py": "40b7a2b9c525495a5a5bb1f897b84ed42b56dcf7877dc8d9b1acc0c126bfaa46"}
ok = True
for f, s in soll.items():
    i = hashlib.sha256(open('ki_forschung/' + f, 'rb').read()).hexdigest(); print(f, i); ok = ok and i == s
raise SystemExit(0 if ok else 1)
PYEOF
} > docs/belege/TB-177/b_sha.txt 2>&1; echo "rc $?" >> docs/belege/TB-177/b_sha.txt
```

Soll: vier Zeilen `<datei> <sha256>` gleich `pfade.py aa64fab44b4b…`, `abrufe.py 8e18fc3ccf60…`, `aufrufe.py 88dfdb05b0f9…`, `test_ki_wachen.py 40b7a2b9c525…`, letzte Zeile `rc 0`.

## Schritt T — Wachen-Test

```
trading-env/bin/python3 -B ki_forschung/test_ki_wachen.py > docs/belege/TB-177/t_wachen.txt 2>&1; echo "rc $?" >> docs/belege/TB-177/t_wachen.txt
git status --porcelain > docs/belege/TB-177/t_status.txt
cat docs/belege/TB-177/t_status.txt
```

Soll: `t_wachen.txt` vorletzte Zeile `Pruefungen: 50, FEHLT: 0`, letzte `rc 0`; `t_status.txt` genau `?? docs/belege/TB-177/` und `?? ki_forschung/` (kein `abrufe.db`/`aufrufe.db`, kein `__pycache__`). **Abbruch in T:** kein B-Commit; `printf '%s\n' "T: nicht wie Soll" > docs/belege/TB-177/abbruch.txt`, `git add` mit Namen für die `BEL`-Dateien (nicht `ki_forschung/`), Commit `TB-177 Abbruch: T`, pushen, melden; `ki_forschung/` bleibt unverfolgt liegen.

Dann genau diese Zeilen, Commit `TB-177 B: ki_forschung/ (Abruf- und Einfrierschicht, Aufrufbuch mit Bremse, Wachen-Test)`, pushen:

```
git add ki_forschung/pfade.py
git add ki_forschung/abrufe.py
git add ki_forschung/aufrufe.py
git add ki_forschung/test_ki_wachen.py
git add docs/belege/TB-177/0a_status.txt
git add docs/belege/TB-177/v_voraussetzung.txt
git add docs/belege/TB-177/b_sha.txt
git add docs/belege/TB-177/t_wachen.txt
git add docs/belege/TB-177/t_status.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

Ergebnis `docs/ERGEBNIS_TB-177_ki_forschung_ba1.md`: Kopf mit Commits; Kurz; 0a; V (letzte Zeilen); B (`b_sha.txt` wörtlich); T (`t_wachen.txt` wörtlich); offene Entscheide (unten); „In einfacher Sprache“. BACKLOG und Journal (genau dieser Befehl, nach dem B-Commit; hängt die Zeile an die Rang-1-Zelle nach dem TB-176a-Anker an und setzt den Journal-Block vor `## Wiederkehrende Lehren`; Kennung = nächste nach der letzten `## F?`-Überschrift, am Bau-HEAD FM ⇒ FN). Soll: letzte Zeile `rc 0`, `Pruefungen: 6, NEIN: 0`:

```
{ trading-env/bin/python3 -B - "$(TZ=Europe/Berlin date +%d.%m.%Y)" "$(git rev-parse --short HEAD)" "$(git log -1 --format=%h --grep='^TB-177 Schritt 0')" <<'PYEOF'
import json, re, sys
datum, cb, s0 = sys.argv[1:4]
anker = "E2 mit TB-176a: `auswertung.py` und `embargo_neun.py` lesen `<bot>_alle_trades.csv` (R107 (e)) |"
bz = " · **KI-Forschung BA1 mit TB-177 (⟨DATUM⟩, Journal ⟨Kennung⟩)**: `ki_forschung/` (pfade, abrufe, aufrufe, test_ki_wachen; Commit ⟨Commit B⟩) ausserhalb der neun, des Laufbereichs und von `discover_bots`; Einfrierschicht nur anfügend mit Vintage-Stempel; Aufrufbuch mit Monatsbremse je Topf 3 $ (sammler, bots), nur Haiku, keine Websuche; Wachen-Test ⟨N⟩/0 mit Gegenproben; kein echter Abruf, kein API-Aufruf, kein Handelscode; **offen: E1 Haiku-Preis (BA7), E3 Formatierungszuschlag messen (BA7)**; nächste: BA3 Regelblätter/Katalog/Prompts mit Hash, BA2 Sammler (mit R108 (b)), BA7 am Mac (Schlüssel, Cron, Erstlauf)"
jb = "## ⟨Kennung⟩ — TB-177: KI-Forschung BA1 (`ki_forschung/`: Abruf- und Einfrierschicht, Aufrufbuch mit Kostenbremse, Wachen-Test)\n*Quelle: `docs/ERGEBNIS_TB-177_ki_forschung_ba1.md`, Auftrag `docs/auftraege/MAC_TB-177_ki_forschung_ba1.md`, Belege `docs/belege/TB-177/`, Commits `⟨S0⟩` (S0, Auftrag) und `⟨Commit B⟩` (B, vier Dateien), danach der Abgabe-Commit.*\n\n### Was gemessen ist\n- B: vier neue Dateien unter `ki_forschung/`, sha256 wie Soll (`b_sha.txt`, rc 0).\n- T: Wachen-Test ⟨N⟩ Prüfungen, FEHLT 0, rc 0 (`t_wachen.txt`), darunter Gegenproben an verfälschten Kopien in Temp-Ordnern; `t_status.txt` nur `ki_forschung/` und `BEL` unverfolgt, kein `.db`, kein `__pycache__`.\n- Kein echter Abruf, kein API-Aufruf, kein Schlüssel gelesen; `shared/`, `strategies/`, `notifications/` unverändert (`f_numstat.txt`).\n\n### Was offen bleibt\n- E1 Haiku-Preis (1 $/5 $ je Million Token, Preisliste, nicht gemessen) und E3 Formatierungszuschlag (500 Token, gewählt): am Erstlauf messen (BA7).\n- BA3 Regelblätter/Katalog/Prompts mit Hash, BA2 Sammler (R108 (b)), BA7 Schlüssel, Cron, Erstlauf.\n\n### In einfacher Sprache\nDer Ordner für die KI-Versuche steht neben den neun Bots: Datenspeicher, der festhält, was wann bekannt war, und ein Kostenbuch mit Monatsbremse. Er ruft noch nichts ab und kostet nichts; ein Selbsttest belegt, dass er die neun Bots nicht berührt und die Bremse greift.\n\n*Geschrieben ⟨DATUM⟩ von der Mac-Sitzung TB-177. Quellenvermerk: siehe Kopf.*\n\n---\n\n"
n = 0; nein = 0
def p(name, ok):
    global n, nein
    n += 1; nein += 0 if ok else 1; print(('ja   ' if ok else 'NEIN ') + name)
N = re.findall(r'^Pruefungen: (\d+), FEHLT: 0$', open('%st_wachen.txt' % 'docs/belege/TB-177/', encoding='utf-8').read(), re.M)
BLp, JLp = 'docs/projektfuehrung/BACKLOG.md', 'docs/projektfuehrung/JOURNAL.md'
bl = open(BLp, encoding='utf-8').read().split('\n'); jl = open(JLp, encoding='utf-8').read()
r1 = [i for i, l in enumerate(bl) if l.startswith('| **1** | **TB-30b')]
ken = re.findall(r'(?m)^## ([A-Z]{2}) \u2014 ', jl)
def weiter(k): return k[0] + chr(ord(k[1]) + 1) if k[1] != 'Z' else chr(ord(k[0]) + 1) + 'A'
neu = weiter(ken[-1]) if ken else '??'
ok = len(r1) == 1 and bl[r1[0]].endswith(anker) and len(N) == 1 and re.fullmatch('[0-9a-f]{7}', cb) and re.fullmatch('[0-9a-f]{7}', s0) and jl.count('\n## Wiederkehrende Lehren\n') == 1 and ('## ' + neu + ' \u2014 ') not in jl
p('Vorbedingungen (Rang-1-Anker, t_wachen, Commits, Journal-Anker, Kennung %s frei)' % neu, ok)
if ok:
    f = lambda t: t.replace('\u27e8DATUM\u27e9', datum).replace('\u27e8Kennung\u27e9', neu).replace('\u27e8Commit B\u27e9', cb).replace('\u27e8S0\u27e9', s0).replace('\u27e8N\u27e9', N[0])
    zeile, block = f(bz), f(jb)
    p('keine Platzhalter mehr', '\u27e8' not in zeile + block)
    bl[r1[0]] = bl[r1[0]][:-2] + zeile + ' |'; open(BLp, 'w', encoding='utf-8').write('\n'.join(bl))
    jl2 = jl.replace('\n## Wiederkehrende Lehren\n', '\n' + block + '## Wiederkehrende Lehren\n'); open(JLp, 'w', encoding='utf-8').write(jl2)
    p('BACKLOG: Zeile genau einmal, Rang 1 endet mit " |"', open(BLp, encoding='utf-8').read().count(zeile) == 1 and open(BLp, encoding='utf-8').read().split('\n')[r1[0]].endswith(zeile + ' |'))
    p('BACKLOG: Zeilenzahl gleich', len(open(BLp, encoding='utf-8').read().split('\n')) == len(bl))
    p('Journal: Block %s genau einmal, vor Wiederkehrende Lehren' % neu, jl2.count('## ' + neu + ' \u2014 TB-177') == 1 and jl2.index('## ' + neu + ' \u2014 TB-177') < jl2.index('\n## Wiederkehrende Lehren\n'))
    p('Journal: alter Inhalt unveraendert (nur eingefuegt)', jl2.replace(block, '', 1) == jl)
print('Kennung ' + neu); print('Pruefungen: %d, NEIN: %d' % (n, nein)); raise SystemExit(1 if nein else 0)
PYEOF
} > docs/belege/TB-177/a_backlog_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-177/a_backlog_journal.txt
```

Dann `git add` mit Namen für `docs/ERGEBNIS_TB-177_ki_forschung_ba1.md`, `docs/projektfuehrung/BACKLOG.md`, `docs/projektfuehrung/JOURNAL.md`, `docs/belege/TB-177/a_backlog_journal.txt`; Commit `TB-177 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩` (Kennung aus `a_backlog_journal.txt`), pushen.

**F.**

```
git status --porcelain > "$TMPDIR/tb177_f.txt"
cp "$TMPDIR/tb177_f.txt" docs/belege/TB-177/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-177/f_numstat.txt
git add docs/belege/TB-177/f_porcelain.txt
git add docs/belege/TB-177/f_numstat.txt
git commit -q -m "TB-177 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; `f_numstat.txt` nennt neben `docs/` genau die vier Dateien unter `ki_forschung/`; kein Pfad unter `strategies/`, `shared/`, `notifications/`, `data/`, `config/`, `research/`.

## Offene Entscheide (nicht in diesem Auftrag entschieden)

- **E1 Preis:** Haiku 1 $ / 5 $ je Million Token steht als Konstante in `aufrufe.py` (Preisliste, nicht im Repo gemessen); Betreiber bestätigt vor dem Erstlauf (BA7). Ist das Modell nicht in der Tabelle, wird nicht aufgerufen.
- **E2 Notschalter-Namen:** `ki_sammler`, `ki_bots` in `config/agenten_aus.txt`; BA1 ändert die Datei nicht.
- **E3 Höchstpreis:** Eingabe-Bytes als Token-Obergrenze plus `FORMAT_ZUSCHLAG_TOKEN` = 500 für den Formatierungs-Overhead der API (gewählt, nicht gemessen; BA7 misst `usage.input_tokens` gegen Bytes); die Reservierung wird nach dem Aufruf auf den echten Preis abgerechnet. Wirft die Buchung der Abrechnung, bleibt die Reservierung: zu viel gebucht, nie zu wenig. Die Abrechnung mit dem echten Preis kann den Deckel um den Fehler der Schätzung eines einzigen Aufrufs überschreiten (bewusst; BA7 misst).
- **E4 Monatsgrenze:** UTC-Monat, nicht Berlin.
- **E5 Laufbereich:** `ki_forschung/` bleibt bewusst ausserhalb von `ARBEITSBAUM_PFADE` (shared/paths.py Z. 239); Sauberkeitsprüfungen der neun sehen es nicht.
- **E7 R108 (b)** (BACKLOG Rang 1, TB-176a): Sammler-Ergänzungen, Leseregel nach 24.3, Auswerteplan vor der ersten Auswertung betreffen BA2/BA3, nicht BA1.
- **E6 Kollisionen aus PLAN_KIBOTS** (MI1 (b)/K24, R107 (d), 16.8/16.9) betreffen BA4 (Bots), nicht BA1; hier nicht berührt.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V nicht `rc 0`; B-sha256 weicht ab; T nicht wie Soll (dann Abbruchweg T, kein B-Commit); `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung.

## In einfacher Sprache

Für die geplanten KI-Versuche entsteht ein eigener Ordner neben den neun Bots. Er kann später Daten aus dem Netz abholen und so einfrieren, dass man nachträglich weiss, was an welchem Tag bekannt war, und er führt Buch über jede Anfrage an das KI-Modell. Bevor eine Anfrage rausgeht, rechnet er, ob sie den Monatsdeckel von 3 $ (getrennt für Sammler und KI-Bots) überschreiten könnte, und lässt sie dann weg. Heute wird nichts abgerufen und nichts bezahlt: ein Selbsttest prüft mit Attrappen, dass der Ordner die neun Bots nicht berührt, keinen Schlüssel liest und die Bremse greift — und dass der Test an absichtlich verfälschten Kopien rot wird.

## Anhänge


### Anhang A — `ki_forschung/pfade.py` (neu)

<!-- DATEI pfade.py -->
````python
"""Pfade der KI-Forschung (TB-177, BA1).

Der Ordner liegt auf oberster Ebene neben broker/ und dashboard/:
ausserhalb von strategies/ (discover_bots in notifications/monitor.py sieht
ihn nie) und ausserhalb des Laufbereichs (shared/paths.py,
ARBEITSBAUM_PFADE). Geschrieben wird nur in die zwei Datenbanken hier.
"""
import os

KI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(KI_DIR)
SHARED_DIR = os.path.join(REPO_DIR, "shared")
ABRUFE_DB = os.path.join(KI_DIR, "abrufe.db")
AUFRUFE_DB = os.path.join(KI_DIR, "aufrufe.db")
````

### Anhang B — `ki_forschung/abrufe.py` (neu)

<!-- DATEI abrufe.py -->
````python
"""Abruf- und Einfrierschicht der KI-Forschung (TB-177, BA1).

Jeder Abruf wird als Rohkopie mit sha256 und Abrufzeit (UTC) in abrufe.db
eingefroren. Die Abrufzeit ist der Vintage-Stempel und wird nur hier intern
gesetzt (kein Parameter des Aufrufers, keine Rueckdatierung); Format fest
JJJJ-MM-TTThh:mm:ss.ffffffZ (CHECK in der Tabelle). Ein spaeterer Prompt
liest nur, was zu seiner Zeit schon eingefroren war (stand()).
Die Tabelle ist nur anfuegend: UPDATE, DELETE und ein INSERT mit schon
vorhandener id (INSERT OR REPLACE, REPLACE) bricht SQLite per Trigger ab;
dazu recursive_triggers je Verbindung. Ein fehlgeschlagener Abruf wird als
Zeile 'ausgefallen' gebucht, nicht nachgeholt. Keine Websuche, kein
Modellaufruf hier.
"""
import datetime
import hashlib
import os
import re
import sqlite3
import sys
import urllib.request

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)
import pfade  # noqa: E402

QUELLEN = ("alfred", "fear_greed", "yfinance", "binance_spot", "rss")
ZEITFORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

SCHEMA = """
CREATE TABLE IF NOT EXISTS abrufe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quelle TEXT NOT NULL,
    schluessel TEXT NOT NULL,
    abgerufen_utc TEXT NOT NULL CHECK (abgerufen_utc GLOB
        '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]Z'),
    url TEXT,
    format TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ok', 'ausgefallen')),
    bytes INTEGER NOT NULL,
    sha256 TEXT NOT NULL,
    roh BLOB NOT NULL,
    fehler TEXT
);
CREATE INDEX IF NOT EXISTS abrufe_stand ON abrufe (quelle, schluessel, abgerufen_utc);
CREATE TRIGGER IF NOT EXISTS abrufe_kein_update BEFORE UPDATE ON abrufe
BEGIN SELECT RAISE(ABORT, 'abrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS abrufe_kein_delete BEFORE DELETE ON abrufe
BEGIN SELECT RAISE(ABORT, 'abrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS abrufe_kein_ersetzen BEFORE INSERT ON abrufe
WHEN NEW.id IS NOT NULL AND EXISTS (SELECT 1 FROM abrufe WHERE id = NEW.id)
BEGIN SELECT RAISE(ABORT, 'abrufe.db ist nur anfuegend (id schon vorhanden)'); END;
"""

_ZEIT_RX = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:[.,](\d{1,6}))?(Z|[+-]\d{2}:\d{2})$")


class EinfrierFehler(Exception):
    """Eine eingefrorene Rohkopie passt nicht mehr zu ihrem sha256."""


def jetzt_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime(ZEITFORMAT)


def zeitpunkt(wert):
    """Ein Zeitpunkt mit Zeitzone (datetime oder ISO-Text mit 'Z' oder '+hh:mm',
    Bruchteile bis 6 Stellen, Punkt oder Komma) als UTC-Text im festen Format
    der Tabelle. Ohne Zeitzone: ValueError. Im festen Format (gleiche Breite,
    UTC) ist der Textvergleich in SQLite ein Zeitvergleich."""
    if isinstance(wert, datetime.datetime):
        d = wert
    else:
        m = _ZEIT_RX.match(str(wert).strip())
        if not m:
            raise ValueError("kein Zeitpunkt mit Zeitzone: %r" % (wert,))
        j, mo, t, h, mi, s, bruch, zone = m.groups()
        if zone == "Z":
            tz = datetime.timezone.utc
        else:
            vz = 1 if zone[0] == "+" else -1
            tz = datetime.timezone(vz * datetime.timedelta(hours=int(zone[1:3]), minutes=int(zone[4:6])))
        d = datetime.datetime(int(j), int(mo), int(t), int(h), int(mi), int(s), int((bruch or "0").ljust(6, "0")), tzinfo=tz)
    if d.tzinfo is None or d.utcoffset() is None:
        raise ValueError("Zeitpunkt ohne Zeitzone: %r" % (wert,))
    return d.astimezone(datetime.timezone.utc).strftime(ZEITFORMAT)


def verbinden(db=None):
    conn = sqlite3.connect(db or pfade.ABRUFE_DB)
    conn.execute("PRAGMA recursive_triggers = ON")
    conn.executescript(SCHEMA)
    return conn


def _quelle_pruefen(quelle):
    if quelle not in QUELLEN:
        raise ValueError("unbekannte Quelle %r (erlaubt: %s)" % (quelle, ", ".join(QUELLEN)))


def _einfrieren(quelle, schluessel, roh, format, url, zeit, db):
    _quelle_pruefen(quelle)
    if not isinstance(roh, bytes):
        raise TypeError("roh muss bytes sein")
    sha = hashlib.sha256(roh).hexdigest()
    conn = verbinden(db)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO abrufe (quelle, schluessel, abgerufen_utc, url, format, status, bytes, sha256, roh)"
                " VALUES (?, ?, ?, ?, ?, 'ok', ?, ?, ?)",
                (quelle, schluessel, zeit, url, format, len(roh), sha, sqlite3.Binary(roh)))
        return {"id": cur.lastrowid, "sha256": sha, "abgerufen_utc": zeit, "status": "ok"}
    finally:
        conn.close()


def _ausfall(quelle, schluessel, fehler, format, url, zeit, db):
    _quelle_pruefen(quelle)
    conn = verbinden(db)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO abrufe (quelle, schluessel, abgerufen_utc, url, format, status, bytes, sha256, roh, fehler)"
                " VALUES (?, ?, ?, ?, ?, 'ausgefallen', 0, ?, ?, ?)",
                (quelle, schluessel, zeit, url, format, hashlib.sha256(b"").hexdigest(),
                 sqlite3.Binary(b""), str(fehler)[:500]))
        return {"id": cur.lastrowid, "abgerufen_utc": zeit, "status": "ausgefallen"}
    finally:
        conn.close()


def einfrieren(quelle, schluessel, roh, format, url=None, db=None):
    """Friert eine Rohkopie ein (Abrufzeit = jetzt, intern) und gibt id, sha256 und Abrufzeit zurueck."""
    return _einfrieren(quelle, schluessel, roh, format, url, jetzt_utc(), db)


def ausfall(quelle, schluessel, fehler, format, url=None, db=None):
    """Bucht einen fehlgeschlagenen Abruf (Ausfalltag, Zeit = jetzt); er wird nicht nachgeholt."""
    return _ausfall(quelle, schluessel, fehler, format, url, jetzt_utc(), db)


def _http_holen(url):
    anfrage = urllib.request.Request(url, headers={"User-Agent": "trading-bot-ki-forschung/1"})
    with urllib.request.urlopen(anfrage, timeout=30) as antwort:
        return antwort.read()


def abrufen(quelle, schluessel, url, format, holer=None, db=None):
    """Holt url (oder ruft die Attrappe holer(url) auf) und friert das Ergebnis ein.
    Abrufzeit = Beginn des Abrufs (intern). Ein Fehler wird als Ausfall gebucht, nicht geworfen."""
    _quelle_pruefen(quelle)
    zeit = jetzt_utc()
    try:
        roh = (holer or _http_holen)(url)
    except Exception as e:  # Ausfall statt Absturz
        return _ausfall(quelle, schluessel, e, format, url, zeit, db)
    return _einfrieren(quelle, schluessel, roh, format, url, zeit, db)


def stand(quelle, schluessel, bis, db=None):
    """Die juengste gueltige Rohkopie mit abgerufen_utc <= bis (Vintage), sha256
    nachgerechnet. bis ist ein Zeitpunkt mit Zeitzone (siehe zeitpunkt()).
    None, wenn es keine gibt."""
    grenze = zeitpunkt(bis)
    conn = verbinden(db)
    try:
        z = conn.execute(
            "SELECT id, abgerufen_utc, format, sha256, roh FROM abrufe WHERE quelle = ? AND schluessel = ?"
            " AND status = 'ok' AND abgerufen_utc <= ? ORDER BY abgerufen_utc DESC, id DESC LIMIT 1",
            (quelle, schluessel, grenze)).fetchone()
    finally:
        conn.close()
    if z is None:
        return None
    roh = bytes(z[4])
    if hashlib.sha256(roh).hexdigest() != z[3]:
        raise EinfrierFehler("Abruf %d: sha256 passt nicht zur Rohkopie" % z[0])
    return {"id": z[0], "abgerufen_utc": z[1], "format": z[2], "sha256": z[3], "roh": roh}
````

### Anhang C — `ki_forschung/aufrufe.py` (neu)

<!-- DATEI aufrufe.py -->
````python
"""Aufrufbuch und Kostenbremse der KI-Forschung (TB-177, BA1).

Jeder Modellaufruf geht ueber aufrufen(). Vor dem Aufruf rechnet die Bremse
die Monatssumme des Deckel-Topfs (UTC-Monat) plus den hoechstmoeglichen
Preis dieses Aufrufs; wuerde das den Deckel ueberschreiten, wird NICHT
aufgerufen (Zeile 'gebremst'). Sonst wird der Hoechstpreis als Zeile
'reserviert' gebucht, dann aufgerufen, dann eine Zeile 'abgerechnet' mit dem
echten Preis aus usage; sie ersetzt in der Monatssumme die Reservierung.
max_tokens muss eine ganze Zahl >= 1 sein, alle Betraege sind >= 0 (Pruefung
im Code und CHECK in der Tabelle). Stuerzt der Lauf dazwischen ab, bleibt
die Reservierung stehen: die Bremse rechnet zu viel, nie zu wenig.
Pruefung und Reservierung laufen in einer Transaktion (BEGIN IMMEDIATE).
Die Tabelle ist nur anfuegend: UPDATE, DELETE und ein INSERT mit schon
vorhandener id (INSERT OR REPLACE) bricht ein Trigger ab; dazu
recursive_triggers je Verbindung. Die Buchungszeit (und damit der Monat)
wird nur intern gesetzt, kein Parameter des Aufrufers.

Zwei Toepfe, getrennt gebucht (Betreiberentscheid 17.10.2026): 'sammler'
und 'bots' (die KI-Bots), je 3 $ im Monat. Nur Haiku, keine Werkzeuge (keine
Websuche). shared/claude_client.py wird nur importiert, nicht geaendert;
Schluessel ANTHROPIC_API_KEY liest claude_client selbst (Umgebung oder
config/email_config.py), dieses Modul liest keinen Schluessel.
Notschalter: steht 'ki_<topf>' in config/agenten_aus.txt, wird nicht
aufgerufen (Zeile 'abgeschaltet').
"""
import datetime
import hashlib
import os
import sqlite3
import sys

_HIER = os.path.dirname(os.path.abspath(__file__))
if _HIER not in sys.path:
    sys.path.insert(0, _HIER)
import pfade  # noqa: E402
if pfade.SHARED_DIR not in sys.path:
    sys.path.append(pfade.SHARED_DIR)  # nur fuer den Import von claude_client

DECKEL_USD = {"sammler": 3.0, "bots": 3.0}
# Preis je Million Token (USD) fuer das eine erlaubte Modell. Aus der
# Preisliste des Anbieters, nicht im Repo gemessen; der Betreiber bestaetigt
# ihn vor dem Erstlauf (BA7). Steht hier ein Modell nicht, wird nicht aufgerufen.
PREIS_JE_MTOK = {"claude-haiku-4-5-20251001": {"ein": 1.0, "aus": 5.0}}

SCHEMA = """
CREATE TABLE IF NOT EXISTS aufrufe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zeit_utc TEXT NOT NULL,
    monat TEXT NOT NULL,
    topf TEXT NOT NULL,
    verbraucher TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('reserviert', 'abgerechnet', 'gebremst', 'abgeschaltet', 'abgelehnt')),
    bezug INTEGER,
    modell_angefordert TEXT NOT NULL,
    modell_geliefert TEXT,
    prompt_hash TEXT NOT NULL,
    eingabe_hash TEXT,
    katalogversion TEXT,
    max_tokens INTEGER NOT NULL CHECK (typeof(max_tokens) = 'integer' AND max_tokens >= 1),
    tokens_ein INTEGER CHECK (tokens_ein IS NULL OR tokens_ein >= 0),
    tokens_aus INTEGER CHECK (tokens_aus IS NULL OR tokens_aus >= 0),
    kosten_usd REAL NOT NULL CHECK (kosten_usd >= 0),
    summe_vorher_usd REAL,
    deckel_usd REAL,
    erfolg INTEGER,
    fehler TEXT
);
CREATE INDEX IF NOT EXISTS aufrufe_monat ON aufrufe (topf, monat);
CREATE TRIGGER IF NOT EXISTS aufrufe_kein_update BEFORE UPDATE ON aufrufe
BEGIN SELECT RAISE(ABORT, 'aufrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS aufrufe_kein_delete BEFORE DELETE ON aufrufe
BEGIN SELECT RAISE(ABORT, 'aufrufe.db ist nur anfuegend'); END;
CREATE TRIGGER IF NOT EXISTS aufrufe_kein_ersetzen BEFORE INSERT ON aufrufe
WHEN NEW.id IS NOT NULL AND EXISTS (SELECT 1 FROM aufrufe WHERE id = NEW.id)
BEGIN SELECT RAISE(ABORT, 'aufrufe.db ist nur anfuegend (id schon vorhanden)'); END;
"""


def _jetzt():
    return datetime.datetime.now(datetime.timezone.utc)


def verbinden(db=None):
    conn = sqlite3.connect(db or pfade.AUFRUFE_DB, isolation_level=None, timeout=30)
    conn.execute("PRAGMA recursive_triggers = ON")
    conn.executescript(SCHEMA)
    return conn


def prompt_hash(system_prompt, user_message):
    return hashlib.sha256(("%s\x00%s" % (system_prompt, user_message)).encode("utf-8")).hexdigest()


# Zuschlag fuer den Formatierungs-Overhead der API (Rollen, Nachrichtenrahmen,
# Systemteil), der nicht in den Bytes von Prompt und Nachricht steckt.
# Gewaehlt, nicht gemessen (Gegenleser GEGEN177 F1); BA7 misst ihn am Erstlauf
# (usage.input_tokens gegen Bytes) und bestaetigt ihn.
FORMAT_ZUSCHLAG_TOKEN = 500


def _ganz(wert):
    """True fuer eine ganze Zahl (int, nicht bool)."""
    return isinstance(wert, int) and not isinstance(wert, bool)


def eingabe_pruefen(system_prompt, user_message, max_tokens):
    """Vor jeder Buchung: Texte sind str, max_tokens ganze Zahl >= 1. Sonst ValueError."""
    if not isinstance(system_prompt, str) or not isinstance(user_message, str):
        raise ValueError("system_prompt und user_message muessen Text (str) sein")
    if not _ganz(max_tokens) or max_tokens < 1:
        raise ValueError("max_tokens muss eine ganze Zahl >= 1 sein, nicht %r" % (max_tokens,))


def hoechstpreis(modell, system_prompt, user_message, max_tokens):
    """Obergrenze des Preises vor dem Aufruf: Eingabe-Token hoechstens so viele
    wie Bytes (jedes Token deckt mindestens ein Byte) plus FORMAT_ZUSCHLAG_TOKEN
    fuer den Formatierungs-Overhead, Ausgabe hoechstens max_tokens. Nie negativ."""
    eingabe_pruefen(system_prompt, user_message, max_tokens)
    p = PREIS_JE_MTOK[modell]
    ein = len(system_prompt.encode("utf-8")) + len(user_message.encode("utf-8")) + FORMAT_ZUSCHLAG_TOKEN
    reserve = (ein * p["ein"] + max_tokens * p["aus"]) / 1e6
    if not (0 <= reserve < float("inf")):
        raise ValueError("Reserve %r nicht im Bereich [0, inf)" % (reserve,))
    return reserve


def preis(modell, tokens_ein, tokens_aus):
    """Echter Preis aus usage; Token muessen ganze Zahlen >= 0 sein, sonst ValueError."""
    if not (_ganz(tokens_ein) and _ganz(tokens_aus) and tokens_ein >= 0 and tokens_aus >= 0):
        raise ValueError("Token muessen ganze Zahlen >= 0 sein: %r, %r" % (tokens_ein, tokens_aus))
    p = PREIS_JE_MTOK[modell]
    return (tokens_ein * p["ein"] + tokens_aus * p["aus"]) / 1e6


def monatssumme(topf, monat, db=None, conn=None):
    eigene = conn is None
    conn = conn or verbinden(db)
    try:
        # Je Aufruf zaehlt die Abrechnung (echter Preis), solange keine da ist die
        # Reservierung (Hoechstpreis). Alle Betraege >= 0 (CHECK).
        s = conn.execute("SELECT COALESCE(SUM(kosten_usd), 0) FROM aufrufe a WHERE topf = ? AND monat = ?"
                         " AND (status = 'abgerechnet' OR (status = 'reserviert' AND NOT EXISTS"
                         " (SELECT 1 FROM aufrufe b WHERE b.status = 'abgerechnet' AND b.bezug = a.id)))",
                         (topf, monat)).fetchone()[0]
        return float(s)
    finally:
        if eigene:
            conn.close()


def _zeile(conn, **w):
    spalten = sorted(w)
    cur = conn.execute("INSERT INTO aufrufe (%s) VALUES (%s)" % (", ".join(spalten), ", ".join("?" * len(spalten))),
                       [w[k] for k in spalten])
    return cur.lastrowid


def aufrufen(topf, verbraucher, system_prompt, user_message, max_tokens=600, eingabe_hash=None,
             katalogversion=None, db=None, aufruf=None, schalter=None):
    """Ein Modellaufruf unter der Bremse. aufruf: Attrappe fuer Tests
    (Signatur wie claude_client.call_claude); ohne sie der echte Aufruf.
    Gibt {'success', 'text', 'gebremst', 'id', ...} zurueck. Gebremst,
    abgeschaltet und ein fehlgeschlagener Modellaufruf werfen nicht.
    Es wirft: ValueError bei unbekanntem Topf (nichts gebucht); ein
    Datenbankfehler vor der Reservierung (z. B. Zeitueberschreitung bei
    BEGIN IMMEDIATE; nichts gebucht, kein Aufruf); ein Datenbankfehler beim
    Buchen der Abrechnung nach dem Aufruf - dann bleibt die Reservierung
    (Hoechstpreis) stehen: zu viel gebucht, nie zu wenig."""
    import claude_client  # shared/, nur importiert
    if topf not in DECKEL_USD:
        raise ValueError("unbekannter Topf %r" % topf)
    eingabe_pruefen(system_prompt, user_message, max_tokens)
    modell = claude_client.MODEL_HAIKU
    zeit = _jetzt()
    zeit_s, monat = zeit.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), zeit.strftime("%Y-%m")
    ph = prompt_hash(system_prompt, user_message)
    basis = dict(zeit_utc=zeit_s, monat=monat, topf=topf, verbraucher=verbraucher, modell_angefordert=modell,
                 prompt_hash=ph, eingabe_hash=eingabe_hash, katalogversion=katalogversion, max_tokens=int(max_tokens),
                 deckel_usd=DECKEL_USD[topf])
    conn = verbinden(db)
    try:
        if modell not in PREIS_JE_MTOK:
            _zeile(conn, status="abgelehnt", kosten_usd=0.0, fehler="kein Preis fuer %s" % modell, **basis)
            return {"success": False, "gebremst": True, "error": "kein Preis fuer Modell %s" % modell}
        if claude_client.agent_abgeschaltet("ki_" + topf, schalter):
            _zeile(conn, status="abgeschaltet", kosten_usd=0.0, **basis)
            return {"success": False, "gebremst": True, "error": "ki_%s abgeschaltet" % topf}
        reserve = hoechstpreis(modell, system_prompt, user_message, max_tokens)
        conn.execute("BEGIN IMMEDIATE")
        try:
            summe = monatssumme(topf, monat, conn=conn)
            if summe + reserve > DECKEL_USD[topf]:
                rid = _zeile(conn, status="gebremst", kosten_usd=0.0, summe_vorher_usd=summe,
                             fehler="Deckel: %.6f + %.6f > %.2f" % (summe, reserve, DECKEL_USD[topf]), **basis)
                conn.execute("COMMIT")
                return {"success": False, "gebremst": True, "id": rid,
                        "error": "Monatsdeckel %s erreicht (%.4f + %.4f > %.2f $)" % (topf, summe, reserve, DECKEL_USD[topf])}
            rid = _zeile(conn, status="reserviert", kosten_usd=reserve, summe_vorher_usd=summe, **basis)
            conn.execute("COMMIT")
        except Exception:
            conn.execute("ROLLBACK")
            raise
        erg = (aufruf or claude_client.call_claude)(system_prompt, user_message, max_tokens=int(max_tokens),
                                                      tools=None, model=modell)
        raw = erg.get("raw")
        usage = getattr(raw, "usage", None)
        t_ein = getattr(usage, "input_tokens", None)
        t_aus = getattr(usage, "output_tokens", None)
        geliefert = getattr(raw, "model", None)
        try:
            kosten = preis(modell, t_ein, t_aus) if erg.get("success") else reserve
        except ValueError:
            kosten = reserve  # usage fehlt oder unbrauchbar: Hoechstpreis (zu viel, nie zu wenig)
        _zeile(conn, status="abgerechnet", bezug=rid, kosten_usd=kosten, modell_geliefert=geliefert,
               tokens_ein=t_ein, tokens_aus=t_aus, erfolg=1 if erg.get("success") else 0,
               fehler=None if erg.get("success") else str(erg.get("error"))[:500],
               **dict(basis, zeit_utc=_jetzt().strftime("%Y-%m-%dT%H:%M:%S.%fZ")))
        return {"success": bool(erg.get("success")), "gebremst": False, "id": rid, "text": erg.get("text", ""),
                "error": erg.get("error"), "modell_geliefert": geliefert, "tokens_ein": t_ein, "tokens_aus": t_aus}
    finally:
        conn.close()
````

### Anhang D — `ki_forschung/test_ki_wachen.py` (neu)

<!-- DATEI test_ki_wachen.py -->
````python
"""
Wachen-Test der KI-Forschung (TB-177, BA1)
==========================================
Prueft die Trennung von den neun Bots und die Kostenbremse, ohne Netz und
ohne API-Aufruf: anthropic wird als Platzhalter angelegt, der beim Erzeugen
eines Clients wirft; jeder Modellaufruf geht an eine Attrappe.

W1  Importe: jedes Modul in ki_forschung/ importiert nur aus der Positivliste
    (Standardbibliothek-Auswahl, die eigenen Module, claude_client) - kein
    strategies/, manual_close, zuteilung, messkette, broker, monitor.
W2  Schreibziele: kein Modul nennt paper_trading, strategies, notifications,
    results, data/, .log oder .env; sqlite3.connect nur in verbinden() auf
    pfade.ABRUFE_DB/AUFRUFE_DB (oder die uebergebene Test-DB); kein open(),
    os.open, io.open, getattr(..., 'open') oder getattr mit Namen aus einer
    Variablen; beide DBs liegen in ki_forschung/. Laufzeit: ein Rekorder
    faengt sqlite3.connect, builtins.open, io.open, os.open, os.fdopen und
    urlopen ab - jedes Schreiben muss im temporaeren Ordner landen, kein Netz;
    dazu die Code-Dateien unter shared/, strategies/, notifications/ (darunter
    die Sperrliste shared/messkette.py, shared/zuteilung.py,
    strategies/*/equity_simulation.py ...) vorher = nachher (Groesse, mtime,
    sha256). Die Bot-DBs paper_trading_*.db werden NICHT gehasht (ein
    Cron-Lauf der neun darf sie waehrend des Tests aendern); fuer sie gilt
    der Rekorder (kein connect ausserhalb des temporaeren Ordners).
W3  Erkennung: ki_forschung liegt nicht unter strategies/, kein Eintrag in
    ASSET_CLASS/DISPLAY_NAMES (monitor.py), kein Pfad des Laufbereichs
    (shared/paths.py ARBEITSBAUM_PFADE) beginnt mit ki_forschung, und kein
    Modul unter shared/, strategies/, notifications/ nennt ki_forschung.
W4  Bremse: stoppt vor der Ueberschreitung (Attrappe nie gerufen), Toepfe
    getrennt, Monatswechsel, Notschalter, Fehlerpfad, nur anfuegend,
    Modell Haiku und tools=None.
W5  Schluessel: kein Modul liest os.environ, .env oder email_config; keine
    Websuche (kein 'web_search', kein tools=...).
W6  Abrufe: Einfrieren mit sha256, Vintage-Stand, Ausfall statt Absturz,
    nur anfuegend (auch gegen INSERT OR REPLACE, beide DBs), unbekannte
    Quelle abgelehnt, Zeitgrenze als Zeitpunkt ('Z', '+hh:mm', Bruchteile),
    Abrufzeit und Buchungszeit nicht vom Aufrufer setzbar.
G   Gegenproben: jede statische Wache (W1, W2, W3, W5), der Rekorder, die
    Bremse (W4), der Ersetzungsschutz und die Zeitgrenze (W6) werden an einer
    verfaelschten Kopie in einem temporaeren Ordner rot.

Nutzung:  python3 -B ki_forschung/test_ki_wachen.py      (Ausgang 0 = gruen)
Schreibt nur in temporaere Ordner (tempfile); das Repo wird nur gelesen.
"""
import ast
import datetime
import hashlib
import os
import shutil
import sqlite3
import sys
import tempfile
import types

KI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(KI_DIR)
ERGEBNIS = []
TEMP = []


def temp(prefix):
    d = tempfile.mkdtemp(prefix=prefix)
    TEMP.append(d)
    return d

ERLAUBTE_IMPORTE = {"ast", "builtins", "datetime", "io", "re", "hashlib", "os", "shutil", "sqlite3", "sys", "tempfile", "types",
                    "urllib", "urllib.request", "pfade", "abrufe", "aufrufe", "claude_client"}
VERBOTENE_WORTE = ("paper_trading", "strategies", "notifications", "results", "data/", ".log", ".env",
                   "email_config", "web_search", "environ", "manual_close", "zuteilung", "messkette")


GEFAEHRLICH = ("open", "fdopen", "popen", "system", "spawnv", "execv", "__import__", "write_text", "write_bytes")


def pruefe(name, ok, detail=""):
    ERGEBNIS.append((name, bool(ok)))
    print("  %s %s%s" % ("ok  " if ok else "FEHLT", name, ("   " + str(detail)[:300]) if detail else ""))


def module(ki_dir):
    return sorted(f for f in os.listdir(ki_dir) if f.endswith(".py") and not f.startswith("test_"))


def befunde_w1(ki_dir):
    """Importe ausserhalb der Positivliste (gilt auch fuer den Test selbst)."""
    b = []
    for f in sorted(x for x in os.listdir(ki_dir) if x.endswith(".py")):
        baum = ast.parse(open(os.path.join(ki_dir, f), encoding="utf-8").read())
        for k in ast.walk(baum):
            namen = []
            if isinstance(k, ast.Import):
                namen = [a.name for a in k.names]
            elif isinstance(k, ast.ImportFrom):
                namen = [(k.module or "")] if k.level == 0 else ["." + (k.module or "")]
            elif isinstance(k, ast.Call) and getattr(k.func, "id", getattr(k.func, "attr", "")) in ("__import__", "import_module"):
                namen = ["dynamischer Import"]
            b += ["%s:%d %s" % (f, k.lineno, n) for n in namen if n not in ERLAUBTE_IMPORTE]
    return b


def _doc_ids(baum):
    return {id(n.body[0].value) for n in ast.walk(baum) if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef))
            and n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}


def _strings(baum):
    """Zeichenketten ohne Docstrings."""
    d = _doc_ids(baum)
    return [(k.lineno, k.value) for k in ast.walk(baum) if isinstance(k, ast.Constant) and isinstance(k.value, str) and id(k) not in d]


def befunde_w2(ki_dir):
    """Schreibziele: verbotene Worte in Zeichenketten und Namen, connect/open ausserhalb der Regel."""
    b = []
    for f in module(ki_dir):
        quelle = open(os.path.join(ki_dir, f), encoding="utf-8").read()
        baum = ast.parse(quelle)
        docs = _doc_ids(baum)
        for k in ast.walk(baum):
            if isinstance(k, ast.Constant) and isinstance(k.value, str) and id(k) not in docs:
                b += ["%s:%d nennt %r" % (f, k.lineno, w) for w in VERBOTENE_WORTE if w in k.value]
            if isinstance(k, ast.Attribute) and k.attr in GEFAEHRLICH:
                b.append("%s:%d .%s" % (f, k.lineno, k.attr))
            if isinstance(k, (ast.Name, ast.Attribute)):
                n = k.id if isinstance(k, ast.Name) else k.attr
                b += ["%s:%d Name %s" % (f, k.lineno, n) for w in ("environ", "manual_close", "zuteilung", "messkette") if n == w]
        in_verbinden = {id(k) for fn in ast.walk(baum) if isinstance(fn, ast.FunctionDef) and fn.name == "verbinden" for k in ast.walk(fn)}
        for fn in [baum]:
            for k in ast.walk(fn):
                if not isinstance(k, ast.Call):
                    continue
                name = getattr(k.func, "attr", getattr(k.func, "id", ""))
                if name == "connect" and id(k) not in in_verbinden:
                    b.append("%s:%d sqlite3.connect ausserhalb verbinden()" % (f, k.lineno))
                if name == "open" and isinstance(k.func, ast.Name):
                    b.append("%s:%d open()" % (f, k.lineno))
                if name == "getattr" and isinstance(k.func, ast.Name):
                    if len(k.args) < 2 or not isinstance(k.args[1], ast.Constant):
                        b.append("%s:%d getattr mit Namen aus einer Variablen" % (f, k.lineno))
                    elif k.args[1].value in GEFAEHRLICH:
                        b.append("%s:%d getattr(..., %r)" % (f, k.lineno, k.args[1].value))
                if name in ("write_text", "write_bytes", "makedirs", "mkdir", "remove", "unlink", "rename", "replace", "rmtree", "copy", "copyfile", "move") \
                        and not (name == "replace" and isinstance(k.func, ast.Attribute) and isinstance(k.func.value, ast.Constant)):
                    b.append("%s:%d %s()" % (f, k.lineno, name))
                if name == "connect" and id(k) in in_verbinden:
                    arg = ast.dump(k.args[0]) if k.args else ""
                    if not ("ABRUFE_DB" in arg or "AUFRUFE_DB" in arg):
                        b.append("%s:%d connect ohne pfade.*_DB" % (f, k.lineno))
    return b


def _arbeitsbaum_pfade(wurzel):
    baum = ast.parse(open(os.path.join(wurzel, "shared", "paths.py"), encoding="utf-8").read())
    werte = {}
    for k in baum.body:
        if isinstance(k, ast.Assign) and len(k.targets) == 1 and isinstance(k.targets[0], ast.Name):
            werte[k.targets[0].id] = k.value
    tup = werte.get("ARBEITSBAUM_PFADE")
    if not isinstance(tup, ast.Tuple):
        return None
    aus = []
    for e in tup.elts:
        if isinstance(e, ast.Constant):
            aus.append(e.value)
        elif isinstance(e, ast.Name) and isinstance(werte.get(e.id), ast.Constant):
            aus.append(werte[e.id].value)
    return aus


def befunde_w3(wurzel, ki_dir):
    b = []
    rel = os.path.relpath(ki_dir, wurzel).replace(os.sep, "/")
    if rel.split("/")[0] == "strategies":
        b.append("ki_forschung liegt unter strategies/")
    lb = _arbeitsbaum_pfade(wurzel)
    if lb is None:
        b.append("ARBEITSBAUM_PFADE nicht lesbar")
    else:
        b += ["Laufbereich enthaelt %s" % p for p in lb if p.split("/")[0] == rel.split("/")[0]]
    mon = ast.parse(open(os.path.join(wurzel, "notifications", "monitor.py"), encoding="utf-8").read())
    for k in mon.body:
        if isinstance(k, ast.Assign) and getattr(k.targets[0], "id", "") in ("ASSET_CLASS", "DISPLAY_NAMES") and isinstance(k.value, ast.Dict):
            b += ["%s nennt %s" % (k.targets[0].id, s.value) for s in k.value.keys
                  if isinstance(s, ast.Constant) and ("ki" in str(s.value).split("_") or str(s.value).startswith("ki"))]
    for ordner in ("shared", "strategies", "notifications"):
        for d, _u, fs in os.walk(os.path.join(wurzel, ordner)):
            for f in fs:
                if f.endswith(".py"):
                    p = os.path.join(d, f)
                    if "ki_forschung" in open(p, encoding="utf-8", errors="replace").read():
                        b.append("%s nennt ki_forschung" % os.path.relpath(p, wurzel))
    return b


def befunde_w5(ki_dir):
    b = []
    for f in module(ki_dir):
        baum = ast.parse(open(os.path.join(ki_dir, f), encoding="utf-8").read())
        for k in ast.walk(baum):
            if isinstance(k, ast.Attribute) and k.attr in ("environ", "getenv"):
                b.append("%s:%d os.%s" % (f, k.lineno, k.attr))
            if isinstance(k, ast.keyword) and k.arg == "tools" and not (isinstance(k.value, ast.Constant) and k.value.value is None):
                b.append("%s:%d tools= nicht None" % (f, k.lineno))
        b += ["%s:%d nennt %r" % (f, z, w) for z, s in _strings(baum) for w in (".env", "email_config", "web_search", "API_KEY") if w in s]
    return b


# --- Laufzeit: Platzhalter und Attrappen ---------------------------------------
STUB = temp("tb177_stub_")
with open(os.path.join(STUB, "anthropic.py"), "w") as _f:
    _f.write("class Anthropic:\n    def __init__(self, *a, **k):\n        raise RuntimeError('Test darf die API nicht aufrufen')\n")
ARBEIT = temp("tb177_arbeit_")


def lade(ki_dir):
    """Laedt pfade/abrufe/aufrufe frisch aus ki_dir (fuer Original und Gegenprobe)."""
    for m in ("pfade", "abrufe", "aufrufe", "claude_client", "anthropic"):
        sys.modules.pop(m, None)
    sys.path[:] = [p for p in sys.path if p not in (KI_DIR, ki_dir, STUB)]
    sys.path.insert(0, STUB)
    sys.path.insert(0, ki_dir)
    import pfade as p_   # noqa
    import abrufe as a_  # noqa
    import aufrufe as u_  # noqa
    return p_, a_, u_


class Attrappe:
    def __init__(self, ein=100, aus=50, erfolg=True):
        self.n, self.ein, self.aus, self.erfolg, self.args = 0, ein, aus, erfolg, []

    def __call__(self, system_prompt, user_message, max_tokens=1000, tools=None, model=None, thinking=None):
        self.n += 1
        self.args.append({"tools": tools, "model": model, "max_tokens": max_tokens})
        if not self.erfolg:
            return {"success": False, "error": "Attrappe: Fehler"}
        raw = types.SimpleNamespace(usage=types.SimpleNamespace(input_tokens=self.ein, output_tokens=self.aus), model=model)
        return {"success": True, "text": "{}", "raw": raw}


def leerer_schalter():
    p = os.path.join(ARBEIT, "schalter_leer.txt")
    open(p, "w").close()
    return p


def bremse_faelle(u, db, cc_modell):
    """Gibt (name, ok, detail) je Fall zurueck."""
    aus = []
    s0 = leerer_schalter()
    okt = datetime.datetime(2026, 10, 20, 12, tzinfo=datetime.timezone.utc)
    u._jetzt = lambda: okt  # Uhr des Moduls (intern), kein Parameter des Aufrufers
    a = Attrappe()
    r = u.aufrufen("bots", "test", "sys", "nutzer", max_tokens=200, db=db, aufruf=a, schalter=s0)
    summe = u.monatssumme("bots", "2026-10", db=db)
    aus.append(("W4a normaler Aufruf: abgerechnet, Monatssumme = echter Preis", r["success"] and a.n == 1 and abs(summe - u.preis(cc_modell, 100, 50)) < 1e-12, (r, summe)))
    aus.append(("W4b Modell = MODEL_HAIKU, tools=None an call_claude", a.args[0]["model"] == cc_modell and a.args[0]["tools"] is None, a.args))
    b = Attrappe(ein=4000, aus=4000)
    n_ok = 0
    for _ in range(100000):
        r = u.aufrufen("sammler", "test", "s" * 2000, "u" * 2000, max_tokens=4000, db=db, aufruf=b, schalter=s0)
        if r["gebremst"]:
            break
        n_ok += 1
    s_sam = u.monatssumme("sammler", "2026-10", db=db)
    res = u.hoechstpreis(cc_modell, "s" * 2000, "u" * 2000, 4000)
    aus.append(("W4c Bremse stoppt vor dem Deckel (Summe <= 3 $, nicht zu frueh, gebremster Aufruf ohne Attrappe)", r["gebremst"] and b.n == n_ok and n_ok > 0 and s_sam <= u.DECKEL_USD["sammler"] and s_sam + res > u.DECKEL_USD["sammler"], (n_ok, s_sam, res)))
    vor = b.n
    r2 = u.aufrufen("sammler", "test", "s", "u", max_tokens=int(u.DECKEL_USD["sammler"] * 1e6), db=db, aufruf=b, schalter=s0)
    aus.append(("W4d Aufruf, dessen Hoechstpreis den Rest uebersteigt, wird gebremst; Attrappe nicht gerufen", r2["gebremst"] and b.n == vor, r2))
    c = Attrappe()
    r3 = u.aufrufen("bots", "test", "sys", "nutzer", max_tokens=200, db=db, aufruf=c, schalter=s0)
    aus.append(("W4e Toepfe getrennt: voller Topf sammler bremst ki_bots nicht", (not r3["gebremst"]) and c.n == 1, r3))
    nov = datetime.datetime(2026, 11, 1, 0, 0, 1, tzinfo=datetime.timezone.utc)
    u._jetzt = lambda: nov
    r4 = u.aufrufen("sammler", "test", "sys", "nutzer", max_tokens=200, db=db, aufruf=c, schalter=s0)
    aus.append(("W4f Monatswechsel (UTC): neuer Monat beginnt bei 0", (not r4["gebremst"]) and u.monatssumme("sammler", "2026-11", db=db) > 0, r4))
    sch = os.path.join(ARBEIT, "schalter_aus.txt")
    open(sch, "w").write("ki_bots\n")
    d = Attrappe()
    r5 = u.aufrufen("bots", "test", "sys", "nutzer", db=db, aufruf=d, schalter=sch)
    aus.append(("W4g Notschalter ki_bots: kein Aufruf", r5["gebremst"] and d.n == 0, r5))
    e = Attrappe(erfolg=False)
    vor_s = u.monatssumme("bots", "2026-11", db=db)
    r6 = u.aufrufen("bots", "test", "sys", "nutzer", max_tokens=300, db=db, aufruf=e, schalter=s0)
    nach_s = u.monatssumme("bots", "2026-11", db=db)
    aus.append(("W4h Fehlerpfad: Reservierung bleibt stehen (zu viel, nie zu wenig)", (not r6["success"]) and abs((nach_s - vor_s) - u.hoechstpreis(cc_modell, "sys", "nutzer", 300)) < 1e-12, (vor_s, nach_s)))
    conn = sqlite3.connect(db)
    fehl = []
    for sql in ("UPDATE aufrufe SET kosten_usd = 0", "DELETE FROM aufrufe"):
        try:
            conn.execute(sql)
            fehl.append(sql)
        except sqlite3.DatabaseError:
            pass
    conn.close()
    aus.append(("W4i aufrufe.db nur anfuegend (UPDATE und DELETE abgewiesen)", not fehl, fehl))
    aus += eingabe_faelle(u, db)
    try:
        u.aufrufen("dritter_topf", "test", "s", "u", db=db, aufruf=Attrappe(), schalter=s0)
        aus.append(("W4j unbekannter Topf abgelehnt", False, ""))
    except ValueError:
        aus.append(("W4j unbekannter Topf abgelehnt", True, ""))
    return aus


def eingabe_faelle(u, db):
    """W4k: unzulaessige Eingaben werden vor jeder Buchung abgewiesen; W4l: CHECK in aufrufe.db."""
    aus = []
    s0 = leerer_schalter()
    zahl = lambda: sqlite3.connect(db).execute("SELECT COUNT(*), COALESCE(SUM(kosten_usd), 0) FROM aufrufe").fetchone()
    f = Attrappe()
    falsch = []
    for mt in (-10 ** 6, -1, 0, 2.5, 600.0, True, None, "600"):
        vor = zahl()
        try:
            u.aufrufen("bots", "test", "sys", "nutzer", max_tokens=mt, db=db, aufruf=f, schalter=s0)
            falsch.append(repr(mt))
        except ValueError:
            if zahl() != vor:
                falsch.append(repr(mt) + " gebucht")
    for sp, um in ((None, "u"), ("s", b"u")):
        vor = zahl()
        try:
            u.aufrufen("bots", "test", sp, um, db=db, aufruf=f, schalter=s0)
            falsch.append("Text %r/%r" % (sp, um))
        except ValueError:
            if zahl() != vor:
                falsch.append("Text gebucht")
    aus.append(("W4k max_tokens negativ, 0, Kommazahl, bool, None, Text und Nicht-Text-Eingaben: ValueError vor jeder Buchung, Attrappe nie gerufen",
                not falsch and f.n == 0, (falsch, f.n)))
    c = sqlite3.connect(db)
    durch = []
    for name, mt, k in (("kosten -1", 1, -1.0), ("max_tokens 0", 0, 0.1), ("max_tokens 2.5", 2.5, 0.1), ("max_tokens -5", -5, 0.0)):
        try:
            c.execute("INSERT INTO aufrufe (zeit_utc, monat, topf, verbraucher, status, modell_angefordert, prompt_hash, max_tokens, kosten_usd)"
                      " VALUES ('x', '2026-10', 'bots', 't', 'reserviert', 'm', 'h', ?, ?)", (mt, k))
            durch.append(name)
        except sqlite3.DatabaseError:
            pass
    c.rollback()
    c.close()
    aus.append(("W4l aufrufe.db CHECK: negative Kosten, max_tokens 0/-5/2.5 abgewiesen", not durch, durch))
    return aus


def abruf_faelle(a, db):
    aus = []
    a.jetzt_utc = lambda: "2026-10-17T06:00:00.000000Z"  # Uhr des Moduls (intern)
    r = a.einfrieren("fear_greed", "fng", b'{"value": 40}', "json", url="attrappe://fng", db=db)
    aus.append(("W6a einfrieren: sha256 der Rohkopie", r["sha256"] == hashlib.sha256(b'{"value": 40}').hexdigest(), r))
    a.jetzt_utc = lambda: "2026-10-18T06:00:00.000000Z"
    a.einfrieren("fear_greed", "fng", b'{"value": 55}', "json", db=db)
    s1 = a.stand("fear_greed", "fng", "2026-10-17T23:59:59Z", db=db)
    s0 = a.stand("fear_greed", "fng", "2026-10-16T23:59:59Z", db=db)
    aus.append(("W6b Vintage: Stand am 17.10. ist der Abruf vom 17.10., vorher keiner", s1 and s1["roh"] == b'{"value": 40}' and s0 is None, (s1 and s1["abgerufen_utc"], s0)))

    def kaputt(url):
        raise OSError("Attrappe: kein Netz")
    r2 = a.abrufen("alfred", "DGS10", "attrappe://alfred", "json", holer=kaputt, db=db)
    aus.append(("W6c Ausfall wird gebucht, nicht geworfen; Stand bleibt beim letzten guten", r2["status"] == "ausgefallen" and a.stand("alfred", "DGS10", "9999-12-31T23:59:59Z", db=db) is None, r2))
    r3 = a.abrufen("binance_spot", "BTCUSDT", "attrappe://b", "json", holer=lambda url: b"[1,2]", db=db)
    aus.append(("W6d abrufen mit Attrappe friert ein", r3["status"] == "ok", r3))
    conn = sqlite3.connect(db)
    fehl = []
    for sql in ("UPDATE abrufe SET roh = x'00'", "DELETE FROM abrufe"):
        try:
            conn.execute(sql)
            fehl.append(sql)
        except sqlite3.DatabaseError:
            pass
    conn.close()
    aus.append(("W6e abrufe.db nur anfuegend", not fehl, fehl))
    try:
        a.einfrieren("websuche", "x", b"", "txt", db=db)
        aus.append(("W6f unbekannte Quelle abgelehnt", False, ""))
    except ValueError:
        aus.append(("W6f unbekannte Quelle abgelehnt", True, ""))
    return aus


def zeitgrenze_fall(a, db):
    """W6h: Abruf um 12:00:00,5 UTC; die Grenze wird als Zeitpunkt verglichen."""
    a.jetzt_utc = lambda: "2026-10-19T12:00:00.500000Z"
    a.einfrieren("rss", "zeitgrenze", b"<rss/>", "xml", db=db)
    st = lambda bis: a.stand("rss", "zeitgrenze", bis, db=db)
    erg = {"12:00:00Z": st("2026-10-19T12:00:00Z") is None,
           "12:00:00,5Z": st("2026-10-19T12:00:00,5Z") is not None,
           "14:00:00.5+02:00": st("2026-10-19T14:00:00.5+02:00") is not None,
           "14:00:00+02:00": st("2026-10-19T14:00:00+02:00") is None,
           "datetime 12:00:00.5 UTC": st(datetime.datetime(2026, 10, 19, 12, 0, 0, 500000, tzinfo=datetime.timezone.utc)) is not None}
    try:
        st("2026-10-19T12:00:01")
        erg["ohne Zeitzone -> ValueError"] = False
    except ValueError:
        erg["ohne Zeitzone -> ValueError"] = True
    return ("W6h Zeitgrenze als Zeitpunkt (Abruf 12:00:00,5; Z, +02:00, Komma, datetime, ohne Zone abgewiesen)",
            all(erg.values()), [k for k, v in erg.items() if not v])


def ersetzen_faelle(db_ab, db_auf):
    """W6g: INSERT OR REPLACE mit vorhandener id ueberschreibt keine Zeile (rohe
    Verbindung ohne recursive_triggers: es schuetzt allein der Trigger); W6i: Zeitformat."""
    aus = []
    c = sqlite3.connect(db_ab)
    vor = c.execute("SELECT roh FROM abrufe WHERE id = 1").fetchone()
    try:
        c.execute("INSERT OR REPLACE INTO abrufe (id, quelle, schluessel, abgerufen_utc, format, status, bytes, sha256, roh)"
                  " VALUES (1, 'rss', 'x', '2026-10-17T06:00:00.000000Z', 'txt', 'ok', 1, '0', x'00')")
        c.commit()
        durch = True
    except sqlite3.DatabaseError:
        durch = False
    nach = c.execute("SELECT roh FROM abrufe WHERE id = 1").fetchone()
    aus.append(("W6g abrufe.db: INSERT OR REPLACE mit vorhandener id abgewiesen, Zeile 1 unveraendert", vor is not None and not durch and vor == nach, (durch, vor == nach)))
    try:
        c.execute("INSERT INTO abrufe (quelle, schluessel, abgerufen_utc, format, status, bytes, sha256, roh)"
                  " VALUES ('rss', 'x', '2026-10-17 06:00', 'txt', 'ok', 0, '0', x'')")
        fmt = False
    except sqlite3.DatabaseError:
        fmt = True
    aus.append(("W6i abrufe.db: Abrufzeit ausserhalb des festen Formats abgewiesen (CHECK)", fmt, ""))
    c.close()
    c = sqlite3.connect(db_auf)
    s_vor = c.execute("SELECT SUM(kosten_usd) FROM aufrufe").fetchone()[0]
    ziel = c.execute("SELECT MIN(id) FROM aufrufe WHERE status = 'abgerechnet'").fetchone()[0]
    try:
        c.execute("INSERT OR REPLACE INTO aufrufe (id, zeit_utc, monat, topf, verbraucher, status, modell_angefordert, prompt_hash, max_tokens, kosten_usd)"
                  " VALUES (?, 'x', '2026-10', 'bots', 't', 'gebremst', 'm', 'h', 1, 0.0)", (ziel,))
        c.commit()
        durch = True
    except sqlite3.DatabaseError:
        durch = False
    s_nach = c.execute("SELECT SUM(kosten_usd) FROM aufrufe").fetchone()[0]
    c.close()
    aus.append(("W6g aufrufe.db: INSERT OR REPLACE auf eine Abrechnungszeile abgewiesen, Summe unveraendert", ziel and s_vor and not durch and s_vor == s_nach, (durch, s_vor, s_nach)))
    return aus


def zeit_nicht_setzbar(a, u):
    arg = lambda f: f.__code__.co_varnames[:f.__code__.co_argcount]
    b = ["abrufe.%s(%s)" % (f.__name__, n) for f in (a.einfrieren, a.ausfall, a.abrufen) for n in arg(f) if "utc" in n or "zeit" in n or "jetzt" in n]
    b += ["aufrufe.aufrufen(%s)" % n for n in arg(u.aufrufen) if "zeit" in n or "jetzt" in n or "monat" in n]
    return ("W6j Abrufzeit und Buchungszeit nicht vom Aufrufer setzbar", not b, b)


def stand_code(wurzel):
    """Groesse, mtime, sha256 der Code-Dateien unter shared/, strategies/, notifications/."""
    st = {}
    for ordner in ("shared", "strategies", "notifications"):
        for d, _u, fs in os.walk(os.path.join(wurzel, ordner)):
            for f in fs:
                if f.endswith(".py") and "__pycache__" not in d:
                    q = os.path.join(d, f)
                    x = os.stat(q)
                    st[os.path.relpath(q, wurzel)] = (x.st_size, x.st_mtime_ns, hashlib.sha256(open(q, "rb").read()).hexdigest())
    return st


class Rekorder:
    """Zeichnet waehrend der Laufzeitfaelle jedes sqlite3.connect und jedes open()
    zum Schreiben auf und sperrt das Netz (urlopen wirft). Ziel: alles unter ARBEIT."""
    def __enter__(self):
        import builtins
        import io
        import urllib.request
        self.b, self.io, self.u, self.pfade, self.netz = builtins, io, urllib.request, [], 0
        self.alt = (sqlite3.connect, builtins.open, urllib.request.urlopen, io.open, os.open, os.fdopen)
        schreib = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
        def os_oeffne(pfad, flags, *a, **k):
            if flags & schreib:
                self.pfade.append(("os.open", str(pfad)))
            return self.alt[4](pfad, flags, *a, **k)
        def io_oeffne(datei, modus="r", *a, **k):
            if isinstance(modus, str) and any(c in modus for c in "wax+"):
                self.pfade.append(("io.open", str(datei)))
            return self.alt[3](datei, modus, *a, **k)
        def fd_oeffne(fd, modus="r", *a, **k):
            if isinstance(modus, str) and any(c in modus for c in "wax+"):
                self.pfade.append(("fdopen", "fd %s" % fd))
            return self.alt[5](fd, modus, *a, **k)
        def connect(db, *a, **k):
            self.pfade.append(("connect", str(db)))
            return self.alt[0](db, *a, **k)
        def oeffne(datei, modus="r", *a, **k):
            if isinstance(modus, str) and any(c in modus for c in "wax+"):
                self.pfade.append(("open", str(datei)))
            return self.alt[1](datei, modus, *a, **k)
        def netz(*a, **k):
            self.netz += 1
            raise OSError("Test: kein Netz")
        sqlite3.connect, builtins.open, urllib.request.urlopen = connect, oeffne, netz
        io.open, os.open, os.fdopen = io_oeffne, os_oeffne, fd_oeffne
        return self

    def __exit__(self, *e):
        sqlite3.connect, self.b.open, self.u.urlopen, self.io.open, os.open, os.fdopen = self.alt
        return False


def verfaelschen(name, aenderung):
    """Kopie von ki_forschung in einen temporaeren Ordner mit einer Verfaelschung."""
    ziel = os.path.join(temp("tb177_gp_"), "ki_forschung")
    shutil.copytree(KI_DIR, ziel, ignore=shutil.ignore_patterns("*.db", "__pycache__"))
    datei, alt, neu = aenderung
    p = os.path.join(ziel, datei)
    q = open(p, encoding="utf-8").read()
    assert q.count(alt) == 1, (name, alt)
    open(p, "w", encoding="utf-8").write(q.replace(alt, neu))
    return ziel


def main():
    print("Wachen-Test KI-Forschung (TB-177)  Repo %s" % REPO)
    print("\nW1 Importe")
    b = befunde_w1(KI_DIR)
    pruefe("W1 nur Importe der Positivliste (%d Dateien)" % len([f for f in os.listdir(KI_DIR) if f.endswith(".py")]), not b, b)
    print("\nW2 Schreibziele (statisch)")
    b = befunde_w2(KI_DIR)
    pruefe("W2 keine fremden Schreibziele, connect nur in verbinden(), kein open()", not b, b)
    p_, a_, u_ = lade(KI_DIR)
    pruefe("W2b abrufe.db und aufrufe.db liegen in ki_forschung/", os.path.dirname(p_.ABRUFE_DB) == KI_DIR == os.path.dirname(p_.AUFRUFE_DB)
           and not os.path.basename(p_.ABRUFE_DB).startswith("paper_trading"), (p_.ABRUFE_DB, p_.AUFRUFE_DB))
    print("\nW3 Erkennung und Laufbereich")
    b = befunde_w3(REPO, KI_DIR)
    pruefe("W3 nicht in strategies/, ASSET_CLASS, Laufbereich; kein Modul in shared/strategies/notifications nennt ki_forschung", not b, b)
    print("\nW5 Schluessel und Websuche")
    b = befunde_w5(KI_DIR)
    pruefe("W5 kein os.environ, keine .env, kein email_config, keine Websuche", not b, b)
    print("\nW4/W6 Laufzeit mit Attrappe (temporaere DBs)")
    db_ki_vorher = [os.path.exists(p_.ABRUFE_DB), os.path.exists(p_.AUFRUFE_DB)]
    import claude_client
    code_vorher = stand_code(REPO)
    with Rekorder() as rek:
        faelle = bremse_faelle(u_, os.path.join(ARBEIT, "aufrufe.db"), claude_client.MODEL_HAIKU) + abruf_faelle(a_, os.path.join(ARBEIT, "abrufe.db"))
        faelle += [zeitgrenze_fall(a_, os.path.join(ARBEIT, "abrufe.db")), zeit_nicht_setzbar(a_, u_)]
    faelle += ersetzen_faelle(os.path.join(ARBEIT, "abrufe.db"), os.path.join(ARBEIT, "aufrufe.db"))
    code_nachher = stand_code(REPO)
    diff_code = sorted(k for k in set(code_vorher) | set(code_nachher) if code_vorher.get(k) != code_nachher.get(k))
    for n, ok, det in faelle:
        pruefe(n, ok, "" if ok else det)
    fremd = sorted(set(p for _a, p in rek.pfade if not os.path.realpath(p).startswith(os.path.realpath(ARBEIT) + os.sep)))
    pruefe("W2c Laufzeit: jedes connect/open zum Schreiben im temporaeren Ordner (%d Zugriffe)" % len(rek.pfade), rek.pfade and not fremd, fremd[:5])
    pruefe("W2e Laufzeit: kein Netz (urlopen nie gerufen)", rek.netz == 0, rek.netz)
    pruefe("W2f Code unter shared/, strategies/, notifications/ vorher = nachher (%d Dateien, Groesse/mtime/sha256)" % len(code_vorher), code_vorher and not diff_code, diff_code[:5])
    pruefe("W2d Laufzeit: echte abrufe.db/aufrufe.db nicht angelegt", [os.path.exists(p_.ABRUFE_DB), os.path.exists(p_.AUFRUFE_DB)] == db_ki_vorher)

    print("\nG Gegenproben (verfaelschte Kopien muessen rot werden)")
    gp = [("G1 Import aus strategies/", befunde_w1, ("aufrufe.py", "import pfade  # noqa: E402\n", "import pfade  # noqa: E402\nfrom strategies.t3_supertrend import forward_test  # noqa\n")),
          ("G1b Import zuteilung", befunde_w1, ("abrufe.py", "import pfade  # noqa: E402\n", "import pfade  # noqa: E402\nimport zuteilung  # noqa\n")),
          ("G2 Schreibziel Bot-DB", befunde_w2, ("pfade.py", 'AUFRUFE_DB = os.path.join(KI_DIR, "aufrufe.db")', 'AUFRUFE_DB = os.path.join(REPO_DIR, "paper_trading_t3_supertrend.db")')),
          ("G2b connect ausserhalb verbinden()", befunde_w2, ("abrufe.py", "def stand(quelle, schluessel, bis, db=None):\n", "def stand(quelle, schluessel, bis, db=None):\n    sqlite3.connect(db)\n")),
          ("G2c os.open", befunde_w2, ("abrufe.py", "    sha = hashlib.sha256(roh).hexdigest()\n", "    sha = hashlib.sha256(roh).hexdigest()\n    os.close(os.open('x', os.O_CREAT))\n")),
          ("G2d getattr(os, 'open')", befunde_w2, ("abrufe.py", "    sha = hashlib.sha256(roh).hexdigest()\n", "    sha = hashlib.sha256(roh).hexdigest()\n    getattr(os, 'open')\n")),
          ("G2e getattr mit Namen aus einer Variablen", befunde_w2, ("abrufe.py", "    sha = hashlib.sha256(roh).hexdigest()\n", "    sha = hashlib.sha256(roh).hexdigest()\n    n = 'op' + 'en'\n    getattr(os, n)\n")),
          ("G5 Schluessel aus der Umgebung", befunde_w5, ("aufrufe.py", "    modell = claude_client.MODEL_HAIKU\n", "    modell = claude_client.MODEL_HAIKU\n    _k = os.environ.get('X')\n")),
          ("G5b Websuche als Werkzeug", befunde_w5, ("aufrufe.py", "tools=None, model=modell)", "tools=[{'type': 'web_search'}], model=modell)"))]
    for name, fn, aend in gp:
        k = verfaelschen(name, aend)
        b = fn(k)
        pruefe("%s -> rot" % name, bool(b), b[:2])
    k = verfaelschen("G4", ("aufrufe.py", "            if summe + reserve > DECKEL_USD[topf]:\n", "            if False:\n"))
    _p, _a, uk = lade(k)
    f = Attrappe(ein=4000, aus=4000)
    okt = datetime.datetime(2026, 10, 20, tzinfo=datetime.timezone.utc)
    uk._jetzt = lambda: okt
    dbg = os.path.join(ARBEIT, "gp_aufrufe.db")
    for _ in range(400):
        uk.aufrufen("sammler", "gp", "s" * 2000, "u" * 2000, max_tokens=4000, db=dbg, aufruf=f, schalter=leerer_schalter())
    pruefe("G4 Bremse ausgebaut -> Summe ueber dem Deckel (rot)", uk.monatssumme("sammler", "2026-10", db=dbg) > uk.DECKEL_USD["sammler"])
    # G7/W4m: Pruefung im Code ausgebaut - der CHECK haelt allein; beides ausgebaut - Bremse umgangen (rot)
    k = verfaelschen("W4m", ("aufrufe.py", "    eingabe_pruefen(system_prompt, user_message, max_tokens)\n    modell = claude_client.MODEL_HAIKU",
                             "    modell = claude_client.MODEL_HAIKU"))
    q = os.path.join(k, "aufrufe.py")
    t = open(q, encoding="utf-8").read().replace("    eingabe_pruefen(system_prompt, user_message, max_tokens)\n    p = PREIS_JE_MTOK", "    p = PREIS_JE_MTOK")
    t = t.replace('    if not (0 <= reserve < float("inf")):\n', '    if False:\n')
    open(q, "w", encoding="utf-8").write(t)
    _p, _a, uk = lade(k)
    dbm = os.path.join(ARBEIT, "w4m_aufrufe.db")
    try:
        uk.aufrufen("sammler", "w4m", "s", "u", max_tokens=-10 ** 6, db=dbm, aufruf=Attrappe(), schalter=leerer_schalter())
        m_ok = False
    except sqlite3.DatabaseError:
        m_ok = uk.monatssumme("sammler", uk._jetzt().strftime("%Y-%m"), db=dbm) == 0
    pruefe("W4m Code-Pruefung ausgebaut: CHECK in aufrufe.db weist die negative Reserve allein ab", m_ok)
    t = open(q, encoding="utf-8").read()
    for alt, neu in (("CHECK (kosten_usd >= 0)", ""), ("CHECK (typeof(max_tokens) = 'integer' AND max_tokens >= 1)", "")):
        assert t.count(alt) == 1, alt
        t = t.replace(alt, neu)
    open(q, "w", encoding="utf-8").write(t)
    _p, _a, uk = lade(k)
    dbg7 = os.path.join(ARBEIT, "g7_aufrufe.db")
    # wie die echte API: der Aufruf mit negativem max_tokens scheitert -> Reserve (negativ) bleibt gebucht
    uk.aufrufen("sammler", "g7", "s", "u", max_tokens=-10 ** 6, db=dbg7, aufruf=Attrappe(erfolg=False), schalter=leerer_schalter())
    g = Attrappe(ein=1, aus=200000)
    for _ in range(10):
        uk.aufrufen("sammler", "g7", "s", "u", max_tokens=200000, db=dbg7, aufruf=g, schalter=leerer_schalter())
    ausgegeben = g.n * uk.preis(list(uk.PREIS_JE_MTOK)[0], 1, 200000)
    pruefe("G7 Pruefung und CHECK ausgebaut -> negative Buchung, danach mehr als 3 $ echt ausgegeben (rot)", ausgegeben > uk.DECKEL_USD["sammler"], (g.n, ausgegeben))
    # G2f: Laufzeit-Rekorder an einer Kopie, die per os.open ausserhalb schreibt
    k = verfaelschen("G2f", ("abrufe.py", "    sha = hashlib.sha256(roh).hexdigest()\n",
                             "    sha = hashlib.sha256(roh).hexdigest()\n    os.close(os.open(os.path.join(pfade.REPO_DIR, 'fremd_g2f.txt'), os.O_CREAT | os.O_WRONLY))\n"))
    _p, ak, _u = lade(k)
    with Rekorder() as rek:
        ak.einfrieren("rss", "g2f", b"x", "xml", db=os.path.join(ARBEIT, "g2f.db"))
    fremd = [q for _a, q in rek.pfade if not os.path.realpath(q).startswith(os.path.realpath(ARBEIT) + os.sep)]
    pruefe("G2f Laufzeit: os.open ausserhalb des temporaeren Ordners -> rot", bool(fremd), fremd[:2])
    # G6: Ersetzungsschutz ausgebaut
    k = verfaelschen("G6", ("abrufe.py", "WHEN NEW.id IS NOT NULL AND EXISTS (SELECT 1 FROM abrufe WHERE id = NEW.id)", "WHEN 0"))
    _p, ak, uk = lade(k)
    ak.einfrieren("rss", "g6", b"x", "xml", db=os.path.join(ARBEIT, "g6_abrufe.db"))
    uk.aufrufen("bots", "g6", "s", "u", db=os.path.join(ARBEIT, "g6_aufrufe.db"), aufruf=Attrappe(), schalter=leerer_schalter())
    g6 = ersetzen_faelle(os.path.join(ARBEIT, "g6_abrufe.db"), os.path.join(ARBEIT, "g6_aufrufe.db"))[0]
    pruefe("G6 abrufe ohne Ersetzungsschutz -> W6g rot", not g6[1], g6[2])
    k = verfaelschen("G6c", ("aufrufe.py", "WHEN NEW.id IS NOT NULL AND EXISTS (SELECT 1 FROM aufrufe WHERE id = NEW.id)", "WHEN 0"))
    _p, ak, uk = lade(k)
    ak.einfrieren("rss", "g6c", b"x", "xml", db=os.path.join(ARBEIT, "g6c_abrufe.db"))
    uk.aufrufen("bots", "g6c", "s", "u", db=os.path.join(ARBEIT, "g6c_aufrufe.db"), aufruf=Attrappe(), schalter=leerer_schalter())
    g6c = ersetzen_faelle(os.path.join(ARBEIT, "g6c_abrufe.db"), os.path.join(ARBEIT, "g6c_aufrufe.db"))[2]
    pruefe("G6c aufrufe ohne Ersetzungsschutz -> W6g rot", not g6c[1], g6c[2])
    # G6b: Zeitgrenze wieder als Text
    k = verfaelschen("G6b", ("abrufe.py", "    grenze = zeitpunkt(bis)\n", "    grenze = bis\n"))
    _p, ak, _u = lade(k)
    g6b = zeitgrenze_fall(ak, os.path.join(ARBEIT, "g6b_abrufe.db"))
    pruefe("G6b Zeitgrenze als Text -> W6h rot", not g6b[1], g6b[2])
    lade(KI_DIR)
    g3 = temp("tb177_g3_")
    for t in ("shared", "notifications"):
        os.makedirs(os.path.join(g3, t))
    shutil.copy(os.path.join(REPO, "shared", "paths.py"), os.path.join(g3, "shared", "paths.py"))
    shutil.copy(os.path.join(REPO, "notifications", "monitor.py"), os.path.join(g3, "notifications", "monitor.py"))
    open(os.path.join(g3, "shared", "fremd.py"), "w").write("import ki_forschung\n")
    pruefe("G3 Laufbereichsmodul nennt ki_forschung -> rot", bool(befunde_w3(g3, os.path.join(g3, "ki_forschung"))))
    pruefe("G3b ki_forschung unter strategies/ -> rot", bool(befunde_w3(REPO, os.path.join(REPO, "strategies", "ki_forschung"))))

    n_fehlt = sum(1 for _n, ok in ERGEBNIS if not ok)
    print("\nPruefungen: %d, FEHLT: %d" % (len(ERGEBNIS), n_fehlt))
    return 1 if n_fehlt else 0


if __name__ == "__main__":
    try:
        rc = main()
    finally:
        for d in TEMP:
            shutil.rmtree(d, ignore_errors=True)
        print("temporaere Ordner entfernt: %d" % len(TEMP))
    sys.exit(rc)
````

