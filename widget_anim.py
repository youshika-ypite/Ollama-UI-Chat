from PySide6.QtCore import QSize, QPoint
from PySide6.QtCore import QEasingCurve, QRect
from PySide6.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation

from PySide6.QtWidgets import QPushButton, QFrame

class WidgetCloseAnimation():
    def __init__(self, main_frame: QFrame, side_frame: QFrame):

        self.main_widget = main_frame
        self.side_widget = side_frame

        self.button = QPushButton("Свернуть/Развернуть")
        self.button.clicked.connect(self.toggle_anim)
        
        main_geom = QRect(self.main_widget.geometry())
        side_geom = QRect(self.side_widget.geometry())

        self.main_hideanim = QPropertyAnimation(self.main_widget, b"geometry")
        self.main_hideanim.setEasingCurve(QEasingCurve.InOutCubic)
        self.main_hideanim.setDuration(200)
        self.main_hideanim.setStartValue(main_geom)

        self.side_hideanim = QPropertyAnimation(self.side_widget, b"geometry")
        self.side_hideanim.setEasingCurve(QEasingCurve.InOutCubic)
        self.side_hideanim.setDuration(200)
        self.side_hideanim.setStartValue(side_geom)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.main_hideanim)
        self.animation_group.addAnimation(self.side_hideanim)

        self.animation_group.setDirection(QAbstractAnimation.Direction.Forward)

        self.animation_group.finished.connect(self.restore_size)

    def get_button(self) -> QPushButton: return self.button
    
    def toggle_anim(self):
        if self.main_widget.geometry().x() >= 0: # Анимация скрытия
            # LeftMenu
            end = QRect(
                QPoint(QPoint(
                    self.main_widget.geometry().x()-self.main_widget.width(),
                    self.main_widget.geometry().y()
                    )
                ),
                QSize(
                    self.main_widget.width(),
                    self.main_widget.height()
                )
            )
            self.main_hideanim.setEndValue(end)
            # RightMenu
            end = QRect(
                QPoint(QPoint(
                    self.side_widget.geometry().x()-self.main_widget.width(),
                    self.side_widget.geometry().y()
                    )
                ),
                QSize(
                    self.side_widget.width()+self.main_widget.width(),
                    self.side_widget.height()
                )
            )
            self.side_hideanim.setEndValue(end)
            self.animation_group.setDirection(QAbstractAnimation.Direction.Forward)

        else: # Анимация показа
            self.animation_group.setDirection(QAbstractAnimation.Direction.Backward)
            self.main_hideanim.setEndValue(QRect(self.main_widget.geometry()))
            self.side_hideanim.setEndValue(QRect(self.side_widget.geometry()))
            # LeftMenu
            end = QRect(
                QPoint(QPoint(0, 0)),
                QSize(
                    self.main_widget.width(),
                    self.main_widget.height()
                )
            )
            self.main_hideanim.setStartValue(end)
            # RightMenu
            end = QRect(
                QPoint(QPoint(
                    self.side_widget.geometry().x()+self.main_widget.width(),
                    self.side_widget.geometry().y()
                    )
                ),
                QSize(
                    self.side_widget.width()-self.main_widget.width(),
                    self.side_widget.height()
                )
            )
            self.side_hideanim.setStartValue(end)

        self.animation_group.start()

    def restore_size(self):
        self.main_hideanim.setStartValue(QRect(self.main_widget.geometry()))
        self.side_hideanim.setStartValue(QRect(self.side_widget.geometry()))
        
        self.main_widget.setGeometry(self.main_widget.geometry())
        self.side_widget.setGeometry(self.side_widget.geometry())