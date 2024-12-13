import sys

from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import QStatusBar

from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QWidget, QFrame

from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout

from config import Config
from chat import ChatWindow
from dialogs import Creator

WINDOW_NAME = "Test chat"
WINDOW_SIZE = QSize(800, 700)
WINDOW_FLAG = Qt.FramelessWindowHint

config = Config()

def generate_button(
        stacked_layout: QStackedLayout,
        index: int,
        page_name: str,
        delete: bool = False
        ) -> QWidget:
    
    def pressed():
        stacked_layout.setCurrentIndex(index)

    def deleted(widget: QWidget, layout: QHBoxLayout):
        config.delete_chat(page_name)
        stacked_layout.removeWidget(stacked_layout.widget(index))
        layout.removeWidget(widget)
        widget.deleteLater()

    widget = QWidget()
    mainlayout = QHBoxLayout(widget)

    button = QPushButton(page_name)
    button.setObjectName("page_btn")
    button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    button.pressed.connect(pressed)

    mainlayout.addWidget(button)

    if delete:
        delete_btn = QPushButton("!DEL")
        delete_btn.setObjectName("del_btn")
        delete_btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        delete_btn.pressed.connect(lambda: deleted(widget, mainlayout))
        mainlayout.addWidget(delete_btn)

    return widget

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self._update_css()
        self._load_policy()

        self.creator = Creator(self.create_chat)

        self.widget = QWidget()
        self.widget.setObjectName("main_widget")
        self.mainlayout = QHBoxLayout(self.widget)
        self.mainlayout.setObjectName("main_layout")

        self.stackLayout = QStackedLayout()
        self.pageLayout = QVBoxLayout()
        self.pageLayout.addLayout(self.stackLayout)


        self.LeftMenuFrame = QFrame()
        self.LeftMenuLayout = QVBoxLayout()
        self.LeftMenuFrame.setLayout(self.LeftMenuLayout)
        self.LeftMenuLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.RightMenuFrame = QFrame()
        self.RightMenuLayout = QVBoxLayout()
        self.RightMenuFrame.setLayout(self.pageLayout)
        self.RightMenuLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)


        self.mainlayout.addWidget(self.LeftMenuFrame)
        self.mainlayout.addWidget(self.RightMenuFrame)


        self.theme_btn = QPushButton("Change theme")
        self.theme_btn.pressed.connect(self.change_theme)
        self.new_chat_btn = QPushButton("Create new chat")
        self.new_chat_btn.pressed.connect(self.creator.show)

        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("status_bar")
        self.status_bar.addPermanentWidget(self.theme_btn)
        self.status_bar.addWidget(self.new_chat_btn)

        self.pages = []
        self.buttons = []

        self.set_all_null_ContentsMargins()
        self.setCentralWidget(self.widget)
        self.setStatusBar(self.status_bar)

        self.load_chats()

    def page_classes(self) -> list[ChatWindow]: return self.pages

    def closeEvent(self, event):
        chats = [name for name in config.get_chats().keys()]
        for item in self.page_classes():
            try:
                if item.chat.name in chats:
                    chat_data = item.close_event()
                    config.update_chat(chat_data.get_data())
            except Exception as exc:
                print(exc)
        
        config.save()

    def set_all_null_ContentsMargins(self):
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.LeftMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.RightMenuLayout.setContentsMargins(0, 0, 0, 0)

    def _update_css(self):
        self.css = open(config.get_theme(), "r").read()
        self.setStyleSheet(self.css)

    def _load_policy(self):
        self.setWindowTitle(WINDOW_NAME)
        self.resize(WINDOW_SIZE)

    def change_theme(self):
        if config.get_theme_index() == 0:
            config.change_theme(1)
        else:
            config.change_theme(0)
        self._update_css()

    def append_page(self, page: ChatWindow):
        self.pages.append(page)

        new_btn = generate_button(
            self.stackLayout,
            self.pages.index(page),
            page.chat.name,
            delete=True
            )
        
        self.buttons.append(new_btn)
        self.LeftMenuLayout.addWidget(self.buttons[-1])


        self.stackLayout.addWidget(
            self.page_classes()[-1].return_widget()
        )

    def load_chats(self):
        chats = config.get_chats()
        names = [item.chat.name for item in self.page_classes()]
        for item in chats:
            if item not in names:
                self.append_page(ChatWindow(item))

    def create_chat(self, name: str):
        if name not in [item.chat.name for item in self.page_classes()]:
            chat = ChatWindow(name)
            self.append_page(chat)


application = QApplication(sys.argv)

main_window = MainWindow()
main_window.show()

application.exec()