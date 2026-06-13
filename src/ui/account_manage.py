from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from src.business.account_service import AccountService
from src.ui.ui_utils import (
    create_button,
    create_button_layout,
    create_cancel_button,
    create_line_edit,
    create_search_layout,
    create_standard_layout,
    create_table_widget,
)


class AccountManageWidget(QWidget):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = create_standard_layout()

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.add_btn = create_button("新增用户")
        self.add_btn.clicked.connect(self.handle_add)
        header_layout.addWidget(self.add_btn)

        layout.addLayout(header_layout)

        self.search_edit, search_layout = create_search_layout()
        self.search_edit.textChanged.connect(self.handle_search)
        layout.addLayout(search_layout)

        self.table = create_table_widget(["用户名", "角色", "操作"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def refresh_data(self, keyword=""):
        try:
            users = AccountService.search_users(keyword)
            self.table.setRowCount(len(users))

            for row, user in enumerate(users):
                self.table.setItem(row, 0, QTableWidgetItem(user["username"]))
                role_text = "管理员" if user["is_admin"] else "操作员"
                self.table.setItem(row, 1, QTableWidgetItem(role_text))

                from src.ui.ui_utils import create_action_buttons

                btn_widget = create_action_buttons(
                    self.handle_edit, self.handle_delete, user
                )
                self.table.setCellWidget(row, 2, btn_widget)

            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def handle_search(self, keyword):
        self.refresh_data(keyword)

    def handle_add(self):
        dialog = AccountFormDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def handle_edit(self, user):
        if user["username"] == self.user["username"]:
            dialog = AccountFormDialog(self, user, True)
        else:
            dialog = AccountFormDialog(self, user)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def handle_delete(self, user):
        if user["username"] == self.user["username"]:
            QMessageBox.warning(self, "警告", "不能删除当前登录用户")
            return

        confirm = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除用户 '{user['username']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                AccountService.delete_user(user["id"])
                QMessageBox.information(self, "删除成功", "用户删除成功")
                self.refresh_data()
            except ValueError as e:
                QMessageBox.warning(self, "删除失败", str(e))


class AccountFormDialog(QDialog):
    def __init__(self, parent, user=None, is_self=False):
        super().__init__(parent)
        self.user = user
        self.is_self = is_self
        self.init_ui()

    def init_ui(self):
        if self.user:
            self.setWindowTitle("编辑用户")
        else:
            self.setWindowTitle("新增用户")

        self.setFixedSize(400, 320)

        layout = create_standard_layout((20, 20, 20, 20), 15)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.username_edit = create_line_edit("请输入用户名")
        self.password_edit = create_line_edit("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_edit = create_line_edit("请再次输入密码")
        self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("用户名 *", self.username_edit)
        form_layout.addRow("密码 *", self.password_edit)
        form_layout.addRow("确认密码 *", self.confirm_edit)

        layout.addLayout(form_layout)

        ok_btn = create_button("保存")
        ok_btn.clicked.connect(self.handle_ok)

        cancel_btn = create_cancel_button()
        cancel_btn.clicked.connect(self.reject)

        button_layout = create_button_layout([ok_btn, cancel_btn])
        layout.addLayout(button_layout)

        self.setLayout(layout)

        if self.user:
            self.username_edit.setText(self.user["username"])
            if self.is_self:
                self.username_edit.setEnabled(False)
            else:
                self.username_edit.setEnabled(False)
                self.password_edit.setPlaceholderText("留空则不修改密码")
                self.confirm_edit.setPlaceholderText("留空则不修改密码")

    def handle_ok(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        confirm = self.confirm_edit.text()

        if not username:
            QMessageBox.warning(self, "错误", "用户名不能为空")
            return

        if self.user and not password:
            try:
                AccountService.update_user(self.user["id"], username, None)
                self.accept()
                return
            except ValueError as e:
                QMessageBox.warning(self, "错误", str(e))
                return

        if not password:
            QMessageBox.warning(self, "错误", "密码不能为空")
            return

        if password != confirm:
            QMessageBox.warning(self, "错误", "两次输入的密码不一致")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "错误", "密码长度不能少于6位")
            return

        try:
            if self.user:
                AccountService.update_user(self.user["id"], username, password)
            else:
                AccountService.add_user(username, password)

            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "错误", str(e))
