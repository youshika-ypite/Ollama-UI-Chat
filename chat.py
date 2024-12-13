from ollama_term import Ollama
from config import PageData, Config
from message import generate_message_widget

from PySide6.QtWidgets import QPushButton, QPlainTextEdit
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea
from PySide6.QtWidgets import QSizePolicy, QGridLayout, QLayout

from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QThread, Signal, Slot


ICON_SIZE = QSize(24, 24)

config = Config()

class Backend(QThread):

    signal = Signal(str, bool)
    generator = None

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def run(self):
        print("||------------------------||")
        message = ""
        if self.generator is None:
            print("Please set generator obj")
            return
        print("||\033[32m QThread is running\033[0m | ", self.name)
        try:
            for dict_obj in self.generator:
                
                if dict_obj['done']:
                    timers = [
                        round(int(dict_obj["total_duration"])/1000000000, 3),
                        round(int(dict_obj["load_duration"] )/1000000000, 3),
                        round(int(dict_obj["eval_duration"] )/1000000000, 3)
                        ]
                    print("||------------------------||")
                    print("|| \033[33mStream statistic:\033[0m")
                    print("|| INFO || model:", dict_obj["model"])
                    print("|| INFO || role:", dict_obj["message"]["role"])
                    print("|| INFO || message:", message.replace("\n", ""))
                    print("|| INFO || total duration:", timers[0], "s.")
                    print("|| INFO || load duration:", timers[1], "s.")
                    print("|| INFO || eval count:", dict_obj["eval_count"])
                    print("|| INFO || eval duration:", timers[2], "s.")
                    print("||------------------------||")
                    print("|| \033[31mQThread stopped\033[0m | Reason:", dict_obj["done_reason"])
                    print("||------------------------||")

                self.signal.emit(dict_obj['message']['content'], dict_obj["done"])
                message += dict_obj['message']['content']
        except Exception as exc:
            print("||------------------------||")
            print("||\033[31m QThread stopped\033[0m")
            print("|| Reason: \033[31m", exc, end="\033[0m\n")
            print("||------------------------||")
            self.signal.emit(exc, True)

    def set_data(self, generator):
        self.generator = generator


class ChatWindow:

    def __init__(self, name: str = "StdPageName"):
        #QMainWindow.__init__(self)

        self.chat = PageData(name)
        result = config.search(self.chat.name)
        if result is None:
            config.update_chat(self.chat.get_data())
        else:
            self.chat.set_data(result)
        
        _chat_history = self.chat.get_chat_history()

        self.ollama_chat = Ollama()
        self.ollama_chat.set_chat_history(_chat_history)
        self.generator_backend = Backend(self.chat.name)
        self.generator_backend.signal.connect(self.draw_generated)
        
        self.widget = QWidget()
        self.widget.setContentsMargins(0, 0, 0, 0)
        self.widget.setObjectName("main_widget")
        # First-half for messages
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.grid_widget)
        self.scroll_area.setObjectName("scroll_area")

        self.vscroll_bar = self.scroll_area.verticalScrollBar()
        self.vscroll_bar.rangeChanged.connect(self.scroll_bottom)
        # Second-half for input
        self.text_input_widget = QPlainTextEdit()
        self.text_input_widget.setObjectName("text_input")
        self.text_input_widget.setMaximumHeight(75)
        self.text_input_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        
        self.send_message_button = QPushButton("Send")
        self.send_message_button.setObjectName("send_btn")
        #self.send_message_button.setIcon(self.dict_icn_css["SEND_ICON"])
        #self.send_message_button.setIconSize(ICON_SIZE)
        self.send_message_button.clicked.connect(self.send_message)
        self.send_message_button.setShortcut(Qt.Key.Key_Enter)
        self.send_message_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

        self.send_frame_layout = QHBoxLayout()
        self.send_frame = QFrame()
        self.send_frame.setLayout(self.send_frame_layout)
        self.send_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.send_frame_layout.addWidget(self.text_input_widget)
        self.send_frame_layout.addWidget(self.send_message_button)
        # Layout sets
        self.mainlayout = QVBoxLayout(self.widget)
        self.mainlayout.setObjectName("mainlayout")
        self.mainlayout.addWidget(self.scroll_area)
        self.mainlayout.addWidget(self.send_frame)

        self.messages = []
        self.last_response = ""

        # Load and draw message from memory
        self.load_messages(_chat_history)
        self.draw_messages()

    def load_messages(self, _chat_history: list[dict[str, any]]):
        for item in _chat_history:
            if item["role"] == "assistant":
                self.append_message_widget()
            elif item["role"] == "system":
                self.append_message_widget(True)
            # QLabel setText
            self.messages[-1][1].setText(item["content"])

    def draw_messages(self):
        for item in self.messages:
            self.draw_last_message(item[0])

    def draw_last_message(self, last_message_widget: QWidget):
        self.grid_layout.addWidget(last_message_widget)

    def append_message_widget(self, user=False):
        widget_and_label = generate_message_widget(user)
        self.messages.append(widget_and_label)

    def send_message(self):
        self.append_message_widget() # Ollama response widget
        self.append_message_widget(True) # User request widget
        
        message = self.text_input_widget.toPlainText()
        if message in ["", " ", None]: return
        self.send_message_button.setEnabled(False)
        self.text_input_widget.setPlainText("")

        # QLabel setText
        self.messages[-1][1].setText(message)

        self.draw_last_message(self.messages[-1][0])
        self.draw_last_message(self.messages[-2][0])

        generator = self.ollama_chat.send_message(message)
        self.generator_backend.set_data(generator)
        self.generator_backend.start()

    @Slot(str, bool)
    def draw_generated(self, char: str, done: bool):
        if done:
            self.ollama_chat.append_response(self.last_response)
            self.last_response = ""

            self.generator_backend.terminate()
            
            self.send_message_button.setEnabled(True)

            return
        
        self.last_response += char
        self.messages[-2][1].setText(self.last_response)

    @Slot(int, int)
    def scroll_bottom(self, minimum, maximum):
        self.vscroll_bar.setValue(maximum)

    def close_event(self) -> PageData:
        chat_history = self.ollama_chat.get_chat_history()
        self.chat.set_chat_history(chat_history)

        return self.chat

    def return_widget(self):
        return self.widget