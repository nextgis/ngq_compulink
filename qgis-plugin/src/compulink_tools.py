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
        email                : info@nextgis.com
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
from qgis.core import QgsMapLayerRegistry, QgsRasterLayer, QgsMessageLog, QgsApplication
from qgis.gui import QgsMessageBar
from os import path
from add_ngw_resource_dialog import AddNgwResourceDialog
from ngw_api.ngw_resource_factory import NGWResourceFactory
from ngw_compulink.ngw_focl_struct import NGWFoclStruct
from ngw_compulink.ngw_focl_proj import NGWFoclProject
from ngw_compulink.ngw_situation_plan import NGWSituationPlan
from plugin_settings import PluginSettings
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
        self.plugin_dir = path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = path.join(
            self.plugin_dir,
            'i18n',
            'CompulinkToolsPlugin_{}.qm'.format(locale))

        if path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Compulink tools')
        self.toolbar = self.iface.addToolBar(self.tr(u'&Compulink tools'))
        self.toolbar.setObjectName(u'CompulinkToolsPlugin')

        # SETUP ENV
        self.check_styles_paths()

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

    def check_styles_paths(self):
        plugin_svg_path = path.join(self.plugin_dir, 'svg/')
        svg_paths = QgsApplication.svgPaths()
        if not plugin_svg_path in svg_paths:
            svg_paths.append(plugin_svg_path)
            QgsApplication.setDefaultSvgPaths(svg_paths)


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        #Tools for NGW communicate
        icon_path = self.plugin_dir + '/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Add projects layers'),
            callback=self.add_layers_from_ngw,
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
        #import pydevd
        #pydevd.settrace('localhost', port=5566, stdoutToServer=True, stderrToServer=True, suspend=False)

        conn_name = PluginSettings.get_last_connection_name()
        if not conn_name:
            error_message = self.tr('You must configure at least one connection!')
            self.iface.messageBar().pushMessage(self.tr('WARNING'),
                                                error_message,
                                                level=QgsMessageBar.WARNING)
            QgsMessageLog.logMessage(error_message, level=QgsMessageLog.WARNING)
            return
        conn_sett = PluginSettings.get_connection(conn_name)

        #setup ngw api
        rsc_factory = NGWResourceFactory(conn_sett)
        types_reg = rsc_factory.resources_types_registry
        types_reg[NGWFoclStruct.type_id] = NGWFoclStruct
        types_reg[NGWFoclProject.type_id] = NGWFoclProject
        types_reg[NGWSituationPlan.type_id] = NGWSituationPlan

        try:
            root_rsc = rsc_factory.get_root_resource()
        except Exception, e:
            error_message = self.tr('Error on fetch resources: ') + e.message
            self.iface.messageBar().pushMessage(self.tr('ERROR'),
                                                error_message,
                                                level=QgsMessageBar.CRITICAL)
            QgsMessageLog.logMessage(error_message, level=QgsMessageLog.CRITICAL)
            return

        res_dialog = AddNgwResourceDialog(root_rsc)
        res_dialog.exec_()

    def settings(self):
        sett_dialog = SettingsDialog()
        sett_dialog.show()
        result = sett_dialog.exec_()
