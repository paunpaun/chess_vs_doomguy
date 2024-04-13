import copy

class ChessBoard:

    def __init__(self):
        """
        Initializes an 8x8 chessboard
        
        """
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.is_white_turn = True

    def initialize_board(self):
        """
        Initializes the chessboard with starting positions of pieces
        
        """
        self.board[0][0] = 'r' 
        self.board[0][1] = 'n' 
        self.board[0][2] = 'b' 
        self.board[0][3] = 'q'  
        self.board[0][4] = 'k'   
        self.board[0][5] = 'b'  
        self.board[0][6] = 'n'  
        self.board[0][7] = 'r'  

        for i in range(8):
            self.board[1][i] = 'p' 

        self.board[7][0] = 'R'  
        self.board[7][1] = 'N'  
        self.board[7][2] = 'B' 
        self.board[7][3] = 'Q'   
        self.board[7][4] = 'K'   
        self.board[7][5] = 'B' 
        self.board[7][6] = 'N' 
        self.board[7][7] = 'R' 

        for i in range(8):
            self.board[6][i] = 'P'  

    def make_move(self, move):
        """
        Makes a move on the chessboard

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)

        """
        from_x, from_y, to_x, to_y = move
        piece = self.board[from_x][from_y] 
        self.board[from_x][from_y] = ' '  
        self.board[to_x][to_y] = piece  

    def is_move_legal(self, move, is_white_turn):
        """
        Checks if a move is legal

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - bool : True if the move is legal, otherwise False

        """
        from_x, from_y, to_x, to_y = move
        piece = self.board[from_x][from_y]
        target_piece = self.board[to_x][to_y]

        if not (0 <= from_x < 8) or not (0 <= from_y < 8) or piece == ' ':
            return False

        if not (0 <= to_x < 8) or not (0 <= to_y < 8):
            return False

        if target_piece.isupper() and piece.isupper():
            return False
        
        if target_piece.islower() and piece.islower():
            return False

        if piece == 'r' or piece == 'R':
            if not self.is_rook_move_legal(move):
                return False
            
        if piece == 'b' or piece == 'B':
            if not self.is_bishop_move_legal(move):
                return False
            
        if piece == 'n' or piece == 'N':
            if not self.is_knight_move_legal(move):
                return False
            
        if piece == 'k' or piece == 'K':
            if not self.is_king_move_legal(move):
                return False
            
        if piece == 'q' or piece == 'Q':
            if not self.is_bishop_move_legal(move) and not self.is_rook_move_legal(move):
                return False
            
        if piece == 'p' or piece == 'P':
            if not self.is_pawn_move_legal(move):
                return False
             
        if is_white_turn and piece.isupper():
            if self.is_next_move_check(move,is_white_turn):
                return False
            
        if not is_white_turn and piece.islower():
            if self.is_next_move_check(move,is_white_turn):
                return False

        return True
    
    def is_rook_move_legal(self, move):
        """
        Checks if the rook's move is legal 

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)

        Return:
        - bool : True if the move is legal, otherwise False

        """
        from_x, from_y, to_x, to_y = move

        if from_x != to_x and from_y != to_y:
            return False

        if from_x == to_x:
            step = 1 if from_y < to_y else -1
            y = from_y + step

            while y != to_y:
                if not (0 <= y < 8) or self.board[from_x][y] != ' ':
                    return False
                y += step
        else:
            step = 1 if from_x < to_x else -1
            x = from_x + step

            while x != to_x:
                if not (0 <= x < 8) or self.board[x][from_y] != ' ':
                    return False
                x += step

        return True
   
    def is_bishop_move_legal(self, move):
        """
        Checks if the bishop's move is legal

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)

        Return:
        - bool : True if the move is legal, otherwise False

        """
        from_x, from_y, to_x, to_y = move

        if abs(from_x - to_x) != abs(from_y - to_y):
            return False

        x_step = 1 if to_x > from_x else -1
        y_step = 1 if to_y > from_y else -1
        x, y = from_x + x_step, from_y + y_step

        while (x, y) != (to_x, to_y):
            if not (0 <= x < 8) or not (0 <= y < 8) or self.board[x][y] != ' ':
                return False
            x += x_step
            y += y_step

        return True
    
    def is_knight_move_legal(self, move):
        """
        Checks if the knight's move is legal

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)

        Return:
        - bool : True if the move is legal, otherwise False

        """
        from_x, from_y, to_x, to_y = move

        dx = abs(to_x - from_x)
        dy = abs(to_y - from_y)

        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
    
    def is_king_move_legal(self, move):
        """
        Checks if the king's move is legal

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)
        
        Return:
        - bool : True if the move is legal, otherwise False
        
        """
        from_x, from_y, to_x, to_y = move

        x_diff = abs(from_x - to_x)
        y_diff = abs(from_y - to_y)

        return x_diff <= 1 and y_diff <= 1
    
    def is_pawn_move_legal(self, move):
        """
        Check if the pawn's move is legal
        
        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)

        Return:
        - bool : True if the move is legal, otherwise False

        """

        from_x, from_y, to_x, to_y = move
        piece = self.board[from_x][from_y]
        
        if piece == 'P':
            is_white = True
        else:
            is_white = False
        x_diff = abs(from_x - to_x)
        y_diff = abs(from_y - to_y)

        if is_white:

            if from_x - to_x == 1 and y_diff == 0 and self.board[to_x][to_y] == ' ':
                return True

            if from_x == 6 and from_x - to_x == 2 and y_diff == 0 and self.board[to_x][to_y] == ' ' and self.board[to_x+1][to_y] == ' ':
                return True

            if from_x - to_x == 1 and y_diff == 1 and self.board[to_x][to_y].islower():
                return True
        else:

            if to_x - from_x == 1 and y_diff == 0 and self.board[to_x][to_y] == ' ':
                return True

            if from_x == 1 and to_x - from_x == 2 and y_diff == 0 and self.board[to_x][to_y] == ' ' and self.board[to_x-1][to_y] == ' ':
                return True

            if to_x - from_x == 1 and y_diff == 1 and self.board[to_x][to_y][0].isupper():
                return True

        return False

    def get_legal_moves(self,is_white_turn):
        """
        Finds all legal moves of a given side and stores them in a list
        
        Parameters:
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - list[] : list containing all legal moves of the given side

        """

        legal_moves = []

        for from_x in range(8):
            for from_y in range(8):
                piece = self.board[from_x][from_y]
                if (is_white_turn == True and piece.isupper()) or (is_white_turn == False and piece.islower()):
                    for to_x in range(8):
                        for to_y in range(8):
                            move = (from_x, from_y, to_x, to_y)
                            if self.is_move_legal(move,is_white_turn):
                                legal_moves.append(move)

        return legal_moves

    def is_square_attacked(self, x, y, is_white_turn):
        """
        Check if the square at position (x, y) is attacked by any of the opponent's pieces

        Parameters:
        - x: row
        - y: column
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - list[] : list containing all legal moves of the given side
        
        """
        opponent_pieces = [
            'r', 'n', 
            'b', 'q', 
            'k', 'p'
            ] if is_white_turn else [
            'R', 'N', 
            'B', 'Q', 
            'K', 'P'
            ]

        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece in opponent_pieces:
                    move = (i, j, x, y)
                    if self.is_move_legal(move,is_white_turn):
                        return True

        return False

    def find_king_position(self, is_white_turn):
        """
        Find the position of the king based on the current player's turn
        
        Parameters:
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - int x,y: the king's position (null if the king can't be found)

        """
        king = 'K' if is_white_turn else 'k'
        king_x, king_y = None, None

        for x in range(8):
            for y in range(8):
                if self.board[x][y] == king:
                    king_x, king_y = x, y
                    break  
            else:
                continue  
            break  

        return king_x, king_y
   
    def copy_board(self):
        """
        Create a deep copy of the current chessboard

        Return:
        - Chessboard object: copied board
        
        """
        copied_board = copy.deepcopy(self)

        return copied_board

    def is_next_move_check(self,move,is_white_turn):
        """
        Checks if doing the given move is going to put the king in check

        Parameters:
        - move: tuple which cointains starting position and target position (y1,x1,y2,x2)
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - bool: True if the next move is check, False otherwise
        
        """
        board_copy = self.copy_board()
        board_copy.make_move(move)     
        king_x, king_y = board_copy.find_king_position(is_white_turn)

        if board_copy.is_square_attacked(king_x,king_y,is_white_turn):
            return True
        
        return False

    def is_checkmate(self, is_white_turn):
        """
        Check if the king is in check
        
        Parameters:
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - bool : True if it's checkmate, otherwise False

        """
        king_x, king_y = self.find_king_position(is_white_turn)

        if (king_x == None or king_y == None):
            return True

        if self.is_square_attacked(king_x, king_y, is_white_turn):
            legal_moves = self.get_legal_moves(is_white_turn)

            for move in legal_moves:
                board_copy = self.copy_board()
                board_copy.make_move(move)
                new_king_x, new_king_y = board_copy.find_king_position(is_white_turn)
               
                if not board_copy.is_square_attacked(new_king_x, new_king_y, is_white_turn):
                    return False
                
            return True

        return False

    def is_stalemate(self, is_white_turn):
        """
        Check if the current player is in a stalemate position
        
        Parameters:
        - is_white_turn: True if the it's white's turn, False otherwise

        Return:
        - bool : True if it's stalemate, otherwise False

        """
        king_x, king_y = self.find_king_position(is_white_turn)

        if (king_x == None or king_y == None):
            return True

        if self.is_square_attacked(king_x, king_y, is_white_turn):
            return False 

        legal_moves = self.get_legal_moves(is_white_turn)

        for move in legal_moves:
            board_copy = self.copy_board()
            board_copy.make_move(move)  
            new_king_x, new_king_y = board_copy.find_king_position(is_white_turn)   

            if not board_copy.is_square_attacked(new_king_x, new_king_y, is_white_turn):
                return False 

        return True

    def evaluate_board(self):
        """
        Evaluate the current chessboard position.
        Positive values indicate an advantage for black, and negative values indicate an advantage for white.

        Return:
        - int evaluation: the evaluation
        """
        evaluation = 0

        piece_values = {
            'p': 10, 
            'q': 90, 
            'k': 900, 
            'r': 50,  
            'n': 30,  
            'b': 30, 
            'P': -10, 
            'Q': -90,  
            'K': -900,
            'R': -50,   
            'N': -30, 
            'B': -30    
        }

        for row in self.board:
            for piece in row:
                evaluation += piece_values.get(piece, 0)

        return evaluation