from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import QStatusBar

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtWidgets import QPushButton, QLabel

from PySide6.QtWidgets import QMainWindow, QSizePolicy

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout,  QMessageBox, QLayoutItem

from config import Config
from chat import ChatWindow
from dialogs import Creator

from toggle_anim import AnimatedToggle
from widget_anim import WidgetCloseAnimation

WINDOW_NAME = "Test chat"
WINDOW_SIZE = QSize(800, 700)
WINDOW_FLAG = Qt.FramelessWindowHint

config = Config()

def generate_button(
        stacked_layout: QStackedLayout,
        stacked_layout_widget: QWidget,
        page_delete_function: object,
        index: int,
        page_name: str,
        delete: bool = False
        ) -> QWidget:
    
    def pressed():
        stacked_layout.setCurrentIndex(index)

    def deleted(widget: QWidget, layout: QHBoxLayout):
        config.delete_chat(page_name)
        stacked_layout.removeWidget(stacked_layout_widget)
        layout.removeWidget(widget)
        widget.deleteLater()
        page_delete_function(page_name)

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

class SideMenu:

    def __init__(self) -> None:

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("side_menu")
        self.main_frame.setLayout(self.main_layout)

    def append_widget(self, widget: QWidget): self.main_layout.addWidget(widget)
    def append_item(self, item: QLayoutItem): self.main_layout.addItem(item)

    def get_side_qframe(self) -> QFrame: return self.main_frame
    def get_layout(self) -> QVBoxLayout: return self.main_layout

class ChatsManager(QMainWindow):

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.create_active = False

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

        self.side_menu = SideMenu()

        #self.LeftMenuFrame = QFrame()
        #self.LeftMenuFrame.setObjectName("left_menu_frame")
        #self.LeftMenuLayout = QVBoxLayout()
        #self.LeftMenuFrame.setLayout(self.LeftMenuLayout)
        #self.LeftMenuLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.RightMenuFrame = QFrame()
        self.RightMenuFrame.setObjectName("right_menu_frame")
        self.RightMenuLayout = QVBoxLayout()
        self.RightMenuFrame.setLayout(self.pageLayout)
        self.RightMenuLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.anim = WidgetCloseAnimation(self.side_menu.get_side_qframe(), self.RightMenuFrame)

        self.mainlayout.addWidget(self.side_menu.get_side_qframe())
        self.mainlayout.addWidget(self.RightMenuFrame)

        self.theme_label = QLabel("Light theme: ")
        self.theme_toggle = AnimatedToggle()
        self.theme_toggle.setFixedSize(self.theme_toggle.sizeHint())
        self.theme_toggle.stateChanged.connect(self.change_theme)

        self.new_chat_btn = QPushButton("Create new chat")
        self.new_chat_btn.pressed.connect(self.creator.show)

        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("status_bar")
        self.status_bar.addPermanentWidget(self.theme_label)
        self.status_bar.addPermanentWidget(self.theme_toggle)
        self.status_bar.addWidget(self.new_chat_btn)
        self.status_bar.addWidget(self.anim.get_button())

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
        event.accept()

    def set_all_null_ContentsMargins(self):
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        #self.LeftMenuLayout.setContentsMargins(0, 0, 0, 0)
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
            stacked_layout=self.stackLayout,
            stacked_layout_widget=self.page_classes()[-1].return_widget(),
            page_delete_function=self.delete_chat,
            index=self.pages.index(page),
            page_name=page.chat.name,
            delete=True
            )
        
        self.buttons.append(new_btn)
        self.side_menu.append_widget(self.buttons[-1])
        #self.LeftMenuLayout.addWidget(self.buttons[-1])

        self.stackLayout.addWidget(
            self.page_classes()[-1].return_widget()
        )

    def load_chats(self):
        chats = config.get_chats()
        names = [item.chat.name for item in self.page_classes()]
        for item in chats:
            if item not in names:
                chat = ChatWindow(item)
                self.append_page(chat)

    def create_chat(self, name: str):
        if name not in [item.chat.name for item in self.page_classes()]:
            chat = ChatWindow(name)
            self.append_page(chat)
        else:
            message = QMessageBox.question(
                self,
                "Ошибка", "Чат с таким именем уже существует",
                QMessageBox.Ok
            )
            return

        if self.create_active:
            self.show()
            self.create_active = False

        index = self.pages.index(chat)
        self.stackLayout.setCurrentIndex(index)

    def delete_chat(self, page_name: str):
        try:
            for item in self.page_classes():
                if item.chat.name == page_name:
                    self.pages.remove(item)
                    break
        except:
            print("Not found chat to remove")

    def show_chat_creator(self):
        self.creator.show()
        self.create_active = True