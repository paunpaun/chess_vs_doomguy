from pathlib import Path
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor

class ChessboardWindow(QWidget):

    pieces = {'p': 'pawn', 'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king'}

    def __init__(self, chessboard):
        super().__init__()
        self.chessboard = chessboard
        self.square_size = 52
        self.piece_images = self.load_piece_images()     
        self.setFixedSize(8 * self.square_size, 8 * self.square_size)
        self.selected_piece = None
        self.selected_position = None
        self.legal_move_highlights_buffer = []
        
    def load_piece_images(self):
        piece_images = {}

        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent 
        
        for color in ['white', 'black']:
            for piece in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']:
                image_path = BASE_DIR / 'assets' / 'chess_icons' / f'{color}_{piece}.png'
                image = QPixmap(str(image_path))  
                image = image.scaled(self.square_size,self.square_size,
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation)
                piece_images[f'{color}_{piece}'] = image

        return piece_images

    def paintEvent(self, event):
        painter = QPainter(self)

        for row in range(8):
            for col in range(8):
                x = col * self.square_size
                y = row * self.square_size
                color = "#c63232" if (row + col) % 2 == 0 else "#9c1b1b"
                painter.fillRect(x, y, self.square_size, self.square_size, QBrush(QColor(color)))
                piece = self.chessboard.board[row][col] 

                if piece.isupper() or piece.islower():
                    color_prefix = 'white_' if piece.isupper() else 'black_'
                    key = color_prefix + ChessboardWindow.pieces[piece.lower()]
                    piece_image = self.piece_images.get(key)

                    if piece_image:
                        painter.drawPixmap(x, y, piece_image)

        for (row, col) in self.legal_move_highlights_buffer:
            center_x = (col * self.square_size) 
            center_y = (row * self.square_size)
            painter.setOpacity(0.5)
            painter.setBrush(QBrush(QColor("#3a3133")))
            painter.drawRect(center_x,center_y,self.square_size,self.square_size)
            painter.setOpacity(1.0)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            click_pos = event.pos() 
            self.handle_click(click_pos)  

    def handle_click(self, position):
        x, y = position.x(), position.y()
        col = x // self.square_size
        row = y // self.square_size
        piece = self.chessboard.board[row][col]

        if self.selected_piece is None:
            print('generating from...')

            if piece != ' ':
                self.selected_piece = (row, col) 
                self.highlight_legal_moves(row, col) 

        elif self.selected_position is None:
            print('generating to...')
            to_x, to_y = row, col
            self.selected_position = (to_x, to_y)
            self.update()  
            
        print(f"Left click at position: {col}, {row}, piece = {piece}")

    def highlight_legal_moves(self,row,col):
        legal_moves = self.chessboard.get_legal_moves(True)

        for move in legal_moves:
            from_x, from_y, to_x, to_y = move
            
            if from_x == row and from_y == col:
                self.legal_move_highlights_buffer.append((to_x, to_y))

        self.update()

    def remove_legal_move_highlights(self):
        self.legal_move_highlights_buffer = []
        self.update()