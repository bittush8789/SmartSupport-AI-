import csv
import json
import random
from datetime import datetime, timedelta

def generate_customers(n=1000):
    customers = []
    plans = ['Basic', 'Premium', 'VIP']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    for i in range(1, n + 1):
        join_date = (datetime.now() - timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d')
        customers.append({
            'customer_id': f'CUST{i:04d}',
            'name': f'Customer {i}',
            'email': f'customer{i}@example.com',
            'city': random.choice(cities),
            'phone': f'+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
            'membership_plan': random.choice(plans),
            'join_date': join_date
        })
    
    with open('smartsupport_ai/datasets/customers.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    return customers

def generate_products(n=500):
    products = []
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Beauty', 'Sports', 'Books', 'Toys']
    
    for i in range(1, n + 1):
        products.append({
            'product_id': f'PROD{i:03d}',
            'product_name': f'Product {i}',
            'category': random.choice(categories),
            'price': round(random.uniform(10, 2000), 2),
            'stock': random.randint(0, 1000),
            'warranty': f'{random.randint(6, 24)} months'
        })
        
    with open('smartsupport_ai/datasets/products.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    return products

def generate_orders(customers, products, n=5000):
    orders = []
    payment_statuses = ['Paid', 'Pending', 'Failed']
    shipping_statuses = ['Shipped', 'Processing', 'Delivered', 'Cancelled']
    
    for i in range(1, n + 1):
        cust = random.choice(customers)
        prod = random.choice(products)
        qty = random.randint(1, 5)
        amount = round(prod['price'] * qty, 2)
        delivery_date = (datetime.now() + timedelta(days=random.randint(-10, 10))).strftime('%Y-%m-%d')
        
        orders.append({
            'order_id': f'ORD{i:04d}',
            'customer_id': cust['customer_id'],
            'product_id': prod['product_id'],
            'quantity': qty,
            'amount': amount,
            'payment_status': random.choice(payment_statuses),
            'shipping_status': random.choice(shipping_statuses),
            'delivery_date': delivery_date
        })
        
    with open('smartsupport_ai/datasets/orders.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)

def generate_tickets(customers, n=1000):
    tickets = []
    issue_types = ['Refund', 'Shipping', 'Damaged Product', 'Payment Issue', 'Account Access', 'General Inquiry']
    priorities = ['Low', 'Medium', 'High', 'Urgent']
    statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
    
    for i in range(1, n + 1):
        cust = random.choice(customers)
        created_at = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
        
        tickets.append({
            'ticket_id': f'TKT{i:04d}',
            'customer_id': cust['customer_id'],
            'issue_type': random.choice(issue_types),
            'issue_description': f'Description for issue {i}...',
            'priority': random.choice(priorities),
            'created_at': created_at,
            'status': random.choice(statuses)
        })
        
    with open('smartsupport_ai/datasets/tickets.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
        writer.writeheader()
        writer.writerows(tickets)

def generate_faqs(n=100):
    faqs = []
    questions = [
        "How do I track my order?", "What is your refund policy?", "How can I contact support?",
        "Do you ship internationally?", "How do I change my password?", "What payment methods do you accept?",
        "Can I cancel my order?", "How long does shipping take?", "What if I receive a damaged product?",
        "Do you have a loyalty program?"
    ]
    
    for i in range(1, n + 1):
        q = random.choice(questions) + f" (Variation {i})"
        faqs.append({
            'question': q,
            'answer': f"This is the automated answer for FAQ {i}. Please follow the standard procedure for {q.lower()}."
        })
        
    with open('smartsupport_ai/datasets/faqs.json', 'w') as f:
        json.dump(faqs, f, indent=4)

def generate_policies():
    policies = {
        "refund_policy": "Customers can request a refund within 30 days of purchase. The item must be in its original packaging.",
        "shipping_policy": "We offer standard shipping (5-7 business days) and express shipping (1-2 business days). Shipping is free on orders over $50.",
        "return_policy": "Returns are accepted within 14 days of delivery. Return shipping costs are covered by the customer unless the item is defective.",
        "cancellation_policy": "Orders can be cancelled within 2 hours of placement. After 2 hours, the order may have already been processed.",
        "privacy_policy": "We value your privacy. Your data is encrypted and never shared with third parties without your consent."
    }
    with open('smartsupport_ai/datasets/policies.json', 'w') as f:
        json.dump(policies, f, indent=4)

def generate_knowledge_base():
    content = """
ShopEase Support Procedures:

1. Order Tracking:
   - Ask customer for Order ID.
   - Look up in PostgreSQL orders table.
   - Provide status (Shipped, Processing, etc.) and delivery date.

2. Refund Process:
   - Verify purchase within 30 days.
   - Check if item is eligible for return.
   - Initiate refund in the system.
   - Inform customer it takes 5-7 business days.

3. Damaged Product:
   - Request photos of damage.
   - Create a support ticket with priority High.
   - Offer replacement or full refund.

4. VIP Support:
   - Identify customers with 'VIP' membership plan.
   - Assign tickets to senior support agents immediately.
   - Provide instant chat responses.

5. Escalation Policy:
   - If a ticket is unresolved for more than 48 hours, escalate to Manager.
   - If customer sentiment is 'Angry', auto-create ticket and notify supervisor.
"""
    with open('smartsupport_ai/datasets/knowledge_base.txt', 'w') as f:
        f.write(content)


if __name__ == "__main__":
    print("Generating data...")
    custs = generate_customers(1000)
    prods = generate_products(500)
    generate_orders(custs, prods, 5000)
    generate_tickets(custs, 1000)
    generate_faqs(100)
    generate_policies()
    generate_knowledge_base()
    print("Data generation complete.")
