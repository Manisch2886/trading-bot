/* Verhaltenstest der Portfolio-Anzeige (Node, ohne Browser)
   ===============================================================
   Prueft nicht, wie der Code GESCHRIEBEN ist, sondern was er ERZEUGT: die
   Anzeige-Funktionen aus static/app.js werden wirklich ausgefuehrt und ihre
   Ausgabe geprueft.

   Warum ueberhaupt: eine Textsuche ueber app.js oder portfolio.html bleibt
   gruen, wenn ein if-Zweig auf `false` steht - der gesuchte Text liegt dann
   unerreichbar im Rumpf. Genau diese Fehlerklasse ist in PR #62, #66, #67,
   #73 und #77 aufgetreten, fuenfmal.

   Der Kern hier ist die Quellenkennzeichnung. Sie wird JE FUNKTION geprueft:
   in der Marke selbst, in der Bot-Zeile, im Gruppenblock und in der
   Gesamtansicht. Eine Angabe, die nur an einer der vier Stellen steht, faellt
   damit auf.

   Aufruf:  node dashboard/test_portfolio_anzeige.js
   Wird von test_portfolio_sicht.py mitgestartet, sofern node vorhanden ist.
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

/* Eine Funktion oder Konstante aus der Quelldatei herausschneiden. app.js
   schreibt jede Funktion linksbuendig, die schliessende Klammer steht also in
   Spalte 1. */
function stueck(quelle, kopf, ende = "\n}") {
  const start = quelle.indexOf(kopf);
  if (start < 0) throw new Error(`nicht gefunden: ${kopf}`);
  const schluss = quelle.indexOf(ende, start);
  if (schluss < 0) throw new Error(`kein Ende fuer: ${kopf}`);
  return quelle.slice(start, schluss + ende.length);
}

const appJs = fs.readFileSync(path.join(__dirname, "static", "app.js"), "utf8");

const teile = [
  stueck(appJs, "function zahl("),
  stueck(appJs, "function prozent("),
  stueck(appJs, "const ZEITZONE_IM_TEXT", ";"),
  stueck(appJs, "function zeitpunkt("),
  stueck(appJs, "function zeit("),
  stueck(appJs, "const PORTFOLIO_QUELLEN", "\n};"),
  stueck(appJs, "function quellenMarke("),
  stueck(appJs, "function portfolioBotZeile("),
  stueck(appJs, "function portfolioGruppe("),
  stueck(appJs, "function portfolioStand("),
  stueck(appJs, "function portfolioSicht("),
];

const umgebung = {
  console,
  encodeURIComponent,
  Object,
  Math,
  Number,
  Date,
  JSON,
};
vm.createContext(umgebung);
vm.runInContext(teile.join("\n"), umgebung);

const {
  quellenMarke, portfolioBotZeile, portfolioGruppe, portfolioStand,
  portfolioSicht, PORTFOLIO_QUELLEN,
} = umgebung;

/* --------------------------------------------------------------------- */
function bot(felder) {
  return Object.assign({
    name: "t3_supertrend",
    anzeigename: "T3/ADX/SuperTrend (Krypto)",
    quelle: "backtest",
    quelle_text: "Backtest-Kurve, erst 3 von 10 Live-Trades",
    geschlossene_trades: 3,
    fehlt_bis_schwelle: 7,
    ist_live_bot: true,
    grundlage_in_ueberarbeitung: null,
    offene_positionen: 2,
    beitrag_pp: 1.25,
  }, felder || {});
}

function gruppe(felder) {
  return Object.assign({
    titel: "Alle Bots (teils Backtest)",
    moeglich: true,
    grund: null,
    anzahl_bots: 3,
    bots: ["a", "b", "c"],
    von: "2025-01-01",
    bis: "2026-06-27",
    tage: 543,
    rendite_pct: 18.29,
    max_drawdown_pct: -6.24,
    schlechtester_einzel_drawdown_pct: -9.1,
    je_bot: [{ name: "a", gewicht_pct: 33.3, rendite_pct: 4.0, max_drawdown_pct: -3.0, beitrag_pp: 1.33 }],
    nur_echte_daten: false,
    enthaelt_backtest: true,
  }, felder || {});
}

function stand(felder) {
  return Object.assign({
    vorhanden: true,
    alter_sekunden: 120,
    veraltet: false,
    max_alter_sekunden: 86400,
    laeuft_gerade: false,
    daten: {
      berechnet_am: "2026-09-12T09:00:00+00:00",
      dauer_sekunden: 2.9,
      schwelle: 10,
      startkapital: 10000.0,
      bots: [bot({ name: "a", anzeigename: "Bot A", quelle: "live", geschlossene_trades: 25 }),
             bot({ name: "b", anzeigename: "Bot B", quelle: "backtest", geschlossene_trades: 3 })],
      gruppen: {
        nur_echte_trades: gruppe({ titel: "Nur echte Trades", nur_echte_daten: true,
                                   enthaelt_backtest: false, anzahl_bots: 1,
                                   bots: ["a"], rendite_pct: 4.99,
                                   je_bot: [{ name: "a", beitrag_pp: 4.99 }] }),
        alle: gruppe({ je_bot: [{ name: "a", beitrag_pp: 1.33 }, { name: "b", beitrag_pp: 16.96 }] }),
      },
      offene_positionen: 7,
      offene_positionen_fehler: null,
      anzahl_live_quellen: 1,
      anzahl_backtest_quellen: 1,
      anzahl_fehlt: 0,
    },
  }, felder || {});
}

/* 1) Die Marke selbst ------------------------------------------------- */
console.log("\n1) quellenMarke - die Kennzeichnung an ihrer Quelle");
let html = quellenMarke(bot({ quelle: "live", geschlossene_trades: 25 }), 10);
check("live: nennt 'echte Trades'", /echte Trades/.test(html), html);
check("live: nennt die Trade-Zahl", html.includes("25"), html);
check("live: traegt die Klasse quelle-live", html.includes("quelle-live"), html);
check("live: sagt NICHT 'Backtest'", !/Backtest/.test(html), html);

html = quellenMarke(bot({ quelle: "backtest", geschlossene_trades: 3 }), 10);
check("Backtest: nennt 'Backtest'", /Backtest/.test(html), html);
check("Backtest: nennt den Abstand zur Schwelle (3 von 10)",
      html.includes("3") && html.includes("10"), html);
check("Backtest: traegt die Klasse quelle-backtest", html.includes("quelle-backtest"), html);

html = quellenMarke(bot({ quelle: "fehlt" }), 10);
check("fehlt: nennt 'keine Kurve'", /keine Kurve/.test(html), html);
check("fehlt: traegt die Klasse quelle-fehlt", html.includes("quelle-fehlt"), html);

html = quellenMarke(bot({ quelle: "voelliger_unsinn" }), 10);
check("unbekannte Quelle faellt auf 'keine Kurve' zurueck, statt leer zu bleiben",
      /keine Kurve/.test(html), html);

/* Die Marke darf NIE leer sein - das ist der eigentliche Punkt. */
["live", "backtest", "fehlt", "", null, undefined].forEach((q) => {
  const ausgabe = quellenMarke(bot({ quelle: q }), 10);
  check(`Marke ist auch bei quelle=${JSON.stringify(q)} nicht leer`,
        ausgabe.replace(/<[^>]*>/g, "").trim().length > 0, ausgabe);
});

/* 2) Die Bot-Zeile ---------------------------------------------------- */
console.log("\n2) portfolioBotZeile - jede Zeile traegt ihre Quelle");
html = portfolioBotZeile(bot({ quelle: "backtest" }), 10);
check("die Zeile enthaelt die Marke", html.includes("quelle-backtest"), html.slice(0, 120));
check("die Zeile verlinkt den Bot", html.includes('href="/bot?name=t3_supertrend"'));
check("die Zeile zeigt den Beitrag", html.includes("1.25"));
check("die Zeile zeigt die offenen Positionen", />2</.test(html));

html = portfolioBotZeile(bot({ beitrag_pp: null }), 10);
check("ohne Beitrag steht ein Gedankenstrich, keine 0",
      html.includes("–") && !/>0\.00%/.test(html), html.slice(0, 200));

html = portfolioBotZeile(bot({ offene_positionen: null }), 10);
check("ohne Positionszahl steht ein Gedankenstrich", html.includes("–"));

html = portfolioBotZeile(bot({ grundlage_in_ueberarbeitung: "Zigzag-Look-Ahead im Backtest" }), 10);
check("eine ueberarbeitete Grundlage wird in der Zeile genannt",
      /Grundlage wird überarbeitet/.test(html) && /Zigzag/.test(html), html.slice(0, 250));

html = portfolioBotZeile(bot({ grundlage_in_ueberarbeitung: null }), 10);
check("ohne diesen Vermerk erscheint keine Warnzeile",
      !/Grundlage wird überarbeitet/.test(html));

/* 3) Der Gruppenblock ------------------------------------------------- */
console.log("\n3) portfolioGruppe - keine Zahl ohne Herkunftssatz");
html = portfolioGruppe(gruppe(), 10);
check("der Titel erscheint", html.includes("Alle Bots (teils Backtest)"));
check("die Rendite erscheint", html.includes("18.29"));
check("der Drawdown erscheint", html.includes("-6.24"));
check("der Zeitraum erscheint", html.includes("2025-01-01") && html.includes("2026-06-27"));
check("die Tageszahl erscheint", html.includes("543"));
check("BACKTEST wird im Herkunftssatz genannt", /Backtest/.test(html), html.slice(0, 300));
check("der Satz sagt ausdruecklich, dass es keine erzielte Rendite ist",
      /keine erzielte Rendite/.test(html));
check("das Fenster wird als Schnittmenge erklaert", /Schnittmenge/.test(html));

html = portfolioGruppe(gruppe({ nur_echte_daten: true, enthaelt_backtest: false,
                                titel: "Nur echte Trades" }), 10);
check("bei echten Daten nennt der Satz die Schwelle", html.includes("10"), html.slice(0, 300));
check("bei echten Daten steht NICHT 'keine erzielte Rendite'",
      !/keine erzielte Rendite/.test(html));

html = portfolioGruppe(gruppe({ moeglich: false, grund: "keine Bots mit Kurve in dieser Gruppe" }), 10);
check("ohne Zahl steht die Begruendung", /keine Bots mit Kurve/.test(html), html);
check("ohne Zahl steht KEINE Rendite da", !/18\.29/.test(html));
check("ohne Zahl steht auch keine 0 %", !/0\.00%/.test(html), html);

html = portfolioGruppe(gruppe({ anzahl_bots: 1 }), 10);
check("bei einem einzigen Bot wird das benannt",
      /keine Diversifikation/.test(html), html.slice(0, 400));
html = portfolioGruppe(gruppe({ anzahl_bots: 3 }), 10);
check("bei mehreren Bots erscheint dieser Satz nicht",
      !/keine Diversifikation/.test(html));

/* 4) Der Stand -------------------------------------------------------- */
console.log("\n4) portfolioStand - eine Zahl ohne Zeitpunkt ist unehrlich");
html = portfolioStand(stand({ alter_sekunden: 120 }));
check("das Alter erscheint in Minuten", /vor 2 Minuten/.test(html), html);
check("die Rechenzeit erscheint", /2\.9 s/.test(html), html);
check("frisch: keine Veraltet-Marke", !/veraltet/.test(html));
/* Der Zeitpunkt muss LESBAR formatiert sein. Zuerst stand hier zeitpunkt(),
   das ein Date-Objekt liefert - im Template wurde daraus
   "Sat Sep 12 2026 09:00:00 GMT+0000". Der Test prueft deshalb das Format,
   nicht nur die Anwesenheit einer Zeitangabe. */
check("der Zeitpunkt steht im deutschen Format (TT.MM., HH:MM)",
      /\d{2}\.\d{2}\.,? \d{2}:\d{2}/.test(html), html);
check("der Zeitpunkt enthaelt keine rohe Date-Ausgabe",
      !/GMT|Coordinated Universal Time/.test(html), html);

html = portfolioStand(stand({ alter_sekunden: 7200 }));
check("aelter als eine Stunde: in Stunden", /vor 2 Stunden/.test(html), html);

html = portfolioStand(stand({ alter_sekunden: 20 }));
check("ganz frisch: 'gerade eben'", /gerade eben/.test(html), html);

html = portfolioStand(stand({ veraltet: true, alter_sekunden: 90000 }));
check("ueber der Altersgrenze: sichtbare Veraltet-Marke",
      /veraltet/.test(html), html);

html = portfolioStand({ vorhanden: false, hinweis: "Noch nicht berechnet." });
check("ohne Stand steht der Hinweis", /Noch nicht berechnet/.test(html), html);
check("ohne Stand steht kein Zeitpunkt", !/Berechnet/.test(html));

/* 5) Die Gesamtansicht ------------------------------------------------ */
console.log("\n5) portfolioSicht - beide Gruppen, jede Zeile, kein stiller Verlust");
html = portfolioSicht(stand());
check("beide Gruppentitel erscheinen",
      html.includes("Nur echte Trades") && html.includes("Alle Bots (teils Backtest)"));
check("beide Renditen erscheinen - zwei Zahlen, nicht eine",
      html.includes("4.99") && html.includes("18.29"));
check("die offenen Positionen erscheinen", /Offene Positionen[\s\S]*7/.test(html));
check("jede Bot-Zeile erscheint",
      html.includes("Bot A") && html.includes("Bot B"));
check("die Marke 'echte Trades' erscheint in der Tabelle", /quelle-live/.test(html));
check("die Marke 'Backtest' erscheint in der Tabelle", /quelle-backtest/.test(html));
check("der Beitrag wird aus der Gruppe 'alle' uebernommen",
      html.includes("16.96"), "Beitrag von Bot B");
check("die Einheit des Beitrags wird erklaert",
      /Prozentpunkten/.test(html));

/* Der stille Verlust: ein Bot ohne Kurve. */
const mitFehlend = stand();
mitFehlend.daten.bots.push(bot({ name: "c", anzeigename: "Bot C", quelle: "fehlt",
                                 beitrag_pp: null, offene_positionen: null }));
mitFehlend.daten.anzahl_fehlt = 1;
html = portfolioSicht(mitFehlend);
check("ein Bot ohne Kurve wird ausdruecklich als 'in KEINER Summe' gemeldet",
      /KEINER Summe/.test(html), html.slice(0, 600));
check("sein Name steht dabei", /Bot C/.test(html));
check("er erscheint auch in der Tabelle", /quelle-fehlt/.test(html));

const ohneFehlend = stand();
html = portfolioSicht(ohneFehlend);
check("ohne fehlende Bots erscheint dieser Hinweis nicht",
      !/KEINER Summe/.test(html));

html = portfolioSicht({ vorhanden: false, hinweis: "Noch nicht berechnet." });
check("ohne Stand zeigt die Gesamtansicht nur den Hinweis",
      /Noch nicht berechnet/.test(html) && !/Rendite/.test(html), html);

/* Ein Datensatz, in dem die Gruppe 'alle' nicht rechenbar ist, darf die
   Tabelle nicht mitnehmen. */
const ohneAlle = stand();
ohneAlle.daten.gruppen.alle = gruppe({ moeglich: false, grund: "kein gemeinsames Zeitfenster" });
html = portfolioSicht(ohneAlle);
check("ohne rechenbare Gruppe 'alle' erscheinen die Bot-Zeilen weiter",
      html.includes("Bot A") && html.includes("Bot B"), "Tabelle bleibt");
check("die Begruendung der Gruppe erscheint", /kein gemeinsames Zeitfenster/.test(html));

/* 6) Keine Zahl ohne Quelle - die Zusicherung als Ganzes -------------- */
console.log("\n6) Die Zusicherung: keine Rendite ohne Herkunftsangabe");
[stand(), mitFehlend, ohneAlle].forEach((s, i) => {
  const ausgabe = portfolioSicht(s);
  const renditen = (ausgabe.match(/kennzahl-name">Rendite im Fenster/g) || []).length;
  const herkunft = (ausgabe.match(/portfolio-herkunft/g) || []).length;
  check(`Datensatz ${i + 1}: jede gezeigte Rendite hat einen Herkunftssatz`,
        renditen <= herkunft, `${renditen} Renditen, ${herkunft} Herkunftssaetze`);
});

console.log("");
const gesamt = bestanden + fehler.length;
console.log(`${bestanden} von ${gesamt} Pruefungen bestanden, ${fehler.length} fehlgeschlagen.`);
fehler.forEach((n) => console.log(`  - ${n}`));
process.exit(fehler.length ? 1 : 0);
