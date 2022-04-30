from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float, Text
from sqlalchemy.orm import relationship
from ecommerce.db import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, default=datetime.now)
    order_amount = Column(Float, default=0.0)
    order_status = Column(String, default="PROCESSING")
    shipping_address = Column(Text)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    order_detail = relationship("OrderDetail", back_populates="order")
    user_info = relationship("User", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "order_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    order = relationship("Order", back_populates="order_detail")
    product_order_detail = relationship("Product", back_populates="order_detail")
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    quantity = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.now)
