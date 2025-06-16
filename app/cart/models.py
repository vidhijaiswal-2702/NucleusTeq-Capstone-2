from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
class Cart(Base):
    __tablename__ =  'cart'
    
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    product_id= Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='_user_product_uc'),)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product",back_populates="cart_entries")