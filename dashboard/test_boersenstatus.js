/* Verhaltenstest des Börsenstatus (Node, ohne Browser)
   ===============================================================
   Prueft nicht, wie der Code GESCHRIEBEN ist, sondern was er ERZEUGT: die
   Funktionen aus app.js, index.html und bot.html werden wirklich ausgefuehrt
   und ihre Ausgabe geprueft.

   Warum das noetig ist: eine Textsuche bleibt gruen, wenn ein if-Zweig auf
   `false` steht - der gesuchte Text liegt dann unerreichbar im Rumpf. Und
   sie bleibt gruen, wenn nur EINE der beiden Ansichten die Angabe zeigt.
   Genau diese Fehlerklasse ist in PR #62, #66, #67 und #73 viermal
   aufgetreten. Deshalb wird hier JE FUNKTION ausgefuehrt, in beiden
   Ansichten.

   Die Faelle (offen, nach Handelsschluss, Wochenende, Feiertag, Halbtag)
   sind KEINE erfundenen Zahlen: sie stammen aus dem echten
   notifications/boersenkalender.py, abgefragt zu Zeitpunkten, die der Test
   kennt. Vorgefertigt liegen sie unten - so laeuft dieser Test auch ohne
   Python und ohne die Kalender-Bibliothek.

   Aufruf:  node dashboard/test_boersenstatus.js
   Wird von test_dashboard.py mitgestartet, sofern node vorhanden ist.
*/

const fs = require("fs");
const path = require("path");
const vm = require("vm");

let bestanden = 0;
const fehler = [];

function check(name, ok, detail) {
  if (ok) {
    bestanden += 1;
    console.log(`  [OK ] ${name}` + (detail ? `   ${detail}` : ""));
  } else {
    fehler.push(name);
    console.log(`  [FEHLER] ${name}` + (detail ? `   ${detail}` : ""));
  }
}

/* Eine Funktion aus einer Quelldatei herausschneiden. Beide Dateien
   schreiben jede Funktion linksbuendig, die schliessende Klammer steht also
   in Spalte 1. */
function funktion(quelle, kopf) {
  const start = quelle.indexOf(kopf);
  if (start < 0) throw new Error(`nicht gefunden: ${kopf}`);
  const ende = quelle.indexOf("\n}", start);
  if (ende < 0) throw new Error(`kein Ende gefunden: ${kopf}`);
  return quelle.slice(start, ende + 2);
}

function konstante(quelle, name) {
  const treffer = quelle.match(new RegExp(`const ${name} =[\\s\\S]*?;\\n`));
  if (!treffer) throw new Error(`nicht gefunden: const ${name}`);
  return treffer[0];
}

const statisch = path.join(__dirname, "static");
const appJs = fs.readFileSync(path.join(statisch, "app.js"), "utf8");
const indexHtml = fs.readFileSync(path.join(statisch, "index.html"), "utf8");
const botHtml = fs.readFileSync(path.join(statisch, "bot.html"), "utf8");

/* --- Minimaler DOM-Ersatz ------------------------------------------------
   Merkt sich je Element innerHTML, textContent und hidden. Reicht fuer die
   vier Zeichenfunktionen; alles Weitere braucht der Browser. */
function neuesDokument(bekannteSpalten = 5) {
  const elemente = {};
  const hole = (id) => {
    if (!elemente[id]) {
      elemente[id] = {
        innerHTML: "", textContent: "", hidden: false,
        // nur fuer #positionen-kopf: zeichnePositionen() zaehlt die Spalten
        querySelectorAll: () => new Array(bekannteSpalten).fill({}),
        appendChild: () => { elemente[id].spalteErgaenzt = true; },
      };
    }
    return elemente[id];
  };
  return {
    dokument: { getElementById: hole, createElement: () => ({}) },
    elemente,
  };
}

/* --- Die Faelle, aus dem echten Kalender geholt -------------------------- */
const BASIS = {
  anlageklasse: "aktien", kalender_gilt: true, unbekannt: false,
  kalender: "NYSE", grund: "…",
};
const FALL = {
  offen: { ...BASIS, offen: true, handelbar_jetzt: true, warteauftrag_noetig: false,
    letzter_handelstag: "2026-09-09", letzter_schluss: "2026-09-09T20:00:00+00:00",
    naechste_oeffnung: "2026-09-11T13:30:00+00:00",
    naechster_schluss: "2026-09-10T20:00:00+00:00", verkuerzter_handelstag: false },
  nachSchluss: { ...BASIS, offen: false, handelbar_jetzt: false, warteauftrag_noetig: true,
    letzter_handelstag: "2026-09-10", letzter_schluss: "2026-09-10T20:00:00+00:00",
    naechste_oeffnung: "2026-09-11T13:30:00+00:00",
    naechster_schluss: "2026-09-11T20:00:00+00:00", verkuerzter_handelstag: false },
  wochenende: { ...BASIS, offen: false, handelbar_jetzt: false, warteauftrag_noetig: true,
    letzter_handelstag: "2026-09-11", letzter_schluss: "2026-09-11T20:00:00+00:00",
    naechste_oeffnung: "2026-09-14T13:30:00+00:00",
    naechster_schluss: "2026-09-14T20:00:00+00:00", verkuerzter_handelstag: false },
  // Thanksgiving 2026 (beweglich): Mi zu, Fr wieder auf - und der Fr ist ein Halbtag
  feiertag: { ...BASIS, offen: false, handelbar_jetzt: false, warteauftrag_noetig: true,
    letzter_handelstag: "2026-11-25", letzter_schluss: "2026-11-25T21:00:00+00:00",
    naechste_oeffnung: "2026-11-27T14:30:00+00:00",
    naechster_schluss: "2026-11-27T18:00:00+00:00", verkuerzter_handelstag: true },
  // Karfreitag 2026 (osterabhaengig): Do zu, Mo wieder auf
  karfreitag: { ...BASIS, offen: false, handelbar_jetzt: false, warteauftrag_noetig: true,
    letzter_handelstag: "2026-04-02", letzter_schluss: "2026-04-02T20:00:00+00:00",
    naechste_oeffnung: "2026-04-06T13:30:00+00:00",
    naechster_schluss: "2026-04-06T20:00:00+00:00", verkuerzter_handelstag: false },
  // der verkuerzte Tag selbst, waehrend er laeuft
  halbtag: { ...BASIS, offen: true, handelbar_jetzt: true, warteauftrag_noetig: false,
    letzter_handelstag: "2026-11-25", letzter_schluss: "2026-11-25T21:00:00+00:00",
    naechste_oeffnung: "2026-11-30T14:30:00+00:00",
    naechster_schluss: "2026-11-27T18:00:00+00:00", verkuerzter_handelstag: true },
  unbekannt: { ...BASIS, offen: null, handelbar_jetzt: false, warteauftrag_noetig: false,
    unbekannt: true, letzter_handelstag: null, letzter_schluss: null,
    naechste_oeffnung: null, naechster_schluss: null, verkuerzter_handelstag: null },
  krypto: { anlageklasse: "krypto", kalender_gilt: false, offen: null,
    handelbar_jetzt: true, warteauftrag_noetig: false, unbekannt: false,
    kalender: null, letzter_handelstag: null, letzter_schluss: null,
    naechste_oeffnung: null, naechster_schluss: null, verkuerzter_handelstag: null },
};

const nurText = (html) => String(html).replace(/<[^>]+>/g, " ")
  .replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim();

/* ======================================================================
   1) app.js - die gemeinsame Quelle
   ====================================================================== */
console.log("\n1) app.js: Lage, Statuszeile, Knopfentscheidung");

const app = {};
vm.runInNewContext([
  konstante(appJs, "ZEITZONE_IM_TEXT"),
  funktion(appJs, "function zeitpunkt("),
  funktion(appJs, "function zeit("),
  konstante(appJs, "BOERSE_UNBEKANNT_TEXT"),
  funktion(appJs, "function boersenZeit("),
  funktion(appJs, "function werktageDazwischen("),
  funktion(appJs, "function boersenLage("),
  funktion(appJs, "function boersenstatusZeile("),
  funktion(appJs, "function wirdVorgemerkt("),
  funktion(appJs, "function crashKnopfText("),
  funktion(appJs, "function datum("),
  funktion(appJs, "function warteauftragHinweisKurz("),
  `this.boersenLage = boersenLage;
   this.boersenstatusZeile = boersenstatusZeile;
   this.wirdVorgemerkt = wirdVorgemerkt;
   this.crashKnopfText = crashKnopfText;
   this.werktageDazwischen = werktageDazwischen;`,
].join("\n\n"), app);

/* Die Unterscheidung Feiertag/Wochenende haengt allein daran - deshalb
   zuerst die Rechnung selbst, an Faellen mit bekannter Antwort. */
check("Werktage zwischen Do-Schluss und Fr-Oeffnung: keine (ueber Nacht)",
      app.werktageDazwischen("2026-09-10T20:00:00+00:00",
                              "2026-09-11T13:30:00+00:00") === 0);
check("Zwischen Fr-Schluss und Mo-Oeffnung: keine (nur Sa/So)",
      app.werktageDazwischen("2026-09-11T20:00:00+00:00",
                              "2026-09-14T13:30:00+00:00") === 0);
check("Zwischen Mi-Schluss und Fr-Oeffnung: EINER (Thanksgiving)",
      app.werktageDazwischen("2026-11-25T21:00:00+00:00",
                              "2026-11-27T14:30:00+00:00") === 1);
check("Zwischen Do-Schluss und Mo-Oeffnung: EINER (Karfreitag, Sa/So zaehlen nicht)",
      app.werktageDazwischen("2026-04-02T20:00:00+00:00",
                              "2026-04-06T13:30:00+00:00") === 1);

const erwarteteLage = {
  offen: "offen", nachSchluss: "geschlossen", wochenende: "wochenende",
  feiertag: "feiertag", karfreitag: "feiertag", halbtag: "offen",
  unbekannt: "unbekannt", krypto: "krypto",
};
for (const [name, erwartet] of Object.entries(erwarteteLage)) {
  const ist = app.boersenLage(FALL[name]);
  check(`Lage "${name}" wird als "${erwartet}" erkannt`, ist === erwartet, ist);
}

const zeile = (fall) => nurText(app.boersenstatusZeile(FALL[fall]));

check("OFFEN: nennt die Boerse und den Handelsschluss",
      zeile("offen").includes("NYSE geöffnet")
      && /schließt \w+, \d{2}:\d{2} Uhr/.test(zeile("offen")), zeile("offen"));
check("GESCHLOSSEN: nennt die naechste Oeffnung mit Wochentag und Uhrzeit",
      /öffnet \w+, \d{2}:\d{2} Uhr/.test(zeile("wochenende")), zeile("wochenende"));
check("FEIERTAG steht als solcher da, nicht bloss \"geschlossen\"",
      zeile("feiertag").includes("(Feiertag)")
      && zeile("karfreitag").includes("(Feiertag)"), zeile("feiertag"));
check("WOCHENENDE wird vom Feiertag unterschieden",
      zeile("wochenende").includes("(Wochenende)")
      && !zeile("wochenende").includes("Feiertag"), zeile("wochenende"));
check("HALBTAG wird ausgewiesen - bei offener Boerse",
      zeile("halbtag").includes("verkürzter Handelstag"), zeile("halbtag"));
check("... und bei geschlossener, weil dann der NAECHSTE Tag gemeint ist",
      zeile("feiertag").includes("verkürzter Handelstag"), zeile("feiertag"));
check("Der Halbtag steht NICHT an einem gewoehnlichen Tag",
      !zeile("offen").includes("verkürzter")
      && !zeile("wochenende").includes("verkürzter"));
check("UNBEKANNT sagt, dass weder geschlossen noch vorgemerkt wird",
      zeile("unbekannt").includes("unbekannt")
      && zeile("unbekannt").includes("weder"), zeile("unbekannt").slice(0, 70));

/* Sichtbarer Text, kein title-Tooltip - am iPhone gibt es kein Hover. */
const rohOffen = app.boersenstatusZeile(FALL.offen);
check("Die Zeile ist sichtbarer Text, kein title-Tooltip",
      rohOffen.includes('class="boersenstatus')
      && !/title\s*=/.test(app.boersenstatusZeile(FALL.wochenende)));

/* KRYPTO: fuer die aendert sich nichts. Die Unterscheidung faellt an EINER
   Stelle (kalender_gilt), nicht je Ansicht. */
check("KRYPTO bekommt gar keine Zeile",
      app.boersenstatusZeile(FALL.krypto) === "");
check("Und auch keinen Knopfwechsel",
      app.wirdVorgemerkt(FALL.krypto) === false);

/* Entschieden wird an `kalender_gilt`, NICHT an `warteauftrag_noetig`.
   Der Unterschied sieht nach Haarspalterei aus, ist aber die ganze
   Zusicherung: `kalender_gilt` ist das Feld, das Krypto von Aktien trennt,
   und es steht genau einmal im Backend (schliessen.boersenlage). Wer hier
   nur `warteauftrag_noetig` prüft, verlässt sich darauf, dass das Backend
   für Krypto nie etwas anderes schickt - und hat die Unterscheidung damit
   stillschweigend in die Anzeige verlegt. Gegenprobe M6: genau so gefunden. */
const krummeKryptoLage = { ...FALL.krypto, warteauftrag_noetig: true };
check("Krypto bleibt Krypto, auch wenn warteauftrag_noetig gesetzt wäre",
      app.wirdVorgemerkt(krummeKryptoLage) === false
      && app.boersenstatusZeile(krummeKryptoLage) === ""
      && app.boersenLage(krummeKryptoLage) === "krypto",
      "die Unterscheidung hängt an kalender_gilt, nicht am Folgefeld");

/* Der Notfallweg darf nie blockiert werden. */
let geworfen = null;
try {
  for (const wert of [null, undefined, {}, { kalender_gilt: true },
                       { kalender_gilt: true, offen: false },
                       { kalender_gilt: true, offen: false,
                         letzter_schluss: "kaputt", naechste_oeffnung: "auch" }]) {
    app.boersenstatusZeile(wert);
    app.wirdVorgemerkt(wert);
    app.boersenLage(wert);
  }
} catch (e) { geworfen = e; }
check("Fehlende oder kaputte Angaben werfen NICHT - die Anzeige blockiert nie",
      geworfen === null, geworfen ? String(geworfen).slice(0, 90) : "");
check("Ohne Angabe bleibt die Zeile leer statt falsch",
      app.boersenstatusZeile(null) === ""
      && app.boersenstatusZeile(undefined) === "");
check("Und ohne Angabe wird NICHT vorgemerkt - der Knopf bleibt \"Schließen\"",
      app.wirdVorgemerkt(null) === false && app.wirdVorgemerkt({}) === false);

/* ======================================================================
   2) index.html - Uebersichtsseite: Statuszeile UND Crash-Knopf
   ====================================================================== */
console.log("\n2) index.html: Statuszeile und Crash-Knopf (erzeugte Ausgabe)");

function uebersichtBauen(boerse, bots) {
  const { dokument, elemente } = neuesDokument();
  const ctx = {
    document: dokument,
    console,
  };
  vm.runInNewContext([
    konstante(appJs, "ZEITZONE_IM_TEXT"),
    funktion(appJs, "function zeitpunkt("),
    funktion(appJs, "function zeit("),
    funktion(appJs, "function zahl("),
    funktion(appJs, "function prozent("),
    funktion(appJs, "function datum("),
    funktion(appJs, "function alterInStunden("),
    konstante(appJs, "BOERSE_UNBEKANNT_TEXT"),
    funktion(appJs, "function boersenZeit("),
    funktion(appJs, "function werktageDazwischen("),
    funktion(appJs, "function boersenLage("),
    funktion(appJs, "function boersenstatusZeile("),
    funktion(appJs, "function wirdVorgemerkt("),
    funktion(appJs, "function crashKnopfText("),
    funktion(appJs, "function warteauftragHinweisKurz("),
    funktion(indexHtml, "function botZeile("),
    "let letzteBoerse = null;",
    funktion(indexHtml, "function zeichneBoersenstatus("),
    funktion(indexHtml, "function zeichneUebersicht("),
    "this.zeichneUebersicht = zeichneUebersicht;",
  ].join("\n\n"), ctx);

  ctx.zeichneUebersicht({
    boerse,
    summe: { anzahl_bots: 9, offene_positionen: 12, geschlossene_trades: 100,
              pnl_heute: 1.0, summe_pnl_prozentpunkte: 5.0 },
    bots,
    abgerufen_am: "2026-09-11T12:00:00+02:00",
  });
  return elemente;
}

const BOTS = [
  { name: "t3_supertrend", anzeigename: "T3", anlageklasse: "krypto",
    offene_positionen: 7, geschlossene_trades: 10, pnl_heute: 0, summe_pnl: 1,
    trefferquote: 50, aktueller_stand: 1, letzter_lauf: "2026-09-11T10:00:00+02:00" },
  { name: "volatility_breakout", anzeigename: "VB", anlageklasse: "aktien",
    offene_positionen: 5, geschlossene_trades: 10, pnl_heute: 0, summe_pnl: 1,
    trefferquote: 50, aktueller_stand: 1, letzter_lauf: "2026-09-11T10:00:00+02:00" },
];

const uebersichtZu = uebersichtBauen(FALL.wochenende, BOTS);
check("Die Uebersicht zeigt die Statuszeile wirklich an",
      nurText(uebersichtZu["boersenstatus"].innerHTML).includes("NYSE geschlossen"),
      nurText(uebersichtZu["boersenstatus"].innerHTML));
check("Mit Wochentag und Uhrzeit der naechsten Oeffnung",
      /öffnet \w+, \d{2}:\d{2} Uhr/.test(
        nurText(uebersichtZu["boersenstatus"].innerHTML)));

/* Der Crash-Knopf ist der einzige, der beide Welten trifft. Bei
   geschlossener Boerse darf er NICHT behaupten, alles werde geschlossen. */
const knopfZu = uebersichtZu["crash-knopf"].textContent;
check("Crash-Knopf nennt beide Bereiche GETRENNT, mit eigenen Zahlen",
      knopfZu.includes("7 Krypto") && knopfZu.includes("5 Aktien"), knopfZu);
check("... und sagt fuer die Aktien \"vormerken\", nicht \"schließen\"",
      /5 Aktien vormerken/.test(knopfZu), knopfZu);
check("Keine Formulierung, die ALLES als sofort geschlossen hinstellt",
      !/ALLE 12 Positionen .* schließen/.test(knopfZu), knopfZu);
check("Der Crash-Hinweis nennt den Warteauftrag ebenfalls",
      nurText(uebersichtZu["crash-hinweis"].innerHTML).includes("Warteauftrag"),
      nurText(uebersichtZu["crash-hinweis"].innerHTML).slice(-90));

const uebersichtOffen = uebersichtBauen(FALL.offen, BOTS);
check("Bei OFFENER Boerse bleibt der Crash-Knopf wie bisher",
      uebersichtOffen["crash-knopf"].textContent
        === "⚠ ALLE 12 Positionen in 2 Bots schließen",
      uebersichtOffen["crash-knopf"].textContent);
check("Und die Statuszeile sagt \"geöffnet\"",
      nurText(uebersichtOffen["boersenstatus"].innerHTML).includes("NYSE geöffnet"));

const uebersichtKrypto = uebersichtBauen(
  FALL.wochenende, [BOTS[0]]);
check("Nur Krypto offen: keine Aufteilung, der Text bleibt der bisherige",
      uebersichtKrypto["crash-knopf"].textContent
        === "⚠ ALLE 7 Positionen in 1 Bots schließen",
      uebersichtKrypto["crash-knopf"].textContent);

const uebersichtOhne = uebersichtBauen(null, BOTS);
check("Ohne Boersenlage: Zeile leer, Knopf unveraendert, nichts bricht",
      uebersichtOhne["boersenstatus"].innerHTML === ""
      && uebersichtOhne["crash-knopf"].textContent
         === "⚠ ALLE 12 Positionen in 2 Bots schließen",
      uebersichtOhne["crash-knopf"].textContent);

/* ======================================================================
   3) bot.html - Bot-Seite: Statuszeile, Einzelknopf, Notfallknopf
   ====================================================================== */
console.log("\n3) bot.html: Statuszeile und beide Knoepfe (erzeugte Ausgabe)");

function botSeiteBauen(boerse, positionen) {
  const { dokument, elemente } = neuesDokument(6);
  const ctx = { document: dokument, console };
  vm.runInNewContext([
    konstante(appJs, "ZEITZONE_IM_TEXT"),
    funktion(appJs, "function zeitpunkt("),
    funktion(appJs, "function zeit("),
    funktion(appJs, "function zahl("),
    funktion(appJs, "function prozent("),
    funktion(appJs, "function datum("),
    konstante(appJs, "BOERSE_UNBEKANNT_TEXT"),
    funktion(appJs, "function boersenZeit("),
    funktion(appJs, "function werktageDazwischen("),
    funktion(appJs, "function boersenLage("),
    funktion(appJs, "function boersenstatusZeile("),
    funktion(appJs, "function wirdVorgemerkt("),
    funktion(appJs, "function warteauftragHinweisKurz("),
    `let schliessInfo = { schliessbar: true, boerse: ${JSON.stringify(boerse)} };
     let letztesDetail = { positionen: ${JSON.stringify(positionen)} };`,
    funktion(botHtml, "function schliessbarAktiv("),
    funktion(botHtml, "function spaltenzahl("),
    funktion(botHtml, "function boerseGeschlossen("),
    funktion(botHtml, "function zeichneBoersenstatus("),
    funktion(botHtml, "function positionsZeile("),
    funktion(botHtml, "function zeichnePositionen("),
    "this.zeichneBoersenstatus = zeichneBoersenstatus; this.zeichnePositionen = zeichnePositionen;",
  ].join("\n\n"), ctx);
  ctx.zeichneBoersenstatus();
  ctx.zeichnePositionen();
  return elemente;
}

const POSITIONEN = [
  { id: 1, symbol: "AAPL", entry_preis: 200, stop_preis: 184,
    aktueller_preis: 210, veraenderung_pct: 5, warteauftrag_offen: false },
  { id: 2, symbol: "MSFT", entry_preis: 400, stop_preis: 368,
    aktueller_preis: 390, veraenderung_pct: -2.5, warteauftrag_offen: false },
];

const botZu = botSeiteBauen(FALL.feiertag, POSITIONEN);
check("Die Bot-Seite zeigt die Statuszeile wirklich an",
      nurText(botZu["boersenstatus"].innerHTML).includes("NYSE geschlossen"),
      nurText(botZu["boersenstatus"].innerHTML));
check("Mit dem Feiertag als Grund, nicht bloss \"geschlossen\"",
      nurText(botZu["boersenstatus"].innerHTML).includes("(Feiertag)"));
check("Der Einzelknopf heisst \"Vormerken\"",
      botZu["positionen"].innerHTML.includes(">Vormerken</button>")
      && !botZu["positionen"].innerHTML.includes(">Schließen</button>"));
check("... und sagt im Langtext, worauf vorgemerkt wird",
      botZu["positionen"].innerHTML.includes('aria-label="Zur Börsenöffnung vormerken"'));
check("Der bot-weite Notfallknopf ebenfalls - das war die Luecke",
      botZu["alle-schliessen"].textContent.includes("vormerken"),
      botZu["alle-schliessen"].textContent);
check("... mit der Anzahl, die wirklich betroffen ist",
      botZu["alle-schliessen"].textContent.includes("alle 2 Positionen"),
      botZu["alle-schliessen"].textContent);
check("Der Hinweis daneben erklaert die Ausfuehrung ohne Rueckfrage",
      botZu["notfall-hinweis"].textContent.includes("ohne erneute Rückfrage"),
      botZu["notfall-hinweis"].textContent.slice(0, 80));

const botOffen = botSeiteBauen(FALL.offen, POSITIONEN);
check("Bei OFFENER Boerse heisst der Einzelknopf wieder \"Schließen\"",
      botOffen["positionen"].innerHTML.includes(">Schließen</button>")
      && !botOffen["positionen"].innerHTML.includes(">Vormerken</button>"));
check("... und der Notfallknopf auch",
      botOffen["alle-schliessen"].textContent
        === "⚠ Notfall: alle 2 Positionen schließen",
      botOffen["alle-schliessen"].textContent);
check("Die Statuszeile sagt dort \"geöffnet\" mit Handelsschluss",
      nurText(botOffen["boersenstatus"].innerHTML).includes("NYSE geöffnet")
      && nurText(botOffen["boersenstatus"].innerHTML).includes("schließt"));

/* Krypto: hier aendert sich NICHTS - weder Zeile noch Knopftext. */
const botKrypto = botSeiteBauen(FALL.krypto, POSITIONEN);
check("KRYPTO-Bot: keine Statuszeile",
      botKrypto["boersenstatus"].innerHTML === "");
check("KRYPTO-Bot: Knopf heisst \"Schließen\", auch am Wochenende",
      botKrypto["positionen"].innerHTML.includes(">Schließen</button>"));
check("KRYPTO-Bot: Notfallknopf unveraendert",
      botKrypto["alle-schliessen"].textContent
        === "⚠ Notfall: alle 2 Positionen schließen",
      botKrypto["alle-schliessen"].textContent);

/* Unbekannter Kalender: die Zeile sagt es, und der Knopf behauptet nichts
   Falsches - vorgemerkt wird dann naemlich auch nicht (PR #71, fail closed). */
const botUnbekannt = botSeiteBauen(FALL.unbekannt, POSITIONEN);
check("UNBEKANNT: die Zeile benennt es",
      nurText(botUnbekannt["boersenstatus"].innerHTML).includes("unbekannt"));
check("UNBEKANNT: der Knopf verspricht kein Vormerken",
      botUnbekannt["positionen"].innerHTML.includes(">Schließen</button>"),
      "sonst verspraeche er etwas, das der Server ablehnt");

/* Ohne jede Boersenangabe muss die Seite trotzdem stehen. */
let botGeworfen = null;
let botOhne = null;
try { botOhne = botSeiteBauen(null, POSITIONEN); } catch (e) { botGeworfen = e; }
check("Ohne Boersenlage zeichnet die Bot-Seite trotzdem - der Weg bleibt offen",
      botGeworfen === null
      && botOhne["positionen"].innerHTML.includes("schliessen-knopf")
      && botOhne["boersenstatus"].innerHTML === "",
      botGeworfen ? String(botGeworfen).slice(0, 90) : "");

console.log(`\n${bestanden}/${bestanden + fehler.length} Pruefungen bestanden.`);
if (fehler.length) {
  fehler.forEach((f) => console.log(`  - ${f}`));
  process.exit(1);
}
