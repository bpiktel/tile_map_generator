import numpy as np

from src.tile import TileTreeNode


class TileMap:
    """
    TileMap object stores 2D array of ids and tiles data corresponding to it.
    :param tiles:
    :type tiles: :class:'tile.Tile'
    :param map:
    :type map: :class:'numpy.ndarray'
    """

    def __init__(self, size_y, size_x, tiles):
        """
        Constructor method takes sizes of map as parameters and creates
        numpy 2D array filled with background tile id.
        """
        if size_x < 1 or size_y < 1:
            raise ValueError(f"Can't create map of size {size_y}x{size_x}")
        self._map = np.zeros((size_y, size_x), dtype=int)
        if not isinstance(tiles, TileTreeNode):
            raise TypeError(f"Expected TileTreeNode type but got{type(tiles)}")
        self._tiles = tiles
        self._map = np.full_like(
            self._map, self.get_background_tile_id())

    def update_map(self, raw_map):
        """Replaces map array with new one without changing tiles list."""
        self._map = raw_map

    def update_tiles(self, new_tiles):
        """Replaces map tiles definitions without changing map."""
        self._tiles = new_tiles

    def get_map(self):
        return self._map

    def get_tiles(self):
        return self._tiles

    def get_background_tile_id(self):
        return self._tiles.get_tile().get_id()
