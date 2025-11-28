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

class Pages(Enum):
    ShipGridPage = 0
    FilePickPage = 1
    ErrorPage = 2

class Components:
    grid:Grid = None
    col_count:int = 12
    row_count:int = 8

    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui
        self.src_file_name = None
        self.set_page(Pages.FilePickPage)
        

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
        
        self.src_file_name = file_name
        self.begin(grid_parse)
        return 

    def begin(self, grid_parse:list[ManifestItem]):
        self.set_page(Pages.ShipGridPage)
        self.hide_all(self.ui.MessageLayouts)
        self.init_ShipGrid(grid_parse)
        num_used_cells = self.get_grid().get_num_used_cells()
        self.display_parse_results(self.get_grid(), num_used_cells, self.get_src_file_name())
        self.show_all(self.ui.ShipGridLayout)

    def hide_all(self, parentLayout:QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = get_all_children_items(parentLayout)
        
        for item in childItems:
            item.setVisible(False)
        
    def show_all(self, parentLayout:QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = get_all_children_items(parentLayout)

        for item in childItems:
            item.setVisible(True)
        
    def set_page(self, page:Pages):
        self.ui.AllPages.setCurrentIndex(page.value)

    def throw_error(self, errorMsg:str):
        self.set_page(Pages.ErrorPage)
        self.ui.ErrorLabel.setText(errorMsg)
        self.ui.ErrorLabel.setStyleSheet("color:red")
    
    def restart(self):
        self.set_page(Pages.FilePickPage)

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
    
    def display_parse_results(self, grid:Grid, num_used_cells:int, src_file_name:str):
        root_name = get_file_root_name(src_file_name)
        message = f"{root_name} has {num_used_cells} containers\nComputing a solution..."
        self.display_message(message)
        self.show_all(self.ui.MessageLhsLayout)


    def display_message(self, message:str):
        self.ui.MessageLhsLabel.setText(message)

    def get_grid(self) -> Grid:
        return self.grid

    def get_src_file_name(self) -> str:
        return self.src_file_name