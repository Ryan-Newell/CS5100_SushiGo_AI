from utils import *
from Player.BasePlayer import BasePlayer
from EvaluationFunction import EvaluationFunction


class MinimaxPlayer(BasePlayer):
    """
    """
    def __init__(self, name, evaluate=True, roundstart='plus'):
        super().__init__(name)
        self.prepare_for_next_round()
        self.evaluate = EvaluationFunction()

        if roundstart == 'plus':
            # Greedy+
            self.priority = [10, 4, 3, 2, 5, 9, 8, 6, 0, 7, 1]
        else:
            # Greedy
            self.priority = [4, 3, 2, 0, 10, 5, 9, 8, 7, 6, 1]
        self.opponentHand = []
        self.rewards = []
        self.max_depth = 3
        self.eval = evaluate
        self.solve_tree = 0
        if evaluate:
            self.greedy_num = 9
            self.solve_tree = 6
        else:
            self.greedy_num = 9

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        # First Play, and more if not using evaluation function
        unique_hand = list(set(self.hand))
        if len(self.hand) > self.greedy_num:
            self.rewards = []
            for card in self.priority:  # Choose based on priority
                if card in unique_hand:
                    self.hand.remove(card)
                    self.opponentHand = self.hand.copy()
                    add_a_card_to_board(self.board, card)
                    return
        else:
            player_board = self.board.copy()
            opponent_board = all_player_boards[1][1].copy()
            if self.eval:
                if len(self.hand) > self.solve_tree:
                    action, reward, choices = self.state_finder(self.hand.copy(), self.opponentHand.copy(),
                                        self.board.copy(), opponent_board.copy(), -1000, 1000, 0)
                else:
                    action, reward, choices = self.state_finder(self.hand.copy(), self.opponentHand.copy(),
                                        self.board.copy(), opponent_board.copy(), -1000, 1000, -50)
            else:
                action, reward, choices = self.state_finder(self.hand.copy(), self.opponentHand.copy(),
                                                            player_board.copy(), opponent_board.copy(), -1000, 1000, -50)

            self.rewards.append(reward)
            self.hand.remove(action)
            self.opponentHand = self.hand.copy()
            add_a_card_to_board(self.board, action)

        # Diagnostics to test how minimax is working. Prints the expected values, and prints a notice if it performs
        # worse than expected.

        # if len(self.hand) == 0:
        #     print(self.rewards)
        #     autowin = False
        #     if self.rewards[0] > 0:
        #         autowin = True
        #     winnable = False
        #     prev = -1000
        #     for reward in self.rewards:
        #         if reward > 0:
        #             winnable = True
        #
        #         if reward < prev:
        #             print("miss estimate")
        #         prev = reward
        #     if winnable and self.rewards[-1] <= 0:
        #         print("ALERT")
        #     if not autowin:
        #         # print("badstart")
        #         if self.rewards[-1] > 0:
        #             pass

        return

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return

    def state_finder(self, player_hand, opponent_hand, player_board, opponent_board, alpha, beta, depth):
        unique_player_hand = list(set(player_hand))
        unique_opponent_hand = list(set(opponent_hand))

        # Base case. If there is 1 card in hand, the game can be scored.
        if len(player_hand) == 1 and len(opponent_hand) == 1:
            temp_player_board = player_board.copy()
            temp_opponent_board = opponent_board.copy()
            action = None
            if len(player_hand) == 1:
                action = player_hand[0]
                add_a_card_to_board(temp_player_board, player_hand[0])
            if len(opponent_hand) == 1:
                add_a_card_to_board(temp_opponent_board, opponent_hand[0])
            scores = score_game([temp_player_board, temp_opponent_board])
            return action, scores[0]-scores[1], (player_board, opponent_board, opponent_hand)

        # Evaluation case. If it has reached the maximum depth, the game can be evaluated
        if depth == self.max_depth:
            scores = []
            card_list = []
            for player_card in unique_player_hand:
                scores.append(
                    self.evaluate.get_card_score_estimate(player_card, player_hand, opponent_hand,
                                                          player_board, opponent_board))
                card_list.append(player_card)
            minimax_card = card_list[scores.index(max(scores))]
            minimax_score = max(scores)
            return minimax_card, minimax_score, (0, 0)

        actions = []
        rewards = []
        reward_ends = []
        opp_accs = []

        # Recursion case. Picks a combination of player and opponent actions, then runs that through state_finder
        for player_card in unique_player_hand:
            temp_player_board = player_board.copy()
            iter_player_hand = player_hand.copy()

            add_a_card_to_board(temp_player_board, player_card)
            iter_player_hand.remove(player_card)
            actions.append(player_card)

            minacs = []
            minimizer = []
            endstates = []

            for opponent_card in unique_opponent_hand:
                temp_opponent_board = opponent_board.copy()
                add_a_card_to_board(temp_opponent_board, opponent_card)

                iter_opponent_hand = opponent_hand.copy()
                iter_opponent_hand.remove(opponent_card)

                action, reward, endstate = self.state_finder(iter_opponent_hand.copy(), iter_player_hand.copy(),
                                                            temp_player_board, temp_opponent_board,
                                                            alpha, beta, depth+1)

                minacs.append(opponent_card)
                minimizer.append(reward)
                endstates.append(endstate)

                # alpha pruning
                beta = min(min(minimizer), beta)
                if reward < alpha:
                    beta = reward
                    break
                # minimizer += reward
            rewards.append(min(minimizer))
            reward_ends.append(endstates[minimizer.index(min(minimizer))])
            opp_accs.append((minacs, minimizer))
            # beta pruning
            alpha = max(max(rewards), alpha)
            if max(rewards) > beta:
                alpha = max(rewards)
                break

        max_index = rewards.index(max(rewards))
        return actions[max_index], rewards[max_index], (actions, rewards, opp_accs)
