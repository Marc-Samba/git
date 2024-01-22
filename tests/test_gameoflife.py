import pygame
import pytest
from gameoflife import GameOfLife
from gameoflife import Pygame
from gameoflife import read_args

def test_create_matrice_block_pattern(self):
        game = GameOfLife(input="block_pattern.txt", output="output.txt", d=False, m=20, f=10, width=3, height=3) #reducing the screen size to have a (3,3) matrix
        result = game._create_matrice()
        expected_result = [[1, 1, 0],
                           [1, 1, 0],
                           [0, 0, 0]]
        assert result==expected_result

def test_create_matrice_blinker_pattern(self):
        game = GameOfLife(input="blinker_pattern.txt", output="output.txt", d=False, m=20, f=10, width=4, height=3) #adjusting screen size
        result = game._create_matrice()
        expected_result = [[1, 1, 1, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]]
        assert result==expected_result

def test_create_matrice_glider_pattern(self):
        game = GameOfLife(input="glider_pattern.txt", output="output.txt", d=False, m=20, f=10, width=3, height=3) #adjusting screen size for the test
        result = game._create_matrice()
        expected_result = [[0, 1, 0],
                           [0, 0, 1],
                           [1, 1, 1]]
        assert result==expected_result

def test_count_neighbors(self):
        game = GameOfLife(input="test_input.txt", output="output.txt", d=False, m=20, f=10, width=800, height=600)
        # Modify the current state to run the test
        game._current_state = [[1, 0, 1],
                               [0, 1, 0],
                               [1, 0, 1]]
        result = game._count_neighbors(game._current_state,1, 1)
        assert result==4

def test_simulation_with(self):
    # Set up an initial state
    initial_state_content = [[1, 0, 1],
                             [0, 1, 0],
                             [1, 0, 1]]

    # Set up expected output after 3 steps
    expected_output_state = [[0,1,0],
                             [1,1,0],
                             [0,0,1]]

    # Create a GameOfLife instance 
    game = GameOfLife(input=initial_state_content, output=None, d=False, m=3, f=10, width=3, height=3)

    # Run the simulation
    game.run()

    # check that the output state matches the expected output state
    assert expected_output_state == game._current_state

