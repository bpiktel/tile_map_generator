from PIL import Image, ImageDraw


class TileMapVisualisation():
    """
    TileMapVisualisation class containing methods of string or
    image representation of tile map
    """

    @staticmethod
    def get_string_map_representation(t_map):
        """Method used get map representation to show in terminal"""
        tiles = t_map.get_tiles()
        raw_map = t_map.get_map()

        string_map = ""
        string_map += TileMapVisualisation.get_tiles_tree(tiles)
        string_map += '\n'
        string_map += TileMapVisualisation.get_map_of_ids(raw_map)
        return string_map

    @staticmethod
    def get_tiles_tree(tiles, step=0):
        tree = ""
        tree += '\t' * step + tiles.get_tile().get_info()
        for child in tiles.get_children():
            tree += '\n'
            tree += TileMapVisualisation.get_tiles_tree(child, step + 1)
        return tree

    @staticmethod
    def get_map_of_ids(id_map):
        p_map = ""

        for row in id_map:
            for id_ in row:
                p_map += f"{str(id_):2}"
                p_map += ' '
            p_map += '\n'
        return p_map

    @staticmethod
    def get_map_image(tile_map, tile_size=10):
        """Returns PIL.Image object of tile map"""
        raw_map = tile_map.get_map()
        tiles = tile_map.get_tiles()

        map_shape = raw_map.shape
        size = (map_shape[1]*tile_size, map_shape[0]*tile_size)
        map_image = Image.new('RGB', size)

        fill_colors = {}
        for id_color_tuple in tiles.get_colors_list():
            fill_colors[id_color_tuple[0]] = id_color_tuple[1]

        for row_number, row in enumerate(raw_map):
            for column_number, id_ in enumerate(row):
                # white color if tile data is missing
                fill_color = fill_colors.get(id_, 'white')
                ImageDraw.Draw(map_image).rectangle([
                    (column_number*tile_size, row_number*tile_size),
                    ((column_number+1)*tile_size, (row_number+1)*tile_size)],
                    outline='#000', fill=fill_color)

        return map_image
