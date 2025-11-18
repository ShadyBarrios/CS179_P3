from PySide6 import QtWidgets
from main_window import *
from grid import Grid
from cell import Cell, CellTypes

class Components:
    grid:Grid = None
    row_count:int = 8
    col_count:int = 12

    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui

    def on_file_pick_click(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a txt file", None, "Text Files (*.txt)")
        file_name = file[0]

    def init_ShipGrid(self):
        grid = []
        for row in range(self.row_count):
            gridRow = []
            for col in range(self.col_count):
                label = QtWidgets.QLabel()
                text = f"[{row},{col}]"
                label.setText(text)
                style = "padding:27px; border: 1px solid black; color:black;"
                label.setStyleSheet(style)

                self.ui.ShipGrid.addWidget(label, row, col)

                cell = Cell(label, CellTypes.UNUSED, text)

                gridRow.append(cell)
            grid.append(gridRow)
                