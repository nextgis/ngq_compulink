"""
/***************************************************************************
 RuGeocoder
                                 A QGIS plugin
 Geocode your csv files to shp
                              -------------------
        begin                : 2012-02-20
        copyright            : (C) 2012 by Nikulin Evgeniy
        email                : nikulin.e at gmail
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
from os import path
import sys
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QObject, SIGNAL, QSettings, QLocale, QFileInfo, QTranslator, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import QgsApplication
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from batch_geocoding_dialog import BatchGeocodingDialog
from converter_dialog import ConverterDialog
from quick_geocoding_toolbox import  QuickGeocodingToolbox
from plugin_settings import PluginSettings


_fs_encoding = sys.getfilesystemencoding()
_current_path = unicode(path.abspath(path.dirname(__file__)), _fs_encoding)


class RuGeocoderPlugin:

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RuGeocoder', message)


    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # i18n support
        override_locale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not override_locale:
            locale_full_name = QLocale.system().name()
        else:
            locale_full_name = QSettings().value('locale/userLocale', '', type=unicode)

        self.locale_path = '%s/i18n/rugeocoder_%s.qm' % (_current_path, locale_full_name[0:2])
        if QFileInfo(self.locale_path).exists():
            self.translator = QTranslator()
            self.translator.load(self.locale_path)
            QCoreApplication.installTranslator(self.translator)

        # menu && toolbars
        self.menu_name = self.tr(u'&RuGeocoder')
        self.toolbar = self.iface.addToolBar(self.menu_name)
        self.toolbar.setObjectName(u'RuGeocoderToolbar')

        # instances
        self.__converter_dlg = ConverterDialog()
        self.__geocoder_dlg = BatchGeocodingDialog()

        # Dock tree panel
        self.__quick_tlb = QuickGeocodingToolbox(self.iface)
        self.iface.addDockWidget(PluginSettings.dock_area(), self.__quick_tlb)
        self.__quick_tlb.setFloating(PluginSettings.dock_floating())
        self.__quick_tlb.resize(PluginSettings.dock_size())
        self.__quick_tlb.move(PluginSettings.dock_pos())
        self.__quick_tlb.setVisible(PluginSettings.dock_visibility())
        self.__quick_tlb.set_active_geocoder(PluginSettings.dock_geocoder_name())
        self.__quick_tlb.setWindowIcon(QIcon(path.join(_current_path, 'edit-find-project.png')))


    def initGui(self):
        # Actions
        self.action_convert = QAction(QIcon(':/plugins/rugeocoderplugin/convert.png'),
                                      QCoreApplication.translate('RuGeocoder', 'Convert CSV to SHP'),
                                      self.iface.mainWindow())
        QObject.connect(self.action_convert, SIGNAL("triggered()"), self.run_convert)

        self.action_batch_geocoding = QAction(QIcon(':/plugins/rugeocoderplugin/icon.png'),
                                              QCoreApplication.translate('RuGeocoder', 'Batch geocoding'),
                                              self.iface.mainWindow())
        QObject.connect(self.action_batch_geocoding, SIGNAL('triggered()'), self.run_batch)

        self.action_quick_geocoding = self.__quick_tlb.toggleViewAction()
        self.action_quick_geocoding.setIcon(QIcon(path.join(_current_path, 'edit-find-project.png')))
        self.action_quick_geocoding.setText(QCoreApplication.translate('RuGeocoder', '&Quick geocoding toolbox'))

        # Add toolbar button and menu item
        self.toolbar.addAction(self.action_convert)
        self.iface.addPluginToWebMenu(self.menu_name, self.action_convert)

        self.toolbar.addAction(self.action_batch_geocoding)
        self.iface.addPluginToWebMenu(self.menu_name, self.action_batch_geocoding)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.action_quick_geocoding)
        self.iface.addPluginToWebMenu(self.menu_name, self.action_quick_geocoding)

        #import pydevd
        #pydevd.settrace('localhost', port=9921, stdoutToServer=True, stderrToServer=True, suspend=False)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginWebMenu(self.menu_name, self.action_convert)
        self.iface.removePluginWebMenu(self.menu_name, self.action_batch_geocoding)
        self.iface.removePluginWebMenu(self.menu_name, self.action_quick_geocoding)

        self.action_convert = None
        self.action_batch_geocoding = None
        self.action_quick_geocoding = None
        self.toolbar = None

        mw = self.iface.mainWindow()
        PluginSettings.set_dock_area(mw.dockWidgetArea(self.__quick_tlb))
        PluginSettings.set_dock_floating(self.__quick_tlb.isFloating())
        PluginSettings.set_dock_pos(self.__quick_tlb.pos())
        PluginSettings.set_dock_size(self.__quick_tlb.size())
        PluginSettings.set_dock_visibility(self.__quick_tlb.isVisible())
        PluginSettings.set_dock_geosoder_name(self.__quick_tlb.get_active_geocoder_name())

        self.iface.removeDockWidget(self.__quick_tlb)
        del self.__quick_tlb



    def run_convert(self):
        if not self.__converter_dlg.isVisible():
            self.__converter_dlg = ConverterDialog()
            self.__converter_dlg.show()
            self.__converter_dlg.exec_()

    def run_batch(self):
        if not self.__geocoder_dlg.isVisible():
            self.__geocoder_dlg = BatchGeocodingDialog()
            self.__geocoder_dlg.show()
            self.__geocoder_dlg.exec_()
