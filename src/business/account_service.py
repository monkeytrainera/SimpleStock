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
        
        if user['role'] == 'admin':
            raise ValueError("管理员账号不能删除")
        
        return AccountDAO.delete_operator(user_id)
    
    @staticmethod
    def get_all_operators():
        return AccountDAO.get_all_operators()
    
    @staticmethod
    def get_user_by_id(user_id):
        return AccountDAO.get_user_by_id(user_id)
