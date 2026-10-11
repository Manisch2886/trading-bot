# TB-151 Eröffnungsdatei im Repo — die Eröffnung des steuernden Chats nach `docs/projektfuehrung/`, `ablage_soll.py` führt sie als B2 Stand (ein Name in `STAND`), sechs Läufe als Nachweis — an: Mac-Sitzung (Claude Code)

**Freigegeben vom steuernden Chat am 11.10.2026, 00:48 (Europe/Berlin) — Handwerk, keine Betreiberfreigabe. Entwurf des Helfers BAU151 (Nachtrag N3, Stand 10.10.2026, 22:46), berichtigt vom Helfer BER151 (11.10.2026, v4). Gegenlesen: GEGEN151 an v2 (Stempel 10.10.2026, 22:29), enger Gegenleser GEGEN151_E an den 40 Stellen v2 → v3 (Stempel 11.10.2026, 00:15), enger Gegenleser GEGEN151_E2 an den 8 Stellen v3 → v4 (Stempel 11.10.2026, 00:41).** Was als ⟨PH:…⟩ steht, setzt der steuernde Chat vor der Freigabe (sechs davon mit `fuellen.py` aus einer Messung); ⟨KENNUNG⟩, ⟨FOLGEKENNUNG⟩ und ⟨DATUM⟩ setzt die Sitzung. Die zwei Skripte sind am Gerät gelaufen: an Kopien und an einer Attrappe von `docs/` ausserhalb des Repos (Linux, Python 3.10.12, Stand `fa40ccb` samt Arbeitsbaum).

**Sitzungstitel:** `TB-151 Eröffnungsdatei im Repo` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, Base `main`, frisch von `main` am HEAD `fa40ccb9c12d3fa554676c76aa5327c12b9e68a1` (beim Bau `fa40ccb9c12d3fa554676c76aa5327c12b9e68a1`; kommt bis zum Start ein Commit dazu, baut der steuernde Chat neu) · **Angelegt:** vom steuernden Chat · **Start:** über den Sitzungswächter (`starte_TB-151`); Arbeitsbaum gemessen 11.10.2026, 00:48 (Vorbild TB-149: über den Sitzungswächter, `starte_TB-151`)
**Dieser Auftrag:** `docs/auftraege/MAC_TB-151_eroeffnungsdatei_im_repo.md`, wird in Schritt 0 mitcommittet. **Interpreter:** `trading-env/bin/python3 -B` (Python 3.9). **Rückfragen an den Betreiber** stehen samt Antwort wörtlich im Ergebnis (ARBEITSWEISE 15).
**Ziel:** Die Eröffnungsdatei liegt von git verfolgt unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, und `docs/werkzeuge/ablage_soll.py` führt sie im Soll der Ablage. Heute liegt sie nur unter `logs/` (ignoriert) und in der Ablage; das Werkzeug meldet sie als „keine Regel“, und ihr Fehlen meldet es nicht.
**Für jede Rohausgabe gilt:** Sie bleibt roh, samt Fehlertext. **Nie `git add -A`, nie `git add .`, nie `git add -f`;** jeder Pfad steht in eigener Zeile. Nach jedem fertigen Teil committen und pushen (ARBEITSWEISE 14, Regel 3). Alle Befehle laufen aus der Repo-Wurzel. **ARBEITSWEISE 7c** (Sicherung der `*.db`, Datenstand, Basislauf) ist nicht einschlägig: kein Lauf gegen Daten, keine db.

## ⭐⭐ Freigabe

**Freigabeklasse: Handwerk, Entscheid des steuernden Chats. Keine Betreiberfreigabe nötig:** kein Register, keine Sperrliste, kein Signalpfad, keine Parameterdatei.

**Entscheid des steuernden Chats (10.10.2026, Weg A):** Die Eröffnungsdatei liegt verfolgt im Repo unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und ist Klasse B2 Stand (ARBEITSWEISE 23.2: Repo und Ablage, eine Fassung ohne Datum im Namen). `ablage_soll.py` bekommt nur den Namen in der Liste `STAND`, mit einem Kommentar zum Grund; keine neue Liste, kein neuer Zweig. Grund: G1 (ARBEITSWEISE 23.1: „Alles, was den Umzug überleben muss, liegt dort committet“) und `UMZUG.md` Abschnitt 4, Schritt 4 („muss mit dem Repo gleich lauten“).

**Die Sitzung darf ändern, und nichts sonst:**

| Datei | was |
|---|---|
| `docs/werkzeuge/ablage_soll.py` | eine Stelle (Z. 56), mit `aendere.py` aus Schritt B: eine Zeile ersetzt durch drei; daneben entsteht kurz `ablage_soll.py.tb151.neu` (bleibt sie liegen: nicht löschen, in keinen Commit nehmen, melden) |
| neu: `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` | unveränderte Kopie von `logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md` (Schritt C) |
| `docs/projektfuehrung/BACKLOG.md` | ein Block, wörtlich aus Anhang 1 |
| `docs/projektfuehrung/JOURNAL.md` | ein Block, wörtlich aus Anhang 2 |
| neu: `docs/belege/TB-151/…`, `docs/ERGEBNIS_TB-151_eroeffnungsdatei_im_repo.md` | Skripte, Läufe, Belege, Ergebnis |
| nicht in git: `$TMPDIR/tb151_0a.txt`, `$TMPDIR/tb151_0a_head.txt`, `$TMPDIR/tb151_d4.txt`, Ordner `$TMPDIR/tb151_*` | Zwischenablage; Ist-Listen und Listen der Läufe |

Schritt 0 committet den Ausgang, wie er im Arbeitsbaum liegt; das ist kein Ändern im Sinn dieser Liste. **Nicht erlaubt:** `UMZUG.md` und `ARBEITSWEISE.md` (die Texte zu dieser Änderung gehen als Stücke in TB-152), `docs/werkzeuge/ablage_ereignisse.json`, jedes andere Werkzeug, alles unter `logs/` (dort nur lesen), `.gitignore`, `.claude/`, Register, `research/`, `shared/`, `strategies/`. Die Sitzung holt keine Ist-Liste aus der Ablage und legt dort nichts ab; das tut der steuernde Chat.

## Belegt · erschlossen · offen

- **Belegt (am Gerät gelesen, `fa40ccb`):** `ablage_soll.py`: 290 Zeilen, 14 498 B, md5 `46c6a18024784b86561ec2486cadc863`, nur ASCII. Es liest `docs/**/*.md` aus dem Dateisystem (Z. 65), nicht aus git, und schreibt nur nach `--aus` (Z. 272–278). Ein Name aus `STAND` steht im Soll, wenn die Datei unter `docs/` liegt (Z. 122–123); sonst heisst der Grund „B2 Stand - FEHLT IM REPO“ (Z. 130). Tests für das Skript gibt es nicht. Die Datei unter `logs/steuernder_chat/`: 13 506 B, md5 `769588e7c4234ccfe694106a40c761e5`; unter `docs/projektfuehrung/` liegt sie nicht. Simulation: Das Soll des Vorlaufs an der Attrappe ist zeilengleich mit dem Lauf am Repo (51 Zeilen).
- **Tatsachennotiz, gemessen an der Attrappe (kein Soll, kein Abbruchkriterium):** `STAND` wirkt in `ablage_soll.py` an drei Stellen (Vorfassung Z. 121–130, darin Z. 125–128, und Z. 222–224). Steht eine datierte Fassung `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT_2026-10-10.md` in der Ist-Liste, führt die Vorfassung sie unter „keine Regel“; die neue Fassung setzt sie nach `entfernen.txt`, Grund „B2 datierte Fassung - EROEFFNUNG_STEUERNDER_CHAT.md liegt im Repo“ — mit diesem Wortlaut auch dann, wenn die Datei ohne Datum nicht im Repo liegt. Liegt unter `docs/` nur eine datierte Fassung, setzt die neue Fassung diese ins Soll, Grund „B2 Stand (Uebergang: EROEFFNUNG_STEUERNDER_CHAT.md fehlt im Repo, juengste datierte Fassung)“; die Vorfassung meldet dann nichts. Unter `docs/` liegt heute keine datierte Fassung. Den Fall „Datei im Repo, datierte Fassung im Ist“ misst die Sitzung in Schritt C nach (Phase `datiert`).
- **Erschlossen:** `git add` nimmt die Datei an: `.gitignore` nennt `logs/` (Z. 27) und keine Zeile für die Datei unter `docs/` (gelesen, nicht mit git gemessen). Am Mac zählt das Soll anders als am Gerät, mindestens um diesen Auftrag, der dann unter `docs/auftraege/` liegt. Darum prüft `laeufe.py` Unterschiede und Zeilen, keine festen Zahlen.
- **Offen:** Ob bis zum Start ein Umzug die Datei unter `logs/` ersetzt; dann ist ihr md5 in 0b und in Schritt C neu zu setzen (`fuellen.py`). Ob die echte Ist-Liste die Datei mit genau dem Pfad `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` nennt, misst der steuernde Chat beim nächsten Abgleich; die Läufe hier nehmen eine künstliche Ist-Liste.

## Schritt 0 — Ausgang

**0a. Zuerst, bevor irgendetwas geschrieben oder committet wird:**

```bash
git status --porcelain > "$TMPDIR/tb151_0a.txt"
git rev-parse HEAD > "$TMPDIR/tb151_0a_head.txt"
```

Soll: in `tb151_0a_head.txt` der HEAD `fa40ccb9c12d3fa554676c76aa5327c12b9e68a1` und in `tb151_0a.txt` genau die Einträge im Block darunter (Reihenfolge egal); sonst **ABBRUCH**. Gemessen 11.10.2026, 00:48 mit `git ls-files -m`, `-d` und `-o --exclude-standard`; dazugesetzt, nicht gemessen: `docs/auftraege/AKTUELLER_AUFTRAG.md`, `docs/auftraege/MAC_TB-151_eroeffnungsdatei_im_repo.md`; Vorgemerktes (Index gegen HEAD) ist nicht gemessen.

```text
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-151_eroeffnungsdatei_im_repo.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-10a_m4_kauf_vor_handelbar_tag.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-10a_m4_widerspruch_schranke_am_einstieg.md
?? docs/projektfuehrung/FABLE_UEBERGABE_2026-10-10_eroeffnung.md
?? docs/projektfuehrung/RECHERCHE_2026-10-10_kerzenformationen.md
```

Commit von Schritt 0 mit genau diesen Pfaden ⇒ **⟨S0⟩**; die `git add`-Zeilen folgen dem Block oben. Erst danach entsteht der Belegordner; ein `cmp` ungleich ⇒ **ABBRUCH**.

```bash
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-151_eroeffnungsdatei_im_repo.md
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-10a_m4_kauf_vor_handelbar_tag.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-10a_m4_widerspruch_schranke_am_einstieg.md
git add docs/projektfuehrung/FABLE_UEBERGABE_2026-10-10_eroeffnung.md
git add docs/projektfuehrung/RECHERCHE_2026-10-10_kerzenformationen.md
git commit -m "TB-151 Schritt 0: Stand des steuernden Chats"
git push
mkdir -p docs/belege/TB-151
cp "$TMPDIR/tb151_0a.txt" docs/belege/TB-151/0a_status.txt
cmp "$TMPDIR/tb151_0a.txt" docs/belege/TB-151/0a_status.txt
cp "$TMPDIR/tb151_0a_head.txt" docs/belege/TB-151/0a_head.txt
cmp "$TMPDIR/tb151_0a_head.txt" docs/belege/TB-151/0a_head.txt
```

**0b. Skripte ablegen, Ausgang messen.** Die zwei Python-Blöcke aus Schritt A und Schritt B zeichengleich nach `docs/belege/TB-151/laeufe.py` und `docs/belege/TB-151/aendere.py` schreiben (nichts verbessern; jede Datei endet mit genau einem Zeilenende). Dann:

```bash
trading-env/bin/python3 -B -c "import hashlib,sys; [print(hashlib.md5(open(p,'rb').read()).hexdigest(), p) for p in sys.argv[1:]]" docs/belege/TB-151/laeufe.py docs/belege/TB-151/aendere.py docs/werkzeuge/ablage_soll.py logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md > docs/belege/TB-151/0b_md5.txt
```

Soll, in dieser Reihenfolge: `379f2472eb84c4bf15807f8267d60541` · `004bf1d29194d5cdc823a28be9c791f5` · `46c6a18024784b86561ec2486cadc863` · `769588e7c4234ccfe694106a40c761e5`. Weicht ein Skript ab: einmal neu schreiben und neu messen; weicht es wieder ab ⇒ **ABBRUCH**. Weicht `ablage_soll.py` oder die Datei unter `logs/` ab ⇒ **ABBRUCH**.

Danach `git status --porcelain`: Neu sind nur Dateien unter `docs/belege/TB-151/`.

## Schritt A — Vorlauf und Lauf `alt_mit` mit der Vorfassung

`docs/belege/TB-151/laeufe.py` (6 481 B). Es ruft `ablage_soll.py` auf, legt Ist-Listen und Listen in einen Ordner `$TMPDIR/tb151_*` und schreibt unter `docs/belege/TB-151/` je Lauf eine Datei `lauf_<name>.txt`, dazu einmal `ist_mit.txt`.

```python
import os, re, subprocess, sys, tempfile
SKRIPT, PHASE, ORD, HEUTE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:5]
NAME = "EROEFFNUNG_STEUERNDER_CHAT.md"
PFAD = "projektfuehrung/" + NAME
IM_REPO = os.path.exists(os.path.join("docs", "projektfuehrung", NAME))
LISTEN = ("soll.txt", "entfernen.txt", "ablegen.txt", "ohne_regel.txt")
# drei erfundene Pfade, damit auch entfernen.txt und ohne_regel.txt Zeilen fuer die Gegenprobe tragen
ZUSATZ = ["belege/TB-151/probe_b7.md", "projektfuehrung/BACKLOG_ARCHIV.md", "projektfuehrung/PROBE_TB-151_ohne_regel.md"]
TMP = tempfile.mkdtemp(prefix="tb151_")
fehler = []


def lauf(name, pfade):
    """ablage_soll.py einmal aufrufen; Ist-Liste und die vier Listen liegen im Scratch, der Beleg ist eine Datei."""
    ist, aus = os.path.join(TMP, "ist_%s.txt" % name), os.path.join(TMP, name)
    with open(ist, "w", encoding="utf-8") as f:
        f.write("".join(p + "\n" for p in pfade))
    r = subprocess.run([sys.executable, "-B", SKRIPT, "--ist", ist, "--aus", aus] + (["--heute"] + HEUTE if HEUTE else []),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    teile = ["== stdout ==\n" + r.stdout]
    for l in LISTEN:
        p = os.path.join(aus, l)
        teile.append("== %s ==\n%s" % (l, open(p, encoding="utf-8").read() if os.path.exists(p) else ""))
    with open(os.path.join(ORD, "lauf_%s.txt" % name), "w", encoding="utf-8") as f:
        f.write("".join(teile))
    print("%s | rc %d | %s" % (name, r.returncode, r.stdout.strip().replace("\n", " // ")))
    if r.returncode != 0:
        fehler.append(name + ": rc")


def lies(name):
    """Beleg eines Laufs -> (Zahlen der Schlusszeile, {Liste: Zeilen ohne Kopfzeile})."""
    with open(os.path.join(ORD, "lauf_%s.txt" % name), encoding="utf-8") as f:
        t = re.split(r"^== (.+?) ==\n", f.read(), flags=re.M)
    d = dict(zip(t[1::2], t[2::2]))
    zahlen = dict((k, int(v)) for k, v in re.findall(r"(Ist|Soll|entfernen|bleibt|ablegen|ohne Regel) (\d+)", d["stdout"]))
    return zahlen, dict((l, [x for x in d[l].splitlines() if not x.startswith("# ")]) for l in LISTEN)


def mit_namen(name):
    return [(l, x) for l in LISTEN for x in lies(name)[1][l] if NAME in x]


def soll(text, bedingung):
    print("%s %s" % ("ok  " if bedingung else "FEHL", text))
    if not bedingung:
        fehler.append(text)


def gegenprobe(namen):
    for l in LISTEN:
        rest = [[x for x in lies(n)[1][l] if NAME not in x] for n in namen]
        soll("Gegenprobe %s: die uebrigen %d Zeilen sind gleich in %s" % (l, len(rest[0]), ", ".join(namen)),
             all(r == rest[0] for r in rest))


def ist_listen():
    with open(os.path.join(ORD, "ist_mit.txt"), encoding="utf-8") as f:
        mit = [x.strip() for x in f if x.strip()]
    return mit, [p for p in mit if p != PFAD]


os.makedirs(ORD, exist_ok=True)
if PHASE == "alt":
    soll("Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/", not IM_REPO)
    lauf("0", [])
    basis = [x.split("\t")[0] for x in lies("0")[1]["soll.txt"]]
    soll("Basis: Pfade aus dem Soll der Vorfassung, die Datei ist nicht darunter",
         len(basis) > 0 and NAME not in [os.path.basename(p) for p in basis])
    with open(os.path.join(ORD, "ist_mit.txt"), "w", encoding="utf-8") as f:
        f.write("".join(p + "\n" for p in basis + ZUSATZ + [PFAD]))
    lauf("alt_mit", ist_listen()[0])
    soll("alt_mit: die Datei steht nur in ohne_regel.txt, Grund 'keine Regel'",
         mit_namen("alt_mit") == [("ohne_regel.txt", PFAD + "\tkeine Regel")])
elif PHASE == "fehlt":
    soll("Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/", not IM_REPO)
    lauf("neu_fehlt", ist_listen()[1])
    a, f = lies("alt_mit")[0], lies("neu_fehlt")[0]
    zeile = NAME + "\tB2 Stand - FEHLT IM REPO"
    soll("neu_fehlt: die Datei steht in soll.txt und ablegen.txt, blanker Name, Grund 'B2 Stand - FEHLT IM REPO'",
         mit_namen("neu_fehlt") == [("soll.txt", zeile), ("ablegen.txt", zeile)])
    soll("neu_fehlt: Soll +1, ablegen +1, Ist -1, ohne Regel -1, bleibt und entfernen wie alt_mit",
         (f["Soll"], f["ablegen"], f["Ist"], f["ohne Regel"]) == (a["Soll"] + 1, a["ablegen"] + 1, a["Ist"] - 1, a["ohne Regel"] - 1)
         and all(f[k] == a[k] for k in ("bleibt", "entfernen")))
    gegenprobe(("alt_mit", "neu_fehlt"))
elif PHASE == "neu":
    soll("Voraussetzung: die Datei liegt unter docs/projektfuehrung/", IM_REPO)
    mit, ohne = ist_listen()
    lauf("neu_mit", mit)
    lauf("neu_ohne", ohne)
    a, m, o = lies("alt_mit")[0], lies("neu_mit")[0], lies("neu_ohne")[0]
    zeile = PFAD + "\tB2 Stand"
    soll("neu_mit: die Datei steht nur in soll.txt, mit Ablagepfad, Grund 'B2 Stand'", mit_namen("neu_mit") == [("soll.txt", zeile)])
    soll("neu_mit: bleibt +1, Soll +1, ohne Regel -1, sonst wie alt_mit",
         (m["bleibt"], m["Soll"], m["ohne Regel"]) == (a["bleibt"] + 1, a["Soll"] + 1, a["ohne Regel"] - 1)
         and all(m[k] == a[k] for k in ("Ist", "entfernen", "ablegen")))
    soll("neu_ohne: die Datei steht in soll.txt und ablegen.txt, mit Ablagepfad, ohne 'FEHLT IM REPO'",
         mit_namen("neu_ohne") == [("soll.txt", zeile), ("ablegen.txt", zeile)])
    soll("neu_ohne: ablegen +1, Ist -1, ohne Regel -1, Soll wie neu_mit, bleibt und entfernen wie alt_mit",
         (o["ablegen"], o["Ist"], o["ohne Regel"], o["Soll"]) == (a["ablegen"] + 1, a["Ist"] - 1, a["ohne Regel"] - 1, m["Soll"])
         and all(o[k] == a[k] for k in ("bleibt", "entfernen")))
    gegenprobe(("alt_mit", "neu_fehlt", "neu_mit", "neu_ohne"))
elif PHASE == "datiert":
    # Tatsachennotiz, kein Soll: eine erfundene datierte Fassung steht in der Ist-Liste (ablage_soll.py Z. 224-226 der neuen Fassung)
    datiert = PFAD[:-3] + "_2026-10-10.md"
    print("Notiz Voraussetzung: Datei unter docs/projektfuehrung/ %s" % ("ja" if IM_REPO else "nein"))
    lauf("neu_datiert", ist_listen()[0] + [datiert])
    z, listen = lies("neu_datiert")
    for l in LISTEN:
        for x in listen[l]:
            if x.startswith(datiert):
                print("Notiz %s: %s" % (l, x))
    m = lies("neu_mit")[0]
    print("Notiz Zahlen gegen neu_mit: " + ", ".join("%s %+d" % (k, z[k] - m[k]) for k in ("Ist", "Soll", "entfernen", "bleibt", "ablegen", "ohne Regel")))
else:
    soll("Phase alt, fehlt, neu oder datiert", False)
print("ERGEBNIS %s: %d Fehler | Python %s" % (PHASE, len(fehler), sys.version.split()[0]))
sys.exit(1 if fehler else 0)
```

```bash
trading-env/bin/python3 -B docs/belege/TB-151/laeufe.py docs/werkzeuge/ablage_soll.py alt docs/belege/TB-151 > docs/belege/TB-151/a_laeufe_alt.txt 2>&1
```

Vorlauf `0` mit leerer Ist-Liste, dann Lauf `alt_mit`: Ist = Soll aus dem Vorlauf, drei erfundene Pfade und die Eröffnungsdatei. **Soll:** rc 0, drei Zeilen, die mit `ok` beginnen, keine Zeile, die mit `FEHL` beginnt, letzte Zeile `ERGEBNIS alt: 0 Fehler | Python 3.9.<x>`; sonst **ABBRUCH**. Am Gerät gemessen (die Zahlen sind kein Soll, sie hängen am Stand von `docs/`):

```text
ok   Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/
0 | rc 0 | Ist 0 | Soll 51 | entfernen 0 | bleibt 0 | ablegen 51 | ohne Regel 0
ok   Basis: Pfade aus dem Soll der Vorfassung, die Datei ist nicht darunter
alt_mit | rc 0 | Ist 55 | Soll 51 | entfernen 2 | bleibt 51 | ablegen 0 | ohne Regel 2
ok   alt_mit: die Datei steht nur in ohne_regel.txt, Grund 'keine Regel'
ERGEBNIS alt: 0 Fehler | Python 3.10.12
```

```bash
git add docs/belege/TB-151/0a_status.txt
git add docs/belege/TB-151/0a_head.txt
git add docs/belege/TB-151/0b_md5.txt
git add docs/belege/TB-151/laeufe.py
git add docs/belege/TB-151/aendere.py
git add docs/belege/TB-151/a_laeufe_alt.txt
git add docs/belege/TB-151/ist_mit.txt
git add docs/belege/TB-151/lauf_0.txt
git add docs/belege/TB-151/lauf_alt_mit.txt
git commit -m "TB-151 A: Skripte, Laeufe mit der Vorfassung"
git push
```

## Schritt B — die Änderung am Werkzeug, Lauf `neu_fehlt`

`docs/belege/TB-151/aendere.py` (1 709 B). Es prüft die md5 der Vorfassung und die Ankerzeile (genau einmal, Z. 56), führt das Ergebnis zur Probe aus (nur Konstanten und Funktionen, kein Lauf) und speichert erst danach, in einem Zug.

```python
import hashlib, os, shutil, sys
P, Z = sys.argv[1], sys.argv[2]
MD5_ALT = "46c6a18024784b86561ec2486cadc863"
NAME = "EROEFFNUNG_STEUERNDER_CHAT.md"
ANKER = '         "PROJEKTSTAND_einfache_sprache.md", "FABLE_DIALOG_INDEX.md", "KANDIDATEN_DURCHGANG_2.md"]  # 27b B2\n'
NEU = ['         "PROJEKTSTAND_einfache_sprache.md", "FABLE_DIALOG_INDEX.md", "KANDIDATEN_DURCHGANG_2.md",\n',
       '         "EROEFFNUNG_STEUERNDER_CHAT.md"]  # 27b B2\n',
       '# EROEFFNUNG_STEUERNDER_CHAT.md: Eroeffnung des steuernden Chats, fester Name, bei jedem Umzug ersetzt (TB-151)\n']
roh = open(P, "rb").read()
assert hashlib.md5(roh).hexdigest() == MD5_ALT, "md5 der Vorfassung %s" % hashlib.md5(roh).hexdigest()
z = roh.decode("ascii").splitlines(True)
assert len(z) == 290, "Zeilen %d" % len(z)
assert z.count(ANKER) == 1, "Anker kommt %d-mal vor" % z.count(ANKER)
assert z.index(ANKER) + 1 == 56, "Anker steht in Z. %d" % (z.index(ANKER) + 1)
assert sum(NAME in x for x in z) == 0, "Name steht schon im Skript"
z[55:56] = NEU
text = "".join(z)
text.encode("ascii")
probe = {"__name__": "tb151_probe"}
exec(compile(text, Z, "exec"), probe)
assert len(probe["STAND"]) == 9 and probe["STAND"][-1] == NAME and probe["STAND"].count(NAME) == 1, "STAND"
tmp = Z + ".tb151.neu"
with open(tmp, "w", encoding="ascii", newline="") as f:
    f.write(text)
shutil.copymode(P, tmp)
os.replace(tmp, Z)
n = open(Z, "rb").read()
print("ablage_soll.py | %d -> %d Zeilen | Anker Z. 56 einmal | 1 Zeile ersetzt durch 3 | STAND %d Namen, letzter %s"
      % (290, len(n.decode("ascii").splitlines()), len(probe["STAND"]), probe["STAND"][-1]))
print("md5 vorher %s | md5 nachher %s | Bytes %d" % (MD5_ALT, hashlib.md5(n).hexdigest(), len(n)))
```

```bash
trading-env/bin/python3 -B docs/belege/TB-151/aendere.py docs/werkzeuge/ablage_soll.py docs/werkzeuge/ablage_soll.py > docs/belege/TB-151/b_aendere.txt 2>&1
```

**Soll, wörtlich:**

```text
ablage_soll.py | 290 -> 292 Zeilen | Anker Z. 56 einmal | 1 Zeile ersetzt durch 3 | STAND 9 Namen, letzter EROEFFNUNG_STEUERNDER_CHAT.md
md5 vorher 46c6a18024784b86561ec2486cadc863 | md5 nachher 2d050828f6cf80b2f95196955828e8c7 | Bytes 14652
```

Endet es mit `AssertionError` oder einem anderen Fehler, ist nichts gespeichert ⇒ **ABBRUCH**. Jede andere Ausgabe ⇒ **ABBRUCH**; dann zuerst die md5 von `ablage_soll.py` messen. Danach der Lauf mit der neuen Fassung, solange die Datei noch nicht unter `docs/` liegt:

```bash
trading-env/bin/python3 -B docs/belege/TB-151/laeufe.py docs/werkzeuge/ablage_soll.py fehlt docs/belege/TB-151 > docs/belege/TB-151/b_laeufe_fehlt.txt 2>&1
```

**Soll:** rc 0, sieben Zeilen, die mit `ok` beginnen, keine Zeile, die mit `FEHL` beginnt, letzte Zeile `ERGEBNIS fehlt: 0 Fehler | Python 3.9.<x>`; sonst **ABBRUCH** (die neue Fassung ist dann gespeichert und nicht committet: als Erstes melden). Am Gerät gemessen (Zahlen kein Soll):

```text
ok   Voraussetzung: die Datei liegt nicht unter docs/projektfuehrung/
neu_fehlt | rc 0 | Ist 54 | Soll 52 | entfernen 2 | bleibt 51 | ablegen 1 | ohne Regel 1
ok   neu_fehlt: die Datei steht in soll.txt und ablegen.txt, blanker Name, Grund 'B2 Stand - FEHLT IM REPO'
ok   neu_fehlt: Soll +1, ablegen +1, Ist -1, ohne Regel -1, bleibt und entfernen wie alt_mit
ok   Gegenprobe soll.txt: die uebrigen 51 Zeilen sind gleich in alt_mit, neu_fehlt
ok   Gegenprobe entfernen.txt: die uebrigen 2 Zeilen sind gleich in alt_mit, neu_fehlt
ok   Gegenprobe ablegen.txt: die uebrigen 0 Zeilen sind gleich in alt_mit, neu_fehlt
ok   Gegenprobe ohne_regel.txt: die uebrigen 1 Zeilen sind gleich in alt_mit, neu_fehlt
ERGEBNIS fehlt: 0 Fehler | Python 3.10.12
```

Zwei Commits: zuerst das Werkzeug allein ⇒ **⟨B⟩**, dann die Belege. Soll in `b_numstat.txt`: genau eine Zahlenzeile, `3`, `1` und der Pfad des Skripts; sonst **ABBRUCH**.

```bash
git add docs/werkzeuge/ablage_soll.py
git commit -m "TB-151 B: ablage_soll.py fuehrt EROEFFNUNG_STEUERNDER_CHAT.md in STAND (B2 Stand)"
git push
git show --numstat --format=%h HEAD > docs/belege/TB-151/b_numstat.txt
git add docs/belege/TB-151/b_aendere.txt
git add docs/belege/TB-151/b_laeufe_fehlt.txt
git add docs/belege/TB-151/lauf_neu_fehlt.txt
git add docs/belege/TB-151/b_numstat.txt
git commit -m "TB-151 B: Belege"
git push
```

## Schritt C — die Datei ins Repo, Läufe `neu_mit` und `neu_ohne`, Gegenprobe, Lauf `neu_datiert`

```bash
cp logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
trading-env/bin/python3 -B -c "import hashlib,sys; [print(hashlib.md5(open(p,'rb').read()).hexdigest(), p) for p in sys.argv[1:]]" logs/steuernder_chat/EROEFFNUNG_STEUERNDER_CHAT.md docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md > docs/belege/TB-151/c_kopie.txt
```

Soll: zwei Zeilen, beide mit `769588e7c4234ccfe694106a40c761e5`; sonst **ABBRUCH**. Dass das Ziel vorher nicht existiert, hat der Lauf `neu_fehlt` gemessen (Zeile „Voraussetzung“).

```bash
trading-env/bin/python3 -B docs/belege/TB-151/laeufe.py docs/werkzeuge/ablage_soll.py neu docs/belege/TB-151 > docs/belege/TB-151/c_laeufe_neu.txt 2>&1
```

**Soll:** rc 0, neun Zeilen, die mit `ok` beginnen, keine Zeile, die mit `FEHL` beginnt, letzte Zeile `ERGEBNIS neu: 0 Fehler | Python 3.9.<x>`; sonst **ABBRUCH**. Am Gerät gemessen (Zahlen kein Soll):

```text
ok   Voraussetzung: die Datei liegt unter docs/projektfuehrung/
neu_mit | rc 0 | Ist 55 | Soll 52 | entfernen 2 | bleibt 52 | ablegen 0 | ohne Regel 1
neu_ohne | rc 0 | Ist 54 | Soll 52 | entfernen 2 | bleibt 51 | ablegen 1 | ohne Regel 1
ok   neu_mit: die Datei steht nur in soll.txt, mit Ablagepfad, Grund 'B2 Stand'
ok   neu_mit: bleibt +1, Soll +1, ohne Regel -1, sonst wie alt_mit
ok   neu_ohne: die Datei steht in soll.txt und ablegen.txt, mit Ablagepfad, ohne 'FEHLT IM REPO'
ok   neu_ohne: ablegen +1, Ist -1, ohne Regel -1, Soll wie neu_mit, bleibt und entfernen wie alt_mit
ok   Gegenprobe soll.txt: die uebrigen 51 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ok   Gegenprobe entfernen.txt: die uebrigen 2 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ok   Gegenprobe ablegen.txt: die uebrigen 0 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ok   Gegenprobe ohne_regel.txt: die uebrigen 1 Zeilen sind gleich in alt_mit, neu_fehlt, neu_mit, neu_ohne
ERGEBNIS neu: 0 Fehler | Python 3.10.12
```

**Tatsachennotiz, kein Soll:** ein Lauf mehr, mit einer erfundenen datierten Fassung der Datei in der Ist-Liste (`STAND` wirkt auch in `ablage_soll.py` Z. 222–224 der Vorfassung).

```bash
trading-env/bin/python3 -B docs/belege/TB-151/laeufe.py docs/werkzeuge/ablage_soll.py datiert docs/belege/TB-151 > docs/belege/TB-151/c_laeufe_datiert.txt 2>&1
```

Am Gerät gemessen. Weicht die Ausgabe ab: im Ergebnis nennen, kein Abbruch.

```text
Notiz Voraussetzung: Datei unter docs/projektfuehrung/ ja
neu_datiert | rc 0 | Ist 56 | Soll 52 | entfernen 3 | bleibt 52 | ablegen 0 | ohne Regel 1
Notiz entfernen.txt: projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT_2026-10-10.md	B2 datierte Fassung - EROEFFNUNG_STEUERNDER_CHAT.md liegt im Repo
Notiz Zahlen gegen neu_mit: Ist +1, Soll +0, entfernen +1, bleibt +0, ablegen +0, ohne Regel +0
ERGEBNIS datiert: 0 Fehler | Python 3.10.12
```

Zwei Commits: zuerst die Datei allein ⇒ **⟨C⟩**, dann die Belege. Meldet `git add` die Datei als ignoriert ⇒ **ABBRUCH** (kein `-f`). Soll in `c_verfolgt.txt`: genau eine Zeile, der Pfad der Datei.

```bash
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git commit -m "TB-151 C: Eroeffnungsdatei des steuernden Chats unter docs/projektfuehrung/"
git push
git ls-files docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md > docs/belege/TB-151/c_verfolgt.txt
git add docs/belege/TB-151/c_kopie.txt
git add docs/belege/TB-151/c_laeufe_neu.txt
git add docs/belege/TB-151/lauf_neu_mit.txt
git add docs/belege/TB-151/lauf_neu_ohne.txt
git add docs/belege/TB-151/c_laeufe_datiert.txt
git add docs/belege/TB-151/lauf_neu_datiert.txt
git add docs/belege/TB-151/c_verfolgt.txt
git commit -m "TB-151 C: Belege"
git push
```

## Schritt D — BACKLOG, Journal, Ergebnis, Abgabe

Dokumentationsauftrag nach ARBEITSWEISE 5b: Die Blöcke stehen wörtlich in Anhang 1 und Anhang 2; nichts umformulieren. Die Sitzung ersetzt darin nur ⟨KENNUNG⟩, ⟨FOLGEKENNUNG⟩ (die Kennung nach ⟨KENNUNG⟩) und ⟨DATUM⟩ (der Tag der Sitzung, TT.MM.JJJJ, zur Laufzeit gemessen). Stimmt eine Aussage eines Blocks nicht mit dem Gemessenen überein: den Block nicht setzen, melden.

**D1. BACKLOG:** Zieldatei `docs/projektfuehrung/BACKLOG.md` · Anker: die Zeile, die mit `## 6 — Geparkt, null Arbeit` beginnt (beim Bau genau einmal, Z. 404 von 415) · Art: Anhang 1 **vor der Zeile**, mit einer Leerzeile danach. Soll `numstat`: `7	0`.

**D2. Journal:** Zieldatei `docs/projektfuehrung/JOURNAL.md` · Anker: `## Wiederkehrende Lehren` (beim Bau genau einmal) · Art: Anhang 2 **vor der Zeile**, mit einer Leerzeile danach. ⟨KENNUNG⟩ vorher messen: die Kennung nach dem letzten Buchstabenblock (beim Bau war EO der letzte, erwartet **EP**). Soll `numstat`: `24	0`.

**D3. Ergebnis** `docs/ERGEBNIS_TB-151_eroeffnungsdatei_im_repo.md`: Kopf (samt Sichtschutz-Zeile, ARBEITSWEISE 23.1, G5) · „Kurz“ (Tabelle Soll | Ist für 0a, 0b, A, B, C, D1, D2, mit den Hashes ⟨S0⟩, ⟨B⟩, ⟨C⟩) · die Zeilen aus `a_laeufe_alt.txt`, `b_laeufe_fehlt.txt`, `c_laeufe_neu.txt` und `c_laeufe_datiert.txt` · „Abweichungen vom Auftrag“ · „Nicht getan“ · „In einfacher Sprache“. Das Ergebnis entsteht erst nach Schritt C: Läge es früher unter `docs/`, änderte es das Soll zwischen den Läufen.

**D4. Abgabe, dann porcelain als Beleg** (Soll: `$TMPDIR/tb151_d4.txt` ist leer; `d4_numstat.txt` nennt die drei Pfade mit den Zahlen aus D1 und D2):

```bash
git add docs/projektfuehrung/BACKLOG.md
git add docs/projektfuehrung/JOURNAL.md
git add docs/ERGEBNIS_TB-151_eroeffnungsdatei_im_repo.md
git commit -m "TB-151 Abgabe: BACKLOG, Journal, Ergebnis"
git push
git status --porcelain > "$TMPDIR/tb151_d4.txt"
git show --numstat --format=%h HEAD > docs/belege/TB-151/d4_numstat.txt
cp "$TMPDIR/tb151_d4.txt" docs/belege/TB-151/d4_porcelain.txt
git add docs/belege/TB-151/d4_numstat.txt
git add docs/belege/TB-151/d4_porcelain.txt
git commit -m "TB-151 Abgabe: numstat und porcelain nach dem Abgabe-Commit"
git push
git rev-parse HEAD origin/main
```

**Schlussmeldung, eine Zeile:** `TB-151 fertig: Datei im Repo (<Hash von ⟨C⟩>), ablage_soll.py (<Hash von ⟨B⟩>), Läufe 0 Fehler, Journal <Kennung>, porcelain <leer | Zeilen>, HEAD <gleich | ungleich> origin/main`.

## Abbruchkriterien — melden, nicht reparieren

- 0a weicht ab, `cmp` ist ungleich, oder in 0b trägt `ablage_soll.py` oder die Datei unter `logs/` eine andere md5.
- A, B oder C (Phasen `alt`, `fehlt`, `neu`): rc ≠ 0, eine Zeile, die mit `FEHL` beginnt (auch „Voraussetzung“), oder `ablage_soll.py` endet mit einem Fehler.
- B: `aendere.py` endet mit einem Fehler oder einer anderen Ausgabe als den zwei Soll-Zeilen; `numstat` weicht ab.
- C: die zwei md5 in `c_kopie.txt` sind ungleich; `git add` meldet die Datei als ignoriert; `c_verfolgt.txt` ist leer.
- Eine Datei ausserhalb der Liste müsste geändert werden; Claude Code lehnt einen Befehl ab (melden, nicht umgehen); `git push` scheitert zweimal.

**Kein Abbruch:** der BACKLOG- oder Journal-Anker kommt nicht genau einmal vor (Block nicht setzen, nennen) · eine andere Journal-Kennung als EP (nehmen, nennen) · andere Zahlen in den Läufen als am Gerät · eine andere Ausgabe der Phase `datiert` (nennen).

**Verfahren bei Abbruch:** `docs/belege/TB-151/abbruch.txt` schreiben (Schritt, Grund im Wortlaut, md5 von `ablage_soll.py`, ob `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` existiert); die Belege mit Namen committen (`TB-151 Abbruch in Schritt <x>: <Grund>`) und pushen, soweit das geht; dann eine Zeile melden: `TB-151 ABBRUCH in Schritt <x>: <Grund>`. Gibt es den Belegordner noch nicht, genügt die Meldung. **Nichts zurückdrehen, nichts löschen.** `ablage_soll.py` trägt nach jedem Abbruch entweder die Vorfassung oder die neue Fassung. Ist die neue Fassung gespeichert oder die Datei kopiert, aber nicht committet oder nicht gepusht, steht das als Erstes in der Meldung.

## Nicht in TB-151

Die Texte, die den Ort der Datei und den Umzug beschreiben (TB-152): `UMZUG.md` Z. 260 nennt die Ablage und die Kopie unter `logs/steuernder_chat/`, `ARBEITSWEISE.md` Z. 118 nennt nur die Ablage, Z. 212 sagt „in der Ablage und nicht nur im Repo“ · die Kopie unter `logs/steuernder_chat/` (bleibt liegen) · die festen Monatsangaben `2026-09-` in `ablage_soll.py` Z. 105 und Z. 145 der Vorfassung (Nebenbefund, eigener Auftrag) · der Abgleich mit der echten Ablage und das Ablegen (steuernder Chat) · `ablage_ereignisse.json`.

## In einfacher Sprache

Wenn ein neuer steuernder Chat anfängt, liest er zuerst einen Eröffnungstext. Dieser Text lag bisher nur in der Projektablage und in einem Ordner, den git nicht sichert. Unsere eigene Regel sagt aber: Was einen Umzug überleben muss, liegt gesichert im Repo. Dieser Auftrag legt den Text deshalb ins Repo. Dazu lernt ein kleines Werkzeug, das dem steuernden Chat sagt, welche Dateien in der Ablage liegen sollen, den Namen dieser Datei. Bisher meldete es sie als „passt zu keiner Regel“, und wenn sie fehlte, merkte es nichts. Sechs Probeläufe mit einer künstlichen Liste zeigen, dass das Werkzeug die Datei jetzt richtig führt und dass sich für die übrigen Dateien dieser Liste nichts ändert. An den Handelsprogrammen und an den Daten ändert der Auftrag nichts.

## Anhang 1 — BACKLOG-Block, wörtlich (D1)

```text
### Eröffnungsdatei des steuernden Chats im Repo, `ablage_soll.py` führt sie als B2 Stand — eingetragen mit TB-151

- **Entscheid des steuernden Chats (Handwerk, 10.10.2026):** Die Eröffnungsdatei liegt verfolgt unter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und ist Klasse B2 Stand (ARBEITSWEISE 23.2: Repo und Ablage, eine Fassung ohne Datum im Namen). Grund: G1 (ARBEITSWEISE 23.1, „Alles, was den Umzug überleben muss, liegt dort committet“) und `UMZUG.md` Abschnitt 4, Schritt 4 („muss mit dem Repo gleich lauten“).
- **Gebaut mit TB-151:** Die Datei ist aus `logs/steuernder_chat/` kopiert (md5 beider Seiten gleich, `docs/belege/TB-151/c_kopie.txt`). `docs/werkzeuge/ablage_soll.py` trägt den Namen in der Liste `STAND` (eine Zeile ersetzt durch drei; md5 nachher `2d050828f6cf80b2f95196955828e8c7`). Vorher fiel die Datei nach `ohne_regel.txt`, und ihr Fehlen meldete das Werkzeug nicht. Nachweis: `docs/belege/TB-151/c_laeufe_neu.txt`.
- **Folge für jeden Auftrag:** Ersetzt ein Umzug die Datei im Repo, ist sie beim nächsten Auftrag geändert und gehört in das Soll von 0a und in den Commit von Schritt 0, wie `UEBERGABE.md`.
- **Offen:** `UMZUG.md` Z. 260 nennt als Ort der Datei noch die Ablage und die Kopie unter `logs/steuernder_chat/`; `ARBEITSWEISE.md` Z. 118 nennt nur die Ablage, Z. 212 sagt „in der Ablage und nicht nur im Repo“ (TB-152). Der steuernde Chat ersetzt die Datei ab TB-151 bei jedem Umzug im Repo und in der Ablage, md5 gleich (Vorgabe des steuernden Chats, vorläufig; `UEBERGABE.md`, Umzug 10.10.2026, 22:55, Block 6); die Regeltexte folgen mit TB-152.
```

## Anhang 2 — Journalblock, wörtlich (D2)

```text
## ⟨KENNUNG⟩ — TB-151: Eröffnungsdatei des steuernden Chats verfolgt unter `docs/projektfuehrung/`, `ablage_soll.py` führt sie als B2 Stand

*Quelle: `docs/ERGEBNIS_TB-151_eroeffnungsdatei_im_repo.md`*

**Quelle:** Mac-Sitzung **TB-151**, ⟨DATUM⟩, Auftrag `docs/auftraege/MAC_TB-151_eroeffnungsdatei_im_repo.md`. Commits und Hashes stehen im Ergebnis, Belege unter `docs/belege/TB-151/`. Entscheid des steuernden Chats vom 10.10.2026 (Handwerk, keine Betreiberfreigabe nötig). Der Wortlaut dieses Blocks stand im Auftrag; die Sitzung hat ihn gesetzt, nachdem jedes Soll der Schritte 0 bis C gehalten hat.

### Was gemessen ist

| | |
|---|---|
| **A** | Vorfassung von `ablage_soll.py` (md5 `46c6a18024784b86561ec2486cadc863`): Steht die Eröffnungsdatei in der Ist-Liste, fällt sie nach `ohne_regel.txt`, Grund „keine Regel“ (`a_laeufe_alt.txt`) |
| **B** | `STAND` trägt neun Namen, der neunte ist `EROEFFNUNG_STEUERNDER_CHAT.md`; numstat 3/1, md5 nachher `2d050828f6cf80b2f95196955828e8c7` (`b_aendere.txt`, `b_numstat.txt`). Liegt die Datei nicht unter `docs/`, steht sie mit „B2 Stand - FEHLT IM REPO“ in `soll.txt` und `ablegen.txt` (`b_laeufe_fehlt.txt`) |
| **C** | Datei von `logs/steuernder_chat/` nach `docs/projektfuehrung/` kopiert, md5 beider Seiten gleich, von git verfolgt (`c_kopie.txt`, `c_verfolgt.txt`). Im Ist: bleibt, Pfad `projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md`, Grund „B2 Stand“; nicht im Ist: `ablegen.txt`. Alle übrigen Zeilen der vier Listen sind in vier Läufen gleich (`c_laeufe_neu.txt`) |

### Was offen bleibt

- `UMZUG.md` Z. 260 nennt als Ort der Datei noch die Ablage und die Kopie unter `logs/steuernder_chat/`; `ARBEITSWEISE.md` Z. 118 nennt nur die Ablage, Z. 212 sagt „in der Ablage und nicht nur im Repo“ (TB-152). Der steuernde Chat ersetzt die Datei ab TB-151 bei jedem Umzug im Repo und in der Ablage, md5 gleich (Vorgabe des steuernden Chats, vorläufig; `UEBERGABE.md`, Umzug 10.10.2026, 22:55, Block 6); die Regeltexte folgen mit TB-152.
- Die Läufe nahmen eine künstliche Ist-Liste; den Abgleich mit der echten Ablage macht der steuernde Chat.
- Nächste Journalkennung nach ⟨KENNUNG⟩: **⟨FOLGEKENNUNG⟩**.

*Geschrieben ⟨DATUM⟩ von der Mac-Sitzung TB-151 nach dem Wortlaut des Auftrags. Quellenvermerk: siehe Kopf.*

---
```
