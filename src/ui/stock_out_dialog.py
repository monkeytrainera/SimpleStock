from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from src.business.product_service import ProductService
from src.business.stock_service import StockService

class StockOutDialog(QDialog):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.products = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("出库管理")
        self.setFixedSize(400, 320)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.product_combo = QComboBox()
        self.product_combo.setEditable(True)
        self.product_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
                min-width: 200px;
            }
        """)
        
        form_layout.addRow("商品 *", self.product_combo)
        
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("请输入出库数量")
        self.quantity_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        
        self.stock_label = QLabel("当前库存: 0")
        self.stock_label.setStyleSheet("color: #666; font-size: 12px;")
        
        self.load_products()
        
        quantity_layout = QVBoxLayout()
        quantity_layout.addWidget(self.quantity_edit)
        quantity_layout.addWidget(self.stock_label)
        
        form_layout.addRow("出库数量 *", quantity_layout)
        
        self.remark_edit = QLineEdit()
        self.remark_edit.setPlaceholderText("请输入备注（可选）")
        self.remark_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        
        form_layout.addRow("备注", self.remark_edit)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        ok_btn = QPushButton("确认出库")
        ok_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        ok_btn.clicked.connect(self.handle_ok)
        
        reset_btn = QPushButton("重置")
        reset_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E8E8E8;
            }
        """)
        reset_btn.clicked.connect(self.handle_reset)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(reset_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        self.product_combo.currentIndexChanged.connect(self.handle_product_change)
        self.quantity_edit.returnPressed.connect(self.handle_ok)
    
    def load_products(self):
        try:
            self.products = ProductService.get_all_products()
            self.product_combo.clear()
            
            for product in self.products:
                self.product_combo.addItem(product['name'], product['id'])
            
            if self.products:
                self.update_stock_label()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
    
    def handle_product_change(self, index):
        self.update_stock_label()
    
    def update_stock_label(self):
        product_id = self.product_combo.currentData()
        if product_id:
            stock = StockService.get_stock_by_product_id(product_id)
            self.stock_label.setText(f"当前库存: {stock}")
        else:
            self.stock_label.setText("当前库存: 0")
    
    def handle_ok(self):
        product_id = self.product_combo.currentData()
        
        if not product_id:
            QMessageBox.warning(self, "错误", "请选择商品")
            return
        
        try:
            quantity = int(self.quantity_edit.text())
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效数量")
            return
        
        remark = self.remark_edit.text().strip()
        
        try:
            StockService.stock_out(product_id, quantity, remark, self.user['id'])
            QMessageBox.information(self, "出库成功", "商品出库成功")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "出库失败", str(e))
    
    def handle_reset(self):
        self.product_combo.setCurrentIndex(0)
        self.quantity_edit.clear()
        self.remark_edit.clear()
