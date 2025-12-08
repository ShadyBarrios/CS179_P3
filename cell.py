from PySide6 import QtWidgets, QtCore

from coordinate import Coordinate
from enums import CellTypes, TargetTypes
from manifest import ManifestItem, ItemPosition

global_stylesheet = """
QLabel[cls="NAN"] { padding-top:17px; padding-bottom:17px; padding-left:10px; padding-right:10px; border: 2px solid black; background-color:BLACK; color:BLACK; }
QLabel[cls="USED"] { padding-top:17px; padding-bottom:17px; padding-left:10px; padding-right:10px; border: 2px solid black; background-color:rgba(255, 165, 0, 0.5); color:BLACK; }
QLabel[cls="TARGET"] { padding-top:17px; padding-bottom:17px; padding-left:10px; padding-right:10px; border: 2px solid black; background-color:rgba(255, 0, 0, 0.5); color:BLACK; }
QLabel[cls="SOURCE"] { padding-top:17px; padding-bottom:17px; padding-left:10px; padding-right:10px; border: 2px solid black; background-color:rgba(60, 179, 133, 0.5); color:BLACK; }
QLabel[cls="PORT"] { padding-top:17px; padding-bottom:17px; padding-left:10px; padding-right:10px; border: 2px solid black;background-color:WHITE; color:WHITE; }
QLabel[cls="STARBOARD"] { padding-top:17px; padding-bottom:17px; padding-left:10px; padding-right:10px; border: 2px solid black; background-color:GRAY; color:GRAY; }
QLabel[cls="PARK"] { border: 2px solid black; background-color:GRAY; color:GRAY; }
"""

class Cell:
    def __init__(self, item: ManifestItem):
        self.item = item
        self.type = item.get_type() 
        self.label = QtWidgets.QLabel()
        self.label.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.targetType = None

        self._set_label_text()
        self.update_style()

    def _set_label_text(self):
        if self.item.title == "UNUSED" or self.item.title == "NAN":
            self.label.setText("UNUSED")
        elif len(self.item.title) > 6:
            self.label.setText(f"{self.item.title[:5]}...<br>{self.item.weight}")
        else:
            self.label.setText(f"{self.item.title}<br>{self.item.weight}")
        
    def get_display_row(self) -> int:
        return (8 - self.item.get_row())
    
    def get_display_col(self) -> int:
        return self.item.get_col()

    def get_type(self) -> CellTypes:
        return self.type
    
    def get_targetType(self) -> TargetTypes|None:
        return self.targetType

    def set_item(self, item:ManifestItem):
        self.item = item

    def set_value(self, value:str):
        self.value = value

    def set_type(self, new_type:CellTypes):
        self.type = new_type

    def set_targetType(self, targetType:TargetTypes):
        self.targetType = targetType

    def update_text(self, value:str=None):
        if value is None:
            self.label.setText(self.value)
        else:
            self.label.setText(value)

    def update_style(self):
        targetType = self.get_targetType()
        # target type takes precedence
        background = self.get_type() if targetType is None else targetType
        if background == CellTypes.UNUSED:
            background = self.item.get_position()
        
        match(background):
            case TargetTypes.TARGET:
                self.label.setProperty("cls", "TARGET")
            case TargetTypes.SOURCE:
                self.label.setProperty("cls", "SOURCE")
            case CellTypes.USED:
                self.label.setProperty("cls", "USED")
            case CellTypes.NAN:
                self.label.setProperty("cls", "NAN")
            case ItemPosition.PORT:
                self.label.setProperty("cls", "PORT")
            case ItemPosition.STARBOARD:
                self.label.setProperty("cls", "STARBOARD")
        
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.label.update()

class ParkCell(Cell):
    def __init__(self, parkLabel:QtWidgets.QLabel):
        self.parkLabel = parkLabel
        self.parkLabel.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.parkLabel.setText("  PARK  ")
        self.coordinate = Coordinate(9,1)
        self.targetType = None
        self.update_park(None)
    
    def update_park(self, status:TargetTypes):
        if status == None or not(isinstance(status, TargetTypes)):
            self.parkLabel.setProperty("cls", "PARK")
        else:
            if status == TargetTypes.SOURCE:
                self.parkLabel.setProperty("cls", "SOURCE")
            else:
                self.parkLabel.setProperty("cls", "TARGET")
        
        self.parkLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.parkLabel.style().unpolish(self.parkLabel)
        self.parkLabel.style().polish(self.parkLabel)
        self.parkLabel.update()