import os
import sys

from models import Board, Player
from tictactoe_bot import MinimaxBot


def clear_screen() -> None:
    # clear the screen
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print()


def help() -> None:
    print('Tic Tac Toe Game')
    print('> How to play?')
    print(
        '> Enter the coordinates of the cell where you want to place your mark.')
    print(
        '> Coordinates are in the form xy where x is the row and y is the column.')
    print('> For example, to place your mark in the top right corner, enter 02.')
    print("> To exit the game, type 'exit'.")


def human_vs_human():
    clear_screen()

    board = Board()
    player1 = Player(name="Player 1", mark='X')
    player2 = Player(name="Player 2", mark='O')
    board.add_players(player1, player2)

    # using the walrus operator
    while (winner := board.validate_board()) is None:
        try:
            help()
            print(board)
            print(f'Current player: {board.current_player}')

            user_input = input('Enter coordinates (x, y) in the form xy: ')

            if user_input == 'exit':
                print('Exiting the game...')
                sys.exit(0)

            x, y = user_input
            clear_screen()

            move = board.play(int(x), int(y))

            if not move:
                raise ValueError

        except ValueError:
            clear_screen()
            print(board)
            print('Invalid move. Try again!')

    if winner == '_':
        print(board)
        print("It's a tie!")
        sys.exit(0)

    if winner is not None:
        print(board)
        print(f'Player {winner} wins!')
        sys.exit(0)


def play_vs_bot(bot_vs_bot=False):
    board = Board()

    player1 = Player(name="Human", mark='X')
    if bot_vs_bot:
        player1 = MinimaxBot(mark='X')
    bot = MinimaxBot(mark='O')

    board.add_players(player1, bot)

    while (winner := board.validate_board()) is None:
        clear_screen()
        help()
        print(board)

        if board.current_player == bot.mark:
            print(f"Bot's turn({bot.mark})...")
            x, y = bot.get_move(board)
            print(f"Bot chose: ({x}, {y})")
            board.play(x, y)
        else:
            print(f"Your turn({board.current_player})...")
            user_input = input("Enter coordinates (x, y) in the form xy: ")
            if user_input.lower() == 'exit':
                print('Exiting the game...')
                sys.exit(0)

            try:
                x, y = user_input
                move = board.play(int(x), int(y))
                if not move:
                    raise ValueError
            except ValueError as e:
                print("Invalid move. Try again!")
                continue

    print(board)
    if winner == '_':
        print("It's a tie!")
    else:
        print(f"{winner} wins!")


if __name__ == "__main__":
    print("Welcome to Tic Tac Toe!")
    print("Choose an option:")
    print("1. Human vs Human")
    print("2. Human vs Bot")
    game_mode = input("Enter your choice: ")

    if game_mode == '1':
        human_vs_human()
        play_again = input("Play again? (y/n): ")
        while play_again.lower() == 'y':
            human_vs_human()
            play_again = input("Play again? (y/n): ")
    elif game_mode == '2':
        play_vs_bot()
        play_again = input("Play again? (y/n): ")
        while play_again.lower() == 'y':
            play_vs_bot()
            play_again = input("Play again? (y/n): ")
