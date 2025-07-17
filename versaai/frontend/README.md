# VersaAI Enterprise Dashboard - Frontend

<div align="center">
  <img src="https://via.placeholder.com/200x80/4F46E5/FFFFFF?text=VersaAI" alt="VersaAI Logo" />
  
  <h3>Dashboard Empresarial de Inteligencia Artificial</h3>
  
  [![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/versaai/dashboard-frontend)
  [![Vue.js](https://img.shields.io/badge/Vue.js-3.4-4FC08D.svg)](https://vuejs.org/)
  [![Vite](https://img.shields.io/badge/Vite-5.0-646CFF.svg)](https://vitejs.dev/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/versaai/dashboard-frontend/actions)
</div>

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Instalación Rápida](#-instalación-rápida)
- [Desarrollo](#-desarrollo)
- [Despliegue](#-despliegue)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración](#-configuración)
- [Scripts Disponibles](#-scripts-disponibles)
- [Contribución](#-contribución)
- [Soporte](#-soporte)

## 🚀 Características

### Dashboard Empresarial
- **Panel de Control Avanzado**: Métricas en tiempo real y KPIs personalizables
- **Gestión de Chatbots**: Creación, configuración y monitoreo de bots de IA
- **Analytics Avanzados**: Reportes detallados y visualizaciones interactivas
- **Gestión de Usuarios**: Control de acceso basado en roles (RBAC)
- **Integraciones**: Conectores para múltiples plataformas y APIs

### Experiencia de Usuario
- **Responsive Design**: Optimizado para desktop, tablet y móvil
- **PWA Ready**: Aplicación web progresiva con soporte offline
- **Tema Personalizable**: Sistema de temas claro/oscuro
- **Internacionalización**: Soporte multi-idioma
- **Accesibilidad**: Cumple con estándares WCAG 2.1

### Características Técnicas
- **Performance**: Lazy loading, code splitting y optimizaciones avanzadas
- **Seguridad**: CSP, HTTPS, autenticación JWT
- **Monitoreo**: Integración con Sentry y Google Analytics
- **Testing**: Cobertura completa con Vitest y Cypress
- **CI/CD**: Pipelines automatizados de despliegue

## 🛠 Tecnologías

### Frontend Core
- **[Vue.js 3](https://vuejs.org/)** - Framework progresivo de JavaScript
- **[Vite](https://vitejs.dev/)** - Build tool ultrarrápido
- **[TypeScript](https://www.typescriptlang.org/)** - Tipado estático
- **[Vue Router](https://router.vuejs.org/)** - Enrutamiento SPA
- **[Pinia](https://pinia.vuejs.org/)** - Gestión de estado

### UI/UX
- **[Tailwind CSS](https://tailwindcss.com/)** - Framework CSS utility-first
- **[Headless UI](https://headlessui.com/)** - Componentes accesibles
- **[Heroicons](https://heroicons.com/)** - Iconografía SVG
- **[Chart.js](https://www.chartjs.org/)** - Gráficos y visualizaciones
- **[Framer Motion](https://www.framer.com/motion/)** - Animaciones fluidas

### Herramientas de Desarrollo
- **[ESLint](https://eslint.org/)** - Linting de código
- **[Prettier](https://prettier.io/)** - Formateo de código
- **[Vitest](https://vitest.dev/)** - Testing unitario
- **[Cypress](https://www.cypress.io/)** - Testing E2E
- **[Storybook](https://storybook.js.org/)** - Desarrollo de componentes

## ⚡ Instalación Rápida

### Opción 1: Script Automatizado (Recomendado)

```bash
# Descargar y ejecutar script de instalación
curl -fsSL https://raw.githubusercontent.com/versaai/dashboard-frontend/main/install.sh | sudo bash
```

### Opción 2: Docker Compose

```bash
# Clonar repositorio
git clone https://github.com/versaai/dashboard-frontend.git
cd dashboard-frontend

# Configurar variables de entorno
cp .env.example .env
cp .env.production.example .env.production

# Ejecutar con Docker
docker-compose up -d
```

### Opción 3: Instalación Manual

```bash
# Prerrequisitos
node --version  # >= 18.0.0
npm --version   # >= 8.0.0

# Clonar e instalar
git clone https://github.com/versaai/dashboard-frontend.git
cd dashboard-frontend
npm install

# Configurar entorno
cp .env.development.example .env.development

# Ejecutar en desarrollo
npm run dev
```

## 💻 Desarrollo

### Configuración del Entorno de Desarrollo

```bash
# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.development.example .env.development

# Iniciar servidor de desarrollo
npm run dev

# El dashboard estará disponible en http://localhost:3000
```

### Comandos de Desarrollo

```bash
# Desarrollo con hot reload
npm run dev

# Build para producción
npm run build:prod

# Preview del build de producción
npm run preview:prod

# Ejecutar tests
npm run test:unit
npm run test:e2e

# Linting y formateo
npm run lint
npm run format

# Análisis del bundle
npm run build:analyze
```

### Estructura de Desarrollo

```
src/
├── api/              # Servicios de API
├── assets/           # Recursos estáticos
├── components/       # Componentes Vue reutilizables
│   ├── auth/         # Componentes de autenticación
│   ├── chatbots/     # Componentes de chatbots
│   ├── dashboard/    # Componentes del dashboard
│   ├── layout/       # Componentes de layout
│   ├── mobile/       # Componentes móviles
│   └── ui/           # Componentes UI base
├── composables/      # Composables de Vue
├── config/           # Configuraciones
├── layouts/          # Layouts de página
├── middleware/       # Middleware de rutas
├── plugins/          # Plugins de Vue
├── router/           # Configuración de rutas
├── services/         # Servicios de negocio
├── stores/           # Stores de Pinia
├── utils/            # Utilidades
└── views/            # Páginas/Vistas
    ├── analytics/    # Vistas de analytics
    ├── auth/         # Vistas de autenticación
    ├── chatbots/     # Vistas de chatbots
    ├── dashboard/    # Vistas del dashboard
    └── mobile/       # Vistas móviles
```

## 🌐 Despliegue

### Despliegue en Producción

Para instrucciones detalladas de despliegue, consulta:
- **[Guía de Despliegue](DEPLOYMENT.md)** - Documentación completa
- **[Script de Instalación](install.sh)** - Instalación automatizada
- **[Script de Actualización](update.sh)** - Actualizaciones automáticas

### Opciones de Despliegue

#### 1. Servidor VPS/Dedicado
```bash
# Instalación completa automatizada
curl -fsSL https://raw.githubusercontent.com/versaai/dashboard-frontend/main/install.sh | sudo bash
```

#### 2. Servicios en la Nube

**Vercel (Recomendado)**
- Build Command: `npm run build:prod`
- Output Directory: `dist`
- Node.js Version: `18.x`

**Netlify**
- Build Command: `npm run build:prod`
- Publish Directory: `dist`
- Node.js Version: `18`

**AWS S3 + CloudFront**
```bash
npm run build:prod
aws s3 sync dist/ s3://your-bucket --delete
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

#### 3. Docker
```bash
# Build imagen
docker build -t versaai-dashboard .

# Ejecutar contenedor
docker run -p 80:80 versaai-dashboard

# Con Docker Compose
docker-compose up -d
```

### Variables de Entorno

#### Producción (.env.production)
```bash
# API Configuration
VITE_API_URL=https://api.versaai.com
VITE_API_VERSION=v1

# App Configuration
VITE_APP_NAME=VersaAI Enterprise Dashboard
VITE_APP_VERSION=2.0.0
VITE_APP_DESCRIPTION=Dashboard empresarial de IA

# Features
VITE_ENABLE_PWA=true
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_REAL_TIME=true
VITE_ENABLE_MOBILE=true

# Security
VITE_ENABLE_CSP=true
VITE_ENABLE_HTTPS_ONLY=true

# External Services
VITE_GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
VITE_SENTRY_DSN=https://xxx@sentry.io/xxx
```

## 📁 Estructura del Proyecto

```
versaai-frontend/
├── public/                 # Archivos públicos
│   ├── favicon.ico
│   ├── manifest.json
│   └── robots.txt
├── src/                    # Código fuente
│   ├── api/               # Servicios de API
│   ├── assets/            # Recursos estáticos
│   ├── components/        # Componentes Vue
│   ├── composables/       # Composables
│   ├── config/            # Configuraciones
│   ├── layouts/           # Layouts
│   ├── middleware/        # Middleware
│   ├── plugins/           # Plugins
│   ├── router/            # Enrutamiento
│   ├── services/          # Servicios
│   ├── stores/            # Estado global
│   ├── utils/             # Utilidades
│   ├── views/             # Vistas/Páginas
│   ├── App.vue            # Componente raíz
│   └── main.js            # Punto de entrada
├── tests/                  # Tests
│   ├── unit/              # Tests unitarios
│   └── e2e/               # Tests E2E
├── docs/                   # Documentación
├── scripts/                # Scripts de utilidad
├── .env.development        # Variables de desarrollo
├── .env.production         # Variables de producción
├── docker-compose.yml      # Configuración Docker
├── Dockerfile              # Imagen Docker
├── nginx.conf              # Configuración Nginx
├── package.json            # Dependencias y scripts
├── vite.config.js          # Configuración Vite
├── tailwind.config.js      # Configuración Tailwind
├── tsconfig.json           # Configuración TypeScript
├── install.sh              # Script de instalación
├── update.sh               # Script de actualización
├── DEPLOYMENT.md           # Guía de despliegue
└── README.md               # Este archivo
```

## ⚙️ Configuración

### Configuración de Vite (vite.config.js)

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  build: {
    outDir: 'dist',
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['@headlessui/vue', '@heroicons/vue'],
          charts: ['chart.js', 'vue-chartjs']
        }
      }
    }
  }
})
```

### Configuración de Tailwind (tailwind.config.js)

```javascript
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a'
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}
```

## 📜 Scripts Disponibles

### Desarrollo
```bash
npm run dev              # Servidor de desarrollo
npm run dev:host         # Servidor accesible en red
npm run dev:https        # Servidor con HTTPS
```

### Build
```bash
npm run build            # Build básico
npm run build:prod       # Build optimizado para producción
npm run build:staging    # Build para staging
npm run build:analyze    # Build con análisis de bundle
```

### Testing
```bash
npm run test             # Todos los tests
npm run test:unit        # Tests unitarios
npm run test:e2e         # Tests E2E
npm run test:coverage    # Tests con cobertura
```

### Calidad de Código
```bash
npm run lint             # Linting
npm run lint:fix         # Linting con auto-fix
npm run format           # Formateo con Prettier
npm run type-check       # Verificación de tipos
```

### Utilidades
```bash
npm run preview          # Preview del build
npm run clean            # Limpiar archivos generados
npm run serve            # Servidor estático
```

### Despliegue
```bash
npm run deploy:staging   # Desplegar a staging
npm run deploy:prod      # Desplegar a producción
```

## 🤝 Contribución

### Guía de Contribución

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Estándares de Código

- **ESLint**: Seguir las reglas configuradas
- **Prettier**: Formateo automático
- **Conventional Commits**: Para mensajes de commit
- **Tests**: Cobertura mínima del 80%

### Estructura de Commits

```
type(scope): description

[optional body]

[optional footer]
```

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formateo, punto y coma faltante, etc.
- `refactor`: Refactorización de código
- `test`: Agregar tests
- `chore`: Mantenimiento

### Proceso de Review

1. **Automated Checks**: CI/CD debe pasar
2. **Code Review**: Al menos 1 aprobación
3. **Testing**: Tests unitarios y E2E
4. **Documentation**: Actualizar docs si es necesario

## 📞 Soporte

### Canales de Soporte

- **📧 Email**: [support@versaai.com](mailto:support@versaai.com)
- **📖 Documentación**: [docs.versaai.com](https://docs.versaai.com)
- **🐛 Issues**: [GitHub Issues](https://github.com/versaai/dashboard-frontend/issues)
- **💬 Discord**: [VersaAI Community](https://discord.gg/versaai)
- **📱 Twitter**: [@VersaAI](https://twitter.com/versaai)

### FAQ

**P: ¿Cómo actualizo el dashboard?**
R: Usa el script de actualización: `sudo ./update.sh`

**P: ¿Cómo configuro HTTPS?**
R: El script de instalación incluye configuración automática de SSL con Let's Encrypt.

**P: ¿Puedo personalizar el tema?**
R: Sí, modifica los archivos en `src/assets/styles/` y `tailwind.config.js`.

**P: ¿Cómo habilito el modo PWA?**
R: Establece `VITE_ENABLE_PWA=true` en tu archivo `.env.production`.

### Recursos Adicionales

- **[Guía de Despliegue](DEPLOYMENT.md)** - Instrucciones detalladas de despliegue
- **[Changelog](CHANGELOG.md)** - Historial de cambios
- **[Roadmap](ROADMAP.md)** - Funcionalidades planificadas
- **[Contributing](CONTRIBUTING.md)** - Guía de contribución
- **[Security](SECURITY.md)** - Política de seguridad

---

<div align="center">
  <p>Hecho con ❤️ por el equipo de VersaAI</p>
  <p>
    <a href="https://github.com/versaai/dashboard-frontend/blob/main/LICENSE">Licencia MIT</a> •
    <a href="https://versaai.com">Sitio Web</a> •
    <a href="https://docs.versaai.com">Documentación</a>
  </p>
</div>