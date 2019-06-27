import sys
from os import listdir
from os.path import getctime

from PyQt5 import QtWidgets, QtCore, QtGui

import workers


class Nearest(QtWidgets.QDialog):
    closed_signal = QtCore.pyqtSignal()  # signal sent when window is closed
    destination_signal = QtCore.pyqtSignal(str)  # signal containing destination to input into destination line edit

    # lightly modified auto generated
    def __init__(self, parent):
        super(Nearest, self).__init__(parent=parent)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout_frame = QtWidgets.QFrame(self)
        self.frame_layout = QtWidgets.QGridLayout(self.main_layout_frame)
        self.main_horizontal = QtWidgets.QHBoxLayout()
        self.coords_vertical = QtWidgets.QVBoxLayout()
        self.x_edit = QtWidgets.QLineEdit(self.main_layout_frame)
        self.y_edit = QtWidgets.QLineEdit(self.main_layout_frame)
        self.z_edit = QtWidgets.QLineEdit(self.main_layout_frame)
        self.output_vertical = QtWidgets.QVBoxLayout()
        self.system_horizontal = QtWidgets.QHBoxLayout()
        self.system_main = QtWidgets.QLabel(self.main_layout_frame)
        self.system_output = QtWidgets.QLabel(self.main_layout_frame)
        self.distance_horizontal = QtWidgets.QHBoxLayout()
        self.distance_main = QtWidgets.QLabel(self.main_layout_frame)
        self.distance_output = QtWidgets.QLabel(self.main_layout_frame)
        self.x_horizontal = QtWidgets.QHBoxLayout()
        self.x_main = QtWidgets.QLabel(self.main_layout_frame)
        self.x_output = QtWidgets.QLabel(self.main_layout_frame)
        self.y_horizontal = QtWidgets.QHBoxLayout()
        self.y_main = QtWidgets.QLabel(self.main_layout_frame)
        self.y_output = QtWidgets.QLabel(self.main_layout_frame)
        self.z_horizontal = QtWidgets.QHBoxLayout()
        self.z_main = QtWidgets.QLabel(self.main_layout_frame)
        self.z_output = QtWidgets.QLabel(self.main_layout_frame)
        self.status_vertical = QtWidgets.QVBoxLayout()
        self.get_button = QtWidgets.QPushButton(enabled=False)
        self.status = QtWidgets.QStatusBar()

    def setupUi(self):
        self.resize(207, 191)
        self.main_layout.setContentsMargins(2, 2, 20, 2)
        self.main_layout.setSpacing(2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_layout_frame.sizePolicy().hasHeightForWidth())
        self.main_layout_frame.setSizePolicy(sizePolicy)
        self.main_layout_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_layout_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.main_layout_frame.setLineWidth(0)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.main_horizontal.setSpacing(0)
        self.coords_vertical.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.coords_vertical.setSpacing(0)
        self.x_edit.setMaximumWidth(60)
        self.coords_vertical.addWidget(self.x_edit)
        self.y_edit.setMaximumWidth(60)
        self.coords_vertical.addWidget(self.y_edit)
        self.z_edit.setMaximumWidth(60)
        self.coords_vertical.addWidget(self.z_edit)
        self.main_horizontal.addLayout(self.coords_vertical)
        self.system_main.setMaximumWidth(68)
        self.system_horizontal.addWidget(self.system_main)
        self.system_horizontal.addWidget(self.system_output, alignment=QtCore.Qt.AlignRight)
        self.output_vertical.addLayout(self.system_horizontal)
        self.distance_main.setMaximumWidth(45)
        self.distance_horizontal.addWidget(self.distance_main)
        self.distance_horizontal.addWidget(self.distance_output, alignment=QtCore.Qt.AlignRight)
        self.output_vertical.addLayout(self.distance_horizontal)
        self.x_main.setMaximumWidth(15)
        self.x_horizontal.addWidget(self.x_main)
        self.x_horizontal.addWidget(self.x_output, alignment=QtCore.Qt.AlignRight)
        self.output_vertical.addLayout(self.x_horizontal)
        self.y_main.setMaximumWidth(15)
        self.y_horizontal.addWidget(self.y_main)
        self.y_horizontal.addWidget(self.y_output, alignment=QtCore.Qt.AlignRight)
        self.output_vertical.addLayout(self.y_horizontal)
        self.z_main.setMaximumWidth(15)
        self.z_horizontal.addWidget(self.z_main)
        self.z_horizontal.addWidget(self.z_output, alignment=QtCore.Qt.AlignRight)
        self.output_vertical.addLayout(self.z_horizontal)
        self.main_horizontal.addLayout(self.output_vertical)
        self.frame_layout.addLayout(self.main_horizontal, 0, 0, 1, 1)
        self.main_layout.addWidget(self.main_layout_frame)
        self.status_vertical.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.status_vertical.setSpacing(0)
        self.main_layout.addLayout(self.status_vertical)
        self.coords_vertical.addWidget(self.get_button)
        self.main_horizontal.setSpacing(10)
        self.get_button.pressed.connect(self.get_nearest)
        self.status_vertical.addWidget(self.status)

        self.retranslateUi()
        regex = QtCore.QRegExp("\-?\d+\.\d+")
        valida = QtGui.QRegExpValidator(regex)
        self.x_edit.setValidator(valida)
        self.y_edit.setValidator(valida)
        self.z_edit.setValidator(valida)

        self.x_edit.textChanged.connect(self.ena_button)
        self.y_edit.textChanged.connect(self.ena_button)
        self.z_edit.textChanged.connect(self.ena_button)

        self.system_output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.system_output.setCursor(QtCore.Qt.IBeamCursor)
        self.system_output.mouseDoubleClickEvent = self.set_destination

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.show()

    def ena_button(self):
        if len(self.x_edit.text()) != 0 and len(self.y_edit.text()) != 0 and len(self.z_edit.text()) != 0:
            self.get_button.setEnabled(True)
        else:
            self.get_button.setEnabled(False)

    def get_nearest(self):
        self.nearest_worker = workers.NearestRequest("https://spansh.co.uk/api/nearest",
                                                     f"x={self.x_edit.text()}&y={self.y_edit.text()}"
                                                     f"&z={self.z_edit.text()}")
        self.nearest_worker.finished_signal.connect(self.nearest_finished)
        self.nearest_worker.status_signal.connect(self.change_status)
        self.nearest_worker.start()

    def nearest_finished(self, system):
        self.nearest_worker.quit()
        self.status.clearMessage()
        self.system_output.setText(str(system['name']))
        self.distance_output.setText(str(round(system['distance'], 2)) + " Ly")
        self.x_output.setText(str(round(system['x'], 2)))
        self.y_output.setText(str(round(system['y'], 2)))
        self.z_output.setText(str(round(system['z'], 2)))

    def change_status(self, message):
        self.status.showMessage(message)

    def set_destination(self, event):
        self.destination_signal.emit(self.system_output.text())

    def retranslateUi(self):
        self.setWindowTitle("Nearest")
        self.system_main.setText("System Name")
        self.distance_main.setText("Distance")
        self.x_main.setText("X")
        self.y_main.setText("Y")
        self.z_main.setText("Z")
        self.get_button.setText("Get sys")

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QDialog, self).closeEvent(*args, **kwargs)
        self.closed_signal.emit()


class GameShutPop(QtWidgets.QDialog):
    worker_signal = QtCore.pyqtSignal(str, list, int)  # signal to start new worker
    # signal to disconenct all main window singals if app is not quit or new worker is not started
    close_signal = QtCore.pyqtSignal()

    def __init__(self, parent, settings, route, index):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.comboBox = QtWidgets.QComboBox(self)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.jour_ver = QtWidgets.QHBoxLayout(self)
        self.save_quit_lay = QtWidgets.QHBoxLayout(self)
        self.save_button = QtWidgets.QPushButton(self)
        self.route = route
        self.index = index
        self.settings = settings
        self.jpath = self.settings.value("paths/journal")

    def setupUi(self):
        self.resize(375, 125)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)

        self.jour_ver.addWidget(self.pushButton, alignment=QtCore.Qt.AlignLeft)
        self.jour_ver.addWidget(self.comboBox, alignment=QtCore.Qt.AlignCenter)
        self.jour_ver.addSpacerItem(QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.MinimumExpanding))

        self.save_quit_lay.addWidget(self.save_button, alignment=QtCore.Qt.AlignRight)
        self.save_quit_lay.addWidget(self.pushButton_2, alignment=QtCore.Qt.AlignRight)

        self.horizontalLayout.addLayout(self.jour_ver)
        self.horizontalLayout.addLayout(self.save_quit_lay)

        self.verticalLayout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.verticalLayout.addSpacerItem(QtWidgets.QSpacerItem(1, 1
                                                                , QtWidgets.QSizePolicy.Fixed,
                                                                QtWidgets.QSizePolicy.MinimumExpanding))
        self.verticalLayout.setContentsMargins(6, 20, 6, 6)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButton_2.pressed.connect(sys.exit)
        self.save_button.pressed.connect(self.save_route)
        self.pushButton.pressed.connect(self.load_journal)

        if self.index == 0 or self.index == 1:
            self.save_button.setDisabled(True)
        self.populate_combo()

        self.setWindowTitle("self")
        self.label.setText("Game shut down")
        self.pushButton.setText("Load journal")
        self.pushButton_2.setText("Quit")
        self.save_button.setText("Save current route")
        self.setModal(True)
        self.show()

    def save_route(self):
        self.settings.setValue("last_route", [self.index, self.route])
        self.save_button.setDisabled(True)

    def populate_combo(self):
        self.comboBox.addItems(["Last journal", "Second to last",
                                "Third to last"][:len([file for file in listdir(self.jpath) if file.endswith(".log")])])

    def load_journal(self):
        journals = sorted([self.jpath + file for file in listdir(self.jpath) if file.endswith(".log")],
                          key=getctime, reverse=True)
        self.worker_signal.emit(journals[self.comboBox.currentIndex()], self.route, self.index)
        self.hide()

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QDialog, self).closeEvent(*args, **kwargs)
        self.close_signal.emit()


class SettingsPop(QtWidgets.QDialog):
    settings_signal = QtCore.pyqtSignal(list)  # signal containing new settings

    def __init__(self, parent, settings: QtCore.QSettings):
        super(SettingsPop, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.main_bind_edit = QtWidgets.QLineEdit(self)
        self.script_edit = QtWidgets.QTextEdit(self)
        self.dark_check = QtWidgets.QCheckBox(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.font_combo = QtWidgets.QFontComboBox(self)
        self.font_size_combo = QtWidgets.QSpinBox(self)
        self.bold_check = QtWidgets.QCheckBox(self)
        self.pushButton = QtWidgets.QPushButton(self)
        self.save_on_quit = QtWidgets.QCheckBox(self)
        self.copy_layout = QtWidgets.QHBoxLayout()
        self.ahk_button = QtWidgets.QPushButton()
        self.copy_check = QtWidgets.QCheckBox(self)
        self.settings = settings
        self.status = QtWidgets.QStatusBar(self)

    def setupUi(self):
        self.resize(265, 371)
        self.main_bind_edit.setMaximumWidth(100)

        self.horizontalLayout.setSpacing(0)
        self.font_size_combo.setMaximumWidth(50)
        self.pushButton.setMaximumWidth(95)
        self.pushButton.pressed.connect(self.save_settings)

        self.setWindowTitle("Settings")
        self.dark_check.setText("Dark theme")
        self.bold_check.setText("Bold")
        self.pushButton.setText("Save settings")
        self.main_bind_edit.setToolTip(
            "Bind to trigger the script, # for win key, ! for alt, ^ for control, + for shift")
        self.save_on_quit.setText("Save route on window close")
        self.copy_check.setText("Copy mode")
        self.ahk_button.setText("AHK Path")

        self.main_bind_edit.setText(self.settings.value("bind"))
        self.script_edit.setText(self.settings.value("script"))
        self.dark_check.setChecked(self.settings.value("window/dark", type=bool))
        self.font_combo.setCurrentFont(self.settings.value("font/font", type=QtGui.QFont))
        self.font_size_combo.setValue(self.settings.value("font/size", type=int))
        self.bold_check.setChecked(self.settings.value("font/bold", type=bool))
        self.save_on_quit.setChecked(self.settings.value("save_on_quit", type=bool))
        self.copy_check.setChecked(self.settings.value("copy_mode", type=bool))
        if self.settings.value("paths/AHK") == "":
            self.copy_check.setDisabled(True)
        self.verticalLayout.addWidget(self.main_bind_edit)
        self.verticalLayout.addWidget(self.script_edit)
        self.verticalLayout.addWidget(self.dark_check)
        self.verticalLayout.addWidget(self.save_on_quit)
        self.copy_layout.addWidget(self.copy_check)
        self.copy_layout.addWidget(self.ahk_button)
        self.verticalLayout.addLayout(self.copy_layout)
        self.horizontalLayout.addWidget(self.font_combo)
        self.horizontalLayout.addWidget(self.font_size_combo)
        self.horizontalLayout.addWidget(self.bold_check, alignment=QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.status)

        self.ahk_button.pressed.connect(self.ahk_dialog)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.show()

    def ahk_dialog(self):
        ahk_path = QtWidgets.QFileDialog.getOpenFileName(filter="AutoHotKey (AutoHotKey*.exe)",
                                                         caption="Select AutoHotkey's executable")
        if len(ahk_path[0]) != 0:
            self.settings.setValue("paths/AHK", ahk_path[0])
            self.copy_check.setDisabled(False)
        self.settings.sync()

    def save_settings(self):
        values = [self.main_bind_edit.text(), self.script_edit.toPlainText(), self.dark_check.isChecked(),
                  self.font_combo.currentFont(), self.font_size_combo.value(), self.bold_check.isChecked(),
                  self.save_on_quit.isChecked(), self.copy_check.isChecked()]

        if "|SYSTEMDATA|" not in values[1]:
            self.status.showMessage('Script must include "|SYSTEMDATA|"')
        else:
            self.settings.setValue("bind", values[0])
            self.settings.setValue("script", values[1])
            self.settings.setValue("window/dark", values[2])
            self.settings.setValue("font/font", values[3])
            self.settings.setValue("font/size", values[4])
            self.settings.setValue("font/bold", values[5])
            self.settings.setValue("save_on_quit", values[6])
            self.settings.setValue("copy_mode", values[7])
            self.settings.sync()
            self.settings_signal.emit(values)


class QuitDialog(QtWidgets.QDialog):
    def __init__(self, parent, prompt, modal):
        super(QuitDialog, self).__init__(parent)
        self.gridLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        self.pushButton = QtWidgets.QPushButton(self)
        self.prompt = prompt
        self.modal = modal

    def setupUi(self):
        self.setFixedSize(300, 100)
        self.setWindowTitle(" ")
        self.gridLayout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)
        self.pushButton.setText("Quit")
        self.label.setText(self.prompt)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.pushButton.setMaximumWidth(95)
        self.pushButton.pressed.connect(sys.exit)

        self.setModal(self.modal)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.show()


class RouteFinishedPop(QtWidgets.QDialog):
    close_signal = QtCore.pyqtSignal()
    new_route_signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(RouteFinishedPop, self).__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.quit_button = QtWidgets.QPushButton()
        self.new_route_button = QtWidgets.QPushButton()
        self.button_layout = QtWidgets.QHBoxLayout()

    def setup(self):
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(7, 20, 7, 10)
        self.main_layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.main_layout.addSpacerItem(QtWidgets.QSpacerItem(1, 1
                                                             , QtWidgets.QSizePolicy.Fixed,
                                                             QtWidgets.QSizePolicy.MinimumExpanding))
        self.main_layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.new_route_button)
        self.button_layout.addSpacerItem(QtWidgets.QSpacerItem(1, 1
                                                               , QtWidgets.QSizePolicy.MinimumExpanding,
                                                               QtWidgets.QSizePolicy.Fixed))
        self.button_layout.addWidget(self.quit_button)

        self.quit_button.pressed.connect(sys.exit)
        self.new_route_button.pressed.connect(self.new_route_signal.emit)
        self.new_route_button.pressed.connect(self.hide)
        self.retranslateUi()
        self.show()

    def retranslateUi(self):
        self.label.setText("Route finished")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.quit_button.setText("Quit")
        self.new_route_button.setText("New route")

    def closeEvent(self, *args, **kwargs):
        super(QtWidgets.QDialog, self).closeEvent(*args, **kwargs)
        self.close_signal.emit()


class LicensePop(QtWidgets.QDialog):
    def __init__(self, parent):
        super(LicensePop, self).__init__(parent)
        self.text = QtWidgets.QTextBrowser()
        self.layout = QtWidgets.QVBoxLayout()

    def setup(self):
        self.setFixedSize(297, 62)
        self.text.setText("Auto Neutron Copyright (C) 2019 Numerlor\n"
                          "This program comes with ABSOLUTELY NO WARRANTY.\n"
                          "This is free software, and you are welcome to redistribute it")
        self.text.append('under certain conditions; <a href="https://www.gnu.org/licenses/">click here</a> for details')
        self.layout.addWidget(self.text)
        self.text.setOpenExternalLinks(True)
        self.setLayout(self.layout)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.show()
