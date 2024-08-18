from sqlalchemy import Integer, Text, Boolean, ForeignKey, String, Column, Table
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship
from database import engine, session, Base

# Many-to-Many bog'lanishni ifodalash uchun yordamchi jadval
order_product = Table('order_product', Base.metadata,
                      Column('order_id', Integer, ForeignKey('order.id'), primary_key=True),
                      Column('product_id', Integer, ForeignKey('product.id'), primary_key=True))

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    password = Column(Text, nullable=True)
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return self.username


class Order(Base):
    ORDER_STATUS = (
        ("PENDING", "PENDING"),
        ("IN_TRANSIT", "IN_TRANSIT"),
        ("DELIVERED", "DELIVERED"),
    )
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_product, back_populates="orders")

    def __repr__(self):
        return f"Order(id={self.id}, quantity={self.quantity}, status={self.order_status})"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    orders = relationship("Order", secondary=order_product, back_populates="products")

    def __repr__(self):
        return self.name



