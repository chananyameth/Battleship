import struct
from utils import *

GAME_INVITE_MESSAGE_TYPE = 0x1
GAME_ACCEPT_MESSAGE_TYPE = 0x2
PLACING_INFORM_MESSAGE_TYPE = 0x3
TURN_MESSAGE_TYPE = 0x4
TURN_RESULT_MESSAGE_TYPE = 0x5
PLACEMENT_INFORM_MESSAGE_TYPE = 0x6


def game_invite_packet(version: int) -> bytes:
    return struct.pack("BB", version, GAME_INVITE_MESSAGE_TYPE)


def game_accept_packet(version: int) -> bytes:
    return struct.pack("BB", version, GAME_ACCEPT_MESSAGE_TYPE)


def placing_inform_packet(version: int, player) -> bytes:
    return struct.pack("BB", version, PLACING_INFORM_MESSAGE_TYPE) + utils.calculate_hash(player)


def turn_packet(version: int, position: int) -> bytes:
    return struct.pack("BBB", version, TURN_MESSAGE_TYPE, position)


def turn_result_packet(version: int, is_hit: bool, submarine) -> bytes:
    # ? might pack into 1 byte instead of 1 bit
    return struct.pack("BB?B", version, TURN_RESULT_MESSAGE_TYPE, is_hit, submarine)


def placement_inform_packet(version: int, player) -> bytes:
    # ? might pack into 1 byte instead of 1 bit
    return struct.pack("BBB?B?B?B?B?i",
                       version,
                       PLACEMENT_INFORM_MESSAGE_TYPE,
                       *player.submarines[SUB_5],
                       *player.submarines[SUB_4],
                       *player.submarines[SUB_3_1],
                       *player.submarines[SUB_3_2],
                       *player.submarines[SUB_2],
                       player.nonce)
