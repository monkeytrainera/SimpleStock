import hashlib

from src.data.db_connection import DBConnection


class AccountDAO:
    @staticmethod
    def login(username, password):
        db = DBConnection()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        result = db.query_one(sql, (username, hashed_password))
        return dict(result) if result else None

    @staticmethod
    def change_password(user_id, old_password, new_password):
        db = DBConnection()
        sql = "SELECT password FROM users WHERE id=?"
        result = db.query_one(sql, (user_id,))

        if not result:
            return False

        old_hashed = hashlib.sha256(old_password.encode()).hexdigest()
        if result['password'] != old_hashed:
            return False

        new_hashed = hashlib.sha256(new_password.encode()).hexdigest()
        update_sql = "UPDATE users SET password=? WHERE id=?"
        db.execute(update_sql, (new_hashed, user_id))
        return True

    @staticmethod
    def add_operator(username, password):
        db = DBConnection()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        sql = "INSERT INTO users (username, password, role) VALUES (?, ?, 'operator')"
        cursor = db.execute(sql, (username, hashed_password))
        return cursor.lastrowid

    @staticmethod
    def delete_operator(user_id):
        db = DBConnection()
        db.execute("DELETE FROM users WHERE id=?", (user_id,))
        return True

    @staticmethod
    def get_all_operators():
        db = DBConnection()
        sql = "SELECT * FROM users ORDER BY created_at DESC"
        results = db.query(sql)
        return [dict(row) for row in results]

    @staticmethod
    def get_user_by_id(user_id):
        db = DBConnection()
        sql = "SELECT * FROM users WHERE id=?"
        result = db.query_one(sql, (user_id,))
        return dict(result) if result else None

    @staticmethod
    def get_user_by_username(username):
        db = DBConnection()
        sql = "SELECT * FROM users WHERE username=?"
        result = db.query_one(sql, (username,))
        return dict(result) if result else None
