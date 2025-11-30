from main_window import *
from utils import *
from grid_display import GridDisplay
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
    col_count: int = 12
    row_count: int = 8

    def __init__(self, ui:Ui_MainWindow):
        self.ui = ui
        self.grid_display = None
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
        num_used_cells = self.grid_display.get_num_used_cells()
        self.display_parse_results(num_used_cells, self.get_src_file_name())
        self.show_all(self.ui.ShipGridLayout)

    def hide_all(self, parentLayout: QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = get_all_children_items(parentLayout)
        
        for item in childItems:
            item.setVisible(False)
        
    def show_all(self, parentLayout: QtWidgets.QLayout):
        childItems:list[QtWidgets.QWidget] = get_all_children_items(parentLayout)

        for item in childItems:
            item.setVisible(True)
        
    def set_page(self, page: Pages):
        self.ui.AllPages.setCurrentIndex(page.value)

    def throw_error(self, errorMsg: str):
        self.set_page(Pages.ErrorPage)
        self.ui.ErrorLabel.setText(errorMsg)
        self.ui.ErrorLabel.setStyleSheet("color:red")
    
    def restart(self):
        self.set_page(Pages.FilePickPage)

    def init_ShipGrid(self, grid_parse: list[ManifestItem]):
        initial_state_grid = create_grid_from_list(grid_parse, self.row_count, self.col_count)
        initial_state_grid_display = GridDisplay(initial_state_grid)

        for cell_row in initial_state_grid_display.cell_grid:
            for cell in cell_row:
                self.ui.ShipGrid.addWidget(cell.label, cell.get_display_row(), cell.get_display_col())
        
        if not initial_state_grid_display.valid_grid():
            self.throw_error("ERROR: Ship layout is not allowed (asymmetric or floating objects)! Try again with a new file.")

        self.grid_display = initial_state_grid_display

    def display_parse_results(self, num_used_cells: int, src_file_name: str):
        root_name = get_file_root_name(src_file_name)
        message = f"{root_name} has {num_used_cells} containers\nComputing a solution..."
        self.display_message(message)
        self.show_all(self.ui.MessageLhsLayout)

    def display_message(self, message: str):
        self.ui.MessageLhsLabel.setText(message)

    def get_grid_display(self) -> GridDisplay:
        return self.grid_display

    def get_src_file_name(self) -> str:
        return self.src_file_name