# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CompulinkToolsPlugin
                                 A QGIS plugin
 Compulink QGIS tools
                              -------------------
        begin                : 2014-10-31
        git sha              : $Format:%H$
        copyright            : (C) 2014 by NextGIS
        email                : info@nextgis.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
# import resources_rc
# Import the code for the dialog
from qgis.core import QgsMapLayerRegistry, QgsRasterLayer, QgsMessageLog
from qgis.gui import QgsMessageBar
import os.path
from settings_dialog import SettingsDialog


class CompulinkToolsPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CompulinkToolsPlugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Compulink tools')
        self.toolbar = self.iface.addToolBar(u'CompulinkToolsPlugin')
        self.toolbar.setObjectName(u'CompulinkToolsPlugin')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CompulinkToolsPlugin', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def add_group_separator(self,
                            add_to_menu=True,
                            add_to_toolbar=True,
                            parent=None):

        sep_action = QAction(parent)
        sep_action.setSeparator(True)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, sep_action)

        if add_to_toolbar:
            self.toolbar.addAction(sep_action)

        self.actions.append(sep_action)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #Tools for NGW communicate
        icon_path = self.plugin_dir + '/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Add projects layers'),
            callback=self.add_layers_from_ngw,
            parent=self.iface.mainWindow())

        #Tools for add external resources
        self.add_group_separator()
        icon_path = self.plugin_dir + '/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Add ZOUIT layer'),
            callback=self.add_zouit_layer,
            parent=self.iface.mainWindow())

        #Settings
        self.add_group_separator()
        icon_path = self.plugin_dir + '/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Settings'),
            callback=self.settings,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Compulink tools'),
                action)
            self.iface.removeToolBarIcon(action)

    def add_layers_from_ngw(self):
        pass

    def add_zouit_layer(self):
        path = os.path.join(self.plugin_dir, 'external_sources/zouit.xml')
        layer = QgsRasterLayer(path, self.tr('ZOUIT'))
        if not layer.isValid():
            error_message = self.tr('Layer ZOUIT can\'t be added to the map!')
            self.iface.messageBar().pushMessage(self.tr('Error'),
                                                error_message,
                                                level=QgsMessageBar.CRITICAL)
            QgsMessageLog.logMessage(error_message, level=QgsMessageLog.CRITICAL)
        else:
            layer.renderer().setOpacity(0.7)
            QgsMapLayerRegistry.instance().addMapLayer(layer)


    def settings(self):
        sett_dialog = SettingsDialog()
        sett_dialog.show()
        result = sett_dialog.exec_()
