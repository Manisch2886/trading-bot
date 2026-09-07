/* Service Worker - macht die Seite auf dem iPhone installierbar und
   sorgt dafuer, dass die Huelle (HTML/CSS/JS/Icons) auch ohne Netz
   laedt.

   WICHTIG - API-Antworten werden BEWUSST NIE zwischengespeichert:
   Kursdaten, offene Positionen und PnL-Zahlen aus dem Cache anzuzeigen,
   waere schlimmer als gar nichts anzuzeigen - man saehe alte Zahlen,
   ohne zu merken, dass sie alt sind. Alles unter /api/ geht deshalb
   ausschliesslich ans Netz; faellt das aus, zeigt die Seite ihre
   eigenen Fehlerhinweise. */

const CACHE = "dashboard-huelle-v1";
const HUELLE = [
  "/",
  "/bot",
  "/statisch/style.css",
  "/statisch/app.js",
  "/statisch/icon-192.png",
  "/statisch/icon-512.png",
  "/manifest.json",
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(HUELLE)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(namen => Promise.all(namen.filter(n => n !== CACHE).map(n => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);

  if (url.origin !== self.location.origin) return;          // nichts Fremdes anfassen
  if (url.pathname.startsWith("/api/")) return;             // niemals Daten cachen
  if (url.pathname === "/login" || url.pathname === "/abmelden") return;
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then(antwort => {
        // Nur erfolgreiche Antworten aufnehmen - eine 401-Weiterleitung
        // auf die Login-Seite darf nicht als Startseite haengenbleiben.
        if (antwort.ok && antwort.type === "basic") {
          const kopie = antwort.clone();
          caches.open(CACHE).then(cache => cache.put(event.request, kopie));
        }
        return antwort;
      })
      .catch(() => caches.match(event.request))
  );
});
