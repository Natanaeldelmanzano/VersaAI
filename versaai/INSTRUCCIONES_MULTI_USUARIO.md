# 🔐 Sistema Multi-Usuario VersaAI - Instrucciones de Uso

## 📋 Usuarios Demo Creados

Se han creado los siguientes usuarios de demostración con diferentes roles:

### 🔴 Super Administrador
- **Email:** `superadmin@versaai.com`
- **Contraseña:** `super123456`
- **Permisos:** Acceso completo al sistema, configuración del sistema, gestión de usuarios y organizaciones

### 🟠 Administrador de Organización
- **Email:** `admin@versaai.com`
- **Contraseña:** `admin123456`
- **Permisos:** Gestión de organización, creación de usuarios, visualización de analíticas

### 🟢 Usuario Estándar
- **Email:** `user@versaai.com`
- **Contraseña:** `user123456`
- **Permisos:** Acceso a datos propios, creación de conversaciones, gestión de chatbots propios

### 🔵 Visualizador
- **Email:** `viewer@versaai.com`
- **Contraseña:** `viewer123456`
- **Permisos:** Solo lectura, visualización de conversaciones y chatbots

### 🟡 Usuario Demo (Adicional)
- **Email:** `demo@versaai.com`
- **Contraseña:** `demo123456`
- **Permisos:** Usuario estándar

## 🚀 Cómo Usar el Sistema

### 1. Acceso Inicial
1. Abre el navegador y ve a `http://localhost:3000`
2. Haz clic en "Iniciar Sesión"
3. Usa cualquiera de las credenciales de arriba

### 2. Cambio de Roles (Modo Demo)
1. Una vez autenticado, busca el componente **"Cambiar Rol"** en el dashboard
2. Selecciona el rol que deseas probar
3. El sistema automáticamente cambiará al usuario correspondiente
4. La página se recargará para reflejar los nuevos permisos

### 3. Funcionalidades por Rol

#### 🔴 Super Administrador
- ✅ Gestión completa de usuarios
- ✅ Configuración del sistema
- ✅ Gestión de organizaciones
- ✅ Acceso a todas las analíticas
- ✅ Eliminación de datos
- ✅ Configuración avanzada

#### 🟠 Administrador de Organización
- ✅ Gestión de usuarios de la organización
- ✅ Creación de nuevos usuarios
- ✅ Visualización de analíticas organizacionales
- ✅ Configuración de la organización
- ❌ Configuración del sistema global

#### 🟢 Usuario Estándar
- ✅ Creación y gestión de conversaciones
- ✅ Gestión de chatbots propios
- ✅ Subida de archivos
- ✅ Analíticas básicas
- ❌ Gestión de otros usuarios
- ❌ Configuración del sistema

#### 🔵 Visualizador
- ✅ Visualización de conversaciones
- ✅ Visualización de chatbots
- ❌ Creación o modificación de contenido
- ❌ Gestión de usuarios
- ❌ Configuración

## 🔧 Características Técnicas

### Autenticación Real
- El sistema usa autenticación JWT real
- Los usuarios están almacenados en la base de datos PostgreSQL
- Los permisos se calculan dinámicamente basados en el rol

### Cambio de Roles
- El componente `RoleSwitcher` permite cambiar entre roles fácilmente
- Cada cambio hace un login real con las credenciales correspondientes
- Los permisos se actualizan automáticamente

### Persistencia
- Los datos de usuario se mantienen en la base de datos
- Las sesiones persisten hasta el logout o expiración del token
- Los permisos se validan tanto en frontend como backend

## 🛠️ Desarrollo y Personalización

### Agregar Nuevos Usuarios
```python
# Ejecutar en el directorio backend
python create_demo_users.py
```

### Modificar Permisos
Edita el archivo `backend/src/schemas/user.py` en el método `get_permissions_for_role()`

### Personalizar Roles
1. Modifica el enum `UserRole` en `backend/src/models/user.py`
2. Actualiza los permisos en `backend/src/schemas/user.py`
3. Actualiza el frontend en `frontend/src/stores/auth.js`

## 🔍 Verificación del Sistema

### Backend
- Servidor corriendo en: `http://localhost:8000`
- Documentación API: `http://localhost:8000/docs`
- Endpoint de usuario actual: `GET /api/v1/auth/me`

### Frontend
- Aplicación corriendo en: `http://localhost:3000`
- RoleSwitcher visible en el dashboard
- Permisos mostrados en tiempo real

## 📞 Soporte

Si encuentras algún problema:
1. Verifica que ambos servidores (frontend y backend) estén corriendo
2. Revisa la consola del navegador para errores
3. Verifica los logs del backend en la terminal
4. Asegúrate de que la base de datos PostgreSQL esté funcionando

---

**¡El sistema multi-usuario está completamente funcional y listo para usar!** 🎉