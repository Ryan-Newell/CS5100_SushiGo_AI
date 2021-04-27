from collections import defaultdict
import math
from datetime import *
from utils import *
import random
from operator import attrgetter
from Player import BasePlayer


class MCTSPlayer(BasePlayer):

    def __init__(self, name, num_simulations, exploration_weight=1.0):
        super().__init__(name)
        self.nodes = []
        self.num_simulations = num_simulations
        self.exploration_weight = exploration_weight
        self.prepare_for_next_round()

    def pick_a_card(self, all_player_boards):
        action = None # represents the best next move
        index = 0
        # Loop through all the players and for each, run mcts
        for player, board in all_player_boards:

            nextPlayerInfo = None
            if index < len(all_player_boards) - 1:
                nextPlayerInfo = all_player_boards[index + 1]

            # Run MCTS
            node = self.run_mcts(player, board, nextPlayerInfo, self.num_simulations)

            if player == self:
                action = max(node.children, key=attrgetter('incoming_move'))

            index += 1
        self.hand.remove(action.incoming_move)
        add_a_card_to_board(self.board, action.incoming_move)

    def run_mcts(self, player, board, nextPlayerInfo, num_simulations):

        root_node = Node(player)

        # Loop through all the moves of the current player

        for player_move in set(player.hand):

            node = self.select_promising_node(root_node)
            
            self.expand_node(node, nextPlayerInfo, player_move)
            
            node_to_explore = node

            if(len(node.children) > 0):
                node_to_explore = node.find_random_child()

            playout_result = self.simulate(node_to_explore, num_simulations)

            self.back_propogate(node_to_explore, playout_result)

        return root_node
    

    def select_promising_node(self, node):
        if node.is_fully_expanded() :
            node = self.uct_select_best_child(node);
        return node

    def expand_node(self, node, nextPlayerInfo, player_move):
        if not node.is_fully_expanded():
            if nextPlayerInfo != None:
                for action in node.player.hand:
                    child = Node(nextPlayerInfo[0], incoming_move=player_move, parent=node)
                    node.children.append(child)

    def simulate(self, node, num_simulations=3):
        for x in range(num_simulations + 1):
            if node.is_terminal():
                return node.reward
            node = node.find_random_child()

    def back_propogate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent

    def uct_select_best_child(self, node):
        if not node.is_fully_expanded():
            raise ValueError("Can only select fom fully expanded node")

        log_N_parent = math.log(node.visits)

        def uct(n):
            "Upper confidence bound for trees"
            return n.reward / n.visits + self.exploration_weight * math.sqrt(log_N_parent / n.visits)

        return max(node.children, key=uct)


class Node:
    def __init__(self, player, incoming_move=None, parent=None):

        self.visits=1
        self.reward = 0.0
        self.parent = parent
        self.children = []
        self.player = player
        self.incoming_move = incoming_move


    def update(self,reward):
        self.reward += reward
        self.visits += 1

    def is_terminal(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def find_random_child(self):
        return random.choice(self.children)

    def is_fully_expanded(self):
        if len(self.children) == len(self.player.hand):
            return True
        return False

    def get_child_with_max_score(self):
        return max(node.reward for node in self.children)

    def __repr__(self):

        s="Node; children: %d; visits: %d; reward: %f"%(len(self.children),self.visits,self.reward)

        return s
