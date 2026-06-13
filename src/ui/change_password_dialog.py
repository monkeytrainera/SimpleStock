from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
)

from src.business.account_service import AccountService
from src.ui.ui_utils import (
    create_button,
    create_button_layout,
    create_cancel_button,
    create_line_edit,
    create_standard_layout,
)


class ChangePasswordDialog(QDialog):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("修改密码")
        self.setFixedSize(400, 320)

        layout = create_standard_layout((20, 20, 20, 20), 15)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.old_password_edit = create_line_edit("请输入原密码")
        self.old_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.new_password_edit = create_line_edit("请输入新密码")
        self.new_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_edit = create_line_edit("请再次输入新密码")
        self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("原密码 *", self.old_password_edit)
        form_layout.addRow("新密码 *", self.new_password_edit)
        form_layout.addRow("确认密码 *", self.confirm_edit)

        layout.addLayout(form_layout)

        ok_btn = create_button("确认修改")
        ok_btn.clicked.connect(self.handle_ok)

        cancel_btn = create_cancel_button()
        cancel_btn.clicked.connect(self.reject)

        button_layout = create_button_layout([ok_btn, cancel_btn])
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_ok(self):
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm = self.confirm_edit.text()

        if not old_password:
            QMessageBox.warning(self, "错误", "原密码不能为空")
            return

        if not new_password:
            QMessageBox.warning(self, "错误", "新密码不能为空")
            return

        if new_password != confirm:
            QMessageBox.warning(self, "错误", "两次输入的新密码不一致")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "错误", "密码长度不能少于6位")
            return

        try:
            if not AccountService.verify_password(self.user["username"], old_password):
                QMessageBox.warning(self, "错误", "原密码不正确")
                return

            AccountService.update_user(
                self.user["id"], self.user["username"], new_password
            )
            QMessageBox.information(self, "修改成功", "密码修改成功")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "错误", str(e))
