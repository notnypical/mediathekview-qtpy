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

from PySide2.QtCore import QByteArray, QRect, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog

import resources


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowIcon(QIcon(':/icons/apps/16/mediathekview.svg'))

        self.createChannels()
        self.createActions()
        self.createMenus()
        self.createToolbars()

        self.setApplicationGeometry()
        self.setApplicationState()

        self.updateActionFullScreen()


    def createChannels(self):

        self.listChannels = {
            '3sat': ['3sat'],
            'ard': ['ARD', 'Das Erste'],
            'arteDe': ['ARTE.de'],
            'arteFr': ['ARTE.fr'],
            'br': ['BR', 'Bayerischer Rundfunk'],
            'dw': ['DW TV', 'Deutsche Welle'],
            'hr': ['HR', 'Hessischer Rundfunk'],
            'kika': ['KiKA', 'Kinderkanal von ARD und ZDF'],
            'mdr': ['MDR', 'Mitteldeutscher Rundfunk'],
            'ndr': ['NDR', 'Norddeutscher Rundfunk'],
            'orf': ['ORF', 'Österreichischer Rundfunk'],
            'phoenix': ['phoenix'],
            'rbb': ['RBB', 'Rundfunk Berlin-Brandenburg'],
            'sr': ['SR', 'Saarländischer Rundfunk'],
            'srf': ['SRF', 'Schweizer Rundfunk'],
            'swr': ['SWR', 'Südwestrundfunk'],
            'wdr': ['WDR', 'Westdeutscher Rundfunk'],
            'zdf': ['ZDF', 'Zweites Deutsches Fernsehen']
        }


    def createActions(self):

        # Actions: Application
        self.actionAbout = QAction(self.tr(f'About {QApplication.applicationName()}'), self)
        self.actionAbout.setObjectName('actionAbout')
        self.actionAbout.setIcon(QIcon(':/icons/apps/16/mediathekview.svg'))
        self.actionAbout.setIconText(self.tr('About'))
        self.actionAbout.setToolTip(self.tr('Brief description of the application'))
        self.actionAbout.triggered.connect(self.onActionAboutTriggered)

        self.actionColophon = QAction(self.tr('Colophon'), self)
        self.actionColophon.setObjectName('actionColophon')
        self.actionColophon.setIconText(self.tr('Colophon'))
        self.actionColophon.setToolTip(self.tr('Lengthy description of the application'))
        self.actionColophon.triggered.connect(self.onActionColophonTriggered)

        self.actionPreferences = QAction(self.tr('Preferences…'), self)
        self.actionPreferences.setObjectName('actionPreferences')
        self.actionPreferences.setIcon(QIcon.fromTheme('configure', QIcon(':/icons/actions/16/application-configure.svg')))
        self.actionPreferences.setIconText(self.tr('Preferences'))
        self.actionPreferences.setToolTip(self.tr('Customize the appearance and behavior of the application'))
        self.actionPreferences.triggered.connect(self.onActionPreferencesTriggered)

        self.actionQuit = QAction(self.tr('Quit'), self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setIcon(QIcon.fromTheme('application-exit', QIcon(':/icons/actions/16/application-exit.svg')))
        self.actionQuit.setIconText(self.tr('Quit'))
        self.actionQuit.setShortcut(QKeySequence.Quit)
        self.actionQuit.setToolTip(self.tr(f'Quit the application [{self.actionQuit.shortcut().toString(QKeySequence.NativeText)}]'))
        self.actionQuit.triggered.connect(self.close)

        # Action: Channels
        self.actionLiveStreams = QAction(self.tr('Live streams'), self)
        self.actionLiveStreams.setObjectName('actionLiveStreams')
        self.actionLiveStreams.setIcon(QIcon.fromTheme('network-wireless-hotspot', QIcon(':/icons/actions/16/live-stream.svg')))
        self.actionLiveStreams.setIconText(self.tr('Live streams'))
        self.actionLiveStreams.setCheckable(True)
        self.actionLiveStreams.setToolTip(self.tr('Show all live streaming channels'))
        self.actionLiveStreams.triggered.connect(lambda checked: self.onActionLiveStreamsToggled(checked))

        self.actionChannels = []
        for it in self.listChannels:

            if len(self.listChannels[it]) > 1:
                text = self.tr(f'{self.listChannels[it][0]} ({self.listChannels[it][1]})')
            else:
                text = f'{self.listChannels[it][0]}'

            channel = QAction(text, self)
            channel.setObjectName(f'actionChannel_{it}')
            channel.setIconText(self.listChannels[it][0])
            channel.setCheckable(True)
            channel.setToolTip(self.tr(f'Show all programs of channel {text}'))
            channel.toggled.connect(lambda checked: self.onActionChannelsToggled(it, checked))

            self.actionChannels.append(channel)


        # Actions: View
        self.actionFullScreen = QAction(self)
        self.actionFullScreen.setCheckable(True)
        self.actionFullScreen.setIconText(self.tr('Full Screen'))
        self.actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self.actionFullScreen.triggered.connect(self.onActionFullScreenTriggered)

        self.actionToolbarApplication = QAction(self.tr('Show Application Toolbar'), self)
        self.actionToolbarApplication.setObjectName('actionToolbarApplication')
        self.actionToolbarApplication.setCheckable(True)
        self.actionToolbarApplication.setChecked(True)
        self.actionToolbarApplication.setToolTip(self.tr('Display the Application toolbar'))
        self.actionToolbarApplication.toggled.connect(lambda checked: self.toolbarApplication.setVisible(checked))

        self.actionToolbarChannels = QAction(self.tr('Show Channels Toolbar'), self)
        self.actionToolbarChannels.setObjectName('actionToolbarChannels')
        self.actionToolbarChannels.setCheckable(True)
        self.actionToolbarChannels.setChecked(True)
        self.actionToolbarChannels.setToolTip(self.tr('Display the Channels toolbar'))
        self.actionToolbarChannels.toggled.connect(lambda checked: self.toolbarChannels.setVisible(checked))

        self.actionToolbarView = QAction(self.tr('Show View Toolbar'), self)
        self.actionToolbarView.setObjectName('actionToolbarView')
        self.actionToolbarView.setCheckable(True)
        self.actionToolbarView.setChecked(True)
        self.actionToolbarView.setToolTip(self.tr('Display the View toolbar'))
        self.actionToolbarView.toggled.connect(lambda checked: self.toolbarView.setVisible(checked))


    def updateActionFullScreen(self):

        if not self.isFullScreen():
            self.actionFullScreen.setText(self.tr('Full Screen Mode'))
            self.actionFullScreen.setIcon(QIcon.fromTheme('view-fullscreen', QIcon(':/icons/actions/16/view-fullscreen.svg')))
            self.actionFullScreen.setChecked(False)
            self.actionFullScreen.setToolTip(self.tr(f'Display the window in full screen [{self.actionFullScreen.shortcut().toString(QKeySequence.NativeText)}]'))
        else:
            self.actionFullScreen.setText(self.tr('Exit Full Screen Mode'))
            self.actionFullScreen.setIcon(QIcon.fromTheme('view-restore', QIcon(':/icons/actions/16/view-restore.svg')))
            self.actionFullScreen.setChecked(True)
            self.actionFullScreen.setToolTip(self.tr(f'Exit the full screen mode [{self.actionFullScreen.shortcut().toString(QKeySequence.NativeText)}]'))


    def createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr('Application'))
        menuApplication.setObjectName('menuApplication')
        menuApplication.addAction(self.actionAbout)
        menuApplication.addAction(self.actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self.actionQuit)

        # Menu: Channels
        menuChannels = self.menuBar().addMenu(self.tr('Channels'))
        menuChannels.setObjectName('menuChannels')
        menuChannels.addAction(self.actionLiveStreams)
        menuChannels.addSeparator()
        menuChannels.addActions(self.actionChannels)

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr('View'))
        menuView.setObjectName('menuView')
        menuView.addAction(self.actionFullScreen)
        menuView.addSeparator()
        menuView.addAction(self.actionToolbarApplication)
        menuView.addAction(self.actionToolbarChannels)
        menuView.addAction(self.actionToolbarView)


    def createToolbars(self):

        # Toolbar: Application
        self.toolbarApplication = self.addToolBar(self.tr('Application Toolbar'))
        self.toolbarApplication.setObjectName('toolbarApplication')
        self.toolbarApplication.addAction(self.actionAbout)
        self.toolbarApplication.addAction(self.actionPreferences)
        self.toolbarApplication.addSeparator()
        self.toolbarApplication.addAction(self.actionQuit)
        self.toolbarApplication.visibilityChanged.connect(lambda visible: self.actionToolbarApplication.setChecked(visible))

        # Toolbar: Channels
        self.toolbarChannels = self.addToolBar(self.tr('View Channels'))
        self.toolbarChannels.setObjectName('toolbarChannels')
        self.toolbarChannels.addAction(self.actionLiveStreams)
        self.toolbarChannels.addSeparator()
        self.toolbarChannels.addActions(self.actionChannels)
        self.toolbarChannels.visibilityChanged.connect(lambda visible: self.actionToolbarChannels.setChecked(visible))

        # Toolbar: View
        self.toolbarView = self.addToolBar(self.tr('View Toolbar'))
        self.toolbarView.setObjectName('toolbarView')
        self.toolbarView.addAction(self.actionFullScreen)
        self.toolbarView.visibilityChanged.connect(lambda visible: self.actionToolbarView.setChecked(visible))


    def setApplicationGeometry(self, geometry = QByteArray()):

        if geometry:
            self.restoreGeometry(geometry)
        else:
            availableGeometry = QRect(QApplication.desktop().availableGeometry(self))
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def applicationGeometry(self):

        return self.saveGeometry()


    def setApplicationState(self, state = QByteArray()):

        if state:
            self.restoreState(state)
        else:
            self.actionToolbarView.setChecked(False)


    def applicationState(self):

        self.saveState()


    def onActionAboutTriggered(self):

        geometry = QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()


    def onActionColophonTriggered(self):

        geometry = QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()


    def onActionPreferencesTriggered(self):
        pass


    def onActionLiveStreamsToggled(self, checked):
        pass


    def onActionChannelsToggled(self, channel, checked):
        pass


    def onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self.updateActionFullScreen()
