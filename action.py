from manifest import ManifestItem
from cell import CellTypes
from enum import Enum

# used to determine if open spots or moveable objects are wanted (they use near identical algo's)
class Wanted(Enum):
    OpenSpots=1
    MoveableItems=2

class Action:
    
    def get_open_spots(grid:list[list[ManifestItem]]):
        open_spots = Action.get(Wanted.OpenSpots, grid)
        return open_spots

    def get_moveable_items(grid:list[list[ManifestItem]]):
        moveable_items = Action.get(Wanted.MoveableItems, grid)
        return moveable_items
    
    def get(desired:Wanted, grid:list[list[ManifestItem]]):
        wanted_items:list[ManifestItem] = []
        row_count = len(grid)
        col_count = len(grid[0])

        for row in range(row_count-1):
            for col in range(col_count):
                item = grid[row][col]
                if CellTypes.to_type(item.get_title()) == CellTypes.USED:
                    item_above = grid[row+1][col]
                    if CellTypes.to_type(item_above.get_title()) == CellTypes.UNUSED:
                        wanted_items.append(item if desired == Wanted.MoveableItems else item_above)
        
        return wanted_items