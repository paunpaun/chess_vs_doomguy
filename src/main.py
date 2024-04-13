import sys
from core.backend.logic.board import ChessBoard
from core.backend.logic.ai import ChessAI
from core.backend.ui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication
import threading

def main(chessboard,ai,main_window):

    chessboard_gui = main_window.chessboard_window
    status_bar = main_window.status_window

    def game_loop():
        player_turn = True 
        while not main_window.stop_game and not chessboard.is_checkmate(player_turn) and not chessboard.is_stalemate(player_turn):
            if player_turn:

                if chessboard_gui.selected_position is not None and chessboard_gui.selected_piece is not None:
                    from_x, from_y = chessboard_gui.selected_piece  
                    to_x, to_y = chessboard_gui.selected_position 

                    if isinstance(chessboard_gui.selected_piece, tuple) and isinstance(chessboard_gui.selected_piece,tuple):
                        move = (from_x, from_y, to_x, to_y)
                        print('move: ',move)
                        print('piece: ',chessboard.board[from_x][from_y])
                        print('target_piece: ', chessboard.board[to_x][to_y])
                        print('--------------------------------------------------------------------\n')

                        if chessboard.is_move_legal(move,True) and chessboard.board[from_x][from_y].isupper():                      
                            chessboard.make_move(move)
                            chessboard_gui.update()
                            player_turn = not player_turn

                        else:                            
                            print("Invalid move!...try again\n")
                            chessboard_gui.selected_piece = None  
                            chessboard_gui.selected_position = None 

                    else:
                        print("Unexpected format for selected_piece or selected_position\n")
                        chessboard_gui.selected_piece = None 
                        chessboard_gui.selected_position = None 

                    chessboard_gui.remove_legal_move_highlights()

            else:
                chessboard_gui.selected_piece = None
                chessboard_gui.selected_position = None 

                ai_thread = threading.Thread(target=status_bar.play_isabelle_sound())
                ai_thread.start()
                
                ai.ai_turn()

                chessboard_gui.update()

                player_turn = not player_turn
                status_bar.update_score()

        if chessboard.is_checkmate(player_turn):
            print('CHECKMATE')
        elif chessboard.is_stalemate(player_turn):
            print('STALEMATE')
        elif chessboard.is_checkmate(not player_turn):
            print('AI IN CHECKMATE')
        elif chessboard.is_stalemate(not player_turn):
            print('AI IN STALEMATE')

    game_thread = threading.Thread(target=game_loop)
    game_thread.start()

if __name__ == "__main__":
    chessboard = ChessBoard()
    ai = ChessAI(chessboard)
    app = QApplication(sys.argv)
    main_window = MainWindow(chessboard,ai)
    main(chessboard,ai,main_window)
    main_window.show()
    sys.exit(app.exec())

