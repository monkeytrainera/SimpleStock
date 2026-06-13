import sqlite3

from src.config.app_config import AppConfig


class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        if self.connection is None:
            AppConfig.init_directories()
            self.connection = sqlite3.connect(AppConfig.DB_PATH)
            self.connection.row_factory = sqlite3.Row
        else:
            try:
                self.connection.execute("SELECT 1")
            except sqlite3.Error:
                AppConfig.init_directories()
                self.connection = sqlite3.connect(AppConfig.DB_PATH)
                self.connection.row_factory = sqlite3.Row
        return self.connection

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def execute(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return cursor

    def query(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()

    def query_one(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchone()


def init_database():
    db = DBConnection()

    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'operator',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''

    create_products_table = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        spec VARCHAR(100),
        unit VARCHAR(20) NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 0,
        initial_quantity INTEGER NOT NULL DEFAULT 0,
        remark TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''

    create_stock_in_table = '''
    CREATE TABLE IF NOT EXISTS stock_in_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        remark TEXT,
        operator_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (operator_id) REFERENCES users(id)
    )
    '''

    create_stock_out_table = '''
    CREATE TABLE IF NOT EXISTS stock_out_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        remark TEXT,
        operator_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (operator_id) REFERENCES users(id)
    )
    '''

    create_indexes = [
        'CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)',
        'CREATE INDEX IF NOT EXISTS idx_stock_in_product_id ON stock_in_records(product_id)',
        'CREATE INDEX IF NOT EXISTS idx_stock_in_created_at ON stock_in_records(created_at)',
        'CREATE INDEX IF NOT EXISTS idx_stock_out_product_id ON stock_out_records(product_id)',
        'CREATE INDEX IF NOT EXISTS idx_stock_out_created_at ON stock_out_records(created_at)',
        'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)'
    ]

    db.execute(create_users_table)
    db.execute(create_products_table)
    db.execute(create_stock_in_table)
    db.execute(create_stock_out_table)

    for index_sql in create_indexes:
        db.execute(index_sql)

    cursor = db.query("SELECT COUNT(*) FROM users WHERE username='admin'")
    count = cursor[0][0] if cursor else 0

    if count == 0:
        import hashlib
        default_password = hashlib.sha256('admin123'.encode()).hexdigest()
        db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                   ('admin', default_password, 'admin'))

    db.close_connection()
