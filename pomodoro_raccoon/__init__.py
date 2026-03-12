"""
Pomodoro Raccoon - Ein simpler Pomodoro-Timer mit ASCII-Waschbär-Animation
"""

__version__ = "0.1.0"
__author__ = "Nick Witmar"
__email__ = "nickwitmar@gmail.com"

from .main import main_menu

def run():
    """Entry point für das Paket"""
    main_menu()