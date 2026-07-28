"""
Button factory for creating calculator buttons with consistent styling.
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont

from styles import get_theme
from translations import t


class CalculatorButton(QPushButton):
    """
    Enhanced calculator button with:
    - Hover effects
    - Click animations
    - Tooltip support
    - Theme support
    """

    # Custom signal with button text
    button_clicked = pyqtSignal(str)

    def __init__(self, text: str, btn_type: str, tooltip: str = "", parent=None):
        super().__init__(text, parent)

        self.btn_type = btn_type
        self.original_text = text
        self._scale = 1.0

        self._init_ui(tooltip)
        self.apply_theme()

        # Connect click
        self.clicked.connect(lambda: self._on_clicked())

    def _init_ui(self, tooltip: str):
        """Initialize button UI."""
        self.setFont(QFont("Arial", 18, QFont.Bold))
        self.setMinimumSize(70, 70)
        self.setCursor(Qt.PointingHandCursor)

        if tooltip:
            self.setToolTip(tooltip)

        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)

    def apply_theme(self):
        """Apply current theme styling."""
        theme = get_theme()
        self.setStyleSheet(theme.get_button_style(self.btn_type))

    def _on_clicked(self):
        """Handle button click with animation."""
        self._animate_click()
        self.button_clicked.emit(self.original_text)

    def _animate_click(self):
        """Subtle scale animation on click."""
        self.animation = QPropertyAnimation(self, b"scale")
        self.animation.setDuration(100)
        self.animation.setStartValue(1.0)
        self.animation.setKeyValueAt(0.5, 0.95)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    # Scale property for animation
    def get_scale(self):
        return self._scale

    def set_scale(self, value):
        self._scale = value
        size = int(70 * value)
        self.setMinimumSize(size, size)

    scale = pyqtProperty(float, get_scale, set_scale)


class ButtonFactory:
    """Factory for creating calculator buttons."""

    @staticmethod
    def create_button(text: str, btn_type: str, tooltip: str = "") -> CalculatorButton:
        """
        Create a calculator button.

        Args:
            text: Button display text
            btn_type: Type of button (number, operator, etc.)
            tooltip: Tooltip text

        Returns:
            Configured CalculatorButton instance
        """
        # Translate tooltip if available
        translated_tooltip = t(tooltip) if tooltip else ""

        return CalculatorButton(text, btn_type, translated_tooltip)

    @staticmethod
    def create_from_config(button_info) -> CalculatorButton:
        """
        Create button from ButtonInfo config object.

        Args:
            button_info: ButtonInfo instance from config

        Returns:
            Configured CalculatorButton
        """
        return ButtonFactory.create_button(
            button_info.text,
            button_info.btn_type,
            button_info.tooltip
        )
