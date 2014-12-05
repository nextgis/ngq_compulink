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
from ngw_api.qt_ngw_resources_model import QNGWResourceItem, QNGWResourcesModel
from ngw_compulink.qt_compulink_proxy_model import QCompulinkProxyModel
from ngw_compulink.qt_compulink_resources_model import QNGWCompulinkResourceItem

__author__ = 'NextGIS'
__date__ = 'October 2014'
__copyright__ = '(C) 2014, NextGIS'

# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os
from PyQt4 import uic
from PyQt4.QtGui import QDialog


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'add_ngw_resource_dialog_base.ui'))


class AddNgwResourceDialog(QDialog, FORM_CLASS):
    def __init__(self, ngw_root_resource, parent=None):
        super(AddNgwResourceDialog, self).__init__(parent)
        self.setupUi(self)


        self.btnAdd.clicked.connect(self.add_resource)
        self.btnClose.clicked.connect(self.reject)

        #model
        self._root_item = QNGWCompulinkResourceItem(ngw_root_resource, None)
        self._resource_model = QNGWResourcesModel(self._root_item)
        #self._proxy_model = QCompulinkProxyModel()
        #self._proxy_model.setSourceModel(self._resource_model)
        self.trvResources.setModel(self._resource_model) #(self._proxy_model)


    def add_resource(self):
        pass