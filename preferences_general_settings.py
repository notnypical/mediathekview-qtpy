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

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel, QVBoxLayout, QWidget


class PreferencesGeneralSettings(QWidget):

    settingsChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        label = QLabel(self.tr('<strong style="font-size:large;">General Options</strong>'))


        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(label)


    def title(self):

        return self.tr('General')


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def onSettingsChanged(self):

        self.settingsChanged.emit()