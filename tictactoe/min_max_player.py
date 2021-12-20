from typing import Any

from tictactoe import board
from tictactoe.board import Board
from tictactoe.player import Player
import copy


class MinMaxPlayer(Player):


    def __init__(self, name, mark):
        Player.__init__(self, name, mark)
        #self.diction = {}
        # counter to measure the improvement, the less times the methods min_max and max_min are called the faster
        self.counter = 0
        self.max_depth = 2

    def do_move(self, board):
        return self.calculate_next_move(board, self.mark)

    def calculate_next_move(self, current_board, mark):

        # for every possible move, add a pair of a min_max score and the move to a list scores.
        score_move_pairs = []
        for next_move in current_board.get_possible_moves():
            next_score = self.min_max(current_board, next_move, self.mark, 1)
            score_move_pairs.append((next_score, next_move))
        # if there is no score/move pair, return 0

        if not score_move_pairs:
            return 0
        # otherwise
        else:
            # compute the max score/move
            highest_score, best_move = max(score_move_pairs)
            # return the move
            return best_move

    def min_max(self, current_board, move, mark, depth):
        next_board = copy.deepcopy(current_board)
        next_board.place_move(move, mark)
        #if tuple(next_board.board) in self.diction:
        #    return self.diction[tuple(next_board.board)]
        if next_board.check_win([mark]):
            return 10
        elif next_board.board_full():
            return 0

        self.counter += 1

        scores = []

        if depth > self.max_depth:
            return self.heuristics(next_board, self.mark)

        for next_move in next_board.get_possible_moves():
            next_score = self.max_min(next_board, next_move, self.other_mark(mark), depth + 1)
            scores.append(int(next_score))
        if not scores:
            return 0
        else:
            lowest_score = min(scores)
            #self.diction[tuple(next_board.board)] = lowest_score
            return lowest_score

    def max_min(self, current_board, move, mark, depth):
        next_board = copy.deepcopy(current_board)
        next_board.place_move(move, mark)
        #if tuple(next_board.board) in self.diction:
        #    return self.diction[tuple(next_board.board)]
        if next_board.check_win([mark]):
            return -10
        elif next_board.board_full():
            return 0

        self.counter += 1

        scores = []
        print(scores)
        if depth > self.max_depth:
            return self.heuristics(next_board, self.mark)

        for next_move in next_board.get_possible_moves():
            next_score = self.min_max(next_board, next_move, self.other_mark(mark), depth + 1)
            scores.append(int(next_score))

        if not scores:
            return 0
        else:
            highest_score = max(scores)
            #self.diction[tuple(next_board.board)] = highest_score
            return highest_score

    def heuristics(self, bro, mark):
        # calculate heuristic score for rows
        h_scores = []
        for i in [0, 3, 6]:
            x1 = 0
            x2 = 0
            o1 = 0
            o2 = 0
            row_square = [i, i + 1, i + 2]
            count = 0
            for square in row_square:
                if bro.board[square] == self.mark:
                    count += 1
                if bro.board[square] == self.other_mark(mark):
                    count = 0
            if count == 1:
                x1 = 1
            elif count == 2:
                x1 = 1
                x2 = 1
            count = 0

            for square in row_square:
                if bro.board[square] == self.other_mark(mark):
                    count += 1
                if bro.board[square] == mark:
                    count = 0
            if count == 1:
                o1 = 1
            elif count == 2:
                o1 = 1
                o2 = 1

            h_score = (3 * x2 + x1) - (3 * o2 + o1)
            h_scores.append(h_score)

        # calculate heuristic score for columns
        for i in [0, 1, 2]:
            x1 = 0
            x2 = 0
            o1 = 0
            o2 = 0
            column_square = [i, i + 3, i + 6]
            count = 0
            for square in column_square:
                if bro.board[square] == self.mark:
                    count += 1
                if bro.board[square] == self.other_mark(mark):
                    count = 0
            if count == 1:
                x1 = 1
            elif count == 2:
                x1 = 1
                x2 = 1
            count = 0

            for square in row_square:
                if bro.board[square] == self.other_mark(mark):
                    count += 1
                if bro.board[square] == self.mark:
                    count = 0
            if count == 1:
                o1 = 1
            elif count == 2:
                o1 = 1
                o2 = 1

            h_score = (3 * x2 + x1) - (3 * o2 + o1)
            h_scores.append(h_score)

        # calculate heuristic score for the diagonals 1
        diagonal_square = [0, 4, 8]
        x1 = 0
        x2 = 0
        o1 = 0
        o2 = 0

        count = 0
        for square in diagonal_square:
            if bro.board[square] == self.mark:
                count += 1
            if bro.board[square] == self.other_mark(mark):
                count = 0
        if count == 1:
            x1 = 1
        elif count == 2:
            x1 = 1
            x2 = 1
        count = 0

        h_score = (3 * x2 + x1) - (3 * o2 + o1)
        h_scores.append(h_score)

        # calculate heuristic score for the diagonals 2
        diagonal_square = [2, 4, 6]
        x1 = 0
        x2 = 0
        o1 = 0
        o2 = 0

        count = 0
        for square in diagonal_square:
            print(square)
            if bro.board[square] == self.mark:
                count += 1
            if bro.board[square] == self.other_mark(mark):
                count = 0
        if count == 1:
            x1 = 1
        elif count == 2:
            x1 = 1
            x2 = 1
        count = 0

        h_score = (3 * x2 + x1) - (3 * o2 + o1)
        h_scores.append(h_score)
        return sum(h_scores)
