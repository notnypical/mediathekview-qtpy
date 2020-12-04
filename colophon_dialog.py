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

from PySide2.QtCore import QByteArray, Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QTabWidget, QVBoxLayout

from colophon_about_page import ColophonAboutPage
from colophon_environment_page import ColophonEnvironmentPage
from dialog_title_box import DialogTitleBox


class ColophonDialog(QDialog):

    def __init__(self, parent=None):
        super(ColophonDialog, self).__init__(parent)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Colophon')

        self.setDialogGeometry(QByteArray())

        # Title box
        titleBox = DialogTitleBox()

        # Content
        aboutPage = ColophonAboutPage()
        environmentPage = ColophonEnvironmentPage()

        tabBox = QTabWidget()
        tabBox.addTab(aboutPage, aboutPage.title())
        tabBox.addTab(environmentPage, environmentPage.title())

        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(titleBox)
        layout.addWidget(tabBox)
        layout.addWidget(buttonBox)


    def setDialogGeometry(self, geometry):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            self.resize(640, 480)


    def dialogGeometry(self):

        return self.saveGeometry()
