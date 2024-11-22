import sys

from ollama import Client
from PySide6.QtWidgets import QLabel, QSpacerItem
from PySide6.QtCore import QThread, Signal, Slot

from ui import *

from config import Config

MODEL = "llama3.1"

ROLE = "role"
CONTENT = "content"

USER = "user"
SYSTEM = "system"
ASSISTANT = "assistant"

class Backend(QThread):

    signal = Signal(str, bool)
    max_range = 500

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        for dict_obj in self.max_range:
            self.signal.emit(dict_obj['message']['content'], dict_obj['done'])

    def set_max_range(self, value):
        self.max_range = value

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet(open("style.css", "r").read())

        self.config = Config()

        self.ollamaResponse = ""
        self.Lasttext = None
        self.chat_history = []

        self.ollama_client = Client()
        self.backend = Backend()

        self.backend.signal.connect(self.draw_generate)

        self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        self.ui.InputTextWidget.setPlaceholderText("Введите запрос..\Enter request..")
        self.ui.SendTextBtn.clicked.connect(self._send)

        self.show()

    def _send(self):
        print("Thread is Running:", self.backend.isRunning())
        if self.backend.isRunning(): return

        self.Lasttext = self.ui.InputTextWidget.toPlainText()
        if self.Lasttext in ["", " ", None]: return
        self.ui.InputTextWidget.setPlainText("")

        messageFrame = QFrame(self.ui.scrollAreaWidgetContents)
        layout = QHBoxLayout(messageFrame)
        self.label = QLabel(messageFrame)
        self.label.setWordWrap(True)

        self.ui.verticalLayout_8.addWidget(messageFrame)

        layout.addItem(self.spacer)
        layout.addWidget(self.label)

        self.label.setText(self.Lasttext)

        start_value = self.ui.scrollArea.verticalScrollBar().value()
        for i in range(50): self.ui.scrollArea.verticalScrollBar().setValue(start_value+i)

        history = self.chat_history.copy()
        request = [{ROLE: USER, CONTENT: self.Lasttext}]

        generator = self.ollama_client.chat(
            model=MODEL,
            messages=history+request,
            stream=True
        )
        request[0][ROLE] = SYSTEM
        self.chat_history.append(request[0])

        self.backend.set_max_range(generator)
        self.response_frame()
        self.backend.start()

    def response_frame(self):
        responseFrame = QFrame(self.ui.scrollAreaWidgetContents)
        layout = QHBoxLayout(responseFrame)
        self.label = QLabel(responseFrame)
        self.label.setWordWrap(True)

        self.ui.verticalLayout_8.addWidget(responseFrame)
        
        layout.addWidget(self.label)
        layout.addItem(self.spacer)

    @Slot(str, bool)
    def draw_generate(self, char, done):
        print(char, end="", flush=True)
        if done:
            print("\n")
            self.backend.terminate()
            print("Thread is Running:", self.backend.isRunning())
            self.ollamaResponse = ""
            return

        self.ollamaResponse += char

        self.label.setText(self.ollamaResponse)


app = QApplication(sys.argv)
window = MainWindow()
app.exec()