import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox as tkm
import random

from board import *
from player import *
from game_settings import *
from game import *


"""
======================================================================
================== START MENU CLASS ==================================
======================================================================
"""
class StartMenu(tk.Frame):
    """Start menu"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # label
        self.label = tk.Label(self, text="Tic-Tac-Toe", font=self.controller.TITLE_FONT, bg='white', width=16, height=2)
        self.label.pack(fill='both')

        self.buttons_container = tk.Frame(self, bg='white')
        self.buttons_container.pack(fill='both', expand=True)
        # start PvP game
        self.button1 = tk.Button(self.buttons_container, text="PvP Game", font=self.controller.BIG_FONT, height=2, bg='white', command=lambda: self.raise_game_settings(False))
        # start single player game
        self.button2 = tk.Button(self.buttons_container, text="SP Game", font=self.controller.BIG_FONT, height=2, bg='white', command=lambda: self.raise_game_settings(True))
        # exit game
        self.button3 = tk.Button(self.buttons_container, text="QUIT", font=self.controller.BIG_FONT, height=2, bg='white', fg='red', command=lambda: quit())
        self.button1.pack(fill='both')
        self.button2.pack(fill='both')
        self.button3.pack(fill='both')

    def raise_game_settings(self, ai):
        """
        creates GameSettings frame, diffrent for Single Player and PvP game.
        If there already is one created and the AI parameter of the existing and new frame differs,
        destroys the existing frame first
        """
        if "GameSettings" not in self.controller.frames:  # check if frame exists
            g_sett = GameSettings(self.parent, self.controller, ai)
            self.controller.add_frame("GameSettings", g_sett)
            self.controller.frames["GameSettings"].grid(row=0, column=0, sticky="nsew")
        else:
            gs = self.controller.frames["GameSettings"]
            if not gs.ai == ai:    # if created settings and new settings ai differs
                del self.controller.frames["GameSettings"]
                # create again
                g_sett = GameSettings(self.parent, self.controller, ai)
                self.controller.add_frame("GameSettings", g_sett)
                self.controller.frames["GameSettings"].grid(row=0, column=0, sticky="nsew")
        # show GameSettings frame
        self.controller.show_frame("GameSettings")



"""
======================================================================
================== TIC-TAC_TOE CLASS =================================
======================================================================
"""
class TicTacToe(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self, bg='white')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Tic Tac Toe")
        self.resizable(0, 0)

        # FONTS
        self.TITLE_FONT = tkf.Font(family='Helvetica', size=20, weight='bold')
        self.BIG_FONT = tkf.Font(family='Helvetica', size=14, weight='bold')
        self.NORM_FONT = tkf.Font(family='Helvetica', size=10)
        self.WARN_FONT = tkf.Font(family='Helvetica', size=10, weight='bold')

        self.frames = {}

        self.frames["StartMenu"] = StartMenu(parent=container, controller=self)
        self.frames["StartMenu"].grid(row=0, column=0, sticky="nsew")

        # show star menu as first frame
        self.show_frame("StartMenu")

    def show_frame(self, frame_name):
        """shows frame with given name"""
        frame = self.frames[frame_name]
        frame.tkraise()

    def add_frame(self, name, frame):
        """adds frame to frame dictionary"""
        self.frames[name] = frame


# run game
if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.mainloop()

# TODO: validate
# TODO: exceptions
# TODO: not-scalable
# TODO: text size
# TODO: AI
# TODO: kivy branch
# TODO: add if
