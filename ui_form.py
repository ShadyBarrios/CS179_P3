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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(934, 700)
        MainWindow.setMinimumSize(QSize(933, 700))
        MainWindow.setMaximumSize(QSize(934, 700))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(934, 700))
        self.centralwidget.setMaximumSize(QSize(934, 700))
        self.AllPages = QStackedWidget(self.centralwidget)
        self.AllPages.setObjectName(u"AllPages")
        self.AllPages.setGeometry(QRect(0, 0, 934, 700))
        self.AllPages.setMinimumSize(QSize(934, 700))
        self.AllPages.setMaximumSize(QSize(934, 700))
        self.ShipGridPage = QWidget()
        self.ShipGridPage.setObjectName(u"ShipGridPage")
        self.verticalLayoutWidget = QWidget(self.ShipGridPage)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 190, 911, 501))
        self.ShipGridLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.ShipGridLayout.setObjectName(u"ShipGridLayout")
        self.ShipGridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.ShipGridLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ShipGrid = QGridLayout()
        self.ShipGrid.setObjectName(u"ShipGrid")

        self.horizontalLayout.addLayout(self.ShipGrid)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.ShipGridLayout.addLayout(self.horizontalLayout)

        self.horizontalLayoutWidget_3 = QWidget(self.ShipGridPage)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(30, 10, 871, 171))
        self.MessageLayouts = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.MessageLayouts.setObjectName(u"MessageLayouts")
        self.MessageLayouts.setContentsMargins(0, 0, 0, 0)
        self.MessagesLhsLayout = QVBoxLayout()
        self.MessagesLhsLayout.setObjectName(u"MessagesLhsLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.MessageLhsLayout = QHBoxLayout()
        self.MessageLhsLayout.setObjectName(u"MessageLhsLayout")
        self.MessageLhsLabel = QLabel(self.horizontalLayoutWidget_3)
        self.MessageLhsLabel.setObjectName(u"MessageLhsLabel")

        self.MessageLhsLayout.addWidget(self.MessageLhsLabel)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.MessageLhsLayout.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.MessageLhsLayout)

        self.ParkLayout = QHBoxLayout()
        self.ParkLayout.setObjectName(u"ParkLayout")
        self.ParkLabel = QLabel(self.horizontalLayoutWidget_3)
        self.ParkLabel.setObjectName(u"ParkLabel")

        self.ParkLayout.addWidget(self.ParkLabel)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ParkLayout.addItem(self.horizontalSpacer_10)

        self.ContinueLayout = QHBoxLayout()
        self.ContinueLayout.setObjectName(u"ContinueLayout")
        self.ContinueButton = QPushButton(self.horizontalLayoutWidget_3)
        self.ContinueButton.setObjectName(u"ContinueButton")

        self.ContinueLayout.addWidget(self.ContinueButton)

        self.WhenDoneLabel = QLabel(self.horizontalLayoutWidget_3)
        self.WhenDoneLabel.setObjectName(u"WhenDoneLabel")

        self.ContinueLayout.addWidget(self.WhenDoneLabel)


        self.ParkLayout.addLayout(self.ContinueLayout)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ParkLayout.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.ParkLayout)


        self.MessagesLhsLayout.addLayout(self.verticalLayout_4)


        self.MessageLayouts.addLayout(self.MessagesLhsLayout)

        self.MessagesRhsLayout = QVBoxLayout()
        self.MessagesRhsLayout.setObjectName(u"MessagesRhsLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.MoveHistoryLabel = QLabel(self.horizontalLayoutWidget_3)
        self.MoveHistoryLabel.setObjectName(u"MoveHistoryLabel")

        self.verticalLayout_5.addWidget(self.MoveHistoryLabel)

        self.scrollArea = QScrollArea(self.horizontalLayoutWidget_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 425, 141))
        self.horizontalLayoutWidget_5 = QWidget(self.scrollAreaWidgetContents)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(9, 9, 561, 121))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.PreviousMovesLabel = QLabel(self.horizontalLayoutWidget_5)
        self.PreviousMovesLabel.setObjectName(u"PreviousMovesLabel")

        self.horizontalLayout_2.addWidget(self.PreviousMovesLabel)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.scrollArea)


        self.MessagesRhsLayout.addLayout(self.verticalLayout_5)


        self.MessageLayouts.addLayout(self.MessagesRhsLayout)

        self.AllPages.addWidget(self.ShipGridPage)
        self.FilePickPage = QWidget()
        self.FilePickPage.setObjectName(u"FilePickPage")
        self.horizontalLayoutWidget = QWidget(self.FilePickPage)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 80, 911, 41))
        self.FilePickLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.FilePickLayout.setObjectName(u"FilePickLayout")
        self.FilePickLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.FilePickLayout.addItem(self.horizontalSpacer_3)

        self.FilePickLabel = QLabel(self.horizontalLayoutWidget)
        self.FilePickLabel.setObjectName(u"FilePickLabel")

        self.FilePickLayout.addWidget(self.FilePickLabel)

        self.FilePickButton = QPushButton(self.horizontalLayoutWidget)
        self.FilePickButton.setObjectName(u"FilePickButton")

        self.FilePickLayout.addWidget(self.FilePickButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.FilePickLayout.addItem(self.horizontalSpacer_4)

        self.AllPages.addWidget(self.FilePickPage)
        self.ErrorPage = QWidget()
        self.ErrorPage.setObjectName(u"ErrorPage")
        self.horizontalLayoutWidget_2 = QWidget(self.ErrorPage)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 80, 911, 81))
        self.ErrorLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.ErrorLayout.setObjectName(u"ErrorLayout")
        self.ErrorLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ErrorLayout.addItem(self.horizontalSpacer_5)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ErrorLabel = QLabel(self.horizontalLayoutWidget_2)
        self.ErrorLabel.setObjectName(u"ErrorLabel")
        self.ErrorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.ErrorLabel)

        self.RestartButton = QPushButton(self.horizontalLayoutWidget_2)
        self.RestartButton.setObjectName(u"RestartButton")

        self.verticalLayout.addWidget(self.RestartButton)


        self.ErrorLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ErrorLayout.addItem(self.horizontalSpacer_6)

        self.AllPages.addWidget(self.ErrorPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.AllPages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Keogh's Port App by CyberSmiths", None))
        self.MessageLhsLabel.setText(QCoreApplication.translate("MainWindow", u"LHS Message", None))
        self.ParkLabel.setText(QCoreApplication.translate("MainWindow", u"Park", None))
        self.ContinueButton.setText(QCoreApplication.translate("MainWindow", u"Continue", None))
        self.WhenDoneLabel.setText(QCoreApplication.translate("MainWindow", u"when done", None))
        self.MoveHistoryLabel.setText(QCoreApplication.translate("MainWindow", u"Move History:", None))
        self.PreviousMovesLabel.setText(QCoreApplication.translate("MainWindow", u"Previous Moves", None))
        self.FilePickLabel.setText(QCoreApplication.translate("MainWindow", u"Enter a manifest (must be .txt):", None))
        self.FilePickButton.setText(QCoreApplication.translate("MainWindow", u"Choose a file", None))
        self.ErrorLabel.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.RestartButton.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
    # retranslateUi

