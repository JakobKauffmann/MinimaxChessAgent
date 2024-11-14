import pygame
import time
import statistics
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent


def count_pieces(board: Board, player: str):
    """Counts the number of pieces left on the board for the given player."""
    piece_count = 0
    for square in board.squares:
        piece = square.occupying_piece
        if piece and piece.color == player:
            piece_count += 1
    return piece_count


def evaluate_draw(board: Board, trial_num):
    """Evaluates the board to determine the draw based on piece count."""
    white_pieces = count_pieces(board, 'white')
    black_pieces = count_pieces(board, 'black')

    if white_pieces > black_pieces:
        print(f"White wins in trial {trial_num}!")
        return 'draw(white)'  # White has more pieces
    elif black_pieces > white_pieces:
        print(f"Black wins in trial {trial_num}!")
        return 'draw(black)'  # Black has more pieces
    else:
        return 'draw'

def eval_match(white_player: ChessAgent, black_player: ChessAgent, trial_num: int = 1):
    assert (white_player.color == 'white')
    assert (black_player.color == 'black')
    pygame.init()
    WINDOW_SIZE = (600, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    board = Board(screen, WINDOW_SIZE[0], WINDOW_SIZE[1])
    agents: list[ChessAgent] = [white_player, black_player]
    i: int = 0
    moves_count: int = 0

    # Run the main game loop
    running = True
    while running:
        if moves_count > 1000:
            # Draw after 1000 moves, evaluate based on number of pieces
            print(f'Too many moves. Evaluating draw in trial {trial_num}...')
            return evaluate_draw(board, trial_num)

        if agents[i] == white_player:  # Check if MinimaxAgent is moving
            start_time = time.time()
            chosen_action = agents[i].choose_action(board)
            decision_time = time.time() - start_time  # Time taken for MinimaxAgent to decide
            decision_times.append(decision_time)  # Collect decision time
        else:
            chosen_action = agents[i].choose_action(board)  # Random player move

        # Ensure no draw if one player has no pieces left
        if count_pieces(board, 'white') == 0:
            print(f'Black wins in trial {trial_num}!')
            return 'black'
        elif count_pieces(board, 'black') == 0:
            print(f'White wins in trial {trial_num}!')
            return 'white'

        if chosen_action == False:
            # Differentiate between a valid draw and a forced win condition
            if count_pieces(board, 'white') == 0:
                print(f'Black wins in trial {trial_num}!')
                return 'black'
            elif count_pieces(board, 'black') == 0:
                print(f'White wins in trial {trial_num}!')
                return 'white'
            else:
                print(f'Players draw by False action in trial {trial_num}.')
                return 'draw'

        i = (i + 1) % len(agents)
        moves_count += 1

        if not board.handle_move(*chosen_action):
            print("Invalid move!")
        elif board.is_in_checkmate(board.turn):
            if board.turn == 'white':
                print(f'Black wins in trial {trial_num}!')
                return 'black'
            else:
                print(f'White wins in trial {trial_num}!')
                return 'white'
        board.draw()


def run_trials(num_trials: int, white_player, black_player):
    white_wins = 0
    black_wins = 0
    draws = 0
    global decision_times  # List to store all decision times for MinimaxAgent
    decision_times = []

    for trial in range(num_trials):
        result = eval_match(white_player, black_player, trial_num=trial + 1)
        if result == 'white' or 'draw(white)':
            white_wins += 1
        elif result == 'black' or 'draw(black)':
            black_wins += 1
        elif 'draw' in result:
            draws += 1

    # Calculate win rate for MinimaxAgent
    win_rate = white_wins / num_trials * 100

    # Calculate average decision time for MinimaxAgent
    avg_decision_time = statistics.mean(decision_times) if decision_times else 0
    decision_time_stddev = statistics.stdev(decision_times) if len(decision_times) > 1 else 0

    # Output results
    print(f"Win Rate of MinimaxAgent (White): {win_rate}%")
    print(f"Black wins: {black_wins}")
    print(f"Draws: {draws}")
    print(f"Average Decision Time for MinimaxAgent: {avg_decision_time:.4f} seconds")
    print(f"Standard Deviation of Decision Time: {decision_time_stddev:.4f} seconds")