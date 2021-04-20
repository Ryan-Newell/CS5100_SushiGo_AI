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
p1 = RulePlayer('Player 1')
# p1.model_dict = json.loads(open('./models/model1.json').read())
p2 = QPlayer('Player 2')
# p2 = RulePlayer('Player 2')
state.add_player(p1)
state.add_player(p2)

df = pd.DataFrame()
all_results = []
hit_rates = []

state.play_games(num_of_games=1000000, round_per_game=3, output_result=True)
all_results.append(state.stats)
print(all_results)