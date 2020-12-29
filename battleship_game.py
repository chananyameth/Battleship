from battleship_player import BattleshipPlayer
from packet_builder import *
from consts import *


class BattleshipGame:
    def __init__(self, opponent_address: str = None):
        """
        init one side of Battleship game.
        @:param opponent_address: if exists, we'll try to connect to the specified address,
                                  if not, we'll listen and wait for incoming players
        """
        self.version = 1
        self.player = BattleshipPlayer()
        self.opponent_hash = INVALID_HASH
        if opponent_address:
            self.send_game_request()
        else:
            self.listen_for_incoming_game()

    def send_game_request(self):
        # ..send
        game_invite_packet(self.version)

        # ..get game_accept

        # ..send_placing_inform
        placing_inform_packet(self.version, self.player)

        # ..get placing_inform

        # ..send turn
        # ..get turn-result
        # ..get turn
        # ..send turn-result

    def listen_for_incoming_game(self):
        # ..get game_invite

        # ..send
        game_accept_packet(self.version)

        # ..send_placing_inform
        placing_inform_packet(self.version, self.player)

        # ..get placing_inform

        # ..get turn
        # ..send turn-result
        # ..send turn
        # ..get turn-result
