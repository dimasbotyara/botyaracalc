import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QGridLayout, QPushButton, QLineEdit,
                             QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # Инициализация пользовательского интерфейса
        self.initUI()

    def initUI(self):
        # Установка заголовка окна
        self.setWindowTitle('Калькулятор')
        # Установка фиксированного размера окна для предотвращения изменения размера
        self.setFixedSize(350, 450)

        # Основной вертикальный макет
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # Создание поля ввода (дисплея)
        self.display = QLineEdit()
        # Выравнивание текста по правому краю
        self.display.setAlignment(Qt.AlignRight)
        # Установка крупного шрифта для удобства чтения
        self.display.setFont(QFont('Arial', 24))
        # Сделать поле ввода только для чтения (ввод только через кнопки)
        self.display.setReadOnly(True)
        # Увеличение высоты дисплея
        self.display.setMinimumHeight(60)
        # Добавление стилей (цвет фона, границы)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        # Добавление дисплея в основной макет
        self.vbox.addWidget(self.display)

        # Сеточный макет для кнопок
        self.grid = QGridLayout()
        self.vbox.addLayout(self.grid)

        # Список меток для кнопок в порядке их расположения
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        # Инициализация координат для размещения кнопок в сетке
        row = 0
        col = 0

        # Цикл для создания и добавления каждой кнопки
        for text in buttons:
            button = QPushButton(text)
            # Установка шрифта для кнопок
            button.setFont(QFont('Arial', 18))
            # Установка минимального размера для квадратной формы
            button.setMinimumSize(70, 70)

            # Настройка политики размера, чтобы кнопки расширялись
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setSizePolicy(sizePolicy)

            # Применение различных стилей в зависимости от типа кнопки
            if text in ['/', '*', '-', '+', '=']:
                # Стиль для кнопок операций (оранжевый фон)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #ff9800;
                        color: white;
                        border: none;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #e68a00;
                    }
                """)
            elif text == 'C':
                # Стиль для кнопки очистки (красный фон)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #d32f2f;
                    }
                """)
            else:
                # Стиль для кнопок с цифрами (светло-серый фон)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0;
                        border: none;
                        border-radius: 35px;
                    }
                    QPushButton:pressed {
                        background-color: #bdbdbd;
                    }
                """)

            # Подключение сигнала нажатия кнопки к методу обработки
            button.clicked.connect(self.on_button_clicked)
            # Добавление кнопки в сетку на текущие координаты
            self.grid.addWidget(button, row, col)

            # Обновление координат (переход на следующий столбец или строку)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_button_clicked(self):
        # Получение кнопки, которая отправила сигнал
        button = self.sender()
        text = button.text()

        # Если нажата кнопка 'C' (очистка)
        if text == 'C':
            self.display.clear()

        # Если нажата кнопка '=' (вычисление)
        elif text == '=':
            try:
                # Получение текущего выражения из дисплея
                expression = self.display.text()
                # Вычисление выражения с помощью встроенной функции eval()
                # Внимание: eval() безопасно использовать здесь, так как ввод ограничен кнопками
                result = str(eval(expression))
                # Отображение результата
                self.display.setText(result)
            except Exception as e:
                # Обработка ошибок (например, деление на ноль)
                self.display.setText('Ошибка')

        # Если нажата любая другая кнопка (цифра или операция)
        else:
            # Получение текущего текста на дисплее
            current_text = self.display.text()

            # Если на дисплее ошибка, начинаем ввод заново
            if current_text == 'Ошибка':
                self.display.setText(text)
            else:
                # Добавление текста нажатой кнопки к текущему тексту
                self.display.setText(current_text + text)

if __name__ == '__main__':
    # Создание объекта приложения
    app = QApplication(sys.argv)

    # Установка общего стиля приложения для лучшего вида на некоторых ОС
    app.setStyle('Fusion')

    # Создание и отображение главного окна калькулятора
    calc = Calculator()
    calc.show()

    # Запуск основного цикла обработки событий
    sys.exit(app.exec_())
