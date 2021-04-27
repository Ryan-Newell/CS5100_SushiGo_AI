import numpy as np


class EvaluationFunction:

    def __init__(self):
        pass

    def get_card_score_estimate(self, card_number, player_hand, opponent_hand, player_board, opponent_board):
        """
                player_hand : Cards currently in players hand
                opponent_hand : Cards currently in opponents hand
                cards_in_game: Total cards currently in the game (Combination of both player and opponent's hands)
                player_board: Cards played by our player

        """

        score = 0

        # cards_in_game = np.add(np.array(player_hand), np.array(opponent_hand))
        cards_in_game = player_hand + opponent_hand

        if card_number == 0:  # sashimi
            sashimi_with_player = player_board[0]
            sashimi_in_game = cards_in_game.count(0)
            if sashimi_with_player + sashimi_in_game > 4:
                possible_future_deck = player_board.copy()
                possible_future_deck[0] += 1
                return self.get_actual_card_score(card_number, possible_future_deck)
            else:
                return 0

        if card_number == 1:  # egg nigiri
            if player_board[7] > 0:
                return 3
            else:
                return 1
        if card_number == 2: # salmon nigiri
            if player_board[7] > 0:
                return 6
            else:
                return 2
        if card_number == 3:   # squid nigiri
            if player_board[7] > 0:
                return 9
            else:
                return 3

        if card_number == 4:  # wasabi
            nigiri_in_game = cards_in_game.count(1) + cards_in_game.count(2) + cards_in_game.count(3)
            if nigiri_in_game == 0:
                return 0
            if 3 in opponent_hand:
                return 4.5
            elif player_hand.count(3) > 1:
                return 4.5
            elif 2 in opponent_hand:
                return 3
            elif player_hand.count(2) > 1:
                return 3
            elif 1 in opponent_hand:
                return 1.5
            elif player_hand.count(1) > 1:
                return 1.5
            else:
                return 0
            # wasabi_with_player = player_board[7]
            # return nigiri_in_game - wasabi_with_player  # wasabi is scored only if there are nigiri cards in the game

        if card_number == 5:  # tempura
            tempura_with_player = player_board[8]
            tempura_with_opponent = opponent_board[8]
            tempura_in_game = cards_in_game.count(5)
            if tempura_with_player == 1:
                return 2.5
            if tempura_with_player % 2 == 0 and tempura_with_opponent % 2 == 0:
                if tempura_in_game < 2:
                    return 0
                if player_hand.count(5) == 1 and opponent_hand.count(5) == 1:
                    return 2.5

            # if player_hand.count(5

            if tempura_with_player + tempura_in_game > 2:
                possible_future_deck = player_board.copy()
                possible_future_deck[8] += 1
                return self.get_actual_card_score(card_number,
                                                  possible_future_deck)  # might have to use cards + 1 (because we're adding a card)
            else:
                return 0
        if card_number == 6:  # dumplings
            dumplings_with_player = player_board[9]
            dumplings_in_game = cards_in_game.count(6)
            if dumplings_in_game > 0:
                future_deck = player_board.copy()
                future_deck[9] += 1
                return self.get_actual_card_score(card_number, future_deck) - \
                       self.get_actual_card_score(card_number,
                                                  player_board)  # we just want to add the resultant increase in score
            else:
                return 0
        # if card_number == 7:  # 1 maki
        #     return self.get_actual_card_score(card_number, player_board)
        # if card_number == 8:  # 2 maki
        #     return self.get_actual_card_score(card_number, player_board)
        # if card_number == 9:  # 3 maki
        #     return self.get_actual_card_score(card_number, player_board)

        # Maki
        if card_number in [7, 8, 9]:
            maki_rolls = card_number - 6
            rolls_in_game = cards_in_game.count(7) + 2 * cards_in_game.count(8) + 3 * cards_in_game.count(9)
            # maki is not useful if one player is guaranteed to have the most
            if opponent_board[10] > player_board[10] + rolls_in_game \
                    or player_board[10] > opponent_board[10] + rolls_in_game:
                return 0
            # prioritize if current maki guarantees a win
            if player_board[10] + maki_rolls > opponent_board[10] + rolls_in_game - maki_rolls:
                # print("decider")
                return 3
            else:
                return 1

        if card_number == 0: # pudding
            # pudding is not useful if one player is guaranteed to have the most
            if opponent_board[11] > player_board[11] + cards_in_game.count[10] \
                    or player_board[11] > opponent_board[11] + cards_in_game.count[10]:
                return 0
            # 12 is the point swing for winning puddings
            return 12
        return 0

    def get_actual_card_score(self, card_number, player_board):
        if card_number == 0:  # sashimi
            return (player_board[0] % 3) * 10
        """
            Actual score is not necessary for nigiri and wasabi nigiris as it is already implemented on the board
        """
        # if card_number == 1:  # egg nigiri
        #     if cards_with_player[4] > 0:  # wasabi card
        #         return min(cards_with_player[1],
        #                    cards_with_player[4]) * 3  # 2 nigiri, 3 wasabi make two pairs, so 2*3 = 6
        #     else:
        #         return cards_with_player[1]
        # if card_number == 2:  # salmon nigiri
        #     if cards_with_player[4] > 0:  # wasabi card
        #         return min(cards_with_player[2],
        #                    cards_with_player[4]) * 6  # 2 nigiri, 3 wasabi make two pairs, so 2*6 = 12
        #     else:
        #         return cards_with_player[2] * 2
        # # Need to figure out how to split wasabi between the nigiri cards
        # if card_number == 3:  # Squid Nigiri
        #     if cards_with_player[4] > 0:  # wasabi card
        #         return min(cards_with_player[3],
        #                    cards_with_player[4]) * 9  # 2 nigiri, 3 wasabi make two pairs, so 2*9 = 18
        #     else:
        #         return cards_with_player[3] * 3

        if card_number == 4:  # wasabi
            return 0
        if card_number == 5:  # tempura
            return (player_board[8] % 2) * 5
        if card_number == 6:  # dumplings

            def dumpling_score(number_of_dumplings):
                if number_of_dumplings == 0:
                    return 0
                else:
                    return number_of_dumplings + dumpling_score(number_of_dumplings - 1)

            return dumpling_score(player_board[9])
        if card_number == 7:  # 1 maki
            return 1
        if card_number == 8:  # 2 maki
            return 2
        if card_number == 9:  # 3 maki
            return 3
        if card_number == 10:  # pudding
            return 0
        if card_number == 11:  # chopsticks
            return 0
        return 0

    def get_state_score(self):
        pass



