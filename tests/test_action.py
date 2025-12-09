from action import Action
from coordinate import Coordinate
from manifest import ManifestItem

class TestAction():
    action = Action(ManifestItem(Coordinate(1, 1), 5, "Item 1"), ManifestItem(Coordinate(1, 3), 0, "UNUSED"))
    
    def test_str(self):
        assert str(self.action) == "Move [01,01] to [01,03]"

    def test_copy(self):
        action_copy = self.action.copy()

        assert str(action_copy) == str(self.action)
    
