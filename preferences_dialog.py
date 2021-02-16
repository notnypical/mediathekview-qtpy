# This Python file uses the following encoding: utf-8
#
# Copyright 2020-2021 NotNypical, <https://notnypical.github.io>.
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

from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences import Preferences
from preferences_database_page import PreferencesDatabasePage
from preferences_general_page import PreferencesGeneralPage


class PreferencesDialog(QDialog):

    _preferences = Preferences()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))

        self.setDialogGeometry()

        # Preferences box
        self.generalPage = PreferencesGeneralPage(self)
        self.generalPage.setZeroMargins()
        self.generalPage.preferencesChanged.connect(self.onPreferencesChanged)

        self.databasePage = PreferencesDatabasePage(self)
        self.databasePage.setZeroMargins()
        self.databasePage.preferencesChanged.connect(self.onPreferencesChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self.generalPage)
        stackedBox.addWidget(self.databasePage)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self.generalPage.title())
        listBox.addItem(self.databasePage.title())
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        preferencesBox = QHBoxLayout()
        preferencesBox.addWidget(listBox, 1)
        preferencesBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        buttonBox.accepted.connect(self.onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(preferencesBox)
        layout.addWidget(buttonBox)

        self.updatePreferences()
        self.buttonApply.setEnabled(False)


    def setDialogGeometry(self, geometry=QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)


    def dialogGeometry(self):

        return self.saveGeometry()


    def setPreferences(self, preferences):

        self._preferences = preferences

        self.updatePreferences()
        self.buttonApply.setEnabled(False)


    def preferences(self):

        return self._preferences


    def onPreferencesChanged(self):

        self.buttonApply.setEnabled(True)


    def onButtonDefaultsClicked(self):

        self.updatePreferences(True)


    def onButtonOkClicked(self):

        self.savePreferences()
        self.close()


    def onButtonApplyClicked(self):

        self.savePreferences()
        self.buttonApply.setEnabled(False)


    def updatePreferences(self, isDefault=False):

        # General: State && Geometries
        self.generalPage.setRestoreApplicationState(self._preferences.restoreApplicationState(isDefault))
        self.generalPage.setRestoreApplicationGeometry(self._preferences.restoreApplicationGeometry(isDefault))
        self.generalPage.setRestoreDialogGeometry(self._preferences.restoreDialogGeometry(isDefault))


    def savePreferences(self):

        # General: State && Geometries
        self._preferences.setRestoreApplicationState(self.generalPage.restoreApplicationState())
        self._preferences.setRestoreApplicationGeometry(self.generalPage.restoreApplicationGeometry())
        self._preferences.setRestoreDialogGeometry(self.generalPage.restoreDialogGeometry())
