class EvaluationFunction:

    def __init__(self):
        pass

    def get_card_score_estimate(self, card_number, cards_in_game, cards_with_player):
        score = 0
        if card_number == 0:  # sashimi
            sashimi_with_player = cards_with_player[0]
            sashimi_in_game = cards_in_game[0]
            if sashimi_with_player + sashimi_in_game > 4:
                possible_future_deck = cards_with_player.copy()
                possible_future_deck[0] += 1
                return self.get_actual_card_score(card_number, possible_future_deck)
            else:
                return 0
        if card_number == 1:  # egg nigiri
            pass
        if card_number == 4:  # wasabi
            nigiri_in_game = cards_in_game[1] + cards_in_game[2] + cards_in_game[3]
            wasabi_with_player = cards_with_player[4]
            return nigiri_in_game - wasabi_with_player
        if card_number == 5:  # tempura
            tempura_with_player = cards_with_player[5]
            tempura_in_game = cards_in_game[5]
            if tempura_with_player + tempura_in_game > 2:
                possible_future_deck = cards_with_player.copy()
                possible_future_deck[5] += 1
                return self.get_actual_card_score(card_number,
                                                  possible_future_deck)  # might have to use cards + 1 (because we're adding a card)
            else:
                return 0
        if card_number == 6:  # dumplings
            dumplings_with_player = cards_with_player[6]
            dumplings_in_game = cards_in_game[6]
            if dumplings_in_game > 0:
                future_deck = cards_with_player.copy()
                future_deck[6] += 1
                return self.get_actual_card_score(card_number, future_deck) - \
                       self.get_actual_card_score(card_number,
                                                  cards_with_player)  # we just want to add the resultant increase in score
            else:
                return 0
        if card_number == 7:  # 1 maki
            return self.get_actual_card_score(card_number, cards_with_player)
        if card_number == 8:  # 2 maki
            return self.get_actual_card_score(card_number, cards_with_player)
        if card_number == 9:  # 3 maki
            return self.get_actual_card_score(card_number, cards_with_player)

    def get_actual_card_score(self, card_number, cards_with_player):
        if card_number == 0:  # sashimi
            return (cards_with_player[0] % 3) * 10
        if card_number == 1:  # egg nigiri
            if cards_with_player[4] > 0:  # wasabi card
                return min(cards_with_player[1],
                           cards_with_player[4]) * 3  # 2 nigiri, 3 wasabi make two pairs, so 2*3 = 6
            else:
                return cards_with_player[1]
        if card_number == 2:  # salmon nigiri
            if cards_with_player[4] > 0:  # wasabi card
                return min(cards_with_player[2],
                           cards_with_player[4]) * 6  # 2 nigiri, 3 wasabi make two pairs, so 2*6 = 12
            else:
                return cards_with_player[2] * 2
        # Need to figure out how to split wasabi between the nigiri cards
        if card_number == 3:  # Squid Nigiri
            if cards_with_player[4] > 0:  # wasabi card
                return min(cards_with_player[3],
                           cards_with_player[4]) * 9  # 2 nigiri, 3 wasabi make two pairs, so 2*9 = 18
            else:
                return cards_with_player[3] * 3
        if card_number == 4:  # wasabi
            return 0
        if card_number == 5:  # tempura
            return (cards_with_player[5] % 2) * 5
        if card_number == 6:  # dumplings

            def dumpling_score(number_of_dumplings):
                if number_of_dumplings == 0:
                    return 0
                else:
                    return number_of_dumplings + dumpling_score(number_of_dumplings - 1)

            return dumpling_score(cards_with_player[6])
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

    def get_state_score(self):
        pass


