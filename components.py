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
from action import Action, ActionTypes
from time import localtime as current_time
from os import makedirs as makedir
from shutil import copy2

class States(Enum):
    init_grid = 1
    show_init = 2
    end = 3

class Pages(Enum):
    ShipGridPage = 0
    CommentPage = 1
    FinishedPage = 2
    FilePickPage = 3
    ErrorPage = 4

class SearchWorker(QtCore.QObject):
    solution = QtCore.Signal(object)

    def __init__(self, initial_state:State):
        super().__init__()
        self.initial_state = initial_state
    
    @QtCore.Slot()
    def run_search(self):
        self.search = Search(self.initial_state)
        time.sleep(0.5)
        solution = self.search.a_star_search()
        self.solution.emit(solution)

class SearchThread(QtCore.QObject):

    def __init__(self, parse):
        super().__init__(None)
        self.thread = QtCore.QThread()
        grid = create_grid_from_list(parse)
        self.worker = SearchWorker(State(grid))

        self.thread.started.connect(self.worker.run_search)

        self.worker.solution.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.moveToThread(self.thread)
    
    def run(self):
        self.thread.start()

class Components(QtCore.QObject):
    searchThread = None
    col_count: int = 12
    row_count: int = 8

    # TODO: Get "APP Started" time for log
    def __init__(self, ui: Ui_MainWindow):
        super().__init__()
        self.ui = ui
        self.app_start_time = current_time()
        self.grid_display = None
        self.src_file_name = ""
        self.directory = "output/" + to_directory_name(self.app_start_time)
        self.log_file_name = to_log_file_name(self.app_start_time)
        self.file_root_name = ""
        self.set_page(Pages.FilePickPage)
        self.solution:Solution = None
        self.solutionIdx = 0
        self.currentMove:str = None
        self.lastAction = None
        self.lastActionType = None
        self.lastMove = None
        self.start_log()
        
    def start_app(self):
        result = self.pick_file()
        if result == None:
            return
        else:
            self.searchThread = SearchThread(result)
            self.searchThread.worker.solution.connect(self.solution_found, type=QtCore.Qt.QueuedConnection)
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
        self.file_root_name = get_file_root_name(file_name)
        self.outbound_file_name = self.file_root_name + "OUTBOUND" + ".txt"
        validShip = self.begin(grid_parse)
        if validShip:
            return grid_parse
        else:
            return None

    def begin(self, grid_parse: list[ManifestItem]) :
        self.remove_solution_metadata()
        self.set_page(Pages.ShipGridPage)
        self.hide_all(self.ui.MessageLayouts)
        self.hide_all(self.ui.ShipGridLayout)
        validShip = self.init_ShipGrid(grid_parse)
        num_used_cells = self.grid_display.get_num_used_cells()
        validShip = validShip and num_used_cells <= 16
        self.log_open_manifest(num_used_cells)
        self.display_parse_results(num_used_cells)
        self.show_all(self.ui.ShipGridLayout)
        if validShip == False:
            self.invalid_ship()

        return validShip

    @QtCore.Slot(object)
    def solution_found(self, solution):
        self.solutionStates = solution.get_states()
        self.solutionActions = solution.get_actions()
        self.solutionIdx = 0 
        if len(self.solutionActions) > 0:
            self.log_solution_metrics(solution)
            self.display_solution_metadata(len(self.solutionActions), solution.get_time_to_execute())
        self.display_solution()
        self.show_all(self.ui.MessageLayouts)
    
    def display_solution_metadata(self, numActions:int, duration:int):
        self.ui.SolutionMetadataLabel.setText(f"Solution contains {numActions} moves and takes {duration} minutes to execute")

    def remove_solution_metadata(self):
        self.ui.SolutionMetadataLabel.setText("")
        
    def start_log(self):
        makedir(self.directory, exist_ok=True)

        try:
            with open(self.directory + "/" + self.log_file_name, "w") as log:
                log.write(parse_time(self.app_start_time) + "Program was started.\n")
        except FileNotFoundError:
            self.throw_error("There was an error opening the log file.")
    
    def log_line(self, output:str):
        try:
            with open(self.directory + "/" + self.log_file_name, "a") as log:   
                log.write(output)
        except FileNotFoundError:
            self.throw_error("There was an issue opening the log file.")

    def log_open_manifest(self, numItems:int):
        currTime=current_time()
        output = parse_time(currTime) + f"Manifest {self.file_root_name}.txt is opened, there {quantify(numItems)} container(s) on the ship.\n"
        self.log_line(output)

    def log_solution_metrics(self, sol:Solution):
        currTime=current_time()
        output = parse_time(currTime) + f"Balance solution found, it will require {len(sol.get_actions())} actions/{sol.get_time_to_execute()} minutes.\n"
        self.log_line(output)
    
    def log_move(self, action:Action, actionType:ActionTypes):
        currTime=current_time()
        if actionType is None or actionType != ActionTypes.MoveItem:
            return
        output = parse_time(currTime) + f"{action.source.coordinate} was moved to {action.target.coordinate}.\n"
        self.log_line(output)

    def log_no_moves_needed(self):
        currTime=current_time()
        output = parse_time(currTime) + f"There are no moves needed for Manifest {self.file_root_name}.txt Operator has been notified. {self.outbound_file_name} has been written to desktop.\n"
        self.log_line(output)
 
    def log_comment(self):
        comment = self.ui.CommentInput.toPlainText()
        currTime=current_time()
        if comment is None or comment == "":
            self.set_page(Pages.ShipGridPage)
            return
        output = parse_time(currTime) + f"{comment}\n"
        self.log_line(output)
        self.set_page(Pages.ShipGridPage)

    def log_completed_cycle(self):
        currTime=current_time()
        output = parse_time(currTime) + f"Finished a Cycle. Manifest {self.outbound_file_name} was written to desktop, and a reminder pop-up to operator to send file was displayed.\n"
        self.log_line(output)

    def log_exit_app(self):
        currTime=current_time()
        output = parse_time(currTime) + f"Program was shut down.\n"
        self.log_line(output)

        # duplicate log file into long-term storage for redundancy
        try: 
            backup_dir = "log_backup"
            makedir(backup_dir, exist_ok=True)
            
            src = f"{self.directory}/{self.log_file_name}"
            dest = f"{backup_dir}/{self.log_file_name}"
            output = parse_time(current_time()) + f"Log file stored for redundancy to log_backup directory.\n"
            self.log_line(output)
            copy2(src, dest)
        except FileNotFoundError:
            self.throw_error("ERROR: Source log file could not be found and duplicated to directory \"log_backup\".")

    def display_solution(self):
        idx = self.solutionIdx
        states:list[State] = self.solutionStates
        actions:list[Action] = self.solutionActions
        park = Coordinate(9,1)
        message = f"{idx+1} of {len(actions)}: Move "

        if len(actions) == 0: # no moves needed
            self.display_no_moves_needed(states[idx])
            return
        
        if self.lastAction is not None:
            self.log_move(self.lastAction, self.lastActionType)
            self.update_outbound_file(states[idx]) # will reach >= actions before >= states

        if self.solutionIdx >= len(actions): # end reached
            self.end_reached()
        else:
            state = states[idx]
            action = actions[idx]
            
            if action.source.coordinate == park:
                actionType = ActionTypes.FromPark 
            elif action.target.coordinate == park:
                actionType = ActionTypes.ToPark
            else:
                actionType = ActionTypes.MoveItem

            if self.lastMove is not None:
                self.add_to_moves(self.lastMove)

            match(actionType):
                case ActionTypes.FromPark:
                    message += f"crane from {source_styling('PARK')} to {target_styling(action.target.get_coordinate())}"
                case ActionTypes.ToPark:
                    message += f"from {source_styling(action.source.get_coordinate())} to {target_styling('PARK')}"
                case ActionTypes.MoveItem:
                    message += f"from {source_styling(action.source.get_coordinate())} to {target_styling(action.target.get_coordinate())}"
            
            self.lastMove = message
            self.lastAction = action
            self.lastActionType = actionType
            self.solutionIdx += 1
            self.ui.MessageLhsLabel.setText(message)
            self.grid_display.update(state, action)

    def display_no_moves_needed(self, state:State):
        self.log_no_moves_needed()
        self.update_outbound_file(state)
        self.throw_error(f"No moves needed! Crate layout already meets criteria.<br>Manifest saved to {self.outbound_file_name}")

    def end_reached(self):
        self.solutionIdx = 0
        self.solutionStates = None
        self.solutionActions = None
        self.currentMove = None
        self.log_completed_cycle()
        self.to_success_page()

    def to_log_comment(self):
        self.set_page(Pages.CommentPage)
        self.ui.CommentInput.setPlainText("")

    def to_success_page(self):
        self.successful_restart()
        self.set_page(Pages.FinishedPage)

    def cancel_comment(self):
        self.set_page(Pages.ShipGridPage)

    def successful_restart(self):
        message = f"I have written an updated manifest to the desktop as <br>{target_styling(self.outbound_file_name)}<br>Find it under the {target_styling(self.directory)} directory.<br>Don't forget to email it to the captain.<br>Click restart to use a new manifest or close the window.<br>"
        self.ui.SuccessMessageLabel.setText(message)

    def update_outbound_file(self, state:State):
        try:
            with open(self.directory + "/" + self.outbound_file_name, "w") as outbound:
                outbound.write(f"{state}")
        except FileNotFoundError:
            self.throw_error("OUTBOUND file could not be opened.")

    def reset_previous_moves(self):
        self.ui.PreviousMovesLabel.setText("")

    def reset_grid_display(self):
        while self.ui.ShipGrid.count():
            item = self.ui.ShipGrid.takeAt(0)
            item.widget().deleteLater()
            del item
        

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
        self.lastAction = None
        self.lastMove = None
        self.lastActionType = None
        self.reset_grid_display()
        self.reset_previous_moves()
        self.set_page(Pages.FilePickPage)

    def init_ShipGrid(self, grid_parse: list[ManifestItem]):
        initial_state_grid = create_grid_from_list(grid_parse, self.row_count, self.col_count)
        initial_state_grid_display = GridDisplay(initial_state_grid, self.ui.ParkLabel)

        for cell_row in initial_state_grid_display.cell_grid:
            for cell in cell_row:
                self.ui.ShipGrid.addWidget(cell.label, cell.get_display_row(), cell.get_display_col())
        
        self.grid_display = initial_state_grid_display

        if not initial_state_grid_display.valid_grid():
            return False
        return True

    def invalid_ship(self):
        self.throw_error("ERROR: Ship layout is not allowed (asymmetric, floating objects, ghost weights, or too many crates)! Try again with a new file.")
        self.log_invalid_ship()
    
    def log_invalid_ship(self):
        currTime=current_time()
        output = parse_time(currTime) + f"Manifest {self.file_root_name}.txt contained an invalid ship grid. Operator has been notified.\n"
        self.log_line(output)

    def display_parse_results(self, num_used_cells: int):
        root_name = self.file_root_name
        message = f"{root_name} has {num_used_cells} containers\nComputing a solution..."
        self.display_message(message)
        self.show_all(self.ui.MessageLhsLayout)
        self.show_all(self.ui.ParkLayout)
        self.hide_all(self.ui.ContinueLayout)
        self.hide_all(self.ui.ToCommentLayout)

    def display_message(self, message: str):
        self.ui.MessageLhsLabel.setText(message)

    def get_grid_display(self) -> GridDisplay:
        return self.grid_display

    def get_src_file_name(self) -> str:
        return self.src_file_name
    
    def add_to_moves(self, move:str) -> str:
        move_history = self.ui.PreviousMovesLabel.text()
        move_history += move + "<br>"
        self.ui.PreviousMovesLabel.setText(move_history)