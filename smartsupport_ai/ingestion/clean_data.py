import pandas as pd

def clean_csv(file_path):
    df = pd.read_csv(file_path)
    # Basic cleaning
    df.fillna("N/A", inplace=True)
    df.drop_duplicates(inplace=True)
    df.to_csv(file_path, index=False)
    print(f"Cleaned {file_path}")

if __name__ == "__main__":
    clean_csv('smartsupport_ai/datasets/customers.csv')
    clean_csv('smartsupport_ai/datasets/products.csv')
    clean_csv('smartsupport_ai/datasets/orders.csv')
    clean_csv('smartsupport_ai/datasets/tickets.csv')
