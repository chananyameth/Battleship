import hashlib

BOARD_SIDE_SIZE = 10

MIN_NONCE = 0
MAX_NONCE = 2 ** 32  # 4 bytes

INVALID_POSITION = -1
INVALID_ORIENTATION = -1

SUB_5 = 0x1
SUB_4 = 0x2
SUB_3_1 = 0x3
SUB_3_2 = 0x4
SUB_2 = 0x5


def coordinate_to_number(column: int, row: int) -> int:
    """pack column and row into one int"""
    return column + (BOARD_SIDE_SIZE * row)


def number_to_coordinate(coordinate: int) -> tuple(int, int):
    """get (column, row) tuple from an int representation of a coordinate"""
    return coordinate % BOARD_SIDE_SIZE, coordinate // BOARD_SIDE_SIZE


def calculate_hash(player):
    number = player.nonce
    number *=
    hasher = hashlib.sha256()
