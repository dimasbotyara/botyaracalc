"""
Settings manager for calculator.
Saves/loads configuration and history to JSON file.
"""

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

from translations import Language


@dataclass
class AppSettings:
    """Application settings structure."""
    language: str = Language.ENGLISH.value
    theme: str = "light"  # "light" or "dark"
    scientific_mode: bool = False
    sound_enabled: bool = False
    font_size: int = 18
    precision: int = 12
    window_width: int = 360
    window_height: int = 520
    history: List[str] = None

    def __post_init__(self):
        if self.history is None:
            self.history = []


class SettingsManager:
    """Manages application settings and persistence."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize settings manager.

        Args:
            config_dir: Directory for config file. If None, uses script directory.
        """
        if config_dir is None:
            # Use script directory
            self.config_dir = Path(__file__).parent
        else:
            self.config_dir = Path(config_dir)

        self.config_file = self.config_dir / "calculator_config.json"
        self.settings = AppSettings()
        self._load()

    def _load(self):
        """Load settings from file."""
        if not self.config_file.exists():
            return

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.settings = AppSettings(**data)
        except Exception as e:
            print(f"Failed to load settings: {e}")
            self.settings = AppSettings()

    def save(self):
        """Save settings to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.settings), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get_language(self) -> Language:
        """Get current language."""
        try:
            return Language(self.settings.language)
        except ValueError:
            return Language.ENGLISH

    def set_language(self, language: Language):
        """Set language and save."""
        self.settings.language = language.value
        self.save()

    def get_theme(self) -> str:
        """Get current theme."""
        return self.settings.theme

    def set_theme(self, theme: str):
        """Set theme and save."""
        self.settings.theme = theme
        self.save()

    def add_to_history(self, expression: str, result: str):
        """Add calculation to history."""
        history_item = f"{expression} = {result}"

        # Avoid duplicates
        if self.settings.history and self.settings.history[0] == history_item:
            return

        self.settings.history.insert(0, history_item)

        # Limit history size
        if len(self.settings.history) > 50:
            self.settings.history = self.settings.history[:50]

        self.save()

    def get_history(self) -> List[str]:
        """Get calculation history."""
        return self.settings.history.copy()

    def clear_history(self):
        """Clear all history."""
        self.settings.history.clear()
        self.save()

    def toggle_scientific_mode(self) -> bool:
        """Toggle scientific mode and return new state."""
        self.settings.scientific_mode = not self.settings.scientific_mode
        self.save()
        return self.settings.scientific_mode

    @property
    def scientific_mode(self) -> bool:
        """Check if scientific mode is enabled."""
        return self.settings.scientific_mode


# Global settings instance
_settings_manager: Optional[SettingsManager] = None


def get_settings() -> SettingsManager:
    """Get global settings manager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
