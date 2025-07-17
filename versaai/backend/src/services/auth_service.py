from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.user import User
from ..models.organization import Organization
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise
    
    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            # Refresh tokens last longer (7 days)
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating refresh token: {e}")
            raise
    
    def verify_refresh_token(self, token: str) -> Optional[dict]:
        """Verify refresh token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "refresh":
                return None
            return payload
        except JWTError:
            return None
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.debug(f"Token payload: {payload}")
            return payload
        except JWTError as e:
            logger.warning(f"JWT verification failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user with email and password"""
        try:
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                logger.warning(f"Authentication failed: User not found for email {email}")
                return None
            
            if not user.is_active:
                logger.warning(f"Authentication failed: User {email} is inactive")
                return None
            
            if not self.verify_password(password, user.hashed_password):
                logger.warning(f"Authentication failed: Invalid password for user {email}")
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            logger.info(f"User {email} authenticated successfully")
            return user
            
        except Exception as e:
            logger.error(f"Error during authentication: {e}")
            db.rollback()
            return None
    
    def get_current_user(self, db: Session, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        payload = self.verify_token(token)
        
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        try:
            user = db.query(User).filter(User.id == int(user_id)).first()
            
            if not user or not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            return None
    
    def create_user_token(self, user: User) -> str:
        """Create access token for a user"""
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "org_id": user.organization_id
        }
        
        return self.create_access_token(token_data)
    
    def register_user(
        self, 
        db: Session, 
        email: str, 
        password: str, 
        username: str, 
        full_name: str,
        organization_id: Optional[int] = None
    ) -> Optional[User]:
        """Register a new user with automatic organization creation"""
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            
            if existing_user:
                logger.warning(f"Registration failed: User with email {email} or username {username} already exists")
                return None
            
            # If no organization_id provided, create a new organization
            if organization_id is None:
                # Extract company name from email domain or use full_name
                email_domain = email.split('@')[1] if '@' in email else 'unknown'
                org_name = f"{full_name}'s Organization"
                
                # Generate unique slug from name
                import re
                base_slug = re.sub(r'[^a-zA-Z0-9\s]', '', org_name.lower())
                base_slug = re.sub(r'\s+', '-', base_slug.strip())
                
                # Ensure slug is unique
                slug = base_slug
                counter = 1
                while db.query(Organization).filter(Organization.slug == slug).first():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                # Create new organization
                organization = Organization(
                    name=org_name,
                    slug=slug,
                    description=f"Organization for {full_name}",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(organization)
                db.flush()  # Get the ID without committing
                organization_id = organization.id
                
                logger.info(f"Created new organization '{org_name}' with slug '{slug}' and ID {organization_id} for user {email}")
            
            # Hash password
            hashed_password = self.get_password_hash(password)
            
            # Create user with explicit timestamps
            current_time = datetime.utcnow()
            user = User(
                email=email,
                username=username,
                full_name=full_name,
                hashed_password=hashed_password,
                organization_id=organization_id,
                created_at=current_time,
                updated_at=current_time
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"User {email} registered successfully with organization_id {organization_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error during user registration: {e}")
            db.rollback()
            return None
    
    def change_password(self, db: Session, user: User, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Verify old password
            if not self.verify_password(old_password, user.hashed_password):
                logger.warning(f"Password change failed: Invalid old password for user {user.email}")
                return False
            
            # Hash new password
            user.hashed_password = self.get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"Password changed successfully for user {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            db.rollback()
            return False
    
    def reset_password(self, db: Session, email: str, new_password: str) -> bool:
        """Reset user password (admin function)"""
        try:
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                logger.warning(f"Password reset failed: User not found for email {email}")
                return False
            
            # Hash new password
            user.hashed_password = self.get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"Password reset successfully for user {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            db.rollback()
            return False

# Global instance
auth_service = AuthService()