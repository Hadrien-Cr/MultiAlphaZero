import pytest
import numpy as np
from alphazero.envs.connect4d.connect4d import Game, NUM_BOARDS  
'''
Run this test: 
python3 -m alphazero.envs.connect4d.test_connect4d
'''

# Helper function for initializing the board with a series of moves
def init_board_from_moves(moves):
    game = Game()
    for move in moves:
        game.play_action(move)
    return game

# Helper function for initializing the board from a given 2D array
def init_board_from_array(board_array):
    game = Game()
    game._board.pieces = np.array([board_array for _ in range(NUM_BOARDS)], dtype=np.intc)
    return game

# Test 1: Simple dynamics check
def test_simple_moves():
    game = init_board_from_moves([4] * NUM_BOARDS +  [5] * NUM_BOARDS + [4] * NUM_BOARDS +  [3] * NUM_BOARDS + [0] * NUM_BOARDS + [6] * NUM_BOARDS)
    expected = np.array([ 
        [[0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, -1, 1, -1, -1]]
            for _ in range(NUM_BOARDS)])
    assert np.array_equal(game._board.pieces , expected)

# Test 2: Overfilling a column and catching an error
def test_overfull_column():
    game = Game()
    column = 3
    for _ in range(game._board.height*NUM_BOARDS):  # Fill the column
        game.play_action(column)
    with pytest.raises(ValueError):
        game.play_action(column)  # Should raise error when overfilled

# Test 3: Valid moves
def test_get_valid_moves():
    column = 3
    game = game = init_board_from_moves([column] * NUM_BOARDS * 6)
    valid_moves = game.valid_moves()
    expected_valid_moves = np.array([True, True, True, False, True, True, True])
    assert np.array_equal(valid_moves, expected_valid_moves)

# Test 4: Symmetries of the board
def test_symmetries():
    game = init_board_from_moves([4] * NUM_BOARDS +  [5] * NUM_BOARDS + [4] * NUM_BOARDS +  [3] * NUM_BOARDS + [0] * NUM_BOARDS + [6] * NUM_BOARDS)
    pi = np.array([0.1, 0.2, 0.3, 0.4, 0.1, 0.1, 0.7])

    symmetries = game.symmetries(pi)
    assert len(symmetries) == 2  # Should have two symmetries

    flipped_board = game._board.pieces[:, :, ::-1]
    assert np.array_equal(flipped_board, symmetries[1][0]._board.pieces)

# Test 5: Game end detection
def test_game_ended():
    game = init_board_from_array([
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ])
    assert np.array_equal(game.win_state(), np.array([True, False, False])) # Player 1 wins with a diagonal
    
    game = init_board_from_moves([])
    assert np.array_equal(game.win_state(), np.array([False, False, False]))  # Initial state is not a game ended

# Test 6: Immutable move check
def test_immutable_move():
    game = init_board_from_moves([])
    clone_game = game.clone()
    game.play_action(5)
    assert np.array_equal(clone_game._board, game._board.pieces) == False  # Board should have changed

# Test 7: Random Rollout
def test_rollout():
    game = init_board_from_moves([])
    while np.array_equal(game.win_state(), np.array([False, False, False])):
        valid_actions = game.valid_moves()
        true_indices = np.where(valid_actions)[0]
        action = np.random.choice(true_indices).item()
        game.play_action(action)
        
if __name__ == "__main__":
    pytest.main()
