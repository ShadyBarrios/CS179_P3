from enum import Enum
from PySide6 import QtWidgets, QtCore
from manifest import ManifestItem, ItemPosition
from coordinate import Coordinate

class TargetTypes(Enum):
    TARGET = 1
    SOURCE = 2

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
        
StyleBackgroundDict = {
    CellTypes.NAN: "background-color:BLACK; color:BLACK;",
    CellTypes.UNUSED: "background-color:WHITE; color:WHITE;",
    CellTypes.USED: "background-color:rgba(255, 165, 0, 0.5); color:BLACK;",
    TargetTypes.TARGET: "background-color:rgba(255, 0, 0, 0.5); color:BLACK;",
    TargetTypes.SOURCE: "background-color:rgba(60, 179, 133, 0.5); color:BLACK;",
    ItemPosition.PORT: "background-color:WHITE; color:WHITE;",
    ItemPosition.STARBOARD: "background-color:GRAY; color:GRAY;"
}

class Cell:
    base_stylesheet = "padding-top:18px; padding-bottom:18px; padding-left:10px; padding-right:10px; border: 2px solid black;"

    def __init__(self, item:ManifestItem):
        self.item = item
        self.type = CellTypes.to_type(item.get_title())
        self.label = QtWidgets.QLabel()
        self.targetType = None

        self._set_label_text()
        self.style = self.base_stylesheet + StyleBackgroundDict[self.type]
        self.label.setStyleSheet(self.style)

    def _set_label_text(self):
        if self.item.title == "UNUSED" or self.item.title == "NAN":
            self.label.setText("UNUSED")
        else:
            self.label.setText(str(self.item.weight))
        # elif len(self.item.title) > 6:
        #     self.label.setText(self.item.title[:5]+"...")
        # else:
        #     self.label.setText(self.item.title)
    
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

    def set_style(self, style:str):
        self.label.setStyleSheet(style)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def generate_style(self) -> str:
        targetType = self.get_targetType()

        # target type takes precedence
        background = self.get_type() if targetType is None else targetType

        if self.type == CellTypes.UNUSED:
            background = self.item.get_position()
        
        return self.base_stylesheet + StyleBackgroundDict[background]
    
class ParkCell(Cell):
    def __init__(self, parkLabel:QtWidgets.QLabel):
        self.parkLabel = parkLabel
        self.parkLabel.setText("CRANE")
        self.coordinate = Coordinate
        self.targetType = None
        self.update(None)
    
    def update(self, status:TargetTypes):
        stylesheet = self.base_stylesheet
        if status == None or not(isinstance(status, TargetTypes)):
            stylesheet += StyleBackgroundDict[ItemPosition.STARBOARD]
        else:
            stylesheet += StyleBackgroundDict[status]
        self.parkLabel.setStyleSheet(stylesheet)