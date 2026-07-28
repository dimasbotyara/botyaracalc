"""
History panel widget for displaying calculation history.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QPushButton, QLabel, QListWidgetItem, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

from styles import get_theme
from translations import t


class HistoryPanel(QWidget):
    """
    Scrollable panel showing calculation history.
    Allows clicking items to reuse them.
    """

    # Signal emitted when history item is clicked
    history_item_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = get_theme()
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel(t("history_title"))
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {self.theme.current_theme.display_text};")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Clear button
        self.clear_button = QPushButton(t("history_clear"))
        self.clear_button.setFont(QFont("Arial", 10))
        self.clear_button.setFixedHeight(30)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setStyleSheet(self._get_clear_button_style())
        self.clear_button.clicked.connect(self._on_clear_clicked)
        header_layout.addWidget(self.clear_button)

        layout.addLayout(header_layout)

        # History list
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Consolas", 12))
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)

        layout.addWidget(self.list_widget)

        # Empty state label
        self.empty_label = QLabel(t("history_empty"))
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setFont(QFont("Arial", 11, QFont.Italic))
        self.empty_label.setStyleSheet(f"color: {self.theme.current_theme.expression_text}; padding: 20px;")
        layout.addWidget(self.empty_label)

        self.setLayout(layout)
        self.apply_theme()
        self._update_empty_state()

    def apply_theme(self):
        """Apply current theme."""
        self.theme = get_theme()
        self.list_widget.setStyleSheet(self.theme.get_history_style())

        # Update labels
        if hasattr(self, 'empty_label'):
            self.empty_label.setStyleSheet(
                f"color: {self.theme.current_theme.expression_text}; padding: 20px;"
            )

    def add_item(self, expression: str, result: str):
        """
        Add calculation to history.

        Args:
            expression: The expression that was calculated
            result: The result of calculation
        """
        item_text = f"{expression} = {result}"

        # Don't add duplicates at the top
        if self.list_widget.count() > 0:
            first_item = self.list_widget.item(0)
            if first_item and first_item.text() == item_text:
                return

        # Insert at top
        item = QListWidgetItem(item_text)
        item.setData(Qt.UserRole, {"expression": expression, "result": result})
        self.list_widget.insertItem(0, item)

        self._update_empty_state()

    def set_history(self, history_items: list):
        """
        Set history from list of strings.

        Args:
            history_items: List of "expression = result" strings
        """
        self.list_widget.clear()

        for item_text in history_items:
            # Parse expression and result
            if " = " in item_text:
                parts = item_text.split(" = ", 1)
                expression = parts[0]
                result = parts[1] if len(parts) > 1 else ""

                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, {"expression": expression, "result": result})
                self.list_widget.addItem(item)

        self._update_empty_state()

    def get_history(self) -> list:
        """
        Get all history items as strings.

        Returns:
            List of "expression = result" strings
        """
        items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            items.append(item.text())
        return items

    def clear(self):
        """Clear all history."""
        self.list_widget.clear()
        self._update_empty_state()

    def _update_empty_state(self):
        """Show/hide empty state message."""
        is_empty = self.list_widget.count() == 0
        self.empty_label.setVisible(is_empty)
        self.list_widget.setVisible(not is_empty)
        self.clear_button.setEnabled(not is_empty)

    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle single click - show tooltip."""
        QApplication.clipboard().setText(item.text())
        # Could show a temporary tooltip here

    def _on_item_double_clicked(self, item: QListWidgetItem):
        """Handle double click - emit signal to use result."""
        data = item.data(Qt.UserRole)
        if data:
            result = data.get("result", "")
            if result:
                self.history_item_selected.emit(result)

    def _on_clear_clicked(self):
        """Handle clear button click."""
        self.clear()

    def _get_clear_button_style(self) -> str:
        """Get stylesheet for clear button."""
        return f"""
            QPushButton {{
                background-color: {self.theme.current_theme.button_clear_bg};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.theme.current_theme.button_clear_hover};
            }}
            QPushButton:pressed {{
                background-color: {self.theme.current_theme.button_clear_pressed};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """
