"""
Движок вычислений калькулятора.
Отвечает за парсинг, валидацию и безопасное вычисление выражений.
"""

import math
import re
from dataclasses import dataclass
from enum import Enum, auto

from config import MAX_DECIMAL_PLACES, DISPLAY_TO_CALC


class CalcError(Enum):
    """Типы ошибок вычислений."""
    NONE = auto()
    DIVISION_BY_ZERO = auto()
    INVALID_EXPRESSION = auto()
    OVERFLOW = auto()
    MATH_ERROR = auto()


@dataclass
class CalcResult:
    """Результат вычисления."""
    value: str
    error: CalcError = CalcError.NONE
    error_message: str = ""

    @property
    def is_success(self) -> bool:
        return self.error == CalcError.NONE


class CalculatorEngine:
    """
    Движок вычислений с валидацией и форматированием.
    Не зависит от UI — чистая логика.
    """

    # Допустимые символы в выражении
    ALLOWED_PATTERN = re.compile(r'^[\d+\-*/().% ]+$')

    # Паттерн для обнаружения оператора в конце
    TRAILING_OPERATOR = re.compile(r'[+\-*/]+$')

    # Паттерн для двойных операторов (кроме отрицательного числа)
    DOUBLE_OPERATOR = re.compile(r'[+*/]{2,}|[+\-*/][+*/]')

    def __init__(self):
        self.memory: float = 0.0
        self.last_result: str = ""

    def calculate(self, expression: str) -> CalcResult:
        """
        Вычисляет математическое выражение.

        Args:
            expression: Строка с выражением (с красивыми символами)

        Returns:
            CalcResult с результатом или ошибкой
        """
        if not expression or not expression.strip():
            return CalcResult(value="0")

        # Конвертация символов отображения → вычислимые
        calc_expr = self._convert_display_to_calc(expression)

        # Очистка выражения
        calc_expr = self._sanitize(calc_expr)

        if not calc_expr:
            return CalcResult(value="0")

        # Валидация
        if not self._validate(calc_expr):
            return CalcResult(
                value="",
                error=CalcError.INVALID_EXPRESSION,
                error_message="Некорректное выражение"
            )

        # Вычисление
        return self._safe_eval(calc_expr)

    def apply_function(self, func_name: str, value: str) -> CalcResult:
        """Применяет математическую функцию к значению."""
        try:
            num = float(value) if value else 0.0
        except ValueError:
            return CalcResult(
                value="",
                error=CalcError.INVALID_EXPRESSION,
                error_message="Некорректное число"
            )

        try:
            match func_name:
                case "x²":
                    result = num ** 2
                case "√":
                    if num < 0:
                        return CalcResult(
                            value="",
                            error=CalcError.MATH_ERROR,
                            error_message="Корень из отрицательного"
                        )
                    result = math.sqrt(num)
                case "%":
                    result = num / 100
                case _:
                    return CalcResult(
                        value="",
                        error=CalcError.INVALID_EXPRESSION,
                        error_message=f"Неизвестная функция: {func_name}"
                    )

            return CalcResult(value=self._format_number(result))

        except OverflowError:
            return CalcResult(
                value="",
                error=CalcError.OVERFLOW,
                error_message="Слишком большое число"
            )

    def negate(self, value: str) -> str:
        """Смена знака числа."""
        if not value or value == "0":
            return value

        try:
            num = float(value)
            return self._format_number(-num)
        except ValueError:
            return value

    # === Работа с памятью ===

    def memory_add(self, value: str):
        """Добавить значение в память."""
        try:
            self.memory += float(value)
        except (ValueError, TypeError):
            pass

    def memory_subtract(self, value: str):
        """Вычесть значение из памяти."""
        try:
            self.memory -= float(value)
        except (ValueError, TypeError):
            pass

    def memory_recall(self) -> str:
        """Получить значение из памяти."""
        return self._format_number(self.memory)

    def memory_clear(self):
        """Очистить память."""
        self.memory = 0.0

    @property
    def has_memory(self) -> bool:
        """Есть ли значение в памяти."""
        return self.memory != 0.0

    # === Приватные методы ===

    @staticmethod
    def _convert_display_to_calc(expression: str) -> str:
        """Конвертация красивых символов в вычислимые."""
        result = expression
        for display_char, calc_char in DISPLAY_TO_CALC.items():
            result = result.replace(display_char, calc_char)
        return result

    def _sanitize(self, expression: str) -> str:
        """
        Очистка выражения: удаление висящих операторов,
        лишних пробелов и т.д.
        """
        expr = expression.strip()

        # Удаляем операторы в конце выражения
        expr = self.TRAILING_OPERATOR.sub('', expr)

        # Удаляем оператор в начале (кроме минуса)
        while expr and expr[0] in '+*/':
            expr = expr[1:].lstrip()

        return expr.strip()

    def _validate(self, expression: str) -> bool:
        """Проверка выражения на допустимость."""
        if not expression:
            return False

        # Проверка символов
        if not self.ALLOWED_PATTERN.match(expression):
            return False

        # Проверка скобок
        depth = 0
        for char in expression:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            if depth < 0:
                return False

        if depth != 0:
            return False

        return True

    def _safe_eval(self, expression: str) -> CalcResult:
        """Безопасное вычисление выражения."""
        try:
            # Разрешаем только безопасные операции
            allowed_names = {"__builtins__": {}}
            result = eval(expression, allowed_names, {})

            # Проверки результата
            if isinstance(result, complex):
                return CalcResult(
                    value="",
                    error=CalcError.MATH_ERROR,
                    error_message="Комплексное число"
                )

            if result == float('inf') or result == float('-inf'):
                return CalcResult(
                    value="",
                    error=CalcError.OVERFLOW,
                    error_message="Слишком большое число"
                )

            if result != result:  # NaN check
                return CalcResult(
                    value="",
                    error=CalcError.MATH_ERROR,
                    error_message="Неопределённый результат"
                )

            formatted = self._format_number(result)
            self.last_result = formatted
            return CalcResult(value=formatted)

        except ZeroDivisionError:
            return CalcResult(
                value="",
                error=CalcError.DIVISION_BY_ZERO,
                error_message="Деление на ноль"
            )
        except OverflowError:
            return CalcResult(
                value="",
                error=CalcError.OVERFLOW,
                error_message="Переполнение"
            )
        except Exception:
            return CalcResult(
                value="",
                error=CalcError.INVALID_EXPRESSION,
                error_message="Ошибка вычисления"
            )

    @staticmethod
    def _format_number(value) -> str:
        """Форматирование числа для отображения."""
        if isinstance(value, float):
            # Если число целое по значению
            if value == int(value) and abs(value) < 1e15:
                return str(int(value))

            # Форматируем с ограниченной точностью
            formatted = f"{value:.{MAX_DECIMAL_PLACES}g}"
            return formatted

        return str(value)
