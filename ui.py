# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'testaTrMjS.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(807, 666)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.MainContainer = QWidget(self.centralwidget)
        self.MainContainer.setObjectName(u"MainContainer")
        self.verticalLayout_2 = QVBoxLayout(self.MainContainer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.AOut = QFrame(self.MainContainer)
        self.AOut.setObjectName(u"AOut")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AOut.sizePolicy().hasHeightForWidth())
        self.AOut.setSizePolicy(sizePolicy)
        self.AOut.setFrameShape(QFrame.Shape.StyledPanel)
        self.AOut.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.AOut)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.AOut)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 785, 542))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)


        self.verticalLayout_2.addWidget(self.AOut)

        self.BInput = QFrame(self.MainContainer)
        self.BInput.setObjectName(u"BInput")
        sizePolicy.setHeightForWidth(self.BInput.sizePolicy().hasHeightForWidth())
        self.BInput.setSizePolicy(sizePolicy)
        self.BInput.setMinimumSize(QSize(0, 32))
        self.BInput.setMaximumSize(QSize(16777215, 96))
        self.BInput.setFrameShape(QFrame.Shape.StyledPanel)
        self.BInput.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.BInput)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.InputTextWidget = QPlainTextEdit(self.BInput)
        self.InputTextWidget.setObjectName(u"InputTextWidget")
        self.InputTextWidget.setMinimumSize(QSize(0, 32))
        self.InputTextWidget.setMaximumSize(QSize(16777215, 96))

        self.horizontalLayout.addWidget(self.InputTextWidget)

        self.SendImageBtn = QPushButton(self.BInput)
        self.SendImageBtn.setObjectName(u"SendImageBtn")

        self.horizontalLayout.addWidget(self.SendImageBtn)

        self.SendTextBtn = QPushButton(self.BInput)
        self.SendTextBtn.setObjectName(u"SendTextBtn")

        self.horizontalLayout.addWidget(self.SendTextBtn)


        self.verticalLayout_2.addWidget(self.BInput)


        self.verticalLayout.addWidget(self.MainContainer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SendImageBtn.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435", None))
        self.SendTextBtn.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c", None))
    # retranslateUi

