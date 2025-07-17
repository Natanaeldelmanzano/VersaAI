#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    try:
        # Obtener URL de la base de datos
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ ERROR: DATABASE_URL no encontrada en .env")
            return False
        
        print(f"🔗 Conectando a: {database_url}")
        
        # Crear engine
        engine = create_engine(database_url)
        
        # Probar conexión
        with engine.connect() as connection:
            # Ejecutar consulta simple
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Conexión exitosa!")
            print(f"📊 PostgreSQL Version: {version}")
            
            # Listar tablas
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"\n📋 Tablas encontradas ({len(tables)}):")
            for table in tables:
                print(f"   - {table}")
            
            # Verificar tabla de usuarios
            result = connection.execute(text("SELECT COUNT(*) FROM users;"))
            user_count = result.fetchone()[0]
            print(f"\n👥 Usuarios en la base de datos: {user_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Probando conexión a PostgreSQL...\n")
    success = test_database_connection()
    
    if success:
        print("\n🎉 ¡Base de datos configurada correctamente!")
        sys.exit(0)
    else:
        print("\n💥 Error en la configuración de la base de datos")
        sys.exit(1)