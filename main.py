import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QDialog
from src.ui.login_dialog import LoginDialog
from src.ui.main_window import MainWindow
from src.data.db_connection import init_database
from src.utils.logger import Logger

def main():
    Logger.info("启动极简库存管理系统")
    
    init_database()
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    login_dialog = LoginDialog()
    
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        user = login_dialog.get_user()
        Logger.info(f"用户 {user['username']} 登录成功")
        
        main_window = MainWindow(user)
        main_window.show()
        
        sys.exit(app.exec())
    else:
        Logger.info("用户取消登录")

if __name__ == "__main__":
    main()
