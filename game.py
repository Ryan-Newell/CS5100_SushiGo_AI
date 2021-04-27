# %load_ext autoreload
import pandas as pd

from Player.MinimaxPlayer import MinimaxPlayer
from State import *
from Player import *
from Player import ApproxQPlayer
from Player import MCTSPlayer
from Player import MinimaxPlayer
import plotly.express as px
from tqdm import tqdm
import json

#%%

state = State(get_actual_card_pool())

p1 = RandomPlayer('Player 1')
# p1.model_dict = json.loads(open('./models/model1.json').read())
# p2 = RandomPlayer('Player 2')
# p1 = MinimaxPlayer.MinimaxPlayer('Player 2')
# p2 = ApproxQPlayer.ApproxQPlayer('Player 2')
# p2 = QPlayer('Player 2')
# p3 = MCTSPlayer.MCTSPlayer('MCTS', num_simulations=3)



state.add_player(p1)
# state.add_player(p2)
# state.add_player(p3)
# state.add_player(p4)

# df = pd.DataFrame()
# all_results = []
# hit_rates = []


# state.play_games(num_of_games=10000, round_per_game=1, output_result=False)
# all_results.append(state.stats)
# print(all_results)


x = [0, 0, 0, 0, 0]
y = [0, 0, 0, 0, 0]
for i in range(5):
    state = State(get_actual_card_pool())
    p1 = RulePlayer('Player 1')
    p2 = QPlayer('Player 2', learning_rate=0.9, discount_factor=0.9)
    state.add_player(p1)
    state.add_player(p2)
    df = pd.DataFrame()
    all_results = []

    state.play_games(num_of_games=50000, round_per_game=1, output_result=False)
    all_results.append(state.stats)
    [[x[i], y[i]]] = all_results

print(x, y)
print(sum(x)/len(x), sum(y)/len(y))