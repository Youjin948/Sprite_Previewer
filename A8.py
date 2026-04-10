#Author: Youjin Oh
#GitHub Repo: https://github.com/Youjin948/Sprite_Previewer.git

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

def load_sprite(number_of_frames):
    frames = []
    for frame in range(1, number_of_frames + 1):
        file_name = f"Sprite_{frame}.png"
        frames.append(QPixmap(file_name))
    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")

        self.num_frames = 6
        self.frames = load_sprite(self.num_frames)

        self.current_frame = 0
        self.is_animating = False
        self.fps = 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.setupUI()

    def setupUI(self):
        frame = QFrame()
        layout = QVBoxLayout()

        self.sprite_label = QLabel()
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setPixmap(
            self.frames[0].scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        )
        layout.addWidget(self.sprite_label)

        self.fps_text_label = QLabel("Frames per second")
        self.fps_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.fps_text_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 100)
        self.slider.setValue(self.fps)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(5)
        self.slider.valueChanged.connect(self.update_fps)
        layout.addWidget(self.slider)

        self.fps_value_label = QLabel(str(self.fps))
        self.fps_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.fps_value_label)

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.clicked.connect(self.toggle_animation)
        layout.addWidget(self.start_stop_button, alignment=Qt.AlignmentFlag.AlignCenter)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_animation)
        file_menu.addAction(pause_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        frame.setLayout(layout)
        self.setCentralWidget(frame)

    def update_fps(self, value):
        self.fps = value
        self.fps_value_label.setText(str(self.fps))
        if self.is_animating:
            self.timer.setInterval(int(1000 / self.fps))

    def toggle_animation(self):
        if self.is_animating:
            self.stop_animation()
        else:
            self.start_animation()

    def start_animation(self):
        self.is_animating = True
        self.start_stop_button.setText("Stop")
        self.timer.start(int(1000 / self.fps))

    def stop_animation(self):
        self.is_animating = False
        self.start_stop_button.setText("Start")
        self.timer.stop()

    def pause_animation(self):
        self.stop_animation()

    def update_frame(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.sprite_label.setPixmap(
            self.frames[self.current_frame].scaled(
                200, 200, Qt.AspectRatioMode.KeepAspectRatio
            )
        )

def main():
    app = QApplication([])
    window = SpritePreview()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()