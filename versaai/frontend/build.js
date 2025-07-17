#!/usr/bin/env node

/**
 * Script de construcción optimizado para VersaAI Dashboard
 * Incluye optimizaciones para producción y configuraciones de despliegue
 */

const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')
const { performance } = require('perf_hooks')

// Colores para la consola
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
}

const log = {
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  step: (msg) => console.log(`${colors.cyan}▶${colors.reset} ${msg}`)
}

class BuildOptimizer {
  constructor() {
    this.startTime = performance.now()
    this.buildInfo = {
      timestamp: new Date().toISOString(),
      version: this.getVersion(),
      gitCommit: this.getGitCommit(),
      nodeVersion: process.version,
      platform: process.platform
    }
  }

  getVersion() {
    try {
      const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'))
      return packageJson.version || '1.0.0'
    } catch {
      return '1.0.0'
    }
  }

  getGitCommit() {
    try {
      return execSync('git rev-parse HEAD', { encoding: 'utf8' }).trim()
    } catch {
      return 'unknown'
    }
  }

  updateEnvFile() {
    log.step('Actualizando variables de entorno...')
    
    const envFile = '.env.production'
    if (fs.existsSync(envFile)) {
      let envContent = fs.readFileSync(envFile, 'utf8')
      
      // Reemplazar placeholders con valores reales
      envContent = envContent.replace('__BUILD_TIMESTAMP__', this.buildInfo.timestamp)
      envContent = envContent.replace('__BUILD_VERSION__', this.buildInfo.version)
      envContent = envContent.replace('__GIT_COMMIT__', this.buildInfo.gitCommit)
      
      fs.writeFileSync(envFile, envContent)
      log.success('Variables de entorno actualizadas')
    }
  }

  cleanDist() {
    log.step('Limpiando directorio de distribución...')
    
    const distPath = path.join(__dirname, 'dist')
    if (fs.existsSync(distPath)) {
      fs.rmSync(distPath, { recursive: true, force: true })
    }
    
    log.success('Directorio dist limpiado')
  }

  installDependencies() {
    log.step('Verificando dependencias...')
    
    try {
      execSync('npm ci --production=false', { stdio: 'inherit' })
      log.success('Dependencias instaladas correctamente')
    } catch (error) {
      log.error('Error instalando dependencias')
      throw error
    }
  }

  runLinting() {
    log.step('Ejecutando linting...')
    
    try {
      execSync('npm run lint', { stdio: 'inherit' })
      log.success('Linting completado sin errores')
    } catch (error) {
      log.warning('Linting completado con advertencias')
      // No detener el build por warnings de linting
    }
  }

  runTests() {
    log.step('Ejecutando tests...')
    
    try {
      execSync('npm run test:unit', { stdio: 'inherit' })
      log.success('Tests ejecutados correctamente')
    } catch (error) {
      log.warning('Tests fallaron, continuando con el build...')
      // En producción, podrías querer detener aquí
    }
  }

  buildProject() {
    log.step('Construyendo proyecto para producción...')
    
    try {
      execSync('npm run build', { 
        stdio: 'inherit',
        env: { 
          ...process.env, 
          NODE_ENV: 'production',
          VITE_BUILD_TIMESTAMP: this.buildInfo.timestamp,
          VITE_BUILD_VERSION: this.buildInfo.version,
          VITE_GIT_COMMIT: this.buildInfo.gitCommit
        }
      })
      log.success('Proyecto construido correctamente')
    } catch (error) {
      log.error('Error en la construcción del proyecto')
      throw error
    }
  }

  optimizeAssets() {
    log.step('Optimizando assets...')
    
    const distPath = path.join(__dirname, 'dist')
    
    // Crear archivo de información del build
    const buildInfoPath = path.join(distPath, 'build-info.json')
    fs.writeFileSync(buildInfoPath, JSON.stringify(this.buildInfo, null, 2))
    
    // Crear archivo .htaccess para Apache (si es necesario)
    const htaccessContent = `
# VersaAI Dashboard - Configuración Apache
RewriteEngine On

# Handle Angular and Vue.js Router
RewriteBase /
RewriteRule ^index\.html$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.html [L]

# Security Headers
Header always set X-Frame-Options DENY
Header always set X-Content-Type-Options nosniff
Header always set X-XSS-Protection "1; mode=block"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"

# Cache Control
<filesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$">
  ExpiresActive On
  ExpiresDefault "access plus 1 year"
  Header append Cache-Control "public, immutable"
</filesMatch>

<filesMatch "\.(html)$">
  ExpiresActive On
  ExpiresDefault "access plus 0 seconds"
  Header set Cache-Control "no-cache, no-store, must-revalidate"
</filesMatch>

# Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/plain
  AddOutputFilterByType DEFLATE text/html
  AddOutputFilterByType DEFLATE text/xml
  AddOutputFilterByType DEFLATE text/css
  AddOutputFilterByType DEFLATE application/xml
  AddOutputFilterByType DEFLATE application/xhtml+xml
  AddOutputFilterByType DEFLATE application/rss+xml
  AddOutputFilterByType DEFLATE application/javascript
  AddOutputFilterByType DEFLATE application/x-javascript
</IfModule>
`
    
    fs.writeFileSync(path.join(distPath, '.htaccess'), htaccessContent.trim())
    
    log.success('Assets optimizados')
  }

  generateSitemap() {
    log.step('Generando sitemap...')
    
    const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://dashboard.versaai.com/</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://dashboard.versaai.com/auth/login</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>`
    
    const distPath = path.join(__dirname, 'dist')
    fs.writeFileSync(path.join(distPath, 'sitemap.xml'), sitemap)
    
    log.success('Sitemap generado')
  }

  generateRobotsTxt() {
    log.step('Generando robots.txt...')
    
    const robots = `User-agent: *
Disallow: /api/
Disallow: /admin/
Disallow: /dashboard/
Allow: /

Sitemap: https://dashboard.versaai.com/sitemap.xml`
    
    const distPath = path.join(__dirname, 'dist')
    fs.writeFileSync(path.join(distPath, 'robots.txt'), robots)
    
    log.success('robots.txt generado')
  }

  analyzeBundle() {
    log.step('Analizando bundle...')
    
    const distPath = path.join(__dirname, 'dist')
    const stats = this.getDirectorySize(distPath)
    
    log.info(`Tamaño total del bundle: ${this.formatBytes(stats.size)}`)
    log.info(`Número de archivos: ${stats.files}`)
    
    // Verificar archivos grandes
    const largeFiles = this.findLargeFiles(distPath, 1024 * 1024) // 1MB
    if (largeFiles.length > 0) {
      log.warning('Archivos grandes detectados:')
      largeFiles.forEach(file => {
        log.warning(`  ${file.name}: ${this.formatBytes(file.size)}`)
      })
    }
    
    log.success('Análisis de bundle completado')
  }

  getDirectorySize(dirPath) {
    let totalSize = 0
    let totalFiles = 0
    
    const files = fs.readdirSync(dirPath)
    
    files.forEach(file => {
      const filePath = path.join(dirPath, file)
      const stats = fs.statSync(filePath)
      
      if (stats.isDirectory()) {
        const subStats = this.getDirectorySize(filePath)
        totalSize += subStats.size
        totalFiles += subStats.files
      } else {
        totalSize += stats.size
        totalFiles++
      }
    })
    
    return { size: totalSize, files: totalFiles }
  }

  findLargeFiles(dirPath, threshold) {
    const largeFiles = []
    
    const files = fs.readdirSync(dirPath)
    
    files.forEach(file => {
      const filePath = path.join(dirPath, file)
      const stats = fs.statSync(filePath)
      
      if (stats.isDirectory()) {
        largeFiles.push(...this.findLargeFiles(filePath, threshold))
      } else if (stats.size > threshold) {
        largeFiles.push({
          name: path.relative(__dirname, filePath),
          size: stats.size
        })
      }
    })
    
    return largeFiles
  }

  formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  async run() {
    try {
      console.log(`${colors.bright}${colors.magenta}🚀 VersaAI Dashboard - Build Optimizer${colors.reset}\n`)
      
      // Pasos del build
      this.updateEnvFile()
      this.cleanDist()
      this.installDependencies()
      this.runLinting()
      // this.runTests() // Descomenta si tienes tests
      this.buildProject()
      this.optimizeAssets()
      this.generateSitemap()
      this.generateRobotsTxt()
      this.analyzeBundle()
      
      const endTime = performance.now()
      const duration = ((endTime - this.startTime) / 1000).toFixed(2)
      
      console.log(`\n${colors.bright}${colors.green}✅ Build completado exitosamente en ${duration}s${colors.reset}`)
      console.log(`${colors.cyan}📦 Archivos listos en: ./dist${colors.reset}`)
      console.log(`${colors.cyan}🌐 Versión: ${this.buildInfo.version}${colors.reset}`)
      console.log(`${colors.cyan}📅 Timestamp: ${this.buildInfo.timestamp}${colors.reset}\n`)
      
    } catch (error) {
      const endTime = performance.now()
      const duration = ((endTime - this.startTime) / 1000).toFixed(2)
      
      console.log(`\n${colors.bright}${colors.red}❌ Build falló después de ${duration}s${colors.reset}`)
      console.log(`${colors.red}Error: ${error.message}${colors.reset}\n`)
      
      process.exit(1)
    }
  }
}

// Ejecutar el build optimizer
if (require.main === module) {
  const optimizer = new BuildOptimizer()
  optimizer.run()
}

module.exports = BuildOptimizer