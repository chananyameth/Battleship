import struct
from consts import *
from battleship_player import BattleshipPlayer
import exceptions


def game_invite_packet(version: int) -> bytes:
    return struct.pack("BB", version, GAME_INVITE_MESSAGE_TYPE)


def game_accept_packet(version: int) -> bytes:
    return struct.pack("BB", version, GAME_ACCEPT_MESSAGE_TYPE)


def placing_inform_packet(version: int, player: BattleshipPlayer) -> bytes:
    return struct.pack("BB", version, PLACING_INFORM_MESSAGE_TYPE) + player.get_hash()


def turn_packet(version: int, position: int) -> bytes:
    return struct.pack("BBB", version, TURN_MESSAGE_TYPE, position)


def turn_result_packet(version: int, is_hit: bool, submarine: Submarine) -> bytes:
    # ? might pack into 1 byte instead of 1 bit
    return struct.pack("BB?B", version, TURN_RESULT_MESSAGE_TYPE, is_hit, submarine.value)


def placement_inform_packet(version: int, player) -> bytes:
    # ? might pack into 1 byte instead of 1 bit
    return struct.pack("BBB?B?B?B?B?i",
                       version,
                       PLACEMENT_INFORM_MESSAGE_TYPE,
                       *player.submarines[Submarine.SUB_5],
                       *player.submarines[Submarine.SUB_4],
                       *player.submarines[Submarine.SUB_3_1],
                       *player.submarines[Submarine.SUB_3_2],
                       *player.submarines[Submarine.SUB_2],
                       player.nonce)


def analyze(version: int, data: bytes) -> tuple:
    try:
        if not struct.unpack_from("B", data, VERSION_OFFSET)[0] == version:
            raise exceptions.InvalidVersionError

        message_type, = struct.unpack_from("B", data, MESSAGE_TYPE_OFFSET)
        if GAME_INVITE_MESSAGE_TYPE == message_type:
            return message_type,
        elif GAME_ACCEPT_MESSAGE_TYPE == message_type:
            return message_type,
        elif PLACING_INFORM_MESSAGE_TYPE == message_type:
            enemy_hash = data[DATA_OFFSET:DATA_OFFSET + HASH_SIZE]
            return message_type, enemy_hash
        elif TURN_MESSAGE_TYPE == message_type:
            square, = struct.unpack_from("B", data, DATA_OFFSET)
            return message_type, square
        elif TURN_RESULT_MESSAGE_TYPE == message_type:
            is_hit, ship = struct.unpack_from("?B", data, DATA_OFFSET)
            return message_type, is_hit, ship
        elif PLACEMENT_INFORM_MESSAGE_TYPE == message_type:
            ship5position, ship5orientation, \
            ship4position, ship4orientation, \
            ship31position, ship31orientation, \
            ship32position, ship32orientation, \
            ship2position, ship2orientation, \
            nonce \
                = struct.unpack_from("B?B?B?B?B?i", data, DATA_OFFSET)
            submarines = {Submarine.SUB_5: [ship5position, ship5orientation],
                          Submarine.SUB_4: [ship4position, ship4orientation],
                          Submarine.SUB_3_1: [ship31position, ship31orientation],
                          Submarine.SUB_3_2: [ship32position, ship32orientation],
                          Submarine.SUB_2: [ship2position, ship2orientation]}
            player = BattleshipPlayer(submarines=submarines)
            player.nonce = nonce
            return message_type, player
        else:
            raise exceptions.InvalidMessageCodeError
    except Exception as error:
        raise exceptions.InvalidMessageError(error)
