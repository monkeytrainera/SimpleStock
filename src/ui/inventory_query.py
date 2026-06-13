from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QTableWidgetItem,
    QWidget,
)

from src.business.product_service import ProductService
from src.ui.ui_utils import (
    create_search_layout,
    create_standard_layout,
    create_table_widget,
)


class InventoryQueryWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = create_standard_layout()

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(header_layout)

        self.search_edit, search_layout = create_search_layout()
        self.search_edit.textChanged.connect(self.handle_search)
        layout.addLayout(search_layout)

        self.table = create_table_widget(["商品名称", "规格", "单位", "当前库存"])
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

            self.table.resizeColumnsToContents()
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(self, "错误", str(e))

    def handle_search(self, keyword):
        self.refresh_data(keyword)
