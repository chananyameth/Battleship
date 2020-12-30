import sys
from battleship_game import BattleshipGame
from converters import coordinate_to_number
from consts import *


def get_x_y(sub_no, len):
    x, y = -1, -1
    while (not 0 <= x <= BOARD_SIDE_SIZE) or (not 0 <= y <= BOARD_SIDE_SIZE):
        try:
            x, y = map(int, input(f"Enter sub No. {sub_no} (len={len})'s top-left position: ").split())
        except ValueError:
            print("invalid input")
    return x, y


def get_orientation():
    orientation = -1
    while orientation != 0 and orientation != 1:
        try:
            orientation = int(input("Enter it's orientation (0 for vertical, 1 for horizontal): "))
        except ValueError:
            print("invalid input")
    return orientation


def get_submarines_positions_from_input():
    input_submarines = {Submarine.SUB_5: [coordinate_to_number(*get_x_y(sub_no=1, len=5)), get_orientation()],
                        Submarine.SUB_4: [coordinate_to_number(*get_x_y(sub_no=2, len=4)), get_orientation()],
                        Submarine.SUB_3_1: [coordinate_to_number(*get_x_y(sub_no=3, len=3)), get_orientation()],
                        Submarine.SUB_3_2: [coordinate_to_number(*get_x_y(sub_no=4, len=3)), get_orientation()],
                        Submarine.SUB_2: [coordinate_to_number(*get_x_y(sub_no=5, len=2)), get_orientation()]}
    return input_submarines


submarines = get_submarines_positions_from_input()
if len(sys.argv) == 1:
    player1 = BattleshipGame(submarines=submarines)
else:
    player2 = BattleshipGame(submarines=submarines, opponent_address=sys.argv[1])
