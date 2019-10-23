class IA:
    INFINITY = 2000000000
    MAX_DEPTH = 4

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
        move, _ = self.__recursive_max(board, 1)

        return move

    def __recursive_max(self, board, depth):
        if depth >= self.MAX_DEPTH:
            return None, self.__h(board)

        curr_move = None
        curr_score = -self.INFINITY
        for next_move in board.valid_moves(self.color):
            board.play(next_move, self.color)
            _, next_score = self.__recursive_min(board, depth + 1)
            if next_score > curr_score:
                curr_score = next_score
                curr_move = next_move

        return curr_move, curr_score

    def __recursive_min(self, board, depth):
        if depth >= self.MAX_DEPTH:
            return board, self.__h(board)

        curr_move = None
        curr_score = self.INFINITY
        for next_move in board.valid_moves(self.opp_color):
            board.play(next_move, self.opp_color)
            _, next_score = self.__recursive_max(board, depth + 1)
            if next_score < curr_score:
                curr_score = next_score
                curr_move = next_move

        return curr_move, curr_score

    def __h(self, board):
        return 0
