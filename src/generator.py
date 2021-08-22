from random import choice, randrange
from math import floor

import numpy as np


class TileMapGenerator:
    """
    TileMapGenerator class contains methods of splitting tile map generation
    into steps of generating single tile type.
    """

    def generate_map(self, tile_map):
        """Splits map into map of ids and tiles object and combines
        generated map of ids with tiles"""
        raw_map = tile_map.get_map()
        tiles = tile_map.get_tiles()

        self.generate_section(raw_map, tiles)
        tile_map.update_map(raw_map)
        return tile_map

    def generate_section(self, raw_map, tile_tree_node):
        """Calls generation of each tile id"""
        parent_tile = tile_tree_node.get_tile()
        children = tile_tree_node.get_children()

        for tile_node in children:
            tile = tile_node.get_tile()
            gen = BorderGeneration(raw_map, parent_tile.get_id())
            raw_map = gen.generate_tile(raw_map,
                                        parent_tile.get_id(),
                                        tile.get_id(),
                                        tile.get_fill(),
                                        tile.get_islands())
            self.generate_section(raw_map, tile_node)


class BorderGeneration:
    """
    BorderGeneration class collects methods used to generate 'islands' of child
    id type on parent id type on numpy 2D array.
    :param raw_map: 2D array of tiles ids.
    :type raw_map: :class:'numpy.ndarray'
    :param parent_id: Parent tile id, on which tile islands will be generated.
    :type parent_id: int
    """

    def __init__(self, raw_map, parent_id):
        """Adds padding around map to avoid getting out of bounds and masks
        all ids not suitable for generation"""
        self._map = np.pad(
            raw_map, (1, 1), mode='constant', constant_values=-1)
        self._map[self._map != parent_id] = -1
        self._parent_id = parent_id

    def generate_tile(self, raw_map, parent_tile, tile_id, fill, islands=1):
        """Generates single tile type. Creates non connecting islands
        one by one and applying mask around them to avoid connections"""
        number_of_tiles = len(self.get_coordinate_tuples(self._parent_id))
        for fill in self.get_fill_per_island(fill, islands):
            self.apply_mask(tile_id)  # apply mask to avoid connections
            n_tiles_to_gen = floor(number_of_tiles * fill)
            self.generate_island(n_tiles_to_gen, self._parent_id, tile_id)
            gen_map = self.get_trimmed_map()
        raw_map = self.apply_generated_section(raw_map, gen_map, tile_id)
        return raw_map

    def apply_mask(self, tile_id):
        """Applies mask of -1 around existing islands to avoid connections"""
        for coord in self.get_coordinate_tuples(tile_id):
            for c in self.get_adj_coords(coord, mode='all'):
                if self._map[c] != tile_id:
                    self._map[c] = -1
        np.put(self._map, tile_id, -1)

    @staticmethod
    def apply_generated_section(output_map, map_to_apply, id_to_apply):
        """Applies generated tile id on map"""
        for row_number, row in enumerate(map_to_apply):
            for column_number, id_ in enumerate(row):
                if id_ == id_to_apply:
                    output_map[row_number, column_number] = id_
        return output_map

    @staticmethod
    def get_fill_per_island(fill, islands, size_diff=5):
        """Randomizes island sizes. Biggest islands can be
        size_diff times bigger that smallest islands"""
        random_sizes = [randrange(1, size_diff) for i in range(islands)]
        sum_of_sizes = sum(random_sizes)
        fills = [size / sum_of_sizes * fill for size in random_sizes]
        return fills

    def generate_island(self, tiles_to_generate, parent_id, child_id):
        """Main generation code. Selects seed around which new tiles will
        appear. First chooeses tile that borders with parent tile
        and generates new tile on random side of selected tile.
        Note that island number has priority over fill so if there are no
        locations to generate new tile result will have less fill, but
        number of islands will be preserved"""
        # selecting seed
        coord_tuples = self.get_coordinate_tuples(parent_id)
        seed = self.get_seed_coordinates(coord_tuples)
        self._map[seed] = child_id

        border_tiles = [seed]

        for x in range(tiles_to_generate - 1):
            # exit if no places to generate
            if len(border_tiles) == 0:
                return
            # generating new tile
            selected_tile = self.get_chosen_tile_coord(border_tiles, parent_id)
            self._map[selected_tile] = child_id
            # check if any adjecent tiles stopped being border tiles
            tiles_adj = self.get_adj_coords(selected_tile)
            tiles_to_check = self.coords_in_both_lists(
                tiles_adj, border_tiles)
            for tile_coord in tiles_to_check:
                if not self.check_if_border_tile(tile_coord, parent_id):
                    border_tiles.remove(tile_coord)
            # check if generated tile becomes border tile
            if self.check_if_border_tile(selected_tile, parent_id):
                border_tiles.append(selected_tile)

    def get_coordinate_tuples(self, searched_id):
        """Returns list of tuples of coordinates of all tiles on map
        with searched id"""
        tuples = []
        for row_number, row in enumerate(self._map):
            for column, id_ in enumerate(row):
                if id_ == searched_id:
                    tuples.append((row_number, column))
        return tuples

    def get_seed_coordinates(self, coord_tuples):
        """Returns random seed coordinate from list of suitable coordinates"""
        return choice(coord_tuples)

    def get_chosen_tile_coord(self, border_tiles, parent_id):
        """Returns coordinate of tile to fill from suitable locations
        around selected border tile"""
        coord = choice(border_tiles)
        options = [c for c in self.get_adj_coords(coord)
                   if self._map[c] == parent_id]
        return choice(options)

    def check_if_border_tile(self, coord, parent_id):
        """Checks if around tile there are any spaces left to generate"""
        for c in self.get_adj_coords(coord):
            if self._map[c] == parent_id:
                return True
        return False

    @staticmethod
    def get_adj_coords(coord, mode='sides'):
        """Returns coordinates adjacent to selected with mode being only sides,
        only corners or all coordinates around"""
        SIDES = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        CORNERS = [(-1, 1), (-1, -1), (1, 1), (1, -1)]

        if mode == 'sides':
            adj = SIDES
        elif mode == 'corners':
            adj = CORNERS
        elif mode == 'all':
            adj = SIDES + CORNERS

        return [(y + coord[0], x + coord[1]) for y, x in adj]

    @staticmethod
    def coords_in_both_lists(list1, list2):
        return [c for c in list1 if c in list2]

    def get_trimmed_map(self):
        """Returns map trimmed of added bounds"""
        return self._map[1:-1, 1:-1]
