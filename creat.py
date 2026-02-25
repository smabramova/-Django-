import csv
import mysql.connector


def clean_and_prepare_data(csv_file):
    cleaned_data = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            price = float(row['price']) if row['price'].strip() else None
            stock_qty = int(row['stock_quantity']) if row['stock_quantity'].strip() else 0
            category_id = int(row['category_id']) if row['category_id'].strip() else None
            
            cleaned_row = {
                'product_id': row['product_id'],
                'name': row['name'],
                'price': price,
                'category_id': category_id,
                'size': row['size'],
                'color': row['color'],
                'stock_quantity': stock_qty
            }
            cleaned_data.append(cleaned_row)
    return cleaned_data



db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database"
)
cursor = db_connection.cursor()


prepared_data = clean_and_prepare_data('products.csv')


insert_query = """
INSERT INTO Products (ProductID, Name, Price, CategoryID, Size, Color, StockQuantity)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""


values_to_insert = [(row['product_id'], row['name'], row['price'], row['category_id'], row['size'], row['color'], row['stock_quantity']) for row in prepared_data]


cursor.executemany(insert_query, values_to_insert)


db_connection.commit()


cursor.close()
db_connection.close()