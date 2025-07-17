# chatbot_endpoint_fix.py
# Corrección para el endpoint de creación de chatbots
# Este código debe reemplazar la función create_chatbot en src/api/v1/endpoints/chatbots.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.database import get_db
from src.core.auth import get_current_active_user
from src.models.user import User
from src.models.chatbot import Chatbot
from src.models.organization import Organization
from src.schemas.chatbot import ChatbotCreate, ChatbotResponse

# Función corregida para crear chatbots
def create_chatbot_fixed(
    chatbot: ChatbotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Crear un nuevo chatbot con organization_id automático
    """
    try:
        # SOLUCIÓN: Obtener organization_id automáticamente
        organization_id = None
        
        # Opción 1: Usuario tiene organization_id
        if hasattr(current_user, 'organization_id') and current_user.organization_id:
            organization_id = current_user.organization_id
            print(f"✅ Usando organization_id del usuario: {organization_id}")
        else:
            # Opción 2: Buscar/crear organización
            print("🔍 Buscando organización del usuario...")
            
            user_org = db.query(Organization).filter(
                Organization.created_by_id == current_user.id
            ).first()
            
            if user_org:
                organization_id = user_org.id
                print(f"✅ Organización encontrada: {organization_id}")
            else:
                # Crear organización automática
                print("🏢 Creando organización automática...")
                new_org = Organization(
                    name=f"Organización de {current_user.full_name or current_user.email}",
                    description="Organización creada automáticamente",
                    created_by_id=current_user.id
                )
                db.add(new_org)
                db.flush()  # Para obtener el ID
                organization_id = new_org.id
                print(f"✅ Nueva organización creada: {organization_id}")
                
                # Actualizar el organization_id del usuario
                current_user.organization_id = organization_id
                db.add(current_user)
        
        # Verificar que tenemos organization_id
        if not organization_id:
            raise HTTPException(
                status_code=500,
                detail="No se pudo determinar organization_id"
            )
        
        # Crear chatbot con organization_id
        chatbot_data = chatbot.dict()
        chatbot_data['organization_id'] = organization_id
        chatbot_data['created_by_id'] = current_user.id
        
        # Generar widget_id si no existe
        if not chatbot_data.get('widget_id'):
            chatbot_data['widget_id'] = str(uuid.uuid4())
        
        print(f"📋 Datos del chatbot: {chatbot_data}")
        
        db_chatbot = Chatbot(**chatbot_data)
        db.add(db_chatbot)
        db.commit()
        db.refresh(db_chatbot)
        
        print(f"✅ Chatbot creado exitosamente: {db_chatbot.id}")
        return db_chatbot
        
    except Exception as e:
        print(f"❌ Error creando chatbot: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear chatbot: {str(e)}"
        )

# Código completo para reemplazar en chatbots.py
complete_endpoint_code = '''
@router.post("/", response_model=ChatbotResponse)
def create_chatbot(
    chatbot: ChatbotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Crear un nuevo chatbot con organization_id automático"""
    try:
        # SOLUCIÓN: Obtener organization_id automáticamente
        organization_id = None
        
        # Opción 1: Usuario tiene organization_id
        if hasattr(current_user, 'organization_id') and current_user.organization_id:
            organization_id = current_user.organization_id
        else:
            # Opción 2: Buscar/crear organización
            user_org = db.query(Organization).filter(
                Organization.created_by_id == current_user.id
            ).first()
            
            if user_org:
                organization_id = user_org.id
            else:
                # Crear organización automática
                new_org = Organization(
                    name=f"Organización de {current_user.full_name or current_user.email}",
                    description="Organización creada automáticamente",
                    created_by_id=current_user.id
                )
                db.add(new_org)
                db.flush()
                organization_id = new_org.id
                
                # Actualizar el organization_id del usuario
                current_user.organization_id = organization_id
                db.add(current_user)
        
        # Crear chatbot con organization_id
        chatbot_data = chatbot.dict()
        chatbot_data['organization_id'] = organization_id
        chatbot_data['created_by_id'] = current_user.id
        
        # Generar widget_id si no existe
        if not chatbot_data.get('widget_id'):
            import uuid
            chatbot_data['widget_id'] = str(uuid.uuid4())
        
        db_chatbot = Chatbot(**chatbot_data)
        db.add(db_chatbot)
        db.commit()
        db.refresh(db_chatbot)
        
        return db_chatbot
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear chatbot: {str(e)}"
        )
'''

print("📄 CÓDIGO PARA REEMPLAZAR EN chatbots.py:")
print("=" * 50)
print(complete_endpoint_code)
print("=" * 50)
print("\n✅ Archivo chatbot_endpoint_fix.py creado")
print("📋 Instrucciones:")
print("1. Copiar el código de arriba")
print("2. Reemplazar la función create_chatbot en src/api/v1/endpoints/chatbots.py")
print("3. Asegurar que los imports estén incluidos")
print("4. Reiniciar el servidor")