import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeyEvent


class Calculator(QWidget):
    """Современный калькулятор с поддержкой клавиатуры и истории."""
    
    def __init__(self):
        super().__init__()
        self.current_expression = ""
        self.history = []
        self.initUI()

    def initUI(self):
        """Инициализация пользовательского интерфейса."""
        self.setWindowTitle('Калькулятор')
        self.setFixedSize(350, 450)

        # Основной вертикальный макет
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Создание дисплея
        self.display = self._create_display()
        main_layout.addWidget(self.display)

        # Создание сетки кнопок
        button_grid = self._create_button_grid()
        main_layout.addLayout(button_grid)

    def _create_display(self) -> QLineEdit:
        """Создание и настройка дисплея калькулятора."""
        display = QLineEdit()
        display.setAlignment(Qt.AlignRight)
        display.setFont(QFont('Arial', 24))
        display.setReadOnly(True)
        display.setMinimumHeight(60)
        display.setPlaceholderText("0")
        display.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                color: #333333;
            }
        """)
        return display

    def _create_button_grid(self) -> QGridLayout:
        """Создание сетки кнопок калькулятора."""
        grid = QGridLayout()
        grid.setSpacing(5)

        # Определение кнопок с их типами
        button_config = [
            ('7', 'number'), ('8', 'number'), ('9', 'number'), ('/', 'operator'),
            ('4', 'number'), ('5', 'number'), ('6', 'number'), ('*', 'operator'),
            ('1', 'number'), ('2', 'number'), ('3', 'number'), ('-', 'operator'),
            ('C', 'clear'),  ('0', 'number'), ('=', 'equals'), ('+', 'operator')
        ]

        # Создание кнопок
        for index, (text, btn_type) in enumerate(button_config):
            row = index // 4
            col = index % 4
            
            button = self._create_button(text, btn_type)
            grid.addWidget(button, row, col)

        # Делаем кнопки растягивающимися
        for i in range(4):
            grid.setRowStretch(i, 1)
            grid.setColumnStretch(i, 1)

        return grid

    def _create_button(self, text: str, btn_type: str) -> QPushButton:
        """Создание отдельной кнопки с соответствующим стилем."""
        button = QPushButton(text)
        button.setFont(QFont('Arial', 18, QFont.Bold))
        button.setMinimumSize(70, 70)
        button.setCursor(Qt.PointingHandCursor)
        
        # Применение стилей в зависимости от типа
        styles = {
            'operator': self._get_operator_style(),
            'equals': self._get_operator_style(),
            'clear': self._get_clear_style(),
            'number': self._get_number_style()
        }
        
        button.setStyleSheet(styles.get(btn_type, styles['number']))
        button.clicked.connect(lambda: self._on_button_clicked(text))
        
        return button

    @staticmethod
    def _get_operator_style() -> str:
        """Стиль для кнопок операций."""
        return """
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 35px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fb8c00;
            }
            QPushButton:pressed {
                background-color: #e68a00;
            }
        """

    @staticmethod
    def _get_clear_style() -> str:
        """Стиль для кнопки очистки."""
        return """
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 35px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """

    @staticmethod
    def _get_number_style() -> str:
        """Стиль для кнопок с цифрами."""
        return """
            QPushButton {
                background-color: #e0e0e0;
                color: #333333;
                border: none;
                border-radius: 35px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
            QPushButton:pressed {
                background-color: #bdbdbd;
            }
        """

    def _on_button_clicked(self, text: str):
        """Обработка нажатий на кнопки."""
        if text == 'C':
            self._clear_display()
        elif text == '=':
            self._calculate_result()
        else:
            self._append_to_display(text)

    def _clear_display(self):
        """Очистка дисплея."""
        self.current_expression = ""
        self.display.clear()

    def _append_to_display(self, text: str):
        """Добавление символа к текущему выражению."""
        current_text = self.display.text()
        
        # Если на дисплее ошибка, начинаем заново
        if current_text in ['Ошибка', 'Деление на ноль']:
            self.current_expression = text
        else:
            self.current_expression = current_text + text
        
        self.display.setText(self.current_expression)

    def _calculate_result(self):
        """Вычисление результата выражения."""
        try:
            expression = self.display.text()
            if not expression:
                return
            
            # Безопасное вычисление (только цифры и операторы)
            # Защита от опасных команд
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Недопустимые символы")
            
            result = eval(expression)
            
            # Проверка на деление на ноль
            if result == float('inf') or result == float('-inf'):
                raise ZeroDivisionError
            
            # Форматирование результата
            if isinstance(result, float):
                # Убираем лишние нули после точки
                result = f"{result:.10g}"
            else:
                result = str(result)
            
            # Сохранение в историю
            self.history.append(f"{expression} = {result}")
            
            self.display.setText(result)
            self.current_expression = result
            
        except ZeroDivisionError:
            self.display.setText('Деление на ноль')
            self.current_expression = ""
        except Exception:
            self.display.setText('Ошибка')
            self.current_expression = ""

    def keyPressEvent(self, event: QKeyEvent):
        """Обработка нажатий клавиш."""
        key = event.key()
        text = event.text()
        
        # Цифры и операторы
        if text in '0123456789+-*/.':
            self._append_to_display(text)
        # Enter или = для вычисления
        elif key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal):
            self._calculate_result()
        # Escape или C для очистки
        elif key in (Qt.Key_Escape, Qt.Key_C):
            self._clear_display()
        # Backspace для удаления последнего символа
        elif key == Qt.Key_Backspace:
            current = self.display.text()
            if current not in ['Ошибка', 'Деление на ноль']:
                self.current_expression = current[:-1]
                self.display.setText(self.current_expression)


def main():
    """Точка входа в приложение."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Установка глобального стиля приложения
    app.setStyleSheet("""
        QWidget {
            background-color: #fafafa;
        }
    """)
    
    calculator = Calculator()
    calculator.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
