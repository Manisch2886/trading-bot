/* Verhaltenstest der Aktualisierungs-Zustaende (Node, ohne Browser)
   ===============================================================
   Prueft nicht, wie der Code GESCHRIEBEN ist, sondern was er TUT:
   static/app.js wird mit einem winzigen DOM-Ersatz wirklich ausgefuehrt
   und durch alle Uebergaenge geschickt.

   Der Unterschied ist wesentlich. Eine Textsuche nach
   classList.remove("laedt", "veraltet") wuerde auch dann gruen bleiben,
   wenn die Zeile an der falschen Stelle stuende. Die entscheidende
   Zusicherung dieser Aenderung - "laedt" und "veraltet" gelten NIE
   gleichzeitig - laesst sich nur durch Ausfuehren belegen.

   app.js ist bewusst ein einfaches Skript ohne Seiteneffekte beim Laden
   (nur const-Deklarationen und Funktionen), deshalb genuegt hier ein
   vm-Kontext mit ein paar Attrappen - ohne jsdom oder sonstige Zusatz-
   Bibliothek.

   Aufruf:  node dashboard/test_zustandsmaschine.js
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

/* --- Minimaler DOM-Ersatz -------------------------------------------------
   Nur so viel, wie markiereAktualisierung() und die Ladeanzeige anfassen:
   eine Klassenliste, title, textContent und hidden. */
function neuesElement(id, grundklassen = "") {
  const klassen = new Set(grundklassen.split(" ").filter(Boolean));
  return {
    id,
    title: "",
    textContent: "",
    hidden: true,
    classList: {
      add: (...n) => n.forEach(k => klassen.add(k)),
      remove: (...n) => n.forEach(k => klassen.delete(k)),
      contains: k => klassen.has(k),
    },
    get className() { return [...klassen].join(" "); },
  };
}

function baueKontext(elemente) {
  const kontext = {
    document: {
      getElementById: id => elemente[id] || null,
      addEventListener: () => {},
      visibilityState: "visible",
    },
    window: {},
    console,
    setInterval: () => 0,
    clearInterval: () => {},
    fetch: async () => { throw new Error("kein Netz im Test"); },
    Date,
    Set,
    Map,
    Math,
    JSON,
    isNaN,
  };
  kontext.globalThis = kontext;
  vm.createContext(kontext);
  const quelle = fs.readFileSync(
    path.join(__dirname, "static", "app.js"), "utf8");
  vm.runInContext(quelle, kontext, { filename: "app.js" });

  // WICHTIG: function-Deklarationen landen als Eigenschaft am Kontext,
  // const-Deklarationen NICHT - die leben in der lexikalischen Bindung des
  // Skripts. kontext.AKTUALISIERUNG_LAEDT waere also undefined, und der
  // Test wuerde stillschweigend gegen einen unbekannten Zustand pruefen
  // (und damit nur den else-Zweig treffen). Deshalb werden die Konstanten
  // im selben Kontext ausgewertet statt vom Objekt gelesen.
  kontext.wert = ausdruck => vm.runInContext(ausdruck, kontext);
  for (const name of ["AKTUALISIERUNG_NORMAL", "AKTUALISIERUNG_LAEDT",
                       "AKTUALISIERUNG_VERALTET", "MINDESTABSTAND_MS"]) {
    kontext[name] = vm.runInContext(name, kontext);
  }
  return kontext;
}

/* --- 1) Die drei Zustaende schliessen sich aus --------------------------- */

function testeZustaende() {
  console.log("\n1) markiereAktualisierung(): genau ein Zustand");
  const stand = neuesElement("stand", "status");
  const k = baueKontext({ stand });

  k.markiereAktualisierung("stand", k.AKTUALISIERUNG_LAEDT, 0);
  check("laedt setzt die Klasse 'laedt'", stand.classList.contains("laedt"));
  check("laedt setzt KEIN 'veraltet'", !stand.classList.contains("veraltet"),
        `className=${stand.className}`);
  check("laedt erklaert sich im title", stand.title.includes("laeuft"),
        JSON.stringify(stand.title));

  k.markiereAktualisierung("stand", k.AKTUALISIERUNG_VERALTET, 1);
  check("veraltet setzt die Klasse 'veraltet'",
        stand.classList.contains("veraltet"));
  check("veraltet entfernt 'laedt' wieder", !stand.classList.contains("laedt"),
        `className=${stand.className}`);
  check("veraltet nennt die Anzahl Fehlversuche im title",
        stand.title.includes("(1x)"), JSON.stringify(stand.title));

  // Der kritische Uebergang: erneuter Versuch NACH einem Fehlschlag.
  k.markiereAktualisierung("stand", k.AKTUALISIERUNG_LAEDT, 1);
  check("Wiederholung nach Fehler zeigt 'laedt', nicht beides",
        stand.classList.contains("laedt") && !stand.classList.contains("veraltet"),
        `className=${stand.className}`);
  check("Wiederholung nach Fehler nennt den Fehlschlag trotzdem im title",
        stand.title.includes("fehlgeschlagen") && stand.title.includes("(1x)"),
        JSON.stringify(stand.title));

  k.markiereAktualisierung("stand", k.AKTUALISIERUNG_NORMAL, 0);
  check("normal entfernt beide Klassen",
        !stand.classList.contains("laedt") && !stand.classList.contains("veraltet"),
        `className=${stand.className}`);
  check("normal loescht den title", stand.title === "");
  check("Die Grundklasse der Anzeige bleibt unangetastet",
        stand.classList.contains("status"), `className=${stand.className}`);

  check("Ein unbekanntes Element wirft nicht", (() => {
    try { k.markiereAktualisierung("gibtsnicht", k.AKTUALISIERUNG_LAEDT, 0);
          return true; } catch (e) { return false; }
  })());
}

/* --- 2) Ladeanzeige: ueberlappende Aufgaben ------------------------------ */

function testeLadeanzeige() {
  console.log("\n2) Ladeanzeige bei ueberlappenden Aufgaben");
  const anzeige = neuesElement("ladeanzeige");
  const k = baueKontext({ ladeanzeige: anzeige });

  check("Anfangs ausgeblendet", anzeige.hidden === true);

  k.ladeanzeigeAn("Aktualisiere …");
  check("Eine laufende Aufgabe blendet die Anzeige ein",
        anzeige.hidden === false && anzeige.textContent === "Aktualisiere …",
        JSON.stringify(anzeige.textContent));
  check("Der Text steht auch im title (Maus-Hinweis)",
        anzeige.title === anzeige.textContent);

  // Der eigentliche Grund fuer die Liste: der 60-Sekunden-Takt kann
  // anlaufen, waehrend die bis zu 12 Sekunden lange Kursabfrage laeuft.
  k.ladeanzeigeAn("Kurse werden geladen …");
  check("Zwei gleichzeitige Aufgaben werden beide genannt",
        anzeige.textContent.includes("Aktualisiere")
        && anzeige.textContent.includes("Kurse"),
        JSON.stringify(anzeige.textContent));

  k.ladeanzeigeAus("Aktualisiere …");
  check("Endet die kurze Aufgabe, bleibt die lange sichtbar",
        anzeige.hidden === false
        && anzeige.textContent === "Kurse werden geladen …",
        JSON.stringify(anzeige.textContent));

  k.ladeanzeigeAus("Kurse werden geladen …");
  check("Erst wenn nichts mehr laeuft, verschwindet die Anzeige",
        anzeige.hidden === true && anzeige.textContent === "");

  k.ladeanzeigeAus("Kurse werden geladen …");
  check("Doppeltes Abmelden schadet nicht", anzeige.hidden === true);
}

/* --- 3) autoAktualisierung: der ganze Ablauf ----------------------------- */

async function testeAblauf() {
  console.log("\n3) autoAktualisierung(): Zustandsfolge eines Laufs");

  const stand = neuesElement("stand", "status");
  const anzeige = neuesElement("ladeanzeige");
  const k = baueKontext({ stand, ladeanzeige: anzeige });

  const folge = [];
  let sollFehlschlagen = false;

  const ausfuehren = k.autoAktualisierung(
    async () => {
      // Zustand MITTEN im Lauf festhalten - genau der Moment, den ein
      // Test nach dem Lauf nicht mehr sehen wuerde.
      folge.push(["waehrend", stand.className, anzeige.hidden,
                   anzeige.textContent]);
      if (sollFehlschlagen) throw new Error("simulierter Fehler");
    },
    60000,
    (zustand, fehlerInFolge) =>
      k.markiereAktualisierung("stand", zustand, fehlerInFolge),
    "Aktualisiere …");

  // MINDESTABSTAND_MS: der erste Aufruf direkt nach dem Anlegen wird
  // absichtlich verworfen. Das ist gewolltes Verhalten aus PR #44 und
  // hier gleich mitgeprueft.
  await ausfuehren("takt");
  check("Ein Lauf unmittelbar nach dem Start wird unterdrueckt (Mindestabstand)",
        folge.length === 0, `folge=${folge.length}`);

  await new Promise(r => setTimeout(r, k.MINDESTABSTAND_MS + 50));

  await ausfuehren("takt");
  check("Waehrend des Laufs steht 'laedt' und die Anzeige ist sichtbar",
        folge.length === 1 && folge[0][1].includes("laedt")
        && folge[0][2] === false
        && folge[0][3] === "Aktualisiere …",
        JSON.stringify(folge[0]));
  check("Nach dem erfolgreichen Lauf ist die Anzeige wieder weg",
        anzeige.hidden === true);
  check("Nach dem erfolgreichen Lauf ist der Zustand wieder normal",
        stand.className === "status", stand.className);

  await new Promise(r => setTimeout(r, k.MINDESTABSTAND_MS + 50));
  sollFehlschlagen = true;
  await ausfuehren("takt");
  check("Nach einem Fehlschlag steht 'veraltet'",
        stand.classList.contains("veraltet")
        && !stand.classList.contains("laedt"), stand.className);
  check("Ein Fehler laesst die Ladeanzeige NICHT haengen (finally)",
        anzeige.hidden === true && anzeige.textContent === "");

  await new Promise(r => setTimeout(r, k.MINDESTABSTAND_MS + 50));
  await ausfuehren("takt");
  check("Der Wiederholungsversuch meldete waehrenddessen 'laedt' ohne 'veraltet'",
        folge[2][1].includes("laedt") && !folge[2][1].includes("veraltet"),
        JSON.stringify(folge[2]));
  check("Fehlversuche werden weitergezaehlt",
        stand.title.includes("(2x)"), JSON.stringify(stand.title));
}

async function main() {
  console.log("Verhaltenstest: Zustaende der automatischen Aktualisierung");
  testeZustaende();
  testeLadeanzeige();
  await testeAblauf();

  console.log(`\n${bestanden}/${bestanden + fehler.length} Pruefungen bestanden.`);
  fehler.forEach(n => console.log(`FEHLGESCHLAGEN: ${n}`));
  process.exit(fehler.length ? 1 : 0);
}

main();
