# -*- coding: utf-8 -*-
"""
/***************************************************************************
    NextGIS WEB Compulink API
                              -------------------
        begin                : 2014-11-19
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
!!!
Элемент модели дерева для NGW Compulink.
Строит дерево сразу с фильтрацией по типам и правам
Запрос дочерних элементов только для одного уровня иерархии
!!!
"""
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon

from ..ngw_api.ngw_group_resource import NGWGroupResource
from ngw_focl_proj import NGWFoclProject
from ngw_focl_struct import NGWFoclStruct
from ngw_situation_plan import NGWSituationPlan


class QNGWCompulinkResourceItem():
    def __init__(self, ngw_resource, parent):
        self._ngw_resource = ngw_resource
        self._parent = parent
        self._children = []  # lazy load
        self._children_loads = False
        print unicode(self.data(Qt.DisplayRole)), ' created!'  # debug

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent.get_children().index(self)
        else:
            return 0

    def get_children(self):
        if not self._children_loads:
            self._load_children()
        return self._children

    def get_child(self, row):
        if not self._children_loads:
            self._load_children()
        return self._children[row]

    def get_children_count(self):
        if not self._children_loads:
            self._load_children()
        return len(self._children)

    def _load_children(self):
        resource_children = self._ngw_resource.get_children()

        self._children = []
        for resource_child in resource_children:
            if resource_child.common.cls in [
                NGWGroupResource.type_id,
                NGWFoclStruct.type_id,
                NGWFoclProject.type_id,
                NGWSituationPlan.type_id,
            ]:
                self._children.append(QNGWCompulinkResourceItem(resource_child, self))

        self._children_loads = True

    def has_children(self):
        return self._ngw_resource.common.children

    def data(self, role):
        if role == Qt.DisplayRole:
            return self._ngw_resource.common.display_name
        if role == Qt.DecorationRole:
            return QIcon(self._ngw_resource.icon_path)
        if role == Qt.ToolTipRole:
            return self._ngw_resource.type_title
        if role == Qt.UserRole:
            return self._ngw_resource
