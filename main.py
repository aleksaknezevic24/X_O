from tkinter import *
import numpy as np
import copy
import random
size_of_board = 600
symbol_size = (size_of_board / 4 - size_of_board / 8) / 2
symbol_thickness = 30
symbol_X_color = '#EB4035'
symbol_O_color = '#0A92CF'
Green_color = '#7BC043'


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window,
                             width=size_of_board,
                             height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(4, 4))
        self.previous_step = (None, None)
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(3):
            self.canvas.create_line((i + 1) * size_of_board / 4, 0,
                                    (i + 1) * size_of_board / 4, size_of_board)

        for i in range(3):
            self.canvas.create_line(0, (i + 1) * size_of_board / 4,
                                    size_of_board, (i + 1) * size_of_board / 4)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(4, 4))
        self.tie = False
        self.X_wins = False
        self.O_wins = False

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)

        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size,
                                grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size,
                                grid_position[1] + symbol_size,
                                width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size,
                                grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size,
                                grid_position[1] + symbol_size,
                                width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size,
                                grid_position[1] - symbol_size,
                                width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2,
                                size_of_board / 3,
                                font="cmr 60 bold",
                                fill=color,
                                text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2,
                                5 * size_of_board / 8,
                                font="cmr 40 bold",
                                fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie            : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2,
                                3 * size_of_board / 4,
                                font="cmr 30 bold",
                                fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2,
                                15 * size_of_board / 16,
                                font="cmr 20 bold",
                                fill="gray",
                                text=score_text)


    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 4) * logical_position + size_of_board / 8

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 4), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def get_next_states(self, current_state, player):
        next_states = []

        for i in range(4):
            for j in range(4):
                if current_state[i][j] == 0:
                    next_state = copy.deepcopy(current_state)
                    next_state[i][j] = player
                    next_states.append((i, j, next_state))

        return next_states

    def Max(self, current_state, alpha, beta):
        state_value = self.evaluation(current_state)
        if state_value != None:
            return (state_value, None, None)

        v = float('-inf')
        (max_i, max_j) = (None, None)

        for (i, j, next_state) in self.get_next_states(current_state, 1):
            (value, min_i, min_j) = self.Min(next_state, alpha, beta)
            if value > v:
                v = value
                max_i = i
                max_j = j

            if v >= beta:
                return (v, i, j)

            if v > alpha:
                alpha = v


        return (v, max_i, max_j)

    def Min(self, current_state, alpha, beta):
        state_value = self.evaluation(current_state)
        if state_value != None:
            return (state_value, None, None)

        v = float('inf')
        (min_i, min_j) = (None, None)

        for (i, j, next_state) in self.get_next_states(current_state, 2):
            (value, max_i, max_j) = self.Max(next_state, alpha, beta)
            if value < v:
                v = value
                min_i = i
                min_j = j

            if v <= alpha:
                return (v, i, j)

            if v < beta:
                beta = v

        return (v, min_i, min_j)

    def evaluation(self, current_state):

        winner = None
        #print(current_state)
        # 4 in a row or column
        for i in range(4):
            if current_state[i][0] == current_state[i][1] == current_state[i][
                    2] == current_state[i][3] != 0:
                winner = current_state[i][0]
            if current_state[0][i] == current_state[1][i] == current_state[2][
                    i] == current_state[3][i] != 0:
                winner = current_state[0][i]

        # square
        for i in range(3):
            for j in range(3):
                if current_state[i][j] == current_state[
                        i + 1][j] == current_state[i][j + 1] == current_state[
                            i + 1][j + 1] != 0:
                    winner = current_state[i][j]

        # Diagonals
        if current_state[0][0] == current_state[1][1] == current_state[2][
                2] == current_state[3][3] != 0:
            winner = current_state[0][0]

        if current_state[0][3] == current_state[1][2] == current_state[2][
                1] == current_state[3][0] != 0:
            winner = current_state[0][3]

        if winner != None:
            if winner == 1:
                # Igrac 1 je pobedio
                return 1
            else:
                # Igrac 2 je pobedio
                return -1

        for i in range(4):
            for j in range(4):
                if current_state[i][j] == 0:
                    return None
        #nereseno
        return 0

    def is_gameover(self):
        state_value = self.evaluation(self.board_status)
        print(f'pobednik je: {state_value}')
        if state_value != None:
            if state_value == -1:
                self.X_wins = True
            elif state_value == 1:
                self.O_wins = True
            else:
                self.tie = True

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover

    def num_free_spaces(self):
        num_free_spaces = 0
        for i in range(4):
            for j in range(4):
                if self.board_status[i][j] == 0:
                    num_free_spaces += 1
        return num_free_spaces
    def get_random_space(self):
        get_field = False
        while not get_field:
            prev_i = self.previous_step[0]
            prev_j = self.previous_step[1]
            i = random.randint(prev_i-1, prev_i+1)
            j = random.randint(prev_j-1, prev_j+1)
            try:
                if self.board_status[i][j] == 0:
                    get_field = True
            except:
                pass
        return i, j

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if not self.is_grid_occupied(logical_position):
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][
                    logical_position[1]] = 2
                self.player_X_turns = not self.player_X_turns
                print(self.board_status.transpose())
                self.previous_step = (logical_position[0], logical_position[1])
                # Check if game is concluded
                if self.is_gameover():
                    self.display_gameover()
                    return

                free = self.num_free_spaces()
                if free < 12:
                    (v, field_i, field_j) = self.Max(self.board_status, -10, 10)

                else:
                    field_i, field_j = self.get_random_space()
                self.board_status[field_i][field_j] = 1
                self.draw_O((field_i, field_j))
                self.player_X_turns = not self.player_X_turns
                print(self.board_status.transpose())
                if self.is_gameover():
                    self.display_gameover()
                    return

        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False



game_instance = Tic_Tac_Toe()
game_instance.mainloop()
