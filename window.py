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

from PySide2.QtCore import QByteArray, QSettings, Qt, Signal
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QStatusBar

from about_dialog import AboutDialog
from colophon_dialog import ColophonDialog
from keyboard_shortcuts_dialog import KeyboardShortcutsDialog
from preferences import Preferences
from preferences_dialog import PreferencesDialog

import icons_rc


class Window(QMainWindow):

    actionTextChanged = Signal()


    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon(":/icons/apps/16/mediathekview.svg"))

        self._keyboardShortcutsDialog = None

        self._preferences = Preferences()
        self._preferences.loadSettings()

        self._createChannels()

        self._createActions()
        self._createMenus()
        self._createToolBars()
        self._createStatusBar()

        self._loadSettings()

        self._updateActionFullScreen()
        self._updateActionsChannels()


    def closeEvent(self, event):

        if True:
            # Store application properties and preferences
            self._saveSettings()
            self._preferences.saveSettings()

            event.accept()
        else:
            event.ignore()


    def _loadSettings(self):

        settings = QSettings()

        # Application properties: Geometry
        geometry = settings.value("Application/Geometry", QByteArray()) if self._preferences.restoreApplicationGeometry() else QByteArray()
        if not geometry.isEmpty():
            self.restoreGeometry(geometry)
        else:
            availableGeometry = self.screen().availableGeometry()
            self.resize(availableGeometry.width() * 2/3, availableGeometry.height() * 2/3)
            self.move((availableGeometry.width() - self.width()) / 2, (availableGeometry.height() - self.height()) / 2)

        # Application properties: State
        state = settings.value("Application/State", QByteArray()) if self._preferences.restoreApplicationState() else QByteArray()
        if not state.isEmpty():
            self.restoreState(state)
        else:
            self._toolbarApplication.setVisible(True)
            self._toolbarChannels.setVisible(True)
            self._toolbarTools.setVisible(True)
            self._toolbarView.setVisible(False)
            self._toolbarHelp.setVisible(False)


    def _saveSettings(self):

        settings = QSettings()

        # Application properties: Geometry
        geometry = self.saveGeometry() if self._preferences.restoreApplicationGeometry() else QByteArray()
        settings.setValue("Application/Geometry", geometry)

        # Application properties: State
        state = self.saveState() if self._preferences.restoreApplicationState() else QByteArray()
        settings.setValue("Application/State", state)


    def _createChannels(self):

        self._listChannels = {
            "3sat": [self.tr("3sat"), None],
            "ard": [self.tr("ARD"), self.tr("Das Erste")],
            "arteDe": [self.tr("ARTE.de"), None],
            "arteFr": [self.tr("ARTE.fr"), None],
            "br": [self.tr("BR"), self.tr("Bayerischer Rundfunk")],
            "dw": [self.tr("DW TV"), self.tr("Deutsche Welle")],
            "hr": [self.tr("HR"), self.tr("Hessischer Rundfunk")],
            "kika": [self.tr("KiKA"), self.tr("Kinderkanal von ARD und ZDF")],
            "mdr": [self.tr("MDR"), self.tr("Mitteldeutscher Rundfunk")],
            "ndr": [self.tr("NDR"), self.tr("Norddeutscher Rundfunk")],
            "orf": [self.tr("ORF"), self.tr("Österreichischer Rundfunk")],
            "phoenix": [self.tr("phoenix"), None],
            "rbb": [self.tr("RBB"), self.tr("Rundfunk Berlin-Brandenburg")],
            "sr": [self.tr("SR"), self.tr("Saarländischer Rundfunk")],
            "srf": [self.tr("SRF"), self.tr("Schweizer Rundfunk")],
            "swr": [self.tr("SWR"), self.tr("Südwestrundfunk")],
            "wdr": [self.tr("WDR"), self.tr("Westdeutscher Rundfunk")],
            "zdf": [self.tr("ZDF"), self.tr("Zweites Deutsches Fernsehen")]
        }


    def _createActions(self):

        #
        # Actions: Application

        self._actionAbout = QAction(self.tr("About {0}").format(QApplication.applicationName()), self)
        self._actionAbout.setObjectName("actionAbout")
        self._actionAbout.setIcon(QIcon(":/icons/apps/16/mediathekview.svg"))
        self._actionAbout.setIconText(self.tr("About"))
        self._actionAbout.setToolTip(self.tr("Brief description of the application"))
        self._actionAbout.triggered.connect(self._onActionAboutTriggered)

        self._actionColophon = QAction(self.tr("Colophon"), self)
        self._actionColophon.setObjectName("actionColophon")
        self._actionColophon.setToolTip(self.tr("Lengthy description of the application"))
        self._actionColophon.triggered.connect(self._onActionColophonTriggered)

        self._actionPreferences = QAction(self.tr("Preferences…"), self)
        self._actionPreferences.setObjectName("actionPreferences")
        self._actionPreferences.setIcon(QIcon.fromTheme("configure", QIcon(":/icons/actions/16/application-configure.svg")))
        self._actionPreferences.setToolTip(self.tr("Customize the appearance and behavior of the application"))
        self._actionPreferences.triggered.connect(self._onActionPreferencesTriggered)

        self._actionQuit = QAction(self.tr("Quit"), self)
        self._actionQuit.setObjectName("actionQuit")
        self._actionQuit.setIcon(QIcon.fromTheme("application-exit", QIcon(":/icons/actions/16/application-exit.svg")))
        self._actionQuit.setShortcut(QKeySequence.Quit)
        self._actionQuit.setToolTip(self.tr("Quit the application"))
        self._actionQuit.triggered.connect(self.close)


        #
        # Action: Channels

        self._actionLiveStreams = QAction(self.tr("Live Streams"), self)
        self._actionLiveStreams.setObjectName("actionLiveStreams")
        self._actionLiveStreams.setIcon(QIcon.fromTheme("network-wireless-hotspot", QIcon(":/icons/actions/16/live-stream.svg")))
        self._actionLiveStreams.setIconText(self.tr("Live"))
        self._actionLiveStreams.setCheckable(True)
        self._actionLiveStreams.setToolTip(self.tr("Show all live streaming channels"))
        self._actionLiveStreams.toggled.connect(lambda checked: self._onActionLiveStreamsToggled(checked))

        self._actionsChannels = []
        for key, value in sorted(self._listChannels.items()):

            text = self.tr("{0} ({1})").format(value[0], value[1]) if value[1] else value[0]

            actionChannel = QAction(text, self)
            actionChannel.setObjectName(f"actionChannel_{key}")
            actionChannel.setIconText(value[0])
            actionChannel.setCheckable(True)
            actionChannel.setData(key)
            actionChannel.toggled.connect(lambda checked, channel=actionChannel.data() : self._onActionChannelToggled(checked, channel))

            self._actionsChannels.append(actionChannel)

        self._actionSelectInvert = QAction(self.tr("Invert Selection"), self)
        self._actionSelectInvert.setObjectName("actionSelectInvert")
        self._actionSelectInvert.setIcon(QIcon.fromTheme("edit-select-invert", QIcon(":/icons/actions/16/edit-select-invert.svg")))
        self._actionSelectInvert.setIconText(self.tr("Invert"))
        self._actionSelectInvert.setCheckable(True)
        self._actionSelectInvert.setToolTip(self.tr("Invert list of selected channels"))
        self._actionSelectInvert.toggled.connect(lambda checked: self._onActionSelectInvertToggled(checked))


        #
        # Actions: Tools

        self._actionUpdate = QAction(self.tr("Update Database"), self)
        self._actionUpdate.setObjectName("actionUpdate")
        self._actionUpdate.setIcon(QIcon.fromTheme("edit-download", QIcon(":/icons/actions/16/edit-download.svg")))
        self._actionUpdate.setIconText(self.tr("Update"))
        self._actionUpdate.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_F5))
        self._actionUpdate.setToolTip(self.tr("Update the local database"))
        self._actionUpdate.triggered.connect(self._onActionUpdateTriggered)


        #
        # Actions: View

        self._actionFullScreen = QAction(self)
        self._actionFullScreen.setObjectName("actionFullScreen")
        self._actionFullScreen.setIconText(self.tr("Full Screen"))
        self._actionFullScreen.setCheckable(True)
        self._actionFullScreen.setShortcuts([QKeySequence(Qt.Key_F11), QKeySequence.FullScreen])
        self._actionFullScreen.triggered.connect(self._onActionFullScreenTriggered)

        self._actionToolbarApplication = QAction(self.tr("Show Application Toolbar"), self)
        self._actionToolbarApplication.setObjectName("actionToolbarApplication")
        self._actionToolbarApplication.setCheckable(True)
        self._actionToolbarApplication.setToolTip(self.tr("Display the Application toolbar"))
        self._actionToolbarApplication.toggled.connect(lambda checked: self._toolbarApplication.setVisible(checked))

        self._actionToolbarChannels = QAction(self.tr("Show Channels Toolbar"), self)
        self._actionToolbarChannels.setObjectName("actionToolbarChannels")
        self._actionToolbarChannels.setCheckable(True)
        self._actionToolbarChannels.setToolTip(self.tr("Display the Channels toolbar"))
        self._actionToolbarChannels.toggled.connect(lambda checked: self._toolbarChannels.setVisible(checked))

        self._actionToolbarTools = QAction(self.tr("Show Tools Toolbar"), self)
        self._actionToolbarTools.setObjectName("actionToolbarTools")
        self._actionToolbarTools.setCheckable(True)
        self._actionToolbarTools.setToolTip(self.tr("Display the Tools toolbar"))
        self._actionToolbarTools.toggled.connect(lambda checked: self._toolbarTools.setVisible(checked))

        self._actionToolbarView = QAction(self.tr("Show View Toolbar"), self)
        self._actionToolbarView.setObjectName("actionToolbarView")
        self._actionToolbarView.setCheckable(True)
        self._actionToolbarView.setToolTip(self.tr("Display the View toolbar"))
        self._actionToolbarView.toggled.connect(lambda checked: self._toolbarView.setVisible(checked))

        self._actionToolbarHelp = QAction(self.tr("Show Help Toolbar"), self)
        self._actionToolbarHelp.setObjectName("actionToolbarHelp")
        self._actionToolbarHelp.setCheckable(True)
        self._actionToolbarHelp.setToolTip(self.tr("Display the Help toolbar"))
        self._actionToolbarHelp.toggled.connect(lambda checked: self._toolbarHelp.setVisible(checked))

        self._actionStatusbar = QAction(self.tr("Show Statusbar"), self)
        self._actionStatusbar.setObjectName("actionStatusbar")
        self._actionStatusbar.setCheckable(True)
        self._actionStatusbar.setChecked(True)
        self._actionStatusbar.setToolTip(self.tr("Display the statusbar"))
        self._actionStatusbar.toggled.connect(lambda checked: self._statusbar.setVisible(checked))


        #
        # Actions: Help

        self._actionKeyboardShortcuts = QAction(self.tr("Keyboard Shortcuts"), self)
        self._actionKeyboardShortcuts.setObjectName("actionKeyboardShortcuts")
        self._actionKeyboardShortcuts.setIcon(QIcon.fromTheme("help-keyboard-shortcuts", QIcon(":/icons/actions/16/help-keyboard-shortcuts.svg")))
        self._actionKeyboardShortcuts.setIconText(self.tr("Shortcuts"))
        self._actionKeyboardShortcuts.setToolTip(self.tr("List of all keyboard shortcuts"))
        self._actionKeyboardShortcuts.triggered.connect(self._onActionKeyboardShortcutsTriggered)


    def _createMenus(self):

        # Menu: Application
        menuApplication = self.menuBar().addMenu(self.tr("Application"))
        menuApplication.setObjectName("menuApplication")
        menuApplication.addAction(self._actionAbout)
        menuApplication.addAction(self._actionColophon)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionPreferences)
        menuApplication.addSeparator()
        menuApplication.addAction(self._actionQuit)

        # Menu: Channels
        menuChannels = self.menuBar().addMenu(self.tr("Channels"))
        menuChannels.setObjectName("menuChannels")
        menuChannels.addAction(self._actionLiveStreams)
        menuChannels.addSeparator()
        menuChannels.addActions(self._actionsChannels)
        menuChannels.addSeparator()
        menuChannels.addAction(self._actionSelectInvert)

        # Menu: Tools
        menuTools = self.menuBar().addMenu(self.tr("Tools"))
        menuTools.setObjectName("menuTools")
        menuTools.addAction(self._actionUpdate)

        # Menu: View
        menuView = self.menuBar().addMenu(self.tr("View"))
        menuView.setObjectName("menuView")
        menuView.addAction(self._actionFullScreen)
        menuView.addSeparator()
        menuView.addAction(self._actionToolbarApplication)
        menuView.addAction(self._actionToolbarChannels)
        menuView.addAction(self._actionToolbarTools)
        menuView.addAction(self._actionToolbarView)
        menuView.addAction(self._actionToolbarHelp)
        menuView.addSeparator()
        menuView.addAction(self._actionStatusbar)

        # Menu: Help
        menuHelp = self.menuBar().addMenu(self.tr("Help"))
        menuHelp.setObjectName("menuHelp")
        menuHelp.addAction(self._actionKeyboardShortcuts)


    def _createToolBars(self):

        # Toolbar: Application
        self._toolbarApplication = self.addToolBar(self.tr("Application Toolbar"))
        self._toolbarApplication.setObjectName("toolbarApplication")
        self._toolbarApplication.addAction(self._actionAbout)
        self._toolbarApplication.addAction(self._actionPreferences)
        self._toolbarApplication.addSeparator()
        self._toolbarApplication.addAction(self._actionQuit)
        self._toolbarApplication.visibilityChanged.connect(lambda visible: self._actionToolbarApplication.setChecked(visible))

        # Toolbar: Channels
        self._toolbarChannels = self.addToolBar(self.tr("Channels Toolbar"))
        self._toolbarChannels.setObjectName("toolbarChannels")
        self._toolbarChannels.setStyleSheet("*[invertChannel=true] { text-decoration: line-through; }")
        self._toolbarChannels.addAction(self._actionLiveStreams)
        self._toolbarChannels.addSeparator()
        self._toolbarChannels.addActions(self._actionsChannels)
        self._toolbarChannels.addSeparator()
        self._toolbarChannels.addAction(self._actionSelectInvert)
        self._toolbarChannels.visibilityChanged.connect(lambda visible: self._actionToolbarChannels.setChecked(visible))

        # Toolbar: Tools
        self._toolbarTools = self.addToolBar(self.tr("Tools Toolbar"))
        self._toolbarTools.setObjectName("toolbarTools")
        self._toolbarTools.addAction(self._actionUpdate)
        self._toolbarTools.visibilityChanged.connect(lambda visible: self._actionToolbarTools.setChecked(visible))

        # Toolbar: View
        self._toolbarView = self.addToolBar(self.tr("View Toolbar"))
        self._toolbarView.setObjectName("toolbarView")
        self._toolbarView.addAction(self._actionFullScreen)
        self._toolbarView.visibilityChanged.connect(lambda visible: self._actionToolbarView.setChecked(visible))

        # Toolbar: Help
        self._toolbarHelp = self.addToolBar(self.tr("Help Toolbar"))
        self._toolbarHelp.setObjectName("toolbarHelp")
        self._toolbarHelp.addAction(self._actionKeyboardShortcuts)
        self._toolbarHelp.visibilityChanged.connect(lambda visible: self._actionToolbarHelp.setChecked(visible))


    def _createStatusBar(self):

        self._statusbar = self.statusBar()


    def _updateActionFullScreen(self):

        if not self.isFullScreen():
            self._actionFullScreen.setText(self.tr("Full Screen Mode"))
            self._actionFullScreen.setIcon(QIcon.fromTheme("view-fullscreen", QIcon(":/icons/actions/16/view-fullscreen.svg")))
            self._actionFullScreen.setChecked(False)
            self._actionFullScreen.setToolTip(self.tr("Display the window in full screen"))
        else:
            self._actionFullScreen.setText(self.tr("Exit Full Screen Mode"))
            self._actionFullScreen.setIcon(QIcon.fromTheme("view-restore", QIcon(":/icons/actions/16/view-restore.svg")))
            self._actionFullScreen.setChecked(True)
            self._actionFullScreen.setToolTip(self.tr("Exit the full screen mode"))

        self.actionTextChanged.emit();


    def _updateActionsChannels(self, invert=False):

        # Tool buttons
        for idx in range(len(self._actionsChannels)):

            widget = self._toolbarChannels.widgetForAction(self._actionsChannels[idx])
            widget.setProperty("invertChannel", invert)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

            if not invert:
                self._actionsChannels[idx].setToolTip(self.tr("Show all programs of channel {0}").format(self._actionsChannels[idx].text()))
            else:
                self._actionsChannels[idx].setToolTip(self.tr("Hide all programs of channel {0}").format(self._actionsChannels[idx].text()))


    def _onActionAboutTriggered(self):

        dialog = AboutDialog(self)
        dialog.exec_()


    def _onActionColophonTriggered(self):

        dialog = ColophonDialog(self)
        dialog.exec_()


    def _onActionPreferencesTriggered(self):

        dialog = PreferencesDialog(self)
        dialog.setPreferences(self._preferences)
        dialog.exec_()

        self._preferences = dialog.preferences()


    def _onActionLiveStreamsToggled(self, checked):
        pass


    def _onActionChannelToggled(self, checked, channel):
        pass


    def _onActionSelectInvertToggled(self, checked):

        self._updateActionsChannels(checked)


    def _onActionUpdateTriggered(self):
        pass


    def _onActionFullScreenTriggered(self):

        if not self.isFullScreen():
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        else:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)

        self._updateActionFullScreen()


    def _onActionKeyboardShortcutsTriggered(self):

        if not self._keyboardShortcutsDialog:
            self._keyboardShortcutsDialog = KeyboardShortcutsDialog(self)
            self.actionTextChanged.connect(self._keyboardShortcutsDialog.actionTextChanged)

        self._keyboardShortcutsDialog.show()
        self._keyboardShortcutsDialog.raise_()
        self._keyboardShortcutsDialog.activateWindow()
