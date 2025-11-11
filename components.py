from PySide6 import QtWidgets
from main_window import *

class Components:
    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui

    def on_file_pick_click(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a txt file", None, "Text Files (*.txt)")
        file_name = file[0]

        CommsLabel = self.ui.CommunicatorLabel

        if file_name == '':
            print("No file selected")
            CommsLabel.setText("You didn't pick a file! Try again.")
        else:
            print(f"File picked {file_name}")
            CommsLabel.setText(f"You picked {file_name}")