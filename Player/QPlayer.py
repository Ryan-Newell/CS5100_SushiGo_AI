from utils import *
from Player import BasePlayer


class QPlayer(BasePlayer):

    def __init__(self, name, learning_rate, discount_factor):
        super().__init__(name)
        self.decay_gamma = discount_factor
        self.lr = learning_rate
        self.exp_rate = 0.3
        self.hits = 0
        self.querys = 0

        self.model_dict = {}

        self.prepare_for_next_round()

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        max_value = -float('inf')
        # print('player hand', self.hand)
        # print('pick a card called', self.get_score())
        for possible_next_card in set(self.hand):
            board = copy.copy(self.board)
            # print('board', board)
            add_a_card_to_board(board, possible_next_card)
            # print('board after adding card', board)
            self.querys += 1
            if str(board) in self.model_dict:
                self.hits += 1
            # print('actual value', self.model_dict.get(str(board), 0))
            value = self.model_dict.get(str(board), 0) + random.random() / 1e6

            # print(value, get_score(board))

            if value > max_value:
                max_value = value
                action = possible_next_card
        # print('max_value', max_value)
        # Take a card based on action
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)

        # Add state to memory
        self.states_in_game.append(str(self.board))

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        # print('original', self.states_in_game)
        # print('used', self.states_in_game[::-1])
        # for state in self.states_in_game[::-1]:
        #     if state not in self.model_dict:
        #         self.model_dict[state] = 0
        #
        #     self.model_dict[state] += (reward - self.model_dict[state]) * self.lr
        #     print('reward updating', reward)
        #     reward *= self.decay_gamma
        # reversed_list = self.states_in_game[::-1]
        reversed_list = self.states_in_game
        for i in range(len(reversed_list) - 1):
            round_reward = 0
            if reversed_list[i] not in self.model_dict:
                self.model_dict[reversed_list[i]] = 0
            if i == len(reversed_list) - 2:
                round_reward = reward * 10
            self.model_dict[reversed_list[i]] = (1 - self.lr) * self.model_dict[reversed_list[i]] + \
                                                self.lr * (round_reward + self.decay_gamma * self.model_dict.get(
                str(reversed_list[i + 1]), 0))
        # print(self.model_dict)

    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.states_in_game.append(str(self.board))
