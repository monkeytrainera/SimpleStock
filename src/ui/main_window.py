from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.ui.account_manage import AccountManageWidget
from src.ui.change_password_dialog import ChangePasswordDialog
from src.ui.inventory_query import InventoryQueryWidget
from src.ui.ledger_view import LedgerViewWidget
from src.ui.product_manage import ProductManageWidget
from src.ui.stock_in_dialog import StockInDialog
from src.ui.stock_out_dialog import StockOutDialog
from src.utils.data_backup import DataBackup
from src.utils.logger import Logger


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.current_widget = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("极简库存管理系统")
        self.setMinimumSize(900, 600)
        self.setGeometry(100, 100, 1000, 700)

        self.create_menu_bar()
        self.create_status_bar()
        self.create_central_widget()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = QMenu("文件", self)
        backup_action = file_menu.addAction("数据备份")
        backup_action.triggered.connect(self.handle_backup)

        restore_action = file_menu.addAction("数据恢复")
        restore_action.triggered.connect(self.handle_restore)

        file_menu.addSeparator()

        exit_action = file_menu.addAction("退出")
        exit_action.triggered.connect(self.close)

        menu_bar.addMenu(file_menu)

        edit_menu = QMenu("编辑", self)
        change_pwd_action = edit_menu.addAction("修改密码")
        change_pwd_action.triggered.connect(self.handle_change_password)

        menu_bar.addMenu(edit_menu)

        help_menu = QMenu("帮助", self)
        about_action = help_menu.addAction("关于")
        about_action.triggered.connect(self.handle_about)

        menu_bar.addMenu(help_menu)

    def create_status_bar(self):
        status_bar = self.statusBar()
        status_bar.showMessage(
            f"当前用户: {self.user['username']} ({'管理员' if self.user['role'] == 'admin' else '操作员'})"
        )

    def create_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav_widget = self.create_navigation()
        layout.addWidget(nav_widget)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        layout.addWidget(self.content_area, 1)

        central_widget.setLayout(layout)

        self.switch_to_product_manage()

    def create_navigation(self):
        nav_widget = QWidget()
        nav_widget.setFixedWidth(180)
        nav_widget.setStyleSheet("background-color: #333;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav_items = [
            ("📦 商品管理", self.switch_to_product_manage),
            ("➕ 入库管理", self.switch_to_stock_in),
            ("➖ 出库管理", self.switch_to_stock_out),
            ("🔍 库存查询", self.switch_to_inventory_query),
            ("📊 台账报表", self.switch_to_ledger),
        ]

        if self.user["role"] == "admin":
            nav_items.append(("👤 账号管理", self.switch_to_account_manage))

        for label, callback in nav_items:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    padding: 15px 20px;
                    text-align: left;
                    border: none;
                    color: #FFF;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #444;
                }
                QPushButton:pressed {
                    background-color: #1E88E5;
                }
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()

        nav_widget.setLayout(layout)
        return nav_widget

    def clear_content(self):
        if self.current_widget:
            self.content_layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
            self.current_widget = None

    def switch_to_product_manage(self):
        self.clear_content()
        self.current_widget = ProductManageWidget(self)
        self.content_layout.addWidget(self.current_widget)

    def switch_to_stock_in(self):
        dialog = StockInDialog(self, self.user)
        dialog.exec()

        if self.current_widget:
            self.current_widget.refresh_data()

    def switch_to_stock_out(self):
        dialog = StockOutDialog(self, self.user)
        dialog.exec()

        if self.current_widget:
            self.current_widget.refresh_data()

    def switch_to_inventory_query(self):
        self.clear_content()
        self.current_widget = InventoryQueryWidget(self)
        self.content_layout.addWidget(self.current_widget)

    def switch_to_ledger(self):
        self.clear_content()
        self.current_widget = LedgerViewWidget(self, self.user)
        self.content_layout.addWidget(self.current_widget)

    def switch_to_account_manage(self):
        if self.user["role"] != "admin":
            QMessageBox.warning(self, "权限不足", "只有管理员可以访问账号管理")
            return

        self.clear_content()
        self.current_widget = AccountManageWidget(self, self.user)
        self.content_layout.addWidget(self.current_widget)

    def handle_backup(self):
        try:
            backup_path = DataBackup.backup()
            QMessageBox.information(
                self, "备份成功", f"数据备份成功！\n备份文件: {backup_path}"
            )
            Logger.info(f"用户 {self.user['username']} 执行数据备份")
        except Exception as e:
            QMessageBox.critical(self, "备份失败", f"数据备份失败: {str(e)}")
            Logger.error(f"数据备份失败: {str(e)}")

    def handle_restore(self):
        backup_list = DataBackup.get_backup_list()
        if not backup_list:
            QMessageBox.warning(self, "无备份文件", "没有找到备份文件")
            return

        backup_path, _ = QFileDialog.getOpenFileName(
            self, "选择备份文件", "", "ZIP文件 (*.zip)"
        )

        if backup_path:
            confirm = QMessageBox.question(
                self,
                "确认恢复",
                "恢复数据将覆盖当前数据库，确定继续？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    DataBackup.restore(backup_path)
                    QMessageBox.information(
                        self, "恢复成功", "数据恢复成功！请重启应用"
                    )
                    Logger.info(f"用户 {self.user['username']} 执行数据恢复")
                except Exception as e:
                    QMessageBox.critical(self, "恢复失败", f"数据恢复失败: {str(e)}")
                    Logger.error(f"数据恢复失败: {str(e)}")

    def handle_change_password(self):
        dialog = ChangePasswordDialog(self, self.user)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "修改成功", "密码修改成功，请重新登录")
            self.close()

    def handle_about(self):
        QMessageBox.information(
            self,
            "关于",
            "极简库存管理系统 v1.0.0\n\n专为小微企业和小型仓库设计的单机轻量化库存管理工具。",
        )

    def closeEvent(self, event):
        confirm = QMessageBox.question(
            self,
            "确认退出",
            "确定要退出系统吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            Logger.info(f"用户 {self.user['username']} 退出系统")
            event.accept()
        else:
            event.ignore()
