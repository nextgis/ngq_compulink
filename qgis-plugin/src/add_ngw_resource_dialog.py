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

from os import path

from PyQt4 import uic
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import Qt
from qgis.core import QgsMapLayerRegistry, QgsProject, QgsVectorLayer, QgsMessageLog

from ngw_api.ngw_wfs_service import NGWWfsService
from ngw_api.qt_ngw_resources_model import QNGWResourcesModel
from ngw_compulink.ngw_focl_struct import NGWFoclStruct
from ngw_compulink.ngw_situation_plan import NGWSituationPlan
from ngw_compulink.qt_compulink_resources_model import QNGWCompulinkResourceItem


FORM_CLASS, _ = uic.loadUiType(path.join(
    path.dirname(__file__), 'add_ngw_resource_dialog_base.ui'))


class AddNgwResourceDialog(QDialog, FORM_CLASS):
    def __init__(self, ngw_root_resource, parent=None):
        super(AddNgwResourceDialog, self).__init__(parent)
        self.setupUi(self)

        #model
        self._root_item = QNGWCompulinkResourceItem(ngw_root_resource, None)
        self._resource_model = QNGWResourcesModel(self._root_item)
        #self._proxy_model = QCompulinkProxyModel()
        #self._proxy_model.setSourceModel(self._resource_model)
        self.trvResources.setModel(self._resource_model) #(self._proxy_model)

        self.btnAdd.clicked.connect(self.add_resource)
        self.btnClose.clicked.connect(self.reject)
        self.trvResources.selectionModel().currentChanged.connect(self.active_item_chg)


    def active_item_chg(self, selected, deselected):
        ngw_resource = selected.data(Qt.UserRole)
        if ngw_resource.common.cls in [NGWFoclStruct.type_id, NGWSituationPlan.type_id]:
            self.btnAdd.setEnabled(True)
        else:
            self.btnAdd.setDisabled(True)


    def add_resource(self):
        sel_index = self.trvResources.selectionModel().currentIndex()
        if sel_index.isValid():
            ngw_resource = sel_index.data(Qt.UserRole)
            self._append_resource_to_map(ngw_resource)



    def _append_resource_to_map(self, ngw_resource):
        children = ngw_resource.get_children()
        wfs_resources = [ch for ch in children if isinstance(ch, NGWWfsService)]
        if len(wfs_resources) < 1:
            #TODO: show error
            return
        wfs_resource = wfs_resources[0]

        #Serach/Add group
        toc_root = QgsProject.instance().layerTreeRoot()


        layers_group = toc_root.insertGroup(0, ngw_resource.common.display_name)

        styles_path = path.join(path.dirname(__file__), 'styles/', ngw_resource.common.cls + '/')

        #Add layers
        for wfs_layer in wfs_resource.wfs.layers:
            url = wfs_resource.get_wfs_url(wfs_layer.keyname) + '&srsname=EPSG:3857&VERSION=1.0.0&REQUEST=GetFeature'
            qgs_wfs_layer = QgsVectorLayer(url, wfs_layer.display_name, 'WFS')

            QgsMapLayerRegistry.instance().addMapLayer(qgs_wfs_layer, False)
            layers_group.insertLayer(0, qgs_wfs_layer)

            layer_style_path = path.join(styles_path, wfs_layer.keyname + '.qml')
            if path.isfile(layer_style_path):
                qgs_wfs_layer.loadNamedStyle(layer_style_path)
            else:
                message = self.tr('Style for layer "%s" (%s) not found!') % (wfs_layer.display_name, wfs_layer.keyname)
                QgsMessageLog.logMessage(message, level=QgsMessageLog.WARNING)