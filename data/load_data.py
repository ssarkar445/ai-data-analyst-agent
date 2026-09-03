import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql+psycopg2://"
    "analyst:analyst_password@localhost:5432/analytics"
)

engine = create_engine(DATABASE_URL)

tables = {
    "customers": "customers.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "inventory": "inventory.csv",
    "monthly_demand": "monthly_demand.csv",
}

for table_name, csv_path in tables.items():
    print(f"Loading {csv_path}...")

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Loaded {len(df)} rows into {table_name}")

print("Data loading completed!")