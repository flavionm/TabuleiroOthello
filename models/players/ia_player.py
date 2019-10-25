class IA:
    INFINITY = 2000000000
    MAX_DEPTH = 6

    def __init__(self, color):
        if color == '@':
            self.color = color
            self.opp_color = 'o'
        else:
            self.color = color
            self.opp_color = '@'

    def play(self, board):
        return self.__minimax(board)

    def __minimax(self, board):
        move, _ = self.__recursive_max(board, self.INFINITY, 1)

        return move

    def __recursive_max(self, board, max_score, depth):
        if depth >= self.MAX_DEPTH:
            return None, self.__h(board)

        curr_move = None
        curr_score = -self.INFINITY

        valid_moves = board.valid_moves(self.color)
        if not valid_moves:
            _, curr_score = self.__recursive_min(board, curr_score, depth + 1)
        else:
            for next_move in valid_moves:
                next_board = board.get_clone()
                next_board.play(next_move, self.color)
                _, next_score = self.__recursive_min(
                    next_board, curr_score, depth + 1)
                if next_score > curr_score:
                    curr_score = next_score
                    curr_move = next_move
                    if curr_score >= max_score:
                        break

        return curr_move, curr_score

    def __recursive_min(self, board, min_score, depth):
        if depth >= self.MAX_DEPTH:
            return None, self.__h(board)

        curr_move = None
        curr_score = self.INFINITY

        valid_moves = board.valid_moves(self.opp_color)
        if not valid_moves:
            _, curr_score = self.__recursive_min(board, curr_score, depth + 1)
        else:
            for next_move in valid_moves:
                next_board = board.get_clone()
                next_board.play(next_move, self.opp_color)
                _, next_score = self.__recursive_max(
                    next_board, curr_score, depth + 1)
                if next_score < curr_score:
                    curr_score = next_score
                    curr_move = next_move
                    if curr_score <= min_score:
                        break

        return curr_move, curr_score

    def __h(self, board):
        w, b = board.score()
        if self.color == '@':
            return b - w
        else:
            return w - b
