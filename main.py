import os
import sys

from PySide6 import QtWidgets
from main_window import *
from components import Components
from cell import global_stylesheet

def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.setStyleSheet(global_stylesheet)
    components = Components(widget.ui)
    components.ui.FilePickButton.clicked.connect(components.start_app)
    components.ui.ErrorRestartButton.clicked.connect(components.restart)
    components.ui.ContinueButton.clicked.connect(components.display_solution)
    components.ui.CancelCommentButton.clicked.connect(components.cancel_comment)
    components.ui.ToCommentButton.clicked.connect(components.to_log_comment)
    components.ui.LogCommentButton.clicked.connect(components.log_comment)
    components.ui.SuccessRestartButton.clicked.connect(components.successful_restart)
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
