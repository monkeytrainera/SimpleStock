import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.business.product_service import ProductService
from src.business.stock_service import StockService
from src.data.db_connection import init_database

class TestStockService(unittest.TestCase):
    def setUp(self):
        init_database()
    
    def test_stock_in(self):
        product_id = ProductService.add_product("库存测试商品", "规格A", "件", 50, "")
        
        result = StockService.stock_in(product_id, 50, "采购入库", 1)
        self.assertTrue(result)
        
        stock = StockService.get_stock_by_product_id(product_id)
        self.assertEqual(stock, 100)
    
    def test_stock_out(self):
        product_id = ProductService.add_product("出库测试商品", "规格B", "个", 100, "")
        
        result = StockService.stock_out(product_id, 30, "销售出库", 1)
        self.assertTrue(result)
        
        stock = StockService.get_stock_by_product_id(product_id)
        self.assertEqual(stock, 70)
    
    def test_stock_out_insufficient(self):
        product_id = ProductService.add_product("库存不足测试", "规格C", "箱", 20, "")
        
        with self.assertRaises(ValueError):
            StockService.stock_out(product_id, 30, "销售出库", 1)
    
    def test_stock_in_negative_quantity(self):
        product_id = ProductService.add_product("负数测试", "规格D", "件", 10, "")
        
        with self.assertRaises(ValueError):
            StockService.stock_in(product_id, -10, "测试", 1)
    
    def test_stock_out_negative_quantity(self):
        product_id = ProductService.add_product("出库负数测试", "规格E", "个", 50, "")
        
        with self.assertRaises(ValueError):
            StockService.stock_out(product_id, -10, "测试", 1)

if __name__ == '__main__':
    unittest.main()
