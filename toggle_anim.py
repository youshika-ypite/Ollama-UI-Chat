from PySide6.QtWidgets import QCheckBox

from PySide6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter

from PySide6.QtCore import Qt, QSize, QPoint, QPointF, QRectF, Slot, Property
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup

class AnimatedToggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE",
        pulse_anim_draw=False
        ):
        super().__init__(parent)

        self.pulse_anim_draw = pulse_anim_draw

        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        # Widget Rect

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0
        
        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic) # OutInCubic #Linear #InCubic #OutCubic
        self.animation.setDuration(200) # ms time

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350) # ms time
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)
        
    def sizeHint(self):
        return QSize(48, 37)
    
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)
    
    @Slot(int)
    def setup_animation(self, value):
        self.animation_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animation_group.start()

    def paintEvent(self, e: QPaintEvent):
        
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.4 * contRect.height()
            )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position


        # Draw pulse trigger Ellipse
        if self.pulse_anim.state() == QPropertyAnimation.Running and self.pulse_anim_draw:
            p.setBrush(
                self._pulse_checked_animation if self.isChecked() else
                self._pulse_unchecked_animation
            )
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)
            
        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)
            
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        # Button Ellipse
        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius
        )
        p.end()
        
    @Property(float)
    def handle_position(self):
        return self._handle_position
    
    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius
    
    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()