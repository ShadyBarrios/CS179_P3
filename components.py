from main_window import *
from utils import *
from grid_display import GridDisplay
from enum import Enum
from file_io import ParseErrorTypes, parse_file
from state import State
from solution import Solution
from search import Search
from PySide6 import QtCore
from coordinate import Coordinate
import time

class States(Enum):
    init_grid = 1
    show_init = 2
    end = 3

class Pages(Enum):
    ShipGridPage = 0
    FilePickPage = 1
    ErrorPage = 2

class SearchWorker(QtCore.QObject):
    solution = QtCore.Signal(Solution)

    def __init__(self, initial_state:State):
        super().__init__()
        self.initial_state = initial_state
    
    @QtCore.Slot()
    def run_search(self):
        self.search = Search(self.initial_state)
        time.sleep(0.5)
        solution = self.search.a_star_search()
        print(f"Hi within thread: {solution.num_actions()} moves in solution")
        self.solution.emit(solution)

class SearchThread(QtCore.QObject):

    def __init__(self, parse):
        super().__init__(None)
        self.thread = QtCore.QThread()
        grid = create_grid_from_list(parse)
        self.worker = SearchWorker(State(grid))
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_search)
        self.worker.solution.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
    
    def run(self):
        self.thread.start()

class Components():
    searchThread = None
    col_count: int = 12
    row_count: int = 8

    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.grid_display = None
        self.src_file_name = None
        self.set_page(Pages.FilePickPage)
        self.solution:Solution = None
        self.solutionIdx = 0
        self.currentMove:str = None
        
    def start_app(self):
        result = self.pick_file()
        if result == None:
            return
        else:
            self.searchThread = SearchThread(result)
            self.searchThread.worker.solution.connect(self.solution_found)
            self.searchThread.run()

    def pick_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None, "Pick a manifest txt file", None, "Text Files (*.txt)")
        file_name = file[0]

        if file_name == '':
            self.throw_error("File not picked. Try again.")
            return None

        grid_parse = parse_file(file_name)

        if isinstance(grid_parse, ParseErrorTypes):
            match grid_parse:
                case ParseErrorTypes.FileNotFound:
                    self.throw_error("ERROR: File not found. Try again.")
                    return None
                case ParseErrorTypes.IncorrectFileType:
                    self.throw_error("ERROR: Must pick .txt file. Try again.")
                    return None
                case ParseErrorTypes.IncorrectFileFormatting:
                    self.throw_error("Error: File is not formatted properly. Try again.")
                    return None
                case ParseErrorTypes.IncorrectManifestLength:
                    self.throw_error("Error: Manifest does not match expected length (n = 96). Try again.")
                    return None
        
        self.src_file_name = file_name
        self.begin(grid_parse)
        return grid_parse

    def begin(self, grid_parse: list[ManifestItem]):
        self.set_page(Pages.ShipGridPage)
        self.hide_all(self.ui.MessageLayouts)
        self.hide_all(self.ui.ShipGridLayout)
        self.init_ShipGrid(grid_parse)
        num_used_cells = self.grid_display.get_num_used_cells()
        self.display_parse_results(num_used_cells, self.get_src_file_name())
        self.show_all(self.ui.ShipGridLayout)

    @QtCore.Slot(Solution)
    def solution_found(self, solution):
        print(f"Hi outside of thread... solution:\n{solution}")
        self.solution = solution   
        self.solutionIdx = 0 
        self.display_solution()
        self.ui.ContinueButton.clicked.connect(self.display_solution)

    def display_solution(self):
        idx = self.solutionIdx
        nodes = self.solution.get_nodes()
        actions = self.solution.get_actions()
        node = nodes[idx]
        action = actions[idx]
        park = Coordinate(9,1)
        message = f"{idx} of {len(actions)}: Move "

        print(f"Here {len(actions)}")
        if len(actions) == 0: # no moves needed
            self.display_no_moves_needed()
        
        if self.solutionIdx == len(actions): # end reached
            self.end_reached()
        
        if action.source == park:
            actionType = ActionTypes.FromPark 
        elif action.target == park:
            actionType = ActionTypes.ToPark
        else:
            actionType = ActionTypes.MoveItem

        if self.currentMove is not None:
            self.add_to_moves(self.currentMove)

        match(actionType):
            case ActionTypes.FromPark:
                message += f"crane from {source_styling('park')} to {target_styling(action.target.get_coordinate())}"
            case ActionTypes.ToPark:
                message += f"from {source_styling(action.source.get_coordinate())} to {target_styling('park')}"
            case ActionTypes.MoveItem:
                message += f"from {source_styling(action.source.get_coordinate())} to {target_styling(action.target.get_coordinate())}"
        
        self.currentMove = message
        self.solutionIdx += 1
        self.grid_display.update(node, action)

    def display_no_moves_needed(self):
        pass

    def end_reached(self):
        self.restart()

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
        initial_state_grid_display = GridDisplay(initial_state_grid, self.ui.ParkLabel)

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
        self.show_all(self.ui.ParkLayout)
        self.hide_all(self.ui.ContinueLayout)

    def display_message(self, message: str):
        self.ui.MessageLhsLabel.setText(message)

    def get_grid_display(self) -> GridDisplay:
        return self.grid_display

    def get_src_file_name(self) -> str:
        return self.src_file_name
    
    def add_to_moves(self, move:str) -> str:
        move_history = self.ui.MoveHistoryLabel.text()
        move_history += move + "\n"
        self.ui.MoveHistoryLabel.setText(move_history)