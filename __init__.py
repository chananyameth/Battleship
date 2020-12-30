import sys
from battleship_game import BattleshipGame

if len(sys.argv) == 1:
    player1 = BattleshipGame()
else:
    player2 = BattleshipGame(opponent_address=sys.argv[1])
