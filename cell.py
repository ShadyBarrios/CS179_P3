from enum import Enum
from PySide6 import QtWidgets, QtCore
from manifest import ManifestItem, ItemPosition

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
    CellTypes.TARGET: "background-color:rgba(255, 0, 0, 0.5); color:BLACK;",
    CellTypes.SOURCE: "background-color:rgba(60, 179, 133, 0.5); color:BLACK;",
    ItemPosition.PORT: "background-color:WHITE; color:WHITE;",
    ItemPosition.STARBOARD: "background-color:GRAY; color:GRAY;"
}

class Cell:
    base_stylesheet = "padding-top:30px; padding-bottom:30px; padding-left:17px; padding-right:17px; border: 3px solid black;"

    def __init__(self, label:QtWidgets.QLabel, item:ManifestItem):
        self.label = label
        self.item = item
        self.type = CellTypes.to_type(item.get_title())

        self.style = self.base_stylesheet + StyleBackgroundDict[self.type]
        self.label.setStyleSheet(self.style)

    def get_type(self) -> CellTypes:
        return self.type

    def set_item(self, item:ManifestItem):
        self.item = item

    def set_value(self, value:str):
        self.value = value

    def set_type(self, type:CellTypes):
        self.type = type

    def update_text(self, value:str=None):
        if value is None:
            self.label.setText(self.value)
        else:
            self.label.setText(value)

    def set_style(self, style:str):
        self.label.setStyleSheet(style)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def generate_style(self) -> str:
        background = self.get_type()
        if self.type == CellTypes.UNUSED:
            background = self.item.get_position()
        return self.base_stylesheet + StyleBackgroundDict[background]
