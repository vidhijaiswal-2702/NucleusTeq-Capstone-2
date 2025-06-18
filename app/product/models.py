from sqlalchemy import Column, Integer, String, Float,ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(50),nullable = False)
    image_url = Column(String(255),nullable = False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) # users id -> as foreign key in product to restrict acess to creator only

    cart_entries = relationship("Cart", back_populates="product", cascade="all, delete-orphan") #one to many-> 1 product = many cart entries
    order_items = relationship("OrderItem", back_populates="product")# 1 product -> in many order items(orders will be diff.)
    creator = relationship("User", back_populates="products")# many to one -> many products created by one particular user.
    
    