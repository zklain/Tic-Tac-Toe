import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox as tkm
import random

import board as b
import player as p
import game as g


"""
======================================================================
================== GAME SETTINGS CLASSES =============================
======================================================================
"""
class GameSettings(tk.Frame):
    def __init__(self, parent, controller, ai):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.p1 = None
        self.p2 = None
        self.ai = ai
        self.board_size = 0
        self.board = None
        self.game = None
        self.of_rounds = 0

        self.create_widgets()

    def create_widgets(self):
        """creates all widgets for GameSettings"""
        # heading label
        self.label = tk.Label(self, text="Game Settings", bg='white', fg='black', font=self.controller.BIG_FONT)
        self.label.pack(expand=True, fill='both')

        #default values
        size = tk.IntVar()
        size.set(3)
        n1 = tk.StringVar()
        n1.set("John")

        # settings container
        self.settings_container = tk.Frame(self, bg='white')
        self.settings_container.pack(fill='both', expand=True)
        if not self.ai:
            # Player1
            # container
            self.p1_cont = tk.Frame(self.settings_container, bg='white')
            self.p1_cont.pack(fill='both', expand=True)
            # name label
            self.p1_name_label = tk.Label(self.p1_cont, bg='white', text='Player 1:')
            self.p1_name_label.pack(side=tk.TOP, expand=True)
            # entry field
            self.p1_name = tk.Entry(self.p1_cont)
            self.p1_name.pack(side=tk.BOTTOM, expand=True)
            # TODO: symbol

            # Player2
            # container
            self.p2_cont = tk.Frame(self.settings_container, bg='white')
            self.p2_cont.pack(fill='both', expand=True)
            # name label
            self.p2_name_label = tk.Label(self.p2_cont, bg='white', text='Player 2: ')
            self.p2_name_label.pack(side=tk.TOP, expand=True)
            # entry field
            self.p2_name = tk.Entry(self.p2_cont)
            self.p2_name.pack(side=tk.BOTTOM, expand=True)
            # TODO: symbol    # PvP game - has entries for 2 player names
        else:
            # Player1
            # container
            self.p1_cont = tk.Frame(self.settings_container, bg='white')
            self.p1_cont.pack(fill='both', expand=True)
            # name label
            self.p1_name_label = tk.Label(self.p1_cont, bg='white', text='Player: ')
            self.p1_name_label.pack(side=tk.LEFT, expand=True, fill='x')
            # entry field
            self.p1_name = tk.Entry(self.p1_cont, text=n1)
            self.p1_name.pack(side=tk.RIGHT, expand=True, fill='x')

        # board size
        self.b_size_label = tk.Label(self.settings_container, bg='white', text="Board Size: ")
        self.b_size_label.pack(expand=True)
        self.b_size_entry = tk.Entry(self.settings_container, width=3, text=size)
        self.b_size_entry.pack(expand=True)

        # warning label
        self.warn_frame = tk.Frame(self, bg='white')
        self.warn_frame.pack(fill='both', expand=True)
        self.warning_label = tk.Label(self.warn_frame, text="", bg='white', fg='red', font=self.controller.WARN_FONT)
        self.warning_label.pack()

        # buttons frame
        self.controll_frame = tk.Frame(self, bg='white')
        self.controll_frame.pack(fill='both', expand=True)
        # start game button
        self.play_button = tk.Button(self.controll_frame, text="PLAY", bg='white', fg='green', font=self.controller.BIG_FONT, command=lambda: self.start_game())
        self.play_button.pack(side=tk.LEFT, expand=True, fill='x')
        # back button
        self.back_button = tk.Button(self.controll_frame, text="Menu", bg='white',font=self.controller.BIG_FONT, command=lambda: self.controller.show_frame("StartMenu"))
        self.back_button.pack(side=tk.RIGHT, expand=True, fill='x')

    def set_players(self):
        """retrieves players names from entries"""
        name1 = self.p1_name.get()
        self.p1 = p.HumanPlayer(name1, "X")
        if not self.ai:
            name2 = self.p2_name.get()
            self.p2 = p.HumanPlayer(name2, "O")
        else:
            self.p2 = p.AIPlayer("O")

    def set_board_size(self):
        """retrieves board_size from entry"""
        self.board_size = int(self.b_size_entry.get())

    def set_game(self):
        """sets the game with given settings"""
        self.set_board_size()
        self.set_players()
        self.board = b.Board(self.board_size)
        self.game = g.Game(
            self.parent,
            self.controller,
            self.board_size,
            self.p1,
            self.p2
        )

    def check_all_correct(self):
        """check if entries filled correctly"""
        size = int(self.b_size_entry.get())
        if size < 3 or size > 10:
            self.warning_handle("Board size must be > 2 and < 11")
            return False
        return True
        # TODO: move all to set

    def check_all_set(self):
        """check if all entries are filled"""
        if self.not_filled(self.p1_name):
            self.warning_handle("Your name, Sir!")
            return False

        if not self.ai and self.not_filled(self.p2_name):
            self.warning_handle("Wie heisst du?!")
            return False

        if self.not_filled(self.b_size_entry):
            self.warning_handle("Just fill it all! Cant't hurt that much!")
            return False
        return True

    def warning_handle(self, message):
        """handles warning messages on the warning label"""
        self.warning_label["text"] = message

    def not_filled(self, entry):
        """checks if entry is filled"""
        return entry.get() == ''

    def start_game(self):
        """
        if all settings are set, starts a game, switches frame to game frame
        """
        if self.check_all_set():
            if self.check_all_correct():
                # set game settings
                self.set_game()
                # add game frame to fraems dictionary
                self.controller.add_frame("Game", self.game)
                self.controller.frames["Game"].grid(row=0, column=0, sticky="nsew")
                # show game frame
                self.controller.show_frame("Game")
                self.game.play_first_move()
