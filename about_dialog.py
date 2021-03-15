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

from PySide2.QtCore import QByteArray, Qt
from PySide2.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout

from colophon_about_page import ColophonAboutPage
from dialog_title_box import DialogTitleBox


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(self.tr(f'About {QApplication.applicationName()}'))

        # Title box
        titleBox = DialogTitleBox()

        # Content
        aboutPage = ColophonAboutPage()
        aboutPage.setZeroMargins()

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(titleBox)
        layout.addWidget(aboutPage)
        layout.addWidget(buttonBox)


    def setDialogGeometry(self, geometry=QByteArray()):

        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            self.resize(480, 320)


    def dialogGeometry(self):

        return self.saveGeometry()
