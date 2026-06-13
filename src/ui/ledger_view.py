from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QDateEdit,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from src.business.stock_service import StockService
from src.ui.ui_utils import (
    create_button,
    create_search_layout,
    create_standard_layout,
    create_table_widget,
)


class LedgerViewWidget(QWidget):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = create_standard_layout()

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.export_btn = create_button("导出报表", "#4CAF50", "#388E3C")
        self.export_btn.clicked.connect(self.handle_export)
        header_layout.addWidget(self.export_btn)

        layout.addLayout(header_layout)

        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)

        start_label = QLabel("开始日期:")
        start_label.setStyleSheet("font-size: 14px;")
        self.start_date_edit = QDateEdit(QDate.currentDate().addDays(-30))
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.start_date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
            """)

        end_label = QLabel("结束日期:")
        end_label.setStyleSheet("font-size: 14px;")
        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
            """)

        search_btn = create_button("查询", "#607D8B", "#546E7A", 80)
        search_btn.clicked.connect(self.handle_search)

        date_layout.addWidget(start_label)
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(end_label)
        date_layout.addWidget(self.end_date_edit)
        date_layout.addWidget(search_btn)
        date_layout.addStretch()

        layout.addLayout(date_layout)

        self.search_edit, search_layout = create_search_layout()
        self.search_edit.textChanged.connect(self.handle_search)
        layout.addLayout(search_layout)

        self.table = create_table_widget(
            ["日期", "商品名称", "类型", "数量", "操作员", "备注"]
        )
        layout.addWidget(self.table)

        self.setLayout(layout)

    def refresh_data(self, keyword=""):
        try:
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
            records = StockService.get_stock_records(start_date, end_date, keyword)
            self.table.setRowCount(len(records))

            for row, record in enumerate(records):
                self.table.setItem(row, 0, QTableWidgetItem(record["created_at"]))
                self.table.setItem(row, 1, QTableWidgetItem(record["product_name"]))
                type_text = (
                    record["type"] if record["type"] in ["入库", "出库"] else "未知"
                )
                self.table.setItem(row, 2, QTableWidgetItem(type_text))
                self.table.setItem(row, 3, QTableWidgetItem(str(record["quantity"])))
                self.table.setItem(row, 4, QTableWidgetItem(record["operator"]))
                self.table.setItem(row, 5, QTableWidgetItem(record["remark"] or ""))

            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def handle_search(self, keyword=""):
        self.refresh_data(keyword)

    def handle_export(self):
        try:
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")

            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出报表", "", "Excel文件 (*.xlsx)"
            )

            if file_path:
                StockService.export_records_to_excel(start_date, end_date, file_path)
                QMessageBox.information(self, "导出成功", "报表导出成功")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", str(e))
