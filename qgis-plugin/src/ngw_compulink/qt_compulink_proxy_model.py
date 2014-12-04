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
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSortFilterProxyModel


class QCompulinkProxyModel(QSortFilterProxyModel):

    def filterAcceptsColumn(self, col, index):
        return True

    def filterAcceptsRow(self, row, index):
        item = self.sourceModel().index(row, 0, index).internalPointer()
        data = item.data(Qt.UserRole)
        return data.common.cls in ['resource_group', 'focl_project'] #  TODO: remake!