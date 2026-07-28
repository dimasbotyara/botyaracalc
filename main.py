"""
Modern Calculator Application
Main entry point with menu bar and application window.
"""

import sys
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QMenu,
                             QAction, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QKeySequence

from calculator_widget import CalculatorWidget
from language_dialog import show_language_dialog
from settings_manager import get_settings
from translations import set_language, t, get_current_language, Language
from styles import get_theme
from config import WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT


class CalculatorWindow(QMainWindow):
    """Main calculator window with menu bar."""

    def __init__(self):
        super().__init__()

        self.settings = get_settings()
        self.theme = get_theme()

        # Check if first launch (show language dialog)
        if not Path(self.settings.config_file).exists():
            self._show_language_selection()
        else:
            # Load saved language
            saved_lang = self.settings.get_language()
            set_language(saved_lang)

        # Load theme
        saved_theme = self.settings.get_theme()
        self.theme.set_theme(saved_theme)

        self._init_ui()
        self._create_menu_bar()
        self._apply_shortcuts()

        # Apply initial theme
        QTimer.singleShot(100, self._apply_theme)

    def _init_ui(self):
        """Initialize main window UI."""
        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Try to set window icon (if exists)
        icon_path = Path(__file__).parent / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # Create central widget
        self.calculator = CalculatorWidget()
        self.setCentralWidget(self.calculator)

        # Connect theme changes
        self.calculator.theme_changed.connect(self._apply_theme)

        # Restore window size
        width = self.settings.settings.window_width
        height = self.settings.settings.window_height
        self.resize(width, height)

    def _create_menu_bar(self):
        """Create application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu(t("menu_file"))

        # Clear history action
        clear_history_action = QAction(t("history_clear"), self)
        clear_history_action.setShortcut(QKeySequence("Ctrl+Shift+Del"))
        clear_history_action.triggered.connect(self._clear_history)
        file_menu.addAction(clear_history_action)

        file_menu.addSeparator()

        # Export history action
        export_action = QAction("📥 " + "Export History", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._export_history)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction(t("menu_exit"), self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu(t("menu_edit"))

        # Copy action
        copy_action = QAction(t("menu_copy"), self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self._copy_result)
        edit_menu.addAction(copy_action)

        # View menu
        view_menu = menubar.addMenu(t("menu_view"))

        # Toggle history
        history_action = QAction(t("menu_history"), self)
        history_action.setShortcut(QKeySequence("Ctrl+H"))
        history_action.setCheckable(True)
        history_action.setChecked(True)
        history_action.triggered.connect(self._toggle_history)
        view_menu.addAction(history_action)

        view_menu.addSeparator()

        # Toggle scientific mode
        scientific_action = QAction(t("setting_scientific"), self)
        scientific_action.setShortcut(QKeySequence("Ctrl+S"))
        scientific_action.setCheckable(True)
        scientific_action.setChecked(self.settings.scientific_mode)
        scientific_action.triggered.connect(self._toggle_scientific)
        view_menu.addAction(scientific_action)

        view_menu.addSeparator()

        # Theme submenu
        theme_menu = view_menu.addMenu(t("setting_theme"))

        light_action = QAction(t("theme_light"), self)
        light_action.setCheckable(True)
        light_action.setChecked(self.settings.get_theme() == "light")
        light_action.triggered.connect(lambda: self._set_theme("light"))
        theme_menu.addAction(light_action)

        dark_action = QAction(t("theme_dark"), self)
        dark_action.setCheckable(True)
        dark_action.setChecked(self.settings.get_theme() == "dark")
        dark_action.triggered.connect(lambda: self._set_theme("dark"))
        theme_menu.addAction(dark_action)

        # Language submenu
        lang_menu = view_menu.addMenu(t("language_select"))

        en_action = QAction("🇬🇧 English", self)
        en_action.setCheckable(True)
        en_action.setChecked(get_current_language() == Language.ENGLISH)
        en_action.triggered.connect(lambda: self._set_language(Language.ENGLISH))
        lang_menu.addAction(en_action)

        ru_action = QAction("🇷🇺 Русский", self)
        ru_action.setCheckable(True)
        ru_action.setChecked(get_current_language() == Language.RUSSIAN)
        ru_action.triggered.connect(lambda: self._set_language(Language.RUSSIAN))
        lang_menu.addAction(ru_action)

        # Help menu
        help_menu = menubar.addMenu(t("menu_help"))

        # Keyboard shortcuts
        shortcuts_action = QAction("⌨️ " + "Keyboard Shortcuts", self)
        shortcuts_action.setShortcut(QKeySequence("F1"))
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        # About action
        about_action = QAction(t("menu_about"), self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _apply_shortcuts(self):
        """Apply global keyboard shortcuts."""
        # Ctrl+T for theme toggle
        pass  # Already handled in calculator_widget

    def _show_language_selection(self):
        """Show language selection dialog on first launch."""
        selected_lang = show_language_dialog(self)
        set_language(selected_lang)
        self.settings.set_language(selected_lang)

    def _apply_theme(self):
        """Apply theme to window."""
        self.setStyleSheet(self.theme.get_window_style())

        # Update menu bar style
        menubar_style = f"""
            QMenuBar {{
                background-color: {self.theme.current_theme.window_bg};
                color: {self.theme.current_theme.display_text};
                padding: 5px;
            }}
            QMenuBar::item:selected {{
                background-color: {self.theme.current_theme.button_number_hover};
                border-radius: 4px;
            }}
            QMenu {{
                background-color: {self.theme.current_theme.display_bg};
                color: {self.theme.current_theme.display_text};
                border: 1px solid {self.theme.current_theme.display_border};
                padding: 5px;
            }}
            QMenu::item:selected {{
                background-color: {self.theme.current_theme.button_number_hover};
                border-radius: 4px;
            }}
        """
        self.menuBar().setStyleSheet(menubar_style)

    def _copy_result(self):
        """Copy current result to clipboard."""
        if self.calculator.display.copy_to_clipboard():
            self.statusBar().showMessage(t("history_copied"), 2000)

    def _toggle_history(self):
        """Toggle history panel visibility."""
        self.calculator._toggle_history()

    def _toggle_scientific(self):
        """Toggle scientific mode."""
        is_scientific = self.settings.toggle_scientific_mode()

        # Show restart message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(t("app_title"))

        if get_current_language() == Language.RUSSIAN:
            msg.setText("Перезапустите приложение для применения изменений")
        else:
            msg.setText("Please restart the application to apply changes")

        msg.exec_()

    def _set_theme(self, theme_name: str):
        """Set application theme."""
        self.settings.set_theme(theme_name)
        self.theme.set_theme(theme_name)
        self.calculator.apply_theme()
        self._apply_theme()

    def _set_language(self, language: Language):
        """Set application language."""
        set_language(language)
        self.settings.set_language(language)

        # Show restart message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Language / Язык")
        msg.setText(
            "Please restart the application to apply language changes.\n\n"
            "Пожалуйста, перезапустите приложение для применения изменений."
        )
        msg.exec_()

    def _clear_history(self):
        """Clear calculation history."""
        reply = QMessageBox.question(
            self,
            t("history_clear"),
            "Are you sure?" if get_current_language() == Language.ENGLISH
            else "Вы уверены?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.calculator.history_panel.clear()
            self.settings.clear_history()
            self.statusBar().showMessage(t("history_clear"), 2000)

    def _export_history(self):
        """Export history to text file."""
        history = self.calculator.history_panel.get_history()

        if not history:
            QMessageBox.information(self, t("app_title"), t("history_empty"))
            return

        # Open file dialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export History",
            "calculator_history.txt",
            "Text Files (*.txt);;All Files (*)"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Calculator History\n")
                    f.write("=" * 50 + "\n\n")
                    for item in history:
                        f.write(item + "\n")

                QMessageBox.information(
                    self,
                    t("app_title"),
                    f"Exported to: {filename}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to export: {str(e)}"
                )

    def _show_shortcuts(self):
        """Show keyboard shortcuts help."""
        shortcuts_text = """
        <h3>Keyboard Shortcuts</h3>
        <table style="width:100%">
        <tr><td><b>0-9, ., +, -, *, /</b></td><td>Number and operators input</td></tr>
        <tr><td><b>Enter</b></td><td>Calculate result</td></tr>
        <tr><td><b>Esc</b></td><td>Clear all</td></tr>
        <tr><td><b>Backspace</b></td><td>Delete last character</td></tr>
        <tr><td><b>Ctrl+C</b></td><td>Copy result</td></tr>
        <tr><td><b>Ctrl+H</b></td><td>Toggle history</td></tr>
        <tr><td><b>Ctrl+T</b></td><td>Toggle theme</td></tr>
        <tr><td><b>Ctrl+Q</b></td><td>Quit application</td></tr>
        </table>
        """

        if get_current_language() == Language.RUSSIAN:
            shortcuts_text = """
            <h3>Горячие клавиши</h3>
            <table style="width:100%">
            <tr><td><b>0-9, ., +, -, *, /</b></td><td>Ввод чисел и операторов</td></tr>
            <tr><td><b>Enter</b></td><td>Вычислить результат</td></tr>
            <tr><td><b>Esc</b></td><td>Очистить всё</td></tr>
            <tr><td><b>Backspace</b></td><td>Удалить последний символ</td></tr>
            <tr><td><b>Ctrl+C</b></td><td>Копировать результат</td></tr>
            <tr><td><b>Ctrl+H</b></td><td>Показать/скрыть историю</td></tr>
            <tr><td><b>Ctrl+T</b></td><td>Сменить тему</td></tr>
            <tr><td><b>Ctrl+Q</b></td><td>Выход</td></tr>
            </table>
            """

        msg = QMessageBox(self)
        msg.setWindowTitle("Shortcuts / Горячие клавиши")
        msg.setTextFormat(Qt.RichText)
        msg.setText(shortcuts_text)
        msg.exec_()

    def _show_about(self):
        """Show about dialog."""
        about_text = t("about_text")

        QMessageBox.about(self, t("menu_about"), about_text)

    def closeEvent(self, event):
        """Handle window close event - save settings."""
        # Save window size
        self.settings.settings.window_width = self.width()
        self.settings.settings.window_height = self.height()
        self.settings.save()

        event.accept()


def main():
    """Application entry point."""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName("Calculator")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("ModernCalc")

    # Use Fusion style for consistent look
    app.setStyle('Fusion')

    # Create and show main window
    window = CalculatorWindow()
    window.show()

    # Center window on screen
    screen_geometry = app.desktop().screenGeometry()
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 2
    window.move(x, y)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
