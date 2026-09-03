from ai_data_analyst.tools import execute_sql


sql = """
    SELECT
        category,
        SUM(price) AS total_product_value
    FROM products
    GROUP BY category
    ORDER BY total_product_value DESC;
"""
results = execute_sql(sql)

for result in results:
    print(result)