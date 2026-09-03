# AI Data Analyst Dataset

## Business definitions
- Revenue = quantity * unit_price * (1 - discount)
- Gross sales = quantity * unit_price
- Discount amount = gross sales - revenue
- Gross profit = revenue - (quantity * product cost)
- Gross margin % = gross profit / revenue
- Average order value (AOV) = total revenue / distinct orders
- Units sold = SUM(order_items.quantity)

## Tables

### customers
- customer_id: unique customer identifier
- customer_name: customer display name
- country: customer country
- segment: Consumer, Small Business, or Enterprise

### products
- product_id: unique product identifier
- product_name: product name
- category: Electronics, Office, Software, or Accessories
- price: standard selling price per unit
- cost: estimated product cost per unit

### orders
- order_id: unique order identifier
- customer_id: foreign key to customers
- order_date: date the order was created
- region: sales region

### order_items
- order_item_id: unique line-item identifier
- order_id: foreign key to orders
- product_id: foreign key to products
- quantity: units sold
- unit_price: selling price per unit before discount
- discount: decimal discount rate (e.g. 0.10 = 10%)
- gross_amount: quantity * unit_price
- discount_amount: gross_amount * discount
- net_amount: gross_amount - discount_amount

### inventory
- product_id: foreign key to products
- warehouse: inventory location
- stock_quantity: current units in stock
- reorder_level: stock level at which replenishment should be considered

### monthly_demand
- month: first day of the month
- product_id: foreign key to products
- demand_units: synthetic monthly demand estimate
