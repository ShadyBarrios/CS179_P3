from enum import Enum
from PySide6 import QtWidgets

class ParseErrorTypes(Enum):
    FileNotFound = 1
    IncorrectFileType = 2
    IncorrectFileFormatting = 3
    IncorrectManifestLength = 4