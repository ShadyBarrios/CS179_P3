from enum import Enum

class ActionTypes(Enum):
    FromPark = 1
    ToItem = 2
    MoveItem = 3
    ToPark = 4

class CellTypes(Enum):
    UNUSED = 1
    NAN = 2
    USED = 3
    TARGET = 4
    SOURCE = 5

    def to_type(title:str):
        if title== "NAN":
            return CellTypes.NAN
        elif title == "UNUSED":
            return CellTypes.UNUSED
        else:
            return CellTypes.USED

class CraneMoves(Enum):
    MoveLeft = 1 # crane is to the right of the object (row doesn't matter)
    MoveRight = 2 # crane is to the left of the object (row doesn't matter)
    MoveDown = 3 # crane is above object
    MoveUp = 4 # crane has met a wall
    AtDest = 5 # crane is at dest
    MoveUpSameRow = 6 # crane is on the same row as object but met an obstacle (since our algo tracks what the crane can grab, it's actually a row above curr_row, so no need to count this move)

class Pages(Enum):
    ShipGridPage = 0
    CommentPage = 1
    FinishedPage = 2
    FilePickPage = 3
    ErrorPage = 4

class ParseErrorTypes(Enum):
    FileNotFound = 1
    IncorrectFileType = 2
    IncorrectFileFormatting = 3
    IncorrectManifestLength = 4

class States(Enum):
    init_grid = 1
    show_init = 2
    end = 3

class TargetTypes(Enum):
    TARGET = 1
    SOURCE = 2