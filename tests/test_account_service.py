import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.business.account_service import AccountService
from src.data.db_connection import init_database

class TestAccountService(unittest.TestCase):
    def setUp(self):
        init_database()
    
    def test_login_success(self):
        user = AccountService.login("admin", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "admin")
        self.assertEqual(user['role'], "admin")
    
    def test_login_failure(self):
        with self.assertRaises(ValueError):
            AccountService.login("admin", "wrongpassword")
    
    def test_login_empty(self):
        with self.assertRaises(ValueError):
            AccountService.login("", "password")
        
        with self.assertRaises(ValueError):
            AccountService.login("user", "")
    
    def test_add_operator(self):
        user_id = AccountService.add_operator("test_operator", "password123")
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0)
    
    def test_add_operator_existing_username(self):
        AccountService.add_operator("existing_user", "password123")
        
        with self.assertRaises(ValueError):
            AccountService.add_operator("existing_user", "password456")
    
    def test_add_operator_short_password(self):
        with self.assertRaises(ValueError):
            AccountService.add_operator("user2", "123")
    
    def test_change_password(self):
        user_id = AccountService.add_operator("change_pwd_user", "oldpassword")
        
        result = AccountService.change_password(user_id, "oldpassword", "newpassword123")
        self.assertTrue(result)
        
        user = AccountService.login("change_pwd_user", "newpassword123")
        self.assertIsNotNone(user)
    
    def test_change_password_wrong_old(self):
        user_id = AccountService.add_operator("wrong_old_user", "correctpassword")
        
        result = AccountService.change_password(user_id, "wrongpassword", "newpassword")
        self.assertFalse(result)
    
    def test_delete_operator(self):
        user_id = AccountService.add_operator("delete_test", "password123")
        result = AccountService.delete_operator(user_id)
        self.assertTrue(result)
    
    def test_delete_admin(self):
        admin = AccountService.login("admin", "admin123")
        
        with self.assertRaises(ValueError):
            AccountService.delete_operator(admin['id'])

if __name__ == '__main__':
    unittest.main()
