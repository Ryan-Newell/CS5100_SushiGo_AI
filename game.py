# %load_ext autoreload
import pandas as pd

from Player.MinimaxPlayer import MinimaxPlayer
from State import *
from Player import *
from Player import ApproxQPlayer
from Player import MCTSPlayer
from Player import MinimaxPlayer
from Player import MCTSPlayer
import plotly.express as px
from tqdm import tqdm
import json

#%%

state = State(get_actual_card_pool())
state2 = State(get_actual_card_pool())
def rungame():
    # p2 = RulePlayer('Player 1', 'plus')
    p1 = RulePlayer('Player 2', 'plus')
    # p2 = QPlayer('Player 2', learning_rate=0.6, discount_factor=0.9)
    p2 = ApproxQPlayer.ApproxQPlayer('Player 2')
    # p2 = RandomPlayer('Player 2')
    # p1.model_dict = json.loads(open('./models/model1.json').read())
    # p2 = RandomPlayer('Player 2')
    # p1 = MinimaxPlayer.MinimaxPlayer('Player 1')
    # p1 = MCTSPlayer.MCTSPlayer('Player 1', 300000)
    # p2 = RandomPlayer('Player 2')
    p3 = HumanPlayer('Player1')
    # p3 = HumanPlayer('Player1')
    state.add_player(p1)
    state.add_player(p2)


    state.play_games(5000, output_result=False)

    state2.add_player(p2)
    state2.add_player(p3)
    print("ready to rumble!")
    state2.play_games(5, output_result=True)
#
#
#
# state.add_player(p1)
# state.add_player(p2)
# state.add_player(p3)
# state.add_player(p4)



# state.play_games(num_of_games=1000000, round_per_game=3, output_result=True)

# all_results.append(state.stats)
# print(all_results)


# x = [0, 0, 0, 0, 0]
# y = [0, 0, 0, 0, 0]
# for i in range(5):
#     state = State(get_actual_card_pool())
#     p1 = RulePlayer('Player 1')
#     p2 = QPlayer('Player 2', learning_rate=0.1, discount_factor=0.01)
#     state.add_player(p1)
#     state.add_player(p2)
#     df = pd.DataFrame()
#     all_results = []
#
#     state.play_games(num_of_games=50000, round_per_game=1, output_result=False)
#     all_results.append(state.stats)
#     [[x[i], y[i]]] = all_results
#
# print(x, y)
# print(sum(x)/len(x), sum(y)/len(y))





# def rungame():
#     # p1 = RulePlayer('Player 2', 'plus')
#     p2 = RulePlayer('Player 2')
#     # p1.model_dict = json.loads(open('./models/model1.json').read())
#     # p2 = RandomPlayer('Player 2')
#     p1 = MinimaxPlayer.MinimaxPlayer('Player 1', False)
#     # p2 = RandomPlayer('Player 2')
#     # p2 = HumanPlayer('Player1')
#
#     state.add_player(p1)
#     state.add_player(p2)
#
#     df = pd.DataFrame()
#     all_results = []
#     hit_rates = []
#
#     state.play_games(1000, output_result=False)



# def manualscore(cards1, cards2):
#     board1 = [0] * len(CARD_ON_BOARD)
#     board2 = [0] * len(CARD_ON_BOARD)
#     for card in cards1:
#         add_a_card_to_board(board1, card)
#     for card in cards2:
#         add_a_card_to_board(board2, card)
#     return score_game([board1, board2])


# c1 = [4,0,1,6]
# c2 = [0,7,6,2]
# print(manualscore(c1, c2))
rungame()

