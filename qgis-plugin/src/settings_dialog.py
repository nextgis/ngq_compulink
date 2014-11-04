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

__author__ = 'NextGIS'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, NextGIS'

# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from PyQt4 import uic
from PyQt4.QtGui import QDialog

from new_ngw_connection_dialog import NewNGWConnectionDialog
from plugin_settings import PluginSettings


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings_dialog_base.ui'))


class SettingsDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.btnNew.clicked.connect(self.new_connection)
        self.btnEdit.clicked.connect(self.edit_connection)
        self.btnDelete.clicked.connect(self.delete_connection)

        self.populate_connection_list()

    def new_connection(self):
        dlg = NewNGWConnectionDialog(self)
        if dlg.exec_():
            self.populate_connection_list()
        del dlg

    def edit_connection(self):
        dlg = NewNGWConnectionDialog(self, self.cmbConnections.currentText())
        if dlg.exec_():
            self.populate_connection_list()
        del dlg

    def delete_connection(self):
        PluginSettings.remove_connection(self.cmbConnections.currentText())
        self.populate_connection_list()

    def populate_connection_list(self):
        self.cmbConnections.clear()
        self.cmbConnections.addItems(PluginSettings.get_connection_names())

        last_connection = PluginSettings.get_last_connection()
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
        PluginSettings.set_last_connection(self.cmbConnections.currentText())
        QDialog.reject(self)
