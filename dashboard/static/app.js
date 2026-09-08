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

const FARBEN = ["#6aa9e0", "#46b877", "#e0a96a", "#c78ae0", "#e06c6c",
                "#6ae0d2", "#e0d76a", "#8a9ae0", "#a0e06a"];

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

function zeit(iso) {
  if (!iso) return "–";
  const datum = new Date(iso);
  if (isNaN(datum)) return iso;
  return datum.toLocaleString("de-DE", { day: "2-digit", month: "2-digit",
                                          hour: "2-digit", minute: "2-digit" });
}

function alterInStunden(iso) {
  if (!iso) return null;
  const datum = new Date(iso);
  if (isNaN(datum)) return null;
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
                    stroke="#3a434f" stroke-width="1"/>`);
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
    .map(p => ({ x: new Date(p.zeitpunkt).getTime(), y: p.kumuliert_pct }))
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
      es einfach erneut versucht. */

function autoAktualisierung(ladefunktion, intervallMs, beiFehlerstatus) {
  let laeuft = false;
  let letzterStart = Date.now();   // die Seite hat gerade selbst geladen
  let fehlerInFolge = 0;

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
    try {
      await ladefunktion(grund);
      fehlerInFolge = 0;
      if (beiFehlerstatus) beiFehlerstatus(0);
    } catch (e) {                                          // (3)
      fehlerInFolge += 1;
      if (beiFehlerstatus) beiFehlerstatus(fehlerInFolge, e);
    } finally {
      laeuft = false;
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

/* Dezente Rueckmeldung an der "Stand"-Anzeige: nach einem fehlgeschlagenen
   Versuch bekommt sie eine gedaempfte Markierung und einen Tooltip, mehr
   nicht. Kein Banner, keine Fehlermeldung ueber der Seite - die angezeigten
   Zahlen sind ja weiterhin gueltig, nur eben nicht mehr taufrisch. */
function markiereAktualisierung(elementId, fehlerInFolge) {
  const feld = document.getElementById(elementId);
  if (!feld) return;
  if (fehlerInFolge > 0) {
    feld.classList.add("veraltet");
    feld.title = `Letzte Aktualisierung fehlgeschlagen (${fehlerInFolge}x). ` +
                 `Angezeigt werden die zuletzt erfolgreich geladenen Daten.`;
  } else {
    feld.classList.remove("veraltet");
    feld.title = "";
  }
}
