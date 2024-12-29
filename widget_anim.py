
from PySide6.QtCore import QEasingCurve
from PySide6.QtCore import QPropertyAnimation

from PySide6.QtWidgets import QPushButton, QFrame

class WidgetCloseAnimation():
    def __init__(self, main_frame: QFrame, side_frame: QFrame):

        self.main_widget = main_frame
        self.side_widget = side_frame

        self.button = QPushButton("Свернуть/Развернуть")
        self.button.clicked.connect(self.toggle_anim)

    def get_button(self) -> QPushButton: return self.button

    def toggle_anim(self):

        width = self.main_widget.width()
        new_width = 0 if width != 0 else 200

        self.animation = QPropertyAnimation(self.main_widget, b"maximumWidth")

        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.animation.start()