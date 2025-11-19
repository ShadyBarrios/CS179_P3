import os
import sys

from PySide6 import QtWidgets
from main_window import *
from components import Components

def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    components = Components(widget.ui)
    components.hide_all(components.ui.FilePickLayout)
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
