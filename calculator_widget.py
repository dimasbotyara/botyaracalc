"""
Main calculator widget combining display, buttons, and logic.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QHBoxLayout,
                             QPushButton, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QFont

from engine import CalculatorEngine, CalcError
from display import CalculatorDisplay
from button_factory import ButtonFactory
from history_panel import HistoryPanel
from styles import get_theme
from config import (BUTTON_LAYOUT, SCIENTIFIC_BUTTONS, KEY_TO_DISPLAY,
                   DISPLAY_TO_CALC, NUMBER, OPERATOR, FUNCTION, EQUALS,
                   CLEAR, SPECIAL)
from translations import t
from settings_manager import get_settings


class CalculatorWidget(QWidget):
    """
    Main calculator widget with all functionality.
    Manages interaction between display, buttons, and calculation engine.
    """

    # Signal when theme should be changed
    theme_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize engine and state
        self.engine = CalculatorEngine()
        self.settings = get_settings()
        self.theme = get_theme()

        self.current_expression = ""
        self.last_was_equals = False
        self.last_was_error = False

        self._init_ui()
        self._load_history()

    def _init_ui(self):
        """Initialize UI components."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create splitter for calculator and history
        self.splitter = QSplitter(Qt.Horizontal)

        # Left side: calculator
        calc_widget = QWidget()
        calc_layout = QVBoxLayout()
        calc_layout.setContentsMargins(0, 0, 0, 0)
        calc_layout.setSpacing(10)

        # Display
        self.display = CalculatorDisplay()
        calc_layout.addWidget(self.display)

        # Buttons grid
        self.button_grid = self._create_button_grid()
        calc_layout.addLayout(self.button_grid)

        # Scientific buttons (initially hidden)
        if self.settings.scientific_mode:
            self.scientific_grid = self._create_scientific_grid()
            calc_layout.insertLayout(1, self.scientific_grid)

        calc_widget.setLayout(calc_layout)
        self.splitter.addWidget(calc_widget)

        # Right side: history panel
        self.history_panel = HistoryPanel()
        self.history_panel.history_item_selected.connect(self._on_history_selected)
        self.splitter.addWidget(self.history_panel)

        # Set initial splitter sizes (calculator: 60%, history: 40%)
        self.splitter.setSizes([600, 400])
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, True)

        main_layout.addWidget(self.splitter)

        # Bottom toolbar (optional - memory buttons, etc.)
        self._create_toolbar(main_layout)

        self.setLayout(main_layout)
        self.apply_theme()

    def _create_button_grid(self) -> QGridLayout:
        """Create main button grid from config."""
        grid = QGridLayout()
        grid.setSpacing(8)

        self.buttons = {}

        for row_idx, row in enumerate(BUTTON_LAYOUT):
            for col_idx, button_info in enumerate(row):
                button = ButtonFactory.create_from_config(button_info)
                button.button_clicked.connect(self._on_button_clicked)

                grid.addWidget(
                    button,
                    row_idx,
                    col_idx,
                    button_info.span_rows,
                    button_info.span_cols
                )

                self.buttons[button_info.text] = button

        return grid

    def _create_scientific_grid(self) -> QGridLayout:
        """Create scientific mode buttons."""
        grid = QGridLayout()
        grid.setSpacing(8)

        for row_idx, row in enumerate(SCIENTIFIC_BUTTONS):
            for col_idx, button_info in enumerate(row):
                button = ButtonFactory.create_from_config(button_info)
                button.button_clicked.connect(self._on_button_clicked)

                grid.addWidget(button, row_idx, col_idx)
                self.buttons[button_info.text] = button

        return grid

    def _create_toolbar(self, parent_layout: QVBoxLayout):
        """Create bottom toolbar with memory and settings."""
        toolbar = QHBoxLayout()
        toolbar.setSpacing(5)

        # Memory indicator
        self.memory_label = QPushButton("M")
        self.memory_label.setFixedSize(30, 30)
        self.memory_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.memory_label.setVisible(False)
        self.memory_label.setStyleSheet(self._get_memory_indicator_style())
        toolbar.addWidget(self.memory_label)

        toolbar.addStretch()

        # Theme toggle button
        theme_button = QPushButton("🌓")
        theme_button.setFixedSize(40, 30)
        theme_button.setToolTip(t("setting_theme"))
        theme_button.setCursor(Qt.PointingHandCursor)
        theme_button.clicked.connect(self._toggle_theme)
        theme_button.setStyleSheet(self._get_toolbar_button_style())
        toolbar.addWidget(theme_button)

        # History toggle
        history_button = QPushButton("📜")
        history_button.setFixedSize(40, 30)
        history_button.setToolTip(t("menu_history"))
        history_button.setCursor(Qt.PointingHandCursor)
        history_button.clicked.connect(self._toggle_history)
        history_button.setStyleSheet(self._get_toolbar_button_style())
        toolbar.addWidget(history_button)

        parent_layout.addLayout(toolbar)

    def apply_theme(self):
        """Apply current theme to all components."""
        self.theme = get_theme()

        # Apply to display
        self.display.apply_theme()

        # Apply to all buttons
        for button in self.buttons.values():
            button.apply_theme()

        # Apply to history
        self.history_panel.apply_theme()

        # Apply to window background
        self.setStyleSheet(self.theme.get_window_style())

    def _on_button_clicked(self, text: str):
        """
        Handle all button clicks.

        Args:
            text: Text of clicked button
        """
        # Reset error state
        if self.last_was_error:
            self.current_expression = ""
            self.last_was_error = False

        # Handle different button types
        if text == "C":
            self._handle_clear()
        elif text == "⌫":
            self._handle_backspace()
        elif text == "=":
            self._handle_equals()
        elif text == "±":
            self._handle_negate()
        elif text in ["x²", "√", "%"]:
            self._handle_function(text)
        elif text in ["(", ")"]:
            self._handle_parenthesis(text)
        else:
            self._handle_input(text)

    def _handle_clear(self):
        """Clear display and expression."""
        self.current_expression = ""
        self.display.clear()
        self.last_was_equals = False

    def _handle_backspace(self):
        """Delete last character."""
        if self.last_was_equals or self.last_was_error:
            return

        current = self.display.get_value()
        if current:
            self.current_expression = current[:-1]
            self.display.set_value(self.current_expression)

    def _handle_input(self, text: str):
        """
        Handle number/operator input.

        Args:
            text: Input character
        """
        # If last action was equals, start fresh with operators
        if self.last_was_equals:
            if text in DISPLAY_TO_CALC:
                # Continue with operator
                self.current_expression = self.display.get_value() + text
            else:
                # Start new calculation
                self.current_expression = text
            self.last_was_equals = False
        else:
            self.current_expression += text

        self.display.set_value(self.current_expression)
        self.display.set_expression(self.current_expression)

    def _handle_equals(self):
        """Calculate result."""
        expression = self.current_expression

        if not expression:
            return

        # Calculate
        result = self.engine.calculate(expression)

        if result.is_success:
            # Show result
            self.display.set_value(result.value)
            self.display.set_expression(expression)
            self.display.flash_result()

            # Add to history
            self._add_to_history(expression, result.value)

            # Update state
            self.current_expression = result.value
            self.last_was_equals = True
        else:
            # Show error
            error_msg = self._get_error_message(result.error)
            self.display.show_error(error_msg)
            self.last_was_error = True

    def _handle_negate(self):
        """Change sign of current number."""
        current = self.display.get_value()
        if current and current != "0":
            negated = self.engine.negate(current)
            self.current_expression = negated
            self.display.set_value(negated)

    def _handle_function(self, func_name: str):
        """
        Apply mathematical function.

        Args:
            func_name: Function to apply (x², √, %)
        """
        current = self.display.get_value()
        if not current:
            current = "0"

        result = self.engine.apply_function(func_name, current)

        if result.is_success:
            expression = f"{func_name}({current})"
            self.display.set_value(result.value)
            self.display.set_expression(expression)

            self._add_to_history(expression, result.value)

            self.current_expression = result.value
            self.last_was_equals = True
        else:
            error_msg = self._get_error_message(result.error)
            self.display.show_error(error_msg)
            self.last_was_error = True

    def _handle_parenthesis(self, paren: str):
        """Handle parenthesis input."""
        self.current_expression += paren
        self.display.set_value(self.current_expression)

    def _add_to_history(self, expression: str, result: str):
        """Add calculation to history."""
        self.history_panel.add_item(expression, result)
        self.settings.add_to_history(expression, result)

    def _load_history(self):
        """Load history from settings."""
        history = self.settings.get_history()
        self.history_panel.set_history(history)

    def _on_history_selected(self, result: str):
        """Handle history item selection."""
        self.current_expression = result
        self.display.set_value(result)
        self.last_was_equals = False

    def _toggle_theme(self):
        """Toggle between light and dark theme."""
        current = self.settings.get_theme()
        new_theme = "dark" if current == "light" else "light"

        self.settings.set_theme(new_theme)
        self.theme.set_theme(new_theme)
        self.apply_theme()

        self.theme_changed.emit()

    def _toggle_history(self):
        """Toggle history panel visibility."""
        if self.history_panel.isVisible():
            self.history_panel.hide()
        else:
            self.history_panel.show()

    def _get_error_message(self, error: CalcError) -> str:
        """Get localized error message."""
        error_map = {
            CalcError.DIVISION_BY_ZERO: "error_division_zero",
            CalcError.INVALID_EXPRESSION: "error_invalid",
            CalcError.OVERFLOW: "error_overflow",
            CalcError.MATH_ERROR: "error_math",
        }

        key = error_map.get(error, "error_invalid")
        return t(key)

    def _get_memory_indicator_style(self) -> str:
        """Stylesheet for memory indicator."""
        return f"""
            QPushButton {{
                background-color: {self.theme.current_theme.button_function_bg};
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }}
        """

    def _get_toolbar_button_style(self) -> str:
        """Stylesheet for toolbar buttons."""
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 1px solid {self.theme.current_theme.display_border};
                border-radius: 4px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.current_theme.button_number_hover};
            }}
        """

    # === Keyboard handling ===

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input."""
        key = event.key()
        text = event.text()

        # Map keyboard to display characters
        if text in KEY_TO_DISPLAY:
            self._handle_input(KEY_TO_DISPLAY[text])
        elif text.isdigit() or text == ".":
            self._handle_input(text)
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self._handle_equals()
        elif key == Qt.Key_Escape:
            self._handle_clear()
        elif key == Qt.Key_Backspace:
            self._handle_backspace()
        elif event.modifiers() == Qt.ControlModifier:
            if key == Qt.Key_C:
                self.display.copy_to_clipboard()
            elif key == Qt.Key_H:
                self._toggle_history()
            elif key == Qt.Key_T:
                self._toggle_theme()
