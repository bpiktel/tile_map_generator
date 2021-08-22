import pickle
import os

import src.visualisation as tmv


class TileMapIO:
    """
    TileMapIO class contains methods of loading and saving map in different
    forms (image, string, serialization)
    """

    @staticmethod
    def save_map_image(image, path):
        if len(path) == 0:
            return
        if os.path.splitext(path)[1] != '.png':
            path += '.png'
        image.save(path)

    @staticmethod
    def display_map_in_termial(map_):
        print(tmv.get_string_map_representation(map_))

    @staticmethod
    def save_map_to_file(map_, path):
        if len(path) == 0:
            return
        if os.path.splitext(path)[1] != '.pickle':
            path += '.pickle'

        with open(path, "wb") as f:
            pickle.dump(map_, f)

    @staticmethod
    def load_map_from_file(path):
        if len(path) == 0:
            return None
        with open(path, "rb") as pickle_in:
            map_ = pickle.load(pickle_in)
        return map_
