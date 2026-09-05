DATABASE_SCHEMA = """
Database: public

Table: customers
Columns:
- customer_id
- customer_name
- country
- segment

Table: products
Columns:
- product_id
- product_name
- category
- price
- cost

Table: orders
Columns:
- order_id
- customer_id
- order_date
- region

Table: order_items
Columns:
- order_item_id
- order_id
- product_id
- quantity
- unit_price
- discount
- gross_amount
- discount_amount
- net_amount

Table: inventory
Columns:
- product_id
- warehouse
- stock_quantity
- reorder_level

Table: monthly_demand
Columns:
- month
- product_id
- demand_units

Relationships:

customers.customer_id
    → orders.customer_id

orders.order_id
    → order_items.order_id

products.product_id
    → order_items.product_id

products.product_id
    → inventory.product_id

products.product_id
    → monthly_demand.product_id
"""