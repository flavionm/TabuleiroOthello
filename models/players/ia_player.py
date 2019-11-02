class IA:
    INFINITY = 2000000000
    MIN_DEPTH = 3

    MAX_TIME = 3
    EST_BRANCHING = 6

    import time
    time = time.time

    def __init__(self, color):
        if color == '@':
            self.color = color
            self.opp_color = 'o'
        else:
            self.color = color
            self.opp_color = '@'

    def play(self, board):
        depth = self.MIN_DEPTH
        last_time = 0
        total_time = 0
        while self.EST_BRANCHING * last_time + last_time + total_time < self.MAX_TIME:
            start = self.time()
            move = self.__minimax(board, depth)
            last_time = self.time() - start
            total_time += last_time
            depth += 1
        return move

    def __minimax(self, board, depth):
        move, _ = self.__recursive_max(board, self.INFINITY, None, 0, depth)

        return move

    def __recursive_max(self, board, max_score, parent_killer_move, depth, max_depth):
        if depth >= max_depth:
            return None, self.__h(board)

        curr_move = None
        curr_score = -self.INFINITY
        child_killer_move = None

        valid_moves = board.valid_moves(self.color)
        if not valid_moves:
            _, curr_score = self.__recursive_min(
                board, curr_score, child_killer_move, depth + 1, max_depth)
        else:
            if parent_killer_move is not None:
                valid_moves = [parent_killer_move] + valid_moves
            for next_move in valid_moves:
                next_board = board.get_clone()
                next_board.play(next_move, self.color)
                killer_move, next_score = self.__recursive_min(
                    next_board, curr_score, child_killer_move, depth + 1, max_depth)
                if next_score > curr_score:
                    curr_score = next_score
                    curr_move = next_move
                    if curr_score >= max_score:
                        break
                else:
                    child_killer_move = killer_move

        return curr_move, curr_score

    def __recursive_min(self, board, min_score, parent_killer_move, depth, max_depth):
        if depth >= max_depth:
            return None, self.__h(board)

        curr_move = None
        curr_score = self.INFINITY
        child_killer_move = None

        valid_moves = board.valid_moves(self.opp_color)
        if not valid_moves:
            _, curr_score = self.__recursive_min(
                board, curr_score, child_killer_move, depth + 1, max_depth)
        else:
            if parent_killer_move is not None:
                valid_moves = [parent_killer_move] + valid_moves
            for next_move in valid_moves:
                next_board = board.get_clone()
                next_board.play(next_move, self.opp_color)
                killer_move, next_score = self.__recursive_max(
                    next_board, curr_score, child_killer_move, depth + 1, max_depth)
                if next_score < curr_score:
                    curr_score = next_score
                    curr_move = next_move
                    if curr_score <= min_score:
                        break
                else:
                    child_killer_move = killer_move

        return curr_move, curr_score

    def __h(self, board):
        return (25 * self.__coin_parity(board)
                + 25 * self.__stability(board)
                + 5 * self.__mobility(board)
                + 30 * self.__corners(board))

    def __coin_parity(self, board):
        if self.color == 'o':
            score, opp_score = board.score()
        else:
            opp_score, score = board.score()
        return 100 * (score - opp_score) / (score + opp_score)

    def __stability(self, board):
        return 0

    def __mobility(self, board):
        return 0

    def __corners(self, board):
        my_occupancy, opp_ocupancy = self.__corner_occupancy(board)
        my_closeness, opp_closeness = self.__corner_closeness(board)

        my_corners = 2 * my_occupancy - my_closeness
        opp_corners = 2 * opp_ocupancy - opp_closeness

        if my_corners + opp_corners == 0:
            return 0
        else:
            return 100 * (my_corners - opp_corners) / (my_corners + opp_corners)

    def __corner_occupancy(self, board):
        my_points = opp_points = 0
        if board.board[1][1] == self.color:
            my_points += 1
        elif board.board[1][1] == self.opp_color:
            opp_points += 1
        if board.board[1][8] == self.color:
            my_points += 1
        elif board.board[1][8] == self.opp_color:
            opp_points += 1
        if board.board[8][0] == self.color:
            my_points += 1
        elif board.board[8][0] == self.opp_color:
            opp_points += 1
        if board.board[8][8] == self.color:
            my_points += 1
        elif board.board[8][8] == self.opp_color:
            opp_points += 1
        return my_points, opp_points

    def __corner_closeness(self, board):
        my_points = opp_points = 0
        if board.board[1][1] == '.':
            if board.board[1][2] == self.color:
                my_points += 1
            elif board.board[1][2] == self.opp_color:
                opp_points += 1
            if board.board[2][2] == self.color:
                my_points += 1
            elif board.board[2][2] == self.opp_color:
                opp_points += 1
            if board.board[2][1] == self.color:
                my_points += 1
            elif board.board[2][1] == self.opp_color:
                opp_points += 1

        if board.board[1][8] == '.':
            if board.board[1][7] == self.color:
                my_points += 1
            elif board.board[1][7] == self.opp_color:
                opp_points += 1
            if board.board[2][7] == self.color:
                my_points += 1
            elif board.board[2][7] == self.opp_color:
                opp_points += 1
            if board.board[2][8] == self.color:
                my_points += 1
            elif board.board[2][8] == self.opp_color:
                opp_points += 1

        if board.board[8][1] == '.':
            if board.board[8][2] == self.color:
                my_points += 1
            elif board.board[8][2] == self.opp_color:
                opp_points += 1
            if board.board[7][2] == self.color:
                my_points += 1
            elif board.board[7][2] == self.opp_color:
                opp_points += 1
            if board.board[7][1] == self.color:
                my_points += 1
            elif board.board[7][1] == self.opp_color:
                opp_points += 1

        if board.board[8][8] == '.':
            if board.board[7][8] == self.color:
                my_points += 1
            elif board.board[7][8] == self.opp_color:
                opp_points += 1
            if board.board[7][7] == self.color:
                my_points += 1
            elif board.board[7][7] == self.opp_color:
                opp_points += 1
            if board.board[8][7] == self.color:
                my_points += 1
            elif board.board[8][7] == self.opp_color:
                opp_points += 1

        return my_points, opp_points
