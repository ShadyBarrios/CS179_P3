from manifest import ManifestItem


class Action:
    def __init__(self, source: ManifestItem, target: ManifestItem):
        self.source = source
        self.target = target
    
    def __str__(self) -> str:
        return f"Move {self.source.get_coordinate()} to {self.target.get_coordinate()}"
    
    def copy(self):
        return Action(self.source.copy(), self.target.copy())