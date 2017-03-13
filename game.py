import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox as tkm
import random

import board as b
import player as p


"""
=====================================================================
================== GAME CLASS ======================================
======================================================================
"""

class Game(tk.Frame):
    """
    Game GUI... creates playboard for a round
    parent: tkinter master
    controller: is the TicTacToe class, controlls frame changeing
    board_size: sets playboard size
    p1: player 1
    p2: player 2
    """
    def __init__(self, parent, controller, board_size, p1, p2):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.board_size = board_size
        self.board = b.Board(board_size)
        self.p1 = p1    # first player
        self.p2 = p2    # second player, AI player is always p2
        self.ai = isinstance(self.p2, p.AIPlayer)  # if AI controlled palyer
        self.current_player = p1
        self.create_widgets()

        self.turn = 0

    def create_widgets(self):
        """creates all game widgets"""

        # TODO: text and shizz in parent only???
        # info frame
        self.info_frame = tk.Frame(self, bg="white")
        self.info_frame.pack(fill="both", expand=True)

        # player label
        self.player_label = tk.Label(self.info_frame, text="Player:  {}".format(self.current_player.name), bg="white", fg="black", font=self.controller.NORM_FONT)
        self.player_label.pack(side=tk.LEFT, expand=True, fill='x')

        # score label
        self.score_label = tk.Label(self.info_frame,
        text="Score: {} : {}".format(self.p1.score, self.p2.score), bg="white", fg="black", font=self.controller.NORM_FONT)
        self.score_label.pack(side=tk.LEFT, expand=True, fill='x')

        # buttons
        self.create_board()

        # warning label
        self.warn_frame = tk.Frame(self, bg='white')
        self.warn_frame.pack(fill='both', expand=True)
        self.warning_label = tk.Label(self.warn_frame, text="", bg='white', fg='red', font=self.controller.WARN_FONT)
        self.warning_label.pack()

        # game controll frame
        self.controll_frame = tk.Frame(self, bg='white')
        self.controll_frame.pack(fill='both', expand=True)

        # reset button
        self.reset_button = tk.Button(self.controll_frame, text="Reset", bg='white',font=self.controller.NORM_FONT, command=lambda: self.really_reset())
        self.reset_button.pack(side=tk.LEFT, expand=True, fill='x')

        # exit button
        self.exit_button = tk.Button(self.controll_frame, text="Exit", bg='white',font=self.controller.NORM_FONT, command=lambda: self.really_quit())
        self.exit_button.pack(side=tk.RIGHT, expand=True, fill='x')

    def create_board(self):
        """creates the playboard"""
        # playboard frame
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(fill="both", expand=tk.NO)
        # buttons
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j] = tk.Button(
                    self.board_frame,
                    height=3,
                    width=7,
                    font=self.controller.BIG_FONT,
                    text='', bg='white',
                    command=lambda x=j, y=i: self.click(self.buttons[y][x])
                )
                self.buttons[i][j].grid(row=i, column=j)

    def play_first_move(self):
        """makes the first move in case computer player is the first player"""
        if self.ai and self.current_player == self.p2:   # if starting player is AI, make first move
            first_move = self.p2.move(self.board)
            self.handle_move(first_move)
        else:                  # if AI but HUmanPlayer starts or PvP
            pass

    def handle_move(self, coords):
        """handles move on given coords"""
        x, y = coords
        self.board.place_symbol(x, y, self.current_player.symbol)   # place to board
        self.place_symbol(x, y)                                     # place to button

        if self.is_round_end():     # check if round ended
            self.handle_round_end() # handle ending
        else:
            self.change_players()   # change_players if round hasn't ended
            self.turn += 1          # iterate turn

    def click(self, button):

        """represents a click action on a button"""
        if self.is_round_end():    # if game hastn't ended
            self.handle_round_end()
        else:
            coords = self.get_bttn_coords(button)   # retrieve buttons coordinates
            if self.can_move(coords):   # if correct coords
                self.handle_move(coords)   # place symbol
                if self.ai and self.turn > 0:                # if computer player play AI move
                    self.handle_move(self.p2.move(self.board))


    def handle_round_end(self):
        """handles actions if round has ended"""
        if self.its_win():      # if round won
            self.win_handle()
        else:                   # if draw
            self.draw_message()

        if self.ask_play_again():   # ask whether to play again
            self.new_round()        # start new round
        else:
            self.back_to_sett_menu()  # quit if player doesnt want another round

    def its_draw(self):
        """check if round is a draw"""
        return self.turn == self.board_size ** 2

    def its_win(self):
        """check if round was won by one of the players"""
        return self.board.check_win(self.current_player)

    def is_round_end(self):
        """check if round has ended"""
        return self.its_win() or self.its_draw()

    def win_handle(self):
        """handles win result"""
        self.win_message()              # win messagebox
        self.current_player.add_score() # adds score to winner
        self.set_next_start_player()    # set next start player

    def get_bttn_coords(self, button):
        """retrieves button coordinates"""
        info = button.grid_info()
        coords = (info["column"], info["row"])
        return coords

    def can_move(self, coords):
        """check if can place symbol on given coordinates"""
        x, y = coords
        if not self.board.not_taken(x, y):
            self.warning_handle('Already taken!', 'red') # red warning
            return False
        else:
            self.warning_handle('OK!', 'green') # green OK if not taken
            return True

    def place_symbol(self, x, y):
        """places current players symbol on the button"""
        self.buttons[y][x].configure(text=self.current_player.symbol)

    def new_round(self):
        """sets stuff for another round of the game"""
        self.reset()
        self.update_score_label()   # updates score labels
        self.change_label_p_name()  # players name
        self.clear_warning_label()  # clear warning label

    def reset(self):
        """resets the plyboard when reset button clicked"""
        self.reset_buttons()        # resets buttons board
        self.board.reset()          # resets board
        self.choose_start_player()  # chooses start player
        self.play_first_move()      # in case computer won the previous
        self.turn = 0               # anulates the score
        

    def clear_warning_label(self):
        """clears warning label messages"""
        self.warning_label.configure(text='')

    def update_score_label(self):
        """updates score"""
        self.score_label.configure(text="Score: {} : {}".format(self.p1.score, self.p2.score))

    def reset_buttons(self):
        """resets the board, replaces symbols on buttons with empty string"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].configure(text='')


    def warning_handle(self, message, color):
        """handles warning messages on warning label"""
        self.warning_label["fg"] = color
        self.warning_label["text"] = message

    def change_players(self):
        """changes players"""
        if self.current_player == self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1
        self.change_label_p_name()

    def change_label_p_name(self):
        """changes players names on the label"""
        self.player_label.configure(text="Player:  {}".format(self.current_player.name))

    def choose_start_player(self):
        """chooses starting player"""
        if self.p2.won_previous:
            self.current_player = self.p2
        else:
            self.current_player = self.p1

    def set_next_start_player(self):
        """set winners won_previous attribute to true, defeaters to false"""
        if self.current_player == self.p1:
            self.p1.prev_won()
            self.p2.prev_lost()
        else:
            self.p2.prev_won()
            self.p1.prev_lost()

    def win_message(self):
        """message window, informs about win"""
        tkm.showinfo("Round won!", "{} is the winner!".format(self.current_player.name))

    def draw_message(self):
        """message window, informs about a draw result"""
        tkm.showinfo("Draw!", "It's a draw!")

    def ask_play_again(self):
        """asks player whether to play again"""
        return tkm.askyesno("Play Again?", "Would you like another round?")

    def total_wiener_schnitzel(self):
        """return string with total winner"""
        if self.p1.score == self.p2.score:
            return "It's a Draw!"
        if self.p1.score > self.p2.score:
            return self.p1.name + " is the total wiener schnitzel"
        elif self.p1.score < self.p2.score:
            return self.p2.name + " is the total wiener schnitzel"

    def total_wiener_msg(self):
        tkm.showinfo("Game End!", self.total_wiener_schnitzel())

    def really_quit(self):
        if tkm.askyesno("Exit?", "Do you really wish to end the game?"):
            self.total_wiener_msg()
            self.back_to_sett_menu()

    def really_reset(self):
        if tkm.askyesno("Reset?", "Do you really wish to reset the board?"):
            self.reset()

    def back_to_sett_menu(self):
        self.controller.show_frame("GameSettings")
