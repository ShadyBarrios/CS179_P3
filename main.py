import os
import sys

from PySide6 import QtWidgets
from main_window import *
from components import Components

def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    components = Components(widget.ui)
    components.init_ShipGrid()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
