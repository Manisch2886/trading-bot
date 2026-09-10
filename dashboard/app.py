"""
Dashboard-Backend (FastAPI) - LESEND, MIT GENAU EINER AUSNAHME
==============================================================
Stellt die Daten der neun Paper-Trading-Bots als JSON bereit und liefert
das kleine Web-Frontend aus.

BIS PR #60 GALT HIER: "ausschliesslich lesend, es gibt KEINEN
schreibenden Endpunkt". Das stimmt nicht mehr, und diese Zeilen sind die
Korrektur dazu - der Satz stand in vier PRs so da und soll nicht
stillschweigend falsch werden.

Es gibt jetzt genau EINEN Zweck, zu dem in eine Bot-Datenbank
geschrieben wird - offene Positionen von Hand schliessen -, in drei
Abstufungen:

  EINZELN   eine Position eines Bots      EIN Tap
  ALLE      alle Positionen EINES Bots    ZWEI Klicks
  GLOBAL    alle Positionen ALLER Bots    ZWEI Klicks + Text "CRASH"

Fuer alle drei gilt:
  * nur fuer die Bots in manual_close.SCHLIESSBARE_BOTS - inzwischen alle
    neun, jeder davon einzeln gegen sein forward_test.py geprueft (Schema,
    PnL-Formel, result-Werte; siehe Testabschnitt 9),
  * nur nach ZWEI getrennten HTTP-Aufrufen (vorbereiten + ausfuehren),
    der zweite mit einer zufaelligen, einmaligen, nach 120 Sekunden
    verfallenden Vorgangs-Kennung, die nur fuer genau diesen Bot, diese
    Position(en) und diese Art von Vorgang gilt (eine Einzel-Kennung
    loest auf dem Alle-Endpunkt nichts aus, und keine der beiden auf dem
    globalen),
  * und nur ueber notifications/manual_close.py, das die gesamte
    Absicherung mitbringt (Transaktion, Nebenlaeufigkeit, Protokoll) -
    auch die beiden Sammelwege rufen dort je Position EINZELN auf, es
    gibt keine Sammelschreibung. Der globale Weg benutzt dafuer genau die
    Schleife des bot-weiten Wegs, nicht eine dritte Fassung.
Siehe dashboard/schliessen.py. Alles andere ist unveraendert lesend:
kein Parameter laesst sich aendern, keine Position eroeffnen, kein
Bot-Lauf anstossen.

Nicht-GET-Routen insgesamt: POST /login (schreibt nur ein Cookie), die
drei Routen des Einzel-Schliessvorgangs, die zwei des bot-weiten
Notfallwegs und die zwei des globalen Crash-Wegs. In eine Datenbank
schreiben genau drei davon:
POST /api/bots/{name}/schliessen/ausfuehren,
POST /api/bots/{name}/alle-schliessen/ausfuehren und
POST /api/alle-bots-schliessen/ausfuehren.

Alle Zahlen kommen ueber dashboard/datenquelle.py aus
notifications/monitor.py, das die Bot-Datenbanken read-only oeffnet.

ZUGRIFFSSCHUTZ: Jede Anfrage - auch die auf HTML, CSS, Icons und den
Service Worker - muss ein gueltiges Token mitbringen (Cookie, Header
X-Dashboard-Token, Authorization: Bearer, oder einmalig ?token=...).
Ohne gueltiges Token gibt es fuer /api/* ein 401 als JSON und fuer
Seitenaufrufe eine Weiterleitung auf die Login-Seite. Der Vergleich
laeuft ueber hmac.compare_digest, also in konstanter Zeit - ein
zeichenweiser Vergleich waere ueber die Antwortzeit angreifbar.

WARUM UEBERHAUPT EIN TOKEN, wenn der Server nur auf localhost lauscht:
Die geplante Absicherung ueber Tailscale existiert noch nicht (siehe
README). Das Token ist die Verteidigungsebene fuer den Fall, dass das
Dashboard vorher versehentlich oder absichtlich netzwerkweit erreichbar
gemacht wird - dann steht nicht die gesamte Handelshistorie fuer jeden
im WLAN offen.
"""

import asyncio
import hmac
import logging
import os
import urllib.parse

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import konfig
import datenquelle
import schliessen

logger = logging.getLogger("dashboard.app")

# Pfade, die OHNE Token erreichbar sein muessen - sonst koennte sich
# niemand anmelden. Bewusst so kurz wie moeglich gehalten; die
# Login-Seite bringt ihr CSS inline mit, damit hier keine weitere
# Ausnahme noetig ist.
OEFFENTLICHE_PFADE = {"/login", "/favicon.ico"}


def _token_aus_anfrage(request: Request):
    """Token aus Cookie, Header oder Query - in dieser Reihenfolge."""
    cookie = request.cookies.get(konfig.COOKIE_NAME)
    if cookie:
        return cookie

    kopfzeile = request.headers.get("x-dashboard-token")
    if kopfzeile:
        return kopfzeile

    autorisierung = request.headers.get("authorization", "")
    if autorisierung.lower().startswith("bearer "):
        return autorisierung[7:].strip()

    return request.query_params.get("token")


def _token_gueltig(uebergeben, erwartet: str) -> bool:
    if not uebergeben:
        return False
    # compare_digest statt "==": konstante Laufzeit, damit sich das Token
    # nicht ueber Antwortzeit-Unterschiede zeichenweise erraten laesst.
    return hmac.compare_digest(str(uebergeben), erwartet)


def erzeuge_app(token: str = None) -> FastAPI:
    """
    token: nur fuer Tests direkt uebergeben. Im Normalbetrieb wird das
    Token ueber konfig.lade_token() aus der Umgebung/.env gelesen und
    der Start bricht ab, wenn keines gesetzt ist (fail closed).
    """
    erwartetes_token = token if token is not None else konfig.lade_token()

    app = FastAPI(
        title="Trading-Bot-Dashboard",
        description=("Uebersicht ueber die neun Paper-Trading-Bots. Lesend, "
                      "mit genau einer schreibenden Ausnahme: das manuelle "
                      "Schliessen offener Positionen - einzeln, bot-weit oder "
                      "global - bei den freigeschalteten Bots."),
        docs_url=None,      # keine oeffentliche API-Doku-Seite - das Dashboard
        redoc_url=None,     # hat genau einen Nutzer, der die Endpunkte kennt.
        openapi_url=None,
    )

    @app.middleware("http")
    async def zugriffsschutz(request: Request, call_next):
        pfad = request.url.path
        if pfad in OEFFENTLICHE_PFADE:
            return await call_next(request)

        uebergeben = _token_aus_anfrage(request)
        if not _token_gueltig(uebergeben, erwartetes_token):
            # Bewusst KEINE Unterscheidung zwischen "kein Token" und
            # "falsches Token" nach aussen, und das Token taucht in
            # keiner Log-Zeile auf.
            logger.warning(f"Abgelehnter Zugriff auf {pfad} (kein gueltiges Token).")
            if pfad.startswith("/api/"):
                return JSONResponse(
                    {"fehler": "Kein gueltiges Zugriffs-Token."}, status_code=401)
            return RedirectResponse("/login", status_code=303)

        antwort = await call_next(request)

        # Wer das Token per ?token=... geschickt hat (der bequeme Weg beim
        # ersten Aufruf auf dem iPhone), bekommt es als Cookie gesetzt und
        # muss es danach nicht mehr an jede URL haengen.
        if request.query_params.get("token") and not request.cookies.get(konfig.COOKIE_NAME):
            _setze_cookie(antwort, erwartetes_token)
        return antwort

    def _setze_cookie(antwort, wert: str):
        antwort.set_cookie(
            konfig.COOKIE_NAME, wert,
            httponly=True,      # kein Zugriff aus JavaScript
            samesite="strict",  # wird nicht an fremde Seiten mitgeschickt
            # secure=False, weil das Dashboard ueber http:// auf localhost
            # bzw. spaeter im Tailscale-Netz laeuft - mit secure=True wuerde
            # der Browser das Cookie dort gar nicht erst setzen. Sobald es
            # jemals ueber echtes HTTPS laeuft, gehoert hier secure=True hin.
            max_age=60 * 60 * 24 * 90,
            path="/",
        )

    # -- Anmeldung ---------------------------------------------------------

    @app.get("/login", response_class=HTMLResponse)
    async def login_seite():
        return _login_html()

    @app.post("/login")
    async def login_absenden(request: Request):
        """Schreibt nur ein Cookie - ohne jede Wirkung auf Bots oder Daten.
        (Bis PR #60 war das die einzige Nicht-GET-Route; seit dem
        manuellen Schliessen gibt es die sieben Routen weiter unten. Diese
        hier bleibt die einzige ohne Token-Pflicht.)

        Der Formularkoerper wird hier von Hand geparst, statt ueber
        FastAPIs Form(...) oder request.form(): beide verlangen das
        Zusatzpaket python-multipart, obwohl ein einfaches
        HTML-Formular als application/x-www-form-urlencoded ankommt -
        ein Format, das die Standardbibliothek in einer Zeile liest.
        Fuer eine Route, die nur ein Cookie setzt, ist das keine
        zusaetzliche Abhaengigkeit wert.
        """
        koerper = (await request.body()).decode("utf-8", errors="replace")
        felder = urllib.parse.parse_qs(koerper)
        token = (felder.get("token") or [""])[0]
        if not _token_gueltig(token, erwartetes_token):
            return HTMLResponse(_login_html(fehler=True), status_code=401)
        antwort = RedirectResponse("/", status_code=303)
        _setze_cookie(antwort, erwartetes_token)
        return antwort

    @app.get("/abmelden")
    async def abmelden():
        antwort = RedirectResponse("/login", status_code=303)
        antwort.delete_cookie(konfig.COOKIE_NAME, path="/")
        return antwort

    # -- Seiten und PWA-Dateien -------------------------------------------

    @app.get("/", response_class=HTMLResponse)
    async def startseite():
        return FileResponse(os.path.join(konfig.STATIC_DIR, "index.html"))

    @app.get("/bot", response_class=HTMLResponse)
    async def bot_seite():
        return FileResponse(os.path.join(konfig.STATIC_DIR, "bot.html"))

    @app.get("/manifest.json")
    async def manifest():
        return FileResponse(os.path.join(konfig.STATIC_DIR, "manifest.json"),
                             media_type="application/manifest+json")

    @app.get("/sw.js")
    async def service_worker():
        # Der Service Worker muss vom Wurzelpfad ausgeliefert werden,
        # sonst gilt sein Geltungsbereich nur fuer /statisch/.
        return FileResponse(os.path.join(konfig.STATIC_DIR, "sw.js"),
                             media_type="application/javascript")

    # -- API (alles GET, alles lesend) ------------------------------------

    @app.get("/api/health")
    async def health():
        return {"status": "ok",
                "modus": "lesend, ausser dem manuellen Schliessen",
                "schliessen_freigeschaltet": schliessen.freigeschaltete_bots()}

    async def _kurse_holen(auswahl: list):
        """Live-Kurse mit harter Zeitgrenze - gibt (kurse, hinweis) zurueck.

        EVENT-LOOP-SICHERHEIT (dieselbe Lektion wie beim Telegram-Bot,
        siehe notifications/monitor.py): Binance- und yfinance-Abfragen
        sind ECHTE, blockierende synchrone Netzwerkaufrufe. FastAPI
        laeuft asynchron in EINEM Event-Loop - ein einziger direkter
        Aufruf hier wuerde den kompletten Server fuer ALLE gleichzeitigen
        Anfragen einfrieren, solange die langsamste Kursabfrage laeuft.
        Deshalb IMMER asyncio.to_thread(), NIE der direkte Aufruf.

        asyncio.wait_for() setzt zusaetzlich eine harte Obergrenze: nach
        LIVE_KURS_TIMEOUT_SEKUNDEN wird lieber ohne Kurse geantwortet
        (mit Hinweis) als beliebig lange zu haengen - das Dashboard zeigt
        dann alle uebrigen Zahlen und "Preis nicht verfuegbar".
        """
        try:
            kurse = await asyncio.wait_for(
                asyncio.to_thread(datenquelle.live_kurse, auswahl),
                timeout=konfig.LIVE_KURS_TIMEOUT_SEKUNDEN,
            )
            return kurse, None
        except asyncio.TimeoutError:
            logger.warning(
                f"Live-Kursabfrage hat {konfig.LIVE_KURS_TIMEOUT_SEKUNDEN}s "
                f"ueberschritten - Antwort ohne Kurse.")
            return {}, (f"Zeitueberschreitung nach {konfig.LIVE_KURS_TIMEOUT_SEKUNDEN} "
                         f"Sekunden - Kurse aktuell nicht verfuegbar.")
        except Exception as e:
            # Ein Netzwerk-/API-Fehler darf niemals die gesamte Seite
            # unbrauchbar machen - genau wie bei /status in Telegram.
            logger.warning(f"Live-Kursabfrage fehlgeschlagen: {e}")
            return {}, "Kursabfrage fehlgeschlagen - siehe Log."

    @app.get("/api/portfolio")
    async def portfolio(live: int = 0):
        """Uebersicht aller Bots.

        Ohne live=1 eine reine Datenbankabfrage ohne jeden
        Netzwerkzugriff - schnell und immer verfuegbar. Das Frontend
        laedt zuerst diese Fassung, zeigt sie sofort an und holt die
        langsame, netzabhaengige Fassung (live=1) danach im Hintergrund
        nach. So haengt die Seite nie an einer langsamen Kursabfrage.
        """
        if not live:
            return await asyncio.to_thread(datenquelle.portfolio_uebersicht)

        auswahl = await asyncio.to_thread(datenquelle.alle_bots)
        kurse, hinweis = await _kurse_holen(auswahl)
        uebersicht = await asyncio.to_thread(datenquelle.portfolio_uebersicht, kurse)
        uebersicht["kurs_hinweis"] = hinweis
        return uebersicht

    @app.get("/api/bots")
    async def bots():
        return {"bots": [
            {"name": b["name"], "anzeigename": b["display_name"],
             "anlageklasse": b["asset_class"]}
            for b in await asyncio.to_thread(datenquelle.alle_bots)
        ]}

    @app.get("/api/bots/{name}")
    async def bot_detail(name: str, trades: int = 50, live: int = 0):
        """Einzelner Bot. live=1 holt zusaetzlich die aktuellen Kurse
        seiner offenen Positionen (langsam, netzabhaengig) - die
        Detailseite laedt genau wie die Uebersicht erst ohne und dann
        mit Kursen."""
        bot = await asyncio.to_thread(datenquelle.finde_bot, name)
        if bot is None:
            raise HTTPException(status_code=404, detail=f"Unbekannter Bot: {name}")

        kurse, hinweis = (None, None)
        if live:
            kurse, hinweis = await _kurse_holen([bot])
        detail = await asyncio.to_thread(datenquelle.bot_detail, bot, kurse, trades)
        detail["kurs_hinweis"] = hinweis
        return detail

    @app.get("/api/bots/{name}/trades")
    async def bot_trades(name: str, limit: int = 50):
        bot = await asyncio.to_thread(datenquelle.finde_bot, name)
        if bot is None:
            raise HTTPException(status_code=404, detail=f"Unbekannter Bot: {name}")
        return {"bot": name,
                "trades": await asyncio.to_thread(datenquelle.geschlossene_trades, bot, limit)}

    @app.get("/api/verlauf")
    async def verlauf():
        return await asyncio.to_thread(datenquelle.gesamtverlauf)

    @app.get("/api/live-kurse")
    async def live_kurse(bot: str = None):
        """Nur die Kurse der offenen Positionen (optional fuer EINEN Bot).

        Siehe _kurse_holen() fuer die Event-Loop- und Timeout-Regeln.
        """
        auswahl = await asyncio.to_thread(datenquelle.alle_bots)
        if bot:
            auswahl = [b for b in auswahl if b["name"] == bot]
            if not auswahl:
                raise HTTPException(status_code=404, detail=f"Unbekannter Bot: {bot}")
        kurse, hinweis = await _kurse_holen(auswahl)
        return {"kurse": kurse, "hinweis": hinweis}

    # -- Manuelles Schliessen: die schreibenden Pfade ---------------------
    # Sieben Routen, aber nur DREI schreiben in eine Datenbank:
    #   GET  .../schliessbare-positionen     liest (IDs + Live-Kurs + PnL)
    #   POST .../schliessen/vorbereiten      legt einen Vorgang im Speicher an
    #   POST .../schliessen/abbrechen        verwirft ihn wieder (beide Arten)
    #   POST .../schliessen/ausfuehren       <- schreibt (eine Position)
    #   POST .../alle-schliessen/vorbereiten legt einen Notfall-Vorgang an
    #   POST .../alle-schliessen/ausfuehren  <- schreibt (alle bestaetigten)
    #   POST /api/alle-bots-schliessen/...   Crash-Weg (weiter unten)
    # Die Aufteilung ist die eigentliche Sicherung: es gibt keinen
    # einzelnen Aufruf, der eine Position schliesst. Ein Bestaetigungs-
    # dialog allein im Browser waere keiner - die API bliebe mit curl
    # direkt erreichbar. Siehe dashboard/schliessen.py.

    async def _koerper(request: Request) -> dict:
        try:
            daten = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Kein gueltiges JSON.")
        if not isinstance(daten, dict):
            raise HTTPException(status_code=400,
                                 detail="Erwartet wird ein JSON-Objekt.")
        return daten

    def _wer(request: Request) -> str:
        """Was ins Protokoll kommt. Das Dashboard hat keine Nutzer-IDs -
        es gibt genau ein Token. Die Gegenstelle ist trotzdem die
        nuetzlichste Angabe, die zur Verfuegung steht."""
        gegenstelle = request.client.host if request.client else "unbekannt"
        return f"dashboard@{gegenstelle}"

    def _bot_oder_404(name: str):
        if not schliessen.ist_freigeschaltet(name):
            # 403 statt 404: der Bot existiert, er ist nur nicht
            # freigeschaltet. Ein 404 wuerde das verschleiern und die
            # Fehlersuche erschweren.
            raise HTTPException(
                status_code=403,
                detail=(f"Fuer '{name}' ist das manuelle Schliessen nicht "
                         f"freigeschaltet. Freigeschaltet: "
                         f"{', '.join(schliessen.freigeschaltete_bots())}."))

    @app.get("/api/bots/{name}/schliessbare-positionen")
    async def schliessbare_positionen(name: str, live: int = 0):
        """Rein lesend. Liefert fuer nicht freigeschaltete Bots bewusst
        ein 200 mit schliessbar=false statt eines Fehlers - das Frontend
        fragt das fuer JEDEN Bot ab und soll dabei keine Fehlermeldung
        anzeigen muessen.

        Ohne live=1 ohne jeden Netzwerkzugriff. Das Frontend braucht von
        hier im Normalfall nur die Antwort auf "ist dieser Bot ueberhaupt
        freigeschaltet" - die Kurse fuer die Zusammenfassung holt der
        Server ohnehin frisch, wenn der Vorgang vorbereitet wird.
        """
        bot = await asyncio.to_thread(datenquelle.finde_bot, name)
        if bot is None:
            raise HTTPException(status_code=404, detail=f"Unbekannter Bot: {name}")
        if not schliessen.ist_freigeschaltet(name):
            return await asyncio.to_thread(schliessen.positionen, name, {})

        kurse, hinweis = ({}, None)
        if live:
            kurse, hinweis = await _kurse_holen([bot])
        antwort = await asyncio.to_thread(schliessen.positionen, name, kurse)
        antwort["kurs_hinweis"] = hinweis
        return antwort

    @app.post("/api/bots/{name}/schliessen/vorbereiten")
    async def schliessen_vorbereiten(name: str, request: Request):
        """Aufruf 1. Schreibt NICHTS - legt nur einen Vorgang im
        Arbeitsspeicher an und gibt die Zusammenfassung zurueck."""
        _bot_oder_404(name)
        daten = await _koerper(request)
        bot = await asyncio.to_thread(datenquelle.finde_bot, name)
        if bot is None:
            raise HTTPException(status_code=404, detail=f"Unbekannter Bot: {name}")

        kurse, _ = await _kurse_holen([bot])
        try:
            return await asyncio.to_thread(
                schliessen.vorbereiten, name, daten.get("trade_id"), kurse)
        except schliessen.SchliessenNichtMoeglich as fehler:
            raise HTTPException(status_code=409, detail=str(fehler))

    @app.post("/api/bots/{name}/schliessen/abbrechen")
    async def schliessen_abbrechen(name: str, request: Request):
        """Verwirft einen angefangenen Vorgang. Beruehrt keine Datenbank -
        der Vorgang liegt ausschliesslich im Arbeitsspeicher."""
        daten = await _koerper(request)
        schliessen.abbrechen(daten.get("vorgang"))
        return {"abgebrochen": True,
                "meldung": "Abgebrochen. Es wurde nichts geaendert."}

    @app.post("/api/bots/{name}/schliessen/ausfuehren")
    async def schliessen_ausfuehren(name: str, request: Request):
        """Aufruf 2 - DER schreibende Endpunkt des Dashboards.

        Ohne eine gueltige, nicht abgelaufene Vorgangs-Kennung aus dem
        vorbereiten-Aufruf passiert hier nichts. Ein zusaetzlicher
        Bestaetigungstext wird nicht mehr verlangt - was hier ankommt, wird
        also gar nicht gelesen. Geschrieben wird ueber
        notifications/manual_close.py, nicht hier.
        """
        _bot_oder_404(name)
        daten = await _koerper(request)
        try:
            return await asyncio.to_thread(
                schliessen.ausfuehren, name, daten.get("vorgang"),
                _wer(request))
        except schliessen.SchliessenNichtMoeglich as fehler:
            # 409 (Konflikt) und nicht 400: die Anfrage war formal in
            # Ordnung, der Zustand hat nur nicht gepasst - abgelaufene
            # Bestaetigung, fremder Bot, oder der Cronjob war schneller.
            raise HTTPException(status_code=409, detail=str(fehler))
        except Exception:
            logger.exception("Unerwarteter Fehler beim manuellen Schliessen.")
            raise HTTPException(
                status_code=500,
                detail=("Unerwarteter Fehler - siehe Log. Ob geschrieben wurde, "
                         "bitte in der Positionsliste pruefen."))

    # -- Notfallweg: ALLE offenen Positionen eines Bots -------------------
    # Dieselbe Aufteilung wie beim Einzelweg, eigene Vorgangs-Art: eine
    # Kennung von dort loest hier nichts aus (siehe schliessen.ART_*).
    # Abgebrochen wird ueber dieselbe abbrechen-Route - der Vorgang liegt im
    # selben Speicher, und eine zweite Abbruchroute waere eine zweite
    # Stelle, die man pflegen muss.

    @app.post("/api/bots/{name}/alle-schliessen/vorbereiten")
    async def alle_schliessen_vorbereiten(name: str, request: Request):
        """Notfallweg, Aufruf 1. Schreibt NICHTS - Uebersicht aller offenen
        Positionen samt Kursen und PnL-Schaetzung, plus Vorgangs-Kennung."""
        _bot_oder_404(name)
        bot = await asyncio.to_thread(datenquelle.finde_bot, name)
        if bot is None:
            raise HTTPException(status_code=404, detail=f"Unbekannter Bot: {name}")

        kurse, _ = await _kurse_holen([bot])
        try:
            return await asyncio.to_thread(schliessen.alle_vorbereiten, name, kurse)
        except schliessen.SchliessenNichtMoeglich as fehler:
            raise HTTPException(status_code=409, detail=str(fehler))

    @app.post("/api/bots/{name}/alle-schliessen/ausfuehren")
    async def alle_schliessen_ausfuehren(name: str, request: Request):
        """Notfallweg, Aufruf 2 - der zweite schreibende Endpunkt.

        Schliesst jede bestaetigte Position EINZELN ueber dieselbe
        Kernfunktion wie der Einzelweg. Ein Fehlschlag bei einer Position
        bricht den Rest NICHT ab; die Antwort nennt Erfolge, Fehlschlaege
        und Uebersprungene vollstaendig.

        Deshalb ist ein Teilausfall hier KEIN HTTP-Fehler: die Anfrage ist
        vollstaendig bearbeitet, das Ergebnis ist nur gemischt. Ein 409 mit
        Fehlertext wuerde verschweigen, was bereits geschlossen WURDE -
        genau die Unklarheit, die diese Funktion vermeiden soll.
        """
        _bot_oder_404(name)
        daten = await _koerper(request)
        try:
            return await asyncio.to_thread(
                schliessen.alle_ausfuehren, name, daten.get("vorgang"),
                _wer(request))
        except schliessen.SchliessenNichtMoeglich as fehler:
            # Nur noch die Faelle, in denen GAR NICHTS versucht wurde:
            # ungueltige, abgelaufene, fremde oder artfremde Kennung.
            raise HTTPException(status_code=409, detail=str(fehler))
        except Exception:
            logger.exception("Unerwarteter Fehler beim Notfall-Schliessen.")
            raise HTTPException(
                status_code=500,
                detail=("Unerwarteter Fehler - siehe Log. Welche Positionen "
                         "geschlossen wurden, bitte in der Positionsliste und "
                         "im Protokoll pruefen."))

    # -- Globaler Crash-Weg: ALLE Bots ------------------------------------
    # Bewusst NICHT unter /api/bots/{name}/... : dieser Weg gehoert zu keinem
    # Bot, sondern zu allen. Eine Route mit Bot-Platzhalter waere die
    # Einladung, ihn versehentlich fuer einen einzelnen aufzurufen.

    @app.post("/api/alle-bots-schliessen/vorbereiten")
    async def global_schliessen_vorbereiten(request: Request):
        """Crash-Weg, Aufruf 1. Schreibt NICHTS - Uebersicht aller offenen
        Positionen ALLER freigeschalteten Bots."""
        bots = await asyncio.to_thread(datenquelle.alle_bots)
        kurse, _ = await _kurse_holen(bots)
        try:
            return await asyncio.to_thread(schliessen.global_vorbereiten, kurse)
        except schliessen.SchliessenNichtMoeglich as fehler:
            raise HTTPException(status_code=409, detail=str(fehler))

    @app.post("/api/alle-bots-schliessen/ausfuehren")
    async def global_schliessen_ausfuehren(request: Request):
        """Crash-Weg, Aufruf 2 - der folgenreichste Endpunkt der Anwendung.

        Braucht die Vorgangs-Kennung aus Aufruf 1 UND den exakt getippten
        Text 'CRASH'. Schliesst je Bot ueber dieselbe Schleife wie der
        bot-weite Notfallweg, je Position ueber dieselbe Kernfunktion wie
        der Einzelweg.

        Wie beim bot-weiten Weg ist ein Teilausfall KEIN HTTP-Fehler,
        sondern ein Ergebnis: ein 409 wuerde verschweigen, was bereits
        geschlossen wurde - hier ueber neun Bots hinweg umso schlimmer.
        """
        daten = await _koerper(request)
        try:
            return await asyncio.to_thread(
                schliessen.global_ausfuehren, daten.get("vorgang"),
                daten.get("bestaetigung"), _wer(request))
        except schliessen.SchliessenNichtMoeglich as fehler:
            # Nur die Faelle, in denen GAR NICHTS versucht wurde: ungueltige,
            # abgelaufene oder artfremde Kennung, oder falscher CRASH-Text.
            raise HTTPException(status_code=409, detail=str(fehler))
        except Exception:
            logger.exception("Unerwarteter Fehler beim globalen Schliessen.")
            raise HTTPException(
                status_code=500,
                detail=("Unerwarteter Fehler - siehe Log. Welche Positionen "
                         "geschlossen wurden, bitte im Protokoll pruefen "
                         "(quelle=dashboard-crash)."))

    # Statische Dateien zuletzt einhaengen, damit die expliziten Routen
    # oben Vorrang haben. Der Zugriffsschutz greift auch hier, weil die
    # Middleware vor jedem Routing laeuft.
    app.mount("/statisch", StaticFiles(directory=konfig.STATIC_DIR), name="statisch")

    return app


def _login_html(fehler: bool = False) -> str:
    hinweis = ('<p class="fehler">Token nicht akzeptiert.</p>' if fehler else "")
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard-Anmeldung</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; background: #14171c;
         color: #e8ecf1; display: flex; min-height: 100vh; align-items: center;
         justify-content: center; margin: 0; }}
  form {{ background: #1d222a; padding: 24px; border-radius: 12px; width: 300px; }}
  h1 {{ font-size: 18px; margin: 0 0 16px; }}
  input {{ width: 100%; box-sizing: border-box; padding: 10px; border-radius: 8px;
           border: 1px solid #333b47; background: #12151a; color: #e8ecf1; }}
  button {{ width: 100%; margin-top: 12px; padding: 10px; border: 0; border-radius: 8px;
            background: #2f6f4f; color: #fff; font-size: 15px; }}
  .fehler {{ color: #e06c6c; font-size: 14px; }}
</style>
</head>
<body>
<form method="post" action="/login">
  <h1>Trading-Bot-Dashboard</h1>
  {hinweis}
  <input type="password" name="token" placeholder="Zugriffs-Token" autofocus
         autocomplete="current-password">
  <button type="submit">Anmelden</button>
</form>
</body>
</html>"""
