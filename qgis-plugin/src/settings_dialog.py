# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SettingsDialog
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

__author__ = 'NextGIS'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, NextGIS'

# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from PyQt4 import uic
from PyQt4.QtGui import QDialog, QIcon

from ngw_api.qgis.ngw_connection_edit_dialog import NGWConnectionEditDialog
from plugin_settings import PluginSettings


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings_dialog_base.ui'))


class SettingsDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon(os.path.dirname(__file__) + '/icon_settings.png'))

        self.btnNew.clicked.connect(self.new_connection)
        self.btnEdit.clicked.connect(self.edit_connection)
        self.btnDelete.clicked.connect(self.delete_connection)

        self.populate_connection_list()

    def new_connection(self):
        dlg = NGWConnectionEditDialog()
        if dlg.exec_():
            conn_sett = dlg.ngw_connection_settings
            PluginSettings.save_ngw_connection(conn_sett)
            self.populate_connection_list()
        del dlg

    def edit_connection(self):
        conn_name = self.cmbConnections.currentText()
        conn_sett = None

        if conn_name is not None:
            conn_sett = PluginSettings.get_ngw_connection(conn_name)

        dlg = NGWConnectionEditDialog(ngw_connection_settings=conn_sett)
        if dlg.exec_():
            conn_sett = dlg.ngw_connection_settings
            # if conn was renamed - remove old
            if conn_name is not None and conn_name != conn_sett.connection_name:
                PluginSettings.remove_ngw_connection(conn_name)
            # save new
            PluginSettings.save_ngw_connection(conn_sett)
            self.populate_connection_list()
        del dlg

    def delete_connection(self):
        PluginSettings.remove_ngw_connection(self.cmbConnections.currentText())
        self.populate_connection_list()

    def populate_connection_list(self):
        self.cmbConnections.clear()
        self.cmbConnections.addItems(PluginSettings.get_ngw_connection_names())

        last_connection = PluginSettings.get_selected_ngw_connection_name()
        idx = self.cmbConnections.findText(last_connection)
        if idx == -1 and self.cmbConnections.count() > 0:
            self.cmbConnections.setCurrentIndex(0)
        else:
            self.cmbConnections.setCurrentIndex(idx)

        if self.cmbConnections.count() == 0:
            self.btnEdit.setEnabled(False)
            self.btnDelete.setEnabled(False)
        else:
            self.btnEdit.setEnabled(True)
            self.btnDelete.setEnabled(True)

    def reject(self):
        PluginSettings.set_selected_ngw_connection_name(self.cmbConnections.currentText())
        QDialog.reject(self)
