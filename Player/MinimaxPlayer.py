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
        if len(self.hand) == 10:

            for card in self.priority:  # Choose based on priority
                if card in self.hand:
                    self.hand.remove(card)
                    # print(self.hand)
                    self.opponentHand = self.hand.copy()
                    add_a_card_to_board(self.board, card)
                    return
        else:
            print(all_player_boards)
            # print(self.opponentHand)
            # print(self.hand)
            # print(self.board)
            player_board = self.board.copy()
            opponent_board = all_player_boards[0][1].copy()
            print(self.state_finder(self.hand, self.opponentHand, self.board, opponent_board))
            action = None
            while True:
                action = int(input("Please choose a card"))
                if action in self.hand:
                    break
                else:
                    print("Invalid choice!")
            self.hand.remove(action)
            add_a_card_to_board(self.board, action)

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return

    def state_finder(self, player_hand, opponent_hand, player_board, opponent_board):
        if len(player_hand) == 0:
            print("endstate")
            print(player_board)
            print(get_score(player_board))
            print(opponent_board)
            print(get_score(opponent_board))
            return get_score(player_board) - get_score(opponent_board)
        unique_player_hand = list(set(player_hand))
        unique_opponent_hand = list(set(opponent_hand))
        for player_card in unique_player_hand:
            player_hand.remove(player_card)
            add_a_card_to_board(player_board, player_card)
            for opponent_card in unique_opponent_hand:
                opponent_hand.remove(opponent_card)
                add_a_card_to_board(opponent_board, opponent_card)
                # print(player_card)
                # print(player_board)
                # print(opponent_card)
                # print(opponent_board)
                return self.state_finder(opponent_hand, player_hand, player_board, opponent_board)
        #return

    @staticmethod
    def win_check(player_board, opponent_board):
        if get_score(player_board) > get_score(opponent_board):
            return True
        else:
            return False