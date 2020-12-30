from enum import Enum

# Player stuff
INVALID_HASH = -1

BOARD_SIDE_SIZE = 10

MIN_NONCE = 0
MAX_NONCE = 2 ** 32  # 4 bytes

HASH_SIZE = 32  # 32 bytes

# ------------------------------------------
# Timeouts, in seconds
GAME_ACCEPT_TIMEOUT = 60
PLACING_INFORM_TIMEOUT = 60 * 10
TURN_TIMEOUT = 60 * 10
TURN_RESULT_TIMEOUT = 10
PLACEMENT_INFO_TIMEOUT = 10

# ------------------------------------------
# Network
PORT = 8300
MAX_MESSAGE_SIZE_VERSION_1 = 34

VERSION_OFFSET = 0
MESSAGE_TYPE_OFFSET = 1
DATA_OFFSET = 2

GAME_INVITE_MESSAGE_TYPE = 0x1
GAME_ACCEPT_MESSAGE_TYPE = 0x2
PLACING_INFORM_MESSAGE_TYPE = 0x3
TURN_MESSAGE_TYPE = 0x4
TURN_RESULT_MESSAGE_TYPE = 0x5
PLACEMENT_INFORM_MESSAGE_TYPE = 0x6

# ------------------------------------------
# Submarine stuff
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

    # to show opponent's ships
    HIT = 0x6
    WATER = 0x7


submarines_length = {Submarine.NO_SUB: 0,
                     Submarine.SUB_5: 5,
                     Submarine.SUB_4: 4,
                     Submarine.SUB_3_1: 3,
                     Submarine.SUB_3_2: 3,
                     Submarine.SUB_2: 2,
                     Submarine.HIT: 0,
                     Submarine.WATER: 0}

submarines_characters_ord = {Submarine.NO_SUB: 45,
                             Submarine.SUB_5: 35,
                             Submarine.SUB_4: 35,
                             Submarine.SUB_3_1: 35,
                             Submarine.SUB_3_2: 35,
                             Submarine.SUB_2: 35,
                             Submarine.HIT: 4,
                             Submarine.WATER: 21}

default_submarines = {Submarine.SUB_5: [11, VERTICAL_ORIENTATION],
                      Submarine.SUB_4: [82, HORIZONTAL_ORIENTATION],
                      Submarine.SUB_3_1: [18, VERTICAL_ORIENTATION],
                      Submarine.SUB_3_2: [57, VERTICAL_ORIENTATION],
                      Submarine.SUB_2: [70, VERTICAL_ORIENTATION]}  # default positions
