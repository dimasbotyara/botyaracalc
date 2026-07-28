"""
Language selection dialog shown on first launch.
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from translations import Language


class LanguageDialog(QDialog):
    """Dialog for selecting application language."""

    language_selected = pyqtSignal(Language)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_language = Language.ENGLISH
        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("Language / Язык")
        self.setModal(True)
        self.setFixedSize(400, 250)

        # Remove question mark button, keep only close
        self.setWindowFlags(
            Qt.Dialog |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.MSWindowsFixedSizeDialogHint
        )

        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Welcome label
        welcome_label = QLabel("🧮 Welcome to Calculator!\n🧮 Добро пожаловать в Калькулятор!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 12, QFont.Bold))
        welcome_label.setStyleSheet("color: #333333; padding: 10px;")
        layout.addWidget(welcome_label)

        # Instruction label
        instruction = QLabel("Please select your language:\nПожалуйста, выберите язык:")
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setFont(QFont("Arial", 10))
        instruction.setStyleSheet("color: #666666;")
        layout.addWidget(instruction)

        # Language selection group
        lang_layout = QVBoxLayout()
        lang_layout.setSpacing(10)

        self.button_group = QButtonGroup(self)

        # English option
        self.radio_en = QRadioButton("🇬🇧 English")
        self.radio_en.setFont(QFont("Arial", 11))
        self.radio_en.setStyleSheet(self._get_radio_style())
        self.radio_en.setChecked(True)
        self.button_group.addButton(self.radio_en, 0)
        lang_layout.addWidget(self.radio_en)

        # Russian option
        self.radio_ru = QRadioButton("🇷🇺 Русский")
        self.radio_ru.setFont(QFont("Arial", 11))
        self.radio_ru.setStyleSheet(self._get_radio_style())
        self.button_group.addButton(self.radio_ru, 1)
        lang_layout.addWidget(self.radio_ru)

        layout.addLayout(lang_layout)

        # Spacer
        layout.addStretch()

        # OK button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_button = QPushButton("OK ✓")
        ok_button.setFont(QFont("Arial", 11, QFont.Bold))
        ok_button.setFixedSize(120, 40)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(self._get_ok_button_style())
        ok_button.clicked.connect(self._on_ok_clicked)
        ok_button.setDefault(True)

        button_layout.addWidget(ok_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Apply overall dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
        """)

    def _get_radio_style(self) -> str:
        """Get stylesheet for radio buttons."""
        return """
            QRadioButton {
                padding: 8px;
                spacing: 10px;
                color: #333333;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #999999;
                background-color: white;
            }
            QRadioButton::indicator:checked {
                background-color: #ff9f0a;
                border: 2px solid #ff9f0a;
            }
            QRadioButton::indicator:hover {
                border: 2px solid #ff9f0a;
            }
            QRadioButton:hover {
                color: #ff9f0a;
            }
        """

    def _get_ok_button_style(self) -> str:
        """Get stylesheet for OK button."""
        return """
            QPushButton {
                background-color: #ff9f0a;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ff9500;
            }
            QPushButton:pressed {
                background-color: #e68a00;
            }
        """

    def _on_ok_clicked(self):
        """Handle OK button click."""
        if self.radio_en.isChecked():
            self.selected_language = Language.ENGLISH
        else:
            self.selected_language = Language.RUSSIAN

        self.language_selected.emit(self.selected_language)
        self.accept()

    def get_selected_language(self) -> Language:
        """Get the selected language."""
        return self.selected_language


def show_language_dialog(parent=None) -> Language:
    """
    Show language selection dialog and return selected language.

    Args:
        parent: Parent widget

    Returns:
        Selected Language enum value
    """
    dialog = LanguageDialog(parent)
    dialog.exec_()
    return dialog.get_selected_language()
