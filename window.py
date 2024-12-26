from PySide6.QtGui import QFont

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton, QLabel

from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QMessageBox, QSpacerItem

from app import ChatsManager

QSZ_POLICY = QSizePolicy.Policy

FONT = QFont("Sans Serif", 16)

TOP_EXPANDER = QSpacerItem(20, 40, QSZ_POLICY.Minimum, QSZ_POLICY.Preferred)
BOTTOM_EXPANDER = QSpacerItem(20, 40, QSZ_POLICY.Minimum, QSZ_POLICY.Expanding)


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        QMainWindow.__init__(self)

        self.chats = None

        self.construct()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены что хотите закрыть окно?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.chats is not None:
                self.chats.close()
            event.accept()
        else:
            event.ignore()

    def __init_chats_window(self):
        self.chats = ChatsManager()
        # Настроить передачу настроек из конфигурационного файла аля для статикмтд

    def _create_new_chat(self):
        if self.chats is None:
            self.__init_chats_window()
        self.chats.show_chat_creator()
        self.hide()

    def _continue_chat(self):
        if self.chats is None:
            self.__init_chats_window()
        if not self.chats.isVisible():
            self.chats.show()
        else:
            self.chats.showNormal()
        self.hide()

    def _open_settings(self): pass
    
    def _open_about_app(self): pass

    def __construct_main_container(self) -> QWidget:
        main_container = QWidget()
        layout = QVBoxLayout(main_container)

        label_widget = QWidget()
        menu_widget = QWidget()

        label_cont_layout = QVBoxLayout(label_widget)
        menu_cont_layout = QVBoxLayout(menu_widget)

        layout.addItem(TOP_EXPANDER)
        layout.addWidget(label_widget, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(menu_widget, 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addItem(BOTTOM_EXPANDER)

        welcome_label = QLabel("Добро пожаловать!")
        welcome_label.setFont(FONT)

        label_cont_layout.addWidget(welcome_label)

        create_chat_button = QPushButton("Создать чат")
        continue_button = QPushButton("Продолжить")
        settings_app_button = QPushButton("Настройки")
        about_app_button = QPushButton("О программе")

        create_chat_button.clicked.connect(self._create_new_chat)
        continue_button.clicked.connect(self._continue_chat)
        #settings_app_button.clicked.connect(self._open_settings)
        #about_app_button.clicked.connect(self._open_about_app)

        menu_cont_layout.addWidget(create_chat_button)
        menu_cont_layout.addWidget(continue_button)
        #menu_cont_layout.addWidget(settings_app_button)
        #menu_cont_layout.addWidget(about_app_button)

        return main_container
    
    #def __construct_side_containers(self) -> tuple[QWidget, QWidget]:
    #    top_side_container = QWidget()
    #    bottom_side_container = QWidget()
    #
    #    top_side_layout = QHBoxLayout(top_side_container)
    #    bottom_side_layout = QHBoxLayout(bottom_side_container)

    #    return (top_side_container, bottom_side_container)
    
    def construct(self):
    #    side_containers = self.__construct_side_containers()
        main_containers = self.__construct_main_container()

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

    #    self.main_layout.addWidget(side_containers[0]) # top_side_cont
        self.main_layout.addWidget(main_containers)
    #    self.main_layout.addWidget(side_containers[1]) # bottom_side_cont

        self.setCentralWidget(self.main_widget)


application = QApplication()

main_window = MainWindow()
main_window.show()

application.exec()