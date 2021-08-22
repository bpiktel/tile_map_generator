class Tile:
    """
    Tile object contains data used to generate and visualize tile map.
    :param id: Unique number that TileMap class uses to store maps, must be
               positive or 0
    :type id: int
    :param name: Name of tile type
    :type name: str
    :param color: Color of tile when exported to image
    :type color: str
    :param fill: Value from 0 to 1 that expresses how much of parent tile type
    will be converted to this tile type
    :type fill: float
    :param islands: Number of separate bodies of this tile type
    :type islands: int

    :raises: :class:'ValueError': Fill value must be from range of 0 to 1
    :raises: :class:'ValueError': ID cannot be negative number
    """

    def __init__(self, id_, name, color, fill=0.2, islands=1):
        if id_ < 0:
            raise ValueError("ID cannot be negative number")
        self._id = id_
        self._name = name
        self._color = color
        if fill < 0 or fill > 1:
            raise ValueError("Fill value must be from range of 0 to 1")
        self._fill = fill
        self._islands = islands

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_fill(self):
        return self._fill

    def get_islands(self):
        return self._islands

    def get_info(self):
        """Returns string with basic tile information"""
        return f"{self._id}, {self._name} - color: {self._color}, " + \
               f"fill: {self._fill}, islands: {self._islands}"


class TileTreeNode:
    """
    TileTreeNode object is used to organise Tile objects in hierarchy that is
    later used in map generation. Every tile is stored in one node as parent
    tile with list of child tiles that can be generated on it.
    :param tile: Tile object storing tile data
    :type tile: Tile
    :param children: List of children tiles for tile, defaults to None
    :type children: list
    """

    def __init__(self, tile, children=None):
        self._tile = tile
        if children is None:
            self._children = []
        else:
            self._children = children

    def get_tile(self):
        return self._tile

    def get_children(self):
        return self._children

    def add_child(self, child):
        self._children.append(child)

    def get_names_list(self):
        """Recursively collect names of node and child nodes"""
        names = [self.get_tile().get_name()]
        for child in self._children:
            names += child.get_names_list()
        return names

    def get_id_color_tuple(self):
        tile = self.get_tile()
        return (tile.get_id(), tile.get_color())

    def get_colors_list(self):
        """
        Returns list of tuples with id of tile and color associated with it
        of all child nodes of this node (and tile from this node)
        :return: List of tuples with color and id
        :rtype: list
        """
        id_color_tuples = []
        id_color_tuples.append(self.get_id_color_tuple())
        for node in self._children:
            id_color_tuples += node.get_colors_list()
        return id_color_tuples
