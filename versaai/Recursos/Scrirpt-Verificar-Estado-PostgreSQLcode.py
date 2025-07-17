# Crear un script para verificar el estado de PostgreSQL
script_content = '''
@echo off
echo Verificando estado de PostgreSQL...
echo.

REM Verificar si PostgreSQL está ejecutándose
tasklist /FI "IMAGENAME eq postgres.exe" 2>NUL | find /I /N "postgres.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ PostgreSQL está ejecutándose
) else (
    echo ❌ PostgreSQL NO está ejecutándose
    echo.
    echo Intentando iniciar PostgreSQL...
    net start postgresql-x64-13
    if "%ERRORLEVEL%"=="0" (
        echo ✅ PostgreSQL iniciado correctamente
    ) else (
        echo ❌ Error al iniciar PostgreSQL
        echo Intenta iniciarlo manualmente desde Servicios de Windows
    )
)

echo.
echo Verificando conexión a la base de datos...
psql -h localhost -p 5432 -U postgres -c "SELECT version();" 2>NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Conexión a PostgreSQL exitosa
) else (
    echo ❌ No se puede conectar a PostgreSQL
    echo Verifica que el servicio esté ejecutándose y las credenciales sean correctas
)

pause
'''

# Guardar el script
with open('/home/user/verificar_postgresql.bat', 'w', encoding='utf-8') as f:
    f.write(script_content)

print("✅ Script creado: verificar_postgresql.bat")
print("\nEjecuta este script en tu terminal de Windows para verificar PostgreSQL")