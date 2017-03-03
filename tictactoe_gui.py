import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox as tkm
import sys
import time

class GuiGame():
    # TODO: change to frame child

    """
    Game GUI... creates playboard for a round
    master: tkinter master
    board_size: sets playboard size
    p1: player 1
    p2: player 2
    """
    def __init__(self, master, board_size, p1, p2):
        self.frame = tk.Frame(master)
        self.frame.pack(expand=tk.NO)
        self.master = master
        self.master.title("Tic Tac Toe")

        self.board_size = board_size
        self.board = Board(board_size)
        self.p1 = p1
        self.p2 = p2

        self.choose_start_player()  # sets current player
        self.round_over = False # if round over
        self.turn = 0   # rounds counter

        """===================== GUI shizz =============================="""

        # font
        self.main_font = tkf.Font(family='Helvetica', size=12, weight='bold')

        #info frame
        self.info_frame = tk.Frame(self.frame, bg="white")
        self.info_frame.pack(fill="both", expand=tk.NO)

        #player label
        self.player_label = tk.Label(self.info_frame, text="Player:  {}".format(self.current_player.name), bg="white", fg="black")
        self.player_label.pack(side=tk.LEFT)

        # score label
        self.score_label = tk.Label(self.info_frame,
        text="Score: {} : {}".format(self.p1.score, self.p2.score), bg="white", fg="black")
        self.score_label.pack(side=tk.RIGHT)

        # buttons
        self.create_board()

        #warning label
        self.warn_frame = tk.Frame(self.frame, bg='white')
        self.warn_frame.pack(fill='both', expand=tk.NO)
        self.warning_label = tk.Label(self.warn_frame, text="", bg='white', fg='red')
        self.warning_label.pack()

    """============= methods ======================"""

    def create_board(self):
        """creates the playboard"""
        # playboard frame
        self.board_frame = tk.Frame(self.frame, )
        self.board_frame.pack(fill="both", expand=tk.NO)
        #buttons
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j] = tk.Button(self.board_frame, height=3, width=7, font=self.main_font, text='', bg='white', command=lambda x=j, y=i: self.click(self.buttons[y][x]))
                self.buttons[i][j].grid(row=i, column=j)

    def play(self):
        pass

    def click(self, button):
        """represents a click action on button"""
        if not self.round_end():    # if game hastn't ended
            # TODO: add if ai

            coords = self.get_bttn_coords(button)   # retrieve buttons coordinates
            if self.can_move(coords):   # if correct coords
                self.move(coords)   # place symbol
                self.turn += 1          # iterate turns

                if not self.round_end():    # if not draw or won
                    self.change_players()   # change current player
                else:
                    if self.its_win():    # if round won
                        self.win_handle()
                    elif self.its_draw():   # if draw
                        self.draw_handle()

                    if self.ask_play_again():     # ask whether to play again
                        self.new_round()        # start new round
                    else:
                        quit()      # quit if player doesnt wants another round

    def its_draw(self):
        """check if round is a draw"""
        return self.turn == self.board_size ** 2

    def its_win(self):
        """check if round was won by one of the players"""
        return self.board.check_win(self.current_player)

    def round_end(self):
        """check if round has ended"""
        return self.its_win() or self.its_draw()

    def win_handle(self):
        """handles win result"""
        self.win_message()
        self.current_player.add_score()
        self.current_player.prev_won()

    def draw_handle(self):
        """handles draw result"""
        self.draw_message()

    def get_bttn_coords(self, button):
        """retrieves button coordinates"""
        info = button.grid_info()
        coords = (info["row"], info["column"])
        return coords

    def can_move(self, coords):
        """check if can place symbol on given coordinates"""
        if self.board.already_taken(coords):
            self.warning_handle('Already taken!', 'red')
            return False
        else:
            self.warning_handle('OK!', 'green')
            return True

    def place_symbol(self, x, y):
        """places current players symbol on the button"""
        self.buttons[y][x].configure(text=self.current_player.symbol)

    def move(self, coords):
        """represents players move, places maark on buttons coordinates"""
        y, x = coords
        self.board.place_symbol(x, y, self.current_player.symbol)   # place to board
        self.place_symbol(x, y)   # place to button

    def new_round(self):
        """sets stuff for another round of the game"""
        # TODO: not destroy?
        self.reset_buttons()        # resets buttons board
        self.turn = 0       # anulates the score
        self.board.reset()  # resets board
        self.set_next_start_player()  # sets previous round winner
        self.choose_start_player()  # sets start player
        self.update_score_label() # updates score labels
        self.clear_warning_label()  #clear warning label

    def clear_warning_label(self):
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
        tkm.showinfo("Game won!", "{} is a proper cunt!".format(self.current_player.name))

    def draw_message(self):
        """message window, informs about a draw result"""
        tkm.showinfo("Draw!", "It's a draw!")

    def ask_play_again(self):
        """asks player whether to play again"""
        return tkm.askyesno("Play Again?", "Would you like another round?")

# TODO: scalable
# TODO: message window
# TODO: run without console
# TODO: make exe
# TODO: text size
# TODO: reset - play again window
# TODO: play again message
# TODO: GUI for menu, Gui for game
# TODO: AI
# TODO: makegui inherit from game


class Board(object):
    """
    represents play board,
    size: size of the playboard
    has methods to print it, place player symbols and check winner
    """
    def __init__(self, size):
        self.size = size
        self.array =  [[''] * self.size for i in range(self.size)]
        self.win_condition = size # TODO: you know...

    def print_board(self):
        """prints playboard"""
        for i in range(self.size):
            for j in range(self.size):
                print(self.array[i][j], end='')
            print()
        print()

    def place_symbol(self, x, y, symbol):
        """places player symbol on given coordinates the board"""
        self.array[y][x] = symbol

    def already_taken(self, coords):
        """check if cell is already taken"""
        pos = self.array[coords[0]][coords[1]]
        return pos == 'O' or pos == 'X'
        # TODO: you know


    """ ========= check winner ==============="""
    def check_win(self, player):
        """check if round was won"""
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
                    return False
            return True

    def check_column(self, x, y, player_symbol):
        """checks columns"""
        if y + self.win_condition > self.size:
            return False
        else:
            for i in range(self.win_condition):
                if self.array[y + i][x] != player_symbol:
                    return False
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
        return True

    def diagonal_up(self, x, y, player_symbol):
        """checks left bottom - right top diagonal"""
        for k in range(self.win_condition):
            if self.array[y - k][x + k] != player_symbol:
                return False
        return True

    def reset(self):
        self.array = [[''] * self.size for i in range(self.size)]

    def is_empty(self, x, y):
        return self.array[y][x] == ''

    def get_ai_taken(self):
        pass

    def get_aviable_moves(self):
        return [(i,j) for i in range(self.size) for j in range(self.size) if is_empty(j,i)]

class Player(object):
    """
    represents a player
    symbol: players symbol
    """
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol    # players symbol
        self.score = 0          # score = rounds won
        self.won_previous = False    # remember whether he won the previous round (he will start if so)

    def add_score(self):
        """adds points"""
        self.score += 1

    def prev_won(self):
        self.won_previous = True

    def prev_lost(self):
        self.won_previous = False

class HumanPlayer(Player):
    """docstring for HumanPlayer."""
    def __init__(self, name, symbol):
        super(HumanPlayer, self).__init__(name, symbol)

class AIPlayer(Player):
    """docstring for AIPlayer."""
    def __init__(self, name, symbol):
        super(AIPlayer, self).__init__(name, symbol)

    def find_best(aviable, taken):
        pass


    def move(self, board):
        moves = board.get_aviable_moves()



class TicTacToe(object):
    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.board_size = 0
        self.board = None
        self.tk_root = tk.Tk()
        self.game = None


    def set_players(self):
        name1 = input("Player 1 (X), choose your name: ")
        name2 = input("Player 2 (O), choose your name: ")
        self.p1 = HumanPlayer(name1, "X")
        self.p2 = HumanPlayer(name2, "O")

    def game_settings(self):
        while True:
            try:
                n = int(input("Set board size: "))
                self.board_size = n
                return
            except Exception as e:
                print (e)

    def start_game(self):
        self.set_players()
        self.game_settings()
        self.game = GuiGame(self.tk_root, self.board_size, self.p1, self.p2)
        self.tk_root.mainloop()


#
# p1 = HumanPlayer("Peter", "X")
# p2 = HumanPlayer("Zdenko", "O")
# root = tk.Tk()
# game = GuiGame(root, 3, p1, p2)
# root.mainloop()


ttt = TicTacToe()
ttt.start_game()
