from enum import Enum

BOARD_SIDE_SIZE = 10

MIN_NONCE = 0
MAX_NONCE = 2 ** 32  # 4 bytes

POSITION = 0
ORIENTATION = 1
INVALID_POSITION = -1
INVALID_ORIENTATION = -1
VERTICAL_ORIENTATION = 0x0
HORIZONTAL_ORIENTATION = 0x1


class Submarine(Enum):
    NO_SUB = 0x0
    SUB_5 = 0x1
    SUB_4 = 0x2
    SUB_3_1 = 0x3
    SUB_3_2 = 0x4
    SUB_2 = 0x5


sub_length = {Submarine.NO_SUB: 0,
              Submarine.SUB_5: 5,
              Submarine.SUB_4: 4,
              Submarine.SUB_3_1: 3,
              Submarine.SUB_3_2: 3,
              Submarine.SUB_2: 2}


def coordinate_to_number(column: int, row: int) -> int:
    """pack column and row into one int"""
    return column + (BOARD_SIDE_SIZE * row)


def number_to_coordinate(coordinate: int) -> tuple:
    """get (column, row) tuple from an int representation of a coordinate"""
    return coordinate % BOARD_SIDE_SIZE, coordinate // BOARD_SIDE_SIZE
