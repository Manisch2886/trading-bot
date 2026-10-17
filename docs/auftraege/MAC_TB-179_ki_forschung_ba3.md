# TB-179 KI-Forschung BA3: Regelblätter, Fragenkatalog v1, Prompts mit Manifest (sha256), Regel-Test — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 17.10.2026, 22:58** (Helfer BAU179, per Skript aus Bausteinen, `/tmp/w36/sc/tb179/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; Holbefehl, V, B und T an einer kleinen Kopie simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser. **Gebaut am HEAD `397b257` (TB-178 fertig; `ki_forschung/` seit `e79ca2c` unverändert, sha256 der vier Dateien gemessen; Regelblätter vom Betreiber am 17.10.2026 freigegeben, danach je Bot ein Satz zum Ort des Startkapitals nach R110 (b) ergänzt); Start am HEAD `397b257a7842ca8e6b538d88055a40eb5c3e57e9`.**

**Sitzungstitel:** `TB-179` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `397b257a7842ca8e6b538d88055a40eb5c3e57e9` · **Start:** über den Sitzungswächter (`starte_TB-179`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-179_ki_forschung_ba3.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`. **Belege:** `docs/belege/TB-179/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-179_ki_forschung_ba3.md`.
**Grundlage:** Betreiberentscheide 17.10.2026 (Haiku; Deckel je Topf 3 $/Monat, `sammler` und `bots` getrennt; keine Websuche; Aktien nur UCITS-ETFs; Filter bei Zustand −2 an der Frage „Risikoneigung“ je Markt, Mit/ohne-Vergleich nur im Bereich „KI-Forschung“, Regel fest vor dem ersten Zustand; drei KI-Bots im Paper Trade, rein KI (MI1 (b) nur für Paper gebrochen), streng getrennt, Regime-Bot fragt selbst und liest den Sammler nicht; Leseregel R108 (b) für den Filtervergleich gebrochen, „Regel vorher fest“). R108 (b) (2): Katalog v1 und Prompt liegen mit Hash im Repo, bevor der erste Lauf schreibt; eine Änderung ist v2. Pläne PLAN_KIBOTS und PLAN_KISAMMLER des steuernden Chats (ausserhalb des Repos). TB-177 (`ki_forschung/` BA1, Wachen-Test 50/0).
**Am Bau-HEAD gemessen:** `MODEL_HAIKU = "claude-haiku-4-5-20251001"` (`shared/claude_client.py` Z. 31); `DECKEL_USD` (`ki_forschung/aufrufe.py` Z. 39) = `{"sammler": 3.0, "bots": 3.0}`; `STARTING_CAPITAL = 10_000.0` in allen neun `strategies/*/equity_simulation.py` (elliott_wave Z. 66; elliott_wave_stocks Z. 71; rsi2_crypto Z. 51; rsi2_mean_reversion Z. 62; t3_supertrend Z. 54; turtle_soup_crypto Z. 45; turtle_soup_stocks Z. 68; volatility_breakout Z. 61; volatility_breakout_crypto Z. 61); `TRADING_FEE_PCT = 0.1` und `SLIPPAGE_PCT = 0.05` in allen neun `forward_test.py`; `ASSET_CLASS` `notifications/monitor.py` Z. 86 (fünf `krypto`, vier `aktien`). Kein UCITS-ISIN steht im Repo: die ISINs der Regelblätter sind „Vorschlag“ aus allgemeiner Quelle (Prüfziffer im Test geprüft, Existenz nicht).
**Handelscode:** nein. Kein Bot, kein Abruf, kein API-Aufruf; es entstehen nur Textdateien, ein Manifest und ein Test unter `ki_forschung/`.
**Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ B (17 Dateien anlegen, eine Zeile in `test_ki_wachen.py`) ⇒ T (Regel-Test, Wachen-Test) ⇒ A (Ergebnis, BACKLOG, Journal, Abgabe) ⇒ F.

## Freigabe — Karte des Betreibers, wörtlich

> Karte des Betreibers im Chat 35 („Opus Trading Bots-17.10.2026 b“), 17.10.2026, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript, Zeit 2026-10-17T20:06:53.819Z UTC): Your questions have been answered: "TB-179 legt die Regeln der KI-Forschung fest, bevor der erste Lauf startet. Danach werden sie nicht mehr geändert, sonst wären die Ergebnisse nicht auswertbar. Sammler: Er stellt täglich je Markt 6 feste Fragen, Antwort von −2 bis +2, und liest nur eingefrorene Daten (rund 0,75 $ im Monat). Filter: Bei Risikoneigung −2 rechnet er nach, wie die neun Bots ohne neue Einstiege gelaufen wären. Er sperrt nichts wirklich, ist nur ein Bericht und nie ein Grund für eine Zulassung. Regime-Bot: BTC und ein S&P-500-UCITS-ETF mit je 50 %; long bei +1 oder mehr, flach bei −1 oder weniger. Rotations-Bot: Hält jeden Montag die besten 3 von 10 UCITS-ETFs (MSCI World, S&P 500, Nasdaq 100, Euro Stoxx 50, DAX, Japan, Schwellenländer, Pazifik, Small Caps, IT) und die besten 3 von 10 Krypto. Nachrichten-Bot: Kauf bei +2 und Kurs über dem 20-Tage-Schnitt, Ausstieg nach 5 Tagen oder bei −5 %. Für alle drei: Paper-Startkapital 10 000, Kosten wie bei den neun, Abbruch bei 25 % unter dem Höchststand, Auswertung am 30.04.2027. Kosten der Bots rund 1,4 $ im Monat (geschätzt). Die ETF-Liste habe ich stichprobenartig geprüft, die Papiere existieren. Kein Handelscode, keine API-Aufrufe; das kommt mit dem Sammler und BA7. Gesendet wird erst nach einer eigenen Karte „Senden?“. Gibst du TB-179 mit diesen Regeln frei? Empfehlung: freigeben. Die Werte sind einfach und messbar, und der Auswertetag gibt rund sechs Monate Daten."="Freigeben (Recommended)". You can now continue with these answers in mind.

Ohne gefüllte Karte (genau eine Zeile `> …` in diesem Abschnitt) **ABBRUCH** in 0a. Die Karte bestätigt die Regelblätter (Anhänge A–E) einschliesslich aller mit „Vorschlag“ markierten Werte; ab dem B-Commit sind sie v1 und fest.

## Was entsteht

- `ki_forschung/regeln/` — fünf Regelblätter (Markdown, je ein Abschnitt `## Pflichtfelder`): `sammler.md` (Märkte, sechs Fragen je Markt, Skala −2 … +2 mit Begründung, Quellen mit Vintage), `filter.md` (Schwelle, Märkte, Start = erster Sammlerlauf, Messgrössen, Auswertedatum, „nie Zulassungsgrund“), `regime_bot.md`, `rotations_bot.md`, `nachrichten_bot.md` (Universum mit UCITS-ISIN bzw. Krypto-Symbol, Entscheidungsregel, Positionsgrösse, Ausstieg, Startkapital Paper, Auswertedatum, Abbruchregel).
- `ki_forschung/prompts/` — 10 Prompts (Sammler: System-Prompt und je Frage eine Datei; je Bot ein System-Prompt) und `manifest.json` (sha256 je Prompt und je Regelblatt, Modell-ID, Deckel je Topf, Topf und Verbraucher je Prompt).
- `ki_forschung/test_ki_regeln.py` — Regel-Test (14 Prüfungen, davon 11 Gegenproben an verfälschten Kopien in temporären Ordnern): Manifest = Dateien, Modell = `MODEL_HAIKU`, Deckel = `DECKEL_USD`, Pflichtfelder je Blatt, ISIN-Prüfziffer, keine US-ISIN, Rotation 10 + 10, Filter „nie Zulassungsgrund“, Prompts ohne Websuche.
- `ki_forschung/test_ki_wachen.py` — eine Zeile: `"json"` kommt in `ERLAUBTE_IMPORTE` (W1 prüft auch Test-Dateien; der Regel-Test liest `manifest.json`). Am Bau gemessen: ohne die Zeile W1 rot (`test_ki_regeln.py:30 json`), mit ihr 50/0.

## Verboten

Kein Abruf, kein API-Aufruf, kein Cron, kein Schlüssel. Nichts unter `strategies/`, `shared/`, `notifications/`, `dashboard/`, `broker/`, `data/`, `config/`, `research/` ändern; in `ki_forschung/` nur die genannten neuen Dateien und die eine Zeile. Kein `git add -A`, kein `-f`, kein `git stash`, kein `rm`, kein `mv`. Keine Regel, kein Prompt, kein Wert ändern (auch kein offensichtlicher Tippfehler): Abweichung melden. **Schreiben darf die Sitzung nur:** `ki_forschung/regeln/`, `ki_forschung/prompts/`, `ki_forschung/test_ki_regeln.py`, die Zeile in `ki_forschung/test_ki_wachen.py` (Schritt B), `BEL`, das Ergebnis, `BACKLOG.md` und `JOURNAL.md` (Schritt A, nur mit dem A-Befehl).

## Schritt 0 — Ausgang

**0a. Zuerst** (Soll: Zweig `main`, HEAD `397b257a7842ca8e6b538d88055a40eb5c3e57e9`, genau die Einträge `[' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-179_ki_forschung_ba3.md']`, `ki_forschung/regeln`, `ki_forschung/prompts`, `ki_forschung/test_ki_regeln.py` gibt es nicht, Karte gefüllt; sonst **ABBRUCH**):

```bash
trading-env/bin/python3 -B - "$TMPDIR" <<'PYEOF'
import os, subprocess, sys
g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True).stdout
st = g("status", "--porcelain"); open(sys.argv[1] + "/tb179_0a.txt", "w", encoding="utf-8").write(st)
soll = [' M docs/auftraege/AKTUELLER_AUFTRAG.md', '?? docs/auftraege/MAC_TB-179_ki_forschung_ba3.md']
ist = [l for l in st.split("\n") if l]; f = []
if g("rev-parse", "--abbrev-ref", "HEAD").strip() != "main": f.append("Zweig nicht main")
if g("rev-parse", "HEAD").strip() != "397b257a7842ca8e6b538d88055a40eb5c3e57e9": f.append("HEAD " + g("rev-parse", "HEAD").strip())
if g("rev-parse", "origin/main").strip() != "397b257a7842ca8e6b538d88055a40eb5c3e57e9": f.append("origin/main " + g("rev-parse", "origin/main").strip())
if os.path.exists(".git/index.lock"): f.append(".git/index.lock da")
f += [p + " gibt es schon" for p in ("ki_forschung/regeln", "ki_forschung/prompts", "ki_forschung/test_ki_regeln.py") if os.path.exists(p)]
f += ["zu viel: " + l for l in ist if l not in soll] + ["fehlt: " + l for l in soll if l not in ist]
z = open("docs/auftraege/MAC_TB-179_ki_forschung_ba3.md", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(z) if l.startswith("## Freigabe")]; b = next(i for i in range(a[0] + 1, len(z)) if z[i].startswith("## "))
k = [l for l in z[a[0] + 1:b] if l.startswith("> ")]
if len(a) != 1 or len(k) != 1 or ("\u27e8\u27e8" + "FREIGABE") in k[0]: f.append("Freigabe-Karte nicht gefuellt")
print("\n".join(ist)); print("ABBRUCH 0a: " + "; ".join(f) if f else "0a gut (%d Eintraege)" % len(ist))
PYEOF
```

Anhänge holen (genau dieser Befehl). Soll genau: `regeln/sammler.md a12425d493e516018b64351708b79b36a02d24e62e29faaae5bd3d5128c838b4`; `regeln/filter.md 567c469ba8495776bc1d1f12347f605971b64ce54367521f98febe1d4faa38ac`; `regeln/regime_bot.md abe56d30393bb9a82adf506bc146fad57adc82070bb2eabb5dec50982022b070`; `regeln/rotations_bot.md d866551f8f06bb8f87827e3267e88d10f988b3770a96955d70bbb72e50b73bca`; `regeln/nachrichten_bot.md f4592c17a404530492e820f914264c8520cfedd73ee87c3870b8055152968705`; `prompts/nachrichten_bot.txt d7e6532dedc270c8d08d5dad6ca7227515948b86a3fb64d26c14ee5c4b85ae54`; `prompts/regime_bot.txt f6ab08a6dfc5321136c3b715f5e93c44173dc02bcbc0533c7a05211b769d33bc`; `prompts/rotations_bot.txt 9641a17bdf193eb687a6779918c6a91ea04c1f2ebfa58f851b16cd96795fd339`; `prompts/sammler_f1_risikoneigung.txt 8657c39a39c5719a775db6d45cd5f8734e01c27425debe0f2cda0673a3a89242`; `prompts/sammler_f2_trend.txt 8c2c15ca26dea29fa5e8b8489feb8f8585ae69d314197a15eb782033f2813c85`; `prompts/sammler_f3_vola_regime.txt 2eb59a1cf257835ddbb9b6a4d215fe18c062b9a095850063ddc6a5eae5f137f9`; `prompts/sammler_f4_makro.txt 3eb0022cd60567cfc50ed7af983ee5daab7a91c8533c76a80d45a664af550744`; `prompts/sammler_f5_liquiditaet.txt 8d42479b8cb10e324686225e874edd3ca43e37fe4eb4a56633422bdd8d9b7d85`; `prompts/sammler_f6_ereignisrisiko.txt d9c1ae746ad45ecd748d20701a23ffb7afd80698b9fd66bf252942e0a90f4e67`; `prompts/sammler_system.txt 2ca4331535326ff1ac7e1b6dd860058cb45ebaa8c5490484e77551f634b4bd10`; `prompts/manifest.json e4f6ac618ce869ee821eee7b084403d3685179f63d4bf5492cb2218f86d5c847`; `test_ki_regeln.py e800dd9521298395b016bc0acb2fb55b0e40d16be79dfe266cc664d63d7365ba`; `Dateien 17`; sonst **ABBRUCH**:

```bash
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-179_ki_forschung_ba3.md "$TMPDIR" <<'PYEOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````[a-z]*\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/tb179_' + name.replace('/', '__'), 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
PYEOF
```

Dann genau diese Zeilen, Commit `TB-179 Schritt 0: Auftrag`, pushen ⇒ **⟨S0⟩**; danach `git status --porcelain` — Soll: keine Ausgabe:

```
trading-env/bin/python3 -B -c "import subprocess, sys; z = [l[3:] for l in open(sys.argv[1], encoding='utf-8').read().split(chr(10)) if l]; print('git add', len(z)); raise SystemExit(subprocess.run(['git', 'add', '--'] + z).returncode)" "$TMPDIR/tb179_0a.txt"
```

## Schritt V — Voraussetzungen

```
mkdir -p docs/belege/TB-179
cp "$TMPDIR/tb179_0a.txt" docs/belege/TB-179/0a_status.txt
{ trading-env/bin/python3 -B - <<'PYEOF'
import hashlib, os
md5 = {"shared/claude_client.py": "7086e27839e6e2825c0d4df9bc133f58", "notifications/monitor.py": "fa8c8a964ab5499fdf729e12f62b2448", "shared/paths.py": "7ee531d0456f2be357192da63995894f"}
alt = {"pfade.py": "aa64fab44b4be80a8b2a74d55487ac91ff202ba01fdd6811ba2afe11db6b47a6", "abrufe.py": "8e18fc3ccf60dc4fd561c5e118ce8eff5444da2a432c8ee71d32d78051a8d83c", "aufrufe.py": "88dfdb05b0f972dc3ed93abaa1c28c3858a3ed0e8362388c2e12c30687a0f337", "test_ki_wachen.py": "40b7a2b9c525495a5a5bb1f897b84ed42b56dcf7877dc8d9b1acc0c126bfaa46"}
n = 0; nein = 0
def p(name, ok):
    global n, nein
    n += 1; nein += 0 if ok else 1; print(('ja   ' if ok else 'NEIN ') + name)
for f, m in md5.items(): p('md5 %s = Bau' % f, hashlib.md5(open(f, 'rb').read()).hexdigest() == m)
for f, s in alt.items(): p('sha256 ki_forschung/%s = TB-177' % f, os.path.isfile('ki_forschung/' + f) and hashlib.sha256(open('ki_forschung/' + f, 'rb').read()).hexdigest() == s)
for x in ('regeln', 'prompts', 'test_ki_regeln.py'): p('ki_forschung/%s fehlt' % x, not os.path.exists('ki_forschung/' + x))
treffer = [os.path.join(d, x) for o in ('shared', 'strategies', 'notifications') for d, _u, fs in os.walk(o) for x in fs if x.endswith('.py') and 'ki_forschung' in open(os.path.join(d, x), encoding='utf-8', errors='replace').read()]
p('kein Modul in shared/strategies/notifications nennt ki_forschung %s' % treffer[:3], not treffer)
print('Pruefungen: %d, NEIN: %d' % (n, nein)); raise SystemExit(1 if nein else 0)
PYEOF
} > docs/belege/TB-179/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-179/v_voraussetzung.txt
```

Soll: letzte Zeile `rc 0` (md5 von `shared/claude_client.py`, `notifications/monitor.py`, `shared/paths.py` = Bau; sha256 der vier Dateien in `ki_forschung/` = TB-177; `regeln/`, `prompts/`, `test_ki_regeln.py` fehlen; kein Modul unter `shared/`, `strategies/`, `notifications/` nennt `ki_forschung`). Abbruch: `printf '%s\n' "V: <Zeile>" > docs/belege/TB-179/abbruch.txt`, `git add` mit Namen für `BEL`-Dateien, Commit `TB-179 Abbruch: V`, pushen, melden.

## Schritt B — Dateien anlegen, eine Zeile ändern

```
mkdir ki_forschung/regeln ki_forschung/prompts
cp "$TMPDIR/tb179_regeln__sammler.md" ki_forschung/regeln/sammler.md
cp "$TMPDIR/tb179_regeln__filter.md" ki_forschung/regeln/filter.md
cp "$TMPDIR/tb179_regeln__regime_bot.md" ki_forschung/regeln/regime_bot.md
cp "$TMPDIR/tb179_regeln__rotations_bot.md" ki_forschung/regeln/rotations_bot.md
cp "$TMPDIR/tb179_regeln__nachrichten_bot.md" ki_forschung/regeln/nachrichten_bot.md
cp "$TMPDIR/tb179_prompts__nachrichten_bot.txt" ki_forschung/prompts/nachrichten_bot.txt
cp "$TMPDIR/tb179_prompts__regime_bot.txt" ki_forschung/prompts/regime_bot.txt
cp "$TMPDIR/tb179_prompts__rotations_bot.txt" ki_forschung/prompts/rotations_bot.txt
cp "$TMPDIR/tb179_prompts__sammler_f1_risikoneigung.txt" ki_forschung/prompts/sammler_f1_risikoneigung.txt
cp "$TMPDIR/tb179_prompts__sammler_f2_trend.txt" ki_forschung/prompts/sammler_f2_trend.txt
cp "$TMPDIR/tb179_prompts__sammler_f3_vola_regime.txt" ki_forschung/prompts/sammler_f3_vola_regime.txt
cp "$TMPDIR/tb179_prompts__sammler_f4_makro.txt" ki_forschung/prompts/sammler_f4_makro.txt
cp "$TMPDIR/tb179_prompts__sammler_f5_liquiditaet.txt" ki_forschung/prompts/sammler_f5_liquiditaet.txt
cp "$TMPDIR/tb179_prompts__sammler_f6_ereignisrisiko.txt" ki_forschung/prompts/sammler_f6_ereignisrisiko.txt
cp "$TMPDIR/tb179_prompts__sammler_system.txt" ki_forschung/prompts/sammler_system.txt
cp "$TMPDIR/tb179_prompts__manifest.json" ki_forschung/prompts/manifest.json
cp "$TMPDIR/tb179_test_ki_regeln.py" ki_forschung/test_ki_regeln.py
{ trading-env/bin/python3 -B - <<'PYEOF'
import hashlib
p = 'ki_forschung/test_ki_wachen.py'
alt, neu = "\"sys\", \"tempfile\", \"types\",\n", "\"sys\", \"tempfile\", \"types\", \"json\",\n"
w = open(p, encoding='utf-8').read()
if w.count(alt) == 1 and hashlib.sha256(w.encode('utf-8')).hexdigest() == "40b7a2b9c525495a5a5bb1f897b84ed42b56dcf7877dc8d9b1acc0c126bfaa46":
    open(p, 'w', encoding='utf-8').write(w.replace(alt, neu))
else:
    print('NEIN test_ki_wachen.py nicht im TB-177-Stand oder Zeile nicht genau einmal')
soll = {"regeln/sammler.md": "a12425d493e516018b64351708b79b36a02d24e62e29faaae5bd3d5128c838b4", "regeln/filter.md": "567c469ba8495776bc1d1f12347f605971b64ce54367521f98febe1d4faa38ac", "regeln/regime_bot.md": "abe56d30393bb9a82adf506bc146fad57adc82070bb2eabb5dec50982022b070", "regeln/rotations_bot.md": "d866551f8f06bb8f87827e3267e88d10f988b3770a96955d70bbb72e50b73bca", "regeln/nachrichten_bot.md": "f4592c17a404530492e820f914264c8520cfedd73ee87c3870b8055152968705", "prompts/nachrichten_bot.txt": "d7e6532dedc270c8d08d5dad6ca7227515948b86a3fb64d26c14ee5c4b85ae54", "prompts/regime_bot.txt": "f6ab08a6dfc5321136c3b715f5e93c44173dc02bcbc0533c7a05211b769d33bc", "prompts/rotations_bot.txt": "9641a17bdf193eb687a6779918c6a91ea04c1f2ebfa58f851b16cd96795fd339", "prompts/sammler_f1_risikoneigung.txt": "8657c39a39c5719a775db6d45cd5f8734e01c27425debe0f2cda0673a3a89242", "prompts/sammler_f2_trend.txt": "8c2c15ca26dea29fa5e8b8489feb8f8585ae69d314197a15eb782033f2813c85", "prompts/sammler_f3_vola_regime.txt": "2eb59a1cf257835ddbb9b6a4d215fe18c062b9a095850063ddc6a5eae5f137f9", "prompts/sammler_f4_makro.txt": "3eb0022cd60567cfc50ed7af983ee5daab7a91c8533c76a80d45a664af550744", "prompts/sammler_f5_liquiditaet.txt": "8d42479b8cb10e324686225e874edd3ca43e37fe4eb4a56633422bdd8d9b7d85", "prompts/sammler_f6_ereignisrisiko.txt": "d9c1ae746ad45ecd748d20701a23ffb7afd80698b9fd66bf252942e0a90f4e67", "prompts/sammler_system.txt": "2ca4331535326ff1ac7e1b6dd860058cb45ebaa8c5490484e77551f634b4bd10", "prompts/manifest.json": "e4f6ac618ce869ee821eee7b084403d3685179f63d4bf5492cb2218f86d5c847", "test_ki_regeln.py": "e800dd9521298395b016bc0acb2fb55b0e40d16be79dfe266cc664d63d7365ba", "test_ki_wachen.py": "821c2120a196311816b68112136613902d294f9ea64b6c674675d41ed975eae4"}
ok = True
for f, s in soll.items():
    i = hashlib.sha256(open('ki_forschung/' + f, 'rb').read()).hexdigest(); print(f, i); ok = ok and i == s
raise SystemExit(0 if ok else 1)
PYEOF
} > docs/belege/TB-179/b_sha.txt 2>&1; echo "rc $?" >> docs/belege/TB-179/b_sha.txt
```

Soll: `b_sha.txt` 18 Zeilen `<datei> <sha256>` gleich Soll (darunter `test_ki_wachen.py 821c2120a196…`), letzte Zeile `rc 0`.

## Schritt T — Regel-Test und Wachen-Test

```
trading-env/bin/python3 -B ki_forschung/test_ki_regeln.py > docs/belege/TB-179/t_regeln.txt 2>&1; echo "rc $?" >> docs/belege/TB-179/t_regeln.txt
trading-env/bin/python3 -B ki_forschung/test_ki_wachen.py > docs/belege/TB-179/t_wachen.txt 2>&1; echo "rc $?" >> docs/belege/TB-179/t_wachen.txt
git status --porcelain > docs/belege/TB-179/t_status.txt
cat docs/belege/TB-179/t_status.txt
```

Soll: `t_regeln.txt` vorletzte Zeile `Pruefungen: 14, FEHLT: 0`, letzte `rc 0`; `t_wachen.txt` vorletzte Zeilen enthalten `Pruefungen: 50, FEHLT: 0`, letzte `rc 0`; `t_status.txt` genau ` M ki_forschung/test_ki_wachen.py`, `?? docs/belege/TB-179/`, `?? ki_forschung/prompts/`, `?? ki_forschung/regeln/`, `?? ki_forschung/test_ki_regeln.py` (kein `.db`, kein `__pycache__`). **Abbruch in T:** kein B-Commit; `printf '%s\n' "T: nicht wie Soll" > docs/belege/TB-179/abbruch.txt`, `git add` mit Namen für die `BEL`-Dateien (nicht `ki_forschung/`), Commit `TB-179 Abbruch: T`, pushen, melden; die neuen Dateien bleiben unverfolgt liegen, die geänderte Zeile bleibt ungestaged.

Dann genau diese Zeilen, Commit `TB-179 B: ki_forschung/ Regelblaetter v1, Prompts mit Manifest, Regel-Test`, pushen:

```
git add ki_forschung/regeln/sammler.md
git add ki_forschung/regeln/filter.md
git add ki_forschung/regeln/regime_bot.md
git add ki_forschung/regeln/rotations_bot.md
git add ki_forschung/regeln/nachrichten_bot.md
git add ki_forschung/prompts/nachrichten_bot.txt
git add ki_forschung/prompts/regime_bot.txt
git add ki_forschung/prompts/rotations_bot.txt
git add ki_forschung/prompts/sammler_f1_risikoneigung.txt
git add ki_forschung/prompts/sammler_f2_trend.txt
git add ki_forschung/prompts/sammler_f3_vola_regime.txt
git add ki_forschung/prompts/sammler_f4_makro.txt
git add ki_forschung/prompts/sammler_f5_liquiditaet.txt
git add ki_forschung/prompts/sammler_f6_ereignisrisiko.txt
git add ki_forschung/prompts/sammler_system.txt
git add ki_forschung/prompts/manifest.json
git add ki_forschung/test_ki_regeln.py
git add ki_forschung/test_ki_wachen.py
git add docs/belege/TB-179/0a_status.txt
git add docs/belege/TB-179/v_voraussetzung.txt
git add docs/belege/TB-179/b_sha.txt
git add docs/belege/TB-179/t_regeln.txt
git add docs/belege/TB-179/t_wachen.txt
git add docs/belege/TB-179/t_status.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

Ergebnis `docs/ERGEBNIS_TB-179_ki_forschung_ba3.md`: Kopf mit Commits; Kurz; 0a; V (letzte Zeilen); B (`b_sha.txt` wörtlich); T (`t_regeln.txt` wörtlich, von `t_wachen.txt` die letzten drei Zeilen); die Kurzfassungen unten; offene Entscheide (unten); „In einfacher Sprache“. BACKLOG und Journal (genau dieser Befehl, nach dem B-Commit; hängt die Zeile an die Rang-1-Zelle nach dem TB-178-Anker an und setzt den Journal-Block vor `## Wiederkehrende Lehren`; Kennung = nächste nach der letzten `## F?`-Überschrift, am Bau-HEAD FO ⇒ FP). Soll: letzte Zeile `rc 0`, `Pruefungen: 6, NEIN: 0`:

```
{ trading-env/bin/python3 -B - "$(TZ=Europe/Berlin date +%d.%m.%Y)" "$(git rev-parse --short HEAD)" "$(git log -1 --format=%h --grep='^TB-179 Schritt 0')" <<'PYEOF'
import json, re, sys
datum, cb, s0 = sys.argv[1:4]
anker = "Ergebnis siehe `p_probe.txt`) |"
bz = " · **KI-Forschung BA3 mit TB-179 (⟨DATUM⟩, Journal ⟨Kennung⟩)**: `ki_forschung/regeln/` (sammler, filter, regime_bot, rotations_bot, nachrichten_bot; v1) und `ki_forschung/prompts/` (Prompts + `manifest.json` mit sha256, Modell Haiku, Deckel je Topf), Regel-Test ⟨NR⟩/0 und Wachen-Test ⟨N⟩/0 (`json` in der Positivliste), Commit ⟨Commit B⟩; Regelblätter per Karte bestätigt; kein Abruf, kein API-Aufruf, kein Handelscode; **offen: Startkapital-Ort (R110 (b), TB-180), Feeds und F6-Termine vor dem ersten Lauf, Auswerteplan (R108 (b))**; nächste: BA2 Sammler, BA4 drei KI-Bots, BA5 Filtervergleich, BA7 am Mac"
jb = "## ⟨Kennung⟩ — TB-179: KI-Forschung BA3 (Regelblätter, Fragenkatalog v1, Prompts mit Manifest, Regel-Test)\n*Quelle: `docs/ERGEBNIS_TB-179_ki_forschung_ba3.md`, Auftrag `docs/auftraege/MAC_TB-179_ki_forschung_ba3.md`, Belege `docs/belege/TB-179/`, Commits `⟨S0⟩` (S0, Auftrag) und `⟨Commit B⟩` (B, Regelblätter, Prompts, Test), danach der Abgabe-Commit.*\n\n### Was gemessen ist\n- B: fünf Regelblätter, Prompts und `manifest.json` unter `ki_forschung/`, `test_ki_regeln.py` neu, eine Zeile in `test_ki_wachen.py`; sha256 wie Soll (`b_sha.txt`, rc 0).\n- T: Regel-Test ⟨NR⟩ Prüfungen, FEHLT 0 (`t_regeln.txt`); Wachen-Test ⟨N⟩ Prüfungen, FEHLT 0 (`t_wachen.txt`); `t_status.txt` ohne `.db`, ohne `__pycache__`.\n- Kein Abruf, kein API-Aufruf, kein Schlüssel; `shared/`, `strategies/`, `notifications/` unverändert (`f_numstat.txt`).\n\n### Was offen bleibt\n- Startkapital-Ort nach R110 (b) (`shared/handelskosten.py`, TB-180); Feed-Adressen und F6-Termine vor dem ersten Lauf; Auswerteplan nach R108 (b); alle „Vorschlag“-Werte gelten mit der Karte.\n- BA2 Sammler, BA4 drei KI-Bots, BA5 Filtervergleich, BA6 Dashboard, BA7 am Mac.\n\n### In einfacher Sprache\nDie Spielregeln der KI-Versuche stehen jetzt fest im Repo, jede Anweisung an das Modell mit Fingerabdruck; ein Test schlägt an, wenn sich auch nur ein Zeichen ändert. Gehandelt und bezahlt wird noch nichts.\n\n*Geschrieben ⟨DATUM⟩ von der Mac-Sitzung TB-179. Quellenvermerk: siehe Kopf.*\n\n---\n\n"
n = 0; nein = 0
def p(name, ok):
    global n, nein
    n += 1; nein += 0 if ok else 1; print(('ja   ' if ok else 'NEIN ') + name)
N = re.findall(r'^Pruefungen: (\d+), FEHLT: 0$', open('docs/belege/TB-179/t_wachen.txt', encoding='utf-8').read(), re.M)
NR = re.findall(r'^Pruefungen: (\d+), FEHLT: 0$', open('docs/belege/TB-179/t_regeln.txt', encoding='utf-8').read(), re.M)
BLp, JLp = 'docs/projektfuehrung/BACKLOG.md', 'docs/projektfuehrung/JOURNAL.md'
bl = open(BLp, encoding='utf-8').read().split('\n'); jl = open(JLp, encoding='utf-8').read()
r1 = [i for i, l in enumerate(bl) if l.startswith('| **1** | **TB-30b')]
ken = re.findall(r'(?m)^## ([A-Z]{2}) \u2014 ', jl)
def weiter(k): return k[0] + chr(ord(k[1]) + 1) if k[1] != 'Z' else chr(ord(k[0]) + 1) + 'A'
neu = weiter(ken[-1]) if ken else '??'
ok = len(r1) == 1 and bl[r1[0]].endswith(anker) and len(N) == 1 and len(NR) == 1 and re.fullmatch('[0-9a-f]{7}', cb) and re.fullmatch('[0-9a-f]{7}', s0) and jl.count('\n## Wiederkehrende Lehren\n') == 1 and ('## ' + neu + ' \u2014 ') not in jl
p('Vorbedingungen (Rang-1-Anker, t_wachen, t_regeln, Commits, Journal-Anker, Kennung %s frei)' % neu, ok)
if ok:
    f = lambda t: t.replace('\u27e8DATUM\u27e9', datum).replace('\u27e8Kennung\u27e9', neu).replace('\u27e8Commit B\u27e9', cb).replace('\u27e8S0\u27e9', s0).replace('\u27e8NR\u27e9', NR[0]).replace('\u27e8N\u27e9', N[0])
    zeile, block = f(bz), f(jb)
    p('keine Platzhalter mehr', '\u27e8' not in zeile + block)
    bl[r1[0]] = bl[r1[0]][:-2] + zeile + ' |'; open(BLp, 'w', encoding='utf-8').write('\n'.join(bl))
    jl2 = jl.replace('\n## Wiederkehrende Lehren\n', '\n' + block + '## Wiederkehrende Lehren\n'); open(JLp, 'w', encoding='utf-8').write(jl2)
    p('BACKLOG: Zeile genau einmal, Rang 1 endet mit " |"', open(BLp, encoding='utf-8').read().count(zeile) == 1 and open(BLp, encoding='utf-8').read().split('\n')[r1[0]].endswith(zeile + ' |'))
    p('BACKLOG: Zeilenzahl gleich', len(open(BLp, encoding='utf-8').read().split('\n')) == len(bl))
    p('Journal: Block %s genau einmal, vor Wiederkehrende Lehren' % neu, jl2.count('## ' + neu + ' \u2014 TB-179') == 1 and jl2.index('## ' + neu + ' \u2014 TB-179') < jl2.index('\n## Wiederkehrende Lehren\n'))
    p('Journal: alter Inhalt unveraendert (nur eingefuegt)', jl2.replace(block, '', 1) == jl)
print('Kennung ' + neu); print('Pruefungen: %d, NEIN: %d' % (n, nein)); raise SystemExit(1 if nein else 0)
PYEOF
} > docs/belege/TB-179/a_backlog_journal.txt 2>&1; echo "rc $?" >> docs/belege/TB-179/a_backlog_journal.txt
```

Dann `git add` mit Namen für `docs/ERGEBNIS_TB-179_ki_forschung_ba3.md`, `docs/projektfuehrung/BACKLOG.md`, `docs/projektfuehrung/JOURNAL.md`, `docs/belege/TB-179/a_backlog_journal.txt`; Commit `TB-179 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩` (Kennung aus `a_backlog_journal.txt`), pushen.

**F.**

```
git status --porcelain > "$TMPDIR/tb179_f.txt"
cp "$TMPDIR/tb179_f.txt" docs/belege/TB-179/f_porcelain.txt
git diff --numstat ⟨S0⟩ HEAD > docs/belege/TB-179/f_numstat.txt
git add docs/belege/TB-179/f_porcelain.txt
git add docs/belege/TB-179/f_numstat.txt
git commit -q -m "TB-179 F: porcelain und numstat"
git push -q origin main
```

Soll: `f_porcelain.txt` leer; `f_numstat.txt` nennt neben `docs/` genau die 17 neuen Dateien und `ki_forschung/test_ki_wachen.py` (1 Zeile hinzu, 1 weg); kein Pfad unter `strategies/`, `shared/`, `notifications/`, `data/`, `config/`, `research/`.

## Kurzfassungen (für das Ergebnis, einfache Sprache)

- **Sammler:** Jeden Morgen fragt der Sammler das KI-Modell sechs feste Fragen zu Krypto und zu Aktien (Risikoneigung, Trend, Schwankung, Makro, Liquidität, Termine), Antwort je −2 bis +2 mit kurzer Begründung. Er liest nur vorher eingefrorene Marktdaten, nie die Bots. Fällt ein Tag aus, bleibt er leer. Kosten geschätzt 0,75 $ im Monat.
- **Filter:** Steht die Risikoneigung eines Markts auf −2, wird nur nachgerechnet, was gewesen wäre, wenn die Bots dieses Markts an dem Tag nicht neu eingestiegen wären; die neun handeln unverändert. Verglichen werden gesperrte Einstiege, ihr Gewinn oder Verlust, Endstand und tiefster Rückgang mit und ohne Sperre, am 30.04.2027. Nur Bericht, nie Zulassungsgrund.
- **Regime-Bot:** Fragt jeden Morgen selbst, ob Bitcoin und der S&P 500 (UCITS-ETF) eher steigen oder fallen. Bei +1/+2 ist die jeweilige Hälfte des Papierkapitals investiert, bei −1/−2 nichts, bei 0 bleibt alles. Kein Stopp. Start 10 000, Gebühren wie die neun. Fällt das Konto 25 % unter seinen Höchststand, hört er auf. Auswertung 30.04.2027.
- **Rotations-Bot:** Jeden Montag ordnet das Modell zehn UCITS-ETFs und zehn Kryptowerte nach erwarteter Stärke, nur anhand vorher berechneter Kennzahlen. Gehalten werden je die ersten drei zu gleichen Teilen; was herausfällt, wird verkauft. Je die Hälfte von 10 000 für ETF und Krypto. Abbruch bei 25 % unter Höchststand. Auswertung 30.04.2027.
- **Nachrichten-Bot:** Täglich bewertet das Modell eingefrorene Schlagzeilen zu fünf Kryptowerten und fünf Index-ETFs mit −2 bis +2. Gekauft wird nur bei +2 und Kurs über dem 20-Tage-Schnitt, 1 000 je Kauf. Verkauft wird nach 5 Handelstagen oder bei −5 %. Start 10 000, Abbruch bei 25 % unter Höchststand, Auswertung 30.04.2027.

## Offene Entscheide (nicht in diesem Auftrag entschieden)

- **E1 Vorschläge (mit der Karte bestätigt oder geändert, sonst nicht fest):** alle ISINs und Symbole der Universen (nicht im Repo belegt; Prüfziffer im Test, Existenz und Xetra-Handel nicht geprüft); Aktien-Instrument des Regime-Bots (S&P 500 UCITS); Währung je Teiltopf (USDT/EUR); Uhrzeiten 06:15/06:30/06:45/07:00 UTC; Auswertedatum 30.04.2027; Abbruch bei 25 % unter Höchststand; Ausfallregeln (Regime 5 Tage, Rotation 2 Wochen, Filter 36 h); Filter-Nachrechnung ohne Neuanlage frei gewordenen Kapitals; Rotations-Kennzahlen; Nachrichten 10 % je Einstieg, höchstens zehn offen, Stopp auf Schlusskursbasis, Feeds, 30 Meldungen; ALFRED-Serien; F6 aus FRED-Release-Terminen; `max_tokens` 900.
- **E2 Startkapital-Ort:** nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die Blätter nennen den Wert 10 000 der neun. Trägt der Ort denselben Wert, liest BA4 ihn dort (keine v2); die KI-Bots lesen nichts aus den neun.
- **E3 Feed-Adressen (BA4) und Release-Auswahl für F6 (BA2):** werden vor dem ersten Lauf als Nachtrag mit Hash festgelegt (Vorschlag: gilt noch als v1, weil vor dem ersten Lauf, R108 (b) (2)).
- **E4 Kosten (erschlossen, nicht gemessen):** Sammler rund 0,75 $/Monat; Bots rund 1,4 $/Monat (Regime 0,6, Rotation 0,05, Nachrichten 0,75); unter den Deckeln, BA7 misst.
- **E5 MI1 (b)/K24:** Regime und Rotation entscheiden rein KI; vom Betreiber nur für Paper gebrochen; Folge: nie Zulassungsgrund, nie im Selektionslauf.
- **E6 Auswerteplan (R108 (b)):** ob `filter.md` für den Filtervergleich als Auswerteplan genügt, entscheidet der Verfahrensprüfer (Vorschlag: ja für den Filter; weitere Auswertungen der Zustände brauchen einen eigenen Plan).

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V nicht `rc 0`; B nicht `rc 0` (sha256 oder alte Zeile in `test_ki_wachen.py` nicht genau einmal); T nicht wie Soll (dann Abbruchweg T, kein B-Commit); `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung.

## In einfacher Sprache

Bevor die KI-Versuche starten, werden ihre Spielregeln festgeschrieben: was der Sammler jeden Tag fragt, wann der Filter einen Einstieg der neun nur rechnerisch sperren würde, und wie die drei KI-Bots auf dem Papier kaufen und verkaufen. Jede Anweisung an das KI-Modell liegt als Datei mit Fingerabdruck (sha256) im Repo; ein Test meldet, wenn auch nur ein Zeichen davon abweicht oder eine Pflichtangabe fehlt. Heute wird nichts abgerufen, nichts bezahlt und nichts gehandelt.

## Anhänge


### Anhang A — `ki_forschung/regeln/sammler.md` (neu)

<!-- DATEI regeln/sammler.md -->
````markdown
# Regelblatt Sammler (Marktzustand) — Katalog v1

Fest vor dem ersten Lauf (R108 (b) (2)): dieses Blatt und die Prompts unter `ki_forschung/prompts/` liegen mit sha256 (`prompts/manifest.json`) im Repo, bevor der erste Lauf schreibt. Jede Änderung an Blatt, Frage oder Prompt ist Katalog v2 und beginnt eine neue Reihe. „Vorschlag“ = vom Plan nicht festgelegt, vom Bau vorgeschlagen, mit der Freigabe-Karte bestätigt oder geändert.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`, `shared/claude_client.py`); Websuche aus, `tools=None`
- **Topf:** `sammler`, Deckel 3 $ je UTC-Monat (`aufrufe.DECKEL_USD`), getrennt vom Topf `bots`
- **Märkte:** `krypto` (gilt für die fünf Krypto-Bots der neun), `aktien` (gilt für die vier Aktien-Bots der neun); Zuordnung wie `ASSET_CLASS` in `notifications/monitor.py`
- **Fragen:** sechs je Markt, in dieser Reihenfolge: F1 Risikoneigung, F2 Trend, F3 Vola-Regime, F4 Makro, F5 Liquidität, F6 Ereignisrisiko 7 Tage (Wortlaut je Frage in `prompts/sammler_f<n>_*.txt`)
- **Skala:** ganze Zahl −2, −1, 0, +1, +2 je Frage (−2 = deutlich ungünstig für Long-Risiko, 0 = neutral, +2 = deutlich günstig); dazu Zuversicht `niedrig`/`mittel`/`hoch` und Begründung höchstens 300 Zeichen, die nur eingefrorene Eingaben nennt
- **Antwortformat:** ein JSON-Objekt je Markt mit den Schlüsseln `f1` … `f6`, je `{"wert": int, "zuversicht": str, "begruendung": str}`; jede andere Antwort ist ungültig und wird als `ungueltig` gebucht (kein Wert, keine Wiederholung)
- **Quellen:** Krypto: Binance-Spot Tageskerzen BTCUSDT und ETHUSDT (letzte 200 geschlossene UTC-Tage), alternative.me Fear & Greed (letzte 30 Werte); Aktien: yfinance `^GSPC`, `^STOXX50E`, `^VIX` (letzte 200 geschlossene Handelstage); beide Märkte: ALFRED `DFF`, `T10Y2Y`, `BAMLH0A0HYM2`, `WALCL`, `DTWEXBGS` (Vorschlag: Serienauswahl) und FRED-Release-Termine der nächsten 7 Tage (Vorschlag: Quelle für F6; Release-Auswahl legt BA2 fest, bevor der erste Lauf schreibt)
- **Vintage:** jede Eingabe stammt aus `ki_forschung/abrufe.py` (`abrufe.db`, Rohkopie + sha256 + `abgerufen_utc`); der Prompt liest nur `stand(quelle, schluessel, bis=Laufzeit)`; ALFRED mit `realtime_start = realtime_end = Abruftag`; bei yfinance, Binance und Fear & Greed ist der Abruftag die Vintage (spätere Revision der Quelle ändert die Reihe nicht)
- **Lauf:** einmal je Tag, Cron am Mac, 06:15 UTC (Vorschlag), zwei Aufrufe (ein Aufruf je Markt, alle sechs Fragen in einem Aufruf), `max_tokens` 900 (Vorschlag); Kosten erschlossen 2 × 30 × rund 0,0125 $ (rund 8 000 Token Eingabe, 900 Ausgabe) = rund 0,75 $ je Monat (nicht gemessen, BA7 misst)
- **Ausfall:** fehlt eine Eingabe, greift die Bremse, ist der Notschalter `ki_sammler` gesetzt oder schläft der Mac, wird der Tag je Markt als `ausgefallen` gebucht; nichts wird nachgeholt oder geschätzt
- **Speicher:** `marktzustand/marktzustand.db` (oberste Ebene, nur anfügend; jede Zeile mit Zeitstempel, Quellen-Hash, Prompt-Hash, Katalogversion, Modell angefordert/geliefert, Tokens); Bau in BA2
- **Leseregel:** R108 (b): der Sammler liest keine Ausgabe eines Bots (`results/`, Bot-DBs, Listen, `ergebnisse/`) und schreibt nichts unter `data/`; ein Zustand ist aufgezeichnete Modellantwort, nie herleitbare Grösse; Zustände werden gegen Bot-Ergebnisse nur aus der Bestätigungsperiode gelesen, nie gegen Selektionsfalten; Auswertung ist Bericht, kein Tor. Ausnahme vom Betreiber (17.10.2026): der Filtervergleich nach `filter.md` mit vorher fester Regel
- **Prompts:** `sammler_system.txt`, `sammler_f1_risikoneigung.txt`, `sammler_f2_trend.txt`, `sammler_f3_vola_regime.txt`, `sammler_f4_makro.txt`, `sammler_f5_liquiditaet.txt`, `sammler_f6_ereignisrisiko.txt`

## Zusammenbau eines Aufrufs

System-Prompt = `sammler_system.txt`. Nachricht = Kopfzeile `Markt: <krypto|aktien>; Stand: <Laufzeit UTC>`, dann die sechs Fragetexte in der Reihenfolge F1 … F6, dann die eingefrorenen Eingaben des Markts als Tabellen (Quelle, Schlüssel, `abgerufen_utc`, sha256, Werte). Der Prompt-Hash (`aufrufe.prompt_hash`) wird je Aufruf gebucht.
````

### Anhang B — `ki_forschung/regeln/filter.md` (neu)

<!-- DATEI regeln/filter.md -->
````markdown
# Regelblatt Filter (Sperre bei Risikoneigung −2) — v1

Fest vor dem ersten Zustand (Betreiber 17.10.2026: „Regel vorher fest“; R108 (b) für diesen Vergleich vom Betreiber gebrochen). Der Filter greift **nicht** in die neun ein: er wird neben ihnen nachgerechnet und nur im Dashboard-Bereich „KI-Forschung“ gezeigt.

## Pflichtfelder

- **Version:** v1
- **Frage:** F1 Risikoneigung des Sammlers (Katalog v1, `sammler.md`), je Markt
- **Schwelle:** Sperre neuer Einstiege eines Bots, wenn der letzte gültige Zustand seines Markts vor der Einstiegszeit den Wert −2 hat; −1 bis +2 sperren nicht; bestehende Positionen und Ausstiege bleiben unberührt
- **Märkte:** `krypto` für elliott_wave, t3_supertrend, rsi2_crypto, turtle_soup_crypto, volatility_breakout_crypto; `aktien` für elliott_wave_stocks, rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout (`ASSET_CLASS`, `notifications/monitor.py`)
- **Startzeitpunkt:** die erste Sammlerzeile nach dem Commit dieses Blatts (`abgerufen_utc` des ersten gültigen Zustands); Einstiege davor werden nicht verglichen
- **Ausfall:** ist der letzte Sammlerlauf vor der Einstiegszeit `ausgefallen` oder `ungueltig`, oder älter als 36 Stunden (Vorschlag), gilt keine Sperre
- **Messgrössen:** je Bot der neun und gesamt: Zahl der Einstiege; Zahl der gesperrten Einstiege; Netto-PnL der gesperrten Einstiege (nach Gebühr und Slippage, wie der Bot sie bucht); Equity am Auswertedatum ohne und mit Filter; MaxDD ohne und mit Filter. „Mit Filter“ = Equity-Kurve des Bots ohne die gesperrten Trades (deren PnL herausgenommen; frei gewordenes Kapital wird nicht neu angelegt — Vorschlag)
- **Quelle der Bot-Zahlen:** nur lesend über `broker/bot_db.py` (`mode=ro`); Ergebnis in `ki_forschung/ki_filtervergleich.db` (Bau in BA5)
- **Auswertedatum:** 30.04.2027 (Vorschlag); Zwischenstände nur als Anzeige, ohne Urteil
- **Status:** Bericht im Bereich „KI-Forschung“, nie Zulassungsgrund, nie Tor, nie im Selektionslauf; die Zahlen werden in keiner Neuselektion zitiert (24.3); eine Regel, die daraus entsteht, ist höchstens ein Overlay-Kandidat nach 16.8 (e) mit eigener Vorregistrierung
- **Prompts:** keine (der Filter ruft kein Modell; er liest nur die Sammlerzeilen)
````

### Anhang C — `ki_forschung/regeln/regime_bot.md` (neu)

<!-- DATEI regeln/regime_bot.md -->
````markdown
# Regelblatt KI-Bot Regime — v1

Paper Trade, rein KI (MI1 (b) vom Betreiber 17.10.2026 nur für Paper gebrochen), streng getrennt von den neun: eigene DB, kein Eintrag in `ASSET_CLASS`/`discover_bots`, nie im Selektionslauf, nie Zulassungsgrund. Der Bot fragt selbst und liest den Sammler nicht. Fest vor dem Start; jede Änderung ist v2 und beginnt eine neue Reihe.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`), `tools=None`, keine Websuche
- **Topf:** `bots`, Deckel 3 $ je UTC-Monat, getrennt vom Sammler
- **Universum:** Krypto `BTCUSDT` (Binance-Spot); Aktien `IE00B5BMR087` iShares Core S&P 500 UCITS ETF (Acc), Xetra `SXR8`, EUR (Vorschlag: Instrument; ISIN aus allgemeiner Quelle, nicht im Repo belegt, vor dem Start äusserlich prüfen)
- **Entscheidungsregel:** einmal je Tag und Markt fragt der Bot das Modell nach dem Regime −2 … +2 auf eingefrorenen Eingaben (Krypto: BTCUSDT-Tageskerzen 200 Tage, Fear & Greed 30 Werte; Aktien: `^GSPC` und `^VIX` 200 Handelstage; beide: ALFRED `DFF`, `T10Y2Y`, `BAMLH0A0HYM2`); Regime ≥ +1 ⇒ long, Regime ≤ −1 ⇒ flach, 0 ⇒ keine Änderung
- **Positionsgrösse:** je Markt ein fester Teiltopf von 50 % des Startkapitals; long = Teiltopf voll investiert, flach = 0; kein Hebel, keine Leerverkäufe
- **Ausstieg:** nur über die Entscheidungsregel (Regime ≤ −1); kein Preisstopp (rein KI)
- **Startkapital:** 10 000 (Wert der neun: `STARTING_CAPITAL = 10_000.0` in allen neun `equity_simulation.py`). Ort des Startkapitals ist nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die KI-Bots lesen nichts aus den neun. Krypto-Teiltopf in USDT, Aktien-Teiltopf in EUR (Vorschlag: Währung)
- **Kosten:** wie die neun: Gebühr 0,1 % je Seite (`TRADING_FEE_PCT`), Slippage 0,05 % (`SLIPPAGE_PCT`, alle neun `forward_test.py`)
- **Ausführung:** Entscheid 06:30 UTC (Vorschlag); Krypto zum Eröffnungskurs der nächsten Binance-Spot-Stundenkerze, Aktien zum Xetra-Eröffnungskurs desselben Handelstags (an Tagen ohne Xetra-Handel: nächster Handelstag)
- **Ausfall:** ungültige oder fehlende Antwort, Bremse oder Notschalter `ki_bots` ⇒ keine Änderung, Tag als `ausgefallen` gebucht; fünf Ausfalltage in Folge ⇒ Markt flach (Vorschlag)
- **Auswertedatum:** 30.04.2027 (Vorschlag); Messgrössen: Rendite, MaxDD, Zahl der Wechsel, Kosten des Modells, Vergleich mit Halten des Instruments über denselben Zeitraum
- **Abbruchregel:** Equity fällt 25 % unter ihren Höchststand ⇒ alles flach, Bot stoppt, Bericht (Vorschlag); Änderung an Blatt oder Prompt nach dem Start ⇒ Reihe v1 endet
- **Speicher:** `ki_forschung/ki_regime.db` (nur anfügend; nie `paper_trading_*`); Bau in BA4
- **Prompts:** `regime_bot.txt`
````

### Anhang D — `ki_forschung/regeln/rotations_bot.md` (neu)

<!-- DATEI regeln/rotations_bot.md -->
````markdown
# Regelblatt KI-Bot Rotation — v1

Paper Trade, rein KI (MI1 (b) vom Betreiber 17.10.2026 nur für Paper gebrochen), streng getrennt von den neun: eigene DB, kein Eintrag in `ASSET_CLASS`/`discover_bots`, nie im Selektionslauf, nie Zulassungsgrund. Fest vor dem Start; jede Änderung ist v2 und beginnt eine neue Reihe.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`), `tools=None`, keine Websuche
- **Topf:** `bots`, Deckel 3 $ je UTC-Monat, getrennt vom Sammler
- **Universum:** ETF (nur UCITS, Xetra, EUR; Vorschlag: Auswahl, ISIN aus allgemeiner Quelle, nicht im Repo belegt, vor dem Start äusserlich prüfen): `IE00B4L5Y983` iShares Core MSCI World (EUNL); `IE00B5BMR087` iShares Core S&P 500 (SXR8); `IE00B53SZB19` iShares Nasdaq 100 (SXRV); `IE00B53L3W79` iShares Core EURO STOXX 50 Acc (SXRT); `DE0005933931` iShares Core DAX (EXS1); `IE00B4L5YX21` iShares Core MSCI Japan IMI (SJPA); `IE00BKM4GZ66` iShares Core MSCI EM IMI (IS3N); `IE00B52MJY50` iShares Core MSCI Pacific ex Japan (SXR1); `IE00BF4RFH31` iShares MSCI World Small Cap (IUSN); `IE00B3WJKG14` iShares S&P 500 Information Technology Sector (QDVE). Krypto (Binance-Spot, Vorschlag: Auswahl): `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`, `DOGEUSDT`, `AVAXUSDT`, `LINKUSDT`, `DOTUSDT`
- **Entscheidungsregel:** jeden Montag je Universum ein Aufruf: das Modell ordnet die zehn Werte nach erwarteter relativer Stärke für die nächste Woche, nur auf eingefrorenen Kennzahlen, die vor dem Aufruf aus den Kursen berechnet werden (Rendite 4, 12, 26 Wochen; Volatilität 20 Tage; Abstand zum SMA 50 und SMA 200; Vorschlag: Kennzahlen); gehalten werden die ersten drei
- **Positionsgrösse:** je Universum ein Teiltopf von 50 % des Startkapitals; die drei Werte je ein Drittel des Teiltopfs, wöchentlich auf gleiche Gewichte zurückgesetzt
- **Ausstieg:** ein Wert fällt am Montag aus den ersten drei ⇒ Verkauf; kein Preisstopp (rein KI)
- **Startkapital:** 10 000 (Wert der neun: `STARTING_CAPITAL = 10_000.0` in allen neun `equity_simulation.py`). Ort des Startkapitals ist nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die KI-Bots lesen nichts aus den neun. Krypto-Teiltopf in USDT, ETF-Teiltopf in EUR (Vorschlag: Währung)
- **Kosten:** wie die neun: Gebühr 0,1 % je Seite (`TRADING_FEE_PCT`), Slippage 0,05 % (`SLIPPAGE_PCT`)
- **Ausführung:** Entscheid montags 06:45 UTC (Vorschlag); Krypto zum Eröffnungskurs der nächsten Binance-Spot-Stundenkerze, ETF zum Xetra-Eröffnungskurs desselben Tags (Feiertag: nächster Handelstag)
- **Ausfall:** ungültige Antwort (nicht genau zehn verschiedene Werte des Universums) oder fehlender Aufruf ⇒ Bestand bleibt eine Woche, Woche als `ausgefallen` gebucht; zwei Ausfallwochen in Folge ⇒ Teiltopf flach (Vorschlag)
- **Auswertedatum:** 30.04.2027 (Vorschlag); Messgrössen: Rendite, MaxDD, Umschlag, Kosten des Modells, Vergleich mit gleichgewichtetem Halten aller zehn
- **Abbruchregel:** Equity fällt 25 % unter ihren Höchststand ⇒ alles flach, Bot stoppt, Bericht (Vorschlag); Änderung an Blatt, Universum oder Prompt nach dem Start ⇒ Reihe v1 endet
- **Speicher:** `ki_forschung/ki_rotation.db` (nur anfügend; nie `paper_trading_*`); Bau in BA4
- **Prompts:** `rotations_bot.txt`
````

### Anhang E — `ki_forschung/regeln/nachrichten_bot.md` (neu)

<!-- DATEI regeln/nachrichten_bot.md -->
````markdown
# Regelblatt KI-Bot Nachrichten — v1

Paper Trade, KI mit Preisbedingung (MI1 (b) vom Betreiber 17.10.2026 nur für Paper gebrochen), streng getrennt von den neun: eigene DB, kein Eintrag in `ASSET_CLASS`/`discover_bots`, nie im Selektionslauf, nie Zulassungsgrund. Einziger Bot mit RSS. Fest vor dem Start; jede Änderung ist v2 und beginnt eine neue Reihe.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`), `tools=None`, keine Websuche
- **Topf:** `bots`, Deckel 3 $ je UTC-Monat, getrennt vom Sammler
- **Universum:** Krypto (Binance-Spot, Vorschlag: Auswahl): `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `BNBUSDT`; ETF (nur UCITS, Xetra, EUR; Vorschlag: Auswahl, ISIN aus allgemeiner Quelle, nicht im Repo belegt, vor dem Start äusserlich prüfen): `IE00B5BMR087` S&P 500 (SXR8), `IE00B53SZB19` Nasdaq 100 (SXRV), `IE00B53L3W79` EURO STOXX 50 (SXRT), `DE0005933931` DAX (EXS1), `IE00BKM4GZ66` MSCI EM IMI (IS3N)
- **Nachrichtenquelle:** RSS, je Lauf eingefroren über `abrufe.py` (Quelle `rss`); Vorschlag: CoinDesk und Cointelegraph (Krypto), Yahoo-Finance-Schlagzeilen je Index (ETF); Feed-Adressen legt BA4 fest, bevor der erste Lauf schreibt; nur Titel und Kurztext der letzten 24 Stunden, höchstens 30 Meldungen je Symbol (Vorschlag)
- **Entscheidungsregel:** einmal je Tag und Symbol bewertet das Modell die eingefrorenen Meldungen mit −2 … +2; Einstieg long, wenn Wert = +2 **und** Schlusskurs des Vortags > SMA 20 (Tageskerzen, eingefroren); sonst kein Einstieg; höchstens eine offene Position je Symbol
- **Positionsgrösse:** 10 % des Startkapitals je Einstieg (1 000), höchstens zehn offene Positionen (Vorschlag)
- **Ausstieg:** nach 5 Handelstagen zum Eröffnungskurs, oder vorher bei −5 % gegen den Einstiegskurs (Stopp, auf Schlusskursbasis geprüft — Vorschlag: Prüfweise); der Ausstieg braucht kein Modell
- **Startkapital:** 10 000 (Wert der neun: `STARTING_CAPITAL = 10_000.0` in allen neun `equity_simulation.py`). Ort des Startkapitals ist nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die KI-Bots lesen nichts aus den neun. Krypto-Teil in USDT, ETF-Teil in EUR (Vorschlag: Währung)
- **Kosten:** wie die neun: Gebühr 0,1 % je Seite (`TRADING_FEE_PCT`), Slippage 0,05 % (`SLIPPAGE_PCT`)
- **Ausführung:** Entscheid 07:00 UTC (Vorschlag); Krypto zum Eröffnungskurs der nächsten Binance-Spot-Stundenkerze, ETF zum Xetra-Eröffnungskurs desselben Handelstags
- **Ausfall:** ungültige oder fehlende Antwort, leerer Feed, Bremse oder Notschalter `ki_bots` ⇒ kein Einstieg an diesem Tag, gebucht als `ausgefallen`; Ausstiege laufen weiter
- **Auswertedatum:** 30.04.2027 (Vorschlag); Messgrössen: Zahl der Einstiege, Trefferquote, Netto-PnL, MaxDD, Kosten des Modells, Vergleich mit derselben Preisbedingung ohne Nachrichtenwert (Kurs > SMA 20 allein)
- **Abbruchregel:** Equity fällt 25 % unter ihren Höchststand ⇒ alles flach, Bot stoppt, Bericht (Vorschlag); Änderung an Blatt, Universum, Feeds oder Prompt nach dem Start ⇒ Reihe v1 endet
- **Speicher:** `ki_forschung/ki_nachrichten.db` (nur anfügend; nie `paper_trading_*`); Bau in BA4
- **Prompts:** `nachrichten_bot.txt`
````

### Anhang F — `ki_forschung/prompts/nachrichten_bot.txt` (neu)

<!-- DATEI prompts/nachrichten_bot.txt -->
````text
Du bist der Nachrichten-Bot eines Paper-Trading-Forschungsprojekts (v1). Du bewertest die eingefrorenen Meldungen der letzten 24 Stunden zu genau einem Wert.

Regeln:
- Nutze ausschliesslich die Meldungen in der Nachricht (Titel, Kurztext, Quelle, Abrufzeit). Kein Wissen über Ereignisse nach dem genannten Stand, keine Kursprognose aus eigenem Wissen.
- Bewerte, wie die Meldungen in Summe auf den Kurs des Werts in den nächsten fünf Handelstagen wirken: -2 = deutlich negativ, -1 = eher negativ, 0 = neutral, ohne Bezug oder keine Meldungen, +1 = eher positiv, +2 = deutlich positiv.
- Begründung höchstens 300 Zeichen, mit Bezug auf die Meldungen.

Antworte nur mit einem JSON-Objekt, ohne Text davor oder danach:
{"wert": 0, "zuversicht": "mittel", "begruendung": "..."}
````

### Anhang G — `ki_forschung/prompts/regime_bot.txt` (neu)

<!-- DATEI prompts/regime_bot.txt -->
````text
Du bist der Regime-Bot eines Paper-Trading-Forschungsprojekts (v1). Du beurteilst einmal am Tag das Marktregime genau eines Markts.

Regeln:
- Nutze ausschliesslich die eingefrorenen Eingaben in der Nachricht (Kurse, Stimmungsindex, Makroreihen mit Abrufzeit). Kein Wissen über Ereignisse nach dem genannten Stand.
- Gib das Regime als ganze Zahl von -2 bis +2 an: -2 = klar abwärts / risikoarm halten, -1 = eher abwärts, 0 = unklar, +1 = eher aufwärts, +2 = klar aufwärts.
- Begründung höchstens 300 Zeichen, nur mit Werten aus den Eingaben.

Antworte nur mit einem JSON-Objekt, ohne Text davor oder danach:
{"regime": 0, "zuversicht": "mittel", "begruendung": "..."}
````

### Anhang H — `ki_forschung/prompts/rotations_bot.txt` (neu)

<!-- DATEI prompts/rotations_bot.txt -->
````text
Du bist der Rotations-Bot eines Paper-Trading-Forschungsprojekts (v1). Einmal je Woche ordnest du ein festes Universum von zehn Werten.

Regeln:
- Nutze ausschliesslich die Kennzahlentabelle in der Nachricht (Rendite 4, 12, 26 Wochen; Volatilität 20 Tage; Abstand zum SMA 50 und SMA 200; Stand der Daten). Kein Wissen über Ereignisse nach dem genannten Stand.
- Ordne alle zehn Werte nach erwarteter relativer Stärke für die nächste Woche, stärkster zuerst. Jeder Wert genau einmal, nur Kennungen aus der Tabelle.
- Begründung höchstens 300 Zeichen.

Antworte nur mit einem JSON-Objekt, ohne Text davor oder danach:
{"rangfolge": ["KENNUNG1", "KENNUNG2", "...", "KENNUNG10"], "begruendung": "..."}
````

### Anhang I — `ki_forschung/prompts/sammler_f1_risikoneigung.txt` (neu)

<!-- DATEI prompts/sammler_f1_risikoneigung.txt -->
````text
F1 Risikoneigung: Wie gross ist die Bereitschaft der Marktteilnehmer, Risiko in diesem Markt zu halten (Stimmungsindex, Risikoaufschläge, Volatilitätsindex, Verhalten nach Rückgängen)? -2 = ausgeprägte Risikoscheu, +2 = ausgeprägte Risikofreude.
````

### Anhang J — `ki_forschung/prompts/sammler_f2_trend.txt` (neu)

<!-- DATEI prompts/sammler_f2_trend.txt -->
````text
F2 Trend: Wie ist der Trend des Leitwerts über 20, 50 und 200 Tage (Lage zu den gleitenden Durchschnitten, Steigung, Hochs und Tiefs)? -2 = klarer Abwärtstrend, +2 = klarer Aufwärtstrend.
````

### Anhang K — `ki_forschung/prompts/sammler_f3_vola_regime.txt` (neu)

<!-- DATEI prompts/sammler_f3_vola_regime.txt -->
````text
F3 Vola-Regime: Wie ist die Schwankung der letzten 20 Tage im Vergleich zu den letzten 200 Tagen, und steigt oder fällt sie? -2 = hohe und steigende Schwankung, +2 = niedrige und fallende Schwankung.
````

### Anhang L — `ki_forschung/prompts/sammler_f4_makro.txt` (neu)

<!-- DATEI prompts/sammler_f4_makro.txt -->
````text
F4 Makro: Wie wirken Leitzins, Zinskurve (10 Jahre minus 2 Jahre) und Dollar laut den eingefrorenen Reihen auf diesen Markt? -2 = deutlich belastend, +2 = deutlich stützend.
````

### Anhang M — `ki_forschung/prompts/sammler_f5_liquiditaet.txt` (neu)

<!-- DATEI prompts/sammler_f5_liquiditaet.txt -->
````text
F5 Liquidität: Wie entwickeln sich Notenbankbilanz, Kreditaufschläge und Handelsvolumen laut den Eingaben? -2 = deutlich straffer werdend, +2 = deutlich lockerer werdend.
````

### Anhang N — `ki_forschung/prompts/sammler_f6_ereignisrisiko.txt` (neu)

<!-- DATEI prompts/sammler_f6_ereignisrisiko.txt -->
````text
F6 Ereignisrisiko 7 Tage: Stehen in den nächsten 7 Tagen laut der eingefrorenen Terminliste Veröffentlichungen an, die diesen Markt stark bewegen können? -2 = mehrere gewichtige Termine, +2 = keine gewichtigen Termine. Ohne Terminliste: 0, Zuversicht niedrig.
````

### Anhang O — `ki_forschung/prompts/sammler_system.txt` (neu)

<!-- DATEI prompts/sammler_system.txt -->
````text
Du bist der Marktzustands-Sammler eines Forschungsprojekts (Katalog v1). Du beantwortest sechs feste Fragen zu genau einem Markt.

Regeln:
- Nutze ausschliesslich die Eingaben in der Nachricht. Kein Wissen über Ereignisse nach dem genannten Stand, keine Vermutung über Kurse, die nicht in den Eingaben stehen.
- Jede Frage bekommt eine ganze Zahl von -2 bis +2: -2 = deutlich ungünstig für Long-Risiko in diesem Markt, -1 = eher ungünstig, 0 = neutral oder unklar, +1 = eher günstig, +2 = deutlich günstig.
- Dazu je Frage eine Zuversicht ("niedrig", "mittel" oder "hoch") und eine Begründung von höchstens 300 Zeichen, die nur Werte aus den Eingaben nennt.
- Fehlen die Eingaben für eine Frage, antworte 0 mit Zuversicht "niedrig" und nenne die fehlende Eingabe.

Antworte nur mit einem JSON-Objekt, ohne Text davor oder danach:
{"f1": {"wert": 0, "zuversicht": "mittel", "begruendung": "..."}, "f2": {...}, "f3": {...}, "f4": {...}, "f5": {...}, "f6": {...}}
````

### Anhang P — `ki_forschung/prompts/manifest.json` (neu)

<!-- DATEI prompts/manifest.json -->
````json
{
 "version": "v1",
 "modell": "claude-haiku-4-5-20251001",
 "deckel_usd_je_monat": {
  "sammler": 3.0,
  "bots": 3.0
 },
 "websuche": "aus",
 "entstanden": "TB-179 (BA3)",
 "prompts": {
  "nachrichten_bot.txt": {
   "sha256": "d7e6532dedc270c8d08d5dad6ca7227515948b86a3fb64d26c14ee5c4b85ae54",
   "verbraucher": "nachrichten_bot",
   "topf": "bots"
  },
  "regime_bot.txt": {
   "sha256": "f6ab08a6dfc5321136c3b715f5e93c44173dc02bcbc0533c7a05211b769d33bc",
   "verbraucher": "regime_bot",
   "topf": "bots"
  },
  "rotations_bot.txt": {
   "sha256": "9641a17bdf193eb687a6779918c6a91ea04c1f2ebfa58f851b16cd96795fd339",
   "verbraucher": "rotations_bot",
   "topf": "bots"
  },
  "sammler_f1_risikoneigung.txt": {
   "sha256": "8657c39a39c5719a775db6d45cd5f8734e01c27425debe0f2cda0673a3a89242",
   "verbraucher": "sammler",
   "topf": "sammler"
  },
  "sammler_f2_trend.txt": {
   "sha256": "8c2c15ca26dea29fa5e8b8489feb8f8585ae69d314197a15eb782033f2813c85",
   "verbraucher": "sammler",
   "topf": "sammler"
  },
  "sammler_f3_vola_regime.txt": {
   "sha256": "2eb59a1cf257835ddbb9b6a4d215fe18c062b9a095850063ddc6a5eae5f137f9",
   "verbraucher": "sammler",
   "topf": "sammler"
  },
  "sammler_f4_makro.txt": {
   "sha256": "3eb0022cd60567cfc50ed7af983ee5daab7a91c8533c76a80d45a664af550744",
   "verbraucher": "sammler",
   "topf": "sammler"
  },
  "sammler_f5_liquiditaet.txt": {
   "sha256": "8d42479b8cb10e324686225e874edd3ca43e37fe4eb4a56633422bdd8d9b7d85",
   "verbraucher": "sammler",
   "topf": "sammler"
  },
  "sammler_f6_ereignisrisiko.txt": {
   "sha256": "d9c1ae746ad45ecd748d20701a23ffb7afd80698b9fd66bf252942e0a90f4e67",
   "verbraucher": "sammler",
   "topf": "sammler"
  },
  "sammler_system.txt": {
   "sha256": "2ca4331535326ff1ac7e1b6dd860058cb45ebaa8c5490484e77551f634b4bd10",
   "verbraucher": "sammler",
   "topf": "sammler"
  }
 },
 "regeln": {
  "filter.md": {
   "sha256": "567c469ba8495776bc1d1f12347f605971b64ce54367521f98febe1d4faa38ac"
  },
  "nachrichten_bot.md": {
   "sha256": "f4592c17a404530492e820f914264c8520cfedd73ee87c3870b8055152968705"
  },
  "regime_bot.md": {
   "sha256": "abe56d30393bb9a82adf506bc146fad57adc82070bb2eabb5dec50982022b070"
  },
  "rotations_bot.md": {
   "sha256": "d866551f8f06bb8f87827e3267e88d10f988b3770a96955d70bbb72e50b73bca"
  },
  "sammler.md": {
   "sha256": "a12425d493e516018b64351708b79b36a02d24e62e29faaae5bd3d5128c838b4"
  }
 }
}
````

### Anhang Q — `ki_forschung/test_ki_regeln.py` (neu)

<!-- DATEI test_ki_regeln.py -->
````python
"""
Regel-Test der KI-Forschung (TB-179, BA3)
=========================================
Prueft, dass Regelblaetter und Prompts vor jedem Start fest im Repo liegen,
ohne Netz und ohne API-Aufruf; das Repo wird nur gelesen.

R1  manifest.json: Version v1, Modell = MODEL_HAIKU aus shared/claude_client.py
    (gelesen per ast, nicht importiert).
R2  Prompts: jede Datei unter prompts/ (ausser manifest.json) steht genau einmal
    im Manifest, jeder Eintrag hat eine Datei, sha256 gleich; Topf je Eintrag
    ist ein Topf aus aufrufe.DECKEL_USD (per ast) und passt zum Verbraucher.
R3  Regelblaetter: genau die fuenf Blaetter unter regeln/, je im Manifest mit
    gleichem sha256.
R4  Pflichtfelder: jedes Blatt traegt jedes Pflichtfeld genau einmal und nicht
    leer; das Feld Prompts nennt nur Dateien des Manifests, und jeder Prompt
    gehoert zu genau einem Blatt mit gleichem Topf.
R5  Inhalt: Sammler zwei Maerkte und F1..F6 mit Prompt je Frage; Filter an
    F1 Risikoneigung, Schwelle -2, "nie Zulassungsgrund"; Bots: Modell Haiku,
    Startkapital 10 000, Auswertedatum TT.MM.JJJJ, jede ISIN mit gueltiger
    Pruefziffer und nicht aus den USA (nur UCITS), Krypto-Symbole ...USDT,
    Rotation genau zehn ETF und zehn Krypto.
R6  Prompts verlangen JSON und nennen weder Websuche noch eine Adresse.
G   Gegenproben: jede Wache wird an einer verfaelschten Kopie in einem
    temporaeren Ordner rot.

Nutzung:  python3 -B ki_forschung/test_ki_regeln.py      (Ausgang 0 = gruen)
"""
import ast
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

KI_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(KI_DIR)
ERGEBNIS = []
TEMP = []

BLAETTER = ("sammler.md", "filter.md", "regime_bot.md", "rotations_bot.md", "nachrichten_bot.md")
PFLICHT_BOT = ("Version", "Modell", "Topf", "Universum", "Entscheidungsregel", "Positionsgrösse", "Ausstieg", "Startkapital",
               "Kosten", "Ausführung", "Ausfall", "Auswertedatum", "Abbruchregel", "Speicher", "Prompts")
PFLICHT = {"sammler.md": ("Version", "Modell", "Topf", "Märkte", "Fragen", "Skala", "Antwortformat", "Quellen", "Vintage", "Lauf",
                          "Ausfall", "Speicher", "Leseregel", "Prompts"),
           "filter.md": ("Version", "Frage", "Schwelle", "Märkte", "Startzeitpunkt", "Ausfall", "Messgrössen",
                         "Quelle der Bot-Zahlen", "Auswertedatum", "Status", "Prompts"),
           "regime_bot.md": PFLICHT_BOT, "rotations_bot.md": PFLICHT_BOT, "nachrichten_bot.md": PFLICHT_BOT + ("Nachrichtenquelle",)}
TOPF_SOLL = {"sammler.md": "sammler", "regime_bot.md": "bots", "rotations_bot.md": "bots", "nachrichten_bot.md": "bots"}
FRAGEN = ("F1 Risikoneigung", "F2 Trend", "F3 Vola-Regime", "F4 Makro", "F5 Liquidität", "F6 Ereignisrisiko")
ISIN_RX = re.compile(r"\b((?:IE|LU|DE|FR|NL|GB|CH|AT|JE|US)[A-Z0-9]{9}[0-9])\b")
KRYPTO_RX = re.compile(r"`([A-Z0-9]{2,10}USDT)`")


def pruefe(name, ok, detail=""):
    ERGEBNIS.append((name, bool(ok)))
    print("  %s %s%s" % ("ok  " if ok else "FEHLT", name, ("   " + str(detail)[:300]) if detail else ""))


def lies(pfad):
    with open(pfad, encoding="utf-8") as f:
        return f.read()


def sha_datei(pfad):
    with open(pfad, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def konstante(pfad, name):
    for k in ast.walk(ast.parse(lies(pfad))):
        if isinstance(k, ast.Assign) and any(isinstance(z, ast.Name) and z.id == name for z in k.targets):
            return ast.literal_eval(k.value)
    return None


def isin_gueltig(isin):
    """Pruefziffer nach ISO 6166 (Luhn auf den in Ziffern gewandelten Zeichen)."""
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}[0-9]", isin):
        return False
    ziffern = "".join(str(int(c, 36)) for c in isin[:-1])
    summe = 0
    for i, c in enumerate(reversed(ziffern)):
        d = int(c) * (2 if i % 2 == 0 else 1)
        summe += d // 10 + d % 10
    return (10 - summe % 10) % 10 == int(isin[-1])


def felder(text):
    """Pflichtfelder: Zeilen '- **Name:** Wert' im Abschnitt '## Pflichtfelder'."""
    teil = text.split("\n## Pflichtfelder\n", 1)[1].split("\n## ", 1)[0] if "\n## Pflichtfelder\n" in text else ""
    f = {}
    for name, wert in re.findall(r"(?m)^- \*\*([^*]+):\*\* ?(.*)$", teil):
        f.setdefault(name, []).append(wert.strip())
    return f


def befunde_manifest(ki_dir, wurzel):
    b = []
    pd = os.path.join(ki_dir, "prompts")
    try:
        m = json.loads(lies(os.path.join(pd, "manifest.json")))
    except (OSError, ValueError) as e:
        return ["manifest.json nicht lesbar: %s" % e]
    haiku = konstante(os.path.join(wurzel, "shared", "claude_client.py"), "MODEL_HAIKU")
    toepfe = konstante(os.path.join(ki_dir, "aufrufe.py"), "DECKEL_USD") or {}
    if m.get("version") != "v1":
        b.append("Version %r" % m.get("version"))
    if not haiku or m.get("modell") != haiku:
        b.append("Modell %r statt %r" % (m.get("modell"), haiku))
    if m.get("deckel_usd_je_monat") != toepfe:
        b.append("Deckel im Manifest %r statt %r" % (m.get("deckel_usd_je_monat"), toepfe))
    pr = m.get("prompts", {})
    da = sorted(x for x in os.listdir(pd) if x != "manifest.json")
    b += ["Prompt ohne Eintrag: " + x for x in da if x not in pr]
    for name, e in sorted(pr.items()):
        p = os.path.join(pd, name)
        if not os.path.isfile(p):
            b.append("Eintrag ohne Datei: " + name)
            continue
        if sha_datei(p) != e.get("sha256"):
            b.append("sha256 weicht ab: prompts/" + name)
        if e.get("topf") not in toepfe:
            b.append("Topf %r unbekannt: %s" % (e.get("topf"), name))
        if (e.get("topf") == "sammler") != (e.get("verbraucher") == "sammler"):
            b.append("Topf passt nicht zum Verbraucher: " + name)
    rg = m.get("regeln", {})
    rd = os.path.join(ki_dir, "regeln")
    da = sorted(os.listdir(rd)) if os.path.isdir(rd) else []
    if da != sorted(BLAETTER):
        b.append("regeln/ enthaelt %s" % da)
    if sorted(rg) != sorted(BLAETTER):
        b.append("Manifest-Regeln %s" % sorted(rg))
    for name in BLAETTER:
        p = os.path.join(rd, name)
        if os.path.isfile(p) and sha_datei(p) != rg.get(name, {}).get("sha256"):
            b.append("sha256 weicht ab: regeln/" + name)
    return b


def befunde_blaetter(ki_dir, wurzel):
    b = []
    try:
        m = json.loads(lies(os.path.join(ki_dir, "prompts", "manifest.json")))
    except (OSError, ValueError) as e:
        return ["manifest.json nicht lesbar: %s" % e]
    haiku = konstante(os.path.join(wurzel, "shared", "claude_client.py"), "MODEL_HAIKU") or "?"
    pr = m.get("prompts", {})
    besitzer = {}
    for name in BLAETTER:
        p = os.path.join(ki_dir, "regeln", name)
        if not os.path.isfile(p):
            b.append("Blatt fehlt: " + name)
            continue
        t = lies(p)
        f = felder(t)
        for feld in PFLICHT[name]:
            w = f.get(feld, [])
            if len(w) != 1 or len(w[0]) < 2:
                b.append("%s: Pflichtfeld %s %s" % (name, feld, "fehlt" if not w else ("doppelt" if len(w) > 1 else "leer")))
        pz = f.get("Prompts", [""])[0]
        for d in re.findall(r"`([^`]+\.txt)`", pz):
            if d not in pr:
                b.append("%s nennt %s, nicht im Manifest" % (name, d))
            besitzer.setdefault(d, []).append(name)
            if name in TOPF_SOLL and pr.get(d, {}).get("topf") != TOPF_SOLL[name]:
                b.append("%s: Topf von %s ist %r" % (name, d, pr.get(d, {}).get("topf")))
        for i in ISIN_RX.findall(t):
            if not isin_gueltig(i):
                b.append("%s: ISIN %s Pruefziffer falsch" % (name, i))
            elif i.startswith("US"):
                b.append("%s: US-ISIN %s (nur UCITS)" % (name, i))
        if name in TOPF_SOLL:
            if haiku not in f.get("Modell", [""])[0]:
                b.append("%s: Modell nicht %s" % (name, haiku))
            if "`%s`" % TOPF_SOLL[name] not in f.get("Topf", [""])[0]:
                b.append("%s: Topf nicht %s" % (name, TOPF_SOLL[name]))
        if name.endswith("_bot.md"):
            if "10 000" not in f.get("Startkapital", [""])[0]:
                b.append("%s: Startkapital nicht 10 000" % name)
            if not re.search(r"\b\d{2}\.\d{2}\.\d{4}\b", f.get("Auswertedatum", [""])[0]):
                b.append("%s: Auswertedatum ohne Datum" % name)
            u = f.get("Universum", [""])[0]
            if not KRYPTO_RX.findall(u) and not ISIN_RX.findall(u):
                b.append("%s: Universum ohne Symbol" % name)
            if name == "rotations_bot.md" and (len(set(ISIN_RX.findall(u))) != 10 or len(set(KRYPTO_RX.findall(u))) != 10):
                b.append("rotations_bot.md: nicht genau 10 ETF und 10 Krypto")
        if name == "sammler.md":
            fr = f.get("Fragen", [""])[0]
            b += ["sammler.md: Frage fehlt: " + q for q in FRAGEN if q not in fr]
            mk = f.get("Märkte", [""])[0]
            b += ["sammler.md: Markt fehlt: " + q for q in ("`krypto`", "`aktien`") if q not in mk]
            for n in range(1, 7):
                if not [d for d in pr if d.startswith("sammler_f%d_" % n)]:
                    b.append("sammler.md: kein Prompt fuer F%d" % n)
        if name == "filter.md":
            if "nie Zulassungsgrund" not in f.get("Status", [""])[0]:
                b.append("filter.md: Status ohne 'nie Zulassungsgrund'")
            if "F1 Risikoneigung" not in f.get("Frage", [""])[0]:
                b.append("filter.md: Frage nicht F1 Risikoneigung")
            if "−2" not in f.get("Schwelle", [""])[0]:
                b.append("filter.md: Schwelle nicht −2")
            if not re.search(r"\b\d{2}\.\d{2}\.\d{4}\b", f.get("Auswertedatum", [""])[0]):
                b.append("filter.md: Auswertedatum ohne Datum")
    for d in pr:
        if len(besitzer.get(d, [])) != 1:
            b.append("Prompt %s gehoert zu %s" % (d, besitzer.get(d, [])))
    return b


def befunde_prompts(ki_dir):
    b = []
    pd = os.path.join(ki_dir, "prompts")
    for d in sorted(x for x in os.listdir(pd) if x.endswith(".txt")):
        t = lies(os.path.join(pd, d))
        if d.startswith("sammler_f"):
            continue
        if "JSON" not in t:
            b.append(d + ": verlangt kein JSON")
    for d in sorted(x for x in os.listdir(pd) if x.endswith(".txt")):
        t = lies(os.path.join(pd, d)).lower()
        b += ["%s nennt %r" % (d, w) for w in ("web_search", "websuche", "http://", "https://") if w in t]
    return b


def verfaelschen(datei, alt, neu):
    k = tempfile.mkdtemp(prefix="tb179_gp_")
    TEMP.append(k)
    ziel = os.path.join(k, "ki_forschung")
    shutil.copytree(KI_DIR, ziel, ignore=shutil.ignore_patterns("__pycache__", "*.db"))
    p = os.path.join(ziel, datei)
    if alt is None:
        with open(p, "w", encoding="utf-8") as f:
            f.write(neu)
    else:
        t = lies(p)
        assert t.count(alt) == 1, (datei, alt)
        with open(p, "w", encoding="utf-8") as f:
            f.write(t.replace(alt, neu))
    return ziel


def main():
    print("Regel-Test KI-Forschung (TB-179)")
    b = befunde_manifest(KI_DIR, REPO)
    pruefe("R1-R3 Manifest: Modell, Prompts und Regelblaetter mit sha256", not b, b)
    b = befunde_blaetter(KI_DIR, REPO)
    pruefe("R4-R5 Regelblaetter: Pflichtfelder und Inhalt (%d Blaetter)" % len(BLAETTER), not b, b)
    b = befunde_prompts(KI_DIR)
    pruefe("R6 Prompts: JSON verlangt, keine Websuche, keine Adresse", not b, b)
    gp = [("G1 Prompt um ein Zeichen geaendert", befunde_manifest, ("prompts/regime_bot.txt", "von -2 bis +2", "von -2 bis +3")),
          ("G2 Prompt ohne Manifest-Eintrag", befunde_manifest, ("prompts/zusatz.txt", None, "Antworte als JSON.\n")),
          ("G3 Modell im Manifest getauscht", befunde_manifest, ("prompts/manifest.json", '"modell": "', '"modell": "claude-sonnet-5x')),
          ("G4 Regelblatt nach dem Hash geaendert", befunde_manifest, ("regeln/filter.md", "36 Stunden", "37 Stunden")),
          ("G5 Pflichtfeld Ausstieg entfernt", befunde_blaetter, ("regeln/regime_bot.md", "- **Ausstieg:**", "- Ausstieg:")),
          ("G6 ISIN mit falscher Pruefziffer", befunde_blaetter, ("regeln/regime_bot.md", "`IE00B5BMR087`", "`IE00B5BMR088`")),
          ("G7 US-ETF im Universum", befunde_blaetter, ("regeln/regime_bot.md", "`IE00B5BMR087`", "`US78462F1030`")),
          ("G8 'nie Zulassungsgrund' entfernt", befunde_blaetter, ("regeln/filter.md", "nie Zulassungsgrund", "kein Zulassungsgrund")),
          ("G9 Rotation mit neun Krypto", befunde_blaetter, ("regeln/rotations_bot.md", ", `DOTUSDT`", "")),
          ("G10 Pflichtfeld doppelt", befunde_blaetter, ("regeln/sammler.md", "- **Version:** v1\n", "- **Version:** v1\n- **Version:** v2\n")),
          ("G11 Websuche im Prompt", befunde_prompts, ("prompts/nachrichten_bot.txt", "Kein Wissen", "Nutze web_search. Kein Wissen"))]
    for name, fn, (datei, alt, neu) in gp:
        k = verfaelschen(datei, alt, neu)
        b = fn(k, REPO) if fn is not befunde_prompts else fn(k)
        pruefe(name + " wird rot", bool(b), b[:1])
    n = len(ERGEBNIS)
    fehlt = sum(1 for _n, ok in ERGEBNIS if not ok)
    print("Pruefungen: %d, FEHLT: %d" % (n, fehlt))
    return 1 if fehlt else 0


if __name__ == "__main__":
    try:
        rc = main()
    finally:
        for d in TEMP:
            shutil.rmtree(d, ignore_errors=True)
    sys.exit(rc)
````

