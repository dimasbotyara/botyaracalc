"""Конфигурация калькулятора: раскладка кнопок, горячие клавиши, константы."""

from dataclasses import dataclass, field


@dataclass
class ButtonInfo:
    """Информация о кнопке калькулятора."""
    text: str
    btn_type: str
    tooltip: str = ""
    span_cols: int = 1
    span_rows: int = 1


# Типы кнопок
NUMBER = "number"
OPERATOR = "operator"
FUNCTION = "function"
EQUALS = "equals"
CLEAR = "clear"
SPECIAL = "special"

# Раскладка кнопок (строки × столбцы)
BUTTON_LAYOUT: list[list[ButtonInfo]] = [
    # Ряд 0: функции
    [
        ButtonInfo("C", CLEAR, "Очистить всё (Esc)"),
        ButtonInfo("⌫", SPECIAL, "Удалить символ (Backspace)"),
        ButtonInfo("%", FUNCTION, "Процент"),
        ButtonInfo("÷", OPERATOR, "Деление (/)"),
    ],
    # Ряд 1
    [
        ButtonInfo("7", NUMBER),
        ButtonInfo("8", NUMBER),
        ButtonInfo("9", NUMBER),
        ButtonInfo("×", OPERATOR, "Умножение (*)"),
    ],
    # Ряд 2
    [
        ButtonInfo("4", NUMBER),
        ButtonInfo("5", NUMBER),
        ButtonInfo("6", NUMBER),
        ButtonInfo("−", OPERATOR, "Вычитание (-)"),
    ],
    # Ряд 3
    [
        ButtonInfo("1", NUMBER),
        ButtonInfo("2", NUMBER),
        ButtonInfo("3", NUMBER),
        ButtonInfo("+", OPERATOR, "Сложение (+)"),
    ],
    # Ряд 4
    [
        ButtonInfo("±", SPECIAL, "Сменить знак"),
        ButtonInfo("0", NUMBER),
        ButtonInfo(".", NUMBER, "Десятичная точка"),
        ButtonInfo("=", EQUALS, "Вычислить (Enter)"),
    ],
]

# Расширенные кнопки (научный режим)
SCIENTIFIC_BUTTONS: list[list[ButtonInfo]] = [
    [
        ButtonInfo("(", SPECIAL, "Открывающая скобка"),
        ButtonInfo(")", SPECIAL, "Закрывающая скобка"),
        ButtonInfo("x²", FUNCTION, "Квадрат числа"),
        ButtonInfo("√", FUNCTION, "Квадратный корень"),
    ],
]

# Маппинг отображаемых символов → символы для вычислений
DISPLAY_TO_CALC = {
    "÷": "/",
    "×": "*",
    "−": "-",
    "+": "+",
}

# Маппинг клавиатуры → отображаемые символы
KEY_TO_DISPLAY = {
    "/": "÷",
    "*": "×",
    "-": "−",
    "+": "+",
    ".": ".",
}

# Размеры окна
WINDOW_MIN_WIDTH = 360
WINDOW_MIN_HEIGHT = 520
SCIENTIFIC_EXTRA_HEIGHT = 100

# Шрифты
DISPLAY_FONT_SIZE = 32
EXPRESSION_FONT_SIZE = 14
BUTTON_FONT_SIZE = 18

# Точность вычислений
MAX_DECIMAL_PLACES = 12
MAX_DISPLAY_LENGTH = 20
MAX_HISTORY_ITEMS = 50
