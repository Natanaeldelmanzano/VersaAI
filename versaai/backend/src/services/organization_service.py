from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ..models.organization import Organization
from ..models.user import User
from ..schemas.organization import OrganizationCreate, OrganizationUpdate
from .cache import cache_manager

logger = logging.getLogger(__name__)

class OrganizationService:
    """Servicio para gestión de organizaciones"""
    
    def __init__(self):
        self.cache_prefix = "org:"
        self.cache_ttl = 3600  # 1 hora
    
    async def create_organization(
        self, 
        db: Session, 
        org_data: OrganizationCreate,
        created_by: Optional[int] = None
    ) -> Organization:
        """Crea una nueva organización"""
        try:
            # Verificar si el nombre ya existe
            existing_org = db.query(Organization).filter(
                Organization.name == org_data.name
            ).first()
            if existing_org:
                raise ValueError("El nombre de la organización ya existe")
            
            # Verificar si el slug ya existe (si se proporciona)
            if org_data.slug:
                existing_slug = db.query(Organization).filter(
                    Organization.slug == org_data.slug
                ).first()
                if existing_slug:
                    raise ValueError("El slug de la organización ya existe")
            else:
                # Generar slug automáticamente
                org_data.slug = self._generate_slug(org_data.name)
            
            # Crear organización
            db_org = Organization(
                name=org_data.name,
                slug=org_data.slug,
                description=org_data.description,
                website=org_data.website,
                logo_url=org_data.logo_url,
                industry=org_data.industry,
                size=org_data.size,
                country=org_data.country,
                timezone=org_data.timezone or "UTC",
                language=org_data.language or "es",
                is_active=org_data.is_active if org_data.is_active is not None else True,
                settings=org_data.settings or {},
                created_by=created_by
            )
            
            db.add(db_org)
            db.commit()
            db.refresh(db_org)
            
            # Limpiar caché relacionado
            await self._invalidate_organization_cache(db_org.id)
            
            logger.info(f"Organización creada: {db_org.name} (ID: {db_org.id})")
            return db_org
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creando organización: {str(e)}")
            raise
    
    async def get_organization(self, db: Session, org_id: int) -> Optional[Organization]:
        """Obtiene una organización por ID"""
        try:
            # Intentar obtener del caché
            cache_key = f"{self.cache_prefix}{org_id}"
            cached_org = await cache_manager.get(cache_key)
            
            if cached_org:
                logger.debug(f"Organización obtenida del caché: {org_id}")
                return self._dict_to_organization(cached_org)
            
            # Obtener de la base de datos
            organization = db.query(Organization).filter(
                Organization.id == org_id
            ).first()
            
            if organization:
                # Guardar en caché
                org_dict = self._organization_to_dict(organization)
                await cache_manager.set(cache_key, org_dict, self.cache_ttl)
                logger.debug(f"Organización obtenida de DB y guardada en caché: {org_id}")
            
            return organization
            
        except Exception as e:
            logger.error(f"Error obteniendo organización {org_id}: {str(e)}")
            return None
    
    async def get_organization_by_slug(self, db: Session, slug: str) -> Optional[Organization]:
        """Obtiene una organización por slug"""
        try:
            # Intentar obtener del caché
            cache_key = f"{self.cache_prefix}slug:{slug}"
            cached_org = await cache_manager.get(cache_key)
            
            if cached_org:
                logger.debug(f"Organización obtenida del caché por slug: {slug}")
                return self._dict_to_organization(cached_org)
            
            # Obtener de la base de datos
            organization = db.query(Organization).filter(
                Organization.slug == slug
            ).first()
            
            if organization:
                # Guardar en caché
                org_dict = self._organization_to_dict(organization)
                await cache_manager.set(cache_key, org_dict, self.cache_ttl)
                # También guardar por ID
                await cache_manager.set(
                    f"{self.cache_prefix}{organization.id}", 
                    org_dict, 
                    self.cache_ttl
                )
                logger.debug(f"Organización obtenida de DB por slug y guardada en caché: {slug}")
            
            return organization
            
        except Exception as e:
            logger.error(f"Error obteniendo organización por slug {slug}: {str(e)}")
            return None
    
    async def update_organization(
        self, 
        db: Session, 
        org_id: int, 
        org_data: OrganizationUpdate,
        updated_by: Optional[int] = None
    ) -> Optional[Organization]:
        """Actualiza una organización"""
        try:
            organization = db.query(Organization).filter(
                Organization.id == org_id
            ).first()
            if not organization:
                return None
            
            # Verificar nombre único si se está actualizando
            if org_data.name and org_data.name != organization.name:
                existing_org = db.query(Organization).filter(
                    and_(
                        Organization.name == org_data.name,
                        Organization.id != org_id
                    )
                ).first()
                if existing_org:
                    raise ValueError("El nombre de la organización ya existe")
            
            # Verificar slug único si se está actualizando
            if org_data.slug and org_data.slug != organization.slug:
                existing_slug = db.query(Organization).filter(
                    and_(
                        Organization.slug == org_data.slug,
                        Organization.id != org_id
                    )
                ).first()
                if existing_slug:
                    raise ValueError("El slug de la organización ya existe")
            
            # Actualizar campos
            update_data = org_data.dict(exclude_unset=True)
            
            # Agregar metadatos de actualización
            update_data["updated_at"] = datetime.utcnow()
            if updated_by:
                update_data["updated_by"] = updated_by
            
            # Aplicar actualizaciones
            for field, value in update_data.items():
                if field == "settings" and value:
                    # Merge settings instead of replacing
                    current_settings = organization.settings or {}
                    current_settings.update(value)
                    setattr(organization, field, current_settings)
                else:
                    setattr(organization, field, value)
            
            db.commit()
            db.refresh(organization)
            
            # Limpiar caché
            await self._invalidate_organization_cache(org_id)
            
            logger.info(f"Organización actualizada: {organization.name} (ID: {organization.id})")
            return organization
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando organización {org_id}: {str(e)}")
            raise
    
    async def delete_organization(self, db: Session, org_id: int) -> bool:
        """Elimina una organización (soft delete)"""
        try:
            organization = db.query(Organization).filter(
                Organization.id == org_id
            ).first()
            if not organization:
                return False
            
            # Verificar si tiene usuarios asociados
            user_count = db.query(User).filter(
                User.organization_id == org_id
            ).count()
            
            if user_count > 0:
                raise ValueError(
                    f"No se puede eliminar la organización. "
                    f"Tiene {user_count} usuarios asociados."
                )
            
            # Soft delete
            organization.is_active = False
            organization.deleted_at = datetime.utcnow()
            
            db.commit()
            
            # Limpiar caché
            await self._invalidate_organization_cache(org_id)
            
            logger.info(f"Organización eliminada (soft): {organization.name} (ID: {organization.id})")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error eliminando organización {org_id}: {str(e)}")
            raise
    
    async def get_organizations(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        country: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: str = "created_at",
        order_desc: bool = True
    ) -> Dict[str, Any]:
        """Obtiene lista de organizaciones con filtros y paginación"""
        try:
            # Construir query base
            query = db.query(Organization)
            
            # Aplicar filtros
            if search:
                search_filter = or_(
                    Organization.name.ilike(f"%{search}%"),
                    Organization.description.ilike(f"%{search}%"),
                    Organization.slug.ilike(f"%{search}%")
                )
                query = query.filter(search_filter)
            
            if industry:
                query = query.filter(Organization.industry == industry)
            
            if size:
                query = query.filter(Organization.size == size)
            
            if country:
                query = query.filter(Organization.country == country)
            
            if is_active is not None:
                query = query.filter(Organization.is_active == is_active)
            
            # Contar total
            total = query.count()
            
            # Aplicar ordenamiento
            if hasattr(Organization, order_by):
                order_column = getattr(Organization, order_by)
                if order_desc:
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column)
            
            # Aplicar paginación
            organizations = query.offset(skip).limit(limit).all()
            
            return {
                "organizations": organizations,
                "total": total,
                "skip": skip,
                "limit": limit,
                "has_next": (skip + limit) < total,
                "has_prev": skip > 0
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo organizaciones: {str(e)}")
            raise
    
    async def get_organization_users(
        self,
        db: Session,
        org_id: int,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Obtiene los usuarios de una organización"""
        try:
            # Verificar que la organización existe
            organization = await self.get_organization(db, org_id)
            if not organization:
                raise ValueError("Organización no encontrada")
            
            # Construir query
            query = db.query(User).filter(User.organization_id == org_id)
            
            # Aplicar filtros
            if role:
                query = query.filter(User.role == role)
            
            if is_active is not None:
                query = query.filter(User.is_active == is_active)
            
            # Contar total
            total = query.count()
            
            # Aplicar paginación
            users = query.offset(skip).limit(limit).all()
            
            return {
                "users": users,
                "total": total,
                "skip": skip,
                "limit": limit,
                "organization": organization
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo usuarios de organización {org_id}: {str(e)}")
            raise
    
    async def get_organization_stats(self, db: Session, org_id: int) -> Dict[str, Any]:
        """Obtiene estadísticas de una organización"""
        try:
            organization = await self.get_organization(db, org_id)
            if not organization:
                return {}
            
            # Contar usuarios
            total_users = db.query(User).filter(
                User.organization_id == org_id
            ).count()
            
            active_users = db.query(User).filter(
                and_(
                    User.organization_id == org_id,
                    User.is_active == True
                )
            ).count()
            
            # Contar usuarios por rol
            users_by_role = db.query(
                User.role,
                func.count(User.id).label('count')
            ).filter(
                User.organization_id == org_id
            ).group_by(User.role).all()
            
            role_stats = {role: count for role, count in users_by_role}
            
            # Estadísticas básicas
            stats = {
                "organization_id": organization.id,
                "name": organization.name,
                "slug": organization.slug,
                "is_active": organization.is_active,
                "created_at": organization.created_at,
                "users": {
                    "total": total_users,
                    "active": active_users,
                    "inactive": total_users - active_users,
                    "by_role": role_stats
                }
            }
            
            # Agregar estadísticas adicionales si es necesario
            # Por ejemplo: número de chatbots, conversaciones, etc.
            
            return stats
            
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas para organización {org_id}: {str(e)}")
            return {}
    
    async def update_organization_settings(
        self,
        db: Session,
        org_id: int,
        settings: Dict[str, Any],
        updated_by: Optional[int] = None
    ) -> Optional[Organization]:
        """Actualiza la configuración de una organización"""
        try:
            organization = db.query(Organization).filter(
                Organization.id == org_id
            ).first()
            if not organization:
                return None
            
            # Merge settings
            current_settings = organization.settings or {}
            current_settings.update(settings)
            
            organization.settings = current_settings
            organization.updated_at = datetime.utcnow()
            if updated_by:
                organization.updated_by = updated_by
            
            db.commit()
            db.refresh(organization)
            
            # Limpiar caché
            await self._invalidate_organization_cache(org_id)
            
            logger.info(f"Configuración actualizada para organización: {organization.name}")
            return organization
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando configuración de organización {org_id}: {str(e)}")
            raise
    
    def _generate_slug(self, name: str) -> str:
        """Genera un slug a partir del nombre"""
        import re
        import unicodedata
        
        # Normalizar unicode
        slug = unicodedata.normalize('NFKD', name)
        slug = slug.encode('ascii', 'ignore').decode('ascii')
        
        # Convertir a minúsculas y reemplazar espacios
        slug = re.sub(r'[^\w\s-]', '', slug.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remover guiones al inicio y final
        slug = slug.strip('-')
        
        return slug[:50]  # Limitar longitud
    
    def _organization_to_dict(self, org: Organization) -> Dict[str, Any]:
        """Convierte un objeto Organization a diccionario para caché"""
        return {
            "id": org.id,
            "name": org.name,
            "slug": org.slug,
            "description": org.description,
            "website": org.website,
            "logo_url": org.logo_url,
            "industry": org.industry,
            "size": org.size,
            "country": org.country,
            "timezone": org.timezone,
            "language": org.language,
            "is_active": org.is_active,
            "settings": org.settings,
            "created_at": org.created_at.isoformat() if org.created_at else None,
            "updated_at": org.updated_at.isoformat() if org.updated_at else None,
            "deleted_at": org.deleted_at.isoformat() if org.deleted_at else None,
            "created_by": org.created_by,
            "updated_by": org.updated_by
        }
    
    def _dict_to_organization(self, org_dict: Dict[str, Any]) -> Organization:
        """Convierte un diccionario de caché a objeto Organization"""
        org = Organization()
        
        for key, value in org_dict.items():
            if key in ["created_at", "updated_at", "deleted_at"]:
                if value:
                    setattr(org, key, datetime.fromisoformat(value))
                else:
                    setattr(org, key, None)
            else:
                setattr(org, key, value)
        
        return org
    
    async def _invalidate_organization_cache(self, org_id: int):
        """Invalida el caché relacionado con una organización"""
        try:
            # Limpiar cachés relacionados
            cache_keys = [
                f"{self.cache_prefix}{org_id}",
                f"{self.cache_prefix}slug:*"
            ]
            
            for key in cache_keys:
                await cache_manager.delete(key)
            
            logger.debug(f"Caché invalidado para organización: {org_id}")
            
        except Exception as e:
            logger.error(f"Error invalidando caché para organización {org_id}: {str(e)}")

# Instancia global del servicio
organization_service = OrganizationService()