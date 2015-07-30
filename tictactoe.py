#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import operator

def main(args):
    TicTacToeInterface()


class TicTacToe(object):
    """A simple Tic Tac Toe game"""

    EMPTY_CELL = ' '
    PlAYER_MARKERS = ['x', 'o']

    def __init__(self, size=3):
        # size is the row and column size of the board
        self.size = size
        # board is a list of lists containing all of the playable cells
        # initialized to a size-by-size table of empty_markers
        self.board = []
        for i in range(self.size):
            self.board.append([TicTacToe.EMPTY_CELL for j in range(self.size)])
        # total moves keeps track of the number of valid moves made
        # cannot exceed size*size
        # makes checking for a stalemate easier
        self.total_moves = 0


    def move(self, player, row, col):
        """Modify the board to reflect players desire to place it's marker on 
           the board at location at row row, and column col
        """
        if not self.is_player_valid(player):
            raise ValueError
        elif not self.is_subscript_valid(row, col):
            raise IndexError
        elif self.board[row][col] != TicTacToe.EMPTY_CELL:
            raise RuntimeWarning
        else:
            self.board[row][col] = str(player).lower()
            self.total_moves += 1


    def is_player_valid(self, player):
        """Is player a valid player marker"""
        if str(player).lower() in TicTacToe.PlAYER_MARKERS:
            return True 
        else:
            return False


    def is_subscript_valid(self, row, col):
        """Are row and col subscripts within the bounds of the board?"""
        return row in range(self.size) and col in range(self.size)


    def has_player_won(self, player):
        """Has the player denoted by the player marker, won the game?"""
        if not self.is_player_valid(player):
            raise ValueError
        
        won_case = [player for i in range(self.size)]

        # check rows
        for i in range(self.size):
            if won_case == [self.board[i][j] for j in range(self.size)]:
                return True

        # check columns
        for j in range(self.size):
            if won_case == [self.board[i][j] for i in range(self.size)]:
                return True

        # check top left diagonal
        if won_case == [self.board[i][i] for i in range(self.size)]:
            return True

        # check top right diagonal
        if won_case == [self.board[i][2-i] for i in range(self.size)]:
            return True

        return False


    def get_state(self):
        """What is the current state of the game?
           ['Player _ has won', 'stalemate', 'ongoing']
        """
        for player in TicTacToe.PlAYER_MARKERS:
            if self.has_player_won(player):
                return 'Player {0} has won.'.format(player)
            
        if self.total_moves == (self.size * self.size):
            return 'stalemate'
        else:
            return 'ongoing'


    def __str__(self):
        """String representation of the game board"""        
        s = []
        s.append(''.join(['_' for i in range(1 + (2 * self.size))]))
        s.append('\n')
        for i in range(self.size):
            s.append('|')
            s.append(','.join([self.board[i][j] for j in range(self.size)]))
            s.append('|\n')
        s.append(''.join(['¯' for i in range(1 + (2 * self.size))]))
        return ''.join(s)


class TicTacToeOponent(object):
    """A simple tictactoe opponent 
    """

    def __init__(self, marker='o'):
        # marker is the symbol used to represent this players cells on the board
        self.marker = marker


    def best_move(self, board):
        """Chooses the best cell to play next by searching for the cell having 
        firstly: most self markers in it's neighboring cells
        secondly: the most non-empty markers in it's neighboring cells

        returns a tuple (row, col)
        """
        if not board:
            raise(ValueError)
        elif len(board) == 1:
            return (0, 0)

        options = dict()
        scored_board = self.score_board(board)
        for i in range(len(board)):
            for j in range(len(board)):
                options[(i, j)] = scored_board[i][j]

        best = sorted(options.items(), key=operator.itemgetter(1), 
                      reverse=True)[0]
        if best[1] == -1:
            # the board is filled up; there are no other cells left to play
            raise(RuntimeWarning)
        else:
            return best[0]


    def score_board(self, board):
        """Score the board in a separate table
        cells containing a non-empty marker are given a score of -1
        all other cells are scored according to the score_subscript method
        """
        size = len(board)
        scored_board = [[-1 for i in range(size)] for j in range(size)]
        for i in range(size):
            for j in range(size):
                if board[i][j] == TicTacToe.EMPTY_CELL:
                    scored_board[i][j] = self.score_subscript(board, i, j)
        return scored_board


    def score_subscript(self, board, row, col):
        """score a cell subscript offensively by countung the number of self 
        markers along the row, column, or diagonals of the (row, col) cell
        """
        subscripts = self.get_row_col_subscripts(board, row, col)

        diag_subscripts = self.get_diagonal_subscripts(board)
        subscripts += diag_subscripts if (row, col) in diag_subscripts else []

        score = 0
        for ss in subscripts:
            score += 1 if board[ss[0]][ss[1]] == self.marker else 0
            score += 1 if board[ss[0]][ss[1]] != TicTacToe.EMPTY_CELL else 0

        return score


    def get_diagonal_subscripts(self, board):
        """returns a list of (row, column) subscripts for both the left and 
        right board diagonal cells
        """
        size_range = range(len(board))
        return (zip(size_range, size_range) + 
                zip(size_range, size_range[::-1]))


    def get_row_col_subscripts(self, board, row, col):
        """returns a list of (row, column) subscripts for all cells in row row,
        and column col
        """
        size_range = range(len(board))
        row_subscripts = zip([row for i in size_range], size_range)
        col_subscripts = zip(size_range, [col for i in size_range])
        return row_subscripts + col_subscripts


class TicTacToeInterface(object):
    """A simple Tic Tac Toe player interface"""

    def __init__(self):
        # game is the tictactoe game instance, containing the playing board
        # state represents weather the game is ongoing, has been won, or is in 
        # stalemate
        self.game = TicTacToe()
        self.state = self.game.get_state()
        self.opponent = TicTacToeOponent('o')
        self.next_move(random.randint(0, 1))


    def next_move(self, cur_player_idx):
        """Main game loop that terminates on stalemate or when a player has won
        """        
        print str(self.game)
        
        self.state = self.game.get_state()
        if self.state != 'ongoing':
            print self.state
        else:
            cur_player_mkr = TicTacToe.PlAYER_MARKERS[cur_player_idx]
            print 'Player {0}\'s turn.'.format(cur_player_mkr)

            if cur_player_mkr != self.opponent.marker:
                row, col = int(raw_input('Row: ')), int(raw_input('Column: '))
            else:
                row, col = self.opponent.best_move(self.game.board)

            self.game.move(cur_player_mkr, row, col)

            if cur_player_idx < len(TicTacToe.PlAYER_MARKERS) - 1:
                cur_player_idx += 1
            else:
                 cur_player_idx = 0
            self.next_move(cur_player_idx)


if __name__ == '__main__':
    sys.exit(main(sys.argv))