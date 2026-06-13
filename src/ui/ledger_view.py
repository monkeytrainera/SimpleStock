from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDateEdit, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt, QDate
from src.business.stock_service import StockService
from src.utils.excel_exporter import ExcelExporter

class LedgerViewWidget(QWidget):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel("台账报表")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        
        self.export_btn = QPushButton("导出Excel")
        self.export_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.export_btn.clicked.connect(self.handle_export)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.export_btn)
        
        layout.addLayout(header_layout)
        
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        start_label = QLabel("日期范围:")
        start_label.setStyleSheet("font-size: 14px;")
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))
        self.start_date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        
        to_label = QLabel("至")
        to_label.setStyleSheet("font-size: 14px;")
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        
        self.query_btn = QPushButton("查询")
        self.query_btn.setStyleSheet("""
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
        self.query_btn.clicked.connect(self.handle_query)
        
        filter_layout.addWidget(start_label)
        filter_layout.addWidget(self.start_date_edit)
        filter_layout.addWidget(to_label)
        filter_layout.addWidget(self.end_date_edit)
        filter_layout.addWidget(self.query_btn)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["时间", "类型", "商品名称", "数量", "操作人"])
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def refresh_data(self, start_date=None, end_date=None):
        try:
            records = StockService.get_all_records(start_date, end_date)
            self.table.setRowCount(len(records))
            
            for row, record in enumerate(records):
                self.table.setItem(row, 0, QTableWidgetItem(record['created_at']))
                
                type_item = QTableWidgetItem(record['type'])
                if record['type'] == '入库':
                    type_item.setForeground(Qt.GlobalColor.green)
                else:
                    type_item.setForeground(Qt.GlobalColor.red)
                self.table.setItem(row, 1, type_item)
                
                self.table.setItem(row, 2, QTableWidgetItem(record['product_name']))
                
                qty = f"+{record['quantity']}" if record['type'] == '入库' else f"-{record['quantity']}"
                qty_item = QTableWidgetItem(qty)
                if record['type'] == '入库':
                    qty_item.setForeground(Qt.GlobalColor.green)
                else:
                    qty_item.setForeground(Qt.GlobalColor.red)
                self.table.setItem(row, 3, qty_item)
                
                self.table.setItem(row, 4, QTableWidgetItem(record['operator_name']))
            
            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))
    
    def handle_query(self):
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd 00:00:00")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd 23:59:59")
        self.refresh_data(start_date, end_date)
    
    def handle_export(self):
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd 00:00:00")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd 23:59:59")
        
        try:
            records = StockService.get_all_records(start_date, end_date)
            
            if not records:
                QMessageBox.warning(self, "提示", "没有可导出的数据")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存Excel文件", "", "Excel文件 (*.xlsx)"
            )
            
            if file_path:
                ExcelExporter.export_ledger(records, file_path)
                QMessageBox.information(self, "导出成功", f"Excel文件已保存到:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", str(e))
