import random
import time
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSlider, QHBoxLayout
from PyQt6.QtGui import QMovie, QPixmap, QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from pathlib import Path
import pygame

class StatusWindow(QWidget):

    def __init__(self,chessboard):
        super().__init__()

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent 
        self.status_assets_path = self.BASE_DIR / 'assets' / 'images'

        self.chessboard = chessboard

        self.setFixedSize(140,466)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.frame = QLabel()
        self.frame.setStyleSheet("background-color: #ffffff;")
        self.frame.setFixedSize(140,150)
        self.frame_image = QPixmap(str(self.status_assets_path / 'frame.jpg'))
        self.frame.setPixmap(self.frame_image)
        self.frame.setScaledContents(True)

        self.doom_gif_label = QLabel()
        #self.doom_gif_label.setGeometry(0,0,20,20)
        self.doom_100_gif = QMovie(str(self.status_assets_path / 'doom.gif'))
        self.doom_gif_label.setMovie(self.doom_100_gif)
        self.doom_100_gif.start()
        self.doom_gif_label.setScaledContents(True)
        self.doom_angry_image = QPixmap(str(self.status_assets_path / 'angry.png'))
        self.doom_happy_image = QPixmap(str(self.status_assets_path / 'happy.png'))

        self.message_label = QLabel()
        self.message_label.setFixedSize(140,40)
        self.message_label.setWindowTitle("Message")
        self.message_label.setStyleSheet(
            "color: white; background-color: #3a3032; font-weight: bold; font-style: italic;")
        self.messages = ["good move, i like it",
                         "goofy move, i dont like it"]

        self.bgm_path = str(self.BASE_DIR/ 'assets' / 'sound' / 'm1.mp3')  
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.bgm_path)
        pygame.mixer.music.play(-1)

        isabelle_sound_path = str(self.BASE_DIR / 'assets' / 'sound' / 'isab.mp3')
        self.isabelle_sound = pygame.mixer.Sound(isabelle_sound_path)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50) 
        self.volume_slider.valueChanged.connect(self.on_volume_changed) 

        self.current_score = self.chessboard.evaluate_board()
        self.score_label = QLabel(f" SCORE: {-self.current_score}") 
        font = QFont("Gemola", 18, 1, True)  
        font.setBold(True)
        palette = self.score_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255,0,0)) 
        self.score_label.setFont(font)
        self.score_label.setPalette(palette)

        self.brainrot = QLabel()
        self.brainrot.setFixedSize(140,200)
        self.brainrot.setScaledContents(True)
        self.subs = QMovie(str(self.status_assets_path / 'subs.gif'))
        self.minecraft = QMovie(str(self.status_assets_path / 'minecraft.gif'))
        self.guy = QMovie(str(self.status_assets_path / 'guy.gif'))
        self.brainrot.setMovie(self.subs)
        self.subs.start()

        self.bored_button = QPushButton("Bored? Game is slow?")
        self.bored_button.setStyleSheet("background-color: #9c1b1b; font-weight: bold;")
        self.bored_button.clicked.connect(self.initialize_brainrot)


        self.brainrot_button = QPushButton("Change")
        self.brainrot_button.setStyleSheet("background-color: #9c1b1b; font-weight: bold;")
        self.brainrot_button.clicked.connect(self.update_brainrot)

        self.stop = QPushButton("Stop")
        self.stop.setStyleSheet("background-color: #9c1b1b; font-weight: bold;")
        self.stop.clicked.connect(self.remove_brainrot)

        self.brainrot_buttons = QWidget()
        self.brainrot_buttons_layout = QHBoxLayout(self.brainrot_buttons)
        self.brainrot_buttons_layout.addWidget(self.brainrot_button)
        self.brainrot_buttons_layout.addWidget(self.stop)

        layout2 = QVBoxLayout(self.frame)
        layout2.addWidget(self.doom_gif_label, Qt.AlignmentFlag.AlignCenter)   
        
        self.layout.addWidget(self.frame) 
        self.layout.addWidget(self.message_label)
        self.layout.addWidget(self.volume_slider)
        self.layout.addWidget(self.score_label) 
        self.layout.addWidget(self.bored_button) 

    def update_score(self):
        self.current_score = self.chessboard.evaluate_board()
        self.score_label.setText(f" SCORE: {-self.current_score}")

    def on_volume_changed(self, value):
        volume = value / 100.0 
        pygame.mixer.music.set_volume(volume)

    def initialize_brainrot(self):
        self.layout.addWidget(self.brainrot_buttons)
        self.layout.addWidget(self.brainrot)

        self.bored_button.setParent(None)
        self.layout.removeWidget(self.bored_button)

    def remove_brainrot(self):
        self.brainrot.setParent(None)
        self.brainrot_buttons.setParent(None)
        self.layout.removeWidget(self.brainrot)
        self.layout.removeWidget(self.brainrot_buttons)

        self.layout.addWidget(self.bored_button)

    def update_brainrot(self):
        if self.brainrot.movie() == self.subs:
            self.brainrot.setMovie(self.guy)
            self.guy.start()
        elif self.brainrot.movie() == self.guy:
            self.brainrot.setMovie(self.minecraft)
            self.minecraft.start()
        elif self.brainrot.movie() == self.minecraft:
            self.brainrot.setMovie(self.subs)
            self.subs.start()

    def play_isabelle_sound(self):
        
        current_bgm_volume = pygame.mixer.music.get_volume()
        self.isabelle_sound.set_volume(current_bgm_volume)
        
        random_index = random.randint(0, 1)

        self.doom_100_gif.stop()
        

        self.isabelle_sound.play()

        if random_index == 0 : 
            self.doom_gif_label.setPixmap(self.doom_happy_image)
            self.update_message_label(self.messages[0])
            

        if random_index == 1 : 
            self.doom_gif_label.setPixmap(self.doom_angry_image)
            self.update_message_label(self.messages[1])
            

        self.isabelle_sound.stop()
        self.doom_gif_label.clear()
        self.doom_100_gif = QMovie(str(self.status_assets_path / 'doom.gif'))
        self.doom_gif_label.setMovie(self.doom_100_gif)
        self.doom_100_gif.start()

    def update_message_label(self, message_text):
        gradual_text = ""
        for letter in message_text:
            time.sleep(0.05)
            gradual_text += letter
            self.message_label.setText(gradual_text)
        time.sleep(0.5)