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

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QTabWidget, QVBoxLayout

from colophon_pages import ColophonPageAbout, ColophonPageAuthors, ColophonPageCredits, ColophonPageEnvironment, ColophonPageLicense
from dialog_title_box import DialogTitleBox


class ColophonDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(640, 480)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(self.tr("Colophon"))

        # Title box
        titleBox = DialogTitleBox()


        #
        # Content

        pageAbout = ColophonPageAbout()
        pageEnvironment = ColophonPageEnvironment()
        pageLicense = ColophonPageLicense()
        pageAuthors = ColophonPageAuthors()
        pageCredits = ColophonPageCredits()

        tabBox = QTabWidget()
        tabBox.addTab(pageAbout, pageAbout.title())
        tabBox.addTab(pageEnvironment, pageEnvironment.title())
        tabBox.addTab(pageLicense, pageLicense.title())
        tabBox.addTab(pageAuthors, pageAuthors.title())
        tabBox.addTab(pageCredits, pageCredits.title())


        # Button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.rejected.connect(self.close)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(titleBox)
        layout.addWidget(tabBox)
        layout.addWidget(buttonBox)
