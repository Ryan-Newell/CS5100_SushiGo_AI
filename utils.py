import random
from collections import Counter
import numpy as np
import copy
import ast
from scipy.stats import rankdata


# Different in rules: Multiple Wasabi can act on a single sushi
# No tie breaker

"""
The values for the indices of a board object. A board is a size 12 array, with each index representing the number of
cards. Note that 10 represents the total maki roll count, so 1 maki and 3 maki would make board[9] = 4. Also, adding
a Nigiri to a wasabi board removes a wasabi at index 7 and adds one on 4, 5, 6.
EX: board = [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 4, 0, 0] means the board has: 1 sashimi, 1 wasabi salmon, 1 wasabi and
4 maki rolls
"""
CARD_ON_BOARD = {
    0: 'Sashimi',
    1: 'Egg Nigiri',
    2: 'Salmon Nigiri',
    3: 'Squid Nigiri',
    4: 'Wasabi Egg',
    5: 'Wasabi Salmon',
    6: 'Wasabi Squid',
    7: 'Wasabi',
    8: 'Tempura',
    9: 'Dumpling',
    10: 'Maki',
    11: 'Pudding',
    12: 'Chopsticks',
}

"""
The values of each card. a hand is a list of cards.
EX: hand = [7, 3, 3, 3] means [1 Maki, Squid Nigiri, Squid Nigiri, Squid Nigiri]
"""
CARDS = {
    0: 'Sashimi',
    1: 'Egg Nigiri',
    2: 'Salmon Nigiri',
    3: 'Squid Nigiri',
    4: 'Wasabi',
    5: 'Tempura',
    6: 'Dumpling',
    7: '1 Maki',
    8: '2 Maki',
    9: '3 Maki',
    10: 'Pudding',
    11: 'Chopsticks',  # Not implemented
}


def get_score(board):
    """
    Gets the score of a board. DOES NOT INCLUDE MAKI OR PUDDING.
    get_maki_score and get_pudding_score is needed for that
    :param board: the board to be scored (excludes maki, pudding)
    :return: the score of the board sans maki, pudding
    """
    score = 0
    score += board[0] // 3 * 10  # Salmon Nigiri
    score += board[1] * 1  # Sashimi
    score += board[2] * 2  # Squid Nigiri
    score += board[3] * 3  # Egg Nigiri
    score += board[4] * 3  # Wasabi Egg
    score += board[5] * 6  # Wasabi Salmon
    score += board[6] * 9  # Wasabi Squid
    score += board[8] // 2 * 5  # Tempura
    # Dumpling
    if board[9] == 1:
        score += 1
    if board[9] == 2:
        score += 3
    if board[9] == 3:
        score += 6
    if board[9] == 4:
        score += 10
    if board[9] > 4:
        score += ((board[9] - 4) * 5 + 10)
    return score


def add_a_card_to_board(board, card):
    """
    Adds the provided card to the board object
    :param board: a board object to be modified
    :param card: the card to be added to board
    :return: None. The board is mutated
    """
    if card == 0:
        board[0] += 1
    if card in [1, 2, 3]:
        if board[7] > 0:
            wasabi_cnt = board[7]
            board[7] = board[7] - 1
            board[card + 3] += 1  # For each wasabi, add a wasabi combo (combo is always +3 index)
        else:
            board[card] += 1
    if card == 4:
        board[7] += 1
    if card == 5:
        board[8] += 1
    if card == 6:
        board[9] += 1
    if card == 7:
        board[10] += 1
    if card == 8:
        board[10] += 2
    if card == 9:
        board[10] += 3
    if card == 10:
        board[11] += 1


def get_maki_score(maki_cnt_list):
    """
    Scores maki rolls for a game
    :param maki_cnt_list: An array of the number of maki rolls each player has. [1, 2] means p1 has 1, p2 has 2.
    :return: an array of scores for the player
    """
    maki_rank = rankdata([_*-1 for _ in maki_cnt_list], method='min')
    maki_score = []
    first_count = np.sum(maki_rank == 1)
    second_count = np.sum(maki_rank == 2)
    for rank in maki_rank:
        if rank == 1:
            maki_score.append(6 / first_count)
        elif rank == 2:
            maki_score.append(3 / second_count)
        else:
            maki_score.append(0)
    return maki_score


def get_pudding_score(pudding_cnt_list):
    """
    Scores pudding for a game
    :param pudding_cnt_list: An array of the number of puddings each player has. [1, 2] means p1 has 1, p2 has 2.
    :return: an array of scores for the player
    """
    pudding_rank = rankdata([_*-1 for _ in pudding_cnt_list], method='min')
    pudding_score = []
    lowest_rank = max(pudding_rank)
    first_count = np.sum(pudding_rank == 1)
    last_count = np.sum(pudding_rank == lowest_rank)
    for rank in pudding_rank:
        if rank == 1:
            pudding_score.append(6 / first_count)
        elif rank == lowest_rank:
            pudding_score.append(-6 / last_count)
        else:
            pudding_score.append(0)
    return pudding_score


def score_game(boards):
    """
    :param boards: array of boards in the game [board1, board2]
    :return: array of scores. [score1, score2]
    """
    scores = []
    makis = []
    puddings = []
    for board in boards:
        scores.append(get_score(board))
        makis.append(board[10])
        puddings.append(board[11])
    maki_scores = get_maki_score(makis)
    pudding_scores = get_pudding_score(puddings)
    for i in range(0, len(scores)):
        scores[i] += maki_scores[i] + pudding_scores[i]
    return scores


def translate_board(board):
    board_list = ast.literal_eval(board)
    res = []
    for i, count in enumerate(board_list):
        res.append(f'{CARDS[i]} X {count}')
    return '  '.join(res)


def convert_hand_to_counter(hand):
    counter = Counter(hand)
    res = [0] * len(CARDS)
    for i in range(len(CARDS)):
        res[i] = counter[i]
    return res


def get_actual_card_pool():
    """
    Creates the card pool from which cards are drawn. Has the same structure as a hand. Types of cards can be removed
    from the pool by commenting out the line where they are added.
    :return: The card pool, a list of cards
    """
    card_pool = []
    card_pool.extend([0] * 14)
    card_pool.extend([1] * 5)
    card_pool.extend([2] * 10)
    card_pool.extend([3] * 5)
    card_pool.extend([4] * 6)
    card_pool.extend([5] * 14)
    card_pool.extend([6] * 14)
    card_pool.extend([7] * 6)
    card_pool.extend([8] * 12)
    card_pool.extend([9] * 8)
    card_pool.extend([10] * 10)

    return card_pool


def is_available_action(hand, action):
    c1 = convert_hand_to_counter(hand)
    c2 = convert_hand_to_counter(action)
    for i in range(c2):
        if c2[i] > c1[i]:
            return False
    return True
