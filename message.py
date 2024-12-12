from PySide6.QtCore import QSize

from PySide6.QtGui import Qt, QPixmap

from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QWidget, QFrame, QLayout
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSpacerItem


from config import Config
config = Config()


ICON_SIZE = QSize(24, 24)
ICON_FRAME_SIZE = QSize(48, 48)

USER_HORIZONTAL_SPACER = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding)
BASE_HORIZONTAL_SPACER = QSpacerItem(40, 0, QSizePolicy.Policy.Preferred)


def generate_message_widget(user: bool = False) -> tuple[QWidget, QLabel]:

    if user: tittle_name = config.get_user_name()
    else: tittle_name = config.get_ollama_name()

    widget = QWidget()
    widget.setObjectName("widget")
    widget.setContentsMargins(0, 0, 0, 0)
    # Титульная часть сообщения
    firstlayout = QHBoxLayout()
    firstlayout.setContentsMargins(0, 0, 0, 0)
    firstlayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
    firstframe = QFrame()
    firstframe.setLayout(firstlayout)
        
    # Основная часть сообщения
    secondlayout = QHBoxLayout()
    secondlayout.setContentsMargins(0, 0, 0, 0)
    secondlayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
    secondframe = QFrame()
    secondframe.setLayout(secondlayout)

    mainlayout = QVBoxLayout(widget)
    mainlayout.setSpacing(0)
    mainlayout.addWidget(firstframe)
    mainlayout.addWidget(secondframe)
    mainlayout.setContentsMargins(3, 3, 3, 3)
    mainlayout.setObjectName("message_frame")
    mainlayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

    icon = QLabel()
    if user: chat_icon = QPixmap(config.get_user_icon())
    else: chat_icon = QPixmap(config.get_bot_icon())
    chat_icon = chat_icon.scaled(ICON_SIZE, aspectMode=Qt.AspectRatioMode.KeepAspectRatio, mode=Qt.TransformationMode.SmoothTransformation)
    icon.setPixmap(chat_icon)
    icon.setFixedSize(ICON_SIZE)
    icon_layout = QHBoxLayout()
    icon_layout.addWidget(icon)
    icon_layout.setContentsMargins(0, 0, 0, 0)
    icon_frame = QFrame()
    icon_frame.setFixedSize(ICON_FRAME_SIZE)
    icon_frame.setLayout(icon_layout)

    tittle = QLabel(tittle_name)
    tittle.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
    tittle.setObjectName("msg_tittle")
    tittle_layout = QHBoxLayout()
    tittle_layout.addWidget(tittle)
    tittle_layout.setContentsMargins(6, 6, 6, 6)
    tittle_frame = QFrame()
    tittle_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
    tittle_frame.setObjectName("msg_tittle_frame")
    tittle_frame.setLayout(tittle_layout)



    content = QLabel("Generating..")
    content.setWordWrap(True)
    content.setObjectName("msg_content")
    content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    content.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    content_layout = QHBoxLayout()
    content_layout.addWidget(content)
    content_layout.setContentsMargins(12, 12, 12, 12)
    content_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
    content_frame = QFrame()
    content_frame.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    if user: content_frame.setObjectName("msg_content_frame_user")
    else: content_frame.setObjectName("msg_content_frame_bot")
    content_frame.setLayout(content_layout)



    if user:
        firstframe.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        secondframe.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        tittle_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        tittle.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        firstlayout.addItem(USER_HORIZONTAL_SPACER)
        firstlayout.addWidget(tittle_frame)
        firstlayout.addWidget(icon_frame)
        
        secondlayout.addItem(USER_HORIZONTAL_SPACER)
        secondlayout.addWidget(content_frame)
    else:
        firstframe.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        secondframe.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        tittle_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        firstlayout.addWidget(icon_frame)
        firstlayout.addWidget(tittle_frame)
        firstlayout.addItem(BASE_HORIZONTAL_SPACER)
        secondlayout.addWidget(content_frame)
        secondlayout.addItem(BASE_HORIZONTAL_SPACER)

    return (widget, content)