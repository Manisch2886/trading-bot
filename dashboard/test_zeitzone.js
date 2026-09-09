/* Verhaltenstest der Zeitanzeige unter verschiedenen Browser-Zeitzonen
   ===================================================================
   Prueft nicht, wie der Code geschrieben ist, sondern was er ANZEIGT:
   static/app.js wird wirklich ausgefuehrt, und zwar in mehreren
   Kindprozessen mit je einer anderen TZ - das ist das naechstliegende
   Modell fuer "derselbe Nutzer, anderes Geraet, andere Zeitzone".

   Die Sollwerte sind fest eingetragen, NICHT aus derselben Date-Logik
   berechnet, die geprueft wird. Sonst wuerde der Test nur bestaetigen,
   dass die Implementierung mit sich selbst uebereinstimmt.

   Zwei Zeitpunkte, mit Absicht: einer im Sommer, einer im Winter. Damit
   faellt auf, wenn jemand den Versatz als feste Zahl (+2 h) einbaut
   statt ihn vom Geraet bestimmen zu lassen.

   Zum Schluss eine Gegenprobe: dieselben Pruefungen gegen die FRUEHERE
   Fassung von app.js (per git geladen). Sie muss durchfallen - sonst
   misst der Test nicht, was er zu messen behauptet.

   Aufruf:  node dashboard/test_zeitzone.js
   Wird von test_dashboard.py mitgestartet, sofern node vorhanden ist.
*/

const { execFileSync } = require("child_process");
const fs = require("fs");
const os = require("os");
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

/* --- app.js in einem eigenen Kontext ausfuehren --------------------------- */

function ladeAppJs(quelle) {
  const kontext = {
    document: { getElementById: () => null, addEventListener: () => {},
                visibilityState: "visible" },
    window: {}, console, setInterval: () => 0, clearInterval: () => {},
    fetch: async () => { throw new Error("kein Netz im Test"); },
    Date, Set, Map, Math, JSON, isNaN, Intl, String, Number, RegExp,
  };
  kontext.globalThis = kontext;
  vm.createContext(kontext);
  vm.runInContext(quelle, kontext, { filename: "app.js" });
  return kontext;
}

/* --- Die Faelle ----------------------------------------------------------
   SOMMER/WINTER: derselbe Augenblick, vom Server mit Offset geschickt.
   Erwartet ist die Wanduhrzeit der jeweiligen Zone - fest eingetragen. */

const SOMMER = "2026-09-08T19:17:00+00:00";   // CEST: UTC+2
const WINTER = "2026-01-15T19:17:00+00:00";   // CET:  UTC+1

// DERSELBE Augenblick in der frueheren Uebertragungsform: was
// datetime.utcnow().isoformat() lieferte - dieselbe Zahl, nur ohne
// Offset. Genau hier entstand der gemeldete Versatz.
const SOMMER_ALTE_FORM = "2026-09-08T19:17:00";

const ZONEN = {
  "Europe/Berlin":    { sommer: "08.09., 21:17", winter: "15.01., 20:17" },
  "America/New_York": { sommer: "08.09., 15:17", winter: "15.01., 14:17" },
  "Asia/Tokyo":       { sommer: "09.09., 04:17", winter: "16.01., 04:17" },
  "UTC":              { sommer: "08.09., 19:17", winter: "15.01., 19:17" },
};

// Zeitpunkte OHNE Zeitzonenangabe: Kerzen-Zeitstempel aus den
// Bot-Datenbanken. Sie sind keine Wanduhrzeit des Nutzers und duerfen
// deshalb in KEINER Zone verschoben werden.
const OHNE_ZONE = [
  ["reine Datumsform (Tages-Kerze)", "2026-01-03", "03.01., 00:00"],
  ["str(pandas.Timestamp)", "2026-01-03 12:00:00", "03.01., 12:00"],
];

/* Laeuft im Kindprozess: eine Zone, Ergebnisse als JSON. */
function kindLauf() {
  const quelle = fs.readFileSync(process.env.APP_JS_PFAD, "utf8");
  const k = ladeAppJs(quelle);
  const drei_stunden_her = new Date(Date.now() - 3 * 3600000).toISOString();
  console.log("---JSON---" + JSON.stringify({
    zone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    sommer: k.zeit(SOMMER),
    sommer_alte_form: k.zeit(SOMMER_ALTE_FORM),
    winter: k.zeit(WINTER),
    ohne_zone: OHNE_ZONE.map(([, wert]) => k.zeit(wert)),
    alter: k.alterInStunden(drei_stunden_her),
    leer: k.zeit(null),
    unlesbar: k.zeit("kein Zeitstempel"),
  }));
}

function laufInZone(zone, appJsPfad) {
  const ausgabe = execFileSync(process.execPath, [__filename, "--kind"], {
    env: { ...process.env, TZ: zone, APP_JS_PFAD: appJsPfad },
    encoding: "utf8",
  });
  return JSON.parse(ausgabe.split("---JSON---")[1]);
}

/* --- 1) Anzeige in vier Zeitzonen ---------------------------------------- */

function testeZonen(appJsPfad) {
  console.log("\n1) Serverzeit mit Offset wird in die Geraete-Zeitzone umgerechnet");
  const ergebnisse = {};
  for (const [zone, soll] of Object.entries(ZONEN)) {
    const ist = laufInZone(zone, appJsPfad);
    ergebnisse[zone] = ist;
    check(`${zone}: Sommerzeitpunkt -> ${soll.sommer}`,
          ist.sommer === soll.sommer, `angezeigt ${ist.sommer}`);
    check(`${zone}: Winterzeitpunkt -> ${soll.winter}`,
          ist.winter === soll.winter, `angezeigt ${ist.winter}`);
  }
  return ergebnisse;
}

/* --- 2) Der gemeldete Fall ------------------------------------------------ */

function testeGemeldetenFall(ergebnisse) {
  console.log("\n2) Der gemeldete Fall: Server 19:17 UTC, Uhr in Berlin 21:17");
  check("Berlin zeigt 21:17, nicht mehr 19:17",
        ergebnisse["Europe/Berlin"].sommer === "08.09., 21:17",
        `angezeigt ${ergebnisse["Europe/Berlin"].sommer}`);
  check("Der Versatz ist keine feste Zahl: im Winter zeigt Berlin 20:17",
        ergebnisse["Europe/Berlin"].winter === "15.01., 20:17",
        `angezeigt ${ergebnisse["Europe/Berlin"].winter}`);
  check("In UTC bleibt es 19:17 - es wird nichts blind addiert",
        ergebnisse["UTC"].sommer === "08.09., 19:17",
        `angezeigt ${ergebnisse["UTC"].sommer}`);

  // Der Kern des Fehlers steckte in der UEBERTRAGUNGSFORM, nicht in der
  // Anzeige: derselbe Augenblick, einmal mit und einmal ohne Offset.
  // Ohne Offset zeigt Berlin weiterhin 19:17 - das ist der gemeldete
  // Versatz, hier reproduziert. Deshalb liefert datenquelle.py den
  // Zeitstempel jetzt mit Offset (siehe _jetzt_iso()).
  const b = ergebnisse["Europe/Berlin"];
  check("die alte Uebertragungsform (ohne Offset) zeigt weiterhin 19:17",
        b.sommer_alte_form === "08.09., 19:17",
        `angezeigt ${b.sommer_alte_form}`);
  check("genau zwei Stunden Unterschied zwischen alter und neuer Form",
        b.sommer === "08.09., 21:17" && b.sommer_alte_form === "08.09., 19:17",
        `${b.sommer_alte_form}  ->  ${b.sommer}`);
}

/* --- 3) Naive Zeitstempel bleiben stehen --------------------------------- */

function testeOhneZone(ergebnisse) {
  console.log("\n3) Kerzen-Zeitstempel ohne Zeitzone werden NICHT verschoben");
  OHNE_ZONE.forEach(([name, wert, soll], i) => {
    const alle = Object.entries(ergebnisse).map(([z, e]) => [z, e.ohne_zone[i]]);
    const gleich = alle.every(([, a]) => a === soll);
    check(`${name} ist in allen vier Zonen ${soll}`, gleich,
          alle.map(([z, a]) => `${z}=${a}`).join("  "));
  });
}

/* --- 4) Alter und Randfaelle --------------------------------------------- */

function testeAlterUndRaender(ergebnisse) {
  console.log("\n4) Altersberechnung und Randfaelle");
  for (const [zone, e] of Object.entries(ergebnisse)) {
    // alterInStunden speist die "veraltet"-Einfaerbung des letzten Laufs.
    // Sie darf sich durch die Zeitzone nicht verschieben, sonst waere ein
    // frischer Lauf in Tokio ploetzlich neun Stunden alt.
    check(`${zone}: drei Stunden alt bleiben drei Stunden`,
          Math.abs(e.alter - 3) < 0.01, `gemessen ${e.alter.toFixed(3)} h`);
  }
  const e = ergebnisse["Europe/Berlin"];
  check("Ein leerer Wert bleibt der Gedankenstrich", e.leer === "–",
        JSON.stringify(e.leer));
  check("Ein unlesbarer Wert wird unveraendert durchgereicht",
        e.unlesbar === "kein Zeitstempel", JSON.stringify(e.unlesbar));
}

/* --- 5) Gegenprobe: die alte Fassung muss durchfallen --------------------- */

/* Die Fassung VOR der Zeitzonen-Korrektur, festgenagelt auf ihren Commit.

   Hier stand frueher `origin/main` - und das war ein Ziel, das sich bewegt.
   Sobald die Korrektur (Commit 68d0c86) in main gemergt war, holte die
   Gegenprobe die KORRIGIERTE Fassung und verlangte von ihr, falsch zu
   liegen. Sie schlug damit fehl, ohne dass irgendetwas kaputt war. Ein
   Commit-Hash ist eine historische Tatsache und veraendert sich nicht. */
const FASSUNG_VOR_DER_KORREKTUR = "68d0c86^:dashboard/static/app.js";

function testeGegenprobe() {
  console.log("\n5) Gegenprobe - die fruehere Fassung von app.js muss scheitern");
  let alt;
  try {
    alt = execFileSync("git", ["-C", path.dirname(__dirname), "show",
                                FASSUNG_VOR_DER_KORREKTUR],
                        { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
  } catch (e) {
    console.log("  [uebersprungen] die fruehere Fassung ist per git nicht erreichbar");
    return;
  }

  const datei = path.join(os.tmpdir(), `app_js_alt_${process.pid}.js`);
  fs.writeFileSync(datei, alt);
  try {
    const berlin = laufInZone("Europe/Berlin", datei);
    const newyork = laufInZone("America/New_York", datei);

    // Die alte Fassung rechnet einen Wert MIT Offset ebenfalls richtig um -
    // dieser Teil war nie kaputt und muss auch in der Gegenprobe stimmen.
    check("alte Fassung: Werte MIT Offset waren schon vorher richtig",
          berlin.sommer === "08.09., 21:17", `angezeigt ${berlin.sommer}`);

    // Kaputt war die reine Datumsform: als UTC gelesen und damit verschoben.
    check("alte Fassung: Tages-Kerze wird verschoben (in Berlin 01:00)",
          berlin.ohne_zone[0] === "03.01., 01:00",
          `angezeigt ${berlin.ohne_zone[0]}`);
    check("alte Fassung: Tages-Kerze landet in New York sogar am Vortag",
          newyork.ohne_zone[0] === "02.01., 19:00",
          `angezeigt ${newyork.ohne_zone[0]}`);
  } finally {
    fs.unlinkSync(datei);
  }
}

function main() {
  if (process.argv.includes("--kind")) return kindLauf();

  console.log("Verhaltenstest: Zeitanzeige in verschiedenen Zeitzonen");
  const appJsPfad = path.join(__dirname, "static", "app.js");
  const ergebnisse = testeZonen(appJsPfad);
  testeGemeldetenFall(ergebnisse);
  testeOhneZone(ergebnisse);
  testeAlterUndRaender(ergebnisse);
  testeGegenprobe();

  console.log(`\n${bestanden}/${bestanden + fehler.length} Pruefungen bestanden.`);
  fehler.forEach(n => console.log(`FEHLGESCHLAGEN: ${n}`));
  process.exit(fehler.length ? 1 : 0);
}

main();
