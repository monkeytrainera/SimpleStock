from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QLineEdit, QLabel)
from PyQt6.QtCore import Qt
from src.business.product_service import ProductService

class InventoryQueryWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel("库存查询")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        
        self.count_label = QLabel("商品总数: 0")
        self.count_label.setStyleSheet("font-size: 14px; color: #666;")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        
        search_label = QLabel("搜索:")
        search_label.setStyleSheet("font-size: 14px;")
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入商品名称")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
                min-width: 200px;
            }
        """)
        self.search_edit.textChanged.connect(self.handle_search)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        search_layout.addStretch()
        
        layout.addLayout(search_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["商品名称", "规格", "单位", "当前库存"])
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_data(self, keyword=""):
        try:
            products = ProductService.search_products(keyword)
            self.table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.table.setItem(row, 0, QTableWidgetItem(product['name']))
                self.table.setItem(row, 1, QTableWidgetItem(product['spec'] or ""))
                self.table.setItem(row, 2, QTableWidgetItem(product['unit']))
                self.table.setItem(row, 3, QTableWidgetItem(str(product['quantity'])))
            
            self.count_label.setText(f"商品总数: {len(products)}")
            self.table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error: {e}")
    
    def handle_search(self, keyword):
        self.refresh_data(keyword)
