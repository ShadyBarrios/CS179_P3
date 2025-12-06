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
    QMainWindow, QPlainTextEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)

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
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.MessagesLhsLayout.addItem(self.verticalSpacer_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.MessageLhsLayout = QHBoxLayout()
        self.MessageLhsLayout.setObjectName(u"MessageLhsLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.SolutionMetadataLabel = QLabel(self.horizontalLayoutWidget_3)
        self.SolutionMetadataLabel.setObjectName(u"SolutionMetadataLabel")

        self.verticalLayout.addWidget(self.SolutionMetadataLabel)

        self.MessageLhsLabel = QLabel(self.horizontalLayoutWidget_3)
        self.MessageLhsLabel.setObjectName(u"MessageLhsLabel")

        self.verticalLayout.addWidget(self.MessageLhsLabel)


        self.MessageLhsLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.MessageLhsLayout.addItem(self.horizontalSpacer_9)


        self.verticalLayout_4.addLayout(self.MessageLhsLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.ParkLayout = QHBoxLayout()
        self.ParkLayout.setObjectName(u"ParkLayout")
        self.ParkLabelLayout = QVBoxLayout()
        self.ParkLabelLayout.setObjectName(u"ParkLabelLayout")
        self.ParkLabel = QLabel(self.horizontalLayoutWidget_3)
        self.ParkLabel.setObjectName(u"ParkLabel")

        self.ParkLabelLayout.addWidget(self.ParkLabel)


        self.ParkLayout.addLayout(self.ParkLabelLayout)

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

        self.ToCommentLayout = QHBoxLayout()
        self.ToCommentLayout.setObjectName(u"ToCommentLayout")
        self.ToCommentButton = QPushButton(self.horizontalLayoutWidget_3)
        self.ToCommentButton.setObjectName(u"ToCommentButton")

        self.ToCommentLayout.addWidget(self.ToCommentButton)


        self.ParkLayout.addLayout(self.ToCommentLayout)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ParkLayout.addItem(self.horizontalSpacer_20)


        self.verticalLayout_4.addLayout(self.ParkLayout)


        self.MessagesLhsLayout.addLayout(self.verticalLayout_4)


        self.MessageLayouts.addLayout(self.MessagesLhsLayout)

        self.MessagesRhsLayout = QVBoxLayout()
        self.MessagesRhsLayout.setObjectName(u"MessagesRhsLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.MoveHistoryLabel = QLabel(self.horizontalLayoutWidget_3)
        self.MoveHistoryLabel.setObjectName(u"MoveHistoryLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MoveHistoryLabel.sizePolicy().hasHeightForWidth())
        self.MoveHistoryLabel.setSizePolicy(sizePolicy)

        self.verticalLayout_5.addWidget(self.MoveHistoryLabel)

        self.PreviousMovesScrollArea = QScrollArea(self.horizontalLayoutWidget_3)
        self.PreviousMovesScrollArea.setObjectName(u"PreviousMovesScrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PreviousMovesScrollArea.sizePolicy().hasHeightForWidth())
        self.PreviousMovesScrollArea.setSizePolicy(sizePolicy1)
        self.PreviousMovesScrollArea.setMinimumSize(QSize(0, 125))
        self.PreviousMovesScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 425, 141))
        self.PreviousMovesLabel = QLabel(self.scrollAreaWidgetContents)
        self.PreviousMovesLabel.setObjectName(u"PreviousMovesLabel")
        self.PreviousMovesLabel.setGeometry(QRect(10, 10, 411, 131))
        sizePolicy1.setHeightForWidth(self.PreviousMovesLabel.sizePolicy().hasHeightForWidth())
        self.PreviousMovesLabel.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(8)
        self.PreviousMovesLabel.setFont(font)
        self.PreviousMovesScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.PreviousMovesScrollArea)


        self.MessagesRhsLayout.addLayout(self.verticalLayout_5)


        self.MessageLayouts.addLayout(self.MessagesRhsLayout)

        self.AllPages.addWidget(self.ShipGridPage)
        self.CommentPage = QWidget()
        self.CommentPage.setObjectName(u"CommentPage")
        self.verticalLayoutWidget_2 = QWidget(self.CommentPage)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(9, 93, 911, 461))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_10)

        self.InsertCommentLabel = QLabel(self.verticalLayoutWidget_2)
        self.InsertCommentLabel.setObjectName(u"InsertCommentLabel")

        self.horizontalLayout_4.addWidget(self.InsertCommentLabel)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_11)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.CommentInput = QPlainTextEdit(self.verticalLayoutWidget_2)
        self.CommentInput.setObjectName(u"CommentInput")

        self.horizontalLayout_3.addWidget(self.CommentInput)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_12)

        self.LogCommentButton = QPushButton(self.verticalLayoutWidget_2)
        self.LogCommentButton.setObjectName(u"LogCommentButton")

        self.horizontalLayout_5.addWidget(self.LogCommentButton)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_21)

        self.CancelCommentButton = QPushButton(self.verticalLayoutWidget_2)
        self.CancelCommentButton.setObjectName(u"CancelCommentButton")

        self.horizontalLayout_5.addWidget(self.CancelCommentButton)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_13)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.AllPages.addWidget(self.CommentPage)
        self.FinishedPage = QWidget()
        self.FinishedPage.setObjectName(u"FinishedPage")
        self.verticalLayoutWidget_3 = QWidget(self.FinishedPage)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 29, 911, 141))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_16)

        self.SuccessMessageLabel = QLabel(self.verticalLayoutWidget_3)
        self.SuccessMessageLabel.setObjectName(u"SuccessMessageLabel")

        self.horizontalLayout_6.addWidget(self.SuccessMessageLabel)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_17)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_14)

        self.SuccessRestartButton = QPushButton(self.verticalLayoutWidget_3)
        self.SuccessRestartButton.setObjectName(u"SuccessRestartButton")

        self.horizontalLayout_7.addWidget(self.SuccessRestartButton)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_15)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.AllPages.addWidget(self.FinishedPage)
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
        self.verticalLayoutWidget_4 = QWidget(self.ErrorPage)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 79, 911, 81))
        self.ErrorLayout = QVBoxLayout(self.verticalLayoutWidget_4)
        self.ErrorLayout.setObjectName(u"ErrorLayout")
        self.ErrorLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.ErrorLabel = QLabel(self.verticalLayoutWidget_4)
        self.ErrorLabel.setObjectName(u"ErrorLabel")
        self.ErrorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ErrorLabel)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)


        self.ErrorLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_18)

        self.ErrorRestartButton = QPushButton(self.verticalLayoutWidget_4)
        self.ErrorRestartButton.setObjectName(u"ErrorRestartButton")

        self.horizontalLayout_9.addWidget(self.ErrorRestartButton)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_19)


        self.ErrorLayout.addLayout(self.horizontalLayout_9)

        self.AllPages.addWidget(self.ErrorPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.AllPages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Keogh's Port App by CyberSmiths", None))
        self.SolutionMetadataLabel.setText("")
        self.MessageLhsLabel.setText("")
        self.ParkLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ContinueButton.setText(QCoreApplication.translate("MainWindow", u"Continue", None))
        self.WhenDoneLabel.setText(QCoreApplication.translate("MainWindow", u"when done", None))
        self.ToCommentButton.setText(QCoreApplication.translate("MainWindow", u"Log Comment", None))
        self.MoveHistoryLabel.setText(QCoreApplication.translate("MainWindow", u"Move History:", None))
        self.PreviousMovesLabel.setText("")
        self.InsertCommentLabel.setText(QCoreApplication.translate("MainWindow", u"Insert Comment Here", None))
        self.LogCommentButton.setText(QCoreApplication.translate("MainWindow", u"Log Comment", None))
        self.CancelCommentButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.SuccessMessageLabel.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.SuccessRestartButton.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
        self.FilePickLabel.setText(QCoreApplication.translate("MainWindow", u"Enter a manifest (must be .txt):", None))
        self.FilePickButton.setText(QCoreApplication.translate("MainWindow", u"Choose a file", None))
        self.ErrorLabel.setText(QCoreApplication.translate("MainWindow", u"Error", None))
        self.ErrorRestartButton.setText(QCoreApplication.translate("MainWindow", u"Restart", None))
    # retranslateUi

