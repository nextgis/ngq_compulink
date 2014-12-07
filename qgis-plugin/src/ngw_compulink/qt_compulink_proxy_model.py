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
!!!
Прокси модель для QNGWResourcesModel из NGW API
Малая скорость работы: при построении дерева запрашивает два уровня иерархии.
!!!
"""
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSortFilterProxyModel
from ..ngw_api.ngw_group_resource import NGWGroupResource
from ngw_focl_proj import NGWFoclProject
from ngw_focl_struct import NGWFoclStruct
from ngw_situation_plan import NGWSituationPlan


class QCompulinkProxyModel(QSortFilterProxyModel):

    def filterAcceptsColumn(self, col, index):
        return True

    def filterAcceptsRow(self, row, index):
        item = self.sourceModel().index(row, 0, index).internalPointer()
        data = item.data(Qt.UserRole)
        return data.common.cls in [
            NGWGroupResource.type_id,
            NGWFoclStruct.type_id,
            NGWFoclProject.type_id,
            NGWSituationPlan.type_id]