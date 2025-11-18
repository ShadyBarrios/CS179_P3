from PySide6 import QtWidgets
from main_window import *

class Components:
    row_count:int = 8
    col_count:int = 12

    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui

    def on_file_pick_click(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a txt file", None, "Text Files (*.txt)")
        file_name = file[0]

    def init_ShipGrid(self):
        print("print")
        for row in range(self.row_count):
            for col in range(self.col_count):
                label = QtWidgets.QLabel()
                label.setText(f"[{row},{col}]")
                label.setStyleSheet("padding:10px; border: 1px solid black;")
                self.ui.ShipGrid.addWidget(label, row, col)
                item = self.ui.ShipGrid.itemAtPosition(row, col)