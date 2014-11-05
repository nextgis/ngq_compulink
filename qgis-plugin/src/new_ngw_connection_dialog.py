# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 New NGW connection dialog
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
import os
from PyQt4 import uic
from PyQt4.QtGui import QDialog

from plugin_settings import PluginSettings
from ngw_api import NGWConnectionSettings

__author__ = 'NextGIS'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, NextGIS'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'new_ngw_connection_dialog_base.ui'))


class NewNGWConnectionDialog(QDialog, FORM_CLASS):
    def __init__(self, parent, connection_name=None):
        super(NewNGWConnectionDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.connection_name = connection_name

        if self.connection_name is not None:
            conn_sett = PluginSettings.get_connection(self.connection_name)
            self.leName.setText(conn_sett.connection_name)
            self.leUrl.setText(conn_sett.url)
            self.leUser.setText(conn_sett.user)
            self.lePassword.setText(conn_sett.password)

    def accept(self):
        if self.connection_name is not None and \
                self.connection_name != self.leName.text():
            PluginSettings.remove_connection(self.connection_name)

        conn_sett = NGWConnectionSettings(
            self.leName.text(),
            self.leUrl.text(),
            self.leUser.text(),
            self.lePassword.text())
        PluginSettings.save_connection(conn_sett)

        QDialog.accept(self)
