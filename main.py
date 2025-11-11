import os
import sys

from PySide6 import QtWidgets
from main_window import *

CommsLabel:QtWidgets.QLabel = None

def get_txt_file_name():
    global CommsLabel

    file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a txt file", None, "Text Files (*.txt)")
    file_name = file[0]
    if file_name == " ":
        print("No file selected")
        CommsLabel.setText("You didn't pick a file! Try again.")
    else:
        print(f"File picked {file_name}")
        CommsLabel.setText(f"You picked {file_name}")

def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    global CommsLabel 
    CommsLabel = widget.ui.CommunicatorLabel
    widget.ui.FilePickButton.clicked.connect(get_txt_file_name)
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
