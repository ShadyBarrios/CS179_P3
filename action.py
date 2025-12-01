from manifest import ManifestItem


class Action:
    def __init__(self, source: ManifestItem, target: ManifestItem):
        self.source = source
        self.target = target
    
    def __str__(self) -> str:
        return f"Move {self.source.get_coordinate()} to {self.target.get_coordinate()}"
     
    # TODO: need to do dummy search, can't phase through things
    def manhattan_dist(self) -> int:
        row_diff = abs(self.source.get_row() - self.target.get_row())
        col_diff = abs(self.source.get_col() - self.target.get_col())

        return (row_diff + col_diff)