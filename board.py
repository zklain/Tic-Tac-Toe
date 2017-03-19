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
        self.array = [[' '] * self.size for i in range(self.size)]
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
        self.would_win_coords = []

        for i in range(self.size):
            for j in range(self.size):
                self.check_other_direct(j, i, player.symbol)
                if self.check_row(j, i, player.symbol) \
                or self.check_column(j, i, player.symbol) \
                or self.check_diagonaly(j, i, player.symbol):
                    # print("TRUE; ABOUT TO WIN: {}".format(self.about_to_win))
                    # print("COORDS: {}".format(self.would_win_coords))
                    return True
        # print("FALSE; ABOUT TO WIN: {}".format(self.about_to_win))
        # print("COORDS: {}".format(self.would_win_coords))
        return False

    def check_row(self, x, y, player_symbol):
        """checks rows from left to rigth"""
        if x + self.win_condition > self.size:
            return False
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
        """checks columns from top to bottom"""
        if y + self.win_condition > self.size:
            return False
        for i in range(self.win_condition):
            if self.array[y + i][x] != player_symbol:
                return False
            # about to win check for next AI move
            if i == self.win_condition - 2 and self.not_taken(x, y + i + 1):
                self.about_to_win = True
                self.would_win_coords.append((x, y + i + 1))
        return True

    def check_diagonaly(self, x, y, player_symbol):
        """checks both diagonals"""
        result = False
        if (x - self.win_condition) + 1 >= 0 and y + self.win_condition <= self.size:
            result = self.diagonal_tr_bl(x, y, player_symbol)
        if not result:  # if not on first diagonal check second
            if x + self.win_condition <= self.size and y + self.win_condition <= self.size:
                result = self.diagonal_tl_br(x, y, player_symbol)
        return result

    def diagonal_tl_br(self, x, y, player_symbol):
        """checks diagonaly top left -> bottom rigth"""
        for k in range(self.win_condition):
            if self.array[y + k][x + k] != player_symbol:
                return False
            # about to win check for AI
            if k == self.win_condition - 2 and self.not_taken(x + k + 1, y + k + 1):
                self.about_to_win = True
                self.would_win_coords.append((x + k + 1, y + k + 1))
        return True

    def diagonal_tr_bl(self, x, y, player_symbol):
        """checks diagonaly top right -> bottom left"""
        for k in range(self.win_condition):
            if self.array[y + k][x - k] != player_symbol:
                return False
            # about to win check for AI
            if k == self.win_condition - 2 and self.not_taken(x - k - 1, y + k + 1):
                self.about_to_win = True
                self.would_win_coords.append((x - k - 1, y + k + 1))
        return True


    """
    ==================== JUST AI SHIT =============================
    """
    def check_other_direct(self, x, y, player_symbol):
        """
        checks the board in other direction to check, whether the player is going to win in next turn
        """
        self.check_row_rl(x, y, player_symbol)
        self.check_column_up(x, y, player_symbol)
        self.check_diagonaly_bt(x, y, player_symbol)

    def check_row_rl(self, x, y, player_symbol):
        """check row from right to left"""
        if (x - self.win_condition) + 1>= 0:
            for k in range(self.win_condition):
                if self.array[y][x - k] != player_symbol:
                    return
                if k == self.win_condition - 2 and self.not_taken(x - k - 1, y):
                    self.would_win_coords.append((x - k - 1, y))
                    self.about_to_win = True

    def check_column_up(self, x, y, player_symbol):
        """check column bottom to top"""
        if (y - self.win_condition) + 1>= 0:
            for k in range(self.win_condition):
                # if all symbols so far are player symbol
                if self.array[y - k][x] != player_symbol:   
                    return
                if k == self.win_condition - 2 and self.not_taken(x, y - k - 1):
                    self.would_win_coords.append((x, y - k - 1))
                    self.about_to_win = True

    def check_diagonaly_bt(self, x, y, player_symbol):
        """checks both diagonals"""
        if x + self.win_condition <= self.size and (y - self.win_condition) + 1 >= 0:
            self.diagonal_bl_tr(x, y, player_symbol)

        if (x - self.win_condition) + 1 >= 0 and (y - self.win_condition) + 1 >= 0:
            self.diagonal_br_tl(x, y, player_symbol)

    def diagonal_bl_tr(self, x, y, player_symbol):
        """check diagonal bottom left -> top rigth"""
        for k in range(self.win_condition):
            if self.array[y - k][x + k] != player_symbol:
                return
            if k == self.win_condition - 2 and self.not_taken(x + k + 1, y - k - 1):
                self.would_win_coords.append((x + k + 1, y - k - 1))
                self.about_to_win = True

    def diagonal_br_tl(self, x, y, player_symbol):
        """check diagonal bottom right -> top left"""
        for k in range(self.win_condition):
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

    def get_available_moves(self):
        """returns list aviable cells"""
        return [(j, i) for i in range(self.size) for j in range(self.size) if self.not_taken(j, i)]
