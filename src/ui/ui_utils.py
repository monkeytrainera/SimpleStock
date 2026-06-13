"""UI工具函数模块 - 封装重复的UI组件创建逻辑"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


def create_button(
    text: str,
    color: str = "#1E88E5",
    hover_color: str = "#1565C0",
    width: int = 100,
    height: int = 32,
) -> QPushButton:
    """创建标准按钮"""
    button = QPushButton(text)
    button.setFixedSize(width, height)
    button.setStyleSheet(f"""
        QPushButton {{
            padding: 8px 20px;
            background-color: {color};
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        """)
    return button


def create_cancel_button(text: str = "取消") -> QPushButton:
    """创建取消按钮"""
    button = QPushButton(text)
    button.setStyleSheet("""
        QPushButton {
            padding: 8px 20px;
            background-color: #F5F5F5;
            color: #333;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #E8E8E8;
        }
        """)
    return button


def create_line_edit(placeholder: str = "", min_width: int = 200) -> QLineEdit:
    """创建标准输入框"""
    edit = QLineEdit()
    edit.setPlaceholderText(placeholder)
    edit.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #1E88E5;
            outline: none;
        }
        """)
    if min_width > 0:
        edit.setMinimumWidth(min_width)
    return edit


def create_search_edit() -> QLineEdit:
    """创建搜索输入框"""
    edit = QLineEdit()
    edit.setPlaceholderText("输入关键词搜索")
    edit.setStyleSheet("""
        QLineEdit {
            padding: 8px;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            font-size: 14px;
            min-width: 200px;
        }
        """)
    return edit


def create_table_widget(columns: list) -> QTableWidget:
    """创建标准表格"""
    table = QTableWidget()
    table.setColumnCount(len(columns))
    table.setHorizontalHeaderLabels(columns)
    table.setStyleSheet("""
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
    header = table.horizontalHeader()
    if header:
        header.setStretchLastSection(True)
    return table


def create_button_layout(
    buttons: list, alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignRight
) -> QHBoxLayout:
    """创建按钮布局"""
    layout = QHBoxLayout()
    layout.setSpacing(10)
    layout.setAlignment(alignment)
    for button in buttons:
        layout.addWidget(button)
    return layout


def create_standard_layout(
    margins: tuple = (16, 16, 16, 16), spacing: int = 16
) -> QVBoxLayout:
    """创建标准垂直布局"""
    layout = QVBoxLayout()
    layout.setContentsMargins(*margins)
    layout.setSpacing(spacing)
    return layout


def create_search_layout() -> tuple:
    """创建搜索布局，返回(search_edit, search_layout)"""
    search_layout = QHBoxLayout()
    search_layout.setSpacing(10)

    search_label = QLabel("搜索:")
    search_label.setStyleSheet("font-size: 14px;")

    search_edit = create_search_edit()

    search_layout.addWidget(search_label)
    search_layout.addWidget(search_edit)
    search_layout.addStretch()

    return search_edit, search_layout


def create_action_buttons(edit_callback, delete_callback, row_data):
    """创建操作按钮组（编辑和删除）"""
    edit_btn = QPushButton("编辑")
    edit_btn.setFixedSize(50, 24)
    edit_btn.setStyleSheet("""
        QPushButton {
            padding: 2px 8px;
            background-color: #FF9800;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #F57C00;
        }
        """)
    edit_btn.clicked.connect(lambda checked, p=row_data: edit_callback(p))

    delete_btn = QPushButton("删除")
    delete_btn.setFixedSize(50, 24)
    delete_btn.setStyleSheet("""
        QPushButton {
            padding: 2px 8px;
            background-color: #F44336;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #D32F2F;
        }
        """)
    delete_btn.clicked.connect(lambda checked, p=row_data: delete_callback(p))

    btn_layout = QHBoxLayout()
    btn_layout.setContentsMargins(0, 2, 0, 2)
    btn_layout.setSpacing(6)
    btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    btn_layout.addWidget(edit_btn)
    btn_layout.addWidget(delete_btn)

    btn_widget = QWidget()
    btn_widget.setLayout(btn_layout)

    return btn_widget
