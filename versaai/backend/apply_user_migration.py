#!/usr/bin/env python3
"""
Script para aplicar migración manual de campos preferences y login_count al modelo User
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.config import settings
from core.database import get_db

def apply_migration():
    """Aplica la migración para agregar preferences y login_count"""
    try:
        # Crear engine directamente
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            # Verificar si las columnas ya existen
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                AND column_name IN ('preferences', 'login_count')
            """))
            
            existing_columns = [row[0] for row in result.fetchall()]
            
            # Agregar columna preferences si no existe
            if 'preferences' not in existing_columns:
                print("Agregando columna 'preferences'...")
                connection.execute(text("ALTER TABLE users ADD COLUMN preferences JSON DEFAULT '{}'"))
                connection.commit()
                print("✅ Columna 'preferences' agregada")
            else:
                print("ℹ️ Columna 'preferences' ya existe")
            
            # Agregar columna login_count si no existe
            if 'login_count' not in existing_columns:
                print("Agregando columna 'login_count'...")
                connection.execute(text("ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0"))
                connection.commit()
                print("✅ Columna 'login_count' agregada")
            else:
                print("ℹ️ Columna 'login_count' ya existe")
            
            # Actualizar valores por defecto para registros existentes
            print("Actualizando valores por defecto...")
            connection.execute(text("UPDATE users SET preferences = '{}' WHERE preferences IS NULL"))
            connection.execute(text("UPDATE users SET login_count = 0 WHERE login_count IS NULL"))
            connection.commit()
            
            print("✅ Migración aplicada exitosamente")
            
    except Exception as e:
        print(f"❌ Error aplicando migración: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔄 Aplicando migración de User...")
    success = apply_migration()
    if success:
        print("🎉 Migración completada")
    else:
        print("💥 Migración falló")
        sys.exit(1)