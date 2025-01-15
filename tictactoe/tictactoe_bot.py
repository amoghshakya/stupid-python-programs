from models import Board, Player, Mark

"""
Implementing the Minimax algorithm for TicTacToe
- This algorithm tries to maximize the bot's chances of winning and minimize
the opponent's chances of winning. 
- We simulate all the possible moves and calculate a score for each move.
- The bot will choose the move with the highest score.
"""


class MinimaxBot(Player):
    name = 'Minimax Bot'

    def __init__(self, mark: Mark):
        self.mark = mark
        self.opponent = 'X' if mark == 'O' else 'O'

    def get_move(self, board: Board) -> tuple[int, int]:
        best_score = -float('inf')
        best_move = (-1, -1)

        for x in range(3):
            for y in range(3):
                if board.board[x][y] == ' ':
                    board.board[x][y] = self.mark
                    score = self.minimax(board, 0, False)

                    board.board[x][y] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move

    def minimax(self, board: Board, depth: int, is_maximizing: bool) -> float:
        winner = board.validate_board()

        if winner == self.mark:  # bot is winning
            return 10 - depth
        elif winner == self.opponent:  # opponent is winning
            return -10 + depth
        elif winner == '_':
            return 0

        if is_maximizing:
            best_score = -float('inf')

            for x in range(3):
                for y in range(3):
                    if board.board[x][y] == ' ':
                        board.board[x][y] = self.mark  # make the move
                        # pass False so that the next move (opponent) is minimizing
                        score = self.minimax(board, depth + 1, False)

                        # undo the move
                        board.board[x][y] = ' '
                        best_score = max(best_score, score)

            return best_score
        else:
            best_score = float('inf')

            for x in range(3):
                for y in range(3):
                    if board.board[x][y] == ' ':
                        # simulating the opponent
                        board.board[x][y] = self.opponent
                        # pass True so that next move (bot) is maximizing
                        score = self.minimax(board, depth + 1, True)

                        # undo the move
                        board.board[x][y] = ' '
                        best_score = min(best_score, score)

            return best_score
