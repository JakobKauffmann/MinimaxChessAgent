# /* MinimaxAgent.py

from typing import Literal
from data.classes.Square import Square
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent
from data.classes.pieces.King import King
import random

zobrist_table = {
    (piece_notation, square, player): random.randint(1, 2**64-1)
    for piece_notation in ['P', 'K','B','R','N','Q']
    for square in [(x,y) for x in range(8) for y in range(8)]
    for player in ['black','white']
}

def zobrist_hash(board: Board):
    board_hash = 0
    squares = board.squares
    for square in squares:
        piece = square.occupying_piece
        if piece is not None:
            piece_notation = square.occupying_piece.notation
            piece_owner = piece.color
            piece_position = square.pos
            board_hash ^= zobrist_table[(piece_notation, piece_position, piece_owner)]
    return board_hash

class MinimaxAgent(ChessAgent):
    # Create private variables for Agent
    def __init__(self, color: Literal['white', 'black']):
        # In child classes, feel free to initialize any other state
        # or helper functions
        self.color = color
        self.depth = 2
        self.agentHistory = []
        self.opponentHistory = []

    def evaluate(self, board:Board, agentHistory, is_maximizing_player):
        value = 0

        if board.is_in_checkmate(self.color):
            return -1000
        if board.is_in_checkmate('white' if self.color == 'black' else 'black'):
            value += 1000
        board_hash = zobrist_hash(board)

        if is_maximizing_player:
            if agentHistory.count(board_hash) >= 2:
                value -= 100
        else:
            if agentHistory.count(board_hash) >= 2:
                value -= 100


        # Piece values (basic material evaluation)
        piece_values = {
            'P': 1,
            'N': 3,
            'B': 3,
            'R': 5,
            'Q': 9,
            'K': 0
        }

        center_squares = []#[(3, 3), (3, 4), (4, 3), (4, 4)]
        for x in range(2,7):
            for y in range(1,7):
                coord = (x,y)
                center_squares.append(coord)

        corner_squares = [(0,0),(0,7),(7,0),(7,7)]

        for square in board.squares:
            piece = square.occupying_piece
            if piece is not None:
                piece_notation = piece.notation
                piece_pos = square.pos
                piece_owner = 'agent' if is_maximizing_player else 'opponent'

                if piece_owner == 'player':
                    value += piece_values[piece_notation]
                else:
                    value -= 1.5 * piece_values[piece_notation]

                if piece_notation == 'K':
                    if piece_owner == 'agent':
                        agentKing = King(piece_pos, piece.color, board)
                        if agentKing.can_castle(board):
                            value += 1
                        if piece_pos in corner_squares:
                            value += 1
                    else:
                        opponentKing = King(piece_pos, piece.color, board)
                        if opponentKing.can_castle(board):
                            value -=1
                        if piece_pos in corner_squares:
                            value -=1
        return value

    def minimax(self, board:Board, depth, alpha, beta, is_maximizing_player):
        # Base case: check if the game is over or if depth is 0
        if depth == 0 or board.is_in_checkmate('white') or board.is_in_checkmate('black'):
            return self.evaluate(board, self.agentHistory, is_maximizing_player), None
       # Get zobrist hash for current board state
        board_hash = zobrist_hash(board)
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if is_maximizing_player:
            max_eval = -float('inf')
            # Track only agent's history
            self.agentHistory.append(board_hash)
            possible_moves = board.get_all_possible_moves(self.color)
            best_move = None
            for move in possible_moves:
                new_board = Board.without_display(config=board.get_config(),turn=board.turn)
                if new_board.handle_move(new_board.get_square_from_pos(move[0]), new_board.get_square_from_pos(move[1])):
                    eval, this_move = self.minimax(new_board, depth - 1, alpha, beta, False)
                    if move[1] in center_squares:
                        eval += 0.5
                    else:
                        eval -= 0.5
                    if eval >= max_eval:
                        max_eval = eval
                        best_move = move
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            self.agentHistory.pop()
            return max_eval, best_move
        else:
            min_eval = float('inf')
            self.opponentHistory.append(board_hash)
            possible_moves = board.get_all_possible_moves("black" if self.color == "white" else "white")
            best_move = None  # Track the best move explicitly
            for move in possible_moves:
                new_board = Board.without_display(config=board.get_config(),turn=board.turn)
                if new_board.handle_move(new_board.get_square_from_pos(move[0]), new_board.get_square_from_pos(move[1])):
                    eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                    if move[1] in center_squares:
                        eval -= 0.5
                    else:
                        eval += 0.5

                    if eval <= min_eval:
                        min_eval = eval
                        best_move = move

                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            self.opponentHistory.pop()
            return min_eval, best_move

    def choose_action(self, board: Board) -> tuple[Square, Square] | bool:
        _, action = self.minimax(board, self.depth, -float('inf'), float('inf'),True)
        if action is not None:
            return (board.get_square_from_pos(action[0]),board.get_square_from_pos(action[1]))
        else:
            return False
