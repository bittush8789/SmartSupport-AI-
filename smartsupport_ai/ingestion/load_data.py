import pandas as pd
import json
from sqlalchemy.orm import Session
from smartsupport_ai.db.database import SessionLocal, engine, init_db
from smartsupport_ai.db.models import Customer, Product, Order, Ticket
import datetime

def load_csv_data(db: Session):
    # Load Customers
    customers_df = pd.read_csv('smartsupport_ai/datasets/customers.csv')
    for _, row in customers_df.iterrows():
        customer = Customer(
            customer_id=row['customer_id'],
            name=row['name'],
            email=row['email'],
            city=row['city'],
            phone=row['phone'],
            membership_plan=row['membership_plan'],
            join_date=datetime.datetime.strptime(row['join_date'], '%Y-%m-%d')
        )
        db.merge(customer)

    # Load Products
    products_df = pd.read_csv('smartsupport_ai/datasets/products.csv')
    for _, row in products_df.iterrows():
        product = Product(
            product_id=row['product_id'],
            product_name=row['product_name'],
            category=row['category'],
            price=row['price'],
            stock=row['stock'],
            warranty=row['warranty']
        )
        db.merge(product)

    # Load Orders
    orders_df = pd.read_csv('smartsupport_ai/datasets/orders.csv')
    for _, row in orders_df.iterrows():
        order = Order(
            order_id=row['order_id'],
            customer_id=row['customer_id'],
            product_id=row['product_id'],
            quantity=row['quantity'],
            amount=row['amount'],
            payment_status=row['payment_status'],
            shipping_status=row['shipping_status'],
            delivery_date=datetime.datetime.strptime(row['delivery_date'], '%Y-%m-%d')
        )
        db.merge(order)

    # Load Tickets
    tickets_df = pd.read_csv('smartsupport_ai/datasets/tickets.csv')
    for _, row in tickets_df.iterrows():
        ticket = Ticket(
            ticket_id=row['ticket_id'],
            customer_id=row['customer_id'],
            issue_type=row['issue_type'],
            issue_description=row['issue_description'],
            priority=row['priority'],
            created_at=datetime.datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S'),
            status=row['status']
        )
        db.merge(ticket)

    db.commit()
    print("PostgreSQL data ingestion complete.")

if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        load_csv_data(db)
    finally:
        db.close()
