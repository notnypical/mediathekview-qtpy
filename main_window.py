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

from PySide2.QtCore import QByteArray, QSettings, Qt
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from preferences import Preferences
from preferences_dialog import PreferencesDialog

import icons


class MainWindow(QMainWindow):

    _preferences = Preferences()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(':/icons/apps/16/mediathekview.svg'))

        self.loadSettings()

        self.createChannels()

        self.createActions()
        self.createMenus()
        self.createToolBars()

        # Application properties
        self.setApplicationState(self._applicationState)
        self.setApplicationGeometry(self._applicationGeometry)

        self.updateActionChannels()
        self.updateActionFullScreen()


    def setApplicationState(self, state=QByteArray()):

        if not state.isEmpty():
            self.restoreState(state)
        else:
            self.toolbarApplication.setVisible(True)
            self.toolbarChannels.setVisible(True)
            self.toolbarTools.setVisible(True)
            self.toolbarView.setVisible(False)
            self.toolbarHelp.setVisible(False)


    def applicationState(self):

        return self.saveState()


    def setApplicationGeometry(self, geometry=QByteArray()):

        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)


    def applicationGeometry(self):

        return self.saveGeometry()


    def closeEvent(self, event):

        if True:
            # Application properties
            self._applicationState = self.applicationState() if self._preferences.restoreApplicationState() else QByteArray()
            self._applicationGeometry = self.applicationGeometry() if self._preferences.restoreApplicationGeometry() else QByteArray()

            self.saveSettings()
            event.accept()
        else:
            event.ignore()


    def loadSettings(self):

        settings = QSettings()

        # Preferences
        self._preferences.load(settings)

        # Application and dialog properties
        self._applicationState = settings.value('Application/State', QByteArray()) if self._preferences.restoreApplicationState() else QByteArray()
        self._applicationGeometry = settings.value('Application/Geometry', QByteArray()) if self._preferences.restoreApplicationGeometry() else QByteArray()
        self._aboutDialogGeometry = settings.value('AboutDialog/Geometry', QByteArray())
        self._colophonDialogGeometry = settings.value('ColophonDialog/Geometry', QByteArray())
        self._preferencesDialogGeometry = settings.value('PreferencesDialog/Geometry', QByteArray())


    def saveSettings(self):

        settings = QSettings()

        # Preferences
        self._preferences.save(settings)

        # Application and dialog properties
        settings.setValue('Application/State', self._applicationState)
        settings.setValue('Application/Geometry', self._applicationGeometry)
        settings.setValue('AboutDialog/Geometry', self._aboutDialogGeometry)
        settings.setValue('ColophonDialog/Geometry', self._colophonDialogGeometry)
        settings.setValue('PreferencesDialog/Geometry', self._preferencesDialogGeometry)


    def createChannels(self):

        self.listChannels = {
            '3sat': [self.tr('3sat'), None],
            'ard': [self.tr('ARD'), self.tr('Das Erste')],
            'arteDe': [self.tr('ARTE.de'), None],
            'arteFr': [self.tr('ARTE.fr'), None],
            'br': [self.tr('BR'), self.tr('Bayerischer Rundfunk')],
            'dw': [self.tr('DW TV'), self.tr('Deutsche Welle')],
            'hr': [self.tr('HR'), self.tr('Hessischer Rundfunk')],
            'kika': [self.tr('KiKA'), self.tr('Kinderkanal von ARD und ZDF')],
            'mdr': [self.tr('MDR'), self.tr('Mitteldeutscher Rundfunk')],
            'ndr': [self.tr('NDR'), self.tr('Norddeutscher Rundfunk')],
            'orf': [self.tr('ORF'), self.tr('Österreichischer Rundfunk')],
            'phoenix': [self.tr('phoenix'), None],
            'rbb': [self.tr('RBB'), self.tr('Rundfunk Berlin-Brandenburg')],
            'sr': [self.tr('SR'), self.tr('Saarländischer Rundfunk')],
            'srf': [self.tr('SRF'), self.tr('Schweizer Rundfunk')],
            'swr': [self.tr('SWR'), self.tr('Südwestrundfunk')],
            'wdr': [self.tr('WDR'), self.tr('Westdeutscher Rundfunk')],
            'zdf': [self.tr('ZDF'), self.tr('Zweites Deutsches Fernsehen')]
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
        self.actionLiveStreams = QAction(self.tr('Live Streams'), self)
        self.actionLiveStreams.setObjectName('actionLiveStreams')
        self.actionLiveStreams.setIcon(QIcon.fromTheme('network-wireless-hotspot', QIcon(':/icons/actions/16/live-stream.svg')))
        self.actionLiveStreams.setIconText(self.tr('Live'))
        self.actionLiveStreams.setCheckable(True)
        self.actionLiveStreams.setToolTip(self.tr('Show all live streaming channels'))
        self.actionLiveStreams.toggled.connect(lambda checked: self.onActionLiveStreamsToggled(checked))

        self.actionChannels = []
        for key, value in sorted(self.listChannels.items()):

            text = self.tr(f'{value[0]} ({value[1]})') if value[1] else value[0]

            actionChannel = QAction(text, self)
            actionChannel.setObjectName(f'actionChannel_{key}')
            actionChannel.setIconText(value[0])
            actionChannel.setCheckable(True)
            actionChannel.setData(key)
            actionChannel.toggled.connect(lambda checked, channel=actionChannel.data() : self.onActionChannelsToggled(checked, channel))

            self.actionChannels.append(actionChannel)

        self.actionSelectInvert = QAction(self.tr('Invert Selection'), self)
        self.actionSelectInvert.setObjectName('actionSelectInvert')
        self.actionSelectInvert.setIcon(QIcon.fromTheme('edit-select-invert', QIcon(':/icons/actions/16/edit-select-invert.svg')))
        self.actionSelectInvert.setIconText(self.tr('Invert'))
        self.actionSelectInvert.setCheckable(True)
        self.actionSelectInvert.setToolTip(self.tr('Invert list of selected channels'))
        self.actionSelectInvert.toggled.connect(lambda checked: self.onActionSelectInvertToggled(checked))

        # Actions: Tools
        self.actionUpdate = QAction(self.tr('Update Database'), self)
        self.actionUpdate.setObjectName('actionUpdate')
        self.actionUpdate.setIcon(QIcon.fromTheme('edit-download', QIcon(':/icons/actions/16/edit-download.svg')))
        self.actionUpdate.setIconText(self.tr('Update'))
        self.actionUpdate.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F5))
        self.actionUpdate.setToolTip(self.tr(f'Update the local database [{self.actionUpdate.shortcut().toString(QKeySequence.NativeText)}]'))
        self.actionUpdate.triggered.connect(self.onActionUpdateTriggered)

        # Actions: View
        self.actionFullScreen = QAction(self)
        self.actionFullScreen.setObjectName('actionFullScreen')
        self.actionFullScreen.setIconText(self.tr('Full Screen'))
        self.actionFullScreen.setCheckable(True)
        self.actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self.actionFullScreen.triggered.connect(self.onActionFullScreenTriggered)

        self.actionToolbarApplication = QAction(self.tr('Show Application Toolbar'), self)
        self.actionToolbarApplication.setObjectName('actionToolbarApplication')
        self.actionToolbarApplication.setCheckable(True)
        self.actionToolbarApplication.setToolTip(self.tr('Display the Application toolbar'))
        self.actionToolbarApplication.toggled.connect(lambda checked: self.toolbarApplication.setVisible(checked))

        self.actionToolbarChannels = QAction(self.tr('Show Channels Toolbar'), self)
        self.actionToolbarChannels.setObjectName('actionToolbarChannels')
        self.actionToolbarChannels.setCheckable(True)
        self.actionToolbarChannels.setToolTip(self.tr('Display the Channels toolbar'))
        self.actionToolbarChannels.toggled.connect(lambda checked: self.toolbarChannels.setVisible(checked))

        self.actionToolbarTools = QAction(self.tr('Show Tools Toolbar'), self)
        self.actionToolbarTools.setObjectName('actionToolbarTools')
        self.actionToolbarTools.setCheckable(True)
        self.actionToolbarTools.setToolTip(self.tr('Display the Tools toolbar'))
        self.actionToolbarTools.toggled.connect(lambda checked: self.toolbarTools.setVisible(checked))

        self.actionToolbarView = QAction(self.tr('Show View Toolbar'), self)
        self.actionToolbarView.setObjectName('actionToolbarView')
        self.actionToolbarView.setCheckable(True)
        self.actionToolbarView.setToolTip(self.tr('Display the View toolbar'))
        self.actionToolbarView.toggled.connect(lambda checked: self.toolbarView.setVisible(checked))

        self.actionToolbarHelp = QAction(self.tr('Show Help Toolbar'), self)
        self.actionToolbarHelp.setObjectName('actionToolbarHelp')
        self.actionToolbarHelp.setCheckable(True)
        self.actionToolbarHelp.setToolTip(self.tr('Display the Help toolbar'))
        self.actionToolbarHelp.toggled.connect(lambda checked: self.toolbarHelp.setVisible(checked))


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
        menuChannels.addSeparator()
        menuChannels.addAction(self.actionSelectInvert)

        # Menu: Tools
        menuTools = self.menuBar().addMenu(self.tr('Tools'))
        menuTools.setObjectName('menuTools')
        menuTools.addAction(self.actionUpdate)

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr('View'))
        menuView.setObjectName('menuView')
        menuView.addAction(self.actionFullScreen)
        menuView.addSeparator()
        menuView.addAction(self.actionToolbarApplication)
        menuView.addAction(self.actionToolbarChannels)
        menuView.addAction(self.actionToolbarTools)
        menuView.addAction(self.actionToolbarView)
        menuView.addAction(self.actionToolbarHelp)

        # Menu: help
        menuHelp = self.menuBar().addMenu(self.tr('Help'))
        menuHelp.setObjectName('menuHelp')


    def createToolBars(self):

        # Toolbar: Application
        self.toolbarApplication = self.addToolBar(self.tr('Application Toolbar'))
        self.toolbarApplication.setObjectName('toolbarApplication')
        self.toolbarApplication.addAction(self.actionAbout)
        self.toolbarApplication.addAction(self.actionPreferences)
        self.toolbarApplication.addSeparator()
        self.toolbarApplication.addAction(self.actionQuit)
        self.toolbarApplication.visibilityChanged.connect(lambda visible: self.actionToolbarApplication.setChecked(visible))

        # Toolbar: Channels
        self.toolbarChannels = self.addToolBar(self.tr('Channels Toolbar'))
        self.toolbarChannels.setObjectName('toolbarChannels')
        self.toolbarChannels.setStyleSheet('*[invertChannel=true] { text-decoration: line-through; }')
        self.toolbarChannels.addAction(self.actionLiveStreams)
        self.toolbarChannels.addSeparator()
        self.toolbarChannels.addActions(self.actionChannels)
        self.toolbarChannels.addSeparator()
        self.toolbarChannels.addAction(self.actionSelectInvert)
        self.toolbarChannels.visibilityChanged.connect(lambda visible: self.actionToolbarChannels.setChecked(visible))

        # Toolbar: Tools
        self.toolbarTools = self.addToolBar(self.tr('Tools Toolbar'))
        self.toolbarTools.setObjectName('toolbarTools')
        self.toolbarTools.addAction(self.actionUpdate)
        self.toolbarTools.visibilityChanged.connect(lambda visible: self.actionToolbarTools.setChecked(visible))

        # Toolbar: View
        self.toolbarView = self.addToolBar(self.tr('View Toolbar'))
        self.toolbarView.setObjectName('toolbarView')
        self.toolbarView.addAction(self.actionFullScreen)
        self.toolbarView.visibilityChanged.connect(lambda visible: self.actionToolbarView.setChecked(visible))

        # Toolbar: Help
        self.toolbarHelp = self.addToolBar(self.tr('Help Toolbar'))
        self.toolbarHelp.setObjectName('toolbarHelp')
        self.toolbarHelp.visibilityChanged.connect(lambda visible: self.actionToolbarHelp.setChecked(visible))


    def updateActionChannels(self, invert=False):

        # Tool buttons
        for idx in range(len(self.actionChannels)):

            widget = self.toolbarChannels.widgetForAction(self.actionChannels[idx])
            widget.setProperty('invertChannel', invert)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

            if not invert:
                self.actionChannels[idx].setToolTip(self.tr(f'Show all programs of channel {self.actionChannels[idx].text()}'))
            else:
                self.actionChannels[idx].setToolTip(self.tr(f'Hide all programs of channel {self.actionChannels[idx].text()}'))


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


    def onActionAboutTriggered(self):

        geometry = self._aboutDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = AboutDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self._aboutDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionColophonTriggered(self):

        geometry = self._colophonDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = ColophonDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.exec_()

        self._colophonDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionPreferencesTriggered(self):

        geometry = self._preferencesDialogGeometry if self._preferences.restoreDialogGeometry() else QByteArray()

        dialog = PreferencesDialog(self)
        dialog.setDialogGeometry(geometry)
        dialog.setPreferences(self._preferences)
        dialog.exec_()

        self._preferences = dialog.preferences()
        self._preferencesDialogGeometry = dialog.dialogGeometry() if self._preferences.restoreDialogGeometry() else QByteArray()


    def onActionLiveStreamsToggled(self, checked):
        pass


    def onActionChannelsToggled(self, checked, channel):
        pass


    def onActionSelectInvertToggled(self, checked):

        self.updateActionChannels(checked)


    def onActionUpdateTriggered(self):
        pass


    def onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self.updateActionFullScreen()
