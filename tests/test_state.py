import utils

from coordinate import Coordinate
from manifest import ManifestItem
from state import State


def get_state(file_name) -> State:
    manifest_list = utils.parse_file(f'examples/{file_name}')
    grid = utils.create_grid_from_list(manifest_list)
    state = State(grid)
    return state

class TestState():

    state_3 = get_state("ShipCase3.txt")
    state_4 = get_state("ShipCase4.txt")
    state_5 = get_state("ShipCase5.txt")
    state_6 = get_state("ShipCase6.txt")
    state_6eq = get_state("ShipCase6.txt")
    state_6a = get_state("ShipCase6_same.txt")
    state_6b = get_state("ShipCase6_diff.txt")


    def test_str(self):
        manifest_list = utils.parse_file("examples/ShipCase3.txt")
        
        expected = "\n".join(map(str, manifest_list))
        assert str(self.state_3) == expected

    def test_eq_true(self):
        assert self.state_6 == self.state_6
        assert self.state_6 == self.state_6eq
        assert self.state_6 == self.state_6a
    
    def test_eq_false(self):
        assert self.state_6 != self.state_6b
        assert self.state_6 != 5
    
    def test_hash_eq(self):
        state_6copy = self.state_6.copy()
        assert hash(self.state_6) == hash(self.state_6)
        assert hash(self.state_6) == hash(self.state_6a)
        assert hash(self.state_6) == hash(state_6copy)
    
    def test_hash_diff(self):
        assert hash(self.state_6) != hash(self.state_6b)
        assert hash(self.state_6a) != hash(self.state_6b)

    def test__copy_grid(self):
        grid_copy = self.state_6._copy_grid()
        for row, row_copy in zip(grid_copy, self.state_6.get_grid()):
            for item, item_copy in zip(row, row_copy):
                assert item == item_copy
    
    def test__compare_weight_columns(self):
        # incorrect types should return false
        assert not self.state_6.__compare_weight_columns__(5)

    def test_copy(self):
        copy_state_6 = self.state_6.copy()
        assert self.state_6 == copy_state_6

        copy_state_6.crane = Coordinate(2, 1)
        copy_state_6.grid = [[]]

        assert self.state_6.crane == Coordinate(9, 1)
        assert self.state_6.grid != [[]]

    def test_get_row_count(self):
        assert self.state_6.get_row_count() == 8

    def test_get_column_count(self):
        assert self.state_6.get_col_count() == 12

    def test_get_grid(self):
        assert self.state_6.get_grid() == self.state_6eq.get_grid()

    def test_get_crane(self):
        assert self.state_6.get_crane() == Coordinate(9, 1)
        assert self.state_6eq.get_crane() == Coordinate(9, 1)

    def test_get_side_weights(self):
        assert (1101, 900) == self.state_6.get_side_weights()
        assert (1101, 900) == self.state_6eq.get_side_weights()
        assert (141, 0) == self.state_3.get_side_weights()
        assert (402, 0) == self.state_4.get_side_weights()
        assert (906, 100) == self.state_5.get_side_weights()

    def test_get_weight_list(self):
        assert self.state_3.get_weight_list() == [101, 40]
        assert self.state_4.get_weight_list() == [200, 103, 99]
        assert self.state_5.get_weight_list() == [101, 100, 99, 102, 504, 100]

    def test_get_moveable_items(self):
        movable_items = self.state_6.get_moveable_items()
        movable_items_eq = self.state_6eq.get_moveable_items()
        expected_items = [
            ManifestItem(Coordinate(1, 2), 61, ""),
            ManifestItem(Coordinate(1, 3), 40, ""),
            ManifestItem(Coordinate(1, 4), 334, ""),
            ManifestItem(Coordinate(1, 5), 333, ""),
            ManifestItem(Coordinate(1, 6), 333, ""),
            ManifestItem(Coordinate(1, 11), 900, "")
        ]

        expected_items_2 = [
            ManifestItem(Coordinate(1, 3), 101, "Fish for Wendys"), 
            ManifestItem(Coordinate(1, 6), 40, "Bikes")
        ]

        assert movable_items == expected_items
        assert movable_items_eq == expected_items
        assert self.state_3.get_moveable_items() == expected_items_2

    def test_get_side_weight_lists(self):
        p_weight_list, s_weight_list = self.state_6.get_side_weight_lists()
        p_weight_list_eq, s_weight_list_eq = self.state_6eq.get_side_weight_lists()
        p_expected = [[61], [40], [334], [333], [333]]
        s_expected = [[900]]
        assert p_weight_list == p_expected
        assert s_weight_list == s_expected

        assert p_weight_list_eq == p_expected
        assert s_weight_list_eq == s_expected

    def test_get_num_used_cells(self):
        assert self.state_3.get_num_used_cells() == 2
        assert self.state_4.get_num_used_cells() == 3
        assert self.state_5.get_num_used_cells() == 6

    def test_get_open_spots(self):
        state = get_state("NanShip.txt")
        expected = [
            ManifestItem(Coordinate(8, 6), 0, "UNUSED"),
            ManifestItem(Coordinate(8, 7), 0, "UNUSED")
        ]
        assert state.get_open_spots() == expected

    def test_is_symmetrical(self):
        assert self.state_3.is_symmetric()
        assert self.state_4.is_symmetric()
        assert self.state_5.is_symmetric()
        assert self.state_6.is_symmetric()
        
        bad_state = get_state("NotSymmetrical.txt")
        assert not bad_state.is_symmetric()

    def test_is_physically_possible(self):
        assert self.state_3.is_physically_possible()
        assert self.state_4.is_physically_possible()
        assert self.state_5.is_physically_possible()
        assert self.state_6.is_physically_possible()
        
        bad_state = get_state("NotPossible.txt")
        assert not bad_state.is_physically_possible()
    
    def test_valid_grid(self):
        assert self.state_3.valid_grid()
        assert self.state_4.valid_grid()

    def test_contains_no_ghost_weights(self):
        state = get_state("GhostWeights.txt")
        assert not state.contains_no_ghost_weights()
        assert self.state_3.contains_no_ghost_weights()



