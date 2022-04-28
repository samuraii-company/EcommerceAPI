from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ecommerce.db import Base

from . import hashing

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    cart = relationship("Cart", back_populates="user_cart")
    order = relationship("Order", back_populates="user_info")
    
    def __init__(self, name: str, email: str, password: str, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = hashing.get_password_hash(password)
        
    def check_password(self, password: str):
        return hashing.verify_password(self.password, password)