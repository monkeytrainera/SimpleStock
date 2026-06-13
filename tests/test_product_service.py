import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.business.product_service import ProductService
from src.data.db_connection import init_database, DBConnection

class TestProductService(unittest.TestCase):
    def setUp(self):
        init_database()
    
    def test_add_product(self):
        product_id = ProductService.add_product("测试商品", "规格A", "件", 100, "测试备注")
        self.assertIsNotNone(product_id)
        self.assertGreater(product_id, 0)
    
    def test_get_product_by_id(self):
        product_id = ProductService.add_product("测试商品2", "规格B", "个", 50, "")
        product = ProductService.get_product_by_id(product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "测试商品2")
        self.assertEqual(product['spec'], "规格B")
        self.assertEqual(product['unit'], "个")
        self.assertEqual(product['quantity'], 50)
    
    def test_search_products(self):
        ProductService.add_product("苹果", "红富士", "斤", 200, "")
        ProductService.add_product("香蕉", "进口", "斤", 150, "")
        
        results = ProductService.search_products("苹果")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "苹果")
        
        results = ProductService.search_products("果")
        self.assertEqual(len(results), 2)
    
    def test_update_product(self):
        product_id = ProductService.add_product("测试商品3", "规格C", "箱", 30, "")
        ProductService.update_product(product_id, "测试商品3-修改", "规格C-修改", "箱", "修改备注")
        
        product = ProductService.get_product_by_id(product_id)
        self.assertEqual(product['name'], "测试商品3-修改")
        self.assertEqual(product['spec'], "规格C-修改")
    
    def test_delete_product(self):
        product_id = ProductService.add_product("测试商品4", "规格D", "个", 0, "")
        result = ProductService.delete_product(product_id)
        self.assertTrue(result)
        
        product = ProductService.get_product_by_id(product_id)
        self.assertIsNone(product)
    
    def test_delete_product_with_stock(self):
        product_id = ProductService.add_product("测试商品5", "规格E", "件", 10, "")
        
        with self.assertRaises(ValueError):
            ProductService.delete_product(product_id)

if __name__ == '__main__':
    unittest.main()
