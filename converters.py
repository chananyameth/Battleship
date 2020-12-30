from consts import *


def coordinate_to_number(column: int, row: int) -> int:
    """pack column and row into one int"""
    return column + (BOARD_SIDE_SIZE * row)


def number_to_coordinate(coordinate: int) -> tuple:
    """get (column, row) tuple from an int representation of a coordinate"""
    return coordinate % BOARD_SIDE_SIZE, coordinate // BOARD_SIDE_SIZE
