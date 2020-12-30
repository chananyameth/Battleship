from hashlib import sha256
from random import randrange
from functools import reduce
from converters import coordinate_to_number, number_to_coordinate

from consts import *


class BattleshipPlayer:
    def __init__(self, submarines: dict):
        self.nonce = randrange(MIN_NONCE, MAX_NONCE)
        self.submarines = submarines
        self.board = populate_board(self.submarines)

    def at(self, column: int, row: int) -> Submarine:
        """get what is in a specific location on the board"""
        return self.board[coordinate_to_number(column, row)]

    def get_hash(self):
        return calculate_hash(self)

    def print_board(self):
        for i in range(len(self.board)):
            if i % BOARD_SIDE_SIZE == 0:
                print("")  # new line
            print(chr(submarines_characters_ord[self.board[i]]), sep="", end="")
        print("\n")  # new lines


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
    board = [Submarine.NO_SUB for _ in range(BOARD_SIDE_SIZE ** 2)]  # Empty board
    for sub_name, sub_data in submarines.items():
        column, row = number_to_coordinate(sub_data[POSITION])
        for i in range(submarines_length[sub_name]):
            if sub_data[ORIENTATION] == VERTICAL_ORIENTATION:
                board[coordinate_to_number(column, row + i)] = sub_name
            else:
                board[coordinate_to_number(column + i, row)] = sub_name
    return board
