/* Dashboard-Frontend - reines JavaScript ohne Framework und ohne
   externe Bibliothek.

   ZUR DIAGRAMM-BIBLIOTHEK: Vorgeschlagen war Chart.js (oder etwas
   Vergleichbares). Stattdessen zeichnet linienDiagramm() unten ein
   schlichtes SVG selbst - rund 60 Zeilen. Gruende: (1) das Dashboard
   soll als PWA auch dann funktionieren, wenn gerade kein Internet da
   ist, ein CDN-Skript waere dann weg; (2) eine mitgelieferte Kopie von
   Chart.js waere ~200 KB fremder, ungepruefter Code im Repo; (3) die
   einzige benoetigte Darstellung ist eine Linie ueber der Zeit. Siehe
   README, Abschnitt Annahmen.

   ALLE Anfragen gehen an die eigene Herkunft und schicken das
   Anmelde-Cookie automatisch mit. Bei 401 wird auf die Login-Seite
   umgeleitet, statt eine leere Seite zu zeigen. */

/* Reihenfarben des Verlaufs-Diagramms. Die REIHENFOLGE ist hier der
   eigentliche Mechanismus, nicht die Auswahl: benachbarte Reihen muessen
   auch fuer Rot-Gruen-Blindheit unterscheidbar bleiben, und das haengt
   daran, welche Farbe neben welcher liegt.

   Die vorherige Liste tat das nicht: #e0a96a (orange) und #46b877 (gruen)
   standen nebeneinander und lagen fuer Protanopie bei Delta E 1.9 - fuer
   einen rot-gruen-blinden Leser praktisch dieselbe Linie. Nachgemessen,
   nicht geschaetzt (dataviz-Palettenpruefer, dunkle Flaeche #1a1f27).

   Diese Reihenfolge besteht alle Pruefungen: Helligkeitsband, Buntheit,
   Kontrast zur Flaeche, und als schlechtestes Nachbarpaar Delta E 8.4
   (Protanopie) bzw. 19.3 fuer normales Sehen. Wer sie aendert, sollte den
   Pruefer erneut laufen lassen - eine huebschere Farbe an falscher Stelle
   kippt das Ergebnis.

   Die Gesamtlinie ("Alle Bots zusammen") ist bewusst NICHT Teil dieser
   Liste: sie ist keine Kategorie neben den Bots, sondern deren Summe, und
   traegt deshalb Weiss. */
const FARBEN = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181",
                "#008300", "#9085e9", "#e66767", "#2aa6b8"];

/* --- Takt der automatischen Aktualisierung ---------------------------------
   Bewusst hier oben und nicht im Seitencode verstreut, damit sich die Werte
   an einer Stelle anpassen lassen.

   Die beiden Takte sind unterschiedlich, weil die dahinterliegenden
   Anfragen unterschiedlich teuer sind: /api/portfolio ist eine reine
   Datenbankabfrage ohne Netzwerkzugriff, /api/portfolio?live=1 loest je
   Aufruf echte Abfragen bei Binance und yfinance aus. Die Kurse werden
   deshalb deutlich seltener geholt - und selbst dann bleibt der Server
   durch asyncio.to_thread() plus Zeitgrenze abgesichert (siehe app.py),
   daran aendert die Automatik nichts. */
const AKTUALISIERUNG_DATEN_MS = 60 * 1000;        // Datenbank-Daten: jede Minute
const AKTUALISIERUNG_KURSE_MS = 150 * 1000;       // Live-Kurse: alle 2,5 Minuten

/* Die drei Zustaende einer automatischen Aktualisierung. Bewusst genau
   drei und bewusst sich gegenseitig ausschliessend: die Anzeige darf nie
   gleichzeitig "laedt gerade" und "veraltet" behaupten. Welcher Zustand
   gilt, entscheidet allein autoAktualisierung() - es gibt keine zweite
   Stelle, die an denselben Klassen dreht. */
const AKTUALISIERUNG_NORMAL   = "normal";     // Daten frisch, nichts laeuft
const AKTUALISIERUNG_LAEDT    = "laedt";      // Anfrage unterwegs
const AKTUALISIERUNG_VERALTET = "veraltet";   // letzter Versuch fehlgeschlagen

/* Mindestabstand zwischen zwei Laeufen derselben Aufgabe. Schuetzt davor,
   dass haeufiges Wechseln zwischen Apps auf dem iPhone (jedes
   Sichtbarwerden loest sofort einen Lauf aus) eine Anfrage-Lawine
   erzeugt. */
const MINDESTABSTAND_MS = 5 * 1000;

async function hole(pfad) {
  const antwort = await fetch(pfad, { credentials: "same-origin" });
  if (antwort.status === 401) {
    window.location.href = "/login";
    throw new Error("nicht angemeldet");
  }
  if (!antwort.ok) {
    throw new Error(`${pfad}: HTTP ${antwort.status}`);
  }
  return antwort.json();
}

/* Schreibender Aufruf. Bewusst getrennt von hole(): jede Stelle, die
   sende() benutzt, veraendert etwas - das soll im Quelltext auf einen
   Blick zu sehen sein und nicht in einem Parameter von hole() versteckt
   liegen.

   FastAPI verpackt Fehlermeldungen in {"detail": "..."}. Die Meldungen
   sind hier bewusst fuer den Nutzer geschrieben (siehe
   dashboard/schliessen.py), also werden sie durchgereicht statt durch
   ein generisches "Fehler 409" ersetzt. */
async function sende(pfad, koerper) {
  const antwort = await fetch(pfad, {
    method: "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(koerper || {}),
  });
  if (antwort.status === 401) {
    window.location.href = "/login";
    throw new Error("nicht angemeldet");
  }
  let daten = null;
  try { daten = await antwort.json(); } catch (e) { daten = null; }
  if (!antwort.ok) {
    throw new Error((daten && daten.detail) || `${pfad}: HTTP ${antwort.status}`);
  }
  return daten;
}

function zahl(wert, nachkomma = 2) {
  if (wert === null || wert === undefined) return "–";
  return Number(wert).toFixed(nachkomma);
}

function prozent(wert) {
  if (wert === null || wert === undefined) return '<span class="gedaempft">–</span>';
  const klasse = wert > 0 ? "gruen" : (wert < 0 ? "rot" : "gedaempft");
  const vorzeichen = wert > 0 ? "+" : "";
  return `<span class="${klasse}">${vorzeichen}${zahl(wert)}%</span>`;
}

/* Die Beschriftung der gewichteten Zahl steht an EINER Stelle und wird im
   Notfall-Dialog (bot.html), im Crash-Dialog (index.html) und in beiden
   Ergebnisanzeigen verwendet. Sie ist kein Beiwerk, sondern
   der Grund, warum diese Zahl überhaupt gezeigt werden darf: ohne sie wäre
   eine Backtest-Annahme als Live-Aussage hingestellt - genau die
   Verwechslung, die Methodik-Grundsatz 2 verhindern soll.

   Bewusst als SICHTBARER Text, nicht als title-Tooltip: dieses Dashboard wird
   überwiegend am iPhone benutzt, und dort gibt es kein Hover. Ein Tooltip wäre
   eine Beschriftung, die der eigentliche Nutzer nie sieht. */
const GEWICHTUNG_ERLAEUTERUNG =
  "Gewichtet nach der je Bot im Backtest <strong>angenommenen</strong> "
  + "Positionsgröße – keine echte Kapitalbindung und keine Portfolio-Rendite.";

function positionsgroesse(pct) {
  return `${zahl(pct, Number.isInteger(pct) ? 0 : 2)} %`;
}

/* Wie viele Positionen je Bot in die gewichtete Zahl eingehen.
   ==========================================================================
   Die gewichtete Zahl rechnet richtig, sagt aber nicht, WORAUS sie besteht.
   `elliott_wave` hat als einziger Bot kein MAX_CONCURRENT_POSITIONS und kann
   deshalb deutlich mehr Positionen gleichzeitig stellen als die anderen. Steht
   dann "Ø gewichtet -8 %" da, kann das der Durchschnitt über sieben Elliott-
   Positionen und eine einzige fremde sein - rechnerisch korrekt, aber
   faktisch die Aussage EINES Bots. Genau in dem Moment, in dem der Nutzer
   entscheidet, ob er alles schließt, darf das nicht unsichtbar sein.

   Die Zahlen werden nicht neu berechnet: `gewichte[].anzahl` zählt die
   Gewichtung ohnehin schon mit. Hier wird sie nur ausgewiesen.

   Wie GEWICHTUNG_ERLAEUTERUNG bewusst SICHTBARER Text, kein title-Tooltip:
   dieses Dashboard wird überwiegend am iPhone benutzt, und dort gibt es kein
   Hover. Und wie dort steht der Text an EINER Stelle, weil bot.html und
   index.html ihn beide brauchen. */
const POSITIONSANZAHL_ERLAEUTERUNG =
  "Bots ohne Obergrenze für gleichzeitige Positionen können die gewichtete "
  + "Zahl allein tragen.";

function positionsanzahlZeilen(g) {
  /* Diese Anzeige darf den Notfallweg unter KEINEN Umständen blockieren -
     dieselbe Regel wie bei der Positionsgröße. Fehlt das Feld (älteres
     Backend), fehlt die Liste oder fehlt eine einzelne Zahl, bleibt die Zeile
     weg bzw. steht ein Strich; geschlossen wird trotzdem. */
  if (!g || !Array.isArray(g.gewichte) || !g.gewichte.length) return [];
  const teile = g.gewichte.map((w) => {
    const wieviele = (w && w.anzahl !== null && w.anzahl !== undefined)
      ? w.anzahl : "–";
    return `${(w && (w.anzeigename || w.bot)) || "unbekannt"}: ${wieviele}`;
  });
  return [`<div class="hinweis-gewichtung">Eingegangene Positionen je Bot – `
          + `${teile.join("; ")}. ${POSITIONSANZAHL_ERLAEUTERUNG}</div>`];
}

function gewichtungsZeilen(g) {
  if (!g) return [];
  const zeilen = [];
  if (g.wert_pct !== null) {
    const groessen = g.gewichte.map((w) => positionsgroesse(w.allokation_pct)).join(" / ");
    zeilen.push(
      `<div><span class="beschriftung">Ø gewichtet</span><span>`
        + `${prozent(g.wert_pct)} &nbsp;<span class="gedaempft">`
        + `(Positionsgröße ${groessen}; dieselben Positionen ungewichtet `
        + `${prozent(g.ungewichtet_schnitt_pct)})</span></span></div>`,
      `<div class="hinweis-gewichtung">${GEWICHTUNG_ERLAEUTERUNG}</div>`);
  }
  /* Direkt unter der Zahl, nicht am Ende: wer sie liest, soll im selben Blick
     sehen, aus wie vielen Positionen je Bot sie besteht. */
  zeilen.push(...positionsanzahlZeilen(g));
  /* Ein Bot ohne dokumentierte Positionsgröße verschwindet NICHT stillschweigend
     aus der Rechnung - er wird benannt, mit Grund und mit seinem eigenen
     ungewichteten Durchschnitt. */
  if (g.nicht_gewichtbar && g.nicht_gewichtbar.length) {
    const liste = g.nicht_gewichtbar
      .map((n) => `${n.anzeigename}: ${n.anzahl} Position(en), ungewichtet `
                  + `${prozent(n.pnl_schnitt_pct)} – ${n.grund}`)
      .join("; ");
    zeilen.push(`<div class="hinweis-gewichtung">Ohne dokumentierte `
      + `Positionsgröße und deshalb <strong>aus der gewichteten Zahl `
      + `ausgenommen</strong> – ${liste}.</div>`);
  }
  return zeilen;
}

/* --- Zeitangaben ----------------------------------------------------------
   Alle Zeitangaben laufen ueber diese eine Stelle, damit Anzeige und
   Altersberechnung nicht auseinanderlaufen koennen.

   Der Server schickt Zeitpunkte, die er selbst erzeugt ("Stand", "Letzter
   Lauf"), als ISO-8601 MIT Zeitzonen-Offset. Erst dadurch ist der Wert
   eindeutig, und erst dann rechnet der Browser ihn in die Zeitzone des
   Geraets um - das ist der Kern der Korrektur. Vorher kam der "Stand" naiv
   in UTC, und die Anzeige stand zwei Stunden zurueck (Sommerzeit).

   Zeitpunkte OHNE Zeitzonenangabe gibt es weiterhin: die Einstiegs- und
   Ausstiegszeiten stammen unveraendert aus den Bot-Datenbanken und sind
   Kerzen-Zeitstempel des Marktes, keine Wanduhrzeit des Nutzers. Sie
   werden deshalb bewusst NICHT verschoben, sondern so gezeigt, wie sie
   dastehen.

   Das muss man erzwingen, weil JavaScript die beiden naiven Formen
   unterschiedlich liest: "2026-01-03T00:00:00" gilt laut Norm als
   Ortszeit, die reine Datumsform "2026-01-03" dagegen als UTC. Ohne die
   Ergaenzung unten wuerde ein Tages-Zeitstempel in Berlin als "01:00"
   erscheinen - und westlich von Greenwich sogar am Vortag. */

const ZEITZONE_IM_TEXT = /(Z|[+-]\d{2}:?\d{2})$/;

function zeitpunkt(iso) {
  if (!iso) return null;
  // Leerzeichen statt "T" ist die Form, die str(pandas.Timestamp) liefert.
  let text = String(iso).trim().replace(" ", "T");
  if (!ZEITZONE_IM_TEXT.test(text) && !text.includes("T")) {
    // reine Datumsform: als lokale Mitternacht lesen, nicht als UTC
    text += "T00:00:00";
  }
  const datum = new Date(text);
  return isNaN(datum) ? null : datum;
}

function zeit(iso) {
  if (!iso) return "–";
  const datum = zeitpunkt(iso);
  if (!datum) return iso;
  return datum.toLocaleString("de-DE", { day: "2-digit", month: "2-digit",
                                          hour: "2-digit", minute: "2-digit" });
}

function alterInStunden(iso) {
  const datum = zeitpunkt(iso);
  if (!datum) return null;
  return (Date.now() - datum.getTime()) / 3600000;
}

function zeigeFehler(text) {
  const bereich = document.getElementById("fehler");
  if (!bereich) return;
  // Leerer Text loescht den Block, statt eine leere rote Box zu zeigen -
  // wird von der automatischen Aktualisierung genutzt, um eine alte
  // Fehlermeldung nach einem geglueckten Versuch wieder wegzunehmen.
  bereich.innerHTML = text ? `<div class="hinweis">${text}</div>` : "";
}

function setzeHinweis(text) {
  const bereich = document.getElementById("kurshinweis");
  if (!bereich) return;
  bereich.innerHTML = text ? `<div class="hinweis">${text}</div>` : "";
}

/* --- SVG-Liniendiagramm ------------------------------------------------
   reihen: [{ name, farbe, punkte: [{x: Date-Millisekunden, y: Zahl}] }]
   Zeichnet eine Nulllinie, weil die dargestellte Groesse (kumulierte
   Prozentpunkte) sowohl positiv als auch negativ sein kann und die Lage
   zur Null die eigentliche Aussage ist. */
function linienDiagramm(behaelter, reihen) {
  const breite = 600, hoehe = 260, rand = { oben: 12, rechts: 12, unten: 24, links: 44 };
  const alle = reihen.flatMap(r => r.punkte);
  if (alle.length === 0) {
    behaelter.innerHTML = '<p class="gedaempft">Noch keine geschlossenen Trades.</p>';
    return;
  }

  const xMin = Math.min(...alle.map(p => p.x));
  const xMax = Math.max(...alle.map(p => p.x));
  let yMin = Math.min(0, ...alle.map(p => p.y));
  let yMax = Math.max(0, ...alle.map(p => p.y));
  if (yMin === yMax) { yMin -= 1; yMax += 1; }

  const zeichenBreite = breite - rand.links - rand.rechts;
  const zeichenHoehe = hoehe - rand.oben - rand.unten;
  const px = x => rand.links + (xMax === xMin ? zeichenBreite / 2
                                              : (x - xMin) / (xMax - xMin) * zeichenBreite);
  const py = y => rand.oben + (yMax - y) / (yMax - yMin) * zeichenHoehe;

  const teile = [];
  // Nulllinie und Achsenbeschriftung
  teile.push(`<line x1="${rand.links}" y1="${py(0)}" x2="${breite - rand.rechts}" y2="${py(0)}"
                    stroke="rgba(255,255,255,.07)" stroke-width="1"/>`);
  for (const wert of [yMax, 0, yMin]) {
    teile.push(`<text x="${rand.links - 6}" y="${py(wert) + 4}" fill="#97a3b2"
                      font-size="11" text-anchor="end">${wert.toFixed(0)}%</text>`);
  }
  teile.push(`<text x="${rand.links}" y="${hoehe - 6}" fill="#97a3b2" font-size="11">
                ${new Date(xMin).toLocaleDateString("de-DE")}</text>`);
  teile.push(`<text x="${breite - rand.rechts}" y="${hoehe - 6}" fill="#97a3b2" font-size="11"
                    text-anchor="end">${new Date(xMax).toLocaleDateString("de-DE")}</text>`);

  for (const reihe of reihen) {
    if (reihe.punkte.length === 0) continue;
    const d = reihe.punkte
      .map((p, i) => `${i === 0 ? "M" : "L"}${px(p.x).toFixed(1)},${py(p.y).toFixed(1)}`)
      .join(" ");
    teile.push(`<path d="${d}" fill="none" stroke="${reihe.farbe}" stroke-width="2"
                      stroke-linejoin="round" stroke-linecap="round"/>`);
  }

  behaelter.innerHTML =
    `<svg viewBox="0 0 ${breite} ${hoehe}" role="img" aria-label="Verlauf der kumulierten Trade-Ergebnisse">
       ${teile.join("\n")}
     </svg>`;
}

function legende(behaelter, reihen) {
  if (!behaelter) return;
  behaelter.innerHTML = reihen
    .filter(r => r.punkte.length > 0)
    .map(r => `<span><i style="background:${r.farbe}"></i>${r.name}</span>`)
    .join("");
}

function punkteAus(liste) {
  return liste
    // ueber zeitpunkt(), damit die Achse dieselbe Lesart benutzt wie die
    // Tabellen - sonst haette derselbe Wert zwei Bedeutungen.
    .map(p => ({ x: (zeitpunkt(p.zeitpunkt) || { getTime: () => NaN }).getTime(),
                  y: p.kumuliert_pct }))
    .filter(p => !isNaN(p.x) && p.y !== null && p.y !== undefined)
    .sort((a, b) => a.x - b.x);
}

/* --- Automatische Aktualisierung -------------------------------------------
   Ein kleiner Taktgeber je Aufgabe (Datenbank-Daten, Live-Kurse). Bewusst
   kein location.reload(): die Seite wird nie neu aufgebaut, es wird nur
   dieselbe Render-Funktion mit frischen Daten erneut aufgerufen. Wer gerade
   scrollt oder eine Tabelle liest, merkt davon nichts ausser aktualisierten
   Zahlen.

   Drei Eigenschaften, die den Unterschied zu einem blossen setInterval
   ausmachen:

   1. PAUSE IM HINTERGRUND. Laeuft nur, solange document.visibilityState
      "visible" ist. Liegt das iPhone gesperrt in der Tasche oder ist der
      Tab im Hintergrund, wird nichts abgefragt - das spart vor allem die
      teuren Kursabfragen. Wird die Seite wieder sichtbar und ist seither
      mehr Zeit vergangen als ein Takt, wird sofort nachgeladen, statt bis
      zum naechsten Tick zu warten (siehe die Bedingung in ausfuehren()
      fuer den Grund, warum nicht bei JEDEM Sichtbarwerden).
   2. KEINE UEBERLAPPUNG. Laeuft eine Abfrage noch (eine Kursabfrage darf
      bis zu 12 Sekunden dauern), wird der naechste Takt uebersprungen
      statt eine zweite Abfrage danebenzustellen.
   3. FEHLER LOESCHEN NICHTS. Schlaegt ein Lauf fehl, bleiben die zuletzt
      erfolgreich angezeigten Daten stehen. Sichtbar wird das nur an einer
      dezenten Markierung an der Stand-Anzeige; beim naechsten Takt wird
      es einfach erneut versucht.
   4. GENAU EIN ZUSTAND. Jeder Lauf durchlaeuft normal -> laedt -> normal
      bzw. -> veraltet. Der Wechsel passiert an genau einer Stelle (hier),
      nicht in einer zweiten, parallelen Anzeige-Logik. Wer wissen will,
      was angezeigt wird, muss nur diese Funktion lesen. */

function autoAktualisierung(ladefunktion, intervallMs, beiZustand, beschriftung) {
  let laeuft = false;
  let letzterStart = Date.now();   // die Seite hat gerade selbst geladen
  let fehlerInFolge = 0;
  const aufgabe = beschriftung || "Aktualisiere \u2026";

  function melde(zustand) {
    if (beiZustand) beiZustand(zustand, fehlerInFolge);
  }

  async function ausfuehren(grund) {
    if (laeuft) return;                                   // (2)
    if (Date.now() - letzterStart < MINDESTABSTAND_MS) return;
    // Beim Sichtbarwerden wird nur nachgeladen, wenn der Takt auch
    // faellig WAERE. Wer zwischen zwei Apps hin- und herwechselt, loest
    // sonst bei jedem Blick eine neue Kursabfrage bei Binance/yfinance
    // aus - und das widerspraeche dem Zweck der Sichtbarkeitspruefung.
    // Fuer den eigentlich gemeinten Fall (Seite war laenger weg als ein
    // Takt) aendert sich nichts: dann ist die Aufgabe faellig und laeuft
    // sofort, ohne auf den naechsten Tick zu warten.
    if (grund === "sichtbar" && Date.now() - letzterStart < intervallMs) return;
    laeuft = true;
    letzterStart = Date.now();
    // (4) Der Zustand wechselt VOR dem await auf LAEDT und im finally
    // zurueck - dadurch gibt es keinen Pfad, auf dem die Anzeige haengen
    // bleibt: auch ein geworfener Fehler kommt am finally vorbei.
    ladeanzeigeAn(aufgabe);
    melde(AKTUALISIERUNG_LAEDT);
    try {
      await ladefunktion(grund);
      fehlerInFolge = 0;
      melde(AKTUALISIERUNG_NORMAL);
    } catch (e) {                                          // (3)
      fehlerInFolge += 1;
      melde(AKTUALISIERUNG_VERALTET, e);
    } finally {
      laeuft = false;
      ladeanzeigeAus(aufgabe);
    }
  }

  setInterval(() => {
    if (document.visibilityState === "visible") ausfuehren("takt");  // (1)
  }, intervallMs);

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") ausfuehren("sichtbar");
  });

  return ausfuehren;
}

/* Dezente Rueckmeldung an der "Stand"-Anzeige (auf der Detailseite am
   Titel). Sie traegt IMMER GENAU EINEN der drei Zustaende - beide Klassen
   werden zuerst entfernt, dann wird hoechstens eine gesetzt. Damit ist ein
   Widerspruch ("blass wegen veraltet" UND "pulsiert wegen laedt")
   strukturell ausgeschlossen, nicht nur nach Absprache.

   Waehrend eines Versuchs NACH einem Fehlschlag gewinnt "laedt": das ist
   die aktuellere Aussage ("gerade passiert etwas"). Damit dabei nichts
   unter den Tisch faellt, nennt der Tooltip in diesem Fall beides. */
function markiereAktualisierung(elementId, zustand, fehlerInFolge) {
  const feld = document.getElementById(elementId);
  if (!feld) return;

  feld.classList.remove("laedt", "veraltet");

  if (zustand === AKTUALISIERUNG_LAEDT) {
    feld.classList.add("laedt");
    feld.title = fehlerInFolge > 0
      ? `Aktualisierung laeuft - der letzte Versuch war fehlgeschlagen (${fehlerInFolge}x).`
      : "Aktualisierung laeuft \u2026";
  } else if (zustand === AKTUALISIERUNG_VERALTET) {
    feld.classList.add("veraltet");
    feld.title = `Letzte Aktualisierung fehlgeschlagen (${fehlerInFolge}x). ` +
                 `Angezeigt werden die zuletzt erfolgreich geladenen Daten.`;
  } else {
    feld.title = "";
  }
}

/* --- Ladeanzeige im Kopfbereich --------------------------------------------
   Ein einziges kleines Element je Seite (#ladeanzeige), das nennt, WAS
   gerade laeuft. Warum eine Liste und nicht ein blosses An/Aus: die beiden
   Takte sind unabhaengig und koennen sich ueberlappen - der 60-Sekunden-Takt
   kann anlaufen, waehrend die Kursabfrage noch unterwegs ist (die darf bis
   zu 12 Sekunden dauern). Ein einfaches Flag wuerde dann beim Ende der
   kurzen Aufgabe auch die noch laufende lange ausblenden, und der Nutzer
   saehe waehrend der langsamsten Abfrage ueberhaupt nichts.

   Deshalb: jede Aufgabe meldet sich mit ihrer Beschriftung an und wieder
   ab; angezeigt wird, was gerade angemeldet ist. Ein Zaehler je
   Beschriftung ist nicht noetig, weil autoAktualisierung() ueberlappende
   Laeufe DERSELBEN Aufgabe ohnehin verhindert.

   aria-live="polite" am Element sorgt dafuer, dass Screenreader die
   Aenderung vorlesen, ohne den Nutzer mitten im Satz zu unterbrechen. */
const laufendeAufgaben = new Set();

function ladeanzeigeAn(beschriftung) {
  laufendeAufgaben.add(beschriftung);
  zeichneLadeanzeige();
}

function ladeanzeigeAus(beschriftung) {
  laufendeAufgaben.delete(beschriftung);
  zeichneLadeanzeige();
}

function zeichneLadeanzeige() {
  const feld = document.getElementById("ladeanzeige");
  if (!feld) return;
  const text = [...laufendeAufgaben].join(" \u00b7 ");
  feld.textContent = text;
  feld.title = text;
  // hidden statt display:none im Stylesheet - so bleibt der Zustand am
  // Element ablesbar und die Animation laeuft nicht unsichtbar weiter.
  feld.hidden = laufendeAufgaben.size === 0;
}

/* --- Boerse geschlossen: Warnschritt und wartende Auftraege ----------------
   Alles in diesem Abschnitt wird von BEIDEN Seiten benutzt (bot.html und
   index.html) und steht deshalb hier - genau wie GEWICHTUNG_ERLAEUTERUNG
   weiter oben. Der Warntext ist der Kern der neuen Funktion; zwei Fassungen
   davon wären die Doppelführung, bei der irgendwann nur noch eine Seite
   sagt, worauf sich der Nutzer einlässt.

   Was der Server liefert, sind FAKTEN (offen ja/nein, letzter Handelstag,
   nächste Öffnung als ISO-Zeitpunkt mit Offset). Der Satz daraus entsteht
   hier - so wie jede andere Beschriftung des Dashboards auch, und so
   stehen die Zeitpunkte in der Zeitzone des Geräts statt in UTC. */

/* Das Feld, mit dem der zusätzliche Warnschritt bestätigt wird. Es heißt
   auf beiden Seiten gleich und wird serverseitig geprüft (siehe
   dashboard/schliessen.py, WARTEAUFTRAG_BESTAETIGUNG). */
const WARTEAUFTRAG_FELD = "warteauftrag_bestaetigt";

function datum(iso) {
  if (!iso) return "–";
  const d = zeitpunkt(iso);
  if (!d) return String(iso);
  return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit",
                                          year: "numeric" });
}

/* Der Satz, um den es geht. Er nennt drei Dinge, und alle drei sind nötig:
   dass NICHT sofort geschlossen wird, wann stattdessen geschlossen wird,
   und dass dabei niemand mehr gefragt wird. Der dritte Punkt ist der neue
   und der unangenehmste - er steht deshalb nicht im Kleingedruckten. */
function warteauftragWarnung(boerse, anzahlText) {
  const b = boerse || {};
  const stand = b.letzter_handelstag
    ? `letzter Handelstag: ${datum(b.letzter_handelstag)}`
    : "letzter Handelstag unbekannt";
  const oeffnung = b.naechste_oeffnung
    ? `voraussichtlich am ${zeit(b.naechste_oeffnung)}`
    : "sobald sie wieder öffnet";
  return `<div class="warteauftrag-warnung">
      <strong>Die Börse ist aktuell geschlossen (${stand}).</strong>
      <div>${anzahlText} wird <strong>NICHT sofort geschlossen</strong>,
        sondern automatisch zum nächstmöglichen echten Kurs, sobald die
        Börse wieder öffnet – ${oeffnung}.</div>
      <div class="warteauftrag-tragweite">Das heißt: die Ausführung passiert
        <strong>später und ohne erneute Rückfrage</strong>. Zu welchem Kurs,
        steht jetzt noch nicht fest – der Markt bewegt sich bis dahin. Bis
        zur Ausführung lässt sich der Auftrag in der Liste „Wartende
        Aufträge“ stornieren.</div>
    </div>`;
}

/* --- Börsenstatus: was gerade gilt, VOR dem Klick ------------------------
   ==========================================================================
   Seit PR #71 wird ausserhalb der Handelszeiten vorgemerkt statt geschlossen.
   Das funktionierte, war aber erst IM Bestätigungsdialog zu sehen. Die
   US-Börsen öffnen in Berlin erst am Nachmittag, und ob gerade Feiertag oder
   Halbtag ist, weiss niemand auswendig — der Nutzer soll vor dem Klick
   wissen, in welcher der beiden Welten er sich befindet.

   Alles hier ist reine DARSTELLUNG. Die Fakten (offen ja/nein, nächste
   Öffnung, verkürzter Handelstag) kommen unverändert aus
   `notifications/boersenkalender.py` über `schliessen.boersenlage()`. Eine
   zweite Quelle für Handelszeiten wäre genau die Stelle, an der die Angaben
   später auseinanderlaufen.

   Die Unterscheidung Krypto/Aktien wird NICHT hier getroffen, sondern
   serverseitig in `boersenlage()`: für Krypto steht dort `kalender_gilt:
   false`, und daran hängt alles Weitere. Eine Fallunterscheidung je Ansicht
   wäre je Ansicht die Gelegenheit, sie einmal zu vergessen. */

const BOERSE_UNBEKANNT_TEXT =
  "Börsenstatus unbekannt – der Kalender gibt gerade keine Auskunft. "
  + "Aktien-Positionen lassen sich deshalb weder sofort schließen noch "
  + "vormerken; Krypto ist davon nicht betroffen.";

/* Wochentag + Uhrzeit in der Zeitzone des GERÄTS. `zeit()` liefert Datum und
   Uhrzeit — hier ist der Wochentag die eigentliche Information ("öffnet
   Montag" sagt mehr als "öffnet 14.09."), und die Uhrzeit entscheidet, ob
   sich das Warten lohnt. */
function boersenZeit(iso) {
  const d = zeitpunkt(iso);
  if (!d) return null;
  const tag = d.toLocaleDateString("de-DE", { weekday: "long" });
  const uhr = d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });
  return `${tag}, ${uhr} Uhr`;
}

/* Wie viele WERKTAGE liegen echt zwischen zwei Zeitpunkten?
   ==========================================================================
   Damit wird ein Feiertag von einem Wochenende unterschieden — und zwar ohne
   eine zweite Kalenderquelle. Der Gedanke: die Börse schliesst am letzten
   Handelstag und öffnet am nächsten. Liegt dazwischen ein WERKTAG ohne
   Sitzung, war das ein Feiertag.

       Do 20:00 zu, Fr 13:30 auf   -> nichts dazwischen        -> über Nacht
       Fr 20:00 zu, Mo 13:30 auf   -> Sa, So                   -> Wochenende
       Mi 21:00 zu, Fr 14:30 auf   -> Do (Werktag!)            -> Feiertag
       Do 20:00 zu, Mo 13:30 auf   -> Fr (Werktag!), Sa, So    -> Feiertag

   Gerechnet wird in UTC-Daten. Das ist hier zulässig und sogar sicherer als
   Gerätezeit: eine NYSE-Sitzung läuft 13:30–21:00 UTC und überschreitet nie
   eine UTC-Datumsgrenze, das UTC-Datum ist also immer der Handelstag. Auf
   Gerätezeit umgerechnet läge ein Handelsschluss in Berlin je nach Jahreszeit
   schon nach Mitternacht — und der Wochentag wäre um einen daneben. */
function werktageDazwischen(vonIso, bisIso) {
  const von = zeitpunkt(vonIso);
  const bis = zeitpunkt(bisIso);
  if (!von || !bis) return null;
  const tag = (d) => Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
  let werktage = 0;
  for (let t = tag(von) + 86400000; t < tag(bis); t += 86400000) {
    const wochentag = new Date(t).getUTCDay();
    if (wochentag !== 0 && wochentag !== 6) werktage += 1;
  }
  return werktage;
}

/* Welcher Fall liegt vor. EINE Stelle, die das entscheidet - Statuszeile und
   Knopfbeschriftung fragen beide hier. */
function boersenLage(boerse) {
  const b = boerse || {};
  if (!b.kalender_gilt) return "krypto";      // auch: gar keine Angabe da
  if (b.unbekannt) return "unbekannt";
  if (b.offen === true) return "offen";
  if (!b.naechste_oeffnung || !b.letzter_schluss) return "geschlossen";
  const werktage = werktageDazwischen(b.letzter_schluss, b.naechste_oeffnung);
  if (werktage === null) return "geschlossen";
  if (werktage > 0) return "feiertag";
  const tage = (zeitpunkt(b.naechste_oeffnung) - zeitpunkt(b.letzter_schluss))
                / 86400000;
  return tage > 1.5 ? "wochenende" : "geschlossen";
}

/* Die Statuszeile. Sichtbarer Text, kein title-Tooltip: dieses Dashboard wird
   überwiegend am iPhone benutzt, und dort gibt es kein Hover — dieselbe
   Begründung wie bei GEWICHTUNG_ERLAEUTERUNG.

   Gibt "" zurück, wenn es nichts zu sagen gibt (Krypto). Wirft nie: fehlt das
   Feld ganz, fehlt die Zeile, und geschlossen wird trotzdem. */
function boersenstatusZeile(boerse) {
  const b = boerse || {};
  const lage = boersenLage(b);
  if (lage === "krypto") return "";
  const boersenname = b.kalender || "Börse";

  if (lage === "unbekannt") {
    return `<div class="boersenstatus unbekannt">${BOERSE_UNBEKANNT_TEXT}</div>`;
  }

  if (lage === "offen") {
    const schluss = boersenZeit(b.naechster_schluss);
    /* Bei OFFENER Börse beschreibt `verkuerzter_handelstag` den laufenden
       Tag - deshalb "schließt heute früher". Bei geschlossener beschreibt es
       den NÄCHSTEN Handelstag, siehe unten. */
    const kurz = b.verkuerzter_handelstag
      ? ' <span class="boersenstatus-marke">verkürzter Handelstag</span>' : "";
    return `<div class="boersenstatus offen"><strong>${boersenname} geöffnet</strong>`
      + (schluss ? ` – schließt ${schluss}` : "") + kurz + `</div>`;
  }

  const anlass = { feiertag: " (Feiertag)", wochenende: " (Wochenende)" }[lage] || "";
  const oeffnung = boersenZeit(b.naechste_oeffnung);
  /* Hier beschreibt `verkuerzter_handelstag` den nächsten Handelstag - die
     Börse öffnet also, schließt aber früher als sonst. Das gehört dazu: wer
     auf die Öffnung wartet, plant sonst mit dem falschen Zeitfenster. */
  const kurz = b.verkuerzter_handelstag
    ? ' <span class="boersenstatus-marke">verkürzter Handelstag</span>' : "";
  return `<div class="boersenstatus zu"><strong>${boersenname} geschlossen`
    + `${anlass}</strong>`
    + (oeffnung ? ` – öffnet ${oeffnung}` : "") + kurz + `</div>`;
}

/* Heisst der Knopf "Schließen" oder "Vormerken"? Dieselbe EINE Quelle für
   alle drei Wege (Einzelposition, bot-weit, Crash) und beide Seiten. */
function wirdVorgemerkt(boerse) {
  return !!(boerse && boerse.kalender_gilt && boerse.warteauftrag_noetig);
}

/* Die Beschriftung des CRASH-Knopfes.
   ==========================================================================
   Dieser Knopf ist der einzige, der BEIDE Welten auf einmal trifft: Krypto
   handelt durchgehend, Aktien nicht. Bei geschlossener Börse wird ein Teil
   sofort geschlossen und ein Teil nur vorgemerkt — und genau das muss am
   Knopf stehen.

   GEWÄHLT: die Zahlen getrennt nennen, nicht zusammenfassen.

       offen         ⚠ ALLE 12 Positionen in 5 Bots schließen
       geschlossen   ⚠ 7 Krypto sofort schließen · 5 Aktien vormerken

   Verworfen wurden zwei bequemere Varianten:
     * „ALLE 12 Positionen schließen bzw. vormerken" — eine Zahl für zwei
       verschiedene Vorgänge. Wer sie liest, weiss hinterher nicht, wie viele
       Positionen nach dem Tap noch offen sind, und genau das ist im Crash-Fall
       die Frage.
     * die Beschriftung unverändert lassen und den Hinweis darunter erweitern —
       das war der Zustand vor dieser Änderung. Der Hinweis wird im Ernstfall
       nicht gelesen, der Knopftext schon; er ist das Letzte, was vor dem Tap
       im Blick ist.

   Ist nur EINE der beiden Welten betroffen, steht auch nur eine Zahl da: eine
   Zeile „0 Krypto sofort schließen" wäre Rauschen.

   Wirft nie. Fehlt die Börsenlage, fehlt die Aufteilung und der Text bleibt
   der bisherige — geschlossen wird trotzdem. */
function crashKnopfText(bots, offenGesamt, anzahlBots, boerse) {
  const unveraendert = `⚠ ALLE ${offenGesamt} Positionen in ${anzahlBots} Bots schließen`;
  if (!wirdVorgemerkt(boerse)) return unveraendert;

  const zaehle = (klasse) => (bots || [])
    .filter((b) => b && b.anlageklasse === klasse)
    .reduce((summe, b) => summe + (b.offene_positionen || 0), 0);
  const aktien = zaehle("aktien");
  const krypto = zaehle("krypto");
  /* Ergibt die Aufteilung nicht die Gesamtzahl, stimmt eine Annahme über die
     Daten nicht (eine dritte Anlageklasse, ein fehlendes Feld). Dann lieber
     die alte, sicher richtige Beschriftung als eine falsche Aufteilung. */
  if (aktien + krypto !== offenGesamt || aktien === 0) return unveraendert;

  const teile = [];
  if (krypto > 0) teile.push(`${krypto} Krypto sofort schließen`);
  teile.push(`${aktien} Aktien vormerken`);
  return `⚠ ${teile.join(" · ")}`;
}

/* Kurzform für die Fußnote unter der Positionstabelle bzw. den Crash-Bereich -
   dieselbe Aussage in einem Satz, ohne den Dialog nachzubauen. */
function warteauftragHinweisKurz(boerse) {
  const b = boerse || {};
  if (b.unbekannt) {
    return "Der Börsenkalender gibt gerade keine Auskunft – Aktien-Positionen "
      + "lassen sich deshalb weder sofort schließen noch vormerken.";
  }
  if (!b.warteauftrag_noetig) return "";
  const oeffnung = b.naechste_oeffnung ? ` (${zeit(b.naechste_oeffnung)})` : "";
  return "Die Börse ist geschlossen: Ein Schließen legt jetzt einen "
    + `Warteauftrag an und wird erst bei der nächsten Öffnung${oeffnung} `
    + "ausgeführt – dann ohne erneute Rückfrage.";
}

/* Eine Zeile je wartendem Auftrag. `mitBot` blendet die Bot-Spalte ein -
   auf der Übersichtsseite stehen die Aufträge aller Bots zusammen, auf der
   Bot-Seite nur die des einen. */
function warteauftragZeile(a, mitBot) {
  const zustand = a.noch_offen === false
    ? '<span class="gedaempft">Position ist nicht mehr offen – der Auftrag '
      + 'wird beim nächsten Lauf abgeräumt</span>'
    : (a.letzter_fehler
        ? `<span class="rot">${a.versuche} Fehlversuch(e): ${a.letzter_fehler}</span>`
        : '<span class="gedaempft">wartet auf die nächste Börsenöffnung</span>');
  return `<tr>
    ${mitBot ? `<td data-spalte="Bot">${a.anzeigename}</td>` : ""}
    <td data-spalte="Symbol">${a.symbol}</td>
    <td data-spalte="Angefordert">${zeit(a.angefordert_am)}</td>
    <td data-spalte="Zustand">${zustand}</td>
    <td data-spalte="Aktion"><button type="button"
        class="knopf stornieren-knopf" data-id="${a.id}">Stornieren</button></td>
  </tr>`;
}

/* Zeichnet den ganzen Bereich (Überschrift, Tabelle, Fußnote) und blendet
   ihn aus, wenn nichts wartet. Ein leerer Block mit der Überschrift
   „Wartende Aufträge“ würde sonst dauerhaft behaupten, es gäbe welche. */
function zeichneWarteauftraege(daten, mitBot) {
  const bereich = document.getElementById("warteauftraege-bereich");
  if (!bereich) return;
  const liste = (daten && daten.auftraege) || [];
  bereich.hidden = liste.length === 0;
  if (bereich.hidden) return;

  document.getElementById("warteauftraege-tabelle").innerHTML =
    liste.map((a) => warteauftragZeile(a, mitBot)).join("");
  const b = (daten && daten.boerse) || {};
  const zustand = b.offen === true
    ? "Die Börse ist offen – der nächste Lauf des Ausführungsskripts "
      + "schließt diese Positionen."
    : (b.naechste_oeffnung
        ? `Ausführung ab der nächsten Börsenöffnung (${zeit(b.naechste_oeffnung)}).`
        : "Ausführung bei der nächsten Börsenöffnung.");
  document.getElementById("warteauftraege-hinweis").innerHTML =
    `${liste.length} wartende(r) Auftrag/Aufträge. ${zustand} `
    + "Ausgeführt wird <strong>ohne erneute Rückfrage</strong>, durch den "
    + "Cronjob <code>dashboard/warteauftraege_ausfuehren.py</code>. "
    + "Stornieren verhindert die Ausführung und ändert sonst nichts.";
}

/* Stornieren ist die risikosenkende Richtung und braucht deshalb KEINE
   Rückfrage - es verhindert einen Schreibzugriff, statt einen auszulösen.
   Der Aufrufer übergibt, was danach neu geladen werden soll. */
async function storniereWarteauftrag(id, danach) {
  const ergebnis = await sende("/api/warteauftraege/stornieren", { id: id });
  const feld = document.getElementById("erfolg");
  if (feld) {
    feld.innerHTML = `<div class="erfolgsmeldung">✅ ${ergebnis.meldung}</div>`;
  }
  if (danach) await danach();
  return ergebnis;
}
