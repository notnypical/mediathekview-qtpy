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

from PySide2.QtCore import QSettings


class Preferences:

    def __init__(self):

        # General: Geometry & State
        self._restoreApplicationGeometry = True
        self._restoreApplicationState = True


    def loadSettings(self):

        settings = QSettings()

        settings.beginGroup("Preferences")

        # General: Geometry & State
        self.setRestoreApplicationGeometry(self._valueToBool(settings.value("RestoreApplicationGeometry", True)))
        self.setRestoreApplicationState(self._valueToBool(settings.value("RestoreApplicationState", True)))

        settings.endGroup()


    def saveSettings(self):

        settings = QSettings()

        settings.remove("Preferences")
        settings.beginGroup("Preferences")

        # General: Geometry & State
        settings.setValue("RestoreApplicationGeometry", self._restoreApplicationGeometry)
        settings.setValue("RestoreApplicationState", self._restoreApplicationState)

        settings.endGroup()


    @staticmethod
    def _valueToBool(value):

        return value.lower() == "true" if isinstance(value, str) else bool(value)


    def setRestoreApplicationGeometry(self, value):

        self._restoreApplicationGeometry = value


    def restoreApplicationGeometry(self, isDefault=False):

        return self._restoreApplicationGeometry if not isDefault else True


    def setRestoreApplicationState(self, value):

        self._restoreApplicationState = value


    def restoreApplicationState(self, isDefault=False):

        return self._restoreApplicationState if not isDefault else True
