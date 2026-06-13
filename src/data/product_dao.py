from src.data.db_connection import DBConnection


class ProductDAO:
    @staticmethod
    def add_product(name, spec, unit, initial_quantity, remark):
        db = DBConnection()
        sql = '''
        INSERT INTO products (name, spec, unit, quantity, initial_quantity, remark)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor = db.execute(sql, (name, spec, unit, initial_quantity, initial_quantity, remark))
        return cursor.lastrowid

    @staticmethod
    def update_product(product_id, name, spec, unit, remark):
        db = DBConnection()
        sql = '''
        UPDATE products SET name=?, spec=?, unit=?, remark=? WHERE id=?
        '''
        db.execute(sql, (name, spec, unit, remark, product_id))
        return True

    @staticmethod
    def delete_product(product_id):
        db = DBConnection()
        db.execute("DELETE FROM products WHERE id=?", (product_id,))
        return True

    @staticmethod
    def get_product_by_id(product_id):
        db = DBConnection()
        sql = "SELECT * FROM products WHERE id=?"
        result = db.query_one(sql, (product_id,))
        return dict(result) if result else None

    @staticmethod
    def search_products(keyword):
        db = DBConnection()
        sql = "SELECT * FROM products WHERE name LIKE ? ORDER BY created_at DESC"
        results = db.query(sql, ('%' + keyword + '%',))
        return [dict(row) for row in results]

    @staticmethod
    def get_all_products():
        db = DBConnection()
        sql = "SELECT * FROM products ORDER BY created_at DESC"
        results = db.query(sql)
        return [dict(row) for row in results]

    @staticmethod
    def update_stock(product_id, quantity):
        db = DBConnection()
        sql = "UPDATE products SET quantity=? WHERE id=?"
        db.execute(sql, (quantity, product_id))
        return True

    @staticmethod
    def get_stock_by_product_id(product_id):
        db = DBConnection()
        sql = "SELECT quantity FROM products WHERE id=?"
        result = db.query_one(sql, (product_id,))
        return result['quantity'] if result else 0

    @staticmethod
    def get_product_count():
        db = DBConnection()
        sql = "SELECT COUNT(*) FROM products"
        result = db.query_one(sql)
        return result[0] if result else 0

    @staticmethod
    def has_stock_or_records(product_id):
        db = DBConnection()

        sql_stock = "SELECT quantity FROM products WHERE id=?"
        stock_result = db.query_one(sql_stock, (product_id,))
        if stock_result and stock_result['quantity'] > 0:
            return True

        sql_in = "SELECT COUNT(*) FROM stock_in_records WHERE product_id=?"
        in_count = db.query_one(sql_in, (product_id,))
        if in_count and in_count[0] > 0:
            return True

        sql_out = "SELECT COUNT(*) FROM stock_out_records WHERE product_id=?"
        out_count = db.query_one(sql_out, (product_id,))
        if out_count and out_count[0] > 0:
            return True

        return False
