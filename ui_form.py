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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 900)
        MainWindow.setMinimumSize(QSize(1200, 900))
        MainWindow.setMaximumSize(QSize(1200, 900))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(1200, 900))
        self.centralwidget.setMaximumSize(QSize(1200, 900))
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 190, 1181, 701))
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

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 140, 1181, 41))
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

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Keogh's Port App by CyberSmiths", None))
        self.FilePickLabel.setText(QCoreApplication.translate("MainWindow", u"Enter a manifest (must be .txt):", None))
        self.FilePickButton.setText(QCoreApplication.translate("MainWindow", u"Choose a file", None))
    # retranslateUi

