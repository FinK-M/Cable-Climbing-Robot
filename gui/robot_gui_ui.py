# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robot_gui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets, QtCore, QtGui


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 449)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 390))
        self.tabWidget.setObjectName("tabWidget")
        self.general = QtWidgets.QWidget()
        self.general.setObjectName("general")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.general)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.general)
        self.frame.setMinimumSize(QtCore.QSize(230, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.line_7 = QtWidgets.QFrame(self.frame)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_2.addWidget(self.line_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.start_run_button = QtWidgets.QPushButton(self.frame)
        self.start_run_button.setMinimumSize(QtCore.QSize(0, 36))
        self.start_run_button.setObjectName("start_run_button")
        self.horizontalLayout_5.addWidget(self.start_run_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.stop_run_button = QtWidgets.QPushButton(self.frame)
        self.stop_run_button.setEnabled(False)
        self.stop_run_button.setMinimumSize(QtCore.QSize(0, 36))
        self.stop_run_button.setAutoDefault(False)
        self.stop_run_button.setDefault(False)
        self.stop_run_button.setFlat(False)
        self.stop_run_button.setObjectName("stop_run_button")
        self.horizontalLayout_5.addWidget(self.stop_run_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.line_8 = QtWidgets.QFrame(self.frame)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_2.addWidget(self.line_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 36))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addWidget(self.frame)
        spacerItem3 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.position_frame = QtWidgets.QFrame(self.general)
        self.position_frame.setMinimumSize(QtCore.QSize(180, 0))
        self.position_frame.setMaximumSize(QtCore.QSize(16777215, 250))
        self.position_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.position_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.position_frame.setObjectName("position_frame")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.position_frame)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 161, 231))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.position_grid = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.position_grid.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.position_grid.setContentsMargins(5, 5, 5, 5)
        self.position_grid.setSpacing(10)
        self.position_grid.setObjectName("position_grid")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.position_grid.addWidget(self.label, 0, 1, 1, 1)
        self.error_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget_2)
        self.error_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.error_lcd.setObjectName("error_lcd")
        self.position_grid.addWidget(self.error_lcd, 4, 1, 1, 1)
        self.motor_pos_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget_2)
        self.motor_pos_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.motor_pos_lcd.setObjectName("motor_pos_lcd")
        self.position_grid.addWidget(self.motor_pos_lcd, 2, 1, 1, 1)
        self.actual_pos_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.actual_pos_label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.actual_pos_label.setObjectName("actual_pos_label")
        self.position_grid.addWidget(self.actual_pos_label, 3, 0, 1, 1)
        self.motor_pos_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.motor_pos_label.setMaximumSize(QtCore.QSize(40, 40))
        self.motor_pos_label.setObjectName("motor_pos_label")
        self.position_grid.addWidget(self.motor_pos_label, 2, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.position_grid.addWidget(self.line_3, 1, 1, 1, 1)
        self.actual_pos_lcd = QtWidgets.QLCDNumber(self.gridLayoutWidget_2)
        self.actual_pos_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.actual_pos_lcd.setObjectName("actual_pos_lcd")
        self.position_grid.addWidget(self.actual_pos_lcd, 3, 1, 1, 1)
        self.error_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.error_label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.error_label.setObjectName("error_label")
        self.position_grid.addWidget(self.error_label, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.gridLayoutWidget_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.position_grid.addWidget(self.line, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 36))
        self.pushButton.setObjectName("pushButton")
        self.position_grid.addWidget(self.pushButton, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.position_grid.addWidget(self.label_3, 5, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.position_frame)
        spacerItem4 = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.jog_frame = QtWidgets.QFrame(self.general)
        self.jog_frame.setMinimumSize(QtCore.QSize(100, 350))
        self.jog_frame.setMaximumSize(QtCore.QSize(100, 350))
        self.jog_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.jog_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.jog_frame.setObjectName("jog_frame")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.jog_frame)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 10, 81, 331))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.jog_vbox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.jog_vbox.setObjectName("jog_vbox")
        self.jog_header_label = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.jog_header_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.jog_header_label.setAlignment(QtCore.Qt.AlignCenter)
        self.jog_header_label.setObjectName("jog_header_label")
        self.jog_vbox.addWidget(self.jog_header_label)
        self.line_1 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.jog_vbox.addWidget(self.line_1)
        self.jog_up_fast = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.jog_up_fast.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/icons/PNG/32/Arrows/double_up-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jog_up_fast.setIcon(icon)
        self.jog_up_fast.setIconSize(QtCore.QSize(32, 32))
        self.jog_up_fast.setCheckable(True)
        self.jog_up_fast.setAutoExclusive(True)
        self.jog_up_fast.setObjectName("jog_up_fast")
        self.jog_vbox.addWidget(self.jog_up_fast)
        self.jog_up_slow = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.jog_up_slow.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/icons/PNG/32/Arrows/angle_up-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jog_up_slow.setIcon(icon1)
        self.jog_up_slow.setIconSize(QtCore.QSize(32, 32))
        self.jog_up_slow.setCheckable(True)
        self.jog_up_slow.setAutoExclusive(True)
        self.jog_up_slow.setObjectName("jog_up_slow")
        self.jog_vbox.addWidget(self.jog_up_slow)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.jog_vbox.addWidget(self.line_5)
        self.jog_stop = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.jog_stop.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:/icons/PNG/32/Transport/stop_sign-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jog_stop.setIcon(icon2)
        self.jog_stop.setIconSize(QtCore.QSize(32, 32))
        self.jog_stop.setCheckable(True)
        self.jog_stop.setAutoExclusive(True)
        self.jog_stop.setObjectName("jog_stop")
        self.jog_vbox.addWidget(self.jog_stop)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget_5)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.jog_vbox.addWidget(self.line_6)
        self.jog_down_slow = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.jog_down_slow.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:/icons/PNG/32/Arrows/angle_down-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jog_down_slow.setIcon(icon3)
        self.jog_down_slow.setIconSize(QtCore.QSize(32, 32))
        self.jog_down_slow.setCheckable(True)
        self.jog_down_slow.setAutoExclusive(True)
        self.jog_down_slow.setObjectName("jog_down_slow")
        self.jog_vbox.addWidget(self.jog_down_slow)
        self.jog_down_fast = QtWidgets.QPushButton(self.verticalLayoutWidget_5)
        self.jog_down_fast.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("C:/icons/PNG/32/Arrows/double_down-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.jog_down_fast.setIcon(icon4)
        self.jog_down_fast.setIconSize(QtCore.QSize(32, 32))
        self.jog_down_fast.setCheckable(True)
        self.jog_down_fast.setAutoExclusive(True)
        self.jog_down_fast.setObjectName("jog_down_fast")
        self.jog_vbox.addWidget(self.jog_down_fast)
        self.horizontalLayout_2.addWidget(self.jog_frame)
        self.tabWidget.addTab(self.general, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.settings)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.microstep_frame = QtWidgets.QFrame(self.settings)
        self.microstep_frame.setMaximumSize(QtCore.QSize(170, 190))
        self.microstep_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.microstep_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.microstep_frame.setObjectName("microstep_frame")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.microstep_frame)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(10, 10, 151, 171))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.microstep_vbox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.microstep_vbox.setContentsMargins(10, -1, 10, -1)
        self.microstep_vbox.setObjectName("microstep_vbox")
        self.microstep_label = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        self.microstep_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.microstep_label.setTextFormat(QtCore.Qt.AutoText)
        self.microstep_label.setAlignment(QtCore.Qt.AlignCenter)
        self.microstep_label.setObjectName("microstep_label")
        self.microstep_vbox.addWidget(self.microstep_label)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget_6)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.microstep_vbox.addWidget(self.line_2)
        self.microstep_1 = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.microstep_1.setObjectName("microstep_1")
        self.microstep_vbox.addWidget(self.microstep_1)
        self.microstep_2 = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.microstep_2.setChecked(True)
        self.microstep_2.setObjectName("microstep_2")
        self.microstep_vbox.addWidget(self.microstep_2)
        self.microstep_4 = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.microstep_4.setObjectName("microstep_4")
        self.microstep_vbox.addWidget(self.microstep_4)
        self.microstep_8 = QtWidgets.QRadioButton(self.verticalLayoutWidget_6)
        self.microstep_8.setObjectName("microstep_8")
        self.microstep_vbox.addWidget(self.microstep_8)
        self.horizontalLayout_4.addWidget(self.microstep_frame)
        self.speed_frame = QtWidgets.QFrame(self.settings)
        self.speed_frame.setMaximumSize(QtCore.QSize(170, 190))
        self.speed_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.speed_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.speed_frame.setObjectName("speed_frame")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.speed_frame)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(10, 10, 151, 171))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.speed_vbox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.speed_vbox.setContentsMargins(10, -1, 10, -1)
        self.speed_vbox.setObjectName("speed_vbox")
        self.speed_label = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.speed_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.speed_label.setTextFormat(QtCore.Qt.AutoText)
        self.speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.speed_label.setObjectName("speed_label")
        self.speed_vbox.addWidget(self.speed_label)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget_7)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.speed_vbox.addWidget(self.line_4)
        self.speed_50 = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.speed_50.setCheckable(True)
        self.speed_50.setAutoExclusive(True)
        self.speed_50.setObjectName("speed_50")
        self.speed_vbox.addWidget(self.speed_50)
        self.speed_100 = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.speed_100.setChecked(True)
        self.speed_100.setObjectName("speed_100")
        self.speed_vbox.addWidget(self.speed_100)
        self.speed_150 = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.speed_150.setObjectName("speed_150")
        self.speed_vbox.addWidget(self.speed_150)
        self.speed_200 = QtWidgets.QRadioButton(self.verticalLayoutWidget_7)
        self.speed_200.setObjectName("speed_200")
        self.speed_vbox.addWidget(self.speed_200)
        self.horizontalLayout_4.addWidget(self.speed_frame)
        self.tabWidget.addTab(self.settings, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.jog_down_fast.clicked['bool'].connect(self.start_run_button.setDisabled)
        self.jog_down_slow.clicked['bool'].connect(self.start_run_button.setDisabled)
        self.jog_up_slow.clicked['bool'].connect(self.start_run_button.setDisabled)
        self.jog_up_fast.clicked['bool'].connect(self.start_run_button.setDisabled)
        self.jog_stop.clicked['bool'].connect(self.start_run_button.setEnabled)
        self.jog_down_fast.clicked['bool'].connect(self.stop_run_button.setDisabled)
        self.jog_down_slow.clicked['bool'].connect(self.stop_run_button.setDisabled)
        self.jog_up_slow.clicked['bool'].connect(self.stop_run_button.setDisabled)
        self.jog_up_fast.clicked['bool'].connect(self.stop_run_button.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Data Aquisition Run"))
        self.start_run_button.setText(_translate("MainWindow", "Start Run"))
        self.stop_run_button.setText(_translate("MainWindow", "Stop Run"))
        self.pushButton_2.setText(_translate("MainWindow", "Save Data"))
        self.label.setText(_translate("MainWindow", "Position Data"))
        self.actual_pos_label.setText(_translate("MainWindow", "Actual"))
        self.motor_pos_label.setText(_translate("MainWindow", "Motors"))
        self.error_label.setText(_translate("MainWindow", "Error"))
        self.pushButton.setText(_translate("MainWindow", "Zero Postions"))
        self.label_3.setText(_translate("MainWindow", "Zero"))
        self.jog_header_label.setText(_translate("MainWindow", "Jog Control"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.general), _translate("MainWindow", "General"))
        self.microstep_label.setText(_translate("MainWindow", "Microstep Setting"))
        self.microstep_1.setText(_translate("MainWindow", "1 (Not Recommended)"))
        self.microstep_2.setText(_translate("MainWindow", "2"))
        self.microstep_4.setText(_translate("MainWindow", "4"))
        self.microstep_8.setText(_translate("MainWindow", "8 (Not Recommended)"))
        self.speed_label.setText(_translate("MainWindow", "Speed Setting"))
        self.speed_50.setText(_translate("MainWindow", "50 rpm"))
        self.speed_100.setText(_translate("MainWindow", "100 rpm"))
        self.speed_150.setText(_translate("MainWindow", "150 rpm"))
        self.speed_200.setText(_translate("MainWindow", "200 rpm"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), _translate("MainWindow", "Settings"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))