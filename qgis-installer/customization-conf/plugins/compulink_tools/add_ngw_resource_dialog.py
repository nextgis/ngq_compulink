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
from PyQt4.QtGui import QDialog, QIcon
from PyQt4.QtCore import Qt
from qgis.core import QgsMapLayerRegistry, QgsProject, QgsVectorLayer, QgsMessageLog, QgsRectangle, QgsMapLayer


from ngw_api.core.ngw_wfs_service import NGWWfsService
from ngw_api.qt.qt_ngw_resource_model import QNGWResourcesModel
from ngw_compulink.ngw_focl_struct import NGWFoclStruct
from ngw_compulink.ngw_situation_plan import NGWSituationPlan
from ngw_compulink.ngw_focl_proj import NGWFoclProject
from ngw_compulink.qt_compulink_resource_model import QNGWCompulinkResourceItem


FORM_CLASS, _ = uic.loadUiType(path.join(
    path.dirname(__file__), 'add_ngw_resource_dialog_base.ui'))


class AddNgwResourceDialog(QDialog, FORM_CLASS):
    def __init__(self, ngw_root_resource, parent=None, iface=None):
        super(AddNgwResourceDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(path.dirname(__file__) + '/icon_list.png'))
        self._iface = iface


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
        if ngw_resource.common.cls in [NGWFoclStruct.type_id, NGWSituationPlan.type_id, NGWFoclProject.type_id]:
            self.btnAdd.setEnabled(True)
        else:
            self.btnAdd.setDisabled(True)


    def add_resource(self):
        sel_index = self.trvResources.selectionModel().currentIndex()
        if sel_index.isValid():
            #extent for_zoom
            summary_extent = QgsRectangle()
            summary_extent.setMinimal()

            self.hide() #hack
            ngw_resource = sel_index.data(Qt.UserRole)
            if ngw_resource.common.cls == NGWFoclProject.type_id:
                for child in ngw_resource.get_children():
                    self._append_resource_to_map(child, ngw_resource, summary_extent)
            else:
                parent_resource = sel_index.parent().data(Qt.UserRole)
                self._append_resource_to_map(ngw_resource, parent_resource, summary_extent)

            self.zoom_to_extent(summary_extent)
            self.close()

    def zoom_to_extent(self, extent):
        if not self._iface or not extent or extent.isNull():
            return
        extent.scale(1.05)
        self._iface.mapCanvas().setExtent(extent)
        self._iface.mapCanvas().refresh()


    def _append_resource_to_map(self, ngw_resource, parent_resource, summary_extent):
        children = ngw_resource.get_children()
        wfs_resources = [ch for ch in children if isinstance(ch, NGWWfsService)]
        if len(wfs_resources) < 1:
            #TODO: show error
            return
        wfs_resource = wfs_resources[0]

        #Serach/Add group
        toc_root = QgsProject.instance().layerTreeRoot()

        parent_group = toc_root.findGroup(parent_resource.common.display_name)
        if not parent_group:
            parent_group = toc_root.insertGroup(0, parent_resource.common.display_name)

        layers_group = parent_group.insertGroup(0, ngw_resource.common.display_name)
        #layers_group.setExpanded(False)

        styles_path = path.join(path.dirname(__file__), 'styles/', ngw_resource.common.cls + '/')

        #Add layers
        for wfs_layer in wfs_resource.wfs.layers:
            url = wfs_resource.get_wfs_url(wfs_layer.keyname) + '&srsname=EPSG:3857&VERSION=1.0.0&REQUEST=GetFeature'
            qgs_wfs_layer = QgsVectorLayer(url, wfs_layer.display_name, 'WFS')

            #summarize extent
            self._summ_extent(summary_extent, qgs_wfs_layer)

            QgsMapLayerRegistry.instance().addMapLayer(qgs_wfs_layer, False)
            toc_layer = layers_group.insertLayer(0, qgs_wfs_layer)
            toc_layer.setExpanded(False)

            layer_style_path = path.join(styles_path, wfs_layer.keyname + '.qml')
            if path.isfile(layer_style_path):
                qgs_wfs_layer.loadNamedStyle(layer_style_path)
            else:
                message = self.tr('Style for layer "%s" (%s) not found!') % (wfs_layer.display_name, wfs_layer.keyname)
                QgsMessageLog.logMessage(message, level=QgsMessageLog.WARNING)

    def _summ_extent(self, summary_extent, layer):
        layer_extent = layer.extent()

        if layer_extent.isEmpty() and layer.type() == QgsMapLayer.VectorLayer:
            layer.updateExtents()
            layer_extent = layer.extent()

        if layer_extent.isNull():
            return

        if self._iface.mapCanvas().hasCrsTransformEnabled():
            layer_extent = self._iface.mapCanvas().mapRenderer().layerExtentToOutputExtent(layer, layer_extent)

        summary_extent.combineExtentWith(layer_extent)