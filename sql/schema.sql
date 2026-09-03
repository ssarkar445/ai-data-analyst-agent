DROP TABLE IF EXISTS monthly_demand, inventory, order_items, orders, products, customers CASCADE;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    country TEXT NOT NULL,
    segment TEXT NOT NULL
);


CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(12,2) NOT NULL,
    cost NUMERIC(12,2) NOT NULL
);


CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    region TEXT NOT NULL
);


CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount NUMERIC(5,4) NOT NULL,
    gross_amount NUMERIC(14,2) NOT NULL,
    discount_amount NUMERIC(14,2) NOT NULL,
    net_amount NUMERIC(14,2) NOT NULL
);


CREATE TABLE inventory (
    product_id INTEGER PRIMARY KEY REFERENCES products(product_id),
    warehouse TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL,
    reorder_level INTEGER NOT NULL
);


CREATE TABLE monthly_demand (
    month DATE NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    demand_units INTEGER NOT NULL,
    PRIMARY KEY (month, product_id)
);
