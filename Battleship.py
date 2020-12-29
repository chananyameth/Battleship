import random
from utils import *


class BattleshipPlayer:
    def __init__(self):
        self.nonce = random.randrange(MIN_NONCE, MAX_NONCE)
        self.board = [0x0 for _ in range(BOARD_SIDE_SIZE ** 2)]  # Empty board
        self.submarines = {SUB_5: [INVALID_POSITION, INVALID_ORIENTATION],
                           SUB_4: [INVALID_POSITION, INVALID_ORIENTATION],
                           SUB_3_1: [INVALID_POSITION, INVALID_ORIENTATION],
                           SUB_3_2: [INVALID_POSITION, INVALID_ORIENTATION],
                           SUB_2: [INVALID_POSITION, INVALID_ORIENTATION]}  # Uninitialized submarines
