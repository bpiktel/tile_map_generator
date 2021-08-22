import numpy as np

from src.generator import BorderGeneration as BG


def test_searching_for_coordinates():
    sample_raw_map = [[0, 0, 1, 2],
                      [3, 4, 1, 3],
                      [8, 3, 4, 1]]
    sample_map = BG(sample_raw_map, 1)
    searched_coord_tuples = sample_map.get_coordinate_tuples(1)
    assert searched_coord_tuples == [(1, 3), (2, 3), (3, 4)]


def test_getting_adjacent_coords():
    assert BG.get_adj_coords((1, 2)) == [(0, 2), (1, 3), (1, 1), (2, 2)]


def test_border_tile_check():
    sample_raw_map = [[0, 0, 1, 2],
                      [3, 4, 1, 3],
                      [8, 3, 4, 1]]
    generator = BG(sample_raw_map, 0)
    assert generator.check_if_border_tile((2, 2), 0)
    assert not generator.check_if_border_tile((3, 3), 0)


def test_mask():
    sample_raw_map = [[0, 0, 0, 0],
                      [0, 1, 1, 0],
                      [0, 0, 0, 0]]
    generator = BG(sample_raw_map, 1)
    generator.apply_mask(1)
    masked_raw_map = generator.get_trimmed_map()
    assert not np.all(masked_raw_map == -1)


def test_randomizing_fills():
    fills = BG.get_fill_per_island(0.2, 3)
    assert len(fills) == 3


def test_lists_comparision():
    list1 = [(0, 0), (2, 4), (4, 3)]
    list2 = [(0, 3), (0, 0), (1, 1), (4, 3)]
    assert BG.coords_in_both_lists(list1, list2) == [(0, 0), (4, 3)]


def test_applying_section():
    map1 = np.array([[1, 1, 1, 1], [3, 4, 1, 1], [1, 1, 1, 1]]).reshape(3, 4)
    map2 = np.array([[3, 5, 0, 0], [1, 1, 0, 0], [0, 0, -1, 0]]).reshape(3, 4)
    map1 = BG.apply_generated_section(map1, map2, 1)
    assert np.all(map1 == 1)
