from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from passlib.context import CryptContext
from jose import JWTError, jwt
from email_validator import validate_email, EmailNotValidError

from ..models.user import User
from ..models.organization import Organization
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..core.config import settings
from ..core.security import verify_password, get_password_hash
from .cache import cache_manager

logger = logging.getLogger(__name__)

class UserService:
    """Servicio para gestión de usuarios"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.cache_prefix = "user:"
        self.cache_ttl = 3600  # 1 hora
    
    async def create_user(
        self, 
        db: Session, 
        user_data: UserCreate,
        created_by: Optional[int] = None
    ) -> User:
        """Crea un nuevo usuario"""
        try:
            # Validar email
            try:
                valid_email = validate_email(user_data.email)
                user_data.email = valid_email.email
            except EmailNotValidError as e:
                raise ValueError(f"Email inválido: {str(e)}")
            
            # Verificar si el email ya existe
            existing_user = db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                raise ValueError("El email ya está registrado")
            
            # Verificar si el username ya existe (si se proporciona)
            if user_data.username:
                existing_username = db.query(User).filter(User.username == user_data.username).first()
                if existing_username:
                    raise ValueError("El nombre de usuario ya está en uso")
            
            # Crear hash de la contraseña
            hashed_password = get_password_hash(user_data.password)
            
            # Crear usuario
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                is_active=user_data.is_active if user_data.is_active is not None else True,
                is_superuser=user_data.is_superuser if user_data.is_superuser is not None else False,
                organization_id=user_data.organization_id,
                role=user_data.role or "user",
                phone=user_data.phone,
                avatar_url=user_data.avatar_url,
                timezone=user_data.timezone or "UTC",
                language=user_data.language or "es",
                created_by=created_by
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            # Limpiar caché relacionado
            await self._invalidate_user_cache(db_user.id)
            
            logger.info(f"Usuario creado: {db_user.email} (ID: {db_user.id})")
            return db_user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creando usuario: {str(e)}")
            raise
    
    async def get_user(self, db: Session, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID"""
        try:
            # Intentar obtener del caché
            cache_key = f"{self.cache_prefix}{user_id}"
            cached_user = await cache_manager.get(cache_key)
            
            if cached_user:
                logger.debug(f"Usuario obtenido del caché: {user_id}")
                return self._dict_to_user(cached_user)
            
            # Obtener de la base de datos
            user = db.query(User).filter(User.id == user_id).first()
            
            if user:
                # Guardar en caché
                user_dict = self._user_to_dict(user)
                await cache_manager.set(cache_key, user_dict, self.cache_ttl)
                logger.debug(f"Usuario obtenido de DB y guardado en caché: {user_id}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario {user_id}: {str(e)}")
            return None
    
    async def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        try:
            # Intentar obtener del caché
            cache_key = f"{self.cache_prefix}email:{email}"
            cached_user = await cache_manager.get(cache_key)
            
            if cached_user:
                logger.debug(f"Usuario obtenido del caché por email: {email}")
                return self._dict_to_user(cached_user)
            
            # Obtener de la base de datos
            user = db.query(User).filter(User.email == email).first()
            
            if user:
                # Guardar en caché
                user_dict = self._user_to_dict(user)
                await cache_manager.set(cache_key, user_dict, self.cache_ttl)
                # También guardar por ID
                await cache_manager.set(f"{self.cache_prefix}{user.id}", user_dict, self.cache_ttl)
                logger.debug(f"Usuario obtenido de DB por email y guardado en caché: {email}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario por email {email}: {str(e)}")
            return None
    
    async def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Obtiene un usuario por username"""
        try:
            # Intentar obtener del caché
            cache_key = f"{self.cache_prefix}username:{username}"
            cached_user = await cache_manager.get(cache_key)
            
            if cached_user:
                logger.debug(f"Usuario obtenido del caché por username: {username}")
                return self._dict_to_user(cached_user)
            
            # Obtener de la base de datos
            user = db.query(User).filter(User.username == username).first()
            
            if user:
                # Guardar en caché
                user_dict = self._user_to_dict(user)
                await cache_manager.set(cache_key, user_dict, self.cache_ttl)
                # También guardar por ID
                await cache_manager.set(f"{self.cache_prefix}{user.id}", user_dict, self.cache_ttl)
                logger.debug(f"Usuario obtenido de DB por username y guardado en caché: {username}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario por username {username}: {str(e)}")
            return None
    
    async def update_user(
        self, 
        db: Session, 
        user_id: int, 
        user_data: UserUpdate,
        updated_by: Optional[int] = None
    ) -> Optional[User]:
        """Actualiza un usuario"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            # Validar email si se está actualizando
            if user_data.email and user_data.email != user.email:
                try:
                    valid_email = validate_email(user_data.email)
                    user_data.email = valid_email.email
                except EmailNotValidError as e:
                    raise ValueError(f"Email inválido: {str(e)}")
                
                # Verificar si el nuevo email ya existe
                existing_user = db.query(User).filter(
                    and_(User.email == user_data.email, User.id != user_id)
                ).first()
                if existing_user:
                    raise ValueError("El email ya está registrado")
            
            # Validar username si se está actualizando
            if user_data.username and user_data.username != user.username:
                existing_username = db.query(User).filter(
                    and_(User.username == user_data.username, User.id != user_id)
                ).first()
                if existing_username:
                    raise ValueError("El nombre de usuario ya está en uso")
            
            # Actualizar campos
            update_data = user_data.dict(exclude_unset=True)
            
            # Manejar contraseña si se proporciona
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            
            # Agregar metadatos de actualización
            update_data["updated_at"] = datetime.utcnow()
            if updated_by:
                update_data["updated_by"] = updated_by
            
            # Aplicar actualizaciones
            for field, value in update_data.items():
                setattr(user, field, value)
            
            db.commit()
            db.refresh(user)
            
            # Limpiar caché
            await self._invalidate_user_cache(user_id)
            
            logger.info(f"Usuario actualizado: {user.email} (ID: {user.id})")
            return user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando usuario {user_id}: {str(e)}")
            raise
    
    async def delete_user(self, db: Session, user_id: int) -> bool:
        """Elimina un usuario (soft delete)"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            # Soft delete
            user.is_active = False
            user.deleted_at = datetime.utcnow()
            
            db.commit()
            
            # Limpiar caché
            await self._invalidate_user_cache(user_id)
            
            logger.info(f"Usuario eliminado (soft): {user.email} (ID: {user.id})")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error eliminando usuario {user_id}: {str(e)}")
            return False
    
    async def get_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        organization_id: Optional[int] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> Dict[str, Any]:
        """Obtiene lista de usuarios con filtros y paginación"""
        try:
            # Construir query base
            query = db.query(User)
            
            # Aplicar filtros
            if search:
                search_filter = or_(
                    User.email.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%")
                )
                query = query.filter(search_filter)
            
            if organization_id is not None:
                query = query.filter(User.organization_id == organization_id)
            
            if role:
                query = query.filter(User.role == role)
            
            if is_active is not None:
                query = query.filter(User.is_active == is_active)
            
            # Contar total
            total = query.count()
            
            # Aplicar ordenamiento
            if hasattr(User, order_by):
                order_column = getattr(User, order_by)
                if order_desc:
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column)
            
            # Aplicar paginación
            users = query.offset(skip).limit(limit).all()
            
            return {
                "users": users,
                "total": total,
                "skip": skip,
                "limit": limit,
                "has_next": (skip + limit) < total,
                "has_prev": skip > 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo usuarios: {str(e)}")
            raise
    
    async def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Autentica un usuario"""
        try:
            user = await self.get_user_by_email(db, email)
            if not user:
                return None
            
            if not verify_password(password, user.hashed_password):
                return None
            
            if not user.is_active:
                return None
            
            # Actualizar último login
            user.last_login = datetime.utcnow()
            db.commit()
            
            # Actualizar caché
            await self._invalidate_user_cache(user.id)
            
            logger.info(f"Usuario autenticado: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Error autenticando usuario {email}: {str(e)}")
            return None
    
    async def change_password(
        self, 
        db: Session, 
        user_id: int, 
        current_password: str, 
        new_password: str
    ) -> bool:
        """Cambia la contraseña de un usuario"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            # Verificar contraseña actual
            if not verify_password(current_password, user.hashed_password):
                return False
            
            # Actualizar contraseña
            user.hashed_password = get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            db.commit()
            
            # Limpiar caché
            await self._invalidate_user_cache(user_id)
            
            logger.info(f"Contraseña cambiada para usuario: {user.email}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error cambiando contraseña para usuario {user_id}: {str(e)}")
            return False
    
    async def reset_password(self, db: Session, email: str) -> Optional[str]:
        """Inicia el proceso de reset de contraseña"""
        try:
            user = await self.get_user_by_email(db, email)
            if not user or not user.is_active:
                return None
            
            # Generar token de reset
            reset_token = self._generate_reset_token(user.id)
            
            # Guardar token en caché con expiración
            cache_key = f"password_reset:{user.id}"
            await cache_manager.set(cache_key, reset_token, 3600)  # 1 hora
            
            logger.info(f"Token de reset generado para usuario: {user.email}")
            return reset_token
            
        except Exception as e:
            logger.error(f"Error generando reset de contraseña para {email}: {str(e)}")
            return None
    
    async def confirm_password_reset(
        self, 
        db: Session, 
        token: str, 
        new_password: str
    ) -> bool:
        """Confirma el reset de contraseña"""
        try:
            # Verificar token
            user_id = self._verify_reset_token(token)
            if not user_id:
                return False
            
            # Verificar que el token esté en caché
            cache_key = f"password_reset:{user_id}"
            cached_token = await cache_manager.get(cache_key)
            if not cached_token or cached_token != token:
                return False
            
            # Obtener usuario
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                return False
            
            # Actualizar contraseña
            user.hashed_password = get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            db.commit()
            
            # Limpiar token de reset
            await cache_manager.delete(cache_key)
            
            # Limpiar caché de usuario
            await self._invalidate_user_cache(user_id)
            
            logger.info(f"Contraseña reseteada para usuario: {user.email}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error confirmando reset de contraseña: {str(e)}")
            return False
    
    async def update_last_activity(self, db: Session, user_id: int) -> bool:
        """Actualiza la última actividad del usuario"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            user.last_activity = datetime.utcnow()
            db.commit()
            
            # Actualizar caché
            await self._invalidate_user_cache(user_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando última actividad para usuario {user_id}: {str(e)}")
            return False
    
    async def get_user_stats(self, db: Session, user_id: int) -> Dict[str, Any]:
        """Obtiene estadísticas del usuario"""
        try:
            user = await self.get_user(db, user_id)
            if not user:
                return {}
            
            # Calcular estadísticas básicas
            stats = {
                "user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "last_login": user.last_login,
                "last_activity": user.last_activity,
                "organization_id": user.organization_id
            }
            
            # Agregar estadísticas adicionales si es necesario
            # Por ejemplo: número de chatbots creados, conversaciones, etc.
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas para usuario {user_id}: {str(e)}")
            return {}
    
    def _generate_reset_token(self, user_id: int) -> str:
        """Genera un token de reset de contraseña"""
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(hours=1),
                "type": "password_reset"
            }
            
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            return token
            
        except Exception as e:
            logger.error(f"Error generando token de reset: {str(e)}")
            return ""
    
    def _verify_reset_token(self, token: str) -> Optional[int]:
        """Verifica un token de reset de contraseña"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            if payload.get("type") != "password_reset":
                return None
            
            return payload.get("user_id")
            
        except JWTError:
            return None
    
    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convierte un objeto User a diccionario para caché"""
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "organization_id": user.organization_id,
            "role": user.role,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "timezone": user.timezone,
            "language": user.language,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "last_activity": user.last_activity.isoformat() if user.last_activity else None,
            "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
            "created_by": user.created_by,
            "updated_by": user.updated_by
        }
    
    def _dict_to_user(self, user_dict: Dict[str, Any]) -> User:
        """Convierte un diccionario de caché a objeto User"""
        user = User()
        
        for key, value in user_dict.items():
            if key in ["created_at", "updated_at", "last_login", "last_activity", "deleted_at"]:
                if value:
                    setattr(user, key, datetime.fromisoformat(value))
                else:
                    setattr(user, key, None)
            else:
                setattr(user, key, value)
        
        return user
    
    async def _invalidate_user_cache(self, user_id: int):
        """Invalida el caché relacionado con un usuario"""
        try:
            # Obtener usuario para limpiar todos los cachés relacionados
            cache_keys = [
                f"{self.cache_prefix}{user_id}",
                f"{self.cache_prefix}email:*",
                f"{self.cache_prefix}username:*"
            ]
            
            for key in cache_keys:
                await cache_manager.delete(key)
            
            logger.debug(f"Caché invalidado para usuario: {user_id}")
            
        except Exception as e:
            logger.error(f"Error invalidando caché para usuario {user_id}: {str(e)}")

# Instancia global del servicio
user_service = UserService()