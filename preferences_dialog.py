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

from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QListWidget, QStackedWidget, QVBoxLayout

from preferences_database_settings import PreferencesDatabaseSettings
from preferences_general_settings import PreferencesGeneralSettings
from settings import Settings


class PreferencesDialog(QDialog):

    _settings = Settings()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(self.tr('Preferences'))

        self.setDialogGeometry()

        # Settings box
        self.generalSettings = PreferencesGeneralSettings(self)
        self.generalSettings.setZeroMargins()
        self.generalSettings.settingsChanged.connect(self.onSettingsChanged)

        self.databaseSettings = PreferencesDatabaseSettings(self)
        self.databaseSettings.setZeroMargins()
        self.databaseSettings.settingsChanged.connect(self.onSettingsChanged)

        stackedBox = QStackedWidget()
        stackedBox.addWidget(self.generalSettings)
        stackedBox.addWidget(self.databaseSettings)
        stackedBox.setCurrentIndex(0)

        listBox = QListWidget()
        listBox.addItem(self.generalSettings.title())
        listBox.addItem(self.databaseSettings.title())
        listBox.setCurrentRow(stackedBox.currentIndex())
        listBox.currentRowChanged.connect(stackedBox.setCurrentIndex)

        settingsBox = QHBoxLayout()
        settingsBox.addWidget(listBox, 1)
        settingsBox.addWidget(stackedBox, 3)

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.RestoreDefaults | QDialogButtonBox.Ok | QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
        self.buttonApply = buttonBox.button(QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.onButtonDefaultsClicked)
        buttonBox.accepted.connect(self.onButtonOkClicked)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.onButtonApplyClicked)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addLayout(settingsBox)
        layout.addWidget(buttonBox)

        self.updateSettings()
        self.buttonApply.setEnabled(False)


    def setDialogGeometry(self, geometry=QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)


    def dialogGeometry(self):

        return self.saveGeometry()


    def setSettings(self, settings):

        self._settings = settings

        self.updateSettings()
        self.buttonApply.setEnabled(False)


    def settings(self):

        return self._settings


    def onSettingsChanged(self):

        self.buttonApply.setEnabled(True)


    def onButtonDefaultsClicked(self):

        self.updateSettings(True)


    def onButtonOkClicked(self):

        self.saveSettings()
        self.close()


    def onButtonApplyClicked(self):

        self.saveSettings()
        self.buttonApply.setEnabled(False)


    def updateSettings(self, isDefault=False):

        # General
        self.generalSettings.setRestoreApplicationState(self._settings.restoreApplicationState(isDefault))
        self.generalSettings.setRestoreApplicationGeometry(self._settings.restoreApplicationGeometry(isDefault))


    def saveSettings(self):

        # General
        self._settings.setRestoreApplicationState(self.generalSettings.restoreApplicationState())
        self._settings.setRestoreApplicationGeometry(self.generalSettings.restoreApplicationGeometry())
