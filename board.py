import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox as tkm
import random

"""
======================================================================
================== BOARD CLASS =======================================
======================================================================
"""
class Board(object):
    """
    represents play board,
    size: size of the playboard
    has methods to print it, place player symbols and check winner
    """
    def __init__(self, size):
        self.size = size
        self.array =  [[' '] * self.size for i in range(self.size)]
        self.win_condition = 3 if size <= 5 else 4  # sets how many you need to win
        self.about_to_win = False    # check if there is only one missing symbol to win
        self.would_win_coords = [] # coords of the cell which when taken would lead to victory

    def print_board(self):
        """
        prints playboard
        just CLI stuff
        """
        for i in range(self.size):
            for j in range(self.size):
                print(self.array[i][j], end='')
            print()
        print()

    def place_symbol(self, x, y, symbol):
        """places player symbol on given coordinates the board"""
        self.array[y][x] = symbol

    def not_taken(self, x, y):
        """check if board on x, y is empty"""
        return self.array[y][x] == ' '

    """ ========= check winner ==============="""

    def check_win(self, player):
        """check if round was won"""
        self.about_to_win = False    # reset this shizz
        for i in range(len(self.would_win_coords)):
            self.would_win_coords.pop()
        self.check_other_direct(player.symbol)

        for i in range(self.size):
            for j in range(self.size):
                if self.check_row(j, i, player.symbol) or self.check_column(j, i, player.symbol) or self.check_diagonaly(j, i, player.symbol):
                    return True
        return False

    def check_row(self, x, y, player_symbol):
        """checks rows"""
        if x + self.win_condition > self.size:
            return False
        else:
            for i in range(self.win_condition):
                if self.array[y][x + i] != player_symbol:
                    # about to win check for AI
                    return False
                else:
                    # about to win check for next AI move
                    if i == self.win_condition - 2 and self.not_taken(x + i + 1, y):
                        self.about_to_win = True
                        self.would_win_coords.append((x + i + 1, y))
            return True

    def check_column(self, x, y, player_symbol):
        """checks columns"""
        if y + self.win_condition > self.size:
            return False
        else:
            for i in range(self.win_condition):
                if self.array[y + i][x] != player_symbol:
                    return False
                else:
                    # about to win check for next AI move
                    if i == self.win_condition - 2 and self.not_taken(x, y + i + 1):
                        self.about_to_win = True
                        self.would_win_coords.append((x, y + i + 1))
            return True

    def check_diagonaly(self, x, y, player_symbol):
        """checks both diagonals"""
        result = False
        if x + self.win_condition <= self.size and y - self.win_condition + 1 >= 0:
            result = self.diagonal_up(x, y, player_symbol)
        if not result:  # if not on first diagonal check second
            if x + self.win_condition <= self.size and y + self.win_condition <= self.size:
                result = self.diagonal_down(x, y, player_symbol)
        return result

    def diagonal_down(self, x, y, player_symbol):
        """checks top left - right bottom diagonal"""
        for k in range(self.win_condition):
            if self.array[y + k][x + k] != player_symbol:
                return False
            else:
                # about to win check for AI
                if k == self.win_condition - 2 and self.not_taken(x + k + 1, y + k + 1):
                    self.about_to_win = True
                    self.would_win_coords.append((x + k + 1, y + k + 1))
        return True

    def diagonal_up(self, x, y, player_symbol):
        """checks left bottom - right top diagonal"""
        for k in range(self.win_condition):
            if self.array[y - k][x + k] != player_symbol:
                return False
            else:
                # about to win check for AI
                if k == self.win_condition - 2 and self.not_taken(x + k + 1, y - k - 1):
                    self.about_to_win = True
                    self.would_win_coords.append((x + k + 1, y - k - 1))
        return True


    """
    ==================== JUST AI SHIT =============================
    """
    def check_other_direct(self, player_symbol):
        """checks the board in other direction to check, whether the player is going to win in next turn"""
        for i in range(self.size - 1, -1, -1):
            for j in range(self.size - 1, -1, -1):
                self.check_row_other(j, i, player_symbol)
                self.check_column_other(j, i, player_symbol)
                self.check_diagonaly_other(j, i, player_symbol)

    def check_row_other(self, x, y, player_symbol):
        if x - self.win_condition >= 0:
            for k in range(self.win_condition - 1):
                if self.array[y][x - k] != player_symbol:
                    return
                if k == self.win_condition - 2 and self.not_taken(x - k - 1, y):
                    self.would_win_coords.append((x - k - 1, y))
                    self.about_to_win = True

    def check_column_other(self, x, y, player_symbol):
        if y - self.win_condition >= 0:
            for k in range(self.win_condition - 1):
                if self.array[y - k][x] != player_symbol:
                    return
                if k == self.win_condition - 2 and self.not_taken(x, y - k - 1):
                    self.would_win_coords.append((x, y - k - 1))
                    self.about_to_win = True

    def check_diagonaly_other(self, x, y, player_symbol):
        # TODO: write to normal check???
        if x + self.win_condition < self.size and y - self.win_condition >= 0:
            self.diagonal_up_other(x, y, player_symbol)

        if x - self.win_condition + 1 >= 0 and y - self.win_condition + 1 >= 0:
            self.diagonal_down_other(x, y, player_symbol)

    def diagonal_up_other(self, x, y, player_symbol):
        for k in range(self.win_condition - 1):
            if self.array[y - k][x + k] != player_symbol:
                return
            if k == self.win_condition - 2 and self.not_taken(x + k + 1, y - k - 1):
                self.would_win_coords.append((x + k + 1, y - k - 1))
                self.about_to_win = True

    def diagonal_down_other(self, x, y, player_symbol):
        for k in range(self.win_condition - 1):
            if self.array[y - k][x - k] != player_symbol:
                return
            if k == self.win_condition - 2 and self.not_taken(x - k - 1, y - k - 1):
                self.would_win_coords.append((x - k - 1, y - k - 1))
                self.about_to_win = True


    def reset(self):
        """resets the board"""
        self.array = [[' '] * self.size for i in range(self.size)]
        self.about_to_win = False
        self.would_win_coords = []


    def get_human_taken(self, AISymbol):
        return [(j, i) for i in range(self.size) for j in range(self.size) if self.array[i][j] == AIsymbol]

    def get_aviable_moves(self):
        """returns list aviable cells"""
        return [(j, i) for i in range(self.size) for j in range(self.size) if self.not_taken(j, i)]
