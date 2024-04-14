from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QRadioButton, QButtonGroup, QSpacerItem
from PyQt6.QtGui import QPainter, QBrush, QColor, QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from core.backend.ui.chessboard_window import ChessboardWindow
from core.backend.ui.status_window import StatusWindow

class MainWindow(QMainWindow):

    def __init__(self,chessboard,ai):
        super().__init__()

        self.ai = ai

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent 
        self.status_assets_path = self.BASE_DIR / 'assets' / 'images'

        self.chessboard_window = ChessboardWindow(chessboard)
        self.status_window = StatusWindow(chessboard)

        self.setWindowTitle("Chessboard")
        self.setFixedSize(700, 500)

        self.easy_button = QRadioButton('Easy(faster)')
        self.easy_button.setStyleSheet(
            "color: white; font-weight: bold; font-style: italic;")
        self.easy_button.toggled.connect(lambda: self.ai.change_difficulty(3))
        self.hard_button = QRadioButton('Hard(slower)')
        self.hard_button.setStyleSheet(
            "color: white; font-weight: bold; font-style: italic;")
        self.hard_button.toggled.connect(lambda: self.ai.change_difficulty(4))

        self.easy_button.setChecked(True) 

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.easy_button)
        self.button_group.addButton(self.hard_button)

        self.button_widget = QWidget(self)
        self.button_widget.resize(400,40)

        url = 'https://qp-keanu.github.io'
        self.credits_url = QLabel(
            f'<a href="{url}">Click for credits</a>',parent=self)
        self.credits_url.setStyleSheet(
            "color: white; font-weight: bold; font-style: italic;")
        self.credits_url.setOpenExternalLinks(True)
        self.credits_url.setGeometry(50,470,500,20)
        self.credits_url.show()

        self.button_widget.resize(400,40)

        frame_pixmap = QPixmap(str(self.status_assets_path / 'brk2.png'))
        frame_label = QLabel(self)
        frame_label.setFixedSize(700,500)
        frame_label.setPixmap(frame_pixmap)
        frame_label.setScaledContents(True)
        
        self.centralWidget = QWidget()       
        self.setCentralWidget(self.centralWidget) 

        
        main_window_layout = QHBoxLayout(self.centralWidget)
        self.button_layout = QHBoxLayout(self.button_widget)
        main_window_layout.addWidget(self.chessboard_window)
        main_window_layout.addWidget(self.status_window)
        self.button_layout.addWidget(self.easy_button)
        self.button_layout.addWidget(self.hard_button)


        self.button_layout.addSpacerItem(QSpacerItem(1000,20))
        self.button_widget.move(50,10)
        self.button_widget.raise_()
        self.credits_url.raise_()

        self.stop_game = False

    def closeEvent(self, event):
        self.stop_game = True
        event.accept()

    def paintEvent(self, e):
        painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('#3a3032'))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(0,0, self.width(), 
                                 self.height())
        painter.fillRect(rect,brush)
        
