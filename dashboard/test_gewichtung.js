/* Verhaltenstest der gewichteten Anzeige (Node, ohne Browser)
   ===============================================================
   Prueft nicht, wie der Code GESCHRIEBEN ist, sondern was er ERZEUGT: die
   beiden Funktionen aus static/bot.html werden wirklich ausgefuehrt und ihr
   HTML geprueft.

   Warum ueberhaupt: eine Textsuche in bot.html bleibt gruen, wenn ein
   if-Zweig auf `false` steht - der Text, nach dem sie sucht, liegt dann
   unerreichbar im Rumpf. Genau das ist in der Gegenprobe zu dieser Aenderung
   passiert (Mutation "ausgeschlossene Bots werden nicht genannt" blieb
   unentdeckt). Erst das Ausfuehren zeigt, ob der Hinweis tatsaechlich in der
   Ausgabe landet.

   Gemeinsam mit dem Dialog wird die ERGEBNISANZEIGE geprueft. Beide bauen ihre
   Zeilen getrennt auf, und eine Anzeige, die nur an einer der beiden Stellen
   beschriftet ist, war in diesem Projekt schon zweimal der Fehler.

   Aufruf:  node dashboard/test_gewichtung.js
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

/* Eine Funktion aus einer Quelldatei herausschneiden. Beide Dateien schreiben
   jede Funktion linksbuendig, die schliessende Klammer steht also in Spalte 1 -
   mehr Zerlegung braucht es hier nicht. */
function funktion(quelle, kopf) {
  const start = quelle.indexOf(kopf);
  if (start < 0) throw new Error(`nicht gefunden: ${kopf}`);
  const ende = quelle.indexOf("\n}", start);
  if (ende < 0) throw new Error(`kein Ende gefunden: ${kopf}`);
  return quelle.slice(start, ende + 2);
}

const statisch = path.join(__dirname, "static");
const botHtml = fs.readFileSync(path.join(statisch, "bot.html"), "utf8");
const indexHtml = fs.readFileSync(path.join(statisch, "index.html"), "utf8");
const appJs = fs.readFileSync(path.join(statisch, "app.js"), "utf8");

/* Die drei Bausteine stehen in app.js, weil beide Seiten sie brauchen. */
const erlaeuterung = appJs.match(/const GEWICHTUNG_ERLAEUTERUNG =[\s\S]*?;\n/);
if (!erlaeuterung) throw new Error("GEWICHTUNG_ERLAEUTERUNG nicht gefunden");
const anzahlErlaeuterung =
  appJs.match(/const POSITIONSANZAHL_ERLAEUTERUNG =[\s\S]*?;\n/);
if (!anzahlErlaeuterung) {
  throw new Error("POSITIONSANZAHL_ERLAEUTERUNG nicht gefunden");
}

/* Minimaler DOM-Ersatz: notfallErgebnisAnzeigen() schreibt in #erfolg. */
const geschrieben = {};
const ctx = {
  document: {
    getElementById: (id) => ({
      set innerHTML(wert) { geschrieben[id] = wert; },
      get innerHTML() { return geschrieben[id] || ""; },
    }),
  },
  console,
};

vm.runInNewContext([
  funktion(appJs, "function zahl("),
  funktion(appJs, "function prozent("),
  erlaeuterung[0],
  funktion(appJs, "function positionsgroesse("),
  anzahlErlaeuterung[0],
  funktion(appJs, "function positionsanzahlZeilen("),
  funktion(appJs, "function gewichtungsZeilen("),
  funktion(botHtml, "function notfallErgebnisAnzeigen("),
  funktion(indexHtml, "function crashListe("),
  funktion(indexHtml, "function crashErgebnisAnzeigen("),
  "this.gewichtungsZeilen = gewichtungsZeilen;",
  "this.positionsanzahlZeilen = positionsanzahlZeilen;",
  "this.notfallErgebnisAnzeigen = notfallErgebnisAnzeigen;",
  "this.crashListe = crashListe;",
  "this.crashErgebnisAnzeigen = crashErgebnisAnzeigen;",
].join("\n\n"), ctx);

/* --- Fall 1: zwei Bots mit verschiedener Groesse, einer ohne ------------- */
const mitGewicht = {
  wert_pct: -2.59, ungewichtet_schnitt_pct: 0.5, anzahl: 4,
  grundlage: "angenommene Positionsgroesse je Bot (ALLOCATION_PCT ...)",
  hinweis: "... Annahme ...",
  gewichte: [
    { bot: "t3_supertrend", anzeigename: "T3/ADX/SuperTrend", allokation_pct: 10.0,
      quelle: "equity_simulation.py", anzahl: 2 },
    { bot: "turtle_soup_stocks", anzeigename: "Turtle Soup (Aktien)",
      allokation_pct: 2.0, quelle: "live_params.py", anzahl: 1 },
  ],
  nicht_gewichtbar: [
    { bot: "neuer_bot", anzeigename: "Neuer Bot", anzahl: 1,
      pnl_schnitt_pct: 1.0, grund: "weder live_params.py noch equity_simulation.py dokumentieren ALLOCATION_PCT als Zahl" },
  ],
};

const dialog = ctx.gewichtungsZeilen(mitGewicht).join("");
check("Der Dialog erzeugt eine Zeile 'Ø gewichtet'", dialog.includes("Ø gewichtet"));
check("Mit dem gewichteten Wert", dialog.includes("-2.59%"), dialog.slice(0, 0));
check("Mit beiden Positionsgroessen (10 % / 2 %)",
      dialog.includes("10 % / 2 %"), (dialog.match(/Positionsgröße[^<]*/) || [""])[0]);
check("Und mit dem ungewichteten Vergleichswert derselben Positionen",
      dialog.includes("ungewichtet") && dialog.includes("+0.50%"));
check("Die Erlaeuterung landet wirklich in der Ausgabe",
      dialog.includes("angenommenen") && dialog.includes("keine Portfolio-Rendite"));
check("Der nicht gewichtbare Bot wird in der Ausgabe BENANNT",
      dialog.includes("Neuer Bot") && dialog.includes("ausgenommen"),
      (dialog.match(/Ohne dokumentierte[^<]*/) || [""])[0].slice(0, 80));
check("Mit seinem Grund und seiner eigenen Zahl",
      dialog.includes("live_params.py") && dialog.includes("+1.00%"));

/* Die Anzahl je Bot: die gewichtete Zahl ist rechnerisch richtig, sagt aber
   nicht, WORAUS sie besteht. Geprueft wird die erzeugte Ausgabe, nicht der
   Quelltext - eine Textsuche waere gruen geblieben, haette der if-Zweig auf
   `false` gestanden. */
check("Der Dialog weist die Anzahl der Positionen JE BOT aus",
      dialog.includes("Eingegangene Positionen je Bot")
      && dialog.includes("T3/ADX/SuperTrend: 2")
      && dialog.includes("Turtle Soup (Aktien): 1"),
      (dialog.match(/Eingegangene Positionen je Bot[^<]*/) || [""])[0].slice(0, 90));
check("Und zwar als SICHTBARE Zeile, nicht als title-Tooltip (am iPhone gibt "
      + "es kein Hover)",
      dialog.includes('class="hinweis-gewichtung">Eingegangene Positionen je Bot')
      && !dialog.includes('title="Eingegangene'));
check("Mit der Erlaeuterung, warum die Anzahl ueberhaupt dasteht",
      dialog.includes("ohne Obergrenze für gleichzeitige Positionen"));

/* --- Fall 1b: der Fall, um den es hier ueberhaupt geht ------------------
   `elliott_wave` hat als einziger Bot kein MAX_CONCURRENT_POSITIONS. Traegt
   er sieben von acht Positionen, ist "Ø gewichtet" praktisch seine Zahl -
   und ohne die Anzahl je Bot sieht man das der Anzeige nicht an. */
const dominiert = {
  wert_pct: -8.05, ungewichtet_schnitt_pct: -8.0, anzahl: 8,
  grundlage: "...", hinweis: "...",
  gewichte: [
    { bot: "elliott_wave", anzeigename: "Elliott Wave (Krypto)",
      allokation_pct: 10.0, quelle: "equity_simulation.py", anzahl: 7 },
    { bot: "turtle_soup_stocks", anzeigename: "Turtle Soup (Aktien)",
      allokation_pct: 2.0, quelle: "live_params.py", anzahl: 1 },
  ],
  nicht_gewichtbar: [],
};
const ungleich = ctx.gewichtungsZeilen(dominiert).join("");
check("Traegt EIN Bot sieben von acht Positionen, ist das ablesbar",
      ungleich.includes("Elliott Wave (Krypto): 7")
      && ungleich.includes("Turtle Soup (Aktien): 1"),
      (ungleich.match(/Eingegangene Positionen je Bot[^<]*/) || [""])[0].slice(0, 90));
check("Die Gewichtung selbst bleibt unveraendert daneben stehen",
      ungleich.includes("-8.05%") && ungleich.includes("10 % / 2 %"));

/* --- Fall 2: gar keine gewichtbare Position ----------------------------- */
const ohne = {
  wert_pct: null, ungewichtet_schnitt_pct: null, anzahl: 0,
  grundlage: "...", hinweis: "...", gewichte: [],
  nicht_gewichtbar: [{ bot: "b", anzeigename: "Bot B", anzahl: 2,
                       pnl_schnitt_pct: -3.0, grund: "kein ALLOCATION_PCT" }],
};
const nurAusschluss = ctx.gewichtungsZeilen(ohne).join("");
check("Ohne gewichtbare Position steht KEINE gewichtete Zahl da",
      !nurAusschluss.includes("Ø gewichtet"), nurAusschluss.slice(0, 80));
check("Der Ausschluss steht trotzdem da - er verschwindet nicht mit der Zahl",
      nurAusschluss.includes("Bot B") && nurAusschluss.includes("ausgenommen"));
check("Und keine erfundene Null", !nurAusschluss.includes("0.00%"));

/* --- Fall 3: ein altes Backend ohne das Feld --------------------------- */
check("Fehlt das Feld ganz (aelteres Backend), bricht nichts",
      ctx.gewichtungsZeilen(undefined).length === 0
      && ctx.gewichtungsZeilen(null).length === 0);

/* --- Fall 3b: die Anzahl-Anzeige darf den Notfallweg NIE blockieren -----
   Dieselbe Regel wie bei der Positionsgroesse: fehlt eine Angabe, wird
   trotzdem geschlossen. Eine Anzeige, die im Crash eine Ausnahme wirft,
   waere schlimmer als eine fehlende Anzeige. */
check("Ohne Feld, ohne Liste und mit leerer Liste entsteht keine Anzahl-Zeile",
      ctx.positionsanzahlZeilen(undefined).length === 0
      && ctx.positionsanzahlZeilen(null).length === 0
      && ctx.positionsanzahlZeilen({}).length === 0
      && ctx.positionsanzahlZeilen({ gewichte: [] }).length === 0
      && ctx.positionsanzahlZeilen({ gewichte: "kaputt" }).length === 0);
check("Fehlt die Anzahl EINES Bots, steht dort ein Strich statt einer Luecke",
      ctx.positionsanzahlZeilen({ gewichte: [{ anzeigename: "Bot A" }] })
        .join("").includes("Bot A: –"));
check("Fehlt auch der Name, bleibt die Zeile lesbar",
      ctx.positionsanzahlZeilen({ gewichte: [{ anzahl: 3 }] })
        .join("").includes("unbekannt: 3"));

/* Der eigentliche Punkt: das uebrige Ergebnis steht trotzdem da. Geprueft
   wird ueber gewichtungsZeilen(), also so, wie der Dialog es aufruft. */
const ohneAnzahl = {
  wert_pct: -2.59, ungewichtet_schnitt_pct: 0.5, anzahl: 4,
  grundlage: "...", hinweis: "...",
  gewichte: [{ bot: "t3_supertrend", anzeigename: "T3/ADX/SuperTrend",
                allokation_pct: 10.0, quelle: "equity_simulation.py" }],
  nicht_gewichtbar: [],
};
let trotzdem = "";
let geworfen = null;
try {
  trotzdem = ctx.gewichtungsZeilen(ohneAnzahl).join("");
} catch (e) {
  geworfen = e;
}
check("Eine fehlende Anzahl wirft nicht - gewichtete Zahl und Erlaeuterung "
      + "stehen unveraendert da",
      geworfen === null && trotzdem.includes("-2.59%")
      && trotzdem.includes("keine Portfolio-Rendite")
      && trotzdem.includes("T3/ADX/SuperTrend: –"),
      geworfen ? String(geworfen).slice(0, 80) : "");

/* --- Fall 4: die Ergebnisanzeige, dieselben Zusicherungen -------------- */
ctx.notfallErgebnisAnzeigen({
  anzahl_geschlossen: 3, angefragt: 4, anzahl_fehlgeschlagen: 0,
  anzahl_uebersprungen: 0, nicht_bestaetigt: [], geschlossen: [],
  fehlgeschlagen: [], uebersprungen: [], pnl_schnitt_pct: 0.5,
  pnl_gewichtet: mitGewicht,
});
const erfolg = geschrieben["erfolg"] || "";
check("Die Ergebnisanzeige nennt den ungewichteten Durchschnitt",
      erfolg.includes("Ø je Position") && erfolg.includes("+0.50%"));
check("Die Ergebnisanzeige nennt AUCH den gewichteten Wert",
      erfolg.includes("gewichtet") && erfolg.includes("-2.59%"),
      (erfolg.match(/Ø je Position[^<]*/) || [""])[0].slice(0, 80));
check("Und dort steht dieselbe Erlaeuterung",
      erfolg.includes("angenommenen") && erfolg.includes("keine Portfolio-Rendite"));
check("Und auch dort wird der ausgeschlossene Bot benannt",
      erfolg.includes("Neuer Bot") && erfolg.includes("ausgenommen"));
/* notfallErgebnisAnzeigen() baut sein HTML SELBST auf und ruft
   gewichtungsZeilen() nicht auf - die Anzahl muss dort eigens geholt werden.
   Genau diese Stelle war in PR #62/#66/#67 dreimal die vergessene. */
check("Die Ergebnisanzeige weist die Anzahl je Bot ebenfalls aus",
      erfolg.includes("Eingegangene Positionen je Bot")
      && erfolg.includes("T3/ADX/SuperTrend: 2")
      && erfolg.includes("Turtle Soup (Aktien): 1"),
      (erfolg.match(/Eingegangene Positionen je Bot[^<]*/) || [""])[0].slice(0, 90));

geschrieben["erfolg"] = "";
ctx.notfallErgebnisAnzeigen({
  anzahl_geschlossen: 1, angefragt: 1, anzahl_fehlgeschlagen: 0,
  anzahl_uebersprungen: 0, nicht_bestaetigt: [], geschlossen: [],
  fehlgeschlagen: [], uebersprungen: [], pnl_schnitt_pct: 9.7,
  pnl_gewichtet: ohne,
});
const erfolg2 = geschrieben["erfolg"] || "";
check("Ohne gewichtbare Position zeigt das Ergebnis nur den Ausschluss",
      !erfolg2.includes("gewichtet -") && erfolg2.includes("ausgenommen"),
      erfolg2.slice(-120));

/* --- Fall 5: der CRASH-Dialog (index.html) ------------------------------
   Dort ist die Gewichtung der eigentliche Punkt: 10 %, 5 % und 2 % treffen
   aufeinander. Geprueft wird wieder die ERZEUGTE Ausgabe, in Uebersicht und
   Ergebnis. */
geschrieben["crash-liste"] = "";
ctx.crashListe({
  anzahl: 4, anzahl_gesamt: 4, anzahl_bots: 2,
  bots: [
    { bot: "t3_supertrend", anzeigename: "T3/ADX/SuperTrend", anlageklasse: "krypto",
      anzahl: 2, anzahl_gesamt: 2, lesefehler: null, pnl_schnitt_pct: -5.0,
      pnl_bestes_pct: -4.0, pnl_schlechtestes_pct: -6.0,
      positionen: [
        { symbol: "BTCUSDT", entry_preis: 100, aktueller_preis: 96,
          pnl_pct: -4.0, schliessbar_jetzt: true, grund: null },
        { symbol: "ETHUSDT", entry_preis: 200, aktueller_preis: 188,
          pnl_pct: -6.0, schliessbar_jetzt: true, grund: null }],
    },
    { bot: "turtle_soup_stocks", anzeigename: "Turtle Soup (Aktien)",
      anlageklasse: "aktien", anzahl: 1, anzahl_gesamt: 1, lesefehler: null,
      pnl_schnitt_pct: 10.0, pnl_bestes_pct: 10.0, pnl_schlechtestes_pct: 10.0,
      positionen: [
        { symbol: "AAPL", entry_preis: 150, aktueller_preis: 165,
          pnl_pct: 10.0, schliessbar_jetzt: true, grund: null }],
    },
  ],
  pnl_gewichtet: mitGewicht,
});
const crash = geschrieben["crash-liste"] || "";
check("Die Crash-Uebersicht nennt den Durchschnitt JE BOT weiterhin",
      (crash.match(/Ø je Position/g) || []).length === 2,
      String((crash.match(/Ø je Position/g) || []).length));
check("UND darunter die gewichtete Zahl ueber alle Bots",
      crash.includes("Ø gewichtet") && crash.includes("-2.59%")
      && crash.includes("Über alle Bots"));
check("Mit Erlaeuterung und mit dem ausgeschlossenen Bot",
      crash.includes("angenommenen") && crash.includes("keine Portfolio-Rendite")
      && crash.includes("Neuer Bot") && crash.includes("ausgenommen"));
check("Die Crash-Uebersicht weist die Anzahl je Bot aus",
      crash.includes("Eingegangene Positionen je Bot")
      && crash.includes("T3/ADX/SuperTrend: 2")
      && crash.includes("Turtle Soup (Aktien): 1"),
      (crash.match(/Eingegangene Positionen je Bot[^<]*/) || [""])[0].slice(0, 90));
check("Die Querzahl steht NACH den Bot-Bloecken, nicht in einem davon",
      crash.indexOf("Über alle Bots") > crash.indexOf("Turtle Soup (Aktien)"),
      `${crash.indexOf("Über alle Bots")} > ${crash.indexOf("Turtle Soup (Aktien)")}`);

geschrieben["erfolg"] = "";
ctx.crashErgebnisAnzeigen({
  anzahl_geschlossen: 4, angefragt: 4, angefragte_bots: 2,
  anzahl_fehlgeschlagen: 0, anzahl_uebersprungen: 0, bots_fehlgeschlagen: [],
  bots: [{ anzeigename: "T3/ADX/SuperTrend", meldung: "2 von 2 geschlossen." },
         { anzeigename: "Turtle Soup (Aktien)", meldung: "1 von 1 geschlossen." }],
  pnl_gewichtet: mitGewicht,
});
const crashErfolg = geschrieben["erfolg"] || "";
check("Das Crash-ERGEBNIS nennt die gewichtete Zahl ebenfalls",
      crashErfolg.includes("Ø gewichtet") && crashErfolg.includes("-2.59%"),
      crashErfolg.slice(-140));
check("Auch dort mit Erlaeuterung und Ausschluss",
      crashErfolg.includes("angenommenen")
      && crashErfolg.includes("keine Portfolio-Rendite")
      && crashErfolg.includes("ausgenommen"));
check("Und das Crash-ERGEBNIS weist die Anzahl je Bot aus",
      crashErfolg.includes("Eingegangene Positionen je Bot")
      && crashErfolg.includes("T3/ADX/SuperTrend: 2")
      && crashErfolg.includes("Turtle Soup (Aktien): 1"),
      (crashErfolg.match(/Eingegangene Positionen je Bot[^<]*/) || [""])[0].slice(0, 90));

geschrieben["erfolg"] = "";
ctx.crashErgebnisAnzeigen({
  anzahl_geschlossen: 1, angefragt: 1, angefragte_bots: 1,
  anzahl_fehlgeschlagen: 0, anzahl_uebersprungen: 0, bots_fehlgeschlagen: [],
  bots: [{ anzeigename: "Bot", meldung: "1 von 1 geschlossen." }],
  pnl_gewichtet: ohne,
});
check("Ohne gewichtbare Position zeigt auch das Crash-Ergebnis nur den Ausschluss",
      !(geschrieben["erfolg"] || "").includes("Ø gewichtet")
      && (geschrieben["erfolg"] || "").includes("ausgenommen"));

console.log(`\n${bestanden}/${bestanden + fehler.length} Pruefungen bestanden.`);
if (fehler.length) {
  fehler.forEach((f) => console.log(`  - ${f}`));
  process.exit(1);
}
