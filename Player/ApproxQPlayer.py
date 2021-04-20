from utils import *
from Player import BasePlayer


class ApproxQPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        pass

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        pass

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        pass

    def prepare_for_next_round(self):
        pass