# %load_ext autoreload
import pandas as pd
from State import *
from Player import *
import plotly.express as px
from tqdm import tqdm
import json

#%%

state = State(get_actual_card_pool())
p1 = RulePlayer('Player 1')
# p1.model_dict = json.loads(open('./models/model1.json').read())
p2 = HumanPlayer('Player 2')
state.add_player(p1)
state.add_player(p2)

df = pd.DataFrame()
all_results = []
hit_rates = []

state.play_games(1, output_result=True)