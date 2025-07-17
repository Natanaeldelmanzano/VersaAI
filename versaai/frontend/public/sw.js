// Service Worker para VersaAI
// Versión: 1.0.0

const CACHE_NAME = 'versaai-v1.0.0'
const STATIC_CACHE = 'versaai-static-v1.0.0'
const DYNAMIC_CACHE = 'versaai-dynamic-v1.0.0'
const API_CACHE = 'versaai-api-v1.0.0'

// Recursos estáticos para cachear
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  // CSS y JS se cachearán automáticamente por Vite
]

// Rutas de API que se pueden cachear
const CACHEABLE_API_ROUTES = [
  '/api/v1/health',
  '/api/v1/user/profile',
  '/api/v1/organizations',
  '/api/v1/chatbots',
]

// Rutas que requieren conexión (no cachear)
const NETWORK_ONLY_ROUTES = [
  '/api/v1/auth/login',
  '/api/v1/auth/register',
  '/api/v1/auth/logout',
  '/api/v1/conversations',
  '/api/v1/analytics',
]

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker: Instalando...')
  
  event.waitUntil(
    Promise.all([
      // Cachear recursos estáticos
      caches.open(STATIC_CACHE).then((cache) => {
        console.log('Service Worker: Cacheando recursos estáticos')
        return cache.addAll(STATIC_ASSETS)
      }),
      // Forzar activación inmediata
      self.skipWaiting()
    ])
  )
})

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activando...')
  
  event.waitUntil(
    Promise.all([
      // Limpiar caches antiguos
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && 
                cacheName !== DYNAMIC_CACHE && 
                cacheName !== API_CACHE) {
              console.log('Service Worker: Eliminando cache antiguo:', cacheName)
              return caches.delete(cacheName)
            }
          })
        )
      }),
      // Tomar control inmediato
      self.clients.claim()
    ])
  )
})

// Interceptar requests
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // Solo manejar requests del mismo origen
  if (url.origin !== location.origin) {
    return
  }
  
  // Estrategia basada en el tipo de request
  if (request.method === 'GET') {
    if (isStaticAsset(request)) {
      // Cache First para recursos estáticos
      event.respondWith(cacheFirst(request, STATIC_CACHE))
    } else if (isAPIRequest(request)) {
      // Estrategia específica para API
      event.respondWith(handleAPIRequest(request))
    } else {
      // Network First para páginas
      event.respondWith(networkFirst(request, DYNAMIC_CACHE))
    }
  }
})

// Estrategia Cache First
async function cacheFirst(request, cacheName) {
  try {
    const cache = await caches.open(cacheName)
    const cachedResponse = await cache.match(request)
    
    if (cachedResponse) {
      // Actualizar cache en background
      updateCacheInBackground(request, cache)
      return cachedResponse
    }
    
    // Si no está en cache, buscar en red
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (error) {
    console.error('Cache First error:', error)
    return createErrorResponse('Recurso no disponible offline')
  }
}

// Estrategia Network First
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName)
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (error) {
    console.log('Network failed, trying cache:', request.url)
    
    const cache = await caches.open(cacheName)
    const cachedResponse = await cache.match(request)
    
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Fallback para páginas HTML
    if (request.destination === 'document') {
      const fallbackResponse = await cache.match('/')
      if (fallbackResponse) {
        return fallbackResponse
      }
    }
    
    return createErrorResponse('Página no disponible offline')
  }
}

// Manejo específico de requests de API
async function handleAPIRequest(request) {
  const url = new URL(request.url)
  const pathname = url.pathname
  
  // Rutas que requieren conexión
  if (NETWORK_ONLY_ROUTES.some(route => pathname.includes(route))) {
    try {
      return await fetch(request)
    } catch (error) {
      return createErrorResponse('Conexión requerida para esta acción', 503)
    }
  }
  
  // Rutas cacheables
  if (CACHEABLE_API_ROUTES.some(route => pathname.includes(route))) {
    return await staleWhileRevalidate(request, API_CACHE)
  }
  
  // Por defecto, intentar red primero
  try {
    const response = await fetch(request)
    
    // Cachear respuestas exitosas de GET
    if (response.ok && request.method === 'GET') {
      const cache = await caches.open(API_CACHE)
      cache.put(request, response.clone())
    }
    
    return response
  } catch (error) {
    return createErrorResponse('API no disponible', 503)
  }
}

// Estrategia Stale While Revalidate
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName)
  const cachedResponse = await cache.match(request)
  
  // Actualizar en background
  const fetchPromise = fetch(request).then((networkResponse) => {
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
    return networkResponse
  }).catch(() => {
    // Silenciar errores de red en background
  })
  
  // Devolver cache inmediatamente si existe
  if (cachedResponse) {
    return cachedResponse
  }
  
  // Si no hay cache, esperar la red
  try {
    return await fetchPromise
  } catch (error) {
    return createErrorResponse('Datos no disponibles', 503)
  }
}

// Actualizar cache en background
async function updateCacheInBackground(request, cache) {
  try {
    const networkResponse = await fetch(request)
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
  } catch (error) {
    // Silenciar errores de actualización en background
  }
}

// Helpers
function isStaticAsset(request) {
  const url = new URL(request.url)
  return url.pathname.match(/\.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$/)
}

function isAPIRequest(request) {
  const url = new URL(request.url)
  return url.pathname.startsWith('/api/')
}

function createErrorResponse(message, status = 404) {
  return new Response(
    JSON.stringify({
      error: true,
      message: message,
      offline: !navigator.onLine
    }),
    {
      status: status,
      statusText: message,
      headers: {
        'Content-Type': 'application/json'
      }
    }
  )
}

// Manejo de mensajes del cliente
self.addEventListener('message', (event) => {
  const { type, payload } = event.data
  
  switch (type) {
    case 'SKIP_WAITING':
      self.skipWaiting()
      break
      
    case 'GET_VERSION':
      event.ports[0].postMessage({
        version: CACHE_NAME,
        caches: [STATIC_CACHE, DYNAMIC_CACHE, API_CACHE]
      })
      break
      
    case 'CLEAR_CACHE':
      clearAllCaches().then(() => {
        event.ports[0].postMessage({ success: true })
      })
      break
      
    case 'CACHE_URLS':
      if (payload && payload.urls) {
        cacheUrls(payload.urls).then(() => {
          event.ports[0].postMessage({ success: true })
        })
      }
      break
  }
})

// Funciones de utilidad
async function clearAllCaches() {
  const cacheNames = await caches.keys()
  return Promise.all(
    cacheNames.map(cacheName => caches.delete(cacheName))
  )
}

async function cacheUrls(urls) {
  const cache = await caches.open(DYNAMIC_CACHE)
  return cache.addAll(urls)
}

// Notificaciones push (preparado para futuro)
self.addEventListener('push', (event) => {
  if (!event.data) return
  
  const data = event.data.json()
  const options = {
    body: data.body,
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    data: data.data || {},
    actions: data.actions || []
  }
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  )
})

// Manejo de clicks en notificaciones
self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  
  const { action, data } = event
  
  event.waitUntil(
    clients.openWindow(data.url || '/')
  )
})

console.log('Service Worker: Registrado correctamente')