from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QDialog,
                             QFormLayout, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from src.business.account_service import AccountService

class AccountManageWidget(QWidget):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.add_btn = QPushButton("新增操作员")
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
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["用户名", "角色", "创建时间", "操作"])
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
    
    def refresh_data(self):
        try:
            users = AccountService.get_all_operators()
            self.table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.table.setItem(row, 0, QTableWidgetItem(user['username']))
                role = "管理员" if user['role'] == 'admin' else "操作员"
                self.table.setItem(row, 1, QTableWidgetItem(role))
                self.table.setItem(row, 2, QTableWidgetItem(user['created_at']))
                
                if user['role'] == 'admin':
                    label = QLabel("(不可删除)")
                    label.setStyleSheet("color: #999; font-size: 12px;")
                    self.table.setCellWidget(row, 3, label)
                else:
                    delete_btn = QPushButton("删除")
                    delete_btn.setStyleSheet("""
                        QPushButton {
                            padding: 4px 12px;
                            background-color: #F44336;
                            color: white;
                            border: none;
                            border-radius: 3px;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #D32F2F;
                        }
                    """)
                    delete_btn.clicked.connect(lambda checked, u=user: self.handle_delete(u))
                    self.table.setCellWidget(row, 3, delete_btn)
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
    
    def handle_add(self):
        dialog = AddOperatorDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
    
    def handle_delete(self, user):
        confirm = QMessageBox.question(
            self, "确认删除", f"确定要删除操作员 '{user['username']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                AccountService.delete_operator(user['id'])
                QMessageBox.information(self, "删除成功", "操作员删除成功")
                self.refresh_data()
            except ValueError as e:
                QMessageBox.warning(self, "删除失败", str(e))

class AddOperatorDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("新增操作员")
        self.setFixedSize(350, 250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码（至少6位）")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("用户名 *", self.username_edit)
        form_layout.addRow("密码 *", self.password_edit)
        
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
    
    def handle_ok(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username:
            QMessageBox.warning(self, "错误", "用户名不能为空")
            return
        
        if not password or len(password) < 6:
            QMessageBox.warning(self, "错误", "密码长度不能少于6位")
            return
        
        try:
            AccountService.add_operator(username, password)
            QMessageBox.information(self, "添加成功", "操作员添加成功")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "添加失败", str(e))
