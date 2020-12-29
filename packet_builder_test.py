import packet_builder
import Battleship
from utils import *
import pytest


def game_invite_packet_test():
    assert packet_builder.game_invite_packet(1) == b'\x01\x01'
    assert packet_builder.game_invite_packet(2) == b'\x02\x01'


def game_accept_packet_test():
    assert packet_builder.game_accept_packet(1) == b'\x01\x02'
    assert packet_builder.game_accept_packet(2) == b'\x02\x02'


def placing_inform_packet_test():
    player = Battleship.BattleshipPlayer()
    player.nonce = 456  # constant for testing
    assert packet_builder.placing_inform_packet(1, player) == \
           b"\x01\x03_\xec\xebf\xff\xc8o8\xd9Rxlmily\xc2\xdb\xc29\xddN\x91\xb4g)\xd7:'\xfbW\xe9"


def turn_packet_test():
    assert packet_builder.turn_packet(1, coordinate_to_number(1, 1)) == b'\x01\x04\x0b'
    assert packet_builder.turn_packet(2, coordinate_to_number(1, 0)) == b'\x02\x04\x01'
    assert packet_builder.turn_packet(1, coordinate_to_number(9, 9)) == b'\x01\x04\x63'


def turn_result_packet_test():
    assert packet_builder.turn_result_packet(1, True, Submarine.SUB_5) == b'\x01\x05\x01\x01'
    assert packet_builder.turn_result_packet(2, False, Submarine.SUB_3_1) == b'\x02\x05\x00\x03'


def placement_inform_packet_test():
    player = Battleship.BattleshipPlayer()
    player.nonce = 456  # constant for testing
    assert packet_builder.placement_inform_packet(1, player) == \
           b"\x01\x06\x0b\x00R\x01\x12\x009\x00F\x00\xc8\x01\x00\x00"


if __name__ == "__main__":
    game_invite_packet_test()
    game_accept_packet_test()
    placing_inform_packet_test()
    turn_packet_test()
    turn_result_packet_test()
    placement_inform_packet_test()
