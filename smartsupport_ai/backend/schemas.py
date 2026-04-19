from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatRequest(BaseModel):
    customer_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    sentiment: str

class TicketCreate(BaseModel):
    customer_id: str
    issue_type: str
    description: str
    priority: str

class FeedbackCreate(BaseModel):
    customer_id: str
    rating: int
    comment: str

class OrderResponse(BaseModel):
    order_id: str
    product_id: str
    amount: float
    shipping_status: str
    delivery_date: datetime

    class Config:
        from_attributes = True
