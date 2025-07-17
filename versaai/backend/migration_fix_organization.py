# migration_fix_organization.py
# Script para corregir el problema de organization_id null constraint

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.core.database import engine, SessionLocal
from src.core.config import settings
from datetime import datetime

def run_migration():
    """
    Migración para agregar organization_id a users y crear organizaciones por defecto
    """
    try:
        # Usar la configuración existente de la base de datos
        db = SessionLocal()
        
        print(f"🔗 Conectando a la base de datos: {settings.DATABASE_URL[:20]}...")
        
        print("🔧 Iniciando migración para organization_id...")
        
        # 1. Verificar si la columna organization_id existe en users
        result = db.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='organization_id';
        """))
        
        if not result.fetchone():
            print("🔧 Agregando columna organization_id a tabla users...")
            db.execute(text("""
                ALTER TABLE users
                ADD COLUMN organization_id INTEGER
                REFERENCES organizations(id);
            """))
            print("✅ Columna organization_id agregada exitosamente")
        else:
            print("✅ Columna organization_id ya existe")
        
        # 2. Crear organizaciones por defecto para usuarios sin organización
        print("🏢 Creando organizaciones por defecto...")
        
        # 2. Buscar usuarios que no tienen organization_id
        users_without_org = db.execute(text("""
            SELECT id, email, full_name
            FROM users
            WHERE organization_id IS NULL;
        """)).fetchall()
        
        print(f"📊 Encontrados {len(users_without_org)} usuarios sin organización")
        
        # Contadores
        created_orgs = 0
        updated_users = 0
        
        for user in users_without_org:
            user_id, email, full_name = user
            org_name = f"Organización de {full_name or email}"
            
            # Crear organización
            db.execute(text("""
                INSERT INTO organizations (name, slug, description, created_at, updated_at)
                VALUES (:name, :slug, :description, :created_at, :updated_at)
            """), {
                'name': org_name,
                'slug': f'org-{user_id}-{int(datetime.utcnow().timestamp())}',
                'description': 'Organización creada automáticamente',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            })
            
            created_orgs += 1
            print(f"✅ Organización creada para usuario {email}")
        
        # 4. Asignar organization_id a usuarios
        print("👥 Asignando organization_id a usuarios...")
        
        # Obtener las organizaciones recién creadas y asignarlas
        for user in users_without_org:
            user_id = user.id
            # Buscar la organización creada para este usuario
            org_result = db.execute(text("""
                SELECT id FROM organizations 
                WHERE slug LIKE :pattern
                ORDER BY created_at DESC
                LIMIT 1;
            """), {'pattern': f'org-{user_id}-%'}).fetchone()
            
            if org_result:
                # Asignar la organización al usuario
                db.execute(text("""
                    UPDATE users 
                    SET organization_id = :org_id 
                    WHERE id = :user_id;
                """), {
                    'org_id': org_result.id,
                    'user_id': user_id
                })
                updated_users += 1
        
        # 5. Verificar resultados
        print("🔍 Verificando resultados...")
        
        users_without_org_count = db.execute(text("""
            SELECT COUNT(*) as count
            FROM users
            WHERE organization_id IS NULL;
        """)).fetchone().count
        
        total_orgs = db.execute(text("""
            SELECT COUNT(*) as count
            FROM organizations;
        """)).fetchone().count
        
        db.commit()
        
        print("\n📊 RESULTADOS DE LA MIGRACIÓN:")
        print(f"✅ Organizaciones creadas: {created_orgs}")
        print(f"✅ Usuarios actualizados: {updated_users}")
        print(f"✅ Usuarios sin organization_id: {users_without_org_count}")
        print(f"✅ Total de organizaciones: {total_orgs}")
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        if 'db' in locals():
            db.rollback()
        raise
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    run_migration()