# This Python file uses the following encoding: utf-8
#
# Copyright 2020 NotNypical, <https://notnypical.github.io>.
#
# This file is part of MediathekView-QtPy.
#
# MediathekView-QtPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MediathekView-QtPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MediathekView-QtPy.  If not, see <https://www.gnu.org/licenses/>.
#

from PySide2.QtCore import QByteArray, QRect
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QMenuBar, QToolBar

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog

import resources


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowIcon(QIcon(':/icons/apps/16/mediathekview.svg'))

        self.createActions()
        self.createMenus()
        self.createToolbars()

        self.setApplicationGeometry(QByteArray())


    def createActions(self):

        # Actions: Application
        self.actionAbout = QAction(f'About {QApplication.applicationName()}', self)
        self.actionAbout.setObjectName('actionAbout')
        self.actionAbout.setIcon(QIcon(':/icons/apps/16/mediathekview.svg'))
        self.actionAbout.setToolTip('Brief description of the application')
        self.actionAbout.triggered.connect(self.onActionAboutTriggered)

        self.actionColophon = QAction('Colophon', self)
        self.actionColophon.setObjectName('actionColophon')
        self.actionColophon.setToolTip('Lengthy description of the application')
        self.actionColophon.triggered.connect(self.onActionColophonTriggered)

        self.actionPreferences = QAction('Preferences…', self)
        self.actionPreferences.setObjectName('actionPreferences')
        self.actionPreferences.setIcon(QIcon.fromTheme('configure', QIcon(':/icons/actions/16/application-configure.svg')))
        self.actionPreferences.setToolTip('Customize the appearance and behavior of the application')
        self.actionPreferences.triggered.connect(self.onActionPreferencesTriggered)

        self.actionQuit = QAction('Quit', self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/actions/16/application-exit.svg')))
        self.actionQuit.setShortcut(QKeySequence.Quit)
        self.actionQuit.setToolTip(f'Quit the application [{self.actionQuit.shortcut().toString(QKeySequence.NativeText)}]')
        self.actionQuit.triggered.connect(self.close)


    def createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu('Application')
        menuApplication.setObjectName('menuApplication')
        menuApplication.addAction(self.actionAbout)
        menuApplication.addAction(self.actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionQuit)


    def createToolbars(self):

        # Toolbar: Application
        toolbarApplication = self.addToolBar('Application')
        toolbarApplication.setObjectName('toolbarApplication')
        toolbarApplication.addAction(self.actionAbout)
        toolbarApplication.addAction(self.actionPreferences)
        toolbarApplication.addSeparator()
        toolbarApplication.addAction(self.actionQuit)


    def setApplicationGeometry(self, geometry):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def applicationGeometry(self):

        return self.saveGeometry()


    def setApplicationState(self, state):

        if state:
            self.restoreState(state)


    def applicationState(self):

        self.saveState()


    def onActionAboutTriggered(self):

        geometry = QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()


    def onActionColophonTriggered(self):

        geometry = QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()


    def onActionPreferencesTriggered(self):
        pass
