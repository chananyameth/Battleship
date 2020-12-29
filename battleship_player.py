from hashlib import sha256
from random import randrange
from functools import reduce

from consts import *
from converters import coordinate_to_number, number_to_coordinate


class BattleshipPlayer:
    def __init__(self, submarines: dict = None):
        self.nonce = randrange(MIN_NONCE, MAX_NONCE)
        if not submarines:
            self.submarines = {Submarine.SUB_5: [coordinate_to_number(1, 1), VERTICAL_ORIENTATION],
                               Submarine.SUB_4: [coordinate_to_number(2, 8), HORIZONTAL_ORIENTATION],
                               Submarine.SUB_3_1: [coordinate_to_number(8, 1), VERTICAL_ORIENTATION],
                               Submarine.SUB_3_2: [coordinate_to_number(7, 5), VERTICAL_ORIENTATION],
                               Submarine.SUB_2: [coordinate_to_number(0, 7), VERTICAL_ORIENTATION]}  # default positions
        else:
            self.submarines = submarines
        self.board = populate_board(self.submarines)

    def at(self, column: int, row: int) -> Submarine:
        """get what is in a specific location on the board"""
        return self.board[coordinate_to_number(column, row)]

    def get_hash(self):
        return calculate_hash(self)


def calculate_hash(player: BattleshipPlayer) -> bytes:
    """calculate hash of player's board"""
    product = player.nonce
    product *= reduce(int.__mul__, [value[POSITION] for value in player.submarines.values()])
    product *= reduce(int.__mul__, [value[ORIENTATION] for value in player.submarines.values()])
    hash_holder = sha256()
    hash_holder.update(str(product).encode())
    return hash_holder.digest()


def populate_board(submarines: dict) -> list:
    """populate the board according to the given submarines"""
    board = [0x0 for _ in range(BOARD_SIDE_SIZE ** 2)]  # Empty board
    for sub_name, sub_data in submarines.items():
        column, row = number_to_coordinate(sub_data[POSITION])
        for i in range(sub_length[sub_name]):
            if sub_data[ORIENTATION] == VERTICAL_ORIENTATION:
                board[coordinate_to_number(column, row + i)] = sub_name
            else:
                board[coordinate_to_number(column + i, row)] = sub_name
    return board
