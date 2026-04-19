from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="customer") # customer, admin

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    city = Column(String)
    phone = Column(String)
    membership_plan = Column(String)
    join_date = Column(DateTime)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(String, primary_key=True, index=True)
    product_name = Column(String)
    category = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    warranty = Column(String)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    product_id = Column(String, ForeignKey('products.product_id'))
    quantity = Column(Integer)
    amount = Column(Float)
    payment_status = Column(String)
    shipping_status = Column(String)
    delivery_date = Column(DateTime)

class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    issue_type = Column(String)
    issue_description = Column(Text)
    priority = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    sentiment = Column(String)

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
