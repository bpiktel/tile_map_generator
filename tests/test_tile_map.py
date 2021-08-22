import pytest
import numpy as np

from src.tile_map import TileMap
from src.tile import Tile
from src.tile import TileTreeNode


def test_constructor():
    tm = TileMap(3, 5, TileTreeNode(Tile(0, "", "")))
    assert tm.get_map().shape == (3, 5)
    assert np.count_nonzero(tm.get_map()) == 0


def test_wrong_data():
    with pytest.raises(ValueError):
        TileMap(-2, 4, TileTreeNode(Tile(0, "", "")))
    with pytest.raises(TypeError):
        TileMap(2, 4, 5)
