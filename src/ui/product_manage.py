from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt
from src.business.product_service import ProductService

class ProductManageWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.add_btn = QPushButton("新增商品")
        self.add_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.add_btn.clicked.connect(self.handle_add)
        header_layout.addWidget(self.add_btn)
        
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["商品名称", "规格", "单位", "当前库存", "操作"])
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
                
                edit_btn = QPushButton("编辑")
                edit_btn.setFixedSize(50, 24)
                edit_btn.setStyleSheet("""
                    QPushButton {
                        padding: 2px 8px;
                        background-color: #FF9800;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                """)
                edit_btn.clicked.connect(lambda checked, p=product: self.handle_edit(p))
                
                delete_btn = QPushButton("删除")
                delete_btn.setFixedSize(50, 24)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        padding: 2px 8px;
                        background-color: #F44336;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #D32F2F;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, p=product: self.handle_delete(p))
                
                btn_layout = QHBoxLayout()
                btn_layout.setContentsMargins(0, 2, 0, 2)
                btn_layout.setSpacing(6)
                btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                btn_layout.addWidget(edit_btn)
                btn_layout.addWidget(delete_btn)
                
                btn_widget = QWidget()
                btn_widget.setLayout(btn_layout)
                self.table.setCellWidget(row, 4, btn_widget)
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
    
    def handle_search(self, keyword):
        self.refresh_data(keyword)
    
    def handle_add(self):
        dialog = ProductFormDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
    
    def handle_edit(self, product):
        dialog = ProductFormDialog(self, product)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
    
    def handle_delete(self, product):
        confirm = QMessageBox.question(
            self, "确认删除", f"确定要删除商品 '{product['name']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                ProductService.delete_product(product['id'])
                QMessageBox.information(self, "删除成功", "商品删除成功")
                self.refresh_data()
            except ValueError as e:
                QMessageBox.warning(self, "删除失败", str(e))

class ProductFormDialog(QDialog):
    def __init__(self, parent, product=None):
        super().__init__(parent)
        self.product = product
        self.init_ui()
    
    def init_ui(self):
        if self.product:
            self.setWindowTitle("编辑商品")
        else:
            self.setWindowTitle("新增商品")
        
        self.setFixedSize(400, 350)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入商品名称")
        
        self.spec_edit = QLineEdit()
        self.spec_edit.setPlaceholderText("请输入规格型号")
        
        self.unit_edit = QLineEdit()
        self.unit_edit.setPlaceholderText("请输入单位")
        
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("请输入初始库存")
        
        self.remark_edit = QLineEdit()
        self.remark_edit.setPlaceholderText("请输入备注")
        
        form_layout.addRow("商品名称 *", self.name_edit)
        form_layout.addRow("规格", self.spec_edit)
        form_layout.addRow("单位 *", self.unit_edit)
        form_layout.addRow("初始库存 *", self.quantity_edit)
        form_layout.addRow("备注", self.remark_edit)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        ok_btn = QPushButton("保存")
        ok_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        ok_btn.clicked.connect(self.handle_ok)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
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
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        if self.product:
            self.name_edit.setText(self.product['name'])
            self.spec_edit.setText(self.product['spec'] or "")
            self.unit_edit.setText(self.product['unit'])
            self.quantity_edit.setText(str(self.product['initial_quantity']))
            self.remark_edit.setText(self.product['remark'] or "")
            self.quantity_edit.setEnabled(False)
    
    def handle_ok(self):
        name = self.name_edit.text().strip()
        spec = self.spec_edit.text().strip()
        unit = self.unit_edit.text().strip()
        remark = self.remark_edit.text().strip()
        
        try:
            quantity = int(self.quantity_edit.text()) if self.quantity_edit.text() else 0
        except ValueError:
            QMessageBox.warning(self, "错误", "初始库存必须是数字")
            return
        
        if not name:
            QMessageBox.warning(self, "错误", "商品名称不能为空")
            return
        
        if not unit:
            QMessageBox.warning(self, "错误", "单位不能为空")
            return
        
        try:
            if self.product:
                ProductService.update_product(self.product['id'], name, spec, unit, remark)
            else:
                ProductService.add_product(name, spec, unit, quantity, remark)
            
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "错误", str(e))
