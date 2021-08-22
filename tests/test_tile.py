import pytest

from src.tile import Tile, TileTreeNode


def test_ttn_structure():
    sample_ttn = TileTreeNode(Tile(0, '0', 'red'),
                              [TileTreeNode(Tile(1, '1', 'green', 0.3, 2)),
                               TileTreeNode(Tile(2, '2', 'blue'),
                                            [TileTreeNode(Tile(3, '3', 'red'))
                                             ])
                               ])
    first_child = sample_ttn.get_children()[0].get_tile()
    assert first_child.get_id() == 1
    assert first_child.get_name() == "1"
    assert first_child.get_color() == 'green'
    assert first_child.get_fill() == 0.3
    assert first_child.get_islands() == 2


def test_malformed_tile_info():
    with pytest.raises(ValueError):
        Tile(-1, '', 'red', 0.2, 1)
    with pytest.raises(ValueError):
        Tile(0, '', 'red', 1.2, 1)


def test_tiles_info():
    test_tile = Tile(0, 'n', 'red', 0.2, 1)
    assert test_tile.get_info() == "0, n - color: red, fill: 0.2, islands: 1"


def test_color_list_generation():
    sample_ttn = TileTreeNode(Tile(0, '0', 'red'),
                              [TileTreeNode(Tile(1, '1', 'green')),
                               TileTreeNode(Tile(2, '2', 'blue'),
                                            [TileTreeNode(Tile(3, '3', 'red'))
                                             ])
                               ])

    colors_list = sample_ttn.get_colors_list()

    assert colors_list == [(0, 'red'), (1, 'green'), (2, 'blue'), (3, 'red')]


def test_names_list():
    sample_ttn = TileTreeNode(Tile(0, '0', 'red'),
                              [TileTreeNode(Tile(1, '1', 'green')),
                               TileTreeNode(Tile(2, '2', 'blue'),
                                            [TileTreeNode(Tile(3, '3', 'red'))
                                             ])
                               ])
    assert sample_ttn.get_names_list() == ['0', '1', '2', '3']
