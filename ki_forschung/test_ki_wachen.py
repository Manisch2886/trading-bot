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
