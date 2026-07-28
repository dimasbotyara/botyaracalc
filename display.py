"""
Display widget for calculator.
Shows current expression and result with animations.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont

from styles import get_theme
from config import MAX_DISPLAY_LENGTH


class CalculatorDisplay(QWidget):
    """
    Two-line display widget:
    - Top line: expression being entered
    - Bottom line: current result/value
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._opacity = 1.0
        self.theme = get_theme()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Expression display (small, top)
        self.expression_display = QLineEdit()
        self.expression_display.setAlignment(Qt.AlignRight)
        self.expression_display.setReadOnly(True)
        self.expression_display.setPlaceholderText("")
        self.expression_display.setMinimumHeight(40)
        self.expression_display.setFont(QFont("Arial", 14))
        self.expression_display.setFrame(False)

        # Main display (large, bottom)
        self.main_display = QLineEdit()
        self.main_display.setAlignment(Qt.AlignRight)
        self.main_display.setReadOnly(True)
        self.main_display.setPlaceholderText("0")
        self.main_display.setMinimumHeight(70)
        self.main_display.setFont(QFont("Arial", 32, QFont.Bold))

        layout.addWidget(self.expression_display)
        layout.addWidget(self.main_display)

        self.setLayout(layout)
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to display."""
        self.expression_display.setStyleSheet(
            self.theme.get_display_style(is_main=False)
        )
        self.main_display.setStyleSheet(
            self.theme.get_display_style(is_main=True)
        )

    def set_expression(self, text: str):
        """Set expression text (top line)."""
        self.expression_display.setText(text)

    def set_value(self, text: str):
        """Set main value (bottom line)."""
        # Truncate if too long
        if len(text) > MAX_DISPLAY_LENGTH:
            text = text[:MAX_DISPLAY_LENGTH - 3] + "..."

        self.main_display.setText(text)

    def get_value(self) -> str:
        """Get current main display value."""
        return self.main_display.text()

    def get_expression(self) -> str:
        """Get current expression."""
        return self.expression_display.text()

    def clear(self):
        """Clear both displays."""
        self.expression_display.clear()
        self.main_display.clear()

    def clear_expression(self):
        """Clear only expression display."""
        self.expression_display.clear()

    def show_error(self, error_message: str):
        """
        Show error message with animation.

        Args:
            error_message: Error text to display
        """
        self.set_value(error_message)
        self._animate_shake()

    def flash_result(self):
        """Flash display when showing result."""
        self._animate_flash()

    # === Animations ===

    def _animate_shake(self):
        """Shake animation for errors."""
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutBounce)

        original_pos = self.pos()

        self.animation.setKeyValueAt(0, original_pos)
        self.animation.setKeyValueAt(0.2, original_pos + Qt.QPoint(-10, 0))
        self.animation.setKeyValueAt(0.4, original_pos + Qt.QPoint(10, 0))
        self.animation.setKeyValueAt(0.6, original_pos + Qt.QPoint(-10, 0))
        self.animation.setKeyValueAt(0.8, original_pos + Qt.QPoint(10, 0))
        self.animation.setKeyValueAt(1, original_pos)

        self.animation.start()

    def _animate_flash(self):
        """Flash animation for results."""
        self.animation = QPropertyAnimation(self, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.3)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    # Property for animation
    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)

    def copy_to_clipboard(self):
        """Copy current value to clipboard."""
        from PyQt5.QtWidgets import QApplication

        value = self.get_value()
        if value and value not in ["0", ""]:
            clipboard = QApplication.clipboard()
            clipboard.setText(value)
            return True
        return False
