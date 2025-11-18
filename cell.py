from enum import Enum
from PySide6 import QtWidgets

class CellTypes(Enum):
    UNUSED = 1
    NAN = 2
    USED = 3

StyleBackgroundDict = {
    CellTypes.NAN: "background-color:BLACK;",
    CellTypes.UNUSED: "background-color:WHITE;",
    CellTypes.USED: "background-color:WHITE;"
}

class Cell:
    base_stylesheet = "padding:27px; border: 1px solid black; color:black;"
    def __init__(self, label:QtWidgets.QLabel, type:CellTypes, value:str=''):
        self.label = label
        self.type = type
        self.value = value

        style = self.base_stylesheet + StyleBackgroundDict[type]
        self.label.setStyleSheet(style)

    def setValue(self, value:str):
        self.value = value

    def setType(self, type:CellTypes):
        self.type = type

    def updateText(self, value:str=None):
        if value is None:
            self.label.setText(self.value)
        else:
            self.label.setText(value)

    