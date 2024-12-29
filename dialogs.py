from PySide6.QtCore import Qt

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWidgets import QLabel, QTextEdit
from PySide6.QtWidgets import QDialog, QDialogButtonBox

class Creator(QDialog):

    def __init__(self, get_func) -> None:
        QDialog.__init__(self)
        
        self.widget = QWidget()
        self.mainlayout = QVBoxLayout(self.widget)

        self.label = QLabel("Enter name for you chat")
        self.textEdit = QTextEdit()
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.buttonbox = QDialogButtonBox()
        self.buttonbox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonbox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.buttonbox.accepted.connect(lambda: self.accepted(get_func))

        self.mainlayout.addWidget(self.label)
        self.mainlayout.addWidget(self.textEdit)
        self.mainlayout.addWidget(self.buttonbox)

        self.setLayout(self.mainlayout)

    def accepted(self, get_func):
        name = self.textEdit.toPlainText()
        get_func(name)
        self.textEdit.setPlainText("")

        self.close()