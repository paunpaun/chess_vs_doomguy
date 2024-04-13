
class ChessAI:

    def __init__(self,chessboard, max_depth=3):
        self.chessboard = chessboard
        self.max_depth = max_depth

    def minimax(self, board, depth, alpha, beta, is_maximizing_player):
        if depth == 0 or board.is_checkmate(is_maximizing_player) or board.is_stalemate(is_maximizing_player):
            return board.evaluate_board(),None

        legal_moves = self.order_moves(board.board,board.get_legal_moves(not is_maximizing_player),is_maximizing_player)
        best_move = None

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                board_copy = board.copy_board()
                board_copy.make_move(move)
                eval = self.minimax(board_copy, depth - 1, alpha, beta, False)[0]
                if(eval > max_eval):
                    best_move = move
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval,best_move 
        
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board_copy = board.copy_board()
                board_copy.make_move(move)
                eval = self.minimax(board_copy, depth - 1, alpha, beta, True)[0]
                if(eval < min_eval):
                    best_move = move
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval,best_move

    def order_moves(self, board, moves, is_white_turn):
        
        if is_white_turn:
            capture_moves = [move for move in moves if board[move[2]][move[3]].isupper()]
            non_capture_moves = [move for move in moves if not board[move[2]][move[3]].isupper()]

        else:
            capture_moves = [move for move in moves if board[move[2]][move[3]].islower()]
            non_capture_moves = [move for move in moves if not board[move[2]][move[3]].islower()]

        return capture_moves + non_capture_moves

    def find_best_move(self):

        board_copy = self.chessboard.copy_board()
        best_move = self.minimax(board_copy, self.max_depth, float('-inf'), float('inf'),True)[1]

        return best_move

    def ai_turn(self):

        best_move = self.find_best_move()

        self.chessboard.make_move(best_move)

    def change_difficulty(self,difficulty):
        self.max_depth = difficulty