# write your code here
import random

TOTAL_CELLS_NUM = 9


class UserTicTacToe:

    def __init__(self, mark):
        self.mark = mark

    def move(self, board):
        while True:
            cords = input("Enter the coordinates: > ")
            try:
                cords = cords.replace(' ', '')
                cord1, cord2 = list(cords)
                cord1, cord2 = int(cord1), int(cord2)
            except ValueError:
                print("You should enter numbers!")
            else:
                # check if cords type is int and they lay between 1 - 3
                if 1 <= cord1 <= 3 and 1 <= cord2 <= 3:

                    # if cell in board is not empty
                    if board[(cord1, cord2)] != ' ':
                        print("This cell is occupied! Choose another one!")
                    else:
                        board[(cord1, cord2)] = self.mark
                        break
                else:
                    print("Coordinates should be from 1 to 3!")


class AITicTacToe:

    def __init__(self, mark, level='easy'):
        self.mark = mark
        self.level = level

    def _easy_level(self, board):

        cords = [cord for cord in board.keys()]
        while True:
            step_index = random.randint(0, len(cords) - 1)
            step_cord = cords[step_index]
            if board[step_cord] not in ('X', 'O'):
                board[step_cord] = self.mark
                break

    def _medium_level(self, board):

        pattern_list = [
            [(1, 1), (1, 2), (1, 3)], [(2, 1), (2, 2), (2, 3)], [(3, 1), (3, 2), (3, 3)],
            [(1, 1), (2, 1), (3, 1)], [(1, 2), (2, 2), (3, 2)], [(1, 3), (2, 3), (3, 3)],
            [(1, 1), (2, 2), (3, 3)], [(1, 3), (2, 2), (3, 1)]
        ]

        enemy_mark = 'X' if self.mark == 'O' else 'O'

        for _ in range(2):
            check = 'O' if enemy_mark == 'X' else 'X'

            for pattern in pattern_list:
                if (board[pattern[0]], board[pattern[1]], board[pattern[2]]) == (
                        " ", check, check):
                    board[pattern[0]] = self.mark
                    return
                elif (board[pattern[0]], board[pattern[1]], board[pattern[2]]) == (
                        check, " ", check):
                    board[pattern[1]] = self.mark
                    return
                elif (board[pattern[0]], board[pattern[1]], board[pattern[2]]) == (
                        check, check, " "):
                    board[pattern[2]] = self.mark
                    return

            enemy_mark = 'O' if enemy_mark == 'X' else 'X'
        self._easy_level(board)

    @staticmethod
    def is_win(board, player) -> bool:
        for i in range(1, 4):
            if board[(i, 1)] == board[(i, 2)] and board[(i, 2)] == board[(i, 3)] and \
                    board[(i, 3)] == player:
                return True

        for i in range(1, 4):
            if board[(1, i)] == board[(2, i)] and board[(2, i)] == board[(3, i)] and \
                    board[(3, i)] == player:
                return True

        return (board[(1, 1)] == board[(2, 2)] and board[(2, 2)] == board[(3, 3)] and
                board[(3, 3)] == player) or (board[(3, 1)] == board[(2, 2)] and
                                             board[(2, 2)] == board[(1, 3)] and board[
                                                 (1, 3)] == player)

    def get_game_state(self, board):

        empty_cells = [cell for cell in board if board[cell] == ' ']

        if self.is_win(board, 'X'):
            return 'X'
        if self.is_win(board, 'O'):
            return 'O'
        if empty_cells:
            return 'N_F'
        return 'DRAW'

    def _minimax(self, board, player, is_maximize, start_player, depth):

        game_state = self.get_game_state(board)

        if game_state == 'X':
            return 10 - depth if start_player == 'X' else depth - 10
        elif game_state == 'O':
            return 10 - depth if start_player == 'O' else depth - 10
        elif game_state == 'DRAW':
            return 0

        best_score = -999 if is_maximize else 999

        for i in range(1, 4):
            for j in range(1, 4):
                if board[(i, j)] == ' ':
                    board[(i, j)] = player
                    score = self._minimax(
                        board, TitTacToe.get_opponent(player), not is_maximize, start_player, depth + 1
                    )
                    board[(i, j)] = ' '
                    best_score = max(best_score, score) if is_maximize else min(best_score, score)

        return best_score

    def _get_move(self, board, player):
        best_score = -999
        best_position = None

        empty_cells = [cell for cell in board if board[cell] == ' ']

        if empty_cells == TOTAL_CELLS_NUM:
            return 2, 2

        for i in range(1, 4):
            for j in range(1, 4):
                if board[(i, j)] == ' ':
                    board[(i, j)] = player
                    score = self._minimax(board, TitTacToe.get_opponent(player), False, player, 1)
                    board[(i, j)] = ' '
                    if score > best_score:
                        best_score = score
                        best_position = (i, j)

        return best_position

    def _hard_level(self, board):
        ai_move = self._get_move(board, self.mark)
        board[ai_move] = self.mark

    def move(self, board):
        print(f"Making move level \"{self.level}\"")
        if self.level == 'easy':
            self._easy_level(board)

        # medium level
        elif self.level == 'medium':
            self._medium_level(board)
        # hard level
        elif self.level == 'hard':
            self._hard_level(board)


class TitTacToe:
    """TitTacToe interface"""

    def __init__(self):
        self.board = {
            (1, 1): ' ', (1, 2): ' ', (1, 3): ' ',
            (2, 1): ' ', (2, 2): ' ', (2, 3): ' ',
            (3, 1): ' ', (3, 2): ' ', (3, 3): ' '
        }
        self.O_count = 0
        self.X_count = 0

    @classmethod
    def get_opponent(cls, player):
        return 'X' if player == 'O' else 'O'

    @classmethod
    def clear_cells(cls):
        return cls()

    def is_win(self, player) -> bool:
        for i in range(3):
            if self.board[(i, 0)] == self.board[(i, 1)] and self.board[(i, 1)] == self.board[(i, 2)] and \
                    self.board[(i, 2)] == player:
                return True

        for i in range(3):
            if self.board[(0, i)] == self.board[(1, i)] and self.board[(1, i)] == self.board[(2, i)] and \
                    self.board[(2, i)] == player:
                return True

        return (self.board[(0, 0)] == self.board[(1, 1)] and self.board[(1, 1)] == self.board[(2, 2)] and
                self.board[(2, 2)] == player) or (self.board[(2, 0)] == self.board[(1, 1)] and
                                                  self.board[(1, 1)] == self.board[(0, 2)] and self.board[
                                                      (0, 2)] == player)

    def get_game_state(self):

        empty_cells = [cell for cell in self.board if self.board[cell] == ' ']

        if self.is_win('X'):
            return 'X'
        if self.is_win('O'):
            return 'O'
        if empty_cells:
            return 'N_F'
        return 'DRAW'

    def out_board(self):
        print("---------")
        print(f"| {self.board[(1, 1)]} {self.board[(1, 2)]} {self.board[(1, 3)]} |")
        print(f"| {self.board[(2, 1)]} {self.board[(2, 2)]} {self.board[(2, 3)]} |")
        print(f"| {self.board[(3, 1)]} {self.board[(3, 2)]} {self.board[(3, 3)]} |")
        print("---------")

    def start_view(self):
        cells = list(input("Enter the cells: > "))
        for cord, cell in zip(self.board.keys(), cells):
            if cell in ('X', 'O'):
                self.board[cord] = cell
                if cell == 'X':
                    self.X_count += 1
                else:
                    self.O_count += 1

    def is_finished(self):
        win_str = "{} wins"
        num_filled_cells = len([val for val in self.board.values() if val != ' '])
        if self.board[(1, 1)] == self.board[(1, 2)] == self.board[(1, 3)] != ' ':
            mark = self.board[(1, 1)]
            print(win_str.format(mark))
        elif self.board[(2, 1)] == self.board[(2, 2)] == self.board[(2, 3)] != ' ':
            mark = self.board[(2, 1)]
            print(win_str.format(mark))
        elif self.board[(3, 1)] == self.board[(3, 2)] == self.board[(3, 3)] != ' ':
            mark = self.board[(3, 1)]
            print(win_str.format(mark))
        elif self.board[(1, 1)] == self.board[(2, 1)] == self.board[(3, 1)] != ' ':
            mark = self.board[(1, 1)]
            print(win_str.format(mark))
        elif self.board[(1, 2)] == self.board[(2, 2)] == self.board[(3, 2)] != ' ':
            mark = self.board[(1, 2)]
            print(win_str.format(mark))
        elif self.board[(1, 3)] == self.board[(2, 3)] == self.board[(3, 3)] != ' ':
            mark = self.board[(1, 3)]
            print(win_str.format(mark))
        elif self.board[(1, 1)] == self.board[(2, 2)] == self.board[(3, 3)] != ' ':
            mark = self.board[(1, 1)]
            print(win_str.format(mark))
        elif self.board[(1, 3)] == self.board[(2, 2)] == self.board[(3, 1)] != ' ':
            mark = self.board[(1, 3)]
            print(win_str.format(mark))

        # Draw and Game not finished
        else:
            if num_filled_cells == TOTAL_CELLS_NUM:
                print("Draw")
                return True
            # Game not finished yet
            else:
                return False

        return True


def menu():
    marks = {0: 'X', 1: 'O'}
    players = {'X': None, 'O': None}

    while True:
        commands = input("Input command: > ")
        if commands == 'exit':
            exit()
        try:
            commands = commands.split(' ')
            if len(commands) < 3:
                raise ValueError
        except ValueError:
            print("Bad parameters!")
        else:
            break

    for i, command in enumerate(commands[1:]):
        if command != 'user':
            players[marks[i]] = AITicTacToe(mark=marks[i], level=command)
        else:
            players[marks[i]] = UserTicTacToe(mark=marks[i])

    return players


def run():
    board = TitTacToe()

    while True:
        players = menu()
        x_player, o_player = players['X'], players['O']

        board.out_board()
        while True:
            x_player.move(board.board)
            board.out_board()

            if board.is_finished():
                break

            o_player.move(board.board)
            board.out_board()

            if board.is_finished():
                break

        board = board.clear_cells()


if __name__ == '__main__':
    run()
