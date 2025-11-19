from enum import Enum
from PySide6 import QtWidgets, QtCore
from manifest import ManifestItem

class CellTypes(Enum):
    UNUSED = 1
    NAN = 2
    USED = 3
    TARGET = 4
    SOURCE = 5

StyleBackgroundDict = {
    CellTypes.NAN: "background-color:BLACK; color:BLACK;",
    CellTypes.UNUSED: "background-color:WHITE; color:WHITE",
    CellTypes.USED: "background-color:rgba(255, 165, 0, 0.5); color:BLACK;",
    CellTypes.TARGET: "background-color:rgba(255, 0, 0, 0.5); color:BLACK;",
    CellTypes.SOURCE: "background-color:rgba(60, 179, 133, 0.5); color:BLACK;"
}

class Cell:
    base_stylesheet = "padding-top:30px; padding-bottom:30px; padding-left:17px; padding-right:17px; border: 3px solid black;"

    def __init__(self, label:QtWidgets.QLabel, item:ManifestItem):
        self.label = label
        self.item = item

        if item.get_title() == "NAN":
            self.type = CellTypes.NAN
        elif item.get_title() == "UNUSED":
            self.type = CellTypes.UNUSED
        else:
            self.type = CellTypes.USED

        self.style = self.base_stylesheet + StyleBackgroundDict[self.type]
        self.label.setStyleSheet(self.style)

    def getType(self):
        return self.type

    def setValue(self, value:str):
        self.value = value

    def setType(self, type:CellTypes):
        self.type = type

    def updateText(self, value:str=None):
        if value is None:
            self.label.setText(self.value)
        else:
            self.label.setText(value)

    def setStyle(self, style:str):
        self.label.setStyleSheet(style)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def generateStyle(self) -> str:
        return self.base_stylesheet + StyleBackgroundDict[self.type]
