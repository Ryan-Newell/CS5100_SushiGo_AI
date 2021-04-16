from utils import *
from Player.BasePlayer import BasePlayer


class MinimaxPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.prepare_for_next_round()

        self.priority = [4, 3, 2, 0, 10, 5, 9, 8, 7, 6, 1]
        self.opponentHand = []

    def draw(self, card):
        self.hand.append(card)

    def pick_a_card(self, all_player_boards):
        if len(self.hand) > 3:
            for card in self.priority:  # Choose based on priority
                if card in self.hand:
                    self.hand.remove(card)
                    # print(self.hand)
                    self.opponentHand = self.hand.copy()
                    add_a_card_to_board(self.board, card)
                    return
        else:
            # print(all_player_boards)
            # print(self.opponentHand)
            # print(self.hand)
            # print(self.board)
            print(len(self.hand))
            player_board = self.board.copy()
            opponent_board = all_player_boards[0][1].copy()
            action, reward = self.state_finder(self.hand.copy(), self.opponentHand.copy(),
                                    self.board.copy(), opponent_board.copy())

            # print(self.hand)
            # print(self.board)
            # print(action)
            # action = None
            # while True:
            #     action = int(input("Please choose a card"))
            #     if action in self.hand:
            #         break
            #     else:
            #         print("Invalid choice!")
            self.hand.remove(action)
            add_a_card_to_board(self.board, action)

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return

    def state_finder(self, player_hand, opponent_hand, player_board, opponent_board):
        # print(player_hand)
        if len(player_hand) <= 1:
            action = None
            if len(player_hand) == 1:
                action = player_hand[0]
                add_a_card_to_board(player_board, player_hand[0])
            if len(opponent_hand) == 1:
                add_a_card_to_board(opponent_board, opponent_hand[0])
            # print(get_score(player_board) - get_score(opponent_board))
            print(opponent_board)
            print(player_board)
            scores = score_game([opponent_board, player_board])
            print(scores[0])
            print(scores[1])
            return action, scores[1]-scores[0]
            # -1/+1 attempt
            # print("leaf")
            # print("[" + str(get_score(opponent_board)) + ", " + str(get_score(player_board)) + "]")

            # if get_score(player_board) > get_score(opponent_board):
            #     print("win!")
            #     print(player_board)
            #     print(opponent_board)
            #     print("[" + str(get_score(opponent_board)) + ", " + str(get_score(player_board)) + "]")
            #     return action, 1
            # elif get_score(player_board) == get_score(opponent_board):
            #     return action, 0
            # else:
            #     return action, -1
        unique_player_hand = list(set(player_hand))
        unique_opponent_hand = list(set(opponent_hand))
        actions = []
        rewards = []

        for player_card in unique_player_hand:
            add_a_card_to_board(player_board, player_card)
            actions.append(player_card)
            minimizer = []
            # minimizer = 0
            iter_player_hand = player_hand.copy()
            iter_player_hand.remove(player_card)
            for opponent_card in unique_opponent_hand:
                add_a_card_to_board(opponent_board, opponent_card)
                # actions.append(player_card)

                iter_opponent_hand = opponent_hand.copy()

                iter_opponent_hand.remove(opponent_card)
                action, reward = self.state_finder(iter_opponent_hand.copy(), iter_player_hand.copy(), player_board.copy(), opponent_board.copy())
                minimizer.append(reward)
                # minimizer += reward
            # print("minimizing: " + str(minimizer))
            rewards.append(minimizer)
        # print("hands")
        # print(player_hand)
        # print(opponent_hand)
        # print("result")
        # print(actions)
        # print(rewards)
        max_index = rewards.index(max(rewards))
        return actions[max_index], rewards[max_index]

    def minimax_recursor(self, ):
        pass

    @staticmethod
    def win_check(player_board, opponent_board):
        if get_score(player_board) > get_score(opponent_board):
            return True
        else:
            return False