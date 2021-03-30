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

import sys
import PySide2.QtCore

from PySide2.QtCore import QSysInfo
from PySide2.QtWidgets import QApplication, QFrame, QTextBrowser, QVBoxLayout, QWidget


class ColophonAboutPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr(f'''<html><body>
            <p>{QApplication.applicationName()} is an open source front-end tool written in Qt for Python and designed for easy access to the <a href="https://mediathekview.de" title="Visit MediathekView's homepage">MediathekView</a> database.</p>
            <p>Copyright &copy; 2020-2021 <a href="{QApplication.organizationDomain()}" title="Visit organization's homepage">{QApplication.organizationName()}</a>.</p>
            <p>This application is licensed under the terms of the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" title="Visit license's homepage">GNU General Public License, version 3</a>.</p>
            </body></html>'''))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('About')


class ColophonAuthorsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr('''<html><body>
            <dl><dt><strong>NotNypical</strong></dt>
                <dd>Created and developed by <a href="https://notnypical.github.io" title="Visit author's homepage">NotNypical</a>.</dd></dl>
            </body></html>'''))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Authors')


class ColophonCreditsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr('''<html><body>
            <dl><dt><strong>BreezeIcons project</strong></dt>
                <dd>Application logo and icons made by <a href="https://api.kde.org/frameworks/breeze-icons/html/" title="Visit project's homepage">BreezeIcons project</a>
                    from <a href="https://kde.org" title="Visit organization's homepage">KDE</a>
                    are licensed under <a href="https://www.gnu.org/licenses/lgpl-3.0.en.html" title="Visit license's homepage">LGPLv3</a>.</dd></dl>
            </body></html>'''))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Credits')


class ColophonEnvironmentPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        pythonVersion = sys.version
        pysideVersion = PySide2.__version__
        qtVersion = PySide2.QtCore.qVersion()  # Qt version used to run Qt for Python
        qtBuildVersion = PySide2.QtCore.__version__  # Qt version used to compile PySide2
        osName = QSysInfo.prettyProductName()
        osKernelVersion = QSysInfo.kernelVersion()
        osCpuArchitecture = QSysInfo.currentCpuArchitecture()

        textBox = QTextBrowser()
        textBox.setFrameStyle(QFrame.NoFrame)
        textBox.setStyleSheet('background-color:transparent;')
        textBox.setOpenExternalLinks(True)
        textBox.setHtml(self.tr(f'''<html><body>
            <dl><dt><strong>Application version</strong></dt>
                <dd>{QApplication.applicationVersion()}</dd></dl>
            <dl><dt><strong>Qt for Python version</strong></dt>
                <dd>{pysideVersion} runs on Qt {qtVersion} (Built against {qtBuildVersion})</dd></dl>
            <dl><dt><strong>Python version</strong></dt>
                <dd>{pythonVersion}</dd></dl>
            <dl><dt><strong>Operation System</strong></dt>
                <dd>{osName} (Kernel {osKernelVersion} on {osCpuArchitecture})</dd></dl>
            </body></html>'''))

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(textBox)


    def setZeroMargins(self):

        self.layout.setContentsMargins(0, 0, 0, 0)


    def title(self):

        return self.tr('Environment')
