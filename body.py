from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import QWidget, QFrame
from PySide6.QtWidgets import QPushButton, QLabel

from PySide6.QtWidgets import QMainWindow, QSizePolicy

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedLayout,  QMessageBox, QSpacerItem

from config import Config
from dialogs import Creator
from chat import ChatWindow

from toggle_anim import AnimatedToggle
from widget_anim import WidgetCloseAnimation

HORIZONTAL_EXPANDER = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

WINDOW_NAME = "Main app body"
WINDOW_SIZE = QSize(800, 700)

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

class TopMenu:

    def __init__(
            self,
            create_chat_function: object,
            css_update_function: object,
            side_bar_hide_function: object,
        ):
        
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("top_menu")
        self.main_frame.setLayout(self.main_layout)

        self.create_chat_btn = QPushButton("Создать чат")
        self.create_chat_btn.pressed.connect(create_chat_function)

        self.hide_side_bar_btn = QPushButton("Скрыть/Показать меню")
        self.hide_side_bar_btn.pressed.connect(side_bar_hide_function)

        self.css_update_lbl = QLabel("Свтелая тема - ")
        self.css_update_btn = AnimatedToggle()
        self.css_update_btn.setFixedSize(self.css_update_btn.sizeHint())
        self.css_update_btn.stateChanged.connect(css_update_function)

        self.main_layout.addWidget(self.hide_side_bar_btn)
        self.main_layout.addItem(HORIZONTAL_EXPANDER)
        self.main_layout.addWidget(self.create_chat_btn)
        self.main_layout.addItem(HORIZONTAL_EXPANDER)
        self.main_layout.addWidget(self.css_update_lbl)
        self.main_layout.addWidget(self.css_update_btn)

    def get_top_frame(self) -> QFrame: return self.main_frame

class SideMenu:

    def __init__(self) -> None:

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_frame = QFrame()
        self.main_frame.setObjectName("side_menu")
        self.main_frame.setLayout(self.main_layout)

    def append_widget(self, widget: QWidget): self.main_layout.addWidget(widget)

    def get_side_frame(self) -> QFrame: return self.main_frame


class MainBody(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.creator = Creator(self.create_chat)
        self.create_active = False

        # main widget construct
        self.main_widget = QWidget()
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # Main body construct
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_frame = QFrame()
        self.body_frame.setObjectName("body")
        self.body_frame.setLayout(self.body_layout)

        # Stacked Layout
        self.stack_layout = QStackedLayout()
        self.page_layout = QVBoxLayout()
        self.page_layout.addLayout(self.stack_layout)
        self.right_body_frame = QFrame()
        self.right_body_frame.setObjectName("right-body")
        self.right_body_frame.setLayout(self.page_layout)
        # init side menu and animation
        self.side_menu = SideMenu()
        self.animation = WidgetCloseAnimation(self.side_menu.get_side_frame())

        # Append to body [[], []]
        self.body_layout.addWidget(self.side_menu.get_side_frame())
        self.body_layout.addWidget(self.right_body_frame)

        # init and append top frame & body frame
        self.top_menu = TopMenu(
            create_chat_function=self.creator.show,
            css_update_function=self.change_theme,
            side_bar_hide_function=self.animation.toggle_anim
        )
        # add all widgets to main
        self.main_layout.addWidget(self.top_menu.get_top_frame())
        self.main_layout.addWidget(self.body_frame)

        self.setCentralWidget(self.main_widget)

        #other

        self.pages = []
        self.buttons = []

        self._load_policy()
        self._update_css()
        self.load_chats()

    def _update_css(self):
        self.css = open(config.get_theme(), "r").read()
        self.setStyleSheet(self.css)
    
    def _load_policy(self):
        self.setWindowTitle(WINDOW_NAME)
        self.resize(WINDOW_SIZE)

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

    def page_classes(self) -> list[ChatWindow]: return self.pages
    def buttons_classes(self) -> list[QPushButton]: return self.buttons

    def change_theme(self):
        if config.get_theme_index() == 0:
            config.change_theme(1)
        else:
            config.change_theme(0)
        self._update_css()

    def append_page(self, page: ChatWindow):
        self.pages.append(page)

        new_btn = generate_button(
            stacked_layout=self.stack_layout,
            stacked_layout_widget=self.page_classes()[-1].return_widget(),
            page_delete_function=self.delete_chat,
            index=self.pages.index(page),
            page_name=page.chat.name,
            delete=True
            )
        
        self.buttons.append(new_btn)
        self.side_menu.append_widget(self.buttons[-1])

        self.stack_layout.addWidget(
            self.page_classes()[-1].return_widget()
        )

    def show_chat_creator(self):
        self.creator.show()
        self.create_active = True

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
        self.stack_layout.setCurrentIndex(index)

    def delete_chat(self, page_name: str):
        try:
            for item in self.page_classes():
                if item.chat.name == page_name:
                    self.pages.remove(item)
                    break
        except:
            print("Not found chat to remove")

    def load_chats(self):
        chats = config.get_chats()
        names = [item.chat.name for item in self.page_classes()]
        for item in chats:
            if item not in names:
                chat = ChatWindow(item)
                self.append_page(chat)