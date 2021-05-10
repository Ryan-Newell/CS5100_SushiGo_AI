from utils import *
from Player import BasePlayer
import numpy as np

class ApproxQPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.learning_rate = 0.01
        self.discount = 0.65
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
            value = self.get_q_value(self.weights, possible_future_board) + random.random() / 1e6
            if value > max_q_value:
                max_q_value = value
                action = possible_next_card
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)
        # Add state to memory
        self.states_in_game.append(str(self.board))

    def get_q_value(self, weights, features):
        q_value = 0
        for i in range(len(features)):
            q_value += weights[i] * features[i]

        return q_value

    def get_max_value(self, board):
        max_value = -float('inf')
        for i in range(11):  # length of player hand - 1(chopsticks)
            possible_next_board = copy.copy(board)
            possible_next_board = eval(possible_next_board)   #converting to array
            add_a_card_to_board(possible_next_board, i)
            value = self.get_q_value(self.weights, possible_next_board)
            if value > max_value:
                max_value = value

        return max_value

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        list_of_states = self.states_in_game

        for i in range(len(list_of_states) - 1):
            round_reward = 0
            if list_of_states[i] not in self.values:
                self.values[list_of_states[i]] = 0
            if i == len(list_of_states) - 2:
                round_reward = reward
            difference = (round_reward + self.discount * self.get_max_value(list_of_states[i + 1])) - self.get_q_value(self.weights, eval(list_of_states[i]))

            for j in range(len(eval(list_of_states[i]))):
                features = eval(list_of_states[i])
                self.weights[j] += self.learning_rate * difference * features[j]


    def prepare_for_next_round(self):
        super().prepare_for_next_round()
        self.states_in_game = []
        self.states_in_game.append(str(self.board))
