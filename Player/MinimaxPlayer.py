from utils import *
from Player.BasePlayer import BasePlayer
from EvaluationFunction import EvaluationFunction


class MinimaxPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.prepare_for_next_round()
        self.evaluate = EvaluationFunction()
        self.priority = [4, 3, 2, 0, 10, 5, 9, 8, 7, 6, 1]
        self.opponentHand = []
        self.rewards = []

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        # print(all_player_boards)
        # print(self.hand)
        # print(self.opponentHand)

        if len(self.hand) > 9:
            self.rewards = []
            for card in self.priority:  # Choose based on priority
                if card in self.hand:
                    self.hand.remove(card)
                    # print(self.hand)
                    self.opponentHand = self.hand.copy()
                    add_a_card_to_board(self.board, card)
                    return
            # self.opponentHand = self.hand.copy()
            # action = self.hand.pop()
            # add_a_card_to_board(self.board, action)
            # random.shuffle(self.hand)
            # action = self.hand.pop()
            # add_a_card_to_board(self.board, action)
            return
        else:
            # print(all_player_boards)
            # print(self.opponentHand)
            # print(self.hand)
            # print(self.board)
            # print("SET")

            player_board = self.board.copy()
            opponent_board = all_player_boards[1][1].copy()
            action, reward, choices = self.state_finder(self.hand.copy(), self.opponentHand.copy(),
                                    self.board.copy(), opponent_board.copy(), -1000, 1000)
            # print("handsize: " + str(len(self.hand)))

            # print(self.board)
            # print(choices[0])
            # print(choices[1])
            # print(action)
            # print(reward)
            self.rewards.append(reward)
            # print(reward)
            # action = None
            # while True:
            #     action = int(input("Please choose a card"))
            #     if action in self.hand:
            #         break
            #     else:
            #         print("Invalid choice!")
            self.hand.remove(action)
            self.opponentHand = self.hand.copy()
            add_a_card_to_board(self.board, action)
        if len(self.hand) == 0:
            print(self.rewards)
            winnable = False
            for reward in self.rewards:
                if reward > 0:
                    winnable = True
            if winnable and self.rewards[-1] <= 0:
                print("ALERT")
            #     prev = reward
        return

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return

    def state_finder(self, player_hand, opponent_hand, player_board, opponent_board, alpha, beta):
        # print(player_hand)
        depth = 0
        limit = 0
        unique_player_hand = list(set(player_hand))
        unique_opponent_hand = list(set(opponent_hand))
        if depth == limit:
            scores = []
            card_list = []
            opponent_scores = []
            for player_card in unique_player_hand:
                print(player_hand)
                print(player_card)
                print(player_board)
                scores.append(
                    self.evaluate.get_card_score_estimate(player_card, player_hand, opponent_hand, player_board))
                card_list.append(player_card)
            # for opponent_card in unique_opponent_hand:
            #     opponent_scores.append(
            #         self.evaluate.get_card_score_estimate(opponent_card, opponent_hand, player_hand, player_board))
            print("Score")
            print(scores)
            minimax_card = card_list[scores.index(max(scores))]
            minimax_score = max(scores) #  - min(opponent_scores)
            return minimax_card, minimax_score, (0, 0)
        if len(player_hand) <= 1:
            action = None
            if len(player_hand) == 1:
                action = player_hand[0]
                add_a_card_to_board(player_board, player_hand[0])
            if len(opponent_hand) == 1:
                add_a_card_to_board(opponent_board, opponent_hand[0])
            # print(get_score(player_board) - get_score(opponent_board))
            # print(opponent_board)
            # print(player_board)
            scores = score_game([opponent_board, player_board])
            # print(scores)
            # print(scores[1])
            return action, scores[1]-scores[0], (action, scores[1]-scores[0])
            # -1/+1 attempt
            # print("leaf")
            # print("[" + str(get_score(opponent_board)) + ", " + str(get_score(player_board)) + "]")

            # if scores[1] > scores[0]:
            #     # print("win!")
            #     # print(player_board)
            #     # print(opponent_board)
            #     # print("[" + str(get_score(opponent_board)) + ", " + str(get_score(player_board)) + "]")
            #     return action, 1
            # elif scores[1] == scores[0]:
            #     return action, 0
            # else:
            #     return action, -1

        actions = []
        rewards = []

        for player_card in unique_player_hand:
            add_a_card_to_board(player_board, player_card)
            actions.append(player_card)
            minacs = []
            minimizer = []
            # minimizer = 0
            iter_player_hand = player_hand.copy()
            iter_player_hand.remove(player_card)
            for opponent_card in unique_opponent_hand:
                add_a_card_to_board(opponent_board, opponent_card)
                # actions.append(player_card)

                iter_opponent_hand = opponent_hand.copy()
                iter_opponent_hand.remove(opponent_card)

                action, reward, choices = self.state_finder(iter_opponent_hand.copy(), iter_player_hand.copy(),
                                                            player_board.copy(), opponent_board.copy(), alpha, beta)

                minacs.append(action)
                minimizer.append(reward)
                beta = min(min(minimizer), beta)
                # alpha =
                if reward < alpha:
                    beta = reward
                    break
                # minimizer += reward
            # print("minimizing: " + str(minimizer))
            # print("minacs: " + str(minacs))
            rewards.append(min(minimizer))
            alpha = max(max(rewards), alpha)
            if max(rewards) > beta:
                break
        # print("hands")
        # print(player_hand)
        # print(opponent_hand)
        # print("result")
        # print(actions)
        # print(rewards)
        max_index = rewards.index(max(rewards))
        # print(max_index)
        # print(rewards)
        # print(rewards[max_index])
        return actions[max_index], rewards[max_index], (actions, rewards)

    def minimax_recursor(self, ):
        pass

    @staticmethod
    def win_check(player_board, opponent_board):
        if get_score(player_board) > get_score(opponent_board):
            return True
        else:
            return False