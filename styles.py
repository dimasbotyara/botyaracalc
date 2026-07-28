"""
Styling system for calculator.
Provides light and dark themes with smooth transitions.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorScheme:
    """Color scheme for theme."""
    # Background colors
    window_bg: str
    display_bg: str
    button_number_bg: str
    button_operator_bg: str
    button_function_bg: str
    button_clear_bg: str
    button_equals_bg: str

    # Hover colors
    button_number_hover: str
    button_operator_hover: str
    button_function_hover: str
    button_clear_hover: str
    button_equals_hover: str

    # Pressed colors
    button_number_pressed: str
    button_operator_pressed: str
    button_function_pressed: str
    button_clear_pressed: str
    button_equals_pressed: str

    # Text colors
    display_text: str
    expression_text: str
    button_text: str
    button_operator_text: str

    # Border colors
    display_border: str
    button_border: str

    # History panel
    history_bg: str
    history_text: str
    history_item_hover: str


# Light theme (modern iOS-style)
LIGHT_THEME = ColorScheme(
    window_bg="#f5f5f5",
    display_bg="#ffffff",
    button_number_bg="#e8e8e8",
    button_operator_bg="#ff9f0a",
    button_function_bg="#a0a0a0",
    button_clear_bg="#ff3b30",
    button_equals_bg="#34c759",

    button_number_hover="#d8d8d8",
    button_operator_hover="#ff9500",
    button_function_hover="#909090",
    button_clear_hover="#ff2d24",
    button_equals_hover="#30b350",

    button_number_pressed="#c8c8c8",
    button_operator_pressed="#e68a00",
    button_function_pressed="#808080",
    button_clear_pressed="#e51e14",
    button_equals_pressed="#28a745",

    display_text="#000000",
    expression_text="#666666",
    button_text="#000000",
    button_operator_text="#ffffff",

    display_border="#d1d1d1",
    button_border="none",

    history_bg="#ffffff",
    history_text="#333333",
    history_item_hover="#f0f0f0",
)

# Dark theme (modern macOS-style)
DARK_THEME = ColorScheme(
    window_bg="#1e1e1e",
    display_bg="#2d2d2d",
    button_number_bg="#3a3a3a",
    button_operator_bg="#ff9f0a",
    button_function_bg="#505050",
    button_clear_bg="#ff453a",
    button_equals_bg="#32d74b",

    button_number_hover="#454545",
    button_operator_hover="#ffa929",
    button_function_hover="#5a5a5a",
    button_clear_hover="#ff5449",
    button_equals_hover="#41e65a",

    button_number_pressed="#505050",
    button_operator_pressed="#e69500",
    button_function_pressed="#656565",
    button_clear_pressed="#e63f34",
    button_equals_pressed="#2dc645",

    display_text="#ffffff",
    expression_text="#a0a0a0",
    button_text="#ffffff",
    button_operator_text="#ffffff",

    display_border="#3a3a3a",
    button_border="none",

    history_bg="#2d2d2d",
    history_text="#e0e0e0",
    history_item_hover="#3a3a3a",
)


class ThemeManager:
    """Manages application themes."""

    THEMES: Dict[str, ColorScheme] = {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
    }

    def __init__(self, initial_theme: str = "light"):
        self.current_theme_name = initial_theme
        self.current_theme = self.THEMES.get(initial_theme, LIGHT_THEME)

    def set_theme(self, theme_name: str):
        """Change current theme."""
        if theme_name in self.THEMES:
            self.current_theme_name = theme_name
            self.current_theme = self.THEMES[theme_name]

    def get_window_style(self) -> str:
        """Get QSS for main window."""
        return f"""
            QWidget {{
                background-color: {self.current_theme.window_bg};
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            }}
        """

    def get_display_style(self, is_main: bool = True) -> str:
        """Get QSS for display."""
        font_size = 32 if is_main else 14
        text_color = self.current_theme.display_text if is_main else self.current_theme.expression_text

        return f"""
            QLineEdit {{
                background-color: {self.current_theme.display_bg};
                border: 2px solid {self.current_theme.display_border};
                border-radius: 8px;
                padding: 10px 15px;
                color: {text_color};
                font-size: {font_size}px;
                font-weight: {'bold' if is_main else 'normal'};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.current_theme.button_operator_bg};
            }}
        """

    def get_button_style(self, button_type: str) -> str:
        """Get QSS for button based on type."""
        # Map button type to colors
        color_map = {
            "number": (
                self.current_theme.button_number_bg,
                self.current_theme.button_number_hover,
                self.current_theme.button_number_pressed,
                self.current_theme.button_text
            ),
            "operator": (
                self.current_theme.button_operator_bg,
                self.current_theme.button_operator_hover,
                self.current_theme.button_operator_pressed,
                self.current_theme.button_operator_text
            ),
            "function": (
                self.current_theme.button_function_bg,
                self.current_theme.button_function_hover,
                self.current_theme.button_function_pressed,
                self.current_theme.button_operator_text
            ),
            "clear": (
                self.current_theme.button_clear_bg,
                self.current_theme.button_clear_hover,
                self.current_theme.button_clear_pressed,
                self.current_theme.button_operator_text
            ),
            "equals": (
                self.current_theme.button_equals_bg,
                self.current_theme.button_equals_hover,
                self.current_theme.button_equals_pressed,
                self.current_theme.button_operator_text
            ),
            "special": (
                self.current_theme.button_number_bg,
                self.current_theme.button_number_hover,
                self.current_theme.button_number_pressed,
                self.current_theme.button_text
            ),
        }

        bg, hover, pressed, text = color_map.get(button_type, color_map["number"])

        return f"""
            QPushButton {{
                background-color: {bg};
                color: {text};
                border: {self.current_theme.button_border};
                border-radius: 20px;
                font-size: 20px;
                font-weight: 500;
                min-width: 70px;
                min-height: 70px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """

    def get_history_style(self) -> str:
        """Get QSS for history panel."""
        return f"""
            QListWidget {{
                background-color: {self.current_theme.history_bg};
                border: 1px solid {self.current_theme.display_border};
                border-radius: 8px;
                color: {self.current_theme.history_text};
                font-size: 14px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            QListWidget::item:hover {{
                background-color: {self.current_theme.history_item_hover};
            }}
        """


# Global theme manager
_theme_manager = ThemeManager()


def get_theme() -> ThemeManager:
    """Get global theme manager."""
    return _theme_manager
