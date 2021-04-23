# %load_ext autoreload
import pandas as pd

from Player.MinimaxPlayer import MinimaxPlayer
from State import *
from Player import *
from Player import MinimaxPlayer
import plotly.express as px
from tqdm import tqdm
import json

#%%

state = State(get_actual_card_pool())
def rungame():
    p2 = RulePlayer('Player 2')
    # p1.model_dict = json.loads(open('./models/model1.json').read())
    # p2 = RandomPlayer('Player 2')
    p1 = MinimaxPlayer.MinimaxPlayer('Player 1')
    # p2 = RandomPlayer('Player 2')

    state.add_player(p1)
    state.add_player(p2)

    df = pd.DataFrame()
    all_results = []
    hit_rates = []

    state.play_games(1000, output_result=True)

# state.play_games(num_of_games=1000000, round_per_game=3, output_result=True)
# all_results.append(state.stats)
# print(all_results)


def manualscore(cards1, cards2):
    board1 = [0] * len(CARD_ON_BOARD)
    board2 = [0] * len(CARD_ON_BOARD)
    for card in cards1:
        add_a_card_to_board(board1, card)
    for card in cards2:
        add_a_card_to_board(board2, card)
    return score_game([board1, board2])


# c1 = [4,0,1,6]
# c2 = [0,7,6,2]
# print(manualscore(c1, c2))
rungame()
