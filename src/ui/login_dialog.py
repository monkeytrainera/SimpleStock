from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from src.business.account_service import AccountService

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.user = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("登录 - 极简库存管理系统")
        self.setFixedSize(420, 500)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 60, 50, 50)
        
        title_label = QLabel("极简库存管理系统")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #1E88E5;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        main_layout.addSpacing(8)
        
        subtitle_label = QLabel("请输入账号密码登录系统")
        subtitle_label.setStyleSheet("font-size: 13px; color: #666;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(30)
        
        username_label = QLabel("用户名")
        username_label.setStyleSheet("font-size: 14px; color: #333;")
        main_layout.addWidget(username_label)
        
        main_layout.addSpacing(12)
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 10px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
                min-height: 32px;
            }
            QLineEdit:focus {
                border-color: #1E88E5;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #999;
            }
        """)
        main_layout.addWidget(self.username_edit)
        
        main_layout.addSpacing(28)
        
        password_label = QLabel("密码")
        password_label.setStyleSheet("font-size: 14px; color: #333;")
        main_layout.addWidget(password_label)
        
        main_layout.addSpacing(12)
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px 10px;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 13px;
                min-height: 32px;
            }
            QLineEdit:focus {
                border-color: #1E88E5;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #999;
            }
        """)
        main_layout.addWidget(self.password_edit)
        
        main_layout.addSpacing(20)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #F44336; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.error_label)
        
        main_layout.addSpacing(20)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.login_btn = QPushButton("登录")
        self.login_btn.setFixedSize(120, 38)
        self.login_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 24px;
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        
        reset_btn = QPushButton("重置")
        reset_btn.setFixedSize(120, 38)
        reset_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 24px;
                background-color: #FFFFFF;
                color: #666;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                border-color: #BDBDBD;
            }
        """)
        reset_btn.clicked.connect(self.handle_reset)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(reset_btn)
        main_layout.addLayout(button_layout)
        
        main_layout.addSpacing(25)
        
        footer_label = QLabel("默认账号：admin / admin123")
        footer_label.setStyleSheet("font-size: 11px; color: #999;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer_label)
        
        self.setLayout(main_layout)
        
        self.username_edit.returnPressed.connect(self.handle_login)
        self.password_edit.returnPressed.connect(self.handle_login)
    
    def handle_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        try:
            self.user = AccountService.login(username, password)
            self.accept()
        except ValueError as e:
            self.error_label.setText(str(e))
    
    def handle_reset(self):
        self.username_edit.clear()
        self.password_edit.clear()
        self.error_label.clear()
    
    def get_user(self):
        return self.user
