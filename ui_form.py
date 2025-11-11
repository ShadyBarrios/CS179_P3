# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(230, 160, 331, 85))
        self.MainVBox = QVBoxLayout(self.verticalLayoutWidget)
        self.MainVBox.setObjectName(u"MainVBox")
        self.MainVBox.setContentsMargins(0, 0, 0, 0)
        self.CommunicatorLabel = QLabel(self.verticalLayoutWidget)
        self.CommunicatorLabel.setObjectName(u"CommunicatorLabel")
        self.CommunicatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.CommunicatorLabel.setWordWrap(True)

        self.MainVBox.addWidget(self.CommunicatorLabel)

        self.FilePickButton = QPushButton(self.verticalLayoutWidget)
        self.FilePickButton.setObjectName(u"FilePickButton")

        self.MainVBox.addWidget(self.FilePickButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.CommunicatorLabel.setText(QCoreApplication.translate("MainWindow", u"BOO! Choose a txt file", None))
        self.FilePickButton.setText(QCoreApplication.translate("MainWindow", u"Click me", None))
    # retranslateUi

