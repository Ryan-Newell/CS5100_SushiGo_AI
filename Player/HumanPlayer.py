from utils import *
from Player.BasePlayer import BasePlayer


class HumanPlayer(BasePlayer):

    def __init__(self, name):
        super().__init__(name)
        self.prepare_for_next_round()
        self.prevBoard = [0] * len(CARD_ON_BOARD)

    def draw(self, card):
        self.hand.append(card)
        self.prevBoard = [0] * len(CARD_ON_BOARD)

    def pick_a_card(self, all_player_boards):
        action = None
        print("Opponent's Board")
        # print(all_player_boards)
        # print(CARD_ON_BOARD)
        for i in range(len(self.prevBoard)):
            print(f"{CARD_ON_BOARD[i]} X {self.prevBoard[i]}")
        print('-' * 50)
        print("Board:")
        for i in range(len(self.board)):
            print(f"{CARD_ON_BOARD[i]} X {self.board[i]}")
        print('-' * 50)
        for card in self.hand:
            print(f"{card}, {CARDS[card]}")
        print('-' * 50)
        while True:
            action = int(input("Please choose a card"))
            if action in self.hand:
                break
            else:
                print("Invalid choice!")
        self.hand.remove(action)
        add_a_card_to_board(self.board, action)
        self.prevBoard = all_player_boards[0][1].copy()

    def get_score(self):
        return get_score(self.board)

    def feed_reward(self, reward):
        return
