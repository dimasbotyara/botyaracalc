"""
Localization system for calculator.
Supports English and Russian languages.
"""

from enum import Enum


class Language(Enum):
    """Supported languages."""
    ENGLISH = "en"
    RUSSIAN = "ru"


class Translations:
    """Translation manager."""

    _translations = {
        Language.ENGLISH: {
            # Window titles
            "app_title": "Calculator",
            "history_title": "History",
            "settings_title": "Settings",
            "language_select": "Select Language",

            # Buttons
            "clear": "Clear",
            "backspace": "Backspace",
            "equals": "Equals",
            "percent": "Percent",
            "square": "Square",
            "sqrt": "Square Root",
            "negate": "Change Sign",
            "open_paren": "Open Parenthesis",
            "close_paren": "Close Parenthesis",

            # Tooltips
            "tooltip_clear": "Clear all (Esc)",
            "tooltip_backspace": "Delete character (Backspace)",
            "tooltip_percent": "Percent",
            "tooltip_divide": "Division (/)",
            "tooltip_multiply": "Multiplication (*)",
            "tooltip_subtract": "Subtraction (-)",
            "tooltip_add": "Addition (+)",
            "tooltip_equals": "Calculate (Enter)",
            "tooltip_negate": "Change sign",
            "tooltip_decimal": "Decimal point",
            "tooltip_square": "Square number",
            "tooltip_sqrt": "Square root",
            "tooltip_open_paren": "Open parenthesis",
            "tooltip_close_paren": "Close parenthesis",

            # Errors
            "error_division_zero": "Division by zero",
            "error_invalid": "Invalid expression",
            "error_overflow": "Number too large",
            "error_math": "Math error",
            "error_complex": "Complex number",
            "error_undefined": "Undefined result",
            "error_negative_sqrt": "Square root of negative",

            # History
            "history_empty": "No history yet",
            "history_clear": "Clear History",
            "history_copied": "Copied to clipboard",

            # Settings
            "setting_theme": "Theme:",
            "setting_scientific": "Scientific Mode",
            "setting_sound": "Sound Effects",
            "theme_light": "Light",
            "theme_dark": "Dark",

            # Menu
            "menu_file": "File",
            "menu_edit": "Edit",
            "menu_view": "View",
            "menu_help": "Help",
            "menu_exit": "Exit",
            "menu_copy": "Copy",
            "menu_paste": "Paste",
            "menu_history": "Show History",
            "menu_settings": "Settings",
            "menu_about": "About",

            # Dialog
            "dialog_welcome": "Welcome to Calculator!",
            "dialog_select_lang": "Please select your language:",
            "dialog_ok": "OK",
            "dialog_cancel": "Cancel",

            # About
            "about_text": "Modern Calculator v2.0\n\nFeatures:\n• Basic arithmetic\n• Scientific functions\n• History tracking\n• Keyboard support\n• Dark/Light themes",
        },

        Language.RUSSIAN: {
            # Window titles
            "app_title": "Калькулятор",
            "history_title": "История",
            "settings_title": "Настройки",
            "language_select": "Выберите язык",

            # Buttons
            "clear": "Очистить",
            "backspace": "Удалить",
            "equals": "Равно",
            "percent": "Процент",
            "square": "Квадрат",
            "sqrt": "Корень",
            "negate": "Изменить знак",
            "open_paren": "Открыть скобку",
            "close_paren": "Закрыть скобку",

            # Tooltips
            "tooltip_clear": "Очистить всё (Esc)",
            "tooltip_backspace": "Удалить символ (Backspace)",
            "tooltip_percent": "Процент",
            "tooltip_divide": "Деление (/)",
            "tooltip_multiply": "Умножение (*)",
            "tooltip_subtract": "Вычитание (-)",
            "tooltip_add": "Сложение (+)",
            "tooltip_equals": "Вычислить (Enter)",
            "tooltip_negate": "Сменить знак",
            "tooltip_decimal": "Десятичная точка",
            "tooltip_square": "Квадрат числа",
            "tooltip_sqrt": "Квадратный корень",
            "tooltip_open_paren": "Открывающая скобка",
            "tooltip_close_paren": "Закрывающая скобка",

            # Errors
            "error_division_zero": "Деление на ноль",
            "error_invalid": "Некорректное выражение",
            "error_overflow": "Слишком большое число",
            "error_math": "Математическая ошибка",
            "error_complex": "Комплексное число",
            "error_undefined": "Неопределённый результат",
            "error_negative_sqrt": "Корень из отрицательного",

            # History
            "history_empty": "История пуста",
            "history_clear": "Очистить историю",
            "history_copied": "Скопировано в буфер",

            # Settings
            "setting_theme": "Тема:",
            "setting_scientific": "Научный режим",
            "setting_sound": "Звуковые эффекты",
            "theme_light": "Светлая",
            "theme_dark": "Тёмная",

            # Menu
            "menu_file": "Файл",
            "menu_edit": "Правка",
            "menu_view": "Вид",
            "menu_help": "Справка",
            "menu_exit": "Выход",
            "menu_copy": "Копировать",
            "menu_paste": "Вставить",
            "menu_history": "Показать историю",
            "menu_settings": "Настройки",
            "menu_about": "О программе",

            # Dialog
            "dialog_welcome": "Добро пожаловать в Калькулятор!",
            "dialog_select_lang": "Пожалуйста, выберите язык:",
            "dialog_ok": "ОК",
            "dialog_cancel": "Отмена",

            # About
            "about_text": "Современный Калькулятор v2.0\n\nВозможности:\n• Базовая арифметика\n• Научные функции\n• История вычислений\n• Поддержка клавиатуры\n• Тёмная/Светлая темы",
        }
    }

    def __init__(self, language: Language = Language.ENGLISH):
        self.current_language = language

    def get(self, key: str) -> str:
        """Get translated string by key."""
        return self._translations.get(
            self.current_language,
            self._translations[Language.ENGLISH]
        ).get(key, key)

    def set_language(self, language: Language):
        """Change current language."""
        self.current_language = language

    @property
    def language(self) -> Language:
        """Get current language."""
        return self.current_language


# Global translator instance
_translator = Translations()


def t(key: str) -> str:
    """Shortcut for translation."""
    return _translator.get(key)


def set_language(language: Language):
    """Set global language."""
    _translator.set_language(language)


def get_current_language() -> Language:
    """Get current language."""
    return _translator.language
