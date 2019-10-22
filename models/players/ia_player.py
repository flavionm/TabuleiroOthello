class IA:
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
        board, _ = self.__recursive_max(board, 1)

        return board


    def __recursive_max(self, board, depth):
        curr_board = None
        curr_score = -2000000000
        for next_board in board.valid_moves(self.color):
            _, next_score = self.__recursive_min(next_board, depth + 1)
            if next_score > curr_score:
                curr_score = next_score
                curr_board = next_board
        
        return curr_board, curr_score


    def __recursive_min(self, board, depth):
        curr_board = None
        curr_score = 2000000000
        for next_board in board.valid_moves(self.opp_color):
            _, next_score = self.__recursive_max(next_board, depth + 1)
            if next_score < curr_score:
                curr_score = next_score
                curr_board = next_board
        
        return curr_board, curr_score


    def __h(self, board):
        return 0