from utils import *
from Player import BasePlayer
import numpy as np

class ApproxQPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.learning_rate = 0.01
        self.discount = 0.65
        self.exploration_rate = 0.3
        self.features = []
        self.weights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.values = {}

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        action = None
        max_q_value = -float('inf')
        current_hand = self.hand
        for possible_next_card in set(current_hand):
            possible_future_board = copy.copy(self.board)
            add_a_card_to_board(possible_future_board, possible_next_card)
            # value = self.values.get(str(possible_future_board), 0) + random.random() / 1e6
            value = self.get_q_value(self.weights, possible_future_board) + random.random() / 1e6
            if value > max_q_value:
                max_q_value = value
                action = possible_next_card
                # print(action)
        # print('->', self.hand, action)
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)
        # Add state to memory
        self.states_in_game.append(str(self.board))

    def get_q_value(self, weights, features):
        q_value = 0

        for i in range(len(features)):
            # print('types', type(weights), type(features))
            # print('->', type(weights), features)
            q_value += weights[i] * features[i]
            # print(weights[i], features[i])

        return q_value

    def get_max_value(self, board):
        max_value = -float('inf')
        for i in range(11):  # length of player hand - 1(chopsticks)
            possible_next_board = copy.copy(board)
            possible_next_board = eval(possible_next_board)   #converting to array
            # print('->', type(possible_next_board))
            add_a_card_to_board(possible_next_board, i)
            # print('->', possible_next_board)
            value = self.get_q_value(self.weights, possible_next_board)
            if value > max_value:
                max_value = value

        return max_value

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        # print('states', self.states_in_game)
        reversed_list = self.states_in_game

        for i in range(len(reversed_list) - 1):
            round_reward = 0
            if reversed_list[i] not in self.values:
                self.values[reversed_list[i]] = 0
            if i == len(reversed_list) - 2:
                round_reward = reward
            # print('culprit', round_reward, self.get_max_value(reversed_list[i + 1]), self.get_q_value(self.weights, eval(reversed_list[i])))
            difference = (round_reward + self.discount * self.get_max_value(reversed_list[i + 1])) - self.get_q_value(self.weights, eval(reversed_list[i]))

            for j in range(len(eval(reversed_list[i]))):
                features = eval(reversed_list[i])
                self.weights[j] += self.learning_rate * difference * features[j]

            # self.values[reversed_list[i]] = (1 - self.learning_rate) * self.values[reversed_list[i]] + \
            #                                 self.learning_rate * (round_reward + self.discount * self.values.get(
            #     str(reversed_list[i + 1]), 0))

    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.states_in_game.append(str(self.board))
