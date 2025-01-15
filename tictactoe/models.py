from typing import Literal, TypeAlias

Mark: TypeAlias = Literal['X', 'O']


class Player:
    def __init__(self, name: str, mark: Mark):
        self.name = name
        self.mark = mark


class Board:
    players: list[Player]
    current_player: Mark

    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = []

    def __str__(self) -> str:
        # pretty print the board

        rows = []
        for i, row in enumerate(self.board):
            # padding each value with spaces (for pretty reasons)
            row = [' ' + cell + ' ' for cell in row]
            rows.append(f'{i} ' + '|'.join(row))

        board_art = '   0   1   2\n\n' + ('\n  ---+---+---\n'.join(rows))

        return board_art

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == ' '

    def play(self, x: int, y: int) -> bool:
        if not self.is_valid_move(x, y):
            return False
        else:
            self.board[x][y] = self.current_player
            self.current_player = self.players[0].mark if self.current_player == self.players[1].mark else self.players[1].mark
            return True

    def add_players(self, player1: Player, player2: Player) -> None:
        self.players = [player1, player2]
        self.current_player = player1.mark

    def validate_board(self) -> Mark | Literal['_'] | None:
        winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],  # row 1
            [(1, 0), (1, 1), (1, 2)],  # row 2
            [(2, 0), (2, 1), (2, 2)],  # row 3
            [(0, 0), (1, 0), (2, 0)],  # col 1
            [(0, 1), (1, 1), (2, 1)],  # col 2
            [(0, 2), (1, 2), (2, 2)],  # col 3
            [(0, 0), (1, 1), (2, 2)],  # diagonal 1
            [(0, 2), (1, 1), (2, 0)]  # diagonal 2
        ]

        for combination in winning_combinations:
            marks = [self.board[x][y] for x, y in combination]

            if all(mark == 'X' for mark in marks):
                return 'X'
            elif all(mark == 'O' for mark in marks):
                return 'O'

        # check for draw
        if all(cell != ' ' for row in self.board for cell in row):
            return '_'

        return None

    def reset_board(self) -> None:
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
