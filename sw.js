const CACHE = "reborn-companion-v2"; // bump version to clear old cache
const ASSETS = [
  "./",
  "./index.html",
  "./app.py",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  // Always try network first for app.py and index.html
  if (url.pathname.endsWith("/app.py") || url.pathname.endsWith("/index.html")) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request).then(res => res || fetch(e.request)));
});
