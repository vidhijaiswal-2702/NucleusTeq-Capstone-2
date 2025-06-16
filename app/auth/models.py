from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, func, ForeignKey
from app.core.database import Base
from app.auth.roles import UserRole
from sqlalchemy.orm import mapped_column, relationship
from app.orders.models import Order
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(50), default=UserRole.user.value, nullable=False)
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    tokens = relationship("UserToken", back_populates="user")
    reset_tokens = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")
    cart_items = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="creator", cascade="all, delete-orphan")


    
    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()
    
    

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    user = relationship("User", back_populates="reset_tokens")
    
class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="tokens")
    

