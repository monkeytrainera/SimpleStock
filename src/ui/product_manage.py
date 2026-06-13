from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from src.business.product_service import ProductService
from src.ui.ui_utils import (
    create_button,
    create_button_layout,
    create_cancel_button,
    create_line_edit,
    create_search_layout,
    create_standard_layout,
    create_table_widget,
)


class ProductManageWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = create_standard_layout()

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.add_btn = create_button("新增商品")
        self.add_btn.clicked.connect(self.handle_add)
        header_layout.addWidget(self.add_btn)

        layout.addLayout(header_layout)

        self.search_edit, search_layout = create_search_layout()
        self.search_edit.textChanged.connect(self.handle_search)
        layout.addLayout(search_layout)

        self.table = create_table_widget(
            ["商品名称", "规格", "单位", "当前库存", "操作"]
        )
        layout.addWidget(self.table)

        self.setLayout(layout)

    def refresh_data(self, keyword=""):
        try:
            products = ProductService.search_products(keyword)
            self.table.setRowCount(len(products))

            for row, product in enumerate(products):
                self.table.setItem(row, 0, QTableWidgetItem(product["name"]))
                self.table.setItem(row, 1, QTableWidgetItem(product["spec"] or ""))
                self.table.setItem(row, 2, QTableWidgetItem(product["unit"]))
                self.table.setItem(row, 3, QTableWidgetItem(str(product["quantity"])))

                from src.ui.ui_utils import create_action_buttons

                btn_widget = create_action_buttons(
                    self.handle_edit, self.handle_delete, product
                )
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
            self,
            "确认删除",
            f"确定要删除商品 '{product['name']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                ProductService.delete_product(product["id"])
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

        layout = create_standard_layout((20, 20, 20, 20), 15)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.name_edit = create_line_edit("请输入商品名称")
        self.spec_edit = create_line_edit("请输入规格型号")
        self.unit_edit = create_line_edit("请输入单位")
        self.quantity_edit = create_line_edit("请输入初始库存")
        self.remark_edit = create_line_edit("请输入备注")

        form_layout.addRow("商品名称 *", self.name_edit)
        form_layout.addRow("规格", self.spec_edit)
        form_layout.addRow("单位 *", self.unit_edit)
        form_layout.addRow("初始库存 *", self.quantity_edit)
        form_layout.addRow("备注", self.remark_edit)

        layout.addLayout(form_layout)

        ok_btn = create_button("保存")
        ok_btn.clicked.connect(self.handle_ok)

        cancel_btn = create_cancel_button()
        cancel_btn.clicked.connect(self.reject)

        button_layout = create_button_layout([ok_btn, cancel_btn])
        layout.addLayout(button_layout)

        self.setLayout(layout)

        if self.product:
            self.name_edit.setText(self.product["name"])
            self.spec_edit.setText(self.product["spec"] or "")
            self.unit_edit.setText(self.product["unit"])
            self.quantity_edit.setText(str(self.product["initial_quantity"]))
            self.remark_edit.setText(self.product["remark"] or "")
            self.quantity_edit.setEnabled(False)

    def handle_ok(self):
        name = self.name_edit.text().strip()
        spec = self.spec_edit.text().strip()
        unit = self.unit_edit.text().strip()
        remark = self.remark_edit.text().strip()

        try:
            quantity = (
                int(self.quantity_edit.text()) if self.quantity_edit.text() else 0
            )
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
                ProductService.update_product(
                    self.product["id"], name, spec, unit, remark
                )
            else:
                ProductService.add_product(name, spec, unit, quantity, remark)

            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "错误", str(e))
