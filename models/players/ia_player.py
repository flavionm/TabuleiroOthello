class IA:
    INFINITY = 2000000000
    MIN_DEPTH = 3

    MAX_TIME = 3
    EST_BRANCHING = 5

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
        return 0
