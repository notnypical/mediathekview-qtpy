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
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QMainWindow

import resources


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowIcon(QIcon(':/icons/apps/16/mediathekview.svg'))

        self.setWindowGeometry(QByteArray())


    def setWindowGeometry(self, geometry):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def windowGeometry(self):

        return self.saveGeometry()


    def setWindowState(self, state):

        if state:
            self.restoreState(state)


    def windowState(self):

        self.saveState()
