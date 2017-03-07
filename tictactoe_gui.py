import tkinter as tk
import tkinter.font as tkf
import tkinter.messagebox as tkm
import random

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
        self.board = Board(board_size)
        self.p1 = p1    # first player
        self.p2 = p2    # second player, AI player is always p2
        self.ai = isinstance(self.p2, AIPlayer)  # if AI controlled palyer
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
        self.reset_buttons()        # resets buttons board
        self.turn = 0               # anulates the score
        self.board.reset()          # resets board
        self.choose_start_player()  # chooses start player
        self.update_score_label()   # updates score labels
        self.change_label_p_name()  # players name
        self.clear_warning_label()  # clear warning label
        self.play_first_move()      # in case computer won the previous


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

    def reset(self):
        """resets the plyboard when reset button clicked"""
        self.reset_buttons()
        self.board.reset()
        self.choose_start_player()
        self.play_first_move()

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
        self.array =  [[''] * self.size for i in range(self.size)]
        self.win_condition = size if size < 5 else size-1  # sets how many you need to win
        self.about_to_win = False    # check if there is only one missing symbol to win
        self.would_win_coords = ()  # coords of the cell which when taken would lead to victory

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
        return self.array[y][x] == ''

    """ ========= check winner ==============="""

    def check_win(self, player):
        """check if round was won"""
        self.about_to_win = False    # reset this shizz
        self.would_win_coords = ()
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
                        self.would_win_coords = (x + i + 1, y)
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
                        self.would_win_coords = (x, y + i + 1)


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
                    self.would_win_coords = (x + k + 1, y + k + 1)
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
                    self.would_win_coords = (x + k + 1, y - k - 1)
        return True

    def reset(self):
        """resets the board"""
        self.array = [[''] * self.size for i in range(self.size)]
        self.about_to_win = False
        self.would_win_coords = ()


    def get_human_taken(self, AISymbol):
        return [(j, i) for i in range(self.size) for j in range(self.size) if self.array[i][j] == AIsymbol]

    def get_aviable_moves(self):
        """returns list aviable cells"""
        return [(j, i) for i in range(self.size) for j in range(self.size) if self.not_taken(j, i)]


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
        self.won_previous = False    # remember whether he won the previous round (he will start if so)

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
        aviable = board.get_aviable_moves()
        if self.about_to_win(board):
            coords = board.would_win_coords
            #debugging
            # print("about to win, {}".format(coords))
        else:
            coords = random.choice(aviable)
        self.placed.append(coords)
        # print (aviable)
        return coords

    # def find_best(self, board):
    #     aviable = board.get_aviable_moves()
    #     if len(self.placed) > 0:
    #         for c in aviable:
    #             if c + 1 in

    # def is_neighbour(self, coords):
    #     pass

    def about_to_win(self, board):
        """checks if the other player is going to win"""
        return board.about_to_win



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
            self.p1_name = tk.Entry(self.p1_cont)
            self.p1_name.pack(side=tk.RIGHT, expand=True, fill='x')

        # board size
        self.b_size_label = tk.Label(self.settings_container, bg='white', text="Board Size: ")
        self.b_size_label.pack(expand=True)
        self.b_size_entry = tk.Entry(self.settings_container, width=3)
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
        self.p1 = HumanPlayer(name1, "X")
        if not self.ai:
            name2 = self.p2_name.get()
            self.p2 = HumanPlayer(name2, "O")
        else:
            self.p2 = AIPlayer("O")

    def set_board_size(self):
        """retrieves board_size from entry"""
        self.board_size = int(self.b_size_entry.get())

    def set_game(self):
        """sets the game with given settings"""
        self.set_board_size()
        self.set_players()
        self.board = Board(self.board_size)
        self.game = Game(
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
ttt = TicTacToe()
ttt.mainloop()

# TODO: validate
# TODO: rounds
# TODO: handle excemptions, show em on wanring label
# TODO: cykle frames?
# TODO: change state instread of deleting shit
# TODO: not-scalable
# TODO: run without console
# TODO: make exe
# TODO: text size
# TODO: reset - play again window
# TODO: play again message
# TODO: GUI for menu, Gui for game
# TODO: AI
# TODO: makegui inherit from game
# TODO: exit button
# TODO: exit buttons - destroy window??? so it wont start new...
# TODO: add rounds
# TODO: not quit program, quit to menu
# TODO: add really quit???
# TODO: show totol winner
# TODO: add reset button
