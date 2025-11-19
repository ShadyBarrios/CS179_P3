from main_window import *
from utils import *
from grid import Grid
from cell import Cell, CellTypes

class Components:
    grid:Grid = None
    row_count:int = 8
    col_count:int = 12

    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui

    def on_file_pick_click(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a manifest txt file", None, "Text Files (*.txt)")
        file_name = file[0]

    def hide_all(self, parentLayout:QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = []
        num_children = parentLayout.count()
        for child_idx in range(num_children):
            childItems.extend(get_all_children_items(parentLayout.itemAt(child_idx)))
        
        for item in childItems:
            item.setVisible(False)

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
                