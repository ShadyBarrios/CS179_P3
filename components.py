from main_window import *
from utils import *
from grid import Grid
from cell import Cell
from enum import Enum
from file_io import ParseErrorTypes, parse_file

class States(Enum):
    init_grid = 1
    show_init = 2
    end = 3

class Components:
    grid:Grid = None
    col_count:int = 12
    row_count:int = 8

    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui

        layouts_to_hide = [self.ui.ErrorLayout, self.ui.ShipGridLayout]
        for layout in layouts_to_hide:
            self.hide_all(layout)
        
        self.show_all(self.ui.FilePickLayout)
        

    def pick_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a manifest txt file", None, "Text Files (*.txt)")
        file_name = file[0]

        if file_name == '':
            self.throw_error("File not picked. Try again.")
            return

        grid_parse = parse_file(file_name)

        if isinstance(grid_parse, ParseErrorTypes):
            match grid_parse:
                case ParseErrorTypes.FileNotFound:
                    self.throw_error("ERROR: File not found. Try again.")
                    return
                case ParseErrorTypes.IncorrectFileType:
                    self.throw_error("ERROR: Must pick .txt file. Try again.")
                    return
                case ParseErrorTypes.IncorrectFileFormatting:
                    self.throw_error("Error: File is not formatted properly. Try again.")
                    return
                case ParseErrorTypes.IncorrectManifestLength:
                    self.throw_error("Error: Manifest does not match expected length (n = 96). Try again.")
                    return
        
        self.begin(grid_parse)
        return 

    def begin(self, grid_parse:list[ManifestItem]):
        self.hide_all(self.ui.FilePickLayout)
        self.init_ShipGrid(grid_parse)
        self.show_all(self.ui.ShipGridLayout)

    def hide_all(self, parentLayout:QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = get_all_children_items(parentLayout)
        
        for item in childItems:
            item.setVisible(False)
        
    def show_all(self, parentLayout:QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = get_all_children_items(parentLayout)

        for item in childItems:
            item.setVisible(True)

    def throw_error(self, errorMsg:str):
        layouts_to_hide = [self.ui.FilePickLayout, self.ui.ShipGridLayout]
        
        for layout in layouts_to_hide:
            self.hide_all(layout)
        
        self.show_all(self.ui.ErrorLayout)
        self.ui.ErrorLabel.setText(errorMsg)
        self.ui.ErrorLabel.setStyleSheet("color:red")
    
    def restart(self):
        layouts_to_hide = [self.ui.ErrorLayout, self.ui.ShipGridLayout]

        for layout in layouts_to_hide:
            self.hide_all(layout)

        self.show_all(self.ui.FilePickLayout)

    def init_ShipGrid(self, grid_parse:list[ManifestItem]):
        grid:list[list[Cell]] = []
        for row in range(self.row_count):
            gridRow = []
            for col in range(self.col_count):
                item = grid_parse[(row*(self.col_count) + col)]

                label = QtWidgets.QLabel()
                text = item.get_title_for_display()
                label.setText(text)

                self.ui.ShipGrid.addWidget(label, item.get_row_for_display(), item.get_col())

                cell = Cell(label, item)

                style = cell.generate_style()
                cell.set_style(style)

                gridRow.append(cell)
            grid.append(gridRow)

        self.grid = Grid(grid, self.row_count, self.col_count)
        if not self.grid.valid_grid():
            self.throw_error("ERROR: Item layout is not physically possible! Try again with a new file.")