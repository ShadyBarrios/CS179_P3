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

    def pick_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a manifest txt file", None, "Text Files (*.txt)")
        file_name = file[0]

        if file_name == '':
            self.ui.FilePickLabel.setText("File not picked. Try again.")
            return

        grid_parse = parse_file(file_name)

        if isinstance(grid_parse, ParseErrorTypes):
            match grid_parse:
                case ParseErrorTypes.FileNotFound:
                    self.ui.FilePickLabel.setText("ERROR: File not found. Try again.")
                    return
                case ParseErrorTypes.IncorrectFileType:
                    self.ui.FilePickLabel.setText("ERROR: Must pick .txt file. Try again.")
                    return
                case ParseErrorTypes.IncorrectFileFormatting:
                    self.ui.FilePickLabel.setText("Error: File is not formatted properly. Try again.")
                    return
                case ParseErrorTypes.IncorrectManifestLength:
                    self.ui.FilePickLabel.setText("Error: Manifest does not match expected length (n = 96). Try again.")
                    return
        
        for item in grid_parse:
            print(item)
        return 

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
                