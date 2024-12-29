from PySide6.QtWidgets import QFrame
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

class WidgetCloseAnimation():
    def __init__(self, main_frame: QFrame):
        self.main_widget = main_frame

    def toggle_anim(self):
        width = self.main_widget.width()
        new_width = 0 if width != 0 else 200

        self.animation = QPropertyAnimation(self.main_widget, b"maximumWidth")

        self.animation.setDuration(200)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.animation.start()