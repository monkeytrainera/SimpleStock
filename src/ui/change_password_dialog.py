from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from src.business.account_service import AccountService

class ChangePasswordDialog(QDialog):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("修改密码")
        self.setFixedSize(350, 280)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.old_password_edit = QLineEdit()
        self.old_password_edit.setPlaceholderText("请输入原密码")
        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setPlaceholderText("请输入新密码（至少6位）")
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("请确认新密码")
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        form_layout.addRow("原密码 *", self.old_password_edit)
        form_layout.addRow("新密码 *", self.new_password_edit)
        form_layout.addRow("确认密码 *", self.confirm_password_edit)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        ok_btn = QPushButton("确认")
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
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        
        if not old_password:
            QMessageBox.warning(self, "错误", "请输入原密码")
            return
        
        if not new_password or len(new_password) < 6:
            QMessageBox.warning(self, "错误", "新密码长度不能少于6位")
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "错误", "两次输入的密码不一致")
            return
        
        try:
            success = AccountService.change_password(self.user['id'], old_password, new_password)
            
            if success:
                QMessageBox.information(self, "修改成功", "密码修改成功")
                self.accept()
            else:
                QMessageBox.warning(self, "修改失败", "原密码不正确")
        except ValueError as e:
            QMessageBox.warning(self, "修改失败", str(e))
