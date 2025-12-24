// Service Worker for PWA - Updated for fresh data
const CACHE_NAME = 'teachmap-v1.1';  // Increment version to force update
const urlsToCache = [
    '/',
    '/css/style.css',
    '/images/icon-192.png',
    '/images/icon-512.png'
];

// Install event - cache static resources
self.addEventListener('install', (event) => {
    console.log('[SW] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Caching static files');
                return cache.addAll(urlsToCache);
            })
            .then(() => self.skipWaiting())  // Force activate immediately
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => {
                        console.log('[SW] Deleting old cache:', name);
                        return caches.delete(name);
                    })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - Network First for API, Cache for static files
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // NEVER cache API calls - always fetch fresh data
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request).catch((error) => {
                console.error('[SW] API fetch failed:', error);
                return new Response(JSON.stringify({ error: 'Network error' }), {
                    headers: { 'Content-Type': 'application/json' }
                });
            })
        );
        return;
    }

    // Network-first for HTML pages
    if (event.request.mode === 'navigate' || event.request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    // Cache the new version
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });
                    return response;
                })
                .catch(() => {
                    // Fallback to cache if offline
                    return caches.match(event.request);
                })
        );
        return;
    }

    // Cache-first for static assets (CSS, JS, images)
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                if (response) {
                    return response;
                }

                return fetch(event.request).then((response) => {
                    // Check if valid response
                    if (!response || response.status !== 200) {
                        return response;
                    }

                    // Cache the new file
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseToCache);
                    });

                    return response;
                });
            })
    );
});
