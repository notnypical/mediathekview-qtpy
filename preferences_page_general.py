# This Python file uses the following encoding: utf-8
#
# Copyright 2020-2021 NotNypical, <https://notnypical.github.io>.
#
# This file is part of MediathekView-QtPy, <https://github.com/notnypical/mediathekview-qtpy>.
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
from PySide2.QtWidgets import QCheckBox, QGroupBox, QLabel, QVBoxLayout, QWidget


class PreferencesPageGeneral(QWidget):

    preferencesChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        # Title
        title = QLabel(self.tr("<strong style=\"font-size:large;\">{0}</strong>").format(self.title()))


        #
        # Content: Geometry & State

        self._chkRestoreApplicationGeometry = QCheckBox(self.tr("Save and restore the application geometry"))
        self._chkRestoreApplicationGeometry.stateChanged.connect(self._onPreferencesChanged)

        self._chkRestoreApplicationState = QCheckBox(self.tr("Save and restore the application state"))
        self._chkRestoreApplicationState.stateChanged.connect(self._onPreferencesChanged)

        geometryStateLayout = QVBoxLayout()
        geometryStateLayout.addWidget(self._chkRestoreApplicationGeometry)
        geometryStateLayout.addWidget(self._chkRestoreApplicationState)

        geometryStateGroup = QGroupBox(self.tr("Geometry && State"))
        geometryStateGroup.setLayout(geometryStateLayout)


        # Main layout
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(title)
        self._layout.addWidget(geometryStateGroup)
        self._layout.addStretch(1)


    def setZeroMargins(self):

        self._layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr("General")


    def _onPreferencesChanged(self):

        self.preferencesChanged.emit()


    def restoreApplicationGeometry(self):

        return self._chkRestoreApplicationGeometry.isChecked()


    def setRestoreApplicationGeometry(self, checked):

        self._chkRestoreApplicationGeometry.setChecked(checked)


    def restoreApplicationState(self):

        return self._chkRestoreApplicationState.isChecked()


    def setRestoreApplicationState(self, checked):

        self._chkRestoreApplicationState.setChecked(checked)
