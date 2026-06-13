import hashlib

from src.data.account_dao import AccountDAO


class AccountService:
    @staticmethod
    def login(username, password):
        if not username or not password:
            raise ValueError("用户名和密码不能为空")

        user = AccountDAO.login(username, password)

        if not user:
            raise ValueError("用户名或密码错误")

        return user

    @staticmethod
    def change_password(user_id, old_password, new_password):
        if not old_password or not new_password:
            raise ValueError("原密码和新密码不能为空")

        if len(new_password) < 6:
            raise ValueError("新密码长度不能少于6位")

        return AccountDAO.change_password(user_id, old_password, new_password)

    @staticmethod
    def add_operator(username, password):
        if not username or not password:
            raise ValueError("用户名和密码不能为空")

        if len(password) < 6:
            raise ValueError("密码长度不能少于6位")

        existing_user = AccountDAO.get_user_by_username(username)
        if existing_user:
            raise ValueError("用户名已存在")

        return AccountDAO.add_operator(username, password)

    @staticmethod
    def delete_operator(user_id):
        user = AccountDAO.get_user_by_id(user_id)

        if not user:
            raise ValueError("用户不存在")

        if user["role"] == "admin":
            raise ValueError("管理员账号不能删除")

        return AccountDAO.delete_operator(user_id)

    @staticmethod
    def get_all_operators():
        return AccountDAO.get_all_operators()

    @staticmethod
    def get_user_by_id(user_id):
        return AccountDAO.get_user_by_id(user_id)

    @staticmethod
    def search_users(keyword=None):
        users = AccountDAO.get_all_operators()

        if keyword:
            keyword = keyword.lower()
            users = [user for user in users if keyword in user["username"].lower()]

        for user in users:
            user["is_admin"] = user["role"] == "admin"

        return users

    @staticmethod
    def add_user(username, password):
        if not username or not password:
            raise ValueError("用户名和密码不能为空")

        if len(password) < 6:
            raise ValueError("密码长度不能少于6位")

        existing_user = AccountDAO.get_user_by_username(username)
        if existing_user:
            raise ValueError("用户名已存在")

        return AccountDAO.add_operator(username, password)

    @staticmethod
    def update_user(user_id, username, password=None):
        from src.data.db_connection import DBConnection

        user = AccountDAO.get_user_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        db = DBConnection()

        if password:
            if len(password) < 6:
                raise ValueError("密码长度不能少于6位")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            db.execute(
                "UPDATE users SET username=?, password=? WHERE id=?",
                (username, hashed_password, user_id),
            )
        else:
            db.execute("UPDATE users SET username=? WHERE id=?", (username, user_id))
        return True

    @staticmethod
    def delete_user(user_id):
        user = AccountDAO.get_user_by_id(user_id)

        if not user:
            raise ValueError("用户不存在")

        if user["role"] == "admin":
            raise ValueError("管理员账号不能删除")

        return AccountDAO.delete_operator(user_id)

    @staticmethod
    def verify_password(username, password):
        user = AccountDAO.get_user_by_username(username)
        if not user:
            return False

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return user["password"] == hashed_password
