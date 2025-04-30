"""
Main file for the banking application
Loads logic and starts application
"""
import sys
from PyQt6.QtWidgets import QApplication
from logic import *


def main() -> None:
    """
    Main function that starts the application
    """
    application = QApplication([])

    window = Logic()
    window.show()

    application.exec()


if __name__ == '__main__':
    main()
