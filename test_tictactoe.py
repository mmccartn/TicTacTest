#!/usr/bin/python

"""Applying basic python unit test practices to the tictactoe module

Reference material:
    [Ned Batchelder: Getting Started Testing - PyCon 2014]
        (https://youtu.be/FxSsnHeWQBY)

Sample Run:
    python-coverage run -m unittest -b test_tictactoe && python-coverage report -m

Sample Output:
    .....................
    ----------------------------------------------------------------------
    Ran 21 tests in 0.002s

    OK
    Name             Stmts   Miss  Cover   Missing
    ----------------------------------------------
    test_tictactoe     109      1    99%   218
    tictactoe          126      2    98%   9, 241
    ----------------------------------------------
    TOTAL              235      3    99%
"""

import unittest
import tictactoe
import mock


class TicTacToeTestCase(unittest.TestCase):
    """Base class for all TicTacToe tests"""

    # Invoked before each test method 
    def setUp(self):
        self.g = tictactoe.TicTacToe()
        self.empty_cell = tictactoe.TicTacToe.EMPTY_CELL


    def assertBoardsEqual(self, b1, b2):
        """assert that the board b1 is equal to board b2""" 
        self.assertEqual(b1, b2)


class GameTest(TicTacToeTestCase):

    def test_empty(self):
        e = self.empty_cell
        self.assertBoardsEqual(self.g.board, [[e, e, e], 
                                              [e, e, e], 
                                              [e, e, e]])

    
    def test_valid_move(self):
        e, x = self.empty_cell, 'x'
        self.g.move(x, 1, 1)
        self.assertBoardsEqual(self.g.board, [[e, e, e], 
                                              [e, x, e], 
                                              [e, e, e]])


    def test_invalid_player(self):
        with self.assertRaises(ValueError):
            self.g.move('a', 0, 0)
    

    def test_invalid_move(self):
        with self.assertRaises(IndexError):
            self.g.move('x', -1, -1)


    def test_occupied_cell(self):
        self.g.move('x', 0, 0)
        with self.assertRaises(RuntimeWarning):
            self.g.move('x', 0, 0)
        

    def test_has_invalid_player_won(self):
        with self.assertRaises(ValueError):
            self.g.has_player_won('a')


    def test_player_win_left_diag(self):
        self.g.move('x', 0, 0)
        self.g.move('x', 1, 1)
        self.g.move('x', 2, 2)
        self.assertEqual(self.g.get_state(), 'Player x has won.')


    def test_player_win_right_diag(self):
        self.g.move('x', 0, 2)
        self.g.move('x', 1, 1)
        self.g.move('x', 2, 0)
        self.assertEqual(self.g.get_state(), 'Player x has won.')


    def test_player_win_row(self):
        self.g.move('x', 0, 0)
        self.g.move('x', 0, 1)
        self.g.move('x', 0, 2)
        self.assertEqual(self.g.get_state(), 'Player x has won.')


    def test_player_win_col(self):
        self.g.move('x', 0, 0)
        self.g.move('x', 1, 0)
        self.g.move('x', 2, 0)
        self.assertEqual(self.g.get_state(), 'Player x has won.')


    def test_stalemate(self):
        x, o = 'x', 'o'
        self.g.move(x, 0, 0)
        self.g.move(o, 0, 1)
        self.g.move(x, 1, 1)
        self.g.move(o, 2, 2)
        self.g.move(x, 1, 0)
        self.g.move(o, 1, 2)
        self.g.move(x, 0, 2)
        self.g.move(o, 2, 0)
        self.g.move(x, 2, 1)
        self.assertEqual(self.g.get_state(), 'stalemate')


class TicTacToeOponentTestCase(unittest.TestCase):
    """Base class for all TicTacToe Oponent tests"""

    # Invoked before each test method 
    def setUp(self):
        self.marker = 'o'
        self.g = tictactoe.TicTacToe()
        e, x, o = tictactoe.TicTacToe.EMPTY_CELL, 'x', 'o'
        self.g.board = [[x, e, o], 
                        [e, e, e], 
                        [o, e, x]]
        self.opo = tictactoe.TicTacToeOponent(self.marker)


class TicTacToeOponentTestCase(TicTacToeOponentTestCase):
    
    def test_empty(self):
        self.assertEquals(self.opo.marker, self.marker)


    def test_row_col_subscripts(self):
        ss = self.opo.get_row_col_subscripts(self.g.board, 0, 0)
        self.assertEquals(ss, [(0, 0), (0, 1), (0, 2),  # col
                               (0, 0), (1, 0), (2, 0)]) # row


    def test_get_diagonal_subscripts(self):
        ss = self.opo.get_diagonal_subscripts(self.g.board)
        self.assertEquals(ss, [(0, 0), (1, 1), (2, 2),  # left
                               (0, 2), (1, 1), (2, 0)]) # right


    def test_score_subscript(self):
        score = self.opo.score_subscript(self.g.board, 1, 1)
        self.assertEquals(score, 6)


    def test_score_board(self):
        scored_board = self.opo.score_board(self.g.board)
        self.assertEquals(scored_board, [[-1, 3, -1], 
                                         [ 3, 6,  3], 
                                         [-1, 3, -1]])


    def test_best_move(self):
        (row, col) = self.opo.best_move(self.g.board)
        self.assertEquals((row, col), (1, 1))


    def test_bes_move_null_board(self):
        with self.assertRaises(ValueError):
            self.opo.best_move(None)


    def test_best_move_single_cell_board(self):
        self.assertEquals(self.opo.best_move(tictactoe.TicTacToe(1).board), 
                          (0, 0))


    def test_best_move_full_board(self):
        x, o = 'x', 'o'
        self.g.board = [[x, x, o], 
                        [o, o, x], 
                        [o, x, x]]
        with self.assertRaises(RuntimeWarning):
            print self.opo.best_move(self.g.board)


class TicTacToeInterfaceTest(unittest.TestCase):

    def test_next_move(self):

        # Create a mock randint method
        with mock.patch('random.randint') as randint:
            randint.return_value = 0

            moves = [1, 1,
                     1, 0,
                     1, 2]

            # Create a mock raw input method
            with mock.patch('__builtin__.raw_input', 
                            side_effect=moves) as raw_input:
                
                tti = tictactoe.TicTacToeInterface()
                
                # verify that fake randint is based off of the chosen range
                randint.assert_called_with(0, 1)

                self.assertEqual(tti.state, 'Player x has won.')


if __name__ == '__main__':
    pass