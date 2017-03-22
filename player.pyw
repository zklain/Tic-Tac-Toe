import random


"""
======================================================================
================== PLAYER CLASSES ====================================
======================================================================
"""
class Player(object):
    """
    represents a player
    name: players name
    symbol: players symbol
    """
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol    # players symbol
        self.score = 0          # score = rounds won
        self.won_previous = False # remember whether he won the previous round (he will start if so)

    def add_score(self):
        """adds points"""
        self.score += 1

    def prev_won(self):
        """sets won_previous to True"""
        self.won_previous = True

    def prev_lost(self):
        """sets won_previes to False"""
        self.won_previous = False


class HumanPlayer(Player):
    """Human controlled player"""
    def __init__(self, name, symbol):
        super(HumanPlayer, self).__init__(name, symbol)


class AIPlayer(Player):
    """Computer controlled player"""
    def __init__(self, symbol):
        super(AIPlayer, self).__init__("Computer", symbol)
        self.placed = []

    def move(self, board):
        """returns coords for AI player move"""
        available = board.get_available_moves()
        if board.about_to_win: # if human player is going to win
            # choose coords from list of coords which player has to take to win
            coords = random.choice(board.would_win_coords)
        else:
            coords = random.choice(available)
        self.placed.append(coords)
        return coords


 
