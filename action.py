from manifest import ManifestItem
from enum import Enum

class ActionTypes(Enum):
    FromPark = 1
    ToItem = 2
    MoveItem = 3
    ToPark = 4

class Action:
    def __init__(self, source: ManifestItem, target: ManifestItem):
        self.source = source
        self.target = target
    
    def copy(self):
        return Action(self.source.copy(), self.target.copy())
    
    def __str__(self) -> str:
        return f"Move {self.source.get_coordinate()} to {self.target.get_coordinate()}"