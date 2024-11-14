# MinimaxChessAgent
Implemented an AI chess agent that uses the Minimax algorithm to optimize move strategy.

## Code Structure
### `MinimaxAgent.py`
`MinimaxAgent.py` is a subclass of the class `ChessAgent`. The MinimaxAgent the minimax algorithm with alpha-beta pruning to choose what move to make. It has multiple supporting functions:
 1. `evaluate( )` returns the value of a given board state based on factors like the number of each piece type for each player, position of king, whether the board is a checkmate, whether that position has been visited before. It also encourages the MinimaxAgent to go towards the other side of the board by adding value when pieces are in the center rows.
 2. `minimax( )` recursively performs the minimax algorithm and returns the best_move for the specified agent (minimizing or maximizing).
 3. `choose_action( )` runs the the minimax function from the current board state and returns the best move for the MinimaxAgent.
### `evaluation.py`
This is based on ChessMatch.py to follow the evaluation metrics required for the assignment.
## Running the program
You can run the program with `python3 main.py MinimaxAgent RandomPlayer` to run `evaluation.py`, which will print the results for all 100 matches as they occur and will print the win rate and average decision time after the 100 matches are completed. 
## Dependencies
I used the `random` library in `MinimaxAgent.py` to generate caches for the board states to address an issue where the MinimaxAgent was repeating an action incessantly. 
You can install it using `pip install random`, though it's usually built-in. 
