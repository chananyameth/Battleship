from os import system
from battleship_player import BattleshipPlayer
from network import Network
from socket import timeout
from converters import coordinate_to_number, number_to_coordinate
from packet_builder import *
from consts import *


def get_position_from_input():
    x, y = -1, -1
    while (not 0 <= x <= BOARD_SIDE_SIZE) or (not 0 <= y <= BOARD_SIDE_SIZE):
        try:
            x, y = map(int, input("Enter a position (x,y) to attack: ").split())
        except ValueError:
            print("invalid input")
    return coordinate_to_number(x, y)


class BattleshipGame:
    # beginning
    def __init__(self, submarines=default_submarines, opponent_address: str = None):
        """
        init one side of Battleship game.
        @:param opponent_address: if exists, we'll try to connect to the specified address,
                                  if not, we'll listen and wait for incoming players
        """
        # myself
        self.version = 1
        self.player = BattleshipPlayer(submarines)
        self.my_success_hits = 0

        # opponent
        self.opponent = BattleshipPlayer(submarines={})  # we don't know the enemy's board so let's begin with empty one
        self.opponents_success_hits = 0
        self.opponent_hash = INVALID_HASH

        # start game
        try:
            if opponent_address:
                self.connection = Network(PORT, opponent_address)
                self.start_game_active()
            else:
                self.connection = Network(PORT)
                self.start_game_passive()
        except timeout as _:
            print("The game finished because of timeout.")
        except exceptions.SubmarineGameError as error:
            print(f"The game finished unexpectedly. details:\n{error}")

    def start_game_active(self):
        self.send_game_invite()
        self.get_game_accept()

        self.send_placing_inform()
        self.get_placing_inform()

        self.print_boards()
        while True:
            self.make_turn()
            self.print_boards()
            if self.is_there_a_winner():
                break

            print("Waiting for a guess from your opponent")
            self.answer_to_opponents_turn()
            self.print_boards()
            if self.is_there_a_winner():
                break

        self.finish_game()

    def start_game_passive(self):
        self.get_game_invite()
        self.send_game_accept()

        self.send_placing_inform()
        self.get_placing_inform()

        while True:
            print("Waiting for a guess from your opponent")
            self.answer_to_opponents_turn()
            self.print_boards()
            if self.is_there_a_winner():
                break

            self.make_turn()
            self.print_boards()
            if self.is_there_a_winner():
                break

        self.finish_game()

    # game flow - starting
    def send_game_invite(self):
        self.connection.send(game_invite_packet(self.version))

    def get_game_invite(self):
        result = analyze(self.version, self.connection.receive())
        if not GAME_INVITE_MESSAGE_TYPE == result[0]:
            raise exceptions.UnexpectedMessageError

    def send_game_accept(self):
        self.connection.send(game_accept_packet(self.version))

    def send_placing_inform(self):
        self.connection.send(placing_inform_packet(self.version, self.player))

    def get_placing_inform(self):
        result = analyze(self.version, self.connection.receive())
        if not PLACING_INFORM_MESSAGE_TYPE == result[0]:
            raise exceptions.UnexpectedMessageError
            self.opponent_hash = result[1]

    # game flow - turns
    def make_turn(self):
        position = self.send_turn()
        self.get_turn_result(position)

    def send_turn(self):
        position = get_position_from_input()
        self.connection.send(turn_packet(self.version, position))
        return position

    def get_turn_result(self, position):
        result = analyze(self.version, self.connection.receive())
        if not TURN_RESULT_MESSAGE_TYPE == result[0]:
            raise exceptions.UnexpectedMessageError
        if result[1]:
            self.my_success_hits += 1
            self.opponent.board[position] = Submarine.HIT
        else:
            if not self.opponent.board[position] == Submarine.HIT:  # in case of re-guessing the same spot
                self.opponent.board[position] = Submarine.WATER

    def get_opponents_turn(self):
        result = analyze(self.version, self.connection.receive())
        if not TURN_MESSAGE_TYPE == result[0]:
            raise exceptions.UnexpectedMessageError

        position = result[1]
        if (not Submarine.NO_SUB == self.player.board[position]) \
                and (not Submarine.HIT == self.player.board[position]):
            sunken_sub = self.which_sub_sunk(result[1])
            is_hit = True
            self.opponents_success_hits += 1
            self.player.board[position] = Submarine.HIT  # this part of the submarine sunk
        else:
            sunken_sub = Submarine.NO_SUB
            is_hit = False
        return is_hit, sunken_sub

    def answer_to_opponents_turn(self):
        is_hit, sunken_sub = self.get_opponents_turn()
        self.send_turn_result(is_hit, sunken_sub)

    def send_turn_result(self, is_hit, sunken_sub):
        self.connection.send(turn_result_packet(self.version, is_hit, sunken_sub))

    def get_game_accept(self):
        result = analyze(self.version, self.connection.receive())
        if not GAME_ACCEPT_MESSAGE_TYPE == result[0]:
            raise exceptions.UnexpectedMessageError

    # game over
    def finish_game(self):
        if self.my_success_hits == sum(list(submarines_length.values())):
            print("You Won!!!")
        elif self.opponents_success_hits == sum(list(submarines_length.values())):
            print("You Lost...")

    # other
    def which_sub_sunk(self, position: int) -> Submarine:
        sub_name = self.player.board[position]
        sub_data = self.player.submarines[sub_name]
        column, row = number_to_coordinate(sub_data[POSITION])
        for i in range(submarines_length[sub_name]):
            if sub_data[ORIENTATION] == VERTICAL_ORIENTATION:
                if sub_name == self.player.at(column, row + i):
                    return Submarine.NO_SUB
            else:
                if sub_name == self.player.at(column + i, row):
                    return Submarine.NO_SUB
        return sub_name  # nothing left of this sub

    def is_there_a_winner(self):
        if self.my_success_hits == sum(list(submarines_length.values())) \
                or self.opponents_success_hits == sum(list(submarines_length.values())):
            return True
        return False

    def print_boards(self):
        system('cls')
        print("Your board:", end="")
        self.player.print_board()
        print("Opponent's board:", end="")
        self.opponent.print_board()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        player1 = BattleshipGame()
    else:
        player2 = BattleshipGame(opponent_address=sys.argv[1])
