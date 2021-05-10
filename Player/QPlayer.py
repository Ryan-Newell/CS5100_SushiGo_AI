from utils import *
from Player import BasePlayer


class QPlayer(BasePlayer):

    def __init__(self, name, learning_rate, discount_factor):
        super().__init__(name)
        self.decay_gamma = discount_factor
        self.lr = learning_rate
        self.hits = 0
        self.querys = 0

        self.model_dict = {}

        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        max_value = -float('inf')
        for possible_next_card in set(self.hand):
            board = copy.copy(self.board)
            add_a_card_to_board(board, possible_next_card)
            self.querys += 1
            if str(board) in self.model_dict:
                self.hits += 1
            value = self.model_dict.get(str(board), 0) + random.random() / 1e6

            if value > max_value:
                max_value = value
                action = possible_next_card
        # Take a card based on action
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)

        # Add state to memory
        self.states_in_game.append(str(self.board))

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        list_of_states = self.states_in_game
        for i in range(len(list_of_states) - 1):
            round_reward = 0
            if list_of_states[i] not in self.model_dict:
                self.model_dict[list_of_states[i]] = 0
            if i == len(list_of_states) - 2:
                round_reward = reward * 10
            self.model_dict[list_of_states[i]] = (1 - self.lr) * self.model_dict[list_of_states[i]] + \
                                                self.lr * (round_reward + self.decay_gamma * self.model_dict.get(
                str(list_of_states[i + 1]), 0))

    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.states_in_game.append(str(self.board))
