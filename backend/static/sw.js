/**
 * SnapLinked v3.0 - Service Worker
 * PWA, Cache e Funcionalidades Offline
 */

const CACHE_NAME = 'snaplinked-v3.0.1';
const STATIC_CACHE = 'snaplinked-static-v3.0.1';
const DYNAMIC_CACHE = 'snaplinked-dynamic-v3.0.1';

// Recursos para cache estático
const STATIC_ASSETS = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/manifest.json',
    '/static/images/icon-192x192.png',
    '/static/images/icon-512x512.png'
];

// Recursos para cache dinâmico
const DYNAMIC_ASSETS = [
    '/api/status',
    '/api/health'
];

// URLs que devem sempre buscar da rede
const NETWORK_FIRST = [
    '/api/auth/',
    '/api/automation/',
    '/api/stats/'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
    console.log('🔧 Service Worker: Instalando...');
    
    event.waitUntil(
        Promise.all([
            // Cache estático
            caches.open(STATIC_CACHE).then((cache) => {
                console.log('📦 Service Worker: Cacheando recursos estáticos');
                return cache.addAll(STATIC_ASSETS);
            }),
            
            // Pular waiting para ativar imediatamente
            self.skipWaiting()
        ])
    );
});

// Ativar Service Worker
self.addEventListener('activate', (event) => {
    console.log('✅ Service Worker: Ativando...');
    
    event.waitUntil(
        Promise.all([
            // Limpar caches antigos
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        if (cacheName !== STATIC_CACHE && 
                            cacheName !== DYNAMIC_CACHE && 
                            cacheName !== CACHE_NAME) {
                            console.log('🗑️ Service Worker: Removendo cache antigo:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            
            // Tomar controle de todas as abas
            self.clients.claim()
        ])
    );
});

// Interceptar requisições
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Ignorar requisições não-HTTP
    if (!request.url.startsWith('http')) {
        return;
    }
    
    // Ignorar requisições para outros domínios (exceto LinkedIn)
    if (url.origin !== self.location.origin && !url.hostname.includes('linkedin.com')) {
        return;
    }
    
    event.respondWith(handleRequest(request));
});

// Gerenciar requisições
async function handleRequest(request) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    try {
        // Estratégia Network First para APIs críticas
        if (NETWORK_FIRST.some(pattern => path.startsWith(pattern))) {
            return await networkFirst(request);
        }
        
        // Estratégia Cache First para recursos estáticos
        if (STATIC_ASSETS.includes(path) || path.startsWith('/static/')) {
            return await cacheFirst(request);
        }
        
        // Estratégia Stale While Revalidate para APIs dinâmicas
        if (path.startsWith('/api/')) {
            return await staleWhileRevalidate(request);
        }
        
        // Estratégia Network First com fallback para páginas
        return await networkFirstWithFallback(request);
        
    } catch (error) {
        console.error('❌ Service Worker: Erro ao processar requisição:', error);
        return await handleOffline(request);
    }
}

// Estratégia Network First
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        // Cache apenas respostas bem-sucedidas
        if (networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('🌐 Service Worker: Rede indisponível, buscando no cache');
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        throw error;
    }
}

// Estratégia Cache First
async function cacheFirst(request) {
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
        return cachedResponse;
    }
    
    try {
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('❌ Service Worker: Falha ao buscar recurso:', request.url);
        throw error;
    }
}

// Estratégia Stale While Revalidate
async function staleWhileRevalidate(request) {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    // Buscar da rede em background
    const networkPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(() => {
        // Ignorar erros de rede silenciosamente
    });
    
    // Retornar cache imediatamente se disponível
    if (cachedResponse) {
        return cachedResponse;
    }
    
    // Aguardar rede se não há cache
    return await networkPromise;
}

// Estratégia Network First com Fallback
async function networkFirstWithFallback(request) {
    try {
        return await fetch(request);
    } catch (error) {
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Fallback para página offline
        if (request.mode === 'navigate') {
            return await caches.match('/') || new Response(
                createOfflinePage(),
                { 
                    headers: { 'Content-Type': 'text/html' },
                    status: 200
                }
            );
        }
        
        throw error;
    }
}

// Lidar com estado offline
async function handleOffline(request) {
    if (request.mode === 'navigate') {
        const cachedPage = await caches.match('/');
        if (cachedPage) {
            return cachedPage;
        }
        
        return new Response(
            createOfflinePage(),
            { 
                headers: { 'Content-Type': 'text/html' },
                status: 200
            }
        );
    }
    
    // Para outros tipos de requisição, retornar erro
    return new Response(
        JSON.stringify({ 
            error: 'Offline', 
            message: 'Você está offline. Verifique sua conexão.' 
        }),
        { 
            headers: { 'Content-Type': 'application/json' },
            status: 503
        }
    );
}

// Criar página offline
function createOfflinePage() {
    return `
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SnapLinked - Offline</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            .offline-container {
                max-width: 500px;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 1rem;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .offline-icon {
                font-size: 4rem;
                margin-bottom: 1rem;
            }
            .offline-title {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }
            .offline-message {
                font-size: 1.1rem;
                margin-bottom: 2rem;
                opacity: 0.9;
                line-height: 1.6;
            }
            .retry-button {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 0.75rem 1.5rem;
                border-radius: 0.5rem;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .retry-button:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="offline-container">
            <div class="offline-icon">📡</div>
            <h1 class="offline-title">Você está offline</h1>
            <p class="offline-message">
                Não foi possível conectar ao SnapLinked. 
                Verifique sua conexão com a internet e tente novamente.
            </p>
            <button class="retry-button" onclick="window.location.reload()">
                🔄 Tentar Novamente
            </button>
        </div>
    </body>
    </html>
    `;
}

// Lidar com mensagens do cliente
self.addEventListener('message', (event) => {
    const { type, payload } = event.data;
    
    switch (type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'GET_VERSION':
            event.ports[0].postMessage({ version: CACHE_NAME });
            break;
            
        case 'CLEAR_CACHE':
            clearAllCaches().then(() => {
                event.ports[0].postMessage({ success: true });
            });
            break;
            
        case 'CACHE_URLS':
            if (payload && payload.urls) {
                cacheUrls(payload.urls).then(() => {
                    event.ports[0].postMessage({ success: true });
                });
            }
            break;
    }
});

// Limpar todos os caches
async function clearAllCaches() {
    const cacheNames = await caches.keys();
    return Promise.all(
        cacheNames.map(cacheName => caches.delete(cacheName))
    );
}

// Cache URLs específicas
async function cacheUrls(urls) {
    const cache = await caches.open(DYNAMIC_CACHE);
    return Promise.all(
        urls.map(url => {
            return fetch(url).then(response => {
                if (response.ok) {
                    return cache.put(url, response);
                }
            }).catch(() => {
                // Ignorar erros silenciosamente
            });
        })
    );
}

// Notificações Push (placeholder)
self.addEventListener('push', (event) => {
    if (!event.data) return;
    
    const data = event.data.json();
    const options = {
        body: data.body || 'Nova notificação do SnapLinked',
        icon: '/static/images/icon-192x192.png',
        badge: '/static/images/badge-72x72.png',
        tag: data.tag || 'snaplinked-notification',
        renotify: true,
        requireInteraction: true,
        actions: [
            {
                action: 'open',
                title: 'Abrir SnapLinked',
                icon: '/static/images/action-open.png'
            },
            {
                action: 'dismiss',
                title: 'Dispensar',
                icon: '/static/images/action-dismiss.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'SnapLinked', options)
    );
});

// Clique em notificação
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    
    if (event.action === 'open' || !event.action) {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Sincronização em background
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Executar sincronização em background
async function doBackgroundSync() {
    try {
        // Sincronizar dados pendentes
        console.log('🔄 Service Worker: Executando sincronização em background');
        
        // Implementar lógica de sincronização aqui
        // Por exemplo: enviar dados offline para o servidor
        
    } catch (error) {
        console.error('❌ Service Worker: Erro na sincronização:', error);
    }
}

console.log('🚀 Service Worker: SnapLinked v3.0 carregado');
