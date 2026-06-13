from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QLabel,
    QMessageBox,
    QVBoxLayout,
)

from src.business.product_service import ProductService
from src.business.stock_service import StockService
from src.ui.ui_utils import (
    create_button,
    create_button_layout,
    create_cancel_button,
    create_line_edit,
    create_standard_layout,
)


class StockInDialog(QDialog):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        self.load_products()

    def init_ui(self):
        self.setWindowTitle("商品入库")
        self.setFixedSize(400, 350)

        layout = create_standard_layout((20, 20, 20, 20), 15)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.product_combo = QComboBox()
        self.product_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
                min-width: 200px;
            }
            """)
        self.product_combo.currentIndexChanged.connect(self.update_stock_label)

        form_layout.addRow("商品 *", self.product_combo)

        self.quantity_edit = create_line_edit("请输入入库数量")

        self.stock_label = QLabel("当前库存: 0")
        self.stock_label.setStyleSheet("color: #666; font-size: 12px;")

        quantity_layout = QVBoxLayout()
        quantity_layout.addWidget(self.quantity_edit)
        quantity_layout.addWidget(self.stock_label)

        form_layout.addRow("入库数量 *", quantity_layout)

        self.remark_edit = create_line_edit("请输入备注（可选）")

        form_layout.addRow("备注", self.remark_edit)

        layout.addLayout(form_layout)

        ok_btn = create_button("确认入库")
        ok_btn.clicked.connect(self.handle_ok)

        cancel_btn = create_cancel_button()
        cancel_btn.clicked.connect(self.reject)

        button_layout = create_button_layout([ok_btn, cancel_btn])
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_products(self):
        try:
            products = ProductService.get_all_products()
            self.product_combo.clear()
            for product in products:
                self.product_combo.addItem(product["name"], product)
            if products:
                self.update_stock_label()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def update_stock_label(self):
        index = self.product_combo.currentIndex()
        if index >= 0:
            product = self.product_combo.itemData(index)
            self.stock_label.setText(f"当前库存: {product['quantity']}")

    def handle_ok(self):
        index = self.product_combo.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "错误", "请选择商品")
            return

        try:
            quantity = int(self.quantity_edit.text())
        except ValueError:
            QMessageBox.warning(self, "错误", "入库数量必须是数字")
            return

        if quantity <= 0:
            QMessageBox.warning(self, "错误", "入库数量必须大于0")
            return

        product = self.product_combo.itemData(index)
        remark = self.remark_edit.text().strip()

        try:
            StockService.stock_in(product["id"], quantity, remark, self.user["id"])
            QMessageBox.information(
                self, "入库成功", f"成功入库 {quantity} {product['unit']}"
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "入库失败", str(e))
