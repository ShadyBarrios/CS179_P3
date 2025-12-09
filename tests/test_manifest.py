from coordinate import Coordinate
from enums import CellTypes, ItemPosition
from manifest import ManifestItem


class TestManifestItem():
    a = ManifestItem(Coordinate(1, 1), 1, "Item 1")
    b = ManifestItem(Coordinate(1, 1), 1, "Item 2")
    c = ManifestItem(Coordinate(1, 1), 2, "Item 3")
    d = ManifestItem(Coordinate(2, 2), 1, "Item 4")
    e = ManifestItem(Coordinate(1, 8), 30, "Item 5")

    unused = ManifestItem(Coordinate(1, 9), 0, "UNUSED")
    nan = ManifestItem(Coordinate(1, 10), 0, "NAN")

    def test_str(self):
        assert str(self.a) == "[01,01], {000001}, Item 1"
        assert str(self.unused) == "[01,09], {000000}, UNUSED"
        assert str(self.nan) == "[01,10], {000000}, NAN"

    def test_eq(self):
        assert self.a == self.b
        assert self.b == self.a

        assert self.a != self.c
        assert self.b != self.c

        assert self.a != self.d
        assert self.b != self.d
        assert self.c != self.d

        # comparison with wrong type returns false
        assert self.a != 5
        assert self.a.get_coordinate() != (1, 1)

    def test_copy(self):
        new_manifest_item = self.a.copy()
        assert new_manifest_item == self.a
        assert new_manifest_item.get_coordinate() == self.a.get_coordinate()
        assert new_manifest_item.get_weight() == self.a.get_weight()
        assert new_manifest_item.get_title() == self.a.get_title()

    def test_hash_eq(self):
        manifest_list = [self.a, self.b]
        manifest_set = {item for item in manifest_list}
        assert hash(manifest_list[0]) == hash(manifest_list[1])
        assert len(manifest_set) == 1

    def test_hash_diff(self):
        manifest_list = [self.b, self.c]
        manifest_set = {item for item in manifest_list}
        assert len(manifest_set) == 2

        manifest_list.append(self.d)
        manifest_set = {item for item in manifest_list}
        assert len(manifest_set) == 3

    def test_get_coordinate(self):
        assert self.a.get_coordinate() == Coordinate(1, 1)
        assert self.b.get_coordinate() == Coordinate(1, 1)
        assert self.c.get_coordinate() == Coordinate(1, 1)
        assert self.d.get_coordinate() == Coordinate(2, 2)

    def test_get_row(self):
        assert self.a.get_row() == 1
        assert self.b.get_row() == 1
        assert self.c.get_row() == 1
        assert self.d.get_row() == 2
    
    def test_get_col(self):
        assert self.a.get_col() == 1
        assert self.b.get_col() == 1
        assert self.c.get_col() == 1
        assert self.d.get_col() == 2

    def test_get_title(self):
        assert self.a.get_title() == "Item 1"
        assert self.b.get_title() == "Item 2"
        assert self.c.get_title() == "Item 3"
        assert self.d.get_title() == "Item 4"
    
    def test_get_weight(self):
        assert self.a.get_weight() == 1
        assert self.b.get_weight() == 1
        assert self.c.get_weight() == 2
        assert self.d.get_weight() == 1
    
    def test_get_position(self):
        assert self.a.get_position() == ItemPosition.PORT
        assert self.b.get_position() == ItemPosition.PORT
        assert self.c.get_position() == ItemPosition.PORT
        assert self.d.get_position() == ItemPosition.PORT

        assert self.e.get_position() == ItemPosition.STARBOARD
        assert self.unused.get_position() == ItemPosition.STARBOARD
        assert self.nan.get_position() == ItemPosition.STARBOARD

    def test_get_type(self):
        assert self.a.get_type() == CellTypes.USED
        assert self.e.get_type() == CellTypes.USED
        assert self.unused.get_type() == CellTypes.UNUSED
        assert self.nan.get_type() == CellTypes.NAN

    def test_set_coordinate(self):
        self.a.set_coordinate(Coordinate(9, 1))
        assert self.a.coordinate == Coordinate(9, 1)

        self.a.set_coordinate(Coordinate(1, 1))
        assert self.a.coordinate == Coordinate(1, 1)

    def test_is_park(self):
        park = ManifestItem(Coordinate(9, 1), 0, "UNUSED")
        assert park.is_park()
        assert not self.b.is_park()
    
    def test_directly_below(self):
        above_a = ManifestItem(Coordinate(2, 1), 0, "UNUSED")
        above_above_a = ManifestItem(Coordinate(3, 1), 0, "NAN")

        assert self.a.directly_below(above_a)
        assert not self.a.directly_below(above_above_a)
        assert above_a.directly_below(above_above_a)
        
        # comparison with wrong type returns false
        assert not self.a.directly_below(5)