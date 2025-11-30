from manifest import ManifestItem
class Action:
    def __init__(self, source: ManifestItem, target: ManifestItem):
        self.source = source
        self.target = target
    
    def manhattan_dist(self) -> int:
        row_diff = abs(self.source.get_row() - self.target.get_row())
        col_diff = abs(self.source.get_col() - self.target.get_col())

        return (row_diff + col_diff)